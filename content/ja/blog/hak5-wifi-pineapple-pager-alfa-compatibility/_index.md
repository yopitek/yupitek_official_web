---
title: "HAK5 WiFi Pineapple Pager × ALFA Network：外付けUSBワイヤレスカードの互換性評価とセットアップガイド"
description: "HAK5 WiFi Pineapple PagerのOpenWrt環境下におけるALFA Network外付けUSBワイヤレスカードとの互換性を深く検証した技術レポートとインストールガイドです。MIPSアーキテクチャのクロスコンパイル、USB 2.0の給電制限、ドライバーの設定について解説します。"
date: 2026-06-19
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi Pineapple Pager", "ALFA Network", "AWUS036ACM", "AWUS036ACH", "compatibility", "wireless-security"]
featureimage: "/images/blog/hak5-wifi-pineapple-pager-alfa-compatibility.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "HAK5 WiFi Pineapple Pagerに外付けALFAアダプターを接続できますか？"
    answer: "できますが、MIPSアーキテクチャの制限とUSB 2.0給電に注意が必要です。AWUS036ACMが首选で、カーネル内蔵ドライバーが最も安定しています。"
  - question: "Pagerに電源付きUSB Hubが必要なのはなぜですか？"
    answer: "PagerはUSB 2.0ポートのみで最大出力500mAですが、高出力ALFAアダプターはピーク720mAに達し、直接挿入すると再起動やカーネルクラッシュを引き起こします。"
  - question: "AWUS036ACMがPager首选アダプターなのはなぜですか？"
    answer: "MT7612UドライバーはOpenWrt 6.6カーネルに統合されており、Pagerでopkgから直接インストールでき、クロスコンパイル不要で最も安定しています。"
  - question: "MIPSアーキテクチャはドライバーインストールにどんな制限がありますか？"
    answer: "PagerはMIPS32ベースのMT7628ANでDKMSをサポートせず、GCCツールチェーンがないため、内蔵ドライバー以外は外部x86ホストでクロスコンパイルする必要があります。"
  - question: "RTL8812AUのPagerでの既知の問題は？"
    answer: "RTL8812AUはMIPSプラットフォームでwiphy_registerカーネルエラーが発生しインターフェースを読み込めない場合があり、コミュニティ修正パッチの適用が必要です。AWUS036ACMの使用をお勧めします。"
---
高出力のUSBワイヤレスカードをHAK5 Pagerに接続する前に、以下の2つの大きなハードウェア・ソフトウェアの壁を理解しておく必要があります。

# HAK5 WiFi Pineapple Pager × ALFA Network：外付けUSBワイヤレスカードの互換性評価とセットアップガイド


{{< tldr >}}
PagerはMIPSアーキテクチャでDKMS非対応、AWUS036ACMはMT7612UドライバーがOpenWrt 6.6カーネルに内蔵でプラグアンドプレイ。AWUS036ACHはクロスコンパイルが必要でwiphy bugあり、USB 2.0給電は500mAのため外部Hubが必要です。
{{< /tldr >}}
ワイヤレスネットワークのセキュリティ監査（ペネトレーションテスト）には、高度な精度、汎用性、そして適切なハードウェアが不可欠です。**HAK5 WiFi Pineapple Pager**は、強力な**PineAP v8**エンジンを搭載した超ポータブルなポケットサイズの監査ツールとして、多くのセキュリティエンジニアの注目を集めています。

しかし、監査範囲の拡大、デュアルバンド（2.4 GHzおよび5 GHz）の同時運用、あるいは内蔵無線に干渉しないマルチチャネルパッシブモニタリングなどを目的として、多くの専門家から次のような質問が寄せられます。**「HAK5 Pagerに外付けのALFA Networkワイヤレスアダプターを接続することは可能でしょうか？」**

簡単な結論から申し上げますと、**「可能ですが、ハードウェアおよびソフトウェアに関する重要な制限事項があります」**。

