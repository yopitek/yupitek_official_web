---
title: "ALFA AWUS036ACH — AC1200 듀얼 밴드 고출력 USB-C 무선 어댑터"
description: "ALFA AWUS036ACH, Realtek RTL8812AU, AC1200 듀얼 밴드, USB-C, 탈착식 5 dBi 듀얼 안테나. 모니터 모드와 패킷 인젝션을 지원하는 Kali Linux 침투 테스트의 표준 어댑터."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB-C", "Dual Antenna", "Monitor Mode", "Kali Linux", "Security Research"]
faq:
  - question: "AWUS036ACH는 Linux에서 드라이버 설치가 필요합니까?"
    answer: "대부분의 경우 필요합니다. Realtek RTL8812AU 칩셋은 일반적으로 최초 1회 수동 DKMS 드라이버 설치가 필요하며, 커널 업데이트 후에는 DKMS가 다시 빌드합니다. 커널 6.13 이상에서는 커널 내장 드라이버를 사용할 수 있습니다."
  - question: "AWUS036ACH는 모니터 모드와 패킷 인젝션을 지원합니까?"
    answer: "예. Kali Linux에서 aircrack-ng 드라이버를 사용하면 모니터 모드와 패킷 인젝션을 완전히 지원합니다. 이 기능은 승인된 보안 테스트 목적으로만 사용하십시오."
  - question: "AWUS036ACH는 Windows와 macOS에서 동작합니까?"
    answer: "Windows 10 및 11과 Linux에서 동작합니다. macOS 지원은 제한적입니다. macOS 10.15 Catalina에서는 수동 설치가 필요하며, macOS 11 이상과 Apple Silicon은 지원되지 않습니다."
---

{{< alert "warning" >}}
**법적 고지**: 모니터 모드 및 패킷 인젝션 기능은 승인된 보안 테스트, 교육 연구 및 합법적인 침투 테스트 목적으로만 사용해야 합니다. 대상 네트워크에 대한 명시적인 승인을 받았는지 확인하십시오.
{{< /alert >}}

## 제품 개요

AWUS036ACH는 Alfa Network의 가장 상징적인 보안 연구용 어댑터로, 2017년 이래 Kali Linux 침투 테스트의 표준으로 자리잡았습니다. 검증된 Realtek RTL8812AU 칩셋을 기반으로 안정적인 모니터 모드와 패킷 인젝션 지원, 장거리 수신을 위한 내장 파워 앰프, 탈착식 5 dBi 안테나 2개를 제공합니다. USB Type-C 커넥터를 갖춘 세계 최초의 WiFi 5 어댑터이기도 합니다.

> **macOS 안내:** 모든 ALFA 어댑터는 macOS 지원이 제한적이거나 지원되지 않습니다. macOS 11 Big Sur 이상 및 Apple Silicon(M1/M2/M3)은 **지원되지 않습니다**. macOS 지원은 Intel Mac의 10.15 Catalina까지입니다.

## 주요 특징

- Realtek RTL8812AU - WiFi 보안 연구에서 가장 널리 검증된 칩셋
- WiFi 5 AC1200 듀얼 밴드: 5 GHz 867 Mbps + 2.4 GHz 300 Mbps
- 내장 파워 앰프 - 일반 노트북 카드 대비 최대 3배의 도달 거리
- RP-SMA female 2개와 탈착식 5 dBi 듀얼 밴드 안테나 2개 (업그레이드 가능)
- 세계 최초의 WiFi 5 USB-C 어댑터
- 스크린 클립 마운트 포함
- Kali Linux 2017.1부터 지원

## 기술 사양

| 항목 | 값 |
|------|------|
| 칩셋 | Realtek RTL8812AU |
| WiFi 표준 | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| 주파수 대역 | 듀얼 밴드 2.4 GHz / 5 GHz |
| 최대 데이터 전송률 | 802.11n: 300 Mbps · 802.11ac: 867 Mbps |
| 합산 최대 속도 | AC1200 (867 + 300 Mbps) |
| 안테나 커넥터 | RP-SMA female 2개 |
| 포함 안테나 | 듀얼 밴드 다이폴 무지향성 2개, 5 dBi |
| USB 인터페이스 | Type-C SuperSpeed (5 Gbps), USB 2.0 하위 호환 |
| 파워 앰프 | 있음 - 도달 거리 확장 |
| 무선 보안 | WPA3 / WPA2 / WPA / WEP / WPS / 802.1X |
| 원산지 | 대만 |

## OS 지원

| OS | 상태 | 비고 |
|------|---------|------|
| Windows 10/11 | ✅ 지원 | Alfa 웹사이트에서 드라이버 다운로드, WPA3 지원 |
| macOS 10.15 Catalina | ⚠️ 제한적 | 수동 설치, macOS 11 이상 및 Apple Silicon 미지원 |
| Ubuntu | ✅ 지원 | RTL8812AU DKMS 수동 설치, 커널 ≥ 6.13에서는 커널 내장(rtw88_8812au) |
| Kali Linux | ✅ 우수 | Kali 2017.1부터, 모니터 모드 + 패킷 인젝션 완전 지원, aircrack-ng 드라이버 사용 |
| NetHunter (Android) | ✅ 지원 | OTG USB, 동작이 폭넓게 확인됨 |

## 하드웨어 지원

| 하드웨어 | 상태 | 비고 |
|------|---------|------|
| Raspberry Pi 3B+/4/5 | ✅ 지원 | morrownr DKMS 스크립트로 수동 드라이버 설치 |
| 데스크톱/노트북 PC | ✅ 지원 | 포함된 케이블을 통해 USB-C 또는 USB-A 사용 |
| Mac (Intel) | ⚠️ 제한적 | 최대 macOS 10.15 Catalina |

## 고급 기능

| 기능 | 상태 |
|------|------|
| 모니터 모드 | ✅ 우수 (표준 - 2017년 이래 커뮤니티에서 검증됨) |
| 패킷 인젝션 | ✅ 우수 |
| Soft AP 모드 | ✅ 지원 |
| Bluetooth | ❌ 없음 |
| VIF | ⚠️ 제한적 |

## 패키지 구성

- AWUS036ACH 어댑터 1개
- 탈착식 5 dBi 듀얼 밴드 다이폴 안테나 2개
- USB-C to USB-A 케이블 1개
- 스크린 클립 마운트 1개

## 리소스 및 링크

| 리소스 | 링크 |
|------|------|
| 공식 제품 페이지 | https://www.alfa.com.tw/products/awus036ach_1 |
| 공식 문서 | https://docs.alfa.com.tw/Product/AWUS036ACH/ |
| 드라이버 (aircrack-ng, Kali에 최적) | https://github.com/aircrack-ng/rtl8812au |
| 드라이버 (morrownr, 일반 Linux) | https://github.com/morrownr/8812au-20210708 |

## 제품 데이터시트

| 문서 | 다운로드 |
|------|------|
| 공식 데이터시트(PDF) | [📄 AWUS036ACH 데이터시트 다운로드](/docs/alfa/AWUS036ACH_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ach_image_1.png" alt="ALFA AWUS036ACH" />
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
