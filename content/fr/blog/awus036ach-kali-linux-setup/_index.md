---
title: "Guide de configuration ALFA AWUS036ACH pour Kali Linux : Mode Moniteur et Injection de Paquets (2026)"
description: "Guide étape par étape pour installer l'ALFA AWUS036ACH sur Kali Linux 2024/2025, activer le mode moniteur avec airmon-ng et vérifier l'injection de paquets — avec les commandes d'installation du pilote."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "kali-linux", "monitor-mode", "packet-injection", "RTL8812AU", "airmon-ng"]
featureimage: "/images/blog/awus036ach-kali-linux-setup.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "L'AWUS036ACH nécessite-t-il un pilote supplémentaire sur Kali Linux ?"
    answer: "Oui. Le RTL8812AU n'est pas un pilote du noyau mainline. Installez-le depuis le dépôt GitHub aircrack-ng, de préférence avec DKMS."
  - question: "Comment vérifier que l'AWUS036ACH est détecté par le système ?"
    answer: "Exécutez lsusb et cherchez l'ID 0bda:8812 pour confirmer la détection du Realtek RTL8812AU, puis lsmod pour vérifier le chargement du module."
  - question: "Que faire si l'interface disparaît après activation du mode moniteur ?"
    answer: "NetworkManager a probablement repris le contrôle de l'interface. Exécutez airmon-ng check kill pour terminer les processus interférents."
  - question: "Quel taux de réussite d'injection de paquets est normal ?"
    answer: "Un taux supérieur à 80% indique un fonctionnement fiable. En dessous de 50%, vérifiez la position de l'antenne, l'alimentation USB et le pilote."
  - question: "Comment gérer la défaillance du pilote AWUS036ACH après une mise à jour du noyau ?"
    answer: "Si installé via DKMS, le pilote se reconstruit automatiquement. En cas d'échec, exécutez dkms autoinstall et vérifiez linux-headers."
---

{{< tldr >}}
L'AWUS036ACH équipé du chipset RTL8812AU, via le pilote aircrack-ng avec DKMS, active stablement le mode moniteur et l'injection de paquets. C'est l'équipement standard du pentesting sur Kali Linux.
{{< /tldr >}}

La plupart des utilisateurs se heurtent à trois obstacles principaux lors de la configuration de l'AWUS036ACH sur Kali : le pilote ne se compile pas, la VM ne transmet pas l'appareil USB, ou le mode moniteur échoue silencieusement. Ce guide couvre les trois, plus la configuration complète à partir de zéro.

{{< alert "circle-info" >}}
Vous utilisez **VirtualBox ou VMware**? Allez directement à la section [Transfert USB](#usb-passthrough-in-virtualbox-and-vmware) — c'est l'échec de configuration le plus courant. Vous utilisez **macOS** ou **Windows** comme système hôte? Consultez les guides [ALFA sur macOS](/fr/blog/alfa-adapter-macos-vm-setup/) ou [ALFA sur Windows](/fr/blog/alfa-adapter-windows-10-11-setup/).
{{< /alert >}}

---

## Pourquoi l'AWUS036ACH est le choix privilégié

Avant de plonger dans les commandes, il est utile de comprendre ce qui rend cet appareil spécial.

**Le Puce RTL8812AU**

Le RTL8812AU de Realtek est un chipset dual-band (2,4 + 5 GHz) 802.11ac avec un support robuste pour les opérations au niveau des trames nécessaires aux outils de sécurité. Le pilote open-source maintenu sur `aircrack-ng/rtl8812au` sur GitHub est le résultat de années de collaboration entre l'équipe Aircrack-ng et la communauté de sécurité Linux. Il est activement maintenu, régulièrement testé avec les nouvelles versions de noyau, et a un support explicite pour le mode moniteur et l'injection de paquets intégré — pas comme un ajout secondaire.

**Support communautaire depuis 2017**

Lorsque vous rencontrez un problème avec l'AWUS036ACH, vous trouverez des réponses. L'appareil apparaît dans des milliers de messages de forum, tutoriels YouTube, guides Hack The Box, matériaux de cours Offensive Security et problèmes GitHub. La base de connaissances de dépannage est inégalée par tout autre appareil.

Vous pouvez le trouver dans notre boutique : [ALFA AWUS036ACH](/fr/products/alfa/awus036ach/).

---

{{< faq >}}

## Résumé

| Étape | Commande |
|---|---|
| Vérifier la détection | `lsusb \| grep Realtek` |
| Installer les dépendances | `sudo apt install git dkms build-essential linux-headers-$(uname -r)` |
| Cloner le pilote | `git clone https://github.com/aircrack-ng/rtl8812au` |
| Compiler & installer | `make && sudo make install` |
| Charger le module | `sudo modprobe 88XXau` |
| Tuer les processus gênants | `sudo airmon-ng check kill` |
| Activer le mode moniteur | `sudo airmon-ng start wlan0` |
| Vérifier le mode moniteur | `iwconfig wlan0mon` |
| Tester l'injection | `sudo aireplay-ng --test wlan0mon` |
| Temps estimé | ~15 minutes (système propre) |

Le [ALFA AWUS036ACH](/fr/products/alfa/awus036ach/) associé à Kali Linux 2024+ et au pilote aircrack-ng RTL8812AU reste l'appareil WiFi le plus fiable et le mieux documenté dans la communauté de test de pénétration.

---

## Références
1. [Dépôt GitHub du pilote aircrack-ng rtl8812au](https://github.com/aircrack-ng/rtl8812au)
2. [Documentation officielle Kali Linux](https://www.kali.org/docs/)
3. [Spécifications Realtek RTL8812AU](https://www.realtek.com/)
4. [Documentation officielle Linux Wireless](https://wireless.wiki.kernel.org/)
