---
title: "AWUS036AXML 모니터 모드 펌웨어 해결: 액티브 모드 크래시 문제 수정"
description: "Kali Linux에서 AWUS036AXML 모니터 모드 펌웨어 크래시를 해결하는 방법. MT7921AUN 펌웨어 업데이트, 커널 버전 요구 사항, 액티브 모드와 패시브 모드 우회 방법, hcxdumptool 대안을 다룹니다."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "AWUS036AXML은 왜 액티브 모니터 모드에서 크래시가 발생합니까?"
    answer: "MT7921AUN은 펌웨어 기반 MAC 아키텍처를 사용합니다. 현재의 Linux mt7921u 드라이버와 펌웨어 조합은 액티브 인젝션에 필요한 커맨드 경로를 완전하게 구현하지 못합니다. aireplay-ng를 실행하면 인터페이스가 사라집니다."
  - question: "MT7921AUN 액티브 모드 크래시는 어떻게 해결합니까?"
    answer: "firmware-misc-nonfree 패키지를 최신 버전으로 업데이트하고, 커널을 6.6 이상으로 업그레이드하며, 고속 디인증(deauthentication) 플러딩을 피하십시오. 이렇게 하면 크래시가 개선될 수는 있지만 완전히 제거되지는 않을 수 있습니다."
  - question: "hcxdumptool은 패킷을 인젝션하지 않고 어떻게 PMKID를 캡처합니까?"
    answer: "hcxdumptool은 패시브 모드로 동작하며, 액세스 포인트가 송출하는 비콘(beacon)과 프로브(probe) 프레임에서 PMKID를 추출합니다. 어떤 패킷도 전송하지 않으므로 펌웨어 크래시를 유발하지 않습니다."
  - question: "AWUS036AXML에서 패시브 모니터링의 한계는 무엇입니까?"
    answer: "패시브 모니터링은 비콘, 핸드셰이크, PMKID를 캡처할 수 있지만, 디인증, 프로브 요청, 연결(association) 플러딩과 같은 액티브 작업은 수행할 수 없습니다. 이러한 작업에는 AWUS036ACH를 사용하십시오."
  - question: "어떤 커널 버전이 MT7921AUN의 안정성을 개선합니까?"
    answer: "커널 6.1 LTS 이상에는 여러 mt7921u 안정성 패치가 포함되어 있습니다. 커널 6.6 이상에는 MediaTek USB 드라이버 스택에 대한 추가 개선 사항이 포함되어 있습니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036AXML", "MT7921AUN", "monitor-mode", "firmware", "kali-linux", "troubleshooting", "wifi-6e"]
featureimage: "/images/blog/awus036axml-firmware-monitor-mode-fix.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

**ALFA AWUS036AXML**은 ALFA Network의 플래그십 WiFi 6E 어댑터로, MediaTek MT7921AUN 칩셋을 기반으로 합니다. 보안 연구자에게 트라이 밴드(2.4 / 5 / 6 GHz) 지원을 제공하며, 2026년 기준 6 GHz 대역에서 패시브 모니터링이 가능한 몇 안 되는 USB 어댑터 중 하나입니다. 사이트 서베이, PCAP 캡처, PMKID 수집과 같은 여러 사용 사례에서 매우 뛰어난 성능을 발휘합니다.

{{< tldr >}}
AWUS036AXML의 mt7921u 드라이버는 액티브 패킷 인젝션 중에 펌웨어 크래시를 유발합니다. 이 글에서는 근본 원인, 진단 단계, 그리고 펌웨어 업데이트, 커널 업그레이드, 패시브 캡처를 위한 hcxdumptool 전환 등의 해결 방법을 다룹니다.
{{< /tldr >}}





하지만 사용자들이 예상치 못하게 겪게 되는 알려진 문제가 있습니다. 바로 **액티브 모니터 모드 명령이 펌웨어를 크래시시킨다**는 점입니다. `aireplay-ng`나 `mdk4`와 같은 도구를 실행하면 `wlan0mon` 인터페이스가 완전히 사라지며, 어댑터를 뽑았다가 다시 꽂아야만 복구할 수 있습니다. 이는 하드웨어 결함이 아니라 현재 Linux `mt7921u` 스택의 드라이버 및 펌웨어 한계입니다.

