---
title: "カーネル更新後にALFAドライバーが壊れた？完全修復ガイド"
description: "Linuxカーネル更新後にALFA USB WiFiアダプターが動作しなくなった？Kali LinuxとUbuntuでのRTL8812AU、RTL8811AU、MT7921AUドライバーの完全修復ガイド。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-driver", "kernel-update", "rtl8812au", "kali-linux", "ubuntu", "dkms", "troubleshooting"]
---

`sudo apt upgrade` を実行して再起動したら、ALFAアダプターが消えてしまいました——インターフェースなし、ランプなし、何もなし。これはLinuxでALFA Network USB WiFiアダプターを使うユーザーから最もよく寄せられるサポートの質問であり、カーネルの更新がほぼ常に原因です。このガイドでは、最も影響を受ける2つのチップセットファミリーの体系的な診断と修復手順を説明します：**RTL8812AU**（AWUS036ACH、ACM、ACS搭載）と **MT7921AU**（AWUS036AXM、AXML、AX搭載）。各セクションの手順に従えば、15分以内にアダプターが復旧します。

---

## カーネル更新がドライバーを壊す理由

Linux WiFiドライバーには2つの種類があります：カーネルのソースツリーに含まれる**カーネル内**ドライバーと、その外部に存在する**ツリー外**ドライバーです。どちらのタイプを使用しているかを理解することで、更新が問題を引き起こす理由が明確になります。

### ツリー外ドライバーとDKMS

RTL8812AUチップセットはコミュニティが管理するツリー外ドライバー（最も一般的なのは `aircrack-ng/rtl8812au` フォーク）を使用します。公式カーネルソースの一部ではないため、**現在実行中のカーネルのヘッダーに対してコンパイルする**必要があります。カーネルバージョンが変わるたびに——`6.6.15` → `6.6.20` のようなマイナーなパッチリリースでさえ——コンパイル済みモジュールは互換性がなくなり、カーネルはロードを拒否します。

**DKMS（Dynamic Kernel Module Support：動的カーネルモジュールサポート）** が標準的な解決策です。DKMSはドライバーのソースコードをシステムレベルのフックに登録し、新しいカーネルパッケージがインストールされるたびにモジュールを自動的に再コンパイルします。DKMSが正しく設定されていれば、カーネルの更新は透明になります：新しいカーネルで再起動すると、アダプターはすでに動作しています。

DKMSが静かに失敗する原因は2つあります：

1. **カーネルヘッダーの欠如** — コンパイラは新しいカーネルのインストール時に `linux-headers-$(uname -r)` がインストールされている必要があります。ヘッダーがカーネルの後に届いた場合、DKMSはビルドの機会を逃します。
2. **古い `dkms.conf`** — インストール済みドライバーバージョンの設定ファイルがソースツリーと一致しない場合、ビルドは不明確なエラーで失敗します。

### カーネル内ドライバー（MT7921U）

MT7921Uチップセットはカーネル **5.18** 以降、メインラインカーネルに含まれています。つまり、コンパイル手順は不要です——カーネルはすでにハードウェアと通信する方法を知っています。ただし、ドライバーは別のパッケージが提供する**ファームウェアバイナリ**（`mt7921u.bin`）に依存しています。そのパッケージが欠落している場合、またはカーネルの更新が期待されるファームウェアAPIを変更した場合、アダプターはロードされているように見えても、どのネットワークにも接続できない場合があります。

### クイック診断コマンド

何かを変更する前に、現在の状況を把握するためにこの2つのコマンドを実行してください：

```bash
# 現在実行中のカーネルは何か？
uname -r

# どのDKMSモジュールがビルドされているか（どのカーネル向けか）？
sudo dkms status
```

`dkms status` がRTL8812AUドライバーが現在のカーネルではなく、*古い*カーネル向けにビルドされていることを示している場合、問題が見つかりました。

---

## ステップ1：ドライバーを診断する

この診断手順を上から順に実行してください。各チェックにより、変更を開始する前に根本原因を絞り込めます。

```bash
# 現在のカーネルを確認
uname -r

# ワイヤレスインターフェースが存在するか確認
ip link show | grep -E "wlan|wlp"

# ドライバーモジュールが現在ロードされているか確認
lsmod | grep -E "88XXau|rtl8812au|mt7921u"

# RTL8812AUアダプターのDKMSビルドステータスを確認
sudo dkms status

# 関連するエラーメッセージのカーネルリングバッファをスキャン
sudo dmesg | grep -E "ALFA|rtl8812|mt7921" | tail -20
```

