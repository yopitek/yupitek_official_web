---
title: "Guide d'installation du pilote ALFA AWUS036AXER pour la Chine : Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Guide étape par étape pour installer les pilotes ALFA AWUS036AXER en Chine en utilisant des miroirs domestiques. Pilote RTL8832BU, adaptateur WiFi 6 nano. Couvre Kali Linux, Ubuntu 22/24, Debian et Raspberry Pi. Aucun GitHub requis."
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
---

L'AWUS036AXER est l'adaptateur WiFi 6 nano d'ALFA — un dongle compact conçu pour rester branché en permanence sur un ordinateur portable. Sa puce RTL8832BU est hors noyau sur les versions Linux inférieures à 6.14 mais est incluse nativement dans Ubuntu 24.04 (noyau 6.8). Ce guide utilise des miroirs Gitee pour les noyaux plus anciens. Aucun GitHub requis.

> **Note sur la recherche en sécurité :** Le RTL8832BU a un support limité du mode moniteur. Les résultats varient selon le noyau et la version du pilote. Pour une injection de paquets fiable sur Kali Linux, l'[AWUS036ACM](/fr/blog/awus036acm-china-install-guide/) ou l'[AWUS036ACH](/fr/blog/awus036ach-china-install-guide/) sont de meilleurs choix.

> **Note sur la portée :** L'AWUS036AXER possède une antenne intégrée non amovible. Pour la recherche en sécurité, les adaptateurs avec antennes externes RP-SMA (AWUS036ACH, AWUS036ACM) offrent une portée nettement meilleure.

## Avant de commencer

1. Adaptateur **ALFA AWUS036AXER**
2. Câble USB-A
3. Connexion Internet active pour accéder aux miroirs domestiques

```bash
lsusb
```

Recherchez ceci dans la sortie :

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

### Étape 3 : Cloner le pilote depuis Gitee

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

---

### Étape 4 : Compiler et installer

```bash
sudo ./install-driver.sh
sudo reboot
```

Vérifiez que le pilote est chargé :

```bash
lsmod | grep 88x2bu
iwconfig
```

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — pilote dans le noyau, pas besoin de Gitee

Ubuntu 24.04 utilise le noyau 6.8, qui inclut nativement le pilote RTL8832BU.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Remplacez les URIs par le miroir Aliyun :
`URIs: http://mirrors.aliyun.com/ubuntu/`

```bash
sudo apt update
sudo modprobe 88x2bu
iwconfig
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
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
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
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Passthrough USB pour machine virtuelle {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Paramètres → USB** → Activer le **Contrôleur USB 3.0 (xHCI)**.
2. Ajouter un filtre : **Realtek** (ID : 0bda:885a).
3. Démarrer la VM → `lsusb` pour confirmer.

### VMware

1. **Machine virtuelle → USB & Bluetooth** → Trouver **Realtek RTL8832BU** → **Connecter**.

---

## Dépannage

| Problème | Cause probable | Solution |
|---------|-------------|-----|
| `lsusb` n'affiche pas 0bda:885a | Adaptateur non détecté | Essayer un autre port USB |
| `install-driver.sh` échoue | En-têtes manquants | `sudo apt install linux-headers-$(uname -r)` |
| Mode moniteur non fiable | Limitation du RTL8832BU | Utiliser l'AWUS036ACM pour le pentest |

## Référence des miroirs chinois

| Ressource | URL | Utilisation pour |
|----------|-----|---------|
| Pilotes officiels Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Packs de pilotes |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | Pilote RTL8832BU |
| Miroir Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |

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
