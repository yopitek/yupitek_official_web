---
title: "macOS에서 ALFA WiFi 어댑터 사용하기: VMware Fusion 및 Parallels USB 패스스루"
description: "macOS에서 ALFA USB WiFi 어댑터를 사용하는 방법. macOS 네이티브 지원, VMware Fusion USB 패스스루, Parallels Desktop을 통한 Kali Linux 모니터 모드 및 패킷 인젝션을 다룹니다."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "ALFA 어댑터가 macOS에서 네이티브로 모니터 모드를 사용할 수 있습니까?"
    answer: "아니요. macOS의 CoreWLAN 및 IO80211Family 프레임워크는 서드파티 어댑터에 대해 모니터 모드나 패킷 인젝션을 지원하지 않습니다. USB 패스스루를 사용하는 Kali Linux VM을 실행해야 합니다."
  - question: "Apple Silicon에서 VMware Fusion과 Parallels 중 무엇을 선택해야 합니까?"
    answer: "둘 다 작동하지만, Parallels Desktop 19 이상은 일반적으로 Apple Silicon에서 VMware Fusion보다 더 나은 ARM64 VM 성능과 더 안정적인 USB 패스스루를 제공합니다."
  - question: "AWUS036AXML은 Apple Silicon Kali VM에서 드라이버 컴파일이 필요합니까?"
    answer: "아니요. MT7921AUN 드라이버는 Linux 5.18부터 메인라인 커널에 포함되어 있습니다. Kali ARM64 2024.x 이상에서는 연결 시 자동으로 인식됩니다."
  - question: "Intel Mac에서는 표준 Kali x86_64 ISO를 사용할 수 있습니까?"
    answer: "네. Intel Mac은 x86_64 아키텍처이므로 공식 kali.org의 표준 Kali Linux x86_64 ISO를 사용하여 VM을 생성할 수 있습니다."
  - question: "Apple Silicon에서 보안 테스트에 VirtualBox가 적합합니까?"
    answer: "권장하지 않습니다. VirtualBox의 Apple Silicon 지원은 아직 실험적 단계이며 USB 패스스루 관련 알려진 문제가 있습니다. 대신 VMware Fusion이나 Parallels를 사용하시기 바랍니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["macos", "vmware-fusion", "parallels", "kali-linux", "usb-passthrough", "alfa-network", "AWUS036AXML"]
featureimage: "/images/blog/alfa-adapter-macos-vm-setup.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

macOS는 완성도 높은 프로덕션급 운영체제입니다. 그러나 무선 보안 연구를 위해 설계된 플랫폼은 아닙니다. 모든 진지한 침투 테스터의 도구에서 핵심이 되는 두 가지 기능, 즉 <strong>모니터 모드</strong>와 <strong>패킷 인젝션</strong>은 macOS Wi-Fi 스택에서 완전히 빠져 있습니다. Apple의 Wi-Fi 드라이버는 깔끔하고 기능적인 네트워킹 인터페이스를 제공할 뿐, 그 이상은 제공하지 않습니다.

{{< tldr >}}
macOS는 ALFA 어댑터에 대해 모니터 모드나 패킷 인젝션을 지원하지 않습니다. 해결책은 USB 패스스루를 사용하여 VMware Fusion 또는 Parallels에서 Kali Linux VM을 실행하는 것입니다. Apple Silicon에서는 ARM64 Kali 이미지가 필요합니다.
{{< /tldr >}}




ALFA Network 어댑터는 드라이버 지원이 깊고 커뮤니티에서 충분히 검증된 Linux에서는 이러한 상황을 바꿔 줍니다. 하지만 macOS에서는 사정이 다릅니다. ALFA 어댑터가 macOS에서 인식되더라도, 네이티브 네트워크 스택은 어댑터를 모니터 모드로 전환하거나 원시(raw) 프레임을 인젝션하도록 허용하지 않습니다. 유일하게 신뢰할 수 있는 방법은 <strong>가상 머신 내부에서 Kali Linux를 실행</strong>하고, USB 어댑터를 게스트 OS로 직접 패스스루하여 macOS를 완전히 우회하는 것입니다.

