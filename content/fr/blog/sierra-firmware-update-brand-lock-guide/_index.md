---
title: "Guide Sierra Wireless : mise à jour du firmware et changement de verrouillage de marque, flasher sans briquer le module"
description: "Le guide complet pour mettre à jour le firmware et changer le verrouillage OEM des modules Sierra Wireless (EM7455, EM7565, MC7455) : procédures FOTA et flash USB, vérification de version avec AT+GMR, sauvegardes du firmware, récupération SED après un brick et les bonnes étapes pour éviter un flash raté."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "fr"
hreflang_group: "sierra-firmware-update-brand-lock-guide"
slug: "sierra-firmware-update-brand-lock-guide"
tags: ["Sierra Wireless", "firmware-update", "qmi-firmware-update", "EM7455", "EM7565", "MC7455", "brand-lock", "SED", "flashing"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/fr/products/sierra/"
faq:
  - question: "Flasher un module Sierra Wireless finit-il toujours par un brick ?"
    answer: "Non. La spécification officielle documente le mécanisme SED (Smart Error Detection) : après 6 redémarrages échoués d'affilée, le module entre en mode boot-and-hold et attend un téléchargement de firmware. C'est le chemin de récupération officiel. La plupart des bricks viennent d'une coupure de courant en plein flash ou d'un firmware incompatible."
  - question: "Peut-on changer le verrouillage de marque (Dell / Lenovo / Generic) ?"
    answer: "C'est une approche éprouvée par la communauté : flasher une autre image firmware change l'identité du module pour qu'elle corresponde à la liste blanche du BIOS du portable. Avant d'essayer, confirme ton modèle de module et prépare la bonne image."
  - question: "Que faire si le flash échoue et que le module redémarre sans arrêt ?"
    answer: "Laisse le module redémarrer jusqu'au mode boot-and-hold (après 6 redémarrages d'affilée), reconnecte-le en USB et utilise un outil de flash pour écrire la bonne image firmware."
---

# Guide Sierra Wireless : mise à jour du firmware et changement de verrouillage de marque, flasher sans briquer le module

**La version courte : tu peux mettre à jour le firmware d'un module Sierra par voie hertzienne (FOTA, poussé par l'opérateur) ou en le flashant toi-même en USB. Le verrouillage de marque qui inquiète tout le monde (la différence entre les éditions Dell ou Lenovo et la version générique) n'est en fait qu'un simple échange d'image firmware. Vérifie la version avec `AT+GMR` avant de flasher, ne coupe jamais le courant en plein flash, et si ça échoue quand même, le module embarque un mode de récupération SED qui peut le ramener à la vie.**

Beaucoup de gens achètent des modules Sierra Wireless sur le marché de l'occasion, les glissent dans leur portable ou leur routeur, et découvrent que la carte ne fonctionne pas. Le coupable, c'est le plus souvent le verrouillage OEM. Ce guide combine les faits solides de la spécification officielle avec ce que la communauté a appris à ses dépens, pour que tu puisses flasher ton module en toute sécurité.

> Sources techniques : spécifications officielles Sierra Wireless (EM7455, EM7565, MC7455). Le changement de verrouillage de marque et les outils tiers reposent sur la pratique de la communauté. Compilé par Yupitek.

---

## Les concepts clés en 30 secondes

Flasher n'est pas dangereux. Ce qui est dangereux, c'est de sauter les sauvegardes, de prendre le mauvais fichier et de débrancher le courant en plein flash.

| Ce qu'il faut savoir | Documenté dans la spécification ? | En clair |
|---|---|---|
| **FOTA (mise à jour par voie hertzienne)** | ✅ Oui | L'opérateur t'envoie la mise à jour directement, mais seulement s'il la prend en charge. |
| **Flash USB (outils constructeur)** | ✅ Oui | Connecte le module à un PC en USB et écris le firmware toi-même. L'approche la plus contrôlée. |
| **Vérifier la version du firmware (AT+GMR)** | ✅ Oui | Cette commande AT affiche la version actuelle du firmware. Fais-le avant chaque flash ! |
| **Verrouillage de marque (Dell/Lenovo)** | ⚠️ Pas directement | La spécification ne mentionne que le « support des étiquettes OEM ». Le mécanisme de verrouillage réel est une liste blanche mise en place par les fabricants de portables. |
| **qmi-firmware-update** | ⚠️ Non documenté | L'outil de flash de référence dans la communauté Linux open source. |

---

## C'est quoi le verrouillage de marque (verrou OEM), en fait ?

Quand Dell ou Lenovo achètent des modules à Sierra Wireless, ils demandent que le module porte leur logo et une image firmware dédiée, et ils intègrent une « liste blanche » dans le BIOS du portable.

Si ton module est l'édition Dell et que tu le branches sur un portable Lenovo, la machine peut se figer ou afficher une erreur au démarrage.
Si ton module est l'édition générique et que le portable applique une liste blanche stricte, tu es aussi coincé.

