---
title: "패킷 인젝션이란 무엇인가? Kali Linux에서 WiFi 어댑터 호환성 테스트하기"
description: "WiFi 패킷 인젝션이 무엇인지, 왜 특정 어댑터가 필요한지, aireplay-ng로 ALFA Network 어댑터를 테스트하는 방법, 그리고 Kali Linux에서 인젝션을 지원하는 칩셋을 알아봅니다."
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "WiFi 패킷 인젝션이란 무엇입니까?"
    answer: "패킷 인젝션은 어댑터가 임의의 802.11 프레임을 무선 매체로 직접 전송할 수 있는 능력으로, aireplay-ng와 같은 도구가 관리, 제어, 데이터 프레임을 구성하고 전송할 수 있게 해줍니다."
  - question: "대부분의 어댑터가 패킷 인젝션을 지원하지 못하는 이유는 무엇입니까?"
    answer: "제약은 드라이버에 있으며 하드웨어에 있지 않습니다. 소비자용 드라이버는 표준 운영 모델에 따라 송신 프레임을 검증합니다. 드라이버가 인젝션을 지원하려면 mac80211 raw TX 경로를 명시적으로 활성화해야 합니다."
  - question: "내 어댑터가 패킷 인젝션을 지원하는지 어떻게 테스트합니까?"
    answer: "먼저 모니터 모드를 활성화한 후 aireplay-ng --test wlan0mon을 실행합니다. 출력에 Injection is working!이 표시되면 인젝션이 확인된 것입니다. 성공률 80% 이상이면 신뢰할 수 있습니다."
  - question: "어떤 ALFA 어댑터가 패킷 인젝션을 지원합니까?"
    answer: "AWUS036ACH(RTL8812AU)와 AWUS036ACM(MT7612U)은 올바른 드라이버와 함께 Kali Linux에서 완전히 지원합니다. AWUS036AXML(MT7921AUN(N))은 커널 6.16 이전에서 인젝션이 동작했다는 커뮤니티 보고가 있으나, 자사 stock 커널 6.17 실측에서는 인젝션 테스트가 통과하지 못했습니다(monitor, AP, WPA3는 사용 가능). 인젝션이 필요하면 ACH, EACS, ACS, AX를 사용하세요."
  - question: "패킷 인젝션 성공률이 50% 미만일 때 어떻게 개선합니까?"
    answer: "대상 AP에 더 가까이 이동하고, 모니터 인터페이스를 동일한 채널로 고정하며, TX Power 설정을 확인하고, 드라이버가 배포판 기본 드라이버가 아니라 aircrack-ng 버전인지 확인하십시오."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["packet-injection", "aireplay-ng", "kali-linux", "wifi-adapter", "RTL8812AU", "ALFA-Network"]
featureimage: "/images/blog/packet-injection-guide.webp"
---
패킷 인젝션 — 정식 명칭으로는 **802.11 프레임 인젝션** — 은 무선 어댑터가 자체 네트워크 스택에서 생성되지 않은 프레임을 포함하여 임의의 802.11 프레임을 무선 매체로 전송할 수 있는 능력입니다. 정상적인 동작에서는 무선 드라이버가 OS가 정당하게 생성한 프레임, 즉 연결 요청이나 연결된 네트워크용 데이터 프레임 등만 구성하고 전송합니다. 패킷 인젝션은 이러한 제약을 우회하여, `aireplay-ng`와 같은 도구가 관리, 제어, 데이터 등 모든 프레임 유형을 임의의 내용, 출발지 주소, 목적지 주소로 구성하고 전송할 수 있게 합니다.

{{< alert "triangle-exclamation" >}}
**법적 고지:** 패킷 인젝션과 무선 모니터링은 본인이 소유하거나 명시적으로 서면 승인을 받은 네트워크에서만 수행해야 합니다. 승인되지 않은 무선 통신 감청은 대부분의 국가에서 불법입니다. 본 가이드의 모든 예시는 **승인된 침투 테스트 및 교육용 실습 환경에서만** 사용해야 합니다.
{{< /alert >}}

