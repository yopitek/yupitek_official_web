---
title: "ALFA AWUS036AXML — Wi-Fi 6E USB-C 트라이 밴드 USB 어댑터"
description: "MediaTek MT7921AUN 칩셋을 탑재한 ALFA AWUS036AXML. Wi-Fi 6E 트라이 밴드(2.4/5/6 GHz), USB-C 인터페이스, Bluetooth 5.2, Kali Linux 모니터 모드 지원."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6E", "USB-C", "802.11ax", "Tri-Band", "Bluetooth 5.2", "6GHz", "Kali Linux"]
faq:
  - question: "AWUS036AXML은 6 GHz 대역을 지원합니까?"
    answer: "예. MediaTek MT7921AUN 칩셋을 기반으로 2.4 GHz, 5 GHz, 6 GHz를 모두 지원하는 트라이 밴드 Wi-Fi 6E 어댑터입니다. Windows에서 6 GHz를 사용하려면 Windows 11이 필요합니다."
  - question: "AWUS036AXML은 Linux에서 드라이버 설치가 필요합니까?"
    answer: "DKMS 빌드는 필요하지 않습니다. mt7921u 드라이버는 Linux 커널 5.18부터 포함되어 있으므로 커널 5.18 이상(예: Ubuntu 22.10 이상, 또는 Ubuntu 22.04의 HWE 커널)이 필요합니다."
  - question: "AWUS036AXML에 Bluetooth가 포함되어 있습니까?"
    answer: "예. 동일한 USB-C 어댑터에 Bluetooth 5.2가 포함되어 있어 하나의 장치로 Wi-Fi와 Bluetooth를 모두 사용할 수 있습니다."
---

{{< alert "warning" >}}
**법적 고지**: 모니터 모드 및 패킷 인젝션 기능은 승인된 보안 테스트, 교육 연구 및 합법적인 침투 테스트 목적으로만 사용해야 합니다. 대상 네트워크에 대한 명시적인 승인을 받았는지 확인하십시오.
{{< /alert >}}

## 제품 개요

AWUS036AXML은 MediaTek MT7921AUN 칩셋을 탑재하고 Wi-Fi 6E 트라이 밴드(2.4 GHz / 5 GHz / 6 GHz)를 지원하며, 합산 최대 3000 Mbps의 처리량과 Bluetooth 5.2를 통합했습니다. USB-C 인터페이스에는 최신 노트북 및 데스크톱과의 호환성을 위해 2-in-1 USB-C/USB-A 케이블이 포함됩니다. 탈착식 RP-SMA 안테나 2개와 스크린 클립 마운트가 함께 제공됩니다.

> **macOS 안내:** 모든 ALFA 어댑터는 macOS 지원이 제한적이거나 지원되지 않습니다. macOS 11 Big Sur 이상 및 Apple Silicon(M1/M2/M3)은 **지원되지 않습니다**. macOS 지원은 Intel Mac의 10.15 Catalina까지입니다.

## 주요 특징

- Wi-Fi 6E 트라이 밴드: 2.4 / 5 / 6 GHz
- MediaTek MT7921AUN 칩셋
- 합산 최대 3000 Mbps 처리량
- Bluetooth 5.2 (콤보 칩)
- USB-C 인터페이스 (USB 3.2 Gen 1, 5 Gbps)
- 2-in-1 USB-C/USB-A 케이블 포함
- 탈착식 RP-SMA 안테나 2개
- 스크린 클립 마운트 포함
- WPA3/WPA2/WPA/WEP/WPS
- Kali Linux 모니터 모드 (커널 ≥ 5.18)

## 기술 사양

| 항목 | 사양 |
|------|---------------|
| 칩셋 | MediaTek MT7921AUN |
| WiFi 표준 | IEEE 802.11 a/b/g/n/ac/ax (WiFi 6E) |
| 주파수 대역 | 2.4 GHz (20/40 MHz) · 5 GHz (20/40/80 MHz) · 6 GHz (20/40/80 MHz) |
| 최대 데이터 전송률 | 2.4GHz: 600 Mbps · 5GHz: 1200 Mbps · 6GHz: 1200 Mbps · 합산: 3000 Mbps |
| Bluetooth | BT 5.2 (콤보 칩) |
| 안테나 커넥터 | RP-SMA female 2개 (탈착식) |
| USB 인터페이스 | USB 3.2 Gen 1 Type-C (5 Gbps) |
| 케이블 | 2-in-1 USB-C/USB-A |
| 무선 보안 | WPA3 / WPA2 / WPA / WEP / WPS |
| 원산지 | 대만 |

## OS 지원

| OS | 상태 | 비고 |
|----|--------|-------|
| Windows 10 | ✅ 지원 | 2.4 GHz 및 5 GHz만 지원, Win10에서는 6 GHz 사용 불가 |
| Windows 11 | ✅ 지원 | 6 GHz를 포함한 전체 트라이 밴드 |
| macOS | ❌ 미지원 | macOS 11 이상 및 Apple Silicon 미지원 |
| Ubuntu | ✅ 지원 | 커널 내장 mt7921u 드라이버, 커널 ≥ 5.18 (Ubuntu 22.10 이상) |
| Kali Linux | ⚠️ 부분 지원 | 모니터 모드: 커널 ≥ 5.18, active 모니터 모드: ≥ 6.12. 패킷 인젝션은 GX10 / stock 커널 6.17 자사 테스트에서 통과하지 못했습니다(커널 6.16 이상의 mac80211 chanctx 회귀이며 칩 자체의 한계가 아닙니다). 실제 Kali 설치 환경에서는 테스트하지 않았습니다 |
| NetHunter (Android) | ⚠️ 부분 지원 | OTG, 커널에 따라 다름 |

## 하드웨어 지원

| 하드웨어 | 상태 | 비고 |
|----------|--------|-------|
| Raspberry Pi 3B+/4/5 | ✅ 지원 | 최신 Pi OS(커널 ≥ 5.18), 펌웨어 파일 복사가 필요할 수 있음 |
| 데스크톱/노트북 PC | ✅ 지원 | 포함된 2-in-1 케이블을 통해 USB-C 또는 USB-A 사용 |
| Mac Intel | ⚠️ 제한적 | 최대 macOS 10.15 Catalina |

## 고급 기능

| 기능 | 상태 |
|---------|--------|
| 모니터 모드 | ✅ 지원 (커널 ≥ 5.18, active 모드 ≥ 6.12) |
| 패킷 인젝션 | ❌ 통과하지 못함 (자사 테스트, GX10, 커널 6.17) |
| Soft AP 모드 | ✅ 지원 |
| Bluetooth | ✅ BT 5.2 |
| VIF | ✅ 지원 |

## 패키지 구성

- AWUS036AXML 어댑터 1개
- 탈착식 다이폴 안테나 2개
- 2-in-1 USB-C/USB-A 케이블 1개
- 스크린 클립 마운트 1개

## 리소스 및 링크

| 리소스 | 링크 |
|----------|------|
| 공식 제품 페이지 | https://www.alfa.com.tw/products/awus036axml |
| 공식 문서 | https://docs.alfa.com.tw/ |
| Linux 드라이버 (커널 내장) | mt7921u - Linux 커널 ≥ 5.18에 내장 |

## 제품 데이터시트

| 문서 | 다운로드 |
|------|------|
| 공식 데이터시트(PDF) | [📄 AWUS036AXML 데이터시트 다운로드](/docs/alfa/AWUS036AXML_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axml_image_1.png" alt="ALFA AWUS036AXML" />
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
