---
title: "Sierra EM7565 en détail : réseau privé CBRS et vitesse d'envoi élevée, quel réseau privé d'entreprise choisir ?"
description: "EM7565 en détail : Cat 12 à 600 Mbit/s en téléchargement, Cat 13 à 150 Mbit/s en envoi, Qualcomm MDM9250, format M.2, MIMO à trois antennes et GNSS multi-constellation. Lecture indispensable pour choisir un réseau privé CBRS d'entreprise et un routeur industriel, avec comparaison complète des bandes, des températures et des certifications. Préparé par Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em7565", "lte-a", "cat-12", "cat-13", "cbrs", "m2", "gnss", "wwan", "private-lte"]
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "L'EM7565 prend-il en charge les réseaux privés CBRS (bande 48) ?"
    answer: "La fiche technique officielle (Rev 8, octobre 2018) liste la bande 48 (3550–3700 MHz, bande CBRS), mais marque B42/B43/B48 comme disabled au moment de la publication, en attente d'approbation réglementaire. Pour un déploiement CBRS, il faut se référer à la fiche technique officielle la plus récente, à la version du firmware et à la réglementation en vigueur."
  - question: "Quelle est la vitesse d'envoi réelle de l'EM7565 ?"
    answer: "L'envoi utilise LTE Cat 13 (2×CA contiguous, 64QAM), avec un pic théorique de 150 Mbit/s ; le téléchargement utilise Cat 12 (3×CA, 256QAM), avec un pic théorique de 600 Mbit/s. Le débit réel dépend de la station de base, de la qualité du signal et de la version du firmware."
  - question: "L'EM7565 a-t-il des antennes intégrées ? Combien d'antennes faut-il ?"
    answer: "Non, il n'y a pas d'antennes intégrées. Le module dispose de 3 connecteurs RF : Main (Tx/Rx), GNSS et Auxiliary (Diversity/MIMO/GNSS). Pour la LTE, il faut au minimum un système d'antennes externes 2×2 MIMO ; les antennes et les feeders sont à concevoir côté hôte."
  - question: "Quelle est la plage de température de fonctionnement de l'EM7565 ?"
    answer: "Classe A (conforme 3GPP) : de -30°C à +70°C ; classe B (non 3GPP) : de -40°C à +85°C, avec un refroidissement adapté et des paramètres de fonctionnement réduits. La température interne du module doit rester sous 90°C, idéalement sous 80°C."
  - question: "L'EM7565 fonctionne-t-il sous Linux ?"
    answer: "Oui. L'interface USB prend en charge QMI (Linux et Android) et MBIM (Windows 8.1/10 et Linux), et propose une interface de commandes AT 3GPP TS 27.007 ainsi qu'un SDK Linux. La prise en charge réelle des pilotes dépend de la distribution et de la version du noyau."
---


Si tu prépares un projet de laboratoire, ou si tu viens de récupérer un projet de réseau privé LTE ou CBRS pour une entreprise, tu verras forcément le module M.2 EM7565 dans la liste des candidats. Mais voilà le point clé : « souvent cité » ne veut pas dire « tu l'achètes, tu le branches, et CBRS fonctionne tout de suite ».

Dans cet article, pas de jargon marketing. Notre seule référence est la fiche technique officielle de Sierra Wireless, « AirPrime EM7565 Product Technical Specification » (Doc 41110788, Rev 8, octobre 2018). Nous vérifions point par point le chip, les vitesses, les bandes, les antennes, les températures et la certification, et nous te disons honnêtement ce que signifie la réserve « en attente d'approbation réglementaire » de la fiche. Ainsi, les étudiants et les ingénieurs en intégration système et architecture réseau peuvent sécuriser leur décision d'achat.

