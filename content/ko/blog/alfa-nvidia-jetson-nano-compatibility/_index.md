---
title: "ALFA 무선 네트워크 카드는 NVIDIA Jetson Nano를 지원하나요?"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-jetson-nano-compatibility"
tags:
  - "ALFA"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "NVIDIA"
  - "Jetson-Nano"
  - "JetPack"
  - "ARM64"
  - "Linux-WiFi"
categories:
  - "Hardware Guide"
description: "Jetson Nano는 다수의 ALFA 네트워크 카드를 지원하며 Realtek 모델이 실용적인 선택입니다. 다만 Wi-Fi 6E 모델은 커널 제약으로 호환되지 않습니다."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

## 1. 문제 요약

고객 문의: "ALFA 시리즈 USB 무선 네트워크 카드를 NVIDIA Jetson Nano 개발 보드에서 사용할 수 있나요?"

간단한 결론: Jetson Nano는 대부분의 ALFA 네트워크 카드를 사용할 수 있으나, 핵심 제약은 JetPack 4.x의 구형 Linux 커널 4.9 버전에 있습니다(평가 근거: ALFA의 현행 9개 USB 네트워크 카드 중 3개는 성숙하여 바로 사용 가능, 2개는 고급 컴파일 필요, 2개는 미검증, 2개는 사용 불가). Realtek 칩셋 모델(AWUS036ACH / ACS / EACS)은 out-of-tree 드라이버를 직접 컴파일할 수 있어 Jetson Nano에 실용적인 선택입니다. MediaTek MT7612U / MT7610U는 mt76 드라이버의 백포트 또는 자체 컴파일이 필요합니다. Wi-Fi 6E 모델인 MT7921AUN(AWUS036AXML / AXM)은 커널 5.18+가 필요하므로 Jetson Nano에서는 실제로 사용할 수 없습니다. 침투 테스트 시나리오에서는 AWUS036ACH(RTL8812AU)가 1순위이며, 일반 인터넷 사용에는 AWUS036ACH(안정적) 또는 AWUS036ACM(mt76 컴파일 필요)이 1순위입니다.

## 2. 대상 하드웨어 사양 아키텍처 분석

### 2.1 NVIDIA Jetson Nano 하드웨어 사양

| 항목 | 사양 |
|---|---|
| 모듈 | Jetson Nano Module (P3448) |
| CPU | Quad-core ARM Cortex-A57 (ARMv8-A / aarch64) |
| GPU | NVIDIA Maxwell 아키텍처, 128 CUDA 코어 |
| 메모리 | 4GB LPDDR4 (64-bit, 25.6 GB/s) |
| 저장장치 | microSD (개발 보드) / eMMC (양산 모듈) |
| USB | 4x USB 3.0 Type-A + 1x USB 2.0 Micro-B (Device Mode / 전원 공급) |
| 네트워크 | 1x Gigabit Ethernet (RJ45) |
| 무선 | 내장 WiFi / Bluetooth 없음 (외장 USB 또는 M.2 확장 필요) |
| 전원 공급 | 5V/4A DC 커넥터 (권장) 또는 micro-USB 5V/2A |
| 크기 | 100mm × 80mm (개발 보드) |

### 2.2 소프트웨어 환경: JetPack 4.x

| 항목 | 내용 |
|---|---|
| 운영체제 | Linux for Tegra (L4T), Ubuntu 18.04 LTS 기반 |
| 커널 버전 | Linux 4.9 (L4T R32.x / JetPack 4.6.x) |
| 아키텍처 | aarch64 (ARM64) |
| 컴파일러 | GCC 7.5 (기본) / GCC 8 (설치 가능) |
| 최신 버전 | JetPack 4.6.4 (L4T R32.7.4), 유지보수 모드 진입 |
| 향후 업그레이드 | Jetson Nano는 하드웨어 제약으로 JetPack 5.x(커널 5.10)를 지원하지 않음 |

### 2.3 핵심 제약: 커널 4.9

Jetson Nano의 커널 4.9는 호환성을 판정하는 핵심 변수입니다:

