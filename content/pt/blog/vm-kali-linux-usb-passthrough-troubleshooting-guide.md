---
title: "A máquina virtual Kali Linux não detecta a placa Wi-Fi? Manual de diagnóstico de USB Pass-Through no VirtualBox e VMware"
date: 2026-08-18
draft: false
slug: "vm-kali-linux-usb-passthrough-troubleshooting-guide"
tags:
  - "Wireless"
  - "Hardware"
categories:
  - "Wireless Hardware"
  - "Technical Guide"
description: "Guia passo a passo para resolver falhas de detecção de adaptadores Wi-Fi USB em máquinas virtuais Kali Linux com VirtualBox e VMware, configurando controladores XHCI e filtros."
featureimage: "/images/blog/08_usb_passthrough_blueprint.jpg"
author: "benny-lai"
lastmod: 2026-08-18
faq:
  - question: "Por que não posso usar o modo monitor no modo NAT ou Bridge?"
    answer: "Os modos NAT/Bridge emulam apenas uma placa Ethernet virtual (eth0). Somente o USB Pass-Through oferece controle direto do hardware."
---

![Virtual Machine USB Pass-Through Blueprint](/images/blog/08_usb_passthrough_blueprint.jpg)

## Visão Geral e Contexto Técnico

Guia passo a passo para resolver falhas de detecção de adaptadores Wi-Fi USB em máquinas virtuais Kali Linux com VirtualBox e VMware, configurando controladores XHCI e filtros.

### Principais Recursos e Destaques da Arquitetura

- **Plataforma de Hardware**: AWUS036AXML com circuito de RF de alta sensibilidade.
- **Compatibilidade de SO**: Suporte nativo nas principais distribuições Linux (Kali Linux, Ubuntu, Debian, Raspberry Pi OS).
- **Vantagens Centrais**: Antenas de alto ganho, estabilidade de sinal e operação plug-and-play.

### Análise Técnica e Implementação

Consulte o blueprint técnico acima para detalhes de pinagem e topologia. Em aplicações críticas como robótica móvel e FPV digital, a alimentação independente e drivers no kernel eliminam pontos de falha.

### Checklist de Pré-Implementação

1. Confirmar detecção do hardware via `lsusb`.
2. Instalar os pacotes de firmware mais recentes (`linux-firmware`).
3. Medir a intensidade de sinal (RSSI) antes da operação definitiva.
4. Respeitar as normas locais de uso do espectro de radiofrequência.

