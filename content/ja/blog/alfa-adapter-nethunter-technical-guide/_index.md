---
title: "ALFA無線アダプターとKali NetHunter完全技術ガイド2026"
description: "Kali NetHunterでALFA USB WiFiアダプターを使用するための技術リファレンス。台湾市場のスマートフォン互換性、カーネル内蔵ドライバー vs DKMS分析、OTGセットアップ、検証済みテスト結果を網羅。"
date: 2026-06-09
draft: false
showBreadcrumbs: true
showTableOfContents: true
featureimage: /images/blog/alfa-nethunter-technical-guide-hero.png
tags: ["nethunter", "kali-linux", "alfa-network", "wireless-security", "android", "usb-otg", "monitor-mode", "packet-injection", "mt7610u", "mt7612u", "rtl8812au"]
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "ALFA無線アダプターをKali NetHunterで使うのに必要なスマートフォンの条件は？"
    answer: "OTG対応のAndroidスマートフォン、Root取得済みでKali NetHunterカーネルをフラッシュ済みであること。互換性確認済み機種はGoogle Pixelシリーズ、OnePlusの旧フラッグシップ機種です。具体的な互換性はカーネルバージョンとアダプターチップドライバーの配置に依存します。"
  - question: "MT7610U/MT7612UとRTL8812AUドライバーの違いは？"
    answer: "MT7610U/MT7612Uドライバーはカーネルツリー内にあり、挿すだけでコンパイル不要。RTL8812AUはDKMS外部ドライバーのコンパイルインストールが必要で、カーネル更新後に再コンパイルが必要な場合があります。セキュリティ現場ではカーネルツリー内ドライバーの安定性が高いです。"
  - question: "ALFAアダプターはNetHunterでMonitor Modeをサポートしていますか？"
    answer: "はい、MT7610U/MT7612UはMonitor Modeとパケットインジェクションをサポートします。RTL8812AUもカーネル6.12未満でサポートしますが、6.12以降ではMonitor Modeが制限されます。セキュリティリサーチではMT7610U/MT7612Uアダプターを優先してお勧めします。"
---

基本的なOTG手順でNetHunterとALFAアダプターをセットアップ済みの方で、クイックスタート版をお探しの場合は、[OTGセットアップガイド](/ja/blog/alfa-adapter-nethunter-android-otg/)で要点をまとめています。本記事はさらに深く掘り下げた内容です——ハードウェア購入前にスマートフォンとアダプターの互換性を評価し、カーネルアップデート後も動作し続けるドライバー方式を理解し、特定の組み合わせに確定する前に検証済みのテスト結果を確認したい、セキュリティ専門家向けの完全な技術リファレンスです。


{{< tldr >}}
MT7610U/MT7612Uはカーネルネイティブドライバーでプラグアンドプレイ、RTL8812AUはDKMSコンパイルが必要。NetHunterスマートフォンはRootとOTGサポートが必要で、ドライバー問題を避けるためMT7612Uアダプターを優先しましょう。
{{< /tldr >}}
本記事では、多くのNetHunterガイドがスキップしている問いに焦点を当てます：**どのアダプターが真のプラグアンドプレイで、どれが最悪のタイミングでドライバーコンパイルの迷宮に陥らせるのか？** その答えはチップセット、スマートフォンのカーネルバージョン、そしてドライバーがカーネルツリー内に存在するか、外部のDKMSリポジトリに依存するか、の3要素にかかっています。選択を誤ると、現場で `modprobe` エラーを眺めながらアダプターはバッグの中に眠ったままです。正しい選択をすれば、差し込んですぐスキャンを開始できます。

---

## 1. 顧客要件

### 1.1 ユースケース

モバイルペネトレーションテスターは、ノートPCを完全に置き換えるセットアップを必要とします。スマートフォンでKali NetHunterを実行し、ALFAアダプターをUSB OTG経由で接続し、ノートPCを持ち歩かずにWi-Fiセキュリティ評価を実施します。中核となるワークフロー——サイトサーベイ、モニターモードキャプチャ、パケットインジェクション、WPAハンドシェイク収集——は、バッテリー駆動で確実に動作しなければなりません。

### 1.2 中核要件

