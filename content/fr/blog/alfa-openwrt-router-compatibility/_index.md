---
title: "Carte réseau sans fil ALFA : prise en charge par OpenWrt ?"
date: 2026-09-03
draft: false
slug: "alfa-openwrt-router-compatibility"
tags:
  - "ALFA"
  - "OpenWrt"
  - "Router"
  - "kmod-mt76"
  - "AWUS036ACM"
  - "AWUS036ACH"
  - "Soft-AP"
categories:
  - "Guide Matériel"
description: "OpenWrt : meilleure compatibilité avec AWUS036ACM (MT7612U) et support varié pour Realtek et MediaTek."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Résumé du problème

Le client demande : « Peut-on utiliser la carte réseau USB ALFA série sur un routeur OpenWrt ? »

Conclusion rapide : OpenWrt est la plateforme des trois principaux systèmes d'exploitation tiers pour les routeurs (DD-WRT / OpenWrt / Tomato) qui offre le meilleur soutien aux cartes réseau USB WiFi ALFA. Les modèles de puces MediaTek (AWUS036ACM / ACHM / AXML / AXM) sont directement pris en charge par le kit officiel kmod-mt76 ; les modèles de puces Realtek (AWUS036ACH / ACS / EACS / AX / AXER) nécessitent l'utilisation de kits de pilotes out-of-tree maintenus par la communauté, leur disponibilité variant selon la version d'OpenWrt. Le modèle AWUS036ACM (MT7612U) est recommandé, ses pilotes sont matures, stables et prennent en charge l'écoute et l'injection.

