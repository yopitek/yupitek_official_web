---
title: "\"Suporte do Cartão de Rede Wireless ALFA para o ALTOS BrainSphere GB10 F1\""
date: 2026-09-03
draft: false
slug: "alfa-altos-brainsphere-gb10-compatibility"
tags:
  - "ALFA"
  - "Altos"
  - "BrainSphere-GB10"
  - "NVIDIA-GB10"
  - "AWUS036ACM"
  - "ARM64"
  - "DGX-OS"
categories:
  - "Guia de Hardware"
description: "GB10 F1 & NVIDIA DGX Spark共享硬件平台，ALFA网卡兼容，MediaTek芯片即插即用，Realtek需编译驱动，注意USB端口配置。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumo do Problema

Pergunta do cliente: “O adaptador de rede sem fio ALFA da série USB pode ser utilizado no trabalho站 ALTOS BrainSphere GB10 F1 (NVIDIA GB10 Grace Blackwell)?”

Conclusão resumida: O trabalho站 ALTOS BrainSphere GB10 F1 compartilha a mesma plataforma de hardware GB10 e o ambiente de software DGX OS com o NVIDIA DGX Spark, garantindo a mesma compatibilidade com os adaptadores de rede ALFA (avaliados 9 modelos de adaptadores de rede USB ativos). Os modelos de chip MediaTek (AWUS036ACM / ACHM / AXML / AXM, 4 modelos) utilizam drivers in-kernel, prontos para uso imediato; os modelos de chip Realtek (AWUS036ACH / ACS / EACS / AX / AXER, 5 modelos) requerem a compilação de drivers out-of-tree no ARM64. Atenção: O BrainSphere GB10 F1 possui 3 portas USB-C de dados + 1 porta de entrada USB-C PD, e os adaptadores de rede ALFA (exceto o AXML) precisam de um adaptador USB-C to USB-A.

## 2. Análise da Arquitetura de Especificações de Hardware de Objetivo

### 2.1 Especificações de Hardware do ALTOS BrainSphere GB10 F1

| Item | Especificação |
|---|---|
| Nome do Produto | ALTOS BrainSphere GB10 F1 (Acer / Altos Computing) |
| Chip de Núcleo | NVIDIA GB10 Grace Blackwell Superchip (Plataforma DGX Spark) |
| CPU | 20-núcleo Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Arquitetura Blackwell da NVIDIA, 6144 núcleos CUDA, Cincoª Geração Tensor Core, Quartoª Geração RT Core |
| Desempenho de IA | Até 1 PetaFLOP (FP4, Sparse) / 1000 TOPS, suporta modelos com até 200 bilhões de parâmetros |
| Memória do Sistema | 128GB LPDDR5x Memória Unificada (256-bit, 273 GB/s) |
| Armazenamento | 4TB NVMe M.2 SSD (autosegurança) |
| USB | 3× USB 3.2 Gen 2×2 Type-C (20Gbps, DP Alt Mode) + 1× USB 3.2 Gen 2×2 Type-C (PD Entrada, 180W EPR PD3.1) |
| Saída de Vídeo | 1× HDMI 2.1a |
| Rede com Fio | 1× 10GbE RJ45 + NVIDIA ConnectX-7 NIC (200G × 2 QSFP) |
| Rede sem Fio | Wi-Fi 7 + Bluetooth 5.4 com LE |
| Sistema Operacional | NVIDIA DGX OS (baseado em Ubuntu Linux, kernel 6.x) |
| Arquitetura | aarch64 (ARM64) |
| Tamanho | 150 × 150 × 50 mm (1.13L) |
| Peso | < 1.5 kg |
| Consumo Máximo | 170W |
| Software Incluído | Altos aiGeni (plataforma de desenvolvimento de IA em um clique, suporta TensorFlow / PyTorch / Jupyter / Ollama) |

> Verificação das Especificações: As dimensões / peso / consumo / configuração de USB acima estão consistentes com o Product Sheet PDF oficial da Altos (ver Capítulo 10 de Referências).

### 2.2 Ambiente de Software: NVIDIA DGX OS + Altos aiGeni