| 드라이버 | 메인라인 통합 커널 버전 | Jetson Nano (커널 4.9) 사용 가능 여부 |
|---|---|---|
| mt76x2u (MT7612U) | 4.19 | ❌ 백포트 / 자체 컴파일 필요 |
| mt76x0u (MT7610U) | 4.19 | ❌ 백포트 / 자체 컴파일 필요 |
| mt7921u (MT7921AUN) | 5.18 | ❌ 사용 불가 (격차가 너무 큼); GX10(kernel 6.17)에서 monitor는 동작하나 인젝션 실패(주원인은 kernel 6.16 이후 mac80211 chanctx 회귀이며 펌웨어의 속도 고정도 있음, 칩 자체의 한계 아님) |
| rtl8812au (RTL8812AU) | 6.13 (rtw88_8812au) | ✅ kernel 4.9에는 내장 드라이버가 없어 out-of-tree 드라이버를 컴파일해야 함; GX10(kernel 6.17)에서는 내장 드라이버로 양 대역 인젝션 100% 실측 |
| rtl8821cu (RTL8821CU) | 6.2 (rtw88_8821cu); 커널 4.9에는 없음 | ✅ out-of-tree 드라이버 컴파일 가능 (커널 6.2 이전 전용) |
| rtw89 (RTL8832BU) | 6.17 (rtw89_8852bu) | ❌ kernel 4.9에는 내장되어 있지 않아 직접 컴파일이 필요하며 호환성 미확인; GX10(kernel 6.17)에서 monitor 동작, 2.4G 인젝션 AX 96%, AXER 73% |

### 2.4 USB 전원 공급 제약

Jetson Nano 개발 보드의 4개 USB 3.0 Type-A 포트는 전원 예산을 공유합니다:

- DC 전원(5V/4A) 사용 시 USB 포트의 총 출력은 약 1.5A(5V)
- micro-USB 전원(5V/2A) 사용 시 총 출력은 약 0.5A에 불과
- ALFA 고출력 네트워크 카드(AWUS036ACH)는 피크 시 800mA-1A에 도달
- 권장: DC 전원 + 전원 공급형 USB 3.0 Hub를 사용하여 전력 부족으로 인한 연결 끊김이나 시스템 재시작을 방지

## 3. 현행 ALFA 네트워크 카드 사양 및 칩셋 분석

2026년 9월 기준, ALFA Network의 현행 USB 무선 네트워크 카드 라인업은 다음과 같습니다:

| 모델 | Wi-Fi 등급 | 칩셋 | 인터페이스 | Jetson Nano 호환성 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ 커널 5.18+ 필요, 사용 불가 |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ 상동 |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtl8852bu 자체 컴파일 필요, 미검증 |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ 상동 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ Morrownr/8812au 컴파일, 성숙 |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | ⚠️ mt76x0u 백포트 필요 |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ⚠️ mt76x2u 백포트 필요 |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | ✅ Morrownr/8812au 드라이버 포함 |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8821CU | USB 2.0 | ✅ Morrownr/8821cu 컴파일 |

## 4. 적용 가능 모델 및 칩셋

### 4.1 추천 분류

| 추천 분류 | 모델 (칩셋) | 설명 |
|---|---|---|
| ⭐ 강력 추천 (침투 테스트) | AWUS036ACH (RTL8812AU) | 드라이버 성숙, Monitor Mode + Packet Injection 지원, Jetson Nano에서 가장 널리 사용되는 ALFA 네트워크 카드 |
| ✅ 추천 (일반 인터넷) | AWUS036ACH (RTL8812AU) | 듀얼밴드 AC1200, 드라이버 설치 간편, 안정적 |
| ✅ 추천 (저전력) | AWUS036EACS (RTL8821CU) | AC600 듀얼밴드, USB 2.0 저전력, 간단한 인터넷 사용에 적합 |
| ✅ 추천 (입문) | AWUS036ACS (RTL8811AU) | AC600 듀얼밴드, 8812au 드라이버로 커버됨 |
| ⚠️ 사용 가능하나 수동 컴파일 필요 | AWUS036ACM (MT7612U) | 커널 4.9에 mt76 드라이버 백포트 필요, 기술 난이도 높음 |
| ⚠️ 사용 가능하나 수동 컴파일 필요 | AWUS036ACHM (MT7610U) | 상동, 433Mbps만 지원 |
| ⚠️ 미검증 / 비권장 | AWUS036AX / AXER (RTL8832BU) | Wi-Fi 6, rtl8852bu 컴파일 필요, 커널 4.9 호환성 미검증 |
| ❌ 사용 불가 | AWUS036AXML / AXM (MT7921AUN) | Wi-Fi 6E, 커널 5.18+ 필요, Jetson Nano 업그레이드 불가 |

