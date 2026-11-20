---
title: "ALFA USB ネットワークカードのLinuxドライバ選択：MediaTek（コンパイル不要）対Realtek（コンパイル必要）"
date: 2026-09-03
draft: false
slug: "alfa-usb-wifi-linux-driver-guide"
tags:
  - "ALFA"
  - "Linux-Driver"
  - "MediaTek"
  - "Realtek"
  - "in-kernel"
  - "out-of-tree"
  - "DKMS"
  - "mt76"
  - "rtl8812au"
categories:
  - "ハードウェアガイド"
description: "6モデルのうち、MediaTekチップセット3モデル（MT7610U / MT7612U / MT7921AUN）は現代のkernelにドライバが内蔵されており挿すだけで使えます。Realtekチップセット3モデル（RTL8812AU / RTL8821CU / RTL8832BU）は、kernelが各モデルの最低バージョン（EACS 6.2、ACH/ACS 6.13、AX/AXER 6.17）より古い場合にout-of-treeドライバの手動コンパイルが必要です（GX10のkernel 6.17では全モデル追加インストール不要）。手間を省くなら、まずチップセットを確認してから購入してください。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> **技術支援文書 · 2026年9月3日 初版（blog-writing-rules.md v1.0 に準拠して作成）**
> 判定対象：Yopitek 現役 ALFA USB ネットワークアダプターの中で、本技術文書マトリックスに収録されている6モデル（MediaTek 3モデル、Realtek 3モデル）。
> 関連記事：[ALFA ネットワークアダプターが NVIDIA DGX Spark に対応しているか](/ja/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA ネットワークアダプターが OpenWrt に対応しているか](/ja/blog/alfa-openwrt-router-compatibility/)｜[ALFA ネットワークアダプターが NVIDIA Jetson Nano に対応しているか](/ja/blog/alfa-nvidia-jetson-nano-compatibility/)｜[ALFA ネットワークアダプターが Tomato に対応しているか](/ja/blog/alfa-tomato-router-compatibility/)｜[ALFA ネットワークアダプターが DD-WRT に対応しているか](/ja/blog/alfa-ddwrt-router-compatibility/)

## 一言でまとめ

**6モデルの中で、3モデルのMediaTekチップセット（MT7610U / MT7612U / MT7921AUN）は現代のkernelに内蔵されたドライバが用意されており、接続するだけで使用可能です；3モデルのRealtekチップセット（RTL8812AU / RTL8821CU / RTL8832BU）は、kernelが各モデルの最低バージョン（EACSのrtw88_8821cuは6.2、ACH/ACSは6.13、AX/AXERは6.17）より古い場合にout-of-treeドライバの手動コンパイルが必要です（GX10のkernel 6.17では全モデル内蔵で免インストール）。** 省力化を望む場合は、まずチップセットを確認してから注文してください。

---

## 第一幕：場面——なぜ、挿すだけで使える人もいれば、2時間かけてコンパイルする人もいるのか

実際の2つの状況：

- 顧客Aが **AWUS036ACM** をUbuntuデスクトップに挿入し、`lsusb`を実行すると、NetworkManagerが自動的にwlan0を表示——何もインストールしていない。
- 顧客Bが同じ機器に **AWUS036ACH** を挿入すると、ネットワークカードが全く反応せず、GitHubからソースコードをダウンロードし、ビルドツールをインストールし、コンパイルし、再起動する必要がある。

この違いは運気やLinuxのリリース版ではなく、**チップセットがどの陣営に属しているか**にあります：MediaTekのUSB WiFiチップセットのドライバ（mt76シリーズ）は既にLinux Kernelのmainlineに統合されています；Realtek USB WiFiチップセットのドライバは、古いkernelではout-of-tree（コア外）の形式で散布されており、コミュニティが維持するドライバリポジトリを手動でインストールする必要があります（EACSのrtw88_8821cuはkernel 6.2から内蔵）。

## 第2章：機構——in-kernel と out-of-treeの違いは何か

### MediaTek：mt76 メインラインドライバ、接続するだけで使用可能

MediaTek USB チップのドライバは、kernelの**mt76**サブシステムでカバーされています：

| 機種 | チップセット | kernel ドライバモジュール | コンパイル不要の条件 |
|---|---|---|---|
| AWUS036ACHM | MT7610U | mt76x0u | kernel 内蔵、バージョン門戸の懸念なし |
| AWUS036ACM | MT7612U | mt76x2u | kernel 内蔵、バージョン門戸の懸念なし |
| AWUS036AXML / AXM | MT7921AUN | mt7921u | **kernel 5.18+ 必要** |

