---
title: "AWUS036AXER 실측 리포트: ASUS GX10 + Ubuntu 24.04(ARM64)에서 수신 성능이 가장 강한 Wi-Fi 6 무선 랜카드"
slug: awus036axer-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axer-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036axer
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - ubuntu-24-04
  - kernel-6-17
  - arm64
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
description: "AWUS036AXER를 ASUS GX10 / Ubuntu 24.04 ARM64에서 드라이버 설치 불필요(rtw89_8852bu)로 실측: 모니터 60초 동안 63 AP+12 client 캡처, 인젝션 73%(2.4G), 5G VHT80 AP와 WPA3 모두 통과."
faq:
  - question: "AWUS036AXER는 Ubuntu 24.04나 Kali에서 드라이버를 따로 설치해야 하나요?"
    answer: "Ubuntu 24.04(ARM64, kernel 6.17.0-1014-nvidia)에서는 필요 없습니다. 커널에 내장된 rtw89_8852bu 드라이버가 꽂자마자 인식되며, 컴파일도 DKMS도 불필요합니다(firmware rtw8852b_fw 0.29.29.5). 본문의 플랫폼은 Kali가 아니라 Ubuntu이며, Kali 본체는 테스트하지 않았습니다. Kali에서 자주 쓰는 도구인 airmon-ng, kismet, bettercap, wifite, Wireshark는 이 플랫폼에서 사용할 수 있습니다. 커널이 오래된 경우 내장을 보장하지 않으니 먼저 버전을 확인하세요."
  - question: "AWUS036AXER는 모니터 모드를 지원하나요? 수신 성능은 얼마나 강한가요?"
    answer: "지원합니다. 2.4 GHz와 5 GHz 모두 모니터로 진입할 수 있습니다. 본인 소유 사무실에서 airodump-ng로 60초간 채널 호핑 스캔을 돌려 63개 AP와 12개 client를 캡처했으며, 같은 자리에서 테스트한 9종 카드 가운데 수신이 가장 강한 한 장이었습니다. 동일 칩셋의 AWUS036AX는 다른 회차 테스트에서 14 AP+4 client였습니다(두 측정은 비동기이므로 참고용)."
  - question: "AWUS036AXER로 패킷 인젝션(packet injection)을 할 수 있나요?"
    answer: "가능합니다. 2.4 GHz의 aireplay-ng --test 응답률은 73%(22/30)였고 Injection is working!가 표시되었으며, 5 GHz도 AP별 자체 테스트를 통과했습니다. 본인 소유 네트워크와 기기에서 handshake 캡처를 완료하고 .22000으로 변환했습니다. 두 밴드 모두 100%에 가까운 성공률을 원한다면, 이 플랫폼 실측 기준으로 AWUS036EACS, ACH, ACS가 더 안정적입니다. 본인 소유 또는 허가된 네트워크에서만 사용하세요."
  - question: "AWUS036AXER와 AWUS036AX는 무엇이 다른가요?"
    answer: "둘 다 Realtek RTL8832BU를 쓰고 rtw89_8852bu 드라이버를 공유하며, 이 플랫폼에서 모드 지원과 인젝션 동작이 동일합니다. 차이는 안테나 튜닝과 이득이 가져오는 수신 성능입니다(AXER는 60초에 63 AP+12 client, AX는 14 AP+4 client). 둘 다 내장 안테나이며 RP-SMA가 없으니, 안테나 사양은 제품 페이지를 기준으로 하세요."
  - question: "AWUS036AXER를 AP로 쓰거나 WPA3를 켤 수 있나요? 지원하지 않는 모드는 무엇인가요?"
    answer: "가능합니다. 2.4 GHz 802.11n과 5 GHz VHT80(VHT-NSS2, 351 Mbit) 모두 iPhone이 접속해 authorized되었고, WPA3-SAE는 sae_pwe=0으로 iPhone 15 Pro가 접속했으며(2.4 GHz, 5 GHz WPA3는 실측하지 않음), STA+AP 병행도 사용 가능합니다. 다만 rtw89_8852bu는 active monitor, IBSS, mesh를 지원하지 않습니다."
draft: false
---

{{< tldr >}}AWUS036AXER는 ASUS GX10 / Ubuntu 24.04 ARM64에서 꽂자마자 바로 사용 가능합니다(커널 내장 rtw89_8852bu). 모니터 60초 동안 63 AP+12 client를 캡처하고, 2.4 GHz 인젝션 73%, AP와 WPA3 모두 통과합니다. active monitor, IBSS, mesh는 지원하지 않습니다.{{< /tldr >}}

