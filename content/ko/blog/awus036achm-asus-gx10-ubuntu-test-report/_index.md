---
title: "AWUS036ACHM 카드별 실측 테스트: MediaTek MT7610U 단일 안테나 AC600의 ASUS GX10(ARM64 / Ubuntu 24.04) Monitor · Injection · AP · WPA3 능력"
slug: awus036achm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036achm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036achm
  - alfa-network
  - mt7610u
  - mt76x0u
  - wifi-5
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - sae-pwe
  - ubuntu-24-04
  - arm64
description: "AWUS036ACHM(MT7610U)은 Ubuntu 24.04에서 드라이버 설치 불필요하며, 듀얼 밴드 모니터 모드 사용 가능, 2.4G 패킷 인젝션 96–100%. AP 개설 시 802.11n을 꺼야 하고, WPA3는 sae_pwe=0으로 설정해야 구형 iPhone이 연결됩니다."
faq:
  - question: "AWUS036ACHM은 Ubuntu 24.04에서 드라이버를 설치해야 하나요?"
    answer: "필요 없습니다. MT7610U는 커널에 내장된 mt76x0u 드라이버가 담당하므로 Ubuntu 24.04(kernel 6.17)에서 꽂으면 바로 인식되며, DKMS도 추가 펌웨어도 필요 없습니다. lsusb에서 USB ID 0e8d:7610을 확인할 수 있습니다."
  - question: "AWUS036ACHM은 monitor mode에 들어갈 수 있나요? 몇 개의 AP를 스캔할 수 있나요?"
    answer: "가능합니다. 2.4GHz와 5GHz 모두 monitor mode에 들어갈 수 있으며, airodump-ng로 채널 호핑 전체 밴드 스캔을 120초 돌린 결과 19개의 AP와 14개의 클라이언트를 스캔했고, ch1, 2, 5, 6, 36, 149, 157에 분포했습니다."
  - question: "AWUS036ACHM의 패킷 인젝션 성공률은 얼마인가요? 5GHz도 가능한가요?"
    answer: "2.4GHz 6번 채널에서 대상별 인젝션 응답률은 96–100%입니다(aireplay-ng --test, 4대의 AP 발견). 5GHz(ch36, ch149)는 브로드캐스트 인젝션만 사용 가능함을 확인했고, 대상별 테스트는 Found 0 APs를 보고하여 이번에는 백분율을 얻지 못했으며 원인은 추후 조사 예정입니다."
  - question: "AWUS036ACHM으로 AP를 개설할 때 iPhone에 '네트워크에 연결할 수 없음' 또는 '비밀번호 오류'가 뜨면 어떻게 하나요?"
    answer: "먼저 802.11n을 끄세요. hostapd 설정 파일에 ieee80211n=1과 ht_capab을 넣지 말고, 2.4GHz는 순수 hw_mode=g, 5GHz는 순수 hw_mode=a(20 MHz)를 사용하세요. 그렇지 않으면 hostapd가 handle_assoc_cb: STA not found를 반복해서 띄우고, 화면은 비밀번호 오류처럼 보이지만 실제로는 802.11n 연계(association) 실패입니다."
  - question: "AWUS036ACHM의 WPA3-SAE가 왜 구형 iPhone에서 연결되지 않나요?"
    answer: "대개 hostapd의 sae_pwe 설정 때문입니다. 실측 결과 sae_pwe=0일 때 iPhone 7 Plus와 iPhone 15 Pro 모두 연결되지만, sae_pwe=2일 때는 iPhone 7 Plus가 연계는 성공하지만 4-way 핸드셰이크 실패로 끊어져 비밀번호 오류처럼 보입니다. ieee80211w=2와 함께 설정하고, 설정 변경 후에는 iPhone에서 해당 네트워크를 먼저 삭제한 뒤 다시 연결하세요."
draft: false
---

