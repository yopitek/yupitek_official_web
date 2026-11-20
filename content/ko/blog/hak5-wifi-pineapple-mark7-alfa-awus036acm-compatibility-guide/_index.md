---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM: 완벽한 5GHz 설정 가이드 (2026)"
description: "HAK5 WiFi Pineapple MK7와 ALFA AWUS036ACM(MT7612U)의 완벽 호환성 가이드 — 플러그 앤 플레이 5GHz 모니터 모드, 패킷 인젝션, PineAP 확장. 검증된 명령어와 함께 단계별 설정을 안내합니다. 드라이버 컴파일이 필요 없습니다."
date: 2026-06-10
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "WiFi Pineapple Mark VII에 외부 어댑터가 필요한가요?"
    answer: "네. MK7 내장 무선 칩은 2.4 GHz만 지원합니다. 2026년에는 대부분의 네트워크가 5 GHz로 옮겨갔습니다. 외부 AWUS036ACM이 5 GHz 모니터링과 인젝션 기능을 추가해 줍니다."
  - question: "AWUS036ACM이 MK7에서 플러그 앤 플레이인 이유는 무엇인가요?"
    answer: "MK7 Firmware 2.x에는 kmod-mt76x2u 드라이버가 사전 탑재되어 있습니다. MT7612U 칩셋은 커널 4.19부터 포함되어 있습니다. 컴파일이나 설치가 필요 없습니다."
  - question: "MK7의 USB 2.0가 AWUS036ACM 성능을 제한하나요?"
    answer: "USB 2.0는 처리량을 150~250 Mbps로 제한하지만, 패킷 캡처나 핸드셰이크 수집 같은 침투 테스트 작업에는 영향이 없습니다. 고처리량 브리징만 제한됩니다."
  - question: "MK7에서 모니터 모드를 어떻게 활성화하나요?"
    answer: "SSH로 접속해 airmon-ng start wlan3을 실행하면 됩니다. 인터페이스가 wlan3mon으로 변경됩니다. iwconfig로 확인하십시오."
  - question: "MK7과 호환되지 않는 ALFA 어댑터는 무엇인가요?"
    answer: "AWUS036AX와 AWUS036AXER는 RTL8832BU를 사용하며, rtw89_8852bu 드라이버는 커널 6.17부터 내장되어 있고 GX10 커널 6.17에서 모니터 모드와 인젝션이 실측으로 동작했습니다. 다만 Mark7에서는 테스트하지 않았습니다. AWUS036EACS(RTL8821CU)의 rtw88_8821cu 드라이버는 커널 6.2부터 메인라인에 포함되어 있으며 GX10 커널 6.17에서 모니터 모드와 인젝션이 실측으로 동작했습니다. 그러나 Mark7 펌웨어의 커널/드라이버에 해당 모듈이 포함되어 있는지는 본 사이트에서 Mark7로 실측하지 않았으므로 검증된 호환 목록에는 넣지 않았습니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz", "penetration-testing"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
---

HAK5 WiFi Pineapple Mark VII는 휴대용 무선 보안 감사의 표준으로 꼽힙니다. 하지만 기본 상태에서는 한 가지 중대한 제약이 있습니다. 내장 무선 칩이 오직 **2.4 GHz**에서만 작동한다는 점입니다. 2026년 들어 대부분의 기업 및 가정 네트워크는 더 나은 성능과 낮은 혼잡도를 위해 5 GHz로 이전했으며 — 이는 기본 MK7이 절반의 공중 대역을 놓친다는 뜻입니다.

{{< tldr >}}
AWUS036ACM은 MT7612U 칩셋을 사용합니다. MK7 Firmware 2.x에 드라이버가 사전 탑재되어 있습니다. 꽂으면 wlan3로 나타나며 5 GHz 모니터 모드, 패킷 인젝션, PineAP 확장을 지원합니다. 설정은 10분이면 됩니다.
{{< /tldr >}}





여기서 **ALFA AWUS036ACM**이 등장합니다. 이것은 Hak5가 [공식 호환으로 확인한](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters) 몇 안 되는 802.11ac 어댑터 중 하나이며, MK7 Firmware 2.x에 사전 탑재된 커널 내장 `mt76x2u` 드라이버 덕분에 **드라이버 컴파일 없이** 작동합니다.

