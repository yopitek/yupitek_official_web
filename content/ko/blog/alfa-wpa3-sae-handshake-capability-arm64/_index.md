---
title: "WPA3-SAE 시대의 무선 감사(audit): ALFA 카드 9종의 handshake 캡처 능력 실측과 iPhone 연결의 sae_pwe 호환성 함정"
slug: alfa-wpa3-sae-handshake-capability-arm64
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-wpa3-sae-handshake-capability-arm64.webp"
bannerimage: "/images/blog/banner/alfa-wpa3-sae-handshake-capability-arm64.webp"
author: "benny-lai"
tags:
  - wpa3-sae
  - wpa-handshake
  - sae-pwe
  - wireless-security
  - alfa-network
  - rtl8821cu
  - hcxpcapngtool
  - wifi-6
description: "ALFA 랜카드의 Ubuntu(Kali로 확장 가능) WPA3-SAE handshake 캡처 능력 실측: 9종의 인젝션률과 엔드투엔드 .22000 캡처 결과, sae_pwe 호환성 함정과 제품 선정 가이드."
faq:
  - question: "AWUS036AXM은 Ubuntu에서 WPA handshake를 캡처할 수 있나요?"
    answer: "이 플랫폼에서는 되지 않습니다. 실측에서 AWUS036AXM과 AWUS036AXML(MT7921 칩)은 injection 실패로 deauth를 송출할 수 없어 4-way handshake 캡처 체인 전체가 함께 끊겼으므로, handshake 캡처가 필요한 용도에는 적합하지 않습니다."
  - question: "어느 ALFA 랜카드의 WPA handshake 캡처가 가장 믿을 만한가요?"
    answer: "실측에서 AWUS036EACS가 가장 탄탄한 표현을 보였습니다. 두 밴드 injection이 모두 100%, deauth 후 79개의 ACK 보고를 수신했고 hashcat에서 쓸 수 있는 .22000 파일을 성공적으로 변환해 냈으며, 이번 묶음에서 엔드투엔드 검증이 가장 완전한 한 종입니다."
  - question: "WPA3-SAE 핫스팟에 왜 구형 iPhone이 연결되지 않나요?"
    answer: "핵심은 hostapd의 sae_pwe 파라미터입니다. 2(강제 H2E)로 설정하면 iPhone 7 Plus가 연결에 실패하고, sae_pwe=0(Hunting-and-Pecking)으로 되돌려야 4-way 교환을 정상적으로 완료하고 연결됩니다."
  - question: "WPA3 환경에서도 4-way handshake를 캡처할 수 있나요?"
    answer: "순수 WPA3-SAE 환경은 PMF(ieee80211w=2)를 강제로 켜서 management frame을 겨냥한 전통적 기법이 차단됩니다. 실무상 여전히 handshake를 캡처할 수 있는 것은 대개 대상이 순수 WPA3가 아니라 WPA2/WPA3 전환 모드로 동작하기 때문입니다."
  - question: "ALFA 랜카드의 5GHz injection이 측정되지 않는데 하드웨어 문제인가요?"
    answer: "반드시 그렇지는 않습니다. 기본 규제 도메인이 일부 5GHz 대역의 송신 출력을 제한하여 인젝션이 \"송출되지 않게\" 할 수 있습니다. 실측에서 규제 도메인을 송신 가능 상태로 전환하자 원래 실패하던 5GHz 인젝션이 바로 사용 가능으로 전환되었으니, 먼저 규제 도메인 설정을 확인한 뒤 하드웨어 제한 여부를 판단하시기 바랍니다."
draft: false
---

> 테스트 기관: Yopitek(ALFA Network 대만 총판) | 테스트 플랫폼: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 | 테스트 장치: 자사 소유 iPhone 7 Plus(WPA3는 iPhone 15 Pro로 별도 측정) | 테스트 대상: 자사 사무실 Wi-Fi(SSID YUPITEK, 2.4G ch5 / 5G ch36, 157).
>
> 이 글은 ALFA 무선 랜카드의 능력과 호환성 총람입니다. 모든 Monitor / Injection / handshake 캡처는 Yopitek 소유 장비, 자사 사무실 Wi-Fi에서 자사 테스트 전화기를 대상으로 수행했으며, 총판이 하드웨어에 대해 수행하는 정당한 능력 검증에 해당합니다. 어떠한 제3자 네트워크도 겨냥하지 않으며, 공격 조작 절차도 제공하지 않습니다.

