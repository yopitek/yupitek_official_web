---
title: "ALFA AWUS036AX 카드별 실측: ASUS GX10 + Ubuntu 24.04의 Wi-Fi 6 모니터 / 인젝션 / AP 성능 보고서(Realtek RTL8832BU / rtw89_8852bu)"
slug: awus036ax-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ax-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ax
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - asus-gx10
  - ubuntu-arm64
description: "AWUS036AX(Wi-Fi 6)를 Ubuntu 24.04 ARM64에서 실측: 드라이버 설치 불필요, 모니터, 2.4G 인젝션 96%, 5G AP VHT80, WPA3-SAE, 엔드투엔드 핸드셰이크(.22000) 통과; IBSS / 메시는 미지원. 플랫폼은 ASUS GX10, RTL8832BU."
faq:
  - question: "AWUS036AX는 Ubuntu 24.04 ARM64에서 드라이버를 설치해야 하나요? lsusb에 0bda:1a2b가 표시되면 어떻게 하나요?"
    answer: "본문에서 테스트한 kernel 6.17(ASUS GX10)에서는 필요 없습니다. RTL8832BU는 내장 rtw89_8852bu 드라이버로 구동되어 컴파일도 DKMS도 필요 없습니다. lsusb에 0bda:1a2b(CD-ROM 모드)가 표시되면 sudo usb_modeswitch -v 0bda -p 1a2b -K를 실행해 WLAN으로 전환하세요."
  - question: "AWUS036AX는 모니터 모드와 패킷 인젝션을 지원하나요?"
    answer: "지원합니다. 2.4 GHz 인젝션 29/30(96%); 5 GHz는 AP를 하나씩 지정해 테스트하면 Injection is working!을 반환합니다. airodump-ng 주파수 호핑 60초로 14개 AP와 4개 client를 스캔했습니다. 액티브 모니터, IBSS, 메시는 지원하지 않습니다."
  - question: "AWUS036AX로 WPA 핸드셰이크를 캡처할 수 있나요? MT7921의 AXM / AXML은 되나요?"
    answer: "AX는 가능합니다. 본인 소유 AP와 본인 소유 iPhone 7 Plus에서 aireplay-ng -0로 재접속을 유도하고 airodump-ng로 완전한 M1–M4를 캡처한 뒤 hcxpcapngtool로 .22000을 변환합니다. MT7921의 AXM / AXML은 본 플랫폼에서 인젝션 실패로 할 수 없습니다. 본인 소유 또는 허가된 네트워크에서만 가능합니다."
  - question: "AWUS036AX를 AP 핫스팟으로 쓸 수 있나요? WPA3을 지원하나요?"
    answer: "가능합니다. hostapd로 2.4G(802.11n)와 5G(VHT 80 MHz) AP를 열어 iPhone 7 Plus가 접속해 VHT-NSS2 80 MHz로 표시됩니다. WPA3-SAE(ieee80211w=2, sae_pwe=0)는 iPhone 15 Pro로 2.4 GHz에서 접속해 MFP: yes로 표시됩니다(5 GHz WPA3는 실측하지 않음)."
  - question: "AWUS036AX와 AWUS036AXER의 차이는 무엇인가요? 어느 것을 선택해야 하나요?"
    answer: "둘 다 RTL8832BU + rtw89_8852bu로 성능 매트릭스가 동일하며, 차이는 안테나와 수신에 있습니다. AXER는 외장 안테나로, 동일 배치 테스트에서 주파수 호핑으로 63 AP + 12 client를 스캔했습니다(AX는 14 AP + 4 client). 데스크톱 고정 용도면 AX, 장거리나 최강 수신이 필요하면 AXER를 선택하세요."
draft: false
---

**핵심 요약(TL;DR)**: Yopitek(ALFA Network 대만 총판) 실측 결과, AWUS036AX는 ASUS GX10 / Ubuntu 24.04 ARM64(kernel 6.17)에서 드라이버 설치 불필요이며 듀얼 밴드 monitor가 가능하고, 2.4G 인젝션 96%, 5G AP VHT80, 엔드투엔드 .22000 통과, IBSS / 메시는 미지원입니다.

