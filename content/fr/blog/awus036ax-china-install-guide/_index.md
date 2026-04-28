---
title: "Guide d'installation du pilote ALFA AWUS036AX pour la Chine : Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Guide étape par étape pour installer les pilotes ALFA AWUS036AX en Chine en utilisant des miroirs domestiques. Pilote RTL8832BU, WiFi 6 AX1800. Couvre Kali Linux, Ubuntu 22/24 (intégré sur 24.04), Debian et Raspberry Pi. Aucun GitHub requis."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["Alfa China Install Guide"]
related_product: "/fr/products/alfa/awus036ax/"
---

L'AWUS036AX est l'adaptateur double bande WiFi 6 AX1800 d'ALFA. Sa puce RTL8832BU est hors noyau sur les versions de Linux inférieures à 6.14 — mais Ubuntu 24.04 (noyau 6.8) l'inclut nativement. Ce guide utilise des miroirs Gitee pour les noyaux plus anciens et le pilote intégré pour Ubuntu 24.04. Aucun GitHub requis.

> **Note sur la recherche en sécurité :** Le RTL8832BU a un support limité du mode moniteur. Les résultats varient selon la version du noyau et du pilote. Pour une injection de paquets fiable sur Kali Linux, l'[AWUS036ACM](/fr/blog/awus036acm-china-install-guide/) ou l'[AWUS036ACH](/fr/blog/awus036ach-china-install-guide/) sont de meilleurs choix.

## Avant de commencer

1. Adaptateur **ALFA AWUS036AX**
2. Câble USB-A
3. Connexion internet active

```bash
lsusb
```

Cherchez :

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

### Étape 1 : Passer au miroir de Chine

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Étape 2 : Installer les dépendances de compilation

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

### Étape 3 : Cloner le pilote depuis Gitee

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

> **NOTE :** Si cette URL Gitee ne se charge pas, recherchez `rtl8852bu` sur Gitee et choisissez le fork le plus récemment mis à jour. Vous pouvez également télécharger des archives sur [files.alfa.com.tw](https://files.alfa.com.tw).

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

### Étape 5 : Activer le mode moniteur {#enable-monitor-mode}

> **Note :** Le support du mode moniteur est limité sur le RTL8832BU. Les commandes suivantes fonctionnent sur la plupart des configurations mais les résultats peuvent varier.

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### Étape 6 : Tester l'injection de paquets {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

Si l'injection n'est pas fiable, envisagez l'[AWUS036ACM](/fr/blog/awus036acm-china-install-guide/) pour les travaux de test d'intrusion.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — pilote dans le noyau, pas besoin de Gitee

Ubuntu 24.04 est livré avec le noyau 6.8, qui inclut nativement le pilote RTL8832BU.

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
sudo modprobe 88x2bu
iwconfig
```

Si le module se charge et qu'une interface apparaît, vous avez terminé. Passez aux étapes du mode moniteur ci-dessus.

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
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

Activez le mode moniteur de la même manière que pour Kali ci-dessus.

---

## Raspberry Pi 4B / 5

Passez d'abord au miroir de Chine :

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

## Redirection USB vers machine virtuelle {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Configuration → USB** → Activer le **contrôleur USB 3.0 (xHCI)**.
2. Ajouter un filtre : **Realtek** (ID: 0bda:885a).
3. Démarrer la VM → `lsusb` pour confirmer → suivre les étapes Kali.

### VMware

1. **Machine virtuelle → USB et Bluetooth** → Trouver **Realtek RTL8832BU** → **Connecter**.
2. `lsusb` pour confirmer → suivre les étapes Kali.

---

## Dépannage

| Problème | Cause probable | Solution |
|----------|----------------|----------|
| `lsusb` n'affiche pas 0bda:885a | Adaptateur non détecté | Essayer un autre port USB |
| `install-driver.sh` échoue | En-têtes manquants | `sudo apt install linux-headers-$(uname -r)` |
| Le clonage Gitee échoue | Problème de réseau | Rechercher `rtl8852bu` sur gitee.com |
| Ubuntu 24.04 : `modprobe 88x2bu` échoue | Module non présent | Installer `linux-modules-extra-$(uname -r)` |
| Mode moniteur peu fiable | Limitation du RTL8832BU | Utiliser l'AWUS036ACM pour les tests d'intrusion |

> **Note sur le VIF :** Le pilote hors noyau RTL8832BU ne prend pas en charge les interfaces virtuelles (VIF).

## Référence des miroirs en Chine

| Ressource | URL | Utilisation |
|-----------|-----|-------------|
| Pilotes officiels Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquets de pilotes |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | Pilote RTL8832BU |
| Miroir de l'Université Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Miroir Alibaba Cloud | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| Miroir USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| Miroir Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

## Plus de guides d'adaptateurs Alfa pour la Chine

- [Guide d'installation AWUS036ACH Chine](/fr/blog/awus036ach-china-install-guide/) — RTL8812AU, haute puissance
- [Guide d'installation AWUS036ACM Chine](/fr/blog/awus036acm-china-install-guide/) — MT7612U, VIF complet
- [Guide d'installation AWUS036ACS Chine](/fr/blog/awus036acs-china-install-guide/) — RTL8811AU, mode moniteur
- AWUS036AX ← vous êtes ici
- [Guide d'installation AWUS036AXER Chine](/fr/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [Guide d'installation AWUS036AXM Chine](/fr/blog/awus036axm-china-install-guide/) — MT7921AUN, forme en L
- [Guide d'installation AWUS036AXML Chine](/fr/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [Guide d'installation AWUS036EACS Chine](/fr/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Des questions ? Laissez un commentaire ci-dessous ou contactez-nous sur [yupitek.com](https://yupitek.com/fr/contact/).