⚠️ 唯一の問題点：**MT7921AUNのkernelの門戸は5.18+です**。古いプラットフォーム（例えばJetson NanoのJetPack 4.x、kernel 4.9）にはbackportができず、直接使用不可能です——これは私たちがJetson Nano技術文書で確認した結論です（[ALFA 無線ネットワークカードが NVIDIA Jetson Nano に対応しているか](/ja/blog/alfa-nvidia-jetson-nano-compatibility/) §7.4を参照）。

### Realtek：古いkernelではout-of-tree、手動コンパイル

古いkernelではRealtek USB チップに利用可能なmainlineドライバがなく、コミュニティの保守するドライバrepoに依存します。EACSのrtw88_8821cuはkernel 6.2から、ACH/ACSは6.13、AX/AXERは6.17からmainlineに内蔵されており、以下のrepoは主にそれより古いkernel向けです。現在、最も活発に保守されているのは**morrownr**で、このリストには3つのチップに対応する3つのrepoがあります：

| 機種 | チップセット | ドライバrepo（morrownr保守） | 2026-09-03 検証 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | [8812au-20210820](https://github.com/morrownr/8812au-20210820) | ✅ 検証済み |
| AWUS036EACS | RTL8821CU（kernel ≥6.2は内蔵） | [8821cu-20210916](https://github.com/morrownr/8821cu-20210916) | ✅ 検証済み |
| AWUS036AX / AXER | RTL8832BU | [rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | ✅ 検証済み |

### 3つの典型的な環境に適用

| 環境 | kernel | MediaTek 陣営（3モデル） | Realtek 陣営（3モデル） |
|---|---|---|---|
| GB10 / DGX Spark 類のプラットフォーム | 6.x + aarch64 | 全て利用可能（mt76 内蔵） | kernel 6.17 では全て内蔵（実測 6.17.0-1014-nvidia）；古い kernel のみコンパイル必要 |
| Jetson Nano（JetPack 4.x） | 4.9 | 7610U/7612U 利用可能；MT7921AUN **利用不可能** | 8812au コンパイル可能（ARM64 サポート）；他は検証されていない |
| OpenWrt ルーター | バージョンによる | 全て利用可能（MT7921AUN 23.05+ 必要） | kmodに対応またはコンパイル必要、難度高 |

（各環境の詳細な判定マトリックスは[ALFA 無線ネットワークカードが NVIDIA DGX Spark に対応しているか](/ja/blog/alfa-nvidia-dgx-spark-compatibility/)、[ALFA 無線ネットワークカードが NVIDIA Jetson Nano に対応しているか](/ja/blog/alfa-nvidia-jetson-nano-compatibility/)、[ALFA 無線ネットワークカードが OpenWrt に対応しているか](/ja/blog/alfa-openwrt-router-compatibility/)を参照。）

## 第三幕：ツールボックス——3分間判定フローとインストール手順

### 判定表：ネットワークカードを手に入れたらまずこれらの3ステップを行ってください

```bash
# ステップ 1: システムがネットワークカードを認識しているか確認 (VID:PIDを記録)
lsusb

# ステップ 2: kernelが対応するドライバを既にロードしているか確認
lsmod | grep -E "mt76|rtl8"

# ステップ 3: kernelのバージョンを確認 (MT7921AUNが使用可能かどうかを決定)
uname -r
```

判定ロジック（メイン：上表の6モデル）：

1. `lsusb`に**MediaTek / MT76xx**が表示された場合 → in-kernel陣営、kernel ≥ 5.18（MT7921AUNモデル）または任意の最近のkernel、挿すだけで使用可能。
2. `lsusb`に**Realtek RTL88xx**が表示された場合 → Realtek陣営：kernelが各モデルの最低バージョン以上なら内蔵ドライバで動作、古いkernelならout-of-treeの手動コンパイル（以下のインストール手順）に進む。
3. `lsusb`に**新しいデバイスが表示されない**場合 → まずUSBポート／ケーブルを交換してハードウェア問題を排除し、モデルがWi-Fi 6のRTL8832BUであるか確認（一部のバッチでは`usb_modeswitch`が必要、このステップは個別のモデルの問題であり、本記事の範囲外、詳細はここでは説明しない）。

### Realtek陣営の汎用インストール（AWUS036ACHを例に）

```bash
# ステップ 1: コンパイル依存関係をインストール (Debian/Ubuntu)
sudo apt install build-essential dkms linux-headers-$(uname -r)

# ステップ 2: ドライバのソースコードを取得 (モデルに対応するrepoは上表を参照)
git clone https://github.com/morrownr/8812au-20210820
cd 8812au-20210820

# ステップ 3: インストール (DKMS登録, kernelの変更で再インストールは必要なし)
sudo ./install-driver.sh

# ステップ 4: 再起動後の確認
lsmod | grep 88XXau
ip link   # 新しいwlanインターフェースが表示されるべき
```

> **表1の結論：判定を先にしてインストール——まずチップセットを見て、90秒で「挿すだけで使用可能」か「repoでコンパイル」かを決め、壁にぶつかる必要はありません。**

### 購入アドバイス（結論文）

- **コンパイルを避けたい場合**：MediaTek陣営（AWUS036ACHM / ACM / AXML）を選んでください。最近のkernelならすべて挿すだけで使えます。
- **Wi-Fi 6でコンパイルを避けたい場合**：AWUS036AXML（MT7921AUN）を選んでくださいが、kernelが5.18以上であることを確認してください。
- **特定のmonitor modeツールチェインが必要でRealtek以外を選ぶ必要がある場合**（特定のmonitor modeツールチェインが必要でRealtek以外を選ぶ必要がある場合）：20～40分をドライバのコンパイルに割り当て、kernelヘッダーが目標プラットフォームに存在することを確認してください。

## 知られている制約と反論条件

以下の条件が**不成立**である場合、結論を以下の代替案に改めてください：

1. **kernel 5.17以下 + MT7921AUN**：mt7921uはbackportができません（現代kernelの基礎設備に依存しています）、結論は「使用不可」に反転します。これは本文で最も重要な例外です。
2. **x86/ARM64 Linux以外**（例えば、いくつかのMIPSルーター）：morrownrリポジトリはコンパイルが保証されていません、OpenWrtのkmodを優先してください（[ALFA無線ネットワークカードがOpenWrtをサポートするかどうか](/ja/blog/alfa-openwrt-router-compatibility/)を参照ください）。
3. **ドライバリポジトリのバージョン進化**：morrownrリポジトリは日付で名付けられています（例：rtl8852bu-20250826）、将来は改版や削除が発生する可能性があります；インストール前にリポジトリの現状を確認してください。
4. **モニターモード / APモードの機能**：同じチップセットでもkernelのバージョンによって機能に差異があります（例えば、OpenWrt 22.03+のrtl8812au-ctが24.10でクラッシュ報告があるように）、詳細な機能マトリックスは各環境の個別記事に準拠してください。
5. **RTL8832BU（AWUS036AX/AXER）は本文で取り上げた6モデルには含まれていませんが、カスタマーサポートでよく関連して質問されます**：rtw89_8852buドライバーはkernel 6.17からmainlineに入っており、GX10（kernel 6.17）ではmonitorが動作し、2.4Gインジェクションは AX 96%、AXER 73%です。古いkernelでのみコミュニティドライバーmorrownr/rtl8852buが必要です。お客様に回答する際は、まずkernelのバージョンを確認してください。

## 参考資料

| 情報源 | 説明 | URL | 検証状態 | 検証日 |
|---|---|---|---|---|
| morrownr/8812au GitHub | RTL8812AU Linux ドライバ | https://github.com/morrownr/8812au-20210820 | ✅ 検証済み | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8821CU Linux ドライバ（kernel 6.2 より前向け） | https://github.com/morrownr/8821cu-20210916 | ✅ 検証済み | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux ドライバ | https://github.com/morrownr/rtl8852bu-20250826 | ✅ 検証済み | 2026-09-03 |
| Yopitek ALFA 製品総覧 | 現役機種およびスペック | /ja/products/alfa/ | ✅ 検証済み | 2026-09-03 |
| Yopitek ブログ：Soft AP ガイド | AP モード実装検証文 | /ja/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 検証済み | 2026-09-03 |
| 本サイト技術文書 9 篇 | 判定行列および環境検証の基礎 | 相対リンク（文末の「関連記事」を参照） | ✅ 検証済み | 2026-09-03 |

> kernel mt76 公式 Wiki ページ：https://wireless.wiki.kernel.org/en/users/drivers/mediatek （検証済み、各チップセットがサポートする初期 kernel バージョンをリストアップ、迅速な確認に利用可能）

## 免責事項

このファイルは榆閤科技（Yopitek Ltd）の技術サポートにより整理されました。スペックおよびドライバの状態は、kernelおよびドライバrepoの更新により変動する可能性があります。インストール前に、公式repoおよびメーカーの規格ページを確認してください。ALFA Networkは、当社の正式認証代理ブランドです。
