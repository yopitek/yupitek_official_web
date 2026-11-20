---
title: "중국 환경을 위한 ALFA AWUS036ACS 드라이버 설치 가이드: Kali Linux, Ubuntu, Debian, Raspberry Pi"
description: "국내 미러를 이용해 중국에서 ALFA AWUS036ACS 드라이버를 설치하는 단계별 가이드입니다. RTL8811AU DKMS 드라이버, 완전한 모니터 모드와 패킷 인젝션을 지원하며 Kali Linux, Ubuntu 22/24, Debian, Raspberry Pi를 다룹니다."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036ACS는 어떤 칩셋을 사용합니까? AWUS036ACH와 동일합니까?"
    answer: "Realtek RTL8811AU 칩셋을 사용합니다. 드라이버 지원 여부는 커널에 따라 다릅니다. Linux 커널 6.13+(예: Ubuntu 24.04 HWE / 커널 6.17)에는 내장 rtw88_8821au 드라이버가 포함되어 있어 DKMS 없이 플러그 앤 플레이로 동작합니다. 6.13 미만의 구형 커널에서만 커뮤니티 8821au 드라이버(morrownr/8821au-20210708, 모듈명 `8821au`)가 필요합니다. RTL8812AU 드라이버와는 공유되지 않습니다. uname -r로 커널을 확인하십시오."
  - question: "AWUS036ACS는 모니터 모드를 지원합니까?"
    answer: "지원합니다. RTL8811AU는 모니터 모드와 패킷 인젝션을 완전히 지원하여, 보안 연구를 위한 가성비 좋은 선택지입니다(커널 6.17의 내장 rtw88_8821au 드라이버에서 인젝션을 2.4GHz 100%, 5GHz 96%로 테스트했으며, 엔드투엔드 WPA .22000 캡처를 수행했습니다). 본인이 소유했거나 테스트 권한을 부여받은 네트워크에서만 사용하십시오."
  - question: "중국에서 AWUS036ACS를 설치하려면 VPN이 필요합니까?"
    answer: "반드시 필요하지는 않습니다. 검증된 GitHub 저장소(morrownr/8821au-20210708)에서 드라이버를 클론하십시오. GitHub가 느리다면 신뢰할 수 있는 프록시나 미러를 사용하십시오. 빌드 도구는 국내 미러에서 설치할 수 있습니다."
  - question: "AWUS036ACS의 USB ID는 무엇입니까?"
    answer: "Realtek RTL8811AU의 USB ID는 0bda:0811입니다. lsusb로 확인하십시오."
  - question: "AWUS036ACS 드라이버를 설치하는 Kali Linux 명령은 무엇입니까?"
    answer: "먼저 uname -r로 커널을 확인하십시오. 커널 6.13+에는 내장 rtw88_8821au 드라이버가 이미 포함되어 있어 설치 없이 플러그 앤 플레이로 동작합니다. 구형 커널에서만 빌드 도구를 설치하고 8821au 드라이버(GitHub의 morrownr/8821au-20210708)를 클론한 뒤 sudo sh install-driver.sh를 실행합니다. apt 패키지 realtek-rtl88xxau-dkms는 RTL8812AU 드라이버이며 이 어댑터용이 아닙니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acs-china-install-guide"
