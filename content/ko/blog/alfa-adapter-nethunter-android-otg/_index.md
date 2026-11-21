---
title: "USB OTG를 통해 Kali NetHunter에서 ALFA WiFi 어댑터 사용하기"
description: "USB OTG를 통해 Android에서 Kali NetHunter와 ALFA USB WiFi 어댑터를 사용하는 방법. AWUS036ACH 드라이버, 모니터 모드 명령, OTG 케이블 요구사항, 지원 기기를 다룹니다."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "ALFA 어댑터와 함께 사용하는 Kali NetHunter는 루트(root)가 필요합니까?"
    answer: "네. 전체 NetHunter 빌드는 RTL8812AU 모듈을 로드하고 USB OTG 어댑터 지원을 활성화하기 위해 커스텀 커널이 적용된 루팅된 Android 기기가 필요합니다."
  - question: "NetHunter에 가장 적합한 ALFA 어댑터는 무엇입니까?"
    answer: "AWUS036ACH(RTL8812AU)가 최선의 선택입니다. NetHunter 커스텀 커널에는 88XXau 모듈이 포함되어 있어 모니터 모드와 패킷 인젝션을 완전히 지원합니다."
  - question: "전원 공급형 USB OTG 허브가 왜 필요합니까?"
    answer: "AWUS036ACH는 USB에서 약 500mW를 소비합니다. 휴대폰 배터리에서 직접 전원을 공급하면 빠르게 소모되고 부하 시 연결이 끊길 수 있습니다. 전원 공급형 허브는 벽면 전원에서 전력을 끌어와 이 문제를 완전히 해결합니다."
  - question: "WiFi 6E 어댑터(AWUS036AXML)가 NetHunter에서 작동합니까?"
    answer: "지원이 제한적입니다. MT7921AUN 커널 모듈의 가용성은 기기와 커널 버전에 따라 다릅니다. NetHunter 커널은 아직 이를 폭넓게 지원하지 않으므로 RTL8812AU 어댑터를 권장합니다."
  - question: "어떤 Android 기기가 NetHunter를 지원합니까?"
    answer: "공식 지원 기기에는 OnePlus, Google Pixel, 일부 Samsung Galaxy 모델이 포함됩니다. 전체 목록은 NetHunter 기기 페이지에서 확인하고 USB OTG 지원 여부를 확인하시기 바랍니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["nethunter", "android", "usb-otg", "kali-linux", "AWUS036ACH", "RTL8812AU", "mobile-pentest"]
featureimage: "/images/blog/alfa-adapter-nethunter-android-otg.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

Android 휴대폰은 이미 주머니 속의 강력한 컴퓨터입니다. 루팅된 기기에 Kali NetHunter를 설치하고 USB OTG를 통해 ALFA WiFi 어댑터를 연결하면, 진정으로 유능한 주머니 크기의 침투 테스트 플랫폼이 됩니다. 노트북이 필요 없습니다. 부피가 큰 하드웨어도 필요 없습니다. 휴대폰, 짧은 OTG 케이블, 그리고 모니터 모드와 패킷 인젝션을 지원하는 어댑터만 있으면 됩니다.

{{< tldr >}}
USB OTG를 통해 ALFA AWUS036ACH를 연결하고 Kali NetHunter를 실행하는 루팅된 Android 휴대폰은 주머니 크기의 침투 테스트 플랫폼이 됩니다. 전체 NetHunter 빌드, 전원 공급형 OTG 허브, 그리고 최상의 호환성을 위한 RTL8812AU 어댑터가 필요합니다.
{{< /tldr >}}




본 가이드에서는 하드웨어 선택부터 드라이버 로드, 모니터 모드 활성화, NetHunter 앱에 내장된 무선 도구까지, NetHunter에서 ALFA AWUS036ACH(또는 호환 어댑터)를 작동시키는 데 필요한 모든 것을 다룹니다.

---

## Kali NetHunter란 무엇입니까?

Kali NetHunter는 Kali Linux의 공식 모바일 침투 테스트 플랫폼입니다. NetHunter는 Android를 대체하는 대신, 기존 Android 설치 위에 Kali Linux chroot 환경을 설치합니다. 휴대폰은 일반 Android 기기로 계속 작동하는 동시에 모든 도구를 갖춘 완전한 Kali Linux 사용자 공간을 함께 실행합니다.

**주요 특징:**