## 핵심 요약(TL;DR)

ASUS GX10(ARM64 / Ubuntu 24.04 / kernel 6.17)에서 실측한 ALFA 9종 중 ACM, ACHM, ACH, ACS, EACS, AX, AXER 7종이 WPA handshake 엔드투엔드 캡처와 `.22000` 변환을 완료했으며, AWUS036EACS는 두 밴드 인젝션 100%, 79 ACKs를 기록했고, MT7921의 AXM / AXML은 본 플랫폼에서 인젝션에 실패했습니다.

- WPA3-SAE가 보급되면서 감사의 초점은 "monitor를 할 수 있는가"에서 "엔드투엔드 handshake 캡처 능력"과 "`sae_pwe` 엔드포인트 호환성"으로 옮겨갔습니다.
- **엔드투엔드 `.22000` 실증 9종 중 7종**: ACM, ACHM, ACH, ACS, EACS, AX, AXER.
- **AXM / AXML(MT7921)은 이 플랫폼에서 injection 실패**로 deauth를 할 수 없어 handshake를 캡처하지 못하므로, 감사 용도에서는 반드시 피하십시오.
- `sae_pwe` 함정: 구형 iPhone은 `sae_pwe=0`이어야 연결됩니다. 5G 인젝션 전에는 먼저 `iw reg set US`로 TX를 해제하십시오.
- 순수 WPA3는 PMF를 강제하는데(`ieee80211w=2`), 현장에서 여전히 캡처가 되는 것은 대개 대상이 WPA2/WPA3 전환(transition) 모드로 동작하기 때문입니다.

## 1. WPA3-SAE 보급이 무선 감사의 문턱 전체를 높였다

지난 10년간 허가 범위 내 무선 감사(authorized wireless audit)는 거의 WPA2-PSK의 4-way handshake를 중심으로 돌았습니다. 완전한 핸드셰이크를 한 번 캡처하면 백엔드에서 오프라인 대조가 가능했습니다. 그러나 Wi-Fi 6 인증이 WPA3를 필수 항목에 포함시킨 이후로, SAE(Simultaneous Authentication of Equals, 흔히 Dragonfly)가 점차 PSK를 대체하면서 "핸드셰이크 캡처, 오프라인 검증"이라는 이 오래된 길을 점점 더 좁혀 막았습니다.

총판과 일선 엔지니어에게 WPA3-SAE는 실무상 세 가지 변화를 가져옵니다.

1. **PMF(Protected Management Frame)가 강제가 됩니다.** WPA3-SAE 규격은 `ieee80211w=2`를 강제로 켜서 management frame을 보호하므로, 전통적인 "손쉽게 deauth 하나로 장치를 끊어버리는" 방식은 순수 WPA3 환경에서 바로 차단됩니다.
2. **전환 모드(transition mode)는 여전히 4-way를 유지합니다.** 현실에서는 많은 AP가 WPA2/WPA3 혼합 전환 모드로 동작하며, 구형 장치 호환을 위해 여전히 WPA2의 4-way handshake를 유지합니다. 이것이 현재 허가 감사에서 여전히 핸드셰이크를 캡처할 수 있는 주된 이유입니다. 핸드셰이크 캡처 가능 여부는 상당 부분 현장 대상이 어떤 모드로 열려 있는지에 달려 있습니다.
3. **엔드포인트 호환성이 새로운 함정이 됩니다.** SAE는 password element 도출 방식이 다르며(`sae_pwe`로 제어), AP 파라미터를 한 번 잘못 설정하면 자사의 구형 iPhone조차 연결되지 않습니다. 감사 현장에서 클라이언트 엔드포인트의 연결 동작을 재현하는 것은 더 말할 것도 없습니다.

