---
title: "Carta Técnica: Suporte do Adaptador de Rede Wireless ALFA para OpenWrt"
date: 2026-09-03
draft: false
slug: "alfa-openwrt-router-compatibility"
tags:
  - "ALFA"
  - "OpenWrt"
  - "Router"
  - "kmod-mt76"
  - "AWUS036ACM"
  - "AWUS036ACH"
  - "Soft-AP"
categories:
  - "Guia de Hardware"
description: "OpenWrt: ótimo suporte ao ALFA USB WiFi, suporta MT7612U com driver oficial, Realtek com driver comunitário."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumo do Problema

Pergunta do cliente: “O adaptador USB sem fio da série ALFA pode ser utilizado em roteadores com OpenWrt?”

Conclusão breve: O OpenWrt é a plataforma de três principais sistemas operacionais de terceiros para roteadores (DD-WRT / OpenWrt / Tomato) que oferece o melhor suporte aos adaptadores USB WiFi da série ALFA. Os modelos com processador MediaTek (AWUS036ACM / ACHM / AXML / AXM) são compatíveis diretamente através do pacote oficial kmod-mt76; os modelos com processador Realtek (AWUS036ACH / ACS / EACS / AX / AXER) requerem o uso de pacotes de drivers mantidos pela comunidade, que podem variar em disponibilidade dependendo da versão do OpenWrt. O AWUS036ACM (MT7612U) é a opção preferida, devido ao seu driver bem estabelecido, estável, e suporte a escaneamento e injecção.

