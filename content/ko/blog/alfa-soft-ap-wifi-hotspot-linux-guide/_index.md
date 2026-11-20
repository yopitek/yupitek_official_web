---
title: "ALFA Network Soft AP 완벽 가이드 2026: Kali Linux, Ubuntu, Debian 및 Raspberry Pi 4/5에서 WiFi 핫스팟 구축하기"
description: "Kali Linux, Ubuntu, Debian, Raspberry Pi 4/5에서 ALFA Network USB WiFi 어댑터의 Soft AP(hostapd/WiFi 핫스팟) 지원 현황을 심층 조사합니다. AWUS036ACM, AWUS036ACH, AWUS036AXML의 전체 설정 가이드, 커뮤니티 피드백, 실전 문제 해결을 다룹니다."
date: 2026-05-21
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "ALFA USB 어댑터를 Linux에서 WiFi 핫스팟으로 사용할 수 있나요?"
    answer: "칩셋에 따라 다릅니다. AWUS036ACM(MT7612U)은 완전하게 지원하며 플러그 앤 플레이로 동작합니다. AWUS036ACH(RTL8812AU)는 조건부 지원이며, AWUS036AXML은 튜닝이 필요한 부분 지원입니다."
  - question: "Raspberry Pi에서 Soft AP를 구성하기에 가장 좋은 ALFA 어댑터는 무엇인가요?"
    answer: "AWUS036ACM이 최선의 선택입니다. 커널 내장 드라이버로 플러그 앤 플레이가 가능하고, 소비 전류가 400mA에 불과해 Pi에 적합하며, WPA3와 VIF 가상 인터페이스를 지원하고 플랫폼 간 안정성이 뛰어납니다."
  - question: "내 어댑터가 AP 모드를 지원하는지 어떻게 확인하나요?"
    answer: "iw list | grep -A 10 'Supported interface modes'를 실행하세요. 출력에 * AP가 포함되어 있으면 드라이버가 Soft AP를 지원하며 hostapd가 정상 동작합니다."
  - question: "RTL8812AU Soft AP의 제약 사항은 무엇인가요?"
    answer: "WPA3 미지원(WPA2-PSK만 가능), VIF 가상 인터페이스 미지원(역할을 분리하려면 어댑터 두 개 필요), 약 800mA의 소비 전류로 인해 Pi에서는 외부 전원 공급형 USB 허브가 필요합니다."
  - question: "AWUS036AXML에서 Soft AP 실행 중 WiFi가 끊기면 어떻게 해야 하나요?"
    answer: "MT7921AUN에 내장된 Bluetooth 5.2가 WiFi를 간섭합니다. /etc/modprobe.d/에 echo 'install btusb /bin/false'를 추가해 Bluetooth 드라이버를 영구적으로 비활성화한 뒤 재부팅하세요."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Soft-AP", "WiFi-Hotspot", "hostapd", "Kali-Linux", "Ubuntu", "Debian", "Raspberry-Pi", "AWUS036ACM", "AWUS036ACH", "AWUS036AXML", "MT7612U", "RTL8812AU", "MT7921AUN", "Linux-WiFi"]
featureimage: "/images/blog/alfa-soft-ap-wifi-hotspot-linux-guide.webp"
---
> "ALFA USB WiFi 어댑터를 Kali Linux / Ubuntu / Raspberry Pi에서 WiFi 핫스팟(Soft AP)으로 사용할 수 있나요?"

## 들어가며

이것은 Yopitek가 가장 자주 받는 질문 중 하나입니다. 질문 자체는 단순하게 들리지만, 답은 모델과 칩셋에 따라 크게 달라집니다 — <strong>모든 USB WiFi 어댑터가 Soft AP 모드로 동작하는 것은 아닙니다.</strong>

{{< tldr >}}
ALFA 어댑터의 Soft AP 호환성은 칩셋 드라이버에 달려 있습니다. AWUS036ACM은 플랫폼 간 안정적인 선택입니다. AWUS036ACH는 동작하지만 WPA3를 지원하지 않습니다. AWUS036AXML은 Bluetooth 비활성화와 펌웨어 업데이트가 필요합니다. RTL8832BU(AX / AXER)는 커널 6.17 이상의 내장 드라이버로 사용할 수 있습니다.
{{< /tldr >}}


ALFA AWUS036ACM(MT7612U)은 Linux Soft AP의 최고 선택지로, 커널 내장 플러그 앤 플레이 드라이버, WPA3 지원, VIF 가상 인터페이스를 제공합니다. RTL8812AU는 조건부로 동작하며, MT7921AUN은 수동 튜닝이 필요합니다.







이 글은 GitHub(morrownr/USB-WiFi), Reddit 기술 포럼, Raspberry Pi 공식 문서, 실사용자 피드백에서 500건이 넘는 커뮤니티 논의를 종합하여, 어떤 ALFA 어댑터가 동작하고 어떤 것이 동작하지 않는지, 그리고 전체 설정 절차를 단계별로 정직하고 포괄적으로 정리한 보고서입니다.

---

## 1. Soft AP란 무엇이며 Linux에서 어떻게 동작하는가 {#what-is-softap}

<strong>Soft AP(Software Access Point)</strong>는 소프트웨어 — 주로 <strong>hostapd</strong> — 를 사용하여 일반 USB WiFi 어댑터를 무선 기지국(Access Point)으로 바꾸는 기능입니다. 이를 통해 전용 라우터나 AP 하드웨어를 구입하지 않고도 다른 기기(휴대폰, 노트북, IoT 장비)가 네트워크에 연결할 수 있습니다.

이 기능은 다음과 같은 여러 시나리오에서 큰 가치를 발휘합니다:

- <strong>여행용 / 가정용 라우터</strong>: 이동 중이나 캠핑 시 ALFA 어댑터를 노트북이나 Raspberry Pi에 꽂아 즉시 휴대용 WiFi 핫스팟을 만듭니다
- <strong>침투 테스트 랩</strong>: 보안 연구를 위한 격리된 Rogue AP를 구축합니다
- <strong>IoT 중계</strong>: 신호 사각지대에 리피터를 만들어 IoT 센서가 데이터를 전송할 수 있도록 합니다
- <strong>엣지 AI 배포</strong>: 유선 네트워크가 없는 산업 환경에서 장치를 핫스팟으로 전환해 다른 장비가 연결하도록 합니다
- <strong>비상 통신</strong>: 연결이 끊긴 상황에서 임시 네트워크를 신속하게 구축합니다

### Linux Soft AP의 4대 핵심 구성 요소

| 구성 요소 | 기능 |
|-----------|----------|
| <strong>hostapd</strong> | Access Point를 생성하는 핵심 데몬 — SSID, 인증, 암호화를 관리합니다 |
| <strong>nl80211</strong> | 표준 Linux 무선 서브시스템 인터페이스 — hostapd와 함께 동작하려면 드라이버가 이 프레임워크를 지원해야 합니다 |
| <strong>dnsmasq</strong> | 연결된 클라이언트에 IP 주소를 자동으로 할당하는 DHCP 서버 |
| <strong>iptables / nftables</strong> | 네트워크 주소 변환(NAT) — 연결된 클라이언트가 상위 네트워크를 공유할 수 있게 합니다 |

### 핵심 개념: Master Mode

<strong>Master Mode</strong>(AP Mode 또는 Infrastructure Mode라고도 함)는 드라이버 수준의 기능입니다. 드라이버가 Master Mode를 지원하지 않으면 설정이 아무리 완벽해도 hostapd는 아예 시작되지 않습니다.

AP 모드 지원 여부는 다음 명령으로 확인합니다:

```bash
iw list | grep -A 10 "Supported interface modes"
```

출력에 `* AP`가 포함되어 있으면 어댑터의 드라이버가 Soft AP를 지원하는 것입니다. 그렇지 않다면 해당 어댑터는 이 용도로 사용할 수 없습니다.

### 💡 커널 내장 드라이버 vs 커널 외부 드라이버

이것은 Soft AP 어댑터를 선택할 때 <strong>가장 중요한</strong> 개념입니다:

| 유형 | 설명 | Soft AP에 미치는 영향 |
|------|-------------|-------------------|
| <strong>커널 내장(In-kernel) 드라이버</strong> | 공식 Linux 소스 트리에 병합되어 부팅 시 자동 로드됨 — 수동 설치 불필요 | ✅ 장기적으로 안정적; 커널 업그레이드에도 유지됨 |
| <strong>커널 외부(Out-of-kernel) 드라이버</strong> | GitHub에서 내려받아 수동 컴파일해야 하며, 커널을 업데이트할 때마다 재컴파일이 필요할 수 있음 | ⚠️ 커널 업그레이드 후 동작이 깨질 수 있음 |

<strong>장기적인 Soft AP 안정성을 위해서는 커널 내장 드라이버가 커널 외부 드라이버보다 월등히 우수합니다.</strong>

---

## 2. ALFA 제품 라인업 및 칩셋 개요 {#product-lineup}

다음은 Yopitek가 판매하는 현행 ALFA 제품 라인업으로, 칩셋과 예비 Soft AP 평가를 함께 정리했습니다:

| 모델 | 칩셋 | 드라이버 유형 | WiFi 규격 | Soft AP 등급 |
|-------|---------|-------------|---------------|----------------|
| <strong>AWUS036ACM</strong> | MediaTek MT7612U | 커널 내장(커널 4.19+) | WiFi 5 AC1200 듀얼밴드 | ✅ 완전 지원 |
| AWUS036ACH | Realtek RTL8812AU | 커널 외부(6.13+부터 커널 내장) | WiFi 5 AC1200 듀얼밴드 | ⚠️ 조건부 |
| AWUS036AXML | MediaTek MT7921AUN | 커널 내장(5.18+, AP 모드 5.19+) | WiFi 6E AX3000 트라이밴드 | ⚠️ 부분 지원 |
| AWUS036AXM | MediaTek MT7921AUN | 커널 내장(위와 동일) | WiFi 6E AX3000 트라이밴드 | ⚠️ 부분 지원 |
| AWUS036AX | Realtek RTL8832BU | 커널 내장 rtw89_8852bu(커널 6.17+), 이전 커널은 커뮤니티 DKMS 드라이버 | WiFi 6 AX1800 듀얼밴드 | ✅ 사용 가능 (커널 6.17+) |
| AWUS036AXER | Realtek RTL8832BU | 커널 내장 rtw89_8852bu(커널 6.17+, AX와 동일) | WiFi 6 AX1800 듀얼밴드 | ✅ 사용 가능 (커널 6.17+) |

> <strong>참고</strong>: AWUS036ACHM(MT7610U)은 단종되어 Yopitek 제품 페이지에 더 이상 게재되지 않습니다. 이 글은 현재 판매 중인 제품만 다룹니다.

---

## 3. AWUS036ACM (MT7612U) — ⭐ 최우선 추천 {#acm}

### Soft AP 상태: ✅ 완전 지원

MT7612U는 ALFA 현행 라인업 중 가장 안정적인 Soft AP 칩셋입니다. 드라이버 `mt76x2u`는 2018년(커널 4.19)부터 공식 Linux 커널에 포함되어 있어, 어느 정도 최신인 시스템이라면 별도 설정 없이 바로 동작합니다 — <strong>`git clone`도, `dkms`도, 커널 업그레이드 후 재컴파일도 필요 없습니다.</strong>

