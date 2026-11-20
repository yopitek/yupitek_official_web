---
title: "ALFA AWUS036EACS 단일 카드 실측: RTL8821CU(BT + WiFi 복합)의 ASUS GX10(ARM64 / Ubuntu 24.04) 모니터 · 인젝션 · AP · 엔드투엔드 핸드셰이크"
slug: awus036eacs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036eacs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036eacs
  - rtl8821cu
  - rtw88-8821cu
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036EACS(블루투스+Wi-Fi 복합)를 Ubuntu 24.04 ARM64에서 실측: 드라이버 설치 불필요, 양쪽 대역 인젝션 100%, 모니터, AP, WPA3-SAE, 엔드투엔드 핸드셰이크(79 ACKs, .22000) 통과. USB 재삽입 리스크 포함. 플랫폼은 ASUS GX10, RTL8821CU."
faq:
  - question: "AWUS036EACS는 Ubuntu 24.04 ARM64에서 드라이버를 설치해야 하나요?"
    answer: "본문에서 테스트한 kernel 6.17(ASUS GX10)에서는 필요 없습니다. RTL8821CU는 내장 rtw88_8821cu 드라이버로 구동되어 꽂으면 바로 인식하며, 컴파일도 DKMS도 필요 없습니다. 인터페이스 이름은 wlx에 MAC을 붙인 형태이며 재삽입해도 바뀌지 않습니다."
  - question: "AWUS036EACS의 모니터 모드와 패킷 인젝션 성능은 어떤가요?"
    answer: "모니터는 2.4G, 5G 모두 안정적이며 대부분의 채널에서 300 frames를 가득 수신합니다. aireplay-ng --test는 양쪽 대역 모두 30/30(100%)입니다. 5G 인젝션 전에는 iw reg set US로 TW의 TX 제한을 해제해야 합니다."
  - question: "AWUS036EACS로 WPA 핸드셰이크를 캡처할 수 있나요?"
    answer: "가능합니다. 본인 소유 AP와 본인 소유 iPhone 7 Plus에서 엔드투엔드로 실측: deauth로 79 ACKs를 받고 완전한 M1–M4를 캡처했으며, hcxpcapngtool --all로 .22000(784 bytes, EAPOL pairs 2조)을 변환했습니다. 본인 소유 또는 허가된 네트워크에서만 가능합니다."
  - question: "AWUS036EACS를 꽂으면 lsusb에는 보이는데 wlx 네트워크 인터페이스가 없으면 어떻게 하나요?"
    answer: "이것은 BT+Wi-Fi 복합 장치의 probe 경쟁 상태입니다. 블루투스는 이미 btusb에 바인딩되었는데 Wi-Fi의 rtw88_8821cu가 멈춘 것입니다. 실측상 모듈 재로드나 수동 bind는 대부분 효과가 없으며, 확실한 해법은 카드를 뽑아 다른 USB 포트에 다시 꽂는 것입니다."
  - question: "AWUS036EACS는 메시, IBSS 또는 hcxdumptool을 지원하나요?"
    answer: "지원하지 않습니다. rtw88의 액티브 모니터, IBSS, 메시, P2P는 -95를 반환하거나 join이 무효이며, hcxdumptool 8.x는 2.4 GHz에서만 arm되고(5 GHz는 failed to arm)  airodump-ng + aireplay-ng를 사용하세요. VHT는 80 MHz만 지원합니다. 메시 / IBSS가 필요하면 AWUS036ACM / ACHM을 선택하세요."
draft: false
---

> 테스트 기관: Yopitek(ALFA Network 대만 총판) | 테스트 플랫폼: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | 테스트 장치: 본인 소유 iPhone 7 Plus(WPA3은 iPhone 15 Pro로 별도 테스트) | 테스트 대상: 본인 소유 사무실 Wi-Fi(SSID YUPITEK, 2.4G ch5 / 5G ch36, 157).
>
> 본문은 AWUS036EACS 단일 카드의 성능 및 호환성 실측입니다. 모든 모니터 / 인젝션 / 핸드셰이크 캡처는 Yopitek 본인 소유 장비, 본인 소유 사무실 Wi-Fi에서 본인 소유 테스트 휴대폰을 대상으로 진행했으며, 유통사가 하드웨어에 대해 수행하는 정당한 성능 검증에 속합니다. 어떠한 제3자 네트워크도 대상으로 하지 않으며, 공격 조작 절차도 제공하지 않습니다.

