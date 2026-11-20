---
title: "MediaTek와 Realtek, Linux USB 네트워크 카드 드라이버 선택 가이드"
date: 2026-09-03
draft: false
slug: "alfa-usb-wifi-linux-driver-guide"
tags:
  - "ALFA"
  - "Linux-Driver"
  - "MediaTek"
  - "Realtek"
  - "in-kernel"
  - "out-of-tree"
  - "DKMS"
  - "mt76"
  - "rtl8812au"
categories:
  - "Hardware Guide"
description: "Yopitek ALFA USB 네트워크 카드 기술 문서 초판으로, MediaTek 및 Realtek 칩셋을 포함한 6개 모델을 다룹니다."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> **기술 지원 문서 · 초판 2026-09-03 (blog-writing-rules.md v1.0 사양에 따라 작성)**
> 대상 범위: 본 기술 문서 매트릭스는 Yopitek 현행 ALFA USB 네트워크 카드 6개 모델을 다룹니다(MediaTek 3개 모델, Realtek 3개 모델).
> 관련 글: [ALFA 무선 네트워크 카드는 NVIDIA DGX Spark를 지원하나요](https://yupitek.com/ko/blog/alfa-nvidia-dgx-spark-compatibility/) | [ALFA 무선 네트워크 카드는 OpenWrt를 지원하나요](https://yupitek.com/ko/blog/alfa-openwrt-router-compatibility/) | [ALFA 무선 네트워크 카드는 NVIDIA Jetson Nano를 지원하나요](https://yupitek.com/ko/blog/alfa-nvidia-jetson-nano-compatibility/) | [ALFA 무선 네트워크 카드는 Tomato를 지원하나요](https://yupitek.com/ko/blog/alfa-tomato-router-compatibility/) | [ALFA 무선 네트워크 카드는 DD-WRT를 지원하나요](https://yupitek.com/ko/blog/alfa-ddwrt-router-compatibility/)

## 한 줄 결론

**본문에서 다루는 6개 모델 중, MediaTek 칩을 탑재한 3개 모델(MT7610U / MT7612U / MT7921AUN)은 최신 커널에 드라이버가 내장되어 있어 플러그 앤 플레이로 동작하지만, Realtek 칩을 탑재한 3개 모델(RTL8812AU / RTL8821CU / RTL8832BU)은 구형 커널에서 out-of-tree 드라이버를 수동으로 컴파일해야 합니다. 다만 최신 커널에서는 메인라인에 편입되었습니다(EACS의 rtw88_8821cu는 커널 6.2부터, ACH/ACS는 6.13부터, AX/AXER는 6.17부터 내장이며, GX10 커널 6.17에서는 모두 설치가 필요 없습니다).** 편의성을 우선한다면 주문 전에 반드시 칩셋을 확인하시기 바랍니다.

---

## 1막: 상황 — 어떤 제품은 꽂자마자 쓰이는데 어떤 제품은 두 시간을 컴파일해야 하는 이유

실제 사례 두 가지:

- 고객 A는 **AWUS036ACM**을 Ubuntu 데스크톱에 연결하고 `lsusb`를 실행하자, 별도의 소프트웨어 설치 없이 NetworkManager가 자동으로 wlan0을 인식했습니다.
- 고객 B는 같은 장비에 **AWUS036ACH**를 연결했지만 네트워크 카드가 반응하지 않았습니다. 결국 GitHub에서 소스 코드를 내려받고, 빌드 도구를 설치하고, 컴파일한 뒤 재부팅해야 했습니다.

이 차이는 운이나 Linux 배포판 때문이 아니라, **칩셋**이 어느 진영에 속하는지에 달려 있습니다. MediaTek의 USB WiFi 칩셋 드라이버(mt76 계열)는 오래전부터 Linux 커널 메인라인에 통합되어 있지만, Realtek의 USB WiFi 칩셋 드라이버는 구형 커널에서는 out-of-tree(커널 외부)로 배포되어 커뮤니티가 유지보수하는 드라이버 저장소에서 수동으로 설치해야 합니다(최근 커널에서는 일부가 메인라인에 편입되었습니다. 아래 참조).

## 2막: 원리 — in-kernel과 out-of-tree는 무엇이 다른가?

### MediaTek: mt76 메인라인 드라이버, 플러그 앤 플레이

MediaTek USB 칩 드라이버는 커널의 **mt76** 서브시스템이 담당합니다:

| 모델 | 칩셋 | 커널 드라이버 모듈 | 무설정 동작 조건 |
|---|---|---|---|
| AWUS036ACHM | MT7610U | mt76x0u | 커널 내장, 버전 요건 고려 불필요 |
| AWUS036ACM | MT7612U | mt76x2u | 커널 내장, 버전 요건 고려 불필요 |
| AWUS036AXML / AXM | MT7921AUN | mt7921u | **커널 5.18 이상 필요** |

⚠️ 유일한 함정: **MT7921AUN의 커널 요건은 5.18 이상입니다.** 구형 플랫폼(예: Jetson Nano의 JetPack 4.x, 커널 4.9)은 백포트가 불가능하여 직접 사용할 수 없습니다. 이는 당사의 Jetson Nano 기술 문서에서 검증한 결론입니다([ALFA 무선 카드는 NVIDIA Jetson Nano를 지원하나요](https://yupitek.com/ko/blog/alfa-nvidia-jetson-nano-compatibility/) §7.4 참조).

### Realtek: 구형 커널은 out-of-tree 수동 컴파일, 최신 커널은 메인라인 내장

Realtek USB 칩은 구형 커널에서는 사용 가능한 메인라인 드라이버가 없어 커뮤니티가 유지보수하는 드라이버 저장소에 의존합니다. 최신 커널에서는 EACS의 rtw88_8821cu(커널 6.2 이상), ACH/ACS(6.13 이상), AX/AXER(6.17 이상)가 내장되어 설치가 필요 없습니다. 가장 활발한 유지보수자는 **morrownr**이며, 본 목록의 3개 칩은 각각 3개의 저장소에 대응합니다:

| 모델 | 칩셋 | 드라이버 저장소 (morrownr 유지보수) | 2026-09-03 기준 검증 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | [8812au-20210820](https://github.com/morrownr/8812au-20210820) | ✅ 검증됨 |
| AWUS036EACS | RTL8821CU | [8821cu-20210916](https://github.com/morrownr/8821cu-20210916) | ✅ 검증됨 |
| AWUS036AX / AXER | RTL8832BU | [rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | ✅ 검증됨 |

### 대표적인 세 가지 환경에 적용하기

| 환경 | 커널 | MediaTek 진영 (3개 모델) | Realtek 진영 (3개 모델) |
|---|---|---|---|
| GB10 / DGX Spark 계열 플랫폼 | 6.x + aarch64 | 모두 사용 가능 (mt76 내장) | 커널 6.17(GX10 실측)에서는 모두 내장되어 설치 불필요, 구형 커널은 컴파일 필요 (ARM64 가능) |
| Jetson Nano (JetPack 4.x) | 4.9 | 7610U/7612U 사용 가능, MT7921AUN **사용 불가** | 8812au 컴파일 가능(ARM64 지원), 나머지는 미검증 |
| OpenWrt 라우터 | 버전에 따라 다름 | 모두 사용 가능 (MT7921AUN은 23.05 이상 필요) | 해당 kmod 또는 컴파일 필요, 난도 높음 |

(각 환경별 완전한 판정 매트릭스는 [ALFA 무선 카드는 NVIDIA DGX Spark를 지원하나요](https://yupitek.com/ko/blog/alfa-nvidia-dgx-spark-compatibility/), [ALFA 무선 카드는 NVIDIA Jetson Nano를 지원하나요](https://yupitek.com/ko/blog/alfa-nvidia-jetson-nano-compatibility/), [ALFA 무선 카드는 OpenWrt를 지원하나요](https://yupitek.com/ko/blog/alfa-openwrt-router-compatibility/)에서 확인할 수 있습니다.)

## 3막: 도구 상자 — 3분 결정 프로세스와 설치 단계

### 결정 테이블: 네트워크 카드를 받았을 때 가장 먼저 밟을 세 단계

```bash
# 1단계: 시스템이 네트워크 카드를 인식하는지 확인 (VID:PID 기록)
lsusb

# 2단계: 해당 드라이버가 커널에 로드되었는지 확인
lsmod | grep -E "mt76|rtl8"

# 3단계: 커널 버전 확인 (MT7921AUN 사용 가능 여부 판단)
uname -r
```

결정 로직 (상위 기준: 위 6개 모델 표):

1. `lsusb`에 **MediaTek / MT76xx**가 표시됨 → in-kernel 진영. 커널 5.18 이상(MT7921AUN 모델) 또는 최근 커널이면 플러그 앤 플레이.
2. `lsusb`에 **Realtek RTL88xx**가 표시됨 → out-of-tree 진영. 아래 설치 단계를 따릅니다.
3. `lsusb`에 새 장치가 **전혀** 표시되지 않음 → 먼저 USB 포트/케이블을 교체하여 하드웨어 문제를 배제하고, 해당 모델이 Wi-Fi 6 RTL8832BU인지 확인합니다(일부 배치는 `usb_modeswitch`가 필요하며, 이는 개별 모델의 문제로 본 개요의 범위를 벗어나므로 상세히 다루지 않습니다).

### Realtek 진영 공통 설치 (AWUS036ACH 예시)

```bash
# 1단계: 빌드 의존성 설치 (Debian/Ubuntu)
sudo apt install build-essential dkms linux-headers-$(uname -r)

# 2단계: 드라이버 소스 코드 받기 (모델별 저장소는 위 표 참조)
git clone https://github.com/morrownr/8812au-20210820
cd 8812au-20210820

# 3단계: 설치 (DKMS 등록, 커널 변경 시 재설치 불필요)
sudo ./install-driver.sh

# 4단계: 재부팅 후 검증
lsmod | grep 88XXau
ip link   # 새 wlan 인터페이스가 표시되어야 함
```

> **표 1 결론: 설치 전에 결정하라 — 먼저 칩셋을 확인하면 90초 만에 "플러그 앤 플레이"인지 "저장소에서 컴파일"해야 하는지 판단할 수 있으며, 먼저 벽에 부딪힐 필요가 없습니다.**

### 구매 권장 사항 (결론)

- **컴파일 불필요**: MediaTek 진영(AWUS036ACHM / ACM / AXML)을 선택하면 최근 커널에서 모두 플러그 앤 플레이입니다.
- **Wi-Fi 6이 필요하고 컴파일은 피하고 싶은 경우**: AWUS036AXML(MT7921AUN)을 선택하되, 커널 5.18 이상인지 먼저 확인하십시오.
- **특수 요구사항이 있어 Realtek이 반드시 필요한 경우**(예: 특정 모니터 모드 툴체인): 드라이버 컴파일에 20~40분을 확보하고, 대상 플랫폼에 커널 헤더가 있는지 확인하십시오.

## 알려진 제한 사항 및 반박 조건

본 글의 결론은 다음 조건에서는 성립하지 않으므로, 대체 방안을 채택하시기 바랍니다:

1. **커널 5.17 이하 + MT7921AUN**: mt7921u 드라이버는 백포트할 수 없으며(최신 커널 인프라에 의존), 이 경우 결론은 "사용 불가"로 뒤바뀝니다. 본 글에서 가장 중요한 예외입니다.
2. **비 x86/ARM64 Linux**(예: 일부 MIPS 라우터): morrownr 저장소의 컴파일 가능 여부를 보장할 수 없으므로, OpenWrt의 kmod를 우선 사용해야 합니다([ALFA 무선 카드는 OpenWrt를 지원하나요](https://yupitek.com/ko/blog/alfa-openwrt-router-compatibility/) 참조).
3. **드라이버 저장소 버전 변화**: morrownr 저장소는 날짜로 명명되며(예: rtl8852bu-20250826), 향후 버전이 업데이트되거나 삭제될 수 있으므로, 설치 전에 저장소 상태를 반드시 확인하십시오.
4. **모니터 모드 / AP 모드 기능**: 동일 칩이라도 커널 버전에 따라 기능이 다릅니다(예: OpenWrt 22.03 이상의 rtl8812au-ct는 24.10에서 크래시 보고가 있습니다). 상세 기능 매트릭스는 각 환경별 전용 글을 참조하십시오.
5. **RTL8832BU(AWUS036AX/AXER)는 본문 6개 기종에는 포함되지 않지만 고객 지원에서 자주 문의받습니다**: rtw89_8852bu 드라이버는 kernel 6.17부터 mainline에 포함되며, GX10(kernel 6.17)에서 monitor 동작, 2.4G 인젝션 AX 96%, AXER 73%였습니다. 오래된 kernel에서만 커뮤니티 드라이버 morrownr/rtl8852bu가 필요합니다. 고객에게 답변할 때는 먼저 kernel 버전을 확인하세요.

## 참고 출처

| 출처 | 설명 | URL | 검증 상태 | 검증 일자 |
|---|---|---|---|---|
| morrownr/8812au GitHub | RTL8812AU Linux 드라이버 | https://github.com/morrownr/8812au-20210820 | ✅ 검증됨 | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8821CU Linux 드라이버(커널 6.2 이전용) | https://github.com/morrownr/8821cu-20210916 | ✅ 검증됨 | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux 드라이버 | https://github.com/morrownr/rtl8852bu-20250826 | ✅ 검증됨 | 2026-09-03 |
| Yopitek ALFA 제품 개요 | 현행 모델 및 사양 | https://yupitek.com/ko/products/alfa/ | ✅ 검증됨 | 2026-09-03 |
| Yopitek 블로그: Soft AP 가이드 | AP 모드 구현 검증 글 | https://yupitek.com/ko/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 검증됨 | 2026-09-03 |
| 본 사이트 기술 문서 9편 | 판정 매트릭스 및 환경 검증 근거 | 상대 링크(글 상단의 "관련 글" 참조) | ✅ 검증됨 | 2026-09-03 |

> 공식 커널 mt76 wiki 페이지: https://wireless.wiki.kernel.org/en/users/drivers/mediatek (검증됨, 각 칩이 지원되는 최초 커널 버전을 나열하므로 빠른 참고 자료로 활용 가능)

## 면책 조항

본 문서는 Yopitek Ltd의 기술 지원팀이 작성하였으며, 사양과 드라이버 상태는 커널 및 드라이버 저장소의 업데이트에 따라 달라질 수 있습니다. 설치 전에 공식 저장소와 제조사 사양 페이지를 참조하시기 바랍니다. ALFA Network는 당사의 공식 대리 브랜드입니다.
