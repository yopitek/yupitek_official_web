---
title: "AWUS036ACM 카드별 실측 테스트: MediaTek MT7612U(mt76x2u)의 ASUS GX10 + Ubuntu 24.04(ARM64) 모니터 / 인젝션 / AP 및 mesh 능력 보고서"
slug: awus036acm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acm-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036acm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acm
  - mt7612u
  - mt76x2u
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - mesh
description: "AWUS036ACM(MT7612U)은 Ubuntu 24.04 ARM64에서 드라이버 설치 불필요하며, 듀얼 밴드 모니터 모드와 aircrack-ng(Kali에서 자주 사용)를 쓸 수 있고, 패킷 인젝션은 2.4G 63–83%, 5G 76%, VIF와 단일 기기 mesh / IBSS를 지원합니다."
faq:
  - question: "AWUS036ACM은 Ubuntu나 Kali에서 드라이버를 설치해야 하나요?"
    answer: "필요 없습니다. MT7612U는 커널에 내장된 mt76x2u 드라이버가 담당하므로 Ubuntu 24.04(kernel 6.17)에서 꽂으면 바로 인식되며, DKMS도 수동 펌웨어 설치도 필요 없습니다. 이번 실측 플랫폼은 Ubuntu 24.04 ARM64이며, Kali도 커널이 충분히 최신이면 원칙적으로 동일하지만 이번에는 Kali 실기에서 검증하지 않았습니다."
  - question: "AWUS036ACM은 모니터 모드에 들어가고 패킷 인젝션을 할 수 있나요? 성공률은 얼마인가요?"
    answer: "가능합니다. 2.4GHz와 5GHz 모두 모니터 모드에 들어가 정상적으로 캡처할 수 있으며, aireplay-ng 인젝션 테스트는 2.4GHz에서 63–83%, 5GHz에서 76%로 아홉 장의 카드 중 중간 수준입니다. 듀얼 밴드 인젝션을 모두 100%로 원한다면 Yopitek 실측 기준 AWUS036ACH, AWUS036EACS가 더 낫습니다."
  - question: "AWUS036ACM은 핫스팟을 열면서 동시에 인터넷에 접속할 수 있나요(VIF)?"
    answer: "가능합니다. STA+AP(한쪽은 상위망에 연결, 한쪽은 핫스팟 개설)와 AP+monitor(핫스팟을 열면서 동시에 모니터링) 두 가지 조합 모두 실측에서 성립했으며, 이는 mt76 드라이버의 다중 인터페이스 동시 운용이 비교적 완성도 높은 부분입니다. 5GHz 핫스팟은 VHT 80 MHz까지 열 수 있습니다."
  - question: "AWUS036ACM은 mesh(802.11s)와 IBSS를 지원하나요?"
    answer: "단일 기기에서 생성 가능합니다. Ubuntu 24.04 / kernel 6.17에서 AWUS036ACM은 802.11s mesh와 IBSS(Ad-hoc) 인터페이스를 생성할 수 있지만, 이번에는 두 번째 노드가 없어 다중 노드 상호 연결은 아직 검증하지 못했으므로 단일 기기에서 생성 가능하다고만 말할 수 있습니다."
  - question: "AWUS036ACM은 WPA handshake를 캡처할 수 있나요?"
    answer: "네. 자체 AP와 자체 iPhone 7 Plus를 대상으로 엔드투엔드가 성공했습니다. deauth, 완전한 4-way(M1–M4) 캡처, hcxpcapngtool --all로 hashcat .22000 추출까지 완료했습니다. 본인 소유 또는 허가된 네트워크에서만 진행합니다."
draft: false
---

