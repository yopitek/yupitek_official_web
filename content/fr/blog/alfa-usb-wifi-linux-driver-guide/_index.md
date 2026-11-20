---
title: "Choisir le pilote Linux pour la carte réseau USB ALFA : MediaTek sans compilation vs Realtek nécessitant une compilation"
date: 2026-09-03
draft: false
slug: "alfa-usb-wifi-linux-driver-guide"
tags:
  - "ALFA"
  - "Linux-Driver"
  - "MediaTek"
  - "Realtek"
  - "in-kernel"
  - "out-of-tree"
  - "DKMS"
  - "mt76"
  - "rtl8812au"
categories:
  - "Guide Matériel"
description: "Document technique de Yopitek sur 6 cartes Wi-Fi USB ALFA : les 3 modèles MediaTek fonctionnent avec les pilotes intégrés au noyau, les modèles Realtek exigent en général la compilation d'un pilote out-of-tree, sauf si le noyau est assez récent (EACS : intégré depuis 6.2 ; ACH/ACS : 6.13 ; AX/AXER : 6.17)."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> **Document de support technique · 1ère version du 3 septembre 2026 (écrit selon les règles de blog-writing-rules.md v1.0)**
> Matrice de référence : Les 6 modèles de cartes réseau USB ALFA actuels de Yopitek mentionnés dans ce document technique (3 modèles MediaTek, 3 modèles Realtek).
> Articles associés : [Les cartes réseau sans fil ALFA sont-elles compatibles avec NVIDIA DGX Spark ?](/fr/blog/alfa-nvidia-dgx-spark-compatibility/) | [Les cartes réseau sans fil ALFA sont-elles compatibles avec OpenWrt ?](/fr/blog/alfa-openwrt-router-compatibility/) | [Les cartes réseau sans fil ALFA sont-elles compatibles avec NVIDIA Jetson Nano ?](/fr/blog/alfa-nvidia-jetson-nano-compatibility/) | [Les cartes réseau sans fil ALFA sont-elles compatibles avec Tomato ?](/fr/blog/alfa-tomato-router-compatibility/) | [Les cartes réseau sans fil ALFA sont-elles compatibles avec DD-WRT ?](/fr/blog/alfa-ddwrt-router-compatibility/)

## Un mot pour résumer

**Sur les 6 modèles répertoriés, 3 utilisent des puces MediaTek (MT7610U / MT7612U / MT7921AUN) et sont prêts à l'emploi avec les pilotes intégrés dans le kernel moderne ; les 3 autres avec des puces Realtek (RTL8812AU / RTL8821CU / RTL8832BU) nécessitent une compilation manuelle des pilotes out-of-tree sur un noyau ancien ; le pilote `rtw88_8821cu` de l'EACS est intégré au noyau depuis 6.2 (ACH/ACS : 6.13 ; AX/AXER : 6.17), donc sur GX10 (noyau 6.17) les trois modèles Realtek fonctionnent sans installation.** Si vous préférez éviter les complications, vérifiez d'abord le type de puce avant de passer commande.

---

## Premier act : Scène - Pourquoi certains peuvent l'utiliser sans rien installer, tandis que d'autres doivent compiler pendant deux heures

Deux situations réelles :

- Client A : il branche le **AWUS036ACM** sur un ordinateur de bureau Ubuntu, exécute `lsusb`, et NetworkManager affiche directement wlan0 - sans rien avoir installé.
- Client B : il branche le **AWUS036ACH** sur le même matériel, mais la carte réseau ne répond pas. Il doit aller sur GitHub, récupérer les codes sources, installer des outils de compilation, compiler, puis redémarrer l'ordinateur.

La différence ne dépend pas du hasard, ni du système d'exploitation Linux, mais bien de l'**appartenance du chip au bon camp** : le pilote USB WiFi du MediaTek (série mt76) est déjà intégré dans le kernel Linux mainline ; celui de Realtek, pour les modèles de haute gamme, reste en forme out-of-tree (en dehors du noyau), et nécessite l'installation manuelle d'un dépôt de pilotes maintenu par la communauté.

## Deuxième acte : Mécanismes - Qu'y a-t-il de différent entre in-kernel et out-of-tree ?

### MediaTek : mt76 en ligne de conduite principale, branché et prêt à l'emploi

Le pilote des puces USB MediaTek est couvert par le sous-système **mt76** du kernel :

| Modèle | SoC | Module de pilote kernel | Conditions sans compilation |
|---|---|---|---|
| AWUS036ACHM | MT7610U | mt76x0u | Kernel intégré, pas de seuil de version |
| AWUS036ACM | MT7612U | mt76x2u | Kernel intégré, pas de seuil de version |
| AWUS036AXML / AXM | MT7921AUN | mt7921u | **Besoin de kernel 5.18+** |

