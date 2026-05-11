---
title: "ALFA AWUS036ACM — Adaptateur USB 3.0 Double Bande AC1200 (Meilleur Plug & Play Linux)"
description: "ALFA AWUS036ACM, MediaTek MT7612U, AC1200 double bande USB 3.0, pilote intégré au noyau Linux depuis le noyau 4.19 (plug & play, zéro compilation). Mode Moniteur, Injection de Paquets et VIF complets. Meilleur adaptateur Alfa pour Raspberry Pi."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB 3.0", "Dual-Band", "Monitor Mode", "Kali Linux", "Raspberry Pi"]
---

{{< alert "warning" >}}
**Avertissement Légal :** Les fonctionnalités Mode Moniteur et Injection de Paquets sont destinées uniquement aux tests de sécurité autorisés, à la recherche éducative et aux tests d'intrusion légaux. Assurez-vous d'avoir l'autorisation explicite du propriétaire du réseau cible avant toute utilisation.
{{< /alert >}}

## Présentation du Produit

L'AWUS036ACM est le premier choix pour les utilisateurs Linux souhaitant une configuration sans effort. Son chipset MediaTek MT7612U est intégré au noyau Linux depuis la version 4.19 — ce qui signifie qu'il fonctionne immédiatement sur Ubuntu, Kali Linux, Raspberry Pi OS, Arch Linux et pratiquement toute distribution moderne sans compiler une seule ligne de code. Il correspond à l'AWUS036ACH en termes de dimensions et de configuration d'antennes, mais utilise le pilote intégré au noyau de MediaTek. Le mode moniteur, l'injection de paquets et le VIF (Interface Virtuelle) sont tous entièrement pris en charge.

> **Avis macOS :** Tous les adaptateurs ALFA ont un support macOS limité ou inexistant. macOS 11+ et Apple Silicon (M1/M2/M3) ne sont **PAS pris en charge**. L'AWUS036ACM prend en charge macOS jusqu'à la version 10.12 Sierra au maximum — plus restrictif que la plupart des autres modèles.

## Caractéristiques Principales

- Chipset MediaTek MT7612U — pilote intégré au noyau Linux depuis le noyau 4.19 (plug & play, aucune compilation requise)
- WiFi 5 (802.11ac) double bande AC1200 — jusqu'à 867 Mbps sur 5 GHz, 300 Mbps sur 2,4 GHz
- 2× connecteurs RP-SMA femelle avec 2× antennes double bande détachables 5 dBi — format physique identique à l'AWUS036ACH
- Interface USB 3.0 (USB-A)
- Mode moniteur, injection de paquets et mode AP complets
- Support VIF (Interface Virtuelle) dans Kali Linux
- Câble d'extension USB 3.0 inclus
- Conforme TAA — adapté aux achats gouvernementaux américains (compatible GSA)
- Fonctionne immédiatement sur Raspberry Pi OS — aucune installation de pilote

## Spécifications Techniques

| Paramètre | Valeur |
|-----------|-------|
| Chipset | MediaTek MT7612U |
| Standards WiFi | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bandes de Fréquence | 2,4 GHz (2,412–2,472 GHz) · 5 GHz (5,15–5,825 GHz) |
| Largeurs de Canal | 20 / 40 / 80 MHz |
| Débit Maximum | 5 GHz : jusqu'à 867 Mbps · 2,4 GHz : jusqu'à 300 Mbps |
| Vitesse Combinée Max | AC1200 (867 + 300 Mbps) |
| Connecteurs d'Antenne | 2× RP-SMA femelle |
| Antennes Incluses | 2× dipôle double bande, 5 dBi |
| Interface USB | USB 3.0 Type-A (rétrocompatible USB 2.0) |
| Puissance d'Émission | 802.11a : 20 dBm · 802.11b : 23 dBm · 802.11g : 23 dBm · 802.11n : 21 dBm · 802.11ac : 20 dBm |
| Sensibilité de Réception | 802.11a : −92 dBm · 802.11b : −97 dBm · 802.11g : −90 dBm · 802.11n : −90 dBm |
| Sécurité Sans Fil | WPA2 / WPA / WEP / WPA-PSK / 802.1X |
| LED | Oui (alimentation + activité WLAN) |
| Accessoires | Câble d'extension USB 3.0 |
| Pays d'Origine | Taïwan |

## Compatibilité Système d'Exploitation

