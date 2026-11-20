---
title: "Le test le plus complet de 2026 : la matrice complète Monitor · Injection · AP des 9 cartes Wi-Fi ALFA sur ASUS GX10 (ARM64 / Ubuntu 24.04)"
slug: alfa-9-cards-arm64-gx10-ubuntu-matrix
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix.webp"
author: "benny-lai"
tags:
  - alfa-network
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - wifi-6
  - kali-linux
description: "Test de 9 cartes USB Wi-Fi ALFA sur Ubuntu 24.04 ARM64 (GX10) : performances Monitor, Injection, AP et WPA3-SAE, avec la compatibilité des outils Kali courants et des conseils de choix ; injection à 100 % pour l'AWUS036ACH / EACS."
faq:
  - question: "L'AWUS036AXM peut-elle injecter (injection) sous Ubuntu ?"
    answer: "Pas sur cette plateforme. En test, l'AWUS036AXM et l'AWUS036AXML (toutes deux en puce MT7921) échouent à l'injection en 2,4 GHz comme en 5 GHz, la cause principale étant la régression du chanctx de mac80211 du stock kernel 6.16+ (pas intrinsèque à la puce) ; elles sont donc déconseillées sur cette plateforme pour un usage nécessitant l'injection ou la capture de handshake."
  - question: "Quelle carte Wi-Fi ALFA a le meilleur taux de réussite d'injection sous Ubuntu ?"
    answer: "En test, l'AWUS036ACH et l'AWUS036EACS atteignent 100 % de taux de réussite d'injection en 2,4 GHz comme en 5 GHz : ce sont les deux meilleures des 9 cartes de ce lot."
  - question: "Les 9 cartes Wi-Fi ALFA nécessitent-elles l'installation d'un pilote sous Ubuntu 24.04 ?"
    answer: "Non. Les 9 cartes utilisent toutes le pilote intégré (in-kernel) sur le kernel 6.17 (familles rtw88 / rtw89 / mt76), reconnues dès le branchement, sans compilation de module DKMS."
  - question: "Les cartes Wi-Fi ALFA peuvent-elles monter un point d'accès WPA3-SAE sous Ubuntu ?"
    answer: "Oui, les 9 cartes montent avec succès un point d'accès WPA3-SAE et laissent les appareils se connecter (testé en 2,4 GHz pour chaque carte sauf l'ACS, testée en 5 GHz ; l'AXML aussi testée en 6 GHz) ; seule l'AWUS036ACHM nécessite de régler le sae_pwe de hostapd à 0, sans quoi l'ancien iPhone 7 Plus échoue à se connecter."
  - question: "Ces résultats de test sous Ubuntu sont-ils exploitables par les utilisateurs de Kali Linux ?"
    answer: "Kali Linux repose sur l'écosystème Debian/Ubuntu et utilise les mêmes pilotes in-kernel rtw88 / rtw89 / mt76 ; la compatibilité des pilotes et la matrice de capacités de cet article peuvent donc, en principe, servir de référence aux utilisateurs de Kali ; mais la plateforme de test de cet article est Ubuntu 24.04, non encore officiellement revérifiée sur Kali — référez-vous à une revérification ultérieure."
draft: false
---

## L'essentiel (TL;DR)

Yopitek (distributeur ALFA Network à Taïwan) a testé 9 adaptateurs Wi-Fi USB ALFA sur ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17) : les 9 fonctionnent en mode monitor et en AP, les AWUS036ACH et AWUS036EACS atteignent 100 % d'injection sur les deux bandes, et les AWUS036AXM / AWUS036AXML à base de MT7921 échouent à l'injection sur cette plateforme.