| Item | Conteúdo |
|---|---|
| OS Básico | Ubuntu Linux (personalizado pela NVIDIA, DGX OS) |
| Kernel | Linux 6.x |
| Arquitetura | aarch64 (ARM64) |
| Plataforma de IA | Altos aiGeni (implantação de ambiente em um clique, backup automático, monitoramento em tempo real, ferramentas inteligentes) |
| Frameworks Pré-instalados | TensorFlow, PyTorch, Jupyter, Ollama |
| Gestão de Pacotes | apt |

### 2.3 Diferenças com o DGX Spark

| Item de Diferença | BrainSphere GB10 F1 | NVIDIA DGX Spark |
|---|---|---|
| Software Incluído | Plataforma de Desenvolvimento de IA Altos aiGeni | Conjunto de Software de Referência da NVIDIA |
| Design de Estrutura | Gabinete personalizado pela Altos / Acer | Gabinete de Referência da NVIDIA |
| Mercado-Alvo | Empresas de IA / Instituições de Pesquisa / Educação | Desenvolvimento de IA em Escritório |
| Consumo Máximo | 170W | Aproximadamente 240W (com conversão de energia) |

Impacto na Compatibilidade com o ALFA: Sem impacto. O Altos aiGeni é um software de aplicação, não afeta o framework de drivers do kernel. Os controladores de USB, versão do kernel e arquitetura de drivers são completamente idênticos ao DGX Spark.

### 2.4 Necessidade de Adaptadores USB Type-C

Os 4 portas USB do BrainSphere GB10 F1 são todas Type-C (3 de dados + 1 de entrada PD), enquanto a linha completa de placas de rede ALFA (exceto a AXML, que é USB-C) são USB Type-A, necessitando de adaptadores.

## 3. Análise das Especificações e Chipsets da Placa de Rede ALFA

Até setembro de 2026, a linha de produtos de placas de rede USB sem fio da ALFA Network é a seguinte:

| Modelo | Nível Wi-Fi | Chipset | Interface | Estado do Driver Linux |
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
| ⚠️ Disponível mas requer atenção | AWUS036AX / AXER (RTL8832BU) | O rtw89 do kernel 6.x pode já suportar; não há necessidade de compilação |

### 4.2 Sugestões de Uso

| Cenário de Uso | Modelo Recomendado | Descrição |
|---|---|---|
| Laboratório de IA corporativo para internet sem fio | AWUS036ACM / ACHM | Driver in-kernel, estável, sem manutenção, adequado para ambiente corporativo |
| Teste de penetração de wireless / pesquisa de segurança | AWUS036ACH ou AWUS036ACM | Ambos suportam Monitor + Injection |
| Wi-Fi 6E / Frequência de 6GHz | AWUS036AXML / AXM | Driver in-kernel MT7921AUN |
| Não necessita de Wi-Fi externo | — | BrainSphere já possui Wi-Fi 7 integrado, geralmente não há necessidade de conexão externa |

## 5. Requisitos de Ambiente

### 5.1 Requisitos de Hardware

| Item | Requisitos |
|---|---|
| Conector USB | Conector USB-C para USB-A ou cabo de transmissão (exceto AXML), recomendado suporte ao USB 3.2 Gen 2×2 |
| Alimentação | Fonte de alimentação USB-C original da ALTOS (180W EPR PD3.1) |

### 5.2 Requisitos de Software

| Item | Requisitos |
|---|---|
| Versão do DGX OS | Qualquer versão em serviço (kernel 6.x) |
| Ferramentas de Compilação (para chipsets Realtek) | build-essential, git, bc, dkms |
| Ferramentas de Gestão de Rede sem fio | iw, network-manager (instalado por padrão no DGX OS) |
| Notas sobre aiGeni | Se for utilizado o ambiente de contêineres do aiGeni, é necessário garantir que o dispositivo USB já está corretamente montado no contêiner (recomenda-se configurar no nível do host OS para acesso à Internet). |

## 6. Determinação de Compatibilidade

### Matriz de Compatibilidade ALFA Modelos Atuais × ALTOS BrainSphere GB10 F1

