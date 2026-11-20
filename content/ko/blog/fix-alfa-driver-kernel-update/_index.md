---
title: "커널 업데이트 후 ALFA 드라이버가 작동하지 않나요? 해결 방법은 다음과 같습니다"
description: "Linux 커널 업데이트 후 ALFA USB WiFi 어댑터가 작동하지 않나요? 커널 업그레이드 후 Kali Linux와 Ubuntu에서 RTL8812AU, RTL8811AU, MT7921AUN 드라이버를 위한 완전한 해결 가이드입니다."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "커널 업데이트 후 ALFA 어댑터가 작동하지 않는 이유는 무엇인가요?"
    answer: "RTL8812AU는 아웃오브트리(out-of-tree) 드라이버를 사용합니다. 컴파일된 모듈은 커널 버전이 바뀔 때마다 호환되지 않게 됩니다. DKMS가 자동으로 재빌드할 수 있지만, 헤더가 없거나 설정이 오래되면 실패합니다."
  - question: "ALFA 드라이버 장애를 어떻게 빠르게 진단하나요?"
    answer: "uname -r로 커널 버전을 확인한 다음, dkms status로 모듈 빌드 상태를 확인하고, 마지막으로 dmesg로 펌웨어 또는 모듈 로딩 오류를 확인하세요."
  - question: "RTL8812AU 드라이버 장애를 가장 빠르게 해결하는 방법은 무엇인가요?"
    answer: "일치하는 커널 헤더를 설치한 다음 dkms autoinstall을 실행하세요. 그래도 실패하면 aircrack-ng/rtl8812au에서 새로 클론하고 make dkms_install을 실행하세요."
  - question: "커널 업데이트 후 MT7921AUN이 연결되지 않으면 어떻게 해야 하나요?"
    answer: "MT7921AUN은 커널 내장 드라이버를 사용합니다. 문제는 대개 펌웨어입니다. firmware-misc-nonfree 패키지를 설치하고 커널 버전이 5.18 이상인지 확인하세요."
  - question: "커널 업데이트가 드라이버를 다시 손상시키지 않도록 하려면 어떻게 하나요?"
    answer: "apt upgrade 대신 apt full-upgrade를 사용하여 헤더와 커널이 함께 설치되도록 하세요. dkms와 linux-headers-generic 메타패키지를 설치하여 의존성을 유지하세요."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-driver", "kernel-update", "rtl8812au", "kali-linux", "ubuntu", "dkms", "troubleshooting"]
featureimage: "/images/blog/fix-alfa-driver-kernel-update.webp"
---

`sudo apt upgrade`를 실행하고 재부팅하면 ALFA 어댑터가 사라졌습니다. 인터페이스도, 표시등도, 아무것도 없습니다. 이것은 Linux에서 ALFA Network USB WiFi 어댑터와 관련해 가장 흔한 지원 문의이며 — 커널 업데이트가 거의 항상 원인입니다. 이 가이드는 가장 큰 영향을 받는 두 칩셋 계열, 즉 **RTL8812AU**(AWUS036ACH와 AWUS036ACS에 탑재)와 **MT7921AUN**(AWUS036AXM과 AXML에 탑재)에 대한 체계적인 진단 및 복구 과정을 안내합니다. 각 섹션을 순서대로 따르면 15분 이내에 어댑터가 다시 온라인 상태가 됩니다.

{{< tldr >}}
커널 업데이트가 ALFA 드라이버를 손상시키는 주된 이유는 헤더와 모듈이 동기화되지 않기 때문입니다. RTL8812AU는 dkms autoinstall로 재빌드합니다. MT7921AUN은 firmware-misc-nonfree가 필요합니다. 장기적인 해결책은 apt full-upgrade를 사용하는 것입니다.
{{< /tldr >}}




---

## 커널 업데이트가 드라이버를 손상시키는 이유

