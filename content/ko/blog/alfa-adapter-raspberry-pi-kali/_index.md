---
title: "Kali Linux가 설치된 Raspberry Pi에서 ALFA WiFi 어댑터 사용하기: 설정 가이드"
description: "Kali Linux ARM64가 실행되는 Raspberry Pi에 ALFA USB WiFi 어댑터를 설치하는 방법. AWUS036ACH RTL8812AU 드라이버 컴파일, 모니터 모드, 휴대용 침투 테스트 설정을 다룹니다."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "침투 테스트에 가장 적합한 Raspberry Pi는 무엇입니까?"
    answer: "Raspberry Pi 5(4 GB 또는 8 GB)가 최선의 선택입니다. Pi 4(4 GB 이상)도 잘 작동합니다. Pi 3B+는 실시간 패킷 캡처에 필요한 속도가 부족합니다."
  - question: "AWUS036ACH는 Raspberry Pi에서 드라이버 컴파일이 필요합니까?"
    answer: "네. RTL8812AU는 메인라인 커널에 포함되어 있지 않습니다. 먼저 Kali DKMS 패키지 realtek-rtl88xxau-dkms를 시도하시기 바랍니다. 실패하면 aircrack-ng GitHub에서 수동으로 컴파일하고 ARM64 플랫폼 플래그를 전환합니다."
  - question: "헤드리스 Pi에서 모니터 모드에 wlan0을 사용할 수 있습니까?"
    answer: "권장하지 않습니다. wlan0은 SSH에 사용되는 Pi 내장 WiFi입니다. airmon-ng check kill을 실행하면 SSH 세션이 끊깁니다. wlan1(ALFA 어댑터)을 사용하고 이더넷 또는 tmux를 통해 연결을 유지하시기 바랍니다."
  - question: "AWUS036AXM은 Raspberry Pi에서 플러그 앤 플레이입니까?"
    answer: "네. MT7921AUN 드라이버는 5.18부터 커널에 내장되어 있으며 Kali ARM64 이미지는 더 최신 커널을 실행합니다. firmware-misc-nonfree 패키지만 설치하면 됩니다."
  - question: "Raspberry Pi에서 AWUS036ACH에 전원을 어떻게 공급합니까?"
    answer: "AWUS036ACH는 약 500mW를 소비합니다. Pi에 직접 연결하면 스로틀링이나 재부팅이 발생할 수 있습니다. 3A 이상의 공식 Pi USB-C 전원 공급 장치와 함께 전원 공급형 USB 3.0 허브를 사용하시기 바랍니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["raspberry-pi", "kali-linux", "alfa-network", "AWUS036ACH", "RTL8812AU", "portable-pentest", "monitor-mode"]
featureimage: "/images/blog/alfa-adapter-raspberry-pi-kali.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

Kali Linux를 실행하는 노트북은 표준 침투 테스트 워크스테이션입니다. 하지만 유일한 선택지는 결코 아닙니다. Raspberry Pi 4 또는 Pi 5를 ALFA USB WiFi 어댑터와 결합하면, 재킷 주머니에 들어가고 USB-C 보조 배터리로 구동되며 대상 환경에 몇 시간 동안 방치해둘 수 있는 컴팩트하고 팬이 없는 수동 냉각 플랫폼이 됩니다. Kali Linux ARM64 이미지는 Offensive Security에서 직접 제공되며 에뮬레이션 없이 Pi 4와 Pi 5에서 네이티브로 실행되어 Aircrack-ng, Kismet, Wireshark, Bettercap 등 표준 Kali 메타패키지 전체 도구를 제공합니다.

{{< tldr >}}
Kali Linux ARM64와 ALFA 어댑터가 적용된 Raspberry Pi 4/5는 주머니 크기의 침투 테스트 플랫폼이 됩니다. AWUS036ACH는 RTL8812AU 드라이버 컴파일이 필요한 반면, AWUS036ACM과 AWUS036AXM은 커널 내장 드라이버로 플러그 앤 플레이입니다. 전원 공급형 USB 허브가 필요합니다.
{{< /tldr >}}




가장 큰 걸림돌은 드라이버입니다. AWUS036ACH 내부의 RTL8812AU 칩셋은 메인라인 커널에 포함되어 있지 않으며, 이는 어댑터를 연결하기만 하면 작동할 것으로 기대할 수 없다는 뜻입니다. 실행 중인 ARM64 커널에 맞춰 드라이버를 컴파일해야 하며, 컴파일 플래그는 x86-64와 다릅니다. 본 가이드는 모든 단계를 안내합니다.

