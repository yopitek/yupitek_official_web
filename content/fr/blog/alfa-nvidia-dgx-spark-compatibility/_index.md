---
title: "Carte sans fil ALFA : Prise en charge du NVIDIA DGX Spark (GB10)"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-dgx-spark-compatibility"
tags:
  - "ALFA"
  - "NVIDIA"
  - "DGX-Spark"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "Guide Matériel"
description: "DGX Spark compatible with ALFA cards, in-kernel drivers for MediaTek, out-of-tree for Realtek, USB-C to USB-A adapter required."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Résumé du problème

Client demande : « L'ALFA série USB carte réseau sans fil peut-elle être utilisée sur le supercalculateur personnel AI NVIDIA DGX Spark (GB10 Grace Blackwell) ? »

Conclusion rapide : DGX Spark exécute NVIDIA DGX OS (basé sur Ubuntu, kernel 6.x), la compatibilité de la carte réseau ALFA est la même que pour un système de bureau moderne Linux. Les modèles de puces MediaTek (AWUS036ACM / ACHM / AXML / AXM) utilisent le pilote in-kernel, prêt à l'emploi ; les modèles de puces Realtek (AWUS036ACH / ACS / EACS / AX / AXER) nécessitent la compilation d'un pilote out-of-tree (architecture ARM64 / aarch64). Attention : tous les ports USB de DGX Spark sont de type USB Type-C, tandis que les cartes réseau ALFA sont de type USB Type-A, il est nécessaire d'utiliser un adaptateur USB-C to USB-A ou un câble de transmission.

