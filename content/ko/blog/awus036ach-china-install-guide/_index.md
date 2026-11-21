---
title: "중국 환경에서의 ALFA AWUS036ACH 드라이버 설치 가이드: Kali Linux, Ubuntu, Debian 및 Raspberry Pi"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036ACH는 어떤 칩셋을 사용하나요? 별도의 드라이버가 필요한가요?"
    answer: "AWUS036ACH는 Realtek RTL8812AU 칩셋을 사용합니다. 해당 드라이버는 Linux 커널에 기본 내장되어 있지 않으므로 수동으로 설치해야 합니다."
  - question: "중국에서 AWUS036ACH 드라이버를 설치하려면 VPN이 반드시 필요한가요?"
    answer: "반드시 필요하지는 않습니다. 검증된 GitHub 저장소(morrownr/8812au-20210820)에서 드라이버를 복제하십시오. GitHub 접속이 느린 경우 신뢰할 수 있는 프록시 또는 미러를 사용하면 됩니다. 빌드 도구는 중국 내 국내 미러에서 그대로 설치할 수 있습니다."
  - question: "AWUS036ACH는 모니터 모드와 패킷 인젝션을 지원하나요?"
    answer: "지원합니다. RTL8812AU 드라이버를 설치한 후 airmon-ng로 모니터 모드를 활성화하고 aireplay-ng로 패킷 인젝션을 테스트할 수 있습니다."
  - question: "AWUS036ACH를 Raspberry Pi에서 사용할 수 있나요?"
    answer: "사용할 수 있습니다. 전원 공급형 USB 허브를 사용하고 Kali ARM64 이미지를 플래시하면 가장 좋은 결과를 얻을 수 있습니다."
  - question: "Kali Linux에서 AWUS036ACH 드라이버를 설치하는 명령어는 무엇인가요?"
    answer: "sudo apt install realtek-rtl88xxau-dkms 명령을 실행하면 Kali에 사전 컴파일된 드라이버가 설치됩니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "driver", "china", "monitor-mode"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 1
description: "중국 내 국내 미러를 활용하여 ALFA AWUS036ACH 드라이버를 설치하는 단계별 가이드입니다. Kali Linux, Ubuntu 22/24, Debian, Raspberry Pi를 모두 다룹니다. 빌드 도구는 국내 미러에서, 드라이버 소스는 검증된 GitHub 저장소에서 받습니다."
related_product: "/ko/products/alfa/awus036ach/"
featureimage: "/images/blog/awus036ach-china-install-guide.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

AWUS036ACH를 막 구입했는데 Linux 장비가 이를 인식하지 못하는 상황일 것입니다. 이는 정상적인 현상입니다. 이 칩은 RTL8812AU 드라이버를 필요로 하며 플러그 앤 플레이로 동작하지 않습니다. 본 가이드는 시스템 패키지는 국내 미러를, 드라이버 소스는 검증된 GitHub 저장소를 사용하여 약 30분 안에 전체 설치 과정을 안내합니다. GitHub 접속이 느린 경우 신뢰할 수 있는 프록시 또는 미러를 사용하십시오.

{{< tldr >}}
AWUS036ACH는 RTL8812AU 칩셋을 사용합니다. Kali에서는 apt로 DKMS 드라이버를 설치하고, Ubuntu/Debian에서는 GitHub에서 소스를 컴파일합니다. 모니터 모드와 패킷 인젝션은 30분 안에 사용할 수 있습니다.
{{< /tldr >}}

다음 항목을 미리 준비하십시오.




## 시작하기 전에

다음 항목을 미리 준비하십시오.

1. <strong>ALFA AWUS036ACH</strong> 어댑터
2. USB 케이블(제품 상자에 동봉된 케이블을 사용해도 무방합니다)
3. 전원 공급형 USB 허브 — Raspberry Pi를 사용하는 경우 필수입니다
4. 국내 미러에 접속할 수 있는 정상적인 인터넷 연결

어댑터를 연결한 다음 시스템이 이를 인식하는지 확인하십시오.

```bash
lsusb
```

출력에서 다음 항목을 찾으십시오.

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

`0bda:8812`가 보이면 어댑터가 정상적으로 인식된 것입니다. 아래의 해당 OS 섹션으로 이동하십시오.

보이지 않는 경우 다른 USB 포트를 사용하거나 케이블을 교체한 후 다시 `lsusb`를 실행하십시오.

