---
title: "NVIDIA Mellanox ConnectX 네트워크 인터페이스 카드 (NIC)"
description: "NVIDIA Mellanox ConnectX-4 Lx, ConnectX-5, ConnectX-6 Dx/Lx, ConnectX-7 NIC 어댑터를 비교해 보십시오. PCIe Gen3/4/5용 10G, 25G, 50G, 100G, 200G, 400G 옵션을 제공합니다."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Mellanox / NVIDIA ConnectX 네트워크 카드 — 10G에서 400G까지

NVIDIA Mellanox ConnectX 어댑터는 엔터프라이즈 서버와 AI 클러스터에 업계 최고 수준의 대역폭과 지연 시간을 제공합니다. 다음은 Yopitek이 유통하는 전체 모델 카탈로그이며 속도 등급별로 정리되어 있습니다.

---

## 10GbE / 25GbE 네트워크 카드

일반 엔터프라이즈 서버, 가상화(VMware ESXi), 고성능 NAS 스토리지에 적합합니다.

### 10G 모델

| 부품 번호 | 세대 / 칩셋 | 포트 | 속도 | PCIe 슬롯 | 커넥터 | 프로토콜 | 브래킷 |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX4121A-XCAT** | ConnectX-4 Lx | 듀얼 | 10GbE | PCIe 3.0 x8 | SFP28 | 이더넷 | Tall |

### 25G 모델

![NVIDIA ConnectX-4 Lx 25G](/images/products/mellanox/official/nic/connectx4-lx-25g-official.jpg)
*NVIDIA ConnectX-4 Lx 25GbE 듀얼 포트 어댑터*

![NVIDIA ConnectX-5 25G](/images/products/mellanox/official/nic/connectx5-25g-official.jpg)
*NVIDIA ConnectX-5 25GbE 듀얼 포트 어댑터*

| 부품 번호 | 세대 / 칩셋 | 포트 | 속도 | PCIe 슬롯 | 커넥터 | 프로토콜 | 브래킷 / 폼 팩터 | 특수 기능 |
|-------------|---------------|-------|-------|-----------|-----------|----------|-----------------------|------------------|
| **MCX4121A-ACAT** | ConnectX-4 Lx | 듀얼 | 25GbE | PCIe 3.0 x8 | SFP28 | 이더넷 | Tall 브래킷 | 표준 PCIe 카드 |
| **MCX4121A-ACUT** | ConnectX-4 Lx | 듀얼 | 25GbE | PCIe 3.0 x8 | SFP28 | 이더넷 | Tall 브래킷 | UEFI 활성화 |
| **MCX512A-ACAT** | ConnectX-5 EN | 듀얼 | 25GbE | PCIe 3.0 x8 | SFP28 | 이더넷 | Tall 브래킷 | 강화된 RoCEv2 |
| **MCX512A-ACUT** | ConnectX-5 EN | 듀얼 | 25GbE | PCIe 3.0 x8 | SFP28 | 이더넷 | Tall 브래킷 | UEFI (x86/ARM) |
| **MCX631102AN-ADAT**| ConnectX-6 Lx | 듀얼 | 25GbE | PCIe 4.0 x8 | SFP28 | 이더넷 | Tall 브래킷 | Secure Boot, 암호화 없음|
| **MCX623432AS-ADAB**| ConnectX-6 Lx | 듀얼 | 25GbE | PCIe 4.0 x8 | SFP28 | 이더넷 | OCP 3.0 Thumbscrew | Secure Boot, OCP 3.0 |

---

## 50GbE / 100GbE 네트워크 카드

고속 NVMe over Fabrics(NVMe-oF) 스토리지, 하이퍼컨버지드 인프라(HCI), 데이터베이스 서버에 적합합니다.

![NVIDIA ConnectX-5 100G](/images/products/mellanox/official/nic/connectx5-100g-official.jpg)
*NVIDIA ConnectX-5 100GbE 어댑터*

![NVIDIA ConnectX-6 Dx 100G](/images/products/mellanox/official/nic/connectx6-dx-100g-official.png)
*NVIDIA ConnectX-6 Dx 100GbE 듀얼 포트 어댑터*

### 50G 모델

| 부품 번호 | 세대 / 칩셋 | 포트 | 속도 | PCIe 슬롯 | 커넥터 | 프로토콜 | 브래킷 |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX515A-GCAT** | ConnectX-5 EN | 싱글 | 50GbE | PCIe 3.0 x16 | QSFP28 | 이더넷 | Tall |

### 100G 모델

