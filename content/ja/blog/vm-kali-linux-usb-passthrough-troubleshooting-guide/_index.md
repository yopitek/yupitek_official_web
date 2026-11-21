---
title: "仮想マシンの Kali Linux が外付け USB アダプターを認識しない？VirtualBox/VMware の USB パススルー診断マニュアル"
description: "VirtualBox Extension Pack、USB 3.0 (xHCI) コントローラー、vboxusers グループ、VMware の USB アービトレーション、lsusb→iwconfig→dmesg の診断手順、FAQ をまとめた標準的な USB パススルー排障マニュアルです。"
date: 2026-08-31
author: benny-lai
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "wireless-adapter", "virtual-machine"]
featureimage: /images/blog/vm-kali-linux-usb-passthrough-troubleshooting-guide.webp
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
faq:
  - question: "USB ポートを変えたら lsusb で表示されなくなりました。アダプターの故障でしょうか？"
    answer: "故障とは限りません。まず「充電専用」ポートに挿していないか、ホストが省電力のためにデバイスをスリープさせていないかを確認してください。マザーボード背面の通常の USB ポートに挿し直すか、一度抜いて挿し直せば、多くの場合は復旧します。"
  - question: "VM ウィンドウ右下の USB アイコンが空です。どうすればよいですか？"
    answer: "次の順に確認してください：① Extension Pack のバージョンが VirtualBox と完全に一致しているか；② Linux ホストで vboxusers グループに所属しているか（再ログインが必要です）；③ ホスト側の lsusb でアダプターがまだ認識されているか；④ 他のソフトウェア（ホスト側のドライバーツールなど）がデバイスを占有していないか。"
  - question: "USB フィルターを設定したら、ホスト側でアダプターが使えなくなりました。正常ですか？"
    answer: "正常です。Guest にパススルーすると、デバイスの制御権は Guest 側に移り、ホスト側では同時に使用できません。ホストで他の作業に使いたい場合は、VM ウィンドウの USB アイコンから「リリース（release）」してホストに戻してください。"
  - question: "Guest 内の lsusb では認識されるのに wlan インターフェースがありません。どのドライバーを入れればよいですか？"
    answer: "チップセットによります：AWUS036AXML（MediaTek MT7921AUN）はカーネル内蔵の mt7921u ドライバーを使用し、Kernel 5.18+ ならプラグアンドプレイで動作します。まず apt install linux-firmware が更新されているか確認してください。AWUS036ACH（Realtek RTL8812AU）はカーネル外（out-of-tree）ドライバーのため、コミュニティ保守の aircrack-ng/rtl8812au をインストールし、DKMS でコンパイルする必要があります（Secure Boot の MOK 署名にも対応してください。Secure Boot は無効にしないでください）。"
  - question: "USB 3.0 コントローラーを選んだら、Guest が起動できなくなりました。なぜですか？"
    answer: "一部の古い Guest カーネルは xHCI のサポートが不十分です。Kali が古いバージョンの場合は、「シャットダウン → USB 2.0 (EHCI) Controller に戻す → 起動 → カーネルをアップグレード → USB 3.0 に戻す」の順でお試しください。Kali はできるだけ最新版を維持してください。xHCI のサポートがより完全になります。"
  - question: "アダプターは実機では速いのに、仮想マシン内では遅くなります。正常ですか？"
    answer: "正常です。仮想マシン内のアダプター性能は「USB エミュレーション層を経由した転送」とほぼ同等で、実機に直接挿した場合より多少のオーバーヘッドが加わります。正しい USB 3.0 (xHCI) コントローラーと新しい Hypervisor を使えば、そのオーバーヘッドを最小限に抑えられます。性能が著しく低下する場合は、まずコントローラーが USB 1.1 のままになっていないか確認してください。"
---

> <strong>対応プラットフォーム</strong>：Windows / Linux / macOS ホスト + Oracle VirtualBox / VMware Workstation 仮想マシン（Guest = Kali Linux / Debian / Ubuntu）
> <strong>対象ハードウェア</strong>：ALFA AWUS036ACH（Realtek RTL8812AU）/ ALFA AWUS036AXML（MediaTek MT7921AUN）
> <strong>本記事の位置づけ</strong>：「USB パススルー（USB Pass-through）」の排障診断を標準化したマニュアルです。macOS ホストの USB パススルー制限については第 5 章をご覧ください。

