---
title: "엔터프라이즈 무선 보안 평가: 완전한 프레임워크"
description: "ALFA 어댑터를 활용한 완전한 엔터프라이즈 무선 보안 평가 프레임워크. 범위 설정, 불량 AP 탐지, WPA2/WPA3 감사, PMF 테스트, IT 보안팀을 위한 보고서 작성까지 다룹니다."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "엔터프라이즈 무선 보안 평가는 어떤 단계로 구성됩니까?"
    answer: "완전한 평가는 여섯 단계로 순차적으로 진행됩니다: 패시브 정찰, 불량 AP 탐지, WPA2/WPA3 핸드셰이크 분석, PMF 검증, 클라이언트 격리 테스트, EAP/RADIUS 평가입니다."
  - question: "무선 보안 평가를 수행하기 전에 어떤 승인이 필요합니까?"
    answer: "CISO 또는 자산 소유자가 서명한 서면 승인을 반드시 확보해야 하며, 테스트 기간, 장비 MAC 주소, 승인된 기법을 명확히 포함해야 합니다. 구두 동의로는 충분하지 않습니다."
  - question: "불량 AP는 어떻게 탐지합니까?"
    answer: "패시브 정찰에서 수집한 BSSID 목록을 승인된 AP 목록과 비교합니다. 기업 SSID를 송출하지만 목록에 없는 BSSID는 불량 AP 후보입니다."
  - question: "PMF(Protected Management Frames)가 왜 중요합니까?"
    answer: "PMF는 디인증 및 연결 해제 공격을 방지하여, 공격자가 클라이언트를 강제로 연결 해제시켜 핸드셰이크를 캡처하거나 서비스 거부를 유발하는 것을 막습니다. WPA3에서는 필수입니다."
  - question: "WPA3 전환 모드(Transition Mode)의 위험은 무엇입니까?"
    answer: "전환 모드는 호환성을 위해 SAE와 PSK를 모두 허용합니다. 공격자는 WPA2 전용 비콘 프레임을 송출하여 클라이언트를 강제로 다운그레이드시켜 전방 비밀성(forward secrecy)을 무력화할 수 있습니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["enterprise", "wireless-security", "penetration-testing", "rogue-AP", "WPA2", "WPA3", "PMF", "ALFA-network"]
featureimage: "/images/blog/enterprise-wireless-security-assessment.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

{{< alert "triangle-exclamation" >}}
**법적 고지:** 모든 무선 보안 평가는 명시적이고 서면으로 승인을 받은 네트워크 및 인프라에서만 수행해야 합니다. 승인되지 않은 무선 모니터링, 인젝션, 불량 AP 배치는 대부분의 국가에서 불법입니다. 본 프레임워크에서 설명하는 모든 단계는 자산 소유자가 서명하고 특정 테스트 기간과 승인된 범위를 명시한 계약서가 적절히 체결되어 있다는 것을 전제로 합니다. 승인된 테스트에만 사용하십시오.
{{< /alert >}}

엔터프라이즈 무선 보안 평가는 단순히 "비밀번호를 크랙할 수 있는가"를 묻는 작업이 아닙니다. 철저한 평가는 무선 아키텍처의 모든 계층을 검토합니다. 인증 프로토콜의 강도, 관리 프레임 보호의 무결성, 승인된 AP 인벤토리의 정확성, 게스트 세그먼트에서의 클라이언트 격리 견고성, 그리고 802.1X 인프라가 불량 RADIUS 공격에 대해 갖는 저항력까지 모두 포함됩니다.

{{< tldr >}}
본 프레임워크는 ALFA 무선 어댑터를 사용하여 범위 설정, 불량 AP 탐지, WPA2/WPA3 감사, PMF 테스트, 클라이언트 격리, 802.1X 평가를 다루는 6단계 엔터프라이즈 무선 보안 평가 방법론을 상세히 설명하며, 보고서 양식과 심각도 정의를 함께 제공합니다.
{{< /tldr >}}




