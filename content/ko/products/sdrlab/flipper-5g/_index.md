---
title: "SDRLab Flipper Zero 5G Add-On Board — 듀얼 밴드 Wi-Fi 보안 연구 모듈"
seo_title: "Flipper Zero 5G Add-On Board | SDRLab 대만 | Yopitek"
description: "SDRLab Flipper Zero 5G 애드온 보드: ESP32-C5 듀얼 밴드 2.4/5 GHz Wi-Fi, 433 MHz 모듈, 액티브 GPS, 2.8인치 TFT. Yopitek에서 대만 공급."
date: 2026-03-12
draft: false
featureimage: "/images/products/sdrlab/flipper-5g.png"
hideFeatureImage: true
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero 애드온", "5GHz", "Wi-Fi", "Deauth", "보안 연구"]
faq:
  - question: "SDRLab Flipper Zero 5G 보드는 어떤 칩과 Wi-Fi 대역을 사용합니까?"
    answer: "듀얼 밴드 2.4 GHz 및 5 GHz Wi-Fi를 지원하는 Espressif ESP32-C5를 사용합니다. ESP32 Marauder 5G 펌웨어가 공장에서 사전 설치되어 출고됩니다."
  - question: "Flipper Zero 5G 보드에는 어떤 안테나가 포함되어 있습니까?"
    answer: "2.4G, 2.4G/5G 듀얼 밴드, 433M, GPS 안테나 4개가 포함되며, 각각 별도의 SMA 커넥터를 사용합니다. Wi-Fi 안테나는 3 dBi (11 cm), 433M 안테나는 3 dBi, GPS 안테나는 20 dBi입니다."
  - question: "보드를 Flipper Zero에 연결한 후 어떤 설정이 필요합니까?"
    answer: "GPIO 핀 설정에서 GPS Pin을 13 또는 14로, ESP32 Pin을 15, 16으로 설정하고 Sub-GHz 모듈을 External로 설정해야 합니다. GPS와 ESP32는 서로 다른 UART 핀을 사용하므로 같은 그룹으로 설정할 수 없습니다."
  - question: "보드에 Flipper Zero가 포함되어 있으며, 어떤 펌웨어가 동작합니까?"
    answer: "아니요, Flipper Zero 호스트는 별도 판매입니다. 이 보드는 Momentum, Unleashed, Xtreme 등의 커스텀 펌웨어와 호환되며, 허가된 보안 연구 용도로만 사용해야 합니다."
---

# SDRLab Flipper Zero 5G 확장 보드 — 듀얼 밴드 Wi-Fi 보안 연구 모듈

> **합법적 사용 선언**: 이 확장 보드는 허가된 보안 연구와 정당한 학습 목적으로만 사용해야 합니다. 소유하지 않았거나 서면 허가를 받지 않은 네트워크, 장치 또는 인프라를 테스트하는 행위는 대부분의 국가 및 지역에서 불법입니다. 현지 무선 주파수 규정을 준수하시고, 책임감 있고 윤리적으로 사용하시기 바랍니다.

---

SDRLab Flipper Zero 5G Add-On Board는 허가된 무선 보안 연구 및 교육을 위한 GPIO 확장 보드입니다. ESP32-C5 듀얼 밴드 2.4/5 GHz Wi-Fi, 433 MHz 모듈, 액티브 GPS, 2.8인치 TFT를 추가하며, Marauder 5G 펌웨어가 사전 설치되어 있습니다. 대만 내 견적은 Yopitek에 문의해 주십시오.

## 1. 제품 소개

Flipper Zero 뒷면의 GPIO 헤더에 장착하는 무선 연구용 확장 보드입니다. 2.4GHz만 지원하는 기본 Flipper에 세 가지 무선 기능을 한 번에 추가합니다.

- **듀얼 밴드 Wi-Fi 2.4GHz + 5GHz**
- **433MHz Sub-GHz** RF
- **액티브 GPS**

이와 함께 **2.8인치 컬러 TFT 화면**, **800mAh 핫스왑 배터리**, **SMA 안테나 인터페이스 4개와 안테나 4개 포함**을 갖추고 있으며, **ESP32 Marauder 5G 펌웨어가 공장에서 사전 설치**되어 있습니다.

별도의 프로그래머를 구입하거나 펌웨어를 직접 컴파일할 필요가 없습니다. 연결한 뒤 세 가지 파라미터만 설정하면 바로 사용할 수 있습니다.

---

## 2. 제품 특징

