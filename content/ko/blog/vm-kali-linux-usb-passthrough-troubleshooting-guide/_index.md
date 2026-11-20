---
title: "Kali Linux VM에서 USB 패스스루 문제 해결"
description: "VirtualBox 및 VMware에서 ALFA AWUS036ACH/AWUS036AXML의 USB 패스스루 문제를 해결합니다. Extension Pack, xHCI, vboxusers, 그리고 lsusb→iwconfig→dmesg 진단 흐름을 다룹니다."
date: 2026-08-31
author: benny-lai
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "wireless-adapter", "virtual-machine"]
featureimage: /images/blog/vm-kali-linux-usb-passthrough-troubleshooting-guide.webp
faq:
  - question: "어댑터를 다른 USB 포트로 옮겼더니 lsusb에 아무것도 나타나지 않습니다. 어댑터가 고장 난 것입니까?"
    answer: "반드시 그렇지는 않습니다. 먼저 충전 전용 포트에 꽂았는지, 또는 호스트가 절전을 위해 장치를 대기 상태로 만들었는지 확인하십시오. 메인보드 뒷면 I/O 패널의 표준 USB 포트로 다시 옮기거나 한 번 뽑았다가 다시 꽂으면 대개 복구됩니다."
  - question: "VM 창 오른쪽 아래의 USB 아이콘 목록이 비어 있습니다. 어떻게 해야 합니까?"
    answer: "순서대로 확인하십시오. ① Extension Pack 버전이 VirtualBox와 정확히 일치하는지, ② Linux 호스트에서는 사용자가 vboxusers 그룹에 속해 있는지(재로그인 필요), ③ 호스트에서 lsusb로 여전히 어댑터가 보이는지, ④ 다른 소프트웨어(예: 호스트 측 드라이버 유틸리티)가 장치를 점유하고 있지 않은지 확인합니다."
  - question: "USB 필터를 설정한 후 호스트에서 더 이상 어댑터를 사용할 수 없습니다. 정상입니까?"
    answer: "네, 예상된 동작입니다. 장치가 Guest로 패스스루되면 제어권이 Guest에 있으므로 호스트는 동시에 사용할 수 없습니다. 호스트에서 어댑터가 다시 필요할 때는 VM 창의 USB 아이콘에서 해제하십시오."
  - question: "Guest 안의 lsusb에는 어댑터가 보이지만 wlan 인터페이스가 없습니다. 어떤 드라이버를 설치해야 합니까?"
    answer: "칩셋에 따라 다릅니다. AWUS036AXML(MediaTek MT7921AUN)은 커널 내장 mt7921u 드라이버를 사용하며 Kernel 5.18 이상에서는 플러그 앤 플레이로 작동합니다. 먼저 apt install linux-firmware가 최신 상태인지 확인하십시오. AWUS036ACH(Realtek RTL8812AU)는 out-of-tree 드라이버를 사용합니다. 커뮤니티에서 관리하는 aircrack-ng/rtl8812au를 설치하고 DKMS로 컴파일하십시오(Secure Boot의 경우 MOK 서명도 처리해야 하며, Secure Boot를 비활성화하지 마십시오)."
  - question: "USB 3.0 컨트롤러를 선택한 후 Guest가 부팅되지 않는 이유는 무엇입니까?"
    answer: "일부 오래된 Guest 커널은 xHCI 지원이 미흡합니다. Kali가 오래된 릴리스라면 다음을 시도하십시오. 종료 → USB 2.0(EHCI) 컨트롤러로 되돌리기 → 부팅 → 커널 업그레이드 → 다시 USB 3.0으로 변경. xHCI를 가장 완전하게 지원받으려면 Kali를 가능한 한 최신 상태로 유지하십시오."
  - question: "물리 머신에서는 어댑터가 빠른데 VM 안에서는 느립니다. 정상입니까?"
    answer: "네. VM 안에서 어댑터의 성능은 대략 USB 에뮬레이션 계층의 전달 속도 수준이며, 물리 머신에서의 직접 연결에 비해 약간의 오버헤드가 추가됩니다. 올바른 USB 3.0(xHCI) 컨트롤러와 최신 Hypervisor를 사용하면 이 오버헤드를 최소화할 수 있습니다. 성능이 심하게 저하되었다면 먼저 컨트롤러가 USB 1.1에 머물러 있지 않은지 확인하십시오."
---

> <strong>지원 호스트</strong>: Oracle VirtualBox / VMware Workstation을 실행하는 Windows / Linux / macOS 호스트 (Guest = Kali Linux / Debian / Ubuntu)
> <strong>대상 하드웨어</strong>: ALFA AWUS036ACH (Realtek RTL8812AU) / ALFA AWUS036AXML (MediaTek MT7921AUN)
> <strong>범위</strong>: 표준화된 USB 패스스루(Pass-through) 문제 해결 매뉴얼입니다. macOS 호스트의 USB 패스스루 제한 사항은 5장에서 다룹니다.

