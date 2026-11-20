---
title: "NVIDIA Mellanox LinkX 광섬유 패치 케이블"
description: "인증된 NVIDIA Mellanox LinkX 광섬유 패치 케이블을 선택하십시오. 오류 없는 NVIDIA 네트워킹을 위해 설계된 고밀도 OM4 멀티모드 MPO-12 패치 케이블입니다."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox LinkX 광섬유 패치 케이블 — OM4 멀티모드 MPO

NVIDIA LinkX® 광섬유 패치 케이블은 광 트랜시버 간의 물리적 연결을 제공합니다. LinkX 정품 광섬유 케이블을 사용하면 커넥터, 페룰 연마 상태, 유리 품질이 고속 이더넷 및 InfiniBand 네트워킹에 요구되는 엄격한 삽입 손실 및 반사 손실 허용치를 충족합니다.

---

## 광섬유 패치 케이블 카탈로그

다음은 당사가 보유한 인증 광섬유 케이블 목록입니다.

![Mellanox MPO 광섬유 패치 케이블](/images/products/mellanox/ai-generated/fiber-patch-mpo.jpg)
*NVIDIA Mellanox 고밀도 OM4 멀티모드 MPO-12 광섬유 패치 케이블*

| 부품 번호 | 커넥터 유형 | 길이 | 광섬유 유형 | 극성 | 대상 용도 |
|-------------|----------------|--------|------------|----------|--------------------|
| **MFP7E10-N003** | MPO-12 (female) to MPO-12 (female) | 3.0m | 멀티모드 OM4 | Type-B (Straight) | 100G/200G/400G 트랜시버 패치 |
| **MFP7E10-N005** | MPO-12 (female) to MPO-12 (female) | 5.0m | 멀티모드 OM4 | Type-B (Straight) | 100G/200G/400G 트랜시버 패치 |
| **MFP7E10-N010** | MPO-12 (female) to MPO-12 (female) | 10m | 멀티모드 OM4 | Type-B (Straight) | 100G/200G/400G 트랜시버 패치 |
| **MFP7E10-N015** | MPO-12 (female) to MPO-12 (female) | 15m | 멀티모드 OM4 | Type-B (Straight) | 100G/200G/400G 트랜시버 패치 |
| **MFP7E10-N020** | MPO-12 (female) to MPO-12 (female) | 20m | 멀티모드 OM4 | Type-B (Straight) | 100G/200G/400G 트랜시버 패치 |
| **MFP7E10-N030** | MPO-12 (female) to MPO-12 (female) | 30m | 멀티모드 OM4 | Type-B (Straight) | 100G/200G/400G 트랜시버 패치 |

---

## 기술 가이드: 광섬유 케이블 사양

### 1. OM4 멀티모드 광섬유 (MMF)
- **코어 직경**: 50µm(마이크로미터) 코어와 125µm 클래딩.
- **색상 표준**: 아쿠아/에리카 바이올렛.
- **대역폭**: 850nm에서 동작하는 VCSEL 레이저에 최적화되어 있습니다. OM4는 100Gb/s(SR4)에서 최대 100m, 25Gb/s(SR)에서 최대 150m까지 지원합니다.

### 2. MPO-12 커넥터
- **핀 구성**: MPO 커넥터에는 암수 구분이 있습니다. 트랜시버에는 핀(male)이 있으므로 패치 케이블은 올바르게 결합되도록 **핀 없는 / female**(가이드 홀 포함) 방식이어야 합니다.
- **끝면 연마**: 표준 MPO 커넥터는 **PC / UPC**(평면) 연마를 사용합니다. 고속 싱글모드 MPO와 최신 400G/800G 멀티모드 OSFP/QSFP112 트랜시버는 역반사를 제거하기 위해 **APC(Angled Physical Contact, 8도 경사)** 연마가 필요합니다. APC 커넥터는 녹색 커넥터 본체로 식별할 수 있습니다.

### 3. MPO 극성 표준
MPO-12 네트워크에서 극성은 한쪽 끝의 송신기가 반대쪽 끝의 수신기에 연결되도록 보장합니다.
- **Type-A (Key Up to Key Down)**: 직선 결선. Pin 1이 Pin 1에 연결됩니다.
- **Type-B (Key Up to Key Up)**: 역방향 결선. Pin 1이 Pin 12에 연결됩니다. **두 개의 SR4 트랜시버를 직접 연결할 때 업계 표준입니다.**
- **Type-C (Pair-wise Flipped)**: Pin 1/2, 3/4가 서로 바뀝니다. 주로 구조화된 백본 트렁킹에 사용됩니다.

---

{{< alert >}}
제품 견적이 필요하신가요? [문의해 주십시오](/ko/contact/)
{{< /alert >}}
