---
title: "AWUS036AXM 단일 카드 실측: MediaTek MT7921AU(Wi-Fi 6 2x2)의 ASUS GX10 + Ubuntu 24.04(ARM64) Monitor · AP · WPA3 성능과 Injection 한계"
slug: awus036axm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axm
  - mt7921
  - mt7921u
  - wifi-6
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - ap-mode
  - wpa3-sae
  - monitor-mode
description: "AWUS036AXM(mt7921u)를 ASUS GX10 / Ubuntu 24.04 ARM64에서 실측: monitor, AP, WPA3는 사용 가능하지만 packet injection은 실패하여 침투 테스트에 부적합, 순수 AP와 접속 용도로 포지셔닝."
faq:
  - question: "AWUS036AXM으로 패킷 인젝션(packet injection)을 할 수 있나요?"
    answer: "우리의 테스트 플랫폼(ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia)에서는 불가능합니다. aireplay-ng --test가 2.4 GHz와 5 GHz 모두 No Answer, Found 0 APs를 보고하며, 따라서 deauth도 WPA handshake 캡처도 불가능합니다. 근본 원인은 kernel 6.16+의 mac80211 chanctx 회귀(regression)이며, 칩셋이 선천적으로 인젝션을 못 하는 것이 아닙니다. 같은 계열의 AWUS036AXML도 결과가 동일합니다. 인젝션이 필요하면 실측으로 사용 가능한 AWUS036EACS, ACH, ACS를 선택하세요."
  - question: "AWUS036AXM은 침투 테스트나 Kali에 적합한가요?"
    answer: "권장하지 않습니다. monitor는 쓸 수 있지만 수신이 약해 client와 data 패킷을 자주 놓치며, 이 플랫폼에서 injection이 실패하여 deauth도 handshake 캡처도 불가능합니다. 본문의 플랫폼은 Ubuntu 24.04이며, Kali 배포판 자체에서는 테스트하지 않았습니다. 이 카드는 순수 AP, 일반 접속, WPA3 핫스팟에 적합합니다. 침투 테스트는 AWUS036EACS, ACH, ACS를 선택하세요."
  - question: "AWUS036AXM은 Ubuntu 24.04에서 드라이버를 따로 설치해야 하나요?"
    answer: "필요 없습니다. mt7921u 드라이버는 kernel 6.17에 내장되어 있어 꽂자마자 인식됩니다(USB ID 0e8d:7961). DKMS도 컴파일도 불필요합니다. 드라이버는 IBSS(Ad-hoc)와 mesh 모드를 제공하지 않는데, 이는 설정 문제가 아니라 제약입니다."
  - question: "AWUS036AXM을 AP로 핫스팟을 열 수 있나요? WPA3를 지원하나요?"
    answer: "가능합니다. 이것이 가장 잘하는 용도입니다. 2.4 GHz(802.11n)와 5 GHz VHT80 모두 iPhone이 접속해 authorized되었고, WPA3-SAE도 2.4 GHz에서 사용 가능하며(MFP: yes, 5 GHz WPA3는 실측하지 않음), 구형 iPhone은 sae_pwe=0으로 설정해야 합니다. STA+AP 병행(VIF)도 사용 가능합니다. 이번 회차에서는 2.4와 5 GHz만 테스트했고, 6 GHz와 블루투스는 별도로 실측하지 않았습니다."
  - question: "AWUS036AXM의 monitor mode는 쓸 만한가요?"
    answer: "monitor로 진입할 수 있고 2.4 GHz와 5 GHz 모두 beacon을 수신하지만, 수신이 약하고 client와 data 패킷 양이 적어 채널 호핑보다 단일 채널 고정을 권장합니다. 넓은 범위나 장거리 모니터링이 필요하다면, 우리 테스트에서는 AWUS036AXER와 ACH가 확연히 더 강했습니다."
draft: false
---

{{< tldr >}}AWUS036AXM은 ASUS GX10 / Ubuntu 24.04 ARM64에서 monitor, AP, WPA3, VIF는 사용 가능하지만, packet injection은 실측 실패(No Answer / Found 0 APs)로 deauth도 handshake 캡처도 불가능하여 침투 테스트에는 권장하지 않습니다. 순수 AP와 접속 용도로 포지셔닝합니다.{{< /tldr >}}

