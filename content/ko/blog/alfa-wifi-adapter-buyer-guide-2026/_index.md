---
title: "ALFA Wi-Fi 어댑터 구매 가이드 2026: 나에게 맞는 모델은?"
description: "2026년 ALFA Network USB Wi-Fi 어댑터 완벽 구매 가이드. AWUS036ACH, ACM, ACS, AX, AXER, AXM, AXML, EACS를 드라이버 지원, 모니터 모드, OS 호환성, 가격 측면에서 비교합니다."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "ALFA 어댑터의 구매 기준은 무엇입니까?"
    answer: "선정 기준에는 칩셋 드라이버 성숙도, OS 호환성, 모니터 모드 지원, 송신 출력이 포함됩니다. RTL8812AU가 가장 성숙하고 안정적인 드라이버를 보유하고 있습니다."
  - question: "어떤 ALFA 어댑터가 모니터 모드를 지원합니까?"
    answer: "ACH, ACM, ACS, AX, AXER은 모니터 모드와 패킷 인젝션을 지원합니다. AXM과 AXML(MT7921AU)은 모니터 모드, AP, WPA3를 지원하지만 패킷 인젝션은 stock 커널 6.17 실측에서 실패했습니다(커널 6.16 이후 mac80211 chanctx 회귀 때문이며 칩 자체의 한계가 아닙니다. 인젝션이 된다는 커뮤니티 보고는 커널 6.16 이전 또는 patched 드라이버 기준이며, 펌웨어가 속도를 1/6 Mbps로 고정합니다). 인젝션이 필요하면 ACH, ACM, ACS, AX 또는 EACS를 사용하세요. EACS(RTL8821CU)는 커널 6.2 이상에 내장된 rtw88_8821cu 드라이버로 모니터 모드(2.4G/5G)와 인젝션(2.4G/5G 모두 100%)이 동작합니다(GX10 커널 6.17 실측)."
  - question: "Wi-Fi 6E/6 어댑터가 필요합니까?"
    answer: "감사 범위에 6GHz 대역이 포함되는 경우에만 필요합니다. AXML은 트라이밴드 AX3000을 지원하며 Linux 커널 5.18 이상과 firmware-misc-nonfree가 필요합니다."
  - question: "RTL8812AU와 MT7612U의 드라이버 설치 차이는 무엇입니까?"
    answer: "RTL8812AU는 DKMS 컴파일이 필요하며 커널 업데이트 후 재빌드가 필요할 수 있습니다. MT7612U는 커널 4.19부터 메인라인 커널에 포함되어 있어 컴파일 없이 플러그 앤 플레이로 동작합니다."
  - question: "2026년 가장 추천하는 ALFA 어댑터는 무엇입니까?"
    answer: "레드팀 운용에는 AWUS036ACH(500mW 듀얼 안테나)를 추천합니다. 예산이 제한적이라면 AWUS036ACM, 엔터프라이즈 6E 환경에는 AWUS036AXML을 추천합니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-network", "wifi-adapter", "buyer-guide", "kali-linux", "penetration-testing", "monitor-mode"]
featureimage: "/images/blog/alfa-wifi-adapter-buyer-guide-2026.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

이 가이드는 2026년에 적합한 ALFA Network USB Wi-Fi 어댑터를 선택해야 하는 네트워크 보안 엔지니어, 엔터프라이즈 IT 전문가, 레드팀 운용자를 위해 불필요한 정보를 걷어내고 핵심만 정리합니다. 현행 생산 중인 8개 모델 전체 — [AWUS036ACS](/ko/products/alfa/awus036acs/), [AWUS036ACH](/ko/products/alfa/awus036ach/), [AWUS036ACM](/ko/products/alfa/awus036acm/), [AWUS036EACS](/ko/products/alfa/awus036eacs/), [AWUS036AX](/ko/products/alfa/awus036ax/), [AWUS036AXER](/ko/products/alfa/awus036axer/), [AWUS036AXM](/ko/products/alfa/awus036axm/), [AWUS036AXML](/ko/products/alfa/awus036axml/) — 을 다루며, 칩셋, 드라이버 성숙도, OS 지원, 실제 활용 사례를 비교합니다. 드라이버 문제 해결에 쓰는 시간을 줄이고 실제 업무에 더 집중할 수 있도록 돕습니다.

{{< tldr >}}
AWUS036ACH는 2026년 레드팀을 위한 선택입니다. 가장 성숙한 RTL8812AU 드라이버를 갖춘 500mW 듀얼 안테나 AC1200 모델입니다. 예산이 제한적이라면 AWUS036ACM을, 엔터프라이즈 6E 환경에는 AWUS036AXML(AX3000 트라이밴드)을 선택하십시오.
{{< /tldr >}}

---

## 선택 방법: 4가지 핵심 질문

제품 페이지를 열기 전에 다음 네 가지 질문에 답하십시오. 이 답변만으로도 대부분의 후보군을 즉시 추려낼 수 있습니다.

### (a) 어떤 OS를 사용하고 있습니까?

