---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM: Guia Completo 5GHz (2026)"
description: "Guia completo de compatibilidade para HAK5 WiFi Pineapple MK7 com ALFA AWUS036ACM (MT7612U) — Modo Monitor 5GHz plug-and-play, injeção de pacotes e extensão PineAP. Configuração passo a passo com comandos verificados."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
---

O HAK5 WiFi Pineapple Mark VII é o padrão para auditoria de segurança sem fio portátil. Mas tem uma limitação: o rádio integrado opera apenas em **2,4 GHz**. Em 2026, a maioria das redes migrou para 5 GHz.

É aqui que entra o **ALFA AWUS036ACM**. É um dos poucos adaptadores [oficialmente confirmados](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters) pela Hak5, e funciona **sem compilação de drivers** graças ao driver `mt76x2u` já incluído no kernel do Firmware MK7 2.x.

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

## 5. Recomendação

**O ALFA AWUS036ACM é o melhor adaptador atualmente disponível para expandir o WiFi Pineapple Mark VII para 5 GHz.**

👉 [Página do Produto AWUS036ACM](/pt/products/alfa/awus036acm/)

*Precisa de ajuda? Contate o suporte Yupitek: [yupitek.com/support](/pt/support/)*