> 본 글은 Yopitek이 ALFA AWUS036ACM을 최신 Linux 플랫폼에서 테스트한 제품 호환성 및 능력 실측 기록으로, 제품 선정 평가용입니다.
> 테스트 플랫폼: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. 모든 데이터는 Yopitek이 **자체 장비, 자체 사무실 Wi-Fi**(SSID `YUPITEK`, 2.4G ch5 / 5G ch36, ch157)에서 **자체 테스트용 스마트폰**(Apple iPhone 7 Plus, WPA3는 iPhone 15 Pro로 추가 재측정)을 대상으로 한 실측 발췌입니다.
> ⚠️ **합법성 및 범위 고지**: 모니터, 인젝션, 핸드셰이크 캡처는 본인 소유 또는 허가된 네트워크와 기기에서만 진행하며, AP 모드는 현지 무선 전파 규정을 준수하십시오. 본 글은 네트워크 카드 자체의 능력, 호환성, 설정에 초점을 맞추며, **제3자 네트워크를 대상으로 한 어떠한 공격 행위도 다루지 않습니다**.

## 핵심 요약(TL;DR)

Yopitek(ALFA Network 대만 총판)이 ASUS GX10 / Ubuntu 24.04 ARM64(kernel 6.17)에서 실측한 결과, AWUS036ACM은 듀얼 밴드 monitor 모드가 가능하고, 패킷 인젝션은 2.4G 63–83%, 5G 76%이며, 두 밴드 모두 AP 핫스팟을 구성할 수 있습니다(5G는 VHT 80 MHz).

- Ubuntu 24.04(ARM64) 드라이버 설치 불필요: MT7612U는 kernel 6.17에 내장된 mt76x2u가 담당하여 꽂으면 바로 인식되며, DKMS가 필요 없습니다.
- 듀얼 밴드 모니터 모드(monitor mode) 사용 가능; 패킷 인젝션은 2.4G 63–83%, 5G 76%로 아홉 장 중 중간 수준입니다.
- 단일 기기에서 802.11s mesh와 IBSS를 생성할 수 있으며, VIF(STA+AP, AP+monitor)를 지원합니다.
- WPA handshake 캡처는 엔드투엔드(완전한 4-way, hashcat `.22000` 추출)로 완료했으며, 완료한 9장 중 7장에 속합니다.
- 듀얼 밴드 인젝션을 모두 100%로 원한다면 AWUS036ACH 또는 AWUS036EACS를 선택하기를 권장합니다.

---

## 1. 이 카드와 테스트 플랫폼

AWUS036ACM은 ALFA 제품 라인의 MediaTek 듀얼 밴드 카드로, 칩은 MT7612U, Wi-Fi 5(802.11ac), 2T2R 듀얼 공간 스트림, 2.4GHz / 5GHz 듀얼 밴드입니다. morrownr의 목록에 오랫동안 Kali 추천 카드로 올라 있는데, 그 이유는 처리량 수치가 아니라 `mt76` 계열 드라이버가 Linux의 모니터, 인젝션, 다중 인터페이스 동시 운용(VIF) 지원이 비교적 완성도 높기 때문입니다. 802.11s mesh 같은 실험적 모드는 이 플랫폼에서도 mt76 진영만 구동할 수 있습니다(Realtek 카드는 단일 기기 IBSS만 생성할 수 있고 mesh는 구동하지 못합니다). 따라서 이 카드를 평가할 때 핵심은 속도가 아니라 능력 측면이 두루 갖춰져 있는지, mt76의 특색이 실제로 구현되는지, 그리고 어떤 항목을 정직하게 경계로 표시해야 하는지에 있습니다.

이번 회차는 동일한 운영 시나리오를 그대로 따릅니다. GX10의 내장 네트워크 카드(`wlP9s9`)가 외부 인터넷을 담당하고, AWUS036ACM은 USB 외장으로 테스트 작업만 맡으며, 모니터나 AP로 전환해도 호스트 자체의 네트워크는 건드리지 않습니다. 전 과정에서 ALFA 카드에 해당하는 `wlx*` 인터페이스만 조작하고 내장 외부 네트워크 카드는 건드리지 않습니다.

