---
title: "2026년 가장 완벽한 실측: ALFA 무선 랜카드 9종의 ASUS GX10(ARM64 / Ubuntu 24.04) Monitor · Injection · AP 종합 매트릭스"
slug: alfa-9-cards-arm64-gx10-ubuntu-matrix
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix.webp"
author: "benny-lai"
tags:
  - alfa-network
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - wifi-6
  - kali-linux
description: "ALFA Wi-Fi USB 랜카드 9종을 Ubuntu 24.04 ARM64(GX10)에서 Monitor, Injection, AP, WPA3-SAE 항목으로 실측하고, Kali 주요 도구 호환성과 제품 선정 가이드까지 정리했습니다. AWUS036ACH / EACS 인젝션 100% 달성."
faq:
  - question: "AWUS036AXM은 Ubuntu에서 인젝션(injection)이 되나요?"
    answer: "이 플랫폼에서는 되지 않습니다. 실측에서 AWUS036AXM과 AWUS036AXML(둘 다 MT7921 칩)은 2.4GHz와 5GHz 모두에서 injection에 실패했습니다. 주원인은 stock kernel 6.16+의 mac80211 chanctx 회귀(칩 선천적 문제가 아님)이므로, 이 플랫폼에서는 인젝션이나 핸드셰이크 캡처가 필요한 용도에 권장하지 않습니다."
  - question: "Ubuntu에서 injection 성공률이 가장 높은 ALFA 랜카드는 무엇인가요?"
    answer: "실측에서 AWUS036ACH와 AWUS036EACS는 2.4GHz와 5GHz injection 성공률이 모두 100%로, 이번 9종 중 가장 뛰어난 두 종입니다."
  - question: "ALFA 랜카드 9종은 Ubuntu 24.04에서 별도로 드라이버를 설치해야 하나요?"
    answer: "필요 없습니다. 9종 모두 커널 6.17에서 커널 내장(in-kernel) 드라이버(rtw88 / rtw89 / mt76 계열)로 동작하여 꽂으면 바로 인식되며, DKMS 모듈을 컴파일할 필요가 없습니다."
  - question: "ALFA 랜카드로 Ubuntu에서 WPA3-SAE 핫스팟을 구축할 수 있나요?"
    answer: "가능합니다. 9종 모두 실측에서 WPA3-SAE 핫스팟을 성공적으로 구축하고 장치를 연결시킬 수 있었습니다(ACS를 제외한 모든 카드는 2.4 GHz에서, ACS는 5 GHz에서 실측했으며 AXML은 6 GHz에서도 실측했습니다). 다만 AWUS036ACHM만 hostapd의 sae_pwe를 0으로 설정해야 하며, 그렇지 않으면 구형 iPhone 7 Plus가 연결에 실패합니다."
  - question: "이 Ubuntu 테스트 결과를 Kali Linux 사용자가 참고할 수 있나요?"
    answer: "Kali Linux는 Debian/Ubuntu 체계를 기반으로 하며 동일한 rtw88 / rtw89 / mt76 인커널 드라이버를 사용하므로, 본문의 드라이버 호환성과 능력 매트릭스는 원칙적으로 Kali 사용자의 참고 근거가 될 수 있습니다. 다만 본문의 실측 플랫폼은 Ubuntu 24.04이며 Kali에서 정식으로 재측정하지는 않았으니, 결과는 추후 재측정을 기준으로 삼으시기 바랍니다."
draft: false
---

## 핵심 요약(TL;DR)

Yopitek(ALFA Network 대만 총판)이 ASUS GX10(ARM64 / Ubuntu 24.04 / kernel 6.17)에서 ALFA USB 무선 랜카드 9종을 실측한 결과, 9종 모두 monitor 모드와 AP가 가능했고, AWUS036ACH와 AWUS036EACS는 두 밴드 인젝션 100%에 도달했으며, MT7921 기반 AWUS036AXM / AWUS036AXML은 본 플랫폼에서 인젝션에 실패했습니다.

