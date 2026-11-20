---
title: "Suporte do Adaptador de Rede Wireless ALFA para o MSI EdgeXpert (GB10)"
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
description: "As 9 placas USB ALFA no MSI EdgeXpert (GB10): testadas no ASUS GX10 (kernel 6.17), usam driver nativo sem DKMS; EACS/ACH/ACS injetam melhor e AXM/AXML falham."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Este artigo foi atualizado com os testes no GX10 de novembro de 2026: no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), as 9 placas de rede ALFA atuais usam todas drivers nativos do kernel, funcionam ao conectar e não precisam de DKMS. Dados completos em [Tabela de testes ARM64 das 9 placas de rede ALFA](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Testado apenas no GX10; os demais modelos GB10 não foram testados um a um.

## 1. Resumo do Problema

Pergunta do cliente: “O adaptador de rede sem fio USB da série ALFA pode ser utilizado no supercomputador MSI EdgeXpert (NVIDIA GB10 Grace Blackwell) AI?”

Conclusão resumida: O MSI EdgeXpert e o NVIDIA DGX Spark usam o mesmo chip GB10 e a mesma família de kernel da NVIDIA. Testamos no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia) os 9 adaptadores de rede USB atuais da ALFA (AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML): todos usam drivers nativos do kernel, funcionam ao conectar e não precisam de compilação nem de DKMS. Espera-se o mesmo comportamento, mas os testes foram feitos apenas no GX10; o MSI EdgeXpert não foi testado individualmente. Diferenças de funcionalidade: os modelos MediaTek MT7921 (AWUS036AXM / AXML) falham na injeção de pacotes (packet injection) no kernel stock 6.17, mas monitor, AP e WPA3 funcionam; nos outros 7 modelos, monitor e injeção foram testados e funcionam. A versão mínima do kernel em que cada driver entrou no mainline varia (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); apenas kernels abaixo dessa versão precisam de drivers DKMS da comunidade. Atenção: Os 4 ports USB do EdgeXpert são todos do tipo USB Type-C (20Gbps), e os adaptadores de rede ALFA (exceto o AXML) precisam de um adaptador USB-C to USB-A.

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
| Armazenamento | 1TB ou 4TB SSD NVMe M.2 (autocriptografado, PCIe Gen5) |
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

O MSI EdgeXpert é uma versão OEM da plataforma DGX Spark, com hardware e software centrais completamente idênticos:

| Item | MSI EdgeXpert | NVIDIA DGX Spark |
|---|---|---|
| Design de Estrutura | Gabinete personalizado pela MSI, opção industrial | Gabinete de referência da NVIDIA |
| Opções de Armazenamento | 1TB / 4TB | Até 4TB |
| Mercado Alvo | IA de borda / IA industrial / Desenvolvimento de desktop | Desenvolvimento de IA de desktop |
| Acessórios | Acessórios originais da MSI | Acessórios originais da NVIDIA |

Impacto na compatibilidade com o ALFA: nenhum impacto esperado (testado apenas no GX10; os demais modelos GB10 não foram testados um a um). Controladores USB, versão do kernel e framework de drivers são completamente idênticos ao DGX Spark.

### 2.4 Necessidade de Adaptador USB Type-C

Os 4 conectores USB do EdgeXpert são Type-C, enquanto todos os cartões de rede da ALFA (exceto o AXML, que é USB-C) são Type-A, exigindo um adaptador. Recomenda-se a escolha de um adaptador que suporte USB 3.2 Gen 2×2 (20Gbps).

## 3. Análise das Especificações e Chipsets da Placa de Rede ALFA

Até setembro de 2026, a linha de produtos de placas de rede USB sem fio da ALFA Network é a seguinte (baseada em 9 modelos):