## 패킷 인젝션이란 무엇인가?

{{< tldr >}}
패킷 인젝션은 임의의 802.11 프레임을 전송할 수 있는 능력으로, 하드웨어가 아니라 드라이버에 의해 제약됩니다. RTL8812AU, MT7612U 칩셋을 탑재한 ALFA 어댑터는 각 칩셋에 맞는 드라이버(각각 rtw88_8812au, mt76x2u)로 이를 완전히 지원합니다. MT7921AUN(N)(AWUS036AXML)은 최신 커널에서는 예외입니다(아래 칩셋 설명 참조).
{{< /tldr >}}


패킷 인젝션은 무선 어댑터가 임의의 802.11 프레임을 전송할 수 있도록 하는 핵심 기능으로, 디인증 공격과 핸드셰이크 캡처의 토대가 됩니다. 이를 위해서는 지원되는 칩셋과 드라이버가 필요합니다.





이 기능은 다음과 같은 여러 범주의 무선 보안 평가에 필수적입니다:

- **WPA/WPA2 핸드셰이크 캡처 가속** — 디인증 프레임을 전송하면 클라이언트가 재인증을 수행하게 되어, 새로운 4-웨이 핸드셰이크가 생성되고 이를 캡처하여 오프라인으로 분석할 수 있습니다
- **WPA 핸드셰이크 검증** — 캡처된 핸드셰이크 파일이 완전하며 오프라인 크래킹에 사용 가능한지 확인합니다
- **재생 공격(Replay Attack)** — 캡처한 ARP 패킷을 재전송하여 WEP 크래킹(레거시 테스트 환경)을 위한 IV(초기화 벡터) 트래픽을 생성합니다
- **이블 트윈/불량 AP 구성** — 비콘 및 프로브 응답 프레임을 인젝션하여 액세스 포인트를 시뮬레이션합니다
- **DoS 테스트** — 승인된 테스트 조건에서 디인증 플러딩에 대한 네트워크의 대응을 평가합니다

> **법적 고지:** 본인이 소유하거나 명시적으로 서면 허가를 받지 않은 네트워크나 장비에 대한 패킷 인젝션은 대부분의 국가에서 불법입니다. 본 문서에서 설명하는 모든 기법은 승인된 침투 테스트, 본인 소유 장비에 대한 보안 연구, 학술 연구 목적으로만 사용해야 합니다.

---

## 대부분의 어댑터가 패킷 인젝션을 할 수 없는 이유

제약 요인은 주로 하드웨어가 아니라 **드라이버**입니다. 소비자용 어댑터를 위한 표준 무선 드라이버는 802.11 표준의 정상적인 운영 모델을 준수하도록 작성됩니다. 드라이버는 송신 프레임을 검증하고, 연결 상태를 강제하며, 예상되는 흐름에 맞지 않는 프레임을 거부합니다.

패킷 인젝션을 지원하려면 드라이버가 이러한 검증을 우회하는 raw 프레임 전송 경로를 노출해야 합니다. 커널의 **mac80211** 서브시스템은 `IEEE80211_HW_SUPPORTS_RAW_TX` 플래그를 통해 이 기능을 제공하지만, 드라이버가 이를 명시적으로 활성화한 경우에만 가능합니다. 대부분의 소비자용 어댑터 벤더 드라이버는 raw TX를 활성화하지 않습니다. 이를 필요로 하는 소비자용 사례가 없고, 활성화할 경우 오남용 가능성이 생기기 때문입니다.

또한 일부 칩셋은 **독점 펌웨어**를 사용하여 MAC 계층을 내부적으로 처리하므로, 드라이버가 원하더라도 호스트 드라이버에서 임의의 프레임을 인젝션할 수 없습니다. 이는 엔터프라이즈 또는 소비자용 노트북을 위해 설계된 Broadcom 및 Intel 칩에서 흔히 볼 수 있습니다.

