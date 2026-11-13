---
title: "OpenSourceSDRLab RTL-SDR Blog V4 — Récepteur SDR d'Entrée de Gamme"
description: "RTL-SDR Blog RTL SDR V4, récepteur SDR large bande 500kHz–1,766GHz, TCXO 1PPM, upconverter HF intégré — le choix incontournable pour débuter en recherche RF."
date: 2026-03-12
draft: false
featureimage: "/images/products/sdrlab/rtl-sdr-v4.png"
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "RTL-SDR", "Radio Reception", "USB", "GNU Radio"]
faq:
  - question: "Ai-je besoin du mode d'échantillonnage direct pour recevoir les HF sur le RTL-SDR Blog V4 ?"
    answer: "Non. Le V4 possède un convertisseur ascendant intégré au lieu d'un circuit d'échantillonnage direct, de sorte que les signaux HF sont convertis vers le haut de 28.8 MHz et le pilote gère le décalage de fréquence. L'activation de l'échantillonnage direct sur un V4 ne donne aucun résultat."
  - question: "Le RTL-SDR Blog V4 a-t-il besoin de pilotes spéciaux ?"
    answer: "Oui. Le V4 nécessite les pilotes RTL-SDR Blog, qui sont rétrocompatibles avec les unités V3 et plus anciennes."
  - question: "Comment fonctionne le bias tee sur le RTL-SDR Blog V4 ?"
    answer: "Le bias tee est contrôlé par logiciel et est classé à 4.5 V, fournissant jusqu'à 180 mA en continu. Sous Linux, il est activé avec rtl_biast."
---

## Caractéristiques

![RTL-SDR Blog RTL SDR V4](/images/products/sdrlab/rtl-sdr-v4.png)

- Tuner R828D à trois entrées ; un triplexeur répartit l'entrée SMA en bandes HF, VHF et UHF pour une meilleure isolation hors bande
- Upconverter HF intégré : le HF est translaté de 28,8 MHz vers le haut, sans mode d'échantillonnage direct (limite basse d'accord 500 kHz)
- Oscillateur à cristal compensé en température (TCXO) 1 PPM pour une stabilité de fréquence considérablement améliorée
- Bias-Tee commandé par logiciel pour alimenter les LNA externes ou les antennes actives
- Filtre notch commutable pour les bandes de radiodiffusion AM, FM et DAB, réduisant les interférences des émetteurs puissants
- Boîtier métallique noir conducteur faisant office de blindage et de dissipateur, avec suppression du bruit USB et protection ESD renforcée
- Kit d'antenne dipôle multiusage inclus — prêt à l'emploi dès la sortie de la boîte

## Spécifications Techniques

| Spécification | Valeur / Description |
|---------------|---------------------|
| Puce Tuner | Rafael Micro R828D |
| Puce ADC | RTL2832U |
| Plage de Fréquences | 500 kHz – 1,766 GHz (mode HF inclus) |
| Précision de Fréquence | TCXO 1 PPM |
| Connecteur RF | SMA |
| Bias-Tee | Activé par logiciel, max. 4,5 V |
| Réception HF | Upconverter intégré (HF translaté de 28,8 MHz ; échantillonnage direct inutile) |
| Boîtier | Boîtier métallique noir conducteur (blindage et dissipateur) |
| Interface | USB (pilote RTL-SDR Blog requis) |
| Support OS | Windows, Linux, macOS, Android |
| Accessoires | Kit antenne dipôle (4× antennes télescopiques (2× 23 cm–1 m, 2× 5–13 cm), câble d'extension 3 m, trépied, ventouse) |

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

[Guide officiel RTL-SDR Blog pour le V4](https://www.rtl-sdr.com/v4/)

**Page boutique du fabricant (OpenSourceSDRLab)** : https://opensourcesdrlab.com/products/rtl-sdr-v4
