---
title: "Adaptador Wi-Fi parou após atualização de kernel no Kali Linux? Corrigindo erros DKMS no RTL8812AU e assinaturas Secure Boot MOK"
date: 2026-08-18
draft: false
slug: "kali-linux-rtl8812au-dkms-secure-boot-mok-setup"
tags:
  - "Wireless"
  - "Hardware"
categories:
  - "Wireless Hardware"
  - "Technical Guide"
description: "Guia definitivo para resolver falhas de compilação DKMS do driver RTL8812AU no Kali Linux e assinar módulos de kernel via MOK com Secure Boot ativado."
featureimage: "/images/blog/05_dkms_mok_flow_blueprint.jpg"
author: "benny-lai"
lastmod: 2026-08-18
faq:
  - question: "Devo desativar o Secure Boot quando drivers não assinados são bloqueados?"
    answer: "Não é recomendado. A prática segura é registrar uma chave MOK via mokutil para assinar os módulos mantendo a segurança."
---

![Linux Kernel DKMS and Secure Boot MOK Flowchart](/images/blog/05_dkms_mok_flow_blueprint.jpg)

## Visão Geral e Contexto Técnico

Guia definitivo para resolver falhas de compilação DKMS do driver RTL8812AU no Kali Linux e assinar módulos de kernel via MOK com Secure Boot ativado.

### Principais Recursos e Destaques da Arquitetura

- **Plataforma de Hardware**: AWUS036ACH com circuito de RF de alta sensibilidade.
- **Compatibilidade de SO**: Suporte nativo nas principais distribuições Linux (Kali Linux, Ubuntu, Debian, Raspberry Pi OS).
- **Vantagens Centrais**: Antenas de alto ganho, estabilidade de sinal e operação plug-and-play.

### Análise Técnica e Implementação

Consulte o blueprint técnico acima para detalhes de pinagem e topologia. Em aplicações críticas como robótica móvel e FPV digital, a alimentação independente e drivers no kernel eliminam pontos de falha.

### Checklist de Pré-Implementação

1. Confirmar detecção do hardware via `lsusb`.
2. Instalar os pacotes de firmware mais recentes (`linux-firmware`).
3. Medir a intensidade de sinal (RSSI) antes da operação definitiva.
4. Respeitar as normas locais de uso do espectro de radiofrequência.

