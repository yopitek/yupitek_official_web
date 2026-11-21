---
title: "Guide d'installation du pilote ALFA AWUS036AX pour la Chine : Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Guide étape par étape pour installer les pilotes ALFA AWUS036AX en Chine en utilisant des miroirs domestiques. Pilote RTL8832BU, WiFi 6 AX1800. Couvre Kali Linux, Ubuntu 22/24 (DKMS), Debian et Raspberry Pi."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 4
related_product: "/fr/products/alfa/awus036ax/"
featureimage: "/images/blog/awus036ax-china-install-guide.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "Quel chipset utilise l'AWUS036AX ? Supporte-t-il le WiFi 6 ?"
    answer: "Il utilise le chipset Realtek RTL8832BU et supporte le WiFi 6 (802.11ax) haut débit."
  - question: "L'AWUS036AX nécessite-t-il un pilote sur Ubuntu 24.04 ?"
    answer: "Cela dépend de votre noyau. Le noyau Linux 6.17 et plus récent (par exemple Ubuntu 24.04 HWE / noyau 6.17) fournit le pilote intégré au noyau rtw89_8852bu — plug-and-play, sans DKMS. Ce n'est que sur les noyaux antérieurs à la 6.17 qu'il faut compiler une fois le pilote communautaire rtl8852bu (morrownr/rtl8852bu-20250826) via DKMS. Vérifiez d'abord avec uname -r."
  - question: "L'AWUS036AX convient-il à la recherche en sécurité sans fil ?"
    answer: "Oui. Avec le pilote intégré au noyau rtw89_8852bu sur le noyau 6.17+, le mode moniteur et l'injection de paquets fonctionnent tous deux dans nos tests (Ubuntu 24.04 / noyau 6.17 : injection 96 % en 2,4 GHz, et une capture WPA .22000 de bout en bout). Remarque : sur les noyaux plus anciens utilisant le pilote communautaire DKMS, la prise en charge du mode moniteur peut être limitée. Uniquement sur les réseaux que vous possédez ou que vous êtes autorisé à tester."
  - question: "Faut-il un VPN pour installer l'AWUS036AX en Chine ?"
    answer: "Pas nécessairement. Clonez le pilote depuis le dépôt GitHub vérifié (morrownr/rtl8852bu-20250826) ; si GitHub est lent, utilisez un proxy ou un miroir de confiance. Les outils de compilation peuvent toujours être installés depuis des miroirs nationaux."
  - question: "Quel est l'USB ID de l'AWUS036AX ?"
    answer: "L'ID fabricant du Realtek RTL8832BU est 0bda. L'ID produit est 8832 ou 885a selon l'unité ; vérifiez-le avec lsusb."
---

{{< tldr >}}
L'AWUS036AX utilise le chipset RTL8832BU avec prise en charge du WiFi 6. Le noyau 6.17+ (y compris Ubuntu 24.04 / noyau 6.17) dispose du pilote intégré au noyau rtw89_8852bu — sans DKMS, avec le mode moniteur et l'injection qui fonctionnent dans nos tests. Les noyaux plus anciens nécessitent le pilote communautaire rtl8852bu via DKMS.
{{< /tldr >}}

L'AWUS036AX est l'adaptateur double bande WiFi 6 AX1800 d'ALFA. Sa puce RTL8832BU est prise en charge par le **pilote intégré au noyau rtw89_8852bu sur le noyau Linux 6.17 et plus récent** (par exemple Ubuntu 24.04 HWE / noyau 6.17) — plug-and-play, sans compilation. Ce n'est que sur les **noyaux plus anciens** (antérieurs à la 6.17) qu'il faut compiler une fois le pilote communautaire rtl8852bu via DKMS. Ce guide couvre les deux cas. Le code source du pilote est cloné depuis le dépôt GitHub vérifié ; si GitHub est lent, utilisez un proxy ou un miroir de confiance.

> **Remarque sur la recherche en sécurité :** Avec le **pilote intégré au noyau rtw89_8852bu sur le noyau 6.17+**, le mode moniteur et l'injection de paquets de l'AWUS036AX fonctionnent dans nos tests (Ubuntu 24.04 / noyau 6.17 : injection 96 % en 2,4 GHz, capture WPA .22000 de bout en bout). Ce n'est que sur les noyaux plus anciens utilisant le pilote communautaire DKMS que la prise en charge du mode moniteur est limitée. Vérifiez d'abord avec `uname -r`. Uniquement sur les réseaux que vous possédez ou que vous êtes autorisé à tester.

## Avant de commencer

1. Adaptateur **ALFA AWUS036AX**
2. Câble USB-A
3. Connexion internet active

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

