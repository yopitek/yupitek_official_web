---
title: "Kali NetHunter에서 ALFA 무선 어댑터 사용하기: 완벽 기술 가이드 2026"
description: "Kali NetHunter에서 ALFA WiFi 어댑터를 사용하는 방법. 대만 출시 휴대폰 모델, 커널 내장 드라이버 vs DKMS 드라이버, OTG 설정 가이드, 검증된 호환성 결과를 다룹니다."
date: 2026-06-09
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "Kali NetHunter에서 ALFA 어댑터를 사용하려면 어떤 휴대폰 요구사항이 필요합니까?"
    answer: "OTG를 지원하는 Android 휴대폰이 필요하며, 루팅되어 있고 Kali NetHunter 커널이 플래싱되어 있어야 합니다. 검증된 모델에는 Google Pixel 시리즈와 구형 OnePlus 플래그십이 포함됩니다. 호환성은 커널 버전과 칩셋 드라이버 지원에 따라 달라집니다."
  - question: "MT7610U/MT7612U와 RTL8812AU 드라이버의 차이점은 무엇입니까?"
    answer: "MT7610U/MT7612U 드라이버는 커널 트리에 포함되어 있어 컴파일 없이 연결 시 바로 작동합니다. RTL8812AU는 DKMS 외부 드라이버 컴파일이 필요하며 커널 업데이트 후 재빌드가 필요할 수 있습니다. 트리 내장 드라이버는 현장 사용에 더 안정적입니다."
  - question: "ALFA 어댑터가 NetHunter에서 모니터 모드를 지원합니까?"
    answer: "네, MT7610U/MT7612U는 모니터 모드와 패킷 인젝션을 지원합니다. RTL8812AU도 커널 6.12 미만에서 작동하지만 6.12 이상에서는 모니터 모드가 제한적입니다. 보안 연구용으로는 MT7610U/MT7612U 어댑터를 권장합니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
featureimage: /images/blog/alfa-nethunter-technical-guide-hero.png
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
tags: ["nethunter", "kali-linux", "alfa-network", "wireless-security", "android", "usb-otg", "monitor-mode", "packet-injection", "mt7610u", "mt7612u", "rtl8812au"]
---

기본 OTG 지침을 사용하여 이미 NetHunter에서 ALFA 어댑터를 설정했고 빠른 시작 버전을 원한다면, [OTG 설정 가이드](/ko/blog/alfa-adapter-nethunter-android-otg/)에서 핵심 사항을 다룹니다. 본 문서는 더 깊이 들어갑니다. 하드웨어를 구매하기 전에 휴대폰과 어댑터 호환성을 평가하고, 커널 업데이트에도 계속 작동하는 드라이버 방식을 이해하며, 특정 조합을 선택하기 전에 검증된 테스트 결과를 확인해야 하는 보안 전문가를 위한 완전한 기술 레퍼런스입니다.

{{< tldr >}}
MT7610U/MT7612U 커널 네이티브 드라이버는 플러그 앤 플레이인 반면, RTL8812U는 DKMS 컴파일이 필요합니다. NetHunter 휴대폰은 루트와 OTG 지원이 필요합니다. 드라이버 문제를 피하려면 MT7612U 어댑터를 우선 선택하시기 바랍니다.
{{< /tldr >}}




우리는 대부분의 NetHunter 가이드가 건너뛰는 질문에 집중합니다: **어떤 어댑터가 진정한 플러그 앤 플레이이며, 어떤 어댑터가 최악의 순간에 드라이버 컴파일의 늪으로 빠뜨리는가?** 그 답은 칩셋, 휴대폰의 커널 버전, 그리고 드라이버가 커널 트리 내부에 포함되어 있는지 외부 DKMS 저장소에 있는지에 따라 달라집니다. 이를 잘못 선택하면 현장에서 `modprobe` 오류를 바라보는 동안 어댑터는 가방 속에 머물게 됩니다. 제대로 선택하면 연결하자마자 스캔을 시작할 수 있습니다.

---

## 1. 고객 요구사항

### 1.1 사용 사례

