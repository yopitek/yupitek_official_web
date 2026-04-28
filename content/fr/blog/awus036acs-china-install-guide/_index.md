---
title: "Guide d'installation du pilote ALFA AWUS036ACS pour la Chine : Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Guide étape par étape pour installer les pilotes ALFA AWUS036ACS en Chine en utilisant des miroirs domestiques. Pilote RTL8811AU DKMS, mode moniteur complet et injection de paquets. Couvre Kali Linux, Ubuntu 22/24, Debian et Raspberry Pi. Aucun compte GitHub requis."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acs-china-install-guide"
tags: ["alfa", "awus036acs", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "rtl8811au"]
categories: ["Guides de pilotes"]
series: ["Guide d'installation Alfa Chine"]
related_product: "/fr/products/alfa/awus036acs/"
---

L'AWUS036ACS est l'adaptateur bi-bande compact d'ALFA pour la recherche en sécurité. Sa puce RTL8811AU prend en charge le mode moniteur complet et l'injection de paquets sur Kali Linux — mais comme le pilote est hors-noyau (out-of-kernel), vous devez le compiler à partir du code source. En Chine, GitHub est bloqué, ce guide utilise donc exclusivement des miroirs Gitee. Pas besoin de GitHub.

## Avant de commencer

Assurez-vous d'avoir ces éléments prêts :

1. Adaptateur **ALFA AWUS036ACS**
2. Câble USB (USB-A 2.0, celui fourni dans la boîte fonctionne parfaitement)
3. Connexion Internet active pour accéder aux miroirs domestiques

Branchez l'adaptateur, puis confirmez que votre système le voit :

```bash
lsusb
```

Cherchez ceci dans la sortie :

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
```

Si vous voyez `0bda:0811`, l'adaptateur est détecté. Passez à la section correspondant à votre système d'exploitation ci-dessous.

## Choisissez votre système d'exploitation

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Déjà installé ? Passez directement à :

- [Activer le mode moniteur](#activer-le-mode-moniteur)
- [Tester l'injection de paquets](#tester-linjection-de-paquets)
- [Pass-through USB pour machine virtuelle](#pass-through-usb-pour-machine-virtuelle)

---

## Kali Linux

### Étape 1 : Passer au miroir chinois

```bash
sudo nano /etc/apt/sources.list
```

Supprimez tout le contenu, puis collez :

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Sauvegardez avec **Ctrl+O**, Entrée, puis **Ctrl+X**. Actualisez :

```bash
sudo apt update
```

> **Miroir de secours :** `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Étape 2 : Installer les dépendances de compilation

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### Étape 3 : Cloner le pilote depuis Gitee

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
```

> **NOTE :** Si cette URL Gitee ne se charge pas, recherchez `8821au` sur Gitee et choisissez le fork le plus récemment mis à jour. Vous pouvez également télécharger les archives des pilotes sur [files.alfa.com.tw](https://files.alfa.com.tw).

---

### Étape 4 : Compiler et installer

```bash
sudo ./install-driver.sh
sudo reboot
```

Après le redémarrage, vérifiez que le pilote est chargé.

```bash
lsmod | grep 88XXau
```

Vous devriez voir un module `88XXau` listé. Confirmez ensuite que l'interface est apparue.

```bash
iwconfig
```

Cherchez `wlan0` ou `wlan1`.

---

### Étape 5 : Activer le mode moniteur {#activer-le-mode-moniteur}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Confirmez avec `iwconfig` — cherchez `wlan1mon` avec `Mode:Monitor`.

---

### Étape 6 : Tester l'injection de paquets {#tester-linjection-de-paquets}

```bash
sudo aireplay-ng --test wlan1mon
```

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

---

## Ubuntu 22.04 / 24.04

### Étape 1 : Passer au miroir chinois

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Supprimez tout et collez :

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

Remplacez toutes les lignes par :

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
```

---

### Étape 2 : Installer les dépendances de compilation

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

---

### Étape 3 : Cloner et installer le pilote depuis Gitee

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

---

### Étape 4 : Activer le mode moniteur

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

---

### Étape 5 : Tester l'injection de paquets

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Debian

### Étape 1 : Passer au miroir chinois

```bash
sudo nano /etc/apt/sources.list
```

Collez (Debian 12 Bookworm) :

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Étape 2 : Installer les dépendances de compilation