따라서 고객이 "어느 ALFA 카드로 WPA3 관련 허가 감사를 할 수 있나요"라고 물으면, 답은 더 이상 "monitor를 할 수 있는가"처럼 단순하지 않고, 두 가지를 봐야 합니다. **엔드투엔드 handshake 캡처 능력**, 그리고 **WPA3-SAE 파라미터 및 실기 엔드포인트에 대한 호환성**입니다. 이 보고서는 바로 9종의 ALFA 카드를 동일한 ARM64 플랫폼에서 실측한 뒤 정리한 능력 대조표입니다.

## 2. "엔드투엔드 handshake 캡처 능력"이란(개념 계층)

여기서는 먼저 능력을 세 단계로 나누어 순수 개념으로만 설명하며, 제3자 네트워크를 겨냥한 어떠한 조작 명령도 포함하지 않습니다.

- **첫 단계: Injection(능동 주입).** 랜카드가 특정 관리 프레임을 "송출할 수 있어야" 이미 연결된 client가 다시 association을 수행하도록 유도할 수 있습니다. 많은 카드는 수동 monitor(패킷 수신)만 되고 injection(능동 송신)은 불가합니다. 이것이 전체 체인에서 가장 막히기 쉬운 단계입니다. 이번 테스트에서는 `aireplay-ng --test`로 인젝션 성공률을 정량화하고, handshake 테스트에서 client가 반환하는 ACKs 수로 프레임이 실제로 도달했는지 검증했습니다.
- **둘째 단계: 4-way handshake 캡처.** client가 다시 association할 때 WPA는 네 개의 EAPOL 메시지(M1–M4)를 교환합니다. 랜카드는 monitor 모드에서 이 네 프레임을 하나도 빠짐없이 완전히 수신해야 합니다.
- **셋째 단계: hashcat `.22000` 변환.** 캡처한 pcap을 `hcxpcapngtool --all`로 hashcat의 `.22000` 포맷으로 변환해 백엔드에 오프라인 검증을 맡깁니다.

**세 단계가 전부 실기에서 끝까지 돌아가야 "엔드투엔드"입니다.** 실제로 자사 iPhone 7 Plus에 deauth(injection)를 송출 → 완전한 M1–M4 수신 → `.22000` 변환 파일 산출. 받기만 하고 못 보내거나, 네 프레임을 다 못 받거나, 파일을 못 뽑아내면 엔드투엔드로 치지 않습니다. 본문은 어떠한 단계별 공격 명령도 나열하지 않습니다. 아래 대조표는 오직 한 가지 질문에만 답합니다. 어느 카드가 이 능력 체인을 끝까지 걸어가는가.

이번 묶음에서 가장 탄탄한 EACS를 예로, 한 번의 성공적인 엔드투엔드는 이렇게 생겼습니다. deauth 송출 후 client가 **79개의 ACKs**를 반환했고(확인 프레임이 실제로 그 전화기에 도달했음), `aircrack-ng`이 YUPITEK에 1개의 handshake가 있다고 판정했으며, EAPOL의 M1 / M2 / M3 / M4 네 프레임을 각각 1부씩 수신했고, 캡처한 client MAC의 앞부분이 Apple OUI로 시작하며(바로 그 iPhone 7 Plus임을 확인), 마지막으로 `hcxpcapngtool --all`로 약 784 bytes의 `.22000`을 변환해 냈습니다. 이 네 조건 중 하나라도 빠지면 그 캡처는 인정되지 않습니다. 이것이 "monitor를 할 수 있다"와 "엔드투엔드로 캡처할 수 있다"가 완전히 다른 두 가지인 이유이기도 합니다.

## 3. 9종 카드 handshake 능력 대조표

