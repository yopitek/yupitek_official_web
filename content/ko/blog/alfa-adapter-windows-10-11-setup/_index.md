---
title: "Windows 10 및 Windows 11용 ALFA 어댑터 설정 가이드"
description: "Windows 10/11에서 ALFA USB WiFi 어댑터를 설치하고 구성하는 방법. 드라이버 다운로드, Acrylic WiFi를 이용한 모니터 모드, 문제 해결, Windows 사용자를 위한 어댑터 비교를 다룹니다."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Windows는 ALFA 어댑터의 모니터 모드를 지원합니까?"
    answer: "Windows는 완전한 모니터 모드를 기본적으로 지원하지 않습니다. NDIS 드라이버 모델은 원시 802.11 프레임 캡처를 노출하지 않습니다. 수동 스캔은 Acrylic WiFi Pro만 가능합니다. 완전한 모니터 모드에는 Kali Linux가 필요합니다."
  - question: "Windows에서 패킷 인젝션을 할 수 있습니까?"
    answer: "아니요. 현재 ALFA 어댑터에 대해 원시 802.11 패킷 인젝션을 지원하는 Windows 드라이버는 없습니다. 이 기능은 Linux에서만 사용할 수 있습니다."
  - question: "Windows 호환성이 가장 좋은 ALFA 어댑터는 무엇입니까?"
    answer: "AWUS036ACH(RTL8812AU)와 AWUS036ACM(MT7612U)은 WHQL 서명 드라이버를 갖추고 있으며, Windows 10/11 호환성 기록이 가장 충실하고 플러그 앤 플레이가 안정적입니다."
  - question: "Windows 11에서 MT7921AUN 드라이버를 수동으로 설치해야 합니까?"
    answer: "아니요. MT7921AUN 드라이버는 Windows 11 드라이버 저장소(빌드 22000+)에 포함되어 있습니다. 어댑터를 연결하면 몇 분 안에 드라이버가 자동으로 설치됩니다."
  - question: "장치 관리자에 Code 43이 표시되면 어떻게 해야 합니까?"
    answer: "드라이버를 제거하고 재부팅한 후 어댑터를 다시 연결하고 방법 B로 수동 설치합니다. 여러 컴퓨터에서 Code 43이 계속되면 일반적으로 하드웨어 결함을 의미합니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["windows-10", "windows-11", "alfa-network", "wifi-adapter", "driver-install", "acrylic-wifi"]
featureimage: "/images/blog/alfa-adapter-windows-10-11-setup.webp"
---

ALFA Network USB WiFi 어댑터는 보안 연구 및 네트워킹 분야에서 잘 알려져 있지만, 대부분의 튜토리얼은 Linux에만 초점을 맞춥니다. Windows 사용자에게 좋은 소식이 있습니다. 모든 주요 ALFA 어댑터는 제조사 제공 드라이버로 Windows 10 및 Windows 11에서 작동하며, 소스 컴파일이 필요 없습니다.

{{< tldr >}}
ALFA 어댑터는 Windows 10/11에서 WiFi 연결용으로 플러그 앤 플레이로 작동하지만, NDIS 드라이버 모델은 완전한 모니터 모드나 패킷 인젝션을 지원하지 않습니다. 보안 테스트에는 Kali Linux(베어메탈 또는 USB 패스스루를 사용하는 VM)로 전환하시기 바랍니다. Windows는 일상적인 연결과 WiFi 서베이에는 충분합니다.
{{< /tldr >}}




Linux와의 결정적인 차이는 모니터 모드입니다. Linux에서는 `aircrack-ng`, `airodump-ng` 같은 도구가 패킷 인젝션과 함께 원시 802.11 캡처를 활용합니다. Windows에서는 드라이버 모델(NDIS)이 동일한 하드웨어 기능을 노출하지 않습니다. 완전한 모니터 모드와 패킷 인젝션은 <strong>Windows에서 기본적으로 사용할 수 없습니다</strong>. Windows가 잘하는 것, 그것도 매우 잘하는 것은 플러그 앤 플레이 연결과 Acrylic WiFi Analyzer 같은 완성도 높은 도구를 이용한 WiFi 스캔입니다.

본 가이드는 드라이버 설치, WiFi 스캔, 그리고 Windows가 ALFA 어댑터로 할 수 있는 것과 할 수 없는 것에 대한 솔직한 평가를 다룹니다.

