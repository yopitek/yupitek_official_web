---
title: "ALFA USB ネットワークカードのLinuxドライバ選択：MediaTek（翻訳不要）対Realtek（翻訳必要）"
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
description: "「Yupitek ALFA USB 網卡技術文件（Mediatek, Realtek）」"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

> **技術支援文書 · 2026年9月3日 初版（依 blog-writing-rules.md v1.0 規範撰寫）**
> 判定対象：Yupitek 現役 ALFA USB ネットワークアダプターの中で、本技術文書マトリックスに収録されている6モデル（MediaTek 3モデル、Realtek 3モデル）。
> 関連記事：[ALFA ネットワークアダプターが NVIDIA DGX Spark に対応しているか](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA ネットワークアダプターが OpenWrt に対応しているか](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)｜[ALFA ネットワークアダプターが NVIDIA Jetson Nano に対応しているか](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)｜[ALFA ネットワークアダプターが Tomato に対応しているか](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[ALFA ネットワークアダプターが DD-WRT に対応しているか](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)

## 一言でまとめ

**6モデルの中で、3モデルのMediaTekチップセット（MT7610U / MT7612U / MT7921AUN）は現代のkernelに内蔵されたドライバが用意されており、接続するだけで使用可能です；3モデルのRealtekチップセット（RTL8812AU / RTL8811CU / RTL8832BU）はすべてout-of-treeドライバの手動編譯が必要です。** 省力化を望む場合は、まずチップセットを確認してから注文してください。

---

## 第一幕：場景——なぜ、誰かは挿入すれば使えるのに、誰かは2時間編譯する必要があるのか

実際の2つの状況：

- 客戸Aが **AWUS036ACM** をUbuntuデスクトップに挿入し、`lsusb`を実行すると、NetworkManagerが自動的にwlan0を表示——何もインストールしていない。
- 客戸Bが同じ機器に **AWUS036ACH** を挿入すると、ネットワークカードが全く反応せず、GitHubからソースコードをダウンロードし、ビルドツールをインストールし、コンパイルし、再起動する必要がある。

この違いは運気やLinuxのリリース版ではなく、**チップセットがどの陣営に属しているか**にあります：MediaTekのUSB WiFiチップセットのドライバ（mt76シリーズ）は既にLinux Kernelのmainlineに統合されています；RealtekのハイエンドUSB WiFiチップセットのドライバはまだout-of-tree（コア外）の形式で散布されており、コミュニティが維持するドライバリポジトリを手動でインストールする必要があります。

## 第2章：機構——in-kernel と out-of-treeの違いは何か

### MediaTek：mt76 メインラインドライバ、接続するだけで使用可能

MediaTek USB クリスタルチップのドライバは、kernelの**mt76**サブシステムでカバーされています：

| 機型 | クリスタルチップセット | kernel ドライバモジュール | 編訳不要条件 |
|---|---|---|---|
| AWUS036ACHM | MT7610U | mt76x0u | kernel 内蔵、バージョン門戸の懸念なし |
| AWUS036ACM | MT7612U | mt76x2u | kernel 内蔵、バージョン門戸の懸念なし |
| AWUS036AXML / AXM | MT7921AUN | mt7921u | **kernel 5.19+ 必要** |

⚠️ 唯一の問題点：**MT7921AUNのkernelの門戸は5.19+です**。古いプラットフォーム（例えばJetson NanoのJetPack 4.x、kernel 4.9）にはbackportができず、直接使用不可能です——これは私たちがJetson Nano技術文書で確認した結論です（[ALFA 无線网卡是否支持 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/) §7.4を参照）。

### Realtek：out-of-tree、全て手動編訳

Realtek USB クリスタルチップには利用可能なmainlineドライバがなく、コミュニティの保守するドライバrepoに依存しています。現在、最も活発に保守されているのは**morrownr**で、このリストには3つのクリスタルチップに対応する3つのrepoがあります：

| 機型 | クリスタルチップセット | ドライバrepo（morrownr保守） | 2026-09-03 検証 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | [8812au-20210820](https://github.com/morrownr/8812au-20210820) | ✅ 検証済み |
| AWUS036EACS | RTL8811CU | [8821cu-20210916](https://github.com/morrownr/8821cu-20210916) | ✅ 検証済み |
| AWUS036AX / AXER | RTL8832BU | [rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | ✅ 検証済み |

### 3つの典型的な環境に適用

| 環境 | kernel | MediaTek 阵営（3モデル） | Realtek 阵営（3モデル） |
|---|---|---|---|
| GB10 / DGX Spark 類のプラットフォーム | 6.x + aarch64 | 全て利用可能（mt76 内蔵） | 全て編訳必要（ARM64 可能） |
| Jetson Nano（JetPack 4.x） | 4.9 | 7610U/7612U 利用可能；MT7921AUN **利用不可能** | 8812au 編訳可能（ARM64 サポート）；他は検証されていない |
| OpenWrt ルーター | バージョンによる | 全て利用可能（MT7921AUN 23.05+ 必要） | kmodに対応または編訳必要、難度高 |

（各環境の詳細な判定マトリックスは[ALFA 无線网卡是否支持 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)、[ALFA 无线网卡是否支持 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)、[ALFA 无线网卡是否 support OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)を参照。）

## 第三幕：ツールボックス——3分間判定フローとインストール手順

### 判定表：ネットワークカードを手に入れたらまずこれらの3ステップを行ってください

```bash
# ステップ 1：システムがネットワークカードを認識しているか確認（VID:PIDを記録）
lsusb

# ステップ 2：kernelが対応するドライバを既にロードしているか確認
lsmod | grep -E "mt76|rtl8"

# ステップ 3：kernelのバージョンを確認（MT7921AUNが使用可能かどうかを決定）
uname -r
```

判定ロジック（メイン：上表の6モデル）：

1. `lsusb`に**MediaTek / MT76xx**が表示された場合 → in-kernel陣営、kernel ≥ 5.19（MT7921AUNモデル）または任意の近代kernel、即插即用。
2. `lsusb`に**Realtek RTL88xx**が表示された場合 → out-of-tree陣営、以下のインストール手順に進む。
3. `lsusb`に**新しいデバイスが表示されない**場合 → まずUSBポート／ケーブルを交換してハードウェア問題を排除し、モデルがWi-Fi 6のRTL8832BUであるか確認（一部のバッチでは`usb_modeswitch`が必要、このステップは個別のモデルの問題であり、本記事の範囲外、詳細はここでは説明しない）。

### Realtek陣営の汎用インストール（AWUS036ACHを例に）

```bash
# ステップ 1：コンパイル依存関係をインストール（Debian/Ubuntu）
sudo apt install build-essential dkms linux-headers-$(uname -r)

# ステップ 2：ドライバのソースコードを取得（モデルに対応するrepoは上表を参照）
git clone https://github.com/morrownr/8812au-20210820
cd 8812au-20210820

# ステップ 3：インストール（DKMS登録、kernelの変更で再インストールは必要なし）
sudo ./install-driver.sh

# ステップ 4：再起動後の確認
lsmod | grep 88XXau
ip link   # 新しいwlanインターフェースが表示されるべき
```

> **表1の結論：判定を先にしてインストール——まずチップセットを見て、90秒で「即插即用」か「repoでコンパイル」かを決め、壁にぶつかる必要はありません。**

### 購入アドバイス（結論文）

- **コンパイルを避けたい場合**：MediaTek陣営（AWUS036ACHM / ACM / AXML）を選んでください。近代kernelはすべて即插即用です。
- **Wi-Fi 6でコンパイルを避けたい場合**：AWUS036AXML（MT7921AUN）を選んでくださいが、kernelが5.19以上であることを確認してください。
- **特定のmonitor modeツールチェインが必要でRealtek以外を選ぶ必要がある場合**（特定のmonitor modeツールチェインが必要でRealtek以外を選ぶ必要がある場合）：20～40分をドライバのコンパイルに割り当て、kernelヘッダーが目標プラットフォームに存在することを確認してください。

## 知られている制約と反論条件

以下の条件が**不成立**である場合、結論を以下の代替案に改めるください：

1. **kernel 5.19以下 + MT7921AUN**：mt7921uはbackportができません（現代kernelの基礎設備に依存しています）、結論は「不可用」と反転します。これは本文で最も重要な例外です。
2. **x86/ARM64 Linux以外**（例えば、いくつかのMIPSルーター）：morrownrリポジトリはコンパイルが保証されていません、OpenWrtのkmodを優先してください（[ALFA無線ネットワークカードがOpenWrtをサポートするかどうか](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)を参照ください）。
3. **ドライバリポジトリのバージョン進化**：morrownrリポジトリは日付で名付けられています（例：rtl8852bu-20250826）、将来は改版や削除が発生する可能性があります；インストール前にリポジトリの現状を確認してください。
4. **モニターモード / APモードの機能**：同じチップセットでもkernelのバージョンによって機能に差異があります（例えば、OpenWrt 22.03+のrtl8812au-ctが24.10でクラッシュ報告があるように）、詳細な機能マトリックスは各環境の専文に準拠してください。
5. **RTL8832BU（AWUS036AX/AXER）は本文で取り上げられていない6モデルの内に含まれていませんが、カスタマーサポートではよく関連して質問されます**：ドライバのメンテナンス者morrownrは、そのチップセットシリーズが「非常に悪いドライバで、チップ自体に問題があると疑います」と公表しています。Linuxユーザーは現時点で避けることを推奨します。これは「コンパイルが必要」という難易度の問題だけでなく、カスタマーへの返信では事実を正直に説明することが重要です。

## 参考資料

| 資料源 | 説明 | URL | 検証状態 | 検証日 |
|---|---|---|---|---|
| morrownr/8812au GitHub | RTL8812AU Linux ドライバ | https://github.com/morrownr/8812au-20210820 | ✅ 検証済み | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8811CU Linux ドライバ | https://github.com/morrownr/8821cu-20210916 | ✅ 検証済み | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux ドライバ | https://github.com/morrownr/rtl8852bu-20250826 | ✅ 検証済み | 2026-09-03 |
| Yupitek ALFA 製品総覧 | 現役機型およびスペック | https://yupitek.com/zh-tw/products/alfa/ | ✅ 検証済み | 2026-09-03 |
| Yupitek ブログ：Soft AP 指南 | AP モード実装検証文 | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 検証済み | 2026-09-03 |
| 本サイト技術文書 9 篇 | 判定行列および環境検証の基礎 | 相対リンク（文末の「関連記事」を参照） | ✅ 検証済み | 2026-09-03 |

> kernel mt76 公式 Wiki ページ：https://wireless.wiki.kernel.org/en/users/drivers/mediatek （検証済み、各チップセットがサポートする初期 kernel バージョンをリストアップ、迅速な確認に利用可能）

## 免責声明

このファイルは榆閤科技（Yopitek Ltd）の技術サポートにより整理されました。スペックおよびドライバの状態は、kernelおよびドライバrepoの更新により変動する可能性があります。インストール前に、公式repoおよび原厂の規格ページを確認してください。ALFA Networkは、当社の正式認証代理ブランドです。

## 免責声明

このファイルは榆閤科技（Yopitek Ltd）の技術サポートにより整理されました。スペックおよびドライバの状態は、kernelおよびドライバrepoの更新により変動する可能性があります。インストール前に、公式repoおよび原厂の規格ページを確認してください。ALFA Networkは、当社の正式認証代理ブランドです。