### 4.2 추천 적용 시나리오

| 적용 시나리오 | 추천 모델 | 설명 |
|---|---|---|
| 무선 침투 테스트 / 모니터링 / Injection | AWUS036ACH | RTL8812AU 드라이버가 Monitor + Injection 지원, 커뮤니티 검증 양호 |
| 로봇 / 드론 무선 제어 | AWUS036ACH 또는 AWUS036EACS | 안정적 연결, 낮은 지연 |
| 일반 IoT 게이트웨이 인터넷 | AWUS036EACS / ACS | 저전력, USB 2.0로 충분, 에너지 절약 |
| 5GHz 고속 인터넷 필요 | AWUS036ACH | AC1200, 5GHz 867Mbps |
| Wi-Fi 6 / 6E 수요 | ❌ 사용 가능한 옵션 없음 | Jetson Nano는 최신 Wi-Fi 6/6E 칩을 지원하지 않음 |

## 5. 환경 요구사항

### 5.1 하드웨어 요구사항

| 항목 | 최소 요구사항 | 권장 |
|---|---|---|
| Jetson Nano 개발 보드 | B01 / A02 버전 모두 적합 | B01 (CSI 카메라 포트 2개) |
| 전원 공급 | 5V/2A micro-USB | 5V/4A DC 커넥터 (다중 USB 장치 사용 시 필요) |
| USB Hub | 불필요 | 전원 공급형 USB 3.0 Hub (고출력 네트워크 카드 사용 시) |
| 냉각 | 방열판 (기본 동봉) | 팬 + 방열판 (장시간 부하 시) |
| 저장장치 | 16GB microSD | 32GB+ UHS-I microSD (드라이버 컴파일 공간 확보에 필요) |

### 5.2 소프트웨어 요구사항

| 항목 | 요구사항 |
|---|---|
| JetPack 버전 | 4.6.x (L4T R32.7.x) |
| 핵심 도구 | build-essential, git, bc, libssl-dev, flex, bison |
| 커널 소스 코드 | 해당 L4T 버전의 커널 소스 코드 다운로드 필요 (mt76 백포트 컴파일 시 필요) |
| 네트워크 | 컴파일 중 유선 네트워크 연결 필요 (Gigabit Ethernet 포트 경유) |

## 6. 호환성 판정

### ALFA 현행 모델 × NVIDIA Jetson Nano 호환성 매트릭스

| 모델 | 칩셋 | 드라이버 방식 | USB 감지 | STA 인터넷 | AP 모드 | Monitor | 설치 복잡도 | 종합 판정 |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | 8812au 컴파일 | ✅ | ✅ | ✅ | ✅ | 중간 | ⭐ 최상 |
| AWUS036ACS | RTL8811AU | 8812au 커버 | ✅ | ✅ | ⚠️ | ❌ | 중간 | ✅ 양호 |
| AWUS036EACS | RTL8821CU | 8821cu 컴파일 | ✅ | ⚠️ | ❌ | ❌ | 중간 | ✅ 양호 |
| AWUS036ACM | MT7612U | mt76x2u 백포트 | ✅ | ✅ | ✅ | ✅ | 높음 | ⚠️ 사용 가능 |
| AWUS036ACHM | MT7610U | mt76x0u 백포트 | ✅ | ✅ | ⚠️ | ⚠️ | 높음 | ⚠️ 사용 가능 |
| AWUS036AX | RTL8832BU | rtl8852bu 컴파일 | ⚠️ | ❌ | ❌ | ❌ | 높음 | ❌ 비권장 |
| AWUS036AXER | RTL8832BU | 상동 | ⚠️ | ❌ | ❌ | ❌ | 높음 | ❌ 비권장 |
| AWUS036AXML | MT7921AUN | 커널 5.18+ 필요 | ❌ | ❌ | ❌ | ❌ | — | ❌ 사용 불가 |
| AWUS036AXM | MT7921AUN | 상동 | ❌ | ❌ | ❌ | ❌ | — | ❌ 사용 불가 |

평가 근거: Jetson Nano JetPack 4.x 커널 4.9에서의 드라이버 사용 가능 여부 + 커뮤니티 테스트(Jetson Nano 포럼, GitHub morrownr 드라이버 issue). MT7921AUN은 Jetson Nano가 커널 5.18+로 업그레이드할 수 없으므로 사용 불가로 평가합니다.

