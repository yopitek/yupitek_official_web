---
title: "ALFA AWUS036ACH와 wfb-ng로 만드는 DIY 장거리 디지털 FPV 및 텔레메트리 링크 (2026)"
description: "ALFA AWUS036ACH 어댑터와 오픈소스 wfb-ng를 사용하여 저지연, 암호화된 장거리 디지털 영상 및 MAVLink 텔레메트리 링크를 구축합니다. 전체 하드웨어 목록, 라즈베리 파이 설정 가이드, 전원 공급 문제 해결 방법을 다룹니다."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "AWUS036ACH", "wfb-ng", "RTL8812AU", "drone-video-link", "digital-FPV", "FPV", "monitor-mode", "packet-injection", "MAVLink", "Raspberry-Pi", "long-range-video", "telemetry-link"]
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "wfb-ng는 일반 WiFi와 무엇이 다릅니까?"
    answer: "일반 WiFi는 연결(association) 핸드셰이크와 ACK 확인이 필요하여 장거리에서는 성능이 좋지 않습니다. wfb-ng는 FEC 순방향 오류 정정과 함께 원시 패킷 인젝션을 사용하여 802.11 연결 오버헤드를 우회하므로, 종단 간 지연 시간을 수십 밀리초 수준으로 유지합니다."
  - question: "기체에 탑재하는 ALFA 어댑터에 별도의 전원 공급이 필요한 이유는 무엇입니까?"
    answer: "AWUS036ACH는 TX 버스트 동안 상당한 전류를 소모합니다. 라즈베리 파이의 USB 2.0 포트에 직접 연결하면 전압 강하로 인해 어댑터가 리셋되거나, 링크가 끊어지거나, 패킷이 손상됩니다. 전용 5V BEC를 사용하고, 필터링을 위해 +5V와 GND 사이에 470µF 저ESR 커패시터를 추가하십시오."
  - question: "연결은 되는데 영상이나 텔레메트리가 나오지 않습니다. 어떻게 해야 합니까?"
    answer: "가장 흔한 원인은 키 불일치입니다. 기체의 drone.key가 지상국의 gs.key와 일치하는지 확인하십시오. 또한 wifi_channel과 link_domain이 양쪽에서 동일한지도 확인하십시오. journalctl -xu wifibroadcast@gs를 실행하여 실시간 로그를 점검하십시오."
  - question: "wfb-ng에 반드시 ALFA AWUS036ACH를 사용해야 합니까?"
    answer: "이론적으로 RTL8812AU 기반 어댑터라면 모두 작동해야 하지만, AWUS036ACH는 wfb-ng 프로젝트가 공식적으로 테스트하는 하드웨어입니다. 드라이버 지원이 가장 안정적이며, 특히 ALFA의 전원 설계와 탈착식 안테나가 뚜렷한 이점을 제공하는 고출력 장거리 시나리오에서 그렇습니다."
---
> 작성자: Yopitek 기술팀 (대만 ALFA Network 공식 유통업체)
> 대상 독자: 드론 애호가, 메이커, 보안 연구원, 농업 방제 및 점검용 UAV 개발자
> 난이도: ★★★☆☆ (기본적인 Linux 및 비행 컨트롤러 지식 필요)

{{< tldr >}}
wfb-ng는 <strong>ALFA AWUS036ACH</strong>와 같이 모니터 모드를 지원하는 WiFi 어댑터를 드론 전용 장거리 무전기로 바꿔 주는 오픈소스 프로젝트입니다. 시중에서 구할 수 있는 하드웨어만으로 저지연, 암호화된 영상 및 MAVLink 텔레메트리 링크를 구축할 수 있습니다.
{{< /tldr >}}

---

## 1. 왜 ALFA 카드로 디지털 FPV 링크를 구축해야 합니까?

