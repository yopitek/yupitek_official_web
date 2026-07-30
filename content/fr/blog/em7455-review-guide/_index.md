---
title: "Test complet de l'EM7455 : pourquoi c'est la carte Sierra préférée des makers et des ingénieurs"
date: 2026-07-30
slug: "em7455-review-guide"
tags:
  - em7455
  - sierra-wireless
  - lte-a
  - cat6
  - m2
  - gnss
  - openwrt
  - linux
categories:
  - Test produit
series:
  - sierra-wireless-selection
series_order: 2
description: "Test complet de l'EM7455 : spécifications, différences avec l'EM7430, configuration OpenWrt/Linux, compatibilité Dell/Lenovo. Documentation technique fournie par Yupitek."
author: "yupitek"
draft: false
faq:
  - question: "Est-ce que l'EM7455 supporte la 5G ?"
    answer: "Non. L'EM7455 est un module LTE-A Cat 6 avec un maximum de 300 Mbps. Si tu as besoin de 5G (Sub-6 ou mmWave), regarde du côté de l'EM9190 (Sub-6) ou de l'EM9191 (Sub-6 + mmWave)."
  - question: "Est-ce que l'EM7455 fonctionne à Taïwan ?"
    answer: "D'une manière générale, le module est compatible avec les cartes SIM des principaux opérateurs taïwanais. La qualité réelle du signal et les bandes disponibles dépendent de l'emplacement des stations de base, de la planification réseau de l'opérateur et du support de l'agrégation de porteuses. Nous te recommandons de vérifier la compatibilité avec ta région et ton opérateur avant de commander."
  - question: "Quelle est la différence entre l'EM7455 et le MC7455 ?"
    answer: "La puce est la même — Qualcomm MDM9230, spécifications identiques. La seule différence est le format : l'EM7455 est en M.2, le MC7455 en mPCIe. Le choix dépend uniquement de ton connecteur."
  - question: "Quelle est la différence entre l'EM7455 et l'EM7430 ?"
    answer: "Même puce Qualcomm MDM9230, mêmes spécifications de base. La différence principale réside dans les bandes de fréquences cibles : l'EM7455 couvre principalement les bandes des Amériques et de l'EMEA, tandis que l'EM7430 couvre celles de l'Asie-Pacifique (APAC). Consulte la fiche technique officielle la plus récente pour la liste détaillée des bandes."
  - question: "Est-ce que le Dell DW5811e est identique à l'EM7455 ?"
    answer: "Oui, le DW5811e est la version de marque Dell de l'EM7455, basée sur la même puce Qualcomm MDM9230. La plupart des retours de la communauté Dell indiquent qu'il n'y a pas de blocage par whitelist BIOS, mais nous te recommandons de vérifier sur ton modèle spécifique."
---

L'EM7455 est un module cellulaire LTE-A Cat 6 au format M.2 de Sierra Wireless, équipé de la puce Qualcomm MDM9230, prenant en charge jusqu'à 300 Mbps en téléchargement et 50 Mbps en upload, avec un GNSS intégré et une plage de température de fonctionnement de -40°C à +85°C. Cet article a été préparé par Yupitek pour fournir les spécifications techniques et les références de configuration.

Le Sierra Wireless EM7455 est un module 4G LTE-Advanced Cat 6 au format M.2 B-Key, largement utilisé dans les routeurs OpenWrt, les stations de base mobiles Raspberry Pi, les passerelles industrielles et les WWAN de notebooks professionnels. Les étapes ci-dessous sont des procédures courantes issues de la communauté et de la documentation officielle — vérifie les commandes en fonction de ta version de système d'exploitation et de firmware, et fais une sauvegarde de ta configuration actuelle avant de les exécuter.

