---
title: "Guide d'installation du pilote ALFA AWUS036AXER pour la Chine : Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Guide étape par étape pour installer les pilotes ALFA AWUS036AXER en Chine en utilisant des miroirs domestiques. Pilote RTL8832BU, adaptateur WiFi 6 nano. Couvre Kali Linux, Ubuntu 22/24, Debian et Raspberry Pi."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axer-china-install-guide"
tags: ["alfa", "awus036axer", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Guides de Pilotes"]
series: ["alfa-china-install-guide"]
series_order: 5
related_product: "/fr/products/alfa/awus036axer/"
featureimage: "/images/blog/awus036axer-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Quel chipset utilise l'AWUS036AXER ? Est-ce le même que l'AWUS036AX ?"
    answer: "Il utilise également le chipset Realtek RTL8832BU supportant le WiFi 6, mais dans un format plus compact et portable."
  - question: "L'AWUS036AXER nécessite-t-il un pilote sur Ubuntu 24.04 ?"
    answer: "Oui. Le RTL8832BU n'est pas dans le noyau d'Ubuntu 24.04. Compilez une fois le pilote communautaire rtl8852bu (morrownr/rtl8852bu-20250826) via DKMS ; il est ensuite recompilé automatiquement à chaque mise à jour du noyau."
  - question: "L'AWUS036AXER convient-il à la recherche en sécurité sans fil ?"
    answer: "Non. Le pilote communautaire rtl8852bu ne prend en charge ni le mode moniteur ni l'injection de paquets. Utilisez plutôt un adaptateur avec pilote MediaTek intégré au noyau, comme l'AWUS036ACM."
  - question: "Quel est l'USB ID de l'AWUS036AXER ?"
    answer: "L'ID fabricant du Realtek RTL8832BU est 0bda. L'ID produit est 8832 ou 885a selon l'unité ; vérifiez-le avec lsusb."
  - question: "Faut-il un VPN pour installer l'AWUS036AXER en Chine ?"
    answer: "Pas nécessairement. Clonez le pilote depuis le dépôt GitHub vérifié (morrownr/rtl8852bu-20250826) ; si GitHub est lent, utilisez un proxy ou un miroir de confiance. Les outils de compilation peuvent toujours être installés depuis des miroirs nationaux."
---

{{< tldr >}}
L'AWUS036AXER utilise le chipset RTL8832BU avec WiFi 6. Le pilote n'est pas dans le noyau : toutes les distributions (y compris Ubuntu 24.04) doivent compiler rtl8852bu via DKMS. Le mode moniteur n'est pas pris en charge.
{{< /tldr >}}

L'AWUS036AXER est l'adaptateur WiFi 6 nano d'ALFA — un dongle compact conçu pour rester branché en permanence sur un ordinateur portable. La puce RTL8832BU de l'AWUS036AXER n'a pas de pilote intégré au noyau Linux : sur toutes les distributions (y compris Ubuntu 24.04), il faut compiler une fois le pilote communautaire rtl8852bu via DKMS. Le code source du pilote est cloné depuis le dépôt GitHub vérifié ; si GitHub est lent, utilisez un proxy ou un miroir de confiance. Ce pilote ne prend pas en charge le mode moniteur.

> **Remarque sur la recherche en sécurité:** Le pilote communautaire rtl8852bu ne prend en charge ni le mode moniteur ni l'injection de paquets. Pour la recherche en sécurité, utilisez un adaptateur avec pilote MediaTek intégré au noyau, comme l'[AWUS036ACM](/fr/blog/awus036acm-china-install-guide/).

> **Note sur la portée :** L'AWUS036AXER possède une antenne intégrée non amovible. Pour la recherche en sécurité, les adaptateurs avec antennes externes RP-SMA (AWUS036ACH, AWUS036ACM) offrent une portée nettement meilleure.

## Avant de commencer

1. Adaptateur **ALFA AWUS036AXER**
2. Câble USB-A
3. Connexion Internet active pour accéder aux miroirs domestiques

```bash
lsusb
```

Cherchez une ligne comme celle-ci (exemple de sortie ; l'ID fabricant est toujours `0bda`, et l'ID produit est `8832` ou `885a` selon l'unité) :

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## Choisissez votre système d'exploitation

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

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

### Étape 2 : Installer les dépendances de construction

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### Étape 3 : Cloner le pilote depuis GitHub

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
```

> **NOTE :** Le pilote amont maintenu est [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826). Si GitHub est lent, utilisez un proxy ou un miroir de confiance. Vous pouvez également télécharger des archives sur [files.alfa.com.tw](https://files.alfa.com.tw).

---

### Étape 4 : Compiler et installer

```bash
sudo ./install-driver.sh
sudo reboot
```

Vérifiez que le pilote est chargé :

```bash
lsmod | grep 8852bu
iwconfig
```

### Étape 5 : Activer le mode moniteur {#enable-monitor-mode}

> **Non pris en charge :** Le pilote communautaire rtl8852bu du RTL8832BU ne prend pas en charge le mode moniteur, il n'y a donc aucune commande à exécuter ici. Si vous avez besoin du mode moniteur, utilisez un adaptateur avec pilote MediaTek intégré au noyau, comme l'[AWUS036ACM](/fr/blog/awus036acm-china-install-guide/).

### Étape 6 : Tester l'injection de paquets {#test-packet-injection}

> **Non pris en charge :** L'injection de paquets dépend du mode moniteur, que ce pilote ne fournit pas. Utilisez l'[AWUS036ACM](/fr/blog/awus036acm-china-install-guide/) pour les tests d'injection.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — DKMS requis

Ubuntu 24.04 (noyau 6.8) n'inclut pas de pilote pour le RTL8832BU. Passez à un miroir domestique, puis compilez le pilote comme pour Ubuntu 22.04 ci-dessous.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

Après le redémarrage, exécutez `sudo modprobe 8852bu` et `iwconfig`. Si le module se charge et qu'une interface apparaît, c'est terminé (mode géré uniquement ; le mode moniteur n'est pas pris en charge).

---

### Ubuntu 22.04 (Jammy) — DKMS requis

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

Collez ceci (Debian 12 Bookworm) :

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Raspberry Pi 4B / 5

Passez d'abord au miroir chinois :

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Passthrough USB pour machine virtuelle {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Paramètres → USB** → Activer le **Contrôleur USB 3.0 (xHCI)**.
2. Ajouter un filtre : **Realtek** (ID fabricant : 0bda, ID produit : 8832 ou 885a).
3. Démarrer la VM → `lsusb` pour confirmer.

### VMware

1. **Machine virtuelle → USB & Bluetooth** → Trouver **Realtek RTL8832BU** → **Connecter**.

---

## Dépannage

| Problème | Cause probable | Solution |
|---------|-------------|-----|
| `lsusb` n'affiche pas 0bda:8832 ou 0bda:885a | Adaptateur non détecté | Essayer un autre port USB |
| `install-driver.sh` échoue | En-têtes manquants | `sudo apt install linux-headers-$(uname -r)` |
| Mode moniteur non fiable | Limitation du RTL8832BU | Utiliser l'AWUS036ACM pour le pentest |

## Référence des miroirs chinois

| Ressource | URL | Utilisation pour |
|----------|-----|---------|
| Pilotes officiels Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Packs de pilotes |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | Pilote RTL8832BU |
| Miroir Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |

{{< faq >}}

## Plus de guides d'installation d'adaptateurs Alfa pour la Chine

- [AWUS036ACH China Install Guide](/fr/blog/awus036ach-china-install-guide/) — RTL8812AU, haute puissance
- [AWUS036ACM China Install Guide](/fr/blog/awus036acm-china-install-guide/) — MT7612U, VIF complet
- [AWUS036ACS China Install Guide](/fr/blog/awus036acs-china-install-guide/) — RTL8811AU, mode moniteur
- [AWUS036AX China Install Guide](/fr/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- AWUS036AXER ← vous êtes ici
- [AWUS036AXM China Install Guide](/fr/blog/awus036axm-china-install-guide/) — MT7921AUN, forme en L
- [AWUS036AXML China Install Guide](/fr/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS China Install Guide](/fr/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Questions ? Laissez un commentaire ci-dessous ou contactez-nous sur [yupitek.com](https://yupitek.com/fr/contact/).

---

## Références
1. [Site officiel Realtek](https://www.realtek.com/)
2. [Site officiel ALFA Network](https://www.alfa.com.tw/)
3. [Documentation officielle Kali Linux](https://www.kali.org/docs/)
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
