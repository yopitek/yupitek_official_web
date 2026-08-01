---
title: "Comment faire un failover 4G/5G sur un routeur industriel : le cas du module EM9191 en 5G privée | Yupitek"
description: "Comment mettre en place un failover 4G/5G sur ton routeur industriel ? Avec le module EM9191 en exemple, on explique la différence entre un réseau 5G SA privé et une architecture LTE de secours, plus les points clés : bandes de fréquence, antennes et dissipation thermique."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "fr"
hreflang_group: "industrial-router-4g-5g-failover-guide"
slug: "industrial-router-4g-5g-failover-guide"
tags: ["Sierra Wireless", "EM9191", "5G", "LTE", "Failover", "Private 5G"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/fr/products/sierra/"
faq:
  - question: "Le EM9191 supporte-t-il la 5G mmWave ?"
    answer: "Non. La fiche technique officielle indique clairement que le EM9191 ne supporte pas le FR2 (mmWave). Pour les ondes millimétriques, choisis le EM9190."
  - question: "Peut-on utiliser le EM9191 dans un réseau 5G privé ?"
    answer: "Oui. Les réseaux 5G privés reposent surtout sur l'architecture SA (Standalone), et le EM9191 supporte pleinement l'architecture SA en 5G NR FR1."
  - question: "À quoi faire attention lors de l'intégration du EM9191 dans un routeur ?"
    answer: "Quatre points : 1. La longueur est de 52 mm, pas 42 mm. 2. Il faut brancher les 4 antennes. 3. L'alimentation doit encaisser un pic de 2,7 A. 4. La dissipation thermique est essentielle, la température interne ne doit pas dépasser 115 °C."
---

# Comment faire un failover 4G/5G sur un routeur industriel : le cas du module EM9191 en 5G privée

**En une phrase : ajouter un module 5G à ton routeur industriel pour le secours, c'est comme prendre une assurance. Le module Sierra Wireless EM9191 gère à la fois la 4G ultra-rapide (LTE Cat 20) et les réseaux 5G privés (5G SA). Tu peux donc démarrer dès maintenant en backup 4G, et quand ton site se dotera d'un réseau 5G privé, pas besoin de changer de matériel. Transition en douceur !**

Dans une usine, chaque minute de coupure réseau coûte de l'argent. Les données des machines ne remontent plus, le monitoring à distance devient noir, et la perte dépasse largement le coût d'une ligne de secours. Voilà pourquoi la redondance (Failover) est si importante. Plutôt que de tirer une deuxième fibre physique chez un autre opérateur, la solution la plus maligne, c'est une carte SIM et le réseau mobile.

Dans cet article, on décortique la fiche technique officielle (EM919X Product Technical Specification) pour te montrer pourquoi le **EM9191** est le choix parfait : pour le secours aujourd'hui, pour le réseau privé demain.

> Source des données techniques : fiche technique officielle Sierra Wireless. Article préparé par Yupitek.

---

## Lecture en 30 secondes : de quoi le EM9191 est-il capable ?

| Ton besoin | Le EM9191 assure ? | Pourquoi ? |
|---|---|---|
| **Backup internet 4G** | ✅ Carrément | Il supporte le LTE Cat 20 (agrégation 7CC), largement suffisant pour un secours. |
| **Connexion à un réseau 5G privé** | ✅ Carrément | Support de l'architecture SA en 5G FR1 (Sub-6), la condition obligatoire pour la 5G privée. |
| **5G ondes millimétriques (mmWave)** | ❌ Pas du tout | C'est écrit noir sur blanc dans la fiche ! Pour le mmWave, prends le EM9190. |
| **Juste faire des économies** | ⚠️ Regarde un autre modèle | Si tu es sûr à 100 % de ne jamais utiliser la 5G, un module purement 4G (EM7690 ou EM7565 par exemple) coûte beaucoup moins cher. |

---

## Comment fonctionne le failover ?

Simple : dans ton routeur, un petit logiciel sentinelle ping en permanence ton réseau principal (la fibre, par exemple). Quand il détecte que le réseau principal est mort, il crie : « Bascule ! » et dirige tous les paquets de données vers le module EM9191 installé dans le routeur, qui les envoie en 5G. Une fois le réseau principal revenu, le trafic revient discrètement.

**Autrement dit, une ligne de secours ne doit pas être « la plus rapide », elle doit être « infaillible ».** L'astuce du EM9191 : si le signal 5G devient mauvais, il bascule tout seul en 4G et continue de transmettre. Pas de coupure.

---

## Pourquoi le EM9191, c'est deux futurs pour le prix d'un ?

À l'intérieur du EM9191 se trouve la puce 5G Qualcomm SDX55. Selon la fiche officielle, elle supporte les deux modes les plus importants :

1. **LTE Only** (mode 4G pur)
2. **5G NR FR1 SA / NSA** (standalone et non-standalone)

Concrètement ?
- **Aujourd'hui** : tu t'en sers comme d'une carte 4G haut de gamme (niveau Cat 20), parce que la 5G publique a encore des zones d'ombre.
- **Demain** : quand ton entreprise construira son propre « réseau 5G privé » (souvent en architecture SA, la plupart du temps en Sub-6), il suffira de changer un réglage pour te connecter. Pas besoin de racheter du matériel !

---

## Les vraies infos pour les ingénieurs : 4 pièges avant l'intégration

Ne crois pas que « module acheté, branché, terminé ». Le EM9191 est un ogre en énergie et en chaleur. À l'intégration dans ton routeur, surveille ces quatre points :

### 1. Antennes incomplètes, moitié de la vitesse
Le EM9191 a **4 connecteurs d'antenne MHF4**. Pour exploiter pleinement son MIMO 4x4 (surtout sur la bande n78 en 5G), il faut brancher les 4 antennes ! Et officiellement, l'affaiblissement du câble doit rester sous 0,5 dB. Pas de câbles pourris interminables.

### 2. Alimentation trop faible, déconnexions en rafale
Le EM9191 fonctionne en 3,3 V. Point crucial : en transmission, le **pic de courant atteint 2,7 A (2700 mA), et 2 A (2000 mA) en continu**. Si l'alimentation de ta carte mère est trop légère, la tension s'effondre dès que le module accélère, et c'est le redémarrage en boucle.

### 3. Pas de refroidissement, tu attends le crash
Un module 5G chauffe beaucoup plus qu'un module 4G. Officiellement, la température interne **ne doit jamais dépasser 115 °C (idéalement sous 100 °C)**. Si tu le mets dans un routeur industriel en tôle sans aération, en été c'est la surchauffe garantie. Prévoyez un dissipateur et conduis la chaleur vers le boîtier.

### 4. Longueur du slot et interface
C'est un format M.2, mais avec **52 mm de long**, soit nettement plus que les modules 42 mm habituels. L'interface peut être PCIe Gen3 ou USB 3.1 Gen2. Attention : le support de l'ancien USB 2.0 n'est pas garanti !

---

## Conclusion

Pour sécuriser tes équipements industriels, le EM9191 est un choix « attaque et défense » parfait.
Avec son LTE Cat 20 costaud et son support 5G SA, il couvre idéalement les deux scénarios : « backup 4G maintenant » et « réseau 5G privé plus tard ». Si tu maîtrises l'alimentation (pic 2,7 A), la dissipation (limite 115 °C) et les antennes (les 4 branchées), il te sauvera la mise au moment critique.

## Infos achat (Call to Action)

Tu veux intégrer le EM9191 dans ton routeur industriel ? Yupitek propose des solutions matérielles complètes et un support technique de première ligne, pour t'aider sur les points les plus délicats : la chaleur et les antennes.
Écris-nous : **sales@yupitek.com**
Découvre les produits : [Série Sierra Wireless](https://yupitek.com/fr/products/sierra/)
