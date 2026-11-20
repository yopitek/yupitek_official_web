---
title: "Kali Linux용 ALFA AWUS036ACH 설정 가이드: 모니터 모드 및 패킷 인젝션 (2026)"
description: "Kali Linux 2024/2025에 ALFA AWUS036ACH를 설치하고, airmon-ng로 모니터 모드를 활성화하며, 패킷 인젝션을 검증하는 단계별 가이드입니다. 드라이버 설치 명령어까지 모두 포함합니다."
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036ACH는 Kali Linux에서 별도의 드라이버가 필요한가요?"
    answer: "필요합니다. RTL8812AU는 메인라인 커널 드라이버가 아닙니다. aircrack-ng GitHub 저장소에서 설치하십시오. 커널 업데이트 후에도 유지되도록 DKMS 사용을 권장합니다."
  - question: "AWUS036ACH가 시스템에서 인식되었는지 어떻게 확인하나요?"
    answer: "lsusb를 실행하여 ID 0bda:8812를 찾으면 Realtek RTL8812AU가 인식된 것입니다. 그런 다음 lsmod로 드라이버 모듈이 로드되었는지 확인하십시오."
  - question: "모니터 모드를 활성화한 후 인터페이스가 사라지면 어떻게 해야 하나요?"
    answer: "보통 NetworkManager가 인터페이스를 다시 가져간 경우입니다. airmon-ng check kill을 실행하여 방해 프로세스를 중지한 다음 모니터 모드를 다시 활성화하십시오."
  - question: "정상으로 간주되는 패킷 인젝션 성공률은 어느 정도인가요?"
    answer: "80% 이상이면 안정적으로 동작하는 것입니다. 50% 미만이라면 안테나 위치, USB 전원 공급, 또는 드라이버 설치 상태를 점검하는 것이 좋습니다."
  - question: "커널 업데이트 후 AWUS036ACH 드라이버가 동작하지 않을 때 어떻게 해결하나요?"
    answer: "DKMS로 설치한 경우 드라이버가 자동으로 재빌드됩니다. 실패하면 dkms autoinstall을 실행하고 linux-headers가 현재 커널 버전과 일치하는지 확인하십시오."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "kali-linux", "monitor-mode", "packet-injection", "RTL8812AU", "airmon-ng"]
featureimage: "/images/blog/awus036ach-kali-linux-setup.webp"
---

Kali에서 AWUS036ACH를 설정할 때 대부분의 사용자는 세 가지 벽에 부딪힙니다. 드라이버가 컴파일되지 않거나, VM이 USB 장치를 패스스루하지 못하거나, 모니터 모드가 아무 메시지 없이 실패하는 경우입니다. 본 가이드는 이 세 가지를 모두 다루며, 처음부터 끝까지 완전히 동작하는 설정 과정도 함께 안내합니다.

{{< tldr >}}
RTL8812AU 칩셋을 탑재한 AWUS036ACH는 aircrack-ng 드라이버와 DKMS로 설치하면 모니터 모드와 패킷 인젝션을 안정적으로 활성화할 수 있습니다. Kali Linux 침투 테스트의 표준 장비입니다.
{{< /tldr >}}




---