모바일 침투 테스터는 노트북을 완전히 대체하는 설정이 필요합니다. 휴대폰은 Kali NetHunter를 실행하고, ALFA 어댑터는 USB OTG를 통해 연결되며, 운영자는 노트북을 들고 다니지 않고 Wi-Fi 보안 평가를 수행합니다. 핵심 워크플로인 사이트 서베이, 모니터 모드 캡처, 패킷 인젝션, WPA 핸드셰이크 수집은 배터리 전원으로 안정적으로 작동해야 합니다.

### 1.2 핵심 요구사항

| 요구사항 | 세부 내용 |
|---|---|
| 플랫폼 | Kali NetHunter(전체 에디션, 커스텀 커널)가 적용된 Android 휴대폰 |
| 연결 | USB OTG 케이블 또는 전원 공급형 OTG 허브 |
| 어댑터 | 모니터 모드 및 패킷 인젝션을 지원하는 ALFA USB WiFi 어댑터 |
| 드라이버 방식 | 컴파일 의존성을 제거하기 위해 커널 내장(드라이버리스) 칩셋 우선 |
| 대만 시장 | 대만에서 공식 판매되는 2024~2026년 모델 |
| 전원 | 배터리 구동, 지속 사용 시 전원 공급형 OTG 허브 강력히 권장 |

---

## 2. 대상 하드웨어 및 소프트웨어 분석

### 2.1 대만에서 구할 수 있는 NetHunter 호환 휴대폰

NetHunter는 117개 이상의 기기 모듈을 지원하지만 대부분은 구형 모델입니다. (a) 대만에서 공식 판매되고, (b) 2024년 이후이며, (c) 작동하는 NetHunter 커스텀 커널이 있는 기기로 필터링한 결과 세 가지 휴대폰이 돋보입니다:

| 모델 | 코드명 | CPU | 커널 버전 | 사전 빌드 이미지 | 대만 판매 여부 |
|---|---|---|---|---|---|
| **OnePlus 11 5G** | salami | Snapdragon 8 Gen 2 (ARM64) | 2 | 2 | ✅ 수입 채널을 통해 구할 수 있음, 2023년 출시 |
| **Nothing Phone (1)** | spacewar | Snapdragon 778G+ (ARM64) | 3 | 1 | ✅ 대만 공식 출시, 활발한 커뮤니티 |
| **Samsung Galaxy S20 FE 5G** | r8q | Snapdragon 865 (ARM64) | 5 | 1 | ✅ 대만 판매 — **Snapdragon 버전 필요** |

{{< alert "triangle-exclamation" >}}
**Samsung Exynos 경고:** 대만 통신사를 통해 판매되는 대부분의 Samsung 기기는 Exynos 칩셋을 사용합니다. NetHunter 커널은 Snapdragon 버전(`r8q`)만 지원합니다. NetHunter용 Samsung 기기를 구매하기 전에 CPU 모델을 확인하시기 바랍니다. 상품 설명에 "Exynos"라고 되어 있다면 작동하지 않습니다. Snapdragon 제품을 수입하거나 대신 OnePlus 11을 선택하시기 바랍니다.
{{< /alert >}}

**NetHunter Rootless**는 루트 없이 모든 Android 기기에서 실행되지만, 모니터 모드를 위한 외부 USB WiFi 어댑터를 지원할 수 없습니다. 패킷 캡처와 인젝션이 필요하다면 커스텀 커널이 적용된 전체 NetHunter 에디션이 필요합니다.

### 2.2 플랫폼 기술 사양

OnePlus 11 5G를 기준 플랫폼으로 사용:

| 매개변수 | 사양 |
|---|---|
| CPU 아키텍처 | ARM64 (aarch64) |
| SoC | Qualcomm Snapdragon 8 Gen 2 (SM8550) |
| USB 컨트롤러 | OTG를 지원하는 USB 3.1 Gen 1 |
| USB 전원 전달 | 5V / 900mA (지속적인 어댑터 작동 시 전원 공급형 OTG 허브 사용) |

### 2.3 소프트웨어 환경

