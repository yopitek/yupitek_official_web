---
title: "Suporte do Adaptador de Rede Wireless ALFA para o Tomato"
date: 2026-09-03
draft: false
slug: "alfa-tomato-router-compatibility"
tags:
  - "ALFA"
  - "Tomato"
  - "FreshTomato"
  - "Router"
  - "Broadcom"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "Guia de Hardware"
description: "ALFA系列無驅動支援Tomato，recomenda OpenWrt para USB WiFi."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumo do Problema

Pergunta do cliente: “O adaptador sem fio USB da série ALFA pode ser utilizado em roteadores que tenham sido flashados com o firmware Tomato?”

Conclusão breve: Atualmente, todos os modelos ativos da série ALFA não possuem suporte a drivers para o Tomato (inclusive as versões derivadas, como FreshTomato e AdvancedTomato), não sendo recomendável seu uso. O Tomato é a plataforma de firmware de terceiro para roteadores que oferece o menor suporte a adaptadores WiFi USB, com o foco de desenvolvimento completamente voltado para o WiFi integrado em roteadores com chipsets Broadcom. Para uso de adaptadores WiFi USB em roteadores, é recomendável a utilização do OpenWrt.

Corpo da análise: 9 modelos de adaptadores USB da série ALFA (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Análise das Especificações e Requisitos do Software de Objetivo

### 2.1 O que é Tomato

Tomato é um kernel de roteador open source histórico, originalmente desenvolvido por Jonathan Zarate, e desde então derivou várias ramificações:

| Versão Derivada | Estado de Manutenção | Plataformas Suportadas |
|---|---|---|
| Versão Original Tomato | Parado (início da década de 2010) | Roteadores Broadcom MIPS |
| Tomato by Shibby | Parado | Broadcom MIPS / ARM |
| AdvancedTomato | Parado | Broadcom (versão GUI revisada de Shibby) |
| FreshTomato | Ativo | Broadcom MIPS / ARM (BCM47xx / BCM53xx) |
| Toastman Tomato | Parado | Broadcom MIPS |

### 2.2 Frame de Suporte ao WiFi USB do Tomato

A filosofia de design central do Tomato é "fornecer um kernel de terceira parte simplificado e estável para roteadores Broadcom", e suas funcionalidades USB são principalmente suportadas:

| Tipo de Funcionalidade USB | Estado de Suporte |
|---|---|
| Dispositivo de Armazenamento USB (pendrive / disco rígido) | ✅ Suporte Completo (Samba / FTP / DLNA) |
| Impressora USB | ✅ Suporte (p910nd / CUPS) |
| Modem 3G/4G | ⚠️ Suporte Parcial |
| Placa de Rede WiFi USB | ❌ Praticamente sem suporte |

O kernel do Tomato pré-definido inclui o módulo de driver de WiFi de código fechado (módulo wl) para o WiFi integrado nos roteadores Broadcom, sem qualquer driver de WiFi USB. O sistema de gerenciamento de pacotes (ipkg / Optware) também não oferece pacotes de drivers de WiFi USB.

### 2.3 Limitações Chave

- Tomato suporta apenas roteadores com chipsets Broadcom, enquanto os ports USB dos roteadores Broadcom geralmente são usados apenas para armazenamento / impressoras
- Embora o FreshTomato ainda esteja em manutenção, o foco do desenvolvimento é a correção de bugs na plataforma Broadcom, não há planos para adicionar drivers de WiFi USB
- O espaço do sistema de arquivos do Tomato é extremamente pequeno (geralmente 4-16MB), então, mesmo que queira traduzir manualmente o driver, não há espaço para instalá-lo
- O Tomato não possui sistemas de gerenciamento de pacotes modernos como o opkg, então não é possível instalar drivers kmod de forma simples, como no OpenWrt

## 3. Análise das Especificações e Chipsets da Placa de Rede ALFA

Até setembro de 2026, a linha de produtos de placas de rede sem fio USB da ALFA Network é a seguinte (baseada em 9 modelos):

| Modelo | Nível Wi-Fi | Chipset | Interface | Estado do Driver Tomato |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ Sem |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ Sem |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ Sem |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ Sem |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ❌ Sem |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ❌ Sem |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ❌ Sem |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ❌ Sem |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ❌ Sem |

## 4. Modelos Aplicáveis e Chipsets

### 4.1 Modelos ALFA extremamente antigos possíveis no Tomato (descontinuados)

| Modelo | Chipset | Módulo de Driver Linux | Descrição |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | Teoricamente carregável, mas o Tomato não o inclui por padrão; é necessário compilar manualmente o módulo do kernel, o que é extremamente improvável |
| AWUS036H | Realtek RTL8187L | rtl8187 | O mesmo, suporta apenas 2.4GHz / 54Mbps, descontinuado há mais de dez anos |

⚠️ Mesmo que esses modelos antigos sejam compatíveis com o Tomato, o usuário precisará compilar manualmente os módulos de driver correspondentes para a versão do kernel, e o espaço do sistema de arquivos do Tomato geralmente não é suficiente para a instalação. Isso não é considerado "suporte", mas sim um "hack extremamente avançado".

### 4.2 Modelos atuais que não são compatíveis com o Tomato

Todos os modelos atuais ALFA (veja a tabela do Capítulo 3) não são compatíveis com o Tomato por os seguintes motivos:

- Chipsets Realtek (RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU): O Tomato não possui nenhum driver correspondente e não pode ser instalado através da gestão de pacotes
- Chipsets MediaTek (MT7612U / MT7610U / MT7921AUN): O Tomato não inclui os drivers mt76 / mt7921 e a equipe de desenvolvimento do FreshTomato não tem planos de adicioná-los
- Mesmo que o lsusb consiga identificar o dispositivo (se o Tomato tiver o suporte ao núcleo USB habilitado), isso apenas identifica o nível de pilha de controle de USB e não permite a criação de uma interface de rede

## 5. Requisitos de Ambiente

Devido à incompatibilidade do modelo ALFA em Tomato, esta seção lista as condições extremas necessárias para que o cliente insista em tentar:

| Item | Requisito |
|---|---|
| Hardware do roteador | Roteador com chip Broadcom, com porta USB 2.0, Flash ≥ 32MB, RAM ≥ 256MB |
| Versão do Tomato | Versão mais recente do FreshTomato (as versões antigas têm suporte USB mais fraco) |
| Ambiente de compilação cruzada | Necessário configurar a ferramenta de compilação cruzada correspondente à arquitetura Broadcom (MIPS / ARM) |
| Código-fonte do driver | Necessário obter o código-fonte do driver Linux correspondente ao chip e modificá-lo para ser compatível com a versão do kernel do Tomato |
| Capacidade técnica | Necessário ter capacidade de desenvolvimento de módulos do kernel Linux, compilação cruzada e depuração |
| Custo de tempo | Estimado em várias horas até vários dias, com baixa probabilidade de sucesso |

Conclusão: Para 99,9% dos usuários, a utilização da placa de rede WiFi USB ALFA em Tomato é inviável.

## 6. Determinação de Compatibilidade

### Matriz de Compatibilidade ALFA Modelos Atuais × Tomato

| Modelo | Chipset | Suporte ao Núcleo USB | Detecção USB | STA Internet | Modo AP | Monitoramento | Avaliação Geral |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ⚠️ Necessário ativar o núcleo USB | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036AXM | MT7921AUN | ⚠️ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036AX | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036AXER | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036ACH | RTL8812AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036ACHM | MT7610U | ⚠️ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036ACM | MT7612U | ⚠️ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036ACS | RTL8811AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Não suportado |
| AWUS036EACS | RTL8811CU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Não suportado |

Critério de Determinação: O Tomato (inclusive FreshTomato) não inclui nenhuma driver para chipsets de WiFi USB moderno em sua biblioteca oficial. O objetivo de design do Tomato nunca incluiu a funcionalidade de expansão de WiFi via USB.

## 7. Passo a Passo Detalhado de Configuração

Devido ao modelo ALFA atual não ser compatível com Tomato, esta seção fornece passos de verificação e soluções alternativas.

### 7.1 Verificação do Suporte do Router Tomato para WiFi USB (Passos de Troubleshooting)

**Passo 1: Acesso à Interface de Gerenciamento do Tomato**

Acesse o navegador e insira 192.168.1.1 (ou o IP do seu roteador).

**Passo 2: Verificação da Ativação do Core USB**

- Acesse USB and NAS > Suporte USB
- Confirme que Core USB Support, Suporte USB 2.0, Suporte USB 3.0 (se houver) estão marcados
- Confirme Suporte ao Dispositivo Wireless USB (se houver essa opção) — A maioria das versões do Tomato não possui essa opção

**Passo 3: Insira a Placa de Rede ALFA no Porta USB do Roteador**

**Passo 4: Verificação da Detecção USB pelo SSH / Telnet**

```bash
# Verificação da existência do lsusb (o Tomato pode não ter por padrão)
which lsusb
# Se não houver lsusb, verifique /proc/bus/usb ou dmesg
cat /proc/bus/usb/devices
# Ou
dmesg | grep -i usb
```

**Passo 5: Verificação da Interface de Rede**

```bash
ifconfig -a
# Se houver apenas vlan0 / br0 / eth0 / eth1 (interfaces internas do roteador), e não wlan0 / wlan1, isso significa que o WiFi USB não foi ativado
```

**Passo 6: Verificação dos Kernel Modules Disponíveis**

```bash
lsmod
# Espera-se que haja apenas wl (driver WiFi integrado Broadcom), et (driver de rede Ethernet) etc.
# Não há drivers USB WiFi como mt76 / rtl8812 / cfg80211 / mac80211
```

**Passo 7: Verificação da Possibilidade de Instalação de Pacotes Adicionais**

```bash
# O Tomato usa ipkg, mas o conteúdo da biblioteca de pacotes é muito limitado
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# O resultado esperado deve estar vazio
```

### 7.2 Soluções Recomendadas

#### Solução 1: Mude para OpenWrt (altamente recomendado)

Se o seu modelo de roteador também suportar OpenWrt, recomendamos que você atualize o firmware do Tomato para OpenWrt. O OpenWrt possui uma biblioteca completa de drivers para WiFi USB, suportando a maioria dos modelos ALFA.

- Confirme se o seu roteador está na lista de dispositivos suportados pelo OpenWrt
- Se for suportado, consulte [Compatibilidade do Router ALFA com OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) para os passos de instalação

#### Solução 2: Uso do WiFi Interno do Roteador

O Tomato possui suporte completo para o WiFi interno dos roteadores Broadcom, se sua necessidade for navegação geral ou pontos de acesso (AP), você pode usar o WiFi interno do roteador sem a necessidade de conectar a placa de rede ALFA.

#### Solução 3: Troca de Hardware

Se você precisa de funcionalidades específicas do WiFi USB (como saída de potência alta, modo de monitoramento, injetor de pacotes), o Tomato não pode atender a essas necessidades. Recomendamos:

- Usar roteadores que suportem OpenWrt + placa de rede ALFA
- Ou usar pequenos servidores x86 com OpenWrt / pfSense + placa de rede ALFA
- Ou usar a placa de rede ALFA diretamente em computadores com Kali Linux / Ubuntu

## 8. Erros Comuns e Solução

| Sintoma | Possível Causa | Solução |
|---|---|---|
| A interface de gerenciamento do Tomato não possui a opção "USB Wireless Device Support" | A versão do Tomato não traduziu o suporte USB WiFi | Isso é normal, não um bug; a maioria das versões do Tomato não possui essa funcionalidade |
| Após inserir a placa de rede ALFA, o dmesg detecta o USB mas não há interface de rede | Faltando driver | Isso não pode ser resolvido, o Tomato não possui driver correspondente |
| Quer instalar manualmente o pacote ipkg, mas não encontra o driver WiFi | A biblioteca de pacotes do Tomato não possui driver USB WiFi | Isso é normal; é recomendado usar o OpenWrt |
| O modelo antigo ALFA (RT3070) é detectado no Tomato mas não consegue se conectar | Driver incompleto / firmware faltando | Mesmo que o chip seja antigo, não há garantia de que será compatível; é recomendado usar o OpenWrt |
| Após flashar o Tomato, o porta USB só pode ler pen drives | A funcionalidade USB do Tomato é projetada apenas para armazenamento / impressoras | Isso é um comportamento esperado; o Tomato não suporta USB WiFi |

## 9. Limitações Conhecidas

- **Nenhum driver USB WiFi incluído**: O núcleo oficial do Tomato (inclusive o FreshTomato) não inclui nenhum driver para chipsets USB WiFi modernos, o que é a limitação mais fundamental.
- **Driver Broadcom de código fechado e vínculo**: O Tomato depende do driver wl de código fechado da Broadcom e não pode coexistir com drivers USB WiFi de arquitetura mac80211 / cfg80211, que são de código aberto.
- **Falta de ecossistema de gerenciamento de pacotes**: A biblioteca de pacotes ipkg do Tomato possui um conteúdo muito limitado, ao contrário do OpenWrt, que possui milhares de pacotes instaláveis.
- **Espaço insuficiente em Flash / RAM**: A maioria dos roteadores Tomato possui apenas 4-16MB de Flash, o que não permite a instalação de drivers, mesmo que sejam compilados.
- **Direção de desenvolvimento diferente**: A equipe de desenvolvimento do FreshTomato prioriza a reparação da estabilidade da plataforma Broadcom e não investe recursos na adição de suporte a USB WiFi.
- **Nenhum suporte para monitoramento / injecção**: A arquitetura WiFi do Tomato (driver Broadcom wl) não suporta funcionalidades de teste de penetração e, portanto, a conexão de um USB WiFi externo não altera essa situação.
- **Nenhum suporte para expansão em modo AP**: Mesmo que os chipsets antigos possam carregar o driver, a interface de configuração de rede do Tomato não suporta a configuração do USB WiFi em modo AP.

Contra-argumentos: Se a versão futura do FreshTomato incluir explicitamente suporte a drivers USB WiFi no release notes oficiais ou se a comunidade apresentar um projeto de移植 do mt76 / rtl8812au amplamente validado, a avaliação de "não suportado" descrita no capítulo 6 precisará ser reavaliada; se o FreshTomato mudar para um núcleo de arquitetura mac80211 de código aberto, a descrição das limitações também precisará ser atualizada.

## 10. Fontes de Referência URL

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| Site Oficial do FreshTomato | Lista de versões mais recentes e dispositivos suportados pelo FreshTomato | https://freshtomato.org/ | ✅ Verificado | 2026-09-03 |
| Documentação Oficial do OpenWrt | Drivers USB WiFi e configurações sem fio (referência comparativa) | https://openwrt.org/docs/start | ✅ Verificado | 2026-09-03 |
| Fórum Oficial do OpenWrt | Discussões sobre drivers USB WiFi (referência comparativa) | https://forum.openwrt.org/ | ✅ Verificado | 2026-09-03 |
| Catálogo de Produtos da ALFA Network (Yupitek) | Especificações dos produtos atuais da ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |

Artigos Relacionados: [A Placa de Rede Wireless ALFA suporta DD-WRT?](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[A Placa de Rede Wireless ALFA suporta OpenWrt?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)｜[A Placa de Rede Wireless ALFA suporta NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[A Placa de Rede Wireless ALFA suporta NVIDIA Jetson Nano?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Declaração de Isenção de Responsabilidade: A determinação de compatibilidade deste artigo se baseia no núcleo oficial do Tomato / FreshTomato e no repositório de pacotes. Em alguns casos extremamente raros, usuários avançados podem tentar compilar cruzadamente para implementar funcionalidades básicas em chips antigos, mas isso não faz parte do suporte oficial e não é recomendado para usuários comuns. Para cenários que exigem o uso de USB WiFi em roteadores, o OpenWrt é a única solução de firmware de terceiros viável.
