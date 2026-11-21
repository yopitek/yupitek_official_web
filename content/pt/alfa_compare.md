---
title: "Comparação de adaptadores USB Wi-Fi ALFA Network"
description: "Comparação completa de especificações de 9 adaptadores USB Wi-Fi ALFA Network: chipset, driver Linux, capacidades de monitor / injeção / AP, com resultados medidos em um ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17)."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
---

A tabela abaixo compara os 9 adaptadores USB Wi-Fi ALFA Network. As colunas Monitor, Injeção, AP e handshake de ponta a ponta são resultados medidos nos testes da Yopitek em um ASUS GX10 (Ubuntu 24.04 LTS / ARM64 / kernel 6.17), com equipamentos e a rede Wi-Fi do próprio escritório — não valores copiados de fichas técnicas.

## Comparação completa de especificações

Role a tabela horizontalmente no celular; toque no nome do modelo para ver a página do produto.

| Modelo | Wi-Fi | Chipset | Bandas | Velocidade máx. | USB | Antenas | MIMO | Modo Monitor | Injeção de pacotes | Handshake (teste GX10) | Driver Linux | Tipo de driver | Modo AP | Potência máx. | Bluetooth | Ideal para |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [AWUS036AXML](/pt/products/alfa/awus036axml/) | Wi-Fi 6E | MT7921AUN | 2.4 + 5 + 6 GHz | 3000 Mbps | USB-C 3.2 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Sim | ❌ Falha no 6.17 padrão | ❌ Não (a injeção falha) | No kernel ≥5.18 | No kernel (Plug & Play) | ✅ Nativo | 3.6W | BT 5.2 | Wi-Fi 6E + Linux + USB-C |
| [AWUS036AXM](/pt/products/alfa/awus036axm/) | Wi-Fi 6E | MT7921AUN | 2,4 + 5 + 6 GHz (6 GHz não testado) | 3000 Mbps | USB-A 3.2 L | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Sim | ❌ Falha no 6.17 padrão | ❌ Não (a injeção falha) | No kernel ≥5.18 | No kernel (Plug & Play) | ✅ Nativo | 3.6W | BT 5.2 | Wi-Fi 6E + antena dupla |
| [AWUS036AX](/pt/products/alfa/awus036ax/) | Wi-Fi 6 | RTL8832BU | 2.4 + 5 GHz | 1200 Mbps | USB-A 3.2 Gen 1 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Sim | ✅ Sim | ✅ Completo (.22000) | No kernel ≥6.17 | No kernel (Plug & Play) | ✅ Nativo | 3.6W | — | Wi-Fi 6 + hotspot AP |
| [AWUS036AXER](/pt/products/alfa/awus036axer/) | Wi-Fi 6 | RTL8832BU | 2.4 + 5 GHz | 1800 Mbps | USB-A 3.2 | Integrada (nano) | 2×2 MIMO | ✅ Sim | ✅ Sim | ✅ Completo (.22000) | No kernel ≥6.17 | No kernel (Plug & Play) | ✅ Nativo | 3.0W | — | Adaptador compacto para viagem |
| [AWUS036ACH](/pt/products/alfa/awus036ach/) | Wi-Fi 5 | RTL8812AU | 2.4 + 5 GHz | 867 Mbps | USB-C 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅✅ Melhor | ✅✅ Melhor | ✅ Completo (.22000) | No kernel ≥6.13 | No kernel (Plug & Play) | ✅ Nativo | 3.6W | — | Padrão de referência no Kali Linux |
| [AWUS036ACM](/pt/products/alfa/awus036acm/) | Wi-Fi 5 | MT7612U | 2.4 + 5 GHz | 867 Mbps | USB-A 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Sim | ✅ Sim | ✅ Completo (.22000) | No kernel ≥4.19 | No kernel (Plug & Play) | ✅ Nativo | 3.0W | — | Plug and play no Linux |
| [AWUS036ACHM](/pt/products/alfa/awus036achm/) | Wi-Fi 5 | MT7610U | 2.4 + 5 GHz | 433 Mbps | USB 2.0 | 1× RP-SMA 5dBi | 1×1 SISO | ✅ Sim | ✅ 2.4 GHz / ⚠️ 5 GHz somente transmissão | ✅ Completo (.22000) | No kernel ≥4.19 | No kernel (Plug & Play) | ✅ Nativo | — | — | AC600 compacto, plug and play no Linux |
| [AWUS036ACS](/pt/products/alfa/awus036acs/) | Wi-Fi 5 | RTL8811AU | 2.4 + 5 GHz | 433 Mbps | USB-A 2.0 | 1× RP-SMA 2dBi | 1×1 SISO | ✅ Sim | ✅ Sim | ✅ Completo (.22000) | No kernel ≥6.13 | No kernel (Plug & Play) | ✅ Nativo (5 GHz testado como 802.11a 20 MHz; VHT80 não testado) | 2.5W | — | Testes de segurança com orçamento reduzido |
| [AWUS036EACS](/pt/products/alfa/awus036eacs/) | Wi-Fi 5 | RTL8821CU | 2.4 + 5 GHz | 433 Mbps | USB 2.0 nano | Integrada 2 dBi | 1×1 SISO | ✅ Sim | ✅✅ Melhor | ✅ Completo (.22000) | No kernel ≥6.2 | No kernel (Plug & Play) | ✅ Nativo (5 GHz testado como 802.11a 20 MHz; VHT80 não testado) | 2.5W | BT 4.2 | Wi-Fi doméstico no Windows + BT |