| 항목 | 내용 |
|---|---|
| 모델 | AWUS036ACM |
| 칩 | MediaTek MT7612U(Wi-Fi 5 / 802.11ac, 2T2R 듀얼 스트림) |
| 드라이버 | `mt76x2u`(in-kernel, kernel 6.17 내장) |
| 세대 / 스트림 | Wi-Fi 5 / 2T2R |
| 비고 | morrownr 추천 Kali 카드 |
| 플랫폼 | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| 테스트 기기 | Apple iPhone 7 Plus(WPA3는 iPhone 15 Pro로 추가 측정) |
| 테스트 환경 | 자체 사무실 Wi-Fi, SSID `YUPITEK`, 2.4G ch5 / 5G ch36, ch157 |

> 이번 회차 종합표에는 AWUS036ACM의 USB ID와 펌웨어 버전 항목이 기록되지 않았으므로("—"로 표시) 본 글에서는 이 두 값을 추측하지 않으며, 아래의 모든 능력 데이터는 종합표 ACM 각 행을 기준으로 합니다.

---

## 2. 하드웨어와 드라이버(무설치)

이 카드는 GX10에서 꽂으면 바로 인식되며, 컴파일도 DKMS도 필요 없습니다. MT7612U는 mainline kernel에 내장된 `mt76x2u` 드라이버가 직접 담당하므로 어떤 out-of-tree 프로젝트도 추가로 올릴 필요가 없고 펌웨어 blob을 수동으로 설치할 필요도 없습니다. ARM64 입장에서 이것이 mt76의 가장 실질적인 장점입니다. 많은 서드파티 Realtek 드라이버는 aarch64에 prebuilt가 없어 커널 버전에 맞춰 직접 컴파일해야 하지만, mt76은 in-kernel 방식이므로 커널을 업그레이드해도 드라이버 의존성에 발목 잡히지 않습니다.

카드를 꽂으면 인터페이스는 `wlx` + MAC 형식으로 명명되며(예: `wlxXXXXXXXXXXXX`), 이름이 MAC에 묶여 있어 다시 꽂아도 변하지 않으므로 스크립트에 고정 지정하기 유리합니다. 드라이버 바인딩과 인터페이스 생성 확인은 아래의 범용 점검으로 할 수 있습니다(기기마다 인터페이스 이름과 phy 번호는 다릅니다):

```bash
# ALFA 카드의 인터페이스 이름 찾기(wlx로 시작하는 것만 선택, 내장 wlP9s9은 건드리지 않음)
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"

# 바인딩된 드라이버가 mt76x2u인지 확인
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# mt76x2u

# 해당 phy가 선언한 지원 인터페이스 모드 나열(이후 어떤 능력을 쓸 수 있는지 결정)
iw phy "$(cat /sys/class/net/$IF/phy80211/name)" info | sed -n '/Supported interface modes/,/Band 1/p'
```

이번 회차 실측에 따르면, `mt76x2u`가 사용할 수 있는 인터페이스 모드는 Realtek `rtw88`보다 완성도가 높습니다. managed / AP / monitor 외에도 IBSS와 mesh point를 단일 기기에서 생성할 수 있습니다(4절 참조). 이것이 ACM이 뒤에서 단일 기기 mesh / IBSS를 구동할 수 있는 바탕입니다. 동일 플랫폼의 Realtek 카드(예: AWUS036ACH)는 단일 기기에서 IBSS는 생성할 수 있지만 802.11s mesh와 active monitor는 이 플랫폼에서 구동되지 않습니다.

---

## 3. 실측 능력: Monitor / Injection / AP / WPA3

먼저 핵심 능력 종합표(아홉 장 종합표 1행 발췌)를 본 뒤 항목별로 전개합니다. 모든 항목은 자체 `YUPITEK` AP + 자체 iPhone 7 Plus에서 완료했습니다.

| 능력 | 2.4 GHz | 5 GHz | 설명 |
|---|---|---|---|
| Monitor(모니터 수신) | ✅ | ✅ | 두 밴드 모두 monitor 진입 및 정상 캡처 가능 |
| Injection(패킷 인젝션) | ✅ 63–83% | ✅ 76% | 표준 injection test의 인젝션 성공률 |
| AP 핫스팟(hostapd) | ✅ | ✅ 80MHz | 5G는 VHT 80 MHz까지 열 수 있음 |
| WPA3-SAE(AP 측) | ✅ | 미실측 | WPA3-SAE는 2.4 GHz에서만 실측했으며 5 GHz는 실측하지 않았습니다 |