Linux WiFi 드라이버에는 두 가지 유형이 있습니다: 커널 소스 트리와 함께 제공되는 **커널 내장(in-kernel)** 드라이버와, 그 외부에 존재하는 **아웃오브트리(out-of-tree)** 드라이버입니다. 어떤 유형을 사용하는지 이해하면 업데이트가 왜 문제를 일으키는지 정확히 알 수 있습니다.

### 아웃오브트리 드라이버와 DKMS

RTL8812AU 칩셋은 커뮤니티가 유지 관리하는 아웃오브트리 드라이버(가장 흔하게는 `aircrack-ng/rtl8812au` 포크)를 사용합니다. 공식 커널 소스의 일부가 아니기 때문에, **현재 실행 중인 특정 커널의 헤더에 맞춰 컴파일되어야** 합니다. 커널 버전이 바뀔 때마다 — `6.6.15` → `6.6.20` 같은 마이너 패치 릴리스조차도 — 컴파일된 모듈은 더 이상 호환되지 않으며 커널이 로드를 거부합니다.

**DKMS(Dynamic Kernel Module Support)**가 표준 해결책입니다. DKMS는 새 커널 패키지가 설치될 때마다 모듈을 자동으로 재컴파일하는 시스템 수준 훅에 드라이버 소스 코드를 등록합니다. DKMS가 올바르게 설정되면 커널 업데이트가 투명하게 처리됩니다: 새 커널로 재부팅하면 어댑터가 이미 작동합니다.

DKMS는 두 가지 이유로 조용히 실패할 수 있습니다:

1. **커널 헤더 누락** — 컴파일러는 새 커널이 설치되는 시점에 `linux-headers-$(uname -r)`이 설치되어 있어야 합니다. 헤더가 커널보다 늦게 도착하면 DKMS는 빌드 시점을 놓칩니다.
2. **오래된 `dkms.conf`** — 설치된 드라이버 버전의 설정 파일이 오래되어 소스 트리와 더 이상 일치하지 않으면, 빌드가 알 수 없는 오류로 실패합니다.

### 커널 내장 드라이버 (MT7921AUN)

MT7921AUN 칩셋은 버전 **5.18**부터 메인라인 커널에 포함되어 있습니다. 즉, 컴파일 단계가 필요 없습니다 — 커널이 이미 하드웨어와 통신하는 방법을 알고 있습니다. 하지만 드라이버는 여전히 별도 패키지가 제공하는 **펌웨어 블롭**(`mt7921u.bin`)에 의존합니다. 그 패키지가 없거나 커널 업데이트가 예상 펌웨어 API를 변경하면, 어댑터는 로드된 것처럼 보이지만 어떤 네트워크에도 연결되지 않을 수 있습니다.

### 빠른 진단 명령

아무것도 손대기 전에, 다음 두 명령을 실행하여 출발점을 파악하세요:

```bash
# 현재 실행 중인 커널은 무엇인가?
uname -r

# 어떤 DKMS 모듈이 빌드되었는가 (그리고 어떤 커널에 대해)?
sudo dkms status
```

`dkms status`가 RTL8812AU 드라이버를 *이전* 커널용으로 빌드했지만 현재 커널용으로는 빌드하지 않았다고 표시하면, 문제를 찾은 것입니다.

---

## 1단계: 드라이버 진단

이 진단 순서를 위에서 아래로 진행하세요. 각 점검은 변경을 시작하기 전에 근본 원인의 범위를 좁혀 줍니다.

```bash
# 현재 커널 확인
uname -r

# 무선 인터페이스가 아예 존재하는지 확인
ip link show | grep -E "wlan|wlp"

# 드라이버 모듈이 현재 로드되어 있는지 확인
lsmod | grep -E "88XXau|rtl8812au|mt7921u"

# RTL8812AU 어댑터의 DKMS 빌드 상태 확인
sudo dkms status

# 커널 링 버퍼에서 관련 오류 메시지 검색
sudo dmesg | grep -E "ALFA|rtl8812|mt7921" | tail -20
```

**결과 해석:**

