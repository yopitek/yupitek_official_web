---
title: "Flipper Zero·Flipper One와 ALFA WiFi 어댑터: 완벽 호환성 가이드"
description: "Flipper Zero에서 ALFA USB WiFi 어댑터로 패킷 인젝션이 가능할까요? 불가능합니다 — 그 이유를 설명합니다. Flipper One은 ALFA AWUS036AXML의 모니터 모드를 지원합니다(패킷 인젝션은 커널 버전에 따라 다릅니다). 칩셋 분석, 드라이버 호환성, 설정 방법을 모두 담은 완벽 가이드."
date: 2026-06-10
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "Flipper Zero에 ALFA USB 무선 어댑터를 연결할 수 있나요?"
    answer: "불가능합니다. Flipper Zero의 STM32WB55 마이크로컨트롤러는 USB 디바이스 모드만 지원합니다. 외부 어댑터를 구동하는 USB 호스트 역할을 할 수 없습니다."
  - question: "Flipper One은 어떤 ALFA 어댑터 모델을 지원하나요?"
    answer: "Flipper One 창립자는 AWUS036AXML을 최고의 선택으로, AWUS036ACM을 가성비 최고 모델로 직접 테스트했습니다. 두 모델 모두 메인라인 Linux 커널에 드라이버가 내장되어 있습니다."
  - question: "AWUS036AXML이 Flipper One에 가장 선호되는 어댑터인 이유는 무엇인가요?"
    answer: "AWUS036AXML은 MT7921AUN 칩셋을 사용합니다. mt7921u 드라이버는 Linux 5.18부터 커널에 내장되어 있으며, 2.4/5/6 GHz 트라이밴드와 모니터 모드를 완전히 지원합니다."
  - question: "Flipper One은 언제 공식 출시되나요?"
    answer: "Flipper One은 현재 개발자 프리뷰 단계입니다. 공식 출시일과 가격은 크라우드펀딩을 통해 발표될 예정입니다. 자세한 내용은 flipper.net에서 확인하십시오."
  - question: "Flipper Zero WiFi Dev Board가 ALFA 어댑터를 대체할 수 있나요?"
    answer: "불가능합니다. WiFi Dev Board는 2.4 GHz 기본 기능만 지원하고 USB 호스트가 없으며, 통신 거리와 인젝션 안정성에서 전용 ALFA 어댑터에 한참 못 미칩니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-alfa-compatibility"
tags: ["flipper-zero", "flipper-one", "alfa-network", "wifi-adapter", "monitor-mode", "packet-injection", "kali-linux", "pentesting", "AWUS036AXML", "wireless-security"]
categories: ["Technical"]
featureimage: "/images/blog/flipper-alfa-compatibility.webp"
---
Flipper Zero를 이미 보유하고 있거나 구매를 고려 중이고, 무선 보안 테스트에 쓰이는 ALFA Network의 전설적인 USB WiFi 어댑터에 대해 들어보셨다면 아마 한 번쯤 이런 궁금증을 가지셨을 겁니다. **"ALFA 어댑터를 Flipper Zero에 꽂아서 WPA2 핸드셰이크를 캡처할 수 있을까?"**

{{< alert "triangle-exclamation" >}}
**법적 고지:** 모니터 모드와 패킷 인젝션은 본인이 소유하거나 명시적인 서면 테스트 허가를 받은 네트워크에서만 수행해야 합니다. 무단 무선 통신 감청은 대부분의 국가에서 불법입니다. 본 가이드에서 설명하는 모든 기법은 오로지 **허가된 침투 테스트, 본인 소유 장비에 대한 보안 연구, 교육 목적**으로만 사용되어야 합니다.
{{< /alert >}}

## 서론: 모든 침투 테스터가 던지는 질문

{{< tldr >}}
Flipper Zero의 STM32WB55는 USB 디바이스 모드만 지원하므로 어떤 ALFA 어댑터도 구동할 수 없습니다. RK3576와 완전한 Debian Linux를 탑재한 Flipper One은 AWUS036AXML로 트라이밴드 모니터링을 지원합니다(인젝션은 커널 버전에 따라 다릅니다).
{{< /tldr >}}


