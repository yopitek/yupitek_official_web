---
title: "ALFA アダプター USB パススルー：VirtualBox と VMware セットアップガイド"
description: "Kali Linux 向けの VirtualBox および VMware Workstation における ALFA USB WiFi アダプターの USB パススルー設定を解説。AWUS036ACH、AWUS036AXML、USB 3.0 フィルター、Extension Pack、トラブルシューティングまで網羅。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "alfa-network", "AWUS036ACH", "AWUS036AXML"]
---

仮想マシン内で ALFA WiFi アダプターを使用するのは、接続するだけでゲスト OS が自動認識するほど単純ではありません。共有フォルダーやブリッジネットワークとは異なり、モニターモードと生パケットインジェクションには**完全な USB 制御**が必要です。つまり、VM がホストのネットワークスタック経由ではなく USB デバイスを排他的に所有する必要があります。これを USB パススルーと呼び、正しく設定することが VM 環境で作業するペネトレーションテスターや CTF プレイヤーにとって最も一般的なセットアップ失敗の原因です。

本ガイドでは、ゲスト OS として Kali Linux を対象に **VirtualBox 7.x** と **VMware Workstation 17+ / VMware Fusion 13+** の完全なパススルー設定を解説します。AWUS036ACH（RTL8812AU チップセット）と新しい AWUS036AXML（MT7921AUN チップセット）の両方を対象に、動作が異なる箇所はアダプター固有のメモとして記載しています。

設定完了後、Kali 内で `lsusb` に ALFA アダプターが表示され、適切なドライバーが読み込まれ、`airmon-ng` でモニターモードの動作が確認できます。

---

## 前提条件

開始前に、環境が以下の要件を満たしているか確認してください。特に VirtualBox Extension Pack が欠如していると、ほとんどのパススルー失敗の根本原因となります。

| 要件 | 詳細 |
|---|---|
| **ハイパーバイザー** | VirtualBox 7.x + Extension Pack **または** VMware Workstation 17+ / Fusion 13+ |
| **ゲスト OS** | Kali Linux 2024.x 以降（2024.1〜2025.1 でテスト済み） |
| **ALFA アダプター** | AWUS036ACH、AWUS036AXML、AWUS036ACM、または RTL8812AU / MT7921AUN デバイス |
| **ホスト USB ポート** | USB 3.0 推奨（特に AWUS036AXML） |
| **ホスト OS** | Windows 10/11、Linux、または macOS（Fusion） |
| **Sudo アクセス** | Kali VM 内で必要 |

{{< alert "circle-info" >}}
Kali 内にドライバーをまだインストールしていない場合は、先に本ガイドの USB パススルー手順を完了してください。VM 内でアダプターが認識された後、[ALFA ドライバーインストールガイド](/ja/blog/install-alfa-driver-kali-ubuntu/) に従って適切なドライバーをコンパイル・読み込みしてください。
{{< /alert >}}

---

## VirtualBox USB パススルー — ステップバイステップ

VirtualBox では USB 2.0 および USB 3.0 パススルーをサポートするために追加コンポーネント「**Extension Pack**」が必要です。インストールしていない場合、USB 1.1（OHCI）しか使用できず、現代の ALFA アダプターには不十分です。

### VirtualBox Extension Pack のインストール

1. [virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads) を開きます。
2. **VirtualBox Extension Pack** の下にある **All supported platforms** をクリックして `.vbox-extpack` ファイルをダウンロードします。バージョンはインストールされている VirtualBox と完全に一致している必要があります。
3. VirtualBox を開き、**ファイル → 環境設定 → 拡張機能**（macOS：**VirtualBox → 設定 → 拡張機能**）に移動します。
4. **+** アイコンをクリックし、ダウンロードした `.vbox-extpack` を参照してインストールします。ライセンスの確認が求められたら承諾します。

コマンドラインで Extension Pack が有効か確認：

```bash
VBoxManage list extpacks
```

期待される出力：