**結果の解釈：**

| 出力 | 意味 |
|---|---|
| `ip link` がワイヤレスを返さない | カーネルモジュールがロードされていないか、ハードウェアが列挙されていない |
| `lsmod` に一致するモジュールが表示されない | モジュールのロードに失敗——エラーの `dmesg` を確認 |
| `dkms status` が現在のカーネルに `broken` または欠落を表示 | DKMSビルドが失敗——RTL8812AU修復手順に従う |
| `dmesg` が `firmware: failed to load mt7921u` を表示 | ファームウェアパッケージが欠落——MT7921U修復手順に従う |
| `dmesg` が `disagrees about version of symbol` を表示 | モジュールが間違ったカーネルヘッダーに対してビルドされている |

{{< alert "triangle-exclamation" >}}
`ip link` がインターフェースを表示しているが、使用しようとすると消える場合は、アダプター固有のトラブルシューティング表に進んでください。表示はされるが機能しないインターフェースと、完全に消えたインターフェースとでは原因が異なります。
{{< /alert >}}

---

## 修復：RTL8812AUドライバー（AWUS036ACH、ACM、ACS、EACS）

RTL8812AUは、デュアルバンドサポートと信頼性の高いモニターモードにより、ペネトレーションテストで最も広く使われているALFAチップセットです。ツリー外ドライバーが必要なため、カーネルの更新で最も頻繁に壊れるチップセットでもあります。

### 4.1 — カーネルヘッダーをインストール

ドライバーに触れる前に、まず*現在の*カーネルのヘッダーがインストールされていることを確認します：

```bash
sudo apt update
sudo apt install linux-headers-$(uname -r)
```

このコマンドが正常に終了すれば、ヘッダーが存在し、DKMSの再ビルドを続行できます。パッケージが見つからないと報告された場合、カーネルが現在のリポジトリスナップショットには新しすぎる可能性があります——まず `sudo apt full-upgrade` を実行して一致するヘッダーを取得し、続行する前に再起動してください。

### 4.2 — DKMSで再ビルド（最速の方法）

ヘッダーが揃ったら、DKMSに現在実行中のカーネル向けに登録されているすべてのモジュールを再ビルドするよう依頼します：

```bash
sudo dkms autoinstall
```

出力を注意深く確認してください。成功したビルドは `DKMS: install completed` で終わります。成功した場合は、再起動せずにモジュールをリロードします：

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

インターフェースが表示されれば完了です。ステップ4.4でモニターモードを確認してください。

### 4.3 — ソースから完全再インストール（DKMSが失敗した場合）

`dkms autoinstall` がエラーを報告した場合、登録されているドライバーソースが破損しているか古くなっています。完全に削除して、最新のアップストリームソースから再インストールします：

```bash
# ドライバーのすべてのDKMS登録バージョンを削除
sudo dkms remove rtl8812au/5.6.4.2 --all 2>/dev/null

# 最新のドライバーソースをクローン
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# DKMSにソースを登録し、コンパイルして一括インストール
sudo make dkms_install
```

{{< alert "triangle-exclamation" >}}
`dkms remove` コマンドのバージョン番号 `5.6.4.2` はよく見られるリリースですが、あなたのバージョンが異なる場合があります。まず `sudo dkms status` を実行して、出力に表示される正確なバージョン文字列を使用してください。
{{< /alert >}}

ビルドが完了したら：

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

### 4.4 — モニターモードを確認

アダプターは物理的に存在し、ドライバーがロードされています。セキュリティテストにこのアダプターを使う理由であるモニターモードがまだ機能することを確認します：

```bash
sudo airmon-ng start wlan0
```

`wlan0` は `ip link` に表示される実際のインターフェース名に置き換えてください。成功すれば `monitor mode vif enabled` と表示され、`wlan0mon` のような新しいインターフェース名が現れます。

### 4.5 — Kaliパッケージ方式（最も簡単）

Kali LinuxにはRTL8812AUドライバーの事前パッケージ化されたDKMSビルドが付属しており、Kaliカーネルと同期を保ちます。Kaliを使用している場合は、GitHubからクローンする代わりにこの方法を使用してください：

```bash
sudo apt update && sudo apt install realtek-rtl88xxau-dkms
```

このコマンド1つで、ドライバーソースのインストール、DKMSへの登録、現在のカーネル向けのビルドが完了します。今後の `apt full-upgrade` 実行時にヘッダーとドライバーが自動的に同期されます。

---

## 修復：MT7921Uドライバー（AWUS036AX、AXM、AXML、AXER）