드라이버 지원이 가장 중요합니다. 최신 커널에서 Kali Linux와 Ubuntu를 사용하는 사용자는 가장 폭넓은 선택지를 갖습니다. macOS 지원은 모든 모델에서 빈약합니다. Windows 10/11은 대체로 잘 지원됩니다. Raspberry Pi 또는 ARM 기반 플랫폼을 사용하는 경우 칩셋 선택이 매우 중요합니다.

- **Kali Linux / Debian:** RTL8812AU(`dkms-rtl8812au`)와 MT7921AUN(커널 네이티브 ≥ 5.18)이 침투 테스트를 위한 두 가지 주요 칩셋 계열입니다.
- **Ubuntu 22.04 / 24.04:** 동일한 드라이버 환경이지만, MT7921AUN의 경우 HWE 커널이나 `firmware-misc-nonfree` 설치가 필요할 수 있습니다.
- **Windows 10/11:** ALFA는 현행 전 모델에 대해 서명된 드라이버를 제공합니다. 설치 과정이 간단합니다.
- **macOS Sonoma:** 커뮤니티가 유지보수하는 kext를 지원하는 어댑터는 극소수에 불과합니다. 어려움이 예상되므로 VM 워크플로를 계획하십시오.
- **Raspberry Pi (Kali NetHunter, ARM):** RTL8812AU 모델(ACH)과 MT7612U 모델(ACM)이 안전한 선택입니다. MT7921AUN도 동작할 수 있으나 `firmware-misc-nonfree` 패키지와 충분히 최신인 커널이 필요합니다.

### (b) 모니터 모드와 패킷 인젝션이 필요합니까?

답이 '예'라면 — 그리고 침투 테스트나 무선 감사 작업이라면 당연히 '예'여야 합니다 — 이 가이드의 대부분의 모델이 해당 요구를 충족합니다. [AWUS036EACS](/ko/products/alfa/awus036eacs/)(RTL8821CU)도 커널 6.2 이상에서는 내장 rtw88_8821cu 드라이버로 모니터 모드와 패킷 인젝션이 가능합니다(GX10 커널 6.17 실측). 예외: AXM과 AXML(MT7921AU)은 모니터 모드를 지원하지만, 패킷 인젝션은 커널 6.16 이상(실측 6.17)에서 실패했습니다. 아래 AXML 참고 사항을 확인하세요.

### (c) VM입니까, 베어메탈입니까?

VirtualBox와 VMware의 USB 패스스루는 복잡성을 한 단계 더합니다. 이 목록의 어떤 어댑터든 패스스루가 적절히 구성되면 동작하지만, RTL8812AU 어댑터(ACH)와 MT7612U 어댑터(ACM)가 VM 환경에서 가장 오랜 검증 이력을 갖고 있습니다. VM으로만 패스스루하는 경우, 런타임에 로드되는 펌웨어 파일에 의존하는 어댑터는 피하십시오 — USB 연결이 끊기면 펌웨어도 사라집니다.

전체 설정 방법은 [VirtualBox 및 VMware에서 ALFA 어댑터 설정](/ko/blog/alfa-adapter-virtualbox-vmware-usb/)을 참조하십시오.

### (d) 예산은 어떻게 됩니까?

Wi-Fi 5 세대(ACH, ACM, ACS)는 더 저렴하고 드라이버가 더 안정적이며, 예산에 제약이 있거나 드라이버 안정성이 최우선인 경우 올바른 선택입니다. Wi-Fi 6/6E 세대(AX, AXER, AXM, AXML)는 하드웨어가 향하고 있는 방향이지만, 더 높은 비용을 지불하고 메인라인이 아닌 커널에서 일부 드라이버의 예외 상황을 감수해야 합니다.

---

## ALFA 어댑터 전체 비교표

<div style="overflow-x: auto;">

| 모델 | Wi-Fi 세대 | 칩 | 최대 속도 | 모니터 모드 | Kali 드라이버 | Windows | macOS | 안테나 | 최적 용도 |
|---|---|---|---|---|---|---|---|---|---|
| [AWUS036ACS](/ko/products/alfa/awus036acs/) | Wi-Fi 5 | RTL8811AU | AC600 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 1× RP-SMA | 경량 휴대 키트 |
| [AWUS036ACH](/ko/products/alfa/awus036ach/) | Wi-Fi 5 | RTL8812AU | AC1200 | ✅✅ 최상 | rtl8812au-dkms | ✅ | ⚠️ | 2× RP-SMA | 레드팀 운용 |
| [AWUS036ACM](/ko/products/alfa/awus036acm/) | Wi-Fi 5 | MT7612U | AC1200 | ✅ | mt76x2u (≥4.19) | ✅ | ⚠️ | 2× RP-SMA | Linux 플러그 앤 플레이 |
| [AWUS036EACS](/ko/products/alfa/awus036eacs/) | Wi-Fi 5 | RTL8821CU | AC1200 | ✅ | rtw88_8821cu (커널 ≥6.2) | ✅ | ⚠️ | 내장 2dBi | 일반 사용 + 인젝션/침투 테스트 + Bluetooth 콤보 |
| [AWUS036AX](/ko/products/alfa/awus036ax/) | Wi-Fi 6 | RTL8832BU | AX1200 | ✅ (6.17+) | OOK (<6.17) | ✅ | ❌ | 2× RP-SMA | Windows Wi-Fi 6 |
| [AWUS036AXER](/ko/products/alfa/awus036axer/) | Wi-Fi 6 | RTL8832BU | AX1800 | ✅ (6.17+) | OOK (<6.17) | ✅ | ❌ | 내장 나노 | 소형 휴대 어댑터 |
| [AWUS036AXM](/ko/products/alfa/awus036axm/) | Wi-Fi 6E | MT7921AUN | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 2× RP-SMA | Wi-Fi 6E + 듀얼 안테나 |
| [AWUS036AXML](/ko/products/alfa/awus036axml/) | Wi-Fi 6E | MT7921AUN | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 2× RP-SMA | Wi-Fi 6E + Linux + USB-C |

