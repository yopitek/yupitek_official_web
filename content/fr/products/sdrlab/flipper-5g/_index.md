---
title: "SDRLab Flipper Zero 5G Add-On Board — Module de Recherche Wi-Fi Double Bande"
description: "Carte d'extension Flipper Zero 5G, Wi-Fi double bande ESP32-C5 (2,4+5GHz), firmware Deauth pré-flashé, alimenté par GPIO, compatible Momentum/Unleashed."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero Add-On", "5GHz", "Wi-Fi", "Deauth", "Security Research"]
---

# SDRLab Flipper Zero 5G Expansion Board — Module de recherche de sécurité Wi-Fi double bande

> **Déclaration d'utilisation légale** : Cette carte d'extension est destinée exclusivement à la recherche en cybersécurité autorisée et à des fins de recherche légales. Tester des réseaux, des appareils ou des infrastructures dont tu ne possèdes pas la propriété ou pour lesquels tu n'as pas obtenu d'autorisation écrite est illégal dans la plupart des pays. Assure-toi de respecter les réglementations locales sur l'utilisation des fréquences radio et utilise ce produit de manière responsable et éthique.

---

## 1. Qu'est-ce que c'est ?

Une carte d'extension de recherche sans fil qui se branche sur les broches GPIO à l'arrière du Flipper Zero. Elle complète les capacités de ton Flipper (qui ne gère que le 2.4 GHz) en lui ajoutant trois capacités sans fil en une seule fois :

- **Wi-Fi double bande 2.4 GHz + 5 GHz**
- **Radiofréquence Sub-GHz 433 MHz**
- **GPS actif**

Elle est également équipée d'un **écran TFT couleur de 2.8 pouces**, d'une **batterie amovible à chaud de 800 mAh**, de **quatre connecteurs SMA pour antennes avec quatre antennes incluses**, et d'un **firmware ESP32 Marauder 5G préinstallé**.

Pas besoin d'acheter un programmateur, pas besoin de compiler le firmware toi-même. Branche-le, configure trois paramètres, et c'est parti.

---

## 2. Caractéristiques du produit

### Trois capacités sans fil en une seule fois
- **Wi-Fi double bande 2.4 GHz + 5 GHz** — Scanne les réseaux 5 GHz modernes, comblant la limite des anciennes cartes qui ne voyaient que le 2.4 GHz.
- **Sub-GHz 433 MHz (module RF A07, 10 dBm)** — Offre une alternative lorsque la réception intégrée du Flipper est faible.
- **GPS actif** — Les enregistrements de wardrive incluent automatiquement les coordonnées. Alimenté par le Flipper quand il est connecté, bascule automatiquement sur la batterie interne quand il est détaché.

### Écran TFT couleur de 2.8 pouces
Les résultats du scan, l'intensité du signal, et le niveau de batterie sont affichés directement sur la carte. Fini les devinettes devant le terminal de ton ordinateur. L'interface utilisateur Marauder est intégrée.

### Quatre connecteurs SMA, quatre antennes incluses
Le dos du boîtier indique clairement la correspondance des quatre connecteurs :

| Sérigraphie | Position | Usage |
|---|---|---|
| `433M A` | Bord supérieur gauche | RF 433 MHz (module A07, 10 dBm) |
| `GPS` | Bord supérieur droit | Antenne GPS active |
| `2.4G` | Aile gauche | Wi-Fi 2.4 GHz |
| `2.4G/5G` | Aile droite | Wi-Fi double bande 2.4 GHz + 5 GHz |

Les quatre connecteurs sont des prises femelles SMA fixées par vis. **Les quatre antennes sont incluses** : antenne Wi-Fi 3 dBi (11 cm), antenne 433M 3 dBi, antenne GPS 20 dBi.

### Batterie 800 mAh amovible à chaud
Une batterie lithium-polymère de 800 mAh est intégrée. Tu peux l'utiliser seule, détachée du Flipper, pour capturer des paquets, puis la reconnecter à la carte principale après le scan.

### Firmware Marauder 5G préinstallé
Prêt à l'emploi, aucun programmateur supplémentaire n'est nécessaire. Un port de programmation USB-C reste disponible sur la carte pour les utilisateurs avancés souhaitant mettre à jour le firmware.

### Contacts dorés + protection contre les surtensions (TVS)
Toutes les broches de signal sont dorées. Chaque broche intègre une diode de suppression de surtension transitoire (TVS) pour protéger la carte lors de la connexion/déconnexion du Flipper.

### Compatibilité de l'écosystème firmware
Compatible avec les firmwares personnalisés incluant WiFi Marauder et GPS, tels que Momentum, Unleashed et Xtreme.

---

## 3. Spécifications techniques

