---
title: "Guide de démarrage Flipper Zero : Déballage, configuration, mise à jour du firmware et 5 fonctionnalités pratiques"
locale: fr
hreflang_group: flipper-zero-beginners-guide-setup-tutorial
slug: flipper-zero-beginners-guide-setup-tutorial
published: 2026-08-10
author: Yupitek
category: Technical
tags:
  - Flipper Zero
  - Tutoriel
hero_image: /static/img/flipper-zero/hero.webp
hero_alt: "Guide de démarrage Flipper Zero : Déballage, mise à jour du firmware et test de 5 fonctionnalités | Yupitek"
seo_description: "Qu'est-ce que le Flipper Zero ? De l'unboxing et de la configuration de la carte microSD à la mise à jour du firmware via qFlipper, jusqu'aux tests pratiques de 5 fonctionnalités clés : RFID, Sub-GHz, NFC, IR et BadUSB. Ce guide vous accompagne pas à pas."
---

# Guide de démarrage Flipper Zero : Déballage, configuration, mise à jour du firmware et 5 fonctionnalités pratiques

> TL;DR : Le Flipper Zero est un outil d'exploration matérielle de poche, équipé de RFID 125 kHz, Sub-GHz, NFC, infrarouge et BLE. Il se connecte à un ordinateur via USB-C pour simuler un clavier (BadUSB). Commencez par installer une carte microSD, mettez à jour le firmware avec qFlipper ou l'application mobile, puis explorez la lecture de cartes RFID et la télécommande IR. Utilisez toutes les fonctionnalités uniquement sur des appareils que vous possédez ou pour lesquels vous avez une autorisation explicite.

## Qu'est-ce que le Flipper Zero ? Pour qui est-il conçu ?

Le Flipper Zero est un appareil portable polyvalent de la taille d'une paume, positionné comme un « outil d'exploration matérielle ». Il ne s'agit pas d'un gadget grand public, mais d'un équipement conçu pour les chercheurs en cybersécurité, les débutants en tests de pénétration, les Maker et les ingénieurs IoT. Il permet de lire, d'analyser et de simuler des protocets sans fil courants et des signaux numériques.

Le matériel principal comprend :

- **RFID 125 kHz** : Lecture et simulation de cartes d'accès basse fréquence.
- **Radio Sub-GHz** (Puce CC1101) : Analyse des signaux des télécommandes, portails de garage et capteurs IoT dans la bande 300–928 MHz.
- **NFC (13,56 MHz)** : Lecture, écriture et simulation de cartes haute fréquence.
- **Infrarouge (IR)** : Apprentissage et retransmission des codes de télécommande pour téléviseurs, climatiseurs, etc.
- **BLE** : Appairage et contrôle via l'application mobile.
- **USB-C** : Connexion à un ordinateur pour les mises à jour du firmware et la simulation de clavier (BadUSB / DuckyScript).
- **GPIO / iButton** : Clés de contact 1-Wire et extensions matérielles.

Public cible : Étudiants se préparant à la recherche en sécurité sans fil, ingénieurs devant vérifier la fiabilité de leurs systèmes d'accès ou capteurs, et Maker souhaitant comprendre les principes du RFID/NFC. Si vous cherchez simplement un « duplicateur de télécommande », la fonction Sub-GHz le permet, mais vérifiez d'abord la législation locale et le contexte d'utilisation.

## Déballage et configuration initiale : Installez la carte microSD avant de démarrer

Le Flipper Zero n'est pas livré avec une carte microSD, mais il est **fortement recommandé** d'en utiliser une pour le stockage du firmware et des données. Suivez ces étapes :

1. **Préparez la carte microSD** : Une capacité de 4 Go ou plus est recommandée. Le format doit être FAT32 (FAT16/FAT32/exFAT sont acceptables). Insérez la carte dans le logement situé au bas de l'appareil, **puces vers le haut**.
2. **Chargez l'appareil** : Connectez-le à un chargeur ou à un ordinateur via USB-C et assurez-vous qu'il est complètement chargé avant la première utilisation.
3. **Allumez l'appareil** : Maintenez le bouton Retour (Back) à l'arrière de l'appareil enfoncé pendant environ 3 secondes. L'animation du dauphin indique que l'appareil est allumé.
4. **Vérifiez la version du système** : Allez dans `Paramètres → À propos`, notez la version actuelle du firmware pour la mise à jour suivante.

> Remarque : L'interface par défaut du Flipper Zero est en anglais. Certains firmwares tiers proposent le chinois, mais il est **déconseillé** aux débutés d'utiliser des firmwares tiers dès le départ. Familiarisez-vous d'abord avec le firmware officiel.

