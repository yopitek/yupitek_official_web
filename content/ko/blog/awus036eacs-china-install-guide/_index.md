---
title: "중국 환경을 위한 ALFA AWUS036EACS 설치 가이드: Windows 설치 및 Linux 호환성"
description: "중국 환경에서 ALFA AWUS036EACS를 설정하는 가이드입니다. RTL8821CU WiFi 5 + Bluetooth 4.2 나노 어댑터로, Windows 드라이버는 files.alfa.com.tw에서 제공됩니다. Linux 커널 6.2 이상에서는 커널 내장 rtw88_8821cu 드라이버가 별도 작업 없이 바로 동작하며, 모니터 모드와 인젝션이 정상 동작하는 것으로 검증되었습니다."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036EACS는 어떤 칩셋을 사용하나요? Bluetooth를 지원하나요?"
    answer: "Realtek RTL8821CU 칩셋을 사용하며, WiFi 5와 Bluetooth 4.2를 지원합니다."
  - question: "AWUS036EACS는 Linux에서 사용하기에 적합한가요?"
    answer: "예. Linux 커널 6.2 이상(예: Ubuntu 24.04 HWE / 커널 6.17)에서는 커널 내장 rtw88_8821cu 드라이버가 별도 컴파일 없이 바로 동작합니다. 당사 측정 결과 2.4 GHz / 5 GHz 양쪽 대역 모두에서 모니터 모드와 패킷 인젝션이 100%로 동작했고, WPA 핸드셰이크를 엔드 투 엔드로 캡처(.22000)했으며, Bluetooth도 정상 동작하는 것으로 검증되었습니다."
  - question: "Windows에서 AWUS036EACS 드라이버는 어떻게 설치하나요?"
    answer: "files.alfa.com.tw에서 Windows 드라이버 패키지를 내려받아 관리자 권한으로 설치한 뒤 재부팅하면 됩니다."
  - question: "AWUS036EACS에서 Bluetooth는 어떻게 활성화하나요?"
    answer: "드라이버를 설치하면 Bluetooth가 대체로 자동으로 활성화됩니다. Windows 설정에서 Bluetooth 스위치를 켜면 기기를 연결할 수 있습니다."
  - question: "Linux용 무선 보안 연구 어댑터가 필요하다면 어떤 제품을 선택해야 하나요?"
    answer: "AWUS036EACS 자체가 커널 6.2 이상에서 모니터 모드와 패킷 인젝션을 지원하며, Bluetooth는 덤으로 제공됩니다. 더 많은 선택지를 원하신다면 AWUS036ACM과 AWUS036ACS 역시 Linux에서 모니터 모드를 완전히 지원합니다. 본인이 소유하거나 테스트 권한을 보유한 네트워크에서만 사용하시기 바랍니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036eacs-china-install-guide"