| 출력 | 의미 |
|---|---|
| `ip link`에 무선이 아무것도 반환되지 않음 | 커널 모듈이 로드되지 않았거나 하드웨어가 인식되지 않음 |
| `lsmod`에 일치하는 모듈이 없음 | 모듈 로드 실패 — `dmesg`에서 오류 확인 |
| `dkms status`가 현재 커널에 대해 `broken` 또는 누락 표시 | DKMS 빌드 실패 — 아래 RTL8812AU 해결 방법 참조 |
| `dmesg`에 `firmware: failed to load mt7921u` 표시 | 펌웨어 패키지 누락 — 아래 MT7921AUN 해결 방법 참조 |
| `dmesg`에 `disagrees about version of symbol` 표시 | 모듈이 잘못된 커널 헤더에 맞춰 빌드됨 |

{{< alert "triangle-exclamation" >}}
`ip link`에 인터페이스가 보이지만 사용하려고 하면 사라진다면, 어댑터별 문제 해결 표로 건너뛰세요. 보이지만 작동하지 않는 인터페이스는 완전히 사라진 인터페이스와 원인이 다릅니다.
{{< /alert >}}

---

## 해결: RTL8812AU 드라이버 (AWUS036ACH, ACS, EACS)

RTL8812AU는 듀얼 밴드 지원과 안정적인 모니터 모드 덕분에 침투 테스트에 가장 널리 사용되는 ALFA 칩셋입니다. 아웃오브트리 드라이버가 필요하므로 커널 업데이트로 가장 자주 손상되는 칩셋이기도 합니다.

> **EACS(RTL8821CU) 참고:** 커널 6.2 이상에서는 `rtw88_8821cu`가 내장 드라이버이므로 DKMS가 필요하지 않습니다(GX10 커널 6.17에서 모니터/인젝션 실측). 커널 6.2 이전의 구형 커널에서만 morrownr/8821cu 같은 커뮤니티 드라이버를 DKMS로 설치해야 합니다.

### 4.1 — 커널 헤더 설치

어떤 드라이버든 손대기 전 가장 먼저 할 일은 *현재* 커널의 헤더가 설치되어 있는지 확인하는 것입니다:

```bash
sudo apt update
sudo apt install linux-headers-$(uname -r)
```

이 명령이 정상적으로 종료되면 헤더가 이제 존재하며 DKMS 재빌드를 진행할 수 있습니다. 패키지를 찾을 수 없다고 보고하면, 커널이 현재 저장소 스냅샷에 비해 너무 최신일 수 있습니다 — 먼저 `sudo apt full-upgrade`를 실행하여 일치하는 헤더를 가져온 다음, 계속하기 전에 재부팅하세요.

### 4.2 — DKMS로 재빌드 (가장 빠른 경로)

헤더가 준비되면, DKMS에 실행 중인 커널용으로 등록된 모든 모듈을 재빌드하도록 요청합니다:

```bash
sudo dkms autoinstall
```

출력을 주의 깊게 지켜보세요. 성공한 빌드는 `DKMS: install completed`로 끝납니다. 성공하면 재부팅 없이 모듈을 다시 로드합니다:

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

인터페이스가 나타나면 완료입니다. 4.4단계로 진행하여 모니터 모드를 검증하세요.

### 4.3 — 소스에서 전체 재설치 (DKMS 실패 시)

`dkms autoinstall`이 오류를 보고하면, 등록된 드라이버 소스가 손상되었거나 오래된 것입니다. 이를 완전히 제거하고 최신 업스트림 소스에서 재설치하세요:

```bash
# 드라이버의 DKMS 등록 버전 모두 제거
sudo dkms remove rtl8812au/5.6.4.2 --all 2>/dev/null

# 최신 드라이버 소스 클론
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# 한 단계로 DKMS에 소스 등록, 컴파일, 설치
sudo make dkms_install
```

{{< alert "triangle-exclamation" >}}
`dkms remove` 명령의 버전 번호 `5.6.4.2`는 흔한 릴리스이지만 사용자 버전은 다를 수 있습니다. 먼저 `sudo dkms status`를 실행하여 출력에 표시된 정확한 버전 문자열을 사용하세요.
{{< /alert >}}