이 가이드는 하드웨어 사양, 드라이버 호환성, 검증된 7단계 설정 과정, 그리고 전체 침투 테스트 토폴로지까지 모든 것을 다룹니다. 10분 이내에 Pineapple에 5 GHz 모니터 모드와 패킷 인젝션을 추가할 수 있습니다.

---

## 1. WiFi Pineapple에 5 GHz가 필요한 이유

MK7의 내장 MT7628AN SoC는 유능한 2.4 GHz b/g/n 무선 칩을 제공합니다 — 비컨 플러딩, deauth 공격, 클라이언트 프로빙 같은 기본 PineAP 작업에는 충분합니다. 하지만 무선 환경은 진화했습니다.

| 시나리오 | 2.4 GHz (내장) | 5 GHz (AWUS036ACM) |
|---|---|---|
| 기업 WPA2-Enterprise 네트워크 | 2.4 GHz가 여전히 남아있는 경우 많음 | 현대적 구축의 **주 대역** |
| 가정용 메시 시스템 (Eero, Google WiFi) | 레거시 폴백 전용 | 클라이언트 연결의 **기본 대역** |
| 802.11ac 클라이언트 기기 | 2.4 GHz로 연결하는 경우 드묾 | **항상 5 GHz 선호** |
| 채널 혼잡 (아파트/사무실) | 극도로 혼잡 (채널 1–11) | 깨끗한 스펙트럼 (채널 36–165) |
| WPA3-SAE 핸드셰이크 캡처 | 제한적 | 완전한 5 GHz 캡처 기능 |

**결론**: 현대적 네트워크를 감사한다면 5 GHz가 필요합니다. AWUS036ACM은 WiFi Pineapple MK7에 5 GHz를 추가하는 가장 신뢰할 수 있는 방법입니다.

---

## 2. 대상 플랫폼: HAK5 WiFi Pineapple Mark VII

### 2.1 하드웨어 사양

MK7은 패킷 수준 작업에 최적화된 싱글코어 MIPS 24KEc 네트워크 프로세서인 MediaTek MT7628AN system-on-chip 기반입니다.

| 구성 요소 | 사양 |
|---|---|
| **SoC** | MediaTek MT7628AN (MIPS 24KEc) |
| **RAM** | 256 MB DDR2 |
| **저장장치** | 2 GB eMMC |
| **전원** | USB-C, 5V @ 2A |
| **USB 호스트** | 1× USB 2.0 Type-A (최대 480 Mbps) |
| **USB 전력 예산** | 500 mA @ 5V (총 2.5W) |

USB 2.0 포트는 특히 주의가 필요합니다. AWUS036ACM은 5 GHz에서 867 Mbps를 낼 수 있는 USB 3.0 디바이스이지만, MK7의 USB 2.0 버스는 처리량을 약 150~250 Mbps로 제한합니다. 모니터 모드 캡처, 핸드셰이크 수집, 비컨 분석 같은 침투 테스트 작업에는 이 대역폭으로 충분하고도 남습니다. 이 제약은 MK7을 고처리량 무선 브리지로 사용하려 할 때만 문제가 되는데, 이는 애초에 설계된 용도가 아닙니다.

### 2.2 소프트웨어 환경

MK7은 Hak5가 관리하는, 대폭 커스터마이즈된 OpenWrt 배포판을 구동합니다.

| 계층 | 세부 내용 |
|---|---|
| **운영체제** | OpenWrt (Hak5 커스텀 빌드) |
| **커널 버전** | 5.4.x (Firmware 2.x 시리즈) |
| **사전 탑재 드라이버** | `kmod-mt76x2u` (MT7612U), `kmod-mt7601u` (MT7601U) |
| **패키지 매니저** | `opkg` |
| **무선 도구** | `iw`, `iwconfig`, `airmon-ng`, `hostapd` (2.9), `uci` |
| **관리** | PineAP Web UI + SSH (포트 22) |

> ✅ **핵심 사실**: `kmod-mt76x2u`는 MK7 Firmware 2.x에 사전 탑재되어 있습니다. AWUS036ACM은 **플러그 앤 플레이**입니다 — `opkg install`도, 크로스 컴파일도, DKMS 골칫거리도 없습니다.

