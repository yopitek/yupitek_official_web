---
title: "AWUS036ACS 카드별 실측 테스트: RTL8811AU 경량 휴대용 카드의 ASUS GX10 + Ubuntu 24.04(ARM64) 호환성 및 성능 보고서"
slug: awus036acs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acs
  - rtl8811au
  - rtw88-8821au
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
description: "AWUS036ACS를 Ubuntu 24.04 ARM64에서 실측: 드라이버 설치 불필요, 모니터 모드, 인젝션(2.4G 100%, 5G 96%), AP, WPA3-SAE, 엔드투엔드 핸드셰이크(.22000) 모두 통과. 플랫폼은 ASUS GX10, kernel 6.17, RTL8811AU."
faq:
  - question: "AWUS036ACS는 Ubuntu 24.04 ARM64에서 드라이버를 설치해야 하나요?"
    answer: "본문에서 테스트한 kernel 6.17(ASUS GX10)에서는 필요 없습니다. RTL8811AU는 내장 rtw88_8821au 드라이버로 구동되어 꽂으면 바로 인식하며, 컴파일도 DKMS도 필요 없습니다. kernel이 더 오래된 경우에는 먼저 modinfo rtw88_8821au로 모듈이 존재하는지 확인하세요."
  - question: "AWUS036ACS는 모니터 모드와 패킷 인젝션을 지원하나요?"
    answer: "지원합니다. 2.4 GHz, 5 GHz 모두 모니터 가능하며, aireplay-ng --test 인젝션은 2.4G가 100%(30/30), 5G가 96%(29/30, 먼저 iw reg set US로 TW 제한을 해제해야 함)입니다. 액티브 모니터는 지원하지 않습니다."
  - question: "AWUS036ACS로 WPA 핸드셰이크를 캡처해 hashcat .22000으로 변환할 수 있나요?"
    answer: "가능합니다. 본인 소유 AP와 본인 소유 iPhone 7 Plus에서 엔드투엔드로 실측: 지향성 deauth로 재접속을 유도하고 완전한 4-way(M1–M4)를 캡처한 뒤 hcxpcapngtool --all로 .22000을 변환합니다. 본인 소유 또는 허가된 네트워크에서만 가능합니다."
  - question: "AWUS036ACS를 AP 핫스팟으로 쓸 수 있나요? WPA3을 지원하나요?"
    answer: "가능합니다. hostapd로 2.4G와 5G 핫스팟(5G 채널 폭은 확인하지 못함)을 열어 iPhone 7 Plus가 접속해 4-way를 완료했으며, 5G의 WPA3-SAE(SAE-only, ieee80211w=2, sae_pwe=0)도 접속에 성공했습니다(2.4G의 WPA3는 실측하지 않음)."
  - question: "AWUS036ACS가 지원하지 않는 모드는 무엇인가요? hcxdumptool은 사용할 수 있나요?"
    answer: "액티브 모니터, IBSS, 메시(802.11s), Wi-Fi Direct(P2P)를 지원하지 않습니다. hcxdumptool 8.x는 failed to arm interface가 발생하므로 airodump-ng + aireplay-ng를 사용하세요. 메시/IBSS가 필요하면 AWUS036ACM/ACHM을 선택하세요."
draft: false
---

**핵심 요약(TL;DR)**: Yupitek(ALFA Network 대만 총판) 실측 결과, AWUS036ACS는 ASUS GX10 / Ubuntu 24.04 ARM64(kernel 6.17)에서 드라이버 설치 불필요이며 듀얼 밴드 monitor와 AP(5G AP 사용 가능, 채널 폭은 확인하지 못함)가 가능하고, 인젝션은 2.4G 100%, 5G 96%, 엔드투엔드 .22000 통과, 메시/IBSS는 미지원입니다.

> 본문은 Yupitek이 ALFA AWUS036ACS를 최신 Linux 플랫폼에서 테스트한 제품 호환성 및 성능 실측 기록으로, 제품 선정 평가에 활용하기 위한 것입니다.
> 테스트 플랫폼: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. 모든 데이터는 Yupitek이 **본인 소유 장비, 본인 소유 사무실 Wi-Fi**(SSID `YUPITEK`, 2.4G ch5 / 5G ch36)에서 **본인 소유 테스트 휴대폰**(Apple iPhone 7 Plus)을 대상으로 실측한 발췌이며, MAC 주소는 일부 가렸습니다.
> ⚠️ **합법성 및 범위 고지**: 모니터, 인젝션, 핸드셰이크 캡처는 본인 소유 또는 허가된 네트워크와 장치에서만 수행했으며, AP 모드는 현지 무선 규제를 준수하십시오. 본문은 네트워크 카드 자체의 성능, 호환성, 설정에 초점을 맞추며, **제3자 네트워크에 대한 어떠한 공격 행위도 포함하지 않습니다**.