</div>

**범례:** ✅ 지원 · ⚠️ 제한적/부분 지원 · ❌ 미지원

{{< alert "circle-info" >}}
**macOS 참고:** 모든 ALFA 어댑터는 macOS Ventura 및 Sonoma에서 드라이버 문제에 직면합니다. 가장 일반적으로 커뮤니티가 유지보수하는 방법은 USB 패스스루와 함께 VM에서 Kali Linux를 실행하는 것입니다. AWUS036EACS(RTL8821CU)는 표준 클라이언트 연결을 위해 서드파티 드라이버를 통해 macOS에서 동작할 수 있지만, macOS 기본 드라이버로는 모니터 모드를 사용할 수 없습니다(Linux에서는 실측으로 동작).
{{< /alert >}}

---

## Wi-Fi 5 어댑터 (드라이버 성숙도 최상)

Wi-Fi 5 세대는 수년간의 커뮤니티 개발이 뒷받침되어 왔습니다. 확고한 드라이버 안정성이 우선이라면 — 특히 CTF 작업, 전문 감사, 또는 커널 업데이트 후 드라이버가 깨지는 상황을 감당할 수 없는 환경이라면 — 여기서 시작하십시오.

### AWUS036ACH — 레드팀 표준

[AWUS036ACH](/ko/products/alfa/awus036ach/)는 보안 커뮤니티에서 가장 널리 배포된 ALFA 어댑터로서, 그만한 이유가 있습니다. RTL8812AU 칩셋은 `aircrack-ng/rtl8812au` 드라이버의 지원을 받으며, 이 드라이버는 수년간 모든 주요 Kali Linux 릴리스에 대해 유지보수되고 테스트되어 왔습니다.

**하드웨어 사양:**
- 칩셋: RTL8812AU (Realtek)
- 탈착식 RP-SMA 안테나 커넥터 2개 — 전체 ALFA 안테나 라인업과 호환
- 500mW 송신 출력 — Wi-Fi 5 라인업 중 최고
- 듀얼 밴드: 2.4GHz 및 5GHz

**레드팀에서 선두를 지키는 이유:** 500mW 송신 출력과 듀얼 외장 안테나, 그리고 성숙한 인젝션 지원이 결합되어, 안정적인 프레임 전달을 유지하면서 원거리 작업이 가능합니다. 기본 무지향성 안테나를 [APA-M25](/ko/products/alfa/apa-m25/) 지향성 패널로 교체하면 본격적인 장거리 플랫폼이 됩니다. 2안테나 폼팩터는 대상 네트워크에 연결될 때 적절한 2T2R MIMO도 가능하게 합니다.

