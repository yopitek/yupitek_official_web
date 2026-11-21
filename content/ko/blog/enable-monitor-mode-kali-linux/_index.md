---
title: "2026년 Kali Linux 모니터 모드 활성화 방법: WiFi 어댑터 완벽 가이드"
description: "airmon-ng 또는 iw 명령어로 Kali Linux 2024/2025에서 모니터 모드를 활성화하는 단계별 가이드입니다. 호환 ALFA 어댑터, 문제 해결, airodump-ng를 이용한 검증 방법까지 다룹니다."
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "모니터 모드와 관리 모드(managed mode)는 어떻게 다른가요?"
    answer: "관리 모드는 자신의 MAC 주소와 일치하는 패킷만 수신하지만, 모니터 모드에서는 어댑터가 공중의 모든 802.11 프레임을 제한 없이 캡처할 수 있습니다. 무선 침투 테스트의 기반이 되는 기능입니다."
  - question: "모니터 모드를 활성화할 때 airmon-ng와 iw는 어떤 차이가 있나요?"
    answer: "airmon-ng는 방해 프로세스를 자동으로 처리하고 wlan0mon 가상 인터페이스를 생성합니다. iw는 새 인터페이스를 만들지 않고 기존 인터페이스를 직접 변경하므로 세밀한 제어가 필요할 때 적합합니다."
  - question: "인터페이스가 자동으로 관리 모드로 돌아가면 어떻게 해야 하나요?"
    answer: "백그라운드에서 wpa_supplicant 또는 NetworkManager가 다시 시작된 경우입니다. airmon-ng check kill을 실행하여 해당 프로세스를 종료하십시오."
  - question: "Kali Linux에서 모니터 모드를 완전히 지원하는 ALFA 어댑터는 무엇인가요?"
    answer: "AWUS036ACH(RTL8812AU), AWUS036AXML(MT7921AUN), AWUS036ACM(MT7612U) 모두 모니터 모드를 완전히 지원하며, ACM은 플러그 앤 플레이로 동작합니다. 단, AWUS036AXML은 stock kernel 6.17에서 패킷 인젝션이 실패하므로 인젝션이 필요하다면 ACH 또는 ACM을 사용하십시오."
  - question: "airodump-ng의 Fixed channel wlan0mon: -1 오류는 어떻게 해결하나요?"
    answer: "airodump-ng가 채널을 전환하지 못한다는 의미입니다. iwconfig wlan0mon channel 1로 채널을 지정하고, 남아 있는 wpa_supplicant 프로세스를 종료하십시오."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["monitor-mode", "kali-linux", "airmon-ng", "iw", "wifi-adapter", "ALFA-Network"]
featureimage: "/images/blog/enable-monitor-mode-kali-linux.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---
모니터 모드는 무선 네트워크 인터페이스 카드(NIC)의 특수 동작 모드로, 자신의 장치로 향하는 프레임뿐 아니라 공중의 **모든** 802.11 프레임을 캡처할 수 있게 해 줍니다. 일반적인 "관리(managed)" 모드에서는 어댑터가 자신의 MAC 주소로 향하는 패킷만 수신하고 나머지는 모두 폐기합니다. 모니터 모드는 이 필터를 완전히 해제합니다.

## 모니터 모드란 무엇이며 침투 테스트에서 왜 중요한가

{{< tldr >}}
모니터 모드는 어댑터 자신에게 향하는 패킷만 수신하는 제한을 해제하며, 무선 침투 테스트의 기반이 됩니다. ALFA 어댑터와 airmon-ng 또는 iw를 사용하면 Kali Linux에서 안정적으로 활성화할 수 있습니다.
{{< /tldr >}}


모니터 모드를 사용하면 무선 어댑터가 공중의 모든 802.11 프레임을 캡처할 수 있으며, 이는 airodump-ng, Wireshark, Kismet 같은 도구의 기반이 됩니다. Kali Linux에서는 airmon-ng 또는 iw 명령어로 활성화할 수 있습니다.







