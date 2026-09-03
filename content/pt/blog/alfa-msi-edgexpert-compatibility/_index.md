---
title: "Carta Técnica: Suporte do Adaptador de Rede Wireless ALFA para o MSI EdgeXpert (GB10)"
date: 2026-09-03
draft: false
slug: "alfa-msi-edgexpert-compatibility"
tags:
  - "ALFA"
  - "MSI"
  - "EdgeXpert"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "Guia de Hardware"
description: "MSI EdgeXpert e NVIDIA DGX Spark compartilham GB10 e DGX OS, compatibilidade ALFA, MediaTek uso in-kernel, Realtek out-of-tree, USB Type-C 20Gbps, AXML precisa adaptador."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumo do Problema

Pergunta do cliente: “O adaptador de rede sem fio USB da série ALFA pode ser utilizado no supercomputador MSI EdgeXpert (NVIDIA GB10 Grace Blackwell) AI?”

Conclusão resumida: O MSI EdgeXpert e o NVIDIA DGX Spark compartilham a mesma plataforma de hardware GB10 e o ambiente de software DGX OS, garantindo total compatibilidade com os adaptadores de rede ALFA. Os modelos de chip MediaTek (AWUS036ACM / ACHM / AXML / AXM) utilizam drivers in-kernel, prontos para uso direto da embalagem; os modelos de chip Realtek (AWUS036ACH / ACS / EACS / AX / AXER) requerem a compilação de drivers out-of-tree no ARM64. Atenção: Os 4 ports USB do EdgeXpert são todos do tipo USB Type-C (20Gbps), e os adaptadores de rede ALFA (exceto o AXML) precisam de um adaptador USB-C to USB-A.