## Guia rápido de compra — por caso de uso

**🔴 Kali Linux / Pentest** — Melhor: AWUS036ACH

RTL8812AU — modo monitor e injeção de pacotes mais maduros no Kali; 100% de injeção em ambas as bandas no GX10 (kernel 6.17). O rtw88_8812au está no kernel desde o 6.13. Dica: em kernels mais antigos, use o driver DKMS do aircrack-ng fixado no commit estável 63cf0b4.

**🔵 Usuário avançado Wi-Fi 6E (tri-banda)** — Melhor: AWUS036AXML or AWUS036AXM

MT7921AUN — driver Linux no kernel desde o 5.18, banda de 6 GHz (verificada no AXML; AXM não testado), Bluetooth 5.2. Observação: a injeção de pacotes falha no kernel 6.17 padrão (regressão do mac80211 desde o 6.16), portanto não é indicado para pentest. Formatos: o AXML tem conector USB-C destacável e corpo de antena única com duas saídas; o AXM tem formato embutido em L com USB-A.

**🌐 Soft-AP / Emulação de hotspot** — Melhor: AWUS036ACM

MT7612U — suporte plug and play ao modo AP via hostapd nativo no kernel Linux. Diferentemente dos adaptadores Realtek, que exigem builds personalizados e problemáticos do hostapd, o MediaTek funciona de forma fluida e estável para simulação de Rogue AP / Evil Twin.

**🟢 Uso diário no Linux (Plug & Play)** — Melhor: AWUS036ACM

MT7612U — no kernel desde a versão 4.19, sem instalação de driver no Ubuntu / Debian / Fedora. A experiência mais simples no Linux.

**🟣 Raspberry Pi / Embarcados** — Melhor: AWUS036ACM

Baixo consumo de energia + driver no kernel o tornam ideal para o Raspberry Pi. Observação: modelos de alta potência (ACH, AXML) consomem até 3.6W e exigem um hub USB alimentado para evitar quedas de tensão e reinicializações da conexão no Pi.

**🟡 Segurança econômica / Iniciantes** — Melhor: AWUS036ACS

RTL8811AU — porta de entrada acessível, com suporte a modo monitor e injeção de pacotes. Antena única, design compacto.

**⚡ Adaptador compacto para viagem** — Melhor: AWUS036AXER

Corpo nano ultrafino de apenas 10.5g. Wi-Fi 6 (1800 Mbps), USB-A. Ótimo para viagens de negócios e uso focado em Windows.

**🏠 Usuário doméstico Windows + Bluetooth** — Melhor: AWUS036EACS

RTL8821CU — combo de modo duplo Wi-Fi 5 + Bluetooth 4.2. Formato nano. Ideal para desktops que precisam de rede sem fio e BT rapidamente, sem slot PCIe.

**🍎 Compatibilidade com macOS** — Melhor: AWUS036ACH or AWUS036AXML

O ACH tem bom suporte no macOS por meio de driver de terceiros. O MT7921AUN do AXML tem suporte da comunidade no macOS. Verifique sempre a compatibilidade com a versão do macOS. Macs Intel têm melhor legado de drivers do que os da série M.

## Guia rápido de compra — por plataforma / SO

| Plataforma / SO | Primeira escolha | Alternativa | Observações |
|---|---|---|---|
| 🐧 Kali Linux | AWUS036ACH | AWUS036ACM | ACH = melhor modo monitor; ACM = suporte ao kernel mais fácil. Para VMs: configure a VM para usar um controlador USB 3.0 (xHCI) para evitar desconexões. |
| 🐧 Ubuntu / Debian | AWUS036ACM | AWUS036AXML | MT7612U no kernel desde o 4.19; MT7921AUN desde o 5.18 |
| 🐧 Raspberry Pi OS | AWUS036ACM | AWUS036ACH | Baixo consumo + driver no kernel; não é necessário compilar manualmente. Recomenda-se um hub USB alimentado para placas de alta potência, evitando reinicializações. |
| 🪟 Windows 10 / 11 | AWUS036AX | AWUS036EACS | Desempenho Wi-Fi 6; o EACS adiciona combo com Bluetooth |
| 🍎 macOS | AWUS036ACH | AWUS036AXML | Há drivers de terceiros; verifique a versão do macOS. Macs Intel têm drivers legados; o Apple Silicon (M1/M2/M3) tem suporte experimental restrito. |
| 📱 Android / NetHunter | AWUS036ACH | AWUS036ACS | RTL8812AU e RTL8811AU têm suporte ao NetHunter; são necessários adaptador OTG e compilação de kernel personalizado. |

---

Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia (novembro de 2026). Os relatórios por adaptador estão no [blog](/pt/blog/).
