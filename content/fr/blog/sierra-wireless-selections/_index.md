---
title: "Guide Complet de Sélection des Modules Cellulaires Sierra Wireless : Du LTE Cat 4 au 5G mmWave"
date: 2026-07-30
slug: "sierra-wireless-selections"
tags:
  - sierra-wireless
  - module-cellulaire
  - 4g-lte
  - 5g-nr
  - guide-de-sélection
  - em7455
  - em9190
  - m2-pcie
  - communication-sans-fil
categories:
  - Guide de Sélection de Produits
series:
  - sierra-wireless-selection
series_order: 1
description: "Yupitek te présente une comparaison complète de dix modules cellulaires Sierra Wireless (Semtech) des séries EM/MC, du LTE Cat 4 au 5G mmWave. EM7455, EM9190, MC7455 et plus."
author: "yupitek"
draft: false
faq:
  - question: "Quels sont les modèles Sierra Wireless disponibles et quelles sont leurs différences ?"
    answer: "Sierra Wireless propose actuellement deux grandes séries — EM et MC — avec dix modules au total, couvrant du LTE Cat 4 / Cat 6 / Cat 12 jusqu'à la 5G Sub-6 et mmWave. La différence principale réside dans le format : EM en M.2, MC en mPCIe. Pour une même puce (ex. EM7455 et MC7455), les performances sont strictement identiques, seul le connecteur change."
  - question: "Est-ce que l'EM7455 et le MC7455 utilisent la même puce ?"
    answer: "Oui. Tous deux utilisent le chipset Qualcomm MDM9230, avec des pics descendants/montants identiques de 300 / 50 Mbps et le support de l'agrégation 2×CA. Les spécifications sont rigoureusement les mêmes — seule la différence de format : M.2 pour l'EM7455, mPCIe pour le MC7455."
  - question: "Faut-il absolument choisir un module mmWave (EM9191) pour la 5G ? Peut-on l'utiliser en France ?"
    answer: "Pas forcément. En Europe, le déploiement 5G se fait principalement en Sub-6, le mmWave étant surtout déployé aux États-Unis (bandes n260/n261). Pour la plupart des applications en France et en Europe, l'EM9190 (5G Sub-6 abordable) suffit amplement. L'EM9191 n'est nécessaire que si tu as besoin du mmWave américain."
  - question: "Comment choisir entre un module M.2 et un module mPCIe ?"
    answer: "Tout dépend du connecteur de ton appareil. Les PC portables et les cartes mères embarquées modernes utilisent du M.2 B-Key — choisis la série EM. Les routeurs industriels anciens et les box industrielles avec slot mPCIe — prends la série MC. Si ta carte n'a que du M.2 mais que tu veux un module MC, il faudra un adaptateur M.2 vers mPCIe."
  - question: "Où acheter des modules Sierra Wireless en France ?"
    answer: "Tu peux te procurer toute la gamme de modules cellulaires Sierra Wireless auprès de Yupitek. Rends-toi sur notre site pour consulter les références et les prix, ou envoie-nous un email à sales@yupitek.com."
---
Tu crains de te perdre dans les fiches techniques, de confondre les modèles ou d'acheter le mauvais format pour ton appareil ? Cet article te présente clairement les dix modules phares et historiques de Sierra Wireless, pour t'aider à choisir du LTE Cat 4 jusqu'au 5G mmWave.

Sierra Wireless appartient désormais à Semtech. Ce guide a été préparé par Yupitek et couvre dix modules cellulaires Sierra Wireless : EM7430, EM7455, EM7511, EM7565, EM9190, EM9191, MC7304, MC7350, MC7354 et MC7455. Les modules de la série EM sont au format M.2, ceux de la série MC au format mPCIe.

Les données techniques de cet article sont compilées par Yupitek.

Les dix modules couvrent du LTE Cat 4 / 6 / 12 à la 5G Sub-6 et mmWave. Les séries EM et MC ne diffèrent que par le format : EM en M.2, MC en mPCIe.