> 본문은 Yopitek이 **본인 소유 장비, 본인 소유 사무실 Wi-Fi(SSID `YUPITEK`), 본인 소유 테스트 휴대폰**에서 완료한 제품 호환성 및 성능 실측으로, 대상은 ALFA **AWUS036AX**(Realtek RTL8832BU, Wi-Fi 6 2x2)입니다.
> 테스트 플랫폼: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`; 대조 장치는 Apple iPhone 7 Plus(WPA3과 VIF는 iPhone 15 Pro로 별도 테스트).
> ⚠️ **합법 사용**: 모니터와 인젝션은 본인 소유 또는 허가된 네트워크에서만 가능하며, AP 모드는 현지 무선 규제를 준수하십시오. 본문은 제3자 네트워크에 대한 어떠한 공격 행위도 포함하지 않습니다.

---

## 1. 이 카드와 테스트 플랫폼

AWUS036AX는 ALFA의 이번 세대 Wi-Fi 6 USB 네트워크 카드로, Realtek RTL8832BU 칩, 2x2 듀얼 공간 스트림을 채택했으며 2.4 GHz와 5 GHz 듀얼 밴드를 지원합니다. ALFA 제품군에서 이것은 외장 안테나 버전인 AWUS036AXER와 동일한 칩과 동일한 드라이버를 공유하며, 차이는 안테나 형태와 수신 이득에 있습니다. 같은 Wi-Fi 6인 MediaTek 제품 AWUS036AXM / AXML과는 완전히 다른 칩 노선이며, 실측 결론도 크게 다릅니다(5장에서 설명).

이번 테스트는 사양서상의 이론 속도를 논하지 않고, 유통 및 엔지니어링 현장이 가장 중시하는 세 가지만 답합니다. 최신 Linux에서 설치가 쉬운가? 어떤 무선 성능이 실제로 작동하는가? 어떤 것이 드라이버가 태생적으로 못 하는, 시간을 헛되이 쓰지 말아야 할 것인가? 결론은 재현 가능해야 하므로, 모든 명령은 2026-11-18 당일 GX10 실기에서 한 줄씩 실행했으며, 아래의 "실측 출력"은 모두 실제 발췌입니다(MAC 주소는 `xx`로 가림).

테스트 경계를 먼저 분명히 합니다. 전 과정은 자사 사무실에서 본인 소유 `YUPITEK` 네트워크와 본인 소유 휴대폰을 대상으로 진행했습니다. 모니터는 본인 환경의 패킷만 수신하고, 인젝션과 핸드셰이크는 자사 AP와 자사 iPhone에만 수행했습니다. 목적은 "이 카드가 이 기기에서 무엇을 할 수 있는지"를 검증하는 것이지 제3자 네트워크 공격을 시연하는 것이 아닙니다.

---

## 2. 하드웨어와 드라이버(Wi-Fi 6, 무설치)

이번 세대의 가장 실질적인 이점은 **꽂으면 바로 인식, 컴파일 불필요, DKMS 불필요**입니다. RTL8832BU의 `rtw89_8852bu` 드라이버는 이미 kernel 6.17의 in-kernel 모듈이며, GX10은 부팅 시 바로 바인딩해 GitHub에서 out-of-tree 프로젝트를 받아 수동 컴파일할 필요가 없습니다.

칩 정보와 검증 단계는 다음과 같습니다. 먼저 `lsusb`로 카드가 WLAN 모드로 열거되는지 확인합니다.

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
```

예상대로라면 `ID 0bda:b832 Realtek Semiconductor Corp. 802.11ax WLAN Adapter`가 보일 것입니다. 본 테스트 기관의 이 카드는 CD-ROM 모드에 걸리지 않고 바로 WLAN 모드로 나타났습니다. 만약 받은 카드가 `0bda:1a2b`로 표시된다면 아직 CD-ROM 모드라는 뜻이며, `sudo usb_modeswitch -v 0bda -p 1a2b -K`로 WLAN으로 전환하면 됩니다.

이어서 드라이버와 펌웨어 로드를 확인합니다.

```bash
sudo dmesg | grep rtw89_8852bu | tail -3
```

실기에서 로드된 것은 `rtw89/rtw8852b_fw-1.bin`, firmware version `0.29.29.5`입니다. 드라이버와 펌웨어 모두 kernel과 함께 내장되므로 별도 패키지를 설치할 필요가 없습니다.