```
Extension Packs: 1
Pack no. 0:   Oracle VirtualBox Extension Pack
Version:      7.0.x
...
Usable:       true
```

{{< alert "triangle-exclamation" >}}
**Usable** フィールドが `false` の場合、Extension Pack のバージョンが VirtualBox のバージョンと一致していません。アンインストールして正しいバージョンを再インストールしてください。
{{< /alert >}}

### vboxusers グループへのユーザー追加（Linux ホストのみ）

Linux ホストでは、USB デバイスにアクセスするためにユーザーアカウントが `vboxusers` グループのメンバーである必要があります。

```bash
sudo usermod -aG vboxusers $USER && newgrp vboxusers
```

実行後、グループ変更を有効にするために**ログアウトして再ログイン**（またはリブート）してください。以下で確認できます：

```bash
groups $USER
```

出力に `vboxusers` が含まれている必要があります。

### VM 設定での USB コントローラーの有効化

1. Kali VM が実行中の場合は停止します。
2. VM を選択し、**設定 → USB** をクリックします。
3. **USB コントローラーを有効にする** にチェックを入れます。
4. ラジオボタンから **USB 3.0 (xHCI) コントローラー** を選択します。

{{< alert "circle-info" >}}
AWUS036AXML には USB 3.0（xHCI）が必要です。AWUS036ACH は USB 2.0 デバイスなので USB 2.0（EHCI）でも技術的には十分ですが、xHCI を使用しても問題なく、設定の一貫性が保たれます。
{{< /alert >}}

### USB デバイスフィルターの追加

1. 同じ **設定 → USB** パネルで **+** アイコン（デバイスから USB フィルターを追加）をクリックします。
2. ALFA アダプターがまだ接続されていない場合は今すぐ接続します。VirtualBox がドロップダウンに表示します。
3. デバイスを選択します。通常 **"Realtek 802.11ac NIC"**（AWUS036ACH）または **"MediaTek Corp. 802.11 b/g/n"**（AWUS036AXML）として表示されます。
4. **OK** をクリックして保存します。

### VM の起動と lsusb による確認

Kali VM を起動します。デスクトップが読み込まれたらターミナルを開き、以下を実行：

```bash
lsusb
```

次のような行が表示されるはずです：

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

または AWUS036AXML の場合：

