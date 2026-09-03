---
title: "Carta Técnica: Suporte do Adaptador de Rede Wireless ALFA para o Firmware DD-WRT"
date: 2026-09-03
draft: false
slug: "alfa-ddwrt-router-compatibility"
tags:
  - "ALFA"
  - "DD-WRT"
  - "Router"
  - "Broadcom"
  - "Atheros"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "Guia de Hardware"
description: "ALFA USB WiFi não suportado no DD-WRT; recomenda-se OpenWrt."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumo do Problema

Pergunta do cliente: “O adaptador USB sem fio da série ALFA pode ser utilizado em roteadores que tenham o firmware DD-WRT instalado?”

Resumo breve: Atualmente, todos os modelos ativos da série ALFA (AWUS036ACH / ACM / ACHM / ACS / EACS / AX / AXER / AXML / AXM, totalizando 9 modelos) não contam com suporte oficial de drivers para o DD-WRT e não são recomendados para uso. (Critério de avaliação: 9 adaptadores USB da ALFA em serviço) O suporte USB WiFi do DD-WRT é limitado a um número reduzido de chipsets Atheros / Ralink antigos e requer uma versão específica de compilação. Se for necessário usar um adaptador USB WiFi em um roteador, é recomendável optar pelo OpenWrt (veja [Compatibilidade do adaptador USB sem fio ALFA com o OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)).

## 2. Análise das Especificações e Requisitos do Software de Objetivo

### 2.1 O que é o DD-WRT

DD-WRT é um firmware de terceira parte para roteadores, de código aberto, projetado principalmente para roteadores com chip WiFi integrado (Broadcom / Atheros / Ralink SoC). Sua arquitetura central é o kernel do Linux, mas os programas de driver estão pré-instalados apenas com os drivers wireless correspondentes ao SoC do roteador alvo.

### 2.2 Frame de Suporte ao WiFi USB do DD-WRT

O DD-WRT instala drivers adicionais através do sistema de gerenciamento de pacotes ipkg, mas os drivers USB WiFi no repositório oficial são extremamente escassos:

| Driver | Estado no DD-WRT | Chip Correspondente (Modelos ALFA) |
|---|---|---|
| ath9k_htc | Parcialmente integrado em algumas versões | Atheros AR9271 (como TP-Link TL-WN722N v1) |
| rt2800usb | Parcialmente integrado em algumas versões | Ralink RT3070 / RT3370 / RT5370 (antigos ALFA AWUS036NH) |
| rtl8812au | Sem pacote oficial | Realtek RTL8812AU (AWUS036ACH) |
| mt76 / mt76x2u | Sem pacote oficial | MediaTek MT7612U / MT7610U (AWUS036ACM / ACHM) |
| mt7921u | Sem pacote oficial | MediaTek MT7921AUN (AWUS036AXML / AXM) |
| rtl8852bu / rtw89 | Sem pacote oficial | Realtek RTL8832BU (AWUS036AX / AXER) |

### 2.3 Limitações Chave

- O núcleo do DD-WRT prioriza o suporte ao WiFi integrado no roteador, enquanto o WiFi USB é uma funcionalidade secundária
- As versões de compilação do DD-WRT para diferentes modelos de roteadores variam, resultando em uma grande diferença na disponibilidade de drivers
- Mesmo que a comunidade faça compilações adicionais com drivers incluídos, muitas vezes não é possível instalar devido à falta de espaço em Flash / RAM
- O DD-WRT quase não suporta o modo de monitoramento (Monitor Mode) e a injecção de pacotes (Packet Injection) para o WiFi USB

## 3. Análise das Especificações e Chipsets da Placa de Rede ALFA

Até setembro de 2026, a linha de produtos de placas de rede USB sem fio da ALFA Network é a seguinte:

| Modelo | Nível Wi-Fi | Chipset | Interface | Estado do Driver Linux |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | Linux in-kernel (mt7921u, requer kernel 5.12+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | Linux in-kernel (mt7921u, requer kernel 5.12+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree (rtl8852bu / rtw89) |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree (rtl8852bu / rtw89) |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | Out-of-tree (8812au, morrownr manutenção) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | Linux in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | Linux in-kernel (mt76x2u) |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | Out-of-tree (8812au coberto) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | Out-of-tree (8821cu, morrownr manutenção) |

## 4. Modelos Aplicáveis e Chipsets

### 4.1 Modelos ALFA Possíveis para o DD-WRT (Descontinuados / Antigos)

| Modelo | Chipset | Driver | Estado do DD-WRT |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | Parte das versões do DD-WRT inclui, apenas 2.4GHz / 150Mbps |
| AWUS036H | Realtek RTL8187L | rtl8187 | Muito antigo, parte das versões suporta, apenas 2.4GHz / 54Mbps |
| AWUS050NH | Atheros AR9170 | carl9170 / ar9170usb | Muito antigo, dual-band, mas descontinuado há muitos anos |

### 4.2 Modelos Atuais Não Suportados pelo DD-WRT

Todos os modelos atuais ALFA (veja a tabela do Capítulo 3) não são oficialmente suportados pelo DD-WRT, devido aos seguintes motivos:

- Chipsets Realtek (RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU): Não há pacotes de drivers out-of-tree correspondentes para o DD-WRT
- Chipsets MediaTek (MT7612U / MT7610U / MT7921AUN): Drivers mt76 / mt7921 não incluídos no DD-WRT
- Mesmo que o roteador tenha uma porta USB e o nível de hardware possa identificar o dispositivo (lsusb pode ver VID/PID), sem drivers não é possível estabelecer uma interface de rede

## 5. Requisitos de Ambiente

Se o cliente ainda desejar tentar usar a placa de rede ALFA no DD-WRT, deve atender aos seguintes requisitos:

| Item | Requisito |
|---|---|
| Hardware do roteador | Deve ter uma porta USB 2.0 / 3.0 e o DD-WRT deve ter o suporte ao núcleo USB habilitado (Services > USB) |
| Versão do DD-WRT | Deve ser a versão mais recente do BrainSlayer / Kong que suporte o roteador, pois as versões antigas têm menos drivers |
| Espaço de Flash | No mínimo 16MB de espaço de Flash (a maioria dos roteadores de entrada possui apenas 4-8MB, o que não permite a instalação de drivers adicionais) |
| RAM | No mínimo 128MB de RAM (o driver de WiFi USB e o hostapd consomem memória) |
| Alimentação | A porta USB deve fornecer corrente suficiente (ao usar a saída de alta potência AWUS036ACH pode alcançar 800mA+, é recomendável usar um Hub USB com fonte de alimentação) |

## 6. Determinação de Compatibilidade

### Matriz de Compatibilidade ALFA Modelos Atuais × DD-WRT

| Modelo | Chipset | Detecção de Conexão USB | Carregamento de Driver | STA Internet | Modo AP | Monitor | Avaliação Geral |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ✅（lsusb） | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036AXM | MT7921AUN | ✅ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036AX | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036AXER | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036ACH | RTL8812AU | ✅ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036ACHM | MT7610U | ✅ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036ACM | MT7612U | ✅ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036ACS | RTL8811AU | ✅ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036EACS | RTL8811CU | ✅ | ❌ | ❌ | ❌ | ❌ | Não suportado |

Critério de Avaliação: A biblioteca oficial do DD-WRT e a pré-compactação do núcleo não incluem os drivers de WiFi USB para o chipset mencionado acima. A visibilidade do dispositivo através do lsusb apenas indica a identificação da camada de conexão USB e não garante a funcionalidade de rede.

## 7. Detalhamento Extremo de Passo a Passo para Configuração

Devido à incompatibilidade do modelo ALFA ativo com o DD-WRT, esta seção fornece duas alternativas:

### Rota A: Verificar se o seu roteador DD-WRT realmente não suporta (passos de depuração)

**Passo 1: Acessar a Interface de Gestão do DD-WRT**

Acesse o navegador e insira `192.168.1.1` (ou o IP do seu roteador).

**Passo 2: Ativar Suporte USB**

- Acesse Services > USB
- Marque Core USB Support、USB 2.0 Support、USB 3.0 Support (se houver)
- Marque USB Wireless Device Support (se houver essa opção)
- Clique em Save > Apply Settings

**Passo 3: Insira a placa de rede ALFA no porta USB do roteador**

**Passo 4: Acessar o roteador via SSH para verificar**

```bash
# Verificar se o dispositivo USB foi detectado
lsusb
# A saída esperada deve conter o VID/PID da placa de rede ALFA, por exemplo:
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter

# Verificar se a interface de rede foi criada
ip link show
# Se não houver novas interfaces como wlan0 / wlan1, o driver não foi carregado

# Verificar o log do kernel
dmesg | tail -30
# Se aparecer "no driver" ou apenas mensagens de enumeração de USB, verifique a falta do driver
```

**Passo 5: Verificar os módulos de driver WiFi disponíveis**

```bash
# Listar os drivers wireless carregados
lsmod | grep -E "ath|rt2|rtl|mt76|mac80211|cfg80211"
# Se apenas houver drivers do WiFi integrado no roteador (como wl / b43 / ath9k), o driver USB WiFi está ausente
```

**Passo 6: Tentar instalar o driver da comunidade (se houver)**

```bash
ipkg update
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# Se o resultado da busca estiver vazio, verifique se a versão do DD-WRT não possui drivers disponíveis
```

### Rota B: Sugestão de Alternativa — Usar OpenWrt

Se o cliente precisar usar a placa de rede ALFA USB WiFi no roteador, é altamente recomendável que o firmware do roteador seja atualizado de DD-WRT para OpenWrt. O OpenWrt possui uma biblioteca ativa de drivers WiFi USB, suportando chipsets MT7612U / MT7610U / RTL8812AU, entre outros. Para obter detalhes sobre a compatibilidade do roteador ALFA com o OpenWrt, consulte [ALFA 无线网卡是否支援 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/).

## 8. Erros Comuns e Solução

| Sintoma | Possível Causa | Solução |
|---|---|---|
| O comando `lsusb` não mostra a placa de rede ALFA | Alimentação USB insuficiente / Falha de contato / DD-WRT não habilitou o núcleo USB | Verifique em Services > USB se o serviço está habilitado; troque o porta USB ou use um Hub USB com alimentação |
| O comando `lsusb` mostra, mas o `ip link` não tem a interface wlan | Faltando o driver correspondente para o chip | Confira se a versão do DD-WRT possui o driver necessário; na maioria dos casos, não há solução, recomenda-se usar o OpenWrt |
| Existe a interface wlan, mas não consegue escanear AP | Driver não completamente suportado / Conflito de modo de escuta | Verifique se o `dmesg` tem erros de carregamento do firmware; confirme a configuração do Regulatory Domain |
| Configurações perdidas após o reboot do roteador | Espaço NVRAM insuficiente no DD-WRT | Evite instalar drivers adicionais em roteadores de baixa potência; considere atualizar o hardware ou usar o OpenWrt |
| Desconexões intermitentes ao usar a saída de alta potência do AWUS036ACH | Alimentação insuficiente do porta USB | Use um Hub USB 3.0 com alimentação; reduza a configuração de TX Power |

## 9. Limitações Conhecidas

- **Falta de Driver**: O DD-WRT oficial não fornece drivers USB WiFi para os modelos atuais da ALFA, o que é a limitação mais fundamental.
- **Recursos de Hardware**: A maioria dos roteadores que podem ser flashados com o DD-WRT tem um Flash (4-16MB) e RAM (32-128MB) limitados, mesmo que haja drivers, pode não ser possível instalá-los.
- **Não Suporte a Monitoramento/Injeção**: A arquitetura USB WiFi do DD-WRT não suporta o Monitor Mode e Packet Injection necessários para testes de penetração.
- **Instabilidade em Modo AP**: Mesmo que os chipsets Ralink antigos possam funcionar, o modo AP do USB WiFi no DD-WRT frequentemente apresenta problemas de desconexão e de desempenho.
- **Fragmentação de Versões**: As versões de compilação do DD-WRT para diferentes modelos de roteadores diferem significativamente, não garantindo que um driver de uma versão funcione em outra.
- **Não Mais Ativo**: O ritmo de desenvolvimento do DD-WRT está diminuído, a possibilidade de adição de drivers USB WiFi é baixa.
- **Suplemento**: Mesmo que se ignore as limitações do DD-WRT, os modelos AWUS036AX / AXER (RTL8832BU) são recomendados pelo mantenedor morrownr para que os usuários do Linux evitem essa série de chipsets (veja [Compatibilidade do Roteador ALFA com OpenWrt](https://yupitek.com/pt-br/blog/alfa-openwrt-router-compatibility/) na seção 9), não sendo um problema apenas do DD-WRT.

Contra-argumentos: Se o cliente estiver usando versões de compilação comunitárias como BrainSlayer / Kong que incluem drivers adicionais, a situação de suporte pode ser diferente; esta avaliação se baseia na versão oficial publicada.

## 10. Fontes de Referência URL

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| Wiki Oficial DD-WRT | Entrada principal para instalação, suporte e FAQ | https://wiki.dd-wrt.com/wiki/Main_Page | ✅ Verificado | 2026-09-03 |
| Wiki Oficial DD-WRT — Instalação | Instrução de instalação (com suporte USB) | https://wiki.dd-wrt.com/wiki/Installation | ✅ Verificado através do link da página principal | 2026-09-03 |
| Documentação Oficial OpenWrt | Referência de comparação de WiFi USB | https://openwrt.org/docs/start | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Driver RTL8812AU para Linux (não integrado no DD-WRT) | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| Catálogo de Produtos ALFA Network (Yupitek) | Especificações dos produtos atuais da ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |

Artigos Relacionados: [O adaptador Wi-Fi ALFA suporta OpenWrt?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) | [O adaptador Wi-Fi ALFA suporta Tomato?](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)

Aviso de Isenção de Responsabilidade: A determinação de compatibilidade deste artigo se baseia no estado do driver do chip e no repositório oficial do DD-WRT. Existem muitas versões de compilação personalizadas da comunidade DD-WRT, e os resultados reais podem variar se o cliente usar versões não oficiais. Recomenda-se que os clientes usem o OpenWrt como a escolha preferencial para o WiFi USB no roteador.
