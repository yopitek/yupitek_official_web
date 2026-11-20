---
title: "중국 환경을 위한 ALFA AWUS036ACM 드라이버 설치 가이드: Kali Linux, Ubuntu, Debian 및 Raspberry Pi"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036ACM은 어떤 칩셋을 사용하며 드라이버가 필요합니까?"
    answer: "MediaTek MT7612U 칩셋을 사용합니다. mt76x2u 드라이버는 Linux 커널 4.19부터 내장되어 있습니다. 대부분의 경우 플러그 앤 플레이로 동작합니다."
  - question: "AWUS036ACM은 VIF 가상 인터페이스를 지원합니까?"
    answer: "예. MT7612U는 커널 네이티브 VIF를 완전히 지원하므로, 패치 없이 모니터 모드와 매니지드 모드 인터페이스를 동시에 운용할 수 있습니다."
  - question: "중국에서 AWUS036ACM을 설치하려면 VPN이 필요합니까?"
    answer: "아니요. 드라이버는 이미 커널에 포함되어 있습니다. 국내(중국) 미러에서 firmware-misc-nonfree 패키지만 설치하면 됩니다."
  - question: "Raspberry Pi에서 AWUS036ACM은 전력을 얼마나 소비합니까?"
    answer: "최대 부하 시 약 400mW입니다. Pi의 스로틀링을 방지하기 위해 전원 공급형 USB 허브 사용을 권장합니다."
  - question: "Debian이 AWUS036ACM을 인식하는데도 동작하지 않는 이유는 무엇입니까?"
    answer: "firmware-misc-nonfree 패키지가 누락되었기 때문입니다. 이를 설치하면 어댑터가 정상적으로 초기화됩니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acm-china-install-guide"
