---
title: "ALFA 어댑터 USB 패스스루: VirtualBox 및 VMware 설정 가이드"
description: "Kali Linux용 VirtualBox 및 VMware Workstation에서 ALFA USB WiFi 어댑터 USB 패스스루를 수행하는 단계별 가이드. AWUS036ACH, AWUS036AXML, USB 3.0 필터, Extension Pack, 문제 해결을 다룹니다."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "VirtualBox에서 ALFA 어댑터를 사용하려면 Extension Pack이 필요합니까?"
    answer: "네. VirtualBox는 USB 2.0 및 USB 3.0 패스스루를 위해 Extension Pack이 필요합니다. 이것이 없으면 USB 1.1만 사용할 수 있으며, 이는 최신 ALFA 어댑터에 충분하지 않습니다."
  - question: "ALFA 어댑터에 USB 2.0과 USB 3.0 컨트롤러 중 무엇을 사용해야 합니까?"
    answer: "AWUS036AXML은 USB 3.0(xHCI)을 사용해야 합니다. AWUS036ACH는 USB 2.0 장치이지만 xHCI에서도 문제없이 작동합니다. 모든 것을 USB 3.0으로 설정하는 것을 권장합니다."
  - question: "VMware Workstation에는 추가 확장이 필요합니까?"
    answer: "아니요. VMware Workstation 17 이상과 Fusion 13 이상은 USB 2.0/3.0 지원이 내장되어 있습니다. USB 중재자(arbiter) 서비스가 실행 중인지만 확인하면 됩니다."
  - question: "lsusb에는 어댑터가 표시되는데 wlan 인터페이스가 없는 이유는 무엇입니까?"
    answer: "USB 패스스루는 성공했지만 드라이버가 로드되지 않은 것입니다. RTL8812AU는 modprobe 88XXau 또는 realtek-rtl88xxau-dkms 패키지가 필요합니다. MT7921AUN은 modprobe mt7921u가 필요합니다."
  - question: "Linux 호스트에서 USB 어댑터가 계속 연결이 끊기면 어떻게 해야 합니까?"
    answer: "echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend를 실행하여 USB 자동 절전을 비활성화하고, 사용자가 vboxusers 그룹에 속해 있는지 확인하시기 바랍니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "alfa-network", "AWUS036ACH", "AWUS036AXML"]
featureimage: "/images/blog/alfa-adapter-virtualbox-vmware-usb.webp"
---

가상 머신 내부에서 ALFA WiFi 어댑터를 실행하는 것은 단순히 연결하고 게스트 OS가 인식하기를 바라는 것만큼 간단하지 않습니다. 공유 폴더나 브리지 네트워킹과 달리, 모니터 모드와 원시 패킷 인젝션에는 <strong>완전한 USB 제어</strong>가 필요합니다. VM은 호스트의 네트워크 스택을 통해 장치를 공유하는 것이 아니라 USB 장치를 독점적으로 소유해야 합니다. 이를 USB 패스스루라고 하며, 이를 올바르게 구성하는 것은 VM에서 작업하는 침투 테스터와 CTF 참가자에게 가장 흔한 설정 실패 지점입니다.

{{< tldr >}}
VirtualBox나 VMware에서 ALFA 어댑터를 사용하려면 USB 패스스루 구성이 필요합니다. VirtualBox는 USB 3.0이 활성화된 Extension Pack이 필요합니다. VMware는 USB 지원이 내장되어 있지만 중재자 서비스가 실행 중이어야 합니다. AWUS036ACH는 88XXau 드라이버를, AWUS036AXML은 mt7921u 드라이버를 사용합니다.
{{< /tldr >}}




본 가이드는 Kali Linux를 게스트 OS로 하여 <strong>VirtualBox 7.x</strong> 및 <strong>VMware Workstation 17+ / VMware Fusion 13+</strong>의 전체 패스스루 설정을 다룹니다. AWUS036ACH(RTL8812AU 칩셋)와 최신 AWUS036AXML(MT7921AUN 칩셋)을 모두 다루며, 동작이 다른 부분에는 어댑터별 참고 사항을 포함합니다.