### 세 가지 무선 기능을 하나로
- **듀얼 밴드 Wi-Fi 2.4GHz + 5GHz** — 2.4GHz만 지원하던 기존 보드의 한계를 넘어 최신 5GHz 네트워크를 스캔할 수 있습니다.
- **433MHz Sub-GHz (A07 RF 모듈, 10 dBm)** — Flipper 내장 수신기의 성능이 좋지 않은 환경에서 대안을 제공합니다.
- **액티브 GPS** — 워드라이빙 로그에 좌표를 자동으로 추가합니다. Flipper에 연결되어 있을 때는 Flipper에서 전원을 공급받고, 분리하면 내부 배터리로 전환됩니다.

### 2.8인치 컬러 TFT 화면
스캔 결과, 신호 강도, 배터리 잔량이 보드에 직접 표시되므로 컴퓨터 터미널을 계속 쳐다볼 필요가 없습니다. Marauder UI가 내장되어 있습니다.

### SMA 안테나 인터페이스 4개, 안테나 4개 포함
후면 커버에 각 인터페이스의 용도가 실크스크린으로 명확하게 표시되어 있습니다.

| 실크스크린 | 위치 | 용도 |
|---|---|---|
| `433M A` | 좌측 상단 | 433MHz RF (A07 모듈, 10 dBm) |
| `GPS` | 우측 상단 | 액티브 GPS 안테나 |
| `2.4G` | 좌측 윙 | Wi-Fi 2.4GHz |
| `2.4G/5G` | 우측 윙 | Wi-Fi 듀얼 밴드 2.4GHz + 5GHz |

네 개의 인터페이스 모두 독립적인 나사 잠금식 SMA 암 커넥터를 사용합니다. **주문 시 안테나 4개가 포함됩니다**: Wi-Fi 안테나 3 dBi (11 cm), 433M 안테나 3 dBi, GPS 안테나 20 dBi.

### 800mAh 핫스왑 배터리
800mAh Li-Po 배터리가 내장되어 있습니다. Flipper에서 분리하여 단독으로 부팅하고 패킷을 캡처한 다음, 스캔이 끝나면 확장 보드로서 호스트에 다시 장착할 수 있습니다.

### Marauder 5G 펌웨어 사전 설치
별도의 프로그래머 없이 바로 사용할 수 있습니다. 펌웨어를 수동으로 업그레이드하려는 고급 사용자를 위해 USB-C 프로그래밍 포트가 유지되어 있습니다.

### 골드 핑거 + TVS 서지 보호
모든 신호 핀은 금도금 처리되어 있으며, 각 핀에는 내부 TVS(Transient Voltage Suppression) 다이오드가 포함되어 Flipper와 탈착할 때 서지 보호를 제공합니다.

### 펌웨어 생태계 호환성
WiFi Marauder 및 GPS 애플리케이션을 포함한 Momentum, Unleashed, Xtreme 등의 커스텀 펌웨어와 호환됩니다.

---

## 3. 제품 사양

| 사양 | 값 / 설명 |
|---|---|
| **메인 칩** | **Espressif ESP32-C5** |
| **Wi-Fi 대역** | 듀얼 밴드 2.4GHz + 5GHz |
| **Wi-Fi 안테나 인터페이스** | **SMA 암 커넥터 4개**: 433M A / GPS / 2.4G / 2.4G+5G. **안테나 4개 포함**: Wi-Fi 3 dBi (11 cm), 433M 3 dBi, GPS 20 dBi |
| **Sub-GHz** | 433MHz A07 RF 모듈, **10 dBm** 출력 |
| **GNSS** | 액티브 GPS 모듈, **자동 전원 전환** (연결 시 호스트 전원, 분리 시 내부 배터리) |
| **화면** | **2.8인치 컬러 TFT**, Marauder UI 내장 |
| **배터리** | **800 mAh Li-Po**, 핫스왑 가능 |
| **연결 인터페이스** | Flipper Zero 표준 GPIO 헤더 (**2×8 핀**), 골드 핑거 + 핀별 TVS 보호 |
| **사전 설치 펌웨어** | **ESP32 Marauder 5G** (오픈소스, 공장 사전 설치) |
| **펌웨어 호환성** | Momentum, Unleashed, Xtreme |

### 포함 액세서리
- 본체 1개 (조립 완료, 케이스와 2.8인치 화면 포함)
- 안테나 4개 — `2.4G` 1개, `2.4G+5G` 듀얼 밴드 1개, `433M A` 1개, `GPS` 1개 (Wi-Fi 3 dBi / 433M 3 dBi / GPS 20 dBi)
- Flipper GPIO 헤더 연결부

### 별도 판매
- **Flipper Zero 호스트** (이 보드는 확장 모듈이며 호스트는 포함되지 않습니다)

---

## 4. 시작하기: 필수 설정 세 가지

보드에는 펌웨어가 사전 설치되어 있으므로 프로그래밍이 필요 없습니다. Flipper에 연결한 후 세 가지 핀 설정만 구성하면 됩니다.

