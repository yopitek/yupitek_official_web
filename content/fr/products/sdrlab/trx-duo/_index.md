---
title: "SDRLab TRX-duo — Plateforme SDR ZYNQ 16 bits Double Canal"
description: "SDRLab TRX-duo, plateforme SDR ADC/DAC 16 bits double canal, Xilinx Zynq 7010 SoC, compatible Red Pitaya, échantillonnage direct 10kHz–60MHz — conçu pour la recherche radio HF avancée."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "TRX-duo", "ZYNQ", "Red Pitaya", "16-bit ADC"]
---

## Caractéristiques

![SDRLab TRX-duo](/images/products/sdrlab/trx-duo.png)

- Conception transceiver double canal (2 RX + 2 TX), entièrement compatible avec l'écosystème logiciel Red Pitaya
- 2× ADC 16 bits haute précision LTC2208 offrant une large plage dynamique et une haute sensibilité
- DAC 14 bits pour la transmission double canal
- SoC Xilinx Zynq 7010 embarqué (ARM Cortex-A9 dual-core + FPGA) — exécuter le logiciel de décodage directement sur l'appareil
- Supporte le déploiement réseau distant pour construire des stations de réception SDR distantes
- Compatible avec les principaux logiciels SDR : HDSDR, SDR#, PowerSDR, SDR Console V3 et plus
- Proposé à environ la moitié du prix du Red Pitaya SDRlab 122-16 officiel (environ 622 USD)

## Spécifications Techniques

| Spécification | Valeur / Description |
|---------------|---------------------|
| Processeur | ARM Cortex-A9 dual-core (Zynq 7010 SoC) |
| FPGA | Xilinx Zynq 7010 |
| RAM | 512 MB |
| Plage de Fréquences de Réception | 10 kHz – 60 MHz (échantillonnage direct) |
| Canaux de Réception | 2 (connecteurs SMA) |
| Résolution ADC | 16 bits (LTC2208) |
| Taux d'Échantillonnage ADC | 125 MS/s |
| Tension Pleine Échelle ADC | 0,5 Vpp / −2 dBm |
| Plage de Tension d'Entrée | DC max. 50 V (couplage AC), 1 Vpp RF |
| Protection d'Entrée | Transformateur RF + couplage AC |
| Canaux d'Émission | 2 |
| Résolution DAC | 14 bits |
| Taux d'Échantillonnage DAC | 125 MS/s |
| Tension de Sortie d'Émission | 1 Vpp / +4 dBm |
| Impédance de Charge d'Émission | 50 Ω |
| Puissance d'Émission | ~2,5 mW (amplificateur de puissance externe requis) |
| Ethernet | 1 Gbit |
| USB | Type-C (USB 2.0) |
| Wi-Fi | Dongle Wi-Fi externe requis (non inclus) |
| GPIO d'Extension | 16× E/S numériques, 4× entrée analogique, 4× sortie analogique |
| Plage de Tension d'Entrée Analogique | 0–3,3 V |
| Plage de Tension de Sortie Analogique | 0–1,8 V |
| Taux d'Échantillonnage Entrée Analogique | 100 kS/s / 12 bits |
| Interfaces de Communication | I2C, UART, SPI |
| Sortie d'Alimentation Extension | +3,3 V |
| Système d'Exploitation | Linux embarqué (firmware Red Pitaya) |

## Cas d'Utilisation

- Émission-réception radio amateur HF (ondes courtes) (CW, SSB, AM, FM)
- Surveillance multi-bandes WSPR à signaux faibles (jusqu'à 8 bandes simultanément)
- Déploiement de station de réception SDR distante (accès réseau distant complet)
- Analyse de spectre HF et recherche sur les signaux
- Développement d'applications compatibles HPSDR
- Expérimentation radio amateur (concours, observation astronomique)

---

{{< alert >}}
Besoin d'un devis pour le produit ? Veuillez [nous contacter](/fr/contact/).
{{< /alert >}}
