---
title: "AWUS036ACH 단일 카드 실측: Realtek RTL8812AU 듀얼 안테나 AC1200의 ASUS GX10(ARM64 / Ubuntu 24.04) Monitor · Injection · AP · WPA3 종합 테스트 보고서"
slug: awus036ach-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ach-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ach
  - rtl8812au
  - rtw88-8812au
  - realtek
  - wifi-5
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - alfa-network
  - asus-gx10
  - arm64
description: "AWUS036ACH(RTL8812AU)은 Ubuntu 24.04 / kernel 6.17에서 DKMS 설치가 필요 없으며, 듀얼 밴드 모니터 모드 사용 가능, 패킷 인젝션 100%, 엔드투엔드 WPA handshake(.22000) 실증 완료. 5G 수신 멈춤 등 한계도 함께 다룹니다."
faq:
  - question: "AWUS036ACH은 Kali나 Ubuntu에서 드라이버를 설치해야 하나요?"
    answer: "커널 버전에 따라 다릅니다. Linux 커널 6.13 이상(이번 실측은 Ubuntu 24.04 / kernel 6.17)에는 rtw88_8812au 드라이버가 내장되어 꽂으면 바로 인식되고 컴파일도 DKMS도 필요 없습니다. 커널이 6.13 미만일 때만 DKMS로 lwfinger/rtw88을 따로 설치해야 합니다. Kali는 먼저 uname -r로 커널 버전을 확인하세요. 이번에는 Kali 실기에서 검증하지 않았습니다."
  - question: "AWUS036ACH의 monitor mode와 패킷 인젝션 성능은 어떤가요?"
    answer: "2.4GHz와 5GHz 모두 monitor mode에 들어갈 수 있으며, aireplay-ng 대상별 지향 인젝션은 2.4GHz(4대의 AP 대상)와 5GHz(YUPITEK ch36 대상) 모두 30/30 = 100%입니다. 5GHz 인젝션 전에는 먼저 규제 도메인을 송신 허용 설정으로 바꿔야 하며(예: iw reg set US), 기본 country 00에서는 5GHz 송신이 금지되어 인젝션이 나가지 않습니다."
  - question: "AWUS036ACH은 WPA handshake를 캡처할 수 있나요?"
    answer: "가능하며, 엔드투엔드로 실증되었습니다. 두 밴드 인젝션 모두 100%이고, 2026-11-19 추가 측정에서 자체 iPhone 15 Pro, 5GHz ch36에서 완전한 4-way 핸드셰이크를 캡처했으며 hcxpcapngtool로 47건의 hashcat .22000 hashline을 추출했습니다. 본인 소유 또는 허가된 네트워크에서만 진행합니다."
  - question: "AWUS036ACH으로 WPA3 핫스팟을 열었는데 iPhone 7 Plus가 연결되지 않으면 어떻게 하나요?"
    answer: "hostapd에서 sae_pwe=0을 설정하고 ieee80211w=2를 함께 써야 iPhone 7 Plus가 연결됩니다. sae_pwe=2를 쓰면 연결되지 않습니다. 같은 설정이 AWUS036ACHM에서도 핵심입니다."
  - question: "AWUS036ACH의 5GHz 수신이 갑자기 멈추면(0 패킷 캡처) 어떻게 하나요?"
    answer: "이것은 rtw88_8812au의 알려진 현상입니다. 모드를 반복 전환하거나 규제 도메인을 변경한 뒤 5GHz 수신이 멈출 수 있으며, 소프트웨어로는 복구되지 않아 물리적으로 뽑았다 꽂거나 재부팅할 수밖에 없습니다. 5GHz 테스트 전에 카드를 먼저 다시 꽂고, 5GHz 항목을 우선 완료하기를 권장합니다."
draft: false
---

