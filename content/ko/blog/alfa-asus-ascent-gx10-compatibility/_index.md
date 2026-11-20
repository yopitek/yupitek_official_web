---
title: "ASUS Ascent GX10(GB10)에서의 ALFA 무선 랜카드 호환성"
date: 2026-09-03
draft: false
slug: "alfa-asus-ascent-gx10-compatibility"
tags:
  - "ALFA"
  - "ASUS"
  - "Ascent-GX10"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "Hardware Guide"
description: "ASUS Ascent GX10에서 ALFA 랜카드 9종은 내장 드라이버로 동작해 DKMS가 필요 없고(GX10 실측), EACS·ACH·ACS는 인젝션이 가장 안정적이며 AXM·AXML은 실패합니다."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 이 글은 2026년 11월 GX10 실측 결과를 반영해 업데이트되었습니다. ASUS GX10(Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia)에서 ALFA 현행 랜카드 9종은 모두 커널 내장 드라이버를 사용하며, 꽂으면 바로 사용할 수 있고 DKMS가 필요 없습니다. 전체 데이터는 [ALFA 랜카드 9종 ARM64 실측 종합표](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)를 참조하시기 바랍니다. GX10에서만 실측했으며, 다른 GB10 기종은 개별적으로 테스트하지 않았습니다.

## 1. 문제 요약

고객 문의: "ALFA 시리즈 USB 무선 랜카드를 ASUS Ascent GX10(NVIDIA GB10 Grace Blackwell) AI 슈퍼컴퓨터에서 사용할 수 있습니까?"

간단한 결론: ASUS Ascent GX10과 NVIDIA DGX Spark는 동일한 GB10 칩과 NVIDIA 커널 계열을 사용합니다. 저희는 ASUS GX10(Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia)에서 ALFA 현행 USB 랜카드 9종(AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML)을 실측했으며, 모두 커널 내장 드라이버를 사용해 꽂으면 바로 사용할 수 있고 컴파일이나 DKMS가 필요 없습니다. 본 문서의 기종이 바로 실측 장비입니다. 기능 차이: MediaTek MT7921 모델(AWUS036AXM / AXML)은 stock kernel 6.17에서 패킷 인젝션(packet injection)에 실패하며, monitor, AP, WPA3는 사용할 수 있습니다. 나머지 7종은 monitor와 인젝션 모두 실측에서 정상 동작했습니다. 카드마다 드라이버가 메인라인에 포함된 최소 kernel 버전이 다르며(ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), 그보다 낮은 구형 커널에서만 커뮤니티 DKMS 드라이버가 필요합니다. 참고: GX10의 모든 USB 포트는 USB Type-C(데이터 포트 3개 + PD 입력 포트 1개)이므로, ALFA 랜카드(AXML 제외)는 USB-C to USB-A 어댑터가 필요합니다.

## 2. 대상 하드웨어 사양 및 아키텍처 분석

### 2.1 ASUS Ascent GX10 하드웨어 사양

| 항목 | 사양 |
|---|---|
| 제품명 | ASUS Ascent GX10 |
| 핵심 칩 | NVIDIA GB10 Grace Blackwell Superchip (DGX Spark 플랫폼) |
| CPU | 20코어 Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | NVIDIA Blackwell 아키텍처, 6144 CUDA 코어, 5세대 Tensor 코어, 4세대 RT 코어 |
| AI 성능 | 최대 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| 시스템 메모리 | 128GB LPDDR5x 통합 메모리 (256-bit, 273 GB/s) |
| 저장 장치 | 최대 4TB NVMe M.2 SSD (자체 암호화) |
| USB | 3× USB 3.2 Gen 2×2 Type-C (20Gbps, DP Alt Mode / DisplayPort 2.1) + 1× USB 3.2 Gen 2×2 Type-C (PD 입력, 180W EPR PD3.1) |
| 디스플레이 출력 | 1× HDMI 2.1 (USB-C DP Alt Mode와 함께 다중 디스플레이 출력 가능) |
| 유선 네트워크 | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (2× 200G QSFP112) |
| 무선 네트워크 | Wi-Fi 7 (MediaTek AW-EM637, 2×2 MIMO) + Bluetooth 5.4 |
| 운영체제 | NVIDIA DGX OS (Ubuntu Linux 기반, kernel 6.x) |
| 아키텍처 | aarch64 (ARM64) |
| 크기 | 150 × 150 × 51 mm (5.91 × 5.91 × 2.01 inch) |
| 무게 | 1.48 kg |
| 냉각 | ASUS 독자 냉각 시스템 (저소음 팬 + 히트 파이프) |
| 기타 | Kensington 잠금 슬롯 |