### Étape 3 : Cloner le pilote depuis GitHub

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
```

> **NOTE :** Le pilote amont maintenu est [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826). Si GitHub est lent, utilisez un proxy ou un miroir de confiance. Vous pouvez également télécharger des archives sur [files.alfa.com.tw](https://files.alfa.com.tw).

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

> **Fonctionne sur le noyau 6.17+ :** Avec le pilote intégré au noyau rtw89_8852bu, le mode moniteur fonctionne :
> ```bash
> sudo nmcli dev set wlxXXXX managed no
> sudo ip link set wlxXXXX down
> sudo iw dev wlxXXXX set type monitor
> sudo ip link set wlxXXXX up
> ```
> Sur les noyaux plus anciens utilisant le pilote communautaire DKMS, la prise en charge du mode moniteur peut être limitée — vous pouvez alors passer à un adaptateur MediaTek intégré au noyau comme l'[AWUS036ACM](/fr/blog/awus036acm-china-install-guide/).

### Étape 6 : Tester l'injection de paquets {#test-packet-injection}

> **Fonctionne sur le noyau 6.17+ :** Après être passé en mode moniteur, testez l'injection avec aireplay-ng (96 % en 2,4 GHz dans nos tests) :
> ```bash
> sudo iw dev wlxXXXX set channel 6
> sudo aireplay-ng --test wlxXXXX
> ```
> Uniquement sur les réseaux que vous possédez ou que vous êtes autorisé à tester. Sur les noyaux plus anciens où le pilote communautaire DKMS n'offre pas le mode moniteur, l'injection n'est pas non plus disponible.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble)

Sur Ubuntu 24.04, seul un **noyau HWE 6.17 ou plus récent** (par exemple le HWE de 24.04.4) inclut le pilote intégré au noyau rtw89_8852bu — il suffit de brancher l'adaptateur, aucune compilation n'est nécessaire. Sur le **noyau GA 6.8** ou le **noyau HWE 6.14** (aucun des deux n'inclut ce pilote), passez à un miroir domestique et compilez le pilote communautaire comme pour Ubuntu 22.04 ci-dessous, ou passez à un noyau HWE 6.17 ou plus récent pour obtenir le pilote intégré au noyau.

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

Après le redémarrage, exécutez `sudo modprobe 8852bu` et `iwconfig`. Si le module se charge et qu'une interface apparaît, c'est terminé. Ceci concerne le chemin du pilote communautaire DKMS des noyaux plus anciens (mode géré ; la prise en charge du mode moniteur peut être limitée) ; sur le noyau 6.17+, le pilote intégré au noyau rtw89_8852bu est utilisé, avec le mode moniteur et l'injection qui fonctionnent.

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

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

Cette procédure concerne le pilote communautaire DKMS pour les noyaux antérieurs à la 6.17, où la prise en charge du mode moniteur peut être limitée (voir l'étape 5 de Kali). Sur le noyau 6.17+ (par exemple Debian avec un noyau backports récent), le pilote intégré au noyau rtw89_8852bu est utilisé et le mode moniteur ainsi que l'injection fonctionnent.

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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Redirection USB vers machine virtuelle {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Configuration → USB** → Activer le **contrôleur USB 3.0 (xHCI)**.
2. Ajouter un filtre : **Realtek** (ID fabricant : 0bda, ID produit : 8832 ou 885a).
3. Démarrer la VM → `lsusb` pour confirmer → suivre les étapes Kali.

### VMware

1. **Machine virtuelle → USB et Bluetooth** → Trouver **Realtek RTL8832BU** → **Connecter**.
2. `lsusb` pour confirmer → suivre les étapes Kali.

---

## Dépannage

| Problème | Cause probable | Solution |
|----------|----------------|----------|
| `lsusb` n'affiche pas 0bda:8832 ou 0bda:885a | Adaptateur non détecté | Essayer un autre port USB |
| `install-driver.sh` échoue | En-têtes manquants | `sudo apt install linux-headers-$(uname -r)` |
| Le clonage GitHub échoue ou est lent | Problème de réseau | Utiliser un proxy ou un miroir de confiance |
| `modprobe 8852bu` échoue | Pilote non compilé ou non chargé | Relancer `sudo ./install-driver.sh`, vérifier `sudo dkms status`, puis redémarrer |
| Le mode moniteur / l'injection ne fonctionne pas | Noyau antérieur à 6.17 avec le pilote communautaire DKMS rtl8852bu (prise en charge du mode moniteur parfois limitée) | Vérifier avec `uname -r` ; utiliser un noyau 6.17+ (rtw89_8852bu intégré) ou l'AWUS036ACM sur les noyaux plus anciens |

> **Note sur le VIF :** Le pilote hors noyau RTL8832BU ne prend pas en charge les interfaces virtuelles (VIF).

## Référence des miroirs en Chine

| Ressource | URL | Utilisation |
|-----------|-----|-------------|
| Pilotes officiels Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquets de pilotes |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | Pilote RTL8832BU |
| Miroir de l'Université Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Miroir Alibaba Cloud | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| Miroir USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| Miroir Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

{{< faq >}}

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

---

## Références
1. [Site officiel Realtek](https://www.realtek.com/)
2. [Site officiel ALFA Network](https://www.alfa.com.tw/)
3. [Documentation officielle Kali Linux](https://www.kali.org/docs/)
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
