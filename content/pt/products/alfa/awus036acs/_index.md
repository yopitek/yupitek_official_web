---
title: "ALFA AWUS036ACS — Adaptador USB AC600 Banda Dupla (Pesquisa de Segurança Básica)"
description: "ALFA AWUS036ACS, Realtek RTL8811AU, AC600 banda dupla USB 2.0, 1× antena RP-SMA removível de 2 dBi, suporta Monitor Mode e injeção de pacotes — ideal para pesquisa de segurança básica."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "RP-SMA", "Monitor Mode", "Kali Linux", "Básico"]
---

{{< alert "warning" >}}
**Aviso Legal**: Os recursos de Monitor Mode e injeção de pacotes destinam-se exclusivamente a testes de segurança autorizados, pesquisa educacional e testes de penetração legais. Certifique-se sempre de ter permissão explícita do proprietário da rede alvo antes de usar.
{{< /alert >}}

## Visão Geral do Produto

O AWUS036ACS é o ponto de entrada mais acessível da Alfa na linha de banda dupla 802.11ac com suporte a modo monitor e injeção de pacotes. Alimentado pelo chipset Realtek RTL8811AU, é compacto e leve com uma única antena RP-SMA removível que pode ser atualizada para melhor alcance. Embora não seja tão poderoso quanto o ACH ou ACM, é uma escolha prática para iniciantes em pesquisa de segurança sem fio ou usuários que precisam de um adaptador 5 GHz econômico com capacidade de antena externa.

> **Aviso sobre macOS:** Todos os adaptadores ALFA têm suporte limitado para macOS. macOS 10.15 Catalina e posterior, e todos os Macs com Apple Silicon (M1/M2/M3), **não são suportados**. O AWUS036ACS suporta até macOS 10.14 Mojave (somente Mac Intel).

## Características Principais

- Chipset Realtek RTL8811AU — modo monitor e injeção de pacotes suportados
- WiFi 5 (802.11ac) banda dupla — 2.4 GHz (150 Mbps) + 5 GHz (433 Mbps) = AC600
- 1× conector RP-SMA fêmea com 1× antena mini removível de 2 dBi — atualizável para antenas de painel ou alto ganho
- Fator de forma compacto — perfil pequeno para fácil portabilidade
- Interface USB 2.0 (USB-A) — compatível com qualquer porta USB
- Compatível com a antena de painel banda dupla Alfa APA-M25 para recepção direcional
- Suporta Kali Linux no Raspberry Pi (KaliPi) — instalação do driver via DKMS

## Especificações Técnicas

| Parâmetro | Valor |
|---|---|
| Chipset | Realtek RTL8811AU |
| Padrões WiFi | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bandas de Frequência | 2.4 GHz (150 Mbps) · 5 GHz (433 Mbps) |
| Velocidade Máxima Combinada | AC600 (150 + 433 Mbps) |
| Conector de Antena | 1× RP-SMA fêmea |
| Antena Incluída | 1× dipolo mini banda dupla, ganho de 2 dBi |
| Interface USB | USB 2.0 Type-A |
| Sensibilidade de Recepção | 802.11b: −85 dBm · 802.11g: −69 dBm · 802.11n: −68 dBm · 802.11ac: −59 dBm |
| Segurança Sem Fio | WPA2 / WPA / WEP / 802.1X |
| País de Origem | Taiwan |

> ⚠️ **NOTA:** Apenas USB 2.0 — velocidade máxima do barramento de dados 480 Mbps. Taxa de transferência limitada a 433 Mbps. Para velocidade máxima, use AWUS036ACM ou AWUS036ACH com USB 3.0.

## Suporte de SO

| Sistema Operacional | Status | Observações |
|---|---|---|
| Windows XP–11 | ✅ Suportado | Driver disponível no site da Alfa |
| macOS 10.5–10.14 | ⚠️ Limitado | macOS 10.15+ e Apple Silicon NÃO suportados |
| Ubuntu | ✅ Suportado | Instalação manual do driver DKMS necessária (morrownr/8821au). Sem suporte integrado no kernel. |
| Kali Linux | ✅ Suportado | Modo monitor + injeção de pacotes suportados. Driver da comunidade do morrownr GitHub. |
| NetHunter (Android) | ✅ Suportado | Conexão USB OTG; RTL8811AU tem compatibilidade confirmada com NetHunter |

## Hardware Compatível

| Hardware | Status | Observações |
|---|---|---|
| Raspberry Pi 3B+/4/5 | ✅ Suportado | Instalação específica para KaliPi disponível via morrownr DKMS. |
| PC Desktop/Laptop | ✅ Suportado | USB-A padrão |
| Mac (Intel) | ⚠️ Limitado | Apenas macOS 10.5–10.14 |

## Capacidades Avançadas

| Recurso | Status |
|---|---|
| Monitor Mode | ✅ Sim |
| Injeção de Pacotes | ✅ Sim |
| Modo Soft AP | ✅ Sim |
| Bluetooth | ❌ Não |
| VIF | ⚠️ Limitado |

## Conteúdo da Embalagem

- 1× Adaptador AWUS036ACS
- 1× Antena mini dipolo banda dupla removível de 2 dBi

## Recursos e Links

| Recurso | Link |
|---|---|
| Página Oficial do Produto | https://www.alfa.com.tw/products/awus036acs_1 |
| Documentação Oficial | https://docs.alfa.com.tw/Product/AWUS036ACS/ |
| Driver Linux (RTL8811AU) | https://github.com/morrownr/8821au-20210708 |

## Download da Ficha Técnica

[📄 Baixar ficha técnica AWUS036ACS](/docs/alfa/AWUS036ACS_spec.pdf)

## Galeria

{{< gallery >}}<img src="/images/products/alfa/awus036acs_image_1.png" alt="ALFA AWUS036ACS" />{{< /gallery >}}

---

{{< alert "info" >}}
Precisa de uma cotação? [Entre em contato](/pt/contact/), oferecemos consultoria de compra detalhada.
{{< /alert >}}