---

## 3. ALFA AWUS036ACM — 하드웨어 심층 분석

### 3.1 사양

AWUS036ACM은 **MediaTek MT7612U** 칩셋을 중심으로 설계되었으며, 이 칩셋은 버전 4.19(2018년 10월)에서 Linux 메인라인 커널에 병합되었습니다. 이 업스트림 포함이 MK7에서 매끄럽게 작동하는 비결입니다.

| 사양 | 세부 내용 |
|---|---|
| **칩셋** | MediaTek MT7612U |
| **USB VID/PID** | `0E8D:7612` |
| **USB 인터페이스** | USB 3.0 Type-A (USB 2.0 하위 호환) |
| **주파수 대역** | 2.4 GHz (b/g/n) + 5 GHz (a/n/ac) |
| **최대 데이터 전송률** | 2.4 GHz: 300 Mbps · 5 GHz: 867 Mbps |
| **채널 폭** | 20 / 40 / 80 MHz |
| **모니터 모드** | ✅ 지원 |
| **패킷 인젝션** | ✅ 지원 (mac80211 프레임워크 경유) |
| **AP 모드 (Master)** | ✅ 지원 |
| **안테나** | 2× 5 dBi 듀얼밴드 RP-SMA (탈착식) |
| **TX 출력** | 2.4G: 23 dBm · 5G: 20 dBm (±2 dBm) |
| **최대 소비 전류** | 약 380 mA @ 5V |
| **보안 프로토콜** | WEP / WPA / WPA2 / WPA3 / 802.1X |

RP-SMA 안테나 커넥터는 큰 장점입니다. 기본 5 dBi 무지향성 안테나를 테스트 환경에 따라 고이득 지향성 안테나, 패널 안테나, 실외용 옵션으로 교체할 수 있습니다.

### 3.2 확인된 Hak5 호환성

Hak5는 [호환 802.11ac 어댑터](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters) 공식 목록을 유지합니다. AWUS036ACM(MT7612U)은 — **동일한 MT7612U 칩셋**을 사용하는 Hak5 자체 MK7AC 어댑터와 함께 — 호환으로 명시되어 있습니다.

| 어댑터 | 칩셋 | 상태 |
|---|---|---|
| Hak5 MK7AC 어댑터 | MT7612U | ✅ 공식 액세서리 |
| **ALFA AWUS036ACM** | **MT7612U** | ✅ **공식 확인됨** |
| EP-AC1605 V1 | MT7612U | ✅ (V2는 호환되지 않음) |

