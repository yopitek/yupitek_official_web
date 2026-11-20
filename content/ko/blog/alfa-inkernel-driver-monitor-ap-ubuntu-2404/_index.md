---
title: "드라이버 설치 불필요: Ubuntu 24.04 + kernel 6.17에서 인커널 드라이버로 ALFA 랜카드 Monitor와 AP 모드 활성화(rtw88 / rtw89 / mt76 실측)"
slug: alfa-inkernel-driver-monitor-ap-ubuntu-2404
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404.webp"
author: "benny-lai"
tags:
  - alfa-network
  - ubuntu-24-04
  - kernel-6-17
  - in-kernel-driver
  - rtw88
  - rtw89
  - mt76
  - monitor-mode
  - hostapd
  - ap-mode
  - linux-wifi
description: "Ubuntu 24.04 / kernel 6.17 드라이버 설치 불필요 가이드: 인커널 rtw88 / rtw89 / mt76 드라이버로 ALFA 랜카드의 Monitor와 AP 모드를 활성화하는 방법과 WPA3 핫스팟 호환성 설정, Kali 도구 체인 주의사항까지 정리했습니다."
faq:
  - question: "Ubuntu 24.04에서 ALFA 랜카드를 monitor mode로 진입시키려면 어떻게 하나요?"
    answer: "kernel 6.17 이상에서는 인터페이스를 NetworkManager 관리에서 내어주고 monitor 인터페이스 모드로 전환하기만 하면 되며, 제3자 드라이버를 설치할 필요가 없습니다. 본문에서 테스트한 rtw88 / rtw89 / mt76 세 드라이버 계열은 절차가 동일하며, 자세한 명령은 본문의 단계를 참조하십시오."
  - question: "왜 Ubuntu에서 ALFA 랜카드는 드라이버를 따로 설치하지 않아도 되나요?"
    answer: "Realtek rtw88/rtw89과 MediaTek mt76이 이 USB 칩들을 mainline 인커널 지원에 차례로 포함시켰기 때문입니다(카드별 최소 버전은 4.19~6.17로 다르며, Ubuntu 24.04에서 AX, AXER는 kernel 6.17 이상, 예: 24.04.4의 HWE가 필요합니다). kernel 6.17(GX10 실측)에서는 본문의 9종 카드 모두 내장되어 꽂으면 바로 인식되고, 컴파일도 DKMS도 필요 없습니다."
  - question: "ALFA 랜카드로 WPA3 핫스팟을 구축했는데 구형 iPhone이 연결되지 않으면 어떻게 하나요?"
    answer: "실측상 두 가지 흔한 원인이 있습니다. 하나는 hostapd의 sae_pwe를 2가 아닌 0으로 설정해야 구형 iPhone과 호환된다는 것이고, 다른 하나는 802.11n 설정을 유지하면 구형 장치의 연결(association)이 실패할 수 있으므로 호환성을 우선할 때는 802.11n을 끄는 것을 권장한다는 것입니다."
  - question: "rtw88, rtw89, mt76 중 어느 드라이버 계열이 mesh나 IBSS를 지원하나요?"
    answer: "실측에서 mt76 계열(예: AWUS036ACM / ACHM)은 단일 기기로 mesh(802.11s)와 IBSS를 구축할 수 있고, Realtek rtw88은 단일 기기로 IBSS에 join할 수 있지만(ACH 실측 기준) mesh는 미지원이며, rtw89은 IBSS조차 지원을 선언하지 않습니다."
draft: false
---

> 이 글은 표준 Linux 네트워크 설정 가이드로, 최신 커널에서 **내장(in-kernel) 드라이버**로 ALFA 무선 랜카드의 Monitor(모니터)와 AP(핫스팟) 모드를 활성화하는 방법을 시연합니다.
> 테스트 플랫폼: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. 모든 데이터는 Yupitek가 본인 소유 장비, 자사 사무실 Wi-Fi(SSID `YUPITEK`)에서 수행한 제품 호환성 실측에서 발췌한 것입니다.
> ⚠️ **합법적 사용**: Monitor 모드는 본인 소유 또는 허가된 네트워크의 모니터링에만 한정되며, AP 모드는 현지 무선 전파 법규를 준수하시기 바랍니다. 본문은 제3자 네트워크를 겨냥한 어떠한 공격 조작도 다루지 않습니다.