빌드가 완료된 후:

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

### 4.4 — 모니터 모드 검증

어댑터가 물리적으로 존재하고 드라이버가 로드되었습니다. 이 어댑터를 보안 테스트에 사용할 가치가 있게 만드는 기능인 모니터 모드가 여전히 작동하는지 확인하세요:

```bash
sudo airmon-ng start wlan0
```

`wlan0`을 `ip link`에서 확인한 실제 인터페이스 이름으로 교체하세요. 성공적인 응답은 `wlan0mon` 같은 새 인터페이스 이름과 함께 `monitor mode vif enabled`를 표시합니다.

### 4.5 — Kali 패키지 방식 (가장 쉬움)

Kali Linux는 Kali 커널과 동기화 상태를 유지하는 RTL8812AU 드라이버의 사전 패키징된 DKMS 빌드를 제공합니다. Kali를 사용 중이라면 GitHub에서 클론하는 대신 이 방식을 사용하세요:

```bash
sudo apt update && sudo apt install realtek-rtl88xxau-dkms
```

이 단일 명령은 드라이버 소스를 설치하고, DKMS에 등록하며, 현재 커널에 맞춰 빌드합니다. 이후 `apt full-upgrade`를 실행하면 헤더와 드라이버가 자동으로 동기화됩니다.

---

## 해결: MT7921AUN 드라이버 (AWUS036AXM, AXML)

MT7921AUN(Wi-Fi 6E) 칩셋은 완전히 다른 경로를 따릅니다. Linux 5.18부터 **커널 내장 드라이버**이기 때문에 DKMS도, 컴파일도, GitHub 클론도 필요 없습니다. 커널 업데이트가 이를 손상시켜서는 안 되지만 — 펌웨어 패키징 문제가 때때로 손상시킵니다.

### 5.1 — 펌웨어 패키지 설치

커널 모듈(`mt7921u.ko`)은 이미 존재하지만, 하드웨어를 초기화하려면 사용자 공간의 펌웨어 바이너리가 필요합니다:

```bash
sudo apt install firmware-misc-nonfree
```

Ubuntu에서 이 패키지는 `non-free` 저장소 구성 요소에 있습니다. 명령이 실패하면 `/etc/apt/sources.list`에 non-free 소스가 활성화되어 있는지 확인하세요.

### 5.2 — 드라이버 다시 로드

