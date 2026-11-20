---
title: "NVIDIA BlueField 데이터 처리 장치 (DPU)"
description: "NVIDIA BlueField DPU 솔루션을 살펴보십시오. ARM 기반 프로그래머블 SmartNIC으로 네트워크, 스토리지, 보안 인프라 서비스를 오프로드, 가속, 격리합니다."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA BlueField 데이터 처리 장치 (DPU)

NVIDIA® BlueField® 데이터 처리 장치(DPU)는 데이터센터 아키텍처의 혁신적인 변화를 대표합니다. 업계 선도적인 ConnectX 네트워크 어댑터를 프로그래머블 ARM® CPU 코어 및 하드웨어 가속 엔진과 결합하여, 인프라 작업을 서버 CPU로부터 오프로드, 가속, 격리합니다.

---

## BlueField DPU 재고

당사는 클라우드 규모의 가상화, 소프트웨어 정의 스토리지, 제로 트러스트 보안을 위해 구성된 BlueField DPU를 유통합니다.

![NVIDIA BlueField DPU](/images/products/mellanox/official/dpu/bluefield2-dpu-official.jpg)
*NVIDIA BlueField 프로그래머블 인프라 어댑터*

| 부품 번호 | 마케팅 명칭 | 핵심 네트워킹 | ARM CPU 코어 | 메모리 | 인터페이스 | 프로토콜 | 폼 팩터 |
|-------------|----------------|-----------------|---------------|--------|-----------|----------|-------------|
| **900-9D3B6-00CV-AA0** | BlueField-2 DPU | 듀얼 포트 100GbE / EDR IB | 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe |
| **900-9D3B6-00CC-EA0** | BlueField-2 DPU | 듀얼 포트 100GbE / EDR IB | 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe (암호화 활성화) |
| **900-9D3B4-00CC-EA0** | BlueField-2 DPU | 싱글 포트 100GbE / EDR IB| 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe (암호화 활성화) |

---

## 주요 DPU 기술

### 1. 인프라 오프로드 (SmartNIC+)
하이퍼바이저 네트워크 스위칭(OVS), 가상화 터널(VXLAN, NVGRE), 네트워크 주소 변환(NAT)을 관리하는 데 귀중한 호스트 CPU 사이클을 사용하는 대신, DPU가 **NVIDIA ASAP²(Accelerated Switch and Packet Processing)** 기술을 사용하여 이러한 작업을 하드웨어에서 와이어 스피드로 직접 처리합니다.

### 2. 소프트웨어 정의 스토리지 가속
**NVMe SNAP™(Software-defined Network Accelerated Processing)**을 사용하면 BlueField DPU가 원격 네트워크 스토리지(RoCEv2 또는 TCP 경유)를 호스트 운영 체제에 로컬 NVMe 물리 드라이브로 제공할 수 있습니다. 에뮬레이션, 암호화, 압축이 모두 DPU에서 처리되므로 가상화 스토리지 병목 현상이 해소됩니다.

### 3. 제로 트러스트 보안 및 격리
DPU는 내장 ARM 코어에서 호스트 서버와 완전히 격리된 독립적인 Linux 운영 체제(일반적으로 Ubuntu)를 실행합니다. 호스트 OS가 침해되더라도 DPU에서 실행되는 보안 에이전트, 에이전트리스 방화벽, 네트워크 암호화(IPsec, TLS)는 변조되지 않은 채 계속 동작합니다.

### 4. NVIDIA DOCA 소프트웨어 프레임워크
BlueField DPU는 네트워킹, 보안, 스토리지, 텔레메트리를 위한 가속 애플리케이션 개발용 업계 표준 API를 제공하는 **NVIDIA DOCA™** 소프트웨어 프레임워크로 프로그래밍합니다.

---

## 주요 활용 사례

- **차세대 클라우드 제공업체**: 인프라 관리를 DPU에 완전히 격리하는 베어메탈 호스팅을 구현합니다.
- **엔터프라이즈 하이퍼컨버지드 인프라(HCI)**: 스토리지와 네트워크 오버레이(VMware NSX / Proxmox OVS)를 오프로드하여 VM 밀도를 극대화합니다.
- **고보안 환경**: 네트워크 보안 모니터링(IDS/IPS)과 암호화 워크로드를 네트워크 경계에서 직접 실행합니다.

---

{{< alert >}}
제품 견적이 필요하신가요? [문의해 주십시오](/ko/contact/)
{{< /alert >}}