MT7921U（Wi-Fi 6E）チップセットはまったく異なるアプローチを取ります。Linux 5.18以降は**カーネル内ドライバー**なので、DKMS不要、コンパイル不要、GitHubクローン不要です。カーネルの更新で壊れることはないはずですが、ファームウェアのパッケージ問題が影響することがあります。

### 5.1 — ファームウェアパッケージをインストール

カーネルモジュール（`mt7921u.ko`）はすでに存在しますが、ハードウェアを初期化するためにユーザー空間からのファームウェアバイナリが必要です：

```bash
sudo apt install firmware-misc-nonfree
```

Ubuntuでは、このパッケージは `non-free` リポジトリコンポーネントにあります。コマンドが失敗した場合は、`/etc/apt/sources.list` でnon-freeソースが有効になっていることを確認してください。

### 5.2 — ドライバーをリロード

ファームウェアのインストール後、再起動せずにドライバーを強制リロードします：

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
```

次にインターフェースを確認します：

```bash
ip link show | grep -E "wlan|wlp"
```

### 5.3 — カーネルバージョンを確認

MT7921Uドライバーにはカーネル **5.18以降**が必要です。このカーネルバージョン以前に公開された最小限のKaliまたはUbuntuイメージをインストールした場合、モジュール自体が存在しません：

```bash
uname -r
# 出力は5.18.x以上でなければならない
```

カーネルが5.18より古い場合は、カーネルをアップグレードしてください（ステップ5.4）。

### 5.4 — カーネルをアップグレード

```bash
sudo apt update && sudo apt full-upgrade && sudo reboot
```

{{< alert "triangle-exclamation" >}}
`upgrade` ではなく `full-upgrade` を使用してください。`upgrade` サブコマンドは他のパッケージの削除が必要なパッケージを保留します——これはしばしばカーネルパッケージ自体が保留されることを意味します。`full-upgrade` は必要な依存関係の解決を許可します。
{{< /alert >}}

### 5.5 — 再起動後に確認

新しいカーネルで再起動したら、すべてが正常に動作していることを確認します：

```bash
sudo modprobe mt7921u
ip link show
sudo dmesg | grep mt7921 | tail -10
```

正常な `dmesg` 出力には、ファームウェアが正常にロードされ、USBデバイスがネットワークインターフェースとして登録されていることが表示されます。

---

## 将来の更新後もドライバーを維持する

予防は修復より簡単です。これらの方法でカーネルの更新がアダプターを再び壊すことを防ぎます。

**Kali rollingでは常に `full-upgrade` を使用：**

```bash
sudo apt update && sudo apt full-upgrade
```

`full-upgrade` コマンドは、新しいカーネルパッケージがインストールされるとき、一致する `linux-headers` パッケージが*同じトランザクション*でインストールされることを保証します。DKMSフックはパッケージのインストール中に起動します——ヘッダーが後の `apt` 実行でカーネルの後に届いた場合、DKMSはビルドを逃します。

**DKMSメタパッケージをインストール：**

```bash
sudo apt install dkms linux-headers-generic
```

これにより `linux-headers-generic` がDKMSパッケージの依存関係として引き込まれ、ヘッダーは常にカーネルと同期して最新の状態を保ちます。

**Ubuntu HWEカーネルスタック：**

Ubuntu LTSでは、ハードウェアイネーブルメントカーネルスタックはGAカーネルよりも頻繁に更新され、ハードウェアサポートも優れています。一度インストールすれば、更新は自動的に処理されます：

```bash
sudo apt install linux-generic-hwe-24.04
```

**DKMS自動インストールが有効であることを確認：**

```bash
cat /etc/dkms/framework.conf | grep autoinstall
```

この行がコメントアウトされているか `no` に設定されている場合、DKMSはモジュールを自動的に再ビルドしません。`/etc/dkms/framework.conf` でコメントを外すか `yes` に設定してください。

---

## アダプター固有のトラブルシューティング表

| 症状 | 可能性のあるチップセット | 根本原因 | クイックフィックス |
|---|---|---|---|
| 再起動後にインターフェースが消える | RTL8812AU | DKMSビルドが失敗 | `sudo dkms autoinstall` |
| インターフェースが消え、`dmesg` がファームウェアエラーを表示 | MT7921AU | ファームウェアパッケージが欠落 | `sudo apt install firmware-misc-nonfree` |
| インターフェースが表示されるが30秒後に消える | RTL8812AU | モジュールのバージョン不一致 | `sudo dkms remove --all && sudo make dkms_install` |
| `SIOCSIFFLAGS` でモニターモードが失敗 | RTL8812AU | ドライバーブランチが間違っている | `aircrack-ng/rtl8812au` をクローンして再インストール |
| `iwconfig` がワイヤレス拡張なしを表示 | どれでも | モジュールがロードされていない | `sudo modprobe 88XXau` または `sudo modprobe mt7921u` |
| インターフェースはあるがネットワークが見つからない | MT7921AU | カーネル < 5.18 | `sudo apt full-upgrade && sudo reboot` |
| `dkms status` が `broken` を表示 | RTL8812AU | ソース/ヘッダーの不一致 | `sudo apt install linux-headers-$(uname -r)` 後に再ビルド |
| TX出力が20 dBmに制限 | RTL8812AU | 規制ドメインロック | `sudo iw reg set US`（地域に合わせて調整） |

---

## 何も効かない場合：フレッシュインストール方法

複数の再ビルド試行が失敗し、`dkms status` が複数の部分インストールからの混乱した出力を表示している場合、デバッグよりも白紙から始める方が早いです：

```bash
# Kaliパッケージがインストールされていた場合はまず削除
sudo apt purge realtek-rtl88xxau-dkms