펌웨어를 설치한 후, 재부팅 없이 드라이버를 강제로 다시 로드합니다:

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
```

그런 다음 인터페이스를 확인합니다:

```bash
ip link show | grep -E "wlan|wlp"
```

### 5.3 — 커널 버전 확인

MT7921AUN 드라이버는 커널 **5.18 이상**이 필요합니다. 이 커널 버전 이전에 출하된 최소 Kali 또는 Ubuntu 이미지를 설치했다면, 모듈이 애초에 존재하지 않습니다:

```bash
uname -r
# 출력은 반드시 5.18.x 이상이어야 함
```

커널이 5.18보다 오래되었다면 업그레이드하세요(5.4단계).

### 5.4 — 커널 업그레이드

```bash
sudo apt update && sudo apt full-upgrade && sudo reboot
```

{{< alert "triangle-exclamation" >}}
`upgrade`가 아니라 `full-upgrade`를 사용하세요. `upgrade` 하위 명령은 다른 패키지를 제거해야 하는 패키지를 보류합니다 — 이는 종종 커널 패키지 자체가 보류됨을 의미합니다. `full-upgrade`는 필요한 의존성 해결을 허용합니다.
{{< /alert >}}

### 5.5 — 재부팅 후 검증

새 커널로 재부팅한 후, 모든 것이 작동하는지 확인합니다:

```bash
sudo modprobe mt7921u
ip link show
sudo dmesg | grep mt7921 | tail -10
```

정상적인 `dmesg` 출력은 펌웨어가 성공적으로 로드되고 USB 장치가 네트워크 인터페이스로 등록되는 것을 보여줍니다.

---

## 향후 업데이트 후에도 드라이버를 유지하기

예방이 복구보다 간단합니다. 다음 관행은 커널 업데이트가 어댑터를 다시 손상시키는 것을 막아 줍니다.

**Kali rolling에서는 항상 `full-upgrade`를 사용하세요:**

```bash
sudo apt update && sudo apt full-upgrade
```

`full-upgrade` 명령은 새 커널 패키지가 설치될 때 일치하는 `linux-headers` 패키지가 *같은 트랜잭션*에서 설치되도록 보장합니다. DKMS 훅은 패키지 설치 중에 실행됩니다 — 헤더가 커널 이후의 나중 `apt` 실행에서 도착하면 DKMS는 빌드를 놓칩니다.

**DKMS 메타패키지 설치:**

```bash
sudo apt install dkms linux-headers-generic
```

이는 DKMS 패키지의 의존성으로 `linux-headers-generic`을 가져오므로, 헤더가 항상 커널과 함께 최신 상태를 유지합니다.

**Ubuntu HWE 커널 스택:**

Ubuntu LTS에서 Hardware Enablement 커널 스택은 GA 커널보다 더 자주 업데이트되고 더 나은 하드웨어 지원을 받습니다. 한 번 설치하면 업데이트가 자동으로 처리됩니다:

```bash
sudo apt install linux-generic-hwe-24.04
```

**DKMS autoinstall이 활성화되어 있는지 확인:**

```bash
cat /etc/dkms/framework.conf | grep autoinstall
```

이 줄이 주석 처리되어 있거나 `no`로 설정되어 있으면, DKMS는 모듈을 자동으로 재빌드하지 않습니다. `/etc/dkms/framework.conf`에서 주석을 해제하거나 `yes`로 설정하세요.

---

## 어댑터별 문제 해결 표

| 증상 | 유력한 칩셋 | 근본 원인 | 빠른 해결 |
|---|---|---|---|
| 재부팅 후 인터페이스 사라짐 | RTL8812AU | DKMS 빌드 실패 | `sudo dkms autoinstall` |
| 인터페이스 사라지고 `dmesg`에 펌웨어 오류 | MT7921AUN | 펌웨어 패키지 누락 | `sudo apt install firmware-misc-nonfree` |
| 인터페이스가 나타나지만 30초 후 사라짐 | RTL8812AU | 모듈 버전 불일치 | `sudo dkms remove --all && sudo make dkms_install` |
| 모니터 모드가 `SIOCSIFFLAGS`로 실패 | RTL8812AU | 잘못된 드라이버 브랜치 | `aircrack-ng/rtl8812au`를 클론하고 재설치 |
| `iwconfig`에 무선 확장이 없음 | 모든 칩셋 | 모듈 미로드 | `sudo modprobe 88XXau` 또는 `sudo modprobe mt7921u` |
| 인터페이스는 있으나 네트워크를 찾지 못함 | MT7921AUN | 커널 < 5.18 | `sudo apt full-upgrade && sudo reboot` |
| `dkms status`가 `broken` 표시 | RTL8812AU | 소스/헤더 불일치 | `sudo apt install linux-headers-$(uname -r)` 후 재빌드 |
| TX 출력이 20 dBm로 제한됨 | RTL8812AU | 규제 도메인 잠금 | `sudo iw reg set US` (지역에 맞게 조정) |

---

## 아무것도 작동하지 않을 때: 새로 설치하는 방법

여러 번의 재빌드 시도가 실패하고 `dkms status`가 여러 부분 설치에서 혼란스러운 출력을 보일 때는, 디버깅보다 깨끗하게 처음부터 시작하는 것이 빠릅니다:

```bash
# Kali 패키지가 설치되어 있었다면 제거
sudo apt purge realtek-rtl88xxau-dkms

# rtl8812au의 모든 DKMS 항목 제거
for ver in $(sudo dkms status | grep rtl8812au | awk -F'[,/]' '{print $2}' | tr -d ' '); do
    sudo dkms remove rtl8812au/$ver --all
done

