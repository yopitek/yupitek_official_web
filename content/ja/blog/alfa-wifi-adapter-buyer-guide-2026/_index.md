---
title: "ALFA WiFi アダプター購入ガイド 2026：あなたに最適なモデルはどれか？"
description: "2026年版 ALFA Network USB WiFi アダプター完全購入ガイド。AWUS036ACH、ACM、ACS、AX、AXER、AXM、AXML、EACSをドライバーサポート、monitor mode、OS互換性、価格で比較。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-network", "wifi-adapter", "buyer-guide", "kali-linux", "penetration-testing", "monitor-mode"]
---

このガイドは、2026年に最適な ALFA Network USB WiFi アダプターを選ぶ必要があるネットワークセキュリティエンジニア、エンタープライズIT専門家、レッドチームのオペレーターのために、情報の混乱を整理します。現在量産中の全8モデル — [AWUS036ACS](/en/products/alfa/awus036acs/)、[AWUS036ACH](/en/products/alfa/awus036ach/)、[AWUS036ACM](/en/products/alfa/awus036acm/)、[AWUS036EACS](/en/products/alfa/awus036eacs/)、[AWUS036AX](/en/products/alfa/awus036ax/)、[AWUS036AXER](/en/products/alfa/awus036axer/)、[AWUS036AXM](/en/products/alfa/awus036axm/)、[AWUS036AXML](/en/products/alfa/awus036axml/) — を対象に、チップセット、ドライバーの成熟度、OSサポート、実際のユースケースを比較することで、ドライバーのトラブルシューティングに費やす時間を減らし、本来の作業に集中できるようにします。

---

## 選び方：4つの重要な質問

製品ページを開く前に、次の4つの質問に答えてください。回答によって、候補のほとんどを即座に絞り込めます。

### (a) どのOSを使用していますか？

ドライバーサポートがすべてです。最近のカーネルを使用している Kali Linux および Ubuntu ユーザーは最も幅広い選択肢があります。macOS のサポートは全モデルで薄いです。Windows 10/11 は一般的によくサポートされています。Raspberry Pi または ARM ベースのプラットフォームを使用している場合、チップセットの選択が非常に重要になります。

- **Kali Linux / Debian：** RTL8812AU（`dkms-rtl8812au`）と MT7921AUN（カーネルネイティブ ≥ 5.18）が2つの主要チップセットファミリーです。
- **Ubuntu 22.04 / 24.04：** ドライバーの状況は同じですが、MT7921AUN に対して HWE カーネルや `firmware-misc-nonfree` のインストールが必要な場合があります。
- **Windows 10/11：** ALFA は現行の全モデルに署名済みドライバーを提供しています。インストールは簡単です。
- **macOS Sonoma：** コミュニティが保守する kext サポートのあるアダプターはごく少数です。摩擦が生じることを想定し、VM ワークフローを計画してください。
- **Raspberry Pi（Kali NetHunter、ARM）：** RTL8812AU モデルが安全な選択肢です。MT7921AUN も動作可能ですが、`firmware-misc-nonfree` パッケージと十分に新しいカーネルが必要です。

### (b) monitor mode と packet injection は必要ですか？

答えが「はい」なら — そしてペネトレーションテストや無線監査作業であれば必ずそうなります — [AWUS036EACS](/en/products/alfa/awus036eacs/) は候補リストからすぐに除外してください。その RTL8821CU チップセットは、Linux での monitor mode や injection を確実にサポートしません。このガイドの他の全モデルはサポートしています。

### (c) VM それともベアメタルですか？

VirtualBox および VMware での USB パススルーは複雑さのレイヤーを追加します。このリストのアダプターは、適切なパススルー設定があれば動作しますが、RTL8812AU アダプター（ACH、ACM）は VM 環境で最も長い実績があります。VM 専用でパススルーを行う場合は、実行時にファームウェアファイルを読み込むアダプターを避けてください — USB 接続が失われるとファームウェアも失われます。

完全なセットアップ手順については、[VirtualBox および VMware での ALFA アダプターセットアップ](/en/blog/alfa-adapter-virtualbox-vmware-usb/)をご覧ください。

### (d) 予算は？