> 테스트 기관: Yopitek(ALFA Network 대만 유통사) | 테스트 플랫폼: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | 테스트 기기: 자체 Apple iPhone 7 Plus | 테스트 대상: 자체 사무실 Wi-Fi(SSID `YUPITEK`, 2.4G ch5 / 5G ch36, 157) | 테스트 일자: 2026-11-18.
>
> 본 글은 유통사가 제품 호환성과 능력 경계를 검증한 하드웨어 검증입니다. 모든 Monitor / Injection / AP / handshake 측정은 Yopitek 자체 장비, 자체 사무실 Wi-Fi에서 자체 테스트용 스마트폰을 대상으로 진행했으며, 어떠한 제3자 네트워크도 대상으로 하지 않고 외부 네트워크에 대한 공격 행위 절차도 제공하지 않습니다. 본문의 데이터는 모두 실기에서 측정한 수치와 상태이며, 사양서로 추측하지 않았습니다.

## 핵심 요약(TL;DR)

ASUS GX10 / Ubuntu 24.04 ARM64(kernel 6.17) 실측에서 AWUS036ACH는 듀얼 밴드 monitor 모드가 가능하고, AP별 패킷 인젝션은 두 밴드 모두 30/30 = 100%이며, 두 밴드 모두 AP 핫스팟을 구성할 수 있습니다(순수 802.11g / 순수 802.11a).

- kernel 6.13 이상이면 DKMS 설치 불필요(이번 Ubuntu 24.04 / kernel 6.17), rtw88_8812au 내장, 꽂으면 바로 인식.
- 듀얼 밴드 모니터 모드(monitor mode) 사용 가능, 두 밴드 대상별 패킷 인젝션 모두 30/30 = 100%.
- 엔드투엔드 WPA handshake 실증 완료: 2026-11-19 추가 측정에서 자체 iPhone 15 Pro, 5G ch36에서 완전한 4-way를 캡처하여 47건의 .22000 hashline 추출.
- 5GHz 수신이 멈출 수 있으며, 물리적으로 뽑았다 꽂거나 재부팅해야 합니다.
- 단일 기기 IBSS 생성 가능하지만, 802.11s mesh, active monitor, Wi-Fi Direct(P2P)는 지원하지 않습니다.

## 1. 이 카드와 테스트 플랫폼

AWUS036ACH은 ALFA Network이 "듀얼 안테나 고이득"으로 포지셔닝한 USB 무선 네트워크 카드로, Realtek RTL8812AU 칩을 채택했으며 사양은 Wi-Fi 5(802.11ac), 2T2R, 듀얼 밴드 AC1200입니다. 같은 시리즈의 단일 안테나 AWUS036ACHM(MediaTek MT7610U, AC600)에 비해, ACH은 두 개의 외장 고이득 안테나로 더 나은 수신과 더 안정적인 injection 성능을 얻으며, 고객이 "장거리 monitor"와 "두 밴드 인젝션"을 문의할 때 자주 오르는 후보입니다.

이번 테스트 플랫폼과 조건은 다음과 같습니다.

- 연산 플랫폼: ASUS GX10(ARM64 / aarch64)
- 운영체제: Ubuntu 24.04 LTS
- 커널 버전: kernel 6.17.0-1014-nvidia
- 테스트 기기: Apple iPhone 7 Plus(2.4G / 5G / WPA3 모두 이 기기로 실측)
- 테스트 환경: 자체 사무실 Wi-Fi, SSID `YUPITEK`(2.4GHz ch5 / 5GHz ch36, ch157)
- 테스트 일자: 2026-11-18 실기 측정

전 과정에서 ALFA 카드에 해당하는 `wlx*` 인터페이스만 조작하고, GX10 외부 인터넷용 내장 네트워크 카드는 건드리지 않으며, `airmon-ng check kill`도 실행하지 않습니다(이 명령은 NetworkManager를 꺼서 호스트를 끊어버립니다).

## 2. 하드웨어와 드라이버(칩 / USB ID / in-kernel 무설치)