Flipper Zero는 하드웨어적 제약으로 인해 어떤 ALFA USB WiFi 어댑터도 사용할 수 없습니다. 반면 Flipper One은 AWUS036AXML 같은 모델을 완전히 지원하며 모니터 모드가 가능합니다(패킷 인젝션은 커널 버전에 따라 다르며 아래에서 설명합니다).







짧게 답하면 "불가능"이지만, 전체 답변은 훨씬 더 흥미롭습니다.

**Flipper Zero는 어떤 ALFA USB WiFi 어댑터에도 연결할 수 없습니다.** 이것은 소프트웨어가 아니라 하드웨어의 한계입니다. Flipper Zero 내부의 STM32WB55 마이크로컨트롤러에 탑재된 USB 컨트롤러는 **디바이스 전용 모드**로만 작동하며, WiFi 어댑터 같은 외부 주변기기를 구동하는 USB 호스트 역할을 물리적으로 할 수 없습니다.

하지만 Flipper Devices는 완전히 새로운 제품인 **Flipper One**을 발표했습니다. 8 GB RAM의 Rockchip RK3576에 완전한 Debian Linux를 구동하는 Flipper One은 USB 3.1 호스트 포트를 두 개 갖추고 있어, 6 GHz Wi-Fi 6E 분석을 포함한 완전한 무선 보안 테스트를 위해 ALFA 어댑터를 직접 사용할 수 있습니다. 실제로 Flipper One 창립자 Pavel Zhovner는 제품 발표에서 **ALFA AWUS036AXML**을 공식 테스트 어댑터로 직접 지목했습니다.

이 글에서는 전체 호환성 상황을 설명합니다. 무엇이 되고, 무엇이 안 되며, 왜 그런지, 그리고 어떻게 설정하는지를 다룹니다.

---

## Flipper Zero: ALFA 어댑터를 사용할 수 없는 이유

이 한계를 이해하려면 Flipper Zero 내부에 무엇이 들어 있는지 알아야 합니다.

### 하드웨어

| 구성 요소 | 사양 |
|-----------|--------------|
| **MCU** | STMicroelectronics STM32WB55RG |
| **아키텍처** | ARM Cortex-M4 (애플리케이션 코어) @ 64 MHz + ARM Cortex-M0+ (무선 코어) @ 32 MHz |
| **RAM** | 256 KB (코어 간 공유) |
| **저장장치** | 1 MB 플래시 + MicroSD |
| **운영체제** | FreeRTOS (실시간 운영체제) |
| **USB** | USB Type-C, USB 2.0 Full Speed (12 Mbps) |
| **USB 모드** | **디바이스 전용** — 호스트 또는 OTG 기능 없음 |

### USB의 한계

STM32WB55의 USB 컨트롤러는 **USB Full-Speed 디바이스 컨트롤러**입니다. Flipper Zero를 컴퓨터에 USB 디바이스로 인식시키는 것(파일 전송, 펌웨어 업데이트, CLI 인터페이스용)은 가능하지만, USB 호스트 역할은 할 수 없습니다. 칩에 호스트 컨트롤러 하드웨어 자체가 없기 때문에, 어떤 펌웨어 수정으로도 이 기능을 추가할 수 없습니다.

ALFA USB WiFi 어댑터를 사용하려면 디바이스에 다음이 필요합니다.
1. **USB 호스트 컨트롤러 하드웨어** — USB 디바이스를 열거하고 통신하기 위함
2. **WiFi 드라이버를 지원하는 Linux 커널** — `mt7921u`, `mt76`, `rtw88` 같은 드라이버를 로드하기 위함
3. **충분한 전력 공급** — ALFA 어댑터는 일반적으로 5V에서 500 mA ~ 900 mA를 소모함

