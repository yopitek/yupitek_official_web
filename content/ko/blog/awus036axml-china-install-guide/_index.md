---
title: "중국에서 ALFA AWUS036AXML 드라이버 설치 가이드: Kali Linux, Ubuntu, Debian 및 Raspberry Pi"
description: "국내 미러를 이용해 중국에서 ALFA AWUS036AXML 드라이버를 설치하는 단계별 가이드. MT7921AUN WiFi 6E 커널 내장 드라이버, 완전한 모니터 모드 및 VIF 지원. Kali Linux, Ubuntu 22/24, Debian, Raspberry Pi를 다룹니다. GitHub가 필요 없습니다."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "AWUS036AXML은 어떤 칩셋을 사용하나요? AWUS036AXM과 동일한가요?"
    answer: "동일한 MediaTek MT7921AUN 칩셋을 사용하지만, AWUS036AXML은 플래그십 USB-C 버전입니다."
  - question: "AWUS036AXML은 드라이버를 수동으로 설치해야 하나요?"
    answer: "아니요. mt7921u 드라이버는 Linux 커널 5.18부터 포함되어 있습니다. 펌웨어 패키지만 설치하면 됩니다."
  - question: "AWUS036AXML은 VIF 가상 인터페이스를 지원하나요?"
    answer: "네. MT7921AUN은 커널 네이티브 VIF를 완전히 지원하여 모니터 인터페이스와 매니지드 인터페이스를 동시에 사용할 수 있습니다."
  - question: "AWUS036AXML 드라이버가 Ubuntu 22.04에서 로드되지 않는 이유는 무엇인가요?"
    answer: "Ubuntu 22.04는 커널 5.15를 탑재하는데 이는 너무 오래된 버전입니다. HWE 커널을 설치하여 5.18 이상으로 업그레이드하세요."
  - question: "AWUS036AXML의 USB ID는 무엇인가요?"
    answer: "MediaTek MT7921AUN의 USB ID는 0e8d:7961입니다. lsusb로 확인하세요."
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axml-china-install-guide"
tags: ["alfa", "awus036axml", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6e", "vif"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 7
related_product: "/ko/products/alfa/awus036axml/"
featureimage: "/images/blog/awus036axml-china-install-guide.webp"
---

AWUS036AXML은 ALFA의 WiFi 6E 플래그십으로, 2.4 GHz, 5 GHz, 그리고 혼잡하지 않은 6 GHz 대역을 아우르는 트라이 밴드 USB-C 어댑터입니다. MT7921AUN 칩은 `mt7921u` 드라이버를 사용하며, 이 드라이버는 Linux 커널 5.18부터 내장되어 있습니다. Ubuntu 24.04와 Kali 2025에서는 국내 미러에서 펌웨어 패키지를 설치하기만 하면 플러그 앤 플레이로 작동합니다. 이 가이드는 GitHub를 전혀 사용하지 않고 펌웨어, 드라이버 검증, 모니터 모드, VIF까지 전체 설정과 패킷 인젝션 관련 주의사항(stock kernel 6.17에서 실패)을 다룹니다.

{{< tldr >}}
AWUS036AXML은 MT7921AUN 칩셋을 사용합니다. 커널 내장 드라이버를 갖춘 WiFi 6E 트라이 밴드 USB-C 플래그십 어댑터입니다. 펌웨어를 설치한 후 모니터 모드, AP/WPA3, VIF를 바로 사용할 수 있습니다(패킷 인젝션은 stock kernel 6.17 실측에서 실패).
{{< /tldr >}}

다음 항목을 준비하세요:




## 시작하기 전에

다음 항목을 준비하세요:

1. <strong>ALFA AWUS036AXML</strong> 어댑터와 USB-C 케이블
2. 전원 공급형 USB 허브 — Raspberry Pi를 사용하는 경우 필수
3. 국내 미러에 접속할 수 있는 인터넷 연결

어댑터를 연결한 다음, 시스템이 이를 인식하는지 확인하세요:

```bash
lsusb
```

출력에서 다음 항목을 찾으세요:

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

`0e8d:7961`이 보이면 어댑터가 감지된 것입니다. 아래의 해당 OS 섹션으로 이동하세요.

보이지 않으면 다른 USB-C 포트나 케이블을 시도한 후 다시 `lsusb`를 실행하세요.

## 운영 체제 선택

사용 중인 OS에 맞는 섹션으로 이동하세요:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

이미 설치했나요? 다음으로 건너뛰세요:

- [모니터 모드 활성화](#enable-monitor-mode)
- [패킷 인젝션 테스트](#test-packet-injection)
- [가상 인터페이스 (VIF)](#virtual-interface-vif)
- [VM USB 패스스루](#virtual-machine-usb-passthrough)

---

## Kali Linux

MT7921AUN 드라이버는 이미 Kali 커널에 포함되어 있습니다. 국내 미러에서 제공하는 MediaTek 펌웨어 패키지만 있으면 됩니다.

### 1단계: 중국 미러로 전환

터미널에서 소스 목록을 엽니다.

```bash
sudo nano /etc/apt/sources.list
```

기존 내용을 모두 삭제한 다음, 다음 줄을 붙여넣으세요:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

저장: <strong>Ctrl+O</strong>를 누르고 Enter를 누른 다음, Ctrl+X로 종료합니다. 패키지 인덱스를 새로 고칩니다.

```bash
sudo apt update
```

> <strong>백업 미러:</strong> USTC(중국과기대) 미러가 느리면 Tsinghua(칭화대) 미러를 대신 사용하세요:
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 2단계: 펌웨어 설치

MT7921AUN은 `firmware-misc-nonfree`와 `linux-firmware`에 포함된 펌웨어 블롭이 필요합니다. 이것이 없으면 드라이버는 로드되지만 어댑터 초기화에 실패합니다.

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### 3단계: 드라이버 검증

재부팅 후 어댑터를 연결하고 확인합니다.

```bash
lsmod | grep mt7921
```

출력에 `mt7921u`가 보여야 합니다. 그런 다음 무선 인터페이스가 생성되었는지 확인하세요.

```bash
iwconfig
```

`wlan0` 또는 `wlan1`을 찾으세요. 나타나면 드라이버가 작동하는 것입니다.

---

### 4단계: 모니터 모드 활성화 {#enable-monitor-mode}

먼저 인터페이스 이름을 확인하세요.

```bash
iwconfig
```

표시된 이름(예: `wlan1`)을 사용합니다. 간섭을 일으키는 프로세스를 종료한 다음 모니터 모드로 전환합니다.

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

전환을 확인합니다.

```bash
iwconfig
```

인터페이스에서 `Mode:Monitor`를 찾으세요.

---

### 5단계: 패킷 인젝션 테스트 {#test-packet-injection}

⚠️ <strong>버전 전제:</strong> 커널 6.16 이전에서는 인젝션이 동작한다는 커뮤니티 보고가 있습니다. 그러나 stock kernel 6.17(ASUS GX10, Ubuntu 24.04 ARM64)에서 실측한 결과 실패했습니다. `aireplay-ng --test`가 `Found 0 APs` / `No Answer`를 표시하므로 deauth 및 handshake 캡처는 불가능합니다. 원인은 커널 6.16 이후의 mac80211 chanctx 회귀이며 칩 자체의 한계가 아닙니다. 커뮤니티 patched 드라이버로 인젝션을 동작시킬 수 있지만 펌웨어가 속도를 고정합니다(1/6 Mbps, HT/VHT 인젝션 불가). 인젝션이 필요하면 AWUS036ACH / EACS / ACS / AX(ACM / ACHM도 가능)를 사용하세요. 모니터 모드, AP, WPA3, VIF는 정상 동작합니다.

```bash
sudo aireplay-ng --test wlan1
```

성공적인 결과:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

실패하면 재부팅 후 다시 시도하세요.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — 커널 6.8, 플러그 앤 플레이

Ubuntu 24.04는 MT7921AUN 드라이버를 기본 내장한 커널 6.8을 탑재합니다.

### 1단계: 중국 미러로 전환

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

모든 내용을 삭제하고 다음을 붙여넣으세요:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

`Ctrl+O`로 저장한 다음 `Ctrl+X`로 종료합니다.

```bash
sudo apt update
```

### 2단계: 펌웨어 설치

```bash
sudo apt install -y linux-firmware
sudo reboot
```

### 3단계: 검증 및 모니터 모드 활성화

재부팅 후 `lsmod | grep mt7921`을 실행하여 드라이버가 로드되었는지 확인한 다음, 위의 Kali 모니터 모드 단계(4단계)를 따르세요.

---

### Ubuntu 22.04 (Jammy) — HWE 커널 필요

Ubuntu 22.04는 커널 5.15를 탑재합니다. MT7921AUN 드라이버는 커널 5.18 이상이 필요합니다. 먼저 HWE 커널을 설치하세요.

### 1단계: 중국 미러로 전환

```bash
sudo nano /etc/apt/sources.list
```

모든 줄을 다음으로 교체하세요:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

저장 후 종료합니다(`Ctrl+O`, 그다음 `Ctrl+X`).

```bash
sudo apt update
```

### 2단계: HWE 커널 설치

```bash
sudo apt install -y linux-generic-hwe-22.04
sudo reboot
```

재부팅 후 커널 버전을 확인합니다:

```bash
uname -r
```

5.19 이상이 표시되어야 합니다. 그런 다음 위와 같이 펌웨어를 설치하고 모니터 모드를 활성화합니다.

### 3단계: 펌웨어 설치

```bash
sudo apt install -y linux-firmware
sudo reboot
```

---

## Debian

### 1단계: 중국 미러로 전환

```bash
sudo nano /etc/apt/sources.list
```

모든 내용을 삭제하고 다음을 붙여넣으세요(Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

`Ctrl+O`로 저장한 다음 `Ctrl+X`로 종료합니다.

```bash
sudo apt update
```

### 2단계: 펌웨어 설치

Debian 12 Bookworm은 커널 6.1을 탑재합니다 — MT7921AUN과 호환됩니다.

```bash
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

### 3단계: 검증 및 모니터 모드 활성화

```bash
lsmod | grep mt7921
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### 4단계: 패킷 인젝션 테스트

⚠️ stock kernel 6.17에서는 이 테스트가 실패합니다(위의 버전 전제 참조). 인젝션이 필요하면 AWUS036ACH / EACS / ACS / AX를 사용하세요.

```bash
sudo aireplay-ng --test wlan1
```

`Injection is working!`이 표시되면 어댑터가 완전히 작동하는 것입니다.

---

## Raspberry Pi 4B / 5

> AWUS036AXML은 부하 시 최대 2.7W를 소모합니다. Raspberry Pi에서는 항상 전원 공급형 USB 허브를 사용하세요.

### 1단계: Kali Linux ARM64 이미지 다운로드

공식 페이지: https://www.kali.org/get-kali/#kali-arm

<strong>Raspberry Pi 4 (64-bit)</strong> 또는 <strong>Raspberry Pi 5 (64-bit)</strong>를 선택하세요 — 64비트가 필수입니다.

> <strong>중국 미러:</strong> https://repo.huaweicloud.com/kali-images/ — 최신 릴리스 폴더로 이동하여 ARM64 이미지를 다운로드하세요.

### 2단계: MicroSD에 플래싱

```bash
lsblk
# /dev/sdX를 실제 SD 카드로 교체하세요
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

기본 자격 증명: <strong>kali / kali</strong>.

### 3단계: 중국 미러로 전환 및 펌웨어 설치

```bash
sudo nano /etc/apt/sources.list
```

다음으로 교체하세요:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

그런 다음:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

### 4단계: 드라이버 검증

```bash
lsmod | grep mt7921
```

`mt7921u`가 나타나야 합니다.

### 5단계: 모니터 모드 활성화

내장 Wi-Fi가 있는 Pi에서는 AWUS036AXML이 `wlan1`로 표시됩니다.

```bash
iwconfig
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### 6단계: 패킷 인젝션 테스트

⚠️ stock kernel 6.17에서는 이 테스트가 실패합니다(위의 버전 전제 참조). 인젝션이 필요하면 AWUS036ACH / EACS / ACS / AX를 사용하세요.

```bash
sudo aireplay-ng --test wlan1
```

---

## 가상 머신 USB 패스스루 {#virtual-machine-usb-passthrough}

### VirtualBox

1. VM을 종료합니다. <strong>설정 → USB</strong>로 이동합니다.
2. <strong>USB 3.0 (xHCI) 컨트롤러</strong>를 활성화합니다.
3. <strong>+</strong>를 클릭하여 USB 필터를 추가합니다.
4. 선택: <strong>MediaTek Inc.</strong> (ID: 0e8d:7961).
5. VM을 시작합니다 — 어댑터가 Kali 내부에 나타납니다.

VM에서 `lsusb`를 실행하여 `0e8d:7961`을 확인한 다음, 위의 Kali 단계를 따르세요.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. VM을 시작합니다.
2. 메뉴: <strong>Virtual Machine → USB & Bluetooth</strong>.
3. <strong>MediaTek MT7921AUN</strong>을 찾아 <strong>Connect</strong>를 클릭합니다.
4. VM에서 `lsusb`를 실행하여 확인한 다음, 위의 Kali 단계를 따르세요.

---

## 가상 인터페이스 (VIF) {#virtual-interface-vif}

MT7921AUN은 커널 네이티브 VIF를 완전히 지원합니다. 패치 없이 동일한 어댑터에서 모니터 인터페이스와 매니지드 인터페이스를 동시에 실행할 수 있습니다.

### 매니지드 모드와 함께 모니터 인터페이스 생성

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
iwconfig
```

`wlan0`(매니지드)과 `mon0`(모니터)이 동시에 활성화된 것을 볼 수 있습니다.

### 연결을 유지하면서 모니터링

```bash
sudo airodump-ng mon0
```

`wlan0`은 연결을 유지하고 `mon0`은 범위 내 모든 것을 캡처합니다.

### 가짜 AP + 모니터

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
iwconfig
```

> <strong>hostapd에 대한 참고:</strong> 완전한 AP 운영을 위해서는 `hostapd` 구성이 필요합니다. 위 단계는 어댑터가 인터페이스를 생성할 수 있음을 확인하는 것이며, 실제 AP 구성은 별도의 주제입니다.

---

{{< faq >}}

## 문제 해결

| 문제 | 가능한 원인 | 해결 방법 |
|---------|-------------|-----|
| `lsusb`에 0e8d:7961이 표시되지 않음 | 어댑터에 전원이 없거나 불량 케이블 | 다른 USB-C 포트를 시도하세요. Raspberry Pi에서는 전원 공급형 허브를 사용하세요. |
| `lsmod`에 mt7921u가 표시되지 않음 | 펌웨어가 설치되지 않았거나 오래된 커널 | `sudo apt install linux-firmware firmware-misc-nonfree && sudo reboot` 실행 |
| Ubuntu 22.04에서 드라이버가 로드되지 않음 | 커널 5.15가 너무 오래됨 | HWE 설치: `sudo apt install linux-generic-hwe-22.04` |
| 인터페이스는 나타나지만 연결되지 않음 | 펌웨어 블롭 누락 | `sudo apt install firmware-misc-nonfree` 실행 후 재부팅 |
| 모니터 모드 전환 실패 | 인터페이스가 아직 활성 상태 | `iw dev` 명령 전에 `sudo ip link set wlan1 down` 실행 |
| 인젝션 테스트가 "No Answer" 표시 | AP가 너무 멀거나 잘못된 인터페이스 (또는 커널 6.16 이상: mac80211 chanctx 회귀) | 더 가까이 이동하세요. `iwconfig`로 `Mode:Monitor`를 확인하세요. 6.16 이상에서 인젝션이 필요하면 ACH / EACS / ACS / AX를 사용하세요. |
| VIF 인터페이스 생성 실패 | 드라이버가 완전히 로드되지 않음 | 분리 후: `sudo rmmod mt7921u && sudo modprobe mt7921u` |

## 중국 미러 참고 자료

| 리소스 | URL | 용도 |
|----------|-----|---------|
| Alfa 공식 드라이버 | [files.alfa.com.tw](https://files.alfa.com.tw) | 드라이버 패키지, 펌웨어 |
| Alfa 문서 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 제품 설명서 |
| 칭화대학 미러 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 알리윈 미러 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (권장) |
| 중국과기대 미러 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (권장) |
| 화웨이 클라우드 미러 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 이미지 (백업) |

## 중국용 Alfa 어댑터 가이드 더 보기

이 글은 <strong>Alfa 중국 설치 가이드</strong> 시리즈의 일부입니다:

- [AWUS036ACH 중국 설치 가이드](/ko/blog/awus036ach-china-install-guide/) — RTL8812AU, 고출력
- [AWUS036ACM 중국 설치 가이드](/ko/blog/awus036acm-china-install-guide/) — MT7612U, 완전한 VIF
- [AWUS036ACS 중국 설치 가이드](/ko/blog/awus036acs-china-install-guide/) — RTL8811AU, 모니터 모드
- [AWUS036AX 중국 설치 가이드](/ko/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER 중국 설치 가이드](/ko/blog/awus036axer-china-install-guide/) — RTL8832BU, 나노
- [AWUS036AXM 중국 설치 가이드](/ko/blog/awus036axm-china-install-guide/) — MT7921AUN, L자형 USB-A
- AWUS036AXML ← 현재 보고 있는 글
- [AWUS036EACS 중국 설치 가이드](/ko/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

궁금한 점이 있으신가요? 아래에 댓글을 남기거나 [yupitek.com](https://yupitek.com/ko/contact/)으로 문의하세요.

## 참고 문헌

1. [Linux Kernel mt7921 Driver](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [aircrack-ng 공식 문서](https://www.aircrack-ng.org/)
3. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
4. [Kali Linux 공식 문서](https://www.kali.org/docs/)
