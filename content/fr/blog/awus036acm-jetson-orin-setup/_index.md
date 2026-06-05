---
title: "Sans compilation de pilotes ! Guide pratique plug-and-play de l'ALFA AWUS036ACM sur les hôtes Edge AI Jetson Orin"
description: "Destiné aux clients de l'AVALUE AIB-NW01 (NVIDIA Jetson Orin NX/Nano), une analyse approfondie de la meilleure clé WiFi USB ALFA Network pour les déploiements Edge AI, avec la preuve concrète que l'AWUS036ACM fonctionne véritablement en plug-and-play."
date: 2026-05-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Jetson-Orin", "Edge-AI", "USB-WiFi", "AWUS036ACM", "AVALUE", "AIB-NW01"]
featureimage: "/images/blog/awus036acm-jetson-orin-setup.webp"
---

## Un e-mail client révèle une question cruciale

> « J'ai un AVALUE AIB-NW01 (Jetson Orin NX) à déployer dans un environnement sans réseau filaire. Quelle clé WiFi USB parmi les vôtres puis-je utiliser directement ? »

Voici une question récemment reçue par Yupitek. Elle semble simple, mais si vous avez passé du temps dans la communauté des développeurs Jetson, vous savez que — **les clés WiFi USB sur la plateforme NVIDIA Jetson sont bien plus problématiques qu'on ne l'imagine.**

Nous avons étudié l'architecture du noyau Jetson, les cas concrets du forum NVIDIA, les rapports d'échec de compilation de pilotes sur GitHub, jusqu'aux données de test réelles sur plateforme ARM64, pour compiler ce guide d'achat.

---

## Options de connectivité sans fil de l'AIB-NW01 : comprendre votre plateforme

L'AVALUE AIB-NW01 est un **système embarqué sans ventilateur** conçu pour les applications Edge AI, offrant quatre configurations de SoM NVIDIA Jetson Orin. Voici ses spécifications matérielles complètes et son environnement logiciel :

### Vue d'ensemble des spécifications matérielles

| Élément | Spécification |
|------|------|
| **Options SoM** | Jetson Orin NX 16 Go / NX 8 Go / Orin Nano 8 Go / Orin Nano 4 Go |
| **CPU** | ARM Cortex-A78AE v8.2 64-bit（NX 16 Go : 8 cœurs @ 2,0 GHz / NX 8 Go : 6 cœurs @ 2,0 GHz / Nano : 6 cœurs @ 1,5 GHz） |
| **GPU** | Architecture NVIDIA Ampere（NX : 1024 CUDA Cores + 32 Tensor Cores / Nano 4 Go : 512 CUDA Cores + 16 Tensor Cores） |
| **Performance IA** | 100 / 70 / 40 / 20 TOPS（selon la configuration SoM） |
| **Mémoire** | LPDDR5（NX 16 Go/8 Go : 128-bit 102,4 Go/s / Nano 8 Go : 128-bit 68 Go/s / Nano 4 Go : 64-bit 34 Go/s） |
| **Stockage** | SSD NVMe M.2 2280 128 Go（intégré） |
| **Réseau** | 2 × GbE RJ-45（10/100/1000 Mbps） |
| **USB** | 4 × USB 3.1 Type-A、1 × Micro USB OTG |
| **Affichage** | 1 × HDMI Type-A |
| **Ports série** | 2 × DB9（RS-232 / RS-485 commutable par cavalier） |
| **Slots d'extension** | 1 × M.2 M-Key 2242/2280（SSD NVMe）、1 × M.2 E-Key 2230（module WiFi/BT）、1 × M.2 B-Key 3042/3052（module 5G/LTE, limité à une température ambiante normale） |
| **SIM** | 1 × slot Micro SIM |
| **Alimentation** | DC 10~24 V（bornier 2 broches） |
| **Dimensions** | 125 × 196 × 66 mm（sans support mural） |
| **Poids** | 1,4 kg |
| **Matériau du boîtier** | Aluminium extrudé + acier, dissipation sans ventilateur |
| **Température de fonctionnement** | -15 °C ~ 60 °C（selon IEC60068-2, flux d'air 0,5 m/s） |
| **Température de stockage** | -40 °C ~ 80 °C |
| **Certifications** | CE、FCC Class A |

