---
title: "Construire un routeur 4G/5G avec Raspberry Pi et OpenWrt : matrice de compatibilité des modules Sierra et guide de configuration"
description: "Construis ton propre routeur OpenWrt avec un Raspberry Pi et des modules 4G/5G Sierra Wireless (EM7455, EM7565, EM7511, EM919x, MC7455). Matrice de compatibilité complète, configuration QMI/MBIM, mise en ligne via wwan0, plus des recommandations sur l'alimentation et les antennes."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "raspberry-pi-openwrt-lte-router"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/fr/products/sierra/"
faq:
  - question: "Quel module Sierra choisir pour un routeur OpenWrt sur Raspberry Pi ?"
    answer: "Les débutants devraient commencer avec l'EM7455 : les tutoriels sont nombreux et les problèmes faciles à rechercher. Choisis l'EM7565 ou l'EM7511 pour un débit montant élevé, l'EM919x pour la 5G et le MC7455 pour les anciens slots mPCIe."
  - question: "Quelle est la différence entre QMI et MBIM ?"
    answer: "QMI est le protocole propre de Qualcomm, tandis que MBIM est le protocole standardisé plus récent. Les deux fonctionnent sur OpenWrt, mais la plupart des guides en ligne utilisent QMI."
  - question: "Que faire si le Raspberry Pi ne détecte pas le module ?"
    answer: "La cause la plus courante est une alimentation USB insuffisante sur le Raspberry Pi (le courant d'appel de pointe peut atteindre 2,5 A). Vérifie l'alimentation de la carte adaptatrice et le câblage, puis attends une dizaine de secondes que le module termine son démarrage."
---

Un Raspberry Pi peut-il transformer un module 4G/5G Sierra Wireless en routeur OpenWrt pleinement fonctionnel ? Oui. Les modules M.2 comme l'EM7455, l'EM7565, l'EM7511 et l'EM919x sont nativement pris en charge sous Linux. Installe `kmod-usb-net-qmi-wwan` ou `kmod-usb-net-cdc-mbim`, configure `wwan0`, et tu es en ligne. Cet article couvre la matrice de compatibilité complète des modules, la configuration pas à pas et les pièges d'alimentation et d'antennes à éviter.

{{< tldr >}}
Un Raspberry Pi avec un module Sierra 4G/5G fait un routeur OpenWrt fiable. La plupart des modules M.2 (EM7455, EM7565, EM7511) utilisent l'USB, l'EM919x ajoute une voie PCIe Gen3 et le MC7455 est la version mPCIe de l'EM7455. Sur OpenWrt, le protocole QMI avec `wwan0` est la voie recommandée : installe `kmod-usb-net-qmi-wwan`, `uqmi` et `luci-proto-qmi`, renseigne l'APN dans `/etc/config/network`, puis redémarre le réseau. Côté vitesse : l'EM7455 / le MC7455 sont LTE Cat 6 (300/50 Mbit/s), l'EM7565 / l'EM7511 sont Cat 12 (600/150 Mbit/s) et la famille EM919x délivre la 5G Sub-6 (l'EM9190 ajoute le mmWave).
{{< /tldr >}}

## Matrice de compatibilité complète des modules Sierra sur OpenWrt

Avant de commencer, vérifie ton module dans ce tableau :

| Modèle | Classe de vitesse | Puce baseband | Facteur de forme | Chemin de données Linux | Positionnement GNSS |
|---|---|---|---|---|---|
| **EM7455** | LTE Cat 6 (300/50 Mbit/s) | MDM9230 | M.2 (42x30 mm) | QMI (Linux) / MBIM | GPS/GLONASS/BeiDou/Galileo |
| **EM7565** | LTE Cat 12 (600/150 Mbit/s) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM (les deux sous Linux) | ajoute QZSS |
| **EM7511** | LTE Cat 12 (600/150 Mbit/s) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM | ajoute QZSS |
| **EM919x** (9190/9191/7690) | 5G Sub-6 (le 9190 ajoute le mmWave) | SDX55 | M.2 (52 mm de long) | Windows/Linux | L1 + L5 (optionnel) |
| **MC7455** | LTE Cat 6 (300/50 Mbit/s) | MDM9230 | mPCIe (50,95x30 mm) | QMI / MBIM | GPS/GLONASS/BeiDou/Galileo |

### Comment choisir un module

- **Makers débutants** : choisis l'**EM7455**. Les guides sont nombreux et les problèmes faciles à rechercher.
- **Fort besoin en upload (streaming, vidéosurveillance)** : choisis l'**EM7565** ou l'**EM7511** pour un upload jusqu'à 150 Mbit/s.
- **La 5G est requise** : choisis l'**EM9190** pour les vitesses 5G.
- **Slot mPCIe ancien uniquement** : opte pour le **MC7455**.