```
Bus 002 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

### ドライバーの読み込み

**AWUS036ACH（RTL8812AU）：**

```bash
sudo modprobe 88XXau
```

失敗した場合（モジュールが見つからない）、先に DKMS パッケージをインストール：

```bash
sudo apt update && sudo apt install -y realtek-rtl88xxau-dkms
sudo modprobe 88XXau
```

**AWUS036AXML（MT7921AUN）：**

```bash
sudo modprobe mt7921u
```

### モニターモードの確認

```bash
sudo airmon-ng start wlan1
sudo iwconfig wlan1mon
```

**Mode** フィールドが `Monitor` と表示されるはずです。

### VirtualBox の一般的なエラー

| エラー | 原因 | 修正方法 |
|---|---|---|
| USB 設定に「利用可能な USB デバイスなし」 | Extension Pack 未インストールまたはバージョン不一致 | 一致する Extension Pack バージョンをインストール |
| アダプターがキャプチャされない / lsusb に表示されない | ユーザーが `vboxusers` グループにいない（Linux ホスト） | `sudo usermod -aG vboxusers $USER`、その後ログアウト/ログイン |
| 「USB デバイスは前のリクエストでビジー」 | ホスト上の別プロセスがデバイスを使用中 | VM 起動前にアダプターを抜き差し |
| VM 内でデバイスが切断し続ける | USB 3.0 コントローラー無効；VM が OHCI を使用 | VM 設定 → USB で USB 3.0（xHCI）に切り替え |
| フィルター追加後もデバイスが自動キャプチャされない | Extension Pack インストール前にフィルターを作成 | フィルターを削除し、Extension Pack インストール後に再追加 |

---

## VMware Workstation / VMware Fusion USB パススルー

VMware は USB パススルーを VirtualBox とは異なる方法で処理します。別途拡張機能をインストールする必要はありません。USB 2.0 および 3.0 サポートは VMware Workstation 17+ と Fusion 13+ に組み込まれています。主なメカニズムは **USB アービトレーターサービス**で、ホストの USB イベントを監視して VM にデバイスをルーティングします。

### デバイスメニューによるアダプターの接続

VM の実行中に ALFA アダプターを接続すると、VMware は通常どの VM がデバイスを所有するかを尋ねるポップアップを表示します。見逃した場合：

1. Kali VM の実行中にメニューバーの **VM → リムーバブルデバイス** に移動します。
2. リストを展開して ALFA アダプターを探します（例：**Realtek 802.11ac NIC**）。
3. **接続（ホストから切断）** をクリックします。

### VMware Fusion（macOS）

1. **仮想マシン → USB と Bluetooth** に移動します。
2. リストで ALFA アダプターを見つけます。
3. 接続を **Linux に接続**（または Kali VM の名前）に切り替えます。

### 確認とドライバーの読み込み

接続後、Kali 内部で確認：

```bash
lsusb
```

次に上記の VirtualBox セクションと同様に適切なドライバーを読み込みます。

### VMware USB アービトレーターサービスの確認

ALFA アダプターが **リムーバブルデバイス** メニューに表示されない場合、USB アービトレーターサービスが実行されていない可能性があります。Linux ホストで：

```bash
sudo systemctl status vmware-usbarbitrator
```

停止している場合：

```bash
sudo systemctl start vmware-usbarbitrator
sudo systemctl enable vmware-usbarbitrator
```

### VMware での USB 3.0 の有効化

Kali VM の `.vmx` ファイルを開き、以下を確認または追加：

```
usb_xhci.present = "TRUE"
```

{{< alert "triangle-exclamation" >}}
USB 3.0（xHCI）サポートには VMware ハードウェアバージョン 14 以降が必要です。VM が古いハードウェアバージョンで作成されている場合は、**VM → 管理 → ハードウェア互換性の変更** でアップグレードしてください。
{{< /alert >}}

### VMware の一般的なエラー

| エラー | 原因 | 修正方法 |
|---|---|---|
| リムーバブルデバイスメニューにアダプターが表示されない | USB アービトレーターが未実行 | `vmware-usbarbitrator` サービスを起動 |
| デバイスが接続後すぐに切断する | ホスト OS ドライバーがデバイスを取り戻す | ホストのアダプター WiFi ドライバーを無効化、または素早く再接続 |
| 「デバイスはホストが使用中」 | ホスト OS がデバイスを要求済み | VM で接続する前にホストから取り外し |
| VM 内で USB 3.0 速度が出ない | VM ハードウェアバージョン < 14 または xHCI 無効 | ハードウェアバージョンをアップグレード、.vmx に `usb_xhci.present = "TRUE"` を追加 |
| パススルー後もモニターモードが失敗 | Kali 内のドライバーが誤りまたは欠如 | [ドライバーインストールガイド](/ja/blog/install-alfa-driver-kali-ubuntu/) に従う |

---

## アダプター固有のメモ

### AWUS036ACH（RTL8812AU）

AWUS036ACH は **USB 2.0** デバイスで、VM 環境で最も十分にテストされているアダプターの一つです。VirtualBox と VMware の両方で安定して動作します。ドライバーパッケージ：`realtek-rtl88xxau-dkms`。モジュール名：`88XXau`。

### AWUS036AXML（MT7921AUN）

AWUS036AXML は WiFi 6E をサポートする **USB 3.0** デバイスで、VM 環境でいくつかの特有の問題があります。USB 3.0（xHCI）コントローラーを**必ず**使用してください。ファームウェアパッケージ：`firmware-misc-nonfree`。初期ロットの一部では VirtualBox USB 3.0 アービトレーションで定期的なフリーズが発生することがあります。VMware Workstation は VirtualBox よりも AWUS036AXML の USB 3.0 パススルーを安定して処理する傾向があります。

完全なレビュー：[AWUS036AXML WiFi 6E レビュー](/ja/blog/awus036axml-wifi-6e-review/)。

### AWUS036ACM（RTL8812AU、シングルアンテナ）

ドライバーとパススルーの観点から AWUS036ACH と同じ動作をします。同じ `88XXau` モジュールと同じ VirtualBox/VMware 設定を使用します。

---

## パフォーマンスのヒント

**ホストの USB オートサスペンドを無効化：**

```bash
echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend
```

**VM に十分なリソースを割り当て：**
- **CPU コア 2 個以上**（4 個推奨）
- **RAM 2 GB 以上**（GUI 付き Kali の場合は 4 GB 推奨）

**ペンテスト作業前に VM スナップショットを取得。**

{{< alert "circle-info" >}}
30 分を超えるキャプチャセッションでは、アダプターとホスト間にセルフパワードの USB ハブの使用を検討してください。安定した電源を提供し、重要なキャプチャ中に電圧降下によりアダプターが切断されるのを防ぎます。
{{< /alert >}}

---

## ベアメタル vs VM：正直な比較

| 機能 | ベアメタル Kali | VirtualBox + Kali | VMware + Kali |
|---|---|---|---|
| **ドライバーサポート** | 完全、直接 | 良好（Extension Pack 必要） | 良好（USB 内蔵） |
| **モニターモードの安定性** | 優秀 | 良好 | 良好〜優秀 |
| **パケットインジェクションの信頼性** | 優秀 | 良好（ときどきフレームロス） | 良好〜優秀 |
| **セットアップ時間** | 高（専用ハードウェア） | 低〜中 | 低〜中 |
| **可搬性** | 低 | 高（スナップショット） | 高 |
| **CTF / ラボ使用** | 過剰 | 最適 | 最適 |
| **プロフェッショナルなペンテスト** | 推奨 | 許容 | 許容 |

---

## トラブルシューティングクイックリファレンス

| 症状 | 最も可能性の高い原因 | 解決策 |
|---|---|---|
| Kali 内の `lsusb` に何も表示されない | USB パススルーが未設定 | USB フィルターを追加（VBox）またはリムーバブルデバイス経由で接続（VMware） |
| VirtualBox USB 設定に「USB デバイスなし」 | Extension Pack が欠如またはバージョン不一致 | 一致する Extension Pack をインストール |
| `lsusb` でアダプターは見えるが `wlan` インターフェースなし | ドライバー未読み込み | `sudo modprobe 88XXau` または `sudo modprobe mt7921u` |
| `modprobe: FATAL: Module 88XXau not found` | DKMS パッケージ未インストール | `sudo apt install realtek-rtl88xxau-dkms` |
| インターフェースが現れては消える | USB オートサスペンドまたは VBox xHCI アービトレーション | オートサスペンドを無効化；ACH には USB 2.0 コントローラーを試す |
| `airmon-ng` 起動するがモニターモードがサイレントに失敗 | 誤ったドライバーまたはネットワークマネージャーの競合 | `sudo airmon-ng check kill` してから再試行 |
| VirtualBox USB フィルターが起動時に自動キャプチャしない | Extension Pack インストール前にフィルターを追加 | フィルターを削除、Extension Pack インストール後に再追加 |
| VMware が長いセッション中にデバイスを失う | VMware USB アービトレーターサービスが停止 | 再有効化して自動起動に設定 |

---

## 次のステップ

- **ドライバーのインストールまたは更新：** [Kali と Ubuntu 向け ALFA ドライバーインストールガイド](/ja/blog/install-alfa-driver-kali-ubuntu/)
- **AWUS036ACH の完全セットアップ：** [AWUS036ACH Kali Linux セットアップガイド](/ja/blog/awus036ach-kali-linux-setup/)
- **AWUS036AXML のハードウェアレビュー：** [AWUS036AXML WiFi 6E レビュー](/ja/blog/awus036axml-wifi-6e-review/)
