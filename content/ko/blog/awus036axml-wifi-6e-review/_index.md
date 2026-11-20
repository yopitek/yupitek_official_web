---
title: "ALFA AWUS036AXML WiFi 6E 리뷰: 2026년 실전 침투 테스트 성능"
description: "ALFA AWUS036AXML WiFi 6E USB 어댑터 심층 리뷰: 사양, Kali Linux 드라이버 설정, 모니터 모드 성능, 6 GHz 대역 스캔, 그리고 AWUS036ACH와의 비교."
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "AWUS036AXML은 어떤 주파수 대역을 지원합니까?"
    answer: "2.4 GHz, 5 GHz, 6 GHz 트라이 밴드를 지원하며 IEEE 802.11ax Wi-Fi 6E를 준수합니다. 보안 연구자가 6 GHz 대역에서 동작할 수 있게 해주는 몇 안 되는 USB 무선 어댑터 중 하나입니다."
  - question: "AWUS036AXML에는 어떤 Linux 커널 버전이 필요합니까?"
    answer: "mt7921u 드라이버는 Linux 5.18부터 메인라인 커널에 병합되었습니다. 6.x 커널을 사용하는 Kali Linux 2024.x / 2025.x에서 문제없이 동작합니다."
  - question: "AWUS036AXML과 AWUS036ACH의 주요 차이점은 무엇입니까?"
    answer: "AWUS036AXML은 MT7921AUN을 사용하여 6 GHz와 Wi-Fi 6E를 지원합니다. AWUS036ACH는 RTL8812AU를 사용하여 듀얼 밴드 Wi-Fi 5만 지원하지만, 드라이버가 더 성숙하고 호환성 범위가 넓습니다."
  - question: "AWUS036AXML은 패킷 인젝션을 지원합니까?"
    answer: "안정적이지 않습니다. 커널 6.16 이전에서는 인젝션이 동작했다는 커뮤니티 보고가 있으나, 자사 stock 커널 6.17 실측에서는 인젝션 테스트가 통과하지 못했습니다(aireplay-ng --test: Found 0 APs / No Answer). 원인은 칩 자체의 한계가 아니라 mac80211 chanctx 회귀입니다. 인젝션이 필요하면 ACH, EACS, ACS, AX를 사용하세요. 모니터, AP, WPA3는 사용 가능하며 패시브 모니터 모드를 권장합니다."
  - question: "AWUS036AXML은 누구에게 적합합니까?"
    answer: "Wi-Fi 6E가 배포된 기업 환경을 평가하는 보안 연구자, 보안 교육 실습실, 그리고 6 GHz 프로토콜 분석을 수행하는 연구자에게 가장 적합합니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036AXML", "wifi-6e", "review", "kali-linux", "MT7921AUN", "6GHz"]
featureimage: "/images/blog/awus036axml-wifi-6e-review.webp"
---
**ALFA AWUS036AXML**은 무선 보안 연구 분야에서 Wi-Fi 6E 시대를 겨냥한 ALFA Network의 제품입니다. **Mediatek MT7921AUN** 칩셋을 기반으로 하며, 2026년 현재 보안 연구자가 **6 GHz 대역**에서 동작할 수 있게 해주는 매우 드문 USB 무선 어댑터 중 하나입니다. 6 GHz 대역은 Wi-Fi 6E 네트워크가 사용하는 가장 최신의 비면허 주파수 할당 대역입니다.

## 제품 개요

{{< tldr >}}
AWUS036AXML은 2.4/5/6 GHz 트라이 밴드와 모니터 모드를 지원하는(패킷 인젝션은 커널 6.16 이전 커뮤니티 보고, stock 커널 6.17 실측 실패) Wi-Fi 6E USB 어댑터입니다. 이 글에서는 사양, Kali Linux 드라이버 설정, 6 GHz 스캔 테스트, 그리고 AWUS036ACH와의 상세 비교를 다룹니다.
{{< /tldr >}}


MediaTek MT7921AUN 칩셋을 탑재한 ALFA AWUS036AXML은 보안 연구자가 6 GHz 대역에서 동작할 수 있게 해주는 몇 안 되는 USB WiFi 어댑터 중 하나입니다. 모니터 모드, AP 모드, WPA3를 지원하며 Linux 커널 5.18 이상이 필요합니다. 패킷 인젝션은 커널 6.16 이전에서 커뮤니티 보고가 있으나 자사 stock 커널 6.17 실측에서는 통과하지 못했습니다(아래 설명 참조).