| 구성 요소 | 요구사항 | 권장 버전 |
|---|---|---|
| 호스트 OS | Kali chroot가 적용된 Android | Android 11+ |
| NetHunter | 전체 에디션(커스텀 커널) | 2024.4 (최신 안정 버전) |
| Linux 커널 | 기기별 커스텀 커널 | 5.x 이상 권장 |
| 사전 로드 드라이버 | 섹션 4의 매트릭스 참조 | — |
| DKMS | RTL8812AU 기반 어댑터에만 필요 | 커널 헤더가 일치해야 함 |
| 무선 도구 | aircrack-ng, Kismet, MANA Toolkit | NetHunter chroot 제공 |
| 루트 | 전체 기능에 필요 | Magisk 26.0+ |

---

## 3. ALFA 어댑터 사양 및 드라이버 출처

### 3.1 AWUS036ACHM — NetHunter 최고 추천

| 매개변수 | 사양 |
|---|---|
| 칩셋 | **MediaTek MT7610U** |
| USB VID/PID | `0x0e8d:0x7610` |
| 대역 | 2.4 GHz + 5 GHz (AC600) |
| 최대 데이터 속도 | 150 Mbps (2.4 GHz) / 433 Mbps (5 GHz) |
| USB | USB 2.0 |
| 모니터 모드 | ✅ 완전 지원 |
| 패킷 인젝션 | ✅ 완전 지원 |
| 안테나 | 1× 분리형 고이득(RP-SMA) |
| 드라이버 | **커널 내장** — 설치 불필요 |
| 커널 모듈 | `mt76x0u` |
| 커널 요구사항 | Linux 4.19+ |
| 제품 페이지 | [/ko/products/alfa/awus036achm/](/ko/products/alfa/awus036achm/) |

MT7610U 칩셋은 Kali 및 NetHunter 커뮤니티에서 널리 권장됩니다. 그 `mt76x0u` 드라이버가 버전 4.19부터 메인라인 Linux 커널에 포함되어 있기 때문입니다. 연결하면 커널이 인식하고 바로 작업을 시작할 수 있습니다. 컴파일 도구 체인도, 커널 헤더도, DKMS도 필요 없습니다. `lsusb` 확인 후 바로 `airmon-ng start`를 실행하면 됩니다.

### 3.2 AWUS036ACM — 고성능 대안

