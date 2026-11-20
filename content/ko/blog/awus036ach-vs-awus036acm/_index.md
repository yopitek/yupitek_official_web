---
title: "ALFA AWUS036ACH vs AWUS036ACM: Kali Linux를 위한 완벽 비교 (2026)"
description: "ALFA AWUS036ACH와 AWUS036ACM의 상세 비교 — 칩셋, 모니터 모드, 패킷 인젝션, 드라이버 지원, 그리고 Kali Linux 침투 테스트에 어느 쪽이 더 나은지 알아봅니다."
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036ACH와 AWUS036ACM의 드라이버 설치 차이는 무엇입니까?"
    answer: "AWUS036ACH는 RTL8812AU를 사용하며 aircrack-ng 커뮤니티 드라이버의 DKMS 컴파일이 필요하고, 커널 업데이트 후 재컴파일이 필요할 수 있습니다. AWUS036ACM은 MT7612U를 사용하며, 해당 드라이버가 4.19부터 메인라인 커널에 포함되어 있어 컴파일 없이 플러그 앤 플레이로 동작합니다."
  - question: "모니터 모드에는 어느 쪽이 더 낫습니까?"
    answer: "AWUS036ACH가 모니터 모드에서 더 안정적입니다. 듀얼 안테나와 30dBm 고출력 덕분에 밀집된 AP 환경에서 패킷 손실이 더 적습니다. ACM도 모니터링을 지원하지만 송신 출력이 더 낮아 근거리 캡처에 적합합니다."
  - question: "초보자는 ACH와 ACM 중 무엇을 선택해야 합니까?"
    answer: "초보자는 AWUS036ACM을 선택해야 합니다. MT7612U 커널 네이티브 드라이버는 컴파일 없이 플러그 앤 플레이로 동작합니다. 가장 강한 신호와 가장 많은 튜토리얼이 필요하고 DKMS에 익숙하다면 AWUS036ACH를 선택하십시오."
  - question: "VM 환경에는 어느 쪽이 권장됩니까?"
    answer: "VM에서는 AWUS036ACM이 유리합니다. USB 패스스루 후, 커널 네이티브 드라이버가 VM 내부에 빌드 도구 체인을 설치하지 않고도 즉시 동작합니다. ACH는 VM 내부에 드라이버 설치가 필요합니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "AWUS036ACM", "comparison", "kali-linux", "RTL8812AU", "MT7612U"]
featureimage: "/images/blog/awus036ach-vs-awus036acm.webp"
---
Kali Linux 침투 테스트에 가장 인기 있는 두 ALFA Network USB 어댑터는 순수 성능과 휴대성 사이의 스펙트럼에서 서로 다른 지점에 위치합니다. **AWUS036ACH**는 검증된 드라이버 이력을 갖춘 고출력 듀얼 안테나 주력 제품입니다. **AWUS036ACM**은 일부 출력을 단순성과 사용 편의성과 맞바꾼 소형의 커널 네이티브 대안입니다. 이 가이드는 실제 침투 테스트 작업에 중요한 모든 측면을 분석합니다.

## 개요

{{< tldr >}}
AWUS036ACH는 RTL8812AU 드라이버와 30dBm 듀얼 안테나로 가장 강력한 모니터링과 인젝션을 제공하여 전문 작업에 적합합니다. AWUS036ACM은 MT7612U 커널 네이티브 드라이버와 무컴파일을 통한 휴대성을 위한 제품으로, 가격은 약 $30~40입니다.
{{< /tldr >}}


전문 침투 테스트에는 AWUS036ACH를 선택하십시오: 성숙한 RTL8812AU 드라이버와 30dBm 듀얼 안테나가 가장 강력한 모니터링과 패킷 인젝션을 제공합니다. 플러그 앤 플레이 휴대성에는 AWUS036ACM을 선택하십시오: MT7612U 커널 네이티브 드라이버로 커널 4.19부터 무컴파일입니다.

---

## AWUS036ACH — AC1200, RTL8812AU, 고출력

[AWUS036ACH](/ko/products/alfa/awus036ach/)는 출시 이후 전문가와 애호가의 Wi-Fi 감사에서 주력 제품이 되어 왔습니다. 2017년부터 오늘날까지 발표된 대부분의 Kali Linux 무선 침투 테스트 튜토리얼, 강좌, 보고서에서 인용되는 어댑터입니다.

