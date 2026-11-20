---
title: "ALFA AWUS036EACS — Adaptateur USB Nano AC600 + Bluetooth 4.2"
description: "ALFA AWUS036EACS, Realtek RTL8821CU, AC600 double bande, format Nano USB 2.0, Bluetooth 4.2. Pilote mainline rtw88_8821cu depuis le noyau 6.2 ; sur GX10, mode moniteur et injection validés sur les deux bandes."
date: 2026-03-12
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "Nano", "Bluetooth 4.2", "Windows", "Home"]
---

## Présentation du Produit

L'AWUS036EACS est l'adaptateur combo WiFi + Bluetooth ultra-compact d'Alfa, conçu pour les utilisateurs à domicile et en bureau souhaitant une connectivité sans fil et Bluetooth dans une seule clé USB discrète. Construit autour du chipset Realtek RTL8821CU, il intègre le WiFi AC600 double bande et le Bluetooth 4.2 dans un format nano avec support de pilote intégré sous Windows. Son mode AP logiciel permet de partager votre connexion internet. Sous Linux, le pilote mainline rtw88_8821cu est inclus depuis le noyau 6.2. Lors des tests sur GX10 (Ubuntu 24.04, noyau 6.17), le mode moniteur et l'injection de paquets ont atteint 100 % en 2,4 GHz comme en 5 GHz, une capture de handshake WPA de bout en bout a réussi, et le Bluetooth et le Wi-Fi ont fonctionné simultanément.

> ⚠️ **Remarque :** L'AWUS036EACS est conçu pour une utilisation domestique sous Windows, mais il fonctionne aussi sous Linux avec le pilote mainline rtw88_8821cu (noyau 6.2+). Pas de port RP-SMA — l'antenne n'est pas améliorable.

## Caractéristiques du Produit

- WiFi double bande 802.11ac AC600 + Bluetooth 4.2 dans un seul adaptateur USB nano
- Plug-and-play sous Windows — le pilote intégré s'installe automatiquement
- Mode AP logiciel — créez un point d'accès WiFi directement depuis l'adaptateur
- Ultra-compact et portable — s'intègre discrètement dans n'importe quel port USB
- Double bande : 2,4 GHz (150 Mbps) + 5 GHz (433 Mbps)
- Antenne 2 dBi intégrée — pas de connecteur RP-SMA externe
- Idéal pour les PC de bureau, systèmes embarqués ou PC domestiques nécessitant WiFi + BT dans un espace minimal
- Bluetooth 4.2 prend en charge la diffusion audio, claviers, souris et autres périphériques

## Spécifications Techniques

| Paramètre | Valeur |
|-----------|-------|
| Chipset | Realtek RTL8821CU |
| Standards WiFi | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bluetooth | BT 4.2 (2,4 GHz) |
| Bandes de Fréquence | WiFi : 2,4 GHz · 5 GHz · BT : 2,4 GHz |
| Débit Maximum | 802.11b : 11 Mbps · 802.11g : 54 Mbps · 802.11n : 150 Mbps · 802.11ac : 433 Mbps |
| Vitesse Combinée Max | AC600 (150 + 433 Mbps) |
| Antenne | Intégrée, 2 dBi (non amovible, pas de RP-SMA) |
| Interface USB | USB 2.0 |
| Puissance d'Émission | 17 dBm typique |
| Sensibilité de Réception | 802.11b : −85 dBm · 802.11g : −69 dBm · 802.11n : −68 dBm · 802.11ac : −59 dBm |
| Sécurité Sans Fil | WEP / WPA-PSK / WPA2-PSK / 802.1X |
| Température de Fonctionnement | −10°C à 60°C |
| Format | Nano / profil bas |
| Pays d'Origine | Taïwan |

## Compatibilité Système d'Exploitation

| Système d'Exploitation | Statut | Notes |
|----|--------|-------|
| Windows XP–10 | ✅ Pris en charge | Pilote intégré ; plug and play. Consulter la page pilote Alfa pour la compatibilité Windows 11. |
| macOS | ⚠️ Limité | Plage de versions exacte à confirmer. Aucun support Apple Silicon. |
| Ubuntu / Linux | ✅ Noyau 6.2+ | Pilote mainline rtw88_8821cu, aucune installation requise (testé sur GX10, Ubuntu 24.04, noyau 6.17). |
| Kali Linux | ✅ Pris en charge | Mode moniteur et injection de paquets vérifiés sur GX10 (Ubuntu 24.04, noyau 6.17) : 100 % sur les deux bandes, capture de handshake WPA de bout en bout réussie. Non testé sur un vrai Kali. |
| NetHunter (Android) | ❌ Non recommandé | RTL8821CU non confirmé fonctionnel avec NetHunter. |

## Compatibilité Matérielle

| Matériel | Statut | Notes |
|----------|--------|-------|
| Raspberry Pi | ⚠️ Non testé | Non testé par nos soins ; le noyau 6.2+ inclut le pilote mainline rtw88_8821cu. |
| PC Bureau / Laptop | ✅ Pris en charge | Windows uniquement recommandé. |
| Embarqué / IoT (Windows) | ⚠️ Windows uniquement | Le design compact convient aux systèmes Windows embarqués. |

## Fonctionnalités Avancées

| Fonctionnalité | Statut |
|---------|--------|
| Mode Moniteur | ✅ Oui (test GX10 : 100 % sur les deux bandes) |
| Injection de Paquets | ✅ Oui (test GX10 : 100 % sur les deux bandes) |
| Mode AP Logiciel | ✅ Oui |
| Bluetooth | ✅ BT 4.2 (utilisable en même temps que le Wi-Fi) |
| VIF | 🟡 Partielle (monitor passif + managed sur le même canal ; pas de double VIF indépendante) |

## Contenu de la Boîte

- 1× Adaptateur nano AWUS036EACS

## Ressources & Liens

| Ressource | Lien |
|----------|------|
| Page Produit Officielle | https://www.alfa.com.tw/products/awus036eacs_1 |
| Documentation Officielle | https://docs.alfa.com.tw/Product/AWUS036EACS/ |

## Téléchargement Fiche Technique

Fiche technique officielle disponible prochainement.

{{< gallery >}}
  <img src="/images/products/alfa/awus036eacs_image_1.png" alt="ALFA AWUS036EACS" />
{{< /gallery >}}

---

## Améliorations d'Antennes Compatibles

Tous les adaptateurs ALFA disposent d'un connecteur RP-SMA standard. Améliorez les performances avec une antenne externe optionnelle pour une portée et un gain accrus :

| Antenne | Fréquence | Gain | Type |
|---------|-----------|------|------|
| [ALFA APA-M04](/fr/products/alfa/apa-m04/) | 2,4 GHz | 7 dBi | Panneau Intérieur |
| [ALFA APA-M25](/fr/products/alfa/apa-m25/) | 2,4 / 5 GHz | 8 / 10 dBi | Panneau Intérieur Double Bande |
| [ALFA APA-M25-6E](/fr/products/alfa/apa-m25-6e/) | 2,4 / 5 / 6 GHz | 8 / 10 / 9 dBi | Panneau Intérieur Tri-Bande |
| [ARS 25-57A](/fr/products/alfa/ars-25-57a/) | 2,4 / 5 GHz | 2,5 / 7 dBi | Omni Extérieur |
| [ARS NT5B7](/fr/products/alfa/ars-nt5b7/) | 2,4 / 5 GHz | 4 / 5 / 7 dBi | Omni |

{{< alert >}}
Besoin d'un devis pour le produit ? Veuillez [nous contacter](/fr/contact/).
{{< /alert >}}