본 가이드에서는 macOS의 두 주요 하이퍼바이저인 VMware Fusion과 Parallels Desktop 모두에서 이를 올바르게 수행하는 방법을 다루며, 특히 어댑터 및 ISO 선택을 복잡하게 만드는 ARM 아키텍처 제약을 도입하는 <strong>Apple Silicon(M1/M2/M3)</strong>에 주목합니다.

---

## macOS 네이티브: VM 없이 가능한 작업

VM 설정으로 바로 넘어가기 전에, macOS가 ALFA 어댑터만으로 무엇을 할 수 있고 할 수 없는지를 이해하는 것이 유용합니다.

<strong>AWUS036AXML(MT7921AUN 칩셋):</strong> 이 어댑터는 macOS에서 일반 USB 네트워킹 장치로 인식됩니다. macOS 13 Ventura 이상에 포함된 <strong>MT7921AUN</strong> 드라이버가 어댑터를 자동으로 인식합니다. <strong>시스템 환경설정 → 네트워크</strong>(Ventura 이상에서는 <strong>시스템 설정 → 네트워크</strong>)에 새 인터페이스로 나타나며, 다른 어댑터와 마찬가지로 Wi-Fi 네트워크에 연결할 수 있습니다. 구버전 macOS에서는 전혀 인식되지 않을 수 있습니다.

<strong>AWUS036ACH(RTL8812AU) 및 AWUS036ACM(MT7612U) — 서드파티 macOS 드라이버가 필요한 어댑터:</strong> 이들은 macOS용 서드파티 드라이버가 필요합니다. 여러 커뮤니티 및 상용 드라이버 패키지가 존재하지만 호환성은 취약합니다. macOS 포인트 업데이트 이후 드라이버 재빌드가 빈번하게 발생하고, macOS 11 이후 커널 확장 서명 요구사항이 강화되었으며, Apple Silicon에서는 커널 확장에 대한 Rosetta의 한계로 인해 상황이 더욱 불안정합니다. 기능적인 설치는 가능하지만 유지보수 부담이 큽니다.

<strong>명확한 한계 — 모니터 모드 불가:</strong> 어떤 어댑터를 사용하든 어떤 드라이버를 설치하든, macOS는 원시 모니터 모드 인터페이스를 제공하지 않습니다. CoreWLAN 프레임워크와 그 기반이 되는 `IO80211Family.kext` 아키텍처는 서드파티 어댑터에 대해 이를 지원하지 않습니다. Wireshark 같은 도구는 `en0`를 통해 내장 Airport 어댑터로 macOS에서 Wi-Fi 트래픽을 캡처할 수 있지만, 이는 수동 캡처에 불과합니다. airmon-ng 모니터 모드와 동등하지 않으며 패킷 인젝션도 불가능합니다.

{{< alert "circle-info" >}}
목표가 단순히 디버깅 목적의 수동 Wi-Fi 트래픽 캡처(보안 테스트가 아님)라면, macOS에서는 Option 키를 누른 채 메뉴 막대의 Wi-Fi 아이콘을 클릭하여 진단 모드로 진입할 수 있습니다. 이는 제대로 된 모니터 모드 워크플로를 대체하지 못합니다.
{{< /alert >}}

보안 테스트, 즉 네트워크 스캔, WPA 핸드셰이크 캡처, 디인증(deauthentication) 공격 실행, 인젝션 테스트 등을 위해서는 macOS에서 USB 패스스루를 사용하는 Kali Linux VM 설정이 필수입니다.

---

## Apple Silicon(M1/M2/M3) vs Intel Mac

Mac의 아키텍처에 따라 필요한 Kali Linux 이미지와 사용 가능한 하이퍼바이저가 결정됩니다. 이는 보안 테스트 VM을 설정하는 macOS 사용자가 가장 흔하게 혼란을 겪는 지점입니다.