| # | 모델 | 칩 / 세대 | Injection 2.4G | Injection 5G | WPA handshake 캡처 능력 |
|---|---|---|---|---|---|
| 1 | AWUS036ACM | MT7612U / Wi-Fi 5 · 2T2R | 사용 가능 63–83% | 사용 가능 76% | **엔드투엔드 `.22000` 실증**(인젝션률은 더 낮음) |
| 2 | AWUS036ACHM | MT7610U / Wi-Fi 5 · 1T1R | 사용 가능 96–100% | 브로드캐스트만 | **엔드투엔드 `.22000` 실증(5 GHz ch36)** |
| 3 | **AWUS036ACH** | RTL8812AU / Wi-Fi 5 · 2T2R | **100%** | **100%** | **엔드투엔드 `.22000` 실증(2026-11-19 추가 측정)** |
| 4 | **AWUS036ACS** | RTL8811AU / Wi-Fi 5 · 1x1 | **100%** | 96% | **엔드투엔드 `.22000` 실증** |
| 5 | **AWUS036EACS** | RTL8821CU / Wi-Fi 5 · 1x1 | **100%** | **100%** | **엔드투엔드 `.22000` 실증(79 ACKs)** |
| 6 | **AWUS036AX** | RTL8832BU / Wi-Fi 6 · 2x2 | 96% | 사용 가능 | **엔드투엔드 `.22000` 실증** |
| 7 | **AWUS036AXER** | RTL8832BU / Wi-Fi 6 · 2x2 | 73% | 사용 가능 | **엔드투엔드 `.22000` 실증** |
| 8 | AWUS036AXM | MT7921AU / Wi-Fi 6 · 2x2 | 실패 | 실패 | 미지원: 인젝션 실패, 캡처 불가 |
| 9 | AWUS036AXML | MT7921AUN / Wi-Fi 6 · 2x2 | 실패 | 실패 | 미지원: 인젝션 실패, 캡처 불가 |

**두 등급, 한눈에 파악:**

- **엔드투엔드 실증(캡처 → `.22000` 파일 산출, 9종 중 7종)**: AWUS036ACM, AWUS036ACHM, AWUS036ACH, AWUS036ACS, AWUS036EACS, AWUS036AX, AWUS036AXER. 그중 EACS는 두 밴드 인젝션이 모두 100%이고 deauth 후 79개의 ACKs를 수신해 이번 묶음에서 핸드셰이크 능력이 가장 탄탄한 한 장입니다. AWUS036ACH(RTL8812AU 듀얼 안테나 고이득)는 두 밴드 인젝션 100%이며, 2026-11-19에 47줄 해시라인의 `.22000`을 추가 측정으로 변환해 EACS와 함께 침투 테스트 1순위로 나란히 섭니다. **엔드투엔드 handshake 캡처를 완주한 모델은 일곱 종입니다: ACM, ACHM, ACH, ACS, EACS, AX, AXER.** ACM은 인젝션률이 더 낮고(2.4G 63–83% / 5G 76%) ACHM은 5 GHz(ch36)에서 완주했지만, 둘 다 `.22000`을 산출했습니다.
- **캡처 불가(2종)**: AWUS036AXM과 AWUS036AXML(MT7921이 이 플랫폼에서 injection 실패, deauth를 할 수 없고 당연히 handshake도 캡처하지 못함).