---

## 핵심 요약(TL;DR)

ASUS GX10(ARM64 / Ubuntu 24.04 / kernel 6.17)에서 Yupitek(ALFA Network 대만 총판)이 실측한 ALFA USB 무선 랜카드 9종은 모두 in-kernel 드라이버(`rtw88` / `rtw89` / `mt76`)로 동작해 드라이버 설치 없이 동일한 절차로 Monitor와 AP 모드를 활성화할 수 있었고, 2.4G와 5G AP에서 iPhone 7 Plus / 15 Pro가 정상 연결되었습니다. 카드별 최소 kernel은 4.19~6.17입니다.

- **최신 kernel에서는 드라이버 설치 불필요**: Realtek `rtw88` / `rtw89`과 MediaTek `mt76`이 이 ALFA USB 칩들을 인커널 지원에 포함시켰습니다. kernel 6.17(GX10 실측)에서는 9장 모두 내장되어 있으므로(카드별 최소 버전은 다름) 꽂으면 바로 사용되고 컴파일도 DKMS도 필요 없습니다.
- **Monitor와 AP 절차는 세 계열이 동일**: NetworkManager에 반환 → `iw`로 monitor 전환 / `hostapd`로 AP 기동.
- **두 가지 호환성 함정**: AP를 열 때 802.11n을 끄는 것을 권장(`ieee80211n=0`)하고 WPA3-SAE는 `sae_pwe=0`을 사용합니다. 그렇지 않으면 구형 iPhone이 연결되지 않습니다.
- **고급 모드 등급**: mesh는 `mt76`만, IBSS 단일 기기는 `mt76`과 `rtw88`(ACH)이 join 가능, `rtw89`는 미선언.
- **플랫폼 철칙**: `airmon-ng check kill`은 절대 실행하지 않으며(GX10이 네트워크가 끊깁니다), 외장 `wlx*` 인터페이스만 다룹니다.

## 1. 왜 "드라이버 설치 불필요"가 이 세대의 핵심인가

과거 Linux에서 ALFA 같은 USB 무선 랜카드를 사용할 때 가장 흔한 진입 장벽은 바로 드라이버였습니다. RTL8812AU, MT7610U 같은 칩은 초기에 mainline kernel에 들어가 있지 않아서, 사용자는 GitHub에서 out-of-tree 프로젝트(예: `morrownr/USB-WiFi`, `aircrack-ng/rtl8812au`)를 받아 DKMS로 현재 커널 버전에 바인딩해 컴파일해야 했습니다. 커널이 업데이트될 때마다 DKMS는 다시 빌드해야 했고, 한 번이라도 컴파일에 실패하면 랜카드가 그대로 사라졌습니다. 안정적 운영이 필요한 총판 검증이나 교육 환경에서는 이것이 오랜 고충이었습니다.

최근 mainline kernel에서 상황이 전환됩니다. Realtek의 `rtw88`, `rtw89`과 MediaTek의 `mt76` 세 대형 드라이버 계열이 이 USB 칩들을 차례로 인커널 지원에 정식 포함시켰습니다. 카드별 최소 kernel 버전은 다르지만(아래 표의 '최소 kernel' 열 참고), kernel 6.17(GX10 실측)에서는 본문에서 테스트한 아홉 장 모두 내장되어 있으며, **꽂으면 바로 인식, 컴파일 불필요, DKMS 불필요**입니다. 더 중요한 것은, 원래 가장 많이 쓰이던 두 out-of-tree 프로젝트(morrownr와 aircrack-ng의 rtl8812au)가 이제 모두 이 내장 드라이버로 방향을 돌렸고, bug 리포트도 `lwfinger/rtw88`로 통일되었다는 점입니다. 다시 말해, 드라이버를 수동으로 컴파일하는 이 단계는 최신 커널에서는 바로 생략할 수 있습니다.