tags: ["alfa", "awus036acm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "vif"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 2
description: "국내(중국) 미러를 사용해 중국 환경에서 ALFA AWUS036ACM 드라이버를 설치하는 단계별 가이드입니다. MT7612U 커널 내장 드라이버, 완전한 VIF 지원. Kali Linux, Ubuntu 22/24, Debian, Raspberry Pi를 모두 다룹니다. GitHub가 필요 없습니다."
related_product: "/ko/products/alfa/awus036acm/"
featureimage: "/images/blog/awus036acm-china-install-guide.webp"
---

AWUS036ACM은 Linux에서 설정하기 가장 쉬운 Alfa 어댑터 중 하나입니다. MT7612U 칩은 `mt76x2u` 드라이버를 사용하며, 이 드라이버는 Linux 커널 4.19 버전부터 커널에 내장되어 있습니다. 대부분의 최신 시스템에서 어댑터는 명령어 두세 개만으로 동작합니다. 이 가이드는 국내(중국) 미러만을 사용하여 드라이버 확인, 모니터 모드, 패킷 인젝션, VIF까지 전체 설정 과정을 다룹니다. GitHub가 필요 없습니다.

{{< tldr >}}
MT7612U 칩셋을 탑재한 AWUS036ACM은 컴파일이 필요 없는 커널 내장 드라이버를 갖추고 있습니다. 모니터 모드, 패킷 인젝션, 동시 VIF 운용을 지원합니다. 중국에서는 펌웨어 패키지만 설치하면 됩니다.
{{< /tldr >}}

다음 항목이 준비되어 있는지 확인하십시오.




## 시작하기 전에

다음 항목이 준비되어 있는지 확인하십시오.

1. **ALFA AWUS036ACM** 어댑터
2. USB 케이블(제품 상자에 동봉된 케이블로 충분합니다)
3. 전원 공급형 USB 허브 — Raspberry Pi를 사용하는 경우 필수입니다
4. 국내(중국) 미러에 접속하기 위한 인터넷 연결

어댑터를 연결한 뒤, 시스템이 이를 인식하는지 확인하십시오.

```bash
lsusb
```

출력에서 다음 항목을 찾으십시오.

```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.
```

`0e8d:7612`가 보이면 어댑터가 감지된 것입니다. 아래에서 사용 중인 운영체제에 해당하는 섹션으로 이동하십시오.

보이지 않는다면 다른 USB 포트를 사용하거나 케이블을 교체한 뒤 `lsusb`를 다시 실행하십시오.

## 운영체제 선택

사용 중인 운영체제에 맞는 섹션으로 이동하십시오.

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

이미 설치했다면 다음 섹션으로 건너뛰십시오.

- [모니터 모드 활성화](#enable-monitor-mode)
- [패킷 인젝션 테스트](#test-packet-injection)
- [가상 인터페이스(VIF)](#virtual-interface-vif)
- [VM USB 패스스루](#virtual-machine-usb-passthrough)

---

## Kali Linux

MT7612U 드라이버는 이미 Kali 커널에 포함되어 있습니다. 대부분의 경우 어댑터를 연결하는 즉시 동작합니다. 아래 단계는 드라이버가 로드되었는지 확인하고 모니터 모드까지 안내합니다.

### 1단계: 중국 미러로 전환

터미널에서 소스 목록 파일을 엽니다.

```bash
sudo nano /etc/apt/sources.list
```

기존 내용을 모두 삭제한 뒤, 다음 줄을 붙여넣습니다.

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

저장하려면 **Ctrl+O**를 누른 뒤 Enter를, 종료하려면 Ctrl+X를 누릅니다. 그리고 패키지 인덱스를 갱신합니다.

```bash
sudo apt update
```

> **백업 미러:** 중국과학기술대학(USTC) 미러가 느리다면 칭화대학(Tsinghua) 미러를 대신 사용하십시오.
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 2단계: 드라이버 확인

어댑터를 연결했을 때 모듈이 자동으로 로드되었는지 확인합니다.

```bash
lsmod | grep mt76
```

`mt76x2u`가 포함된 출력이 보여야 합니다. 아무것도 나타나지 않으면 수동으로 로드하십시오.

```bash
sudo modprobe mt76x2u
```

`lsmod | grep mt76`를 다시 실행하여 확인합니다. 그런 다음 어댑터가 활성화되었는지 확인합니다.

```bash
iwconfig
```

무선 인터페이스(일반적으로 `wlan0` 또는 `wlan1`)를 찾으십시오. 해당 인터페이스가 ESSID 또는 `unassociated` 상태로 표시되면 드라이버가 정상적으로 동작하고 있는 것입니다.

---

### 2단계(대안): 추가 커널 모듈 설치

`modprobe mt76x2u` 실행 시 "Module not found" 오류가 발생한다면, 사용 중인 커널 빌드에 MT76 모듈이 누락되어 있을 수 있습니다. 중국 미러에서 설치하십시오.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
```

설치가 완료되면 모듈을 다시 로드합니다.

```bash
sudo modprobe mt76x2u
```

사용 중인 정확한 커널 버전에 해당하는 패키지를 사용할 수 없다면, 대신 더 최신 커널로 업그레이드하십시오. 해당 드라이버는 메인라인 Linux 커널의 일부이므로 컴파일이 필요 없습니다.

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

> **참고:** `mt76x2u`는 메인라인 Linux 커널의 일부이므로 소스 빌드가 필요 없습니다. 드라이버 아카이브는 [files.alfa.com.tw](https://files.alfa.com.tw)에서 직접 내려받을 수도 있습니다.

---

### 3단계: 모니터 모드 활성화 {#enable-monitor-mode}

모니터 모드로 전환하기 전에, 시스템이 어댑터에 어떤 인터페이스 이름을 할당했는지 확인하십시오.

```bash
iwconfig
```

`wlan0` 또는 `wlan1`을 찾으십시오. 아래 명령어에서 해당 이름을 사용합니다.

NetworkManager와 wpa_supplicant가 간섭하지 않도록 중지합니다.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

전환되었는지 확인합니다.

```bash
iwconfig
```

`Mode:Monitor`로 표시된 `wlan0mon` 같은 항목을 찾으십시오. 이것이 보이면 어댑터는 패킷 캡처 준비가 된 것입니다.

---

### 4단계: 패킷 인젝션 테스트 {#test-packet-injection}

모니터 인터페이스를 대상으로 인젝션 테스트를 실행합니다.

```bash
sudo aireplay-ng --test wlan0mon
```

성공한 결과는 다음과 같습니다.

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

테스트가 실패하면 재부팅 후 다시 실행하십시오. 그래도 실패한다면 `iwconfig`로 다른 프로세스가 인터페이스를 점유하고 있지 않은지 확인하십시오.

---

## Ubuntu 22.04 / 24.04

MT7612U 드라이버는 Ubuntu 커널에도 포함되어 있지만, 기본 커널 이미지가 아니라 `linux-modules-extra` 패키지에 들어 있을 수 있습니다. 아래 단계는 두 경우를 모두 처리합니다.

### 1단계: 중국 미러로 전환

#### Ubuntu 24.04 (Noble)

DEB822 형식의 소스 파일을 엽니다.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

모든 내용을 삭제하고 다음을 붙여넣습니다.

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

`Ctrl+O`로 저장한 뒤 `Ctrl+X`로 종료합니다.

#### Ubuntu 22.04 (Jammy)

기존 형식의 소스 파일을 엽니다.

```bash
sudo nano /etc/apt/sources.list
```

모든 줄을 다음으로 교체합니다.

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

저장하고 종료합니다(`Ctrl+O`, `Ctrl+X`).

#### 패키지 인덱스 갱신

```bash
sudo apt update
```

---

### 2단계: 드라이버 로드

먼저 모듈을 직접 로드해 봅니다.

```bash
sudo modprobe mt76x2u
```

"Module not found" 오류가 발생하면 추가 모듈 패키지를 설치합니다.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

어댑터가 인식되는지 확인합니다.

```bash
iwconfig
```

출력에 `wlan0` 또는 `wlan1` 같은 인터페이스가 나타나면 드라이버가 활성화된 것입니다.

---

### 3단계: 무선 도구 설치

모니터 모드 및 인젝션 테스트를 위해 aircrack-ng를 설치합니다.

```bash
sudo apt install -y aircrack-ng
```

---

### 4단계: 모니터 모드 활성화

간섭하는 프로세스를 종료한 뒤 모니터 모드를 시작합니다.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

> **참고:** 다른 무선 카드가 있는 경우 인터페이스가 `wlan1`일 수 있습니다. 먼저 `iwconfig`를 실행하여 확인하십시오.

---

### 5단계: 패킷 인젝션 테스트

```bash
sudo aireplay-ng --test wlan0mon
```

성공한 결과에는 `Injection is working!`가 표시됩니다. 인터페이스 오류가 보이면 `iwconfig wlan0mon`으로 모니터 모드가 활성화되어 있는지 확인하십시오.

---

## Debian

MT7612U 드라이버는 Debian 커널에 포함되어 있지만, 완전히 초기화하려면 `firmware-misc-nonfree` 패키지가 필요한 경우가 있습니다.

### 1단계: 중국 미러로 전환

소스 목록 파일을 엽니다.

```bash
sudo nano /etc/apt/sources.list
```

모든 내용을 삭제하고 다음 세 줄을 붙여넣습니다(Debian 12 Bookworm).

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

`Ctrl+O`로 저장한 뒤 `Ctrl+X`로 종료합니다. 그리고 갱신합니다.

```bash
sudo apt update
```

### 2단계: Non-Free 펌웨어 설치

MT7612U는 `firmware-misc-nonfree` 패키지의 펌웨어 파일을 필요로 합니다. 이것이 없으면 어댑터는 초기화되지만 연결되지 않거나 모니터 모드로 전환되지 않을 수 있습니다.

```bash
sudo apt install -y firmware-misc-nonfree
```

### 3단계: 드라이버 로드

```bash
sudo modprobe mt76x2u
```

모듈이 누락되어 있다면 먼저 추가 커널 모듈을 설치합니다.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

인터페이스가 나타났는지 확인합니다.

```bash
iwconfig
```

### 4단계: 모니터 모드 활성화

```bash
sudo apt install -y aircrack-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

`iwconfig`로 모니터 모드를 확인하십시오. `Mode:Monitor`로 표시된 `wlan0mon`을 찾으십시오.

### 5단계: 패킷 인젝션 테스트

```bash
sudo aireplay-ng --test wlan0mon
```

`Injection is working!`가 표시되면 어댑터가 완전히 동작하고 있는 것입니다.

---

## Raspberry Pi 4B / 5

> AWUS036ACM은 부하 시 약 400mW를 소비합니다. Pi의 스로틀링을 방지하기 위해 전원 공급형 USB 허브를 사용하십시오.

---

### 1단계: Kali Linux ARM64 이미지 다운로드

공식 Kali ARM 다운로드 페이지로 이동하십시오.
https://www.kali.org/get-kali/#kali-arm

**Raspberry Pi 4 (64-bit)** 또는 **Raspberry Pi 5 (64-bit)**를 선택하십시오. 32비트 이미지는 사용하지 마십시오. 반드시 64비트가 필요합니다.

> **중국 미러:** kali.org가 느리다면 화웨이 클라우드(Huawei Cloud)를 사용하십시오.
> https://repo.huaweicloud.com/kali-images/
> 최신 릴리스 폴더로 이동하여 그곳에서 ARM64 이미지를 내려받으십시오.

---

### 2단계: MicroSD에 기록

먼저 카드의 장치 경로를 확인합니다.

```bash
lsblk
```

그런 다음 `/dev/sdX`를 실제 카드 경로로 바꿔 기록합니다.

```bash
# /dev/sdX를 실제 SD 카드 경로로 바꾸십시오 (lsblk로 확인)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

`sync`가 완료될 때까지 기다린 뒤 부팅합니다. 기본 자격 증명: **kali / kali**.

---

### 3단계: 중국 미러로 전환

```bash
sudo nano /etc/apt/sources.list
```

내용을 다음으로 교체합니다.

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

저장하고 적용합니다.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

### 4단계: 드라이버 확인

재부팅 후 어댑터를 연결하고 확인합니다.

```bash
lsmod | grep mt76
```

`mt76x2u`가 나타나면 완료입니다. 그렇지 않다면 다음을 실행합니다.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

---

### 5단계: 모니터 모드 활성화

내장 Wi-Fi가 있는 Pi에서는 내장 라디오가 `wlan0`을 차지하므로 AWUS036ACM이 `wlan1`로 표시됩니다.

```bash
iwconfig
```

인터페이스 이름을 확인한 뒤, 해당 인터페이스에서 모니터 모드를 시작합니다.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

`iwconfig`로 확인하십시오. `Mode:Monitor`로 표시된 `wlan1mon`을 찾으십시오.

---

### 6단계: 패킷 인젝션 테스트

```bash
sudo aireplay-ng --test wlan1mon
```

`Injection is working!`가 표시되면 완전히 동작하는 것입니다. 실패하면 전원 공급형 허브를 사용하고 있는지 다시 확인하십시오.

---

## 가상 머신 USB 패스스루 {#virtual-machine-usb-passthrough}

### VirtualBox

1. VM을 종료합니다. **Settings → USB**로 이동합니다.
2. **USB 3.0 (xHCI) Controller**를 활성화합니다.
3. **+**를 클릭하여 USB 필터를 추가합니다.
4. **MediaTek Inc. MT7612U** (ID: 0e8d:7612)를 선택합니다.
5. VM을 시작하면 어댑터가 Kali 내부에 나타납니다.

VM에서 `lsusb`를 실행하여 `0e8d:7612`를 확인한 뒤, 위의 Kali 단계를 따르십시오.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. VM을 시작합니다.
2. 메뉴: **Virtual Machine → USB & Bluetooth**.
3. **MediaTek MT7612U**를 찾아 **Connect**를 클릭합니다.
4. VM에서 `lsusb`를 실행하여 확인한 뒤, 위의 Kali 단계를 따르십시오.

---

## 가상 인터페이스(VIF) {#virtual-interface-vif}

이 부분이 AWUS036ACM이 ACH보다 앞서는 지점입니다. MT7612U 칩은 완전한 커널 네이티브 VIF를 지원합니다. 하나의 어댑터에서 모니터 인터페이스와 매니지드 또는 AP 인터페이스를 동시에 운용할 수 있습니다. 패치도, 편법도 필요 없습니다.

### 두 번째 가상 인터페이스 생성

어댑터가 `wlan0`으로 매니지드 모드에 있는 상태에서, 그 옆에 모니터 인터페이스를 추가합니다.

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

이제 두 인터페이스가 모두 활성화되었는지 확인합니다.

```bash
iwconfig
```

`wlan0`(연결됨, 매니지드 모드)과 `mon0`(모니터 모드)가 모두 보여야 합니다. 어댑터가 두 가지를 동시에 수행하고 있는 것입니다.

### 활용 사례: 연결을 유지하면서 모니터링

이를 통해 `wlan0`이 네트워크에 연결된 상태를 유지하는 동안 `mon0`에서 트래픽을 캡처할 수 있습니다. 상관 분석에 유용합니다.

```bash
sudo airodump-ng mon0
```

`wlan0`은 정상적인 연결을 유지하고, `mon0`은 범위 내의 모든 것을 캡처합니다.

### 활용 사례: 가짜 AP + 모니터

AP 인터페이스와 모니터 인터페이스를 함께 생성합니다.

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

`iwconfig`를 실행하여 세 인터페이스(`wlan0`, `ap0`, `mon0`)가 모두 활성화되었는지 확인하십시오.

> **hostapd에 대한 참고:** 완전한 AP 운용에는 `hostapd` 구성이 필요합니다. 이는 이 가이드의 범위를 벗어납니다. 위 단계는 어댑터가 인터페이스를 생성할 수 있음을 확인하는 것이며, 실제 AP 구성은 별도의 주제입니다.

---

{{< faq >}}

## 문제 해결

| 문제 | 가능한 원인 | 해결 방법 |
|---------|-------------|-----|
| `lsusb`에 0e8d:7612가 표시되지 않음 | 어댑터에 전원이 공급되지 않거나 케이블 불량 | 다른 USB 포트를 사용하십시오. Raspberry Pi에서는 전원 공급형 허브를 사용하십시오. |
| `modprobe mt76x2u`가 "Module not found" 출력 | 커널에 추가 모듈이 누락됨 | `sudo apt install linux-modules-extra-$(uname -r)`를 실행하십시오 |
| 인터페이스는 나타나지만 연결되지 않음 | 펌웨어 파일 누락 | `sudo apt install firmware-misc-nonfree`를 실행하십시오 (Debian) |
| `airmon-ng start wlan0` 실패 | NetworkManager가 여전히 실행 중 | 먼저 `sudo airmon-ng check kill`을 실행하십시오 |
| 모니터 모드는 시작되지만 트래픽이 캡처되지 않음 | 잘못된 채널 또는 잘못된 인터페이스 이름 | 채널을 설정하십시오: `iwconfig wlan0mon channel 6` |
| 인젝션 테스트가 "No Answer" 출력 | AP가 너무 멀거나 잘못된 인터페이스 | AP에 더 가까이 이동하십시오. `wlan0`이 아닌 `wlan0mon`을 사용하십시오. |
| VIF 인터페이스 생성 실패 | 드라이버가 완전히 로드되지 않음 | 어댑터를 분리하고 모듈을 다시 로드하십시오: `sudo rmmod mt76x2u && sudo modprobe mt76x2u` |

## 중국 미러 참조

이 가이드에서 사용한 모든 자원 — GitHub가 필요 없습니다.

| 자원 | URL | 용도 |
|----------|-----|---------|
| Alfa 공식 드라이버 | [files.alfa.com.tw](https://files.alfa.com.tw) | 드라이버 패키지, 펌웨어 |
| Alfa 문서 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 제품 설명서 |
| 칭화대학(Tsinghua) 미러 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 알리바바 클라우드(Aliyun) 미러 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (권장) |
| 중국과학기술대학(USTC) 미러 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (권장) |
| 화웨이 클라우드(Huawei Cloud) 미러 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 이미지 (백업) |
| MT76 드라이버 (메인라인 커널) | [kernel.org: drivers/net/wireless/mediatek/mt76](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek/mt76) | 커널 내장, 컴파일 불필요 |

## 중국 환경을 위한 추가 Alfa 어댑터 가이드

이 글은 **Alfa 중국 설치 가이드** 시리즈의 일부입니다. 각 글은 하나의 어댑터 모델을 다룹니다.

- [AWUS036ACH 중국 설치 가이드](/ko/blog/awus036ach-china-install-guide/) — RTL8812AU, 고출력
- AWUS036ACM ← 현재 보고 있는 글
- [AWUS036ACS 중국 설치 가이드](/ko/blog/awus036acs-china-install-guide/)
- [AWUS036AX 중국 설치 가이드](/ko/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 중국 설치 가이드](/ko/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 중국 설치 가이드](/ko/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 중국 설치 가이드](/ko/blog/awus036axml-china-install-guide/)
- [AWUS036EAC 중국 설치 가이드](/ko/blog/awus036eacs-china-install-guide/)

궁금한 점이 있으십니까? 아래에 댓글을 남기거나 [yupitek.com](https://yupitek.com/ko/contact/)으로 문의해 주십시오.

## 참고 자료

1. [Linux 커널 mt76 드라이버](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [aircrack-ng 공식 문서](https://www.aircrack-ng.org/)
3. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
4. [Kali Linux 공식 문서](https://www.kali.org/docs/)
5. [Debian firmware-misc-nonfree 패키지](https://packages.debian.org/bookworm/firmware-misc-nonfree)
