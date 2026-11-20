---
title: "ALFA 무선 네트워크 카드는 NVIDIA DGX Spark(GB10)를 지원하나요?"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-dgx-spark-compatibility"
tags:
  - "ALFA"
  - "NVIDIA"
  - "DGX-Spark"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "Hardware Guide"
description: "NVIDIA DGX Spark에서 ALFA 네트워크 카드 9종은 내장 드라이버로 동작해 DKMS가 필요 없고(GX10 실측), EACS·ACH·ACS는 인젝션이 가장 안정적이며 AXM·AXML은 실패합니다."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 이 글은 2026년 11월 GX10 실측 결과를 반영해 업데이트되었습니다. ASUS GX10(Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia)에서 ALFA 현행 네트워크 카드 9종은 모두 커널 내장 드라이버를 사용하며, 꽂으면 바로 사용할 수 있고 DKMS가 필요 없습니다. 전체 데이터는 [ALFA 네트워크 카드 9종 ARM64 실측 종합표](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)를 참조하시기 바랍니다. GX10에서만 실측했으며, 다른 GB10 기종은 개별적으로 테스트하지 않았습니다.

## 1. 문제 요약

고객 문의: "ALFA 시리즈 USB 무선 네트워크 카드를 NVIDIA DGX Spark(GB10 Grace Blackwell) 개인용 AI 슈퍼컴퓨터에서 사용할 수 있나요?"

간단한 결론: DGX Spark는 NVIDIA DGX OS(Ubuntu 기반, kernel 6.x)에서 동작합니다. 저희는 같은 GB10 플랫폼인 ASUS GX10(Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia)에서 ALFA 현행 USB 네트워크 카드 9종을 실측했으며, 모두 커널 내장 드라이버를 사용해 꽂으면 바로 사용할 수 있고 컴파일이나 DKMS가 필요 없습니다. DGX Spark는 동일한 GB10과 NVIDIA 커널 계열을 사용하므로 동작이 같을 것으로 예상되지만, GX10에서만 실측했으며 DGX Spark는 개별적으로 테스트하지 않았습니다. 기능 차이: MediaTek MT7921 모델(AWUS036AXM / AXML)은 stock kernel 6.17에서 패킷 인젝션에 실패하며, monitor, AP, WPA3는 사용할 수 있습니다. 나머지 7종은 monitor와 인젝션 모두 실측에서 정상 동작했습니다. 카드마다 드라이버가 메인라인에 포함된 최소 kernel 버전이 다르며(ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), 그보다 낮은 구형 커널에서만 커뮤니티 DKMS 드라이버가 필요합니다. 참고: DGX Spark의 USB 포트는 모두 USB Type-C이며, ALFA 네트워크 카드는 USB Type-A이므로 USB-C to USB-A 어댑터 또는 케이블이 필요합니다.