> 본 글은 Yupitek(ALFA 대만 유통사)이 본인 소유 장비에서 수행한 제품 호환성 및 성능 실측입니다.
> 테스트 플랫폼: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. 테스트 환경은 본인 소유 사무실 Wi-Fi(SSID `YUPITEK`)이며, 본인 소유 테스트용 스마트폰 iPhone 7 Plus(WPA3는 별도로 iPhone 15 Pro)로 진행했습니다.
> ⚠️ **합법적 사용**: 모니터와 인젝션은 본인 소유 또는 허가된 네트워크와 기기에서만 수행하세요. AP 모드는 해당 지역의 무선 전파 규정을 준수하세요. 본 글은 랜카드의 성능, 호환성, 설정, 제품 선정에 초점을 맞추며, 제3자 네트워크에 대한 어떠한 공격 행위도 다루지 않습니다.

---

## 1. 이 카드와 테스트 플랫폼

AWUS036AXER는 ALFA의 Wi-Fi 6(802.11ax) 2x2 USB 랜카드로, Realtek RTL8832BU 칩셋(블루투스 없음)을 채택했습니다. 같은 제조사의 AWUS036AX와 **동일한 칩셋, 동일한 드라이버**(`rtw89_8852bu`)를 사용하며, 이 플랫폼에서 모드 지원과 동작이 일치합니다. 두 카드의 진짜 차이는 외장이냐 내장이냐가 아니라 **안테나 튜닝과 이득**입니다. AXER는 **내장(Nano) 안테나 설계, RP-SMA 없음**으로, 칩셋과 RF 튜닝으로 수신 성능을 최대한 끌어올렸습니다. 이 글의 핵심 결론을 먼저 기억해 두세요. 같은 자리에서 비교한 9종 ALFA 카드 중에서 AXER의 **수신이 가장 강한 한 장**입니다.

테스트 플랫폼은 ASUS GX10으로, NVIDIA GB10 슈퍼칩과 128GB 통합 메모리를 탑재했고, 운영체제는 Ubuntu 24.04 LTS, 아키텍처는 ARM64(aarch64), 커널은 `6.17.0-1014-nvidia`입니다. 모든 결과는 2026-11-18에 이 장비에서 실기로 측정했으며, 테스트 기기는 본인 소유 iPhone 7 Plus(WPA3는 별도로 iPhone 15 Pro), 테스트 네트워크는 본인 소유 사무실 Wi-Fi입니다. 유통 검증 관점에서 ARM64에 최신 커널 조합은 상대적으로 까다로운 조합인데, 아래 2절에서 이 세대가 오히려 더 손이 덜 가는 이유를 설명합니다.

사양 맥락을 조금 보태면, AXER는 2x2(듀얼 공간 스트림) Wi-Fi 6 카드로 두 개의 공간 스트림을 동시에 송수신할 수 있으며, 이는 뒤의 5 GHz AP 실측에서 협상된 VHT-NSS2에도 대응됩니다. 다만 이 카드가 이번 회차에서 승리한 것은 스트림 수가 아니라 안테나 설계와 RF 튜닝 덕분입니다(AX도 동일하게 2x2). 칩셋, 드라이버, 플랫폼이 모두 같고 안테나 튜닝이 사실상 유일한 변수이므로, AXER와 AX의 수신 차이는 내장 안테나 설계와 이득 튜닝으로 깔끔하게 귀속할 수 있습니다.

---

## 2. 하드웨어와 드라이버(내장 안테나, 드라이버 설치 불필요)

AWUS036AXER는 Ubuntu 24.04의 6.17 커널에서 **꽂자마자 인식되고, 컴파일 불필요, DKMS 불필요**입니다. 드라이버 `rtw89_8852bu`는 이미 in-kernel 모듈이며, firmware는 `rtw8852b_fw`(버전 0.29.29.5)로 부팅 시 로드됩니다. GitHub에서 out-of-tree 프로젝트를 받거나 DKMS에 묶을 필요가 없습니다. 장기 운영과 여러 차례의 커널 업데이트를 거쳐야 하는 유통·교육 환경에서는, 드라이버 컴파일 단계가 사라지는 것만으로도 가장 흔한 장애 지점 하나가 줄어듭니다.