## Tableau comparatif des dix modules

Voici le tableau complet, basé sur les fiches techniques officielles, pour que tu puisses comparer facilement. Les pics descendants des EM9190/EM9191 peuvent varier légèrement selon les sources — avant d'acheter, vérifie la dernière fiche technique officielle ou demande-nous confirmation (voir les liens en annexe).

| Modèle | Norme Cellulaire | Chipset | Débit descendant / montant max | Agrégation de porteuses | 5G | mmWave | Format | GNSS | Remarques |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](https://yupitek.com/fr/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | Cat 6 d'entrée de gamme (vérifie la config des bandes auprès de nous) |
| [EM7455](https://yupitek.com/fr/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | Le plus populaire de la communauté, le plus de tutoriels |
| [EM7511](https://yupitek.com/fr/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | Cat 12 à débit montant élevé |
| [EM7565](https://yupitek.com/fr/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | Supporte bandes CBRS/LAA (vérifie la certification), max de bandes et débit montant |
| [EM9190](https://yupitek.com/fr/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | 2.5 Gbps descendant (pic montant — contacte-nous) | 8×CA | ✓ | — | M.2 | ✓ | Entrée de gamme 5G Sub-6 abordable |
| [EM9191](https://yupitek.com/fr/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | Jusqu'à 4.5 Gbps descendant (mmWave) / 2.5 Gbps Sub-6 (pic montant — contacte-nous) | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | Flagship 5G, inclut mmWave |
| [MC7304](https://yupitek.com/fr/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4 d'entrée de gamme (proche EOL) |
| [MC7350](https://yupitek.com/fr/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4, bandes Amérique du Nord |
| [MC7354](https://yupitek.com/fr/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4, bandes globales |
| [MC7455](https://yupitek.com/fr/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | Version mPCIe de l'EM7455 |

> **Note :** L'EM9190 et l'EM9191 partagent la même fiche technique EM919x/EM7690. L'EM9190 est la version 5G Sub-6 abordable, tandis que l'EM9191 ajoute le mmWave pour une configuration flagship. Cette fiche officielle est en accès réservé aux membres — les chiffres de débit descendant que nous citons sont compilés à partir de sources publiques. Pour les détails comme le pic montant, contacte-nous avant de commander pour obtenir la version la plus récente.

## Différences de format : série EM (M.2) vs série MC (mPCIe)

C'est le premier critère de sélection, et aussi celui sur lequel on fait le plus d'erreurs.

**Série EM = format M.2 B-Key :** format compact (environ 30×42 mm), conçu pour les slots WWAN des PC portables et les connecteurs M.2 embarqués. La plupart des cartes mères industrielles modernes et des mini-PC l'adoptent.

**Série MC = format Mini PCIe (mPCIe) :** aspect identique à une carte d'extension PC classique, conçu pour les slots mPCIe des routeurs industriels anciens et des box industrielles. Si ta carte n'a que du M.2, il te faudra un adaptateur M.2 vers mPCIe pour utiliser un module MC.

**Prérequis communs :** les deux formats nécessitent un porte-SIM externe et des antennes. Les connecteurs d'antenne sont généralement des U.FL, avec une configuration typique en 2×2 MIMO (antenne principale + antenne de diversité) plus une antenne GNSS.

**Un point qu'on nous demande souvent :** l'EM7455 et le MC7455 sont « la même puce, seul le format change » — tous deux utilisent le Qualcomm MDM9230, avec des spécifications rigoureusement identiques. La seule différence est le connecteur : M.2 ou mPCIe. Le choix se résume donc à ton équipement.

## Recommandations par cas d'usage

### Routeurs sans fil / CPE (OpenWrt / ROOter)

**Recommandé : [EM7455](https://yupitek.com/fr/products/sierra/em7455/) / [MC7455](https://yupitek.com/fr/products/sierra/mc7455/)**
Pourquoi : c'est le duo le plus documenté de la communauté. Les tutoriels ROOter (firmware OpenWrt spécialisé routeur cellulaire) et les exemples de configuration QMI/MBIM sont les plus nombreux — si tu as un problème, tu trouves la réponse sur Google.

### Mise à niveau WWAN pour PC portable

**Recommandé : [EM7430](https://yupitek.com/fr/products/sierra/em7430/) / [EM7455](https://yupitek.com/fr/products/sierra/em7455/)**
Pourquoi : les deux sont en format M.2, compatibles avec les slots WWAN des PC portables Dell, Lenovo et autres machines professionnelles. L'EM7455 est bien connu pour sa couverture de bandes étendue et son prix bas en occasion — c'est le choix numéro un pour une upgrade (contacte-nous avant de commander pour vérifier la compatibilité des bandes avec ton opérateur).

### Routeurs industriels / Passerelles (température étendue, certifications, longue disponibilité)

**Recommandé : série EM75 ([EM7511](https://yupitek.com/fr/products/sierra/em7511/), [EM7565](https://yupitek.com/fr/products/sierra/em7565/)), [EM9190](https://yupitek.com/fr/products/sierra/em9190/)/[EM9191](https://yupitek.com/fr/products/sierra/em9191/), [MC7455](https://yupitek.com/fr/products/sierra/mc7455/)**
Pourquoi : dans l'industrie, on privilégie la tenue en température (options −40°C), les certifications complètes et la garantie d'approvisionnement long terme. Les modules Cat 12 et 5G offrent un débit montant plus élevé et une marge de bande passante pour le futur. Les spécifications exactes de température et les certifications sont à vérifier sur la fiche technique officielle — contacte-nous pour obtenir la version la plus récente avant de finaliser ton choix.

### Télématique embarquée / Flotte (géolocalisation GNSS)

**Recommandé : [EM7455](https://yupitek.com/fr/products/sierra/em7455/) / [EM7565](https://yupitek.com/fr/products/sierra/em7565/) / [EM9191](https://yupitek.com/fr/products/sierra/em9191/)**
Pourquoi : ces trois modules intègrent le GNSS, parfait pour le tracking embarqué et la remontée de position. Si ton application embarquée a besoin de 5G haut débit, choisis l'EM9191.

### Réseaux privés 5G / CBRS

**Recommandé : [EM9191](https://yupitek.com/fr/products/sierra/em9191/) (bandes CBRS), [EM7565](https://yupitek.com/fr/products/sierra/em7565/) (bandes CBRS/LAA)**
Pourquoi : le CBRS (bande partagée 3.5 GHz aux États-Unis) et le LAA sont des besoins courants pour les réseaux privés. L'EM9191 et l'EM7565 supportent ces bandes au niveau matériel. Avant de déployer un réseau privé, vérifie la réglementation locale et l'environnement opérateur — contacte-nous pour une évaluation technique complète.

### Surveillance vidéo / Retour haut débit pour affichage numérique

**Recommandé : [EM9190](https://yupitek.com/fr/products/sierra/em9190/) / [EM9191](https://yupitek.com/fr/products/sierra/em9191/)**
Pourquoi : le haut débit 5G (jusqu'à 2.5 Gbps descendant en Sub-6, jusqu'à 4.5 Gbps avec mmWave) est idéal pour la remontée temps réel de plusieurs flux vidéo et le streaming d'affichage 4K.

### Maintenance / Pièces de rechange long terme (Cat 4)

**Recommandé : [MC7304](https://yupitek.com/fr/products/sierra/mc7304/) / [MC7350](https://yupitek.com/fr/products/sierra/mc7350/) / [MC7354](https://yupitek.com/fr/products/sierra/mc7354/)**
Pourquoi : ces modules Cat 4 en format mPCIe sont les pièces de rechange idéales pour la maintenance des anciens équipements. Attention cependant : la série MC73xx approche de sa fin de vie (EOL). Pour un approvisionnement long terme, on te recommande de migrer vers l'[EM7455](https://yupitek.com/fr/products/sierra/em7455/) ou l'[EM7565](https://yupitek.com/fr/products/sierra/em7565/), qui offrent une disponibilité prolongée.

## Contact et devis

Tu hésites encore sur ton choix ? Tu peux te procurer les dix modules EM/MC Sierra Wireless présentés dans cet article auprès de Yupitek, ainsi que les antennes, adaptateurs SIM et cartes d'évaluation associés. On t'accompagne sur la vérification des spécifications, la comparaison des bandes, le devis quantité et le support technique.

## Questions fréquentes (FAQ)

**Q1 : Quels sont les modèles Sierra Wireless disponibles et quelles sont leurs différences ?**
Sierra Wireless propose actuellement deux grandes séries — EM et MC — avec dix modules au total, couvrant du LTE Cat 4 / Cat 6 / Cat 12 jusqu'à la 5G Sub-6 et mmWave. La différence principale réside dans le format : EM en M.2, MC en mPCIe. Pour une même puce (ex. EM7455 et MC7455), les performances sont strictement identiques, seul le connecteur change.

**Q2 : Est-ce que l'EM7455 et le MC7455 utilisent la même puce ?**
Oui. Tous deux utilisent le chipset Qualcomm MDM9230, avec des pics descendants/montants identiques de 300 / 50 Mbps et le support de l'agrégation 2×CA. Les spécifications sont rigoureusement les mêmes — seule la différence de format : M.2 pour l'EM7455, mPCIe pour le MC7455.

**Q3 : Faut-il absolument choisir un module mmWave (EM9191) pour la 5G ? Peut-on l'utiliser en France ?**
Pas forcément. En Europe, le déploiement 5G se fait principalement en Sub-6, le mmWave étant surtout déployé aux États-Unis (bandes n260/n261). Pour la plupart des applications en France et en Europe, l'EM9190 (5G Sub-6 abordable) suffit amplement. L'EM9191 n'est nécessaire que si tu as besoin du mmWave américain.

**Q4 : Comment choisir entre un module M.2 et un module mPCIe ?**
Tout dépend du connecteur de ton appareil. Les PC portables et les cartes mères embarquées modernes utilisent du M.2 B-Key — choisis la série EM. Les routeurs industriels anciens et les box industrielles avec slot mPCIe — prends la série MC. Si ta carte n'a que du M.2 mais que tu veux un module MC, il faudra un adaptateur M.2 vers mPCIe.

**Q5 : Où acheter des modules Sierra Wireless en France ?**
Tu peux te procurer toute la gamme de modules cellulaires Sierra Wireless auprès de Yupitek. Rends-toi sur notre site pour consulter les références et les prix, ou envoie-nous un email à sales@yupitek.com.

## Annexe : Liens vers les fiches techniques officielles

Les liens ci-dessous fournissent des copies PDF des fiches techniques de chaque module (téléchargement direct, sans connexion), issues de la base de ressources techniques officielle de Sierra Wireless (source.sierrawireless.com). Pour les MC7350 et MC7354, les liens externes d'origine sont conservés car aucun PDF individuel n'est disponible (connexion requise). Les chiffres de cet article sont compilés à partir des données publiquement accessibles. Si tu as besoin des valeurs exactes à vérifier ligne par ligne (notamment les pics montants des EM9190/EM9191), contacte-nous pour obtenir les documents officiels :

- **EM7430** : https://yupitek.com/docs/sierra/em7430_spec.pdf
- **EM7455** : https://yupitek.com/docs/sierra/em7455_spec.pdf
- **EM7511** : https://yupitek.com/docs/sierra/EM7511_spec.pdf
- **EM7565** : https://yupitek.com/docs/sierra/EM7565_spec.pdf
- **EM9190 / EM9191** : https://yupitek.com/docs/sierra/EM919x.pdf
- **MC7304** : https://yupitek.com/docs/sierra/MC7304_spec.pdf
- **MC7350** : https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354** : https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455** : https://yupitek.com/docs/sierra/mc7455_spec.pdf
