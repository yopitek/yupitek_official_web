---

title: "macOSでALFA WiFiアダプターを使う：VMware FusionとParallels USBパススルー完全ガイド"
description: "macOSでALFA USB WiFiアダプターを使う方法。macOSネイティブサポート、VMware Fusion USBパススルー、Parallels Desktopを使ったKali LinuxのモニターモードとパケットインジェクションをApple Silicon対応で解説。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["macos", "vmware-fusion", "parallels", "kali-linux", "usb-passthrough", "alfa-network", "AWUS036AXML"]
featureimage: "/images/blog/alfa-adapter-macos-vm-setup.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "ALFAアダプターはmacOSでネイティブにモニターモードを使えますか？"
    answer: "使えません。macOSのCoreWLANとIO80211Familyアーキテクチャはサードパーティアダプターのモニターモードやパケットインジェクションをサポートしておらず、VMでKali Linuxを実行しUSBパススルーを使用する必要があります。"
  - question: "Apple Silicon MacではVMware FusionとParallelsのどちらが良いですか？"
    answer: "どちらでも使えますが、Parallels Desktop 19+はApple Silicon上のARM64 VMパフォーマンスとUSBパススルーの安定性で通常VMware Fusionより優れています。"
  - question: "AWUS036AXMLはApple SiliconのKali VMでドライバーをコンパイルする必要がありますか？"
    answer: "不要です。MT7921AUNドライバーはLinux 5.18以降カーネルに内蔵されており、Kali ARM64 2024.x以降なら挿すだけで自動認識されます。"
  - question: "Intel Macで標準のKali x86_64 ISOを使えますか？"
    answer: "使えます。Intel Macはx86_64アーキテクチャなので、kali.org公式の標準Kali Linux x86_64 ISOを直接使用してVMを作成できます。"
  - question: "VirtualBoxはApple Siliconでセキュリティテストに適していますか？"
    answer: "推奨しません。VirtualBoxのApple Siliconサポートはまだ実験段階で、USBパススルーに既知の問題があるため、VMware FusionまたはParallelsをお使いください。"
---

macOSは洗練された生産性重視のOSですが、無線セキュリティリサーチ向けには設計されていません。ペネトレーションテスターのツールキットを定義する2つの機能——**モニターモード**と**パケットインジェクション**——はmacOSのWi-Fiスタックには存在しません。AppleのWi-Fiドライバーは、きれいで機能的なネットワークインターフェースを提供するだけです。


{{< tldr >}}
macOSはALFAアダプターのモニターモードとパケットインジェクションをサポートしていません。解決策はVMware FusionまたはParallelsでKali Linux VMを実行し、USBパススルーでアダプターをVMに渡すことです。Apple SiliconではARM64版Kaliイメージが必要です。
{{< /tldr >}}
ALFAアダプターはLinuxではドライバーサポートが充実していますが、macOSでは状況が異なります。ALFAアダプターがmacOSに認識されても、ネイティブネットワークスタックではモニターモードへの切り替えや生のパケット送信はできません。唯一の確実な解決策は、**仮想マシンでKali Linuxを実行し**、macOSを完全にバイパスしてUSBアダプターをゲストOSに直接パススルーすることです。

このガイドでは、macOSの2大ハイパーバイザー——VMware FusionとParallels Desktop——での正しいセットアップ方法を解説します。特に**Apple Silicon（M1/M2/M3）**に重点を置き、ARMアーキテクチャがアダプターとISOの選択に与える影響を詳しく説明します。

---

## macOSネイティブ：VMなしでできること

VM設定に入る前に、macOSがALFAアダプターで何ができて何ができないかを理解しておくことが重要です。

**AWUS036AXML（MT7921AUNチップセット）：** macOSはこのアダプターを汎用USBネットワークデバイスとして認識します。macOS 13 Ventura以降に搭載された**MT7921AUN**ドライバーが自動的にアダプターを検出します。**システム環境設定 → ネットワーク**（Ventura以降は**システム設定 → ネットワーク**）に新しいインターフェースとして表示され、通常のアダプターと同様にWi-Fiに接続できます。

**AWUS036ACH（RTL8812AU）とAWUS036ACM（MT7612U）— macOSでサードパーティドライバーが必要なアダプター：** macOSではサードパーティドライバーが必要です。コミュニティや商用のドライバーパッケージはありますが、互換性は不安定です。macOSのマイナーアップデート後にドライバーの再インストールが必要になることが多く、macOS 11以降はカーネル拡張の署名要件が厳しくなっています。