---

{{< tldr >}}

Kali ユーザーの多くは、アダプターをホストに挿しているのに、仮想マシン内でワイヤレスインターフェースが見えないという状況に遭遇します。<strong>このようなケースの多くは、次の 3 つの非常によくある原因によるもので、アダプター自体の故障である可能性は低いです。</strong>

1. <strong>VirtualBox に拡張パック（Extension Pack）がインストールされていない</strong>：これがないと、Guest は USB 2.0/3.0 コントローラーすら利用できません（USB 1.1 の転送速度は最大 12 Mbps で、アダプターにはまったく不十分です）。
2. <strong>USB パススルー設定が行われていない</strong>：ホストは既定ですべての USB デバイスを「占有」します。Guest 側で手動でマウントするか、「USB フィルター（VM USB Filter）」を設定してアダプターを自動的に引き継ぐ必要があります。
3. <strong>Guest 内のドライバーが読み込まれていない</strong>：USB 層は通過しています（`lsusb` では認識されます）が、Linux に対応するドライバーがないため、`ip link` に `wlan` インターフェースが表示されません。

排障の順序は、まずホスト側のハードウェア、次に Guest 側のパススルー、最後にドライバー層です。完全な診断の手順は 1.3 をご覧ください。

{{< /tldr >}}

---

## 1. なぜ仮想マシンは既定でホストのワイヤレスアダプターを使えないのか？

### 1.1 USB アダプターは「同時に」1 つの OS にしか属さない

USB は<strong>シングルホスト（single host）</strong>アーキテクチャで動作します。1 つの USB デバイスは、同時に 1 つの「USB ホストコントローラー（Host Controller）」にしか制御されません。アダプターをホストに挿すと、デバイスはまず<strong>ホスト OS（Host OS）</strong>に列挙（enumerate）されて引き継がれます。ホストのドライバーがそれを認識し、制御します。

仮想マシン（Guest VM）は USB バスに挿された物理デバイスではなく、ホスト内でハイパーバイザー（Hypervisor）が演じる「仮想ハードウェア」にすぎません。そのため Guest が USB アダプターを使うには、<strong>ホストがデバイスを Guest に積極的に「引き渡す」必要があります</strong>——この仕組みを <strong>USB パススルー（USB Pass-through / USB Redirection）</strong> と呼びます。

### 1.2 USB パススルーは何を通過させるのか？

VirtualBox を例にすると、パススルーの流れは次のとおりです：

```
物理 USB アダプター (AWUS036ACH / AWUS036AXML)
       │  ホストの物理 USB ポートに挿す
       ▼
ホスト OS (Host OS) の USB ホストコントローラー
       │  Hypervisor (VirtualBox) がインターセプトしてリダイレクト
       ▼
仮想 USB ホストコントローラー (エミュレートされた EHCI / xHCI)
       │  Guest (Kali) には"自分に挿さっている"ように見える
       ▼
Kali の USB ドライバー → ワイヤレスドライバー → wlan インターフェース
```

パススルーが成功すると、このデバイスの<strong>ホスト側の制御権は Guest に移り</strong>、ホストからは「抜かれた」ように見えて使用できなくなります。代わりに Guest 内では新しい USB デバイスとして認識されます。<strong>これは正常な動作であり、バグではありません。</strong> ホストの 1 つの USB デバイスを両方で同時に使うことはできません。

### 1.3 「認識されない」には実は 3 つの層がある

| 層 | 確認ツール | 症状 | 意味 |
|----|-----------|------|------|
| <strong>USB パススルー層</strong> | Guest 内の `lsusb` | `lsusb` でアダプターの VID:PID がまったく見えない | パススルー失敗（Extension Pack / コントローラー / フィルターの問題） |
| <strong>ドライバー層</strong> | Guest 内の `dmesg` | `lsusb` では見えるが、`dmesg` にエラーがある（ファームウェア不足、`Required key not available` など） | Guest 内にドライバーがない、またはモジュールの読み込みに失敗 |
| <strong>ワイヤレスインターフェース層</strong> | Guest 内の `iwconfig` / `ip link` | `lsusb` と `dmesg` は正常なのに `wlan` インターフェースがない | ドライバーは読み込まれたがインターフェースが登録されていない、またはモード／設定の問題 |

