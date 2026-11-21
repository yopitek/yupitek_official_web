---
title: "6GHz Wi-Fi 6E로 엣지 AI 대역폭 병목 해소하기"
description: "Jetson Orin Nano에 ALFA AWUS036AXML Wi-Fi 6E 어댑터를 설치하여 다중 스트림 RTSP 4K 영상을 6GHz 대역으로 옮기는 방법을, iperf3 및 GStreamer A/B 테스트 결과와 함께 설명합니다."
date: 2026-08-31
author: benny-lai
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["jetson-orin-nano", "wifi-6e", "awus036axml", "6ghz", "rtsp", "edge-ai", "nvidia"]
featureimage: "/images/blog/jetson-orin-nano-wifi-6e-6ghz-high-bandwidth-streaming.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

> <strong>대상 플랫폼</strong>: NVIDIA Jetson Orin Nano Developer Kit, JetPack 6.x (Ubuntu 22.04 LTS 기반, Linux Kernel 5.15)
> <strong>가이드 하드웨어</strong>: ALFA AWUS036AXML (MediaTek MT7921AUN 칩셋, Wi-Fi 6E 트라이밴드 USB 어댑터)
> <strong>범위</strong>: 본 문서는 DIY 오픈소스 학술 / 엔지니어링 개발 플랫폼을 위한 벤치 테스트 평가이며, 상용 제품에 대한 공식 지원이 아니고 폐쇄형 플랫폼 벤더의 보증도 아닙니다.

## 서문: 엣지 디바이스의 "대역폭 한계"는 어디에서 오는가?

Jetson Orin Nano를 액세스 포인트(AP)에 연결하여 IP 카메라 두세 대를 운용하는 것은 평범해 보입니다. 그러나 여러 개의 <strong>4K 라이브 스트림</strong>을 GPU 추론에 투입하는 순간, 많은 분이 처음으로 무선의 한계에 부딪힙니다.

- 화질이 계속 떨어집니다(비트레이트가 정체되고 화면이 흐려지거나 블록 현상이 생깁니다).
- 지연 시간이 크게 요동치며, 영상 AI 추론의 "시간 불일치"가 점점 뚜렷해집니다.
- 스케줄링이 멈추고 관제 센터 화면이 검게 변하는데, 로그에는 "무선 패킷 손실"이라고 나옵니다.

본 문서는 <strong>엣지에서의 다중 스트림 RTSP 4K</strong>가 제기하는 대역폭 과제를 <strong>물리 계층 → 설정 계층 → 측정 계층</strong>의 세 관점에서 분석합니다. 이어서 <strong>Jetson Orin Nano(JetPack / Ubuntu 22.04 LTS)</strong>에 <strong>AWUS036AXML Wi-Fi 6E 어댑터</strong>를 연결하고 깨끗한 <strong>6GHz 대역</strong>으로 전환하는 과정을 보여 드립니다. 마지막으로, 이러한 워크로드에 6GHz가 첫 번째 선택인 이유를 데이터로 설명합니다.

이 카드를 구매할지 아직 결정하지 못하셨다면, 4장의 "구매 전 호환성 체크리스트"로 먼저 이동하여 항목별로 확인하십시오.

---

## 1. 엣지에서의 다중 스트림 RTSP 4K: 무선의 대역폭 및 간섭 과제

### 1.1 먼저 계산해 보기: 4K 스트림 하나에 필요한 대역폭은?

RTSP(Real-Time Streaming Protocol)는 핸드셰이크와 제어만을 위한 프로토콜이며, 실제 영상 데이터는 RTP 패킷으로 전송됩니다. 일반적인 상용 IP 카메라 출력을 예로 들면 다음과 같습니다.

| 카메라 출력 | 코덱 | 스트림당 실제 처리량 (품질 설정에 따라 다름) |
|---|---|---|
| 1080p30 | H.264 | ~4 – 8 Mbps |
| 4K (2160p)30 | H.264 | ~20 – 35 Mbps |
| 4K (2160p)30 | H.265 | ~10 – 20 Mbps |
| 4K (2160p)30 (고비트레이트, 저지연 설정) | H.264 | 최대 45 Mbps 이상 |