- **Monitor 전원 사용 가능**: 9종 모두 모니터 모드로 진입할 수 있으며, 차이는 수신 감도뿐입니다.
- **Injection이 분수령**: Realtek `rtw88`의 ACH, EACS는 두 밴드에서 인젝션 100%를 달성했고 ACS가 그다음이며, MT7921의 AXM / AXML은 이 플랫폼에서 인젝션에 실패했습니다.
- **엔드투엔드 핸드셰이크(캡처 → `.22000` 변환) 실증 9종 중 7종**: ACM, ACHM, ACH, ACS, EACS, AX, AXER.
- **AP와 WPA3-SAE는 거의 전원 통과**: AWUS036ACHM만 구형 iPhone 호환을 위해 `sae_pwe=0` 설정이 필요합니다.
- **ARM64 컴파일 불필요**: 9종 전부 커널 6.17 내장 드라이버로 동작하여 꽂으면 바로 사용되고 DKMS가 필요 없습니다.

Yopitek는 ALFA Network의 대만 총판(유통사)입니다. 고객이 USB 무선 랜카드를 구매할 때 가장 많이 묻는 세 가지 질문은 거의 항상 같습니다. "이 카드가 내 Linux 환경에서 모니터 모드로 들어갈 수 있나요? 인젝션은 되나요? AP를 구축할 수 있나요?" 스펙 시트로 답하는 대신, 저희는 현역 ALFA 랜카드 9종을 직접 자사 실험대에 올려 **ASUS GX10(ARM64)** 과 **Ubuntu 24.04 LTS** 환경에서 한 장씩 실측하고, Monitor, Injection, AP, WPA3-SAE 네 가지 능력 축을 한 번에 비교했습니다. 그리고 어떤 카드가 "이 플랫폼에서 무엇을 못 하는지"도 정직하게 표기했습니다.

먼저 포지션을 분명히 해 둡니다. 본문의 모든 테스트는 Yopitek 소유의 장비와 자사 사무실 Wi-Fi에서 자사 테스트 전화기를 대상으로 수행했습니다. 이는 총판이 제품 호환성과 능력 경계를 검증하기 위한 하드웨어 검증이며, 제3자 네트워크를 겨냥한 공격 튜토리얼이 아닙니다. 본문은 외부 네트워크를 대상으로 한 어떠한 조작 절차도 제공하지 않으며, 인젝션과 핸드셰이크 관련 능력은 모두 본인 소유의 폐쇄 환경에서 본인 소유 장치를 대상으로 측정했습니다.

이 글은 종합표 형태의 허브(Hub) 문서입니다. 각 카드의 단계별 설정과 완전한 증거는 별도의 카드별 심화 문서로 분리됩니다(글 말미의 더 읽어보기 참조).

## 테스트 플랫폼과 방법

- **연산 플랫폼**: ASUS GX10(ARM64 / aarch64)
- **운영체제**: Ubuntu 24.04 LTS
- **커널 버전**: kernel 6.17.0-1014-nvidia
- **드라이버 전략**: 9종 모두 커널 내장(in-kernel) 드라이버를 사용하여 꽂으면 바로 인식되며, 제3자 DKMS 모듈을 일절 설치하지 않습니다.
- **테스트 장치**: Apple iPhone 7 Plus(WPA3-SAE 호환성은 iPhone 15 Pro로 별도 재측정)
- **테스트 환경**: 자사 사무실 Wi-Fi, SSID `YUPITEK`, 2.4GHz ch5 / 5GHz ch36, ch157
- **테스트 기간**: 2026-11-16 ~ 2026-11-18 실기 측정

방법 면에서는 각 카드에 대해 동일한 절차 세트를 돌렸습니다. 먼저 드라이버 로드와 인터페이스 생성(`wlx*`)을 확인한 뒤, 2.4GHz / 5GHz의 monitor, injection, AP, WPA3-SAE 연결을 순서대로 검증하고, 마지막으로 자사 테스트 전화기에 대해 엔드투엔드 핸드셰이크 캡처 체인의 검수를 수행했습니다. 모든 결과는 실제로 측정한 수치나 상태로 기록했으며, 스펙 시트로 추정하지 않았습니다.

본문 표는 다음 범례를 사용합니다.

> ✅ 통과 | 🟡 부분 또는 단일 기기에서 성립 | ⚠️ 제한 있음 | ❌ 미지원 또는 테스트 실패 | N/A 드라이버가 해당 모드를 지원하지 않음 | ⬜ 미측정(두 번째 장비 부족)

## 1. 하드웨어와 드라이버 대조

먼저 9종의 하드웨어 사양과 커널 6.17에서 실제로 로드되는 드라이버를 살펴봅니다.

