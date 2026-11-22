---
title: "Comparatif des adaptateurs WiFi USB ALFA Network"
description: "Comparatif complet des spécifications de 9 adaptateurs WiFi USB ALFA Network : chipset, pilote Linux, capacités monitor / injection / AP, avec résultats mesurés sur ASUS GX10 (Ubuntu 24.04 ARM64, noyau 6.17)."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
---

Le tableau ci-dessous compare les 9 adaptateurs WiFi USB ALFA Network. Les colonnes Monitor, Injection, AP et handshake de bout en bout sont des résultats mesurés lors des tests Yopitek sur un ASUS GX10 (Ubuntu 24.04 LTS / ARM64 / noyau 6.17), avec notre propre matériel et le WiFi de nos propres bureaux — et non des valeurs recopiées des fiches techniques.

## Comparatif complet des spécifications

Sur mobile, faites défiler le tableau horizontalement ; touchez le nom d'un modèle pour accéder à sa page produit.

| Modèle | Génération WiFi | Chipset | Bandes | Débit max. | USB | Antennes | MIMO | Monitor Mode | Packet Injection | Handshake (test GX10) | Pilote Linux | Type de pilote | Mode AP | Puissance max. | Bluetooth | Idéal pour |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [AWUS036AXML](/fr/products/alfa/awus036axml/) | WiFi 6E | MT7921AUN | 2.4 + 5 + 6 GHz | 3000 Mbps | USB-C 3.2 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Oui | ❌ Échec sur le noyau 6.17 standard | ❌ Non (l'injection échoue) | Dans le noyau ≥5.18 | Dans le noyau (Plug & Play) | ✅ Natif | 3.6W | BT 5.2 | WiFi 6E + Linux + USB-C |
| [AWUS036AXM](/fr/products/alfa/awus036axm/) | WiFi 6E | MT7921AUN | 2,4 + 5 + 6 GHz (6 GHz non testé) | 3000 Mbps | USB-A 3.2 L | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Oui | ❌ Échec sur le noyau 6.17 standard | ❌ Non (l'injection échoue) | Dans le noyau ≥5.18 | Dans le noyau (Plug & Play) | ✅ Natif | 3.6W | BT 5.2 | WiFi 6E + double antenne |
| [AWUS036AX](/fr/products/alfa/awus036ax/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1200 Mbps | USB-A 3.2 Gen 1 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Oui | ✅ Oui | ✅ De bout en bout (.22000) | Dans le noyau ≥6.17 | Dans le noyau (Plug & Play) | ✅ Natif | 3.6W | — | WiFi 6 + hotspot AP |
| [AWUS036AXER](/fr/products/alfa/awus036axer/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1800 Mbps | USB-A 3.2 | Intégrée (nano) | 2×2 MIMO | ✅ Oui | ✅ Oui | ✅ De bout en bout (.22000) | Dans le noyau ≥6.17 | Dans le noyau (Plug & Play) | ✅ Natif | 3.0W | — | Adaptateur de voyage compact |
| [AWUS036ACH](/fr/products/alfa/awus036ach/) | WiFi 5 | RTL8812AU | 2.4 + 5 GHz | 867 Mbps | USB-C 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅✅ Le meilleur | ✅✅ Le meilleur | ✅ De bout en bout (.22000) | Dans le noyau ≥6.13 | Dans le noyau (Plug & Play) | ✅ Natif | 3.6W | — | Référence sous Kali Linux |
| [AWUS036ACM](/fr/products/alfa/awus036acm/) | WiFi 5 | MT7612U | 2.4 + 5 GHz | 867 Mbps | USB-A 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Oui | ✅ Oui | ✅ De bout en bout (.22000) | Dans le noyau ≥4.19 | Dans le noyau (Plug & Play) | ✅ Natif | 3.0W | — | Linux plug & play |
| [AWUS036ACHM](/fr/products/alfa/awus036achm/) | WiFi 5 | MT7610U | 2.4 + 5 GHz | 433 Mbps | USB 2.0 | 1× RP-SMA 5dBi | 1×1 SISO | ✅ Oui | ✅ 2,4 GHz / ⚠️ 5 GHz diffusion uniquement | ✅ De bout en bout (.22000) | Dans le noyau ≥4.19 | Dans le noyau (Plug & Play) | ✅ Natif | — | — | AC600 compact, Linux plug & play |
| [AWUS036ACS](/fr/products/alfa/awus036acs/) | WiFi 5 | RTL8811AU | 2.4 + 5 GHz | 433 Mbps | USB-A 2.0 | 1× RP-SMA 2dBi | 1×1 SISO | ✅ Oui | ✅ Oui | ✅ De bout en bout (.22000) | Dans le noyau ≥6.13 | Dans le noyau (Plug & Play) | ✅ Natif (5 GHz testé en 802.11a 20 MHz ; VHT80 non testé) | 2.5W | — | Tests de sécurité à petit budget |
| [AWUS036EACS](/fr/products/alfa/awus036eacs/) | WiFi 5 | RTL8821CU | 2.4 + 5 GHz | 433 Mbps | USB 2.0 nano | Intégrée 2 dBi | 1×1 SISO | ✅ Oui | ✅✅ Le meilleur | ✅ De bout en bout (.22000) | Dans le noyau ≥6.2 | Dans le noyau (Plug & Play) | ✅ Natif (5 GHz testé en 802.11a 20 MHz ; VHT80 non testé) | 2.5W | BT 4.2 | WiFi domestique Windows + BT |

## Guide d'achat rapide — par cas d'usage

**🔴 Kali Linux / Pentest** — Le meilleur: AWUS036ACH

RTL8812AU — le monitor mode et la packet injection les plus aboutis sous Kali ; 100 % d'injection sur les deux bandes sur le GX10 (noyau 6.17). Pilote rtw88_8812au dans le noyau depuis la 6.13. Astuce : sur les noyaux plus anciens, utilisez le pilote DKMS d'aircrack-ng figé sur le commit stable 63cf0b4.

**🔵 WiFi 6E (Tri-Band) pour utilisateurs avancés** — Le meilleur: AWUS036AXML or AWUS036AXM

MT7921AUN — pilote Linux dans le noyau depuis la 5.18, bande 6 GHz (vérifiée sur l'AXML ; AXM non testé), Bluetooth 5.2. Remarque : la packet injection échoue sur le noyau standard 6.17 (régression mac80211 depuis la 6.16), il ne convient donc pas au pentest. Formats : l'AXML dispose d'un connecteur USB-C amovible et d'un boîtier à une seule antenne avec deux sorties ; l'AXM présente un format USB-A en L intégré.

**🌐 Émulation Soft-AP / Hotspot** — Le meilleur: AWUS036ACM

MT7612U — prise en charge du mode AP en plug-and-play via le hostapd natif du noyau Linux. Contrairement aux adaptateurs Realtek qui nécessitent des builds hostapd personnalisés problématiques, MediaTek fonctionne de façon fluide et stable pour la simulation de Rogue AP / Evil Twin.

**🟢 Linux au quotidien (Plug & Play)** — Le meilleur: AWUS036ACM

MT7612U — dans le noyau depuis la version 4.19, aucune installation de pilote sous Ubuntu / Debian / Fedora. L'expérience Linux la plus simple.

**🟣 Raspberry Pi / Embarqué** — Le meilleur: AWUS036ACM

Faible consommation + pilote dans le noyau : idéal pour le Raspberry Pi. Remarque : les modèles à forte puissance (ACH, AXML) consomment jusqu'à 3.6W et nécessitent un hub USB alimenté pour éviter les chutes de tension et les coupures de connexion sur le Pi.

**🟡 Sécurité à petit budget / Débutant** — Le meilleur: AWUS036ACS

RTL8811AU — entrée de gamme abordable avec prise en charge du monitor mode et de la packet injection. Antenne unique, conception compacte.

**⚡ Adaptateur de voyage compact** — Le meilleur: AWUS036AXER

Boîtier nano ultra-fin de seulement 10.5g. WiFi 6 (1800 Mbps), USB-A. Idéal pour les déplacements professionnels, orienté Windows.

**🏠 Utilisateur Windows à domicile + Bluetooth** — Le meilleur: AWUS036EACS

RTL8821CU — combo bi-mode WiFi 5 + Bluetooth 4.2. Format nano. Idéal pour les PC de bureau nécessitant rapidement WiFi + BT sans emplacement PCIe.

**🍎 Compatibilité macOS** — Le meilleur: AWUS036ACH or AWUS036AXML

L'ACH bénéficie d'une bonne prise en charge de macOS via un pilote tiers. Le MT7921AUN de l'AXML bénéficie d'un support communautaire sous macOS. Vérifiez toujours la compatibilité avec votre version de macOS. Les Mac Intel disposent d'un meilleur héritage de pilotes que la série M.

## Guide d'achat rapide — par plateforme / système d'exploitation

| Plateforme / Système d'exploitation | Premier choix | Alternative | Remarques |
|---|---|---|---|
| 🐧 Kali Linux | AWUS036ACH | AWUS036ACM | ACH = meilleur monitor mode ; ACM = prise en charge du noyau la plus simple. Pour les VM : configurez la VM avec un contrôleur USB 3.0 (xHCI) afin d'éviter les déconnexions. |
| 🐧 Ubuntu / Debian | AWUS036ACM | AWUS036AXML | MT7612U dans le noyau depuis la 4.19 ; MT7921AUN depuis la 5.18 |
| 🐧 Raspberry Pi OS | AWUS036ACM | AWUS036ACH | Faible consommation + pilote dans le noyau ; aucune compilation manuelle nécessaire. Un hub USB alimenté est recommandé pour les cartes à forte puissance afin d'éviter les coupures. |
| 🪟 Windows 10 / 11 | AWUS036AX | AWUS036EACS | Performances WiFi 6 ; l'EACS ajoute un combo Bluetooth |
| 🍎 macOS | AWUS036ACH | AWUS036AXML | Pilotes tiers disponibles ; vérifiez la version de macOS. Les Mac Intel disposent de pilotes hérités ; Apple Silicon (M1/M2/M3) ne bénéficie que d'une prise en charge expérimentale restreinte. |
| 📱 Android / NetHunter | AWUS036ACH | AWUS036ACS | Le RTL8812AU et le RTL8811AU sont pris en charge par NetHunter ; adaptateur OTG et compilation d'un noyau personnalisé requis. |

---

Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / noyau 6.17.0-1014-nvidia (novembre 2026). Les rapports par adaptateur sont disponibles sur le [blog](/fr/blog/).
