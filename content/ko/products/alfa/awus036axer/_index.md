---
title: "ALFA AWUS036AXER — Wi-Fi 6 초슬림 나노 USB 어댑터"
description: "Realtek RTL8832BU 칩셋을 탑재한 ALFA AWUS036AXER. Wi-Fi 6 듀얼 밴드 나노 폼팩터(약 65×24×10mm). 커널 6.17 이상에서 mainline rtw89_8852bu 드라이버를 사용하며, GX10에서 모니터 모드와 패킷 인젝션을 확인했습니다."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6", "802.11ax", "Ultra-Slim", "USB 3.2", "Portable", "Nano"]
---

## 제품 개요

AWUS036AXER은 Realtek RTL8832BU 칩셋을 탑재하고 Wi-Fi 6(802.11ax) 듀얼 밴드(2.4 GHz + 5 GHz)를 지원하며, 최대 1800 Mbps(2.4 GHz: 573 Mbps + 5 GHz: 1200 Mbps)를 제공합니다. 휴대용 일상 사용을 위한 초슬림 나노 설계(약 65 × 24 × 10 mm, 약 10g)입니다.

> ⚠️ **참고:** 나노 폼팩터로 **RP-SMA 커넥터가 없어** 안테나를 업그레이드할 수 없습니다. GX10(Ubuntu 24.04, 커널 6.17)에서 mainline rtw89_8852bu 드라이버로 모니터 모드와 패킷 인젝션이 모두 테스트를 통과했습니다(인젝션: 2.4 GHz 73%, 5 GHz 동작).

> **macOS 안내:** 모든 ALFA 어댑터는 macOS 지원이 제한적이거나 지원되지 않습니다. macOS 11 Big Sur 이상 및 Apple Silicon(M1/M2/M3)은 **지원되지 않습니다**. macOS 지원은 Intel Mac의 10.15 Catalina까지입니다.

## 주요 특징

- Wi-Fi 6(802.11ax) 듀얼 밴드: 2.4 GHz + 5 GHz
- Realtek RTL8832BU 칩셋
- 최대 1800 Mbps
- 초슬림 나노 설계(약 65×24×10mm, 약 10g)
- USB 3.2 Gen 1 Type-A
- WPA3/WPA2/WPA/WEP
- ⚠️ RP-SMA 커넥터 없음, 내장 안테나

## 기술 사양

| 항목 | 사양 |
|------|---------------|
| 칩셋 | Realtek RTL8832BU |
| WiFi 표준 | IEEE 802.11 a/b/g/n/ac/ax (WiFi 6) |
| 주파수 대역 | 2.4 GHz + 5 GHz (6 GHz 미지원) |
| 최대 데이터 전송률 | 1800 Mbps (2.4G: 573 Mbps + 5G: 1200 Mbps) |
| 안테나 | 내장 나노형 (RP-SMA 없음) |
| USB 인터페이스 | USB 3.2 Gen 1 Type-A |
| 크기 | 약 65 × 24 × 10 mm, 약 10g |
| 무선 보안 | WPA3 / WPA2 / WPA / WEP |

## OS 지원

| OS | 상태 | 비고 |
|----|--------|-------|
| Windows 10/11 | ✅ 지원 | ALFA 웹사이트의 드라이버 사용 |
| macOS | ❌ 미지원 | macOS 11 이상 및 Apple Silicon 미지원 |
| Ubuntu | ✅ 커널 6.17 이상 | mainline rtw89_8852bu 드라이버(Linux 6.17부터 포함). 이전 커널에서는 커뮤니티 rtl8852bu 드라이버를 DKMS로 빌드해야 함 |
| Kali Linux | ✅ 지원 | GX10(Ubuntu 24.04, 커널 6.17)에서 mainline 드라이버로 모니터 모드와 패킷 인젝션 확인됨. 이전 커널에서는 DKMS 드라이버가 필요합니다. 실제 Kali 설치 환경에서는 테스트하지 않았습니다 |
| NetHunter | ⚠️ 제한적 | 커널에 따라 다름 |

## 하드웨어 지원

| 하드웨어 | 상태 | 비고 |
|----------|--------|-------|
| Raspberry Pi 4/5 | ⚠️ 드라이버 필요 | Pi OS에서는 DKMS 드라이버를 수동으로 설치해야 함 |
| 데스크톱/노트북 PC | ✅ 지원 | 표준 USB-A |

## 고급 기능

| 기능 | 상태 |
|---------|--------|
| 모니터 모드 | ✅ 지원 (mainline rtw89_8852bu, 커널 6.17 이상, GX10 테스트에서 수신 감도 우수) |
| 패킷 인젝션 | ✅ 지원 (GX10 테스트: 2.4 GHz 73%, 5 GHz 동작) |
| Soft AP 모드 | ✅ 지원 |
| Bluetooth | ❌ 없음 |

## 패키지 구성

- AWUS036AXER 나노 어댑터 1개

## 리소스 및 링크

| 리소스 | 링크 |
|----------|------|
| 공식 문서 | https://docs.alfa.com.tw/ |
| Linux 드라이버 (RTL8832BU) | https://github.com/morrownr/rtl8852bu-20250826 |

## 제품 데이터시트

| 문서 | 다운로드 |
|------|------|
| 공식 데이터시트(PDF) | [📄 AWUS036AXER 데이터시트 다운로드](/docs/alfa/AWUS036AXER_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axer_image_1.png" alt="ALFA AWUS036AXER" />
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
