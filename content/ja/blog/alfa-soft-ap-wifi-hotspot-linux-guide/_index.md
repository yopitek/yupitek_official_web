---

title: "ALFAネットワーク Soft AP完全ガイド2026：Kali Linux、Ubuntu、Debian、Raspberry Pi 4/5でWiFiホットスポットを構築"
description: "ALFA Network USB無線LANアダプタのSoft AP（hostapd/WiFiホットスポット）機能をKali Linux、Ubuntu、Debian、Raspberry Pi 4/5で徹底検証。AWUS036ACM、AWUS036ACH、AWUS036AXMLの詳細設定ガイド、コミュニティの実践事例、トラブルシューティングを完全収録。"
date: 2026-05-21
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Soft-AP", "WiFi-Hotspot", "hostapd", "Kali-Linux", "Ubuntu", "Debian", "Raspberry-Pi", "AWUS036ACM", "AWUS036ACH", "AWUS036AXML", "MT7612U", "RTL8812AU", "MT7921AUN", "Linux-WiFi"]
featureimage: "/images/blog/alfa-soft-ap-wifi-hotspot-linux-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "ALFA USBアダプターはLinuxでWiFiホットスポットとして使えますか？"
    answer: "チップセットによります。AWUS036ACM（MT7612U）は完全サポートでプラグアンドプレイ、AWUS036ACH（RTL8812AU）は条件付きサポート、AWUS036AXMLは部分サポートでチューニングが必要です。"
  - question: "Raspberry PiでSoft APを構築するのに最適なALFAアダプターは？"
    answer: "AWUS036ACMが最適です。カーネル内蔵ドライバーでプラグアンドプレイ、消費電力わずか400mAでPi給電に適し、WPA3とVIF仮想インターフェースをサポートし全プラットフォームで安定します。"
  - question: "アダプターがAPモードをサポートしているかどう確認しますか？"
    answer: "iw list | grep -A 10 'Supported interface modes'を実行し、出力に * AP が含まれていればドライバーがSoft APをサポートしており、hostapdが正常に動作します。"
  - question: "RTL8812AUドライバーのSoft APにはどんな制限がありますか？"
    answer: "WPA3をサポートせずWPA2-PSKのみ、VIF仮想インターフェース非対応で2枚のカードで役割分担が必要、消費電力約800mAでPiでは電源付きUSB Hubが必要です。"
  - question: "AWUS036AXMLでSoft AP実行中にWiFiが突然切断したら？"
    answer: "MT7921AUNの内蔵Bluetooth 5.2がWiFiに干渉します。echo 'install btusb /bin/false'を/etc/modprobe.d/に書き込んでBluetoothドライバーを永続的に無効化し、再起動してください。"
---
> 「ALFAのUSB無線LANアダプタは、Kali Linux / Ubuntu / Raspberry PiでWiFiホットスポット（Soft AP）として使えますか？」

# ALFAネットワーク Soft AP完全ガイド2026：Kali Linux、Ubuntu、Debian、Raspberry Pi 4/5でWiFiホットスポットを構築


{{< tldr >}}
ALFAアダプターのSoft AP互換性はチップドライバーに依存します。AWUS036ACMが全プラットフォーム安定の首选、AWUS036ACHは使用可能ですがWPA3非対応、AWUS036AXMLはBluetooth無効化とファームウェア更新が必要、RTL8832BUは使用非推奨です。
{{< /tldr >}}


ALFA AWUS036ACM（MT7612U）は Linux Soft AP に最適な選択肢です。in-kernel ドライバによりプラグアンドプレイで動作し、WPA3 と VIF 仮想インターフェースに対応しています。RTL8812AU は条件付きサポート、MT7921AUN は手動調整が必要です。

## はじめに

これはYupitekが最も頻繁に受けるお問い合わせの一つです。質問はシンプルに聞こえますが、答えはモデルとチップセットによって大きく異なります——**すべてのUSB WiFiアダプタがSoft APモードで動作するわけではありません。**

本記事では、GitHub（morrownr/USB-WiFi）の500件以上のコミュニティ議論、Redditの技術フォーラム、Raspberry Pi公式ドキュメント、実際のユーザーフィードバックを集約し、どのALFAアダプタが動作し、どれが動作しないかについて、誠実で包括的なレポートを提供します。

---

## 1. Soft APとは？Linuxでの動作方法 {#what-is-softap}

