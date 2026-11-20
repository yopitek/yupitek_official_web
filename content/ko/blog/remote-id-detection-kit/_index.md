---
title: "ALFA AWUS036ACH × Raspberry Pi: 표준 Remote ID 드론 탐지 키트 완벽 가이드 (2026)"
description: "ALFA AWUS036ACH와 Raspberry Pi로 합법적인 수동형 Remote ID 드론 탐지 키트를 구축합니다. ASTM F3411 표준 분석, 하드웨어 목록, 단계별 설정, 그리고 DJI OcuSync와 표준 RID의 기술적 차이에 대한 설명을 다룹니다."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["Remote-ID", "ALFA-Network", "AWUS036ACH", "drone-detection", "Counter-UAV", "ASTM-F3411", "EN-4709-002", "opendroneid", "unix_rid_capture", "DJI-OcuSync", "Raspberry-Pi"]
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "최신 Wi-Fi 6/6E 어댑터 대신 AWUS036ACH가 첫 번째 선택인 이유는 무엇입니까?"
    answer: "Remote ID 캡처에는 안정적인 모니터 모드와 원시 패킷 인젝션이 필요합니다. 현재 가장 성숙한 커뮤니티 드라이버 브랜치는 Realtek rtl88xxau(RTL8812AU / RTL8814AU)입니다. Wi-Fi 6/6E 칩셋 중 MediaTek MT7921AUN(AWUS036AXM / AXML)은 기본 6.17 커널에서 패킷 인젝션이 실패하며, Realtek RTL8832BU(AWUS036AX / AXER)는 커널 6.17 이상에서 커널 내장 rtw89_8852bu로 인젝션이 가능하지만(GX10 테스트: 2.4 GHz 인젝션 AX 96%, AXER 73%) 이 키트와 함께 검증되지는 않았습니다. AWUS036ACH는 커뮤니티와 이 키트 양쪽에서 이중으로 검증되었습니다."
  - question: "nRF52840은 필수입니까?"
    answer: "Wi-Fi Remote ID(NAN / Beacon)만 필요하다면 필수가 아니며, AWUS036ACH만으로 충분합니다. Bluetooth 5 Long Range 브로드캐스트를 동시에 캡처하려면 nRF52840(스니퍼 펌웨어 플래시 필요)이 필요합니다. 전체 범위를 커버하기 위해 이 모듈을 포함하시기를 권장합니다."
  - question: "이 키트로 DJI 드론을 디코딩할 수 있습니까?"
    answer: "DJI의 표준 Wi-Fi / BT Remote ID 브로드캐스트는 처리할 수 있습니다. 그러나 DJI 고유의 OcuSync DroneID는 표준 프로토콜에 포함되지 않으며, ALFA 어댑터로는 디코딩할 수 없습니다. Kismet 플러그인이 설치된 별도의 SDR(ANTSDR / HackRF)이 필요합니다. 두 가지를 함께 배치할 수 있습니다."
  - question: "어떤 세대의 Raspberry Pi를 사용해야 합니까?"
    answer: "Raspberry Pi 4(2 GB 이상)가 가장 균형이 좋습니다. Pi 3B는 unix_rid_capture 작성자가 테스트에서 검증했습니다. Pi 5도 동작합니다(냉각과 전원에 유의). Pi 내장 WiFi는 모니터 모드로 안정적으로 진입할 수 없으므로, 외장 AWUS036ACH가 필요합니다."
  - question: "수동 수신은 합법입니까?"
    answer: "드론이 공개적으로 브로드캐스트하는 Remote ID 정보를 수신하는 것은 합법이며, 공개된 정보를 읽는 것과 동등합니다. 그러나 능동적인 재밍은 엄격하게 규제되며 이 키트의 범위를 벗어납니다."
---
> Yopitek 기술팀 | 대만 ALFA Network 공식 유통업체

