---
title: "ALFA Network USB Wi-Fi 어댑터 비교"
description: "ALFA Network USB Wi-Fi 어댑터 9종의 상세 사양 비교: 칩셋, Linux 드라이버, Monitor／Injection／AP 지원 여부와 ASUS GX10(Ubuntu 24.04 ARM64, kernel 6.17) 실측 결과."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
---

아래 표는 ALFA Network USB Wi-Fi 어댑터 9종의 전체 사양을 정리한 것입니다. Monitor, Injection, AP 및 엔드투엔드 handshake 열은 Yopitek이 ASUS GX10(Ubuntu 24.04 LTS / ARM64 / kernel 6.17)에서 자사 장비와 자사 사무실 Wi-Fi로 측정한 실측 결과이며, 데이터시트 수치를 옮긴 것이 아닙니다.

## 전체 사양 비교

모바일에서는 표를 좌우로 스크롤하세요. 모델명을 누르면 제품 페이지로 이동합니다.

| 모델 | Wi-Fi 세대 | 칩셋 | 주파수 대역 | 최대 속도 | USB 인터페이스 | 안테나 | MIMO | 모니터 모드 | 패킷 인젝션 | 엔드투엔드 handshake (GX10 실측) | Linux 드라이버 | 드라이버 유형 | AP 모드 | 최대 소비 전력 | 블루투스 | 권장 용도 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [AWUS036AXML](/ko/products/alfa/awus036axml/) | WiFi 6E | MT7921AUN | 2.4 + 5 + 6 GHz | 3000 Mbps | USB-C 3.2 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 지원 | ❌ 기본 6.17 커널에서 실패 | ❌ 미지원 (인젝션 실패) | 커널 내장 ≥5.18 | 커널 내장 (플러그 앤 플레이) | ✅ 기본 지원 | 3.6W | BT 5.2 | Wi-Fi 6E + Linux + USB-C |
| [AWUS036AXM](/ko/products/alfa/awus036axm/) | WiFi 6E | MT7921AUN | 2.4 + 5 + 6 GHz(6 GHz 미검증) | 3000 Mbps | USB-A 3.2 L | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 지원 | ❌ 기본 6.17 커널에서 실패 | ❌ 미지원 (인젝션 실패) | 커널 내장 ≥5.18 | 커널 내장 (플러그 앤 플레이) | ✅ 기본 지원 | 3.6W | BT 5.2 | Wi-Fi 6E + 듀얼 안테나 |
| [AWUS036AX](/ko/products/alfa/awus036ax/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1200 Mbps | USB-A 3.2 Gen 1 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 지원 | ✅ 지원 | ✅ 엔드투엔드 (.22000) | 커널 내장 ≥6.17 | 커널 내장 (플러그 앤 플레이) | ✅ 기본 지원 | 3.6W | — | Wi-Fi 6 + AP 핫스팟 |
| [AWUS036AXER](/ko/products/alfa/awus036axer/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1800 Mbps | USB-A 3.2 | 내장(nano) | 2×2 MIMO | ✅ 지원 | ✅ 지원 | ✅ 엔드투엔드 (.22000) | 커널 내장 ≥6.17 | 커널 내장 (플러그 앤 플레이) | ✅ 기본 지원 | 3.0W | — | 소형 휴대용 어댑터 |
| [AWUS036ACH](/ko/products/alfa/awus036ach/) | WiFi 5 | RTL8812AU | 2.4 + 5 GHz | 867 Mbps | USB-C 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅✅ 최적 | ✅✅ 최적 | ✅ 엔드투엔드 (.22000) | 커널 내장 ≥6.13 | 커널 내장 (플러그 앤 플레이) | ✅ 기본 지원 | 3.6W | — | Kali Linux 표준 선택 |
| [AWUS036ACM](/ko/products/alfa/awus036acm/) | WiFi 5 | MT7612U | 2.4 + 5 GHz | 867 Mbps | USB-A 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 지원 | ✅ 지원 | ✅ 엔드투엔드 (.22000) | 커널 내장 ≥4.19 | 커널 내장 (플러그 앤 플레이) | ✅ 기본 지원 | 3.0W | — | Linux 플러그 앤 플레이 |
| [AWUS036ACHM](/ko/products/alfa/awus036achm/) | WiFi 5 | MT7610U | 2.4 + 5 GHz | 433 Mbps | USB 2.0 | 1× RP-SMA 5dBi | 1×1 SISO | ✅ 지원 | ✅ 2.4 GHz / ⚠️ 5 GHz 브로드캐스트만 가능 | ✅ 엔드투엔드 (.22000) | 커널 내장 ≥4.19 | 커널 내장 (플러그 앤 플레이) | ✅ 기본 지원 | — | — | 소형 AC600, Linux 플러그 앤 플레이 |
| [AWUS036ACS](/ko/products/alfa/awus036acs/) | WiFi 5 | RTL8811AU | 2.4 + 5 GHz | 433 Mbps | USB-A 2.0 | 1× RP-SMA 2dBi | 1×1 SISO | ✅ 지원 | ✅ 지원 | ✅ 엔드투엔드 (.22000) | 커널 내장 ≥6.13 | 커널 내장 (플러그 앤 플레이) | ✅ 기본 지원 (5 GHz는 802.11a 20 MHz로 시험, VHT80은 미시험) | 2.5W | — | 가성비 보안 테스트 |
| [AWUS036EACS](/ko/products/alfa/awus036eacs/) | WiFi 5 | RTL8821CU | 2.4 + 5 GHz | 433 Mbps | USB 2.0 nano | 내장 2dBi | 1×1 SISO | ✅ 지원 | ✅✅ 최적 | ✅ 엔드투엔드 (.22000) | 커널 내장 ≥6.2 | 커널 내장 (플러그 앤 플레이) | ✅ 기본 지원 (5 GHz는 802.11a 20 MHz로 시험, VHT80은 미시험) | 2.5W | BT 4.2 | Windows 가정용 Wi-Fi + 블루투스 |

## 용도별 빠른 선택 가이드

**🔴 Kali Linux / 침투 테스트** — 추천: AWUS036ACH

RTL8812AU — Kali에서 모니터 모드와 패킷 인젝션 지원이 가장 성숙함. GX10(kernel 6.17)에서 두 대역 모두 인젝션 성공률 100%. 커널 내장 rtw88_8812au 드라이버는 6.13부터 제공. 팁: 오래된 커널에서는 안정 commit 63cf0b4로 고정한 aircrack-ng DKMS 드라이버를 사용하세요.

**🔵 WiFi 6E (트라이밴드) 고급 사용자** — 추천: AWUS036AXML or AWUS036AXM

MT7921AUN — Linux 커널 내장 드라이버는 5.18부터 제공. 6 GHz 대역 지원(AXML에서 확인, AXM은 미시험), 블루투스 5.2. 참고: 기본 kernel 6.17에서는 패킷 인젝션이 실패하므로(6.16 이후의 mac80211 회귀) 침투 테스트에는 적합하지 않습니다. 폼팩터: AXML은 분리형 USB-C 커넥터와 듀얼 출력을 갖춘 단일 안테나 본체이며, AXM은 일체형 L자 USB-A 형태입니다.

**🌐 Soft-AP / 핫스팟 에뮬레이션** — 추천: AWUS036ACM

MT7612U — Linux 커널 기본 hostapd로 플러그 앤 플레이 AP 모드를 지원합니다. 별도 빌드한 hostapd가 필요하고 문제가 잦은 Realtek 어댑터와 달리 MediaTek은 매끄럽고 안정적이어서 Rogue AP / Evil Twin 시뮬레이션에 적합합니다.

**🟢 Linux 일상 사용 (플러그 앤 플레이)** — 추천: AWUS036ACM

MT7612U — 커널 4.19부터 내장되어 Ubuntu / Debian / Fedora에서 별도 드라이버 설정이 필요 없습니다. 가장 손쉬운 Linux 환경입니다.

**🟣 Raspberry Pi / 임베디드** — 추천: AWUS036ACM

낮은 소비 전력과 커널 내장 드라이버 덕분에 Raspberry Pi에 적합합니다. 참고: 고출력 모델(ACH, AXML)은 최대 3.6W를 소비하므로 Pi에서 전압 강하와 연결 재설정을 막으려면 외부 전원 USB 허브가 필요합니다.

**🟡 가성비 / 입문용 보안 테스트** — 추천: AWUS036ACS

RTL8811AU — 모니터 모드와 패킷 인젝션을 지원하는 입문용 어댑터입니다. 단일 안테나의 소형 설계입니다.

**⚡ 소형 휴대용 어댑터** — 추천: AWUS036AXER

초박형 나노 본체로 무게는 10.5g에 불과합니다. WiFi 6(1800 Mbps), USB-A. 출장용으로 적합하며 Windows 중심 환경에 맞습니다.

**🏠 Windows 가정 사용자 + 블루투스** — 추천: AWUS036EACS

RTL8821CU — WiFi 5와 블루투스 4.2를 결합한 듀얼 모드 어댑터입니다. 나노 폼팩터. PCIe 슬롯 없이 무선과 블루투스를 간편하게 추가하려는 데스크톱에 적합합니다.

**🍎 macOS 호환성** — 추천: AWUS036ACH or AWUS036AXML

ACH는 서드파티 드라이버로 macOS에서 잘 동작합니다. AXML의 MT7921AUN은 커뮤니티 macOS 지원이 있습니다. 항상 macOS 버전 호환성을 확인하세요. Intel Mac은 M 시리즈보다 기존 드라이버 지원이 더 충실합니다.

## 플랫폼 / OS별 빠른 선택 가이드

| 플랫폼 / OS | 1순위 | 2순위 | 비고 |
|---|---|---|---|
| 🐧 Kali Linux | AWUS036ACH | AWUS036ACM | ACH = 모니터 모드 최상, ACM = 커널 지원이 가장 쉬움. 가상 머신 사용 시: 연결 끊김을 방지하려면 VM을 USB 3.0(xHCI) 컨트롤러로 설정하세요. |
| 🐧 Ubuntu / Debian | AWUS036ACM | AWUS036AXML | MT7612U는 4.19부터, MT7921AUN은 5.18부터 커널 내장 |
| 🐧 Raspberry Pi OS | AWUS036ACM | AWUS036ACH | 저전력에 커널 내장 드라이버라 수동 컴파일이 필요 없습니다. 고출력 카드는 리셋 방지를 위해 외부 전원 USB 허브를 권장합니다. |
| 🪟 Windows 10 / 11 | AWUS036AX | AWUS036EACS | WiFi 6 성능, EACS는 블루투스 콤보 추가 |
| 🍎 macOS | AWUS036ACH | AWUS036AXML | 서드파티 드라이버가 있으니 macOS 버전을 확인하세요. Intel Mac에는 기존 드라이버가 있으며, Apple Silicon(M1/M2/M3)은 제한적인 실험적 지원만 가능합니다. |
| 📱 Android / NetHunter | AWUS036ACH | AWUS036ACS | RTL8812AU와 RTL8811AU는 NetHunter를 지원하며, OTG 어댑터와 커널 직접 컴파일이 필요합니다. |

---

측정 환경: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia (2026-11). 어댑터별 상세 보고서는 [블로그](/ko/blog/)에서 확인하세요.