**Soft AP（ソフトウェアアクセスポイント）** とは、専用のAPハードウェアを使用せず、ソフトウェア（主に**hostapd**）を使って通常のUSB無線LANアダプタを無線基地局（アクセスポイント）に変える仕組みです。専用ルーターやAP機器を購入することなく、他のデバイス（携帯電話、ノートPC、IoT機器）をネットワークに接続できます。

以下のシナリオで非常に有用です：

- **旅行・ホームルーター**：出張やキャンプ時に、ノートPCやRaspberry PiにALFAアダプタを接続するだけで、ポータブルWiFiホットスポットを即座に作成
- **ペネトレーションテスト環境**：隔離環境でRogue APを構築し、セキュリティ研究を実施
- **IoT中継**：電波の死角に中継局を設置し、IoTセンサーがデータを送信できるようにする
- **エッジAI展開**：有線ネットワークのない産業環境で、機器をホットスポット化して他のデバイスを接続
- **緊急通信**：ネットワーク切断時に一時的な通信網を迅速に構築

### Linux Soft APの4つのコアコンポーネント

| コンポーネント | 機能 |
|--------------|------|
| **hostapd** | アクセスポイントを作成するコアデーモン — SSID、認証、暗号化を管理 |
| **nl80211** | Linux無線サブシステムの標準インターフェース — ドライバはこのフレームワークをサポートする必要がある |
| **dnsmasq** | DHCPサーバー — 接続クライアントにIPアドレスを自動割り当て |
| **iptables / nftables** | NAT（ネットワークアドレス変換） — 接続クライアントがアップストリームネットワークを共有 |

### 重要な概念：Master Mode

**Master Mode**（AP Mode、Infrastructure Modeとも呼ばれる）はドライバレベルの機能です。ドライバがMaster Modeをサポートしていない場合、hostapdは起動できません——設定がどれほど完璧でも無意味です。

APモードのサポートを確認するコマンド：

```bash
iw list | grep -A 10 "Supported interface modes"
```

出力に `* AP` が含まれていれば、そのアダプタのドライバはSoft APをサポートしています。含まれていなければ、そのアダプタはこの用途に使用できません。

### 💡 インカーネルドライバ vs アウトオブカーネルドライバ

Soft APアダプタを選ぶ際の**最も重要な**概念です：

| 種類 | 説明 | Soft APへの影響 |
|------|------|----------------|
| **インカーネルドライバ** | Linux公式ソースツリーに統合済み。起動時に自動ロード、手動インストール不要 | ✅ 長期安定、カーネルアップグレード後も継続使用可能 |
| **アウトオブカーネルドライバ** | GitHubからダウンロードして手動コンパイルが必要。カーネルアップグレードごとに再コンパイルが必要な場合あり | ⚠️ カーネル更新のたびに故障する可能性 |

**Soft APの長期的な安定性には、インカーネルドライバがアウトオブカーネルよりはるかに優れています。**

---

## 2. ALFA製品ラインアップとチップセット概要 {#product-lineup}

Yupitekが現在販売しているALFA製品ライン、チップセット、およびSoft APの予備評価：

| モデル | チップセット | ドライバタイプ | WiFi規格 | Soft AP評価 |
|--------|------------|--------------|---------|-----------|
| **AWUS036ACM** | MediaTek MT7612U | インカーネル（kernel 4.19+） | WiFi 5 AC1200 デュアルバンド | ✅ 完全サポート |
| AWUS036ACH | Realtek RTL8812AU | アウトオブカーネル（6.14+からインカーネル） | WiFi 5 AC1200 デュアルバンド | ⚠️ 条件付き |
| AWUS036AXML | MediaTek MT7921AUN | インカーネル（5.18+、APモード 5.19+） | WiFi 6E AX3000 トライバンド | ⚠️ 部分サポート |
| AWUS036AXM | MediaTek MT7921AUN | インカーネル（同上） | WiFi 6E AX3000 トライバンド | ⚠️ 部分サポート |
| AWUS036AX | Realtek RTL8832BU | アウトオブカーネル（kernel 6.12+推奨） | WiFi 6 AX1800 デュアルバンド | ❌ 非推奨 |
| AWUS036AXER | Realtek RTL8832BU | アウトオブカーネル（同上） | WiFi 6 AX1800 デュアルバンド | ❌ 非推奨 |

> **注記**：AWUS036ACHM（MT7610U）は製造終了となり、Yupitek製品ページには掲載されていません。本記事では現行販売製品のみを対象とします。

---

## 3. AWUS036ACM（MT7612U）— ⭐ Soft AP最推奨 {#acm}

### Soft APステータス：✅ 完全サポート

