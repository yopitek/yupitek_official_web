---
title: "Connectivité cellulaire BVLOS pour drones et robots d'inspection : comment assurer un backhaul à faible latence | Yupitek"
description: "Comment connecter un drone hors ligne de vue (BVLOS) ? Cet article compare les Sierra EM9190, EM9191 et EM7565 : architecture 5G SA à faible latence, envoi vidéo et géolocalisation double fréquence L1/L5, pour que tu construises une solution sans coupure pour robots d'inspection et drones."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "fr"
hreflang_group: "drone-bvlos-cellular-connectivity-low-latency-backhaul"
slug: "drone-bvlos-cellular-connectivity-low-latency-backhaul"
tags: ["Sierra Wireless", "EM9190", "EM9191", "EM7565", "drones", "BVLOS", "5G", "faible latence", "GNSS", "LTE"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/fr/products/sierra/"
faq:
  - question: "Pourquoi un drone en BVLOS doit-il absolument utiliser la connectivité cellulaire ?"
    answer: "Quand le drone sort de la ligne de vue, le signal du boîtier de commande se coupe. Le réseau 4G/5G est alors la seule solution offrant une couverture étendue, un contrôle à faible latence et une transmission vidéo à large bande passante."
  - question: "Quelle est la différence entre les EM9190 et EM9191 ?"
    answer: "Le EM9190 prend en charge en plus les ondes millimétriques 5G (mmWave), mais nécessite des antennes en réseau très énergivores et encombrantes. Dans les régions sans réseau millimétrique, le EM9191, pur 5G Sub-6, est le choix le plus adapté."
  - question: "Quel module convient à un robot d'inspection ?"
    answer: "Pour l'inspection d'un site industriel, il suffit généralement de renvoyer une vidéo standard : le module 4G EM7565 (Cat 12, 150 Mbit/s en montant) répond aux besoins et coûte moins cher."
---

Quand un drone ou un robot quitte ta ligne de vue (c'est ce qu'on appelle le BVLOS, Beyond Visual Line of Sight), ta télécommande classique ne sert plus à rien. Il ne reste alors que la carte 4G/5G embarquée : elle se connecte à la station de base, renvoie la vidéo haute définition et reçoit les commandes de ton manche.

{{< tldr >}}
Une fois hors ligne de vue (BVLOS), la télécommande ne sert plus à rien et le 4G/5G devient la seule bouée de sauvetage : transmission vidéo, commandes et coordonnées. Nous décortiquons les EM9190, EM9191 et EM7565 et te montrons quels secrets de faible latence et de géolocalisation précise L1+L5 se cachent dans les spécifications officielles.
{{< /tldr >}}

**En une phrase : pour faire voler un drone hors de la ligne de vue, il te faut un module 4G/5G capable de gérer à la fois la « transmission vidéo, la télécommande et la géolocalisation ». Si ton drone doit se connecter à un réseau privé 5G, exige une vitesse d'envoi vidéo extrême et une géolocalisation double fréquence L1+L5 ultra-précise, choisis le EM9191. Si c'est juste un robot d'inspection qui avance lentement sur un site industriel, le module 4G EM7565, économique et fiable, suffit amplement.**

Dans cet article, nous prenons les spécifications officielles de Sierra Wireless pour te dévoiler : pourquoi ces modules conviennent-ils particulièrement aux drones et aux robots ? Comment parviennent-ils à une faible latence ?

> Source des données techniques : spécifications officielles Sierra Wireless (EM9190/EM9191, EM7565). Article compilé par Yupitek.

---

## Choix rapide en 30 secondes : quel module installer dans le drone / le robot ?

| Scénario | Module recommandé | Pourquoi lui ? |
|---|---|---|
| **Drone haut de gamme (réseau privé 5G)** | **EM9191** | Prend en charge le 5G Sub-6 et l'architecture 5G SA pour réseaux privés, vitesse montante LTE Cat 20 au sommet, et géolocalisation haute précision L1+L5 intégrée. |
| **Drone haut de gamme (marché américain)** | **EM9190** | Le grand frère du EM9191, avec en plus les ondes millimétriques (mmWave). Inutile à Taïwan. |
| **Robot d'inspection de site (au sol)** | **EM7565** | C'est un module 4G Cat 12 : léger et économe. Pour une inspection de site, le 5G serait tuer une mouche avec un canon, le choix le plus rentable. |

---

## Comment la faible latence est-elle obtenue ? Les secrets des spécifications

Les joueurs savent que le ping (latence) est crucial. Pour un drone dans le ciel, la latence peut être une question de vie ou de mort. Les spécifications n'indiquent pas « latence en millisecondes », mais il y a trois armes qui réduisent fortement la latence :

1. **Architecture 5G SA (standalone)** : les EM919x supportent l'architecture SA (Option 2). Concrètement, le drone se connecte directement au cœur de réseau 5G, sans passer par les vieilles stations de base 4G. C'est le levier le plus puissant pour réduire la latence.
2. **Contrôle de priorité QoS QCI** : le module prend en charge les réglages QoS du 3GPP R15. Tu peux définir une priorité plus élevée pour les « commandes de vol » que pour la « transmission vidéo ». Même en cas d'engorgement réseau, la machine ne perd pas le contrôle.
3. **Agrégation de porteuses montantes (UL CA) et 256QAM** : le retour vidéo dépend entièrement du débit montant. Les EM919x comme le EM7565 savent regrouper plusieurs bandes en montant et utilisent la modulation avancée 256QAM (EM919x) ou 64QAM (EM7565) pour que la transmission vidéo reste fluide, sans à-coups.

---

## Drone vs robot d'inspection : des logiques de choix très différentes

Ce qui vole dans le ciel et ce qui roule au sol n'ont pas du tout les mêmes exigences vis-à-vis de la carte réseau.

### Drone (Drone) : extrêmement sensible au poids, à la chaleur et à la géolocalisation
- **Le poids, c'est de l'autonomie** : le EM9191 mesure 52 mm de long et pèse 9 g ; le EM7565 mesure 42 mm et pèse 6.5 g.
- **Précision de géolocalisation** : le drone dépend fortement du GPS. Les EM919x embarquent une **GNSS double fréquence L1 + L5**, nettement plus précise qu'un GPS monofréquence classique et bien protégée contre les interférences.
- **Nombre d'antennes** : les EM919x exigent les 4 antennes pour exploiter pleinement le MIMO. En concevant le carénage du drone, il faut prévoir l'emplacement de ces 4 antennes. Et si tu choisis le EM9190 avec ses antennes millimétriques en plus, le poids et la consommation deviennent encore plus lourds.

### Robot d'inspection (Robot) : sensible à la stabilité et au coût
- Le robot avance lentement au sol, construit généralement sa carte avec un lidar (LiDAR) et dépend moins du GPS. Le GPS monofréquence intégré du EM7565 suffit.
- Le ventre du robot offre beaucoup d'espace et une grosse batterie, mais sur un site industriel il n'y a souvent que du 4G. Là, le EM7565 (Cat 12, 150 Mbit/s en montant) est déjà largement suffisant, pas besoin de forcer sur le 5G.

---

## Les pièges matériels à connaître avant l'embarquement

Si tu es ingénieur en intégration matérielle, avant de dessiner le module sur la carte, note ceci :

1. **Ne te laisse pas bluffer par le mmWave (ondes millimétriques)** : beaucoup pensent qu'il faut acheter le EM9190 haut de gamme pour jouer avec les ondes millimétriques. En réalité, les ondes millimétriques traversent extrêmement mal les obstacles, et il n'existe pratiquement aucun réseau privé mmWave à Taïwan. Pour 99% des drones, le **EM9191** compatible Sub-6 est le choix parfait, et il t'épargne tout un tas d'antennes externes compliquées.
2. **Attention à la surchauffe** : les EM919x sont des géants 5G, la ligne rouge de température interne est à 115°C (recommandé : rester sous 100°C). En été, un drone exposé au soleil en altitude, avec le module enfermé dans un boîtier plastique sans circulation d'air, il est certain que ça réduira la vitesse, voire coupera la liaison.
3. **Ne lésine pas sur les câbles d'antenne** : la spécification exige une perte de câble inférieure à 0.5 dB avec une impédance de 50 ohms. Acheter un module haut de gamme mais le relier avec des câbles de mauvaise qualité, et la qualité de ta transmission vidéo sera tout simplement lamentable.

## Conclusion

Pour bâtir une solution de liaison hors ligne de vue (BVLOS), les modules Sierra Wireless ont déjà emballé « la bande passante vidéo, l'architecture à faible latence et la géolocalisation haute précision » dans une petite carte M.2.
Tu voles dans le ciel, tu as le budget et tu veux un réseau privé 5G : prends directement le **EM9191**. Tu roules au sol et il te faut juste une transmission stable en 1080p : le choix le plus serein est le **EM7565**.

## Où acheter (Call To Action)

Tu conçois la carte de communication d'un drone ou d'un robot d'inspection ? Tu ne sais pas comment planifier les antennes et le refroidissement ? Yupitek propose la gamme complète de modules Sierra Wireless et un service de conseil en intégration matérielle.
Écris-nous : **sales@yupitek.com**
Voir les produits : [Sierra Wireless](https://yupitek.com/fr/products/sierra/)

{{< faq >}}
