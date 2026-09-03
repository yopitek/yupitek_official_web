---
title: "Suporte do Cartão de Rede Wireless ALFA para o ASUS Ascent GX10 (GB10)"
date: 2026-09-03
draft: false
slug: "alfa-asus-ascent-gx10-compatibility"
tags:
  - "ALFA"
  - "ASUS"
  - "Ascent-GX10"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "Guia de Hardware"
description: "ASUS GX10 e NVIDIA DGX Spark compartilham hardware e software, compatibilidade ALFA, MediaTek e Realtek, USB-C, adaptador necessário."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumo do Problema

Pergunta do cliente: “O adaptador de rede sem fio USB da série ALFA pode ser utilizado no supercomputador ASUS Ascent GX10 (NVIDIA GB10 Grace Blackwell) AI?”

Conclusão breve: O ASUS Ascent GX10 e o NVIDIA DGX Spark compartilham a mesma plataforma de hardware GB10 e o ambiente de software DGX OS, garantindo total compatibilidade com o adaptador de rede ALFA (avaliação baseada nos 9 modelos de adaptadores de rede USB atuais da ALFA). Os modelos com chip MediaTek (AWUS036ACM / ACHM / AXML / AXM, 4 modelos) utilizam o driver in-kernel, prontos para uso imediato; os modelos com chip Realtek (AWUS036ACH / ACS / EACS / AX / AXER, 5 modelos) requerem a compilação do driver out-of-tree no ARM64. Atenção: todos os ports USB do GX10 são do tipo USB Type-C (3 ports de dados + 1 port de entrada PD), exceto o AXML, que necessita de um adaptador USB-C to USB-A.

## 2. Análise da Arquitetura de Especificações de Hardware de Objetivo

### 2.1 Especificações de Hardware do ASUS Ascent GX10

| Item | Especificação |
|---|---|
| Nome do Produto | ASUS Ascent GX10 |
| Chip de Núcleo | NVIDIA GB10 Grace Blackwell Superchip (Plataforma DGX Spark) |
| CPU | 20-core Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Arquitetura Blackwell da NVIDIA, 6144 núcleos CUDA, Cincoª Geração Tensor Core, Quartoª Geração RT Core |
| Desempenho de IA | Até 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| Memória do Sistema | 128GB LPDDR5x Memória Unificada (256-bit, 273 GB/s) |
| Armazenamento | Até 4TB NVMe M.2 SSD (autenticado) |
| USB | 3× USB 3.2 Gen 2×2 Type-C (20Gbps, DP Alt Mode / DisplayPort 2.1) + 1× USB 3.2 Gen 2×2 Type-C (PD Entrada, 180W EPR PD3.1) |
| Saída de Vídeo | 1× HDMI 2.1 (pode ser usado em conjunto com o DP Alt Mode para saída de múltiplos monitores) |
| Rede com Fio | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (2× 200G QSFP112) |
| Rede sem Fio | Wi-Fi 7 (MediaTek AW-EM637, 2×2 MIMO) + Bluetooth 5.4 |
| Sistema Operacional | NVIDIA DGX OS (baseado no Ubuntu Linux, kernel 6.x) |
| Arquitetura | aarch64 (ARM64) |
| Tamanho | 150 × 150 × 51 mm (5.91 × 5.91 × 2.01 polegadas) |
| Peso | 1.48 kg |
| Refrigeração | Sistema de Refrigeração Patenteado da ASUS (ventilador silencioso + tubo de condução de calor) |
| Outros | Buraco de Chave Kensington para Segurança |

> ⚠️ Nota de Correção de Especificações: O rascunho original escreveu "150 × 150 × 50 mm" e não incluiu peso. Após verificação, as especificações oficiais da ASUS techspec são **150 × 150 × 51 mm / 1.48 kg**, que foram corrigidas. A versão do HDMI é 2.1 (o rascunho escreveu 2.1b e foi corrigido). Veja a Seção 10 de Referências.

### 2.2 Ambiente de Software: NVIDIA DGX OS