MT7612Uは、ALFAの現行製品の中で最も安定したSoft APチップセットです。そのドライバ`mt76x2u`は2018年（kernel 4.19）からLinux公式カーネルに組み込まれており、**差し込むだけで使えます**——`git clone`も`dkms`も、カーネルアップグレード後の再コンパイルも不要です。

### 主な利点

- **WPA2 + WPA3 デュアルサポート**：MediaTekのインカーネルドライバがWPA3 SAEをネイティブサポート — Realtekドライバにはない利点
- **VIF仮想インターフェースサポート**：単一アダプタでAP + Managed + Monitorモードを同時実行 — 2枚目のカード購入不要
- **超低消費電力**：最大約400mA、Raspberry Piに最適（Pi 4のUSBサブシステムは合計1200mAのみ）
- **クロスプラットフォーム**：Kali Linux 2022.x–2025.x、Ubuntu 22.04/24.04、Debian 11/12、Raspberry Pi OS（Pi 3B+、4、5）で広範囲に検証済み

### 正しいhostapd設定（MT7612U専用）

以下のcapability flagsはコミュニティ（morrownr/USB-WiFi）での長年のテストで確認されています。**MT7612Uの実際のハードウェア能力に完全に一致させる必要があります：**

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACM (MT7612U)
interface=wlan1
driver=nl80211
ssid=YourNetworkName
hw_mode=a                     # 5GHz；2.4GHzの場合はgに変更
channel=36                    # UNII-1、非DFS、最も安全な選択
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# MT7612U 正しいHT / VHT capabilities
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42    # channel 36に対応する中心周波数インデックス

# セキュリティ：WPA2 + WPA3混合モード
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK SAE       # WPA2 + WPA3デュアルサポート
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=YourPassword
```

### ⚠️ 最も多い間違い

`ht_capab`にMT7612Uが実際にサポートしていないcapability flags（特にUSB 2.0経由で特定のHT40設定を強制する場合）が含まれていると、hostapdはエラーメッセージが非常に不明瞭なままサイレントクラッシュします。**上記の検証済みフラグ組み合わせのみを使用し、RTL8812AUなど他のチップセットの設定をコピーしないでください。**（出典：[GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)）

### コミュニティレビュー

> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. I have tested the Alfa AWUS036ACM with many different computer systems and Linux distros. In my opinion, it is an outstanding USB WiFi adapter."
> — **morrownr**氏、GitHubで最も権威あるLinux USB WiFiコミュニティ知識ベースのメンテナー

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> — eBayユーザーレビュー

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> — GitHub issue #2 ディスカッションスレッド

---

## 4. AWUS036ACH（RTL8812AU）— 動作するが制限あり {#ach}

### Soft APステータス：⚠️ 条件付きサポート

RTL8812AUはALFAの最も象徴的なペネトレーションテスト用チップセットで、Kali Linuxコミュニティで長年愛用されています。Soft AP機能は実際に動作します——基本的なホットスポット作成は問題ありません——が、Realtekのアウトオブカーネルドライバアーキテクチャにはいくつかの永続的な制限があります。

### 既知の制限

1. **WPA3非対応**：RTL8812AUドライバはWPA3対応と表示されますが、複数のユーザーが実際には機能しないことを確認しています。**WPA2-PSKのみ。**
2. **VIF非対応**：同一カードでAP + Monitorモードを同時実行できません。APとモニタリングの両方が必要な場合は、2枚のアダプタが必要です。
3. **Kali Linux 2025.x ドライバ問題**：最新Kaliのaircrack-ng/rtl8812auドライバに互換性問題があります — 特定の古いコミット（`63cf0b4`）にロールバックする必要があります。kernel 6.14+のインカーネルrtw88ドライバで改善が期待されます。
4. **高消費電力**：最大約800mA — Raspberry Piで複数のUSB機器を同時接続するとシステム不安定の原因に。電源付きUSBハブの使用を推奨。

### hostapd設定（RTL8812AU）

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACH (RTL8812AU)
# 注意：MT7612Uとはcapabilitiesが完全に異なります！
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]

# セキュリティ：WPA2のみ、WPA3は追加しないでください
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
```

### ドライバのインストール（Kali Linux / Ubuntu / Debian）

```bash
sudo apt update && sudo apt install -y dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
# Kali 2025.xでは古いコミットが必要
git checkout 63cf0b4
make && sudo make install
sudo modprobe 88XXau
```

### コミュニティレビュー

> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine."
> — GitHub issue #2 ユーザー

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> — morrownr氏 技術ノート

### ACHについての判断