아날로그 FPV(5.8 GHz 아날로그 영상)를 사용해 보셨다면 상황을 잘 아실 것입니다. 신호가 가려지면 화면이 눈발로 뒤덮이고, 거리가 급격히 줄어들며, <strong>수신기만 있으면 누구나 여러분의 영상을 볼 수 있습니다</strong>. 암호화도 없고 텔레메트리 복귀 채널도 없습니다.

지난 1년 동안 저희 팀은 농업 방제 사업자, 점검팀, 보안 교육 고객을 위해 링크를 구축해 왔습니다. 계속 반복된 질문이 하나 있었습니다. <strong>흔한 ALFA USB 어댑터와 오픈소스 소프트웨어로, 영상과 텔레메트리를 모두 전송하는 디지털 암호화 장거리 링크를 만들 수 있습니까?</strong>

답은 "그렇다"이며, 생각보다 훨씬 간단합니다.

기존 아날로그 FPV와 비교하면, ALFA 어댑터에서 오픈소스 <strong>wfb-ng</strong>를 실행하는 방식에는 몇 가지 결정적인 장점이 있습니다.

- <strong>저지연</strong>: 원시 WiFi 인젝션은 802.11 ACK와 핸드셰이크 오버헤드를 우회합니다. 종단 간 지연이 수십 밀리초로 줄어들어 FPV 체감이 아날로그에 가깝습니다.
- <strong>디지털 암호화</strong>: 영상 및 텔레메트리 패킷에 libsodium 암호화를 사용합니다. 누군가 신호를 포착하더라도 영상이나 비행 데이터를 해독할 수 없습니다.
- <strong>하나의 링크, 여러 스트림</strong>: 하나의 주파수에서 어댑터 하나가 다음을 모두 처리합니다.
  - 실시간 영상 (RTP / RTSP)
  - MAVLink 텔레메트리 (양방향, 비행 컨트롤러 ↔ 지상국)
  - TCP/IP 터널 (VPN, SSH 또는 파일 전송용)
- <strong>TX 다이버시티</strong>: 여러 어댑터가 협력하여 송신 다이버시티를 구현함으로써 장애물에 대한 내성을 높일 수 있습니다.
- <strong>오픈소스, 완전한 커스터마이징</strong>: ALFA AWUS036ACH와 wfb-ng를 조합하면 상용 디지털 FPV 시스템(DJI O3, Walksnail 등)의 일부 비용만으로 구축할 수 있으며, 모든 코드가 공개되어 있습니다.

{{< alert "circle-info" >}}
이 가이드는 DJI 기본 FPV 시스템을 대체하려는 것이 아닙니다. <strong>자신만의 링크를 소유하거나, 보조 이중화를 구축하거나, 맞춤형 페이로드를 만들고자</strong> 하는 분들을 위한 실용적인 오픈소스 경로입니다.
{{< /alert >}}

---

## 2. 정체: wfb-ng 설명

<strong>wfb-ng</strong>(Wireless Fibre / WiFi Broadcast – next generation)는 핵심 아이디어가 영리한 오픈소스 디지털 FPV 및 텔레메트리 프로젝트입니다.

> WiFi를 "네트워크"로 사용하지 않고 "무전기"로 사용합니다.

표준 802.11은 근거리 네트워크, 즉 연결, ACK, 재전송을 위해 설계되었습니다. 장거리, 이동체, 약한 신호 환경에서는 이러한 오버헤드가 오히려 부담이 됩니다. wfb-ng는 <strong>원시 WiFi 인젝션</strong>이라는 다른 접근 방식을 취합니다.

- 어댑터가 <strong>모니터 모드</strong>로 들어가며, 어떤 대상에도 "연결"되지 않습니다.
- 원시 WiFi 프레임을 직접 인젝션합니다. <strong>ACK도 재전송도 없으며</strong>(패킷 손실은 FEC 순방향 오류 정정이 처리합니다).
- 이를 통해 표준 802.11의 거리 및 지연 한계를 우회하여, 거리와 안정성을 하드웨어의 물리적 한계까지 끌어올립니다.

