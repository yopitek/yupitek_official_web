---
title: "Flipper Zero 입문 가이드: 개봉, 설정, 펌웨어 업데이트, 5가지 핵심 기능"
slug: flipper-zero-beginners-guide-setup-tutorial
published: 2026-08-10
author: Yopitek
category: Technical
tags:
  - Flipper Zero
  - Tutorial
hero_image: /static/img/flipper-zero/hero.webp
hero_alt: "Flipper Zero 입문 가이드: 개봉, 펌웨어 업데이트, 5가지 핵심 기능 실측 | Yopitek"
seo_description: "Flipper Zero란 무엇일까요? 개봉, microSD 설정, qFlipper 펌웨어 업데이트부터 RFID, Sub-GHz, NFC, IR, BadUSB 실전 테스트까지, 이 가이드가 Flipper Zero를 시작하는 데 도움이 됩니다."
---

> 요약: Flipper Zero는 125 kHz RFID, Sub-GHz, NFC, 적외선, BLE를 갖춘 휴대용 하드웨어 탐색 도구입니다. USB-C로 연결하면 키보드(BadUSB)로 동작할 수 있습니다. 개봉 후 microSD 카드를 설치하고, qFlipper 또는 모바일 앱으로 펌웨어를 업데이트한 다음, RFID 읽기와 IR 리모컨 제어부터 시작해 보십시오. 이러한 기능은 항상 <strong>본인 소유이거나 명시적으로 테스트 권한을 받은 기기</strong>에서만 사용하십시오.

## Flipper Zero란 무엇이며 누구를 위한 제품입니까?

Flipper Zero는 손바닥만 한 크기의 다기능 휴대용 장치로, "하드웨어 탐색 도구"를 표방합니다. 일반 소비자용 기기가 아니라 사이버 보안 연구자, 침투 테스트 입문자, 메이커, IoT 엔지니어가 흔히 쓰이는 무선 프로토콜과 디지털 신호를 읽고, 분석하고, 에뮬레이션할 수 있도록 설계된 장치입니다.

핵심 하드웨어 기능은 다음과 같습니다.

- <strong>125 kHz RFID</strong>: 저주파 출입 카드를 읽고 에뮬레이션합니다.
- <strong>Sub-GHz 무선</strong>(CC1101 칩셋): 300–928 MHz 대역의 리모컨, 차고 문, IoT 센서 신호를 분석합니다.
- <strong>NFC (13.56 MHz)</strong>: 고주파 카드를 읽고, 쓰고, 에뮬레이션합니다.
- <strong>적외선(IR)</strong>: TV, 에어컨 등의 IR 코드를 학습하고 다시 송신합니다.
- <strong>BLE</strong>: 모바일 앱으로 페어링하고 제어합니다.
- <strong>USB-C</strong>: 컴퓨터에 연결하여 펌웨어를 업데이트하고 키보드를 에뮬레이션합니다(BadUSB / DuckyScript).
- <strong>GPIO / iButton</strong>: 1-Wire 접촉식 키와 하드웨어 확장.

<strong>이런 분께 적합합니다:</strong> 무선 보안 연구를 준비하는 학생, 자신의 출입 통제 시스템이나 센서의 신뢰성을 검증하는 엔지니어, RFID/NFC 원리에 관심 있는 메이커. 단순히 "리모컨 복사기"를 찾으신다면 Sub-GHz 기능으로 구현할 수 있지만, 먼저 현지 법률과 사용 시나리오를 확인하십시오.

## 개봉 및 초기 설정: 전원을 켜기 전에 microSD 설치

Flipper Zero는 microSD 카드 없이 출고되지만, 펌웨어와 데이터 저장을 위해 카드를 사용하는 것을 <strong>강력히 권장</strong>합니다. 다음 단계를 따르십시오.

1. <strong>microSD 카드 준비</strong>: 4 GB 이상의 카드를 사용하고 FAT32로 포맷합니다(FAT16/FAT32/exFAT를 지원합니다). 기기 하단의 슬롯에 <strong>칩 면이 위를 향하도록</strong> 카드를 삽입합니다.
2. <strong>충전</strong>: USB-C로 충전기나 컴퓨터에 연결하여 처음 사용하기 전에 완전히 충전합니다.
3. <strong>전원 켜기</strong>: 기기 뒷면의 Back 버튼을 약 3초간 길게 누릅니다. 돌고래 애니메이션이 나타나면 부팅에 성공한 것입니다.
4. <strong>시스템 버전 확인</strong>: `Settings → About`으로 이동하여 업데이트를 진행하기 전에 현재 펌웨어 버전을 기록해 둡니다.

> 참고: Flipper Zero는 기본적으로 영어 인터페이스를 사용합니다. 일부 서드파티 펌웨어는 중국어를 지원하지만, <strong>신규 사용자는 처음에는 서드파티 펌웨어를 설치하지 않는 것을 권장합니다</strong>. 먼저 공식 펌웨어의 작업 흐름에 익숙해지십시오.