Flipper Zero는 이 세 가지 요건을 모두 충족하지 못합니다.
- ❌ USB 호스트 컨트롤러 없음 (하드웨어)
- ❌ Linux가 아닌 FreeRTOS 구동 — 커널 드라이버 프레임워크가 존재하지 않음
- ⚠️ GPIO 5V 출력은 모든 핀 합산 1.2A로 제한되며, 수동으로 활성화해야만 사용 가능

> **결론:** 어떤 ALFA USB WiFi 어댑터도 Flipper Zero에 연결하는 것은 **물리적으로 불가능**합니다. 이것은 소프트웨어, 펌웨어 업데이트, 확장 보드로 우회할 수 있는 한계가 아니라 — 실리콘에 새겨진 제약입니다.

---

## Flipper Zero + WiFi Dev Board: 제한적인 대안

Flipper Devices는 **ESP32-S2** 마이크로컨트롤러 기반의 공식 **WiFi Dev Board**를 판매합니다. 이 보드는 Flipper Zero의 GPIO 헤더에 꽂혀 기본적인 2.4 GHz WiFi 기능을 제공하지만, USB 호스트 상황을 **바꾸지는** 못합니다.

| 항목 | 기능 |
|--------|-----------|
| **WiFi 칩** | ESP32-S2 (Xtensa LX7 싱글코어, 240 MHz) |
| **주파수** | 2.4 GHz 전용, 802.11 b/g/n |
| **USB 호스트** | ❌ WiFi Dev Board는 USB 호스트를 제공하지 않음 — ESP32-S2는 USB가 아닌 GPIO로 Flipper Zero에 연결됨 |
| **펌웨어** | ESP32 Marauder (커뮤니티 개발) |

**ESP32 Marauder 펌웨어**를 설치하면 WiFi Dev Board로 다음을 수행할 수 있습니다.

- ✅ 디인증(Deauthentication) 공격 (2.4 GHz 전용)
- ✅ PMKID 캡처 (2.4 GHz 전용)
- ✅ 액세스 포인트 스캔 및 SSID 브로드캐스트
- ✅ 기본 패킷 스니핑 (2.4 GHz 전용)

반면 할 수 **없는** 것은 다음과 같습니다.

- ❌ 외부 ALFA USB 어댑터 사용 (USB 호스트 없음)
- ❌ 5 GHz 또는 6 GHz 대역 운용
- ❌ 전용 ALFA 어댑터 수준의 통신 거리나 인젝션 안정성 달성
- ❌ aircrack-ng, Kismet, Wireshark 같은 Linux 기반 도구 실행

> **Flipper Zero만 보유하고 있고 기본적인 2.4 GHz 테스트가 필요하다면**, ESP32 Marauder를 탑재한 WiFi Dev Board가 기능은 하지만 심각하게 제한적인 임시 방편이 됩니다. 그 이상의 작업에는 다른 하드웨어가 필요합니다.

---

## Flipper One: ALFA가 기다려온 플랫폼

**2026년 5월 21일**, Flipper Devices 창립자 Pavel Zhovner는 *"Flipper One — We Need Your Help"*라는 블로그 글을 게시하며 완전히 새로운 제품을 발표했습니다. Flipper One은 Flipper Zero의 업그레이드가 아니라 — 프로토콜 스택의 다른 계층을 위해 설계된 완전히 다른 종류의 디바이스입니다.

> *"Flipper Zero는 Layer 0입니다 — 오프라인 지점 간 접근 제어: NFC, RFID, Sub-GHz, 적외선. Flipper One은 Layer 1입니다 — IP 연결성: Wi-Fi, Ethernet, 5G, 위성. 두 제품은 서로를 대체하지 않습니다."*
> — Pavel Zhovner, flipper.net

