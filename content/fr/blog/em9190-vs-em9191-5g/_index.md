---
title: "EM9190 vs EM9191 : 5G Sub-6 ou mmWave, que choisir ? On démêle le vrai du faux sur Internet"
description: "EM9190 vs EM9191, comment choisir ? Selon la fiche technique officielle (41113174 Rev 8) : l'EM9190 prend en charge le 5G Sub-6 + mmWave (n257/258/260/261, uniquement NSA), l'EM9191 seulement le Sub-6. Tous deux sur Qualcomm SDX55, M.2, avec comparatif des bandes 5G taïwanaises. Préparé par Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em9190", "em9191", "5g", "mmwave", "sub-6", "n78", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM9190_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "Quelle est la vraie différence entre l'EM9190 et l'EM9191 ? Lequel prend en charge le mmWave ?"
    answer: "Selon la fiche technique officielle (41113174, Rev 8), les capacités Sub-6 (FR1), LTE, 3G et GNSS sont identiques. La seule différence majeure est le 5G mmWave (FR2) : l'EM9190 prend en charge LTE+FR2 NSA EN-DC (avec modules d'antennes mmWave QTM525/QTM527, uniquement en mode NSA), l'EM9191 indique Not supported. C'est donc l'EM9190 qui a le mmWave."
  - question: "L'EM9191 convient-il aux applications 5G à Taïwan ?"
    answer: "Oui. La bande centrale du réseau 5G taïwanais est le 3,5 GHz, correspondant au n78 3GPP (3300–3800 MHz, TDD) ; l'EM9190 comme l'EM9191 prennent en charge le n78. Le 28 GHz taïwanais (correspondant au n257) est moins déployé ; seuls ces sites-là nécessitent l'EM9190 + module d'antennes mmWave. Pour les FWA 5G classiques et les routeurs industriels, l'EM9191 suffit."
  - question: "Le mmWave est-il inclus à l'achat du module EM9190 ?"
    answer: "Non. L'EM9190 n'a pas d'antennes intégrées : pour le mmWave, il faut ajouter 1 à 4 modules d'antennes mmWave Qualcomm QTM525 (faible puissance, EIRP 23 dBm) ou QTM527 (haute puissance, EIRP 45 dBm), chacun raccordé par deux câbles IF MHF7S (jusqu'à 8 câbles) et alimenté en externe en 3,8V ; de plus, le FR2 n'est pris en charge qu'en mode NSA."
  - question: "Quelle est la différence de consommation entre les deux modules ?"
    answer: "Selon le tableau 3-2 de la fiche technique : courant de crête EM9190 (avec mmWave) 5,0A, EM9190 (sans mmWave) 3,0A, EM9191 2,7A ; courant continu respectivement 4,0A, 2,3A et 2,0A. Pour les terminaux sur batterie ou à refroidissement limité, l'EM9191 est nettement plus simple à concevoir côté alimentation."
  - question: "Les designs de cartes mères de l'EM9190 et de l'EM9191 sont-ils compatibles ?"
    answer: "Très largement : tous deux en M.2 (WWAN Type 3042-S3-B, 52 mm de long), même interface 75-pin, mêmes interfaces USB 3.1 Gen2 / PCIe Gen3, mêmes 4 ports d'antennes MHF4 Sub-6. La différence : l'EM9190 ajoute 8 connecteurs IF MHF7S mmWave et des pins de contrôle QTM (pin 40/42/44/46/48, NC sur l'EM9191)."
---

# EM9190 vs EM9191 : 5G Sub-6 ou mmWave, que choisir ? On démêle le vrai du faux sur Internet

Si tu fais un projet 5G avec ton professeur à l'université, ou si tu es en charge du choix du module 5G dans ton entreprise, tu verras sûrement souvent cette phrase en cherchant sur Internet : « L'EM9190 est la version Sub-6 économique, et l'EM9191 est le modèle phare avec le mmWave (ondes millimétriques). »

**Faux ! C'est exactement l'inverse !**

