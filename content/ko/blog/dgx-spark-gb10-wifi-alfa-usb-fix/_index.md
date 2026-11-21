---
title: "DGX Spark Wi-Fi가 연결되지 않나요? 이 ALFA USB 어댑터로 10분 만에 해결하세요"
description: "DGX Spark 등 GB10 AI 서버의 내장 Wi-Fi 문제를 드라이버 설치 없는 ALFA USB 어댑터로 10분 만에 해결하며, ASUS·MSI·HP·ALTOS·GIGABYTE 기종에도 적용됩니다."
date: 2026-05-20
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "DGX Spark Wi-Fi가 연결에 실패하는 이유는 무엇인가요?"
    answer: "DGX Spark에는 MediaTek MT7925 Wi-Fi 7 칩이 내장되어 있지만, OOBE 단계의 wpa_supplicant가 지나치게 간소화되어 있습니다. 특정 AP 브랜드(특히 UniFi)와 호환되지 않으며, WPA2-Enterprise는 거의 확실히 실패합니다."
  - question: "ALFA USB 어댑터 해결책은 모든 GB10 AI 서버에 적용되나요?"
    answer: "네. NVIDIA GB10 Grace Blackwell Superchip을 탑재한 모든 AI Edge Server(ASUS, MSI, HP, ALTOS, GIGABYTE)는 동일한 MT7925 Wi-Fi 칩을 사용합니다. ALFA AWUS036ACM 해결책은 모든 모델에서 작동할 것으로 예상됩니다(ASUS GX10에서만 실측했으며, 다른 기종은 개별적으로 테스트하지 않았습니다)."
  - question: "AWUS036ACM은 DGX Spark에서 드라이버 설치가 필요한가요?"
    answer: "아니요. MT7612U의 mt76 드라이버는 메인라인 커널 4.19부터 포함되어 있습니다. DGX OS Kernel 6.17+는 이를 기본 지원합니다. USB에 꽂으면 자동으로 로드됩니다."
  - question: "ALFA USB 어댑터 Wi-Fi 해결에는 시간이 얼마나 걸리나요?"
    answer: "10분 미만입니다. USB-C to USB-A 어댑터를 통해 GX10의 USB-C 포트에 꽂으면 시스템이 드라이버를 자동으로 로드하고, nmcli로 스캔하여 연결합니다. 드라이버 컴파일이나 재부팅이 필요 없습니다."
  - question: "DGX Spark에서 다른 ALFA 어댑터를 사용할 수 있나요?"
    answer: "네. 저희는 ASUS GX10(GB10, Ubuntu 24.04 ARM64, kernel 6.17)에서 ALFA 현행 네트워크 카드 9종을 실측했으며, 모두 커널 내장 드라이버를 사용해 꽂으면 바로 사용할 수 있고 DKMS가 필요 없습니다. AWUS036ACH는 내장 rtw88_8812au를 사용합니다. 다만 AWUS036AXM / AXML은 stock kernel 6.17에서 패킷 인젝션에 실패하므로 연결과 AP 용도에만 적합합니다. 다른 GB10 기종은 개별적으로 테스트하지 않았습니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["dgx-spark", "gb10", "ai-server", "wifi", "alfa-network", "tutorial", "asus-ascent-gx10", "msi-edgexpert", "hp-zgx-nano", "altos-brainsphere", "gigabyte-ai-top-atom"]
featureimage: "/images/blog/dgx-spark-gb10-wifi-alfa-usb-fix.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

> 📌 이 글은 2026년 11월 GX10 실측 결과를 반영해 업데이트되었습니다. ASUS GX10(Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia)에서 ALFA 현행 네트워크 카드 9종은 모두 커널 내장 드라이버를 사용하며, 꽂으면 바로 사용할 수 있고 DKMS가 필요 없습니다. 전체 데이터는 [ALFA 네트워크 카드 9종 ARM64 실측 종합표](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)를 참조하시기 바랍니다. GX10에서만 실측했으며, 다른 GB10 기종은 개별적으로 테스트하지 않았습니다.

오랫동안 기다려 온 <strong>NVIDIA DGX Spark</strong>(코드명 Project DIGITS)가 드디어 도착했습니다.

