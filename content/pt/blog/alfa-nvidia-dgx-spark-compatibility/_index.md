---
title: "Suporte do Adaptador de Rede Wireless ALFA para NVIDIA DGX Spark (GB10)"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-dgx-spark-compatibility"
tags:
  - "ALFA"
  - "NVIDIA"
  - "DGX-Spark"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "Guia de Hardware"
description: "DGX Spark com NVIDIA DGX OS, compatibilidade ALFA com Linux, drivers in-kernel para MediaTek, out-of-tree para Realtek, USB-C to USB-A required."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumo do Problema

Pergunta do cliente: “O adaptador de rede sem fio USB da série ALFA pode ser utilizado no supercomputador pessoal AI NVIDIA DGX Spark (GB10 Grace Blackwell)?”

Conclusão resumida: O DGX Spark executa o NVIDIA DGX OS (baseado no Ubuntu, kernel 6.x), e a compatibilidade do adaptador de rede ALFA é semelhante à de sistemas de desktop modernos do Linux. Os modelos de chip MediaTek (AWUS036ACM / ACHM / AXML / AXM) utilizam o driver in-kernel, são prontos para uso; os modelos de chip Realtek (AWUS036ACH / ACS / EACS / AX / AXER) requerem a compilação do driver out-of-tree (arquitetura ARM64 / aarch64). Atenção: todos os ports USB do DGX Spark são do tipo USB Type-C, enquanto os adaptadores de rede ALFA são do tipo USB Type-A, portanto, é necessário usar um adaptador USB-C to USB-A ou um cabo de transmissão.