Yupitek은 ALFA Network의 대만 유통사입니다. 이 글은 AWUS036AXM의 카드별 실측으로, 목적은 단순합니다. 이 Wi-Fi 6 랜카드가 **ASUS GX10(ARM64) + Ubuntu 24.04**에서 "무엇을 할 수 있고 무엇을 할 수 없는지"를 명확히 측정해, 구매하는 고객이 사양표로 추측하지 않도록 하는 것입니다.

먼저 포지셔닝을 분명히 하면: 아래 모든 테스트는 Yupitek 본인 소유 장비, 본인 소유 사무실 Wi-Fi에서 완료했으며, 대상은 우리 자신의 테스트용 스마트폰입니다. 이것은 유통사가 제품 호환성과 성능 경계를 검증하는 하드웨어 검증이지, 제3자 네트워크에 대한 공격 교육이 아닙니다. 본문은 외부 네트워크에 대한 어떠한 조작 절차도 제공하지 않으며, monitor와 인젝션 관련 측정은 일률적으로 본인 소유 폐쇄 환경에서 본인 소유 기기를 대상으로 진행했습니다.

이 카드에 대해 가장 먼저 알아야 할 한 가지: **이 플랫폼에서 injection(인젝션)은 실패합니다.** 용도가 인젝션이나 handshake 캡처를 쓰게 된다면 바로 4·5절의 제품 선정 결론으로 건너뛰어도 됩니다. 안정적인 접속과 AP 구축이 목적이라면, AWUS036AXM은 매우 유능한 한 장이 될 것입니다.

## 1. 카드와 테스트 플랫폼

AWUS036AXM은 MediaTek **MT7921AU** 칩셋을 채택하고, 커널에 내장된 **mt7921u** 드라이버를 사용하며, 사양은 **Wi-Fi 6(802.11ax), 2x2** 듀얼 공간 스트림입니다. 동일 칩셋의 **AWUS036AXML**(MT7921AUN, 블루투스 추가)은 이 플랫폼에서 Wi-Fi monitor / AP / 인젝션 동작이 완전히 동일하여 두 카드를 서로 참조할 수 있습니다. 차이는 AXML에 블루투스가 추가되었고 본 장비 실측에서 6 GHz band를 사용할 수 있다는 점이며, AXM의 6 GHz와 블루투스는 이번 회차에서 별도로 실측하지 않았습니다.

- **연산 플랫폼**: ASUS GX10(ARM64 / aarch64)
- **운영체제**: Ubuntu 24.04 LTS
- **커널 버전**: kernel 6.17.0-1014-nvidia
- **테스트 기기**: Apple iPhone 7 Plus(WPA3-SAE와 VIF는 별도로 iPhone 15 Pro로 재검증)
- **테스트 환경**: 본인 소유 사무실 Wi-Fi, SSID `YUPITEK`, 2.4GHz ch5 / 5GHz ch36
- **테스트 기간**: 2026-11-16 ~ 2026-11-18 실기 측정

## 2. 하드웨어와 드라이버(설치 불필요, 바로 사용)

mt7921u 드라이버는 이미 kernel 6.17에 내장되어 있어, AWUS036AXM을 GX10에 꽂으면 바로 인식됩니다. DKMS도 필요 없고, 제3자 드라이버를 직접 컴파일할 필요도 없습니다. 이것이 이 세대 MediaTek 카드가 ARM64에서 가장 손이 덜 가는 지점입니다.

| 항목 | 내용 |
|---|---|
| 모델명 | AWUS036AXM |
| 칩셋 | MediaTek MT7921AU |
| USB ID | `0e8d:7961` |
| 드라이버(in-kernel) | `mt7921u` |
| 세대 / 스트림 | Wi-Fi 6(802.11ax) / 2x2 |
| 인터페이스 모드 | managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO / P2P-device |
| 미지원 모드 | IBSS(Ad-hoc), Mesh(802.11s) |

랜카드가 인식되는지 확인합니다:

```bash
lsusb | grep 0e8d:7961
```

예상 출력은 `ID 0e8d:7961 MediaTek Inc. Wireless_Device`입니다. 또한 `iw phy info`가 나열하는 인터페이스 모드에 IBSS와 mesh point가 없다는 점에 유의하세요. 이는 mt7921u의 선천적 제약이지 설정 문제가 아닙니다. mesh / IBSS를 돌려야 하는 시나리오라면 `mt76`의 AWUS036ACM / ACHM으로 대체하세요.