- **Monitor disponible pour toutes** : les 9 cartes passent en mode monitor, seule la qualité de réception varie.
- **L'injection est la ligne de partage** : l'ACH et l'EACS en Realtek `rtw88` atteignent 100 % d'injection sur les deux bandes, l'ACS suit ; les AXM / AXML en MT7921 échouent à l'injection sur cette plateforme.
- **Handshake de bout en bout (capture → export `.22000`) prouvé pour 7 cartes sur 9** : ACM, ACHM, ACH, ACS, EACS, AX, AXER.
- **AP et WPA3-SAE passent pour presque toutes** : seule l'AWUS036ACHM nécessite `sae_pwe=0` pour être compatible avec les anciens iPhone.
- **Sans compilation en ARM64** : les 9 cartes utilisent le pilote intégré au kernel 6.17, prêtes à l'emploi, sans DKMS.

Yopitek est le distributeur ALFA Network à Taïwan. Lorsqu'un client choisit une carte Wi-Fi USB, les trois questions les plus fréquentes sont presque toujours les mêmes : « Cette carte peut-elle passer en mode monitor dans mon environnement Linux ? Peut-elle faire de l'injection ? Peut-elle monter un AP ? » Plutôt que de répondre d'après la fiche technique, nous avons posé les 9 cartes ALFA en activité sur notre propre banc d'essai, pour les tester une à une dans un environnement **ASUS GX10 (ARM64)** sous **Ubuntu 24.04 LTS**, en comparant d'un coup les quatre lignes de capacités Monitor, Injection, AP et WPA3-SAE, et en signalant honnêtement lesquelles « ne peuvent pas faire quoi sur cette plateforme ».

Précisons d'abord le positionnement : tous les tests de cet article sont réalisés sur les propres équipements de Yopitek et son propre Wi-Fi de bureau, à destination de nos propres téléphones de test. C'est une vérification matérielle, par le distributeur, de la compatibilité et des limites de capacités du produit, pas un tutoriel offensif visant un réseau tiers. Le texte ne fournit aucune procédure contre un réseau externe ; les capacités liées à l'injection et au handshake sont toutes mesurées en environnement fermé en propre, à destination de nos propres appareils.

C'est un article Hub de type tableau récapitulatif. La configuration pas à pas et les preuves complètes de chaque carte sont détaillées dans des articles individuels approfondis (voir « Pour aller plus loin » en fin d'article).

## Plateforme et méthode de test

- **Plateforme de calcul** : ASUS GX10 (ARM64 / aarch64)
- **Système d'exploitation** : Ubuntu 24.04 LTS
- **Version du kernel** : kernel 6.17.0-1014-nvidia
- **Stratégie de pilote** : les 9 cartes utilisent toutes le pilote intégré (in-kernel), reconnues dès le branchement, sans aucun module DKMS tiers
- **Appareil de test** : Apple iPhone 7 Plus (compatibilité WPA3-SAE aussi revérifiée sur iPhone 15 Pro)
- **Environnement de test** : Wi-Fi de bureau en propre, SSID `YUPITEK`, 2,4 GHz ch5 / 5 GHz ch36, ch157
- **Période de test** : mesures sur machine réelle du 2026-11-16 au 2026-11-18

Côté méthode, chaque carte suit le même ensemble de procédures : confirmer d'abord le chargement du pilote et la création de l'interface (`wlx*`), puis vérifier dans l'ordre le monitor, l'injection, l'AP et la connexion WPA3-SAE en 2,4 GHz / 5 GHz, et enfin valider la chaîne de capture de handshake de bout en bout à destination de notre propre téléphone. Chaque résultat est consigné sous forme de chiffre ou d'état réellement mesuré, sans extrapolation de fiche technique.

Les tableaux de cet article utilisent la légende suivante :