쉽게 말해, 흔한 USB 어댑터를 RTP 영상, MAVLink 텔레메트리, 심지어 IP 터널까지 전송할 수 있는 한 쌍의 "디지털 무전기"로 바꾸는 것입니다.

- 프로젝트 홈페이지 (GitHub): https://github.com/svpcom/wfb-ng.git
- PX4 / ArduPilot 생태계에서 DIY 디지털 FPV용으로 널리 사용됩니다. 커뮤니티가 활발하며, 우크라이나 드론 커뮤니티에서 흔히 쓰이는 오픈소스 링크입니다.

---

## 3. 주인공: ALFA AWUS036ACH

이 링크의 "무전기"는 <strong>ALFA AWUS036ACH</strong>입니다.

<strong>Realtek RTL8812AU</strong> 칩셋을 사용하며, <strong>802.11ac(WiFi 5)</strong>, <strong>2.4 GHz / 5 GHz 듀얼 밴드</strong>, USB 3.0 Type-C, 탈착식 RP-SMA 안테나를 갖추고 있습니다. 무엇보다 중요한 점은 <strong>wfb-ng의 공식 테스트 하드웨어가 양쪽 모두 5 GHz에서 AWUS036ACH를 사용한다</strong>는 것입니다. 이 어댑터는 프로젝트 작성자가 가장 안정적인 드라이버 지원을 확인한 모델입니다.

돋보이는 이유는 세 가지입니다.

1. <strong>충분한 출력</strong>: ALFA 특유의 고출력 설계와 외장 고이득 안테나를 결합하면 어떤 노트북 내장 카드보다도 훨씬 뛰어난 장거리 성능을 제공합니다.
2. <strong>모니터 모드 + 인젝션</strong>: 패치된 드라이버(아래에서 자세히 설명)를 사용하면 RTL8812AU가 모니터 모드와 원시 패킷 인젝션을 안정적으로 지원하며, 이는 wfb-ng의 전제 조건입니다.
3. <strong>범용성과 내구성</strong>: USB 폼팩터라서 기체와 지상국 양쪽에서 모두 작동합니다. 기기마다 다른 어댑터를 구매할 필요가 없으며, 하나가 고장 나면 다른 것으로 교체하면 됩니다.

{{< alert "triangle-exclamation" >}}
<strong>참고</strong>: wfb-ng에는 <strong>패치된 드라이버</strong>(예: `rtl88xxau_wfb`)가 필요합니다. 기본 Linux 커널 드라이버로는 wfb-ng가 필요로 하는 인젝션 모드로 들어갈 수 없습니다. 설치 방법은 아래의 소프트웨어 목록 및 단계별 설정 섹션에서 다룹니다.
{{< /alert >}}

---

## 4. 하드웨어 목록

링크는 <strong>드론(기체)</strong>과 <strong>지상국</strong> 두 부분으로 나뉩니다.

### 드론 (기체)

| 항목 | 권장 모델 / 참고 사항 |
|---|---|
| 탑재 컴퓨터 | Raspberry Pi 3B / 3B+ / Zero 2 W / 4 (1080p에는 <strong>Pi 4 또는 Zero 2 W</strong> 사용) |
| 카메라 | Raspberry Pi Camera (CSI) 또는 Logitech C920 (USB) |
| WiFi 어댑터 | <strong>ALFA AWUS036ACH</strong> (또는 RTL8812AU 기반의 다른 어댑터) |
| 전원 공급 | <strong>5V BEC</strong> (어댑터 전용 전원 - 문제 해결 참고 사항 참조) |
| 필터 커패시터 | <strong>470µF 저ESR 커패시터</strong> (어댑터의 +5V와 GND 사이) |
| 비행 컨트롤러 | Pixhawk 또는 유사 제품 (탑재 컴퓨터와 UART를 통한 MAVLink) |

### 지상국

