---
title: "ALFA AWUS036ACS — AC600 듀얼 밴드 USB 어댑터 (보급형 보안 연구용)"
description: "ALFA AWUS036ACS, Realtek RTL8811AU, AC600 듀얼 밴드 USB 2.0, 2 dBi RP-SMA 탈착식 안테나 1개, 모니터 모드와 패킷 인젝션 지원 - 입문용 보안 연구 어댑터로 적합합니다."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "RP-SMA", "Monitor Mode", "Kali Linux", "Budget"]
---

{{< alert "warning" >}}
**법적 고지**: 모니터 모드 및 패킷 인젝션 기능은 승인된 보안 테스트, 교육 연구 및 합법적인 침투 테스트 목적으로만 사용해야 합니다. 사용 전에 대상 네트워크 소유자의 명시적인 허가를 받았는지 항상 확인하십시오.
{{< /alert >}}

## 제품 개요

AWUS036ACS는 모니터 모드와 패킷 인젝션을 지원하는 Alfa 듀얼 밴드 802.11ac 라인업 중 가장 저렴한 입문 모델입니다. Realtek RTL8811AU 칩셋을 탑재하였으며, 컴팩트하고 가벼우며 탈착식 RP-SMA 안테나 1개를 갖추고 있어 도달 거리 향상을 위해 업그레이드할 수 있습니다. ACH 또는 ACM만큼 강력하지는 않지만, 무선 보안 연구를 시작하는 입문자나 외장 안테나 연결이 가능한 저렴한 5 GHz 어댑터가 필요한 사용자에게 실용적인 선택입니다.

> **macOS 안내:** 모든 ALFA 어댑터는 macOS 지원이 제한적입니다. macOS 10.15 Catalina 이상 및 모든 Apple Silicon(M1/M2/M3) Mac은 **지원되지 않습니다**. AWUS036ACS는 macOS 10.14 Mojave(Intel Mac 전용)까지 지원합니다.

## 주요 특징

- Realtek RTL8811AU 칩셋 - 모니터 모드와 패킷 인젝션 지원
- WiFi 5(802.11ac) 듀얼 밴드 - 2.4 GHz (150 Mbps) + 5 GHz (433 Mbps) = AC600
- RP-SMA female 커넥터 1개와 2 dBi 미니 탈착식 안테나 1개 - 패널 안테나 또는 고이득 안테나로 업그레이드 가능
- 컴팩트한 폼팩터 - 작은 크기로 휴대가 간편
- USB 2.0(USB-A) 인터페이스 - 모든 USB 포트와 호환
- 지향성 수신을 위해 Alfa APA-M25 듀얼 밴드 패널 안테나와 호환
- Raspberry Pi의 Kali Linux(KaliPi) 지원 - DKMS를 통한 드라이버 설치

## 기술 사양

| 항목 | 값 |
|---|---|
| 칩셋 | Realtek RTL8811AU |
| WiFi 표준 | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| 주파수 대역 | 2.4 GHz (150 Mbps) · 5 GHz (433 Mbps) |
| 합산 최대 속도 | AC600 (150 + 433 Mbps) |
| 안테나 커넥터 | RP-SMA female 1개 |
| 포함 안테나 | 듀얼 밴드 다이폴 미니 1개, 이득 2 dBi |
| USB 인터페이스 | USB 2.0 Type-A |
| 수신 감도 | 802.11b: −85 dBm · 802.11g: −69 dBm · 802.11n: −68 dBm · 802.11ac: −59 dBm |
| 무선 보안 | WPA2 / WPA / WEP / 802.1X |
| 원산지 | 대만 |

> ⚠️ **참고:** USB 2.0 전용 - 데이터 버스 속도는 최대 480 Mbps입니다. 처리량은 433 Mbps로 제한됩니다. 최대 속도가 필요하면 USB 3.0을 사용하는 AWUS036ACM 또는 AWUS036ACH를 사용하십시오.

## OS 지원

| OS | 상태 | 비고 |
|---|---|---|
| Windows XP–11 | ✅ 지원 | Alfa 웹사이트에서 드라이버 제공 |
| macOS 10.5–10.14 | ⚠️ 제한적 | macOS 10.15 이상 및 Apple Silicon 미지원 |
| Ubuntu | ✅ 지원 | 커널 ≥ 6.13에서는 mainline rtw88_8821au 드라이버 사용. 이전 커널에서는 DKMS 드라이버 수동 설치 필요(morrownr/8821au). |
| Kali Linux | ✅ 지원 | 모니터 모드 + 패킷 인젝션 지원(GX10, Ubuntu 24.04, 커널 6.17: 인젝션 2.4 GHz 100%, 5 GHz 96%). 커널 6.13 이상에서는 mainline 드라이버, 이전 커널에서는 morrownr 커뮤니티 드라이버를 사용합니다. 실제 Kali 설치 환경에서는 테스트하지 않았습니다. |
| NetHunter (Android) | ✅ 지원 | OTG USB 연결, RTL8811AU는 NetHunter 호환성이 확인됨 |

## 하드웨어 지원

| 하드웨어 | 상태 | 비고 |
|---|---|---|
| Raspberry Pi 3B+/4/5 | ✅ 지원 | morrownr DKMS를 통한 KaliPi 전용 설치 제공. |
| 데스크톱/노트북 PC | ✅ 지원 | 표준 USB-A |
| Mac (Intel) | ⚠️ 제한적 | macOS 10.5–10.14만 지원 |

## 고급 기능

| 기능 | 상태 |
|---|---|
| 모니터 모드 | ✅ 지원 |
| 패킷 인젝션 | ✅ 지원 |
| Soft AP 모드 | ✅ 지원 |
| Bluetooth | ❌ 없음 |
| VIF | ⚠️ 제한적 |

## 패키지 구성

- AWUS036ACS 어댑터 1개
- 탈착식 2 dBi 듀얼 밴드 미니 다이폴 안테나 1개

## 리소스 및 링크

| 리소스 | 링크 |
|---|---|
| 공식 제품 페이지 | https://www.alfa.com.tw/products/awus036acs_1 |
| 공식 문서 | https://docs.alfa.com.tw/Product/AWUS036ACS/ |
| Linux 드라이버 (RTL8811AU) | https://github.com/morrownr/8821au-20210708 |

## 데이터시트 다운로드

[📄 AWUS036ACS 데이터시트 다운로드](/docs/alfa/AWUS036ACS_spec.pdf)

## 갤러리

{{< gallery >}}<img src="/images/products/alfa/awus036acs_image_1.png" alt="ALFA AWUS036ACS" />{{< /gallery >}}

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