Critérios de avaliação: Os 9 adaptadores de rede USB atuais da ALFA (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Análise da Arquitetura de Especificações de Hardware de Objetivo

### 2.1 Especificações de Hardware do MSI EdgeXpert

| Item | Especificação |
|---|---|
| Nome do Produto | MSI EdgeXpert (Modelos: EdgeXpert-MS-C931 / 59STW e outros) |
| Chip de Núcleo | NVIDIA GB10 Grace Blackwell Superchip (Plataforma DGX Spark) |
| CPU | 20-núcleo Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | NVIDIA Blackwell, 6144 núcleos CUDA, Cincoª Geração Tensor Core, Quartoª Geração RT Core |
| Desempenho de IA | Até 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| Memória do Sistema | 128GB LPDDR5x Memória Unificada (256-bit, 273 GB/s) |
| Armazenamento | 1TB ou 4TB SSD NVMe M.2 (加密, PCIe Gen5) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (até 20Gbps) |
| Saída de Vídeo | 1× HDMI 2.1a (4× DP1.4a via USB-C Alt Mode) |
| Rede com Fio | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (QSFP 200GbE, interconexão de sistemas) |
| Rede sem Fio | Wi-Fi 7 + Bluetooth 5.4 |
| Sistema Operacional | NVIDIA DGX OS (baseado em Ubuntu Linux, kernel 6.x) |
| Arquitetura | aarch64 (ARM64) |
| Tamanho | 151 × 151 × 52 mm (aproximadamente 5.95" × 5.95" × 2.05") |
| Peso | Aproximadamente 1.2 kg (2.65 lbs) |
| Alimentação | Fonte de alimentação USB-C de 240W |
| Versão | Versão Consumidor / Versão Industrial (EdgeXpert-MS-C931, versão de temperatura ampla / industrial) |

### 2.2 Ambiente de Software: NVIDIA DGX OS

O MSI EdgeXpert é pré-instalado com o NVIDIA DGX OS, idêntico ao DGX Spark / ASUS GX10:

| Item | Descrição |
|---|---|
| Base | Ubuntu Linux (personalizado pela NVIDIA) |
| Kernel | Linux 6.x |
| Arquitetura | aarch64 (ARM64) |
| Software Pré-instalado | NVIDIA AI Software Stack (CUDA, cuDNN, TensorRT, PyTorch, Jupyter e outros) |
| Gestão de Pacotes | apt |

### 2.3 Diferenças com o DGX Spark

O MSI EdgeXpert é uma versão OEM da plataforma DGX Spark, com hardware e software completamente idênticos:

| Item | MSI EdgeXpert | NVIDIA DGX Spark |
|---|---|---|
| Design de Estrutura | Gabinete personalizado pela MSI, opção industrial | Gabinete de referência da NVIDIA |
| Opções de Armazenamento | 1TB / 4TB | Até 4TB |
| Mercado Alvo | IA de borda / IA industrial / Desenvolvimento de desktop | Desenvolvimento de IA de desktop |
| Acessórios | Acessórios originais da MSI | Acessórios originais da NVIDIA |

Impacto na compatibilidade com o ALFA: sem impacto. Controladores USB, versão do kernel e framework de drivers são completamente idênticos ao DGX Spark.

### 2.4 Necessidade de Adaptador USB Type-C

Os 4 conectores USB do EdgeXpert são Type-C, enquanto todos os cartões de rede da ALFA (exceto o AXML, que é USB-C) são Type-A, exigindo um adaptador. Recomenda-se a escolha de um adaptador que suporte USB 3.2 Gen 2×2 (20Gbps).

## 3. Análise das Especificações e Chipsets da Placa de Rede ALFA

Até setembro de 2026, a linha de produtos de placas de rede USB sem fio da ALFA Network é a seguinte (baseada em 9 modelos):

| Modelo | Nível Wi-Fi | Chipset | Interface | Status do Driver Linux |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel (mt7921u) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel (mt7921u) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 / out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Igual ao acima |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree (8812au) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel (mt76x2u)⭐ Recomendado |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree (8812au coberto) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree (8821cu) |

## 4. Modelos Aplicáveis e Chipsets

### 4.1 Classificação de Recomendação

| Nível de Recomendação | Modelo (Chipset) | Descrição |
|---|---|---|
| ⭐ Recomendação Forte | AWUS036ACM (MT7612U) | Driver in-kernel, pronto para usar, AC1200 dual-band, suporta AP / Monitor / Injection |
| ✅ Recomendado | AWUS036ACHM (MT7610U) | Driver in-kernel, baixo consumo de energia, AC433 dual-band |
| ✅ Recomendado (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | Driver in-kernel, Wi-Fi 6E, AXML com conector USB-C direto |
| ⚠️ Disponível mas requer compilação | AWUS036ACH (RTL8812AU) | Requer compilação do morrownr/8812au (ARM64), após a compilação, todas as funções estarão completas |
| ⚠️ Disponível mas requer compilação | AWUS036ACS / EACS | Requer compilação do driver out-of-tree correspondente |
| ⚠️ Disponível mas com atenção | AWUS036AX / AXER (RTL8832BU) | O rtw89 do kernel 6.x pode já suportar; não há necessidade de compilação |

### 4.2 Sugestões de Uso

| Cenário de Uso | Modelo Recomendado | Descrição |
|---|---|---|
| Internet sem fio em pontos de acesso de AI de borda | AWUS036ACM / ACHM | Driver in-kernel, estável, sem manutenção |
| Testes de penetração sem fio em ambientes industriais | AWUS036ACH ou AWUS036ACM | Ambos suportam Monitor + Injection |
| Wi-Fi 6E / Frequência de 6GHz | AWUS036AXML / AXM | Driver in-kernel MT7921AUN |
| Não há necessidade de Wi-Fi externo | — | O EdgeXpert já possui Wi-Fi 7, geralmente não há necessidade de conexão externa |

## 5. Requisitos de Ambiente

### 5.1 Requisitos de Hardware

| Item | Requisitos |
|---|---|
| Conector USB | Conector USB-C para USB-A ou cabo de transmissão (exceto AXML), recomendado suporte a USB 3.2 Gen 2×2 |
| Alimentação | Fonte de alimentação USB-C de 240W da MSI EdgeXpert, original |

### 5.2 Requisitos de Software

| Item | Requisitos |
|---|---|
| Versão do DGX OS | Qualquer versão em serviço (kernel 6.x) |
| Ferramentas de Compilação (para chipsets Realtek) | build-essential, git, bc, dkms |
| Ferramentas de Gestão de Rede | iw, network-manager (instalado por padrão no DGX OS) |

## 6. Determinação de Compatibilidade

### Matriz de Compatibilidade entre Modelos Atuais do ALFA × MSI EdgeXpert（GB10）

| Modelo | Chipset | Modo de Driver | Detecção de USB | STA Internet | Modo AP | Monitor | Dificuldade de Instalação | Avaliação Geral |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel（mt76x2u） | ✅ | ✅ | ✅ | ✅ | Sem instalação | ⭐ Melhor |
| AWUS036ACHM | MT7610U | in-kernel（mt76x0u） | ✅ | ✅ | ✅ | ⚠️ Limitado | Sem instalação | ✅ Bom |
| AWUS036AXML | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ Limitado | Sem instalação | ✅ Bom |
| AWUS036AXM | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ Limitado | Sem instalação | ✅ Bom |
| AWUS036ACH | RTL8812AU | out-of-tree（8812au） | ✅ | ✅ | ✅ | ✅ | Médio（tradução） | ⚠️ Utilizável |
| AWUS036ACS | RTL8811AU | out-of-tree（8812au） | ✅ | ✅ | ⚠️ | ❌ | Médio（tradução） | ⚠️ Utilizável |
| AWUS036EACS | RTL8811CU | out-of-tree（8821cu） | ✅ | ⚠️ | ❌ | ❌ | Médio（tradução） | ⚠️ Utilizável |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Médio-Alto | ⚠️ Utilizável |
| AWUS036AXER | RTL8832BU | Igual ao acima | ✅ | ⚠️ | ⚠️ | ❌ | Médio-Alto | ⚠️ Utilizável |

Critério de Determinação: O MSI EdgeXpert e o DGX Spark compartilham a mesma plataforma de hardware GB10 e o DGX OS (kernel 6.x, aarch64), e a determinação de compatibilidade é completamente idêntica à do DGX Spark.

## 7. Passo a Passo Detalhado de Configuração

Os passos de instalação do MSI EdgeXpert são idênticos aos do NVIDIA DGX Spark. A seguir, está uma versão resumida; para o passo a passo completo, consulte o Capítulo 7 de [ALFA Wi-Fi Card - Suporte ao NVIDIA DGX Spark](https://yupitek.com/pt-br/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modelos de Chip MediaTek (Pronto para Uso)

**Passo 1: Insira a Placa de Rede**

Utilize um adaptador USB-C to USB-A (AXML pode ser conectado diretamente) para inserir a placa de rede ALFA no porta USB-C do EdgeXpert.

**Passo 2: Confirme a Detecção do USB**

```bash
lsusb
# Saída esperada (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Passo 3: Confirme a Interface de Rede**

```bash
ip link show
# Deve aparecer wlan0 (driver carregado automaticamente no kernel)
```

**Passo 4: Conecte-se à WiFi**

```bash
nmcli dev wifi connect "SSID" password "senha"
```

### 7.2 Modelos de Chip Realtek (Necessita de Compilação)

Tomando como exemplo o AWUS036ACH (RTL8812AU):

**Passo 1: Instale as Ferramentas de Compilação**

```bash
sudo apt update && sudo apt install -y build-essential git bc dkms
```

**Passo 2: Baixe e Compile o Driver**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
# Confirme que CONFIG_PLATFORM_ARM64 = y está no Makefile
make
sudo make install
sudo modprobe 8812au
```

**Passo 3: Confirme a Interface Após a Insersão da Placa de Rede**

```bash
ip link show
```

**Passo 4: Conecte-se à WiFi**

```bash
nmcli dev wifi connect "SSID" password "senha"
```

### 7.3 Modo de Escuta (Teste de Penetração)

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

## 8. Erros Comuns e Solução

| Sintoma | Possível Causa | Solução |
|---|---|---|
| `lsusb` não vê a placa de rede ALFA | Conector USB-C defeituoso / Especificação de apenas carregamento | Troque por um conector USB 3.2 Gen 2×2 que suporte transferência de dados; tente em diferentes portas USB-C |
| Chipset MediaTek sem interface wlan | Módulo não carregado automaticamente / Firmware faltando | `sudo modprobe mt76x2u`；`sudo apt install linux-firmware`；verifique `dmesg | grep mt76` |
| Falha na compilação do driver Realtek | Configuração de cross-compilação incorreta | Confirme a compilação nativa no EdgeXpert; o Makefile não deve definir CROSS_COMPILE |
| Velocidade de WiFi lenta | Conector suporta apenas USB 2.0 | Troque por um conector USB 3.2 Gen 2×2 |
| Conflito entre Wi-Fi 7 integrado e externo | Conflito de roteamento | `sudo nmcli radio wifi off` desative o Wi-Fi integrado antes de usar o Wi-Fi externo |
| Instabilidade em ambientes industriais de alta temperatura | Refrigeração / Diferenças na versão industrial | Confirme o uso da versão industrial do EdgeXpert (MS-C931); certifique-se de que a temperatura ambiente está dentro do intervalo especificado |

## 9. Restrições Conhecidas

- Necessidade de adaptador USB Type-C: Além do AXML, todos os cartões de rede ALFA necessitam de adaptador USB-C to USB-A
- Necessidade de tradução manual para o chip Realtek: RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU não estão no mainline
- Possível conflito com Wi-Fi 7 integrado: EdgeXpert já possui Wi-Fi 7 + BT 5.4 integrados
- Modo AP precisa de configuração manual: O DGX OS é pré-configurado como ambiente de desenvolvimento
- Restrições regulatórias de 6GHz: A disponibilidade do Wi-Fi 6E depende da região regulatória
- Dependência de atualizações de drivers: Drivers out-of-tree da Realtek são mantidos pela comunidade, e após atualizações do kernel, é necessário recompilar
- Diferenças na versão industrial não afetam a compatibilidade: A versão industrial da MSI (MS-C931) possui especificações de hardware idênticas à versão de consumo, e a compatibilidade do USB WiFi é a mesma

Condições de refutação: Se a página de especificações oficiais da MSI for alterada (ajustes na especificação do porta USB, versão do kernel inferior a 6.x), ou se testes em campo revelarem que o mt76x2u / mt7921u não carregam automaticamente no DGX OS, a matriz de compatibilidade descrita no Capítulo 6 deve ser revisada novamente; se o driver morrownr deixar de manter a ramificação ARM64, a avaliação dos modelos da Realtek deve ser reavaliada.

## 10. Fontes de Referência URL

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| MSI EdgeXpert Loja Oficial (US) | Especificações da Edição Consumidor do EdgeXpert | https://us-store.msi.com/MSI-EdgeXpert-Blackwell-AI-Supercomputer | ✅ Verificado | 2026-09-03 |
| MSI EdgeXpert Loja (TW) | Especificações da Edição Consumidor do EdgeXpert (23STW) | https://tw-store.msi.com/products/edgexpert-23stw-bgb104tg4 | ✅ Verificado | 2026-09-03 |
| MSI Anúncios de Computadores Industriais | Informações de Lançamento do EdgeXpert | https://ipc.msi.com/en/news/146241 | ✅ Verificado | 2026-09-03 |
| NVIDIA DGX Spark Página Oficial | Informações sobre a Plataforma GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Driver RTL8812AU para Linux | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| ALFA Network Visão Geral de Produtos (Yupitek) | Especificações dos Produtos Atuais da ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |

Artigos Relacionados: [A Placa de Rede sem Fio ALFA Suporta o NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[A Placa de Rede sem Fio ALFA Suporta o ASUS Ascent GX10?](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[A Placa de Rede sem Fio ALFA Suporta o ALTOS BrainSphere GB10 F1?](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[A Placa de Rede sem Fio ALFA Suporta o GIGABYTE AI TOP ATOM?](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[A Placa de Rede sem Fio ALFA Suporta o NVIDIA Jetson Nano?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Declaração de Isenção de Responsabilidade: A determinação de compatibilidade deste artigo é baseada no NVIDIA DGX OS pré-instalado no MSI EdgeXpert (kernel 6.x, aarch64). O EdgeXpert e o DGX Spark compartilham a mesma plataforma de hardware, com compatibilidade completa. O driver de chip MediaTek é do Linux mainline, com alta estabilidade; o driver de chip Realtek é mantido pela comunidade. O EdgeXpert já possui Wi-Fi 7, e o uso do ALFA externo é principalmente para testes de penetração ou necessidades de chip específicas.
