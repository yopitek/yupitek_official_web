---
title: "Guide de configuration de l'ALFA AWUS036EACS pour la Chine : Installation sous Windows et compatibilité Linux"
description: "Guide de configuration de l'ALFA AWUS036EACS en Chine. Adaptateur nano WiFi 5 + Bluetooth 4.2 RTL8821CU. Pilote Windows disponible sur files.alfa.com.tw. Sous Linux noyau 6.2+, le pilote intégré rtw88_8821cu fonctionne dès le branchement — mode moniteur et injection testés et fonctionnels."
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
featureimage: "/images/blog/awus036eacs-china-install-guide.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Quel chipset utilise l'AWUS036EACS ? Supporte-t-il le Bluetooth ?"
    answer: "Il utilise le chipset Realtek RTL8821CU, supportant le WiFi 5 et le Bluetooth 4.2."
  - question: "L'AWUS036EACS est-il recommandé pour Linux ?"
    answer: "Oui. Sous Linux noyau 6.2+ (par ex. Ubuntu 24.04 HWE / noyau 6.17), le pilote rtw88_8821cu est intégré au noyau, sans compilation et fonctionnel dès le branchement. Nous avons mesuré le mode moniteur et l'injection de paquets à 100 % sur les deux bandes (2,4 GHz / 5 GHz) avec capture WPA .22000 de bout en bout, et le Bluetooth a aussi été testé avec succès."
  - question: "Comment installer le pilote AWUS036EACS sur Windows ?"
    answer: "Téléchargez le paquet de pilotes Windows depuis files.alfa.com.tw, installez en tant qu'administrateur et redémarrez."
  - question: "Comment activer le Bluetooth de l'AWUS036EACS ?"
    answer: "Après installation du pilote, le Bluetooth s'active généralement automatiquement. Activez-le dans les paramètres Windows."
  - question: "Quelle carte choisir pour la recherche en sécurité sans fil sous Linux ?"
    answer: "L'AWUS036EACS lui-même fonctionne pour le mode moniteur et l'injection de paquets sous le noyau 6.2+, avec le Bluetooth en bonus. Si vous voulez plus d'options, l'AWUS036ACM et l'AWUS036ACS supportent également pleinement le mode moniteur sous Linux. À utiliser uniquement sur des réseaux qui vous appartiennent ou que vous êtes autorisé à tester."
---

{{< tldr >}}
L'AWUS036EACS utilise le chipset RTL8821CU, carte mini WiFi 5 avec Bluetooth 4.2. Installation simple sous Windows ; sous Linux noyau 6.2+, le pilote rtw88_8821cu est intégré, si bien que le mode moniteur et l'injection de paquets fonctionnent dès le branchement, et le Bluetooth est également testé et fonctionnel.
{{< /tldr >}}

L'AWUS036EACS est l'adaptateur combiné nano WiFi 5 + Bluetooth 4.2 d'ALFA. C'est une mise à niveau sans fil compacte pour les utilisateurs Windows, et sous Linux noyau 6.2+, le pilote intégré rtw88_8821cu le prend en charge dès le branchement (sans compilation). Ce guide couvre l'installation sous Windows à partir de sources chinoises et l'utilisation sous Linux.

## Utilisateurs Linux : Veuillez lire ceci en premier

> **L'AWUS036EACS fonctionne dès le branchement sous Linux noyau 6.2+.** Les noyaux 6.2 et plus récents (par ex. Ubuntu 24.04 HWE / noyau 6.17) incluent le pilote rtw88_8821cu intégré, donc aucune compilation n'est nécessaire. Nous avons mesuré le mode moniteur et l'injection de paquets à 100 % sur les deux bandes (2,4 GHz / 5 GHz), capturé une poignée de main WPA de bout en bout (.22000), et le Bluetooth (BT) est aussi testé et fonctionnel (BR/EDR + BLE détectent tous deux des appareils et coexistent avec le WiFi). À utiliser uniquement sur des réseaux qui vous appartiennent ou que vous êtes autorisé à tester.
>
> **Conseil pratique :** C'est une carte combo BT+WiFi. Après des changements de mode répétés, la réception WiFi peut se bloquer (`ip link set up` renvoie `Operation already in progress` et `iw ... set channel` renvoie `-16 busy`). Avant chaque phase de test, débranchez l'adaptateur et rebranchez-le sur un autre port USB pour le réinitialiser.
>
> Autres adaptateurs Linux de la même série :
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

Sous **noyau 6.2+**, le RTL8821CU est piloté par le module intégré `rtw88_8821cu`, il n'y a donc rien à compiler — branchez-le et il est reconnu. Vérifiez d'abord votre version de noyau avec `uname -r`.

### Kali Linux

Avec un noyau 6.2+, le pilote intégré `rtw88_8821cu` se charge automatiquement. Nous avons testé le mode moniteur et l'injection de paquets à 100 % sur les deux bandes (2,4 GHz / 5 GHz) et capturé une poignée de main WPA de bout en bout (.22000). À utiliser uniquement sur des réseaux qui vous appartiennent ou que vous êtes autorisé à tester.

```bash
sudo nmcli dev set wlxXXXX managed no
sudo ip link set wlxXXXX down
sudo iw dev wlxXXXX set type monitor
sudo ip link set wlxXXXX up
```

### Ubuntu / Debian / Raspberry Pi

Dès que le noyau est 6.2 ou plus récent (y compris les versions ARM64 comme sur Raspberry Pi), le pilote intégré `rtw88_8821cu` gère l'adaptateur sans compilation. Sur un noyau plus ancien, passez au noyau HWE pour obtenir le pilote intégré.

### Conseil pratique (carte combo BT+WiFi)

Comme l'EACS réunit Bluetooth et WiFi sur une seule puce, des changements de mode répétés peuvent bloquer la réception WiFi — `ip link set up` renvoie `Operation already in progress` et `iw ... set channel` renvoie `-16 busy`. Avant chaque phase de test, débranchez l'adaptateur et rebranchez-le sur un autre port USB pour réinitialiser l'état. Le Bluetooth (BR/EDR + BLE) est testé, fonctionnel et coexiste avec le WiFi.

---

## Référence des miroirs chinois

| Ressource | URL | Utilisation pour |
|----------|-----|---------|
| Pilotes officiels Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Pilote Windows EACS |

{{< faq >}}

## Plus de guides d'installation d'adaptateurs Alfa pour la Chine

- [AWUS036ACH China Install Guide](/fr/blog/awus036ach-china-install-guide/) — RTL8812AU, haute puissance
- AWUS036EACS ← vous êtes ici

Des questions ? Laissez un commentaire ci-dessous ou contactez-nous sur [yupitek.com](https://yupitek.com/fr/contact/).

---

## Références
1. [Site officiel ALFA Network](https://www.alfa.com.tw/)
2. [Téléchargement de pilotes officiels ALFA](https://files.alfa.com.tw)
3. [Site officiel Realtek](https://www.realtek.com/)