{{< alert "circle-info" >}}
**출시 안내:** Flipper One은 현재 **개발자 프리뷰** 단계입니다. 정식 출시, 가격, 지역별 유통은 크라우드펀딩을 통해 발표될 예정입니다. 업데이트는 [flipper.net](https://flipper.net)과 [Flipper One Developer Portal](https://docs.flipper.net/one)에서 확인하십시오.
{{< /alert >}}

### 하드웨어 사양

| 구성 요소 | 사양 |
|-----------|--------------|
| **CPU** | Rockchip RK3576: 4× Cortex-A72 + 4× Cortex-A53, 최대 2.2 GHz |
| **GPU** | ARM Mali-G52 MC3 (OpenGL ES 3.2, Vulkan 1.2) |
| **NPU** | 6 TOPS @ INT8 (로컬 LLM 구동 가능) |
| **보조 프로세서** | Raspberry Pi RP2350B (듀얼 M33 + 듀얼 RISC-V), 디스플레이/버튼/전원 담당 |
| **RAM** | 8 GB LPDDR5 |
| **저장장치** | 64 GB UFS 2.2 + MicroSD |
| **운영체제** | Debian 13 (Trixie) — Flipper Devices는 아웃오브트리 패치 의존성 없이 메인라인 Linux 커널 7.0을 목표로 한다고 밝힘 |
| **USB 호스트** | USB-C2 + USB-A, 모두 USB 3.1 (5 Gbps), 모두 호스트 가능 |
| **내장 WiFi** | MT7921AUN 기반 Wi-Fi 6E (2.4/5/6 GHz, 2×2 MIMO) |
| **Ethernet** | 2× RJ45 Gigabit (인라인/MitM 스니핑 지원) |
| **M.2 확장** | Key-B: PCIe 2.1 ×1 / USB 3.1 / SATA3 / SIM 카드 |

### Flipper One이 ALFA 어댑터와 작동하는 이유

Flipper Zero와 달리 Flipper One은 세 가지 요건을 모두 충족합니다.

1. ✅ **USB 3.1 호스트 컨트롤러**: 외부 디바이스를 열거하고 전력을 공급할 수 있는 호스트 가능 USB 포트 두 개
2. ✅ **완전한 Debian Linux**: `mt7921u`, `mt76`, `rtw88`를 커널 내에서 지원하는 표준 Linux 커널
3. ✅ **충분한 전력**: USB 포트가 표준 버스 전력을 공급하며, GPIO는 eFuse 보호와 함께 5V @ 2A, 3.3V @ 2A 제공

USB 3.1의 대역폭(5 Gbps)은 차고 넘칩니다 — 가장 빠른 ALFA 어댑터(AXE3000의 AWUS036AXML)조차도 USB 3.0의 실사용 처리량 약 1.2 Gbps에 의해 제한됩니다.

### 소프트웨어 환경

Flipper One은 표준 Debian 환경을 구동하므로, `apt`로 무선 보안 도구를 직접 설치할 수 있습니다.

```bash
sudo apt update
sudo apt install aircrack-ng kismet wireshark hcxdumptool hashcat
```

Flipper One은 또한 **Flipper OS Profiles**를 도입했습니다 — 스냅샷 기반 시스템으로 깨끗하고 격리된 환경을 생성할 수 있습니다. 모든 무선 도구를 갖춘 전용 "Pentest" 프로파일을 유지하면서, 일상적인 사용을 위해서는 교차 오염 없이 깨끗한 프로파일로 전환할 수 있습니다.

---

## Flipper One에 권장되는 ALFA 어댑터

모든 ALFA 어댑터가 무선 보안 테스트에 동등하게 잘 작동하는 것은 아닙니다. 핵심 요소는 **칩셋**, **드라이버 성숙도**, 그리고 **커널 내장 지원**(DKMS 컴파일 불필요를 의미)입니다.

### ⭐⭐⭐⭐⭐ 최고의 선택: AWUS036AXML (Wi-Fi 6E)

| 사양 | 세부 내용 |
|------|--------|
| **칩셋** | MediaTek MT7921AUN |
| **대역** | 2.4 / 5 / 6 GHz (Wi-Fi 6E) |
| **최대 속도** | AXE3000 (이론값), 실사용 약 1.2 Gbps |
| **드라이버** | `mt7921u` — Linux 5.18부터 커널 내장 |
| **DKMS 필요 여부** | ❌ 불필요 |
| **안테나** | 듀얼 RP-SMA (교체 가능) + Bluetooth 5.2 |

> **최고인 이유:** Flipper One 제작자가 직접 테스트한 바로 그 어댑터입니다. `mt7921u` 드라이버는 벤더 패치가 전혀 필요 없이 메인라인 커널에 포함되어 있습니다. 세 가지 WiFi 대역(2.4/5/6 GHz)을 모두 지원하므로 Wi-Fi 6E 보안 평가에 대비한 미래 지향적 선택입니다. 모니터 모드는 안정적이고 충분히 검증되어 있습니다. 패킷 인젝션은 커널 6.16 이전에서 동작한다는 커뮤니티 보고가 있으나, stock 커널 6.17 실측에서는 실패했습니다(aireplay-ng --test: Found 0 APs / No Answer). 원인은 커널 6.16 이후 mac80211 chanctx 회귀이며 칩 자체의 한계가 아닙니다. patched 드라이버에서는 동작하지만 펌웨어가 속도를 고정합니다(1/6 Mbps). 인젝션이 필요하면 AWUS036ACM 또는 ACH를 사용하세요.

### ⭐⭐⭐⭐⭐ 가성비 최고: AWUS036ACM (Wi-Fi 5 AC1200)

| 사양 | 세부 내용 |
|------|--------|
| **칩셋** | MediaTek MT7612U |
| **대역** | 2.4 / 5 GHz (Wi-Fi 5) |
| **최대 속도** | AC1200 (300 + 867 Mbps) |
| **드라이버** | `mt76` — Linux 4.19부터 커널 내장 |
| **DKMS 필요 여부** | ❌ 불필요 |
| **안테나** | 듀얼 5 dBi RP-SMA (교체 가능) |

> **가성비 최고인 이유:** MT7612U 칩셋은 침투 테스트 커뮤니티에서 충분히 검증되었습니다. `mt76` 드라이버는 수년간 커널에 포함되어 있었으며 대단히 안정적입니다. 커널 6.5 이상에서 모니터 모드와 인젝션이 완벽하게 작동합니다. AXML보다 낮은 가격대에서 2.4/5 GHz 테스트에 최고의 가격 대비 성능을 제공합니다.

### ⭐⭐⭐⭐ 경량형 선택: AWUS036ACHM (Wi-Fi 5 AC600)

| 사양 | 세부 내용 |
|------|--------|
| **칩셋** | MediaTek MT7610U |
| **대역** | 2.4 / 5 GHz (Wi-Fi 5) |
| **최대 속도** | AC600 (이론값) |
| **드라이버** | `mt76` — Linux 4.19부터 커널 내장 |
| **DKMS 필요 여부** | ❌ 불필요 |
| **안테나** | 단일 고이득 RP-SMA (교체 가능) |

> **경량형 선택인 이유:** 가장 휴대성이 뛰어난 옵션입니다 — USB 2.0, 단일 안테나, 최저 소비 전력. ACM과 동일한 `mt76` 드라이버 계열을 사용합니다. 순수 처리량보다 크기와 전력 효율이 더 중요한 현장 작업에 이상적입니다. **참고:** ARM64 플랫폼(RK3576 포함)에서는 `airodump-ng`와 `aireplay-ng`를 동시에 실행하면 알려진 인터페이스 드롭 버그(morrownr 이슈 #379)가 발생할 수 있습니다. 이 점을 인지하고 사용하십시오.

### ⭐⭐⭐ 대안: AWUS036ACH (Wi-Fi 5 AC1200, RTL8812AU)

| 사양 | 세부 내용 |
|------|--------|
| **칩셋** | Realtek RTL8812AU |
| **대역** | 2.4 / 5 GHz (Wi-Fi 5) |
| **최대 속도** | AC1200 (300 + 867 Mbps) |
| **드라이버** | `rtw88` — Flipper One의 예정 커널에서는 커널 내장; 구형 시스템에서는 DKMS가 필요할 수 있음 |
| **DKMS 필요 여부** | ❌ Flipper One에서는 불필요 / ⚠️ 구형 커널에서는 [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) DKMS가 필요할 수 있음 |
| **안테나** | 듀얼 6 dBi RP-SMA (높은 TX 출력) |

> **대안인 이유:** RTL8812AU 칩셋은 침투 테스트 분야에서 오랜 역사를 가지고 있습니다. Flipper One의 예정 커널에서 추가 DKMS 모듈 없이 지원될 것으로 예상됩니다. 구형 시스템의 경우 aircrack-ng DKMS 드라이버를 계속 사용할 수 있습니다. 고이득 6 dBi 안테나가 뛰어난 통신 거리를 제공하지만, 더 성숙한 커널 내장 드라이버 지원 덕분에 MediaTek 기반 어댑터가 일반적으로 선호됩니다.

> **또 다른 대안: AWUS036EACS(RTL8821CU).** `rtw88_8821cu` 드라이버가 Linux 커널 6.2부터 메인라인에 내장되어 있으며, GX10(Ubuntu 24.04 ARM64, 커널 6.17)에서 모니터 모드와 패킷 인젝션이 2.4 GHz/5 GHz 모두 동작함을 실측했습니다. 다만 Flipper One 자체에서는 아직 실측하지 않았습니다. 커널 6.2 이전의 오래된 시스템에서만 morrownr/8821cu 같은 커뮤니티 드라이버가 필요합니다.

### ⚠️ 사용 전 유의사항

다음 ALFA 모델은 Flipper One 자체에서는 테스트하지 않았습니다. ASUS GX10 테스트 환경(Ubuntu 24.04 ARM64, 커널 6.17)에서는 모두 모니터 모드가 동작했지만, 필요한 내장 드라이버는 최신 커널에만 있으며 인젝션 결과는 칩셋마다 다릅니다. **무선 보안 작업에 사용하기 전에 Flipper One의 커널 버전을 확인하십시오.**

| 모델 | 칩셋 | 문제점 |
|-------|---------|-------|
| AWUS036AX | RTL8832BU | rtw89_8852bu 드라이버는 커널 6.17부터 메인라인에 포함됨. GX10 실측: 모니터 가능, 인젝션 2.4 GHz 96%, 5 GHz 사용 가능. 오래된 커널은 커뮤니티 드라이버 필요 |
| AWUS036AXER | RTL8832BU | 동일한 RTL8832BU. GX10 실측: 모니터 가능, 인젝션 2.4 GHz 73%, 5 GHz 사용 가능 |
| AWUS036ACS | RTL8811AU | rtw88_8821au 드라이버는 커널 6.13부터 메인라인에 포함됨. GX10 실측: 모니터 가능, 인젝션 2.4 GHz 100%, 5 GHz 96% |

---

## 설정 가이드: Flipper One + ALFA AWUS036AXML

이 가이드는 Debian Linux를 구동하는 Flipper One에 어댑터가 USB 호스트 포트에 물리적으로 연결되어 있다고 가정합니다.

### 1단계: 어댑터 인식 확인

```bash
# USB 디바이스 열거 확인
lsusb
# 예상 출력 (예시):
# Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device

# 무선 인터페이스 목록
iw dev
# 예상: wlan0 (내장 WiFi가 wlan0을 차지하면 wlan1)

# 대체 확인 방법
ip link show
```

### 2단계: 드라이버 로드 확인

```bash
# AWUS036AXML / AWUS036AXM (MT7921AUN)의 경우:
lsmod | grep mt7921u

# AWUS036ACM / AWUS036ACHM (MT7612U / MT7610U)의 경우:
lsmod | grep mt76

# AWUS036ACH (RTL8812AU)의 경우:
lsmod | grep rtw88

# 커널 버전 확인 (MT7921AUN 최적 지원을 위해 6.12+ 권장):
uname -r
```

드라이버 모듈이 목록에 표시되면 로드되어 사용할 준비가 된 것입니다. 추가 설치가 필요 없습니다 — 모두 커널 내장 드라이버입니다.

### 3단계: 모니터 모드 활성화

```bash
# 간섭 프로세스 종료 (NetworkManager, wpa_supplicant 등)
# 참고: 이 명령은 Flipper One의 내장 WiFi도 끊습니다 — 평상시 네트워크 연결에
# 지장을 주지 않도록 침투 테스트 전용 Flipper OS 프로파일을 사용하십시오.
sudo airmon-ng check kill

# 어댑터에서 모니터 모드 시작
sudo airmon-ng start wlan0
# 인터페이스가 wlan0mon으로 변경됨

# 모니터 모드 활성화 확인
iw dev wlan0mon info
# 다음이 표시되어야 함: type monitor
```

수동 방법 (airmon-ng를 사용하지 않으려는 경우):

```bash
sudo ip link set wlan0 down
sudo iw wlan0 set monitor none
sudo ip link set wlan0 up
```

### 4단계: 패킷 인젝션 테스트

```bash
# 인젝션 기능 테스트
sudo aireplay-ng --test wlan0mon
# 확인할 문구: "Injection is working!"
# 참고: AXML/AXM은 커널 6.16 이상(실측 6.17)에서 실패합니다(Found 0 APs / No Answer). 인젝션에는 ACM / ACH를 사용하세요

# 기본 스캔 수행
sudo airodump-ng wlan0mon

# 지원되는 모든 대역 스캔 (AWUS036AXML 전용)
sudo airodump-ng --band abg wlan0mon     # 2.4 GHz + 5 GHz
sudo airodump-ng --band 6 wlan0mon       # 6 GHz (aircrack-ng 1.7+)

# 특정 채널 타겟팅
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF wlan0mon
```

### 5단계: WPA2 핸드셰이크 캡처

```bash
# 터미널 1: 대상 채널에서 캡처 시작
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# 터미널 2: 재연결을 유도하기 위해 deauth 전송
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon

# 터미널 1에서 핸드셰이크 캡처 확인:
# 캡처되면 "WPA handshake: AA:BB:CC:DD:EE:FF" 표시됨
```

### 6단계: 정상 작동 복귀

```bash
# 모니터 모드 중지 및 관리 모드 복원
sudo airmon-ng stop wlan0mon

# 네트워크 서비스 재시작
sudo systemctl restart NetworkManager
```

### 아키텍처 개요

아래 다이어그램은 Flipper One과 ALFA 어댑터를 사용한 완전한 무선 침투 테스트 아키텍처를 보여줍니다.

![Flipper One + ALFA WiFi 어댑터 침투 테스트 아키텍처](diagram/flipper-alfa-topology.svg)

*토폴로지: Flipper One 플랫폼 → ALFA USB 어댑터 → 침투 테스트 툴체인 → 무선 기능*

---

## Flipper Zero vs. Flipper One: 나란히 비교

| 기능 | Flipper Zero | Flipper One |
|---------|:-----------:|:----------:|
| **운영체제** | FreeRTOS | Debian 13 (Trixie) |
| **CPU** | STM32WB55 (Cortex-M4, 64 MHz) | RK3576 (8코어 ARM, 2.2 GHz) |
| **RAM** | 256 KB | 8 GB LPDDR5 |
| **저장장치** | 1 MB 플래시 + MicroSD | 64 GB UFS 2.2 + MicroSD |
| **GPU / NPU** | ❌ | Mali-G52 GPU + 6 TOPS NPU |
| **USB 호스트** | ❌ 디바이스 전용 | ✅ USB-C2 + USB-A (USB 3.1) |
| **ALFA 어댑터 지원** | ❌ | ✅ |
| **내장 WiFi** | ❌ (BLE 전용) | ✅ Wi-Fi 6E (MT7921AUN) |
| **5 GHz / 6 GHz WiFi** | ❌ | ✅ |
| **Gigabit Ethernet** | ❌ | ✅ 2× RJ45 |
| **모니터 모드** | ❌ (기본) | ✅ |
| **패킷 인젝션** | ❌ (기본) | ✅ |
| **M.2 확장** | ❌ | ✅ Key-B (PCIe / USB 3.1 / SATA) |
| **가격** | 약 169 USD (양산 중) | 개발자 프리뷰 (크라우드펀딩 미정) |

---

{{< faq >}}

## 결론: 작업에 맞는 올바른 도구

무선 보안 테스트에 ALFA WiFi 어댑터를 사용하려 한다면 **Flipper Zero는 잘못된 플랫폼**입니다 — 그 자체의 결함 때문이 아닙니다. Flipper Zero는 다른 목적, 즉 오프라인 접근 제어 테스트(NFC, RFID, Sub-GHz, 적외선)를 위해 설계되었습니다. 그 작업들에는 탁월하지만, USB 호스트 기능은 애초에 설계에 포함되지 않았습니다.

**ALFA 어댑터를 이용한 모니터 모드와 패킷 인젝션**이라는 구체적 용도에는 두 가지 경로가 있습니다.

| 경로 | 플랫폼 | ALFA 어댑터 | 기능 |
|------|----------|-------------|------------|
| **최고** | Flipper One | AWUS036AXML (MT7921AUN) | 완전한 2.4/5/6 GHz, 커널 내장 드라이버, 공식 지원 |
| **가성비** | Flipper One | AWUS036ACM (MT7612U) | 완전한 2.4/5 GHz, 커널 내장 드라이버, 검증된 안정성 |
| **임시 방편** | Flipper Zero + WiFi Dev Board | 없음 (ESP32-S2 내장) | 2.4 GHz 전용, 제한적 통신 거리, 기본 기능 |

**Flipper One은 세대적 도약을 상징합니다** — 완전한 Debian Linux 환경과 USB 3.1 호스트 기능을 휴대 가능한 전용 하드웨어 플랫폼에 담았습니다. ALFA AWUS036AXML(Flipper One 제작자가 직접 테스트한 어댑터)과 결합하면, 완전한 무선 보안 평가 툴킷을 주머니에 넣을 수 있습니다.

---

### 구매처

권장하는 모든 ALFA 어댑터는 ALFA Network 공식 총판인 Yopitek에서 구매할 수 있습니다. 전체 라인업을 둘러보거나 모델을 비교하십시오.

- [ALFA USB WiFi 어댑터 — 전체 카탈로그](https://yupitek.com/ko/products/alfa/) — 모든 모델의 사양과 가격
- [ALFA 제품 비교](/ko/alfa_compare/) — 칩셋, 대역, 드라이버 나란히 비교

### 더 읽을거리

- [Flipper One 공식 블로그 게시글](https://blog.flipper.net/flipper-one-we-need-your-help/) — Pavel Zhovner, 2026년 5월
- [Flipper One Developer Portal](https://docs.flipper.net/one) — 기술 사양 및 문서
- [패킷 인젝션이란?](/ko/blog/packet-injection-guide/) — 패킷 인젝션 기초 가이드
- [AWUS036AXML WiFi 6E 리뷰](/ko/blog/awus036axml-wifi-6e-review/) — 당사 플래그십 어댑터 심층 리뷰
- [ALFA 제품 비교](/ko/alfa_compare/) — 모든 ALFA 모델의 사양 나란히 비교

---

*Flipper One 및 ALFA 어댑터 호환성에 대한 사전 구매 문의는 support@yupitek.com으로 Yopitek 지원팀에 연락하거나 +886-2-87325338로 전화하십시오.*

## 참고 문헌

1. [Flipper One 공식 블로그, Pavel Zhovner 제품 발표](https://blog.flipper.net/flipper-one-we-need-your-help/)
2. [Flipper One Developer Portal, 기술 사양 및 문서](https://docs.flipper.net/one)
3. [Flipper Zero 공식 웹사이트](https://flipperzero.one/)
4. [aircrack-ng, 무선 보안 툴킷 공식 웹사이트](https://www.aircrack-ng.org/)
5. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