tags: ["alfa", "awus036acs", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "rtl8811au"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 3
related_product: "/ko/products/alfa/awus036acs/"
featureimage: "/images/blog/awus036acs-china-install-guide.webp"
---

AWUS036ACS는 ALFA의 소형 듀얼밴드 보안 연구용 어댑터입니다. RTL8811AU 칩은 Kali Linux에서 완전한 모니터 모드와 패킷 인젝션을 지원합니다. **Linux 커널 6.13+**(예: Ubuntu 24.04 HWE / 커널 6.17)에서는 커널에 이미 내장 rtw88_8821au 드라이버가 포함되어 있어 DKMS 없이 플러그 앤 플레이로 동작합니다. **구형 커널**(6.13 미만)에서만 커뮤니티 8821au 드라이버를 소스에서 컴파일해야 합니다. 중국에서는 GitHub가 느릴 수 있으므로, 그 경우 이 가이드는 국내 미러에서 빌드 도구를 설치하고 검증된 GitHub 저장소에서 드라이버를 클론합니다. GitHub가 느리다면 신뢰할 수 있는 프록시나 미러를 사용하십시오.

> **먼저 커널을 확인하십시오:** `uname -r`을 실행합니다. 커널 6.13+(예: Ubuntu 24.04 HWE / 커널 6.17)에는 내장 rtw88_8821au 드라이버가 포함되어 있습니다. DKMS 없이 플러그 앤 플레이이며, 모니터 모드와 인젝션이 정상 동작하는 것으로 테스트되었습니다(2.4GHz 100%, 5GHz 96%, 엔드투엔드 WPA .22000). 아래의 컴파일·설치 단계는 구형 커널(6.13 미만)에서만 필요합니다. 본인이 소유했거나 테스트 권한을 부여받은 네트워크에서만 사용하십시오.

{{< tldr >}}
AWUS036ACS는 RTL8811AU 칩셋을 사용합니다. 커널 6.13+(Ubuntu 24.04 HWE / 커널 6.17 포함)에는 내장 rtw88_8821au 드라이버가 포함되어 있습니다. DKMS 없이 플러그 앤 플레이이며, 모니터 모드와 인젝션이 정상 동작하는 것으로 테스트되었습니다(2.4GHz 100%, 5GHz 96%, 엔드투엔드 WPA .22000). 구형 커널에서만 GitHub 저장소 morrownr/8821au-20210708의 install-driver.sh로 커뮤니티 8821au DKMS 드라이버를 빌드합니다.
{{< /tldr >}}

다음 항목을 준비했는지 확인하십시오.




## 시작하기 전에

다음 항목을 준비했는지 확인하십시오.

1. **ALFA AWUS036ACS** 어댑터
2. USB 케이블 (USB-A 2.0, 박스 동봉품으로 충분합니다)
3. 국내 미러에 접속할 수 있는 활성 인터넷 연결

어댑터를 꽂은 뒤, 시스템이 인식하는지 확인하십시오.

```bash
lsusb
```

출력에서 다음 항목을 찾으십시오.

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
```

`0bda:0811`이 보이면 어댑터가 인식된 것입니다. 아래의 해당 OS 섹션으로 이동하십시오.

## 운영체제 선택

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

이미 설치하셨나요? 다음으로 건너뛰십시오.

- [모니터 모드 활성화](#enable-monitor-mode)
- [패킷 인젝션 테스트](#test-packet-injection)
- [VM USB 패스스루](#virtual-machine-usb-passthrough)

---

## Kali Linux

### 1단계: 중국 미러로 전환

```bash
sudo nano /etc/apt/sources.list
```

기존 내용을 모두 삭제한 뒤 다음을 붙여넣으십시오.

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

**Ctrl+O**, Enter로 저장한 뒤 Ctrl+X로 나가십시오. 갱신합니다.

```bash
sudo apt update
```

> **백업 미러:** `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 2단계: 빌드 의존성 설치

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### 3단계: GitHub에서 드라이버 클론

```bash
git clone https://github.com/morrownr/8821au-20210708.git
cd 8821au-20210708
```

> **참고:** 유지보수되는 업스트림 드라이버는 [morrownr/8821au-20210708](https://github.com/morrownr/8821au-20210708)입니다. GitHub가 느리다면 신뢰할 수 있는 프록시나 미러를 사용하십시오. [files.alfa.com.tw](https://files.alfa.com.tw)에서 아카이브를 내려받을 수도 있습니다.

---

### 4단계: 컴파일 및 설치

```bash
sudo ./install-driver.sh
sudo reboot
```

재부팅 후 드라이버가 로드되었는지 확인하십시오.

```bash
lsmod | grep 8821au
```

목록에 `8821au` 모듈이 보여야 합니다. 그런 다음 인터페이스가 생성되었는지 확인하십시오.

```bash
iwconfig
```

`wlan0` 또는 `wlan1`을 찾으십시오.

---

### 5단계: 모니터 모드 활성화 {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

`iwconfig`로 확인하십시오. `Mode:Monitor`가 표시된 `wlan1mon`을 찾으십시오.

---

### 6단계: 패킷 인젝션 테스트 {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1mon
```

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

---

## Ubuntu 22.04 / 24.04

### 1단계: 중국 미러로 전환

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

모든 내용을 삭제한 뒤 다음을 붙여넣으십시오.

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

모든 줄을 다음으로 교체하십시오.

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
```

---

### 2단계: 빌드 의존성 설치

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

---

### 3단계: GitHub에서 드라이버 클론 및 설치

```bash
git clone https://github.com/morrownr/8821au-20210708.git
cd 8821au-20210708
sudo ./install-driver.sh
sudo reboot
```

---

### 4단계: 모니터 모드 활성화

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

---

### 5단계: 패킷 인젝션 테스트

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Debian

### 1단계: 중국 미러로 전환

```bash
sudo nano /etc/apt/sources.list
```

다음을 붙여넣으십시오 (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### 2단계: 빌드 의존성 설치

```bash
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
```

### 3단계: 클론 및 설치

```bash
git clone https://github.com/morrownr/8821au-20210708.git
cd 8821au-20210708
sudo ./install-driver.sh
sudo reboot
```

### 4단계: 모니터 모드 활성화

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

확인: `iwconfig` → `Mode:Monitor`가 표시된 `wlan1mon`을 찾으십시오.

### 5단계: 패킷 인젝션 테스트

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Raspberry Pi 4B / 5

### 1단계: Kali ARM64 다운로드 및 플래싱

공식: https://www.kali.org/get-kali/#kali-arm — Raspberry Pi 4/5 64비트를 선택하십시오.

중국 미러: https://repo.huaweicloud.com/kali-images/

```bash
lsblk
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

기본 자격 증명: **kali / kali**.

### 2단계: 중국 미러로 전환

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### 3단계: 빌드 의존성 설치

```bash
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
```

### 4단계: 드라이버 클론 및 설치

```bash
git clone https://github.com/morrownr/8821au-20210708.git
cd 8821au-20210708
sudo ./install-driver.sh
sudo reboot
```

### 5단계: 모니터 모드 활성화

내장 Wi-Fi가 있는 Pi에서는 AWUS036ACS가 `wlan1`로 나타납니다.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

### 6단계: 패킷 인젝션 테스트

```bash
sudo aireplay-ng --test wlan1mon
```

---

## 가상 머신 USB 패스스루 {#virtual-machine-usb-passthrough}

### VirtualBox

1. VM 전원을 끈 뒤 **설정 → USB** → **USB 2.0 컨트롤러**를 활성화합니다.
2. **+**를 클릭 → **Realtek** (ID: 0bda:0811)을 선택합니다.
3. VM을 시작합니다. `lsusb`를 실행해 `0bda:0811`을 확인한 뒤 위의 Kali 단계를 따르십시오.

### VMware Fusion / Workstation

1. **Virtual Machine → USB & Bluetooth** → **Realtek 8811AU**를 찾아 **Connect**를 클릭합니다.
2. `lsusb`를 실행해 확인한 뒤 위의 Kali 단계를 따르십시오.

---

{{< faq >}}

## 문제 해결

| 문제 | 추정 원인 | 해결 방법 |
|---------|-------------|-----|
| `lsusb`에 0bda:0811이 표시되지 않음 | 어댑터에 전원이 들어오지 않거나 케이블 불량 | 다른 USB 포트를 시도 |
| `install-driver.sh` 실패 | 헤더 누락 | `sudo apt install linux-headers-$(uname -r)` 실행 |
| GitHub 클론 실패 또는 느림 | 네트워크 문제 | 신뢰할 수 있는 프록시나 미러 사용 |
| `airmon-ng start` 실패 | NetworkManager 실행 중 | 먼저 `sudo airmon-ng check kill` 실행 |
| 모니터 모드에서 트래픽 없음 | 잘못된 채널 | 채널 설정: `iwconfig wlan1mon channel 6` |
| 인젝션 "No Answer" | AP가 너무 멀리 있음 | 더 가까이 이동. `wlan1`이 아닌 `wlan1mon`을 사용 |

> **VIF 관련 참고:** RTL8811AU 드라이버는 가상 인터페이스(VIF)를 지원하지 않습니다. 이 어댑터에서는 모니터 + 매니지드 모드 동시 사용이 불가능합니다.

## 중국 미러 참조

| 리소스 | URL | 용도 |
|----------|-----|---------|
| Alfa 공식 드라이버 | [files.alfa.com.tw](https://files.alfa.com.tw) | 드라이버 패키지 |
| Alfa 문서 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 제품 매뉴얼 |
| 8821au 드라이버 (GitHub) | [github.com/morrownr/8821au-20210708](https://github.com/morrownr/8821au-20210708) | RTL8811AU 드라이버 |
| 칭화대학교 미러 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 알리클라우드 미러 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (권장) |
| 중국과학기술대학 미러 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (권장) |
| 화웨이클라우드 미러 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 이미지 |

## 중국 환경을 위한 그 외 Alfa 어댑터 가이드

- [AWUS036ACH 중국 설치 가이드](/ko/blog/awus036ach-china-install-guide/) — RTL8812AU, 고출력
- [AWUS036ACM 중국 설치 가이드](/ko/blog/awus036acm-china-install-guide/) — MT7612U, 완전한 VIF
- AWUS036ACS ← 현재 보고 계신 문서입니다
- [AWUS036AX 중국 설치 가이드](/ko/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER 중국 설치 가이드](/ko/blog/awus036axer-china-install-guide/) — RTL8832BU, 나노
- [AWUS036AXM 중국 설치 가이드](/ko/blog/awus036axm-china-install-guide/) — MT7921AUN, L자형
- [AWUS036AXML 중국 설치 가이드](/ko/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS 중국 설치 가이드](/ko/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

궁금한 점이 있으신가요? 아래에 댓글을 남기거나 [yupitek.com](https://yupitek.com/ko/contact/)으로 문의해 주십시오.

## 참고 자료

1. [aircrack-ng 공식 문서](https://www.aircrack-ng.org/)
2. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
3. [Kali Linux 공식 문서](https://www.kali.org/docs/)
4. [GitHub: morrownr/8821au-20210708](https://github.com/morrownr/8821au-20210708)