본 프레임워크는 엔터프라이즈 환경에서 활동하는 전문 침투 테스트팀이 실제로 수행하는 평가 전체 주기를 다룹니다. 범위 설정 및 사전 참여, 패시브 정찰, 불량 AP 탐지, WPA2/WPA3 핸드셰이크 분석, PMF 검증, 클라이언트 격리 테스트, EAP/RADIUS 평가라는 여섯 개의 순차적 단계로 구성되며, 그 뒤에 보고서 양식과 툴킷 참조가 이어집니다. 모든 단계는 ALFA Network 어댑터로 수행할 수 있도록 설계되었으며, 이 어댑터들은 엔터프라이즈급 무선 테스트에 필요한 모니터 모드 안정성, 인젝션 기능, 멀티밴드 커버리지를 제공합니다.

연례 무선 감사를 의뢰하는 CISO이든, 평가를 준비하는 내부 레드팀이든, 신규 엔터프라이즈 고객을 온보딩하는 외부 침투 테스트 업체이든, 본 프레임워크는 반복 가능하고 방어 가능한 방법론을 제공합니다.

---

## 범위 및 사전 참여 요건

모든 무선 평가의 품질은 단 하나의 패킷을 캡처하기 전에 이미 결정됩니다. 범위가 잘못 설정된 참여는 시간을 낭비하고 법적 노출을 발생시키며, 특정 인프라에 귀속시킬 수 없는 결과물을 만들어냅니다. 잘 작성된 범위 문서는 모호함을 없애고 테스트팀과 고객 모두를 보호합니다.

### 범위 문서에 반드시 포함되어야 할 항목

범위 문서에는 최소한 다음 항목이 열거되어야 합니다:

- **테스트 대상이 되는 모든 SSID**: 기업 SSID, 게스트 SSID, IoT 전용 SSID, 그리고 네트워크 팀이 알고 있는 숨겨진 네트워크를 포함합니다
- **사용 중인 주파수 대역**: 2.4GHz, 5GHz, 6GHz(Wi-Fi 6E) — 각 대역은 서로 다른 AP 모델, 드라이버 동작, 보안 설정을 가질 수 있습니다
- **물리적 경계**: 알려진 AP 배치가 표시된 건물 또는 캠퍼스 지도와 평면도. 특히 다수의 임차인이 있는 건물에서는 인접 SSID가 스캔 결과에 나타날 수 있으므로 중요합니다
- **승인된 AP 인벤토리**: 모든 정당한 액세스 포인트의 MAC 주소(BSSID) 목록으로, 불량 AP 탐지의 기준선으로 사용됩니다
- **승인서**: CISO, CTO 또는 지정된 자산 소유자가 서명하며, 테스트 기간(시작 및 종료 날짜/시간), 테스트팀 구성원의 이름, 그리고 승인된 구체적 활동(패시브 스캐닝, 액티브 인젝션, 디인증, 불량 AP 시뮬레이션)을 명시적으로 포함해야 합니다

### 기본적으로 범위에서 제외되는 항목

서면으로 명시적으로 포함되지 않는 한, 다음은 항상 범위에서 제외됩니다:

- **클라이언트 장비**: 무선 네트워크에 연결되는 노트북, 휴대폰, IoT 엔드포인트. 클라이언트 측 공격(불량 RADIUS를 통한 자격 증명 수집)은 지정된 테스트 장비에서만 수행할 수 있으며, 운영 중인 사용자 장비에는 절대 수행해서는 안 됩니다
- **게스트 네트워크 사용자**: 공개적으로 접근 가능한 게스트 SSID에 연결하는 개인은 보안 테스트의 대상이 될 것을 예상하지 않습니다
- **인접 네트워크**: 공유 건물 내 인접 임차인에 속한 SSID는 패시브 스캔에서 보이더라도 범위에서 제외됩니다

### 법적 주의사항

{{< alert "triangle-exclamation" >}}
**항상 서면 승인을 확보하십시오.** 정확한 테스트 기간(날짜, 시작 시간, 종료 시간, 시간대), 테스트 장비의 이름과 MAC 주소, 그리고 승인된 구체적 기법을 명시해야 합니다. 구두 동의로는 충분하지 않습니다. 서명된 승인서는 참여 파일과 함께 보관하고, 법 집행기관의 연락이 있을 경우를 대비해 테스트 중에도 즉시 제시할 수 있도록 하십시오.
{{< /alert >}}

---

## 1단계: 패시브 정찰