Critérios de avaliação: Os 9 adaptadores de rede USB da ALFA em serviço (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Análise da Arquitetura de Especificações de Hardware de Objetivo

### 2.1 Especificações de Hardware do NVIDIA DGX Spark

| Item | Especificação |
|---|---|
| Nome do Produto | NVIDIA DGX Spark |
| Chip de Núcleo | NVIDIA GB10 Grace Blackwell Superchip |
| CPU | 20-core Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Arquitetura Blackwell da NVIDIA, 6144 núcleos CUDA, Cincoª Geração Tensor Core, Quartoª Geração RT Core |
| Desempenho de IA | Até 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| Memória do Sistema | 128GB LPDDR5x Memória Unificada (256-bit, 273 GB/s) |
| Armazenamento | Até 4TB NVMe M.2 SSD (加密 auto) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (20Gbps), onde 1 suporta entrada PD (180W EPR PD3.1) |
| Saída de Vídeo | 1× HDMI 2.1a |
| Rede com Fio | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (200G QSFP) |
| Rede sem Fio | Wi-Fi 7 (interno) + Bluetooth 5.4 |
| Sistema Operacional | NVIDIA DGX OS (baseado em Ubuntu Linux, kernel 6.x) |
| Arquitetura | aarch64 (ARM64) |
| Tamanho | 150 × 150 × 50.5 mm (1.13L) |
| Peso | Aproximadamente 1.2 kg |
| Alimentação | Fonte de alimentação USB-C de 240W |

### 2.2 Ambiente de Software: NVIDIA DGX OS

| Item | Descrição |
|---|---|
| Base | Ubuntu Linux (personalizado pela NVIDIA) |
| Kernel | Linux 6.x (versão específica conforme atualização do DGX OS) |
| Arquitetura | aarch64 (ARM64) |
| Software Pré-instalado | NVIDIA AI Software Stack (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Gestão de Pacotes | apt (sistema Debian/Ubuntu) |
| Framework de Drivers | Arquitetura de driver do kernel Linux padrão (cfg80211 / mac80211) |

### 2.3 Características Chave: Kernel Moderno + ARM64

O ambiente de software do DGX Spark tem dois impactos principais na compatibilidade com as placas de rede ALFA:

- Kernel 6.x (moderno): Todos os drivers de WiFi que entram no mainline podem ser usados diretamente, incluindo mt76 (MT7612U / MT7610U) e mt7921u (MT7921AUN). Isso contrasta marcadamente com o kernel 4.9 do Jetson Nano.
- Arquitetura ARM64 (aarch64): Drivers out-of-tree da Realtek (8812au / 8821cu / rtl8852bu) precisam ser compilados no ARM64. O upstream desses drivers (morrownr) já suporta compilação no ARM64, mas é necessário confirmar que CONFIG_PLATFORM_ARM64 = y no Makefile.

### 2.4 Necessidade de Conversor USB Type-C

Os 4 conectores USB do DGX Spark são Type-C, enquanto a linha completa de placas de rede ALFA (exceto AXML que é USB-C) utiliza interface USB Type-A:

| Modelo | Especificação de Interface | Precisa de Conversor |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ Não precisa de conversor (pode ser inserido diretamente) |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ Precisa de USB-C to USB-A |
| AWUS036AX | USB Type-A / USB 3.2 | ✅ Precisa |
| AWUS036AXER | USB Type-A / USB 3.2 | ✅ Precisa |
| AWUS036ACH | USB Type-A / USB 3.0 | ✅ Precisa |
| AWUS036ACHM | USB Type-A / USB 2.0 | ✅ Precisa |
| AWUS036ACM | USB Type-A / USB 3.0 | ✅ Precisa |
| AWUS036ACS | USB Type-A / USB 2.0 | ✅ Precisa |
| AWUS036EACS | USB Type-A / USB 2.0 | ✅ Precisa |

Recomendação: Use um conversor ou linha de transmissão USB-C to USB-A compatível com USB 3.2 Gen 2×2 (20Gbps) para garantir que os modelos AWUS036ACH / ACM / AX etc. que utilizam USB 3.x possam operar a plena velocidade.

## 3. Análise das Especificações e Chipsets da Placa de Rede ALFA

Até setembro de 2026, a linha de produtos de placas de rede USB sem fio da ALFA Network é a seguinte (baseada em 9 modelos):

| Modelo | Nível Wi-Fi | Chipset | Interface | Status do Driver Linux |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel (mt7921u, kernel 5.19+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel (mt7921u) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 (kernel 5.16+, suporte USB gradualmente integrado) ou out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Conforme acima |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree (morrownr/8812au, necessita de compilação ARM64) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel (mt76x2u)⭐ Recomendado |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree (8812au cobre) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree (morrownr/8821cu) |

## 4. Modelos Aplicáveis e Chipsets

### 4.1 Classificação de Recomendação

| Nível de Recomendação | Modelo (Chipset) | Descrição |
|---|---|---|
| ⭐ Recomendação Forte | AWUS036ACM (MT7612U) | Driver in-kernel, pronto para usar, AC1200 dual-band, suporta AP / Monitor / Injection |
| ✅ Recomendado | AWUS036ACHM (MT7610U) | Driver in-kernel, baixo consumo de energia, AC433 dual-band |
| ✅ Recomendado (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | Driver in-kernel, Wi-Fi 6E, AXML com conector USB-C direto |
| ⚠️ Disponível mas requer compilação | AWUS036ACH (RTL8812AU) | Requer compilação do morrownr/8812au (ARM64), após a compilação, todas as funcionalidades estão completas (inclusive Monitor / Injection) |
| ⚠️ Disponível mas requer compilação | AWUS036ACS (RTL8811AU) | Coberto pelo driver 8812au |
| ⚠️ Disponível mas requer atenção | AWUS036EACS (RTL8811CU) | Requer compilação do morrownr/8821cu (ARM64) |
| ⚠️ Disponível mas requer atenção | AWUS036AX / AXER (RTL8832BU) | O kernel 6.x do rtw89 pode já suportar USB; se não for necessário compilar out-of-tree |

### 4.2 Sugestões de Uso

| Cenário de Uso | Modelo Recomendado | Descrição |
|---|---|---|
| Acesso Wireless Básico (muito simples) | AWUS036ACM / ACHM | Driver in-kernel, sem compilação, pronto para usar |
| Teste de Penetração / Monitoramento / Injeção de Wireless | AWUS036ACH ou AWUS036ACM | Ambos suportam Monitor + Injection; ACH requer compilação, ACM pronto para usar |
| Wi-Fi 6E / Frequência de 6GHz | AWUS036AXML / AXM | Driver in-kernel MT7921AUN, suporte completo do kernel 6.x |
| Usuários que já possuem AWUS036ACH e desejam continuar usando | AWUS036ACH | Basta compilar o driver ARM64 para obter funcionalidades completas |
| Não necessita de WiFi externo (usando interno) | — | DGX Spark já possui Wi-Fi 7 + Bluetooth 5.4, não é necessário usar cartão ALFA para acessar a internet |
  
Nota: DGX Spark já possui Wi-Fi 7 + Bluetooth 5.4, não é necessário usar cartão ALFA para acessar a internet em cenários comuns. A principal necessidade de usar cartão ALFA é para testes de penetração (monitoramento/injeção), necessidades específicas de chipsets ou cenários onde o Wi-Fi interno não é suficiente.

## 5. Requisitos de Ambiente

### 5.1 Requisitos de Hardware

| Item | Requisito |
|---|---|
| Conector USB | Conector USB-C para USB-A ou cabo de transmissão (exceto AXML) |
| Alimentação | Fonte de alimentação USB-C de 240W original DGX Spark (suficiente alimentação no porta USB) |
| Refrigeração | Refrigeração original suficiente (o Wi-Fi USB não aumenta significativamente a carga do sistema) |

### 5.2 Requisitos de Software

| Item | Requisito |
|---|---|
| Versão do DGX OS | Qualquer versão em serviço (kernel 6.x) |
| Ferramentas de Compilação (necessárias para o chip Realtek) | build-essential, git, bc, dkms |
| Ferramentas de Gestão de Wireless | iw, wpa_supplicant, network-manager (instalado por padrão no DGX OS) |
| Rede | Rede com fio durante a compilação do driver (10GbE) ou Wi-Fi 7 integrado |

## 6. Determinação de Compatibilidade

### Matriz de Compatibilidade entre Modelos Atuais do ALFA × NVIDIA DGX Spark (GB10)

| Modelo | Chipset | Método de Driver | Detecção de USB | STA de Internet | Modo AP | Monitor | Dificuldade de Instalação | Avaliação Geral |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel (mt76x2u) | ✅ | ✅ | ✅ | ✅ | Sem instalação | ⭐ Melhor |
| AWUS036ACHM | MT7610U | in-kernel (mt76x0u) | ✅ | ✅ | ✅ | ⚠️ Limitado | Sem instalação | ✅ Bom |
| AWUS036AXML | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ Limitado | Sem instalação | ✅ Bom |
| AWUS036AXM | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ Limitado | Sem instalação | ✅ Bom |
| AWUS036ACH | RTL8812AU | out-of-tree (8812au) | ✅ | ✅ | ✅ | ✅ | Médio (compilação) | ⚠️ Utilizável |
| AWUS036ACS | RTL8811AU | out-of-tree (8812au) | ✅ | ✅ | ⚠️ | ❌ | Médio (compilação) | ⚠️ Utilizável |
| AWUS036EACS | RTL8811CU | out-of-tree (8821cu) | ✅ | ⚠️ | ❌ | ❌ | Médio (compilação) | ⚠️ Utilizável |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Médio-Alto | ⚠️ Utilizável |
| AWUS036AXER | RTL8832BU | Igual ao acima | ✅ | ⚠️ | ⚠️ | ❌ | Médio-Alto | ⚠️ Utilizável |

Critérios de Determinação: Disponibilidade do driver mainline do kernel 6.x do DGX OS + suporte do driver morrownr para ARM64. Os chipsets MediaTek, devido ao driver já estar no mainline, são prontos para uso no kernel 6.x sem a necessidade de instalação. Os chipsets Realtek requerem a compilação do driver out-of-tree, mas a compilação para ARM64 já é suportada pelo upstream.

## 7. Detalhamento Extremo de Passo a Passo para Configuração

### 7.1 Pré-requisitos

**Passo 1: Inicie e faça login no DGX Spark** (através de SSH ou conexão direta teclado-tela)

```bash
ssh username@<dgx-spark-ip>
```

**Passo 2: Verifique a Arquitetura do Sistema e a Versão do Kernel**

```bash
uname -m
# Esperado: aarch64
uname -r
# Esperado: 6.x.x (kernel do DGX OS)
```

**Passo 3: (Necessário para chipsets Realtek) Instale as ferramentas de compilação**

```bash
sudo apt update
sudo apt install -y build-essential git bc dkms
```

### 7.2 Rota A: Modelos com Chipset MediaTek (AWUS036ACM / ACHM / AXML / AXM) — Pronto para Uso

**Passo 1: Insira a Placa de Rede**

Use um adaptador USB-C to USB-A para (AXML pode ser inserido diretamente no conector USB-C), insira a placa de rede ALFA na porta USB do DGX Spark.

**Passo 2: Confira se a placa de rede foi detectada**

```bash
lsusb
# Saída esperada (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Passo 3: Confira se a interface de rede foi automaticamente configurada**

```bash
ip link show
# Esperado: wlan0 ou wlp... (driver carregado automaticamente no kernel)
```

**Passo 4: Escaneie redes WiFi**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**Passo 5: Conecte-se à rede WiFi (usando NetworkManager**)

```bash
nmcli dev wifi list
nmcli dev wifi connect "nome_da_sua_rede_wifi" password "senha_da_sua_rede_wifi"
```

**Passo 6: (Opcional) Ative o Modo Monitoramento**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info
```

### 7.3 Rota B: Modelos com Chipset Realtek (AWUS036ACH / ACS / EACS) — Necessita de Compilação

Tomando como exemplo o AWUS036ACH (RTL8812AU):

**Passo 1: Baixe o Código Fonte do Driver**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**Passo 2: Confira as Opções de Compilação para ARM64**

Edite o Makefile, confira `CONFIG_PLATFORM_ARM64 = y` (a maioria das versões novas detecta automaticamente a aarch64).

**Passo 3: Compile e Instale**

```bash
make
sudo make install
sudo modprobe 8812au
```

**Passo 4: Insira a Placa de Rede ALFA (através de adaptador USB-C to USB-A), confira a interface**

```bash
ip link show
# Esperado: wlan0
```

**Passo 5: Conecte-se da Mesma Forma que no Passo 5 da Rota 7.2 (usando nmcli**)

**Passo 6: (Opcional) Modo Monitoramento e Injeção**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

### 7.4 Rota C: Modelos Wi-Fi 6 (AWUS036AX / AXER, RTL8832BU)

**Passo 1: Verifique se o kernel já possui suporte para rtw89 USB**

```bash
# Verifique após inserir a placa de rede
lsusb
dmesg | grep -i "rtw89\|rtl8852\|8832"
ip link show
# Se wlan0 aparecer automaticamente, o rtw89 no kernel 6.x já suporta, você pode usá-lo diretamente
```

**Passo 2: Se o kernel não suportar automaticamente, compile o driver out-of-tree**

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
# Confira CONFIG_PLATFORM_ARM64 = y
make
sudo make install
sudo modprobe rtl8852bu
```

## 8. Erros Comuns e Solução

| Sintomas | Possíveis Causas | Forma de Solução |
|---|---|---|
| O comando `lsusb` não mostra a placa de rede ALFA | Adaptador USB-C defeituoso / Falta de contato | Trocar o adaptador USB-C to USB-A; Verificar se o adaptador suporta transmissão de dados (não apenas carregamento); Tentar diferentes portas USB-C |
| O chip MediaTek, após ser inserido, não possui interface wlan | Módulo do kernel não foi carregado automaticamente / Firmware faltando | Carregar manualmente: `sudo modprobe mt76x2u`; Verificar `dmesg | grep mt76`; Instalar firmware: `sudo apt install linux-firmware` |
| O driver da Realtek está retornando erro no make `aarch64-linux-gnu-gcc: not found` | Configuração de cross-compilação incorreta | Confirmar que a compilação é nativa no DGX Spark (não cross-compilação); Não deve haver configuração de CROSS_COMPILE no Makefile |
| O comando `modprobe 8812au` está retornando "Operation not permitted" | Secure Boot / Assinatura do módulo | O DGX Spark tem o Secure Boot desativado por padrão; Se estiver ativado, é necessário assinar o módulo ou desativar o Secure Boot |
| Conexão WiFi instável / lenta | O adaptador USB-C suporta apenas USB 2.0 | Trocar o adaptador que suporta USB 3.2 Gen 2×2; Verificar se o adaptador está marcado como "Data" e não "Charge Only" |
| O Wi-Fi integrado e o ALFA externo se interferem | Colisão entre duas interfaces sem fio | Desativar o Wi-Fi integrado: `sudo nmcli radio wifi off` ou desativar no BIOS/UEFI; ou configurar a prioridade de roteamento |
| O 6GHz (Wi-Fi 6E) não pode ser usado | Restrição de Domínio Regulatório | Definir o domínio regulatório: `sudo iw reg set US` (6GHz aberto nos EUA); Confirmar que o firmware do AWUS036AXML/AXM suporta 6GHz |
| O modo AP falha ao ser iniciado | Conflito entre NetworkManager e hostapd | Consultar o Guia de Soft AP da Yupitek ALFA; Desativar o NetworkManager para gerenciar a interface após a configuração manual do hostapd |
| A placa de rede desaparece após o despertar | Suspensão automática do USB | Desativar a suspensão automática do USB: `echo 'options usbcore autosuspend=-1' | sudo tee /etc/modprobe.d/usb.conf` |

## 9. Limitações Conhecidas

- **Requisito de Conversão USB Type-C**: Além do AXML, todas as placas de rede ALFA necessitam de adaptador USB-C to USB-A, a qualidade do adaptador pode afetar o desempenho e a estabilidade.
- **Tradução Manual do Chip Realtek**: RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU não estão no mainline, necessitando de tradução out-of-tree no ARM64.
- **Possível Conflito com Wi-Fi Externo**: O DGX Spark já possui Wi-Fi 7 integrado, e ao usar Wi-Fi interno e externo ao mesmo tempo, podem ocorrer conflitos de roteamento ou recursos.
- **Configuração Manual do Modo AP**: O DGX OS é pré-configurado para ambiente de desenvolvimento, e o modo热点 AP requer instalação e configuração manual de hostapd / dnsmasq.
- **Restrições Regulamentares de 6GHz**: A disponibilidade da faixa de 6GHz do Wi-Fi 6E depende das configurações regulamentares da região, a situação de abertura da 6GHz em Taiwan deve ser confirmada conforme a legislação mais recente.
- **Dependência de Atualizações de Driver**: O driver out-of-tree do Realtek é mantido pela comunidade (morrownr), após a atualização do kernel do DGX OS, pode ser necessário recompilar.
- **Diferenças nas Funções de Teste de Penetração**: A função de injecção da série MediaTek mt76 foi melhorada no kernel 6.x, mas o Realtek 8812au continua sendo a escolha tradicional da comunidade de testes de penetração.
- **Função Bluetooth**: A função Bluetooth 5.2 do AWUS036AXM não foi amplamente validada no DGX OS (o DGX Spark já possui BT 5.4 integrado).
- ⚠️ **Sugestão Pública do Mantenedor do Driver RTL8832BU (AWUS036AX/AXER)**: O mantenedor do driver, morrownr, declarou oficialmente que a série rtl8852/32au "é um driver péssimo, suspeitando de problemas no próprio chip", recomendando que os usuários Linux evitem usá-lo no momento (fonte: Capítulo 10). A classificação "⚠️ Utilizável mas com Cuidado" destes modelos nos Capítulos 4 e 6 deve ser entendida como um consenso da indústria que desaconselha, e não apenas um problema de dificuldade de instalação.
- **Informação de 2026 Inicial sobre RTL8812AU "out-of-tree"**: Na verdade, o driver in-kernel compatível com o padrão mac80211 deste chip já foi integrado ao mainline no kernel 6.13 e atingiu maturidade a partir do kernel 6.14 (anúncio oficial de morrownr), se o DGX OS usar o núcleo 6.14 ou superior, o AWUS036ACH pode ser utilizado sem necessidade de compilação, recomenda-se que o suporte técnico peça ao cliente para informar `uname -r` antes de responder.

Condições de Refutação: Se a atualização do DGX OS resultar em mudanças na versão do kernel ou no driver do controlador USB, ou se o driver morrownr parar de manter a ramificação ARM64, a matriz de compatibilidade do Capítulo 6 deve ser revisada novamente; se o suporte USB do rtw89 for implementado completamente no kernel 6.x, a classificação do AWUS036AX / AXER pode ser atualizada de "Utilizável mas com Cuidado" para "Utilizável".

## 10. Fontes de Referência URL

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| Página Oficial do NVIDIA DGX Spark | Especificações e informações sobre a plataforma DGX Spark | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| Documentação do NVIDIA DGX | Arquitetura do sistema operacional DGX e versão do kernel | https://docs.nvidia.com/dgx/dgx-spark | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Driver RTL8812AU para Linux (suporte ARM64) | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| morrownr/8821cu GitHub | Driver RTL8811CU para Linux | https://github.com/morrownr/8821cu-20210916 | ✅ Verificado | 2026-09-03 |
| morrownr/rtl8852bu GitHub | Driver RTL8832BU para Linux | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Verificado | 2026-09-03 |
| Documentação do driver mt76 do kernel Linux | Descrição do driver MediaTek mt76 / mt7921 mainline (versão inicial do kernel suportada por cada chip) | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ Verificado | 2026-09-03 |
| Guia de Soft AP WiFi Hotspot Linux do ALFA (Yupitek) | Guia de configuração do modo AP no Linux para o ALFA | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verificado | 2026-09-03 |
| Catálogo de Produtos da ALFA Network (Yupitek) | Especificações dos produtos atuais da ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |
| Issue #314 do morrownr/USB-WiFi | Declaração oficial do mantenedor do driver: Recomendação de evitar o chip rtl8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Verificado | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | Anúncio mais recente sobre o estado do driver RTL8812AU (inclusão na linha principal do kernel 6.13, maturidade de qualidade no 6.14) | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |

Artigos Relacionados: [O adaptador Wi-Fi ALFA suporta o MSI EdgeXpert?](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)｜[O adaptador Wi-Fi ALFA suporta o ASUS Ascent GX10?](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[O adaptador Wi-Fi ALFA suporta o ALTOS BrainSphere GB10 F1?](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[O adaptador Wi-Fi ALFA suporta o GIGABYTE AI TOP ATOM?](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[O adaptador Wi-Fi ALFA suporta o NVIDIA Jetson Nano?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Declaração de Isenção de Responsabilidade: A determinação de compatibilidade deste artigo é baseada no NVIDIA DGX OS (kernel 6.x, aarch64). Os drivers de chip MediaTek são do mainline do Linux, com alta estabilidade; os drivers de chip Realtek são mantidos pela comunidade (morrownr), e a estabilidade pode variar conforme a versão. O DGX Spark já possui Wi-Fi 7, e o uso de adaptadores ALFA de rede externa é principalmente para testes de penetração ou necessidades de chips específicos. A qualidade do adaptador USB-C afeta diretamente a experiência de uso, recomenda-se a escolha de adaptadores com marca e etiqueta USB 3.2 Gen 2×2.
