---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM: 5GHz 완벽 설정 가이드 (2026)"
description: "HAK5 WiFi Pineapple MK7과 ALFA AWUS036ACM (MT7612U)의 완벽한 호환성 가이드 — 플러그 앤 플레이 5GHz 모니터 모드, 패킷 인젝션, PineAP 확장. 검증된 명령어와 함께하는 단계별 설정 방법. 드라이버 컴파일이 필요하지 않습니다."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz", "침투테스트"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
---

HAK5 WiFi Pineapple Mark VII는 휴대용 무선 보안 감사의 업계 표준입니다. 하지만 기본 상태에서는 중요한 제한이 있습니다. 내장 무선 모듈이 **2.4 GHz**만 지원한다는 점입니다. 2026년 현재, 대부분의 기업 및 가정용 네트워크는 더 나은 성능과 혼잡 감소를 위해 5 GHz로 이전했습니다. 즉, 기본형 MK7는 무선 스펙트럼의 절반을 놓치게 됩니다.

바로 여기에 **ALFA AWUS036ACM**이 필요합니다. 이 제품은 Hak5가 [공식적으로 호환성을 확인](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)한 몇 안 되는 802.11ac 어댑터 중 하나입니다. MK7 펌웨어 2.x에 사전 탑재된 `mt76x2u` 커널 드라이버 덕분에 **드라이버 컴파일이 전혀 필요 없는** 플러그 앤 플레이를 경험할 수 있습니다.

이 가이드는 하드웨어 사양, 드라이버 호환성 분석, 검증된 7단계 설정 절차, 그리고 완전한 침투 테스트 토폴로지까지 모든 내용을 다룹니다. 단 10분 만에 Pineapple에 5 GHz 모니터 모드와 패킷 인젝션 기능을 추가할 수 있습니다.

---

## 1. WiFi Pineapple에 5 GHz가 필요한 이유

MK7의 내장 MT7628AN SoC는 기본적인 PineAP 작업(비콘 플러딩, 디인증 공격, 클라이언트 프로빙)에 충분한 2.4 GHz b/g/n 무선을 제공합니다. 그러나 무선 환경은 이미 진화했습니다:

| 시나리오 | 2.4 GHz (내장) | 5 GHz (AWUS036ACM) |
|---|---|---|
| 기업 WPA2-Enterprise 네트워크 | 일부 잔존 | **최신 배포의 주요 대역** |
| 가정용 메시 시스템 (Eero, Google WiFi) | 레거시 폴백 전용 | **클라이언트 연결의 기본 대역** |
| 802.11ac 클라이언트 기기 | 거의 연결 안 함 | **항상 5 GHz 우선** |
| 채널 혼잡 (아파트/사무실) | 극도로 혼잡 (채널 1–11) | 깨끗한 스펙트럼 (채널 36–165) |
| WPA3-SAE 핸드셰이크 캡처 | 제한적 | 완전한 5 GHz 캡처 능력 |

**결론**: 현대 네트워크를 감사하려면 5 GHz가 필요합니다. AWUS036ACM은 MK7에 5 GHz를 추가하는 가장 신뢰할 수 있는 방법입니다.

---

## 2. 대상 플랫폼: HAK5 WiFi Pineapple Mark VII

### 2.1 하드웨어 사양

MK7은 패킷 수준 작업에 최적화된 단일 코어 MIPS 24KEc 네트워크 프로세서인 MediaTek MT7628AN 시스템 온 칩을 기반으로 합니다:

| 구성 요소 | 사양 |
|---|---|
| **SoC** | MediaTek MT7628AN (MIPS 24KEc) |
| **RAM** | 256 MB DDR2 |
| **저장소** | 2 GB eMMC |
| **전원** | USB-C, 5V @ 2A |
| **USB 호스트** | 1× USB 2.0 Type-A (최대 480 Mbps) |
| **USB 전력 예산** | 500 mA @ 5V (총 2.5W) |

USB 2.0 포트는 특별히 주목할 필요가 있습니다. AWUS036ACM은 USB 3.0 장치로 5 GHz에서 최대 867 Mbps를 지원하지만, MK7의 USB 2.0 버스는 처리량을 약 150–250 Mbps로 제한합니다. 침투 테스트 작업 부하(모니터 모드 캡처, 핸드셰이크 수집, 비콘 분석)에는 이 대역폭이 충분합니다. MK7을 고처리량 무선 브리지로 사용하려는 경우에만 제한이 문제가 됩니다.

### 2.2 소프트웨어 환경

MK7은 Hak5가 유지 관리하는 고도로 커스터마이즈된 OpenWrt 배포판을 실행합니다:

| 계층 | 세부 정보 |
|---|---|
| **운영체제** | OpenWrt (Hak5 커스텀 빌드) |
| **커널 버전** | 5.4.x (펌웨어 2.x 시리즈) |
| **사전 탑재 드라이버** | `kmod-mt76x2u` (MT7612U), `kmod-mt7601u` (MT7601U) |
| **패키지 관리자** | `opkg` |
| **무선 도구** | `iw`, `iwconfig`, `airmon-ng`, `hostapd` (2.9), `uci` |
| **관리** | PineAP Web UI + SSH (포트 22) |

> ✅ **중요 사실**: `kmod-mt76x2u`는 MK7 펌웨어 2.x에 사전 탑재되어 있습니다. AWUS036ACM은 **플러그 앤 플레이**입니다 — `opkg install`도, 크로스 컴파일도, DKMS 골치 아픈 일도 없습니다.

---

## 3. ALFA AWUS036ACM — 하드웨어 심층 분석

### 3.1 사양

AWUS036ACM은 2018년 10월 Linux 커널 4.19 버전에 메인라인으로 병합된 **MediaTek MT7612U** 칩셋을 기반으로 합니다. 이 업스트림 통합이 MK7에서의 원활한 호환성을 가능하게 합니다.

| 사양 | 세부 정보 |
|---|---|
| **칩셋** | MediaTek MT7612U |
| **USB VID/PID** | `0E8D:7612` |
| **USB 인터페이스** | USB 3.0 Type-A (USB 2.0 하위 호환) |
| **주파수 대역** | 2.4 GHz (b/g/n) + 5 GHz (a/n/ac) |
| **최대 데이터 속도** | 2.4 GHz: 300 Mbps · 5 GHz: 867 Mbps |
| **채널 폭** | 20 / 40 / 80 MHz |
| **모니터 모드** | ✅ 지원 |
| **패킷 인젝션** | ✅ 지원 (mac80211 프레임워크 경유) |
| **AP 모드 (마스터)** | ✅ 지원 |
| **안테나** | 2× 5 dBi 듀얼밴드 RP-SMA (탈착 가능) |
| **TX 출력** | 2.4G: 23 dBm · 5G: 20 dBm (±2 dBm) |
| **최대 전류 소비** | ~380 mA @ 5V |
| **보안 프로토콜** | WEP / WPA / WPA2 / WPA3 / 802.1X |

RP-SMA 안테나 커넥터는 중요한 장점입니다. 테스트 환경에 따라 기본 5 dBi 무지향성 안테나를 고이득 지향성, 패널 안테나 또는 실외용 옵션으로 교체할 수 있습니다.

### 3.2 Hak5 공식 호환성 확인

Hak5는 공식 [호환 802.11ac 어댑터 목록](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)을 유지 관리합니다. AWUS036ACM (MT7612U)은 호환 목록에 명시되어 있으며, Hak5 자체 MK7AC 어댑터와 **동일한 MT7612U 칩셋**을 사용합니다.

| 어댑터 | 칩셋 | 상태 |
|---|---|---|
| Hak5 MK7AC 어댑터 | MT7612U | ✅ 공식 액세서리 |
| **ALFA AWUS036ACM** | **MT7612U** | ✅ **공식 확인** |
| EP-AC1605 V1 | MT7612U | ✅ (V2는 비호환) |

---

## 4. 호환성 매트릭스

| 평가 항목 | 결과 | 비고 |
|---|---|---|
| 칩셋 호환성 | ✅ **완전** | MT7612U는 MK7 확인 호환 칩 |
| 드라이버 가용성 | ✅ **사전 탑재** | `kmod-mt76x2u`가 펌웨어 2.x에 내장 |
| USB 인식 | ✅ **자동** | VID `0E8D` / PID `7612` → `mt76x2u` 자동 매칭 |
| 모니터 모드 | ✅ **지원** | `airmon-ng` 또는 `iw` 경유 |
| 패킷 인젝션 | ✅ **지원** | mac80211 프레임워크 경유 |
| 5 GHz 스캔 | ✅ **지원** | 삽입 후 `wlan3`으로 표시 |
| USB 2.0 대역폭 | ⚠️ **제한** | 실제 5 GHz 처리량 ~150–250 Mbps |
| 전력 예산 | ✅ **안전** | 380 mA 피크 vs. 500 mA USB 한도 |

---

## 5. 단계별 설정 가이드

### 사전 조건

- WiFi Pineapple MK7, **펌웨어 2.x** 실행 (2.1.3 Stable 이상 권장)
- ALFA AWUS036ACM — 정품 확인: `lsusb`에서 PID `7612` 표시
- MK7에 인터넷 연결 (`opkg update` 필요 시)
- SSH 클라이언트

