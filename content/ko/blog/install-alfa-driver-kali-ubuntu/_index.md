---
title: "Kali Linux & Ubuntu 24.04에서 ALFA USB WiFi 드라이버 설치하는 방법 (2026)"
description: "RTL8812AU, MT7612U, MT7921AUN 칩셋을 위해 Kali Linux 2024와 Ubuntu 24.04에 ALFA Network USB WiFi 어댑터 드라이버를 설치하는 완벽 가이드. 문제 해결 팁 포함."
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "ALFA USB WiFi 어댑터는 Linux에서 드라이버가 필요한가요?"
    answer: "칩셋에 따라 다릅니다. MT7612U와 MT7921AUN은 커널 내장이라 modprobe만 실행하면 됩니다. RTL8812AU는 aircrack-ng GitHub에서 외부 드라이버를 설치해야 합니다."
  - question: "내 ALFA 어댑터가 어떤 칩셋을 사용하는지 어떻게 확인하나요?"
    answer: "어댑터를 꽂고 lsusb를 실행하십시오. USB ID를 대조하십시오: 0bda:8812는 RTL8812AU, 0e8d:7612는 MT7612U, 0e8d:7961은 MT7921AUN입니다."
  - question: "DKMS란 무엇이고 왜 필요한가요?"
    answer: "DKMS는 새 커널이 설치될 때 드라이버 모듈을 자동으로 재컴파일합니다. DKMS 없이는 커널 외부 드라이버가 커널 업데이트마다 작동을 멈춰 수동 재컴파일이 필요합니다."
  - question: "Ubuntu 22.04에서 MT7921AUN 어댑터를 쓸 수 있나요?"
    answer: "기본 커널 5.15는 지원하지 않습니다. HWE 커널 linux-generic-hwe-22.04를 설치해 6.2 이상으로 업그레이드하거나 Ubuntu 24.04 LTS로 업그레이드하십시오."
  - question: "make가 linux/module.h not found를 보고하면 어떻게 해야 하나요?"
    answer: "커널 헤더가 설치되지 않은 것입니다. sudo apt install linux-headers-$(uname -r)을 실행해 현재 커널에 맞는 헤더를 설치한 다음 재컴파일하십시오."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["driver-install", "kali-linux", "ubuntu", "RTL8812AU", "MT7612U", "MT7921AUN", "ALFA-Network"]
featureimage: "/images/blog/install-alfa-driver-kali-ubuntu.webp"
---

Linux에서 USB WiFi 어댑터를 작동시키는 것은 결국 한 가지, 바로 드라이버로 귀결됩니다. 제조사가 드라이버를 실행형 설치 프로그램으로 묶어 제공하는 Windows와 달리, Linux는 커널 모듈을 사용합니다 — 운영체제가 하드웨어와 통신하기 위해 로드하는 컴파일된 코드입니다. 이 모델을 이해하면 문제 해결이 명쾌해지고 드라이버 설치가 예측 가능해집니다.

{{< tldr >}}
ALFA 어댑터 드라이버 설치는 칩셋에 따라 다릅니다. MT7612U와 MT7921AUN은 커널 내장이라 플러그 앤 플레이입니다. RTL8812AU는 aircrack-ng GitHub에서 설치해야 하며, 커널 업데이트를 견디려면 DKMS가 필요합니다.
{{< /tldr >}}




이 가이드는 Kali Linux 2024/2025와 Ubuntu 24.04 LTS 양쪽에서 모든 주요 ALFA Network USB WiFi 어댑터 칩셋의 드라이버 설치를 다룹니다.

---

## Linux에서 USB WiFi 드라이버가 작동하는 방식

### 커널 모듈

Linux WiFi 드라이버는 **커널 모듈**입니다 — 부팅 시 또는 필요 시 실행 중인 커널에 로드되는 `.ko` 파일입니다. USB 디바이스를 꽂으면 커널은 그 USB Vendor ID와 Product ID를 읽고, 데이터베이스에서 일치하는 모듈을 찾아 자동으로 로드합니다.

MediaTek MT7612U 같은 일반적인 칩셋의 경우 이 과정이 투명하게 일어납니다. 어댑터를 꽂으면 모듈이 로드되고 인터페이스가 나타납니다. 더 새롭거나 덜 일반적인 칩셋의 경우에는 커널 내장(in-tree) 모듈이 존재하지 않아 소스에서 직접 컴파일해야 합니다.