Évaluation des modèles : ALFA propose 9 cartes réseau USB actuelles (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analyser les spécifications et les besoins du logiciel cible

### 2.1 Qu'est-ce que OpenWrt ?

OpenWrt est un système de firmware pour routeurs open source, hautement modulaire, utilisant le kernel Linux et le système de gestion de paquets opkg. Contrairement à DD-WRT ou Tomato, les pilotes de OpenWrt sont fournis sous forme de modules noyau (kmod) indépendants, ce qui permet aux utilisateurs d'installer des pilotes WiFi USB sans avoir à recompiler tout le firmware.

### 2.2 Le cadre de pilotes WiFi USB d'OpenWrt

La bibliothèque de paquets officielle d'OpenWrt contient les pilotes WiFi USB suivants :

| Paquet de pilote | Source | Chips / Modèles couverts | État de maintenance |
|---|---|---|---|
| kmod-mt76-usb + kmod-mt76x2u | Officiel in-kernel | MediaTek MT7612U (AWUS036ACM) | Actif, stable |
| kmod-mt76-usb + kmod-mt76x0u | Officiel in-kernel | MediaTek MT7610U (AWUS036ACHM) | Actif |
| kmod-mt7921u | Officiel in-kernel | MediaTek MT7921AUN (AWUS036AXML / AXM) | Disponible depuis la version 23.05+ |
| kmod-rtl8812au-ct | Communauté out-of-tree | Realtek RTL8812AU / RTL8811AU (AWUS036ACH / ACS) | Maintenu par la communauté, des crashs du kernel ont été signalés en 24.10 |
| kmod-rtl8821cu | Communauté out-of-tree | Realtek RTL8811CU (AWUS036EACS) | Maintenu par la communauté |
| kmod-rtw89 / kmod-rtl8852bu | En développement | Realtek RTL8832BU (AWUS036AX / AXER) | La prise en charge USB rtw89 est progressivement intégrée, nécessite un kernel plus récent |

### 2.3 Prérequis : Support du noyau USB

Avant d'installer les pilotes WiFi, il est nécessaire de s'assurer que OpenWrt a activé le support du noyau USB :

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

La plupart des versions modernes d'OpenWrt incluent déjà kmod-usb-core, mais usbutils (qui fournit la commande lsusb) doit être installé manuellement.

## 3. Analyse des spécifications et des puces des cartes réseau ALFA

Au 9 septembre 2026, la gamme de produits de cartes réseau USB sans fil actuels d'ALFA Network est la suivante (base : 9 modèles) :

| Modèle | Niveau Wi-Fi | Puce | Interface | Paquet de pilotes OpenWrt |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | kmod-mt7921u (23.05+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | kmod-mt7921u (23.05+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | kmod-rtw89 (en développement) / rtl8852bu personnalisé |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Comme ci-dessus |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | kmod-rtl8812au-ct (communauté) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | kmod-mt76x0u (officiel) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | kmod-mt76x2u (officiel)⭐ Recommandé |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | kmod-rtl8812au-ct (couverture) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | kmod-rtl8821cu (communauté) |

## 4. Modèles et SoC compatibles

### 4.1 Catégorie de recommandation

| Catégorie de recommandation | Modèle (SoC) | Description |
|---|---|---|
| ⭐ Fortement recommandé | AWUS036ACM (MT7612U) | Pilotes officiels matures et stables, supporte AP / STA / Monitor / Injection, le meilleur choix sur OpenWrt |
| ✅ Recommandé | AWUS036ACHM (MT7610U) | Pilotes officiels, double fréquence mais seulement 433Mbps, adapté aux scénarios à faible consommation d'énergie |
| ✅ Recommandé (nouvelle version) | AWUS036AXML / AXM (MT7921AUN) | Wi-Fi 6E, pilotes officiels, nécessite OpenWrt 23.05+ et kernel 5.15+ |
| ⚠️ Disponible mais à surveiller | AWUS036ACH (RTL8812AU) | Pilotes communautaires, la version 24.10 a des rapports de crash du kernel, recommandé d'utiliser 23.05 |
| ⚠️ Disponible mais à surveiller | AWUS036ACS (RTL8811AU) | Comme ci-dessus, couvert par le pilote 8812au |
| ⚠️ Disponible mais à surveiller | AWUS036EACS (RTL8811CU) | Pilotes communautaires, stabilité moyenne |
| ❌ Déconseillé | AWUS036AX / AXER (RTL8832BU) | Wi-Fi 6, le support rtw89 USB est en développement, la plupart des versions OpenWrt ne peuvent pas être utilisées directement |

### 4.2 Exigences matérielles du routeur

| Item | Exigences minimales | Exigences recommandées |
|---|---|---|
| Port USB | USB 2.0 (AWUS036ACHM / ACS / EACS) | USB 3.0 (AWUS036ACH / ACM / AX série) |
| Flash | 16MB (installation des pilotes + dépendances) | 32MB+ |
| RAM | 128MB | 256MB+ (mode AP + utilisateurs multiples) |
| Version OpenWrt | 21.02+ | 23.05.x (version stable) |

## 5. Nécessités environnementales

### 5.1 Environnement logiciel

- Version stable d'OpenWrt : 23.05.x (kernel 5.15) ou 24.10.x (kernel 6.6)
- Sources de paquets : dépôt officiel opkg (https://downloads.openwrt.org/releases/{version}/packages/{arch}/)
- Connexion réseau : le routeur doit être connecté à Internet pendant l'installation du pilote (via le port WAN)

### 5.2 Environnement matériel

- Routeur compatible OpenWrt avec un port USB 2.0 / 3.0
- Pour les modèles à haute puissance (AWUS036ACH), il est recommandé d'utiliser un hub USB 3.0 alimenté pour éviter une alimentation insuffisante du port USB du routeur
- Le modèle AWUS036AXML est en interface USB-C, veillez à ce que votre routeur dispose d'un port USB-C ou utilisez un adaptateur USB-C to USB-A

## 6. Détermination de la compatibilité

### Matrice de compatibilité ALFA modèles actuels × OpenWrt

| Modèle | Processeur | Mode de pilotage | Détection USB | STA Internet | Mode AP | Monitor | Version minimale | Évaluation globale |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | kmod-mt76x2u | ✅ | ✅ | ✅ | ✅ | 21.02+ | ⭐ Meilleure |
| AWUS036ACHM | MT7610U | kmod-mt76x0u | ✅ | ✅ | ✅ | ⚠️ Limitée | 21.02+ | ✅ Bonne |
| AWUS036AXML | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ Limitée | 23.05+ | ✅ Bonne |
| AWUS036AXM | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ Limitée | 23.05+ | ✅ Bonne |
| AWUS036ACH | RTL8812AU | kmod-rtl8812au-ct | ✅ | ✅ | ✅ | ⚠️ Limitée | 22.03+（24.10 avec crash） | ⚠️ Utilisable |
| AWUS036ACS | RTL8811AU | kmod-rtl8812au-ct | ✅ | ✅ | ⚠️ | ❌ | 22.03+ | ⚠️ Utilisable |
| AWUS036EACS | RTL8811CU | kmod-rtl8821cu | ✅ | ⚠️ | ❌ | ❌ | 23.05+ | ⚠️ Utilisable |
| AWUS036AX | RTL8832BU | rtw89（en développement） | ⚠️ | ❌ | ❌ | ❌ | Nécessite compilation personnalisée | ❌ Déconseillé |
| AWUS036AXER | RTL8832BU | rtw89（en développement） | ⚠️ | ❌ | ❌ | ❌ | Nécessite compilation personnalisée | ❌ Déconseillé |

Critères de détermination : Accessibilité des paquets kmod dans le dépôt officiel d'OpenWrt (23.05 / 24.10) + retours des utilisateurs du forum OpenWrt. Les pilotes pour les puces Realtek sont maintenus par la communauté, leur stabilité et intégrité fonctionnelle sont inférieures à celles de la série MediaTek mt76.

## 7. Détails étape par étape détaillés

### 7.1 Préparations initiales : Activer le support USB

**Étape 1 : Connexion SSH au routeur OpenWrt**

```bash
ssh root@192.168.1.1
```

**Étape 2 : Mise à jour des dépôts de paquets et installation du support USB**

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

**Étape 3 : Insérer la carte réseau ALFA et vérifier la détection USB**

```bash
lsusb
# Sortie prévue (AWUS036ACM / MT7612U) :
# Bus 002 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

### 7.2 Chemin A : Modèles de puces MediaTek (AWUS036ACM / ACHM / AXML / AXM)

Par exemple, avec l'AWUS036ACM (MT7612U) :

**Étape 1 : Installation des pilotes**

```bash
# AWUS036ACM (MT7612U)
opkg install kmod-mt76-usb kmod-mt76x2u

# AWUS036ACHM (MT7610U) — Utiliser
# opkg install kmod-mt76-usb kmod-mt76x0u

# AWUS036AXML / AXM (MT7921AUN) — Utiliser (nécessite 23.05+)
# opkg install kmod-mt7921u
```

**Étape 2 : Installation des outils de gestion sans fil**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**Étape 3 : Vérification de la création de l'interface réseau**

```bash
iw dev
# Sortie prévue : wlan0 ou wlan1
```

**Étape 4 : Scan des réseaux WiFi à proximité (validation des fonctionnalités)**

```bash
iw dev wlan0 scan | grep -E "SSID|signal"
```

**Étape 5 : Configuration en mode STA (se connecter à un AP existant)**

Éditer /etc/config/wireless :

```text
config wifi-device 'radio1'
       option type 'mac80211'
       option path 'platform/usb1/1-1/1-1:1.0'
       option channel 'auto'
       option htmode 'VHT80'

config wifi-iface 'wifinet2'
       option device 'radio1'
       option mode 'sta'
       option network 'wwan'
       option ssid 'Nom de ton WiFi'
       option encryption 'psk2'
       option key 'Mot de passe de ton WiFi'
```

**Étape 6 : Redémarrage du service réseau**

```bash
/etc/init.d/network restart
```

**Étape 7 : Configuration en mode AP (partage de la connexion)**

Éditer /etc/config/wireless, changez le mode en ap :

```text
config wifi-iface 'wifinet2'
   option device 'radio1'
   option mode 'ap'
   option network 'lan'
   option ssid 'ALFA-OpenWrt-AP'
   option encryption 'psk2'
   option key 'Mot de passe de ton hotspot'
```

**Étape 8 : Activation du mode écoute (pour les tests d'intrusion)**

```bash
opkg install aircrack-ng
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
iw dev wlan0 set channel 6
# Validation
iw dev wlan0 info
# type devrait afficher monitor
```

### 7.3 Chemin B : Modèles de puces Realtek (AWUS036ACH / ACS / EACS)

Par exemple, avec l'AWUS036ACH (RTL8812AU) :

**Étape 1 : Installation des pilotes communautaires**

```bash
opkg update
opkg install kmod-rtl8812au-ct

# AWUS036EACS (RTL8811CU) — Utiliser
# opkg install kmod-rtl8821cu
```

**Étape 2 : Installation des outils de gestion sans fil**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**Étape 3 : Vérification de l'interface**

```bash
iw dev
# Note : L'interface du pilote kmod-rtl8812au-ct peut être wlan0 ou wlan1
```

La configuration est la même que pour l'étape 7.2 (configuration en mode STA / AP).

**Étape 4 : Mode écoute**

```bash
# Le pilote kmod-rtl8812au-ct supporte le mode écoute
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
# La fonctionnalité d'injection de paquets est limitée, il est recommandé d'utiliser des puces mt76 pour les tests d'intrusion
```

**Étape 5 : Si vous rencontrez un crash du noyau (problème connu depuis la version 24.10)**

```bash
# Retournez à la version stable 23.05, ou utilisez un pilote personnalisé compilé
# Vérifiez les journaux de crash
logread | grep -i "panic\|crash\|rtl8812"
```

### 7.4 Chemin C : Modèles Wi-Fi 6 (AWUS036AX / AXER, RTL8832BU)

⚠️ Ce chemin nécessite une compilation personnalisée d'OpenWrt, pas recommandé pour les utilisateurs ordinaires.

**Étape 1 : Vérifiez si la version d'OpenWrt contient le support rtw89 USB**

```bash
opkg list | grep rtw89
# Si vous ne voyez pas de résultat, cela signifie que la version n'inclut pas
```

**Étape 2 : Si nécessaire, compilez l'image d'OpenWrt vous-même**

Ajoutez kmod-rtw89 et le firmware correspondant.

** 建议** : Pour les besoins de cartes réseau USB Wi-Fi 6 sur un routeur OpenWrt, l'AWUS036AXML (MT7921AUN) est actuellement le meilleur choix.

## 8. Erreurs Courantes et Solutions

| Symptômes | Causes Probables | Solutions |
|---|---|---|
| `lsusb` ne voit pas la carte réseau ALFA | Core USB non installé / Alimentation insuffisante | Vérifiez si kmod-usb-core, kmod-usb2 et kmod-usb3 sont installés ; utilisez un Hub USB avec alimentation |
| `lsusb` voit la carte mais `iw dev` n'a pas d'interface | Pilote non installé / Pilote incompatible | Installez le paquet kmod approprié ; vérifiez dmesg pour des erreurs de firmware manquant |
| `opkg install kmod-mt76x2u` affiche « kernel version mismatch » | Version OpenWrt et version de la bibliothèque de packages non compatibles | Exécutez `opkg update` puis réessayez ; vérifiez que la version du noyau et l'architecture de la bibliothèque de packages sont compatibles |
| Échec du démarrage du mode AP (erreur hostapd) | Pilote non compatible avec le mode AP / Configuration de canal incorrecte | Vérifiez si le chip prend en charge le mode AP ; essayez de fixer un canal (comme 6 ou 149) ; vérifiez le domaine réglementaire |
| Impossible d'injecter des paquets en mode surveillance | Pilote non compatible avec l'insertion de paquets / Conflit de canal | La série MediaTek mt76 est recommandée ; la fonction d'insertion de paquets sur Realtek 8812au-ct est limitée ; vérifiez `airmon-ng check kill` |
| AWUS036ACH se déconnecte lors de l'utilisation à haute puissance | Alimentation USB insuffisante | Utilisez un Hub USB avec alimentation ; dans /etc/config/wireless, réglez `option txpower '20'` pour réduire la puissance |
| Kernel panic après l'installation de `rtl8812au-ct` sur 24.10 | Problème de compatibilité connu du pilote | Retournez à la version stable 23.05.x ; ou suivez les issues GitHub en attendant la correction |
| MT7921 (AXML/AXM) ne peut pas utiliser la bande 6GHz | Limitation du domaine réglementaire / Version du kernel | Nécessite un kernel 5.19+ et la configuration correcte de la région réglementaire Wi-Fi 6E ; la prise en charge de la bande 6GHz dans OpenWrt 23.05 est encore en test |

## 9. Limites connues

- Le pilote de puce Realtek pour la maintenance de la communauté : kmod-rtl8812au-ct, kmod-rtl8821cu n'est pas maintenu par l'OpenWrt officiel, la stabilité et le calendrier des mises à jour ne peuvent pas être garanties
- La version 24.10 de rtl8812au-ct a des rapports de crash du kernel : il est recommandé aux utilisateurs de puces Realtek de rester à 23.05.x
- Le soutien à Wi-Fi 6 (RTL8832BU) est insuffisant : le pilote USB rtw89 est encore en développement, la plupart des versions OpenWrt ne peuvent pas utiliser directement AWUS036AX / AXER
- La performance en mode AP est limitée : lorsque le WiFi USB fait office d'AP, la capacité de transmission est inférieure à celle du WiFi intégré au routeur (largeur de bande du port USB + overhead du pilote)
- Les différences de fonctionnalités de surveillance / injection : la série MediaTek mt76 est la plus complète ; les fonctions d'injection des puces Realtek sont limitées, et ne sont pas adaptées aux tests de pénétration professionnels
- Ressources matérielles du routeur : sur les routeurs de basse gamme (16MB Flash / 128MB RAM), l'installation du pilote peut entraîner un espace insuffisant, affectant d'autres fonctionnalités
- Interférences de l'USB 3.0 : les appareils USB 3.0 peuvent interférer avec le WiFi 2.4GHz, il est recommandé d'utiliser un port USB 2.0 ou un Hub USB bien isolé
- Utilisation simultanée de plusieurs cartes réseau : en utilisant simultanément le WiFi intégré au routeur et le WiFi USB, des conflits de canal ou des conflits de ressources peuvent survenir
- ⚠️ **Le mainteneur du pilote RTL8832BU (AWUS036AX/AXER) a recommandé publiquement d'éviter son utilisation** : comme indiqué à la section 4.1, la mention «❌ Non recommandé» n'est pas seulement due au fait que rtw89 USB est encore en développement, mais aussi parce que le mainteneur morrownr a déclaré publiquement que cette série de puces est «très mauvais pilote, suspectant que la puce elle-même a des problèmes», recommandant aux utilisateurs Linux d'éviter cela pour le moment (voir la section 10 pour la source)
- **Il faut clarifier les termes de seuil de version du kernel** : la mention dans la section 4.1 «MT7921AUN nécessite OpenWrt 23.05+ et kernel 5.15+» peut être trompeuse - le pilote mt7921u nécessite en réalité **kernel 5.19+** sur Linux desktop (voir les propos du mainteneur du pilote), mais les kits officiels OpenWrt sont souvent pré-enregistrés via le mécanisme de backport, donc OpenWrt 23.05 (même s'il est marqué kernel 5.15) a toujours des utilisateurs qui signalent une installation réussie de kmod-mt7921u. **Veuillez vous référer à la version du client `opkg list` pour une vérification réelle, et ne pas déduire la version du kernel**.

Conditions de réfutation : si les mises à jour ultérieures du kit OpenWrt corrigent le problème de crash du kernel de rtl8812au-ct version 24.10, les recommandations pour AWUS036ACH dans les sections 4.1 et 6 peuvent être mise à jour de «maintenir 23.05»; si le soutien USB rtw89 est officiellement intégré dans le kit OpenWrt, la décision de ne pas recommander AWUS036AX / AXER doit être réexaminée; si une déclaration complète de soutien à la fréquence 6GHz pour MT7921 est publiée par l'officiel, la description des limitations pour AXML / AXM doit être mise à jour.

## 10. Sources de référence URL

| Source | Description | URL | État de vérification | Date de vérification |
|---|---|---|---|---|
| Documentation officielle OpenWrt | Entrée des documents officiels OpenWrt (réglage sans fil / gestion des paquets) | https://openwrt.org/docs/start | ✅ Vérifié | 2026-09-03 |
| Forum officiel OpenWrt | Entrée de discussion sur les pilotes WiFi USB | https://forum.openwrt.org/ | ✅ Vérifié | 2026-09-03 |
| morrownr/8812au GitHub | Pilote Linux RTL8812AU en amont | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |
| ALFA Network Catalogue de produits (Yupitek) | Spécifications des produits actuels d'ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Vérifié | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | Déclaration officielle du mainteneur de pilotes : recommandation d'éviter les puces rtl8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Vérifié | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko nécessite le kernel 5.19+ pour apparaître dans le noyau (dites du mainteneur de pilotes) | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ Vérifié | 2026-09-03 |
| Forum officiel OpenWrt — Meilleur dongle USB WiFi pour Raspberry Pi 4B | Rapports des utilisateurs sur l'installation réussie de kmod-mt7921u avec OpenWrt 23.05.0 | https://forum.openwrt.org/t/best-usb-wifi-dongle-for-raspberry-pi-4b/160103 | ✅ Vérifié | 2026-09-03 |

Articles associés : [Est-ce que la carte réseau sans fil ALFA est compatible avec DD-WRT](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Déclaration d'exonération de responsabilité : La détermination de la compatibilité de cet article est basée sur la bibliothèque de paquets officielle OpenWrt 23.05.x / 24.10.x. La disponibilité des paquets peut varier en fonction des architectures de routeurs (ath79 / ramips / mvebu / x86, etc.). Les pilotes pour les puces Realtek sont maintenus par la communauté, et leur stabilité peut varier selon les versions. Il est recommandé de choisir les modèles de puces MediaTek (AWUS036ACM en premier) comme choix prioritaire pour le USB WiFi OpenWrt.