`lwfinger/rtw88` 커뮤니티는 여전히 활발하게 유지보수를 이어가며 수정 사항을 꾸준히 상류로 보내므로, 내장 드라이버의 안정성도 커널과 함께 업데이트됩니다. 사용자는 더 이상 각자 브랜치를 유지보수할 필요가 없고, 업그레이드할 때마다 DKMS 컴파일 실패에 발목을 잡히지도 않습니다. 총판 검증과 교육 환경에서는 동일한 조작 절차를 여러 카드와 여러 번의 커널 업데이트에 걸쳐 반복 사용할 수 있어 유지보수 비용이 뚜렷이 낮아지며, 이것이 본문이 "드라이버 설치 불필요"에 초점을 둔 이유입니다.

본문 테스트가 다루는 칩과 대응 내장 드라이버 모듈은 다음과 같습니다.

| 칩 계열 | 칩 모델 | 내장 드라이버 모듈 | 최소 kernel | 세대 / 스트림 | 대표 카드 |
|---|---|---|---|---|---|
| **MediaTek mt76** | MT7612U | `mt76x2u` | 4.19 | Wi-Fi 5 / 2T2R | AWUS036ACM |
| **MediaTek mt76** | MT7610U | `mt76x0u` | 4.19 | Wi-Fi 5 / 1T1R | AWUS036ACHM |
| **MediaTek mt76** | MT7921AU | `mt7921u` | 5.18 | Wi-Fi 6 / 2x2 | AWUS036AXM / AXML |
| **Realtek rtw88** | RTL8812AU | `rtw88_8812au` | 6.13 | Wi-Fi 5 / 2T2R | AWUS036ACH |
| **Realtek rtw88** | RTL8811AU | `rtw88_8821au` | 6.13 | Wi-Fi 5 / 1x1 | AWUS036ACS |
| **Realtek rtw88** | RTL8821CU | `rtw88_8821cu` | 6.2 | Wi-Fi 5 / 1x1(+BT) | AWUS036EACS |
| **Realtek rtw89** | RTL8832BU | `rtw89_8852bu` | 6.17 | Wi-Fi 6 / 2x2 | AWUS036AX / AXER |

> 시스템 커널이 해당 카드의 최소 버전(위 표 참고)보다 낮을 때만 옛 방식이 필요합니다. DKMS로 out-of-tree 드라이버(rtw88 계열은 `lwfinger/rtw88`)를 설치하십시오. Ubuntu 24.04를 예로 들면, GA kernel 6.8에는 ACM, ACHM, AXM, AXML, EACS 드라이버가 내장되어 있고, HWE 6.14에서 ACH, ACS가 추가됩니다. AX, AXER는 kernel 6.17 이상(예: 24.04.4의 HWE)이 필요합니다. 본문은 GX10의 kernel 6.17을 기준으로 합니다.

---

## 2. 드라이버가 로드되어 바인딩되었는지 확인

어떤 모드로 전환하기 전에, 먼저 카드가 올바르게 인식되고 드라이버가 바인딩되었으며 인터페이스 이름이 생성되었는지 확인합니다. Realtek의 AWUS036ACH(`rtw88_8812au`)를 예로 네 가지 확인 단계는 다음과 같습니다.

**1단계: USB 장치가 열거되었는지 확인.** `lsusb`로 USB ID를 찾습니다(Realtek은 대개 `0bda:xxxx`, MediaTek은 대개 `0e8d:xxxx`).