### 목표

패시브 정찰은 단 1바이트도 송신하지 않고 무선 환경의 사실적 기준(ground truth)을 확립합니다. 목표는 다음과 같습니다:

- 범위 내에서 송출되는 모든 AP를 식별합니다. 승인된 인벤토리에 없는 AP도 포함합니다
- SSID, BSSID, 운영 채널, 신호 강도, 보안 설정(암호화 유형, PMF 상태)을 기록합니다
- 프로브 응답을 통해 숨겨진 SSID를 탐지합니다
- 테스트 신뢰성에 영향을 줄 수 있는 동일 채널 및 인접 채널 간섭을 식별합니다

패시브 정찰 중에는 **인젝션하지 않고, 디인증하지 않고, 송신하지 않습니다.** 이 단계는 완전히 청취(listen-only)만 수행합니다.

### 도구

**airodump-ng**는 스냅샷 스캔과 핸드셰이크 캡처에 적합합니다. 더 풍부한 메타데이터를 통한 지속적 로깅에는 **Kismet**이 선호됩니다. 보고서 작성 도구로 가져올 수 있는 구조화된 로그를 생성하고, 시간에 따라 프로브 요청을 장치 신원과 상관시킬 수 있습니다.

```bash
# 모든 대역에 대한 패시브 스캔 — 정찰 중에는 인젝션이나 디인증을 수행하지 마십시오
sudo airodump-ng wlan0mon --band abg -w enterprise_recon

# 포괄적이고 지속적인 로깅을 위한 Kismet
sudo kismet -c wlan0mon
```

Kismet은 `.kismet` SQLite 데이터베이스 파일과 `.pcapng` 캡처를 동시에 기록하여, 평가 기간 전체를 아우르는 지속적인 기록을 남깁니다.

### 기록할 항목

발견된 각 AP에 대해 다음을 기록합니다:

| 항목 | 비고 |
|---|---|
| BSSID | AP 라디오의 MAC 주소 |
| SSID | 네트워크 이름(숨겨진 경우 빈 값) |
| 암호화 | WPA2-PSK, WPA2-Enterprise, WPA3-SAE, WPA3-Enterprise, Open |
| 채널 | 2.4GHz와 5GHz 양쪽에 나타나는 듀얼 라디오 AP에 주의 |
| 신호(dBm) | 물리적 위치 추정에 유용 |
| PMF 상태 | 비콘 프레임의 RSN IE에서 추출: Required / Capable / Disabled |
| 벤더 | BSSID OUI로부터 유추 — 승인되지 않은 소비자용 장비를 식별하는 데 유용 |

### 어댑터 권장사항

- **AWUS036AXML** — 트라이밴드(2.4/5/6GHz)로, 6GHz 채널에서 운영되는 Wi-Fi 6E AP를 탐지하는 데 필수적입니다. Wi-Fi 6E 인프라를 도입한 최신 엔터프라이즈 환경에서 필수 장비입니다
- **AWUS036ACH** — 듀얼밴드(2.4/5GHz), 안정적인 RTL8812AU 칩셋을 탑재하여, 6GHz를 사용하지 않고 기존 도구와의 최대 호환성이 중요한 환경에 적합합니다

---

## 2단계: 불량 AP 탐지

불량 액세스 포인트란 환경 내에서 운영되지만 승인된 AP 인벤토리에 없는 AP를 말합니다. 운영상 관련이 있는 두 가지 범주가 있습니다:

1. **내부 네트워크에 연결된 비승인 AP** — 선의의 직원이 소비자용 라우터를 연결하거나, 물리적 접근 권한을 획득한 공격자가 이더넷 포트에 숨겨진 AP를 설치하는 경우입니다. 이러한 AP는 내부 네트워크에 연결되어 있으며 모든 경계 제어를 우회합니다
2. **이블 트윈(Evil Twin) AP** — 정당한 것처럼 보이는 SSID(기업 SSID와 동일하거나 매우 유사한 이름)를 송출하는 AP로, 공격자가 자격 증명을 수집하거나 중간자 공격을 수행하기 위해 운영합니다. 일반적으로 내부 네트워크에는 연결되어 있지 않습니다

### 탐지 방법

