---
title: "NVIDIA Mellanox LinkX 광 트랜시버"
description: "NVIDIA Mellanox LinkX 정품 광 트랜시버 모듈을 선택하십시오. 멀티모드 및 싱글모드 네트워크용 고속 25G, 100G, 400G, 800G 트랜시버입니다."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox LinkX 광 트랜시버 — 25G에서 800G까지

NVIDIA LinkX® 광 트랜시버는 고성능 컴퓨팅, 엔터프라이즈 스토리지, 하이퍼스케일 환경의 엄격한 요구 사항을 충족하도록 설계되었습니다. 정품 트랜시버를 사용하면 최적의 신호 무결성, 가장 낮은 비트 오류율(BER), ConnectX 어댑터 및 Quantum 스위치와의 완전한 호환성을 확보할 수 있습니다.

---

## 광 트랜시버 카탈로그

다음은 당사가 보유한 활성 광 트랜시버 모델 목록입니다.

<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin: 1.5rem 0;">
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/sfp28-25g-transceiver.jpg" alt="25G SFP28 Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA Mellanox 25G SFP28 SR Optical Transceiver</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/qsfp28-100g-transceiver.jpg" alt="100G QSFP28 Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA Mellanox 100G QSFP28 SR4 Optical Transceiver</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/osfp-400g-transceiver.jpg" alt="400G OSFP Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA 400G OSFP NDR Optical Transceiver</p>
  </div>
</div>

| 부품 번호 | 속도 | 인터페이스 | 커넥터 | 파장 | 광섬유 유형 | 최대 거리 | 설명 |
|-------------|-------|-----------|-----------|------------|------------|--------------|-------------|
| **MMA2P00-AS** | 25G | SFP28 | LC Duplex | 850nm | 멀티모드 (MMF) | 150m (OM4) / 100m (OM3) | 25GbE SR 모듈 |
| **MMA1B00-C100-TG** | 100G | QSFP28 | MPO-12 | 850nm | 멀티모드 (MMF) | 100m (OM4) / 70m (OM3) | 100GbE SR4 모듈, DDMI |
| **MMA4Z00-NS400** | 400G | OSFP | MPO-12 APC| 850nm | 멀티모드 (MMF) | 50m (OM4) | NDR IB/ETH SR 모듈, Flat Top |
| **MMA4Z00-NS** | 800G | OSFP | 2xMPO-12 APC| 850nm | 멀티모드 (MMF) | 50m (OM4) | 2xNDR 트윈 포트 SR 모듈, Finned |

---

## 거리 및 케이블링 참고 가이드

### 1. SR, SR4, NDR (멀티모드 솔루션)
- **25G SR (SFP28)**: 표준 LC-LC 듀플렉스 멀티모드 패치 케이블을 사용합니다. 송신과 수신에 각각 단일 레인을 사용합니다.
- **100G SR4 (QSFP28)**: 12심 MPO(MPO-12) 리본 패치 케이블(일반적으로 Type-B 극성)을 사용하여 25G 병렬 레인 4개로 전송합니다.
- **400G/800G NDR (OSFP)**: PAM4 변조를 사용하여 MPO-12 APC(Angled Physical Contact) 커넥터로 초고대역폭을 전송합니다. 경사진 끝면이 역반사를 최소화하며, 이는 더 높은 속도에서 매우 중요합니다.

### 2. 싱글모드 (LR4/FR4)와 멀티모드 (SR/SR4)
- **멀티모드 (MMF)**: 랙 내부 또는 단거리 랙 간 배선(최대 100–150m)에 적합합니다. 트랜시버 비용이 더 낮습니다.
- **싱글모드 (SMF)**: 150m를 초과하는 거리(LR4의 경우 최대 10km)에 필요합니다. 9/125µm 광섬유에 듀플렉스 LC 커넥터를 사용합니다.

---

## 기술 자문: OEM 모듈과 서드파티 모듈

트랜시버를 구매할 때 고객들이 자주 묻는 질문이 있습니다. *"범용 또는 프로그래밍된 서드파티 트랜시버를 사용해도 됩니까?"*

### NVIDIA LinkX 정품을 권장하는 이유:
1. **펌웨어 호환성**: NVIDIA ConnectX NIC와 Quantum 스위치는 특화된 운영 체제(MLNX-OS 또는 Onyx 등)를 실행합니다. 시스템 업데이트로 인해 범용 코딩 모듈이 차단되거나 플래그가 지정되어 포트 상태가 down이 되는 경우가 자주 발생합니다.
2. **진단 신뢰성(DDM/DOM)**: 정품 모듈은 정확한 온도, 전압, TX 전력, RX 전력 값을 시스템 컨트롤러(iDRAC, HPE iLO 또는 MLNX-OS)에 직접 보고합니다. 올바른 측정값은 오탐성 온도 경고를 방지합니다.
3. **고급 기능 지원**: LinkX 모듈은 Forward Error Correction(FEC) 설정과 같은 핵심 기능을 별도 작업 없이 바로 지원하도록 인증되어, 처리량이 높은 데이터베이스 워크로드에서 패킷 손실을 방지합니다.

---

{{< alert >}}
제품 견적이 필요하신가요? [문의해 주십시오](/ko/contact/)
{{< /alert >}}
