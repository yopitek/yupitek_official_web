---
title: "Flipper Zero 5G 확장 보드 사용 설명서 (v2.0): 그림으로 보는 설치 및 사용 가이드"
description: "Flipper Zero 5G 확장 보드의 설치와 사용 방법을 단계별로 안내하는 완전 가이드(v2.0)입니다. 아이소메트릭 엔지니어링 도면, 안테나 설치, 슬롯 상세 설명, GPIO 설정을 포함합니다."
date: 2026-10-18
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-zero-5g-expansion-board-user-manual"
tags: ["Flipper Zero", "5G Expansion Board", "SDRLab", "Tutorial"]
categories: ["Technical"]
author: "Yopitek"
lastmod: 2026-10-18
featureimage: "/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg"
hideFeatureImage: true
---

> <strong>대상 독자</strong>: 5G 확장 보드를 처음 사용하는 고객.  
> <strong>핵심 목표</strong>: 이 가이드는 모든 중요한 설치 단계에 대해 상세한 아이소메트릭 도면을 제공합니다. 각 단계마다 전용 이미지를 함께 제시하여 오류 없이 원활하게 설치할 수 있도록 돕습니다.

---

## 00. 개봉 및 패키지 구성품

Flipper Zero 5G 확장 보드를 선택해 주셔서 감사합니다. 설치를 시작하기 전에 패키지에 아래 항목이 모두 들어 있는지 확인해 주십시오.

![Package Contents](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg)
*그림 1: 포함된 패키지 액세서리*

### ⚠️ 패키지 구성품 상세
*   <strong>기본 포함 항목</strong>:
    1.  5G 확장 보드 본체 모듈 x 1
    2.  433MHz 휩 안테나(짧은 검은색 휩 안테나) x 1
    3.  GPS 액티브 세라믹 패치 안테나(케이블이 달린 정사각형 안테나) x 1
    4.  듀얼 밴드 WiFi 접착식 패치 안테나(평평한 검은색 안테나) x 1
*   <strong>미포함 항목(별도 구매 필요)</strong>:
    *   <strong>Flipper Zero 본체</strong>(이 모듈에는 포함되어 있지 않습니다)
    *   <strong>MicroSD 카드</strong>(모듈 작동에 필요하며 별도로 구매해야 합니다)

---

## 01. 5G 모듈 알아보기

안테나를 연결하거나 모듈을 Flipper Zero 본체에 장착하기 전에, 주요 인터페이스와 하드웨어 배치를 먼저 살펴보시기 바랍니다.

### 전면 인터페이스

![Front Interface Diagram](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_02_front_interface.jpg)
*그림 2: 전면 하드웨어 구성 배치*

*   <strong>LCD 화면</strong>: 현재 연결 상태, IP 주소, 작동 모드를 표시합니다.
*   <strong>토글 스위치</strong>: 모듈 화면의 전원 공급을 제어합니다. 스위치를 위로 올리면 켜집니다.
*   <strong>MicroSD 카드 슬롯</strong>: 펌웨어 설정과 시스템 로그를 저장하는 데 사용합니다.
*   <strong>GPIO 소켓</strong>: Flipper Zero 상단의 수(male) GPIO 핀에 연결되는 암(female) 헤더입니다.
*   <strong>LED 표시등</strong>: 전원과 배터리 충전 상태를 표시합니다.

### 측면 안테나 포트

![Antenna Ports Diagram](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_03_antenna_ports.jpg)
*그림 3: 안테나 포트 위치와 표기*

*   <strong>433M A</strong>: 433MHz 휩 안테나를 연결합니다.
*   <strong>GPS</strong>: 액티브 GPS 세라믹 안테나를 연결합니다.
*   <strong>2.4G</strong> 및 <strong>2.4G/5G</strong>: 듀얼 밴드 WiFi 접착식 패치 안테나를 연결합니다.