이 가이드는 근본 원인을 설명하고, 진단 단계를 안내하며, 세션을 잃지 않고 작업을 계속할 수 있도록 구체적인 해결책과 우회 방법을 제공합니다. 작업 중인 침투 테스터든 새 랩을 구축하는 연구자든, 이 글이 막힌 지점에서 벗어나도록 도와줄 것입니다.

---

## 문제: 액티브 모니터 모드 크래시

### 증상

모니터 모드를 활성화한 뒤 `aireplay-ng --test wlan0mon` 같은 액티브 명령이나 디인증/인젝션 작업을 실행하면, `wlan0mon` 인터페이스가 `ip link` 및 `iwconfig` 출력에서 사라집니다. 어댑터는 응답하지 않게 되며, 물리적으로 분리했다가 다시 연결하지 않으면 복구할 수 없습니다. 어떤 경우에는 크래시 직후 `dmesg`에 펌웨어 오류나 리셋 이벤트가 표시됩니다.

패시브 작업, 즉 `airodump-ng`를 통한 스캐닝이나 원시(raw) 프레임 캡처는 액티브 인젝션이 트리거되지 않는 한 크래시 전후로 계속 정상 동작합니다.

### 근본 원인

**MT7921AUN 칩셋**은 펌웨어 기반 MAC 아키텍처를 사용합니다. `mt7921u` Linux 커널 드라이버는 모니터 모드에서의 프레임 인젝션을 비롯한 특정 하위 계층 작업을 처리하기 위해 칩셋에 내장된 펌웨어에 의존합니다. 현재의 펌웨어와 드라이버 조합은 Linux에서 모니터 모드의 액티브 인젝션에 필요한 커맨드 경로를 완전하게 구현하지 못합니다.

참고: GX10의 stock kernel 6.17 실측에서 인젝션 실패의 주된 원인은 커널 6.16 이후의 mac80211 chanctx 회귀이며 칩 자체의 한계가 아닙니다. 커뮤니티 patched 드라이버로는 인젝션이 동작하지만, 펌웨어가 전송 속도를 1/6 Mbps로 고정하여 HT/VHT 프레임은 인젝션할 수 없습니다.

반면 **패시브 모니터링**(이미 공중에 존재하는 프레임을 스니핑)은 펌웨어가 무언가를 전송할 필요가 없으므로 크래시를 유발하지 않고 동작합니다. 이 문제는 전송 경로(transmit-path) 작업에 한정됩니다. 디인증 프레임, 프로브 요청, 연결 플러딩, 그리고 이와 유사한 액티브 작업이 그것입니다.

{{< alert "triangle-exclamation" >}}
**알려진 펌웨어 크래시 버그.** 이는 2026년 초 기준 Linux `mt7921u` 드라이버에서 확인된 문제입니다. AWUS036AXML 및 기타 MT7921AUN 기반 USB 어댑터에 영향을 미칩니다. 향후 커널 또는 펌웨어 업데이트에서 해결될 수 있으므로, 최신 상태는 [드라이버 설치 가이드](/ko/blog/install-alfa-driver-kali-ubuntu/)에서 확인하십시오.
{{< /alert >}}

---

## 진단: 당신의 문제가 맞습니까?

다른 문제가 아니라 MT7921AUN 액티브 모드 크래시를 겪고 있는지 확인하려면 다음 순서를 따르십시오.

```bash
# Check adapter is recognized
lsusb | grep -i mediatek

# Check driver loaded
lsmod | grep mt7921u

# Check kernel version (must be >= 5.18)
uname -r

# Start monitor mode
sudo airmon-ng start wlan0

# Test passive capture (should work fine)
sudo airodump-ng wlan0mon

# Test active injection (may crash)
sudo aireplay-ng --test wlan0mon
```

`aireplay-ng --test` 실행 후 어댑터가 `ip link`에서 사라진다면, 펌웨어 크래시 버그를 확인한 것입니다.

커널 로그를 통한 추가 검증은 다음과 같습니다.

```bash
sudo dmesg | grep -E "mt7921|firmware|reset" | tail -20
```

aireplay-ng 호출 직후에 `mt7921u: firmware crash`, `mt7921u: chip reset`, `usb disconnect`와 같은 메시지가 나타나는지 확인하십시오. 이러한 메시지는 펌웨어 수준의 장애를 확인해 줍니다.

