---
title: "Carte réseau sans fil ALFA : Prise en charge de DD-WRT"
date: 2026-09-03
draft: false
slug: "alfa-ddwrt-router-compatibility"
tags:
  - "ALFA"
  - "DD-WRT"
  - "Router"
  - "Broadcom"
  - "Atheros"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "Guide Matériel"
description: "ALFA USB WiFi卡無DD-WRT官方驅動，建議使用OpenWrt。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Résumé du problème

Client demande : « Peut-on utiliser la carte réseau USB ALFA série sur un routeur sur lequel on a flashé le firmware DD-WRT ? »

Conclusion rapide : Actuellement, toutes les modèles actuels de la série ALFA (AWUS036ACH / ACM / ACHM / ACS / EACS / AX / AXER / AXML / AXM, au total 9 modèles) n'ont pas de prise en charge officielle des pilotes sur DD-WRT, et il n'est pas recommandé de les utiliser. (Critère : 9 cartes réseau USB ALFA actuelles) La prise en charge USB WiFi de DD-WRT est limitée à un très petit nombre de puces Atheros / Ralink anciennes, et nécessite une version de compilation spécifique. Si vous souhaitez utiliser une carte réseau USB WiFi sur un routeur, il est recommandé de passer à OpenWrt (voir [Carte réseau USB ALFA : est-elle compatible avec OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)).

## 2. Analyser les spécifications et les besoins du logiciel cible

### 2.1 Qu'est-ce que DD-WRT ?

DD-WRT est un firmware tiers open source pour routeurs, principalement conçu pour les routeurs intégrant des puces WiFi (Broadcom / Atheros / Ralink SoC). Son architecture de base est le kernel Linux, mais les pilotes par défaut sont précompilés pour les SoC correspondants du routeur cible.

### 2.2 Le cadre de support USB WiFi de DD-WRT

DD-WRT installe des pilotes supplémentaires via le système de gestion de paquets ipkg, mais les pilotes USB WiFi dans la bibliothèque de paquets officielle sont très rares :

| Pilote | État DD-WRT | SoC correspondant (modèles ALFA) |
|---|---|---|
| ath9k_htc | Partie des versions intégrées | Atheros AR9271 (par exemple, TP-Link TL-WN722N v1) |
| rt2800usb | Partie des versions intégrées | Ralink RT3070 / RT3370 / RT5370 (anciens modèles ALFA AWUS036NH) |
| rtl8812au | Aucun paquet officiel | Realtek RTL8812AU (AWUS036ACH) |
| mt76 / mt76x2u | Aucun paquet officiel | MediaTek MT7612U / MT7610U (AWUS036ACM / ACHM) |
| mt7921u | Aucun paquet officiel | MediaTek MT7921AUN (AWUS036AXML / AXM) |
| rtl8852bu / rtw89 | Aucun paquet officiel | Realtek RTL8832BU (AWUS036AX / AXER) |

### 2.3 Limites clés

- Le noyau de DD-WRT prend en priorité le WiFi intégré au routeur, et le WiFi USB est une fonction secondaire.
- Les versions de DD-WRT compilées pour différents modèles de routeurs diffèrent, et la disponibilité des pilotes varie énormément.
- Même si la communauté compile et ajoute des pilotes, ils ne peuvent souvent pas être installés en raison d'un espace Flash / RAM insuffisant.
- DD-WRT ne prend pratiquement pas en charge le mode surveillance (Monitor Mode) et l'injection de paquets (Packet Injection) pour le WiFi USB.

## 3. Analyse des spécifications et des puces des cartes réseau ALFA

Au 9 septembre 2026, la gamme de produits de cartes réseau USB sans fil actuels d'ALFA Network est la suivante :