{{< tldr >}}
NVIDIA DGX Spark와 모든 GB10 AI 서버는 내장 MT7925 Wi-Fi 7 칩에 알려진 연결 결함이 있습니다. 해결책은 ALFA AWUS036ACM USB 어댑터를 꽂는 것입니다. mt76 드라이버는 4.19부터 커널에 내장되어 있으며, DGX OS Kernel 6.17+는 플러그 앤 플레이로 작동합니다. 10분이면 연결이 완료됩니다.
{{< /tldr >}}




개봉하고 전원을 연결하면 OOBE(최초 설정) 화면이 나타납니다 — 모든 것이 순조로워 보입니다. Wi-Fi 네트워크를 선택하고 비밀번호를 입력하면 화면이 30초 동안 돌아갑니다...

<strong>"이 네트워크에 연결할 수 없습니다."</strong>

다시 시도합니다. 재부팅합니다. 초기화합니다. 여전히 실패합니다.

당신만 겪는 문제가 아닙니다. [NVIDIA 개발자 포럼](https://forums.developer.nvidia.com)에는 정확히 같은 문제, 즉 DGX Spark의 Wi-Fi가 작동하지 않는다는 <strong>수십 개의 스레드</strong>가 올라와 있습니다.

이것은 설정 실수가 아닙니다. DGX Spark의 알려진 설계 결함입니다.

---

## 근본 원인: DGX Spark Wi-Fi는 왜 이렇게 불안정한가?

DGX Spark와 <strong>NVIDIA GB10 Grace Blackwell Superchip</strong>을 기반으로 하는 다른 모든 AI 서버는 <strong>MediaTek MT7925 Wi-Fi 7 칩</strong>을 사용합니다. 사양만 보면 최상급 하드웨어입니다.

문제는 소프트웨어 계층에 있습니다.

### 세 가지 치명적 결함

<strong>① OOBE Wi-Fi supplicant가 지나치게 간소화됨</strong>

DGX Spark의 최초 설정은 대부분의 엔터프라이즈 인증 기능을 제거한 최소 `wpa_supplicant`를 사용합니다. 이 때문에 특정 액세스 포인트와의 연결(association)을 완료하지 못하며, Ubiquiti UniFi가 가장 흔하게 보고되는 사례입니다.

NVIDIA는 이 문제를 <strong>DGX Spark 릴리스 노트(2026년 4월 업데이트)</strong>에 명시적으로 문서화했으며, 이 글을 작성하는 시점까지도 해결되지 않았습니다.

<strong>② WPA2-Enterprise 비호환</strong>

사무실이나 연구실에서 WPA2-Enterprise(기업 환경에서 일반적)를 사용한다면, DGX Spark의 내장 Wi-Fi는 거의 확실히 실패합니다. 이는 설정 파일로 해결할 수 있는 문제가 아닙니다 — 드라이버 계층과 supplicant 양쪽 모두의 이중 한계입니다.

<strong>③ 무작위 "No Wi-Fi Adapter Found" 오류</strong>

NVIDIA 포럼(스레드 #356183)의 여러 사용자가 DGX Spark가 정상 사용 중 무작위로 "No Wi-Fi Adapter Found"를 표시하며, 복구하려면 전체 재부팅이 필요하다고 보고합니다. 더 나쁜 점은 <strong>연결이 끊긴 후 시스템이 자동으로 재연결하지 않는다는 것</strong>입니다 — 다시 온라인 상태가 되려면 `nmcli` 명령을 수동으로 실행해야 합니다.

| 문제 | 영향 |
|------|------|
| OOBE가 엔터프라이즈 AP에 연결하지 못함 | UniFi / WPA2-Enterprise — 완전히 작동 불가 |
| 무작위 "No Wi-Fi Adapter Found" | 재부팅 필요, 개발 워크플로 중단 |
| 끊김 후 자동 재연결 없음 | 원격 관리가 무용지물이 됨 |
| 릴리스 노트에서 문제 인정 | NVIDIA 확인, 개별 사례 아님 |

> 💡 <strong>좋은 소식: 이러한 소프트웨어 수준의 문제가 당장 완전히 해결되지는 않겠지만, 간단하고 안정적이며 완벽하게 호환되는 하드웨어 해결책이 있습니다.</strong>

---

## DGX Spark만이 아닙니다 — 모든 GB10 AI Edge Server가 동일한 Wi-Fi 칩을 공유합니다

DGX Spark가 주목받는 이유는 단지 NVIDIA 자체 브랜드이고 가장 먼저 출하되었기 때문입니다. 하지만 실상은 <strong>NVIDIA GB10 Grace Blackwell Superchip을 탑재한 모든 AI Edge Server</strong>가 정확히 동일한 <strong>MediaTek MT7925 Wi-Fi 7 칩</strong>을 사용한다는 것입니다 — 동일한 드라이버 스택, 동일한 `wpa_supplicant` 한계, 동일한 호환성 문제를 갖습니다.

현재 시장에는 여섯 종의 GB10 AI Edge Server가 출시되어 있습니다:

### GB10 AI Edge Server 전체 사양 비교

모든 모델은 다음 핵심 사양을 공유합니다:

| 구성 요소 | 사양 |
|----------|------|
| Superchip | <strong>NVIDIA GB10 Grace Blackwell</strong> |
| CPU | <strong>20코어 Arm</strong> (10× Cortex-X925 + 10× Cortex-A725) |
| GPU | <strong>NVIDIA Blackwell GPU</strong>, 5세대 Tensor Core / 4세대 RT Core |
| AI 성능 | <strong>1 PFLOP FP4</strong> (1000 TOPS AI) |
| 시스템 메모리 | <strong>128 GB LPDDR5x</strong> 통합, 256-bit, 273 GB/s 대역폭 |
| 메모리 인터커넥트 | <strong>NVLink-C2C</strong> (PCIe 5.0 대비 5배 대역폭) |
| NIC | <strong>NVIDIA ConnectX-7</strong> SmartNIC (200G × 2 QSFP) |
| 이더넷 | <strong>1× 10GbE RJ-45</strong> |
| Wi-Fi 칩 | <strong>MediaTek MT7925</strong> Wi-Fi 7 (2×2) |
| 디스플레이 출력 | <strong>1× HDMI 2.1a</strong> |
| 운영 체제 | <strong>NVIDIA DGX OS</strong> (Ubuntu Linux 기반) |
| 전원 공급 | <strong>240W</strong> USB-C 외장 어댑터 |
| 듀얼 유닛 스태킹 | 지원 (최대 405B 파라미터 모델) |

브랜드별 차이는 다음과 같습니다:

| 기능 | <strong>ASUS ASCENT GX10</strong> | <strong>MSI EdgeXpert</strong> | <strong>NVIDIA DGX Spark</strong> | <strong>HP ZGX Nano G1n</strong> | <strong>ALTOS BrainSphere GB10 F1</strong> | <strong>GIGABYTE AI TOP ATOM</strong> |
|------|----------------------|-------------------|----------------------|---------------------|------------------------------|--------------------------|
| 스토리지 | 1TB / 2TB / 4TB NVMe | 1TB / 4TB NVMe | 1TB / 4TB NVMe | 1TB / 2TB / 4TB NVMe | 4TB NVMe | 1TB / 4TB NVMe (Gen5 최대) |
| Wi-Fi 모듈 | AW-EM637 (Wi-Fi 7) | Wi-Fi 7 | Wi-Fi 7 | MT7925 (Wi-Fi 7) | Wi-Fi 7 | Wi-Fi 7 |
| Bluetooth | BT 5.4 | BT 5.3 | BT 5.4 | BT 5.4 | BT 5.4 LE | BT 5.4 |
| USB | 4× USB 3.2 Gen 2×2 Type-C | 4× USB 3.2 Type-C | 4× USB Type-C | 4× USB Type-C | 4× USB 3.2 Gen 2×2 Type-C | 4× USB 3.2 Gen 2×2 Type-C |
| 크기 | 150×150×51mm | 151×151×52mm | 150×150×50.5mm | 150×150×51mm | 150×150×50mm | 150×150×50.5mm |
| 무게 | 1.48 kg | 1.2 kg | 1.2 kg | 1.25 kg | < 1.5 kg | 1.2 kg |
| 번들 소프트웨어 | — | — | — | HP ZGX Toolkit | Altos aiGeni Platform | — |

> ⚠️ <strong>결론</strong>: 어떤 GB10 AI Edge Server를 구매했든, 내장 Wi-Fi는 동일한 MediaTek MT7925 칩이며, 모두 동일한 연결 문제를 겪을 수 있습니다. 아래의 ALFA USB 어댑터 솔루션은 <strong>여섯 모델 모두에서 작동할 것으로 예상됩니다</strong>(ASUS GX10에서만 실측했으며, 다른 기종은 개별적으로 테스트하지 않았습니다).

---

## 해결책: USB Wi-Fi 어댑터 하나, 10분

NVIDIA는 DGX OS(Ubuntu 24.04 기반)만 공식적으로 테스트합니다. <strong>모든 GB10 플랫폼은 ARM64(aarch64) 아키텍처</strong>를 사용하며 Kernel <strong>버전 6.17 이상</strong>을 탑재합니다.

이는 USB Wi-Fi 어댑터가 세 가지 요건을 충족해야 함을 의미합니다:

1. ✅ <strong>커널 내장 Linux 드라이버</strong> — 컴파일 불필요, DKMS 불필요
2. ✅ <strong>완전한 ARM64(aarch64) 지원</strong> — GB10에서 플러그 앤 플레이
3. ✅ <strong>검증된 안정성</strong> — 커뮤니티에서 폭넓게 검증됨

ALFA 현행 USB 네트워크 카드 9종은 GX10에서 실측한 kernel 6.17에서 이 세 가지를 모두 충족합니다(GX10 실측, 글 끝의 "다른 ALFA 네트워크 카드" 참조). 이 글에서는 관리용 네트워크에 가장 적합한 AWUS036ACM을 예로 듭니다.

### 🥇 추천: ALFA AWUS036ACM

| 항목 | 세부 정보 |
|------|------|
| 칩셋 | <strong>MediaTek MT7612U</strong> |
| 드라이버 | <strong>Linux Kernel 내장 mt76</strong> (Kernel 4.19부터) |
| 밴드 | 듀얼 밴드 2.4GHz + 5GHz (AC1200) |
| 안테나 | 2× RP-SMA 분리형 5dBi (업그레이드 가능) |
| 인터페이스 | USB 3.0 Type-A |
| 모니터 모드 | ✅ 완전 지원 |
| AP 모드 | ✅ 지원 |
| TAA 준수 | ✅ 미국 정부 조달 기준 충족 |

#### 왜 이 제품인가? 여섯 가지 이유

<strong>1. 드라이버 불필요 플러그 앤 플레이</strong>

mt76 드라이버는 버전 4.19부터 메인라인 Linux Kernel에 포함되어 있습니다. DGX Spark의 Kernel 6.17은 이를 기본 지원합니다. USB 포트에 꽂으면 시스템이 <strong>드라이버를 자동으로 로드합니다</strong> — 아무것도 설치하지 않습니다.

<strong>2. ARM64 실측 검증</strong>

MT7612U는 수년간 ARM 플랫폼에서 철저히 검증되었습니다 — Raspberry Pi OS(aarch64), Ubuntu Server(ARM64) 등. 저희도 GB10 플랫폼인 ASUS GX10(kernel 6.17)에서 실측했으며, 꽂으면 `mt76x2u`가 자동으로 로드되고 패치가 전혀 필요 없었습니다.

<strong>3. 무컴파일, 무설정</strong>

mt76 드라이버는 수년 전부터 메인라인에 포함되어 있어, DGX OS Kernel을 업데이트해도 ACM은 그대로 플러그 앤 플레이로 작동합니다. (Realtek 모델도 kernel 6.17에서는 마찬가지로 컴파일이 필요 없습니다. 카드마다 최소 버전이 다르며, 그보다 낮은 경우에만 DKMS가 필요합니다.)

<strong>4. 모니터 모드 및 패킷 인젝션 지원</strong>

DGX Spark에서 보안 연구를 위해 Kali Linux VM을 실행할 계획이라면, ACM은 모니터 모드, 패킷 인젝션, 가상 인터페이스(VIF)를 지원합니다. GX10 실측 인젝션 성공률은 2.4GHz 63–83%, 5GHz 76%였으며, 인젝션이 주 용도라면 AWUS036EACS, ACH(두 대역 100%)가 더 우수합니다.

<strong>5. 교체형 안테나</strong>

두 개의 RP-SMA 분리형 안테나를 제공합니다. 5dBi로 출하되며, 필요에 따라 7dBi 또는 9dBi 고이득 안테나로 교체할 수 있습니다 — Wi-Fi 신호가 약한 서버실이나 공장의 엣지 배치에 이상적입니다.

<strong>6. TAA 준수</strong>

조직에 정부 조달 요건이 있다면, ALFA AWUS036ACM은 <strong>TAA 준수</strong>를 갖춘 몇 안 되는 외장 USB Wi-Fi 어댑터 중 하나입니다.

---

## 실전: "무선 없음"에서 10분 만에 듀얼 네트워크로

DGX Spark에서 ALFA AWUS036ACM을 사용하는 전체 워크플로는 다음과 같습니다:

### 1단계: USB 어댑터 꽂기

DGX Spark의 USB 포트는 모두 USB-C이므로, 데이터 전송을 지원하는 USB-C to USB-A 어댑터를 통해 AWUS036ACM을 꽂습니다.

터미널을 열고 실행합니다:

```bash
dmesg | tail -20
```

다음과 유사한 출력이 보여야 합니다:

다음은 ASUS GX10(kernel 6.17.0-1014-nvidia)에서 AWUS036ACM으로 실측한 dmesg 출력입니다(MAC 주소는 가림 처리):

```
usb 5-1: new high-speed USB device number 2 using xhci-hcd
usb 5-1: New USB device found, idVendor=0e8d, idProduct=7612, bcdDevice= 1.00
mt76x2u 5-1:1.0: ASIC revision: 76120044
mt76x2u 5-1:1.0: ROM patch build: 20141115060606a
mt76x2u 5-1:1.0: Firmware Version: 0.0.00
usbcore: registered new interface driver mt76x2u
mt76x2u 5-1:1.0 wlxXXXXXXXXXXXX: renamed from wlan0
```

<strong>이것이 드라이버가 자동으로 로드되었다는 신호입니다.</strong> 아무것도 설치하지 않았습니다.

### 2단계: 어댑터 인식 확인

```bash
nmcli device status
```

`wlan1`(또는 `wlx...`)이 상태 `disconnected`로 나열되어야 합니다.

### 3단계: Wi-Fi 연결

```bash
# 사용 가능한 네트워크 스캔
nmcli device wifi list

# SSID에 연결 ("MyLabWiFi"를 본인 것으로 교체)
sudo nmcli device wifi connect "MyLabWiFi" password "your-password"

# 연결 상태 확인
nmcli connection show --active
```

### 4단계: 부팅 시 자동 연결 활성화

앞 단계가 성공했다면 `nmcli`가 연결 프로필을 자동으로 저장합니다. 이후 부팅할 때마다 자동으로 연결됩니다.

프로필이 저장되었는지 확인합니다:

```bash
nmcli connection show
```

목록에 SSID가 보이면 완료입니다. USB를 꽂는 순간부터 안정적인 Wi-Fi까지 <strong>총 10분이 채 걸리지 않습니다</strong>.

---

## 진정한 AI 서버 네트워크 아키텍처는 이렇게 생겼습니다

AWUS036ACM을 사용하면 DGX Spark 네트워크 구성이 전문적인 <strong>듀얼 네트워크 아키텍처</strong>로 한 단계 발전합니다:

{{< mermaid >}}
%%{init:{"theme":"dark","themeVariables":{"primaryColor":"#2d1f4e","primaryTextColor":"#e2d9f3","primaryBorderColor":"#7c3aed","lineColor":"#9d6dff","secondaryColor":"#1a1030","tertiaryColor":"#0e0818","background":"#0e0818","mainBkg":"#1e1040","nodeBorder":"#7c3aed","clusterBkg":"#150d2a","titleColor":"#c4b5fd","edgeLabelBackground":"#1a1030","attributeBackgroundColorEven":"#1e1040","attributeBackgroundColorOdd":"#150d2a"}}}%%
flowchart TD
    subgraph sub1["🌐 네트워크 계층"]
        direction LR
        A["⚡ 10GbE / ConnectX-7<br/>모델 학습 · 대용량 데이터 전송"]
        B["📡 ALFA AWUS036ACM<br/>SSH 관리 · Jupyter · 시스템 업데이트"]
    end

    C["🖥️ DGX Spark / GB10<br/>ARM64 | 128GB | 20코어 CPU"]

    subgraph sub2["🎯 사용 사례"]
        D["🤖 AI 개발자<br/>추론 + SSH 병행"]
        E["🔐 보안 연구실<br/>LLM 학습 + 침투 테스트"]
        F["🚀 엣지 배치<br/>운영 네트워크 + 격리된 관리"]
    end

    A -->|고속 데이터| C
    B -->|관리 링크| C
    C --> D
    C --> E
    C --> F
{{< /mermaid >}}

<strong>트래픽을 분리하는 이유는?</strong>

AI 모델 학습은 사전 학습된 가중치 다운로드, 데이터셋 동기화, 분산 학습 통신 등 막대한 네트워크 트래픽을 발생시킵니다. 이를 동일한 링크에서 SSH 관리와 혼용하면:

- SSH 세션이 느려지거나 아예 타임아웃됩니다
- 10GbE 대역폭이 관리 트래픽에 낭비됩니다
- 기본 연결이 끊기면(예: 모델 다운로드가 멈출 때) 문제를 해결하기 위해 원격 접속조차 할 수 없습니다

분리하면 <strong>모델 워크로드와 관계없이 관리 연결이 안정적으로 유지됩니다</strong>.

---

## 세 가지 시나리오, 하나의 어댑터

### 시나리오 A: AI 개발자
```
10GbE → 모델 추론, 데이터 전송
ALFA ACM → SSH, Jupyter Notebook, 시스템 업데이트
```

### 시나리오 B: 보안 연구실 (자신이 소유하거나 승인을 받은 네트워크에서만)
```
GB10 → LLM 파인튜닝 실행
Kali Linux VM → USB 패스스루 ALFA ACM → 무선 침투 테스트
```

### 시나리오 C: 엣지 배치 (공장 / 창고)
```
10GbE → 운영 네트워크
ALFA ACM + 고이득 안테나 → 사무 관리용 Wi-Fi
```

---

## FAQ

<strong>Q: AWUS036ACM의 MT7612U와 GB10의 내장 MT7925는 둘 다 MediaTek인데, 같은 것 아닌가요?</strong>

A: 제조사는 같지만 드라이버 아키텍처는 완전히 다릅니다. MT7925는 아직 개선 중인 새로운 PCIe 인터페이스 드라이버인 `mt7925e`를 사용합니다. MT7612U는 Kernel 4.19부터 성숙해 온 `mt76` USB 드라이버를 사용하며 매우 안정적입니다.

<strong>Q: 이 어댑터는 DGX OS 외부에서도 작동하나요?</strong>

A: 물론입니다. MT7612U 드라이버는 메인라인 Linux Kernel의 일부입니다 — Ubuntu, Debian, Raspberry Pi OS, Kali Linux, Fedora, Arch Linux 등 Kernel 4.19 이상이면 무엇이든 가능합니다. 모두 플러그 앤 플레이입니다.

---

## 다른 ALFA 네트워크 카드: GX10 실측 결과

저희는 ASUS GX10(Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia)에서 ALFA 현행 네트워크 카드 9종을 실측했으며, 모두 커널 내장 드라이버를 사용해 꽂으면 바로 사용할 수 있고 DKMS가 필요 없습니다. 다른 GB10 기종(DGX Spark, MSI EdgeXpert, GIGABYTE AI TOP ATOM, ALTOS BrainSphere, HP ZGX Nano)은 동일한 GB10과 NVIDIA 커널 계열을 사용하므로 동작이 같을 것으로 예상되지만, 개별적으로 테스트하지는 않았습니다.

| 모델 | 칩 | 내장 드라이버 | 패킷 인젝션 (GX10 실측) | 적합한 용도 |
|------|------|----------|----------------------|----------|
| AWUS036ACM | MediaTek MT7612U | mt76x2u | ✅ 2.4G 63–83% / 5G 76% | 관리용 네트워크, AP, 침투 테스트 |
| AWUS036ACHM | MediaTek MT7610U | mt76x0u | ⚠️ 2.4G 96–100% / 5G 브로드캐스트만 | 관리용 네트워크, AP |
| AWUS036ACH | Realtek RTL8812AU | rtw88_8812au | ✅ 두 대역 100% | 침투 테스트, 장거리 수신 |
| AWUS036ACS | Realtek RTL8811AU | rtw88_8821au | ✅ 2.4G 100% / 5G 96% | 침투 테스트, 휴대용 |
| AWUS036EACS | Realtek RTL8821CU (블루투스 포함) | rtw88_8821cu | ✅ 두 대역 100% | 침투 테스트 |
| AWUS036AX | Realtek RTL8832BU | rtw89_8852bu | ✅ 2.4G 96% | Wi-Fi 6 연결, AP |
| AWUS036AXER | Realtek RTL8832BU | rtw89_8852bu | ✅ 2.4G 73% | Wi-Fi 6 연결, AP, 모니터 수신 |
| AWUS036AXM | MediaTek MT7921AUN | mt7921u | ❌ 실패 | 연결, AP 전용 |
| AWUS036AXML | MediaTek MT7921AUN | mt7921u | ❌ 실패 | 연결, AP 전용 (6GHz 실측 동작) |

AWUS036AXM / AXML은 stock kernel 6.17에서 패킷 인젝션에 실패하므로(monitor, AP, WPA3는 사용 가능) 침투 테스트에는 적합하지 않습니다. 카드마다 드라이버가 메인라인에 포함된 최소 kernel 버전이 다르며(ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), 그보다 낮은 경우에만 커뮤니티 DKMS 드라이버가 필요합니다. 전체 데이터는 [ALFA 네트워크 카드 9종 ARM64 실측 종합표](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)를 참조하시기 바랍니다.

---

{{< faq >}}

## 요약: 어떤 GB10이든 10분 만에 온라인으로

NVIDIA DGX Spark, ASUS ASCENT GX10, MSI EdgeXpert, HP ZGX Nano, ALTOS BrainSphere GB10 F1, GIGABYTE AI TOP ATOM 중 무엇을 구매했든 — 이 GB10 AI Edge Server들은 128GB 통합 메모리, 20코어 ARM CPU, ConnectX-7 200GbE 네트워킹을 갖춘 경이로운 AI 개발 머신입니다. 하지만 모두 동일한 MediaTek MT7925 Wi-Fi 칩을 공유하며, 모두 동일한 첫 단계에서 발목이 잡힐 수 있습니다.

ALFA AWUS036ACM 솔루션은 거의 어처구니없을 만큼 간단합니다: <strong>꽂으면 끝.</strong>

하지만 그 단순함이야말로 진정한 엔지니어링 생산성의 모습입니다 — 당신은 Wi-Fi 드라이버를 디버깅하고 있어서는 안 됩니다. 모델을 학습시켜야 합니다.

다른 방법과 비교하면 장점이 분명합니다:

| 방법 | 시간 | 신뢰성 | 유지 보수 |
|------|------|--------|---------|
| NVIDIA가 Wi-Fi 드라이버를 고칠 때까지 대기 | 불확실 (수개월?) | 불확실 | 낮음 |
| Wi-Fi 브리지 구매 | 설정 30분 | 중간 | 중간 |
| <strong>ALFA AWUS036ACM</strong> | <strong>< 10분</strong> | <strong>최고</strong> | <strong>없음</strong> |

10분, USB 어댑터 하나면 당신의 AI 서버가 진정으로 온라인이 됩니다.

---

> 📌 <strong>ALFA AWUS036ACM 지금 재고 보유</strong> → [Yopitek 제품 페이지](/ko/products/alfa/awus036acm/)
>
> Yopitek Ltd는 대만의 공인 ALFA Network 유통업체입니다
> 주문 또는 기술 문의: sales@yupitek.com

---

*출처: NVIDIA DGX Spark 릴리스 노트, NVIDIA 개발자 포럼, morrownr/USB-WiFi GitHub, ALFA Network 문서, Linux Kernel Wireless 문서*

## 참고 문헌

1. [NVIDIA DGX Spark 공식 문서](https://developer.nvidia.com/dgx-spark)
2. [NVIDIA 개발자 포럼](https://forums.developer.nvidia.com/)
3. [morrownr/USB-WiFi GitHub 프로젝트](https://github.com/morrownr/USB-WiFi)
4. [Linux Kernel Wireless 문서](https://wireless.wiki.kernel.org/)
5. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
