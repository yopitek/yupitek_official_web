---
title: "Guide complet d'installation des modules Sierra 4G/5G sur Ubuntu / Debian / Linux Mint : configuration EM7455, EM7565, EM919x, MC7455 et positionnement GNSS | Yupitek"
description: "Comment installer un module Sierra 4G/5G sur Ubuntu/Debian/Linux Mint ? Ce guide t'accompagne dans l'installation de ModemManager, la connexion avec qmicli/mbimcli et la configuration du positionnement GNSS. Couvre EM7455, EM7565, EM919x et MC7455."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "fr"
hreflang_group: "ubuntu-debian-sierra-4g-5g-setup-guide"
slug: "ubuntu-debian-sierra-4g-5g-setup-guide"
tags: ["Sierra Wireless", "Ubuntu", "Debian", "Linux", "GNSS"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/fr/products/sierra/"
faq:
  - question: "Peut-on utiliser directement un module Sierra 4G/5G sous Ubuntu pour se connecter à internet ?"
    answer: "Oui. Installe les paquets modemmanager, libqmi-utils et les paquets associés, puis renseigne ton APN dans NetworkManager et tu es en ligne."
  - question: "Comment activer le positionnement GNSS d'un module Sierra sous Linux ?"
    answer: "Utilise les commandes ModemManager : lance d'abord mmcli -m 0 --location-enable-gps-raw, puis récupère les coordonnées avec --location-get. Assure-toi que l'antenne GNSS est bien branchée."
---

Tu veux installer un module Sierra Wireless (EM7455, EM7565, MC7455, EM919x) sur Ubuntu, Debian ou Linux Mint ? Linux prend en charge ces périphériques nativement. Tu as juste besoin de savoir quels paquets installer, comme ModemManager et libqmi-utils. Cet article couvre tout, étape par étape : du branchement du matériel et de l'installation des pilotes, jusqu'à la mise en ligne et l'activation du positionnement GNSS. Que tu montes un drone ou un PC industriel, suis le guide et tu y arriveras.

{{< tldr >}}
Tu veux installer un module Sierra Wireless (EM7455, EM7565, MC7455, EM919x) sur Ubuntu, Debian ou Linux Mint ? Linux prend en charge ces périphériques nativement. Installe juste les bons paquets, ModemManager et libqmi-utils. Du branchement matériel et des pilotes à la connexion et au GNSS, le guide fonctionne pour les drones comme pour les PC industriels.
{{< /tldr >}}

**En une phrase : installer ces modules Sierra sous Linux est un jeu d'enfant. Installe `modemmanager` et les outils associés avec `apt`, connecte-toi via NetworkManager, et tu peux même lire les positions GPS sans transpirer.**

Beaucoup reçoivent un EM7455, EM7565, EM919x ou MC7455, le branchent sur la carte mère, puis ne savent pas comment se connecter. En réalité, la prise en charge de ces modules sous Linux est très mature. Ils communiquent tous via USB, avec les protocoles QMI ou MBIM. Dans ce guide, on te fait faire la configuration pas à pas.

> Toutes les spécifications et références techniques proviennent de la documentation officielle Sierra Wireless. Compilé par Yupitek.

---

## Avant de commencer : connais ton matériel

Si le matériel est faux, aucune commande logicielle n'y fera rien.

| Module | Format | Classe de vitesse | Protocole Linux principal | Nombre d'antennes |
|---|---|---|---|---|
| **EM7455** | M.2 (42 mm de long) | Cat 6 (300/50 Mbit/s) | QMI | 3 (Main, GNSS, Aux) |
| **EM7565** | M.2 (42 mm de long) | Cat 12 (600/150 Mbit/s) | QMI / MBIM | 3 (Main, GNSS, Aux) |
| **EM919x** (5G) | M.2 (**52 mm** de long) | 5G NR / LTE Cat 20 | MBPW et autres packs large bande | 4 ou plus |
| **MC7455** | mPCIe (slot ancien) | Cat 6 (300/50 Mbit/s) | QMI | 3 connecteurs U.FL |

**Deux pièges matériels à retenir :**
1. **L'EM919x est plus long** : avec ses 52 mm, il ne rentre pas dans un slot de 42 mm. Le forcer endommagerait la carte.
2. **Pas d'antenne, pas de signal** : au minimum, branche l'antenne principale (Main). Pour la géolocalisation, achète une antenne GPS et branche-la sur le connecteur dédié **GNSS**.

---

## Étape 1 : installer les outils Linux indispensables

Sous Ubuntu / Debian / Linux Mint, inutile d'écrire ou de compiler des pilotes toi-même. Les dépôts de paquets ont tout prévu.

Ouvre un terminal et lance ces deux lignes :
```bash
sudo apt update
sudo apt install modemmanager libqmi-utils libmbim-utils
```
Après l'installation, vérifie que le service tourne :
```bash
systemctl status ModemManager
```
Avec ces outils, ton Linux comprend la carte 4G/5G.

---

## Étape 2 : vérifier que le système voit la carte

Carte installée, machine démarrée, lance ces trois commandes pour contrôler :

1. **Vérifier le matériel USB :**
   ```bash
   lsusb
   ```
   (Tu devrais voir un périphérique Sierra ou Qualcomm.)

2. **Vérifier le pilote du noyau :**
   ```bash
   dmesg | grep -iE 'qmi|mbim|cdc|wwan'
   ```
   (Voir `cdc-wdm0` et `wwan0` signifie que l'interface a bien été montée.)

3. **Vérifier l'état de ModemManager :**
   ```bash
   mmcli -L
   ```
   (Ça liste les modems avec leurs numéros. Note le numéro, en général `0`.)

---

## Étape 3 : la connexion facile (avec NetworkManager)

Si tu utilises la version desktop d'Ubuntu ou de Mint, le gestionnaire réseau intégré est l'option la plus pratique.

```bash
# Crée une connexion (remplace "internet" par l'APN de ton opérateur)
nmcli connection add type gsm ifname cdc-wdm0 con-name "mobile" apn "internet"

# Et on lance !
nmcli connection up mobile
```
C'est tout. Tu peux vérifier que `wwan0` a bien reçu une IP avec `ip addr show`.

### (Avancé) Connexion en mode texte sans bureau
Sur un serveur headless ou une carte embarquée, tu peux piloter le module directement avec `qmicli` :
```bash
sudo ip link set wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn=internet,ip-type=ipv4" --client-no-release-cid
sudo dhclient -v wwan0
```

---

## Étape 4 : active le positionnement GPS !

Tous ces modules embarquent un système de positionnement GNSS intégré (prise en charge de GPS, GLONASS et plus).
D'après les spécifications officielles :
- EM7455 / EM7565 / MC7455 : 1 seconde en démarrage à chaud, 32 secondes à froid. Précision horizontale d'environ 2 à 5 mètres.
- L'EM919x 5G : démarrage à froid plus rapide (≤28 secondes), précision légèrement meilleure (<4 m à 95 %).

**Pour récupérer des coordonnées sous Linux, le plus rapide :**

1. Activer la fonction GPS :
```bash
mmcli -m 0 --location-enable-gps-raw
```
2. Récupérer les coordonnées actuelles :
```bash
mmcli -m 0 --location-get
```
Ta latitude et ta longitude s'affichent direct. Si tu veux streamer la position en temps réel vers d'autres programmes, associe ça à `gpsd`.

---

## Pièges courants et dépannage express

1. **`mmcli -L` ne montre rien** : `ModemManager` a peut-être planté, ou ton alimentation USB ne tire tout simplement pas la carte.
2. **Le GPS échoue tout le temps** : tu as branché l'antenne GPS sur Main ou Aux ? Le port GNSS a son propre connecteur dédié !
3. **L'EM919x ne monte pas en vitesse** : c'est une carte 5G qui supporte USB 3.1 Gen 2 et même PCIe Gen 3. Si tu la branches sur un port USB 2.0, le fabricant ne garantit pas les performances.

## Conclusion

Travailler avec les modules Sierra sous Linux n'est pas si dur qu'il n'y paraît. Vérifie le slot et les antennes, installe la famille de paquets `modemmanager`, configure l'APN, et te voilà en ligne. Cette méthode est parfaite pour les ingénieurs qui font de l'edge computing ou de l'IoT industriel (IIoT).

## Où acheter (Call To Action)

Tu veux intégrer un module Sierra dans ton appareil sous Ubuntu ? Yupitek propose des solutions complètes : modules, antennes, cartes adaptatrices, plus un support technique en première ligne.
Contacte-nous : **sales@yupitek.com**
Voir les produits : [Série Sierra Wireless](https://yupitek.com/fr/products/sierra/)

{{< faq >}}