## Trois façons de connecter le matériel

### A. Raspberry Pi 5 + HAT M.2 (PCIe)

Le Pi 5 dispose du PCIe, donc une carte support HAT+ M.2 te permet de brancher directement un module WWAN M.2 (confirme qu'il s'agit d'une clé B).

### B. Raspberry Pi 4B ou plus ancien + boîtier adaptateur WWAN USB

Les modules de la série EM prennent aussi en charge l'USB 2.0/3.0, donc un boîtier M.2 vers USB (généralement avec un slot SIM intégré) branché sur le port USB du Pi est la voie la plus simple et la plus accessible.

### C. Adaptateur MC7455 (mPCIe)

Le MC7455 utilise l'ancienne interface mPCIe, il te faut donc une carte adaptatrice mPCIe vers USB ou mPCIe vers M.2.

> ⚠️ **L'alimentation est le plus gros piège** : le module consomme de 3,135 à 4,4 V (typiquement 3,3 V). Une erreur « module non détecté » signifie généralement que l'alimentation USB du Raspberry Pi ne fournit pas assez de puissance. Le courant d'appel peut grimper à 2,5 A, alors laisse une bonne marge sur ta source d'alimentation.

## Comprendre QMI et MBIM

Les deux protocoles contrôlent la façon dont le module 4G/5G se connecte au réseau :

- **QMI** : le protocole propre de Qualcomm, utilisé par la plupart des guides Linux/OpenWrt (l'interface apparaît sous le nom `wwan0`).
- **MBIM** : le protocole standardisé plus récent, utilisable sous Windows comme sous Linux (l'interface apparaît aussi sous le nom `wwan0`).

**Lequel choisir ?** La plupart des utilisateurs peuvent utiliser QMI directement. Passe à MBIM uniquement si ton firmware l'exige explicitement.

## Pratique, partie 1 : configurer QMI sur OpenWrt

Quatre étapes, aucune compilation requise.

### 1. Installer les paquets

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi
```

### 2. Vérifier que le Raspberry Pi détecte le module

```bash
lsusb                                  # chercher un périphérique Sierra
ls /dev/cdc-wdm*                       # canal de contrôle QMI
dmesg | grep qmi_wwan                  # vérifier que le pilote est chargé
ip link show wwan0                     # vérifier que l'interface est apparue
```

### 3. Configurer le fichier réseau (`/etc/config/network`)

Ajoute une section QMI et remplace l'APN par celui de ton opérateur :

```bash
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option auth 'none'
```

### 4. Redémarrer le réseau

```bash
/etc/init.d/network restart
ifup wwan
```

Et voilà. Dès que `wwan0` obtient une adresse IP, tu es en ligne.

## Antennes et SIM : ne saute pas ces étapes

Le module n'a **pas d'antenne intégrée**, et la qualité des antennes influence directement ton débit.

- **Antenne principale** : obligatoire.
- **Antenne auxiliaire (Aux)** : requise pour les vitesses MIMO ; sans elle, le débit chute.
- **Antenne GNSS** : uniquement pour les cas d'usage de positionnement. Ne la confonds pas avec l'antenne principale.

## Pièges courants (à lire absolument pour les débutants)

1. **`lsusb` n'affiche rien** : dans 99 % des cas, c'est une alimentation insuffisante, une carte adaptatrice mal fixée ou un câble défectueux.
2. **Trop d'impatience** : le module a besoin de temps pour démarrer. Attends 10 secondes après le branchement avant de lancer des commandes.
3. **Les modules 5G (EM919x) chauffent** : des températures autour de 100 °C sont courantes (115 °C max), donc prévois un refroidissement.
4. **Conflits avec ModemManager** : quand tu travailles manuellement sur un système Linux standard, arrête d'abord `ModemManager` (`systemctl stop ModemManager`) pour qu'il ne prenne pas le contrôle du module.

## Résumé

Piloter un module Sierra depuis un Raspberry Pi avec OpenWrt, c'est un processus à suivre pas à pas. Vérifie le matériel (facteur de forme, tension, antennes), installe les pilotes QMI/MBIM, puis renseigne l'APN. Nous espérons que ce guide évitera quelques détours à ton projet et amènera ton Raspberry Pi à pleine vitesse 4G/5G.

## Informations d'achat (appel à l'action)

Si tu as besoin de modules EM7455, EM7565, EM7511, ou de cartes adaptatrices M.2 et d'antennes compatibles, Yupitek propose des solutions matérielles complètes et des conseils techniques.

Écris-nous : **sales@yupitek.com**

Voir les produits : [Série Sierra Wireless de Yupitek](https://yupitek.com/en/products/sierra/)
