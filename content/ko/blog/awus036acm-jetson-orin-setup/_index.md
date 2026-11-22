---
title: "컴파일 없는 설정: Jetson Orin 엣지 AI 시스템에서의 ALFA AWUS036ACM"
description: "AVALUE AIB-NW01(NVIDIA Jetson Orin NX/Nano) 엣지 AI 구축에 어떤 ALFA Network USB WiFi 어댑터가 가장 적합한지 심층 분석합니다. AWUS036ACM이 진정한 플러그 앤 플레이를 구현한다는 실제 검증 사례와 함께 살펴봅니다."
date: 2026-05-20
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "USB WiFi 어댑터는 왜 Jetson Orin에서 자주 실패합니까?"
    answer: "Jetson은 표준 Ubuntu 커널이 아니라 NVIDIA가 커스터마이즈한 Tegra 커널을 사용합니다. 서드파티 드라이버는 사용 가능한 커널 헤더가 없거나 ABI 비호환으로 인해 컴파일에 실패하는 경우가 많습니다."
  - question: "AWUS036ACM은 Jetson Orin에서 드라이버 컴파일이 필요합니까?"
    answer: "아니요. MT7612U용 mt76x2u 드라이버는 커널 4.19부터 메인라인 커널에 포함되어 있습니다. AIB-NW01의 커널 5.10에도 이미 들어 있습니다. 그냥 꽂기만 하면 됩니다."
  - question: "AWUS036ACH(RTL8812AU)는 Jetson Orin에서 동작합니까?"
    answer: "동작하지만 수동 드라이버 컴파일이 필요합니다. JetPack의 NVIDIA 커널 패치가 cfg80211 ABI를 깨뜨려 컴파일 실패를 유발할 수 있습니다. 컴파일 경험이 있는 사용자에게만 권장합니다."
  - question: "JetPack 업그레이드가 USB WiFi 어댑터를 망가뜨릴 수 있습니까?"
    answer: "그럴 수 있습니다. 서드파티 드라이버는 커널 API 변경으로 인해 JetPack 업그레이드 후 작동이 중단되어 재컴파일이 필요할 수 있습니다. mt76x2u와 같은 인커널(in-kernel) 드라이버는 영향을 받지 않습니다."
  - question: "AIB-NW01은 어떤 Linux 커널 버전을 사용합니까?"
    answer: "AIB-NW01은 Ubuntu 20.04.6 LTS와 JetPack 5.0을 탑재하며, NVIDIA가 커스터마이즈한 Tegra 커널 5.10.x-tegra를 사용합니다. CPU 아키텍처는 ARM64입니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Jetson-Orin", "Edge-AI", "USB-WiFi", "AWUS036ACM", "AVALUE", "AIB-NW01"]
featureimage: "/images/blog/awus036acm-jetson-orin-setup.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---
> "유선 네트워크가 없는 환경에 배치해야 하는 AVALUE AIB-NW01(Jetson Orin NX)이 있습니다. 귀사의 USB WiFi 어댑터 중 별도 설정 없이 바로 동작하는 제품은 무엇입니까?"

## 한 통의 고객 이메일이 던진 핵심 질문

이것은 최근 Yopitek이 실제로 받은 질문입니다. 언뜻 단순해 보이지만, Jetson 개발자 커뮤니티를 조금이라도 경험해 본 분이라면 **NVIDIA Jetson 플랫폼에서의 USB WiFi가 대부분의 예상보다 훨씬 까다롭다는 사실**을 아실 것입니다.

{{< tldr >}}
Jetson Orin은 NVIDIA가 커스터마이즈한 Tegra 커널을 사용하며, 이 환경에서는 서드파티 WiFi 드라이버가 컴파일에 실패하는 경우가 많습니다. MT7612U를 탑재한 ALFA AWUS036ACM은 커널 4.19부터 드라이버가 인커널로 제공되어, 컴파일 없이 플러그 앤 플레이로 동작합니다. 모니터 모드, 패킷 인젝션, AP 모드를 지원합니다.
{{< /tldr >}}