このガイドでは、CPUアーキテクチャやUSB給電制限などの技術的な制約を徹底的に分析し、ALFAの現行製品ラインナップとの互換性を評価した上で、CLIによるセットアップおよびトラブルシューティングの手順を順を追って解説します。

---

## 1. 重要な技術制限

### 1.1 CPUアーキテクチャ：MIPSアーキテクチャの制約
x86_64アーキテクチャの標準的なKali Linuxマシンや、ARMを採用するRaspberry Piとは異なり、HAK5 Pagerには**MediaTek MT7628AN SoC**（OpenWrtでは`mipsel_24kc`としてコンパイルされる**MIPS32r2, Little-Endian**コア）が搭載されています。

> [!IMPORTANT]
> Pager OSは**OpenWrt（バージョン 24.10.1、カーネル 6.6.86）**ベースであるため、**DKMS（動態カーネルモジュール支援）に対応していません**。Pager単体ではGCCやMakeなどのビルドツールが不足しているため、カーネル外（Out-of-Kernel）のドライバーソースコードを直接ビルドすることは不可能です。内蔵されていないドライバーは、外部のx86_64 Linuxホスト上でOpenWrt SDKを使用してクロスコンパイルする必要があります。

### 1.2 USB 2.0の給電能力：電圧安定性の制限
HAK5 Pagerに搭載されているUSBポートはUSB 2.0 Hostが1つのみです。標準のUSB 2.0仕様では、最大電流出力は**500 mA @ 5V（2.5W）**に制限されています。

一方、ALFA AWUS036ACH (RTL8812AU) や AWUS036AXML (MT7921AUN) などの高出力ワイヤレスアダプターは、パケット注入（Packet Injection）や高密度なチャネルスキャン時に最大で**720 mA（3.6W）**の電力を消費します。

> [!WARNING]
> 高出力のALFAカードをPagerのUSBポートに直接接続すると、電圧降下が発生し、**デバイスの再起動、カーネルパニック、またはワイヤレスカードの切断**が引き起こされます。これらの高出力カードを安定して動作させるには、**外部電源付きのセルフパワーUSBハブ（5V/2A以上）**を必ず経由させる必要があります。

---

## 2. ALFAアダプター互換性評価マトリクス

以下の表は、Pager OS（カーネル 6.6）を搭載したHAK5 Pagerと現行のALFA Network USBワイヤレスアダプターとの互換性を示したものです。

| ALFA型番 | チップセット | 対応バンド | USB消費電力 | カーネル 6.6 互換ステータス | インストール方法 | Monitor / Injection 支援 | 評価・購入アドバイス |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AWUS036ACM** | MediaTek **MT7612U** | 2.4 GHz / 5 GHz | ~600 mA (ハブ推奨) | **内蔵ドライバー (Native)** | `opkg`で直接インストール | ✅ 対応 / ✅ 対応 | 🏆 **一押し・ベストチョイス（最推奨）** |
| **AWUS036ACH** | Realtek **RTL8812AU** | 2.4 GHz / 5 GHz | ~720 mA (電源付きハブ必須) | カーネル外ドライバー | SDKによるクロスコンパイル | ✅ 対応 / ✅ 対応 | ⭐⭐ **上級者向け**（MIPS環境でwiphyバグあり） |
| **AWUS036AXML** | MediaTek **MT7921AUN** | 2.4/5/6 GHz (WiFi 6E) | ~720 mA (電源付きハブ必須) | **内蔵ドライバー (Native)** | `opkg` + 手動ファームウェア配置 | ✅ 対応 / ✅ 対応 | ⭐⭐⭐ **将来性大**、ただし給電に注意 |
| **AWUS036ACHM** | MediaTek **MT7610U** | 2.4 GHz / 5 GHz | ~400 mA (直接給電可) | 部分内蔵 | `opkg`でインストール | ✅ 対応 / ✅ 対応 | ⭐⭐⭐ **コストパフォーマンス重視** |
| **AWUS036ACS** | Realtek **RTL8811AU** | 2.4 GHz / 5 GHz | ~500 mA (限界値) | カーネル外ドライバー | SDKによるクロスコンパイル | ✅ 対応 / ✅ 対応 | ⭐⭐ **普通**（手動ビルドが必要） |
| **AWUS036EACS** | Realtek **RTL8821CU** | 2.4 GHz / 5 GHz | ~500 mA | カーネル外ドライバー | 非推奨 | ❌ **モニターモード非対応** | ❌ **使用不可** |