**전체 사양:**
- **Wi-Fi 표준:** IEEE 802.11a/b/g/n/ac (Wi-Fi 5)
- **칩셋:** Realtek RTL8812AU
- **주파수 대역:** 2.4GHz + 5GHz (듀얼 밴드)
- **최대 처리량:** AC1200 (300 + 867 Mbps)
- **안테나:** 탈착식 RP-SMA 커넥터 2개 (듀얼 안테나 다이버시티)
- **기본 안테나:** 2× 5dBi 무지향성
- **USB 커넥터:** USB-C (USB 3.0 호환)
- **TX 출력:** 최대 30dBm — USB 어댑터 중 최고 수준
- **크기:** 더 큰 폼팩터 (데스크톱/휴대 용도)

듀얼 RP-SMA 커넥터는 중요한 장점입니다: 고이득 지향성 또는 무지향성 안테나를 장착하여 도달 범위를 크게 확장할 수 있으며, 이는 장거리 감사 시나리오에 필수적입니다.

---

## AWUS036ACM — AC600, MT7612U, 소형

[AWUS036ACM](/ko/products/alfa/awus036acm/)은 단순성, 휴대성, 커널 네이티브 드라이버 지원을 우선시하는 사용자를 겨냥합니다. MediaTek MT7612U(또는 MT7612UN) 칩셋을 사용하며, 이는 버전 4.19부터 메인라인 Linux 커널의 일부였습니다 — 즉, 현대의 모든 Kali Linux 시스템에서 **드라이버 컴파일이 전혀 필요 없습니다**.

**전체 사양:**
- **Wi-Fi 표준:** IEEE 802.11a/b/g/n/ac (Wi-Fi 5)
- **칩셋:** MediaTek MT7612U / MT7612UN
- **주파수 대역:** 2.4GHz + 5GHz (듀얼 밴드)
- **최대 처리량:** AC600 (150 + 433 Mbps)
- **안테나:** 탈착식 RP-SMA 커넥터 1개
- **기본 안테나:** 1× 5dBi 무지향성
- **USB 커넥터:** USB-C (USB 3.0 호환)
- **TX 출력:** 표준 출력 (ACH보다 낮음)
- **크기:** 소형 폼팩터 (휴대 용도)

단일 안테나와 더 낮은 TX 출력은 ACH에 비해 장거리 성능이 떨어짐을 의미하지만, 깔끔한 커널 드라이버 경험과 소형 본체는 은밀성이나 이동성이 중요한 작업에 매우 실용적입니다.

---

## 전체 사양 비교표

| 특성 | AWUS036ACH | AWUS036ACM |
|---|---|---|
| **Wi-Fi 표준** | 802.11ac (Wi-Fi 5) | 802.11ac (Wi-Fi 5) |
| **칩셋** | RTL8812AU | MT7612U / MT7612UN |
| **주파수 대역** | 2.4GHz + 5GHz | 2.4GHz + 5GHz |
| **최대 처리량** | AC1200 | AC600 |
| **RP-SMA 커넥터** | 2× | 1× |
| **TX 출력** | 최대 30dBm | 표준 |
| **USB 유형** | USB-C | USB-C |
| **드라이버 소스** | 아웃 오브 트리 (DKMS) | 메인라인 커널 (4.19+) |
| **드라이버 설치** | 수동 컴파일 | 플러그 앤 플레이 |
| **모니터 모드** | ★★★★★ | ★★★★☆ |
| **패킷 인젝션** | ★★★★★ | ★★★★☆ |
| **폼팩터** | 더 큼 | 소형 |
| **가격대** | ~$40–50 | ~$30–40 |

---

## 칩셋 심층 분석

### RTL8812AU (AWUS036ACH)

Realtek RTL8812AU는 무선 보안 연구에서 가장 광범위하게 테스트된 칩셋 중 하나입니다. 커뮤니티가 유지보수하는 드라이버는 [github.com/aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au)에 호스팅되어 있으며 2017년부터 활발히 개발되고 패치되어 왔습니다.

**Kali Linux에 설치:**

