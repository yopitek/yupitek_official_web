---
title: "Guide d'installation du pilote ALFA AWUS036ACH pour la Chine : Kali Linux, Ubuntu, Debian & Raspberry Pi"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "driver", "china", "monitor-mode"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 1
description: "Guide étape par étape pour installer le pilote ALFA AWUS036ACH en Chine en utilisant des miroirs domestiques. Compatible Kali Linux, Ubuntu 22/24, Debian et Raspberry Pi. Aucun accès à GitHub requis."
related_product: "/fr/products/alfa/awus036ach/"
featureimage: "/images/blog/awus036ach-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Quel chipset utilise l'AWUS036ACH ? Faut-il installer un pilote ?"
    answer: "L'AWUS036ACH utilise le chipset Realtek RTL8812AU. Le pilote n'est pas intégré au noyau Linux et nécessite une installation manuelle."
  - question: "Faut-il un VPN pour installer le pilote AWUS036ACH en Chine ?"
    answer: "Non, l'installation utilise uniquement des miroirs nationaux (USTC, Aliyun) et Gitee pour le code source."
  - question: "L'AWUS036ACH supporte-t-il le mode moniteur et l'injection de paquets ?"
    answer: "Oui, après installation du pilote RTL8812AU, utilisez airmon-ng pour activer le mode moniteur et aireplay-ng pour tester l'injection."
  - question: "L'AWUS036ACH fonctionne-t-il sur Raspberry Pi ?"
    answer: "Oui, utilisez un hub USB alimenté et flashez la version Kali ARM64."
  - question: "Quelle est la commande pour installer le pilote AWUS036ACH sur Kali Linux ?"
    answer: "Kali permet d'installer directement avec sudo apt install realtek-rtl88xxau-dkms."
---

{{< tldr >}}
L'AWUS036ACH utilise le chipset RTL8812AU. Sur Kali, installez le pilote DKMS via apt. Sur Ubuntu/Debian, compilez depuis Gitee. Mode moniteur et injection opérationnels en 30 minutes.
{{< /tldr >}}

Vous venez de recevoir le AWUS036ACH et votre système Linux ne le reconnaît pas. C'est tout à fait normal — cette puce nécessite le pilote RTL8812AU, qui ne fonctionne pas en plug-and-play. Ce guide vous accompagne tout au long de l'installation en environ 30 minutes, en utilisant uniquement des miroirs domestiques. Aucun accès à GitHub n'est requis.

## Avant de commencer

Assurez-vous d'avoir ces éléments prêts :

1. **ALFA AWUS036ACH** adaptateur
2. Câble USB (celui fourni dans la boîte convient parfaitement)
3. Un hub USB alimenté — obligatoire sur Raspberry Pi
4. Connexion Internet active vers les miroirs domestiques

Branchez l'adaptateur, puis vérifiez que votre système le détecte :

```bash
lsusb
```

Cherchez cette ligne dans la sortie :

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

Si vous voyez `0bda:8812`, l'adaptateur est détecté. Passez à la section correspondant à votre OS ci-dessous.

Si vous ne le voyez pas, essayez un autre port USB ou changez le câble, puis relancez `lsusb`.

## Choisissez votre système d'exploitation

Accédez directement à la section correspondant à votre OS :

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Déjà installé ? Passez directement à :

