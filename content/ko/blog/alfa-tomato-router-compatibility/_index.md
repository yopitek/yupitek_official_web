---
title: "ALFA 무선 네트워크 카드는 Tomato를 지원하나요?"
date: 2026-09-03
draft: false
slug: "alfa-tomato-router-compatibility"
tags:
  - "ALFA"
  - "Tomato"
  - "FreshTomato"
  - "Router"
  - "Broadcom"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "Hardware Guide"
description: "ALFA 라우터 모델은 Tomato 펌웨어에서 USB WiFi를 지원하지 않으므로 권장하지 않습니다. USB WiFi 호환성을 위해서는 OpenWrt를 사용하세요."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

## 1. 문제 요약

고객 문의: "ALFA 시리즈 USB 무선 네트워크 카드를 Tomato 펌웨어로 플래싱한 라우터에서 사용할 수 있나요?"

간단한 결론: 현재 ALFA 시리즈의 모든 현행 모델은 Tomato 펌웨어(FreshTomato, AdvancedTomato 등 파생 버전 포함)에서 지원되지 않으므로 사용을 권장하지 않습니다. Tomato는 3대 주요 서드파티 라우터 펌웨어 중 USB WiFi 지원이 가장 취약한 플랫폼으로, 개발 초점이 전적으로 Broadcom 칩셋의 내장 WiFi에 맞춰져 있습니다. USB WiFi 네트워크 카드를 라우터에서 사용해야 한다면 Tomato 대신 OpenWrt를 사용하는 것이 맞습니다.