마지막 단계는 이 드라이버가 **어떤 인터페이스 모드를 지원한다고 선언하는지** 먼저 명확히 보는 것입니다. 이 단계가 이후 어떤 성능이 있고 어떤 것이 N/A인지를 직접 결정합니다.

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

실기에서 나열된 것은 `managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO`입니다. 목록에 IBSS, mesh point, 액티브 모니터는 보이지 않습니다. 이것은 설정이 잘못된 것이 아니라 `rtw89_8852bu`가 애초에 이 세 가지 모드를 구현하지 않았기 때문이며, 4장에서 이에 따라 N/A로 표시합니다.

---

## 3. 실측 성능: 모니터 / 인젝션 / AP / WPA3

먼저 성능 종합표를 제시하며, 각 칸은 아래의 실측 발췌에 대응합니다.

| 성능 | 2.4 GHz | 5 GHz | 실측 발췌 |
|---|---|---|---|
| **모니터** | ✅ 강함 | ✅ 강함 | airodump 주파수 호핑 60초로 **14 AP + 4 client** 스캔 |
| **인젝션** | ✅ **96%** | ✅ 사용 가능 | 2.4G `aireplay-ng --test` 29/30(96%); 5G 하나씩 `Injection is working!` |
| **AP 핫스팟** | ✅ 802.11n(HT) | ✅ **VHT 80 MHz** | iPhone 7 Plus 접속: 2.4G MCS 12, 5G VHT-NSS2 80 MHz |
| **WPA3-SAE** | ✅ | 미실측 | iPhone 15 Pro 접속, MFP: yes(`sae_pwe=0`), 2.4 GHz에서만 실측 |
| **WPA 핸드셰이크 캡처** | ✅ **엔드투엔드** | — | 본인 소유 iPhone에 deauth → 완전한 4-way 캡처 → hashcat `.22000` 변환 |

**모니터(모니터 모드 / 수신) ✅ 강함.** 모니터로 전환한 뒤 2.4 GHz와 5 GHz 모두 많은 패킷을 수신합니다(각각 약 100 패킷/6초). `airodump-ng --band abg`로 60초 주파수 호핑 스캔을 하면 실측상 14개 AP에 4개 client를 찾았으며, 수신 성능은 ALFA Wi-Fi 5의 ACM / ACHM과 동급으로 MediaTek MT7921 두 카드(AXM / AXML은 실측상 수신이 약함)를 크게 능가합니다. 현장 조사, 채널 점유 실사 같은 작업에 이 카드의 수신은 충분합니다.

**인젝션(패킷 인젝션) ✅ 사용 가능, 이것이 AX가 MediaTek 제품을 상대하는 핵심 차이입니다.** 2.4 GHz(ch6)에서 `aireplay-ng --test`를 돌리면 실측상 `29/30: 96%`, `Injection is working!`로 응답률 96%입니다. 5 GHz(ch36)에서 브로드캐스트 테스트는 `Found 0 APs`를 반환할 수 있지만(현대 AP는 브로드캐스트 probe에 응답하지 않으므로 정상), AP BSSID를 하나씩 지정해 테스트하면 `Injection is working!`을 반환해 5 GHz 인젝션 사용 가능을 확인합니다. 반대로 같은 Wi-Fi 6인 MediaTek AXM / AXML은 본 플랫폼에서 **인젝션이 바로 실패**합니다(주된 원인은 kernel 6.16 이후 mac80211 chanctx 회귀이며, 여기에 firmware가 인젝션 속도를 1/6 Mbps로 고정하는 문제가 더해진 것으로, 칩셋 자체의 한계는 아닙니다). 이 점은 제품 선정 시 반드시 구분해야 합니다.

**AP 핫스팟 ✅ 듀얼 밴드 개설 가능, 5 GHz는 VHT80까지 올라감.** hostapd로 AP를 띄워 2.4 GHz는 802.11n(`ieee80211n=1`, HT20)으로 열었고 iPhone 7 Plus가 접속한 뒤 MCS 12, authorized로 표시됩니다. 5 GHz는 VHT 80 MHz(`vht_oper_chwidth=1`, `ht_capab=[HT40+]`)로 열었고 iPhone 7 Plus가 접속한 뒤 VHT-NSS2 80 MHz, authorized로 표시됩니다. 양쪽 대역 모두 클라이언트를 안정적으로 띄울 수 있고, 80 MHz 대역폭도 실제로 협상에 성공합니다.

