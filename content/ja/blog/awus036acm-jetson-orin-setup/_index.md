---
title: "ドライバーコンパイル不要！ALFA AWUS036ACM を Jetson Orin エッジ AI ホストでプラグ＆プレイする実践ガイド"
description: "AVALUE AIB-NW01（NVIDIA Jetson Orin NX/Nano）ユーザー向けに、エッジ AI デプロイに最適な ALFA Network USB 無線アダプターを徹底分析し、AWUS036ACM がなぜ真のプラグ＆プレイを実現できるのかを実証的に解説します。"
date: 2026-05-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Jetson-Orin", "Edge-AI", "USB-WiFi", "AWUS036ACM", "AVALUE", "AIB-NW01"]
featureimage: "/images/blog/awus036acm-jetson-orin-setup.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "USB WiFiアダプターがJetson Orinでよく使えないのはなぜですか？"
    answer: "JetsonはNVIDIAカスタムTegraカーネルを使用し、標準Ubuntuカーネルではありません。サードパーティドライバーはカーネルheadersが取得できないかABI非互換でコンパイルに失敗することがよくあります。"
  - question: "AWUS036ACMはJetson Orinでドライバーをコンパイルする必要がありますか？"
    answer: "不要です。MT7612Uチップのmt76x2uドライバーはLinux Kernel 4.19以降カーネルメインラインに内蔵され、AIB-NW01のKernel 5.10に既に含まれており、挿すだけで使えます。"
  - question: "AWUS036ACH（RTL8812AU）はJetson Orinで使えますか？"
    answer: "使えますがドライバーの手動コンパイルが必要です。JetPackのNVIDIA kernel patchesがcfg80211 ABIを破壊しコンパイル失敗を引き起こす可能性があるため、コンパイル経験のある方にお勧めします。"
  - question: "JetPackアップグレードでUSB WiFiアダプターが使えなくなりますか？"
    answer: "可能性があります。サードパーティドライバーはJetPackアップグレード後にカーネルAPI変更で無効になることがあり、再コンパイルが必要です。カーネル内蔵ドライバー（mt76x2uなど）は影響を受けません。"
  - question: "AIB-NW01はどのLinuxカーネルバージョンを使用していますか？"
    answer: "AIB-NW01は工場出荷時Ubuntu 20.04.6 LTSとJetPack 5.0を搭載し、NVIDIAカスタムTegraカーネル5.10.x-tegraを使用、CPUアーキテクチャはARM64です。"
---
> 「AVALUE AIB-NW01（Jetson Orin NX）を有線ネットワークのない環境に設置する予定です。御社の USB 無線アダプターでそのまま使えるのはどれですか？」

## 一通の顧客からの問い合わせが、重要な課題を浮き彫りにした


{{< tldr >}}
Jetson OrinはNVIDIAカスタムTegraカーネルを使用し、サードパーティWiFiドライバーのコンパイルがよく失敗します。ALFA AWUS036ACMはMT7612Uチップを採用し、ドライバーはKernel 4.19以降カーネルに内蔵、挿すだけで使えて唯一の真のコンパイル不要ソリューションです。モニターモード、パケットインジェクション、APモードをサポートします。
{{< /tldr >}}
これは Yupitek に最近寄せられた問い合わせだ。一見シンプルな質問だが、Jetson 開発者コミュニティにしばらくいればわかることだが——**USB 無線アダプターは NVIDIA Jetson プラットフォーム上では想像以上に扱いが難しい。**

Jetson のコアアーキテクチャ、NVIDIA フォーラムの実例、GitHub 上のドライバーコンパイル失敗報告、そして ARM64 プラットフォームでの実測データまでを追跡し、この選定ガイドをまとめた。

---

## AIB-NW01 の無線接続オプション：まずはプラットフォームを理解する

AVALUE AIB-NW01 は、エッジ AI アプリケーション向けに設計された**ファンレス組み込みシステム**であり、4 種類の NVIDIA Jetson Orin SoM 構成を提供する。以下に完全なハードウェア仕様とソフトウェア環境を示す。

### ハードウェア仕様概要