| 기능 | 설정 경로 | 값 |
|---|---|---|
| **GPS** | Momentum → Protocol Settings → GPIO Pin Settings → **GPS Pin** | **13 또는 14** |
| **ESP32 (WiFi / Marauder)** | 위와 동일 → **ESP32 Pin** | **15, 16** |
| **433MHz Sub-GHz** | Flipper → Sub-GHz → Advanced Settings → **Module** | **External** |

> ⚠️ **GPS와 ESP32는 서로 다른 두 UART 핀 세트를 사용하므로 같은 그룹으로 설정할 수 없습니다.** 같은 그룹으로 설정하면 GPS와 Wi-Fi가 모두 응답하지 않게 됩니다.

설정을 마친 후 Flipper를 재시작하십시오. `Apps → GPIO` 아래에 해당 WiFi Marauder 및 GPS 애플리케이션이 표시됩니다.

---

## 5. 활용 시나리오

- **듀얼 밴드 Wi-Fi 스캔** — 2.4GHz 및 5GHz 네트워크를 수동으로 열거하며 SSID, BSSID, Channel, RSSI, 암호화 유형, 연결된 클라이언트를 수집합니다.
- **WPA 핸드셰이크 캡처** — 허가된 네트워크의 보안 감사를 위해 EAPOL/PMKID 핸드셰이크 패킷을 스니핑합니다.
- **Deauth 테스트** — 네트워크 복원력을 테스트하기 위해 Deauth 패킷을 전송합니다. 소유하거나 허가받은 네트워크에 한정됩니다.
- **워드라이브 네트워크 토폴로지 매핑** — GPS 태그가 포함된 Wi-Fi 및 장치 기록을 CSV로 내보내 추가 분석에 활용합니다.
- **433MHz RF 연구** — Flipper의 Sub-GHz 메뉴에서 조작하며, Flipper 내장 수신기의 성능이 좋지 않은 환경에 적합합니다.
- **Evil Portal 훈련** — 허가된 환경에서 랜딩 페이지를 프로토타입 테스트합니다.
- **IoT 무선 프로토콜 연구** — 통제된 실험실 환경에서 듀얼 밴드에 걸친 IoT 장치의 동작을 분석합니다.

---

## 6. 알려진 제한 사항 (꼭 확인하십시오)

- **5GHz Deauth의 안정성은 펌웨어 버전에 따라 달라집니다.** ESP32-C5에서 오픈소스 Marauder 펌웨어의 5GHz deauth 지원은 아직 지속적으로 개선되고 있습니다. Deauth 테스트는 주로 **2.4GHz**에서 수행하기를 권장합니다. 5GHz에서는 스캔, 신호 모니터링, 워드라이빙 로깅을 주요 기능으로 사용하십시오. 실제 성능은 현재 펌웨어 버전에 따라 달라집니다.
- **GPS 안테나는 지향성입니다.** 무지향성으로 홍보되고 있으나 실제로는 그렇지 않습니다. 최적의 측위를 위해 안테나가 탁 트인 하늘을 향하도록 배치하십시오. 최초 콜드 스타트 시에는 위성 궤도력 데이터를 내려받는 데 수 분이 소요됩니다. 실내에서는 성능이 좋지 않으므로 실외나 창가 근처에서 사용하기를 권장합니다.
- **GPS는 시간을 UTC+0으로 보고합니다.** 펌웨어 메뉴에는 시간대 설정 옵션이 없습니다. 대만 시간(UTC+8)을 사용하려면 수동으로 8시간을 더하십시오.
- **GPS와 ESP32는 서로 다른 UART 핀을 사용합니다** (GPS: 13 또는 14, ESP32: 15, 16). 같은 그룹으로 설정할 수 없으며, 그렇게 하면 GPS와 Wi-Fi가 모두 응답하지 않게 됩니다.
- **펌웨어 플래시 포트** — 전면 좌측의 USB-C 포트는 펌웨어 플래시용입니다.
- **GPS 자동 전원 전환** — Flipper에 연결되어 있을 때는 호스트에서 전원을 공급받고, 분리하면 내부 배터리로 전환됩니다. 전환 중 잠시 재시작되는 것은 정상입니다.

---

**제품 페이지 링크**: https://yupitek.com/ko/products/sdrlab/flipper-5g/
**전체 사용자 매뉴얼**: https://doc.yupitek.com/sdrlab/expansion/5g-board/
**제조사 스토어 페이지 (OpenSourceSDRLab)**: https://opensourcesdrlab.com/products/opensourcesdrlab-new-5g-multi-in-one-module-flipperzero-module-with-screen-flipperzero5g-expansion-board?VariantsId=10754

{{< faq >}}