| Modelo | Chipset | Modo de Drive | Detecção USB | STA Internet | Modo AP | Monitor | Dificuldade de Instalação | Avaliação Geral |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel（mt76x2u） | ✅ | ✅ | ✅ | ✅ | Sem instalação | ⭐ Melhor |
| AWUS036ACHM | MT7610U | in-kernel（mt76x0u） | ✅ | ✅ | ✅ | ⚠️ Limitado | Sem instalação | ✅ Bom |
| AWUS036AXML | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ Limitado | Sem instalação | ✅ Bom |
| AWUS036AXM | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ Limitado | Sem instalação | ✅ Bom |
| AWUS036ACH | RTL8812AU | out-of-tree（8812au） | ✅ | ✅ | ✅ | ✅ | Médio（tradução） | ⚠️ Disponível |
| AWUS036ACS | RTL8811AU | out-of-tree（8812au） | ✅ | ✅ | ⚠️ | ❌ | Médio（tradução） | ⚠️ Disponível |
| AWUS036EACS | RTL8811CU | out-of-tree（8821cu） | ✅ | ⚠️ | ❌ | ❌ | Médio（tradução） | ⚠️ Disponível |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Médio-Alto | ⚠️ Disponível |
| AWUS036AXER | RTL8832BU | Igual ao acima | ✅ | ⚠️ | ⚠️ | ❌ | Médio-Alto | ⚠️ Disponível |

Critérios de Determinação: O ALTOS BrainSphere GB10 F1 e o DGX Spark compartilham a mesma plataforma de hardware GB10 e o DGX OS (kernel 6.x, aarch64), e a determinação de compatibilidade é completamente idêntica ao DGX Spark. O Altos aiGeni é um software de camada de aplicação e não afeta a compatibilidade do driver.

## 7. Passo a Passo Detalhado de Configuração

