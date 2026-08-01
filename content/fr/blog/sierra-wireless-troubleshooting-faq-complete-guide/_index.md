---
title: "FAQ des modules Sierra Wireless : la carte de dépannage du « périphérique non détecté » au « pas de connexion réseau »"
description: "La carte de dépannage 4G/5G Sierra Wireless : du périphérique non détecté, aux interfaces QMI/MBIM disparues, en passant par une SIM non enregistrée et l'absence de réseau. Cet article vous montre, avec les commandes AT et les outils Linux/Windows, comment diagnostiquer précisément le problème en quatre couches, sans détour."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "sierra-wireless-troubleshooting-faq-complete-guide"
tags: ["sierra-wireless", "cellular-module", "troubleshooting", "lte", "5g", "qmi", "mbim"]
featureimage: "/images/products/sierra/sierra_banner.png"
author: "benny-lai"
lastmod: 2026-07-31
related_product: "/fr/products/sierra/"
faq:
  - question: "Mon module Sierra Wireless n'est pas détecté du tout par l'ordinateur. Quelle est la cause la plus probable ?"
    answer: "Le plus souvent, c'est un problème de couche matérielle : une alimentation insuffisante provoque des redémarrages, le slot M.2 a un mauvais contact, ou la broche W_DISABLE# est tirée vers le bas par la carte mère, ce qui met le module en mode avion. Commencez par vérifier avec lsusb ou le gestionnaire de périphériques."
  - question: "L'USB voit le module, mais il n'y a pas d'interface de connexion sous Linux. Que faire ?"
    answer: "Cela signifie que l'hôte n'a pas lié le bon pilote d'interface. Soit le noyau Linux n'a pas les pilotes qmi_wwan / cdc_mbim, soit la composition USB interne du module est mal réglée et masque le canal Internet."
  - question: "Toutes les interfaces sont là, mais la connexion 4G ne s'établit pas. Où est le problème ?"
    answer: "Dans neuf cas sur dix, c'est la carte SIM ou l'APN. Ouvrez le terminal, saisissez AT+CPIN? pour vérifier l'état de la SIM, puis AT!GSTATUS? pour confirmer l'enregistrement auprès de la station de base. Vérifiez enfin que vos paramètres APN correspondent aux exigences de votre opérateur."
---

# FAQ des modules Sierra Wireless : la carte de dépannage du « périphérique non détecté » au « pas de connexion réseau »

Quand on travaille avec des modules 4G/5G Sierra Wireless (que ce soit l'EM7455, l'EM7565 ou le tout récent EM919x), le pire est quand le module « ne réagit pas » ou « ne se connecte pas » une fois branché.

Les tutos sur Internet sont éparpillés : tantôt on vous dit de flasher le firmware, tantôt de changer les réglages. Cet article vous donne une « carte de dépannage en quatre couches ». Suivez les étapes dans l'ordre, et vous trouverez forcément le problème.

{{< tldr >}}
Votre module Sierra Wireless (EM7455, EM7565, EM919x, MC7455) pose problème ? Beaucoup, face à « pas de connexion », veulent flasher le firmware aussitôt. Or le dépannage, c'est comme peler un oignon : il y a un ordre précis. D'abord l'énumération USB (périphérique non détecté ?), puis l'interface QMI/MBIM (pilote ou composition erronés ?), ensuite la SIM et l'APN (pas d'enregistrement ?), et enfin les antennes et le refroidissement. Cet article réunit cette « carte de dépannage en quatre couches » avec un tableau de référence des commandes AT (comme AT+GMR, AT!PCTEMP), pour que les ingénieurs et les makers trouvent le cœur du problème en cinq minutes !
{{< /tldr >}}

**En bref : votre carte ne se connecte pas ? Vérifiez d'abord si l'ordinateur la voit (énumération USB), ensuite si un canal de données existe (interface QMI/MBIM), puis si la carte SIM et l'APN sont bons (enregistrement), et seulement à la fin les antennes et le refroidissement. Neuf personnes sur dix échouent à la troisième étape. Surtout, ne vous lancez pas à l'aveugle dans un flash de firmware !**

> Sources : spécifications officielles Sierra Wireless. Les procédures de dépannage proviennent de l'expérience terrain. Article compilé par Yupitek (Yughe Technology).

---

## Repérez le problème en 30 secondes

Regardez d'abord quel symptôme correspond à votre cas, et sautez directement à la couche concernée !

| Votre symptôme | Quelle couche est en cause ? | Quelle commande utiliser ? |
|---|---|---|
| **L'ordinateur ne voit pas du tout le module** | **C1 (couche matérielle/USB)** | Gestionnaire de périphériques Windows / Linux `lsusb` |
| **L'USB est vu, mais pas d'interface de connexion** | **C2 (couche interface/pilotes)** | Linux `ls /dev/cdc-wdm*` ou vérification du pilote lié |
| **Interface présente, mais la connexion échoue ou pas d'IP** | **C3 (couche SIM/APN)** | Ouvrir le terminal, saisir `AT+CPIN?` et `AT!GSTATUS?` |
| **Connecté, mais lent, coupures fréquentes ou pas de GPS** | **C4 (couche antennes/refroidissement)** | `AT!PCTEMP` pour la température, `AT+CSQ` pour le signal |

---

## Couche 1 (C1) : l'ordinateur ne détecte pas du tout le module

