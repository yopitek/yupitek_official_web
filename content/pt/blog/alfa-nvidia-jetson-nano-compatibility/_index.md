---
title: "Carta de Suporte do Adaptador de Rede Wireless ALFA para a NVIDIA Jetson Nano"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-jetson-nano-compatibility"
tags:
  - "ALFA"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "NVIDIA"
  - "Jetson-Nano"
  - "JetPack"
  - "ARM64"
  - "Linux-WiFi"
categories:
  - "Guia de Hardware"
description: "Suporte variado para ALFA USB Wi-Fi cards no Jetson Nano, com limitações de kernel e compatibilidade variada."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumo do Problema

Pergunta do cliente: “O adaptador USB sem fio da série ALFA pode ser utilizado no desenvolvimento com a placa NVIDIA Jetson Nano?”

Conclusão breve: O Jetson Nano pode usar a maioria dos adaptadores da série ALFA, mas a limitação principal está no kernel Linux 4.9 da versão 4.x do JetPack, que é mais antigo (avaliação: dos 9 modelos de adaptadores USB da ALFA em serviço, 3 são prontos para uso, 2 requerem compilação avançada, 2 não foram verificados e 2 não são compatíveis). Os modelos com chip Realtek (AWUS036ACH / ACS / EACS) podem ser compilados diretamente com o driver out-of-tree, sendo uma escolha útil para o Jetson Nano; os modelos MediaTek MT7612U / MT7610U precisam de backport ou compilação própria do driver mt76. O modelo MT7921AUN de Wi-Fi 6E (AWUS036AXML / AXM) não é realmente compatível no Jetson Nano, devido à necessidade de kernel 5.19+. Para cenários de teste de penetração, o AWUS036ACH (RTL8812AU) é a primeira escolha; para cenários de navegação geral, o AWUS036ACH (estável) ou o AWUS036ACM (requer compilação mt76) são as primeiras opções.

## 2. Análise da Arquitetura de Especificações de Hardware de Objetivo

### 2.1 Especificações de Hardware do NVIDIA Jetson Nano

| Item | Especificação |
|---|---|
| Módulo | Módulo Jetson Nano (P3448) |
| CPU | Quad-core ARM Cortex-A57 (ARMv8-A / aarch64) |
| GPU | NVIDIA Maxwell arquitetura, 128 núcleos CUDA |
| Memória | 4GB LPDDR4 (64-bit, 25.6 GB/s) |
| Armazenamento | microSD (placa de desenvolvimento) / eMMC (módulo de produção) |
| USB | 4x USB 3.0 Type-A + 1x USB 2.0 Micro-B (Modo Dispositivo / Alimentação) |
| Rede | 1x Gigabit Ethernet (RJ45) |
| Sem fio | Sem WiFi / Bluetooth integrados (necessário adaptador USB ou M.2) |
| Alimentação | Conector DC 5V/4A (recomendado) ou micro-USB 5V/2A |
| Tamanho | 100mm × 80mm (placa de desenvolvimento) |

### 2.2 Ambiente de Software: JetPack 4.x

| Item | Conteúdo |
|---|---|
| Sistema Operacional | Linux for Tegra (L4T), baseado em Ubuntu 18.04 LTS |
| Versão do Kernel | Linux 4.9 (L4T R32.x / JetPack 4.6.x) |
| Arquitetura | aarch64 (ARM64) |
| Compilador | GCC 7.5 (padrão) / GCC 8 (instalável) |
| Versão mais recente | JetPack 4.6.4 (L4T R32.7.4), em manutenção |
| Atualizações posteriores | O Jetson Nano não suporta JetPack 5.x (kernel 5.10) devido a limitações de hardware |

### 2.3 Limitações Críticas: Kernel 4.9

O kernel 4.9 do Jetson Nano é um fator crucial para a compatibilidade:

| Driver | Versão do kernel que entrou no mainline | Disponibilidade no Jetson Nano (kernel 4.9) |
|---|---|---|
| mt76x2u (MT7612U) | 4.19 | ❌ Necessita backport / compilação manual |
| mt76x0u (MT7610U) | 4.19 | ❌ Necessita backport / compilação manual |
| mt7921u (MT7921AUN) | 5.19 | ❌ Inutilizável (diferença muito grande) |
| rtl8812au (RTL8812AU) | Nunca entrou no mainline | ✅ Compilável como driver out-of-tree |
| rtl8821cu (RTL8811CU) | Nunca entrou no mainline | ✅ Compilável como driver out-of-tree |
| rtw89 (RTL8832BU) | 5.16 (PCIe) / USB gradualmente integrado | ❌ Necessita compilação manual, compatibilidade desconhecida |

### 2.4 Limitações de Alimentação via USB

Os 4 portos USB 3.0 Type-A do Jetson Nano compartilham um orçamento de energia:

- Usando alimentação DC (5V/4A), a saída total dos portos USB é aproximadamente 1.5A (5V)
- Usando alimentação micro-USB (5V/2A), a saída total dos portos USB é aproximadamente 0.5A
- Placa de rede ALFA de alta potência (AWUS036ACH) pode alcançar picos de 800mA-1A
- Recomendação: Use alimentação DC + Hub USB 3.0 com alimentação, para evitar interrupções de energia ou reinicializações do sistema devido à falta de energia

## 3. Análise das Especificações da Placa de Rede ALFA e do Chipset

Até setembro de 2026, a linha de produtos de placas de rede USB sem fio da ALFA Network é a seguinte:

| Modelo | Nível Wi-Fi | Chipset | Interface | Compatibilidade com Jetson Nano |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ Requer kernel 5.19+, não disponível |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ Igual acima |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Requer rtl8852bu personalizado, não verificado |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Igual acima |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ Compilado com morrownr/8812au, maduro |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ⚠️ Requer backport mt76x0u |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ⚠️ Requer backport mt76x2u |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ✅ Coberto pelo driver 8812au |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ✅ Compilado com morrownr/8821cu |

## 4. Modelos Aplicáveis e Chipsets

### 4.1 Classificação de Recomendação

| Nível de Recomendação | Modelo (Chipset) | Descrição |
|---|---|---|
| ⭐ Recomendação Forte (Teste de Penetração) | AWUS036ACH (RTL8812AU) | Drivers maduros, suporte a Monitor Mode + Packet Injection, a placa de rede ALFA mais frequentemente usada no Jetson Nano |
| ✅ Recomendação (Navegação Geral) | AWUS036ACH (RTL8812AU) | AC1200, instalação de drivers simples, estável |
| ✅ Recomendação (Baixa Potência) | AWUS036EACS (RTL8811CU) | AC600, baixa potência USB 2.0, adequado para navegação simples |
| ✅ Recomendação (Entrada) | AWUS036ACS (RTL8811AU) | AC433, coberto pelos drivers do 8812au |
| ⚠️ Disponível mas Requer Tradução Manual | AWUS036ACM (MT7612U) | Requer backport do driver mt76 para o kernel 4.9, barreira técnica alta |
| ⚠️ Disponível mas Requer Tradução Manual | AWUS036ACHM (MT7610U) | Como acima, apenas 433Mbps |
| ⚠️ Não Verificado / Não Recomendado | AWUS036AX / AXER (RTL8832BU) | Wi-Fi 6, requer tradução do rtl8852bu, compatibilidade do kernel 4.9 não verificada |
| ❌ Indisponível | AWUS036AXML / AXM (MT7921AUN) | Wi-Fi 6E, requer kernel 5.19+, Jetson Nano não pode ser atualizado |

### 4.2 Sugestões de Uso

| Cenário de Uso | Modelo Recomendado | Descrição |
|---|---|---|
| Teste de Penetração / Monitoramento / Injeção de Pacotes | AWUS036ACH | Drivers RTL8812AU suportam Monitor + Injection, com forte verificação da comunidade |
| Controle Wireless de Robôs / Veículos Autônomos | AWUS036ACH ou AWUS036EACS | Conexão estável, baixa latência |
| Navegação em IoT em Portais | AWUS036EACS / ACS | Baixa potência, USB 2.0 suficiente, economia de energia |
| Navegação de Alta Velocidade em 5GHz | AWUS036ACH | AC1200, 5GHz com 867Mbps |
| Necessidade de Wi-Fi 6 / 6E | ❌ Nenhuma Opção Disponível | Jetson Nano não suporta chipsets Wi-Fi 6/6E modernos |

