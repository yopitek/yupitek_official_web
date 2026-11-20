---
title: "WiFi 6E vs WiFi 5: 침투 테스트에 어떤 ALFA 어댑터를 선택해야 할까요?"
description: "Kali Linux 침투 테스트를 위한 ALFA AWUS036AXML(Wi-Fi 6E)과 AWUS036ACH(Wi-Fi 5)를 비교합니다. 6 GHz 지원, 드라이버 성숙도, 모니터 모드, 실제 활용 사례를 다룹니다."
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "침투 테스트 관점에서 Wi-Fi 6E와 Wi-Fi 5의 차이는 무엇입니까?"
    answer: "Wi-Fi 6E는 6 GHz 대역과 1.2 GHz의 스펙트럼을 추가하여 최신 기업 환경을 점검하는 데 적합합니다. Wi-Fi 5는 드라이버가 더 성숙하여 2.4/5 GHz에서 더 높은 안정성을 제공합니다."
  - question: "AWUS036ACH와 AWUS036AXML 중 무엇을 선택해야 합니까?"
    answer: "일상적인 침투 테스트에는 드라이버가 성숙하고 커뮤니티 자료가 풍부한 AWUS036ACH를 선택하십시오. 6 GHz Wi-Fi 6E 환경을 점검하려면 AWUS036AXML을 선택하십시오. 예산이 허락한다면 두 가지를 모두 갖추는 것이 이상적입니다."
  - question: "Kali Linux에서 AWUS036AXML의 모니터 모드는 안정적입니까?"
    answer: "커널 6.1 이상과 최신 linux-firmware 패키지가 필요합니다. 커뮤니티에서는 커널 6.16 이전에서 패킷 인젝션이 동작했다고 보고하지만, 자체 테스트에서는 기본 커널 6.17에서 실패했습니다(칩셋의 한계가 아니라 mac80211 chanctx 회귀 때문입니다). 인젝션이 필요하다면 AWUS036ACH를 사용하십시오."
  - question: "2026년 침투 테스트에 6 GHz 어댑터가 필요합니까?"
    answer: "대부분의 테스트 사례는 여전히 2.4/5 GHz에 집중되어 있습니다. 그러나 대상 환경에 Wi-Fi 6E 액세스 포인트가 구축되어 있다면 6 GHz 어댑터는 전략적으로 필수가 됩니다."
  - question: "AWUS036ACH용 RTL8812AU 드라이버는 어떻게 설치합니까?"
    answer: "aircrack-ng GitHub에서 rtl8812au 저장소를 클론한 후 make dkms_install을 실행합니다. DKMS를 사용하면 커널 업데이트 후에도 드라이버가 자동으로 다시 빌드됩니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["wifi-6e", "wifi-5", "AWUS036AXML", "AWUS036ACH", "penetration-testing", "kali-linux"]
featureimage: "/images/blog/wifi-6e-vs-wifi-5-kali-linux.webp"
---

진짜 질문은 이것입니다. 2026년 현재 귀하의 테스트 환경에서 6 GHz 기능을 추가하는 것이 그만한 복잡성을 감수할 가치가 있을까요? 이 글은 사양표가 아니라 의사결정 프레임워크를 제공합니다.

{{< tldr >}}
AWUS036ACH는 드라이버가 성숙하고 안정성이 가장 높아 일상적인 침투 테스트의 1순위 선택입니다. AWUS036AXML은 Wi-Fi 6E 환경 점검을 위해 6 GHz 대역을 지원하지만, 드라이버는 아직 성숙해 가는 단계입니다.
{{< /tldr >}}





---

## 60초 선택 가이드

다음 질문에 순서대로 답하면 바로 결론을 얻을 수 있습니다.

**Q1: WiFi 6E AP(6 GHz 활성화)가 구축된 건물의 네트워크를 테스트하십니까?**
- 아니요 → WiFi 5 어댑터로 충분합니다. AWUS036ACH가 필요한 모든 것을 지원합니다.
- 예 → Q2로 진행하십시오.

**Q2: Kali 커널이 5.18 이상입니까?**

```bash
uname -r   # Must be 5.18+ for mt7921u firmware support
```

- 아니요 → 먼저 `sudo apt update && sudo apt full-upgrade`를 실행한 후 재부팅하십시오.
- 예 → Q3로 진행하십시오.