> ✅ réussi | 🟡 partiel ou tenable en local | ⚠️ avec limite | ❌ non pris en charge ou test en échec | N/A mode absent du pilote | ⬜ non testé (faute d'un second équipement)

## 1. Comparatif matériel et pilote

Voyons d'abord les détails matériels des 9 cartes et le pilote réellement monté sur le kernel 6.17.

| # | Modèle | Puce | USB ID | Pilote (in-kernel) | Firmware | Génération / flux | Remarque |
|---|---|---|---|---|---|---|---|
| 1 | **AWUS036ACM** | MediaTek MT7612U | — | `mt76x2u` | — | Wi-Fi 5 / 2T2R | Carte Kali recommandée par morrownr |
| 2 | **AWUS036ACHM** | MediaTek MT7610U | — | `mt76x0u` | — | Wi-Fi 5 / 1T1R (AC600) | Mono-antenne |
| 3 | **AWUS036ACH** | Realtek RTL8812AU | `0bda:8812` | `rtw88_8812au` | — | Wi-Fi 5 / 2T2R (AC1200) | Fort gain bi-antenne |
| 4 | **AWUS036ACS** | Realtek RTL8811AU | `0bda:0811` | `rtw88_8821au` | 42.4.0 | Wi-Fi 5 / 1x1 | Nomade léger |
| 5 | **AWUS036EACS** | Realtek RTL8821CU | `0bda:c820` | `rtw88_8821cu` | 24.11.0 | Wi-Fi 5 / 1x1 | Composite BT + WiFi |
| 6 | **AWUS036AX** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | — |
| 7 | **AWUS036AXER** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | Même puce, antenne intégrée (Nano) |
| 8 | **AWUS036AXM** | MediaTek MT7921AU | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | — |
| 9 | **AWUS036AXML** | MediaTek MT7921AUN | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | + BT |

Quelques points clés :

**Deux grands camps de pilotes.** Les 9 cartes relèvent de deux ensembles de pilotes in-kernel : MediaTek (`mt76x2u` / `mt76x0u` / `mt7921u`) et Realtek (`rtw88_*` / `rtw89_8852bu`). Les générations de puces couvrent le Wi-Fi 5 (6 cartes) et le Wi-Fi 6 (3 cartes : AX, AXER en `rtw89_8852bu` ; AXM, AXML en `mt7921u`).

**L'avantage le plus concret en ARM64 est « sans compilation ».** Ces 9 cartes utilisent toutes le pilote in-kernel du kernel 6.17, reconnues dès le branchement, sans avoir à gérer de module DKMS out-of-tree sur aarch64. C'est particulièrement sensible en ARM64 : beaucoup de pilotes Realtek tiers n'ont pas de binaire précompilé pour aarch64 et doivent souvent être compilés depuis les sources contre la version du kernel, avec un fort risque de pépin. Ce lot de cartes supprime entièrement cette étape.

**Même puce, modèles différents.** L'AWUS036AX et l'AWUS036AXER reposent sur la même puce RTL8832BU et le même pilote `rtw89_8852bu`, la différence étant la conception d'antenne (l'AXER adopte une antenne intégrée Nano, sans RP-SMA), ce qui se reflète plus loin dans les chiffres de réception et d'injection.

**Deux cartes sont des dispositifs composites BT + WiFi.** L'AWUS036EACS (RTL8821CU) et l'AWUS036AXML (MT7921AUN) embarquent toutes deux un Bluetooth ; cette caractéristique a un effet secondaire pratique au rebranchement, expliqué plus loin dans « Précautions de la plateforme ».

## 2. Matrice des capacités centrales : Monitor / Injection / AP / WPA3

C'est le tableau principal de l'article, et le premier à consulter lors du choix.

| # | Modèle | Monitor 2,4G | Monitor 5G | **Injection 2,4G** | **Injection 5G** | AP 2,4G | AP 5G | WPA3-SAE |
|---|---|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ | ✅ | ✅ 63–83% | ✅ 76% | ✅ | ✅ 80MHz | ✅ 2,4G |
| 2 | AWUS036ACHM | ✅ | ✅ | ✅ 96–100% | ⚠️ diffusion uniquement | ✅ | ✅ | ✅* 2,4G |
| 3 | AWUS036ACH | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ | ✅ 2,4G |
| 4 | AWUS036ACS | ✅ | ✅ | ✅ **100%** | ✅ 96% | ✅ | ✅ (802.11a, 20 MHz ; VHT80 non testé) | ✅ 5G |
| 5 | AWUS036EACS | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ (802.11a, 20 MHz ; VHT80 non testé) | ✅ 2,4G |
| 6 | AWUS036AX | ✅ fort | ✅ fort | ✅ 96% | ✅ | ✅ | ✅ 80MHz | ✅ 2,4G |
| 7 | AWUS036AXER | ✅ fort | ✅ fort | ✅ 73% | ✅ | ✅ | ✅ 80MHz | ✅ 2,4G |
| 8 | AWUS036AXM | ✅ faible | ✅ faible | ❌ **échec** | ❌ **échec** | ✅ | ✅ 80MHz | ✅ 2,4G |
| 9 | AWUS036AXML | ✅ faible | ✅ faible | ❌ **échec** | ❌ **échec** | ✅ | ✅ 80MHz | ✅ 2,4G / 6G |