{{< alert "circle-info" >}}
Kali를 **VirtualBox 또는 VMware**에서 실행하고 계십니까? 먼저 [USB 패스스루](#usb-passthrough-in-virtualbox-and-vmware) 섹션으로 이동하십시오. 가장 흔한 설정 실패 지점입니다. 호스트 OS로 **macOS** 또는 **Windows**를 사용하는 경우 [macOS에서의 ALFA](/ko/blog/alfa-adapter-macos-vm-setup/) 또는 [Windows에서의 ALFA](/ko/blog/alfa-adapter-windows-10-11-setup/) 가이드를 참조하십시오.
{{< /alert >}}

---

## AWUS036ACH가 대표적인 선택지인 이유

명령어를 다루기에 앞서, 이 어댑터를 특별하게 만드는 요소가 정확히 무엇인지 이해해 둘 가치가 있습니다.

**RTL8812AU 칩셋**

Realtek의 RTL8812AU는 듀얼 밴드(2.4 + 5 GHz) 802.11ac 칩셋으로, 보안 도구가 요구하는 프레임 수준의 작업을 견고하게 지원합니다. GitHub의 `aircrack-ng/rtl8812au`에서 유지보수되는 오픈소스 드라이버는 Aircrack-ng 팀과 폭넓은 Linux 보안 커뮤니티가 수년에 걸쳐 협력한 직접적인 결과물입니다. 이 드라이버는 활발하게 유지보수되고, 새로운 커널 버전에 대해 정기적으로 테스트되며, 모니터 모드와 패킷 인젝션을 부가 기능이 아니라 명시적으로 지원하도록 설계되어 있습니다.

**2017년부터 이어진 커뮤니티 지원**

AWUS036ACH에서 문제가 발생하면 답을 찾을 수 있습니다. 이 어댑터는 수천 건의 포럼 게시물, YouTube 튜토리얼, Hack The Box 공략, Offensive Security 교육 자료, GitHub 이슈에 등장합니다. 다른 어떤 어댑터도 따라올 수 없는 수준의 문제 해결 지식 기반을 갖추고 있습니다.

**AC1200 듀얼 밴드 성능**

이 어댑터는 2.4 GHz에서 최대 300 Mbps, 5 GHz에서 최대 867 Mbps를 제공하며, 2×2 MIMO를 지원하는 두 개의 분리형 RP-SMA 안테나를 갖추고 있습니다. 필요할 때 실질적인 고속 처리 성능을 발휘하는 동시에 완전한 침투 테스트 기능도 제공합니다.

**USB 3.0**

USB 3.0 인터페이스는 대용량 캡처를 수행하거나 여러 도구를 동시에 실행할 때 어댑터가 병목 지점이 되는 것을 방지합니다.

당사 스토어에서 확인하실 수 있습니다: [ALFA AWUS036ACH](/ko/products/alfa/awus036ach/).

---

## 사전 준비 사항

시작하기 전에 다음 사항을 확인하십시오.

- **Kali Linux 2024.x 이상** (본 가이드는 Kali 2024.1부터 2025.1까지에서 테스트되었습니다)
- **USB 3.0 포트** — 어댑터는 USB 2.0에서도 동작하지만 처리량이 제한됩니다. 최상의 결과를 위해 USB 3.0을 사용하십시오.
- 드라이버 다운로드를 위한 **인터넷 연결**
- **root 또는 sudo 권한**
- **빌드 도구 설치** — 2단계에서 다룹니다

Kali를 가상 머신(VMware, VirtualBox, UTM)에서 실행하는 경우, USB 장치를 VM으로 패스스루해야 합니다. VMware에서는 VM → Removable Devices → 어댑터 연결을 선택합니다. VirtualBox에서는 Settings → USB에서 Realtek 장치에 대한 USB 필터를 추가합니다.

---

## VirtualBox 및 VMware에서의 USB 패스스루

### VirtualBox

VirtualBox에서 USB 3.0을 지원하려면 **Extension Pack**이 필요합니다. 이것이 없으면 USB 2.0만 패스스루할 수 있으며, 이 경우 AWUS036ACH에서 아무 메시지 없는 실패가 발생하거나 처리량이 저하됩니다.

1. [virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)에서 Extension Pack을 다운로드합니다. 사용 중인 VirtualBox 버전과 정확히 일치해야 합니다.
2. 설치: **File → Tools → Extension Pack Manager → Install**
3. Kali VM 설정에서: **USB → Enable USB Controller → USB 3.0 (xHCI)**
4. 어댑터를 연결한 상태에서 USB Device Filter를 추가합니다: **Settings → USB → "+" 아이콘 클릭**

```bash
# VM 내부에서 어댑터가 보이는지 확인
lsusb | grep -E "0bda|Realtek"
# 예상 출력: Bus 002 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

### VMware Workstation / Player

VMware는 기본적으로 VirtualBox보다 USB 패스스루를 더 잘 처리하지만, 호스트에서 **VMware USB Arbitrator** 서비스가 실행 중이어야 합니다.

```bash
# Windows 호스트 — 서비스 실행 여부 확인
sc query VMwareUSBArbitrator

# 중지된 경우:
sc start VMwareUSBArbitrator
```

VM에서: **VM 메뉴 → Removable Devices → ALFA AWUS036ACH → Connect**

```bash
# Kali 내부에서 성공 여부 확인
lsusb | grep -E "0bda|Realtek"
dmesg | tail -10
```

---

## 1단계: 어댑터 연결 및 인식 확인

AWUS036ACH를 USB 포트에 연결하고 다음을 실행합니다.

```bash
lsusb
```

다음과 유사한 항목이 보여야 합니다.

```
Bus 001 Device 004: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

중요한 식별자는 다음과 같습니다.
- **Vendor ID:** `0bda` (Realtek)
- **Product ID:** `8812` (RTL8812AU)

장치가 전혀 나타나지 않으면 다른 USB 포트나 케이블을 사용해 보십시오. 다른 Product ID로 나타난다면 다른 하드웨어 리비전일 수 있습니다.

연결 직후 커널 메시지 로그도 확인하십시오.

```bash
dmesg | tail -20
```

드라이버가 이미 로드되어 있다면(새로 설치한 Kali에서는 드문 경우입니다) 다음과 같은 줄이 보입니다.

```
usb 1-1: new high-speed USB device number 4 using xhci_hcd
usbcore: registered new interface driver rtl88XXau
```

드라이버가 설치되지 않은 경우에는 USB 장치는 감지되지만 인터페이스는 생성되지 않은 상태로 표시됩니다.

---

## 2단계: RTL8812AU 드라이버 설치

설치 방법은 두 가지입니다. **방법 A(aircrack-ng 드라이버)**는 Kali Linux에 권장됩니다. **방법 B(DKMS)**는 커널 업데이트 전반에 걸쳐 드라이버를 자동으로 유지하고자 할 때 권장됩니다.

### 빌드 종속성 설치

두 방법 모두 동일한 종속성을 필요로 합니다.

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r)
```

이 명령은 현재 실행 중인 커널과 일치하는 커널 헤더를 설치하며, 드라이버 빌드 과정에 이 헤더가 필요합니다.

### 방법 A: 직접 설치 (aircrack-ng 드라이버 — Kali 권장)

```bash
# aircrack-ng가 유지보수하는 드라이버 복제
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au

