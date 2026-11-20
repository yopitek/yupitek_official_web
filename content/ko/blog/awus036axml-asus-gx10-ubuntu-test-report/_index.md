---
title: "AWUS036AXML 실측: Wi-Fi 6 + 블루투스 복합 카드의 ASUS GX10(ARM64 / Ubuntu 24.04) —— AP 안정, 인젝션 실패에 대한 정직한 리포트"
slug: awus036axml-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axml-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axml
  - mt7921
  - mt7921u
  - wifi-6
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - ap-mode
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036AXML(Wi-Fi+블루투스)을 ASUS GX10 / Ubuntu 24.04 ARM64에서 실측: AP, WPA3, monitor는 사용 가능하지만 injection 실패, handshake 캡처 불가로 침투 테스트에는 권장하지 않음."
faq:
  - question: "AWUS036AXML으로 패킷 인젝션(packet injection)을 할 수 있나요?"
    answer: "우리의 테스트 플랫폼(ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia)에서는 불가능합니다. aireplay-ng --test가 No Answer, Found 0 APs를 보고하고, 지정 AP를 AP별로 테스트해도 No such BSSID available만 나옵니다. 일반 스캔에서는 해당 AP가 보이는데도(약 -54 dBm) 인젝션 도구 상황에서는 그 beacon을 수신하지 못해, deauth와 handshake 캡처(0건) 모두 사용할 수 없습니다. 근본 원인은 kernel 6.16+의 mac80211 chanctx 회귀(regression)이며, 칩셋이 선천적으로 인젝션을 못 하는 것이 아닙니다. AWUS036AXM도 결과가 동일합니다. 인젝션이 필요하면 AWUS036EACS, ACH, ACS를 선택하세요."
  - question: "AWUS036AXML의 블루투스는 Ubuntu에서 사용할 수 있나요?"
    answer: "본 장비 실측에서 블루투스는 사용 가능합니다. bluetoothctl / hciconfig로 hci 컨트롤러가 UP임을 확인했고, BLE와 클래식 블루투스 기기를 스캔할 수 있으며, Wi-Fi와 블루투스를 동시에 사용할 수 있습니다(공존). 이 제품은 Wi-Fi+블루투스 복합 장치입니다. 참고: 다시 꽂을 때 가끔 WiFi probe에서 멈춰 wlx 인터페이스가 생성되지 않는데, 다른 USB 포트에 다시 꽂으면 복구됩니다."
  - question: "AWUS036AXML은 Ubuntu 24.04에서 드라이버를 따로 설치해야 하나요?"
    answer: "필요 없습니다. mt7921u 드라이버는 kernel 6.17에 내장되어 있어, 꽂으면 dmesg에서 mt7921u가 인터페이스를 wlx 더하기 MAC으로 개명하는 것을 볼 수 있습니다(USB ID 0e8d:7961). DKMS도 컴파일도 불필요합니다. 드라이버는 IBSS와 mesh 모드를 제공하지 않습니다."
  - question: "AWUS036AXML으로 AP를 열 수 있나요? WPA3를 지원하나요?"
    answer: "가능합니다. 이것이 가장 안정적인 용도입니다. 2.4 GHz(802.11n, MCS 10)와 5 GHz VHT80(VHT-NSS2) 모두 iPhone이 접속해 authorized되었고, WPA3-SAE는 sae_pwe=0으로 iPhone 15 Pro가 접속했으며(MFP: yes, 2.4 GHz와 6 GHz에서 실측했고 5 GHz는 미실측), STA+AP 병행 시 STA 측 ping은 약 4.4 ms입니다. Wi-Fi 6 칩셋으로 포지셔닝되지만, 본 장비에서는 6 GHz band도 별도로 실측해 사용 가능했습니다(6135 MHz AP를 직접 구축, iPhone 15 Pro가 802.11ax로 접속해 IP 획득)."
  - question: "AWUS036AXML과 AWUS036AXM은 무엇이 다르고 어느 것을 골라야 하나요?"
    answer: "이 플랫폼에서 두 카드의 Wi-Fi 동작은 동일합니다. 같은 mt7921u를 쓰고, injection도 똑같이 실패하며, monitor 수신도 똑같이 약하고, AP, WPA3, VIF도 똑같이 사용 가능합니다. 차이는 AXML에 블루투스가 추가되었고(본 장비 실측 사용 가능) 본 장비에서 6 GHz band를 실측해 사용 가능하다는 점이며, AXM의 블루투스와 6 GHz는 이번 회차에서 별도로 실측하지 않았습니다. 순수 AP나 일반 접속이면 어느 쪽을 골라도 되지만, injection이나 handshake가 필요하면 두 카드 모두 선택하지 마세요."