# rtl8812auのすべてのDKMSエントリを削除
for ver in $(sudo dkms status | grep rtl8812au | awk -F'[,/]' '{print $2}' | tr -d ' '); do
    sudo dkms remove rtl8812au/$ver --all
done

# 残っているソースディレクトリがあれば削除
sudo rm -rf /usr/src/rtl8812au*

# 古くなったモジュールキャッシュをクリア
sudo depmod -a

# フレッシュクローンとインストール
git clone https://github.com/aircrack-ng/rtl8812au.git /tmp/rtl8812au
cd /tmp/rtl8812au
sudo make dkms_install
sudo modprobe 88XXau
ip link show | grep wlan
```

{{< alert "triangle-exclamation" >}}
DKMSエントリを削除するループはバージョンが見つからない場合に静かに失敗します——それは問題ありません。重要なステップは `sudo rm -rf /usr/src/rtl8812au*` で、これにより壊れた状態になっている可能性のあるソースツリーが削除されます。
{{< /alert >}}

---

## 予防チェックリスト

システム更新のたびにこのチェックリストを使用して、作業中の予期せぬ問題を避けてください：

**`apt upgrade` の前に：**

```bash
# どのカーネルパッケージが保留中かを確認
apt list --upgradable 2>/dev/null | grep linux-image
```

新しいカーネルが来る場合は、本番作業の前にテスト再起動を計画してください。

**すべてのアップグレードと再起動後に：**

```bash
# アダプターが戻ったことを確認
ip link show | grep -E "wlan|wlp"

# モニターモードがまだ機能することを確認
sudo airmon-ng check
```

**フォールバックを維持：**
- Kali Liveイメージ（または既知の動作するドライバーを持つ2番目のアダプター）の入ったUSBドライブを用意してください。予定されたエンゲージメント中の接続の問題はコストがかかります——物理的なフォールバックは数分で準備でき、いざというときに救ってくれます。

**Kaliで重要なドライバーパッケージをピン留め：**

```bash
# アップグレード中に特定のドライバーパッケージが自動削除されるのを防ぐ
sudo apt-mark hold realtek-rtl88xxau-dkms
```

ドライバーを明示的にアップグレードする前にホールドを解除：

```bash
sudo apt-mark unhold realtek-rtl88xxau-dkms && sudo apt upgrade realtek-rtl88xxau-dkms
```

---

## まとめ

カーネル更新後のALFAドライバーの失敗は予測可能なパターンに従い、予測可能な解決策があります。RTL8812AUアダプターには `dkms autoinstall`（または `aircrack-ng/rtl8812au` からのフレッシュクローン）と一致するカーネルヘッダーが必要です。MT7921Uアダプターには `firmware-misc-nonfree` とカーネル5.18以降が必要です。どちらの場合も、長期的な解決策は標準的な更新コマンドとして `apt upgrade` ではなく `apt full-upgrade` を使用し、ヘッダーとカーネルを同期させることです。

---

**関連ガイド：**
- [Kali Linux & UbuntuでALFA USB WiFiドライバーをインストールする方法](/ja/blog/install-alfa-driver-kali-ubuntu/) — ドライバーを一度もインストールしたことがない場合はここから始めてください
- [AWUS036ACH Kali Linuxセットアップガイド](/ja/blog/awus036ach-kali-linux-setup/) — モニターモードとパケットインジェクション確認を含む完全なセットアップウォークスルー