| Spécification | Valeur / Description |
|---|---|
| **Puce principale** | **Espressif ESP32-C5** (5G/2.4G) |
| **Wi-Fi** | Double bande 2.4 GHz + 5 GHz |
| **Connecteur antenne Wi-Fi** | **4 prises SMA femelles** : 433M A / GPS / 2.4G / 2.4G+5G, **4 antennes incluses** : Wi-Fi 3 dBi (11 cm), 433M 3 dBi, GPS 20 dBi |
| **Sub-GHz** | Module RF 433 MHz A07, sortie de **10 dBm** |
| **GNSS** | Module GPS actif, **commutation d'alimentation automatique** (alimenté par le Flipper quand connecté, batterie interne quand détaché) |
| **Écran** | **TFT couleur 2.8 pouces**, interface Marauder intégrée |
| **Batterie** | **800 mAh Lithium-polymère**, amovible à chaud |
| **Interface de connexion** | Broches GPIO standard Flipper Zero (**2x8 broches**), contacts dorés + protection TVS par broche |
| **Firmware préchargé** | **ESP32 Marauder 5G** (open source, préinstallé) |
| **Compatibilité firmware** | Momentum, Unleashed, Xtreme |

### Accessoires inclus
- Carte principale ×1 (assemblée, avec écran 2.8 pouces)
- Antennes ×4 — 1x `2.4G`, 1x `2.4G+5G`, 1x `433M A`, 1x `GPS`
- Connecteur GPIO Flipper

### À acheter séparément
- **Flipper Zero** (cette carte est une extension, la console n'est pas incluse)

---

## 4. Prise en main : trois paramètres à configurer

La carte est livrée avec le firmware préinstallé, aucune programmation n'est nécessaire. Après l'avoir branchée sur le Flipper, tu dois configurer trois jeux de broches :

| Fonction | Chemin de configuration | Valeur |
|---|---|---|
| **GPS** | Momentum → Paramètres du protocole → Paramètres GPIO → **GPS Pin** | **13 ou 14** |
| **ESP32 (WiFi / Marauder)** | Idem → **ESP32 Pin** | **15, 16** |
| **Sub-GHz 433 MHz** | Flipper → Sub-GHz → Paramètres avancés → **Module** | **External** |

> ⚠️ **Le GPS et l'ESP32 utilisent des broches UART différentes. Ne les configure pas sur le même jeu, sinon le GPS et le Wi-Fi ne fonctionneront pas.**

Redémarre le Flipper après la configuration. Tu devrais voir les applications WiFi Marauder et GPS apparaître dans `Apps → GPIO`.

---

## 5. Cas d'utilisation

- **Scan Wi-Fi double bande** — Énumération passive des réseaux 2.4 GHz et 5 GHz ; capture du SSID, BSSID, canal, RSSI, type de chiffrement et clients connectés.
- **Capture de poignées de main WPA** — Sniffing des paquets de poignée de main EAPOL/PMKID, utilisé pour les audits de sécurité sur des réseaux autorisés.
- **Test Deauth** — Envoi de paquets Deauth pour tester la résilience du réseau, réservé aux réseaux dont tu es propriétaire ou autorisé.
- **Cartographie de topologie réseau Wardrive** — Enregistrements Wi-Fi et appareils marqués par GPS, exportés en CSV pour analyse ultérieure.
- **Recherche RF 433 MHz** — Opération via le menu Sub-GHz du Flipper, utile pour évaluer les environnements où la réception intégrée du Flipper est faible.
- **Simulation Evil Portal** — Prototypage et test de pages d'entrée dans un environnement autorisé.
- **Recherche sur les protocoles sans fil IoT** — Analyse du comportement des appareils IoT sur double bande dans un environnement de laboratoire contrôlé.

---

## 6. Limitations connues (à lire attentivement)

- **La stabilité du Deauth 5 GHz dépend de la version du firmware**. Le firmware Marauder open source continue d'améliorer le support du deauth 5 GHz sur l'ESP32-C5. Il est recommandé d'utiliser principalement le **2.4 GHz** pour les tests de deauth. Pour le 5 GHz, privilégie le scan, la surveillance du signal et les enregistrements de wardrive. Les performances réelles dépendent de la version du firmware utilisée.
- **L'antenne GPS est directionnelle**, bien que le produit soit souvent décrit comme omnidirectionnel. Oriente l'antenne vers le ciel dégagé pour obtenir un positionnement. Le premier démarrage à froid peut prendre plusieurs minutes pour télécharger les données éphémérides. Les performances sont médiocres à l'intérieur ; utilise-le de préférence en extérieur ou près d'une fenêtre.
- **L'heure renvoyée par le GPS est en UTC+0**. Il n'y a pas d'option de réglage du fuseau horaire dans le firmware. Pour l'heure de Taïwan (UTC+8), ajoute 8 heures manuellement.
- **Le GPS et l'ESP32 utilisent des broches UART différentes** (GPS : 13 ou 14 ; ESP32 : 15, 16). Ne les configure pas sur le même jeu, sinon le GPS et le Wi-Fi ne répondront pas.
- **Port USB-C de programmation** — Le port Type-C situé à l'avant, côté gauche, sert à la programmation du firmware.
- **Commutation automatique d'alimentation du GPS** — Alimenté par le Flipper quand connecté, bascule sur la batterie interne quand détaché. Un redémarrage bref lors de la commutation est normal.

---

**Lien vers la page produit** : https://yupitek.com/zh-tw/products/sdrlab/flipper-5g/
**Manuel d'utilisation complet** : https://doczhtw.yupitek.com/sdrlab/expansion/5g-board/
**Page boutique du fabricant (OpenSourceSDRLab)** : https://opensourcesdrlab.com/products/opensourcesdrlab-new-5g-multi-in-one-module-flipperzero-module-with-screen-flipperzero5g-expansion-board?VariantsId=10754
