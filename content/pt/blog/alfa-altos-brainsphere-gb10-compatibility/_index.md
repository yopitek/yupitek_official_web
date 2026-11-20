---
title: "Suporte do Cartão de Rede Wireless ALFA para o ALTOS BrainSphere GB10 F1"
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
description: "As 9 placas USB ALFA no ALTOS BrainSphere GB10 F1: testadas no ASUS GX10 (kernel 6.17), usam driver nativo sem DKMS; EACS/ACH/ACS injetam bem, AXM/AXML falham."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Este artigo foi atualizado com os testes no GX10 de novembro de 2026: no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), as 9 placas de rede ALFA atuais usam todas drivers nativos do kernel, funcionam ao conectar e não precisam de DKMS. Dados completos em [Tabela de testes ARM64 das 9 placas de rede ALFA](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Testado apenas no GX10; os demais modelos GB10 não foram testados um a um.

## 1. Resumo do Problema

Pergunta do cliente: “O adaptador de rede sem fio ALFA da série USB pode ser utilizado na estação de trabalho ALTOS BrainSphere GB10 F1 (NVIDIA GB10 Grace Blackwell)?”

Conclusão resumida: A estação de trabalho ALTOS BrainSphere GB10 F1 e o NVIDIA DGX Spark usam o mesmo chip GB10 e a mesma família de kernel da NVIDIA. Testamos no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia) os 9 adaptadores de rede USB atuais da ALFA (AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML): todos usam drivers nativos do kernel, funcionam ao conectar e não precisam de compilação nem de DKMS. Espera-se o mesmo comportamento, mas os testes foram feitos apenas no GX10; o ALTOS BrainSphere GB10 F1 não foi testado individualmente. Diferenças de funcionalidade: os modelos MediaTek MT7921 (AWUS036AXM / AXML) falham na injeção de pacotes (packet injection) no kernel stock 6.17, mas monitor, AP e WPA3 funcionam; nos outros 7 modelos, monitor e injeção foram testados e funcionam. A versão mínima do kernel em que cada driver entrou no mainline varia (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); apenas kernels abaixo dessa versão precisam de drivers DKMS da comunidade. Atenção: O BrainSphere GB10 F1 possui 3 portas USB-C de dados + 1 porta de entrada USB-C PD, e os adaptadores de rede ALFA (exceto o AXML) precisam de um adaptador USB-C to USB-A.

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

Impacto na Compatibilidade com o ALFA: nenhum impacto esperado (testado apenas no GX10; os demais modelos GB10 não foram testados um a um). O Altos aiGeni é um software de aplicação, não afeta o framework de drivers do kernel. Os controladores de USB, versão do kernel e arquitetura de drivers são completamente idênticos ao DGX Spark.

### 2.4 Necessidade de Adaptadores USB Type-C

Os 4 portas USB do BrainSphere GB10 F1 são todas Type-C (3 de dados + 1 de entrada PD), enquanto a linha completa de placas de rede ALFA (exceto a AXML, que é USB-C) são USB Type-A, necessitando de adaptadores.

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
| Laboratório de IA corporativo para internet sem fio | Qualquer um dos 9 (por exemplo, AWUS036ACM / ACHM) | Todos usam drivers nativos do kernel e funcionam ao conectar |
| Teste de penetração de wireless / pesquisa de segurança | AWUS036EACS / ACH / ACS | Injeção testada 96–100%, captura de WPA handshake de ponta a ponta; evite AXM / AXML (injeção falha) |
| Wi-Fi 6 + hotspot AP | AWUS036AX / AXER | AP 2x2 com 80MHz testado e funcional |
| Banda de 6GHz | AWUS036AXML | AP WPA3 em 6GHz testado e funcional; o AXM usa o mesmo chip, mas 6GHz não foi testado |
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
| Versão do kernel | O kernel 6.17 (testado no 6.17.0-1014-nvidia) já integra os drivers das 9 placas, sem necessidade de ferramentas de compilação; a versão mínima varia por placa (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), e apenas kernels abaixo dela precisam de drivers DKMS da comunidade |
| Ferramentas de Gestão de Rede sem fio | iw, network-manager (instalado por padrão no DGX OS) |
| Notas sobre aiGeni | Se for utilizado o ambiente de contêineres do aiGeni, é necessário garantir que o dispositivo USB já está corretamente montado no contêiner (recomenda-se configurar no nível do host OS para acesso à Internet). |

## 6. Determinação de Compatibilidade

### Matriz de Compatibilidade ALFA Modelos Atuais × ALTOS BrainSphere GB10 F1