> ⚠️ <strong>생산 배치 안내</strong>:  
> 안테나 포트 배치는 생산 배치에 따라 다소 다를 수 있습니다. 예를 들어 GPS 포트와 WiFi 포트의 위치가 서로 바뀌어 있을 수 있습니다. 신호 저하나 하드웨어 손상을 방지하려면 기억에 의존하지 말고 <strong>반드시 실제 모듈 케이스에 인쇄된 라벨을 확인해 주십시오</strong>.

---

## 02. 단계별 설치 가이드

### 1단계 | MicroSD 카드 준비 및 설치

5G 모듈은 설정 파일을 저장하기 위해 MicroSD 카드가 필요합니다.

1.  <strong>삽입 방향</strong>: 금속 접점이 아래를 향하도록 MicroSD 카드를 슬롯에 삽입합니다. 딸깍 소리가 날 때까지 카드를 가볍게 누릅니다.

![MicroSD Card Slot Close-up](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_07_sd_card_slot.jpg)
*그림 4: 올바른 MicroSD 카드 삽입 방향*

---

### 2단계 | 안테나 3개 설치

포함된 안테나 3개를 각각 해당하는 SMA 안테나 포트에 체결합니다. 각 커넥터는 손으로 단단히 조이되 과도한 힘을 주지 마십시오.

![Antenna Installation Diagram](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_08_three_antenna_connection.jpg)
*그림 5: 안테나 연결 및 배선 경로 도면*

| 안테나 유형 | 포트 표기 | 설치 상세 |
| :--- | :--- | :--- |
| <strong>GPS 액티브 세라믹 안테나</strong> | <strong>GPS 포트</strong> | 연장 케이블이 달린 정사각형 세라믹 하우징 |
| <strong>듀얼 밴드 WiFi 접착식 패치 안테나</strong> | <strong>2.4G/5G 포트</strong> | 평평한 검은색 접착식 패치 안테나 |
| <strong>433MHz 휩 안테나</strong> | <strong>433M A 포트</strong> | 짧고 단단한 검은색 휩 안테나 |

#### ⚠️ GPS 안테나 방향 주의
GPS 안테나는 방향성이 매우 강합니다. 설치할 때 <strong>세라믹 면(양면테이프가 붙은 면의 반대쪽인 평평한 윗면)이 위쪽(하늘 방향)을 향해야 합니다</strong>. 잘못 설치하면 모듈이 위성 신호를 수신하지 못합니다.

![GPS Antenna Orientation Comparison](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_09_gps_antenna_orientation.jpg)
*그림 6: GPS 안테나의 올바른 배치(위쪽 향함)와 잘못된 배치(아래쪽 향함) 비교*

---

### 3단계 | Flipper Zero에 모듈 장착

5G 모듈을 Flipper Zero 상단의 GPIO 핀에 끼웁니다.

1.  핫플러그로 인한 하드웨어 손상을 방지하기 위해 <strong>Flipper Zero의 전원을 끕니다</strong>.
2.  Flipper Zero 상단의 GPIO 핀과 모듈 하단의 소켓을 정렬합니다.

![GPIO Alignment Diagram](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_10_gpio_alignment.jpg)
*그림 7: GPIO 정렬 지침 및 배치*

3.  양손으로 고르게 힘을 주어 <strong>모듈을 끝까지 단단히 눌러 끼웁니다</strong>.
4.  <strong>장착 확인</strong>: 모듈을 옆에서 살펴봅니다. 모듈이 Flipper Zero에 완전히 밀착되어 <strong>틈이 보이지 않아야 합니다</strong>.

![GPIO Fit Verification](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_19_gpio_insertion_flat.jpg)
*그림 8: 올바르게 정렬되어 완전히 삽입된 GPIO 연결*

---

### 4단계 | Flipper Zero 소프트웨어 설정

장착을 마쳤으면 Flipper Zero의 전원을 켜고 GPIO 핀을 설정합니다.

<strong>Momentum 펌웨어</strong>를 사용하는 경우 다음 단계를 따르십시오.