## 5. Requisitos de Ambiente

### 5.1 Requisitos de Hardware

| Item | Requisitos Mínimos | Recomendação |
|---|---|---|
| Placa de Desenvolvimento Jetson Nano | Versão B01 / A02 | B01 (2 portas CSI de câmera) |
| Fonte de Alimentação | 5V/2A micro-USB | Conector DC de 5V/4A (necessário para dispositivos USB de alta potência) |
| Hub USB | Não necessário | Hub USB 3.0 com energia (usado com adaptadores de alta potência) |
| Refrigeração | Fita de dissipação de calor (inclusa por padrão) | Ventilador + fita de dissipação de calor (para longos períodos de alta carga) |
| Armazenamento | 16GB microSD | 32GB+ UHS-I microSD (necessário para espaço de compilação de drivers) |

### 5.2 Requisitos de Software

| Item | Requisitos |
|---|---|
| Versão do JetPack | 4.6.x (L4T R32.7.x) |
| Ferramentas de Núcleo | build-essential, git, bc, libssl-dev, flex, bison |
| Código Fonte do Kernel | Necessário baixar o código-fonte do kernel correspondente à versão L4T (para compilação do backport mt76) |
| Rede | Conexão de rede via cabo durante a compilação (através da porta Ethernet Gigabit) |

## 6. Determinação de Compatibilidade

### Matriz de Compatibilidade do ALFA Modelos Atuais × NVIDIA Jetson Nano

| Modelo | Chipset | Método de Driver | Detecção de USB | STA Internet | Modo AP | Monitor | Dificuldade de Instalação | Avaliação Geral |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | Tradução 8812au | ✅ | ✅ | ✅ | ✅ | Média | ⭐ Melhor |
| AWUS036ACS | RTL8811AU | Cobertura 8812au | ✅ | ✅ | ⚠️ | ❌ | Média | ✅ Boa |
| AWUS036EACS | RTL8811CU | Tradução 8821cu | ✅ | ⚠️ | ❌ | ❌ | Média | ✅ Boa |
| AWUS036ACM | MT7612U | Backport mt76x2u | ✅ | ✅ | ✅ | ✅ | Alta | ⚠️ Disponível |
| AWUS036ACHM | MT7610U | Backport mt76x0u | ✅ | ✅ | ⚠️ | ⚠️ | Alta | ⚠️ Disponível |
| AWUS036AX | RTL8832BU | Tradução rtl8852bu | ⚠️ | ❌ | ❌ | ❌ | Alta | ❌ Não Recomendado |
| AWUS036AXER | RTL8832BU | Igual ao acima | ⚠️ | ❌ | ❌ | ❌ | Alta | ❌ Não Recomendado |
| AWUS036AXML | MT7921AUN | Necessário kernel 5.19+ | ❌ | ❌ | ❌ | ❌ | — | ❌ Não Disponível |
| AWUS036AXM | MT7921AUN | Igual ao acima | ❌ | ❌ | ❌ | ❌ | — | ❌ Não Disponível |

Critérios de Determinação: Disponibilidade do driver para o kernel 4.9 do Jetson Nano JetPack 4.x + Relatórios de Testes da Comunidade (Fórum do Jetson Nano, Issues do GitHub morrownr driver). MT7921AUN, devido ao Jetson Nano não poder ser atualizado para o kernel 5.19+, é considerado não disponível.

## 7. Detalhado Passo a Passo de Configuração

### 7.1 Pré-requisitos: Atualização do Sistema e Ambiente de Compilação

**Passo 1: Iniciar e Logar no Jetson Nano via SSH**

```bash
ssh username@<ip-do-jetson-nano>
```

**Passo 2: Atualizar os Pacotes do Sistema**

```bash
sudo apt update
sudo apt upgrade -y
```

**Passo 3: Instalar Ferramentas de Compilação e Dependências**