- Android를 지우지 않고 실행됩니다. 앱, 연락처, 데이터가 그대로 유지됩니다.
- 공격 모듈과 하드웨어 제어를 위한 전용 런처인 NetHunter 앱이 포함되어 있습니다.
- Kali 도구 모음(Metasploit, Aircrack-ng, Nmap 등 수백 가지)에 접근할 수 있는 완전한 터미널을 제공합니다.
- 전체 기능을 위해서는 루팅된 Android 기기가 필요합니다.

**세 가지 에디션:**

| 에디션 | 루트 필요 | 커널 수정 | 사용 사례 |
|---|---|---|---|
| NetHunter (Full) | 예 | 예(커스텀 커널) | 전체 공격 범위, 하드웨어 인터페이스 지원 |
| NetHunter Lite | 예 | 아니요 | 루트 전용 도구, 커스텀 커널 불필요 |
| NetHunter Rootless | 아니요 | 아니요 | 제한된 도구, 하드웨어 공격 불가 |

모니터 모드가 포함된 USB OTG 어댑터 지원을 위해서는 RTL8812AU 모듈을 포함하는 커스텀 커널이 적용된 **전체 NetHunter 에디션**이 필요합니다.

**공식 지원 기기**에는 OnePlus, Google Pixel, 선별된 Samsung Galaxy 기기의 모델이 포함됩니다. 완전하고 최신의 목록은 [공식 NetHunter 기기 페이지](https://www.kali.org/docs/nethunter/)를 참조하시기 바랍니다.

**USB OTG는 필수 요구사항입니다.** 하드웨어를 구매하기 전에, 사용 중인 특정 기기 모델이 USB OTG를 지원하는지 확인하시기 바랍니다. 대부분의 최신 기기는 지원하지만, 일부 보급형 모델과 구형 하드웨어는 필요한 USB 컨트롤러 지원이 없을 수 있습니다.

---

## 하드웨어 요구사항

이 설정을 올바르게 구성한다는 것은 모든 수준에서 호환되는 하드웨어를 선택한다는 의미입니다. 기기, 케이블, 어댑터 등 체인의 어느 한 곳이라도 불일치하면 어댑터가 `lsusb`에 전혀 나타나지 않거나, 간헐적으로 연결이 끊기거나, 드라이버 오류가 발생합니다.

| 항목 | 요구사항 | 비고 |
|---|---|---|
| Android 기기 | 루팅됨, NetHunter 지원, USB OTG 가능 | 구매 전 OTG 지원 확인, 커스텀 커널이 적용된 전체 NetHunter 필요 |
| USB OTG 케이블 / 어댑터 | 기기 포트에 따라 USB-C OTG 또는 Micro-USB OTG | 품질이 중요함, 저렴한 케이블은 간헐적 연결 끊김 유발 |
| ALFA WiFi 어댑터 | AWUS036ACH 또는 AWUS036ACM 권장 | AWUS036ACH(RTL8812AU)가 최상의 NetHunter 커널 모듈 지원, AWUS036ACM(MT7612U)도 호환 |
| 전원 공급형 USB OTG 허브 | 강력히 권장 | 어댑터로 인한 배터리 소모 및 USB 불안정 방지 |

{{< alert "triangle-exclamation" >}}
AWUS036ACH는 USB 포트에서 약 **500mW**를 소비합니다. 전용 전원 없이 휴대폰 배터리에서 직접 전원을 공급하면 배터리가 훨씬 빠르게 소모되고 부하 시 어댑터가 리셋되거나 연결이 끊길 수 있습니다. 벽면 어댑터에서 전력을 공급받아 휴대폰으로 데이터를 전달하는 전원 공급형 OTG 허브는 이 문제를 완전히 제거합니다.
{{< /alert >}}

**전원 공급형 OTG 허브 선택 시:**

전원 전달(power delivery) 패스스루가 포함된 USB OTG를 지원한다고 명시된 허브를 찾으시기 바랍니다. 이는 허브가 USB 충전기에서 5V를 받아 휴대폰이 아닌 충전기에서 연결된 장치에 전원을 공급하면서도 휴대폰과 연결된 장치 간에 데이터를 전달한다는 것을 의미합니다. 모든 USB 허브가 이를 지원하는 것은 아니므로 구매 전에 제품 사양을 주의 깊게 확인하시기 바랍니다.

---

## NetHunter 지원 ALFA 어댑터

NetHunter의 커스텀 커널에는 특정 칩셋 세트에 대한 사전 컴파일된 커널 모듈이 포함되어 있습니다. RTL8812AU 칩셋 제품군은 초기에 통합되었고 활발하게 유지보수되고 있기 때문에 가장 강력한 지원을 받습니다.

| 어댑터 | 칩셋 | NetHunter 지원 | 비고 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | ✅ 최상의 지원 | NetHunter 커널에 `88XXau` 모듈 포함, 모니터 모드 및 패킷 인젝션 완전 지원 |
| AWUS036ACM | MT7612U | ✅ 양호한 지원 | 대체 칩셋, 일반적으로 작동, 사용 기기 커널에 대해 확인 필요 |
| AWUS036ACS | RTL8811AU | ✅ 작동 | RTL8812AU와 동일한 드라이버 제품군, 낮은 전력 소비(~300mW), 단일 대역 2.4/5 GHz |
| AWUS036AXM | MT7921AUN | ⚠️ 제한적 | WiFi 6E 어댑터, 커널 모듈 가용성이 기기 및 커널 버전에 따라 다름 |
| AWUS036AXML | MT7921AUN | ⚠️ 제한적 | AXM과 동일 칩셋, NetHunter 커널에서 보편적으로 지원되지 않음 |

**권장 사항:** 안정적인 NetHunter 작동을 위해서는 RTL8812AU 기반 어댑터를 사용하시기 바랍니다. `88XXau` 드라이버는 대부분의 NetHunter 커스텀 커널에 특별히 포함되어 있고, 광범위한 커뮤니티 문서를 찾을 수 있으며, 문제 해결 경로가 잘 알려져 있습니다. WiFi 6E 어댑터는 기술적으로 인상적이지만, 순수 처리량보다 안정성이 더 중요한 모바일 침투 테스트 설정에서는 호환성 위험을 감수할 가치가 없습니다.

폭넓은 NetHunter 호환성을 갖춘 듀얼 밴드 AC1200 성능을 원한다면, **AWUS036ACH**가 올바른 선택입니다.

---

## 설정 단계

다음 단계는 전체 NetHunter가 설치된 루팅 Android 기기와 USB OTG 케이블 또는 전원 공급형 허브가 준비되어 있다고 가정합니다.

### 1단계: NetHunter 앱 열기

Android 기기에서 NetHunter 앱을 실행합니다. **Kali Services**로 이동하여 chroot 환경이 실행 중인지 확인합니다. 실행 중이 아니면 **Start**를 탭하여 시작합니다. 커널이 USB 장치를 Kali 도구에 노출하려면 chroot가 활성 상태여야 합니다.

### 2단계: OTG를 통해 ALFA 어댑터 연결

USB OTG 케이블 또는 허브를 휴대폰의 USB 포트에 연결한 다음, ALFA 어댑터를 OTG 케이블이나 허브에 연결합니다. 전원 공급형 허브를 사용하는 경우 허브의 전원 어댑터를 먼저 벽면 콘센트에 연결합니다.

### 3단계: USB 권한 부여

Android가 NetHunter 앱이 USB 장치에 접근하도록 허용할지 묻는 권한 대화 상자를 표시합니다. **OK**를 탭하고, 향후 세션에서 이 프롬프트를 건너뛰려면 **항상 허용**을 체크합니다. 권한을 부여하지 않고 이 대화 상자를 닫으면 Kali chroot에서 어댑터에 접근할 수 없습니다.

### 4단계: `lsusb`에서 어댑터 확인

NetHunter 터미널을 열고 실행합니다:

```bash
lsusb
```

**Realtek Semiconductor**와 장치 ID를 포함하는 항목이 보여야 합니다. AWUS036ACH의 경우 다음과 같이 표시됩니다:

```
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

Realtek 장치가 나타나지 않으면 문제는 하드웨어 수준에 있습니다. OTG 케이블을 확인하고, 다른 케이블을 시도하거나, 기기의 개발자 설정에서 OTG가 활성화되어 있는지 확인하시기 바랍니다.

### 5단계: 드라이버 로드

```bash
sudo modprobe 88XXau
```

대부분의 NetHunter 빌드에서는 어댑터가 감지되면 드라이버가 자동으로 로드됩니다. 어댑터 연결 후 인터페이스가 나타나지 않으면 이 명령을 수동으로 실행합니다. `88XXau` 모듈은 NetHunter의 커스텀 커널에 포함된 Aircrack-ng가 유지보수하는 RTL8812AU 드라이버입니다.

### 6단계: 인터페이스 확인

```bash
ip link show | grep wlan
```

`wlan1`(또는 기기에 `wlan0`에 내장 WiFi 인터페이스가 있는 경우 `wlan2`)이 보여야 합니다. 모니터 모드를 활성화하기 전에 인터페이스가 목록에 있는지 확인하시기 바랍니다.

### 7단계: 모니터 모드 활성화

```bash
sudo airmon-ng start wlan1
```

`airmon-ng`가 모니터 모드를 방해할 수 있는 프로세스를 보고하면 먼저 종료한 다음(아래 명령 섹션 참조) 이 명령을 다시 실행합니다. 모니터 모드가 활성화되면 인터페이스 이름이 `wlan1mon`으로 변경됩니다.

---

## NetHunter의 모니터 모드 명령

다음 명령 시퀀스는 어댑터 확인부터 활성 캡처까지 전체 워크플로를 다룹니다:

```bash
# 어댑터가 시스템에서 인식되는지 확인
lsusb | grep -i realtek

# 어댑터 연결 후 자동 로드되지 않으면 드라이버 로드
sudo modprobe 88XXau

# 모니터 모드를 방해하는 프로세스 종료 (NetworkManager, wpa_supplicant 등)
sudo airmon-ng check kill

# ALFA 어댑터 인터페이스에서 모니터 모드 시작
sudo airmon-ng start wlan1

# 보이는 모든 네트워크 스캔 (중지하려면 Ctrl+C)
sudo airodump-ng wlan1mon

# 특정 네트워크의 트래픽 캡처
# -c: 채널, --bssid: 대상 AP MAC 주소, -w: 출력 파일 접두사
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan1mon
```

**모니터 모드를 중지하고 관리 모드로 돌아가려면:**

```bash
sudo airmon-ng stop wlan1mon
```

**어댑터 기능을 확인하고 모니터 모드가 활성 상태인지 확인하려면:**

```bash
iwconfig wlan1mon
```

모든 것이 올바르게 작동한다면 출력에 `Mode:Monitor`가 표시되어야 합니다.

---

## NetHunter WiFi 공격 (승인된 테스트 전용)

NetHunter 앱에는 여러 WiFi 중심 공격 모듈을 위한 내장 GUI 인터페이스가 포함되어 있습니다. 이들은 터미널 명령을 입력하지 않고도 접근할 수 있어 시연이나 현장 운영 시 유용합니다.

{{< alert "triangle-exclamation" >}}
모든 무선 보안 테스트는 **본인이 소유하거나 테스트에 대한 명시적인 서면 허가를 받은 네트워크 및 기기에서만** 수행되어야 합니다. 컴퓨터 네트워크에 대한 무단 접근은 전 세계 대부분의 관할권에서 불법입니다. 여기에 설명된 도구는 승인된 침투 테스트, 보안 연구, 교육 목적으로만 사용됩니다. Yopitek은 오용에 대해 어떠한 책임도 지지 않습니다.
{{< /alert >}}

**WiFi Evil Portal(WPS3):** NetHunter 앱의 기본 메뉴에서 직접 사용할 수 있습니다. 승인된 사회공학 평가 중 자격 증명 수집을 위한 캡티브 포털이 있는 악성 액세스 포인트를 생성합니다. AP 모드를 지원하는 외부 어댑터가 필요합니다.

**MANA Rogue AP Toolkit:** **NetHunter 앱 > Wireless Attacks > MANA Toolkit**에 위치합니다. MANA는 KARMA 스타일 공격과 SSL 스트리핑 기능으로 표준 악성 AP 개념을 확장합니다. 전체 기능을 사용하려면 호환되는 외부 WiFi 어댑터가 필요합니다. 내장 Android WiFi 칩은 대부분의 MANA 구성에 충분하지 않습니다.

두 모듈 모두 ALFA 어댑터와 직접 연동되므로, 이 내장 도구를 실질적으로 사용하려면 외부 어댑터 지원이 필수적입니다.

---

## 배터리 및 전원 관리

휴대폰에서 AWUS036ACH를 실행하는 것은 배터리와 USB 전원 전달 서브시스템에 부담을 줍니다. 예상되는 상황과 완화 방법은 다음과 같습니다:

**전력 소비:** AWUS036ACH는 활성 사용 중 지속적으로 약 500mW를 소비합니다. 일반적인 3,500 mAh Android 배터리에서는 일반 휴대폰 사용에 비해 배터리 소모율이 대략 두 배가 됩니다.

**전원 공급형 OTG 허브 사용:** 이것이 가장 효과적인 해결책입니다. 허브가 벽면 어댑터에서 전원을 끌어와 ALFA 어댑터에 공급합니다. 휴대폰의 USB 포트는 어댑터에 전원이 아닌 데이터만 전달합니다. 배터리 소모가 거의 정상 수준으로 돌아옵니다.

**충전하면서 작동:** 전원 공급형 허브를 사용할 수 없는 경우, PD 패스스루가 포함된 USB-C 허브를 사용하여 휴대폰을 동시에 충전함으로써 배터리 소모를 완화할 수 있습니다. 이는 데이터 패스스루(OTG 기능용)와 동시 충전 입력을 모두 지원하는 허브가 필요한데, 이러한 제품은 구할 수 있지만 신중한 제품 선택이 필요합니다.

**디스플레이 관리:** 화면은 현장 운영 중 또 다른 주요 전력 소비 요소입니다. 디스플레이 시간 제한을 30초(**설정 > 디스플레이 > 절전**)로 설정하고 밝기를 최소로 낮춥니다. 전원 공급형 허브와 결합하면 실질적으로 여러 시간의 운영 시간을 확보할 수 있습니다.

**열 관리 고려사항:** 휴대폰 케이스 안에서 어댑터를 장시간 작동하면 열이 축적될 수 있습니다. 휴대폰의 열 보호 기능이 USB 컨트롤러를 조절(throttle)하면 어댑터 연결 끊김이 발생할 수 있습니다. 장시간 캡처 세션 중에는 휴대폰 케이스를 제거하시기 바랍니다.

---

## 문제 해결

**어댑터가 인식되지 않음(`lsusb`에 아무것도 표시되지 않음):**
1. USB OTG가 활성화되어 있는지 확인 — **설정 > 개발자 옵션 > OTG** 확인(위치는 Android 버전과 제조사에 따라 다름)
2. 다른 OTG 케이블 시도 — 케이블 품질은 흔한 실패 지점입니다
3. 다른 USB 장치에 어댑터를 연결하여 어댑터 자체가 정상인지 확인
4. 제조사 사양을 확인하여 기기가 USB OTG를 지원하는지 확인

**드라이버가 로드되지 않음(`modprobe` 후 `wlan1` 인터페이스 없음):**
1. NetHunter 터미널에서 `dmesg`를 확인하여 USB 및 드라이버 오류 메시지 찾기: `dmesg | tail -30`
2. NetHunter chroot가 실행 중이고 그 내부에서 명령을 실행하고 있는지 확인
3. NetHunter 빌드에 `88XXau` 모듈이 포함되어 있는지 확인: `find /lib/modules -name "*88XX*"`

**사용 중 `wlan1` 인터페이스가 사라짐:**
이는 거의 항상 USB 전원 문제입니다. 어댑터가 휴대폰 USB 포트가 공급할 수 있는 것보다 더 많은 전류를 끌어오고 있는 것입니다. 전원 공급형 OTG 허브를 사용하시기 바랍니다. 임시 조치로 `sudo iw dev wlan1 set txpower fixed 1000`(10 dBm으로 설정)으로 송신 전력을 낮출 수 있습니다.

**권한 거부 오류:**
NetHunter chroot에서 루트로 명령을 실행하고 있는지 확인합니다. 먼저 `sudo su`를 실행한 다음 명령을 실행합니다. 또는 각 명령 앞에 `sudo`를 붙입니다.

**모니터 모드는 시작되지만 `airodump-ng`에 네트워크가 나타나지 않음:**
1. 채널이 올바르게 설정되어 있는지 확인 — 모든 대역을 스캔하려면 `sudo airodump-ng --band abg wlan1mon` 시도
2. 모니터 모드 시작 전에 `airmon-ng check kill`이 실행되었는지 확인
3. 안테나가 어댑터에 제대로 연결되어 있는지 확인

---

{{< faq >}}

## 관련 가이드

ALFA 어댑터의 다른 플랫폼 및 사용 사례:

- [Kali Linux에서 AWUS036ACH 설정 가이드(데스크톱/노트북)](/ko/blog/awus036ach-kali-linux-setup/)
- [Raspberry Pi 및 Kali에서 ALFA 어댑터 사용하기](/ko/blog/alfa-adapter-raspberry-pi-kali/)

## 참고 자료

1. [Kali NetHunter 공식 문서](https://www.kali.org/docs/nethunter/)
2. [aircrack-ng rtl8812au 드라이버 프로젝트](https://github.com/aircrack-ng/rtl8812au)
3. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
4. [Android USB OTG 개발자 문서](https://developer.android.com/guide/topics/connectivity/usb)