**C'est pour ça que les gens veulent « changer le verrouillage de marque »** : en pratique, ça veut dire télécharger l'image firmware de la bonne marque (ou la version générique) et l'écrire de force sur le module en USB, pour que le module se présente comme l'autre édition.

> ⚠️ **Remarque** : flasher le firmware de la mauvaise marque comporte un vrai risque. Découvre précisément quelle version ta carte mère exige avant de toucher à quoi que ce soit.

---

## Avant de flasher : trois étapes pour éviter le brick

Ne te précipite pas pour flasher dès que tu as un fichier. Suis la spécification et règle d'abord ces trois points :

### 1. Vérifie la version actuelle du firmware
Ouvre un terminal (minicom ou PuTTY font très bien l'affaire), connecte-toi au port AT du module et tape :
```text
AT+GMR
```
Fais une capture de la ligne de version. Si un flash tourne mal, tu sauras quelle version réinstaller.

### 2. Sauvegarde tes réglages
La spécification ne couvre pas les sauvegardes, mais en pratique tu devrais noter tes réglages APN actuels et tes paramètres PRI avant de toucher à quoi que ce soit.

### 3. Comprendre l'« arrêt sûr »
Couper le courant directement, c'est le péché cardinal, à la fois après un flash et avant de retirer le module. La spécification prévient explicitement qu'une perte de courant soudaine peut endommager le système de fichiers du module.
- **EM7455 / EM7565** : mets la broche `Full_Card_Power_Off#` à l'état bas, attends environ 20 à 25 secondes, puis coupe le courant.
- **MC7455** : envoie d'abord `AT!PCOFFEN=0`, puis mets `W_DISABLE_N` à l'état bas, attends quelques dizaines de secondes, puis débranche.

---

## Flasher en pratique : le flux USB

Si tu utilises `qmi-firmware-update`, le favori de la communauté Linux, le flux ressemble à peu près à ça (réfère-toi toujours à la documentation officielle de l'outil) :

1. **Récupère le bon fichier** : obtiens le paquet firmware de ton modèle exact auprès du constructeur ou du site officiel. L'EM7455 et l'EM7565 utilisent des puces complètement différentes, ne mélange jamais leurs images !
2. **Branche le module** : confirme que l'appareil apparaît dans `lsusb`.
3. **Arrête les services qui interfèrent** : éteins `ModemManager` et les services réseau similaires pour qu'ils ne s'emparent pas du port USB.
4. **Lance l'outil de flash** : donne-lui le fichier et démarre le flash.
5. **Les mains loin du clavier** : pendant le flash, le module est dans un état instable. **Ne coupe jamais le courant et ne débranche jamais le câble !** C'est là que la plupart des gens briquent leur module.
6. **Redémarre et vérifie** : après le flash, arrête proprement, rallume et exécute `AT+GMR` pour confirmer que la version a changé.

---

## Et si c'est déjà un brick ? (Le mécanisme de récupération SED)

Si le module redémarre en boucle après un flash et n'atteint jamais le système, ne le jette pas tout de suite.

Les modules Sierra embarquent une bouée de sauvetage appelée **SED (Smart Error Detection)**.
La spécification est explicite : **si le module plante et redémarre 6 fois d'affilée au boot, il abandonne et passe en mode « boot-and-hold ».** Ce mode est la porte laissée ouverte pour que tu réinstalles le firmware.

**Étapes de récupération :**
1. Laisse-le redémarrer. Après le 6e cycle, il se stabilise et reste en attente (mode boot-and-hold).
2. Reconnecte le câble USB.
3. Ouvre ton outil de flash, choisis un paquet firmware connu comme bon, et flashe à nouveau.
4. Dans la plupart des cas, ça ramène le module à la vie.

> Si l'USB ne se connecte pas du tout, essaie un reset matériel (RESET#). Le timing varie selon le module : environ 3 à 5,5 secondes sur l'EM7455, et 0,2 à 2,5 secondes sur l'EM7565. Si tu attends trop longtemps, le cycle recommence, il faudra donc viser le bon timing.

---

## Conclusion

Flasher un module Sierra Wireless ou changer son verrouillage de marque ressemble beaucoup au flash d'un téléphone : **il y a une procédure standard et un mécanisme de récupération, donc tant que tu ne improvises pas, tu t'en sors.**

Les gros pièges sont en réalité :
1. Prendre le firmware du mauvais modèle.
2. Couper le câble d'alimentation en plein flash.
3. Oublier d'arrêter le module proprement.

Vérifie la version (`AT+GMR`) avant de commencer, prépare la bonne image et donne au module une alimentation stable. Tu pourras offrir une nouvelle vie à ta carte WWAN en toute confiance.

## Où acheter (appel à l'action)

Tu ne sais pas si ton module est l'édition Dell ou Lenovo ? Tu cherches un module Sierra fiable pour faire évoluer ton appareil ? Yupitek propose des solutions matérielles complètes et des conseils techniques.
Écris-nous : **sales@yupitek.com**
Découvre la gamme : [Modules Sierra Wireless](https://yupitek.com/fr/products/sierra/)
