---
title: "Guide d'achat des modules cellulaires Sierra Wireless : du LTE Cat 4 au 5G mmWave"
description: "Le comparatif complet des dix modules cellulaires Sierra Wireless (Semtech) des séries EM/MC, du LTE Cat 4 au 5G mmWave : spécifications, formats de boîtier et conseils de sélection. Données techniques compilées par Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "lte", "5g", "mmwave", "m2", "mpcie", "module-selection"]
featureimage: "/images/products/sierra/sierra_banner.png"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "Quels modules Sierra Wireless existent, et quelles sont leurs différences ?"
    answer: "Sierra Wireless propose actuellement dix modules répartis en deux séries, EM et MC, couvrant le LTE Cat 4, Cat 6, Cat 12, le 5G Sub-6 et le mmWave. La plus grosse différence tient au format : les modules EM utilisent le M.2, les MC le mPCIe. Les modèles sur le même chipset, comme l'EM7455 et le MC7455, offrent les mêmes performances et ne diffèrent que par la forme du connecteur."
  - question: "L'EM7455 et le MC7455 utilisent-ils la même puce ?"
    answer: "Oui. Les deux reposent sur le chipset Qualcomm MDM9230 avec des débits de pointe identiques de 300/50 Mbit/s et l'agrégation de porteuses 2×CA. La seule différence, c'est le format : l'EM7455 est en M.2, le MC7455 en mPCIe."
  - question: "Faut-il forcément prendre le mmWave (EM9191) pour la 5G ? Est-ce qu'il fonctionne à Taïwan ?"
    answer: "Pas forcément. Les réseaux 5G taïwanais s'appuient aujourd'hui surtout sur le Sub-6, tandis que le mmWave est surtout déployé dans les environnements de type américain (bandes n260/n261). Pour la plupart des projets à Taïwan, l'EM9190 (5G Sub-6 économique) suffit ; ne choisissez l'EM9191 que si vous avez un vrai besoin de test mmWave aux normes américaines."
  - question: "Comment choisir entre un module cellulaire M.2 et mPCIe ?"
    answer: "Tout dépend du connecteur de votre appareil. Les laptops et les cartes embarquées modernes utilisent généralement le M.2 B-Key : prenez la série EM. Les routeurs industriels anciens et les PC industriels avec connecteur mPCIe prendront la série MC. Si votre carte n'a que du M.2 mais que vous voulez un module MC, il vous faudra un adaptateur M.2 vers mPCIe."
  - question: "Où acheter des modules Sierra Wireless à Taïwan ?"
    answer: "Vous pouvez vous procurer toute la gamme de modules cellulaires Sierra Wireless via Yupitek. Consultez les pages produits du site Yupitek pour les modèles et les prix, ou écrivez directement à sales@yupitek.com."
---

# Guide d'achat des modules cellulaires Sierra Wireless : du LTE Cat 4 au 5G mmWave

Que vous soyez étudiant en train de monter un projet IoT ou ingénieur en train de développer du matériel réseau en laboratoire, le pire dans l'achat d'un module cellulaire est toujours le même : vous passez une heure sur les fiches techniques, les numéros de modèle se mélangent, et vous finissez avec le mauvais format qui ne rentre tout simplement pas dans votre appareil.

Ce guide passe en revue les dix modules Sierra Wireless actuels et durables (désormais filiale de Semtech), du LTE Cat 4 d'entrée de gamme jusqu'au 5G mmWave. Tous les modules de la série EM abordés ici utilisent le format M.2, tandis que la série MC est en mPCIe.

Les données techniques de cet article ont été compilées par Yupitek.

## Le tableau des dix modules : les chiffres d'abord

On commence par le tableau essentiel ! Tous les chiffres sont issus des fiches techniques officielles, pour comparer directement. Une remarque : les débits de pointe en liaison montante (upload) de l'EM9190/EM9191 peuvent varier légèrement selon les sources. Si vous achetez pour un vrai projet, vérifiez la dernière fiche technique officielle ou demandez-nous directement (liens en annexe).