### 커널 외부(Out-of-Tree) 드라이버

드라이버가 메인라인 커널에 포함되지 않은 경우("out-of-tree" 또는 "외부" 드라이버라고 함) 다음을 해야 합니다.

1. 드라이버 소스 코드 다운로드
2. 실행 중인 커널의 헤더에 맞춰 컴파일
3. 생성된 `.ko` 파일을 커널 모듈 디렉터리에 설치
4. `modprobe`로 로드

컴파일 단계는 커널 헤더가 설치되어 있고 실행 중인 커널과 정확히 일치해야 합니다. 이것이 드라이버 설치 실패의 가장 흔한 원인입니다.

### DKMS: Dynamic Kernel Module Support

평범한 `make install`은 현재 커널에 맞춰 드라이버를 컴파일합니다. Kali나 Ubuntu가 커널을 업데이트하면 — 이는 정기적으로 일어납니다 — 기존 드라이버는 더 이상 로드되지 않아 재컴파일해야 합니다.

**DKMS**는 드라이버 소스 코드를 시스템 데몬에 등록해, 새 커널이 설치될 때마다 등록된 모듈을 자동으로 재컴파일함으로써 이 문제를 해결합니다. 커널 외부 드라이버가 필요한 모든 어댑터에 권장되는 방식입니다.

---

## 칩셋 식별하기

필요한 드라이버는 어댑터의 마케팅 명칭이 아니라 전적으로 칩셋에 달려 있습니다. 이름은 같지만 하드웨어 리비전이 다른 두 어댑터는 서로 다른 칩셋을 사용할 수 있습니다.

### ALFA 모델 대 칩셋 매핑

| ALFA 모델 | 칩셋 | USB ID | 드라이버 |
|---|---|---|---|
| [AWUS036ACH](/ko/products/alfa/awus036ach/) | RTL8812AU | 0bda:8812 | aircrack-ng/rtl8812au |
| [AWUS036ACM](/ko/products/alfa/awus036acm/) | MT7612U | 0e8d:7612 | mt76x2u (커널 내장) |
| [AWUS036AX](/ko/products/alfa/awus036ax/) | RTL8832BU | 0e8d:885a | OOK 드라이버 (<6.17) |
| [AWUS036AXML](/ko/products/alfa/awus036axml/) | MT7921AUN | 0e8d:7961 | mt7921u (커널 5.18+) |

### lsusb로 어댑터 식별

어댑터를 꽂고 실행합니다.

```bash
lsusb
```

예시 출력:

```
Bus 003 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
Bus 003 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/bgn/ac
```

`ID xx:xx` 값을 위 표와 대조해 칩셋을 확인하십시오.

---

## 시스템 준비

어떤 칩셋을 가지고 있든, 먼저 공통 빌드 사전 요구 사항을 설치합니다.

**Kali Linux:**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r)
```

**Ubuntu 24.04:**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r) \
    linux-headers-generic
```

실행 중인 정확한 커널에 맞는 헤더가 설치되었는지 확인합니다.

```bash
uname -r
# 예시: 6.6.9-amd64

ls /lib/modules/$(uname -r)/build
# 존재해야 함 — 없으면 헤더가 설치되지 않은 것
```

---

## RTL8812AU 드라이버 (AWUS036ACH)

RTL8812AU는 커널 외부 드라이버가 필요합니다. 커뮤니티가 관리하는 두 가지 포크가 있으며, OS에 따라 선택하십시오.

### 옵션 A: aircrack-ng/rtl8812au (Kali Linux — 권장)

이 포크는 Aircrack-ng 팀이 관리하며 명시적인 Kali 호환성과 최적화된 패킷 인젝션 지원을 제공합니다.

```bash
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
make
sudo make install
sudo modprobe 88XXau
```

인터페이스가 나타났는지 확인합니다.

```bash
ip link show | grep wlan
# wlan0 또는 유사한 항목이 표시되어야 함
```

### 옵션 B: morrownr/8812au-20210708 (Ubuntu 24.04 — 권장)

morrownr 포크는 Ubuntu에 최적화되어 있으며 DKMS 통합이 포함된 편리한 설치 스크립트를 제공합니다.