```bash
lsusb | grep 0bda:8812
# Bus 004 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

**2단계: 드라이버 바인딩과 USB 속도 확인.** `lsusb -t`로 바인딩된 driver와 연결 속도를 동시에 볼 수 있습니다(`5000M`은 USB 3.0을 의미).

```bash
lsusb -t | grep rtw88_8812au
# |__ Port 001: Dev 002, If 0, Class=Vendor Specific Class, Driver=rtw88_8812au, 5000M
```

MediaTek 카드는 `dmesg`로 드라이버 초기화 메시지를 관찰하면서 동시에 인터페이스 이름 변경을 확인할 수 있습니다.

```bash
sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0
```

**3단계: 인터페이스 이름 가져오기.** Ubuntu는 예측 가능한 명명(predictable naming)을 채택하며, ALFA 외장 카드는 항상 `wlx` 뒤에 MAC 주소가 붙습니다. 이 이름은 MAC으로 결정되므로 **다시 꽂아도 바뀌지 않아** 스크립트화에 편리합니다. 내장된 외부 랜카드는 또 다른 이름(GX10에서는 `wlP9s9`)이므로 반드시 구분하십시오.

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cabca7f5
```

**4단계: 칩이 선언한 지원 인터페이스 모드 조회.** 이 단계가 뒤에서 어떤 모드를 쓸 수 있는지 결정합니다.

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Realtek rtw88(ACH)은 `IBSS / managed / AP / AP/VLAN / monitor`를 나열하지만 mesh와 P2P는 **없습니다.** MediaTek mt76(ACHM)은 추가로 `mesh point / P2P-client / P2P-GO`를 나열합니다. 이 목록이 각 계열 능력 차이의 1차 근거이며, 자세한 내용은 5절을 참조하십시오.

---

## 3. Monitor 모드 활성화(2.4 GHz / 5 GHz)

Monitor(모니터) 모드는 랜카드가 어떤 AP와도 연결하지 않고 공중의 802.11 frame을 직접 수신하게 하며, 자가 네트워크의 패킷 진단, 스펙트럼 점검, 신호 커버리지 평가에 자주 쓰입니다. 세 계열의 활성화 절차는 동일하고, 차이는 개별 계열의 안정성 주의사항뿐입니다(5, 6절 참조).