**핵심 요약(TL;DR)**: AWUS036EACS는 GX10 / Ubuntu 24.04(kernel 6.17)에서 드라이버 설치 불필요이며, 양쪽 대역 인젝션 100%, 엔드투엔드 .22000 통과(79 ACKs)입니다. BT+Wi-Fi 복합 카드이므로 재삽입에 유의해야 합니다.

## 1. 이 카드와 테스트 플랫폼

AWUS036EACS는 ALFA의 경량 휴대용 Wi-Fi 5(802.11ac) USB 네트워크 카드로, 칩은 Realtek RTL8821CU이며 1x1 단일 스트림, 2.4GHz와 5GHz 듀얼 밴드에 블루투스까지 내장해 BT + WiFi 복합 장치에 속합니다. 이 글은 이 카드를 단독으로 Yopitek의 실험 테이블에 올려, ASUS GX10(ARM64)에 Ubuntu 24.04를 조합한 환경에서 항목별로 검수하며, 고객이 가장 중시하는 몇 가지 질문에 답합니다. 드라이버가 ARM64에서 인식되는지, 어떤 모드에 진입할 수 있는지, 성능은 어디까지인지.

먼저 포지셔닝을 분명히 하겠습니다. 이것은 유통사가 자사 제품에 대해 수행하는 호환성 및 성능 경계 검증이지 공격 교육이 아닙니다. 글 속의 모든 인젝션 및 핸드셰이크 관련 성능 측정은 일률적으로 본인 소유 폐쇄 환경에서 본인 소유 장치를 대상으로 진행했으며, 외부 네트워크에 대한 어떠한 조작 절차도 제공하지 않습니다.

테스트 플랫폼과 방법은 본 배치의 다른 단일 카드 글과 동일합니다.

- 연산 플랫폼: ASUS GX10(ARM64 / aarch64)
- 운영체제: Ubuntu 24.04 LTS, kernel 6.17.0-1014-nvidia
- 드라이버 전략: kernel 내장(in-kernel) 드라이버 사용, 꽂으면 바로 인식, 제3자 DKMS 모듈은 설치하지 않음
- 테스트 장치: Apple iPhone 7 Plus(WPA3-SAE는 iPhone 15 Pro로 재테스트)
- 테스트 환경: 본인 소유 사무실 Wi-Fi, SSID YUPITEK, 2.4GHz ch5 / 5GHz ch36, ch157
- 안전 수칙: 전 과정에서 `wlx*` 인터페이스만 조작하고 내장 외부 연결 메인 라인은 건드리지 않음. `airmon-ng check kill`은 절대 실행하지 않음(NetworkManager를 꺼 GX10의 외부 연결이 끊김)

## 2. 하드웨어와 드라이버: BT + WiFi 복합 장치의 실체

먼저 내막을 봅니다. 아래 표는 AWUS036EACS가 kernel 6.17에서 실제로 로드된 상태입니다.

| 항목 | 내용 |
|---|---|
| 칩 | Realtek RTL8821CU(1x1 단일 스트림) |
| 세대 | Wi-Fi 5(802.11ac), 2.4 + 5GHz |
| 복합 기능 | BT + WiFi 복합 장치(블루투스 내장) |
| USB ID | `0bda:c820` |
| 드라이버 | `rtw88_8821cu`(in-kernel, kernel 6.2부터 USB 지원) |
| 펌웨어 | 24.11.0(H2C version 12, dmesg 실측) |
| VHT 대역폭 | 80MHz만(160 / 80+80 없음) |

`iw phy`로 조회하면 지원 인터페이스 모드는 `managed` / `AP` / `AP/VLAN` / `monitor`입니다(`IBSS`는 나열되지만 실측상 join 무효). 주파수 대역은 2.4GHz ch1–13과 5GHz ch36–165를 포함하며(그중 ch52–144는 DFS 대역), cipher는 CCMP-256, GCMP-128 / GCMP-256, CMAC를 포함해 AP 측에서 WPA3을 구동할 조건을 갖추고 있습니다.