옛날 방식과 대조하면 더 체감됩니다. 과거 Realtek의 이런 USB 칩셋은 대부분 mainline 커널에 들어가지 못해, 사용자가 GitHub에서 out-of-tree 프로젝트(예: `morrownr/USB-WiFi`)를 받아 DKMS로 현재 커널에 묶어 컴파일해야 했고, 커널이 업데이트될 때마다 다시 컴파일해야 했으며, 한 번 컴파일이 실패하면 랜카드가 그대로 사라졌습니다. rtw89가 in-kernel로 정식 편입된 뒤에는 이런 단계가 6.17에서 통째로 생략되며, 같은 조작을 같은 드라이버를 쓰는 여러 카드에 반복 적용할 수도 있습니다.

먼저 카드가 올바르게 인식되는지 확인합니다:

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
# Bus 00x Device 00x: ID 0bda:b832 Realtek Semiconductor Corp. 802.11ac WLAN Adapter
```

정상 WLAN 모드의 USB ID는 `0bda:b832`입니다. `0bda:1a2b`로 보인다면 카드가 아직 "CD-ROM 모드"에 머물러 있다는 뜻이므로, `sudo usb_modeswitch -v 0bda -p 1a2b -K`를 한 번 실행해 WLAN 모드로 전환하면 됩니다. 본 테스트에서는 이 카드가 바로 WLAN 모드로 열거되어 CD-ROM 모드를 겪지 않았습니다.

인터페이스 이름은 `wlx` + MAC 방식(예: `wlxAABBCCDDEEFF`)으로, 어느 기기에 꽂아도 바뀌지 않아 스크립트에서 고정 바인딩하기 편합니다. 이 카드가 지원하는 모드를 조회합니다:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

실측에서 보고된 모드는 managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO입니다. 여기에 IBSS, mesh도, active monitor도 없는데, 이는 rtw89 드라이버의 선천적 제약입니다. 4절에서 정직하게 설명하니 제품 선정 시 오판하지 마세요.

안테나 부분: AXER는 내장(Nano) 안테나 설계, RP-SMA 없음이며, 동일 칩셋의 AX와 비교해 차이는 안테나 튜닝과 이득에 있고, 실무에서 가장 직접적으로 드러나는 것은 수신 감도입니다. 다음 절의 모니터 데이터가 이 점을 분명히 보여줍니다.

---

## 3. 실측 성능

세 가지 핵심 성능(Monitor / Injection / AP)과 WPA3의 실측 결과를 먼저 표로 정리하고, 세부 사항은 표 뒤에서 항목별로 펼칩니다:

| 성능 | 2.4 GHz | 5 GHz | 실측 요점 |
|---|---|---|---|
| **Monitor(모니터)** | ✅ 강함 | ✅ 강함 | 채널 호핑으로 **63 AP + 12 client** 캡처, 9종 카드 중 수신 최강 |
| **Injection(인젝션)** | ✅ 73% | ✅ 사용 가능 | 2.4G `22/30 73%`; 5G `Injection is working!` |
| **AP(핫스팟)** | ✅ 802.11n | ✅ VHT 80 MHz | iPhone 접속; 5G VHT-NSS2, 351 Mbit |
| **WPA3-SAE** | ✅ | 미실측 | AP 측 iPhone 15 Pro 접속(`sae_pwe=0`), 2.4 GHz에서만 실측 |
| **WPA handshake 캡처** | ✅ 엔드투엔드 | — | 본인 소유 네트워크+본인 소유 기기, 4-way(M1–M4)→ `.22000` |

### 3-1. Monitor(이번 글의 하이라이트: 수신 최강)

모니터 전환은 표준 `iw` 흐름입니다. 먼저 인터페이스를 직접 관리로 되돌리고(`nmcli dev set $IF managed no`), 인터페이스를 내린 뒤 monitor type을 설정하고, 인터페이스를 올린 다음 채널을 지정합니다:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36        # 5 GHz; 2.4 GHz는 channel 6 사용
sudo timeout 8 tcpdump -l -i $IF -nn -e -c 200
```

2.4 GHz와 5 GHz 각각 6초 이내에 100 frames를 가득 채웠습니다. 진짜 격차를 벌린 것은 채널 호핑 스캔입니다. `sudo airodump-ng --band abg $IF`를 60초 돌려 **63개 AP와 12개 client를 캡처**했습니다. 이는 이번 회차 9종 카드 중 가장 많은 대상을 잡은 한 장으로, 내장 안테나 설계와 RF 튜닝이 가져오는 수신 우위를 직접 반영합니다. 현장 조사(site survey), 장거리 모니터링, 또는 신호가 약한 환경에서는 이 수신 능력이 바로 AXER의 핵심 가치입니다.