| # | 모델 | 칩 | USB ID | 드라이버(in-kernel) | 펌웨어 | 세대 / 스트림 | 비고 |
|---|---|---|---|---|---|---|---|
| 1 | **AWUS036ACM** | MediaTek MT7612U | — | `mt76x2u` | — | Wi-Fi 5 / 2T2R | morrownr 추천 Kali 카드 |
| 2 | **AWUS036ACHM** | MediaTek MT7610U | — | `mt76x0u` | — | Wi-Fi 5 / 1T1R(AC600) | 단일 안테나 |
| 3 | **AWUS036ACH** | Realtek RTL8812AU | `0bda:8812` | `rtw88_8812au` | — | Wi-Fi 5 / 2T2R(AC1200) | 듀얼 안테나 고이득 |
| 4 | **AWUS036ACS** | Realtek RTL8811AU | `0bda:0811` | `rtw88_8821au` | 42.4.0 | Wi-Fi 5 / 1x1 | 경량 휴대형 |
| 5 | **AWUS036EACS** | Realtek RTL8821CU | `0bda:c820` | `rtw88_8821cu` | 24.11.0 | Wi-Fi 5 / 1x1 | BT + WiFi 복합 |
| 6 | **AWUS036AX** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | — |
| 7 | **AWUS036AXER** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | 동일 칩, 내장 안테나(Nano) |
| 8 | **AWUS036AXM** | MediaTek MT7921AU | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | — |
| 9 | **AWUS036AXML** | MediaTek MT7921AUN | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | + BT |

몇 가지 핵심:

**두 개의 드라이버 진영.** 9종은 MediaTek(`mt76x2u` / `mt76x0u` / `mt7921u`)와 Realtek(`rtw88_*` / `rtw89_8852bu`) 두 가지 인커널 드라이버로 나뉩니다. 칩 세대는 Wi-Fi 5(6종)와 Wi-Fi 6(3종: AX, AXER는 `rtw89_8852bu`, AXM, AXML은 `mt7921u`)을 아우릅니다.

**ARM64에서 가장 현실적인 장점은 "컴파일 불필요"입니다.** 이 9종은 커널 6.17에서 전부 인커널 드라이버로 동작하여 꽂으면 바로 인식되며, aarch64에서 out-of-tree DKMS 모듈을 다룰 필요가 없습니다. 이 점은 ARM64에서 특히 체감됩니다. 많은 제3자 Realtek 드라이버는 aarch64용 prebuilt가 없어서 흔히 원본 소스에서 컴파일하고 커널 버전에 맞춰야 하며, 문제가 터질 확률이 높습니다. 이 카드들은 그 과정을 아예 생략합니다.

**동일 칩, 다른 모델.** AWUS036AX와 AWUS036AXER는 동일한 RTL8832BU와 동일한 `rtw89_8852bu` 드라이버를 쓰며, 차이는 안테나 설계에 있습니다(AXER는 내장 안테나 Nano 설계로 RP-SMA가 없습니다). 이 차이는 뒤의 수신과 인젝션 수치에 반영됩니다.

**두 종은 BT + WiFi 복합 장치입니다.** AWUS036EACS(RTL8821CU)와 AWUS036AXML(MT7921AUN)은 블루투스를 함께 탑재하는데, 이 특성은 카드를 다시 꽂을 때 실무적인 부작용이 있습니다. 뒤의 "플랫폼 주의사항"에서 설명합니다.

## 2. 핵심 능력 매트릭스: Monitor / Injection / AP / WPA3

이것이 본문의 메인 표이자, 제품 선정 시 가장 먼저 봐야 할 표입니다.

| # | 모델 | Monitor 2.4G | Monitor 5G | **Injection 2.4G** | **Injection 5G** | AP 2.4G | AP 5G | WPA3-SAE |
|---|---|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ | ✅ | ✅ 63–83% | ✅ 76% | ✅ | ✅ 80MHz | ✅ 2.4G |
| 2 | AWUS036ACHM | ✅ | ✅ | ✅ 96–100% | ⚠️ 브로드캐스트만 | ✅ | ✅ | ✅* 2.4G |
| 3 | AWUS036ACH | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ | ✅ 2.4G |
| 4 | AWUS036ACS | ✅ | ✅ | ✅ **100%** | ✅ 96% | ✅ | ✅(802.11a, 20 MHz 실측, VHT80 미측정) | ✅ 5G |
| 5 | AWUS036EACS | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅(802.11a, 20 MHz 실측, VHT80 미측정) | ✅ 2.4G |
| 6 | AWUS036AX | ✅ 강 | ✅ 강 | ✅ 96% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 7 | AWUS036AXER | ✅ 강 | ✅ 강 | ✅ 73% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 8 | AWUS036AXM | ✅ 약 | ✅ 약 | ❌ **실패** | ❌ **실패** | ✅ | ✅ 80MHz | ✅ 2.4G |
| 9 | AWUS036AXML | ✅ 약 | ✅ 약 | ❌ **실패** | ❌ **실패** | ✅ | ✅ 80MHz | ✅ 2.4G / 6G |