> ⚠️ 사양 참고: 초안에는 "150 × 150 × 50 mm"로 기재되었고 무게가 포함되지 않았습니다. 검증 결과 ASUS 공식 techspec은 **150 × 150 × 51 mm / 1.48 kg**이며 이를 수정했습니다. HDMI 버전은 2.1입니다(초안에는 2.1b로 기재되어 수정함). 참고 자료는 섹션 10을 참조하시기 바랍니다.

### 2.2 소프트웨어 환경: NVIDIA DGX OS

| 항목 | 내용 |
|---|---|
| 기본 OS | Ubuntu Linux (NVIDIA 커스터마이징) |
| 커널 | Linux 6.x |
| 아키텍처 | aarch64 (ARM64) |
| 사전 설치 소프트웨어 | NVIDIA AI 소프트웨어 스택 (CUDA, cuDNN, TensorRT, PyTorch, Jupyter 등) |
| 패키지 관리 | apt |

### 2.3 DGX Spark와의 차이점

| 차이 항목 | ASUS GX10 | NVIDIA DGX Spark |
|---|---|---|
| 냉각 설계 | ASUS 독자 냉각 시스템 | NVIDIA 레퍼런스 냉각 |
| 섀시 설계 | ASUS 맞춤형 섀시 | NVIDIA 레퍼런스 섀시 |
| 무선 모듈 | MediaTek AW-EM637 (Wi-Fi 7) | 동급 Wi-Fi 7 모듈 |
| 액세서리 | ASUS 정품 액세서리 | NVIDIA 정품 액세서리 |
| 보증 | ASUS 보증 | NVIDIA 보증 |

ALFA 호환성에 대한 영향: 영향 없을 것으로 예상됩니다(GX10에서만 실측했으며, 다른 GB10 기종은 개별적으로 테스트하지 않았습니다). USB 컨트롤러, 커널 버전, 드라이버 프레임워크는 모두 DGX Spark와 동일합니다.

### 2.4 USB Type-C 변환 요구사항

GX10에는 4개의 USB 포트가 있으며 모두 Type-C입니다:

- 데이터 포트 3개 (DP Alt Mode 지원, 모니터 연결 가능)
- PD 입력 포트 1개 (전원 공급용)

ALFA 전 제품군 랜카드(USB-C인 AXML 제외)는 USB Type-A이므로 변환 어댑터가 필요합니다.

## 3. 현행 ALFA 랜카드 사양 및 칩셋 분석

2026년 9월 기준 ALFA Network의 현행 USB 무선 랜카드 제품군은 다음과 같습니다:

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

## 4. 적용 모델 및 칩셋

### 4.1 권장 등급 분류

| 권장 등급 | 모델 (칩셋) | 설명 |
|---|---|---|
| ⭐ 침투 테스트 최우선 추천 | AWUS036EACS (RTL8821CU) / AWUS036ACH (RTL8812AU) / AWUS036ACS (RTL8811AU) | 내장 드라이버로 설치 불필요. 인젝션 실측: EACS·ACH는 두 대역 모두 100%, ACS는 2.4GHz 100%·5GHz 96%. WPA handshake를 엔드투엔드로 캡처 가능 |
| ✅ 권장 | AWUS036ACM (MT7612U) | 내장 드라이버로 설치 불필요. monitor, 인젝션(2.4GHz 63–83%, 5GHz 76%), AP, WPA3 모두 사용 가능 |
| ✅ 권장 | AWUS036ACHM (MT7610U) | 내장 드라이버로 설치 불필요. 2.4GHz 인젝션 96–100%, 5GHz 인젝션은 브로드캐스트만 가능. WPA3 AP는 sae_pwe=0 설정 필요 |
| ✅ 권장 (Wi-Fi 6) | AWUS036AX / AXER (RTL8832BU) | 내장 드라이버로 설치 불필요. monitor 수신 감도 강함, 인젝션 가능(2.4GHz: AX 96%, AXER 73%), AP 80MHz 지원 |
| ⚠️ 연결 / AP 용도에만 적합 | AWUS036AXML / AXM (MT7921AUN) | 내장 드라이버로 설치 불필요. monitor, AP, WPA3는 사용 가능하지만 stock kernel 6.17에서 인젝션에 실패하므로 침투 테스트에는 부적합. AXML은 USB-C로 직접 연결 가능 |