Wi-Fi 5 世代（ACH、ACM、ACS）は安価で、より安定したドライバーを持ち、予算が制約となる場合やドライバーの安定性が最優先の場合に適した選択肢です。Wi-Fi 6/6E 世代（AX、AXER、AXM、AXML）はハードウェアの方向性ですが、より高額で、メインライン以外のカーネルではドライバーのエッジケースを受け入れることになります。

---

## ALFA アダプター完全比較表

<div style="overflow-x: auto;">

| モデル | Wi-Fi 世代 | チップ | 最大速度 | Monitor Mode | Kali ドライバー | Windows | macOS | アンテナ | 最適用途 |
|---|---|---|---|---|---|---|---|---|---|
| [AWUS036ACS](/en/products/alfa/awus036acs/) | Wi-Fi 5 | RTL8811AU | AC600 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 1× RP-SMA | 軽量トラベルキット |
| [AWUS036ACH](/en/products/alfa/awus036ach/) | Wi-Fi 5 | RTL8812AU | AC1200 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 2× RP-SMA | レッドチーム運用 |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | Wi-Fi 5 | MT7612U | AC1200 | ✅ | mt76x2u (≥4.19) | ✅ | ⚠️ | 2× RP-SMA | 低価格デュアルバンド |
| [AWUS036EACS](/en/products/alfa/awus036eacs/) | Wi-Fi 5 | RTL8821CU | AC1200 | ⚠️ | rtl88xxcu | ✅ | ✅ | 1× RP-SMA | 一般用途（injection 不可） |
| [AWUS036AX](/en/products/alfa/awus036ax/) | Wi-Fi 6 | RTL8832BU | AX1800 | ✅ | OOK (<6.14) | ✅ | ❌ | Integrated | Wi-Fi 6 監査 |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | Wi-Fi 6 | RTL8832BU | AX1800 | ✅ | OOK (<6.14) | ✅ | ❌ | Integrated nano | 長距離 Wi-Fi 6 |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | Wi-Fi 6E | MT7921AUN | AX1800 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 2× RP-SMA | Wi-Fi 6E エントリー |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | Wi-Fi 6E | MT7921AUN | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 1× RP-SMA | フラッグシップ 6E |

</div>

**凡例：** ✅ サポート済み · ⚠️ 限定的／部分的 · ❌ 非サポート

{{< alert "circle-info" >}}
**macOS に関する注記：** 全 ALFA アダプターは macOS Ventura および Sonoma でドライバーの問題に直面します。最も一般的なコミュニティの解決策は、Kali Linux を VM で動作させ USB パススルーを使用することです。AWUS036EACS は例外で、macOS ネイティブの Realtek ドライバーを介して動作する可能性がありますが、monitor mode は利用できません。
{{< /alert >}}

---

## Wi-Fi 5 アダプター（ドライバー成熟度 最高）

Wi-Fi 5 世代には、数年にわたるコミュニティ開発の蓄積があります。ドライバーの安定性を最優先とする場合 — 特に CTF 作業、プロフェッショナルな監査、またはカーネルアップデート後にドライバーが壊れる余裕のない環境 — はここから始めてください。

### AWUS036ACH — レッドチームのスタンダード

[AWUS036ACH](/en/products/alfa/awus036ach/) は、セキュリティコミュニティで最も広く展開されている ALFA アダプターとして、その地位を維持しています。その RTL8812AU チップセットは `aircrack-ng/rtl8812au` ドライバーによってサポートされており、このドライバーは数年にわたって主要な Kali Linux リリースに対してメンテナンスおよびテストされてきました。

**ハードウェア仕様：**
- チップセット：RTL8812AU（Realtek）
- 着脱可能な RP-SMA アンテナコネクター × 2 — ALFA アンテナラインナップ全体に対応
- 送信電力 500 mW — Wi-Fi 5 ラインナップ中最高
- デュアルバンド：2.4 GHz および 5 GHz

**レッドチームでリードする理由：** 500 mW の送信電力、デュアル外部アンテナ、成熟した injection サポートの組み合わせにより、距離を保ちながら確実なフレーム配信を維持できます。付属の全方向性アンテナを [APA-M25](/en/products/alfa/apa-m25/) 指向性パネルアンテナに交換すれば、本格的な長距離プラットフォームが完成します。また、デュアルアンテナ構成により、ターゲットネットワークに接続した際の適切な 2T2R MIMO 動作も実現します。