| Modèle | Niveau Wi-Fi | Puce | Interface | État du pilote Linux |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | Linux in-kernel (mt7921u, nécessite kernel 5.12+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | Linux in-kernel (mt7921u, nécessite kernel 5.12+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree (rtl8852bu / rtw89) |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree (rtl8852bu / rtw89) |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | Out-of-tree (8812au, morrownr maintenance) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | Linux in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | Linux in-kernel (mt76x2u) |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | Out-of-tree (8812au couvert) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | Out-of-tree (8821cu, morrownr maintenance) |

## 4. Modèles et chipsets compatibles

### 4.1 Modèles ALFA compatibles avec DD-WRT (désormais épuisés / anciens)

| Modèle | Chipset | Pilote | État DD-WRT |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | Partie des versions DD-WRT intégrées, seulement 2.4GHz / 150Mbps |
| AWUS036H | Realtek RTL8187L | rtl8187 | Très ancien, certaines versions compatibles, seulement 2.4GHz / 54Mbps |
| AWUS050NH | Atheros AR9170 | carl9170 / ar9170usb | Très ancien, double bande, mais arrêté depuis plusieurs années |

### 4.2 Modèles actuels incompatibles avec DD-WRT

Tous les modèles ALFA actuels (voir le tableau de la section 3) ne sont pas pris en charge officiellement par DD-WRT, pour les raisons suivantes :

- Chipset Realtek (RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU) : DD-WRT n'a pas de pilote out-of-tree correspondant
- Chipset MediaTek (MT7612U / MT7610U / MT7921AUN) : DD-WRT n'a pas intégré les pilotes mt76 / mt7921
- Même si le routeur a un port USB et que le niveau matériel peut identifier le périphérique (lsusb peut voir VID/PID), sans pilote, il est impossible de créer une interface réseau

## 5. Besoins en environnement

Si le client souhaite tout de même essayer d'utiliser la carte réseau ALFA sur DD-WRT, il doit respecter les conditions suivantes :

| Élément | Besoin |
|---|---|
| Matériel du routeur | Le routeur doit avoir un port USB 2.0 / 3.0 et DD-WRT doit avoir activé le support du noyau USB (Services > USB) |
| Version de DD-WRT | Doit être la version la plus récente de BrainSlayer / Kong compatible avec le routeur, les anciennes versions ont moins de pilotes |
| Espace Flash | Au moins 16MB d'espace Flash (la plupart des routeurs d'entrée de gamme n'ont que 4-8MB, ce qui ne permet pas d'installer des pilotes supplémentaires) |
| RAM | Au moins 128MB de RAM (le pilote USB WiFi et hostapd consomment de la mémoire) |
| Alimentation | Le port USB doit fournir un courant suffisant (l'AWUS036ACH avec une sortie haute puissance peut atteindre 800mA+, il est recommandé d'utiliser un Hub USB avec alimentation) |

## 6. Détermination de la compatibilité

### Matrices de compatibilité ALFA en service × DD-WRT

| Modèle | Processeur | Détection du panneau USB | Chargeur de pilote | STA Internet | Mode AP | Monitor | Évaluation globale |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ✅（lsusb） | ❌ | ❌ | ❌ | ❌ | Non pris en charge |
| AWUS036AXM | MT7921AUN | ✅ | ❌ | ❌ | ❌ | ❌ | Non pris en charge |
| AWUS036AX | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | Non pris en charge |
| AWUS036AXER | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | Non pris en charge |
| AWUS036ACH | RTL8812AU | ✅ | ❌ | ❌ | ❌ | ❌ | Non pris en charge |
| AWUS036ACHM | MT7610U | ✅ | ❌ | ❌ | ❌ | ❌ | Non pris en charge |
| AWUS036ACM | MT7612U | ✅ | ❌ | ❌ | ❌ | ❌ | Non pris en charge |
| AWUS036ACS | RTL8811AU | ✅ | ❌ | ❌ | ❌ | ❌ | Non pris en charge |
| AWUS036EACS | RTL8811CU | ✅ | ❌ | ❌ | ❌ | ❌ | Non pris en charge |

Critère de détermination : La bibliothèque officielle de DD-WRT et la compilation par défaut du noyau n'incluent pas les pilotes USB WiFi pour les puces mentionnées ci-dessus. La visualisation du dispositif via lsusb ne signifie que la reconnaissance au niveau du panneau USB, et ne garantit pas que la fonction réseau est disponible.

## 7. Détails ultra détaillés des étapes de configuration

Puisque les modèles actuels ALFA ne sont pas compatibles avec DD-WRT, cette section propose deux alternatives :

### Chemin A : Vérifiez si votre routeur DD-WRT ne prend pas en charge réellement (étapes de dépannage)

**Étape 1 : Connectez-vous à l'interface de gestion DD-WRT**

Saisissez `192.168.1.1` (ou l'IP de votre routeur) dans votre navigateur.

**Étape 2 : Activez le support USB**

- Allez dans Services > USB
- Cochez Core USB Support, USB 2.0 Support, USB 3.0 Support (si disponible)
- Cochez USB Wireless Device Support (si disponible)
- Cliquez sur Save > Apply Settings

**Étape 3 : Insérez la carte réseau ALFA dans le port USB de votre routeur**

**Étape 4 : Connectez-vous au routeur via SSH pour vérifier**

```bash
# Vérifiez si le périphérique USB est détecté
lsusb
# La sortie prévue doit inclure le VID/PID de la carte réseau ALFA, par exemple :
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter

# Vérifiez si l'interface réseau est créée
ip link show
# Si vous ne voyez pas de nouvelles interfaces comme wlan0 / wlan1, cela signifie que le pilote n'est pas chargé

# Vérifiez le journal du noyau
dmesg | tail -30
# Si vous voyez "no driver" ou uniquement des messages de liste USB, vérifiez que le pilote manque
```

**Étape 5 : Vérifiez les modules de pilotes WiFi disponibles**

```bash
# Liste des pilotes sans fil chargés
lsmod | grep -E "ath|rt2|rtl|mt76|mac80211|cfg80211"
# Si seules les pilotes intégrés au routeur (comme wl / b43 / ath9k) sont détectés, cela signifie qu'il n'y a pas de pilote WiFi USB
```

**Étape 6 : Essayez d'installer les pilotes communautaires (si disponibles)**

```bash
ipkg update
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# Si le résultat de la recherche est vide, vérifiez que la version de DD-WRT n'a pas de pilotes disponibles
```

### Chemin B : Solution alternative recommandée — Utilisez OpenWrt

Si vous devez utiliser la carte réseau WiFi USB ALFA sur le routeur, il est fortement recommandé de flasher le firmware du routeur de DD-WRT à OpenWrt. OpenWrt dispose d'une bibliothèque de pilotes WiFi USB active, prenant en charge les puces MT7612U / MT7610U / RTL8812AU. Pour plus de détails, consultez [L'adaptabilité de la carte réseau sans fil ALFA avec OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/).

## 8. Erreurs Courantes et Solutions

| Symptômes | Causes Probables | Solutions |
|---|---|---|
| `lsusb` ne voit pas la carte réseau ALFA | Alimentation USB insuffisante / Mauvais contact / DD-WRT n'a pas activé le noyau USB | Vérifiez Services > USB pour voir si il est activé ; changez de port USB ou utilisez un Hub USB avec alimentation |
| `lsusb` le voit mais `ip link` n'a pas d'interface wlan | Manque de pilote pour le chip correspondant | Vérifiez si la version de DD-WRT contient ce pilote ; dans la plupart des cas, il n'y a pas de solution, envisagez de passer à OpenWrt |
| Il y a une interface wlan mais impossible de scanner les AP | Le pilote ne prend pas en charge complètement / Mode d'écoute en conflit | Vérifiez si dmesg a des erreurs de chargement de firmware ; vérifiez la configuration de la Réglementation Domaine |
| La configuration est perdue après le redémarrage du routeur | Espace NVRAM insuffisant dans DD-WRT | Évitez d'installer des pilotes supplémentaires sur des routeurs bas de gamme ; envisagez de mettre à niveau le matériel ou de passer à OpenWrt |
| AWUS036ACH coupe le courant lors de l'output à haute puissance | Alimentation du port USB insuffisante | Utilisez un Hub USB 3.0 avec alimentation ; réduisez la configuration de la puissance TX |

## 9. Limites connues

- Absence de pilote : DD-WRT officiel ne fournit pas de pilote USB WiFi pour les modèles ALFA en service, c'est la limitation la plus fondamentale.
- Ressources matérielles : La plupart des routeurs qui peuvent être flashés avec DD-WRT ont une mémoire Flash (4-16MB) et une mémoire RAM (32-128MB) limitées. Même avec un pilote, il peut être impossible d'installer.
- Non-soutien aux modes Monitor et Packet Injection : L'architecture USB WiFi de DD-WRT ne prend pas en charge les modes Monitor et Packet Injection nécessaires aux tests d'intrusion.
- Instabilité en mode AP : Même si les puces Ralink anciennes peuvent fonctionner, le mode AP USB WiFi sur DD-WRT est souvent sujet à des coupures de connexion et des problèmes de performance.
- Fragmentation des versions : Les versions de compilation de DD-WRT diffèrent grandement d'un modèle de routeur à l'autre, ce qui ne garantit pas que le pilote d'une version peut fonctionner sur une autre version.
- Maintenance non active : Le rythme de développement de DD-WRT ralentit, et la probabilité d'ajouter un pilote USB WiFi est faible.
- Complément : Même en dépit des limitations de DD-WRT, les utilisateurs Linux sont vivement recommandés par le mainteneur de pilotes morrownr pour éviter cette série de puces (voir [Est-ce que la carte réseau sans fil ALFA est compatible avec OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) - Chapitre 9), ce n'est pas seulement un problème du plateau DD-WRT.

Conditions de contestation : Si le client utilise des versions communautaires avec des pilotes supplémentaires telles que BrainSlayer / Kong, les conditions de soutien peuvent être différentes ; cette évaluation se fait sur la version officielle publiée.

## 10. Sources de référence URL

| Source | Description | URL | État de vérification | Date de vérification |
|---|---|---|---|---|
| Wiki officiel DD-WRT | Entrée principale pour l'installation, la support et les FAQ | https://wiki.dd-wrt.com/wiki/Main_Page | ✅ Vérifié | 2026-09-03 |
| Wiki officiel DD-WRT — Installation | Instructions d'installation (y compris la support USB) | https://wiki.dd-wrt.com/wiki/Installation | ✅ Confirmé via le lien de la page principale | 2026-09-03 |
| Documents officiels OpenWrt | Comparaison USB WiFi | https://openwrt.org/docs/start | ✅ Vérifié | 2026-09-03 |
| morrownr/8812au GitHub | Pilote Linux RTL8812AU (non intégré dans DD-WRT) | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |
| Vue d'ensemble des produits ALFA Network (Yupitek) | Spécifications des produits actuels ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Vérifié | 2026-09-03 |

Articles associés : [Est-ce que la carte réseau sans fil ALFA est compatible avec OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) | [Est-ce que la carte réseau sans fil ALFA est compatible avec Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)

Déclaration de non-responsabilité : La détermination de la compatibilité de cet article se fait sur la base de l'état du pilote du processeur et de la bibliothèque de packages officiels de DD-WRT. Il existe de nombreuses versions de traduction personnalisées dans la communauté DD-WRT, et les résultats réels peuvent varier si le client utilise une version non officielle. Il est recommandé aux clients de choisir OpenWrt comme option prioritaire pour le WiFi USB du routeur.