### 4.2 사용 시나리오별 권장

| 사용 시나리오 | 권장 모델 | 설명 |
|---|---|---|
| 일반 무선 인터넷 (가장 간단) | 9종 모두 가능 (예: AWUS036ACM / ACHM) | 모두 커널 내장 드라이버로, 꽂으면 바로 사용 가능 |
| 무선 침투 테스트 / 모니터링 / 인젝션 | AWUS036EACS / ACH / ACS | 인젝션 실측 96–100%, WPA handshake를 엔드투엔드로 캡처 가능. AXM / AXML은 선택하지 마십시오(인젝션 실패) |
| Wi-Fi 6 + AP 핫스팟 | AWUS036AX / AXER | 2x2, 80MHz AP 실측 동작 |
| 6GHz 대역 | AWUS036AXML | 6GHz에서 WPA3 AP 구성 실측 성공. AXM은 같은 칩이지만 6GHz 미실측 |
| 외장 WiFi 불필요 | — | GX10은 Wi-Fi 7을 내장하고 있어 일반 인터넷 접속에는 외장 WiFi가 필요 없음 |

## 5. 환경 요구사항

### 5.1 하드웨어 요구사항

| 항목 | 요구사항 |
|---|---|
| USB 어댑터 | USB-C to USB-A 어댑터 또는 케이블(AXML 제외), USB 3.2 Gen 2×2 지원 제품 권장 |
| 전원 공급 장치 | ASUS GX10 정품 USB-C 전원 공급 장치 (180W EPR PD3.1) |

### 5.2 소프트웨어 요구사항

| 항목 | 요구사항 |
|---|---|
| DGX OS 버전 | 모든 현행 버전 (kernel 6.x) |
| 커널 버전 | kernel 6.17(실측 6.17.0-1014-nvidia)에는 랜카드 9종의 드라이버가 모두 내장되어 있어 컴파일 도구가 필요 없음. 카드마다 최소 버전이 다르며(ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), 그보다 낮을 때만 커뮤니티 DKMS 드라이버 설치 필요 |
| 무선 관리 도구 | iw, network-manager (DGX OS에 사전 설치됨) |

## 6. 호환성 판정

### ALFA 현행 모델 × ASUS Ascent GX10 (GB10) 호환성 매트릭스

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

판정 기준: 2026-11-16~11-18에 ASUS GX10(Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia)에서 실기 테스트를 진행했으며, 테스트 대상은 자체 보유 Wi-Fi와 자체 보유 휴대폰입니다. 본 문서의 기종이 바로 실측 장비입니다. 전체 데이터는 [ALFA 랜카드 9종 ARM64 실측 종합표](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)를 참조하시기 바랍니다.

## 7. 단계별 상세 설정

ASUS GX10의 설치 단계는 NVIDIA DGX Spark와 동일합니다. 다음은 간략화된 버전이며, 전체 단계는 [ALFA 무선 랜카드는 NVIDIA DGX Spark를 지원합니까](/ko/blog/alfa-nvidia-dgx-spark-compatibility/)의 섹션 7을 참조하시기 바랍니다.

### 7.1 MediaTek 칩 모델 (AWUS036ACM / ACHM / AXM / AXML)

- USB-C to USB-A 어댑터를 사용하여(AXML은 직접 연결 가능) ALFA 랜카드를 GX10의 USB-C 포트에 연결
- 인식 확인: `lsusb`
- 인터페이스 확인: `ip link show` (wlx로 시작하는 인터페이스가 자동으로 나타나야 함)
- WiFi 연결: `nmcli dev wifi connect "SSID" password "password"`

### 7.2 Realtek 칩 모델 (AWUS036ACH / ACS / EACS / AX / AXER)

