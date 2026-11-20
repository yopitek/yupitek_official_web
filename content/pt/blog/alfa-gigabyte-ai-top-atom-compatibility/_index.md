---
title: "Suporte do Cartão de Rede Wireless ALFA para o GIGABYTE AI TOP ATOM (GB10)"
date: 2026-09-03
draft: false
slug: "alfa-gigabyte-ai-top-atom-compatibility"
tags:
  - "ALFA"
  - "GIGABYTE"
  - "AI-TOP-ATOM"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "Guia de Hardware"
description: "As 9 placas USB ALFA no GIGABYTE AI TOP ATOM: testadas no ASUS GX10 (kernel 6.17), usam driver nativo sem DKMS; EACS/ACH/ACS injetam melhor e AXM/AXML falham."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Este artigo foi atualizado com os testes no GX10 de novembro de 2026: no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), as 9 placas de rede ALFA atuais usam todas drivers nativos do kernel, funcionam ao conectar e não precisam de DKMS. Dados completos em [Tabela de testes ARM64 das 9 placas de rede ALFA](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Testado apenas no GX10; os demais modelos GB10 não foram testados um a um.

## 1. Resumo do Problema

Pergunta do cliente: “O adaptador de rede sem fio USB da série ALFA pode ser utilizado no supercomputador pessoal AI TOP ATOM da GIGABYTE (modelo ATAGB10-9000, NVIDIA GB10 Grace Blackwell)?”

Conclusão breve: O GIGABYTE AI TOP ATOM e o NVIDIA DGX Spark usam o mesmo chip GB10 e a mesma família de kernel da NVIDIA. Testamos no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia) os 9 adaptadores de rede USB atuais da ALFA (AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML): todos usam drivers nativos do kernel, funcionam ao conectar e não precisam de compilação nem de DKMS. Espera-se o mesmo comportamento, mas os testes foram feitos apenas no GX10; o GIGABYTE AI TOP ATOM não foi testado individualmente. Diferenças de funcionalidade: os modelos MediaTek MT7921 (AWUS036AXM / AXML) falham na injeção de pacotes (packet injection) no kernel stock 6.17, mas monitor, AP e WPA3 funcionam; nos outros 7 modelos, monitor e injeção foram testados e funcionam. A versão mínima do kernel em que cada driver entrou no mainline varia (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); apenas kernels abaixo dessa versão precisam de drivers DKMS da comunidade. Atenção: todos os ports USB do AI TOP ATOM são do tipo USB Type-C; por isso, todos os adaptadores de rede ALFA, exceto o AXML, necessitam de um adaptador USB-C to USB-A.

## 2. Análise da Arquitetura de Especificações de Hardware de Objetivo

### 2.1 Especificações de Hardware do GIGABYTE AI TOP ATOM

| Item | Especificação |
|---|---|
| Nome do Produto | GIGABYTE AI TOP ATOM (Modelos: ATAGB10-9000 / ATAGB10-9001) |
| Chip de Núcleo | NVIDIA GB10 Grace Blackwell Superchip (Plataforma DGX Spark) |
| CPU | 20-núcleo Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Arquitetura Blackwell da NVIDIA, 6144 núcleos CUDA, Cincoª Geração Tensor Core, Quartoª Geração RT Core |
| Desempenho de AI | Até 1 PetaFLOP (FP4, Sparse) / 1000 TOPS, suporta modelos com até 200 bilhões de parâmetros |
| Memória do Sistema | 128GB LPDDR5x Memória Unificada (256-bit, 273 GB/s) |
| Armazenamento | Até 4TB M.2 NVMe SSD (ATAGB10-9000 é PCIe Gen5 4TB; 9001 é Gen4 4TB) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (20Gbps), onde 1 é entrada de energia (igual ao design de referência GB10) |
| Saída de Vídeo | 1× HDMI 2.1a (expandível via DP Alt Mode pelo USB-C) |
| Rede com Fio | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC |
| Rede sem Fio | Wi-Fi 7 + Bluetooth 5.4 |
| Sistema Operacional | NVIDIA DGX OS (baseado em Ubuntu Linux, kernel 6.x) |
| Arquitetura | aarch64 (ARM64) |
| Tamanho | 150 × 150 × 50.5 mm (1.13L) |
| Peso | Aproximadamente 1.2 kg |
| Alimentação | Fonte de alimentação USB-C de 240W |
| Garantia | 1 ano de garantia original |