| 항목 | 사양 |
|---|---|
| 모델 | AWUS036ACH |
| 칩 | Realtek RTL8812AU |
| USB ID | `0bda:8812` |
| 드라이버 | `rtw88_8812au`(kernel 내장, mainline ≥ 6.13) |
| 펌웨어 | `rtw88/rtw8812a_fw.bin`(시스템 내장) |
| 세대 / 스트림 | Wi-Fi 5(802.11ac) / 2T2R |
| 대역폭 등급 | 듀얼 밴드 AC1200 |
| 안테나 | 듀얼 안테나 고이득(외장) |
| USB 인터페이스 | USB 3.0(실측 열거는 5000M) |

ACH은 GX10의 6.17 kernel에서 진정한 플러그 앤 플레이입니다. `lsusb`가 `0bda:8812`를 인식하고, 드라이버 `rtw88_8812au`가 자동으로 바인딩되며, 펌웨어 `rtw8812a_fw.bin`은 시스템에 이미 내장되어 있어 컴파일도 DKMS도 필요 없습니다. 이 점은 ARM64 환경에서 특히 중요합니다. 많은 구형 out-of-tree Realtek 드라이버는 aarch64에서 소스부터 컴파일해야 하지만, morrownr/USB-WiFi와 aircrack-ng/rtl8812au라는 두 오래된 프로젝트는 지금 모두 이 내장 드라이버로 방향을 틀었고, 버그 리포트는 lwfinger/rtw88으로 모이고 있습니다. 따라서 kernel ≥ 6.13(GX10의 6.17 포함) 사용자는 더 이상 서드파티 DKMS를 건드릴 필요가 없으며, 구형 kernel(< 6.13)에서만 DKMS로 `lwfinger/rtw88`을 따로 설치해야 합니다. 이 상위 프로젝트는 현재도 활발히 유지되고 있어(최신 commit은 2026-10-24, 내용에 8812A의 블루투스 1T1R 수정 포함), 이 칩에 대한 mainline 지원이 계속 갱신되고 있음을 보여줍니다. 업데이트가 끊긴 구형 드라이버가 아닙니다.

하드웨어 연결에는 유의할 세부 사항이 하나 있습니다. ACH은 USB-A 수 커넥터이므로, USB-C→A 어댑터로 GX10의 USB-C 포트에 직접 꽂아 USB 3.0(열거 표시 5000M)으로 동작시키십시오. 키보드·마우스의 USB 2.0 hub 뒤에 연결하면 속도가 제한되어 USB3의 동작을 측정할 수 없습니다.

인터페이스 모드 측면에서, `iw phy`는 IBSS / managed / AP / AP-VLAN / monitor 지원을 보고하지만 mesh, P2P, active-monitor는 없으며, 이 경계가 4절의 일부 한계를 직접 결정합니다.

## 3. 실측 능력: Monitor / Injection / AP / WPA3

| 기능 | 2.4 GHz | 5 GHz | 실측 데이터 |
|---|---|---|---|
| Monitor | ✅ | ✅ | 2.4G ch1/6/11 = 92/214/71 frames; 5G ch36/149/157 = 260/137/127 frames |
| Injection(브로드캐스트 탐색) | ✅ | ✅ | `aireplay-ng --test` broadcast probe 두 밴드 모두 Injection is working 반환 |
| Injection(대상별 지향) | ✅ 30/30 = 100% | ✅ 30/30 = 100% | 2.4G는 4대의 AP(YUPITEK 포함) 대상; 5G는 YUPITEK ch36 대상 |
| AP 핫스팟(iPhone 7 Plus) | ✅ 순수 802.11g | ✅ 순수 802.11a(ch36) | 4-way handshake 완료, 첫 시도에 바로 연결 |
| WPA3-SAE AP | ✅(`sae_pwe=0`) | 미실측 | `ieee80211w=2`와 함께, iPhone 7 Plus 연결(2.4 GHz에서만 실측) |

