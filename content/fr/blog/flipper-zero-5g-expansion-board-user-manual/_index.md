---
title: "Manuel d'utilisation et d'installation illustré de la carte d'extension Flipper Zero 5G (v2.0)"
description: "Ce guide d'installation et d'utilisation de la carte d'extension Flipper Zero 5G v2.0 propose des schémas isométriques détaillés pour t'aider à installer les antennes, la carte MicroSD et à configurer les broches GPIO."
date: 2026-10-18
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-zero-5g-expansion-board-user-manual"
tags: ["Flipper Zero", "5G Expansion Board", "SDRLab", "Tutorial"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-10-18
featureimage: "/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg"
hideFeatureImage: true
---

# Manuel d'utilisation et d'installation illustré de la carte d'extension Flipper Zero 5G (v2.0)

> **Public cible** : les nouveaux clients qui découvrent ce module pour la première fois.  
> **Principe de rédaction** : des schémas détaillés pour chaque étape sensible ou technique. Oublie les suppositions et profite d'une installation simple, étape par étape.

---

## 00. Déballage et liste des accessoires

Bienvenue dans l'univers du module d'extension Flipper Zero 5G ! Avant de commencer, vérifie que ton pack contient bien les accessoires suivants.

![開箱全家福與配件圖](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg)
*Figure 1 : liste complète des accessoires fournis*

### ⚠️ Précisions sur les accessoires
*   **Inclus dans le pack standard** :
    1.  Le module principal de la carte d'extension 5G (5G Expansion Board) x 1
    2.  Une antenne-bâton 433MHz (antenne noire courte) x 1
    3.  Une antenne active GPS en céramique (antenne carrée) x 1
    4.  Une antenne patch WiFi double bande (antenne noire plate) x 1
*   **Non inclus (à préparer par tes soins)** :
    *   **Le Flipper Zero** (le module est vendu sans la console)
    *   **Une carte MicroSD** (indispensable pour faire fonctionner le module)

---

## 01. Découvre ton module 5G

Avant de brancher les antennes ou de connecter la console, prends une minute pour te familiariser avec les différentes interfaces et la disposition matérielle de la carte.

### Description de la face avant

![模組正面標註圖](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_02_front_interface.jpg)
*Figure 2 : légendes des composants de la face avant*

*   **Écran (LCD Screen)** : affiche l'état actuel de la connexion, l'adresse IP et le mode de fonctionnement.
*   **Interrupteur à bascule (Toggle Switch)** : contrôle l'alimentation de l'écran du module (bascule vers le haut pour l'allumer).
*   **Emplacement carte MicroSD (SD Card Slot)** : sert à stocker les configurations du micrologiciel système et les fichiers de log.
*   **Connecteur GPIO** : le connecteur femelle qui vient s'emboîter sur le dessus du Flipper Zero.
*   **Indicateurs lumineux (LED Indicators)** : affichent l'état de l'alimentation et de la charge.

### Description des ports d'antennes latéraux

![側面天線埠標註圖](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_03_antenna_ports.jpg)
*Figure 3 : positions et marquages des ports d'antennes*

*   **433M A** : port pour l'antenne-bâton 433MHz.
*   **GPS** : port pour l'antenne GPS en céramique.
*   **2.4G** et **2.4G/5G** : ports pour l'antenne patch WiFi double bande.

> ⚠️ **Rappel important concernant les versions de production** :  
> L'emplacement des ports d'antennes peut varier légèrement selon les lots de production (par exemple, les connecteurs GPS et WiFi peuvent être inversés). **Fie-toi impérativement aux étiquettes imprimées sur le boîtier de ton module**, et évite de brancher les antennes de mémoire afin de ne pas risquer une mauvaise réception ou d'endommager le matériel.

---

## 02. Guide d'installation pas à pas

### Étape 1 | Préparation et installation de la carte MicroSD

Le module 5G a besoin d'une carte mémoire pour stocker ses paramètres.

1.  **Spécifications requises** : une capacité maximale de **32 Go ou moins**, formatée impérativement en **FAT32**.
2.  **Sens d'insertion** : insère la carte avec les broches dorées orientées vers le bas dans l'emplacement MicroSD, puis appuie doucement jusqu'au clic de verrouillage.

![MicroSD 卡插槽特寫](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_07_sd_card_slot.jpg)
*Figure 4 : gros plan sur le sens correct d'insertion de la carte MicroSD*

---

### Étape 2 | Installation des trois antennes

Visse les trois antennes fournies sur leurs connecteurs SMA correspondants. Attention à ne pas forcer, sers simplement jusqu'à ce que l'antenne soit bien fixée.

![天線安裝接線圖](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_08_three_antenna_connection.jpg)
*Figure 5 : schéma de connexion et d'orientation des trois types d'antennes*

| Type d'antenne | Port d'antenne correspondant | Instructions d'installation |
| :--- | :--- | :--- |
| **Antenne GPS céramique** | **Port GPS** | Connecteur carré en céramique avec un long câble |
| **Antenne patch WiFi double bande** | **Port 2.4G/5G** | Antenne patch plate et noire |
| **Antenne-bâton 433MHz** | **Port 433M A** | Antenne rigide noire courte |

#### ⚠️ Avertissement sur le sens de pose de l'antenne GPS
L'antenne GPS a une orientation précise. Lors de l'installation, **la face en céramique (généralement la face opposée à l'autocollant double face, ou la face sans texte) doit être orientée vers le haut (vers le ciel)**, sinon la géolocalisation ne fonctionnera pas !

![GPS 天線朝向對比圖](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_09_gps_antenna_orientation.jpg)
*Figure 6 : comparaison entre le bon positionnement (vers le ciel) et le mauvais positionnement (vers le sol) de l'antenne GPS*

---

### Étape 3 | Connexion à la console Flipper Zero

Insère le module 5G sur les broches GPIO situées sur le dessus de ton Flipper Zero.

1.  **Éteins d'abord ton Flipper Zero** pour éviter d'endommager le matériel lors de la connexion.
2.  Aligne les broches GPIO du Flipper Zero avec les fentes sous le module.

![GPIO 對接 alignment 圖](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_10_gpio_alignment.jpg)
*Figure 7 : positionnement et alignement des broches GPIO*

3.  Applique une pression uniforme avec les deux mains pour **enfoncer délicatement le module au maximum**.
4.  **Vérifie l'alignement** : une fois l'installation terminée, regarde le module de profil. Il doit être **parfaitement ajusté contre la console, sans aucun espace visible**.

![GPIO 插入貼合度確認](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_19_gpio_insertion_flat.jpg)
*Figure 8 : connexion correcte avec insertion complète sans aucun espace*

---

### Étape 4 | Configuration logicielle sur le Flipper Zero

Une fois connecté, allume ton Flipper Zero puis passe à la configuration des broches matérielles (GPIO Pin).

Prenons l'exemple du micrologiciel **Momentum** pour effectuer les réglages suivants :

1.  **Activer l'alimentation de l'écran** : pousse l'interrupteur à bascule situé à l'avant gauche du module sur la position **UP**.
    ![螢幕撥動開關 UP 特寫](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_16_toggle_switch_up.jpg)
    *Figure 9 : interrupteur de l'écran basculé sur UP pour activer l'affichage*

2.  **Configuration des broches GPS** :
    *   Chemin : `Protocol Settings` ➔ `GPIO Pin Settings` ➔ `GPS Pin`
    *   Valeur : choisis **13** ou **14** (selon le manuel ou les indications fournies avec ton lot).
3.  **Configuration des broches ESP32 (fonctions WiFi/Bluetooth)** :
    *   Chemin : `Protocol Settings` ➔ `GPIO Pin Settings` ➔ `ESP32 Pin`
    *   Valeur : choisis **15, 16**.
4.  **Configuration du module radio 433MHz** :
    *   Va dans `Sub-GHz` ➔ `Advanced Settings` ➔ configure Module sur **External** (pour activer l'antenne externe).

---

### Étape 5 | Charge et vérification de la batterie

Ce module intègre une batterie rechargeable.

![USB-C 介面對比與警告](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_17_usb_ports_comparison.jpg)
*Figure 10 : comparaison entre le port de charge supérieur (CHARGE ONLY) et le port de flash latéral (FLASH ONLY)*

*   **Port USB-C supérieur** : **dédié uniquement à la charge** (indiqué par « CHARGE ONLY »). Utilise obligatoirement ce port pour recharger la batterie !
*   **Port USB-C latéral** : **dédié uniquement au flash du micrologiciel** (indiqué par « FLASH ONLY »). Ne l'utilise jamais pour la charge quotidienne, sous peine de ne pas pouvoir alimenter la batterie.

#### État des indicateurs LED de batterie :
La face avant du module comporte 4 indicateurs LED qui affichent le pourcentage de charge restant :

![電量指示燈圖解](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_18_battery_led_indicators.jpg)
*Figure 11 : niveau de charge correspondant aux 4 LED*

*   1 LED allumée : environ 25 % de batterie (recharge au plus vite)
*   2 LED allumées : environ 50 % de batterie
*   3 LED allumées : environ 75 % de batterie
*   4 LED allumées : 100 % de batterie (charge complète)

---

## 03. Diagnostic des erreurs fréquentes (résolution des problèmes pour les débutants)

Si ton module ne fonctionne pas correctement, prends le temps de vérifier les points suivants :

*   [ ] **Les broches GPIO sont-elles bien enfoncées au maximum ?** (Le module doit être parfaitement collé au dessus du Flipper Zero, sans espace visible, voir Figure 8)
*   [ ] **L'orientation de l'antenne GPS est-elle correcte ?** (La face en céramique doit pointer vers le ciel, voir Figure 6)
*   [ ] **Les antennes sont-elles vissées sur les bons ports ?** (Les emplacements peuvent varier selon les lots de fabrication, vérifie les indications imprimées sur le boîtier, voir Figure 3)
*   [ ] **La carte MicroSD respecte-t-elle les spécifications ?** (La capacité doit être de 32 Go ou moins, formatée en FAT32, voir Figure 4)
*   [ ] **L'interrupteur de l'écran est-il bien basculé sur UP ?** (Voir Figure 9)

---

## 04. Mise à jour et flash du micrologiciel (fonction avancée)

Lors de la sortie d'une nouvelle version du micrologiciel, tu devras flasher le module en utilisant le port USB-C latéral.

1.  Prépare un câble USB-C connecté à ton ordinateur.
2.  **Étape cruciale** : tout en branchant le câble sur le **port USB-C latéral (FLASH ONLY)** du module, **maintiens enfoncé le bouton de flash situé à l'arrière ou sur le côté droit du module** afin de basculer la puce en mode Boot.

![韌體燒錄按鍵與插入順序](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_20_boot_flash_sequence.jpg)
*Figure 12 : schéma de la procédure (maintien du bouton de flash tout en insérant le câble USB)*