> \* Le WPA3 de l'AWUS036ACHM nécessite `sae_pwe=0` ; avec `sae_pwe=2`, l'iPhone 7 Plus ne se connecte pas.
>
> Colonne WPA3-SAE : la bande indiquée est celle réellement testée (2,4G pour toutes les cartes sauf l'ACS, testée en 5G ; l'AXML aussi testée en 6G). Les autres bandes n'ont pas été testées.

Lecture point par point :

**Monitor : les 9 cartes sont toutes utilisables, la réception variant.** En 2,4 GHz comme en 5 GHz, les 9 passent en mode monitor sans exception. La différence tient à l'agressivité du balayage et à la sensibilité de réception : les AX / AXER Wi-Fi 6 ont la meilleure réception et le balayage le plus agressif ; les AXM / AXML MT7921 passent en monitor mais sont relativement faibles. Pour une simple écoute passive ou un inventaire spectral, les 9 conviennent.

**Injection : c'est là que l'écart se creuse.** La série Realtek `rtw88` est la meilleure : l'ACH et l'EACS atteignent **100 %** en 2,4 GHz / 5 GHz, l'ACS fait 100 % en 2,4 GHz / 96 % en 5 GHz. La MediaTek `mt76` ACM est utilisable mais en milieu de tableau (2,4 GHz 63–83 %, 5 GHz 76 %) ; le 5 GHz de l'ACHM ne fait que de la diffusion, sans injection vers une cible précise. Les `rtw89` AX / AXER peuvent injecter, l'AXER ayant un taux d'injection 2,4 GHz (73 %) nettement inférieur à l'AX (96 %).

**La limite honnête la plus importante : l'injection MT7921 (AXM / AXML) échoue sur cette plateforme.** Ce n'est pas un réglage mal fait ni une incapacité intrinsèque de la puce à injecter — la cause principale est la régression du chanctx de mac80211 à partir du kernel 6.16 ; un pilote git / patché sur le même modèle peut fonctionner dans la communauté, mais le firmware verrouille le débit (correspond à morrownr/USB-WiFi #387, morrownr/mt76 #18). Sur cette plateforme, du fait de l'échec d'injection, ces deux cartes ne peuvent pas faire de deauth, et donc pas dérouler la chaîne de capture de handshake. Pour un usage nécessitant l'injection, écartez directement ces deux cartes sur cette plateforme.

**AP et WPA3 : presque toutes passent.** Les 9 cartes peuvent servir d'AP, la plupart prenant en charge le 5 GHz VHT80 (80 MHz) ; la connexion WPA3-SAE tient aussi pour toutes sur la bande testée (voir la note sous le tableau). La seule à surveiller est l'AWUS036ACHM, dont le WPA3 nécessite de régler le `sae_pwe` de hostapd à 0, sans quoi l'ancien iPhone 7 Plus ne se connecte pas (connexion OK en revérification sur iPhone 15 Pro, c'est une différence de réglage de compatibilité).

## 3. Récapitulatif des fonctions avancées et de la capacité de handshake

Creusons une couche plus loin : handshake de bout en bout, interfaces virtuelles (VIF), active monitor et mesh / IBSS.