draft: false
---

{{< tldr >}}AWUS036AXML은 ASUS GX10 / Ubuntu 24.04 ARM64에서 AP, WPA3, VIF와 수동 monitor는 사용 가능하고, 블루투스와 6 GHz band도 본 장비 실측에서 사용 가능하지만, injection은 실측 실패(No Answer / Found 0 APs)로 deauth도 handshake 캡처도 불가능하여 침투 테스트에는 권장하지 않습니다. 순수 AP와 일반 접속 용도로 포지셔닝합니다.{{< /tldr >}}

ALFA AWUS036AXML은 이번 9종 랜카드 중 유일한 "MediaTek Wi-Fi 6 + 블루투스" 복합 모델입니다. 블루투스가 없는 AWUS036AXM과 동일 세대 칩셋(MT7921, `mt7921u` 드라이버 사용)이며, 차이는 블루투스 한 조가 추가된 것뿐입니다. 고객이 가장 자주 묻는 것은 역시 그 세 가지입니다. monitor로 들어갈 수 있는가? injection이 되는가? AP를 구축할 수 있는가? 이 글은 AWUS036AXML을 따로 떼어, ASUS GX10(ARM64)에 Ubuntu 24.04를 조합해 항목별로 실측하고, 할 수 있는 것과 할 수 없는 것을 한 번에 분명히 밝힙니다. 특히 가장 핵심적인 제약은: **injection이 이 플랫폼에서 실패한다**는 것입니다.

먼저 포지셔닝을 분명히 하면: 아래 모든 측정은 Yupitek 본인 소유 장비, 본인 소유 사무실 Wi-Fi(SSID `YUPITEK`), 본인 소유 테스트용 스마트폰(iPhone 7 Plus, WPA3는 별도로 iPhone 15 Pro로 재검증)에서 완료했습니다. 이것은 유통사가 제품 호환성과 성능 경계를 검증하는 하드웨어 검증이지, 제3자 네트워크에 대한 조작 교육이 아닙니다. 본문의 monitor, AP, injection 자체 테스트는 전부 본인 소유 폐쇄 환경에서 본인 소유 기기를 대상으로 진행했습니다.

## 1. 이 카드와 테스트 플랫폼

- **연산 플랫폼**: ASUS GX10(ARM64 / aarch64)
- **운영체제**: Ubuntu 24.04 LTS
- **커널 버전**: kernel 6.17.0-1014-nvidia
- **피측정 랜카드**: ALFA AWUS036AXML(MediaTek MT7921AUN, Wi-Fi 6 / 2x2 / +BT)
- **테스트 기기**: Apple iPhone 7 Plus(WPA3-SAE는 별도로 iPhone 15 Pro로 재검증)
- **테스트 환경**: 본인 소유 사무실 Wi-Fi, SSID `YUPITEK`, 2.4GHz ch5 / 5GHz ch36, ch157
- **테스트 기간**: 2026-11-16 ~ 2026-11-18 실기 측정

모든 결과는 실제로 측정한 수치나 상태로 기록했으며 사양서로 추측하지 않았습니다. MAC 주소는 출력에서 `xx`로 가렸습니다.

## 2. 하드웨어와 드라이버: MT7921AUN, 꽂으면 바로 사용

