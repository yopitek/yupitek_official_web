---
title: "ALFA 무선 어댑터와 Kali NetHunter 완벽 기술 가이드 2026"
description: "Kali NetHunter에서 ALFA USB WiFi 어댑터를 사용하기 위한 기술 레퍼런스. 대만 시장 스마트폰 호환성, 커널 내장 드라이버 vs DKMS 분석, OTG 설정, 검증된 테스트 결과를 다룹니다."
date: 2026-06-09
draft: false
showBreadcrumbs: true
showTableOfContents: true
featureimage: /images/blog/alfa-nethunter-technical-guide-hero.png
tags: ["nethunter", "kali-linux", "alfa-network", "wireless-security", "android", "usb-otg", "monitor-mode", "packet-injection", "mt7610u", "mt7612u", "rtl8812au"]
---

이미 ALFA 어댑터와 NetHunter의 기본 OTG 설정을 마치셨다면, 빠른 버전의 [OTG 설정 가이드](/ko/blog/alfa-adapter-nethunter-android-otg/)에서 핵심 내용을 확인하실 수 있습니다. 본 문서는 더 깊이 들어갑니다 — 하드웨어 구매 전에 스마트폰과 어댑터 호환성을 평가하고, 커널 업데이트 후에도 드라이버가 안정적으로 작동하는 접근 방식을 이해하며, 특정 조합에 커밋하기 전에 검증된 테스트 결과를 확인해야 하는 보안 전문가를 위한 완전한 기술 레퍼런스입니다.

여기서는 대부분의 NetHunter 가이드에서 건너뛰는 질문에 집중합니다: **어떤 어댑터가 진정한 플러그 앤 플레이이고, 어떤 어댑터가 최악의 순간에 드라이버 컴파일 지옥으로 빠뜨리는가?** 답은 칩셋, 스마트폰의 커널 버전, 그리고 드라이버가 커널 트리 안에 내장되어 있는지 외부 DKMS 리포지토리에 존재하는지에 따라 달라집니다. 이 판단을 잘못하면 현장에서 `modprobe` 오류를 바라보며 어댑터를 가방 속에 그대로 두게 됩니다. 제대로 판단하면 꽂자마자 스캔을 시작할 수 있습니다.

---

## 1. 고객 요구사항

### 1.1 활용 사례

모바일 침투 테스터는 노트북을 완전히 대체할 수 있는 설정이 필요합니다. 스마트폰은 Kali NetHunter를 실행하고, ALFA 어댑터는 USB OTG로 연결되며, 작업자는 노트북 없이 Wi-Fi 보안 평가를 수행합니다. 사이트 서베이, 모니터 모드 캡처, 패킷 인젝션, WPA 핸드셰이크 수집이라는 핵심 워크플로우가 배터리 전원으로 안정적으로 작동해야 합니다.

### 1.2 핵심 요구사항

| 요구사항 | 세부 내용 |
|---|---|
| 플랫폼 | Kali NetHunter (full edition, custom kernel)가 설치된 Android 스마트폰 |
| 연결 방식 | USB OTG 케이블 또는 유전원 OTG 허브 |
| 어댑터 | 모니터 모드 및 패킷 인젝션을 지원하는 ALFA USB WiFi 어댑터 |
| 드라이버 접근 방식 | 컴파일 의존성을 없애기 위해 in-kernel (driverless) 칩셋 우선 |
| 대만 시장 | 2024~2026년 모델 중 대만에서 공식 구매 가능한 기기 |
| 전원 | 배터리 구동, 지속 운영 시 유전원 OTG 허브 강력 권장 |

---

## 2. 대상 하드웨어 및 소프트웨어 분석

### 2.1 대만에서 구할 수 있는 NetHunter 호환 스마트폰

NetHunter는 117개 이상의 기기 모듈을 지원하지만, 대부분 구형 모델입니다. (a) 대만에서 공식 구매 가능하고, (b) 2024년 이후 출시되었으며, (c) NetHunter 커스텀 커널이 정상 작동하는 기기로 필터링하면 세 가지 스마트폰이 두드러집니다:

| 모델 | 코드네임 | CPU | 커널 버전 | 빌드 이미지 | 대만 구매 가능 여부 |
|---|---|---|---|---|---|
| **OnePlus 11 5G** | salami | Snapdragon 8 Gen 2 (ARM64) | 2 | 2 | ✅ 병행 수입 채널로 구매 가능, 2023년 출시 |
| **Nothing Phone (1)** | spacewar | Snapdragon 778G+ (ARM64) | 3 | 1 | ✅ 대만 공식 출시, 활발한 커뮤니티 |
| **Samsung Galaxy S20 FE 5G** | r8q | Snapdragon 865 (ARM64) | 5 | 1 | ✅ 대만 판매 — **Snapdragon 변종 필수** |

{{< alert "triangle-exclamation" >}}
**Samsung Exynos 경고:** 대만 통신사를 통해 유통되는 대부분의 Samsung 기기는 Exynos 칩셋을 사용합니다. NetHunter 커널은 Snapdragon 변종(`r8q`)만 지원합니다. NetHunter용 Samsung 기기를 구매하기 전에 CPU 모델을 반드시 확인하십시오 — 제품 설명에 "Exynos"라고 기재되어 있으면 작동하지 않습니다. Snapdragon 유닛을 병행 수입하거나 OnePlus 11을 선택하십시오.
{{< /alert >}}

**NetHunter Rootless**는 루팅 없이 모든 Android 기기에서 실행되지만, 모니터 모드를 위한 외부 USB WiFi 어댑터를 지원할 수 없습니다. 패킷 캡처와 인젝션이 필요하다면 커스텀 커널이 포함된 NetHunter full edition이 필요합니다.

### 2.2 플랫폼 기술 사양

OnePlus 11 5G를 기준 플랫폼으로 사용합니다:

| 파라미터 | 사양 |
|---|---|
| CPU 아키텍처 | ARM64 (aarch64) |
| SoC | Qualcomm Snapdragon 8 Gen 2 (SM8550) |
| USB 컨트롤러 | USB 3.1 Gen 1, OTG 지원 |
| USB 전원 공급 | 5V / 900mA (지속적인 어댑터 운영 시 유전원 OTG 허브 권장) |

### 2.3 소프트웨어 환경

| 구성 요소 | 요구사항 | 권장 버전 |
|---|---|---|
| 호스트 OS | Kali chroot가 포함된 Android | Android 11 이상 |
| NetHunter | Full edition (custom kernel) | 2024.4 (최신 안정 버전) |
| Linux 커널 | 기기별 커스텀 커널 | 5.x 이상 권장 |
| 사전 로드 드라이버 | 섹션 4 매트릭스 참조 | — |
| DKMS | RTL8812AU 기반 어댑터에만 필요 | 커널 헤더 버전 일치 필수 |
| 무선 도구 | aircrack-ng, Kismet, MANA Toolkit | NetHunter chroot 제공 |
| Root | 전체 기능 사용에 필요 | Magisk 26.0 이상 |

---

## 3. ALFA 어댑터 사양 및 드라이버 소스

### 3.1 AWUS036ACHM — NetHunter 최고 추천 제품

| 파라미터 | 사양 |
|---|---|
| 칩셋 | **MediaTek MT7610U** |
| USB VID/PID | `0x0e8d:0x7610` |
| 대역 | 2.4GHz + 5GHz (AC433) |
| 최대 데이터 속도 | 150Mbps (2.4GHz) / 433Mbps (5GHz) |
| USB | USB 2.0 |
| 모니터 모드 | ✅ 완벽 지원 |
| 패킷 인젝션 | ✅ 완벽 지원 |
| 안테나 | 1× 탈착식 고이득 안테나 (RP-SMA) |
| 드라이버 | **In-kernel** — 설치 불필요 |
| 커널 모듈 | `mt76x0u` |
| 커널 요구사항 | Linux 4.19 이상 |
| 제품 페이지 | [/ko/products/alfa/awus036achm/](/ko/products/alfa/awus036achm/) |

MT7610U 칩셋은 `mt76x0u` 드라이버가 Linux 커널 4.19부터 mainline에 포함되어 있어 Kali 및 NetHunter 커뮤니티에서 널리 권장됩니다. 꽂으면 커널이 인식하고 바로 작업을 시작할 수 있습니다. 컴파일 툴체인도, 커널 헤더도, DKMS도 필요하지 않습니다 — `lsusb`로 확인한 후 `airmon-ng start`만 하면 됩니다.

### 3.2 AWUS036ACM — 고성능 대안