**Q3: 테스트 환경이 가상 환경(VirtualBox 또는 VMware)입니까?**
- 예 → AWUS036AXML은 VM 패스스루 지원이 제한적입니다. 베어메탈 Kali를 사용하거나, VM에서는 AWUS036ACH를 사용하는 것을 고려하십시오.
- 아니요(베어메탈 Kali) → AWUS036AXML이 올바른 선택입니다.

---

## Wi-Fi 6E란? 새로운 6 GHz 대역 설명

Wi-Fi 6E는 Wi-Fi 6(IEEE 802.11ax) 표준의 확장으로, 이전에는 활용되지 않았던 방대한 스펙트럼인 **6 GHz 주파수 대역**을 사용할 수 있게 합니다. Wi-Fi 5(802.11ac)는 2.4 GHz와 5 GHz에서만 동작하며 일반 Wi-Fi 6도 마찬가지인 반면, Wi-Fi 6E는 5.925 GHz에서 7.125 GHz에 이르는 추가 **1.2 GHz 스펙트럼**을 열어 줍니다.

실제로 이는 다음을 의미합니다.

- 6 GHz 대역에서 **최대 7개의 추가 160 MHz 채널** (5 GHz 대역에서는 1~2개에 불과)
- 레거시 기기가 6 GHz를 사용할 수 없으므로 **간섭 감소**
- 고밀도 환경에서 **낮은 지연 시간**과 높은 처리량
- **하위 호환성** — Wi-Fi 6E 어댑터는 2.4 GHz와 5 GHz에서도 통신합니다

일반 소비자와 기업 IT 부서에게 Wi-Fi 6E는 판도를 바꾸는 기술입니다. 침투 테스터에게는 상황이 좀 더 미묘합니다.

---

## 침투 테스트 관점: 2026년에 6 GHz가 중요할까요?

2026년에 Wi-Fi 6E 액세스 포인트는 기업 환경, 코워킹 스페이스, 최신 주거 환경에서 점점 더 흔해지고 있습니다. 그러나 **실제 침투 테스트 업무의 대부분은 여전히 2.4 GHz와 5 GHz 네트워크를 대상으로 합니다.** 그 이유는 다음과 같습니다.

1. **레거시 인프라가 지배적입니다** — 대부분의 중소기업과 오래된 기업 환경은 Wi-Fi 5 이하를 운영합니다.
2. **도구 지원이 미성숙합니다** — Aircrack-ng, Hashcat, hostapd-wpe는 아직 6 GHz 워크플로에 대응해 가는 중입니다.
3. **규제의 복잡성** — 6 GHz 대역 사용은 엄격히 규제되며, 많은 국가에서 명시적인 허가 없이 6 GHz로 송신하는 것을 제한합니다.
4. **클라이언트 기기 지원** — 6 GHz 전용 기기는 아직 소수이며, 대부분 여전히 5 GHz로 연결합니다.

그렇다 하더라도 업무에 최신 기업용 Wi-Fi 6E 환경이 포함된다면, 6 GHz 지원 어댑터는 더 이상 선택 사항이 아니라 전략적 이점입니다.

---

## ALFA AWUS036ACH — AC1200 Wi-Fi 5, RTL8812AU

[AWUS036ACH](/ko/products/alfa/awus036ach/)는 침투 테스트 커뮤니티에서 가장 검증이 많이 이루어진 USB Wi-Fi 어댑터 중 하나입니다. 출시된 지 수년이 지나 방대한 커뮤니티 지식, 드라이버 패치, 검증된 워크플로가 축적되어 있습니다.

**주요 사양:**
- **표준:** IEEE 802.11a/b/g/n/ac (Wi-Fi 5)
- **칩셋:** Realtek RTL8812AU
- **주파수 대역:** 2.4 GHz + 5 GHz
- **최대 처리량:** AC1200 (2.4 GHz에서 300 Mbps + 5 GHz에서 867 Mbps)
- **안테나:** 2× 탈착식 RP-SMA (듀얼 안테나 다이버시티)
- **USB:** USB-C (USB 3.0 호환)
- **TX 출력:** 최대 30 dBm (고출력)

**Kali Linux 드라이버 상태:**

RTL8812AU 드라이버는 Aircrack-ng 팀이 [github.com/aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au)에서 관리합니다. DKMS로 설치되며 Kali 2023.x 및 2024.x 커널에서 안정적으로 컴파일됩니다. 드라이버 설치 후에는 모니터 모드와 패킷 인젝션이 별도 설정 없이 안정적으로 동작합니다.