**Kali에서의 드라이버 설치:**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
```

{{< alert "triangle-exclamation" >}}
커널 ≥ 6.2에서는 구형 Kali 이미지에 포함된 기본 `rtl8812au` 모듈이 로드에 실패할 수 있습니다. 항상 Kali 저장소의 `dkms-rtl8812au`를 설치하십시오 — 이 패키지는 커널 변경을 추적하고 DKMS를 통해 커널 업데이트 시 자동으로 재빌드합니다.
{{< /alert >}}

### AWUS036ACM — Linux 플러그 앤 플레이 선택

[AWUS036ACM](/ko/products/alfa/awus036acm/)은 MediaTek MT7612U 칩셋을 사용하며, 이는 ACH의 RTL8812AU와는 다른 계열입니다. 가장 큰 장점은 커널 4.19부터 `mt76x2u` 드라이버로 메인라인 Linux 커널에 지원된다는 점으로, 현대의 모든 Kali Linux나 Ubuntu 시스템에서 드라이버 컴파일이 전혀 필요 없습니다. 듀얼 안테나 운용을 위해 RP-SMA 커넥터 2개를 탑재하고 있습니다.

기능적으로 모니터 모드와 인젝션 지원은 보안 작업에 완전히 적합합니다.

안테나 포트 하나만 필요하고 ACH의 확장된 송신 출력이 필요하지 않다면, ACM은 더 적은 비용으로 동일한 활용 사례를 커버합니다. 감사 팀을 위해 어댑터를 대량 구매하는 키트 배포 환경에서 흔히 선택됩니다.

**ACH 대신 ACM을 선택해야 할 때:** 번거로움 없는 Linux 드라이버 설정, Ubuntu/Kali에서 컴파일 없는 플러그 앤 플레이, ACH보다 낮은 가격대에서의 듀얼 안테나 커버리지가 필요한 경우입니다.

### AWUS036ACS — 경량 및 휴대성

[AWUS036ACS](/ko/products/alfa/awus036acs/)는 RTL8811AU 칩셋을 사용합니다. 송신 출력 면에서 RTL8812AU보다 한 단계 낮지만, 여전히 모니터 모드와 패킷 인젝션을 완전히 수행할 수 있습니다. 소형 폼팩터와 단일 안테나는, 공항 보안 검색대에서 여러 개의 RP-SMA 안테나를 관리하고 싶지 않은 출장이 잦은 컨설턴트에게 휴대용 선택이 됩니다.

RTL8811AU 드라이버는 Kali에서 동일한 `rtl8812au-dkms` 패키지를 공유하므로 설치 워크플로가 동일합니다.

**ACH/ACM 대비 절충점:** 더 낮은 송신 출력(원거리 도달 범위 감소), 단일 안테나(MIMO 없음), AC1200 대비 AC600 최대 처리량. 대부분의 캡처 및 인젝션 워크플로에서는 이러한 차이가 무의미합니다. 다만 장거리 운용에서는 중요합니다.

### AWUS036EACS — 일반 용도 + 인젝션 가능(커널 6.2 이상) + Bluetooth 콤보

[AWUS036EACS](/ko/products/alfa/awus036eacs/)는 Realtek RTL8821CU 칩셋으로 구동됩니다. RTL8821CU는 Linux 커널 6.2부터 메인라인 rtw88_8821cu 드라이버가 내장되어 있습니다. GX10(Ubuntu 24.04 ARM64, 커널 6.17)에서 모니터 모드(2.4G/5G), 인젝션(2.4G/5G 모두 100%), WPA handshake 종단 간 캡처(.22000)가 모두 성공했고, Bluetooth와 Wi-Fi 동시 사용도 가능했습니다. 이 어댑터는 Windows 클라이언트 연결용으로 설계되었고 Bluetooth 4.2를 포함합니다.

{{< alert "triangle-exclamation" >}}
**커널 6.2 이전의 오래된 커널에서는 rtw88_8821cu가 없으므로 morrownr/8821cu 같은 커뮤니티 드라이버가 필요합니다.** 커널 6.2 이상에서는 별도 설치 없이 모니터 모드와 인젝션을 사용할 수 있습니다. 일반 무선 연결, DJI 드론 컨트롤러 거리 확장, Bluetooth 콤보가 필요한 Windows 우선 배포뿐 아니라, 소형 폼팩터의 인젝션/침투 테스트용으로도 적합합니다(안테나는 내장형 2dBi).
{{< /alert >}}

이 제품이 목록에 포함된 이유는 Bluetooth 4.2 콤보 기능, Windows 기본 지원, 그리고 커널 6.2 이상 Linux에서의 모니터/인젝션 지원 때문입니다. macOS에서는 커뮤니티 RTL8821CU 드라이버 지원이 제한적이며, macOS 기본 드라이버로는 모니터 모드를 사용할 수 없습니다.

---

## Wi-Fi 6 어댑터 (Windows 중심)

Wi-Fi 6(802.11ax)은 고밀도 환경 성능, 대상이 많은 MU-MIMO 시나리오, 그리고 네트워크 식별을 위한 BSS Coloring에서 의미 있는 개선을 가져왔습니다. AWUS036AX와 AWUS036AXER는 ALFA의 Wi-Fi 6 어댑터로, 주로 Windows 연결용으로 설계되었습니다.

두 Wi-Fi 6 ALFA 어댑터 모두 Realtek RTL8832BU 칩셋을 사용합니다. Linux에서 RTL8832BU는 커널 6.17부터 커널 내장 `rtw89_8852bu` 드라이버로 지원됩니다. ASUS GX10(Ubuntu 24.04 / kernel 6.17) 실측에서 모니터 모드는 2.4GHz와 5GHz 모두 동작하며 패킷 인젝션도 가능합니다(2.4GHz: AX 96%, AXER 73%, 5GHz 사용 가능). 6.17 미만 커널에서는 커널 외부(OOK) 커뮤니티 DKMS 드라이버가 필요하며, 이 경우 모니터 모드가 제한될 수 있습니다. (참고: AXML은 커널 6.16 이상에서 인젝션이 되지 않습니다. 아래 AXML 참고 사항 참조.)

### AWUS036AX — Wi-Fi 6 Windows 어댑터

[AWUS036AX](/ko/products/alfa/awus036ax/)는 탈착식 RP-SMA 안테나 2개를 갖춘 ALFA의 Wi-Fi 6 어댑터입니다. 2.4GHz 및 5GHz 대역에서 AX1200 속도를 제공하며 Windows 10/11 연결에 적합합니다.

**드라이버 상태:**
- Windows: ALFA 제공 드라이버를 통한 완전 지원
- Linux 커널 ≥ 6.17: 커널 내장 RTL8832BU 드라이버
- Linux 커널 < 6.17: 커널 외부 드라이버 필요
- 모니터 모드: ✅ 커널 6.17 이상에서 동작 (구형 커널의 커뮤니티 DKMS 드라이버에서는 제한될 수 있음)
- 패킷 인젝션: ✅ 커널 6.17 이상에서 동작 (실측 2.4GHz: AX 96%, AXER 73%)

{{< alert "triangle-exclamation" >}}
**Linux 침투 테스트 참고:** AWUS036AX는 RTL8832BU 칩셋을 사용하며, Linux 커널 6.17 이상(내장 rtw89_8852bu, Ubuntu 24.04 / kernel 6.17 실측)에서는 모니터 모드와 패킷 인젝션이 모두 동작합니다. 커뮤니티 DKMS 드라이버를 쓰는 구형 커널에서만 모니터 모드가 제한될 수 있으므로 먼저 `uname -r`로 커널 버전을 확인하십시오. (참고: AXML은 커널 6.16 이상에서 인젝션이 되지 않습니다. 아래 AXML 참고 사항 참조.)
{{< /alert >}}

### AWUS036AXER — 소형 휴대용 Wi-Fi 6 어댑터

[AWUS036AXER](/ko/products/alfa/awus036axer/)는 AWUS036AX와 동일한 RTL8832BU 칩셋을 사용하지만 초소형 나노 폼팩터(10.5g)로 제공됩니다. 드라이버 상황은 동일합니다 — 같은 RTL8832BU, 같은 Linux 지원 상태와 실측 결과, 같은 Windows 호환성입니다.

휴대성이 결정적 요소일 때 AX보다 AXER를 선택하십시오: 출장, 최소 공간 구성, 또는 풀사이즈 어댑터보다 소형 동글이 선호되는 상황에 적합합니다.

---

## Wi-Fi 6E 어댑터 (미래 대비)

Wi-Fi 6E는 802.11ax를 6GHz 대역으로 확장하여 새로운 5.925–7.125GHz 스펙트럼에 대한 접근을 제공합니다. 실제로 이는 간섭 감소, 더 넓은 채널 폭(최대 160MHz), 그리고 구형 장비가 볼 수도 도달할 수도 없는 대역에 대한 접근을 의미합니다. 엔터프라이즈 네트워크가 Wi-Fi 6E 인프라를 배포함에 따라, 감사자는 전체 공격 표면을 평가하기 위해 6E 지원 어댑터가 필요합니다.

두 Wi-Fi 6E ALFA 어댑터 모두 6GHz 지원을 위해 커널 ≥ 5.18이 필요합니다. 6GHz 대역은 규제 도메인이 올바르게 설정되어야 하며, 대부분의 관할권에서 6GHz에 대한 규제 집행은 2.4/5GHz보다 더 엄격합니다.

### AWUS036AXM — Wi-Fi 6E 진입점

[AWUS036AXM](/ko/products/alfa/awus036axm/)은 사양상 6GHz를 포함한 트라이밴드(Wi-Fi 6E)를 지원하는 MT7921AUN 칩셋을 사용합니다(6GHz는 본 사이트에서 AXM으로 실측하지 않았으며, AXML은 6GHz 실측 완료). 2T2R 듀얼 안테나 운용을 위해 RP-SMA 커넥터 2개를 탑재하고 있습니다.

주로 2.4 및 5GHz 환경에서 작업하지만 플래그십 가격을 지불하지 않고도 신흥 네트워크 평가를 위한 6GHz 기능을 원하는 운용자에게 AXM은 논리적인 진입점입니다.

**대역 커버리지:** 2.4GHz, 5GHz, 6GHz (트라이밴드)
**안테나:** 2× RP-SMA — 호환되는 모든 ALFA 안테나로 교체 가능

### AWUS036AXML — 플래그십 6E 어댑터

[AWUS036AXML](/ko/products/alfa/awus036axml/)은 ALFA의 현행 플래그십 어댑터입니다. MT7921AUN 칩셋, USB-C 3.2 연결, Bluetooth 5.2, 그리고 단일 고이득 RP-SMA 커넥터를 특징으로 합니다.

**주요 사양:**
- 칩셋: MT7921AUN (MediaTek)
- RP-SMA 커넥터 1개 — 전체 ALFA 안테나 라인업과 호환
- 트라이밴드: 2.4GHz + 5GHz + 6GHz
- AX3000 등급 (대역 전체에서 이론상 최대 3000Mbps)
- USB-C 3.2 — USB-A 대비 더 빠른 호스트 버스 대역폭

**AXML 드라이버 참고:**
- MT7921AUN은 커널 ≥ 5.18에서 `mt7921u` 드라이버 계열로 지원됩니다
- 모니터 모드가 지원되지만, 펌웨어를 사용한 액티브 모니터는 일부 커널에서 펌웨어 재시작 문제를 보였습니다 — 전체 테스트 데이터는 [AWUS036AXML 상세 리뷰](/ko/blog/awus036axml-wifi-6e-review/)를 참조하십시오
- 모니터 모드의 6GHz 대역은 규제 도메인이 6GHz 채널에서의 수동 스캔을 허용해야 합니다

{{< alert "triangle-exclamation" >}}
**AWUS036AXML 펌웨어 참고:** 6.1 미만 커널에서 일부 사용자는 AXML을 모니터 모드와 관리 모드 사이에서 반복적으로 전환할 때 펌웨어 충돌을 경험합니다. 워크플로가 빈번한 모드 전환을 요구한다면, 커널 ≥ 6.1을 실행하고 최신 `firmware-misc-nonfree` 패키지를 설치하십시오. **인젝션 참고:** AXM/AXML의 패킷 인젝션 커뮤니티 보고는 커널 6.16 이전 기준입니다. stock 커널 6.16 이상(실측 6.17, ASUS GX10, Ubuntu 24.04 ARM64)에서는 모니터, AP, WPA3, VIF는 동작하지만 인젝션 테스트가 실패하여(aireplay-ng --test: Found 0 APs / No Answer) deauth와 handshake 캡처가 불가능합니다. 원인은 mac80211 chanctx 회귀이며 칩 자체의 한계가 아닙니다. patched 드라이버로 인젝션이 동작하지만 펌웨어가 속도를 고정합니다(1/6 Mbps, HT/VHT 인젝션 불가). 인젝션이 필요하면 ACH, ACM, ACS 또는 AX를 사용하세요.
{{< /alert >}}

---

## 드라이버 호환성 심층 분석

<div style="overflow-x: auto;">

| 모델 | 칩 | Kali 패키지 | Ubuntu HWE | RPi ARM | Windows 10/11 |
|---|---|---|---|---|---|
| [AWUS036ACS](/ko/products/alfa/awus036acs/) | RTL8811AU | `dkms-rtl8812au` | 수동 빌드 | ✅ rtl8812au-dkms | ✅ ALFA 드라이버 |
| [AWUS036ACH](/ko/products/alfa/awus036ach/) | RTL8812AU | `dkms-rtl8812au` | 수동 빌드 | ✅ rtl8812au-dkms | ✅ ALFA 드라이버 |
| [AWUS036ACM](/ko/products/alfa/awus036acm/) | MT7612U | `mt76x2u` (커널 내장) | 커널 내장 ≥4.19 | ✅ 네이티브 | ✅ ALFA 드라이버 |
| [AWUS036EACS](/ko/products/alfa/awus036eacs/) | RTL8821CU | `rtw88_8821cu` (커널 ≥6.2 내장) | 커널 내장 ≥6.2 | ⚠️ 커널 ≥6.2 필요(Pi 미실측) | ✅ ALFA 드라이버 |
| [AWUS036AX](/ko/products/alfa/awus036ax/) | RTL8832BU | OOK (<6.17) | OOK (<6.17) | ⚠️ 제한적 | ✅ ALFA 드라이버 |
| [AWUS036AXER](/ko/products/alfa/awus036axer/) | RTL8832BU | OOK (<6.17) | OOK (<6.17) | ⚠️ 제한적 | ✅ ALFA 드라이버 |
| [AWUS036AXM](/ko/products/alfa/awus036axm/) | MT7921AUN | `firmware-misc-nonfree` | 커널 내장 ≥5.18 | ✅ 펌웨어 필요 | ✅ ALFA 드라이버 |
| [AWUS036AXML](/ko/products/alfa/awus036axml/) | MT7921AUN | `firmware-misc-nonfree` | 커널 내장 ≥5.18 | ✅ 펌웨어 필요 | ✅ ALFA 드라이버 |

</div>

**RTL8812AU 커널 이력:** RTL8812AU 드라이버는 Linux 5.2에서 메인라인 커널에 부분적으로 통합되었으나, 모니터 모드와 인젝션이 없는 등 상당한 제약이 있었습니다. 완전한 침투 테스트 기능을 위해서는 Kali에서 `dkms-rtl8812au`로 패키징된 아웃 오브 트리 `rtl8812au` 드라이버가 필요합니다. DKMS 패키지는 커널이 업데이트될 때 자동으로 재빌드되어, Kali Linux 시스템에서 사실상 유지보수가 필요 없습니다.

**MT7921AUN 커널 이력:** 네이티브 통합은 `mt7921u` USB 드라이버를 통해 Linux 5.18에서 이루어졌습니다. 펌웨어 파일 `WIFI_MT7961_patch_mcu_1_2_hdr.bin`(및 관련 펌웨어 블롭)이 `/lib/firmware/mediatek/`에 존재해야 합니다. Kali에서는 `firmware-misc-nonfree`가 이를 포함합니다. 기본 커널을 사용하는 Ubuntu 22.04 LTS에서는 ≥ 5.18에 도달하기 위해 HWE 스택(`linux-generic-hwe-22.04`)을 설치해야 할 수 있습니다.

**Raspberry Pi 세부 사항:** RTL8812AU 드라이버는 `dkms-rtl8812au`를 사용하여 Raspberry Pi OS(32비트 및 64비트)에서 깔끔하게 컴파일됩니다. NetHunter 배포에 가장 안전한 선택입니다. MT7921AUN 어댑터(AXM, AXML)는 Pi 4/5에서 동작할 수 있으나 `firmware-misc-nonfree`와 충분히 최신인 Raspberry Pi OS 커널이 필요합니다(2023년 이후 이미지라면 문제없습니다).

---

## 활용 사례별 최적의 ALFA 어댑터

### 레드팀 운용

**추천: [AWUS036ACH](/ko/products/alfa/awus036ach/)**

ACH의 500mW 송신 출력, 듀얼 안테나, 그리고 검증된 RTL8812AU 드라이버는 레드팀 임무의 기본 선택이 됩니다. 커널 업데이트 후에도 동작하고, VM을 안정적으로 통과하며, 가져온 어떤 RP-SMA 안테나든 수용할 것이라고 믿을 수 있습니다. 예산이 허락하고 6E 커버리지가 범위에 포함된다면, 6GHz 네트워크 탐지를 위한 보조 어댑터로 [AWUS036AXML](/ko/products/alfa/awus036axml/)을 추가하십시오.

### CTF 대회

**추천: [AWUS036ACM](/ko/products/alfa/awus036acm/)**

CTF 무선 과제는 일반적으로 송신 출력이 결정적 변수가 아닌 통제된 환경에서 진행됩니다. ACM은 번거로움 없는 Linux 드라이버 설정(커널 4.19부터 내장된 MT7612U)과 함께 완전한 모니터 모드 및 인젝션 기능을 제공합니다. 소형 듀얼 안테나 폼팩터는 챙기고 배치하기 쉽습니다. CTF에 Wi-Fi 6 과제(아직 드물지만 증가 추세)가 포함된다면 [AWUS036AXML](/ko/products/alfa/awus036axml/)을 대신 사용하십시오.

### Raspberry Pi / Kali NetHunter

**추천: [AWUS036ACH](/ko/products/alfa/awus036ach/) 또는 [AWUS036ACM](/ko/products/alfa/awus036acm/)**

RTL8812AU(ACH)와 MT7612U(ACM) 어댑터는 Raspberry Pi 하드웨어에서 검증된 실적을 갖고 있습니다. 특정 이미지에서 커널 및 펌웨어 호환성을 확인하지 않은 한, Pi 배포에는 MT7921AUN 모델(AXM, AXML)을 피하십시오. 현장에서 안정적이어야 하는 전용 NetHunter Pi를 구축한다면 ACH가 더 안전한 선택입니다.

### 엔터프라이즈 무선 감사

**추천: [AWUS036AXML](/ko/products/alfa/awus036axml/) + [AWUS036ACH](/ko/products/alfa/awus036ach/)**

현대적인 엔터프라이즈 무선 감사는 2.4, 5, 6GHz 대역을 모두 커버해야 합니다. AXML은 6E를 포함한 전체 트라이밴드 스펙트럼을 커버하고, ACH는 5GHz 작업을 위한 안정적인 고출력 백업을 제공합니다. 별도의 캡처 인터페이스로 두 어댑터를 동시에 운용하면 드라이버 타협 없이 완전한 대역 커버리지를 확보합니다. 액티브 인젝션 작업에는 ACH를, 수동 6GHz 모니터링에는 AXML을 사용하십시오.

### DJI 드론 거리 확장

**추천: [AWUS036EACS](/ko/products/alfa/awus036eacs/)**

Litchi 또는 DJI GO를 통한 DJI 거리 확장은 일반적인 합법적 활용 사례입니다. RTL8821CU를 탑재한 EACS가 여기서 추천되는 이유는, 추가 드라이버 없이 Windows(DJI 소프트웨어가 실행되는 환경)에서 기본적으로 동작하고, 범용 연결 프로파일이 이 활용 사례에 적합하기 때문입니다. 모니터 모드는 필요 없으며, 중요한 것은 클라이언트 모드 연결과 송신 출력입니다. 최대 유효 거리를 위해 [APA-M25](/ko/products/alfa/apa-m25/) 패널 안테나와 짝지어 사용하십시오.

---

## OS별 권장 사항

### Kali Linux

Kali Linux는 보안 작업에 사용되는 모든 ALFA 어댑터의 주 지원 플랫폼입니다. Kali 저장소에는 RTL8812AU/RTL8811AU 어댑터용 `dkms-rtl8812au`와 MT7921AUN 어댑터용 `firmware-misc-nonfree`가 포함되어 있습니다. Kali 설치를 최신 상태로 유지하십시오 — DKMS 패키지가 커널 변경을 자동으로 추적합니다.

**빠른 설정 (RTL8812AU 계열):**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
sudo modprobe 88XXau
```

