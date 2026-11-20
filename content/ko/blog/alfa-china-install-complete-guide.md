---
title: "완벽 가이드: 중국에서 Linux에 모든 Alfa USB WiFi 어댑터 설치하기 - Kali, Ubuntu, Raspberry Pi"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "중국에서 Alfa WiFi 어댑터를 설치하려면 VPN이 필요합니까?"
    answer: "반드시 그렇지는 않습니다. 시스템 패키지는 중국 내 미러(USTC, Aliyun, Tsinghua)에서 받고, 커널 외부 드라이버 소스는 morrownr의 검증된 GitHub 저장소에서 클론합니다. GitHub가 느리다면 신뢰할 수 있는 프록시나 미러를 사용하시기 바랍니다."
  - question: "모니터 모드와 패킷 인젝션에 가장 적합한 Alfa 어댑터는 무엇입니까?"
    answer: "MT7612U 칩셋을 사용하는 AWUS036ACM은 커널 내장 드라이버와 완전한 VIF 지원을 갖추고 있어 최선의 선택입니다."
  - question: "WiFi 6를 지원하는 Alfa 어댑터는 무엇입니까?"
    answer: "AWUS036AX와 AWUS036AXER는 WiFi 6를 지원하는 RTL8832BU 칩셋을 사용합니다. Ubuntu 24.04에서는 드라이버 설치 없이 플러그 앤 플레이로 작동합니다."
  - question: "WiFi 6E를 지원하는 Alfa 어댑터는 무엇입니까?"
    answer: "AWUS036AXM과 AWUS036AXML은 MT7921AUN 칩셋(WiFi 6E 트라이 밴드)을 사용합니다. AXML의 6 GHz는 로컬에서 실측으로 동작을 확인했으며, AXM은 사양상 Wi-Fi 6E를 지원하지만 6 GHz는 실측하지 않았습니다."
  - question: "Raspberry Pi에서 Alfa 어댑터를 사용할 때 주의할 점은 무엇입니까?"
    answer: "항상 전원 공급형 USB 허브로 전원을 공급하고, 최상의 드라이버 지원을 위해 Kali ARM64 이미지를 플래싱하시기 바랍니다."