kernel 6.17(GX10 실측 버전)에는 모든 Realtek 모델의 드라이버가 이미 내장되어 있으므로, 절차는 MediaTek 모델과 같으며 컴파일이 필요 없습니다(최소 버전: EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17):

```bash
# 1. 커널 버전 확인 (6.17 이상이면 모든 Realtek 모델 드라이버 내장, GX10 실측은 6.17.0-1014-nvidia)
uname -r

# 2. 랜카드 연결 후 드라이버가 자동 로드되었는지 확인
lsusb
lsmod | grep -E "rtw88|rtw89"
ip link show

# 3. WiFi 연결
nmcli dev wifi connect "SSID" password "password"
```

모델별 자동 로드 모듈: ACH → `rtw88_8812au`, ACS → `rtw88_8821au`, EACS → `rtw88_8821cu`, AX / AXER → `rtw89_8852bu`. `uname -r`이 해당 카드의 최소 버전보다 낮은 경우(구형 시스템)에만 커뮤니티가 유지보수하는 DKMS 드라이버(예: RTL8812AU용 morrownr/8812au-20210820)를 설치해야 합니다.

### 7.3 모니터 모드 (침투 테스트)

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

## 8. 일반적인 오류 및 문제 해결

| 증상 | 가능한 원인 | 해결 방법 |
|---|---|---|
| lsusb에 ALFA 랜카드가 보이지 않음 | USB-C 어댑터 불량 / 충전 전용 규격 | 데이터 전송을 지원하는 USB 3.2 Gen 2×2 어댑터로 교체, 다른 USB-C 포트 시도 |
| MediaTek 칩에 wlan 인터페이스가 없음 | 모듈이 자동 로드되지 않음 / 펌웨어 누락 | `sudo modprobe mt76x2u`; `sudo apt install linux-firmware`; `dmesg | grep mt76` 확인 |
| Realtek 카드를 연결해도 wlan 인터페이스가 없음 | 커널이 해당 카드의 최소 버전(EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17)보다 낮아 대응 드라이버가 내장되어 있지 않음 | `uname -r`로 버전 확인. 커널을 업그레이드하거나, 구형 커널에서는 커뮤니티 DKMS 드라이버 설치 |
| monitor / AP를 반복 전환한 뒤 어떤 신호도 스캔되지 않음 | RX 정지(RX stall) | 랜카드를 뽑았다 다시 꽂아 USB를 재열거 |
| EACS / AXML을 다시 꽂은 뒤 wlx 인터페이스가 없음 | 블루투스 + Wi-Fi 복합 장치의 probe가 멈춤 | 다른 USB 포트에 다시 연결 |
| WiFi 속도가 느림 | 어댑터가 USB 2.0만 지원 | USB 3.2 Gen 2×2 어댑터로 교체 |
| 내장 Wi-Fi 7과 외장 WiFi 간섭 | 라우팅 충돌 | 외장 WiFi 사용 전 `sudo nmcli radio wifi off`로 내장 WiFi 비활성화 |
| 6GHz를 사용할 수 없음 | 규제 도메인(Regulatory Domain) 제한 | `sudo iw reg set US`; 최신 규정 확인 |

## 9. 알려진 제한 사항

- USB Type-C 변환 필요: AXML을 제외한 모든 ALFA 랜카드는 USB-C to USB-A 변환 어댑터가 필요합니다.
- MT7921 모델의 인젝션 실패: AWUS036AXM / AXML은 stock kernel 6.17에서 패킷 인젝션에 실패하여 deauth나 handshake 캡처를 할 수 없습니다. monitor, AP, WPA3는 사용할 수 있습니다. 주된 원인은 kernel 6.16 이후 mac80211 chanctx 회귀이며, 커뮤니티 패치 드라이버도 여전히 속도 제한이 있습니다.
- 실측 범위: ASUS GX10(kernel 6.17.0-1014-nvidia)에서만 실측했으며, 다른 GB10 기종은 개별적으로 테스트하지 않았습니다.
- hcxdumptool 사용 불가: 2.4 GHz의 EACS를 제외한 모든 카드에서 `failed to arm`이 발생하므로 airodump-ng + aireplay-ng를 사용하십시오.
- 내장 Wi-Fi 7이 외장 장치와 충돌할 수 있음: GX10은 Wi-Fi 7(MediaTek AW-EM637)을 내장하고 있습니다.
- AP 모드는 수동 구성 필요: DGX OS는 기본적으로 개발 환경으로 설정되어 있습니다.
- 6GHz 규제 제한: Wi-Fi 6E 사용 가능 여부는 규제 지역에 따라 다릅니다.
- 구형 커널: kernel이 해당 카드의 최소 버전(EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17)보다 낮은 시스템에서만 Realtek 모델에 커뮤니티 DKMS 드라이버가 필요하며, 커널을 업데이트할 때마다 재컴파일해야 합니다.
- ASUS 하드웨어 차이는 호환성에 영향 없음: 냉각 및 기구 설계의 차이는 USB WiFi 드라이버 호환성에 영향을 주지 않습니다.