**WPA3-SAE ✅.** AP의 `wpa_key_mgmt`를 `SAE`, `ieee80211w=2`로 바꾸자 실측상 iPhone 15 Pro가 접속했고 MFP(Management Frame Protection)가 yes로 표시됩니다. 여기에는 호환성 세부 사항이 있습니다. `sae_pwe`를 `0`(Hunting-and-Pecking)으로 설정해야 구형 iPhone이 접속할 수 있습니다.

**WPA 핸드셰이크 캡처 ✅ 엔드투엔드 성공.** 자사 `YUPITEK` 네트워크에서 본인 소유 iPhone 7 Plus를 대상으로 전체 흐름을 진행했습니다. 모니터 측에서 해당 채널 녹취 → `aireplay-ng -0`으로 deauth를 보내 재접속 유도 → `airodump-ng`로 완전한 4-way 핸드셰이크(M1/M2/M3/M4) 캡처 → `hcxpcapngtool`로 hashcat의 `.22000` 형식 변환. 이 카드는 인젝션이 사용 가능하기 때문에 전체 체인이 통과하는 것이며, 인젝션이 실패하는 카드(예: AXM / AXML)는 deauth 단계에서 끊깁니다. 이 핸드셰이크 캡처 체인에 쓰인 Kali 상용 도구(aircrack-ng, hcxtools)는 모두 Ubuntu 24.04 ARM64에서 바로 실행됩니다.

---

## 4. 고급 기능과 제한(rtw89 드라이버의 N/A 항목)

이 장에서는 "할 수 있는 고급 기능"과 "드라이버가 태생적으로 못 하는 것"을 한 번에 분명히 밝혀 현장에서 시간을 헛되이 쓰지 않도록 합니다.

| 기능 | 상태 | 설명 |
|---|---|---|
| **VIF(STA + AP 병행)** | ✅ | 주 인터페이스는 `YUPITEK`에 연결하고 동시에 AP VIF(ch36 VHT80)를 열어 두 인터페이스 병행; STA 측 ping 3.2 ms |
| **WPA 핸드셰이크 캡처** | ✅ 엔드투엔드 | M1–M4 캡처, `hcxpcapngtool`로 `.22000` 변환 |
| **액티브 모니터** | **N/A** | `rtw89_8852bu`는 이 모드가 없음(`iw phy`의 supported modes에 없음) |
| **Ad-hoc(IBSS)** | **N/A** | 드라이버 미지원 |
| **메시(802.11s)** | **N/A** | 드라이버 미지원 |
| **Wi-Fi Direct(P2P)** | ⬜ 미테스트 | 드라이버는 지원을 선언하나 두 번째 장치가 필요해 이번에는 생략 |

**VIF ✅.** AP 가상 인터페이스(다른 MAC, unmanage)를 하나 만들고, 주 인터페이스는 Wi-Fi 연결을 유지한 채 같은 채널에서 AP를 엽니다. 실측상 주 인터페이스가 `YUPITEK`에 연결된 동시에 AP VIF가 ch36에서 VHT80으로 구동되어 두 인터페이스가 병행 작동하며, STA 측 ping은 3.2 ms입니다. "한쪽으로 인터넷에 연결하면서 다른 쪽으로 테스트 핫스팟을 여는" 시나리오에 적합합니다.

**액티브 모니터 / IBSS / 메시는 N/A이지 고장이 아닙니다.** 이 세 가지 모드는 2장 `iw phy info`의 supported interface modes에 나타나지 않는데, 이는 `rtw89_8852bu` 드라이버가 아예 구현하지 않았음을 의미합니다. `sudo iw dev $IF set type ibss` 같은 명령은 바로 실패하며, 해결책이 없습니다. 이것은 파라미터나 펌웨어로 구제할 수 있는 것이 아니며, 이 세 가지 모드가 필요하면 칩 노선을 바꿔야 합니다(예: MediaTek mt76의 ACM / ACHM은 단일 기기에서 IBSS / 메시를 생성 가능).