### 3-1. Monitor(2.4 GHz + 5 GHz) ✅

2.4 GHz와 5 GHz 모두 정상적으로 monitor에 진입하여 패킷을 캡처할 수 있으며, 이 카드에서 가장 논란의 여지가 없는 능력입니다. 2T2R 듀얼 안테나 카드로서 두 밴드의 모니터 수신이 안정적이어서 현장 채널 점검과 패킷 진단을 뒷받침하기에 충분합니다.

### 3-2. Injection(패킷 인젝션) ✅(중간 수준)

표준 injection test로 패킷 인젝션 신뢰도를 측정하면, AWUS036ACM은 2.4 GHz에서 63–83%, 5 GHz에서 76%입니다. 아홉 장 안에서는 중간 수준으로, Realtek RTL8812AU(AWUS036ACH, 두 밴드 100%)와 RTL8821CU(AWUS036EACS, 두 밴드 100%)보다는 분명히 떨어지지만, 기능은 완전하고 실무상 충분합니다. ACM은 인젝션이 가능하되 안정성이 반에서 최고는 아닙니다. 고객이 "인젝션 성공률이 최고여야 한다"를 1순위로 둔다면 첫 번째 선택지가 아닙니다(5절 제품 선정 참조).

5 GHz 인젝션 전에는 설정 세부 사항 하나를 유의해야 합니다. 기본 규제 도메인은 일부 UNII 밴드의 능동 송신을 잠그므로, 테스트 전에 regulatory domain을 송신 허용 설정으로 바꾸고 측정 후 다시 현지 도메인으로 되돌려야 합니다(`iw reg set US` → 테스트 → `iw reg set TW`). 이는 5 GHz가 정상적으로 송신할 수 있는지의 전제이며, 카드 자체의 능력과는 무관합니다.

### 3-3. AP 핫스팟과 WPA3-SAE ✅

AWUS036ACM은 AP로 동작할 수 있으며, 2.4 GHz와 5 GHz 모두 가능하고 5 GHz는 80 MHz 대역폭(VHT80)까지 열 수 있습니다. AP 측에서 2.4 GHz로 WPA3-SAE를 활성화하면 자체 테스트용 스마트폰이 정상적으로 연결됩니다(5 GHz WPA3는 실측하지 않았습니다).

여기서 같은 mt76 계열의 단일 안테나 모델 AWUS036ACHM과 대조할 만합니다. ACHM의 WPA3는 hostapd의 `sae_pwe`를 반드시 0으로 설정해야 하며, 그렇지 않으면 iPhone 7 Plus가 연결되지 않습니다. AWUS036ACM은 이번 회차에서 이 제약을 겪지 않았고 WPA3-SAE를 바로 사용할 수 있었습니다.

---

## 4. 고급 능력: VIF / mesh / IBSS 단일 기기와 한계

더 깊은 층위로 handshake, 가상 인터페이스(VIF), active monitor, mesh / IBSS를 봅니다. 이 절은 AWUS036ACM이 Realtek 카드와 격차를 벌리는 지점이기도 합니다.

| 고급 항목 | ACM 결과 | 설명 |
|---|---|---|
| WPA handshake 캡처 | ✅ 엔드투엔드(.22000) | 자체 iPhone 7 Plus에 deauth, 완전한 4-way M1–M4 캡처, hashcat `.22000` 추출 |
| VIF(다중 인터페이스 동시 운용) | ✅ STA+AP / AP+mon | STA+AP 또는 AP+monitor 동시 가능 |
| Active monitor | 🟡 설정 가능, ACK 미검증 | 모드는 생성 가능하나 ACK 응답 동작은 미검증 |
| Ad-hoc(IBSS) | 🟡 단일 기기 | 단일 기기에서 인터페이스 생성 가능, 상호 연결에는 두 번째 기기 필요 |
| Mesh(802.11s) | 🟡 단일 기기 | 단일 기기에서 인터페이스 생성 가능, 상호 연결에는 두 번째 기기 필요 |
| Wi-Fi Direct(P2P) | ⬜ 두 번째 기기 필요 | 이번 회차 미측정 |