**Monitor**: 2.4GHz는 ch1 / ch6 / ch11에서 각각 92 / 214 / 71개의 frame을 포착했고, 5GHz는 ch36 / ch149 / ch157에서 260 / 137 / 127개의 frame을 포착했습니다. 두 밴드 monitor 모두 정상이며, 5GHz의 수신량은 2.4GHz보다 오히려 높아(ch36에서 260 frame 포착) 듀얼 안테나 고이득 포지셔닝과 부합합니다.

**Injection**: 이것이 ACH의 강점입니다. 2.4GHz에서 `aireplay-ng --test`는 먼저 broadcast probe를 수행하고(Injection is working, Found 4 APs 보고), 이어서 대상별 지향으로 YUPITEK을 포함한 4대의 AP에 대해 응답률 모두 30/30 = 100%, min/avg/max RTT 약 4.9 / 39.2 / 99.0 ms, Power 약 -47이었습니다. 듀얼 안테나 ACH의 2.4G injection은 단일 안테나 ACHM보다 분명히 더 안정적입니다. 실무상 `--ignore-negative-one`을 추가하는 것을 기억해야 합니다. 이는 lwfinger/rtw88 #453의 알려진 현상으로, STA 인터페이스가 켜져 있을 때 monitor channel이 `-1`을 보고할 수 있고, 이 플래그를 추가하지 않으면 인젝션 실패로 오판됩니다. 또한 상위 기록에 따르면 고부하 injection 시 내장 driver가 간혹 USB reset을 일으키지만, 이번 약 90초 측정에서는 관찰되지 않았습니다. 5GHz에서 YUPITEK(ch36) 대상별 지향도 마찬가지로 30/30 = 100%, 평균 RTT 13.6 ms, Power -69.1이었습니다. 이는 "카드를 새로 꽂고 + regdomain을 TX 가능한 규제로 설정"한 전제에서 측정한 결과입니다(자세한 내용은 4절의 5G 주의 사항 참조).

**AP 핫스팟**: hostapd로 개설하여 2.4GHz는 순수 802.11g(`ieee80211n=0`), 5GHz는 순수 802.11a(ch36)로 했고, iPhone 7 Plus가 두 밴드 모두 첫 시도에 바로 연결되어 association 실패가 없었습니다. log에서 authenticated → associated → AP-STA-CONNECTED → EAPOL-4WAY-HS-COMPLETED의 완전한 네 단계를 볼 수 있습니다. 실측 경험상 ACH은 "802.11n을 끄고 순수 g / 순수 a" 설정에서 연결이 가장 깔끔합니다.

**WPA3-SAE**: SAE-only AP를 열 때 핵심 파라미터는 `sae_pwe=0`(hunting-and-pecking)에 `ieee80211w=2`를 조합하는 것이며, 그래야 iPhone 7 Plus가 연결됩니다. `sae_pwe=2`를 쓰면 연결되지 않습니다. 이는 같은 시리즈 ACHM이 겪은 것과 동일한 호환성 함정입니다.

## 4. 고급 능력과 handshake: 가능 범위와 정직한 한계

| 고급 능력 | 결과 | 설명 / 근거 |
|---|---|---|
| VIF(STA + monitor 동시) | ✅ 실측 가능 | 주 인터페이스 managed와 `mon9`(monitor) 동시 up, monitor VIF 8초에 100 frame 포착 |
| WPA handshake 캡처 | ✅ 엔드투엔드(.22000) 실증 완료 | 두 밴드 인젝션 100%; 2026-11-19 추가 측정 5G ch36에서 완전한 4-way 캡처, hcxpcapngtool로 47건 `.22000` hashline 추출 |
| macchanger(MAC 변경) | ✅ | 랜덤 MAC 설정과 복원 모두 정상(먼저 `ip link down` 필요) |
| Ad-hoc(IBSS) | 🟡 단일 기기 | 단일 기기 `Joined IBSS` 성공; peer link는 두 번째 기기가 없어 미측정 |
| Active monitor | ❌ | `Operation not supported (-95)` |
| Mesh(802.11s) | ❌ | `Operation not supported (-95)` |
| Wi-Fi Direct(P2P) | ❌ | `Operation not supported (-95)` |