| Modelo | Nível Wi-Fi | Chipset | Interface | Driver Linux nativo (versão mínima do kernel) |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E (6GHz testado e funcional) | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ Nativo (mt7921u, 5.18+) |
| AWUS036AXM | Wi-Fi 6E (segundo o fabricante; 6GHz não testado) | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ Nativo (mt7921u, 5.18+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ Nativo (rtw89_8852bu, 6.17+) |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ Nativo (rtw89_8852bu, 6.17+) |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ Nativo (rtw88_8812au, 6.13+) |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | ✅ Nativo (mt76x0u, 4.19+) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ Nativo (mt76x2u, 4.19+) |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | ✅ Nativo (rtw88_8821au, 6.13+) |
| AWUS036EACS | Wi-Fi 5 (AC600) + Bluetooth | Realtek RTL8821CU | USB 2.0 | ✅ Nativo (rtw88_8821cu, 6.2+) |

Nota: o kernel 6.17 testado no GX10 já integra os drivers das 9 placas; a versão mínima do kernel varia por placa (veja os parênteses da tabela). Somente sistemas antigos com kernel abaixo da versão mínima da placa precisam de drivers DKMS mantidos pela comunidade.

## 4. Modelos Aplicáveis e Chipsets

### 4.1 Classificação de Recomendação

| Nível de Recomendação | Modelo (Chipset) | Descrição |
|---|---|---|
| ⭐ Melhor escolha para testes de penetração | AWUS036EACS (RTL8821CU) / AWUS036ACH (RTL8812AU) / AWUS036ACS (RTL8811AU) | Driver nativo, sem instalação; injeção testada: EACS e ACH 100% nas duas bandas, ACS 100% em 2.4GHz e 96% em 5GHz; captura de WPA handshake de ponta a ponta |
| ✅ Recomendado | AWUS036ACM (MT7612U) | Driver nativo, sem instalação; monitor, injeção (2.4GHz 63–83%, 5GHz 76%), AP e WPA3 funcionam |
| ✅ Recomendado | AWUS036ACHM (MT7610U) | Driver nativo, sem instalação; injeção em 2.4GHz 96–100%, em 5GHz apenas broadcast; AP WPA3 requer sae_pwe=0 |
| ✅ Recomendado (Wi-Fi 6) | AWUS036AX / AXER (RTL8832BU) | Driver nativo, sem instalação; recepção forte em monitor, injeção funcional (2.4GHz: AX 96%, AXER 73%), AP com 80MHz |
| ⚠️ Apenas conexão / AP | AWUS036AXML / AXM (MT7921AUN) | Driver nativo, sem instalação; monitor, AP e WPA3 funcionam, mas a injeção falha no kernel stock 6.17, não sendo adequado para testes de penetração; AXML com conector USB-C direto |

### 4.2 Sugestões de Uso

| Cenário de Uso | Modelo Recomendado | Descrição |
|---|---|---|
| Internet sem fio em gateways de AI de borda | Qualquer um dos 9 (por exemplo, AWUS036ACM / ACHM) | Todos usam drivers nativos do kernel e funcionam ao conectar |
| Testes de penetração sem fio em ambientes industriais | AWUS036EACS / ACH / ACS | Injeção testada 96–100%, captura de WPA handshake de ponta a ponta; evite AXM / AXML (injeção falha) |
| Wi-Fi 6 + hotspot AP | AWUS036AX / AXER | AP 2x2 com 80MHz testado e funcional |
| Banda de 6GHz | AWUS036AXML | AP WPA3 em 6GHz testado e funcional; o AXM usa o mesmo chip, mas 6GHz não foi testado |
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
| Versão do kernel | O kernel 6.17 (testado no 6.17.0-1014-nvidia) já integra os drivers das 9 placas, sem necessidade de ferramentas de compilação; a versão mínima varia por placa (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), e apenas kernels abaixo dela precisam de drivers DKMS da comunidade |
| Ferramentas de Gestão de Rede | iw, network-manager (instalado por padrão no DGX OS) |

## 6. Determinação de Compatibilidade

### Matriz de Compatibilidade entre Modelos Atuais do ALFA × MSI EdgeXpert (GB10)

| Modelo | Chipset | Driver (nativo do kernel) | Detecção de USB | STA Internet | Modo AP | Monitor | Injeção de pacotes | Dificuldade de Instalação | Avaliação Geral |
|---|---|---|---|---|---|---|---|---|---|
| AWUS036EACS | RTL8821CU | rtw88_8821cu | ✅ | ✅ | ✅ | ✅ | ✅ 100% nas duas bandas | Sem instalação | ⭐ Melhor |
| AWUS036ACH | RTL8812AU | rtw88_8812au | ✅ | ✅ | ✅ | ✅ | ✅ 100% nas duas bandas | Sem instalação | ⭐ Melhor |
| AWUS036ACS | RTL8811AU | rtw88_8821au | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 100% / 5G 96% | Sem instalação | ⭐ Melhor |
| AWUS036ACM | MT7612U | mt76x2u | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 63–83% / 5G 76% | Sem instalação | ✅ Bom |
| AWUS036ACHM | MT7610U | mt76x0u | ✅ | ✅ | ✅ | ✅ | ⚠️ 2.4G 96–100% / 5G apenas broadcast | Sem instalação | ✅ Bom |
| AWUS036AX | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ Recepção forte | ✅ 2.4G 96% / 5G funcional | Sem instalação | ✅ Bom |
| AWUS036AXER | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ Recepção forte | ✅ 2.4G 73% / 5G funcional | Sem instalação | ✅ Bom |
| AWUS036AXML | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ Recepção fraca | ❌ Falha | Sem instalação | ⚠️ Apenas conexão / AP |
| AWUS036AXM | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ Recepção fraca | ❌ Falha | Sem instalação | ⚠️ Apenas conexão / AP |

Critério de Determinação: testes em máquina real realizados de 16 a 18/11/2026 no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), usando como alvo Wi-Fi e celulares próprios. O MSI EdgeXpert usa o mesmo GB10 e a mesma família de kernel da NVIDIA, portanto espera-se o mesmo comportamento, mas os testes foram feitos apenas no GX10; o MSI EdgeXpert não foi testado individualmente. Dados completos em [Tabela de testes ARM64 das 9 placas de rede ALFA](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 7. Passo a Passo Detalhado de Configuração

Espera-se que os passos de instalação do MSI EdgeXpert sejam idênticos aos do NVIDIA DGX Spark (passos testados no GX10). A seguir, está uma versão resumida; para o passo a passo completo, consulte o Capítulo 7 de [A Placa de Rede sem Fio ALFA Suporta o NVIDIA DGX Spark?](/pt/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modelos de Chip MediaTek (AWUS036ACM / ACHM / AXM / AXML)

**Passo 1: Insira a Placa de Rede**

Utilize um adaptador USB-C to USB-A (AXML pode ser conectado diretamente) para inserir a placa de rede ALFA na porta USB-C do EdgeXpert.

**Passo 2: Confirme a Detecção do USB**

```bash
lsusb
# Saída esperada (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Passo 3: Confirme a Interface de Rede**

```bash
ip link show
# Deve aparecer automaticamente uma interface começando com wlx (driver in-kernel carregado automaticamente)
```

**Passo 4: Conecte-se à WiFi**

```bash
nmcli dev wifi connect "SSID" password "senha"
```

### 7.2 Modelos de Chip Realtek (AWUS036ACH / ACS / EACS / AX / AXER)

O kernel 6.17 (versão testada no GX10) já integra os drivers de todos os modelos Realtek; os passos são os mesmos dos modelos MediaTek, sem compilação (versões mínimas: EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17):

```bash
# 1. Confira a versão do kernel (a partir do 6.17 todos os drivers Realtek vêm integrados; no GX10 testado: 6.17.0-1014-nvidia)
uname -r

# 2. Após inserir a placa de rede, confira se o driver foi carregado automaticamente
lsusb
lsmod | grep -E "rtw88|rtw89"
ip link show

# 3. Conecte-se à WiFi
nmcli dev wifi connect "SSID" password "senha"
```

Módulos carregados automaticamente por modelo: ACH → `rtw88_8812au`, ACS → `rtw88_8821au`, EACS → `rtw88_8821cu`, AX / AXER → `rtw89_8852bu`. Somente se `uname -r` for inferior à versão mínima da placa (sistemas antigos) é necessário instalar drivers DKMS mantidos pela comunidade (por exemplo, morrownr/8812au-20210820 para o RTL8812AU).

### 7.3 Modo de Escuta (Teste de Penetração)

⚠️ Faça testes de monitoramento e injeção apenas em redes próprias ou com autorização.

```bash
sudo apt install -y aircrack-ng
IF=wlx00c0cafe0000   # substitua pelo nome da interface mostrado em ip link
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
sudo aireplay-ng --test $IF
```

- Não execute `airmon-ng check kill`: ele encerra o NetworkManager e deixa o host sem conexão externa.
- No kernel stock 6.17, o `aireplay-ng --test` falha nos AWUS036AXM / AXML (Found 0 APs), impossibilitando deauth ou captura de handshake.
- O hcxdumptool 8.x apresenta `failed to arm` nas 9 placas, exceto o EACS em 2.4 GHz (o driver não suporta active monitor); use airodump-ng + aireplay-ng.

## 8. Erros Comuns e Solução

| Sintoma | Possível Causa | Solução |
|---|---|---|
| `lsusb` não vê a placa de rede ALFA | Conector USB-C defeituoso / Especificação de apenas carregamento | Troque por um conector USB 3.2 Gen 2×2 que suporte transferência de dados; tente em diferentes portas USB-C |
| Chipset MediaTek sem interface wlan | Módulo não carregado automaticamente / Firmware faltando | `sudo modprobe mt76x2u`; `sudo apt install linux-firmware`; verifique `dmesg \| grep mt76` |
| Placa Realtek inserida sem interface wlan | Kernel abaixo da versão mínima da placa (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), sem o driver correspondente integrado | Confirme a versão com `uname -r`; atualize o kernel ou, em kernel antigo, instale o driver DKMS da comunidade |
| Nenhum sinal é detectado após alternar repetidamente entre monitor / AP | Travamento de RX (RX stall) | Desconecte e reconecte a placa para que o USB seja reenumerado |
| EACS / AXML sem interface wlx após reconectar | Probe travado no dispositivo composto Bluetooth + Wi-Fi | Reconecte em outra porta USB |
| Velocidade de WiFi lenta | Conector suporta apenas USB 2.0 | Troque por um conector USB 3.2 Gen 2×2 |
| Conflito entre Wi-Fi 7 integrado e externo | Conflito de roteamento | `sudo nmcli radio wifi off` desative o Wi-Fi integrado antes de usar o Wi-Fi externo |
| Instabilidade em ambientes industriais de alta temperatura | Refrigeração / Diferenças na versão industrial | Confirme o uso da versão industrial do EdgeXpert (MS-C931); certifique-se de que a temperatura ambiente está dentro do intervalo especificado |

## 9. Restrições Conhecidas

- Necessidade de adaptador USB Type-C: Além do AXML, todos os cartões de rede ALFA necessitam de adaptador USB-C to USB-A
- Falha de injeção nos modelos MT7921: os AWUS036AXM / AXML falham na injeção de pacotes no kernel stock 6.17, sem deauth nem captura de handshake; monitor, AP e WPA3 funcionam. A causa principal é uma regressão de chanctx do mac80211 a partir do kernel 6.16; drivers corrigidos pela comunidade ainda têm limitação de taxa
- Escopo dos testes: testado apenas no ASUS GX10 (kernel 6.17.0-1014-nvidia); o MSI EdgeXpert não foi testado individualmente, espera-se o mesmo comportamento
- hcxdumptool indisponível: todas as placas, exceto o EACS em 2.4 GHz, apresentam `failed to arm`; use airodump-ng + aireplay-ng
- Possível conflito com Wi-Fi 7 integrado: EdgeXpert já possui Wi-Fi 7 + BT 5.4 integrados
- Modo AP precisa de configuração manual: O DGX OS é pré-configurado como ambiente de desenvolvimento
- Restrições regulatórias de 6GHz: A disponibilidade do Wi-Fi 6E depende da região regulatória
- Kernel antigo: somente em sistemas com kernel abaixo da versão mínima da placa (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17) os modelos Realtek precisam de drivers DKMS da comunidade, que devem ser recompilados a cada atualização do kernel
- Diferenças na versão industrial não afetam a compatibilidade: A versão industrial da MSI (MS-C931) possui especificações de hardware idênticas à versão de consumo, e a compatibilidade do USB WiFi é a mesma

Condições de refutação: Se a página de especificações oficiais da MSI for alterada (ajustes na especificação da porta USB, versão do kernel inferior a 6.x), ou se testes em máquina real revelarem que o mt76x2u / mt7921u não carregam automaticamente no DGX OS, a matriz de compatibilidade descrita no Capítulo 6 deve ser revisada novamente; se o comportamento dos drivers nativos mudar após uma atualização do kernel da NVIDIA, será necessário testar novamente.

## 10. Fontes de Referência URL

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| MSI EdgeXpert Loja Oficial (US) | Especificações da Edição Consumidor do EdgeXpert | https://us-store.msi.com/MSI-EdgeXpert-Blackwell-AI-Supercomputer | ✅ Verificado | 2026-09-03 |
| MSI EdgeXpert Loja (TW) | Especificações da Edição Consumidor do EdgeXpert (23STW) | https://tw-store.msi.com/products/edgexpert-23stw-bgb104tg4 | ✅ Verificado | 2026-09-03 |
| MSI Anúncios de Computadores Industriais | Informações de Lançamento do EdgeXpert | https://ipc.msi.com/en/news/146241 | ✅ Verificado | 2026-09-03 |
| NVIDIA DGX Spark Página Oficial | Informações sobre a Plataforma GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Driver RTL8812AU para Linux | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| ALFA Network Visão Geral de Produtos (Yopitek) | Especificações dos Produtos Atuais da ALFA | /pt/products/alfa/ | ✅ Verificado | 2026-09-03 |
| Tabela de testes ARM64 das 9 placas de rede ALFA (Yopitek) | Testes em máquina real no ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Testado | 2026-11-18 |

Artigos Relacionados: [A Placa de Rede sem Fio ALFA Suporta o NVIDIA DGX Spark?](/pt/blog/alfa-nvidia-dgx-spark-compatibility/) | [A Placa de Rede sem Fio ALFA Suporta o ASUS Ascent GX10?](/pt/blog/alfa-asus-ascent-gx10-compatibility/) | [A Placa de Rede sem Fio ALFA Suporta o ALTOS BrainSphere GB10 F1?](/pt/blog/alfa-altos-brainsphere-gb10-compatibility/) | [A Placa de Rede sem Fio ALFA Suporta o GIGABYTE AI TOP ATOM?](/pt/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [A Placa de Rede sem Fio ALFA Suporta o NVIDIA Jetson Nano?](/pt/blog/alfa-nvidia-jetson-nano-compatibility/)

Declaração de Isenção de Responsabilidade: A determinação de compatibilidade deste artigo é baseada nos testes em máquina real realizados em novembro de 2026 no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia). O MSI EdgeXpert e o GX10 usam o mesmo GB10 e a mesma família de kernel da NVIDIA, portanto espera-se o mesmo comportamento, mas ele não foi testado individualmente. O kernel 6.17 testado no GX10 já integra os drivers das 9 placas de rede ALFA (a versão mínima varia por placa); apenas kernels abaixo da versão mínima da placa precisam de drivers DKMS da comunidade. O EdgeXpert já possui Wi-Fi 7, e o uso do ALFA externo é principalmente para testes de penetração ou necessidades de chip específicas. Monitoramento e injeção devem ser feitos apenas em redes próprias ou com autorização.