**공통 활성화 단계:**

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no      # 우리가 직접 관리하도록 반환, NetworkManager 개입 방지
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
iw dev $IF info | grep type
# type monitor
```

`type monitor`가 보이면 전환 성공입니다. 이어서 모니터링할 채널을 지정합니다. **2.4 GHz**는 `set channel`을 사용합니다.

```bash
sudo iw dev $IF set channel 6
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch6.pcap
tcpdump -r /tmp/mon-ch6.pcap | wc -l
```

**5 GHz**는 주파수 지정이 오류가 적습니다(ch36 = 5180 MHz).

```bash
sudo iw dev $IF set freq 5180
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch36.pcap
tcpdump -r /tmp/mon-ch36.pcap | wc -l
```

**예상 결과(실측 발췌):** AWUS036ACH는 ch1 / ch6 / ch11에서 각각 92 / 214 / 71개의 frame을 잡았고, 5 GHz의 ch36 / ch149 / ch157에서는 각각 260 / 137 / 127개의 frame을 잡아, 2.4G와 5G 모니터링이 모두 정상임을 나타냅니다. MediaTek의 ACHM은 `airodump-ng --band abg`로 120초간 주파수 홉 스캔하여 ch1/5/6/36/149/157 일대에서 19개의 기지국과 14개의 클라이언트를 찾을 수 있었습니다. 어떤 채널에서 0개의 패킷이 잡히는 것은 보통 그 순간 해당 채널에 AP가 없는 것일 뿐, 랜카드 고장이 아닙니다.

monitor 모드로 전환한 뒤에는 흔히 쓰는 표준 진단 도구들을 `wlx*` 인터페이스에서 바로 쓸 수 있습니다. `airmon-ng`는 랜카드와 드라이버 상태를 나열하는 데 쓰고, `kismet`은 데이터 소스로 삼아 실시간 측록하며 `.kismet` log를 생성할 수 있고, `Wireshark`와 `tshark`는 캡처한 패킷을 분석하며, `bettercap`은 채널 점검에 쓸 수 있습니다. 이 도구들은 세 계열 모두에서 실측상 사용 가능하며, 자가 무선 환경의 채널 사용 현황과 신호 커버리지를 점검하기에 매우 적합합니다. 유일하게 주의할 것은 `hcxdumptool` 8.x가 이 플랫폼에서 세 계열 모두에서(2.4 GHz의 EACS 제외) `failed to arm`을 낸다는 점입니다(내장 드라이버가 active-monitor를 제공하지 않음). 유사한 기능이 필요하면 `airodump-ng`에 aircrack-ng 패키지를 함께 쓰는 것으로 전환하십시오.

> **5 GHz 안내:** 기본 regdomain(`country 00`)에서는 많은 5 GHz 채널이 passive/no-IR이어서 모니터링은 되지만 능동 송신이 제한됩니다. 이후 허가된 범위 내에서 5 GHz 테스트를 하려면 먼저 `sudo iw reg set US`로 해제하고, 끝난 뒤 `sudo iw reg set TW`로 되돌리십시오. Realtek `rtw88_8812au`는 알려진 5G RX-stuck 현상(모드를 반복 전환한 뒤 5G에서 패킷을 못 받음)이 별도로 있으니, 만나면 카드를 물리적으로 한 번 뽑았다 꽂고 5G를 우선 수행하십시오.

---

## 4. AP / 핫스팟 모드 활성화(2.4 GHz / 5 GHz)

AP(핫스팟) 모드는 `hostapd`로 랜카드를 하나의 Wi-Fi 기지국으로 만듭니다. 세 계열의 절차는 동일합니다. 먼저 인터페이스를 NetworkManager에서 내어주고, `hostapd` 설정 파일로 기동합니다. 다음은 공통의 최소 설정입니다.

**4-1. 2.4 GHz(순수 802.11g)**

설정 파일 `/tmp/ap24.conf`를 만듭니다.

```ini
interface=wlx00c0cabca7f5
driver=nl80211
ssid=ALFA-AP-24G
hw_mode=g
channel=6
country_code=TW
auth_algs=1
ieee80211n=0
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=<비밀번호 최소 8자리>
```

기동:

```bash
sudo nmcli dev set $IF managed no
sudo hostapd /tmp/ap24.conf
```

클라이언트가 연결되면 `hostapd`는 순서대로 `authenticated` → `associated` → `AP-STA-CONNECTED` → `EAPOL-4WAY-HS-COMPLETED`를 출력합니다. 마지막 줄이 보이면 4-way 핸드셰이크 완료, 연결 성공을 의미합니다.

**4-2. 5 GHz(순수 802.11a, ch36)**

위 설정을 5 GHz로 바꿉니다.

```ini
ssid=ALFA-AP-5G
hw_mode=a
channel=36
```

2x2 카드(예: rtw89의 AX/AXER, mt76의 ACM/AXM)는 VHT80 설정을 추가해 80 MHz 대역폭으로 끌어올릴 수 있으며, 단일 안테나이거나 호환성을 원할 때는 20 MHz 순수 a로 유지하면 됩니다.

**4-3. 두 가지 핵심 호환성 설정**

1. **AP를 열 때 802.11n을 끄는 것을 권장**(`ieee80211n=0`, 순수 g / 순수 a로 동작). 실측상 구형 클라이언트(iPhone 7 Plus)는 `ieee80211n=1`을 유지하면 연결에 실패하고 화면에 "비밀번호 오류"로 잘못 표시되는데, 실제로는 `handle_assoc_cb: STA not found`입니다. 802.11n을 제거하면 첫 시도에 바로 연결됩니다.
2. **WPA3-SAE는 `sae_pwe=0`을 사용**(hunting-and-pecking). `sae_pwe=2`(강제 H2E)를 쓰면 구형 기기에서 키 교환이 실패합니다. WPA3 구간 예시:

```ini
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
ieee80211w=2
sae_pwe=0
```

이 두 함정은 Realtek과 MediaTek 카드에서 모두 똑같이 발생하며, 드라이버 차이가 아니라 클라이언트 호환성에 속합니다. 본문에서 테스트한 아홉 장의 카드는 2.4G와 5G AP에서 모두 iPhone 7 Plus / 15 Pro를 정상적으로 연결시킬 수 있었습니다.

**4-4. 인터넷을 쓰면서 동시에 핫스팟 되기(STA + AP)**

mt76 계열은 한 장의 카드로 기존 Wi-Fi에 연결하는 동시에 또 다른 AP VIF를 만들어 중계 핫스팟으로 쓰는 것을 지원합니다. 실측상 ACHM은 메인 인터페이스가 YUPITEK에 연결된 채로 5 GHz 핫스팟을 열어 iPhone을 연결시켰고, 다운로드는 여전히 198 Mbit/s, ping 평균 3.2 ms였습니다. 이 조합은 세 가지 조건을 만족해야 합니다. AP VIF는 다른 MAC을 써야 하고, 인터페이스 이름은 `wlx` 형식을 유지해야 하며, 모든 VIF가 같은 채널에 있어야 합니다. Realtek 카드는 이 조합이 phy로 보장되지 않습니다(rtw88의 managed + monitor는 사용 가능하지만 STA + AP는 안정적이지 않음). 중계 핫스팟을 만들려면 mt76 계열을 우선 선택하는 것을 권장합니다.

---

## 5. 세 칩 계열의 차이와 제약

기본인 managed / monitor / AP 세 모드는 세 계열 모두 지원하며 표현도 일치합니다. 차이는 **고급 인터페이스 모드**(mesh, IBSS, active monitor, P2P)에 있습니다. 이는 전적으로 드라이버 선언에 달려 있고 카드의 안테나 수와는 무관합니다. 다음은 실측 종합입니다.

| 고급 모드 | MediaTek mt76 | Realtek rtw88 | Realtek rtw89 |
|---|---|---|---|
| Monitor(2.4G/5G) | ✅ | ✅ | ✅ |
| AP(hostapd) | ✅ | ✅ | ✅ |
| Ad-hoc / IBSS(단일 기기) | 🟡 단일 기기 구축 가능 | 🟡 단일 기기 구축 가능 | ❌ 드라이버 미선언 |
| Mesh(802.11s, 단일 기기) | 🟡 단일 기기 구축 가능 | ❌ `-95` 미지원 | ❌ 드라이버 미선언 |
| Active monitor | 🟡 설정 가능 | ❌ `-95` 미지원 | N/A |
| Wi-Fi Direct(P2P) | 두 번째 장치 필요 | ❌ `-95` 미지원 | N/A |

**MediaTek mt76(ACM / ACHM / AXM / AXML)** 은 고급 모드가 가장 완전한 계열입니다. `iw phy info`가 바로 `mesh point`, `IBSS`, `P2P-client/GO`를 선언합니다. 실측상 단일 기기로 `Joined IBSS`, `type mesh point`가 되고 대응 beacon을 송출했습니다(두 번째 peer link는 두 번째 장비 부족으로 미검증). 용도가 mesh나 IBSS 단일 기기 실험이라면 mt76 계열이 1순위입니다. 특히 주의할 것은 Wi-Fi 6의 MT7921(AXM/AXML)로, 모드는 완비되어 있고 AP도 안정적이지만 이 플랫폼에서는 frame injection을 할 수 없습니다(주원인은 stock kernel 6.16+의 mac80211 chanctx 회귀이며 칩 선천적 문제가 아님. 커뮤니티에서 동일 모델에 git/patched 드라이버를 쓰면 동작하기도 하지만 펌웨어가 속도를 잠급니다. morrownr/USB-WiFi #387, morrownr/mt76 #18 대응). 인젝션이 필요한 고급 테스트에는 적합하지 않습니다.

**Realtek rtw88(ACH / ACS / EACS)** 은 `IBSS / managed / AP / AP/VLAN / monitor`를 지원합니다. IBSS는 단일 기기 구축이 가능하지만(`Joined IBSS`, ACH 실측 기준. EACS는 iftype을 나열하지만 실측에서는 join이 무효), **mesh(802.11s), active monitor, Wi-Fi Direct 세 가지는 실측에서 모두 `Operation not supported (-95)`를 반환합니다.** rtw88 고유의 또 다른 특성은 VIF입니다. `iw phy` 플래그에는 "interface combinations are not supported"라고 적혀 있지만, ACH 실측상 managed + monitor 두 인터페이스를 동시에 up할 수 있었고 monitor VIF가 100개의 frame을 잡아 "인터넷을 쓰면서 동시에 측록"이 가능했습니다. 다만 phy가 이 조합을 보장하지 않으므로, 고부하 장시간 운용에는 여전히 mt76 계열을 권장합니다.

**Realtek rtw89(AX / AXER)** 은 본문에서 가장 최신인 Wi-Fi 6 계열로, monitor와 AP(VHT80 포함) 모두 좋은 표현을 보이고 수신 감도도 강합니다. 다만 고급 모드에서는 active monitor / mesh / IBSS / P2P가 드라이버 레벨에서 미선언(N/A)이므로, 이러한 단일 기기 실험은 mt76 카드로 전환하십시오. rtw89의 포지션은 안정적인 Wi-Fi 6 모니터링과 핫스팟이지, 고급 인터페이스 모드의 실험 플랫폼이 아닙니다.

> 한 문장 제품 선정: **mesh / IBSS 단일 기기가 필요하면 → mt76(ACM / ACHM); Wi-Fi 6 핫스팟과 강한 수신이 필요하면 → rtw89(AX / AXER); 듀얼 밴드 범용과 VIF가 필요하면 → rtw88(ACH).**

---

## 6. 플랫폼 보안 주의(GX10 + Ubuntu ARM64)

GX10처럼 "내장 랜카드가 외부 인터넷을 담당하고, 외장 ALFA 카드로 테스트하는" 기기에서는 다음 몇 가지가 운영 철칙이며, 그대로 따라야 본인 네트워크를 끊지 않습니다.

1. **`airmon-ng check kill`을 절대 실행하지 마십시오.** 이 명령은 NetworkManager를 꺼서 GX10의 외부 연결까지 함께 끊습니다. 본문은 전 과정에서 `iw`와 `nmcli dev set <인터페이스> managed no`만 사용하고 `check kill`은 건드리지 않습니다.
2. **`wlx*`만 다루고, 내장 `wlP9s9`은 절대 건드리지 마십시오.** `wlP9s9`은 GX10의 외부 인터넷 본선으로, 어떤 down / 모드 변경 동작도 ALFA의 `wlx*` 인터페이스에만 내려야 합니다. 명령 전에는 반드시 `echo $IF`로 대상을 확인하십시오.
3. **RX stall은 뽑았다 꽂아 복구.** monitor / AP를 반복 전환한 뒤 아무것도 스캔되지 않으면 대개 드라이버의 수신 멈춤입니다(Realtek 5G에서 특히 흔함). 소프트웨어로는 보통 복구가 안 되니, 카드를 **물리적으로 한 번 뽑았다 꽂으십시오.** USB가 재열거되고 인터페이스 이름은 MAC이 불변이라 일관되게 유지됩니다.
4. **BT+WiFi 복합 카드는 USB 포트 교체.** EACS, AXML 같은 블루투스+Wi-Fi 복합 장치는 다시 꽂을 때 간혹 Wi-Fi probe가 멈춰 `wlx` 인터페이스가 생성되지 않는데, USB 포트를 바꾸면 대개 정상화됩니다.
5. **5 GHz 송신 전 regdomain 먼저 설정.** 기본 `country 00`에서는 5 GHz 대부분이 no-IR로 능동 송신이 금지됩니다. 허가 범위 내 테스트 전에 `sudo iw reg set US`로 해제하고, 끝나면 `sudo iw reg set TW`로 되돌립니다.
6. **ARM64의 패키지 주의.** GX10은 aarch64이며 `aircrack-ng`는 prebuilt wheel/package가 없는 경우가 많아 원본 소스에서 컴파일해야 하고, `wifite`는 apt 의존성 충돌을 우회하기 위해 GitHub 버전을 권장합니다. 또한 `hcxdumptool` 8.x는 이 플랫폼에서 세 계열 모두에서(2.4 GHz의 EACS 제외) `failed to arm`을 내므로(내장 드라이버가 active-monitor 미지원), 모니터 캡처는 `airodump-ng`에 aircrack-ng 패키지를 함께 쓰는 것으로 전환하십시오.

**테스트 종료 후 일반 모드로 복구:**

```bash
sudo pkill hostapd 2>/dev/null
sudo ip link set $IF down
sudo iw dev $IF set type managed
sudo ip link set $IF up
sudo nmcli dev set $IF managed yes
iw dev $IF info | grep type      # 예상 type managed
```

---

## 자주 묻는 질문(FAQ)

**Q: Ubuntu 24.04에서 ALFA 랜카드를 monitor mode로 진입시키려면 어떻게 하나요?**
A: kernel 6.17 이상에서는 인터페이스를 NetworkManager 관리에서 내어주고 monitor 인터페이스 모드로 전환하기만 하면 되며, 제3자 드라이버를 설치할 필요가 없습니다. 본문에서 테스트한 rtw88 / rtw89 / mt76 세 드라이버 계열은 절차가 동일하며, 자세한 명령은 본문의 단계를 참조하십시오.

**Q: 왜 Ubuntu에서 ALFA 랜카드는 드라이버를 따로 설치하지 않아도 되나요?**
A: Realtek `rtw88`/`rtw89`과 MediaTek `mt76`이 이 USB 칩들을 mainline 인커널 지원에 차례로 포함시켰기 때문입니다(카드별 최소 버전은 4.19~6.17로 다르며, Ubuntu 24.04에서 AX, AXER는 kernel 6.17 이상, 예: 24.04.4의 HWE가 필요합니다). kernel 6.17(GX10 실측)에서는 본문의 9종 카드 모두 내장되어 꽂으면 바로 인식되고, 컴파일도 DKMS도 필요 없습니다.

**Q: ALFA 랜카드로 WPA3 핫스팟을 구축했는데 구형 iPhone이 연결되지 않으면 어떻게 하나요?**
A: 실측상 두 가지 흔한 원인이 있습니다. 하나는 hostapd의 `sae_pwe`를 2가 아닌 0으로 설정해야 구형 iPhone과 호환된다는 것이고, 다른 하나는 802.11n 설정을 유지하면 구형 장치의 연결(association)이 실패할 수 있으므로 호환성을 우선할 때는 802.11n을 끄는 것을 권장한다는 것입니다.

**Q: `rtw88`, `rtw89`, `mt76` 중 어느 드라이버 계열이 mesh나 IBSS를 지원하나요?**
A: 실측에서 `mt76` 계열(예: AWUS036ACM / ACHM)은 단일 기기로 mesh(802.11s)와 IBSS를 구축할 수 있고, Realtek `rtw88`은 단일 기기로 IBSS에 join할 수 있지만(ACH 실측 기준) mesh는 미지원이며, `rtw89`은 IBSS조차 지원을 선언하지 않습니다.

## 7. 더 읽어보기

- 아홉 장의 ALFA 카드 전체 능력 비교와 제품 선정 총평 → [ALFA 무선 랜카드 총평 Hub(종합표)](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Realtek rtw88 대표 카드 단계별 가이드 → [AWUS036ACH 단일 카드 실측](/ko/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- MediaTek mt76 대표 카드 단계별 가이드 → [AWUS036ACHM 단일 카드 실측](/ko/blog/awus036achm-asus-gx10-ubuntu-test-report/)

---

*테스트 기관: Yupitek(ALFA Network 대만 총판) — https://www.yupitek.com | 테스트 환경: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | 테스트 장치: Apple iPhone 7 Plus(WPA3는 iPhone 15 Pro로 별도 측정)*