```bash
git clone https://github.com/morrownr/8812au-20210708
cd 8812au-20210708
sudo ./install-driver.sh
```

설치 스크립트가 DKMS 등록을 자동으로 처리합니다. 실행 후:

```bash
# 새 모듈을 로드하기 위해 재부팅
sudo reboot

# 재부팅 후 확인
lsmod | grep 8812au
```

### 수동 DKMS 등록 (두 포크 모두)

수동으로 제어하고 싶다면:

```bash
# 드라이버 클론 (두 포크 중 하나 사용)
git clone https://github.com/aircrack-ng/rtl8812au

# Makefile에서 버전 확인
grep "^MODULE_VERSION" rtl8812au/Makefile
# 버전을 메모 (예: v5.6.4.2 → 5.6.4.2 사용)

# 소스를 DKMS 디렉터리로 복사
sudo cp -r rtl8812au /usr/src/rtl8812au-5.6.4.2

# 등록, 빌드, 설치
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2

# 확인
dkms status
# 예상: rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

### 예상 lsusb 및 lsmod 출력

설치 성공 후:

```bash
lsusb
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU ...

lsmod | grep 88XXau
# 88XXau    3461120  0
```

---

## MT7612U 드라이버 (AWUS036ACM, AWUS036ACX)

MT7612U 칩셋은 드라이버가 버전 **4.19**부터 메인라인 Linux 커널의 일부였기 때문에, 네 가지 중 가장 작동시키기 쉽습니다. Kali Linux 2022+와 Ubuntu 20.04+에서는 드라이버 설치가 전혀 필요 없습니다.

### 커널 버전 확인

```bash
uname -r
```

출력이 4.19 이상이라면(현대적인 Kali나 Ubuntu에서는 항상 그러함) `mt76x2u` 모듈을 사용할 수 있습니다.

### 모듈 로드

```bash
sudo modprobe mt76x2u
```

로드되었는지 확인합니다.

```bash
lsmod | grep mt76x2u
# mt76x2u    86016  0
# mt76x2_common    61440  1 mt76x2u
# mt76_usb    40960  1 mt76x2u
```

무선 인터페이스가 즉시 나타나야 합니다.

```bash
ip link show
# wlan0: ...
```

### 부팅 시 모듈 로드하기

대부분의 시스템에서는 어댑터가 감지되면 모듈이 자동으로 로드됩니다. 부팅 시 확실히 로드되도록 명시적으로 지정하려면:

```bash
echo "mt76x2u" | sudo tee -a /etc/modules
```

### 컴파일 불필요

이것이 MT7612U 칩셋의 큰 장점입니다. 컴파일 제로, 드라이버 소스 불필요, 커널 헤더 의존 없음. 지원되는 모든 배포판에서 기본 상태로 작동합니다. 드라이버 관리의 번거로움을 원치 않는 사용자에게 [AWUS036ACM](/ko/products/alfa/awus036acm/)은 가장 플러그 앤 플레이에 가까운 침투 테스트 어댑터입니다.

---

## MT7921AUN 드라이버 (AWUS036AXM, AWUS036AXML — Wi-Fi 6E)

MT7921AUN은 MediaTek의 Wi-Fi 6E 칩셋입니다. 그 Linux 드라이버 `mt7921u`는 **버전 5.18**에서 메인라인 커널에 병합되었습니다.

### 커널 버전 확인

```bash
uname -r
```

**Kali Linux 2022.2 이후**는 커널 5.18 이상을 탑재합니다 — 지원됨.
**Ubuntu 22.04 LTS**는 커널 5.15를 탑재합니다 — 커널 업그레이드 없이는 **지원 안 됨**.
**Ubuntu 24.04 LTS**는 커널 6.8을 탑재합니다 — 완전히 지원됨.

### 모듈 로드 (커널 5.18+)

```bash
sudo modprobe mt7921u
```

확인합니다.

```bash
lsmod | grep mt7921u
# mt7921u    57344  0
# mt7921_common    196608  1 mt7921u
```

### Ubuntu 22.04: 커널 업그레이드 경로

먼저 현재 실행 중인 커널 버전을 확인합니다(HWE 시스템에서는 실행 중인 커널이 예상과 다를 수 있으므로 중요).

```bash
# 실행 중인 커널 확인
uname -r

