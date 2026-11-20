---
title: "ALFA AWUS036EACS — AC600 + Bluetooth 4.2 나노 USB 어댑터"
description: "ALFA AWUS036EACS, Realtek RTL8821CU, AC600 듀얼 밴드, USB 2.0 나노 폼팩터, Bluetooth 4.2, Windows 가정용 사용자를 위해 설계되었습니다. 커널 6.2부터 mainline rtw88_8821cu 드라이버를 제공하며, GX10 테스트에서 두 대역 모두 모니터 모드와 인젝션을 통과했습니다."
date: 2026-03-12
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "Nano", "Bluetooth 4.2", "Windows", "Home"]
---

## 제품 개요

AWUS036EACS는 Alfa의 초소형 WiFi + Bluetooth 결합형 어댑터로, 하나의 작은 USB 동글로 두 가지 무선 연결을 사용하려는 가정 및 사무실 사용자를 위해 설계되었습니다. Realtek RTL8821CU 칩셋을 기반으로 AC600 듀얼 밴드 WiFi와 Bluetooth 4.2를 나노 폼팩터에 통합했으며 Windows에서는 내장 드라이버를 지원합니다. Soft AP 모드로 인터넷 연결을 공유할 수 있습니다. Linux에서는 커널 6.2부터 mainline rtw88_8821cu 드라이버가 포함되어 있습니다. GX10(Ubuntu 24.04, 커널 6.17) 테스트에서 모니터 모드와 패킷 인젝션이 2.4 GHz와 5 GHz 모두 100%를 기록했고, WPA 핸드셰이크 end-to-end 캡처에 성공했으며, Bluetooth와 Wi-Fi를 동시에 사용할 수 있었습니다.

> ⚠️ **참고:** AWUS036EACS는 Windows 가정용으로 설계되었습니다. 다만 Linux에서도 mainline rtw88_8821cu 드라이버(커널 6.2 이상)로 동작합니다. RP-SMA 포트가 없어 안테나를 업그레이드할 수 없습니다.

## 제품 특징

- 802.11ac AC600 듀얼 밴드 WiFi + Bluetooth 4.2를 하나의 나노 USB 어댑터에 통합
- Windows에서 플러그 앤 플레이 - 내장 드라이버가 자동으로 설치됩니다
- Soft AP 모드 - 어댑터에서 직접 WiFi 핫스팟 생성
- 초소형 휴대형 - 어떤 USB 포트에서도 눈에 띄지 않습니다
- 듀얼 밴드: 2.4 GHz (150 Mbps) + 5 GHz (433 Mbps)
- 2 dBi 내장 안테나 - 외장 RP-SMA 커넥터 없음
- 최소한의 공간에서 WiFi + BT가 필요한 데스크톱, 임베디드 시스템 또는 가정용 PC에 적합
- Bluetooth 4.2로 오디오 스트리밍, 키보드, 마우스 및 기타 주변기기 지원

## 기술 사양

| 항목 | 값 |
|-----------|-------|
| 칩셋 | Realtek RTL8821CU |
| WiFi 표준 | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bluetooth | BT 4.2 (2.4 GHz) |
| 주파수 대역 | WiFi: 2.4 GHz · 5 GHz · BT: 2.4 GHz |
| 최대 데이터 전송률 | 802.11b: 11 Mbps · 802.11g: 54 Mbps · 802.11n: 150 Mbps · 802.11ac: 433 Mbps |
| 합산 최대 속도 | AC600 (150 + 433 Mbps) |
| 안테나 | 내장형, 2 dBi (분리 불가, RP-SMA 없음) |
| USB 인터페이스 | USB 2.0 |
| 출력 | 일반 17 dBm |
| 수신 감도 | 802.11b: −85 dBm · 802.11g: −69 dBm · 802.11n: −68 dBm · 802.11ac: −59 dBm |
| 무선 보안 | WEP / WPA-PSK / WPA2-PSK / 802.1X |
| 동작 온도 | −10°C ~ 60°C |
| 폼팩터 | 나노 / 저형(low-profile) |
| 원산지 | 대만 |

## OS 호환성

| OS | 상태 | 비고 |
|----|--------|-------|
| Windows XP–10 | ✅ 지원 | 내장 드라이버, 플러그 앤 플레이. Windows 11 호환성은 Alfa 드라이버 페이지를 확인하십시오. |
| macOS | ⚠️ 제한적 | 정확한 버전 범위는 확인 중입니다. Apple Silicon 미지원. |
| Ubuntu / Linux | ✅ 커널 6.2 이상 | mainline rtw88_8821cu 드라이버 사용, 설치 불필요(GX10, Ubuntu 24.04, 커널 6.17에서 테스트). |
| Kali Linux | ✅ 지원 | GX10(Ubuntu 24.04, 커널 6.17)에서 모니터 모드와 패킷 인젝션 확인됨: 두 대역 모두 100%, WPA 핸드셰이크 end-to-end 캡처 성공. 실제 Kali 설치 환경에서는 테스트하지 않았습니다. |
| NetHunter (Android) | ❌ 권장하지 않음 | RTL8821CU의 NetHunter 동작이 확인되지 않았습니다. |

## 하드웨어 지원

| 하드웨어 | 상태 | 비고 |
|----------|--------|-------|
| Raspberry Pi | ⚠️ 미테스트 | 자사에서 테스트하지 않았으며, 커널 6.2 이상에는 mainline rtw88_8821cu 드라이버가 포함되어 있습니다. |
| 데스크톱 / 노트북 PC | ✅ 지원 | Windows 전용으로 권장합니다. |
| 임베디드 / IoT (Windows) | ⚠️ Windows 전용 | 소형 설계로 임베디드 Windows 시스템에 적합합니다. |

## 고급 기능

| 기능 | 상태 |
|---------|--------|
| 모니터 모드 | ✅ 지원 (GX10 테스트: 두 대역 모두 100%) |
| 패킷 인젝션 | ✅ 지원 (GX10 테스트: 두 대역 모두 100%) |
| Soft AP 모드 | ✅ 지원 |
| Bluetooth | ✅ BT 4.2 (Wi-Fi와 동시 사용 가능) |
| VIF | 🟡 부분 지원(같은 채널의 passive monitor + managed, 독립적인 이중 VIF 미지원) |

## 패키지 구성

- AWUS036EACS 나노 어댑터 1개

## 리소스 및 링크

| 리소스 | 링크 |
|----------|------|
| 공식 제품 페이지 | https://www.alfa.com.tw/products/awus036eacs_1 |
| 공식 문서 | https://docs.alfa.com.tw/Product/AWUS036EACS/ |

## 데이터시트 다운로드

공식 데이터시트는 준비 중입니다.

{{< gallery >}}
  <img src="/images/products/alfa/awus036eacs_image_1.png" alt="ALFA AWUS036EACS" />
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