## 7. 단계별 상세 설정 절차

### 7.1 사전 작업: 시스템 업데이트 및 컴파일 환경

**1단계: 부팅 후 Jetson Nano에 SSH 로그인**

```bash
ssh username@<jetson-nano-ip>
```

**2단계: 시스템 패키지 업데이트**

```bash
sudo apt update
sudo apt upgrade -y
```

**3단계: 컴파일 도구 및 의존성 설치**

```bash
sudo apt install -y build-essential git bc libssl-dev flex bison dkms
```

**4단계: 커널 버전 확인**

```bash
uname -r
# 예상 출력: 4.9.337-tegra (또는 유사한 4.9.x-tegra)
```

### 7.2 경로 A: Realtek 칩셋 모델 (AWUS036ACH / ACS / EACS) — 권장

예시: AWUS036ACH (RTL8812AU)

**1단계: 드라이버 소스 코드 다운로드**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**2단계: (선택) ARM64용 컴파일 설정 조정**

Makefile을 편집하여 다음 설정이 포함되어 있는지 확인합니다:

```
CONFIG_PLATFORM_ARM64 = y
```

(대부분의 최신 Makefile은 aarch64를 자동으로 감지합니다)

**3단계: 컴파일 및 설치**

```bash
make
sudo make install
```

**4단계: 드라이버 모듈 로드**

```bash
sudo modprobe 8812au
# 또는 재부팅
sudo reboot
```

**5단계: ALFA 네트워크 카드 삽입 및 네트워크 인터페이스 확인**

```bash
ip link show
# 예상 출력: wlan0 인터페이스
# 없으면 dmesg 확인
dmesg | grep -i "8812au\|rtl8812\|usb"
```

**6단계: WiFi 네트워크 스캔 (기능 테스트)**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**7단계: WiFi 네트워크 연결 (NetworkManager / nmcli 사용)**

```bash
# Jetson Nano는 기본적으로 NetworkManager가 설치되어 있음
nmcli dev wifi list
nmcli dev wifi connect "WiFi 이름" password "WiFi 비밀번호"
```

**8단계: (선택) AP 핫스팟 모드 설정**

```bash
# hostapd 및 dnsmasq 설치
sudo apt install -y hostapd dnsmasq
# ALFA Soft AP 가이드 참조
# https://yupitek.com/ko/blog/alfa-soft-ap-wifi-hotspot-linux-guide/
```