すでにAWUS036ACHをお持ちの場合は、Soft APとして使用できます（基本的なホットスポット機能は動作します）。しかし、まだ購入しておらず主目的がSoft APであれば、**ACMを選んでください。**

---

## 5. AWUS036AXML / AWUS036AXM（MT7921AUN）— 注意して選択 {#axml}

### Soft APステータス：⚠️ 部分サポート — 既知のファームウェア/ドライバ問題あり

AWUS036AXMLとAWUS036AXMはWiFi 6Eトライバンドフラッグシップで、2.4GHz、5GHz、新しい6GHz帯をカバーします。インカーネルドライバ`mt7921u`はkernel 5.18から組み込まれ、APモードサポートは5.19で正式追加されました。しかし、MT7921AUNチップはBluetooth 5.2も統合しており、これが2024–2025年のコミュニティ最大の頭痛の種となっています。

### APモードのカーネルバージョンマイルストーン

| モード | 最小カーネル |
|--------|------------|
| Managed（通常WiFi） | 5.18+ |
| **APモード（Soft AP）** | **5.19+** |
| AP/VLAN | 5.19+ |
| P2P-GO（Wi-Fi Direct AP） | 6.4+ |

### 既知の問題と解決策

#### 問題1：Bluetooth干渉によるWiFiクラッシュ

kernel 6.6以降、BTサブシステムの変更によりmt7921uのWiFi機能が散発的にクラッシュします。再現性はシステム環境によって異なります。**最も効果的な回避策はbtusbドライバを無効にすることです：**

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

#### 問題2：古いファームウェア

システムのMediaTekファームウェアが古すぎる場合、アダプタが正しく認識されないことがあります。2024年11月以降の最新ファームウェアをインストールしてください：

```bash
# 現在のファームウェアバージョンを確認
dmesg | grep "WM Firmware"
# 表示されるべき：Build Time: 20241106151045 またはそれ以降

# 古い場合、kernel.orgからダウンロード
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek/
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek/
sudo reboot
```

#### 問題3：hostapdバージョン要件

一部のユーザーは、完全なWiFi 6 APモードサポートのためにhostapdをgitからコンパイルする必要があると報告しています。システムパッケージマネージャ版では不完全な場合があります。

#### 問題4：APモードでのTx Power表示異常

`iw`では3 dBmのみと表示され調整不可ですが、実際にはチップに内蔵アンプがあります — これはカーネルドライバの表示問題であり、ハードウェア制限ではありません。

#### 問題5：特定カーネルバージョンでのモニターモード問題

2025年12月現在、kernel 6.18および一部の以前のmt7921uドライババージョンでモニターモードの問題があります。

