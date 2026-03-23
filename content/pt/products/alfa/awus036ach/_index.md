---
title: "ALFA AWUS036ACH — Adaptador USB-C Sem Fio AC1200 Dual Band de Alta Potência"
description: "ALFA AWUS036ACH, Realtek RTL8812AU, AC1200 dual band, USB-C, 2 antenas externas 5 dBi, padrão ouro para pesquisa de segurança no Kali Linux, Monitor Mode e Packet Injection."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB-C", "Dupla Antena", "Monitor Mode", "Kali Linux", "Pesquisa de Segurança"]
---

{{< alert "warning" >}}
**Aviso Legal**: Os recursos Monitor Mode e Packet Injection são exclusivos para testes de segurança autorizados, pesquisa educacional e testes de penetração legais. Certifique-se de ter autorização explícita da rede alvo.
{{< /alert >}}

## Visão Geral do Produto

O AWUS036ACH é o adaptador mais icônico da ALFA Network — o padrão ouro para testes de penetração no Kali Linux desde 2017. Alimentado pelo comprovado chipset Realtek RTL8812AU, oferece suporte sólido a Monitor Mode e injeção de pacotes, amplificador de potência integrado para recepção de longo alcance e duas antenas desmontáveis de 5 dBi. Foi o primeiro adaptador WiFi 5 do mundo com conector USB Type-C.

> **Aviso macOS:** Todos os adaptadores ALFA têm suporte limitado ou nenhum para macOS. macOS 11 Big Sur e posteriores, e Apple Silicon (M1/M2/M3) **NÃO** são suportados. O suporte máximo é macOS 10.15 Catalina em Macs Intel.

## Características Principais

- Realtek RTL8812AU — chipset mais amplamente testado para pesquisa de segurança WiFi
- WiFi 5 (802.11ac) dual band AC1200 — 867 Mbps em 5 GHz, 300 Mbps em 2.4 GHz
- Amplificador de potência integrado — até 3× o alcance de placas típicas de notebook
- 2× RP-SMA fêmea com 2× antenas dual band de 5 dBi desmontáveis (atualizáveis)
- Primeiro adaptador WiFi 5 USB-C do mundo
- Suporte de clipe para monitor incluído
- Suporte a Packet Injection no Kali Linux desde Kali 2017.1
- Compatível com 802.11a/b/g/n

## Especificações Técnicas

| Parâmetro | Valor |
|-----------|-------|
| Chipset | Realtek RTL8812AU |
| Padrões WiFi | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bandas de Frequência | 2.4 GHz · 5 GHz (dual band) |
| Taxa Máxima de Dados | 802.11b: 11 Mbps · 802.11a/g: 54 Mbps · 802.11n: 300 Mbps · 802.11ac: 867 Mbps |
| Velocidade Máxima Combinada | AC1200 (867 + 300 Mbps) |
| Conectores de Antena | 2× RP-SMA fêmea |
| Antenas Incluídas | 2× dipolo omnidirecional dual band, 5 dBi |
| Interface USB | Type-C SuperSpeed USB (5 Gbps); retrocompatível com USB 2.0 |
| Amplificador de Potência | Sim — alcance estendido |
| Segurança Sem Fio | WPA3 / WPA2 / WPA / WEP / WPS / 802.1X |
| Acessórios | Clipe para monitor · Cabo USB |
| País de Origem | Taiwan |

## Suporte de SO

| Sistema Operacional | Status | Observações |
|--------------------|--------|-------------|
| Windows 10 / 11 | ✅ Suportado | Baixar driver do site da Alfa; suporte WPA3 (driver out. 2019+) |
| macOS 10.15 Catalina | ⚠️ Limitado | Instalação manual; macOS 11+ e Apple Silicon NÃO suportados |
| Ubuntu | ✅ Suportado | Instalação manual RTL8812AU DKMS; integrado no Ubuntu 24.10+ (kernel ≥ 6.14) |
| Kali Linux | ✅ Excelente | Desde Kali 2017.1; Monitor Mode + Packet Injection completo; usar driver aircrack-ng |
| NetHunter (Android) | ✅ Suportado | OTG USB; amplamente confirmado |

## Hardware Compatível

| Hardware | Status | Observações |
|----------|--------|-------------|
| Raspberry Pi 3B+/4/5 | ✅ Suportado | Driver manual via script morrownr DKMS |
| PC Desktop/Notebook | ✅ Suportado | USB-C ou USB-A (através do cabo incluído) |
| Mac (Intel) | ⚠️ Limitado | Máximo macOS 10.15 Catalina |

## Capacidades Avançadas

| Recurso | Status |
|---------|--------|
| Monitor Mode | ✅ Excelente (padrão ouro — comprovado pela comunidade desde 2017) |
| Packet Injection | ✅ Excelente |
| Modo Soft AP | ✅ Sim |
| Bluetooth | ❌ Não |
| VIF | ⚠️ Limitado (use AWUS036ACM para suporte VIF completo) |

## Conteúdo da Embalagem

- 1× Adaptador AWUS036ACH
- 2× Antenas dipolo dual band desmontáveis de 5 dBi
- 1× Cabo USB-C para USB-A
- 1× Clipe para monitor

## Recursos e Links

| Recurso | Link |
|---------|------|
| Página Oficial do Produto | https://www.alfa.com.tw/products/awus036ach_1 |
| Documentação Oficial | https://docs.alfa.com.tw/Product/AWUS036ACH/ |
| Driver (aircrack-ng, recomendado para Kali) | https://github.com/aircrack-ng/rtl8812au |
| Driver (morrownr, Linux geral) | https://github.com/morrownr/8812au-20210708 |

## Download da Ficha Técnica

| Documento | Download |
|-----------|---------|
| Ficha técnica oficial (PDF) | [📄 Baixar ficha técnica AWUS036ACH](/docs/alfa/AWUS036ACH_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ach_image_1.png" alt="ALFA AWUS036ACH" />
{{< /gallery >}}

---

## Acessórios de Antena Compatíveis

Todos os adaptadores USB ALFA utilizam um conector RP-SMA padrão. Faça upgrade com uma antena externa opcional para maior alcance e ganho:

| Antena | Frequência | Ganho | Tipo |
|--------|-----------|-------|------|
| [ALFA APA-M04](/pt/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | Painel interno direcional |
| [ALFA APA-M25](/pt/products/alfa/apa-m25/) | 2.4 / 5 GHz | 7 dBi | Painel interno dual band |
| [ALFA APA-M25-6E](/pt/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 7 dBi | Painel interno tri band |
| [ARS 25-57A](/pt/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 2.5 / 7 dBi | Omnidirecional exterior |
| [ARS NT5B7](/pt/products/alfa/ars-nt5b7/) | 2.4 / 5 GHz | 5 / 7 dBi | Omnidirecional |

{{< alert >}}
Precisa de uma cotação? [Entre em contato](/pt/contact/), oferecemos consultoria de compra detalhada.
{{< /alert >}}