# 일치하는 헤더가 설치되어 있는지 확인
dpkg -l | grep "linux-headers-$(uname -r)"
# 출력이 없으면: sudo apt install linux-headers-$(uname -r)
```

커널 5.15의 Ubuntu 22.04를 사용 중이라면 두 가지 옵션이 있습니다.

**옵션 A: HWE 커널** (권장)

```bash
sudo apt install linux-generic-hwe-22.04
sudo reboot
```

Ubuntu 22.04용 HWE(Hardware Enablement) 커널은 6.2+이며 mt7921u를 지원합니다.

**옵션 B: Ubuntu 24.04로 업그레이드**

Ubuntu 24.04 LTS는 커널 6.8과 완전한 mt7921u 지원을 탑재합니다. 이것이 가장 깔끔한 장기적 해법입니다.

### Wi-Fi 6E 및 모니터 모드 상태

2026년 기준으로 mt7921u 드라이버는 2.4 GHz, 5 GHz, 6 GHz 대역에서 관리 모드(네트워크 연결)를 안정적으로 지원합니다. 2.4 및 5 GHz에서의 모니터 모드 지원은 기능합니다. **6 GHz 모니터 모드**는 아직 성숙 중이므로 — 6 GHz 평가에 의존하기 전에 `mt76` 커널 드라이버 이슈 트래커에서 현재 상태를 확인하십시오.

---

---

## DKMS: 커널 업데이트 후에도 드라이버 유지하기

Kali Linux와 Ubuntu 모두 커널을 정기적으로 업데이트합니다. DKMS 없이는 커널 외부 드라이버(RTL8812AU)가 커널 업데이트 후 수동 재컴파일 전까지 작동을 멈춥니다.

DKMS가 올바르게 구성되어 있으면 재컴파일이 `apt upgrade` 중에 자동으로 일어납니다.

### DKMS가 드라이버를 관리하는지 확인

```bash
dkms status
```

드라이버가 올바르게 관리되고 있음을 보여주는 예시 출력:

```
rtl8812au/5.6.4.2, 6.6.9-amd64: installed
8814au/5.8.7.4, 6.6.9-amd64: installed
```

### 커널 업데이트 중 일어나는 일

```
apt upgrade
→ 새 커널 패키지 다운로드
→ DKMS 훅 트리거
→ rtl8812au 소스가 새 커널에 맞춰 재컴파일됨
→ 새 .ko 설치됨
→ 시스템이 새 커널로 재부팅됨
→ 드라이버 자동 로드됨
```

업그레이드 중 DKMS가 실패하면(`dkms status`에 "built"로는 보이지만 "installed"가 아닌 경우로 확인 가능) 수동으로 재설치합니다.

```bash
sudo dkms install rtl8812au/5.6.4.2 -k $(uname -r)
```

---

## 문제 해결

| 증상 | 유력한 원인 | 해결책 |
|---|---|---|
| 꽂은 후 wlan 인터페이스 없음 | 드라이버 미로드 | `sudo modprobe 88XXau` 또는 `sudo modprobe mt76x2u` |
| `modprobe: FATAL: Module not found` | 현재 커널에 맞게 드라이버 미컴파일 | 드라이버 재컴파일 또는 `sudo dkms install` 실행 |
| 인터페이스가 나타났다가 수 초 후 사라짐 | 전력 관리 간섭 | `sudo iwconfig wlan0 power off` |
| `make`가 "linux/module.h not found"로 실패 | 커널 헤더 미설치 | `sudo apt install linux-headers-$(uname -r)` |
| `make`가 버전 불일치로 실패 | 헤더가 실행 커널과 불일치 | `uname -r` vs `ls /lib/modules` — 일치하는 헤더 재설치 |
| lsusb에는 디바이스가 보이나 인터페이스 없음 | 모듈은 로드됐으나 인터페이스 미생성 | `dmesg \| tail -30`에서 오류 확인 |
| 모니터 모드 실패: "Operation not supported" | 드라이버 버전이 모니터 모드 미지원 | 배포판 패키지 드라이버 대신 aircrack-ng 포크 사용 |
| aireplay-ng 인젝션 테스트: 0% | 인터페이스가 모니터 모드 아님 | `iwconfig`로 확인, `airmon-ng start` 재실행 |
| 드라이버는 작동하나 재부팅 후 멈춤 | 모듈이 initramfs에 미추가 | `sudo update-initramfs -u` 또는 DKMS 사용 |
| 커널 업데이트 후 DKMS 빌드 실패 | 새 커널용 헤더 누락 | `sudo apt install linux-headers-$(uname -r)` |

### 상세 진단 명령어

```bash
# 로드된 모든 무선 모듈 확인
lsmod | grep -E "8812|8814|mt76|mt79"

