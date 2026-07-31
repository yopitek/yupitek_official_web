---
title: "Test complet du Sierra EM7455 : pourquoi c'est la carte Sierra préférée des makers et des labos"
description: "Test complet de l'EM7455 : spécifications, différences avec l'EM7430, configuration OpenWrt/Linux, compatibilité Dell et Lenovo. Données techniques compilées par Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em7455", "lte-a", "cat-6", "openwrt", "linux", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM7455_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "L'EM7455 prend-il en charge la 5G ?"
    answer: "Non. C'est un module LTE-A Cat 6 dont la vitesse maximale est de 300 Mbit/s. Pour la 5G, regardez plutôt l'EM9190 ou l'EM9191."
  - question: "Est-ce que l'EM7455 fonctionne à Taïwan ?"
    answer: "Oui, avec les opérateurs taïwanais courants, tant que votre SIM utilise une bande prise en charge. Le niveau de signal réel et l'agrégation de porteuses dépendent de la couverture des antennes, donc discutons de la compatibilité avec vous avant l'achat."
  - question: "Quelle est la différence entre l'EM7455 et le MC7455 ?"
    answer: "Les deux reposent sur le même chipset Qualcomm MDM9230 avec des spécifications identiques. La seule différence, c'est le format : l'EM7455 est en M.2, le MC7455 en mPCIe. Le choix se fait selon votre connecteur."
  - question: "Quelle est la différence entre l'EM7455 et l'EM7430 ?"
    answer: "Ils partagent le même chipset MDM9230 et les mêmes spécifications de base. La différence principale porte sur les bandes couvertes : l'EM7455 couvre les bandes Amériques et EMEA, tandis que l'EM7430 couvre les bandes Asie-Pacifique."
  - question: "Le Dell DW5811e, c'est le même que l'EM7455 ?"
    answer: "Oui. Le DW5811e est la version rebadgée Dell de l'EM7455, basée sur le même chipset Qualcomm MDM9230."
---

# Test complet du Sierra EM7455 : pourquoi c'est la carte Sierra préférée des makers et des labos

Si vous avez déjà bidouillé un Raspberry Pi avec OpenWrt, ou voulu ajouter de la 4G à du matériel de laboratoire, vous avez forcément entendu parler de la carte légendaire Sierra EM7455 ! C'est un module cellulaire LTE-A Cat 6 au format M.2 signé Sierra Wireless, animé par le chipset Qualcomm MDM9230 : jusqu'à 300 Mbit/s en téléchargement et 50 Mbit/s en envoi, un GNSS intégré, et une plage de température de fonctionnement qui encaisse même les environnements extrêmes de -40°C à +85°C.

Cet article, compilé par Yupitek, vous explique pourquoi ce module 4G LTE-Advanced Cat 6 au format M.2 B-Key est si populaire, et comment installer le pilote et la configuration sous Linux.

