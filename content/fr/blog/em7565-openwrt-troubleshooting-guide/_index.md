---
title: "EM7565 non détecté sous OpenWrt ou Raspberry Pi ? Guide complet de dépannage QMI/MBIM"
description: "EM7565 non détecté sous OpenWrt ou Raspberry Pi, ou le port QMI a disparu ? Ce guide te fait passer de lsusb et dmesg à la composition USB, au chargement des pilotes et aux étapes de configuration de l'EM7565 pour résoudre les problèmes de connexion matériels et logiciels."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "em7565-openwrt-troubleshooting-guide"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/fr/products/sierra/em7565/"
faq:
  - question: "Quelle est la raison la plus courante pour laquelle l'EM7565 n'est pas détecté sous OpenWrt ?"
    answer: "La cause la plus courante est une alimentation insuffisante (VCC hors de la plage 3,135 à 4,4 V), si bien que lsusb n'affiche rien, ou un réglage de composition USB incorrect qui laisse l'interface QMI désactivée."
  - question: "L'EM7565 redémarre sans cesse et ne démarre pas. Est-il cassé ?"
    answer: "Pas forcément. Il dispose d'un mécanisme de protection SED : après 6 redémarrages anormaux consécutifs, il entre dans un état protégé, et le rechargement du firmware le restaure."
---

Ton EM7565 refuse d'apparaître sous OpenWrt ou sur un Raspberry Pi ? Avant de remplacer le module, parcours la procédure de débogage issue de la spécification officielle. Ce guide couvre la confirmation de la liaison USB matérielle, la vérification de la composition USB, le chargement des bons pilotes Linux, l'exclusion des interférences des services système et la gestion du délicat état SED du firmware. Suis ces cinq étapes pour cerner rapidement la cause racine.

{{< tldr >}}
Quand l'EM7565 n'est pas détecté, vérifie ces cinq points : 1. Confirme la couche USB avec `lsusb` (inspecte l'alimentation et la carte adaptatrice). 2. Confirme l'interface QMI/MBIM et l'existence de `/dev/cdc-wdm0` ; vérifie les pilotes `qmi_wwan` / `cdc_mbim` et la composition USB. 3. Arrête `ModemManager` pour exclure une interférence des services système. 4. Vérifie la séquence de mise sous tension (n'envoie aucun signal dans les 100 ms suivant l'allumage ; l'ondulation doit rester sous 100 mVc-c). 5. Vérifie l'état du firmware : 6 échecs de démarrage consécutifs déclenchent la protection SED, qui exige de recharger le firmware. Le principe : le matériel d'abord, puis le logiciel, le firmware en dernier.
{{< /tldr >}}

**L'EM7565 est un module WWAN M.2 de type 3042-S3-B (4G LTE-Advanced) construit sur le Qualcomm MDM9250. Il prend en charge à la fois les interfaces USB QMI et MBIM.** Quand OpenWrt ou un Raspberry Pi ne le détecte pas, le défaut se situe généralement à un de ces trois endroits : l'USB n'est pas alimenté, la composition USB est bloquée dans une mauvaise configuration, ou le pilote Linux n'a pas été chargé correctement. Parfois, le module entre aussi en mode de protection après des redémarrages répétés. En suivant le manuel officiel de Sierra Wireless, nous avons assemblé une séquence de débogage fiable, étape par étape.