**빠른 설정 (MT7921AUN 계열 — AXM, AXML):**
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
# Reboot or reload the module:
sudo modprobe mt7921u
```

**모니터 모드 활성화:**
```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

### Ubuntu 24.04 LTS

Ubuntu 24.04는 커널 6.8과 함께 제공됩니다. MT7921AUN 어댑터(AXM, AXML)는 `firmware-misc-nonfree`가 설치되면 기본적으로 동작합니다:
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

Ubuntu에서 RTL8812AU 지원은 DKMS 모듈 빌드가 필요합니다:
```bash
sudo apt install -y git dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && sudo make dkms_install
```

### Windows 11

모든 ALFA 어댑터는 Windows 10/11 호환 드라이버와 함께 제공됩니다. ALFA Network 웹사이트에서 드라이버 패키지를 다운로드하거나, MT7921AUN의 경우 Windows Update를 통해 설치하십시오(Microsoft가 WHQL 서명된 인박스 드라이버를 제공합니다). RTL8812AU 어댑터는 ALFA가 제공하는 Realtek 드라이버 패키지가 필요하며, RTL8812AU용 Windows Update 드라이버는 제공이 일관되지 않습니다.

Acrylic Wi-Fi, inSSIDer, 또는 Windows용 Wireshark와 같은 도구와 함께 사용할 경우, ALFA 드라이버는 NDIS 모니터 모드를 통해 Windows에서 기능하는 모니터 모드 래퍼를 제공합니다 — 다만 이는 액티브 인젝션 작업에서 Linux 모니터 모드보다 상당히 기능이 떨어집니다.

