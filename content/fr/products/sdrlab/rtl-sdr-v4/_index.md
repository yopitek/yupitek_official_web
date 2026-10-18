---
title: "OpenSourceSDRLab RTL-SDR Blog V4 — Récepteur SDR d'Entrée de Gamme"
description: "RTL-SDR Blog RTL SDR V4, récepteur SDR large bande 500kHz–1,7GHz, TCXO 1PPM, upconverter HF intégré, USB 2.0 — le choix incontournable pour débuter en recherche RF."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "RTL-SDR", "Radio Reception", "USB", "GNU Radio"]
faq:
  - question: "Ai-je besoin du mode d'échantillonnage direct pour recevoir les HF sur le RTL-SDR Blog V4 ?"
    answer: "Non. Le V4 possède un convertisseur ascendant intégré au lieu d'un circuit d'échantillonnage direct, de sorte que les signaux HF sont convertis vers le haut de 28.8 MHz et le pilote gère le décalage de fréquence. L'activation de l'échantillonnage direct sur un V4 ne donne aucun résultat."
  - question: "Le RTL-SDR Blog V4 a-t-il besoin de pilotes spéciaux ?"
    answer: "Oui. Le V4 nécessite les pilotes RTL-SDR Blog, qui sont rétrocompatibles avec les unités V3 et plus anciennes. La branche Osmocom par défaut prend désormais également en charge le V4."
  - question: "Comment fonctionne le bias tee sur le RTL-SDR Blog V4 ?"
    answer: "Le bias tee est contrôlé par logiciel et est classé à 4.5 V, fournissant jusqu'à 180 mA en continu. Sous Linux, il est activé avec rtl_biast. Ne l'activez pas avec une antenne court-circuitée en DC sauf si un LNA ou un appareil alimenté est dans la chaîne."
---

## Caractéristiques

![RTL-SDR Blog RTL SDR V4](/images/products/sdrlab/rtl-sdr-v4.png)

- Tuner R828D amélioré offrant un bruit plus faible et une meilleure sensibilité par rapport au R820T/R860 précédent
- Upconverter intégré permettant la réception HF jusqu'à 500 kHz (les dongles RTL-SDR standard descendent à 24 MHz minimum)
- Oscillateur à cristal compensé en température (TCXO) 1 PPM pour une stabilité de fréquence considérablement améliorée
- Bias-Tee commandé par logiciel pour alimenter les LNA externes ou les antennes actives
- Filtre frontend triple-notch supprimant efficacement les interférences FM/AM/DAB
- PCB faible bruit repensé avec protection ESD améliorée et boîtier en aluminium à refroidissement passif
- Kit d'antenne dipôle multiusage inclus — prêt à l'emploi dès la sortie de la boîte

## Spécifications Techniques

| Spécification | Valeur / Description |
|---------------|---------------------|
| Puce Tuner | Rafael Micro R828D |
| Puce ADC | RTL2832U |
| Plage de Fréquences | 500 kHz – 1,7 GHz (mode HF inclus) |
| Bande Passante Maximale | 3,2 MHz (stable à 2,4 MHz) |
| Résolution ADC | 8-bit |
| Précision de Fréquence | TCXO 1 PPM |
| Connecteur RF | SMA Female (F) |
| Bias-Tee | Activé par logiciel, max. 4,5 V |
| Réception HF | Upconverter intégré avec filtre passe-bas 28,8 MHz |
| Boîtier | Alliage d'aluminium, refroidissement passif |
| Interface | USB 2.0 (pilote RTL-SDR Blog requis) |
| Support OS | Windows, Linux, macOS, Android |
| Accessoires | Kit antenne dipôle (2× antennes télescopiques, câble d'extension 3 m, trépied, ventouse) |

## Cas d'Utilisation

- Suivi d'aéronefs ADS-B
- Surveillance maritime AIS
- Réception d'images satellites météo NOAA / Meteor M2
- Radio amateur (réception HF/VHF/UHF)
- Radioastronomie (observation de la raie hydrogène)
- Décodage voix numérique P25 et MotoTRBO
- Suivi de paquets APRS et ACARS
- Réception radio numérique DAB
- Surveillance du spectre RF et recherche en sécurité

---

{{< alert >}}
Besoin d'un devis pour le produit ? Veuillez [nous contacter](/fr/contact/).
{{< /alert >}}

{{< faq >}}

[Guides d'installation et détails techniques — doc.yupitek.com](https://doc.yupitek.com/sdrlab/hardware/rtl-sdr-v4/)