<strong>Intel Mac(x86_64):</strong>
VMware Fusion, Parallels Desktop, VirtualBox 세 가지 주요 하이퍼바이저 모두 Intel Mac에서 네이티브로 실행됩니다. 공식 kali.org 다운로드 페이지에서 표준 <strong>Kali Linux x86_64 ISO</strong>를 사용할 수 있습니다. VM 내부의 드라이버 컴파일은 아키텍처가 일치하므로 온라인의 모든 Kali 가이드에 문서화된 것과 동일한 단계를 따릅니다.

<strong>Apple Silicon(M1/M2/M3):</strong>
Apple Silicon은 ARM64입니다. 표준 x86_64 Kali ISO는 하이퍼바이저 내부라 하더라도 Apple Silicon 하드웨어에서 부팅되지 않습니다. VM 수준에는 x86 에뮬레이션 계층이 없기 때문입니다(Rosetta는 전체 OS 가상화가 아니라 사용자 공간 macOS 애플리케이션에만 적용됩니다). [kali.org/get-kali](https://www.kali.org/get-kali/)의 Apple Silicon / ARM 섹션에서 제공되는 <strong>Kali Linux ARM64</strong> 이미지를 사용해야 합니다.

| 하이퍼바이저 | Intel Mac | Apple Silicon |
|---|---|---|
| VMware Fusion 13+ | ✅ 무료 개인 라이선스 | ✅ ARM64 VM 지원 |
| Parallels Desktop 19+ | ✅ | ✅ 최고의 Apple Silicon 성능 |
| VirtualBox 7.x | ✅ | ⚠️ Apple Silicon에서 실험적 |

{{< alert "triangle-exclamation" >}}
VirtualBox의 Apple Silicon 지원은 여전히 실험적으로 표시되어 있습니다. 특히 USB 패스스루는 M 칩 Mac에서 알려진 문제가 있습니다. 보안 테스트 워크플로의 경우 Apple Silicon 하드웨어에서는 VMware Fusion 또는 Parallels Desktop을 사용하시기 바랍니다.
{{< /alert >}}

<strong>USB 패스스루는 아키텍처에 영향을 받지 않습니다:</strong> ALFA 어댑터 자체는 USB 장치입니다. 호스트 CPU가 x86_64인지 ARM64인지는 USB 패스스루 작동 방식에 영향을 주지 않습니다. 어댑터는 USB 버스를 통해 게스트 VM으로 전달되며, Kali 내부의 드라이버가 이를 처리합니다. 아키텍처는 사용하는 Kali 이미지와 VM 내부에서 드라이버가 컴파일되는 방식에만 영향을 줍니다.

---

## 옵션 A: VMware Fusion USB 패스스루

VMware Fusion은 Fusion 13부터 개인용으로 무료로 제공되며, 비용 없이 견고한 USB 패스스루 지원을 원하는 macOS 사용자에게 기본 권장 옵션입니다.

### 1단계 — VMware Fusion 13+ 설치

[vmware.com/products/fusion.html](https://www.vmware.com/products/fusion.html)에서 VMware Fusion을 다운로드합니다. 설치 중에 <strong>시스템 환경설정 → 보안 및 개인정보 보호 → 일반</strong>에서 VMware 시스템 확장을 허용하라는 메시지가 표시됩니다. 이 확장 승인은 USB 패스스루가 작동하는 데 필수적이며, 이것이 없으면 VMware는 macOS USB 스택에서 USB 이벤트를 가로챌 수 없습니다.

승인 후 macOS가 재시작을 요구할 수 있습니다. 계속 진행하기 전에 재시작을 완료하시기 바랍니다.

### 2단계 — Kali Linux VM 생성

- <strong>Apple Silicon Mac:</strong> kali.org에서 Kali Linux ARM64 설치 ISO 또는 사전 빌드된 Parallels/VMware ARM 이미지를 다운로드합니다. VMware Fusion에서 새 VM을 생성하고 ARM64 ISO를 선택합니다.
- <strong>Intel Mac:</strong> 표준 Kali Linux x86_64 설치 ISO를 다운로드합니다. 새 VM을 생성하고 해당 ISO를 설치 미디어로 선택합니다.

작동 가능한 Kali 설치를 위해 최소 <strong>4 GB RAM</strong>과 <strong>40 GB 디스크</strong>를 할당하시기 바랍니다. Kali 설정 중에 무선 도구(aircrack-ng, airmon-ng, airodump-ng)를 기본으로 포함하도록 전체 기본 패키지 세트를 설치합니다.

### 3단계 — USB 패스스루로 ALFA 어댑터 연결

Kali VM이 실행 중이고 ALFA 어댑터를 Mac의 USB 포트에 연결한 상태에서:

1. VMware Fusion에 다음 팝업이 표시됩니다: <strong>"A USB device is requesting permission to connect to your virtual machine."</strong>
2. <strong>Connect to [VM Name]</strong>을 클릭하여 어댑터를 Kali VM으로 직접 전달합니다.
3. 이 시점에서 macOS는 어댑터를 더 이상 인식하지 못합니다. 이제 어댑터는 VM이 독점적으로 소유합니다.

{{< alert "circle-info" >}}
팝업이 나타나지 않는 경우(예: VM 시작 전에 어댑터가 이미 연결되어 있었거나 팝업을 닫은 경우), VMware Fusion 메뉴 막대에서 <strong>Virtual Machine → USB & Bluetooth → [ALFA 어댑터 이름] → Connect (Disconnect from Mac)</strong>로 이동합니다. 이렇게 하면 USB 장치가 수동으로 VM에 재할당됩니다.
{{< /alert >}}

### 4단계 — Kali 내부에서 확인

Kali VM에서 터미널을 열고 어댑터가 보이는지 확인합니다:

```bash
lsusb | grep -i mediatek
# AWUS036AXML / MT7921AUN: Bus 001 Device 002: ID 0e8d:7961 MediaTek Inc. ...

lsusb | grep -i realtek
# AWUS036ACH / RTL8812AU: Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. ...
```

두 명령 모두 출력이 없다면 패스스루가 완료되지 않은 것입니다. VMware 장치 메뉴를 다시 확인하시기 바랍니다.

### 5단계 — 드라이버 로드 및 모니터 모드 확인

MT7921AUN(AWUS036AXML)의 경우 드라이버가 Kali 커널에 내장되어 있습니다. RTL8812AU 어댑터의 경우 드라이버 설치가 필요합니다. [드라이버 설치 가이드](/ko/blog/install-alfa-driver-kali-ubuntu/)를 참조하시기 바랍니다. 드라이버가 활성화되면:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
```

airodump-ng의 실시간 스캔 출력은 패스스루, 드라이버 로드, 모니터 모드가 모두 올바르게 작동하고 있음을 확인해 줍니다.

---

## 옵션 B: Parallels Desktop USB 패스스루

Parallels Desktop은 성능이 우선순위인 Apple Silicon Mac에서 선호되는 하이퍼바이저입니다. 무료가 아니며 구독 라이선스가 필요하지만, ARM64 VM 지원과 USB 패스스루 구현이 Apple Silicon 하드웨어에서 VMware Fusion보다 더 성숙합니다.

### 1단계 — Parallels Desktop 19+

[parallels.com](https://www.parallels.com)에서 Parallels Desktop을 설치합니다. VMware Fusion과 동일한 시스템 확장 승인 절차가 적용됩니다. <strong>보안 및 개인정보 보호</strong>에서 Parallels 시스템 확장을 허용하고 메시지가 표시되면 재시작합니다.

### 2단계 — Kali Linux ARM64 VM 생성

Apple Silicon에서 Parallels는 ARM64 게스트 OS 이미지에서만 작동합니다. kali.org에서 Kali Linux ARM64 이미지를 다운로드하고 해당 이미지를 사용하여 Parallels에서 새 VM을 생성합니다.

{{< alert "circle-info" >}}
Parallels Desktop 19 이상은 Apple Silicon에서 새 VM 어시스턴트를 통해 Kali Linux ARM을 직접 다운로드하고 설치할 수 있습니다. ISO를 수동으로 다운로드할 필요가 없을 수 있습니다.
{{< /alert >}}

Intel Mac에서는 표준 x86_64 Kali ISO가 수정 없이 Parallels에서 작동합니다.

### 3단계 — USB로 ALFA 어댑터 연결

Kali VM이 실행 중이고 ALFA 어댑터를 연결한 상태에서:

1. macOS 메뉴 막대에서 <strong>Devices → USB & Bluetooth</strong>로 이동합니다.
2. 목록에서 ALFA 어댑터를 찾습니다(<strong>Realtek 802.11ac NIC</strong>, <strong>MediaTek Wi-Fi</strong> 등으로 표시될 수 있습니다).
3. 어댑터를 클릭하고 <strong>Connect to Linux</strong>(또는 VM 이름)를 선택합니다.

Parallels가 어댑터를 macOS에서 분리하고 Kali VM에 독점적으로 전달합니다.

### 4단계 — lsusb로 확인

Kali VM 터미널 내부에서:

```bash
lsusb
ip link show
```

ALFA 어댑터는 `lsusb` 출력과 `ip link show`의 새 `wlan` 인터페이스 모두에 나타나야 합니다. 인터페이스가 보이지 않으면 Parallels Devices 메뉴를 통해 장치를 다시 연결하시기 바랍니다.

{{< alert "circle-info" >}}
Apple Silicon의 Parallels는 I/O 집약적 VM 워크로드에서 VMware Fusion을 지속적으로 능가합니다. 장시간 airodump-ng 세션을 실행하거나 무거운 패킷 캡처를 수행하는 경우 Parallels가 일반적으로 더 낮은 CPU 오버헤드를 제공합니다.
{{< /alert >}}

---

## Apple Silicon의 Kali: ARM64 드라이버 참고 사항

Apple Silicon의 VM 내부에서 Kali ARM64를 실행하면 드라이버 컴파일 환경이 바뀝니다. 대부분의 온라인 가이드는 x86_64를 가정하지만 단계는 거의 동일합니다. 핵심 차이점은 어떤 패키지가 사전 설치되어 있는지와 DKMS가 ARM 커널 헤더를 처리하는 방식입니다.

<strong>ARM64의 RTL8812AU:</strong>
[aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au)의 RTL8812AU 드라이버는 ARM64에서 올바르게 컴파일됩니다. DKMS 빌드 프로세스는 x86_64와 동일합니다. 저장소를 클론하고 `dkms` 명령을 실행하면 모듈이 ARM64 커널 헤더에 맞춰 빌드됩니다:

```bash
sudo apt update && sudo apt install -y dkms linux-headers-$(uname -r) build-essential
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

컴파일에는 몇 분이 걸릴 수 있습니다. 결과 모듈은 사용자의 ARM64 커널에 특화된 아키텍처별 모듈입니다.

<strong>ARM64의 MT7921AUN:</strong>
`mt7921u` 드라이버는 <strong>Linux 5.18부터 커널에 내장</strong>되어 있으며 Kali ARM64 2024.x 이상에 포함되어 있습니다. Kali ARM64에서 AWUS036AXML은 수동 컴파일이 필요하지 않습니다. 어댑터는 USB 패스스루 후 자동으로 인식됩니다.

```bash
dmesg | grep mt7921
# [ 4.123456] mt7921u 1-1:1.0: HW/SW Version: 0x8a108a10, Build Time: ...
```

<strong>M 칩 Mac을 위한 권장 사항:</strong> Apple Silicon Mac에서 VM 내 Kali와 함께 사용하기 위해 ALFA 어댑터를 구매하려는 경우, <strong>AWUS036AXML(MT7921AUN)</strong>이 더 나은 선택입니다. 커널 내장 드라이버 덕분에 DKMS 컴파일 단계가 완전히 제거되며 ARM64 Kali 빌드에서 안정적으로 작동합니다. AWUS036ACH도 작동하지만 RTL8812AU 트리 외부(out-of-tree) 드라이버가 필요하여 커널 헤더 가용성에 대한 유지보수 의존성이 추가됩니다. 다만 인젝션은 커널 버전에 따라 다릅니다. kernel 6.16 이전에서는 인젝션이 동작한다는 커뮤니티 보고가 있지만, stock kernel 6.16 이상(6.17에서 실측)에서는 AXML의 패킷 인젝션 테스트(`aireplay-ng --test`: Found 0 APs / No Answer)가 실패하여 deauth 및 핸드셰이크 캡처가 불가능합니다. 원인은 칩 자체의 한계가 아니라 mac80211 chanctx 회귀이며, 커뮤니티 patched 드라이버로 인젝션이 동작하더라도 펌웨어가 전송 속도를 고정합니다(1/6 Mbps, HT/VHT 인젝션 불가). 모니터 모드, AP, WPA3는 영향이 없습니다. 인젝션이 필요하면 AWUS036ACH 또는 AWUS036EACS를 선택하세요.

---

## 모니터 모드 및 인젝션 테스트

VMware Fusion 또는 Parallels로 USB 패스스루를 완료한 후, 다음 명령 시퀀스를 실행하여 USB 인식부터 모니터 모드 활성화까지 전체 스택이 작동하는지 확인합니다:

```bash
# 1. USB 장치가 보이는지 확인
lsusb

# 2. 무선 인터페이스 목록 확인
ip link show

# 3. 충돌하는 프로세스 종료 (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# 4. 무선 인터페이스에서 모니터 모드 시작
sudo airmon-ng start wlan1

# 5. 모니터 인터페이스가 생성되었는지 확인
ip link show wlan1mon

# 6. 수동 스캔 시작
sudo airodump-ng wlan1mon
```

SSID, BSSID, 채널, 클라이언트 장치를 보여주는 성공적인 airodump-ng 출력은 USB 패스스루, 드라이버 로드, 모니터 모드, 패킷 수신이 모두 엔드투엔드로 작동하고 있음을 확인해 줍니다.

<strong>패스스루 후에도 `wlan1`이 나타나지 않는 경우:</strong>

1. Mac에서 ALFA 어댑터를 분리합니다.
2. 5초 동안 기다린 후 다시 연결합니다.
3. 하이퍼바이저의 USB 장치 메뉴를 통해 VM에 재할당합니다(VMware Fusion에서는 Virtual Machine → USB & Bluetooth, Parallels에서는 Devices → USB & Bluetooth).
4. Kali 내부에서 `lsusb`를 다시 실행하여 장치가 나타나는지 확인합니다.

{{< alert "triangle-exclamation" >}}
VM 내부의 기본 `wlan0` 인터페이스에서 `airmon-ng start wlan0`을 시도하지 마십시오. 해당 인터페이스는 일반적으로 패스스루된 ALFA 어댑터가 아니라 인터넷 연결에 사용되는 VMware/Parallels 가상 네트워크 어댑터입니다. 잘못된 인터페이스를 사용하면 ALFA 어댑터에서 모니터 모드를 활성화하지 못한 채 VM의 네트워크 연결이 끊깁니다.
{{< /alert >}}

---

## 성능 및 제한 사항

<strong>USB 패스스루 지연:</strong> 하이퍼바이저 계층을 통해 USB 장치를 전달하면 베어메탈 Linux에서 어댑터를 사용하는 경우에 비해 약 1~2 ms의 처리 지연이 추가됩니다. 패킷 캡처, 핸드셰이크 수집, 인젝션 테스트 등 802.11 보안 테스트 목적에서는 이 지연이 운영상 유의미하지 않습니다. 이는 실시간 지연이 중요한 애플리케이션에서만 문제가 되는데, 보안 테스트는 그러한 범주에 속하지 않습니다.

<strong>독점적 소유:</strong> macOS는 ALFA 어댑터를 Kali VM과 동시에 공유할 수 없습니다. 어댑터가 VM으로 패스스루되면 macOS에서 완전히 사라집니다. 어댑터를 macOS로 되돌리려면(예: 일반 Wi-Fi 어댑터로 사용) 하이퍼바이저의 USB 장치 메뉴를 통해 VM에서 분리한 후 어댑터를 뽑았다가 다시 연결합니다. macOS가 이를 표준 인터페이스로 다시 인식합니다.

<strong>전력 소비:</strong> 자체 Wi-Fi 라디오도 함께 실행 중인 Mac에서 VM 내부로 USB Wi-Fi 어댑터(최대 100 mW의 RF 에너지를 송출)를 실행하는 것은 적지 않은 전력 소모입니다. 장시간 airodump-ng 세션이나 패킷 인젝션 테스트는 일반 작동보다 MacBook 배터리를 훨씬 빠르게 소모시킬 수 있습니다. 특히 배터리 관리가 열 설계와 긴밀하게 통합된 Apple Silicon MacBook에서는 <strong>장시간 테스트 세션 중에 충전기를 사용</strong>하시기 바랍니다.

<strong>테스트 전 VM 스냅샷:</strong> VMware Fusion과 Parallels는 모두 VM 스냅샷을 지원합니다. 테스트 세션 전에 깨끗하게 구성된 Kali 설치의 스냅샷을 찍어두면 드라이버 업데이트나 구성 변경으로 문제가 발생했을 때 알려진 양호한 상태로 롤백할 수 있습니다.

---

## 문제 해결

| 증상 | 가능한 원인 | 해결책 |
|---|---|---|
| ALFA 어댑터가 하이퍼바이저 USB 메뉴에 나타나지 않음 | macOS 시스템 확장이 승인되지 않음 | <strong>시스템 환경설정 → 보안 및 개인정보 보호 → 일반</strong> → VMware / Parallels 확장 허용 후 재시작 |
| Kali VM 내부의 `lsusb`에 ALFA 어댑터가 표시되지 않음 | USB 패스스루가 완료되지 않음 | VM → USB & Bluetooth 메뉴를 통해 수동 연결, 어댑터 재연결 |
| 패스스루 후 `wlan1` 인터페이스 누락 | 드라이버가 로드되지 않음(RTL8812AU) | DKMS를 통해 RTL8812AU 드라이버 설치, [드라이버 설치 가이드](/ko/blog/install-alfa-driver-kali-ubuntu/) 참조 |
| `airmon-ng start wlan1`이 "Operation not permitted"로 실패 | NetworkManager가 인터페이스를 점유 중 | 먼저 `sudo airmon-ng check kill` 실행 후 재시도 |
| 모니터 모드는 시작되지만 airodump-ng에 네트워크가 표시되지 않음 | 잘못된 채널 또는 인터페이스 | `ip link show`로 `wlan1mon` 존재 확인, `sudo airodump-ng --band abg wlan1mon` 시도 |
| ALFA 어댑터 연결 시 VM 멈춤 | USB 컨트롤러 충돌(VMware) | VM 종료, VM Settings → USB로 이동, 컨트롤러를 USB 3.0에서 USB 2.0으로 전환, VM 재시작 |

{{< alert "circle-info" >}}
특히 Apple Silicon에서 ALFA 어댑터는 인식되지만 Kali에 인터페이스가 나타나지 않는 경우, 연결 직후 `dmesg | tail -30`을 확인하시기 바랍니다. 출력을 통해 커널이 장치를 감지하고 있는지, 그리고 어떤 드라이버가 바인딩을 시도하고 있는지 알 수 있습니다.
{{< /alert >}}

---

{{< faq >}}

## 관련 가이드

VirtualBox 또는 VMware Workstation을 사용하는 Windows 및 Linux 호스트의 경우, 관련 가이드를 참조하시기 바랍니다: [ALFA 어댑터 USB 패스스루: VirtualBox 및 VMware 설정 가이드](/ko/blog/alfa-adapter-virtualbox-vmware-usb/).

본 가이드 전반에서 권장하는 AWUS036AXML의 어댑터별 세부 정보(6 GHz 대역 성능 벤치마크 및 드라이버 버전 참고 사항 포함)는 전체 리뷰를 참조하시기 바랍니다: [ALFA AWUS036AXML WiFi 6E 리뷰](/ko/blog/awus036axml-wifi-6e-review/).

## 참고 자료

1. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
2. [Kali Linux 공식 다운로드](https://www.kali.org/get-kali/)
3. [VMware Fusion 제품 페이지](https://www.vmware.com/products/fusion.html)
4. [Parallels Desktop 공식 웹사이트](https://www.parallels.com/)
5. [aircrack-ng rtl8812au 드라이버 프로젝트](https://github.com/aircrack-ng/rtl8812au)