> <strong>핵심 포인트</strong>: 4K는 괴물입니다. 스트림 하나당 <strong>HD의 2.5~8배 대역폭</strong>이 소요됩니다. 4K/H.264 스트림 네 개를 동시에 보드로 받으면 <strong>80~140 Mbps의 유효 페이로드</strong>가 됩니다. 주의: 무선 PHY 속도가 아니라 *유효 페이로드*이며, 둘은 거의 두 배 차이가 납니다(1.3 참조).

### 1.2 패킷 손실 ≠ 신호 문제: 무선 매체는 반이중이며 공유된다

많은 분이 "안테나 표시가 가득하면 문제없다"고 생각하지만, 엣지 환경에서 진짜 문제는 <strong>혼잡</strong>입니다.

- <strong>2.4GHz에는 겹치지 않는 채널이 3개뿐입니다</strong>: Bluetooth, 전자레인지, 이웃 공장의 AP가 모두 여기에 몰립니다. CSMA/CA 백오프로 인해 장치 수가 늘어날수록 처리량이 절반으로, 다시 절반으로 줄어듭니다.
- <strong>5GHz는 더 낫지만 여전히 격전지입니다</strong>: 아파트, 사무실, 공장의 5GHz 밀도 때문에 채널 사용률이 한계에 이릅니다.
- <strong>무선은 공유 매체입니다</strong>: PHY 속도가 아무리 높아도 다른 누군가가 채널을 사용 중이면 내 패킷은 기다려야 합니다. 그 결과 TCP 혼잡 제어가 계속 속도를 낮춥니다.

### 1.3 "PHY 2400 Mbps"가 "처리량 2400 Mbps"가 아닌 이유는?

무선 처리량에는 여러 차감이 따릅니다. 이는 물리 법칙입니다.

1. <strong>프로토콜 오버헤드</strong>: Wi-Fi 프레임 헤더, ACK, 비콘, CSMA/CA 경쟁 윈도우가 PHY 속도의 대략 30~50%를 소모합니다.
2. <strong>환경 손실</strong>: 거리, 벽, 금속 반사로 인해 PHY가 낮은 속도로 내려갑니다(최고 MCS에서 더 낮은 MCS로).
3. <strong>양방향 스케줄링</strong>: 영상 업링크와 제어 다운링크가 동일한 무선 링크를 공유합니다.

따라서 2400 Mbps급으로 광고되는 카드는 <strong>깨끗한 환경에서 일반적으로 600~900 Mbps의 실제 페이로드를 제공</strong>하며, 이는 다중 스트림 4K(80~140 Mbps)에 충분합니다. 그러나 <strong>혼잡한 2.4G/5G 채널에 끼어들면 실측치가 흔히 100~300 Mbps로 떨어져</strong> 즉시 병목이 됩니다.

### 1.4 먼저 측정해야 할 세 가지 기준값

하드웨어를 바꾸기 전에 현재 수치를 기록하십시오(이 데이터는 애프터서비스 문의 시 접수 자료로도 쓰입니다).

```bash
# 1) Kernel and system
uname -r
grep PRETTY /etc/os-release

# 2) Current wireless interface and signal
iw dev                      # list wireless interfaces
iw dev wlan0 link           # check current AP, channel, RSSI, bitrate

# 3) AP-side channel utilization (run on the AP, or check the AP WebUI)
#    Connectivity baseline
ping -c 60 -i 1 <AP_GATEWAY_IP>
```

"기존 카드 / 기존 대역"의 RSSI, 비트레이트, ping 지연 시간, 패킷 손실률을 적어 두십시오. 3장의 끝에서 6GHz와 비교하게 됩니다.

---