| # | Modèle | Capture de handshake WPA | VIF | Active monitor | Ad-hoc (IBSS) | Mesh (802.11s) |
|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ **bout en bout** (.22000) | ✅ STA+AP / AP+mon | 🟡 configurable, ACK non vérifié | 🟡 en local | 🟡 en local |
| 2 | AWUS036ACHM | ✅ **bout en bout** (.22000, en 5 GHz ch36) | ✅ | 🟡 | 🟡 en local | 🟡 en local |
| 3 | AWUS036ACH | ✅ **bout en bout** (.22000) | ✅ STA+mon | ❌ -95 | 🟡 en local | ❌ -95 |
| 4 | AWUS036ACS | ✅ **bout en bout** (.22000) | ✅ | ❌ -95 | ❌ | ❌ -95 |
| 5 | AWUS036EACS | ✅ **bout en bout** (.22000, 79 ACKs) | 🟡 monitor passif + managed sur le même canal (monitor logiciel) ; pas de double VIF indépendante | ❌ -95 | ❌ | ❌ -95 |
| 6 | AWUS036AX | ✅ **bout en bout** (.22000) | ✅ STA+AP | N/A | N/A | N/A |
| 7 | AWUS036AXER | ✅ **bout en bout** (.22000) | ✅ STA+AP | N/A | N/A | N/A |
| 8 | AWUS036AXM | ❌ injection en échec | ✅ | 🟡 | N/A | N/A |
| 9 | AWUS036AXML | ❌ injection en échec | ✅ | 🟡 | N/A | N/A |

Le « bout en bout » a ici une définition précise : exécuter avec la carte une injection vers notre **propre iPhone 7 Plus de Yopitek** (connecté à notre propre SSID `YUPITEK`), capturer le 4-way handshake complet (M1–M4), puis le convertir au format hashcat `.22000` avec `hcxpcapngtool --all`. Le fait que toute la chaîne tienne ou non, voilà le point de validation de la « capacité de test d'intrusion » — pas le simple « passage en monitor ».