| Requirement | Detail |
|---|---|
| Platform | Kali NetHunter（フルエディション、カスタムカーネル）搭載のAndroidスマートフォン |
| Connection | USB OTGケーブルまたは給電型OTGハブ |
| Adapter | モニターモードおよびパケットインジェクション対応のALFA USB WiFiアダプター |
| Driver approach | コンパイル依存を排除するため、カーネル内蔵（ドライバーレス）チップセットを優先 |
| Taiwan market | 台湾で正規販売されているスマートフォン、2024〜2026年モデル |
| Power | バッテリー駆動。持続使用には給電型OTGハブを強く推奨 |

---

## 2. 対象ハードウェア・ソフトウェア分析

### 2.1 台湾で入手可能なNetHunter対応スマートフォン

NetHunterは117以上のデバイスモジュールをサポートしていますが、その大半は旧モデルです。(a) 台湾で正規入手可能、(b) 2024年以降発売、(c) 動作するNetHunterカスタムカーネルが存在する、という条件で絞り込むと、以下の3機種が際立ちます。

| Model | Codename | CPU | Kernel Versions | Pre-built Images | Taiwan Availability |
|---|---|---|---|---|---|
| **OnePlus 11 5G** | salami | Snapdragon 8 Gen 2 (ARM64) | 2 | 2 | ✅ 輸入チャネル経由で入手可能、2023年発売 |
| **Nothing Phone (1)** | spacewar | Snapdragon 778G+ (ARM64) | 3 | 1 | ✅ 台湾で正規発売済み、活発なコミュニティ |
| **Samsung Galaxy S20 FE 5G** | r8q | Snapdragon 865 (ARM64) | 5 | 1 | ✅ 台湾で販売——**Snapdragon版が必須** |

{{< alert "triangle-exclamation" >}}
**Samsung Exynosに関する警告：** 台湾の通信キャリアを通じて販売されているSamsung端末の多くはExynosチップセットを搭載しています。NetHunterカーネルがサポートするのはSnapdragon版（`r8q`）のみです。NetHunter用にSamsung端末を購入する前に、CPUモデルを必ず確認してください——製品ページに「Exynos」と記載されている場合は動作しません。Snapdragon版を輸入するか、代わりにOnePlus 11を選んでください。
{{< /alert >}}

**NetHunter Rootless**はroot権限なしの任意のAndroid端末で動作しますが、モニターモード用の外部USB WiFiアダプターには対応していません。パケットキャプチャとインジェクションが必要な場合は、カスタムカーネルを搭載したNetHunterフルエディションが必要です。

### 2.2 プラットフォーム技術仕様

OnePlus 11 5Gをリファレンスプラットフォームとして：

| Parameter | Specification |
|---|---|
| CPU Architecture | ARM64 (aarch64) |
| SoC | Qualcomm Snapdragon 8 Gen 2 (SM8550) |
| USB Controller | USB 3.1 Gen 1（OTG対応） |
| USB Power Delivery | 5V / 900mA（持続的なアダプター動作には給電型OTGハブを使用） |

### 2.3 ソフトウェア環境

| Component | Requirement | Recommended Version |
|---|---|---|
| Host OS | Kali chrootを搭載したAndroid | Android 11+ |
| NetHunter | フルエディション（カスタムカーネル） | 2024.4（最新安定版） |
| Linux Kernel | デバイス固有のカスタムカーネル | 5.x以降を推奨 |
| Preloaded Drivers | マトリックスはセクション4を参照 | — |
| DKMS | RTL8812AUベースのアダプターのみ必須 | カーネルヘッダーが一致していること |
| Wireless Tools | aircrack-ng、Kismet、MANA Toolkit | NetHunter chrootが提供 |
| Root | 全機能に必須 | Magisk 26.0+ |

---

## 3. ALFAアダプター仕様とドライバーソース

### 3.1 AWUS036ACHM — NetHunter向け最優先候補

| Parameter | Specification |
|---|---|
| Chipset | **MediaTek MT7610U** |
| USB VID/PID | `0x0e8d:0x7610` |
| Bands | 2.4 GHz + 5 GHz (AC433) |
| Max Data Rate | 150 Mbps (2.4 GHz) / 433 Mbps (5 GHz) |
| USB | USB 2.0 |
| Monitor Mode | ✅ 完全サポート |
| Packet Injection | ✅ 完全サポート |
| Antenna | 1× 着脱式ハイゲイン (RP-SMA) |
| Driver | **カーネル内蔵** — インストール不要 |
| Kernel Module | `mt76x0u` |
| Kernel Requirement | Linux 4.19+ |
| Product Page | [/ja/products/alfa/awus036achm/](/ja/products/alfa/awus036achm/) |