---

## 권장 하드웨어

Pi 모델, 어댑터, 전원 공급 장치의 모든 조합이 안정적으로 작동하는 것은 아닙니다. 아래 표는 잘 작동하는 것으로 알려진 구성과 예상되는 절충점을 나타냅니다.

| 구성 요소 | 권장 | 비고 |
|---|---|---|
| 싱글 보드 컴퓨터 | Raspberry Pi 5(4 GB 또는 8 GB) | Pi 4(4 GB 이상)도 잘 작동, Pi 3B+는 실시간 캡처에 너무 느림 |
| 주력 어댑터 | ALFA AWUS036ACH | RTL8812AU 칩셋, 최상의 ARM 드라이버 지원, 듀얼 밴드 AC1200 |
| 대체 어댑터 | ALFA AWUS036ACM | MT7612U 칩셋, 커널 내장 드라이버(mt76x2u), Kali ARM64에서 플러그 앤 플레이 |
| WiFi 6 어댑터 | ALFA AWUS036AXM 또는 AXML | MT7921AUN 칩셋, 5.18부터 커널 네이티브, firmware-misc-nonfree 필요 |
| USB 허브 | 전원 공급형 USB 3.0 허브 | AWUS036ACH는 ~500 mW 소비, 허브 없이는 Pi USB 포트가 전압 강하 발생 가능 |
| 저장 장치 | MicroSD 32 GB 이상(Class 10 / A2) | A2 등급 카드는 눈에 띄게 빠른 부팅 및 apt 작업 제공 |
| 전원 공급 장치 | 공식 Pi USB-C PSU(≥ 3 A) | 서드파티 어댑터는 안정성 문제의 흔한 원인 |

{{< alert "triangle-exclamation" >}}
AWUS036ACH는 고전류 USB 장치입니다. 전원 공급형 USB 허브 없이 Raspberry Pi 4 또는 Pi 5에 직접 연결하면 부하 시 Pi가 스로틀링되거나 재시작될 수 있습니다. 다른 USB 주변기기와 함께 AWUS036ACH를 실행할 때는 항상 전원 공급형 허브를 사용하시기 바랍니다.
{{< /alert >}}

---

## Raspberry Pi에 Kali Linux ARM64 설치하기

### ARM 이미지 다운로드