| Modèle | Standard cellulaire | Chipset | Débit de pointe descendant / montant | Agrégation de porteuses | 5G | mmWave | Format | GNSS | Remarque |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](/fr/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbit/s | 2×CA | — | — | M.2 | ✓ | Cat 6 d'entrée de gamme (configuration des bandes à confirmer) |
| [EM7455](/fr/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbit/s | 2×CA | — | — | M.2 | ✓ | Le plus populaire dans la communauté open source, le plus de tutoriels |
| [EM7511](/fr/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbit/s | 3×CA | — | — | M.2 | ✓ | Cat 12 avec uplink élevé |
| [EM7565](/fr/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbit/s | 3×CA | — | — | M.2 | ✓ | Supporte les bandes CBRS/LAA, le plus de bandes et l'uplink le plus élevé |
| [EM9190](/fr/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | 2.5 Gbit/s en descendant (pic montant sur demande) | 8×CA | ✓ | — | M.2 | ✓ | Point d'entrée économique du 5G Sub-6 |
| [EM9191](/fr/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | jusqu'à 4.5 Gbit/s descendant incl. mmWave / 2.5 Gbit/s Sub-6 (pic montant sur demande) | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | Le 5G phare, ondes millimétriques incluses |
| [MC7304](/fr/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbit/s | — | — | — | mPCIe | ✓ | Cat 4 d'entrée de gamme (proche de la fin de vie EOL) |
| [MC7350](/fr/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbit/s | — | — | — | mPCIe | ✓ | Cat 4, orienté bandes nord-américaines |
| [MC7354](/fr/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbit/s | — | — | — | mPCIe | ✓ | Cat 4, bandes mondiales |
| [MC7455](/fr/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbit/s | 2×CA | — | — | mPCIe | ✓ | En clair, la version mPCIe de l'EM7455 |

> Note : l'EM9190 et l'EM9191 partagent le même document de spécification (EM919x/EM7690). L'EM9190 est le 5G Sub-6 économique, tandis que l'EM9191 ajoute le mmWave pour le haut de gamme. La fiche technique officielle ne se télécharge qu'après connexion au compte, donc les débits descendants du tableau proviennent de sources publiques. Pour les pics montants et autres détails, mieux vaut nous confirmer la dernière version avant de passer commande.

## Premier cap : quelle différence entre la série EM (M.2) et la série MC (mPCIe) ?

C'est l'écueil numéro un des débutants ! Acheter le mauvais format et ne pas pouvoir l'insérer, c'est vraiment gênant.

**Série EM = format M.2 B-Key.** Imaginez l'interface dans laquelle on insère un SSD dans un laptop : très compacte (environ 30×42 mm). Ces modules sont conçus pour les slots WWAN de laptops et les connecteurs M.2 embarqués, ceux qu'utilisent la plupart des cartes mères industrielles récentes et des mini-PC.

**Série MC = format Mini PCIe (mPCIe).** Visuellement proches des cartes d'extension des vieux ordinateurs, ils conviennent aux connecteurs mPCIe des routeurs industriels et PC industriels plus anciens. Si votre carte n'a qu'un slot M.2, utiliser un module MC exige une carte adaptatrice séparée (M.2 vers mPCIe).

**Ce qu'ils ont en commun :** les deux ont besoin d'un support de carte SIM externe et d'antennes. Les connecteurs d'antenne sont généralement en U.FL, avec une configuration standard 2×2 MIMO (une antenne principale plus une antenne de diversité), et une antenne GNSS supplémentaire pour la géolocalisation.

**La question qu'on nous pose tout le temps :** quelle est la vraie différence entre l'EM7455 et le MC7455 ? Réponse : « même puce, seul le format change ». Les deux cartes utilisent le Qualcomm MDM9230 avec des spécifications identiques, donc le choix se résume vraiment à l'apparence de votre carte mère.

## Nos recommandations selon votre projet ou cas d'usage

### 1. Monter son propre routeur / CPE (avec OpenWrt ou ROOter)

**On recommande : [EM7455](/fr/products/sierra/em7455/) / [MC7455](/fr/products/sierra/mc7455/)**
La raison est simple : c'est pour ces modules que la communauté open source a le plus de ressources. Si vous utilisez ROOter (un firmware basé sur OpenWrt), les tutoriels et exemples de configuration QMI/MBIM sont très complets, et une recherche rapide sur le web vous sortira de presque tous les pièges.

### 2. Upgrader la carte WWAN d'un vieux laptop

**On recommande : [EM7430](/fr/products/sierra/em7430/) / [EM7455](/fr/products/sierra/em7455/)**
Les deux sont en M.2 et correspondent aux slots WWAN des laptops professionnels Dell, Lenovo et autres. L'EM7455 est en plus souvent très bien placé sur le marché de l'occasion et reste le favori des upgrades (mais confirmez avant de commander que les bandes correspondent à votre opérateur).

### 3. Routeurs industriels / passerelles IoT (robustesse et température étendue)

**On recommande : série EM75 ([EM7511](/fr/products/sierra/em7511/), [EM7565](/fr/products/sierra/em7565/)), [EM9190](/fr/products/sierra/em9190/)/[EM9191](/fr/products/sierra/em9191/), [MC7455](/fr/products/sierra/mc7455/)**
Dans les projets industriels, ce qui compte c'est la température étendue (pensez aux environnements rudes de -40°C à +85°C), des certifications complètes et une disponibilité à long terme. Les modules Cat 12 et 5G offrent plus de bande passante montante et une meilleure marge d'évolution. Vérifiez toujours les valeurs de température réelles dans la documentation officielle la plus récente.

### 4. Véhicules connectés / suivi de flotte (GNSS requis)

**On recommande : [EM7455](/fr/products/sierra/em7455/) / [EM7565](/fr/products/sierra/em7565/) / [EM9191](/fr/products/sierra/em9191/)**
Les projets télématiques demandent généralement un positionnement précis. Ces trois modules ont un GNSS intégré, ce qui règle connectivité et localisation avec une seule carte. Si vous avez besoin de la bande passante 5G, partez directement sur l'EM9191.

### 5. Réseaux privés 5G / expérimentations CBRS

**On recommande : [EM9191](/fr/products/sierra/em9191/) (bandes CBRS), [EM7565](/fr/products/sierra/em7565/) (bandes CBRS/LAA)**
Si vous étudiez le CBRS (la bande partagée américaine de 3.5 GHz) ou le LAA en laboratoire, les deux modules prennent en charge ces technologies au niveau matériel. Attention : tester un vrai réseau privé sur site dépend de la réglementation locale et de l'environnement opérateur, donc discutons des détails techniques avant tout déploiement.

### 6. Vidéosurveillance / renvoi de flux vidéo HD

**On recommande : [EM9190](/fr/products/sierra/em9190/) / [EM9191](/fr/products/sierra/em9191/)**
Avec une bande passante 5G aussi généreuse (jusqu'à 2.5 Gbit/s en descendant en Sub-6, et 4.5 Gbit/s avec le mmWave), ces modules sont parfaits pour le renvoi temps réel de plusieurs flux vidéo ou le streaming 4K.

### 7. Réparation d'anciens équipements / pièces détachées pour vieilles machines de labo (Cat 4)

**On recommande : [MC7304](/fr/products/sierra/mc7304/) / [MC7350](/fr/products/sierra/mc7350/) / [MC7354](/fr/products/sierra/mc7354/)**
C'est le premier choix pour entretenir les vieilles machines au format mPCIe. Mais soyons honnêtes : la série MC73xx approche de la fin de vie (EOL). Pour les projets au long cours, passer à l'[EM7455](/fr/products/sierra/em7455/) ou à l'[EM7565](/fr/products/sierra/em7565/) est plus sûr.

## Toujours indécis ? Parlez-nous-en

Si après lecture vous ne savez toujours pas quoi choisir : à Taïwan, vous pouvez vous procurer les dix modules cellulaires des séries EM/MC via Yupitek, antennes, adaptateurs SIM ou cartes d'évaluation inclus. Que ce soit pour vérifier des spécifications, comparer des bandes, ou obtenir un devis et du support technique pour votre projet, on est là pour vous.

## Questions fréquentes

{{< faq >}}

## Annexe : les fiches techniques officielles des dix modèles

Les liens ci-dessous mènent à la bibliothèque technique officielle de Sierra Wireless (source.sierrawireless.com). **Certains PDF nécessitent une inscription pour être téléchargés.** Les chiffres de l'article proviennent de sources publiques ; si vous voulez confirmer point par point des détails très précis (comme les pics montants de l'EM9190/EM9191), contactez-nous et nous vous transmettrons les documents officiels à jour.

- **EM7430** : https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7430_product_technical_specification/
- **EM7455** : https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7455_product_technical_specification/
- **EM7511** : https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7511_product_technical_specification/
- **EM7565** : https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7565_product_technical_specification/
- **EM9190 / EM9191** : https://source.sierrawireless.com/resources/airprime/minicard/airprime_em919x-7690_product_technical_specification/
- **MC7304** : https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7304_product_technical_specification_and_customer_design_guidelines/
- **MC7350** : https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354** : https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455** : https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_mc7455_product_technical_specification/