> \* AWUS036ACHM의 WPA3는 `sae_pwe=0` 설정이 필요하며, `sae_pwe=2`에서는 iPhone 7 Plus가 연결되지 않습니다.
>
> WPA3-SAE 열: 표시된 밴드가 실제로 실측한 밴드입니다(ACS를 제외한 모든 카드는 2.4G, ACS는 5G이며 AXML은 6G에서도 실측). 그 외 밴드는 실측하지 않았습니다.

항목별 해설:

**Monitor: 9종 전부 사용 가능하며, 차이는 수신 감도입니다.** 2.4GHz든 5GHz든 9종 모두 예외 없이 모니터 모드로 진입할 수 있습니다. 차이는 스캔 적극성과 수신 감도입니다. Wi-Fi 6의 AX / AXER가 수신이 가장 강하고 스캔이 가장 적극적이며, MT7921의 AXM / AXML도 모니터 진입은 되지만 상대적으로 약합니다. 수동 측록이나 스펙트럼 점검만 필요하다면 9종 모두 쓸 수 있습니다.

**Injection: 여기서부터 격차가 벌어집니다.** Realtek `rtw88` 계열이 가장 좋습니다. ACH와 EACS는 2.4GHz / 5GHz에서 모두 **100%**, ACS도 2.4GHz 100% / 5GHz 96%입니다. MediaTek `mt76`의 ACM은 사용 가능하지만 수치가 중간대(2.4GHz 63–83%, 5GHz 76%)에 머물며, ACHM의 5GHz는 브로드캐스트만 되고 특정 대상에 대한 인젝션은 불가합니다. `rtw89`의 AX / AXER는 인젝션이 가능하며, 그중 AXER의 2.4GHz 인젝션률(73%)은 AX(96%)보다 한 단계 낮습니다.

