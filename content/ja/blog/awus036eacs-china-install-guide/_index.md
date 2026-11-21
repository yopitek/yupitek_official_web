---
title: "ALFA AWUS036EACS 設定ガイド（中国版）：WindowsでのインストールとLinux互換性について"
description: "中国国内でのALFA AWUS036EACSの設定ガイド。RTL8821CU WiFi 5 + Bluetooth 4.2 Nanoアダプター。Windows用ドライバは files.alfa.com.tw から入手可能です。Linuxカーネル6.2以降では内蔵のrtw88_8821cuドライバが挿すだけで動作し、モニターモードとインジェクションも実測で動作します。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036eacs-china-install-guide"
tags: ["alfa", "awus036eacs", "windows", "driver", "china", "bluetooth", "rtl8821cu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 8
related_product: "/ja/products/alfa/awus036eacs/"
featureimage: "/images/blog/awus036eacs-china-install-guide.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036EACSはどのチップを使っていますか？Bluetoothをサポートしていますか？"
    answer: "Realtek RTL8821CUチップを採用し、WiFi 5とBluetooth 4.2をサポートしています。"
  - question: "AWUS036EACSはLinuxでの使用に適していますか？"
    answer: "適しています。Linuxカーネル6.2以降（例：Ubuntu 24.04 HWE / kernel 6.17）には内蔵のrtw88_8821cuドライバが含まれ、コンパイル不要で挿すだけで認識します。モニターモードとパケットインジェクションは両バンド（2.4GHz / 5GHz）で100%、WPA .22000のエンドツーエンド取得も実測でき、Bluetoothも動作確認済みです。"
  - question: "AWUS036EACSのWindowsドライバーはどうインストールしますか？"
    answer: "Alfa公式サイトfiles.alfa.com.twからWindowsドライバーパッケージをダウンロードし、管理者としてインストール後に再起動するだけです。"
  - question: "AWUS036EACSのBluetoothはどう有効にしますか？"
    answer: "ドライバーインストール後に通常自動的に有効になり、Windowsの設定でBluetoothスイッチをオンにしてデバイスに接続できます。"
  - question: "Linuxで無線セキュリティリサーチ用アダプターが必要な場合、どれを選ぶべきですか？"
    answer: "AWUS036EACS自体がカーネル6.2以降でモニターモードとパケットインジェクションに対応し、Bluetoothも使えます。さらに選択肢が欲しい場合は、AWUS036ACMやAWUS036ACSもLinuxでモニターモードを完全にサポートします。自分が所有または許可されたネットワークでのみ使用してください。"
---

AWUS036EACSは、ALFAの超小型（Nano）WiFi 5 + Bluetooth 4.2 コンボアダプターです。コンパクトなワイヤレスアップグレードを必要とするWindowsユーザーに最適で、Linuxカーネル6.2以降では内蔵のrtw88_8821cuドライバが挿すだけで対応します（コンパイル不要）。このガイドでは、中国国内のソースからのWindowsへのインストール方法と、Linuxでの使い方について解説します。


{{< tldr >}}
AWUS036EACSはRTL8821CUチップを採用したWiFi 5とBluetooth 4.2搭載のミニアダプターで、Windowsインストールは簡単です。Linuxカーネル6.2以降では内蔵のrtw88_8821cuドライバが含まれるため、モニターモードとパケットインジェクションが挿すだけで動作し、Bluetoothも動作確認済みです。
{{< /tldr >}}

> **AWUS036EACSは、Linuxカーネル6.2以降で挿すだけで動作します。** カーネル6.2以降（例：Ubuntu 24.04 HWE / kernel 6.17）には内蔵のrtw88_8821cuドライバが含まれるため、コンパイルは不要です。モニターモードとパケットインジェクションは両バンド（2.4GHz / 5GHz）で100%、WPAハンドシェイクのエンドツーエンド取得（.22000）も実測でき、Bluetooth（BT）も動作確認済みです（BR/EDR・BLEともにデバイスをスキャンでき、WiFiと共存します）。自分が所有または許可されたネットワークでのみ使用してください。
>
> **運用のヒント：** これはBT+WiFiコンボカードです。モードを繰り返し切り替えるとWiFiの受信が固まることがあります（`ip link set up` が `Operation already in progress`、`iw ... set channel` が `-16 busy` を返す）。各テスト段階の前に、アダプターを抜いて別のUSBポートに挿し直すと回復します。
>
> 同シリーズのその他のLinux対応アダプター：
> - **[AWUS036ACM](/ja/blog/awus036acm-china-install-guide/)** — MT7612U インカーネルドライバ、モニターモード・VIFに完全対応
> - **[AWUS036ACS](/ja/blog/awus036acs-china-install-guide/)** — RTL8811AU、手頃な価格でモニターモードに対応

## Linuxユーザーの方へ：最初にお読みください

> **AWUS036EACSは、Linuxカーネル6.2以降で挿すだけで動作します。** カーネル6.2以降（例：Ubuntu 24.04 HWE / kernel 6.17）には内蔵のrtw88_8821cuドライバが含まれるため、コンパイルは不要です。モニターモードとパケットインジェクションは両バンド（2.4GHz / 5GHz）で100%、WPAハンドシェイクのエンドツーエンド取得（.22000）も実測でき、Bluetooth（BT）も動作確認済みです（BR/EDR・BLEともにデバイスをスキャンでき、WiFiと共存します）。自分が所有または許可されたネットワークでのみ使用してください。
>
> **運用のヒント：** これはBT+WiFiコンボカードです。モードを繰り返し切り替えるとWiFiの受信が固まることがあります（`ip link set up` が `Operation already in progress`、`iw ... set channel` が `-16 busy` を返す）。各テスト段階の前に、アダプターを抜いて別のUSBポートに挿し直すと回復します。
>
> 同シリーズのその他のLinux対応アダプター：
> - **[AWUS036ACM](/ja/blog/awus036acm-china-install-guide/)** — MT7612U インカーネルドライバ、モニターモード・VIFに完全対応
> - **[AWUS036ACS](/ja/blog/awus036acs-china-install-guide/)** — RTL8811AU、手頃な価格でモニターモードに対応

---

## Windows 10 / 11 でのセットアップ

### ステップ 1: Alfaからドライバをダウンロードする

Alfaの公式ドライバサーバーは、中国国内からもアクセス可能です：

https://files.alfa.com.tw

**AWUS036EACS** の製品フォルダに移動し、Windows用ドライバパッケージ（`.zip` または `.exe`）をダウンロードしてください。

または、以下のドキュメントページからもアクセスできます：
https://docs.alfa.com.tw/Product/AWUS036EACS/

### ステップ 2: ドライバのインストール

1. ダウンロードしたzipファイルを解凍します。
2. インストーラー（`.exe`）を右クリックし、「**管理者として実行**」を選択します。
3. 画面の指示に従って進めます。
4. 指示があった場合は、再起動を行ってください。

### ステップ 3: アダプターの確認

再起動後、**デバイスマネージャー**を開きます（Win+X キーを押し、デバイスマネージャーを選択）。

「**ネットワーク アダプター**」の下に、以下が表示されていれば成功です：

```
Realtek 8821CU Wireless LAN 802.11ac USB NIC
```

これで、2.4 GHz および 5 GHz のネットワークに接続する準備が整いました。

### ステップ 4: Wi-Fiへの接続

1. タスクバーのWi-Fiアイコンをクリックします。
2. 接続したいネットワークを選択します。
3. パスワードを入力して接続します。

---

## Bluetooth のセットアップ (Windows)

AWUS036EACSには Bluetooth 4.2 も搭載されています。ドライバのインストール後：

1. **設定 → Bluetooth とデバイス** を開きます。
2. Bluetooth を「**オン**」にします。
3. 「**デバイスの追加**」をクリックして、キーボード、マウス、ヘッドフォンなどの周辺機器をペアリングします。

---

## Linux 互換性の詳細

**カーネル6.2以降**では、RTL8821CUは内蔵の `rtw88_8821cu` モジュールで駆動されるため、コンパイルは不要です。挿すだけで認識されます。まず `uname -r` でカーネルバージョンを確認してください。

### Kali Linux

6.2以降のカーネルでは、内蔵の `rtw88_8821cu` ドライバが自動的に読み込まれます。モニターモードとパケットインジェクションを両バンド（2.4GHz / 5GHz）で100%実測し、WPAハンドシェイクのエンドツーエンド取得（.22000）も確認しました。自分が所有または許可されたネットワークでのみ使用してください。

```bash
sudo nmcli dev set wlxXXXX managed no
sudo ip link set wlxXXXX down
sudo iw dev wlxXXXX set type monitor
sudo ip link set wlxXXXX up
```

### Ubuntu 22.04 / 24.04

Ubuntu 24.04 は GA カーネル 6.8・HWE カーネル（例：kernel 6.17）のいずれにも内蔵の `rtw88_8821cu` ドライバ（カーネル6.2でmainlineに統合）が含まれ、モニターモード、パケットインジェクション、クライアント接続が挿すだけで動作します。旧カーネル（6.2未満、例：Ubuntu 22.04 の GA カーネル）の場合は、HWE カーネルに更新すると内蔵ドライバが利用できます。

### Debian / Raspberry Pi

状況は同じです。カーネルが6.2以降（ARM64ビルドを含む）であれば、内蔵の `rtw88_8821cu` ドライバがコンパイル不要でアダプターを処理します。

### 運用のヒント（BT+WiFiコンボカード）

EACSはBluetoothとWiFiを1つのチップに搭載しているため、モードを繰り返し切り替えるとWiFiの受信が固まることがあります（`ip link set up` が `Operation already in progress`、`iw ... set channel` が `-16 busy` を返す）。各テスト段階の前に、アダプターを抜いて別のUSBポートに挿し直すと状態がクリアされます。Bluetooth（BR/EDR・BLE）は動作確認済みで、WiFiと共存します。

---

## 中国国内向けリソース

| リソース | URL | 用途 |
|----------|-----|---------|
| Alfa 公式ドライバ | [files.alfa.com.tw](https://files.alfa.com.tw) | EACS Windows用ドライバ |
| Alfa ドキュメント | [docs.alfa.com.tw](https://docs.alfa.com.tw) | セットアップガイド、FAQ |
| Alfa Wiki | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 製品マニュアル |


---

{{< faq >}}

---

## 中国向け Alfa アダプターガイド（その他）

- [AWUS036ACH 中国インストールガイド](/ja/blog/awus036ach-china-install-guide/) — RTL8812AU、高出力
- [AWUS036ACM 中国インストールガイド](/ja/blog/awus036acm-china-install-guide/) — MT7612U、VIF完全対応
- [AWUS036ACS 中国インストールガイド](/ja/blog/awus036acs-china-install-guide/) — RTL8811AU、モニターモード
- [AWUS036AX 中国インストールガイド](/ja/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER 中国インストールガイド](/ja/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [AWUS036AXM 中国インストールガイド](/ja/blog/awus036axm-china-install-guide/) — MT7921AUN, L型
- [AWUS036AXML 中国インストールガイド](/ja/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- AWUS036EACS ← 現在のページ

ご不明な点がありますか？下のコメント欄に記入するか、[yupitek.com](https://yupitek.com/ja/contact/) までお問い合わせください。

---

## 参考文献

1. [ALFA Network公式ウェブサイト](https://www.alfa.com.tw/)
2. [Alfa公式ドライバーダウンロード](https://files.alfa.com.tw)
3. [Realtek公式ウェブサイト](https://www.realtek.com/)
