---
title: "Le guide complet pour ajouter la 4G/5G à ton portable Dell ou Lenovo : modèles compatibles et installation"
description: "Le guide complet pour faire évoluer ton portable Dell ou Lenovo avec une carte WWAN 4G/5G : comparaison des specs EM7455 vs EM7430, comment vérifier le slot M.2, les antennes WWAN et la liste blanche du BIOS. Cat 6 avec 300 Mbit/s en download, installation pas à pas incluse."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "fr"
hreflang_group: "dell-lenovo-laptop-4g-5g-upgrade-guide"
slug: "dell-lenovo-laptop-4g-5g-upgrade-guide"
tags: ["Dell", "Lenovo", "EM7455", "EM7430", "WWAN", "M.2", "4G", "LTE", "laptop-upgrade"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/fr/products/sierra/"
faq:
  - question: "Je peux simplement installer une EM7455 ou une EM7430 dans mon portable Dell ou Lenovo ?"
    answer: "La marque ne suffit pas. Trois conditions doivent être réunies : la carte mère a un slot WWAN M.2 B-key (67 broches), le châssis a des antennes WWAN pré-câblées et le BIOS n'impose pas de liste blanche. Vérifie le manuel de service officiel et ouvre la machine pour confirmer avant d'acheter."
  - question: "Quelle est la différence entre l'EM7455 et l'EM7430 ?"
    answer: "Les deux utilisent le même chipset Qualcomm MDM9230, les deux sont LTE Cat 6 (300/50 Mbit/s) et les deux existent dans le même format M.2. La différence, c'est la couverture des bandes : l'EM7455 penche vers les Amériques et les bandes globales, tandis que l'EM7430 couvre l'Asie-Pacifique et ajoute le TD-SCDMA pour la Chine."
  - question: "De combien d'antennes la carte a-t-elle besoin ?"
    answer: "Le module a 3 connecteurs RF : Main, GNSS et Aux. Connecte au moins Main pour les données cellulaires, ajoute Aux pour la pleine vitesse, et connecte GNSS uniquement si tu as besoin du positionnement GPS."
---

# Le guide complet pour ajouter la 4G/5G à ton portable Dell ou Lenovo : modèles compatibles et installation

**La version courte : avant d'équiper ton portable d'une carte 4G, vérifie que les antennes et le slot sont vraiment là, puis que le BIOS t'autorise l'installation. Côté carte : pour un usage à Taïwan ou dans la région Asie-Pacifique, l'EM7455 comme l'EM7430 font l'affaire. Elles sont basées sur le même chipset MDM9230 et sont toutes deux des cartes Cat 6, donc la vitesse est identique ; la seule vraie différence, c'est les bandes couvertes.**

Beaucoup de gens qui ont un Dell Latitude ou un Lenovo ThinkPad veulent glisser une carte 4G dans le slot WWAN libre pour arrêter de chercher du Wi-Fi en déplacement professionnel. Mais ce n'est pas aussi simple que ça en a l'air. Il faut confirmer que la carte mère a le bon slot, que les antennes sont réellement câblées et que le fabricant n'a pas verrouillé le BIOS avec une liste blanche.

Dans ce guide, on utilise les spécifications officielles Sierra Wireless pour comparer les deux cartes d'évolution les plus populaires, l'EM7455 et l'EM7430, et on te accompagne dans l'installation.

> Sources : spécifications officielles Sierra Wireless (EM7455, EM7430). Compilé par Yupitek.

---

## Auto-vérification en 30 secondes : mon portable peut-il la recevoir ?

| À vérifier | Ce que c'est | Comment le savoir |
|---|---|---|
| **Le bon slot** | Un slot WWAN M.2 B-key (67 broches) | Ouvre la coque inférieure et cherche un slot vide de 42 mm, généralement marqué WWAN. Ne le confonds pas avec le slot Wi-Fi ! |
| **Antennes présentes** | Le module a besoin d'antennes pour recevoir le moindre signal | Cherche des câbles d'antenne rouges, bleus et noirs en réserve près du slot. S'il n'y en a pas, la carte sera inutile même si tu l'achètes. |
| **Liste blanche du BIOS** | Les fabricants limitent l'installation aux cartes certifiées d'usine | Cherche le « Service Manual » de ton modèle de portable sur le site officiel et vérifie la liste des modules WWAN pris en charge. |
| **C'est quoi le DW5811e de Dell ?** | Un numéro de pièce Dell, pas un modèle de carte | Le même numéro de pièce peut cacher des cartes différentes. À l'achat d'occasion, cherche la mention « Sierra EM7455 » directement sur la carte. |

---

## Le duel : EM7455 vs EM7430

Ces deux cartes sont quasi jumelles. Les deux tournent sur le chipset Qualcomm MDM9230, les deux sont LTE Cat 6 (jusqu'à 300 Mbit/s en download, 50 Mbit/s en upload) et les deux partagent exactement le même format (pack M.2 42×30 mm, 6,5 g).

**Alors, qu'est-ce qui diffère vraiment ? Les bandes.**

| Point de comparaison | EM7455 | EM7430 | Verdict |
|---|---|---|---|
| **Focus des bandes** | Global et Amériques (surtout FDD) | Asie-Pacifique (FDD + TDD) | En Asie, la 7430 couvre plus de terrain ; prends la 7455 pour les déplacements aux États-Unis. |
| **3G Chine (TD-SCDMA)** | Non pris en charge | Pris en charge (Band 39) | Pertinent seulement si tu as des besoins spécifiques de voyage en Chine. |
| **Certifications** | Inclut les Amériques (FCC/IC/PTCRB) et plus | Certifications américaines non listées dans la spec | L'EM7430 est plutôt une variante spécifique à l'Asie. |

**Conseil pour les utilisateurs à Taïwan** : les deux cartes couvrent les bandes 4G grand public utilisées à Taïwan, et tu ne verras aucune différence de vitesse. Prends celle qui est la plus simple à acheter là où tu es, et celle que la liste blanche du BIOS de ton portable accepte.

---

## Avant d'acheter : vérifie l'espace à l'intérieur

Avant d'acheter la carte, confirme l'espace disponible à l'intérieur de ton portable :

1. **Taille du slot** : les deux modules sont **M.2 WWAN Type 3042-S3-B**, soit 42 mm de long et 30 mm de large.
2. **Dégagement en hauteur** : le module ne dépasse pas de plus de 1,50 mm au-dessus de la carte électronique. Assure-toi que rien au-dessus, comme un SSD ou un radiateur, ne le bloque.
3. **Alimentation** : ils acceptent de 3,135 V à 4,4 V (typiquement 3,7 V). La carte mère du portable gère normalement ça pour toi. Fais quand même attention à la chaleur : la recommandation officielle est de garder la température interne sous 80 °C (maximum absolu 93 °C).

---

## Installation : étape par étape

Si ton portable a les antennes, que le slot est bon et qu'il n'y a pas de problème de liste blanche, fonce.

1. **Éteins et décharge** : arrête le portable, débranche l'adaptateur secteur, retire la batterie externe s'il y en a une, et appuie plusieurs fois sur le bouton d'alimentation pour décharger. La protection ESD compte !
2. **Retire la coque inférieure** : ouvre le panneau du bas et trouve le slot M.2 vide marqué WWAN.
3. **Insère la carte** : glisse le module à un angle de 30 degrés, en alignant l'encoche avec le connecteur B-key.
4. **Visse** : appuie pour aplatir et serre la petite vis.
5. **Connecte les antennes (la partie délicate)** :
   - Le module a 3 connecteurs : de gauche à droite, généralement Main (antenne principale), GNSS (GPS) et Aux (antenne de diversité).
   - Aligne-les soigneusement avant d'appuyer. Les connecteurs MHF4 sont minuscules et fragiles, en écraser un est une catastrophe.
   - Connecte au minimum Main, sinon aucun signal. Ajoute Aux pour la pleine vitesse. Connecte GNSS seulement si tu veux la navigation.
6. **Insère la SIM** : le module n'a pas d'emplacement pour la carte SIM ; le tiroir SIM se trouve sur le bord du portable ou dans le compartiment batterie ! Les deux cartes prennent en charge les SIM 1,8 V et 3 V.
7. **Allume et termine** : remets la coque, démarre et installe le pilote. Windows 10 détecte la carte automatiquement via MBIM.

---

## Les erreurs les plus courantes

- **Mauvais slot** : forcer une carte mPCIe (comme la MC7455) dans un slot M.2.
- **Installer sans antennes** : supposer que chaque portable a des câbles d'antenne pré-câblés, pour découvrir qu'il n'y a aucun câble à connecter et un signal qui ne quitte jamais zéro barre.
- **Bloqué par la liste blanche d'usine** : acheter une carte générique suspecte de bon marché, puis tomber sur un écran noir au démarrage avec une erreur « unauthorized card ».
- **Attendre la 5G** : l'EM7455 et l'EM7430 sont toutes deux de pures cartes 4G LTE (Cat 6). Pour la 5G, il te faut quelque chose comme l'EM9190, et elle exige 4 connexions d'antennes ou plus !

## Conclusion

Ajouter une carte cellulaire à ton portable n'est pas difficile. Ce qui est difficile, c'est la reconnaissance matérielle avant. Ouvre le portable et vérifie d'abord les antennes, puis regarde si le constructeur a verrouillé la liste blanche. Passe ces deux contrôles, et l'EM7455 comme l'EM7430 te donneront une connectivité mobile fluide et fiable.

## Où acheter (appel à l'action)

Tu veux acheter une carte Sierra Wireless, ou tu n'es pas sûr que ton PC industriel puisse en accueillir une ? Yupitek propose des solutions matérielles complètes et un support technique.
Écris-nous : **sales@yupitek.com**
Découvre la gamme : [Série Sierra Wireless](https://yupitek.com/fr/products/sierra/)