| 項目 | 仕様 |
|------|------|
| **SoM オプション** | Jetson Orin NX 16GB / NX 8GB / Orin Nano 8GB / Orin Nano 4GB |
| **CPU** | ARM Cortex-A78AE v8.2 64-bit（NX 16GB: 8-core @ 2.0 GHz / NX 8GB: 6-core @ 2.0 GHz / Nano: 6-core @ 1.5 GHz） |
| **GPU** | NVIDIA Ampere アーキテクチャ（NX: 1024 CUDA Cores + 32 Tensor Cores / Nano 4GB: 512 CUDA Cores + 16 Tensor Cores） |
| **AI 性能** | 100 / 70 / 40 / 20 TOPS（SoM 構成による） |
| **メモリ** | LPDDR5（NX 16GB/8GB: 128-bit 102.4 GB/s / Nano 8GB: 128-bit 68 GB/s / Nano 4GB: 64-bit 34 GB/s） |
| **ストレージ** | 128GB M.2 2280 NVMe SSD（内蔵） |
| **ネットワーク** | 2 × GbE RJ-45（10/100/1000 Mbps） |
| **USB** | 4 × USB 3.1 Type-A、1 × Micro USB OTG |
| **ディスプレイ** | 1 × HDMI Type-A |
| **シリアルポート** | 2 × DB9（RS-232 / RS-485 ジャンパ切替可能） |
| **拡張スロット** | 1 × M.2 M-Key 2242/2280（NVMe SSD）、1 × M.2 E-Key 2230（WiFi/BT モジュール）、1 × M.2 B-Key 3042/3052（5G/LTE モジュール、常温使用限定） |
| **SIM** | 1 × Micro SIM スロット |
| **電源** | DC 10~24V（2-pin ターミナルブロック） |
| **寸法** | 125 × 196 × 66 mm（壁掛けブラケット除く） |
| **重量** | 1.4 kg |
| **筐体材質** | アルミ押出 + スチールプレート、ファンレス放熱設計 |
| **動作温度** | -15°C ~ 60°C（IEC60068-2 準拠、0.5 m/s 風速） |
| **保管温度** | -40°C ~ 80°C |
| **認証** | CE、FCC Class A |

### ソフトウェア環境