**먼저 알아둘 플랫폼 계층의 제한 하나: hcxdumptool이 GX10에서 `failed to arm`.** 이는 AX 고유의 문제가 아닙니다. `hcxdumptool 8.x`는 액티브 모니터를 필요로 하는데, GX10에는 삼중 밴드 네트워크 카드가 내장되어 있어 USB 카드 열거 시 `-I`가 내장 phy에 잘못 매핑되기 쉽습니다. 그 결과 이 기기에서는 모든 피시험 USB 카드가 arm에 실패합니다(예외는 2.4 GHz의 AWUS036EACS뿐입니다). 실무적 방법은 **aircrack-ng 패키지로 바꾸는 것**(airodump-ng + aireplay-ng)으로 캡처를 돌리는 것이며, 이 카드는 인젝션이 사용 가능해 전체 체인이 그대로 엔드투엔드로 완주합니다(3장 참고).

**안전 수칙(GX10 플랫폼 공통):** `airmon-ng check kill`은 절대 돌리지 마세요. NetworkManager를 꺼 GX10의 외부 연결이 끊깁니다. 조작 시 `wlx*` 인터페이스만 다루고 내장된 외부 연결 메인 라인 네트워크 카드는 건드리지 마세요.

---

## 5. 적용 시나리오와 제품 선정(Wi-Fi 6 AP 핫스팟, Hub로 연결)

실측 결론을 제품 선정 권장으로 바꾸면: **AWUS036AX의 스위트 스폿은 "Wi-Fi 6 + AP 핫스팟"이면서 동시에 인젝션 성능이 필요한 시나리오입니다.**

| 용도 | AWUS036AX 적합도 | 설명 |
|---|---|---|
| Wi-Fi 6 AP 핫스팟 / 엣지 액세스 | ★ 최우선 | 2x2 VHT80 듀얼 밴드 개설 가능, WPA3-SAE 사용 가능 |
| 인젝션 + 핸드셰이크 감사 | ★ 감당 가능 | 2.4G 96%, 5G 사용 가능, 엔드투엔드 캡처 성공 |
| 최강 수신 / 장거리 모니터 | ○ 충분하나 AXER가 최우선 | 같은 칩의 AXER는 외장 안테나로 수신이 더 강함 |
| 메시 / IBSS 실험 | ✗ 부적합 | 드라이버 N/A, mt76의 ACM / ACHM으로 선택 변경 |

**전형적 배포: Wi-Fi 6 핫스팟으로 삼아 엣지 장치를 중앙 Hub로 연결.** 실측한 AP(VHT80)와 VIF 성능을 활용해 GX10에 이 카드를 조합하면 Wi-Fi 6 액세스 포인트로 배치할 수 있고, 테스트 휴대폰, IoT 센서 같은 엣지 장치가 접속한 뒤 트래픽이 주 인터페이스를 거쳐 중앙 Hub(gateway)로 돌아갑니다. VIF 실측에서 "주 인터페이스로 상위 네트워크에 연결"과 "아래로 AP 개설"이 병행 가능함을 이미 입증했고, STA 측 지연은 3.2 ms이며, 이 토폴로지는 본 플랫폼에서 검증되어 실현 가능합니다. 엣지 액세스 구간에 현대적 암호화를 더하려면 WPA3-SAE를 추가하면 됩니다.

**제품 선정 유의: 인젝션 / 핸드셰이크 용도라면 AWUS036AXM / AXML을 고르지 마세요.** 이 두 카드는 같은 Wi-Fi 6 2x2이고 AP도 열리지만, MediaTek MT7921은 본 플랫폼에서 **인젝션 실패**로 deauth가 불가능하고 핸드셰이크를 캡처하지 못합니다. 고객이 단순히 Wi-Fi 6 AP / 일반 연결 카드만 필요하고 인젝션을 전혀 건드리지 않는다면 MediaTek 제품도 안정적이라 무방합니다. 다만 용도가 무선 감사에 조금이라도 닿는다면 Realtek의 AX(또는 외장 안테나의 AXER)를 선택해야 합니다.

**같은 칩의 AXER와는 어떻게 구분하나?** 둘은 칩, 드라이버, 성능 매트릭스가 일치합니다. AXER는 외장 안테나 버전으로 수신과 장거리 모니터가 더 강합니다(동일 배치 테스트에서 AXER는 주파수 호핑으로 63 AP + 12 client를 스캔). 데스크톱 고정이고 안테나 요구가 높지 않으면 AX를, 거리를 늘리고 최강 수신이 필요하면 AXER를 선택하세요.