## 2. JetPack (Ubuntu 22.04 LTS)에서 AWUS036AXML Wi-Fi 6E 설정하기

### 2.1 먼저 JetPack 커널 버전 확인하기

AWUS036AXML은 MediaTek MT7921AUN 칩(AXM은 MT7921AU 사용)을 사용하며, 해당 `mt7921u` 드라이버는 Kernel 5.18에서야 메인라인 Linux 커널에 들어왔습니다. JetPack 6.x는 기본적으로 Kernel 5.15를 탑재하고 있어 메인라인 `mt7921u`가 포함되어 있지 않으므로, <strong>"JetPack을 설치하면 바로 동작한다"고 가정하지 마십시오</strong>. 먼저 커널 버전과 드라이버를 확인하십시오.

```bash
uname -r
```

참조 표:

| JetPack | 기반 OS | Linux Kernel | AWUS036AXML 지원 |
|---|---|---|---|
| JetPack 5.1.x | Ubuntu 20.04 (직접 확인 필요) | 5.10 | 드라이버 확인 필요, JetPack 6.x로 바로 업그레이드하기를 권장 |
| JetPack 6.0 / 6.1 / 6.2 / 6.2.2 (L4T 36.2–36.5) | Ubuntu 22.04 LTS | 5.15 LTS (예: `5.15.116-release-tegra`) | 메인라인 병합(5.18)보다 오래된 버전이며, NVIDIA의 L4T 커널이 드라이버를 백포트한 경우에만 동작하므로 먼저 `modinfo mt7921u`를 실행하십시오 |

> <strong>이 어댑터는 Jetson에서 테스트되지 않았습니다.</strong> Yopitek의 유일한 테스트 플랫폼은 ASUS GX10(Ubuntu 24.04, 커널 6.17)이며, AXML의 6 GHz는 동작하고 모니터 모드는 약하며 패킷 인젝션은 실패합니다. 모든 JetPack 6.x 릴리스는 Kernel 5.15를 사용하므로, JetPack 6.2로 업그레이드해도 드라이버가 내장되지는 않습니다. `modinfo mt7921u`를 실행하여 출력이 나오면 L4T 커널이 이미 드라이버를 포함하고 있는 것이고, 그렇지 않으면 백포트 / DKMS 드라이버가 필요하거나 업스트림 커널 5.18 이상으로 교체해야 합니다(NVIDIA는 JetPack 6가 업스트림 커널 5.14 이상을 실행할 수 있다고 하지만 기본 구성은 아닙니다).

드라이버와 펌웨어가 준비되었는지 확인합니다.

```bash
modinfo mt7921u                         # output = driver is built into the kernel
sudo apt update
sudo apt install linux-firmware         # ensure the latest MediaTek firmware
sudo reboot
```

> <strong>지원 범위</strong>: AWUS036AXML은 <strong>macOS(Intel 및 Apple Silicon 모두)를 지원하지 않습니다</strong>. JetPack은 Jetson 전용 Ubuntu 22.04 LTS 환경에서만 실행되며 본 문서의 모든 명령은 Linux를 전제로 합니다. 개발 호스트가 Mac이라면 아무 Linux 호스트를 엣지 컴퓨팅 노드로 대신 사용하십시오.

### 2.2 어댑터를 Jetson에 연결하기: USB 포트 및 전원 유의 사항

Jetson Orin Nano Developer Kit는 USB 3.2 Type-A 포트(파란색) 2개와 USB 2.0 포트 2개를 제공합니다. AWUS036AXML은 <strong>USB-C 3.2 Gen1</strong> 인터페이스를 사용하며, 2-in-1(USB-C to USB-A) 전원 겸 데이터 케이블이 동봉됩니다.

```bash
# After plugging in, confirm the device is recognized at the USB layer (MediaTek MT7921AU VID:PID is 0e8d:7961)
lsusb | grep -i mediatek
```

<strong>전원 유의 사항 (실제 현장에서 흔한 문제의 원인)</strong>:

- AWUS036AXML은 최대 약 <strong>2.7W</strong>를 소비하므로, Jetson의 USB 3.2 포트에 직접 꽂아도 대개 문제없이 동작합니다.
- 여러 고전력 어댑터, 외장 SSD, USB 카메라를 동시에 사용한다면 전압 강하로 어댑터가 끊겼다 연결되는 일을 피하기 위해 <strong>독립 전원이 있는 전원 공급형 USB 허브를 사용하십시오</strong>.
- 연장 케이블이나 전면 패널 분배 헤더는 사용하지 마십시오. USB 케이블은 짧고 굵을수록 좋습니다.

### 2.3 AP에 연결하고 대역 고정하기

JetPack은 NetworkManager로 무선 네트워크를 관리합니다.

```bash
# Scan and connect
nmcli device wifi list
nmcli device wifi connect "YOUR_SSID" password "YOUR_PASSWORD"
```

<strong>대역 고정 (핵심 단계)</strong>: `nmcli band` 값은 2.4GHz가 `bg`, 5GHz가 `a`이며, <strong>Wi-Fi 6E의 6GHz는 `a`(확장)를 사용합니다</strong>. 가장 확실한 방법은 <strong>AP 측</strong>에서 전용 "<strong>6GHz 전용</strong>" SSID를 만들고 Band Steering을 비활성화한 다음, 클라이언트가 실제로 어느 대역에 접속했는지를 물리 채널 정보로 확인하는 것입니다.

```bash
# Confirm the current connection channel (6GHz frequencies sit between 5925–7125 MHz)
iw dev wlan0 link

# Clean way to confirm: check which band the frequency falls in
iw dev wlan0 link | grep -i freq
#   2.4GHz → 2400-2500 MHz
#   5GHz   → 4900-5900 MHz
#   6GHz   → 5925-7125 MHz (Wi-Fi 6E exclusive)
```

클라이언트가 혼잡한 2.4/5GHz 대역으로 다시 로밍하는 것을 원치 않으면 연결 설정에서 고정하십시오.

```bash
nmcli c show --active                       # find the connection name
nmcli con mod "CONNECTION_NAME" 802-11-wireless.band a
nmcli con up "CONNECTION_NAME"
```

> <strong>규제 관련 유의 사항</strong>: 6GHz 대역의 사용 가능 여부는 해당 국가/지역의 규정과 <strong>AP 펌웨어</strong>에 따라 달라집니다. 예를 들어 대만에서는 NCC가 6GHz로 <strong>5945–6425 MHz</strong>를 개방했으며 <strong>실내 저전력 사용에 한정</strong>됩니다. 5925–7125 MHz 전체가 아닙니다. `iw reg get`이 6GHz를 포함하지 않는 규제 도메인을 표시하거나 AP에서 6GHz를 활성화하지 않았다면 어댑터는 연결되지 않습니다. 이는 하드웨어 결함이 아니라 규제/설정 문제입니다.

---

## 3. 6GHz vs. 혼잡한 2.4G/5G: 실측 대역폭 및 지연 시간

> 이 테스트의 취지는 <strong>같은 Jetson, 같은 어댑터, 같은 AP, 같은 거리</strong>에서 대역만 바꾸고 나머지는 모두 동일하게 유지하는 것입니다. 그래야만 측정된 차이가 대역 자체를 반영합니다.

### 3.1 통제 실험 설계하기

| 변수 | 통제 방법 |
|---|---|
| AP 위치 | 고정. 세 대역 모두 동일한 Wi-Fi 6E AP 사용 |
| 거리 | 고정 (예: 장애물 없는 가시선 3미터) |
| 시간대 | 같은 날, 비슷한 시간 (2.4/5GHz 혼잡도는 현장에서 측정) |
| 어댑터 | 동일한 AWUS036AXML, SSID만 변경 |
| 간섭 환경 | 현장의 기존 간섭을 유지 (실환경 테스트의 핵심) |