## 펌웨어 업데이트: qFlipper 데스크톱과 모바일 앱

펌웨어 업데이트는 Flipper Zero를 시작할 때 가장 중요한 단계입니다. 제조사가 버그를 지속적으로 수정하고 프로토콜 지원을 추가하므로, 오래된 펌웨어 버전에서는 일부 카드나 신호를 읽지 못할 수 있습니다.

### 방법 1: qFlipper 데스크톱(권장)

1. Flipper 공식 웹사이트에서 사용 중인 플랫폼(Windows / macOS / Linux)용 qFlipper를 다운로드합니다.
2. USB-C로 Flipper Zero를 컴퓨터에 연결하고 qFlipper를 실행합니다.
3. 오른쪽 상단의 렌치 아이콘(Advanced controls)을 클릭하고 "Firmware update channel"을 선택합니다.
4. <strong>Release (Stable)</strong>를 선택하고 Update를 클릭합니다.
5. 업데이트가 끝날 때까지 기다립니다(약 5–10분 소요). 기기가 자동으로 재시작됩니다.

### 방법 2: 모바일 앱

1. 공식 Flipper Mobile App(iOS / Android)을 설치합니다.
2. 휴대폰의 Bluetooth를 켜고 Flipper Zero와 페어링합니다(기기에서: `Settings → Bluetooth`).
3. 앱에서 Update를 탭하면 BLE로 펌웨어가 전송되며, 약 10분이 걸립니다.

### 펌웨어 채널은 어떻게 선택합니까?

| 채널 | 안정성 | 대상 |
|---|---|---|
| Release (Stable) | 높음 | <strong>신규 사용자는 항상 이 채널을 선택하십시오</strong> |
| Release Candidate (RC) | 보통 | 새 기능을 미리 테스트하려는 사용자 |
| Development | 낮음 | 개발자 및 테스터 |

> ⚠️ 업데이트 중에는 케이블을 분리하거나 전원을 끊지 마십시오. 기기가 부팅 화면에서 멈추면 복구 모드로 진입하여 다시 플래싱할 수 있습니다(Reset 버튼을 빠르게 두 번 누릅니다). 서드파티 펌웨어(예: Xtreme)는 확장 기능을 제공하지만 불안정할 수 있습니다. 신규 사용자는 공식 안정 버전을 사용하십시오.

## 실전 테스트: 5가지 핵심 기능

### 1. 125 kHz RFID: 저주파 카드 읽기와 에뮬레이션

오래된 출입 카드(125 kHz)는 대개 암호화 없이 ID 코드만 담고 있습니다. Flipper Zero 하단에는 LF 안테나가 있어, 카드를 가까이 대기만 하면 읽을 수 있습니다.

1. 메인 메뉴 → `125 kHz RFID` → `Read`.
2. 카드를 기기 하단에 평평하게 댑니다. 읽기에 성공하면 UID와 데이터가 표시됩니다.
3. 에뮬레이션하려면 읽은 후 `Emulate`를 선택합니다. 이제 기기가 임시 대체 카드 역할을 할 수 있습니다.

### 2. Sub-GHz: 300–928 MHz 무선 신호 분석

내장된 CC1101 트랜시버로 리모컨, 차고 문, IoT 센서의 신호를 캡처할 수 있습니다.

1. 메인 메뉴 → `Sub-GHz` → `Read Raw`.
2. 리모컨의 버튼을 누릅니다. 화면에 주파수와 신호 파형이 표시됩니다.
3. 신호를 저장하고 `Replay`를 선택하면 다시 송신합니다. 주파수를 직접 설정하여 주변의 무선 활동을 스캔할 수도 있습니다.

### 3. NFC: 13.56 MHz 카드 읽기, 쓰기, 에뮬레이션

NFC 모듈은 일반적인 13.56 MHz 표준을 지원합니다. 교통카드 같은 비접촉식 카드의 UID와 데이터 블록을 읽을 수 있습니다(완전한 에뮬레이션 가능 여부는 카드의 암호화 방식에 따라 다릅니다).

1. 메인 메뉴 → `NFC` → `Read`.
2. 카드를 기기 뒷면에 대고 정보를 읽습니다.
3. 카드 유형에 따라 `Emulate` 또는 `Write`를 선택합니다.

### 4. IR: 적외선 코드 학습과 재송신

내장된 IR 송수신기로 TV, 에어컨, 프로젝터의 코드를 학습하고 다시 송신할 수 있습니다.

1. 메인 메뉴 → `Infrared` → `Learn`.
2. 리모컨을 기기 상단의 IR 창에 향하고 버튼을 누릅니다. 학습이 끝나면 이름을 붙여 코드를 저장합니다.
3. `Infrared → Saved`에서 언제든 코드를 다시 송신할 수 있습니다.

### 5. BadUSB / DuckyScript: USB-C 키보드 에뮬레이션

컴퓨터에 연결하면 Flipper Zero가 USB 키보드를 에뮬레이션하여 DuckyScript 스크립트(자동 키 입력)를 실행할 수 있습니다.