### 4-1. VIF(가상 인터페이스 동시 운용) — ACM의 강점 ✅

이 카드는 두 개의 가상 인터페이스를 동시에 구동할 수 있습니다. 이번 회차 실측에서 STA+AP(한쪽은 상위망에 연결, 한쪽은 핫스팟 개설)와 AP+monitor(한쪽은 핫스팟 개설, 한쪽은 모니터링) 두 조합 모두 성립했으며, "연결하면서 관측"하거나 "단일 카드로 동시에 client와 기지국 역할"과 같은 시나리오에 적합합니다. 이는 `mt76` 드라이버의 다중 인터페이스 동시 운용이 비교적 완성도 높은 부분입니다.

### 4-2. mesh / IBSS "단일 기기 가능" — mt76의 핵심 차이 🟡

AWUS036ACM은 단일 기기에서 802.11s mesh와 ad-hoc(IBSS) 인터페이스를 생성할 수 있습니다. Realtek `rtw88` / `rtw89`(AWUS036ACH, AWUS036AX 등)는 단일 기기에서 IBSS는 생성할 수 있지만 이 플랫폼에서 802.11s mesh는 지원하지 않습니다. 따라서 802.11s mesh 실험을 하려면 mt76 카드(ACM / ACHM)가 Realtek 카드에는 없는 출발점을 갖습니다.

경계를 분명히 하자면, 이번 회차에서 확인한 것은 "단일 기기에서 인터페이스 생성 가능"이며, 완전한 다중 노드 상호 연결은 두 번째 카드 / 두 번째 노드가 더 필요하여 아직 진행하지 않았습니다. 그래서 여기는 ✅가 아니라 🟡(단일 기기)로 표시합니다.

### 4-3. 정직한 능력 경계

- **handshake**: ACM은 완전한 엔드투엔드 과정(자체 기기 deauth → 완전한 4-way M1–M4 캡처 → `hcxpcapngtool --all`로 hashcat `.22000` 추출)을 완료했습니다. 인젝션 성공률(2.4G 63–83% / 5G 76%)이 Realtek 카드보다 낮더라도 마찬가지입니다.
- **active monitor**: 모드는 설정할 수 있지만 ACK 응답 동작은 이번 회차에 미검증입니다(🟡 표기). 관련하여, 플랫폼 레벨의 `hcxdumptool` 8.x는 2.4 GHz의 AWUS036EACS를 제외한 모든 카드에서 `failed to arm`입니다(active-monitor를 요구하는데, 이 플랫폼의 트라이 밴드 내장 카드와 현행 드라이버는 이를 제공하지 않습니다). 그래서 ACM의 handshake 과정은 `airodump-ng` + `aireplay-ng`로 대체했습니다.
- **Wi-Fi Direct(P2P)**: 이번 회차 미측정이며, 두 번째 기기가 필요합니다.

### 4-4. 플랫폼 운용 주의(GX10 ARM64, ACM 관련)

1. **자신의 네트워크를 끊지 말 것**: `airmon-ng check kill`을 절대 실행하지 않습니다(NetworkManager를 꺼서 GX10이 인터넷에서 끊어집니다). `wlx*`만 조작하고 내장 외부 `wlP9s9`은 건드리지 않습니다.
2. **RX stall 해소**: monitor / AP를 반복 전환한 뒤 갑자기 아무것도 스캔되지 않으면, 카드를 **한 번 뽑았다 꽂으면** 복구됩니다(USB 재열거, 인터페이스 이름은 MAC으로 결정되어 변하지 않음).
3. **5 GHz TX 잠금 해제**: 5 GHz injection 전에 올바른 규제 도메인을 설정해 TX 출력을 잠금 해제하고, 측정 후 현지 도메인으로 되돌립니다.
4. **handshake 캡처 요령**: 사무실에는 동일 이름의 AP가 여러 대 있는 경우가 많아, 실무상 단일 `--bssid`로 고정하지 않고 채널 전체를 캡처하는 편이 더 안정적입니다. 변환은 `hcxpcapngtool --all`을 사용합니다.
5. **ARM64 툴체인**: `aircrack-ng`은 소스에서 직접 컴파일해야 하고, `wifite`는 git 3.0.0 버전을 사용합니다(apt 의존성 충돌 우회).