```bash
sudo apt update
sudo apt install dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

설치 후, 모듈은 DKMS를 통해 커널 업데이트 전반에 걸쳐 유지됩니다. 드라이버가 지원하는 기능:

- **모니터 모드** — 완전히 작동하며 극도로 안정적
- **프레임 인젝션** — 모든 인젝션 유형(deauth, beacon, probe, data)
- **다중 가상 인터페이스** — 모니터 + 관리 모드 동시 실행
- **WPA3-SAE 핸드셰이크 캡처** — 최신 커널/드라이버 조합에서 동작 확인

주요 절충점은 새 커널이 설치될 때 **반드시 재컴파일**해야 한다는 점입니다(또는 DKMS가 자동으로 처리함). 간혹 새 Kali 커널 버전이 드라이버가 업데이트될 때까지 일시적으로 빌드를 깨뜨리기도 합니다. 이는 관리 가능하지만 실질적인 운용상의 고려 사항입니다.

### MT7612U (AWUS036ACM)

MediaTek MT7612U 드라이버(`mt76x2u`)는 버전 **4.19(2018년 10월)**에서 메인라인 Linux 커널에 병합되었습니다. 즉, 커널 4.19 이상을 실행하는 모든 Kali Linux 설치 — 2018년 말 이후의 모든 Kali 릴리스가 해당 — 에서 AWUS036ACM은 **플러그 앤 플레이**입니다.

```bash
# Verify the module is loaded
lsmod | grep mt76x2u

# Manual load if needed
sudo modprobe mt76x2u
```

주요 드라이버 특성:

- **컴파일 불필요** — 에어갭 또는 제한된 환경에 이상적
- **모니터 모드** — 지원되며 작동함
- **패킷 인젝션** — 지원되며 대체로 안정적
- **안정성** — 커널 네이티브 드라이버는 커널 업데이트 전반에 걸쳐 더 안정적인 경향이 있음
- **커뮤니티 지원** — 성장 중이나 RTL8812AU 생태계보다는 작음

한 가지 유의점: (일부 ACM 배치에 사용되는) MT7612UN 변종은 Linux에서 동일하게 동작하며, 둘 다 동일한 `mt76x2u` 모듈로 처리되기 때문입니다.

---

## 모니터 모드 비교

두 어댑터 모두 모니터 모드를 지원하지만 실질적인 차이가 있습니다.

**AWUS036ACH (RTL8812AU):**

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
# Creates wlan0mon in monitor mode
iwconfig wlan0mon
```

모니터 모드에서의 채널 전환이 즉각적이고 안정적입니다. 인터페이스는 일반 캡처 속도에서 패킷 손실 없이 고트래픽 캡처 환경(밀집된 AP, 다수의 클라이언트)을 처리합니다.

**AWUS036ACM (MT7612U):**

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# Or via airmon-ng:
sudo airmon-ng start wlan0
```

모니터 모드가 작동하며 Wireshark, tcpdump, airodump-ng, kismet에서 동작이 확인되었습니다. 다만 일부 사용자는 특정 커널 버전에서 가장 안정적인 결과를 위해 airmon-ng 대신 `iw`를 직접 사용해야 한다고 보고합니다.

---

## 패킷 인젝션 비교

**AWUS036ACH:** 패킷 인젝션은 가장 강력한 장점 중 하나입니다. 모든 aireplay-ng 공격 모드가 안정적으로 동작합니다:

```bash
# Test injection
sudo aireplay-ng --test wlan0mon

# Deauthentication attack
sudo aireplay-ng -0 5 -a [BSSID] wlan0mon