⚠️ Le seul piège : **Le seuil de version du kernel pour MT7921AUN est 5.18+. Les anciens plateformes (comme Jetson Nano avec JetPack 4.x, kernel 4.9) ne peuvent pas être backportées, elles ne sont pas utilisables directement - c'est une conclusion que nous avons vérifiée dans le document technique de Jetson Nano (voir [ALFA Carte réseau sans fil, est-elle compatible avec NVIDIA Jetson Nano](/fr/blog/alfa-nvidia-jetson-nano-compatibility/) §7.4).**

### Realtek : out-of-tree, compilation manuelle sur noyau ancien

Sur un noyau ancien, les puces USB Realtek n'ont pas de pilote principal disponible, et dépendent des dépôts de pilotes maintenus par la communauté. Actuellement, le mainteneur le plus actif est **morrownr**, et ce tableau répertorie 3 puces et 3 dépôts de pilotes :

| Modèle | SoC | Dépôt de pilote (maintenu par morrownr) | Vérification au 3 septembre 2026 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | [8812au-20210820](https://github.com/morrownr/8812au-20210820) | ✅ Vérifié |
| AWUS036EACS | RTL8821CU (intégré depuis le noyau 6.2 ; dépôt nécessaire seulement avant) | [8821cu-20210916](https://github.com/morrownr/8821cu-20210916) | ✅ Vérifié |
| AWUS036AX / AXER | RTL8832BU | [rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | ✅ Vérifié |

### Application à trois environnements typiques

| Environnement | Kernel | Campement MediaTek (3 modèles) | Campement Realtek (3 modèles) |
|---|---|---|---|
| GB10 / DGX Spark et autres plateformes | 6.x + aarch64 | Tous disponibles (mt76 intégré) | Compilation nécessaire seulement sur un noyau ancien (6.17 : tous intégrés ; ARM64 possible) |
| Jetson Nano (JetPack 4.x) | 4.9 | 7610U/7612U disponibles ; MT7921AUN **indisponible** | 8812au peut être compilé (support ARM64) ; les autres non vérifiés |
| Routeur OpenWrt | Selon la version | Tous disponibles (MT7921AUN nécessite 23.05+) | Nécessite le kmod correspondant ou une compilation, niveau de difficulté élevé |

(Voir les matrices de jugement complètes pour chaque environnement dans [ALFA Carte réseau sans fil, est-elle compatible avec NVIDIA DGX Spark](/fr/blog/alfa-nvidia-dgx-spark-compatibility/), [ALFA Carte réseau sans fil, est-elle compatible avec NVIDIA Jetson Nano](/fr/blog/alfa-nvidia-jetson-nano-compatibility/), [ALFA Carte réseau sans fil, est-elle compatible avec OpenWrt](/fr/blog/alfa-openwrt-router-compatibility/).)

## Troisième acte : Boîte à outils - Processus de détermination en trois minutes et étapes d'installation

### Tableau de détermination : Les trois étapes à suivre après avoir récupéré la carte réseau

```bash
# Étape 1 : Vérifiez que le système voit la carte réseau (notez VID:PID)
lsusb

# Étape 2 : Vérifiez si le kernel a chargé le pilote correspondant
lsmod | grep -E "mt76|rtl8"

# Étape 3 : Vérifiez la version du kernel (décide si MT7921AUN peut être utilisé)
uname -r
```

Logique de détermination (matrice principale : les 6 modèles du tableau ci-dessus) :

1. `lsusb` affiche **MediaTek / MT76xx** → camp in-kernel, kernel ≥ 5.18 (modèles MT7921AUN) ou kernel récent, plug and play.
2. `lsusb` affiche **Realtek RTL88xx** → camp out-of-tree, suivre les étapes d'installation suivantes.
3. `lsusb` **ne montre aucune** nouvelle installation → changez de port USB / câble pour exclure les problèmes matériels, puis vérifiez si le modèle est RTL8832BU Wi-Fi 6 (certains lots nécessitent `usb_modeswitch`, cette étape est un problème spécifique à certains modèles et n'est pas inclus dans la matrice de ce guide, ne pas développer davantage).

### Installation universelle pour le camp Realtek (par exemple, AWUS036ACH)

```bash
# Étape 1 : Installez les dépendances de compilation (Debian/Ubuntu)
sudo apt install build-essential dkms linux-headers-$(uname -r)

# Étape 2 : Obtenez le code source du pilote (repo correspondant au modèle, voir le tableau ci-dessus)
git clone https://github.com/morrownr/8812au-20210820
cd 8812au-20210820

# Étape 3 : Installez (enregistrez DKMS, sans avoir à réinstaller après un changement de kernel)
sudo ./install-driver.sh

# Étape 4 : Vérifiez après le redémarrage
lsmod | grep 88XXau
ip link   # Une nouvelle interface wlan devrait apparaître
```

> **Tableau 1 Conclusion : Détermination avant installation - Regardez d'abord le composant, 90 secondes pour décider si vous êtes "plug and play" ou "compilation dans le repo", sans avoir à vous heurter à un mur.**

### Conseils d'achat (phrase conclusive)

- **Pas de compilation nécessaire** : choisissez le camp MediaTek (AWUS036ACHM / ACM / AXML), tous les kernels récents sont plug and play.
- **Wi-Fi 6 et sans compilation** : choisissez AWUS036AXML (MT7921AUN), mais vérifiez d'abord que le kernel ≥ 5.18.
- **Besoin de spéciales fonctionnalités et Realtek est impératif** (comme des outils spécifiques en mode monitor) : prévoyez 20–40 minutes pour compiler le pilote, et vérifiez que la plateforme cible a les en-têtes du kernel.

## Connaissances limitées et conditions de refus

La conclusion de cet article n'est pas valable dans les conditions suivantes, veuillez envisager des solutions de rechange :

1. **kernel 5.17 et inférieur + MT7921AUN** : mt7921u ne peut pas être backporté (dépend des infrastructures du kernel moderne), la conclusion est inversée pour devenir "inutilisable". C'est l'exception la plus importante de cet article.
2. **Non x86/ARM64 Linux** (comme certains routeurs MIPS) : le dépôt morrownr n'est pas garanti pour être compilable, préférez le kmod d'OpenWrt (voir [Est-ce que la carte sans fil ALFA est compatible avec OpenWrt](/fr/blog/alfa-openwrt-router-compatibility/)).
3. **Évolution de la version du dépôt de pilotes** : le dépôt morrownr est nommé par date (par exemple, rtl8852bu-20250826), il pourrait être modifié ou supprimé à l'avenir ; veuillez vous référer à l'état actuel du dépôt avant l'installation.
4. **Capacité en mode monitor / AP** : les capacités varient d'une version de kernel à l'autre pour le même chip (par exemple, rtl8812au-ct dans OpenWrt 22.03+ a des rapports de crash dans 24.10), pour une matrice de capacité détaillée, veuillez vous référer à des articles spécifiques à chaque environnement.
5. **Le RTL8832BU (AWUS036AX/AXER) ne fait pas partie des 6 modèles de cet inventaire, mais le support client est souvent interrogé à son sujet** : le pilote rtw89_8852bu est dans le mainline depuis le noyau 6.17 ; sur le GX10 (noyau 6.17), le mode monitor fonctionne, injection 2,4 GHz : AX 96 %, AXER 73 %. Le pilote communautaire morrownr/rtl8852bu n'est nécessaire que sur les anciens noyaux. Vérifiez d'abord la version du noyau avant de répondre au client.

## Sources de Référence

| Source | Description | URL | État de Vérification | Date de Vérification |
|---|---|---|---|---|
| morrownr/8812au GitHub | Pilote RTL8812AU pour Linux | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |
| morrownr/8821cu GitHub | Pilote RTL8821CU pour Linux (pour les noyaux antérieurs à 6.2) | https://github.com/morrownr/8821cu-20210916 | ✅ Vérifié | 2026-09-03 |
| morrownr/rtl8852bu GitHub | Pilote RTL8832BU pour Linux | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Vérifié | 2026-09-03 |
| Yopitek ALFA Produit Global | Modèles actuels et spécifications | /fr/products/alfa/ | ✅ Vérifié | 2026-09-03 |
| Yopitek Blog : Guide Soft AP | Validation de l'implémentation AP | /fr/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Vérifié | 2026-09-03 |
| Documents Techniques du Site 9 Articles | Matrices de jugement et bases d'validation environnementale | Lien Relatif (voir en haut de l'article « Articles Relatifs ») | ✅ Vérifié | 2026-09-03 |

> Page Wiki Officielle kernel mt76 : https://wireless.wiki.kernel.org/en/users/drivers/mediatek (Vérifié, liste les versions de kernel prises en charge par chaque puce, peut être utilisé comme point de référence rapide)

## Avis de non-responsabilité

Ce document a été rédigé par le service d'assistance technique de Yopitek Ltd ; les spécifications et les états des pilotes peuvent varier en fonction des mises à jour du kernel et des dépôts de pilotes ; veuillez vous référer aux dépôts officiels et aux pages de spécifications du fabricant avant l'installation. ALFA Network est une marque agréée par notre entreprise.