| 항목 | 권장 모델 / 참고 사항 |
|---|---|
| 컴퓨터 | Linux 머신 (Ubuntu / Debian x86-64) 또는 또 다른 Raspberry Pi |
| WiFi 어댑터 | <strong>ALFA AWUS036ACH</strong> |
| 모니터링 소프트웨어 | <strong>QGroundControl</strong>을 실행하는 머신 (지상국 컴퓨터와 동일해도 됩니다) |

> 참고: <strong>수신 전용(RX)</strong> 구성에서는 모니터 모드를 지원하는 어떤 어댑터든 사용할 수 있으며, OpenWRT를 설치한 라우터도 가능합니다. 그러나 공식 테스트 구성과 이 가이드는 AWUS036ACH를 사용합니다.

---

## 5. 소프트웨어 목록

### 운영체제

- <strong>Raspberry Pi OS</strong> / <strong>Debian</strong> / <strong>Ubuntu</strong> (Linux 커널 ≥ 4.x)

### 핵심 프로젝트

- <strong>wfb-ng</strong> (svpcom/wfb-ng): 디지털 FPV / 텔레메트리 메인 프로그램
- <strong>패치된 드라이버</strong>:
  - RTL8812AU → `svpcom/rtl8812au` (브랜치 <strong>v5.2.20</strong>, dkms로 설치)
  - RTL8812EU → `svpcom/rtl8812eu`
  - 로드 후 어댑터는 `rtl88xxau_wfb`(또는 `rtl8812eu`)로 표시됩니다

### 시스템 의존성

```bash
sudo apt update
sudo apt install -y \
  python3-all libpcap-dev libsodium-dev libevent-dev \
  python3-pip python3-pyroute2 python3-twisted python3-serial \
  python3-all-dev python3-venv iw socat debhelper dh-python \
  fakeroot build-essential python3-msgpack python3-setuptools \
  libgstrtspserver-1.0-dev
```

### 암호화

- <strong>libsodium</strong>: `wfb_keygen`을 사용하여 `drone.key`(기체)와 `gs.key`(지상국)를 생성합니다

### 지상국 재생

- <strong>QGroundControl</strong>: 비행 컨트롤러 상태 및 텔레메트리 모니터링
- <strong>GStreamer / RTSP</strong>: 기체에서 전송된 실시간 영상 수신 및 재생

---

## 6. GitHub 링크 및 ALFA AWUS036ACH 사양표

### 공식 링크

| 항목 | 링크 |
|---|---|
| wfb-ng 프로젝트 | https://github.com/svpcom/wfb-ng.git |
| 패치된 드라이버 (RTL8812AU) | https://github.com/svpcom/rtl8812au |
| 패치된 드라이버 (RTL8812EU) | https://github.com/svpcom/rtl8812eu |
| ALFA AWUS036ACH 제품 페이지 | https://yupitek.com/ko/products/alfa/awus036ach/ |
| PX4 WFB-ng 튜토리얼 | https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html |

### ALFA AWUS036ACH 사양표

| 사양 | 상세 |
|---|---|
| 칩셋 | Realtek <strong>RTL8812AU</strong> |
| 무선 표준 | 802.11a / b / g / n / <strong>ac (WiFi 5)</strong> |
| 주파수 | <strong>2.4 GHz + 5 GHz</strong> 듀얼 밴드 |
| 인터페이스 | USB 3.0 <strong>Type-C</strong> |
| 안테나 | 탈착식 <strong>RP-SMA</strong> 2개 (2T2R MIMO) |
| 모니터 모드 | 모니터 모드 + 패킷 인젝션 지원 (wfb-ng 패치 드라이버 필요) |
| wfb-ng 드라이버 | `rtl88xxau_wfb` (svpcom/rtl8812au, v5.2.20) |
| 상태 | wfb-ng <strong>공식 테스트 어댑터</strong> (양쪽 5 GHz) |

---

## 7. 단계별 설정

이 섹션은 네 부분으로 구성됩니다. <strong>경로 A(라즈베리 파이 빠른 시작)</strong>가 가장 권장되며, 거의 굽자마자 바로 쓰는 수준입니다. <strong>경로 B</strong>는 x86 Linux 지상국을 수동으로 설치하는 경우입니다. <strong>경로 C와 D</strong>는 키 페어링과 설정을 다루며, 두 경로 모두에서 사용합니다.