| 항목 | 사양 |
|---|---|
| 모델명 | AWUS036AXML |
| 칩셋 | MediaTek MT7921AUN |
| USB ID | `0e8d:7961`(MediaTek Inc. Wireless_Device) |
| in-kernel 드라이버 | `mt7921u` |
| 세대 / 스트림 | Wi-Fi 6 / 2x2(2T2R) |
| 블루투스 | 있음(BT + WiFi 복합 장치; 본 장비 실측에서 hci 컨트롤러 UP, BLE와 클래식 블루투스 기기 스캔 가능, WiFi+BT 공존) |
| USB 열거 | USB 3 |
| 인터페이스 명명 | `wlx<MAC>`(예: `wlx00c0cabd65b9`) |

인식 방법은 매우 직접적입니다. 꽂은 뒤 `lsusb`로 MediaTek의 USB ID를 보고, `dmesg`로 `mt7921u`가 적재되어 인터페이스를 개명하는 것을 봅니다:

```bash
lsusb | grep 0e8d:7961
# Bus 004 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device

sudo dmesg | grep mt7921u | tail -1
# mt7921u 4-1:1.3 wlx00c0cabd65b9: renamed from wlan0
```

핵심은 두 가지입니다. 첫째는 컴파일 불필요입니다. AWUS036AXML은 kernel 6.17에 내장된 `mt7921u` 드라이버를 쓰므로 꽂자마자 인식되며, aarch64에서 어떠한 out-of-tree DKMS 모듈도 다룰 필요가 없어 ARM64 플랫폼에서 특히 손이 덜 갑니다. 둘째는 USB 3으로 열거된다는 점입니다(이전 세대 일부 모델의 OTG 케이블은 USB 2.0에 불과). 전송 대역폭이 병목이 아닙니다.

자주 오해되는 점 하나를 보태면: AWUS036AXML은 Wi-Fi 6(6E 아님) 칩셋으로 포지셔닝되지만, **본 장비 실측에서 6 GHz band를 사용할 수 있었습니다** —— 6135 MHz AP를 직접 구축하자 iPhone 15 Pro가 802.11ax로 접속해 IP를 획득했습니다. 또한 블루투스도 실측 사용 가능합니다. `hciconfig` / `bluetoothctl`로 hci 컨트롤러 상태가 UP임을 확인했고, BLE와 클래식 블루투스 기기를 스캔할 수 있으며, Wi-Fi와 블루투스가 동시에 작동합니다(공존).

지원 인터페이스 모드를 다시 조회하면, 제품 선정에 의미 있는 세부 사항 하나가 보입니다. 바로 IBSS도, mesh point도 없다는 점입니다:

```bash
iw phy <phyN> info | sed -n '/Supported interface modes/,/Band 1/p'
```
```
Supported interface modes:
    * managed
    * AP
    * AP/VLAN
    * monitor
    * P2P-client / P2P-GO / P2P-device
```

즉, managed, AP, monitor, P2P는 모두 있지만, ad-hoc(IBSS)와 802.11s mesh 이 두 모드는 `mt7921u` 드라이버가 아예 제공하지 않습니다. mesh / IBSS 실험을 해야 하는 고객은 이 카드를 바로 제외하세요(`mt76`의 ACM / ACHM을 보세요).

## 3. 실측 성능: Monitor / AP / WPA3, 그리고 injection의 정직한 한계

핵심 성능을 한 번에 보겠습니다:

| 성능 | 2.4GHz | 5GHz | 설명 |
|---|---|---|---|
| Monitor | ✅(약함) | ✅(약함) | beacon 측정 가능; client / data 패킷 자주 놓침 |
| **Injection** | ❌ **실패** | ❌ **실패** | `aireplay-ng` 인젝션 / deauth 작동 불가; 근본 원인은 kernel 6.16+ mac80211 chanctx 회귀(regression)(칩셋 선천적 문제 아님) |
| AP 핫스팟 | ✅ 802.11n 포함 | ✅ VHT80(80MHz) | iPhone 7 Plus 접속, `authorized: yes` |
| WPA3-SAE | ✅ | 미실측 | iPhone 15 Pro 접속, `MFP: yes`(`sae_pwe=0`), 6 GHz(ch37, 6135 MHz)에서도 실측 |

### Monitor: 두 밴드 모두 진입 가능하나 수신 약함