> Lien produit : [Série Sierra Wireless de Yupitek](https://yupitek.com/en/products/sierra/)

## Conclusion rapide : cinq étapes quand l'EM7565 n'est pas détecté

L'erreur la plus courante pendant le débogage est de sauter directement à un reflash du firmware. **Confirme d'abord le matériel, puis le logiciel, et ne touche au firmware qu'en dernier.**

1. **Vérifie la couche USB** : lance `lsusb` pour voir si le module apparaît. Si ce n'est pas le cas, vérifie l'alimentation (VCC doit être de 3,135 à 4,4 V), la carte adaptatrice et le câble USB.
2. **Vérifie l'interface QMI/MBIM** : `lsusb` montre le module mais pas de `/dev/cdc-wdm0` ? Vérifie que les pilotes `qmi_wwan` / `cdc_mbim` sont chargés, et si la composition USB n'expose que le mode diagnostic.
3. **Vérifie les services système** : le `ModemManager` du système peut retenir le module.
4. **Vérifie la séquence de mise sous tension** : n'envoie aucun signal pendant au moins 100 ms après la mise sous tension et garde l'ondulation sous 100 mVc-c. Une tension instable provoque des déconnexions et reconnexions répétées de la liaison USB.
5. **Vérifie l'état du firmware** : si le module redémarre 6 fois de suite après des échecs de démarrage, il entre dans l'état de protection SED (Smart Error Detection), et tu dois recharger le firmware.

## Comprendre l'EM7565 : quel genre de module est-ce ?

Avant de déboguer, voici un aperçu rapide de l'EM7565. C'est un module M.2 qui exige trois antennes externes (Main, GNSS, Aux). Les antennes ne sont pas incluses.

| Élément | Spécification officielle (Doc# 41110788, Rev 8) |
|---|---|
| **Puce** | Qualcomm MDM9250 |
| **Facteur de forme** | M.2 (3042-S3-B) / 42 × 30 mm, jusqu'à 1,50 mm d'épaisseur, 6,5 g |
| **Débit descendant max** | Cat 12 (3CA, 256QAM) jusqu'à 600 Mbit/s |
| **Débit montant max** | Cat 13 (2CA, 64QAM) jusqu'à 150 Mbit/s |
| **Bandes LTE** | B1/2/3/4/5/7/8/9/12/13/18/19/20/26/28/29/30/32/41/46/66 (nota : B42/B43/B48 désactivées en attente d'approbation réglementaire) |
| **Interfaces hôte** | USB 2.0 et USB 3.0 ; commandes QMI / MBIM / AT |
| **Tension d'alimentation** | VCC 3,135 V (min) / 3,3 V (typ) / 4,4 V (max), ondulation ≤ 100 mVc-c |
| **Température de fonctionnement** | Maintiens la température interne sous 90 °C (idéalement sous 80 °C) |

## Étape 1 : commence par la couche USB

L'hôte voit-il réellement le matériel ?

```bash
lsusb
```

Si un périphérique Sierra Wireless commençant par 1199 apparaît, la liaison matérielle est établie. Si rien ne s'affiche :

- Vérifie l'alimentation : le courant d'appel de l'EM7565 au démarrage peut atteindre 2,2 à 2,5 A (courant de fonctionnement max 1,5 A). Beaucoup de boîtiers adaptateurs USB pour Raspberry Pi ne peuvent pas fournir ça.
- Laisse-lui du temps : attends 10 secondes après le branchement pour que l'énumération USB puisse se terminer.

Ensuite, inspecte le journal du noyau :

```bash
dmesg | tail -50
```

Si tu vois `qmi_wwan` créer `/dev/cdc-wdm0`, le module est prêt à se connecter.

## Étape 2 : vérifie la composition USB

Si `lsusb` montre le module mais que `/dev/cdc-wdm0` n'apparaît jamais, les canaux QMI/MBIM du module sont peut-être désactivés. Un réglage appelé USB composition, interne au module, décide des canaux qu'il expose.

Interroge-le avec la commande `AT!USBCOMP?`. Une bascule imprudente peut supprimer tous les canaux, alors note les paramètres d'origine avant de changer quoi que ce soit et consulte le manuel officiel des commandes AT (Doc#41111748).

## Étape 3 : exclure une interférence de ModemManager

Sur un Linux de bureau ou un Raspberry Pi, un service intégré appelé `ModemManager` a tendance à s'emparer du module 4G. Une fois qu'il en a pris le contrôle, tes propres commandes `qmicli` se bloquent.

Pendant un débogage manuel, arrête-le d'abord :

```bash
sudo systemctl stop ModemManager
```

Une fois que tu as confirmé que le module est sain, décide de composer manuellement ou de rendre la main à ModemManager.

## Étape 4 : le firmware est-il verrouillé ? (Protection SED)

Si le module redémarre sans fin après la mise sous tension, il a peut-être basculé dans l'état **SED (Smart Error Detection)**.

La spécification officielle est explicite : si 6 redémarrages surviennent peu après le boot, le module se gare dans le bootloader et attend un rechargement du firmware. Cela est généralement causé par une alimentation instable avec des chutes de tension sévères.

Ne présume pas que le module est mort. Passe à une meilleure alimentation et reflashe le firmware avec l'outil officiel pour le récupérer.

## Comment composer avec QMI (exemple OpenWrt)

Une fois les problèmes ci-dessus résolus et `/dev/cdc-wdm0` apparu, la connexion sous OpenWrt est simple.

1. Installe les paquets requis :

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option
```

2. Configure ton APN dans `/etc/config/network` (utilise les valeurs de ton opérateur) :

```text
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

3. Redémarre le réseau :

```bash
/etc/init.d/network restart
```

L'interface `wwan0` apparaît, et tu es en ligne.

## Résumé

Un EM7565 introuvable sous OpenWrt ou sur un Raspberry Pi, c'est comme réparer un ordinateur : respecte l'ordre et ça va vite.

1. **Matériel** : est-ce que `lsusb` est propre et la tension stable ?
2. **Interface** : la composition USB est-elle correcte ?
3. **Logiciel** : les pilotes sont-ils installés, et ModemManager se bat-il pour l'appareil ?
4. **Firmware** : trop de redémarrages ont-ils verrouillé le module ?

Tant que tu ne reflashes pas le firmware à l'aveugle, la plupart des problèmes peuvent être diagnostiqués en dix minutes.

## Informations d'achat (appel à l'action)

Tu ne sais pas si ta carte adaptatrice ou tes antennes sont compatibles avec l'EM7565 ? Yupitek fournit la gamme complète de produits Sierra Wireless et des solutions d'intégration matérielle complètes.

Écris-nous : **sales@yupitek.com**

Voir le produit : [Page produit EM7565](https://yupitek.com/en/products/sierra/em7565/)