### 주요 장점

- <strong>WPA2 + WPA3 동시 지원</strong>: MediaTek의 커널 내장 드라이버는 WPA3 SAE를 기본 지원합니다 — Realtek 드라이버가 따라올 수 없는 장점입니다
- <strong>VIF 가상 인터페이스 지원</strong>: 단일 어댑터에서 AP + Managed + Monitor 모드를 동시에 실행할 수 있어 두 번째 카드를 살 필요가 없습니다. 네트워크를 공유하면서 동시에 무선 스펙트럼을 모니터링할 수 있습니다
- <strong>초저전력</strong>: 최대 소비 전류 약 400mA로, Raspberry Pi에 완벽합니다(Pi 4의 USB 서브시스템은 전체 1200mA만 공급)
- <strong>플랫폼 호환성</strong>: Kali Linux 2022.x~2025.x, Ubuntu 22.04/24.04, Debian 11/12, Raspberry Pi OS(Pi 3B+, 4, 5)에서 광범위하게 검증됨

### 올바른 hostapd 설정 (MT7612U)

다음 capability 플래그는 수년간의 커뮤니티 테스트(morrownr/USB-WiFi)를 통해 검증되었습니다. <strong>MT7612U의 실제 하드웨어 사양과 정확히 일치해야 합니다:</strong>

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACM (MT7612U)
interface=wlan1
driver=nl80211
ssid=YourNetworkName
hw_mode=a                     # 5GHz; 2.4GHz는 g 사용
channel=36                    # UNII-1, non-DFS, 가장 안전한 선택
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# MT7612U 올바른 HT / VHT capabilities
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42    # 채널 36의 중심 주파수 인덱스

# 보안: WPA2 + WPA3 혼합 모드
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK SAE       # WPA2 + WPA3 동시 지원
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=YourPassword
```

### ⚠️ 가장 흔한 실수

`ht_capab`에 MT7612U가 실제로 지원하지 않는 capability 플래그가 포함되어 있으면(특히 USB 2.0에서 특정 HT40 설정을 강제하는 경우), hostapd는 매우 불친절한 오류 메시지와 함께 조용히 중단됩니다. <strong>위에서 검증된 플래그 조합만 사용하고, RTL8812AU 같은 다른 칩셋의 설정을 복사하지 마세요.</strong> (출처: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2))

### 커뮤니티 평가

> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. I have tested the Alfa AWUS036ACM with many different computer systems and Linux distros. In my opinion, it is an outstanding USB WiFi adapter."
> — <strong>morrownr</strong>, GitHub에서 가장 권위 있는 Linux USB WiFi 커뮤니티 지식 베이스의 유지보수자

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> — eBay 사용자 리뷰

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> — GitHub issue #2 토론 스레드

---

## 4. AWUS036ACH (RTL8812AU) — 동작하지만 절충이 필요 {#ach}

### Soft AP 상태: ⚠️ 조건부 지원

RTL8812AU는 ALFA의 가장 상징적인 침투 테스트 칩셋이자 오랫동안 Kali Linux 커뮤니티의 사랑을 받아온 제품입니다. Soft AP 기능 자체는 동작하며 — 기본적인 핫스팟 생성은 문제없습니다 — 다만 Realtek의 커널 외부 드라이버 구조상 다음과 같은 지속적인 제약이 따릅니다:

### 알려진 제약 사항

1. <strong>WPA3 미지원</strong>: RTL8812AU 드라이버가 WPA3 지원을 표방하지만, 여러 사용자가 실제로는 동작하지 않음을 확인했습니다. <strong>WPA2-PSK만 가능합니다.</strong>
2. <strong>VIF 미지원</strong>: 동일 카드에서 AP + Monitor 모드를 동시에 실행할 수 없습니다. AP와 모니터링이 모두 필요하다면 별도의 어댑터 두 개를 사용해야 합니다.
3. <strong>Kali Linux 2025.x 드라이버 문제</strong>: 최신 Kali에서 최신 aircrack-ng/rtl8812au 드라이버는 호환성 문제가 있어, 특정 구버전 커밋(`63cf0b4`)으로 롤백해야 합니다. 커널 6.13+의 커널 내장 rtw88 드라이버로 상황이 개선될 수 있습니다.
4. <strong>높은 소비 전류</strong>: 최대 약 800mA — Raspberry Pi에 여러 USB 장치를 연결한 상태에서는 시스템 불안정을 유발할 수 있으므로 외부 전원 공급형 USB 허브를 사용하세요.

### hostapd 설정 (RTL8812AU)

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACH (RTL8812AU)
# 주의: MT7612U와는 capabilities가 완전히 다릅니다!
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]

# 보안: WPA2만, WPA3는 추가하지 말 것
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
```

### 드라이버 설치 (Kali Linux / Ubuntu / Debian)

```bash
sudo apt update && sudo apt install -y dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
# Kali 2025.x는 구버전 커밋이 필요
git checkout 63cf0b4
make && sudo make install
sudo modprobe 88XXau
```

### 커뮤니티 평가

> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine."
> — GitHub issue #2 사용자

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> — morrownr 기술 노트

### ACH에 대한 결론

이미 AWUS036ACH를 보유하고 있다면 Soft AP로 활용할 수 있습니다(기본 핫스팟 기능은 동작). 하지만 아직 구매 전이고 주된 목적이 Soft AP라면 <strong>ACM을 선택하세요.</strong>

---