### A. 라즈베리 파이 빠른 시작 (권장)

wfb-ng는 사전 빌드된 라즈베리 파이 이미지를 제공합니다. 드론용과 지상국용으로 각각 하나씩 플래시하면 부팅 후 바로 작동합니다.

<strong>1. 이미지 다운로드 및 플래시</strong>

wfb-ng GitHub <strong>Releases</strong> 페이지로 이동하여 최신 `*.img.gz`를 내려받아 압축을 풀고, <strong>두 장</strong>의 SD 카드(드론용 하나, 지상국용 하나)에 플래시합니다.

```bash
# Extract the image (filename varies by release)
gunzip wfb-ng-*.img.gz
# Flash to SD card using Raspberry Pi Imager, dd, or balenaEtcher
```

<strong>2. 어댑터 연결, 부팅 및 SSH 접속</strong>

두 보드 모두에 ALFA AWUS036ACH를 꽂고 전원을 켠 뒤 SSH로 접속합니다(기본 IP와 자격 증명은 아래와 같습니다).

```bash
ssh pi@192.168.0.111
# Password: raspberry
```

<strong>3. 지상국 서비스 활성화</strong>

<strong>지상국 Pi</strong>에서 다음을 실행합니다.

```bash
sudo systemctl enable wifibroadcast@gs
sudo systemctl enable rtsp
sudo systemctl enable fpv-video
sudo systemctl enable osd
sudo reboot
```

<strong>4. 드론 서비스 활성화</strong>

<strong>드론 Pi</strong>에서 다음을 실행합니다.

```bash
sudo systemctl enable wifibroadcast@drone
sudo systemctl enable fpv-camera
sudo reboot
```

<strong>5. 지상국에서 링크 상태 모니터링</strong>

```bash
wfb-cli gs
```

> 연결, 채널, 패킷 손실 정보가 표시되면 링크가 연결된 것입니다. QGroundControl을 열어 텔레메트리와 영상에 접근하십시오.

---

### B. Debian / Ubuntu 지상국 수동 설치

x86-64 Linux 데스크톱이나 노트북을 지상국으로 사용하는 경우 수동으로 설치합니다.

<strong>1. dkms 및 패치된 드라이버 설치</strong>

```bash
git clone -b v5.2.20 https://github.com/svpcom/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh
```

<strong>2. 어댑터가 wfb-ng 드라이버를 사용하는지 확인</strong>

```bash
# Should show wlan0 with MTU 2312
ifconfig

# Driver name should be rtl88xxau_wfb (RTL8812AU) or rtl8812eu (RTL8812EU)
ethtool -i wlan0
```

{{< alert "triangle-exclamation" >}}
`ethtool -i wlan0`에 `rtl88xxau_wfb`가 아니라 일반 `rtl8812au`가 표시된다면 패치된 드라이버가 올바르게 설치되지 않은 것이며, wfb-ng가 인젝션 모드로 들어갈 수 없습니다. dkms 설치 과정에서 오류가 없었는지 다시 확인하십시오.
{{< /alert >}}

<strong>3. 공식 자동 설치 스크립트 실행</strong>

```bash
curl -o install_gs.sh https://raw.githubusercontent.com/svpcom/wfb-ng/refs/heads/master/scripts/install_gs.sh
sudo bash ./install_gs.sh
```

<strong>4. 링크 모니터링</strong>

```bash
wfb-cli gs
```

---

### C. 키 페어링

wfb-ng의 영상과 텔레메트리는 암호화되어 있습니다. 기체와 지상국은 통신하려면 <strong>서로 일치하는 키</strong>를 사용해야 합니다.

```bash
# Generate keys (do this on the drone side, then distribute)
wfb_keygen

# Place drone.key on the drone
# Place gs.key on the ground station
# Both must match — otherwise the link shows "connected" but no data
```