{{< alert "circle-info" >}}
**패시브 캡처는 영향을 받지 않습니다.** `airodump-ng`는 동작하지만 `aireplay-ng`가 크래시된다면, 이것이 바로 알려진 MT7921AUN 버그입니다. 아래 해결 방법으로 진행하십시오.
{{< /alert >}}

---

## 해결책 1: 펌웨어 패키지 업데이트

가장 효과적인 첫 단계는 최신 MT7921 펌웨어 파일을 확보하는 것입니다. 구 버전 펌웨어는 크래시가 더 잘 발생하며, 업데이트된 펌웨어는 일부 액티브 작업의 안정성을 개선합니다.

```bash
sudo apt update
sudo apt install firmware-misc-nonfree

# Or manually install latest mt7921 firmware from linux-firmware repo
sudo apt install git
git clone https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
sudo cp linux-firmware/mediatek/mt7921* /lib/firmware/mediatek/
sudo modprobe -r mt7921u
sudo modprobe mt7921u
```

펌웨어 파일을 업데이트한 후에는 드라이버를 다시 로드하고 액티브 모드를 재시험하십시오.

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

펌웨어 버전과 커널 버전의 일부 조합은 액티브 명령에서 안정성이 크게 개선되는 것으로 나타납니다. 크래시가 완전히 해결되지 않더라도, 업데이트된 펌웨어는 장애 빈도를 줄이고 제한적인 액티브 작업이 성공적으로 완료되도록 해 줄 수 있습니다.

---

## 해결책 2: 최신 커널 사용

`mt7921u` 드라이버는 업스트림 Linux 커널에서 활발하게 유지 관리되고 있습니다. 안정성, 펌웨어 커맨드 처리, 모니터 모드와 관련된 드라이버 수준의 패치가 5.18 이후의 커널 업데이트에 포함되어 왔습니다. 더 최신 커널을 사용하는 것은 동작을 개선하는 가장 확실한 방법 중 하나입니다.

현재 커널 버전을 확인하십시오.

```bash
uname -r
```

Kali Linux에서 사용 가능한 최신 커널로 업데이트하십시오.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

재부팅 후 새 커널 버전을 확인하십시오.

```bash
uname -r
```

목표는 가장 완전한 `mt7921u` 드라이버 패치를 위한 **커널 6.1 LTS 이상**입니다. 커널 6.6 이상에는 사용자 보고에서 긍정적인 결과를 보인 MediaTek PCIe/USB 드라이버 스택에 대한 추가 개선 사항이 포함되어 있습니다. 2026년 기준 Kali Linux는 기본적으로 6.x 커널을 제공하므로, 일반적인 `full-upgrade`만으로도 별도의 수동 커널 설치 없이 충분히 최신 버전에 도달하는 것이 보통입니다.

{{< alert "circle-info" >}}
**커널 6.6+ 개선.** 여러 커뮤니티 보고에 따르면, 업데이트된 펌웨어와 함께 사용하는 커널 6.6은 MT7921AUN의 액티브 모드 크래시를 줄여줍니다(다만 항상 제거하지는 못합니다). 업그레이드 후에는 진단 순서를 다시 실행하여 자신의 특정 조합을 평가하십시오.
{{< /alert >}}

---

## 우회 방법: hcxdumptool 사용 (패시브 PMKID 캡처)

펌웨어 수준의 해결책으로 작업에 필요한 만큼 크래시가 완전히 해결되지 않는다면, `hcxdumptool`은 프레임 인젝션을 전혀 요구하지 않는 매우 효과적인 대체 워크플로를 제공합니다.

`hcxdumptool`은 **패시브 모드**로 동작합니다. 액세스 포인트가 송출하는 비콘과 프로브 프레임에서 직접 PMKID 값을 캡처합니다. 디인증 프레임을 전송하지 않고, 인젝션이 발생하지 않으며, 펌웨어 크래시도 유발되지 않습니다. AWUS036AXML은 이 워크플로를 완벽하게 처리합니다.