## 5. AWUS036AXML / AWUS036AXM (MT7921AUN) — 신중하게 접근 {#axml}

### Soft AP 상태: ⚠️ 부분 지원 — 알려진 펌웨어/드라이버 이슈 존재

AWUS036AXML과 AWUS036AXM은 ALFA의 WiFi 6E 트라이밴드 플래그십으로, 2.4 GHz, 5 GHz 및 새로운 6 GHz 대역을 커버합니다(AXML의 6 GHz는 실측 확인, AXM의 6 GHz는 사양상 지원이며 미실측). 커널 내장 드라이버 `mt7921u`는 5.18 버전부터 커널에 포함되었으며, AP 모드 지원은 5.19에서 공식 추가되었습니다. 다만 MT7921AUN 칩에는 Bluetooth 5.2도 통합되어 있는데, 이것이 2024~2025년 커뮤니티의 가장 큰 골칫거리가 되었습니다.

### AP 모드 커널 버전 이정표

| 모드 | 최소 커널 |
|------|---------------|
| Managed(일반 WiFi) | 5.18+ |
| <strong>AP Mode(Soft AP)</strong> | <strong>5.19+</strong> |
| AP/VLAN | 5.19+ |
| P2P-GO(Wi-Fi Direct AP) | 6.4+ |

### 알려진 문제와 해결책

#### 문제 1: Bluetooth 간섭으로 인한 WiFi 다운

커널 6.6+에서는 BT 서브시스템 변경으로 인해 mt7921u에서 간헐적인 WiFi 다운이 발생합니다. 재현 여부는 시스템 환경에 따라 다릅니다. <strong>가장 효과적인 해결책은 btusb 드라이버를 비활성화하는 것입니다:</strong>

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

#### 문제 2: 오래된 펌웨어

시스템의 MediaTek 펌웨어가 너무 오래되면 어댑터가 제대로 인식되지 않을 수 있습니다. 2024년 11월 이후 버전의 펌웨어를 설치하세요:

```bash
# 현재 펌웨어 버전 확인
dmesg | grep "WM Firmware"
# 출력 예상: Build Time: 20241106151045 또는 그 이후

# 오래된 경우 kernel.org에서 내려받기
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek/
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek/
sudo reboot
```

#### 문제 3: hostapd 버전 요구사항

완전한 WiFi 6 AP 모드 지원을 위해 hostapd를 git에서 컴파일해야 한다는 사용자 보고가 있습니다. 시스템 패키지 관리자의 버전은 기능이 불완전할 수 있습니다.

#### 문제 4: AP 모드에서 Tx Power 표시 이상

`iw`가 조정 불가능한 3 dBm만 표시하지만 칩에는 실제로 내부 증폭기가 있습니다 — 이는 커널 드라이버의 표시 문제일 뿐 하드웨어 한계가 아닙니다.

#### 문제 5: 특정 커널 버전에서의 Monitor 모드 문제

2025년 12월 기준, 커널 6.18 및 일부 이전 mt7921u 드라이버 버전에는 Monitor 모드 문제가 있습니다.