- **Bout en bout réussi (7 cartes sur 9)** : ACM, ACHM, ACH, ACS, EACS, AX, AXER produisent toutes un `.22000`, l'EACS recevant 79 ACKs, le retour de signal le plus solide ; l'ACH, à 100 % d'injection sur les deux bandes, a exporté un `.22000` de 47 hashlines en revérification le 2026-11-19. L'ACHM l'a mené à terme en 5 GHz (ch36) ; l'ACM l'a réussi malgré un taux d'injection plus faible.
- **Chaîne rompue en bout en bout** : l'AXM / AXML, du fait de l'échec d'injection, voient toute la chaîne de handshake rompue. Ce qui confirme à nouveau : le MT7921 est inadapté au test d'intrusion sur cette plateforme.
- **VIF (coexistence d'interfaces virtuelles)** : les 9 cartes prennent en charge une forme de coexistence multi-interface ; les Realtek rtw89 peuvent faire tourner STA + AP en même temps, tandis que l'EACS ne gère qu'un monitor passif avec une interface managed sur le même canal (monitor logiciel), pas de doubles VIF indépendantes.
- **Active monitor (avec retour d'ACK)** : les `rtw88` ACH / ACS / EACS renvoient -95 (non pris en charge) ; les `rtw89` AX / AXER n'ont pas ce mode dans le pilote (N/A) ; les `mt76` / `mt7921u` sont partiellement possibles (🟡).
- **Mesh (802.11s)** : seules les `mt76` ACM / ACHM savent le monter en local (🟡, une seconde carte étant nécessaire pour valider l'interconnexion complète) ; les Realtek `rtw88` renvoient -95 (non pris en charge), et les pilotes `rtw89` et `mt7921u` n'ont pas ce mode. Pour une expérimentation mesh, le MediaTek `mt76` est la seule option de ce lot.
- **IBSS (Ad-hoc)** : les `mt76` ACM / ACHM et la `rtw88` ACH peuvent toutes faire un join en local (🟡) ; l'EACS liste l'iftype mais le join est sans effet en test, et les `rtw89` AX / AXER n'ont pas d'iftype IBSS (N/A).

### Compatibilité au niveau des outils Kali / aircrack (commune à la plateforme)

Les outils suivants relèvent du niveau plateforme sur les 9 cartes, indépendamment de chaque carte :

| Outil | État | Commentaire |
|---|---|---|
| airmon-ng | ✅ | Détection / gestion de toutes les cartes ; **n'exécutez jamais `check kill`** (il arrête NetworkManager et déconnecte le GX10) |
| kismet | ✅ | Chaque carte démarre comme data source et produit un log `.kismet` |
| bettercap | ✅ | `wifi.recon` et channel hopper normaux |
| wifite (git 3.0.0) | ✅ | Balayage et constitution de liste de cibles (version git requise, la version apt entre en conflit avec l'aircrack-ng compilé maison) |
| Wireshark / tshark | ✅ | Capture et analyse monitor normales |
| **hcxdumptool 8.x** | ⚠️ | **failed to arm sur toutes les cartes, sauf l'EACS en 2,4 GHz (échec en 5 GHz)** : exige l'active-monitor, que ni `rtw88`, ni `rtw89`, ni `mt7921u` ne prennent en charge → utilisez `airodump-ng` + `aireplay-ng` |

Complément ARM64 : `aircrack-ng` doit être compilé depuis les sources, et `wifite` est conseillé en version git 3.0.0, pour contourner le conflit de dépendances entre le paquet apt et la version compilée maison.

## 4. Conseils de choix par usage

Synthétisons les trois tableaux ci-dessus en « choisir directement selon l'usage ».

| Usage | Premier choix | Commentaire |
|---|---|---|
| **Test d'intrusion (injection + handshake)** | **AWUS036EACS** / AWUS036ACS / AWUS036ACH | Meilleure injection sur les deux bandes (EACS, ACH à 100 %) ; bout en bout `.22000` prouvé sur EACS, ACS, ACH (ACH revérifiée le 2026-11-19) |
| **Meilleure réception / monitor longue portée** | **AWUS036AXER** / AWUS036ACH | L'AXER détecte 63 AP + 12 clients en un balayage en saut de fréquence ; l'ACH a un fort gain bi-antenne |
| **Wi-Fi 6 + point d'accès** | AWUS036AX / AWUS036AXER | 2x2 VHT80, AP stable et injection disponible |
| **Pur AP / connexion ordinaire (sans injection)** | AWUS036AXM / AWUS036AXML | MediaTek stable en connexion, mais **injection en échec**, inadaptée à l'usage d'intrusion |
| **Expérimentation mesh / IBSS** | AWUS036ACM / AWUS036ACHM | Le pilote `mt76` crée mesh et IBSS en local (la `rtw88` ACH ne fait que l'IBSS en local, pas le mesh ; le `rtw89` ne déclare ni l'un ni l'autre) |

Quelques conclusions en clair :

- **Pour le test d'intrusion, pour capturer un handshake** : 7 cartes sur 9 ont un bout en bout `.22000` prouvé avec dépôt de fichier — **AWUS036EACS** (le plus solide, 79 ACKs), **AWUS036ACS**, les Wi-Fi 6 AWUS036AX / AWUS036AXER, **AWUS036ACM** et **AWUS036ACHM** (5 GHz), et **AWUS036ACH** (100 % d'injection sur les deux bandes, `.22000` de 47 hashlines exporté en revérification le 2026-11-19).
- **Pour la plus grande portée de réception, la plus large écoute** : AWUS036AXER (Wi-Fi 6, antenne intégrée Nano + réglage de la puce, balayage en saut de fréquence le plus agressif) ou AWUS036ACH à fort gain bi-antenne.
- **Pour monter un point d'accès Wi-Fi 6** : AWUS036AX / AWUS036AXER, 2x2 VHT80 avec injection prise en charge.
- **Pour une simple connexion stable / un simple AP** : la solution MediaTek AWUS036AXM / AWUS036AXML est stable en connexion, sans problème au quotidien.
- **Pour jouer avec le mesh** : dans ce lot, seules les `mt76` AWUS036ACM / AWUS036ACHM y parviennent (pour l'IBSS en local, la `rtw88` AWUS036ACH peut aussi faire un join).

**Piège à éviter (le plus important)** : si votre usage est l'**injection ou le handshake**, **ne choisissez pas l'AWUS036AXM / AWUS036AXML**. Le MT7921 échoue à l'injection sur la plateforme ASUS GX10 (ARM64 / Ubuntu 24.04 / stock kernel 6.17) ; la cause principale est la régression du chanctx de mac80211 à partir du kernel 6.16 (pas intrinsèque à la puce), ce n'est pas un problème de configuration ; un pilote git / patché sur le même modèle peut fonctionner dans la communauté, mais le firmware verrouille le débit, et sur le stock kernel de cette plateforme l'injection reste impossible. Réservez-les aux scénarios « pure connexion / pur AP ».

## 5. Précautions de la plateforme (pratique GX10 ARM64)

Voici les points pratiques communs aux 9 cartes lorsqu'on les manipule sur ASUS GX10 + Ubuntu 24.04 (ARM64) :

1. **Ne coupez pas votre propre réseau** : n'exécutez jamais `airmon-ng check kill`, il arrête NetworkManager et déconnecte tout le GX10. Opérez uniquement sur l'interface externe `wlx*`, sans toucher à la ligne principale d'accès Internet intégrée.
2. **Dépannage du RX stall** : après des bascules répétées monitor / AP, si plus rien n'est détecté, c'est généralement un RX stall ; débranchez/rebranchez la carte une fois pour récupérer (ré-énumération USB, le nom d'interface nommé d'après la MAC ne change pas).
3. **Dispositif composite BT + WiFi** : l'EACS et l'AXML embarquent un Bluetooth ; au rebranchement, la probe WiFi se bloque parfois sans créer d'interface `wlx` ; changer de port USB résout généralement le problème.
4. **Déverrouillage du TX 5 GHz** : avant une injection 5 GHz en environnement propre, réglez d'abord le bon domaine réglementaire pour déverrouiller la puissance TX, puis remettez le domaine local après le test. C'est le préalable à l'émission correcte en 5 GHz.
5. **Astuce de capture de handshake** : au bureau, plusieurs AP portent souvent le même nom ; en pratique, plutôt que de verrouiller un seul BSSID, il est plus robuste de capturer tout le canal, et d'utiliser `hcxpcapngtool --all` pour l'export.
6. **hcxdumptool échoue en failed to arm sur toute la plateforme (exception : l'EACS en 2,4 GHz)** : la carte intégrée tri-bande et les pilotes ci-dessus ne prennent pas en charge l'active-monitor ; utilisez directement la suite aircrack-ng (`airodump-ng` + `aireplay-ng`).
7. **Détails de compilation ARM64** : `aircrack-ng` doit être compilé depuis les sources, et `wifite` en version git pour contourner le conflit de dépendances apt.

Rappelons encore le positionnement : les capacités d'injection / deauth / handshake ci-dessus sont toutes mesurées en environnement fermé en propre chez Yopitek, à destination de nos propres appareils de test, dans le but de vérifier les capacités du produit et les limites de compatibilité. Cet article ne fournit ni ne conseille les opérations ci-dessus contre un quelconque réseau tiers.

## Conclusion

Sur la plateforme ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17), l'évaluation globale des 9 cartes ALFA tient en trois phrases : **le Monitor est disponible pour toutes, l'AP et le WPA3 passent pour presque toutes, la ligne de partage est l'Injection.** Pour un usage professionnel nécessitant injection et handshake, les Realtek `rtw88` EACS / ACH / ACS sont les choix les plus sûrs ; pour la réception et le Wi-Fi 6, voyez l'AXER / AX ; les MT7921 AXM / AXML sont à réserver aux scénarios de pure connexion. Toutes sans compilation, prêtes à l'emploi : voilà le plus grand avantage commun de ce lot de cartes en ARM64.

## Questions fréquentes (FAQ)

**Q : L'AWUS036AXM peut-elle injecter (injection) sous Ubuntu ?**
R : Pas sur cette plateforme. En test, l'AWUS036AXM et l'AWUS036AXML (toutes deux en puce MT7921) échouent à l'injection en 2,4 GHz comme en 5 GHz, la cause principale étant la régression du chanctx de mac80211 du stock kernel 6.16+ (pas intrinsèque à la puce) ; elles sont donc déconseillées sur cette plateforme pour un usage nécessitant l'injection ou la capture de handshake.

**Q : Quelle carte Wi-Fi ALFA a le meilleur taux de réussite d'injection sous Ubuntu ?**
R : En test, l'AWUS036ACH et l'AWUS036EACS atteignent 100 % de taux de réussite d'injection en 2,4 GHz comme en 5 GHz : ce sont les deux meilleures des 9 cartes de ce lot.

**Q : Les 9 cartes Wi-Fi ALFA nécessitent-elles l'installation d'un pilote sous Ubuntu 24.04 ?**
R : Non. Les 9 cartes utilisent toutes le pilote intégré (in-kernel) sur le kernel 6.17 (familles rtw88 / rtw89 / mt76), reconnues dès le branchement, sans compilation de module DKMS.

**Q : Les cartes Wi-Fi ALFA peuvent-elles monter un point d'accès WPA3-SAE sous Ubuntu ?**
R : Oui, les 9 cartes montent avec succès un point d'accès WPA3-SAE et laissent les appareils se connecter (testé en 2,4 GHz pour chaque carte sauf l'ACS, testée en 5 GHz ; l'AXML aussi testée en 6 GHz) ; seule l'AWUS036ACHM nécessite de régler le `sae_pwe` de hostapd à 0, sans quoi l'ancien iPhone 7 Plus échoue à se connecter.

**Q : Ces résultats de test sous Ubuntu sont-ils exploitables par les utilisateurs de Kali Linux ?**
R : Kali Linux repose sur l'écosystème Debian/Ubuntu et utilise les mêmes pilotes in-kernel rtw88 / rtw89 / mt76 ; la compatibilité des pilotes et la matrice de capacités de cet article peuvent donc, en principe, servir de référence aux utilisateurs de Kali ; mais la plateforme de test de cet article est Ubuntu 24.04, non encore officiellement revérifiée sur Kali — référez-vous à une revérification ultérieure.

## Pour aller plus loin

Cet article est le Hub récapitulatif. Les articles approfondis et tests carte par carte suivants sont mis en ligne progressivement (liens en construction) :

- « Sans installation de pilote : activer les modes Monitor et AP sous Ubuntu (ARM64) » → [`/fr/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/fr/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- « Pratique de la capture de handshake WPA3-SAE (vérifié en environnement propre) » → [`/fr/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/fr/blog/alfa-wpa3-sae-handshake-capability-arm64/)

9 tests individuels approfondis :

- [Test individuel de l'AWUS036ACM](/fr/blog/awus036acm-asus-gx10-ubuntu-test-report/)
- [Test individuel de l'AWUS036ACHM](/fr/blog/awus036achm-asus-gx10-ubuntu-test-report/)
- [Test individuel de l'AWUS036ACH](/fr/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- [Test individuel de l'AWUS036ACS](/fr/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- [Test individuel de l'AWUS036EACS](/fr/blog/awus036eacs-asus-gx10-ubuntu-test-report/)
- [Test individuel de l'AWUS036AX](/fr/blog/awus036ax-asus-gx10-ubuntu-test-report/)
- [Test individuel de l'AWUS036AXER](/fr/blog/awus036axer-asus-gx10-ubuntu-test-report/)
- [Test individuel de l'AWUS036AXM](/fr/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- [Test individuel de l'AWUS036AXML](/fr/blog/awus036axml-asus-gx10-ubuntu-test-report/)

---

*Unité de test : Yopitek (distributeur ALFA Network à Taïwan) | Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Appareil de test : Apple iPhone 7 Plus (WPA3 aussi testé sur iPhone 15 Pro) | Environnement de test : Wi-Fi de bureau en propre. Cet article est une vérification de compatibilité produit et de capacités, pas un tutoriel d'opérations visant un réseau tiers.*