---

{{< tldr >}}

많은 Kali 사용자가 어댑터를 호스트에 꽂았는데 VM 안에서 무선 인터페이스가 보이지 않는 상황을 겪습니다. <strong>대부분의 경우 원인은 매우 흔한 세 가지 중 하나이며</strong>, 어댑터 고장일 가능성은 낮습니다.

1. <strong>VirtualBox Extension Pack이 설치되지 않음</strong>: 설치하지 않으면 Guest는 USB 2.0/3.0 컨트롤러를 전혀 사용할 수 없습니다(USB 1.1은 최대 12 Mbps로, 무선 어댑터에는 턱없이 부족합니다).
2. <strong>USB 패스스루가 설정되지 않음</strong>: 호스트는 기본적으로 모든 USB 장치를 점유합니다. Guest에서는 수동으로 연결하거나, 어댑터를 자동으로 가져가는 VM USB 필터를 설정해야 합니다.
3. <strong>Guest 안의 드라이버가 로드되지 않음</strong>: USB 계층은 패스스루되었지만(`lsusb`에 장치가 표시됨) Linux에 일치하는 드라이버가 없어서 `ip link`에 `wlan` 인터페이스가 나타나지 않습니다.

순서대로 점검하십시오. 호스트 하드웨어, Guest 패스스루, 드라이버 계층 순입니다. 전체 진단 암기법은 1.3절을 참조하십시오.

{{< /tldr >}}

---

## 1. VM이 기본적으로 호스트의 무선 어댑터를 사용할 수 없는 이유

### 1.1 USB 어댑터는 한 번에 하나의 OS에만 속합니다

USB는 <strong>단일 호스트</strong> 아키텍처로 동작합니다. 하나의 USB 장치는 어느 시점에든 하나의 USB 호스트 컨트롤러만 제어할 수 있습니다. 어댑터를 호스트에 꽂으면 호스트 OS가 이를 열거하고 점유합니다. 호스트 드라이버가 이를 인식하고 제어합니다.

Guest VM은 USB 버스 위의 물리 장치가 아니라, Hypervisor가 호스트 내부에서 에뮬레이션하는 "가상 하드웨어"입니다. Guest가 USB 어댑터를 사용하려면 <strong>호스트가 장치를 Guest에게 적극적으로 넘겨주어야 하며</strong>, 이 메커니즘을 <strong>USB 패스스루(Pass-through, USB Redirection)</strong>라고 합니다.

### 1.2 실제로 무엇이 패스스루됩니까?

VirtualBox에서는 흐름이 다음과 같습니다.

```
Physical USB adapter (AWUS036ACH / AWUS036AXML)
       │  plugged into a physical USB port on the host
       ▼
Host OS USB host controller
       │  Hypervisor (VirtualBox) intercepts and redirects
       ▼
Virtual USB host controller (emulated EHCI / xHCI)
       │  the Guest (Kali) sees it "as if plugged into itself"
       ▼
Kali USB driver → wireless driver → wlan interface
```

패스스루가 성공하면 <strong>호스트 측 장치의 제어권이 Guest로 넘어갑니다</strong>. 호스트에서는 장치가 "뽑힌" 것처럼 동작하며 더 이상 사용할 수 없습니다. Guest 안에서는 완전히 새로운 USB 장치로 나타납니다. <strong>이는 정상 동작이며 버그가 아닙니다.</strong> 호스트의 USB 장치 하나는 양쪽을 동시에 지원할 수 없습니다.

### 1.3 "보이지 않는다"에는 사실 세 가지 계층이 있습니다

| 계층 | 확인 방법 | 증상 | 의미 |
|-------|-----------|---------|---------------|
| <strong>USB 패스스루 계층</strong> | Guest 안에서 `lsusb` | `lsusb`에 어댑터의 VID:PID가 전혀 나타나지 않음 | 패스스루 실패(Extension Pack / 컨트롤러 / 필터 문제) |
| <strong>드라이버 계층</strong> | Guest 안에서 `dmesg` | `lsusb`에는 장치가 보이지만 `dmesg`에 오류가 보고됨(펌웨어 누락, `Required key not available`) | Guest 안에 드라이버가 없거나 모듈 로드 실패 |
| <strong>무선 인터페이스 계층</strong> | Guest 안에서 `iwconfig` / `ip link` | `lsusb`와 `dmesg`는 모두 정상이지만 `wlan` 인터페이스가 없음 | 드라이버는 로드되었으나 인터페이스가 등록되지 않았거나 모드/설정 문제 |