---

## 3. ステップ・バイ・ステップ セットアップガイド

最も推奨されるモデルのCLIによる詳細なセットアップ手順です。

### 3.1 シナリオ A：AWUS036ACM (MT7612U) — プラグ＆プレイ（推奨）

**AWUS036ACM**は、HAK5 Pagerにとって最も安定した選択肢です。MediaTekの`mt76`メインラインドライバーはLinux Kernel 6.6にネイティブ統合されており、面倒なビルド作業は一切不要です。

#### ステップ 1: ハードウェアの接続
1. 外部電源付きのUSBハブをHAK5 PagerのUSBポートに接続します。
2. AWUS036ACMをUSBハブに差し込みます。
3. SSHでPagerにログインします：
   ```bash
   ssh root@172.16.42.1
   ```

#### ステップ 2: デバイス認識の確認
`lsusb`コマンドを実行し、MediaTekチップセットが正しく認識されているか確認します：
```bash
lsusb
# 期待される出力:
# Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

#### ステップ 3: opkgによるドライバーのインストール
パッケージマネージャーを更新し、必要なカーネルモジュールとファームウェアをインストールします：
```bash
opkg update
opkg install kmod-mt76x2u kmod-mt76-usb firmware-utils
```

#### ステップ 4: MIPS環境におけるUSB Scatter-Gatherクラッシュの修正
MIPSアーキテクチャのOpenWrtデバイスにおいて、`mt76-usb`ドライバーがUSB Scatter-Gather (USB SG) を有効にしていると、ファームウェア転送時にカーネルクラッシュ（`-110`エラー）が発生することが知られています。

> [!TIP]
> 動作の安定性を確保するために、カーネルモジュールパラメーターを設定してUSB SGを明示的に無効化する必要があります。

`/etc/modules.d/mt76-usb-sg`ファイルを作成し、以下の設定を書き込みます：
```bash
echo "mt76-usb disable_usb_sg=1" > /etc/modules.d/mt76-usb-sg
```
Pagerを再起動して設定を反映させます：
```bash
reboot
```

#### ステップ 5: モニターモードとパケット注入の検証
再起動後、SSHで再度ログインし、ワイヤレスインターフェースを確認します：
```bash
iw dev
# 新しいインターフェース（例：wlan2）が表示されていることを確認します
```

モニターモードの有効化：
```bash
ip link set wlan2 down
iw dev wlan2 set monitor none
ip link set wlan2 up
```
状態の確認：
```bash
iw dev wlan2 info
# 「type monitor」が表示されれば設定成功です
```

---

### 3.2 シナリオ B：AWUS036ACH (RTL8812AU) — クロスコンパイルビルド

**AWUS036ACH**はKali Linuxにおいて絶大な信頼を得ていますが、OpenWrt 6.6のメインラインカーネルにはドライバーが含まれていません。クロスコンパイルが必要です。

#### 前提条件
- Ubuntu 22.04またはDebian 12のビルド用PC (x86_64)
- `ramips/mt76x8`ターゲットに対応したOpenWrt SDK

#### ステップ 1: ビルドPCでのSDKダウンロード
UbuntuビルドPC上で以下を実行します：
```bash
wget https://downloads.openwrt.org/releases/24.10.1/targets/ramips/mt76x8/openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
tar --zstd -xf openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
cd openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64
```

#### ステップ 2: rtl8812auパッケージソースの追加
```bash
git clone https://github.com/aircrack-ng/rtl8812au.git package/kernel/rtl8812au
./scripts/feeds update -a
./scripts/feeds install -a
```

#### ステップ 3: 構成設定とビルド
設定メニューを開き、ワイヤレスドライバーを選択します：
```bash
make menuconfig
# 選択項目: Kernel modules -> Wireless Drivers -> kmod-rtl8812au を有効化
```
ビルドを実行します：
```bash
make package/kernel/rtl8812au/compile V=s
```

#### ステップ 4: `.ipk`ファイルの転送とインストール
コンパイル完了後、生成されたインストール用`.ipk`ファイルは`bin/packages/mipsel_24kc/`に保存されます。これをPagerに転送してインストールします：
```bash
scp bin/packages/mipsel_24kc/base/kmod-rtl8812au*.ipk root@172.16.42.1:/tmp/
ssh root@172.16.42.1 "opkg install /tmp/kmod-rtl8812au*.ipk"
```

> [!CAUTION]
> MIPSプラットフォーム上でカーネル外の`rtl8812au`ドライバーを使用する場合、`wiphy_register`エラーが発生し、ハードウェアが認識されない不具合が報告されています。これを解決するには、コンパイル前にMIPS用の修正パッチを当てる必要があります。トラブルを避けるためにも、**AWUS036ACM**の採用を強くお勧めします。

---

## 4. 解放されるワイヤレス監査機能

外付けの互換ALFAワイヤレスカードを接続することにより、HAK5 Pagerは以下のペネトレーションテスト機能をフルに活用できるようになります。

1. **5 GHz帯への対応**：Pager内蔵の無線チップでは対応が難しい5 GHz帯の監査が可能となり、現代の主要なエンタープライズAPのWPA/WPA2ハンドシェイクパケットを確実にキャプチャできます。
2. **専用攻撃デバイスの追加**：内蔵無線をクライアント誘導（Evil Twin / KARMA攻撃）に専念させ、外付けのALFAカード（`wlan2`）をDeauthパケットの高速射撃用に特化させることができます。
3. **PineAPの統合**：Web管理画面またはCLIから、外付けワイヤレスカードをPineAPのメインインターフェースとして登録でき、クライアントの取り込みとレスポンスの速度を最大100倍に高めることができます。

---


---

{{< faq >}}

## 5. まとめ・推奨構成

ALFA NetworkのワイヤレスカードとHAK5 WiFi Pineapple Pagerを組み合わせることで、ステルス性と性能を両立したポータブル無線ペネトレーションテストステーションが完成します。ただし、以下のハードウェア選定は極めて重要です。

- **プラグ＆プレイで即戦力**：[ALFA AWUS036ACM](https://yupitek.com/ja/products/alfa/awus036acm)をお選びください。OpenWrtカーネルとの相性が抜群で、極めて安定しています。
- **電源供給の確保**：動作の切断を防ぎ、十分な電波強度を維持するため、必ず**セルフパワー（外部給電）対応のUSBハブ**をご使用ください。

技術的なご質問、ハードウェアの選定、またはカスタムOpenWrtビルドのご相談は、**Yupitekサポートチーム**までお気軽にお問い合わせください。

- 🌐 公式ウェブサイト: [www.yupitek.com](https://www.yupitek.com)
- 📧 お問い合わせ窓口: [sales@yupitek.com](mailto:sales@yupitek.com)
- 📞 電話番号: +886-2-87325338
- 📍 本社所在地: 1F., No. 72, Ln. 34, Fuyang St., Xinyi Dist., Taipei City, Taiwan

---

## 参考文献

1. [Hak5公式ドキュメント — WiFi Pineapple製品ドキュメント](https://documentation.hak5.org/)
2. [OpenWrt公式ウェブサイト — OpenWrt 24.10リリース](https://openwrt.org/)
3. [OpenWrt mt76ドライバーリポジトリ — GitHub](https://github.com/openwrt/mt76)
4. [aircrack-ng/rtl8812au — コミュニティドライバーGitHubリポジトリ](https://github.com/aircrack-ng/rtl8812au)
5. [ALFA Network公式ウェブサイト](https://www.alfa.com.tw/)