**9단계: 모니터 모드 활성화 (침투 테스트용)**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# 확인
sudo iw dev wlan0 info
# type이 monitor로 표시되어야 함
# 패킷 인젝션 테스트
sudo aireplay-ng --test wlan0
```

### 7.3 경로 B: MediaTek 칩셋 모델 (AWUS036ACM / ACHM) — 고급

예시: AWUS036ACM (MT7612U), mt76 드라이버를 백포트해야 합니다:

**1단계: Jetson Nano 커널 소스 코드 다운로드**

```bash
# L4T 버전에 맞는 커널 소스 코드 다운로드
# 예: L4T R32.7.4:
wget https://developer.nvidia.com/embedded/l4t/r32_release_v7.4/sources/public_sources.tbz2
tar -xjf public_sources.tbz2
cd Linux_for_Tegra/source/public
tar -xjf kernel_src.tbz2
```

**2단계: 커널 컴파일 환경 준비**

```bash
cd kernel/kernel-4.9
# 기본 설정 생성
make tegra_defconfig
# menuconfig로 mt76 옵션 활성화
make menuconfig
# 이동 경로: Device Drivers > Network device support > Wireless LAN
# 선택: <M> MediaTek MT76x2U USB support
# 선택: <M> MediaTek MT76x0U USB support
```

**3단계: 커널 모듈 컴파일**

```bash
make modules_prepare
make M=drivers/net/wireless/mediatek/mt76 modules
```

**4단계: 모듈 설치**

```bash
sudo make M=drivers/net/wireless/mediatek/mt76 modules_install
sudo depmod -a
```

**5단계: 드라이버 로드**

```bash
sudo modprobe mt76x2u
# AWUS036ACM 삽입
dmesg | grep mt76
ip link show
```

⚠️ 주의: 커널 4.9에 mt76를 백포트하면 컴파일 오류가 발생할 수 있으며 소스 코드의 수동 수정이 필요합니다. 이는 고급 작업으로, 커널 컴파일 경험이 있는 사용자만 시도해야 합니다. 어려움이 있으면 AWUS036ACH(RTL8812AU)로 전환하는 것을 권장합니다.

### 7.4 경로 C: Wi-Fi 6 / 6E 모델 (AWUS036AX / AXER / AXML / AXM)

- AWUS036AXML / AXM (MT7921AUN): 사용 불가. Jetson Nano의 커널 4.9는 5.18+로 업그레이드할 수 없으며, mt7921u 드라이버는 백포트할 수 없습니다(격차가 너무 크고 최신 커널 인프라에 의존함).
- AWUS036AX / AXER (RTL8832BU): Jetson Nano에서는 비권장. kernel 4.9에는 내장 드라이버가 없어 morrownr/rtl8852bu를 직접 컴파일해야 하며 커뮤니티 검증도 없습니다. rtw89_8852bu는 kernel 6.17부터 mainline에 포함되며, GX10(kernel 6.17)에서 monitor 동작, 2.4G 인젝션은 AX 96%, AXER 73%였습니다. Wi-Fi 6이 필요하면 kernel 6.17 이상 플랫폼을 권장합니다.

## 8. 일반적인 오류 및 문제 해결

| 증상 | 가능한 원인 | 해결 방법 |
|---|---|---|
| 네트워크 카드 삽입 후 dmesg에 반응 없음 | USB 전압 부족 / 접촉 불량 | DC 전원(5V/4A) 사용; USB 포트 교체; 전원 공급형 USB Hub 사용 |
| 8812au make 컴파일 시 오류: gcc: error: unrecognized command line option | GCC가 너무 오래됨 | GCC 8 설치: `sudo apt install gcc-8 g++-8` 후 Makefile에 `CC = gcc-8` 지정 |
| modprobe 8812au 시 오류: Required key not available | Secure Boot 활성화됨 (Jetson Nano는 일반적으로 이 문제 없음) | Jetson Nano의 Secure Boot가 비활성화되어 있는지 확인; 모듈 재서명 또는 Secure Boot 비활성화 |
| wlan0 인터페이스는 보이나 AP를 스캔할 수 없음 | Regulatory Domain 미설정 / 드라이버 누락 | Regulatory Domain 설정: `sudo iw reg set TW`; dmesg에서 펌웨어 로딩 오류 확인 |
| 고출력 시 시스템 재시작 또는 네트워크 카드 연결 끊김 | USB 전압 부족 | DC 전원 + 전원 공급형 USB Hub 사용; TX Power 낮춤: `sudo iw dev wlan0 set txpower fixed 2000` |
| 모니터 모드에서 aireplay-ng --test가 Injection is working!을 표시하나 실제 공격은 무효 | 드라이버 인젝션 기능 제한 / 채널 충돌 | RTL8812AU 인젝션 기능은 기본적으로 사용 가능; `airmon-ng check kill`로 NetworkManager를 중지했는지 확인; 다른 채널 시도 |
| mt76 백포트 컴파일 실패 | 커널 4.9와 최신 mt76 소스 코드 간 큰 차이 | 구버전 mt76(커널 4.19용 커밋에 해당) 시도; 또는 AWUS036ACH 사용 |
| 시스템 절전 해제 후 네트워크 카드 사라짐 | USB 절전 모드 | USB autosuspend 비활성화: `echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |
| AWUS036ACH가 5GHz를 사용할 수 없음 | 지역 규제 제한 / 드라이버 채널 테이블 | `sudo iw reg set US` 설정(미국 규정은 더 많은 5GHz 채널 개방); 사용 채널이 현지 규정 범위에서 허용되는지 확인 |

## 9. 알려진 제한 사항