### 3-2. Injection(인젝션)

인젝션은 aireplay-ng의 자체 테스트 모드로 검증하며, 측정 대상은 외부 공격이 아니라 랜카드 자체의 능력입니다:

```bash
sudo iw dev $IF set channel 6
sudo aireplay-ng --test $IF
# Found 21 APs
# 22/30:  73%
# Injection is working!
```

2.4 GHz 응답률은 73%(22/30)로 사용 가능 판정입니다. 5 GHz는 지정 AP를 대상으로 한 AP별 자체 테스트에서도 `Injection is working!`을 보고했습니다. 플랫폼 공통 원칙을 하나 보태면, **5 GHz에서 송신/인젝션하기 전에 먼저 `iw reg set US`로 TX 출력을 해제하고, 테스트가 끝나면 `iw reg set TW`로 대만 규정 밴드로 되돌리는 것**을 잊지 마세요.

### 3-3. AP 핫스팟(2.4 GHz 802.11n, 5 GHz VHT 80 MHz)

AXER는 두 밴드 모두 hostapd AP를 띄울 수 있습니다. 2.4 GHz는 `hw_mode=g` + `ieee80211n=1`로 802.11n 핫스팟을 띄워, iPhone 7 Plus가 MCS 15로 협상해 authorized되었습니다. 5 GHz는 `hw_mode=a` + `ieee80211ac=1` + `vht_oper_chwidth=1`로 VHT 80 MHz 핫스팟을 띄워, iPhone 7 Plus가 **VHT-NSS2, 80 MHz, 351 Mbit, authorized**로 협상되었습니다. AP를 띄우기 위한 사전 작업은 `sudo nmcli dev set $IF managed no`이며, `wpa_passphrase`는 최소 8자여야 합니다. 그렇지 않으면 hostapd가 `invalid WPA passphrase length`를 반환합니다.

### 3-4. WPA3-SAE와 handshake 캡처

WPA3-SAE는 AP 측에서 `wpa_key_mgmt=SAE`, `ieee80211w=2`, `sae_pwe=0`을 설정했고, 실측에서 iPhone 15 Pro가 접속했습니다. **`sae_pwe`는 이번 ALFA 카드들에서 호환성의 지뢰밭입니다.** 일부 기기는 `sae_pwe=2`(Hash-to-Element)에서 접속하지 못하는데, `sae_pwe=0`으로 설정하면 비교적 오래된 iPhone과 호환됩니다.

handshake 능력은 **본인 소유 사무실 Wi-Fi(YUPITEK)+본인 소유 테스트 기기**에서 수행한 엔드투엔드 검증입니다. 완전한 4-way(M1/M2/M3/M4)를 캡처한 뒤 `hcxpcapngtool`로 hashcat이 읽을 수 있는 `.22000`으로 변환했습니다. 여기서 GX10 플랫폼의 공통 현상 하나를 짚어야 합니다. **`hcxdumptool`은 이 플랫폼의 모든 USB 카드(2.4 GHz의 AWUS036EACS 제외)에서 `failed to arm`이 발생합니다**(GX10의 3밴드 내장 랜카드 열거 충돌에 더해, 드라이버에 active monitor가 없음). 그래서 handshake 흐름은 aircrack-ng 제품군(airodump-ng + aireplay-ng)으로 우회했습니다. AXER의 인젝션 능력은 이 경로에서 충분히 쓸 만합니다.

---

## 4. 고급 기능과 정직한 한계

**VIF(STA + AP 병행) ✅**: AXER는 station으로 상위 Wi-Fi에 접속하면서 동시에 AP VIF를 띄울 수 있습니다. 실측에서 메인 인터페이스는 YUPITEK에 접속하고 AP VIF는 ch36 VHT80에서 병행했으며, STA 측 ping은 3.5 ms로, "접속하면서 동시에 핫스팟을 여는" 시나리오에 적합합니다.

**Wi-Fi Direct(P2P) 미테스트(⬜)**: 드라이버가 P2P-client / P2P-GO를 선언하지만, 완전히 검증하려면 두 번째 상대 장비가 필요하므로 이번 회차에서는 건너뛰었고, 따라서 검증된 능력에는 포함하지 않습니다. 이처럼 "드라이버는 지원을 선언했으나 실기로 돌려보지 않은" 항목은 일률적으로 정직하게 미테스트로 표기하며, 통과로 부풀리지 않습니다.