# WPA handshake capture via deauth
sudo airodump-ng -c [CH] --bssid [BSSID] -w capture wlan0mon &
sudo aireplay-ng -0 3 -a [BSSID] wlan0mon
```

**AWUS036ACM:** 인젝션은 모든 표준 공격 유형에서 동작하지만, 일부 사용자는 매우 높은 속도로 인젝션할 경우 특정 커널 버전에서 간혹 인터페이스가 멈출 수 있다고 보고했습니다. 일반적인 침투 테스트 워크플로(통제된 deauth, PMKID 캡처, KRACK 테스트)에서는 안정적으로 수행됩니다.

---

## 드라이버 설치 복잡성

이 표는 가장 먼저 확인해야 할 항목입니다 — 첫날과 이후 모든 커널 업데이트에서 겪게 될 설정 마찰 정도를 결정하기 때문입니다.

| 작업 | AWUS036ACH | AWUS036ACM |
|---|---|---|
| 새 Kali 설치, 어댑터 연결 | 인식되지 않음 — 드라이버 설치 필요 | 즉시 인식 |
| 커널 업데이트 후 | DKMS 자동 재빌드 (대개) | 조치 불필요 |
| 에어갭 머신 | 오프라인 패키지 준비 필요 | 네이티브로 동작 |
| Kali Live USB | 세션 내 드라이버 설치 필요 | 바로 동작 |
| VirtualBox/VMware 패스스루 | 게스트에서 드라이버 설치 후 동작 | 게스트에서 즉시 동작 |
| Raspberry Pi / ARM | DKMS + ARM 헤더 필요 | Pi 4/5에서 플러그 앤 플레이 |

ACM의 무설치 경험은 라이브 부트 환경, 고객 제공 머신, 또는 시간과 단순성이 최우선인 CTF 대회 설정과 같은 시나리오에서 진정한 장점입니다.

---

## 크기와 휴대성

**AWUS036ACH**는 눈에 띄게 더 큰 PCB와 하우징을 갖습니다. 이는 부분적으로 듀얼 RP-SMA 커넥터와 30dBm 출력에 필요한 더 큰 전원 부품 때문입니다. 노트북 가방에는 쉽게 들어가지만 "포켓" 어댑터는 아닙니다.

**AWUS036ACM**은 훨씬 더 소형입니다. 물리적 보안 작업 중에 또는 큰 USB 어댑터가 주목을 끌 수 있는 환경에서 눈에 띄지 않게 사용할 수 있습니다. 또한 소비 전력이 더 적어, 장시간 현장 작업 중 노트북 배터리로 구동할 때 중요합니다.

---

## 가격 대비 가치

약 $40~50인 **AWUS036ACH**는 주로 듀얼 안테나 구성, 높은 TX 출력, 검증된 드라이버 유산 때문에 프리미엄 가격을 받습니다. 신뢰성과 신호 강도가 산출물 품질에 직접 영향을 미치는 전문 작업에서는 이 프리미엄이 정당화됩니다.

약 $30~40인 **AWUS036ACM**은 다음과 같은 사용자층에게 뛰어난 가치를 제공합니다:
- 플러그 앤 플레이의 단순함을 원하는 무선 보안 학습자
- 주로 근거리 환경에서 작업하는 테스터
- 백업 또는 보조 어댑터가 필요한 팀
- 깔끔하고 무컴파일 워크플로를 우선시하는 모든 사람

---

## 결론

**레드팀 및 전문 침투 테스터 → AWUS036ACH.** RTL8812AU 드라이버 생태계는 공격 도구에서 더 잘 지원되며, 듀얼 안테나 인젝션은 실제 평가에서 측정 가능할 만큼 더 안정적입니다. 유료 작업에서 인젝션 성공률이 중요하다면 ACH가 우세합니다.

**CTF 학생 및 Kali 첫 사용자 → AWUS036ACM.** Kali 2023.3+에서 무컴파일입니다. 커널 모듈을 컴파일해 본 적이 없다면 여기서 시작하십시오 — 깨질 것이 없습니다.

**Raspberry Pi 및 ARM 플랫폼 사용자 → AWUS036ACM.** MT7612U는 커널 4.x부터 Linux 커널 트리에 포함되어 있습니다. Pi 4/5, Odroid, Orange Pi에서 플러그 앤 플레이입니다. ACH도 동작하지만 ARM 전용 헤더로 아웃 오브 트리 RTL8812AU 드라이버를 컴파일해야 합니다.

---

{{< faq >}}

## Raspberry Pi 및 ARM 호환성

Raspberry Pi 4, Pi 5, 또는 임의의 ARM 단일 보드 컴퓨터에서 Kali를 실행한다면, AWUS036ACM의 MT7612U 칩셋이 명백한 선택입니다. 커널 4.x부터 Linux 커널 트리에 포함되어 있어 — Raspberry Pi OS, Kali ARM, Ubuntu Server ARM에서 플러그 앤 플레이입니다.

RTL8812AU(AWUS036ACH)는 ARM에서 아웃 오브 트리 드라이버가 필요합니다. 컴파일 과정은 x86에서와 동일하지만, ARM 커널에 맞는 올바른 헤더를 설치해야 합니다:

```bash
sudo apt install linux-headers-$(uname -r) bc
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && make && sudo make install
```

전체 설정 가이드는 [Raspberry Pi 4 & Pi 5에서의 ALFA USB WiFi](/ko/blog/alfa-adapter-raspberry-pi-kali/)를 참조하십시오.

## 참고 자료

1. [aircrack-ng rtl8812au 드라이버](https://github.com/aircrack-ng/rtl8812au)
2. [kernel.org mt76 드라이버](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76)
3. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw)
4. [Yopitek 공식 웹사이트](https://www.yupitek.com)