```bash
sudo apt install dkms git
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

AWUS036ACH는 수천 건의 실제 침투 테스트에서 검증되었습니다. 대부분의 Kali Linux 침투 테스트 강의에서 권장하는 **기준 어댑터**입니다.

---

## ALFA AWUS036AXML — AX1800 Wi-Fi 6E, MT7921AUN

[AWUS036AXML](/ko/products/alfa/awus036axml/)은 차세대 ALFA 침투 테스트 어댑터를 대표합니다. **6 GHz 대역**을 지원하는 최초의 널리 구할 수 있는 USB 어댑터로, Wi-Fi 6E 액세스 포인트와 상호 작용할 수 있습니다.

**주요 사양:**
- **표준:** IEEE 802.11a/b/g/n/ac/ax (Wi-Fi 6E)
- **칩셋:** MediaTek MT7921AUN
- **주파수 대역:** 2.4 GHz + 5 GHz + **6 GHz**
- **최대 처리량:** AX1800 (합산 최대 1800 Mbps)
- **안테나:** 1× 탈착식 RP-SMA
- **USB:** USB-C (USB 3.2 Gen 1)

**Kali Linux 드라이버 상태:**

MT7921AUN 드라이버(`mt7921u`)는 **버전 5.18부터 메인라인 Linux 커널에 병합되었습니다.** 커널 5.18 이상을 탑재한 Kali 2022.2 이후 버전에서는 드라이버 컴파일이 필요하지 않습니다. 어댑터를 연결하기만 하면 인식됩니다.

```bash
# Verify kernel module is loaded
lsmod | grep mt7921u