| 파라미터 | 사양 |
|---|---|
| 칩셋 | **MediaTek MT7612U** |
| USB VID/PID | `0x0e8d:0x7612` |
| 대역 | 2.4GHz + 5GHz (AC1200) |
| 최대 데이터 속도 | 300Mbps (2.4GHz) / 867Mbps (5GHz) |
| USB | USB 3.0 |
| 모니터 모드 | ✅ 완벽 지원 |
| 패킷 인젝션 | ✅ Kali 2024.3 / 2025.1에서 안정성 확인 |
| 안테나 | 2× 듀얼 안테나 (RP-SMA), MIMO 2T2R |
| 드라이버 | **In-kernel** — 설치 불필요 |
| 커널 모듈 | `mt76x2u` |
| 커널 요구사항 | Linux 4.19 이상 |
| 제품 페이지 | [/ko/products/alfa/awus036acm/](/ko/products/alfa/awus036acm/) |

ACM은 MIMO 2T2R 및 USB 3.0 대역폭을 갖춘 AC1200 듀얼 밴드를 추가합니다. `mt76x2u` 드라이버 역시 커널 4.19부터 mainline에 포함되어 있습니다. 단, 일부 구형 NetHunter 커스텀 커널(대표적으로 OnePlus 7T의 4.14 커널)에서는 `mt76x2u` 모듈을 포함하지 않고 빌드된 경우가 있습니다. 커널 4.19 이상에서는 문제가 되지 않지만, 구형 커널 빌드를 사용하는 기기라면 `lsmod | grep mt76x2u`로 확인하십시오.

### 3.3 AWUS036ACH — 가장 폭넓은 커뮤니티 지원

| 파라미터 | 사양 |
|---|---|
| 칩셋 | **Realtek RTL8812AU** |
| USB VID/PID | `0x0bda:0x8812` |
| 대역 | 2.4GHz + 5GHz (AC1200) |
| 최대 데이터 속도 | 300Mbps (2.4GHz) / 867Mbps (5GHz) |
| USB | USB 3.0 |
| 모니터 모드 | ✅ 완벽 지원 |
| 패킷 인젝션 | ✅ 완벽 지원 |
| 안테나 | 2× 5dBi 외장 안테나 (RP-SMA) |
| 드라이버 | 외부 DKMS (대부분의 NetHunter 커널에 사전 컴파일됨) |
| 커널 모듈 | `88XXau` |
| 드라이버 리포지토리 | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| 제품 페이지 | [/ko/products/alfa/awus036ach/](/ko/products/alfa/awus036ach/) |

ACH는 수년간 Kali 및 NetHunter 환경의 사실상 표준으로 자리 잡았습니다. 대부분의 NetHunter 커스텀 커널에는 `88XXau` 모듈이 사전 컴파일되어 포함되어 있으므로, 일반적으로 소스에서 빌드할 필요가 없습니다. 하지만 커널 버전에 포함되어 있지 않다면, 일치하는 커널 헤더가 포함된 컴파일 환경이 필요합니다 — 바로 MT7610U와 MT7612U 칩셋이 피할 수 있는 의존성 체인입니다. 듀얼 5dBi 안테나는 제품군 중 가장 강력한 신호 도달 범위를 제공하며, 이는 장거리 캡처 시나리오에서 중요한 장점입니다.

### 3.4 AWUS036ACS — 컴팩트 폼 팩터

| 파라미터 | 사양 |
|---|---|
| 칩셋 | Realtek RTL8811AU |
| USB VID/PID | `0x0bda:0x0811` |
| 대역 | 2.4GHz + 5GHz (AC433) |
| USB | USB 2.0 |
| 모니터 모드 | ✅ 지원 (RTL8812AU와 동일한 드라이버 계열) |
| 패킷 인젝션 | ✅ 지원 |
| 안테나 | 내장형, 55mm 초슬림 바디 |
| 소비 전력 | 약 300mW — 제품군 중 최저 |
| 드라이버 | 외부 (RTL8812AU와 aircrack-ng 리포지토리 공유) |
| 제품 페이지 | [/ko/products/alfa/awus036acs/](/ko/products/alfa/awus036acs/) |

ACS는 가장 휴대성이 뛰어난 옵션입니다. 300mW 전력 소비로 스마트폰 배터리에 가장 부담이 적으며, 슬림한 폼 팩터로 주머니 속에 부담 없이 들어갑니다. 트레이드 오프는 싱글 스트림 AC433 성능과 RTL8812AU 제품군과 공유되는 외부 DKMS 드라이버 의존성입니다.