**Kali でのドライバーインストール：**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
```

{{< alert "triangle-exclamation" >}}
カーネル ≥ 6.2 では、古い Kali イメージに含まれる標準の `rtl8812au` モジュールが読み込みに失敗する場合があります。Kali リポジトリから `dkms-rtl8812au` を必ずインストールしてください — これはカーネルの変更を追跡し、DKMS を通じてカーネル更新時に自動的に再ビルドされます。
{{< /alert >}}

### AWUS036ACM — 低価格デュアルバンドの選択肢

[AWUS036ACM](/en/products/alfa/awus036acm/) は ACH の RTL8812AU とは異なるファミリーの MediaTek MT7612U チップセットを搭載しています。2本の RP-SMA コネクターを備えたデュアルアンテナ構成で、カーネル 4.19 以降のメインライン `mt76x2u` ドライバーによりドライバーのコンパイルが不要です。monitor mode と packet injection をサポートしています。

MT7612U のメインラインドライバーサポートにより、ACM はカーネル更新後も `dkms-rtl8812au` のリビルドなしに動作し続けます。監査チームで複数のアダプターをまとめて購入するキット展開では一般的な選択肢です。

**ACH より ACM を選ぶ場面：** 予算の制約、カーネル更新後のドライバーメンテナンスを最小化したい場合、またはメインラインカーネルドライバーを優先する環境。

### AWUS036ACS — 軽量でポータブル

[AWUS036ACS](/en/products/alfa/awus036acs/) は RTL8811AU チップセットを使用しています — RTL8812AU より送信電力は下がりますが、monitor mode と packet injection に完全に対応しています。コンパクトなフォームファクターと単一アンテナにより、空港のセキュリティで複数の RP-SMA アンテナを管理したくない出張の多いコンサルタントのための携帯選択肢になります。

RTL8811AU ドライバーは Kali 上で同じ `rtl8812au-dkms` パッケージを共有しているため、インストール手順は同一です。

**ACH/ACM とのトレードオフ：** 送信電力が低い（遠距離での距離が短い）、単一アンテナ（MIMO なし）、最大スループットが AC1200 に対して AC600。ほとんどのキャプチャ・インジェクションワークフローではこれらの違いは無関係です。長距離運用では問題になります。

### AWUS036EACS — 一般用途向け、ペンテストには不向き

[AWUS036EACS](/en/products/alfa/awus036eacs/) は Realtek RTL8821CU チップセットを搭載し、`rtl88xxcu` カーネルドライバーを使用します。このチップセットはクライアント接続向けに設計されており、パケット操作向けではありません。`rtl88xxcu` での monitor mode サポートは不安定であり、標準ドライバー設定では packet injection はサポートされていません。

{{< alert "triangle-exclamation" >}}
**AWUS036EACS をペネトレーションテスト、レッドチーム運用、または monitor mode や packet injection を必要とするタスクに使用しないでください。** 一般的な無線接続、DJI ドローンコントローラーの距離延長（一般的に組み合わせられる用途）、標準クライアントアダプターの動作が許容される Windows 優先の展開に適しています。
{{< /alert >}}

macOS 互換性においてリスト入りの理由があります — Realtek や MediaTek チップセットと比較して RTL8821CU の macOS でのドライバー状況は良好です — また、アダプターが純粋にクライアントとして使用されるコンシューマー／エンタープライズ接続展開にも適しています。

---

## Wi-Fi 6 アダプター（現在のスイートスポット）

Wi-Fi 6（802.11ax）は、高密度環境でのパフォーマンス、ターゲットリッチな MU-MIMO シナリオ、ネットワーク識別のための BSS Coloring に意義ある改善をもたらしました。エンタープライズ展開が 802.11ax インフラへ積極的にシフトするにつれ、Wi-Fi 6 アダプターは無線監査担当者にとってますます重要になっています。

両方の Wi-Fi 6 ALFA アダプター（AX、AXER）は Realtek RTL8832BU チップセットを使用しています。Linux では、カーネル 6.14 未満で RTL8832BU ドライバーはアウトオブカーネル（OOK）となり、monitor mode と packet injection は限定的なサポートとなります。主に Windows クライアント接続向けに設計されています。

### AWUS036AX — クリーンな Wi-Fi 6 の選択肢

[AWUS036AX](/en/products/alfa/awus036ax/) は RTL8832BU チップセットを搭載した Wi-Fi 6 アダプターです：統合アンテナ（外部 RP-SMA コネクターなし）、2.4 GHz および 5 GHz バンドで AX1800（理論上最大 1800 Mbps）。

**ドライバーの状態：**
- Windows：完全サポート（ALFA 提供ドライバー）
- カーネル ≥ 6.14：インカーネルドライバーサポート
- カーネル < 6.14：アウトオブカーネル（OOK）ドライバーが必要
- Monitor mode：⚠️ 限定的

**monitor mode に関する実用的な注記：** RTL8832BU の monitor mode サポートはカーネル 6.14 未満では限定的です。ペネトレーションテストや packet injection が主な用途であれば、RTL8812AU ベースのアダプター（ACH、ACM）または MT7921AUN ベースの AXM/AXML を検討してください。

{{< alert "circle-info" >}}
**カーネルの確認：** 購入前に `uname -r` を実行してカーネルバージョンを確認してください。カーネル ≥ 6.14 では RTL8832BU のインカーネルドライバーが利用可能です。
{{< /alert >}}

### AWUS036AXER — 長距離バリアント

[AWUS036AXER](/en/products/alfa/awus036axer/) は AWUS036AX と同じ RTL8832BU チップセットを搭載した超コンパクトなナノフォームファクターのアダプターです。ドライバーの状況は同一です — 同じ RTL8832BU、同じ Linux の制限（カーネル < 6.14 では OOK）、同じ Windows 互換性。

動作距離が決定要因である場合に AX より AXER を選択してください：大規模キャンパスのサイトサーベイ、屋外評価、または AP が遠距離にあるシナリオ。価格プレミアムは控えめで、距離が展開に重要であれば正当化できます。

---

## Wi-Fi 6E アダプター（将来対応）

Wi-Fi 6E は 802.11ax を 6 GHz バンドに拡張し、新しい 5.925–7.125 GHz スペクトルへのアクセスを提供します。実際には、これは干渉の減少、より広いチャネル幅（最大 160 MHz）、そして古い機器が見たり届いたりできないバンドへのアクセスを意味します。エンタープライズネットワークが Wi-Fi 6E インフラを展開するにつれ、監査担当者は完全な攻撃対象領域を評価するために 6E 対応アダプターが必要になります。

両方の Wi-Fi 6E ALFA アダプターは 6 GHz サポートに カーネル ≥ 5.18 が必要です。6 GHz バンドは規制ドメインを正しく設定する必要があります — ほとんどの地域で 6 GHz の規制実施は 2.4/5 GHz よりも厳格です。

### AWUS036AXM — Wi-Fi 6E エントリーポイント

[AWUS036AXM](/en/products/alfa/awus036axm/) は 6 GHz バンドサポートが有効になった MT7921AUN チップセットを使用しています。2本の RP-SMA コネクターが付属し、2T2R デュアルアンテナ動作に対応しています。

主に 2.4 GHz および 5 GHz 環境で作業しながら、フラッグシップ価格を払わずに新興ネットワーク評価のための 6 GHz 対応を必要とするオペレーターにとって、AXM は論理的なエントリーポイントです。

**バンドカバレッジ：** 2.4 GHz、5 GHz、6 GHz（トライバンド）
**アンテナ：** 2× RP-SMA — 対応する ALFA アンテナと交換可能

### AWUS036AXML — フラッグシップ 6E アダプター

[AWUS036AXML](/en/products/alfa/awus036axml/) は ALFA の現在の最上位アダプターです。MT7921AUN チップセット、シングル高ゲイン RP-SMA コネクター、USB-C 3.2 接続、Bluetooth 5.2 を備えています。

**主要仕様：**
- チップセット：MT7921AUN（MediaTek）
- RP-SMA コネクター × 1（シングル高ゲイン）
- トライバンド：2.4 GHz + 5 GHz + 6 GHz
- AX3000 クラス（バンド全体で理論上最大 3000 Mbps）
- ALFA 6E ラインナップ中最高の電力出力

**AXML のドライバー注記：**
- MT7921AUN はカーネル ≥ 5.18 で同じ `mt7921u` ドライバーファミリーでサポートされています
- Monitor mode はサポート済み；ファームウェアを使用したアクティブモニターは一部のカーネルでファームウェア再起動の問題を示しています — 完全なテストデータについては [AWUS036AXML 詳細レビュー](/en/blog/awus036axml-wifi-6e-review/)を参照してください
- Monitor mode での 6 GHz バンドには、規制ドメインが 6 GHz チャネルでのパッシブスキャンを許可している必要があります

{{< alert "triangle-exclamation" >}}
**AWUS036AXML ファームウェア注記：** カーネル 6.1 未満では、AXML を monitor mode とマネージドモード間で繰り返し切り替える際にファームウェアクラッシュを経験するユーザーがいます。ワークフローで頻繁なモード切り替えが必要な場合は、カーネル ≥ 6.1 で実行し、最新の `firmware-misc-nonfree` パッケージをインストールしてください。
{{< /alert >}}

---

## ドライバー互換性の詳細

<div style="overflow-x: auto;">

| モデル | チップ | Kali パッケージ | Ubuntu HWE | RPi ARM | Windows 10/11 |
|---|---|---|---|---|---|
| [AWUS036ACS](/en/products/alfa/awus036acs/) | RTL8811AU | `dkms-rtl8812au` | 手動ビルド | ✅ rtl8812au-dkms | ✅ ALFA ドライバー |
| [AWUS036ACH](/en/products/alfa/awus036ach/) | RTL8812AU | `dkms-rtl8812au` | 手動ビルド | ✅ rtl8812au-dkms | ✅ ALFA ドライバー |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | MT7612U | `mt76x2u (in-kernel)` | カーネル ≥ 4.19 | ✅ mt76x2u (≥4.19) | ✅ ALFA ドライバー |
| [AWUS036EACS](/en/products/alfa/awus036eacs/) | RTL8821CU | `rtl88xxcu` | カーネル内蔵 | ⚠️ 限定的 | ✅ 内蔵 |
| [AWUS036AX](/en/products/alfa/awus036ax/) | RTL8832BU | `firmware-misc-nonfree` | カーネル ≥ 5.18 | ⚠️ ファームウェア要 | ✅ ALFA ドライバー |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | RTL8832BU | `firmware-misc-nonfree` | カーネル ≥ 5.18 | ⚠️ ファームウェア要 | ✅ ALFA ドライバー |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | MT7921AUN | `firmware-misc-nonfree` | カーネル ≥ 5.18 | ⚠️ ファームウェア要 | ✅ ALFA ドライバー |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | MT7921AUN | `firmware-misc-nonfree` | カーネル ≥ 5.18 | ⚠️ ファームウェア要 | ✅ ALFA ドライバー |

</div>

**RTL8812AU カーネル履歴：** RTL8812AU ドライバーは Linux 5.2 でメインラインカーネルに部分的に統合されましたが、大きな制限がありました — monitor mode なし、injection なし。完全なペネトレーションテスト機能には、アウトオブツリーの `rtl8812au` ドライバーが必要で、Kali では `dkms-rtl8812au` としてパッケージ化されています。DKMS パッケージはカーネル更新時に自動的に再ビルドされるため、Kali Linux システムでは実質的にメンテナンスフリーです。

**MT7921AUN カーネル履歴：** ネイティブ統合は Linux 5.18 で `mt7921u` USB ドライバーとして実現しました。ファームウェアファイル `WIFI_MT7961_patch_mcu_1_2_hdr.bin`（および関連するファームウェアブロブ）が `/lib/firmware/mediatek/` に存在している必要があります。Kali では `firmware-misc-nonfree` によって取り込まれます。デフォルトカーネルを使用した Ubuntu 22.04 LTS では、≥ 5.18 に達するために HWE スタック（`linux-generic-hwe-22.04`）のインストールが必要な場合があります。

**Raspberry Pi の詳細：** RTL8812AU ドライバーは `dkms-rtl8812au` を使用して Raspberry Pi OS（32ビットおよび64ビット）でクリーンにコンパイルされます。NetHunter 展開の最も安全な選択です。MT7921AUN アダプターは Pi 4/5 で動作可能ですが、`firmware-misc-nonfree` と十分に新しい Raspberry Pi OS カーネル（2023年以降のイメージなら大丈夫です）が必要です。

---

## ユースケース別の最適 ALFA アダプター

### レッドチーム運用

**推奨：[AWUS036ACH](/en/products/alfa/awus036ach/)**

ACH の 500 mW 送信電力、デュアルアンテナ、実戦テスト済みの RTL8812AU ドライバーにより、レッドチームエンゲージメントのデフォルト選択肢となっています。カーネル更新後も動作し、VM を通じて確実にパススルーでき、持参するどんな RP-SMA アンテナも受け入れます。予算が許し、スコープに 6E カバレッジが含まれる場合は、6 GHz ネットワーク探索用のセカンダリアダプターとして [AWUS036AXML](/en/products/alfa/awus036axml/) を追加してください。

### CTF コンペティション

**推奨：[AWUS036ACM](/en/products/alfa/awus036acm/)**

CTF の無線チャレンジは通常、送信電力が重要な変数でない管理された環境を含みます。ACM は低価格で完全な monitor mode と injection 機能を提供します。コンパクトな単一アンテナのフォームファクターは持ち運びと展開が容易です。CTF が Wi-Fi 6 のチャレンジを含む場合（まだまれですが増えています）は、代わりに [AWUS036AX](/en/products/alfa/awus036ax/) を使用してください。

### Raspberry Pi / Kali NetHunter

**推奨：[AWUS036ACH](/en/products/alfa/awus036ach/) または [AWUS036ACM](/en/products/alfa/awus036acm/)**

両方の RTL8812AU アダプターは Raspberry Pi ハードウェアで実績があります。特定のイメージでカーネルとファームウェアの互換性を確認していない限り、Pi 展開では MT7921AUN モデルを避けてください。フィールドで確実に動作する必要がある専用 NetHunter Pi を構築する場合は、ACH がより安全な選択です。

### エンタープライズ無線監査

**推奨：[AWUS036AXML](/en/products/alfa/awus036axml/) + [AWUS036ACH](/en/products/alfa/awus036ach/)**

最新のエンタープライズ無線監査は 2.4、5、6 GHz バンドをカバーする必要があります。AXML は 6E を含む完全なトライバンドスペクトルをカバーし、ACH は 5 GHz 作業のための安定した高電力フォールバックを提供します。別々のキャプチャインターフェースで両方を同時実行すれば、ドライバーの妥協なしに完全なバンドカバレッジが得られます。ACH をアクティブ injection タスクに使用し、AXML をパッシブ 6 GHz モニタリングに使用してください。

### DJI ドローン距離延長

**推奨：[AWUS036EACS](/en/products/alfa/awus036eacs/)**

Litchi や DJI GO を通じた DJI 距離延長は一般的な合法的ユースケースです。RTL8821CU を搭載した EACS はここで特別に推奨されます。DJI ソフトウェアが動作する Windows 上で追加ドライバーなしにネイティブで動作し、その汎用接続プロファイルがこのユースケースに適しています。Monitor mode は不要で、クライアントモード接続と送信電力が重要です。最大の実効距離のために [APA-M25](/en/products/alfa/apa-m25/) パネルアンテナと組み合わせてください。

---

## OS別の推奨事項

### Kali Linux

Kali Linux は、セキュリティ作業に使用される全 ALFA アダプターの主要サポートプラットフォームです。Kali リポジトリには、RTL8812AU/RTL8811AU アダプター用の `dkms-rtl8812au` と MT7921AUN/MT7921AUN アダプター用の `firmware-misc-nonfree` が含まれています。Kali のインストールを更新し続けてください — DKMS パッケージはカーネルの変更を自動的に追跡します。

**クイックセットアップ（RTL8812AU ファミリー）：**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
sudo modprobe 88XXau
```