패시브 정찰에서 얻은 BSSID 목록을 범위 설정 단계에서 제공된 승인 AP 인벤토리와 비교합니다. 기업 SSID를 송출하지만 인벤토리에 없는 BSSID는 불량 AP 후보입니다.

```bash
# 스캔 출력에서 기업 SSID를 필터링하여 이를 송출하는 모든 AP를 분리
sudo airodump-ng wlan0mon | grep "CorporateSSID"

# 발견된 BSSID를 승인 목록과 비교 (diff 사용 예시)
# airodump의 BSSID 열을 discovered.txt에 저장하고, 승인 목록을 authorized.txt에 저장
diff <(sort discovered.txt) <(sort authorized.txt)
```

`discovered.txt`에는 있지만 `authorized.txt`에는 없는 BSSID는 모두 발견 사항(finding)입니다.

### 디인증 기반 탐지(승인된 경우)

디인증이 범위에 명시적으로 포함된 경우, 클라이언트의 재연결 동작을 이용해 의심스러운 AP가 내부 네트워크에 연결되어 있는지 판단할 수 있습니다. 의심 AP에서 클라이언트를 디인증시키고, 해당 클라이언트가 동일 SSID의 정당한 AP로 재연결하는지 관찰합니다. 클라이언트가 원활하게 로밍하면 불량 AP가 동일한 백엔드 네트워크를 공유할 가능성이 있습니다. 클라이언트가 재연결에 실패하면 불량 AP는 격리되어 있을 가능성이 높습니다(이블 트윈 시나리오).

### WIDS 검증

조직이 무선 침입 탐지/방지 시스템(WIDS/WIPS)을 도입한 경우, 이 단계에는 WIDS가 테스트용 불량 AP를 허용 가능한 시간 범위 내에 탐지하는지 검증하는 통제된 테스트가 포함되어야 합니다. 인벤토리에 없는 MAC 주소를 사용해 기업 SSID로 테스트용 AP를 배치하고 탐지 지연 시간을 측정합니다. 60초를 초과하는 탐지 시간은 탐지 범위에 의미 있는 공백이 있음을 나타냅니다.

---

## 3단계: WPA2/WPA3 핸드셰이크 분석

### WPA2: 4-웨이 핸드셰이크 캡처

WPA2 4-웨이 핸드셰이크를 캡처하면 네트워크의 패스프레이즈가 조직의 비밀번호 복잡도 정책을 충족하는지 오프라인에서 검증할 수 있습니다. 이는 패스프레이즈 크래킹을 평가 목표로 승인하는 것이 아니라, 준수 여부를 검증하는 작업입니다. 즉, 캡처된 해시가 범용 하드웨어를 사용하는 공격자에 의해 합리적인 시간 내에 크랙될 수 있는가를 확인하는 것입니다.

```bash
# 6번 채널의 특정 AP를 대상으로 캡처를 파일에 기록
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w handshake wlan0mon

# 캡처한 .cap을 오프라인 감사를 위해 hashcat 형식으로 변환
hcxpcapngtool -o hash.hc22000 handshake-01.cap
```

생성된 `.hc22000` 해시를 조직이 승인한 워드리스트와 규칙 세트에 대해 오프라인 비밀번호 감사기에 제출합니다. 패스프레이즈가 일반적인 비밀번호 목록(rockyou, 회사명 변형, 키보드 패턴)에 대해 복구 가능하다면, 해당 SSID의 네트워크 접근 권한에 따라 Medium 또는 High 등급으로 보고합니다.

### WPA3: SAE 및 전환 모드

WPA3는 SAE(Simultaneous Authentication of Equals)를 사용하여 전방 비밀성(forward secrecy)을 제공하고 오프라인 사전 공격에 대한 저항력을 갖습니다. 그러나 많은 조직이 WPA2 클라이언트와의 호환성을 유지하기 위해 **WPA3 전환 모드**를 도입하고 있으며, 이 모드는 SAE와 PSK 인증을 모두 허용합니다. 동일한 SSID에 대해 WPA2 전용 비콘을 제시하여 공격자가 WPA3 클라이언트를 WPA2로 강제 다운그레이드시킬 수 있는지 테스트합니다. 다운그레이드가 성공하면 High 등급으로 보고합니다.

