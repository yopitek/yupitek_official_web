---
title: "Sierra EM7455 완전 리뷰: 메이커와 연구실에서 가장 사랑받는 Sierra 카드인 이유"
description: "EM7455 종합 리뷰: 사양, EM7430과의 차이, OpenWrt/Linux 설정, Dell/Lenovo 호환성. Yopitek이 정리한 기술 자료입니다."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em7455", "lte-a", "cat-6", "openwrt", "linux", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM7455_hero.jpg"
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "EM7455는 5G를 지원합니까?"
    answer: "아니요. 최대 속도 300 Mbps의 LTE-A Cat 6 모듈입니다. 5G가 필요하시다면 EM9190 또는 EM9191을 검토하시기 바랍니다."
  - question: "EM7455를 대만에서 사용할 수 있습니까?"
    answer: "SIM이 지원 대역을 사용한다면 대만의 주요 통신사에서 작동합니다. 실제 신호 강도와 캐리어 애그리게이션은 기지국 커버리지에 따라 달라지므로, 구매 전에 호환성을 저희와 상의하시기 바랍니다."
  - question: "EM7455와 MC7455의 차이는 무엇입니까?"
    answer: "두 제품 모두 동일한 Qualcomm MDM9230 칩셋을 기반으로 하며 사양이 같습니다. 차이는 패키지 형태뿐으로, EM7455는 M.2이고 MC7455는 mPCIe입니다. 사용하시는 슬롯에 맞게 선택하시면 됩니다."
  - question: "EM7455와 EM7430의 차이는 무엇입니까?"
    answer: "두 제품은 동일한 MDM9230 칩셋과 핵심 사양을 공유합니다. 주된 차이는 대역 커버리지로, EM7455는 미주 및 EMEA 대역을, EM7430은 아시아 태평양 대역을 지원합니다."
  - question: "Dell DW5811e는 EM7455와 동일한 제품입니까?"
    answer: "네. DW5811e는 Dell이 브랜드를 변경한 EM7455이며, 동일한 Qualcomm MDM9230 칩셋을 기반으로 합니다."
---

{{< alert >}}
Yopitek은 Sierra Wireless / Semtech 제품 정보와 기술 콘텐츠를 제공합니다. 공식 인증 유통업체가 아니며, 기술 참고용입니다.
{{</alert >}}

OpenWrt를 실행하는 Raspberry Pi를 다뤄 보셨거나 연구실 장비에 4G를 추가하고 싶으셨다면, Sierra EM7455에 대해 들어 보셨을 것입니다. Sierra Wireless의 LTE-A Cat 6 M.2 셀룰러 모듈로, Qualcomm MDM9230 칩셋을 기반으로 최대 300 Mbps 다운링크와 50 Mbps 업링크를 제공하며, GNSS 위치 측위를 내장하고 -40°C에서 +85°C까지의 동작 범위를 견딥니다.

Yopitek이 정리한 이 글에서는 이 M.2 B-Key 4G LTE-Advanced Cat 6 모듈이 왜 이토록 인기를 얻었는지, 그리고 Linux에서 드라이버와 설정을 동작시키는 방법을 설명합니다.