---

## Windows 호환 ALFA 어댑터

아래의 모든 어댑터는 Windows 10 및 Windows 11에서 공식 지원됩니다. 드라이버 가용성과 모니터 모드 기능은 칩셋에 따라 다릅니다.

<div class="table-nowrap" style="overflow-x: auto;">

| 모델 | 칩셋 | Windows 10 | Windows 11 | 모니터 모드 지원 |
|---|---|---|---|---|
| [AWUS036ACH](/ko/products/alfa/awus036ach/) | RTL8812AU | ✅ 완전 지원 | ✅ 완전 지원 | ⚠️ 수동 스캔만(Acrylic WiFi Pro) |
| [AWUS036ACM](/ko/products/alfa/awus036acm/) | MT7612U | ✅ 완전 지원 | ✅ 완전 지원 | ⚠️ 수동 스캔만 |
| [AWUS036ACS](/ko/products/alfa/awus036acs/) | RTL8811AU | ✅ 완전 지원 | ✅ 완전 지원 | ⚠️ 수동 스캔만 |
| [AWUS036AX](/ko/products/alfa/awus036ax/) | RTL8832BU | ⚠️ 수동 드라이버 다운로드 | ✅ 기본 내장 드라이버 | ⚠️ 제한적 |
| [AWUS036AXER](/ko/products/alfa/awus036axer/) | RTL8832BU | ⚠️ 수동 드라이버 다운로드 | ✅ 기본 내장 드라이버 | ⚠️ 제한적 |
| [AWUS036AXM](/ko/products/alfa/awus036axm/) | MT7921AUN | ⚠️ 수동 드라이버 다운로드 | ✅ 기본 내장 드라이버 | ❌ 미지원 |
| [AWUS036AXML](/ko/products/alfa/awus036axml/) | MT7921AUN | ⚠️ 수동 드라이버 다운로드 | ✅ 기본 내장 드라이버 | ❌ 미지원 |

</div>

{{< alert "circle-info" >}}
순수하게 Windows 일상 사용 목적이라면 AWUS036ACH(RTL8812AU)와 AWUS036ACM(MT7612U)이 가장 충분히 검증된 선택입니다. 두 제품 모두 Realtek/MediaTek WHQL 서명 드라이버를 제공받으며 Windows 호환성 기록이 가장 폭넓습니다.
{{< /alert >}}

---

## 드라이버 설치

### 방법 A: Windows Update(권장)

Windows Update는 대부분의 어댑터에서 가장 쉬운 방법입니다. 지원되는 ALFA 어댑터를 연결하면 Windows가 Windows Update에서 일치하는 NDIS 드라이버를 자동으로 조회합니다.

1. ALFA 어댑터를 USB 3.0 포트에 연결합니다.
2. 30~60초 기다립니다. Windows 10에서는 *"장치 드라이버 소프트웨어가 설치되었습니다"* 알림이 표시되며, Windows 11에서는 별도 알림 없이 완료됩니다.
3. <strong>장치 관리자</strong>(`Win + X` → 장치 관리자)를 엽니다.
4. <strong>네트워크 어댑터</strong>를 펼칩니다. 어댑터가 목록에 표시되어야 합니다(예: *"Realtek 8812AU Wireless LAN 802.11ac USB NIC"* 또는 *"MediaTek Wi-Fi 6 MT7921AUN Wireless LAN Card"*).
5. 어댑터에 노란색 경고 아이콘이 표시되면 방법 B로 진행합니다.

{{< alert "circle-info" >}}
Windows Update로 드라이버를 다운로드하려면 인터넷 연결이 필요합니다. 격리된 랩 머신을 설정하는 경우, 다른 컴퓨터에서 드라이버 패키지를 다운로드하여 수동으로 옮긴 후 방법 B를 사용하시기 바랍니다.
{{< /alert >}}

### 방법 B: 수동 드라이버 설치 — RTL8812AU(AWUS036ACH / AWUS036ACS)