```bash
sudo apt install -y build-essential git bc libssl-dev flex bison dkms
```

**Passo 4: Verificar a Versão do Kernel**

```bash
uname -r
# Saída esperada: 4.9.337-tegra (ou similar a 4.9.x-tegra)
```

### 7.2 Rota A: Modelos de Chipset Realtek (AWUS036ACH / ACS / EACS) — Recomendado

Vamos usar o AWUS036ACH (RTL8812AU) como exemplo:

**Passo 1: Baixar o Código Fonte do Driver**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**Passo 2: (Opcional) Ajustar Parâmetros de Compilação para ARM64**

Edite o Makefile para confirmar a seguinte configuração:

```
CONFIG_PLATFORM_ARM64 = y
```

(Muitas versões mais novas do Makefile já detectam automaticamente a arquitetura aarch64)

**Passo 3: Compilar e Instalar**

```bash
make
sudo make install
```

**Passo 4: Carregar o Módulo do Driver**

```bash
sudo modprobe 8812au
# Ou reiniciar
sudo reboot
```

**Passo 5: Inserir a Placa de Rede ALFA e Confirmar a Interface de Rede**

```bash
ip link show
# Saída esperada: wlan0 (se não aparecer, verifique dmesg)
dmesg | grep -i "8812au\|rtl8812\|usb"
```

**Passo 6: Escanear Redes WiFi (Verificação de Funcionalidade)**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**Passo 7: Conectar à Rede WiFi (usando NetworkManager / nmcli)**

```bash
# O Jetson Nano já instala o NetworkManager por padrão
nmcli dev wifi list
nmcli dev wifi connect "nome-da-sua-WiFi" password "senha-da-sua-WiFi"
```

**Passo 8: (Opcional) Configurar como Ponto de Acesso (Soft AP)**

```bash
# Instalar hostapd e dnsmasq
sudo apt install -y hostapd dnsmasq
# Consulte a Guia de Soft AP ALFA para configuração
# https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/
```