# 드라이버 빌드
make

# 드라이버 설치
sudo make install

# 드라이버 모듈 로드
sudo modprobe 88XXau
```

모듈이 로드되었는지 확인합니다.

```bash
lsmod | grep 88XXau
```

예상 출력:

```
88XXau               3461120  0
cfg80211             1081344  1 88XXau
```

이제 무선 인터페이스가 나타나야 합니다.

```bash
ip link show
# 또는
iwconfig
```

새 인터페이스가 보여야 합니다. 다른 무선 인터페이스가 있는 경우 일반적으로 `wlan0` 또는 `wlan1`로 표시됩니다.

### 방법 B: DKMS 설치 (커널 업데이트 전반에 걸쳐 유지)

일반적인 `make install`을 사용하면 드라이버 모듈이 현재 커널에 대해서만 컴파일됩니다. Kali가 커널을 업데이트하면(`apt upgrade`를 통해 정기적으로 발생합니다) 재컴파일할 때까지 드라이버가 동작하지 않습니다.

DKMS(Dynamic Kernel Module Support)는 새 커널이 설치될 때마다 드라이버를 자동으로 재컴파일하여 이 문제를 해결합니다.

```bash
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au

# DKMS 설치 스크립트 사용
sudo make dkms_install
```

또는 수동으로 DKMS에 등록할 수 있습니다.

```bash
# 드라이버 버전 확인
grep MODULE_VERSION Makefile | head -1
# 출력 예시: v5.6.4.2

# 소스를 DKMS 디렉터리로 복사
sudo cp -r ../rtl8812au /usr/src/rtl8812au-5.6.4.2

# DKMS에 등록
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2
```

DKMS 등록을 확인합니다.

```bash
dkms status
# 예상: rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

---

## 3단계: 모니터 모드 활성화

드라이버가 로드되고 인터페이스가 보이면 모니터 모드를 활성화할 준비가 된 것입니다.

### 방법 A: airmon-ng (권장)

먼저 모니터 모드를 방해할 수 있는 프로세스를 모두 종료합니다.

```bash
sudo airmon-ng check kill
```

이 명령은 인터페이스를 점유하고 있는 NetworkManager, wpa_supplicant 및 기타 데몬을 중지합니다. 예상 출력:

```
Killing these processes:
  PID Name
  1234 NetworkManager
  1235 wpa_supplicant
```

이제 모니터 모드를 시작합니다.

```bash
sudo airmon-ng start wlan0
```

인터페이스 이름이 다른 경우 `wlan0`을 실제 인터페이스 이름으로 바꾸십시오. 예상 출력:

```
PHY     Interface   Driver      Chipset
phy0    wlan0       88XXau      Realtek Semiconductor Corp. RTL8812AU

                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)
```

모니터 모드 인터페이스의 이름은 `wlan0mon`입니다.

### 방법 B: iw (수동)

NetworkManager를 종료하고 싶지 않거나 airmon-ng를 사용할 수 없는 경우:

```bash
# 인터페이스 내리기
sudo ip link set wlan0 down

# 모니터 모드로 전환
sudo iw dev wlan0 set type monitor

# 다시 올리기
sudo ip link set wlan0 up
```

모니터 모드를 활성화하면서 채널을 지정하려면:

```bash
sudo iw dev wlan0 set channel 6
```

---

## 4단계: 모니터 모드 검증

인터페이스가 모니터 모드인지 확인합니다.

```bash
iwconfig
```

`wlan0mon`(또는 `wlan0`) 항목을 찾으십시오. 다음과 같이 표시되어야 합니다.

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

핵심 지표는 `Mode:Monitor`입니다. `Mode:Managed`로 표시된다면 모니터 모드가 활성화되지 않은 것입니다.

다음 명령도 사용할 수 있습니다.

```bash
iw dev wlan0mon info
```

예상 출력에 다음이 포함됩니다.

```
type monitor
```

### Airodump-ng로 검증

빠른 스캔을 실행하여 어댑터가 트래픽을 캡처하는지 확인합니다.

```bash
sudo airodump-ng wlan0mon
```

출력에 WiFi 네트워크가 즉시 나타나야 합니다. `Ctrl+C`를 눌러 중지합니다.

---

## 5단계: 패킷 인젝션 테스트

패킷 인젝션은 임의의 802.11 프레임을 전송하는 기능입니다. aireplay-ng의 인젝션 테스트를 사용합니다.

```bash
sudo aireplay-ng --test wlan0mon
```

이 명령은 테스트 프레임을 브로드캐스트하고 인근 액세스 포인트의 응답을 수신합니다. 성공한 경우 다음과 같이 표시됩니다.

```
15:42:11  Trying broadcast probe requests...
15:42:11  Injection is working!
15:42:12  Found 3 APs

15:42:12  Trying directed probe requests...
15:42:12  aa:bb:cc:dd:ee:ff - channel: 6 - 'HomeNetwork' - 30/30: 100%
15:42:13  11:22:33:44:55:66 - channel: 11 - 'OfficeWiFi' - 28/30: 93%
```

백분율은 인젝션 성공률을 나타냅니다. 인근 AP의 경우 80% 이상이면 허용 가능한 수준입니다. 통신 범위 내에 있을 때는 100%가 일반적입니다.

출력에 `Injection is working!`이 보이면 설정이 완료되어 전체 Aircrack-ng 제품군과 함께 사용할 준비가 된 것입니다.

### 듀얼 밴드 인젝션 테스트 (5 GHz)

5 GHz에서 인젝션을 테스트하려면 채널을 지정합니다.

```bash
# 5 GHz 채널로 전환(예: 채널 36)
sudo iwconfig wlan0mon channel 36
# 또는
sudo iw dev wlan0mon set channel 36

# 인젝션 테스트 실행
sudo aireplay-ng --test wlan0mon
```

---

## 문제 해결

### "Interface not found" / 드라이버 설치 후 wlan 인터페이스가 없음

**원인:** 드라이버 모듈이 정상적으로 로드되지 않았습니다.

**해결 방법:**

```bash
# 모듈 로드 오류 확인
dmesg | grep -i 88XX
dmesg | grep -i rtl

# 모듈 수동 로드 시도
sudo modprobe 88XXau

# modprobe가 실패하면 누락된 종속성 확인
modinfo 88XXau

# 드라이버 재빌드
cd rtl8812au
make clean && make && sudo make install
```

커널 헤더가 실행 중인 커널과 일치하는지도 확인하십시오.