ALFA AWUS036ACM은 Jetson Orin에서 진정으로 컴파일이 필요 없는 유일한 플러그 앤 플레이 USB WiFi 어댑터입니다. MT7612U 드라이버가 커널 4.19부터 메인라인 커널에 포함되어 있어, Jetson 커스텀 커널의 드라이버 컴파일 문제를 완전히 우회합니다.






Jetson 핵심 아키텍처, NVIDIA 포럼의 실제 사례, GitHub의 드라이버 컴파일 실패 보고, ARM64 플랫폼 벤치마크를 깊이 있게 조사하여 이 가이드를 정리했습니다.

---

## AIB-NW01의 무선 연결 옵션: 플랫폼을 먼저 이해하라

AVALUE AIB-NW01은 엣지 AI 애플리케이션을 위해 설계된 **팬리스(fanless) 임베디드 시스템**으로, 네 가지 NVIDIA Jetson Orin SoM 구성으로 제공됩니다. 전체 하드웨어 사양과 소프트웨어 환경은 다음과 같습니다.

### 하드웨어 사양

| 항목 | 사양 |
|------|---------------|
| **SoM 옵션** | Jetson Orin NX 16GB / NX 8GB / Orin Nano 8GB / Orin Nano 4GB |
| **CPU** | ARM Cortex-A78AE v8.2 64비트 (NX 16GB: 8코어 @ 2.0 GHz / NX 8GB: 6코어 @ 2.0 GHz / Nano: 6코어 @ 1.5 GHz) |
| **GPU** | NVIDIA Ampere 아키텍처 (NX: 1024 CUDA 코어 + 32 Tensor 코어 / Nano 4GB: 512 CUDA 코어 + 16 Tensor 코어) |
| **AI 성능** | 100 / 70 / 40 / 20 TOPS (SoM 구성에 따라 다름) |
| **메모리** | LPDDR5 (NX 16GB/8GB: 128비트 102.4 GB/s / Nano 8GB: 128비트 68 GB/s / Nano 4GB: 64비트 34 GB/s) |
| **스토리지** | 128GB M.2 2280 NVMe SSD (내장) |
| **네트워크** | 2 × GbE RJ-45 (10/100/1000 Mbps) |
| **USB** | 4 × USB 3.1 Type-A, 1 × Micro USB OTG |
| **디스플레이** | 1 × HDMI Type-A |
| **시리얼** | 2 × DB9 (RS-232 / RS-485, 점퍼 선택식) |
| **확장 슬롯** | 1 × M.2 M-Key 2242/2280 (NVMe SSD), 1 × M.2 E-Key 2230 (WiFi/BT 모듈), 1 × M.2 B-Key 3042/3052 (5G/LTE 모듈, 표준 온도 사양 한정) |
| **SIM** | 1 × Micro SIM 슬롯 |
| **전원** | DC 10~24V (2핀 터미널 블록) |
| **크기** | 125 × 196 × 66 mm (벽면 마운트 제외) |
| **무게** | 1.4 kg |
| **섀시 재질** | 알루미늄 압출재 + 강판, 팬리스 방열 설계 |
| **동작 온도** | -15°C ~ 60°C (IEC60068-2 기준, 0.5 m/s 기류) |
| **보관 온도** | -40°C ~ 80°C |
| **인증** | CE, FCC Class A |

### 소프트웨어 환경