**Passo 9: Ativar o Modo de Escuta (para Testes de Penetração)**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# Verificação
sudo iw dev wlan0 info
# type deve exibir monitor
# Teste de injetor de pacotes
sudo aireplay-ng --test wlan0
```

### 7.3 Rota B: Modelos de Chipset MediaTek (AWUS036ACM / ACHM) — Avançado

Vamos usar o AWUS036ACM (MT7612U) como exemplo, é necessário backportar o driver mt76:

**Passo 1: Baixar o Código Fonte do Kernel do Jetson Nano**

```bash
# Baixe o código-fonte do kernel correspondente à versão do L4T
# Por exemplo, para L4T R32.7.4:
wget https://developer.nvidia.com/embedded/l4t/r32_release_v7.4/sources/public_sources.tbz2
tar -xjf public_sources.tbz2
cd Linux_for_Tegra/source/public
tar -xjf kernel_src.tbz2
```

**Passo 2: Preparar o Ambiente de Compilação do Kernel**

```bash
cd kernel/kernel-4.9
# Gerar configuração padrão
make tegra_defconfig
# Ativar opções mt76 relacionadas (menuconfig)
make menuconfig
# Navegue até: Device Drivers > Network device support > Wireless LAN
# Selecione: <M> MediaTek MT76x2U USB support
# Selecione: <M> MediaTek MT76x0U USB support
```

**Passo 3: Compilar os Módulos do Kernel**

```bash
make modules_prepare
make M=drivers/net/wireless/mediatek/mt76 modules
```

**Passo 4: Instalar os Módulos**

```bash
sudo make M=drivers/net/wireless/mediatek/mt76 modules_install
sudo depmod -a
```

**Passo 5: Carregar o Driver**

```bash
sudo modprobe mt76x2u
# Inserir AWUS036ACM
dmesg | grep mt76
ip link show
```

⚠️ Atenção: Backportar mt76 para o kernel 4.9 pode encontrar erros de compilação e pode ser necessário corrigir o código-fonte manualmente. Esta é uma operação avançada e é recomendado apenas para usuários com experiência em compilação de kernel. Em caso de dificuldades, é recomendado usar AWUS036ACH (RTL8812AU).

### 7.4 Rota C: Modelos Wi-Fi 6 / 6E (AWUS036AX / AXER / AXML / AXM)

- AWUS036AXML / AXM (MT7921AUN): Não disponível. O kernel 4.9 do Jetson Nano não pode ser atualizado para 5.19+, e o driver mt7921u não pode ser backportado (diferença muito grande, depende de infraestrutura de kernel moderno).
- AWUS036AX / AXER (RTL8832BU): Não recomendado. Teoricamente, é possível tentar compilar o driver morrownr/rtl8852bu, mas a compatibilidade com o kernel 4.9 não foi verificada pela comunidade e as funcionalidades Wi-Fi 6 podem não funcionar corretamente. Se for necessário Wi-Fi 6, é recomendado usar o Jetson Orin Nano (JetPack 5.x, kernel 5.10+) ou computador x86.

## 8. Erros Comuns e Solução

| Sintoma | Possível Causa | Solução |
|---|---|---|
| Após a inserção da placa de rede, o dmesg não exibe nenhuma reação | Falta de alimentação USB / Contato inadequado | Usar alimentação DC (5V/4A); Trocar o porta USB; Usar Hub USB com alimentação |
| Erro ao compilar 8812au com make: gcc: erro: opção de linha de comando não reconhecida | Versão do GCC muito antiga | Instalar GCC 8: `sudo apt install gcc-8 g++-8` e especificar `CC = gcc-8` no Makefile |
| modprobe 8812au informa Required key not available | Boot Seguro ativado (o Jetson Nano geralmente não tem esse problema) | Verificar se o Jetson Nano não tem Boot Seguro ativado; reassinar o módulo ou desativar o Boot Seguro |
| A interface wlan0 aparece mas não consegue scanear AP | Domínio Regulatório não configurado / Faltando driver de firmware | Configurar o domínio regulatório: `sudo iw reg set TW`; Verificar se há erro de carregamento do firmware no dmesg |
| No modo de alta potência, o sistema reinicia ou a placa de rede desliga | Falta de alimentação USB | Usar alimentação DC + Hub USB com alimentação; Reduzir o TX Power: `sudo iw dev wlan0 set txpower fixed 2000` |
| No modo de escuta, o aireplay-ng --test exibe Injection is working! mas o ataque é ineficaz | Funcionalidade de injecção do driver limitada / Colisão de canais | A funcionalidade de injecção do RTL8812AU é básica; Confirmar se `airmon-ng check kill` parou o NetworkManager; Tente diferentes canais |
| Falha na compilação do mt76 backport | Diferença grande entre o kernel 4.9 e o código-fonte original do mt76 | Tentar usar uma versão mais antiga do mt76 (correspondente ao commit da época do kernel 4.19); ou usar AWUS036ACH |
| A placa de rede desaparece após o despertar do sistema | Configuração de economia de energia USB | Desativar a suspensão automática USB: `echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |
| O 5GHz do AWUS036ACH não pode ser usado | Restrições de domínio regulatório / Tabela de canais do driver | Configurar `sudo iw reg set US` (domínio regulatório dos EUA abre mais canais de 5GHz); Confirmar se o canal usado está dentro do escopo permitido pelas regulamentações locais |

## 9. Limitações Conhecidas