> <strong>진단 암기법</strong>: 먼저 `lsusb`를 실행하여 장치가 Guest로 패스스루되었는지 확인하고, 그다음 `ip link`를 실행하여 드라이버가 이를 인식하는지 확인하십시오. <strong>어댑터가 고장 났을 것이라는 의심부터 시작하지 마십시오.</strong>

---

## 2. VirtualBox: 먼저 Extension Pack을 설치하고, USB 3.0 컨트롤러를 설정하십시오

### 2.1 Extension Pack은 필수입니다

VirtualBox 기본 패키지는 <strong>USB 1.1(OHCI) 컨트롤러</strong>만 에뮬레이션하며, USB 1.1의 처리량은 무선 어댑터에 턱없이 부족합니다. <strong>USB 2.0(EHCI) 및 USB 3.0(xHCI) 컨트롤러는 Oracle 공식 Extension Pack을 통해서만 사용할 수 있습니다.</strong>

Extension Pack이 없을 때의 증상은 전형적입니다. Guest 설정에 USB 2.0 / USB 3.0 컨트롤러 옵션이 없거나, 어댑터를 연결할 때 "가상 머신에 대한 장치 연결에 실패했습니다(error code E_FAIL / VERR_PDM_NO_USB_PORTS)"라는 오류가 발생합니다.

### 2.2 버전이 정확히 일치해야 합니다

Extension Pack 버전은 <strong>VirtualBox 버전과 정확히 일치해야 합니다</strong>(예: VirtualBox 7.0.20에는 7.0.20 Extension Pack이 필요합니다). 마이너 버전만 달라도 설치나 로드가 실패할 수 있습니다.

```bash
# Check the current VirtualBox version
vboxmanage --version
```