> <strong>判断の手順</strong>：まず `lsusb` で「デバイスが Guest にパススルーされたか」を確認し、次に `ip link` で「ドライバーが認識しているか」を確認します。<strong>最初からアダプターの故障を疑わないでください。</strong>

---

## 2. VirtualBox：まず Extension Pack をインストールし、次に USB 3.0 コントローラーを設定する

### 2.1 拡張パック（Extension Pack）は必須です

VirtualBox の基本パッケージは<strong>USB 1.1（OHCI）コントローラーのエミュレーションのみ</strong>を内蔵しており、USB 1.1 の転送速度ではアダプターにまったく不十分です。<strong>USB 2.0（EHCI）と USB 3.0（xHCI）コントローラーは、Oracle 公式の「拡張パック（Extension Pack）」がなければ利用できません。</strong>

Extension Pack がない場合の症状は典型的です：Guest の設定で USB 2.0 / USB 3.0 コントローラーを選択できない、またはアダプターをマウントすると「仮想マシンへのデバイス接続に失敗しました（error code E_FAIL / VERR_PDM_NO_USB_PORTS）」と表示されます。

### 2.2 バージョンは「完全に」一致させる必要があります

Extension Pack のバージョンは<strong>VirtualBox 本体のバージョンと完全に一致させる必要があります</strong>（例：VirtualBox 7.0.20 には 7.0.20 の Extension Pack が必要です）。マイナーバージョンが 1 つでも違うと、インストールや読み込みに失敗する可能性があります。

```bash
# 現在の VirtualBox バージョンを確認
vboxmanage --version
```

Oracle 公式ダウンロードページ（https://www.virtualbox.org/wiki/Downloads）から対応バージョンの
`Oracle_VM_VirtualBox_Extension_Pack-<バージョン>.vbox-extpack` をダウンロードし、次の手順を実行します：

```bash
# 方法 1: GUI インストール (VirtualBox 本体 → ファイル → ツール → Extension Pack Manager → インストール)
# 方法 2: コマンドラインでインストール
sudo VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-*.vbox-extpack

# インストール済みか確認
VBoxManage list extpacks
```

> インストール時には Oracle のライセンス（Personal Use and Evaluation License）が表示されます。個人利用は無料ですが、商用環境ではライセンスの内容に従ってください。

### 2.3 Linux ホスト：vboxusers グループに自分を追加する

Linux ホストでは、VirtualBox が USB デバイスにアクセスするために、<strong>ユーザーが `vboxusers` グループに属している必要があります</strong>。拡張パックをインストールしても失敗する多くのケースは、この権限が原因です。

```bash
# グループに追加 (<user> は自分のユーザー名に置き換えてください)
sudo usermod -aG vboxusers $USER

# ログアウトして再ログイン (または再起動) してグループを有効化; 確認する
id $USER
```

### 2.4 USB 3.0（xHCI）コントローラーを設定する

1. Kali 仮想マシンを選択 → <strong>設定（Settings）→ ポート（Ports）→ USB</strong>。
2. 「Enable USB Controller」にチェックを入れ、<strong>USB 3.0 (xHCI) Controller</strong> を選択します。
   - AWUS036AXML は USB 3.2 Gen 1（USB-C）仕様です。<strong>必ず USB 3.0 (xHCI) を選択してください</strong>。USB 2.0 を選ぶと転送速度が制限されます。
   - AWUS036ACH は USB Type-A インターフェースで、USB 2.0 と USB 3.0 のどちらのコントローラーでも使用できます。より良い転送速度を得るには、こちらも USB 3.0 (xHCI) を選択してください。
3. コントローラーを変更したら、<strong>シャットダウンしてから起動</strong>してください（Guest 内で reboot を実行するのではありません）。変更を反映するために必要です。

### 2.5 手動マウントと VMware との対比

Kali 仮想マシンを起動したら、ウィンドウ<strong>右下の USB アイコン</strong>（USB プラグの形）に注目してください：

1. USB アイコンをクリックすると、現在ホストに挿されている USB デバイスの一覧が表示されます。
2. アダプターは `Realtek 802.11ac NIC`（ACH）や `ALFA AWUS036AXML` / MediaTek（AXML）のように表示されるはずです。
3. クリックすると、デバイスが Kali に「引き渡され」ます。