- Versão do Kernel congelada em 4.9: O Jetson Nano não suporta o JetPack 5.x, impossibilitando a atualização do kernel, o que é a raiz de todos os problemas de compatibilidade
- MT7921AUN (Wi-Fi 6E) completamente inutilizável: Requer kernel 5.19+, não pode ser backported para 4.9
- Chip MediaTek mt76 precisa de backport manual: Usuários de AWUS036ACM / ACHM precisam compilar manualmente o módulo do kernel, com alto nível técnico
- ⚠️ **Mantenedor do driver Wi-Fi 6 (RTL8832BU) recomendou evitar seu uso**: O mantenedor morrownr em sua publicação oficial destacou que a série rtl8852/32au é "muito ruim", suspeitando de problemas no próprio chip, e recomendou que os usuários do Linux evitem este chip (fonte: Capítulo 10). Isso é mais grave do que simplesmente "compatibilidade do kernel 4.9 não verificada"; a avaliação de AWUS036AX / AXER neste documento e em outros documentos deve ser entendida como "não recomendado" em vez de "pode ser tentado, mas complicado"
- Limitações de alimentação via USB: Quatro portas USB compartilham aproximadamente 1.5A (alimentação DC), e placas de rede de alta potência precisam usar hubs com alimentação
- Desempenho em modo AP: A capacidade do CPU do Jetson Nano é limitada, e a taxa de transferência do Wi-Fi USB pode ser inferior ao esperado ao operar em modo AP
- Diferenças em funções de monitoramento/injeção: RTL8812AU oferece o melhor suporte; as funções de injeção dos chips MediaTek após o backport do kernel 4.9 podem ser instáveis
- Manutenção a longo prazo: O JetPack 4.x já entrou em modo de manutenção, não haverá novas funcionalidades ou atualizações de drivers no futuro
- Funcionalidade Bluetooth: A funcionalidade Bluetooth 5.2 do AWUS036AXM não foi verificada no Jetson Nano (requer suporte do BlueZ)
- Refrigeração: Ao usar o Wi-Fi USB de alta potência por longos períodos, a temperatura total do Jetson Nano pode aumentar, recomenda-se a instalação de ventiladores

Contra-indicações: As avaliações acima são baseadas no JetPack 4.6.x (kernel 4.9). Se a NVIDIA liberar suporte do JetPack 5.x para o Jetson Nano no futuro (atualmente não oficialmente suportado) ou se a comunidade desenvolver um backport estável do kernel 5.x, a avaliação de inutilização descrita no Capítulo 4 precisará ser revalidada.

## 10. Fontes de Referência URL

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| Página Oficial do NVIDIA Jetson Nano | Especificações de Hardware do Jetson Nano | https://developer.nvidia.com/embedded/jetson-nano | ✅ Verificado | 03/09/2026 |
| Página Oficial do NVIDIA JetPack SDK | Informações sobre a Versão do JetPack e do Kernel | https://developer.nvidia.com/embedded/jetpack | ✅ Verificado | 03/09/2026 |
| morrownr/8812au GitHub | Driver RTL8812AU Linux (compatível com Jetson Nano) | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 03/09/2026 |
| morrownr/8821cu GitHub | Driver RTL8811CU Linux | https://github.com/morrownr/8821cu-20210916 | ✅ Verificado | 03/09/2026 |
| Guia de Linux para ALFA Soft AP WiFi Hotspot (Yupitek) | Configuração em Modo AP do ALFA no Linux | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verificado | 03/09/2026 |
| Catálogo de Produtos da ALFA Network (Yupitek) | Especificações dos Produtos Atuais da ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 03/09/2026 |
| Issue #314 do morrownr/USB-WiFi | Declaração Oficial do Mantenedor do Driver: Recomendação de Evitar o Chip rtl8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Verificado | 03/09/2026 |
| Discussão #292 do morrownr/USB-WiFi | mt7921u.ko só aparecerá no núcleo com kernel 5.19+ (palavra original do mantenedor do driver) | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ Verificado | 03/09/2026 |

Artigos Relacionados: [O Cartão de Rede sem Fio ALFA suporta o NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/) (Comparação com a Plataforma GB10, ambiente de kernel 6.x) | [O Cartão de Rede sem Fio ALFA suporta o OpenWrt?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)

Declaração de Isenção de Responsabilidade: A determinação de compatibilidade deste artigo é baseada no Jetson Nano JetPack 4.6.x (kernel 4.9). Os drivers para o chip Realtek são mantidos pela comunidade (morrownr), e a estabilidade pode variar conforme a versão. A operação de backport para o chip MediaTek mt76 requer experiência em compilação de kernel e não há garantia de 100% de sucesso. Para suporte a Wi-Fi 6/6E ou kernel moderno, é recomendável atualizar para a série Jetson Orin (JetPack 5.x+) ou usar computadores x86.
