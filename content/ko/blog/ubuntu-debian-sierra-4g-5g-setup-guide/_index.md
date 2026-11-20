---
title: "Ubuntu / Debian / Linux Mint에서 Sierra 4G/5G 모듈 설치 완벽 가이드: EM7455, EM7565, EM919x, MC7455 설정 및 GNSS 측위"
description: "Ubuntu/Debian/Linux Mint에 Sierra 4G/5G 모듈을 설치하려면 어떻게 해야 할까요? 이 가이드는 ModemManager 설치, qmicli/mbimcli를 이용한 다이얼링, GNSS 측위 설정을 단계별로 안내합니다. EM7455, EM7565, EM919x, MC7455를 다룹니다."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "ubuntu-debian-sierra-4g-5g-setup-guide"
tags: ["Sierra Wireless", "Ubuntu", "Debian", "Linux", "GNSS"]
categories: ["Technical"]
author: "Yopitek"
lastmod: 2026-11-20
related_product: "/ko/products/sierra/"
faq:
  - question: "Ubuntu에서 Sierra 4G/5G 모듈로 바로 인터넷에 접속할 수 있습니까?"
    answer: "네. modemmanager, libqmi-utils 및 관련 패키지를 설치한 다음 NetworkManager에 APN을 입력하면 온라인 상태가 됩니다."
  - question: "Linux에서 Sierra 모듈의 GNSS 측위를 활성화하려면 어떻게 합니까?"
    answer: "ModemManager 명령을 사용합니다. 먼저 mmcli -m 0 --location-enable-gps-raw를 실행한 다음 --location-get으로 좌표를 가져옵니다. GNSS 안테나가 연결되어 있는지 확인하십시오."
---

Ubuntu, Debian 또는 Linux Mint에 Sierra Wireless 모듈(EM7455, EM7565, MC7455, EM919x)을 설치하고 싶으십니까? Linux는 이러한 장치를 기본적으로 지원합니다. ModemManager와 libqmi-utils 같은 어떤 패키지를 설치해야 하는지만 알면 됩니다. 이 글은 하드웨어 연결과 드라이버 설치부터 다이얼링과 인터넷 접속, 마지막으로 GNSS 측위 기능 활성화까지 모든 과정을 단계별로 다룹니다. 드론을 만들든 산업용 컴퓨터를 만들든, 따라 하면 해낼 수 있습니다.

{{< tldr >}}
Ubuntu, Debian 또는 Linux Mint에 Sierra Wireless 모듈(EM7455, EM7565, MC7455, EM919x)을 설치하고 싶으십니까? Linux는 이러한 장치를 기본적으로 지원합니다. ModemManager와 libqmi-utils 같은 올바른 패키지만 설치하면 됩니다. 하드웨어 연결과 드라이버 설치부터 다이얼링과 GNSS 측위 활성화까지, 드론이든 산업용 컴퓨터든 따라 하면 됩니다.
{{< /tldr >}}

**한마디로, Linux에서 이러한 Sierra 모듈을 설치하는 것은 간단합니다. `apt`로 `modemmanager`와 관련 도구를 설치하고 NetworkManager로 연결하면, GPS 위치까지도 어렵지 않게 읽어 낼 수 있습니다.**

많은 분이 EM7455, EM7565, EM919x 또는 MC7455를 받아 메인보드에 꽂고 나서 인터넷에 어떻게 연결해야 할지 몰라 막막해합니다. 사실 Linux에서 이 모듈들에 대한 지원은 매우 성숙해 있습니다. 모두 QMI 또는 MBIM 프로토콜을 사용하여 USB로 통신합니다. 이 가이드에서는 설정 과정을 한 단계씩 안내합니다.

> 모든 사양과 기술 참조는 Sierra Wireless 공식 문서에서 가져왔습니다. Yopitek 정리.

---

## 시작 전에: 하드웨어를 파악하십시오

하드웨어가 잘못되어 있으면 소프트웨어 명령을 아무리 입력해도 소용이 없습니다.

| 모듈 | 폼 팩터 | 속도 등급 | 주요 Linux 프로토콜 | 안테나 수 |
|---|---|---|---|---|
| **EM7455** | M.2 (길이 42mm) | Cat 6 (300/50 Mbps) | QMI | 3 (Main, GNSS, Aux) |
| **EM7565** | M.2 (길이 42mm) | Cat 12 (600/150 Mbps) | QMI / MBIM | 3 (Main, GNSS, Aux) |
| **EM919x** (5G) | M.2 (길이 **52mm**) | 5G NR / LTE Cat 20 | MBPW 등 브로드밴드 패키지 | 4개 이상 |
| **MC7455** | mPCIe (레거시 슬롯) | Cat 6 (300/50 Mbps) | QMI | U.FL 커넥터 3개 |

**기억해야 할 두 가지 하드웨어 함정:**
1. **EM919x는 더 깁니다**: 52mm이므로 42mm 슬롯에는 맞지 않습니다. 억지로 끼우면 보드가 손상됩니다.
2. **안테나가 없으면 신호도 없습니다**: 최소한 주 안테나(Main)는 연결해야 합니다. 측위를 원한다면 GPS 안테나를 구입하여 전용 **GNSS 커넥터**에 연결하십시오.