**クイックセットアップ（MT7921AUN ファミリー）：**
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
# 再起動またはモジュールの再読み込み：
sudo modprobe mt7921u
```

**monitor mode の有効化：**
```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

### Ubuntu 24.04 LTS

Ubuntu 24.04 はカーネル 6.8 で出荷されます。`firmware-misc-nonfree` をインストールすれば MT7921AUN アダプターがすぐに動作します：
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

Ubuntu での RTL8812AU サポートには DKMS モジュールのビルドが必要です：
```bash
sudo apt install -y git dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && sudo make dkms_install
```

### Windows 11

全 ALFA アダプターは Windows 10/11 互換ドライバーが付属しています。ALFA Network ウェブサイトからドライバーパッケージをダウンロードするか、MT7921AUN の場合は Windows Update（Microsoft は WHQL 署名済みの受信トレイドライバーを提供）でインストールしてください。RTL8812AU アダプターには ALFA 提供の Realtek ドライバーパッケージが必要です；RTL8812AU の Windows Update ドライバーの利用可能性は一定しません。

Acrylic Wi-Fi、inSSIDer、または Windows 版の Wireshark などのツールで使用する場合、ALFA ドライバーは NDIS monitor mode を通じて Windows で機能的な monitor mode ラッパーを提供します — ただし、これはアクティブな injection 作業に対して Linux の monitor mode よりも実質的に機能が劣ります。