WPA3 관련 테스트에 대한 자세한 내용은 [WPA3 보안 테스트 가이드](/ko/blog/wpa3-security-testing-alfa-2026/)를 참조하십시오.

---

## 4단계: PMF(Protected Management Frames) 테스트

### PMF가 중요한 이유

802.11w Protected Management Frames(PMF)는 디인증 및 연결 해제 공격을 방지합니다. PMF가 없으면 공격자가 위조된 디인증 프레임을 임의의 클라이언트에 전송하여 강제로 연결을 해제시키고, 핸드셰이크 캡처, 불량 AP를 통한 자격 증명 수집, 혹은 단순한 서비스 거부를 유발할 수 있습니다. PMF는 WPA3에서는 필수이며 WPA2에서는 선택 사항이지만(강력히 권장됩니다).

### 테스트 절차

테스트 대상인 각 SSID에 연결된 테스트 클라이언트를 대상으로 디인증 공격을 시도합니다. 그 결과로 PMF가 적용되고 있는지 확인할 수 있습니다:

```bash
# AP에 대한 디인증 플러딩 시도
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF wlan0mon

# 연결된 테스트 클라이언트가 연결이 끊어지면: PMF가 적용되지 않음 — 보고 대상 발견 사항
# 테스트 클라이언트가 연결을 유지하면: PMF 적용됨 — 통과
```

이 테스트는 항상 지정된 테스트 장비에서만 수행하고, 운영 중인 클라이언트에는 절대 수행하지 마십시오.

### PMF 상태 보고

각 SSID와 그 PMF 적용 수준을 다음과 같이 문서화합니다:

| SSID | 암호화 | PMF 상태 | 발견 사항 |
|---|---|---|---|
| Corp-WiFi | WPA2-Enterprise | Capable (필수 아님) | Medium |
| Corp-WiFi-6E | WPA3-Enterprise | Required | Pass |
| CorpGuest | WPA2-PSK | Disabled | High |

**모든 SSID에서 PMF가 Disabled**이면 최소 Medium 등급입니다. 내부 리소스에 접근 가능한 기업 SSID에서 PMF가 Disabled인 경우는 High 등급입니다. PMF 테스트 방법론의 전체 내용은 [패킷 인젝션 가이드](/ko/blog/packet-injection-guide/)를 참조하십시오.

---

## 5단계: 클라이언트 격리 테스트

### 게스트 네트워크 격리

게스트 SSID는 클라이언트 격리를 강제해야 합니다. 즉, 한 게스트 클라이언트가 다른 게스트 클라이언트와 직접 통신할 수 없어야 합니다. 격리가 없으면 게스트 네트워크상의 악의적인 사용자가 ARP 포이즈닝, LLMNR/NBT-NS 스푸핑, 혹은 다른 게스트에 대한 직접 공격을 수행할 수 있습니다.

**테스트 절차:**

1. 전용 테스트 장비 두 대(운영 중인 사용자 장비는 제외)를 게스트 SSID에 연결합니다
2. 장비 A에서 장비 B의 IP 주소로 ICMP 핑을 시도합니다
3. 장비 A에서 게스트 서브넷에 대한 ARP 스캔을 시도합니다

테스트 장비 간 핑이 성공하는 등 클라이언트 격리에 실패한 게스트 SSID는 High 등급입니다.

### 게스트-내부망 격리

게스트 네트워크가 내부 네트워크 범위에 도달할 수 없는지 검증합니다:

```bash
# 게스트 SSID의 테스트 장비에서 내부 네트워크 범위를 ARP 스캔
sudo arp-scan -l --interface wlan0
# 내부 범위에서 응답이 없으면 = 통과
# 내부 범위에서 응답이 있으면 = Critical 발견 사항
```

또한, 내부 호스트명에 대한 DNS 해석과 내부 관리 인터페이스(SSH, HTTP 관리 패널)로의 직접 TCP 연결을 시도합니다. 게스트 세그먼트에서 내부 인프라로의 연결이 성공하면 Critical 등급입니다.

---

## 6단계: EAP/RADIUS 평가(엔터프라이즈 SSID)

### 802.1X 인증과 불량 RADIUS 공격