---

## 1단계: 필수 Linux 도구 설치

Ubuntu / Debian / Linux Mint에서는 드라이버를 직접 작성하거나 컴파일할 필요가 없습니다. 패키지 저장소에 모두 준비되어 있습니다.

터미널을 열고 다음 두 줄을 실행하십시오.
```bash
sudo apt update
sudo apt install modemmanager libqmi-utils libmbim-utils
```
설치 후 서비스가 실행 중인지 확인합니다.
```bash
systemctl status ModemManager
```
이 도구들이 갖추어지면 Linux 시스템이 이제 이 4G/5G 카드를 이해할 수 있습니다.

---

## 2단계: 시스템이 카드를 인식하는지 확인

카드를 장착하고 부팅한 후, 다음 세 가지 명령으로 확인합니다.

1. **USB 하드웨어 확인:**
   ```bash
   lsusb
   ```
   (Sierra 또는 Qualcomm 장치가 보여야 합니다.)

2. **커널 드라이버 확인:**
   ```bash
   dmesg | grep -iE 'qmi|mbim|cdc|wwan'
   ```
   (`cdc-wdm0`와 `wwan0`가 보이면 인터페이스가 성공적으로 마운트된 것입니다.)

3. **ModemManager 상태 확인:**
   ```bash
   mmcli -L
   ```
   (모뎀 목록이 번호와 함께 표시됩니다. 번호를 적어 두십시오. 보통 `0`입니다.)

---

## 3단계: 쉬운 방법으로 다이얼링 (NetworkManager 사용)

Ubuntu나 Mint의 데스크톱 에디션을 사용 중이라면 내장 네트워크 관리자가 가장 편리한 선택입니다.

```bash
# Create a connection (replace "internet" with your carrier's APN)
nmcli connection add type gsm ifname cdc-wdm0 con-name "mobile" apn "internet"

# Bring it up!
nmcli connection up mobile
```
이것으로 끝입니다. `ip addr show`로 `wwan0`가 IP를 받았는지 확인할 수 있습니다.

### (고급) 데스크톱 없이 텍스트 모드로 연결
헤드리스 서버나 임베디드 보드에서는 `qmicli`로 모듈을 직접 제어할 수 있습니다.
```bash
sudo ip link set wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn=internet,ip-type=ipv4" --client-no-release-cid
sudo dhclient -v wwan0
```

---

## 4단계: GPS 측위 켜기!

이 모듈들은 모두 내장 GNSS 측위 시스템(GPS, GLONASS 등 지원)을 갖추고 있습니다.
공식 사양에 따르면 다음과 같습니다.
- EM7455 / EM7565 / MC7455: 핫 스타트 1초, 콜드 스타트 32초. 수평 정확도는 약 2 ~ 5미터.
- 5G EM919x: 더 빠른 콜드 스타트(≤28초)와 약간 더 나은 정확도(95%에서 <4m).

**Linux에서 좌표를 가져오는 가장 빠른 방법은 다음과 같습니다.**

1. GPS 기능을 활성화합니다.
```bash
mmcli -m 0 --location-enable-gps-raw
```
2. 현재 좌표를 가져옵니다.
```bash
mmcli -m 0 --location-get
```
현재 위도와 경도가 바로 출력됩니다. 위치를 다른 프로그램에 실시간으로 전달하려면 `gpsd`와 함께 사용하십시오.

---

## 흔한 함정과 빠른 해결책

1. **`mmcli -L`에 아무것도 표시되지 않음**: `ModemManager`가 중단되었거나, USB 전원 공급이 카드를 구동하기에 부족할 수 있습니다.
2. **GPS 측위가 계속 실패함**: GPS 안테나를 Main이나 Aux에 꽂지는 않았습니까? GNSS 포트는 전용 커넥터입니다!
3. **EM919x가 최대 속도에 도달하지 못함**: USB 3.1 Gen 2와 심지어 PCIe Gen 3까지 지원하는 5G 카드입니다. USB 2.0 포트에 꽂으면 제조사는 성능을 보장하지 않습니다.

## 결론

Linux에서 Sierra 모듈을 다루는 일은 보기보다 어렵지 않습니다. 하드웨어 슬롯과 안테나를 확인하고, `modemmanager` 계열 패키지를 설치하고, APN을 설정하면 온라인 상태가 됩니다. 이 작업 흐름은 엣지 컴퓨팅이나 산업용 IoT(IIoT)를 다루는 엔지니어에게 꼭 맞습니다.

## 구매처 (Call To Action)

Ubuntu 장치에 Sierra 모듈을 통합하고 싶으십니까? Yopitek은 모듈, 안테나, 어댑터 보드의 완전한 솔루션과 1차 기술 지원을 제공합니다.
문의: **sales@yupitek.com**
제품 둘러보기: [Sierra Wireless 시리즈](https://yupitek.com/ko/products/sierra/)

{{< faq >}}