AWUS036AXML은 2.4GHz(ch1 / 6 / 11)와 5GHz(ch36 / 149 / 157) 모두 monitor mode로 진입할 수 있고, beacon 측정에 문제가 없습니다. 설정 흐름은 표준 `iw dev` 4단계입니다:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36     # 2.4GHz는 set channel 6으로 변경
```

정직하게 말하면: 이 카드의 monitor 수신은 같은 회차의 MT7612U(ACM)나 Wi-Fi 6의 AXER보다 확연히 약합니다. beacon은 잡히지만 client / data 패킷을 자주 놓치며, `airodump-ng`로 채널 호핑 스캔할 때 일부 AP를 놓치기 쉽습니다. 실무적으로는 채널 호핑보다 단일 채널 고정(`-c <ch>`)을 권장하며, 그러면 수확이 좀 더 안정적입니다. 또한 monitor 모드에서 `iw info`가 txpower를 3 dBm으로만 보고하는데, 이는 **보고상의 착시**(하드웨어 실제 TX는 약 20–23 dBm, `txpower_sku`로 검증됨)이지 출력이 실제로 3 dBm으로 눌린 것이 아닙니다. 이 점은 뒤의 "주의사항"에서 함께 다룹니다.

### AP 핫스팟: 2.4GHz HT 포함, 5GHz VHT80 가능

AP는 AWUS036AXML에서 가장 안정적인 부분입니다. 2.4GHz는 802.11n(HT)을 그대로 유지할 수 있어, 단일 안테나의 ACHM처럼 HT를 끌 필요가 없습니다. 5GHz는 VHT 80MHz까지 열 수 있습니다. 두 밴드 모두 실측에서 iPhone 7 Plus가 접속해 `authorized: yes`였습니다.

5GHz VHT80의 hostapd 핵심 설정:

```
hw_mode=a
channel=36
ieee80211ac=1
ht_capab=[HT40+][SHORT-GI-20][SHORT-GI-40]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42
vht_capab=[SHORT-GI-80]
```

실측 접속 후는 VHT-NSS2, 80MHz였습니다. 2.4GHz 버전은 `hw_mode`를 `g`로, `channel=6`으로 바꾸고 `ieee80211n=1`과 `ht_capab=[HT20]`을 유지하면 되며, iPhone 접속은 MCS 10(802.11n)이었습니다.

### WPA3-SAE: 사용 가능, sae_pwe=0 잊지 마세요

AP의 `wpa_key_mgmt`를 `SAE`로 바꾸고 `ieee80211w=2`와 `sae_pwe=0`을 추가하면 WPA3-SAE를 열 수 있습니다. 실측에서 iPhone 15 Pro가 2.4 GHz(및 6 GHz)에서 접속해(5 GHz는 미실측) `authorized: yes`, `MFP: yes`였습니다. `sae_pwe=0`은 구형 iPhone과 호환하기 위한 것으로, 이 점은 ACHM의 지뢰와 같으며 `sae_pwe=2`일 때 구형 기기가 자주 접속하지 못합니다.

### VIF: 한쪽으로 인터넷, 한쪽으로 핫스팟, 가능

AWUS036AXML은 다중 인터페이스 병존을 지원합니다. AP VIF(다른 MAC, unmanage)를 만들고, 메인 인터페이스는 Wi-Fi에 접속하고, 같은 채널에서 AP를 열었더니, 실측에서 iPhone 7 Plus가 AP VIF에 접속할 때 STA의 `YUPITEK`에 대한 ping은 4.4 ms였습니다. "한 카드로 동시에 인터넷에 접속하면서 핫스팟을 공유하는" 요구는 성립합니다.

### 정직한 한계: injection이 이 플랫폼에서 실패

이것이 AWUS036AXML(그리고 블루투스 없는 쌍둥이 AXM)에서 가장 분명히 밝혀야 할 항목입니다. ASUS GX10 + kernel 6.17에서 본인 소유 테스트 환경을 대상으로 injection 자체 테스트를 한 결과는 실패입니다:

```bash
sudo aireplay-ng --test $IF
```
```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

자가 AP의 BSSID를 지정해 AP별로 테스트해도 `No such BSSID available`만 반환됩니다. 핵심은: 일반 스캔에서는 분명히 해당 AP가 보이는데도(신호 -54 dBm), 인젝션 도구 상황에 들어가면 이 카드가 대상의 beacon을 "듣지 못하고", deauth를 내보내지 못하며, 4-way handshake 캡처 수가 0이라는 점입니다.

