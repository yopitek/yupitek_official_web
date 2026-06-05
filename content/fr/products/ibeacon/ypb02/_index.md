---
title: "Balise Détectrice de Mouvement YPB02 BLE"
description: "Balise Détectrice de Mouvement YPB02 BLE. Bluetooth Low Energy BLE 5.0, pour localisation, contrôle de présence et suivi d'actifs."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yupitek", "CR2477", "Waterproof", "Sensor", "Accelerometer"]
---

## Présentation du produit

Le **YPB02** est une balise Bluetooth® (BLE 5.0) équipée d'un **accéléromètre LIS3DH 3 axes**. Elle possède le même boîtier IP67 et la même pile CR2477 que le YPB01, tout en ajoutant des fonctions de télémétrie de mouvement.

La balise peut modifier sa fréquence d'émission ou envoyer des alertes uniquement en cas de mouvement, de vibration ou de chute.

---

## Caractéristiques principales

* **Accéléromètre 3 axes:** Capteur LIS3DH mesurant l'orientation et l'accélération sur les axes X, Y, Z.
* **Diffusion sur déclencheur:** Permet d'émettre en mouvement, d'envoyer une alerte de chute ou de réduire l'intervalle à 100 ms en déplacement.
* **Protection IP67:** Étanche à la poussière et à l'immersion.
* **Pile remplaçable:** Remplacement rapide de la pile bouton CR2477.

---

## Détection de mouvement et télémétrie

Grâce au capteur LIS3DH, le YPB02 permet:
1. **Diffusion selon l'activité:** Émet les trames standards et déclenche les trames de capteurs uniquement en mouvement.
2. **Mode double:** Reste en veille à l'arrêt et passe à un intervalle de 100 ms en mouvement.
3. **Seuils réglables:** Les paramètres de sensibilité sont configurables via l'application.

---

## Guide de configuration

La configuration se fait sans fil via l'application **BeaconSET+**:
1. Téléchargez **BeaconSET+**.
2. Activez le Bluetooth et le service de localisation.
3. Connectez-vous à la balise après détection de son adresse MAC.
4. Saisissez le mot de passe pour modifier les réglages.

## Technical Specifications

| Paramètre | Spécifications | Remarques |
| :--- | :--- | :--- |
| **Chip Model** | nRF52 series | Ultra-low power consumption |
| **Bluetooth Version** | BLE 5.0 | High efficiency and speed |
| **Waterproof Level** | IP67 | Splash and dust resistant (1m immersion) |
| **Sensor** | LIS3DH 3-axis accelerometer | X, Y, Z axes telemetry |
| **Transmission Range** | Up to 100 meters | Open space |
| **Antenna Impedance** | 50 ohm | On-board / PCB Antenna |
| **Power Source** | 1 × CR2477 coin battery | Replaceable (3.0V, 1000mAh) |
| **Operating Voltage** | 1.8V - 3.9V | DC |
| **Peak Current** | 5.3 mA | Tested at 0dBm transmission power |
| **Dimensions** | Φ39 × 15.5 mm | Compact circular shape |
| **Default Settings** | UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms | Configurable via App |

---

## Galerie du produit

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb02.png" alt="Yupitek YPB02" />
{{< /gallery >}}

---

{{< alert >}}
Besoin d'un devis pour le produit ? Veuillez [nous contacter](/fr/contact/).
{{< /alert >}}