## 3. 실측 성능: Monitor / AP / WPA3, 그리고 Injection 실패에 대한 정직한 설명

먼저 핵심 성능 매트릭스를 제시하고, 항목별로 설명하겠습니다.

| 성능 항목 | 2.4 GHz | 5 GHz | 실측 비고 |
|---|---|---|---|
| Monitor(모니터) | ✅ 사용 가능(수신 약함) | ✅ 사용 가능(수신 약함) | beacon은 수신, client / data frame 양은 적음 |
| **Injection(인젝션)** | ❌ **이 플랫폼에서 실패** | ❌ **이 플랫폼에서 실패** | 근본 원인은 kernel 6.16+ mac80211 chanctx 회귀(regression)(칩셋 선천적 문제 아님) |
| AP(핫스팟) | ✅ 802.11n(HT20) 포함 | ✅ VHT 80 MHz | iPhone 7 Plus 실기 접속, authorized |
| WPA3-SAE | ✅ | 미실측 | MFP: yes, `sae_pwe=0`으로 구형 iPhone 호환, 2.4 GHz에서만 실측 |
| VIF(STA + AP) | ✅ | ✅ | 한 카드 두 용도, STA 측 ping 17 ms |

### Monitor(모니터) ✅ 사용 가능하나 수신 약함

2.4GHz와 5GHz 모두 monitor 모드로 전환할 수 있고, beacon도 수신합니다. 다만 정직하게 말하면: AWUS036AXM의 수신은 같은 플랫폼의 AWUS036ACM / ACHM보다 확연히 약하고, 실측 frame 수가 적으며, client와 data 패킷 캡처량이 많지 않습니다. 실무적으로는 **단일 채널 고정** 측정을 권장하며, 채널 호핑을 하지 않으면 수확이 좀 더 안정적입니다.

또 오판하기 쉬운 지점 하나: monitor 모드에서 `txpower`가 3 dBm으로 보고되는데, 이는 보고상의 착시(하드웨어 실제 TX는 약 20 dBm, `txpower_sku`로 검증됨)이지 실제 송신이 그렇게 낮게 눌린 것이 아닙니다. AWUS036AXM은 애초에 넓은 범위 측정을 위해 설계된 카드가 아닙니다. 넓게 스캔하고 멀리 수신하려면, 안테나 튜닝이 더 강하고 채널 호핑이 더 적극적인 AWUS036AXER, 또는 듀얼 안테나 고이득의 AWUS036ACH를 보세요. 이 두 장은 같은 플랫폼에서 monitor 수신이 확연히 더 강합니다.

### AP(핫스팟) ✅ 이것이 AXM이 가장 잘하는 시나리오

2.4GHz AP는 802.11n(HT20)을 동시에 열 수 있으며, iPhone 7 Plus가 MCS 7로 협상해 authorized되었습니다. 5GHz는 **VHT 80 MHz**까지 열 수 있고, iPhone이 VHT-NSS2, authorized로 접속했습니다. 2.4G든 5G든 AWUS036AXM은 핫스팟으로서 안정적이며, 이것이 이 플랫폼에서 가장 값어치를 하는 능력입니다.

### WPA3-SAE ✅

AP 측에서 WPA3-SAE를 열어 iPhone 7 Plus가 성공적으로 접속했고, MFP(Management Frame Protection)가 `yes`로 표시되었습니다. 실무 팁: `sae_pwe=0`으로 설정하면 iPhone 7 Plus 같은 비교적 구형 기기와 호환됩니다. `sae_pwe=2`로 설정하면 구형 iPhone이 접속하지 못할 수 있습니다.

### VIF(STA + AP 한 카드 두 용도) ✅

AWUS036AXM은 STA로 기존 Wi-Fi에 접속하면서 동시에 AP 가상 인터페이스(VIF)를 열 수 있습니다. 실측에서 iPhone 15 Pro가 AP VIF에 접속할 때 STA 측의 `YUPITEK`에 대한 ping은 약 17 ms로 접속이 정상이었습니다. "한 카드로 동시에 인터넷에 접속하면서 핫스팟을 공유하는" 요구에 사용 가능합니다.