### 3.2 측정 1: RSSI 및 단일 링크 처리량 (iperf3)

Jetson에 iperf3를 설치하고 수신 호스트와 짝을 이룹니다.

```bash
# Receiver (e.g., another computer or server)
iperf3 -s

# Jetson side (client, 60-second bidirectional run)
iperf3 -c <RECEIVER_IP> -t 60 -R     # -R measures reverse (Jetson upload)
```

<strong>2.4GHz SSID, 5GHz SSID, 6GHz SSID</strong> 각각에서 한 번씩 실행하고 `sender Mbps`와 `receiver Mbps`를 기록하십시오. 먼저 링크 품질을 확인할 수도 있습니다.

```bash
iw dev wlan0 link                              # RSSI + current PHY bitrate
iw dev wlan0 station dump | grep -E "signal|tx bitrate|rx bitrate"
```

### 3.3 측정 2: 연결성 및 지연 시간 (ping)

```bash
ping -c 60 -i 1 <RECEIVER_IP> | tail -2
```

세 대역 모두에 대해 <strong>평균 지연 시간(ms)</strong>, <strong>패킷 손실률(%)</strong>, <strong>지연 시간 지터(최대-최소)</strong>를 기록하십시오.

### 3.4 측정 3: 실제 다중 스트림 RTSP 4K (GStreamer 스트레스 테스트)

처리량과 지연 시간은 간접 지표이며, <strong>진짜 중요한 것은 프레임 드롭 없이 동시에 디코딩되는 4K 스트림의 수</strong>입니다. JetPack에는 GStreamer 1.0과 NVIDIA의 하드웨어 디코더 플러그인(`nvv4l2decoder`)이 포함되어 있습니다.

```bash
# Use the perf element to count actual decoded frame rate (sampled every 1 second)
gst-launch-1.0 \
  rtspsrc location="rtsp://CAMERA_IP/stream" ! \
  rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! \
  perf print-stats=true ! fakesink
```

여러 터미널을 열어 각각 4K 스트림 하나씩을 실행하고, `nvidia-smi`(Jetson에서는 `tegrastats`)로 GPU/메모리를 관찰하십시오.

```bash
sudo tegrastats
```

<strong>합격 기준</strong>:
- 각 스트림의 `perf`에서 <strong>드롭/렌더링 프레임 레이트(FPS)가 원본 레이트(30fps)에 안정적으로 근접</strong> → 합격.
- 2.4/5GHz에서 프레임이 드롭되거나 화질이 저하되고 6GHz에서 회복된다면 → 대역 혼잡을 실측으로 증명한 것입니다.

### 3.5 예상 결과 예시

| 대역 | PHY 비트레이트 | iperf3 실측 업/다운 | ping 평균/지터 | 다중 스트림 4K 결과 |
|---|---|---|---|---|
| 2.4GHz (혼잡한 사무실) | 300 Mbps | 80–120 Mbps | 8 ms / 높은 지터, 간헐적 손실 | 화질 저하, 화면 흐림 |
| 5GHz (보통 수준 사용) | 800 Mbps | 400–550 Mbps | 3 ms / 중간 | 간신히 동작, 간헐적 끊김 |
| 6GHz (깨끗한 전용 SSID) | 1200 Mbps | 700–900 Mbps | 1–2 ms / 안정적 | 4K 2~4 스트림, 모두 정상 |

> 이것은 "깨끗함 vs. 혼잡함"의 전형적인 대비입니다. <strong>6GHz의 가치는 거의 아무도 사용하지 않는 새로운 대역이라는 점입니다.</strong> 카메라가 밀집하고 장치가 포화된 환경에서는 그 이점이 곧바로 안정적인 다중 스트림 4K 수용 능력으로 이어집니다.

---

## 4. 구매 전 호환성 체크리스트

