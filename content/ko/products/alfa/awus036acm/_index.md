---
title: "ALFA AWUS036ACM — AC1200 듀얼 밴드 USB 3.0 어댑터 (Linux 플러그 앤 플레이 최적)"
description: "ALFA AWUS036ACM, MediaTek MT7612U, AC1200 듀얼 밴드 USB 3.0, 커널 4.19부터 Linux 내장 드라이버 제공(플러그 앤 플레이, 컴파일 불필요). 모니터 모드, 패킷 인젝션, VIF를 완전 지원합니다. Raspberry Pi용 최적의 Alfa 어댑터."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB 3.0", "Dual-Band", "Monitor Mode", "Kali Linux", "Raspberry Pi"]
faq:
  - question: "AWUS036ACM은 Linux에서 드라이버 설치가 필요합니까?"
    answer: "아니요. MediaTek MT7612U 칩셋을 사용하며, mt76x2u 드라이버가 Linux 커널 4.19부터 포함되어 있으므로 최신 Kali Linux 및 Ubuntu 릴리스에서 바로 동작합니다."
  - question: "AWUS036ACM은 모니터 모드와 패킷 인젝션을 지원합니까?"
    answer: "예. 커널 내장 드라이버로 iw, aircrack-ng 같은 표준 도구를 통해 모니터 모드와 패킷 인젝션이 동작합니다. 승인된 보안 테스트 목적으로만 사용하십시오."
  - question: "AWUS036ACM의 안테나를 교체할 수 있습니까?"
    answer: "예. RP-SMA female 커넥터 2개와 탈착식 5 dBi 듀얼 밴드 안테나가 있어, ALFA 패널 안테나나 고이득 안테나 같은 호환 RP-SMA 안테나로 교체할 수 있습니다."
---

{{< alert "warning" >}}
**법적 고지**: 모니터 모드 및 패킷 인젝션 기능은 승인된 보안 테스트, 교육 연구 및 합법적인 침투 테스트 목적으로만 사용해야 합니다. 사용 전에 대상 네트워크 소유자의 명시적인 승인을 받았는지 확인하십시오.
{{< /alert >}}

## 제품 개요

AWUS036ACM은 번거로움 없는 설정을 원하는 Linux 사용자에게 가장 먼저 추천하는 제품입니다. MediaTek MT7612U 칩셋은 Linux 커널 4.19부터 내장되어 있어 Ubuntu, Kali Linux, Raspberry Pi OS, Arch Linux 등 거의 모든 최신 배포판에서 코드를 한 줄도 컴파일하지 않고 바로 동작합니다. 물리적 크기와 안테나 구성은 AWUS036ACH와 동일하지만 MediaTek의 안정적인 커널 내장 드라이버를 사용합니다. 모니터 모드, 패킷 인젝션, VIF(Virtual Interface)를 모두 완전히 지원합니다.

> **macOS 안내:** 모든 ALFA 어댑터는 macOS 지원이 제한적이거나 지원되지 않습니다. macOS 11 이상 및 Apple Silicon(M1/M2/M3)은 **지원되지 않습니다**. AWUS036ACM은 최대 macOS 10.12 Sierra까지 지원하며, 다른 대부분의 모델보다 제약이 큽니다.

## 주요 특징

- MediaTek MT7612U 칩셋 - 커널 4.19부터 Linux 내장 드라이버 제공 (플러그 앤 플레이, 컴파일 불필요)
- WiFi 5(802.11ac) 듀얼 밴드 AC1200 - 5 GHz에서 최대 867 Mbps, 2.4 GHz에서 300 Mbps
- RP-SMA female 커넥터 2개와 탈착식 5 dBi 듀얼 밴드 안테나 2개 - AWUS036ACH와 동일한 물리적 구성
- USB 3.0(USB-A) 인터페이스
- 모니터 모드, 패킷 인젝션, AP 모드 완전 지원
- Kali Linux에서 VIF(Virtual Interface) 지원
- USB 3.0 연장 케이블 포함
- TAA 준수 - 미국 정부 조달에 적합 (GSA 호환)
- Raspberry Pi OS에서 바로 동작 - 드라이버 설치 불필요

## 기술 사양

| 항목 | 값 |
|-----------|-------|
| 칩셋 | MediaTek MT7612U |
| WiFi 표준 | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| 주파수 대역 | 2.4 GHz (2.412–2.472 GHz) · 5 GHz (5.15–5.825 GHz) |
| 채널 폭 | 20 / 40 / 80 MHz |
| 최대 데이터 전송률 | 5 GHz: 최대 867 Mbps · 2.4 GHz: 최대 300 Mbps |
| 합산 최대 속도 | AC1200 (867 + 300 Mbps) |
| 안테나 커넥터 | RP-SMA female 2개 |
| 포함 안테나 | 듀얼 밴드 다이폴 2개, 이득 5 dBi |
| USB 인터페이스 | USB 3.0 Type-A (USB 2.0 하위 호환) |
| 출력 | 802.11a: 20 dBm · 802.11b: 23 dBm · 802.11g: 23 dBm · 802.11n: 21 dBm · 802.11ac: 20 dBm |
| 수신 감도 | 802.11a: −92 dBm · 802.11b: −97 dBm · 802.11g: −90 dBm · 802.11n: −90 dBm |
| 무선 보안 | WPA2 / WPA / WEP / WPA-PSK / 802.1X |
| LED | 있음 (전원 + WLAN 활동) |
| 액세서리 | USB 3.0 연장 케이블 |
| 원산지 | 대만 |