### 커뮤니티 평가

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> — <strong>fhteagle</strong>, [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

### AXML/AXM에 대한 결론

WiFi 6E의 6 GHz 대역이 필요하고 가끔씩 설정을 손볼 의향이 있다면 이 제품을 선택하세요. <strong>흔들림 없는 Soft AP 안정성이 요구되는 운영 환경이라면 ACM을 선택하세요.</strong>

---

## 6. AWUS036AX / AWUS036AXER (RTL8832BU) — 커널 6.17 이상에서 Soft AP 사용 가능 {#ax}

### Soft AP 상태: ✅ 커널 6.17 이상에서 사용 가능 (구형 커널은 커뮤니티 DKMS 드라이버 필요)

ASUS GX10(Ubuntu 24.04 ARM64, 커널 6.17)에서 내장 `rtw89_8852bu` 드라이버로 실측한 결과, AWUS036AX와 AWUS036AXER(같은 칩, 같은 드라이버)는 동일하게 동작하며 2.4 GHz와 5 GHz 모두에서 Soft AP가 동작합니다.

<strong>실측 결과 (커널 6.17):</strong>

1. <strong>AP 모드</strong>: 2.4 GHz(802.11n)와 5 GHz(VHT 80 MHz) 모두 동작
2. <strong>VIF(STA + AP)</strong>: 동작 — 같은 채널에서 클라이언트 연결과 AP 인터페이스를 동시에 유지
3. <strong>WPA3-SAE AP</strong>: 2.4 GHz에서 동작 (iPhone 15 Pro 연결, MFP 활성, 5 GHz 미실측)
4. <strong>Monitor / 인젝션</strong>: 2.4 및 5 GHz에서 monitor 수신이 강력함. 2.4 GHz 인젝션 AX 96% / AXER 73%, 5 GHz 사용 가능. 엔드투엔드 WPA 핸드셰이크 캡처 성공
5. <strong>미지원</strong>: IBSS, Mesh, Active monitor

<strong>유의 사항:</strong>

- <strong>커널 버전이 전제 조건</strong>: rtw89_8852bu는 커널 6.17부터 내장됩니다. 구형 커널에서는 커뮤니티 DKMS 드라이버(rtl8852bu)가 필요하며, 이 경우 monitor가 제한될 수 있고 VIF도 지원되지 않습니다.
- <strong>USB 모드</strong>: 일부 장치는 CD-ROM 모드(`0bda:1a2b`)로 인식되어 `usb_modeswitch -v 0bda -p 1a2b -K`가 필요할 수 있습니다. 이번 테스트 장치는 처음부터 무선 어댑터로 인식되었습니다.
- <strong>커뮤니티 사례</strong>: MT7612U와 RTL8812AU에 비해 이 칩의 Soft AP 사례는 아직 적습니다.

> Yopitek 실측 결과(ASUS GX10, 커널 6.17): 내장 드라이버에서 AWUS036AX / AWUS036AXER는 monitor 수신이 강력하고 패킷 인젝션이 동작하므로 침투 테스트에도 사용할 수 있습니다. monitor 지원이 제한되는 것은 구형 커널에서 커뮤니티 DKMS 드라이버를 쓰는 경우뿐입니다.
>
> 보충: stock kernel 6.16 이상(6.17에서 실측)에서 AWUS036AXML의 monitor, AP, WPA3, VIF는 동작하지만 패킷 인젝션 테스트는 실패했습니다(aireplay-ng --test: Found 0 APs / No Answer). 원인은 칩 자체가 아니라 mac80211 chanctx 회귀입니다. 인젝션이 필요하면 AWUS036ACH, EACS, ACS 또는 AX를 사용하세요.

---

## 7. 플랫폼 호환성 매트릭스 {#compat-matrix}

### AWUS036ACM (MT7612U)

| 플랫폼 | Soft AP | 비고 |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ✅ | 커널 내장, 플러그 앤 플레이, 커널 5.x / 6.x |
| Ubuntu 22.04 / 24.04 | ✅ | 커널 내장, 무설정, LTS 사용 권장 |
| Debian 11 / 12 | ✅ | 커널 내장, 안정적 |
| Raspberry Pi 4 (RPi OS) | ✅ | 최저 전력(400mA), morrownr 장기 검증. Pi 4 USB 3.0 포트 우선 사용 |
| Raspberry Pi 5 (RPi OS) | ✅ | Pi 4와 동일 드라이버, 안정적 |

### AWUS036ACH (RTL8812AU)

| 플랫폼 | Soft AP | 비고 |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ⚠️ | 외부 드라이버 필요; 2025.x는 커밋 `63cf0b4` 필요. 커널 6.13+ rtw88로 개선 가능 |
| Ubuntu 22.04 / 24.04 | ⚠️ | rtw88 또는 aircrack-ng 드라이버 수동 설치 필요할 수 있음 |
| Debian 11 / 12 | ⚠️ | 위와 동일 |
| Raspberry Pi 4 | ⚠️ | 동작하지만 고전력(800mA); 외부 전원 공급형 USB 허브 사용 |
| Raspberry Pi 5 | ⚠️ | 동일; Pi 5 USB 컨트롤러 차이가 동작에 영향을 줄 수 있음 |

### AWUS036AXML / AWUS036AXM (MT7921AUN)

| 플랫폼 | Soft AP | 비고 |
|----------|---------|-------|
| Kali Linux 2022.x (커널 5.18+) | ✅ | btusb 비활성화, 펌웨어 업데이트 |
| Kali Linux 2024.x / 2025.x | ⚠️ | 커널 6.11+ BT/WiFi 충돌, 불안정 |
| Ubuntu 24.04 (커널 6.8+) | ⚠️ | 2024년 말 문제 보고됨 |
| Ubuntu 25.04 / CachyOS (커널 6.14+) | ✅ | 플러그 앤 플레이, 신규 커널에서 크게 개선 |
| Debian 12 | ⚠️ | 커널 버전에 따라 다름 |
| Raspberry Pi 4 / 5 | ⚠️ | 성공 사례 있으나 펌웨어 확인 + BT 비활성화 필요 |

### AWUS036AX / AWUS036AXER (RTL8832BU)

| 플랫폼 | Soft AP | 비고 |
|----------|---------|-------|
| Kali Linux | ✅ | 커널 6.17+에서는 내장 rtw89_8852bu. 구형 커널은 커뮤니티 DKMS 드라이버 필요 |
| Ubuntu / Debian | ✅ | Ubuntu 24.04는 HWE 커널 6.17+ 필요(GA 6.8 / HWE 6.14는 커뮤니티 DKMS 드라이버 필요). Debian은 커널 6.17+ 필요 |
| Raspberry Pi 4 / 5 | ⚠️ | Pi에서는 미검증. 커널 6.17 미만은 커뮤니티 DKMS 드라이버 필요 |

---

## 8. 완전한 Soft AP 설정 가이드 (AWUS036ACM) {#setup-guide}

다음은 Raspberry Pi 4에서 AWUS036ACM으로 5GHz Soft AP를 구성하는 완전한 단계별 가이드입니다.

### 1단계: 어댑터 감지 및 드라이버 확인

```bash
# 어댑터 감지 확인
lsusb | grep MediaTek
# 예상: Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U

# 드라이버 로드 확인
dmesg | grep mt76
# 예상: mt76x2u 1-1.4:1.0 wlx00c0ca9821a5: renamed from wlan0

# AP 모드 지원 확인
iw list | grep -A 10 "Supported interface modes"
# 출력에 "* AP"가 포함되어 있는지 확인
```

### 2단계: 필수 패키지 설치

```bash
sudo apt update
sudo apt install -y hostapd dnsmasq iptables
```

### 3단계: hostapd 설정

`/etc/hostapd/hostapd.conf`를 생성합니다:

```ini
interface=wlan0
driver=nl80211
ssid=Yupitek_AP
hw_mode=a                       # a=5GHz, g=2.4GHz
channel=36                      # UNII-1, non-DFS, 가장 안전한 선택
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# HT/VHT 설정 (MT7612U 전용)
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42

# WPA2 + WPA3 혼합 모드
wpa=2
wpa_passphrase=MySecurePassword123
wpa_key_mgmt=WPA-PSK SAE
wpa_pairwise=CCMP
rsn_pairwise=CCMP

auth_algs=1
macaddr_acl=0
ignore_broadcast_ssid=0
```

### 4단계: dnsmasq 설정 (DHCP)

`/etc/dnsmasq.conf`를 생성합니다:

```ini
interface=wlan0
dhcp-range=192.168.10.2,192.168.10.100,255.255.255.0,12h
dhcp-option=3,192.168.10.1
dhcp-option=6,8.8.8.8,8.8.4.4
```

### 5단계: 고정 IP 및 NAT 설정

```bash
# wlan0에 고정 IP 할당
sudo ip addr add 192.168.10.1/24 dev wlan0

# IP 포워딩 활성화
sudo sysctl net.ipv4.ip_forward=1

# NAT 설정 (eth0이 상위 인터페이스라고 가정)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# iptables 규칙 영구 저장
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```

### 6단계: 서비스 시작

```bash
sudo systemctl unmask hostapd
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# 서비스 상태 확인
sudo systemctl status hostapd
sudo systemctl status dnsmasq

# 부팅 시 자동 시작 활성화
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```

완료되면 휴대폰이나 노트북에서 WiFi를 검색해 보세요 — `Yupitek_AP` SSID가 보일 것입니다.

---

## 9. 자주 발생하는 문제 해결 {#troubleshooting}

### Q1: hostapd가 시작 즉시 중단됨

<strong>증상</strong>: `sudo systemctl status hostapd`가 `exited` 또는 `failed`를 표시

<strong>유력한 원인</strong>: `hostapd.conf`에 칩셋이 지원하지 않는 capability 플래그가 포함됨

<strong>해결책</strong>: 불필요한 플래그를 제거하세요. MT7612U(ACM)의 경우, 3절에서 검증된 설정을 사용하는 것이 가장 안전합니다. <strong>다른 칩셋의 ht_capab을 복사하지 마세요.</strong>

---

### Q2: 클라이언트가 연결되지만 인터넷에 접속할 수 없음

<strong>증상</strong>: WiFi 연결됨, IP 할당됨, 그러나 `ping 8.8.8.8`에 응답 없음

<strong>점검 목록</strong>:

```bash
# 1. IP 포워딩 활성화 여부 확인
cat /proc/sys/net/ipv4/ip_forward
# 출력이 1이어야 함

# 2. NAT 규칙 존재 여부 확인
sudo iptables -t nat -L POSTROUTING -v
# MASQUERADE 규칙이 보여야 함

# 3. 상위 인터페이스 동작 확인
ping -I eth0 8.8.8.8
```

---

### Q3: 5GHz AP가 보이지 않거나 불안정함

<strong>가능한 원인</strong>:

1. <strong>DFS 채널(100–144) 사용</strong>: MT7612U / MT7610U는 DFS를 지원하지 않습니다 — UNII-1 채널(36–48)을 사용하세요
2. <strong>송신 출력 부족</strong>: RP-SMA 커넥터에 안테나가 제대로 조여져 있는지 확인하세요
3. <strong>USB 전원 부족</strong>(Raspberry Pi): 공식 5A 전원 공급 장치 또는 외부 전원 공급형 USB 허브를 사용하세요

---

### Q4: Raspberry Pi에서 hostapd가 계속 재시작됨

<strong>증상</strong>: `dmesg`에 잦은 USB 리셋 메시지가 표시됨

<strong>유력한 원인</strong>: USB 포트 전원 부족(특히 AWUS036ACH 고전력 칩셋, 최대 800mA)

<strong>해결책</strong>:
- 공식 Pi 5A 전원 공급 장치 사용
- 외부 전원 공급형 USB 허브 사용
- 어댑터를 USB 3.0 포트에 연결(Pi 4 한정)

---

### Q5: AWUS036AXML/AXM의 WiFi가 갑자기 끊기거나 시작되지 않음

<strong>유력한 원인</strong>: Bluetooth 서브시스템이 WiFi를 간섭(MT7921AUN은 BT 5.2 내장)

<strong>해결책</strong>: Bluetooth 드라이버를 영구적으로 비활성화

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## 10. 기술 심층 분석: VIF, WPA3, DFS 채널 {#technical}

### VIF (가상 인터페이스): 하나의 카드, 여러 역할

VIF(Virtual Interface)는 단일 물리 어댑터가 여러 논리 인터페이스로 동시에 동작하게 합니다. 예를 들어 한 인터페이스는 상위 라우터에 연결(managed mode)하고, 다른 인터페이스는 다른 기기를 위한 AP(master mode)로 동작합니다.

세 가지 일반적인 시나리오:

| 시나리오 | VIF 필요 여부 | 최적 어댑터 |
|----------|--------------|--------------|
| 기본 NAT 라우팅(eth0 상위 + wlan AP) | ❌ 불필요 | AP 가능 어댑터 아무거나 |
| 무선 브리징(WiFi 수신 + WiFi AP 동시) | ✅ 필요 | ACM (MT7612U) |
| Monitor + AP 동시(보안 연구 / Rogue AP) | ✅ 필요 | ACM (MT7612U) |

<strong>VIF 실전 예제 (MT7612U):</strong>

```bash
# 기존 wlan1과 함께 추가 AP 가상 인터페이스 생성
sudo iw phy phy1 interface add ap0 type __ap
sudo ip link set ap0 up
# 이제 wlan1은 상위에 연결하고 ap0은 hostapd를 실행할 수 있음
```

VIF를 완전히 지원하는 것은 MediaTek 커널 내장 드라이버(mt76x2u, mt7921u)뿐입니다. Realtek 커널 외부 드라이버는 사실상 이 기능이 없으므로, AP + Monitor를 동시에 사용하려면 별도의 어댑터 두 개를 써야 합니다.

---

### WPA3 지원 비교

| 칩셋 | 해당 모델 | WPA2 | WPA3 |
|---------|-------------------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ 네이티브 SAE 지원 |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ 네이티브 SAE 지원 |
| RTL8812AU | AWUS036ACH | ✅ | ❌ 지원 표방하나 동작하지 않음 |
| RTL8832BU | AWUS036AX / AXER | ✅ | ✅ 커널 6.17에서 실측 확인 (`sae_pwe=0`, MFP 활성) |

---

### 5GHz Soft AP 채널 선택: DFS 회피

DFS(Dynamic Frequency Selection) 채널(ch100–ch140)은 커널 수준의 레이더 감지가 필요합니다. MT7612U를 비롯한 유사 칩셋은 DFS를 지원하지 않습니다. 5GHz AP 모드에서는 다음을 선택하세요:

| 대역 | 권장 채널 | 이유 |
|------|---------------------|--------|
| <strong>UNII-1</strong> | <strong>36, 40, 44, 48</strong> | 모든 칩셋 지원; 가장 안전한 선택 |
| UNII-2 (DFS) | 52–144 | 대부분 미지원; 권장하지 않음 |
| UNII-3 | 149–165 | 부분 지원(지역에 따라 다름) |

---

## 11. 실전 커뮤니티 사례 {#real-cases}

### 사례 1: RPi4B + AWUS036ACM = 장기 안정 가정용 5GHz AP

<strong>출처</strong>: morrownr/7612u GitHub 지식 베이스
<strong>시나리오</strong>: morrownr는 RPi4B + AWUS036ACM을 가정용 5GHz AP로 장기 운용하며, Pi 내장 2.4GHz와 결합해 듀얼밴드 서비스를 제공
<strong>결과</strong>: 재시작 불필요, 장기 안정 운영, "outstanding" 평가
<strong>설정</strong>: hostapd + dnsmasq + iptables NAT

### 사례 2: RPi3B+ + ACM — 초기 다운, 해결됨

<strong>출처</strong>: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
<strong>문제</strong>: RPi3B+에서 USB 2.0으로 실행 시 hostapd가 다운됨
<strong>근본 원인</strong>: `ht_capab`에 USB 2.0 대역폭 한계에서 지원되지 않는 HT40 플래그가 포함됨
<strong>해결책</strong>: 불필요한 플래그 제거; Kali Linux에서 정상 시작

### 사례 3: Pi PwnBox + AWUS036ACH = Red Team Rogue AP

<strong>출처</strong>: GitHub koutto/pi-pwnbox-rogueap
<strong>시나리오</strong>: RPi3B+ Rogue AP 플랫폼: 하나의 RTL8812AU(AWUS036ACH)는 AP용, 또 다른 RT3070(AWUS036NEH)은 패킷 인젝션 공격용
<strong>핵심 발견</strong>: RTL8812AU는 VIF가 없기 때문에 별도의 어댑터 두 개가 필요했음(단일 카드로 둘 다 처리하는 ACM과 대조됨)

### 사례 4: RPi3B ArchLinux ARM에서 AWUS036AXML 안정 AP

<strong>출처</strong>: [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
<strong>시나리오</strong>: 사용자가 RPi3B ArchLinux aarch64에서 AWUS036AXML을 AP 모드로 성공적으로 운용
<strong>인용</strong>: "It's the most stable mt7921 in my collection."
<strong>핵심 요구사항</strong>: git에서 컴파일한 hostapd + btusb 비활성화

### 사례 5: Pi4에서 AWUS036ACHM(MT7610U, 단종) 풀스피드 AP

<strong>출처</strong>: [GitHub Discussion #31](https://github.com/morrownr/USB-WiFi/discussions/31)
<strong>문제</strong>: 초기 설정에서 링크 속도가 65 Mbps에 불과해 AC 5GHz 풀스피드에 크게 못 미침
<strong>해결책</strong>: 올바른 `vht_oper_chwidth=1`과 `vht_oper_centr_freq_seg0_idx`를 추가; 433 Mbps 링크 속도 달성
<strong>ACM에 대한 시사점</strong>: 동일한 VHT 파라미터 설정은 MT7612U(ACM)에도 똑같이 중요함

---

## 12. 구매 추천 및 최종 결론 {#recommendations}

### 빠른 의사결정 매트릭스

| 등급 | 모델 | 추천 대상 | 한 줄 평 |
|--------|-------|----------|-----------|
| 🥇 <strong>최우선 추천</strong> | <strong>AWUS036ACM</strong> | 모두, 특히 Soft AP를 처음 구축하는 사용자 | 모든 플랫폼에서 안정적, 번거로움 제로 |
| 🥈 사용 가능 | AWUS036ACH | 이미 이 모델을 보유한 사용자 | 드라이버 필요, WPA3 미지원 |
| 🥉 상급자용 | AWUS036AXML | WiFi 6E가 필요하고 설정을 손볼 의향이 있는 사용자 | 6GHz 장점, 수동 조정 필요 |
내장 드라이버; 2.4 / 5 GHz AP, VIF 실측, WPA3는 2.4 GHz에서 실측 |

### 🎯 의사결정 가이드

- <strong>Kali / Ubuntu / Debian / Raspberry Pi 4 또는 5에서 안정적인 Soft AP가 필요한가요?</strong>
  → 두말할 것 없이 <strong>AWUS036ACM</strong>을 선택하세요.

- <strong>이미 AWUS036ACH를 보유하고 있고 Soft AP를 시도하고 싶나요?</strong>
  → 동작하지만 WPA2만 가능하며 드라이버를 설치해야 합니다. 이 제약을 수용할 수 있다면 진행하세요.

- <strong>WiFi 6E(6 GHz 대역)가 필요하고 설정을 손볼 의향이 있나요?</strong>
  → AWUS036AXML — BT 드라이버 비활성화와 커널 ≥ 6.6 LTS 확인을 잊지 마세요.

- <strong>주된 목적이 침투 테스트가 아니라 Soft AP인가요?</strong>
  → 모든 플랫폼에서 광범위한 커뮤니티 검증을 거친 유일한 선택지는 AWUS036ACM입니다.

---

### 결론

Soft AP 구축의 핵심 요소는 WiFi 속도나 안테나 개수가 아니라 <strong>칩셋 드라이버의 AP 모드 지원 여부입니다.</strong>

우리가 조사한 모든 ALFA 제품 중에서, <strong>AWUS036ACM(MT7612U)</strong>은 커널 내장 드라이버, 네이티브 WPA3, VIF 가상 인터페이스, 저전력, 플랫폼 간 안정성을 동시에 만족하는 유일한 어댑터입니다. Soft AP의 황금 표준입니다.

AWUS036ACH(RTL8812AU)는 제약을 수용한다면 동작합니다. AWUS036AXML/AXM(MT7921AUN)은 잠재력이 뛰어나지만 드라이버 성숙도가 아직 발전 중입니다. AWUS036AX/AXER(RTL8832BU)는 커널 6.17 이상에서 내장 드라이버로 잘 동작합니다(AP, VIF, WPA3 실측). 구형 커널에서는 커뮤니티 DKMS 드라이버가 필요합니다.

<strong>Raspberry Pi나 Kali Linux에서 Soft AP를 처음 구성한다면 — ACM을 선택하세요. 후회하지 않을 것입니다.</strong>

---

### 구매 링크

- [AWUS036ACM — Soft AP 최우선 추천](/ko/products/alfa/awus036acm/)
- [AWUS036ACH — 클래식 침투 테스트 어댑터](/ko/products/alfa/awus036ach/)
- [AWUS036AXML — WiFi 6E 트라이밴드 플래그십](/ko/products/alfa/awus036axml/)
- [ALFA Network 전체 제품 라인업](/ko/products/alfa/)

### 더 읽어보기

- [AWUS036ACH vs AWUS036ACM: 칩셋 드라이버 완전 비교](/ko/blog/awus036ach-vs-awus036acm/)
- [Raspberry Pi에서의 AWUS036ACM IBSS & Mesh](/ko/blog/)
- [morrownr/USB-WiFi — 권위 있는 Linux USB WiFi 지식 베이스](https://github.com/morrownr/USB-WiFi) (스타 4,100개 이상)
- [morrownr/7612u — MT7612U 레퍼런스(RPi4B Bridged AP 튜토리얼 포함)](https://github.com/morrownr/7612u)
- [DeepWiki — morrownr/USB-WiFi 자동 큐레이션 지식 베이스](https://deepwiki.com/morrownr/USB-WiFi)

---

### 📚 데이터 출처

이 글은 다음 정보를 종합했습니다:
- <strong>morrownr/USB-WiFi</strong> GitHub 지식 베이스(스타 4,100개 이상), 완전한 iw_list 기록 포함
- <strong>morrownr/7612u</strong> — RPi4B에서의 MT7612U Bridged AP 튜토리얼
- <strong>GitHub issue tracker</strong> — issue #2(ACM AP 설정), #476(AXML AP 테스트), Discussion #31(ACHM 풀스피드 AP)
- <strong>koutto/pi-pwnbox-rogueap</strong> — ALFA 어댑터 RogueAP 구현 사례
- <strong>Rokland</strong> 공인 리셀러 Linux 지원 페이지
- <strong>Lab401</strong> 기술 리뷰 및 2025 침투 테스트 베스트 픽 리포트
- <strong>Raspberry Pi 공식 포럼</strong> — Pi 4/5 USB WiFi 호환성 논의
- <strong>Yopitek 기존 블로그</strong> — ACM 중국 설치 가이드, AXML WiFi 6E 리뷰, Kali Linux 2026 베스트 어댑터

---

{{< faq >}}

> <strong>태그</strong>: #ALFANetwork #SoftAP #WiFiHotspot #hostapd #KaliLinux #Ubuntu #Debian #RaspberryPi #AWUS036ACM #AWUS036ACH #AWUS036AXML #MT7612U #RTL8812AU #MT7921AUN #Yopitek
>
> <strong>작성자</strong>: Yopitek Ltd — ALFA Network 대만 공인 유통사
>
> <strong>면책 조항</strong>: 조사 데이터는 2026년 5월 기준입니다. Linux 커널과 배포판은 계속 발전하므로 드라이버 지원은 새 버전에서 변경될 수 있습니다. 배포 전 대상 플랫폼의 커널 버전과 드라이버 호환성을 확인하세요.
>
> <strong>기술 지원</strong>: Soft AP 설정 문제는 Yopitek 대만 기술 지원으로 문의하세요. 제품 문의: [yupitek.com](https://yupitek.com/ko/).

## 참고 자료

1. [morrownr/USB-WiFi GitHub 지식 베이스](https://github.com/morrownr/USB-WiFi)
2. [hostapd 공식 문서](https://w1.fi/cgit/hostap/)
3. [Linux Wireless mt76 드라이버](https://wireless.wiki.kernel.org/en/users/Drivers/mt76)
4. [Raspberry Pi 공식 문서](https://www.raspberrypi.com/documentation/)
5. [Kali Linux 공식 문서](https://www.kali.org/docs/)
</content>
</invoke>