```bash
sudo apt install hcxdumptool hcxtools

# Passive capture — no deauth, no firmware crash
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1

# Convert to hashcat format
hcxpcapngtool -o hash.hc22000 capture.pcapng

# Crack with hashcat
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

이 워크플로는 아무것도 전송하지 않고 비콘 프레임에서 PMKID를 캡처합니다. 무선 매체의 관점에서 보면 완전히 패시브한 방식입니다. PMKID 기반 WPA/WPA2 평가에서는, 클라이언트가 존재하거나 응답하는지에 의존하지 않기 때문에 전통적인 디인증-후-캡처 방식보다 오히려 더 효율적이라고 할 수 있습니다.

{{< alert "circle-info" >}}
**PMKID 캡처는 모든 최신 WPA2/WPA3 네트워크에서 동작합니다.** 액세스 포인트는 클라이언트의 연결 여부와 관계없이 비콘 프레임으로 PMKID를 송출합니다. 클라이언트의 통신 범위 안에 있을 필요 없이 AP만 있으면 됩니다. 덕분에 펌웨어 한계나 작업 범위상의 이유로 디인증을 사용할 수 없는 상황에서 패시브 PMKID 캡처가 이상적인 선택이 됩니다.
{{< /alert >}}

---

## 우회 방법: 액티브 인젝션에는 AWUS036ACH 사용

디인증을 통한 WPA 핸드셰이크 강제 캡처, WPS 열거, 또는 그와 유사한 작업처럼 실제로 액티브 프레임 인젝션이 반드시 필요한 작업에는, **AWUS036ACH**(RTL8812AU 칩셋)가 Kali Linux에서 성숙하고 충분히 검증된 드라이버 지원을 갖춘 확립된 해결책입니다.

권장되는 듀얼 어댑터 전문가 구성은 다음과 같습니다.

- **AWUS036AXML** → 5 GHz / 6 GHz에서 패시브 스캐닝 및 캡처
- **AWUS036ACH** → 2.4 GHz / 5 GHz에서 액티브 인젝션

이 조합은 Linux에서 수년간 액티브 모드 지원이 안정적이었던 RTL8812AU가 인젝션을 담당함으로써 모든 대역에 걸쳐 완전한 커버리지를 제공합니다. AWUS036AXML은 6 GHz 탐지와 고품질 패시브 캡처를 맡고, AWUS036ACH는 평가에 필요한 모든 액티브 작업을 처리합니다.

대부분의 최신 노트북과 USB 허브는 두 어댑터를 동시에 문제없이 다룹니다. 작업 시작 시점에 각각을 별도의 논리적 역할로 지정하여 워크플로를 깔끔하게 유지하십시오.

두 어댑터의 설정 세부 사항은 [AWUS036AXML 리뷰](/ko/blog/awus036axml-wifi-6e-review/)와 [패킷 인젝션 가이드](/ko/blog/packet-injection-guide/)를 참고하십시오.

---

## 액티브 모드가 동작하는 경우

액티브 모드가 항상 실패하는 것은 아니라는 점을 짚어 둘 필요가 있습니다. 커뮤니티 구성원들은 MT7921AUN에서 안정적이거나 거의 안정적인 액티브 모드 동작을 만들어내는 여러 조건을 보고했습니다.

- **커널 6.6 이상**과 firmware-misc-nonfree 20240610 이상
- `aireplay-ng --deauth`의 버스트 모드 사용 피하기(고속 패킷 전송률의 디인증 플러딩이 단일 프레임 작업보다 크래시를 유발할 가능성이 높습니다)
- 연속적인 디인증 스트림 대신 `--deauth 1` 또는 `--deauth 3` 사용
- 어댑터를 USB 3.0 포트에 연결하기(USB 2.0의 대역폭 제약은 펌웨어 커맨드 파이프라인에 부담을 가중시킵니다)
- 인젝션 시 5 GHz보다 2.4 GHz에서 동작하기(일부 드라이버 버전에서는 저주파 대역이 더 안정적으로 보입니다)

작업이 실제 운용에 들어가기 전 신중한 테스트를 허용한다면, 의존하기 전에 각 액티브 작업을 테스트 네트워크에서 개별적으로 검증하십시오. 자신의 특정 커널 및 펌웨어 조합에서 어떤 명령과 파라미터가 안정적으로 동작하는지 기록해 두십시오.

{{< alert "triangle-exclamation" >}}
**실제 작업 전에 테스트하십시오.** 액티브 모드가 동작하는 것처럼 보이더라도, MT7921AUN 펌웨어는 부하가 걸린 상태에서 작업 도중에 크래시될 수 있습니다. AWUS036AXML을 액티브 작업에 사용할 때는 항상 복구 계획(백업 어댑터 또는 패시브 전용 워크플로)을 마련해 두십시오.
{{< /alert >}}

---

## 펌웨어가 업데이트되었는지 확인하기

최신 펌웨어 파일을 보유하고 있는지, 그리고 정확히 어떤 버전이 로드되어 있는지 확인하려면 다음과 같이 하십시오.

```bash
# Check current firmware file date
ls -la /lib/firmware/mediatek/mt7921*

