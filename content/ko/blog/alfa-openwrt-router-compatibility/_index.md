---
title: "ALFA 무선 네트워크 카드의 OpenWrt 호환성"
date: 2026-09-03
draft: false
slug: "alfa-openwrt-router-compatibility"
tags:
  - "ALFA"
  - "OpenWrt"
  - "Router"
  - "kmod-mt76"
  - "AWUS036ACM"
  - "AWUS036ACH"
  - "Soft-AP"
categories:
  - "Hardware Guide"
description: "OpenWrt는 ALFA USB WiFi 카드에 대한 지원이 가장 우수한 플랫폼으로, MediaTek 모델은 공식 드라이버로 직접 지원되고 Realtek 모델은 커뮤니티 유지보수 드라이버로 지원됩니다. 권장 모델은 AWUS036ACM(MT7612U)입니다."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

## 1. 문제 요약

고객 문의: "ALFA 시리즈 USB 무선 네트워크 카드를 OpenWrt 라우터에서 사용할 수 있나요?"

간단한 결론: OpenWrt는 3대 서드파티 라우터 펌웨어(DD-WRT / OpenWrt / Tomato) 중 ALFA USB WiFi 네트워크 카드 지원이 가장 우수한 플랫폼입니다. MediaTek 칩 모델(AWUS036ACM / ACHM / AXML / AXM)은 공식 kmod-mt76 계열 패키지로 직접 지원되며, Realtek 칩 모델(AWUS036ACH / ACS / EACS / AX / AXER)은 커뮤니티가 유지보수하는 out-of-tree 드라이버 패키지가 필요하고 가용성은 OpenWrt 버전에 따라 달라집니다. 가장 권장하는 모델은 드라이버가 성숙하고 안정적이며 모니터링과 패킷 인젝션을 지원하는 AWUS036ACM(MT7612U)입니다.