---

## 자주 묻는 질문(FAQ)

**Q: AWUS036AX는 Ubuntu 24.04 ARM64에서 드라이버를 설치해야 하나요? lsusb에 0bda:1a2b가 표시되면 어떻게 하나요?**
본문에서 테스트한 kernel 6.17(ASUS GX10)에서는 필요 없습니다. RTL8832BU는 내장 rtw89_8852bu 드라이버로 구동되어 컴파일도 DKMS도 필요 없습니다. lsusb에 `0bda:1a2b`(CD-ROM 모드)가 표시되면 `sudo usb_modeswitch -v 0bda -p 1a2b -K`를 실행해 WLAN으로 전환하세요.

**Q: AWUS036AX는 모니터 모드와 패킷 인젝션을 지원하나요?**
지원합니다. 2.4 GHz 인젝션 29/30(96%); 5 GHz는 AP를 하나씩 지정해 테스트하면 `Injection is working!`을 반환합니다. airodump-ng 주파수 호핑 60초로 14개 AP와 4개 client를 스캔했습니다. 액티브 모니터, IBSS, 메시는 지원하지 않습니다.

**Q: AWUS036AX로 WPA 핸드셰이크를 캡처할 수 있나요? MT7921의 AXM / AXML은 되나요?**
AX는 가능합니다. 본인 소유 AP와 본인 소유 iPhone 7 Plus에서 `aireplay-ng -0`으로 재접속을 유도하고 `airodump-ng`로 완전한 M1–M4를 캡처한 뒤 `hcxpcapngtool`로 .22000을 변환합니다. MT7921의 AXM / AXML은 본 플랫폼에서 인젝션 실패로 할 수 없습니다. 본인 소유 또는 허가된 네트워크에서만 가능합니다.

**Q: AWUS036AX를 AP 핫스팟으로 쓸 수 있나요? WPA3을 지원하나요?**
가능합니다. `hostapd`로 2.4G(802.11n)와 5G(VHT 80 MHz) AP를 열어 iPhone 7 Plus가 접속해 VHT-NSS2 80 MHz로 표시됩니다. WPA3-SAE(ieee80211w=2, sae_pwe=0)는 iPhone 15 Pro로 2.4 GHz에서 접속해 MFP: yes로 표시됩니다(5 GHz WPA3는 실측하지 않음).

**Q: AWUS036AX와 AWUS036AXER의 차이는 무엇인가요? 어느 것을 선택해야 하나요?**
둘 다 RTL8832BU + rtw89_8852bu로 성능 매트릭스가 동일하며, 차이는 안테나와 수신에 있습니다. AXER는 외장 안테나로, 동일 배치 테스트에서 주파수 호핑으로 63 AP + 12 client를 스캔했습니다(AX는 14 AP + 4 client). 데스크톱 고정 용도면 AX, 장거리나 최강 수신이 필요하면 AXER를 선택하세요.

---

## 6. 더 읽어보기

- 〈9종 ALFA 무선 네트워크 카드 ASUS GX10 + Ubuntu ARM64 성능 종합표〉 — 전 모델 모니터 / 인젝션 / AP / 핸드셰이크 한 번에 대조 → [종합표 Hub](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [드라이버 설치 불필요: Ubuntu 24.04 + kernel 6.17에서 in-kernel 드라이버로 모니터와 AP 활성화](/ko/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/) — rtw88 / rtw89 / mt76 공통 설정 흐름
- [AWUS036AXER 카드별 실측](/ko/blog/awus036axer-asus-gx10-ubuntu-test-report/) — 같은 칩의 외장 안테나 버전, 수신과 장거리 모니터 비교
- [WPA3-SAE 핸드셰이크 캡처 성능 실측과 sae_pwe 호환성](/ko/blog/alfa-wpa3-sae-handshake-capability-arm64/) — iPhone 연결의 `sae_pwe` 지뢰밭

---

*테스트 기관: Yopitek(ALFA 총판) — https://www.yupitek.com | 테스트 환경: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 | 대조 장치: Apple iPhone 7 Plus(WPA3 / VIF는 iPhone 15 Pro로 별도 테스트)*