# Check driver version and source
modinfo mt7921u | grep -E "version|filename"

# Check kernel messages for firmware loading
sudo dmesg | grep mt7921
```

펌웨어가 성공적으로 로드되면 `dmesg` 출력에 다음과 같은 내용이 표시됩니다.

```
mt7921u 1-2.3:1.0: firmware init done
mt7921u 1-2.3:1.0: HW/SW Version: ...
```

`firmware load failed`나 그와 유사한 오류가 보인다면, 펌웨어 파일이 없거나 손상된 것입니다. `firmware-misc-nonfree`를 재설치하거나 해결책 1에서 설명한 대로 `linux-firmware` 저장소에서 파일을 수동으로 복사하십시오.

MT7921의 최신 버전을 실행 중인지 판단하려면, 펌웨어 파일 날짜를 `linux-firmware` 저장소의 커밋 이력과 대조하십시오.

---

{{< faq >}}

## 요약: AWUS036AXML 최적 활용 사례

MT7921AUN의 현재 Linux 한계를 이해하면, AWUS036AXML을 진정으로 강점을 발휘하는 곳에 배치하는 데 도움이 됩니다.

- ✅ **패시브 WiFi 6E 스캐닝 및 PCAP 캡처** — 완벽하게 동작합니다
- ✅ **hcxdumptool PMKID 캡처** — 인젝션 불필요, 펌웨어 크래시 없음
- ✅ **6 GHz 네트워크 탐지** — 6 GHz 대역에서의 airodump-ng 패시브 스캐닝
- ✅ **WiFi 6E 사이트 서베이 및 간섭 분석** — 트라이 밴드 패시브 모니터링
- ✅ **기본 WPA2 핸드셰이크 캡처** — 기존 트래픽에서의 핸드셰이크 패시브 캡처
- ⚠️ **액티브 프레임 인젝션** — MT7921AUN 펌웨어가 성숙할 때까지는 AWUS036ACH를 대신 사용하십시오
- ⚠️ **디인증 플러딩** — 펌웨어 크래시 위험이 있으니 커널 6.6+에서 신중하게 테스트하십시오
- ⭐ **최적의 워크플로: AWUS036AXML + AWUS036ACH를 함께 휴대** — 완전한 커버리지 확보

AWUS036AXML은 뛰어난 패시브 캡처 어댑터이자 6 GHz 작업에 알맞은 도구입니다. 여기에 인젝션을 위한 AWUS036ACH를 조합하면, 아직 성숙 중인 펌웨어에 의존하지 않고도 모든 대역과 모든 작업 유형을 아우르는 전문가급 구성을 갖추게 됩니다.

---

## 관련 가이드

- [AWUS036AXML 전체 리뷰](/ko/blog/awus036axml-wifi-6e-review/) — 완전한 하드웨어 리뷰 및 Kali Linux 설정
- [패킷 인젝션 가이드](/ko/blog/packet-injection-guide/) — aireplay-ng 사용법과 인젝션 테스트 방법론
- [드라이버 설치 가이드](/ko/blog/install-alfa-driver-kali-ubuntu/) — Kali 및 Ubuntu에서 MT7921AUN 및 RTL8812AU 드라이버 설치

## 참고 문헌

1. [Linux Firmware Repository (kernel.org)](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git)
2. [Linux Kernel mt76 Driver](https://wireless.wiki.kernel.org/en/users/drivers/mediatek)
3. [aircrack-ng Toolkit](https://www.aircrack-ng.org/)
4. [hcxdumptool GitHub Project](https://github.com/ZerBea/hcxdumptool)
5. [ALFA Network Official Support](https://www.alfa.com.tw/)