1. `.txt` 스크립트(DuckyScript 문법으로 작성)를 microSD 카드의 `badusb/` 폴더에 넣습니다.
2. USB-C로 Flipper Zero를 대상 컴퓨터에 연결합니다. 메인 메뉴에서 `BadUSB`로 이동하여 실행할 스크립트를 선택합니다.

> ⚠️ <strong>BadUSB는 매우 민감한 기능입니다</strong>: 스크립트는 키보드 입력으로 컴퓨터에서 명령을 실행하므로, 사실상 "누군가 컴퓨터 앞에서 타이핑하는 것"과 같습니다. 본인의 컴퓨터이거나 테스트 권한을 명시적으로 받은 환경에서만 사용하십시오.

## 합법적 사용 안내(필독)

Flipper Zero 자체는 합법적인 도구이지만, 사용 시나리오에는 명확한 법적 경계가 있습니다.

- <strong>출입 카드 및 리모컨 복사/에뮬레이션</strong>: 본인이 소유하거나 관리자 권한을 부여받은 시스템에만 하십시오. 타인의 출입 카드나 차고 리모컨을 무단으로 읽거나 에뮬레이션하면 형법(사생활 침해), 통신 관련 법률, 개인정보 보호 규정에 따른 법적 책임이 발생할 수 있습니다.
- <strong>BadUSB</strong>: 허가 없이 타인의 컴퓨터에서 스크립트를 실행하는 것은 불법입니다.
- <strong>신호 간섭</strong>: 타인의 무선 기기(예: 차고 문)를 의도적으로 방해하면 법적 위험이 따릅니다.

<strong>원칙은 간단합니다. 본인이 소유했거나 서면으로 테스트 권한을 받은 기기만 테스트하십시오.</strong>

## 자주 묻는 질문(FAQ)

<strong>Q1: Flipper Zero에 microSD 카드를 꼭 설치해야 합니까?</strong>
필수는 아니지만 강력히 권장합니다. 대부분의 앱, 신호 라이브러리, BadUSB 스크립트가 microSD 카드에 저장됩니다. 카드가 없으면 기능이 크게 제한됩니다.

<strong>Q2: 펌웨어를 업데이트하면 기기가 벽돌이 됩니까?</strong>
공식 안정 펌웨어의 위험은 매우 낮습니다. 정전이나 케이블 분리로 업데이트가 중단되지만 않으면 실패하는 경우는 드뭅니다. 이상이 생기면 복구 모드로 다시 플래싱할 수 있습니다.

<strong>Q3: 교통카드(예: EasyCard)를 복사할 수 있습니까?</strong>
최신 교통카드는 대부분 암호화와 키 보호가 적용되어 있습니다. Flipper Zero는 UID나 암호화되지 않은 블록만 읽을 수 있으며, 카드를 완전히 복사할 수는 없습니다. 또한 교통카드를 무단으로 복사하는 것은 불법입니다.

<strong>Q4: Flipper Zero와 SDR(소프트웨어 정의 라디오)은 어떻게 다릅니까?</strong>
Flipper Zero에 내장된 Sub-GHz 트랜시버는 일반적인 프로토콜(OOK/ASK/FSK 등)에 초점을 맞추고 있어 조작이 직관적입니다. SDR(HackRF, RTL-SDR 등)은 더 넓은 주파수 범위와 원시 스펙트럼 분석을 제공하지만 컴퓨터와 더 깊은 기술 배경이 필요합니다. 두 도구는 서로 보완적입니다.

<strong>Q5: Flipper Zero는 어디에서 구매할 수 있습니까?</strong>
Yopitek은 Flipper Zero 제품과 관련 액세서리를 공급하며 기술 상담도 제공합니다. 구매 후 설정 관련 문의는 sales@yupitek.com으로 이메일을 보내 주십시오.

<strong>Q6: 서드파티 펌웨어를 설치해도 됩니까?</strong>
가능하지만 초보자에게는 권장하지 않습니다. 서드파티 펌웨어(예: Xtreme)는 인터페이스 커스터마이징과 추가 기능을 제공하지만, 안정성과 보안은 직접 평가해야 하며 공식 업데이트 지원을 받지 못할 수 있습니다.

## 요약

Flipper Zero를 시작하는 길은 간단합니다. <strong>microSD 설치 → 공식 안정 펌웨어로 업데이트 → RFID 읽기와 IR 리모컨 제어부터 시작 → 익숙해지면 Sub-GHz와 BadUSB 탐색.</strong> 무선 프로토콜과 하드웨어 보안을 이해하는 훌륭한 출발점입니다. 다만 기억하십시오. 도구가 강력할수록 스스로를 더 엄격히 다스려야 합니다. 접근 권한이 있는 기기만 테스트하십시오.

Flipper Zero 또는 관련 액세서리에 대해서는 [sales@yupitek.com](mailto:sales@yupitek.com)으로 문의해 주십시오. Yopitek이 제품 및 기술 상담 서비스를 제공합니다.