1.  <strong>모듈 화면 켜기</strong>: 모듈 전면 왼쪽에 있는 토글 스위치를 <strong>위(UP)</strong> 위치로 올립니다.
    ![Toggle Switch UP position](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_16_toggle_switch_up.jpg)
    *그림 9: 토글 스위치를 UP 위치로 올려 화면 활성화*

2.  <strong>GPS 핀 설정</strong>:
    *   이동 경로: `Protocol Settings` > `GPIO Pin Settings` > `GPS Pin`
    *   값을 <strong>13</strong> 또는 <strong>14</strong>로 설정합니다(하드웨어 버전별 사양에 따라 다릅니다).
3.  <strong>ESP32 핀 설정(WiFi/Bluetooth 기능)</strong>:
    *   이동 경로: `Protocol Settings` > `GPIO Pin Settings` > `ESP32 Pin`
    *   값을 <strong>15, 16</strong>으로 설정합니다.
4.  <strong>433MHz Sub-GHz 모듈 설정</strong>:
    *   이동 경로: `Sub-GHz` > `Advanced Settings` > Module을 <strong>External</strong>로 설정하여 외부 안테나를 활성화합니다.

---

### 5단계 | 충전 및 배터리 잔량 확인

이 모듈에는 충전식 배터리가 내장되어 있습니다.

![USB-C Port Locations](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_17_usb_ports_comparison.jpg)
*그림 10: 상단 포트(CHARGE ONLY)와 측면 포트(FLASH ONLY)*

*   <strong>상단 USB-C 포트</strong>: <strong>충전 전용</strong>입니다(CHARGE ONLY 표기). 평소 충전에는 이 포트를 사용하십시오.
*   <strong>측면 USB-C 포트</strong>: <strong>펌웨어 플래싱 전용</strong>입니다(FLASH ONLY 표기). 이 포트로는 배터리가 충전되지 않으므로 충전기를 연결하지 마십시오.

#### 배터리 표시 LED:
모듈 전면에는 남은 충전량을 단계별로 나타내는 배터리 상태 LED 4개가 있습니다.

![Battery Level Indicator LEDs](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_18_battery_led_indicators.jpg)
*그림 11: 4개 상태 LED가 나타내는 배터리 잔량*

---

## 03. 문제 해결 체크리스트(초보자용)

모듈이 예상대로 작동하지 않는다면 다음 설정 사항을 확인해 주십시오.

*   [ ] <strong>GPIO 연결이 완전히 장착되어 있습니까?</strong> 모듈이 Flipper Zero 상단에 빈틈없이 밀착되어야 합니다(그림 8 참조).
*   [ ] <strong>GPS 안테나의 방향이 올바릅니까?</strong> 세라믹 면이 하늘을 향해야 합니다(그림 6 참조).
*   [ ] <strong>안테나가 올바른 포트에 연결되어 있습니까?</strong> 배치는 생산 배치마다 다릅니다. 케이스에 인쇄된 문자 라벨을 확인하십시오(그림 3 참조).
*   [ ] <strong>화면 스위치가 UP으로 설정되어 있습니까?</strong> (그림 9 참조).

---

## 04. 펌웨어 업데이트 및 플래싱(고급 사용자용)

새 펌웨어가 출시되면 측면 USB-C 포트를 사용하여 모듈을 플래싱합니다.

1.  USB-C 케이블을 컴퓨터에 연결합니다.
2.  <strong>중요한 플래싱 순서</strong>: 모듈 뒷면/오른쪽 측면의 부트/플래시 버튼을 누른 채로 USB-C 케이블을 <strong>측면 USB-C 포트(FLASH ONLY)</strong>에 꽂아 부트로더 모드로 진입합니다.

![Firmware Flashing Sequence](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_20_boot_flash_sequence.jpg)
*그림 12: 부트 버튼을 누르고 플래싱 케이블을 연결하는 올바른 순서*
