---
title: "\"Est-ce que la carte réseau sans fil ALFA est compatible avec Tomato ?\""
date: 2026-09-03
draft: false
slug: "alfa-tomato-router-compatibility"
tags:
  - "ALFA"
  - "Tomato"
  - "FreshTomato"
  - "Router"
  - "Broadcom"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "Guide Matériel"
description: "ALFA系列無USB WiFi驅動於Tomato，建議使用OpenWrt。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Résumé du problème

Client demande : « Peut-on utiliser la carte réseau sans fil USB de la série ALFA sur un routeur qui a été flashé avec le firmware Tomato ? »

Conclusion rapide : Actuellement, tous les modèles actuels de la série ALFA ne sont pas compatibles avec Tomato (y compris FreshTomato et AdvancedTomato) en ce qui concerne les pilotes, et il est fortement déconseillé de l'utiliser. Tomato est la plateforme la moins compatible avec les cartes réseau sans fil USB parmi les trois principaux firmware tiers pour les routeurs. Son développement se concentre principalement sur le WiFi intégré des routeurs Broadcom. Si vous avez besoin d'utiliser une carte réseau sans fil USB sur un routeur, il est préférable d'opter pour OpenWrt.

Éléments de jugement : Les 9 cartes réseau USB actuelles de la série ALFA (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analyser les spécifications et les besoins du logiciel cible

### 2.1 Qu'est-ce que Tomato ?

Tomato est un ancien firmware open-source pour routeurs, initialement développé par Jonathan Zarate, et qui a donné naissance à plusieurs branches :

| Version dérivée | État de maintenance | Plateformes prises en charge |
|---|---|---|
| Version originale Tomato | Arrêté (début des années 2010) | Routeurs Broadcom MIPS |
| Tomato by Shibby | Arrêté | Broadcom MIPS / ARM |
| AdvancedTomato | Arrêté | Broadcom (GUI modifié de la branche Shibby) |
| FreshTomato | Maintenu activement | Broadcom MIPS / ARM (BCM47xx / BCM53xx) |
| Toastman Tomato | Arrêté | Broadcom MIPS |

### 2.2 Framework de support USB WiFi de Tomato

La philosophie de conception principale de Tomato est de « fournir un firmware tiers simple et stable pour les routeurs Broadcom ». Sa fonction USB est principalement prise en charge :

| Type de fonction USB | État de support |
|---|---|
| Dispositif de stockage USB (clé USB / disque dur) | ✅ Complètement pris en charge (Samba / FTP / DLNA) |
| Imprimante USB | ✅ Prise en charge (p910nd / CUPS) |
| Modem 3G/4G USB | ⚠️ Prise en charge partielle |
| Carte réseau WiFi USB | ❌ Presque pas pris en charge |

Le noyau de Tomato prévoit par défaut l'implémentation fermée du pilote WiFi intégré aux routeurs Broadcom (module wl), sans aucun pilote WiFi USB. Le système de gestion des paquets (ipkg / Optware) ne fournit pas non plus de paquets de pilotes WiFi USB.

### 2.3 Limites clés

- Tomato ne prend en charge que les routeurs avec des puces Broadcom, et les ports USB des routeurs Broadcom sont généralement utilisés uniquement pour le stockage / l'impression.
- Bien que FreshTomato soit toujours maintenu, les points de focus du développement sont la correction des bugs sur la plateforme Broadcom, et il ne sera pas ajouté de pilotes WiFi USB.
- Le système de fichiers de Tomato a très peu d'espace (généralement 4-16MB), il n'y a pas d'espace pour installer manuellement les pilotes.
- Tomato n'a pas de système de gestion de paquets moderne comme opkg, et il n'est pas possible d'installer des pilotes kmod de la même manière qu'avec OpenWrt.

## 3. Analyse les spécifications et les puces des cartes réseau ALFA actuelles

Au 9 septembre 2026, la gamme de produits de cartes réseau USB sans fil actuels d'ALFA Network est la suivante (base : 9 modèles) :

| Modèle | Niveau Wi-Fi | Puce | Interface | État du pilote Tomato |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ Aucun |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ Aucun |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ Aucun |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ Aucun |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ❌ Aucun |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ❌ Aucun |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ❌ Aucun |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ❌ Aucun |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ❌ Aucun |

## 4. Modèles et groupements de puces applicables

### 4.1 Modèles ALFA très anciens pouvant être utilisables sur Tomato (déjà arrêtés de production)

| Modèle | Groupement de puces | Module de pilote Linux | Description |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | Théoriquement chargeable, mais Tomato ne l'intègre pas par défaut ; nécessite la compilation manuelle du module du noyau, la faisabilité réelle est très faible |
| AWUS036H | Realtek RTL8187L | rtl8187 | Idem, uniquement 2.4GHz / 54Mbps, arrêté de production depuis plus de dix ans |

⚠️ Même pour ces modèles anciens, il est nécessaire pour l'utilisateur de compiler manuellement les modules de pilote correspondant à la version du noyau sur Tomato, et l'espace du système de fichiers de Tomato est généralement insuffisant pour l'installation. Ce n'est pas une «prise en charge», mais un «hack extrêmement avancé».

### 4.2 Modèles actuels inutilisables sur Tomato

Tous les modèles actuels ALFA (voir le tableau de la section 3) ne sont pas utilisables sur Tomato pour les raisons suivantes :

- Puces Realtek (RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU) : Tomato n'a aucun pilote correspondant, et il n'est pas possible de l'installer via le gestionnaire de paquets
- Puces MediaTek (MT7612U / MT7610U / MT7921AUN) : Tomato n'intègre pas les pilotes mt76 / mt7921, et l'équipe de développement de FreshTomato n'a pas l'intention de les ajouter
- Même si lsusb peut voir le périphérique (si Tomato a activé le noyau USB), il ne s'agit que d'une reconnaissance au niveau du bus USB, et il n'est pas possible de créer une interface réseau

## 5. Besoins Environnementaux

Étant donné que les modèles actuels ALFA ne sont pas disponibles sur Tomato, nous listons ici les conditions extrêmes nécessaires si le client tient à essayer :

| Item | Besoins |
|---|---|
| Matériel du routeur | Routeur avec puce Broadcom, avec un port USB 2.0, Flash ≥ 32MB, RAM ≥ 256MB |
| Version de Tomato | Dernière version de FreshTomato (les anciennes versions ont une prise en charge USB plus mauvaise) |
| Environnement de compilation croisée | Nécessité de construire un outil de compilation croisée pour l'architecture Broadcom (MIPS / ARM) |
| Code source du pilote | Nécessité de se procurer le code source du pilote Linux correspondant à la puce et de le modifier pour correspondre à la version du noyau Tomato |
| Compétences techniques | Nécessité d'avoir des compétences en développement de modules du noyau Linux, compilation croisée et débogage |
| Coût en temps | Prévu pour plusieurs heures à plusieurs jours, avec une probabilité de succès faible |

Conclusion : Pour 99,9% des utilisateurs, l'utilisation de la carte réseau WiFi USB ALFA sur Tomato n'est pas viable.

## 6. Détermination de la compatibilité

### Matrice de compatibilité ALFA modèles actuels × Tomato

| Modèle | Processeur | Support du noyau USB | Détection USB | STA Internet | Mode AP | Monitor | Évaluation globale |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ⚠️ Doit activer le noyau USB | ❌ | ❌ | ❌ | ❌ | Non supporté |
| AWUS036AXM | MT7921AUN | ⚠️ | ❌ | ❌ | ❌ | ❌ | Non supporté |
| AWUS036AX | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Non supporté |
| AWUS036AXER | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Non supporté |
| AWUS036ACH | RTL8812AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Non supporté |
| AWUS036ACHM | MT7610U | ⚠️ | ❌ | ❌ | ❌ | ❌ | Non supporté |
| AWUS036ACM | MT7612U | ⚠️ | ❌ | ❌ | ❌ | ❌ | Non supporté |
| AWUS036ACS | RTL8811AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Non supporté |
| AWUS036EACS | RTL8811CU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Non supporté |

Critère de détermination : Le noyau officiel de Tomato (y compris FreshTomato) et les dépôts de packages officiels ne contiennent aucune pile de pilote pour les puces WiFi USB modernes. L'objectif de conception de Tomato n'a jamais inclus la fonctionnalité d'extension WiFi USB.

## 7. Détails ultra détaillés des étapes à suivre

Puisque les modèles actuels ALFA ne sont pas disponibles sur Tomato, cette section fournit des étapes de vérification et des solutions de remplacement.

### 7.1 Vérification de la compatibilité de votre routeur Tomato avec le WiFi USB (étapes de dépannage)

**Étape 1 : Connexion à l'interface de gestion Tomato**

Saisissez 192.168.1.1 (ou l'IP de votre routeur) dans votre navigateur.

**Étape 2 : Vérification de l'activation du noyau USB**

- Allez dans USB and NAS > USB Support
- Vérifiez que Core USB Support, USB 2.0 Support, USB 3.0 Support (si disponible) sont cochés
- Vérifiez USB Wireless Device Support (si disponible) — La plupart des versions de Tomato n'ont pas cette option

**Étape 3 : Insérez la carte réseau ALFA dans le port USB de votre routeur**

**Étape 4 : Vérifiez la détection USB via SSH / Telnet**

```bash
# Vérifiez si lsusb existe (Tomato pourrait ne pas l'avoir par défaut)
which lsusb
# Si lsusb n'existe pas, vérifiez /proc/bus/usb ou dmesg
cat /proc/bus/usb/devices
# Ou
dmesg | grep -i usb
```

**Étape 5 : Vérification de l'interface réseau**

```bash
ifconfig -a
# Si vous ne voyez que vlan0 / br0 / eth0 / eth1 (interfaces internes du routeur), et pas wlan0 / wlan1, cela signifie que le WiFi USB n'est pas pris en charge
```

**Étape 6 : Vérification des modules noyau disponibles**

```bash
lsmod
# Vous devriez voir uniquement wl (pilote WiFi intégré Broadcom), et et (pilote réseau Ethernet)
# Vous ne devriez pas voir mt76 / rtl8812 / cfg80211 / mac80211 (pilotes WiFi USB)
```

**Étape 7 : Vérification de la disponibilité des extensions de packages**

```bash
# Tomato utilise ipkg, mais la bibliothèque de packages est très limitée
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# Le résultat devrait être vide
```

### 7.2 Solutions de remplacement suggérées

#### Solution 1 : Utilisez OpenWrt (fortement recommandé)

Si votre modèle de routeur est également compatible avec OpenWrt, il est recommandé de flasher le firmware de Tomato en OpenWrt. OpenWrt dispose d'une bibliothèque complète de pilotes WiFi USB, compatible avec la plupart des modèles ALFA.

- Vérifiez si votre routeur figure dans la liste des appareils pris en charge par OpenWrt
- Si c'est le cas, consultez les étapes d'installation [ALFA 无线网卡是否支持 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)

#### Solution 2 : Utilisez le WiFi intégré au routeur

Tomato prend en charge parfaitement le WiFi intégré aux routeurs Broadcom. Si vos besoins sont de simples connexions Internet ou de points d'accès (AP), utilisez directement le WiFi intégré du routeur sans besoin de carte réseau ALFA.

#### Solution 3 : Changer de matériel

Si vous avez besoin de fonctionnalités spécifiques du WiFi USB (comme une sortie de puissance élevée, le mode surveillance, l'injection de paquets), la plate-forme Tomato ne peut pas répondre à vos besoins. Nous vous recommandons :

- Utiliser un routeur compatible avec OpenWrt + carte réseau ALFA
- Utiliser un mini-ordinateur x86 avec OpenWrt / pfSense + carte réseau ALFA
- Utiliser directement la carte réseau ALFA sur un ordinateur portable avec Kali Linux / Ubuntu

## 8. Erreurs Courantes et Solutions

| Symptômes | Causes Probables | Solutions |
|---|---|---|
| L'interface de gestion Tomato ne possède pas l'option « USB Wireless Device Support » | Cette version de Tomato n'a pas traduit le support USB WiFi | C'est la norme, ce n'est pas un bug ; la plupart des versions de Tomato n'ont pas cette fonction |
| Après avoir inséré la carte réseau ALFA, dmesg détecte le USB mais pas l'interface réseau | Manque de pilote | Impossible à résoudre, Tomato n'a pas de pilote correspondant |
| Vous souhaitez installer manuellement le paquet ipkg mais ne trouvez pas le pilote WiFi | Le dépôt de paquets Tomato ne contient pas de pilote USB WiFi | C'est la norme ; nous vous recommandons de passer à OpenWrt |
| Les anciens modèles ALFA (RT3070) sont détectés par Tomato mais ne peuvent pas se connecter | Pilote incomplet / firmware manquant | Même pour les puces anciennes, cela n'est pas garanti ; nous recommandons d'utiliser OpenWrt |
| Après avoir flashé Tomato sur le routeur, le port USB ne peut lire que les clés USB | Les fonctionnalités USB de Tomato sont conçues uniquement pour le stockage / les imprimantes | C'est le comportement prévu ; Tomato ne prend pas en charge le WiFi USB |

## 9. Limites connues

- Pas de pilote USB WiFi intégré : le noyau officiel de Tomato (y compris FreshTomato) ne contient aucune prise en charge de pilote de puce USB WiFi moderne, c'est la limitation la plus fondamentale.
- Pilote Broadcom fermé et lié : Tomato dépend du pilote fermé wl de Broadcom et ne peut pas coexister avec des pilotes USB WiFi basés sur l'architecture ouverte mac80211 / cfg80211.
- Aucun écosystème de gestion de paquets : la bibliothèque de paquets ipkg de Tomato contient très peu de contenu, contrairement à OpenWrt qui en compte des milliers disponibles pour l'installation.
- Espace Flash / RAM insuffisant : la plupart des routeurs Tomato ne disposent que de 4 à 16 MB de Flash, ce qui ne laisse pas assez de place pour installer des pilotes même s'ils sont compilés.
- Direction de développement différente : pour l'équipe de développement de FreshTomato, la priorité est la stabilité de la plateforme Broadcom, et ils ne dédieront pas de ressources à l'ajout de la prise en charge USB WiFi.
- Pas de support pour le sniffing / injection : l'architecture WiFi de Tomato (pilote Broadcom wl) ne prend pas en charge les fonctionnalités de test de pénétration, et l'ajout d'un USB WiFi externe ne change rien à cela.
- Pas d'extension de mode AP : Même si les puces anciennes peuvent charger les pilotes, l'interface de configuration réseau de Tomato ne prend pas en charge la configuration du mode AP pour le USB WiFi.

Contre-arguments : Si une version future de FreshTomato ajoute explicitement la prise en charge des pilotes USB WiFi dans les notes de release officielles, ou si la communauté présente un projet de移植 de modules mt76 / rtl8812au largement validé, la détermination de "pas de prise en charge" dans le paragraphe 6 devra être réévaluée ; si FreshTomato passe à un noyau basé sur mac80211 ouvert, les explications des limitations devront également être mises à jour.

## 10. Sources de Référence URL

| Source | Description | URL | État de vérification | Date de vérification |
|---|---|---|---|---|
| Site officiel de FreshTomato | Liste des versions les plus récentes et des appareils pris en charge par FreshTomato | https://freshtomato.org/ | ✅ Vérifié | 2026-09-03 |
| Documentation officielle d'OpenWrt | Pilotes WiFi USB et paramètres sans fil (référence comparative) | https://openwrt.org/docs/start | ✅ Vérifié | 2026-09-03 |
| Forum officiel d'OpenWrt | Discussions sur les pilotes WiFi USB (référence comparative) | https://forum.openwrt.org/ | ✅ Vérifié | 2026-09-03 |
| Aperçu des produits d'ALFA Network (Yupitek) | Spécifications des produits actuels d'ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Vérifié | 2026-09-03 |

Articles associés : [Est-ce que la carte réseau sans fil ALFA est compatible avec DD-WRT ?](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/) | [Est-ce que la carte réseau sans fil ALFA est compatible avec OpenWrt ?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) | [Est-ce que la carte réseau sans fil ALFA est compatible avec NVIDIA DGX Spark ?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/) | [Est-ce que la carte réseau sans fil ALFA est compatible avec NVIDIA Jetson Nano ?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Déclaration de non-responsabilité : La détermination de la compatibilité de cet article se fait sur la base du noyau officiel de Tomato / FreshTomato et des bibliothèques de packages. Un très petit nombre d'utilisateurs avancés peuvent peut-être réaliser des fonctionnalités de base sur des puces anciennes en effectuant des compilations croisées, mais cela ne fait pas partie du support officiel et n'est pas recommandé pour les utilisateurs ordinaires. Pour les scénarios où l'utilisation d'un USB WiFi sur un routeur est nécessaire, OpenWrt est la seule option de firmware tiers réellement viable.