이것이 중요한 이유는 기업 및 소비자 환경의 Wi-Fi 6E 배포가 이제 널리 확산되었기 때문입니다. 듀얼 밴드(2.4/5 GHz) 어댑터만 갖춘 침투 테스터는 사실상 최신 네트워크 인프라의 한 부류 전체를 보지 못하게 됩니다. AWUS036AXML은 바로 그 공백을 메웁니다.

이 어댑터는 USB-A로 연결되며 USB 버스에서 전적으로 전원을 공급받습니다. 외부 전원이 필요 없습니다. 듀얼 밴드(2.4/5 GHz) 러버 덕 안테나와 함께 제공되며, 범위 확장 테스트를 위해 서드파티 고이득 안테나를 장착할 수 있는 RP-SMA 커넥터를 갖추고 있습니다.

---

## 사양

| 항목 | 값 |
|---|---|
| 칩셋 | Mediatek MT7921AUN |
| 표준 | IEEE 802.11ax (Wi-Fi 6E) |
| 주파수 대역 | 2.4 GHz / 5 GHz / 6 GHz |
| 최대 데이터 전송률 | AX1800 (574 Mbps @ 2.4 GHz, 1201 Mbps @ 5/6 GHz) |
| 인터페이스 | USB-A 3.0 |
| 안테나 커넥터 | RP-SMA (1×) |
| 안테나 (기본 제공) | 2 dBi 듀얼 밴드 러버 덕 |
| USB 소비 전류 | ~900 mA (최대) |
| 크기 | 95 mm × 25 mm × 15 mm (본체) |
| 동작 온도 | 0°C ~ 50°C |
| OS 지원 | Linux (커널 5.18+), Windows 10/11 |
| 모니터 모드 | ✅ 지원 |
| 패킷 인젝션 | ⚠️ 커널 6.16 이전 커뮤니티 보고, 6.17 실측 실패 |

---

## 빌드 품질 및 디자인

AWUS036AXML은 무광 블랙 플라스틱 하우징을 사용하며, 무겁지 않으면서도 견고한 느낌을 줍니다. USB-A 플러그는 금속 칼라로 보강되어 있는데, 이는 현장 작업 중 어댑터를 자주 연결하고 분리할 때 중요한 부분입니다. RP-SMA 커넥터는 적절한 측면 저항을 지니고 있어 표준 안테나의 무게에도 흔들리지 않습니다.

폼 팩터는 콤팩트하고 실용적입니다. 노트북 가방에 편하게 들어가며, 짧은 본체 덕분에 직접 꽂았을 때 USB 포트에 부담을 주지 않습니다. 장기간 현장 배치 시에는 짧은 USB 연장 케이블과 함께 사용하는 것이 좋습니다. 이는 포트에 가해지는 기계적 부담을 줄이고, 최적의 신호를 위해 안테나 위치를 조정할 수 있게 해줍니다.

기본 제공되는 듀얼 밴드 안테나는 사용 가능한 수준이지만 2 dBi로 제한됩니다. 특히 6 GHz 동작의 경우, 기본 안테나는 근거리 테스트에는 충분하지만 RP-SMA 연결로 사용할 수 있는 고이득 대안 제품에는 미치지 못합니다.

---

## Kali Linux 드라이버 설정

이 부분은 보안 연구자에게 가장 중요한 섹션입니다. MT7921AUN 드라이버 상황은 칩셋 출시 이후 상당히 개선되었지만, 여전히 주의가 필요합니다.

### 커널 버전 요구 사항

`mt7921u` 드라이버(USB MT7921 변형용)는 **Linux 커널 5.18**에 도입되었습니다. 현재 커널 버전을 확인하십시오.

```bash
uname -r
```

현재 Kali Linux 2024.x / 2025.x에서 예상되는 출력:

```
6.8.0-kali3-amd64
```

6.x 커널이면 어느 것이든 충분합니다. 이전 커널(5.15 또는 그 이하)을 사용 중이라면 진행하기 전에 Kali를 업데이트하십시오.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### 드라이버 자동 로드 검증

AWUS036AXML을 연결한 후, 커널이 인식했는지 확인하십시오.

```bash
lsusb | grep -i mediatek
```

예상 출력:

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

드라이버 모듈이 로드되었는지 확인하십시오.

```bash
lsmod | grep mt7921
```

예상 출력:

```
mt7921u               28672  0
mt7921_common         98304  1 mt7921u
mt76_connac_lib       65536  2 mt7921u,mt7921_common
mt76                 131072  3 mt7921u,mt7921_common,mt76_connac_lib
mac80211             933888  3 mt7921u,mt7921_common,mt76
```

모듈이 없으면 수동으로 로드하십시오.

```bash
sudo modprobe mt7921u
```

### 무선 인터페이스 검증

인터페이스가 생성되었는지 확인하십시오.

```bash
ip link show | grep wlan
```

`wlan0` 또는 `wlx<mac-address>`와 같은 항목이 보일 것입니다. 해당 기능을 확인하십시오.

```bash
iw phy phy0 info | grep -A5 "Frequencies"
```

6000–7125 MHz 범위의 항목을 찾으십시오. 이것이 보이면 6 GHz 지원이 활성화되었음이 확인됩니다.

### 펌웨어

MT7921AUN은 바이너리 펌웨어 파일을 필요로 합니다. Kali Linux에서는 일반적으로 `firmware-misc-nonfree` 패키지를 통해 설치됩니다.

```bash
sudo apt install firmware-misc-nonfree
```

어댑터가 `lsusb`에서는 열거되지만 무선 인터페이스가 나타나지 않는다면, 펌웨어 파일 누락이 가장 유력한 원인입니다. 펌웨어 로드 오류가 있는지 `dmesg`를 확인하십시오.

```bash
dmesg | grep -i mt7921
```

펌웨어 로드가 성공하면 다음과 같이 보입니다.

```
[    5.420113] mt7921u 1-1.4:1.0: HW/SW Version: 0x8a108a10, Build Time: 20230905153852a
[    5.623841] mt7921u 1-1.4:1.0: WM Firmware Version: ____010000, Build Time: 20230905153852
```

오류가 발생하면 다음과 같이 보입니다.

```
[    5.312441] mt7921u 1-1.4:1.0: Direct firmware load for mediatek/WIFI_MT7961_patch_mcu_1_2_hdr.bin failed
```

펌웨어 로드 실패가 보이면, Linux 펌웨어 저장소에서 펌웨어를 수동으로 다운로드하여 `/lib/firmware/mediatek/`에 복사하십시오.

---

## 모니터 모드 및 패킷 인젝션

{{< alert "triangle-exclamation" >}}
**알려진 드라이버 제약:** AWUS036AXML이 사용하는 mt7921u 드라이버는 **액티브 모니터 모드**에서 확인된 문제가 있습니다. `airodump-ng`와 같은 도구가 액티브 프로브 요청을 전송할 때 드라이버가 크래시하거나 인터페이스를 리셋할 수 있습니다. **패시브 모니터 모드**만 사용하십시오. 이 어댑터에서 모니터 모드 중 액티브 인젝션은 피하십시오. 이는 하드웨어 결함이 아니라 커널 드라이버 문제입니다.
{{< /alert >}}

### 모니터 모드 활성화

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

검증:

```bash
iwconfig wlan0mon
```

