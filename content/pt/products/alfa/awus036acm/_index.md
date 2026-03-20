---
title: "ALFA AWUS036ACM — Adaptador AC1200 Dual Band USB 3.0 (Melhor Plug & Play para Linux)"
description: "ALFA AWUS036ACM, MediaTek MT7612U, AC1200 dual band USB 3.0, driver integrado no kernel Linux desde a versão 4.19 (plug & play, sem compilação). Monitor mode, packet injection e VIF completos. Melhor adaptador Alfa para Raspberry Pi."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB 3.0", "Dual Band", "Monitor Mode", "Kali Linux", "Raspberry Pi"]
---

{{< alert "warning" >}}
**Aviso Legal**: As funções de Monitor Mode e Injeção de Pacotes (Packet Injection) são exclusivamente para testes de segurança autorizados, pesquisa educacional e testes de penetração legais. Certifique-se de ter obtido autorização explícita do proprietário da rede alvo.
{{< /alert >}}

## Visão Geral do Produto

O AWUS036ACM é a primeira recomendação para usuários Linux que desejam configuração sem complicações. Seu chipset MediaTek MT7612U está integrado ao kernel Linux desde a versão 4.19 — o que significa que funciona imediatamente no Ubuntu, Kali Linux, Raspberry Pi OS, Arch Linux e praticamente qualquer distribuição moderna sem compilar uma única linha de código. Tem o mesmo tamanho físico e configuração de antenas que o AWUS036ACH, mas usa o driver estável integrado ao kernel da MediaTek. Monitor mode, packet injection e VIF (Interface Virtual) são totalmente suportados.

> **Aviso macOS:** Todos os adaptadores ALFA têm suporte limitado ou inexistente para macOS. macOS 11+ e Apple Silicon (M1/M2/M3) **NÃO são suportados**. O AWUS036ACM suporta no máximo macOS 10.12 Sierra — mais restritivo que a maioria dos outros modelos.

## Características Principais

- Chipset MediaTek MT7612U — driver Linux integrado ao kernel desde a versão 4.19 (plug & play, sem compilação)
- WiFi 5 (802.11ac) dual band AC1200 — até 867 Mbps em 5 GHz, 300 Mbps em 2.4 GHz
- 2× conectores RP-SMA fêmea com 2× antenas dipolo dual band de 5 dBi removíveis — formato físico idêntico ao AWUS036ACH
- Interface USB 3.0 (USB-A)
- Suporte completo a monitor mode, packet injection e modo AP
- Suporte a VIF (Interface Virtual) no Kali Linux
- Cabo de extensão USB 3.0 incluído
- Compatível com TAA — adequado para aquisição governamental dos EUA (compatível com GSA)
- Funciona imediatamente no Raspberry Pi OS — sem instalação de driver

## Especificações Técnicas

| Parâmetro | Valor |
|-----------|-------|
| Chipset | MediaTek MT7612U |
| Padrões WiFi | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bandas de Frequência | 2.4 GHz (2.412–2.472 GHz) · 5 GHz (5.15–5.825 GHz) |
| Larguras de Canal | 20 / 40 / 80 MHz |
| Velocidade Máxima | 5 GHz: até 867 Mbps · 2.4 GHz: até 300 Mbps |
| Velocidade Máxima Combinada | AC1200 (867 + 300 Mbps) |
| Conectores de Antena | 2× RP-SMA fêmea |
| Antenas Incluídas | 2× dipolo dual band, 5 dBi |
| Interface USB | USB 3.0 Type-A (retrocompatível com USB 2.0) |
| Potência de Saída | 802.11a: 20 dBm · 802.11b: 23 dBm · 802.11g: 23 dBm · 802.11n: 21 dBm · 802.11ac: 20 dBm |
| Sensibilidade de Recepção | 802.11a: −92 dBm · 802.11b: −97 dBm · 802.11g: −90 dBm · 802.11n: −90 dBm |
| Segurança Sem Fio | WPA2 / WPA / WEP / WPA-PSK / 802.1X |
| LED | Sim (alimentação + atividade WLAN) |
| Acessórios | Cabo de extensão USB 3.0 |
| País de Origem | Taiwan |

## Suporte de SO

| SO | Status | Notas |
|----|--------|-------|
| Windows XP–11 | ✅ Suportado | Driver do site da Alfa. Windows 10/11 recomendado. |
| macOS 10.7–10.12 | ⚠️ Limitado | Suporte oficial termina no macOS 10.12 Sierra. macOS 11+ e Apple Silicon NÃO suportados. |
| Ubuntu 19.04+ | ✅ Plug & Play | Driver mt76 integrado ao kernel (kernel ≥ 4.19). Zero instalação no Ubuntu 20.04 LTS e posteriores. |
| Kali Linux 2019.3+ | ✅ Plug & Play | Driver integrado ao kernel. Monitor mode confirmado. VIF suportado. Modo AP em 5 GHz pode requerer parâmetro `disable_usb_sg`. |
| NetHunter (Android) | ✅ Suportado | OTG USB; driver integrado ao kernel oferece maior compatibilidade Android que adaptadores RTL. |

## Hardware Compatível

| Hardware | Status | Notas |
|----------|--------|-------|
| Raspberry Pi 3B+/4/5 | ✅ Excelente | Funciona imediatamente no Raspberry Pi OS — sem instalação de driver. Melhor adaptador Alfa para Pi. |
| PC Desktop/Laptop | ✅ Suportado | USB-A padrão, com cabo de extensão incluído. |
| Mac (Intel) | ⚠️ Limitado | Apenas macOS 10.7–10.12. |

## Capacidades Avançadas

| Função | Status |
|--------|--------|
| Monitor Mode | ✅ Sim (integrado ao kernel, sem etapas extras em distros modernas) |
| Packet Injection | ✅ Sim |
| Modo Soft AP | ✅ Sim (AP 5 GHz: adicionar parâmetro `disable_usb_sg` para melhor desempenho) |
| Bluetooth | ❌ Não |
| VIF (Interface Virtual) | ✅ Sim (suporte VIF completo no Kali) |

## Conteúdo da Embalagem

- 1× Adaptador AWUS036ACM
- 2× Antenas dipolo dual band de 5 dBi removíveis
- 1× Cabo de extensão USB 3.0
- 1× CD de driver (Windows)

## Recursos e Links

| Recurso | Link |
|---------|------|
| Página oficial do produto | https://www.alfa.com.tw/products/awus036acm_1 |
| Documentação oficial | https://docs.alfa.com.tw/Product/AWUS036ACM/ |
| Informações do driver Linux (integrado ao kernel) | Driver mt76 — incluído no kernel Linux ≥ 4.19, sem instalação necessária |

## Download da Ficha Técnica

| Documento | Download |
|-----------|----------|
| Ficha técnica oficial (PDF) | [📄 Baixar ficha técnica AWUS036ACM](/docs/alfa/AWUS036ACM_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036acm_image_1.png" alt="ALFA AWUS036ACM" />
{{< /gallery >}}

---

{{< alert >}}
Precisa de uma cotação? [Entre em contato](/pt/contact/), oferecemos consultoria de compra detalhada.
{{< /alert >}}