---

## 1. 이 카드와 테스트 플랫폼

AWUS036ACS는 ALFA 제품군 중 경량 휴대용 무선 네트워크 카드로, 칩은 Realtek RTL8811AU이며 Wi-Fi 5(802.11ac) 세대, 1x1 단일 공간 스트림입니다. 포지셔닝은 명확합니다. 작은 크기, 저전력, 단일 안테나로, 현장에 들고 나가 실사하기 위한 카드이지 최고 처리량이나 최장 거리를 겨루는 중장비 카드가 아닙니다. 따라서 이 카드를 평가할 때의 질문은 "얼마나 빠른가"가 아니라 "이렇게 가벼운 사양에서 어떤 실무 성능이 여전히 온전히 작동하는가"입니다.

이번 테스트에서는 이 카드를 전형적인 운영 시나리오에 배치했습니다. GX10의 내장 네트워크 카드(`wlP9s9`)는 외부 인터넷 연결을 담당하고, AWUS036ACS는 USB 외장으로 연결해 테스트 작업만 맡습니다. 이렇게 하면 모니터나 AP로 전환해도 호스트 자체의 네트워크를 건드리지 않습니다. 전 과정에서 ALFA 카드에 대응하는 `wlx*` 인터페이스만 다루고, 내장된 외부 연결 네트워크 카드는 건드리지 않습니다.

| 항목 | 내용 |
|---|---|
| 모델명 | AWUS036ACS |
| 칩 | Realtek RTL8811AU(Wi-Fi 5 / 802.11ac, 1x1 단일 스트림) |
| USB ID | `0bda:0811` |
| 드라이버 | `rtw88_8821au`(in-kernel, kernel 6.17 내장) |
| 펌웨어 | 42.4.0(dmesg 실측) |
| 플랫폼 | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| 테스트 장치 | Apple iPhone 7 Plus |

---

## 2. 하드웨어와 드라이버(무설치)

이 카드는 GX10에 꽂으면 바로 인식되며, 컴파일도 DKMS도 필요 없습니다. RTL8811AU / RTL8821AU 칩은 mainline kernel 6.13부터 Realtek의 in-kernel `rtw88` 드라이버 계열에 정식으로 병합되었고, GX10에 탑재된 6.17에는 이미 `rtw88_8821au` 모듈이 내장되어 있어, GitHub에서 out-of-tree 프로젝트를 받을 필요가 없습니다. (이전 설치 가이드와 다릅니다. 초기 게시물은 `morrownr` out-of-tree 드라이버나 더 오래된 kernel을 전제로 DKMS 직접 컴파일이 필요하다고 했지만, kernel 6.17의 in-kernel 드라이버에서는 더 이상 필요하지 않습니다.) 과거에 흔히 쓰이던 `morrownr/8821au-20210708`은 이제 legacy로 전환되었으며(6.13 미만 커널에만 권장되고, 설치하면 내장 드라이버를 blacklist 처리함), 새 kernel에서는 이 옛 경로를 다시 밟을 필요가 없습니다. 운영 비용 측면의 이점은 더욱 실질적입니다. in-kernel 드라이버는 kernel과 함께 업데이트되어 사용자가 각자 브랜치를 유지보수할 필요가 없고, 업그레이드할 때마다 DKMS 컴파일 실패에 막히지도 않으며, 동일한 조작을 여러 번의 kernel 업데이트에 걸쳐 반복 사용할 수 있습니다. 펌웨어는 `linux-firmware`가 시스템과 함께 제공하며, 본 기기 실측은 42.4.0으로 마찬가지로 수동 처리가 필요 없습니다.

카드가 인식되었고 드라이버가 바인딩되었으며 인터페이스도 생성되었는지 확인합니다.