예상 출력:

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
```

### 패킷 인젝션 테스트

```bash
sudo aireplay-ng --test wlan0mon
```

커널 6.16 이전의 커뮤니티 보고에서는 이 어댑터로 인젝션이 동작했습니다. 그러나 자사 stock 커널 6.17 실측에서는 `aireplay-ng --test`가 통과하지 못해(Found 0 APs / No Answer) deauth나 핸드셰이크 캡처가 불가능했습니다. 원인은 칩 자체의 한계가 아니라 커널 6.16 이후의 mac80211 chanctx 회귀이며, 커뮤니티 patched 드라이버로는 인젝션이 동작하지만 펌웨어가 전송 속도를 고정합니다(1/6 Mbps, HT/VHT 인젝션 불가). 인젝션이 필요하면 ACH, EACS, ACS, AX를 사용하세요.

---

## 6 GHz 대역 스캔

{{< alert "circle-info" >}}
**규제 관련 참고:** 6 GHz 대역(Wi-Fi 6E)은 대만을 포함한 여러 국가에서 규제 제약을 받습니다. 이 섹션에서 설명하는 모든 작업은 **승인된 테스트 환경에서만** 사용하도록 의도된 것입니다.
{{< /alert >}}

6 GHz 대역은 Wi-Fi 6E 네트워크가 독점적으로 동작하는 영역입니다. 이 대역을 스캔하려면 어댑터와 드라이버가 모두 이를 지원해야 합니다.

### airodump-ng로 6 GHz 네트워크 스캔

```bash
sudo airodump-ng --band 6 wlan0mon
```

또는 세 대역을 동시에 스캔:

```bash
sudo airodump-ng --band abg wlan0mon
```

> **참고:** `--band 6` 플래그는 airodump-ng가 6 GHz 스펙트럼을 스캔하도록 지시합니다. 모든 버전의 airodump-ng가 이 플래그를 지원하는 것은 아니므로, aircrack-ng 1.7 이상을 실행하고 있는지 확인하십시오.

### 예상 출력 (6 GHz 네트워크가 보이는 경우)

```
 CH 37 ][ Elapsed: 12 s ][ 2026-03-23 09:42

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 AA:BB:CC:11:22:33  -58       12        0    0  37  540   WPA3 CCMP   SAE  Enterprise6E
 DD:EE:FF:44:55:66  -71        8        0    0  53  270   WPA3 CCMP   SAE  HomeWiFi6E
```

6 GHz 대역의 채널 번호는 1부터 233까지의 범위를 가집니다(비중첩: 1, 5, 9, 13, ...). 이러한 채널에서 AP가 보이면 6 GHz 스캔이 동작하고 있음이 확인됩니다.

### iw 스캔 (대안)

```bash
sudo iw dev wlan0mon scan | grep -E "BSS|SSID|freq|signal"
```

이는 MHz 단위의 주파수를 포함하는 더 상세한 출력을 생성하므로, 6 GHz 네트워크(5925 MHz를 초과하는 주파수)를 즉시 식별할 수 있게 해줍니다.

---

## 실전 성능

### 신호 캡처 품질

혼합 환경 테스트(여러 2.4 GHz, 5 GHz, 6 GHz 네트워크가 있는 사무실 건물)에서, AWUS036AXML은 모니터 모드 활성화 외에 별도의 구성 변경 없이 세 대역 모두에서 비콘 프레임을 캡처했습니다. 가장 주목할 만한 결과는 6 GHz 캡처였습니다. RTL8812AU나 MT7612U 기반의 경쟁 어댑터는 이러한 네트워크를 아예 보지 못합니다.

표준 사무실 벽 두 개를 통과한 15미터 거리에서, 6 GHz 신호 강도는 대상 AP의 송신 출력에 따라 -65에서 -78 dBm 사이로 측정되었습니다. 이는 핸드셰이크 캡처에는 충분하지만 범위 확장 테스트에는 이상적이지 않습니다. 더 높은 이득의 외장 안테나로 교체하자 결과가 약 8–10 dBm 개선되었습니다.

### 2.4 및 5 GHz 범위

레거시 대역에서의 성능은 AWUS036ACM(MT7612U)과 동등하거나 약간 더 뛰어납니다. MT7921AUN의 AX 기능이 AC 세대 어댑터 대비 침투 테스트에서 직접적인 이점을 제공하지는 않지만, 최신 커널에서의 더 깔끔한 드라이버 구현 덕분에 장시간 실행되는 airodump-ng 세션 중 캡처 드롭이 더 적습니다.

### 채널 호핑 속도

airodump-ng 채널 호핑을 활성화한 광역 정찰 중에, AWUS036AXML은 세 대역 전반에 걸쳐 허용 가능한 머무름 시간(dwell time)을 유지합니다. 6 GHz 채널을 포함할 때는 채널 범위가 더 넓어 약간의 오버헤드가 있지만, 이는 대부분의 사용 사례에서 정찰 품질에 유의미한 영향을 주지 않습니다.

---

## 장단점

| 장점 | 단점 |
|---|---|
| Kali Linux에서 안정적인 6 GHz 지원을 제공하는 유일한 USB 어댑터 | 커널 5.18+ 필요(오래된 Kali 설치는 업데이트 필요) |
| 완전한 모니터 모드, AP, WPA3 지원 | MT7921AUN 드라이버는 비교적 신규이며 엣지 케이스가 존재할 수 있음. stock 커널 6.17에서 인젝션 실패 |
| MT76 드라이버가 Linux 커널에 업스트림으로 포함됨 | 기본 제공 안테나가 2 dBi로 제한됨 |
| 현행 Kali 2024.x / 2025.x 커널에서 안정적 | 고이득 안테나 없이는 6 GHz 범위가 5 GHz 대비 제한적 |
| USB-A 3.0 — 테스트용 노트북과 폭넓게 호환 | 단일 안테나, 캡처 다이버시티를 위한 MIMO 없음 |
| 안테나 업그레이드를 위한 RP-SMA 커넥터 | 듀얼 밴드 대안보다 약간 높은 가격 |

---

## 비교: AWUS036AXML vs AWUS036ACH

| 기능 | AWUS036AXML | AWUS036ACH |
|---|---|---|
| 칩셋 | MT7921AUN | RTL8812AU |
| Wi-Fi 표준 | 802.11ax (Wi-Fi 6E) | 802.11ac (Wi-Fi 5) |
| 대역 | 2.4 / 5 / 6 GHz | 2.4 / 5 GHz |
| 모니터 모드 | ✅ | ✅ |
| 패킷 인젝션 | ⚠️ 커널 6.17 실측 실패 | ✅ |
| 커널 드라이버 | mt7921u (커널 내장, 5.18+) | rtl8812au (아웃오브트리, 매우 안정적) |
| 드라이버 성숙도 | 비교적 신규, 활발히 개발 중 | 성숙, 2017년경부터 검증됨 |
| 6 GHz 지원 | ✅ | ❌ |
| 안테나 커넥터 | 1× RP-SMA | 2× RP-SMA |
| 적합 용도 | Wi-Fi 6E 대상 환경 | 최대 호환성, 검증된 안정성 |

**결론:** 대상 환경에 Wi-Fi 6E 네트워크가 포함된다면 — 그리고 2026년 현재 많은 기업 환경이 그러합니다 — AWUS036AXML이 올바른 도구입니다. 드라이버는 비교적 신규이지만 MT76 프로젝트는 Linux 커널 커뮤니티에 의해 잘 유지 관리되고 있습니다. 레거시 및 최신 듀얼 밴드 네트워크에 대해 가장 검증되고 호환성이 넓은 옵션이 필요하다면, AWUS036ACH는 수년간의 검증된 현장 사용 실적을 바탕으로 여전히 훌륭한 선택입니다.

많은 전문 침투 테스터는 두 제품을 모두 휴대합니다. 안정적인 듀얼 밴드 작업에는 AWUS036ACH를, Wi-Fi 6E 인프라가 있는 환경에는 AWUS036AXML을 구체적으로 사용합니다.

---

## AWUS036AXML은 누가 구매해야 하는가

**기업 환경을 대상으로 하는 보안 연구자.** Wi-Fi 6E 인프라를 배포한 대규모 조직이 점점 더 흔해지고 있습니다. 6 GHz를 지원하는 어댑터가 없으면 무선 평가가 불완전해지며, 상당 부분의 클라이언트 및 AP 활동을 놓치게 됩니다.

**실습실 및 교육 시설.** 무선 보안을 가르치면서 학생들이 6 GHz 대역 운용을 포함한 현행 Wi-Fi 기술의 상태에 익숙해지기를 원한다면, AWUS036AXML이 적절한 교육 도구입니다.

**Wi-Fi 6E 프로토콜 분석을 수행하는 연구자.** 모니터 모드와 6 GHz 접근의 조합(stock 커널 6.17에서는 인젝션 불가)은 AWUS036AXML을 6 GHz 네트워크에서의 WPA3-SAE 동작, 6 GHz BSS 컬러링, 멀티링크 운용(MLO) 프레임 분석을 연구하기 위한 유일한 실용적 USB 옵션으로 만듭니다.

**미래 대비.** 2026년에 보안 연구용 무선 어댑터를 구매하면서 Wi-Fi 6E 도입이 계속 가속화됨에 따라 그 관련성을 유지하기를 원한다면, AWUS036AXML이 미래 지향적인 선택입니다.

---

{{< faq >}}

ALFA AWUS036AXML은 대만 공식 ALFA Network 총판인 [Yopitek](/ko/products/alfa/awus036axml/)에서 구매하실 수 있습니다. Yopitek을 통해 구매하면 제조사 보증과 현지 기술 지원이 포함된 정품 NCC 인증 제품을 받으실 수 있습니다.

## 참고 문헌

1. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
2. [MediaTek MT7921 칩셋 정보](https://www.mediatek.com/products/networking-and-connectivity)
3. [Linux Kernel mt76 드라이버](https://wireless.wiki.kernel.org/en/users/drivers/mediatek)
4. [aircrack-ng 툴킷](https://www.aircrack-ng.org/)
5. [Wi-Fi Alliance Wi-Fi 6E 인증](https://www.wi-fi.org/discover-wi-fi/wi-fi-6e)