# If not loaded:
sudo modprobe mt7921u
```

다만 MT7921AUN의 **모니터 모드 지원**은 비교적 최근에 이루어졌으며 커널 버전과 펌웨어에 따라 달라집니다. 2026년 초 기준으로 모니터 모드는 최신 `linux-firmware` 패키지가 설치된 커널 6.1 이상에서 동작합니다. 패킷 인젝션은 커널 6.16 이전에서 커뮤니티 보고상 동작했으나, 자체 테스트에서는 기본 커널 6.17에서 실패했습니다(`aireplay-ng --test`에서 Found 0 APs / No Answer가 표시되어 인증 해제(deauth)와 핸드셰이크 캡처가 불가능했습니다). 주된 원인은 칩셋의 한계가 아니라 커널 6.16 이후의 mac80211 chanctx 회귀입니다. 패치된 커뮤니티 드라이버로 인젝션을 동작시킬 수는 있지만, 펌웨어가 여전히 전송 속도를 고정합니다(1/6 Mbps, HT/VHT 인젝션 불가). 모니터 모드, AP, WPA3, VIF는 정상 동작하므로, 인젝션이 필요하다면 AWUS036ACH를 사용하십시오.

```bash
sudo apt update && sudo apt install linux-firmware
sudo airmon-ng start wlan0
```

---

## 비교표

| 항목 | AWUS036ACH | AWUS036AXML |
|---|---|---|
| **Wi-Fi 표준** | 802.11ac (Wi-Fi 5) | 802.11ax (Wi-Fi 6E) |
| **칩셋** | RTL8812AU | MT7921AUN |
| **주파수 대역** | 2.4 GHz + 5 GHz | 2.4 GHz + 5 GHz + 6 GHz |
| **최대 처리량** | AC1200 | AX1800 |
| **모니터 모드 안정성** | ★★★★★ (매우 견고) | ★★★★☆ (커널 6.1 이상 필요) |
| **패킷 인젝션** | ★★★★★ (신뢰도 매우 높음) | ⚠️ 커널 6.16 이전에서 커뮤니티 보고, 6.17에서는 실패 |
| **드라이버 설치** | 수동 DKMS (10분) | 커널 내장 (커널 5.18 이상) |
| **6 GHz 지원** | ✗ | ✓ |
| **안테나** | 2× RP-SMA | 1× RP-SMA |
| **TX 출력** | 최대 30 dBm | 표준 |
| **USB 커넥터** | USB-C | USB-C |
| **드라이버 성숙도** | 2017년부터 검증됨 | 2022년 이후 안정적 |
| **커뮤니티 자료** | 풍부함 | 증가 중 |
| **가격대** | ~$40–50 | ~$55–70 |

---

## 실제 침투 테스트 시나리오

### AWUS036ACH가 뛰어난 경우

- **기존 인프라의 Wi-Fi 감사** (2.4/5 GHz의 WPA2-PSK, WPA2-Enterprise, WPA3)
- **인증 해제(Deauthentication) 공격 및 핸드셰이크 캡처** — 검증된 RTL8812AU 드라이버가 문제없이 처리합니다
- hostapd를 사용한 **Evil twin / 불법 AP 구성** — 널리 문서화된 설정이 존재합니다
- **장거리 평가** — 듀얼 RP-SMA 안테나와 높은 TX 출력으로 고이득 지향성 안테나를 장착해 도달 거리를 늘릴 수 있습니다
- **CTF 과제 및 실습 환경** — 온라인 가이드와의 호환성이 가장 높습니다
- **신뢰성이 필수인 업무** — 고객 대면 작업 중 예기치 못한 문제가 없습니다

### AWUS036AXML이 뛰어난 경우

- **최신 기업 6 GHz 네트워크 감사** — 대상이 6 GHz에서만 Wi-Fi 6E를 사용하는 경우 유일한 현실적 선택입니다
- **Wi-Fi 6E 정찰** — 6 GHz SSID와 클라이언트를 스캔하고 식별합니다
- **도구 세트의 미래 대비** — 2026년 이후 Wi-Fi 6E 도입이 가속화됨에 따라
- **커널 네이티브 워크플로** — 최신 Kali 설치에서 드라이버 컴파일의 번거로움이 없습니다
- **다중 대역 환경** — 하나의 어댑터로 트라이밴드를 모두 지원합니다

---

## 권장 사항

**다음에 해당한다면 [AWUS036ACH](/ko/products/alfa/awus036ach/)를 선택하십시오.**
- 일상적인 침투 테스트에 신뢰할 수 있고 검증된 어댑터가 필요합니다
- 업무가 2.4/5 GHz의 WPA2/WPA3 네트워크에 집중되어 있습니다
- 모니터 모드와 패킷 인젝션에 크게 의존합니다
- 최대한의 커뮤니티 문서와 도구 호환성을 원합니다
- 도달 거리 확장을 위해 듀얼 안테나를 지원하는 고출력 어댑터를 선호합니다

**다음에 해당한다면 [AWUS036AXML](/ko/products/alfa/awus036axml/)을 선택하십시오.**
- 최신 Wi-Fi 6E 환경을 정기적으로 감사합니다
- 2026년 이후를 내다보는 도구 세트를 구축하고 있습니다
- Kali Linux 설치본이 커널 6.1 이상에서 실행됩니다
- 컴파일 없이 커널 네이티브 드라이버 지원을 원합니다
- 고객 업무 전에 모니터 모드/인젝션을 직접 테스트하는 데 부담이 없습니다

**결론:** 2026년의 대부분의 전문 침투 테스터에게 AWUS036ACH는 여전히 신뢰성의 표준입니다. AWUS036AXML은 최첨단 기업 인프라를 대상으로 하거나 미래 대비 도구 세트를 구축하는 팀에게 현명한 선택입니다. 가능하다면 둘 다 휴대하는 것이 이상적입니다.

---

{{< faq >}}

## 기업 IT 및 Windows 환경

WiFi 6E는 특히 2022년 이후 신축 또는 리모델링된 건물의 기업 환경에서 점점 더 일반화되고 있습니다. 조직에서 최신 무선 인프라를 평가하는 경우:

**Windows(Acrylic WiFi, NetSpot):** 두 도구 모두 호환 하드웨어와 함께 6 GHz 채널 스캔을 지원합니다. AWUS036AXML은 제조사 드라이버로 Windows에서 동작합니다.

**Linux(Kismet, airodump-ng, hcxdumptool):** 전체 6 GHz 스캔과 패시브 캡처에는 커널 5.18 이상에서 실행되는 AWUS036AXML이 필요합니다.

**권장 기업용 키트:** 평가 키트당 AWUS036ACH 1개(안정적이고 검증되었으며 VM에서 동작)와 AWUS036AXML 1개(베어메탈 Kali에서 6 GHz 커버리지)를 구성합니다. 이렇게 하면 도구 호환성을 해치지 않으면서 2.4 GHz부터 6 GHz까지 전체 스펙트럼을 커버할 수 있습니다.

## 참고 자료

1. [aircrack-ng Official rtl8812au Driver](https://github.com/aircrack-ng/rtl8812au)
2. [MediaTek MT7921 Kernel Driver](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek/mt7921)
3. [Wi-Fi Alliance Wi-Fi 6E Certification](https://www.wi-fi.org/discover-wi-fi/wi-fi-6e)
4. [Kali Linux Official Documentation](https://www.kali.org/docs/)
5. [IEEE 802.11ax Standards Resources](https://standards.ieee.org/ieee/802.11ax/)