- [Activer le mode moniteur](#activer-le-mode-moniteur)
- [Tester l'injection de paquets](#tester-linjection-de-paquets)
- [Passthrough USB pour VM](#passthrough-usb-pour-machine-virtuelle)

---

## Kali Linux

Kali est livré avec des outils sans fil puissants intégrés. Faire fonctionner le pilote AWUS036ACH se fait en quatre étapes. Commencez par passer à un miroir chinois rapide pour que tous les téléchargements restent fluides.

### Étape 1 : Passer au miroir China

Ouvrez votre liste de sources dans le terminal.

```bash
sudo nano /etc/apt/sources.list
```

Supprimez tout ce qu'il y a dedans, puis collez cette ligne :

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Sauvegardez le fichier : appuyez sur **Ctrl+O**, puis Entrée, puis Ctrl+X pour quitter. Actualisez l'index des paquets.

```bash
sudo apt update
```

> **Miroir de secours :** Si 中科大 (USTC) est lent sur votre connexion, utilisez plutôt 清华 (Tsinghua) :
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Étape 2 : Installer le pilote

Le dépôt de paquets de Kali comprend un pilote DKMS préconstruit. Installez-le avec une seule commande.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

DKMS recompile automatiquement le pilote à chaque mise à jour du noyau, vous n'aurez donc pas besoin de le réinstaller manuellement après une mise à niveau.

Vérifiez que le pilote s'est chargé correctement.

```bash
modinfo 88XXau | grep -E "filename|version"
```

Vous devriez voir une ligne `filename` se terminant par `.ko` et une ligne `version` affichant une chaîne de version comme `5.6.4.2`. Si les deux apparaissent, le pilote est prêt.

---

### Étape 2 (Alternative) : Compilation manuelle depuis les sources

Suivez cette section uniquement si `apt install` ci-dessus a échoué. Installez d'abord les dépendances de compilation.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Téléchargez le code source du pilote depuis Gitee.

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

> **REMARQUE :** Si cette URL ne se charge pas, recherchez `rtl8812au` sur Gitee et choisissez le fork le plus récemment mis à jour. Vous pouvez également télécharger une archive source directement depuis [files.alfa.com.tw](https://files.alfa.com.tw).

Entrez dans le répertoire cloné, puis compilez et installez.

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

Chargez le pilote dans le noyau en cours d'exécution.

```bash
sudo modprobe 88XXau
```

---

### Étape 3 : Activer le mode moniteur {#activer-le-mode-moniteur}

Avant de passer l'adaptateur en mode moniteur, vérifiez le nom d'interface que votre système lui a attribué.

```bash
iwconfig
```

Cherchez une entrée `wlan0` ou `wlan1`. Utilisez ce nom dans les commandes ci-dessous.

Arrêtez NetworkManager et wpa_supplicant — les deux se disputent l'adaptateur et bloqueront le mode moniteur.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirmez que le changement a fonctionné.

```bash
iwconfig
```

Cherchez une entrée comme `wlan0mon` avec `Mode:Monitor`. Lorsque vous la voyez, l'adaptateur est prêt pour la capture de paquets.

---

### Étape 4 : Tester l'injection de paquets {#tester-linjection-de-paquets}

Lancez le test d'injection contre l'interface moniteur.

```bash
sudo aireplay-ng --test wlan0mon
```

Un résultat réussi ressemble à ceci :

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

Si le test échoue, redémarrez la machine et relancez le test. S'il échoue toujours après un redémarrage, vérifiez qu'aucun autre processus ne détient l'interface — lancez `iwconfig` et assurez-vous que seul `wlan0mon` apparaît, sans rien d'autre qui revendique l'adaptateur.

---

## Ubuntu 22.04 / 24.04

Ubuntu se divise en deux branches avec des formats de fichiers de paquets différents. Les étapes ci-dessous couvrent les deux. Utilisez **阿里云 (Aliyun)** comme miroir — il est rapide, fiable et maintenu par Alibaba.

### Étape 1 : Passer au miroir China

Choisissez votre version d'Ubuntu et suivez uniquement ce chemin.

#### Ubuntu 24.04 (Noble)

Ouvrez le nouveau fichier sources au format DEB822 :

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Supprimez tout dans le fichier et collez ce contenu exact :

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Sauvegardez avec `Ctrl+O`, puis quittez avec `Ctrl+X`.

#### Ubuntu 22.04 (Jammy)

Ouvrez plutôt le fichier sources classique :

```bash
sudo nano /etc/apt/sources.list
```

Remplacez toutes les lignes existantes par :

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Sauvegardez et quittez de la même façon (`Ctrl+O`, puis `Ctrl+X`).

#### Actualiser l'index des paquets

Lancez ceci pour les deux versions après avoir modifié votre fichier sources :

```bash
sudo apt update
```

---

### Étape 2 : Installer les dépendances de compilation

Le pilote se compile depuis les sources, vous avez donc besoin des en-têtes du noyau et des outils de compilation en premier :

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Ceci installe gcc, make et les en-têtes correspondant exactement à votre noyau en cours d'exécution. La partie `$(uname -r)` détecte automatiquement votre version du noyau — pas besoin de la taper manuellement.

---

### Étape 3 : Télécharger les sources du pilote (miroir China)

Clonez le dépôt du pilote depuis Gitee, accessible en Chine :

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

Puis entrez dans le dossier cloné :

```bash
cd rtl8812au
```

> **Remarque :** Si cette URL expire ou renvoie une 404, allez sur [gitee.com](https://gitee.com) et recherchez `rtl8812au`. Choisissez le fork avec la date de commit la plus récente.

---

### Étape 4 : Compiler et installer

Construisez le module noyau depuis les sources :

```bash
make
```

Installez-le dans le système :

```bash
sudo make install
```

Enregistrez le module auprès de DKMS pour qu'il survive aux mises à niveau du noyau :

```bash
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

Chargez le module dans le noyau en cours d'exécution :

```bash
sudo modprobe 88XXau
```

Vérifiez que le module s'est chargé correctement :

```bash
modinfo 88XXau | grep filename
```

Vous devriez voir un chemin se terminant par `88XXau.ko` ou similaire. Si la commande retourne une sortie, le pilote est actif.

---

### Étape 5 : Activer le mode moniteur

Terminez d'abord tous les processus qui pourraient interférer avec l'interface sans fil :

```bash
sudo airmon-ng check kill
```

Puis passez l'adaptateur en mode moniteur :

```bash
sudo airmon-ng start wlan0
```

> **Remarque :** Votre interface peut s'appeler `wlan1` au lieu de `wlan0`. Lancez d'abord `iwconfig` pour voir toutes les interfaces sans fil listées, puis substituez le nom correct dans la commande ci-dessus.

---

### Étape 6 : Tester l'injection de paquets

Avec l'adaptateur en mode moniteur, lancez le test d'injection :

```bash
sudo aireplay-ng --test wlan0mon
```

Un résultat réussi affiche des lignes comme `Injection is working!`. Si vous voyez des erreurs sur l'interface, vérifiez que le mode moniteur est actif avec `iwconfig wlan0mon`.

---

## Debian

Le gestionnaire de paquets de Debian pointe par défaut vers des serveurs étrangers. Passer au miroir 清华大学 (Université Tsinghua) fait passer les vitesses de téléchargement de l'escargot au sprint.

### Étape 1 : Passer au miroir China

Ouvrez la liste des sources :

```bash
sudo nano /etc/apt/sources.list
```

Supprimez tout à l'intérieur et collez ces trois lignes (Debian 12 Bookworm) :

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Sauvegardez avec `Ctrl+O`, puis quittez avec `Ctrl+X`. Actualisez l'index des paquets :

```bash
sudo apt update
```

### Étape 2 : Installer les dépendances de compilation

Le pilote AWUS036ACH se compile depuis les sources, vous avez besoin des en-têtes du noyau et des outils de compilation :

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Cette commande installe automatiquement le paquet d'en-têtes correspondant à votre version du noyau en cours.

### Étape 3 : Télécharger les sources du pilote (miroir China)

Clonez le dépôt du pilote depuis Gitee :

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

Entrez dans le dossier du projet :

```bash
cd rtl8812au
```

> **Impossible d'accéder à cette URL ?** Recherchez `rtl8812au` sur Gitee et choisissez le fork le plus récemment mis à jour.

### Étape 4 : Compiler et installer

Lancez ces commandes dans l'ordre dans le dossier `rtl8812au` :

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

`dkms` enregistre le pilote pour qu'il survive automatiquement aux mises à jour du noyau.

### Étape 5 : Activer le mode moniteur

**Terminez les processus interférants** avant de changer de mode :

```bash
sudo airmon-ng check kill
```

Démarrez le mode moniteur sur votre adaptateur :

```bash
sudo airmon-ng start wlan0
```

Si `airmon-ng` est absent, installez-le d'abord :

```bash
sudo apt install -y aircrack-ng
```

Confirmez que l'interface est montée :

```bash
iwconfig
```

Cherchez une interface nommée `wlan0mon` dans la sortie.

### Étape 6 : Tester l'injection de paquets

```bash
sudo aireplay-ng --test wlan0mon
```

Un flux de résultats de test d'injection confirme que l'adaptateur fonctionne. Vous êtes prêt.

---

## Raspberry Pi 4B / 5

> Le AWUS036ACH consomme environ 500mW. Le brancher directement sur un port USB du Raspberry Pi peut provoquer une limitation ou un redémarrage du Pi sous charge. **Utilisez toujours un hub USB avec alimentation propre.**

---

### Étape 1 : Télécharger l'image Kali Linux ARM64

Allez sur la page officielle de téléchargement ARM de Kali :
https://www.kali.org/get-kali/#kali-arm

Choisissez **Raspberry Pi 4 (64-bit)** ou **Raspberry Pi 5 (64-bit)** selon votre carte. Ne téléchargez pas l'image 32-bit — la compilation du pilote nécessite un noyau 64-bit.

> **Miroir China :** Si kali.org charge lentement, essayez plutôt 华为云 :
> https://repo.huaweicloud.com/kali-images/
> Naviguez vers le dossier de la dernière release et téléchargez la même image ARM64 depuis là.

---

### Étape 2 : Flasher sur MicroSD

Insérez votre carte microSD, puis vérifiez son chemin de périphérique avant d'écrire quoi que ce soit.

```bash
lsblk
```

Trouvez votre carte dans la liste — elle apparaîtra comme quelque chose de type `sdb` ou `mmcblk0`. Flashez ensuite l'image, en remplaçant `/dev/sdX` par votre chemin réel.

```bash
# Remplacez /dev/sdX par votre carte SD réelle (vérifiez avec lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Attendez que `sync` se termine avant de retirer la carte. Démarrez le Pi depuis la carte. Identifiants par défaut après démarrage : **kali / kali**.

---

### Étape 3 : Passer au miroir China

Après le premier démarrage, ouvrez le fichier des sources de paquets.

```bash
sudo nano /etc/apt/sources.list
```

Supprimez tout dans le fichier et remplacez par cette unique ligne :

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Sauvegardez : appuyez sur **Ctrl+O**, puis Entrée, puis Ctrl+X. Appliquez le miroir et mettez à jour le système.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

Le redémarrage prend en compte les mises à jour du noyau avant l'installation du pilote.

---

### Étape 4 : Installer le pilote (ARM64)

Le paquet DKMS fonctionne sur ARM64 exactement comme sur x86 — aucune étape spéciale nécessaire.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

Si cette commande renvoie une erreur indiquant que le paquet est introuvable, compilez le pilote depuis les sources à la place.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

---

### Étape 5 : Activer le mode moniteur

Avant de toucher l'adaptateur, vérifiez le nom d'interface que le Pi lui a attribué.

```bash
iwconfig
```

Sur un Pi avec une puce Wi-Fi intégrée, le AWUS036ACH apparaît comme `wlan1` — la radio intégrée occupe `wlan0`. Utilisez le nom rapporté par `iwconfig` ci-dessus.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Relancez `iwconfig` et cherchez une entrée se terminant par `mon` — `wlan1mon` dans le cas typique du Pi — avec `Mode:Monitor`. Cela confirme que l'adaptateur a bien basculé.

---

### Étape 6 : Tester l'injection de paquets

```bash
sudo aireplay-ng --test wlan1mon
```

Remplacez `wlan1mon` par le nom d'interface moniteur apparu à l'étape 5. Un adaptateur fonctionnel affiche `Injection is working!`. Si le test échoue, redémarrez et réessayez. Une mauvaise connexion USB via un hub sans alimentation propre est la cause la plus fréquente sur Pi — vérifiez que vous utilisez bien le hub alimenté.

---

## Passthrough USB pour machine virtuelle

Vous faites tourner Kali Linux dans une VM sur macOS ou Windows ? Vous devez passer l'adaptateur USB au système d'exploitation invité.

### VirtualBox

1. La VM éteinte, allez dans **Paramètres → USB**.
2. Activez **Contrôleur USB 3.0 (xHCI)**.
3. Cliquez sur l'icône **+** pour ajouter un filtre USB.
4. Sélectionnez : **Realtek 802.11ac NIC [...]** (ID: 0bda:8812).
5. Démarrez la VM — l'adaptateur apparaît dans Kali.

Dans la VM, lancez `lsusb` pour confirmer que `0bda:8812` apparaît, puis suivez les étapes Kali Linux ci-dessus.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Démarrez la VM.
2. Dans le menu : **Machine virtuelle → USB & Bluetooth**.
3. Trouvez **Realtek 802.11ac NIC** et cliquez sur **Connecter**.
4. L'adaptateur se déconnecte de l'hôte et apparaît dans la VM.

Lancez `lsusb` dans la VM pour confirmer, puis suivez les étapes Kali Linux ci-dessus.

### Note sur le VIF (Interface Virtuelle)

La puce RTL8812AU dans le AWUS036ACH a un support VIF limité sous Linux. Vous ne pouvez pas faire fonctionner de manière fiable le mode géré et le mode moniteur (ou le mode AP) en même temps sur le même adaptateur.

Si votre flux de travail nécessite VIF — par exemple, faire tourner des faux AP tout en surveillant simultanément — le AWUS036ACH n'est pas le bon outil. Consultez plutôt le [guide d'installation AWUS036ACM](/fr/blog/awus036acm-china-install-guide/). Cet adaptateur utilise la puce MT7612U, qui bénéficie d'un support VIF natif complet dans le noyau et gère les interfaces virtuelles simultanées sans patches.

---

## Dépannage

| Problème | Cause probable | Solution |
|----------|---------------|---------|
| `lsusb` n'affiche pas 0bda:8812 | Adaptateur non alimenté ou câble défectueux | Essayez un autre port USB. Utilisez un hub alimenté sur Raspberry Pi. |
| `make` échoue avec des erreurs d'en-tête | En-têtes du noyau manquants ou version incompatible | Lancez `sudo apt install linux-headers-$(uname -r)` |
| `modprobe 88XXau` échoue | Secure Boot bloque les modules non signés | Désactivez Secure Boot dans le BIOS, ou signez le module |
| Le pilote disparaît après une mise à jour du noyau | Pilote non enregistré auprès de DKMS | Relancez `sudo dkms install rtl8812au/$(cat VERSION)` depuis le répertoire source |
| `airmon-ng start wlan0` échoue | NetworkManager toujours en cours d'exécution | Lancez d'abord `sudo airmon-ng check kill` |
| Le mode moniteur démarre mais ne capture pas le trafic | Mauvais canal ou mauvais nom d'interface | Vérifiez l'interface avec `iwconfig`. Définissez le canal : `iwconfig wlan0mon channel 6` |
| Le test d'injection indique "No Answer" | AP trop éloigné, ou mauvaise interface | Rapprochez-vous du AP. Utilisez `wlan0mon` et non `wlan0` |

## Référence des miroirs China

Toutes les ressources utilisées dans ce guide — GitHub non requis :

| Ressource | URL | Utilisé pour |
|-----------|-----|-------------|
| Pilotes officiels Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquets de pilotes, firmware |
| Documentation Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Manuels produits |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recommandé) |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recommandé) |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Images Kali ARM (backup) |
| Pilote RTL8812AU (Gitee) | [gitee.com/mirrors/rtl8812au](https://gitee.com/mirrors/rtl8812au) | Compilation manuelle en fallback |

{{< faq >}}

## Plus de guides d'adaptateurs Alfa pour la Chine

Ceci fait partie de la série **Alfa China Install Guide**. Chaque article couvre un modèle d'adaptateur :

- AWUS036ACH ← vous êtes ici
- [Guide d'installation AWUS036ACM pour la Chine](/fr/blog/awus036acm-china-install-guide/) — MT7612U, meilleur support VIF
- [Guide d'installation AWUS036ACS pour la Chine](/fr/blog/awus036acs-china-install-guide/)
- [Guide d'installation AWUS036AX pour la Chine](/fr/blog/awus036ax-china-install-guide/)
- [Guide d'installation AWUS036AXER pour la Chine](/fr/blog/awus036axer-china-install-guide/)
- [Guide d'installation AWUS036AXM pour la Chine](/fr/blog/awus036axm-china-install-guide/)
- [Guide d'installation AWUS036AXML pour la Chine](/fr/blog/awus036axml-china-install-guide/)
- [Guide d'installation AWUS036EAC pour la Chine](/fr/blog/awus036eacs-china-install-guide/)

Des questions ? Laissez un commentaire ci-dessous ou contactez-nous sur [yupitek.com](https://yupitek.com/fr/contact/).

---

## Références
1. [Documentation officielle aircrack-ng](https://www.aircrack-ng.org/)
2. [Site officiel ALFA Network](https://www.alfa.com.tw/)
3. [Documentation officielle Kali Linux](https://www.kali.org/docs/)
4. [Miroir Gitee rtl8812au](https://gitee.com/mirrors/rtl8812au)
5. [Pilote Realtek RTL8812AU](https://www.realtek.com/)