플랫폼 레벨의 Kali 도구(`airmon-ng`, `kismet`, `bettercap`, `wifite` git 버전, Wireshark / tshark)는 모두 ACM을 data source로 정상적으로 사용할 수 있습니다. 유일한 예외는 앞서 말한 active-monitor를 요구하는 `hcxdumptool`입니다.

---

## 5. 적용 시나리오와 제품 선정(Hub로 돌아가기)

위의 능력을 제품 포지셔닝에 대응시켜 보면, AWUS036ACM의 역할은 사실 매우 분명합니다. 능력이 균형 잡혀 있고 드라이버 설치가 필요 없으며, mt76의 mesh / IBSS / VIF 강점을 독자적으로 지닌 Wi-Fi 5 2T2R 카드입니다. 그렇다면 어떤 시나리오에 써야 할까요?

- **mesh(802.11s) 실험의 최우선 선택**: 이번 아홉 장 중 mt76의 ACM / ACHM만 단일 기기에서 802.11s mesh 인터페이스를 생성할 수 있습니다. Realtek `rtw88` / `rtw89`은 단일 기기 IBSS는 생성할 수 있지만 802.11s mesh는 지원하지 않습니다. mesh 실험을 하려면 ACM이 올바른 출발점입니다.
- **VIF 동시 운용이 필요한 경우**: STA+AP, AP+monitor 모두 성립하므로, 단일 카드로 동시에 client와 AP 역할을 하거나 연결하면서 모니터링하기에 적합합니다.
- **무드라이버 운용을 중시하는 경우**: in-kernel `mt76x2u`로 커널 업그레이드 시 드라이버에 발목 잡히지 않으며, ARM64에서 out-of-tree 모듈 컴파일의 번거로움을 덜어줍니다.
- **최적해가 아닌 시나리오**: 핵심 요구가 "최고 injection 성공률"이라면, ACM의 인젝션(2.4G 63–83% / 5G 76%)은 반에서 최고가 아니므로 Realtek의 AWUS036EACS / ACH / ACS로 바꾸기를 권장합니다. 최강 수신 / 장거리 monitor를 추구한다면 AWUS036AXER / ACH를 보십시오.

같은 제품군과 비교하면 포지셔닝 차이는 다음과 같습니다.

| 요구 | 권장 카드 | 이유 |
|---|---|---|
| mesh(802.11s) 단일 기기 실험 | **AWUS036ACM** / AWUS036ACHM | `mt76` 드라이버로 단일 기기 802.11s mesh 생성 가능(Realtek은 단일 기기 IBSS만, mesh 미지원) |
| VIF 동시 운용(STA+AP / AP+mon) | **AWUS036ACM** | 다중 인터페이스 동시 운용 성립 |
| 듀얼 밴드 인젝션 모두 100% / 엔드투엔드 handshake | AWUS036EACS, AWUS036ACH, AWUS036ACS | 두 밴드 인젝션 최고, `.22000` 엔드투엔드 입증 완료 |
| 최강 수신 / 장거리 monitor | AWUS036AXER, AWUS036ACH | 채널 호핑으로 더 많은 대상 포착 / 듀얼 안테나 고이득 |