{{< tldr >}}
Remote ID 탐지 키트는 <strong>ALFA AWUS036ACH</strong> 어댑터의 모니터 모드를 사용하여, 드론이 법적으로 브로드캐스트해야 하는 신원 및 위치 정보를 수동적으로 수신합니다. 공역을 위한 "번호판 인식기"라고 생각하시면 됩니다. 현장 보안 관리자에게 합법적이고 저렴한 상황 인식 도구를 제공합니다.
{{< /tldr >}}

---

## 1. Remote ID 탐지 키트가 필요한 이유

전 세계의 드론 규제는 "신원 브로드캐스트" 시대에 접어들었습니다. 표준에 따라 드론은 비행 중 다음 정보를 지속적으로 브로드캐스트해야 합니다.

| 브로드캐스트 필드 | 설명 |
|---|---|
| UAS / 운용자 ID | 일련번호 또는 등록 코드 |
| 현재 위치(위도, 경도, 고도) | WGS-84 / 기압 고도 |
| 속도 및 방향 | 수평 / 수직 속도 |
| 운용자 위치 | 이륙 지점 또는 현재 위치 |

브로드캐스트에는 두 종류의 무선 매체가 사용됩니다.

- <strong>Bluetooth</strong>: BT4 Legacy Advertising, BT5 Long Range (Extended Advertising)
- <strong>Wi-Fi</strong>: NAN (Wi-Fi Aware, 2.4 / 5 GHz), Beacon (2.4 / 5 GHz)

공항, 산업단지, 교도소, 대규모 행사의 현장 관리자에게 <strong>이러한 공개 브로드캐스트를 수동적으로 수신하는 것</strong>(본질적으로 드론의 "기체 번호"를 확인하는 것)은 능동적인 간섭 없이 상황을 인식할 수 있는, 규정을 준수하는 저비용 방법입니다.

{{< alert "triangle-exclamation" >}}
<strong>법적 유의 사항</strong>: 이 가이드에서 설명하는 모든 방법은 <strong>공개적으로 브로드캐스트되는 데이터의 수동 수신</strong>입니다. 능동적인 재밍은 모든 관할 지역에서 엄격하게 규제되며, 이 키트에 포함되지 않고 권장되지도 않습니다.
{{< /alert >}}

---

## 2. 제품 포지셔닝: 위험이 가장 낮은 오픈소스 경로

여러 기술적 접근 방식을 평가한 끝에, <strong>ALFA AWUS036ACH</strong>를 중심으로 한 구성을 선택했습니다.

- AWUS036ACH는 <strong>Realtek RTL8812AU</strong> 칩셋을 사용하며, 듀얼 밴드 2.4 + 5 GHz(802.11ac), 2×2 MIMO, 분리 가능한 5 dBi 고이득 RP-SMA 안테나 2개, 그리고 넉넉한 USB 3.0 대역폭을 갖추고 있습니다.
- 커뮤니티에서 유지보수하는 `rtl88xxau` 드라이버는 안정적인 <strong>모니터 모드</strong>와 <strong>원시 패킷 인젝션</strong>을 제공하며, 이는 Wi-Fi RID Beacon / NAN 프레임을 캡처하기 위한 전제 조건입니다.
- 무엇보다 `sxjack/unix_rid_capture` README는 <strong>"Tested using an rtl8812au based WiFi dongle, an nRF52840 dongle and a Raspberry Pi 3B"</strong>라고 명시하고 있습니다. 커뮤니티가 이미 하드웨어 검증을 해 두었습니다. 제품화된 키트를 위해 이들의 아키텍처를 재현하는 것이 위험이 가장 낮은 경로입니다.

---

## 3. 하드웨어 목록