> <strong>경로 B의 자동 설치 스크립트(install_gs.sh)</strong>를 사용했다면 키가 자동으로 생성되고 설정됩니다. 수동 설치의 경우 `drone.key`와 `gs.key`가 같은 쌍에 속하는지 확인하십시오.

---

### D. 핵심 설정 파일: /etc/wifibroadcast.cfg

`/etc/wifibroadcast.cfg`는 wfb-ng의 핵심 설정 파일입니다. 조정이 필요할 가능성이 가장 높은 매개변수는 다음과 같습니다.

```ini
[common]
# Channel 165 = 5825 MHz (5.8 GHz band)
wifi_channel = 165

# Set the country code to 'BO' (Bolivia) to unlock maximum TX power
wifi_region = 'BO'

[drone]
# link_domain MUST be identical on both drone and ground station
link_domain = "my_wfb_link_01"

[drone_mavlink]
# Receive MAVLink from the flight controller UART (set UART to 1500000 baud)
peer = 'serial:ttyS0:1500000'

[drone_video]
peer = 'listen://0.0.0.0:5602'

[gs]
# Same as above — must match the drone
link_domain = "my_wfb_link_01"
```

<strong>가장 흔한 세 가지 함정:</strong>

1. <strong>`wifi_channel`은 양쪽이 일치해야 합니다</strong>: 이 가이드는 165(5825 MHz, 5.8 GHz)를 사용합니다. 드론과 지상국 양쪽에 동일하게 설정하십시오.
2. <strong>`link_domain`은 양쪽이 일치해야 합니다</strong>: 링크 식별자입니다. 값이 다르면 연결되지 않습니다.
3. <strong>비행 컨트롤러 UART 보드레이트는 1500000이어야 합니다</strong>: `peer = 'serial:ttyS0:1500000'`은 비행 컨트롤러 UART가 1500000 baud로 설정되어야 하며, 그렇지 않으면 MAVLink가 작동하지 않습니다.

{{< alert "triangle-exclamation" >}}
<strong>참고</strong>: `wifi_region = 'BO'`는 최대 TX 출력을 해제하지만, <strong>이것이 해당 지역에서 합법이라는 의미는 아닙니다</strong>. 아래의 규제 안내를 확인하십시오.
{{< /alert >}}

---

## 8. 실전 참고 사항 및 흔한 함정

이 섹션은 실제 배포 과정에서 저희가 직접 겪은 문제를 다룹니다. 꼭 읽어 보십시오.

### 함정 1: 어댑터 전원 부족으로 인한 포트 리셋 및 패킷 손실

AWUS036ACH는 <strong>TX 버스트 동안 상당한 전류를 소모</strong>합니다. 라즈베리 파이의 표준 USB 2.0 포트에 연결하면 파이의 USB 전원이 피크 전류를 감당하지 못합니다. 그 결과 <strong>어댑터 포트 리셋, 링크 끊김, 패킷 손상, 영상 정지</strong>가 발생합니다.

해결 방법 (드론 측에서는 필수):

- 어댑터에 <strong>5V BEC에서 직접</strong> 전원을 공급하십시오(파이의 USB가 아닙니다). BEC 출력을 어댑터에 연결합니다.
- TX 전류 스파이크를 흡수하도록 어댑터의 <strong>+5V와 GND 사이에 470µF 저ESR 커패시터</strong>를 추가하십시오.
- 지상국 측에서는 <strong>노트북의 USB 3.0 포트와 정품 USB 3.0 케이블</strong>이면 보통 충분한 전원을 공급하므로 별도의 BEC가 필요 없습니다.

> 이 한 단계가 링크의 안정성을 좌우합니다. 패킷 손실의 원인이 불량한 전원 공급으로 밝혀진 사례를 수없이 보았습니다.

### 함정 2: 암호화 오류 / 연결 안 됨