### Environnement logiciel

| Élément | Spécification |
|------|------|
| **Système d'exploitation** | Ubuntu 20.04.6 LTS (Focal Fossa) |
| **SDK NVIDIA** | JetPack 5.0（inclut CUDA 11.4、cuDNN 8.4、TensorRT 8.4） |
| **Noyau Linux** | 5.10.x-tegra（noyau Tegra personnalisé par NVIDIA, **différent du noyau Ubuntu standard**） |
| **Architecture CPU** | ARM64 (aarch64) |
| **Ressources SDK IA** | [github.com/Avalue-Technology](https://github.com/Avalue-Technology/repositories.directory) |

> **Rappel important** : la plateforme Jetson utilise le noyau personnalisé `linux-tegra` maintenu par NVIDIA, et non le noyau Ubuntu standard. Cela a un impact profond sur la compatibilité des pilotes tiers — voir la section « Les trois défis des clés WiFi USB sur Jetson Orin » ci-dessous.

Cette machine offre trois voies de connectivité sans fil :

### M.2 2230 E-Key（slot module WiFi）

**Avantages** : débit élevé, intégré à la carte mère, n'occupe pas de port USB
**Inconvénients** : nécessite le démontage, connecteurs d'antenne fixés dans le boîtier, remplacement difficile, compatibilité des modules à vérifier un par un

### USB 3.1 Type-A（4 ports）

**Avantages** : hot-plug, pas de démontage, antennes positionnables au meilleur emplacement pour le signal, partageable entre appareils
**Inconvénients** : encombrement supérieur, débit plafonné par l'interface USB

### 5G M.2 B-Key（en option）

**Avantages** : connexion indépendante, pas de dépendance à l'infrastructure WiFi sur site
**Inconvénients** : coût élevé, nécessite une carte SIM et un abonnement, configuration complexe

Pour la majorité des scénarios de déploiement Edge AI — phase de POC, surveillance extérieure, lignes de production — **la clé WiFi USB est le choix le plus flexible et le plus économique.**

Mais la question se pose : peut-on simplement acheter n'importe quelle clé WiFi USB et la brancher sur le Jetson ?

La réponse est : **pas nécessairement. Et le taux d'échec est bien plus élevé que vous ne l'imaginez.**

---

## Les trois défis des clés WiFi USB sur Jetson Orin

La plupart des articles sur le WiFi USB ne traitent que du Linux x86, mais la plateforme Jetson est une tout autre histoire.

### Défi n°1 : votre noyau n'est pas le noyau Ubuntu

Le Jetson fonctionne avec le **noyau Tegra Linux personnalisé par NVIDIA**, et non avec le noyau Ubuntu standard. Cela signifie que :

- `apt install linux-headers-$(uname -r)` **ne pourra probablement pas obtenir les en-têtes du noyau correspondants**
- NVIDIA applique des patches au noyau qui peuvent casser l'ABI requise par les pilotes tiers
- L'environnement de compilation des modules du noyau est totalement différent de celui d'un poste de travail x86

Les clés WiFi USB annoncées « compatibles Linux » ne garantissent **pas** une compilation réussie sur Jetson.

### Défi n°2 : la compilation des pilotes tiers échoue souvent sur Jetson

Cas réel sur GitHub（avril 2025）：sous JetPack 6.2 (kernel 5.15.148-tegra), `make` et `dkms` du pilote RTL8812EU échouent tous les deux. L'analyse de la communauté a révélé que — **les patches du noyau NVIDIA de JetPack cassent l'ABI cfg80211**, empêchant la compilation correcte des pilotes WiFi tiers.

> Source：[GitHub issue #421 — RTL8812EU Driver Compilation Failed on Jetson Orin Nano](https://github.com/svpcom/wfb-ng/issues/421)

### Défi n°3 : une mise à jour de JetPack peut rendre votre clé inutilisable

Cas du forum NVIDIA（octobre 2024）：la RTL8188EUS fonctionnait correctement sous JetPack 5.1.x, mais après la mise à niveau vers JetPack 6, elle est devenue **totalement non reconnue**. La solution consiste à recompiler manuellement le pilote depuis GitHub — mais que se passera-t-il si une future version de JetPack modifie à nouveau les API du noyau ?

> Source：[Jetson Orin Nano — JetPack 6 ne prend pas en charge la RTL8188EUS](https://nvidia-jetson.piveral.com/jetson-orin-nano/jetpack-6-doesnt-support-rtl8188eus/)

### Leçon à retenir

> **Sur la plateforme Jetson, le seul choix véritablement fiable est d'utiliser une clé WiFi USB dont le pilote est intégré au noyau (in-kernel).**

Car NVIDIA est obligé de maintenir la compatibilité des pilotes intégrés au noyau — c'est la seule garantie que votre clé continuera de fonctionner après une mise à niveau de JetPack.

---

## Vue d'ensemble de la compatibilité des chipsets : tout comprendre en un tableau

Voici un récapitulatif de la compatibilité des chipsets des clés WiFi USB ALFA Network courantes avec le Jetson Orin :

| Chipset | Modèle ALFA | Type de pilote | Noyau minimum requis | Verdict Jetson Orin |
|------|-----------|----------|-----------------|------------------|
| **MT7612U** | **AWUS036ACM** | **In-kernel (mt76x2u)** | **4.19+** | ✅ Compatible, plug-and-play |
| RTL8812AU | AWUS036ACH | Out-of-tree（compilation requise） | Compilation manuelle requise | ⚠️ Envisageable mais compilation risquée |
| RTL8811AU | AWUS036ACS | Out-of-tree（compilation requise） | Compilation manuelle requise | ⚠️ Mêmes problèmes que RTL8812AU |
| RTL8812BU | AWUS036AX | Out-of-tree（compilation requise） | Compilation manuelle requise | ⚠️ Compilation requise, problèmes connus |
| MT7921AU | AWUS036AXM | In-kernel (mt7921u) | **5.18+** | ❌ K5.10/5.15 non satisfait |
| RTL8832CU | AWUS036AXER | Out-of-tree（compilation requise） | Compilation manuelle requise | ❌ Déconseillé, support ARM64 incertain |

Source des données：[morrownr/USB-WiFi — Tableau de support des chipsets](https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Chipsets.md)

---

## Recommandation principale : ALFA AWUS036ACM（MediaTek MT7612U）

### Aperçu des spécifications

| Élément | Détail |
|------|------|
| Chipset | MediaTek MT7612U / MT7612UN |
| Norme WiFi | 802.11ac (WiFi 5) double bande AC1200 |
| Débit maximal | 5 GHz : 867 Mbps / 2,4 GHz : 300 Mbps |
| Antennes | 2 × RP-SMA amovibles 5 dBi double bande |
| Interface | USB 3.0（connecteur USB-C） |
| Puissance d'émission | Puissance standard, adaptée à une connexion directe sur port USB |

**Page produit**：https://yupitek.com/en/products/alfa/awus036acm/

### Raison n°1 : la seule solution véritablement sans pilote

Le chipset MT7612U utilisé par l'AWUS036ACM dispose de son pilote `mt76x2u` intégré dans le noyau Linux principal depuis la **version 4.19（octobre 2018）**. L'AIB-NW01 tourne avec le noyau 5.10.x, donc :

**Branchez et ça fonctionne. Pas de compilation, pas de configuration.**

C'est crucial sur la plateforme Jetson — vous évitez totalement les trois défis mentionnés précédemment（noyau personnalisé, échecs de compilation, obsolescence après mise à jour）.

### Raison n°2 : validation sur plateforme ARM64

Un utilisateur GitHub a testé l'AWUS036ACM dans un environnement ARM64 + Kernel 5.10.198：

```
$ lsusb | grep MediaTek
ID 0e8d:7612 MediaTek Inc. MT7612U

$ dmesg | grep mt76
mt76x2u 1-1:1.0 wlx00c0ca9821a5: renamed from wlan0
```

**Prêt à l'emploi**, le module se nomme `mt76x2u`, aucune étape supplémentaire requise.

> Source：[GitHub issue #574 — AWUS036ACM on ARM64 K5.10](https://github.com/morrownr/USB-WiFi/issues/574)

### Raison n°3 : prise en charge complète des fonctionnalités professionnelles

Cette clé ne fait pas que se connecter à Internet, elle prend en charge un ensemble complet de fonctionnalités réseau sans fil professionnelles :

- Mode Monitor — pour le diagnostic et l'analyse réseau
- Injection de paquets (Packet injection) — pour les tests d'intrusion et la recherche
- Mode AP — permet de transformer l'AIB-NW01 en point d'accès WiFi（la bande 5 GHz peut nécessiter le paramètre de module `disable_usb_sg`）
- VIF (Virtual Interface) — permet d'exécuter simultanément les modes monitor et managed sur la même clé

### Raison n°4 : une flexibilité d'antenne inégalée

La conception à 2 antennes externes RP-SMA signifie que vous pouvez :

- Remplacer par des antennes à gain élevé（ex. 9 dBi）pour étendre la couverture
- Utiliser des antennes directionnelles pour concentrer le signal dans une direction spécifique
- Étendre les antennes à l'extérieur du boîtier métallique via des câbles d'extension（particulièrement important dans les scénarios d'armoire industrielle）

---

## Les cinq avantages concrets de l'AWUS036ACM

### Avantage n°1 : connexion immédiate, déploiement sans latence

Dès l'insertion, le système reconnaît l'interface `wlan0`（ou `wlx...`）. Trois commandes suffisent :

```bash
# Scanner les réseaux disponibles
sudo nmcli device wifi list

# Connexion
sudo nmcli device wifi connect "Votre_SSID" password "Votre_MotDePasse"
```

Pas de compilation, pas de redémarrage, pas d'installation de paquets.

### Avantage n°2 : contourner toutes les limitations des modules WiFi M.2

| Module WiFi M.2 | Clé WiFi USB (AWUS036ACM) |
|---------------|--------------------------|
| Nécessite le démontage | Branchement externe, sans démontage |
| Antennes fixées dans le boîtier | Antennes positionnables au meilleur emplacement |
| Remplacement difficile | Hot-plug, remplacement instantané |
| Limité à cette machine | Partageable entre appareils |

### Avantage n°3 : adapté à tous les scénarios de déploiement industriel

L'AWUS036ACM répond aux besoins des scénarios Edge AI typiques :

- **Lignes de production** — pas de port réseau filaire à proximité ? Branchez pour une connexion sans fil
- **Surveillance extérieure** — le WiFi est le seul canal de transmission des données
- **Déploiement temporaire** — en phase POC, sans vouloir démonter pour installer un module M.2
- **Véhicules mobiles** — AGV/AMR nécessitant une connexion sans fil stable

### Avantage n°4 : coût de maintenance à long terme le plus bas

Les avantages du pilote in-kernel sont très concrets :

- La clé continue de fonctionner après une mise à niveau de JetPack（NVIDIA maintient lui-même les pilotes intégrés au noyau）
- Pas de DKMS ni de compilation manuelle de pilotes à gérer
- Les mises à jour de sécurité du noyau ne sont pas bloquées
- Économie sur les coûts de maintenance et de support ultérieurs

### Avantage n°5 : couverture du signal optimisable selon les besoins

La conception à 2 antennes externes RP-SMA fait de cette clé une solution sans fil adaptable. Selon l'environnement de déploiement, vous pouvez :

- Remplacer par des antennes à gain élevé（ex. 9 dBi）pour étendre la couverture
- Utiliser des antennes directionnelles pour concentrer le signal
- Placer les antennes à l'extérieur du boîtier métallique via des câbles d'extension（scénarios d'armoire industrielle）
- Utiliser des antennes à base magnétique adhérent aux surfaces métalliques

---

## Étapes d'installation : seulement trois étapes

### Étape 1：Brancher

Branchez l'AWUS036ACM sur un port USB 3.0 Type-A de l'AIB-NW01.

### Étape 2：Vérifier que le pilote est chargé

```bash
lsusb | grep MediaTek
# Sortie attendue : ID 0e8d:7612 MediaTek Inc. MT7612U

dmesg | grep mt76
# Sortie attendue : mt76x2u 1-1:1.0 wlx...: renamed from wlan0
```

### Étape 3：Se connecter au WiFi

```bash
# Scanner les réseaux disponibles
sudo nmcli device wifi list

# Connexion
sudo nmcli device wifi connect "Votre_SSID" password "Votre_MotDePasse"

# Vérifier l'état de la connexion
ip addr show wlx...
```

Terminé. Votre Jetson Orin est connecté au réseau.

---

## Remarques et précisions honnêtes

### L'AWUS036ACM est WiFi 5（AC1200）

Ce n'est pas l'option la plus rapide du marché. L'AWUS036AXM（WiFi 6E, MT7921AU）est théoriquement plus rapide, mais elle est **inutilisable** sur l'AIB-NW01 avec le noyau 5.10（nécessite le noyau 5.18+）. Pour la majorité des besoins en bande passante des applications Edge AI（transfert de données, mise à jour de modèles, SSH distant）, l'AC1200 est largement suffisant.

### Preuves expérimentales sur ARM64

La validation du GitHub issue #574 a été réalisée sur un **Odroid M1**（ARM64 + Kernel 5.10）et non directement sur l'AIB-NW01. Les deux partagent la même architecture de noyau et la même pile de pilotes, nous sommes donc hautement confiants que les résultats sont identiques, mais nous recommandons tout de même aux utilisateurs de procéder à une vérification sur la machine réelle.

### Scénarios adaptés aux autres modèles

L'AWUS036ACH（RTL8812AU）et l'AWUS036AX（RTL8812BU）ne sont pas inutilisables pour autant, ils nécessitent simplement une compilation manuelle du pilote sur Jetson. Si vous avez de l'expérience en compilation et êtes prêt à maintenir le pilote, ces modèles méritent également d'être considérés.

---

## Conclusion : la solution la plus simple est souvent la meilleure

Revenons à la question initiale du client : quelle clé WiFi USB ALFA convient le mieux à l'AVALUE AIB-NW01 ?

La réponse est l'**ALFA AWUS036ACM**.

Non pas parce qu'elle est la plus rapide ou la moins chère — mais parce qu'elle est, sur une plateforme aussi spécifique que Jetson, **la seule solution qui fonctionne réellement dès le branchement**. Sur une plateforme où même la compilation de pilotes échoue régulièrement, les pilotes in-kernel sont la voie royale.

### Passez à l'action

- Voir les détails du produit：https://yupitek.com/en/products/alfa/awus036acm/
- Support technique：Yupitek fournit un support technique local à Taïwan, n'hésitez pas à nous contacter

### Pour aller plus loin

- [AWUS036ACH vs AWUS036ACM：comparaison complète des pilotes RTL8812AU et MT7612U](https://yupitek.com/en/blog/awus036ach-vs-awus036acm/)
- [Tableau de compatibilité Linux ALFA Network](https://docs.alfa.com.tw/Support/Compat/)
- [Liste officielle des modules WiFi validés par NVIDIA（AGX Orin）](https://forums.developer.nvidia.com/t/wi-fi-6-6e-7-modules-that-have-been-validated-with-agx-orin-devkits/313431)

---

> **Tags**：#JetsonOrin #EdgeAI #ALFANetwork #USBWiFi #AWUS036ACM #Yupitek
>
> **Auteur**：Yupitek Ltd — Distributeur agréé ALFA Network à Taïwan
>
> **Avertissement**：les données de recherche de cet article sont à jour jusqu'en mai 2026. La plateforme Jetson et le noyau Linux évoluent en continu, il est conseillé de vérifier les dernières versions de JetPack et la prise en charge des pilotes intégrés au noyau avant tout déploiement.