| 항목 | 모델 / 사양 | 역할 | 요구 사항 |
|---|---|---|---|
| <strong>핵심 어댑터</strong> | ALFA <strong>AWUS036ACH</strong> (RTL8812AU, 듀얼 밴드 2.4/5 GHz, USB 3.0, 5 dBi RP-SMA 안테나 2개) | Wi-Fi Remote ID 캡처(모니터 모드) | <strong>필수</strong> |
| 싱글 보드 컴퓨터 | Raspberry Pi 4 (2 GB 이상 권장; 3B / 5도 동작) | 연산 호스트 | <strong>필수</strong> |
| 스토리지 | microSD 16 GB 이상 (Samsung / SanDisk Endurance 권장) | 시스템 디스크 | <strong>필수</strong> |
| Bluetooth 5 캡처 | <strong>nRF52840</strong> USB 동글 (스니퍼 펌웨어 플래시, 예: Nordic Sniffer) | BT5 Long Range Remote ID 캡처 | 권장 (선택 사항) |
| 전원 | 5 V / 3 A USB-C (공식 Pi 전원 어댑터) | 전원 공급 | <strong>필수</strong> |
| 네트워크 | 이더넷 케이블 또는 WiFi 자격 증명 | 업로드 / 관리 | <strong>필수</strong> |
| 안테나 업그레이드 | ALFA <strong>APA-M25</strong> 지향성 패널 안테나 | 수신 범위 확장, 주변 노이즈 제거 | 선택 사항 |

> 참고: 커뮤니티 `DroneAware` 프로젝트는 원래 <strong>AWUS036N(Ralink RT3070, 2.4 GHz 단일 대역)</strong>을 지정했습니다. 이 키트는 2.4 GHz와 5 GHz <strong>NAN 및 Beacon</strong> Wi-Fi RID 전송 방식을 모두 커버하기 위해 <strong>AWUS036ACH(듀얼 밴드)</strong>로 업그레이드하였으며, 더 넓은 커버리지와 더 나은 미래 대응성을 제공합니다.

---

## 4. 소프트웨어 목록