| 項目 | 仕様 |
|------|------|
| **OS** | Ubuntu 20.04.6 LTS (Focal Fossa) |
| **NVIDIA SDK** | JetPack 5.0（CUDA 11.4、cuDNN 8.4、TensorRT 8.4 を含む） |
| **Linux カーネル** | 5.10.x-tegra（NVIDIA カスタム Tegra カーネル、**標準 Ubuntu カーネルではない**） |
| **CPU アーキテクチャ** | ARM64 (aarch64) |
| **AI SDK リソース** | [github.com/Avalue-Technology](https://github.com/Avalue-Technology/repositories.directory) |

> **重要な注意点**：Jetson プラットフォームは、標準の Ubuntu カーネルではなく、NVIDIA がメンテナンスするカスタムカーネル `linux-tegra` を使用している。これはサードパーティドライバーの互換性に大きな影響を及ぼす——詳細は後述の「USB 無線アダプターが Jetson Orin で直面する 3 つの課題」を参照。

本機は以下の 3 つの無線接続経路を提供している：

### M.2 2230 E-Key（WiFi モジュールスロット）

**利点**：高速、マザーボード内蔵、USB ポートを占有しない
**欠点**：分解が必要、アンテナコネクタが筐体内に固定、交換困難、モジュール互換性は逐一検証が必要

### USB 3.1 Type-A（4 ポート）

**利点**：ホットプラグ対応、分解不要、アンテナを最適な信号位置に配置可能、複数デバイス間で共有可能
**欠点**：USB アダプターがやや大きい、速度上限は USB インターフェースに依存

### 5G M.2 B-Key（オプション）

**利点**：独立した接続、現場の WiFi インフラに依存しない
**欠点**：コスト高、SIM カードと月額プランが必要、設定が複雑

ほとんどのエッジ AI デプロイメントシナリオ——PoC フェーズ、屋外監視、工場生産ライン——において、**USB 無線アダプターは最も柔軟性が高く、コストも最も低い選択肢である。**

しかし問題はここからだ。適当な USB WiFi アダプターを買って Jetson に挿せば使えるのか？

答えは：**必ずしもそうではない。そして失敗する確率は想像以上に高い。**

---

## USB 無線アダプターが Jetson Orin で直面する 3 つの課題

ほとんどの USB WiFi 記事は x86 Linux についてしか語らないが、Jetson プラットフォームはまったく別の世界だ。

### 課題 1：あなたのカーネルは Ubuntu カーネルではない

Jetson が動作させているのは **NVIDIA カスタム Tegra Linux カーネル**であり、標準の Ubuntu カーネルではない。これは以下のことを意味する：

- `apt install linux-headers-$(uname -r)` は**対応するカーネルヘッダーを取得できない**可能性が高い
- NVIDIA はカーネルにパッチを適用しており、サードパーティドライバーが必要とする ABI を破壊する可能性がある
- カーネルモジュールのコンパイル環境が x86 デスクトップとは完全に異なる

一般的な「Linux 対応」USB アダプターは、**Jetson 上でコンパイルが成功するとは限らない。**

### 課題 2：サードパーティドライバーのコンパイルが Jetson では頻繁に失敗する

GitHub 上の実例（2025 年 4 月）：JetPack 6.2（kernel 5.15.148-tegra）において、RTL8812EU ドライバーの `make` と `dkms` の両方がエラーを発生させた。コミュニティの解析により判明したのは——**JetPack の NVIDIA カーネルパッチが cfg80211 ABI を破壊する**ため、サードパーティ WiFi ドライバーが正しくコンパイルできないという事実だ。

> 出典：[GitHub issue #421 — RTL8812EU Driver Compilation Failed on Jetson Orin Nano](https://github.com/svpcom/wfb-ng/issues/421)

### 課題 3：JetPack のアップグレードでアダプターが「使えなくなる」可能性

NVIDIA フォーラムの事例（2024 年 10 月）：RTL8188EUS が JetPack 5.1.x では正常動作していたが、JetPack 6 にアップグレード後**完全に認識不能**になった。解決策は GitHub から手動でドライバーを再コンパイルすること——しかし新しい JetPack でまたカーネル API が変更されたらどうするのか？

> 出典：[Jetson Orin Nano — JetPack 6 が RTL8188EUS をサポートしていない](https://nvidia-jetson.piveral.com/jetson-orin-nano/jetpack-6-doesnt-support-rtl8188eus/)

### 教訓：まとめ

> **Jetson プラットフォームにおいて、唯一本当に信頼できる選択肢は、Linux カーネル内蔵（in-kernel）ドライバーを持つ USB 無線アダプターである。**

なぜなら NVIDIA はカーネル内蔵ドライバーの互換性を維持せざるを得ないからだ——これこそが、JetPack アップグレード後もアダプターが使い続けられる唯一の保証である。

---

## チップセット互換性総覧：一枚の表で理解する

以下に Jetson Orin で一般的な ALFA Network USB 無線アダプターのチップセット互換性をまとめる：

| チップセット | ALFA モデル | ドライバー方式 | 最低 Kernel 要件 | Jetson Orin 判定 |
|------|-----------|----------|-----------------|------------------|
| **MT7612U** | **AWUS036ACM** | **In-kernel (mt76x2u)** | **4.19+** | ✅ 完全互換、プラグ＆プレイ |
| RTL8812AU | AWUS036ACH | Out-of-tree（コンパイル要） | 手動コンパイル要 | ⚠️ 検討可能だがコンパイルリスクあり |
| RTL8811AU | AWUS036ACS | Out-of-tree（コンパイル要） | 手動コンパイル要 | ⚠️ RTL8812AU と同様の問題 |
| RTL8812BU | AWUS036AX | Out-of-tree（コンパイル要） | 手動コンパイル要 | ⚠️ コンパイル要、既知の問題あり |
| MT7921AU | AWUS036AXM | In-kernel (mt7921u) | **5.18+** | ❌ K5.10/5.15 では要件未達 |
| RTL8832CU | AWUS036AXER | Out-of-tree（コンパイル要） | 手動コンパイル要 | ❌ 非推奨、ARM64 サポート不明 |

データ出典：[morrownr/USB-WiFi チップセットサポート表](https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Chipsets.md)

---

## 最優先推奨：ALFA AWUS036ACM（MediaTek MT7612U）

### 製品仕様早見

| 項目 | 内容 |
|------|------|
| チップセット | MediaTek MT7612U / MT7612UN |
| WiFi 規格 | 802.11ac (WiFi 5) デュアルバンド AC1200 |
| ピークスループット | 5 GHz: 867 Mbps / 2.4 GHz: 300 Mbps |
| アンテナ | 2 × RP-SMA 着脱式 5 dBi デュアルバンドアンテナ |
| インターフェース | USB 3.0（USB-C コネクタ） |
| 送信出力 | 標準出力、USB ポート直挿しに最適 |

**製品ページ**：https://yupitek.com/ja/products/alfa/awus036acm/

### 推奨理由 1：唯一の「真のドライバーレス」ソリューション

AWUS036ACM が搭載する MT7612U チップセットのドライバー `mt76x2u` は、**Linux Kernel 4.19（2018 年 10 月）**以降、カーネルメインラインに組み込まれている。AIB-NW01 のカーネルバージョンは 5.10.x であるため：

**挿すだけで使える。コンパイル不要、設定不要。**

これは Jetson プラットフォームにおいて極めて重要だ——前述の 3 つの課題（カスタムカーネル、コンパイル失敗、アップグレードによる無効化）を完全に回避できる。

### 推奨理由 2：ARM64 プラットフォームでの実証済み

GitHub ユーザーが ARM64 + Kernel 5.10.198 環境で AWUS036ACM をテストした結果：

```
$ lsusb | grep MediaTek
ID 0e8d:7612 MediaTek Inc. MT7612U

$ dmesg | grep mt76
mt76x2u 1-1:1.0 wlx00c0ca9821a5: renamed from wlan0
```

**開梱即使用可能**、モジュール名は `mt76x2u`、追加の手順は一切不要。

> 出典：[GitHub issue #574 — AWUS036ACM on ARM64 K5.10](https://github.com/morrownr/USB-WiFi/issues/574)

### 推奨理由 3：完全なプロフェッショナル機能対応

このアダプターは単にインターネットに接続できるだけでなく、無線ネットワークのプロフェッショナル機能をフルサポートしている：

- モニターモード (Monitor mode) — ネットワーク診断・解析に最適
- パケットインジェクション (Packet injection) — ペネトレーションテスト・研究に最適
- AP モード — AIB-NW01 を WiFi ホットスポットに変換可能（5 GHz では `disable_usb_sg` モジュールパラメータが必要な場合あり）
- VIF (Virtual Interface) — 同一アダプター上で monitor + managed インターフェースを同時実行可能

### 推奨理由 4：アンテナの柔軟性は比類なし

2 × RP-SMA 外部アンテナ設計により、以下のことが可能になる：

- 高ゲインアンテナ（9 dBi など）に交換してカバレッジを拡大
- 指向性アンテナを使用して特定方向に信号を集中
- 延長ケーブルでアンテナを金属筐体外に延伸（産業用ラック環境では特に重要）

---

## AWUS036ACM がもたらす 5 つの具体的メリット

### メリット 1：即時接続、デプロイ遅延ゼロ

挿入後、即座にシステムに `wlan0`（または `wlx...`）インターフェースとして認識される。ユーザーはわずか 3 つのコマンドで完了：

```bash
# 利用可能なネットワークをスキャン
sudo nmcli device wifi list

# 接続
sudo nmcli device wifi connect "あなたのSSID" password "あなたのパスワード"
```

コンパイル不要、再起動不要、パッケージのインストールも一切不要。

### メリット 2：M.2 WiFi モジュールの全制約を回避

| M.2 WiFi モジュール | USB 無線アダプター (AWUS036ACM) |
|---------------|--------------------------|
| 分解して取り付けが必要 | 外付け、分解不要 |
| アンテナが筐体内に固定 | アンテナを最適な信号位置に配置可能 |
| 交換困難 | ホットプラグ、瞬時に交換 |
| 当該ホストのみで使用可 | 複数デバイス間で共有可能 |

### メリット 3：あらゆる産業用デプロイメントシナリオに対応

エッジ AI プロジェクトの典型的なシナリオにおいて、AWUS036ACM はすべてに対応できる：

- **工場生産ライン** — 装置の近くに有線ポートがない？挿せば即無線接続
- **屋外監視** — WiFi が唯一のデータバックホール回線
- **一時的デプロイ** — PoC 段階、M.2 モジュールを取り付けるために分解したくない
- **移動車両** — AGV/AMR に安定した無線接続が必要

### メリット 4：長期メンテナンスコストが最も低い

in-kernel ドライバーを使用することの実用的な利点：

- JetPack アップグレード後もアダプターはそのまま使用可能（NVIDIA 自身がカーネル内蔵ドライバーをメンテナンス）
- DKMS やドライバーの自己コンパイルを気にする必要なし
- カーネルセキュリティアップデートがブロックされない
- 後続のメンテナンス・サポートコストを削減

### メリット 5：信号カバレッジを要件に応じて最適化可能

2 × RP-SMA 外部アンテナ設計により、このアダプターは調整可能な無線ソリューションでもある。デプロイ環境に応じて：

- 高ゲインアンテナ（9 dBi など）に交換してカバレッジを拡大
- 指向性アンテナで信号を集中
- 延長ケーブルでアンテナを金属筐体外に配置（産業用ラック環境）
- マグネットベースアンテナで金属面に吸着

---

## インストール手順：本当に 3 ステップだけ

### Step 1：挿す

AWUS036ACM を AIB-NW01 の USB 3.0 Type-A ポートに挿入する。

### Step 2：ドライバーがロードされたことを確認

```bash
lsusb | grep MediaTek
# 期待される出力：ID 0e8d:7612 MediaTek Inc. MT7612U

dmesg | grep mt76
# 期待される出力：mt76x2u 1-1:1.0 wlx...: renamed from wlan0
```

### Step 3：WiFi に接続

```bash
# 利用可能なネットワークをスキャン
sudo nmcli device wifi list

# 接続
sudo nmcli device wifi connect "Your_SSID" password "Your_Password"

# 接続状態を確認
ip addr show wlx...
```

完了。あなたの Jetson Orin はネットワークに接続された。

---

## 注意事項と正直な説明

### AWUS036ACM は WiFi 5（AC1200）である

市場最速の選択肢ではない。AWUS036AXM（WiFi 6E、MT7921AU）は理論上より高速だが、AIB-NW01 の Kernel 5.10 では**使用不可**（Kernel 5.18+ が必要）。ほとんどのエッジ AI アプリケーションの帯域要件（データ転送、モデル更新、リモート SSH）に対しては、AC1200 で十分以上である。

### ARM64 での実験的エビデンス

GitHub issue #574 の検証は **Odroid M1**（ARM64 + Kernel 5.10）上で実施されており、AIB-NW01 上で直接テストされたものではない。両者は同一のカーネルアーキテクチャとドライバースタックを使用しているため、結果は一致すると高い確度で確信しているが、ユーザー自身による実機確認を推奨する。

### 他モデルの適用シナリオ

AWUS036ACH（RTL8812AU）および AWUS036AX（RTL8812BU）が使えないわけではなく、単に Jetson 上で手動ドライバーコンパイルが必要なだけである。コンパイル環境の経験があり、ドライバーをメンテナンスする意思があるのであれば、これらのモデルも検討に値する。

---


---

{{< faq >}}

## 結び：最もシンプルなソリューションこそ最善であることが多い

最初の顧客の質問に立ち返ろう：AVALUE AIB-NW01 に最適な ALFA USB 無線アダプターはどれか？

答えは **ALFA AWUS036ACM** である。

最速だからでも最安だからでもない——Jetson のような特殊なプラットフォームにおいて、**唯一本当に挿すだけで使えるソリューション**だからだ。ドライバーのコンパイルすら頻繁に失敗するプラットフォームでは、in-kernel ドライバーこそが王道である。

### 今すぐアクション

- 製品詳細を見る：https://yupitek.com/ja/products/alfa/awus036acm/
- 技術サポート：Yupitek は台湾国内の技術サポートを提供しています。お気軽にお問い合わせください。

### さらに読む

- [AWUS036ACH vs AWUS036ACM：RTL8812AU と MT7612U のドライバー方式完全比較](https://yupitek.com/en/blog/awus036ach-vs-awus036acm/)
- [ALFA Network Linux 互換性総合表](https://docs.alfa.com.tw/Support/Compat/)
- [NVIDIA 公式検証済み WiFi モジュール一覧（AGX Orin）](https://forums.developer.nvidia.com/t/wi-fi-6-6e-7-modules-that-have-been-validated-with-agx-orin-devkits/313431)

---

> **タグ**：#JetsonOrin #EdgeAI #ALFANetwork #USBWiFi #AWUS036ACM #Yupitek
>
> **著者**：Yupitek Ltd.（ユーピテック） — ALFA Network 台湾正規代理店
>
> **免責事項**：本記事の調査データは 2026 年 5 月時点のものです。Jetson プラットフォームと Linux Kernel は継続的に更新されるため、デプロイ前に最新の JetPack バージョンとカーネル内蔵ドライバーのサポート状況を確認することを推奨します。

---

## 参考文献

1. [AVALUE Technology AIB-NW01製品ページ](https://www.avalue.com.tw/)
2. [NVIDIA Jetson公式開発者フォーラム](https://forums.developer.nvidia.com/)
3. [morrownr/USB-WiFiチップ対応表](https://github.com/morrownr/USB-WiFi)
4. [Linux Kernel mt76ドライバードキュメント](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
5. [ALFA Network Linux互換性一覧表](https://docs.alfa.com.tw/Support/Compat/)
