---
title: "Solution de liaison cellulaire pour la vidéosurveillance et l'affichage numérique : comment choisir entre Cat 6 et 5G ? | Yupitek"
description: "Quel module cellulaire faut-il pour les caméras et l'affichage numérique ? Tout dépend de la direction du trafic : vers le haut ou vers le bas ! Cet article compare les EM7455 (Cat 6), EM7565 (Cat 12) et EM9191 (5G) sur la base des spécifications officielles, pour que tu choisisses précisément sans gaspiller ton argent."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "fr"
hreflang_group: "video-surveillance-digital-signage-cellular-backhaul-cat6-to-5g"
slug: "video-surveillance-digital-signage-cellular-backhaul-cat6-to-5g"
tags: ["Sierra Wireless", "EM7455", "EM7565", "EM9191", "vidéosurveillance 4G", "affichage numérique", "retour vidéo 5G", "Cat 6", "LTE"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/fr/products/sierra/"
faq:
  - question: "Quel débit montant faut-il pour le retour 4G d'une caméra de surveillance ?"
    answer: "Un flux 1080p H.264 consomme environ 2~6 Mbit/s. Avec le EM7455 (limite montante de 50 Mbit/s), on peut transporter de manière stable environ 4~6 flux 1080p. Pour des besoins plus importants, il est conseillé de passer au EM7565."
  - question: "Le Cat 6 suffit-il pour connecter de l'affichage numérique ?"
    answer: "L'affichage numérique fonctionne surtout en « téléchargement ». Le Cat 6 (comme le EM7455) offre 300 Mbit/s de débit descendant, largement suffisant pour des mises à jour d'images et de vidéos courantes. Pour pousser très fréquemment de très gros fichiers vidéo 4K, tu peux passer au EM7565 (600 Mbit/s) pour réduire le temps de téléchargement."
  - question: "À quoi faut-il faire attention en installant un module 4G/5G dans un boîtier extérieur ?"
    answer: "Deux points essentiels : la dissipation thermique et l'alimentation. La température interne du module ne doit généralement pas dépasser 90°C~115°C. Les boîtiers extérieurs surchauffent facilement, il faut donc bien évacuer la chaleur. De plus, un module 5G peut consommer jusqu'à 2.7A en pic, le bloc d'alimentation doit encaisser cette pointe de courant."
---

Une caméra envoie ses images vers le backend, et un écran publicitaire au bord de la route télécharge les dernières annonces. Quel module 4G/5G faut-il acheter pour que ce soit suffisant ? La vraie question n'est pas « plus c'est rapide, mieux c'est », mais de savoir si ton trafic monte ou descend. Nous prenons trois modules populaires de Sierra Wireless, les EM7455, EM7565 et EM9191, et à partir des chiffres réels des spécifications officielles, nous te montrons si tu as besoin de Cat 6, de Cat 12 ou directement de 5G.

{{< tldr >}}
Les caméras envoient leurs images vers le backend, les écrans publicitaires téléchargent les dernières annonces. Le point clé n'est pas « plus c'est rapide, mieux c'est », mais la direction du trafic : vers le haut ou vers le bas. Nous prenons les EM7455, EM7565 et EM9191 comme exemple et, à partir des spécifications officielles, nous te montrons si tu as besoin de Cat 6, de Cat 12 ou directement de 5G.
{{< /tldr >}}

**En une phrase : ne fonce pas sur le 5G les yeux fermés. Demande-toi d'abord si ta machine « envoie beaucoup » ou « reçoit beaucoup ». Une caméra transmet sans cesse des images vers le cloud : regarde le débit montant (Uplink). Un écran publicitaire télécharge sans cesse de nouvelles vidéos : regarde le débit descendant (Downlink). Si tu n'as que quelques flux 1080p à transmettre, la carte Cat 6 la moins chère suffit largement !**

Beaucoup de clients, quand ils lancent un appel d'offres pour des travaux réseau sur des « caméras de carrefour » ou des « écrans publicitaires de chaînes de magasins », déclarent d'emblée : « Donne-moi le module 5G le plus rapide ! »
Résultat : ils dépensent une grosse somme pour quelque chose dont ils n'ont en réalité aucun besoin.

Choisir une carte réseau, ce n'est pas choisir une voiture de sport. Ce n'est pas « plus vite, c'est mieux », mais il faut traiter la cause. Dans cet article, nous passons au crible les trois modules M.2 les plus courants de Sierra Wireless (EM7455, EM7565, EM9191) et, avec les chiffres des spécifications officielles, nous t'apprenons à choisir le plus rentable.

> Source des données techniques : spécifications officielles Sierra Wireless. Article compilé par Yupitek.

---

## Guide de choix rapide en 30 secondes : laquelle acheter ?

| Ton scénario | Trafic principal | Quelle carte ? | Pourquoi ? |
|---|---|---|---|
| **Petit projet : 1~4 caméras 1080p** | Montant (UL) | **EM7455 (Cat 6)** | Sa limite montante est de 50 Mbit/s, largement de quoi porter quelques caméras 1080p, et c'est la moins chère. |
| **Moyen à grand : 5~10 caméras 1080p ou 4K** | Montant (UL) | **EM7565 (Cat 12)** | Le débit montant fait un bond à 150 Mbit/s, la marge est confortable. |
| **Mise à jour de la publicité sur écran numérique** | Descendant (DL) | **EM7565 (Cat 12)** | Jusqu'à 600 Mbit/s en descendant : un clip publicitaire 4K de quelques Go se télécharge en un instant. |
| **Le monstre : multi-stream 4K en direct + écran** | Rapide dans les deux sens | **EM9191 (5G)** | 5G plus la fiche technique musclée du LTE Cat 20. Si l'argent n'est pas un problème, achète-le. |

---

## Pourquoi distinguer « montant » et « descendant » ?

Parce que dans le monde 4G/5G, **le débit descendant est généralement 5 à 6 fois supérieur au débit montant !**

Prends le EM7455 le plus basique : la fiche officielle indique 300 Mbit/s en descendant, mais seulement **50 Mbit/s** en montant.
Si tu regardes les 300 Mbit/s avec enthousiasme et décides de brancher 10 caméras 4K dessus, tu vas sûrement douter de tout : car ce que les caméras consomment, ce sont ces maigres 50 Mbit/s !

| Appareil | Son comportement réseau | La caractéristique à regarder |
|---|---|---|
| **Caméra / NVR** | Envoie en permanence les images à l'extérieur | **Montant (Uplink, UL)** |
| **Affichage numérique** | Télécharge les vidéos prêtes à diffuser | **Descendant (Downlink, DL)** |
| **Borne interactive** | Télécharge des vidéos, remonte parfois des données de clic | **Descendant en priorité, montant en complément** |

---

## Calculons : de combien de débit montant une caméra a-t-elle besoin ?

(Attention : ce sont des valeurs empiriques du secteur, elles varient selon le codec et la dynamique de l'image)

- 1 flux **1080p (H.264)** = environ **2~6 Mbit/s**
- 1 flux **4K (H.265)** = environ **8~16 Mbit/s**

Si tu as 6 caméras 1080p, le calcul donne `6 caméras × 5 Mbit/s = 30 Mbit/s`.
Le EM7455 (montant 50 Mbit/s) semble alors juste ? Non ! **Dans la réalité, il est impossible d'atteindre la limite théorique.** Compte tenu de l'affaiblissement du signal, c'est déjà une situation très tendue. Je recommande de passer directement au EM7565 (montant 150 Mbit/s) pour la stabilité.

---

## Trois générations côte à côte : EM7455 vs EM7565 vs EM9191

Regardons les chiffres matériels des spécifications officielles :

| Spécification | EM7455 (Cat 6) | EM7565 (Cat 12) | EM9191 (5G) |
|---|---|---|---|
| **Limite descendante (DL)** | 300 Mbit/s | 600 Mbit/s | Cat 20 (très rapide) |
| **Limite montante (UL)** | 50 Mbit/s | 150 Mbit/s | montant de niveau Cat 12 |
| **Nombre de connecteurs antenne** | 3 | 3 | 4 (branche-les tous) |
| **Température de fonctionnement max.** | interne max. 93°C | interne max. 90°C | interne max. 115°C |
| **Courant de pointe** | 1.5A | 1.5A (surtension 2.5A) | monte à 2.7A (2700 mA) |

---

## Tu installes le module dans un coffret extérieur ? Attention à la cuisson !

Quand tu installes ces modules dans un coffret de caméra au bord de la route ou dans un écran publicitaire, surveille ces deux ennemis :

### 1. Il a de la fièvre
Ces trois modules craignent la chaleur. Le fabricant recommande de rester si possible sous 80°C~100°C. En été, la température dans un coffret extérieur à Taïwan dépasse facilement 60 degrés. Si tu ne colles pas de dissipateur et n'évacues pas la chaleur, le module réduira sa vitesse dès qu'il a chaud, puis finira par planter complètement.

### 2. Alimentation : donne de la marge
Surtout le géant 5G EM9191 : en pleine transmission de données, il peut tirer jusqu'à **2.7A** en pointe ! Si ton bloc d'alimentation est trop juste, la tension chute et le module redémarre en boucle infinie.

---

## Conclusion

Acheter une carte réseau, c'est comme louer un camion : selon la quantité de marchandises, tu loues la bonne taille.

- **Économie d'abord** : si tu as des caméras 1080p (jusqu'à 4) ou un écran avec du texte et des images simples, achète le **EM7455** les yeux fermés.
- **Meilleur rapport qualité-prix** : si les images sont nombreuses et nettes, ou si l'écran télécharge souvent de gros fichiers, le **EM7565** avec 150 Mbit/s en montant et 600 Mbit/s en descendant est le point idéal actuel.
- **Guerrier du futur** : sauf si le client exige explicitement le 5G, ou si tu as plusieurs flux 4K à diffuser en direct en même temps, ne t'intéresse au module 5G **EM9191**, chaud et gourmand, qu'ensuite.

## Où acheter (Call To Action)

Tu prépares une solution de retour vidéo ou de connexion pour l'affichage numérique ? Yupitek propose la gamme complète de modules Sierra Wireless ainsi qu'un accompagnement technique professionnel pour t'aider à trouver la combinaison la plus rentable !
Écris-nous : **sales@yupitek.com**
Voir les produits : [Sierra Wireless](https://yupitek.com/fr/products/sierra/)

{{< faq >}}