| 소프트웨어 / 패키지 | 용도 | 출처 |
|---|---|---|
| Raspberry Pi OS Lite (64-bit) | 운영체제 (헤드리스) | raspberrypi.com |
| <strong>rtl88xxau driver</strong> | RTL8812AU 모니터 / 인젝션 드라이버 | [morrownr/8812au-20210629](https://github.com/morrownr/8812au-20210629) |
| `libpcap-dev`, `libbluetooth-dev`, `libncurses-dev` | `unix_rid_capture` 빌드 의존성 | APT |
| <strong>opendroneid-core-c</strong> | Open Drone ID 메시지 인코딩/디코딩 C 라이브러리 (ASTM F3411 / EN 4709-002) | [opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| <strong>unix_rid_capture</strong> | Linux Wi-Fi / BT RID 캡처 프로그램 (JSON 출력) | [sxjack/unix_rid_capture](https://github.com/sxjack/unix_rid_capture) |
| DroneAware Node (선택 사항) | 원클릭 커뮤니티 실시간 지도 연동 | [fduflyer/DroneAware-Node-Releases](https://github.com/fduflyer/DroneAware-Node-Releases) |
| Kismet + ANTSDR plugin (DJI 경로) | DJI OcuSync DroneID 디코딩 (SDR 하드웨어 필요) | [kismetwireless/kismet](https://github.com/kismetwireless/kismet) + [alphafox02/antsdr_dji_droneid](https://github.com/alphafox02/antsdr_dji_droneid) |

---

## 5. GitHub 프로젝트 링크

```text
# Core decode library (ASTM F3411 / EN 4709-002 message encode/decode)
https://github.com/opendroneid/opendroneid-core-c

# Linux capture program (this kit's main software, validated on rtl8812au + nRF52840 + RPi)
https://github.com/sxjack/unix_rid_capture

# Community real-time map network (one-click install, auto-uploads to droneaware.io)
https://github.com/fduflyer/DroneAware-Node-Releases

# Wireless detection framework (DJI OcuSync path requires SDR plugin)
https://github.com/kismetwireless/kismet

# RTL8812AU monitor / injection driver (required for AWUS036ACH)
https://github.com/morrownr/8812au-20210629
```

---

## 6. 단계별 설정

### Step 1 — 시스템 플래시

<strong>Raspberry Pi Imager</strong>를 사용하여 <strong>Raspberry Pi OS Lite (64-bit)</strong>를 기록하십시오. 톱니바퀴 아이콘(고급 설정)을 클릭합니다.

- 호스트 이름: `droneid-kit`
- SSH를 활성화하고 자격 증명 설정
- WiFi 자격 증명 입력 (나중에 이더넷을 연결하는 수고를 덜 수 있습니다)

### Step 2 — 연결 및 하드웨어 확인

AWUS036ACH를 Pi의 <strong>USB 3.0</strong> 포트(파란색 / `SS` 표시)에 직접 꽂으십시오. 두 안테나가 단단히 조여져 있는지 확인하십시오. 부팅 후 SSH로 접속합니다.

```bash
ssh <user>@droneid-kit.local
sudo -i
lsusb
```

다음과 같이 표시되어야 합니다.

```text
Bus 002 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter
```

### Step 3 — rtl88xxau 모니터 드라이버 설치

```bash
sudo apt update && sudo apt install -y dkms git bc
git clone https://github.com/morrownr/8812au-20210629.git
cd 8812au-20210629
sudo ./install-driver.sh
sudo reboot
```

### Step 4 — 모니터 모드 확인

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
iwconfig wlan0
```

출력에 <strong>`Mode:Monitor`</strong>가 표시되어야 합니다.

### Step 5 — 빌드 의존성 설치

```bash
sudo apt install -y git cmake libncurses-dev libpcap-dev \
  libbluetooth-dev libgps-dev libnl-genl-3-dev libgtest-dev build-essential
```

### Step 6 — opendroneid-core-c 빌드

```bash
git clone --recursive https://github.com/opendroneid/opendroneid-core-c
cd opendroneid-core-c
mkdir build && cd build
cmake ../.
make -j
# Produces libopendroneid/libopendroneid.so and test/odidtest
```

### Step 7 — unix_rid_capture 빌드

`unix_rid_capture`에는 `opendroneid.c` / `opendroneid.h`가 필요합니다. 이전 단계에서 복사하십시오.

```bash
cd ~
git clone https://github.com/sxjack/unix_rid_capture
cp opendroneid-core-c/libopendroneid/opendroneid.{c,h} unix_rid_capture/
cd unix_rid_capture
cmake .
make
```

### Step 8 — 캡처 실행

root 권한 또는 `cap_net_raw`가 필요합니다.

```bash
sudo setcap cap_net_raw+eip rid_capture
./rid_capture -x > rid_capture.txt        # Capture and save as JSON
```

실시간 UDP 출력(다른 터미널에서 실행):

```bash
nc -lu 32001
```

### Step 9 — 비행 경로 시각화 (GPX → Google Earth)

```bash
./scripts/rid2gpx.pl < rid_capture.txt      # Generate .gpx
```

.gpx 파일을 Google Earth에서 열면 드론의 비행 경로를 볼 수 있습니다. 일반적인 탐지 JSON 항목은 다음과 같습니다.

```json
{
  "mac": "ac:67:b2:09:50:d4",
  "operator": "GBR-OP-ZZZZZZZZZZZZ",
  "uav id": "SERIAL NUMBER",
  "uav latitude": 25.0330,
  "uav longitude": 121.5654,
  "uav altitude": 120,
  "uav heading": 90,
  "uav speed": 8,
  "base latitude": 25.0300,
  "base longitude": 121.5600
}
```

### Step 10 — (선택 사항) DroneAware 커뮤니티 실시간 지도에 연결

```bash
curl -fsSL https://github.com/fduflyer/DroneAware-Node-Releases/releases/latest/download/install.sh | sudo bash
```

{{< alert "circle-info" >}}
<strong>보안 유의 사항</strong>: 모든 서드파티 `curl ... | sudo bash` 스크립트는 먼저 다운로드하여 검토하시기를 권장합니다: `curl -fsSL <url> -o install.sh && less install.sh && sudo bash install.sh`. 설치 프로그램은 USB 어댑터를 자동으로 감지하고, 노드 이름을 묻고, droneaware.io 등록 과정을 안내합니다. 탐지 결과는 실시간 지도에 표시됩니다.
{{< /alert >}}

---

## 7. 중요한 기술적 설명: 표준 RID vs. DJI OcuSync

바로 여기에서 전문성이 중요합니다. 고객이 차이점을 확실히 이해하도록 하십시오.

| 경로 | 다루는 범위 | 하드웨어 | ALFA AWUS036ACH로 동작합니까? |
|---|---|---|---|
| <strong>표준 Remote ID</strong> | ASTM F3411 Wi-Fi / BT 브로드캐스트 | AWUS036ACH + nRF52840 | ✅ 예 (본 문서의 주요 주제) |
| <strong>DJI OcuSync DroneID</strong> | DJI 고유 프로토콜 (표준 Wi-Fi 아님) | 풀 SDR (ANTSDR / HackRF / USRP) + Kismet `kismet_cap_antsdr_droneid` 플러그인 | ❌ 아니요 |

- ALFA AWUS036ACH는 <strong>Wi-Fi 대역(2.4 / 5 / 6 GHz) 수신기</strong>입니다. 표준 RID는 완벽하게 처리합니다.
- DJI의 고유 <strong>OcuSync</strong> DroneID는 표준 Wi-Fi 프로토콜을 사용하지 않습니다. <strong>ALFA 어댑터로는 디코딩할 수 없습니다</strong>. 2.4 / 5.8 GHz를 커버하는 SDR(예: ANTSDR E200)과 `alphafox02/antsdr_dji_droneid` + Kismet 플러그인이 필요합니다.
- ⚠️ 참고: <strong>일반 RTL-SDR은 대역폭 상한이 약 1.7 GHz</strong>이므로 2.4 / 5.8 GHz의 OcuSync를 볼 수 없습니다. 더 높은 주파수를 지원하는 SDR을 선택해야 합니다.
- 두 경로는 <strong>상호 보완적</strong>입니다. ALFA 어댑터는 표준 RID 브로드캐스트 탐지를, SDR은 DJI의 고유 프로토콜을 담당하며, 함께 완전한 Counter-UAV / RF 상황 인식 프런트 엔드를 구성합니다.

---

{{< faq >}}

---

## 부록: 입문자를 위한 용어집

드론 규제와 대(對)드론 기술이 처음이시라면, 이 가이드에서 사용한 용어를 쉬운 말로 정리한 빠른 참고 자료를 활용하십시오.

| 용어 | 쉬운 설명 |
|---|---|
| <strong>Remote ID</strong> | 드론의 "디지털 번호판"입니다. 규정에 따라 드론은 신원, 위치 및 기타 정보를 지속적으로 브로드캐스트해야 하며, 지상의 사람들, 특히 규제 당국이 "누구의 드론이며 어디로 가고 있는지"를 볼 수 있습니다. |
| <strong>ASTM F3411 / EN 4709-002</strong> | 각각 미국과 EU의 Remote ID 브로드캐스트 사양 표준입니다. 어떤 정보를 어떤 형식으로 브로드캐스트해야 하는지를 정의하여, 서로 다른 드론 브랜드와 탐지 장비 간의 상호 운용성을 보장합니다. |
| <strong>수동 탐지(Passive Detection)</strong> | 공개적으로 브로드캐스트되는 메시지를 "듣기만" 하는 것입니다. 드론을 방해하거나 공격하기 위한 신호를 능동적으로 송신하지 않습니다. 법적으로 능동적 재밍과는 매우 다릅니다. |
| <strong>모니터 모드</strong> | WiFi 어댑터가 액세스 포인트에 연결을 시도하는 것을 멈추고 대신 공중의 모든 무선 패킷을 "수동적으로 듣는" 상태입니다. Remote ID 브로드캐스트를 캡처하기 위한 전제 조건입니다. |
| <strong>NAN (Wi-Fi Aware) / Beacon</strong> | 드론이 Remote ID를 브로드캐스트하는 데 사용하는 두 가지 Wi-Fi 프레임 형식입니다. 이 키트는 두 가지를 모두 디코딩하려고 시도합니다. |
| <strong>Bluetooth 5 Long Range</strong> | Wi-Fi 외에도 일부 드론은 Bluetooth로 Remote ID를 브로드캐스트합니다. 이를 캡처하려면 추가 nRF52840 동글이 필요합니다. |
| <strong>DJI OcuSync / DroneID</strong> | DJI의 고유 영상 및 텔레메트리 전송 프로토콜입니다. 표준 Wi-Fi가 <strong>아니며</strong>, 이 문서에서 다루는 Remote ID 프로토콜도 <strong>아닙니다</strong>. 완전히 다른 SDR 하드웨어와 플러그인이 필요합니다. 자세한 내용은 7절을 참조하십시오. |
| <strong>SDR (Software Defined Radio)</strong> | 주파수 범위와 복조 방식을 소프트웨어로 설정할 수 있는 범용 무선 수신기입니다. ANTSDR, HackRF 같은 장치는 ALFA 어댑터가 닿을 수 없는 주파수 대역(DJI OcuSync 등)을 커버할 수 있습니다. |
| <strong>RTL8812AU</strong> | ALFA AWUS036ACH 내부의 Realtek 칩셋입니다. 이 칩이 어댑터의 모니터 모드 지원 여부를 결정합니다. |
| <strong>GPX 파일</strong> | GPS 좌표 궤적을 기록하는 표준 형식입니다. Google Earth 등의 소프트웨어에서 바로 열어 드론의 비행 경로를 시각화할 수 있습니다. |

> 한 문장으로 요약하면, 이 가이드는 ALFA 어댑터를 "드론 신원 스캐너"로 바꾸는 방법, 즉 드론이 법적으로 브로드캐스트해야 하는 공개 정보를 수동적으로 수신하는 방법을 알려드립니다. 현장 보안 관리를 위한 합법적인 방법입니다.

---

## 참고 자료

1. [opendroneid/opendroneid-core-c — Open Drone ID Core C Library](https://github.com/opendroneid/opendroneid-core-c)
2. [sxjack/unix_rid_capture — WiFi/BT RID capture (rtl8812au + nRF52840 + RPi validated)](https://github.com/sxjack/unix_rid_capture)
3. [fduflyer/DroneAware-Node-Releases — Community Remote ID detection network](https://github.com/fduflyer/DroneAware-Node-Releases)
4. [kismetwireless/kismet — Wireless detection framework](https://github.com/kismetwireless/kismet)
5. [alphafox02/antsdr_dji_droneid — DJI OcuSync DroneID SDR decoder](https://github.com/alphafox02/antsdr_dji_droneid)
6. [morrownr/8812au-20210629 — RTL8812AU Linux monitor/injection driver](https://github.com/morrownr/8812au-20210629)
7. [ALFA AWUS036ACH 제품 페이지 (Yopitek)](https://yupitek.com/ko/products/alfa/awus036ach/)
8. [문의 및 주문 (Yopitek)](https://www.yupitek.com/ko/contact/)

---

*이 문서는 Yopitek 기술팀이 작성하였습니다. AWUS036ACH 및 관련 하드웨어는 Yopitek을 통해 기술 지원과 함께 구매하실 수 있습니다(Yopitek은 대만의 ALFA Network 공인 유통업체입니다).*