| 부품 번호 | 세대 / 칩셋 | 포트 | 속도 | PCIe 슬롯 | 커넥터 | 프로토콜 | 폼 팩터 | 특수 기능 |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX515A-CCAT** | ConnectX-5 EN | 싱글 | 100GbE | PCIe 3.0 x16 | QSFP28 | 이더넷 | Tall PCIe | 표준 100G NIC |
| **MCX555A-ECAT** | ConnectX-5 VPI | 싱글 | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | Tall PCIe | EDR IB 및 100GbE |
| **MCX516A-CCAT** | ConnectX-5 EN | 듀얼 | 100GbE | PCIe 3.0 x16 | QSFP28 | 이더넷 | Tall PCIe | 듀얼 포트 100G |
| **MCX516A-CDAT** | ConnectX-5 Ex | 듀얼 | 100GbE | PCIe 4.0 x16 | QSFP28 | 이더넷 | Tall PCIe | PCIe 4.0 인터페이스|
| **MCX556A-ECAT** | ConnectX-5 VPI | 듀얼 | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | Tall PCIe | 듀얼 포트 EDR IB |
| **MCX556A-EDAT** | ConnectX-5 Ex VPI| 듀얼 | 100G | PCIe 4.0 x16 | QSFP28 | VPI (IB/ETH) | Tall PCIe | PCIe 4.0 듀얼 EDR |
| **MCX653105A-ECAT**| ConnectX-6 VPI | 싱글 | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | Tall PCIe | HDR100 IB 및 100GbE|
| **MCX653106A-ECAT**| ConnectX-6 VPI | 듀얼 | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | Tall PCIe | HDR100 IB 및 100GbE|
| **MCX623106AN-CDAT**| ConnectX-6 Dx | 듀얼 | 100GbE | PCIe 4.0 x16 | QSFP56 | 이더넷 | Tall PCIe | 100G 듀얼 SFP56/QSFP56|
| **MCX623436AN-CDAB**| ConnectX-6 Dx | 듀얼 | 100GbE | PCIe 4.0 x16 | QSFP56 | 이더넷 | OCP 3.0 Thumbscrew | OCP 폼 팩터 |

---

## 200GbE / 400GbE 네트워크 카드

AI GPU 서버 노드(예: NVIDIA HGX/DGX 아키텍처), 고빈도 매매(HFT), HPC 네트워크 백본을 위해 설계된 플래그십 어댑터입니다.

![NVIDIA ConnectX-7 400G](/images/products/mellanox/official/nic/connectx7-400g-official.png)
*NVIDIA ConnectX-7 400G OSFP 어댑터*

### 200G 모델

| 부품 번호 | 세대 / 칩셋 | 포트 | 속도 | PCIe 슬롯 | 커넥터 | 프로토콜 | 폼 팩터 | 특수 기능 |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX653105A-HDAT**| ConnectX-6 VPI | 싱글 | 200G | PCIe 4.0 x16 | QSFP56 | VPI (IB/ETH) | Tall PCIe | HDR IB 및 200GbE |
| **MCX653106A-HDAT**| ConnectX-6 VPI | 듀얼 | 200G | PCIe 4.0 x16 | QSFP56 | VPI (IB/ETH) | Tall PCIe | 듀얼 포트 HDR/200G|
| **MCX623105A-VDAT**| ConnectX-6 Dx | 싱글 | 200GbE | PCIe 4.0 x16 | QSFP56 | 이더넷 | Tall PCIe | 싱글 포트 200G |
| **MCX75310AAS-HEAT**| ConnectX-7 IB | 싱글 | 200G | PCIe 5.0 x16 | OSFP | InfiniBand | Tall PCIe | NDR200, Socket Direct|
| **MCX755106AS-HEAT**| ConnectX-7 VPI | 듀얼 | 200G | PCIe 5.0 x16 | QSFP112 | VPI (IB/ETH) | Tall PCIe | 1번 포트 IB, 2번 포트 VPI|
| **MCX753436MS-HEAB**| ConnectX-7 VPI | 듀얼 | 200G | PCIe 5.0 x16 | QSFP112 | VPI (IB/ETH) | OCP 3.0 Thumbscrew | OCP Multi-Host / Socket Direct|

### 400G 모델

| 부품 번호 | 세대 / 칩셋 | 포트 | 속도 | PCIe 슬롯 | 커넥터 | 프로토콜 | 폼 팩터 | 특수 기능 |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX75310AAS-NEAT**| ConnectX-7 IB | 싱글 | 400Gb/s| PCIe 5.0 x16 | OSFP | InfiniBand | Tall PCIe | NDR InfiniBand |
| **MCX75510AAS-NEAT**| ConnectX-7 IB | 싱글 | 400Gb/s| PCIe 5.0 x16 | OSFP | InfiniBand | Tall PCIe | NDR OSFP, Socket Direct 지원 예정|

---

## 기술 선택 가이드

ConnectX 어댑터 카드를 선택할 때는 다음 사항에 특히 유의하십시오.

### 1. 프로토콜 모드 (VPI와 EN)
- **EN 어댑터**는 이더넷 네트워크만 지원합니다.
- **VPI(Virtual Protocol Interconnect) 어댑터**는 펌웨어를 통해 InfiniBand 또는 이더넷 카드로 동작하도록 구성할 수 있어 최대의 배포 유연성을 제공합니다.

### 2. PCIe 대역폭 요구 사항
호스트 서버의 PCIe 버전과 슬롯 폭이 카드를 최고 속도로 지원할 수 있는지 확인하십시오.
- 듀얼 포트 100G NIC는 두 포트를 동시에 최대 용량으로 동작시키려면 PCIe 4.0 x16이 필요합니다.
- PCIe 4.0 카드를 PCIe 3.0 슬롯에 연결하는 것은 하위 호환되지만, 처리량은 PCIe 3.0 한계(x8은 약 64Gbps, x16은 약 128Gbps)로 제한됩니다.

### 3. OCP 3.0과 표준 PCIe 폼 팩터
`-ADAB`, `-CDAB`, `-HEAB` 등의 접미사가 붙은 모델은 **OCP NIC 3.0** 폼 팩터를 사용합니다. 이 카드는 전용 서버 베이(Supermicro, Dell, HPE, Lenovo의 최신 세대에서 흔함)에 삽입하는 방식이며 표준 PCIe 슬롯에는 장착할 수 없습니다.

---

{{< alert >}}
제품 견적이 필요하신가요? [문의해 주십시오](/ko/contact/)
{{< /alert >}}