> 제품 페이지: [EM7455 — Yopitek](/ko/products/sierra/em7455/) | 공식 사양: [AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## EM7455 전체 사양표: 한눈에 보는 수치

아래 수치는 Sierra Wireless 공식 사양서를 기반으로 정리한 것입니다. 실제 프로젝트를 위해 주문하신다면, 대역이나 펌웨어 버전처럼 시간이 지나며 바뀌는 항목은 특히 먼저 저희에게 최신 공식 문서를 요청하시기 바랍니다.

| 항목 | 사양 |
|---|---|
| **모델** | AirPrime EM7455 |
| **셀룰러 표준** | LTE-A Cat 6 |
| **칩셋** | Qualcomm MDM9230 (Snapdragon X7 LTE) |
| **최대 다운로드** | 300 Mbps (LTE-A, 2×CA) |
| **최대 업로드** | 50 Mbps (LTE-A) |
| **캐리어 애그리게이션** | 2×CA (다양한 조합 지원, 공식 AT 명령 레퍼런스 참조) |
| **폼 팩터** | PCI Express M.2 B-Key (52핀) |
| **크기** | 42 x 30 x 2.3 mm |
| **동작 온도** | -40°C ~ +85°C (산업용 등급) |
| **GNSS** | GPS, GLONASS, BeiDou, Galileo |
| **호스트 인터페이스** | USB 3.0 / USB 2.0 High Speed |
| **LTE 대역** | 미주 및 EMEA(유럽/중동/아프리카) 주요 대역, 전체 대역 목록은 최신 공식 사양서에서 확인하시기 바랍니다 |
| **3G WCDMA 대역** | 최신 공식 사양서에서 확인하시기 바랍니다 |
| **일반 VID:PID** | `1199:9079` (EM7455, 표준 버전) |
| **Dell DW5811e VID:PID** | `413c:81b6` (브랜드 버전, 보유하신 장치에서 `lsusb`로 확인하시기 바랍니다) |
| **Linux 드라이버** | `qcserial`, `qmi_wwan`, `cdc_mbim` (대부분의 주요 배포판에 내장) |
| **일반 펌웨어** | 공식 source.sierrawireless.com의 최신 버전을 사용하시기 바랍니다 |
| **통신사 인증** | 지역에 따라 다름 (예: AT&T, Verizon, Vodafone), 최신 목록은 저희에게 확인하시기 바랍니다 |

---

## EM7455는 어떤 프로젝트에 적합합니까?

**간단히 말해, EM7455는 세 가지 대표적인 요구에 대한 해답입니다. (1) OpenWrt나 ROOter 같은 오픈소스 펌웨어로 4G LTE 라우터 구축, (2) Dell 또는 Lenovo 노트북의 WWAN 카드 업그레이드, (3) 산업용 연구실에서 IoT 게이트웨이나 텔레매틱스 트래커 구축.**

가장 큰 강점은 매우 성숙한 Linux 드라이버 생태계, 풍부한 커뮤니티 튜토리얼, 폭넓은 대역 지원입니다.

### 메이커 또는 학생이라면

| 활용 사례 | 권장 구성 | 적합한 이유 |
|---|---|---|
| Raspberry Pi 4G 라우터 | Pi 4/5 + M.2-USB 어댑터 + OpenWrt / ROOter | 탄탄한 OpenWrt 커뮤니티 지원과 안정적인 `uqmi` 패키지 |
| GL.iNet 라우터 업그레이드 | GL-MT1300 / GL-AR750S + USB 어댑터 | ROOter용 커뮤니티 `create_connect.sh` 논의 덕분에 설정이 쉬움 |
| 휴대용 야외 LTE 핫스팟 | 배터리 전원 + USB 어댑터 + 소형 라우터 | 낮은 발열과 우수한 열 특성이 야외 자산 추적에 적합 |

### 기업 또는 산업 프로젝트라면

| 활용 사례 | 권장 구성 | 적합한 이유 |
|---|---|---|
| 산업용 라우터 | M.2 슬롯이 있는 산업용 게이트웨이 (예: Advantech) | 내구성이 뛰어나고 안심할 수 있는 -40 ~ 85°C 광범위 온도 등급, 풍부한 대역 |
| 텔레매틱스 | 차량용 게이트웨이 + GNSS 안테나 | GPS/GLONASS 위치 측위 내장: 한 장의 카드로 연결과 위치 확인 |
| 노트북 WWAN 업그레이드 | Dell Latitude / Lenovo ThinkPad | M.2 B-Key 슬롯에 그대로 장착되며, 대부분 Linux에서 플러그 앤 플레이 |
| WAN 페일오버 | OpenWrt / pfSense 듀얼 WAN 페일오버 | QMI/MBIM 듀얼 모드 지원 (pfSense 지원은 편차가 있으며, OpenWrt가 더 안전한 선택) |

---

## EM7455 vs EM7430: 실제로 무엇이 다릅니까?

매우 자주 나오는 질문입니다. **EM7455와 EM7430은 완전히 동일한 Qualcomm MDM9230 칩셋을 기반으로 하므로 핵심 사양(Cat 6, 300/50 Mbps, 2×CA, GNSS)이 같습니다. 실제 차이는 각 모델이 겨냥하는 시장의 대역입니다.** EM7455는 미주와 EMEA(유럽/중동/아프리카)를, EM7430은 아시아 태평양(APAC) 지역을 대상으로 합니다.

| 항목 | EM7455 | EM7430 |
|---|---|---|
| **칩셋** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **셀룰러 표준** | LTE-A Cat 6 | LTE-A Cat 6 |
| **최대 다운로드** | 300 Mbps | 300 Mbps |
| **최대 업로드** | 50 Mbps | 50 Mbps |
| **캐리어 애그리게이션** | 2×CA | 2×CA |
| **폼 팩터** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **대상 지역** | 미주, EMEA | 아시아 태평양 (APAC) |

**간단한 선택 팁:** SIM을 주로 북미나 유럽에서 사용하신다면 **EM7455**를 선택하시고, 아시아 태평양 지역(일본, 호주 등)에서는 이론상 **EM7430**이 더 잘 맞습니다. 일부 시장에서는 통신사의 대역 할당이 특이할 수 있으므로, 주문 전에 사용하시는 통신사에 어떤 카드가 가장 잘 맞는지 저희에게 확인하시기 바랍니다.

---

## EM7455 vs MC7455: 동일한 칩, 다른 핀 배치

앞서 설명한 대로 EM7455(M.2)와 MC7455(mPCIe)는 동일한 Qualcomm MDM9230을 사용하며 전기적으로 동일한 사양입니다. 유일한 차이는 "껍데기", 즉 패키지입니다.

| 항목 | EM7455 | MC7455 |
|---|---|---|
| **폼 팩터** | M.2 (B-Key) | Mini PCIe (mPCIe) |
| **크기** | 42 x 30 x 2.3 mm | 51 x 30 x 3.5 mm |
| **적합한 용도** | 노트북 WWAN 슬롯, 최신 개발 보드 | 구형 패널 PC의 mPCIe 슬롯 |
| **일반 VID:PID** | `1199:9079` | `1199:9071` |

**간단합니다. 장치의 슬롯에 맞는 카드를 고르시면 됩니다.** 잘못 선택했더라도 어댑터 보드(M.2에서 mPCIe로, 또는 그 반대)로 대개 해결할 수 있습니다.

---

## Linux에서 설정하기 (Ubuntu / Debian / Linux Mint)

EM7455는 주요 Linux 시스템에서 매우 잘 지원됩니다. 아래 단계는 커뮤니티 표준 기본 설정입니다. 장치마다 OS 버전과 커널이 다르므로, 먼저 운영 환경이 아닌 장치에서 테스트하시기 바랍니다.

### 1단계: 하드웨어 인식 확인

```bash
lsusb | grep -i sierra
# You should see output similar to: Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### 2단계: 필수 도구 설치

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### 3단계: USB 모드를 QMI로 전환

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# Verify the mode switch succeeded
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# You should see: USB composition 6: DM, NMEA, AT, QMI
```

> 통신사에서 MBIM 모드를 요구하는 경우 `AT!USBCOMP` 명령을 참고하시고 `mbimcli`로 연결하시기 바랍니다.

### 4단계: FCC 인증 해제

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# For fully automatic handling via ModemManager:
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### 5단계: NetworkManager로 연결

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn 'YOUR_APN'
sudo nmcli connection up 'EM7455 LTE'
```

### 6단계: 수동 QMI 연결 (고급 문제 해결용)

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='YOUR_APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## OpenWrt에서 QMI 설정하기

EM7455는 OpenWrt 커뮤니티에서 평판이 좋습니다. OpenWrt가 설치된 라우터를 보유하고 계시다면, 표준 QMI 설정 방법은 다음과 같습니다.

### 필수 패키지 설치

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### 네트워크 설정 편집

`/etc/config/network`를 열고 다음 인터페이스 블록을 추가하시기 바랍니다.

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'YOUR_APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### 네트워크 재시작

```bash
/etc/init.d/network restart
```

LuCI 웹 인터페이스를 선호하신다면, Network, Interfaces로 이동하여 새 인터페이스를 추가하고 QMI 프로토콜을 선택한 뒤 `/dev/cdc-wdm0`을 선택하고 APN을 입력하시기 바랍니다.

> Raspberry Pi 사용자를 위한 팁: 4G/5G 라우팅 전용으로 만들어진 OpenWrt 기반 펌웨어인 ROOter에는 편리한 설정 훅이 많이 내장되어 있습니다. 한번 사용해 보시기 바랍니다.

---

## 브랜드 노트북 호환성: Dell 및 Lenovo

### Dell 노트북 (해당 카드는 DW5811e라고 부릅니다)

온라인에서 Dell DW5811e에 대한 언급을 자주 보게 되실 것입니다. Dell이 브랜드를 변경한 EM7455(VID `413c`, PID `81b6`)로, 내부에 동일한 MDM9230 칩이 들어 있으며 대부분의 Linux `qmi_wwan` 드라이버가 오래전부터 인식해 왔습니다.

```bash
lsusb | grep 413c
# You should see something like: Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

좋은 소식은, 커뮤니티 보고에 따르면 대부분의 Dell 노트북(Latitude, Precision 등)이 BIOS 화이트리스트를 적용하지 않아 카드를 그대로 꽂으면 보통 작동한다는 점입니다.

### Lenovo 노트북 (성가신 화이트리스트)

Lenovo ThinkPad에서는 주의가 필요합니다. Lenovo는 때때로 Lenovo 순정 FRU 카드만 허용하는 BIOS 화이트리스트를 적용합니다. 일부 포럼 회원들이 이 제한을 우회하는 AT 명령을 공유했으며, 모험을 감수하실 분을 위한 것입니다.

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **경고: 이 명령들은 포럼에서 가져온 것입니다. 잘못 실행하면 카드가 벽돌이 될 수 있습니다.** 하드웨어를 분해하고 위험을 감수하는 것을 즐기시는 경우가 아니라면, 주문 전에 더 안전한 대안에 대해 저희에게 문의하시기 바랍니다.

---

## 플랫폼 지원 현황 한눈에 보기

| 사용하는 플랫폼 | 지원 수준 | 연결 방법 | 비고 |
|---|---|---|---|
| Raspberry Pi + OpenWrt | ✅✅ 매우 안정적, 튜토리얼 풍부 | QMI / MBIM | M.2-USB 어댑터 보드 필요 |
| Raspberry Pi + ROOter | ✅✅ | QMI | Pi 사용자에게 적극 권장 |
| Ubuntu / Debian | ✅✅ | ModemManager / QMI | 플러그 앤 플레이일 가능성이 높음 |
| DD-WRT | ⚠️ 운에 따라 다름 | QMI / PPP | 커뮤니티 논의가 적어 초보자에게는 비추천 |
| pfSense | ⚠️ 편차가 있음 | QMI / PPP | 수고를 줄이려면 OpenWrt를 고려하시기 바랍니다 |
| Dell 노트북 | ✅ | QMI / MBIM | 일반적으로 Linux에서 인식됨 |
| Lenovo 노트북 | ⚠️ 우회 방법이 필요할 수 있음 | QMI | BIOS 화이트리스트에 유의, 무모한 명령은 벽돌 위험 |

---

## 추가 자료를 찾을 수 있는 곳

막히는 부분이 있다면 다음 오픈소스 커뮤니티를 참고해 볼 만합니다.

- **danielewood의 GitHub**: EM7455/MC7455에 대한 포괄적인 스크립트와 논의.
- **Gentoo Wiki**: Linux 커뮤니티가 관리하는 매우 상세한 문제 해결 가이드.
- **OpenWrt LTE Wiki**: 공식 문서로, 네트워크를 설정하기 전에 읽어 보시기 바랍니다.

## 자주 묻는 질문

{{< faq >}}

---

## 연구실용으로 구매하시나요? 저희와 상담하세요

이 글은 Yopitek의 엔지니어링 팀이 정리했습니다. 대학 프로젝트, 연구실 프로그램, 또는 EM7455나 기타 Sierra 모듈의 기업 대량 구매 등 어떤 경우든 저희와 상담해 주시기 바랍니다.

- **이 카드 보기**: [https://yupitek.com/ko/products/sierra/em7455/](/ko/products/sierra/em7455/)
- **모든 Sierra 모델 보기**: [https://yupitek.com/ko/products/sierra/](/ko/products/sierra/)
- **이메일 문의**: sales@yupitek.com