### コミュニティレビュー

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> — **fhteagle**氏、[GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

### AXML/AXMについての判断

WiFi 6Eの6GHz帯が必要で、時折設定調整することを厭わない場合に選択してください。**安定性が求められる本番環境のSoft APには、ACMを推奨します。**

---

## 6. AWUS036AX / AWUS036AXER（RTL8832BU）— Soft APには非推奨 {#ax}

### Soft APステータス：❌ 非推奨

WiFi 6対応ですが、RTL8832BUチップは「マルチステート」デバイスです — デフォルトでUSB大容量ストレージとして列挙され、Linuxで無線アダプタとして機能するにはUSB mode switchが必要です。

**主な問題点：**

1. **マルチステートデバイス**：展開の複雑さが増す — 接続してもすぐにネットワークアダプタとして認識されない
2. **モニターモード制限**：kernel 6.14未満では不完全なサポート
3. **Soft APコミュニティ事例が極めて少ない**：MT7612UやRTL8812AUと比較して、RTL8832BUのSoft AP実例はほぼ存在しない
4. **コミュニティドキュメントが明確に非推奨**：morrownr/USB-WiFiはこのチップセットを「ペネトレーションテストに非推奨」とマーク

> Yupitekの公式ドキュメントは明確に述べています：「AWUS036AX / AWUS036AXERのRTL8832BUチップセットはkernel 6.14未満で制限付きモニターモードサポートのみであり、ペネトレーションテストには推奨されません。AWUS036ACHまたはAWUS036AXMLを使用してください。」

---

## 7. プラットフォーム互換性マトリックス {#compat-matrix}

### AWUS036ACM（MT7612U）

| プラットフォーム | Soft AP | 備考 |
|---------------|---------|------|
| Kali Linux 2022.x – 2025.x | ✅ | インカーネル、プラグアンドプレイ、kernel 5.x / 6.x対応 |
| Ubuntu 22.04 / 24.04 | ✅ | インカーネル、ゼロ設定、LTS版推奨 |
| Debian 11 / 12 | ✅ | インカーネル、安定 |
| Raspberry Pi 4（RPi OS） | ✅ | 最低消費電力（400mA）、morrownr氏長期検証済み |
| Raspberry Pi 5（RPi OS） | ✅ | Pi 4と同一ドライバ、安定 |

### AWUS036ACH（RTL8812AU）

| プラットフォーム | Soft AP | 備考 |
|---------------|---------|------|
| Kali Linux 2022.x – 2025.x | ⚠️ | 外部ドライバ必要；2025.xではコミット`63cf0b4`が必要 |
| Ubuntu 22.04 / 24.04 | ⚠️ | rtw88またはaircrack-ngコミュニティドライバの手動インストールが必要な場合あり |
| Debian 11 / 12 | ⚠️ | 同上 |
| Raspberry Pi 4 | ⚠️ | 動作するが高消費電力（800mA）、電源付きUSBハブ推奨 |
| Raspberry Pi 5 | ⚠️ | 同上、Pi 5 USBコントローラの差異が動作に影響する可能性あり |

### AWUS036AXML / AWUS036AXM（MT7921AUN）

| プラットフォーム | Soft AP | 備考 |
|---------------|---------|------|
| Kali Linux 2022.x（kernel 5.18+） | ✅ | btusb無効化、ファームウェア更新が必要 |
| Kali Linux 2024.x / 2025.x | ⚠️ | Kernel 6.11+ BT/WiFi競合、不安定 |
| Ubuntu 24.04（kernel 6.8+） | ⚠️ | 2024年末に問題報告あり |
| Ubuntu 25.04 / CachyOS（kernel 6.14+） | ✅ | プラグアンドプレイ、新カーネルで大幅改善 |
| Debian 12 | ⚠️ | カーネルバージョンに依存 |
| Raspberry Pi 4 / 5 | ⚠️ | 成功事例あり、ただしファームウェア確認とBT無効化が必要 |

### AWUS036AX / AWUS036AXER（RTL8832BU）

| プラットフォーム | Soft AP | 備考 |
|---------------|---------|------|
| Kali Linux | ❌ | マルチステート、USB mode switch必要、コミュニティ事例極少 |
| Ubuntu / Debian | ❌ | 同上 |
| Raspberry Pi 4 / 5 | ❌ | 同上 |

---

## 8. Soft AP完全セットアップガイド（AWUS036ACM）{#setup-guide}

以下は、Raspberry Pi 4でAWUS036ACMを使用して5GHz Soft APを設定する完全なステップバイステップガイドです。

### ステップ1：アダプタの検出とドライバの確認

```bash
# アダプタが検出されたことを確認
lsusb | grep MediaTek
# 期待される出力：Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U

# ドライバがロードされたことを確認
dmesg | grep mt76
# 期待される出力：mt76x2u 1-1.4:1.0 wlx00c0ca9821a5: renamed from wlan0

# APモードサポートを確認
iw list | grep -A 10 "Supported interface modes"
# 出力に"* AP"が含まれていることを確認
```

### ステップ2：必要なパッケージのインストール

```bash
sudo apt update
sudo apt install -y hostapd dnsmasq iptables
```

### ステップ3：hostapdの設定

`/etc/hostapd/hostapd.conf`を作成：

```ini
interface=wlan0
driver=nl80211
ssid=Yupitek_AP
hw_mode=a                       # a=5GHz, g=2.4GHz
channel=36                      # UNII-1、非DFS、最も安全
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# HT/VHT設定（MT7612U専用）
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42

# WPA2 + WPA3混合モード
wpa=2
wpa_passphrase=MySecurePassword123
wpa_key_mgmt=WPA-PSK SAE
wpa_pairwise=CCMP
rsn_pairwise=CCMP

auth_algs=1
macaddr_acl=0
ignore_broadcast_ssid=0
```

### ステップ4：dnsmasq（DHCP）の設定

`/etc/dnsmasq.conf`を作成：

```ini
interface=wlan0
dhcp-range=192.168.10.2,192.168.10.100,255.255.255.0,12h
dhcp-option=3,192.168.10.1
dhcp-option=6,8.8.8.8,8.8.4.4
```

### ステップ5：静的IPとNATの設定

```bash
# wlan0に静的IPを割り当て
sudo ip addr add 192.168.10.1/24 dev wlan0

# IPフォワーディングを有効化
sudo sysctl net.ipv4.ip_forward=1

# NATを設定（eth0がアップストリームインターフェースと仮定）
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# iptablesルールを永続化
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```

### ステップ6：サービスの起動

```bash
sudo systemctl unmask hostapd
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# サービスステータスの確認
sudo systemctl status hostapd
sudo systemctl status dnsmasq

# 起動時の自動起動を有効化
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```

完了後、携帯電話やノートPCでWiFiを検索すると、`Yupitek_AP`というSSIDが表示されるはずです。

---

## 9. よくあるトラブルシューティング {#troubleshooting}

### Q1：hostapdが起動後すぐにクラッシュする

**症状**：`sudo systemctl status hostapd`が`exited`または`failed`を表示

**考えられる原因**：`hostapd.conf`にチップセットがサポートしていないcapability flagsが含まれている

**解決策**：余分なflagsを削除。MT7612U（ACM）の場合、セクション3の検証済み設定を使用するのが最も安全です。**他のチップセットのht_capabをコピーしないでください。**

---

### Q2：クライアントが接続してもインターネットにアクセスできない

**症状**：WiFi接続完了、IP取得済み、しかし`ping 8.8.8.8`が応答しない

**チェックリスト**：

```bash
# 1. IPフォワーディングが有効か確認
cat /proc/sys/net/ipv4/ip_forward
# 出力されるべき：1

# 2. NATルールが存在するか確認
sudo iptables -t nat -L POSTROUTING -v
# MASQUERADEルールが表示されるはず

# 3. アップストリームインターフェースが動作しているか確認
ping -I eth0 8.8.8.8
```

---

### Q3：5GHz APが表示されない、または不安定

**考えられる原因**：

1. **DFSチャンネル（100–144）を使用**：MT7612U / MT7610UはDFS非対応 — UNII-1チャンネル（36–48）を使用
2. **送信電力不足**：アンテナがRP-SMAコネクタに正しく固定されているか確認
3. **USB電力不足**（Raspberry Pi）：公式5A電源または電源付きUSBハブを使用

---

### Q4：Raspberry Piでhostapdが繰り返し再起動する

**症状**：`dmesg`にUSBリセットメッセージが頻繁に表示される

**考えられる原因**：USBポートの電力不足（特にAWUS036ACH高電力チップセット、最大800mA）

**解決策**：
- 公式Pi 5A電源を使用
- 電源付きUSBハブを使用
- アダプタをUSB 3.0ポートに接続（Pi 4のみ）

---

### Q5：AWUS036AXML/AXMのWiFiが突然切断される、または起動しない

**考えられる原因**：BluetoothサブシステムがWiFiに干渉（MT7921AUNはBT 5.2内蔵）

**解決策**：Bluetoothドライバを恒久的に無効化

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## 10. 技術詳細：VIF、WPA3、DFSチャンネル {#technical}

### VIF（仮想インターフェース）：1枚のカードで複数の役割

VIF（Virtual Interface）を使用すると、単一の物理アダプタで複数の論理インターフェースを同時に動作させることができます。例：1つのインターフェースがアップストリームルーターに接続（managedモード）し、別のインターフェースがAP（masterモード）として他のデバイスにサービスを提供します。

3つの一般的なシナリオ：

| シナリオ | VIF必要？ | 最適なアダプタ |
|----------|----------|--------------|
| 基本NATルーティング（eth0アップストリーム + wlan AP） | ❌ 不要 | AP対応の任意のアダプタ |
| 無線ブリッジ（WiFi受信 + WiFi AP同時） | ✅ 必要 | ACM（MT7612U） |
| モニター + AP同時（セキュリティ研究 / Rogue AP） | ✅ 必要 | ACM（MT7612U） |

**VIF実践例（MT7612U）：**

```bash
# 既存のwlan1に加えて追加のAP仮想インターフェースを作成
sudo iw phy phy1 interface add ap0 type __ap
sudo ip link set ap0 up
# これでwlan1はアップストリームに接続し、ap0はhostapdを実行
```

MediaTekインカーネルドライバ（mt76x2u、mt7921u）のみがVIFを完全にサポートしています。Realtekアウトオブカーネルドライバには基本的にこの機能がありません — AP + Monitorを同時に実行する必要がある場合は、2枚のアダプタが必要です。

---

### WPA3サポート比較

| チップセット | 対応モデル | WPA2 | WPA3 |
|------------|----------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ SAEネイティブサポート |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ SAEネイティブサポート |
| RTL8812AU | AWUS036ACH | ✅ | ❌ サポート表示あるが機能せず |
| RTL8832BU | AWUS036AX / AXER | ✅ | ⚠️ 未確認 |

---

### 5GHz Soft APのチャンネル選択：DFSを避ける

DFS（Dynamic Frequency Selection）チャンネル（ch100–ch140）にはカーネルレベルのレーダー検出が必要です。MT7612UなどのチップセットはDFSをサポートしていません。5GHz APモードでは以下を選択してください：

| 帯域 | 推奨チャンネル | 理由 |
|------|-------------|------|
| **UNII-1** | **36, 40, 44, 48** | 全チップセット対応、最も安全 |
| UNII-2（DFS） | 52–144 | ほとんど非対応、非推奨 |
| UNII-3 | 149–165 | 部分対応（地域による） |

---

## 11. コミュニティ実践事例 {#real-cases}

### 事例1：RPi4B + AWUS036ACM = 長期安定ホーム5GHz AP

**出典**：morrownr/7612u GitHub知識ベース
**シナリオ**：morrownr氏がRPi4B + AWUS036ACMをホーム5GHz APとして長期使用、Pi内蔵2.4GHzと組み合わせてデュアルバンドサービスを提供
**結果**：長期安定動作、再起動不要、「outstanding」評価
**構成**：hostapd + dnsmasq + iptables NAT

### 事例2：RPi3B+ + ACM — 初期クラッシュ、修正後成功

**出典**：[GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
**問題**：RPi3B+のUSB 2.0経由でhostapdがクラッシュ
**根本原因**：`ht_capab`にUSB 2.0帯域制限下でサポートされないHT40フラグが含まれていた
**解決策**：余分なフラグを削除し、Kali Linuxで起動成功

### 事例3：Pi PwnBox + AWUS036ACH = レッドチームRogue AP

**出典**：GitHub koutto/pi-pwnbox-rogueap
**シナリオ**：RPi3B+でRogue APプラットフォームを構築：RTL8812AU（AWUS036ACH）1枚でAP担当、RT3070（AWUS036NEH）1枚でパケットインジェクション攻撃担当
**重要な発見**：RTL8812AUはVIF非対応のため、2枚のカードで役割分担が必要（ACMなら1枚で完結）

### 事例4：AWUS036AXMLがRPi3B ArchLinux ARMで安定AP動作

**出典**：[GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
**シナリオ**：RPi3B ArchLinux aarch64でAWUS036AXMLをAPモードで正常実行
**引用**：「It's the most stable mt7921 in my collection.」
**重要な条件**：hostapdをgitからコンパイル + btusb無効化

### 事例5：AWUS036ACHM（MT7610U、製造終了）がPi4でフルスピードAP達成

**出典**：[GitHub Discussion #31](https://github.com/morrownr/USB-WiFi/discussions/31)
**問題**：初期設定では65 Mbpsリンク速度のみ、AC 5GHzフルスピードに達せず
**解決策**：正しい`vht_oper_chwidth=1`と`vht_oper_centr_freq_seg0_idx`設定を追加し、433 Mbpsリンクレートを達成
**ACMへの示唆**：同じVHTパラメータ設定がMT7612U（ACM）にも重要

---


---

{{< faq >}}

## 12. 購入推奨と最終判断 {#recommendations}

### クイック判断マトリックス

| 評価 | モデル | 最適な対象 | 一言 |
|------|--------|----------|------|
| 🥇 **最推奨** | **AWUS036ACM** | 全員、特に初めてSoft APを構築する方 | 全プラットフォーム安定、手間ゼロ |
| 🥈 使用可能 | AWUS036ACH | すでにこのモデルをお持ちの方 | ドライバ必要、WPA3なし |
| 🥉 上級者向け | AWUS036AXML | WiFi 6Eが必要で設定調整を厭わない方 | 6GHzの利点、手動修正必要 |
| ❌ スキップ | AWUS036AX / AXER | N/A | Soft APのコミュニティ検証なし |

### 🎯 判断ガイド

- **Kali / Ubuntu / Debian / Raspberry Pi 4または5で安定したSoft APが必要ですか？**
  → **AWUS036ACM**を選んでください。これ一択です。

- **すでにAWUS036ACHをお持ちで、Soft APを試してみたいですか？**
  → 動作しますが、WPA2のみでドライバのインストールが必要です。これらの制限を受け入れられるなら問題ありません。

- **WiFi 6E（6GHz帯）が必要で、設定作業を厭わないですか？**
  → AWUS036AXML — BTドライバを無効化し、kernel ≥ 6.6 LTSを確認してください。

- **主目的がSoft APで、ペネトレーションテストではありませんか？**
  → AWUS036ACMが全プラットフォームで広範なコミュニティ検証がある唯一の選択肢です。

---

### 結論

Soft AP構築の核心は、WiFi速度でもアンテナの本数でもありません——**チップセットドライバのAPモードサポートこそが鍵です。**

調査した全ALFA製品の中で、**AWUS036ACM（MT7612U）**は「インカーネルドライバ、WPA3ネイティブサポート、VIF仮想インターフェース、低消費電力、クロスプラットフォーム安定性」を同時に満たす唯一のアダプタです。Soft APにおけるゴールドスタンダードです。

AWUS036ACH（RTL8812AU）は制限を受け入れれば使用可能です。AWUS036AXML/AXM（MT7921AUN）は大きな可能性を秘めていますが、ドライバの成熟度はまだ発展途上です。AWUS036AX/AXER（RTL8832BU）は、この用途には推奨しません。

**Raspberry PiやKali Linuxで初めてSoft APを設定するなら — ACMを選んでください。後悔はしません。**

---

### 購入リンク

- [AWUS036ACM — Soft AP最推奨](/ja/products/alfa/awus036acm/)
- [AWUS036ACH — クラシックペンテストアダプタ](/ja/products/alfa/awus036ach/)
- [AWUS036AXML — WiFi 6Eトライバンドフラッグシップ](/ja/products/alfa/awus036axml/)
- [ALFA Network 全製品ラインアップ](/ja/products/alfa/)

### 参考資料

- [AWUS036ACH vs AWUS036ACM：チップセットドライバ完全比較](/ja/blog/awus036ach-vs-awus036acm/)
- [AWUS036ACM IBSS & Mesh on Raspberry Pi](/ja/blog/)
- [morrownr/USB-WiFi — 最も権威あるLinux USB WiFi知識ベース](https://github.com/morrownr/USB-WiFi)（4,100+ stars）
- [morrownr/7612u — MT7612Uリファレンス（RPi4B Bridged APチュートリアル含む）](https://github.com/morrownr/7612u)
- [DeepWiki — morrownr/USB-WiFi自動キュレーション知識ベース](https://deepwiki.com/morrownr/USB-WiFi)

---

### 📚 データソース

本記事は以下の情報を集約しています：
- **morrownr/USB-WiFi** GitHub知識ベース（4,100+ stars）、完全なiw_list記録
- **morrownr/7612u** — MT7612U Bridged AP on RPi4Bチュートリアル
- **GitHub Issue Tracker** — issue #2（ACM AP設定）、#476（AXML APテスト）、Discussion #31（ACHMフルスピードAP）
- **koutto/pi-pwnbox-rogueap** — AlfaアダプタRogueAP実装事例
- **Rokland** 正規販売店Linuxサポートページ
- **Lab401** 技術レビューおよび2025年ペンテスト推奨製品レポート
- **Raspberry Pi公式フォーラム** — Pi 4/5 USB WiFi互換性議論
- **Yupitek既存ブログ** — ACM China Install Guide、AXML WiFi 6E Review、Kali Linux 2026ベストアダプタ

---

> **タグ**：#ALFANetwork #SoftAP #WiFiHotspot #hostapd #KaliLinux #Ubuntu #Debian #RaspberryPi #AWUS036ACM #AWUS036ACH #AWUS036AXML #MT7612U #RTL8812AU #MT7921AUN #Yupitek
>
> **著者**：Yupitek Ltd — ALFA Network 正規販売代理店（台湾）
>
> **免責事項**：調査データは2026年5月現在のものです。Linuxカーネルとディストリビューションは継続的に進化しており、ドライバサポートはバージョンによって変更される可能性があります。デプロイ前にターゲットプラットフォームのカーネルバージョンとドライバ互換性を確認してください。
>
> **テクニカルサポート**：Soft AP設定に関する問題は、Yupitek台湾テクニカルサポートまでお問い合わせください。製品に関するお問い合わせ：[yupitek.com](https://yupitek.com/ja/)。

---

## 参考文献

1. [morrownr/USB-WiFi GitHubナレッジベース](https://github.com/morrownr/USB-WiFi)
2. [hostapd公式ドキュメント](https://w1.fi/cgit/hostap/)
3. [Linux Wireless mt76ドライバー](https://wireless.wiki.kernel.org/en/users/Drivers/mt76)
4. [Raspberry Pi公式ドキュメント](https://www.raspberrypi.com/documentation/)
5. [Kali Linux公式ドキュメント](https://www.kali.org/docs/)