드라이버 소스는 GitHub의 [OpenWrt mt76 저장소](https://github.com/openwrt/mt76)에 있으며, 설치 참고 사항은 커뮤니티가 [morrownr/7612u](https://github.com/morrownr/7612u)에서 관리합니다.

---

## 4. 호환성 매트릭스

| 평가 항목 | 결과 | 비고 |
|---|---|---|
| 칩셋 호환성 | ✅ **완전** | MT7612U는 MK7의 확인된 칩셋 |
| 드라이버 가용성 | ✅ **사전 탑재** | `kmod-mt76x2u`가 Firmware 2.x에 내장 |
| USB 식별 | ✅ **자동** | VID `0E8D` / PID `7612`를 `mt76x2u`가 매칭 |
| 모니터 모드 | ✅ **지원** | `airmon-ng` 또는 `iw` 경유 |
| 패킷 인젝션 | ✅ **지원** | mac80211 프레임워크 경유 |
| 5 GHz 스캔 | ✅ **지원** | 삽입 후 `wlan3`으로 나타남 |
| USB 2.0 대역폭 | ⚠️ **제한적** | 실사용 5 GHz 처리량 약 150~250 Mbps |
| 전력 예산 | ✅ **안전** | 최대 380 mA vs. 500 mA USB 한도 |
| LED 동작 | ℹ️ **설계상** | MT7612U 드라이버는 LED를 점등하지 않음 — 결함 아님 |

USB 2.0 병목이 유일하게 의미 있는 제약이며, 이는 대량 데이터 전송 속도에만 영향을 줍니다. 모니터 모드 캡처, 핸드셰이크 수집, 인젝션 테스트에는 영향이 없습니다.

---

## 5. 단계별 설정 가이드

### 사전 준비 사항

- **Firmware 2.x**를 구동하는 WiFi Pineapple MK7 (2.1.3 Stable 이상 권장)
- ALFA AWUS036ACM — 정품 칩셋 확인: `lsusb`에 PID `7612`가 표시되어야 함
- MK7의 인터넷 연결 (필요 시 `opkg update`용)
- SSH 클라이언트 (macOS/Linux 내장 터미널; Windows는 PuTTY 또는 MobaXterm)

---

### 1단계: 연결 및 USB 감지 확인

AWUS036ACM을 MK7의 USB Type-A 포트에 꽂습니다. Pineapple에 SSH로 접속합니다.

```bash
ssh root@172.16.42.1
```

USB 디바이스가 인식되는지 확인합니다.

```bash
lsusb
```

**예상 출력** (이 줄을 찾으십시오):

```
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

> ⚠️ PID가 `7612`가 아니라면 해당 어댑터는 AWUS036ACM(MT7612U)이 아닙니다. RTL8812AU 칩셋(PID `8812`)이 탑재된 위조품이나 잘못 표기된 어댑터는 사전 탑재 드라이버로 작동하지 않습니다.

---

### 2단계: 드라이버 로드 확인

```bash
lsmod | grep mt76
```

**예상 출력:**

```
mt76x2u
mt76x2_common
mt76x02_usb
mt76_usb
mt76x02_lib
mt76
```

모듈이 없다면(Firmware 2.x에서는 드문 경우) 수동으로 로드합니다.

```bash
modprobe mt76x2u
```

또는 `opkg`로 설치합니다.

```bash
opkg update
opkg install kmod-mt76x2u
```

---

### 3단계: 무선 인터페이스 표시 확인

```bash
iw dev
```

**예상 출력** (`wlan3` 또는 유사한 항목을 찾으십시오):

```
phy#3
    Interface wlan3
        ifindex 7
        wdev 0x300000001
        addr aa:bb:cc:dd:ee:ff
        type managed
        channel 6 (2437 MHz), width: 20 MHz
```

인터페이스 번호는 기존 무선 칩에 따라 달라집니다. 일반적인 매핑은 다음과 같습니다.
- `wlan0` — 관리 AP (내장 2.4 GHz)
- `wlan1` — PineAP 엔진 (내장 2.4 GHz)
- `wlan2` — 클라이언트 모드 (구성된 경우)
- `wlan3` — **AWUS036ACM** (외부 USB)

---

### 4단계: 모니터 모드 활성화

**방법 A — airmon-ng (권장):**

```bash
airmon-ng check kill
airmon-ng start wlan3
```

인터페이스가 `wlan3mon`으로 변경됩니다. 확인합니다.

```bash
iwconfig wlan3mon
```

**예상 출력:**

```
wlan3mon  IEEE 802.11  Mode:Monitor  Frequency:2.437 GHz ...
```

**방법 B — iw (경량, airmon-ng 의존성 없음):**

```bash
ip link set wlan3 down
iw wlan3 set monitor control
ip link set wlan3 up
```

---

### 5단계: 5 GHz 채널 고정 및 스캔

5 GHz 채널로 전환합니다 (예시: 5180 MHz의 채널 36):

```bash
iw wlan3mon set channel 36
```

airodump-ng를 실행해 5 GHz 대역을 스캔합니다.

```bash
airodump-ng --band a wlan3mon
```

`--band a` 플래그는 802.11a/n/ac(5 GHz)를 대상으로 합니다. 스캔 출력에 5 GHz 액세스 포인트가 나타나야 합니다.

---

### 6단계: 패킷 인젝션 테스트 (선택)

인젝션 기능을 확인합니다.

```bash
aireplay-ng --test wlan3mon
```

**예상 출력 (성공):**

```
09:14:22  Trying injection in the monitor interface... wlan3mon
09:14:22  Injection is working!
```

---

### 7단계: 부팅 시 자동 활성화 (선택)

AWUS036ACM이 삽입된 상태로 MK7이 부팅될 때마다 모니터 모드를 자동으로 활성화하려면, 다음을 `/etc/rc.local`에 추가합니다.

```bash
cat >> /etc/rc.local << 'EOF'
# Auto-enable AWUS036ACM monitor mode on boot
sleep 5
if iw dev wlan3 info > /dev/null 2>&1; then
    ip link set wlan3 down
    iw wlan3 set monitor control
    ip link set wlan3 up
    logger "AWUS036ACM wlan3 set to monitor mode"
fi
EOF
```

---

## 6. 검증 결과

모든 테스트는 정품 ALFA AWUS036ACM이 장착된 MK7 Firmware 2.1.3에서 수행되었습니다.

| 테스트 | 명령어 | 결과 |
|---|---|---|
| USB 디바이스 감지 | `lsusb \| grep 7612` | ✅ 통과 |
| 드라이버 모듈 로드 | `lsmod \| grep mt76x2u` | ✅ 통과 |
| 인터페이스 표시 (wlan3) | `iw dev` | ✅ 통과 |
| 모니터 모드 활성화 | `airmon-ng start wlan3` | ✅ 통과 |
| 5 GHz 채널 전환 | `iw wlan3mon set channel 36` | ✅ 통과 (채널 36–165) |
| 5 GHz AP 스캔 | `airodump-ng --band a wlan3mon` | ✅ 통과 |
| 패킷 인젝션 | `aireplay-ng --test wlan3mon` | ✅ 통과 |
| WPA 핸드셰이크 캡처 | `airodump-ng -c 36 wlan3mon` | ✅ 통과 (EAPOL 캡처됨) |
| 전력 안정성 | 30분 연속 스캔 | ✅ 통과 (연결 끊김 없음) |
| LED 표시등 | 육안 확인 | ℹ️ 정상 (드라이버 설계) |

---

## 7. 권장 사항

**ALFA AWUS036ACM은 현재 구할 수 있는 어댑터 중 WiFi Pineapple Mark VII를 5 GHz로 확장하는 최고의 선택입니다.**

Hak5 자체 MK7AC 어댑터와 정확히 동일한 MT7612U 칩셋을 공유하고, 컴파일이 전혀 필요 없는 커널 내장 드라이버를 사용하며, MK7의 USB 전력 예산 안에서 충분히 여유 있게 작동하고, 모든 5 GHz 채널에 걸쳐 모니터 모드, 패킷 인젝션, 핸드셰이크 캡처라는 완전한 침투 테스트 툴킷을 지원합니다.

**Yopitek에서 AWUS036ACM 구매:**

👉 [ALFA AWUS036ACM 제품 페이지](/ko/products/alfa/awus036acm/)

당사는 ALFA Network 공식 총판이며 모든 ALFA × HAK5 통합 시나리오에 대한 완전한 기술 지원을 제공합니다. 테스트 요구에 맞는 올바른 도구를 찾으려면 전체 [ALFA 어댑터 라인업](/ko/products/alfa/)을 둘러보십시오.

**Yopitek의 관련 자료:**
- [AWUS036ACH vs AWUS036ACM — Kali Linux용 전체 비교](/ko/blog/awus036ach-vs-awus036acm/)
- [2026년 Kali Linux에 가장 좋은 WiFi 어댑터](/ko/blog/best-wifi-adapter-kali-linux-2026/)
- [Kali Linux에서 모니터 모드 활성화 — 완벽 가이드](/ko/blog/enable-monitor-mode-kali-linux/)

**외부 참고 자료:**
- [Hak5 공식 문서 — 호환 802.11ac 어댑터](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)
- [OpenWrt mt76 드라이버 저장소](https://github.com/openwrt/mt76)
- [morrownr USB-WiFi 호환성 목록](https://github.com/morrownr/USB-WiFi)

---

{{< faq >}}

*설정에 도움이 필요하신가요? [yupitek.com/support](/ko/support/)에서 Yopitek 기술 지원에 연락하십시오.*

## 참고 문헌

1. [Hak5 공식 문서, 호환 802.11ac 어댑터](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)
2. [OpenWrt mt76 드라이버 저장소, GitHub](https://github.com/openwrt/mt76)
3. [aircrack-ng, 무선 보안 툴킷 공식 웹사이트](https://www.aircrack-ng.org/)
4. [ALFA Network 공식 웹사이트, AWUS036ACM 제품 사양](https://www.alfa.com.tw/)
5. [Linux Wireless, MT76x2U 드라이버 문서](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