- **커널 버전 4.9에 고정**: Jetson Nano는 JetPack 5.x를 지원하지 않아 커널 업그레이드가 불가능하며, 이것이 모든 호환성 문제의 근원입니다.
- **MT7921AUN (Wi-Fi 6E) 완전 사용 불가**: 커널 5.18+가 필요하며 4.9로 백포트할 수 없습니다.
- **MediaTek mt76 칩은 수동 백포트 필요**: AWUS036ACM / ACHM 사용자는 직접 커널 모듈을 컴파일해야 하며 기술 난이도가 높습니다.
- ℹ️ **Wi-Fi 6 (RTL8832BU)**: rtw89_8852bu는 kernel 6.17부터 mainline에 포함되며, 오래된 kernel(예: Jetson Nano의 4.9)에서만 커뮤니티 드라이버 morrownr/rtl8852bu가 필요합니다. 이 커뮤니티 드라이버는 kernel 4.9에서 검증되지 않았습니다. GX10(kernel 6.17)에서 monitor 동작, 2.4G 인젝션 AX 96%, AXER 73%.
- **USB 전원 공급 제약**: 4개 USB 포트가 약 1.5A(DC 전원)를 공유하므로, 고출력 네트워크 카드는 전원 공급형 Hub를 사용해야 합니다.
- **AP 모드 성능**: Jetson Nano의 CPU 성능이 제한적이어서 USB WiFi AP 성능이 기대 이하일 수 있습니다.
- **모니터 / 인젝션 기능 차이**: RTL8812AU가 가장 잘 지원하며, MediaTek 칩은 커널 4.9에 백포트한 후 인젝션 기능이 불안정할 수 있습니다.
- **장기 유지보수**: JetPack 4.x는 유지보수 모드에 진입하여 새로운 기능이나 드라이버 업데이트가 제공되지 않습니다.
- **Bluetooth 기능**: AWUS036AXM의 Bluetooth 5.2 기능은 Jetson Nano에서 검증되지 않았습니다(BlueZ 지원 필요).
- **냉각**: USB WiFi를 고출력으로 장시간 사용하면 Jetson Nano의 전체 온도가 상승할 수 있으므로 팬 추가를 권장합니다.

반박 조건: 이 판정은 JetPack 4.6.x(커널 4.9)를 기준으로 합니다. 향후 NVIDIA가 Jetson Nano용 JetPack 5.x 지원을 출시하거나(현재는 공식적으로 미지원) 커뮤니티에서 안정적인 커널 5.x 백포트가 등장한다면, 4장에서 내린 사용 불가 판정을 재평가해야 합니다.

## 10. 참고 URL

| 출처 | 설명 | URL | 검증 상태 | 검증 일자 |
|---|---|---|---|---|
| NVIDIA Jetson Nano 공식 페이지 | Jetson Nano 하드웨어 사양 | https://developer.nvidia.com/embedded/jetson-nano | ✅ 검증됨 | 2026-09-03 |
| NVIDIA JetPack SDK 공식 페이지 | JetPack 버전 및 커널 정보 | https://developer.nvidia.com/embedded/jetpack | ✅ 검증됨 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 드라이버 (Jetson Nano 호환) | https://github.com/morrownr/8812au-20210820 | ✅ 검증됨 | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8821CU Linux 드라이버 | https://github.com/morrownr/8821cu-20210916 | ✅ 검증됨 | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide (Yopitek) | Linux에서 ALFA AP 모드 설정 | https://yupitek.com/ko/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 검증됨 | 2026-09-03 |
| ALFA Network 제품 개요 (Yopitek) | ALFA 현행 제품 사양 | https://yupitek.com/ko/products/alfa/ | ✅ 검증됨 | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | 드라이버 유지보수자의 rtl8852/32au(RTL8832BU) 커뮤니티 드라이버에 대한 과거 평가; kernel 6.17부터 내장 rtw89_8852bu 드라이버 제공 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 검증됨 | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko는 커널 5.19+에서만 커널에 포함됨 (드라이버 유지보수자 발언) | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ 검증됨 | 2026-09-03 |

관련 글: [ALFA 무선 네트워크 카드는 NVIDIA DGX Spark를 지원하나요](https://yupitek.com/ko/blog/alfa-nvidia-dgx-spark-compatibility/) (GB10 플랫폼 비교, 커널 6.x 환경) | [ALFA 무선 네트워크 카드는 OpenWrt를 지원하나요](https://yupitek.com/ko/blog/alfa-openwrt-router-compatibility/)

면책 조항: 본 문서의 호환성 판정은 Jetson Nano JetPack 4.6.x(커널 4.9)를 기준으로 합니다. Realtek 칩 드라이버는 커뮤니티(morrownr)가 유지보수하며, 실제 안정성은 버전에 따라 다를 수 있습니다. MediaTek mt76 칩의 백포트는 커널 컴파일 경험이 필요하며 100% 성공을 보장하지 않습니다. Wi-Fi 6/6E 또는 최신 커널 지원이 필요하다면 Jetson Orin 시리즈(JetPack 5.x+)로 업그레이드하거나 x86 컴퓨터 사용을 권장합니다.