---

## 패킷 인젝션을 지원하는 칩셋

다음 칩셋들은 Kali Linux에서 안정적으로 패킷 인젝션을 지원하는 것으로 잘 알려져 있으며, ALFA Network 어댑터에 사용됩니다.

### Realtek RTL8812AU

2024~2026년 기준 침투 테스트에서 가장 널리 사용되는 칩셋입니다. 듀얼밴드(2.4/5GHz), 802.11ac를 지원하며, 커널 6.13부터는 내장 드라이버인 `rtw88_8812au`로 지원됩니다. 모니터 모드와 인젝션 모두 안정적으로 동작합니다.


### Mediatek MT7612U

듀얼밴드 802.11ac 칩셋으로, 커널에 내장된 `mt76x2u` 드라이버로 잘 관리되고 있습니다. 모니터 모드와 인젝션은 업스트림 커널에서 지원되므로, 대부분의 최신 Kali Linux 버전에서는 별도의 외부 드라이버 설치가 필요하지 않습니다.


### Mediatek MT7921AU(N) (Wi-Fi 6E)

이 목록 중 가장 최신 칩셋으로, AWUS036AXML에 사용됩니다. 802.11ax 기반 2.4/5/6GHz 트라이밴드를 지원합니다. `mt7921u` 드라이버는 커널 5.18부터 메인라인에 내장되어 있습니다. 모니터 모드와 인젝션 자체는 지원되지만, 자사 실측 결과 stock 커널 6.17 환경에서는 AWUS036AXML/AXM의 패킷 인젝션 테스트가 통과하지 못했습니다. 최신 드라이버인 만큼 배포판에 따라 예외적인 문제가 발생할 수 있으므로, 실제 평가에 투입하기 전 반드시 `aireplay-ng --test`로 직접 확인하시기 바랍니다.

---

## aireplay-ng로 패킷 인젝션 테스트하기

실제 평가에서 인젝션에 의존하기 전에, 항상 사용 중인 어댑터와 드라이버 조합이 올바르게 동작하는지 확인해야 합니다. 인젝션 지원 여부는 커널 버전과 드라이버 리비전에 따라 달라집니다.

### 사전 준비

어댑터가 이미 모니터 모드여야 합니다. 그렇지 않다면 먼저 활성화하십시오:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

모니터 인터페이스가 생성되었는지 확인합니다:

```bash
iwconfig
# Mode:Monitor 를 확인
```

### 인젝션 테스트 실행

```bash
sudo aireplay-ng --test wlan0mon
```

### 성공 출력 예시

```
09:15:34  Trying broadcast probe requests...
09:15:34  Injection is working!
09:15:36  Found 3 APs

09:15:36  Trying directed probe requests...
09:15:36   AA:BB:CC:DD:EE:01 - channel: 6 - 'HomeNetwork'
09:15:37  Ping (min/avg/max): 1.153ms/5.464ms/12.214ms Power: -62
09:15:37  29/30: 96%

09:15:37   AA:BB:CC:DD:EE:02 - channel: 11 - 'OfficeWiFi'
09:15:38  Ping (min/avg/max): 2.101ms/6.322ms/14.881ms Power: -71
09:15:38  28/30: 93%
```

정상적으로 동작하는 인젝션 환경은 **"Injection is working!"** 메시지와 함께 인접 액세스 포인트에 대한 성공적인 핑 비율을 보여줍니다. 80% 이상이면 일반적으로 신뢰할 수 있습니다. 50% 미만이면 간섭, 거리 문제, 또는 드라이버 문제를 의심해야 합니다.

### 실패 출력 예시

```
09:15:34  Trying broadcast probe requests...
09:15:36  No Answer...
09:15:36  Injection is working! (RTL)
09:15:36  Trying directed probe requests...
09:15:37   AA:BB:CC:DD:EE:01 - channel: 6 - 'HomeNetwork'
09:15:39  Failed!
```