Cet article ne s'appuie pas sur des rumeurs en ligne : notre seule référence est la fiche technique officielle de Sierra Wireless, « EM919X/EM7690 Product Technical Specification » (Doc 41113174, Rev 8, mai 2023). Nous vérifions les différences entre ces deux modules point par point. Nous accordons une attention particulière aux bandes n78 et 28 GHz, celles qui intéressent le plus les lecteurs taïwanais, pour que tu ne te trompes pas lors de l'achat de ton équipement 5G.

> Liens produits : [EM9190 — page produit Yupitek](/fr/products/sierra/em9190/) | [EM9191 — page produit Yupitek](/fr/products/sierra/em9191/) | Fiche technique officielle : [EM919X/EM7690 Product Technical Specification](https://yupitek.com/docs/sierra/EM919x.pdf)

---

## Démêlons le vrai du faux : quelle est la vraie différence entre l'EM9190 et l'EM9191 ?

**En bref, l'EM9190 et l'EM9191 sont des jumeaux (même série, même chip de bande de base) : tous deux prennent en charge le 5G Sub-6, la 4G LTE et la localisation GNSS. La seule différence : l'EM9190 prend en charge en plus le 5G mmWave (ondes millimétriques, FR2), l'EM9191 non.**

Pour avoir le mmWave, après l'achat de l'EM9190, tu dois encore connecter des modules d'antennes Qualcomm QTM525 ou QTM527 (et ça ne fonctionne qu'en mode NSA).