## 운영체제 선택

사용 중인 OS에 해당하는 섹션으로 이동하십시오.

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

이미 설치를 완료했다면 다음으로 건너뛰십시오.

- [모니터 모드 활성화](#enable-monitor-mode)
- [패킷 인젝션 테스트](#test-packet-injection)
- [가상 머신 USB 패스스루](#virtual-machine-usb-passthrough)

---

## Kali Linux

Kali에는 강력한 무선 도구가 기본으로 포함되어 있습니다. AWUS036ACH 드라이버를 구동하는 데는 네 단계가 필요합니다. 먼저 빠른 중국 미러로 전환하여 모든 다운로드를 신속하게 유지하는 것으로 시작합니다.

### 1단계: 중국 미러로 전환

터미널에서 소스 목록 파일을 엽니다.

```bash
sudo nano /etc/apt/sources.list
```

기존 내용을 모두 삭제한 다음 아래 한 줄을 붙여넣습니다.

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

파일을 저장합니다. <strong>Ctrl+O</strong>를 누른 후 Enter, 이어서 Ctrl+X를 눌러 종료합니다. 패키지 인덱스를 새로 고칩니다.

```bash
sudo apt update
```

> <strong>백업 미러:</strong> 사용 중인 연결에서 中科大(USTC)가 느린 경우 清华(Tsinghua)를 대신 사용하십시오.
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 2단계: 드라이버 설치

Kali의 패키지 저장소에는 사전 빌드된 DKMS 드라이버가 포함되어 있습니다. 한 번의 명령으로 설치합니다.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

DKMS는 커널이 업데이트될 때마다 드라이버를 자동으로 재컴파일하므로, 업그레이드 후에 수동으로 재설치할 필요가 없습니다.

드라이버가 올바르게 로드되었는지 확인합니다.

```bash
modinfo 88XXau | grep -E "filename|version"
```

`.ko`로 끝나는 `filename` 줄과 `5.6.4.2`와 같은 버전 문자열을 표시하는 `version` 줄이 보여야 합니다. 두 줄이 모두 나타나면 드라이버가 준비된 것입니다.

---

### 2단계 (대안): 소스에서 수동 컴파일

위의 `apt install`이 실패한 경우에만 이 섹션을 따르십시오. 먼저 빌드 종속성을 설치합니다.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

GitHub에서 드라이버 소스를 다운로드합니다.

```bash
git clone https://github.com/morrownr/8812au-20210820.git
```

> <strong>참고:</strong> 유지보수되는 업스트림 드라이버는 [morrownr/8812au-20210820](https://github.com/morrownr/8812au-20210820)입니다. GitHub 접속이 느린 경우 신뢰할 수 있는 프록시 또는 미러를 사용하십시오. [files.alfa.com.tw](https://files.alfa.com.tw)에서 소스 아카이브를 직접 다운로드할 수도 있습니다.

복제한 디렉터리로 이동한 다음 컴파일 및 설치를 진행합니다.

```bash
cd 8812au-20210820
sudo ./install-driver.sh
```

드라이버를 실행 중인 커널에 로드합니다.

```bash
sudo modprobe 8812au
```

---

### 3단계: 모니터 모드 활성화 {#enable-monitor-mode}

어댑터를 모니터 모드로 전환하기 전에 시스템이 어떤 인터페이스 이름을 할당했는지 확인하십시오.

```bash
iwconfig
```

`wlan0` 또는 `wlan1` 항목을 찾으십시오. 아래 명령에서 해당 이름을 사용하십시오.

NetworkManager와 wpa_supplicant를 중지하십시오. 두 프로세스는 어댑터를 두고 서로 충돌하며 모니터 모드를 차단합니다.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

전환이 정상적으로 이루어졌는지 확인합니다.

```bash
iwconfig
```

`Mode:Monitor`로 표시되는 `wlan0mon`과 같은 항목을 찾으십시오. 이 항목이 보이면 어댑터가 패킷 캡처를 수행할 준비가 된 것입니다.

---

### 4단계: 패킷 인젝션 테스트 {#test-packet-injection}

모니터 인터페이스를 대상으로 인젝션 테스트를 실행합니다.

```bash
sudo aireplay-ng --test wlan0mon
```

성공한 경우 다음과 같은 결과가 표시됩니다.

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

테스트가 실패하면 장비를 재부팅한 후 테스트를 다시 실행하십시오. 재부팅 후에도 계속 실패한다면 다른 프로세스가 인터페이스를 점유하고 있지 않은지 확인하십시오. `iwconfig`를 실행하여 `wlan0mon`만 나타나고 다른 어떤 것도 어댑터를 점유하고 있지 않은지 확인하십시오.

---

## Ubuntu 22.04 / 24.04

Ubuntu는 패키지 파일 형식이 서로 다른 두 가지 버전으로 나뉩니다. 아래 단계는 두 경우를 모두 다룹니다. 미러로는 <strong>阿里云(Aliyun)</strong>을 사용하십시오. 빠르고 안정적이며 Alibaba가 유지보수합니다.

### 1단계: 중국 미러로 전환

사용 중인 Ubuntu 버전을 선택하여 해당 경로만 따르십시오.

#### Ubuntu 24.04 (Noble)

새로운 DEB822 형식의 소스 파일을 엽니다.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

파일의 모든 내용을 삭제하고 아래 내용을 정확히 붙여넣습니다.

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

`Ctrl+O`로 저장한 다음 `Ctrl+X`로 종료합니다.

#### Ubuntu 22.04 (Jammy)

대신 기존 형식의 소스 파일을 엽니다.

```bash
sudo nano /etc/apt/sources.list
```

기존의 모든 줄을 다음으로 교체합니다.

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

같은 방식으로 저장하고 종료합니다(`Ctrl+O` 후 `Ctrl+X`).

#### 패키지 인덱스 새로 고침

소스 파일을 수정한 후 두 버전 모두 다음을 실행합니다.

```bash
sudo apt update
```

---

### 2단계: 빌드 종속성 설치

드라이버는 소스에서 컴파일되므로 먼저 커널 헤더와 빌드 도구가 필요합니다.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

이 명령은 gcc, make, 그리고 현재 실행 중인 커널과 정확히 일치하는 헤더를 함께 설치합니다. `$(uname -r)` 부분이 커널 버전을 자동으로 감지하므로 직접 입력할 필요가 없습니다.

---

### 3단계: 드라이버 소스 다운로드 (GitHub)

GitHub에서 드라이버 저장소를 복제합니다.

```bash
git clone https://github.com/morrownr/8812au-20210820.git
```

이어서 복제한 폴더로 이동합니다.

```bash
cd 8812au-20210820
```

> <strong>참고:</strong> GitHub 접속이 느린 경우 신뢰할 수 있는 프록시 또는 미러를 사용하십시오.

---

### 4단계: 컴파일 및 설치

설치 스크립트를 실행합니다. 이 스크립트는 커널 모듈을 빌드하고 DKMS에 등록하여 커널 업그레이드 후에도 유지되도록 합니다.

```bash
sudo ./install-driver.sh
```

DKMS가 모듈을 등록했는지 확인합니다.

```bash
sudo dkms status
```

새 모듈이 깨끗하게 로드되도록 재부팅합니다.

```bash
sudo reboot
```

모듈을 실행 중인 커널에 로드합니다.

```bash
sudo modprobe 8812au
```

모듈이 올바르게 로드되었는지 확인합니다.

```bash
modinfo 8812au | grep filename
```

`8812au.ko` 또는 이와 유사한 이름으로 끝나는 경로가 보여야 합니다. 명령이 출력을 반환하면 드라이버가 활성화된 것입니다.

---

### 5단계: 모니터 모드 활성화

먼저 무선 인터페이스를 방해할 수 있는 프로세스를 모두 종료합니다.

```bash
sudo airmon-ng check kill
```

그런 다음 어댑터를 모니터 모드로 전환합니다.

```bash
sudo airmon-ng start wlan0
```

> <strong>참고:</strong> 인터페이스 이름이 `wlan0`이 아니라 `wlan1`일 수 있습니다. 먼저 `iwconfig`를 실행하여 나열된 모든 무선 인터페이스를 확인한 다음, 위 명령에서 올바른 이름으로 바꾸십시오.

---

### 6단계: 패킷 인젝션 테스트

어댑터가 모니터 모드인 상태에서 인젝션 테스트를 실행합니다.

```bash
sudo aireplay-ng --test wlan0mon
```

성공한 경우 `Injection is working!`과 같은 줄이 표시됩니다. 인터페이스 관련 오류가 보이면 `iwconfig wlan0mon`으로 모니터 모드가 활성화되어 있는지 다시 확인하십시오.

---

## Debian

Debian의 패키지 관리자는 기본적으로 해외 서버를 가리킵니다. 清华大学(Tsinghua University) 미러로 전환하면 해외 서버의 느린 속도가 로컬 수준의 빠른 속도로 바뀝니다.

### 1단계: 중국 미러로 전환

소스 목록 파일을 엽니다.

```bash
sudo nano /etc/apt/sources.list
```

안의 내용을 모두 삭제하고 다음 세 줄을 붙여넣습니다(Debian 12 Bookworm).

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

`Ctrl+O`로 저장한 다음 `Ctrl+X`로 종료합니다. 패키지 인덱스를 새로 고칩니다.

```bash
sudo apt update
```

### 2단계: 빌드 종속성 설치

AWUS036ACH 드라이버는 소스에서 컴파일되므로 커널 헤더와 빌드 도구가 필요합니다.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

이 명령은 헤더 패키지를 현재 실행 중인 커널 버전에 맞게 자동으로 선택합니다.

### 3단계: 드라이버 소스 다운로드 (GitHub)

GitHub에서 드라이버 저장소를 복제합니다.

```bash
git clone https://github.com/morrownr/8812au-20210820.git
```

프로젝트 폴더로 이동합니다.

```bash
cd 8812au-20210820
```

> <strong>참고:</strong> GitHub 접속이 느린 경우 신뢰할 수 있는 프록시 또는 미러를 사용하십시오.

### 4단계: 컴파일 및 설치

`8812au-20210820` 폴더 안에서 다음 명령을 순서대로 실행합니다.

```bash
sudo ./install-driver.sh
sudo modprobe 8812au
```

`dkms`가 드라이버를 등록하므로 커널 업데이트 후에도 자동으로 유지됩니다.

### 5단계: 모니터 모드 활성화

모드를 전환하기 전에 <strong>방해 프로세스를 종료</strong>하십시오.

```bash
sudo airmon-ng check kill
```

어댑터에서 모니터 모드를 시작합니다.

```bash
sudo airmon-ng start wlan0
```

`airmon-ng`가 없는 경우 먼저 설치합니다.

```bash
sudo apt install -y aircrack-ng
```

인터페이스가 올라왔는지 확인합니다.

```bash
iwconfig
```

출력에서 `wlan0mon`이라는 이름의 인터페이스를 찾으십시오.

### 6단계: 패킷 인젝션 테스트

```bash
sudo aireplay-ng --test wlan0mon
```

연속으로 표시되는 인젝션 테스트 결과는 어댑터가 정상적으로 작동함을 확인해 줍니다. 이제 사용할 준비가 되었습니다.

---

## Raspberry Pi 4B / 5

> AWUS036ACH는 약 500mW를 소비합니다. 이를 Raspberry Pi의 USB 포트에 직접 연결하면 부하 상태에서 Pi가 성능을 제한하거나 재시작할 수 있습니다. <strong>항상 전원 공급형 USB 허브를 사용하십시오.</strong>

---

### 1단계: Kali Linux ARM64 이미지 다운로드

공식 Kali ARM 다운로드 페이지로 이동합니다.
https://www.kali.org/get-kali/#kali-arm

사용 중인 보드에 맞게 <strong>Raspberry Pi 4 (64-bit)</strong> 또는 <strong>Raspberry Pi 5 (64-bit)</strong>를 선택하십시오. 32비트 이미지는 다운로드하지 마십시오. 드라이버 빌드에는 64비트 커널이 필요합니다.

> <strong>중국 미러:</strong> kali.org의 로딩이 느린 경우 华为云(Huawei Cloud)을 사용해 보십시오.
> https://repo.huaweicloud.com/kali-images/
> 최신 릴리스 폴더로 이동하여 같은 ARM64 이미지를 다운로드하십시오.

---

### 2단계: MicroSD에 플래시

microSD 카드를 삽입한 다음, 어떤 것을 쓰기 전에 장치 경로를 확인하십시오.

```bash
lsblk
```

목록에서 카드를 찾으십시오. `sdb` 또는 `mmcblk0`와 같은 형태로 표시됩니다. 그런 다음 `/dev/sdX`를 실제 경로로 바꾸어 이미지를 플래시합니다.

```bash
# /dev/sdX를 실제 SD 카드 경로로 바꾸십시오(lsblk로 확인)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

카드를 빼기 전에 `sync`가 완료될 때까지 기다리십시오. 카드로 Pi를 부팅합니다. 부팅 후 기본 자격 증명은 <strong>kali / kali</strong>입니다.

---

### 3단계: 중국 미러로 전환

최초 부팅 후 패키지 소스 파일을 엽니다.

```bash
sudo nano /etc/apt/sources.list
```

파일의 모든 내용을 삭제하고 아래 한 줄로 교체합니다.

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

저장합니다. <strong>Ctrl+O</strong>를 누른 후 Enter, 이어서 Ctrl+X를 누릅니다. 이제 미러를 적용하고 시스템을 업그레이드합니다.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

재부팅 시 드라이버를 설치하기 전에 커널 업데이트가 적용됩니다.

---

### 4단계: 드라이버 설치 (ARM64)

DKMS 패키지는 ARM64에서도 x86과 완전히 동일하게 작동하며, 별도의 특별한 단계가 필요하지 않습니다.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

이 명령이 패키지를 찾을 수 없다는 오류를 반환하면, 대신 소스에서 드라이버를 컴파일하십시오.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
sudo ./install-driver.sh
sudo modprobe 8812au
```

---

### 5단계: 모니터 모드 활성화

어댑터를 다루기 전에 Pi가 할당한 인터페이스 이름을 확인하십시오.

```bash
iwconfig
```

내장 Wi-Fi 칩이 있는 Pi에서는 AWUS036ACH가 `wlan1`로 표시됩니다. 내장 라디오가 `wlan0`을 차지하기 때문입니다. 위에서 `iwconfig`가 보고한 이름을 사용하십시오.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

`iwconfig`를 다시 실행하여 `mon`으로 끝나는 항목(일반적인 Pi 사례에서는 `wlan1mon`)이 `Mode:Monitor`로 표시되는지 확인하십시오. 이 항목이 보이면 어댑터가 정상적으로 전환된 것입니다.

---

### 6단계: 패킷 인젝션 테스트

```bash
sudo aireplay-ng --test wlan1mon
```

`wlan1mon`을 5단계에서 나타난 모니터 인터페이스 이름으로 바꾸십시오. 정상적으로 작동하는 어댑터는 `Injection is working!`을 출력합니다. 테스트가 실패하면 재부팅한 후 다시 한 번 시도하십시오. Pi에서 가장 흔한 원인은 전원이 공급되지 않는 허브를 통한 불량 USB 연결이므로, 전원 공급형 허브를 사용하고 있는지 다시 확인하십시오.

---

## 가상 머신 USB 패스스루 {#virtual-machine-usb-passthrough}

macOS 또는 Windows에서 VM 안에 Kali Linux를 실행하고 있습니까? USB 어댑터를 게스트 OS로 전달해야 합니다.

### VirtualBox

1. VM의 전원을 끈 상태에서 <strong>Settings → USB</strong>로 이동합니다.
2. <strong>USB 3.0 (xHCI) Controller</strong>를 활성화합니다.
3. <strong>+</strong> 아이콘을 클릭하여 USB 필터를 추가합니다.
4. <strong>Realtek 802.11ac NIC [...]</strong>(ID: 0bda:8812)를 선택합니다.
5. VM을 시작합니다. 어댑터가 Kali 내부에 나타납니다.

VM 내부에서 `lsusb`를 실행하여 `0bda:8812`가 나타나는지 확인한 다음, 위의 Kali Linux 단계를 따르십시오.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. VM을 시작합니다.
2. 메뉴에서 <strong>Virtual Machine → USB & Bluetooth</strong>로 이동합니다.
3. <strong>Realtek 802.11ac NIC</strong>를 찾아 <strong>Connect</strong>를 클릭합니다.
4. 어댑터가 호스트에서 분리되고 VM 내부에 나타납니다.

VM 내부에서 `lsusb`를 실행하여 확인한 다음, 위의 Kali Linux 단계를 따르십시오.

### VIF(가상 인터페이스)에 관한 참고 사항

AWUS036ACH에 탑재된 RTL8812AU 칩은 Linux에서 VIF 지원이 제한적입니다. 동일한 어댑터에서 관리 모드와 모니터 모드(또는 AP 모드)를 동시에 안정적으로 실행할 수 없습니다.

VIF가 필요한 작업, 예를 들어 가짜 AP를 운영하면서 동시에 모니터링을 수행해야 하는 경우라면 AWUS036ACH는 적합한 도구가 아닙니다. 대신 [AWUS036ACM 설치 가이드](/ko/blog/awus036acm-china-install-guide/)를 확인하십시오. 해당 어댑터는 MT7612U 칩을 사용하며, 커널 네이티브 VIF를 완전히 지원하여 패치 없이도 여러 가상 인터페이스를 동시에 처리합니다.

---

{{< faq >}}

## 문제 해결

| 문제 | 가능한 원인 | 해결 방법 |
|---------|-------------|-----|
| `lsusb`에 0bda:8812가 표시되지 않음 | 어댑터에 전원이 공급되지 않거나 케이블 불량 | 다른 USB 포트를 사용하십시오. Raspberry Pi에서는 전원 공급형 허브를 사용하십시오. |
| `install-driver.sh`가 헤더 오류로 실패 | 커널 헤더가 없거나 버전 불일치 | `sudo apt install linux-headers-$(uname -r)` 실행 |
| `modprobe 8812au` 실패 | Secure Boot가 서명되지 않은 모듈을 차단 | BIOS에서 Secure Boot를 비활성화하거나 모듈에 서명하십시오 |
| 커널 업데이트 후 드라이버가 사라짐 | 드라이버가 DKMS에 등록되지 않음 | 소스 디렉터리에서 `sudo ./install-driver.sh`를 다시 실행하십시오 |
| `airmon-ng start wlan0` 실패 | NetworkManager가 여전히 실행 중 | 먼저 `sudo airmon-ng check kill`을 실행하십시오 |
| 모니터 모드가 시작되지만 트래픽이 캡처되지 않음 | 잘못된 채널 또는 잘못된 인터페이스 이름 | `iwconfig`로 인터페이스를 확인하십시오. 채널 설정: `iwconfig wlan0mon channel 6` |
| 인젝션 테스트에서 "No Answer" 표시 | AP가 너무 멀거나 잘못된 인터페이스 사용 | AP에 더 가까이 이동하십시오. `wlan0`이 아니라 `wlan0mon`을 사용하십시오 |

## 중국 미러 참조

본 가이드에서 사용한 모든 리소스입니다.

| 리소스 | URL | 용도 |
|----------|-----|---------|
| Alfa 공식 드라이버 | [files.alfa.com.tw](https://files.alfa.com.tw) | 드라이버 패키지, 펌웨어 |
| Alfa 문서 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 제품 매뉴얼 |
| 清华大学镜像 (칭화대학교 미러) | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 (Aliyun 미러) | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (권장) |
| 中科大镜像 (USTC 미러) | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (권장) |
| 华为云镜像 (Huawei Cloud 미러) | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 이미지 (백업) |
| RTL8812AU 드라이버 (GitHub) | [github.com/morrownr/8812au-20210820](https://github.com/morrownr/8812au-20210820) | 수동 컴파일 대체 수단 |

## 중국 환경용 추가 Alfa 어댑터 가이드

본 문서는 <strong>Alfa China Install Guide</strong> 시리즈의 일부입니다. 각 문서는 하나의 어댑터 모델을 다룹니다.

- AWUS036ACH ← 현재 보고 계신 문서
- [AWUS036ACM China Install Guide](/ko/blog/awus036acm-china-install-guide/) — MT7612U, 최고의 VIF 지원
- [AWUS036ACS China Install Guide](/ko/blog/awus036acs-china-install-guide/)
- [AWUS036AX China Install Guide](/ko/blog/awus036ax-china-install-guide/)
- [AWUS036AXER China Install Guide](/ko/blog/awus036axer-china-install-guide/)
- [AWUS036AXM China Install Guide](/ko/blog/awus036axm-china-install-guide/)
- [AWUS036AXML China Install Guide](/ko/blog/awus036axml-china-install-guide/)
- [AWUS036EAC China Install Guide](/ko/blog/awus036eacs-china-install-guide/)

궁금한 점이 있으신가요? 아래에 댓글을 남기거나 [yupitek.com](https://yupitek.com/ko/contact/)으로 문의하십시오.

## 참고 문헌

1. [aircrack-ng 공식 문서](https://www.aircrack-ng.org/)
2. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
3. [Kali Linux 공식 문서](https://www.kali.org/docs/)
4. [GitHub: morrownr/8812au-20210820](https://github.com/morrownr/8812au-20210820)
5. [Realtek RTL8812AU 드라이버](https://www.realtek.com/)