> Lien produit : [EM7455 — page produit Yupitek](/fr/products/sierra/em7455/) | Fiche technique officielle : [AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## La fiche technique complète de l'EM7455 : tous les chiffres en un coup d'œil

Les chiffres ci-dessous sont extraits de la fiche technique officielle Sierra Wireless. Comme toujours : si vous commandez pour un vrai projet, demandez-nous d'abord le document officiel le plus récent, surtout pour les éléments qui évoluent dans le temps comme les bandes ou les versions de firmware.

| Élément | Spécification |
|---|---|
| **Modèle** | AirPrime EM7455 |
| **Standard cellulaire** | LTE-A Cat 6 |
| **Chipset** | Qualcomm MDM9230 (Snapdragon X7 LTE) |
| **Débit descendant de pointe** | 300 Mbit/s (LTE-A, 2×CA) |
| **Débit montant de pointe** | 50 Mbit/s (LTE-A) |
| **Agrégation de porteuses** | 2×CA (plusieurs combinaisons, voir la référence officielle des commandes AT) |
| **Format** | PCI Express M.2 B-Key (52 broches) |
| **Dimensions** | 42 × 30 × 2.3 mm |
| **Température de fonctionnement** | -40°C ~ +85°C (grade industriel) |
| **GNSS** | GPS, GLONASS, BeiDou, Galileo |
| **Interface hôte** | USB 3.0 / USB 2.0 High Speed |
| **Bandes LTE** | Bandes courantes Amériques et EMEA (Europe/Moyen-Orient/Afrique) ; confirmez la liste complète des bandes sur la fiche technique officielle la plus récente |
| **Bandes 3G WCDMA** | À confirmer sur la fiche technique officielle la plus récente |
| **VID:PID générique** | `1199:9079` (EM7455, version standard) |
| **VID:PID Dell DW5811e** | `413c:81b6` (version de marque ; vérifiez avec `lsusb` sur votre appareil) |
| **Pilotes Linux** | `qcserial`, `qmi_wwan`, `cdc_mbim` (intégrés à la plupart des distributions courantes) |
| **Firmware générique** | Utilisez la dernière version sur le site officiel source.sierrawireless.com |
| **Certifications opérateurs** | Variables selon la région (ex. AT&T, Verizon, Vodafone) ; confirmez la liste à jour avec nous |

---

## Pour quels projets l'EM7455 est-il fait ?

**En résumé, l'EM7455 est le sauveur de trois cas classiques : (1) monter un routeur 4G LTE sur firmware open source comme OpenWrt ou ROOter, (2) upgrader la carte WWAN d'un laptop Dell ou Lenovo, (3) construire des passerelles IoT ou des trackers télématiques dans des labos industriels.**

Son plus grand atout, c'est un écosystème de pilotes Linux très mature, des tonnes de tutoriels communautaires et une large couverture de bandes.

### Si vous êtes maker ou étudiant

| Cas d'usage | Montage conseillé | Pourquoi ce choix |
|---|---|---|
| Routeur 4G sur Raspberry Pi | Raspberry Pi 4/5 + adaptateur M.2 vers USB + OpenWrt / ROOter | Support communautaire OpenWrt ultra stable, paquet `uqmi` solide |
| Upgrade de routeur GL.iNet | GL-MT1300 / GL-AR750S + adaptateur USB | Les discussions communautaires sur `create_connect.sh` pour ROOter se pompent facilement |
| Hotspot LTE portable outdoor | Alimentation batterie + adaptateur USB + mini-routeur | Faible dégagement de chaleur, bon comportement thermique, idéal pour le tracking d'objets en extérieur |

### Pour les projets entreprise ou industriels

| Cas d'usage | Montage conseillé | Pourquoi ce choix |
|---|---|---|
| Routeur industriel | Passerelle industrielle avec slot M.2 (ex. Advantech) | Robuste, plage de température -40~85°C rassurante, assez de bandes |
| Télématique / flotte | Passerelle véhicule + antenne GNSS | Géolocalisation GPS/GLONASS intégrée : connexion et position sur une seule carte |
| Upgrade WWAN de laptop | Dell Latitude / Lenovo ThinkPad | Le M.2 B-Key se branche direct ; Linux le détecte souvent en plug-and-play |
| WAN de secours | OpenWrt / pfSense en double WAN | Compatible mode double QMI/MBIM (le support pfSense est aléatoire, OpenWrt est plus sûr) |

---

## EM7455 vs EM7430 : qu'est-ce qui change vraiment ?

On nous pose très souvent cette question. En réalité, **l'EM7455 et l'EM7430 utilisent exactement le même chipset Qualcomm MDM9230, donc les spécifications de base (Cat 6, 300/50 Mbit/s, 2×CA, GNSS) sont identiques. La vraie différence tient aux bandes ciblées par chaque modèle.** L'EM7455 vise l'Amérique et l'EMEA (Europe/Moyen-Orient/Afrique), tandis que l'EM7430 vise la région Asie-Pacifique (APAC).

| Élément | EM7455 | EM7430 |
|---|---|---|
| **Chipset** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **Standard cellulaire** | LTE-A Cat 6 | LTE-A Cat 6 |
| **Débit descendant de pointe** | 300 Mbit/s | 300 Mbit/s |
| **Débit montant de pointe** | 50 Mbit/s | 50 Mbit/s |
| **Agrégation de porteuses** | 2×CA | 2×CA |
| **Format** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **Région cible** | Amériques, EMEA | Asie-Pacifique (APAC) |

**Petit conseil de sélection :** si les SIM de votre projet ou de vos appareils sont utilisées surtout en Amérique du Nord ou en Europe, prenez l'**EM7455** ; dans la région Asie-Pacifique (Taïwan, Japon, Australie), l'**EM7430** est théoriquement plus adapté. Comme la répartition des bandes des opérateurs taïwanais est particulière, demandez-nous avant de commander quelle carte s'accorde le mieux avec votre opérateur.

---

## EM7455 vs MC7455 : des puces identiques, juste des connecteurs différents

Comme dit plus haut, l'EM7455 (M.2) et le MC7455 (mPCIe) utilisent le même Qualcomm MDM9230, avec des spécifications électriques strictement identiques. La seule différence, c'est la « peau », c'est-à-dire le format :

| Élément | EM7455 | MC7455 |
|---|---|---|
| **Format** | M.2 (B-Key) | Mini PCIe (mPCIe) |
| **Dimensions** | 42 × 30 × 2.3 mm | 51 × 30 × 3.5 mm |
| **Mieux adapté à** | Slots WWAN de laptop, cartes de dev modernes | Slots mPCIe des PC industriels plus anciens |
| **VID:PID générique** | `1199:9079` | `1199:9071` |

**Simple : choisissez la carte qui correspond au connecteur de votre appareil.** Si vous vous trompez, une carte adaptatrice (M.2 vers mPCIe, ou l'inverse) rattrape généralement le coup.

---

## Comment la configurer sous Linux ? (Ubuntu / Debian / Linux Mint)

L'EM7455 est très bien supporté sur les systèmes Linux courants. Voici les étapes de base utilisées par la communauté. Rappelez-vous : chaque machine a sa version d'OS et de kernel, donc testez d'abord sur une machine hors production.

### Étape 1 : vérifier que le matériel est détecté

```bash
lsusb | grep -i sierra
# Vous devriez voir un résultat du type : Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### Étape 2 : installer les outils nécessaires

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### Étape 3 : passer le mode USB en QMI

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# Vérifier que le changement de mode a réussi
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# Vous devriez voir : USB composition 6: DM, NMEA, AT, QMI
```

> Si votre opérateur impose le mode MBIM, cherchez la commande `AT!USBCOMP` et connectez-vous avec `mbimcli` à la place.

### Étape 4 : déverrouiller l'authentification FCC

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# Pour une prise en charge 100 % automatique via ModemManager :
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### Étape 5 : se connecter via NetworkManager

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn 'VOTRE_APN'
sudo nmcli connection up 'EM7455 LTE'
```

### Étape 6 : connexion QMI manuelle (pour le dépannage avancé)

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='VOTRE_APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## Configurer QMI sous OpenWrt

L'EM7455 a très bonne réputation dans la communauté OpenWrt. Si vous avez un routeur flashé en OpenWrt, voici la configuration QMI standard.

### Installer les paquets nécessaires

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### Modifier la configuration réseau

Ouvrez `/etc/config/network` et ajoutez ce bloc d'interface :

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'VOTRE_APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### Redémarrer le réseau

```bash
/etc/init.d/network restart
```

Si vous préférez cliquer (interface web LuCI) : allez dans « Network » → « Interfaces », ajoutez une nouvelle interface, choisissez le protocole « QMI », sélectionnez `/dev/cdc-wdm0` et renseignez votre APN, c'est réglé.

> Astuce pour les utilisateurs de Raspberry Pi : essayez ROOter (un firmware basé sur OpenWrt, spécialisé dans le routage 4G/5G) — il embarque déjà beaucoup de hooks de configuration bien pratiques.

---

## Compatibilité avec les laptops de marque : Dell et Lenovo

### Laptops Dell (cette carte s'appelle DW5811e)

On voit souvent le Dell DW5811e en ligne. C'est en fait l'EM7455 rebadgé par Dell (VID `413c`, PID `81b6`), avec le même chipset MDM9230 à l'intérieur, et la plupart des pilotes Linux `qmi_wwan` le reconnaissent depuis longtemps.

```bash
lsusb | grep 413c
# Vous devriez voir un résultat du type : Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

Bonne nouvelle : d'après les retours de la communauté, la plupart des laptops Dell (Latitude, Precision, etc.) n'imposent pas de liste blanche BIOS pénible, donc la carte fonctionne généralement dès l'insertion.

### Laptops Lenovo (la fameuse liste blanche)

Avec un Lenovo ThinkPad, attention. Lenovo impose parfois une liste blanche BIOS qui n'accepte que les cartes FRU d'origine Lenovo. Certains membres de forums ont partagé des commandes AT qui contournent la restriction, pour les plus aventureux :

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **Attention : ces commandes viennent de forums. Mal exécutées, elles peuvent transformer votre carte en brique !** Si vous n'êtes pas un joueur avancé qui aime démonter du matériel et assumer les risques, demandez-nous des alternatives plus sûres avant de commander.

---

## Quelles plateformes sont prises en charge ? Tout dans un tableau

| Votre plateforme | Niveau de support | Méthode de connexion | Remarque |
|---|---|---|---|
| Raspberry Pi + OpenWrt | ✅✅ ultra stable, beaucoup de tutoriels | QMI / MBIM | Il faut une petite carte adaptatrice M.2 vers USB |
| Raspberry Pi + ROOter | ✅✅ | QMI | Vivement recommandé pour les utilisateurs de Pi |
| Ubuntu / Debian | ✅✅ | ModemManager / QMI | Très forte probabilité de plug-and-play |
| DD-WRT | ⚠️ coup de chance | QMI / PPP | Peu de discussions communautaires, pas pour les débutants |
| pfSense | ⚠️ très aléatoire | QMI / PPP | Évaluez plutôt OpenWrt, moins de prise de tête |
| Laptops Dell | ✅ | QMI / MBIM | Linux les détecte quasi systématiquement |
| Laptops Lenovo | ⚠️ peut demander un contournement | QMI | Méfiez-vous de la liste blanche BIOS, les commandes à l'aveugle risquent la brique |

---

## Où trouver d'autres ressources ?

Si vous bloquez sur un projet, ces communautés open source valent le détour :

- **GitHub de danielewood** : scripts et discussions très complets sur l'EM7455/MC7455.
- **Gentoo Wiki** : une base de dépannage très détaillée tenue par la communauté Linux.
- **OpenWrt LTE Wiki** : la documentation officielle, à lire avant de configurer votre réseau.

## Questions fréquentes

{{< faq >}}

---

## Vous achetez pour un labo ? Parlez-nous-en

Cet article a été compilé par l'équipe d'ingénierie de Yupitek. Que ce soit pour un projet universitaire, un programme de laboratoire ou un achat en volume en entreprise de l'EM7455 ou d'autres modules Sierra, venez en discuter avec nous !

- **Voir la carte** : [https://yupitek.com/fr/products/sierra/em7455/](/fr/products/sierra/em7455/)
- **Voir tous les modèles Sierra** : [https://yupitek.com/fr/products/sierra/](/fr/products/sierra/)
- **Nous écrire** : sales@yupitek.com
