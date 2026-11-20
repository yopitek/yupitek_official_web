---
title: "YPB02 모션 감지 BLE 비콘"
description: "YPB02 Bluetooth Low Energy(BLE 5.0) 센서 비콘. LIS3DH 3축 가속도 센서, 교체 가능한 CR2477 배터리, IP67 방수 설계를 갖추어 움직임 감지, 낙상 경보, 자산 추적에 적합합니다."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yopitek", "CR2477", "Waterproof", "Sensor", "Accelerometer"]
---

## 제품 개요

<strong>YPB02</strong>는 <strong>LIS3DH 3축 가속도 센서</strong>를 내장한 모션 감지 Bluetooth® Low Energy(BLE 5.0) 비콘입니다. YPB01과 동일한 소형 폼팩터, 교체 가능한 1000mAh CR2477 코인 셀 배터리, IP67 방수 케이스를 공유하면서 지능형 움직임 감지와 텔레메트리 기능이 추가되었습니다.

이 비콘은 트리거 기반 광고를 지원하여, 이동, 진동 또는 낙상이 발생할 때에만 실시간 가속도 데이터를 송출하거나 송신 간격을 변경할 수 있습니다. 이를 통해 배터리 소모를 최소화하고 고급 자산 활동 모니터링을 구현할 수 있습니다.

---

## 기술 사양

| 항목 | 사양 | 비고 |
| :--- | :--- | :--- |
| <strong>칩 모델</strong> | nRF52 시리즈 | 초저전력 소비 |
| <strong>Bluetooth 버전</strong> | BLE 5.0 | 높은 효율과 속도 |
| <strong>방수 등급</strong> | IP67 | 생활 방수 및 방진 (1m 침수) |
| <strong>센서</strong> | LIS3DH 3축 가속도 센서 | X, Y, Z축 텔레메트리 |
| <strong>통달 거리</strong> | 최대 100미터 | 개방된 공간 기준 |
| <strong>안테나 임피던스</strong> | 50 ohm | 온보드 / PCB 안테나 |
| <strong>전원</strong> | CR2477 코인 배터리 1개 | 교체 가능 (3.0V, 1000mAh) |
| <strong>동작 전압</strong> | 1.8V - 3.9V | DC |
| <strong>피크 전류</strong> | 5.3 mA | 0dBm 송신 출력에서 측정 |
| <strong>외형 치수</strong> | Φ39 × 15.5 mm | 소형 원형 |
| <strong>기본 설정</strong> | UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms | 앱에서 설정 가능 |

---

## 주요 특징

* <strong>3축 가속도 센서:</strong> LIS3DH 센서가 X, Y, Z축을 따라 변위, 기울기, 움직임 텔레메트리를 매핑합니다.
* <strong>트리거 기반 송출:</strong> 특정 트리거 조건을 설정할 수 있습니다(예: 움직일 때만 송출, 낙상 경보, 자산 이동 추적을 위해 이동 시 간격을 100ms로 변경).
* <strong>고보호 케이스:</strong> IP67 방수 및 방진 등급으로 실내 및 가벼운 실외 설치가 가능합니다.
* <strong>교체 가능한 배터리:</strong> 장수명 CR2477 배터리(1000mAh)를 회전식 하우징 구조로 쉽게 교체할 수 있습니다.

---

## 모션 트리거 및 텔레메트리

LIS3DH 센서를 사용하여 YPB02는 다음을 지원합니다.
1. <strong>활동 기반 광고:</strong> 표준 iBeacon/Eddystone 프레임은 계속 송출하되, 비콘이 이동하거나 움직일 때에만 센서 데이터 프레임(HT/ACC)을 송출합니다.
2. <strong>공존 모드:</strong> 정지 상태와 움직임 상태에 대해 서로 다른 파라미터를 지원합니다. 예를 들어 정지해 있을 때는 비콘이 무음(슬립 모드) 상태를 유지하고, 이동하면 100ms 간격으로 송출하여 실시간 위치를 추적할 수 있습니다.
3. <strong>임계값 보정:</strong> 가속도 임계값과 트리거 지속 시간을 앱에서 사용자 지정할 수 있습니다.

---

## 설정 안내

YPB02의 파라미터(가속도 센서 임계값, 트리거, UUID, Major, Minor 포함)는 <strong>BeaconSET+</strong> 애플리케이션을 통해 무선으로 설정합니다.
1. Google Play 또는 Apple App Store에서 <strong>BeaconSET+</strong>를 다운로드합니다.
2. 휴대폰의 Bluetooth와 위치 서비스가 켜져 있는지 확인합니다.
3. 앱을 열고 비콘의 MAC 주소를 검색한 다음 눌러서 연결합니다.
4. 보안 기본 설정 비밀번호를 입력하여 잠금을 해제하고 파라미터를 편집합니다.

---

## 제품 갤러리

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb02.png" alt="Yopitek YPB02 센서 BLE 5.0 코인 비콘" />
{{< /gallery >}}

---

{{< alert >}}
제품 견적이 필요하신가요? [문의해 주십시오](/ko/contact/)
{{< /alert >}}