---

### 1단계: USB 감지 연결 및 확인

AWUS036ACM을 MK7의 USB Type-A 포트에 연결합니다. SSH로 Pineapple에 접속:

```bash
ssh root@172.16.42.1
```

USB 장치 인식 확인:

```bash
lsusb
```

**예상 출력:**

```
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

> ⚠️ PID가 `7612`가 아니면, 어댑터가 AWUS036ACM (MT7612U)이 아닙니다.

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

모듈이 없는 경우:

```bash
modprobe mt76x2u
```

또는 opkg 경유:

```bash
opkg update
opkg install kmod-mt76x2u
```

---

### 3단계: 무선 인터페이스 확인

```bash
iw dev
```

**예상 출력** (`wlan3` 또는 유사):

```
phy#3
    Interface wlan3
        ifindex 7
        wdev 0x300000001
        addr aa:bb:cc:dd:ee:ff
        type managed
```

---

### 4단계: 모니터 모드 활성화

**방법 A — airmon-ng (권장):**

```bash
airmon-ng check kill
airmon-ng start wlan3
```

인터페이스가 `wlan3mon`으로 변경됩니다. 확인:

```bash
iwconfig wlan3mon
```

**방법 B — iw (경량):**

```bash
ip link set wlan3 down
iw wlan3 set monitor control
ip link set wlan3 up
```

---

### 5단계: 5 GHz 채널에 고정 및 스캔

```bash
iw wlan3mon set channel 36
airodump-ng --band a wlan3mon
```

`--band a` 플래그는 802.11a/n/ac (5 GHz)를 대상으로 합니다.

---

### 6단계: 패킷 인젝션 테스트 (선택)

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

모든 테스트는 MK7 펌웨어 2.1.3에서 정품 ALFA AWUS036ACM을 사용하여 수행되었습니다:

| 테스트 | 명령어 | 결과 |
|---|---|---|
| USB 장치 감지 | `lsusb \| grep 7612` | ✅ 통과 |
| 드라이버 모듈 로드 | `lsmod \| grep mt76x2u` | ✅ 통과 |
| 인터페이스 표시 (wlan3) | `iw dev` | ✅ 통과 |
| 모니터 모드 활성화 | `airmon-ng start wlan3` | ✅ 통과 |
| 5 GHz 채널 전환 | `iw wlan3mon set channel 36` | ✅ 통과 (채널 36–165) |
| 5 GHz AP 스캔 | `airodump-ng --band a wlan3mon` | ✅ 통과 |
| 패킷 인젝션 | `aireplay-ng --test wlan3mon` | ✅ 통과 |
| WPA 핸드셰이크 캡처 | `airodump-ng -c 36 wlan3mon` | ✅ 통과 (EAPOL 캡처됨) |
| 전원 안정성 | 연속 스캔 30분 | ✅ 통과 (연결 끊김 없음) |

---

## 7. 권장 사항

**ALFA AWUS036ACM은 WiFi Pineapple Mark VII를 5 GHz로 확장하기 위해 현재 구매 가능한 최고의 어댑터입니다.**

Hak5 자체 MK7AC 어댑터와 정확히 동일한 MT7612U 칩셋을 공유하며, 커널 내장 드라이버로 컴파일이 전혀 필요 없고, MK7의 USB 전력 예산 내에서 완벽하게 작동하며, 모든 5 GHz 채널에 걸쳐 모니터 모드, 패킷 인젝션, 핸드셰이크 캡처 등 완전한 침투 테스트 도구 체인을 지원합니다.

**Yupitek에서 AWUS036ACM 구매하기:**

👉 [ALFA AWUS036ACM 제품 페이지](/ko/products/alfa/awus036acm/)

저희는 ALFA Network 공식 대리점으로, 모든 ALFA × HAK5 통합 시나리오에 대한 완전한 기술 지원을 제공합니다.

**Yupitek 관련 자료:**
- [AWUS036ACH vs AWUS036ACM — Kali Linux 완전 비교](/ko/blog/awus036ach-vs-awus036acm/)
- [2026년 Kali Linux 최고의 WiFi 어댑터](/ko/blog/best-wifi-adapter-kali-linux-2026/)

**외부 참조:**
- [Hak5 공식 문서 — 호환 802.11ac 어댑터](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)
- [OpenWrt mt76 드라이버 저장소](https://github.com/openwrt/mt76)
- [morrownr USB-WiFi 호환성 목록](https://github.com/morrownr/USB-WiFi)

---

*설정에 도움이 필요하신가요? Yupitek 기술 지원팀에 문의하세요: [yupitek.com/support](/ko/support/)*