> 테스트 기관: Yupitek(ALFA Network 대만 유통사) | 테스트 플랫폼: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia` | 테스트 기기: 자체 iPhone 7 Plus(WPA3는 iPhone 15 Pro로 추가 측정) | 테스트 대상: 자체 사무실 Wi-Fi(SSID `YUPITEK`, 2.4G ch5 / 5G ch36, 157).
>
> 본 글은 유통사가 제품 호환성과 능력 경계를 검증한 하드웨어 검증입니다. 모든 Monitor / Injection / AP / WPA3 테스트는 Yupitek 자체 장비, 자체 사무실 Wi-Fi에서 자체 테스트용 스마트폰을 대상으로 진행한 정당한 능력 검증이며, 어떠한 제3자 네트워크도 대상으로 하지 않고 공격 행위 절차도 제공하지 않습니다. 본문의 injection은 probe request만 보내 능력을 자체 테스트한 것으로, 공격 패킷을 보내지 않습니다.

## 핵심 요약(TL;DR)

ASUS GX10 / Ubuntu 24.04 ARM64(kernel 6.17) 실측에서 AWUS036ACHM은 듀얼 밴드 monitor 모드가 가능하고, 2.4G 패킷 인젝션은 96–100%(5G는 브로드캐스트 인젝션만 확인)이며, 두 밴드 모두 AP 핫스팟을 구성할 수 있습니다(802.11n 비활성화 필요).

- Ubuntu 24.04 드라이버 설치 불필요: MT7610U는 kernel 6.17에 내장된 mt76x0u가 담당하여 꽂으면 바로 인식되며, DKMS도 추가 펌웨어도 필요 없습니다.
- 듀얼 밴드 모니터 모드(monitor mode) 사용 가능; 2.4G 패킷 인젝션 96–100%.
- 5GHz는 브로드캐스트 인젝션만 확인했고, 대상별 응답률은 이번에 얻지 못했습니다(원인 추후 조사).
- AP 개설 시 802.11n을 꺼야 하며, WPA3는 `sae_pwe=0`으로 설정해야 구형 iPhone이 연결됩니다.
- 단일 안테나 1T1R(AC600)로, 처리량과 포지셔닝이 2T2R의 ACM / ACH와 다른 급입니다.

## 1. 이 카드와 이 플랫폼

AWUS036ACHM은 ALFA의 단일 안테나 AC600 카드로, 칩은 MediaTek MT7610U이며 대응하는 Linux 내장 드라이버는 `mt76x0u`입니다. AWUS036ACM(MT7612U, 2T2R)의 단일 스트림 자매 모델로, 사양상 1T1R(AC600)이라 공간 스트림이 하나 적지만, 그 대신 더 작은 크기와 커뮤니티에서 인정받는 장거리 수신을 얻습니다. morrownr/USB-WiFi 커뮤니티는 이를 Kali 추천 목록과 "The Short List"에 올렸고, VIF, Active monitor, WPA3 모두 Yes, Very Long range, 단일 스트림, in-kernel로 표기했습니다.

우리는 이를 ASUS GX10(NVIDIA GB10, 128GB UMA, ARM64)에 꽂아 Ubuntu 24.04 LTS, kernel 6.17에서 Monitor, Injection, AP, WPA3-SAE를 항목별로 측정했습니다. 먼저 결론부터 말하면, 이 카드는 이 플랫폼에서 사용할 수 있고 2.4GHz의 능력도 상당히 완전합니다. 다만 먼저 알아야 할 호환성 함정이 두 가지 있습니다. AP 개설 시 반드시 802.11n을 꺼야 하고, WPA3는 반드시 `sae_pwe=0`으로 설정해야 합니다. 또한 5GHz의 대상별 injection은 이번에 브로드캐스트만 확인했습니다. 아래 표는 전체 개요입니다.

| 능력 항목 | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor(측면 기록) | ✅ | ✅ |
| Injection(인젝션) | ✅ 96–100% | ⚠️ 브로드캐스트만 가능, 대상별 응답률 미취득 |
| AP 핫스팟 | ✅(순수 802.11g 필요) | ✅(순수 802.11a, 20 MHz 필요) |
| WPA3-SAE | ✅(`sae_pwe=0` 필요) | 미실측 |

> 범례: ✅ 실측 통과 | 🟡 일부 또는 단일 기기에서 성립 | ⚠️ 제한 있음 | ❌ 미지원 또는 실패.

## 2. 하드웨어와 드라이버(무설치)

ACHM을 GX10에 꽂으면 kernel 6.17에 내장된 `mt76x0u`가 바로 인식하며, DKMS도 추가 펌웨어도 필요 없고 GitHub에서 out-of-tree 드라이버를 컴파일할 필요도 없습니다. 네트워크 카드를 확인하는 세 가지 명령은 다음과 같습니다.

```bash
lsusb | grep 0e8d:7610
# Bus 003 Device 005: ID 0e8d:7610 MediaTek Inc. WiFi

sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cababcd2
```

인터페이스 이름은 MAC으로 명명되며(`wlx<MAC>`), 카드를 다시 꽂아도 이름이 변하지 않으므로 스크립트 작성 시 바로 바인딩할 수 있습니다. `iw phy info`가 선언한 지원 인터페이스 모드에는 `managed`, `AP`, `monitor`, `mesh point`, `IBSS`, `P2P-client`, `P2P-GO`가 포함되어 본 글에서 테스트할 모든 시나리오를 아우릅니다.

플랫폼 공통의 안전 수칙 두 가지는 ACHM에서도 그대로 적용됩니다. 첫째, `airmon-ng check kill`을 절대 실행하지 않습니다. 그러면 NetworkManager가 꺼져 GX10이 외부와 끊어집니다. 둘째, 전 과정에서 `wlx*` 인터페이스만 조작하고 내장 `wlP9s9`(GX10 외부 인터넷 주회선)은 건드리지 않습니다. monitor/AP에 들어갈 때는 항상 `iw`에 `nmcli dev set $IF managed no`를 조합해 사용하여 시스템 주 네트워크 카드를 건드리지 않습니다.

## 3. 실측 능력: Monitor / Injection / AP / WPA3

### 3-1. Monitor(2.4 + 5 GHz) ✅

두 밴드의 측면 기록 모두 정상입니다. 2.4GHz 6번 채널은 8초 만에 300패킷의 캡처 상한에 도달했고, 5GHz는 주파수별 활동량에 따라 다릅니다. ch36(5180)은 8초 만에 300개, 5745는 254개, 5785는 54개를 받았습니다(어떤 채널의 패킷이 적다는 것은 보통 당시 그 채널에 활성 AP가 없다는 뜻이며 네트워크 카드 문제가 아닙니다).

채널 호핑 전체 밴드 스캔이 단일 안테나 카드의 수신 실력을 가장 잘 드러냅니다.

```bash
sudo timeout -s INT 120 airodump-ng --band abg $IF
```

실측 120초 동안 19개의 기지국, 14개의 클라이언트를 스캔했고 ch1/2/5/6/36/149/157에 분포했습니다. 단일 스트림 AC600 카드로서는 이 정도 커버리지가 안정적인 측면 기록 소스로 쓰기에 충분하며, 커뮤니티가 매긴 "Very Long range" 평가와도 부합합니다.

### 3-2. Injection(2.4 + 5 GHz)

이것이 ACHM에서 두 밴드의 차이가 가장 뚜렷한 지점이자, 제품 선정 시 특별히 유의해야 할 항목입니다.

2.4GHz 6번 채널에서 `aireplay-ng --test` 능력 자체 테스트를 하면 결과가 훌륭합니다.

```text
Injection is working!
Found 4 APs
30/30: 100%
```

네 대의 기지국 응답률이 96–100%에 들어, 인젝션 능력이 완전합니다.

하지만 5GHz로 바꾸면(ch36과 ch149 모두 시도) 달라집니다.

```text
Injection is working!
Found 0 APs
```

즉, 5GHz의 브로드캐스트 인젝션은 사용 가능하지만(드라이버가 `Injection is working!`을 보고), `aireplay-ng --test`의 대상별 응답률은 두 5G 채널 모두에서 `Found 0 APs`였으며, 이번에는 백분율을 얻지 못했습니다. 이는 ACHM이라는 단일 안테나 카드가 이 플랫폼에서 보인 실측 현상이며, 원인은 추적 조사가 필요합니다. 우리는 측정하지 못한 수치를 임의로 채워 넣지 않습니다. 정직하게 말하면, 용도상 안정적인 5GHz 대상별 인젝션이 필요하다면 ACHM은 이번에 2.4GHz에서만 완전한 인젝션율을 확인했습니다.

### 3-3. AP 핫스팟(2.4 + 5 GHz) ✅ — 단, 반드시 802.11n을 꺼야 함

ACHM의 첫 번째 호환성 함정이 여기 있습니다. AP 개설 시 hostapd 설정 파일에 `ieee80211n=1`과 `ht_capab`을 넣지 않습니다. 2.4GHz는 순수 `hw_mode=g`, 5GHz는 순수 `hw_mode=a`(20 MHz)를 씁니다. 최소 사용 가능한 2.4GHz 설정은 다음과 같습니다.

```ini
interface=wlx00c0cababcd2
driver=nl80211
ssid=ALFA-TEST-ACHM-24
# 순수 802.11g, ieee80211n=1 이나 ht_capab 을 추가하지 말 것
hw_mode=g
channel=6
country_code=TW
wmm_enabled=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=최소 8자 이상의 본인 비밀번호로 변경
```

실측에서 iPhone 7 Plus는 두 밴드 모두 연결되었습니다. 2.4GHz는 `AP-STA-CONNECTED`에 이어 `EAPOL-4WAY-HS-COMPLETED`가 보였고, 5GHz(ch36, 20 MHz)는 -71 dBm, rx 54 Mbit, `authorized: yes`로 측정되었습니다.

반대로 설정 파일에 `ieee80211n=1`을 남겨두면 hostapd가 `handle_assoc_cb: STA not found`를 반복해서 내뱉고, iPhone 화면에는 "네트워크에 연결할 수 없음" 또는 "비밀번호 오류"가 뜨지만, 그것은 사실 802.11n 연계 실패이지 비밀번호 문제가 아닙니다. 802.11n을 제거하면 해결됩니다. ACHM은 단일 안테나 카드이므로 5GHz AP는 이번에 20 MHz를 채택했고 VHT80은 시도하지 않았습니다.

### 3-4. WPA3-SAE ✅ — 단, 반드시 `sae_pwe=0`(가장 빠지기 쉬운 호환성 함정)

ACHM의 두 번째이자 가장 따로 짚어둘 만한 호환성 함정입니다. WPA3-SAE의 hostapd는 `sae_pwe`로 비밀번호 요소(password element)의 유도 방식을 제어합니다. `0`은 전통적 Hunting-and-Pecking만, `1`은 Hash-to-Element(H2E)만, `2`는 둘 다 병존(Hunting-and-Pecking과 H2E 동시 지원)입니다. 이 차이가 구형 iPhone의 연결 여부를 직접 결정합니다.

```ini
wpa=2
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
# WPA3 는 PMF 강제
ieee80211w=2
# 핵심: iPhone 7 Plus 같은 구형 단말과의 호환
sae_pwe=0
sae_password=본인 비밀번호로 변경
```

실측 대조:

- `sae_pwe=0`: iPhone 15 Pro와 iPhone 7 Plus **모두 연결**(`authorized: yes`, `MFP: yes`).
- `sae_pwe=2`: iPhone 7 Plus는 **연계는 성공하지만 4-way 키 핸드셰이크 실패로 끊어지며**, 표면상 다시 "비밀번호 오류"처럼 보입니다. iPhone 15 Pro는 연결됩니다.

결론은 직접적입니다. 구형 iPhone(iPhone 7 Plus 같은 2016년 기종 포함)과 호환하려면 hostapd에서 반드시 `sae_pwe=0`을 설정해야 합니다. 설정 변경 후에는 iPhone에서 "이 네트워크 삭제"를 먼저 한 뒤 다시 연결하여, 잔여 연계 상태로 인한 가짜 실패를 피하십시오. 이 점은 9종 종합표에서 ACHM의 WPA3 항목이 "✅*"로 별표를 붙여 특별히 표기된 이유입니다.

## 4. 고급 능력과 한계

먼저 한 장의 표로 이번 ACHM의 완전한 커버리지 범위와 상태를 정리하고, 이후 단락에서 핵심을 전개합니다.

| 기능 | 상태 | 이번 실측 핵심 |
|---|---|---|
| Monitor(2.4 + 5 GHz) | ✅ | 채널 호핑 120초에 19 AP + 14 client 스캔 |
| Injection 2.4 GHz | ✅ | 응답률 96–100% |
| Injection 5 GHz | ⚠️ | 브로드캐스트 가능, 대상별 응답률 미취득 |
| AP(2.4 + 5 GHz) | ✅ | iPhone 두 밴드 연결, 802.11n 꺼야 함 |
| WPA3-SAE | ✅* | 2.4 GHz에서 실측(5 GHz 미실측), 신구 iPhone 모두 연결, `sae_pwe=0` 필요 |
| VIF(STA+AP, AP+monitor) | ✅ | 인터넷하면서 핫스팟, 다운로드 198 Mbit/s |
| WPA handshake 캡처 | ✅ 엔드투엔드(.22000, 5 GHz ch36) | 자체 iPhone에 deauth, 완전한 4-way M1–M4 캡처, hashcat `.22000` 추출 |
| Active monitor | 🟡 | 측면 기록 설정 가능, ACK 미검증 |
| Ad-hoc(IBSS) | 🟡 | 단일 기기 생성 가능, 두 번째 기기와 상호 연결 미확인 |
| Mesh(802.11s) | 🟡 | 단일 기기 참여 가능, peer link 미확인 |
| Wi-Fi Direct(P2P) | ⬜ | 두 번째 기기 필요, 생략 |

> ✅* = WPA3-SAE 사용 가능하나 `sae_pwe=0` 필요; 자세한 내용은 3-4절 참조.

**VIF(가상 인터페이스, 동일 채널, 최대 2 인터페이스).** ACHM은 한 장의 카드에서 여러 인터페이스를 동시에 운용할 수 있으며, 전제는 각 VIF가 서로 다른 MAC을 쓰고, AP VIF를 NetworkManager에 맡기지 않으며, 모든 VIF가 동일 채널이어야 하고, ACHM은 추가로 AP의 802.11n을 꺼야 한다는 점입니다. 두 가지 조합 모두 실측했습니다.

- **STA + AP(한쪽은 인터넷, 한쪽은 핫스팟)**: iPhone 7 Plus가 AP에 연결(-66 dBm, authorized)됨과 동시에, 주 인터페이스가 YUPITEK에 연결되어 ping 30/30, avg 3.2 ms, 다운로드 198 Mbit/s.
- **AP + Monitor**: AP를 켠 상태로 측면 기록, 8초에 300 frame 캡처, 그중 자체 AP의 beacon 46개 포함.

**handshake 캡처.** ACHM은 5 GHz(ch36)에서 엔드투엔드 과정을 완료했습니다. 자체 iPhone에 deauth를 보내 완전한 4-way(M1–M4)를 캡처하고 hashcat `.22000`을 추출했습니다. 엔드투엔드를 완료한 9장 중 7장(ACM, ACHM, ACH, ACS, EACS, AX, AXER)에 속합니다. 다만 5GHz 대상별 인젝션 응답률(`aireplay-ng --test`)은 여전히 얻지 못했습니다.

**mesh / IBSS(단일 기기에서 생성 가능).** 이것이 mt76 계열이 Realtek rtw88/rtw89에 비해 갖는 차이점입니다. IBSS(Ad-hoc)는 약 9초 만에 `Joined IBSS`가 되어 beacon을 낼 수 있고, Mesh(802.11s)는 `type mesh point`에 진입하여 mesh beacon을 낼 수 있습니다. 둘 다 이번에는 단일 기기에서 성립했고 두 번째 기기와 상호 연결하지 못했으므로(두 번째 기기가 없어 생략) 🟡로 표기합니다. Realtek의 rtw88/rtw89 카드(예: AWUS036ACH)는 이 플랫폼에서 단일 기기 IBSS는 생성할 수 있지만 802.11s mesh는 지원하지 않습니다. 따라서 802.11s mesh 실험을 하려면 ACM과 ACHM이라는 두 장의 mt76 카드가 오히려 몇 안 되는 선택지입니다.

**Active monitor 🟡.** 설정 가능하고 측면 기록도 정상이지만, ACK 응답 동작은 두 번째 기기가 있어야 검증할 수 있어 이번에는 미검증입니다.

**Kali 도구(플랫폼 레벨, 다른 카드와 공통).** `airmon-ng`, `kismet`, `bettercap`, `wifite`(git 버전), Wireshark/tshark는 모두 ACHM을 소스로 사용할 수 있습니다. 오직 `hcxdumptool`만 이 플랫폼에서 `failed to arm interface`입니다(2.4 GHz의 AWUS036EACS는 예외이며, 내장 드라이버가 active-monitor를 지원하지 않음). 캡처는 `airodump-ng`에 aircrack-ng 패키지를 조합해 사용하십시오. ARM64에서는 추가로 유의할 점이 있습니다. `aircrack-ng`은 prebuilt package가 없는 경우가 많아 소스에서 직접 컴파일해야 하고, `wifite`는 apt 의존성 충돌을 우회하기 위해 GitHub 버전을 권장합니다.

## 5. 적용 시나리오와 제품 선정(Hub로 돌아가기)

ACHM을 9종의 제품 선정 맥락에 다시 놓으면, 그 위치가 매우 분명합니다.

**적합**

- **mesh(802.11s) 실험**: mt76 드라이버는 단일 기기에서 802.11s mesh(와 IBSS)를 생성할 수 있습니다. Realtek 카드는 단일 기기 IBSS는 생성할 수 있지만 802.11s mesh는 하지 못합니다.
- **장거리 단일 스트림 monitor 측면 기록**: 채널 호핑 120초에 19 AP + 14 client를 스캔했고, 커뮤니티는 Very Long range로 평가합니다.
- **2.4GHz injection, 그리고 AP / WPA3 핫스팟**: 2.4G 인젝션 96–100%, WPA3를 `sae_pwe=0`으로 올바르게 설정하면 신구 iPhone 모두 연결됩니다.

**유의할 점(정직한 한계)**

- 5GHz 대상별 injection은 이번에 브로드캐스트만 확인했고 백분율이 없습니다.
- AP 개설 시 802.11n을 꺼야 하고 WPA3는 `sae_pwe=0`이어야 하며, 두 설정이 틀리면 모두 구형 iPhone이 "비밀번호 오류처럼 보이게" 됩니다.
- 단일 안테나 1T1R로, 처리량과 포지셔닝이 2T2R의 ACM / ACH와 다른 급입니다.

**제품 선정 지침**: 핵심 요구가 두 밴드 안정 인젝션에 엔드투엔드 handshake라면 9종 중 AWUS036EACS / AWUS036ACH / AWUS036ACS가 더 적합합니다. Wi-Fi 6 + AP 핫스팟을 원한다면 AWUS036AX / AWUS036AXER를 보십시오. mesh / IBSS 단일 기기 실험이나 장거리 측면 기록이 주 목적이라면 ACHM(또는 그 2T2R 자매 ACM)이 올바른 도구입니다. 마지막으로 함정 회피를 당부합니다. injection / handshake 용도로는 AWUS036AXM / AXML을 선택하지 마십시오. 이 두 장의 MT7921 인젝션은 이 플랫폼에서 실패합니다.

9종 모델의 하드웨어, 드라이버, Monitor / Injection / AP / WPA3 전체 매트릭스와 용도별 제품 선정 종합 평가는 Hub 종합표를 참조하세요: [9종 ALFA 무선 네트워크 카드 ARM64 / GX10 실측 종합 매트릭스](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 자주 묻는 질문(FAQ)

**Q: AWUS036ACHM은 Ubuntu 24.04에서 드라이버를 설치해야 하나요?**
필요 없습니다. MT7610U는 커널에 내장된 mt76x0u 드라이버가 담당하므로 Ubuntu 24.04(kernel 6.17)에서 꽂으면 바로 인식되며, DKMS도 추가 펌웨어도 필요 없습니다. lsusb에서 USB ID 0e8d:7610을 확인할 수 있습니다.

**Q: AWUS036ACHM은 monitor mode에 들어갈 수 있나요? 몇 개의 AP를 스캔할 수 있나요?**
가능합니다. 2.4GHz와 5GHz 모두 monitor mode에 들어갈 수 있으며, airodump-ng로 채널 호핑 전체 밴드 스캔을 120초 돌린 결과 19개의 AP, 14개의 클라이언트를 스캔했고 ch1, 2, 5, 6, 36, 149, 157에 분포했습니다.

**Q: AWUS036ACHM의 패킷 인젝션 성공률은 얼마인가요? 5GHz도 가능한가요?**
2.4GHz 6번 채널에서 대상별 인젝션 응답률은 96–100%입니다(aireplay-ng --test, 4대의 AP 발견). 5GHz(ch36, ch149)는 브로드캐스트 인젝션만 사용 가능함을 확인했고, 대상별 테스트는 Found 0 APs를 보고하여 이번에는 백분율을 얻지 못했으며 원인은 추후 조사 예정입니다.

**Q: AWUS036ACHM으로 AP를 개설할 때 iPhone에 "네트워크에 연결할 수 없음" 또는 "비밀번호 오류"가 뜨면 어떻게 하나요?**
먼저 802.11n을 끄세요. hostapd 설정 파일에 ieee80211n=1과 ht_capab을 넣지 말고, 2.4GHz는 순수 hw_mode=g, 5GHz는 순수 hw_mode=a(20 MHz)를 사용하세요. 그렇지 않으면 hostapd가 handle_assoc_cb: STA not found를 반복해서 띄우고, 화면은 비밀번호 오류처럼 보이지만 실제로는 802.11n 연계 실패입니다.

**Q: AWUS036ACHM의 WPA3-SAE가 왜 구형 iPhone에서 연결되지 않나요?**
대개 hostapd의 sae_pwe 설정 때문입니다. 실측 결과 sae_pwe=0일 때 iPhone 7 Plus와 iPhone 15 Pro 모두 연결되지만, sae_pwe=2일 때는 iPhone 7 Plus가 연계는 성공하지만 4-way 핸드셰이크 실패로 끊어져 비밀번호 오류처럼 보입니다. ieee80211w=2와 함께 설정하고, 설정 변경 후에는 iPhone에서 해당 네트워크를 먼저 삭제한 뒤 다시 연결하세요.

## 6. 더 읽어보기

- 〔Hub 종합표〕9종 ALFA 무선 네트워크 카드의 ASUS GX10(ARM64 / Ubuntu 24.04) Monitor · Injection · AP 전체 매트릭스와 제품 선정 종합 평가 → [/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 〔자매 모델〕AWUS036ACM(MT7612U / 2T2R) 카드별 실측 테스트 — 내부 링크 준비 중(준비 중, 링크 작업 중)
- 〔플랫폼 튜토리얼〕드라이버 설치 불필요: Ubuntu 24.04 + kernel 6.17에서 in-kernel 드라이버로 ALFA 네트워크 카드 Monitor와 AP 활성화 — 내부 링크 준비 중(준비 중, 링크 작업 중)
- 〔특집〕WPA3-SAE 시대의 handshake 캡처 능력과 `sae_pwe` 호환성 함정 — 내부 링크 준비 중(준비 중, 링크 작업 중)

---

*테스트 기관: Yupitek(ALFA Network 대만 유통사) — https://www.yupitek.com | 테스트 환경: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | 테스트 기기: Apple iPhone 7 Plus(WPA3는 iPhone 15 Pro로 추가 측정). 데이터는 2026-11-16~11-18의 실기 테스트 보고서에서 인용했으며, 어떠한 제3자 네트워크도 대상으로 하지 않고 공격 행위 절차도 제공하지 않습니다.*
