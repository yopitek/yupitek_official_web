---
title: "ACS ACR122U — Leitor NFC USB"
description: "ACS ACR122U, Leitor NFC USB, suporta ISO 14443 A/B, MIFARE, FeliCa, 13,56MHz, ideal para pesquisa NFC e desenvolvimento de aplicações."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["acr"]
tags: ["NFC", "RFID", "ISO 14443", "MIFARE", "USB", "Leitor de Cartão"]
faq:
  - question: "Preciso instalar um driver ACS para o ACR122U no Windows?"
    answer: "Não. A ACS afirma que o ACR122U é compatível com PC/SC e usa o driver Microsoft CCID padrão, portanto, nenhum driver ACS é necessário no Windows, pois o driver já está integrado ao sistema operacional."
  - question: "Quais cartões e tags o ACR122U pode ler e gravar?"
    answer: "De acordo com a ACS, ele acessa cartões ISO 14443-4 Tipo A e Tipo B, MIFARE, FeliCa e todos os quatro tipos de tags NFC (ISO/IEC 18092), com uma distância de leitura de cartão de até 50 mm, dependendo do tipo de tag. Seu sistema anti-colisão integrado significa que apenas uma tag é acessada por vez."
  - question: "Como programo o ACR122U na minha própria aplicação?"
    answer: "O ACR122U suporta PC/SC e CT-API por meio de um wrapper sobre o PC/SC. Comandos para tags ISO 18092 e para o LED e o buzzer são enviados como pseudo-APDUs. A ACS também lista suporte para Android 3.1 e superior."
---

ACR122U

## Visão Geral do Produto

O ACR122U é um leitor/gravador de cartões inteligentes sem contato conectado ao PC, baseado em tecnologia RFID de 13,56 MHz. Compatível com o padrão ISO/IEC 18092 NFC, suporta MIFARE®, ISO 14443 Type A/B e todos os quatro tipos de tags NFC. É um dispositivo USB plug-and-play compatível com PC/SC e CCID, com velocidade de acesso de até 424 Kbps, interface USB Full Speed (12 Mbps) e distância de operação de até 50 mm.

## Especificações Principais

| Especificação | Detalhes |
|---------------|----------|
| Frequência de Operação | 13,56 MHz |
| Distância de Operação | Até 50 mm (dependendo do tipo de etiqueta) |
| Velocidade de Leitura/Gravação | 106 Kbps / 212 Kbps / 424 Kbps |
| Interface USB | USB Full Speed (12 Mbps) |
| Tensão de Alimentação | 5V DC regulado |
| Corrente de Alimentação | 200 mA máx. / 100 mA normal / 50 mA standby |
| Tamanho da Antena | 50 mm × 40 mm |
| Dimensões | 98 × 65 × 12,8 mm |
| Peso | 70 g |
| Temperatura de Operação | 0°C – 60°C |
| Umidade | Máx. 90% (sem condensação) |
| MTBF | 408.500 horas |
| LED | 1 bicolor Vermelho/Verde (controlável pelo usuário) |
| Buzzer | Monotônico (controlável pelo usuário) |
| Slot SAM | 1 × ISO 7816-3 (opcional) |
| Conformidade | PC/SC, CCID, CE, FCC, RoHS |

## Recursos Principais

- Interface USB Full Speed
- Compatível com CCID e PC/SC, plug-and-play
- Velocidade de leitura/gravação até 424 Kbps
- Antena embutida, distância de leitura de cartão até 50 mm
- Suporta todos os 4 tipos de tags NFC (ISO/IEC 18092)
- Suporta MIFARE Ultralight C, MIFARE Plus, DESFire EV1
- Leitor/gravador para ISO 14443 Tipo A/B, MIFARE, FeliCa e tags NFC
- Anti-colisão embutida (1 tag por vez)
- LED bicolor e buzzer controláveis pelo usuário
- Slot SAM ISO 7816-3 opcional para segurança aprimorada
- Disponível em formato de módulo para integração em POS/controle de acesso
- Suporta PC/SC e CT-API

## Tipos de Etiquetas Suportadas

| Tipo de Etiqueta / Cartão | Padrão |
|--------------------------|--------|
| NFC Tag Type 1 | ISO 14443 Type A |
| NFC Tag Type 2 | ISO 14443 Type A |
| NFC Tag Type 3 | FeliCa |
| NFC Tag Type 4 | ISO 14443 Type A and B |
| MIFARE Classic (1K, 4K, MINI) | ISO 14443 Type A |
| MIFARE Ultralight / Ultralight C | ISO 14443 Type A |
| MIFARE Plus | ISO 14443 Type A |
| MIFARE DESFire / DESFire EV1 | ISO 14443 Type A |
| FeliCa | ISO 18092 |
| Cartões ISO 14443 Type A | ISO 14443 |
| Cartões ISO 14443 Type B | ISO 14443 |

## Sistemas Operacionais Suportados

- Windows CE 5.0, Windows Embedded Compact 6.0 / 7
- Windows XP, Vista, 7, 8, 8.1, 10
- Windows Server 2003 / 2008 / 2012 / 2016
- Linux®
- macOS®
- Solaris
- Android™ 3.1 e versões posteriores


## 📄 Ficha Técnica

| Recurso | Link |
|----------|------|
| 📄 ACR122U Especificação (PDF) | [Baixar PDF](/docs/acr/ACR122U_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/acr/acr122u.webp" alt="ACS ACR122U Leitor NFC" />
{{< /gallery >}}

---

{{< alert >}}
Precisa de uma cotação do produto? Por favor, [entre em contato conosco](/pt/contact/).
{{< /alert >}}

{{< faq >}}

[Guias de configuração e detalhes técnicos — doc.yupitek.com](https://doc.yupitek.com/acs/products/acr122u/)