또는 더 완전한 실패 시나리오의 경우:

```
09:15:34  Trying broadcast probe requests...
09:15:46  No Answer...
09:15:46  Injection is NOT working!
```

"Injection is NOT working!"은 확정적인 실패를 의미합니다. 어댑터가 인젝션을 지원하지 않거나, 드라이버가 올바르게 설치되지 않은 것입니다.

---

## 패킷 인젝션을 지원하는 ALFA 어댑터

모든 주요 [ALFA Network](/ko/products/alfa/) 어댑터 모델은 Kali Linux에서 올바른 드라이버를 사용할 경우 패킷 인젝션을 지원합니다.

| 모델 | 칩셋 | 밴드 | 인젝션 지원 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | 2.4 / 5 GHz | ✅ 완전 지원(드라이버: rtw88_8812au, 커널 6.13+ 내장) |
| AWUS036AXML | MT7921AUN(N) | 2.4 / 5 / 6 GHz | ⚠️ 드라이버는 mt7921u(커널 5.18+ 내장)로 지원되나, 자사 실측 결과 stock 커널 6.17에서 인젝션 테스트 미통과 — 사용 전 반드시 직접 확인 필요 |
| AWUS036ACM | MT7612U | 2.4 / 5 GHz | ✅ 완전 지원(드라이버: mt76x2u) |

---

## 흔한 인젝션 테스트 실패와 해결 방법

### 모니터 모드 시작 직후 "Injection is NOT working!"이 나타나는 경우

가장 흔한 원인은 NetworkManager나 wpa_supplicant가 여전히 백그라운드에서 실행 중인 경우입니다. 이를 종료하고 다시 시도하십시오:

```bash
sudo airmon-ng check kill
sudo airmon-ng stop wlan0mon
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

### 성공률이 낮은 경우(50% 미만)

- **거리:** 근처 액세스 포인트에 더 가까이 이동한 후 다시 테스트합니다
- **채널 불일치:** 모니터 인터페이스를 테스트 대상 AP와 동일한 채널로 고정합니다: `sudo iwconfig wlan0mon channel 6`
- **드라이버 문제:** 외부(out-of-tree) 드라이버를 재설치합니다. RTL8812AU의 경우: `https://github.com/aircrack-ng/rtl8812au`에서 클론한 후 `sudo make dkms_install`을 실행합니다

### 커널 모듈이 로드되지 않는 경우

```bash
sudo modprobe -r rtl8812au
sudo modprobe rtl8812au
dmesg | tail -20
```

`dmesg`에서 모듈 관련 오류 메시지를 확인하십시오. 펌웨어 파일 누락은 흔한 문제이며, `firmware-linux-nonfree` 또는 칩셋별 펌웨어 패키지를 설치하십시오.

### 연결 후 어댑터가 나타나지 않는 경우

```bash
lsusb
dmesg | tail -30
```

`lsusb`에는 장치가 표시되지만 `ip link`에 무선 인터페이스가 나타나지 않는다면, 드라이버가 바인딩에 실패한 것입니다. 이는 대개 드라이버가 설치되지 않았거나 커널 모듈 로드에 실패했음을 의미합니다.

---

## 활용 사례: 승인된 테스트에서 인젝션 적용하기

### WPA2 핸드셰이크 캡처

전문 침투 테스트에서 가장 흔한 인젝션 활용 사례입니다. airodump-ng로 대상 AP의 채널에서 캡처를 시작한 후, aireplay-ng로 디인증 프레임을 전송하여 클라이언트의 재연결을 강제합니다:

```bash
# 터미널 1: 캡처
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w handshake wlan0mon

# 터미널 2: 디인증 (특정 클라이언트에 디인증 프레임 5개 전송)
sudo aireplay-ng --deauth 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
```