> Lien produit : [EM7565 — page produit Yupitek](/fr/products/sierra/em7565/) | Fiche technique officielle : [AirPrime EM7565 Product Technical Specification](https://yupitek.com/docs/sierra/EM7565_spec.pdf)

---

## L'essentiel d'abord : qu'est-ce que l'EM7565 ?

**L'EM7565 est un module cellulaire WWAN de Sierra Wireless au format M.2, équipé du chip Qualcomm MDM9250. Il atteint LTE Cat 12 en téléchargement (jusqu'à 600 Mbit/s) et Cat 13 en envoi (jusqu'à 150 Mbit/s), avec en plus une localisation GNSS multi-constellation.**

Réponses directes aux trois questions les plus importantes :

| Question | Réponse directe |
|---|---|
| **Peut-on construire un réseau privé CBRS avec l'EM7565 ?** | La fiche technique liste bien la bande LTE 48 (la bande 3,5 GHz du CBRS), mais à la publication de la Rev 8 elle était marquée « disabled, en attente d'approbation réglementaire ». Pour un usage commercial, il faut toujours se baser sur la réglementation en vigueur et la fiche technique officielle la plus récente. Contacte-nous avant de commander pour vérifier les documents à jour ! |
| **Quelle est la vitesse d'envoi ?** | Jusqu'à 150 Mbit/s (Cat 13) ; le téléchargement atteint 600 Mbit/s (Cat 12). |
| **À qui convient-il le mieux ?** | Aux routeurs industriels d'entreprise et aux intégrateurs système qui ont besoin, pour l'edge computing, de « renvoyer de gros volumes de données vers le cloud » (grâce à la vitesse d'envoi élevée). Si tu es un maker qui bidouille avec un Raspberry Pi, un adaptateur M.2 vers USB fonctionne aussi. |
| **Y a-t-il des antennes intégrées ?** | Non ! Sur la carte, il n'y a que 3 petits connecteurs RF (Main, GNSS, Auxiliary). Tu dois acheter les antennes toi-même et concevoir les tracés. |

---

## Tableau complet des caractéristiques de l'EM7565 (comparaison directe avec les données officielles)

Les ingénieurs adorent les chiffres. Toutes les valeurs ci-dessous proviennent de la fiche technique officielle de Sierra Wireless ; les lignes de sources sont indiquées dans le Verification Log à la fin du document.

| Élément | Caractéristique | Source |
|---|---|---|
| **Modèle** | AirPrime EM7565 (numéro de document 41110788, Rev 8) | Couverture de la fiche technique |
| **Format** | M.2 (WWAN Type 3042-S3-B) | Page 14 de la fiche technique |
| **Chipset** | Processeur de bande de base Qualcomm MDM9250 | Page 12 de la fiche technique |
| **Norme cellulaire** | LTE : 3GPP Release 11 ; UMTS : 3GPP Release 9 | Page 18 de la fiche technique |
| **Pic de téléchargement** | Cat 12, 3×CA, 256QAM : 600 Mbit/s (Cat 9 : 450 Mbit/s) | Page 12 de la fiche technique |
| **Pic d'envoi** | Cat 13, 2×CA contiguous, 64QAM : 150 Mbit/s | Page 12 de la fiche technique |
| **Agrégation de porteuses** | DL LTE-FDD : 60 MHz ; DL LTE-TDD : 60 MHz ; UL LTE : 40 MHz (intraband contiguous) | Page 15 de la fiche technique |
| **MIMO** | 2×2 / 4×2 en téléchargement | Page 12 de la fiche technique |
| **Vitesses UMTS** | DC-HSPA+ jusqu'à 42 Mbit/s en téléchargement, 11 Mbit/s en envoi | Page 12 de la fiche technique |
| **Bandes LTE** | B1/B2/B3/B4/B5/B7/B8/B9/B12/B13/B18/B19/B20/B26/B28/B29(DL)/B30(DL)/B32(DL)/B41/B42/B43/B46/B48/B66 (B42/43/48 marqués disabled à la publication) | Page 42 de la fiche technique |
| **Bandes WCDMA** | Band 1/2/4/5/6/8/9/19 | Pages 43–44 de la fiche technique |
| **Interfaces** | USB 2.0 + USB 3.0 ; prise en charge QMI, MBIM ; commandes AT | Pages 15, 28 de la fiche technique |
| **SIM** | Double SIM (1.8V ou 3V), mais tu dois fournir le support de carte SIM | Page 29 de la fiche technique |
| **Interfaces antennes** | 3 connecteurs RF : Main, GNSS, Auxiliary | Page 37 de la fiche technique |
| **GNSS** | Suivi simultané GPS, GLONASS, Galileo, BeiDou, QZSS ; démarrage à froid 32 secondes | Page 47 de la fiche technique |
| **Dimensions** | 42±0,15 × 30±0,15 mm | Page 57 de la fiche technique |
| **Poids** | 6,5 g | Page 57 de la fiche technique |
| **Température de fonctionnement** | Classe A : -30°C à +70°C ; classe B : -40°C à +85°C (avec refroidissement et réduction de fréquence) | Pages 14, 57 de la fiche technique |
| **Température interne du module** | Impérativement sous 90°C, recommandé sous 80°C | Page 14 de la fiche technique |
| **Certification réglementaire** | Conforme FCC (États-Unis), IC (Canada), NCC (Taïwan), MIC (Japon), RED (UE), etc. | Page 62 de la fiche technique |

> **À noter impérativement** : les chiffres ci-dessus correspondent à la version Rev 8 (octobre 2018). Le firmware et la certification évoluent avec le temps. Si tu veux commander, demande-nous d'abord les documents officiels les plus récents et vérifie une nouvelle fois.

---

## Le réseau privé CBRS tant attendu : peut-on vraiment utiliser l'EM7565 ?

**En bref : le support matériel existe, mais le firmware et la réglementation dépendent de l'état actuel.**

La fiche technique contient bien la bande 48 (3550–3700 MHz) utilisée pour le CBRS, mais (et ce « mais » est très important) à la publication de la Rev 8, les bandes B42/B43/B48 étaient explicitement marquées « disabled as of publication date, support pending regulatory approval » (désactivées à la date de publication, prise en charge en attente d'approbation réglementaire).

Nous ne pouvons donc pas garantir qu'on « l'achète et qu'on monte directement un réseau CBRS ». Si tu veux construire un réseau privé CBRS, trois points sont à vérifier : le B48 est-il déverrouillé dans le firmware le plus récent, le produit est-il conforme à la certification FCC Part 96 en vigueur, et l'ensemble du système passe-t-il l'OTA ? Si tu en as besoin, le plus sûr est de nous contacter d'abord pour connaître l'état actuel.

---

## Cat 12 en téléchargement + Cat 13 en envoi : quel intérêt pour ton projet ?

**Le point fort n'est en réalité pas le téléchargement, mais la « très forte capacité d'envoi » !**

En général, on télécharge beaucoup sur son téléphone (vidéos, flux). Mais dans les applications industrielles ou les projets IoT, les équipements doivent souvent « renvoyer des données vers le cloud ». L'EM7565 offre un envoi Cat 13 (jusqu'à 150 Mbit/s, 2×CA, 64QAM) et un téléchargement Cat 12 (jusqu'à 600 Mbit/s, 3×CA, 256QAM).

C'est très intéressant pour les scénarios où **le besoin d'envoi dépasse le téléchargement** : « la caméra de surveillance de l'usine doit transmettre l'image à la salle de contrôle en temps réel », « les données des capteurs d'un véhicule autonome doivent remonter massivement vers le cloud ». Si ton projet a seulement besoin que l'équipement se connecte à Internet et consulte des données, un module Cat 6 moins cher (par exemple l'EM7455) suffit largement.

---

## Quelles bandes prend en charge l'EM7565 ?

**Réponse courte : 24 bandes LTE au total (dont B1–B66) et 8 bandes WCDMA. Les bandes principales de Taïwan et de la région Asie-Pacifique sont essentiellement couvertes.**

### Récapitulatif des bandes LTE :

- **Bandes courantes** : B1, B3, B7, B8, B28 (la plupart des opérateurs de Taïwan et d'Asie-Pacifique les utilisent).
- **Téléchargement uniquement** : B29, B30 (Tx désactivé), B32, B46 (LTE-LAA).
- **En attente d'approbation réglementaire (à la publication)** : B42, B43, B48 (CBRS).

Si ton projet se fait à Taïwan, la couverture de l'EM7565 ne pose aucun problème. Mais si le laboratoire veut tester des réseaux privés ou des bandes spéciales (comme la B48), ne commande pas sur la base de l'ancienne fiche technique : renseigne-toi d'abord sur l'état actuel.

---

## Conception à trois antennes : il faudra gérer les tracés RF toi-même

**L'EM7565 n'a pas d'antennes sorties ; les antennes doivent être conçues sur la carte mère.** Il dispose de trois petits connecteurs RF : Main (antenne principale émission/réception), Auxiliary (antenne diversité/MIMO) et GNSS (antenne de localisation).

Pour la LTE, il faut au minimum tirer les deux antennes Main et Auxiliary en 2×2 MIMO. Les connecteurs sont au standard I-PEX MHF4. Le fabricant recommande un VSWR (taux d'ondes stationnaires) inférieur à 2:1 et une efficacité de rayonnement supérieure à 50 %. Autrement dit : si ton projet prévoit de fabriquer ta propre carte et de tracer les antennes, prépare-toi à tester le RF.

---

## GNSS : Internet et localisation, un seul module suffit

Si ton projet touche à la « voiture » ou à la « logistique », ce module intègre directement le suivi de cinq constellations (GPS, GLONASS, Galileo, BeiDou, QZSS), avec jusqu'à 30 canaux suivis simultanément. Le démarrage à froid prend environ 32 secondes et les données sortent directement au format standard NMEA 0183. Tu économises ainsi l'achat d'un module GPS séparé et de l'espace sur la carte.

---

## Conception grande plage de température : la robustesse industrielle

Dans l'équipement industriel, ce qu'on craint le plus, c'est la surchauffe. L'EM7565 supporte, selon la norme 3GPP, des températures ambiantes de -30°C à +70°C ; avec un bon refroidissement, il tient jusqu'à -40°C et +85°C (mais avec une baisse de performance).

**Conseil d'expérience en laboratoire** : la fiche technique précise que la température interne du module (consultable avec `AT!PCTEMP`) **ne doit en aucun cas dépasser 90°C, idéalement rester sous 80°C**. Si tu le loges dans un petit boîtier et que tu le fais tourner en envoi à pleine vitesse, pense à coller un pad thermique ou à installer un ventilateur, sinon le mécanisme de protection se déclenchera : réduction de vitesse, voire extinction !

---

## Alimentation et consommation : ne choisis pas ton bloc d'alimentation au hasard

L'EM7565 fonctionne de 3.135V à 4.4V (typiquement 3.3V). Attention : à pleine vitesse ou au moment de la mise sous tension, le courant grimpe fortement :

- **Courant de crête** : 1,3A (moyenne sur 100 microsecondes)
- **Courant maximal** : 1,5A
- **Courant d'appel instantané** : de 2,2A à 2,5A

Quand tu conçois ta carte et que tu choisis un convertisseur abaisseur DC-DC ou un LDO, garde une marge sur la base du « courant d'appel de 2,5A ». Ne choisis pas un circuit d'alimentation en regardant « seulement 2,8mA en veille » : il ne tiendra pas la charge.

---

## Réglementation et certifications

La fiche technique indique que la conception est conforme aux normes FCC (États-Unis), NCC (Taïwan), RED (UE), etc., et dispose des certifications GCF et PTCRB. Pour une entreprise qui lance un produit, cela évite beaucoup de tracas de certification. Mais rappelle-toi : c'est le « module » qui est certifié. Ton « appareil » complet devra quand même passer les tests FCC ou NCC pour être légal.

---

## Conclusion : faut-il acheter l'EM7565 ?

| Ton besoin | L'EM7565 convient-il ? | Pourquoi ? |
|---|---|---|
| J'ai besoin d'une vitesse d'envoi très élevée | ✅ Très adapté | Les 150 Mbit/s du Cat 13 sont faits pour toi. |
| Je veux tester un réseau privé CBRS | ⚠️ Attends un peu | Le support matériel du B48 existe, mais vérifie d'abord avec nous l'état du firmware et de la réglementation. |
| J'ai juste besoin d'Internet et d'envoyer des fichiers texte | ❌ Surdimensionné | Un Cat 4 ou Cat 6 pas cher (comme l'EM7455) suffit, et ça fait économiser le budget du patron. |
| Je fais de la gestion de flotte et j'ai besoin d'une localisation précise | ✅ Très adapté | La 4G et la localisation sur cinq constellations en un seul module, pas besoin de dessiner un GPS supplémentaire. |

### Comparaison rapide : EM7565 vs EM7455

| Élément | EM7565 | EM7455 |
|---|---|---|
| Téléchargement | 600 Mbit/s (Cat 12, 3×CA) | 300 Mbit/s (Cat 6, 2×CA) |
| Envoi | 150 Mbit/s (Cat 13, 2×CA) | 50 Mbit/s (Cat 6) |
| Chip | Qualcomm MDM9250 | Qualcomm MDM9230 |

---

## FAQ rapide

{{< faq >}}

---

## Contacte-nous pour discuter de ton projet

Cette analyse technique approfondie a été préparée par l'équipe d'ingénieurs de Yupitek. Si tu choisis un module 4G pour ton laboratoire, ou si ton projet d'entreprise a besoin d'une tarification en volume sur l'EM7565 et d'un accompagnement pour la conception d'antennes, n'hésite pas à nous contacter.

- **Page produit EM7565** : [https://yupitek.com/fr/products/sierra/em7565/](/fr/products/sierra/em7565/)
- **Voir d'autres modèles Sierra** : [https://yupitek.com/fr/products/sierra/](/fr/products/sierra/)
- **E-mail de contact** : sales@yupitek.com