드라이버 쪽은 의문의 여지가 없습니다. RTL8821CU의 USB 지원은 kernel 6.2부터 mainline `rtw88`에 병합되었고, GX10의 kernel 6.17에는 이미 `rtw88_8821cu`가 내장되어 꽂으면 바로 로드되며 컴파일이나 DKMS가 필요 없습니다. 초기 in-kernel 버전의 AP mode에는 bug가 있었으나 macid patch(linux-next-20240911부터)로 수정되었고, 이번 kernel 6.17에서의 AP 세 가지 모드 실측은 모두 정상적으로 마무리되었습니다. 확인 방법은 다음과 같습니다.

```bash
lsusb | grep -i '0bda:c820'
# ID 0bda:c820 Realtek Semiconductor Corp. 802.11ac NIC
sudo dmesg | grep -i 8821cu
# rtw88_8821cu ...: Firmware version 24.11.0, H2C version 12 -> renamed from wlan0
```

Wi-Fi 인터페이스는 로드된 뒤 `wlan0`이 아니라 `wlx` + MAC으로 명명됩니다(예: `wlx00c0cab3a52e`). 재삽입해도 이름이 바뀌지 않으므로 스크립트를 작성할 때 안정적으로 참조할 수 있습니다.

정말 유의해야 할 것은 "복합 장치"라는 점입니다. `lsusb -t`로 보면 동일한 RTL8821CU 아래에 여러 USB interface가 걸려 있는 것을 볼 수 있습니다. 블루투스 기능은 `btusb`에, Wi-Fi 기능은 별도로 `rtw88_8821cu`에 바인딩됩니다.

```
/:  Bus 0X.Port X: Dev X, Class=root_hub, Driver=xhci-hcd
    |__ Port X: Dev X, If 0, Class=Wireless, Driver=btusb               <- 블루투스
    |__ Port X: Dev X, If 1, Class=Wireless, Driver=btusb               <- 블루투스
    |__ Port X: Dev X, If 2, Class=Vendor Specific, Driver=rtw88_8821cu <- Wi-Fi
```

(Bus / Port 번호는 삽입 횟수에 따라 바뀝니다. 핵심은 interface 0/1이 `btusb`를 쓰고 interface 2가 Wi-Fi의 `rtw88_8821cu`라는 점입니다.)

**BT + WiFi 복합 장치의 재삽입 리스크(배포 전 필독).** 블루투스와 Wi-Fi가 동일한 USB 장치를 공유하기 때문에, 일부 USB 포트나 빠른 재삽입 상황에서는 블루투스는 이미 `btusb`에 바인딩되었지만 Wi-Fi 쪽 interface의 probe가 멈춰, 결국 `lsusb`에는 `0bda:c820`이 보이는데 `wlx` 인터페이스가 생성되지 않는 경쟁 상태가 발생할 수 있습니다. 실측에서 `modprobe -r` 후 재로드하거나 수동 `bind`를 하는 것은 대부분 효과가 없었습니다(`bind`는 `Operation already in progress`를 반환). 확실한 해법은 하나뿐입니다. 카드를 뽑아 다른 USB 포트에 다시 꽂으면 열거가 깔끔해지고 `wlx` 인터페이스가 정상적으로 나타납니다. 이는 비복합인 AWUS036ACS(RTL8811AU)에 비해 이 카드가 추가로 알아두어야 할 조작 세부 사항이며, 미리 알면 카드 고장으로 오판하지 않습니다.

## 3. 실측 성능: 모니터 / 인젝션 / AP / WPA3

아래 표는 AWUS036EACS의 핵심 성능 실측 요약으로, 각 항목은 2026-11-18에 GX10 실기에서 실행했습니다.