| Modelo | Chipset | Driver (nativo do kernel) | Detecção USB | STA Internet | Modo AP | Monitor | Injeção de pacotes | Dificuldade de Instalação | Avaliação Geral |
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

Critérios de Determinação: testes em máquina real realizados de 16 a 18/11/2026 no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), usando como alvo Wi-Fi e celulares próprios. O ALTOS BrainSphere GB10 F1 usa o mesmo GB10 e a mesma família de kernel da NVIDIA, portanto espera-se o mesmo comportamento, mas os testes foram feitos apenas no GX10; o ALTOS BrainSphere GB10 F1 não foi testado individualmente. Dados completos em [Tabela de testes ARM64 das 9 placas de rede ALFA](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 7. Passo a Passo Detalhado de Configuração

Espera-se que os passos de instalação do ALTOS BrainSphere GB10 F1 sejam idênticos aos do NVIDIA DGX Spark (passos testados no GX10). A seguir está uma versão resumida; para os passos completos, consulte o Capítulo 7 de [A Placa de Rede sem Fio ALFA suporta o NVIDIA DGX Spark?](/pt/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modelos de Chip MediaTek (AWUS036ACM / ACHM / AXM / AXML)

- Utilize o adaptador USB-C to USB-A (AXML pode ser diretamente conectado), insira a placa de rede ALFA na porta USB-C do BrainSphere
- Confira a detecção: `lsusb`
- Confira a interface: `ip link show` (deve aparecer automaticamente uma interface começando com wlx)
- Conecte-se ao WiFi: `nmcli dev wifi connect "SSID" password "senha"`

### 7.2 Modelos de Chip Realtek (AWUS036ACH / ACS / EACS / AX / AXER)

O kernel 6.17 (versão testada no GX10) já integra os drivers de todos os modelos Realtek; os passos são os mesmos dos modelos MediaTek, sem compilação (versões mínimas: EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17):

```bash
# 1. Confira a versão do kernel (a partir do 6.17 todos os drivers Realtek vêm integrados; no GX10 testado: 6.17.0-1014-nvidia)
uname -r

# 2. Após inserir a placa de rede, confira se o driver foi carregado automaticamente
lsusb
lsmod | grep -E "rtw88|rtw89"
ip link show

# 3. Conecte-se ao WiFi
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

### 7.4 Uso do WiFi no Container aiGeni (Avançado)

Se precisar de usar a placa de rede ALFA no container Altos aiGeni:

1. Primeiro, no host OS (DGX OS), confirme que o driver foi carregado automaticamente e conclua a conexão WiFi
2. Inicie o container com `--network=host` ou monte a interface de rede correspondente
3. Recomenda-se que a navegação geral seja feita no nível do host OS, com o container usando `--network=bridge` para compartilhar a rede

## 8. Erros Comuns e Solução

| Sintoma | Possível Causa | Forma de Solução |
|---|---|---|
| `lsusb` não vê a placa de rede ALFA | Adaptador USB-C defeituoso / Especificação de apenas carregamento | Trocar por um adaptador USB 3.2 Gen 2×2 que suporte transferência de dados; tentar em diferentes portas USB-C |
| Chip MediaTek sem interface wlan | Módulo não carregado automaticamente / Firmware faltando | Executar `sudo modprobe mt76x2u`; executar `sudo apt install linux-firmware`; verificar `dmesg \| grep mt76` |
| Placa Realtek inserida sem interface wlan | Kernel abaixo da versão mínima da placa (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), sem o driver correspondente integrado | Confirmar a versão com `uname -r`; atualizar o kernel ou, em kernel antigo, instalar o driver DKMS da comunidade |
| Nenhum sinal é detectado após alternar repetidamente entre monitor / AP | Travamento de RX (RX stall) | Desconectar e reconectar a placa para que o USB seja reenumerado |
| EACS / AXML sem interface wlx após reconectar | Probe travado no dispositivo composto Bluetooth + Wi-Fi | Reconectar em outra porta USB |
| Velocidade de WiFi lenta | Adaptador suporta apenas USB 2.0 | Trocar por um adaptador USB 3.2 Gen 2×2 |
| Conflito entre Wi-Fi 7 integrado e externo | Conflito de roteamento | Executar `sudo nmcli radio wifi off` para desativar o WiFi integrado antes de usar o externo |
| Wi-Fi não visível no container aiGeni | Problema de configuração de rede do container | Usar `--network=host`; ou conectar ao host OS e permitir que o container compartilhe a rede |
| Não é possível usar a frequência de 6GHz | Restrição de Domínio Regulatório | Executar `sudo iw reg set US`; confirmar as últimas regulamentações |

## 9. Restrições Conhecidas

- Necessidade de conversor USB Type-C: Além do AXML, todos os adaptadores de rede ALFA necessitam de conversor USB-C to USB-A
- Falha de injeção nos modelos MT7921: os AWUS036AXM / AXML falham na injeção de pacotes no kernel stock 6.17, sem deauth nem captura de handshake; monitor, AP e WPA3 funcionam. A causa principal é uma regressão de chanctx do mac80211 a partir do kernel 6.16; drivers corrigidos pela comunidade ainda têm limitação de taxa
- Escopo dos testes: testado apenas no ASUS GX10 (kernel 6.17.0-1014-nvidia); o ALTOS BrainSphere GB10 F1 não foi testado individualmente, espera-se o mesmo comportamento
- hcxdumptool indisponível: todas as placas, exceto o EACS em 2.4 GHz, apresentam `failed to arm`; use airodump-ng + aireplay-ng
- Possível conflito com Wi-Fi 7 integrado: BrainSphere já inclui Wi-Fi 7 + BT 5.4
- Configuração manual do modo AP: O DGX OS é pré-configurado como ambiente de desenvolvimento
- Restrições regulatórias de 6GHz: A disponibilidade do Wi-Fi 6E depende da região regulatória
- Kernel antigo: somente em sistemas com kernel abaixo da versão mínima da placa (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17) os modelos Realtek precisam de drivers DKMS da comunidade, que devem ser recompilados a cada atualização do kernel
- Isolamento de contêineres aiGeni: Se usar WiFi em contêineres aiGeni, atenção deve ser dada ao espaço de nomes de rede e ao montagem de dispositivos; é recomendável gerenciar WiFi no nível do host OS
- Diferenças de software Altos não afetam a compatibilidade: aiGeni é uma plataforma de camada de aplicativo, não afetando a compatibilidade do driver de WiFi USB do kernel

Condições de refutação: As avaliações acima são baseadas no DGX OS (baseado em Ubuntu, kernel 6.x). Se a Altos mudar para um sistema operacional próprio sem base Ubuntu ou se houver mudança na versão major do kernel do DGX OS, a avaliação de drivers nativos deve ser testada novamente.

## 10. Fontes de Referência URL

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| Folheto Oficial do Product Sheet do ALTOS BrainSphere GB10 F1 | Especificações de Hardware (170W / 50mm / Configuração USB) | https://www.altoscomputing.com/filepic/pdf/Altos_BrainSphere_GB10_F1_Product_Sheet_TW.pdf | ✅ Verificado | 2026-09-03 |
| Site Oficial da Altos Computing | Informações sobre o Produto BrainSphere GB10 F1 | https://www.altoscomputing.com/en-Us | ✅ Verificado | 2026-09-03 |
| Página Oficial do NVIDIA DGX Spark | Informações sobre a Plataforma GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Driver RTL8812AU para Linux | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| Catálogo de Produtos da ALFA Network (Yopitek) | Especificações dos Produtos Atuais da ALFA | /pt/products/alfa/ | ✅ Verificado | 2026-09-03 |
| Tabela de testes ARM64 das 9 placas de rede ALFA (Yopitek) | Testes em máquina real no ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Testado | 2026-11-18 |

Artigos Relacionados: [A Placa de Rede sem Fio ALFA suporta o NVIDIA DGX Spark?](/pt/blog/alfa-nvidia-dgx-spark-compatibility/) | [A Placa de Rede sem Fio ALFA suporta o ASUS Ascent GX10?](/pt/blog/alfa-asus-ascent-gx10-compatibility/) | [A Placa de Rede sem Fio ALFA suporta o GIGABYTE AI TOP ATOM?](/pt/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [A Placa de Rede sem Fio ALFA suporta o MSI EdgeXpert?](/pt/blog/alfa-msi-edgexpert-compatibility/)

Declaração de Isenção de Responsabilidade: A determinação de compatibilidade deste artigo é baseada nos testes em máquina real realizados em novembro de 2026 no ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia). O ALTOS BrainSphere GB10 F1 e o GX10 usam o mesmo GB10 e a mesma família de kernel da NVIDIA, portanto espera-se o mesmo comportamento, mas ele não foi testado individualmente. O Altos aiGeni é um software de camada de aplicação, que não afeta a compatibilidade do driver. O kernel 6.17 testado no GX10 já integra os drivers das 9 placas de rede ALFA (a versão mínima varia por placa); apenas kernels abaixo da versão mínima da placa precisam de drivers DKMS da comunidade. O BrainSphere já possui Wi-Fi 7, e o uso do ALFA externo é principalmente para testes de penetração ou necessidades de chip específicas. Monitoramento e injeção devem ser feitos apenas em redes próprias ou com autorização.