**handshake 캡처 능력은 분명히 짚어야 합니다**: ACH의 두 밴드 injection은 모두 100%이며, injection은 바로 "자체 테스트용 스마트폰 deauth → 완전한 4-way(M1–M4) 캡처 → hcxpcapngtool로 hashcat `.22000` 추출"이라는 엔드투엔드 작업 흐름의 발동 측입니다. 2026-11-19 추가 측정에서 자체 iPhone 15 Pro, 5GHz ch36에서 완전한 4-way 핸드셰이크를 캡처했고 hcxpcapngtool로 47건의 `.22000` hashline을 추출했으므로, ACH의 엔드투엔드 handshake 캡처는 실증되었습니다. 우리 9종 카드 종합표에서 엔드투엔드(`.22000`)가 실증된 것은 9종 중 7종입니다: AWUS036ACM, AWUS036ACHM, AWUS036ACH, AWUS036ACS, AWUS036EACS, AWUS036AX, AWUS036AXER. 모든 캡처는 본인 소유 또는 허가된 네트워크에서만 진행합니다.

**VIF**: `iw phy`의 플래그에는 interface combinations are not supported라고 적혀 있지만, 실기에서는 managed 주 인터페이스와 별도로 연 monitor 인터페이스 `mon9`을 동시에 up할 수 있고, `mon9`이 8초 안에 100개의 frame을 포착하여 "인터넷하면서 측면 기록"이 ACH에서 통한다는 것을 보여줍니다. 다만 유의할 점은 phy가 이 조합을 보장하지 않으므로, 장시간이나 고부하 시나리오에서는 mt76 계열(ACM / ACHM)로 바꾸기를 권장합니다.

**특별히 표기해야 할 세 가지 한계:**

1. **Active monitor, Mesh(802.11s), Wi-Fi Direct(P2P) 미지원**: 세 가지 모두 실측에서 `Operation not supported (-95)`를 반환합니다. 이 세 능력이 필요하면 mt76 계열 카드(ACM / ACHM의 phy가 mesh / P2P / active-monitor를 선언)로 바꾸십시오.
2. **5G RX 멈춤(`rtw88_8812au` 알려진 현상)**: 카드를 막 꽂았을 때는 5G monitor / injection이 정상이지만, 모드를 반복 전환하거나 regdomain을 변경한 뒤 5G 수신이 멈출 수 있고(0 패킷 캡처), 소프트웨어로는 복구되지 않아 물리적으로 뽑았다 꽂거나 재부팅할 수밖에 없습니다. 5G 테스트 전에 한 번 뽑았다 꽂고 5G 항목을 우선 완료하기를 권장합니다. 여기서 5G injection이 송신될 수 있는 전제도 보충합니다. 기본 `country 00`에서는 5G 전체가 passive / no-IR(TX 금지)이므로 지향 인젝션이 아예 나가지 못합니다. TX 가능한 규제로 설정해야 하며(`iw reg set US`는 ch36 / ch149를 잠금 해제, `TW`는 ch149 이상만 허용하고 ch36은 제외), 측정 후 다시 `TW`로 되돌립니다. 그리고 "카드를 새로 꽂음"이란 물리적으로 뽑았다 꽂아 USB가 재열거되는 것을 뜻합니다. `dmesg`에서 `USB disconnect`와 `renamed from wlan0`, bus 번호 변경이 보여야 인정됩니다. 5G가 이미 멈췄다면 aireplay는 `No such BSSID available`을 반환합니다.
3. **hcxdumptool은 이 플랫폼에서 2.4 GHz의 AWUS036EACS를 제외한 모든 카드가 `failed to arm`**: active-monitor를 요구하는데 rtw88 / rtw89 / mt7921u 모두 지원하지 않기 때문입니다. handshake를 캡처하려면 airodump-ng + aireplay-ng 경로로 바꾸십시오.