MT7610Uチップセットは、その `mt76x0u` ドライバーがLinux 4.19以降メインラインカーネルに組み込まれているため、KaliおよびNetHunterコミュニティで広く推奨されています。差し込めばカーネルが認識し、すぐに作業を開始できます。コンパイルツールチェーンも、カーネルヘッダーも、DKMSも不要——`lsusb` で確認した後 `airmon-ng start` を実行するだけです。

### 3.2 AWUS036ACM — 高性能オルタナティブ

| Parameter | Specification |
|---|---|
| Chipset | **MediaTek MT7612U** |
| USB VID/PID | `0x0e8d:0x7612` |
| Bands | 2.4 GHz + 5 GHz (AC1200) |
| Max Data Rate | 300 Mbps (2.4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| Monitor Mode | ✅ 完全サポート |
| Packet Injection | ✅ Kali 2024.3 / 2025.1で安定動作確認済み |
| Antenna | 2× デュアルアンテナ (RP-SMA)、MIMO 2T2R |
| Driver | **カーネル内蔵** — インストール不要 |
| Kernel Module | `mt76x2u` |
| Kernel Requirement | Linux 4.19+ |
| Product Page | [/ja/products/alfa/awus036acm/](/ja/products/alfa/awus036acm/) |

ACMはAC1200デュアルバンドにMIMO 2T2R、USB 3.0スループットを追加しています。`mt76x2u` ドライバーもカーネル4.19以降メインラインです。注意点：一部の古いNetHunterカスタムカーネル（特にOnePlus 7Tのカーネル4.14）では `mt76x2u` モジュールがビルドに含まれていない場合があります。カーネル4.19以降では問題になりませんが、古いカーネルビルドを使用している場合は `lsmod | grep mt76x2u` で確認してください。

### 3.3 AWUS036ACH — 最も広範なコミュニティサポート

| Parameter | Specification |
|---|---|
| Chipset | **Realtek RTL8812AU** |
| USB VID/PID | `0x0bda:0x8812` |
| Bands | 2.4 GHz + 5 GHz (AC1200) |
| Max Data Rate | 300 Mbps (2.4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| Monitor Mode | ✅ 完全サポート |
| Packet Injection | ✅ 完全サポート |
| Antenna | 2× 5dBi 外部アンテナ (RP-SMA) |
| Driver | 外部DKMS（ほとんどのNetHunterカーネルでプリコンパイル済み） |
| Kernel Module | `88XXau` |
| Driver Repo | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| Product Page | [/ja/products/alfa/awus036ach/](/ja/products/alfa/awus036ach/) |

ACHは長年、KaliとNetHunterセットアップのデファクトスタンダードです。ほとんどのNetHunterカスタムカーネルには `88XXau` モジュールがプリコンパイル済みで出荷されるため、通常はソースからのビルドは不要です。ただし、お使いのカーネルバージョンにモジュールが含まれていない場合、一致するカーネルヘッダーを備えたコンパイル環境が必要になります——これはまさにMT7610UやMT7612Uチップセットが回避している依存関係の連鎖です。デュアル5dBiアンテナによりラインナップ最強の信号到達距離を実現しており、長距離キャプチャシナリオで有効です。

### 3.4 AWUS036ACS — コンパクトフォームファクター

| Parameter | Specification |
|---|---|
| Chipset | Realtek RTL8811AU |
| USB VID/PID | `0x0bda:0x0811` |
| Bands | 2.4 GHz + 5 GHz (AC433) |
| USB | USB 2.0 |
| Monitor Mode | ✅ 対応（RTL8812AUと同一ドライバーファミリー） |
| Packet Injection | ✅ 対応 |
| Antenna | 内蔵、55mm超薄型ボディ |
| Power Draw | ~300mW — ラインナップ最低 |
| Driver | 外部（RTL8812AUとaircrack-ngリポジトリを共有） |
| Product Page | [/ja/products/alfa/awus036acs/](/ja/products/alfa/awus036acs/) |

ACSは最もポータブルな選択肢です。300mWの消費電力はスマートフォンのバッテリーに最も優しく、スリムなフォームファクターはポケットにすっぽり収まります。トレードオフはシングルストリームAC433性能と、RTL8812AUファミリーと共通の外部DKMSドライバー依存です。

### 3.5 NetHunterに非推奨のアダプター

| Adapter | Chipset | Reason |
|---|---|---|
| AWUS036AX / AWUS036AXER | RTL8832BU | カーネル6.14+が必要。Androidカーネルでのモニターモード安定性未検証 |
| AWUS036AXML / AWUS036AXM | MT7921AUN | WiFi 6E / 6 GHzサポートが現行NetHunterカーネルビルドで不安定。主要ペネトレーションテスト用アダプターとして不適 |

### 3.6 ドライバーソースリポジトリ

| Chipset | Driver | Source |
|---|---|---|
| MT7610U | `mt76x0u`（カーネル内蔵） | [torvalds/linux — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| MT7612U | `mt76x2u`（カーネル内蔵） | 上記と同一カーネルツリー |
| RTL8812AU | `88XXau`（外部） | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| RTL8811AU | `88XXau`（外部、共有） | 同一aircrack-ngリポジトリ |

---

## 4. ドライバー互換性分析

### 4.1 カーネル内蔵 vs 外部DKMS

NetHunter用のアダプターを選ぶ際、最も重要な判断基準はドライバーがカーネルツリー内部にあるか外部にあるかです。その理由は以下の通りです：

| | In-Kernel（MT7610U, MT7612U） | External DKMS（RTL8812AU, RTL8811AU） |
|---|---|---|
| プラグアンドプレイ | ✅ はい — 挿入時に自動認識 | ⚠️ カーネルに `88XXau` がプリコンパイルされているかに依存 |
| カーネルアップデート後も動作 | ✅ はい — ドライバーはカーネルビルドの一部 | ❌ カーネルアップデート後に破損する可能性あり。再コンパイルが必要 |
| linux-headersの要否 | ❌ 不要 | ✅ 手動コンパイル時は必要 |
| DKMSの要否 | ❌ 不要 | ✅ カーネルにプリコンパイルされていない場合は必要 |
| コミュニティドキュメント | 中程度 | 豊富（ACHのチュートリアルが最多） |
| 現場での故障リスク | 低 | 中程度（コンパイル依存） |

**結論：** 現場でドライバー問題が発生するリスクを最小限に抑えたいなら、MT7610UまたはMT7612Uアダプターを選んでください。ドライバーはすでにカーネル内にあります——コンパイルするものはなく、アップデートで壊れるものもなく、現場でトラブルシューティングするものもありません。

### 4.2 NetHunterカーネルモジュールサポートマトリックス

| Device | NetHunter Kernel | MT7610U (`mt76x0u`) | MT7612U (`mt76x2u`) | RTL8812AU (`88XXau`) |
|---|---|---|---|---|
| OnePlus 11 5G | Android 13 kernel | ✅ Supported | ✅ Supported | ✅ Supported |
| Samsung S20 FE (Snapdragon) | Android 12 kernel (4.19) | ✅ Supported | ✅ Supported | ✅ Supported（XDAレポート要確認） |
| Nothing Phone (1) | Android 12/13 kernel | ✅ Supported | カーネル設定確認要 | ✅ Supported |
| OnePlus 7/7T | 4.14（旧バージョン） | ✅ Supported | ⚠️ ビルドに含まれていない可能性あり | ✅ Supported |

出典：NetHunter GitLab、XDA Forumsコミュニティレポート（2024〜2026年）。

### 4.3 既知の問題

**問題1：古いカーネルでMT7612Uインターフェースが表示されない**

症状：`lsusb` は `0e8d:7612` を表示するが、`ip link` に `wlan1` が表示されない。  
根本原因：カスタムカーネルが `mt76x2u` モジュールなしでコンパイルされている。一部の4.14ベースNetHunterカーネル（OnePlus 7T世代）に影響。  
修正方法：モジュールを含むカーネルビルドを使用するか、古いカーネルでもより広くサポートされているAWUS036ACHM（MT7610U）に切り替える。

**問題2：USB電力ブラウンアウトによるアダプター切断**

症状：スキャン中にアダプターが消失し、`dmesg` にUSBリセットエラーが表示される。  
根本原因：スマートフォンのUSBポートがアダプターの消費電流を維持できない。特にUSB 3.0アダプター（ACHは約500mW消費）で発生。  
修正方法：壁コンセントからアダプターに5Vを供給しつつデータをスマートフォンに渡す、給電型OTGハブを使用する。

**問題3：chroot起動前にアダプターを接続した**

症状：AndroidがUSB権限ダイアログを表示するが、Kaliツールがアダプターにアクセスできない。  
根本原因：USBデバイスが公開される前にNetHunter chroot環境が起動している必要がある。  
修正方法：先にchrootを起動し（Kali Services → Start）、その後にアダプターを接続してUSB権限を許可する。

---

## 5. セットアップガイド

### 5.1 前提条件

ハードウェアを接続する前に、以下を確認してください：

```bash
# 端末がroot化されていることを確認
su -c "id"

# NetHunter chrootバージョンを確認
cat /kali/etc/os-release
# NetHunter搭載のKali Linuxと表示されるはず

# USB OTGが有効化されていることを確認
# 設定 → 開発者向けオプション → OTG（正確な場所はAndroidバージョンにより異なります）
```

### 5.2 ハードウェア接続手順

順序が重要です：

1. **NetHunterアプリ**を起動 → **Kali Services**を開く → **Start**をタップしてchrootを起動
2. **給電型OTGハブ**をスマートフォンのUSBポートに接続
3. **ALFAアダプター**をOTGハブに接続
4. AndroidのUSB権限ダイアログが表示されたら、**OK**をタップし、**常に許可**にチェックを入れる

{{< alert "circle-info" >}}
持続的な運用には給電型OTGハブを強く推奨します。AWUS036ACHは約500mWを消費します——スマートフォンのバッテリーから直接給電すると、バッテリー消耗が著しく加速し、USBの不安定性を引き起こす可能性があります。壁コンセントから電力を引きつつデータを通過させるハブを使用すれば、両方の問題が解消されます。
{{< /alert >}}

### 5.3 アダプター検出の確認

```bash
# USBデバイスを一覧表示 — アダプターが表示されることを確認
lsusb

# モデル別の想定出力：
# AWUS036ACHM: Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.
# AWUS036ACM:  Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U
# AWUS036ACH:  Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp.
```

アダプターが表示されない場合：別のOTGケーブルを試す、開発者向けオプションでOTGが有効になっていることを確認する、またはアダプターが正常に動作するかPCでテストしてください。

### 5.4 ドライバーのロード

**MT7610U（AWUS036ACHM）の場合 — ほとんどのカーネルで自動ロード：**

```bash
# 自動ロードを確認
lsmod | grep mt76

# 必要に応じて手動ロード（稀）
sudo modprobe mt76x0u
```

**MT7612U（AWUS036ACM）の場合 — カーネル4.19以降で自動ロード：**

```bash
# 確認
lsmod | grep mt76

# 必要に応じて手動ロード
sudo modprobe mt76x2u
```

**RTL8812AU（AWUS036ACH）の場合 — ほとんどのNetHunterカーネルでプリコンパイル済み：**

```bash
# プリコンパイル済みモジュールをロード
sudo modprobe 88XXau

# ロードされたことを確認
lsmod | grep 88XX
```

### 5.5 ネットワークインターフェースの確認

```bash
# ワイヤレスインターフェースを一覧表示
ip link show | grep wlan

# またはiwを使用
iw dev

# 外部アダプターは通常wlan1として表示されます
# （wlan0は通常、スマートフォン内蔵WiFiです）
```

### 5.6 モニターモードの有効化

```bash
# 干渉するプロセスを停止
sudo airmon-ng check kill

# アダプターでモニターモードを開始
sudo airmon-ng start wlan1

# モニターモードが有効であることを確認
iwconfig wlan1mon
# 想定出力：Mode:Monitor

# 近隣ネットワークをスキャン（許可されたテストのみ）
sudo airodump-ng wlan1mon

# 全バンドをスキャン（2.4 GHz + 5 GHz）
sudo airodump-ng --band abg wlan1mon
```

### 5.7 管理モードへの復帰

```bash
sudo airmon-ng stop wlan1mon
sudo service NetworkManager restart
```

---

## 6. アプリケーショントポロジー

<img src="/images/blog/nethunter-topology.png" alt="NetHunter + ALFA Application Topology Diagram" loading="eager" style="max-width:100%;height:auto;display:block">

---

## 7. 検証結果

### 7.1 テストマトリックス

以下の組み合わせは、コミュニティテストとベンダードキュメントを通じて検証されています：

| Phone | ALFA Adapter | Chipset | Monitor Mode | Packet Injection | Status |
|---|---|---|---|---|---|
| OnePlus 11 5G | AWUS036ACHM | MT7610U | ✅ | ✅ | Verified |
| OnePlus 11 5G | AWUS036ACM | MT7612U | ✅ | ✅ | Verified |
| OnePlus 11 5G | AWUS036ACH | RTL8812AU | ✅ | ✅ | Verified |
| Samsung S20 FE (Snapdragon) | AWUS036ACH | RTL8812AU | ✅ | ⚠️ | コミュニティレポート — カーネル設定要確認 |
| Samsung S20 FE (Snapdragon) | AWUS036ACHM | MT7610U | ✅ | ✅ | コミュニティレポート |
| Nothing Phone (1) | AWUS036ACHM | MT7610U | ✅ | ✅ | コミュニティレポート |

出典：XDA Forums、Reddit r/NetHunter、Kali NetHunter GitLab Issues（2024〜2026年）。

### 7.2 想定される `lsusb` 出力

```
# AWUS036ACHM
Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.

# AWUS036ACM
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter

# AWUS036ACH
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
```

### 7.3 モニターモード検証

```bash
# 成功時のiwconfig想定出力
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.437 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

---

## 8. 推奨構成

### 8.1 最優先候補：OnePlus 11 5G + AWUS036ACHM

この組み合わせは、テスト済みの全セットアップの中で最も障壁が低い構成です。OnePlus 11は、台湾市場向けに現在も入手可能な、公式NetHunterカーネルサポートを備えた最新のフラッグシップです。AWUS036ACHMのMT7610Uチップセットは `mt76x0u` ドライバーを使用します——これはカーネル4.19以降メインラインに組み込まれており、コンパイルが一切不要で、国際セキュリティコミュニティ（Lab401、morrownr USB-WiFiデータベース）でもKaliとNetHunter向けの最も安全な選択肢として一貫して評価されています。アダプターはコンパクトでシングルアンテナ、USB 2.0動作であり、モバイルシナリオでは利点となります——低消費電力、低発熱、故障リスクが少ない。

### 8.2 高性能候補：OnePlus 11 5G + AWUS036ACM

遠距離での5GHzキャプチャ向けにMIMO 2T2RのデュアルバンドAC1200性能が必要な場合、ACMはカーネル内蔵ドライバーエコシステムを離れることなくそれを提供します。MT7612Uの `mt76x2u` ドライバーもカーネル4.19以降メインラインです。トレードオフ：USB 3.0は消費電力が大きく、デュアルアンテナボディは大型です。カーネルに `mt76x2u` が含まれていることを確認してください——OnePlus 11では確認済みです。

### 8.3 コミュニティ定番：任意のNetHunter端末 + AWUS036ACH

ACHはNetHunterエコシステムにおいて、最も多くのチュートリアル、最大のコミュニティトラブルシューティングベース、最高のサードパーティドキュメントを誇るアダプターです。デュアル5dBiアンテナによりALFAラインナップ最強の信号到達距離を実現します。ほとんどのNetHunterカーネルは `88XXau` モジュールをプリコンパイルしているため、コンパイルが必要になることは稀です。プラグアンドプレイの簡便さよりもコミュニティサポートと長距離キャプチャを重視するなら、これが選択肢です。

### 8.4 シナリオ別選択

| Scenario | Recommended Combo | Rationale |
|---|---|---|
| 初めてのNetHunterセットアップ、リスク最小化 | OnePlus 11 + AWUS036ACHM | カーネル内蔵ドライバー、コンパイル不要、最小フォームファクター |
| 広範囲デュアルバンドキャプチャ | OnePlus 11 + AWUS036ACM | AC1200 + MIMO、カーネル内蔵 |
| 長距離サーベイ、最大のチュートリアル数 | 任意の対応端末 + AWUS036ACH | 最強アンテナ、最も広いコミュニティサポート |
| 超ポータブル、最小消費電力 | 任意の対応端末 + AWUS036ACS | 300mW消費、どのポケットにも収まる |

### 8.5 サポートリソース

| Resource | Link |
|---|---|
| Yupitek — ALFA正規代理店台湾 | [yupitek.com](https://www.yupitek.com) |
| ALFA Network公式製品ページ | [alfa.com.tw](https://www.alfa.com.tw) |
| MT7610Uドライバー（カーネルツリー） | [torvalds/linux — mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| RTL8812AUドライバー（aircrack-ng） | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| NetHunter対応デバイス一覧 | [nethunter.kali.org/device-kernels.html](https://nethunter.kali.org/device-kernels.html) |
| NetHunter公式ドキュメント | [kali.org/docs/nethunter/](https://www.kali.org/docs/nethunter/) |
| XDA NetHunterフォーラム | [xdaforums.com/tags/nethunter/](https://xdaforums.com/tags/nethunter/) |
| Yupitek ALFA製品カタログ | [/ja/products/alfa/](/ja/products/alfa/) |

---

## 付録：クイックトラブルシューティング

**アダプターが `lsusb` に表示されない：**
1. 開発者向けオプションでOTGが有効になっているか確認
2. 別のOTGケーブルを試す——ケーブル品質が最も一般的な障害ポイント
3. 給電型OTGハブを使用する
4. NetHunter chrootが起動済みであることを確認

**`lsusb` にデバイスが表示されるが `wlan1` インターフェースがない：**

```bash
# カーネルメッセージでドライバーエラーを確認
dmesg | tail -30 | grep -E "usb|mt76|rtl|88XX"

# カーネルモジュールの存在を確認
find /lib/modules -name "mt76*" 2>/dev/null
find /lib/modules -name "*88XX*" 2>/dev/null

# 手動ロードを試行
sudo modprobe mt76x0u   # MT7610U
sudo modprobe mt76x2u   # MT7612U
sudo modprobe 88XXau    # RTL8812AU
```

**モニターモードは開始するがネットワークが表示されない：**

```bash
# まず干渉するプロセスを停止
sudo airmon-ng check kill

# 全バンドを再スキャン
sudo airodump-ng --band abg wlan1mon

# チャンネル設定を確認
sudo iw dev wlan1mon info
```

**使用中にアダプターが切断される（USBリセット）：**

```bash
# 一時的な修正 — 送信電力を下げる
sudo iw dev wlan1 set txpower fixed 1000  # 10 dBm

# 恒久的な修正 — 給電型OTGハブを使用する
```

---


---

{{< faq >}}

## 関連ガイド

- [ALFAアダプターとNetHunterの基本OTGセットアップ](/ja/blog/alfa-adapter-nethunter-android-otg/)
- [ALFA WiFiアダプター購入ガイド2026](/ja/blog/alfa-wifi-adapter-buyer-guide-2026/)
- [Kali LinuxとUbuntuへのALFAドライバーのインストール](/ja/blog/install-alfa-driver-kali-ubuntu/)
- [Raspberry PiとKaliでのALFAアダプターの使用](/ja/blog/alfa-adapter-raspberry-pi-kali/)

---

*本文書は**Yupitek Ltd**（ALFA Network台湾正規代理店）が作成しました。*  
*データは2026-06-09時点のものです。LinuxカーネルおよびNetHunterのバージョンは定期的に更新されます。最新の互換性情報については公式ソースを確認してください。*

---

## 参考文献

1. [Kali NetHunter公式ドキュメント](https://www.kali.org/docs/nethunter/) — NetHunterインストールとカーネルフラッシュガイド
2. [Linux Kernel mt76ドライバーソースコード](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek/mt76) — MT7610U/MT7612Uメインラインドライバー
3. [aircrack-ng RTL8812AUドライバー](https://github.com/aircrack-ng/rtl8812au) — DKMS外部ドライバーリポジトリ
4. [ALFA Network公式ウェブサイト](https://alfa.com.tw/) — 製品仕様とドライバーダウンロード
5. [Android USB OTG公式ドキュメント](https://developer.android.com/guide/topics/connectivity/usb) — OTG APIとハードウェア要件
