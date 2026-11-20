---
title: "NVIDIA Mellanox InfiniBand 및 이더넷 스위치"
description: "고밀도 엔터프라이즈 네트워크 스위치. Mellanox EDR(100G), HDR(200G), NDR(400G) 스위치를 선택하십시오. 고성능 컴퓨팅과 AI 클러스터를 위해 제작되었습니다."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox InfiniBand 및 이더넷 스위치 — EDR, HDR, NDR

NVIDIA Mellanox InfiniBand 스위치는 현대 AI 학습 클러스터와 고성능 컴퓨팅(HPC) 환경의 백본입니다. 높은 포트 밀도, 낮은 스위치 지연 시간, 고급 혼잡 관리 기능을 갖추고 있어 멀티 노드 시스템을 매끄럽게 확장할 수 있습니다.

---

## 스위치 제품 카탈로그

다음은 당사가 보유한 비관리형 및 관리형 1U 랙 마운트 스위치 목록입니다.

![Mellanox HDR InfiniBand 스위치](/images/products/mellanox/official/switch/switch-hdr-40port-official.png)
*NVIDIA Mellanox Quantum HDR 40포트 InfiniBand 스위치*

| 부품 번호 | 칩셋 세대 | 관리 여부 | 포트 구성 | 포트 속도 | 폼 팩터 | 공기 흐름 | 전원 공급 장치 |
|-------------|--------------------|---------|---------------------|------------|-------------|---------|--------------|
| **MSB7800-ES2F** | Switch-IB 2 (EDR) | 예 (x86) | 36x QSFP28 | 100Gb/s | 1U 표준 | Port-to-Power (P2C) | 듀얼 AC PSU |
| **MSB7890-ES2R** | Switch-IB 2 (EDR) | 아니요 | 36x QSFP28 | 100Gb/s | 1U 표준 | Power-to-Port (C2P) | 듀얼 AC PSU |
| **MQM8700-HS2F** | Quantum (HDR) | 예 (x86) | 40x QSFP56 | 200Gb/s | 1U 표준 | Port-to-Power (P2C) | 듀얼 AC PSU |
| **MQM8790-HS2F** | Quantum (HDR) | 아니요 | 40x QSFP56 | 200Gb/s | 1U 표준 | Port-to-Power (P2C) | 듀얼 AC PSU |
| **MQM9700-NS2F** | Quantum 2 (NDR) | 예 | 32x OSFP (64x NDR 포트) | 400Gb/s (OSFP) | 1U 표준 | Port-to-Power (P2C) | 듀얼 AC PSU |
| **MQM9790-NS2F** | Quantum 2 (NDR) | 아니요 | 32x OSFP (64x NDR 포트) | 400Gb/s (OSFP) | 1U 표준 | Port-to-Power (P2C) | 듀얼 AC PSU |

---

## InfiniBand 세대 비교

| 세대 | 칩셋 | 최대 포트 속도 | 스위치 용량 | 신호 전송률 / 변조 방식 | 지연 시간 |
|------------|---------|----------------|-----------------|-----------------------------|---------|
| **EDR** | Switch-IB 2 | 100 Gb/s | 7.2 Tb/s | 25 Gb/s NRZ | 90 ns |
| **HDR** | Quantum | 200 Gb/s | 16.0 Tb/s | 50 Gb/s PAM4 | 130 ns |
| **NDR** | Quantum 2 | 400 Gb/s (800G 지원 예정) | 51.2 Tb/s | 100 Gb/s PAM4 | 205 ns |

---

## InfiniBand 네트워크 토폴로지 가이드

AI 학습이나 물리 시뮬레이션을 위한 스케일 아웃 클러스터를 구축하려면 특화된 토폴로지가 필요합니다.

![NVIDIA Mellanox Fat-Tree InfiniBand 토폴로지](/images/products/mellanox/ai-generated/switch_topology@2x.png)

### 1. Fat-Tree (논블로킹 CLOS) 토폴로지
InfiniBand 네트워크의 표준 아키텍처입니다. 스위치를 계층적 티어(Leaf 및 Spine)로 구성하여 여러 병렬 경로를 제공합니다.
- **논블로킹 (1:1 서브스크립션)**: 모든 노드가 동시에 전체 와이어 스피드로 통신할 수 있습니다. 노드로 향하는 다운링크 대역폭과 스파인으로 향하는 업링크 대역폭이 같아야 합니다.
- **오버 서브스크립션 (예: 2:1)**: 스파인 링크 수를 줄여 스위치 비용을 낮추며, 국지적인 컴퓨팅 통신을 하는 워크로드에 적합합니다.

### 2. 레일 최적화 AI 네트워크
멀티 GPU 노드(예: GPU 8개를 탑재한 NVIDIA HGX H100)에서는 각 GPU에 전용 ConnectX NIC가 있습니다. 레일 최적화는 모든 서버의 "GPU 1" 어댑터를 전용 "Rail Switch 1"에, 모든 "GPU 2" 어댑터를 "Rail Switch 2"에 연결하는 방식으로 이어집니다. 이렇게 하면 딥러닝 라이브러리(NCCL)의 링 통신 패턴이 물리 스위치에 직접 매핑되어 지연 시간이 최소화됩니다.

---

## 관리형 스위치와 비관리형 스위치, 그리고 서브넷 매니저 (SM)

ARP를 통해 플러그 앤 플레이로 동작하는 이더넷 네트워크와 달리, InfiniBand 네트워크는 **활성 서브넷 매니저(SM) 없이는 트래픽을 전달할 수 없습니다**. SM은 토폴로지를 탐색하고 로컬 식별자(LID)를 할당하며 라우팅 경로를 계산합니다.
- **관리형 스위치**: MLNX-OS/Onyx를 실행하는 내부 CPU가 임베디드 서브넷 매니저를 호스팅합니다. 독립형 소규모 클러스터(약 36노드까지)에 이상적입니다.
- **비관리형 스위치**: 지연 시간이 매우 낮지만 온보드 CPU가 없습니다. 호스트 서버(OpenSM 경유) 또는 패브릭 내의 별도 관리형 스위치에서 실행되는 외부 SM이 필요합니다.

---

{{< alert >}}
제품 견적이 필요하신가요? [문의해 주십시오](/ko/contact/)
{{< /alert >}}
