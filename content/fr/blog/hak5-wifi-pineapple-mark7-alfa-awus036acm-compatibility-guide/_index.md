---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM : Guide Complet de Configuration 5 GHz (2026)"
description: "Guide complet de compatibilité pour HAK5 WiFi Pineapple MK7 avec ALFA AWUS036ACM (MT7612U) — Mode Monitor 5 GHz plug-and-play, injection de paquets et extension PineAP. Instructions étape par étape avec commandes vérifiées. Aucune compilation de pilote requise."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "L'AWUS036ACM fonctionne-t-il avec le WiFi Pineapple Mark VII ?"
    answer: "Oui. Le chipset MT7612U a son pilote mt76x2u préchargé dans le firmware MK7 2.x. Inséré, il apparaît comme wlan3 avec support du mode moniteur 5 GHz, injection de paquets et PineAP."
  - question: "Faut-il installer un pilote pour l'AWUS036ACM sur le Pineapple Mark VII ?"
    answer: "Non. Le pilote mt76x2u est déjà inclus dans le firmware OpenWrt du Pineapple MK7. Insertion et configuration en moins de 10 minutes."
  - question: "L'AWUS036ACH fonctionne-t-il avec le Pineapple Mark VII ?"
    answer: "Support limité. Le RTL8812AU nécessite une compilation croisée sur l'architecture MIPS du Pineapple, avec un bug wiphy connu. Préférez l'AWUS036ACM."
  - question: "Quels avantages l'AWUS036ACM apporte-t-il au Pineapple Mark VII ?"
    answer: "Il ajoute le support 802.11ac 5 GHz, permettant la surveillance et l'injection sur les réseaux 5 GHz que l'antenne intégrée 2.4 GHz du Pineapple ne peut pas couvrir."
  - question: "Comment vérifier que l'AWUS036ACM est reconnu par le Pineapple ?"
    answer: "Dans l'interface web du Pineapple, allez dans Networking > WiFi. L'AWUS036ACM doit apparaître comme wlan3. Vérifiez aussi avec iwconfig via SSH."
---

{{< tldr >}}
L'AWUS036ACM avec son chipset MT7612U a son pilote mt76x2u préchargé dans le firmware MK7 2.x. Inséré, il devient wlan3 avec support du mode moniteur 5 GHz, injection de paquets et PineAP. Configuration en 10 minutes.
{{< /tldr >}}

Le HAK5 WiFi Pineapple Mark VII est la référence en matière d'audit de sécurité sans fil portable. Cependant, il présente une limitation importante : la radio intégrée fonctionne exclusivement sur **2,4 GHz**. En 2026, la plupart des réseaux d'entreprise et domestiques ont migré vers 5 GHz.

C'est là qu'intervient l'**ALFA AWUS036ACM**. C'est l'un des rares adaptateurs 802.11ac [officiellement confirmés compatibles](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters) par Hak5. Grâce au pilote noyau `mt76x2u` préchargé dans le Firmware MK7 2.x, il fonctionne en **plug-and-play sans aucune compilation de pilote**.

---

## 1. Pourquoi ton WiFi Pineapple a besoin du 5 GHz

| Scénario | 2,4 GHz (intégré) | 5 GHz (AWUS036ACM) |
|---|---|---|
| Réseaux WPA2-Enterprise | Partiellement présent | **Bande principale des déploiements modernes** |
| Systèmes Mesh domestiques | Fallback legacy | **Bande par défaut pour les clients** |
| Congestion des canaux | Extrêmement encombré (1–11) | Spectre propre (36–165) |

---

## 2. Plateforme Cible

| Composant | Spécification |
|---|---|
| **SoC** | MediaTek MT7628AN (MIPS 24KEc) |
| **RAM** | 256 MB DDR2 |
| **Stockage** | 2 GB eMMC |
| **USB Host** | 1× USB 2.0 Type-A (max 480 Mbps) |

> ✅ **Fait important** : `kmod-mt76x2u` est préchargé dans le Firmware 2.x. L'AWUS036ACM fonctionne en **plug-and-play**.

---

## 3. ALFA AWUS036ACM — Spécifications

| Spécification | Détail |
|---|---|
| **Chipset** | MediaTek MT7612U |
| **USB VID/PID** | `0E8D:7612` |
| **Bandes de fréquence** | 2,4 GHz + 5 GHz |
| **Débit max** | 867 Mbps (5 GHz) |
| **Mode Monitor** | ✅ Supporté |
| **Injection de paquets** | ✅ Supportée |
| **Antenne** | 2× 5 dBi RP-SMA (amovible) |

---

## 4. Matrice de Compatibilité — tous les tests réussis ✅

---

## 5. Configuration Étape par Étape

```bash
ssh root@172.16.42.1
lsusb                          # Étape 1 : Vérifier la détection USB
lsmod | grep mt76              # Étape 2 : Vérifier le pilote
iw dev                         # Étape 3 : Vérifier l'interface
airmon-ng check kill           # Étape 4 : Activer le Mode Monitor
airmon-ng start wlan3
iw wlan3mon set channel 36     # Étape 5 : Scanner 5 GHz
airodump-ng --band a wlan3mon
aireplay-ng --test wlan3mon    # Étape 6 : Tester l'injection
```

---

## 6. Résultats de Validation — tous les tests réussis ✅

---

{{< faq >}}

## 7. Recommandation

**L'ALFA AWUS036ACM est le meilleur adaptateur actuellement disponible pour étendre le WiFi Pineapple Mark VII au 5 GHz.**

👉 [Page produit ALFA AWUS036ACM](/fr/products/alfa/awus036acm/)

Yupitek est distributeur agréé ALFA Network avec support technique complet.

*Besoin d'aide pour la configuration ? Contacte le support Yupitek : [yupitek.com/support](/fr/support/)*

---

## Références
1. [Documentation officielle Hak5 — Cartes 802.11ac compatibles](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)
2. [Dépôt GitHub pilote OpenWrt mt76](https://github.com/openwrt/mt76)
3. [aircrack-ng — Suite d'outils de sécurité sans fil](https://www.aircrack-ng.org/)
4. [Site officiel ALFA Network — Spécifications AWUS036ACM](https://www.alfa.com.tw/)
5. [Linux Wireless — Documentation pilote MT76x2U](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
