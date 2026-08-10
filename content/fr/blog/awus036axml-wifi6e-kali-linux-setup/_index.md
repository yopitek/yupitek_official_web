---
title: "Tutoriel d'installation ALFA AWUS036AXML : test pratique du Monitor Mode et de la Packet Injection Wi-Fi 6E sur Kali Linux"
locale: "fr"
hreflang_group: "awus036axml-wifi6e-kali-linux-setup"
description: "Tutoriel d'installation de l'ALFA AWUS036AXML (puce MT7921AUN) sur Kali Linux : pilote mt7921u intégré, prérequis de version de kernel, Monitor Mode, Packet Injection et dépannage."
date: 2026-08-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axml-wifi6e-kali-linux-setup"
tags: ["Test de Monitor Mode et de Packet Injection Wi-Fi 6E sur Kali Linux", "FR", "wifi6e-kali-linux-setup", "AWUS036AXML", "Kali Linux", "Tutoriel Monitor Mode et Packet Injection Wi-Fi 6E | Yupitek"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-08-10
---


# Tutoriel d'installation ALFA AWUS036AXML : test pratique du Monitor Mode et de la Packet Injection Wi-Fi 6E sur Kali Linux

> En bref : l'ALFA AWUS036AXML embarque une puce MediaTek MT7921AUN. Sous Kali Linux (kernel 5.18+), elle **fonctionne directement avec le pilote intégré `mt7921u`**, tu n'as pas besoin de compiler un autre pilote. Si tu veux un active monitor mode stable ou faire de la Packet Injection, nous te conseillons d'utiliser un kernel 6.12+ ainsi qu'un hub USB alimenté. Après branchement, la commande `lsusb` doit afficher `0e8d:7961`. Il te suffit ensuite d'utiliser `airmon-ng` ou `iw` pour passer en Monitor Mode.

## Pourquoi s'intéresser aux cartes Wi-Fi 6E pour le pentest ?

La nouvelle bande **6 GHz** (5925–7125 MHz) du Wi-Fi 6E est au cœur de la modernisation des réseaux d'entreprise : points d'accès de nouvelle génération, salles de conférence à haute densité et IoT industriel adoptent désormais cette fréquence. Si tu réalises des audits de sécurité et que ta cible utilise du 6 GHz, ta carte réseau de test **doit absolument pouvoir écouter cette bande**, sous peine de rater une grande partie du périmètre d'audit.

L'AWUS036AXML est une carte USB Wi-Fi 6E conçue par ALFA Network. Elle gère trois bandes (2.4, 5 et 6 GHz). Par rapport à l'ancienne AWUS036ACH (puce RTL8812AU, limitée au 2.4 et 5 GHz), sa force est d'ajouter l'écoute en 6 GHz. Si tu connais déjà le fonctionnement de l'AWUS036ACH, les étapes présentées ici te seront très familières.

## Spécifications et prérequis pour l'AWUS036AXML

| Caractéristique | AWUS036AXML | AWUS036ACH (comparatif) | AWUS036ACM (comparatif) |
|---|---|---|---|
| Chipset | MediaTek MT7921AUN | Realtek RTL8812AU | MediaTek MT7612U |
| Bandes | 2.4 / 5 / 6 GHz (Wi-Fi 6E) | 2.4 / 5 GHz | 2.4 / 5 GHz |
| Pilote Linux | `mt7921u` (**intégré au kernel**) | `88XXau` (compilation ou DKMS nécessaire) | `mt76` (intégré au kernel) |
| Kernel recommandé | ≥ 5.18 (support du 6 GHz) | 5.x (versions plus anciennes acceptées) | 5.x |
| Active monitor mode | Conseillé avec kernel ≥ 6.12 | Standard | Standard |
| ID USB (lsusb) | `0e8d:7961` | `0bda:8812` | `0e8d:7612` |
| Consommation | Environ 2,7 W (hub alimenté conseillé) | Plus faible | Plus faible |
| Packet Injection | Supportée (test recommandé) | Supportée | Supportée |

> Note sur le kernel : le pilote `mt7921u` fait partie de la branche principale depuis le kernel 5.18, et le support de la bande 6 GHz s'est amélioré au fil des versions. Nous conseillons un kernel 6.12+ pour un active monitor mode stable. La version de Kali Linux 2026 utilise par défaut un kernel 6.14 ou supérieur, ce qui remplit parfaitement cette condition.

## Prérequis

1. **Kali Linux 2024.x ou version ultérieure** (pense à mettre ton système à jour : `sudo apt update && sudo apt full-upgrade -y`).
2. Vérifier la version du kernel avec `uname -r`. Si elle est inférieure à 5.18, mets à jour ton système.
3. Un port USB 3.0 disponible. Si tu te branches sur un Raspberry Pi ou un hub USB, **utilise de préférence un hub avec alimentation externe**. L'AWUS036AXML consomme environ 2,7 W, et un manque de puissance peut empêcher la carte d'être détectée.
4. Autorisation légale : toutes les commandes de ce tutoriel doivent uniquement servir sur des réseaux qui t'appartiennent ou pour lesquels tu as obtenu un accord explicite.

## Étape 1 : brancher la carte et vérifier sa détection

Branche ta carte, puis utilise `lsusb` pour vérifier si le système l'identifie bien :

```bash
lsusb
```

Tu devrais voir une ligne similaire à celle-ci :

```text
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

`0e8d:7961` correspond à l'identifiant USB du chipset MT7921AUN. Si la ligne n'apparaît pas, vérifie d'abord l'alimentation en changeant de port USB ou en ajoutant un hub alimenté.

Vérifie ensuite que le pilote est bien chargé :

```bash
lsmod | grep mt7921
dmesg | grep -i mt7921 | tail -20
```

Le kernel par défaut de Kali Linux 2026 intègre déjà le pilote `mt7921u`. La carte fonctionne dès son branchement, sans avoir à compiler ou télécharger de pilote externe. C'est la grande différence par rapport à l'AWUS036ACH, pour laquelle tu devais installer manuellement le pilote `88XXau`.

## Étape 2 : identifier l'interface réseau sans fil

```bash
ip link show
# ou
iwconfig
```

Tu devrais voir une nouvelle interface sans fil, souvent nommée `wlan0` ou `wlan1` selon la configuration de ta machine. Dans la suite de ce guide, nous utiliserons `wlan1` à titre d'exemple, remplace-le par le nom de ta propre interface.

## Étape 3 : activer le Monitor Mode

### Méthode 1 : airmon-ng (recommandée)

```bash
# Terminer les processus susceptibles de causer des interférences
sudo airmon-ng check kill

# Activer le Monitor Mode (remplace wlan1 par le nom de ton interface)
sudo airmon-ng start wlan1
```

Une fois l'opération réussie, l'interface virtuelle `wlan1mon` sera créée.

### Méthode 2 : iw (contrôle direct)

```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

Cette méthode modifie directement l'interface existante sans générer de nouvelle interface `wlan1mon`.

## Étape 4 : confirmer l'activation du Monitor Mode

```bash
iwconfig
```

La ligne correspondante doit afficher `Mode:Monitor` :

```text
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.412 GHz  Tx-Power=30 dBm
          Power Management:off
```

Tu peux également taper `iw dev` pour t'assurer que le mode est bien configuré sur `monitor`. Lance ensuite un test avec `airodump-ng` :

```bash
sudo airodump-ng wlan1mon
```

Si les réseaux Wi-Fi environnants s'affichent avec leurs canaux, puissances et types de sécurité, le Monitor Mode fonctionne correctement. Pour scanner sur la bande 6 GHz :

```bash
sudo airodump-ng --band 6g wlan1mon
```

> Attention : le scan en 6 GHz nécessite que le pilote et le kernel de ton système supportent cette fréquence, le kernel 6.12+ offrant une meilleure stabilité. Si l'option `--band 6g` n'est pas reconnue, teste d'abord les fréquences 5 GHz avec `--band a` pour t'assurer du bon fonctionnement général, puis mets à jour ton kernel.

## Étape 5 : tester la Packet Injection

```bash
sudo aireplay-ng --test wlan1mon
```

Tu devrais obtenir une réponse indiquant :

```text
Injection is working!
```

Un taux de réussite supérieur à 80 % indique que le matériel est fiable. Si le taux tombe sous les 50 %, ajuste l'orientation des antennes, vérifie l'alimentation USB ou privilégie un branchement direct sur un port USB 3.0.

## Cas particulier du Raspberry Pi : créer une plateforme d'audit portable

L'AWUS036AXML est officiellement compatible avec les Raspberry Pi 3B+, 4 et 5, ce qui en fait un excellent choix pour monter un kit d'audit réseau portable. Voici quelques points importants à garder en tête :

- **Alimentation** : les ports USB du Raspberry Pi délivrent un courant parfois trop faible. Nous te conseillons d'utiliser un hub USB alimenté en externe pour éviter les déconnexions aléatoires.
- **Système** : l'image officielle Kali ARM64 pour Raspberry Pi convient très bien, elle intègre aussi le pilote `mt7921u` nativement.
- **Validation** : dès que `lsusb` affiche `0e8d:7961` et que `lsmod | grep mt7921` renvoie un résultat, ton outil est prêt.

## Dépannage fréquent

**Q : Que faire si `lsusb` n'affiche pas `0e8d:7961` ?**
Dans la quasi-totalité des cas, le problème vient d'une alimentation trop faible ou d'un mauvais contact. Branche la carte sur un autre port USB 3.0 en direct. Si tu passes par un hub, choisis un modèle alimenté en externe. Tu peux aussi tenter de changer de câble USB pour un modèle plus court.

**Q : Pourquoi l'interface repasse-t-elle en mode Managed juste après avoir activé le Monitor Mode ?**
NetworkManager ou wpa_supplicant reprennent généralement le contrôle en tâche de fond. Lance la commande `sudo airmon-ng check kill` pour couper les processus gênants, ou arrête-les manuellement avec `sudo systemctl stop NetworkManager wpa_supplicant`.

**Q : Pourquoi `iwconfig` indique-t-il `Mode:Managed` ou pourquoi l'interface a-t-elle disparu ?**
Le pilote n'a peut-être pas été chargé correctement, ou ton kernel est trop vieux. Vérifie la présence du module avec `lsmod | grep mt7921`, puis vérifie que ton kernel est bien supérieur ou égal à la version 5.18 via la commande `uname -r`.

**Q : Je ne trouve aucun réseau en 6 GHz, est-ce normal ?**
Vérifie d'abord les fréquences gérées via `iw dev wlan1mon info`. Les déploiements en 6 GHz restent encore rares. Pour la France et les autres pays, assure-toi de la réglementation locale sur ces fréquences. Tu peux commencer par tester les bandes 2.4 et 5 GHz afin de valider le bon fonctionnement de la carte.

**Q : Quelle carte choisir entre l'AWUS036AXML et l'AWUS036ACH ?**
Si ta cible possède déjà une infrastructure en 6 GHz, opte pour l'AWUS036AXML. Si tu n'as besoin que des fréquences 2.4 et 5 GHz et que tu as un budget serré, l'AWUS036ACH reste un choix très mûr. Les deux cartes fonctionnent très bien sous Kali Linux, la différence réside dans la couverture des bandes de fréquences et la méthode d'installation du pilote (l'AXML a un pilote intégré et ne nécessite pas de compilation).

## Foire Aux Questions (FAQ)

**Q1 : Faut-il installer un pilote externe pour l'ALFA AWUS036AXML sous Kali Linux ?**
Non. Elle utilise le pilote `mt7921u` directement intégré au kernel (version 5.18+). Il suffit de la brancher pour l'utiliser, contrairement à l'AWUS036ACH qui requiert l'installation d'un pilote DKMS.

**Q2 : L'AWUS036AXML gère-t-elle le Monitor Mode ?**
Oui. Tu peux l'activer simplement avec `airmon-ng` ou `iw`. Pour l'utilisation de l'active monitor mode (comme les tests de désauthentification), nous recommandons un kernel 6.12+.

**Q3 : La bande 6 GHz du Wi-Fi 6E peut-elle être testée librement ?**
La bande 6 GHz est réglementée. Avant de lancer tes tests, informe-toi sur les décisions des autorités locales concernant cette fréquence et limite tes audits aux réseaux sur lesquels tu disposes d'une autorisation explicite.

**Q4 : Que faire si le Raspberry Pi ne détecte pas ma carte ?**
Contrôle l'alimentation en priorité. L'AWUS036AXML consomme environ 2,7 W. Utilise un hub USB alimenté en externe et opte pour un câble USB de bonne qualité.

**Q5 : Quelles sont les différences entre l'AWUS036AXML et l'AWUS036ACH ?**
L'AXML supporte le Wi-Fi 6E (avec la bande 6 GHz en plus) et intègre son pilote nativement dans le kernel. L'ACH est double bande (2.4 et 5 GHz) et nécessite l'installation manuelle du pilote pour la puce RTL8812AU. Les deux modèles restent d'excellents choix pour l'audit sous Kali Linux.

## Conclusion

L'installation de l'AWUS036AXML est bien plus simple qu'il n'y paraît : **un kernel 5.18+, un branchement direct utilisant le pilote intégré `mt7921u`, la vérification de l'ID `0e8d:7961`, le passage en Monitor Mode via airmon-ng, puis la validation de l'injection avec aireplay-ng**. La grande différence avec l'AWUS036ACH tient à la bande 6 GHz et à l'absence de compilation pour le pilote. Si ton périmètre d'audit englobe désormais le Wi-Fi 6E, cette carte représente une solution idéale pour compléter ta couverture de fréquences. N'oublie pas de mener tes tests uniquement sur des réseaux autorisés.

La gamme de cartes ALFA Network bénéficie du support technique et commercial de Yupitek. Si tu as besoin d'une AWUS036AXML, d'un hub USB alimenté ou d'antennes adaptées, n'hésite pas à nous contacter à l'adresse [sales@yupitek.com](mailto:sales@yupitek.com).