1. [ALFA Network 다운로드 페이지](https://www.alfa.com.tw/service_1.html) 또는 Realtek 드라이버 아카이브에서 RTL8812AU용 최신 Windows WHQL 드라이버를 다운로드합니다.
2. `.zip` 아카이브를 로컬 폴더(예: `C:\Drivers\RTL8812AU`)에 압축 해제합니다.
3. `.exe` 설치 프로그램을 관리자 권한으로 실행합니다. UAC 프롬프트를 승인합니다.
4. 설치 마법사를 따릅니다. 메시지가 표시되면 기본 설치 경로를 그대로 둡니다.
5. 설치가 완료되면 재부팅합니다.
6. <strong>장치 관리자</strong> → <strong>네트워크 어댑터</strong>를 엽니다. 어댑터가 경고 아이콘 없이 표시되는지 확인합니다.

드라이버 버전을 확인하려면:

1. 장치 관리자에서 어댑터를 마우스 오른쪽 버튼으로 클릭 → <strong>속성</strong>.
2. <strong>드라이버</strong> 탭을 클릭합니다.
3. 향후 참고를 위해 <strong>드라이버 버전</strong>과 <strong>드라이버 날짜</strong>를 기록합니다.

### 방법 B: 수동 드라이버 설치 — MT7921AUN(AWUS036AXM / AWUS036AXML)

MediaTek의 MT7921AUN 드라이버는 Windows 11의 드라이버 저장소(빌드 22000+)에 포함되어 있습니다. Windows 10의 경우:

1. [MediaTek 공식 사이트](https://www.mediatek.com/products/home-networking/wi-fi-6-6e) 또는 ALFA Network 지원 페이지에서 MediaTek MT7921 드라이버 패키지를 다운로드합니다.
2. 패키지를 압축 해제하고 `Setup.exe`를 관리자 권한으로 실행합니다.
3. 설치 후 재부팅합니다.

{{< alert "circle-info" >}}
MT7921AUN 어댑터(AWUS036AXM, AWUS036AXML)를 사용하는 Windows 11 사용자는 새로 설치한 시스템에서도 일반적으로 어댑터 연결 후 몇 분 안에 작동하는 드라이버를 받습니다. 수동 다운로드가 필요 없습니다.
{{< /alert >}}

### 장치 관리자의 일반적인 오류 코드

| 오류 코드 | 의미 | 우선 조치 |
|---|---|---|
| <strong>Code 43</strong> | 드라이버가 오류를 보고함 | 드라이버 제거 → 재부팅 → 재설치 |
| <strong>Code 10</strong> | 장치를 시작할 수 없음 | 다른 USB 포트 시도, USB 선택적 절전 비활성화 |
| <strong>Code 28</strong> | 드라이버가 설치되지 않음 | Windows Update 실행 또는 드라이버 수동 설치 |
| <strong>Code 45</strong> | 장치가 연결되지 않음 | 어댑터 재연결, 연장 케이블 사용 시 다른 USB 케이블 시도 |

---

## Windows에서 ALFA 어댑터로 WiFi 스캔하기

### Windows 기본 명령줄 스캔

Windows에는 추가 소프트웨어가 필요 없는 WiFi 스캔 명령이 내장되어 있습니다:

```cmd
netsh wlan show networks mode=bssid
```

이 명령은 보이는 모든 SSID와 함께 BSSID(MAC 주소), 신호 강도, 무선 유형, 채널, 인증 유형을 출력합니다. 빠른 진단에는 유용하지만 실시간 채널 그래프나 숨겨진 SSID 감지 기능은 없습니다.

### Acrylic WiFi Analyzer(무료)

Windows에서 본격적인 WiFi 분석을 하려면 [Acrylic WiFi Analyzer](https://www.acrylicwifi.com/)를 권장합니다. 무료 버전은 다음을 제공합니다:

- 2.4 GHz, 5 GHz, 6 GHz 대역에 걸친 실시간 스캔
- 채널 점유율 그래프 — 혼잡한 채널을 즉시 식별
- 숨겨진 SSID 감지(빈 SSID를 브로드캐스트하는 네트워크 표시)
- 개별 액세스 포인트의 신호 이력 차트
- BSSID 식별을 위한 벤더 OUI 조회

Acrylic WiFi는 위에 나열된 모든 ALFA 모델을 포함하여 Windows와 호환되는 모든 WiFi 어댑터에서 작동합니다. NDIS 드라이버 확장이 Windows 무선 스택과 직접 통합되므로 Linux 방식의 모니터 모드 없이도 작동합니다.

{{< alert "circle-info" >}}
Acrylic WiFi Analyzer는 수동 스캔 측면에서 `airodump-ng` 같은 도구에 가장 가까운 Windows 대안입니다. 워크플로가 WiFi 서베이, 사이트 분석, 채널 계획이라면 Windows를 벗어나지 않고도 필요한 거의 모든 것을 다룰 수 있습니다.
{{< /alert >}}

### Windows에서 Wireshark 캡처

Wireshark는 Npcap(아래 전용 섹션 참조)의 도움으로 Windows에서 WiFi 트래픽을 캡처할 수 있습니다. 그러나 진정한 모니터 모드가 없으면 다음만 캡처할 수 있습니다:

- 사용자 어댑터로 향하는 프레임(사용자 MAC으로의 유니캐스트)
- 연결된 네트워크의 브로드캐스트 및 멀티캐스트 프레임

다른 기기 간의 트래픽은 동일한 브로드캐스트 도메인에 있고 스위치 네트워크에서 Wireshark가 무차별(promiscuous) 모드로 실행 중인 경우가 아니라면 캡처되지 <strong>않습니다</strong>. 완전한 802.11 프레임 캡처(관리 프레임, 외부 AP의 비콘 프레임)는 제한됩니다.

---

## Windows의 모니터 모드(솔직한 사실)

이 부분은 기대치를 명확히 설정해야 하는 지점입니다.

<strong>Windows의 모니터 모드는 Linux 모니터 모드와 근본적으로 다릅니다.</strong>

Linux에서는 `aircrack-ng/rtl8812au` 같은 드라이버가 진정한 모니터 모드 인터페이스(`wlan0mon`)를 노출하며, 이 인터페이스는 연결(association) 없이도 무선 환경의 모든 802.11 프레임, 즉 관리 프레임, 다른 네트워크의 데이터 프레임, 프로브 요청, 비콘 프레임을 수신합니다. 어댑터는 또한 패킷 인젝션, 즉 하드웨어 수준에서 원시 802.11 프레임을 송신하는 기능을 지원합니다.

Windows에서는 NDIS 드라이버 모델이 이러한 기능을 노출하지 않습니다. Windows 기반 모니터링을 위한 실용적인 두 가지 접근 방식은 다음과 같습니다:

<strong>접근 A: Acrylic WiFi Pro + 호환 드라이버</strong>

Acrylic WiFi Pro는 커스텀 NDIS 드라이버 확장을 사용하여 *수동 802.11 스캔*을 가능하게 합니다. 이를 통해 연결되지 않은 액세스 포인트의 비콘 프레임과 프로브 응답을 수신할 수 있으며, RF 서베이, 채널 분석, AP 열거에 충분합니다. 패킷 인젝션이나 완전한 핸드셰이크 캡처는 지원하지 <strong>않습니다</strong>.

<strong>접근 B: Kali Linux 라이브 USB</strong>

완전한 모니터 모드와 패킷 인젝션이 필요한 워크플로(WPA 핸드셰이크 캡처, 디인증 테스트, 비콘 플러딩)의 경우 올바른 플랫폼은 Kali Linux입니다. 두 가지 옵션이 있습니다:

- 동일한 머신에서 <strong>Kali Linux 라이브 USB</strong>로 부팅(베어메탈, 완전한 하드웨어 접근)
- USB 패스스루를 사용하여 ALFA 어댑터를 VM의 USB 스택에 직접 넘겨주는 <strong>Kali Linux VM</strong>(VMware 또는 VirtualBox) 실행

자세한 VM 설정 지침은 [VirtualBox/VMware USB 패스스루 가이드](/ko/blog/alfa-adapter-virtualbox-vmware-usb/)를 참조하시기 바랍니다.

{{< alert "triangle-exclamation" >}}
WPA 핸드셰이크 캡처, 디인증 프레임, 또는 모든 능동적 802.11 공격을 위해 워크플로에 모니터 모드 + 패킷 인젝션이 필요하다면, Windows는 이를 안정적으로 수행할 수 없습니다. Kali Linux(베어메탈 또는 USB 패스스루를 사용하는 VM)가 올바른 플랫폼입니다. 현재 ALFA 어댑터에 대해 원시 802.11 인젝션을 지원하는 Windows 드라이버는 없습니다.
{{< /alert >}}

---

## 문제 해결

### 어댑터가 전혀 인식되지 않음

1. 다른 USB 포트, 가능하면 USB 3.0(파란색 포트)을 시도합니다. 일부 USB 허브는 듀얼 밴드 어댑터에 충분한 전력을 공급하지 못합니다.
2. 장치 관리자를 열고 <strong>기타 장치</strong> 아래에 노란색 물음표가 있는 항목이 있는지 확인합니다. 이는 Windows가 하드웨어를 인식하지만 드라이버가 없다는 것을 의미합니다.
3. 마우스 오른쪽 버튼 클릭 → <strong>드라이버 업데이트</strong> → <strong>내 컴퓨터에서 찾아보기</strong>를 선택하고 수동으로 다운로드한 드라이버 폴더를 지정합니다.
4. 기타 장치 아래에도 장치 관리자에 아무것도 나타나지 않으면, 다른 USB 케이블(연장 케이블 사용 시)을 시도하거나 다른 컴퓨터에서 어댑터를 테스트하여 하드웨어 고장 여부를 확인합니다.

### 장치 관리자에는 어댑터가 보이지만 네트워크가 검색되지 않음

1. Windows Defender 방화벽이 어댑터 초기화를 차단하고 있지 않은지 확인하기 위해 일시적으로 비활성화합니다. 테스트 후 다시 활성화합니다.
2. 장치 관리자에서 어댑터를 마우스 오른쪽 버튼으로 클릭 → <strong>속성</strong> → <strong>고급</strong> 탭. <strong>Wireless Mode</strong> 또는 <strong>Band</strong> 설정을 찾습니다. 5 GHz 전용으로 설정되어 있으면 2.4 GHz 전용 환경에서는 네트워크가 보이지 않습니다.
3. 어댑터가 비활성화되어 있지 않은지 확인합니다: 마우스 오른쪽 버튼 클릭 → <strong>디바이스 사용</strong>.
4. 관리자 권한 명령 프롬프트에서 `netsh wlan show interfaces`를 실행하여 어댑터의 작동 상태를 확인합니다.

### Windows 11에서 느린 속도 또는 잦은 연결 끊김

Windows 11의 <strong>Connected Standby</strong>(Modern Standby)는 USB 장치를 적극적으로 절전 모드로 전환하여 USB WiFi 어댑터에 간섭할 수 있습니다.

USB 선택적 절전을 비활성화합니다:

1. <strong>제어판</strong> → <strong>전원 옵션</strong> → <strong>설정 변경</strong> → <strong>고급 전원 관리 옵션 설정 변경</strong>을 엽니다.
2. <strong>USB 설정</strong> → <strong>USB 선택적 절전 모드 설정</strong>을 펼칩니다.
3. <strong>배터리 사용</strong>과 <strong>전원 사용</strong> 모두 <strong>사용 안 함</strong>으로 설정합니다.
4. <strong>적용</strong> → <strong>확인</strong>을 클릭한 후 재부팅합니다.

### Code 43: 드라이버가 오류를 보고함

1. 장치 관리자를 열고 어댑터를 마우스 오른쪽 버튼으로 클릭 → <strong>디바이스 제거</strong>. 옵션이 표시되면 *"이 장치의 드라이버 소프트웨어를 삭제합니다"*를 체크합니다.
2. 어댑터를 분리합니다.
3. 컴퓨터를 재부팅합니다.
4. 어댑터를 다시 연결합니다.
5. 위의 방법 B로 드라이버를 재설치합니다.

클린 재설치 후에도 Code 43이 계속되면 다른 USB 포트를 시도하거나 다른 머신에서 테스트하시기 바랍니다. 여러 머신에서 Code 43이 지속되면 일반적으로 어댑터 자체의 하드웨어 결함을 의미합니다.

---

## ALFA 어댑터 + Wireshark 설정

Windows의 Wireshark는 패킷 캡처 라이브러리로 <strong>Npcap</strong>이 필요합니다. WinPcap(레거시 대안)은 오래되어 최신 Windows 버전을 안정적으로 지원하지 않습니다.

### 1단계: Npcap 설치

1. [https://npcap.com/](https://npcap.com/)에서 Npcap을 다운로드합니다(개인 및 교육용 무료).
2. 설치 프로그램을 관리자 권한으로 실행합니다.
3. Wireshark와 함께 레거시 도구를 사용할 계획이라면 설치 중 <strong>"Install Npcap in WinPcap API-compatible mode"</strong>를 체크합니다.
4. 재부팅합니다.

### 2단계: Wireshark 구성

1. Wireshark를 엽니다. ALFA 어댑터가 인터페이스 목록에 나타납니다.
2. 어댑터 인터페이스를 더블 클릭하여 캡처를 시작합니다.
3. 802.11 관리 프레임(비콘 프레임, 프로브 요청)을 필터링하려면 다음 Wireshark 표시 필터를 사용합니다:

```
wlan.fc.type == 0
```

4. 프로브 요청만 필터링하려면:

```
wlan.fc.type_subtype == 0x0004
```

{{< alert "circle-info" >}}
`wlan.fc.type` 필터는 Wireshark가 헤더가 보이는 실제 802.11 프레임을 수신할 때만 작동합니다. 모니터 모드가 없는 Windows에서는 WiFi를 통하더라도 대부분의 캡처가 Ethernet II 프레임으로 표시됩니다. NDIS 계층이 프레임을 Npcap으로 전달하기 전에 802.11 헤더를 제거하기 때문입니다. 완전한 802.11 헤더 캡처에는 Linux에서 사용할 수 있는 진정한 모니터 모드 인터페이스가 필요합니다.
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
허가 없이 네트워크 트래픽을 캡처하는 것은 대부분의 관할권에서 불법입니다. 본인이 소유하거나 테스트에 대한 명시적인 서면 허가를 받은 네트워크에서만 트래픽을 캡처하시기 바랍니다.
{{< /alert >}}

---

{{< faq >}}

## 요약: ALFA 어댑터를 위한 Windows vs Linux

| 기능 | Windows 10/11 | Kali Linux |
|---|---|---|
| <strong>플러그 앤 플레이</strong> | ✅ 자동 드라이버 설치 | ⚠️ 칩셋에 따라 다름 |
| <strong>WiFi 스캔</strong> | ✅ Acrylic WiFi / netsh | ✅ airodump-ng / iwlist |
| <strong>모니터 모드</strong> | ⚠️ 수동만(Acrylic Pro) | ✅ 완전한 모니터 모드 |
| <strong>패킷 인젝션</strong> | ❌ 미지원 | ✅ 완전한 인젝션 |
| <strong>Wireshark 캡처</strong> | ⚠️ 제한적(802.11 헤더 없음) | ✅ 완전한 802.11 캡처 |
| <strong>WPA 핸드셰이크 캡처</strong> | ❌ 신뢰할 수 없음 | ✅ aircrack-ng / hcxdumptool |
| <strong>최적 사용 사례</strong> | 일상 연결, WiFi 서베이, 채널 분석 | 보안 테스트, CTF 과제, 침투 테스트 |

결론: 목표가 네트워크 연결, WiFi 분석, 채널 계획이라면 Windows는 ALFA 어댑터를 위한 훌륭한 플랫폼입니다. 워크플로에 원시 802.11 프레임 인젝션이나 WPA 핸드셰이크 캡처가 필요해지는 순간, 네이티브로 또는 USB 패스스루를 사용하는 VM을 통해 Kali Linux로 전환하시기 바랍니다.

---

## 관련 가이드

- [ALFA 어댑터를 위한 VirtualBox 및 VMware USB 패스스루](/ko/blog/alfa-adapter-virtualbox-vmware-usb/) — 완전한 ALFA 어댑터 지원으로 VM에서 Kali Linux 실행
- [Kali Linux 및 Ubuntu용 드라이버 설치 가이드](/ko/blog/install-alfa-driver-kali-ubuntu/) — 칩셋별 전체 드라이버 설치
- [ALFA WiFi 어댑터 구매 가이드 2026](/ko/blog/alfa-wifi-adapter-buyer-guide-2026/) — 사용 사례에 맞는 어댑터 선택

## 참고 자료

1. [ALFA Network 공식 드라이버 다운로드](https://www.alfa.com.tw/service_1.html)
2. [Microsoft NDIS 드라이버 문서](https://learn.microsoft.com/windows-hardware/drivers/network/ndis-drivers)
3. [Acrylic WiFi Analyzer 공식 웹사이트](https://www.acrylicwifi.com/)
4. [Npcap 공식 웹사이트](https://npcap.com/)
5. [Wireshark 공식 문서](https://www.wireshark.org/docs/)