**지원하지 않는 세 가지 모드(N/A)**: `rtw89_8852bu` 드라이버는 **active monitor, Ad-hoc(IBSS), Mesh(802.11s)를 제공하지 않습니다**. `iw dev $IF set type ibss` 또는 `mp`는 바로 실패하며, 이는 드라이버 레이어의 제약으로 설정으로 우회할 수 없습니다. 용도가 mesh나 IBSS 실험이라면 MediaTek mt76 계열(예: AWUS036ACM / ACHM)을 봐야 합니다.

**플랫폼 공통 주의사항:**

- 절대로 `airmon-ng check kill`을 실행하지 마세요. NetworkManager를 꺼버려 GX10이 외부와 단절됩니다. `wlx*` 인터페이스만 조작하고, 내장된 외부 인터넷 랜카드는 건드리지 마세요.
- 모니터/AP를 반복 전환한 뒤 갑자기 아무것도 스캔되지 않으면(RX stall), 카드를 **한 번 뽑았다 꽂으면** 복구됩니다(USB 재열거, 인터페이스 이름은 MAC으로 결정되므로 바뀌지 않음).
- ARM64 플랫폼에서는 aircrack-ng를 소스에서 컴파일해야 하며, wifite는 git 버전을 써서 apt 의존성 충돌을 우회합니다.

**Kali 도구 호환성**: airmon-ng, kismet 2026.10, bettercap 2.32, wifite(git), Wireshark / tshark 4.2 모두 AXER를 데이터 소스나 관리 인터페이스로 정상적으로 사용할 수 있습니다.

---

## 5. 적용 시나리오와 제품 선정 제안

한마디로 정리하면: **AXER는 "수신 지향" Wi-Fi 6 카드**입니다. AX와 동일 칩셋에 기능도 일치하며, 차이는 안테나 튜닝과 이득이 가져오는 수신 우위이므로, 제품 선정 논리가 매우 명확합니다:

| 당신의 요구 | AXER가 1순위인가 | 설명 |
|---|---|---|
| 최강 수신 / 장거리 monitor / 현장 조사 | ✅ **1순위** | 채널 호핑으로 63 AP + 12 client 캡처, 9종 카드 중 최강; AWUS036ACH(듀얼 안테나 고이득)와 상호 보완 가능 |
| Wi-Fi 6 + AP 핫스팟 | ✅ 적합 | 2x2, 5G VHT80; AWUS036AX와 동급 |
| Injection + 엔드투엔드 handshake | 🟡 사용 가능 | 2.4G 73% 사용 가능; 두 밴드 모두 100%에 가깝게 원하면 AWUS036EACS / ACH / ACS가 더 안정적 |
| mesh / IBSS 실험 | ❌ 부적합 | rtw89 미지원, AWUS036ACM / ACHM(mt76)으로 대체 |

전형적인 현장 적용 시나리오: AXER를 **원격 무선 모니터링 노드**로 삼아, 신호가 약하거나 거리가 먼 지점에 두고, 내장 안테나의 수신 우위로 현장의 AP / client를 최대한 전부 캡처한 뒤, 스캔 결과를 중앙 호스트로 취합해 통합 검토합니다. 내장(Nano) 안테나이고 RP-SMA가 없어 안테나를 교체할 수 없으므로, 더 높은 이득이나 강한 지향성이 필요하면 듀얼 안테나 고이득의 AWUS036ACH와 상호 보완하면 됩니다.

반대로 용도가 순수 AP나 일반 접속이고 인젝션이 전혀 필요 없다면, MediaTek의 AWUS036AXM / AXML도 쓸 수 있습니다. 다만 **인젝션이나 handshake가 조금이라도 얽히면 AXM / AXML을 선택하지 마세요.** 이들은 이 플랫폼에서 인젝션이 실패합니다(주된 원인은 kernel 6.16 이후 mac80211 chanctx 회귀이며, 여기에 firmware가 인젝션 속도를 1/6 Mbps로 고정하는 문제가 더해진 것으로, 칩셋 자체의 한계는 아닙니다). AXER는 정확히 반대입니다. 인젝션 사용 가능, 수신 또한 최강입니다.

