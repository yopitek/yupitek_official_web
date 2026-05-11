---
title: "ALFA AWUS036ACH — Adaptateur USB-C Double Bande AC1200 Haute Puissance"
description: "ALFA AWUS036ACH, Realtek RTL8812AU, AC1200 double bande, USB-C, deux antennes détachables 5 dBi. La référence pour les tests d'intrusion sur Kali Linux avec Mode Moniteur et Injection de Paquets."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB-C", "Dual Antenna", "Monitor Mode", "Kali Linux", "Security Research"]
---

{{< alert "warning" >}}
**Avertissement Légal :** Les fonctionnalités Mode Moniteur et Injection de Paquets sont destinées uniquement aux tests de sécurité autorisés, à la recherche éducative et aux tests d'intrusion légaux. Assurez-vous d'avoir une autorisation explicite pour le réseau cible.
{{< /alert >}}

## Présentation du Produit

L'AWUS036ACH est l'adaptateur de recherche en sécurité le plus emblématique d'Alfa Network — la référence absolue pour les tests d'intrusion sur Kali Linux depuis 2017. Propulsé par le chipset Realtek RTL8812AU éprouvé, il offre un mode moniteur et une injection de paquets irréprochables, un amplificateur de puissance intégré pour une réception longue portée, et deux antennes détachables 5 dBi. Il fut le premier adaptateur WiFi 5 au monde avec un connecteur USB Type-C.

> **Avis macOS :** Tous les adaptateurs ALFA ont un support macOS limité ou inexistant. macOS 11 Big Sur et versions ultérieures, ainsi qu'Apple Silicon (M1/M2/M3), ne sont **PAS** pris en charge. Le support macOS maximum est 10.15 Catalina sur Mac Intel.

## Caractéristiques Principales

- Realtek RTL8812AU — chipset le plus testé pour la recherche en sécurité WiFi
- WiFi 5 AC1200 double bande : 5 GHz 867 Mbps + 2,4 GHz 300 Mbps
- Amplificateur de puissance intégré — jusqu'à 3× la portée des cartes laptop classiques
- 2× RP-SMA femelle avec 2× antennes double bande détachables 5 dBi (améliorables)
- Premier adaptateur WiFi 5 USB-C au monde
- Support pince-écran inclus
- Support Kali Linux depuis 2017.1

## Spécifications Techniques

| Paramètre | Valeur |
|------|------|
| Chipset | Realtek RTL8812AU |
| Standards WiFi | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bandes de Fréquence | Double Bande 2,4 GHz / 5 GHz |
| Débit Maximum | 802.11n : 300 Mbps · 802.11ac : 867 Mbps |
| Vitesse Combinée Max | AC1200 (867 + 300 Mbps) |
| Connecteurs d'Antenne | 2× RP-SMA femelle |
| Antennes Incluses | 2× dipôle omni double bande, 5 dBi |
| Interface USB | Type-C SuperSpeed (5 Gbps) ; rétrocompatible USB 2.0 |
| Amplificateur de Puissance | Oui — portée étendue |
| Sécurité Sans Fil | WPA3 / WPA2 / WPA / WEP / WPS / 802.1X |
| Pays d'Origine | Taïwan |

## Compatibilité Système d'Exploitation

| Système d'Exploitation | Statut | Notes |
|------|---------|------|
| Windows 10/11 | ✅ Pris en charge | Télécharger le pilote depuis le site Alfa ; WPA3 pris en charge |
| macOS 10.15 Catalina | ⚠️ Limité | Installation manuelle ; macOS 11+ et Apple Silicon NON pris en charge |
| Ubuntu | ✅ Pris en charge | Installation manuelle RTL8812AU DKMS ; intégré au noyau ≥ 6.14 |
| Kali Linux | ✅ Excellent | Depuis Kali 2017.1 ; mode moniteur complet + injection de paquets ; utiliser le pilote aircrack-ng |
| NetHunter (Android) | ✅ Pris en charge | USB OTG ; fonctionnement largement confirmé |

## Compatibilité Matérielle

| Matériel | Statut | Notes |
|------|---------|------|
| Raspberry Pi 3B+/4/5 | ✅ Pris en charge | Pilote manuel via script morrownr DKMS |
| PC Bureau/Laptop | ✅ Pris en charge | USB-C ou USB-A via câble inclus |
| Mac (Intel) | ⚠️ Limité | macOS 10.15 Catalina maximum |

## Fonctionnalités Avancées

| Fonctionnalité | Statut |
|------|------|
| Mode Moniteur | ✅ Excellent (référence absolue — éprouvé par la communauté depuis 2017) |
| Injection de Paquets | ✅ Excellent |
| Mode AP Logiciel | ✅ Oui |
| Bluetooth | ❌ Non |
| VIF | ⚠️ Limité |

## Contenu de la Boîte

- 1× Adaptateur AWUS036ACH
- 2× Antennes dipôle double bande détachables 5 dBi
- 1× Câble USB-C vers USB-A
- 1× Support pince-écran

## Ressources & Liens

| Ressource | Lien |
|------|------|
| Page Produit Officielle | https://www.alfa.com.tw/products/awus036ach_1 |
| Documentation Officielle | https://docs.alfa.com.tw/Product/AWUS036ACH/ |
| Pilote (aircrack-ng, recommandé pour Kali) | https://github.com/aircrack-ng/rtl8812au |
| Pilote (morrownr, Linux général) | https://github.com/morrownr/8812au-20210708 |

## Fiche Technique du Produit

| Document | Téléchargement |
|------|------|
| Fiche Technique Officielle (PDF) | [📄 Télécharger la Fiche AWUS036ACH](/docs/alfa/AWUS036ACH_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ach_image_1.png" alt="ALFA AWUS036ACH" />
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
Besoin d'un devis ou de plus d'informations ? [Contactez-nous](/fr/contact/)
{{< /alert >}}