| 성능 항목 | 2.4GHz | 5GHz | 실측 요점 |
|---|---|---|---|
| 모니터 | ✅ 강함 | ✅ 강함 | 대부분 채널에서 300 frames 가득 수신; 커뮤니티 #453 "ch1 멈춤" 재현 안 됨 |
| 인젝션 | ✅ 100%(30/30) | ✅ 100%(30/30) | Power 2.4G -38.27 / 5G -76.10; 본 배치 ac 카드 중 인젝션 최강 |
| AP 핫스팟 | ✅ 깔끔한 마무리 | ✅ VHT 80MHz | `hostapd`로 구축, iPhone 7 Plus 접속 후 4-way 완료 |
| WPA3-SAE(AP 측) | ✅ iPhone 접속 | 미실측 | SAE-only + PMF 강제(`ieee80211w=2`, `sae_pwe=0`) |
| WPA 핸드셰이크 캡처 | — | ✅ 엔드투엔드 | M1–M4 완전, deauth 79 ACKs 수신, `.22000` 변환 |

모니터(모니터 모드)는 2.4와 5GHz 모두 안정적입니다. 6개 채널을 하나씩 캡처했고 대부분 300 frames를 가득 수신했습니다. 8821cu에게는 여기서 매우 중요한 긍정적 결과가 하나 더 있습니다. rtw88 커뮤니티가 오래 추적해 온 GitHub #453 "8821cu가 kernel ≥6.9, STA up 상태에서 모니터가 ch1에 멈춤"이 GX10 환경에서는 재현되지 않았으며, 5GHz의 ch36, ch149, ch157 모두 300 프레임을 안정적으로 가득 수신했습니다. 2.4 / 5GHz를 넘나들며 스펙트럼 조사나 패킷 분석을 하려면 이 카드의 모니터는 안심하고 사용할 수 있습니다.

인젝션(패킷 인젝션)의 성능이 가장 돋보입니다. `aireplay-ng --test`로 측정하면 2.4GHz와 5GHz 모두 30/30, 100%로, 본 배치 ac 카드 중 인젝션이 가장 강한 카드입니다(같은 1x1인 AWUS036ACS는 5G에서 96%에 불과). 여기에는 대만 현지 특유의 세부 사항이 있습니다. 5GHz의 TX는 regulatory domain이 TW로 설정되면 잠기므로, 측정 전에 먼저 `iw reg set US`로 잠금을 해제하고 측정 후 `iw reg set TW`로 되돌립니다.

AP 핫스팟 쪽은 `hostapd`로 각각 2.4GHz(WPA2), 5GHz(VHT 80MHz), WPA3-SAE 세 가지를 구축했고, iPhone 7 Plus가 모두 접속해 4-way 핸드셰이크를 완료했으며, 접속 종료도 깔끔하게 마무리되었습니다(`AP-DISABLED` / `TERMINATING`). 일부 카드에서 나타나는 beacon re-key 문제가 발생하지 않아, 2.4G에서는 이 점이 자매 카드 ACS보다 안정적입니다. WPA3은 SAE-only에 PMF 강제(`ieee80211w=2`, `sae_pwe=0`)를 조합했고, iPhone 15 Pro로 성공적으로 접속해 RTL8821CU가 AP 측에서 WPA3-SAE를 사용할 수 있음을 확인했습니다.

Kali 도구 체인(플랫폼 계층)도 이 카드에서 모두 구동됩니다. `airmon-ng`는 EACS(`rtw88_8821cu`)를 감지하지만 마찬가지로 `check kill`을 쓰지 마세요. `kismet`은 이 카드를 data source로 하여 성공적으로 시작했고, 실측상 약 733 KB의 `.kismet` log를 생성했습니다. `bettercap` 2.32의 `wifi.recon on`은 정상 작동합니다(txpower 경고는 무시 가능). `wifite`(git 3.0.0)는 자사 YUPITEK(ch5, PWR 84)을 포함해 10대 이상의 AP를 스캔했는데, 이 버전에는 `--band` 플래그가 없어 `-c 1,6,11,36,149,157`로 채널을 지정해야 합니다. `Wireshark` / `tshark` 4.x는 monitor ch6에서 실제로 325 frames를 캡처해 분석했으며, `macchanger`의 랜덤 MAC 위장도 사용할 수 있습니다. 도구 계층 이 부분은 본 배치의 다른 카드와 일치하며, 차이는 주로 앞의 인젝션과 모니터 하드웨어 성능에 있습니다.