`wfb-cli gs`에 "connected"가 표시되는데 <strong>영상이나 텔레메트리가 없다면</strong>, 원인은 거의 항상 다음 중 하나입니다.

- <strong>키 불일치</strong>: 드론의 `drone.key`가 지상국의 `gs.key`와 일치하는지 확인하십시오.
- <strong>채널 또는 link_domain 불일치</strong>: 양쪽의 `wifi_channel`과 `link_domain` 설정이 동일해야 합니다.

디버그 명령:

```bash
# Check ground station service logs for encryption / connection errors
journalctl -xu wifibroadcast@gs
```

### 함정 3: 규제 준수 (중요)

이 링크는 전파를 송출합니다. 무선 송신 장치입니다.

- <strong>사용하려는 출력과 주파수에서 이러한 유형의 WiFi 송신을 현지 규정이 허용하는지 확인하십시오.</strong>
- 대만, 중국, EU, 미국은 각각 5.8 GHz ISM 대역의 TX 출력, 사용 가능한 채널, "비연결(non-association)" 송신에 대한 자체 규정을 가지고 있습니다.
- `wifi_region = 'BO'`로 설정하면 하드웨어의 출력 상한이 해제되지만, <strong>그것이 귀하의 국가에서 합법임을 의미하지는 않습니다</strong>. 현지 무선 규정을 준수하도록 채널과 출력을 조정하십시오.
- 허가된 환경(사유 농지, 폐쇄된 시험장, 교육 시설)에서만 사용하십시오. 다른 통신을 방해하지 마십시오.

---

## 9. 결론

ALFA AWUS036ACH 하나와 오픈소스 wfb-ng 프로젝트만으로 다음을 제공하는 링크를 구축했습니다.

- <strong>비용 이점</strong>: 전체 BOM 비용이 어떤 상용 디지털 FPV 솔루션보다 훨씬 낮습니다.
- <strong>오픈소스</strong>: 모든 코드, 모든 드라이버, 모든 설정이 공개되어 있습니다.
- <strong>완전한 커스터마이징</strong>: 채널, 출력, 암호화 키, MAVLink 라우팅 등 모든 것을 직접 제어할 수 있습니다.
- <strong>장거리</strong>: 하나의 링크에서 디지털 영상과 텔레메트리를 전송하며, 5 GHz 현장 테스트 거리는 아날로그를 크게 능가하고, 암호화와 장애물 내성까지 갖추고 있습니다.

농업 방제, 점검, 보안 교육, 또는 디지털 FPV가 내부적으로 실제로 어떻게 작동하는지 이해하고 싶은 분이라면 걸어 볼 만한 길입니다.

저희 팀은 앞으로도 이 블로그에서 ALFA 어댑터 드론 링크 구현 노트를 계속 공유하겠습니다. 설정 중 문제가 생기면 언제든 문의해 주십시오. <strong>직접 만들어 보는 것이 가장 빠른 학습 방법입니다</strong>.

---

{{< faq >}}

---

## 부록: 초보자를 위한 용어집

드론 링크 기술이 처음이시라면, 이 가이드에서 사용한 용어를 쉬운 말로 정리한 아래 표를 참고하십시오.