| Système d'Exploitation | Statut | Notes |
|----|--------|-------|
| Windows XP–11 | ✅ Pris en charge | Pilote disponible sur le site Alfa. Windows 10/11 recommandé. |
| macOS 10.7–10.12 | ⚠️ Limité | Le support officiel s'arrête à macOS 10.12 Sierra. macOS 11+ et Apple Silicon NON pris en charge. |
| Ubuntu 19.04+ | ✅ Plug & Play | Pilote mt76 intégré au noyau (noyau ≥ 4.19). Zéro installation sur Ubuntu 20.04 LTS et versions ultérieures. |
| Kali Linux 2019.3+ | ✅ Plug & Play | Pilote intégré au noyau. Mode moniteur confirmé. VIF (Interface Virtuelle) pris en charge. Le mode AP sur 5 GHz peut nécessiter le paramètre de module `disable_usb_sg`. |
| NetHunter (Android) | ✅ Pris en charge | USB OTG ; le pilote intégré au noyau offre une compatibilité Android plus large que les adaptateurs RTL. |

## Compatibilité Matérielle

| Matériel | Statut | Notes |
|----------|--------|-------|
| Raspberry Pi 3B+/4/5 | ✅ Excellent | Fonctionne immédiatement sur Raspberry Pi OS — aucune installation de pilote requise. Meilleur adaptateur Alfa pour Pi. |
| PC Bureau/Laptop | ✅ Pris en charge | USB-A standard, avec câble d'extension inclus. |
| Mac (Intel) | ⚠️ Limité | macOS 10.7–10.12 uniquement. |

## Fonctionnalités Avancées

| Fonctionnalité | Statut |
|---------|--------|
| Mode Moniteur | ✅ Oui (intégré au noyau, aucune étape supplémentaire sur les distributions modernes) |
| Injection de Paquets | ✅ Oui |
| Mode AP Logiciel | ✅ Oui (AP 5 GHz : ajouter le paramètre de module `disable_usb_sg` pour de meilleures performances) |
| Bluetooth | ❌ Non |
| VIF (Interface Virtuelle) | ✅ Oui (support VIF complet dans Kali) |

## Contenu de la Boîte

- 1× Adaptateur AWUS036ACM
- 2× Antennes dipôle double bande détachables 5 dBi
- 1× Câble d'extension USB 3.0
- 1× CD de pilotes (Windows)

## Ressources & Liens

| Ressource | Lien |
|----------|------|
| Page Produit Officielle | https://www.alfa.com.tw/products/awus036acm_1 |
| Documentation Officielle | https://docs.alfa.com.tw/Product/AWUS036ACM/ |
| Info Pilote Linux (intégré au noyau) | Pilote mt76 — inclus dans le noyau Linux ≥ 4.19, aucune installation nécessaire |

## Téléchargement Fiche Technique

| Document | Téléchargement |
|----------|----------|
| Fiche Technique Officielle (PDF) | [📄 Télécharger la Fiche AWUS036ACM](/docs/alfa/AWUS036ACM_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036acm_image_1.png" alt="ALFA AWUS036ACM" />
{{< /gallery >}}

---

## Améliorations d'Antennes Compatibles

Tous les adaptateurs ALFA disposent d'un connecteur RP-SMA standard. Améliorez les performances avec une antenne externe optionnelle pour une portée et un gain accrus :

| Antenne | Fréquence | Gain | Type |
|---------|-----------|------|------|
| [ALFA APA-M04](/fr/products/alfa/apa-m04/) | 2,4 GHz | 7 dBi | Panneau Intérieur |
| [ALFA APA-M25](/fr/products/alfa/apa-m25/) | 2,4 / 5 GHz | 7 dBi | Panneau Intérieur Double Bande |
| [ALFA APA-M25-6E](/fr/products/alfa/apa-m25-6e/) | 2,4 / 5 / 6 GHz | 7 dBi | Panneau Intérieur Tri-Bande |
| [ARS 25-57A](/fr/products/alfa/ars-25-57a/) | 2,4 / 5 GHz | 2,5 / 7 dBi | Omni Extérieur |
| [ARS NT5B7](/fr/products/alfa/ars-nt5b7/) | 2,4 / 5 GHz | 5 / 7 dBi | Omni |

{{< alert >}}
Besoin d'un devis ou de conseils d'achat ? [Contactez-nous](/fr/contact/).
{{< /alert >}}