draft: false
slug: "alfa-china-install-complete-guide"
tags: ["alfa", "kali-linux", "ubuntu", "raspberry-pi", "driver", "china", "monitor-mode", "packet-injection", "wireless"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 9
description: "중국에서 Linux에 모든 Alfa USB WiFi 어댑터를 설치하는 완벽 가이드. Kali Linux, Ubuntu 22/24, Debian, Raspberry Pi를 다룹니다. 시스템 패키지는 중국 내 미러에서, 드라이버 소스는 검증된 GitHub 저장소에서 받습니다."
featureimage: "/images/blog/alfa-china-install-complete-guide.webp"
---
이 글을 읽고 계시다면, 아마 Alfa USB WiFi 어댑터를 구매했지만 다음과 같은 이유로 막혀 있을 것입니다:

## Alfa Linux 설치 완벽 가이드에 오신 것을 환영합니다

{{< tldr >}}
중국에서 Linux에 Alfa WiFi 어댑터를 설치하는 완벽 가이드로, Kali, Ubuntu, Debian, Raspberry Pi를 다룹니다. RTL8812AU, MT7612U, RTL8832BU를 포함한 모든 칩셋을 지원합니다. 시스템 패키지는 중국 내 미러를, 드라이버 소스는 검증된 GitHub 저장소를 사용합니다.
{{< /tldr >}}


본 가이드는 중국 본토에서 모든 주요 Linux 배포판에 모든 Alfa USB WiFi 어댑터를 설치하는 전체 단계를 다루며, 시스템 패키지는 중국 내 미러를, 드라이버 소스는 검증된 GitHub 저장소를 사용합니다.







- 중국에 있어 GitHub에 접속할 수 없는 경우
- 드라이버 설치가 복잡해 보이는 경우
- 무선 테스트를 위해 모니터 모드와 패킷 인젝션을 활성화해야 하는 경우
- 사용 중인 Alfa 모델에 어떤 드라이버가 필요한지 확실하지 않은 경우

본 가이드는 <strong>이 모든 문제</strong>를 해결합니다. 시스템 패키지에는 <strong>중국에서 접속 가능한 미러</strong>를, 드라이버 소스에는 검증된 GitHub 저장소를 사용하여 <strong>모든 주요 Linux 배포판</strong>에 <strong>모든 Alfa USB WiFi 어댑터</strong>를 설치하는 과정을 안내합니다. 번거로움 없이 진행할 수 있습니다.

---

## 본 가이드를 작성한 이유

Alfa USB WiFi 어댑터는 침투 테스터, 네트워크 엔지니어, 무선 기술 애호가들 사이에서 인기가 높습니다. 대부분의 일반 소비자용 WiFi 어댑터에는 없는 모니터 모드와 패킷 인젝션을 지원하기 때문입니다.

하지만 문제가 있습니다. <strong>대부분의 드라이버 설치 가이드는 GitHub에 빠르게 접속할 수 있다고 가정합니다</strong>. 중국에서는 GitHub가 느리거나 불안정할 수 있습니다. 본 가이드는 시스템 패키지를 중국 내 미러에서 설치하고 드라이버 소스는 검증된 GitHub 저장소에서 클론합니다. GitHub가 느리다면 신뢰할 수 있는 프록시나 미러를 사용하시기 바랍니다.

---

## 빠른 모델 참조

본격적으로 시작하기 전에, 보유한 Alfa 어댑터와 사용하는 칩을 확인해 보겠습니다:

### AX 시리즈 (Wi-Fi 6 / 802.11ax)

| 모델 | 칩셋 | 드라이버 | 적합한 용도 |
|-------|---------|--------|----------|
| AWUS036AX | Realtek RTL8832BU | `8852bu` | 일반 용도, 우수한 도달 거리 |
| AWUS036AXM | MediaTek MT7921AUN | `mt7921u` | 컴팩트한 디자인 |
| AWUS036AXML | MediaTek MT7921AUN | `mt7921u` | 초소형 |
| AWUS036AXER | Realtek RTL8832BU | `8852bu` | 강화된 출력 |

### AC 시리즈 (Wi-Fi 5 / 802.11ac)

| 모델 | 칩셋 | 드라이버 | 적합한 용도 |
|-------|---------|--------|----------|
| AWUS036ACH | Realtek RTL8812AU | `88XXau` | 고출력, 뛰어난 도달 거리 |
| AWUS036ACM | MediaTek MT7612U | `mt76x2u` | <strong>최고의 VIF 지원</strong>, 플러그 앤 플레이 |
| AWUS036ACS | Realtek RTL8811AU | `8811au` | 합리적인 가격 |

### 보유한 어댑터는 무엇입니까?

1. 어댑터의 라벨을 확인합니다
2. 제품 상자를 확인합니다
3. 온라인으로 구매했다면 주문 내역을 확인합니다

모델을 확인했다면 아래의 해당 섹션으로 이동하거나 일반 워크플로를 따르시기 바랍니다.

---

## 시작하기 전에: 준비물

시작하기 전에 다음이 준비되어 있는지 확인하시기 바랍니다:

1. <strong>Alfa USB WiFi 어댑터</strong> — 용도에 맞는 모델
2. <strong>USB 케이블</strong> — 제품에 동봉된 케이블로 충분합니다
3. <strong>전원 공급형 USB 허브</strong> — Raspberry Pi를 사용하는 경우 필수
4. <strong>인터넷 연결</strong> — 중국 내 미러에 접속하기 위해 필요
5. <strong>Sudo 권한</strong> — 드라이버 설치에 관리자 권한이 필요합니다

먼저 어댑터를 연결하여 시스템이 인식하는지 확인합니다:

```bash
lsusb
```

출력에서 어댑터의 벤더 ID를 찾습니다:

- <strong>Alfa 어댑터</strong>는 `0e8d`(MediaTek) 또는 `0bda`(Realtek)로 표시됩니다
- 예: `Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.`
- 예: `Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.`

ID가 보이면 어댑터가 인식된 것입니다. 아래의 드라이버 설치 섹션으로 이동하시기 바랍니다.

보이지 않으면 다른 USB 포트를 시도하거나 케이블을 교체한 후 `lsusb`를 다시 실행합니다.

---

## 운영체제 선택

사용 중인 OS에 맞는 섹션으로 이동하시기 바랍니다:

- [Kali Linux](#kali-linux-설치)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404-설치)
- [Debian 12 (Bookworm)](#debian-12-bookworm-설치)
- [Raspberry Pi OS (64-bit)](#raspberry-pi-os-설치)

이미 드라이버를 설치했다면 고급 섹션으로 건너뛰시기 바랍니다:

- [모니터 모드 활성화](#모든-어댑터에서-모니터-모드-활성화)
- [패킷 인젝션 테스트](#패킷-인젝션-테스트)
- [가상 인터페이스(VIF) 지원](#가상-인터페이스-vif-지원)
- [VM USB 패스스루](#가상-머신-usb-패스스루)

---

## 중국에서 접속 가능한 미러 참조

본 가이드의 모든 리소스는 다음의 중국에서 접속 가능한 미러를 사용합니다:

| 리소스 | URL | 용도 |
|----------|-----|---------|
| <strong>Alfa 공식 다운로드</strong> | [files.alfa.com.tw](https://files.alfa.com.tw) | 드라이버 패키지, 펌웨어 |
| <strong>Alfa 문서</strong> | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 제품 매뉴얼(영문) |
| <strong>칭화대학교 미러(Tsinghua)</strong> | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| <strong>알리클라우드 미러(Aliyun)</strong> | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu(권장) |
| <strong>중국과학기술대학교 미러(USTC)</strong> | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali(권장) |
| <strong>화웨이 클라우드 미러(Huawei Cloud)</strong> | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 이미지(백업) |
| <strong>GitHub (morrownr)</strong> | [github.com/morrownr](https://github.com/morrownr) | 드라이버 소스 코드 |

---

## Kali Linux 설치

Kali Linux에는 무선 도구가 사전 설치되어 있습니다. Alfa 어댑터를 작동시키는 데는 몇 단계만 필요합니다.

### 1단계: 중국 미러로 전환

소스 목록을 엽니다:

```bash
sudo nano /etc/apt/sources.list
```

모든 내용을 다음으로 교체합니다:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

저장: <strong>Ctrl+O</strong>, Enter, 그다음 <strong>Ctrl+X</strong>. 새로 고침:

```bash
sudo apt update
```

> <strong>백업 미러:</strong> USTC(중국과학기술대학교) 미러가 느리다면 Tsinghua(칭화대학교) 미러를 사용하시기 바랍니다:
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

### 2단계: 칩셋별 드라이버 설치

#### AX 시리즈 (RTL8832BU)

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
```

#### AC 시리즈 - Realtek (RTL8812AU / RTL8811AU)

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### AC 시리즈 - MediaTek (MT7612U)

MT7612U 드라이버는 Kali 커널에 내장되어 있습니다. 로드되었는지 확인합니다:

```bash
lsmod | grep mt76
```

`mt76x2u`가 보이면 완료입니다. 보이지 않으면:

```bash
sudo modprobe mt76x2u
```

### 3단계: 드라이버 로드 확인

`lsusb`를 다시 실행합니다. 어댑터가 표시되어야 합니다. 그런 다음 무선 인터페이스를 확인합니다:

```bash
iwconfig
```

`wlan0` 또는 `wlan1`을 찾습니다. 인터페이스가 나타나면 드라이버가 작동하는 것입니다.

### 4단계: 모니터 모드 활성화

방해 프로세스를 중지합니다:

```bash
sudo airmon-ng check kill
```

모니터 모드를 시작합니다:

```bash
sudo airmon-ng start wlan0
```

확인합니다:

```bash
iwconfig
```

`Mode:Monitor` 상태의 `wlan0mon`을 찾습니다. 완료입니다!

---

## Ubuntu 22.04 / 24.04 설치

### 1단계: 중국 미러로 전환

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

다음으로 교체합니다:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

<strong>Ctrl+O</strong>로 저장하고 <strong>Ctrl+X</strong>로 종료합니다.

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

다음으로 교체합니다:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

저장하고 종료합니다.

#### 패키지 인덱스 새로 고침

```bash
sudo apt update
```

### 2단계: 빌드 의존성 설치

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### 3단계: 드라이버 설치

#### AX 시리즈 (RTL8832BU)

GitHub에서 클론합니다:

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo modprobe 8852bu
```

#### AC 시리즈 - Realtek (RTL8812AU)

GitHub에서 클론합니다:

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
sudo ./install-driver.sh
sudo modprobe 8812au
```

#### AC 시리즈 - MediaTek (MT7612U)

드라이버는 Ubuntu 커널에 내장되어 있습니다. 로드합니다:

```bash
sudo modprobe mt76x2u
```

### 4단계: 모니터 모드 활성화

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

`Mode:Monitor` 상태의 `wlan0mon`을 찾습니다.

---

## Debian 12 (Bookworm) 설치

### 1단계: 중국 미러로 전환

```bash
sudo nano /etc/apt/sources.list
```

다음으로 교체합니다:

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

저장하고 종료합니다. 새로 고침:

```bash
sudo apt update
```

### 2단계: Non-Free 펌웨어 설치

```bash
sudo apt install -y firmware-misc-nonfree
```

### 3단계: 빌드 의존성 설치

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### 4단계: 드라이버 설치

#### AX 시리즈 (RTL8832BU)

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo modprobe 8852bu
```

#### AC 시리즈 - Realtek (RTL8812AU)

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
sudo ./install-driver.sh
sudo modprobe 8812au
```

#### AC 시리즈 - MediaTek (MT7612U)

```bash
sudo modprobe mt76x2u
```

### 5단계: Aircrack-ng 설치

```bash
sudo apt install -y aircrack-ng
```

### 6단계: 모니터 모드 활성화

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

`Mode:Monitor` 상태의 `wlan0mon`을 찾습니다.

---

## Raspberry Pi OS 설치

> <strong>중요:</strong> AWUS036ACH는 약 500mW, AWUS036ACM은 약 400mW를 소비합니다. 부하 시 Pi가 스로틀링되거나 다운되지 않도록 <strong>항상 전원 공급형 USB 허브를 사용</strong>하시기 바랍니다.

### 1단계: Kali Linux ARM64 이미지 다운로드

다음으로 이동합니다: https://www.kali.org/get-kali/#kali-arm

<strong>Raspberry Pi 4 (64-bit)</strong> 또는 <strong>Raspberry Pi 5 (64-bit)</strong>를 선택합니다. 32비트는 사용하지 마십시오. 64비트가 필요합니다.

> <strong>중국 미러:</strong> kali.org가 느리다면 화웨이 클라우드(Huawei Cloud) 미러를 사용하시기 바랍니다: https://repo.huaweicloud.com/kali-images/

### 2단계: MicroSD에 플래싱

SD 카드의 장치 경로를 확인합니다:

```bash
lsblk
```

이미지를 플래싱합니다(`/dev/sdX`를 실제 카드로 교체):

```bash
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

`sync`가 완료될 때까지 기다립니다. Pi를 부팅합니다. 기본 자격 증명: <strong>kali / kali</strong>.

### 3단계: 중국 미러로 전환

```bash
sudo nano /etc/apt/sources.list
```

다음으로 교체합니다:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

저장하고 적용합니다:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### 4단계: 드라이버 설치

#### AX 시리즈 (RTL8832BU)

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
```

#### AC 시리즈 - Realtek (RTL8812AU)

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### AC 시리즈 - MediaTek (MT7612U)

```bash
sudo modprobe mt76x2u
```

### 5단계: 모니터 모드 활성화

내장 Wi-Fi가 있는 Pi에서는 Alfa 어댑터가 `wlan1`로 표시됩니다:

```bash
iwconfig
```

그런 다음:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
iwconfig
```

`Mode:Monitor` 상태의 `wlan1mon`을 찾습니다.

---

## 모든 어댑터에서 모니터 모드 활성화

드라이버가 설치되면 모니터 모드는 쉽게 활성화할 수 있습니다:

### 1단계: 인터페이스 이름 확인

```bash
iwconfig
```

`wlan0`인지 `wlan1`인지 기록합니다.

### 2단계: 방해 프로세스 종료

```bash
sudo airmon-ng check kill
```

### 3단계: 모니터 모드 시작

```bash
sudo airmon-ng start wlan0
```

인터페이스 이름이 다르다면 `wlan0`을 실제 인터페이스 이름으로 교체합니다.

### 4단계: 확인

```bash
iwconfig
```

`Mode:Monitor` 상태이며 이름이 `mon`으로 끝나는 인터페이스(예: `wlan0mon`)를 찾습니다.

---

## 패킷 인젝션 테스트

이 테스트는 어댑터가 조작된 패킷을 송신할 수 있는지 확인합니다. 무선 테스트에 필수적입니다.

```bash
sudo aireplay-ng --test wlan0mon
```

<strong>성공 시 출력:</strong>

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

<strong>실패하는 경우:</strong>
- 재부팅 후 다시 시도
- 다른 프로세스가 인터페이스를 점유하고 있지 않은지 확인(`iwconfig`)
- 테스트를 위해 WiFi AP에 더 가까이 이동
- `wlan0`이 아닌 `wlan0mon`을 사용하고 있는지 확인

---

## 가상 인터페이스 (VIF) 지원

VIF(Virtual Interface Functionality)를 사용하면 하나의 어댑터에서 여러 인터페이스를 동시에 실행할 수 있습니다. 예를 들어:

- <strong>관리 모드</strong>(`wlan0`) + <strong>모니터 모드</strong>(`mon0`)를 동시에 사용
- 네트워크 연결을 유지하면서 트래픽을 캡처

### VIF를 지원하는 어댑터는?

| 칩셋 | VIF 지원 | 비고 |
|---------|-------------|-------|
| <strong>MT7612U (AWUS036ACM)</strong> | ✅ 완전한 네이티브 지원 | VIF 워크플로에 최선의 선택 |
| <strong>RTL8812AU (AWUS036ACH)</strong> | ⚠️ 제한적 | 관리 모드 + 모니터 모드 동시 실행 불가 |
| <strong>RTL8832BU (AX 시리즈)</strong> | ✅ STA+AP 가능 | 커널 내장 rtw89_8852bu(kernel 6.17 이상)에서 실측 동작 확인. 구형 커널의 커뮤니티 DKMS 드라이버는 VIF 미지원 |

### 가상 인터페이스 생성 (MT7612U)

AWUS036ACM(MT7612U)을 보유하고 있다면:

```bash
# wlan0을 관리 모드로 유지하면서 모니터 인터페이스 생성
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

두 인터페이스가 모두 활성 상태인지 확인합니다:

```bash
iwconfig
```

다음이 보여야 합니다:
- `wlan0` — 관리 모드(AP에 연결됨)
- `mon0` — 모니터 모드(모든 트래픽 캡처)

### 사용 사례

<strong>연결을 유지하면서 트래픽 캡처:</strong>

```bash
sudo airodump-ng mon0
```

`mon0`이 모든 것을 캡처하는 동안 `wlan0`은 정상 작동을 계속합니다.

<strong>가짜 AP + 모니터:</strong>

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

---

## 가상 머신 USB 패스스루

VM 안에서 Linux를 실행 중이라면 USB 어댑터를 게스트로 패스스루해야 합니다.

### VirtualBox

1. VM 전원을 끕니다
2. <strong>Settings → USB</strong>로 이동합니다
3. <strong>USB 3.0 (xHCI) Controller</strong>를 활성화합니다
4. <strong>+</strong>를 클릭하여 USB 필터를 추가합니다
5. Alfa 어댑터를 선택합니다(ID: `0bda:8812` 또는 `0e8d:7612`)
6. VM을 시작합니다

VM 내부에서 `lsusb`를 실행하여 확인한 후 위의 Kali Linux 단계를 따릅니다.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. VM을 시작합니다
2. 메뉴: <strong>Virtual Machine → USB & Bluetooth</strong>
3. Alfa 어댑터를 찾아 <strong>Connect</strong>를 클릭합니다
4. 어댑터가 VM 내부에 나타납니다

`lsusb`를 실행하여 확인한 후 드라이버 설치 단계를 따릅니다.

---

## 문제 해결

| 문제 | 가능한 원인 | 해결 |
|---------|-------------|-----|
| `lsusb`에 어댑터 ID가 표시되지 않음 | 케이블 불량 또는 전원 부족 | 다른 USB 포트 시도. Pi에서는 전원 공급형 허브 사용. |
| `modprobe`가 "Module not found" 출력 | 커널 모듈 누락 | `sudo apt install linux-modules-extra-$(uname -r)` 실행 |
| 드라이버는 작동하지만 모니터 모드로 전환되지 않음 | NetworkManager 간섭 | 먼저 `sudo airmon-ng check kill` 실행 |
| 모니터 모드는 시작되지만 아무것도 캡처되지 않음 | 잘못된 인터페이스 또는 채널 | `iwconfig` 실행. 채널 설정: `iwconfig wlan0mon channel 6` |
| 인젝션 테스트 실패 | 잘못된 인터페이스 사용 | `wlan0`이 아닌 `wlan0mon` 사용 |
| VIF 생성 실패 | 드라이버가 완전히 로드되지 않음 | 어댑터를 뽑았다가 다시 연결하거나 모듈 재로드 |

---

## 부록: 전체 Alfa 모델 목록

| 모델 | 칩셋 | 드라이버 | 중국 미러 출처 |
|-------|---------|--------|---------------------|
| AWUS036ACH | RTL8812AU | `8812au` | GitHub: morrownr/8812au-20210820 |
| AWUS036ACM | MT7612U | `mt76x2u` | 커널 내장 드라이버 |
| AWUS036ACS | RTL8811AU | `8821au` | GitHub: morrownr/8821au-20210708 |
| AWUS036AX | RTL8832BU | `8852bu` | GitHub: morrownr/rtl8852bu-20250826 |
| AWUS036AXM | MT7921AUN | `mt7921u` | 커널 내장 드라이버 |
| AWUS036AXML | MT7921AUN | `mt7921u` | 커널 내장 드라이버 |
| AWUS036AXER | RTL8832BU | `8852bu` | GitHub: morrownr/rtl8852bu-20250826 |
| AWUS036EAC | RTL8814AU | `8814au` | GitHub: morrownr/8814au |

---

{{< faq >}}

## 마무리

본 가이드는 <strong>중국에서 접속 가능한 리소스만</strong> 사용하여 <strong>모든 주요 Linux 배포판</strong>에서 <strong>모든 Alfa USB WiFi 어댑터</strong>를 다룹니다. 이제 다음을 할 수 있습니다:

✅ 모든 Alfa 어댑터의 드라이버 설치  
✅ Kali, Ubuntu, Debian, Raspberry Pi에서 모니터 모드 활성화  
✅ 패킷 인젝션 테스트  
✅ 지원 모델에서 가상 인터페이스(VIF) 사용  
✅ VM으로 어댑터 패스스루  

<strong>질문이나 문제가 있으십니까?</strong> 시리즈의 모델별 가이드를 확인하시거나 [yupitek.com](https://yupitek.com/ko/contact/)으로 문의하시기 바랍니다.

---

## 관련 가이드

본 문서는 <strong>Alfa 중국 설치 가이드</strong> 시리즈의 일부입니다:

- [AWUS036ACH 중국 설치 가이드](/ko/blog/awus036ach-china-install-guide/) — RTL8812AU, 고출력
- [AWUS036ACM 중국 설치 가이드](/ko/blog/awus036acm-china-install-guide/) — MT7612U, 최고의 VIF 지원
- [AWUS036ACS 중국 설치 가이드](/ko/blog/awus036acs-china-install-guide/) — RTL8811AU, 저예산 옵션
- [AWUS036AX 중국 설치 가이드](/ko/blog/awus036ax-china-install-guide/) — Wi-Fi 6, RTL8832BU
- [AWUS036AXM 중국 설치 가이드](/ko/blog/awus036axm-china-install-guide/) — Wi-Fi 6, 컴팩트 디자인
- [AWUS036AXML 중국 설치 가이드](/ko/blog/awus036axml-china-install-guide/) — Wi-Fi 6, 초소형
- [AWUS036AXER 중국 설치 가이드](/ko/blog/awus036axer-china-install-guide/) — Wi-Fi 6, 강화된 출력
- [AWUS036EAC 중국 설치 가이드](/ko/blog/awus036eacs-china-install-guide/) — RTL8814AU, 고출력

---

*최종 업데이트: 2026년 4월 24일*

## 참고 자료

1. [aircrack-ng 공식 문서](https://www.aircrack-ng.org/)
2. [Linux 커널 mt76 드라이버](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
3. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
4. [Kali Linux 공식 문서](https://www.kali.org/docs/)
5. [GitHub: morrownr](https://github.com/morrownr)