무선 침투 테스터에게 모니터 모드는 가장 기본적인 기능입니다. 모니터 모드가 없으면 **airodump-ng**, 무선 캡처 모드의 **Wireshark**, **Kismet** 같은 도구로 네트워크 트래픽을 수동적으로 수집할 수 없습니다. 모니터 모드로 가능한 작업은 다음과 같습니다.

- **수동 정찰** - 프레임을 전혀 송신하지 않고 주변의 모든 액세스 포인트와 클라이언트를 스캔합니다.
- **핸드셰이크 캡처** - 클라이언트 인증 과정에서 WPA/WPA2 4-way 핸드셰이크를 수신합니다.
- **Deauthentication 공격** - 802.11 관리 프레임을 송신합니다(모니터 모드와 함께 패킷 인젝션이 필요합니다).
- **Rogue AP 탐지** - 네트워크의 비인가 액세스 포인트를 식별합니다.
- **프로토콜 분석** - 802.11 관리, 제어, 데이터 프레임을 심층 분석합니다.

모든 무선 어댑터가 모니터 모드를 지원하는 것은 아닙니다. 이 기능은 **칩셋**과 커널에 포함된 **드라이버**에 의해 결정됩니다. 가정용으로 판매되는 일반 소비자용 어댑터는 거의 호환되지 않습니다. ALFA Network 제품군처럼 보안 연구용으로 출시된 어댑터는 모니터 모드를 깔끔하게 지원하는 칩셋과 드라이버를 기반으로 설계되어 있습니다.

---

## 사전 요구사항

모니터 모드를 활성화하기 전에 다음 사항을 확인하십시오.

1. 호환 커널을 갖춘 **Kali Linux**(2024.1 이상 권장)를 실행 중일 것.
2. 무선 어댑터가 연결(USB 어댑터) 또는 장착(PCIe/mini-PCIe)되어 있을 것.
3. **root 또는 sudo** 권한이 있을 것.
4. 인터페이스 이름을 확인했을 것: `ip link` 또는 `iwconfig`를 실행하여 무선 인터페이스 이름(일반적으로 `wlan0`, `wlan1`, `wlx...`)을 기록하십시오.

```bash
ip link show
```

`wlan`으로 시작하거나 `wlx`로 시작하는 MAC 주소 기반의 긴 이름을 가진 항목을 찾으십시오.

---

## 방법 1: airmon-ng로 모니터 모드 활성화

`airmon-ng`는 **aircrack-ng** 제품군에 포함된 도구로, Kali Linux에서 모니터 모드를 전환할 때 가장 널리 사용됩니다. 모드 전환을 방해하는 프로세스 중지 등 다양한 예외 상황을 자동으로 처리합니다.

### 1단계 - 방해 프로세스 종료

NetworkManager, wpa_supplicant, dhclient는 모두 모니터 모드와 충돌합니다. 먼저 종료하십시오.

```bash
sudo airmon-ng check kill
```

> **이 단계가 필요한 이유:** NetworkManager와 wpa_supplicant는 WiFi 인터페이스를 독점적으로 점유합니다. 먼저 종료하지 않으면 모드 전환이 성공한 것처럼 보이지만 실제로는 조용히 실패하여 인터페이스가 관리 모드에 그대로 머뭅니다. 모드를 전환하기 전에 항상 이 프로세스들을 종료하십시오.

예상 출력:

```
Killing these processes:
  PID Name
  812 wpa_supplicant
  934 NetworkManager
```

> **참고:** 이 작업을 수행하면 기존 네트워크 연결이 끊어집니다. 테스트 중 인터넷 연결이 필요하다면 유선 연결을 사용하거나 관리 모드로 동작하는 두 번째 무선 어댑터를 사용하십시오.

### 2단계 - 모니터 모드 시작

```bash
sudo airmon-ng start wlan0
```

예상 출력:

```
PHY     Interface   Driver      Chipset
phy0    wlan0       rtw88_8812au   Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac

(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
(mac80211 station mode vif disabled for [phy0]wlan0)
```