# 남아 있는 소스 디렉터리가 있으면 제거
sudo rm -rf /usr/src/rtl8812au*

# 오래된 모듈 캐시 정리
sudo depmod -a

# 새로 클론하고 설치
git clone https://github.com/aircrack-ng/rtl8812au.git /tmp/rtl8812au
cd /tmp/rtl8812au
sudo make dkms_install
sudo modprobe 88XXau
ip link show | grep wlan
```

{{< alert "triangle-exclamation" >}}
DKMS 항목을 제거하는 루프는 버전을 찾지 못하면 조용히 실패합니다 — 괜찮습니다. 중요한 단계는 손상된 상태로 남아 있을 수 있는 소스 트리를 제거하는 `sudo rm -rf /usr/src/rtl8812au*`입니다.
{{< /alert >}}

---

## 예방 체크리스트

작업 중 예기치 않은 상황을 피하려면 모든 시스템 업데이트 전에 이 체크리스트를 사용하세요:

**`apt upgrade` 전:**

```bash
# 어떤 커널 패키지가 대기 중인지 정확히 확인
apt list --upgradable 2>/dev/null | grep linux-image
```

새 커널이 들어올 예정이라면, 운영 작업 전에 테스트 재부팅을 계획하세요.

**모든 업그레이드와 재부팅 후:**

```bash
# 어댑터가 복귀했는지 확인
ip link show | grep -E "wlan|wlp"

# 모니터 모드가 여전히 작동하는지 확인
sudo airmon-ng check
```

**대비책을 마련하세요:**
- Kali Live 이미지가 담긴 USB 드라이브(또는 정상 작동하는 드라이버가 설치된 두 번째 어댑터)를 준비해 두세요. 예정된 작업 중 연결 문제는 비용이 큽니다 — 물리적 대비책은 준비하는 데 몇 분이면 되고 위기를 넘길 수 있습니다.

**Kali에서 중요한 드라이버 패키지 고정:**

```bash
# 업그레이드 중 특정 드라이버 패키지가 자동 제거되는 것을 방지
sudo apt-mark hold realtek-rtl88xxau-dkms
```

드라이버를 명시적으로 업그레이드하기 전에 고정을 해제하세요:

```bash
sudo apt-mark unhold realtek-rtl88xxau-dkms && sudo apt upgrade realtek-rtl88xxau-dkms
```

---

{{< faq >}}

## 요약

커널 업데이트 후 ALFA 드라이버 장애는 예측 가능한 패턴을 따르며 예측 가능한 해결책이 있습니다. RTL8812AU 어댑터는 `dkms autoinstall`(또는 `aircrack-ng/rtl8812au`에서 새로 클론)과 일치하는 커널 헤더가 필요합니다. MT7921AUN 어댑터는 `firmware-misc-nonfree`와 5.18 이상의 커널이 필요합니다. 두 경우 모두 장기적인 해결책은 `apt upgrade`가 아니라 `apt full-upgrade`를 표준 업데이트 명령으로 사용하는 것이며, 이는 헤더와 커널을 보조를 맞춰 유지합니다.

---

**관련 가이드:**
- [Kali Linux와 Ubuntu에 ALFA USB WiFi 드라이버 설치하기](/ko/blog/install-alfa-driver-kali-ubuntu/) — 드라이버를 처음 설치한다면 여기서 시작하세요
- [AWUS036ACH Kali Linux 설정 가이드](/ko/blog/awus036ach-kali-linux-setup/) — 모니터 모드 및 패킷 인젝션 검증을 포함한 전체 설정 안내

## 참고 문헌

1. [aircrack-ng 공식 rtl8812au 드라이버](https://github.com/aircrack-ng/rtl8812au)
2. [DKMS 공식 문서](https://github.com/dell/dkms)
3. [Kali Linux 패키지 관리 문서](https://www.kali.org/docs/general-use/package-management/)
4. [Linux Kernel 공식 문서](https://www.kernel.org/doc/html/latest/)
5. [MediaTek MT7921 드라이버](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek/mt7921)