Là, vous n'avez même pas la chance d'envoyer une commande AT. Si `lsusb` ne montre aucun périphérique Sierra ni périphérique commençant par 1199, c'est **à 100 % un problème matériel**.

**Les trois coupables habituels :**
1. **Pas assez d'alimentation** : le module fonctionne en 3,3 V (certains en 3,7 V) et peut tirer plus de 2 A au démarrage. Avec un adaptateur USB bon marché, l'alimentation s'effondre et le module redémarre en boucle.
2. **Mauvais contact** : la languette de maintien n'est pas bien enclenchée, ou la carte adaptatrice est cassée.
3. **Désactivé par la broche « mode avion »** : le slot M.2 possède une broche `W_DISABLE#`. Si la carte mère la tire vers le bas, le module ne démarre tout simplement pas.

> 💡 **Le saviez-vous ?** Si le module plante six fois de suite à cause d'une alimentation instable, il entre en **mode de protection SED (Smart Error Detection)** (appelé « brick » dans le langage courant). Dans ce cas, rebranchez l'USB et reflashez le firmware avec l'outil officiel pour le ressusciter.

---

## Couche 2 (C2) : l'USB est vu, mais aucune interface de communication

`lsusb` voit le périphérique, mais sous Linux on ne trouve ni `/dev/ttyUSB*` (pour les commandes AT) ni `/dev/cdc-wdm0` (pour se connecter à Internet).

**Qui est coupable ?**
1. **Pilotes Linux non installés** : assurez-vous que `qmi_wwan` (pour QMI) ou `cdc_mbim` (pour MBIM) sont bien chargés.
2. **Mauvaise composition USB (combinaison d'interfaces)** : le module a un réglage appelé USB Composition. Parfois il est réglé en « mode diagnostic uniquement », ne laissant que quelques ports COM et masquant le canal Internet. Vérifiez avec `AT!USBCOMP?` et repassez sur un mode avec QMI ou MBIM.

---

## Couche 3 (C3) : toutes les interfaces sont là, mais pas de connexion (la plupart restent bloqués ici)

Tous les ports sont présents, mais la connexion échoue. Ouvrez un logiciel de terminal (par exemple minicom ou PuTTY), connectez-vous au port AT et menez l'enquête avec ces commandes, dans l'ordre :

### 1. La carte SIM est-elle en bon état ?
```text
AT+CPIN?
```
- Réponse `READY` : la SIM est lue correctement et n'est pas verrouillée par un code PIN.
- Réponse `SIM PIN` ou même `ERROR` : félicitations, vous avez trouvé le problème. La carte est mal insérée ou verrouillée.

### 2. Une station de base est-elle trouvée ?
```text
AT!GSTATUS?
```
C'est une commande Sierra très puissante (en cas d'erreur, vous devrez peut-être d'abord saisir `AT!ENTERCND="<mot de passe>"` pour déverrouiller les droits). Elle vous indique sur quelle bande vous êtes, la force du signal et si vous êtes enregistré sur le réseau.

### 3. L'APN est-il bien configuré ?
Pas besoin de commande ici. Retournez dans votre logiciel de connexion (par exemple NetworkManager ou la configuration OpenWrt). Chez des opérateurs comme Chunghwa Telecom ou Taiwan Mobile, l'APN est généralement `internet`. Avec un projet en IP fixe, l'APN est forcément différent, appelez alors votre opérateur.

---

## Couche 4 (C4) : connecté, mais lent, avec des coupures ou sans GPS

### 1. Antennes mal branchées ou incomplètes
Ces cartes ont de trois à quatre petits trous d'antenne (MHF4 ou U.FL).
**Branchez au minimum MAIN et AUX !** Avec MAIN seul, vous accédez à Internet, mais la vitesse et la stabilité en prennent un coup.
Pour le GPS, l'antenne doit impérativement être branchée sur la prise marquée **GNSS**.

### 2. GPS oublié d'être activé
Si l'antenne est bien branchée mais que la position ne se trouve pas, le module a probablement coupé le GPS pour économiser l'énergie. Réveillez-le avec cette commande :
```text
AT!CUSTOM="GPSENABLE"
```

### 3. Surchauffe
Le module est enfermé dans un boîtier extérieur non climatisé ? Vérifiez s'il a de la fièvre :
```text
AT!PCTEMP
```
- **EM7455 / MC7455** : limite interne 93 °C
- **EM7565** : limite interne 90 °C
- **EM919x (5G)** : limite interne 115 °C

Au-dessus de la température de fonctionnement recommandée, le module réduit lui-même sa vitesse, voire coupe la connexion pour se protéger. Ajoutez un dissipateur !

---

## Conclusion

Quand un module 4G/5G refuse de travailler, ne vous jetez pas à l'aveugle sur le flash de firmware ! Prenez cette carte et descendez couche par couche : **alimentation/matériel → pilotes/interface → réglages SIM et APN → refroidissement et antennes**. Tous les problèmes finiront par se montrer.

## Informations d'achat (Call to Action)

Votre projet est bloqué sur des problèmes de connexion ? Vous cherchez des modules Sierra Wireless fiables avec un support technique ? Yupitek (Yughe Technology) fournit des solutions matérielles complètes et un support de première ligne pour vous sortir de l'enfer du dépannage.
Écrivez-nous : **sales@yupitek.com**
Voir les produits : [Section des modules Sierra Wireless](https://yupitek.com/fr/products/sierra/)

---

## Questions fréquentes

{{< faq >}}