```bash
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
```

### Étape 3 : Cloner et installer

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### Étape 4 : Activer le mode moniteur

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Confirmez : `iwconfig` → cherchez `wlan1mon` avec `Mode:Monitor`.

### Étape 5 : Tester l'injection de paquets

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Raspberry Pi 4B / 5

### Étape 1 : Télécharger et flasher Kali ARM64

Officiel : https://www.kali.org/get-kali/#kali-arm — choisissez Raspberry Pi 4/5 64-bit.

Miroir chinois : https://repo.huaweicloud.com/kali-images/

```bash
lsblk
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Identifiants par défaut : **kali / kali**.

### Étape 2 : Passer au miroir chinois

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### Étape 3 : Installer les dépendances de compilation

```bash
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
```

### Étape 4 : Cloner et installer le pilote

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### Étape 5 : Activer le mode moniteur

Sur un Pi avec Wi-Fi intégré, l'AWUS036ACS apparaît comme `wlan1`.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

### Étape 6 : Tester l'injection de paquets

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Pass-through USB pour machine virtuelle {#pass-through-usb-pour-machine-virtuelle}

### VirtualBox

1. Éteignez la VM → **Configuration → USB** → Activez le **Contrôleur USB 2.0**.
2. Cliquez sur **+** → Sélectionnez : **Realtek** (ID: 0bda:0811).
3. Démarrez la VM. Exécutez `lsusb` pour confirmer `0bda:0811`, puis suivez les étapes Kali ci-dessus.

### VMware Fusion / Workstation

1. **Machine virtuelle → USB & Bluetooth** → Trouvez **Realtek 8811AU** → **Connecter**.
2. Exécutez `lsusb` pour confirmer, puis suivez les étapes Kali ci-dessus.

---

## Dépannage

| Problème | Cause probable | Solution |
|----------|----------------|----------|
| `lsusb` n'affiche pas 0bda:0811 | Adaptateur non alimenté ou mauvais câble | Essayez un autre port USB |
| `install-driver.sh` échoue | Headers manquants | Exécutez `sudo apt install linux-headers-$(uname -r)` |
| Le clonage Gitee échoue | Problème réseau | Recherchez `8821au` sur gitee.com, essayez un autre fork |
| `airmon-ng start` échoue | NetworkManager est en cours d'exécution | Exécutez d'abord `sudo airmon-ng check kill` |
| Pas de trafic en mode moniteur | Mauvais canal | Réglez le canal : `iwconfig wlan1mon channel 6` |
| Injection "No Answer" | AP trop loin | Rapprochez-vous. Utilisez `wlan1mon`, pas `wlan1`. |

> **Note sur le VIF :** Le pilote RTL8811AU ne prend pas en charge les interfaces virtuelles (VIF). Le mode moniteur et le mode géré simultanés ne sont pas disponibles sur cet adaptateur.

## Référence des miroirs chinois

| Ressource | URL | Utilisation pour |
|-----------|-----|------------------|
| Pilotes officiels Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquets de pilotes |
| Documentation Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Manuels produits |
| Pilote 8821au (Gitee) | [gitee.com/mirrors/8821au](https://gitee.com/mirrors/8821au) | Pilote RTL8811AU |
| Miroir Université Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Miroir Alibaba Cloud | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recommandé) |
| Miroir USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recommandé) |
| Miroir Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Images Kali ARM |

## Plus de guides d'adaptateurs Alfa pour la Chine

- [Guide d'installation AWUS036ACH Chine](/fr/blog/awus036ach-china-install-guide/) — RTL8812AU, haute puissance
- [Guide d'installation AWUS036ACM Chine](/fr/blog/awus036acm-china-install-guide/) — MT7612U, VIF complet
- AWUS036ACS ← vous êtes ici
- [Guide d'installation AWUS036AX Chine](/fr/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [Guide d'installation AWUS036AXER Chine](/fr/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [Guide d'installation AWUS036AXM Chine](/fr/blog/awus036axm-china-install-guide/) — MT7921AUN, forme en L
- [Guide d'installation AWUS036AXML Chine](/fr/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [Guide d'installation AWUS036EACS Chine](/fr/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Des questions ? Laissez un commentaire ci-dessous ou contactez-nous sur [yupitek.com](https://yupitek.com/fr/contact/).