> Lien produit : [EM7455 — Page produit Yupitek](https://yupitek.com/zh-tw/products/sierra/em7455/) | Fiche technique officielle : [AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## Tableau des spécifications complètes de l'EM7455

Les spécifications ci-dessous sont compilées à partir de la fiche technique officielle de Sierra Wireless et de sources publiques. Avant de passer commande, nous te recommandons de demander les documents officiels les plus récents pour une vérification détaillée, en particulier pour les bandes de fréquences et les versions de firmware qui peuvent évoluer dans le temps.

| Paramètre | Spécification |
|---|---|
| **Modèle** | AirPrime EM7455 |
| **Standard cellulaire** | LTE-A Cat 6 |
| **Puce** | Qualcomm MDM9230 (Snapdragon X7 LTE) |
| **Débit descendant max** | 300 Mbps (LTE-A, 2×CA) |
| **Débit montant max** | 50 Mbps (LTE-A) |
| **Agrégation de porteuses** | 2×CA (prend en charge diverses combinaisons, voir la référence officielle des commandes AT) |
| **Format** | PCI Express M.2 B-Key (52 broches) |
| **Dimensions** | 42 × 30 × 2,3 mm |
| **Température de fonctionnement** | -40°C ~ +85°C (classe industrielle) |
| **GNSS** | GPS, GLONASS, BeiDou, Galileo |
| **Interface de communication** | USB 3.0 / USB 2.0 High Speed |
| **Bandes LTE** | Couvre les principales bandes des Amériques et de l'EMEA (Europe/Moyen-Orient/Afrique). Liste détaillée dans la fiche technique officielle la plus récente |
| **Bandes 3G WCDMA** | Voir la fiche technique officielle la plus récente |
| **VID:PID générique** | `1199:9079` (EM7455, version standard) |
| **Dell DW5811e VID:PID** | `413c:81b6` (version de marque, à vérifier avec `lsusb` sur ton appareil) |
| **Pilotes Linux** | `qcserial`, `qmi_wwan`, `cdc_mbim` (intégrés dans les distributions courantes ; la version minimale du noyau dépend de ta distribution) |
| **Firmware standard** | Utilise la dernière version sur source.sierrawireless.com. Cet article ne spécifie pas de version particulière pour éviter l'obsolescence |
| **Certification opérateur** | Varie selon l'opérateur et la région (AT&T, Verizon, T-Mobile, Bell, Rogers, Telus, Vodafone, etc.). Demande la liste de certification la plus récente pour ta région |

---

## À quoi sert l'EM7455 ?

**L'EM7455 est idéal pour trois cas d'usage : (1) construire ton propre routeur 4G LTE (OpenWrt / ROOter), (2) mettre à niveau le WWAN d'un notebook (Dell / Lenovo), (3) les passerelles IoT industrielles et la télématique embarquée.** Ses principaux atouts sont la maturité des pilotes Linux, la richesse des ressources communautaires et la large couverture des bandes pour les Amériques et l'EMEA.

### Scénarios Maker

| Application | Configuration | Raison |
|---|---|---|
| Routeur 4G Raspberry Pi | Raspberry Pi 4/5 + adaptateur M.2→USB + OpenWrt / ROOter | L'EM7455 montre une compatibilité stable dans la communauté OpenWrt, le paquet uqmi est mature |
| Mise à niveau routeur GL.iNet | GL-MT1300 / GL-AR750S + adaptateur USB | Des discussions communautaires sur les hooks ROOter et `create_connect.sh` sont disponibles |
| Point d'accès LTE portable | Alimentation batterie + adaptateur USB + mini-routeur | L'EM7455 dégage peu de chaleur et dissipe bien, idéal pour le suivi d'objets |

### Scénarios entreprise / industrie

| Application | Configuration | Raison |
|---|---|---|
| Routeur industriel | Passerelle industrielle avec slot M.2 (Advantech, Cincoze) | Large plage de température -40~85°C, couverture étendue des bandes |
| Télématique embarquée | Passerelle véhicule + antenne GNSS | GPS/GLONASS/BeiDou/Galileo intégrés — un seul module pour connectivité et géolocalisation |
| Mise à niveau WWAN notebook | Dell Latitude / Precision / Lenovo ThinkPad | Installation directe dans le slot M.2 B-Key, excellente compatibilité des pilotes Linux |
| WAN de secours | OpenWrt / pfSense double WAN de secours | Support des modes QMI et MBIM, mais la compatibilité pfSense est plus limitée — OpenWrt est recommandé en priorité |

---

## Quelle est la différence entre l'EM7455 et l'EM7430 ?

**L'EM7455 et l'EM7430 utilisent la même puce Qualcomm MDM9230 — les spécifications de base sont identiques (Cat 6, 300/50 Mbps, 2×CA, GNSS). La différence principale réside dans les bandes de fréquences cibles : l'EM7455 couvre principalement les bandes des Amériques et de l'EMEA, tandis que l'EM7430 couvre celles de l'Asie-Pacifique (APAC).**

| Paramètre | EM7455 | EM7430 |
|---|---|---|
| **Puce** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **Standard cellulaire** | LTE-A Cat 6 | LTE-A Cat 6 |
| **Débit descendant max** | 300 Mbps | 300 Mbps |
| **Débit montant max** | 50 Mbps | 50 Mbps |
| **Agrégation de porteuses** | 2×CA | 2×CA |
| **Format** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **Région cible** | Amériques, EMEA (Europe/Moyen-Orient/Afrique) | APAC (Asie-Pacifique) |
| **Liste détaillée des bandes** | Voir la fiche technique officielle la plus récente | Voir la fiche technique officielle la plus récente |

> La répartition précise bande par bande des deux modules est à consulter dans la dernière fiche technique officielle — nous ne listons pas les numéros de bandes ici pour éviter qu'ils ne deviennent obsolètes ou inexacts. Si tu connais ton opérateur et les bandes de fréquences nécessaires, n'hésite pas à nous contacter pour déterminer le module le plus adapté.

**Recommandation de choix** : si ton opérateur SIM est principalement basé en Amérique du Nord ou en Europe, privilégie l'**EM7455** ; si tu utilises surtout des opérateurs de la région Asie-Pacifique (Taïwan, Japon, Australie, etc.), l'**EM7430** est plus adapté. Pour le marché taïwanais, en raison de la configuration des bandes des opérateurs locaux, nous te recommandons de vérifier tes besoins réels en bandes avant de commander.

---

## EM7455 vs MC7455 : même puce, seul le format change

L'EM7455 (M.2) et le MC7455 (mPCIe) utilisent la même puce Qualcomm MDM9230 — leurs caractéristiques électriques de base sont identiques. La différence principale est **l'interface de format** :

| Paramètre | EM7455 | MC7455 |
|---|---|---|
| **Format** | M.2 (B-Key) | Mini PCIe (mPCIe) |
| **Dimensions** | 42 × 30 × 2,3 mm | 51 × 30 × 3,5 mm |
| **Appareils compatibles** | Slot WWAN notebook, cartes mères M.2 modernes | Slots mPCIe des routeurs industriels anciens |
| **VID:PID générique** | `1199:9079` | `1199:9071` |

**Le choix dépend uniquement du connecteur de ton appareil.** Si ta carte mère n'a que du M.2, choisis l'EM7455 ; si elle n'a que du mPCIe, choisis le MC7455. En cas de mauvais choix, tu peux utiliser un adaptateur (M.2→mPCIe ou mPCIe→M.2).

---

## Configuration Linux (Ubuntu / Debian / Linux Mint)

L'EM7455 bénéficie d'une bonne compatibilité avec les pilotes des principales distributions Linux. Voici les étapes de configuration courantes issues de la communauté — selon ton environnement (version de la distribution, version du noyau, version du firmware), des différences peuvent apparaître. Nous te recommandons de valider d'abord dans un environnement de test avant de passer en production.

### Étape 1 : Détection matérielle

```bash
lsusb | grep -i sierra
# Sortie attendue : Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### Étape 2 : Installation des outils

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### Étape 3 : Passage en mode composite USB QMI

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# Vérification du mode composite
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# Résultat attendu : USB composition 6: DM, NMEA, AT, QMI
```

> Si tu as besoin uniquement du mode MBIM (exigé par certains opérateurs), consulte les paramètres `AT!USBCOMP` et utilise `mbimcli`. Les valeurs exactes sont dans la référence officielle des commandes AT.

### Étape 4 : Déverrouillage FCC Auth

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# Pour utiliser l'automatisation intégrée de ModemManager :
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### Étape 5 : Connexion avec NetworkManager

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn 'TON_APN'
sudo nmcli connection up 'EM7455 LTE'
```

### Étape 6 : Connexion QMI manuelle (avancé / dépannage)

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='TON_APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## Configuration OpenWrt QMI

L'EM7455 est l'un des modèles les mieux compatibles avec OpenWrt selon la communauté. Voici un exemple de configuration de base pour le mode QMI.

### Installation des paquets

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### Modification du fichier de configuration réseau

Modifie `/etc/config/network` et ajoute l'interface suivante :

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'TON_APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### Redémarrage du réseau

```bash
/etc/init.d/network restart
```

Avec l'interface web LUCI : Réseau → Interfaces → Ajouter une nouvelle interface → protocole « QMI », périphérique `/dev/cdc-wdm0`, renseigner l'APN.

> ROOter (un firmware pour routeurs cellulaires basé sur OpenWrt) dispose d'un support communautaire pour les modules Sierra QMI avec des hooks `create_connect.sh` intégrés. Si tu utilises un Raspberry Pi, tu peux envisager d'utiliser directement le firmware ROOter — consulte la documentation officielle de ROOter pour la liste de compatibilité.

---

## Compatibilité des marques : notebooks Dell / Lenovo

### Notebooks Dell (le DW5811e correspond à l'EM7455)

Le Dell DW5811e est la version de marque Dell de l'EM7455 (VID `413c`, PID `81b6`), basée sur la même puce Qualcomm MDM9230. Le pilote `qmi_wwan` des principales distributions Linux contient déjà les ID de nombreuses versions de marque ; la nécessité de configurations supplémentaires est à déterminer par un test pratique :

```bash
lsusb | grep 413c
# Sortie attendue : Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

Selon la communauté, la plupart des modèles Dell (Latitude, Precision, XPS) n'ont pas de whitelist BIOS — le DW5811e peut généralement être installé directement. Les conditions réelles peuvent toutefois varier selon le modèle et la version du BIOS, donc vérifie sur ton appareil spécifique.

### Notebooks Lenovo (FRU EM7455)

La communauté fait état de restrictions de whitelist BIOS sur les Lenovo ThinkPad — certains modèles ne reconnaissent que les modules avec FRU Lenovo. Voici un exemple de commandes AT discutées dans la communauté pour tenter de contourner cette limitation :

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **Nous n'avons pas vérifié individuellement la source et l'exactitude de ces commandes. Elles concernent des opérations de bas niveau qui modifient le comportement du firmware du module, et une exécution incorrecte peut rendre le module inutilisable (ce qu'on appelle « briquer » le module). Cet exemple est tiré de discussions publiques de la communauté et ne constitue pas une procédure standard validée par Yupitek. Si tu souhaites essayer, nous te recommandons vivement de : sauvegarder la version actuelle du firmware, n'opérer que dans un environnement non critique, et assumer tous les risques. En cas de doute, contacte-nous pour discuter de tes besoins et des solutions possibles.**

### Modèles ThinkPad (signalés par la communauté pour ce type de configuration)

La liste ci-dessous est basée sur des discussions de la communauté. La compatibilité réelle et la nécessité de mises à jour BIOS/firmware dépendent des spécifications officielles et de la version du BIOS de ton appareil. Avant d'acheter, nous te recommandons de nous contacter ou de te renseigner auprès du support officiel Lenovo :

- Série 60 : T460 / T460s / T460p / T560 / X260 / X1 Carbon 4th Gen / X1 Yoga 1st Gen
- Série 70 : T470 / T480 / T570 / T580 / X270 / X280 / X1 Carbon 5th/6th Gen / P51 / P52

---

## Aperçu de la compatibilité des plateformes

| Plateforme | Support | Type de connexion | Remarques |
|---|---|---|---|
| Raspberry Pi + OpenWrt | ✅✅ Nombreux exemples communauté | QMI / MBIM | Adaptateur M.2→USB requis |
| Raspberry Pi + ROOter | ✅✅ | QMI (hooks communauté intégrés) | Recommandé pour les utilisateurs Raspberry Pi |
| Ubuntu/Debian/Linux Mint | ✅✅ | ModemManager / QMI | Bon support pilotes dans les distributions courantes |
| DD-WRT | ⚠️ Support limité | QMI / PPP | Nécessite une version BETA récente, communauté restreinte |
| pfSense / FreeBSD | ⚠️ Support limité | QMI / PPP (surtout via commandes AT) | Pilotes cellulaires FreeBSD natifs limités — évaluation au cas par cas |
| Dell (DW5811e) | ✅ | QMI / MBIM | Reconnu par la plupart des distributions courantes ; tester sur certains modèles |
| Lenovo | ⚠️ Configuration supplémentaire requise | QMI | Restriction whitelist BIOS sur certains modèles — voir remarques ci-dessus |

---

## Ressources communautaires et lectures complémentaires

Voici des ressources communautaires et officielles accessibles au public pour approfondir l'étude de l'EM7455 :

- **danielewood/sierra-wireless-modems** : Scripts de configuration et discussions sur l'EM7455/MC7455 : [GitHub](https://github.com/danielewood/sierra-wireless-modems)
- **Gentoo Wiki — Sierra EM7455 (Dell DW5560)** : Compilation communautaire pour la configuration Linux (incluant options du noyau, mise à jour du firmware, dépannage) : [Wiki](https://wiki.gentoo.org/wiki/Sierra_EM7455_(Dell_wireless_modem_DW5560))
- **OpenWrt LTE Wiki** : Liste officielle des modems LTE supportés et guides : [OpenWrt LTE Guide](https://openwrt.org/docs/guide-user/network/wan/wwan/ltedongle)
- **bkerler/SierraWirelessGen** : Outils en mode ingénierie, potentiellement pour les paramètres PRI et bandes : [GitHub](https://github.com/bkerler/SierraWirelessGen)

> Les ressources tierces ci-dessus ne sont pas maintenues par nous — vérifie leur exactitude et leur actualité avant de les utiliser.

---

## Foire aux questions (FAQ)

**Question 1 : Est-ce que l'EM7455 supporte la 5G ?**
Non. L'EM7455 est un module LTE-A Cat 6 avec un maximum de 300 Mbps. Si tu as besoin de 5G (Sub-6 ou mmWave), regarde du côté de l'EM9190 (Sub-6) ou de l'EM9191 (Sub-6 + mmWave).

**Question 2 : Est-ce que l'EM7455 fonctionne à Taïwan ?**
D'une manière générale, le module est compatible avec les cartes SIM des principaux opérateurs taïwanais. La qualité réelle du signal et les bandes disponibles dépendent de l'emplacement des stations de base, de la planification réseau de l'opérateur et du support de l'agrégation de porteuses. Nous te recommandons de vérifier la compatibilité avec ta région et ton opérateur avant de commander.

**Question 3 : Quelle est la différence entre l'EM7455 et le MC7455 ?**
La puce est la même — Qualcomm MDM9230, spécifications identiques. La seule différence est le format : l'EM7455 est en M.2, le MC7455 en mPCIe. Le choix dépend uniquement de ton connecteur.

**Question 4 : Que faire si l'EM7455 n'est pas détecté sous Ubuntu ?**
Vérifie d'abord si `1199:9079` apparaît dans la sortie de `lsusb`. Sinon, essaie un port USB 2.0 (dans certains cas, l'USB 3.0 peut causer des interférences). Assure-toi ensuite que `qcserial` et `qmi_wwan` sont chargés : exécute `lsmod | grep qmi`. Tu peux aussi arrêter ModemManager (`systemctl stop ModemManager`) et exécuter `qmicli` manuellement pour le diagnostic. Si le problème persiste, contacte-nous pour obtenir de l'aide.

**Question 5 : Est-ce que le Dell DW5811e est identique à l'EM7455 ?**
Oui, le DW5811e est la version de marque Dell de l'EM7455, basée sur la même puce Qualcomm MDM9230. La version Dell est largement disponible sur le marché de l'occasion et généralement moins chère. La plupart des retours de la communauté Dell indiquent qu'il n'y a pas de blocage par whitelist BIOS, mais nous te recommandons de vérifier sur ton modèle spécifique.

---

## Contact pour les achats

Les spécifications et informations de configuration de l'EM7455 ci-dessus ont été préparées par Yupitek. Pour acheter l'EM7455, l'EM7430, le MC7455 ou toute la gamme de modules cellulaires Sierra Wireless, consulte la page produit ou contacte notre équipe technique.

- **Page produit** : [https://yupitek.com/zh-tw/products/sierra/em7455/](https://yupitek.com/zh-tw/products/sierra/em7455/)
- **Toute la gamme** : [https://yupitek.com/zh-tw/products/sierra/](https://yupitek.com/zh-tw/products/sierra/)
- **Email** : sales@yupitek.com