### macOS Sonoma

2026년 macOS Sonoma를 공식 지원하는 ALFA 어댑터는 없습니다. RTL8812AU용 커뮤니티 kext 프로젝트가 존재하지만 서명되지 않았으며 시스템 무결성 보호(SIP)를 비활성화해야 합니다. 현실적인 권장 사항은 USB 패스스루와 함께 VM(Parallels, VMware Fusion, 또는 UTM)에서 Kali Linux를 실행하는 것입니다.

RTL8821CU를 탑재한 AWUS036EACS는 커뮤니티 프로젝트를 통해 제한적인 macOS 드라이버 지원을 가질 수 있으나, macOS 기본 드라이버로는 모니터 모드를 사용할 수 없습니다(Linux 커널 6.2 이상에서는 실측으로 모니터/인젝션 동작).

### Raspberry Pi / Kali NetHunter

Kali NetHunter를 실행하는 Raspberry Pi 4 및 Pi 5에서:

```bash
# For RTL8812AU adapters (ACH, ACS):
sudo apt update && sudo apt install -y dkms-rtl8812au

# For MT7921AUN adapters (AXM, AXML — Pi 5 with recent kernel recommended):
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

{{< alert "circle-info" >}}
전용 NetHunter 드롭박스를 구축한다면 [AWUS036ACH](/ko/products/alfa/awus036ach/) 또는 [AWUS036ACM](/ko/products/alfa/awus036acm/)을 사용하십시오. RTL8812AU(ACH)와 MT7612U(ACM) 드라이버는 ARM에서 안정적으로 컴파일되며 펌웨어 파일 의존성이 없습니다. MT7921AUN 모델(AXM, AXML)은 Pi에서 기능하지만 오프라인 배포에서 골칫거리가 될 수 있는 펌웨어 파일 의존성을 추가합니다.
{{< /alert >}}

---

{{< faq >}}

## 최종 권장 사항

드라이버 성숙도, 하드웨어 성능, 실제 활용 사례에 걸쳐 8개 어댑터를 모두 평가한 결과, 대부분의 전문가를 커버하는 세 가지 선택은 다음과 같습니다:

**예산형 선택: [AWUS036ACM](/ko/products/alfa/awus036acm/)**
듀얼 RP-SMA 커넥터를 갖춘 MT7612U 어댑터는 무설정 Linux 드라이버 설정(커널 4.19부터 내장)과 함께 완전한 모니터 모드 및 패킷 인젝션 지원을 제공합니다. 신뢰할 수 있고 번거로움 없는 도구를 원하는 컨설턴트나 어댑터를 대량 구매하는 팀에 이상적입니다.

**다재다능형 선택: [AWUS036ACH](/ko/products/alfa/awus036ach/)**
듀얼 안테나, 500mW RTL8812AU 어댑터는 보안 전문가에게 가장 널리 추천되는 단일 어댑터입니다. 2.4 및 5GHz를 커버하고, 외장 안테나를 수용하며, 이 목록의 어떤 어댑터보다 성숙한 드라이버 스택을 갖추었고, ACM보다 소폭 높은 비용만 듭니다. 어댑터 하나를 구매하는데 아직 무엇이 필요한지 확신이 서지 않는다면 이 제품을 구매하십시오.

**엔터프라이즈 / 미래 대비형 선택: [AWUS036AXML](/ko/products/alfa/awus036axml/)**
감사 범위에 Wi-Fi 6E 인프라가 포함된다면 — 2026년에 시작하는 모든 업무라면 포함되어야 합니다 — AXML은 USB-C 3.2, 6GHz 기능, Bluetooth 5.2를 하나의 패키지로 제공하는 유일한 어댑터입니다. ACH와 짝지으면 2.4GHz부터 6GHz까지 모든 대역을 타협 없이 커버하는 2어댑터 키트가 됩니다. 듀얼 안테나 6E 커버리지가 필요하다면 AWUS036AXM을 고려하십시오.

상세한 설정 및 구성 방법은 다음을 참조하십시오:
- [Kali Linux 및 Ubuntu에 ALFA 드라이버 설치](/ko/blog/install-alfa-driver-kali-ubuntu/)
- [커널 업데이트 후 ALFA 드라이버 수정](/ko/blog/fix-alfa-driver-kernel-update/)
- [Kali Linux에서 모니터 모드 활성화](/ko/blog/enable-monitor-mode-kali-linux/)
- [AWUS036AXML Wi-Fi 6E 리뷰 및 드라이버 테스트](/ko/blog/awus036axml-wifi-6e-review/)

## 참고 자료

1. [aircrack-ng rtl8812au 드라이버](https://github.com/aircrack-ng/rtl8812au)
2. [Wi-Fi Alliance 공식 웹사이트](https://www.wi-fi.org/)
3. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw)
4. [Linux 커널 mt76 드라이버](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76)
