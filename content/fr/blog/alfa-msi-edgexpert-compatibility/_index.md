---
title: "Les cartes Wi-Fi ALFA sont-elles compatibles avec le MSI EdgeXpert (GB10) ?"
date: 2026-09-03
draft: false
slug: "alfa-msi-edgexpert-compatibility"
tags:
  - "ALFA"
  - "MSI"
  - "EdgeXpert"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "Guide Matériel"
description: "Cartes USB ALFA sur MSI EdgeXpert (GB10) : 9 modèles testés sur ASUS GX10 en kernel 6.17, pilotes intégrés sans DKMS ; injection en échec sur AXM/AXML."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Article mis à jour d'après nos tests sur GX10 de novembre 2026 : sur l'ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), les 9 cartes réseau ALFA actuelles utilisent toutes les pilotes intégrés au kernel et fonctionnent dès le branchement, sans DKMS. Données complètes : [Tableau des tests ARM64 des 9 cartes réseau ALFA](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Tests effectués uniquement sur le GX10 ; les autres machines GB10 n'ont pas été testées une par une.

## 1. Résumé du problème

Question d'un client : « Les cartes réseau sans fil USB de la gamme ALFA peuvent-elles être utilisées sur le supercalculateur IA MSI EdgeXpert (NVIDIA GB10 Grace Blackwell) ? »

Conclusion rapide : le MSI EdgeXpert et le NVIDIA DGX Spark utilisent la même puce GB10 et la même famille de kernels NVIDIA. Nous avons testé sur l'ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia) les 9 cartes réseau USB ALFA actuelles (AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML) : toutes utilisent les pilotes intégrés au kernel et fonctionnent dès le branchement, sans compilation ni DKMS. Le comportement attendu est identique, mais les tests ont été effectués uniquement sur le GX10 : le MSI EdgeXpert n'a pas été testé individuellement. Différences fonctionnelles : les modèles MediaTek MT7921 (AWUS036AXM / AXML) échouent à l'injection de paquets (packet injection) sur le kernel 6.17 d'origine, tandis que les modes monitor, AP et WPA3 fonctionnent ; pour les 7 autres modèles, le mode monitor et l'injection ont été validés en test. La version minimale du kernel à partir de laquelle chaque pilote est intégré à la branche principale diffère selon la carte (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17) ; seuls les kernels antérieurs à cette version nécessitent les pilotes DKMS de la communauté. Attention : les 4 ports USB de l'EdgeXpert sont tous de type USB Type-C (20Gbps) ; les cartes ALFA (à l'exception de l'AXML) doivent utiliser un adaptateur USB-C vers USB-A.

Modèles évalués : ALFA dispose de 9 cartes réseau USB actuelles (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analyse des spécifications matérielles cibles

### 2.1 Spécifications matérielles de MSI EdgeXpert

| Élément | Spécification |
|---|---|
| Nom du produit | MSI EdgeXpert (modèles : EdgeXpert-MS-C931 / 59STW et autres) |
| Processeur central | NVIDIA GB10 Grace Blackwell Superchip (plateforme DGX Spark) |
| CPU | 20-coeurs Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Architecture Blackwell de NVIDIA, 6144 cœurs CUDA, cinquième génération Tensor Core, quatrième génération RT Core |
| Performance AI | Jusqu'à 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| Mémoire système | 128GB LPDDR5x mémoire unifiée (256-bit, 273 GB/s) |
| Stockage | 1TB ou 4TB SSD NVMe M.2 (cryptage intégré, PCIe Gen5) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (jusqu'à 20Gbps) |
| Sortie vidéo | 1× HDMI 2.1a (4× DP1.4a via USB-C Alt Mode) |
| Réseau filaire | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (QSFP 200GbE, interconnexions système) |
| Réseau sans fil | Wi-Fi 7 + Bluetooth 5.4 |
| Système d'exploitation | NVIDIA DGX OS (basé sur Ubuntu Linux, kernel 6.x) |
| Architecture | aarch64 (ARM64) |
| Dimensions | 151 × 151 × 52 mm (environ 5.95" × 5.95" × 2.05") |
| Poids | Environ 1.2 kg (2.65 lbs) |
| Alimentation | Alimentation USB-C de 240W |
| Version | Version grand public / version industrielle (EdgeXpert-MS-C931, plage de température étendue / usage industriel) |

### 2.2 Environnement logiciel : NVIDIA DGX OS

Le MSI EdgeXpert est livré avec NVIDIA DGX OS préinstallé, tout comme le DGX Spark et l'ASUS GX10 :

| Élément | Description |
|---|---|
| Base | Ubuntu Linux (personnalisé par NVIDIA) |
| Kernel | Linux 6.x |
| Architecture | aarch64 (ARM64) |
| Logiciels préinstallés | NVIDIA AI Software Stack (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Gestion des paquets | apt |

### 2.3 Différences avec DGX Spark

Le MSI EdgeXpert est une version OEM de la plateforme DGX Spark, avec un matériel et des logiciels identiques :

| Élément | MSI EdgeXpert | NVIDIA DGX Spark |
|---|---|---|
| Conception du châssis | Châssis personnalisé MSI, option industrielle | Châssis de référence NVIDIA |
| Options de stockage | 1TB / 4TB | Jusqu'à 4TB |
| Marché cible | IA en périphérie / IA industrielle / développement sur poste de travail | Développement IA sur poste de travail |
| Accessoires | Accessoires d'origine MSI | Accessoires d'origine NVIDIA |

Impact sur la compatibilité avec ALFA : aucun impact attendu (tests effectués uniquement sur le GX10 ; les autres machines GB10 n'ont pas été testées une par une). Les contrôleurs USB, les versions du kernel et les frameworks de pilotes sont identiques à ceux du DGX Spark.

### 2.4 Besoins en adaptateurs USB Type-C

Les 4 ports USB de l'EdgeXpert sont de type C. Toute la gamme de cartes réseau ALFA (sauf l'AXML en USB-C) est de type A, il est donc nécessaire d'utiliser un adaptateur. Il est recommandé de choisir un adaptateur compatible USB 3.2 Gen 2×2 (20Gbps).

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

## 4. Modèles et SoC applicables

### 4.1 Catégorie de recommandation

| Catégorie de recommandation | Modèle (SoC) | Description |
|---|---|---|
| ⭐ Premier choix pour les tests d'intrusion | AWUS036EACS (RTL8821CU) / AWUS036ACH (RTL8812AU) / AWUS036ACS (RTL8811AU) | Pilote intégré, aucune installation ; injection testée à 100 % sur les deux bandes pour EACS et ACH, ACS à 100 % en 2.4GHz et 96 % en 5GHz ; capture de handshake WPA de bout en bout possible |
| ✅ Recommandé | AWUS036ACM (MT7612U) | Pilote intégré, aucune installation ; monitor, injection (2.4GHz 63–83 %, 5GHz 76 %), AP et WPA3 fonctionnent |
| ✅ Recommandé | AWUS036ACHM (MT7610U) | Pilote intégré, aucune installation ; injection 2.4GHz 96–100 %, en 5GHz seule l'injection en broadcast fonctionne ; un AP WPA3 nécessite sae_pwe=0 |
| ✅ Recommandé (Wi-Fi 6) | AWUS036AX / AXER (RTL8832BU) | Pilote intégré, aucune installation ; bonne réception en monitor, injection fonctionnelle (2.4GHz : AX 96 %, AXER 73 %), AP en 80MHz |
| ⚠️ Connexion / AP uniquement | AWUS036AXML / AXM (MT7921AUN) | Pilote intégré, aucune installation ; monitor, AP et WPA3 fonctionnent, mais l'injection échoue sur le kernel 6.17 d'origine, donc inadapté aux tests d'intrusion ; l'AXML se branche directement en USB-C |

### 4.2 Recommandations d'utilisation

| Scénario d'utilisation | Modèle recommandé | Description |
|---|---|---|
| Connexion sans fil pour passerelle IA en périphérie | Les 9 modèles conviennent (par exemple AWUS036ACM / ACHM) | Tous utilisent des pilotes intégrés au kernel et fonctionnent dès le branchement |
| Tests d'intrusion sans fil en environnement industriel | AWUS036EACS / ACH / ACS | Injection testée à 96–100 %, capture de handshake WPA de bout en bout ; évitez AXM / AXML (injection en échec) |
| Wi-Fi 6 + point d'accès AP | AWUS036AX / AXER | AP 2x2 en 80MHz validé en test |
| Bande 6GHz | AWUS036AXML | Création d'un AP WPA3 en 6GHz validée en test ; l'AXM a la même puce mais le 6GHz n'a pas été testé |
| Pas besoin de Wi-Fi externe | — | L'EdgeXpert intègre déjà le Wi-Fi 7 ; pas besoin d'ajouter un Wi-Fi externe pour naviguer sur Internet |

## 5. Besoins environnementaux

### 5.1 Besoins matériels

| Élément | Besoin |
|---|---|
| Adaptateur USB | Adaptateur ou câble USB-C vers USB-A (sauf pour l'AXML), de préférence compatible USB 3.2 Gen 2×2 |
| Alimentation | Alimentation USB-C 240W d'origine MSI EdgeXpert |

### 5.2 Besoins logiciels

| Élément | Besoin |
|---|---|
| Version DGX OS | Version actuelle (kernel 6.x) |
| Version du kernel | Le kernel 6.17 (testé sur 6.17.0-1014-nvidia) intègre les pilotes des 9 cartes réseau, aucun outil de compilation n'est nécessaire ; la version minimale diffère selon la carte (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), et seuls les kernels antérieurs à cette version nécessitent les pilotes DKMS de la communauté |
| Outils de gestion sans fil | iw, network-manager (installés par défaut dans DGX OS) |

## 6. Détermination de la compatibilité

### Matrice de compatibilité modèles ALFA actuels × MSI EdgeXpert (GB10)

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

Critère de détermination : tests sur machine réelle du 16 au 18 novembre 2026 sur l'ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), avec notre propre réseau Wi-Fi et nos propres téléphones comme cibles. Le MSI EdgeXpert utilise la même puce GB10 et la même famille de kernels NVIDIA ; le comportement attendu est identique, mais les tests ont été effectués uniquement sur le GX10 et le MSI EdgeXpert n'a pas été testé individuellement. Données complètes : [Tableau des tests ARM64 des 9 cartes réseau ALFA](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 7. Guide ultra détaillé : configuration étape par étape

Les étapes d'installation du MSI EdgeXpert devraient être identiques à celles du NVIDIA DGX Spark (étapes validées sur le GX10). Voici une version abrégée ; pour les étapes complètes, consultez la section 7 de l'article [Les cartes réseau sans fil ALFA sont-elles compatibles avec le NVIDIA DGX Spark ?](/fr/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modèles à puce MediaTek (AWUS036ACM / ACHM / AXM / AXML)

**Étape 1 : Insérer la carte réseau**

Utilisez un adaptateur USB-C vers USB-A (l'AXML se branche directement) pour insérer la carte réseau ALFA dans un port USB-C de l'EdgeXpert.

**Étape 2 : Vérifier la détection USB**

```bash
lsusb
# Exemple de sortie attendue (AWUS036ACM / MT7612U) :
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Étape 3 : Vérifier l'interface réseau**

```bash
ip link show
# Une interface commençant par wlx doit apparaître automatiquement (pilote in-kernel chargé automatiquement)
```

**Étape 4 : Se connecter au WiFi**

```bash
nmcli dev wifi connect "SSID" password "mot de passe"
```

### 7.2 Modèles à puce Realtek (AWUS036ACH / ACS / EACS / AX / AXER)

Le kernel 6.17 (version testée sur le GX10) intègre les pilotes de tous les modèles Realtek ; les étapes sont identiques à celles des modèles MediaTek, sans compilation (versions minimales : EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17) :

```bash
# 1. Vérifiez la version du kernel (à partir de 6.17, les pilotes de tous les modèles Realtek sont intégrés ; testé sur GX10 en 6.17.0-1014-nvidia)
uname -r

# 2. Après avoir branché la carte réseau, vérifiez que le pilote est chargé automatiquement
lsusb
lsmod | grep -E "rtw88|rtw89"
ip link show

# 3. Connectez-vous au WiFi
nmcli dev wifi connect "SSID" password "mot de passe"
```

Modules chargés automatiquement pour chaque modèle : ACH → `rtw88_8812au`, ACS → `rtw88_8821au`, EACS → `rtw88_8821cu`, AX / AXER → `rtw89_8852bu`. Ce n'est que si `uname -r` est inférieur à la version minimale de la carte (anciens systèmes) qu'il faut installer les pilotes DKMS maintenus par la communauté (par exemple morrownr/8812au-20210820 pour le RTL8812AU).

### 7.3 Mode écoute (test d'intrusion)

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

## 8. Erreurs courantes et solutions

| Symptômes | Causes possibles | Solutions |
|---|---|---|
| `lsusb` ne voit pas la carte réseau ALFA | Adaptateur USB-C défectueux / charge uniquement | Utiliser un adaptateur USB 3.2 Gen 2×2 compatible avec la transmission de données ; essayer un autre port USB-C |
| Interface wlan absente pour la puce MediaTek | Module non chargé automatiquement / firmware manquant | `sudo modprobe mt76x2u` ; `sudo apt install linux-firmware` ; vérifier `dmesg \| grep mt76` |
| Aucune interface wlan après avoir branché une carte Realtek | Kernel antérieur à la version minimale de la carte (EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), sans pilote correspondant intégré | Vérifier la version avec `uname -r` ; mettre à jour le kernel, ou installer les pilotes DKMS de la communauté sur l'ancien kernel |
| Plus aucun signal détecté après plusieurs bascules monitor / AP | Blocage de la réception (RX stall) | Débrancher et rebrancher la carte pour forcer une nouvelle énumération USB |
| Pas d'interface wlx après avoir rebranché l'EACS / l'AXML | Blocage du probe du périphérique composite Bluetooth + Wi-Fi | Rebrancher sur un autre port USB |
| Vitesse WiFi lente | Adaptateur limité à l'USB 2.0 | Utiliser un adaptateur USB 3.2 Gen 2×2 |
| Conflit entre le Wi-Fi intégré et externe | Conflit de routage | `sudo nmcli radio wifi off` pour désactiver le WiFi intégré avant d'utiliser le WiFi externe |
| Instabilité à haute température en environnement industriel | Refroidissement / différences avec la version industrielle | Vérifier que vous utilisez la version industrielle EdgeXpert (MS-C931) ; s'assurer que la température ambiante est dans les limites spécifiées |

## 9. Limitations connues

- Adaptateur USB Type-C nécessaire : toutes les cartes réseau ALFA, sauf l'AXML, nécessitent un adaptateur USB-C vers USB-A
- Échec de l'injection sur les modèles MT7921 : sur le kernel 6.17 d'origine, les AWUS036AXM / AXML échouent à l'injection de paquets et ne peuvent ni effectuer de deauth ni capturer de handshake ; les modes monitor, AP et WPA3 fonctionnent. La cause principale est une régression du chanctx de mac80211 apparue après le kernel 6.16 ; les pilotes corrigés par la communauté restent limités en débit
- Périmètre des tests : tests effectués uniquement sur l'ASUS GX10 (kernel 6.17.0-1014-nvidia) ; le MSI EdgeXpert n'a pas été testé individuellement, mais le comportement attendu est identique
- hcxdumptool inutilisable : toutes les cartes sauf l'EACS en 2,4 GHz affichent `failed to arm` ; utilisez plutôt airodump-ng + aireplay-ng
- Possibilité de conflit avec le Wi-Fi 7 intégré : l'EdgeXpert intègre déjà le Wi-Fi 7 + BT 5.4
- Mode AP à configurer manuellement : DGX OS est par défaut un environnement de développement
- Limitations réglementaires pour la bande 6GHz : la disponibilité du Wi-Fi 6E dépend des zones réglementaires
- Anciens kernels : sur les systèmes dont le kernel est antérieur à la version minimale de la carte (EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), seuls les modèles Realtek nécessitent les pilotes DKMS de la communauté, qui doivent être recompilés après chaque mise à jour du kernel
- La version industrielle n'a pas d'incidence sur la compatibilité : la version industrielle MSI (MS-C931) a les mêmes spécifications matérielles que la version grand public, et la compatibilité USB WiFi est identique

Conditions de réfutation : si la page de spécifications officielle de MSI change (modification des ports USB, version du kernel inférieure à 6.x), ou si des tests réels montrent que mt76x2u / mt7921u ne se chargent pas automatiquement sous DGX OS, la matrice de compatibilité de la section 6 devra être révisée ; si le comportement des pilotes intégrés change après une mise à jour du kernel NVIDIA, de nouveaux tests seront nécessaires.

## 10. Sources de référence URL

| Source | Description | URL | État de vérification | Date de vérification |
|---|---|---|---|---|
| Boutique officielle MSI EdgeXpert (US) | Spécifications de la version grand public d'EdgeXpert | https://us-store.msi.com/MSI-EdgeXpert-Blackwell-AI-Supercomputer | ✅ Vérifié | 2026-09-03 |
| Boutique MSI EdgeXpert (TW) | Spécifications de la version grand public d'EdgeXpert (23STW) | https://tw-store.msi.com/products/edgexpert-23stw-bgb104tg4 | ✅ Vérifié | 2026-09-03 |
| Annonce officielle MSI (ordinateurs industriels) | Informations de lancement du produit EdgeXpert | https://ipc.msi.com/en/news/146241 | ✅ Vérifié | 2026-09-03 |
| Page officielle NVIDIA DGX Spark | Informations sur la plateforme GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Vérifié | 2026-09-03 |
| morrownr/8812au GitHub | Pilote Linux pour RTL8812AU | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |
| Produits ALFA Network (Yopitek) | Spécifications des produits actuels d'ALFA | /fr/products/alfa/ | ✅ Vérifié | 2026-09-03 |
| Tableau des tests ARM64 des 9 cartes réseau ALFA (Yopitek) | Tests sur machine réelle ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Testé | 2026-11-18 |

Articles associés : [Les cartes réseau sans fil ALFA sont-elles compatibles avec le NVIDIA DGX Spark ?](/fr/blog/alfa-nvidia-dgx-spark-compatibility/) | [Les cartes réseau sans fil ALFA sont-elles compatibles avec l'ASUS Ascent GX10 ?](/fr/blog/alfa-asus-ascent-gx10-compatibility/) | [Les cartes réseau sans fil ALFA sont-elles compatibles avec l'ALTOS BrainSphere GB10 F1 ?](/fr/blog/alfa-altos-brainsphere-gb10-compatibility/) | [Les cartes réseau sans fil ALFA sont-elles compatibles avec le GIGABYTE AI TOP ATOM ?](/fr/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [Les cartes réseau sans fil ALFA sont-elles compatibles avec le NVIDIA Jetson Nano ?](/fr/blog/alfa-nvidia-jetson-nano-compatibility/)

Déclaration de non-responsabilité : les conclusions de compatibilité de cet article reposent sur les tests sur machine réelle effectués en novembre 2026 sur l'ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia). Le MSI EdgeXpert utilise la même puce GB10 et la même famille de kernels NVIDIA que le GX10 ; le comportement attendu est identique, mais il n'a pas été testé individuellement. Le kernel 6.17 testé sur le GX10 intègre les pilotes des 9 cartes réseau ALFA (la version minimale diffère selon la carte) ; seuls les kernels antérieurs à la version minimale de la carte nécessitent les pilotes DKMS de la communauté. L'EdgeXpert intègre le Wi-Fi 7 ; une carte ALFA externe sert principalement aux tests d'intrusion ou aux besoins de puces spécifiques. L'écoute et l'injection ne doivent être effectuées que sur vos propres réseaux ou sur des réseaux pour lesquels vous disposez d'une autorisation.
