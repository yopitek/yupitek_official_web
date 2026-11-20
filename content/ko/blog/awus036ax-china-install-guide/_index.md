---
title: "중국 환경을 위한 ALFA AWUS036AX 드라이버 설치 가이드: Kali Linux, Ubuntu, Debian, Raspberry Pi"
description: "국내 미러를 이용해 중국에서 ALFA AWUS036AX 드라이버를 설치하는 단계별 가이드입니다. RTL8832BU 드라이버, WiFi 6 AX1800을 지원하며 Kali Linux, Ubuntu 22/24(DKMS), Debian, Raspberry Pi를 다룹니다."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "AWUS036AX는 어떤 칩셋을 사용합니까? WiFi 6을 지원합니까?"
    answer: "Realtek RTL8832BU 칩셋을 사용하며, WiFi 6(802.11ax) 고속 네트워킹을 지원합니다."
  - question: "AWUS036AX는 Ubuntu 24.04에서 드라이버가 필요합니까?"
    answer: "커널에 따라 다릅니다. Linux 커널 6.17 이상(예: Ubuntu 24.04 HWE / 커널 6.17)에는 인커널 rtw89_8852bu 드라이버가 포함되어 있어 DKMS 없이 플러그 앤 플레이로 동작합니다. 6.17 미만의 커널에서만 커뮤니티 rtl8852bu 드라이버(morrownr/rtl8852bu-20250826)를 DKMS로 한 번 빌드하면 됩니다. 먼저 uname -r로 확인하십시오."
  - question: "AWUS036AX는 무선 보안 연구에 적합합니까?"
    answer: "적합합니다. 커널 6.17+의 인커널 rtw89_8852bu 드라이버에서는 모니터 모드와 패킷 인젝션이 모두 테스트에서 동작했습니다(Ubuntu 24.04 / 커널 6.17: 2.4GHz 인젝션 96%, 엔드투엔드 WPA .22000 캡처). 참고: 커뮤니티 DKMS 드라이버를 사용하는 구형 커널에서는 모니터 지원이 제한될 수 있습니다. 본인이 소유했거나 테스트 권한을 부여받은 네트워크에서만 사용하십시오."
  - question: "중국에서 AWUS036AX를 설치하려면 VPN이 필요합니까?"
    answer: "반드시 필요하지는 않습니다. 검증된 GitHub 저장소(morrownr/rtl8852bu-20250826)에서 드라이버를 클론하십시오. GitHub가 느리다면 신뢰할 수 있는 프록시나 미러를 사용하십시오. 빌드 도구는 국내 미러에서 설치할 수 있습니다."
  - question: "AWUS036AX의 USB ID는 무엇입니까?"
    answer: "Realtek RTL8832BU의 벤더 ID는 0bda입니다. 제품 ID는 유닛에 따라 8832 또는 885a이므로 lsusb로 확인하십시오."
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 4
related_product: "/ko/products/alfa/awus036ax/"
featureimage: "/images/blog/awus036ax-china-install-guide.webp"
---

AWUS036AX는 ALFA의 WiFi 6 AX1800 듀얼밴드 어댑터입니다. RTL8832BU 칩은 **Linux 커널 6.17 이상의 인커널 rtw89_8852bu 드라이버**(예: Ubuntu 24.04 HWE / 커널 6.17)에서 지원되어 컴파일 없이 플러그 앤 플레이로 동작합니다. **구형 커널**(6.17 미만)에서만 커뮤니티 rtl8852bu 드라이버를 DKMS로 한 번 빌드하면 됩니다. 이 가이드는 두 경우를 모두 다룹니다. 드라이버 소스는 검증된 GitHub 저장소에서 클론합니다. GitHub가 느리다면 신뢰할 수 있는 프록시나 미러를 사용하십시오.

{{< tldr >}}
AWUS036AX는 WiFi 6을 지원하는 RTL8832BU 칩셋을 사용합니다. 커널 6.17+(Ubuntu 24.04 / 커널 6.17 포함)에는 인커널 rtw89_8852bu 드라이버가 포함되어 있습니다. DKMS가 필요 없으며, 모니터 모드와 인젝션이 테스트에서 동작합니다. 구형 커널에서는 DKMS를 통한 커뮤니티 rtl8852bu 드라이버가 필요합니다.
{{< /tldr >}}