# USB 및 무선 이벤트에 대한 커널 메시지 확인
dmesg | grep -iE "rtl|mt76|mt79|usb 802|wlan"

# 모든 무선 인터페이스 목록
iw dev

# 특정 인터페이스가 사용하는 드라이버 확인
ethtool -i wlan0 | grep driver

# USB 디바이스 상세 정보 확인
lsusb -v -d 0bda:8812 2>/dev/null | grep -E "idVendor|idProduct|iProduct"

# 등록된 모든 모듈의 DKMS 상태 확인
dkms status
```

---

## 빠른 참조: 어떤 어댑터에 어떤 드라이버

| 보유 모델 | 칩셋 | Kali/Ubuntu x86 | Raspberry Pi ARM |
|---|---|---|---|
| [AWUS036ACH](/ko/products/alfa/awus036ach/) | RTL8812AU | `aircrack-ng/rtl8812au` (DKMS) | 수동 DKMS + ARM 헤더 |
| [AWUS036ACM](/ko/products/alfa/awus036acm/) | MT7612U | 내장 (`mt76x2u`) ✅ | 내장 — 플러그 앤 플레이 ✅ |
| [AWUS036AX](/ko/products/alfa/awus036ax/) | RTL8832BU | OOK (<6.17) | 해당 없음 |
| [AWUS036AXML](/ko/products/alfa/awus036axml/) | MT7921AUN | 내장 (`mt7921u`, 커널 5.18+) | `linux-firmware` 패키지 |

---

## 정품 하드웨어 확보하기

드라이버 문제는 때때로 USB ID를 잘못 보고하거나 명시된 모델과 맞지 않는 열등한 칩셋을 사용하는 위조 어댑터에서 비롯됩니다. 공식 총판의 정품 ALFA Network 어댑터는 문서에 기재된 그대로 동작합니다.

Yopitek은 ALFA Network 공식 총판입니다. 정품 하드웨어를 제조사 보증과 예측 가능한 드라이버 호환성과 함께 구매하려면 전체 [ALFA Network 제품군](/ko/products/alfa/)을 둘러보십시오.

---

{{< faq >}}

## 요약

Linux WiFi 드라이버 설치는 간단한 결정 트리를 따릅니다.

1. `lsusb`와 위 매핑 표로 **칩셋을 식별**합니다.
2. **MT7612U 또는 MT7921AUN(커널 5.18+)인가요?** → `modprobe`만 실행하면 끝입니다.
3. **RTL8812AU인가요?** → `aircrack-ng/rtl8812au`를 클론하고 `make && sudo make install`을 실행한 뒤, 지속성을 위해 DKMS를 활성화합니다.
4. **무언가 작동하지 않나요?** → 문제 해결 표를 확인하고, 헤더가 커널과 일치하는지 검증하며, `dmesg`를 확인합니다.

ALFA Network 어댑터의 장점은 네 가지 주요 칩셋 모두 잘 문서화되고 활발히 관리되는 드라이버 해법을 갖고 있다는 점입니다. 지원되지 않는 영역에 갇히는 일이 결코 없습니다.

## 참고 문헌

1. [aircrack-ng 공식 rtl8812au 드라이버](https://github.com/aircrack-ng/rtl8812au)
2. [morrownr USB-WiFi 지식 베이스](https://github.com/morrownr/USB-WiFi)
3. [Kali Linux 공식 문서](https://www.kali.org/docs/)
4. [Ubuntu 공식 HWE 커널 문서](https://wiki.ubuntu.com/Kernel/LTSEnablementStack)
5. [Linux Wireless mt76 드라이버](https://wireless.wiki.kernel.org/en/users/Drivers/mt76)