이제 어댑터가 모니터 모드로 전환되었으며, 일반적으로 **wlan0mon**이라는 새 가상 인터페이스가 생성됩니다.

### 3단계 - 채널 지정(선택 사항이지만 권장)

기본적으로 어댑터는 여러 채널을 순회합니다. 특정 대상을 캡처하려면 채널을 고정하십시오.

```bash
sudo iwconfig wlan0mon channel 6
```

---

## 방법 2: iw로 모니터 모드 활성화

`iw` 명령어는 최신 저수준 무선 설정 유틸리티입니다. 보다 직접적인 제어가 가능하며, `airmon-ng`를 사용할 수 없거나 정상적으로 동작하지 않을 때 유용합니다.

```bash
# Bring the interface down
sudo ip link set wlan0 down

# Set monitor mode
sudo iw dev wlan0 set type monitor

# Bring the interface back up
sudo ip link set wlan0 up
```

세 명령어를 한 줄로 연결하면 다음과 같습니다.

```bash
sudo ip link set wlan0 down && sudo iw dev wlan0 set type monitor && sudo ip link set wlan0 up
```

이 방법은 새 `wlan0mon` 인터페이스를 생성하지 않고 기존 `wlan0` 인터페이스를 직접 변경합니다. 변경 사항이 적용되었는지 확인하십시오.

```bash
iw dev wlan0 info
```

출력에서 `type monitor`를 확인하십시오.

---

## 모니터 모드 확인

### iwconfig 사용

```bash
iwconfig
```

모니터 모드 인터페이스는 다음과 같이 표시됩니다.

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

핵심 항목은 **Mode:Monitor**입니다.

### iw dev 사용

```bash
iw dev
```

해당 인터페이스 항목 아래에 `type monitor`가 있는지 확인하십시오. `type managed`로 표시된다면 모니터 모드가 정상적으로 적용되지 않은 것입니다.

---

## airodump-ng로 테스트

모니터 모드가 활성화되면 `airodump-ng`로 전체 동작을 테스트하십시오.

```bash
sudo airodump-ng wlan0mon
```

주변 액세스 포인트 목록이 BSSID, 채널, 신호 강도(PWR), 암호화 방식, ESSID와 함께 화면에 실시간으로 표시되어야 합니다. 화면이 비어 있거나 오류가 표시된다면 아래 문제 해결 섹션을 참조하십시오.

5 GHz 대역만 스캔하려면:

```bash
sudo airodump-ng --band a wlan0mon
```

특정 네트워크를 캡처하고 이후 분석을 위해 결과를 저장하려면:

```bash
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
```

---

## ALFA 어댑터 호환성 표

[ALFA Network](/ko/products/alfa/) 어댑터는 Kali Linux 무선 테스트 분야의 업계 표준입니다. 다음 모델은 모니터 모드를 완전히 지원합니다.

| 모델 | 칩셋 | 대역 | 모니터 모드 | 인젝션 | 비고 |
|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | 2.4 / 5 GHz | ✅ | ✅ | 침투 테스트에서 가장 인기 있는 모델, 커널 6.13 이상 내장 드라이버 rtw88_8812au |
| AWUS036AXML | MT7921AUN | 2.4 / 5 / 6 GHz | ✅ | ❌ stock kernel 6.17에서 실패 | Wi-Fi 6E, 커널 5.18 이상 필요(mt7921u) |
| AWUS036ACM | MT7612U | 2.4 / 5 GHz | ✅ | ✅ | 우수한 Linux 드라이버 지원(mt76x2u) |

위 모델은 모두 Kali Linux 2024.x 및 2025.x에서 드라이버 지원이 확인되었습니다. RTL8812AU는 커널 6.13 이상에서 내장 드라이버 `rtw88_8812au`로 지원되므로 DKMS가 필요 없습니다. 6.13 미만의 구형 커널에서만 Aircrack-ng GitHub 저장소의 드라이버를 설치하면 됩니다.

---

## 문제 해결

### "Cannot enable monitor mode" 또는 인터페이스가 사라지는 경우