Kali Linux는 Raspberry Pi용 퍼스트파티 ARM64 이미지를 [https://www.kali.org/get-kali/#kali-arm](https://www.kali.org/get-kali/#kali-arm)에서 관리합니다. <strong>Raspberry Pi 4 (64-bit)</strong> 또는 <strong>Raspberry Pi 5 (64-bit)</strong>로 표시된 이미지를 다운로드합니다. 32비트 이미지를 사용하지 마십시오. 본 가이드의 드라이버 빌드 단계에는 ARM64 커널이 필요합니다.

### MicroSD에 플래싱

Raspberry Pi Imager GUI 도구 또는 명령줄의 `dd`로 플래싱할 수 있습니다:

```bash
# /dev/sdX를 실제 SD 카드 장치로 교체 (lsblk로 확인)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Raspberry Pi Imager에서는 <strong>Use custom</strong> 선택 → Kali `.img.xz` 파일 선택 → SD 카드 선택 → 쓰기를 진행합니다.

### 첫 부팅 및 초기 설정

SD 카드를 삽입하고 모니터와 키보드를 연결(또는 시리얼 콘솔로 헤드리스 접근을 먼저 설정)한 후 전원을 켭니다. 기본 자격 증명은 다음과 같습니다:

- <strong>사용자명:</strong> `kali`
- <strong>비밀번호:</strong> `kali`

로그인 후 `kali-tweaks`를 실행하고 프롬프트에 따라 기본 구성을 강화합니다. 그런 다음 드라이버를 건드리기 전에 시스템을 완전히 업데이트합니다:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

{{< alert "circle-info" >}}
키보드와 모니터가 아닌 SSH로 Pi에 접근할 계획이라면, 첫 부팅 전에 SD 카드의 `/boot` 파티션에 `ssh`라는 빈 파일을 넣어 SSH를 활성화합니다. 이는 표준 Raspberry Pi OS와 동일한 메커니즘입니다.
{{< /alert >}}

---

## Kali ARM64에 RTL8812AU 드라이버 설치하기(AWUS036ACH)

RTL8812AU 드라이버는 메인라인 Linux 커널에 포함되어 있지 않습니다. ARM64에서는 소스에서 컴파일하거나 Kali 패키지 DKMS 버전을 설치해야 합니다. 두 방법 모두 아래에서 다룹니다. 패키지 방식으로 시작하고, 커널 버전 불일치가 발생하는 경우에만 수동 빌드로 전환하시기 바랍니다.

### 옵션 1: Kali 패키지(권장 시작점)

Kali Linux는 커널이 업데이트될 때마다 재컴파일을 자동으로 처리하는 DKMS 패키지 버전의 RTL8812AU 드라이버를 제공합니다.

```bash
sudo apt install realtek-rtl88xxau-dkms
```

설치 후 재부팅하고 모듈이 로드되었는지 확인합니다:

```bash
sudo modprobe 88XXau
ip link show
```

`wlan1` 인터페이스가 보이면(`wlan0`이 Pi의 내장 어댑터라고 가정) 드라이버가 작동하는 것입니다. 이 패키지는 GitHub 소스보다 몇 주 뒤처질 수 있지만 마찰이 가장 적은 시작점입니다.

{{< alert "circle-info" >}}
Kali 패키지는 일반적으로 대부분의 ARM64 설정에 충분합니다. `uname -r`로 확인할 수 있는 현재 커널 버전에 대해 DKMS 패키지가 컴파일에 실패하는 경우에만 아래의 수동 빌드로 진행하시기 바랍니다.
{{< /alert >}}

### 옵션 2: 소스에서 수동 빌드(ARM64)

DKMS 패키지가 실패하는 경우(가장 흔하게는 커널이 패키지의 마지막 테스트 버전보다 최신이기 때문), GitHub의 Aircrack-ng 포크에서 직접 빌드합니다. 이것이 ARM64 지원의 공식 출처입니다.

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)

git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# 플랫폼 플래그를 x86에서 ARM64로 전환
sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/' Makefile
sed -i 's/CONFIG_PLATFORM_ARM64_RPI = n/CONFIG_PLATFORM_ARM64_RPI = y/' Makefile

sudo make dkms_install
```

`sed` 명령은 x86-64 빌드와의 핵심적인 차이입니다. 이것이 없으면 Makefile이 x86 플랫폼 경로를 기본값으로 사용하며 결과 모듈이 ARM64에서 로드되지 않습니다.

성공적으로 빌드한 후 모듈을 로드하고 확인합니다:

```bash
sudo modprobe 88XXau
ip link show
```

새 인터페이스(일반적으로 `wlan1`)가 목록에 보여야 합니다. `ip link show`에 인터페이스가 표시되면 드라이버가 올바르게 작동하는 것입니다.

---

## Raspberry Pi의 MT7921AUN(AWUS036AXM / AXML)

AWUS036AXM 및 AXML 어댑터에 사용되는 MediaTek MT7921AUN 칩셋은 버전 5.18부터 메인라인 커널에 포함되어 있습니다. Kali Linux ARM64 이미지는 그 기준을 훨씬 상회하는 커널을 제공하므로, 어댑터를 연결하면 드라이버가 자동으로 로드됩니다. 컴파일이 필요 없습니다.

유일한 추가 단계는 MT7921AUN에 필요한 비공개 소스 펌웨어 블롭을 설치하는 것입니다:

```bash
sudo apt install firmware-misc-nonfree
sudo reboot
```

재부팅 후 어댑터가 감지되고 인터페이스가 활성화되었는지 확인합니다:

```bash
lsusb
sudo modprobe mt7921u
ip link show
```

`lsusb`에 MediaTek 장치가 표시되고 `ip link show`에 새 무선 인터페이스가 나열되면 어댑터가 준비된 것입니다. MT7921AUN의 모니터 모드 지원은 커널 5.18 이후 크게 개선되었지만, 특정 패킷 인젝션 테스트의 경우 RTL8812AU 기반 어댑터보다 덜 안정적일 수 있습니다. 구형 침투 테스트 워크플로와의 최대 호환성을 위해서는 AWUS036ACH가 여전히 더 강력한 선택입니다. 다만 인젝션은 커널 버전에 따라 다릅니다. kernel 6.16 이전에서는 인젝션이 동작한다는 커뮤니티 보고가 있지만, stock kernel 6.16 이상(6.17에서 실측)에서는 AXML의 패킷 인젝션 테스트(`aireplay-ng --test`: Found 0 APs / No Answer)가 실패하여 deauth 및 핸드셰이크 캡처가 불가능합니다. 원인은 칩 자체의 한계가 아니라 mac80211 chanctx 회귀이며, 커뮤니티 patched 드라이버로 인젝션이 동작하더라도 펌웨어가 전송 속도를 고정합니다(1/6 Mbps, HT/VHT 인젝션 불가). 모니터 모드, AP, WPA3는 영향이 없습니다. 인젝션이 필요하면 AWUS036ACH 또는 AWUS036EACS를 선택하세요.

---

## Raspberry Pi에서 모니터 모드 활성화하기

Raspberry Pi에는 내장 WiFi 인터페이스(`wlan0`)가 있습니다. SSH 접근을 위해 네트워크에 연결된 상태로 유지하시기 바랍니다. ALFA 어댑터(`wlan1`)는 모니터 모드와 패킷 캡처 전용으로 사용합니다. 헤드리스 Pi에서는 절대 `wlan0`을 모니터 모드로 전환하지 마십시오. SSH 연결을 잃게 됩니다.

```bash
# 모니터 모드와 충돌하는 프로세스 종료 (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# ALFA 어댑터 인터페이스에서 모니터 모드 활성화
sudo airmon-ng start wlan1

# 모니터 모드가 활성 상태인지 확인
sudo iwconfig wlan1mon

# 모든 채널에서 캡처 시작
sudo airodump-ng wlan1mon
```

{{< alert "circle-info" >}}
`airmon-ng start wlan1`은 `wlan1mon`이라는 새 인터페이스를 생성합니다. 이후 도구는 항상 `wlan1`이 아닌 `wlan1mon`에 대해 실행하시기 바랍니다. `iwconfig` 또는 `ip link show`로 인터페이스 이름을 확인할 수 있습니다.
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
`airmon-ng check kill`을 실행하면 NetworkManager와 wpa_supplicant가 중지됩니다. `wlan0`을 통해 SSH로 연결되어 있다면 이로 인해 SSH 세션도 끊깁니다. 헤드리스 설정의 경우 이 명령을 실행하기 전에 이더넷이나 두 번째 유선 인터페이스를 통해 연결하거나, 연결이 끊겨도 세션이 유지되도록 `tmux`를 사용하시기 바랍니다.
{{< /alert >}}

모니터 모드를 비활성화하고 관리 모드를 복원하려면:

```bash
sudo airmon-ng stop wlan1mon
sudo systemctl start NetworkManager
```

---

## 휴대용 침투 테스트 설정 팁

하드웨어를 작동시키는 것은 작업의 절반에 불과합니다. 다음의 실용적인 선택이 안정적인 현장 키트와 답답한 케이블 더미의 차이를 만듭니다.

<strong>네트워크 아키텍처:</strong> 관리 연결을 유지하기 위해 `wlan0`(Pi의 내장 WiFi)을 사용합니다. 동일한 LAN이나 핫스팟에 있는 노트북에서 Pi로 SSH 접속합니다. `wlan1`(ALFA 어댑터)은 전적으로 침투 테스트 활동에 할당합니다. 절대 두 역할을 혼용하지 마십시오.

<strong>헤드리스 운영:</strong> 현장에서 키보드, 마우스, 모니터를 연결하지 마십시오. 첫 부팅 시 SSH를 구성하고 노트북의 터미널 에뮬레이터를 통해 모든 것에 접근합니다. `tmux` 세션은 재연결 시에도 유지되며, 이는 네트워크 상태가 불안정할 때 매우 유용합니다.

<strong>전원:</strong> 최소 3 A 등급의 공식 Raspberry Pi USB-C 전원 공급 장치를 사용합니다. AWUS036ACH의 경우 2.5 A 이상 등급의 전원 공급형 USB 허브를 추가합니다. 고품질 USB-C 보조 배터리(65 W 이상)는 부하에 따라 4~6시간 동안 Pi, 허브, 어댑터를 동시에 구동할 수 있습니다.

<strong>저장 장치:</strong> Kismet 로그와 캡처 파일은 MicroSD 카드가 아닌 USB SSD에 기록합니다. MicroSD 카드는 쓰기 주기가 제한적이며 지속적인 로깅 워크로드에서 빠르게 성능이 저하됩니다. 전원 공급형 허브에 연결된 USB 3.0 SSD가 더 빠르고 내구성이 좋습니다.

<strong>인클로저:</strong> 전원 공급형 허브를 수용할 수 있는 개방형 USB 포트나 절개부가 있는 Pi 케이스를 선택합니다. 수동 방열 핀이 있는 알루미늄 케이스는 지속적인 캡처 중 발열 관리에 도움이 됩니다.

---

## Raspberry Pi에서 Kismet 실행하기

Kismet은 백그라운드 서버로 실행되며 브라우저 기반 웹 UI를 제공하는 수동 WiFi 스캐너입니다. 헤드리스 Pi 배포에 매우 적합합니다. Pi를 실행 상태로 두고 동일한 네트워크의 어떤 기기에서든 웹 인터페이스를 확인할 수 있습니다.

```bash
sudo apt install kismet

# 모니터 모드에서 ALFA 어댑터를 사용하여 Kismet 실행
kismet -c wlan1
```

{{< alert "circle-info" >}}
인터페이스 이름을 직접 전달하면 Kismet이 스스로 인터페이스를 모니터 모드로 전환합니다. Kismet을 실행하기 전에 `airmon-ng start`를 실행할 필요가 없습니다. Kismet이 인터페이스 수명 주기를 내부적으로 관리합니다.
{{< /alert >}}

실행되면 네트워크의 모든 브라우저에서 Kismet 웹 UI에 접근합니다:

```
http://raspberrypi.local:2501
```

첫 실행 시 Kismet이 관리자 사용자명과 비밀번호 생성을 요청합니다. 로그인 후 감지된 네트워크, 연결된 클라이언트, 신호 강도 이력, 그리고 GPS 동글이 연결된 경우 GPS 데이터를 볼 수 있습니다.

Kismet은 기본적으로 모든 것을 `~/.kismet/`의 `.kismet` 데이터베이스 파일에 기록합니다. 이는 나중에 분석을 위해 내보내거나 WiGLE에 업로드할 수 있습니다.

---

## 사용 사례: 워드라이빙 설정

ALFA 어댑터와 GPS 동글을 사용하여 Kismet을 실행하는 Raspberry Pi는 완전한 독립형 워드라이빙 키트입니다. 전용 워드라이빙 장비보다 작고 저렴합니다.

<strong>필수 구성 요소:</strong>
- Raspberry Pi 4 또는 Pi 5
- ALFA AWUS036ACH
- USB GPS 동글(u-blox 칩셋이 Kismet과 잘 작동)
- 전원 공급형 USB 허브
- USB-C 보조 배터리(65 W 이상, 패스스루 충전 지원)

<strong>설정 단계:</strong>

1. Kismet과 GPS 패키지 설치:

```bash
sudo apt install kismet gpsd gpsd-clients
```

2. GPS 동글에서 읽도록 `gpsd` 구성:

```bash
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
```

3. GPS 지원으로 Kismet 시작:

```bash
kismet -c wlan1 --gps=gpsd:host=localhost,port=2947
```

4. Pi, 허브, 어댑터, 보조 배터리를 가방이나 인클로저에 장착하고 차량에 둡니다. 휴대폰 핫스팟이나 Pi와 동일한 WiFi 네트워크에 연결된 태블릿에서 Kismet 웹 UI에 접근합니다.

Kismet 로그는 감지된 모든 네트워크에 대해 GPS 좌표를 캡처합니다. `kismetdb_to_wigle`(Kismet에 포함)을 사용하여 `.kismet` 데이터베이스를 WiGLE CSV 형식으로 내보내고 매핑을 위해 WiGLE에 업로드합니다.

{{< alert "triangle-exclamation" >}}
네트워크 스캔 활동을 수행하기 전에 항상 현지 법률을 준수하시기 바랍니다. 많은 관할권에서 수동 스캔만 하는 워드라이빙은 합법이지만, 허가 없이 네트워크에 능동적으로 프로빙하거나 연결하는 것은 불법입니다. 현지 규정을 숙지하시기 바랍니다.
{{< /alert >}}

---

{{< faq >}}

## 더 읽어보기

데스크톱 Kali Linux 및 Ubuntu에서의 전체 RTL8812AU 드라이버 설치 가이드는 [Kali Linux 및 Ubuntu에서 ALFA 드라이버 설치하기](/ko/blog/install-alfa-driver-kali-ubuntu/) 가이드를 참조하시기 바랍니다. 어떤 어댑터를 구매할지 아직 고민 중이라면, [ALFA WiFi 어댑터 구매 가이드 2026](/ko/blog/alfa-wifi-adapter-buyer-guide-2026/)에서 칩셋 세부 정보와 사용 사례별 권장 사항과 함께 모든 현행 모델을 다룹니다.

## 참고 자료

1. [Kali Linux ARM 공식 다운로드](https://www.kali.org/get-kali/#kali-arm)
2. [aircrack-ng rtl8812au 드라이버 프로젝트](https://github.com/aircrack-ng/rtl8812au)
3. [Raspberry Pi 공식 웹사이트](https://www.raspberrypi.com/)
4. [Linux 커널 mt76 드라이버 문서](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
5. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