**가장 중요한 정직한 제약: MT7921(AXM / AXML) 인젝션은 이 플랫폼에서 실패합니다.** 이는 파라미터를 못 맞춰서도 아니고, 칩이 선천적으로 인젝션을 못 해서도 아닙니다. 주원인은 커널 6.16+의 mac80211 chanctx 회귀(regression)입니다. 커뮤니티에서는 동일 모델에 git/patched 드라이버를 써서 동작시키기도 하지만, 펌웨어가 속도를 잠급니다(morrownr/USB-WiFi #387, morrownr/mt76 #18 참조). 이 플랫폼에서는 인젝션 실패로 인해 두 카드가 deauth를 할 수 없고, 따라서 핸드셰이크 캡처 체인을 끝까지 돌릴 수 없습니다. 인젝션이 필요한 용도라면 이 두 카드는 이 플랫폼에서 바로 제외하시기 바랍니다.

**AP와 WPA3: 거의 전원 통과.** 9종 모두 AP로 동작하며, 대부분 5GHz VHT80(80MHz)을 지원합니다. WPA3-SAE 연결도 실측한 밴드에서 전부 성립합니다(표 아래 주석 참고). 유일하게 주의할 것은 AWUS036ACHM으로, WPA3는 hostapd의 `sae_pwe`를 0으로 설정해야 하며 그렇지 않으면 구형 iPhone 7 Plus가 연결되지 않습니다(iPhone 15 Pro로 재측정 시 연결 가능하므로 호환성 설정 차이에 해당합니다).

## 3. 고급 기능과 핸드셰이크 능력 요약

범위를 한 단계 더 깊이 넓혀서 핸드셰이크 엔드투엔드, 가상 인터페이스(VIF), active monitor, mesh / IBSS를 봅니다.

| # | 모델 | WPA 핸드셰이크 캡처 | VIF | Active monitor | Ad-hoc(IBSS) | Mesh(802.11s) |
|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ **엔드투엔드**(.22000) | ✅ STA+AP / AP+mon | 🟡 설정 가능, ACK 미검증 | 🟡 단일 기기 | 🟡 단일 기기 |
| 2 | AWUS036ACHM | ✅ **엔드투엔드**(.22000, 5 GHz ch36) | ✅ | 🟡 | 🟡 단일 기기 | 🟡 단일 기기 |
| 3 | AWUS036ACH | ✅ **엔드투엔드**(.22000) | ✅ STA+mon | ❌ -95 | 🟡 단일 기기 | ❌ -95 |
| 4 | AWUS036ACS | ✅ **엔드투엔드**(.22000) | ✅ | ❌ -95 | ❌ | ❌ -95 |
| 5 | AWUS036EACS | ✅ **엔드투엔드**(.22000, 79 ACKs) | 🟡 같은 채널의 passive monitor + managed(소프트웨어 monitor)만 가능, 독립적인 이중 VIF 미지원 | ❌ -95 | ❌ | ❌ -95 |
| 6 | AWUS036AX | ✅ **엔드투엔드**(.22000) | ✅ STA+AP | N/A | N/A | N/A |
| 7 | AWUS036AXER | ✅ **엔드투엔드**(.22000) | ✅ STA+AP | N/A | N/A | N/A |
| 8 | AWUS036AXM | ❌ 인젝션 실패 | ✅ | 🟡 | N/A | N/A |
| 9 | AWUS036AXML | ❌ 인젝션 실패 | ✅ | 🟡 | N/A | N/A |

여기서 "엔드투엔드"에는 명확한 정의가 있습니다. 해당 카드로 **Yopitek 소유의 iPhone 7 Plus**(자사 `YUPITEK` SSID에 연결됨)에 injection을 수행하여 완전한 4-way 핸드셰이크(M1–M4)를 캡처하고, 다시 `hcxpcapngtool --all`로 hashcat의 `.22000` 포맷으로 변환하는 전 과정입니다. 이 체인 전체가 끝까지 돌아가는지가 "침투 테스트 능력"의 검수 지점이며, "모니터에 진입할 수 있다"로 끝나는 것이 아닙니다.

- **엔드투엔드 통과(9종 중 7종)**: ACM, ACHM, ACH, ACS, EACS, AX, AXER 모두 `.22000`을 산출할 수 있으며, 그중 EACS는 79개의 ACK를 수신해 신호 피드백이 가장 탄탄했습니다. ACH는 두 밴드 인젝션 100%로, 2026-11-19에 47줄 해시라인의 `.22000`을 추가 측정으로 변환해 냈습니다. ACHM은 5GHz(ch36)에서 완주했고, ACM은 인젝션 성공률이 더 낮음에도 완주했습니다.
- **엔드투엔드 체인 단절**: AXM / AXML은 인젝션 실패로 인해 핸드셰이크 체인 전체가 함께 끊깁니다. 이는 MT7921이 이 플랫폼에서 침투 테스트 용도에 적합하지 않음을 다시 한번 입증합니다.
- **VIF(가상 인터페이스 병존)**: 9종 모두 어떤 형태로든 다중 인터페이스 병존을 지원하며, Realtek rtw89는 STA + AP를 동시에 돌릴 수 있습니다. 다만 EACS는 같은 채널의 managed 인터페이스와 함께 동작하는 passive monitor(소프트웨어 monitor)만 지원하고 독립적인 이중 VIF는 지원하지 않습니다.
- **Active monitor(ACK 보고 포함)**: `rtw88`의 ACH / ACS / EACS는 -95(미지원)를 반환하고, `rtw89`의 AX / AXER는 드라이버가 해당 모드를 지원하지 않습니다(N/A). `mt76` / `mt7921u`는 부분 가능(🟡)입니다.
- **Mesh(802.11s)**: `mt76`의 ACM / ACHM만 단일 기기에서 구축 가능합니다(🟡, 완전한 상호 연결 검증에는 두 번째 카드 필요). Realtek `rtw88`은 -95 미지원을 반환하고, `rtw89`와 `mt7921u` 드라이버는 해당 모드를 지원하지 않습니다. mesh 실험을 하려면 MediaTek `mt76`이 이 묶음에서 유일한 선택지입니다.
- **IBSS(Ad-hoc)**: `mt76`의 ACM / ACHM과 `rtw88`의 ACH는 모두 단일 기기 join이 가능합니다(🟡). EACS는 iftype을 나열하지만 실측에서는 join이 무효였고, `rtw89`의 AX / AXER는 IBSS iftype이 없습니다(N/A).

### Kali / aircrack 도구 레벨 호환성(플랫폼 공통)

다음 도구는 9종에서 플랫폼 레벨 표현이며, 개별 카드와 무관합니다.

| 도구 | 상태 | 설명 |
|---|---|---|
| airmon-ng | ✅ | 전 카드 탐지 / 관리 가능; **`check kill` 절대 금지**(NetworkManager를 꺼서 GX10이 네트워크가 끊깁니다) |
| kismet | ✅ | 각 카드를 data source로 시작해 `.kismet` log를 산출할 수 있습니다 |
| bettercap | ✅ | `wifi.recon`과 channel hopper 정상 |
| wifite(git 3.0.0) | ✅ | 스캔하여 대상 목록 작성 가능(git 버전 필수, apt 버전은 소스 빌드한 aircrack-ng와 충돌) |
| Wireshark / tshark | ✅ | monitor 캡처와 분석 정상 |
| **hcxdumptool 8.x** | ⚠️ | **2.4 GHz의 EACS를 제외한 전 카드 failed to arm(EACS는 5 GHz에서 실패)**: active-monitor가 필요한데 `rtw88` / `rtw89` / `mt7921u`가 모두 미지원 → `airodump-ng` + `aireplay-ng`로 전환 |

ARM64 보충: `aircrack-ng`는 원본 소스에서 컴파일해야 하며, `wifite`는 apt 패키지와 소스 빌드 버전 간의 의존성 충돌을 피하기 위해 git 3.0.0 버전을 권장합니다.

## 4. 용도별 제품 선정 가이드

위의 세 표를 "용도에 따라 바로 선택"으로 수렴합니다.

| 용도 | 1순위 | 설명 |
|---|---|---|
| **침투 테스트(injection + handshake)** | **AWUS036EACS** / AWUS036ACS / AWUS036ACH | 두 밴드 인젝션 최고(EACS, ACH 100%); 엔드투엔드 `.22000`은 EACS, ACS, ACH로 입증(ACH는 2026-11-19 추가 측정) |
| **최강 수신 / 장거리 monitor** | **AWUS036AXER** / AWUS036ACH | AXER는 한 번의 주파수 홉으로 63개 AP + 12개 client 스캔; ACH는 듀얼 안테나 고이득 |
| **Wi-Fi 6 + AP 핫스팟** | AWUS036AX / AWUS036AXER | 2x2 VHT80, AP 안정적이며 인젝션 사용 가능 |
| **순수 AP / 일반 연결(인젝션 불필요)** | AWUS036AXM / AWUS036AXML | MediaTek 연결 안정적이나 **인젝션 실패**로 침투 용도에는 부적합 |
| **mesh / IBSS 실험** | AWUS036ACM / AWUS036ACHM | `mt76` 드라이버로 단일 기기 mesh와 IBSS 구축 가능(`rtw88`의 ACH는 IBSS 단일 기기 join만 가능, mesh 미지원; `rtw89`는 둘 다 미선언) |

몇 마디로 요약하면 다음과 같습니다.

- **침투 테스트를 하거나 핸드셰이크를 캡처하려면**: 엔드투엔드 `.22000`이 파일로 실증된 것은 9종 중 7종입니다 — **AWUS036EACS**(가장 탄탄, 79 ACKs), **AWUS036ACS**, Wi-Fi 6의 AWUS036AX / AWUS036AXER, **AWUS036ACM**과 **AWUS036ACHM**(5 GHz), 그리고 **AWUS036ACH**(두 밴드 인젝션 100%, 2026-11-19에 47줄 해시라인의 `.22000`을 추가 측정으로 변환).
- **가장 먼 수신 거리, 가장 넓은 측록이 필요하면**: AWUS036AXER(Wi-Fi 6, 내장 안테나 Nano 설계 + 칩 튜닝, 주파수 홉 스캔이 가장 적극적)이나 듀얼 안테나 고이득의 AWUS036ACH.
- **Wi-Fi 6 핫스팟을 구축하려면**: AWUS036AX / AWUS036AXER, 2x2 VHT80이면서 인젝션도 함께 지원.
- **안정적인 연결만, 단순 AP 용도라면**: AWUS036AXM / AWUS036AXML의 MediaTek 솔루션은 연결이 안정적이어서 일상 사용에 문제없습니다.
- **mesh를 다뤄보려면**: 이 묶음에서는 `mt76`의 AWUS036ACM / AWUS036ACHM만 가능합니다(IBSS 단일 기기는 별도로 `rtw88`의 AWUS036ACH도 join 가능).

**피해야 할 점(가장 중요한 한 가지)**: 용도가 **injection 또는 handshake**라면 **AWUS036AXM / AWUS036AXML은 선택하지 마십시오.** MT7921은 ASUS GX10(ARM64 / Ubuntu 24.04 / stock kernel 6.17) 이 플랫폼에서 인젝션에 실패합니다. 주원인은 커널 6.16+의 mac80211 chanctx 회귀(regression)이며(칩 선천적 문제가 아님) 설정 문제가 아닙니다. 커뮤니티에서는 동일 모델에 git/patched 드라이버를 써서 동작시키기도 하지만 펌웨어가 속도를 잠그고, 이 플랫폼의 stock kernel에서는 여전히 인젝션이 불가합니다. 이 카드들은 "순수 연결 / 순수 AP" 용도로만 남겨두면 됩니다.

## 5. 플랫폼 주의사항(GX10 ARM64 실무)

다음은 ASUS GX10 + Ubuntu 24.04(ARM64)에서 이 카드들을 다룰 때 9종 공통의 실무 포인트입니다.

1. **본인의 네트워크를 끊지 마십시오**: `airmon-ng check kill`은 절대 실행하지 마십시오. NetworkManager를 꺼서 GX10 전체가 네트워크가 끊깁니다. 작업할 때는 외장 `wlx*` 인터페이스만 다루고, 내장된 외부 인터넷 연결 본선은 건드리지 마십시오.
2. **RX stall 해소**: monitor / AP를 반복 전환한 뒤 갑자기 아무것도 스캔되지 않으면 보통 RX stall입니다. 카드를 한 번 뽑았다 꽂으면 복구됩니다(USB 재열거, 인터페이스 이름은 MAC 기반이라 변하지 않음).
3. **BT + WiFi 복합 장치**: EACS와 AXML은 블루투스를 함께 탑재하는데, 다시 꽂을 때 간혹 WiFi probe에서 멈춰 `wlx` 인터페이스가 생성되지 않습니다. USB 포트를 바꾸면 대개 해결됩니다.
4. **5GHz의 TX 해제**: 본인 소유 환경에서 5GHz injection을 하기 전에, 먼저 올바른 규제 도메인(regulatory domain)을 설정해 TX 출력을 해제해야 합니다. 테스트 종료 후에는 현지 도메인으로 되돌립니다. 이것이 5GHz가 정상적으로 송출될 수 있는 전제입니다.
5. **핸드셰이크 캡처의 소소한 요령**: 사무실에는 동일 이름 AP가 여러 대인 경우가 많으므로, 실무상 단일 BSSID를 고정하지 말고 채널 전체를 캡처하는 편이 더 안정적입니다. 변환 시에는 `hcxpcapngtool --all`을 사용합니다.
6. **hcxdumptool 전 플랫폼 failed to arm(예외는 2.4 GHz의 EACS)**: 세 밴드 내장 카드와 위 드라이버는 모두 active-monitor를 지원하지 않으므로, 바로 aircrack-ng 패키지(`airodump-ng` + `aireplay-ng`)로 전환합니다.
7. **ARM64의 컴파일 세부사항**: `aircrack-ng`는 원본 소스에서 컴파일해야 하고, `wifite`는 apt 의존성 충돌을 우회하기 위해 git 버전을 사용합니다.

다시 한번 포지션을 강조합니다. 위의 injection / deauth / handshake 능력은 모두 Yopitek 소유의 폐쇄 환경에서 자사 테스트 장치를 대상으로 측정했으며, 용도는 제품 능력과 호환성 경계를 검증하는 것입니다. 본문은 어떠한 제3자 네트워크에도 위 조작을 수행하는 것을 제공하지도, 권장하지도 않습니다.

## 맺음말

ASUS GX10(ARM64 / Ubuntu 24.04 / kernel 6.17) 이 플랫폼에서 ALFA 카드 9종의 총평은 세 문장으로 압축할 수 있습니다. **Monitor는 전원 사용 가능, AP와 WPA3는 거의 전원 통과, 분수령은 Injection입니다.** 인젝션과 핸드셰이크가 필요한 전문 용도라면 Realtek `rtw88`의 EACS / ACH / ACS가 가장 안정적인 선택입니다. 수신과 Wi-Fi 6이 필요하다면 AXER / AX를 보고, MT7921의 AXM / AXML은 순수 연결 용도로 남겨두십시오. 전부 컴파일 불필요, 꽂으면 바로 사용 — 이것이 ARM64에서 이 카드들의 가장 큰 공통 장점입니다.

## 자주 묻는 질문(FAQ)

**Q: AWUS036AXM은 Ubuntu에서 인젝션(injection)이 되나요?**
A: 이 플랫폼에서는 되지 않습니다. 실측에서 AWUS036AXM과 AWUS036AXML(둘 다 MT7921 칩)은 2.4GHz와 5GHz 모두에서 injection에 실패했습니다. 주원인은 stock kernel 6.16+의 mac80211 chanctx 회귀(칩 선천적 문제가 아님)이므로, 이 플랫폼에서는 인젝션이나 핸드셰이크 캡처가 필요한 용도에 권장하지 않습니다.

**Q: Ubuntu에서 injection 성공률이 가장 높은 ALFA 랜카드는 무엇인가요?**
A: 실측에서 AWUS036ACH와 AWUS036EACS는 2.4GHz와 5GHz injection 성공률이 모두 100%로, 이번 9종 중 가장 뛰어난 두 종입니다.

**Q: ALFA 랜카드 9종은 Ubuntu 24.04에서 별도로 드라이버를 설치해야 하나요?**
A: 필요 없습니다. 9종 모두 커널 6.17에서 커널 내장(in-kernel) 드라이버(rtw88 / rtw89 / mt76 계열)로 동작하여 꽂으면 바로 인식되며, DKMS 모듈을 컴파일할 필요가 없습니다.

**Q: ALFA 랜카드로 Ubuntu에서 WPA3-SAE 핫스팟을 구축할 수 있나요?**
A: 가능합니다. 9종 모두 실측에서 WPA3-SAE 핫스팟을 성공적으로 구축하고 장치를 연결시킬 수 있었습니다(ACS를 제외한 모든 카드는 2.4 GHz에서, ACS는 5 GHz에서 실측했으며 AXML은 6 GHz에서도 실측했습니다). 다만 AWUS036ACHM만 hostapd의 `sae_pwe`를 0으로 설정해야 하며, 그렇지 않으면 구형 iPhone 7 Plus가 연결에 실패합니다.

**Q: 이 Ubuntu 테스트 결과를 Kali Linux 사용자가 참고할 수 있나요?**
A: Kali Linux는 Debian/Ubuntu 체계를 기반으로 하며 동일한 rtw88 / rtw89 / mt76 인커널 드라이버를 사용하므로, 본문의 드라이버 호환성과 능력 매트릭스는 원칙적으로 Kali 사용자의 참고 근거가 될 수 있습니다. 다만 본문의 실측 플랫폼은 Ubuntu 24.04이며 Kali에서 정식으로 재측정하지는 않았으니, 결과는 추후 재측정을 기준으로 삼으시기 바랍니다.

## 더 읽어보기

이 글은 종합표 허브입니다. 아래 심화 문서와 카드별 실측이 순차적으로 공개됩니다(링크 준비 중).

- 《드라이버 설치 불필요: Ubuntu(ARM64)에서 Monitor와 AP 모드 활성화》 → [`/ko/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/ko/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 《WPA3-SAE 핸드셰이크 캡처 실무(본인 소유 환경 검증)》 → [`/ko/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/ko/blog/alfa-wpa3-sae-handshake-capability-arm64/)

카드별 심화 실측 9편:

- [AWUS036ACM 단일 카드 실측](/ko/blog/awus036acm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACHM 단일 카드 실측](/ko/blog/awus036achm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACH 단일 카드 실측](/ko/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- [AWUS036ACS 단일 카드 실측](/ko/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- [AWUS036EACS 단일 카드 실측](/ko/blog/awus036eacs-asus-gx10-ubuntu-test-report/)
- [AWUS036AX 단일 카드 실측](/ko/blog/awus036ax-asus-gx10-ubuntu-test-report/)
- [AWUS036AXER 단일 카드 실측](/ko/blog/awus036axer-asus-gx10-ubuntu-test-report/)
- [AWUS036AXM 단일 카드 실측](/ko/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- [AWUS036AXML 단일 카드 실측](/ko/blog/awus036axml-asus-gx10-ubuntu-test-report/)

---

*테스트 기관: Yopitek(ALFA Network 대만 총판) | 테스트 플랫폼: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | 테스트 장치: Apple iPhone 7 Plus(WPA3는 iPhone 15 Pro로 별도 측정) | 테스트 환경: 자사 사무실 Wi-Fi. 본문은 제품 호환성과 능력 검증이며, 제3자 네트워크를 겨냥한 조작 튜토리얼이 아닙니다.*
