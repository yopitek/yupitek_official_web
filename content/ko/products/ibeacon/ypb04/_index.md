---
title: "YPB04 충전식 배지 비콘"
description: "YPB04 충전식 스마트 카드 배지 Bluetooth 비콘. 마그네틱 충전, 150m 통달 거리, IP67 방수 설계, 가속도 센서, 진동 모터, RGB LED, 선택형 RFID를 갖추어 인원 관리와 체크인에 적합합니다."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yopitek", "Rechargeable", "Badge", "RFID", "Sensor", "Vibration"]
---

## 제품 개요

<strong>YPB04</strong>는 스마트 오피스 체크인, 인원 동선 모니터링, 지오펜싱을 위해 설계된 착용형 카드 모양 Bluetooth® Low Energy(BLE 5.0) 비콘입니다. 얇은 배지 형태(86 × 55 × 6 mm, 무게 19g)로 목걸이 줄에 걸거나 유니폼에 부착하기 쉽습니다.

<strong>외부 푸시 버튼</strong>, <strong>진동 모터</strong>, <strong>RGB LED</strong>를 갖추고 있어 시각적, 물리적 피드백을 제공합니다. 마그네틱 충전 포트, 내장 3축 가속도 센서, 선택적인 듀얼 주파수 <strong>RFID(LF/HF/UHF)</strong> 지원을 통해 BLE 추적과 기존의 물리적 게이트 카드 출입을 함께 사용할 수 있습니다.

---

## 기술 사양

| 항목 | 사양 | 비고 |
| :--- | :--- | :--- |
| <strong>칩 모델</strong> | nRF52 시리즈 | 낮은 지연 시간과 높은 효율 |
| <strong>Bluetooth 버전</strong> | BLE 5.0 | 보안 연결 및 긴 통달 거리 |
| <strong>방수 등급</strong> | IP67 | 생활 방수 및 방진 (1m 침수) |
| <strong>센서</strong> | 3축 가속도 센서 | 변위 및 움직임 감지 |
| <strong>피드백 요소</strong> | 진동 모터 1개, RGB LED 1개 | 촉각 및 시각 신호 |
| <strong>제어 버튼</strong> | 외부 물리 버튼 1개 | 트리거 및 경보 작동 |
| <strong>RFID 호환성</strong> | LF / HF / UHF | 선택형 빌드 통합 |
| <strong>통달 거리</strong> | 최대 150미터 (492 ft) | 개방된 공간 기준 최대값 |
| <strong>전원</strong> | 마그네틱 충전식 Li-po 배터리 | 270mAh 용량 (충전식) |
| <strong>배터리 수명</strong> | 최대 3개월 | 클릭 빈도에 따라 다름 |
| <strong>충전 시간</strong> | 약 2시간 | 5V / 1A 전원 어댑터 |
| <strong>외형 치수 및 무게</strong> | 86 × 55 × 6 mm \| 19 g | 얇은 카드 형태 |

---

## 작동 가이드

### 배지 켜기
* 물리 버튼을 <strong>3초</strong> 동안 길게 누릅니다.
* 파란색 LED가 3초 동안 켜지고 장치가 한 번 진동하여 활성화되었음을 알려 줍니다.

### 배지 끄기
* 보안을 위해 장치는 <strong>BeaconSET+ 앱</strong>에서 설정 비밀번호를 입력한 후 무선으로만 끌 수 있습니다.
* 정상적으로 종료되면 파란색 LED가 5회 깜박입니다.

### 배터리 상태 및 충전
* <strong>배터리 부족 경고:</strong> 배터리가 20% 미만으로 떨어지면 빨간색 LED가 3초마다 한 번 깜박입니다.
* <strong>충전 표시:</strong> 충전 중에는 빨간색 LED가 계속 켜져 있습니다.
* <strong>충전 완료:</strong> 충전이 완료되면 녹색 LED가 계속 켜져 있습니다.

### 버튼 클릭 트리거
배지 버튼이 특정 송출을 트리거하도록 설정할 수 있습니다(예: 더블 클릭 또는 트리플 클릭으로 비상 신호 또는 체크인 텔레메트리 전송).
* <strong>더블 클릭:</strong> 파란색 LED가 2회 깜박이고 모터가 한 번 진동합니다.
* <strong>트리플 클릭:</strong> 파란색 LED가 3회 깜박이고 모터가 두 번 진동합니다.

---

## 설정 안내

YPB04의 파라미터(트리거 동작, UUID, Major, Minor 포함)는 <strong>BeaconSET+</strong> 애플리케이션을 통해 무선으로 설정합니다.
1. Google Play 또는 Apple App Store에서 <strong>BeaconSET+</strong>를 다운로드합니다.
2. 휴대폰의 Bluetooth와 위치 서비스가 켜져 있는지 확인합니다.
3. 앱을 열고 배지의 MAC 주소를 검색한 다음 눌러서 연결합니다.
4. 보안 기본 설정 비밀번호를 입력하여 잠금을 해제하고 파라미터를 편집합니다.

---

## 제품 갤러리

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb04.png" alt="Yopitek YPB04 충전식 스마트 카드 배지 비콘" />
{{< /gallery >}}

---

{{< alert >}}
제품 견적이 필요하신가요? [문의해 주십시오](/ko/contact/)
{{< /alert >}}