한마디로 제품 선정: mesh / IBSS를 다루고 VIF 동시 운용이 필요하며 무드라이버 운용을 원한다면, AWUS036ACM이 이번 제품군에서 가장 잘 맞는 mt76 카드입니다. 듀얼 밴드 인젝션 모두 100%가 필요하다면 EACS / ACH로 가십시오. 아홉 장 전체의 가로 비교와 제품 선정 결정은 [ALFA 무선 네트워크 카드 종합 평가 Hub(아홉 장 종합표)](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)를 참고하세요.

---

## 자주 묻는 질문(FAQ)

**Q: AWUS036ACM은 Ubuntu나 Kali에서 드라이버를 설치해야 하나요?**
필요 없습니다. MT7612U는 커널에 내장된 mt76x2u 드라이버가 담당하므로 Ubuntu 24.04(kernel 6.17)에서 꽂으면 바로 인식되며, DKMS도 수동 펌웨어 설치도 필요 없습니다. 이번 실측 플랫폼은 Ubuntu 24.04 ARM64이며, Kali도 커널이 충분히 최신이면 원칙적으로 동일하지만 이번에는 Kali 실기에서 검증하지 않았습니다.

**Q: AWUS036ACM은 monitor mode에 들어가고 패킷 인젝션을 할 수 있나요? 성공률은 얼마인가요?**
가능합니다. 2.4GHz와 5GHz 모두 monitor mode에 들어가 정상적으로 캡처할 수 있으며, aireplay-ng 인젝션 테스트는 2.4GHz에서 63–83%, 5GHz에서 76%로 아홉 장의 카드 중 중간 수준입니다. 듀얼 밴드 인젝션을 모두 100%로 원한다면 Yopitek 실측 기준 AWUS036ACH, AWUS036EACS가 더 낫습니다.

**Q: AWUS036ACM은 핫스팟을 열면서 동시에 인터넷에 접속할 수 있나요(VIF)?**
가능합니다. 실측에서 STA+AP(한쪽은 상위망에 연결, 한쪽은 핫스팟 개설)와 AP+monitor(핫스팟을 열면서 동시에 모니터링) 두 조합 모두 성립했으며, 이는 mt76 드라이버의 다중 인터페이스 동시 운용이 비교적 완성도 높은 부분입니다. 5GHz 핫스팟은 VHT 80 MHz까지 열 수 있습니다.

**Q: AWUS036ACM은 mesh(802.11s)와 IBSS를 지원하나요?**
단일 기기에서 생성 가능합니다. Ubuntu 24.04 / kernel 6.17에서 AWUS036ACM은 802.11s mesh와 IBSS(Ad-hoc) 인터페이스를 생성할 수 있지만, 이번에는 두 번째 노드가 없어 다중 노드 상호 연결은 아직 검증하지 못했으므로 단일 기기에서 생성 가능하다고만 말할 수 있습니다.

**Q: AWUS036ACM은 WPA handshake를 캡처할 수 있나요?**
네. 자체 AP와 자체 iPhone 7 Plus를 대상으로 엔드투엔드가 성공했습니다. deauth, 완전한 4-way(M1–M4) 캡처, hcxpcapngtool --all로 hashcat .22000 추출까지 완료했습니다. 본인 소유 또는 허가된 네트워크에서만 진행합니다.

---

## 6. 더 읽어보기

- 아홉 장 ALFA 카드의 완전한 능력 비교와 제품 선정 종합 평가 → [ALFA 무선 네트워크 카드 종합 평가 Hub(아홉 장 종합표)](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 드라이버 설치 불필요: Ubuntu 24.04 + kernel 6.17에서 Monitor / AP 활성화(rtw88 / rtw89 / mt76 실측)(준비 중, 링크 작업 중)
- WPA3-SAE와 엔드투엔드 handshake 캡처 단계별 튜토리얼(준비 중, 링크 작업 중)
- 같은 mt76의 단일 안테나 모델 → AWUS036ACHM 카드별 실측 테스트(준비 중, 링크 작업 중)

---

*테스트 기관: Yopitek(ALFA Network 대만 유통사) — https://www.yupitek.com | 테스트 환경: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | 테스트 기기: Apple iPhone 7 Plus(WPA3는 iPhone 15 Pro로 추가 측정)*