### Injection(인젝션) ❌ 이 플랫폼에서 실패 —— 제품 선정의 분수령

이것이 AWUS036AXM에서 가장 중요하고, 가장 정직하게 밝혀야 할 항목입니다. 실측 `aireplay-ng --test`의 출력은 다음과 같습니다:

```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

2.4GHz와 5GHz 모두 동일하게 실패합니다. 먼저 흔한 오해 하나를 짚자면: monitor 모드에서 `iw`가 txpower를 3 dBm으로만 보고하는 것은 **보고상의 착시**이며, 하드웨어 실제 TX는 약 20–23 dBm(`txpower_sku`로 검증됨)으로 송신 출력이 낮게 눌린 것이 아니므로 실패의 주원인이 아닙니다. 진짜 근본 원인은 **소프트웨어 레이어**에 있습니다. kernel 6.16 이후 mac80211의 channel context(chanctx)에 회귀(regression)가 발생해, stock 드라이버가 active monitor / 인젝션 상황에서 대상 beacon을 수신하지 못하고, `aireplay-ng`가 그래서 `No Answer`로 판정합니다. 이것은 **커널 쪽의 회귀이지, MT7921 칩셋이 선천적으로 인젝션을 못 하는 것이 아닙니다.** 현상은 morrownr/USB-WiFi issue #387에 기록되어 있고, 근본 원인 분석은 morrownr/mt76 issue #18에 있습니다.

보충하면: 커뮤니티 실측에 따르면 같은 모델에서 git / patched 드라이버로 바꾸면 active monitor와 인젝션을 작동시킬 수 있지만, 그렇더라도 MT7921 firmware는 인젝션을 **1 Mbps / 6 Mbps의 기본 속도에 고정**하여 HT / VHT 속도로 인젝션할 수 없습니다. 바꿔 말하면 커널 회귀를 우회하더라도 이 카드의 인젝션 능력은 제한됩니다. Realtek의 rtw89 카드(예: AWUS036AX / AXER)가 동일한 aircrack-ng, 동일한 GX10 플랫폼에서 인젝션 가능한 것과 대조적으로, MT7921의 이 경로는 **stock kernel 6.17**에서 막혀 있습니다.

다시 한번 강조하면, 이것은 개별 카드의 고장도, 설정 오류도 아닙니다. 동일 칩셋의 AWUS036AXML도 동작이 완전히 똑같으며, stock kernel 6.17에서 파라미터를 바꾸거나 채널을 바꾸거나 regulatory domain을 바꿔도 되살릴 수 없습니다. 근본 원인은 kernel 6.16+의 mac80211 chanctx 회귀에 더해 firmware의 인젝션 속도 고정이며, 칩셋 하드웨어 결함이 아닙니다. 직접적인 결과: AWUS036AXM은 이 플랫폼에서 **deauth 불가, WPA handshake의 능동 캡처 불가**입니다. 이런 능력이 필요하면 다음 절의 Realtek / mt76x 방안으로 바꾸세요.

고급 기능은 다음과 같이 정리합니다:

| 고급 기능 | 상태 | 설명 |
|---|---|---|
| WPA handshake 캡처 | ❌ | 인젝션 실패로 사용 불가, ACM / ACHM / ACH / ACS / EACS로 대체 |
| VIF(STA + AP) | ✅ | 한 카드 두 용도 사용 가능 |
| Active monitor | 🟡 | `set monitor active`는 수용되나 ACK 미검증 |
| Ad-hoc(IBSS) | N/A | mt7921u 미지원 |
| Mesh(802.11s) | N/A | mt7921u 미지원 |
| Wi-Fi Direct(P2P) | ⬜ | 드라이버는 지원 선언, 두 번째 장비 부재로 미테스트 |

### 조작 안전과 실무 팁

GX10에서 이 카드를 조작할 때의 실무 요점 몇 가지를 먼저 짚으면 지뢰를 덜 밟습니다:

- **자신의 네트워크를 끊지 마세요**: 절대로 `airmon-ng check kill`을 실행하지 마세요. NetworkManager를 꺼버려 GX10 전체가 인터넷에서 끊깁니다. 조작할 때는 외장 `wlx*` 인터페이스만 다루고, GX10 내장 외부 인터넷 메인 라인은 건드리지 마세요.
- **AP 비밀번호는 8자 이상**: 그렇지 않으면 hostapd가 `invalid WPA passphrase length`를 반환하여 띄우지 못합니다.
- **스마트폰이 SSID를 못 찾을 때**: 랜카드를 한 번 뽑았다 꽂아 리셋하거나 스마트폰을 가까이 대면 해결됩니다(monitor 모드가 보고하는 3 dBm은 착시이지 실제 출력이 아니므로 주원인이 아닙니다).
- **RX stall 해결**: monitor / AP를 반복 전환한 뒤 갑자기 아무것도 스캔되지 않으면 대개 RX stall이며, 랜카드를 한 번 뽑았다 꽂으면 복구됩니다(인터페이스 이름은 MAC으로 명명되어 바뀌지 않음).

## 4. 적합한 용도와 부적합한 용도

위의 측정을 한마디로 수렴하면: AWUS036AXM은 뛰어난 "접속 / AP" 카드이지만, "인젝션 / 공방" 카드는 아닙니다.

**적합한 용도**

- 안정적인 일상 접속(Wi-Fi 6, 2x2)
- 2.4GHz / 5GHz AP 핫스팟 구축(802.11n과 VHT80 포함)
- WPA3-SAE 호환성 검증과 배포 테스트
- STA + AP 한 카드 두 용도(VIF)
- beacon 수동 측정의 경량 monitor 요구

**부적합한 용도(지뢰 회피)**

- injection / deauth
- WPA handshake 캡처, 능동적 공방 훈련
- IBSS(Ad-hoc)나 Mesh가 필요한 실험
- 장거리, 고감도의 넓은 범위 monitor 측정

**가장 중요한 지뢰 회피**: 용도가 **injection이나 handshake**라면 **AWUS036AXM(또는 동일 칩셋의 AWUS036AXML)을 선택하지 마세요.** MT7921은 ASUS GX10(ARM64 / Ubuntu 24.04 / stock kernel 6.17) 이 플랫폼에서 인젝션이 실패하며, 근본 원인은 kernel 6.16+의 mac80211 chanctx 회귀이지 칩셋이 선천적으로 인젝션을 못 하는 것이 아닙니다. 2026-11-18 기준 stock 환경에서는 파라미터 조정으로 해결할 수 없으니, "순수 접속 / 순수 AP" 시나리오로 남겨 두면 됩니다.

## 5. 제품 선정 제안(순수 AP / 접속)

| 당신의 요구 | 권장 선택 | 이유 |
|---|---|---|
| 순수 AP / 안정적 접속(인젝션 불필요) | **AWUS036AXM** / AWUS036AXML | MediaTek 접속이 안정적이고 AP와 WPA3 성능이 좋음 |
| 침투 테스트(injection + handshake) | AWUS036EACS / AWUS036ACH / AWUS036ACS | 두 밴드 인젝션 사용 가능, 엔드투엔드 handshake 작동 |
| 최강 수신 / 장거리 monitor | AWUS036AXER / AWUS036ACH | AXER는 채널 호핑 스캔이 적극적, ACH는 듀얼 안테나 고이득 |
| Wi-Fi 6 + AP이면서 인젝션 필요 | AWUS036AX / AWUS036AXER | 2x2 VHT80, AP 안정적이며 인젝션 사용 가능 |
| mesh / IBSS 실험 | AWUS036ACM / AWUS036ACHM | `mt76` 드라이버로 단일 기기에서 생성 가능 |

쉽게 한마디로: 안정적인 접속과 AP 구축이 목적이면 AWUS036AXM이 매우 유능하고, 인젝션이나 handshake가 얽히면 Realtek의 EACS / ACH / ACS로 바꾸세요. 같은 카드들을 ARM64에서 전면 비교한 내용과 9종 Monitor / Injection / AP / WPA3 전체 매트릭스는 종합표 Hub를 참고하세요:

- [2026 가장 완전한 실측: 9종 ALFA 무선 랜카드의 ASUS GX10(ARM64 / Ubuntu 24.04) 전체 매트릭스](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

다시 포지셔닝을 강조하면: 본문의 모든 monitor / 인젝션 관련 측정은 전부 Yupitek 본인 소유 폐쇄 환경에서 본인 소유 테스트 기기를 대상으로 진행했으며, 용도는 제품 능력과 호환성 경계를 검증하는 것입니다. 어떠한 제3자 네트워크에 대해서도 위 조작을 제공하지도 권장하지도 않습니다.

## 자주 묻는 질문(FAQ)

**Q1. AWUS036AXM으로 패킷 인젝션(packet injection)을 할 수 있나요?**
우리의 테스트 플랫폼(ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia)에서는 불가능합니다. `aireplay-ng --test`가 2.4 GHz와 5 GHz 모두 `No Answer`, `Found 0 APs`를 보고하며, 따라서 deauth도 WPA handshake 캡처도 불가능합니다. 근본 원인은 kernel 6.16+의 mac80211 chanctx 회귀이며, 칩셋이 선천적으로 인젝션을 못 하는 것이 아닙니다. 같은 계열의 AWUS036AXML도 결과가 동일합니다. 인젝션이 필요하면 실측으로 사용 가능한 AWUS036EACS, ACH, ACS를 선택하세요.

**Q2. AWUS036AXM은 침투 테스트나 Kali에 적합한가요?**
권장하지 않습니다. monitor는 쓸 수 있지만 수신이 약해 client와 data 패킷을 자주 놓치며, 이 플랫폼에서 injection이 실패하여 deauth도 handshake 캡처도 불가능합니다. 본문의 플랫폼은 Ubuntu 24.04이며, Kali 배포판 자체에서는 테스트하지 않았습니다. 이 카드는 순수 AP, 일반 접속, WPA3 핫스팟에 적합합니다. 침투 테스트는 AWUS036EACS, ACH, ACS를 선택하세요.

**Q3. AWUS036AXM은 Ubuntu 24.04에서 드라이버를 따로 설치해야 하나요?**
필요 없습니다. mt7921u 드라이버는 kernel 6.17에 내장되어 있어 꽂자마자 인식됩니다(USB ID `0e8d:7961`). DKMS도 컴파일도 불필요합니다. 드라이버는 IBSS(Ad-hoc)와 mesh 모드를 제공하지 않는데, 이는 설정 문제가 아니라 제약입니다.

**Q4. AWUS036AXM을 AP로 핫스팟을 열 수 있나요? WPA3를 지원하나요?**
가능합니다. 이것이 가장 잘하는 용도입니다. 2.4 GHz(802.11n)와 5 GHz VHT80 모두 iPhone이 접속해 authorized되었고, WPA3-SAE도 2.4 GHz에서 사용 가능하며(`MFP: yes`, 5 GHz WPA3는 실측하지 않음), 구형 iPhone은 `sae_pwe=0`으로 설정해야 합니다. STA+AP 병행(VIF)도 사용 가능합니다. 이번 회차에서는 2.4와 5 GHz만 테스트했고, 6 GHz와 블루투스는 별도로 실측하지 않았습니다.

**Q5. AWUS036AXM의 monitor mode는 쓸 만한가요?**
monitor로 진입할 수 있고 2.4 GHz와 5 GHz 모두 beacon을 수신하지만, 수신이 약하고 client와 data 패킷 양이 적어 채널 호핑보다 단일 채널 고정을 권장합니다. 넓은 범위나 장거리 모니터링이 필요하다면, 우리 테스트에서는 AWUS036AXER와 ACH가 확연히 더 강했습니다.

## 6. 더 읽어보기

다음 관련 글들이 순차적으로 공개됩니다(링크 작업 중):

- 《드라이버 설치 불필요: Ubuntu(ARM64)에서 Monitor와 AP 모드 활성화하기》 → [`/ko/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/ko/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 《WPA3-SAE 능력과 handshake 실무(본인 소유 환경 검증)》 → [`/ko/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/ko/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 《AWUS036AXML 단일 카드 실측(동일 MT7921 칩셋 + BT)》 →(준비 중, 링크 작업 중)
- 《mt7921u가 kernel 6.16 이후 인젝션을 못 하는 이유: chanctx 회귀와 firmware 속도 고정 설명》 →(준비 중, 링크 작업 중)

---

*테스트 기관: Yupitek(ALFA 유통사) | 플랫폼: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | 테스트 기기: Apple iPhone 7 Plus(WPA3 / VIF는 별도로 iPhone 15 Pro)*