> Nota de Verificação de Especificações: O tamanho de 50.5mm e o peso de 1.2kg são consistentes com as especificações oficiais da GIGABYTE; a versão Bluetooth é **BT 5.4**, conforme a página oficial de especificações da GIGABYTE ([página oficial](https://www.gigabyte.com/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM/sp)). A configuração USB é 3 portas de dados + 1 porta de alimentação (as especificações oficiais são 4× Type-C, onde 1 é dedicada à energia do sistema).

### 2.2 Ambiente de Software: NVIDIA DGX OS

| Item | Conteúdo |
|---|---|
| OS Básico | Ubuntu Linux (personalizado pela NVIDIA) |
| Kernel | Linux 6.x |
| Arquitetura | aarch64 (ARM64) |
| Software Pré-instalado | NVIDIA AI Software Stack (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, Ollama, etc.) + GIGABYTE AI TOP Utility |
| Gestão de Pacotes | apt |

### 2.3 Diferenças com o DGX Spark

| Item de Diferença | AI TOP ATOM | NVIDIA DGX Spark |
|---|---|---|
| Design de Estrutura | Personalizado pela GIGABYTE / AORUS | Design de referência da NVIDIA |
| Posicionamento da Marca | Supercomputador AI Pessoal (mesa / escritório) | Plataforma de Desenvolvimento de AI para Mesa |
| Armazenamento | Até 4TB (versões Gen5 / Gen4) | Até 4TB |
| Acessórios | Acessórios originais da GIGABYTE + AI TOP Utility | Acessórios originais da NVIDIA |
| Garantia | 1 ano | Conforme o canal de venda |

Influência na Compatibilidade com o ALFA: nenhum impacto esperado (testado apenas no GX10; os demais modelos GB10 não foram testados um a um). O controlador USB, a versão do kernel e o framework de drivers são completamente idênticos ao DGX Spark.

### 2.4 Necessidade de Conector USB Type-C

Todas as portas do AI TOP ATOM são Type-C, enquanto todos os cartões de rede da série ALFA (exceto o AXML, que é USB-C) são Type-A, exigindo um conector de adaptação. Recomenda-se usar um conector de adaptação que suporte USB 3.2 Gen 2×2 (20Gbps) para garantir que os modelos AWUS036ACH / ACM / AX, entre outros, possam operar a plena velocidade.

## 3. Análise das Especificações e Chipsets da Placa de Rede ALFA

Até setembro de 2026, a linha de produtos de placas de rede USB sem fio da ALFA Network é a seguinte:

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
| Desenvolvimento de AI em desktop e conexão sem fio | Qualquer um dos 9 (por exemplo, AWUS036ACM / ACHM) | Todos usam drivers nativos do kernel e funcionam ao conectar |
| Teste de Penetração e Pesquisa em Segurança sem fio | AWUS036EACS / ACH / ACS | Injeção testada 96–100%, captura de WPA handshake de ponta a ponta; evite AXM / AXML (injeção falha) |
| Wi-Fi 6 + hotspot AP | AWUS036AX / AXER | AP 2x2 com 80MHz testado e funcional |
| Banda de 6GHz | AWUS036AXML | AP WPA3 em 6GHz testado e funcional; o AXM usa o mesmo chip, mas 6GHz não foi testado |
| Não necessita de Wi-Fi externo | — | O AI TOP ATOM já possui Wi-Fi 7 integrado, geralmente não há necessidade de conexão externa |

## 5. Requisitos de Ambiente

### 5.1 Requisitos de Hardware

| Item | Requisitos |
|---|---|
| Conector USB | Conector USB-C para USB-A ou cabo de transmissão (exceto AXML), recomendado suporte a USB 3.2 Gen 2×2 |
| Alimentação | Fonte de alimentação USB-C de 240W da GIGABYTE |

### 5.2 Requisitos de Software

| Item | Requisitos |
|---|---|
| Versão do DGX OS | Qualquer versão em serviço (kernel 6.x) |
| Versão do kernel | O kernel 6.17 (testado no 6.17.0-1014-nvidia) já integra os drivers das 9 placas, sem necessidade de ferramentas de compilação; a versão mínima varia por placa (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), e apenas kernels abaixo dela precisam de drivers DKMS da comunidade |
| Ferramentas de Gestão de Rede | iw, network-manager (instalado por padrão no DGX OS) |

## 6. Determinação de Compatibilidade

### Matriz de Compatibilidade do Modelo Atual ALFA × GIGABYTE AI TOP ATOM (GB10)

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

Critério de Determinação: testes em máquina real realizados de 16 a 18/11/2026 no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), usando como alvo Wi-Fi e celulares próprios. O GIGABYTE AI TOP ATOM usa o mesmo GB10 e a mesma família de kernel da NVIDIA, portanto espera-se o mesmo comportamento, mas os testes foram feitos apenas no GX10; o GIGABYTE AI TOP ATOM não foi testado individualmente. Dados completos em [Tabela de testes ARM64 das 9 placas de rede ALFA](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 7. Passo a Passo Detalhado de Configuração

Espera-se que os passos de instalação do GIGABYTE AI TOP ATOM sejam idênticos aos do NVIDIA DGX Spark (passos testados no GX10). A seguir, está uma versão resumida; para os passos completos, consulte o Capítulo 7 de [A Placa de Rede sem Fio ALFA Suporta o NVIDIA DGX Spark?](/pt/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modelos de Chip MediaTek (AWUS036ACM / ACHM / AXM / AXML)

- Utilize o adaptador USB-C to USB-A (AXML pode ser conectado diretamente), insira a placa de rede ALFA na porta USB-C do AI TOP ATOM
- Confira a detecção: `lsusb`
- Confira a interface: `ip link show` (deve aparecer automaticamente uma interface começando com wlx)
- Conecte-se à WiFi: `nmcli dev wifi connect "SSID" password "senha"`

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

| Sintoma | Possível Causa | Forma de Solução |
|---|---|---|
| `lsusb` não vê a placa de rede ALFA | Adaptador USB-C defeituoso / Especificação de apenas carregamento | Trocar por adaptador USB 3.2 Gen 2×2 que suporte transferência de dados; tentar em diferentes portas USB-C |
| Chipset MediaTek sem interface wlan | Módulo não carregado automaticamente / Firmware faltando | `sudo modprobe mt76x2u`; `sudo apt install linux-firmware`; verificar `dmesg \| grep mt76` |
| Placa Realtek inserida sem interface wlan | Kernel abaixo da versão mínima da placa (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), sem o driver correspondente integrado | Confirmar a versão com `uname -r`; atualizar o kernel ou, em kernel antigo, instalar o driver DKMS da comunidade |
| Nenhum sinal é detectado após alternar repetidamente entre monitor / AP | Travamento de RX (RX stall) | Desconectar e reconectar a placa para que o USB seja reenumerado |
| EACS / AXML sem interface wlx após reconectar | Probe travado no dispositivo composto Bluetooth + Wi-Fi | Reconectar em outra porta USB |
| Velocidade de WiFi lenta | Adaptador suporta apenas USB 2.0 | Trocar por adaptador USB 3.2 Gen 2×2 |
| Conflito entre Wi-Fi interno e externo | Conflito de roteamento | `sudo nmcli radio wifi off` desativar o WiFi interno antes de usar o externo |
| Não é possível usar a frequência de 6GHz | Restrição de Domínio Regulatório | `sudo iw reg set US`; confirmar as últimas regulamentações |
| Placa de rede desaparece após o despertar do sistema | Suspensão automática do USB | `echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. Restrições Conhecidas

- **Requisito de Conector USB Type-C**: Exceto para AXML, todos os adaptadores de rede ALFA necessitam de adaptador USB-C to USB-A.
- **Falha de injeção nos modelos MT7921**: os AWUS036AXM / AXML falham na injeção de pacotes no kernel stock 6.17, sem deauth nem captura de handshake; monitor, AP e WPA3 funcionam. A causa principal é uma regressão de chanctx do mac80211 a partir do kernel 6.16; drivers corrigidos pela comunidade ainda têm limitação de taxa.
- **Escopo dos testes**: testado apenas no ASUS GX10 (kernel 6.17.0-1014-nvidia); o GIGABYTE AI TOP ATOM não foi testado individualmente, espera-se o mesmo comportamento.
- **hcxdumptool indisponível**: todas as placas, exceto o EACS em 2.4 GHz, apresentam `failed to arm`; use airodump-ng + aireplay-ng.
- **Possível Conflito com Wi-Fi 7 Integrado**: O Wi-Fi 7 integrado pode conflitar com dispositivos externos; o AI TOP ATOM já possui Wi-Fi 7 + BT 5.4.
- **Configuração Manual do Modo AP**: O DGX OS é pré-configurado como ambiente de desenvolvimento.
- **Restrições Regulamentares de 6GHz**: A disponibilidade do Wi-Fi 6E depende das regulamentações da região.
- **Kernel antigo**: somente em sistemas com kernel abaixo da versão mínima da placa (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17) os modelos Realtek precisam de drivers DKMS da comunidade, que devem ser recompilados a cada atualização do kernel.
- **Diferenças de Hardware da GIGABYTE Não Afetam a Compatibilidade**: Diferenças em design de estrutura e dissipação de calor não afetam a compatibilidade do driver USB WiFi.
- **Garantia e suporte técnico**: a partir do kernel 6.17 não é necessário instalar drivers de terceiros; se drivers DKMS da comunidade forem instalados em um kernel antigo, o suporte técnico da GIGABYTE pode não cobrir problemas com drivers de terceiros.

**Condições de Rejeição**: As avaliações acima são baseadas no DGX OS (baseado em Ubuntu, kernel 6.x). Caso a GIGABYTE lance versões de firmware próprias para sistemas operacionais diferentes do DGX OS, a avaliação deve ser revalidada; a versão do Bluetooth (5.4) deve ser verificada conforme a especificação do lote de fábrica, e é recomendável verificar a página oficial após o recebimento.

## 10. Fontes de Referência URL

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| Página de Produtos Oficial da GIGABYTE AI TOP ATOM | Especificações de Hardware AI TOP ATOM (ATAGB10-9000) | https://www.gigabyte.com/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM | ✅ Verificado | 2026-09-03 |
| Página Oficial da GIGABYTE AI TOP ATOM (Mirror em Chinês Simplificado) | Características e Especificações do Produto | https://www.gigabyte.cn/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM | ✅ Verificado | 2026-09-03 |
| Review da GIGABYTE AI TOP ATOM (LinuxGizmos) | Avaliação de Terceiros e Verificação de Especificações (50.5mm) | https://linuxgizmos.com/gigabyte-ai-top-atom-introduces-nvidia-grace-blackwell-gb10-performance-for-the-desktop/ | ✅ Verificado | 2026-09-03 |
| Página Oficial do NVIDIA DGX Spark | Informações sobre a Plataforma GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Driver Linux para RTL8812AU | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| Visão Geral de Produtos da ALFA Network (Yopitek) | Especificações dos Produtos Atuais da ALFA | /pt/products/alfa/ | ✅ Verificado | 2026-09-03 |
| Tabela de testes ARM64 das 9 placas de rede ALFA (Yopitek) | Testes em máquina real no ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Testado | 2026-11-18 |

Artigos Relacionados: [A Placa de Rede sem Fio ALFA Suporta o NVIDIA DGX Spark?](/pt/blog/alfa-nvidia-dgx-spark-compatibility/) | [A Placa de Rede sem Fio ALFA Suporta o ASUS Ascent GX10?](/pt/blog/alfa-asus-ascent-gx10-compatibility/) | [A Placa de Rede sem Fio ALFA Suporta o ALTOS BrainSphere GB10 F1?](/pt/blog/alfa-altos-brainsphere-gb10-compatibility/) | [A Placa de Rede sem Fio ALFA Suporta o MSI EdgeXpert?](/pt/blog/alfa-msi-edgexpert-compatibility/)

Declaração de Isenção de Responsabilidade: A determinação de compatibilidade deste artigo é baseada nos testes em máquina real realizados em novembro de 2026 no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia). O GIGABYTE AI TOP ATOM e o GX10 usam o mesmo GB10 e a mesma família de kernel da NVIDIA, portanto espera-se o mesmo comportamento, mas ele não foi testado individualmente. O kernel 6.17 testado no GX10 já integra os drivers das 9 placas de rede ALFA (a versão mínima varia por placa); apenas kernels abaixo da versão mínima da placa precisam de drivers DKMS da comunidade. O AI TOP ATOM já possui Wi-Fi 7, e o uso da ALFA é principalmente para testes de penetração ou necessidades de chip específicas. Monitoramento e injeção devem ser feitos apenas em redes próprias ou com autorização.