### 툴체인 호환성(Kali)

Kali에서 자주 쓰는 도구를 ACH에 대해 한 차례 빠르게 선별했으며(환경 대상은 자체 `YUPITEK`), 결과는 다음과 같습니다.

| 도구 | 상태 | 설명 |
|---|---|---|
| airmon-ng | ✅ | `phy2 / wlx... / rtw88_8812au / RTL8812AU 2T2R`을 정확히 나열 |
| Wireshark / tshark | ✅ | `tshark -i $IF`로 beacon(YUPITEK 포함) 포착, 20 packets captured |
| kismet | ✅ 설치됨 | `/usr/bin/kismet`, data source로 시작 가능 |
| bettercap | ✅ 설치됨 | `/usr/bin/bettercap` |
| hcxdumptool | ⚠️ | 설치됨, 그러나 이 플랫폼에서 `failed to arm`(active-monitor 필요, 위 참조) |
| macchanger | ✅ | GNU 1.7.0; `-r` 랜덤, `-p` 복원, 실측 정상 |
| wifite | ❌ 미설치 | 본 기기에 이 명령 없음, 따로 설치 필요(자체 컴파일 aircrack-ng와의 apt 의존성 충돌을 피하려면 git 버전 권장) |

결론은 단순합니다. airmon-ng는 ACH을 정확히 인식·관리할 수 있고, 일반 monitor와 캡처 과정은 aircrack-ng 패키지(airodump-ng + aireplay-ng)로 가는 것이 가장 안정적이며, active-monitor가 필요한 hcxdumptool은 이 플랫폼에서 arm할 수 없으니 거기에 매달리지 마십시오.

## 5. 적용 시나리오와 제품 선정 권장(종합표 Hub로 돌아가기)

ACH을 제품 라인 전체로 놓고 보면, 그 포지셔닝은 매우 분명합니다. 듀얼 안테나 고이득, 두 밴드 injection 100%, 엔드투엔드 WPA handshake(.22000) 실증 완료로, "안정적인 인젝션이 필요하면서 더 강한 수신도 원하는" 고객의 실용적 선택입니다.

- **침투 테스트(injection + handshake)**: 최우선 그룹은 AWUS036EACS / AWUS036ACH / AWUS036ACS로, 셋 다 두 밴드 인젝션 성능이 상위권입니다.
- **최강 수신 / 장거리 monitor**: AWUS036AXER와 AWUS036ACH이며, ACH은 듀얼 안테나 고이득이 강점입니다.
- **802.11s mesh / active-monitor / P2P가 필요한 경우**: ACH(Realtek rtw88)은 하지 못합니다(실측 `-95` 반환). mt76 드라이버의 AWUS036ACM / AWUS036ACHM으로 바꾸십시오. ACH의 IBSS는 단일 기기 생성만 가능하며 peer-link는 미측정입니다.
- **순수 AP나 일반 연결만 필요하고 인젝션은 하지 않는 경우**: MediaTek의 AWUS036AXM / AXML이 더 안정적이지만, 이 두 장은 이 플랫폼에서 인젝션 실패이므로 침투 용도에는 적합하지 않음에 유의하십시오.