WPA2-Enterprise와 WPA3-Enterprise는 802.1X EAP 인증을 사용하며, 클라이언트는 RADIUS 서버에 인증을 요청합니다. 핵심 보안 통제는 **서버 인증서 검증**입니다. 각 클라이언트는 자격 증명을 제출하기 전에 반드시 RADIUS 서버의 인증서를 검증해야 합니다. 클라이언트가 인증서를 검증하지 않으면, 공격자는 불량 RADIUS 서버를 갖춘 불량 AP를 배치하여 NTLMv2 해시나 EAP 자격 증명을 수집할 수 있습니다.

### 테스트 절차

`hostapd-wpe`를 사용해 기업 SSID로 불량 AP를 배치합니다. 이는 모든 인증 시도를 로깅하는 불량 RADIUS 서버를 갖춘 802.1X 지원 AP를 생성합니다:

```bash
# hostapd-wpe 설치
sudo apt install hostapd-wpe

# 대상 SSID와 채널로 구성
# /etc/hostapd-wpe/hostapd-wpe.conf를 대상 SSID/채널 정보로 편집
sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf

# 출력에서 캡처된 자격 증명 해시를 모니터링
```

**Critical 발견 사항:** 이전에 운영 중인 802.1X SSID에 연결했던 클라이언트를 포함하여 어떤 클라이언트든 인증서 경고를 표시하지 않고 불량 RADIUS에 연결하거나, 사용자가 인증서 경고를 수락하여 자격 증명이 캡처된 경우 Critical 등급입니다. 이는 클라이언트가 인증서 피닝이나 올바른 체인 검증을 강제하지 않음을 나타냅니다.

**대응 방안:** MDM(모바일 장치 관리) 구성 프로필을 통해 정확한 RADIUS 서버 인증서 또는 발급 CA를 지정하는 인증서 피닝을 배치합니다. 최종 사용자가 예상치 못한 인증서 알림을 거부하도록 보안 인식 교육을 받도록 합니다.

---

## 평가 툴킷 참조

다음 도구들은 엔터프라이즈 무선 평가 작업의 전체 흐름을 다룹니다. 모두 모니터 모드에서 ALFA Network 어댑터와 호환됩니다. 어댑터 설정 방법은 [Kali Linux에서 모니터 모드 활성화하기](/ko/blog/enable-monitor-mode-kali-linux/) 가이드를 참조하십시오.

| 도구 | 용도 | 권장 어댑터 | 주요 명령어 |
|---|---|---|---|
| airodump-ng | 패시브 스캐닝, 핸드셰이크 캡처 | 모든 ALFA(AWUS036AXML / AWUS036ACH) | `sudo airodump-ng wlan0mon --band abg` |
| hcxdumptool | PMKID 캡처, 패시브 핸드셰이크 수집 | AWUS036AXML(Wi-Fi 6E) | `sudo hcxdumptool -i wlan0mon -o out.pcapng` |
| hcxpcapngtool | 캡처 파일을 hashcat 형식으로 변환 | 해당 없음(후처리) | `hcxpcapngtool -o hash.hc22000 cap.pcapng` |
| Kismet | 지속적 로깅, SSID/클라이언트 상관 분석 | AWUS036ACH | `sudo kismet -c wlan0mon` |
| aireplay-ng | PMF 테스트, 디인증 인젝션 | AWUS036ACH | `sudo aireplay-ng --deauth 10 -a BSSID wlan0mon` |
| hostapd-wpe | EAP 테스트용 불량 AP / 불량 RADIUS | AWUS036ACH | `sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf` |
| Wireshark | 캡처 파일의 패킷 단위 분석 | 캡처 파일을 통해 모든 장비 | `wireshark -r handshake-01.cap` |
| arp-scan | 게스트/내부망 격리 검증 | 모든 장비 | `sudo arp-scan -l --interface wlan0` |

---

## 보고서 양식

### 경영진 요약

경영진 요약은 무선 보안에 대한 배경지식이 없는 CTO나 CISO도 읽을 수 있어야 합니다. 다음 항목을 반드시 포함해야 합니다:

- **전체 위험 등급**: Critical / High / Medium / Low — 확인된 가장 높은 심각도의 발견 사항을 기준으로 산정
- 심각도 등급별 **주요 발견 사항 수**
- **컴플라이언스 격차 설명**: 관련 표준(PCI-DSS 4.0 Requirement 11.2, ISO/IEC 27001 A.13.1, NIST 800-153) 참조 및 평가 대상 무선 환경이 해당 요구사항을 충족하는지 여부
- **즉시 조치 항목**: 다음 영업일 전까지 대응이 필요한 발견 사항

### 발견 사항 테이블

모든 기술적 발견 사항은 각 항목을 심각도, 영향을 받는 인프라, 구체적인 대응 권고안에 매핑한 표준화된 표로 제시해야 합니다:

| ID | 심각도 | 발견 사항 | 영향받는 SSID | 권고안 |
|---|---|---|---|---|
| WL-01 | Critical | 게스트 SSID에 클라이언트 격리가 없음; 테스트 장비가 직접 통신함 | CorpGuest | WLAN 컨트롤러에서 AP 클라이언트 격리를 활성화하고 재테스트로 검증 |
| WL-02 | Critical | 802.1X 클라이언트가 인증서 경고 없이 불량 RADIUS에 연결됨 | Corp-WiFi | MDM을 통한 인증서 피닝 배치; RADIUS 서버 CA 신뢰 앵커 구성 |
| WL-03 | High | 기업 SSID에서 PMF가 Disabled; 디인증 공격 성공 | Corp-WiFi | 모든 WPA2 SSID에서 PMF Required 활성화; 하드웨어가 지원하는 경우 WPA3로 업그레이드 |
| WL-04 | High | 인벤토리에 없는 BSSID로 기업 SSID를 송출하는 불량 AP 탐지됨 | Corp-WiFi-5G | 물리적 AP 조사; 알려지지 않은 BSSID에 대한 WIDS 알림 배치 |
| WL-05 | Medium | WPA2 패스프레이즈가 4시간 이내에 일반 사전으로 복구 가능 | Corp-IoT | 16자 이상의 무작위 패스프레이즈 적용; 분기별 교체 |
| WL-06 | Low | 비콘 OUI 및 프로브 응답으로 AP 벤더/모델을 식별 가능 | 전체 | 위협 모델이 필요로 하는 경우 AP 핑거프린트 난독화 고려 |

### 무선 발견 사항의 심각도 정의

| 심각도 | 정의 | 예시 |
|---|---|---|
| Critical | 자격 증명 탈취나 내부 네트워크 접근으로 이어지는 즉각적이고 악용 가능한 경로 | 암호화 없는 개방형 SSID, 게스트-내부망 침투, 802.1X 불량 RADIUS 성공 |
| High | 신속한 대응이 필요한 중대한 통제 실패 | PMF Disabled 상태의 WPA2, 네트워크상 불량 AP 확인, WPA3 다운그레이드 공격 성공 |
| Medium | 위험을 증가시키지만 악용을 위해 추가 조건이 필요한 통제 공백 | 취약한 패스프레이즈 정책, 다운그레이드 방지가 없는 WPA3 전환 모드 |
| Low | 정보성 또는 심층 방어(defense-in-depth) 공백 | AP 모델 핑거프린팅, SSID 정보 노출 |

---

{{< faq >}}

## 관련 자료

- [패킷 인젝션 가이드: aireplay-ng로 WiFi 어댑터 테스트하기](/ko/blog/packet-injection-guide/)
- [ALFA 어댑터로 수행하는 WPA3 보안 테스트(2026)](/ko/blog/wpa3-security-testing-alfa-2026/)
- [Kali Linux에서 모니터 모드 활성화하기](/ko/blog/enable-monitor-mode-kali-linux/)

## 참고 문헌

1. [aircrack-ng 공식 문서](https://www.aircrack-ng.org/)
2. [Wi-Fi Alliance WPA3 사양](https://www.wi-fi.org/discover-wi-fi/wpa3)
3. [IEEE 802.11w Protected Management Frames 표준](https://standards.ieee.org/ieee/802.11w/4454/)
4. [NIST SP 800-153 무선 보안 가이드](https://csrc.nist.gov/publications/detail/sp/800-153/final)
5. [Kismet 무선 탐지 도구](https://www.kismetwireless.net/)