완료되면 ALFA 어댑터가 `lsusb`를 통해 Kali 내부에 나타나고, 올바른 드라이버가 로드되며, `airmon-ng`이 모니터 모드가 작동함을 확인해 줍니다.

---

## 사전 요구사항

시작하기 전에 환경이 아래 요구사항과 일치하는지 확인하시기 바랍니다. 특히 VirtualBox Extension Pack 중 하나라도 누락되면 대부분의 패스스루 실패의 근본 원인이 됩니다.

| 요구사항 | 세부 내용 |
|---|---|
| <strong>하이퍼바이저</strong> | VirtualBox 7.x + Extension Pack <strong>또는</strong> VMware Workstation 17+ / Fusion 13+ |
| <strong>게스트 OS</strong> | Kali Linux 2024.x 이상(2024.1~2025.1에서 테스트) |
| <strong>ALFA 어댑터</strong> | AWUS036ACH, AWUS036AXML, AWUS036ACM, 또는 모든 RTL8812AU / MT7921AUN 장치 |
| <strong>호스트 USB 포트</strong> | USB 3.0 권장(특히 AWUS036AXML의 경우) |
| <strong>호스트 OS</strong> | Windows 10/11, Linux, 또는 macOS(Fusion) |
| <strong>Sudo 접근</strong> | Kali VM 내부에서 필요 |

{{< alert "circle-info" >}}
아직 Kali 내부에 드라이버를 설치하지 않았다면, 먼저 본 가이드의 USB 패스스루 단계를 완료하시기 바랍니다. 어댑터가 VM 내부에서 보이면, [ALFA 드라이버 설치 가이드](/ko/blog/install-alfa-driver-kali-ubuntu/)에 따라 올바른 드라이버를 컴파일하고 로드합니다.
{{< /alert >}}

---

## VirtualBox USB 패스스루 — 단계별 안내

VirtualBox는 USB 2.0 및 USB 3.0 패스스루를 지원하기 위해 추가 구성 요소인 <strong>Extension Pack</strong>이 필요합니다. 이것이 없으면 USB 1.1(OHCI)만 사용할 수 있으며, 이는 최신 ALFA 어댑터에 충분하지 않습니다.

### VirtualBox Extension Pack 설치

1. [virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)를 엽니다.
2. <strong>VirtualBox Extension Pack</strong> 아래에서 <strong>All supported platforms</strong>를 클릭하여 `.vbox-extpack` 파일을 다운로드합니다. 버전은 설치된 VirtualBox 버전과 정확히 일치해야 합니다.
3. VirtualBox를 열고 <strong>File → Preferences → Extensions</strong>(macOS: <strong>VirtualBox → Settings → Extensions</strong>)로 이동합니다.
4. <strong>+</strong> 아이콘을 클릭하고 다운로드한 `.vbox-extpack`를 찾아 설치합니다. 메시지가 표시되면 라이선스에 동의합니다.

명령줄에서 Extension Pack이 활성화되어 있는지 확인하려면:

```bash
VBoxManage list extpacks
```

예상 출력:

```
Extension Packs: 1
Pack no. 0:   Oracle VirtualBox Extension Pack
Version:      7.0.x
...
Usable:       true
```

{{< alert "triangle-exclamation" >}}
<strong>Usable</strong> 필드가 `false`로 표시되면 Extension Pack 버전이 VirtualBox 버전과 일치하지 않는 것입니다. 올바른 버전을 제거하고 다시 설치하시기 바랍니다.
{{< /alert >}}

### 사용자를 vboxusers 그룹에 추가(Linux 호스트 전용)

Linux 호스트에서는 USB 장치에 접근하려면 사용자 계정이 `vboxusers` 그룹의 구성원이어야 합니다.

```bash
sudo usermod -aG vboxusers $USER && newgrp vboxusers
```

이를 실행한 후 그룹 변경 사항이 적용되도록 <strong>로그아웃 후 다시 로그인</strong>(또는 재부팅)합니다. 다음으로 확인할 수 있습니다:

```bash
groups $USER
```

출력에 `vboxusers`가 포함되어야 합니다.

### VM 설정에서 USB 컨트롤러 활성화