```bash
lsusb | grep -i 0bda:0811
# Bus 003 Device 004: ID 0bda:0811 Realtek Semiconductor Corp. Realtek 8812AU/8821AU 802.11ac WLAN Adapter

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"
cat /sys/class/net/$IF/phy80211/name
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# IF=wlx00c0cabce039 / phy1 / rtw88_8821au
```

펌웨어 버전은 `dmesg`로 확인할 수 있습니다(실측 42.4.0).

```bash
sudo dmesg | grep -i 8821au
# rtw88_8821au ... Firmware version 42.4.0, H2C version 0
```

선언된 지원 인터페이스 모드(이것이 이후 어떤 성능을 쓸 수 있는지 결정합니다).

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
# IBSS / managed / AP / AP/VLAN / monitor
```

이 목록에는 `IBSS / managed / AP / AP/VLAN / monitor`가 나열되어 있습니다. 여기서 특히 주의할 점은, 목록에 IBSS가 나와 있지만 실측에서 `ibss join` 이후 `iw link`가 Not connected로 표시되어 연결되지 않는다는 것입니다. 메시, 액티브 모니터, P2P는 아예 목록에 없습니다(자세한 내용은 4장 제한 사항 참고). 이는 RTL8811AU의 하드웨어 및 드라이버 현황이며 안테나 개수와는 무관합니다.

주파수 대역 범위: 2.4 GHz ch1–13(ch14 disabled), 5 GHz ch36–165(그중 ch52–144는 radar / DFS 표시). 기본 regdomain은 `TW`, TX 출력은 2.4 GHz 30 dBm, 5 GHz UNII-1/2 23 dBm, UNII-3 30 dBm입니다.

---

## 3. 실측 성능: 모니터 / 인젝션 / AP / WPA3

먼저 핵심 성능 종합표를 보고, 이어서 항목별로 펼칩니다. 모든 항목은 본인 소유 YUPITEK AP + 본인 소유 iPhone 7 Plus에서 완료했습니다.

| 성능 | 2.4 GHz | 5 GHz |
|---|---|---|
| 모니터(수신 리스닝) | ✅ 강함 | ✅ 강함 |
| 인젝션(패킷 인젝션) | ✅ **100%**(30/30) | ✅ **96%**(29/30, 먼저 reg 잠금 해제 필요) |
| AP 핫스팟(hostapd) | ✅ iPhone 접속 + 핸드셰이크 완료 | ✅ **안정적**(채널 폭 확인하지 못함) |
| AP WPA3-SAE | 미실측 | ✅ iPhone 접속(SAE-only + PMF) |

### 3-1. 모니터(모니터 모드, 2.4 GHz + 5 GHz) ✅

모니터로 전환한 뒤 6개 채널에서 각각 한 번씩 고정 길이 캡처를 수행했으며, 수신은 모두 정상이었습니다. 인기 채널은 6초 이내에 300 프레임 캡처 상한에 도달했습니다.

| 채널 | 캡처 frames |
|---|---|
| ch1 / 2412 | 300 |
| ch6 / 2437 | 300 |
| ch11 / 2462 | 146 |
| ch36 / 5180 | 300 |
| ch149 / 5745 | 141 |
| ch157 / 5785 | 154 |

2.4 GHz와 5 GHz 모두 안정적으로 수신합니다. 단일 안테나 휴대용 카드로서 이 수신 성능은 현장 채널 실사와 패킷 진단을 충분히 감당할 수 있습니다. ch11, ch149, ch157의 프레임 수가 낮은 것은 해당 채널의 당시 공중 트래픽이 원래 적었기 때문이지 카드가 수신하지 못한 것이 아닙니다. 인기 채널인 ch1, ch6, ch36은 6초 이내에 300 프레임 상한을 채웠으며, 수신은 분명히 이 카드의 병목이 아닙니다.

### 3-2. 인젝션(패킷 인젝션) ✅

`aireplay-ng --test`로 자사 YUPITEK AP에 지향성 인젝션 테스트를 수행했습니다. 2.4 GHz는 100%(30/30, `Injection is working!`)에 도달했고, 5 GHz는 96%(29/30)입니다. 5 GHz에는 주의할 설정 세부 사항이 하나 있습니다. 기본 `reg=TW`는 일부 UNII 대역의 능동 송신을 잠그므로, 테스트 전에 먼저 `sudo iw reg set US`로 잠금을 해제하고 테스트 후 `sudo iw reg set TW`로 되돌립니다.

```bash
# 2.4 GHz(YUPITEK는 실제로 ch5 / 2432에 위치)
sudo iw dev $IF set freq 2432
sudo aireplay-ng --test --ignore-negative-one -a <YUPITEK-BSSID> $IF
# Injection is working!  30/30: 100%  Power: -60.00
```

단일 안테나 카드가 2.4 GHz에서 100%, 5 GHz에서 96%를 얻은 것은 이미 상당히 신뢰할 수 있는 인젝션 성능이며, 이것이 뒤의 엔드투엔드 핸드셰이크 캡처를 완료할 수 있는 기반이기도 합니다.

### 3-3. AP 핫스팟(2.4 GHz / 5 GHz) ✅

`hostapd`로 카드를 기지국으로 만들었고, 세 가지 설정 모두에서 iPhone 7 Plus가 성공적으로 접속해 4-way 핸드셰이크(`EAPOL-4WAY-HS-COMPLETED`)를 완료했습니다.

- **5 GHz(채널 폭 확인하지 못함)**: 가장 안정적인 구성으로, iPhone 접속, 핸드셰이크 완료, `AP-DISABLED`로 깔끔하게 마무리되었습니다.
- **2.4 GHz(WPA2-PSK)**: iPhone 접속, 핸드셰이크 완료, 접속 종료 후 깔끔하게 닫혔습니다. 여기서 한 가지 상황을 정직하게 기록합니다. 이전 라운드의 동일한 설정에서 STA 접속 종료 후 `key not allowed / Failed to set beacon parameters`로 중단된 적이 있었으나, 재테스트에서는 재현되지 않아 rtw88_8821au의 간헐적 beacon re-key로 판단되며 고정적 결함은 아닙니다. 장시간, 고빈도 재접속 시나리오에서는 여전히 유의하거나 아예 5 GHz AP로 바꾸는 것을 권장합니다.
- **WPA3-SAE(5 GHz, PMF 강제, 2.4 GHz 미실측)**: 핵심 설정은 `wpa_key_mgmt=SAE`(순수 WPA3, WPA2 fallback 없음), `ieee80211w=2`(Management Frame Protection 강제), `sae_pwe=0`(구형 엔드포인트 호환)입니다. iPhone 7 Plus(iOS 15)가 SAE로 성공적으로 접속했습니다. AP는 SAE만 열고 WPA2 퇴로가 없으므로, 연결(association)을 완료할 수 있다는 것은 SAE 인증 핸드셰이크가 성립했음을 의미합니다. RTL8811AU + rtw88_8821au는 AP 측에서 WPA3-SAE를 사용할 수 있습니다.

---

## 4. 엔드투엔드 핸드셰이크 성능과 제한

### 4-1. 엔드투엔드 핸드셰이크 캡처 ✅

이것은 인젝션과 캡처를 실제로 "하나로 이을" 수 있는지 검증하는 종합 테스트로, 전 과정을 본인 소유 YUPITEK AP, 본인 소유 iPhone 7 Plus, 허가된 전제하에 진행했습니다. 흐름은 다음과 같습니다. 대상 채널을 모니터 → 본인 소유 장치에 지향성 deauth를 보내 재접속 유도 → 완전한 4-way(M1–M4) 캡처 → `hcxpcapngtool --all`로 hashcat이 읽을 수 있는 `.22000`으로 변환.

실측 결과: `aircrack-ng`가 YUPITEK에서 핸드셰이크 1개를 확보했다고 판정했고, EAPOL 네 개 메시지 M1–M4가 모두 도착했으며, client는 Apple OUI(`b8:53:ac`, iPhone 7 Plus로 확인)이고, 변환된 `.22000`은 바로 hashcat에 넣을 수 있습니다. 이는 AWUS036ACS가 완전한 엔드투엔드 핸드셰이크 캡처 성능을 갖추고 있음을 의미합니다.

실측에서 기록할 만한 두 가지 요점이 있습니다(완전한 단계별 설정은 별도 글 참고).

1. **사무실에서 같은 채널에 동명 AP가 여러 대 있을 때는 `--bssid`로 단일 대를 잠그지 말고**, 채널 전체를 캡처해야 다른 대에 연결된 장치를 놓치지 않습니다.
2. `hcxpcapngtool`는 기본적으로 엄격해 "not enough M1"을 반환할 수 있습니다. `--all`을 추가하면 완전한 M1–M4에서 `.22000`을 변환할 수 있습니다.

이 핸드셰이크 캡처 체인에 쓰인 Kali 상용 도구(aircrack-ng, hcxtools)는 모두 Ubuntu 24.04 ARM64에서 바로 실행되며, airodump-ng, aireplay-ng, hcxpcapngtool 모두 정상 작동합니다.

### 4-2. VIF(가상 인터페이스) ✅

`iw dev $IF interface add mon9 type monitor`로 모니터 VIF를 생성해 100 frames를 캡처할 수 있었습니다. 또한 스크립트로 "주 인터페이스는 YUPITEK에 STA로 연결 + AP VIF 하나"를 구성해, 단일 칩이 STA와 AP를 동시에 수행할 수 있었습니다.

### 4-3. 정직한 제한(실측 보고)

| 고급 모드 / 도구 | 상태 | 실측 |
|---|---|---|
| 액티브 모니터 | ❌ 미지원 | `iw set monitor active` → `Operation not supported (-95)` |
| Ad-hoc(IBSS) | ❌ 미지원 | 모드는 나열되나 `ibss join` 이후 `iw link` = Not connected |
| 메시(802.11s) | ❌ 미지원 | `set type mp` → `-95` |
| Wi-Fi Direct(P2P) | ❌ 미지원 | `interface add type __p2pcl` → `-95` |
| hcxdumptool 8.x | ⚠️ arm 불가 | `failed to arm interface`: rtw88_8821au는 액티브 모니터를 제공하지 않음. airodump-ng + aireplay-ng를 사용하세요 |

이 외에도 알아두어야 할 운영상의 제한이 두 가지 있습니다. 단일 스트림 1x1은 이론적 상한(HT Max RX 150 Mbps, VHT80 약 433 Mbps)을 결정하므로 처리량은 원래 이 카드의 강점이 아닙니다. 모니터 / AP를 반복 전환한 뒤에는 RX가 간혹 잠시 degraded 상태(아무것도 스캔되지 않음)가 되는데, 이때 카드를 물리적으로 한 번 뽑았다 꽂으면 복구됩니다. 인터페이스 이름은 MAC으로 결정되므로 뽑았다 꽂아도 그대로 유지됩니다.

---

## 5. 적용 시나리오와 제품 선정(경량 휴대용, Hub로 연결)

위의 성능을 제품 포지셔닝에 다시 대응시키면 AWUS036ACS의 역할은 명확합니다. 성능은 완전하지만 휴대성을 주력으로 하는 휴대용 카드입니다. 그렇다면 어떤 시나리오에 적합할까요?

- **현장 신속 실사 / 휴대 진단**: 단일 안테나, 작은 크기, 저전력으로 들고 나가 채널 실사, 신호 순회 점검, 패킷 진단을 하기에 적합합니다. GX10 같은 중앙 플랫폼과 조합하면 휴대용 카드가 현장에서 캡처하고 데이터를 Hub로 연결해 집중 분석하는 분업이 명확합니다.
- **교육과 검증**: 모니터 / 인젝션 / AP / WPA3-SAE / 엔드투엔드 핸드셰이크라는 이 주력 라인을 모두 통과하므로, 시연 및 허가 범위 내 검증용 카드로 적합합니다.
- **적합하지 않은 시나리오**: 최고 처리량, 최장 거리가 필요하거나 메시 / IBSS / P2P / 액티브 모니터가 필요한 상황이라면 이 카드는 올바른 선택이 아닙니다.

경량이 기능 축소를 뜻하지는 않습니다. 주력 성능은 하나도 빠지지 않으며, 절충된 것은 처리량 상한과 고급 인터페이스 모드입니다. 따라서 이 카드를 선택할지는 "들고 다니는 것"을 원하는지 "최대로 달리는 것"을 원하는지에 달렸습니다.

같은 제품군과 비교한 포지셔닝 차이는 다음과 같습니다.

| 요구 | 권장 카드 | 이유 |
|---|---|---|
| 경량 휴대 + 주력 성능 완비 | **AWUS036ACS** | 2.4G 인젝션 100%, 5G 96%, 엔드투엔드 핸드셰이크 사용 가능, 단일 안테나로 가벼움 |
| 듀얼 밴드 인젝션 모두 100% / 더 안정적인 침투 검증 | AWUS036EACS, AWUS036ACH | 양쪽 대역 인젝션 100%, EACS는 BT도 포함 |
| 최강 수신 / 장거리 모니터 | AWUS036AXER, AWUS036ACH | 주파수 호핑으로 더 많은 대상을 스캔 / 듀얼 안테나 고이득 |
| 메시 / IBSS 단일 기기 실험 | AWUS036ACM, AWUS036ACHM | mt76 드라이버로 단일 기기에서 생성 가능(Realtek rtw88은 미지원) |

한마디로 정리하는 제품 선정: 가벼우면서 주력 성능도 두루 갖추려면 AWUS036ACS가 적합한 휴대용 선택이고, 듀얼 밴드 인젝션 모두 100% 또는 더 무거운 침투 검증이 필요하면 EACS / ACH로 가세요.

---

## 자주 묻는 질문(FAQ)

**Q: AWUS036ACS는 Ubuntu 24.04 ARM64에서 드라이버를 설치해야 하나요?**
본문에서 테스트한 kernel 6.17(ASUS GX10)에서는 필요 없습니다. RTL8811AU는 내장 rtw88_8821au 드라이버로 구동되어 꽂으면 바로 인식하며, 컴파일도 DKMS도 필요 없습니다. kernel이 더 오래된 경우에는 먼저 `modinfo rtw88_8821au`로 모듈이 존재하는지 확인하세요.

**Q: AWUS036ACS는 모니터 모드와 패킷 인젝션을 지원하나요?**
지원합니다. 2.4 GHz, 5 GHz 모두 모니터 가능하며, `aireplay-ng --test` 인젝션은 2.4G가 100%(30/30), 5G가 96%(29/30, 먼저 `iw reg set US`로 TW 제한을 해제해야 함)입니다. 액티브 모니터는 지원하지 않습니다.

**Q: AWUS036ACS로 WPA 핸드셰이크를 캡처해 hashcat .22000으로 변환할 수 있나요?**
가능합니다. 본인 소유 AP와 본인 소유 iPhone 7 Plus에서 엔드투엔드로 실측: 지향성 deauth로 재접속을 유도하고 완전한 4-way(M1–M4)를 캡처한 뒤 `hcxpcapngtool --all`로 .22000을 변환합니다. 본인 소유 또는 허가된 네트워크에서만 가능합니다.

**Q: AWUS036ACS를 AP 핫스팟으로 쓸 수 있나요? WPA3을 지원하나요?**
가능합니다. `hostapd`로 2.4G와 5G 핫스팟(5G 채널 폭은 확인하지 못함)을 열어 iPhone 7 Plus가 접속해 4-way를 완료했으며, 5G의 WPA3-SAE(SAE-only, ieee80211w=2, sae_pwe=0)도 접속에 성공했습니다(2.4G의 WPA3는 실측하지 않음).

**Q: AWUS036ACS가 지원하지 않는 모드는 무엇인가요? hcxdumptool은 사용할 수 있나요?**
액티브 모니터, IBSS, 메시(802.11s), Wi-Fi Direct(P2P)를 지원하지 않습니다. hcxdumptool 8.x는 failed to arm interface가 발생하므로 airodump-ng + aireplay-ng를 사용하세요. 메시 / IBSS가 필요하면 AWUS036ACM / ACHM을 선택하세요.

---

## 6. 더 읽어보기

- 9종 ALFA 카드의 완전한 성능 비교 및 제품 선정 종합 평가 → [ALFA 무선 네트워크 카드 종합 평가 Hub(종합표)](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [드라이버 설치 불필요: Ubuntu 24.04 + kernel 6.17에서 모니터 / AP 활성화(rtw88 / rtw89 / mt76 실측)](/ko/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- [WPA3-SAE와 엔드투엔드 핸드셰이크 캡처 단계별 튜토리얼](/ko/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 같은 제품군 BT+WiFi 복합 카드 → [AWUS036EACS 카드별 실측 테스트](/ko/blog/awus036eacs-asus-gx10-ubuntu-test-report/)

---

*테스트 기관: Yupitek(ALFA Network 대만 총판) — https://www.yupitek.com | 테스트 환경: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | 테스트 장치: Apple iPhone 7 Plus*