| 매개변수 | 사양 |
|---|---|
| 칩셋 | **MediaTek MT7612U** |
| USB VID/PID | `0x0e8d:0x7612` |
| 대역 | 2.4 GHz + 5 GHz (AC1200) |
| 최대 데이터 속도 | 300 Mbps (2.4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| 모니터 모드 | ✅ 완전 지원 |
| 패킷 인젝션 | ✅ Kali 2024.3 / 2025.1에서 안정 확인 |
| 안테나 | 2× 듀얼 안테나(RP-SMA), MIMO 2T2R |
| 드라이버 | **커널 내장** — 설치 불필요 |
| 커널 모듈 | `mt76x2u` |
| 커널 요구사항 | Linux 4.19+ |
| 제품 페이지 | [/ko/products/alfa/awus036acm/](/ko/products/alfa/awus036acm/) |

ACM은 MIMO 2T2R와 USB 3.0 처리량을 갖춘 AC1200 듀얼 밴드를 추가합니다. `mt76x2u` 드라이버 역시 커널 4.19부터 메인라인에 포함되어 있습니다. 한 가지 주의점: 일부 구형 NetHunter 커스텀 커널(특히 버전 4.14의 OnePlus 7T 커널)은 `mt76x2u` 모듈 없이 컴파일되었습니다. 커널 4.19 이상에서는 문제가 되지 않지만, 기기가 구형 커널 빌드를 실행하는 경우 `lsmod | grep mt76x2u`로 확인하시기 바랍니다.

### 3.3 AWUS036ACH — 가장 폭넓은 커뮤니티 지원

| 매개변수 | 사양 |
|---|---|
| 칩셋 | **Realtek RTL8812AU** |
| USB VID/PID | `0x0bda:0x8812` |
| 대역 | 2.4 GHz + 5 GHz (AC1200) |
| 최대 데이터 속도 | 300 Mbps (2.4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| 모니터 모드 | ✅ 완전 지원 |
| 패킷 인젝션 | ✅ 완전 지원 |
| 안테나 | 2× 5dBi 외장형(RP-SMA) |
| 드라이버 | 외부 DKMS(대부분의 NetHunter 커널에 사전 컴파일됨) |
| 커널 모듈 | `88XXau` |
| 드라이버 저장소 | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| 제품 페이지 | [/ko/products/alfa/awus036ach/](/ko/products/alfa/awus036ach/) |

ACH는 수년간 Kali 및 NetHunter 설정의 사실상 표준이었습니다. 대부분의 NetHunter 커스텀 커널은 `88XXau` 모듈을 사전 컴파일된 상태로 제공하므로 일반적으로 소스에서 빌드할 필요가 없습니다. 그러나 커널 버전에 포함되어 있지 않다면 일치하는 커널 헤더가 있는 작동 가능한 컴파일 환경이 필요합니다. 이것이 바로 MT7610U 및 MT7612U 칩셋이 피하는 의존성 체인입니다. 듀얼 5dBi 안테나는 제품군 중 가장 강력한 신호 도달 범위를 제공하며, 이는 장거리 캡처 시나리오에서 중요합니다.

### 3.4 AWUS036ACS — 컴팩트 폼 팩터

| 매개변수 | 사양 |
|---|---|
| 칩셋 | Realtek RTL8811AU |
| USB VID/PID | `0x0bda:0x0811` |
| 대역 | 2.4 GHz + 5 GHz (AC600) |
| USB | USB 2.0 |
| 모니터 모드 | ✅ 지원(RTL8812AU와 동일한 드라이버 제품군) |
| 패킷 인젝션 | ✅ 지원 |
| 안테나 | 내장형, 55 mm 초슬림 본체 |
| 전력 소비 | ~300mW — 제품군 중 최저 |
| 드라이버 | 외부(RTL8812AU와 aircrack-ng 저장소 공유) |
| 제품 페이지 | [/ko/products/alfa/awus036acs/](/ko/products/alfa/awus036acs/) |

ACS는 가장 휴대성이 좋은 옵션입니다. 300mW의 전력 소비로 휴대폰 배터리에 부담이 가장 적으며, 슬림한 폼 팩터는 주머니에 쏙 들어갑니다. 절충점은 단일 스트림 AC600 성능과 RTL8812AU 제품군과 공유하는 외부 DKMS 드라이버 의존성입니다.

### 3.5 NetHunter에 권장하지 않는 어댑터

| 어댑터 | 칩셋 | 이유 |
|---|---|---|
| AWUS036AX / AWUS036AXER | RTL8832BU | 커널 6.17+ 필요, Android 커널에서 모니터 모드 안정성 미검증 |
| AWUS036AXML / AWUS036AXM | MT7921AUN | 현재 NetHunter 커널 빌드에서 WiFi 6E / 6 GHz 지원 불안정, 주력 침투 테스트 어댑터로 부적합 |

### 3.6 드라이버 출처 저장소

| 칩셋 | 드라이버 | 출처 |
|---|---|---|
| MT7610U | `mt76x0u`(커널 내장) | [torvalds/linux — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| MT7612U | `mt76x2u`(커널 내장) | 위와 동일한 커널 트리 |
| RTL8812AU | `88XXau`(외부) | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| RTL8811AU | `88XXau`(외부, 공유) | 동일한 aircrack-ng 저장소 |

---

## 4. 드라이버 호환성 분석

### 4.1 커널 내장 vs 외부 DKMS

NetHunter용 어댑터를 선택할 때 가장 중요한 단 하나의 결정은 드라이버가 커널 트리 내부에 있는지 외부에 있는지입니다. 그 이유는 다음과 같습니다:

| | 커널 내장(MT7610U, MT7612U) | 외부 DKMS(RTL8812AU, RTL8811AU) |
|---|---|---|
| 플러그 앤 플레이 | ✅ 예 — 삽입 시 인식 | ⚠️ 커널에 `88XXau`가 사전 컴파일되어 있는지에 따라 다름 |
| 커널 업데이트 후에도 유지 | ✅ 예 — 드라이버가 커널 빌드의 일부 | ❌ 커널 업데이트 후 중단될 수 있음, 재컴파일 필요 |
| linux-headers 필요 | ❌ 아니요 | ✅ 수동 컴파일이 필요한 경우 예 |
| DKMS 필요 | ❌ 아니요 | ✅ 커널에 사전 컴파일되지 않은 경우 예 |
| 커뮤니티 문서 | 보통 | 광범위(ACH가 가장 많은 튜토리얼 보유) |
| 현장 실패 위험 | 낮음 | 보통(컴파일 의존성) |

**결론:** 현장에서 드라이버 문제 위험을 최대한 낮추고 싶다면 MT7610U 또는 MT7612U 어댑터를 선택하시기 바랍니다. 드라이버가 이미 커널에 있어 컴파일할 것도, 업데이트 중 깨질 것도, 현장에서 문제를 해결할 것도 없습니다.

### 4.2 NetHunter 커널 모듈 지원 매트릭스

| 기기 | NetHunter 커널 | MT7610U (`mt76x0u`) | MT7612U (`mt76x2u`) | RTL8812AU (`88XXau`) |
|---|---|---|---|---|
| OnePlus 11 5G | Android 13 커널 | ✅ 지원 | ✅ 지원 | ✅ 지원 |
| Samsung S20 FE (Snapdragon) | Android 12 커널 (4.19) | ✅ 지원 | ✅ 지원 | ✅ 지원(XDA 보고 확인) |
| Nothing Phone (1) | Android 12/13 커널 | ✅ 지원 | 커널 구성 확인 | ✅ 지원 |
| OnePlus 7/7T | 4.14 (구형) | ✅ 지원 | ⚠️ 빌드에서 누락될 수 있음 | ✅ 지원 |

출처: NetHunter GitLab, XDA 포럼 커뮤니티 보고(2024~2026).

### 4.3 알려진 문제

**문제 1: 구형 커널에서 MT7612U 인터페이스가 나타나지 않음**

증상: `lsusb`에는 `0e8d:7612`가 표시되지만 `ip link`에 `wlan1`이 나열되지 않음.  
근본 원인: 커스텀 커널이 `mt76x2u` 모듈 없이 컴파일됨. 일부 4.14 기반 NetHunter 커널(OnePlus 7T 시대)에 영향을 미침.  
해결: 해당 모듈이 포함된 커널 빌드를 사용하거나, 구형 커널에서 더 폭넓게 지원되는 AWUS036ACHM(MT7610U)으로 전환.

**문제 2: USB 전압 강하(brownout)로 인한 어댑터 연결 끊김**

증상: 스캔 도중 어댑터가 사라지고 `dmesg`에 USB 리셋 오류 표시.  
근본 원인: 특히 USB 3.0 어댑터(ACH는 ~500mW 소비)의 경우 휴대폰 USB 포트가 어댑터의 전류 소비를 유지할 수 없음.  
해결: 데이터를 휴대폰으로 전달하면서 벽면 어댑터에서 어댑터에 5V를 공급하는 전원 공급형 OTG 허브 사용.

**문제 3: chroot 시작 전에 어댑터를 삽입함**

증상: Android가 USB 권한 대화 상자를 표시하지만 Kali 도구가 어댑터에 접근할 수 없음.  
근본 원인: USB 장치가 노출되기 전에 NetHunter chroot 환경이 실행 중이어야 함.  
해결: chroot를 먼저 시작(Kali Services → Start)한 다음 어댑터를 연결하고 USB 권한을 부여.

---

## 5. 설정 가이드

### 5.1 사전 요구사항

하드웨어를 연결하기 전에 다음을 확인합니다:

```bash
# 기기가 루팅되었는지 확인
su -c "id"

# NetHunter chroot 버전 확인
cat /kali/etc/os-release
# NetHunter가 적용된 Kali Linux가 표시되어야 함

# USB OTG가 활성화되었는지 확인
# 설정 → 개발자 옵션 → OTG (정확한 위치는 Android 버전에 따라 다름)
```

### 5.2 하드웨어 연결 순서

순서가 중요합니다:

1. **NetHunter 앱** 실행 → **Kali Services** 열기 → **Start**를 탭하여 chroot 시작
2. **전원 공급형 OTG 허브**를 휴대폰의 USB 포트에 연결
3. **ALFA 어댑터**를 OTG 허브에 연결
4. Android USB 권한 대화 상자가 나타나면 **OK**를 탭하고 **항상 허용** 체크

{{< alert "circle-info" >}}
지속적인 작동을 위해 전원 공급형 OTG 허브를 강력히 권장합니다. AWUS036ACH는 약 500mW를 소비합니다. 휴대폰 배터리에서 직접 전원을 공급하면 소모가 크게 가속되고 USB 불안정을 유발할 수 있습니다. 벽면 어댑터에서 전력을 끌어오면서 데이터를 전달하는 허브는 이 두 문제를 모두 제거합니다.
{{< /alert >}}

### 5.3 어댑터 감지 확인

```bash
# USB 장치 목록 — 어댑터가 나타나는지 확인
lsusb

# 모델별 예상 출력:
# AWUS036ACHM: Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.
# AWUS036ACM:  Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U
# AWUS036ACH:  Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp.
```

어댑터가 나타나지 않는 경우: 다른 OTG 케이블을 시도하거나, 개발자 설정에서 OTG가 활성화되어 있는지 확인하거나, 컴퓨터에서 어댑터를 테스트하여 정상 작동하는지 확인하시기 바랍니다.

### 5.4 드라이버 로드

**MT7610U(AWUS036ACHM)의 경우 — 대부분의 커널에서 자동 로드:**

```bash
# 자동 로드 확인
lsmod | grep mt76

# 필요 시 수동 로드 (드문 경우)
sudo modprobe mt76x0u
```

**MT7612U(AWUS036ACM)의 경우 — 커널 4.19+에서 자동 로드:**

```bash
# 확인
lsmod | grep mt76

# 필요 시 수동 로드
sudo modprobe mt76x2u
```

**RTL8812AU(AWUS036ACH)의 경우 — 대부분의 NetHunter 커널에 사전 컴파일됨:**

```bash
# 사전 컴파일된 모듈 로드
sudo modprobe 88XXau

# 로드되었는지 확인
lsmod | grep 88XX
```

### 5.5 네트워크 인터페이스 확인

```bash
# 무선 인터페이스 목록
ip link show | grep wlan

# 또는 iw 사용
iw dev

# 외부 어댑터는 일반적으로 wlan1로 나타남
# (wlan0은 보통 휴대폰의 내장 WiFi)
```

### 5.6 모니터 모드 활성화

```bash
# 방해 프로세스 종료
sudo airmon-ng check kill

# 어댑터에서 모니터 모드 시작
sudo airmon-ng start wlan1

# 모니터 모드가 활성 상태인지 확인
iwconfig wlan1mon
# 예상 출력: Mode:Monitor

# 주변 네트워크 스캔 (승인된 테스트 전용)
sudo airodump-ng wlan1mon

# 모든 대역 스캔 (2.4 GHz + 5 GHz)
sudo airodump-ng --band abg wlan1mon
```

### 5.7 관리 모드로 복귀

```bash
sudo airmon-ng stop wlan1mon
sudo service NetworkManager restart
```

---

## 6. 애플리케이션 토폴로지

<img src="/images/blog/nethunter-topology.png" alt="NetHunter + ALFA 애플리케이션 토폴로지 다이어그램" loading="eager" style="max-width:100%;height:auto;display:block">

---

## 7. 검증 결과

### 7.1 테스트 매트릭스

다음 조합은 커뮤니티 테스트와 벤더 문서를 통해 검증되었습니다:

| 휴대폰 | ALFA 어댑터 | 칩셋 | 모니터 모드 | 패킷 인젝션 | 상태 |
|---|---|---|---|---|---|
| OnePlus 11 5G | AWUS036ACHM | MT7610U | ✅ | ✅ | 검증됨 |
| OnePlus 11 5G | AWUS036ACM | MT7612U | ✅ | ✅ | 검증됨 |
| OnePlus 11 5G | AWUS036ACH | RTL8812AU | ✅ | ✅ | 검증됨 |
| Samsung S20 FE (Snapdragon) | AWUS036ACH | RTL8812AU | ✅ | ⚠️ | 커뮤니티 보고 — 커널 구성 확인 |
| Samsung S20 FE (Snapdragon) | AWUS036ACHM | MT7610U | ✅ | ✅ | 커뮤니티 보고 |
| Nothing Phone (1) | AWUS036ACHM | MT7610U | ✅ | ✅ | 커뮤니티 보고 |

출처: XDA 포럼, Reddit r/NetHunter, Kali NetHunter GitLab Issues(2024~2026).

### 7.2 예상 `lsusb` 출력

```
# AWUS036ACHM
Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.

# AWUS036ACM
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter

# AWUS036ACH
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
```

### 7.3 모니터 모드 검증

```bash
# 성공 시 예상 iwconfig 출력
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.437 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

---

## 8. 권장 사항

### 8.1 최고 추천: OnePlus 11 5G + AWUS036ACHM

이 조합은 테스트한 모든 설정 중 마찰이 가장 적습니다. OnePlus 11은 대만 시장에서 여전히 구할 수 있으면서 공식 NetHunter 커널을 지원하는 가장 최신 플래그십입니다. AWUS036ACHM의 MT7610U 칩셋은 `mt76x0u` 드라이버를 사용하며, 이는 4.19부터 메인라인 커널에 포함되어 있고 컴파일이 전혀 필요 없습니다. 국제 보안 커뮤니티(Lab401, morrownr USB-WiFi 데이터베이스)는 이를 Kali 및 NetHunter에 가장 안전한 선택으로 지속적으로 평가합니다. 이 어댑터는 컴팩트하고 단일 안테나이며 USB 2.0에서 작동하는데, 이는 모바일 시나리오에서 이점입니다. 낮은 전력 소비, 낮은 발열, 문제 발생 여지가 적습니다.

### 8.2 성능 추천: OnePlus 11 5G + AWUS036ACM

장거리 5 GHz 캡처를 위한 MIMO 2T2R을 갖춘 듀얼 밴드 AC1200 성능이 필요하다면, ACM은 커널 내장 드라이버 생태계를 벗어나지 않고 이를 제공합니다. MT7612U의 `mt76x2u` 드라이버 역시 4.19부터 메인라인에 포함되어 있습니다. 절충점: USB 3.0은 더 많은 전력을 소비하고 듀얼 안테나 본체는 더 큽니다. 커널에 `mt76x2u`가 포함되어 있는지 확인하시기 바랍니다. OnePlus 11에서는 이것이 확인되었습니다.

### 8.3 커뮤니티 인기작: 모든 NetHunter 기기 + AWUS036ACH

ACH는 NetHunter 생태계의 어떤 어댑터보다 가장 많은 튜토리얼, 가장 큰 커뮤니티 문제 해결 기반, 가장 우수한 서드파티 문서를 보유하고 있습니다. 듀얼 5dBi 안테나는 ALFA 제품군 중 가장 강력한 신호 도달 범위를 제공합니다. 대부분의 NetHunter 커널은 `88XXau` 모듈을 사전 컴파일하므로 컴파일이 거의 필요하지 않습니다. 플러그 앤 플레이의 단순함보다 커뮤니티 지원과 장거리 캡처를 중시한다면 이것이 선택지입니다.

### 8.4 시나리오 기반 선택

| 시나리오 | 권장 조합 | 근거 |
|---|---|---|
| 첫 NetHunter 설정, 위험 최소화 | OnePlus 11 + AWUS036ACHM | 커널 내장 드라이버, 컴파일 불필요, 최소 폼 팩터 |
| 장거리 듀얼 밴드 캡처 | OnePlus 11 + AWUS036ACM | AC1200 + MIMO, 여전히 커널 내장 |
| 장거리 서베이, 최대 튜토리얼 | 모든 지원 기기 + AWUS036ACH | 최강 안테나, 가장 폭넓은 커뮤니티 지원 |
| 초휴대용, 최저 전력 | 모든 지원 기기 + AWUS036ACS | 300mW 소비, 어느 주머니에나 들어감 |

### 8.5 지원 자료

| 자료 | 링크 |
|---|---|
| Yopitek — 대만 ALFA 공인 유통업체 | [yupitek.com](https://www.yupitek.com) |
| ALFA Network 공식 제품 페이지 | [alfa.com.tw](https://www.alfa.com.tw) |
| MT7610U 드라이버(커널 트리) | [torvalds/linux — mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| RTL8812AU 드라이버(aircrack-ng) | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| NetHunter 지원 기기 | [nethunter.kali.org/device-kernels.html](https://nethunter.kali.org/device-kernels.html) |
| NetHunter 공식 문서 | [kali.org/docs/nethunter/](https://www.kali.org/docs/nethunter/) |
| XDA NetHunter 포럼 | [xdaforums.com/tags/nethunter/](https://xdaforums.com/tags/nethunter/) |
| Yopitek ALFA 제품 카탈로그 | [/ko/products/alfa/](/ko/products/alfa/) |

---

## 부록: 빠른 문제 해결

**`lsusb`에 어댑터가 없음:**
1. 개발자 옵션에서 OTG가 활성화되어 있는지 확인
2. 다른 OTG 케이블 시도 — 케이블 품질이 가장 흔한 실패 지점
3. 전원 공급형 OTG 허브 사용
4. NetHunter chroot가 시작되었는지 확인

**`lsusb`에는 기기가 나타나지만 `wlan1` 인터페이스가 없음:**

```bash
# 드라이버 오류에 대한 커널 메시지 확인
dmesg | tail -30 | grep -E "usb|mt76|rtl|88XX"

# 커널 모듈이 존재하는지 확인
find /lib/modules -name "mt76*" 2>/dev/null
find /lib/modules -name "*88XX*" 2>/dev/null

# 수동 로드 시도
sudo modprobe mt76x0u   # MT7610U
sudo modprobe mt76x2u   # MT7612U
sudo modprobe 88XXau    # RTL8812AU
```

**모니터 모드는 시작되지만 네트워크가 나타나지 않음:**

```bash
# 먼저 방해 프로세스 종료
sudo airmon-ng check kill

# 모든 대역 재스캔
sudo airodump-ng --band abg wlan1mon

# 채널 설정 확인
sudo iw dev wlan1mon info
```

**사용 중 어댑터 연결 끊김(USB 리셋):**

```bash
# 임시 해결 — 송신 전력 감소
sudo iw dev wlan1 set txpower fixed 1000  # 10 dBm

# 영구 해결 — 전원 공급형 OTG 허브 사용
```

---

## 관련 가이드

- [ALFA 어댑터와 NetHunter의 기본 OTG 설정](/ko/blog/alfa-adapter-nethunter-android-otg/)
- [ALFA WiFi 어댑터 구매 가이드 2026](/ko/blog/alfa-wifi-adapter-buyer-guide-2026/)
- [Kali Linux 및 Ubuntu에서 ALFA 드라이버 설치하기](/ko/blog/install-alfa-driver-kali-ubuntu/)
- [Raspberry Pi 및 Kali에서 ALFA 어댑터 사용하기](/ko/blog/alfa-adapter-raspberry-pi-kali/)

---

{{< faq >}}

*본 문서는 대만 ALFA Network 공인 유통업체 **Yopitek Ltd**가 작성했습니다.*  
*데이터는 2026-06-09 기준입니다. Linux 커널 및 NetHunter 버전은 정기적으로 업데이트되므로, 최신 호환성 정보는 공식 출처를 통해 확인하시기 바랍니다.*

## 참고 자료

1. [Kali NetHunter 공식 문서](https://www.kali.org/docs/nethunter/)
2. [Linux 커널 mt76 드라이버 소스](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek/mt76)
3. [aircrack-ng RTL8812AU 드라이버](https://github.com/aircrack-ng/rtl8812au)
4. [ALFA Network 공식 웹사이트](https://alfa.com.tw/)
5. [Android USB OTG 공식 문서](https://developer.android.com/guide/topics/connectivity/usb)