> 주문하기 전에 모든 항목을 확인하십시오. <strong>구매 전에 이 표를 작성하면 구매 후 문제를 해결하는 수고를 열 배 줄일 수 있습니다.</strong>

### 1단계: 엣지 컴퓨팅 플랫폼 확인

| 확인 항목 | 확인 방법 | 결과 |
|---|---|---|
| 플랫폼 모델 | `cat /proc/device-tree/model` | \_\_\_\_\_ |
| JetPack 버전 | `cat /etc/nv_tegra_release` (JetPack 6.x = L4T 36.x) | \_\_\_\_\_ |
| Linux Kernel | `uname -r` | \_\_\_\_\_ |
| `mt7921u` 내장 여부? | `modinfo mt7921u` | 출력 있음 / 출력 없음 |

> `uname -r`이 5.18 미만이고 `modinfo mt7921u`가 출력을 내지 않는다면(JetPack 6.x의 기본 상황): L4T 커널에 이 드라이버가 포함되어 있지 않은 것입니다. 선택지는 사용 중인 커널에 맞는 백포트 / DKMS 드라이버이거나 5.18 이상 커널로 교체하는 것이며, 둘 다 직접 유지보수해야 하는 구성이므로 먼저 백업하고 롤백 경로를 확보하십시오. JetPack 버전만 올려서는 Kernel 5.15가 바뀌지 않습니다.

### 2단계: 무선 환경 확인

| 확인 항목 | 선택지 / 조건 |
|---|---|
| AP가 Wi-Fi 6E(6GHz)를 지원합니까? | 예 / 아니요 (6GHz AP가 없으면 본 문서의 이점은 적용되지 않습니다) |
| AP에서 6GHz가 활성화되어 있습니까? | 예 / 아니요 (규제 도메인 / 국가 코드 설정 포함) |
| "6GHz 전용" 또는 6GHz 고정이 가능한 전용 SSID가 있습니까? | 예 / 아니요 |
| 카메라 트래픽 추정 | 4K 스트림 몇 개? H.264/H.265? 총 약 \_\_\_ Mbps |
| 거리 및 장애물 | 몇 미터? 벽/금속 차폐? |

### 3단계: OS 지원 확인

| 플랫폼 | 지원 현황 |
|---|---|
| Ubuntu 22.04 / 24.04 | ✅ `mt7921u`는 Kernel 5.18부터 메인라인이며, JetPack 6.x는 기본 5.15이므로 먼저 `modinfo mt7921u`로 확인하거나 백포트 / DKMS 드라이버를 사용하십시오 |
| Kali Linux | ✅ 네이티브 지원 (Monitor Mode); ⚠️ Packet Injection: 커널 6.16 이전에는 커뮤니티 보고가 있었으나, 기본 6.17에서는 테스트에서 실패 |
| Windows 11 | ✅ (6GHz 대역은 Windows 11 이상 필요) |
| Windows 10 | ✅ (단 6GHz 대역 없음, 2.4/5GHz만 가능) |
| macOS (Intel / Apple Silicon) | ❌ <strong>지원 안 됨</strong> (MT7921AU용 macOS 드라이버 없음, 이를 위해 구매하지 마십시오) |
| Raspberry Pi / 기타 Linux SBC | ✅ (Kernel 5.18 이상, `linux-firmware` 설치) |

> <strong>지원 범위 재강조</strong>: AWUS036AXML은 <strong>macOS를 지원하지 않습니다</strong>. 주 개발 장비가 Mac이라면 이 카드의 Wi-Fi 기능은 해당 장비에서 동작하지 않으므로, 사용 플랫폼으로 Linux 호스트나 Linux SBC를 반드시 확보하십시오.

### 4단계: 전원 및 포트 확인

| 확인 항목 | 권장 사항 |
|---|---|
| 호스트 USB 포트 직결 | 가능 (2.7W 저전력) |
| 여러 장치 동시 사용 | <strong>독립 전원이 있는 전원 공급형 USB 허브</strong> 사용 |
| 안테나 배치 | RP-SMA 5dBi 무지향성 안테나 2개를 세워서, 금속 섀시에서 ≥ 5cm 이격 |