특별히 짚어야 할 것은 **AXM / AXML**입니다. 두 종 모두 Wi-Fi 6이고 monitor와 AP는 정상이지만, 유독 이 플랫폼에서 injection이 동작하지 않습니다. 주원인은 stock kernel 6.16+의 mac80211 chanctx 회귀(regression)이며(칩 선천적 문제가 아님), 커뮤니티에서 동일 모델에 git/patched 드라이버를 쓰면 동작하기도 하지만 펌웨어가 속도를 잠급니다(morrownr/USB-WiFi #387, morrownr/mt76 #18 대응). 순수 인터넷, 핫스팟 구축은 문제없지만, **인젝션이나 handshake 캡처가 필요한 감사 용도라면 이 플랫폼에서는 일괄 피하십시오.**

## 4. WPA3-SAE 호환성 함정: 파라미터를 잘못 설정하면 자사 iPhone도 연결 안 됨

능력 외에, WPA3-SAE의 파라미터 호환성은 현장에서 가장 쉽게 뒤집어지는 부분입니다. 이번 실측에서 두 가지 핵심 함정을 밟았습니다.

### 4-1. ACHM은 반드시 `sae_pwe=0`, 그렇지 않으면 iPhone 7 Plus가 연결 안 됨

SAE의 password element 도출에는 여러 방식이 있고, hostapd는 `sae_pwe`로 제어합니다. 이번에 AWUS036ACHM을 순수 WPA3-SAE(`wpa_key_mgmt=SAE` + 강제 PMF `ieee80211w=2`)로 구축했을 때, `sae_pwe`를 `2`로 설정하자 **iPhone 7 Plus가 바로 연결되지 않았습니다.** `sae_pwe=0`(Hunting-and-Pecking, 구형 엔드포인트 호환)으로 되돌린 뒤에야 iPhone 7 Plus(iOS 15)가 순조롭게 연결되어 4-way를 완료했습니다.

이 함정의 의미는 이렇습니다. 감사 현장에서 구형 iOS 엔드포인트 위주의 WPA3 환경을 "재현"하려면, AP 측의 `sae_pwe`가 엔드포인트 능력에 맞아야 합니다. 그렇지 않으면 얻는 것은 "연결 안 됨"이라는 거짓 음성(false negative)이지, 진정한 호환성 결론이 아닙니다. EACS, ACS의 WPA3-SAE AP 테스트도 마찬가지로 `sae_pwe=0` + `ieee80211w=2`를 채택했고 iPhone 7 Plus가 모두 연결되었습니다. `sae_pwe=0`은 이번 묶음에서 구형 iPhone 엔드포인트에 대해 검증된 안전 값입니다.

### 4-2. 5G injection 전에 먼저 `iw reg set US`로 TX 해제

두 번째 함정은 규제 도메인(regulatory domain)과 관련 있습니다. 기본 `reg=TW`는 일부 UNII 대역의 TX를 잠가서, 5 GHz의 injection / deauth가 "송출되지 않게" 합니다. 이번 묶음은 5G 인젝션 전에 일괄적으로 `iw reg set US`로 TX를 해제하고, 끝난 즉시 `iw reg set TW`로 복원했습니다. ACS의 5G 인젝션은 해제 후 실패에서 96%로 전환되었고, EACS, ACH는 바로 100%였습니다. reg 해제를 잊으면, 인젝션 능력이 정상인 카드를 "5G 불가"로 오판하게 됩니다.

### 4-3. 덧붙여: PMF는 WPA3에서 강제입니다

WPA3-SAE 규격은 `ieee80211w=2`(Management Frame Protection)를 강제합니다. 이는 순수 WPA3 환경에서 management frame을 겨냥한 전통적 기법이 PMF에 막힌다는 뜻입니다. 현실 감사에서 여전히 4-way를 캡처할 수 있는 것은 대개 대상이 아직 WPA2/WPA3 전환 모드로 동작하기 때문입니다. 카드를 고를 때 이 점을 함께 고려해야 순수 WPA3 대상에 잘못된 기대를 품지 않습니다.

## 5. 도구 체인 개요: ARM64 플랫폼에서 실제로 돌아가는 세트

하드웨어 능력 외에, 플랫폼 도구 체인도 감사 효율에 영향을 줍니다. 다음은 이번 묶음이 GX10(ARM64)에서 정리한 몇 가지 실측 심득입니다.

- **변환은 일괄 `hcxpcapngtool --all`.** 기본 파라미터는 더 엄격해서 흔히 "not enough M1"을 반환하며 파일이 안 나옵니다. `--all`을 붙여야 완전한 M1–M4에서 `.22000`을 안정적으로 변환할 수 있습니다.
- **사무실에 동일 이름 AP가 여러 대일 때는 `--bssid`를 고정하지 마십시오.** Yopitek 사무실에는 같은 채널에 동일 이름 YUPITEK AP가 여러 대 있어서 iPhone은 신호가 가장 강한 한 대에 연결됩니다. 캡처 시 `--bssid`로 단일 BSSID를 고정하면 iPhone이 실제로 연결된 그 대를 걸러내 캡처 전체가 허탕이 되기 쉽습니다. 실측 결론은 **BSSID를 고정하지 말고 채널 전체를 캡처한 뒤**, 산출 파일에서 완전한 핸드셰이크를 골라내는 것입니다.
- **`hcxdumptool` 8.x는 이 플랫폼에서 2.4 GHz의 EACS를 제외하고 `failed to arm`(5 GHz에서는 실패).** rtw88 / rtw89 / mt7921u 모두 active-monitor를 제공하지 않는데 hcxdumptool 8.x는 그것을 요구합니다. 해법은 `airodump-ng` + `aireplay-ng`라는 전통적 aircrack-ng 흐름으로 전환하는 것입니다.
- **모드를 반복 전환한 뒤 아무것도 스캔 안 되면 먼저 카드를 뽑았다 꽂으십시오.** rtw88 / rtw89은 monitor / AP를 반복 전환한 뒤 RX stall(스캔 0 패킷)이 발생할 수 있습니다. USB 재열거로 복구되며, 인터페이스 이름은 MAC으로 결정되어 뽑았다 꽂아도 변하지 않습니다. handshake 캡처 전에 가장 먼저 할 일은 카드를 한 번 다시 꽂는 것을 권장합니다.
- **BT+WiFi 복합 장치(EACS / AXML)는 다시 꽂을 때 경쟁 상태가 있음.** 블루투스를 포함한 복합 카드는 다시 꽂거나 특정 USB 포트에 꽂을 때 WiFi 기능 probe가 멈춰 `wlx` 인터페이스가 생성되지 않을 수 있습니다. 해법은 USB 포트를 바꿔 다시 꽂는 것이며, `modprobe`나 수동 bind는 대개 무효입니다.
- **ARM64의 도구 설치 요령.** aircrack-ng는 aarch64에서 prebuilt 패키지가 없는 경우가 많아 원본 소스에서 컴파일해야 하고, wifite는 git 버전을 씁니다(apt 버전은 소스 빌드한 aircrack-ng와 의존성 충돌).
- **안전 수칙: `airmon-ng check kill` 절대 금지.** GX10의 외부 인터넷은 내장 랜카드에 의존하므로, `check kill`은 NetworkManager까지 함께 꺼서 호스트의 네트워크를 끊습니다. 이번 묶음은 전 과정에서 ALFA 카드의 `wlx*` 인터페이스만 다루고, 내장 외부 본선은 건드리지 않습니다.

## 6. 제품 선정 요약: WPA3 관련 감사를 하려면 어느 모델을 골라야 하나

능력, 호환성, 플랫폼 도구 체인을 합쳐서 보면, "WPA3 관련 허가 감사" 용도에 대한 이번 묶음의 권장은 다음과 같습니다.

| 요구 상황 | 권장 모델 | 이유 |
|---|---|---|
| 종합 1순위(인젝션 + 엔드투엔드 handshake) | **AWUS036EACS** | 두 밴드 인젝션 100%, deauth 79 ACKs 수신, 엔드투엔드 `.22000` 실증; 유일한 주의점은 BT+WiFi 복합 장치여서 다시 꽂을 때 간혹 USB 포트를 바꿔야 함 |
| 고이득 / 장거리 + 강한 인젝션 | **AWUS036ACH** | RTL8812AU 듀얼 안테나, 두 밴드 인젝션 100%, 수신 능력 강함 |
| 경량 휴대형 | **AWUS036ACS** | 단일 스트림, 엔드투엔드 `.22000` 실증, 5G 인젝션 96% |
| Wi-Fi 6 요구 | **AWUS036AX / AWUS036AXER** | 2x2 VHT80, 엔드투엔드 `.22000` 실증; AXER는 내장 안테나(Nano) 설계 + 칩 튜닝으로 스캔 커버리지가 가장 넓음 |
| **반드시 피할 것** | AWUS036AXM / AWUS036AXML | MT7921이 이 플랫폼에서 injection 실패, handshake 캡처 불가 |

한 문장으로 요약하면: **WPA3 관련 감사를 하려면 EACS를 우선, 그다음 ACH / ACS; Wi-Fi 6이 필요하면 AX / AXER; AXM / AXML은 반드시 피하십시오.** 엔드투엔드 handshake 캡처를 완주한 일곱 종 중 Realtek(rtw88 / rtw89)은 전부 인젝션이 가능하고, MediaTek은 ACM과 ACHM(mt76)도 완주했으며 MT7921의 AXM / AXML은 불가합니다. 제품 선정 시에는 모델명보다 칩을 알아보는 것이 더 정확합니다.

## 자주 묻는 질문(FAQ)

**Q: AWUS036AXM은 Ubuntu에서 WPA handshake를 캡처할 수 있나요?**
A: 이 플랫폼에서는 되지 않습니다. 실측에서 AWUS036AXM과 AWUS036AXML(MT7921 칩)은 injection 실패로 deauth를 송출할 수 없어 4-way handshake 캡처 체인 전체가 함께 끊겼으므로, handshake 캡처가 필요한 용도에는 적합하지 않습니다.

**Q: 어느 ALFA 랜카드의 WPA handshake 캡처가 가장 믿을 만한가요?**
A: 실측에서 AWUS036EACS가 가장 탄탄한 표현을 보였습니다. 두 밴드 injection이 모두 100%, deauth 후 79개의 ACK 보고를 수신했고 hashcat에서 쓸 수 있는 `.22000` 파일을 성공적으로 변환해 냈으며, 이번 묶음에서 엔드투엔드 검증이 가장 완전한 한 종입니다.

**Q: WPA3-SAE 핫스팟에 왜 구형 iPhone이 연결되지 않나요?**
A: 핵심은 hostapd의 `sae_pwe` 파라미터입니다. 2(강제 H2E)로 설정하면 iPhone 7 Plus가 연결에 실패하고, `sae_pwe=0`(Hunting-and-Pecking)으로 되돌려야 4-way 교환을 정상적으로 완료하고 연결됩니다.

**Q: WPA3 환경에서도 4-way handshake를 캡처할 수 있나요?**
A: 순수 WPA3-SAE 환경은 PMF(`ieee80211w=2`)를 강제로 켜서 management frame을 겨냥한 전통적 기법이 차단됩니다. 실무상 여전히 handshake를 캡처할 수 있는 것은 대개 대상이 순수 WPA3가 아니라 WPA2/WPA3 전환 모드로 동작하기 때문입니다.

**Q: ALFA 랜카드의 5GHz injection이 측정되지 않는데 하드웨어 문제인가요?**
A: 반드시 그렇지는 않습니다. 기본 규제 도메인이 일부 5GHz 대역의 송신 출력을 제한하여 인젝션이 "송출되지 않게" 할 수 있습니다. 실측에서 규제 도메인을 송신 가능 상태로 전환하자 원래 실패하던 5GHz 인젝션이 바로 사용 가능으로 전환되었으니, 먼저 규제 도메인 설정을 확인한 뒤 하드웨어 제한 여부를 판단하시기 바랍니다.

## 7. 더 읽어보기

- [ALFA 무선 랜카드 9종 ARM64 실측 종합표와 제품 선정 총평](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 모델별 카드 실측: [AWUS036EACS 단일 카드 실측](/ko/blog/awus036eacs-asus-gx10-ubuntu-test-report/), [AWUS036ACS 단일 카드 실측](/ko/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*본문의 모든 테스트는 Yopitek 자사 사무실 Wi-Fi(SSID YUPITEK)에서 자사 소유 iPhone 7 Plus를 대상으로 수행했으며, 총판이 ALFA 무선 랜카드에 대해 수행하는 정당한 능력 검증에 해당합니다. 데이터는 2026-11-16~11-18의 실기 테스트 보고서에서 인용했으며, 어떠한 제3자 네트워크도 겨냥하지 않고 공격 조작 절차도 제공하지 않습니다. 테스트 기관: Yopitek(ALFA Network 대만 총판) — https://www.yupitek.com*
