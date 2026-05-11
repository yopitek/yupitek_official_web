---
title: "SDRLab Flipper Zero 5G Add-On Board — Module de Recherche Wi-Fi Double Bande"
description: "Carte d'extension Flipper Zero 5G, Wi-Fi double bande RTL8720DN (2,4+5GHz), BLE 5.0, firmware Deauth pré-flashé, alimenté par GPIO, compatible Momentum/Unleashed."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero Add-On", "5GHz", "Wi-Fi", "Deauth", "Security Research"]
---

{{< alert "warning" >}}
**Avis d'utilisation légale** : Cette carte d'extension est destinée exclusivement à la recherche en sécurité autorisée et aux tests légaux. Assurez-vous de respecter la réglementation locale sur les fréquences radio avant utilisation.
{{< /alert >}}

## Caractéristiques

![SDRLab Flipper Zero 5G Add-On Board](/images/products/sdrlab/flipper-5g.png)

- **Couverture Double Bande** — 2,4 GHz + 5 GHz (IEEE 802.11 a/b/g/n) ; accès aux réseaux 5 GHz modernes inaccessibles avec les anciens add-ons Flipper
- **Realtek RTL8720DN via AI Thinker BW16** — SoC double bande standard de l'industrie avec module pré-certifié FCC/CE
- **CPU Dual-Core** — ARM Cortex-M4 @ 200 MHz pour les protocoles actifs ; Cortex-M0 @ 20 MHz pour les tâches de fond à faible consommation
- **Firmware Marauder 5G pré-flashé** — inclut les modes scan, deauth, beacon flood, sniff (EAPOL/PMKID) et evil portal ; prêt à l'emploi
- **BLE 5.0** — énumération de périphériques Bluetooth Low Energy et analyse de balises en parallèle des recherches Wi-Fi
- **Alimentation GPIO** — tire 5 V directement du connecteur GPIO du Flipper Zero ; aucune alimentation externe requise
- **Upgrade Antenne** — connecteur IPEX (U.FL) sur les révisions compatibles pour fixer une antenne externe à gain élevé
- **Écosystème Firmware** — compatible avec les frameworks de firmware personnalisé Momentum et Unleashed
- **Développement PlatformIO** — support complet du développement de firmware personnalisé via le framework Ameba D compatible Arduino
- **Plage de Fonctionnement Robuste** — −40°C à 85°C pour une utilisation sur le terrain dans n'importe quel climat

## Spécifications

| Spécification | Valeur / Description |
|---------------|---------------------|
| Puce Principale | Realtek RTL8720DN (module AI Thinker BW16) |
| CPU | ARM Cortex-M4 @ 200 MHz + Cortex-M0 @ 20 MHz |
| Standard Wi-Fi | IEEE 802.11 a/b/g/n (2,4 GHz + 5 GHz double bande) |
| Puissance TX Wi-Fi | ~17 dBm (selon la réglementation régionale) |
| Bluetooth | BLE 5.0 |
| Flash | 4 MB |
| Source d'Alimentation | GPIO Flipper Zero (5 V) |
| Consommation Typique | 150–250 mA (scan actif) |
| Interface de Connexion | Connecteur GPIO standard Flipper Zero (2×8 broches) |
| Firmware Pré-chargé | Marauder 5G (scan, deauth, beacon, sniff, evil portal) |
| Compatibilité Firmware | Momentum, Unleashed |
| Développement Personnalisé | PlatformIO (framework Ameba D / RTL8720DN) |
| Température de Fonctionnement | −40°C à 85°C |
| Interface Antenne | IPEX (U.FL) ou antenne PCB embarquée (selon révision) |
| Facteur de Forme | Carte d'extension GPIO Flipper Zero |

## Cas d'Utilisation

- **Scan Wi-Fi Double Bande** — énumération passive des réseaux 2,4 GHz et 5 GHz ; capture du SSID, BSSID, canal, RSSI, type de chiffrement et clients connectés
- **Recherche de Déauthentification Wi-Fi** — envoi de trames deauth 802.11 pour tester la résilience réseau et évaluer la protection 802.11w/PMF sur les réseaux autorisés
- **Capture de Handshake WPA** — interception des handshakes EAPOL/PMKID pour l'audit de sécurité réseau autorisé
- **Développement Evil Portal** — prototype de scénarios de portail captif AP factice pour les tests de sensibilisation au phishing (environnements autorisés uniquement)
- **Test de Beacon Flood** — diffusion de SSID personnalisés pour étudier l'impact de la congestion RF et le comportement des clients
- **Énumération de Périphériques BLE** — scan et identification des périphériques BLE 5.0 à proximité en parallèle des recherches Wi-Fi
- **Cartographie de Topologie Réseau Mesh** — identification des relations AP mesh, des canaux backhaul et des configurations SSID cachées
- **Recherche de Protocoles sans Fil IoT** — analyse du comportement des appareils IoT sur les deux bandes Wi-Fi dans un environnement de laboratoire contrôlé
- **Formation aux Tests de Pénétration Autorisés** — plateforme d'apprentissage pratique pour les fondamentaux de la sécurité Wi-Fi dans des environnements autorisés

---

{{< alert "warning" >}}
**Nouveau avec cette carte ?** Suivez notre guide de démarrage étape par étape — couvrant les prérequis, la configuration du firmware, le premier scan et toutes les fonctionnalités clés.
[📖 Ouvrir le Manuel Utilisateur en Ligne](/fr/products/sdrlab/flipper-5g/flipper_5G_module.html)
{{< /alert >}}

{{< alert >}}
Besoin d'un devis ? [Contactez-nous](/fr/contact/)
{{< /alert >}}