| 용어 | 쉬운 설명 |
|---|---|
| <strong>FPV</strong> (First Person View) | 드론에서 지상의 화면이나 고글로 전송되는 실시간 카메라 영상으로, 조종석에 앉아 있는 것과 같은 느낌을 줍니다. |
| <strong>디지털 FPV vs 아날로그 FPV</strong> | 아날로그는 옛날 TV와 같습니다. 신호가 약하면 눈발이 생기고 누구나 시청할 수 있습니다. 디지털은 영상을 데이터 패킷으로 인코딩하므로 암호화가 가능하고 간섭에 더 강하지만, 더 복잡한 하드웨어와 설정이 필요합니다. |
| <strong>모니터 모드</strong> | 일반 WiFi 어댑터는 액세스 포인트에만 연결합니다. 모니터 모드는 어댑터가 어떤 대상에도 연결하지 않고 원시 전파 신호를 수신(및 송신)하도록 하며, 이 가이드의 기반이 됩니다. |
| <strong>패킷 인젝션</strong> | 모니터 모드에서는 일반적인 WiFi 연결 절차를 거치지 않고 사용자 지정 무선 프레임을 공중에 직접 주입할 수 있습니다. wfb-ng는 이 메커니즘을 사용하여 영상과 텔레메트리를 전송합니다. |
| <strong>wfb-ng</strong> | WiFi 어댑터를 범용 네트워크 어댑터가 아닌 드론 전용 무선 링크로 용도 변경하는 오픈소스 소프트웨어입니다. 이 가이드의 핵심 소프트웨어입니다. |
| <strong>FEC (순방향 오류 정정)</strong> | 송신기가 여분의 중복 데이터를 함께 보냅니다. 공중에서 일부 패킷이 손실되더라도 수신기가 중복 데이터로부터 원본 데이터를 복원하므로 재전송이 필요 없습니다(길고 빠르게 움직이는 링크에서는 재전송이 너무 느립니다). |
| <strong>MAVLink</strong> | 드론 비행 컨트롤러(Pixhawk 등)가 지상국과 통신할 때 사용하는 범용 프로토콜로, 비행 상태, 명령, 텔레메트리 데이터를 전달합니다. |
| <strong>RTP / RTSP</strong> | 네트워크를 통해 실시간 영상을 스트리밍하는 표준 프로토콜입니다. IP 카메라와 보안 시스템도 같은 종류의 프로토콜을 사용할 가능성이 높습니다. |
| <strong>libsodium 암호화</strong> | 이 가이드에서 영상과 텔레메트리를 암호화하는 데 사용하는 오픈소스 암호화 라이브러리입니다. 페어링된 드론과 지상국만 내용을 해독할 수 있습니다. |
| <strong>TX 다이버시티 (송신 다이버시티)</strong> | 여러 어댑터를 사용하여 동일한 데이터를 동시에 송신하는 방식입니다. 한 어댑터의 신호가 가려지면 다른 어댑터가 보완하므로, 이중화 시스템과 같습니다. |
| <strong>BEC (Battery Eliminator Circuit)</strong> | 드론 배터리 전압을 어댑터가 필요로 하는 5 V로 낮추는 전압 레귤레이터 모듈로, 링크를 끊을 수 있는 전원 강하 없이 높은 전류 스파이크를 처리합니다. |
| <strong>RTL8812AU</strong> | ALFA AWUS036ACH 내부에 있는 Realtek 칩셋입니다. 이 칩이 어댑터의 모니터 모드 및 패킷 인젝션 지원 여부를 결정합니다. |

> 한 문장으로 요약하면, wfb-ng는 ALFA 어댑터를 드론 전용 무선국으로 바꾸어 영상과 비행 데이터가 오픈소스 암호화 링크를 통해 먼 거리를 이동하도록 해 줍니다. 바로 여러분만의 전용 채널입니다.

---

## 참고 자료

- <strong>wfb-ng 프로젝트 (svpcom/wfb-ng)</strong>: https://github.com/svpcom/wfb-ng.git
- <strong>ALFA AWUS036ACH 제품 페이지</strong>: https://yupitek.com/ko/products/alfa/awus036ach/
- <strong>패치된 드라이버 (RTL8812AU)</strong>: https://github.com/svpcom/rtl8812au
- <strong>패치된 드라이버 (RTL8812EU)</strong>: https://github.com/svpcom/rtl8812eu
- <strong>PX4 WFB-ng 튜토리얼</strong>: https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html

---

*이 글은 Yopitek 기술팀(대만 ALFA Network 공식 유통업체)이 wfb-ng 공식 문서와 실제 구현 경험을 바탕으로 작성했습니다. 이 링크를 구축하기 전에 현지 무선 규정을 확인하고 그에 맞게 TX 출력과 주파수를 조정하십시오.*