| Ta question | La bonne réponse selon la fiche technique officielle |
|---|---|
| **Quelle est la différence entre ces deux cartes ?** | Seulement le mmWave (FR2). Sur la fiche de l'EM9190, on lit « LTE+FR2 NSA EN-DC Supported » ; sur celle de l'EM9191, « Not supported ». Tout le reste, bandes Sub-6, LTE, etc., est identique. |
| **L'EM9190 a-t-il le mmWave ?** | Oui. Mais ce n'est pas automatique à l'achat de la carte : tu dois connecter en externe des modules d'antennes mmWave Qualcomm (jusqu'à 4), avec prise en charge des n257/n258/n260/n261, et uniquement en mode NSA (réseau non autonome). |
| **L'EM9191 a-t-il le mmWave ?** | Non. Le tableau officiel 1-1 indique clairement « Not supported », et tous les pins de signal liés au mmWave sont en NC (non connectés) sur la carte. |
| **Quel module acheter pour un projet 5G à Taïwan ?** | Le 5G taïwanais tourne le plus souvent sur 3,5 GHz (n78), supporté par les deux modules ; le 28 GHz (correspondant au n257) est plus rare à Taïwan. Seulement si tu fais justement des expériences là-dessus, tu as besoin de l'EM9190 plus les antennes mmWave. |
| **Quel module pour quel profil ?** | **EM9190** : marchés américain et japonais, tests en laboratoire des ondes millimétriques, équipements CPE extérieurs à très large bande.<br>**EM9191** : projets Sub-6 à Taïwan ou en Asie, quand le module doit consommer moins et que le budget est limité. |

> **On insiste encore une fois** : ne crois plus aux affirmations en ligne selon lesquelles « l'EM9191 est le phare mmWave ». La fiche technique officielle dit noir sur blanc que **seul l'EM9190 a la capacité mmWave**. Te tromper à l'achat serait gênant.

---

## Les frères d'une même famille : comment distinguer EM9190 / EM9191 / EM7690 ?

En réalité, la famille EM91 compte trois frères. Selon la fiche technique :

- **EM9190** : version complète (LTE + 5G Sub-6 + 5G mmWave)
- **EM9191** : version standard pratique (LTE + 5G Sub-6, sans mmWave)
- **EM7690** : version allégée (LTE uniquement, pas de 5G)

Dans cet article, nous comparons surtout les deux premiers frères 5G ; l'EM7690 est juste mentionné pour que tu saches qu'il existe.

---

## Tableau de comparaison technique poussé (d'après la 41113174 Rev 8 officielle)

Tous les chiffres ci-dessous proviennent de la fiche technique officielle. Si tu es ingénieur, regarde directement ce tableau :

| Élément | EM9190 | EM9191 | Source |
|---|---|---|---|
| **5G NR Sub-6 (FR1)** | ✓ | ✓ | Table 1-2 |
| **5G NR mmWave (FR2)** | ✓ (uniquement en mode NSA, module d'antennes externe requis) | ✗ | Table 1-1 |
| **Bandes millimétriques FR2** | n257 / n258 / n260 / n261 | — | Table 1-2 |
| **Bandes FR1 Sub-6** | n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n38/n40/n41/n48/n66/n71/n77/n78/n79 | identiques sur les deux | Table 4-4 |
| **Chip de bande de base** | Qualcomm SDX55 | Qualcomm SDX55 | Figure 3-1 |
| **Norme cellulaire** | 5G 3GPP Release 15 ; LTE Release 15 | identique sur les deux | Table 2-1 |
| **Format** | M.2 (WWAN Type 3042-S3-B, 52 mm de long) | identique sur les deux | §1.2 |
| **Interface ordinateur/carte mère** | USB 3.1 Gen2, PCIe Gen3 une voie | identique sur les deux | §1.3 |
| **Ports d'antennes Sub-6** | 4 connecteurs MHF4 (MAIN/MIMO1/MIMO2/AUX) | identique sur les deux | §4.1 |
| **Ports d'antennes mmWave** | 8 connecteurs MHF7S (jusqu'à 4 modules d'antennes externes) | aucun | §4.1 |
| **Consommation instantanée maximale (crête)** | 5,0A (avec mmWave) / 3,0A (sans) | 2,7A | Table 3-2 |
| **Température de fonctionnement** | -30°C à +70°C (classe A) ; -40°C à +85°C (classe B, avec baisse de performance) | identique sur les deux | Table 7-1 |
| **Localisation (GNSS)** | L1 (GPS/GLONASS, etc.) + L5 (en option) | identique sur les deux | Table 4-13 |

> **Petit rappel** : cette fiche technique date de mai 2023. Certaines bandes (comme n7, n8, n20, etc.) peuvent varier selon le firmware ou le SKU livré. Avant de commander pour un vrai projet, demande-nous les documents officiels les plus récents et compare.

---

## Le mmWave ne vient pas avec le module : les coûts cachés de l'EM9190

Beaucoup d'étudiants et de makers pensent qu'acheter l'EM9190 permet de tester immédiatement les ondes millimétriques. C'est une grande erreur.

La fiche technique est claire : « **L'EM9190 ne prend en charge le 5G mmWave qu'avec des modules d'antennes mmWave Qualcomm en option.** » De plus, seul le mode NSA (réseau non autonome) est pris en charge, c'est-à-dire que tu as obligatoirement besoin d'un signal 4G LTE comme point d'ancrage (Anchor).

### Comment configurer les antennes millimétriques ?

Tu dois acheter des modules d'antennes Qualcomm QTM525 (version faible puissance) ou QTM527 (version haute puissance). Et les différents modules d'antennes prennent en charge différentes bandes (voir le tableau officiel 4-2) :

- Si ton laboratoire veut tester le **n257** (la bande 28 GHz de Taïwan), tu dois acheter QTM525-2, QTM525-5 ou QTM527-2 ; si tu achètes QTM527-1, pas de n257 !

**Le piège à éviter pour les ingénieurs** :
Si tu veux utiliser l'EM9190 comme récepteur 5G extérieur (CPE), il faudra peut-être monter les 4 antennes haute puissance QTM527. Cela signifie : tirer 8 câbles MHF7S très chers, concevoir une alimentation 3,8V séparée pour ces antennes, et prévoir un refroidissement costaud. Ce coût de développement dépasse souvent largement le prix de la carte seule !

---

## Si tu fais du 5G à Taïwan, l'EM9191 suffit en réalité

**Parce que la fréquence principale du 5G taïwanais est le 3,5 GHz (c'est-à-dire le n78 dans le langage 3GPP), et que l'EM9190 comme l'EM9191 supportent parfaitement le n78.**

Si ton projet doit simplement faire tourner du 5G à Taïwan, ou si tu fabriques des routeurs industriels pour des clients classiques :

- Les deux modules prennent en charge le n78 5G taïwanais (3300–3800 MHz).
- Les deux modules prennent en charge les bandes 4G existantes à Taïwan (comme point d'ancrage NSA, aucun problème).

**Pourquoi te recommandons-nous d'acheter l'EM9191 ?**
Parce que si tu n'as pas besoin des ondes millimétriques, il est inutile de payer pour l'EM9190. De plus, l'EM9191 n'ayant pas de matériel mmWave, son courant de crête n'est que de 2,7A, nettement plus simple que l'EM9190 (voir la section suivante), et la charge sur l'alimentation de la carte est beaucoup plus légère.

---

## Comparaison de la consommation : ne rate pas la conception de l'alimentation

Ceux qui font du matériel le savent : si l'alimentation ne suit pas, l'appareil redémarre. Selon les données du tableau officiel 3-2 :

| Paramètre de consommation | EM9190 (avec mmWave) | EM9190 (sans mmWave) | EM9191 |
|---|---|---|---|
| Courant de crête instantané | 5,0A | 3,0A | 2,7A |
| Courant continu en usage | 4,0A | 2,3A | 2,0A |

Tous les modules fonctionnent de 3.135V à 4.4V (généralement conçus pour 3.3V). Tu le vois : si l'EM9190 active le mmWave, le courant instantané monte à 5,0A ! C'est un vrai défi pour les appareils sur batterie ou de petite taille. Si tu veux juste du 5G Sub-6, l'EM9191 n'exige de gérer qu'un pic de 2,7A, et la conception de l'alimentation devient bien plus simple.

---

## Le design des pins de la carte : peut-on partager un même design ?

**Le design Sub-6 peut être partagé.**

Les deux modules sont au format M.2 (52 mm de long, un peu plus longs que les 42 mm habituels des notebooks, fais attention à la place mécanique) et ont la même interface 75-pin.

La seule différence : pour piloter toutes ces antennes mmWave, l'EM9190 utilise certains pins initialement libres (par exemple QTM_PON sur les pin 40/42/44/46 et l'alimentation 1.9V sur le pin 48). Sur l'EM9191, ces pins sont vides (NC).
Tu peux donc très bien concevoir d'abord une carte universelle pour l'EM9191, puis, le jour où tu veux vraiment faire des ondes millimétriques, ajouter simplement les lignes de commande nécessaires à l'EM9190.

---

## Conclusion : quel module acheter ?

| Tes besoins | Choisis l'EM9190 | Choisis l'EM9191 |
|---|---|---|
| Tu dois tester des bandes mmWave comme le 28 GHz | ✅ Lui uniquement (pense à acheter les antennes en plus) | ❌ Non supporté |
| Projet à Taïwan, uniquement du 5G Sub-6 (n78) | Possible (mais un peu du gaspillage) | ✅ Recommandé, économise de l'argent et de l'énergie |
| L'alimentation de la carte ne supporte pas un gros courant | ⚠️ Pic possible jusqu'à 5,0A | ✅ Pic de 2,7A, bien plus facile à gérer |

**Guide pour éviter les pièges** :

1. Ne te trompe plus : seul l'EM9190 a le mmWave.
2. Acheter l'EM9190 ne veut pas dire avoir le mmWave : il faut en plus des antennes spéciales et du câblage.
3. De nombreuses bandes (comme n7, n8, n28) sont soumises aux versions de firmware et aux restrictions régionales. Avant d'acheter, vérifie absolument auprès de ton fournisseur si ton SKU peut déverrouiller ces bandes.

---

## FAQ rapide

{{< faq >}}

---

## Besoin d'acheter ou d'en discuter ? Contacte-nous

Si tu as encore des questions d'intégration matérielle après cet article, ou si ton laboratoire/entreprise doit acheter ces deux modules 5G, contacte l'équipe d'ingénieurs de Yupitek. Nous proposons aussi les antennes et les cartes adaptatrices correspondantes.

- **Page produit EM9190 (le vrai phare avec mmWave)** : [https://yupitek.com/fr/products/sierra/em9190/](/fr/products/sierra/em9190/)
- **Page produit EM9191 (la version Sub-6 pratique)** : [https://yupitek.com/fr/products/sierra/em9191/](/fr/products/sierra/em9191/)
- **Toutes les séries Sierra** : [https://yupitek.com/fr/products/sierra/](/fr/products/sierra/)
- **E-mail de contact** : sales@yupitek.com
