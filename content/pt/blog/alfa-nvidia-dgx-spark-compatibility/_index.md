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
description: "As 9 placas USB ALFA no NVIDIA DGX Spark (GB10): testadas no ASUS GX10 (kernel 6.17), usam driver nativo sem DKMS; EACS/ACH/ACS injetam bem e AXM/AXML falham."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Este artigo foi atualizado com os testes no GX10 de novembro de 2026: no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), as 9 placas de rede ALFA atuais usam todas drivers nativos do kernel, funcionam ao conectar e não precisam de DKMS. Dados completos em [Tabela de testes ARM64 das 9 placas de rede ALFA](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Testado apenas no GX10; os demais modelos GB10 não foram testados um a um.

## 1. Resumo do Problema

Pergunta do cliente: “O adaptador de rede sem fio USB da série ALFA pode ser utilizado no supercomputador pessoal AI NVIDIA DGX Spark (GB10 Grace Blackwell)?”

Conclusão resumida: O DGX Spark executa o NVIDIA DGX OS (baseado no Ubuntu, kernel 6.x). Testamos no ASUS GX10, que também usa a plataforma GB10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), os 9 adaptadores de rede USB atuais da ALFA: todos usam drivers nativos do kernel, funcionam ao conectar e não precisam de compilação nem de DKMS. O DGX Spark usa o mesmo GB10 e a mesma família de kernel da NVIDIA, portanto espera-se o mesmo comportamento, mas os testes foram feitos apenas no GX10; o DGX Spark não foi testado individualmente. Diferenças de funcionalidade: os modelos MediaTek MT7921 (AWUS036AXM / AXML) falham na injeção de pacotes no kernel stock 6.17, mas monitor, AP e WPA3 funcionam; nos outros 7 modelos, monitor e injeção foram testados e funcionam. A versão mínima do kernel em que cada driver entrou no mainline varia (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); apenas kernels abaixo dessa versão precisam de drivers DKMS da comunidade. Atenção: todos os ports USB do DGX Spark são do tipo USB Type-C, enquanto os adaptadores de rede ALFA são do tipo USB Type-A, portanto, é necessário usar um adaptador USB-C to USB-A ou um cabo de transmissão.

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
| Armazenamento | Até 4TB NVMe M.2 SSD (autocriptografado) |
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

- Kernel 6.x (moderno): o kernel 6.17 (versão testada no GX10) já integra os drivers das 9 placas deste artigo, incluindo mt76 (MT7612U / MT7610U, 4.19+), mt7921u (MT7921AUN, 5.18+), rtw88 (RTL8821CU 6.2+; RTL8812AU / RTL8811AU 6.13+) e rtw89 (RTL8832BU, 6.17+). Isso contrasta marcadamente com o kernel 4.9 do Jetson Nano.
- Arquitetura ARM64 (aarch64): ao usar os drivers nativos do kernel, não é preciso compilar nada no ARM64; somente em sistemas antigos com kernel abaixo da versão mínima da placa os modelos Realtek precisam compilar drivers DKMS da comunidade (como a série morrownr, confirmando que CONFIG_PLATFORM_ARM64 = y no Makefile).

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
| Acesso Wireless Básico (muito simples) | Qualquer um dos 9 (por exemplo, AWUS036ACM / ACHM) | Todos usam drivers nativos do kernel e funcionam ao conectar |
| Teste de Penetração / Monitoramento / Injeção de Wireless | AWUS036EACS / ACH / ACS | Injeção testada 96–100%, captura de WPA handshake de ponta a ponta; evite AXM / AXML (injeção falha) |
| Wi-Fi 6 + hotspot AP | AWUS036AX / AXER | AP 2x2 com 80MHz testado e funcional |
| Banda de 6GHz | AWUS036AXML | AP WPA3 em 6GHz testado e funcional; o AXM usa o mesmo chip, mas 6GHz não foi testado |
| Usuários que já possuem AWUS036ACH e desejam continuar usando | AWUS036ACH | A partir do kernel 6.13 o rtw88_8812au vem integrado, funciona ao conectar e a injeção testada foi 100% nas duas bandas |
| Não necessita de WiFi externo (usando interno) | — | O DGX Spark já possui Wi-Fi 7 integrado; para acesso comum à internet não é preciso um ALFA externo |

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
| Versão do kernel | O kernel 6.17 (testado no GX10 com 6.17.0-1014-nvidia) já integra os drivers das 9 placas, sem necessidade de ferramentas de compilação; a versão mínima varia por placa (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), e apenas kernels abaixo dela precisam de drivers DKMS da comunidade |
| Ferramentas de Gestão de Wireless | iw, wpa_supplicant, network-manager (instalado por padrão no DGX OS) |

