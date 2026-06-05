---
title: "ALFA AWUS036ACS — Adaptateur USB Double Bande AC600 (Recherche Sécurité Entrée de Gamme)"
description: "ALFA AWUS036ACS, Realtek RTL8811AU, AC600 double bande USB 2.0, 1× antenne détachable RP-SMA 2 dBi, supporte Mode Moniteur et Injection de Paquets — adaptateur idéal pour débuter en recherche sécurité."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "RP-SMA", "Monitor Mode", "Kali Linux", "Budget"]
---

{{< alert "warning" >}}
**Avertissement Légal :** Les fonctionnalités Mode Moniteur et Injection de Paquets sont destinées uniquement aux tests de sécurité autorisés, à la recherche éducative et aux tests d'intrusion légaux. Assurez-vous toujours d'avoir l'autorisation explicite du propriétaire du réseau cible avant toute utilisation.
{{< /alert >}}

## Présentation du Produit

L'AWUS036ACS est le point d'entrée le plus abordable d'Alfa dans la gamme 802.11ac double bande avec support du mode moniteur et de l'injection de paquets. Propulsé par le chipset Realtek RTL8811AU, il est compact et léger avec une seule antenne RP-SMA détachable pouvant être améliorée pour une meilleure portée. Bien que moins puissant que l'ACH ou l'ACM, il constitue un choix pratique pour les débutants en recherche sécurité sans fil ou les utilisateurs ayant besoin d'un adaptateur 5 GHz économique avec connecteur d'antenne externe.

> **Avis macOS :** Tous les adaptateurs ALFA ont un support macOS limité. macOS 10.15 Catalina et versions ultérieures, ainsi que tous les Mac Apple Silicon (M1/M2/M3), ne sont **pas pris en charge**. L'AWUS036ACS prend en charge jusqu'à macOS 10.14 Mojave (Mac Intel uniquement).

## Caractéristiques Principales

- Chipset Realtek RTL8811AU — mode moniteur et injection de paquets pris en charge
- WiFi 5 (802.11ac) double bande — 2,4 GHz (150 Mbps) + 5 GHz (433 Mbps) = AC600
- 1× connecteur RP-SMA femelle avec 1× mini antenne détachable 2 dBi — améliorable avec des antennes panneau ou haute gain
- Format compact — profil réduit pour une grande portabilité
- Interface USB 2.0 (USB-A) — compatible avec tout port USB
- Compatible avec l'antenne panneau double bande Alfa APA-M25 pour une réception directionnelle
- Supporte Kali Linux sur Raspberry Pi (KaliPi) — installation du pilote via DKMS

## Spécifications Techniques

| Paramètre | Valeur |
|---|---|
| Chipset | Realtek RTL8811AU |
| Standards WiFi | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bandes de Fréquence | 2,4 GHz (150 Mbps) · 5 GHz (433 Mbps) |
| Vitesse Combinée Max | AC600 (150 + 433 Mbps) |
| Connecteur d'Antenne | 1× RP-SMA femelle |
| Antenne Incluse | 1× mini dipôle double bande, 2 dBi |
| Interface USB | USB 2.0 Type-A |
| Sensibilité de Réception | 802.11b : −85 dBm · 802.11g : −69 dBm · 802.11n : −68 dBm · 802.11ac : −59 dBm |
| Sécurité Sans Fil | WPA2 / WPA / WEP / 802.1X |
| Pays d'Origine | Taïwan |

> ⚠️ **REMARQUE :** USB 2.0 uniquement — vitesse maximale du bus de données 480 Mbps. Le débit est limité à 433 Mbps. Pour une vitesse maximale, utiliser l'AWUS036ACM ou l'AWUS036ACH avec USB 3.0.

## Compatibilité Système d'Exploitation

| Système d'Exploitation | Statut | Notes |
|---|---|---|
| Windows XP–11 | ✅ Pris en charge | Pilote disponible sur le site Alfa |
| macOS 10.5–10.14 | ⚠️ Limité | macOS 10.15+ et Apple Silicon NON pris en charge |
| Ubuntu | ✅ Pris en charge | Installation manuelle du pilote DKMS requise (morrownr/8821au). Pas de support intégré au noyau. |
| Kali Linux | ✅ Pris en charge | Mode moniteur + injection de paquets pris en charge. Pilote communautaire depuis GitHub morrownr. |
| NetHunter (Android) | ✅ Pris en charge | Connexion USB OTG ; compatibilité NetHunter confirmée pour RTL8811AU |

## Compatibilité Matérielle

| Matériel | Statut | Notes |
|---|---|---|
| Raspberry Pi 3B+/4/5 | ✅ Pris en charge | Installation KaliPi disponible via morrownr DKMS. |
| PC Bureau/Laptop | ✅ Pris en charge | USB-A standard |
| Mac (Intel) | ⚠️ Limité | macOS 10.5–10.14 uniquement |

## Fonctionnalités Avancées

| Fonctionnalité | Statut |
|---|---|
| Mode Moniteur | ✅ Oui |
| Injection de Paquets | ✅ Oui |
| Mode AP Logiciel | ✅ Oui |
| Bluetooth | ❌ Non |
| VIF | ⚠️ Limité |

## Contenu de la Boîte

- 1× Adaptateur AWUS036ACS
- 1× Mini antenne dipôle double bande détachable 2 dBi

## Ressources & Liens

| Ressource | Lien |
|---|---|
| Page Produit Officielle | https://www.alfa.com.tw/products/awus036acs_1 |
| Documentation Officielle | https://docs.alfa.com.tw/Product/AWUS036ACS/ |
| Pilote Linux (RTL8811AU) | https://github.com/morrownr/8821au-20210708 |

## Téléchargement Fiche Technique

[📄 Télécharger la Fiche AWUS036ACS](/docs/alfa/AWUS036ACS_spec.pdf)

## Galerie

{{< gallery >}}<img src="/images/products/alfa/awus036acs_image_1.png" alt="ALFA AWUS036ACS" />{{< /gallery >}}

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
Besoin d'un devis pour le produit ? Veuillez [nous contacter](/fr/contact/).
{{< /alert >}}