```bash
uname -r
ls /lib/modules/$(uname -r)/build
```

`build` 디렉터리가 없으면 헤더를 다시 설치하십시오.

```bash
sudo apt install linux-headers-$(uname -r)
```

---

### 모니터 모드 활성화 시 "Operation not permitted"

**원인:** root로 실행하고 있지 않거나 권한(capability)이 누락되었습니다.

**해결 방법:**

airmon-ng 및 aireplay-ng는 항상 `sudo`와 함께 사용하십시오.

```bash
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

이미 root로 실행 중이라면 Kali 사용자가 실제로 root인지 확인하십시오.

```bash
whoami
# 출력되어야 하는 값: root
```

---

### "No module named rtl8812au" / 커널 업데이트 후 DKMS 실패

**원인:** DKMS가 새 커널용으로 드라이버를 재컴파일하지 않았습니다.

**해결 방법:**

```bash
# DKMS 상태 확인
dkms status

# rtl8812au가 새 커널에 대해 "built"로만 표시되고 "installed"가 아닌 경우:
sudo dkms install rtl8812au/5.6.4.2 -k $(uname -r)

# 그래도 실패하면 제거 후 재설치:
sudo dkms remove rtl8812au/5.6.4.2 --all
cd /path/to/rtl8812au
sudo make dkms_install
```

---

### 모니터 모드는 시작되지만 트래픽이 캡처되지 않음

**원인:** 잘못된 채널, 간섭, 또는 규제 도메인 문제입니다.

**해결 방법:**

```bash
# 현재 채널 확인
iwconfig wlan0mon

# 채널 수동 설정
sudo iwconfig wlan0mon channel 1

# 규제 도메인 확인
iw reg get

# 허용 범위가 넓은 규제 도메인 설정(책임감 있게 사용)
sudo iw reg set BO
```

---

### 낮은 인젝션 성공률 (50% 미만)

**원인:** AP와의 거리, 간섭, 또는 전원 관리 문제입니다.

**해결 방법:**

```bash
# 인터페이스의 전원 관리 비활성화
sudo iwconfig wlan0mon power off

# TX 전력 증가(사용 전 현지 규정 확인)
sudo iw dev wlan0mon set txpower fixed 3000  # 30 dBm
```

---

## 관리 모드 복원

테스트를 마치고 정상적으로 네트워크에 다시 연결하고자 할 때:

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

또는 iw를 사용할 경우:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

---

{{< faq >}}

## 요약

| 단계 | 명령어 |
|---|---|
| 인식 확인 | `lsusb \| grep Realtek` |
| 종속성 설치 | `sudo apt install git dkms build-essential linux-headers-$(uname -r)` |
| 드라이버 복제 | `git clone https://github.com/aircrack-ng/rtl8812au` |
| 빌드 및 설치 | `make && sudo make install` |
| 모듈 로드 | `sudo modprobe 88XXau` |
| 방해 프로세스 종료 | `sudo airmon-ng check kill` |
| 모니터 모드 활성화 | `sudo airmon-ng start wlan0` |
| 모니터 모드 검증 | `iwconfig wlan0mon` |
| 인젝션 테스트 | `sudo aireplay-ng --test wlan0mon` |
| 예상 소요 시간 | 약 15분 (깨끗한 시스템 기준) |

[ALFA AWUS036ACH](/ko/products/alfa/awus036ach/)는 Kali Linux 2024 이상 및 aircrack-ng RTL8812AU 드라이버와 함께 사용할 때 침투 테스트 커뮤니티에서 가장 안정적이고 가장 잘 문서화된 WiFi 어댑터 설정으로 꼽힙니다. 인젝션이 정상 동작함을 확인하고 나면, 전체 Aircrack-ng 제품군, Wireshark, Kismet, Bettercap을 비롯해 모니터 모드나 패킷 인젝션이 필요한 모든 도구를 사용할 준비가 된 것입니다.

## 참고 문헌

1. [aircrack-ng 공식 rtl8812au 드라이버 저장소](https://github.com/aircrack-ng/rtl8812au)
2. [Kali Linux 공식 문서](https://www.kali.org/docs/)
3. [Realtek RTL8812AU 사양](https://www.realtek.com/)
4. [Linux Wireless 공식 문서](https://wireless.wiki.kernel.org/)