Éléments à vérifier : ALFA 9 cartes réseau USB actuelles (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analyse des spécifications matérielles cibles

### 2.1 Spécifications matérielles de NVIDIA DGX Spark

| Élément | Spécification |
|---|---|
| Nom du produit | NVIDIA DGX Spark |
| Processeur central | NVIDIA GB10 Grace Blackwell Superchip |
| CPU | 20-coeurs Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Architecture Blackwell, 6144 cœurs CUDA, cinquième génération Tensor Core, quatrième génération RT Core |
| Performance AI | Jusqu'à 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| Mémoire système | 128GB LPDDR5x mémoire unifiée (256-bit, 273 GB/s) |
| Stockage | Jusqu'à 4TB NVMe M.2 SSD (cryptage intégré) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (20Gbps), dont 1 prend en charge l'entrée PD (180W EPR PD3.1) |
| Sortie vidéo | 1× HDMI 2.1a |
| Réseau câblé | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (200G QSFP) |
| Réseau sans fil | Wi-Fi 7 (intégéré) + Bluetooth 5.4 |
| Système d'exploitation | NVIDIA DGX OS (basé sur Ubuntu Linux, kernel 6.x) |
| Architecture | aarch64 (ARM64) |
| Dimensions | 150 × 150 × 50.5 mm (1.13L) |
| Poids | Environ 1.2 kg |
| Alimentation | Alimentation USB-C de 240W |

### 2.2 Environnement logiciel : NVIDIA DGX OS

| Élément | Description |
|---|---|
| Base | Ubuntu Linux (personnalisé par NVIDIA) |
| Kernel | Linux 6.x (version spécifique suivant la mise à jour de DGX OS) |
| Architecture | aarch64 (ARM64) |
| Logiciels préinstallés | Stack de logiciels AI NVIDIA (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Gestion des paquets | apt (système Debian/Ubuntu) |
| Cadre de pilotes | Architecture de pilotes kernel Linux standard (cfg80211 / mac80211) |

### 2.3 Caractéristiques clés : kernel moderne + ARM64

L'environnement logiciel de DGX Spark a deux impacts clés sur la compatibilité avec les cartes ALFA :

- Kernel 6.x (moderne) : Tous les pilotes WiFi entrés dans le mainline peuvent être utilisés directement, y compris mt76 (MT7612U / MT7610U) et mt7921u (MT7921AUN). Cela forme un contraste frappant avec le kernel 4.9 de Jetson Nano.
- Architecture ARM64 (aarch64) : Les pilotes out-of-tree de Realtek (8812au / 8821cu / rtl8852bu) doivent être compilés sur ARM64. Les上游 de ces pilotes (morrownr) supportent déjà la compilation ARM64, mais il faut vérifier que CONFIG_PLATFORM_ARM64 = y est configuré dans Makefile.

### 2.4 Besoins en convertisseurs USB Type-C

Les 4 ports USB de DGX Spark sont de type Type-C, tandis que la gamme complète des cartes ALFA (sauf AXML pour USB-C) utilise une interface USB Type-A :

| Modèle | Spécification de l'interface | Besoin de convertisseur |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ Pas besoin de convertisseur (peut être inséré directement) |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ Besoin de USB-C to USB-A |
| AWUS036AX | USB Type-A / USB 3.2 | ✅ Besoin de convertisseur |
| AWUS036AXER | USB Type-A / USB 3.2 | ✅ Besoin de convertisseur |
| AWUS036ACH | USB Type-A / USB 3.0 | ✅ Besoin de convertisseur |
| AWUS036ACHM | USB Type-A / USB 2.0 | ✅ Besoin de convertisseur |
| AWUS036ACM | USB Type-A / USB 3.0 | ✅ Besoin de convertisseur |
| AWUS036ACS | USB Type-A / USB 2.0 | ✅ Besoin de convertisseur |
| AWUS036EACS | USB Type-A / USB 2.0 | ✅ Besoin de convertisseur |

Conseil : Utilisez un convertisseur ou un câble USB-C to USB-A supportant USB 3.2 Gen 2×2 (20Gbps) pour assurer que les modèles AWUS036ACH / ACM / AX peuvent fonctionner à pleine vitesse.

## 3. Analyse des spécifications et des puces des cartes réseau ALFA

Au 9 septembre 2026, la gamme de produits de cartes réseau USB sans fil actuels d'ALFA Network est la suivante (base : 9 modèles) :

| Modèle | Niveau Wi-Fi | Puce | Interface | État du pilote Linux |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel (mt7921u, kernel 5.19+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel (mt7921u) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 (kernel 5.16+, support USB en cours d'intégration) ou out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Comme ci-dessus |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree (morrownr/8812au, nécessite une compilation ARM64) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel (mt76x2u)⭐ Recommandé |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree (8812au couvre) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree (morrownr/8821cu) |

## 4. Modèles et SoC compatibles

### 4.1 Catégorie recommandée

| Catégorie recommandée | Modèle (SoC) | Description |
|---|---|---|
| ⭐ Fortement recommandé | AWUS036ACM (MT7612U) | Pilote in-kernel, prêt à l'emploi, AC1200 double bande, supporte AP / Monitor / Injection |
| ✅ Recommandé | AWUS036ACHM (MT7610U) | Pilote in-kernel, faible consommation d'énergie, AC433 double bande |
| ✅ Recommandé (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | Pilote in-kernel, Wi-Fi 6E, AXML est directement insérable en USB-C |
| ⚠️ Disponible mais nécessite la compilation | AWUS036ACH (RTL8812AU) | Nécessite la compilation de morrownr/8812au (ARM64), fonctionnalités complètes après compilation (y compris Monitor / Injection) |
| ⚠️ Disponible mais nécessite la compilation | AWUS036ACS (RTL8811AU) | Couvert par le pilote 8812au |
| ⚠️ Disponible mais nécessite la compilation | AWUS036EACS (RTL8811CU) | Nécessite la compilation de morrownr/8821cu (ARM64) |
| ⚠️ Disponible mais à utiliser avec précaution | AWUS036AX / AXER (RTL8832BU) | Le rtw89 du kernel 6.x pourrait déjà le prendre en charge USB ; sans compilation out-of-tree |

### 4.2 Suggestions de scénarios d'utilisation

| Scénario d'utilisation | Modèle recommandé | Description |
|---|---|---|
| Internet sans fil (le plus simple) | AWUS036ACM / ACHM | Pilote in-kernel, sans compilation, prêt à l'emploi |
| Tests de pénétration / Surveillance / Injection sans fil | AWUS036ACH ou AWUS036ACM | Les deux supportent Monitor + Injection ; ACH nécessite la compilation, ACM prêt à l'emploi |
| Wi-Fi 6E / Fréquence 6GHz | AWUS036AXML / AXM | Pilote in-kernel MT7921AUN, support complet du kernel 6.x |
| AWUS036ACH déjà en possession | AWUS036ACH | Compilation du pilote ARM64 nécessaire, fonctionnalités complètes |
| Pas de Wi-Fi externe nécessaire (utilisation intégrée) | — | DGX Spark intègre déjà Wi-Fi 7 + Bluetooth 5.4, l'utilisation quotidienne n'a pas besoin de carte réseau ALFA externe |
| Principal besoin : Tests de pénétration (Surveillance/Injection), besoins spécifiques de SoC ou Wi-Fi intégré insuffisant | — | DGX Spark intègre déjà Wi-Fi 7 + Bluetooth 5.4, l'utilisation quotidienne n'a pas besoin de carte réseau ALFA externe. Les besoins principaux de l'ALFA externe sont : Tests de pénétration (Surveillance/Injection), besoins spécifiques de SoC ou Wi-Fi intégré insuffisant.

## 5. Besoins Environnementaux

### 5.1 Besoins Hardware

| Élément | Besoin |
|---|---|
| Adaptateur USB | Adaptateur USB-C vers USB-A ou câble de transmission (sauf pour AXML) |
| Alimentation | Alimentation d'origine DGX Spark de 240W USB-C (alimentation suffisante via le port USB) |
| Refroidissement | Refroidissement d'origine suffisant (le USB WiFi ne会增加系统负载) |

### 5.2 Besoins Logiciels

| Élément | Besoin |
|---|---|
| Version DGX OS | Toute version en service (kernel 6.x) |
| Outils de compilation (nécessaire pour le chip Realtek) | build-essential, git, bc, dkms |
| Outils de gestion sans fil | iw, wpa_supplicant, network-manager (préinstallé sur DGX OS) |
| Réseau | Réseau câblé (10GbE) ou Wi-Fi 7 intégré pendant la compilation du pilote |

## 6. Détermination de la compatibilité

### Matrice de compatibilité ALFA modèles actuels × NVIDIA DGX Spark（GB10）

| Modèle | Processeur | Mode de pilotage | Détecteur USB | STA Internet | Mode AP | Moniteur | Difficulté d'installation | Évaluation globale |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel（mt76x2u） | ✅ | ✅ | ✅ | ✅ | Sans installation | ⭐ Meilleur |
| AWUS036ACHM | MT7610U | in-kernel（mt76x0u） | ✅ | ✅ | ✅ | ⚠️ Limité | Sans installation | ✅ Bon |
| AWUS036AXML | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ Limité | Sans installation | ✅ Bon |
| AWUS036AXM | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ Limité | Sans installation | ✅ Bon |
| AWUS036ACH | RTL8812AU | out-of-tree（8812au） | ✅ | ✅ | ✅ | ✅ | Moyen（compilation） | ⚠️ Disponible |
| AWUS036ACS | RTL8811AU | out-of-tree（8812au） | ✅ | ✅ | ⚠️ | ❌ | Moyen（compilation） | ⚠️ Disponible |
| AWUS036EACS | RTL8811CU | out-of-tree（8821cu） | ✅ | ⚠️ | ❌ | ❌ | Moyen（compilation） | ⚠️ Disponible |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Moyen-Haut | ⚠️ Disponible |
| AWUS036AXER | RTL8832BU | Comme ci-dessus | ✅ | ⚠️ | ⚠️ | ❌ | Moyen-Haut | ⚠️ Disponible |

Critère de détermination : Disponibilité des pilotes mainline pour le kernel DGX OS 6.x + prise en charge ARM64 du pilote morrownr. Les puces MediaTek sont prêtes à l'emploi sur le kernel 6.x dès l'ouverture de la boîte. Les puces Realtek nécessitent la compilation de pilotes out-of-tree, mais la compilation ARM64 est déjà prise en charge par l'upstream.

## 7. Détails ultra détaillés des étapes à suivre

### 7.1 Préparations initiales

**Étape 1 : Démarrage et connexion à DGX Spark** (par SSH ou en connectant directement le clavier et l'écran)

```bash
ssh username@<dgx-spark-ip>
```

**Étape 2 : Vérification de la structure du système et de la version du kernel**

```bash
uname -m
# Attendu : aarch64
uname -r
# Attendu : 6.x.x (kernel DGX OS)
```

**Étape 3 : (Nécessaire pour les puces Realtek) Installation des outils de compilation**

```bash
sudo apt update
sudo apt install -y build-essential git bc dkms
```

### 7.2 Chemin A : Modèles de puces MediaTek (AWUS036ACM / ACHM / AXML / AXM) — Prêt à l'emploi

**Étape 1 : Insérer la carte réseau**

Utilisez un adaptateur USB-C vers USB-A (AXML peut être inséré directement dans le port USB-C), et insérez la carte réseau ALFA dans un port USB de DGX Spark.

**Étape 2 : Vérification de la détection de la carte réseau**

```bash
lsusb
# Sortie attendue (AWUS036ACM / MT7612U) :
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Étape 3 : Vérification de la création automatique de l'interface réseau**

```bash
ip link show
# Sortie attendue : wlan0 ou wlp... (pilotage automatique du pilote in-kernel)
```

**Étape 4 : Scan du réseau WiFi**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**Étape 5 : Connexion au WiFi (via NetworkManager**)

```bash
nmcli dev wifi list
nmcli dev wifi connect "Nom de votre WiFi" password "Mot de passe de votre WiFi"
```

**Étape 6 : (Optionnel) Activation du mode écoute**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info
```

### 7.3 Chemin B : Modèles de puces Realtek (AWUS036ACH / ACS / EACS) — Nécessite la compilation

Prenez AWUS036ACH (RTL8812AU) comme exemple :

**Étape 1 : Téléchargement du code source du pilote**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**Étape 2 : Vérification des options de compilation ARM64**

Éditez Makefile et vérifiez que `CONFIG_PLATFORM_ARM64 = y` (la plupart des versions récentes détectent automatiquement aarch64).

**Étape 3 : Compilation et installation**

```bash
make
sudo make install
sudo modprobe 8812au
```

**Étape 4 : Insérer la carte réseau (via un adaptateur USB-C vers USB-A), vérifier l'interface**

```bash
ip link show
# Sortie attendue : wlan0
```

**Étape 5 : Mode de connexion identique à l'étape 5 de 7.2 (via nmcli**)

**Étape 6 : (Optionnel) Mode écoute et injection**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

### 7.4 Chemin C : Modèles Wi-Fi 6 (AWUS036AX / AXER, RTL8832BU)

**Étape 1 : Vérifiez si le kernel a déjà la prise en charge USB rtw89**

```bash
# Vérifiez après l'insertion de la carte réseau
lsusb
dmesg | grep -i "rtw89\|rtl8852\|8832"
ip link show
# Si wlan0 apparaît automatiquement, cela signifie que le rtw89 du kernel 6.x est pris en charge, vous pouvez l'utiliser directement
```

**Étape 2 : Si le kernel n'est pas pris en charge automatiquement, compilez le pilote out-of-tree**

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
# Vérifiez que CONFIG_PLATFORM_ARM64 = y
make
sudo make install
sudo modprobe rtl8852bu
```

## 8. Erreurs Courantes et Solutions

| Symptômes | Causes Probables | Solutions |
|---|---|---|
| `lsusb` ne voit pas la carte réseau ALFA | Adaptateur USB-C défectueux / mauvais contact | Changer l'adaptateur USB-C to USB-A ; vérifier que l'adaptateur prend en charge la transmission de données (pas seulement la charge) ; essayer un autre port USB-C |
| Le processeur MediaTek inséré n'a pas d'interface wlan | Module noyau non chargé automatiquement / firmware manquant | Charger manuellement : `sudo modprobe mt76x2u` ; vérifier `dmesg | grep mt76` ; installer le firmware : `sudo apt install linux-firmware` |
| Le pilote Realtek renvoie des erreurs de make : `aarch64-linux-gnu-gcc: not found` | Configuration de la compilation croisée incorrecte | Confirmer que la compilation est native sur DGX Spark (pas croisée) ; ne pas configurer CROSS_COMPILE dans Makefile |
| `modprobe 8812au` renvoie "Operation not permitted" | Secure Boot / signature du module | DGX Spark désactive par défaut Secure Boot ; si activé, signer le module ou désactiver Secure Boot |
| Connexion WiFi instable / lente | L'adaptateur USB-C ne prend en charge que USB 2.0 | Changer un adaptateur prenant en charge USB 3.2 Gen 2×2 ; vérifier que l'adaptateur est marqué "Data" et non "Charge Only" |
| Le Wi-Fi intégré et l'ALFA sont en conflit | Conflit de deux interfaces sans fil | Désactiver le Wi-Fi intégré : `sudo nmcli radio wifi off` ou désactiver dans BIOS/UEFI ; ou configurer l'ordre de priorité des routes |
| Le 6GHz (Wi-Fi 6E) ne peut pas être utilisé | Limite de domaine réglementaire | Définir le domaine réglementaire : `sudo iw reg set US` (6GHz ouverts aux États-Unis) ; vérifier que le firmware du AWUS036AXML/AXM prend en charge le 6GHz |
| Échec du démarrage du mode AP | Conflit entre NetworkManager et hostapd | Se référer au guide Yupitek ALFA Soft AP ; désactiver NetworkManager pour gérer cette interface et configurer manuellement hostapd |
| La carte réseau disparaît après la mise en veille | Arrêt automatique USB | Désactiver l'arrêt automatique USB : `echo 'options usbcore autosuspend=-1' | sudo tee /etc/modprobe.d/usb.conf` |

## 9. Limites connues

- **Nécessité de convertisseur USB Type-C** : À l'exception de AXML, toutes les cartes réseau ALFA nécessitent un adaptateur USB-C to USB-A. La qualité de l'adaptateur peut influencer les performances et la stabilité.
- **Nécessité de compilation manuelle pour les puces Realtek** : RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU ne sont pas intégrés dans le mainline, nécessitant une compilation out-of-tree sur ARM64.
- **Possibilité de conflit avec Wi-Fi externe** : DGX Spark intègre déjà Wi-Fi 7, et l'utilisation simultanée de Wi-Fi intégré et externe peut entraîner des conflits de route ou de ressources.
- **Configuration manuelle du mode AP** : DGX OS est configuré par défaut pour un environnement de développement, le mode热点 AP nécessite une installation et une configuration manuelle de hostapd / dnsmasq.
- **Restrictions réglementaires pour la bande 6GHz** : La disponibilité de la bande 6GHz pour Wi-Fi 6E dépend des paramètres réglementaires de la zone, la situation d'ouverture de la bande 6GHz à Taïwan doit être confirmée en fonction des réglementations les plus récentes.
- **Mise à jour des pilotes dépendante de l'upstream** : Les pilotes out-of-tree pour Realtek sont maintenus par la communauté (morrownr), une mise à jour du kernel DGX OS peut nécessiter une recompilation.
- **Différences dans les fonctionnalités de pénétration de test** : Les fonctionnalités d'injection de la série MediaTek mt76 ont été améliorées sur le kernel 6.x, mais RTL8812au reste le choix traditionnel de la communauté de test de pénétration.
- **Fonctionnalités Bluetooth** : La fonction Bluetooth 5.2 de AWUS036AXM n'a pas été largement vérifiée sur DGX OS (DGX Spark intègre déjà BT 5.4).
- ⚠️ **RTL8832BU (AWUS036AX/AXER) : le mainteneur de pilotes recommande d'éviter son utilisation** : Le mainteneur morrownr a déclaré officiellement que la série rtl8852/32au est "très mauvais pilote, soupçonnant que le chip en lui-même a des problèmes", recommandant aux utilisateurs Linux d'éviter son utilisation pour le moment (voir la section 10 pour la source). Les évaluations "⚠️ Utilisable mais à noter" des modèles dans les sections 4 et 6 devraient être comprises comme une concurrence d'industrie qui ne recommande pas, et non pas simplement un problème de difficulté d'installation.
- **Information sur le RTL8812AU "out-of-tree" datant de début 2026** ; En réalité, le pilote in-kernel compatible avec la norme mac80211 de ce chip a été intégré dans le kernel 6.13 et est devenu mature à partir de la version 6.14 (annonce officielle de morrownr). Si DGX OS utilise un noyau 6.14+, AWUS036ACH pourrait être utilisable sans compilation, il est recommandé aux services client de demander à leurs clients de rapporter `uname -r` pour confirmation avant de répondre.

Conditions de contestation : Si la mise à jour de DGX OS entraîne des changements dans la version du kernel ou le pilote du contrôleur USB, ou si le pilote morrownr cesse de maintenir la branche ARM64, la matrice de compatibilité de la section 6 devra être réexaminée ; si le support USB rtw89 est intégré de manière complète dans le kernel 6.x, l'évaluation de AWUS036AX / AXER peut être mise à niveau de "utilisable mais à noter".

## 10. Sources de référence URL

| Source | Description | URL | État de vérification | Date de vérification |
|---|---|---|---|---|
| Page officielle NVIDIA DGX Spark | Spécifications et plateformes de DGX Spark | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Vérifié | 2026-09-03 |
| Documents NVIDIA DGX | Architecture du système d'exploitation DGX et version du kernel | https://docs.nvidia.com/dgx/dgx-spark | ✅ Vérifié | 2026-09-03 |
| morrownr/8812au GitHub | Pilotes Linux RTL8812AU (prise en charge ARM64) | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |
| morrownr/8821cu GitHub | Pilotes Linux RTL8811CU | https://github.com/morrownr/8821cu-20210916 | ✅ Vérifié | 2026-09-03 |
| morrownr/rtl8852bu GitHub | Pilotes Linux RTL8832BU | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Vérifié | 2026-09-03 |
| Documents du pilote mt76 du kernel Linux | Documentation des pilotes MediaTek mt76 / mt7921 mainline (versions de kernel de démarrage prises en charge pour chaque puce) | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ Vérifié | 2026-09-03 |
| Guide Linux ALFA Soft AP WiFi Hotspot (Yupitek) | Guide de configuration en mode AP pour ALFA sous Linux | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Vérifié | 2026-09-03 |
| Vue d'ensemble des produits ALFA Network (Yupitek) | Spécifications des produits actuels d'ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Vérifié | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | Déclaration officielle du responsable du pilote : recommandation d'éviter les puces rtl8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Vérifié | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | Dernières annonces sur l'état du pilote RTL8812AU (intégration dans la branche principale du kernel 6.13, maturité de la qualité pour le kernel 6.14) | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |

Articles associés : [Est-ce que la carte réseau sans fil ALFA est compatible avec MSI EdgeXpert ?](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec ASUS Ascent GX10 ?](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec ALTOS BrainSphere GB10 F1 ?](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec GIGABYTE AI TOP ATOM ?](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec NVIDIA Jetson Nano ?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Déclaration de non-responsabilité : La détermination de la compatibilité de cet article se fait sur la base de NVIDIA DGX OS (kernel 6.x, aarch64). Les pilotes de puces MediaTek sont pour Linux mainline, avec une haute stabilité ; les pilotes de puces Realtek sont maintenus par la communauté (morrownr), et leur stabilité réelle peut varier en fonction de la version. DGX Spark est prévu avec Wi-Fi 7, et les cartes réseau ALFA externes sont principalement utilisées pour des tests de pénétration ou des besoins spécifiques de puces. La qualité du convertisseur USB-C peut直接影响 l'expérience d'utilisation, il est recommandé de choisir un convertisseur avec une marque et marqué USB 3.2 Gen 2×2.