1. Kali VM이 실행 중이면 종료합니다.
2. VM을 선택하고 <strong>Settings → USB</strong>를 클릭합니다.
3. <strong>Enable USB Controller</strong>를 체크합니다.
4. 라디오 버튼에서 <strong>USB 3.0 (xHCI) Controller</strong>를 선택합니다.

{{< alert "circle-info" >}}
AWUS036AXML에는 USB 3.0(xHCI)이 필요합니다. AWUS036ACH의 경우 어댑터 자체가 USB 2.0이므로 USB 2.0(EHCI)이 기술적으로 충분하지만, xHCI를 사용해도 무해하며 구성의 일관성을 유지할 수 있습니다.
{{< /alert >}}

### USB 장치 필터 추가

USB 장치 필터는 매 세션마다 수동 개입 없이 ALFA 어댑터가 연결될 때마다 자동으로 캡처하도록 VirtualBox에 지시합니다.

1. 동일한 <strong>Settings → USB</strong> 패널에서 <strong>+</strong> 아이콘(Add USB filter from device)을 클릭합니다.
2. ALFA 어댑터가 아직 연결되어 있지 않다면 지금 연결합니다. VirtualBox가 드롭다운에 표시합니다.
3. 장치를 선택합니다. 일반적으로 <strong>"Realtek 802.11ac NIC"</strong>(AWUS036ACH) 또는 <strong>"MediaTek Corp. 802.11 b/g/n"</strong>(AWUS036AXML)으로 나타납니다.
4. <strong>OK</strong>를 클릭하여 저장합니다.

필터는 벤더 및 제품 ID를 저장합니다. 다음에 어댑터를 연결한 상태로 VM이 부팅되면 VirtualBox가 자동으로 패스스루합니다.

### VM 시작 및 lsusb로 확인

Kali VM을 시작합니다. 데스크톱이 로드되면 터미널을 열고 실행합니다:

```bash
lsusb
```

다음과 유사한 줄이 보여야 합니다:

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

또는 AWUS036AXML의 경우:

```
Bus 002 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

장치가 나타나지 않으면 이 섹션 끝의 문제 해결 표를 참조하시기 바랍니다.

### 드라이버 로드

<strong>AWUS036ACH(RTL8812AU):</strong>

```bash
sudo modprobe 88XXau
```

실패하는 경우(모듈을 찾을 수 없음) 먼저 DKMS 패키지를 설치합니다:

```bash
sudo apt update && sudo apt install -y realtek-rtl88xxau-dkms
sudo modprobe 88XXau
```

<strong>AWUS036AXML(MT7921AUN):</strong>

```bash
sudo modprobe mt7921u
```

MT7921AUN 드라이버는 5.18부터 메인라인 커널에 포함되어 있습니다. Kali 2024.x는 이를 포함할 만큼 새로운 커널을 제공하지만 펌웨어가 추가로 필요할 수 있습니다:

```bash
sudo apt install -y firmware-misc-nonfree
```

### 모니터 모드 확인

드라이버가 로드된 상태에서 인터페이스 이름을 확인합니다:

```bash
ip link show
```

`wlan0`, `wlan1` 또는 유사한 이름의 인터페이스를 찾습니다. 그런 다음 모니터 모드를 활성화합니다:

```bash
sudo airmon-ng start wlan1
```

성공적인 출력은 모니터 인터페이스 이름(예: `wlan1mon`)으로 끝납니다. 확인합니다:

```bash
sudo iwconfig wlan1mon
```

<strong>Mode</strong> 필드는 `Monitor`로 표시되어야 합니다.

### VirtualBox 일반적인 오류

| 오류 | 원인 | 해결 |
|---|---|---|
| USB 설정에 "No USB devices available" | Extension Pack 미설치 또는 버전 불일치 | 일치하는 Extension Pack 버전 설치 |
| 어댑터가 캡처되지 않음 / lsusb에 보이지 않음 | 사용자가 `vboxusers` 그룹에 없음(Linux 호스트) | `sudo usermod -aG vboxusers $USER` 후 로그아웃/로그인 |
| "USB device is busy with a previous request" | 호스트의 다른 프로세스가 장치를 사용 중 | VM 시작 전에 어댑터를 뽑았다가 다시 연결 |
| VM 내부에서 장치가 계속 끊김 | USB 3.0 컨트롤러 미활성화, VM이 OHCI 사용 중 | VM Settings → USB에서 USB 3.0(xHCI)으로 전환 |
| 필터를 추가했지만 장치가 자동 캡처되지 않음 | Extension Pack 설치 전에 필터 생성됨 | Extension Pack 설치 후 필터 삭제 및 재추가 |

---

## VMware Workstation / VMware Fusion USB 패스스루

VMware는 VirtualBox와 다른 방식으로 USB 패스스루를 처리합니다. 설치할 별도의 확장이 없습니다. USB 2.0 및 3.0 지원은 VMware Workstation 17 이상과 Fusion 13 이상에 내장되어 있습니다. 주요 메커니즘은 호스트 USB 이벤트를 모니터링하고 장치를 VM으로 라우팅하는 <strong>USB 중재자(arbitrator) 서비스</strong>입니다.

### 장치 메뉴를 통해 어댑터 연결

VM이 실행 중일 때 ALFA 어댑터를 연결하면, VMware는 일반적으로 어느 VM이 장치를 소유해야 하는지 묻는 팝업을 표시합니다. 팝업을 놓친 경우:

1. Kali VM이 실행 중인 상태에서 메뉴 막대의 <strong>VM → Removable Devices</strong>로 이동합니다.
2. 목록을 펼치고 ALFA 어댑터(예: <strong>Realtek 802.11ac NIC</strong>)를 찾습니다.
3. <strong>Connect (Disconnect from Host)</strong>를 클릭합니다.

장치가 호스트 OS에서 분리되어 VM에 독점적으로 사용 가능해집니다.

### VMware Fusion(macOS)

VMware Fusion이 설치된 macOS에서:

1. <strong>Virtual Machine → USB & Bluetooth</strong>로 이동합니다.
2. 목록에서 ALFA 어댑터를 찾습니다.
3. 연결을 <strong>Connect to Linux</strong>(또는 Kali VM 이름)로 전환합니다.

또는 Fusion의 VM Settings에서 <strong>USB & Bluetooth</strong> 아래 <strong>Automatically connect new USB devices</strong>를 활성화하여 Fusion이 메시지 없이 활성 VM에 장치를 패스스루하도록 할 수 있습니다.

### 확인 및 드라이버 로드

연결되면 Kali 내부에서 확인합니다:

```bash
lsusb
```

그런 다음 위의 VirtualBox 섹션에 설명된 대로 적절한 드라이버를 로드합니다(3.6 및 3.7 단계가 동일하게 적용됩니다).

### VMware USB 중재자 서비스 확인

ALFA 어댑터가 <strong>Removable Devices</strong> 메뉴에 나타나지 않으면 USB 중재자 서비스가 실행되고 있지 않을 수 있습니다. Linux 호스트에서:

```bash
sudo systemctl status vmware-usbarbitrator
```

중지된 경우:

```bash
sudo systemctl start vmware-usbarbitrator
sudo systemctl enable vmware-usbarbitrator
```

Windows 호스트에서는 <strong>서비스</strong>(`services.msc`)를 열고 <strong>VMware USB Arbitration Service</strong>를 찾아 <strong>자동(시작)</strong>으로 설정합니다.

### VMware에서 USB 3.0 활성화

AWUS036AXML 및 기타 USB 3.0 장치의 경우, VM 하드웨어 버전이 xHCI를 지원하는지 확인합니다. Kali VM의 `.vmx` 파일(VM 폴더에 위치)을 열고 다음을 확인하거나 추가합니다:

```
usb_xhci.present = "TRUE"
```

VMware Workstation GUI에서: <strong>VM → Settings → USB Controller</strong>로 이동하여 드롭다운에서 <strong>USB 3.1</strong>을 선택합니다. 이 설정을 변경하려면 VM의 전원이 꺼져 있어야 합니다.

{{< alert "triangle-exclamation" >}}
USB 3.0(xHCI) 지원에는 VMware 하드웨어 버전 14 이상이 필요합니다. VM이 구형 하드웨어 버전으로 생성된 경우 <strong>VM → Manage → Change Hardware Compatibility</strong>를 통해 업그레이드하시기 바랍니다.
{{< /alert >}}

### VMware 일반적인 오류

| 오류 | 원인 | 해결 |
|---|---|---|
| Removable Devices 메뉴에 어댑터가 없음 | USB 중재자가 실행되지 않음 | `vmware-usbarbitrator` 서비스 시작 |
| 장치가 연결되었다가 즉시 끊김 | 호스트 OS 드라이버가 장치를 다시 가져감 | 어댑터에 대한 호스트 WiFi 드라이버 비활성화, 또는 더 빠르게 뽑았다가 다시 연결 |
| "Device already in use by host" | 호스트 OS가 장치를 점유함 | VM에서 연결하기 전에 호스트에서 꺼내기(예: 호스트 네트워크 어댑터 비활성화) |
| VM 내부에서 USB 3.0 속도가 나오지 않음 | VM 하드웨어 버전 < 14 또는 xHCI 미활성화 | 하드웨어 버전 업그레이드, .vmx에 `usb_xhci.present = "TRUE"` 추가 |
| 패스스루 후에도 모니터 모드 실패 | Kali 내부의 잘못되었거나 누락된 드라이버 | [드라이버 설치 가이드](/ko/blog/install-alfa-driver-kali-ubuntu/) 참조 |

---

## 어댑터별 참고 사항

### AWUS036ACH(RTL8812AU)

AWUS036ACH는 <strong>USB 2.0</strong> 장치이며 VM 환경에서 가장 잘 테스트된 어댑터 중 하나입니다. VirtualBox와 VMware 모두 이를 안정적으로 처리합니다.

- USB 컨트롤러: USB 2.0(EHCI) 또는 USB 3.0(xHCI) 중 어느 것이든 잘 작동합니다.
- 드라이버 패키지: `realtek-rtl88xxau-dkms`(Kali 저장소에서 사용 가능). 모듈 이름: `88XXau`.
- 일부 최신 커널(6.x)에서는 DKMS 패키지에 패치가 필요할 수 있습니다. 최신 상태는 [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) GitHub 페이지를 확인하시기 바랍니다.
- 모니터 모드와 패킷 인젝션은 VM 패스스루에서 매우 안정적입니다.

제품은 당사 스토어에서 확인할 수 있습니다: [ALFA AWUS036ACH](/ko/products/alfa/awus036ach/).

### AWUS036AXML(MT7921AUN)

AWUS036AXML은 WiFi 6E를 지원하는 <strong>USB 3.0</strong> 장치입니다. 더 최신이며 VM 환경에서 일부 엣지 케이스가 있습니다.

- USB 컨트롤러: <strong>반드시</strong> USB 3.0(xHCI)을 사용해야 합니다. USB 2.0 패스스루는 장치가 저하된 성능으로 작동하게 하며 펌웨어 로드 실패를 유발할 수 있습니다.
- 드라이버: `mt7921u`는 메인라인 커널(5.18+)에 포함되어 있습니다. Kali 2024.x에 포함되어 있습니다. 펌웨어 패키지: `firmware-misc-nonfree`.
- <strong>알려진 문제</strong>: 일부 초기 AWUS036AXML 제품은 VirtualBox USB 3.0 중재 하에서 주기적인 멈춤을 겪습니다. `ip link`에서 인터페이스가 사라졌다 다시 나타나는 것이 보이면, 진단 단계로 VirtualBox USB 컨트롤러를 USB 2.0으로 전환해 보시기 바랍니다. 그렇게 해서 안정화된다면 이는 드라이버 문제가 아니라 VirtualBox xHCI 중재 문제입니다.
- VMware Workstation은 USB 3.0 패스스루에서 VirtualBox보다 AWUS036AXML을 더 안정적으로 처리하는 경향이 있습니다.

전체 리뷰: [AWUS036AXML WiFi 6E 리뷰](/ko/blog/awus036axml-wifi-6e-review/).

### AWUS036ACM(MT7612U, 듀얼 안테나)

AWUS036ACM은 커널 내장 드라이버(`mt76x2u`, 커널 4.19부터 메인라인)가 있는 MediaTek MT7612U 칩셋을 사용합니다. 드라이버 설치가 필요 없습니다. 패스스루가 구성되면 어댑터는 VM 내부에서 플러그 앤 플레이로 작동합니다. 모듈이 자동으로 로드되지 않으면 `sudo modprobe mt76x2u`를 실행합니다. AWUS036ACM에는 두 개의 RP-SMA 안테나 포트가 있습니다.

---

## 성능 팁

어댑터를 VM에 연결하는 것이 첫 단계입니다. 실제 침투 테스트나 캡처 세션 중에 안정적인 성능을 얻으려면 몇 가지 추가 튜닝 단계가 필요합니다.

<strong>올바른 USB 필터 유형 사용.</strong> AWUS036AXML의 경우 VirtualBox에서 항상 USB 3.0 필터를 사용하시기 바랍니다(xHCI 컨트롤러가 선택되어 있는지 확인). USB 3.0 장치에 USB 2.0 필터를 사용하면 장치가 USB 2.0 속도로 협상하여 처리량이 절반으로 줄어듭니다.

<strong>호스트에서 USB 자동 절전 비활성화.</strong> Linux 호스트는 USB 장치를 적극적으로 절전 모드로 전환하여 VM이 이를 잃게 할 수 있습니다. 호스트 수준에서 비활성화합니다:

```bash
echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend
```

재부팅 후에도 유지하려면 `/etc/rc.local`에 추가하거나 udev 규칙을 생성합니다.

<strong>적절한 VM 리소스 할당.</strong> 패킷 인젝션 및 캡처 워크로드는 CPU 집약적입니다. 최소한 다음을 할당합니다:
- <strong>CPU 코어 2개</strong>(`hcxdumptool` + `hashcat` 같은 병렬 도구의 경우 4개 권장)
- <strong>RAM 2 GB</strong>(GUI 도구가 있는 전체 Kali 데스크톱을 실행하는 경우 4 GB)

<strong>작업 전 VM 스냅샷 생성.</strong> 침투 테스트 세션을 시작하기 전에 Kali VM의 스냅샷을 찍습니다. 드라이버 충돌이나 잘못된 펌웨어 업데이트로 설정이 손상되면, 스냅샷을 되돌려 몇 초 만에 알려진 양호한 상태로 복구할 수 있습니다.

<strong>어댑터를 시원하게 유지.</strong> 고이득 안테나가 있는 ALFA 어댑터는 지속적인 인젝션 중에 열을 발생시킵니다. VM에서는 호스트 OS가 열 또는 전력 문제를 감지하면 USB 장치를 스로틀링할 수 있습니다. 통풍이 잘 되는 환경에서 어댑터를 사용하시기 바랍니다.

{{< alert "circle-info" >}}
30분보다 긴 캡처 세션의 경우, 어댑터와 호스트 사이에 전원 공급형 USB 허브를 사용하는 것을 고려하시기 바랍니다. 이는 안정적인 전원을 제공하고 중요한 캡처 중에 어댑터가 끊기게 할 수 있는 전압 강하를 방지합니다.
{{< /alert >}}

---

## 베어메탈 vs VM: 솔직한 비교

가상 머신은 어댑터와 커널 사이에 복잡성 계층을 도입합니다. 인프라 결정을 내리는 보안 전문가를 위한 솔직한 평가는 다음과 같습니다:

| 기능 | 베어메탈 Kali | VirtualBox + Kali | VMware + Kali |
|---|---|---|---|
| <strong>드라이버 지원</strong> | 완전, 직접 | 양호(Extension Pack 사용) | 양호(내장 USB) |
| <strong>모니터 모드 안정성</strong> | 우수 | 양호 | 양호~우수 |
| <strong>패킷 인젝션 신뢰성</strong> | 우수 | 양호(간헐적 프레임 손실) | 양호~우수 |
| <strong>USB 3.0 처리량</strong> | 최대 속도 | 거의 최대 | 거의 최대 |
| <strong>설정 시간</strong> | 높음(전용 하드웨어) | 낮음~보통 | 낮음~보통 |
| <strong>휴대성</strong> | 낮음(전용 머신) | 높음(스냅샷, 이동성) | 높음 |
| <strong>리소스 오버헤드</strong> | 없음 | 보통 | 낮음~보통 |
| <strong>CTF / 랩 사용</strong> | 과함 | 이상적 | 이상적 |
| <strong>전문 작업</strong> | 권장 | 허용 가능 | 허용 가능 |

<strong>결론:</strong> CTF 대회, 랩 연습, 학습 환경의 경우 적절한 USB 패스스루가 적용된 VM은 편리하고 유능합니다. 신뢰성과 포렌식 무결성이 중요한 전문 침투 테스트 작업의 경우, 전용 Kali 노트북이나 베어메탈 설치가 더 믿을 수 있는 선택입니다. VM의 프레임 손실과 간헐적인 USB 중재 문제는 PMKID 캡처나 디인증 플러딩 같은 시간에 민감한 공격의 신뢰성에 영향을 줄 수 있습니다.

---

## 빠른 문제 해결 참조

| 증상 | 가장 가능성 높은 원인 | 해결책 |
|---|---|---|
| Kali 내부의 `lsusb`에 아무것도 표시되지 않음 | USB 패스스루 미구성 | USB 필터 추가(VBox) 또는 Removable Devices로 연결(VMware) |
| VirtualBox USB 설정에 "No USB devices" | Extension Pack 누락 또는 버전 불일치 | 일치하는 Extension Pack 설치 |
| `lsusb`에는 어댑터가 보이지만 `wlan` 인터페이스가 없음 | 드라이버가 로드되지 않음 | `sudo modprobe 88XXau` 또는 `sudo modprobe mt7921u` |
| `modprobe: FATAL: Module 88XXau not found` | DKMS 패키지 미설치 | `sudo apt install realtek-rtl88xxau-dkms` |
| 인터페이스가 나타났다가 사라짐 | USB 자동 절전 또는 VBox xHCI 중재 | 자동 절전 비활성화, ACH의 경우 USB 2.0 컨트롤러 시도 |
| `airmon-ng`은 시작되지만 모니터 모드가 조용히 실패 | 잘못된 드라이버 또는 충돌하는 네트워크 관리자 | `sudo airmon-ng check kill` 후 재시도 |
| VirtualBox USB 필터가 부팅 시 캡처하지 않음 | Extension Pack 설치 전에 필터 추가됨 | 필터 삭제, Extension Pack 설치, 필터 재추가 |
| VMware가 긴 세션 중에 장치를 잃음 | VMware USB 중재자 서비스 중지 | 재활성화하고 자동 시작으로 설정 |

---

{{< faq >}}

## 다음 단계

USB 패스스루가 구성되고 모니터 모드가 확인되었으면 다음을 진행할 준비가 된 것입니다:

- <strong>드라이버 설치 또는 업데이트:</strong> [Kali 및 Ubuntu용 ALFA 드라이버 설치 가이드](/ko/blog/install-alfa-driver-kali-ubuntu/)
- <strong>전체 AWUS036ACH 설정 안내:</strong> [AWUS036ACH Kali Linux 설정 가이드](/ko/blog/awus036ach-kali-linux-setup/)
- <strong>AWUS036AXML 하드웨어 리뷰:</strong> [AWUS036AXML WiFi 6E 리뷰](/ko/blog/awus036axml-wifi-6e-review/)

VM 기반 침투 테스트를 위해 어떤 어댑터를 구매할지 평가 중이라면, AWUS036ACH는 성숙한 USB 2.0 패스스루 동작과 충분히 검증된 드라이버 덕분에 여전히 가장 신뢰할 수 있는 선택입니다. AWUS036AXML은 모든 것이 작동하기 시작하면 더 나은 성능을 내지만, 더 세심한 USB 3.0 구성이 필요합니다.

## 참고 자료

1. [VirtualBox 공식 다운로드](https://www.virtualbox.org/wiki/Downloads)
2. [VMware Workstation 제품 페이지](https://www.vmware.com/products/workstation-pro.html)
3. [aircrack-ng rtl8812au 드라이버 프로젝트](https://github.com/aircrack-ng/rtl8812au)
4. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
5. [Kali Linux 공식 문서](https://www.kali.org/docs/)