한마디로 함정 회피: 고객의 요구가 명확히 인젝션과 handshake라면 AWUS036AXM / AXML을 선택하지 마십시오(MT7921 칩의 인젝션은 이 플랫폼 실측에서 실패하여 deauth도 handshake 캡처도 불가능합니다). 이런 요구에는 오히려 ACH이 안정적인 후보입니다. 제품 선정 시 대역폭 수치만 보지 마십시오. 듀얼 안테나 고이득이 주는 수신 안정성은 실제 측면 기록 거리에서 지면 사양보다 체감 차이가 큰 경우가 많습니다. 제품 선정 결정과 플랫폼 공통 함정은 종합표 Hub를 참조하세요: [9종 ALFA 무선 네트워크 카드의 ASUS GX10(ARM64) Monitor · Injection · AP 전체 매트릭스](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 자주 묻는 질문(FAQ)

**Q: AWUS036ACH은 Kali나 Ubuntu에서 드라이버를 설치해야 하나요?**
커널 버전에 따라 다릅니다. Linux 커널 6.13 이상(이번 실측 Ubuntu 24.04 / kernel 6.17)에는 rtw88_8812au 드라이버가 내장되어 꽂으면 바로 인식되고 컴파일도 DKMS도 필요 없습니다. 커널이 6.13 미만일 때만 DKMS로 lwfinger/rtw88을 따로 설치해야 합니다. Kali는 먼저 uname -r로 커널 버전을 확인하세요. 이번에는 Kali 실기에서 검증하지 않았습니다.

**Q: AWUS036ACH의 monitor mode와 패킷 인젝션 성능은 어떤가요?**
2.4GHz와 5GHz 모두 monitor mode에 들어갈 수 있으며, aireplay-ng 대상별 지향 인젝션은 2.4GHz(4대의 AP 대상)와 5GHz(YUPITEK ch36 대상) 모두 30/30 = 100%입니다. 5GHz 인젝션 전에는 먼저 규제 도메인을 송신 허용 설정으로 바꿔야 하며(예: iw reg set US), 기본 country 00에서는 5GHz 송신이 금지되어 인젝션이 나가지 않습니다.

**Q: AWUS036ACH은 WPA handshake를 캡처할 수 있나요?**
가능하며, 엔드투엔드로 실증되었습니다. 두 밴드 인젝션 모두 100%이고, 2026-11-19 추가 측정에서 자체 iPhone 15 Pro, 5GHz ch36에서 완전한 4-way 핸드셰이크를 캡처했으며 hcxpcapngtool로 47건의 hashcat .22000 hashline을 추출했습니다. 본인 소유 또는 허가된 네트워크에서만 진행합니다.

**Q: AWUS036ACH으로 WPA3 핫스팟을 열었는데 iPhone 7 Plus가 연결되지 않으면 어떻게 하나요?**
hostapd에서 sae_pwe=0을 설정하고 ieee80211w=2를 함께 써야 iPhone 7 Plus가 연결됩니다. sae_pwe=2를 쓰면 연결되지 않습니다. 같은 설정이 AWUS036ACHM에서도 핵심입니다.

**Q: AWUS036ACH의 5GHz 수신이 갑자기 멈추면(0 패킷 캡처) 어떻게 하나요?**
이것은 rtw88_8812au의 알려진 현상입니다. 모드를 반복 전환하거나 규제 도메인을 변경한 뒤 5GHz 수신이 멈출 수 있으며, 소프트웨어로는 복구되지 않아 물리적으로 뽑았다 꽂거나 재부팅할 수밖에 없습니다. 5GHz 테스트 전에 카드를 먼저 다시 꽂고, 5GHz 항목을 우선 완료하기를 권장합니다.

## 6. 더 읽어보기

- 종합표 Hub: [9종 ALFA 무선 네트워크 카드 ARM64 전체 매트릭스](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 드라이버 설치 불필요로 Ubuntu(ARM64)에서 Monitor와 AP 활성화: [준비 중, 링크 작업 중](/ko/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- WPA3-SAE handshake 캡처와 `sae_pwe` 호환성: [준비 중, 링크 작업 중](/ko/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 자매 카드 대조: AWUS036ACHM(단일 안테나 AC600) 단일 카드 실측 [준비 중, 링크 작업 중]
- 본 모델 전체 근거 경로(내부): `AWUS036ACH_evidence/`(p0 열거, p1_gx10 동작, retest 조사)

<!-- hreflang: zh-TW가 원고 기준; zh-CN / en / ja / ko / de / fr / es는 원고 확정 후 생성하여 rel=alternate 보완. -->