**根本的な制限——モニターモード不可：** どのアダプターを使っても、どのドライバーをインストールしても、macOSはrawモニターモードインターフェースを提供しません。CoreWLANフレームワークと基盤となる`IO80211Family.kext`アーキテクチャは、サードパーティアダプターのモニターモードをサポートしていません。セキュリティテストにはUSBパススルー付きのKali Linux VMが必要です。

{{< alert "circle-info" >}}
デバッグ目的のパッシブなWi-Fiトラフィックキャプチャのみが目的であれば、macOSではOptionキーを押しながらメニューバーのWi-Fiアイコンをクリックして診断モードに入ることができます。ただし、これは正式なモニターモードワークフローの代替にはなりません。
{{< /alert >}}

---

## Apple Silicon（M1/M2/M3）vs Intel Mac

MacのアーキテクチャによってKali Linuxのイメージと使用可能なハイパーバイザーが決まります。

**Intel Mac（x86_64）：**
VMware Fusion、Parallels Desktop、VirtualBoxの3つのハイパーバイザーすべてがIntel Macでネイティブ動作します。kali.orgの公式ダウンロードページから標準の**Kali Linux x86_64 ISO**を使用できます。

**Apple Silicon（M1/M2/M3）：**
Apple SiliconはARM64アーキテクチャです。標準のx86_64 Kali ISOはApple Siliconハードウェアでは起動できません——x86エミュレーション層がないためです（RosettaはmacOSユーザースペースアプリにのみ適用され、OS全体の仮想化には適用されません）。[kali.org/get-kali](https://www.kali.org/get-kali/)のApple Silicon / ARMセクションから**Kali Linux ARM64**イメージを使用する必要があります。

| ハイパーバイザー | Intel Mac | Apple Silicon |
|---|---|---|
| VMware Fusion 13+ | ✅ 個人利用は無料 | ✅ ARM64 VMに対応 |
| Parallels Desktop 19+ | ✅ | ✅ Apple Siliconで最高性能 |
| VirtualBox 7.x | ✅ | ⚠️ Apple Siliconでは実験的 |

{{< alert "triangle-exclamation" >}}
Apple SiliconへのVirtualBoxサポートはまだ実験的とされています。USBパススルーはMチップMacで既知の問題があります。Apple Siliconハードウェアでのセキュリティテストには、VMware FusionまたはParallels Desktopを使用してください。
{{< /alert >}}

**USBパススルーはアーキテクチャに依存しない：** ALFAアダプター自体はUSBデバイスです。ホストCPUがx86_64かARM64かに関わらず、USBパススルーの動作は同じです。アダプターはUSBバス経由でゲストVMに引き渡され、Kali内のドライバーが処理します。

---

## オプションA：VMware Fusion USBパススルー

VMware FusionはFusion 13から個人利用が無料になり、コストゼロのハイパーバイザーを求めるmacOSユーザーの標準推奨となっています。

### ステップ1 — VMware Fusion 13+のインストール

[vmware.com/products/fusion.html](https://www.vmware.com/products/fusion.html)からVMware Fusionをダウンロードします。インストール時に**システム環境設定 → セキュリティとプライバシー → 一般**でVMwareシステム拡張を許可する必要があります。この拡張の承認はUSBパススルーに必須です。承認後、macOSが再起動を求める場合は完了してから続けてください。

### ステップ2 — Kali Linux VMの作成

- **Apple Silicon Mac：** kali.orgからKali Linux ARM64インストールISOまたは事前構築されたVMware ARMイメージをダウンロードし、VMware FusionでそのARM64 ISOを選択して新しいVMを作成します。
- **Intel Mac：** 標準のKali Linux x86_64インストールISOをダウンロードし、新しいVMを作成します。

最低**4 GB RAM**と**40 GBディスク**を割り当ててください。Kaliのインストール時にフルデフォルトパッケージセットを選択して、無線ツール（aircrack-ng、airmon-ng、airodump-ng）を事前インストールします。

### ステップ3 — ALFAアダプターをUSBパススルーで接続

KaliのVMが実行中で、ALFAアダプターをMacのUSBポートに接続した状態で：

1. VMware Fusionがポップアップを表示します：**「USBデバイスが仮想マシンへの接続を要求しています。」**
2. **[VM名]に接続**をクリックして、アダプターをKali VMに直接引き渡します。
3. この時点でmacOSはアダプターを見失います——VMが排他的に所有します。

{{< alert "circle-info" >}}
ポップアップが表示されない場合（VMの起動前にアダプターが既に接続されていた場合など）、VMware Fusionのメニューバーから**仮想マシン → USBとBluetooth → [ALFAアダプター名] → 接続（Macから切断）**で手動でUSBデバイスをVMに割り当てます。
{{< /alert >}}

### ステップ4 — Kali内での確認

Kali VMのターミナルでアダプターが見えることを確認します：

```bash
lsusb | grep -i mediatek
# AWUS036AXML / MT7921AUN: Bus 001 Device 002: ID 0e8d:7961 MediaTek Inc. ...

lsusb | grep -i realtek
# AWUS036ACH / RTL8812AU: Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. ...
```

### ステップ5 — ドライバーのロードとモニターモードの確認

MT7921AUN（AWUS036AXML）のドライバーはKaliカーネルに組み込まれています。RTL8812AUアダプターはドライバーのインストールが必要です——[ドライバーインストールガイド](/ja/blog/install-alfa-driver-kali-ubuntu/)を参照してください。ドライバーが有効になったら：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
```

---

## オプションB：Parallels Desktop USBパススルー

Parallels Desktopはパフォーマンスを優先するApple Silicon Macの推奨ハイパーバイザーです。サブスクリプションライセンスが必要ですが、Apple SiliconハードウェアでのARM64 VMサポートとUSBパススルーの実装はVMware Fusionより成熟しています。

### ステップ1 — Parallels Desktop 19+

[parallels.com](https://www.parallels.com)からParallels Desktopをインストールします。VMware Fusionと同様に、**セキュリティとプライバシー**でParallelsシステム拡張を許可して再起動します。

### ステップ2 — Kali Linux ARM64 VMの作成

Apple SiliconではParallelsはARM64ゲストOSイメージのみサポートします。kali.orgからKali Linux ARM64イメージをダウンロードし、Parallelsでそのイメージを使用して新しいVMを作成します。

{{< alert "circle-info" >}}
Parallels Desktop 19+はApple Silicon上の新しいVMアシスタントからKali Linux ARMを直接ダウンロードしてインストールできます——ISOを手動でダウンロードする必要がない場合があります。
{{< /alert >}}

### ステップ3 — USBでALFAアダプターを接続

KaliのVMが実行中でALFAアダプターが接続された状態で：

1. macOSのメニューバーで**デバイス → USBとBluetooth**に移動します。
2. リストからALFAアダプターを見つけます（**Realtek 802.11ac NIC**、**MediaTek Wi-Fi**などと表示される場合があります）。
3. クリックして**Linuxに接続**（またはVMの名前）を選択します。

### ステップ4 — lsusbで確認

Kali VMのターミナルで：

```bash
lsusb
ip link show
```

{{< alert "circle-info" >}}
Apple SiliconでのParallelsは、I/O集約型のVMワークロードでVMware Fusionより一般的に高いパフォーマンスを発揮します。長時間のairodump-ngセッションや大量のパケットキャプチャを行う場合、ParallelsのほうがCPU負荷が低くなる傾向があります。
{{< /alert >}}

---

## Apple Silicon上のKali：ARM64ドライバーの注意事項

**RTL8812AU（ARM64）：**
[aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au)のRTL8812AUドライバーはARM64でも正しくコンパイルできます。DKMSビルドプロセスはx86_64と同じです：

```bash
sudo apt update && sudo apt install -y dkms linux-headers-$(uname -r) build-essential
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

**MT7921AUN（ARM64）：**
`mt7921u`ドライバーは**Linux 5.18からカーネルに内蔵**されており、Kali ARM64 2024.x以降に含まれています。AWUS036AXMLはKali ARM64で手動コンパイル不要で、USBパススルー後に自動的に認識されます。

```bash
dmesg | grep mt7921
# [ 4.123456] mt7921u 1-1:1.0: HW/SW Version: 0x8a108a10, Build Time: ...
```

**Mチップ Mac向け推奨：** Apple Silicon Mac上のVMで使用するためにALFAアダプターを購入するなら、**AWUS036AXML（MT7921AUN）** がより良い選択です。カーネル内蔵ドライバーによりDKMSコンパイル手順が不要で、ARM64 Kaliで確実に動作します。

---

## モニターモードとインジェクションテスト

USBパススルー完了後、以下のコマンドシーケンスを実行してスタック全体が正常に動作していることを確認します：

```bash
# 1. USBデバイスが見えることを確認
lsusb

# 2. 無線インターフェースの一覧表示
ip link show

# 3. 競合するプロセスを終了
sudo airmon-ng check kill

# 4. 無線インターフェースでモニターモードを開始
sudo airmon-ng start wlan1

# 5. モニターインターフェースが作成されたことを確認
ip link show wlan1mon

# 6. パッシブスキャンを開始
sudo airodump-ng wlan1mon
```

**パススルー後に`wlan1`が表示されない場合：**
ALFAアダプターをMacから抜き、5秒待ってから再接続し、ハイパーバイザーのUSBデバイスメニューでVMに再割り当てして、Kali内で`lsusb`を再実行してデバイスが表示されることを確認します。

{{< alert "triangle-exclamation" >}}
VM内のデフォルト`wlan0`インターフェースに対して`airmon-ng start wlan0`を実行しないでください——そのインターフェースは通常、VMware/Parallelsがインターネット接続に使用する仮想ネットワークアダプターであり、パススルーされたALFAアダプターではありません。
{{< /alert >}}

---

## パフォーマンスと制限事項

**USBパススルーのレイテンシ：** ハイパーバイザー層を経由してUSBデバイスをパススルーすると、ベアメタルLinuxと比較して約1〜2 msの処理レイテンシが追加されます。802.11セキュリティテストの目的では、このレイテンシは操作上重要ではありません。

**排他的所有権：** macOSはALFAアダプターをKali VMと同時に共有できません。アダプターがVMにパススルーされると、macOSからは完全に見えなくなります。

**消費電力：** USBのWi-FiアダプターをVM内で動作させながらMac自体のWi-Fiも動作させると、電力消費がかなり大きくなります。**長時間のテストセッションでは充電器を使用してください**。

---

## トラブルシューティング

| 症状 | 考えられる原因 | 解決策 |
|---|---|---|
| ALFAアダプターがハイパーバイザーのUSBメニューに表示されない | macOSシステム拡張が未承認 | **システム環境設定 → セキュリティとプライバシー → 一般** → VMware/Parallels拡張を許可して再起動 |
| Kali VM内の`lsusb`にALFAアダプターが表示されない | USBパススルーが完了していない | VM → USBとBluetoothメニューで手動接続；アダプターを再接続 |
| パススルー後に`wlan1`インターフェースがない | ドライバーが未ロード（RTL8812AU） | DKMSでRTL8812AUドライバーをインストール；[ドライバーインストールガイド](/ja/blog/install-alfa-driver-kali-ubuntu/)を参照 |
| `airmon-ng start wlan1`が「Operation not permitted」で失敗 | NetworkManagerがインターフェースを保持 | まず`sudo airmon-ng check kill`を実行してから再試行 |
| モニターモードは開始されるがairodump-ngにネットワークが表示されない | 間違ったチャンネルまたはインターフェース | `ip link show`で`wlan1mon`の存在を確認；`sudo airodump-ng --band abg wlan1mon`を試す |
| ALFAアダプター接続時にVMがフリーズ | USBコントローラーの競合（VMware） | VMをシャットダウン、VM設定 → USBでコントローラーをUSB 3.0からUSB 2.0に変更、VMを再起動 |

{{< alert "circle-info" >}}
Apple Siliconで、ALFAアダプターは認識されるがインターフェースがKaliに表示されない場合、接続直後に`dmesg | tail -30`を実行してください。カーネルがデバイスを検出したかどうか、どのドライバーがバインドを試みているかが表示されます。
{{< /alert >}}

---


---

{{< faq >}}

## 関連ガイド

WindowsおよびLinuxホストでVirtualBoxまたはVMware Workstationを使用する場合のガイド：[ALFA アダプター USBパススルー：VirtualBoxとVMwareのセットアップガイド](/ja/blog/alfa-adapter-virtualbox-vmware-usb/)。

このガイドで推奨しているAWUS036AXMLの詳細レビューは：[ALFA AWUS036AXML WiFi 6E レビュー](/ja/blog/awus036axml-wifi-6e-review/)。

---

## 参考文献

1. [ALFA Network公式ウェブサイト](https://www.alfa.com.tw/)
2. [Kali Linux公式ダウンロードページ](https://www.kali.org/get-kali/)
3. [VMware Fusion製品ページ](https://www.vmware.com/products/fusion.html)
4. [Parallels Desktop公式ウェブサイト](https://www.parallels.com/)
5. [aircrack-ng rtl8812auドライバープロジェクト](https://github.com/aircrack-ng/rtl8812au)