반증 조건: 위의 판단은 DGX OS(Ubuntu 기반, kernel 6.x)를 기준으로 합니다. 향후 ASUS가 DGX OS가 아닌 펌웨어(자체 Android 또는 커스터마이징된 시스템 버전 등)를 출시하는 경우 판단을 재검증해야 합니다.

## 10. 참고 URL

| 출처 | 설명 | URL | 검증 상태 | 검증 날짜 |
|---|---|---|---|---|
| ASUS Ascent GX10 공식 Techspec | GX10 하드웨어 사양 (**150×150×51mm / 1.48kg** / USB 구성 / HDMI 2.1) | https://www.asus.com/ph/networking-iot-servers/desktop-ai-supercomputer/ultra-small-ai-supercomputers/asus-ascent-gx10/techspec/ | ✅ 검증됨 | 2026-09-03 |
| ASUS Ascent GX10 공식 스토어 (UK) | GX10 제품 페이지 (150 × 150 × 51mm) | https://uk.store.asus.com/asus-ascent-gx105004-33389.html | ✅ 검증됨 | 2026-09-03 |
| NVIDIA DGX Spark 공식 페이지 | GB10 플랫폼 정보 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ 검증됨 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 드라이버 | https://github.com/morrownr/8812au-20210820 | ✅ 검증됨 | 2026-09-03 |
| ALFA Soft AP WiFi 핫스팟 Linux 가이드 (Yopitek) | ALFA Linux AP 모드 가이드 | /ko/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 검증됨 | 2026-09-03 |
| ALFA Network 제품 개요 (Yopitek) | ALFA 현행 제품 사양 | /ko/products/alfa/ | ✅ 검증됨 | 2026-09-03 |
| ALFA 랜카드 9종 ARM64 실측 종합표 (Yopitek) | ASUS GX10 + Ubuntu 24.04 ARM64 실기 테스트 | https://yupitek.com/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ 실측 | 2026-11-18 |

관련 문서: [ALFA 무선 랜카드는 NVIDIA DGX Spark와 호환됩니까](/ko/blog/alfa-nvidia-dgx-spark-compatibility/) | [ALFA 무선 랜카드는 ALTOS BrainSphere GB10 F1과 호환됩니까](/ko/blog/alfa-altos-brainsphere-gb10-compatibility/) | [ALFA 무선 랜카드는 GIGABYTE AI TOP ATOM과 호환됩니까](/ko/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [ALFA 무선 랜카드는 MSI EdgeXpert와 호환됩니까](/ko/blog/alfa-msi-edgexpert-compatibility/)

면책 조항: 본 문서의 호환성 판정은 2026년 11월 ASUS GX10(Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia)에서의 실기 테스트를 기준으로 합니다. GX10에서 실측한 kernel 6.17에는 ALFA 랜카드 9종의 드라이버가 모두 내장되어 있으며(카드마다 최소 버전이 다름), kernel이 해당 카드의 최소 버전보다 낮을 때만 커뮤니티 DKMS 드라이버가 필요합니다. GX10은 Wi-Fi 7을 내장하고 있으므로, 외장 ALFA는 주로 침투 테스트나 특수 칩셋 요구사항에 사용됩니다. 모니터링과 인젝션은 자신이 소유하거나 승인을 받은 네트워크에서만 수행하십시오.