## Mise à jour du firmware : qFlipper (Bureau) et Application Mobile

La mise à jour du firmware est l'étape la plus importante pour débuter avec le Flipper Zero. Le fabricant corrige régulièrement les bugs et ajoute le support de nouveaux protocoles ; un ancien firmware pourrait ne pas lire certaines cartes ou signaux.

### Méthode 1 : qFlipper (Version Bureau) – Recommandé

1. Téléchargez qFlipper pour votre plateforme (Windows / macOS / Linux) depuis le site officiel de Flipper.
2. Connectez le Flipper Zero à votre ordinateur via USB-C et ouvrez qFlipper.
3. Cliquez sur l'icône en forme de clé anglaise en haut à droite (Contrôles avancés), puis sélectionnez « Firmware update channel ».
4. Choisissez **Release (Version stable)** et cliquez sur Update.
5. Attendez la fin de la mise à jour (environ 5 à 10 minutes). L'appareil redémarrera automatiquement.

### Méthode 2 : Application Mobile

1. Installez l'application officielle Flipper Mobile (iOS / Android).
2. Activez le Bluetooth sur votre téléphone et appairez-le avec le Flipper Zero (sur l'appareil : `Paramètres → Bluetooth`).
3. Dans l'application, cliquez sur Update. La mise à jour se transmet via BLE et prend environ 10 minutes.

### Comment choisir le canal de firmware ?

| Canal | Stabilité | Public cible |
|---|---|---|
| Release (Stable) | Élevée | **Les débutés doivent toujours choisir cette option** |
| Release Candidate (RC) | Moyenne | Utilisateurs souhaitant tester de nouvelles fonctionnalités en avance |
| Development (Dev) | Faible | Développeurs et testeurs |

> ⚠️ Ne débranchez pas l'appareil ni ne coupez l'alimentation pendant la mise à jour. Si l'appareil reste bloqué sur l'écran de démarrage, entrez en mode recovery et réinstallez le firmware (double-cliquez sur Reset). Bien que les firmwares tiers (comme Xtreme) offrent des fonctionnalités étendues, ils peuvent être instables. Les débutés doivent utiliser la version stable officielle.

## Test de 5 fonctionnalités pratiques

### 1. RFID 125 kHz : Lecture et simulation de cartes basse fréquence

Les anciennes cartes d'accès (125 kHz) contiennent souvent uniquement un code ID sans mécanisme de vérification. Le Flipper Zero dispose d'une antenne LF au bas de l'appareil pour la lecture rapprochée :

1. Menu principal → `RFID 125 kHz` → `Read` (Lire).
2. Placez la carte à plat près du bas de l'appareil. Une fois la lecture réussie, l'UID et les données s'affichent.
3. Pour simuler, sélectionnez `Emulate` après la lecture. L'appareil peut alors servir de carte temporaire.

### 2. Sub-GHz : Analyse des signaux sans fil 300–928 MHz

Le transceiver CC1101 intégré permet de capturer les signaux émis par des télécommandes, des portails de garage ou des capteurs IoT :

1. Menu principal → `Sub-GHz` → `Read Raw` (Lire brut).
2. Appuyez sur un bouton de la télécommande. L'écran affiche la fréquence et l'onde du signal.
3. Vous pouvez sauvegarder le signal et utiliser `Replay` pour le retransmettre. Vous pouvez également définir manuellement une fréquence pour scanner les activités sans fil dans votre environnement.

### 3. NFC : Lecture, écriture et simulation de cartes 13,56 MHz

Le module NFC prend en charge les standards courants 13,56 MHz. Il peut lire l'UID et les blocs de données de cartes sans contact (comme les cartes de transport). La capacité de simulation complète dépend du mécanisme de chiffrement de la carte :

1. Menu principal → `NFC` → `Read` (Lire).
2. Posez la carte sur la zone de détection à l'arrière de l'appareil pour lire les informations.
3. Selon le type de carte, vous pouvez choisir `Emulate` ou `Write` (Écrire).

### 4. IR : Apprentissage et retransmission de télécommandes infrarouges

L'émetteur/récepteur IR intégré permet d'apprendre les codes de télécommandes pour téléviseurs, climatiseurs et vidéoprojecteurs, puis de les retransmettre :

1. Menu principal → `Infrared` → `Learn` (Apprendre).
2. Pointez la fenêtre IR de l'appareil vers la télécommande et appuyez sur un bouton. Une fois l'apprentissage réussi, nommez et sauvegardez le code.
3. Vous pouvez ensuite retransmettre ce code à tout moment via `Infrared → Saved` (Sauvegardés).

### 5. BadUSB / DuckyScript : Simulation de clavier USB-C

Lorsqu'il est connecté à un ordinateur, le Flipper Zero peut simuler un clavier USB et exécuter des scripts DuckyScript (saisie automatique de commandes) :

1. Placez un script `.txt` (syntaxe DuckyScript) dans le dossier `badusb/` de la carte microSD.
2. Connectez l'appareil à l'ordinateur cible via USB-C. Dans le menu principal, allez dans `BadUSB` et sélectionnez le script à exécuter.

> ⚠️ **Le BadUSB est une fonctionnalité hautement sensible** : Les scripts s'exécutent sur l'ordinateur via la saisie clavier, équivalant à « quelqu'un qui tape au clavier devant l'ordinateur ». Utilisez cette fonction uniquement sur votre propre ordinateur ou dans un environnement de test explicitement autorisé.

## Rappel d'utilisation légale (À lire absolument)

Le Flipper Zero est un outil légal, mais son utilisation a des limites juridiques claires :

- **Copie/simulation de cartes d'accès et de télécommandes** : Autorisé uniquement pour les systèmes que vous possédez ou pour lesquels vous avez l'autorisation de l'administrateur. La lecture ou la simulation non autorisée de cartes d'accès ou de télécommandes de garage d'autrui peut engager votre responsabilité pénale (atteinte à la vie privée, loi sur les télécommunications, protection des données) en fonction de la juridiction.
- **BadUSB** : L'exécution de scripts sur l'ordinateur d'autrui sans autorisation est illégale.
- **Brouillage de signaux** : L'interférence intentionnelle avec les équipements sans fil d'autrui (comme les portails de garage) comporte également des risques juridiques.

**Le principe est simple : testez uniquement vos propres appareils ou ceux pour lesquels vous avez une autorisation écrite.**

## Questions fréquentes (FAQ)

**Q1 : Faut-il obligatoirement installer une carte microSD sur le Flipper Zero ?**
Ce n'est pas obligatoire, mais fortement recommandé. La plupart des applications, des bases de données de signaux et des scripts BadUSB sont stockés sur la carte microSD. Sans carte, les fonctionnalités sont considérablement limitées.

**Q2 : La mise à jour du firmware peut-elle rendre l'appareil inutilisable (brick) ?**
Le risque avec le firmware stable officiel est extrêmement faible. Tant que l'alimentation n'est pas coupée et que la connexion n'est pas interrompue pendant la mise à jour, l'échec est rare. En cas de problème, vous pouvez réinstaller le firmware via le mode recovery.

**Q3 : Peut-on copier une carte de transport (type EasyCard) ?**
La plupart des cartes de transport récentes sont chiffrées et protégées par des clés. Le Flipper Zero ne peut lire que l'UID ou les blocs non chiffrés, et ne peut pas effectuer une copie complète. De plus, la copie non autorisée de titres de transport est illégale.

**Q4 : Quelle est la différence entre le Flipper Zero et un SDR (Radio Logicielle) ?**
Le Flipper Zero intègre un transceiver Sub-GHz optimisé pour les protocoles courants (OOK/ASK/FSK, etc.), avec une prise en main intuitive. Un SDR (comme le HackRF ou le RTL-SDR) offre une plage de fréquences plus large et permet de visualiser le spectre brut, mais nécessite un ordinateur et des connaissances techniques plus approfondies. Les deux outils sont complémentaires.

**Q5 : Où acheter un Flipper Zero ?**
Yupitek (Yuhé Technology) propose des Flipper Zero et des accessoires associés, ainsi que du conseil technique. Pour toute question concernant la configuration après achat, veuillez contacter sales@yupitek.com.

**Q6 : Peut-on installer un firmware tiers ?**
Oui, mais ce n'est pas recommandé pour les débutants. Les firmwares tiers (comme Xtreme) offrent une interface personnalisée et des fonctionnalités supplémentaires, mais leur stabilité et leur sécurité doivent être évaluées par l'utilisateur, et ils peuvent entraîner la perte du support de mise à jour officiel.

## Conclusion

La courbe d'apprentissage du Flipper Zero est simple : **installez la microSD → mettez à jour le firmware stable officiel → commencez par la lecture RFID et la télécommande IR → familiarisez-vous avec Sub-GHz et BadUSB ensuite**. C'est un excellent point de départ pour comprendre les protocoles sans fil et la sécurité matérielle. N'oubliez jamais : plus les fonctionnalités sont puissantes, plus l'autodiscipline est nécessaire. Testez uniquement les appareils dont vous avez l'autorisation.

Pour acheter un Flipper Zero ou des accessoires associés, ou pour obtenir des conseils techniques, n'hésitez pas à contacter [sales@yupitek.com](mailto:sales@yupitek.com). Yupitek fournit des services de conseil produit et technique.