이것은 파라미터를 제대로 조정하지 않은 것도, 개별 랜카드의 고장도 아닙니다. 진짜 근본 원인은 **소프트웨어 레이어**에 있습니다. kernel 6.16 이후 mac80211의 channel context(chanctx)에 회귀(regression)가 발생해, stock 드라이버가 인젝션 상황에서 대상 beacon을 수신하지 못하고 `aireplay-ng`가 그래서 `No Answer`로 판정하며, **MT7921 칩셋이 선천적으로 인젝션을 못 하는 것이 아닙니다.** 현상은 morrownr/USB-WiFi issue #387에 기록되어 있고, 근본 원인 분석은 morrownr/mt76 issue #18에 있습니다. 커뮤니티 실측에 따르면 같은 모델에서 git / patched 드라이버로 active monitor와 인젝션을 작동시킬 수 있지만, MT7921 firmware는 여전히 인젝션을 1 Mbps / 6 Mbps 기본 속도에 고정하여 HT / VHT로 인젝션할 수 없습니다. AXM과 AXML 두 모델은 **stock kernel 6.17**에서 똑같이 당첨되었으며, 2026-11-18 기준 파라미터 조정으로 해결할 수 없습니다.

따라서 injection이 얽히는 능력, 즉 deauth, WPA handshake 캡처, 인젝션을 전제로 한 침투 테스트는 AWUS036AXML이 이 플랫폼에서 모두 할 수 없습니다. 이런 용도는 실측 인젝션이 가능한 모델로 바꾸세요(아래 제품 선정 참고).

### 기타 고급 모드 일람

| 고급 기능 | 상태 | 설명 |
|---|---|---|
| VIF(STA + AP 병존) | ✅ | 같은 채널 ch36; iPhone 접속 시 STA ping 4.4 ms |
| WPA handshake 캡처 | ❌ | 인젝션 실패 → deauth 전송 불가, handshake 0 |
| Active monitor | 🟡 | `set monitor active`는 수용되나 ACK 미검증 |
| Ad-hoc(IBSS) | N/A | `mt7921u` 드라이버에 이 모드 없음 |
| Mesh(802.11s) | N/A | `mt7921u` 드라이버에 이 모드 없음 |
| Wi-Fi Direct(P2P) | ⬜ | 드라이버는 지원 선언, 두 번째 장비 필요, 건너뜀 |

## 4. 블루투스 복합 주의사항과 적용 / 부적용 용도

### BT + WiFi 복합 카드의 실무 부작용

AWUS036AXML은 블루투스를 내장하며, 이번 회차의 두 복합 장치 중 하나입니다(다른 하나는 Realtek의 EACS). 블루투스는 본 장비에서 이미 실측 사용 가능합니다(hci 컨트롤러 UP, BLE와 클래식 블루투스 기기 스캔 가능, Wi-Fi와 공존, 앞 내용 참조). 여기서는 복합 장치의 실무 부작용 하나를 보탭니다. 다시 꽂을 때 가끔 WiFi probe에서 멈춰 `wlx` 인터페이스가 생성되지 않는데, 증상은 뽑았다 꽂은 뒤 `ls /sys/class/net`에 랜카드가 좀처럼 나타나지 않는 것입니다. 해법은 매우 단순합니다. **다른 USB 포트**에 다시 꽂으면 보통 정상적으로 열거됩니다.

기억해 둘 또 하나의 작은 동작: AP 모드에서 스마트폰이 갑자기 당신의 SSID를 못 찾으면, 랜카드를 **한 번 뽑았다 꽂아** 리셋하면 되고, 설정을 바꿀 필요가 없습니다.(참고: 앞서 언급한 monitor가 보고하는 3 dBm은 착시이지 실제 출력이 아니므로, SSID가 사라지는 주원인이 아닙니다.)

### 플랫폼 안전 수칙