一覧が空の場合は、パススルー層に問題があります。2.2 / 2.3 / 2.4 に戻って確認するか（USB コントローラーが有効になっていない場合も含む）、第 6 章の排障ワークシートを実行してください。

<strong>VMware との対比</strong>：VMware Workstation / Fusion は<strong>追加の拡張パックなしで</strong> USB パススルー機能を利用できますが、よくある確認ポイントが 2 つあります：

1. <strong>ホスト側サービス</strong>：Linux ホストでは `vmware-usbarbitrator`（USB アービトレーションサービス）が動作しているか確認してください：
   ```bash
   sudo systemctl status vmware-usbarbitrator
   # 動作していない場合は起動し, 起動時に自動実行するよう設定
   sudo systemctl enable --now vmware-usbarbitrator
   ```
2. <strong>仮想マシン設定</strong>：仮想マシン設定 → USB Controller → <strong>USB 3.1（または USB 3.0）</strong> にチェックを入れます。
3. <strong>手動接続</strong>：VMware ウィンドウのメニュー → <strong>リムーバブルデバイス（Removable Devices）→ アダプター → 接続（Connect）</strong>。

> <strong>対比のポイント</strong>：VirtualBox は「拡張パック未インストール」で詰まります。VMware は「アービトレーションサービスが動作していない」または「USB 3.0 コントローラーがオフ」で詰まります。まずどちらを使っているか確認してから、該当する項目をチェックしてください。

---

## 3. 診断ツールの 3 ステップ：lsusb → iwconfig → dmesg

パススルー設定が完了したら、3 つのコマンドで問題を「パススルー層」か「ドライバー層」かに切り分けます。

### ステップ 0：まずホスト側でハードウェアを確認する（アダプターのせいにしない）

<strong>ホスト OS</strong> でターミナルを開いて実行します：

```bash
lsusb
```

期待される出力（モデルによる）：

