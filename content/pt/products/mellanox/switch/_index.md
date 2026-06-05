---
title: "Switches Ethernet e InfiniBand NVIDIA Mellanox"
description: "Switches de rede corporativos de alta densidade. Escolha switches Mellanox EDR (100G), HDR (200G) e NDR (400G), projetados para computação de alto desempenho e clusters de IA."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Switches Ethernet e InfiniBand NVIDIA Mellanox — EDR, HDR e NDR

Os switches InfiniBand NVIDIA Mellanox formam a espinha dorsal de clusters modernos de treinamento de IA e ambientes de computação de alto desempenho (HPC). Com alta densidade de portas, baixíssima latência de comutação e gerenciamento avançado de congestionamento, esses switches permitem escalonar sistemas multi-nós de maneira simplificada.

---

## Catálogo de switches

Veja abaixo a lista de switches gerenciados e não gerenciados de 1U para montagem em rack disponíveis em nosso estoque.

![Mellanox HDR InfiniBand Switch](/images/products/mellanox/official/switch/switch-hdr-40port-official.png)
*Switch InfiniBand NVIDIA Mellanox Quantum HDR de 40 portas*

| Part Number | Geração do Chipset | Gerenciável | Configuração de Portas | Velocidade da Porta | Formato | Fluxo de Ar | Fonte de Alimentação |
|-------------|--------------------|---------|---------------------|------------|-------------|---------|--------------|
| **MSB7800-ES2F** | Switch-IB 2 (EDR) | Sim (x86) | 36x QSFP28 | 100Gb/s | 1U Padrão | Porta para Fonte (P2C) | Fonte CA Dupla |
| **MSB7890-ES2R** | Switch-IB 2 (EDR) | Não | 36x QSFP28 | 100Gb/s | 1U Padrão | Fonte para Porta (C2P) | Fonte CA Dupla |
| **MQM8700-HS2F** | Quantum (HDR) | Sim (x86) | 40x QSFP56 | 200Gb/s | 1U Padrão | Porta para Fonte (P2C) | Fonte CA Dupla |
| **MQM8790-HS2F** | Quantum (HDR) | Não | 40x QSFP56 | 200Gb/s | 1U Padrão | Porta para Fonte (P2C) | Fonte CA Dupla |
| **MQM9700-NS2F** | Quantum 2 (NDR) | Sim | 32x OSFP (64x portas NDR) | 400Gb/s (OSFP) | 1U Padrão | Porta para Fonte (P2C) | Fonte CA Dupla |
| **MQM9790-NS2F** | Quantum 2 (NDR) | Não | 32x OSFP (64x portas NDR) | 400Gb/s (OSFP) | 1U Padrão | Porta para Fonte (P2C) | Fonte CA Dupla |

---

## Comparação de gerações InfiniBand

| Geração | Chipset | Velocidade Máxima da Porta | Capacidade do Switch | Taxa de Sinalização / Modulação | Latência |
|------------|---------|----------------|-----------------|-----------------------------|---------|
| **EDR** | Switch-IB 2 | 100 Gb/s | 7.2 Tb/s | 25 Gb/s NRZ | 90 ns |
| **HDR** | Quantum | 200 Gb/s | 16.0 Tb/s | 50 Gb/s PAM4 | 130 ns |
| **NDR** | Quantum 2 | 400 Gb/s (preparado para 800G) | 51.2 Tb/s | 100 Gb/s PAM4 | 205 ns |

---

## Guia de topologia de rede InfiniBand

A montagem de clusters escalonáveis para treinamento de inteligência artificial ou simulação física exige topologias de rede específicas:

![Topologia InfiniBand Fat-Tree NVIDIA Mellanox](/images/products/mellanox/ai-generated/switch_topology@2x.png)

### 1. Topologia Fat-Tree (CLOS não bloqueante)
Esta é a arquitetura padrão para redes InfiniBand. Ela organiza os switches em camadas hierárquicas (Leaf e Spine) para disponibilizar múltiplos caminhos paralelos.
- **Não bloqueante (proporção 1:1)**: Cada nó consegue se comunicar simultaneamente na velocidade física total da porta. Exige que a largura de banda de subida (uplink) para a camada spine seja idêntica à de descida (downlink) para os nós.
- **Sobreassinada (Over-subscribed, ex: 2:1)**: Reduz o custo em switches ao diminuir os links com a camada spine, sendo adequada para cargas de trabalho onde a comunicação computacional ocorre de forma mais localizada.

### 2. Redes de IA otimizadas por trilho (Rail-Optimized)
Em nós de servidores multi-GPU (como o NVIDIA HGX H100 com 8 GPUs), cada GPU possui uma placa ConnectX dedicada. A arquitetura de otimização por trilho (rail-optimization) interliga todas as placas "GPU 1" de todos os servidores a um switch dedicado "Rail Switch 1", todas as placas "GPU 2" ao "Rail Switch 2", e assim por diante. Essa topologia mapeia o padrão de comunicação em anel usado por bibliotecas de aprendizagem profunda (como NCCL) diretamente nos switches físicos, minimizando a latência.

---

## Switches gerenciados vs não gerenciados e Gerenciador de Sub-rede (Subnet Manager)

Diferentemente de redes Ethernet que operam no modo plug-and-play por meio de ARP, uma rede InfiniBand **não transmite tráfego sem um Gerenciador de Sub-rede (Subnet Manager - SM) ativo**. O SM mapeia a topologia da rede, atribui identificadores locais (LIDs) e calcula as rotas de envio.
- **Switches gerenciados**: Contam com CPU interna executando MLNX-OS/Onyx que hospeda um Subnet Manager integrado. Ideal para pequenos clusters isolados (até cerca de 36 nós).
- **Switches não gerenciados**: Oferecem latência física ainda menor por não possuírem CPU onboard. Exigem um SM externo em execução em um servidor host (por meio do OpenSM) ou em outro switch gerenciado presente no mesmo barramento (fabric).

---

{{< alert >}}
Precisa de uma cotação do produto? Por favor, [entre em contato conosco](/pt/contact/).
{{< /alert >}}