Critérios de avaliação: Os 9 adaptadores USB de rede atuais da ALFA (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Análise das Especificações e Requisitos do Software de Objetivo

### 2.1 O que é o OpenWrt

OpenWrt é um firmware de roteador open source altamente modular, que utiliza o kernel Linux e o sistema de gerenciamento de pacotes opkg. Diferente de DD-WRT / Tomato, os drivers do OpenWrt são fornecidos na forma de pacotes de módulos do kernel (kmod) que podem ser instalados individualmente, permitindo ao usuário instalar drivers de WiFi USB sem a necessidade de recompilar todo o firmware.

### 2.2 Framework de Drivers de WiFi USB do OpenWrt

A biblioteca de pacotes oficial do OpenWrt inclui os seguintes drivers de WiFi USB:

| Pacote de Driver | Fonte | Chipsets / Modelos | Estado de Manutenção |
|---|---|---|---|
| kmod-mt76-usb + kmod-mt76x2u | Oficial in-kernel | MediaTek MT7612U (AWUS036ACM) | Ativo, estável |
| kmod-mt76-usb + kmod-mt76x0u | Oficial in-kernel | MediaTek MT7610U (AWUS036ACHM) | Ativo |
| kmod-mt7921u | Oficial in-kernel | MediaTek MT7921AUN (AWUS036AXML / AXM) | Disponível a partir da versão 23.05 |
| kmod-rtl8812au-ct | Comunidade out-of-tree | Realtek RTL8812AU / RTL8811AU (AWUS036ACH / ACS) | Manutenção comunitária, relatórios de kernel crash em 24.10 |
| kmod-rtl8821cu | Comunidade out-of-tree | Realtek RTL8811CU (AWUS036EACS) | Manutenção comunitária |
| kmod-rtw89 / kmod-rtl8852bu | Em desenvolvimento | Realtek RTL8832BU (AWUS036AX / AXER) | Suporte USB rtw89 gradualmente integrado, requer kernel mais recente |

### 2.3 Pré-requisitos: Suporte ao Núcleo USB

Antes de instalar os drivers de WiFi, é necessário garantir que o OpenWrt tenha suporte ao núcleo USB habilitado:

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

A maioria das versões atuais do OpenWrt já inclui o kmod-usb-core, mas o usbutils (que fornece o comando lsusb) deve ser instalado manualmente.

## 3. Análise das Especificações da Placa de Rede ALFA e do Chipset

Até setembro de 2026, a linha de produtos de placas de rede USB sem fio da ALFA Network é a seguinte (base: 9 modelos):

| Modelo | Nível Wi-Fi | Chipset | Interface | Pacote de Drivers OpenWrt |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | kmod-mt7921u (23.05+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | kmod-mt7921u (23.05+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | kmod-rtw89 (em desenvolvimento) / rtl8852bu personalizado |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Como acima |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | kmod-rtl8812au-ct (comunidade) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | kmod-mt76x0u (oficial) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | kmod-mt76x2u (oficial)⭐ Recomendado |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | kmod-rtl8812au-ct (cobertura) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | kmod-rtl8821cu (comunidade) |

## 4. Modelos Aplicáveis e Chipsets

### 4.1 Classificação de Recomendação

| Nível de Recomendação | Modelo (Chipset) | Descrição |
|---|---|---|
| ⭐ Recomendação Forte | AWUS036ACM (MT7612U) | Drivers oficialmente maduros e estáveis, suportam AP / STA / Monitor / Injection, a melhor escolha no OpenWrt |
| ✅ Recomendado | AWUS036ACHM (MT7610U) | Drivers oficiais, dual band mas apenas 433Mbps, adequado para cenários de baixa potência |
| ✅ Recomendado (nova versão) | AWUS036AXML / AXM (MT7921AUN) | Wi-Fi 6E, drivers oficiais, requer OpenWrt 23.05+ e kernel 5.15+ |
| ⚠️ Disponível mas com Atenção | AWUS036ACH (RTL8812AU) | Drivers da comunidade, versão 24.10 com relatórios de crash de kernel, recomendado usar 23.05 |
| ⚠️ Disponível mas com Atenção | AWUS036ACS (RTL8811AU) | Como acima, coberto pelo driver 8812au |
| ⚠️ Disponível mas com Atenção | AWUS036EACS (RTL8811CU) | Drivers da comunidade, estabilidade média |
| ❌ Não Recomendado | AWUS036AX / AXER (RTL8832BU) | Wi-Fi 6, suporte rtw89 USB ainda em desenvolvimento, a maioria das versões do OpenWrt não pode ser usada diretamente |

### 4.2 Requisitos de Hardware do Roteador

| Item | Requisito Mínimo | Requisito Recomendado |
|---|---|---|
| Porta USB | USB 2.0 (AWUS036ACHM / ACS / EACS) | USB 3.0 (AWUS036ACH / ACM / AX Series) |
| Flash | 16MB (instalação de drivers + dependências) | 32MB+ |
| RAM | 128MB | 256MB+ (modo AP + múltiplos usuários) |
| Versão do OpenWrt | 21.02+ | 23.05.x (versão estável) |

## 5. Requisitos de Ambiente

### 5.1 Ambiente de Software

- Versão estável do OpenWrt: 23.05.x (kernel 5.15) ou 24.10.x (kernel 6.6)
- Fonte de Pacotes: Repositório oficial do opkg (https://downloads.openwrt.org/releases/{version}/packages/{arch}/)
- Conexão de Rede: Durante a instalação do driver, o roteador deve estar conectado à internet (através da porta WAN)

### 5.2 Ambiente de Hardware

- Roteador compatível com OpenWrt que possua porta USB 2.0 / 3.0
- Modelos de alta potência (AWUS036ACH) são recomendados para usar um Hub USB 3.0 com alimentação, para evitar fornecimento insuficiente de energia na porta USB do roteador
- O AWUS036AXML possui interface USB-C, é necessário garantir que o roteador possua porta USB-C ou usar um adaptador USB-C to USB-A

## 6. Determinação de Compatibilidade

### Matriz de Compatibilidade ALFA Modelos Atuais × OpenWrt

| Modelo | Chipset | Método de Driver | Detecção de USB | STA Internet | Modo AP | Monitor | Versão Mínima | Avaliação Geral |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | kmod-mt76x2u | ✅ | ✅ | ✅ | ✅ | 21.02+ | ⭐ Melhor |
| AWUS036ACHM | MT7610U | kmod-mt76x0u | ✅ | ✅ | ✅ | ⚠️ Limitada | 21.02+ | ✅ Boa |
| AWUS036AXML | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ Limitada | 23.05+ | ✅ Boa |
| AWUS036AXM | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ Limitada | 23.05+ | ✅ Boa |
| AWUS036ACH | RTL8812AU | kmod-rtl8812au-ct | ✅ | ✅ | ✅ | ⚠️ Limitada | 22.03+（24.10 com crash） | ⚠️ Utilizável |
| AWUS036ACS | RTL8811AU | kmod-rtl8812au-ct | ✅ | ✅ | ⚠️ | ❌ | 22.03+ | ⚠️ Utilizável |
| AWUS036EACS | RTL8811CU | kmod-rtl8821cu | ✅ | ⚠️ | ❌ | ❌ | 23.05+ | ⚠️ Utilizável |
| AWUS036AX | RTL8832BU | rtw89（em desenvolvimento） | ⚠️ | ❌ | ❌ | ❌ | Necessita compilação personalizada | ❌ Não recomendado |
| AWUS036AXER | RTL8832BU | rtw89（em desenvolvimento） | ⚠️ | ❌ | ❌ | ❌ | Necessita compilação personalizada | ❌ Não recomendado |

Critérios de Determinação: Disponibilidade dos pacotes kmod na biblioteca oficial do OpenWrt (23.05 / 24.10) + relatórios de usuários do fórum do OpenWrt. Os drivers de chipsets Realtek são mantidos pela comunidade, sua estabilidade e integridade funcional são inferiores à série MediaTek mt76.

## 7. Detalhado Passo a Passo de Configuração

### 7.1 Pré-requisitos: Ativação do Suporte ao USB

**Passo 1: Acesso SSH ao Router OpenWrt**

```bash
ssh root@192.168.1.1
```

**Passo 2: Atualização do Repositório de Pacotes e Instalação do Suporte ao USB**

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

**Passo 3: Insira a Placa de Rede ALFA e Confirme a Detecção USB**

```bash
lsusb
# Saída esperada (AWUS036ACM / MT7612U):
# Bus 002 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

### 7.2 Rota A: Modelos com Chip MediaTek (AWUS036ACM / ACHM / AXML / AXM)

Tomando como exemplo o AWUS036ACM (MT7612U):

**Passo 1: Instalação do Pacote de Drivers**

```bash
# AWUS036ACM (MT7612U)
opkg install kmod-mt76-usb kmod-mt76x2u

# AWUS036ACHM (MT7610U) — Substitua por
# opkg install kmod-mt76-usb kmod-mt76x0u

# AWUS036AXML / AXM (MT7921AUN) — Substitua por (necessário 23.05+)
# opkg install kmod-mt7921u
```

**Passo 2: Instalação das Ferramentas de Gestão de Rede**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**Passo 3: Verificação da Interface de Rede**

```bash
iw dev
# Espera-se que apareça a interface wlan0 ou wlan1
```

**Passo 4: Scaneamento de WiFi Próximo (Verificação de Funcionalidade)**

```bash
iw dev wlan0 scan | grep -E "SSID|signal"
```

**Passo 5: Configuração como Cliente STA (Conectando-se a um AP Existente)**

Edite /etc/config/wireless:

```text
config wifi-device 'radio1'
       option type 'mac80211'
       option path 'platform/usb1/1-1/1-1:1.0'
       option channel 'auto'
       option htmode 'VHT80'

config wifi-iface 'wifinet2'
       option device 'radio1'
       option mode 'sta'
       option network 'wwan'
       option ssid 'SeuNomeDeWiFi'
       option encryption 'psk2'
       option key 'SuaSenhaDeWiFi'
```

**Passo 6: Reinício do Serviço de Rede**

```bash
/etc/init.d/network restart
```

**Passo 7: Configuração como Ponto de Acesso (AP) (Compartilhamento de Rede)**

Edite /etc/config/wireless, alterando o mode para ap:

```text
config wifi-iface 'wifinet2'
   option device 'radio1'
   option mode 'ap'
   option network 'lan'
   option ssid 'ALFA-OpenWrt-AP'
   option encryption 'psk2'
   option key 'SuaSenhaDoPontoDeAcesso'
```

**Passo 8: Ativação do Modo de Escuta (Testes de Penetração)**

```bash
opkg install aircrack-ng
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
iw dev wlan0 set channel 6
# Verificação
iw dev wlan0 info
# type deve exibir monitor
```

### 7.3 Rota B: Modelos com Chip Realtek (AWUS036ACH / ACS / EACS)

Tomando como exemplo o AWUS036ACH (RTL8812AU):

**Passo 1: Instalação do Driver Comunitário**

```bash
opkg update
opkg install kmod-rtl8812au-ct

# AWUS036EACS (RTL8811CU) — Substitua por
# opkg install kmod-rtl8821cu
```

**Passo 2: Instalação das Ferramentas de Gestão de Rede**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**Passo 3: Verificação da Interface**

```bash
iw dev
# Nota: A interface nomeada pelo driver rtl8812au-ct pode ser wlan0 ou wlan1
```

A configuração é semelhante aos Passos 5-7 da Rota 7.2 (Configuração STA / AP).

**Passo 4: Modo de Escuta**

```bash
# O driver rtl8812au-ct suporta o modo de escuta
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
# A função de injecção de pacotes é limitada, recomenda-se usar o chip mt76 para testes de penetração
```

**Passo 5: Caso de Kernel Crash (Problema Conhecido na Versão 24.10)**

```bash
# Retorne para a versão estável 23.05 ou use drivers compilados personalizados
# Verifique os logs de crash
logread | grep -i "panic\|crash\|rtl8812"
```

### 7.4 Rota C: Modelos Wi-Fi 6 (AWUS036AX / AXER, RTL8832BU)

⚠️ Esta rota requer a compilação personalizada do OpenWrt, não recomendada para usuários comuns.

**Passo 1: Verificação da Versão do OpenWrt para Suporte ao rtw89 USB**

```bash
opkg list | grep rtw89
# Sem resultados, indica que a versão não inclui
```

**Passo 2: Se necessário, compilação personalizada do Imagem do OpenWrt**

Adicione kmod-rtw89 e o firmware correspondente.

**Sugestão Alternativa**: Para necessidades de uso de rede Wi-Fi 6 em roteadores OpenWrt, o AWUS036AXML (MT7921AUN) é a melhor escolha atualmente.

## 8. Erros Comuns e Solução

| Sintoma | Possível Causa | Solução |
|---|---|---|
| O comando `lsusb` não vê a placa de rede ALFA | Núcleo USB não instalado / Alimentação insuficiente | Verifique se o `kmod-usb-core`, o `kmod-usb2` e o `kmod-usb3` foram instalados; use um Hub USB com alimentação |
| O comando `lsusb` vê, mas `iw dev` não tem interface | Driver não instalado / Driver incompatível | Instale o pacote `kmod` correspondente; verifique `dmesg` para erros de firmware |
| O comando `opkg install kmod-mt76x2u` retorna "versão do kernel não coincide" | Versão do OpenWrt e a versão do repositório de pacotes não coincidem | Execute `opkg update` e tente novamente; verifique se a versão do firmware coincide com a arquitetura do repositório |
| Falha ao inicializar o modo AP (erro do hostapd) | Driver não suporta AP / Configuração de canal incorreta | Verifique se o chip suporta o modo AP; tente fixar o canal (por exemplo, 6 ou 149); verifique o Regulatory Domain |
| Modo de escuta não consegue injetar pacotes | Driver não suporta injecção / Colisão de canal | A série MediaTek mt76 oferece o melhor suporte; a função de injecção do Realtek 8812au-ct é limitada; verifique `airmon-ng check kill` |
| AWUS036ACH desliga durante a alta potência | Alimentação USB insuficiente | Use um Hub USB 3.0 com alimentação; defina `option txpower '20'` no arquivo `/etc/config/wireless` para reduzir a potência |
| Kernel panic após a instalação do `rtl8812au-ct` na versão 24.10 | Problema de compatibilidade conhecido do driver | Retorne para a versão estável 23.05.x; ou siga o issue no GitHub para esperar pela correção |
| MT7921 (AXML/AXM) não pode usar a faixa de 6GHz | Restrição do Regulatory Domain / Versão do kernel | É necessário kernel 5.19+ e configuração correta da região regulamentar Wi-Fi 6E; o suporte de 6GHz no OpenWrt 23.05 ainda está em teste |

## 9. Restrições Conhecidas

- O driver do chip Realtek é mantido pela comunidade: `kmod-rtl8812au-ct`, `kmod-rtl8821cu` não são mantidos oficialmente pelo OpenWrt, não há garantia de estabilidade e cronograma de atualizações.
- A versão 24.10 do `rtl8812au-ct` apresentou relatórios de crash do kernel: é recomendável que os usuários de chips Realtek mantenham-se na versão 23.05.x.
- Suporte insuficiente para Wi-Fi 6 (RTL8832BU): o driver USB `rtw89` está em desenvolvimento, a maioria das versões do OpenWrt não pode usar diretamente AWUS036AX / AXER.
- Restrições de desempenho no modo AP: ao usar WiFi USB como AP, a taxa de transferência é menor do que a do WiFi integrado no roteador (largura de banda do conector USB + overhead do driver).
- Diferenças nas funções de monitoramento / injecção: a série MediaTek mt76 oferece o suporte mais completo; as funções de injecção do chip Realtek são limitadas, não são apropriadas para testes de penetração profissionais.
- Recursos de hardware do roteador: em roteadores de baixo custo (16MB Flash / 128MB RAM), a instalação do driver pode resultar em espaço insuficiente, afetando outras funcionalidades.
- Interferência de USB 3.0: dispositivos USB 3.0 podem interferir no WiFi 2.4GHz, é recomendável usar portas USB 2.0 ou hubs USB bem isolados.
- Uso simultâneo de várias placas de rede: ao usar WiFi integrado no roteador + WiFi USB ao mesmo tempo, podem ocorrer conflitos de canais ou competição por recursos.
- ⚠️ **O mantenedor do driver RTL8832BU (AWUS036AX/AXER) publicou uma recomendação de evitar seu uso**: a seção 4.1 deste documento está marcada como "❌ Não recomendado", a razão não é apenas o desenvolvimento do driver `rtw89` em andamento, mas também o mantenedor morrownr declarou publicamente que a série de chips é "muito ruim, suspeitando de problemas no próprio chip", recomendando que os usuários Linux evitem usá-la neste momento (fonte: seção 10).
- **É necessário esclarecer a expressão de limiar da versão do kernel**: a escrita "MT7921AUN requer OpenWrt 23.05+ e kernel 5.15+" na seção 4.1 pode ser enganosa - o driver `mt7921u` realmente precisa de **kernel 5.19+** no Linux desktop (veja a declaração original do mantenedor), mas os pacotes oficiais do OpenWrt geralmente utilizam o mecanismo de backport para incluir cedo, portanto, o OpenWrt 23.05 (embora indique kernel básico 5.15) ainda há relatórios de usuários que instalaram com sucesso o `kmod-mt7921u`. **A determinação deve ser feita com base no resultado real da consulta `opkg list` da versão do cliente, não pelo número da versão do kernel**.

Condições de refutação: se o pacote subsequente do OpenWrt corrigir o problema de crash do kernel do `rtl8812au-ct` na versão 24.10, as recomendações da seção 4.1 e 6 para o AWUS036ACH podem ser atualizadas de "manter 23.05"; se o suporte do `rtw89 USB` for oficialmente incluído no repositório oficial do OpenWrt, a avaliação "não recomendado" para o AWUS036AX / AXER deve ser reavaliada; se o oficial emitir uma declaração completa de suporte para a frequência de 6GHz do MT7921, a descrição das restrições do AXML / AXM deve ser atualizada.

## 10. Fontes de Referência URL

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| Documentação Oficial do OpenWrt | Entrada de documentos oficiais do OpenWrt (configuração sem fio / gerenciamento de pacotes) | https://openwrt.org/docs/start | ✅ Verificado | 2026-09-03 |
| Fórum Oficial do OpenWrt | Entrada de discussão sobre drivers USB WiFi | https://forum.openwrt.org/ | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Driver upstream RTL8812AU para Linux | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| Catálogo de Produtos da ALFA Network (Yupitek) | Especificações de produtos atuais da ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | Declaração oficial do mantenedor do driver: Recomenda evitar o chip rtl8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Verificado | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko só aparecerá no núcleo com kernel 5.19+ (palavra do mantenedor) | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ Verificado | 2026-09-03 |
| Fórum Oficial do OpenWrt — Melhor adaptador USB WiFi para Raspberry Pi 4B | Relatórios de usuários sobre a instalação bem-sucedida do kmod-mt7921u no OpenWrt 23.05.0 | https://forum.openwrt.org/t/best-usb-wifi-dongle-for-raspberry-pi-4b/160103 | ✅ Verificado | 2026-09-03 |

Artigos Relacionados: [O adaptador sem fio ALFA suporta DD-WRT?](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[O adaptador sem fio ALFA suporta Tomato?](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[O adaptador sem fio ALFA suporta NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[O adaptador sem fio ALFA suporta NVIDIA Jetson Nano?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Declaração de Isenção de Responsabilidade: A determinação de compatibilidade deste artigo é baseada no repositório oficial de pacotes do OpenWrt 23.05.x / 24.10.x. A disponibilidade de pacotes pode variar dependendo da arquitetura do roteador (ath79 / ramips / mvebu / x86, etc.). Os drivers de chip Realtek são mantidos pela comunidade e sua estabilidade pode variar conforme as versões. Recomenda-se usar modelos de chip MediaTek (AWUS036ACM como preferência) como a escolha prioritária para o OpenWrt USB WiFi.