### macOS Sonoma

2026年において、macOS Sonoma に対して公式サポートされている ALFA アダプターはありません。RTL8812AU 向けのコミュニティ kext プロジェクトは存在しますが、署名されておらず System Integrity Protection（SIP）を無効にする必要があります。現実的な推奨事項は、ALFA アダプターへの USB パススルーで Kali Linux を VM（Parallels、VMware Fusion、または UTM）で実行することです。

RTL8821CU を搭載した AWUS036EACS は、ネイティブの Realtek kext を通じて最も機能的な macOS サポートを持っていますが、標準クライアント接続のみで monitor mode は対応していません。

### Raspberry Pi / Kali NetHunter

Kali NetHunter を実行する Raspberry Pi 4 および Pi 5 上で：

```bash
# RTL8812AU アダプターの場合：
sudo apt update && sudo apt install -y dkms-rtl8812au

# MT7921AUN アダプターの場合（最新カーネルの Pi 5 推奨）：
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

{{< alert "circle-info" >}}
専用の NetHunter ドロップボックスを構築する場合は、[AWUS036ACH](/en/products/alfa/awus036ach/) または [AWUS036ACM](/en/products/alfa/awus036acm/) を使用してください。これらの RTL8812AU ドライバーは ARM 上で確実にコンパイルされ、ファームウェアファイルへの依存がありません。MT7921AUN モデルは Pi でも機能しますが、オフライン展開で問題を引き起こす可能性のあるファームウェアファイルへの依存関係が追加されます。
{{< /alert >}}

---

## 最終推奨

ドライバーの成熟度、ハードウェア機能、実際のユースケース全体にわたって全8モデルを評価した結果、ほとんどのプロフェッショナルをカバーする3つの選択肢は以下の通りです：

**コスパ重視：[AWUS036ACM](/en/products/alfa/awus036acm/)**
MT7612U チップセットのデュアルアンテナアダプターは、デュアルバンドラインナップ中最低価格で完全な monitor mode と packet injection サポートを提供します。信頼性の高いツールを過剰な投資なしに求めるコンサルタント、または量でアダプターを購入するチームに最適です。

**万能：[AWUS036ACH](/en/products/alfa/awus036ach/)**
デュアルアンテナ、500 mW の RTL8812AU アダプターは、セキュリティ専門家に最も広く推奨される単一アダプターです。2.4 GHz および 5 GHz をカバーし、外部アンテナを受け入れ、このリストのどのアダプターよりも成熟したドライバースタックを持ち、ACM よりも若干高いだけです。1つのアダプターを購入する場合で、まだ必要なものが明確でなければ、これを買ってください。

**エンタープライズ／将来対応：[AWUS036AXML](/en/products/alfa/awus036axml/)**
監査スコープに Wi-Fi 6E インフラが含まれる場合 — 2026年以降に始まるエンゲージメントではそうあるべきです — AXML はデュアルアンテナの 6 GHz 機能を提供する唯一のアダプターです。ACH と組み合わせて、2.4 GHz から 6 GHz までの全バンドを妥協なくカバーする2アダプターキットを構成してください。

詳細なセットアップと設定手順については以下を参照してください：
- [Kali Linux および Ubuntu への ALFA ドライバーインストール](/en/blog/install-alfa-driver-kali-ubuntu/)
- [カーネル更新後の ALFA ドライバー修正](/en/blog/fix-alfa-driver-kernel-update/)
- [Kali Linux での monitor mode 有効化](/en/blog/enable-monitor-mode-kali-linux/)
- [AWUS036AXML Wi-Fi 6E レビューとドライバーテスト](/en/blog/awus036axml-wifi-6e-review/)