> **보안 연구 참고:** **커널 6.17+의 인커널 rtw89_8852bu 드라이버**에서는 AWUS036AX의 모니터 모드와 패킷 인젝션이 테스트에서 동작합니다(Ubuntu 24.04 / 커널 6.17: 2.4GHz 인젝션 96%, 엔드투엔드 WPA .22000). 커뮤니티 DKMS 드라이버를 사용하는 구형 커널에서만 모니터 지원이 제한됩니다. 먼저 `uname -r`을 확인하십시오. 본인이 소유했거나 테스트 권한을 부여받은 네트워크에서만 사용하십시오.

## 시작하기 전에

1. **ALFA AWUS036AX** 어댑터
2. USB-A 케이블
3. 활성 인터넷 연결

```bash
lsusb
```

다음과 같은 줄을 찾으십시오(예시 출력이며, 벤더 ID는 항상 `0bda`이고 제품 ID는 유닛에 따라 `8832` 또는 `885a`입니다):

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## 운영체제 선택

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

### 1단계: 중국 미러로 전환

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### 2단계: 빌드 의존성 설치

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

### 3단계: GitHub에서 드라이버 클론

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
```

> **참고:** 유지보수되는 업스트림 드라이버는 [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)입니다. GitHub가 느리다면 신뢰할 수 있는 프록시나 미러를 사용하십시오. [files.alfa.com.tw](https://files.alfa.com.tw)에서 아카이브를 내려받을 수도 있습니다.

### 4단계: 컴파일 및 설치

```bash
sudo ./install-driver.sh
sudo reboot
```

드라이버가 로드되었는지 확인하십시오.

```bash
lsmod | grep 8852bu
iwconfig
```

### 5단계: 모니터 모드 활성화 {#enable-monitor-mode}

> **커널 6.17+에서 동작:** 인커널 rtw89_8852bu 드라이버에서는 모니터 모드가 동작합니다.
> ```bash
> sudo nmcli dev set wlxXXXX managed no
> sudo ip link set wlxXXXX down
> sudo iw dev wlxXXXX set type monitor
> sudo ip link set wlxXXXX up
> ```
> 커뮤니티 DKMS 드라이버를 사용하는 구형 커널에서는 모니터 지원이 제한될 수 있습니다. 그 경우 [AWUS036ACM](/ko/blog/awus036acm-china-install-guide/)과 같은 인커널 MediaTek 어댑터로 전환할 수 있습니다.

### 6단계: 패킷 인젝션 테스트 {#test-packet-injection}

> **커널 6.17+에서 동작:** 모니터 모드로 진입한 뒤 aireplay-ng로 인젝션을 테스트합니다(테스트에서 2.4GHz 96%).
> ```bash
> sudo iw dev wlxXXXX set channel 6
> sudo aireplay-ng --test wlxXXXX
> ```
> 본인이 소유했거나 테스트 권한을 부여받은 네트워크에서만 사용하십시오. 커뮤니티 DKMS 드라이버에 모니터 모드가 없는 구형 커널에서는 인젝션도 사용할 수 없습니다.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble)

Ubuntu 24.04에서는 **커널 6.17 이상의 HWE**(예: 24.04.4의 HWE)에만 인커널 rtw89_8852bu 드라이버가 포함되어 있어, 꽂기만 하면 되고 빌드가 필요 없습니다. **GA 커널 6.8**이나 **HWE 커널 6.14**(둘 다 이 드라이버 미포함)에서는 아래 Ubuntu 22.04와 마찬가지로 국내 미러로 전환하여 커뮤니티 드라이버를 빌드하거나, 6.17 이상의 HWE 커널로 업그레이드하여 인커널 드라이버를 사용하십시오.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

재부팅 후 `sudo modprobe 8852bu`와 `iwconfig`를 실행하십시오. 모듈이 로드되고 인터페이스가 나타나면 완료입니다(구형 커널용 커뮤니티 DKMS 드라이버 경로이며 모니터 지원이 제한될 수 있습니다. 커널 6.17+에서는 내장 rtw89_8852bu를 사용하며 모니터 모드와 인젝션이 동작합니다).

---

### Ubuntu 22.04 (Jammy) — DKMS 필요

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

이 경로는 6.17 미만의 구형 커널용 커뮤니티 DKMS 드라이버로, 모니터 지원이 제한될 수 있습니다(Kali 5단계 참고). 커널 6.17+에서는 내장 rtw89_8852bu 드라이버를 사용하며 모니터 모드가 동작합니다.

---

## Raspberry Pi 4B / 5

먼저 중국 미러로 전환하십시오.

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## 가상 머신 USB 패스스루 {#virtual-machine-usb-passthrough}

### VirtualBox

1. **설정 → USB** → **USB 3.0 (xHCI)**를 활성화합니다.
2. 필터 추가: **Realtek** (벤더 ID: 0bda, 제품 ID: 8832 또는 885a).
3. VM을 시작 → `lsusb`로 확인 → Kali 단계를 따르십시오.

### VMware

1. **Virtual Machine → USB & Bluetooth** → **Realtek RTL8832BU**를 찾아 **Connect**를 클릭합니다.
2. `lsusb`로 확인 → Kali 단계를 따르십시오.

---

{{< faq >}}

## 문제 해결

| 문제 | 추정 원인 | 해결 방법 |
|---------|-------------|-----|
| `lsusb`에 0bda:8832 또는 0bda:885a가 표시되지 않음 | 어댑터가 인식되지 않음 | 다른 USB 포트를 시도 |
| `install-driver.sh` 실패 | 헤더 누락 | `sudo apt install linux-headers-$(uname -r)` |
| GitHub 클론 실패 또는 느림 | 네트워크 문제 | 신뢰할 수 있는 프록시나 미러 사용 |
| `modprobe 8852bu` 실패 | 드라이버가 빌드되지 않았거나 로드되지 않음 | `sudo ./install-driver.sh` 재실행, `sudo dkms status` 확인 후 재부팅 |
| 모니터 모드 / 인젝션이 동작하지 않음 | 커널이 6.17 미만이며 커뮤니티 rtl8852bu DKMS 드라이버 사용(모니터 지원이 제한될 수 있음) | `uname -r`로 확인 후 커널 6.17+(내장 rtw89_8852bu) 사용, 구형 커널에서는 AWUS036ACM 사용 |

> **VIF 관련 참고:** RTL8832BU 아웃오브커널 드라이버는 가상 인터페이스(VIF)를 지원하지 않습니다.

## 중국 미러 참조

| 리소스 | URL | 용도 |
|----------|-----|---------|
| Alfa 공식 드라이버 | [files.alfa.com.tw](https://files.alfa.com.tw) | 드라이버 패키지 |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | RTL8832BU 드라이버 |
| 칭화대학교 미러 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 알리클라우드 미러 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 중국과학기술대학 미러 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| 화웨이클라우드 미러 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

## 중국 환경을 위한 그 외 Alfa 어댑터 가이드

- [AWUS036ACH 중국 설치 가이드](/ko/blog/awus036ach-china-install-guide/) — RTL8812AU, 고출력
- [AWUS036ACM 중국 설치 가이드](/ko/blog/awus036acm-china-install-guide/) — MT7612U, 완전한 VIF
- [AWUS036ACS 중국 설치 가이드](/ko/blog/awus036acs-china-install-guide/) — RTL8811AU, 모니터 모드
- AWUS036AX ← 현재 보고 계신 문서입니다
- [AWUS036AXER 중국 설치 가이드](/ko/blog/awus036axer-china-install-guide/) — RTL8832BU, 나노
- [AWUS036AXM 중국 설치 가이드](/ko/blog/awus036axm-china-install-guide/) — MT7921AUN, L자형
- [AWUS036AXML 중국 설치 가이드](/ko/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS 중국 설치 가이드](/ko/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

궁금한 점이 있으신가요? 아래에 댓글을 남기거나 [yupitek.com](https://yupitek.com/ko/contact/)으로 문의해 주십시오.

## 참고 자료

1. [Realtek 공식 웹사이트](https://www.realtek.com/)
2. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
3. [Kali Linux 공식 문서](https://www.kali.org/docs/)
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
