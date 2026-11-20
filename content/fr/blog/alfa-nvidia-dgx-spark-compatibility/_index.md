---
title: "Les cartes Wi-Fi ALFA sont-elles compatibles avec le NVIDIA DGX Spark (GB10) ?"
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
description: "Cartes USB ALFA sur NVIDIA DGX Spark (GB10) : 9 modèles testés sur ASUS GX10 en kernel 6.17, pilotes intégrés sans DKMS ; injection en échec sur AXM/AXML."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Article mis à jour d'après nos tests sur GX10 de novembre 2026 : sur l'ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), les 9 cartes réseau ALFA actuelles utilisent toutes les pilotes intégrés au kernel et fonctionnent dès le branchement, sans DKMS. Données complètes : [Tableau des tests ARM64 des 9 cartes réseau ALFA](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Tests effectués uniquement sur le GX10 ; les autres machines GB10 n'ont pas été testées une par une.

## 1. Résumé du problème

Question d'un client : « Les cartes réseau sans fil USB de la gamme ALFA peuvent-elles être utilisées sur le supercalculateur IA personnel NVIDIA DGX Spark (GB10 Grace Blackwell) ? »

Conclusion rapide : le DGX Spark exécute NVIDIA DGX OS (basé sur Ubuntu, kernel 6.x). Nous avons testé sur l'ASUS GX10, qui repose sur la même plateforme GB10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), les 9 cartes réseau USB ALFA actuelles : toutes utilisent les pilotes intégrés au kernel et fonctionnent dès le branchement, sans compilation ni DKMS. Le DGX Spark utilise la même puce GB10 et la même famille de kernels NVIDIA ; le comportement attendu est identique, mais les tests ont été effectués uniquement sur le GX10 et le DGX Spark n'a pas été testé individuellement. Différences fonctionnelles : les modèles MediaTek MT7921 (AWUS036AXM / AXML) échouent à l'injection de paquets sur le kernel 6.17 d'origine, tandis que les modes monitor, AP et WPA3 fonctionnent ; pour les 7 autres modèles, le mode monitor et l'injection ont été validés en test. La version minimale du kernel à partir de laquelle chaque pilote est intégré à la branche principale diffère selon la carte (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17) ; seuls les kernels antérieurs à cette version nécessitent les pilotes DKMS de la communauté. Attention : tous les ports USB du DGX Spark sont de type USB Type-C, tandis que les cartes réseau ALFA sont en USB Type-A ; il est nécessaire d'utiliser un adaptateur ou un câble USB-C vers USB-A.

Modèles évalués : les 9 cartes réseau USB ALFA actuelles (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

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
| Réseau sans fil | Wi-Fi 7 (intégré) + Bluetooth 5.4 |
| Système d'exploitation | NVIDIA DGX OS (basé sur Ubuntu Linux, kernel 6.x) |
| Architecture | aarch64 (ARM64) |
| Dimensions | 150 × 150 × 50.5 mm (1.13L) |
| Poids | Environ 1.2 kg |
| Alimentation | Alimentation USB-C de 240W |

### 2.2 Environnement logiciel : NVIDIA DGX OS

| Élément | Description |
|---|---|
| Base | Ubuntu Linux (personnalisé par NVIDIA) |
| Kernel | Linux 6.x (la version exacte suit les mises à jour de DGX OS) |
| Architecture | aarch64 (ARM64) |
| Logiciels préinstallés | Stack de logiciels AI NVIDIA (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Gestion des paquets | apt (famille Debian/Ubuntu) |
| Cadre de pilotes | Architecture de pilotes standard du kernel Linux (cfg80211 / mac80211) |

### 2.3 Caractéristiques clés : kernel moderne + ARM64

L'environnement logiciel du DGX Spark a deux impacts clés sur la compatibilité avec les cartes ALFA :

- Kernel 6.x (moderne) : le kernel 6.17 (version testée sur le GX10) intègre les pilotes des 9 cartes réseau de cet article, notamment mt76 (MT7612U / MT7610U, 4.19+), mt7921u (MT7921AUN, 5.18+), rtw88 (RTL8821CU 6.2+ ; RTL8812AU / RTL8811AU 6.13+) et rtw89 (RTL8832BU, 6.17+). Cela contraste fortement avec le kernel 4.9 du Jetson Nano.
- Architecture ARM64 (aarch64) : avec les pilotes intégrés au kernel, il n'y a rien à compiler sur ARM64 ; seuls les anciens systèmes dont le kernel est antérieur à la version minimale de la carte nécessitent la compilation des pilotes DKMS de la communauté pour les modèles Realtek (par exemple la série morrownr, en vérifiant que CONFIG_PLATFORM_ARM64 = y dans le Makefile).

### 2.4 Besoins en adaptateurs USB Type-C

Les 4 ports USB du DGX Spark sont de type C, tandis que toute la gamme des cartes ALFA (sauf l'AXML en USB-C) utilise une interface USB Type-A :

| Modèle | Spécification de l'interface | Adaptateur nécessaire |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ Pas d'adaptateur (branchement direct) |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ Adaptateur USB-C vers USB-A nécessaire |
| AWUS036AX | USB Type-A / USB 3.2 | ✅ Nécessaire |
| AWUS036AXER | USB Type-A / USB 3.2 | ✅ Nécessaire |
| AWUS036ACH | USB Type-A / USB 3.0 | ✅ Nécessaire |
| AWUS036ACHM | USB Type-A / USB 2.0 | ✅ Nécessaire |
| AWUS036ACM | USB Type-A / USB 3.0 | ✅ Nécessaire |
| AWUS036ACS | USB Type-A / USB 2.0 | ✅ Nécessaire |
| AWUS036EACS | USB Type-A / USB 2.0 | ✅ Nécessaire |

Conseil : utilisez un adaptateur ou un câble USB-C vers USB-A compatible USB 3.2 Gen 2×2 (20Gbps) pour que les modèles USB 3.x comme AWUS036ACH / ACM / AX puissent fonctionner à pleine vitesse.

## 3. Analyse des spécifications et des puces des cartes réseau ALFA

Au 9 septembre 2026, la gamme de cartes réseau USB sans fil actuelles d'ALFA Network est la suivante (base : 9 modèles) :

| Modèle | Niveau Wi-Fi | Puce | Interface | Pilote Linux intégré (version minimale du kernel) |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E (6GHz validé en test) | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ Intégré (mt7921u, 5.18+) |
| AWUS036AXM | Wi-Fi 6E (selon le fabricant, 6GHz non testé) | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ Intégré (mt7921u, 5.18+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ Intégré (rtw89_8852bu, 6.17+) |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ Intégré (rtw89_8852bu, 6.17+) |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ Intégré (rtw88_8812au, 6.13+) |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | ✅ Intégré (mt76x0u, 4.19+) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ Intégré (mt76x2u, 4.19+) |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | ✅ Intégré (rtw88_8821au, 6.13+) |
| AWUS036EACS | Wi-Fi 5 (AC600) + Bluetooth | Realtek RTL8821CU | USB 2.0 | ✅ Intégré (rtw88_8821cu, 6.2+) |

Remarque : le kernel 6.17 testé sur le GX10 intègre les pilotes des 9 modèles ; la version minimale du kernel diffère selon la carte (voir entre parenthèses dans le tableau). Seuls les anciens systèmes dont le kernel est antérieur à la version minimale de la carte nécessitent l'installation des pilotes DKMS maintenus par la communauté.

## 4. Modèles et SoC compatibles

### 4.1 Catégorie recommandée

| Catégorie recommandée | Modèle (SoC) | Description |
|---|---|---|
| ⭐ Premier choix pour les tests d'intrusion | AWUS036EACS (RTL8821CU) / AWUS036ACH (RTL8812AU) / AWUS036ACS (RTL8811AU) | Pilote intégré, aucune installation ; injection testée à 100 % sur les deux bandes pour EACS et ACH, ACS à 100 % en 2.4GHz et 96 % en 5GHz ; capture de handshake WPA de bout en bout possible |
| ✅ Recommandé | AWUS036ACM (MT7612U) | Pilote intégré, aucune installation ; monitor, injection (2.4GHz 63–83 %, 5GHz 76 %), AP et WPA3 fonctionnent |
| ✅ Recommandé | AWUS036ACHM (MT7610U) | Pilote intégré, aucune installation ; injection 2.4GHz 96–100 %, en 5GHz seule l'injection en broadcast fonctionne ; un AP WPA3 nécessite sae_pwe=0 |
| ✅ Recommandé (Wi-Fi 6) | AWUS036AX / AXER (RTL8832BU) | Pilote intégré, aucune installation ; bonne réception en monitor, injection fonctionnelle (2.4GHz : AX 96 %, AXER 73 %), AP en 80MHz |
| ⚠️ Connexion / AP uniquement | AWUS036AXML / AXM (MT7921AUN) | Pilote intégré, aucune installation ; monitor, AP et WPA3 fonctionnent, mais l'injection échoue sur le kernel 6.17 d'origine, donc inadapté aux tests d'intrusion ; l'AXML se branche directement en USB-C |

### 4.2 Suggestions de scénarios d'utilisation

| Scénario d'utilisation | Modèle recommandé | Description |
|---|---|---|
| Internet sans fil général (le plus simple) | Les 9 modèles conviennent (par exemple AWUS036ACM / ACHM) | Tous utilisent des pilotes intégrés au kernel et fonctionnent dès le branchement |
| Tests d'intrusion / Écoute / Injection sans fil | AWUS036EACS / ACH / ACS | Injection testée à 96–100 %, capture de handshake WPA de bout en bout ; évitez AXM / AXML (injection en échec) |
| Wi-Fi 6 + point d'accès AP | AWUS036AX / AXER | AP 2x2 en 80MHz validé en test |
| Bande 6GHz | AWUS036AXML | Création d'un AP WPA3 en 6GHz validée en test ; l'AXM a la même puce mais le 6GHz n'a pas été testé |
| Vous possédez déjà un AWUS036ACH | AWUS036ACH | À partir du kernel 6.13, rtw88_8812au est intégré : la carte fonctionne dès le branchement, injection testée à 100 % sur les deux bandes |
| Pas besoin de Wi-Fi externe (utilisation du Wi-Fi intégré) | — | Le DGX Spark intègre déjà le Wi-Fi 7 ; une navigation Internet classique ne nécessite pas de carte ALFA externe |

Remarque : le DGX Spark intègre déjà le Wi-Fi 7 + Bluetooth 5.4 ; pour un usage Internet classique, une carte réseau ALFA externe n'est pas nécessaire. Les principaux besoins justifiant une carte ALFA externe sont : les tests d'intrusion (écoute / injection), les besoins liés à une puce spécifique, ou les situations où le Wi-Fi intégré ne suffit pas.

## 5. Besoins environnementaux

### 5.1 Besoins matériels

| Élément | Besoin |
|---|---|
| Adaptateur USB | Adaptateur ou câble USB-C vers USB-A (sauf pour l'AXML) |
| Alimentation | Alimentation USB-C 240W d'origine du DGX Spark (alimentation suffisante des ports USB) |
| Refroidissement | Le refroidissement d'origine suffit (une carte WiFi USB n'augmente pas sensiblement la charge du système) |

### 5.2 Besoins logiciels

| Élément | Besoin |
|---|---|
| Version DGX OS | Toute version actuelle (kernel 6.x) |
| Version du kernel | Le kernel 6.17 (testé sur GX10 en 6.17.0-1014-nvidia) intègre les pilotes des 9 cartes réseau, aucun outil de compilation n'est nécessaire ; la version minimale diffère selon la carte (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), et seuls les kernels antérieurs à cette version nécessitent les pilotes DKMS de la communauté |
| Outils de gestion sans fil | iw, wpa_supplicant, network-manager (préinstallés sur DGX OS) |

## 6. Détermination de la compatibilité

### Matrice de compatibilité modèles ALFA actuels × NVIDIA DGX Spark (GB10)

| Modèle | Puce | Pilote (intégré au kernel) | Détection USB | STA Internet | Mode AP | Monitor | Injection de paquets | Difficulté d'installation | Évaluation globale |
|---|---|---|---|---|---|---|---|---|---|
| AWUS036EACS | RTL8821CU | rtw88_8821cu | ✅ | ✅ | ✅ | ✅ | ✅ 100 % sur les deux bandes | Sans installation | ⭐ Meilleur |
| AWUS036ACH | RTL8812AU | rtw88_8812au | ✅ | ✅ | ✅ | ✅ | ✅ 100 % sur les deux bandes | Sans installation | ⭐ Meilleur |
| AWUS036ACS | RTL8811AU | rtw88_8821au | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 100 % / 5G 96 % | Sans installation | ⭐ Meilleur |
| AWUS036ACM | MT7612U | mt76x2u | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 63–83 % / 5G 76 % | Sans installation | ✅ Bon |
| AWUS036ACHM | MT7610U | mt76x0u | ✅ | ✅ | ✅ | ✅ | ⚠️ 2.4G 96–100 % / 5G broadcast uniquement | Sans installation | ✅ Bon |
| AWUS036AX | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ Bonne réception | ✅ 2.4G 96 % / 5G fonctionnel | Sans installation | ✅ Bon |
| AWUS036AXER | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ Bonne réception | ✅ 2.4G 73 % / 5G fonctionnel | Sans installation | ✅ Bon |
| AWUS036AXML | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ Réception faible | ❌ Échec | Sans installation | ⚠️ Connexion / AP uniquement |
| AWUS036AXM | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ Réception faible | ❌ Échec | Sans installation | ⚠️ Connexion / AP uniquement |

Critère de détermination : tests sur machine réelle du 16 au 18 novembre 2026 sur l'ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), avec notre propre réseau Wi-Fi et nos propres téléphones comme cibles. Le DGX Spark utilise la même puce GB10 et la même famille de kernels NVIDIA ; le comportement attendu est identique, mais les tests ont été effectués uniquement sur le GX10 et le DGX Spark n'a pas été testé individuellement. Données complètes : [Tableau des tests ARM64 des 9 cartes réseau ALFA](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 7. Guide ultra détaillé : configuration étape par étape

### 7.1 Préparation

**Étape 1 : Démarrer et se connecter au DGX Spark** (par SSH ou en branchant directement clavier et écran)

```bash
ssh username@<dgx-spark-ip>
```

**Étape 2 : Vérifier l'architecture du système et la version du kernel**

```bash
uname -m
# Attendu : aarch64
uname -r
# Attendu : 6.x.x (kernel DGX OS)
```

**Étape 3 : Vérifier que la version du kernel est 6.17 ou supérieure**

À partir du kernel 6.17, les pilotes des 9 cartes réseau sont tous intégrés et aucun outil de compilation n'est nécessaire. La version minimale diffère selon la carte (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17) ; en dessous de cette version, seuls les modèles Realtek nécessitent les pilotes DKMS de la communauté (voir le dernier paragraphe de la section 7.3).

### 7.2 Chemin A : Modèles à puce MediaTek (AWUS036ACM / ACHM / AXML / AXM) — Prêts à l'emploi

**Étape 1 : Insérer la carte réseau**

Utilisez un adaptateur USB-C vers USB-A (l'AXML se branche directement sur un port USB-C) et insérez la carte réseau ALFA dans un port USB du DGX Spark.

**Étape 2 : Vérifier la détection de la carte réseau**

```bash
lsusb
# Exemple de sortie attendue (AWUS036ACM / MT7612U) :
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Étape 3 : Vérifier la création automatique de l'interface réseau**

```bash
ip link show
# Attendu : une interface commençant par wlx (nommée d'après l'adresse MAC, pilote in-kernel chargé automatiquement)
```

**Étape 4 : Scanner les réseaux WiFi** (wlan0 est utilisé ici à titre d'exemple ; remplacez-le par le nom d'interface trouvé avec `ip link show`)

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**Étape 5 : Se connecter au WiFi (via NetworkManager)**

```bash
nmcli dev wifi list
nmcli dev wifi connect "Nom de votre WiFi" password "Mot de passe de votre WiFi"
```

**Étape 6 : (Optionnel) Activer le mode écoute**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info
```

### 7.3 Chemin B : Modèles Realtek Wi-Fi 5 (AWUS036ACH / ACS / EACS) — aucune installation à partir du kernel 6.13 (EACS 6.2+)

**Étape 1 : Insérer la carte réseau et vérifier que le pilote est chargé automatiquement**

```bash
uname -r          # ACH / ACS : 6.13 ou supérieur requis ; EACS : 6.2 ou supérieur requis
lsusb
lsmod | grep rtw88
ip link show
```

Modules chargés automatiquement pour chaque modèle : ACH → `rtw88_8812au`, ACS → `rtw88_8821au`, EACS → `rtw88_8821cu` (l'EACS intègre aussi le Bluetooth, validé en test).

**Étape 2 : Connexion identique à l'étape 5 de la section 7.2 (via nmcli)**

**Étape 3 : (Optionnel) Mode écoute et injection**

⚠️ N'effectuez des tests d'écoute et d'injection que sur vos propres réseaux ou sur des réseaux pour lesquels vous disposez d'une autorisation.

```bash
sudo apt install -y aircrack-ng
IF=wlx00c0cafe0000   # remplacez par le nom d'interface trouvé avec ip link
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
sudo aireplay-ng --test $IF
```

- N'exécutez pas `airmon-ng check kill` : cette commande arrête NetworkManager et coupe la connexion réseau de la machine.
- Sur le kernel 6.17 d'origine, `aireplay-ng --test` échoue avec les AWUS036AXM / AXML (Found 0 APs) : impossible d'effectuer une deauth ou de capturer un handshake.
- hcxdumptool 8.x affiche `failed to arm` avec les 9 cartes sauf l'EACS en 2,4 GHz (le pilote ne prend pas en charge l'active monitor) ; utilisez plutôt airodump-ng + aireplay-ng.

**Étapes nécessaires uniquement sur un ancien kernel (ACH / ACS antérieur à 6.13, EACS antérieur à 6.2)** : après avoir installé `build-essential git bc dkms`, compilez le pilote de la communauté, par exemple morrownr/8812au-20210820 pour le RTL8812AU (en vérifiant que `CONFIG_PLATFORM_ARM64 = y` dans le Makefile). Si la version est suffisante, utilisez directement le pilote intégré.

### 7.4 Chemin C : Modèles Wi-Fi 6 (AWUS036AX / AXER, RTL8832BU) — aucune installation à partir du kernel 6.17

```bash
lsusb                      # attendu : 0bda:b832
lsmod | grep rtw89_8852bu
ip link show
```

Résultat des tests sur GX10 : le pilote intégré `rtw89_8852bu` se charge automatiquement, bonne réception en monitor, injection fonctionnelle (2.4GHz : AX 96 %, AXER 73 %), AP en 80MHz. rtw89_8852bu n'est intégré à la branche principale qu'à partir du kernel 6.17 ; les systèmes en kernel 6.16 ou antérieur nécessitent le pilote DKMS de la communauté (morrownr/rtl8852bu-20250826).

## 8. Erreurs courantes et solutions

| Symptômes | Causes probables | Solutions |
|---|---|---|
| `lsusb` ne voit pas la carte réseau ALFA | Adaptateur USB-C défectueux / mauvais contact | Changer l'adaptateur USB-C vers USB-A ; vérifier que l'adaptateur prend en charge la transmission de données (pas seulement la charge) ; essayer un autre port USB-C |
| Pas d'interface wlan après l'insertion d'une carte MediaTek | Module du kernel non chargé automatiquement / firmware manquant | Charger manuellement : `sudo modprobe mt76x2u` ; vérifier `dmesg \| grep mt76` ; installer le firmware : `sudo apt install linux-firmware` |
| Aucune interface wlan après avoir branché une carte Realtek | Kernel antérieur à la version minimale de la carte (EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), sans pilote correspondant intégré | Vérifier la version avec `uname -r` ; mettre à jour le kernel, ou installer les pilotes DKMS de la communauté sur l'ancien kernel |
| Sur un ancien kernel, `modprobe` renvoie "Operation not permitted" après l'installation d'un pilote DKMS | Secure Boot / signature du module | Signer le module ou désactiver Secure Boot (ce problème ne se pose pas avec les pilotes intégrés) |
| Plus aucun signal détecté après plusieurs bascules monitor / AP | Blocage de la réception (RX stall) | Débrancher et rebrancher la carte pour forcer une nouvelle énumération USB |
| Pas d'interface wlx après avoir rebranché l'EACS / l'AXML | Blocage du probe du périphérique composite Bluetooth + Wi-Fi | Rebrancher sur un autre port USB |
| Connexion WiFi instable / lente | L'adaptateur USB-C ne prend en charge que l'USB 2.0 | Utiliser un adaptateur compatible USB 3.2 Gen 2×2 ; vérifier que l'adaptateur porte la mention "Data" et non "Charge Only" |
| Conflit entre le Wi-Fi 7 intégré et la carte ALFA | Conflit de routage entre deux interfaces sans fil | Désactiver le Wi-Fi intégré : `sudo nmcli radio wifi off` ou le désactiver dans le BIOS/UEFI ; ou configurer l'ordre de priorité des routes |
| Le 6GHz (Wi-Fi 6E) ne peut pas être utilisé | Limitation du domaine réglementaire | Définir le domaine réglementaire : `sudo iw reg set US` (6GHz ouvert aux États-Unis) ; l'AXML a été validé en 6GHz, l'AXM n'a pas été testé |
| Échec du démarrage du mode AP | Conflit entre NetworkManager et hostapd | Se référer au guide Yopitek ALFA Soft AP ; retirer cette interface de la gestion de NetworkManager puis configurer hostapd manuellement |
| La carte réseau disparaît après la sortie de veille | Mise en veille automatique de l'USB (autosuspend) | Désactiver l'autosuspend USB : `echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. Limites connues

- **Adaptateur USB Type-C nécessaire** : à l'exception de l'AXML, toutes les cartes réseau ALFA nécessitent un adaptateur USB-C vers USB-A ; la qualité de l'adaptateur influe sur les performances et la stabilité.
- **Échec de l'injection sur les modèles MT7921** : sur le kernel 6.17 d'origine, les AWUS036AXM / AXML échouent à l'injection de paquets et ne peuvent ni effectuer de deauth ni capturer de handshake ; les modes monitor, AP et WPA3 fonctionnent. La cause principale est une régression du chanctx de mac80211 apparue après le kernel 6.16 ; les pilotes corrigés par la communauté restent limités en débit.
- **Périmètre des tests** : tests effectués uniquement sur l'ASUS GX10 (kernel 6.17.0-1014-nvidia) ; le DGX Spark n'a pas été testé individuellement, mais le comportement attendu est identique.
- **hcxdumptool inutilisable** : toutes les cartes sauf l'EACS en 2,4 GHz affichent `failed to arm` ; utilisez plutôt airodump-ng + aireplay-ng.
- **Possibilité de conflit avec le Wi-Fi intégré** : le DGX Spark intègre déjà le Wi-Fi 7 ; l'utilisation simultanée du Wi-Fi intégré et d'une carte externe peut entraîner des conflits de routage ou de ressources.
- **Configuration manuelle du mode AP** : DGX OS est configuré par défaut comme environnement de développement ; le mode point d'accès AP nécessite l'installation et la configuration manuelles de hostapd / dnsmasq.
- **Restrictions réglementaires pour la bande 6GHz** : la disponibilité de la bande 6GHz du Wi-Fi 6E dépend du domaine réglementaire configuré ; pour Taïwan, vérifiez la réglementation la plus récente concernant l'ouverture de la bande 6GHz.
- **Anciens kernels** : sur les systèmes dont le kernel est antérieur à la version minimale de la carte (EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), seuls les modèles Realtek nécessitent les pilotes DKMS de la communauté (morrownr), qui doivent être recompilés après chaque mise à jour du kernel.
- **Différences pour les tests d'intrusion** : lors des tests sur GX10, les taux de réussite d'injection les plus élevés ont été obtenus avec les modèles Realtek rtw88 (EACS et ACH : 100 % sur les deux bandes) ; les modèles MediaTek mt76 (ACM / ACHM) fonctionnent ; les MT7921 (AXM / AXML) échouent.
- **Fonctions Bluetooth** : le Bluetooth des AWUS036AXML et AWUS036EACS a été validé sur GX10 ; celui de l'AWUS036AXM n'a pas été vérifié séparément (le DGX Spark intègre déjà le BT 5.4).
- **RTL8832BU (AWUS036AX / AXER)** : le mainteneur de pilotes morrownr a publiquement recommandé d'éviter les pilotes out-of-tree de la série rtl8852/32au (source en section 10). Nos tests sur GX10 ont utilisé le pilote intégré au kernel `rtw89_8852bu`, avec lequel monitor, injection, AP et WPA3 fonctionnent ; cette conclusion ne s'applique qu'au pilote intégré des kernels 6.17 et ultérieurs.
- **RTL8812AU (AWUS036ACH)** : le pilote in-kernel `rtw88_8812au`, conforme au standard mac80211, a été intégré à la branche principale dans le kernel 6.13 et est mature depuis la version 6.14 (annonce de morrownr). Sur GX10 en kernel 6.17, la carte fonctionne dès le branchement, avec une injection à 100 % sur les deux bandes. Avant de répondre, le service client peut demander au client d'indiquer le résultat de `uname -r` pour vérifier qu'il s'agit d'un kernel 6.13 ou ultérieur.

Conditions de réfutation : si une mise à jour de DGX OS modifie la version du kernel ou le pilote du contrôleur USB et entraîne un comportement différent, ou si des tests sur un DGX Spark réel donnent des résultats différents de ceux du GX10, la matrice de compatibilité de la section 6 devra être réexaminée ; si un futur kernel corrige le problème d'injection de mt7921u, l'évaluation des AWUS036AXM / AXML pourra passer de « Connexion / AP uniquement » à un niveau supérieur.

## 10. Sources de référence URL

| Source | Description | URL | État de vérification | Date de vérification |
|---|---|---|---|---|
| Page officielle NVIDIA DGX Spark | Spécifications et informations sur la plateforme DGX Spark | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Vérifié | 2026-09-03 |
| Documentation NVIDIA DGX | Architecture de DGX OS et version du kernel | https://docs.nvidia.com/dgx/dgx-spark | ✅ Vérifié | 2026-09-03 |
| morrownr/8812au GitHub | Pilote Linux RTL8812AU (prise en charge ARM64) | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |
| morrownr/8821cu GitHub | Pilote Linux RTL8821CU (pour les anciens kernels) | https://github.com/morrownr/8821cu-20210916 | ✅ Vérifié | 2026-09-03 |
| morrownr/rtl8852bu GitHub | Pilote Linux RTL8832BU | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Vérifié | 2026-09-03 |
| Documentation du pilote mt76 du kernel Linux | Documentation des pilotes mainline MediaTek mt76 / mt7921 (y compris la version de kernel initiale prise en charge pour chaque puce) | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ Vérifié | 2026-09-03 |
| Guide Linux ALFA Soft AP WiFi Hotspot (Yopitek) | Guide de configuration du mode AP pour ALFA sous Linux | /fr/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Vérifié | 2026-09-03 |
| Vue d'ensemble des produits ALFA Network (Yopitek) | Spécifications des produits actuels d'ALFA | /fr/products/alfa/ | ✅ Vérifié | 2026-09-03 |
| Tableau des tests ARM64 des 9 cartes réseau ALFA (Yopitek) | Tests sur machine réelle ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Testé | 2026-11-18 |
| morrownr/USB-WiFi Issue #314 | Déclaration officielle du mainteneur du pilote : recommandation d'éviter les puces rtl8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Vérifié | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | Dernière annonce sur l'état du pilote RTL8812AU (intégré à la branche principale dans le kernel 6.13, mature à partir du kernel 6.14) | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |

Articles associés : [Les cartes réseau sans fil ALFA sont-elles compatibles avec le MSI EdgeXpert ?](/fr/blog/alfa-msi-edgexpert-compatibility/) | [Les cartes réseau sans fil ALFA sont-elles compatibles avec l'ASUS Ascent GX10 ?](/fr/blog/alfa-asus-ascent-gx10-compatibility/) | [Les cartes réseau sans fil ALFA sont-elles compatibles avec l'ALTOS BrainSphere GB10 F1 ?](/fr/blog/alfa-altos-brainsphere-gb10-compatibility/) | [Les cartes réseau sans fil ALFA sont-elles compatibles avec le GIGABYTE AI TOP ATOM ?](/fr/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [Les cartes réseau sans fil ALFA sont-elles compatibles avec le NVIDIA Jetson Nano ?](/fr/blog/alfa-nvidia-jetson-nano-compatibility/)

Déclaration de non-responsabilité : les conclusions de compatibilité de cet article reposent sur les tests sur machine réelle effectués en novembre 2026 sur l'ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia). Le DGX Spark utilise la même puce GB10 et la même famille de kernels NVIDIA que le GX10 ; le comportement attendu est identique, mais il n'a pas été testé individuellement. Le kernel 6.17 testé sur le GX10 intègre les pilotes des 9 cartes réseau ALFA (la version minimale diffère selon la carte) ; seuls les kernels antérieurs à la version minimale de la carte nécessitent les pilotes DKMS de la communauté (morrownr). Le DGX Spark intègre le Wi-Fi 7 ; les cartes réseau ALFA externes servent principalement aux tests d'intrusion ou aux besoins de puces spécifiques. La qualité de l'adaptateur USB-C influe directement sur l'expérience d'utilisation : choisissez de préférence un adaptateur de marque portant la mention USB 3.2 Gen 2×2. L'écoute et l'injection ne doivent être effectuées que sur vos propres réseaux ou sur des réseaux pour lesquels vous disposez d'une autorisation.