## OS 지원

| OS | 상태 | 비고 |
|----|--------|-------|
| Windows XP–11 | ✅ 지원 | Alfa 웹사이트의 드라이버 사용. Windows 10/11 권장. |
| macOS 10.7–10.12 | ⚠️ 제한적 | 공식 지원은 macOS 10.12 Sierra까지. macOS 11 이상 및 Apple Silicon은 미지원. |
| Ubuntu 19.04+ | ✅ 플러그 앤 플레이 | 커널 내장 mt76x2u 드라이버(커널 ≥ 4.19). Ubuntu 20.04 LTS 이상에서는 드라이버 설치 불필요. |
| Kali Linux 2019.3+ | ✅ 플러그 앤 플레이 | 커널 내장 드라이버. 모니터 모드 확인됨. VIF(Virtual Interface) 지원. 5 GHz AP 모드는 `disable_usb_sg` 모듈 파라미터가 필요할 수 있음. |
| NetHunter (Android) | ✅ 지원 | OTG USB, 커널 내장 드라이버이므로 RTL 어댑터보다 Android 호환 범위가 넓음. |

## 하드웨어 지원

| 하드웨어 | 상태 | 비고 |
|----------|--------|-------|
| Raspberry Pi 3B+/4/5 | ✅ 우수 | Raspberry Pi OS에서 바로 동작하며 드라이버 설치가 필요 없습니다. Pi용 최적의 Alfa 어댑터. |
| 데스크톱/노트북 PC | ✅ 지원 | 표준 USB-A, 연장 케이블 포함. |
| Mac (Intel) | ⚠️ 제한적 | macOS 10.7–10.12만 지원. |

## 고급 기능

| 기능 | 상태 |
|---------|--------|
| 모니터 모드 | ✅ 지원 (커널 내장, 최신 배포판에서 추가 작업 불필요) |
| 패킷 인젝션 | ✅ 지원 |
| Soft AP 모드 | ✅ 지원 (5 GHz AP: 최적 성능을 위해 `disable_usb_sg` 모듈 파라미터 추가) |
| Bluetooth | ❌ 없음 |
| VIF (Virtual Interface) | ✅ 지원 (Kali에서 완전한 VIF 지원) |

## 패키지 구성

- AWUS036ACM 어댑터 1개
- 탈착식 5 dBi 듀얼 밴드 다이폴 안테나 2개
- USB 3.0 연장 케이블 1개
- 드라이버 CD 1장 (Windows)

## 리소스 및 링크

| 리소스 | 링크 |
|----------|------|
| 공식 제품 페이지 | https://www.alfa.com.tw/products/awus036acm_1 |
| 공식 문서 | https://docs.alfa.com.tw/Product/AWUS036ACM/ |
| Linux 드라이버 정보 (커널 내장) | mt76x2u 드라이버 - Linux 커널 ≥ 4.19에 포함, 설치 불필요 |

## 데이터시트 다운로드

| 문서 | 다운로드 |
|----------|----------|
| 공식 데이터시트(PDF) | [📄 AWUS036ACM 데이터시트 다운로드](/docs/alfa/AWUS036ACM_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036acm_image_1.png" alt="ALFA AWUS036ACM" />
{{< /gallery >}}

---

## 호환 안테나 업그레이드

모든 ALFA 어댑터는 표준 RP-SMA 커넥터를 사용합니다. 별도의 외장 안테나로 업그레이드하면 더 넓은 도달 거리와 높은 이득을 얻을 수 있습니다.

| 안테나 | 주파수 | 이득 | 유형 |
|---------|-----------|------|------|
| [ALFA APA-M04](/ko/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | 실내용 패널 |
| [ALFA APA-M25](/ko/products/alfa/apa-m25/) | 2.4 / 5 GHz | 8 / 10 dBi | 듀얼 밴드 실내용 패널 |
| [ALFA APA-M25-6E](/ko/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 8 / 10 / 9 dBi | 트라이 밴드 실내용 패널 |
| [ARS 25-57A](/ko/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 5 / 7 dBi | 옥외용 무지향성 |
| [ARS NT5B7](/ko/products/alfa/ars-nt5b7/) | 2.4 / 5 / 6 GHz | 4 / 5 / 7 dBi | 무지향성 |

{{< alert >}}
제품 견적이 필요하십니까? [문의해 주십시오](/ko/contact/)
{{< /alert >}}

{{< faq >}}