| 항목 | 사양 |
|------|---------------|
| **운영체제** | Ubuntu 20.04.6 LTS (Focal Fossa) |
| **NVIDIA SDK** | JetPack 5.0 (CUDA 11.4, cuDNN 8.4, TensorRT 8.4 포함) |
| **Linux 커널** | 5.10.x-tegra (NVIDIA 커스터마이즈 Tegra 커널, **표준 Ubuntu 커널 아님**) |
| **CPU 아키텍처** | ARM64 (aarch64) |
| **AI SDK 리소스** | [github.com/Avalue-Technology](https://github.com/Avalue-Technology/repositories.directory) |

> **중요 참고**: Jetson 플랫폼은 표준 Ubuntu 커널이 아니라 NVIDIA의 커스텀 `linux-tegra` 커널을 실행합니다. 이는 서드파티 드라이버 호환성에 깊은 영향을 미칩니다. 아래의 "Jetson Orin에서 USB WiFi가 겪는 세 가지 주요 난관"을 참고하십시오.

AIB-NW01은 세 가지 무선 연결 경로를 제공합니다.

### M.2 2230 E-Key (WiFi 모듈 슬롯)

**장점**: 높은 처리량, 내장형, USB 포트를 소모하지 않음
**단점**: 분해 필요, 안테나가 섀시 내부에 고정됨, 교체가 어려움, 모듈 호환성을 사례별로 검증해야 함

### USB 3.1 Type-A (4 포트)

**장점**: 핫스왑 가능, 분해 불필요, 최적 신호를 위해 안테나 위치 조정 가능, 여러 장치 간 공유 가능
**단점**: USB 어댑터는 부피가 큼, USB 인터페이스에 의해 속도 상한이 제한됨

### 5G M.2 B-Key (옵션)

**장점**: 독립적인 연결, 현장 WiFi 인프라에 의존하지 않음
**단점**: 비용 증가, SIM 카드와 월 요금제 필요, 설정이 복잡함

대부분의 엣지 AI 구축 시나리오(개념 증명 단계, 실외 감시, 공장 현장)에서는 **USB WiFi 어댑터가 가장 낮은 비용으로 가장 높은 유연성을 제공합니다.**

하지만 진짜 질문은 이것입니다. 아무 USB WiFi 동글이나 집어 들어 Jetson에 꽂으면 바로 동작하리라 기대할 수 있을까요?

답은 **반드시 그렇지는 않다는 것입니다. 그리고 실패율은 생각보다 훨씬 높습니다.**

---

## Jetson Orin에서 USB WiFi가 겪는 세 가지 주요 난관

대부분의 USB WiFi 관련 글은 x86 Linux만 다루지만, Jetson 플랫폼은 완전히 다른 영역입니다.

### 난관 1: 당신의 커널은 Ubuntu의 커널이 아니다

Jetson은 표준 Ubuntu 커널이 아니라 **NVIDIA가 커스터마이즈한 Tegra Linux 커널**을 실행합니다. 이것이 의미하는 바는 다음과 같습니다.

- `apt install linux-headers-$(uname -r)` 명령은 **일치하는 커널 헤더를 가져오지 못할 가능성이 높습니다**
- NVIDIA는 커널에 자체 패치를 적용하며, 이로 인해 서드파티 드라이버가 의존하는 ABI가 깨질 수 있습니다
- 커널 모듈 빌드 환경이 x86 데스크톱과 완전히 다릅니다

"Linux 지원"이라고 광고되는 USB 어댑터라도 **Jetson에서 컴파일이 성공하리라는 보장은 없습니다.**

### 난관 2: 서드파티 드라이버 컴파일이 Jetson에서 자주 실패한다

GitHub의 실제 사례(2025년 4월): JetPack 6.2(커널 5.15.148-tegra)에서 RTL8812EU 드라이버가 `make`와 `dkms` 단계 모두에서 실패했습니다. 커뮤니티 분석 결과, **JetPack의 NVIDIA 커널 패치가 cfg80211 ABI를 깨뜨려** 서드파티 WiFi 드라이버가 올바르게 컴파일되지 못하는 것으로 밝혀졌습니다.

> 출처: [GitHub issue #421 — RTL8812EU Driver Compilation Failed on Jetson Orin Nano](https://github.com/svpcom/wfb-ng/issues/421)

### 난관 3: JetPack 업그레이드가 어댑터를 "먹통"으로 만들 수 있다

NVIDIA 포럼 사례(2024년 10월): RTL8188EUS 어댑터가 JetPack 5.1.x에서는 정상 동작했으나 JetPack 6으로 업그레이드한 후 **전혀 인식되지 않았습니다**. 해결책은 GitHub에서 드라이버를 수동으로 재컴파일하는 것이었지만, 다음 JetPack 릴리스가 또다시 커널 API를 변경하면 어떻게 될까요?

> 출처: [Jetson Orin Nano — JetPack 6 Does Not Support RTL8188EUS](https://nvidia-jetson.piveral.com/jetson-orin-nano/jetpack-6-doesnt-support-rtl8188eus/)

### 핵심 결론

> **Jetson 플랫폼에서 진정으로 신뢰할 수 있는 유일한 선택지는 인커널 드라이버를 갖춘 USB WiFi 어댑터입니다.**

NVIDIA는 인커널 드라이버와의 호환성을 유지할 이해관계를 가지고 있으며, 이것이 JetPack 업그레이드 후에도 어댑터가 계속 동작하리라는 유일한 보장입니다.

---

## 칩셋 호환성 개요: 한눈에 보기

주요 ALFA Network USB WiFi 칩셋이 Jetson Orin에서 어떻게 평가되는지 정리했습니다.

| 칩셋 | ALFA 모델 | 드라이버 출처 | 최소 커널 | Jetson Orin 평가 |
|---------|------------|---------------|----------------|---------------------|
| **MT7612U** | **AWUS036ACM** | **인커널 (mt76x2u)** | **4.19+** | ✅ 완전 호환, 플러그 앤 플레이 |
| RTL8812AU | AWUS036ACH | 아웃오브트리 (컴파일 필요) | 수동 컴파일 | ⚠️ 사용 가능하나 컴파일에 위험 수반 |
| RTL8811AU | AWUS036ACS | 아웃오브트리 (컴파일 필요) | 수동 컴파일 | ⚠️ RTL8812AU와 동일한 문제 적용 |
| RTL8832BU | AWUS036AX | 아웃오브트리 (컴파일 필요) | 수동 컴파일 | ⚠️ 컴파일 필요, 알려진 문제 있음 |
| MT7921AUN | AWUS036AXM | 인커널 (mt7921u) | **5.18+** | ❌ K5.10/5.15는 최소 요건 미충족 |
| RTL8832BU | AWUS036AXER | 아웃오브트리 (컴파일 필요) | 수동 컴파일 | ❌ 권장하지 않음, ARM64 지원 불확실 |

출처: [morrownr/USB-WiFi Chipset Support Table](https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Chipsets.md)

---

## 최우선 추천: ALFA AWUS036ACM (MediaTek MT7612U)

### 핵심 사양

| 항목 | 상세 |
|------|--------|
| 칩셋 | MediaTek MT7612U / MT7612UN |
| WiFi 표준 | 802.11ac (WiFi 5) 듀얼밴드 AC1200 |
| 최대 처리량 | 5 GHz: 867 Mbps / 2.4 GHz: 300 Mbps |
| 안테나 | 2 × RP-SMA 탈착형 5 dBi 듀얼밴드 안테나 |
| 인터페이스 | USB 3.0 (USB-C 커넥터) |
| 송신 출력 | 표준 출력, USB 포트 직접 연결에 적합 |

**제품 페이지**: https://yupitek.com/ko/products/alfa/awus036acm/

### 이유 1: 진정으로 "드라이버가 필요 없는" 유일한 솔루션

AWUS036ACM이 사용하는 MT7612U 칩셋은 드라이버(`mt76x2u`)가 **커널 4.19(2018년 10월)부터** 메인라인 Linux 커널에 내장되어 있습니다. AIB-NW01은 커널 5.10.x를 실행하므로 다음과 같습니다.

**꽂기만 하면 바로 동작합니다. 컴파일도, 설정도 필요 없습니다.**

이는 Jetson에서 결정적으로 중요합니다. 앞서 설명한 세 가지 난관(커스텀 커널, 컴파일 실패, 업그레이드로 인한 작동 중단)을 완전히 우회할 수 있기 때문입니다.

### 이유 2: ARM64에서 검증됨

한 GitHub 사용자가 ARM64 + 커널 5.10.198 환경에서 AWUS036ACM을 테스트했습니다.

```
$ lsusb | grep MediaTek
ID 0e8d:7612 MediaTek Inc. MT7612U

$ dmesg | grep mt76
mt76x2u 1-1:1.0 wlx00c0ca9821a5: renamed from wlan0
```

**설정 없이 바로 동작합니다.** 모듈은 `mt76x2u`입니다. 추가 단계가 필요 없습니다.

> 출처: [GitHub issue #574 — AWUS036ACM on ARM64 K5.10](https://github.com/morrownr/USB-WiFi/issues/574)

### 이유 3: 완전한 전문가용 기능 세트

이 어댑터는 기본 연결을 넘어, 완전한 무선 네트워킹 기능 세트를 지원합니다.

- 모니터 모드 — 네트워크 진단 및 분석용
- 패킷 인젝션 — 침투 테스트 및 연구용
- AP 모드 — AIB-NW01을 WiFi 핫스팟으로 전환 (5 GHz에서는 `disable_usb_sg` 모듈 파라미터가 필요할 수 있음)
- VIF (가상 인터페이스) — 동일 어댑터에서 모니터 + 매니지드 인터페이스를 동시에 운용

### 이유 4: 비할 데 없는 안테나 유연성

2 × RP-SMA 외장 안테나 설계 덕분에 다음이 가능합니다.

- 고이득 안테나(예: 9 dBi)로 교체하여 커버리지 확장
- 지향성 안테나를 사용해 특정 영역에 신호 집중
- 연장 케이블을 통해 금속 함체 외부로 안테나 배치 (산업용 캐비닛 구축에서 결정적)

---

## AWUS036ACM의 다섯 가지 구체적 이점

### 이점 1: 즉각적인 연결, 배치 지연 제로

꽂으면 시스템이 즉시 `wlan0`(또는 `wlx...`) 인터페이스로 인식합니다. 단 세 개의 명령이면 됩니다.

```bash
# Scan available networks
sudo nmcli device wifi list

# Connect
sudo nmcli device wifi connect "Your_SSID" password "Your_Password"
```

컴파일도, 재부팅도, 패키지 설치도 필요 없습니다.

### 이점 2: 모든 M.2 WiFi 모듈의 한계를 우회

| M.2 WiFi 모듈 | USB WiFi 어댑터 (AWUS036ACM) |
|-----------------|-------------------------------|
| 분해 필요 | 외장형, 분해 불필요 |
| 안테나가 섀시 내부에 고정됨 | 최적 신호를 위해 안테나 배치 가능 |
| 교체가 어려움 | 핫스왑 가능, 즉시 교체 |
| 단일 장치에 종속됨 | 여러 장치 간 공유 가능 |

### 이점 3: 산업 현장 구축을 위한 설계

AWUS036ACM은 전형적인 엣지 AI 프로젝트 생애주기에 들어맞습니다.

- **공장 현장** — 가까이에 이더넷 포트가 없다? 꽂아서 무선으로 연결
- **실외 감시** — WiFi가 유일한 데이터 백홀 채널인 경우
- **임시 배치** — POC 단계에서 M.2 모듈을 위해 섀시를 열 이유가 없을 때
- **이동형 플랫폼** — 안정적인 무선 연결이 필요한 AGV/AMR 유닛

### 이점 4: 가장 낮은 장기 유지보수 비용

인커널 드라이버의 실질적 이점은 다음과 같습니다.

- JetPack 업그레이드에도 어댑터가 살아남습니다 (NVIDIA가 인커널 드라이버를 직접 유지보수)
- DKMS나 수동 드라이버 컴파일을 걱정할 필요 없음
- 커널 보안 업데이트가 차단되지 않음
- 지속적인 유지보수 및 지원 부담이 획기적으로 감소

### 이점 5: 환경에 맞춰 조정 가능한 신호 커버리지

2 × RP-SMA 외장 안테나 설계는 이 어댑터를 구성 가능한 무선 솔루션으로 만듭니다. 구축 환경에 따라 다음이 가능합니다.

- 고이득 안테나(예: 9 dBi)로 교체하여 범위 확장
- 지향성 안테나로 신호 집중
- 연장 케이블을 통해 금속 함체 외부로 안테나 배치 (산업용 캐비닛 시나리오)
- 금속 표면에 부착되는 자석 베이스 안테나 사용

---

## 설치 단계: 말 그대로 단 세 단계

### 1단계: 꽂기

AWUS036ACM을 AIB-NW01의 USB 3.0 Type-A 포트 중 아무 곳에나 연결합니다.

### 2단계: 드라이버 로드 확인

```bash
lsusb | grep MediaTek
# Expected output: ID 0e8d:7612 MediaTek Inc. MT7612U

dmesg | grep mt76
# Expected output: mt76x2u 1-1:1.0 wlx...: renamed from wlan0
```

### 3단계: WiFi 연결

```bash
# Scan available networks
sudo nmcli device wifi list

# Connect
sudo nmcli device wifi connect "Your_SSID" password "Your_Password"

# Verify connection status
ip addr show wlx...
```

끝입니다. 이제 Jetson Orin이 온라인 상태입니다.

---

## 유의 사항 및 솔직한 고지

### AWUS036ACM은 WiFi 5 (AC1200)입니다

시장에서 가장 빠른 어댑터는 아닙니다. AWUS036AXM(WiFi 6E, MT7921AUN)이 이론적으로 더 빠르지만, AIB-NW01의 커널 5.10에서는 **동작하지 않습니다**(커널 5.18+ 필요). 데이터 텔레메트리, 모델 업데이트, 원격 SSH 등 대부분의 엣지 AI 애플리케이션이 요구하는 대역폭에는 AC1200이면 충분하고도 남습니다.

### ARM64 검증 맥락

GitHub issue #574의 검증은 AIB-NW01에서 직접 수행된 것이 아니라 **Odroid M1**(ARM64 + 커널 5.10)에서 이루어졌습니다. 두 기기는 동일한 커널 아키텍처와 드라이버 스택을 공유하므로 결과가 동일하리라는 높은 확신을 갖고 있습니다. 다만 실제 사용하는 하드웨어에서 테스트할 것을 항상 권장합니다.

### 다른 모델에도 쓸 자리가 있다

AWUS036ACH(RTL8812AU)와 AWUS036AX(RTL8832BU)는 사용할 수 없는 제품이 아닙니다. 다만 Jetson에서 수동 드라이버 컴파일이 필요할 뿐입니다. 빌드 환경을 갖추고 있고 드라이버를 직접 유지보수할 의향이 있다면, 이 모델들도 고려할 가치가 있습니다.

---

{{< faq >}}

## 결론: 가장 단순한 솔루션이 흔히 최선이다

처음의 고객 질문으로 돌아가 봅시다. 어떤 ALFA USB WiFi 어댑터가 AVALUE AIB-NW01에 가장 적합할까요?

답은 **ALFA AWUS036ACM**입니다.

가장 빠르거나 가장 저렴해서가 아니라, Jetson처럼 까다로운 플랫폼에서 **꽂는 순간 진정으로 동작하는** 유일한 어댑터이기 때문입니다. 드라이버 컴파일조차 운에 맡겨야 하는 상황에서는 인커널 지원이 왕입니다.

### 다음 단계

- 제품 상세 보기: https://yupitek.com/ko/products/alfa/awus036acm/
- 기술 지원: Yopitek은 대만 현지에서 기술 지원을 제공합니다. 도움이 필요하시면 문의해 주십시오

### 더 읽어보기

- [AWUS036ACH vs AWUS036ACM: RTL8812AU vs MT7612U 드라이버 비교](https://yupitek.com/ko/blog/awus036ach-vs-awus036acm/)
- [ALFA Network Linux 호환성 표](https://docs.alfa.com.tw/Support/Compat/)
- [NVIDIA 공식 검증 WiFi 모듈 목록 (AGX Orin)](https://forums.developer.nvidia.com/t/wi-fi-6-6e-7-modules-that-have-been-validated-with-agx-orin-devkits/313431)

---

> **태그**: #JetsonOrin #EdgeAI #ALFANetwork #USBWiFi #AWUS036ACM #Yopitek
>
> **작성자**: Yopitek Ltd — 대만 ALFA Network 공인 총판
>
> **면책 고지**: 본 문서의 조사 내용은 2026년 5월 기준입니다. Jetson 플랫폼과 Linux 커널 업데이트는 지속적으로 이루어지므로, 배치 전에 최신 JetPack 버전과 인커널 드라이버 지원 여부를 확인할 것을 권장합니다.

## 참고 자료

1. [AVALUE Technology AIB-NW01 제품 페이지](https://www.avalue.com.tw/)
2. [NVIDIA Jetson 공식 개발자 포럼](https://forums.developer.nvidia.com/)
3. [morrownr/USB-WiFi Chipset Support Table](https://github.com/morrownr/USB-WiFi)
4. [Linux 커널 mt76 드라이버 문서](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
5. [ALFA Network Linux 호환성 목록](https://docs.alfa.com.tw/Support/Compat/)