평가 대상: ALFA 현행 9개 USB 네트워크 카드 모델(AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. 대상 소프트웨어 사양 및 요구사항 분석

### 2.1 Tomato란?

Tomato는 오랜 역사를 지닌 오픈소스 라우터 서드파티 펌웨어로, 원래 Jonathan Zarate가 개발했으며 여러 분기 버전이 파생되었습니다:

| 파생 버전 | 유지보수 상태 | 지원 플랫폼 |
|---|---|---|
| Original Tomato | 유지보수 중단 (2010년대 초) | Broadcom MIPS 라우터 |
| Tomato by Shibby | 유지보수 중단 | Broadcom MIPS / ARM |
| AdvancedTomato | 유지보수 중단 | Broadcom (Shibby 분기의 GUI 개조) |
| FreshTomato | 활발히 유지보수 중 | Broadcom MIPS / ARM (BCM47xx / BCM53xx) |
| Toastman Tomato | 유지보수 중단 | Broadcom MIPS |

### 2.2 Tomato의 USB WiFi 지원 프레임워크

Tomato의 핵심 설계 철학은 "Broadcom 라우터를 위한 미니멀하고 안정적인 서드파티 펌웨어를 제공한다"는 것으로, USB 기능은 주로 다음을 지원합니다:

| USB 기능 유형 | 지원 상태 |
|---|---|
| USB 저장 장치 (USB 메모리 / 하드디스크) | ✅ 완전 지원 (Samba / FTP / DLNA) |
| USB 프린터 | ✅ 지원 (p910nd / CUPS) |
| USB 3G/4G 데이터 모뎀 | ⚠️ 부분 지원 |
| USB WiFi 네트워크 카드 | ❌ 거의 미지원 |

Tomato의 커널에는 기본적으로 Broadcom 라우터 내장 WiFi용 폐쇄 소스 드라이버(wl 모듈)만 포함되어 있으며, USB WiFi 드라이버는 없습니다. 패키지 관리 시스템(ipkg / Optware) 역시 USB WiFi 드라이버 패키지를 제공하지 않습니다.

### 2.3 주요 제한 사항

- Tomato는 Broadcom 칩 라우터만 지원하며, Broadcom 라우터의 USB 포트는 보통 저장 장치 / 프린터 용도로만 사용됩니다
- FreshTomato는 여전히 유지보수되고 있으나, 개발 초점은 Broadcom 플랫폼의 버그 수정에 있으며 새로운 USB WiFi 드라이버는 추가되지 않습니다
- Tomato는 파일 시스템 공간이 매우 작아(보통 4-16MB), 드라이버를 수동으로 컴파일하더라도 설치할 공간이 없습니다
- Tomato에는 opkg 같은 최신 패키지 관리 시스템이 없어, OpenWrt처럼 kmod 드라이버를 손쉽게 설치할 수 없습니다

## 3. 현행 ALFA 네트워크 카드 사양 및 칩셋 분석

2026년 9월 기준, ALFA Network의 현행 USB 무선 네트워크 카드 라인업은 다음과 같습니다(상위 모델 기준 9개):

| 모델 | Wi-Fi 등급 | 칩셋 | 인터페이스 | Tomato 드라이버 상태 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ 없음 |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ 없음 |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ 없음 |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ 없음 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ❌ 없음 |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | ❌ 없음 |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ❌ 없음 |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | ❌ 없음 |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8821CU | USB 2.0 | ❌ 없음 |

## 4. 적용 가능 모델 및 칩셋

### 4.1 Tomato에서 사용 가능할 수 있는 초구형 ALFA 모델 (단종)

| 모델 | 칩셋 | Linux 드라이버 모듈 | 설명 |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | 이론상 로드 가능하나 Tomato에 기본 포함되지 않음. 커널 모듈을 수동으로 컴파일해야 하며 실제 실현 가능성은 극히 낮음 |
| AWUS036H | Realtek RTL8187L | rtl8187 | 위와 동일. 2.4GHz / 54Mbps만 지원하며 10여 년 전 단종됨 |

⚠️ 위에 언급한 구형 모델이라도, 사용자는 Tomato에서 해당 커널 버전에 맞는 드라이버 모듈을 직접 크로스 컴파일해야 하며, Tomato의 파일 시스템 공간은 대개 설치하기에 부족합니다. 이는 "지원"에 해당하지 않으며 "극도로 고난도의 해킹"에 가깝습니다.

### 4.2 Tomato에서 완전히 사용 불가능한 현행 모델

현행 ALFA 모델 전체(3번 표 참조)는 다음과 같은 이유로 Tomato에서 사용할 수 없습니다:

- Realtek 칩 (RTL8812AU / RTL8811AU / RTL8821CU / RTL8832BU): Tomato에 해당 드라이버가 없으며, 패키지 관리 시스템을 통해서도 설치할 수 없음
- MediaTek 칩 (MT7612U / MT7610U / MT7921AUN): Tomato가 mt76 / mt7921 드라이버를 포함하지 않으며, FreshTomato 개발팀도 추가 계획이 없음
- lsusb에서 장치가 보이더라도(Tomato에 USB 코어가 활성화된 경우), 이는 USB 버스 수준에서만 인식되는 것일 뿐 네트워크 인터페이스를 생성할 수 없음

## 5. 환경 요구사항

현행 ALFA 모델은 Tomato에서 사용할 수 없으므로, 이 섹션에서는 고객이 그래도 시도하고자 할 경우 요구되는 극단적인 조건을 정리합니다:

| 항목 | 요구사항 |
|---|---|
| 라우터 하드웨어 | USB 2.0 포트가 있는 Broadcom 칩 라우터, Flash ≥ 32MB, RAM ≥ 256MB |
| Tomato 버전 | FreshTomato 최신 버전 (구형 버전은 USB 지원이 더 열악함) |
| 크로스 컴파일 환경 | Tomato용 Broadcom 아키텍처(MIPS / ARM)에 맞는 크로스 컴파일 툴체인 구축 필요 |
| 드라이버 소스 코드 | 해당 칩의 Linux 드라이버 소스 코드를 입수하고 Tomato 커널 버전에 맞게 수정해야 함 |
| 기술 역량 | Linux 커널 모듈 개발, 크로스 컴파일, 디버깅 능력 필요 |
| 시간 비용 | 수 시간에서 수일이 소요되며 성공률은 낮음 |

결론: 99.9%의 사용자에게 ALFA USB WiFi 어댑터를 Tomato에서 사용하는 것은 실현 가능하지 않습니다.

## 6. 호환성 판정

### ALFA 현행 모델 × Tomato 호환성 매트릭스

| 모델 | 칩셋 | USB 코어 지원 | USB 감지 | STA 인터넷 접속 | AP 모드 | Monitor | 종합 판정 |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ⚠️ USB 코어 활성화 필요 | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036AXM | MT7921AUN | ⚠️ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036AX | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036AXER | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036ACH | RTL8812AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036ACHM | MT7610U | ⚠️ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036ACM | MT7612U | ⚠️ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036ACS | RTL8811AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036EACS | RTL8821CU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 미지원 |

판정 기준: Tomato(FreshTomato 포함)의 공식 커널과 패키지 저장소에는 최신 USB WiFi 칩셋용 드라이버가 전혀 포함되어 있지 않습니다. Tomato의 설계 목표에는 애초에 USB WiFi 확장 기능이 포함된 적이 없습니다.

## 7. 단계별 상세 설정 절차

현행 ALFA 모델은 Tomato에서 사용할 수 없으므로, 이 섹션에서는 검증 절차와 대안을 제시합니다.

### 7.1 Tomato 라우터가 USB WiFi를 지원하는지 확인 (문제 해결 절차)

**1단계: Tomato 관리 인터페이스 로그인**

브라우저에 192.168.1.1(또는 라우터 IP)를 입력합니다.

**2단계: USB 코어 활성화 여부 확인**

- USB and NAS > USB Support로 이동
- Core USB Support, USB 2.0 Support, USB 3.0 Support(가능한 경우)가 체크되어 있는지 확인
- USB Wireless Device Support(가능한 경우) 확인 — 대부분의 Tomato 버전에는 이 옵션이 없음

**3단계: ALFA 네트워크 카드를 라우터의 USB 포트에 삽입**

**4단계: SSH / Telnet으로 라우터에서 USB 감지 확인**

```bash
# lsusb 사용 가능 여부 확인 (Tomato에는 기본적으로 없을 수 있음)
which lsusb
# lsusb를 사용할 수 없으면 /proc/bus/usb 또는 dmesg 확인
cat /proc/bus/usb/devices
# 또는
dmesg | grep -i usb
```

**5단계: 네트워크 인터페이스 확인**

```bash
ifconfig -a
# vlan0 / br0 / eth0 / eth1(라우터 내장 인터페이스)만 있고 wlan0 / wlan1이 없으면 USB WiFi가 구동되지 않은 것임
```

**6단계: 사용 가능한 커널 모듈 확인**

```bash
lsmod
# wl(Broadcom 내장 WiFi 드라이버), et(이더넷 드라이버) 등만 있을 것으로 예상
# mt76 / rtl8812 / cfg80211 / mac80211 등 USB WiFi 드라이버는 없어야 함
```

**7단계: 추가 패키지 설치 가능 여부 확인**

```bash
# Tomato는 ipkg를 사용하지만 패키지 저장소가 매우 제한적임
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# 예상 결과는 비어 있음
```

### 7.2 권장 대안

#### 대안 1: OpenWrt로 전환 (강력 권장)

라우터 모델이 OpenWrt에서도 지원된다면, 펌웨어를 Tomato에서 OpenWrt로 플래싱하는 것을 권장합니다. OpenWrt는 완전한 USB WiFi 드라이버 패키지 저장소를 보유하여 대부분의 ALFA 모델을 지원합니다.

- 라우터가 OpenWrt Supported Devices 목록에 있는지 확인
- 지원된다면 [ALFA 무선 네트워크 카드는 OpenWrt를 지원하나요](https://yupitek.com/ko/blog/alfa-openwrt-router-compatibility/)의 설치 절차를 참조하세요

#### 대안 2: 라우터 내장 WiFi 사용

Tomato는 Broadcom 라우터의 내장 WiFi를 훌륭하게 지원합니다. 일반적인 인터넷 접속이나 AP 핫스팟이 목적이라면, 외장 ALFA 네트워크 카드 없이 라우터 내장 WiFi를 그대로 사용할 수 있습니다.

#### 대안 3: 하드웨어 교체

고출력, Monitor Mode, 패킷 인젝션 등 USB WiFi 고유 기능이 필요하다면 Tomato 플랫폼으로는 요구를 충족할 수 없습니다. 다음을 권장합니다:

- OpenWrt 지원 라우터 + ALFA 네트워크 카드 사용
- 또는 x86 미니 PC에 OpenWrt / pfSense 설치 + ALFA 네트워크 카드 사용
- 또는 Kali Linux / Ubuntu 컴퓨터에서 ALFA 네트워크 카드를 직접 사용

## 8. 일반적인 오류 및 문제 해결

| 증상 | 가능한 원인 | 해결 방법 |
|---|---|---|
| Tomato 관리 인터페이스에 "USB Wireless Device Support" 옵션이 없음 | 해당 Tomato 버전에 USB WiFi 지원이 컴파일되지 않음 | 정상이며 버그가 아님. 대부분의 Tomato 버전에는 이 기능이 없음 |
| ALFA 네트워크 카드 삽입 후 dmesg에 USB 감지는 보이나 네트워크 인터페이스가 없음 | 드라이버 부재 | 해결 불가. Tomato에 해당 드라이버가 없음 |
| ipkg 패키지를 수동 설치하려 하나 WiFi 드라이버를 찾을 수 없음 | Tomato 패키지 저장소에 USB WiFi 드라이버가 없음 | 정상이며 OpenWrt로 전환을 권장 |
| 구형 ALFA (RT3070)가 Tomato에서 감지되나 연결되지 않음 | 드라이버 불완전 / 펌웨어 누락 | 구형 칩이라도 사용 가능성을 보장할 수 없으며 OpenWrt 사용을 권장 |
| Tomato 플래싱 후 라우터 USB 포트가 USB 메모리만 읽음 | Tomato의 USB 기능은 저장 장치 / 프린터 전용으로 설계됨 | 예상된 동작임. Tomato는 USB WiFi를 지원하지 않음 |

## 9. 알려진 제한 사항

- **USB WiFi 드라이버의 완전한 부재**: Tomato(FreshTomato 포함)의 공식 커널에는 최신 USB WiFi 칩용 드라이버가 전혀 포함되어 있지 않으며, 이것이 가장 근본적인 제한입니다.
- **Broadcom 폐쇄 소스 드라이버 결속**: Tomato는 Broadcom의 폐쇄 소스 `wl` 드라이버에 의존하며, 오픈소스 `mac80211`/`cfg80211` 아키텍처 기반 USB WiFi 드라이버와 공존할 수 없습니다.
- **패키지 관리 생태계 부족**: Tomato의 ipkg 패키지 저장소에는 패키지가 매우 적어, 수천 개의 설치 가능한 패키지를 갖춘 OpenWrt와 다릅니다.
- **Flash/RAM 공간 부족**: 대부분의 Tomato 라우터는 Flash가 4-16MB에 불과하여, 드라이버를 컴파일하더라도 설치할 공간이 없습니다.
- **다른 개발 방향**: FreshTomato 개발팀의 우선순위는 Broadcom 플랫폼의 안정성 수정이며, USB WiFi 지원 추가에 자원을 투입하지 않습니다.
- **Monitor/Injection 미지원**: Tomato의 WiFi 아키텍처(Broadcom `wl` 드라이버) 자체가 침투 테스트 기능을 지원하지 않으며, 외장 USB WiFi를 연결해도 이는 변하지 않습니다.
- **AP 모드 확장 불가**: 구형 칩이 드라이버를 로드할 수 있더라도, Tomato의 네트워크 설정 인터페이스는 USB WiFi를 AP 모드로 설정하는 것을 지원하지 않습니다.

**반박 조건**: 향후 FreshTomato 버전이 공식 릴리스 노트에 USB WiFi 드라이버 지원을 명시적으로 추가하거나, 커뮤니티에서 널리 검증된 FreshTomato mt76/rtl8812au 모듈 이식 프로젝트가 등장한다면, 본 문서 6장의 "미지원" 판정은 재평가가 필요합니다. 또한 FreshTomato가 오픈소스 `mac80211` 아키텍처 커널로 전환한다면 제한 사항 설명도 갱신이 필요합니다.

## 10. 참고 URL

| 출처 | 설명 | URL | 검증 상태 | 검증 일자 |
|---|---|---|---|---|
| FreshTomato 공식 웹사이트 | FreshTomato 최신 버전 및 지원 장치 목록 | https://freshtomato.org/ | ✅ 검증됨 | 2026-09-03 |
| OpenWrt 공식 문서 | USB WiFi 드라이버 및 무선 설정 (비교 참고) | https://openwrt.org/docs/start | ✅ 검증됨 | 2026-09-03 |
| OpenWrt 공식 포럼 | USB WiFi 드라이버 관련 논의 (비교 참고) | https://forum.openwrt.org/ | ✅ 검증됨 | 2026-09-03 |
| ALFA Network 제품 개요 (Yopitek) | ALFA 현행 제품 사양 | https://yupitek.com/ko/products/alfa/ | ✅ 검증됨 | 2026-09-03 |

관련 글: [ALFA 무선 네트워크 카드는 DD-WRT를 지원하나요](https://yupitek.com/ko/blog/alfa-ddwrt-router-compatibility/) | [ALFA 무선 네트워크 카드는 OpenWrt를 지원하나요](https://yupitek.com/ko/blog/alfa-openwrt-router-compatibility/) | [ALFA 무선 네트워크 카드는 NVIDIA DGX Spark를 지원하나요](https://yupitek.com/ko/blog/alfa-nvidia-dgx-spark-compatibility/) | [ALFA 무선 네트워크 카드는 NVIDIA Jetson Nano를 지원하나요](https://yupitek.com/ko/blog/alfa-nvidia-jetson-nano-compatibility/)

면책 조항: 본 글의 호환성 판정은 Tomato / FreshTomato 공식 커널과 패키지 저장소를 기준으로 합니다. 극소수의 고급 사용자는 특정 구형 칩에서 직접 크로스 컴파일을 통해 기본 기능을 구현할 수도 있으나, 이는 공식 지원 범위에 속하지 않으며 일반 사용자에게는 권장하지 않습니다. 라우터에서 USB WiFi를 사용해야 하는 경우, OpenWrt가 실질적으로 선택 가능한 유일한 서드파티 펌웨어입니다.