tags: ["alfa", "awus036eacs", "windows", "driver", "china", "bluetooth", "rtl8821cu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 8
related_product: "/ko/products/alfa/awus036eacs/"
featureimage: "/images/blog/awus036eacs-china-install-guide.webp"
---

AWUS036EACS는 ALFA의 나노 WiFi 5 + Bluetooth 4.2 콤보 어댑터입니다. Windows 사용자에게 적합한 소형 무선 업그레이드 제품이며, Linux 커널 6.2 이상에서는 커널 내장 rtw88_8821cu 드라이버가 별도 컴파일 없이 바로 지원합니다. 이 가이드에서는 중국 내 소스를 통한 Windows 설치 방법과 Linux 사용 경험을 다룹니다.

{{< tldr >}}
AWUS036EACS는 RTL8821CU 칩셋을 사용합니다. WiFi 5에 Bluetooth 4.2를 더한 미니 어댑터로 Windows에서 손쉽게 설치할 수 있으며, Linux 커널 6.2 이상에서는 커널 내장 rtw88_8821cu 드라이버가 기본 포함되어 모니터 모드와 패킷 인젝션이 별도 작업 없이 동작하고 Bluetooth도 정상 동작하는 것으로 검증되었습니다.
{{< /tldr >}}

> **AWUS036EACS는 Linux 커널 6.2 이상에서 별도 작업 없이 바로 동작합니다.** 커널 6.2 이상(예: Ubuntu 24.04 HWE / 커널 6.17)에는 커널 내장 rtw88_8821cu 드라이버가 포함되어 있어 컴파일이 필요 없습니다. 당사 측정 결과 2.4 GHz / 5 GHz 양쪽 대역 모두에서 모니터 모드와 패킷 인젝션이 100%로 동작했고, WPA 핸드셰이크를 엔드 투 엔드로 캡처(.22000)했으며, Bluetooth(BT)도 정상 동작하는 것으로 검증되었습니다(BR/EDR + BLE 모두 기기 스캔이 가능하고 WiFi와 공존함). 본인이 소유하거나 테스트 권한을 보유한 네트워크에서만 사용하시기 바랍니다.
>
> **운용 팁:** 이 제품은 BT+WiFi 콤보 카드입니다. 모드를 반복적으로 전환하다 보면 WiFi RX가 멈출 수 있습니다(`ip link set up`이 `Operation already in progress`를 반환하고, `iw ... set channel`이 `-16 busy`를 반환함). 각 테스트 단계를 시작하기 전에 어댑터를 뽑았다가 다른 USB 포트에 다시 꽂아 복구하시기 바랍니다.
>
> 같은 시리즈의 다른 Linux 어댑터:
> - **[AWUS036ACM](/ko/blog/awus036acm-china-install-guide/)** — MT7612U 커널 내장 드라이버, 완전한 모니터 모드 + VIF
> - **[AWUS036ACS](/ko/blog/awus036acs-china-install-guide/)** — RTL8811AU, 가성비 좋은 모니터 모드





## Linux 사용자께서는 먼저 읽어주세요

> **AWUS036EACS는 Linux 커널 6.2 이상에서 별도 작업 없이 바로 동작합니다.** 커널 6.2 이상(예: Ubuntu 24.04 HWE / 커널 6.17)에는 커널 내장 rtw88_8821cu 드라이버가 포함되어 있어 컴파일이 필요 없습니다. 당사 측정 결과 2.4 GHz / 5 GHz 양쪽 대역 모두에서 모니터 모드와 패킷 인젝션이 100%로 동작했고, WPA 핸드셰이크를 엔드 투 엔드로 캡처(.22000)했으며, Bluetooth(BT)도 정상 동작하는 것으로 검증되었습니다(BR/EDR + BLE 모두 기기 스캔이 가능하고 WiFi와 공존함). 본인이 소유하거나 테스트 권한을 보유한 네트워크에서만 사용하시기 바랍니다.
>
> **운용 팁:** 이 제품은 BT+WiFi 콤보 카드입니다. 모드를 반복적으로 전환하다 보면 WiFi RX가 멈출 수 있습니다(`ip link set up`이 `Operation already in progress`를 반환하고, `iw ... set channel`이 `-16 busy`를 반환함). 각 테스트 단계를 시작하기 전에 어댑터를 뽑았다가 다른 USB 포트에 다시 꽂아 복구하시기 바랍니다.
>
> 같은 시리즈의 다른 Linux 어댑터:
> - **[AWUS036ACM](/ko/blog/awus036acm-china-install-guide/)** — MT7612U 커널 내장 드라이버, 완전한 모니터 모드 + VIF
> - **[AWUS036ACS](/ko/blog/awus036acs-china-install-guide/)** — RTL8811AU, 가성비 좋은 모니터 모드

---

## Windows 10 / 11 설정

### 1단계: Alfa에서 드라이버 내려받기

Alfa 공식 드라이버 서버는 중국에서 접속할 수 있습니다:

https://files.alfa.com.tw

**AWUS036EACS** 제품 폴더로 이동하여 Windows 드라이버 패키지(`.zip` 또는 `.exe`)를 내려받습니다.

또는 문서 페이지를 참고하셔도 됩니다:
https://docs.alfa.com.tw/Product/AWUS036EACS/

### 2단계: 드라이버 설치

1. 내려받은 zip 파일의 압축을 풉니다.
2. 설치 파일 `.exe`를 마우스 오른쪽 버튼으로 클릭한 뒤 **관리자 권한으로 실행**을 선택합니다.
3. 화면의 안내를 따릅니다.
4. 메시지가 표시되면 재부팅합니다.

### 3단계: 어댑터 확인

재부팅 후 **장치 관리자**를 엽니다(Win+X → 장치 관리자).

**네트워크 어댑터** 항목 아래에 다음이 표시되어야 합니다:

```
Realtek 8821CU Wireless LAN 802.11ac USB NIC
```

이제 어댑터가 2.4 GHz 및 5 GHz 네트워크에 연결할 준비가 되었습니다.

### 4단계: WiFi 연결

1. 작업 표시줄의 WiFi 아이콘을 클릭합니다.
2. 연결할 네트워크를 선택합니다.
3. 비밀번호를 입력하고 연결합니다.

---

## Bluetooth 설정(Windows)

AWUS036EACS에는 Bluetooth 4.2가 포함되어 있습니다. 드라이버를 설치한 후:

1. **설정 → Bluetooth 및 장치**를 엽니다.
2. Bluetooth를 **켜기**로 전환합니다.
3. **장치 추가**를 클릭하여 키보드, 마우스, 헤드폰 등 Bluetooth 주변기기를 페어링합니다.

---

## Linux 호환성 상세

**커널 6.2 이상**에서는 RTL8821CU가 커널 내장 `rtw88_8821cu` 모듈로 구동되므로 컴파일할 것이 없습니다. 꽂기만 하면 인식됩니다. 먼저 `uname -r`로 커널 버전을 확인하시기 바랍니다.

### Kali Linux

커널 6.2 이상에서는 기본 포함된 `rtw88_8821cu` 드라이버가 자동으로 로드됩니다. 당사 테스트 결과 2.4 GHz / 5 GHz 양쪽 대역 모두에서 모니터 모드와 패킷 인젝션이 100%로 동작했고, WPA 핸드셰이크를 엔드 투 엔드로 캡처(.22000)했습니다. 본인이 소유하거나 테스트 권한을 보유한 네트워크에서만 사용하시기 바랍니다.

```bash
sudo nmcli dev set wlxXXXX managed no
sudo ip link set wlxXXXX down
sudo iw dev wlxXXXX set type monitor
sudo ip link set wlxXXXX up
```

### Ubuntu 22.04 / 24.04

Ubuntu 24.04는 GA 커널 6.8과 HWE 커널(예: 커널 6.17) 모두에 커널 내장 `rtw88_8821cu` 드라이버(커널 6.2부터 mainline 포함)가 기본 탑재되어 있어 모니터 모드, 패킷 인젝션, 클라이언트 연결이 별도 작업 없이 동작합니다. 더 오래된 커널(6.2 미만, 예: Ubuntu 22.04 GA 커널)을 사용 중이라면 HWE 커널로 업데이트하여 커널 내장 드라이버를 사용하시기 바랍니다.

### Debian / Raspberry Pi

마찬가지입니다. 커널이 6.2 이상(ARM64 빌드 포함)이면 커널 내장 `rtw88_8821cu` 드라이버가 컴파일 없이 어댑터를 처리합니다.

### 운용 팁(BT+WiFi 콤보 카드)

EACS는 하나의 칩에 Bluetooth와 WiFi를 모두 탑재하고 있어, 모드를 반복적으로 전환하면 WiFi RX가 멈춘 상태로 남을 수 있습니다. 이때 `ip link set up`은 `Operation already in progress`를, `iw ... set channel`은 `-16 busy`를 반환합니다. 각 테스트 단계를 시작하기 전에 어댑터를 뽑았다가 다른 USB 포트에 다시 꽂아 상태를 초기화하시기 바랍니다. Bluetooth(BR/EDR + BLE)는 정상 동작하는 것으로 검증되었으며 WiFi와 공존합니다.

---

{{< faq >}}

## 중국 리소스

| 리소스 | URL | 용도 |
|----------|-----|---------|
| Alfa 공식 드라이버 | [files.alfa.com.tw](https://files.alfa.com.tw) | EACS Windows 드라이버 |
| Alfa 문서 | [docs.alfa.com.tw](https://docs.alfa.com.tw) | 설치 가이드, FAQ |
| Alfa 위키 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 제품 설명서 |

## 중국 환경을 위한 추가 Alfa 어댑터 가이드

- [AWUS036ACH 중국 설치 가이드](/ko/blog/awus036ach-china-install-guide/) — RTL8812AU, 고출력
- [AWUS036ACM 중국 설치 가이드](/ko/blog/awus036acm-china-install-guide/) — MT7612U, 완전한 VIF
- [AWUS036ACS 중국 설치 가이드](/ko/blog/awus036acs-china-install-guide/) — RTL8811AU, 모니터 모드
- [AWUS036AX 중국 설치 가이드](/ko/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER 중국 설치 가이드](/ko/blog/awus036axer-china-install-guide/) — RTL8832BU, 나노
- [AWUS036AXM 중국 설치 가이드](/ko/blog/awus036axm-china-install-guide/) — MT7921AUN, L자형
- [AWUS036AXML 중국 설치 가이드](/ko/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- AWUS036EACS ← 현재 보고 있는 글

궁금한 점이 있으신가요? 아래에 댓글을 남기시거나 [yupitek.com](https://yupitek.com/ko/contact/)으로 문의해 주시기 바랍니다.

## 참고 문헌

1. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
2. [ALFA 공식 드라이버 다운로드](https://files.alfa.com.tw)
3. [Realtek 공식 웹사이트](https://www.realtek.com/)