대부분 NetworkManager가 인터페이스를 다시 가져간 경우입니다. `airmon-ng check kill`을 다시 실행한 후 재시도하십시오. 문제가 계속되면 NetworkManager를 수동으로 중지하십시오.

```bash
sudo systemctl stop NetworkManager
sudo systemctl stop wpa_supplicant
```

### 모니터 모드가 관리 모드로 되돌아가는 경우

일부 드라이버는 몇 초 후 자동으로 관리 모드로 초기화됩니다. 보통 백그라운드에서 wpa_supplicant가 다시 시작된 경우입니다. 실행 중인 프로세스를 확인하십시오.

```bash
ps aux | grep -E "wpa_supplicant|NetworkManager"
```

발견된 프로세스를 PID로 종료한 후 모니터 모드를 다시 활성화하십시오.

### airmon-ng 실행 후 인터페이스 이름이 다른 경우

시스템에 따라 새 인터페이스 이름이 `wlan0mon`, `mon0` 또는 전혀 다른 이름일 수 있습니다. `airmon-ng start` 실행 후에는 항상 `iwconfig` 또는 `iw dev`로 실제 인터페이스 이름을 확인한 다음 airodump-ng에 사용하십시오.

### airodump-ng의 "Fixed channel wlan0mon: -1" 오류

airodump-ng가 채널을 변경하지 못한다는 의미입니다. 가장 흔한 원인은 규제 도메인(regulatory domain) 제한입니다. 해결 방법:

```bash
# Set a permissive regulatory domain (for authorized testing environments only)
sudo iw reg set BO
sudo airmon-ng stop wlan0mon
sudo airmon-ng start wlan0
```

그래도 해결되지 않으면 남아 있는 wpa_supplicant 프로세스를 종료한 후 다시 시도하십시오.

```bash
sudo iwconfig wlan0mon channel 1
```

### RTL8812AU 드라이버 관련 문제

커널 6.13 이상에서는 내장 드라이버 `rtw88_8812au`가 RTL8812AU를 지원하므로 DKMS나 외부 드라이버 설치가 필요 없습니다. 먼저 커널 버전과 모듈 로드 여부를 확인하십시오.

```bash
uname -r
lsmod | grep rtw88_8812au
```

6.13 미만의 구형 커널을 사용하는 경우에만 커뮤니티 드라이버를 설치하십시오.

```bash
sudo apt install dkms git
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

설치 후 재부팅하십시오.

---

## 작업 완료 후 모니터 모드 비활성화

테스트를 마치면 항상 어댑터를 관리 모드로 복원하십시오. 모니터 모드 상태로 두면 일반 네트워크 연결을 사용할 수 없습니다.

### airmon-ng 사용 시:

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

### iw 사용 시:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

`iwconfig`로 인터페이스가 관리 모드로 돌아왔는지 확인한 후 네트워크에 다시 연결하십시오.

---

{{< faq >}}

## 요약

Kali Linux에서 모니터 모드를 활성화하는 과정은 두 단계입니다. 방해 서비스를 중지한 다음 `airmon-ng` 또는 `iw`로 인터페이스 모드를 전환하면 됩니다. 성공의 핵심은 지원되는 칩셋을 탑재한 어댑터를 사용하는 것입니다. RTL8812AU, MT7921AUN, MT7612U 칩셋을 탑재한 ALFA Network 어댑터는 Kali Linux에서 가장 안정적인 즉시 사용 환경을 제공합니다.

대만의 ALFA Network 공식 유통사인 [Yopitek의 ALFA Network 무선 어댑터 전체 제품군](/ko/products/alfa/)을 살펴보고, 무선 보안 연구에 적합한 어댑터를 찾아보십시오.

## 참고 자료

1. [aircrack-ng 공식 문서](https://www.aircrack-ng.org/documentation.html)
2. [Kali Linux 공식 문서](https://www.kali.org/docs/)
3. [Linux Wireless mac80211 Subsystem](https://wireless.wiki.kernel.org/en/developers/Documentation/mac80211)
4. [iw 명령어 문서](https://wireless.wiki.kernel.org/en/users/Documentation/iw)
