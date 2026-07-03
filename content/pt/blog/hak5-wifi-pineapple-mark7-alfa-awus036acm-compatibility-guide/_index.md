---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM: Guia Completo 5GHz (2026)"
description: "Guia completo de compatibilidade para HAK5 WiFi Pineapple MK7 com ALFA AWUS036ACM (MT7612U) — Modo Monitor 5GHz plug-and-play, injeção de pacotes e extensão PineAP. Configuração passo a passo com comandos verificados."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
author: "benny-lai"
lastmod: 2026-07-02

faq:
  - question: "O WiFi Pineapple Mark VII precisa de adaptador externo?"
    answer: "Sim. O radio integrado do MK7 suporta apenas 2.4 GHz. Em 2026, a maioria das redes já migrou para 5 GHz. Conectar um AWUS036ACM adiciona capacidade de monitoramento e injeção em 5 GHz."
  - question: "Por que o AWUS036ACM é plug-and-play no MK7?"
    answer: "O Firmware 2.x do MK7 já vem com o driver kmod-mt76x2u pré-instalado. O chipset MT7612U está integrado ao kernel desde o Linux 4.19, sem necessidade de compilação ou instalação."
  - question: "O USB 2.0 do MK7 limita o desempenho do AWUS036ACM?"
    answer: "O USB 2.0 limita o throughput a 150-250 Mbps, mas cargas de trabalho de pentest como captura de pacotes e coleta de handshakes não são afetadas. Apenas bridging de alto throughput  é limitado."
  - question: "Como ativar o Monitor Mode no MK7?"
    answer: "Após fazer login via SSH, execute airmon-ng start wlan3. A interface será renomeada para wlan3mon. Verifique o modo com iwconfig."
  - question: "Quais adaptadores ALFA são incompatíveis com o MK7?"
    answer: "AWUS036AX e AWUS036AXER usam o chip RTL8832BU, e o AWUS036EACS usa RTL8811CU. Os drivers não suportam modo monitor ou injeção, sendo todos incompatíveis."
---

O HAK5 WiFi Pineapple Mark VII é o padrão para auditoria de segurança sem fio portátil. Mas tem uma limitação: o rádio integrado opera apenas em **2,4 GHz**. Em 2026, a maioria das redes migrou para 5 GHz.

É aqui que entra o **ALFA AWUS036ACM**. É um dos poucos adaptadores [oficialmente confirmados](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters) pela Hak5, e funciona **sem compilação de drivers** graças ao driver `mt76x2u` já incluído no kernel do Firmware MK7 2.x.

{{< tldr >}}
O AWUS036ACM usa o chipset MT7612U, com driver pre-instalado no Firmware 2.x do MK7. Ao conectar, aparece como interface wlan3, suportando modo monitor de 5 GHz, injecao de pacotes e expansao PineAP. Configuracao completa em 10 minutos.
{{< /tldr >}}


---

## 1. Especificações

| Componente | Especificação |
|---|---|
| **SoC** | MediaTek MT7628AN (MIPS 24KEc) |
| **RAM** | 256 MB DDR2 |
| **USB Host** | 1× USB 2.0 Type-A |

> ✅ `kmod-mt76x2u` pré-carregado no Firmware 2.x — **plug-and-play**.

---

## 2. ALFA AWUS036ACM

| Especificação | Detalhe |
|---|---|
| **Chipset** | MediaTek MT7612U |
| **USB VID/PID** | `0E8D:7612` |
| **Bandas** | 2,4 GHz + 5 GHz |
| **Modo Monitor** | ✅ Suportado |
| **Injeção de Pacotes** | ✅ Suportada |

---

## 3. Configuração

```bash
ssh root@172.16.42.1
lsusb                          # Verificar USB
lsmod | grep mt76              # Verificar driver
iw dev                         # Verificar interface
airmon-ng check kill           # Ativar Modo Monitor
airmon-ng start wlan3
iw wlan3mon set channel 36     # Escanear 5 GHz
airodump-ng --band a wlan3mon
aireplay-ng --test wlan3mon    # Testar injeção
```

---

## 4. Resultados — todos os testes aprovados ✅

---

{{< faq >}}

## 5. Recomendação

**O ALFA AWUS036ACM é o melhor adaptador atualmente disponível para expandir o WiFi Pineapple Mark VII para 5 GHz.**

👉 [Página do Produto AWUS036ACM](/pt/products/alfa/awus036acm/)

*Precisa de ajuda? Contate o suporte Yupitek: [yupitek.com/support](/pt/support/)*

## Referências

1. [Documentacao oficial Hak5 — Lista de adaptadores 802.11ac compativeis](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)
2. [Repositorio GitHub do driver mt76 OpenWrt](https://github.com/openwrt/mt76)
3. [aircrack-ng — Site oficial do conjunto de ferramentas de seguranca sem fio](https://www.aircrack-ng.org/)
4. [Site oficial da ALFA Network — Especificacoes do produto AWUS036ACM](https://www.alfa.com.tw/)
5. [Linux Wireless — Documentacao do driver MT76x2U](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
