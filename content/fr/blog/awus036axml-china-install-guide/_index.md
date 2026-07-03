---
title: "Guide d'installation du pilote ALFA AWUS036AXML pour la Chine : Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Guide étape par étape pour installer les pilotes ALFA AWUS036AXML en Chine en utilisant des miroirs domestiques. Pilote MT7921AUN WiFi 6E dans le noyau, support complet du mode moniteur et VIF. Couvre Kali Linux, Ubuntu 22/24, Debian et Raspberry Pi. Aucun GitHub requis."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axml-china-install-guide"
tags: ["alfa", "awus036axml", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6e", "vif"]
categories: ["Guides de Pilotes"]
series: ["alfa-china-install-guide"]
series_order: 7
related_product: "/fr/products/alfa/awus036axml/"
featureimage: "/images/blog/awus036axml-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Quel chipset utilise l'AWUS036AXML ? Est-ce le même que l'AWUS036AXM ?"
    answer: "Il utilise également le chipset MediaTek MT7921AUN, mais l'AWUS036AXML est la version phare avec interface USB-C."
  - question: "Le pilote de l'AWUS036AXML nécessite-t-il une installation manuelle ?"
    answer: "Non, le pilote mt7921u est intégré au noyau Linux depuis 5.18. Seul le paquet de firmware est à installer."
  - question: "L'AWUS036AXML supporte-t-il les interfaces virtuelles VIF ?"
    answer: "Oui, le MT7921AUN supporte pleinement le VIF natif du noyau, permettant d'exécuter simultanément une interface moniteur et une interface managed."
  - question: "Pourquoi le pilote de l'AWUS036AXML échoue-t-il sur Ubuntu 22.04 ?"
    answer: "Le noyau par défaut d'Ubuntu 22.04 (5.15) est trop ancien. Installez le noyau HWE pour passer à 5.18 ou supérieur."
  - question: "Quel est l'USB ID de l'AWUS036AXML ?"
    answer: "L'USB ID du MediaTek MT7921AUN est 0e8d:7961, vérifiable avec lsusb."
---

{{< tldr >}}
L'AWUS036AXML utilise le chipset MT7921AUN, carte phare WiFi 6E tri-bande USB-C. Le pilote est intégré au noyau. Après installation du firmware, le mode moniteur, l'injection de paquets et le VIF sont disponibles.
{{< /tldr >}}

L'AWUS036AXML est le fleuron WiFi 6E d'ALFA — un adaptateur USB-C tri-bande couvrant les bandes 2,4 GHz, 5 GHz et la bande 6 GHz non encombrée. Sa puce MT7921AUN utilise le pilote `mt7921u`, intégré au noyau Linux depuis la version 5.18. Sur Ubuntu 24.04 et Kali 2025, il est plug-and-play une fois que le package de micrologiciel est installé à partir d'un miroir domestique. Ce guide couvre la configuration complète — micrologiciel, vérification du pilote, mode moniteur, injection de paquets et VIF — sans toucher à GitHub.

## Avant de commencer

Assurez-vous d'avoir ces éléments prêts :

1. Adaptateur **ALFA AWUS036AXML** et câble USB-C
2. Un concentrateur USB alimenté — requis si vous êtes sur Raspberry Pi
3. Connexion Internet active pour accéder aux miroirs domestiques

Branchez l'adaptateur, puis confirmez que votre système le voit :

```bash
lsusb
```

Recherchez ceci dans la sortie :

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

Si vous voyez `0e8d:7961`, l'adaptateur est détecté. Passez à la section de votre système d'exploitation ci-dessous.

## Choisissez votre système d'exploitation

Passez à la section correspondant à votre OS :

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

Le pilote MT7921AUN est déjà dans le noyau Kali. Tout ce dont vous avez besoin est le package de micrologiciel MediaTek, disponible sur les miroirs domestiques.

### Étape 1 : Passer au miroir chinois

Ouvrez votre liste de sources dans le terminal.

```bash
sudo nano /etc/apt/sources.list
```

Supprimez tout ce qui s'y trouve, puis collez cette ligne :

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Sauvegardez : appuyez sur **Ctrl+O**, puis Entrée, puis Ctrl+X pour quitter. Actualisez l'index des paquets.

```bash
sudo apt update
```

---

### Étape 2 : Installer le micrologiciel

Le MT7921AUN nécessite des fichiers de micrologiciel provenant de `firmware-misc-nonfree` et `linux-firmware`.

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### Étape 3 : Vérifier le pilote

Après le redémarrage, branchez l'adaptateur et vérifiez.

```bash
lsmod | grep mt7921
```

Vous devriez voir `mt7921u` dans la sortie. Confirmez ensuite qu'une interface sans fil est apparue.

```bash
iwconfig
```

Recherchez `wlan0` ou `wlan1`.

---

### Étape 4 : Activer le mode moniteur {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

Recherchez `Mode:Monitor` sur l'interface.

---

### Étape 5 : Tester l'injection de paquets {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

Un résultat réussi affichera : `Injection is working!`.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — noyau 6.8, plug-and-play

Ubuntu 24.04 inclut le pilote nativement.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Passez aux miroirs Aliyun :
`URIs: http://mirrors.aliyun.com/ubuntu/`

```bash
sudo apt update
sudo apt install -y linux-firmware
sudo reboot
```

---

## Debian

Passez au miroir Tsinghua :

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

---

## Dépannage

| Problème | Cause probable | Solution |
|---------|-------------|-----|
| `lsusb` n'affiche pas 0e8d:7961 | Manque d'alimentation | Essayer un autre port ou concentrateur alimenté |

## Référence des miroirs chinois

| Ressource | URL | Utilisation pour |
|----------|-----|---------|
| Pilotes officiels Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Packs de pilotes |
| Miroir Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |

{{< faq >}}

## Plus de guides d'installation d'adaptateurs Alfa pour la Chine

- [AWUS036ACH China Install Guide](/fr/blog/awus036ach-china-install-guide/) — RTL8812AU, haute puissance
- AWUS036AXML ← vous êtes ici

Des questions ? Laissez un commentaire ci-dessous ou contactez-nous sur [yupitek.com](https://yupitek.com/fr/contact/).

---

## Références
1. [Pilote mt7921 du noyau Linux](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [Documentation officielle aircrack-ng](https://www.aircrack-ng.org/)
3. [Site officiel ALFA Network](https://www.alfa.com.tw/)
4. [Documentation officielle Kali Linux](https://www.kali.org/docs/)