## 4. 엔드투엔드 핸드셰이크: 강점과 정직한 제한

이 카드의 강점은 인젝션과 캡처를 완전히 사용 가능한 하나의 체인으로 잇는 것입니다. 자사 YUPITEK AP와 본인 소유 iPhone 7 Plus 사이에서 전체 체인을 실기로 통과시켰습니다. 본인 소유 iPhone에 deauth 전송(인젝션, 실측상 79개의 ACKs를 받아 인젝션 패킷이 실제로 client에 도달했음을 확인) → iPhone이 재접속할 때 완전한 4-way 핸드셰이크 수신(M1, M2, M3, M4 각 1) → `hcxpcapngtool --all`로 hashcat 형식 `.22000` 변환(784 bytes, EAPOL pairs 2조, RC checked). 전체 흐름은 오로지 카드 성능 검증을 위한 것으로, 대상은 전 과정에서 자사 AP와 본인 소유 휴대폰이며 어떠한 제3자 네트워크도 포함하지 않습니다.

실무상 두 가지 핵심 세부 사항을 기록해 둘 만합니다. 사무실에 동명 YUPITEK AP가 여러 대 ch36에 있을 때, 캡처 시 `--bssid`로 잠그지 말고 채널 전체를 받아야 iPhone이 실제로 연결한 대를 걸러내지 않습니다. 또한 `hcxpcapngtool`는 기본적으로 엄격해 `--all`을 추가해야 `.22000`을 변환할 수 있습니다.

정직한 제한도 한 번에 분명히 밝힙니다.

- **액티브 모니터 / IBSS(Ad-hoc) / 메시(802.11s) / Wi-Fi Direct(P2P)를 지원하지 않습니다.** 이 모드들은 `rtw88`에서 `-95`(Operation not supported)를 반환하거나 나열은 되지만 join이 무효이며, 드라이버 계층 제한으로 해결책이 없습니다. 메시 / IBSS 실험이 필요한 고객은 MediaTek의 AWUS036ACM / ACHM으로 바꿔야 합니다.
- **`hcxdumptool` 8.x는 제한적입니다.** 액티브 모니터를 필요로 하며, 이 카드에서는 2.4 GHz에서만 arm되고 5 GHz에서는 `failed to arm`이 발생합니다(본 배치의 다른 카드는 모두 `failed to arm interface`). `airodump-ng` + `aireplay-ng`로 바꾸면 되며, 이 카드는 인젝션이 100%라 영향을 받지 않습니다.
- **VHT는 80MHz만 지원합니다.** 단일 스트림, 160MHz나 80+80 없음으로, 포지셔닝 자체가 경량 휴대용 카드이지 처리량을 겨루는 역할이 아닙니다.
- **VIF는 부분 지원입니다.** 같은 채널에서 managed 인터페이스와 함께 동작하는 passive monitor 인터페이스(소프트웨어 monitor)만 가능하며(실측 100 frames), 독립적인 이중 VIF는 지원하지 않습니다.

## 5. 적용 시나리오와 제품 선정

실측을 종합하면 AWUS036EACS의 포지셔닝은 명확합니다. 듀얼 밴드 모니터 + 인젝션 + 엔드투엔드 핸드셰이크 검증이 필요하면서 가볍고 블루투스를 내장한 휴대용 카드를 원한다면, 이것이 적합한 해답입니다. 양쪽 대역 인젝션 100%와 깔끔한 AP / WPA3 성능 덕분에, 허가 범위 내의 무선 감사 및 보안 교육 용도에서 AWUS036ACH, AWUS036ACS와 함께 최우선 후보군에 듭니다.

어떤 경우에 다른 카드를 권하는가:

- **현장에서 재삽입이 잦거나, 섀시 USB 포트 품질이 들쭉날쭉** → 복합 장치의 probe 경쟁 상태가 번거로움을 늘리므로, 비복합인 AWUS036ACS(RTL8811AU, 동일한 1x1 ac에 블루투스 변수가 없음)를 고려할 수 있습니다.
- **메시 / IBSS 실험을 해야 함** → `rtw88`은 미지원이니 MediaTek의 AWUS036ACM / ACHM으로 바꾸세요.
- **최강 수신이나 장거리 모니터를 추구** → 듀얼 안테나의 AWUS036ACH나 Wi-Fi 6의 AWUS036AXER가 더 적합합니다.
- **피해야 할 선택**: 용도가 인젝션 / 핸드셰이크라면 MT7921의 AWUS036AXM / AXML을 고르지 마세요. 인젝션이 본 플랫폼에서 바로 실패합니다.