### 고객 서비스 접수 자료

구매 후에도 문제가 발생하면 기술 지원에 문의할 때 다음을 <strong>한꺼번에</strong> 첨부하십시오. 플랫폼 모델, JetPack/커널 버전, `lsusb` 출력, `modinfo mt7921u` 결과, `iw dev wlan0 link`의 RSSI/비트레이트, 그리고 AP 모델과 대역 설정입니다. 이렇게 하면 "규제 미개방", "AP 설정", "하드웨어" 중 어느 문제인지 즉시 판단할 수 있습니다.

---

## 5. 면책 조항 및 안전 레드라인

이 솔루션은 <strong>DIY 오픈소스 학술 / 엔지니어링 개발 플랫폼을 위한 벤치 테스트 평가</strong>이며, 상용 제품에 대한 공식 지원이 아니고 "플러그 앤 플레이 상용 턴키 솔루션"을 약속하는 것도 아닙니다.

- <strong>macOS 미지원</strong>: AWUS036AXML에는 macOS 드라이버가 없으므로 본 문서의 워크플로는 Mac에서 실행할 수 없습니다.
- <strong>특정 폐쇄형 플랫폼과의 공식 호환성을 주장하지 않음</strong>: 본 문서는 Jetson Orin Nano 오픈소스 개발 보드와 일반 Linux 환경만 다룹니다. 대상이 <strong>상용 폐쇄형 소스 드론/로봇/비전 시스템</strong>이라면 이 내용은 해당 벤더의 보증이 아니므로, 무선 개조에 대해서는 벤더의 기술 지원에 문의하십시오.
- <strong>안전이 중요한 시스템 제외</strong>: 산업용 안전 필수 제어 시스템에 적용하는 경우, 무선 영상 전송을 안전 루프에 직접 넣지 말고 유선 또는 기존 안전 채널을 유지하십시오.
- <strong>시스템 보호 기능 비활성화 금지</strong>: 본 문서의 모든 설정은 보호 기능이 켜진 상태에서 동작합니다. 네트워크 문제에 대응하기 위해 방화벽, Secure Boot 등을 비활성화하지 마십시오.
- <strong>전파 규정 준수</strong>: 6GHz 사용은 해당 국가/지역의 규정을 준수해야 합니다. 본 문서는 기술적 설정만 설명하며 규제에 대한 조언이 아닙니다.

---

## 결론 및 하드웨어 권장 사항

다중 스트림 4K 영상이 엣지 AI 플랫폼에 유입되면 병목은 대개 연산이 아니라 <strong>무선 페이로드 용량과 채널의 청결도</strong>입니다. 2.4G/5G는 이미 장치로 가득 차 있으며, <strong>Wi-Fi 6E의 6GHz는 간섭 없는 새로운 채널을 제공합니다</strong>. 드라이버를 사용할 수 있는 어댑터와 함께 사용하면(Jetson의 기본 커널은 5.15이므로 먼저 `modinfo mt7921u`로 확인하십시오. 2.1 참조, 이 카드는 Jetson에서 테스트되지 않았습니다) Jetson Orin Nano는 4K 2~4 스트림을 안정적으로 처리할 수 있으며, "대역폭 한계" 문제를 단번에 해소합니다.

<strong>권장 하드웨어</strong>: ALFA AWUS036AXML (MediaTek MT7921AUN, Linux Kernel 5.18 이상에서 컴파일 불필요한 네이티브 지원, Wi-Fi 6E 트라이밴드, RP-SMA 5dBi 고이득 안테나 2개, 2.7W 저전력).

<strong>다음 단계</strong>: 먼저 1장의 기준 측정을 실행한 다음 4장의 체크리스트를 확인하십시오. 측정 데이터를 현장에 가져가 데이터가 대역 전략을 결정하도록 하십시오.