평가 대상: ALFA의 현행 9개 USB 네트워크 카드(AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. 대상 하드웨어 사양 분석

### 2.1 NVIDIA DGX Spark 하드웨어 사양

| 항목 | 사양 |
|---|---|
| 제품명 | NVIDIA DGX Spark |
| 핵심 칩 | NVIDIA GB10 Grace Blackwell Superchip |
| CPU | 20-core Arm(10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | NVIDIA Blackwell 아키텍처, 6144 CUDA 코어, 5세대 Tensor Core, 4세대 RT Core |
| AI 성능 | 최대 1 PetaFLOP(FP4, Sparse) / 1000 TOPS |
| 시스템 메모리 | 128GB LPDDR5x 통합 메모리(256-bit, 273 GB/s) |
| 스토리지 | 최대 4TB NVMe M.2 SSD(자체 암호화) |
| USB | 4× USB 3.2 Gen 2×2 Type-C(20Gbps), 이 중 1개는 PD 입력 지원(180W EPR PD3.1) |
| 디스플레이 출력 | 1× HDMI 2.1a |
| 유선 네트워크 | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC(200G QSFP) |
| 무선 네트워크 | Wi-Fi 7(내장) + Bluetooth 5.4 |
| 운영체제 | NVIDIA DGX OS(Ubuntu Linux 기반, kernel 6.x) |
| 아키텍처 | aarch64(ARM64) |
| 크기 | 150 × 150 × 50.5 mm(1.13L) |
| 무게 | 약 1.2 kg |
| 전원 | 240W USB-C 전원 공급 장치 |

### 2.2 소프트웨어 환경: NVIDIA DGX OS

| 항목 | 설명 |
|---|---|
| 기반 | Ubuntu Linux(NVIDIA 커스터마이징) |
| Kernel | Linux 6.x(구체적인 버전은 DGX OS 업데이트에 따라 달라짐) |
| 아키텍처 | aarch64(ARM64) |
| 사전 설치 소프트웨어 | NVIDIA AI 소프트웨어 스택(CUDA, cuDNN, TensorRT, PyTorch, Jupyter 등) |
| 패키지 관리 | apt(Debian/Ubuntu 계열) |
| 드라이버 프레임워크 | 표준 Linux kernel driver 아키텍처(cfg80211 / mac80211) |

### 2.3 핵심 특징: 최신 kernel + ARM64

DGX Spark의 소프트웨어 환경은 ALFA 네트워크 카드 호환성에 두 가지 핵심적인 영향을 미칩니다:

- Kernel 6.x(최신): kernel 6.17(GX10 실측 버전)에는 본문의 네트워크 카드 9종 드라이버가 모두 내장되어 있으며, 여기에는 mt76(MT7612U / MT7610U, 4.19+), mt7921u(MT7921AUN, 5.18+), rtw88(RTL8821CU 6.2+, RTL8812AU / RTL8811AU 6.13+), rtw89(RTL8832BU, 6.17+)가 포함됩니다. 이는 Jetson Nano의 kernel 4.9와 뚜렷이 대비됩니다.
- ARM64(aarch64) 아키텍처: 커널 내장 드라이버를 사용할 때는 ARM64에서 아무것도 컴파일할 필요가 없습니다. kernel이 해당 카드의 최소 버전보다 낮은 구형 시스템에서만 Realtek 모델에 커뮤니티 DKMS 드라이버(morrownr 계열 등, Makefile에서 CONFIG_PLATFORM_ARM64 = y 확인 필요)를 컴파일해야 합니다.

### 2.4 USB Type-C 어댑터 요구사항

DGX Spark의 USB 포트 4개는 모두 Type-C이며, ALFA 전 제품(AXML은 USB-C 제외)은 USB Type-A 인터페이스입니다:

| 모델 | 인터페이스 사양 | 어댑터 필요 여부 |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ 어댑터 불필요(직접 삽입 가능) |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ USB-C to USB-A 필요 |
| AWUS036AX | USB Type-A / USB 3.2 | ✅ 필요 |
| AWUS036AXER | USB Type-A / USB 3.2 | ✅ 필요 |
| AWUS036ACH | USB Type-A / USB 3.0 | ✅ 필요 |
| AWUS036ACHM | USB Type-A / USB 2.0 | ✅ 필요 |
| AWUS036ACM | USB Type-A / USB 3.0 | ✅ 필요 |
| AWUS036ACS | USB Type-A / USB 2.0 | ✅ 필요 |
| AWUS036EACS | USB Type-A / USB 2.0 | ✅ 필요 |

권장: USB 3.2 Gen 2×2(20Gbps)를 지원하는 USB-C to USB-A 어댑터 또는 케이블을 사용하여 AWUS036ACH / ACM / AX 등 USB 3.x 모델이 최대 속도를 낼 수 있도록 하십시오.

## 3. 현행 ALFA 네트워크 카드 사양 및 칩셋 분석

2026년 9월 기준, ALFA Network의 현행 USB 무선 네트워크 카드 라인업은 다음과 같습니다(평가 대상: 9개 모델):

| 모델 | Wi-Fi 등급 | 칩셋 | 인터페이스 | Linux 내장 드라이버 (최소 kernel 버전) |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E (6GHz 실측 동작) | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ 내장 (mt7921u, 5.18+) |
| AWUS036AXM | Wi-Fi 6E (제조사 표기, 6GHz 미실측) | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ 내장 (mt7921u, 5.18+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ 내장 (rtw89_8852bu, 6.17+) |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ 내장 (rtw89_8852bu, 6.17+) |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ 내장 (rtw88_8812au, 6.13+) |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | ✅ 내장 (mt76x0u, 4.19+) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ 내장 (mt76x2u, 4.19+) |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | ✅ 내장 (rtw88_8821au, 6.13+) |
| AWUS036EACS | Wi-Fi 5 (AC600) + 블루투스 | Realtek RTL8821CU | USB 2.0 | ✅ 내장 (rtw88_8821cu, 6.2+) |

참고: GX10에서 실측한 kernel 6.17에는 9종의 드라이버가 모두 내장되어 있습니다. 카드마다 최소 kernel 버전이 다르며(위 표의 괄호 참조), kernel이 해당 카드의 최소 버전보다 낮은 구형 시스템에서만 커뮤니티가 유지보수하는 DKMS 드라이버를 설치해야 합니다.

## 4. 적용 가능 모델 및 칩셋

### 4.1 추천 등급 분류

| 추천 등급 | 모델(칩셋) | 설명 |
|---|---|---|
| ⭐ 침투 테스트 최우선 추천 | AWUS036EACS (RTL8821CU) / AWUS036ACH (RTL8812AU) / AWUS036ACS (RTL8811AU) | 내장 드라이버로 설치 불필요. 인젝션 실측: EACS·ACH는 두 대역 모두 100%, ACS는 2.4GHz 100%·5GHz 96%. WPA handshake를 엔드투엔드로 캡처 가능 |
| ✅ 추천 | AWUS036ACM (MT7612U) | 내장 드라이버로 설치 불필요. monitor, 인젝션(2.4GHz 63–83%, 5GHz 76%), AP, WPA3 모두 사용 가능 |
| ✅ 추천 | AWUS036ACHM (MT7610U) | 내장 드라이버로 설치 불필요. 2.4GHz 인젝션 96–100%, 5GHz 인젝션은 브로드캐스트만 가능. WPA3 AP는 sae_pwe=0 설정 필요 |
| ✅ 추천 (Wi-Fi 6) | AWUS036AX / AXER (RTL8832BU) | 내장 드라이버로 설치 불필요. monitor 수신 감도 강함, 인젝션 가능(2.4GHz: AX 96%, AXER 73%), AP 80MHz 지원 |
| ⚠️ 연결 / AP 용도에만 적합 | AWUS036AXML / AXM (MT7921AUN) | 내장 드라이버로 설치 불필요. monitor, AP, WPA3는 사용 가능하지만 stock kernel 6.17에서 인젝션에 실패하므로 침투 테스트에는 부적합. AXML은 USB-C로 직접 연결 가능 |

### 4.2 사용 시나리오 권장

| 사용 시나리오 | 권장 모델 | 설명 |
|---|---|---|
| 일반 무선 인터넷(가장 간단) | 9종 모두 가능 (예: AWUS036ACM / ACHM) | 모두 커널 내장 드라이버로, 꽂으면 바로 사용 가능 |
| 무선 침투 테스트 / 모니터링 / 인젝션 | AWUS036EACS / ACH / ACS | 인젝션 실측 96–100%, WPA handshake를 엔드투엔드로 캡처 가능. AXM / AXML은 선택하지 마십시오(인젝션 실패) |
| Wi-Fi 6 + AP 핫스팟 | AWUS036AX / AXER | 2x2, 80MHz AP 실측 동작 |
| 6GHz 대역 | AWUS036AXML | 6GHz에서 WPA3 AP 구성 실측 성공. AXM은 같은 칩이지만 6GHz 미실측 |
| 기존 AWUS036ACH를 계속 사용하고 싶은 경우 | AWUS036ACH | kernel 6.13 이상에는 rtw88_8812au가 내장되어 꽂으면 바로 사용 가능, 두 대역 인젝션 실측 100% |
| 외장 WiFi 불필요(내장 사용) | — | DGX Spark는 Wi-Fi 7이 내장되어 있어 일반 인터넷에는 외장 ALFA가 불필요 |

참고: DGX Spark는 Wi-Fi 7 + Bluetooth 5.4가 내장되어 있어 일반적인 인터넷 사용 시나리오에는 외장 ALFA 네트워크 카드가 필요하지 않습니다. 외장 ALFA의 주요 수요는 침투 테스트(모니터링/인젝션), 특수 칩셋 요구사항, 또는 내장 WiFi로 부족한 경우입니다.

## 5. 환경 요구사항

### 5.1 하드웨어 요구사항

| 항목 | 요구사항 |
|---|---|
| USB 어댑터 | USB-C to USB-A 어댑터 또는 케이블(AXML 제외) |
| 전원 | DGX Spark 정품 240W USB-C 전원 공급 장치(USB 포트 전원 충분) |
| 방열 | 정품 방열로 충분(USB WiFi는 시스템 부하를 크게 증가시키지 않음) |

### 5.2 소프트웨어 요구사항

| 항목 | 요구사항 |
|---|---|
| DGX OS 버전 | 모든 현행 버전(kernel 6.x) |
| 커널 버전 | kernel 6.17(GX10 실측 6.17.0-1014-nvidia)에는 네트워크 카드 9종의 드라이버가 모두 내장되어 있어 컴파일 도구가 필요 없음. 카드마다 최소 버전이 다르며(ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), 그보다 낮을 때만 커뮤니티 DKMS 드라이버 설치 필요 |
| 무선 관리 도구 | iw, wpa_supplicant, network-manager(DGX OS 기본 설치) |

## 6. 호환성 판정

### ALFA 현행 모델 × NVIDIA DGX Spark(GB10) 호환성 매트릭스

| 모델 | 칩셋 | 드라이버 (커널 내장) | USB 인식 | STA 인터넷 | AP 모드 | Monitor | 패킷 인젝션 | 설치 난이도 | 종합 평가 |
|---|---|---|---|---|---|---|---|---|---|
| AWUS036EACS | RTL8821CU | rtw88_8821cu | ✅ | ✅ | ✅ | ✅ | ✅ 두 대역 100% | 설치 불필요 | ⭐ 최상 |
| AWUS036ACH | RTL8812AU | rtw88_8812au | ✅ | ✅ | ✅ | ✅ | ✅ 두 대역 100% | 설치 불필요 | ⭐ 최상 |
| AWUS036ACS | RTL8811AU | rtw88_8821au | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 100% / 5G 96% | 설치 불필요 | ⭐ 최상 |
| AWUS036ACM | MT7612U | mt76x2u | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 63–83% / 5G 76% | 설치 불필요 | ✅ 양호 |
| AWUS036ACHM | MT7610U | mt76x0u | ✅ | ✅ | ✅ | ✅ | ⚠️ 2.4G 96–100% / 5G 브로드캐스트만 | 설치 불필요 | ✅ 양호 |
| AWUS036AX | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ 수신 강함 | ✅ 2.4G 96% / 5G 가능 | 설치 불필요 | ✅ 양호 |
| AWUS036AXER | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ 수신 강함 | ✅ 2.4G 73% / 5G 가능 | 설치 불필요 | ✅ 양호 |
| AWUS036AXML | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ 수신 약함 | ❌ 실패 | 설치 불필요 | ⚠️ 연결 / AP 전용 |
| AWUS036AXM | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ 수신 약함 | ❌ 실패 | 설치 불필요 | ⚠️ 연결 / AP 전용 |

판정 근거: 2026-11-16~11-18에 ASUS GX10(Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia)에서 실기 테스트를 진행했으며, 테스트 대상은 자체 보유 Wi-Fi와 자체 보유 휴대폰입니다. DGX Spark는 동일한 GB10과 NVIDIA 커널 계열을 사용하므로 동작이 같을 것으로 예상되지만, GX10에서만 실측했으며 DGX Spark는 개별적으로 테스트하지 않았습니다. 전체 데이터는 [ALFA 네트워크 카드 9종 ARM64 실측 종합표](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)를 참조하시기 바랍니다.

## 7. 상세 단계별 설정 절차

### 7.1 사전 준비

**1단계: DGX Spark 부팅 및 로그인**(SSH 또는 키보드/모니터 직접 연결)

```bash
ssh username@<dgx-spark-ip>
```

**2단계: 시스템 아키텍처 및 kernel 버전 확인**

```bash
uname -m
# 예상: aarch64
uname -r
# 예상: 6.x.x(DGX OS kernel)
```

**3단계: kernel 버전이 6.17 이상인지 확인**

kernel 6.17 이상에는 네트워크 카드 9종의 드라이버가 모두 내장되어 있으므로 컴파일 도구를 설치할 필요가 없습니다. 카드마다 최소 버전이 다르며(ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), 그보다 낮은 경우에만 Realtek 모델에 커뮤니티 DKMS 드라이버가 필요합니다(7.3의 마지막 단락 참조).

### 7.2 경로 A: MediaTek 칩 모델(AWUS036ACM / ACHM / AXML / AXM) — 바로 사용

**1단계: 네트워크 카드 삽입**

USB-C to USB-A 어댑터를 사용하여(AXML은 USB-C 포트에 직접 삽입 가능) ALFA 네트워크 카드를 DGX Spark의 USB 포트에 꽂습니다.

**2단계: 네트워크 카드 감지 확인**

```bash
lsusb
# 예상 출력 예시(AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**3단계: 네트워크 인터페이스 자동 생성 확인**

```bash
ip link show
# wlx로 시작하는 인터페이스가 나타나야 함(MAC 기반 이름, in-kernel 드라이버 자동 로드)
```

**4단계: WiFi 네트워크 스캔**(아래는 wlan0을 예로 든 것이므로 `ip link show`에서 확인한 인터페이스 이름으로 바꾸십시오)

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**5단계: WiFi 연결(NetworkManager 사용)**

```bash
nmcli dev wifi list
nmcli dev wifi connect "WiFi이름" password "WiFi비밀번호"
```

**6단계:(선택) 모니터링 모드 활성화**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info
```

### 7.3 경로 B: Realtek Wi-Fi 5 모델(AWUS036ACH / ACS / EACS) — kernel 6.13+ 설치 불필요(EACS는 6.2+)

**1단계: 네트워크 카드를 꽂고 드라이버가 자동 로드되었는지 확인**

```bash
uname -r          # ACH / ACS는 6.13 이상, EACS는 6.2 이상 필요
lsusb
lsmod | grep rtw88
ip link show
```

모델별 자동 로드 모듈: ACH → `rtw88_8812au`, ACS → `rtw88_8821au`, EACS → `rtw88_8821cu`(EACS는 블루투스도 포함하며 실측에서 동작 확인).

**2단계: 연결 방법은 7.2의 5단계와 동일(nmcli 사용)**

**3단계:(선택) 모니터링 모드 및 인젝션**

⚠️ 모니터링 및 인젝션 테스트는 자신이 소유하거나 승인을 받은 네트워크에서만 수행하십시오.

```bash
sudo apt install -y aircrack-ng
IF=wlx00c0cafe0000   # ip link에서 확인한 인터페이스 이름으로 변경
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
sudo aireplay-ng --test $IF
```

- `airmon-ng check kill`은 실행하지 마십시오. NetworkManager가 종료되어 호스트의 외부 연결이 끊어집니다.
- AWUS036AXM / AXML은 stock kernel 6.17에서 `aireplay-ng --test`가 실패하며(Found 0 APs), deauth나 handshake 캡처를 할 수 없습니다.
- hcxdumptool 8.x는 2.4 GHz의 EACS를 제외한 모든 카드에서 `failed to arm`(드라이버가 active monitor를 지원하지 않음)이 발생하므로, airodump-ng + aireplay-ng를 사용하십시오.

**구형 커널(ACH / ACS는 6.13 미만, EACS는 6.2 미만)에서만 필요한 단계**: `build-essential git bc dkms`를 설치한 뒤 커뮤니티 드라이버를 컴파일합니다. 예를 들어 RTL8812AU는 morrownr/8812au-20210820을 사용합니다(Makefile에서 `CONFIG_PLATFORM_ARM64 = y` 확인). 버전이 충분하면 내장 드라이버를 그대로 사용하십시오.

### 7.4 경로 C: Wi-Fi 6 모델(AWUS036AX / AXER, RTL8832BU) — kernel 6.17+ 설치 불필요

```bash
lsusb                      # 0bda:b832가 나타나야 함
lsmod | grep rtw89_8852bu
ip link show
```

GX10 실측: 커널 내장 `rtw89_8852bu`가 자동 로드되며, monitor 수신 감도가 강하고 인젝션 가능(2.4GHz: AX 96%, AXER 73%), AP는 80MHz를 지원합니다. rtw89_8852bu는 kernel 6.17에서야 메인라인에 포함되었으므로, kernel 6.16 이하 시스템에서는 커뮤니티 DKMS 드라이버(morrownr/rtl8852bu-20250826)가 필요합니다.

## 8. 일반적인 오류 및 문제 해결

| 증상 | 가능한 원인 | 해결 방법 |
|---|---|---|
| lsusb에 ALFA 네트워크 카드가 보이지 않음 | USB-C 어댑터 불량 / 접촉 불량 | USB-C to USB-A 어댑터 교체; 어댑터가 데이터 전송을 지원하는지(충전 전용이 아닌지) 확인; 다른 USB-C 포트 시도 |
| MediaTek 칩 삽입 후 wlan 인터페이스 없음 | kernel module 미자동 로드 / firmware 누락 | 수동 로드: `sudo modprobe mt76x2u`; `dmesg \| grep mt76` 확인; firmware 설치: `sudo apt install linux-firmware` |
| Realtek 카드를 연결해도 wlan 인터페이스가 없음 | 커널이 해당 카드의 최소 버전(EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17)보다 낮아 대응 드라이버가 내장되어 있지 않음 | `uname -r`로 버전 확인. 커널을 업그레이드하거나, 구형 커널에서는 커뮤니티 DKMS 드라이버 설치 |
| 구형 커널에 DKMS 드라이버 설치 후 modprobe 시 Operation not permitted 오류 | Secure Boot / 모듈 서명 | 모듈 서명 또는 Secure Boot 비활성화 필요(내장 드라이버를 사용하면 발생하지 않음) |
| monitor / AP를 반복 전환한 뒤 어떤 신호도 스캔되지 않음 | RX 정지(RX stall) | 네트워크 카드를 뽑았다 다시 꽂아 USB를 재열거 |
| EACS / AXML을 다시 꽂은 뒤 wlx 인터페이스가 없음 | 블루투스 + Wi-Fi 복합 장치의 probe가 멈춤 | 다른 USB 포트에 다시 연결 |
| WiFi 연결 불안정 / 속도 느림 | USB-C 어댑터가 USB 2.0만 지원 | USB 3.2 Gen 2×2를 지원하는 어댑터로 교체; 어댑터에 "Data" 표기가 있는지(단순 "Charge Only"가 아닌지) 확인 |
| 내장 Wi-Fi 7과 외장 ALFA 충돌 | 두 무선 인터페이스의 라우팅 충돌 | 내장 WiFi 비활성화: `sudo nmcli radio wifi off` 또는 BIOS/UEFI에서 비활성화; 또는 라우팅 우선순위 설정 |
| 6GHz(Wi-Fi 6E) 사용 불가 | Regulatory Domain 제한 | 규제 지역 설정: `sudo iw reg set US`(미국은 6GHz 개방); AXML은 6GHz 동작을 실측으로 확인했으며, AXM은 미실측 |
| AP 모드 시작 실패 | NetworkManager와 hostapd 충돌 | Yopitek ALFA Soft AP 가이드 참조; 해당 인터페이스에 대한 NetworkManager 관리 비활성화 후 hostapd 수동 설정 |
| 절전 복귀 후 네트워크 카드 사라짐 | USB 자동 절전(autosuspend) | USB autosuspend 비활성화: `echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. 알려진 제한 사항

- USB Type-C 어댑터 요구사항: AXML을 제외한 모든 ALFA 네트워크 카드는 USB-C to USB-A 어댑터가 필요하며, 어댑터 품질이 성능과 안정성에 영향을 줍니다.
- MT7921 모델의 인젝션 실패: AWUS036AXM / AXML은 stock kernel 6.17에서 패킷 인젝션에 실패하여 deauth나 handshake 캡처를 할 수 없습니다. monitor, AP, WPA3는 사용할 수 있습니다. 주된 원인은 kernel 6.16 이후 mac80211 chanctx 회귀이며, 커뮤니티 패치 드라이버도 여전히 속도 제한이 있습니다.
- 실측 범위: ASUS GX10(kernel 6.17.0-1014-nvidia)에서만 실측했으며, DGX Spark는 개별적으로 테스트하지 않았습니다(동작은 같을 것으로 예상).
- hcxdumptool 사용 불가: 2.4 GHz의 EACS를 제외한 모든 카드에서 `failed to arm`이 발생하므로 airodump-ng + aireplay-ng를 사용하십시오.
- 내장 Wi-Fi 7과 외장 충돌 가능: DGX Spark는 Wi-Fi 7이 내장되어 있어 내장과 외장 WiFi를 동시에 사용할 때 라우팅 또는 리소스 충돌이 발생할 수 있습니다.
- AP 모드는 수동 설정 필요: DGX OS는 기본적으로 개발 환경이므로 AP 핫스팟 모드는 hostapd / dnsmasq를 수동으로 설치/설정해야 합니다.
- 6GHz 규제 제한: Wi-Fi 6E의 6GHz 대역 가용성은 규제 지역 설정에 따라 달라지며, 각 지역의 6GHz 개방 현황은 최신 규정을 확인해야 합니다.
- 구형 커널: kernel이 해당 카드의 최소 버전(EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17)보다 낮은 시스템에서만 Realtek 모델에 커뮤니티 DKMS 드라이버(morrownr)가 필요하며, 커널을 업데이트할 때마다 재컴파일해야 합니다.
- 침투 테스트 기능 차이: GX10 실측 인젝션 성공률은 Realtek rtw88 모델이 가장 높았습니다(EACS, ACH 두 대역 100%). MediaTek mt76 모델(ACM / ACHM)은 사용 가능하며, MT7921(AXM / AXML)은 실패했습니다.
- 블루투스 기능: AWUS036AXML과 AWUS036EACS의 블루투스는 GX10에서 실측으로 동작을 확인했습니다. AWUS036AXM의 블루투스는 별도로 검증하지 않았습니다(DGX Spark에는 BT 5.4가 내장됨).
- RTL8832BU(AWUS036AX / AXER): 드라이버 유지보수자 morrownr는 rtl8852/32au 계열의 out-of-tree 드라이버를 피하라고 공개적으로 권고한 바 있습니다(출처는 10장 참조). 이번 GX10 실측에서는 커널 내장 `rtw89_8852bu`를 사용했으며 monitor, 인젝션, AP, WPA3 모두 사용할 수 있었습니다. 이 결론은 kernel 6.17 이상의 내장 드라이버에만 적용됩니다.
- RTL8812AU(AWUS036ACH): mac80211 표준 in-kernel 드라이버 `rtw88_8812au`는 kernel 6.13에서 mainline에 병합되었고 6.14부터 품질이 성숙했습니다(morrownr 공지). GX10 실측에서 kernel 6.17에 꽂으면 바로 동작했고 두 대역 인젝션이 100%였습니다. 고객 응대 시 답변 전에 고객에게 `uname -r`로 6.13 이상인지 확인을 요청할 수 있습니다.

반박 조건: DGX OS 업데이트 후 kernel 버전이나 USB 컨트롤러 드라이버 변경으로 동작이 달라지거나, DGX Spark 실기에서 GX10과 다른 결과가 측정되는 경우, 본문 6장의 호환성 매트릭스를 재검토해야 합니다. 향후 커널에서 mt7921u의 인젝션 문제가 수정되면 AWUS036AXM / AXML의 평가는 "연결 / AP 전용"에서 상향될 수 있습니다.

## 10. 참고 URL

| 출처 | 설명 | URL | 검증 상태 | 검증 일자 |
|---|---|---|---|---|
| NVIDIA DGX Spark 공식 페이지 | DGX Spark 사양 및 플랫폼 정보 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ 검증됨 | 2026-09-03 |
| NVIDIA DGX 문서 | DGX OS 시스템 아키텍처 및 kernel 버전 | https://docs.nvidia.com/dgx/dgx-spark | ✅ 검증됨 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 드라이버(ARM64 지원) | https://github.com/morrownr/8812au-20210820 | ✅ 검증됨 | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8821CU Linux 드라이버(구형 커널용) | https://github.com/morrownr/8821cu-20210916 | ✅ 검증됨 | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux 드라이버 | https://github.com/morrownr/rtl8852bu-20250826 | ✅ 검증됨 | 2026-09-03 |
| Linux kernel mt76 드라이버 문서 | MediaTek mt76 / mt7921 mainline 드라이버 설명(각 칩의 지원 시작 kernel 버전 포함) | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ 검증됨 | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide(Yopitek) | ALFA의 Linux AP 모드 설정 가이드 | https://yupitek.com/ko/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 검증됨 | 2026-09-03 |
| ALFA Network 제품 개요(Yopitek) | ALFA 현행 제품 사양 | https://yupitek.com/ko/products/alfa/ | ✅ 검증됨 | 2026-09-03 |
| ALFA 네트워크 카드 9종 ARM64 실측 종합표 (Yopitek) | ASUS GX10 + Ubuntu 24.04 ARM64 실기 테스트 | https://yupitek.com/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ 실측 | 2026-11-18 |
| morrownr/USB-WiFi Issue #314 | 드라이버 유지보수자 공식 성명: rtl8852/32au(RTL8832BU) 칩 회피 권고 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 검증됨 | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | RTL8812AU 드라이버 상태 최신 공지(kernel 6.13 mainline 병합, 6.14 품질 성숙) | https://github.com/morrownr/8812au-20210820 | ✅ 검증됨 | 2026-09-03 |

관련 글: [ALFA 무선 네트워크 카드는 MSI EdgeXpert를 지원하나요](https://yupitek.com/ko/blog/alfa-msi-edgexpert-compatibility/) | [ALFA 무선 네트워크 카드는 ASUS Ascent GX10을 지원하나요](https://yupitek.com/ko/blog/alfa-asus-ascent-gx10-compatibility/) | [ALFA 무선 네트워크 카드는 ALTOS BrainSphere GB10 F1을 지원하나요](https://yupitek.com/ko/blog/alfa-altos-brainsphere-gb10-compatibility/) | [ALFA 무선 네트워크 카드는 GIGABYTE AI TOP ATOM을 지원하나요](https://yupitek.com/ko/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [ALFA 무선 네트워크 카드는 NVIDIA Jetson Nano를 지원하나요](https://yupitek.com/ko/blog/alfa-nvidia-jetson-nano-compatibility/)

면책 조항: 본 글의 호환성 판정은 2026년 11월 ASUS GX10(Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia)에서의 실기 테스트를 기준으로 합니다. DGX Spark는 GX10과 동일한 GB10과 NVIDIA 커널 계열을 사용하므로 동작이 같을 것으로 예상되지만, 개별적으로 테스트하지는 않았습니다. GX10에서 실측한 kernel 6.17에는 ALFA 네트워크 카드 9종의 드라이버가 모두 내장되어 있으며(카드마다 최소 버전이 다름), kernel이 해당 카드의 최소 버전보다 낮을 때만 커뮤니티 DKMS 드라이버(morrownr)가 필요합니다. DGX Spark는 Wi-Fi 7이 내장되어 있어 외장 ALFA 네트워크 카드는 주로 침투 테스트나 특수 칩셋 요구사항에 사용됩니다. USB-C 어댑터의 품질은 사용 경험에 직접적인 영향을 미치므로, 브랜드가 있고 USB 3.2 Gen 2×2로 표기된 어댑터를 선택할 것을 권장합니다. 모니터링과 인젝션은 자신이 소유하거나 승인을 받은 네트워크에서만 수행하십시오.