평가 근거: ALFA의 현행 9개 USB 네트워크 카드(AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. 대상 소프트웨어 사양 및 요구사항 분석

### 2.1 OpenWrt란?

OpenWrt는 고도로 모듈화된 오픈소스 라우터 펌웨어로, Linux 커널과 opkg 패키지 관리 시스템을 사용합니다. DD-WRT / Tomato와 달리 OpenWrt의 드라이버는 개별적으로 설치할 수 있는 커널 모듈(kmod) 패키지로 제공되므로, 사용자는 펌웨어 전체를 다시 컴파일하지 않고도 필요에 따라 USB WiFi 드라이버를 설치할 수 있습니다.

### 2.2 OpenWrt의 USB WiFi 드라이버 프레임워크

OpenWrt 공식 패키지 저장소에는 다음과 같은 USB WiFi 드라이버가 포함되어 있습니다:

| 드라이버 패키지 | 출처 | 해당 칩 / 모델 | 유지보수 상태 |
|---|---|---|---|
| kmod-mt76-usb + kmod-mt76x2u | 공식 in-kernel | MediaTek MT7612U (AWUS036ACM) | 활발, 안정 |
| kmod-mt76-usb + kmod-mt76x0u | 공식 in-kernel | MediaTek MT7610U (AWUS036ACHM) | 활발 |
| kmod-mt7921u | 공식 in-kernel | MediaTek MT7921AUN (AWUS036AXML / AXM) | 23.05+ 버전에서 사용 가능 |
| kmod-rtl8812au-ct | 커뮤니티 out-of-tree | Realtek RTL8812AU / RTL8811AU (AWUS036ACH / ACS) | 커뮤니티 유지보수, 24.10에서 커널 크래시 보고 있음 |
| kmod-rtl8821cu | 커뮤니티 out-of-tree | Realtek RTL8821CU (AWUS036EACS) | 커뮤니티 유지보수 |
| kmod-rtw89 / kmod-rtl8852bu | 개발 중 | Realtek RTL8832BU (AWUS036AX / AXER) | rtw89 USB 지원이 점진적으로 통합되는 중이며, 최신 커널 필요 |

### 2.3 전제 조건: USB 코어 지원

WiFi 드라이버를 설치하기 전에 OpenWrt에서 USB 코어 지원이 활성화되어 있는지 확인해야 합니다:

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

최신 OpenWrt 버전은 대부분 kmod-usb-core를 기본 포함하지만, lsusb 명령을 제공하는 usbutils는 수동으로 설치해야 합니다.

## 3. 현행 ALFA 네트워크 카드 사양 및 칩셋 분석

2026년 9월 기준, ALFA Network의 현행 USB 무선 네트워크 카드 라인업은 다음과 같습니다(현행 모델: 9개):

| 모델 | Wi-Fi 등급 | 칩셋 | 인터페이스 | OpenWrt 드라이버 패키지 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | kmod-mt7921u (23.05+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | kmod-mt7921u (23.05+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | kmod-rtw89 (개발 중) / rtl8852bu 직접 컴파일 |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | 위와 동일 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | kmod-rtl8812au-ct (커뮤니티) |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | kmod-mt76x0u (공식) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | kmod-mt76x2u (공식)⭐ 권장 |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | kmod-rtl8812au-ct (포함) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8821CU | USB 2.0 | kmod-rtl8821cu (커뮤니티) |

## 4. 적용 가능 모델 및 칩셋

### 4.1 권장 등급 분류

| 권장 등급 | 모델 (칩셋) | 설명 |
|---|---|---|
| ⭐ 적극 권장 | AWUS036ACM (MT7612U) | 공식 드라이버가 성숙하고 안정적이며 AP / STA / Monitor / Injection을 지원하는, OpenWrt 최적의 선택 |
| ✅ 권장 | AWUS036ACHM (MT7610U) | 공식 드라이버, 듀얼밴드이나 433Mbps에 그쳐 저전력 시나리오에 적합 |
| ✅ 권장 (신규 버전) | AWUS036AXML / AXM (MT7921AUN) | Wi-Fi 6E, 공식 드라이버, OpenWrt 23.05+ 및 커널 5.15+ 필요 |
| ⚠️ 사용 가능하나 주의 필요 | AWUS036ACH (RTL8812AU) | 커뮤니티 드라이버, 24.10 버전에서 커널 크래시 보고 있음, 23.05 사용 권장 |
| ⚠️ 사용 가능하나 주의 필요 | AWUS036ACS (RTL8811AU) | 위와 동일, 8812au 드라이버로 커버됨 |
| ⚠️ 사용 가능하나 주의 필요 | AWUS036EACS (RTL8821CU) | 커뮤니티 드라이버, 안정성 보통 |
| ❌ 권장하지 않음 | AWUS036AX / AXER (RTL8832BU) | Wi-Fi 6, rtw89 USB 지원이 아직 개발 중이며, 대부분의 OpenWrt 버전에서 직접 사용 불가 |

### 4.2 라우터 하드웨어 요구사항

| 항목 | 최소 요구사항 | 권장 요구사항 |
|---|---|---|
| USB 포트 | USB 2.0 (AWUS036ACHM / ACS / EACS) | USB 3.0 (AWUS036ACH / ACM / AX 시리즈) |
| Flash | 16MB (드라이버 설치 + 의존성 패키지) | 32MB+ |
| RAM | 128MB | 256MB+ (AP 모드 + 다중 사용자) |
| OpenWrt 버전 | 21.02+ | 23.05.x (안정 버전) |

## 5. 환경 요구사항

### 5.1 소프트웨어 환경

- OpenWrt 안정 버전: 23.05.x (커널 5.15) 또는 24.10.x (커널 6.6)
- 패키지 소스: 공식 opkg 패키지 저장소 (https://downloads.openwrt.org/releases/{version}/packages/{arch}/)
- 네트워크 연결: 드라이버 설치 과정에서 라우터가 온라인 상태여야 함 (WAN 포트 경유)

### 5.2 하드웨어 환경

- USB 2.0 / 3.0 포트를 갖춘 OpenWrt 호환 라우터
- 고출력 모델(AWUS036ACH)은 라우터 USB 포트의 전원 부족을 피하기 위해 전원 공급형 USB 3.0 Hub 사용 권장
- AWUS036AXML은 USB-C 인터페이스이므로, 라우터에 USB-C 포트가 있는지 확인하거나 USB-C to USB-A 어댑터 사용

## 6. 호환성 판정

### ALFA 현행 모델 × OpenWrt 호환성 매트릭스

| 모델 | 칩셋 | 드라이버 방식 | USB 감지 | STA 인터넷 | AP 모드 | Monitor | 최소 버전 | 종합 평가 |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | kmod-mt76x2u | ✅ | ✅ | ✅ | ✅ | 21.02+ | ⭐ 최상 |
| AWUS036ACHM | MT7610U | kmod-mt76x0u | ✅ | ✅ | ✅ | ⚠️ 제한적 | 21.02+ | ✅ 양호 |
| AWUS036AXML | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ 제한적 | 23.05+ | ✅ 양호 |
| AWUS036AXM | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ 제한적 | 23.05+ | ✅ 양호 |
| AWUS036ACH | RTL8812AU | kmod-rtl8812au-ct | ✅ | ✅ | ✅ | ⚠️ 제한적 | 22.03+ (24.10에서 크래시 있음) | ⚠️ 사용 가능 |
| AWUS036ACS | RTL8811AU | kmod-rtl8812au-ct | ✅ | ✅ | ⚠️ | ❌ | 22.03+ | ⚠️ 사용 가능 |
| AWUS036EACS | RTL8821CU | kmod-rtl8821cu | ✅ | ⚠️ | ❌ | ❌ | 23.05+ | ⚠️ 사용 가능 |
| AWUS036AX | RTL8832BU | rtw89 (개발 중) | ⚠️ | ❌ | ❌ | ❌ | 커스텀 컴파일 필요 | ❌ 권장하지 않음 |
| AWUS036AXER | RTL8832BU | rtw89 (개발 중) | ⚠️ | ❌ | ❌ | ❌ | 커스텀 컴파일 필요 | ❌ 권장하지 않음 |

판정 기준: OpenWrt 공식 패키지 저장소(23.05 / 24.10)의 kmod 패키지 가용성 + OpenWrt 포럼의 사용자 보고. Realtek 칩 드라이버는 커뮤니티가 유지보수하며, 안정성과 기능 완성도가 MediaTek mt76 계열만큼 완전하지는 않습니다.

## 7. 단계별 상세 설정 절차

### 7.1 준비 단계: USB 코어 지원 활성화

**1단계: SSH로 OpenWrt 라우터 접속**

```bash
ssh root@192.168.1.1
```

**2단계: 패키지 저장소 업데이트 및 USB 코어 지원 설치**

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

**3단계: ALFA 네트워크 카드 삽입 및 USB 감지 확인**

```bash
lsusb
# 예상 출력 예시 (AWUS036ACM / MT7612U):
# Bus 002 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

### 7.2 경로 A: MediaTek 칩셋 모델 (AWUS036ACM / ACHM / AXML / AXM)

AWUS036ACM(MT7612U)을 예로 들면:

**1단계: 드라이버 패키지 설치**

```bash
# AWUS036ACM (MT7612U)
opkg install kmod-mt76-usb kmod-mt76x2u

# AWUS036ACHM (MT7610U) — 대신 사용
# opkg install kmod-mt76-usb kmod-mt76x0u

# AWUS036AXML / AXM (MT7921AUN) — 대신 사용 (23.05+ 필요)
# opkg install kmod-mt7921u
```

**2단계: 무선 관리 도구 설치**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**3단계: 네트워크 인터페이스 생성 확인**

```bash
iw dev
# wlan0 또는 wlan1 인터페이스가 보여야 함
```

**4단계: 주변 WiFi 스캔 (기능 검증)**

```bash
iw dev wlan0 scan | grep -E "SSID|signal"
```

**5단계: STA 클라이언트 모드로 설정 (기존 AP에 연결)**

/etc/config/wireless 편집:

```text
config wifi-device 'radio1'
       option type 'mac80211'
       option path 'platform/usb1/1-1/1-1:1.0'
       option channel 'auto'
       option htmode 'VHT80'

config wifi-iface 'wifinet2'
       option device 'radio1'
       option mode 'sta'
       option network 'wwan'
       option ssid 'Your WiFi Name'
       option encryption 'psk2'
       option key 'Your WiFi Password'
```

**6단계: 무선 서비스 재시작**

```bash
/etc/init.d/network restart
```

**7단계: AP 핫스팟 모드로 설정 (네트워크 공유)**

/etc/config/wireless를 편집하여 mode를 ap로 변경:

```text
config wifi-iface 'wifinet2'
   option device 'radio1'
   option mode 'ap'
   option network 'lan'
   option ssid 'ALFA-OpenWrt-AP'
   option encryption 'psk2'
   option key 'Your Hotspot Password'
```

**8단계: Monitor 모드 활성화 (침투 테스트용)**

```bash
opkg install aircrack-ng
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
iw dev wlan0 set channel 6
# 확인
iw dev wlan0 info
# type이 monitor로 표시되어야 함
```

### 7.3 경로 B: Realtek 칩셋 모델 (AWUS036ACH / ACS / EACS)

AWUS036ACH(RTL8812AU)를 예로 들면:

**1단계: 커뮤니티 드라이버 설치**

```bash
opkg update
opkg install kmod-rtl8812au-ct

# AWUS036EACS (RTL8821CU) — 대신 사용
# opkg install kmod-rtl8821cu
```

**2단계: 무선 관리 도구 설치**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**3단계: 인터페이스 확인**

```bash
iw dev
# 참고: rtl8812au-ct 드라이버의 인터페이스 이름은 wlan0 또는 wlan1일 수 있음
```

설정 방법은 7.2의 5-7단계(STA / AP 모드 설정)와 동일합니다.

**4단계: Monitor 모드**

```bash
# rtl8812au-ct 드라이버는 monitor 모드를 지원함
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
# 패킷 인젝션 기능은 제한적이므로, 침투 테스트에는 mt76 칩셋 사용을 권장
```

**5단계: 커널 크래시가 발생하는 경우 (24.10 버전의 알려진 문제)**

```bash
# 23.05 안정 버전으로 롤백하거나, 커스텀 컴파일 드라이버 사용
# 크래시 로그 확인
logread | grep -i "panic\|crash\|rtl8812"
```

### 7.4 경로 C: Wi-Fi 6 모델 (AWUS036AX / AXER, RTL8832BU)

⚠️ 이 경로는 OpenWrt를 커스텀 컴파일해야 하므로 일반 사용자에게 적합하지 않습니다.

**1단계: OpenWrt 버전에 rtw89 USB 지원이 포함되어 있는지 확인**

```bash
opkg list | grep rtw89
# 결과가 없으면 해당 버전에는 포함되어 있지 않음
```

**2단계: 필요 시 OpenWrt 이미지 파일을 직접 컴파일**

kmod-rtw89와 해당 펌웨어를 추가합니다.

**대안 제안**: OpenWrt 라우터에서 Wi-Fi 6 USB 네트워크 카드를 사용해야 한다면, 현재로서는 AWUS036AXML(MT7921AUN)을 대안으로 사용하는 것을 권장합니다.

## 8. 일반적인 오류 및 문제 해결

| 증상 | 가능한 원인 | 해결 방법 |
|---|---|---|
| lsusb에 ALFA 네트워크 카드가 표시되지 않음 | USB 코어 미설치 / 전원 부족 | kmod-usb-core, kmod-usb2, kmod-usb3가 설치되어 있는지 확인; 전원 공급형 USB Hub 사용 |
| lsusb에는 카드가 보이나 iw dev에 인터페이스 없음 | 드라이버 미설치 / 비호환 드라이버 | 해당 kmod 패키지 설치; dmesg에서 펌웨어 누락 오류 확인 |
| opkg install kmod-mt76x2u 실행 시 'kernel version mismatch' 보고 | OpenWrt 버전이 패키지 저장소 버전과 불일치 | opkg update 후 재시도; 펌웨어 버전이 패키지 저장소 아키텍처와 일치하는지 확인 |
| AP 모드 시작 실패 (hostapd 오류) | 드라이버가 AP 미지원 / 채널 설정 오류 | 칩이 AP 모드를 지원하는지 확인; 고정 채널(예: 6 또는 149) 설정 시도; Regulatory Domain 확인 |
| Monitor 모드에서 패킷 인젝션 불가 | 드라이버가 injection 미지원 / 채널 충돌 | MediaTek mt76 계열 지원이 가장 우수; Realtek 8812au-ct는 injection 기능이 제한적; airmon-ng check kill 확인 |
| AWUS036ACH 고출력 시 연결 끊김 | USB 전원 부족 | 전원 공급형 USB 3.0 Hub 사용; /etc/config/wireless에서 option txpower '20'으로 출력 낮춤 |
| 24.10에서 rtl8812au-ct 설치 후 커널 패닉 | 알려진 드라이버 호환성 문제 | 23.05.x 안정 버전으로 롤백; 또는 GitHub issue에서 수정 상황 추적 |
| MT7921 (AXML/AXM)에서 6GHz 사용 불가 | Regulatory Domain 제한 / 커널 버전 | 커널 5.19+ 및 올바른 Wi-Fi 6E regulatory domain 설정 필요; OpenWrt 23.05의 6GHz 지원은 아직 테스트 단계 |

## 9. 알려진 제한 사항

- Realtek 칩 드라이버는 커뮤니티가 유지보수: `kmod-rtl8812au-ct`, `kmod-rtl8821cu`는 OpenWrt가 공식적으로 유지보수하지 않으며, 안정성과 업데이트 일정을 보장할 수 없습니다.
- 24.10 버전 `rtl8812au-ct`의 커널 크래시 보고: Realtek 칩 사용자는 23.05.x 버전을 유지할 것을 권장합니다.
- Wi-Fi 6(RTL8832BU) 지원 부족: `rtw89` USB 드라이버가 아직 개발 중이어서, 대부분의 OpenWrt 버전에서 AWUS036AX / AXER를 직접 사용할 수 없습니다.
- 제한적인 AP 모드 성능: USB WiFi를 AP로 사용할 때 처리량이 라우터 내장 WiFi보다 낮습니다(USB 버스 대역폭 + 드라이버 오버헤드로 인함).
- Monitor/Inject 기능 차이: MediaTek mt76 계열 지원이 가장 완전하며, Realtek 칩의 injection 기능은 제한적이어서 전문적인 침투 테스트에는 적합하지 않습니다.
- 라우터 하드웨어 자원: 저사양 라우터(16MB Flash / 128MB RAM)에서는 드라이버 설치 시 공간 부족으로 다른 기능에 영향을 줄 수 있습니다.
- USB 3.0 간섭: USB 3.0 장치는 2.4GHz WiFi를 간섭할 수 있으므로, USB 2.0 포트나 차폐가 잘 된 USB Hub 사용을 권장합니다.
- 다중 네트워크 카드 동시 사용: 라우터 내장 WiFi + USB WiFi를 동시에 사용할 때 채널 충돌이나 자원 경합이 발생할 수 있습니다.
- ⚠️ **RTL8832BU(AWUS036AX/AXER)의 드라이버 유지보수자가 사용 회피를 공개적으로 권고함**: 4.1절에서 "❌ 권장하지 않음"으로 표시한 것은 단지 `rtw89` USB가 아직 개발 중이기 때문만이 아니라, 드라이버 유지보수자 morrownr가 이 칩 계열에 대해 "매우 나쁜 드라이버이며, 칩 자체에도 의문이 있다"고 공개적으로 밝히며 Linux 사용자에게 당분간 사용을 피할 것을 권고했기 때문입니다(출처는 10장 참조).
- **커널 버전 임계값 용어에 대한 명확화 필요**: 4.1절의 "MT7921AUN은 OpenWrt 23.05+ 및 커널 5.15+ 필요"라는 표현은 오해를 유발하기 쉽습니다——`mt7921u` 드라이버 자체는 데스크톱 Linux에서 실제로 **커널 5.19+**를 필요로 하지만(드라이버 유지보수자의 원문 참조), OpenWrt 공식 패키지는 backport 메커니즘을 통해 이를 조기에 포함하는 경우가 많아, OpenWrt 23.05(기본 커널이 5.15로 표기되어 있음에도)에서 `kmod-mt7921u` 설치에 성공했다는 사용자 보고가 존재합니다. **커널 버전을 추론하지 말고, 고객 버전의 실제 `opkg list` 조회 결과를 근거로 판단하시기 바랍니다**.

반박 조건: OpenWrt의 후속 패키지 업데이트가 24.10 `rtl8812au-ct`의 커널 크래시 문제를 수정한다면, 4.1절과 6장의 AWUS036ACH 권장 사항을 "23.05 유지"에서 상향 조정할 수 있습니다. `rtw89` USB에 대한 공식 지원이 OpenWrt 공식 패키지 저장소에 정식 포함된다면, AWUS036AX / AXER의 "권장하지 않음" 판정을 재검토해야 합니다. 공식에서 MT7921의 6GHz에 대한 완전한 지원 성명을 발표한다면, AXML / AXM의 제한 사항을 갱신해야 합니다.

## 10. 참고 URL

| 출처 | 설명 | URL | 검증 상태 | 검증 일자 |
|---|---|---|---|---|
| OpenWrt 공식 문서 | OpenWrt 공식 문서 진입점 (무선 설정 / 패키지 관리) | https://openwrt.org/docs/start | ✅ 검증됨 | 2026-09-03 |
| OpenWrt 공식 포럼 | USB WiFi 드라이버 논의 진입점 | https://forum.openwrt.org/ | ✅ 검증됨 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 드라이버 업스트림 | https://github.com/morrownr/8812au-20210820 | ✅ 검증됨 | 2026-09-03 |
| ALFA Network 제품 개요 (Yopitek) | ALFA 현행 제품 사양 | https://yupitek.com/ko/products/alfa/ | ✅ 검증됨 | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | 드라이버 유지보수자 공식 성명: rtl8852/32au(RTL8832BU) 칩 회피 권고 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 검증됨 | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko는 커널 5.19+에서만 커널에 나타남 (드라이버 유지보수자 원문) | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ 검증됨 | 2026-09-03 |
| OpenWrt 공식 포럼 — Best USB WiFi Dongle for Raspberry Pi 4B | OpenWrt 23.05.0에서 kmod-mt7921u 설치 성공 사용자 보고 | https://forum.openwrt.org/t/best-usb-wifi-dongle-for-raspberry-pi-4b/160103 | ✅ 검증됨 | 2026-09-03 |

관련 글: [ALFA 무선 네트워크 카드는 DD-WRT를 지원하나요](https://yupitek.com/ko/blog/alfa-ddwrt-router-compatibility/) | [ALFA 무선 네트워크 카드는 Tomato를 지원하나요](https://yupitek.com/ko/blog/alfa-tomato-router-compatibility/) | [ALFA 무선 네트워크 카드는 NVIDIA DGX Spark를 지원하나요](https://yupitek.com/ko/blog/alfa-nvidia-dgx-spark-compatibility/) | [ALFA 무선 네트워크 카드는 NVIDIA Jetson Nano를 지원하나요](https://yupitek.com/ko/blog/alfa-nvidia-jetson-nano-compatibility/)

면책 조항: 본 글의 호환성 판정은 OpenWrt 23.05.x / 24.10.x 공식 패키지 저장소를 기준으로 합니다. 패키지 가용성은 라우터 아키텍처(ath79 / ramips / mvebu / x86 등)에 따라 달라질 수 있습니다. Realtek 칩 드라이버는 커뮤니티가 유지보수하며, 실제 안정성은 버전 변경에 따라 달라질 수 있습니다. OpenWrt USB WiFi에는 MediaTek 칩 모델(AWUS036ACM을 최우선)을 우선적으로 선택할 것을 권장합니다.
