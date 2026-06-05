---
title: "Unidades de Processamento de Dados (DPU) NVIDIA BlueField"
description: "Explore as soluções de DPU NVIDIA BlueField. Descarregue, acelere e isole serviços de rede, armazenamento e segurança com SmartNICs programáveis baseadas em ARM."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Unidades de Processamento de Dados (DPU) NVIDIA BlueField

As Unidades de Processamento de Dados (DPUs) NVIDIA® BlueField® introduziram uma nova arquitetura para data centers. Ao integrar as placas de rede ConnectX com núcleos de CPU ARM® programáveis e mecanismos de aceleração por hardware, as DPUs descarregam, aceleram e isolam as tarefas de infraestrutura da CPU do servidor.

---

## Nosso estoque de DPUs BlueField

Distribuímos DPUs BlueField configuradas para virtualização em escala de nuvem, armazenamento definido por software e segurança zero-trust.

![NVIDIA BlueField DPU](/images/products/mellanox/official/dpu/bluefield2-dpu-official.jpg)
*Adaptador de infraestrutura programável NVIDIA BlueField*

| Part Number | Nome Comercial | Rede Integrada | Núcleos de CPU ARM | Memória | Interface | Protocolo | Formato |
|-------------|----------------|-----------------|---------------|--------|-----------|----------|-------------|
| **900-9D3B6-00CV-AA0** | BlueField-2 DPU | Dupla 100GbE / EDR IB | 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | PCIe FHHL |
| **900-9D3B6-00CC-EA0** | BlueField-2 DPU | Dupla 100GbE / EDR IB | 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | PCIe FHHL (Criptografia Ativa) |
| **900-9D3B4-00CC-EA0** | BlueField-2 DPU | Única 100GbE / EDR IB | 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | PCIe FHHL (Criptografia Ativa) |

---

## Principais tecnologias da DPU

### 1. Descarregamento de infraestrutura (SmartNIC+)
Em vezes de consumir ciclos da CPU do servidor para gerenciar o chaveamento de rede do hipervisor (OVS), túneis de virtualização (VXLAN, NVGRE) ou tradução de endereços de rede (NAT), a DPU processa essas tarefas na velocidade física do cabo direto no hardware por meio da tecnologia **NVIDIA ASAP² (Accelerated Switch and Packet Processing)**.

### 2. Aceleração de armazenamento definido por software
Com o **NVMe SNAP™ (Software-defined Network Accelerated Processing)**, a DPU BlueField pode disponibilizar o armazenamento de rede remoto (via RoCEv2 ou TCP) como se fosse um disco físico NVMe local para o sistema operacional host. A emulação, criptografia e compressão ocorrem inteiramente na DPU, eliminando gargalos de armazenamento na virtualização.

### 3. Segurança e isolamento Zero-Trust
A DPU executa seu próprio sistema operacional Linux independente (geralmente Ubuntu) nos núcleos ARM integrados, totalmente isolado do servidor principal. Mesmo se o sistema operacional host for comprometido, os agentes de segurança, firewalls independentes de agente e a criptografia de rede (IPsec, TLS) executados na DPU continuam operando sem qualquer alteração ou comprometimento.

### 4. Framework de software NVIDIA DOCA
As DPUs BlueField são programadas por meio do framework **NVIDIA DOCA™**, que oferece APIs padronizadas para o desenvolvimento de aplicações aceleradas em rede, segurança, armazenamento e telemetria.

---

## Casos de uso comuns

- **Provedores de nuvem de última geração**: Viabilizam hospedagem bare-metal onde todo o gerenciamento da infraestrutura fica isolado na DPU.
- **Infraestrutura hiperconvergente corporativa (HCI)**: Descarregamento de armazenamento e camadas de rede (VMware NSX / Proxmox OVS) para maximizar a densidade de máquinas virtuais (VMs).
- **Ambientes de alta segurança**: Execução de monitoramento de segurança de rede (IDS/IPS) e processamento de criptografia diretamente na borda da rede.

---

{{< alert >}}
Precisa de uma cotação do produto? Por favor, [entre em contato conosco](/pt/contact/).
{{< /alert >}}