## 6. Determinação de Compatibilidade

### Matriz de Compatibilidade entre Modelos Atuais do ALFA × NVIDIA DGX Spark (GB10)

| Modelo | Chipset | Driver (nativo do kernel) | Detecção de USB | STA de Internet | Modo AP | Monitor | Injeção de pacotes | Dificuldade de Instalação | Avaliação Geral |
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

Critérios de Determinação: testes em máquina real realizados de 16 a 18/11/2026 no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), usando como alvo Wi-Fi e celulares próprios. O DGX Spark usa o mesmo GB10 e a mesma família de kernel da NVIDIA, portanto espera-se o mesmo comportamento, mas os testes foram feitos apenas no GX10; o DGX Spark não foi testado individualmente. Dados completos em [Tabela de testes ARM64 das 9 placas de rede ALFA](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

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

**Passo 3: Confirme se a versão do kernel é 6.17 ou superior**

A partir do kernel 6.17, os drivers das 9 placas já vêm integrados e não é preciso instalar ferramentas de compilação. A versão mínima varia por placa (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); somente abaixo dela os modelos Realtek precisam de drivers DKMS da comunidade (veja o último parágrafo de 7.3).

### 7.2 Rota A: Modelos com Chipset MediaTek (AWUS036ACM / ACHM / AXML / AXM) — Pronto para Uso

**Passo 1: Insira a Placa de Rede**

Use um adaptador USB-C to USB-A (o AXML pode ser inserido diretamente no conector USB-C) e insira a placa de rede ALFA na porta USB do DGX Spark.

**Passo 2: Confira se a placa de rede foi detectada**

```bash
lsusb
# Saída esperada (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Passo 3: Confira se a interface de rede foi criada automaticamente**

```bash
ip link show
# Esperado: uma interface começando com wlx (nomeada pelo MAC, driver in-kernel carregado automaticamente)
```

**Passo 4: Escaneie redes WiFi** (o exemplo abaixo usa wlan0; substitua pelo nome da interface mostrado em `ip link show`)

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**Passo 5: Conecte-se à rede WiFi (usando NetworkManager)**

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

### 7.3 Rota B: Modelos Realtek Wi-Fi 5 (AWUS036ACH / ACS / EACS) — sem instalação no kernel 6.13+ (EACS 6.2+)

**Passo 1: Insira a placa de rede e confira se o driver foi carregado automaticamente**

```bash
uname -r          # ACH/ACS exigem 6.13 ou superior; EACS exige 6.2 ou superior
lsusb
lsmod | grep rtw88
ip link show
```

Módulos carregados automaticamente por modelo: ACH → `rtw88_8812au`, ACS → `rtw88_8821au`, EACS → `rtw88_8821cu` (o EACS também tem Bluetooth, testado e funcional).

**Passo 2: A conexão é feita como no Passo 5 de 7.2 (usando nmcli)**

**Passo 3: (Opcional) Modo Monitoramento e Injeção**

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

**Passos necessários apenas em kernel antigo (ACH/ACS abaixo do 6.13, EACS abaixo do 6.2)**: depois de instalar `build-essential git bc dkms`, compile o driver da comunidade, por exemplo morrownr/8812au-20210820 para o RTL8812AU (confirmando `CONFIG_PLATFORM_ARM64 = y` no Makefile). Com uma versão de kernel suficiente, use diretamente o driver nativo.

### 7.4 Rota C: Modelos Wi-Fi 6 (AWUS036AX / AXER, RTL8832BU) — sem instalação no kernel 6.17+

```bash
lsusb                      # esperado: 0bda:b832
lsmod | grep rtw89_8852bu
ip link show
```

Teste no GX10: o `rtw89_8852bu` nativo do kernel é carregado automaticamente, a recepção em monitor é forte, a injeção funciona (2.4GHz: AX 96%, AXER 73%) e o AP suporta 80MHz. O rtw89_8852bu só entrou no mainline no kernel 6.17; sistemas com kernel 6.16 ou inferior precisam do driver DKMS da comunidade (morrownr/rtl8852bu-20250826).

## 8. Erros Comuns e Solução

| Sintomas | Possíveis Causas | Forma de Solução |
|---|---|---|
| O comando `lsusb` não mostra a placa de rede ALFA | Adaptador USB-C defeituoso / Falta de contato | Trocar o adaptador USB-C to USB-A; Verificar se o adaptador suporta transmissão de dados (não apenas carregamento); Tentar diferentes portas USB-C |
| O chip MediaTek, após ser inserido, não possui interface wlan | Módulo do kernel não foi carregado automaticamente / Firmware faltando | Carregar manualmente: `sudo modprobe mt76x2u`; Verificar `dmesg \| grep mt76`; Instalar firmware: `sudo apt install linux-firmware` |
| Placa Realtek inserida sem interface wlan | Kernel abaixo da versão mínima da placa (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), sem o driver correspondente integrado | Confirmar a versão com `uname -r`; atualizar o kernel ou, em kernel antigo, instalar o driver DKMS da comunidade |
| Em kernel antigo, após instalar o driver DKMS, o modprobe retorna "Operation not permitted" | Secure Boot / Assinatura do módulo | É necessário assinar o módulo ou desativar o Secure Boot (isso não ocorre ao usar os drivers nativos) |
| Nenhum sinal é detectado após alternar repetidamente entre monitor / AP | Travamento de RX (RX stall) | Desconectar e reconectar a placa para que o USB seja reenumerado |
| EACS / AXML sem interface wlx após reconectar | Probe travado no dispositivo composto Bluetooth + Wi-Fi | Reconectar em outra porta USB |
| Conexão WiFi instável / lenta | O adaptador USB-C suporta apenas USB 2.0 | Trocar o adaptador que suporta USB 3.2 Gen 2×2; Verificar se o adaptador está marcado como "Data" e não "Charge Only" |
| O Wi-Fi integrado e o ALFA externo se interferem | Colisão entre duas interfaces sem fio | Desativar o Wi-Fi integrado: `sudo nmcli radio wifi off` ou desativar no BIOS/UEFI; ou configurar a prioridade de roteamento |
| O 6GHz (Wi-Fi 6E) não pode ser usado | Restrição de Domínio Regulatório | Definir o domínio regulatório: `sudo iw reg set US` (6GHz aberto nos EUA); o AXML foi testado e funciona em 6GHz, o AXM não foi testado |
| O modo AP falha ao ser iniciado | Conflito entre NetworkManager e hostapd | Consultar o Guia de Soft AP da Yopitek ALFA; retirar a interface do controle do NetworkManager e configurar o hostapd manualmente |
| A placa de rede desaparece após o despertar | Suspensão automática do USB | Desativar a suspensão automática do USB: `echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. Limitações Conhecidas

- **Requisito de Conversão USB Type-C**: Além do AXML, todas as placas de rede ALFA necessitam de adaptador USB-C to USB-A, a qualidade do adaptador pode afetar o desempenho e a estabilidade.
- **Falha de injeção nos modelos MT7921**: os AWUS036AXM / AXML falham na injeção de pacotes no kernel stock 6.17, sem deauth nem captura de handshake; monitor, AP e WPA3 funcionam. A causa principal é uma regressão de chanctx do mac80211 a partir do kernel 6.16; drivers corrigidos pela comunidade ainda têm limitação de taxa.
- **Escopo dos testes**: testado apenas no ASUS GX10 (kernel 6.17.0-1014-nvidia); o DGX Spark não foi testado individualmente, espera-se o mesmo comportamento.
- **hcxdumptool indisponível**: todas as placas, exceto o EACS em 2.4 GHz, apresentam `failed to arm`; use airodump-ng + aireplay-ng.
- **Possível Conflito com Wi-Fi Externo**: O DGX Spark já possui Wi-Fi 7 integrado, e ao usar Wi-Fi interno e externo ao mesmo tempo, podem ocorrer conflitos de roteamento ou recursos.
- **Configuração Manual do Modo AP**: O DGX OS é pré-configurado para ambiente de desenvolvimento, e o modo hotspot AP requer instalação e configuração manual de hostapd / dnsmasq.
- **Restrições Regulamentares de 6GHz**: A disponibilidade da faixa de 6GHz do Wi-Fi 6E depende das configurações regulamentares da região, a situação de abertura da 6GHz em Taiwan deve ser confirmada conforme a legislação mais recente.
- **Kernel antigo**: somente em sistemas com kernel abaixo da versão mínima da placa (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17) os modelos Realtek precisam de drivers DKMS da comunidade (morrownr), que devem ser recompilados a cada atualização do kernel.
- **Diferenças nas Funções de Teste de Penetração**: no GX10, a maior taxa de sucesso de injeção foi dos modelos Realtek rtw88 (EACS e ACH 100% nas duas bandas); os modelos MediaTek mt76 (ACM / ACHM) funcionam; os MT7921 (AXM / AXML) falham.
- **Função Bluetooth**: o Bluetooth do AWUS036AXML e do AWUS036EACS foi testado e funciona no GX10; o Bluetooth do AWUS036AXM não foi validado separadamente (o DGX Spark já possui BT 5.4 integrado).
- **RTL8832BU (AWUS036AX / AXER)**: o mantenedor de drivers morrownr já recomendou publicamente evitar os drivers out-of-tree da série rtl8852/32au (fonte no Capítulo 10). Neste teste no GX10 foi usado o `rtw89_8852bu` nativo do kernel, e monitor, injeção, AP e WPA3 funcionaram; esta conclusão vale apenas para o driver nativo do kernel 6.17 ou superior.
- **RTL8812AU (AWUS036ACH)**: o driver in-kernel `rtw88_8812au`, padrão mac80211, foi integrado ao mainline no kernel 6.13 e atingiu maturidade a partir do 6.14 (anúncio de morrownr). No GX10 com kernel 6.17 funcionou ao conectar, com injeção de 100% nas duas bandas. Antes de responder, o suporte técnico pode pedir ao cliente o resultado de `uname -r` para confirmar se é 6.13 ou superior.

Condições de Refutação: se, após uma atualização do DGX OS, mudanças na versão do kernel ou no driver do controlador USB alterarem o comportamento, ou se testes em um DGX Spark real mostrarem resultados diferentes dos do GX10, a matriz de compatibilidade do Capítulo 6 deve ser revisada; se um futuro kernel corrigir o problema de injeção do mt7921u, a avaliação dos AWUS036AXM / AXML poderá subir de "Apenas conexão / AP".

## 10. Fontes de Referência URL

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| Página Oficial do NVIDIA DGX Spark | Especificações e informações sobre a plataforma DGX Spark | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| Documentação do NVIDIA DGX | Arquitetura do sistema operacional DGX e versão do kernel | https://docs.nvidia.com/dgx/dgx-spark | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Driver RTL8812AU para Linux (suporte ARM64) | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| morrownr/8821cu GitHub | Driver RTL8821CU para Linux (para kernels antigos) | https://github.com/morrownr/8821cu-20210916 | ✅ Verificado | 2026-09-03 |
| morrownr/rtl8852bu GitHub | Driver RTL8832BU para Linux | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Verificado | 2026-09-03 |
| Documentação do driver mt76 do kernel Linux | Descrição do driver MediaTek mt76 / mt7921 mainline (versão inicial do kernel suportada por cada chip) | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ Verificado | 2026-09-03 |
| Guia de Soft AP WiFi Hotspot Linux do ALFA (Yopitek) | Guia de configuração do modo AP no Linux para o ALFA | /pt/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verificado | 2026-09-03 |
| Catálogo de Produtos da ALFA Network (Yopitek) | Especificações dos produtos atuais da ALFA | /pt/products/alfa/ | ✅ Verificado | 2026-09-03 |
| Tabela de testes ARM64 das 9 placas de rede ALFA (Yopitek) | Testes em máquina real no ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Testado | 2026-11-18 |
| Issue #314 do morrownr/USB-WiFi | Declaração oficial do mantenedor do driver: Recomendação de evitar o chip rtl8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Verificado | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | Anúncio mais recente sobre o estado do driver RTL8812AU (inclusão na linha principal do kernel 6.13, maturidade de qualidade no 6.14) | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |

Artigos Relacionados: [O adaptador Wi-Fi ALFA suporta o MSI EdgeXpert?](/pt/blog/alfa-msi-edgexpert-compatibility/) | [O adaptador Wi-Fi ALFA suporta o ASUS Ascent GX10?](/pt/blog/alfa-asus-ascent-gx10-compatibility/) | [O adaptador Wi-Fi ALFA suporta o ALTOS BrainSphere GB10 F1?](/pt/blog/alfa-altos-brainsphere-gb10-compatibility/) | [O adaptador Wi-Fi ALFA suporta o GIGABYTE AI TOP ATOM?](/pt/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [O adaptador Wi-Fi ALFA suporta o NVIDIA Jetson Nano?](/pt/blog/alfa-nvidia-jetson-nano-compatibility/)

Declaração de Isenção de Responsabilidade: A determinação de compatibilidade deste artigo é baseada nos testes em máquina real realizados em novembro de 2026 no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia). O DGX Spark e o GX10 usam o mesmo GB10 e a mesma família de kernel da NVIDIA, portanto espera-se o mesmo comportamento, mas ele não foi testado individualmente. O kernel 6.17 testado no GX10 já integra os drivers das 9 placas de rede ALFA (a versão mínima varia por placa); apenas kernels abaixo da versão mínima da placa precisam de drivers DKMS da comunidade (morrownr). O DGX Spark já possui Wi-Fi 7, e o uso de adaptadores ALFA de rede externa é principalmente para testes de penetração ou necessidades de chips específicos. A qualidade do adaptador USB-C afeta diretamente a experiência de uso, recomenda-se a escolha de adaptadores com marca e etiqueta USB 3.2 Gen 2×2. Monitoramento e injeção devem ser feitos apenas em redes próprias ou com autorização.