### 3.5 NetHunter에 권장하지 않는 어댑터

| 어댑터 | 칩셋 | 사유 |
|---|---|---|
| AWUS036AX / AWUS036AXER | RTL8832BU | 커널 6.14 이상 필요, Android 커널에서 모니터 모드 안정성 미검증 |
| AWUS036AXML / AWUS036AXM | MT7921AUN | WiFi 6E / 6GHz 지원이 현재 NetHunter 커널 빌드에서 불안정, 주력 펜테스트 어댑터로 부적합 |

### 3.6 드라이버 소스 리포지토리

| 칩셋 | 드라이버 | 소스 |
|---|---|---|
| MT7610U | `mt76x0u` (in-kernel) | [torvalds/linux — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| MT7612U | `mt76x2u` (in-kernel) | 위와 동일한 커널 트리 |
| RTL8812AU | `88XXau` (외부) | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| RTL8811AU | `88XXau` (외부, 공유) | 동일한 aircrack-ng 리포지토리 |

---

## 4. 드라이버 호환성 분석

### 4.1 In-Kernel vs 외부 DKMS

NetHunter용 어댑터를 선택할 때 가장 중요한 판단 기준은 드라이버가 커널 트리 내부에 있는지 외부에 있는지입니다. 그 이유는 다음과 같습니다:

|  | In-Kernel (MT7610U, MT7612U) | 외부 DKMS (RTL8812AU, RTL8811AU) |
|---|---|---|
| 플러그 앤 플레이 | ✅ 예 — 삽입 시 즉시 인식 | ⚠️ 커널에 `88XXau` 사전 컴파일 여부에 의존 |
| 커널 업데이트 후 유지 | ✅ 예 — 드라이버는 커널 빌드의 일부 | ❌ 커널 업데이트 후 손상 가능, 재컴파일 필요 |
| linux-headers 필요 | ❌ 불필요 | ✅ 수동 컴파일 시 필요 |
| DKMS 필요 | ❌ 불필요 | ✅ 커널에 사전 컴파일되지 않은 경우 필요 |
| 커뮤니티 문서 | 보통 | 풍부 (ACH가 가장 많은 튜토리얼 보유) |
| 현장 실패 위험 | 낮음 | 중간 (컴파일 의존성) |

**결론:** 현장에서 드라이버 문제 발생 가능성을 최소화하려면 MT7610U 또는 MT7612U 어댑터를 선택하십시오. 드라이버가 이미 커널에 내장되어 있어 컴파일할 것도, 업데이트로 인해 손상될 것도, 현장에서 문제를 해결할 것도 없습니다.

### 4.2 NetHunter 커널 모듈 지원 매트릭스

| 기기 | NetHunter 커널 | MT7610U (`mt76x0u`) | MT7612U (`mt76x2u`) | RTL8812AU (`88XXau`) |
|---|---|---|---|---|
| OnePlus 11 5G | Android 13 커널 | ✅ 지원 | ✅ 지원 | ✅ 지원 |
| Samsung S20 FE (Snapdragon) | Android 12 커널 (4.19) | ✅ 지원 | ✅ 지원 | ✅ 지원 (XDA 보고서 확인 필요) |
| Nothing Phone (1) | Android 12/13 커널 | ✅ 지원 | 커널 설정 확인 필요 | ✅ 지원 |
| OnePlus 7/7T | 4.14 (구형) | ✅ 지원 | ⚠️ 빌드에서 누락되었을 수 있음 | ✅ 지원 |

출처: NetHunter GitLab, XDA Forums 커뮤니티 보고서 (2024~2026).

### 4.3 알려진 이슈

**이슈 1: 구형 커널에서 MT7612U 인터페이스가 표시되지 않음**

증상: `lsusb`에는 `0e8d:7612`가 표시되지만 `ip link`에는 `wlan1`이 표시되지 않습니다.  
근본 원인: 커스텀 커널이 `mt76x2u` 모듈 없이 컴파일되었습니다. 일부 4.14 기반 NetHunter 커널(OnePlus 7T 시기)에서 발생합니다.  
해결책: 해당 모듈이 포함된 커널 빌드를 사용하거나, 구형 커널에서 더 널리 지원되는 AWUS036ACHM (MT7610U)으로 전환하십시오.

**이슈 2: USB 전원 부족으로 어댑터 연결 해제**

증상: 스캔 중 어댑터가 사라지고 `dmesg`에 USB 리셋 오류가 기록됩니다.  
근본 원인: 스마트폰 USB 포트가 어댑터의 전류 소비를 지속적으로 감당하지 못합니다. 특히 USB 3.0 어댑터(ACH는 약 500mW 소비)에서 두드러집니다.  
해결책: 벽면 어댑터에서 어댑터로 5V 전원을 공급하면서 데이터를 스마트폰에 전달하는 유전원 OTG 허브를 사용하십시오.

**이슈 3: chroot 시작 전 어댑터 연결**

증상: Android에 USB 권한 대화상자가 표시되지만, Kali 도구에서 어댑터에 접근할 수 없습니다.  
근본 원인: NetHunter chroot 환경이 실행된 후에 USB 기기가 노출되어야 합니다.  
해결책: chroot를 먼저 시작하고 (Kali Services → Start), 그 후 어댑터를 연결하여 USB 권한을 허용하십시오.

---

## 5. 설정 가이드

### 5.1 사전 준비 사항

하드웨어를 연결하기 전에 다음을 확인하십시오:

```bash
# 기기 루팅 확인
su -c "id"

# NetHunter chroot 버전 확인
cat /kali/etc/os-release
# Kali Linux with NetHunter로 표시되어야 함

# USB OTG 활성화 확인
# 설정 → 개발자 옵션 → OTG (Android 버전에 따라 경로 상이)
```

### 5.2 하드웨어 연결 순서

순서가 중요합니다:

1. **NetHunter 앱** 실행 → **Kali Services** 진입 → **Start**를 탭하여 chroot 구동
2. **유전원 OTG 허브**를 스마트폰 USB 포트에 연결
3. **ALFA 어댑터**를 OTG 허브에 연결
4. Android USB 권한 대화상자가 나타나면 **OK**를 탭하고 **항상 허용** 체크

{{< alert "circle-info" >}}
지속적인 운영을 위해 유전원 OTG 허브를 강력히 권장합니다. AWUS036ACH는 약 500mW의 전력을 소비하므로, 스마트폰 배터리로 직접 구동하면 배터리 소모가 크게 가속화되고 USB 불안정성을 유발할 수 있습니다. 벽면 어댑터에서 전원을 공급받으면서 데이터를 통과시키는 허브는 두 가지 문제를 모두 해결합니다.
{{< /alert >}}

### 5.3 어댑터 감지 확인

```bash
# USB 기기 목록 확인 — 어댑터가 나타나는지 확인
lsusb

# 모델별 예상 출력:
# AWUS036ACHM: Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.
# AWUS036ACM:  Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U
# AWUS036ACH:  Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp.
```

어댑터가 나타나지 않으면 다른 OTG 케이블로 시도하거나, 개발자 옵션에서 OTG가 활성화되어 있는지 확인하거나, 컴퓨터에 연결하여 어댑터가 정상 작동하는지 테스트하십시오.

### 5.4 드라이버 로드

**MT7610U (AWUS036ACHM) — 대부분의 커널에서 자동 로드:**

```bash
# 자동 로드 확인
lsmod | grep mt76

# 필요 시 수동 로드 (드문 경우)
sudo modprobe mt76x0u
```

**MT7612U (AWUS036ACM) — 커널 4.19 이상에서 자동 로드:**

```bash
# 확인
lsmod | grep mt76

# 필요 시 수동 로드
sudo modprobe mt76x2u
```

**RTL8812AU (AWUS036ACH) — 대부분의 NetHunter 커널에 사전 컴파일됨:**

```bash
# 사전 컴파일된 모듈 로드
sudo modprobe 88XXau

# 로드 확인
lsmod | grep 88XX
```

### 5.5 네트워크 인터페이스 확인

```bash
# 무선 인터페이스 목록
ip link show | grep wlan

# 또는 iw 사용
iw dev

# 외부 어댑터는 일반적으로 wlan1로 표시됨
# (wlan0은 보통 스마트폰 내장 WiFi)
```

### 5.6 모니터 모드 활성화

```bash
# 방해 프로세스 종료
sudo airmon-ng check kill

# 어댑터에서 모니터 모드 시작
sudo airmon-ng start wlan1

# 모니터 모드 활성화 확인
iwconfig wlan1mon
# 예상 출력: Mode:Monitor

# 주변 네트워크 스캔 (승인된 테스트만 수행)
sudo airodump-ng wlan1mon

# 전체 대역 스캔 (2.4GHz + 5GHz)
sudo airodump-ng --band abg wlan1mon
```

### 5.7 Managed Mode로 복귀

```bash
sudo airmon-ng stop wlan1mon
sudo service NetworkManager restart
```

---

## 6. 애플리케이션 구성도

<img src="/images/blog/nethunter-topology.png" alt="NetHunter + ALFA Application Topology Diagram" loading="eager" style="max-width:100%;height:auto;display:block">

---

## 7. 검증 결과

### 7.1 테스트 매트릭스

다음 조합은 커뮤니티 테스트와 벤더 문서를 통해 검증되었습니다:

| 스마트폰 | ALFA 어댑터 | 칩셋 | 모니터 모드 | 패킷 인젝션 | 상태 |
|---|---|---|---|---|---|
| OnePlus 11 5G | AWUS036ACHM | MT7610U | ✅ | ✅ | 검증 완료 |
| OnePlus 11 5G | AWUS036ACM | MT7612U | ✅ | ✅ | 검증 완료 |
| OnePlus 11 5G | AWUS036ACH | RTL8812AU | ✅ | ✅ | 검증 완료 |
| Samsung S20 FE (Snapdragon) | AWUS036ACH | RTL8812AU | ✅ | ⚠️ | 커뮤니티 보고 — 커널 설정 확인 필요 |
| Samsung S20 FE (Snapdragon) | AWUS036ACHM | MT7610U | ✅ | ✅ | 커뮤니티 보고 |
| Nothing Phone (1) | AWUS036ACHM | MT7610U | ✅ | ✅ | 커뮤니티 보고 |

출처: XDA Forums, Reddit r/NetHunter, Kali NetHunter GitLab Issues (2024~2026).

### 7.2 예상 `lsusb` 출력

```
# AWUS036ACHM
Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.

# AWUS036ACM
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter

# AWUS036ACH
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
```

### 7.3 모니터 모드 확인

```bash
# 성공 시 예상 iwconfig 출력
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.437 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

---

## 8. 권장 사항

### 8.1 최고 추천: OnePlus 11 5G + AWUS036ACHM

이 조합은 테스트된 설정 중 가장 낮은 마찰을 제공합니다. OnePlus 11은 대만 시장에서 여전히 구할 수 있는 NetHunter 공식 커널 지원이 포함된 가장 최신 플래그십입니다. AWUS036ACHM의 MT7610U 칩셋은 `mt76x0u` 드라이버를 사용하며, 4.19 이후 mainline 커널에 포함되어 있어 컴파일이 전혀 필요하지 않습니다. 국제 보안 커뮤니티(Lab401, morrownr USB-WiFi 데이터베이스)에서도 Kali 및 NetHunter에 가장 안전한 선택으로 일관되게 평가하고 있습니다. 어댑터는 컴팩트하고 단일 안테나이며 USB 2.0으로 구동되어 모바일 시나리오에서 장점으로 작용합니다 — 낮은 전력 소비, 낮은 발열, 적은 장애 요소.

### 8.2 성능 추천: OnePlus 11 5G + AWUS036ACM

장거리 5GHz 캡처를 위해 MIMO 2T2R이 탑재된 AC1200 듀얼 밴드 성능이 필요하다면, ACM은 in-kernel 드라이버 생태계를 벗어나지 않고 이를 제공합니다. MT7612U의 `mt76x2u` 드라이버 역시 4.19 이후 mainline입니다. 트레이드 오프: USB 3.0은 더 많은 전력을 소비하고 듀얼 안테나 바디는 더 큽니다. OnePlus 11에서 `mt76x2u` 포함은 확인되었습니다.

### 8.3 커뮤니티 인기: 모든 NetHunter 기기 + AWUS036ACH

ACH는 NetHunter 생태계에서 가장 많은 튜토리얼, 가장 큰 커뮤니티 문제 해결 기반, 최고의 서드파티 문서를 보유한 어댑터입니다. 듀얼 5dBi 안테나는 ALFA 제품군 중 가장 강력한 신호 도달 범위를 제공합니다. 대부분의 NetHunter 커널에는 `88XXau` 모듈이 사전 컴파일되어 있어 컴파일이 거의 필요하지 않습니다. 플러그 앤 플레이의 단순함보다 커뮤니티 지원과 장거리 캡처를 우선시한다면 이것이 선택입니다.

### 8.4 시나리오별 선택

| 시나리오 | 권장 조합 | 근거 |
|---|---|---|
| 첫 NetHunter 설정, 리스크 최소화 | OnePlus 11 + AWUS036ACHM | In-kernel 드라이버, 컴파일 불필요, 가장 작은 폼 팩터 |
| 장거리 듀얼 밴드 캡처 | OnePlus 11 + AWUS036ACM | AC1200 + MIMO, 여전히 in-kernel |
| 장거리 서베이, 최대 튜토리얼 | 모든 지원 기기 + AWUS036ACH | 가장 강력한 안테나, 가장 넓은 커뮤니티 지원 |
| 초경량, 최저 전력 | 모든 지원 기기 + AWUS036ACS | 300mW 소비, 모든 주머니에 적합 |

### 8.5 지원 리소스

| 리소스 | 링크 |
|---|---|
| Yupitek — 대만 ALFA 공식 유통사 | [yupitek.com](https://www.yupitek.com) |
| ALFA Network 공식 제품 페이지 | [alfa.com.tw](https://www.alfa.com.tw) |
| MT7610U 드라이버 (커널 트리) | [torvalds/linux — mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| RTL8812AU 드라이버 (aircrack-ng) | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| NetHunter 지원 기기 | [nethunter.kali.org/device-kernels.html](https://nethunter.kali.org/device-kernels.html) |
| NetHunter 공식 문서 | [kali.org/docs/nethunter/](https://www.kali.org/docs/nethunter/) |
| XDA NetHunter 포럼 | [xdaforums.com/tags/nethunter/](https://xdaforums.com/tags/nethunter/) |
| Yupitek ALFA 제품 카탈로그 | [/ko/products/alfa/](/ko/products/alfa/) |

---

## 부록: 빠른 문제 해결

**어댑터가 `lsusb`에 표시되지 않음:**
1. 개발자 옵션에서 OTG가 활성화되어 있는지 확인
2. 다른 OTG 케이블로 시도 — 케이블 품질이 가장 흔한 실패 원인
3. 유전원 OTG 허브 사용
4. NetHunter chroot가 시작되었는지 확인

**`lsusb`에는 표시되나 `wlan1` 인터페이스가 없음:**

```bash
# 커널 메시지에서 드라이버 오류 확인
dmesg | tail -30 | grep -E "usb|mt76|rtl|88XX"

# 커널 모듈 존재 여부 확인
find /lib/modules -name "mt76*" 2>/dev/null
find /lib/modules -name "*88XX*" 2>/dev/null

# 수동 로드 시도
sudo modprobe mt76x0u   # MT7610U
sudo modprobe mt76x2u   # MT7612U
sudo modprobe 88XXau    # RTL8812AU
```

**모니터 모드가 시작되나 네트워크가 표시되지 않음:**

```bash
# 방해 프로세스 먼저 종료
sudo airmon-ng check kill

# 전체 대역 재스캔
sudo airodump-ng --band abg wlan1mon

# 채널 설정 확인
sudo iw dev wlan1mon info
```

**사용 중 어댑터 연결 해제 (USB 리셋):**

```bash
# 임시 해결 — 송신 전력 감소
sudo iw dev wlan1 set txpower fixed 1000  # 10 dBm

# 영구 해결 — 유전원 OTG 허브 사용
```

---

## 관련 가이드

- [ALFA 어댑터 및 NetHunter 기본 OTG 설정](/ko/blog/alfa-adapter-nethunter-android-otg/)
- [ALFA WiFi 어댑터 구매 가이드 2026](/ko/blog/alfa-wifi-adapter-buyer-guide-2026/)
- [Kali Linux 및 Ubuntu에 ALFA 드라이버 설치](/ko/blog/install-alfa-driver-kali-ubuntu/)
- [Raspberry Pi 및 Kali에서 ALFA 어댑터 사용하기](/ko/blog/alfa-adapter-raspberry-pi-kali/)

---

*본 문서는 **Yupitek Ltd** — ALFA Network 대만 공식 유통사가 작성하였습니다.*  
*데이터 기준일: 2026-06-09. Linux 커널 및 NetHunter 버전은 정기적으로 업데이트되므로, 최신 호환성 정보는 공식 소스에서 확인하십시오.*
