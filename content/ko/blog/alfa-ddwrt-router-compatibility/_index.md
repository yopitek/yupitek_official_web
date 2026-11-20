---
title: "ALFA 무선 네트워크 카드는 DD-WRT를 지원하나요?"
date: 2026-09-03
draft: false
slug: "alfa-ddwrt-router-compatibility"
tags:
  - "ALFA"
  - "DD-WRT"
  - "Router"
  - "Broadcom"
  - "Atheros"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "Hardware Guide"
description: "ALFA USB WiFi 카드(9개 모델)는 DD-WRT에서 공식적으로 지원되지 않습니다. 라우터 호환성을 위해서는 OpenWrt를 권장합니다."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

## 1. 문제 요약

고객 문의: "ALFA 시리즈 USB 무선 네트워크 카드를 DD-WRT 펌웨어로 플래싱한 라우터에서 사용할 수 있나요?"

간단한 결론: 현재 ALFA 시리즈의 모든 현행 모델(AWUS036ACH / ACM / ACHM / ACS / EACS / AX / AXER / AXML / AXM, 총 9개 모델)은 DD-WRT에서 공식 드라이버 지원이 없으므로 사용을 권장하지 않습니다. (평가 근거: ALFA 현행 9개 USB 네트워크 카드 모델) DD-WRT의 USB WiFi 지원은 일부 구형 Atheros / Ralink 칩셋에 한정되며, 특정 컴파일 버전이 필요합니다. USB WiFi 네트워크 카드를 라우터에서 사용해야 한다면 OpenWrt로 전환하는 것을 권장합니다([ALFA 무선 네트워크 카드의 OpenWrt 호환성](https://yupitek.com/ko/blog/alfa-openwrt-router-compatibility/) 참조).

## 2. 대상 소프트웨어 사양 및 요구사항 분석

### 2.1 DD-WRT란?

DD-WRT는 오픈소스 라우터 서드파티 펌웨어로, 주로 WiFi 칩이 내장된 라우터(Broadcom / Atheros / Ralink SoC)를 위해 설계되었습니다. 핵심 아키텍처는 Linux 커널 기반이지만, 기본 드라이버에는 대상 라우터의 SoC에 해당하는 무선 드라이버가 사전 설치되어 있습니다.

### 2.2 DD-WRT의 USB WiFi 지원 프레임워크

DD-WRT는 ipkg 패키지 관리 시스템을 통해 추가 드라이버를 설치하지만, 공식 패키지 저장소에 포함된 USB WiFi 드라이버는 매우 적습니다:

| 드라이버 | DD-WRT 상태 | 해당 칩 (ALFA 모델) |
|---|---|---|
| ath9k_htc | 일부 내장 | Atheros AR9271 (예: TP-Link TL-WN722N v1) |
| rt2800usb | 일부 내장 | Ralink RT3070 / RT3370 / RT5370 (구형 ALFA AWUS036NH) |
| rtl8812au | 공식 패키지 없음 | Realtek RTL8812AU (AWUS036ACH) |
| mt76 / mt76x2u | 공식 패키지 없음 | MediaTek MT7612U / MT7610U (AWUS036ACM / ACHM) |
| mt7921u | 공식 패키지 없음 | MediaTek MT7921AUN (AWUS036AXML / AXM) |
| rtl8852bu / rtw89 | 공식 패키지 없음 | Realtek RTL8832BU (AWUS036AX / AXER) |

### 2.3 주요 제한 사항

- DD-WRT의 핵심 지원은 라우터 내장 WiFi를 우선하며, USB WiFi는 부차적인 기능입니다
- 라우터 모델마다 DD-WRT 컴파일 버전이 달라 드라이버 가용성에 큰 차이가 발생합니다
- 커뮤니티가 드라이버를 이식하여 추가하더라도 Flash / RAM 부족으로 설치하지 못하는 경우가 많습니다
- DD-WRT는 USB WiFi의 Monitor Mode 및 Packet Injection 지원이 제한적입니다

## 3. 현행 ALFA 네트워크 카드 사양 및 칩셋 분석

2026년 9월 기준, ALFA Network의 현행 USB 무선 네트워크 카드 라인업은 다음과 같습니다:

| 모델 | Wi-Fi 등급 | 칩셋 | 인터페이스 | Linux 드라이버 상태 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | Linux in-kernel (mt7921u, 커널 5.12+ 필요) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | Linux in-kernel (mt7921u, 커널 5.12+ 필요) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree (rtl8852bu / rtw89) |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree (rtl8852bu / rtw89) |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | Out-of-tree (8812au, morrownr 유지보수) |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | Linux in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | Linux in-kernel (mt76x2u) |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | Out-of-tree (8812au 포함) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8821CU | USB 2.0 | Out-of-tree (8821cu, morrownr 유지보수) |

## 4. 적용 가능 모델 및 칩셋

### 4.1 DD-WRT에서 사용 가능할 수 있는 ALFA 모델 (단종 / 구형 모델)

| 모델 | 칩셋 | 드라이버 | DD-WRT 상태 |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | 일부 DD-WRT 버전에 부분 내장, 2.4GHz / 150Mbps만 지원 |
| AWUS036H | Realtek RTL8187L | rtl8187 | 매우 구형, 일부 버전에서 부분 지원, 2.4GHz / 54Mbps만 지원 |
| AWUS050NH | Atheros AR9170 | carl9170 / ar9170usb | 매우 구형, 듀얼밴드이나 단종된 지 오래됨 |

### 4.2 DD-WRT에서 사용 불가능한 모델

현행 ALFA 모델 전체(3번 표 참조)는 다음과 같은 이유로 DD-WRT에서 공식 지원되지 않습니다:

- Realtek 칩셋 (RTL8812AU / RTL8811AU / RTL8821CU / RTL8832BU): DD-WRT에 해당 out-of-tree 드라이버 패키지가 없음
- MediaTek 칩셋 (MT7612U / MT7610U / MT7921AUN): DD-WRT가 mt76 / mt7921 드라이버를 통합하지 않음
- 라우터에 USB 포트가 있고 하드웨어 계층에서 장치를 인식하더라도(lsusb로 VID/PID 확인 가능), 드라이버가 없으면 네트워크 인터페이스를 생성할 수 없음

## 5. 환경 요구사항

고객이 그래도 DD-WRT에서 ALFA 네트워크 카드 사용을 시도하고자 한다면, 다음 조건을 충족해야 합니다:

| 항목 | 요구사항 |
|---|---|
| 라우터 하드웨어 | USB 2.0 / 3.0 포트가 있어야 하며, DD-WRT에서 USB 코어 지원을 활성화해야 함 (Services > USB) |
| DD-WRT 버전 | 해당 라우터용으로 지원되는 최신 BrainSlayer / Kong 버전이어야 함. 구형 버전은 드라이버가 더 적음 |
| Flash 공간 | 최소 16MB Flash (대부분의 엔트리급 라우터는 4-8MB에 불과하여 추가 드라이버를 설치하기에 부족함) |
| RAM | 최소 128MB RAM (USB WiFi 드라이버와 hostapd가 메모리를 소비함) |
| 전원 공급 | USB 포트가 충분한 전류를 공급해야 함 (AWUS036ACH의 고출력은 800mA+에 달할 수 있으므로, 전원 공급형 USB Hub 사용 권장) |

## 6. 호환성 판정

### ALFA 현행 모델 × DD-WRT 호환성 매트릭스

| 모델 | 칩셋 | USB 버스 감지 | 드라이버 로딩 | STA 인터넷 접속 | AP 모드 | Monitor | 종합 판정 |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ✅ (lsusb) | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036AXM | MT7921AUN | ✅ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036AX | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036AXER | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036ACH | RTL8812AU | ✅ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036ACHM | MT7610U | ✅ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036ACM | MT7612U | ✅ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036ACS | RTL8811AU | ✅ | ❌ | ❌ | ❌ | ❌ | 미지원 |
| AWUS036EACS | RTL8821CU | ✅ | ❌ | ❌ | ❌ | ❌ | 미지원 |

판정 기준: DD-WRT 공식 패키지 저장소와 커널 기본 컴파일에는 위 칩셋용 USB WiFi 드라이버가 포함되어 있지 않습니다. lsusb로 장치가 보이는 것은 USB 버스 수준의 인식을 의미할 뿐, 네트워크 기능을 사용할 수 있다는 뜻은 아닙니다.

## 7. 단계별 상세 설정 절차

현행 ALFA 모델은 DD-WRT에서 지원되지 않으므로, 이 섹션에서는 두 가지 대안 경로를 제시합니다:

### 경로 A: DD-WRT 라우터가 실제로 미지원인지 확인 (문제 해결 절차)

**1단계: DD-WRT 관리 인터페이스 로그인**

브라우저에 `192.168.1.1`(또는 라우터 IP)를 입력합니다.

**2단계: USB 지원 활성화**

- Services > USB로 이동
- Core USB Support, USB 2.0 Support, USB 3.0 Support(가능한 경우) 체크
- USB Wireless Device Support(가능한 경우) 체크
- Save > Apply Settings 클릭

**3단계: ALFA 네트워크 카드를 라우터의 USB 포트에 삽입**

**4단계: SSH로 라우터에 로그인하여 확인**

```bash
# USB 장치가 감지되었는지 확인
lsusb
# 예상 출력에는 ALFA 네트워크 카드의 VID/PID가 포함되어야 함, 예:
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter

# 네트워크 인터페이스가 생성되었는지 확인
ip link show
# wlan0 / wlan1 같은 새 인터페이스가 없으면 드라이버가 로드되지 않은 것임

# 커널 로그 확인
dmesg | tail -30
# "no driver"가 표시되거나 USB 열거 메시지만 보이면 드라이버가 없는 것으로 확인
```

**5단계: 사용 가능한 WiFi 드라이버 모듈 확인**

```bash
# 로드된 무선 드라이버 목록 표시
lsmod | grep -E "ath|rt2|rtl|mt76|mac80211|cfg80211"
# 라우터 내장 WiFi 드라이버(wl / b43 / ath9k 등)만 있으면 USB WiFi 드라이버가 없는 것임
```

**6단계: 커뮤니티 드라이버 설치 시도 (가능한 경우)**

```bash
ipkg update
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# 검색 결과가 비어 있으면 이 DD-WRT 버전에 사용 가능한 드라이버가 없는 것으로 확인
```

### 경로 B: 권장 대안 — OpenWrt로 전환

고객이 라우터에서 ALFA USB WiFi 네트워크 카드를 사용해야 한다면, 라우터 펌웨어를 DD-WRT에서 OpenWrt로 플래싱할 것을 강력히 권장합니다. OpenWrt는 활발한 USB WiFi 드라이버 패키지 저장소를 보유하여 MT7612U / MT7610U / RTL8812AU 칩 등을 지원합니다. 자세한 절차는 [ALFA 무선 네트워크 카드는 OpenWrt를 지원하나요](https://yupitek.com/ko/blog/alfa-openwrt-router-compatibility/)를 참조하세요.

## 8. 일반적인 오류 및 문제 해결

| 증상 | 가능한 원인 | 해결 방법 |
|---|---|---|
| lsusb에 ALFA 네트워크 카드가 표시되지 않음 | USB 전원 부족 / 접촉 불량 / DD-WRT USB 코어 미활성화 | Services > USB에서 활성화 여부 확인; USB 포트 교체 또는 전원 공급형 USB Hub 사용 |
| lsusb에는 카드가 보이나 ip link에 wlan 인터페이스 없음 | 해당 칩 드라이버 누락 | DD-WRT 버전에 드라이버가 있는지 확인; 대부분 해결 불가, OpenWrt 전환 권장 |
| wlan 인터페이스는 있으나 AP 스캔 불가 | 드라이버 미완전 지원 / 모니터링 모드 충돌 | dmesg에서 펌웨어 로딩 오류 확인; Regulatory Domain 설정 확인 |
| 재부팅 후 라우터 설정 손실 | DD-WRT NVRAM 공간 부족 | 저사양 라우터에 추가 드라이버 설치를 피할 것; 하드웨어 업그레이드 또는 OpenWrt 전환 고려 |
| AWUS036ACH 고출력 시 연결 끊김 | USB 포트 전원 부족 | 전원 공급형 USB 3.0 Hub 사용; TX Power 설정을 낮춤 |

## 9. 알려진 제한 사항

- **드라이버 부재**: DD-WRT는 현행 ALFA 모델용 USB WiFi 드라이버를 공식적으로 제공하지 않으며, 이것이 근본적인 제한입니다.
- **하드웨어 자원**: DD-WRT로 플래싱 가능한 대부분의 라우터는 Flash(4-16MB)와 RAM(32-128MB)이 제한적이어서, 드라이버가 있더라도 설치하지 못할 수 있습니다.
- **Monitor/Injection 미지원**: DD-WRT의 USB WiFi 아키텍처는 침투 테스트에 필요한 Monitor Mode 및 Packet Injection을 지원하지 않습니다.
- **불안정한 AP 모드**: 동작 가능한 구형 Ralink 칩이라도, DD-WRT에서 USB WiFi의 AP 모드는 연결 끊김과 성능 문제가 자주 발생합니다.
- **버전 파편화**: 라우터 모델별 DD-WRT 컴파일 버전은 큰 차이가 있어, 한 버전의 드라이버가 다른 버전에서 작동하리라고 보장할 수 없습니다.
- **유지보수 중단**: DD-WRT의 개발 속도가 느려져 USB WiFi 드라이버가 추가될 가능성은 낮습니다.
- **보충**: DD-WRT 자체의 제한을 차치하더라도, AWUS036AX / AXER(RTL8832BU) 모델의 드라이버 유지보수자 morrownr는 Linux 사용자에게 이 칩 계열을 피할 것을 공개적으로 권고합니다([ALFA 무선 카드는 OpenWrt를 지원하나요](https://yupitek.com/ko/blog/alfa-openwrt-router-compatibility/) 9장 참조). 이는 DD-WRT 플랫폼만의 문제가 아닙니다.

**반박 조건**: 고객이 BrainSlayer / Kong 등 추가 드라이버가 포함된 커뮤니티 컴파일 버전을 사용 중이라면 실제 지원 상태가 다를 수 있습니다. 본 평가는 공식 릴리스 버전을 기준으로 합니다.

## 10. 참고 URL

| 출처 | 설명 | URL | 검증 상태 | 검증 일자 |
|---|---|---|---|---|
| DD-WRT 공식 Wiki | 설치, 지원, FAQ 주요 진입점 | https://wiki.dd-wrt.com/wiki/Main_Page | ✅ 검증됨 | 2026-09-03 |
| DD-WRT 공식 Wiki — Installation | 설치 안내 (USB 지원 포함) | https://wiki.dd-wrt.com/wiki/Installation | ✅ 홈페이지 링크로 검증 | 2026-09-03 |
| OpenWrt 공식 문서 | USB WiFi 비교 참고 자료 | https://openwrt.org/docs/start | ✅ 검증됨 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 드라이버 (DD-WRT 미통합) | https://github.com/morrownr/8812au-20210820 | ✅ 검증됨 | 2026-09-03 |
| ALFA Network 제품 개요 (Yopitek) | ALFA 현행 제품 사양 | https://yupitek.com/ko/products/alfa/ | ✅ 검증됨 | 2026-09-03 |

관련 글: [ALFA 무선 카드는 OpenWrt를 지원하나요](https://yupitek.com/ko/blog/alfa-openwrt-router-compatibility/) | [ALFA 무선 카드는 Tomato를 지원하나요](https://yupitek.com/ko/blog/alfa-tomato-router-compatibility/)

면책 조항: 본 글의 호환성 판정은 칩셋의 드라이버 상태와 DD-WRT 공식 패키지 저장소를 기준으로 합니다. DD-WRT 커뮤니티에는 다수의 커스텀 이식 버전이 존재합니다. 고객이 비공식 버전을 사용하는 경우 실제 결과가 다를 수 있습니다. 라우터 USB WiFi에는 OpenWrt를 우선적으로 선택할 것을 권장합니다.