9종 카드의 전체 매트릭스와 교차 비교를 한 번에 보려면 종합 평가 페이지로 돌아가세요 → [`/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

---

## 자주 묻는 질문(FAQ)

**Q1. AWUS036AXER는 Ubuntu 24.04나 Kali에서 드라이버를 따로 설치해야 하나요?**
Ubuntu 24.04(ARM64, kernel 6.17.0-1014-nvidia)에서는 필요 없습니다. 커널에 내장된 `rtw89_8852bu` 드라이버가 꽂자마자 인식되며, 컴파일도 DKMS도 불필요합니다(firmware `rtw8852b_fw` 0.29.29.5). 본문의 플랫폼은 Kali가 아니라 Ubuntu이며, Kali 본체는 테스트하지 않았습니다. Kali에서 자주 쓰는 도구인 airmon-ng, kismet, bettercap, wifite, Wireshark는 이 플랫폼에서 사용할 수 있습니다. 커널이 오래된 경우 내장을 보장하지 않으니 먼저 버전을 확인하세요.

**Q2. AWUS036AXER는 monitor mode를 지원하나요? 수신 성능은 얼마나 강한가요?**
지원합니다. 2.4 GHz와 5 GHz 모두 모니터로 진입할 수 있습니다. 본인 소유 사무실에서 airodump-ng로 60초간 채널 호핑 스캔을 돌려 63개 AP와 12개 client를 캡처했으며, 같은 자리에서 테스트한 9종 카드 가운데 수신이 가장 강한 한 장이었습니다. 동일 칩셋의 AWUS036AX는 다른 회차 테스트에서 14 AP+4 client였습니다(두 측정은 비동기이므로 참고용).

**Q3. AWUS036AXER로 패킷 인젝션(packet injection)을 할 수 있나요?**
가능합니다. 2.4 GHz의 `aireplay-ng --test` 응답률은 73%(22/30)였고 `Injection is working!`가 표시되었으며, 5 GHz도 AP별 자체 테스트를 통과했습니다. 본인 소유 네트워크와 기기에서 handshake 캡처를 완료하고 `.22000`으로 변환했습니다. 두 밴드 모두 100%에 가까운 성공률을 원한다면, 이 플랫폼 실측 기준으로 AWUS036EACS, ACH, ACS가 더 안정적입니다. 본인 소유 또는 허가된 네트워크에서만 사용하세요.

**Q4. AWUS036AXER와 AWUS036AX는 무엇이 다른가요?**
둘 다 Realtek RTL8832BU를 쓰고 `rtw89_8852bu` 드라이버를 공유하며, 이 플랫폼에서 모드 지원과 인젝션 동작이 동일합니다. 차이는 안테나 튜닝과 이득이 가져오는 수신 성능입니다(AXER는 60초에 63 AP+12 client, AX는 14 AP+4 client). 둘 다 내장 안테나이며 RP-SMA가 없으니, 안테나 사양은 제품 페이지를 기준으로 하세요.

**Q5. AWUS036AXER를 AP로 쓰거나 WPA3를 켤 수 있나요? 지원하지 않는 모드는 무엇인가요?**
가능합니다. 2.4 GHz 802.11n과 5 GHz VHT80(VHT-NSS2, 351 Mbit) 모두 iPhone이 접속해 authorized되었고, WPA3-SAE는 `sae_pwe=0`으로 iPhone 15 Pro가 접속했으며(2.4 GHz, 5 GHz WPA3는 실측하지 않음), STA+AP 병행도 사용 가능합니다. 다만 `rtw89_8852bu`는 active monitor, IBSS, mesh를 지원하지 않습니다.

---

## 6. 더 읽어보기

- 9종 ALFA 카드 종합 매트릭스와 제품 선정 종합표(Monitor · Injection · AP 전체 비교) → `/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`
- 동일 칩셋의 AWUS036AX 실측(안테나 튜닝 차이) → `/ko/blog/awus036ax-asus-gx10-ubuntu-test-report/`
- 드라이버 설치 불필요: in-kernel 드라이버로 Monitor와 AP 모드 활성화 → `/ko/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`
- WPA3-SAE 시대의 handshake 캡처 능력과 `sae_pwe` 호환성 → `/ko/blog/alfa-wpa3-sae-handshake-capability-arm64/`

<!-- 더 읽어보기 내부 링크는 확정 후 정식 hreflang 대응 URL을 보완할 예정이며, 위는 ko slug placeholder입니다. -->

---

*테스트 기관: Yupitek(ALFA 유통사) — https://www.yupitek.com | 테스트 플랫폼: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | 테스트 기기: Apple iPhone 7 Plus(WPA3는 별도로 iPhone 15 Pro)*