Oracle 공식 다운로드 페이지(https://www.virtualbox.org/wiki/Downloads)에서 일치하는 `Oracle_VM_VirtualBox_Extension_Pack-<version>.vbox-extpack`을 내려받은 후 다음을 수행하십시오.

```bash
# Option 1: GUI install (VirtualBox main window → File → Tools → Extension Pack Manager → Install)
# Option 2: Command-line install
sudo VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-*.vbox-extpack

# Confirm the installation
VBoxManage list extpacks
```

> 설치 프로그램에 Oracle 라이선스(Personal Use and Evaluation License)가 표시됩니다. 개인 사용은 무료이며, 상업 환경에서는 라이선스 조건을 따르십시오.

### 2.3 Linux 호스트: 자신을 vboxusers 그룹에 추가하십시오

Linux 호스트에서 VirtualBox가 USB 장치에 접근하려면 <strong>사용자가 `vboxusers` 그룹에 속해 있어야 합니다</strong>. 많은 사람이 Extension Pack을 설치하고도 실패하는데, 걸림돌은 권한입니다.

```bash
# Join the group (replace <user> with your username)
sudo usermod -aG vboxusers $USER

# Log out and back in (or reboot) for the group to take effect; verify it
id $USER
```

### 2.4 USB 3.0(xHCI) 컨트롤러 설정

1. Kali VM을 선택하고 <strong>설정 → 포트 → USB</strong>로 이동합니다.
2. "USB 컨트롤러 활성화"를 선택하고 <strong>USB 3.0(xHCI) 컨트롤러</strong>를 고릅니다.
   - AWUS036AXML은 USB 3.2 Gen 1(USB-C) 장치이므로 <strong>반드시 USB 3.0(xHCI)을 선택해야 합니다</strong>. USB 2.0을 선택하면 전송 속도가 제한됩니다.
   - AWUS036ACH는 USB Type-A를 사용하며 USB 2.0과 USB 3.0 컨트롤러 모두에서 작동합니다. 최상의 전송 속도를 위해 USB 3.0(xHCI)도 선택하십시오.
3. 컨트롤러를 변경한 후에는 변경 사항이 적용되도록 <strong>전원을 끄고 다시 켜십시오</strong>(Guest 안에서의 재부팅이 아닙니다).

### 2.5 수동 연결과 VMware 비교

Kali VM이 실행 중일 때 <strong>창 오른쪽 아래의 USB 아이콘</strong>(USB 플러그 모양)을 확인하십시오.

1. USB 아이콘을 클릭하면 현재 호스트에 연결된 USB 장치 목록이 표시됩니다.
2. 어댑터는 `Realtek 802.11ac NIC`(ACH) 또는 `ALFA AWUS036AXML` / MediaTek(AXML)과 같은 이름으로 나타나야 합니다.
3. 한 번 클릭하면 장치가 Kali로 넘어갑니다.

목록이 비어 있다면 패스스루 계층에 문제가 있는 것입니다. 2.2 / 2.3 / 2.4절(USB 컨트롤러가 활성화되지 않은 경우 포함)을 다시 확인하거나 6장의 문제 해결 워크시트를 실행하십시오.

<strong>VMware 비교</strong>: VMware Workstation / Fusion은 USB 패스스루에 <strong>별도의 Extension Pack이 필요하지 않지만</strong>, 두 가지 흔한 점검 사항이 있습니다.

1. <strong>호스트 측 서비스</strong>: Linux 호스트에서는 `vmware-usbarbitrator`(USB 중재 서비스)가 실행 중인지 확인합니다.
   ```bash
   sudo systemctl status vmware-usbarbitrator
   # If it is not running, start it and enable it at boot
   sudo systemctl enable --now vmware-usbarbitrator
   ```
2. <strong>VM 설정</strong>: VM 설정 → USB 컨트롤러 → <strong>USB 3.1(또는 USB 3.0)</strong>을 선택합니다.
3. <strong>수동 연결</strong>: VMware 창 메뉴 → <strong>이동식 장치 → 사용 중인 어댑터 → 연결</strong>을 선택합니다.

> <strong>핵심 비교</strong>: VirtualBox는 보통 Extension Pack 누락 때문에 실패하고, VMware는 보통 중재 서비스가 실행되지 않거나 USB 3.0 컨트롤러가 꺼져 있어서 실패합니다. 어떤 제품을 사용하는지 먼저 확인한 다음 해당 항목을 점검하십시오.

---

## 3. 세 가지 진단 명령어: lsusb → iwconfig → dmesg

패스스루 설정 후에는 세 가지 명령어로 문제가 "패스스루 계층"에 있는지 "드라이버 계층"에 있는지 정확히 찾아낼 수 있습니다.

### 0단계: 먼저 호스트에서 하드웨어를 확인합니다 (어댑터를 탓하지 마십시오)

<strong>호스트 OS</strong>에서 터미널을 열고 다음을 실행합니다.

```bash
lsusb
```

예상 출력(모델에 따라 다름):

```
# AWUS036ACH (Realtek RTL8812AU)
Bus ... ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
# or AWUS036AXML (MediaTek MT7921AUN)
Bus ... ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

- 호스트에서 보인다 → 하드웨어와 케이블은 정상이며, 문제는 패스스루 또는 Guest 드라이버에 있습니다.
- 호스트에서 보이지 않는다 → <strong>먼저 호스트 측을 점검하십시오</strong>(다른 USB 포트, 다른 케이블, 다른 머신에서 교차 테스트). 그다음 지원 티켓 접수를 고려하십시오.

### 1단계: Guest 안에서 lsusb: 패스스루가 성공했습니까?

<strong>Kali VM</strong> 안에서 실행합니다.

```bash
lsusb
```

- 같은 VID:PID가 보인다 → <strong>패스스루 성공</strong>, 2단계로 이동합니다.
- 보이지 않는다 → <strong>패스스루 실패</strong>. 2장(Extension Pack / 컨트롤러 / vboxusers 그룹)으로 돌아가거나, 다른 호스트 소프트웨어가 어댑터를 점유하고 있는지 확인하십시오.

### 2단계: iwconfig / ip link: 무선 인터페이스가 나타났습니까?

```bash
iwconfig
# or (newer versions)
iw dev
ip link
```

- `wlan0` / `wlx...` 인터페이스가 나타난다 → <strong>모든 것이 정상 작동 중이므로</strong> 사용을 시작하십시오.
- 무선 인터페이스는 없지만 `lsusb`에 장치가 보인다 → 문제는 <strong>Guest 드라이버 계층</strong>에 있으며, 3단계로 이동합니다.

### 3단계: dmesg: 드라이버 계층이 실패한 이유는 무엇입니까?

```bash
# Watch the kernel's recent messages
sudo dmesg | tail -30
# Filter USB and wireless-related messages
sudo dmesg | grep -iE "usb|wlan|8812|mt7921|rtl" | tail -30
```

일반적인 `dmesg` 결과:

| `dmesg` 메시지 | 원인 | 해결 방법 |
|-----------------|-------|-----|
| `usb 3-1: new high-speed USB device ...` 뒤에 아무것도 없음 | 장치는 열거되었으나 사용할 드라이버가 없음 | Guest 안에 일치하는 드라이버 설치(FAQ Q4 참조) |
| `Direct firmware load failed` / `firmware_loading` | 펌웨어 파일 누락 | `apt install firmware-realtek` 후 모듈 재로드 |
| `Required key not available` | Secure Boot가 켜져 있고 모듈에 서명되지 않음 | MOK 키로 서명(Secure Boot를 비활성화하지 마십시오) |
| `disagrees about version of symbol` | 드라이버 버전이 커널과 일치하지 않음 | DKMS로 다시 빌드하고 설치 |

> <strong>핵심 통찰</strong>: `lsusb`에 장치가 보이는 것은 "USB 패스스루가 작동했다"는 것만 증명할 뿐, <strong>드라이버가 로드되었다는 뜻은 아닙니다</strong>. 흔히 겪는 "패스스루는 되는데 wlan이 없는" 경우가 바로 이것입니다. Guest 안에 일치하는 드라이버가 없는 것입니다.

---

## 4. USB VM 필터: 연결 시 자동 연결 + 연결 끊김 문제 해결

### 4.1 USB 필터를 설정하는 이유

수동 연결(2장, 2.5절)의 문제점은 <strong>Kali VM을 재시작할 때마다 다시 클릭해야 한다는 것</strong>입니다. USB 필터를 사용하면 어댑터를 꽂는 순간(또는 VM이 부팅되는 순간) VirtualBox가 <strong>일치하는 장치를 자동으로 Guest로 옮겨 줍니다</strong>.

설정 방법(VirtualBox):

1. VM 설정 → USB → <strong>"+"를 클릭하여 필터 추가 → 사용 중인 어댑터 선택</strong>.
2. VirtualBox가 필터 규칙(제조업체 ID / 제품 ID / 일련 번호 필드)을 자동으로 채웁니다.
   - <strong>이름</strong>: 예: `ALFA AWUS036AXML` 또는 `AWUS036ACH`
   - <strong>제조업체 ID</strong>: AWUS036ACH는 `0bda`, AWUS036AXML은 `0e8d`
   - <strong>제품 ID</strong>: AWUS036ACH는 `8812`, AWUS036AXML은 `7961`
3. 같은 모델의 어댑터가 여러 개라면 필터가 잘못된 것을 가져가지 않도록 <strong>일련 번호</strong> 필드도 입력하십시오.

> 팁: 필터를 마우스 오른쪽 버튼으로 클릭 → <strong>필터 편집</strong>에서 제조업체 ID와 제품 ID만 유지(느슨한 일치)하거나 일련 번호를 추가(정확한 일치)할 수 있습니다.

### 4.2 잦은 연결 끊김: 대개 전원 또는 컨트롤러 문제입니다

고전력 어댑터(AWUS036ACH는 모니터/인젝션 중 순간 전류가 더 높고, AWUS036AXML은 USB 3 장치입니다)는 VM 안에서 가끔 "끊기거나 연결이 해제"될 수 있습니다. 전형적인 원인과 해결 방법은 다음과 같습니다.

| 증상 | 원인 | 해결 방법 |
|---------|-------|-----|
| 패스스루 후 전력이 부족하여 계속 끊김 | 에뮬레이션된 가상 USB 컨트롤러가 전력에 보수적이거나, 호스트 포트가 충분한 전력을 공급하지 못함 | 호스트의 <strong>메인보드 뒷면 USB 포트</strong>를 사용하거나 자체 전원이 있는 USB 허브 사용 |
| 어댑터가 나타났다 사라졌다 함 | 호스트의 <strong>USB 자동 절전</strong>이 장치를 대기 상태로 만듦 | 호스트 설정에서 "해당 장치"의 USB 자동 절전 비활성화(시스템 전체의 보안 보호 기능은 비활성화하지 마십시오) |
| 연결 즉시 일련의 오류 코드와 함께 실패 | 잘못된 컨트롤러 선택(USB 1.1/2.0은 USB 3 장치를 지원할 수 없음) | <strong>USB 3.0(xHCI) 컨트롤러</strong>로 변경하고 전원 재시작 |
| 호스트가 절전에서 깨어난 후 어댑터가 작동하지 않음 | 호스트 절전 중 Hypervisor의 USB 리다이렉션이 끊김 | 사용 중에는 호스트 절전을 피하거나, 깨어난 후 한 번 다시 연결 |

### 4.3 보안 알림

끊김을 줄이기 위해 <strong>단일 USB 장치</strong>의 자동 절전을 비활성화할 수는 있지만, 반드시 "해당 장치" 수준에서만 하십시오. 번거로움을 피하려고 시스템 수준의 보안 보호 기능(방화벽, Secure Boot)을 <strong>비활성화하지 마십시오</strong>. 치르는 대가가 균형에 맞지 않습니다.

---

## 5. macOS 호스트의 제한 사항과 플랫폼 경계

### 5.1 macOS 호스트에는 본질적인 USB 패스스루 제한이 있습니다

macOS 호스트에서 VM을 실행하며 USB 패스스루를 사용하는 것은 <strong>가장 막히기 쉬운 조합</strong>입니다. 먼저 자신의 상황을 확인하십시오.

| macOS 호스트 | VirtualBox | VMware Fusion |
|------------|-----------|---------------|
| <strong>Apple Silicon (M1/M2/M3/M4)</strong> | ⚠️ <strong>USB 패스스루 지원이 제한적/불완전합니다</strong>. 공식 문서에 기재된 제한 사항 중 하나이며, 어댑터 드라이버가 작동하더라도 패스스루 계층을 사용할 수 없을 수 있습니다 | ⚠️ 지원이 더 완전하지만, 먼저 "호스트에 직접 연결"하여 어댑터가 macOS에서 작동하는지 확인하는 것을 여전히 권장합니다 |
| <strong>Intel (Intel Mac)</strong> | ✅ 작동하지만, 먼저 <strong>커널 확장 승인</strong> 절차(시스템 설정 → 개인정보 보호 및 보안 → Oracle 관련 커널 확장 허용)를 완료하고 정확히 일치하는 Extension Pack을 설치해야 합니다 | ✅ 작동합니다 |

<strong>권장 사항</strong>: 호스트가 macOS라면 "호스트에 직접 연결 → `system_profiler SPUSBDataType` → 어댑터가 호스트에서 작동하는지 확인"을 모든 문제 해결 세션의 첫 번째 관문으로 삼으십시오. <strong>macOS에서 지원되지 않는 모델을 VM 문제 해결 대상에 포함하지 마십시오.</strong> 많은 시간을 낭비하게 됩니다.

### 5.2 플랫폼 경계 (지원 경계)

| 플랫폼 | 지원 상태 | 비고 |
|----------|---------------|-------|
| Windows 호스트 + VirtualBox / VMware + Kali Guest | ✅ 지원 | 이 글의 모든 절차가 적용됩니다 |
| Linux 호스트 + VirtualBox / VMware + Kali Guest | ✅ 지원 | vboxusers 그룹(VB)과 vmware-usbarbitrator 서비스(VMware)를 기억하십시오 |
| <strong>macOS (Apple Silicon)</strong> + VirtualBox | ⚠️ <strong>USB 패스스루 제한</strong> | VMware Fusion으로 전환하거나 Linux / Windows 호스트를 사용하십시오 |
| macOS (Intel) + VirtualBox | ✅ 지원 | 커널 확장 승인 + 버전이 일치하는 Extension Pack 필요 |
| <strong>Guest가 macOS인 경우</strong> | ❌ 권장하지 않음 | 이 글은 Kali / Debian / Ubuntu와 같은 Linux Guest를 전제로 합니다 |

> <strong>지원 경계</strong>: 문제 해결 전에 항상 "호스트가 어댑터를 인식하는가"를 먼저 확인한 다음 VM 설정을 논의하십시오. 호스트 자체가 어댑터를 인식하지 못한다면 어떤 VM 설정으로도 해결할 수 없으며, 다음 단계는 호스트 측 드라이버 문제입니다(본 사이트의 다른 드라이버 문제 해결 글을 참조하십시오).

---

## 6. 표준 문제 해결 워크시트: 티켓을 접수하기 전에 실행하십시오 (지원 접수)

> "VM에서 어댑터가 보이지 않는" 문제가 발생하면 아래 표를 순서대로 따라 하며 결과를 기록하십시오. <strong>지원 티켓을 열기로 결정하기 전에 전체 워크시트를 실행하십시오.</strong> 많은 사례가 저절로 해결되며, 지원 과정의 주고받는 횟수를 크게 줄여 줍니다.

### 1단계: 호스트 하드웨어 점검

| 점검 항목 | 명령어 | 기록 |
|-------|---------|--------|
| 호스트 OS 및 아키텍처 | `uname -a` / `systeminfo` | \_\_\_\_\_ |
| 호스트가 어댑터를 인식합니까? | 호스트에서 `lsusb` | VID:PID \_\_\_\_\_ |
| USB 포트 및 케이블 | 다른 포트, 다른 케이블 시도 | 결과 \_\_\_\_\_ |

### 2단계: Hypervisor 계층 점검

| 점검 항목 | 작업 | 기록 |
|-------|--------|--------|
| Hypervisor 및 버전 | VirtualBox: `vboxmanage --version` / VMware: 도움말 → 정보 | \_\_\_\_\_ |
| Extension Pack 버전이 일치합니까? | VirtualBox: `VBoxManage list extpacks` | 버전 \_\_\_\_\_ |
| 호스트 권한 / 서비스 | Linux 호스트: `id`로 vboxusers 확인, VMware: `systemctl status vmware-usbarbitrator` | \_\_\_\_\_ |
| USB 컨트롤러 설정 | VirtualBox: USB 3.0(xHCI) 컨트롤러가 선택되어 있습니까? | 예 / 아니요 |

### 3단계: 패스스루 결과 점검

| 점검 항목 | 명령어 | 기록 |
|-------|---------|--------|
| Guest가 어댑터를 인식합니까? | Guest 안에서 `lsusb` | \_\_\_\_\_ |
| 무선 인터페이스가 나타났습니까? | Guest 안에서 `iwconfig` / `ip link` | \_\_\_\_\_ |
| 드라이버 계층 메시지 | Guest 안에서 `sudo dmesg \| tail -30` | \_\_\_\_\_ |
| 사용 중인 Guest 커널 | `uname -r` | \_\_\_\_\_ |

### 4단계: 판정 및 기록

- `lsusb`(Guest)에 아무것도 없음 → <strong>패스스루 계층</strong> 문제 → 2장과 2단계를 검토하십시오.
- `lsusb`에 장치가 보이지만 `ip link`에 wlan이 없음 → <strong>드라이버 계층</strong> 문제 → 3장, 3단계를 검토하십시오.
- 모두 정상이지만 불안정함 → <strong>전원 / 자동 절전 / 컨트롤러</strong> 문제 → 4장.

### 지원 접수 정보 패키지

지원팀에 전화하거나 티켓을 제출하기 전에 다음을 한 번에 첨부하면 담당자가 바로 핵심에 접근할 수 있습니다.

> <strong>호스트 OS + 아키텍처, Hypervisor 및 버전, Extension Pack 설치 여부와 버전, 호스트 측 `lsusb` 출력, Guest 측 `lsusb` 출력, Guest 측 `ip link` / `iwconfig` 출력, 관련 `dmesg` 메시지, 어댑터 모델 및 연결 방식(USB-C / USB-A, 직접 연결 또는 허브 경유)</strong>

---

## 7. FAQ

<strong>Q1: 어댑터를 다른 USB 포트로 옮겼더니 `lsusb`에 아무것도 나타나지 않습니다. 어댑터가 고장 난 것입니까?</strong>
반드시 그렇지는 않습니다. 먼저 충전 전용 포트에 꽂았는지, 또는 호스트가 절전을 위해 장치를 대기 상태로 만들었는지 확인하십시오. 메인보드 뒷면 I/O 패널의 표준 USB 포트로 다시 옮기거나 한 번 뽑았다가 다시 꽂으면 대개 복구됩니다.

<strong>Q2: VM 창 오른쪽 아래의 USB 아이콘 목록이 비어 있습니다. 어떻게 해야 합니까?</strong>
순서대로 확인하십시오. ① Extension Pack 버전이 VirtualBox와 정확히 일치하는지, ② Linux 호스트에서는 사용자가 `vboxusers` 그룹에 속해 있는지(재로그인 필요), ③ 호스트에서 `lsusb`로 여전히 어댑터가 보이는지, ④ 다른 소프트웨어(예: 호스트 측 드라이버 유틸리티)가 장치를 점유하고 있지 않은지 확인합니다.

<strong>Q3: USB 필터를 설정한 후 호스트에서 더 이상 어댑터를 사용할 수 없습니다. 정상입니까?</strong>
네, 예상된 동작입니다. 장치가 Guest로 패스스루되면 제어권이 Guest에 있으므로 호스트는 동시에 사용할 수 없습니다. 호스트에서 어댑터가 다시 필요할 때는 VM 창의 USB 아이콘에서 해제하십시오.

<strong>Q4: Guest 안의 `lsusb`에는 어댑터가 보이지만 wlan 인터페이스가 없습니다. 어떤 드라이버를 설치해야 합니까?</strong>
칩셋에 따라 다릅니다.
- <strong>AWUS036AXML (MediaTek MT7921AUN)</strong>: 커널 내장 `mt7921u` 드라이버를 사용하며 Kernel 5.18 이상에서는 플러그 앤 플레이로 작동합니다. 먼저 `apt install linux-firmware`가 최신 상태인지 확인하십시오.
- <strong>AWUS036ACH (Realtek RTL8812AU)</strong>: out-of-tree 드라이버를 사용합니다. 커뮤니티에서 관리하는 `aircrack-ng/rtl8812au`를 설치하고 DKMS로 컴파일하십시오(Secure Boot의 경우 MOK 서명도 처리해야 하며, Secure Boot를 비활성화하지 마십시오).

<strong>Q5: USB 3.0 컨트롤러를 선택한 후 Guest가 부팅되지 않는 이유는 무엇입니까?</strong>
일부 오래된 Guest 커널은 xHCI 지원이 미흡합니다. Kali가 오래된 릴리스라면 다음을 시도하십시오. 종료 → USB 2.0(EHCI) 컨트롤러로 되돌리기 → 부팅 → 커널 업그레이드 → 다시 USB 3.0으로 변경. xHCI를 가장 완전하게 지원받으려면 Kali를 가능한 한 최신 상태로 유지하십시오.

<strong>Q6: 물리 머신에서는 어댑터가 빠른데 VM 안에서는 느립니다. 정상입니까?</strong>
네. VM 안에서 어댑터의 성능은 대략 USB 에뮬레이션 계층의 전달 속도 수준이며, 물리 머신에서의 직접 연결에 비해 약간의 오버헤드가 추가됩니다. 올바른 USB 3.0(xHCI) 컨트롤러와 최신 Hypervisor를 사용하면 이 오버헤드를 최소화할 수 있습니다. 성능이 심하게 저하되었다면 먼저 컨트롤러가 USB 1.1에 머물러 있지 않은지 확인하십시오.

---

## 8. 결론 및 하드웨어 권장 사항

"VM에서 어댑터가 보이지 않는" 사례의 90% 이상은 <strong>패스스루 설정</strong> 또는 <strong>Guest 드라이버</strong>를 잘못 구성한 것이 원인이며, 하드웨어 고장은 드뭅니다. 이 글의 단계를 순서대로 따라 하십시오.

1. <strong>먼저 호스트에서 `lsusb`로 하드웨어를 확인하십시오.</strong>
2. <strong>VirtualBox에서는 항상 버전이 일치하는 Extension Pack을 설치하고</strong>, Linux 호스트에서는 `vboxusers` 그룹에 가입하십시오. VMware에서는 `vmware-usbarbitrator` 서비스가 실행 중인지 확인하십시오.
3. <strong>USB 컨트롤러를 USB 3.0(xHCI)으로 설정하고</strong>, USB 필터를 사용하여 어댑터가 자동으로 연결되도록 하십시오.
4. <strong>Guest 안에서 `lsusb → iwconfig / ip link → dmesg`로 문제 계층을 찾고</strong>, 누락된 드라이버를 설치하십시오. 어댑터가 고장 났을 것이라고 추측하는 일은 그만두십시오.

<strong>권장 하드웨어</strong>: ALFA AWUS036AXML(MediaTek MT7921AUN)은 <strong>커널 내장 드라이버를 갖추고 있어 플러그 앤 플레이로 작동</strong>하며, 최신 Kali 커널에서 VM 패스스루 후 가장 손이 덜 갑니다. ALFA AWUS036ACH(Realtek RTL8812AU)도 동등한 성능을 갖추고 있지만, Guest 안에서 커뮤니티 드라이버를 DKMS로 컴파일하고 Secure Boot 서명을 처리해야 한다는 점을 기억하십시오(본 사이트의 RTL8812AU DKMS 문제 해결 글 참조). 두 제품 모두 호스트 측에서 자체 전원이 있는 USB 포트 / 허브를 사용하면 "끊김" 변수를 한 번에 제거할 수 있습니다. 인젝션은 커널에 따라 달라진다는 점에 유의하십시오. 6.16 이전 커널에서는 인젝션이 작동했다는 커뮤니티 보고가 있지만, 6.16 이후의 표준 커널(6.17에서 테스트)에서는 AXML이 패킷 인젝션 테스트(`aireplay-ng --test`: Found 0 APs / No Answer)에 실패하여 deauth와 핸드셰이크 캡처가 불가능합니다. 원인은 칩 한계가 아니라 mac80211 chanctx 회귀입니다. 패치된 커뮤니티 드라이버로 인젝션을 복구할 수 있지만, 펌웨어가 여전히 속도를 고정합니다(1/6 Mbps, HT/VHT 인젝션 불가). 모니터 모드, AP, WPA3는 영향을 받지 않습니다. 인젝션이 필요하다면 AWUS036ACH 또는 AWUS036EACS를 선택하십시오.

<strong>다음 단계</strong>: 6장의 워크시트를 Kali VM 바탕화면에 사본으로 저장해 두십시오. 어댑터가 "사라질" 때마다 먼저 전체를 실행한 다음 지원 티켓을 열지 결정하십시오. 워크시트를 따르면 데이터가 해결해 줍니다.

---

## 참고 자료

| 자료 | 링크 |
|----------|------|
| Oracle VirtualBox 공식 다운로드 페이지 (Extension Pack) | https://www.virtualbox.org/wiki/Downloads |
| VirtualBox 공식 매뉴얼: USB 설정 및 필터 | https://www.virtualbox.org/manual/ ("USB" 장 검색) |
| VirtualBox 매뉴얼: 알려진 제한 사항 (Apple Silicon USB 패스스루 제한 포함) | https://www.virtualbox.org/manual/ (Changelog / Limitations) |
| VirtualBox Extension Pack 설치 명령어 | `vboxmanage help extpack` |
| aircrack-ng RTL8812AU 커뮤니티 드라이버 (Guest 안의 AWUS036ACH용) | https://github.com/aircrack-ng/rtl8812au |
| ALFA AWUS036ACH 공식 제품 페이지 | https://www.alfa.com.tw/products/awus036ach_1 |
| ALFA AWUS036AXML 공식 제품 페이지 | https://www.alfa.com.tw/ |
| Yopitek 기술 지원 | https://yupitek.com/ |