터미널 1로 돌아가 airodump-ng 화면 우상단에 `WPA handshake: AA:BB:CC:DD:EE:FF` 메시지가 나타나는지 확인합니다.

### PMKID 공격 — 디인증이 필요 없음

2018년 이후, PMKID 공격 방식을 사용하면 **디인증 프레임을 전송하지 않고도** WPA2 키 오프라인 테스트에 충분한 데이터를 캡처할 수 있어, 연결된 클라이언트가 거의 없거나 전혀 없는 네트워크에서도 훨씬 은밀하고 효과적입니다:

```bash
# 도구 설치
sudo apt install hcxdumptool hcxtools

# PMKID 캡처 (패시브, 디인증 없음)
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1

# hashcat용으로 변환
hcxpcapngtool -o hash.hc22000 capture.pcapng

# 오프라인 크래킹 (활성 네트워크 연결이 필요 없음)
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

### 디인증 테스트(DoS 평가)

보안 평가자는 디인증 플러딩을 전송하여 무선 복원력을 테스트하고, 클라이언트가 안전하게 재연결되는지, AP가 공격을 로깅하거나 완화하는지를 평가합니다. 반드시 서명된 작업 명세서(SOW) 하에서만 수행합니다.

---

## 엔터프라이즈 보안팀에 주는 의미

패킷 인젝션 테스트는 무선 침투 테스트 참여의 표준 구성 요소입니다. 엔터프라이즈 IT를 위한 주요 활용 사례는 다음과 같습니다:

- **불량 AP 탐지:** 기업 주파수에서 비승인 AP가 송출되고 있는지 확인합니다
- **WPA2 핸드셰이크 캡처 감사:** 비밀번호 강도 정책 준수 여부를 평가합니다
- **PMF(Protected Management Frames) 검증:** 모든 엔터프라이즈 AP에서 802.11w가 적용되고 있는지 확인합니다. 디인증 공격이 성공하면 PMF가 활성화되지 않은 것입니다
- **클라이언트 격리 테스트:** 게스트 네트워크에서 클라이언트 간 트래픽이 차단되는지 확인합니다

완전한 엔터프라이즈 무선 보안 평가 프레임워크는 [엔터프라이즈 무선 보안 평가](/ko/blog/enterprise-wireless-security-assessment/)를 참조하십시오.

---

## 책임 있는 사용

패킷 인젝션은 강력한 기능입니다. 승인된 침투 테스트에서의 정당한 활용 사례는 핸드셰이크 캡처, 무선 보안 통제 검증, 클라이언트 동작 테스트 등으로 잘 확립되어 있습니다. 오남용은 해롭고 불법입니다.

항상 다음을 확보하십시오:
- 테스트 전 네트워크 소유자로부터의 서면 승인
- 무선 테스트를 명시적으로 포함하는 범위가 명확한 작업 명세서(SOW)
- 무선 보안 테스트를 규율하는 현지 법률에 대한 인식

본 문서에서 설명한 도구(aireplay-ng, airodump-ng, aircrack-ng)는 승인된 보안 테스트를 위해 Kali Linux에 포함되어 있습니다. 그 목적에 맞게 사용하십시오.

---

{{< faq >}}

패킷 인젝션 지원이 확인된 무선 어댑터를 찾으신다면, 대만 ALFA Network 공식 총판인 [Yopitek의 ALFA Network 제품 라인](/ko/products/alfa/)을 둘러보십시오.

## 참고 문헌

1. [aircrack-ng 공식 웹사이트 및 문서](https://www.aircrack-ng.org/)
2. [aireplay-ng 사용 가이드](https://www.aircrack-ng.org/doku.php?id=aireplay-ng)
3. [Kali Linux 공식 문서](https://www.kali.org/docs/)
4. [Linux mac80211 서브시스템 문서](https://wireless.wiki.kernel.org/en/developers/Documentation/mac80211)
5. [IEEE 802.11 표준 자료](https://standards.ieee.org/ieee/802.11/)