```
# AWUS036ACH (Realtek RTL8812AU)
Bus ... ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
# または AWUS036AXML (MediaTek MT7921AUN)
Bus ... ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

- ホストで認識される → ハードウェアとケーブルは正常です。問題はパススルーか Guest のドライバーにあります。
- ホストでも認識されない → <strong>まずホスト側を確認</strong>（USB ポートを変える、ケーブルを変える、別のマシンでクロステスト）してから、技術サポートのチケットを検討してください。

### ステップ 1：Guest 側の lsusb——パススルーは成功したか？

<strong>Kali 仮想マシン内</strong>で実行します：

```bash
lsusb
```

- 同じ VID:PID が見える → <strong>パススルー成功</strong>です。ステップ 2 へ進みます。
- 見えない → <strong>パススルー失敗</strong>です。第 2 章（Extension Pack / コントローラー / vboxusers グループ）に戻って確認するか、アダプターがホストの他のソフトウェアに占有されていないか確認してください。

### ステップ 2：iwconfig / ip link——ワイヤレスインターフェースは現れたか？

```bash
iwconfig
# または (新しいバージョン)
iw dev
ip link
```

- `wlan0` / `wlx...` インターフェースが現れる → <strong>すべて接続完了</strong>です。使用を開始できます。
- ワイヤレスインターフェースがないが `lsusb` では見える → 問題は <strong>Guest のドライバー層</strong>にあります。ステップ 3 へ進みます。

### ステップ 3：dmesg——ドライバー層はなぜ失敗したのか？

```bash
# カーネルの直近のメッセージを確認
sudo dmesg | tail -30
# USB とワイヤレス関連のメッセージをフィルタリング
sudo dmesg | grep -iE "usb|wlan|8812|mt7921|rtl" | tail -30
```

よくある `dmesg` の結果と対比：

| `dmesg` メッセージ | 原因 | 対処方法 |
|-------------------|------|---------|
| `usb 3-1: new high-speed USB device ...` の後に続きがない | デバイスの列挙は完了したが、利用可能なドライバーがない | Guest 内に対応するドライバーをインストール（FAQ Q4 参照） |
| `Direct firmware load failed` / `firmware_loading` | ファームウェア（firmware）ファイルがない | `apt install firmware-realtek` を実行してからモジュールを再読み込み |
| `Required key not available` | Secure Boot が有効で、モジュールが署名されていない | MOK キーで署名（Secure Boot は無効にしないでください） |
| `disagrees about version of symbol` | ドライバーのバージョンがカーネルと一致しない | DKMS で再コンパイルしてインストール |

> <strong>重要な理解</strong>：`lsusb` で見えるのは「USB パススルーは成功した」ことの証明にすぎず、<strong>ドライバーが読み込まれたことを意味しません</strong>。「パススルーは成功したのに wlan がない」というよくあるケースは、まさに Guest 内に対応するドライバーがないことが原因です。

---

## 4. USB VM Filter：挿すだけで自動マウント + 切断トラブル

### 4.1 なぜ USB フィルター（USB Filter）を設定するのか？

手動マウント（第 2 章 2.5）の問題は、<strong>Kali 仮想マシンを再起動するたびに再度クリックしなければならない</strong>ことです。「USB フィルター」を設定すると、アダプターを挿した瞬間（または仮想マシンの起動時）に、VirtualBox が<strong>条件に一致するデバイスを自動的に Guest へ転送</strong>します。

設定方法（VirtualBox）：

1. 仮想マシン設定 → USB → 右側の <strong>「＋」でフィルターを追加 → アダプターを選択</strong>。
2. VirtualBox がフィルタールールを自動入力します（ベンダー ID / プロダクト ID / シリアル番号などのフィールド）：
   - <strong>名前（Name）</strong>：例 `ALFA AWUS036AXML` または `AWUS036ACH`
   - <strong>ベンダー ID（Vendor ID）</strong>：AWUS036ACH は `0bda`、AWUS036AXML は `0e8d`
   - <strong>プロダクト ID（Product ID）</strong>：AWUS036ACH は `8812`、AWUS036AXML は `7961`
3. 同じモデルのアダプターを複数持っている場合は、「シリアル番号（Serial Number）」フィールドも入力して、別のアダプターに誤ってフィルターがかからないようにします。

> ヒント：フィルターを右クリック → <strong>フィルターの編集</strong>で、Vendor ID と Product ID だけを残す（緩いマッチ）か、シリアル番号を追加する（正確なマッチ）かを選べます。

### 4.2 頻繁な切断：多くは給電またはコントローラーの問題

高電力アダプター（AWUS036ACH はモニターモード／インジェクション時に瞬間電流が高く、AWUS036AXML は USB 3 仕様）は、仮想マシン内で「使用中にデバイスが落ちる／切断される」ことがあります。典型的な原因と対策は次のとおりです：

| 現象 | 原因 | 対策 |
|------|------|------|
| パススルー後に給電不足で落ち続ける | 仮想 USB コントローラーのエミュレートする給電能力が控えめ、またはホストのポートの給電が不足 | ホスト側で<strong>マザーボード背面の USB ポート</strong>または独立給電の USB Hub を使用 |
| アダプターが現れたり消えたりする | ホストの <strong>USB 省電力（autosuspend）</strong> がデバイスをスリープさせた | ホスト設定で「そのデバイス」の USB 自動スリープを無効化（システム全体のセキュリティ保護は無効にしないでください） |
| マウントすると即失敗、error code の羅列 | コントローラーの選択ミス（USB 1.1/2.0 では USB 3 デバイスを支えられない） | 「USB 3.0 (xHCI) Controller」に変更してシャットダウン後に再起動 |
| ホストのスリープ（sleep）から復帰後にアダプターが使えない | ホストのスリープ中に Hypervisor の USB リダイレクトが切断された | 使用中はホストのスリープを避ける；または復帰後に一度マウントし直す |

### 4.3 セキュリティ上の注意

デバイスが落ちるのを減らすために、<strong>単一の USB デバイス</strong>の自動スリープを無効化することはできますが、これは「そのデバイス」レベルに限られます。手間を省くためにシステムレベルのセキュリティ保護（ファイアウォール、Secure Boot）を無効化するのは<strong>やめてください</strong>。釣り合わない代償を払うことになります。

---

## 5. macOS ホストの制限とプラットフォームの境界線

### 5.1 macOS ホストの USB パススルーには先天的な制限がある

macOS ホストから仮想マシンを実行して USB パススルーを行うのは、<strong>最も詰まりやすい組み合わせ</strong>です。まず自分の状況を確認してください：

| macOS ホスト | VirtualBox | VMware Fusion |
|-------------|-----------|---------------|
| <strong>Apple Silicon（M1/M2/M3/M4）</strong> | ⚠️ <strong>USB パススルーのサポートが制限／不完全</strong>です。公式に公表されている既知の制限の 1 つで、アダプターのドライバーが正常でも、パススルー層がそもそも使えない可能性があります | ⚠️ サポートはより完全ですが、まず「ホストに直接挿して」macOS 側でアダプターが正常か確認することをお勧めします |
| <strong>Intel（Intel Mac）</strong> | ✅ 使用可能ですが、まず<strong>カーネルエクステンション（Kernel Extension）の承認</strong>フロー（システム設定 → プライバシーとセキュリティ → Oracle 関連のカーネルエクステンションを許可）を完了し、バージョンが完全に一致する Extension Pack をインストールする必要があります | ✅ 使用可能 |

<strong>推奨</strong>：ホストが macOS の場合は、「ホストに直接挿す → `system_profiler SPUSBDataType` → ホスト側でアダプターが正常か確認」をすべての排障の第一関門にしてください。<strong>macOS 側でサポートされていないモデルを仮想マシンの排障リストに持ち込まないでください</strong>。多くの時間を無駄にします。

### 5.2 プラットフォームの境界線（Support Boundary）

| プラットフォーム | サポート状況 | 説明 |
|----------------|-------------|------|
| Windows ホスト + VirtualBox / VMware + Kali Guest | ✅ サポート | 本章のすべての手順が適用されます |
| Linux ホスト + VirtualBox / VMware + Kali Guest | ✅ サポート | vboxusers グループ（VB）と vmware-usbarbitrator サービス（VMware）を忘れずに |
| <strong>macOS（Apple Silicon）</strong> + VirtualBox | ⚠️ <strong>USB パススルー制限あり</strong> | VMware Fusion への変更、または Linux／Windows ホストの使用を推奨 |
| macOS（Intel）+ VirtualBox | ✅ サポート | カーネルエクステンションの承認 + バージョン一致の Extension Pack が必要 |
| <strong>Guest が macOS</strong> | ❌ 非推奨 | 本記事は Kali / Debian / Ubuntu などの Linux Guest を前提としています |

> <strong>サポート境界</strong>：排障の際は必ず「ホスト側でアダプターが正常か」を先に確認してから、仮想マシン設定の問題を検討してください。ホスト側自体がアダプターを認識できない場合、どの仮想マシン設定でも復旧できません——その場合の次のステップはホスト側のドライバー問題です（当サイトの他のドライバー排障記事を参照してください）。

---

## 6. 標準排障ワークシート：問い合わせ前に一通り実行する（カスタマーサポート Intake）

> 「仮想マシンがアダプターを認識しない」場合は、次の表を順に完了し、結果を記録してください。<strong>このワークシートを一通り実行してから、技術サポートのチケットを開くかどうか決めてください</strong>——多くの場合、自分で解決できますし、サポートの往復時間も大幅に短縮できます。

### Step 1：ホスト側のハードウェア確認

| 確認項目 | コマンド | 記録欄 |
|---------|---------|-------|
| ホスト OS とアーキテクチャ | `uname -a` / `systeminfo` | \_\_\_\_\_ |
| ホストでアダプターが見えるか？ | ホストの `lsusb` | VID:PID \_\_\_\_\_ |
| USB ポートとケーブル | ポートを変える、ケーブルを変えて再試行 | 結果 \_\_\_\_\_ |

### Step 2：仮想化ソフトウェア（Hypervisor）層の確認

| 確認項目 | 操作 | 記録欄 |
|---------|------|-------|
| 仮想化ソフトウェアとバージョン | VirtualBox：`vboxmanage --version` ／ VMware：Help → About | \_\_\_\_\_ |
| 拡張パックのバージョンは一致？ | VirtualBox：`VBoxManage list extpacks` | バージョン \_\_\_\_\_ |
| ホストの権限 / サービス | Linux ホスト：`id` で vboxusers を確認；VMware：`systemctl status vmware-usbarbitrator` | \_\_\_\_\_ |
| USB コントローラー設定 | VirtualBox：USB 3.0 (xHCI) Controller にチェック？ | はい / いいえ |

### Step 3：パススルー結果の確認

| 確認項目 | コマンド | 記録欄 |
|---------|---------|-------|
| Guest でアダプターが見えるか？ | Guest 内の `lsusb` | \_\_\_\_\_ |
| ワイヤレスインターフェースは現れた？ | Guest 内の `iwconfig` / `ip link` | \_\_\_\_\_ |
| ドライバー層のメッセージ | Guest 内の `sudo dmesg \| tail -30` | \_\_\_\_\_ |
| 使用中の Guest カーネル | `uname -r` | \_\_\_\_\_ |

### Step 4：判断と記録

- `lsusb`（Guest）で見えない → <strong>パススルー層</strong>の問題 → 第 2 章と Step 2 を復習。
- `lsusb` では見えるが `ip link` に wlan がない → <strong>ドライバー層</strong>の問題 → 第 3 章のステップ 3 を復習。
- すべて正常だが不安定 → <strong>給電／省電力／コントローラー</strong>の問題 → 第 4 章。

### カスタマーサポート Intake 情報パケット

技術サポートに電話する／チケットを送信する前に、次の情報を一度に添付すれば、サポートがすぐに本題に入れます：

> <strong>ホスト OS + アーキテクチャ、仮想化ソフトウェアとバージョン、拡張パックのインストール有無とバージョン、ホスト側の `lsusb` 出力、Guest 側の `lsusb` 出力、Guest 側の `ip link` / `iwconfig` 出力、関連する `dmesg` メッセージ、アダプターのモデルと接続方法（USB-C / USB-A、直挿しまたは Hub）</strong>

---

## 7. よくある質問（FAQ）

<strong>Q1：USB ポートを変えたら `lsusb` で表示されなくなりました。アダプターの故障でしょうか？</strong>
故障とは限りません。まず「充電専用」ポートに挿していないか、ホストが省電力のためにデバイスをスリープさせていないかを確認してください。マザーボード背面の通常の USB ポートに挿し直すか、一度抜いて挿し直せば、多くの場合は復旧します。

<strong>Q2：VM ウィンドウ右下の USB アイコンが空です。どうすればよいですか？</strong>
次の順に確認してください：① Extension Pack のバージョンが VirtualBox と完全に一致しているか；② Linux ホストで `vboxusers` グループに所属しているか（再ログインが必要です）；③ ホスト側の `lsusb` でアダプターがまだ認識されているか；④ 他のソフトウェア（ホスト側のドライバーツールなど）がデバイスを占有していないか。

<strong>Q3：USB フィルターを設定したら、ホスト側でアダプターが使えなくなりました。正常ですか？</strong>
正常です。Guest にパススルーすると、デバイスの制御権は Guest 側に移り、ホスト側では同時に使用できません。ホストで他の作業に使いたい場合は、VM ウィンドウの USB アイコンから「リリース（release）」してホストに戻してください。

<strong>Q4：Guest 内の `lsusb` では認識されるのに wlan インターフェースがありません。どのドライバーを入れればよいですか？</strong>
チップセットによります：
- <strong>AWUS036AXML（MediaTek MT7921AUN）</strong>：カーネル内蔵の `mt7921u` ドライバーを使用し、Kernel 5.18+ ならプラグアンドプレイで動作します。まず `apt install linux-firmware` が更新されているか確認してください。
- <strong>AWUS036ACH（Realtek RTL8812AU）</strong>：カーネル外（out-of-tree）ドライバーのため、コミュニティ保守の `aircrack-ng/rtl8812au` をインストールし、DKMS でコンパイルする必要があります（Secure Boot の MOK 署名にも対応してください。Secure Boot は無効にしないでください）。

<strong>Q5：USB 3.0 コントローラーを選んだら、Guest が起動できなくなりました。なぜですか？</strong>
一部の古い Guest カーネルは xHCI のサポートが不十分です。Kali が古いバージョンの場合は、「シャットダウン → USB 2.0 (EHCI) Controller に戻す → 起動 → カーネルをアップグレード → USB 3.0 に戻す」の順でお試しください。Kali はできるだけ最新版を維持してください。xHCI のサポートがより完全になります。

<strong>Q6：アダプターは実機では速いのに、仮想マシン内では遅くなります。正常ですか？</strong>
正常です。仮想マシン内のアダプター性能は「USB エミュレーション層を経由した転送」とほぼ同等で、実機に直接挿した場合より多少のオーバーヘッドが加わります。正しい USB 3.0 (xHCI) コントローラーと新しい Hypervisor を使えば、そのオーバーヘッドを最小限に抑えられます。性能が著しく低下する場合は、まずコントローラーが USB 1.1 のままになっていないか確認してください。

---

## 8. 結論とハードウェアの推奨

「仮想マシンが外付けアダプターを認識しない」ケースの 9 割以上は、<strong>パススルー設定</strong>または<strong>Guest のドライバー</strong>が原因で、ハードウェアの故障はむしろまれです。本記事の手順を順番に実行してください：

1. <strong>ホスト側の `lsusb` でまずハードウェアに問題がないか確認します。</strong>
2. <strong>VirtualBox には必ずバージョン一致の Extension Pack をインストール</strong>し、Linux ホストでは `vboxusers` グループに参加します。VMware では `vmware-usbarbitrator` サービスが動作しているか確認します。
3. <strong>USB コントローラーを USB 3.0 (xHCI) に設定</strong>し、USB フィルターでアダプターを自動マウントさせます。
4. <strong>Guest 内で `lsusb → iwconfig / ip link → dmesg` の順に層を特定</strong>し、ドライバーが不足していれば補います。アダプターの故障を推測するのはやめましょう。

<strong>推奨ハードウェア</strong>：ALFA AWUS036AXML（MediaTek MT7921AUN）は、新しいカーネルの Kali では<strong>カーネル内蔵ドライバーでプラグアンドプレイ</strong>動作し、仮想マシンでのパススルー後に最も手間がかかりません。ALFA AWUS036ACH（Realtek RTL8812AU）も同様に使えますが、Guest 内で DKMS によりコミュニティドライバーをコンパイルし、Secure Boot の署名を処理することを忘れないでください（当サイトの RTL8812AU DKMS 排障記事を参照できます）。どちらも、ホスト側で独立給電の USB ポート／Hub を使用し、「デバイスが落ちる」という変数を一度に排除することをお勧めします。ただしインジェクションはカーネルバージョンに依存します。kernel 6.16 以前ではインジェクションが動作するというコミュニティ報告がありますが、stock kernel 6.16 以降（6.17 で実測）では AXML のパケットインジェクションテストは失敗し（`aireplay-ng --test` は Found 0 APs / No Answer）、deauth やハンドシェイク取得はできません。原因は mac80211 chanctx のリグレッションでチップ固有の制限ではなく、コミュニティの patched ドライバーでインジェクションは動作しますが、ファームウェアがレートを固定しており（1/6 Mbps、HT/VHT のインジェクション不可）。モニターモード、AP、WPA3 には影響しません。インジェクションが必要な場合は AWUS036ACH または AWUS036EACS をお選びください。

<strong>次のステップ</strong>：第 6 章の排障ワークシートを Kali 仮想マシンのデスクトップに保存しておきましょう。「アダプターを認識しない」たびに、まず一通り実行してから技術サポートのチケットを開くかどうか決めてください——表に従って進めれば、データがすべてを解決します。

---

## 参考リソース

| リソース | リンク |
|---------|-------|
| Oracle VirtualBox 公式ダウンロードページ（Extension Pack） | https://www.virtualbox.org/wiki/Downloads |
| VirtualBox 公式マニュアル：USB 設定とフィルター | https://www.virtualbox.org/manual/（「USB」の章を検索） |
| VirtualBox マニュアル：既知の制限（Apple Silicon の USB パススルー制限を含む） | https://www.virtualbox.org/manual/（Changelog / Limitations） |
| VirtualBox Extension Pack インストールコマンド | `vboxmanage help extpack` |
| aircrack-ng RTL8812AU コミュニティドライバー（Guest 内の AWUS036ACH 用） | https://github.com/aircrack-ng/rtl8812au |
| ALFA AWUS036ACH 公式製品ページ | https://www.alfa.com.tw/products/awus036ach_1 |
| ALFA AWUS036AXML 公式製品ページ | https://www.alfa.com.tw/ |
| Yopitek 技術サポート | https://yupitek.com/ |

> <strong>合法的な使用に関する声明</strong>：仮想マシン内でモニターモードやパケットインジェクションなどのセキュリティ操作を有効にするのは、ご自身が所有する、または明確な許可を得たネットワーク環境に限られます。利用者は所在地の法令を遵守し、すべてのテストに合法的な許可の根拠があることを確認する必要があります。