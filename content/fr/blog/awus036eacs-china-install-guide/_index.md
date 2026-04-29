---
title: "Guide de configuration de l'ALFA AWUS036EACS pour la Chine : Installation sous Windows et compatibilité Linux"
description: "Guide de configuration de l'ALFA AWUS036EACS en Chine. Adaptateur nano WiFi 5 + Bluetooth 4.2 RTL8821CU. Pilote Windows disponible sur files.alfa.com.tw. Linux et Kali Linux ne sont pas supportés — voir les alternatives recommandées."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036eacs-china-install-guide"
tags: ["alfa", "awus036eacs", "windows", "driver", "china", "bluetooth", "rtl8821cu"]
categories: ["Guides de Pilotes"]
series: ["alfa-china-install-guide"]
series_order: 8
related_product: "/fr/products/alfa/awus036eacs/"
---

L'AWUS036EACS est l'adaptateur combiné nano WiFi 5 + Bluetooth 4.2 d'ALFA. Il est conçu pour les utilisateurs Windows qui ont besoin d'une mise à niveau sans fil compacte. Son chipset RTL8821CU n'a pas de pilote Linux open-source fiable — le mode moniteur et l'injection de paquets ne sont pas supportés. Ce guide couvre l'installation sous Windows à partir de sources chinoises et explique clairement les limitations de Linux.

## Utilisateurs Linux : Veuillez lire ceci en premier

> **L'AWUS036EACS ne fonctionne pas de manière fiable sur Kali Linux, Ubuntu, Debian ou Raspberry Pi.** Le chipset RTL8821CU n'a pas de pilote open-source maintenu. Le mode moniteur, l'injection de paquets et le VIF ne sont pas disponibles.
>
> Si vous avez besoin d'un adaptateur compatible Linux pour la recherche en sécurité, utilisez l'un de ceux-ci à la place :
> - **[AWUS036ACM](/fr/blog/awus036acm-china-install-guide/)** — Pilote MT7612U dans le noyau, mode moniteur complet + VIF
> - **[AWUS036ACS](/fr/blog/awus036acs-china-install-guide/)** — RTL8811AU, mode moniteur économique

---

## Configuration Windows 10 / 11

### Étape 1 : Télécharger le pilote depuis Alfa

Le serveur de pilotes officiel d'Alfa est accessible depuis la Chine :

https://files.alfa.com.tw

Naviguez vers le dossier produit **AWUS036EACS** et téléchargez le package de pilote Windows (`.zip` ou `.exe`).

### Étape 2 : Installer le pilote

1. Extrayez le fichier zip téléchargé.
2. Faites un clic droit sur l'installateur `.exe` et sélectionnez **Exécuter en tant qu'administrateur**.
3. Suivez les instructions à l'écran.
4. Redémarrez lorsque vous y êtes invité.

---

## Détails de compatibilité Linux

### Kali Linux

Le RTL8821CU n'a pas de pilote DKMS maintenu pour les noyaux Kali modernes. Des pilotes maintenus par la communauté existent mais sont instables.

**Recommandation :** Utilisez l'[AWUS036ACM](/fr/blog/awus036acm-china-install-guide/) pour les travaux de sécurité sur Kali Linux.

---

## Référence des miroirs chinois

| Ressource | URL | Utilisation pour |
|----------|-----|---------|
| Pilotes officiels Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Pilote Windows EACS |

## Plus de guides d'installation d'adaptateurs Alfa pour la Chine

- [AWUS036ACH China Install Guide](/fr/blog/awus036ach-china-install-guide/) — RTL8812AU, haute puissance
- AWUS036EACS ← vous êtes ici

Des questions ? Laissez un commentaire ci-dessous ou contactez-nous sur [yupitek.com](https://yupitek.com/fr/contact/).