9종 ALFA 카드의 모니터 / 인젝션 / AP / WPA3 횡단 비교와 완전한 제품 선정 매트릭스를 한 번에 보려면 종합표로 돌아가세요: [2026 최완성 실측: 9종 ALFA 무선 네트워크 카드의 ASUS GX10 전체 매트릭스](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 자주 묻는 질문(FAQ)

**Q: AWUS036EACS는 Ubuntu 24.04 ARM64에서 드라이버를 설치해야 하나요?**
본문에서 테스트한 kernel 6.17(ASUS GX10)에서는 필요 없습니다. RTL8821CU는 내장 rtw88_8821cu 드라이버로 구동되어 꽂으면 바로 인식하며, 컴파일도 DKMS도 필요 없습니다. 인터페이스 이름은 wlx에 MAC을 붙인 형태이며 재삽입해도 바뀌지 않습니다.

**Q: AWUS036EACS의 모니터 모드와 패킷 인젝션 성능은 어떤가요?**
모니터는 2.4G, 5G 모두 안정적이며 대부분의 채널에서 300 frames를 가득 수신합니다. `aireplay-ng --test`는 양쪽 대역 모두 30/30(100%)입니다. 5G 인젝션 전에는 `iw reg set US`로 TW의 TX 제한을 해제해야 합니다.

**Q: AWUS036EACS로 WPA 핸드셰이크를 캡처할 수 있나요?**
가능합니다. 본인 소유 AP와 본인 소유 iPhone 7 Plus에서 엔드투엔드로 실측: deauth로 79 ACKs를 받고 완전한 M1–M4를 캡처했으며, `hcxpcapngtool --all`로 .22000(784 bytes, EAPOL pairs 2조)을 변환했습니다. 본인 소유 또는 허가된 네트워크에서만 가능합니다.

**Q: AWUS036EACS를 꽂으면 lsusb에는 보이는데 wlx 네트워크 인터페이스가 없으면 어떻게 하나요?**
이것은 BT+Wi-Fi 복합 장치의 probe 경쟁 상태입니다. 블루투스는 이미 btusb에 바인딩되었는데 Wi-Fi의 rtw88_8821cu가 멈춘 것입니다. 실측상 모듈 재로드나 수동 bind는 대부분 효과가 없으며, 확실한 해법은 카드를 뽑아 다른 USB 포트에 다시 꽂는 것입니다.

**Q: AWUS036EACS는 메시, IBSS 또는 hcxdumptool을 지원하나요?**
지원하지 않습니다. rtw88의 액티브 모니터, IBSS, 메시, P2P는 -95를 반환하거나 join이 무효이며, hcxdumptool 8.x는 2.4 GHz에서만 arm되고(5 GHz는 failed to arm)  airodump-ng + aireplay-ng를 사용하세요. VHT는 80 MHz만 지원합니다. 메시 / IBSS가 필요하면 AWUS036ACM / ACHM을 선택하세요.

---

## 6. 더 읽어보기

- [2026 최완성 실측: 9종 ALFA 무선 네트워크 카드의 ASUS GX10(ARM64 / Ubuntu 24.04) 모니터 · 인젝션 · AP 전체 매트릭스](/ko/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)(Hub 종합표)
- [WPA3-SAE 시대의 무선 감사: 9종 ALFA 카드 핸드셰이크 캡처 성능 실측](/ko/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- [드라이버 설치 불필요: Ubuntu 24.04 + kernel 6.17에서 in-kernel 드라이버로 ALFA 카드 모니터와 AP 모드 활성화](/ko/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 같은 rtw88 USB ac 카드 → [AWUS036ACS 단일 카드 실측 보고서(RTL8811AU)](/ko/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*테스트 기관: Yopitek(ALFA Network 대만 총판) — https://www.yupitek.com*