Os passos de instalação do ALTOS BrainSphere GB10 F1 são idênticos aos do NVIDIA DGX Spark. A seguir está uma versão resumida; para os passos completos, consulte o Capítulo 7 de [ALFA Wireless Network Card - Suporte ao NVIDIA DGX Spark](https://yupitek.com/pt-br/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modelos de Chip MediaTek (Pronto para Uso)

- Utilize o adaptador USB-C to USB-A (AXML pode ser diretamente conectado), insira a placa de rede ALFA na porta USB-C do BrainSphere
- Confira a detecção: `lsusb`
- Confira a interface: `ip link show` (deve aparecer wlan0 automaticamente)
- Conecte-se ao WiFi: `nmcli dev wifi connect "SSID" password "senha"`

### 7.2 Modelos de Chip Realtek (Necessita de Compilação)

Tomando como exemplo o AWUS036ACH (RTL8812AU):

```bash
# 1. Instale as ferramentas de compilação
sudo apt update && sudo apt install -y build-essential git bc dkms

# 2. Baixe e compile o driver
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
# Confira que CONFIG_PLATFORM_ARM64 = y está no Makefile
make
sudo make install
sudo modprobe 8812au

# 3. Confira a interface após a inserção da placa de rede
ip link show

# 4. Conecte-se ao WiFi
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

### 7.4 Uso do WiFi no Container aiGeni (Avançado)

Se precisar de usar a placa de rede ALFA no container Altos aiGeni:

1. Complete a instalação do driver e a conexão WiFi no host OS (DGX OS)
2. Inicie o container com `--network=host` ou monte a interface de rede correspondente
3. Recomenda-se que a navegação geral seja feita no nível do host OS, com o container usando `--network=bridge` para compartilhar a rede

## 8. Erros Comuns e Solução

| Sintoma | Possível Causa | Forma de Solução |
|---|---|---|
| `lsusb` não vê a placa de rede ALFA | Adaptador USB-C defeituoso / Especificação de apenas carregamento | Trocar por um adaptador USB 3.2 Gen 2×2 que suporte transferência de dados; tentar em diferentes portas USB-C |
| Chip MediaTek sem interface wlan | Módulo não carregado automaticamente / Firmware faltando | Executar `sudo modprobe mt76x2u`；executar `sudo apt install linux-firmware`；verificar `dmesg | grep mt76` |
| Falha na compilação do driver Realtek | Configuração de cross-compilação incorreta | Confirmar a compilação nativa no BrainSphere; o Makefile não deve definir CROSS_COMPILE |
| Velocidade de WiFi lenta | Adaptador suporta apenas USB 2.0 | Trocar por um adaptador USB 3.2 Gen 2×2 |
| Conflito entre Wi-Fi 7 integrado e externo | Conflito de roteamento | Executar `sudo nmcli radio wifi off` para desativar o WiFi integrado antes de usar o externo |
| Wi-Fi não visível no container aiGeni | Problema de configuração de rede do container | Usar `--network=host`; ou conectar ao host OS e permitir que o container compartilhe a rede |
| Não é possível usar a frequência de 6GHz | Restrição de Domínio Regulatório | Executar `sudo iw reg set US`; confirmar as últimas regulamentações |

## 9. Restrições Conhecidas

- Necessidade de conversor USB Type-C: Além do AXML, todos os adaptadores de rede ALFA necessitam de conversor USB-C to USB-A
- Tradução manual de chipsets Realtek: RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU não foram incluídos no mainline
- Possível conflito com Wi-Fi 7 integrado: BrainSphere já inclui Wi-Fi 7 + BT 5.4
- Configuração manual do modo AP: O DGX OS é pré-configurado como ambiente de desenvolvimento
- Restrições regulatórias de 6GHz: A disponibilidade do Wi-Fi 6E depende da região regulatória
- Dependência de atualizações de drivers: Drivers out-of-tree da Realtek são mantidos pela comunidade, e após atualizações do kernel, é necessário recompilar
- Isolamento de contêineres aiGeni: Se usar WiFi em contêineres aiGeni, atenção deve ser dada ao espaço de nomes de rede e ao montagem de dispositivos; é recomendável gerenciar WiFi no nível do host OS
- Diferenças de software Altos não afetam a compatibilidade: aiGeni é uma plataforma de camada de aplicativo, não afetando a compatibilidade do driver de WiFi USB do kernel

Condições de refutação: As seguintes avaliações são baseadas no DGX OS (baseado em Ubuntu, kernel 6.x). Se o Altos mudar para uma base de sistema operacional não Ubuntu ou se houver variação na versão major do kernel do DGX OS, a verificação de in-kernel / out-of-tree deve ser refeita.

## 10. Fontes de Referência URL

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| Folheto Oficial do Product Sheet do ALTOS BrainSphere GB10 F1 | Especificações de Hardware (170W / 50mm / Configuração USB) | https://www.altoscomputing.com/filepic/pdf/Altos_BrainSphere_GB10_F1_Product_Sheet_TW.pdf | ✅ Verificado | 2026-09-03 |
| Site Oficial da Altos Computing | Informações sobre o Produto BrainSphere GB10 F1 | https://www.altoscomputing.com/en-Us | ✅ Verificado | 2026-09-03 |
| Página Oficial do NVIDIA DGX Spark | Informações sobre a Plataforma GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Driver RTL8812AU para Linux | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| Catálogo de Produtos da ALFA Network (Yupitek) | Especificações dos Produtos Atuais da ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |

Artigos Relacionados: [A Placa de Rede sem Fio ALFA suporta o NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[A Placa de Rede sem Fio ALFA suporta o ASUS Ascent GX10?](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[A Placa de Rede sem Fio ALFA suporta o GIGABYTE AI TOP ATOM?](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[A Placa de Rede sem Fio ALFA suporta o MSI EdgeXpert?](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)

Declaração de Isenção de Responsabilidade: A determinação de compatibilidade deste artigo é baseada no NVIDIA DGX OS pré-instalado no ALTOS BrainSphere GB10 F1 (kernel 6.x, aarch64). O BrainSphere e o DGX Spark compartilham a mesma plataforma de hardware, com compatibilidade completa. O Altos aiGeni é um software de camada de aplicação, que não afeta a compatibilidade do driver. O driver de chip MediaTek é do Linux mainline, com alta estabilidade; o driver de chip Realtek é mantido pela comunidade. O BrainSphere já possui Wi-Fi 7, e o uso do ALFA externo é principalmente para testes de penetração ou necessidades de chip específicas.