| Item | Conteúdo |
|---|---|
| OS Básico | Ubuntu Linux (personalizado pela NVIDIA) |
| Kernel | Linux 6.x |
| Arquitetura | aarch64 (ARM64) |
| Software Pré-instalado | Conjunto de Software de IA da NVIDIA (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Gestão de Pacotes | apt |

### 2.3 Diferenças com o DGX Spark

| Item de Diferença | ASUS GX10 | NVIDIA DGX Spark |
|---|---|---|
| Design de Refrigeração | Sistema de Refrigeração Patenteado da ASUS | Refrigeração Referencial da NVIDIA |
| Design de Estrutura | Gabinete Personalizado da ASUS | Gabinete Referencial da NVIDIA |
| Módulo sem Fio | MediaTek AW-EM637 (Wi-Fi 7) | Módulo sem Fio de Nível de同类 |
| Acessórios | Acessórios de Fábrica da ASUS | Acessórios de Fábrica da NVIDIA |
| Garantia | Garantia da ASUS | Garantia da NVIDIA |

Impacto na Compatibilidade com o ALFA: Sem impacto. Controladores de USB, versão do kernel e framework de drivers são completamente idênticos ao DGX Spark.

## 3. Análise das Especificações da Placa de Rede ALFA e do Chipset

Até setembro de 2026, a linha de produtos de placas de rede USB sem fio da ALFA Network é a seguinte:

| Modelo | Nível Wi-Fi | Chipset | Interface | Estado do Driver Linux |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel (mt7921u) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel (mt7921u) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 / out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Igual acima |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree (8812au) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel (mt76x2u)⭐ Recomendado |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree (8812au coberto) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree (8821cu) |

## 4. Modelos Aplicáveis e Chipsets

### 4.1 Classificação de Recomendação

| Nível de Recomendação | Modelo (Chipset) | Descrição |
|---|---|---|
| ⭐ Recomendação Forte | AWUS036ACM (MT7612U) | Driver in-kernel, pronto para uso, AC1200 dual-band, suporta AP / Monitor / Injection |
| ✅ Recomendado | AWUS036ACHM (MT7610U) | Driver in-kernel, baixo consumo de energia, AC433 dual-band |
| ✅ Recomendado (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | Driver in-kernel, Wi-Fi 6E, AXML com conector USB-C direto |
| ⚠️ Disponível mas requer compilação | AWUS036ACH (RTL8812AU) | Requer compilação do morrownr/8812au (ARM64), após a compilação, todas as funções estarão completas |
| ⚠️ Disponível mas requer compilação | AWUS036ACS / EACS | Requer compilação do driver out-of-tree correspondente |
| ⚠️ Disponível mas requer atenção | AWUS036AX / AXER (RTL8832BU) | O rtw89 do kernel 6.x pode já suportar; não há necessidade de compilação |

### 4.2 Sugestões de Uso

| Cenário de Uso | Modelo Recomendado | Descrição |
|---|---|---|
| Acesso Wireless Básico (muito simples) | AWUS036ACM / ACHM | Driver in-kernel, sem necessidade de compilação |
| Teste de Penetração / Monitoramento / Injeção de Wireless | AWUS036ACH ou AWUS036ACM | Ambos suportam Monitor + Injection |
| Wi-Fi 6E / 6GHz | AWUS036AXML / AXM | Driver in-kernel MT7921AUN |
| Não necessita de Wi-Fi Externo | — | GX10 já possui Wi-Fi 7 integrado, geralmente não há necessidade de conexão externa |

## 5. Requisitos de Ambiente

### 5.1 Requisitos de Hardware

| Item | Requisitos |
|---|---|
| Conector USB | Conector USB-C para USB-A ou cabo de transmissão (exceto AXML), recomendado suporte a USB 3.2 Gen 2×2 |
| Alimentação | Fonte de alimentação USB-C original ASUS GX10 (180W EPR PD3.1) |

### 5.2 Requisitos de Software

| Item | Requisitos |
|---|---|
| Versão do DGX OS | Qualquer versão em serviço (kernel 6.x) |
| Ferramentas de Compilação (para chipsets Realtek) | build-essential, git, bc, dkms |
| Ferramentas de Gestão de Rede | iw, network-manager (instalado por padrão no DGX OS) |

## 6. Determinação de Compatibilidade

### Matriz de Compatibilidade do Modelo Atual ALFA × ASUS Ascent GX10 (GB10)

| Modelo | Chipset | Modo de Driver | Detecção USB | Internet STA | Modo AP | Monitor | Dificuldade de Instalação | Avaliação Geral |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel (mt76x2u) | ✅ | ✅ | ✅ | ✅ | Sem instalação | ⭐ Melhor |
| AWUS036ACHM | MT7610U | in-kernel (mt76x0u) | ✅ | ✅ | ✅ | ⚠️ Limitado | Sem instalação | ✅ Boa |
| AWUS036AXML | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ Limitado | Sem instalação | ✅ Boa |
| AWUS036AXM | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ Limitado | Sem instalação | ✅ Boa |
| AWUS036ACH | RTL8812AU | out-of-tree (8812au) | ✅ | ✅ | ✅ | ✅ | Médio (tradução) | ⚠️ Utilizável |
| AWUS036ACS | RTL8811AU | out-of-tree (8812au) | ✅ | ✅ | ⚠️ | ❌ | Médio (tradução) | ⚠️ Utilizável |
| AWUS036EACS | RTL8811CU | out-of-tree (8821cu) | ✅ | ⚠️ | ❌ | ❌ | Médio (tradução) | ⚠️ Utilizável |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Médio-Alto | ⚠️ Utilizável |
| AWUS036AXER | RTL8832BU | Igual ao acima | ✅ | ⚠️ | ⚠️ | ❌ | Médio-Alto | ⚠️ Utilizável |

Critério de Determinação: O ASUS GX10 e o DGX Spark compartilham a mesma plataforma de hardware GB10 e o DGX OS (kernel 6.x, aarch64), e a determinação de compatibilidade é completamente idêntica à do DGX Spark.

## 7. Passo a Passo Detalhado de Configuração

Os passos de instalação do ASUS GX10 são idênticos aos do NVIDIA DGX Spark. A seguir está uma versão resumida; para os passos completos, consulte o Capítulo 7 de [ALFA 无线网卡是否支持 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modelos de Chip MediaTek (Pronto para Uso)

- Utilize o adaptador USB-C to USB-A (AXML pode ser diretamente conectado), insira a placa de rede ALFA no porta USB-C do GX10
- Confira a detecção: `lsusb`
- Confira a interface: `ip link show` (deve aparecer wlan0 automaticamente)
- Conecte-se à rede WiFi: `nmcli dev wifi connect "SSID" password "senha"`

### 7.2 Modelos de Chip Realtek (Necessita de Compilação)

Tomando como exemplo o AWUS036ACH (RTL8812AU):

```bash
# 1. Instale as ferramentas de compilação
sudo apt update && sudo apt install -y build-essential git bc dkms

# 2. Baixe e compile o driver
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
# Confira que o CONFIG_PLATFORM_ARM64 = y está no Makefile
make
sudo make install
sudo modprobe 8812au

# 3. Após a inserção da placa de rede, confira a interface
ip link show

# 4. Conecte-se à rede WiFi
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
| O `lsusb` não mostra a placa de rede ALFA | Adaptador USB-C defeituoso / Suporte apenas para carga | Troque por um adaptador USB 3.2 Gen 2×2 que suporte transferência de dados; tente em diferentes portas USB-C |
| Chip MediaTek sem interface wlan | Módulo não carregado automaticamente / Firmware faltando | Execute `sudo modprobe mt76x2u`；instale `sudo apt install linux-firmware`；verifique `dmesg | grep mt76` |
| Falha na compilação do driver Realtek | Configuração de cross-compilação incorreta | Confira a compilação nativa no GX10; o Makefile não deve definir CROSS_COMPILE |
| Velocidade de WiFi lenta | Adaptador suporta apenas USB 2.0 | Troque por um adaptador USB 3.2 Gen 2×2 |
| Conflito entre Wi-Fi interno e externo | Conflito de roteamento | Execute `sudo nmcli radio wifi off` para desativar o Wi-Fi interno antes de usar o Wi-Fi externo |
| Não é possível usar a frequência de 6GHz | Restrição de Domínio Regulatório | Execute `sudo iw reg set US`；confira as últimas regulamentações |

## 9. Restrições Conhecidas

- **Requisito de Conversão USB Type-C**: Além do AXML, todos os adaptadores de rede ALFA necessitam de adaptador USB-C to USB-A.
- **Tradução Manual de Chipsets Realtek**: RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU não foram incluídos no mainline.
- **Possível Conflito com Wi-Fi 7 Integrado**: O GX10 já possui Wi-Fi 7 (MediaTek AW-EM637).
- **Configuração Manual do Modo AP**: O DGX OS é pré-configurado como ambiente de desenvolvimento.
- **Restrições Regulamentares de 6GHz**: A disponibilidade do Wi-Fi 6E depende da região regulamentar.
- **Dependência de Atualizações de Drivers**: Drivers out-of-tree da Realtek são mantidos pela comunidade, e após atualizações do kernel, é necessário recompilar.
- **Diferenças de Hardware da ASUS Não Afetam a Compatibilidade**: Diferenças em dissipação de calor e design de estrutura não afetam a compatibilidade do driver USB WiFi.

**Condições de Rejeição**: As avaliações acima são baseadas no DGX OS (baseado em Ubuntu, kernel 6.x). Caso a ASUS venha a lançar futuras versões de sistemas operacionais não-DGX (como versões próprias do Android ou sistemas operacionais personalizados), a avaliação deve ser revalidada.

## 10. Fontes de Referência URL

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| ASUS Ascent GX10 Especificações Técnicas Oficiais | Especificações de Hardware GX10 (150×150×51mm / 1,48kg / Configuração USB / HDMI 2.1) | https://www.asus.com/ph/networking-iot-servers/desktop-ai-supercomputer/ultra-small-ai-supercomputers/asus-ascent-gx10/techspec/ | ✅ Verificado | 2026-09-03 |
| ASUS Ascent GX10 Loja Oficial (Reino Unido) | Página do Produto GX10 (150 × 150 × 51mm) | https://uk.store.asus.com/asus-ascent-gx105004-33389.html | ✅ Verificado | 2026-09-03 |
| NVIDIA DGX Spark Página Oficial | Informações sobre a Plataforma GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Driver RTL8812AU para Linux | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| Guia de Linux para ALFA Soft AP WiFi Hotspot (Yupitek) | Guia de Modo AP do ALFA Linux | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verificado | 2026-09-03 |
| Visão Geral de Produtos da ALFA Network (Yupitek) | Especificações dos Produtos Atuais da ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |

Artigos Relacionados: [O Cartão de Rede sem Fio ALFA suporta o NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[O Cartão de Rede sem Fio ALFA suporta o ALTOS BrainSphere GB10 F1?](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[O Cartão de Rede sem Fio ALFA suporta o GIGABYTE AI TOP ATOM?](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[O Cartão de Rede sem Fio ALFA suporta o MSI EdgeXpert?](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)

Declaração de Isenção de Responsabilidade: A determinação de compatibilidade deste artigo é baseada no NVIDIA DGX OS pré-instalado no ASUS Ascent GX10 (kernel 6.x, aarch64). O GX10 compartilha a mesma plataforma de hardware com o DGX Spark, garantindo completa compatibilidade. O driver de chip MediaTek é do Linux mainline, oferecendo alta estabilidade; o driver de chip Realtek é mantido pela comunidade. O GX10 já possui Wi-Fi 7 integrado, e o uso do ALFA é principalmente para testes de penetração ou necessidades de chip específicas.