- 절대로 `airmon-ng check kill`을 실행하지 마세요. NetworkManager를 꺼버려 GX10 전체가 인터넷에서 끊깁니다. 조작할 때는 외장 `wlx*` 인터페이스만 다루고, 내장 외부 인터넷 메인 라인은 건드리지 마세요.
- `hcxdumptool 8.x`는 이 장비에서 `failed to arm`이 발생합니다(2.4 GHz의 AWUS036EACS는 예외이며, GX10의 3밴드 내장 카드 열거 충돌 + 드라이버에 active-monitor 없음). 이는 플랫폼 전체의 공통 문제로 AXML과 무관합니다. 비슷한 기능이 필요하면 `airodump-ng`와 다른 aircrack-ng 도구를 조합해 쓰세요.
- ARM64 보충: `aircrack-ng`는 소스에서 컴파일해야 하고, `wifite`는 apt 의존성 충돌을 우회하기 위해 git 버전을 권장합니다.

### 적용 / 부적용 일람

| 적용 시나리오 | 부적용 시나리오 |
|---|---|
| 순수 AP / 핫스팟(2.4G HT 포함, 5G VHT80) | injection / deauth |
| WPA3-SAE 핫스팟 | WPA handshake 캡처 |
| 일반 managed 접속 | 인젝션을 전제로 한 침투 테스트 주력 카드 |
| 수동 monitor / 스펙트럼 조사(단일 채널 고정) | mesh / IBSS 실험 |
| STA + AP 병존(VIF, 한쪽 인터넷 한쪽 공유) | 강한 수신이 필요한 장거리 측정 |

## 5. 제품 선정 제안(종합표로 연결)

AWUS036AXML을 9종의 전체 그림 속에 다시 놓고 보면, 포지셔닝이 매우 분명합니다. MediaTek은 접속이 안정적이고, 컴파일 불필요이며, 두 밴드 AP 모두 VHT80을 올릴 수 있어 유능한 "순수 접속 / 순수 AP" 카드입니다. injection이 조금이라도 닿으면 그의 무대가 아닙니다.

| 요구 | 권장 모델 |
|---|---|
| 순수 AP / 일반 접속(인젝션 불필요) | **AWUS036AXML / AWUS036AXM**(본 카드 적용) |
| injection + handshake(침투 테스트) | AWUS036EACS / AWUS036ACH / AWUS036ACS |
| mesh / IBSS 실험 | AWUS036ACM / AWUS036ACHM |
| 최강 수신 / 장거리 monitor | AWUS036AXER / AWUS036ACH |

9종 사이에서 고민하고 있다면, 완전한 Monitor / Injection / AP / WPA3 전체 매트릭스와 용도별 제품 선정은 종합표를 보세요:

- [2026 가장 완전한 실측: 9종 ALFA 무선 랜카드의 ASUS GX10 전체 매트릭스](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

한마디 지뢰 회피: **injection이나 handshake가 필요하면 AWUS036AXML / AWUS036AXM을 선택하지 마세요.** 순수 접속이나 핫스팟 구축이면 매우 쓸 만합니다.

## 자주 묻는 질문(FAQ)

**Q1. AWUS036AXML으로 패킷 인젝션(packet injection)을 할 수 있나요?**
우리의 테스트 플랫폼(ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia)에서는 불가능합니다. `aireplay-ng --test`가 `No Answer`, `Found 0 APs`를 보고하고, 지정 AP를 AP별로 테스트해도 `No such BSSID available`만 나옵니다. 일반 스캔에서는 해당 AP가 보이는데도(약 -54 dBm) 인젝션 도구 상황에서는 그 beacon을 수신하지 못해, deauth와 handshake 캡처(0건) 모두 사용할 수 없습니다. 근본 원인은 kernel 6.16+의 mac80211 chanctx 회귀이며, 칩셋이 선천적으로 인젝션을 못 하는 것이 아닙니다. AWUS036AXM도 결과가 동일합니다. 인젝션이 필요하면 AWUS036EACS, ACH, ACS를 선택하세요.

**Q2. AWUS036AXML의 블루투스는 Ubuntu에서 사용할 수 있나요?**
본 장비 실측에서 블루투스는 사용 가능합니다. `bluetoothctl` / `hciconfig`로 hci 컨트롤러가 UP임을 확인했고, BLE와 클래식 블루투스 기기를 스캔할 수 있으며, Wi-Fi와 블루투스를 동시에 사용할 수 있습니다(공존). 이 제품은 Wi-Fi+블루투스 복합 장치입니다. 참고: 다시 꽂을 때 가끔 WiFi probe에서 멈춰 `wlx` 인터페이스가 생성되지 않는데, 다른 USB 포트에 다시 꽂으면 복구됩니다.

**Q3. AWUS036AXML은 Ubuntu 24.04에서 드라이버를 따로 설치해야 하나요?**
필요 없습니다. mt7921u 드라이버는 kernel 6.17에 내장되어 있어, 꽂으면 dmesg에서 mt7921u가 인터페이스를 `wlx` 더하기 MAC으로 개명하는 것을 볼 수 있습니다(USB ID `0e8d:7961`). DKMS도 컴파일도 불필요합니다. 드라이버는 IBSS와 mesh 모드를 제공하지 않습니다.

**Q4. AWUS036AXML으로 AP를 열 수 있나요? WPA3를 지원하나요?**
가능합니다. 이것이 가장 안정적인 용도입니다. 2.4 GHz(802.11n, MCS 10)와 5 GHz VHT80(VHT-NSS2) 모두 iPhone이 접속해 authorized되었고, WPA3-SAE는 `sae_pwe=0`으로 iPhone 15 Pro가 접속했으며(`MFP: yes`, 2.4 GHz와 6 GHz에서 실측했고 5 GHz는 미실측), STA+AP 병행 시 STA 측 ping은 약 4.4 ms입니다. Wi-Fi 6 칩셋으로 포지셔닝되지만, 본 장비에서는 6 GHz band도 별도로 실측해 사용 가능했습니다(6135 MHz AP를 직접 구축, iPhone 15 Pro가 802.11ax로 접속해 IP 획득).

**Q5. AWUS036AXML과 AWUS036AXM은 무엇이 다르고 어느 것을 골라야 하나요?**
이 플랫폼에서 두 카드의 Wi-Fi 동작은 동일합니다. 같은 mt7921u를 쓰고, injection도 똑같이 실패하며, monitor 수신도 똑같이 약하고, AP, WPA3, VIF도 똑같이 사용 가능합니다. 차이는 AXML에 블루투스가 추가되었고(본 장비 실측 사용 가능) 본 장비에서 6 GHz band를 실측해 사용 가능하다는 점이며, AXM의 블루투스와 6 GHz는 이번 회차에서 별도로 실측하지 않았습니다. 순수 AP나 일반 접속이면 어느 쪽을 골라도 되지만, injection이나 handshake가 필요하면 두 카드 모두 선택하지 마세요.

## 더 읽어보기

(링크는 순차적으로 공개됩니다, 준비 중)

- 동일 칩셋 블루투스 미탑재 버전: [AWUS036AXM 단일 카드 실측](/ko/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- 인젝션 사용 가능한 대체 방안: [AWUS036EACS 단일 카드 실측](/ko/blog/awus036eacs-asus-gx10-ubuntu-test-report/), [AWUS036ACH 단일 카드 실측](/ko/blog/awus036ach-asus-gx10-ubuntu-test-report/), [AWUS036ACS 단일 카드 실측](/ko/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- 주제 글: [드라이버 설치 불필요: Ubuntu(ARM64)에서 Monitor와 AP 모드 활성화하기](/ko/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 주제 글: [WPA3-SAE 접속과 handshake 실무(본인 소유 환경 검증)](/ko/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 종합표 Hub: [9종 ALFA 랜카드의 ASUS GX10 전체 매트릭스](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

---

*테스트 기관: Yupitek(ALFA Network 대만 유통사) | 테스트 플랫폼: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | 테스트 기기: Apple iPhone 7 Plus(WPA3는 별도로 iPhone 15 Pro) | 테스트 환경: 본인 소유 사무실 Wi-Fi(SSID YUPITEK). 본 글은 제품 호환성과 성능 검증이며, 제3자 네트워크에 대한 조작 교육이 아닙니다.*
