---
title: "Guide d'installation du pilote ALFA AWUS036ACM pour la Chine : Kali Linux, Ubuntu, Debian & Raspberry Pi"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acm-china-install-guide"
tags: ["alfa", "awus036acm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "vif"]
categories: ["Driver Guides"]
series: ["Alfa China Install Guide"]
description: "Guide pas à pas pour installer les pilotes ALFA AWUS036ACM en Chine en utilisant des miroirs nationaux. Pilote MT7612U intégré au noyau, prise en charge complète du VIF. Couvre Kali Linux, Ubuntu 22/24, Debian et Raspberry Pi. GitHub non requis."
related_product: "/fr/products/alfa/awus036acm/"
---

L'AWUS036ACM est l'un des adaptateurs Alfa les plus faciles à configurer sous Linux. Sa puce MT7612U utilise le pilote `mt76x2u`, intégré au noyau Linux depuis la version 4.19. Sur la plupart des systèmes modernes, l'adaptateur fonctionne avec deux ou trois commandes. Ce guide couvre la configuration complète — vérification du pilote, mode moniteur, injection de paquets et VIF — en utilisant uniquement des miroirs nationaux. GitHub n'est pas nécessaire.

## Avant de commencer

Assurez-vous d'avoir ces éléments prêts :

1. L'adaptateur **ALFA AWUS036ACM**
2. Un câble USB (celui inclus dans la boîte convient)
3. Un hub USB alimenté — obligatoire si vous êtes sur Raspberry Pi
4. Une connexion Internet active pour accéder aux miroirs nationaux

Branchez l'adaptateur, puis confirmez que votre système le reconnaît :

```bash
lsusb
```

Recherchez ceci dans la sortie :

```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.
```

Si vous voyez `0e8d:7612`, l'adaptateur est détecté. Passez à la section de votre système d'exploitation ci-dessous.

Si vous ne le voyez pas, essayez un autre port USB ou changez le câble, puis relancez `lsusb`.

## Choisissez votre système d'exploitation

Accédez directement à la bonne section pour votre OS :

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Déjà installé ? Passez directement à :

- [Activer le mode moniteur](#enable-monitor-mode)
- [Tester l'injection de paquets](#test-packet-injection)
- [Interface virtuelle (VIF)](#virtual-interface-vif)
- [Passage USB en machine virtuelle](#virtual-machine-usb-passthrough)

---

## Kali Linux

Le pilote MT7612U est déjà dans le noyau Kali. Dans la plupart des cas, l'adaptateur fonctionne dès que vous le branchez. Les étapes ci-dessous vérifient que le pilote est chargé et vous guident à travers le mode moniteur.

### Étape 1 : Basculer vers le miroir chinois

Ouvrez votre liste de sources dans le terminal.

```bash
sudo nano /etc/apt/sources.list
```

Supprimez tout ce qui s'y trouve, puis collez cette ligne :

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Sauvegarder : appuyez sur **Ctrl+O**, puis Entrée, puis Ctrl+X pour quitter. Actualisez l'index des paquets.

```bash
sudo apt update
```

> **Miroir de secours :** Si 中科大 (USTC) est lent, utilisez 清华 (Tsinghua) à la place :
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Étape 2 : Vérifier le pilote

Vérifiez si le module s'est chargé automatiquement lors du branchement de l'adaptateur.

```bash
lsmod | grep mt76
```

Vous devriez voir une sortie contenant `mt76x2u`. Si rien n'apparaît, chargez-le manuellement.

```bash
sudo modprobe mt76x2u
```

Relancez `lsmod | grep mt76` pour confirmer. Ensuite, vérifiez que l'adaptateur est actif.

```bash
iwconfig
```

Recherchez une interface sans fil — généralement `wlan0` ou `wlan1`. Si l'interface apparaît avec un ESSID ou `unassociated`, le pilote fonctionne.

---

### Étape 2 (Alternative) : Installer des modules noyau supplémentaires

Si `modprobe mt76x2u` génère une erreur « Module not found », votre build du noyau manque peut-être des modules MT76. Installez-les depuis le miroir chinois.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
```

Après l'installation, chargez à nouveau le module.

```bash
sudo modprobe mt76x2u
```

Si le paquet n'est pas disponible pour votre version exacte du noyau, compilez le pilote depuis les sources.

```bash
sudo apt install -y git build-essential libssl-dev
git clone https://gitee.com/mirrors/mt76.git
cd mt76
make
sudo make install
sudo modprobe mt76x2u
```

> **REMARQUE :** Si cette URL Gitee ne se charge pas, recherchez `mt76` sur Gitee et choisissez le fork le plus récemment mis à jour. Vous pouvez également télécharger les archives de pilotes directement depuis [files.alfa.com.tw](https://files.alfa.com.tw).

---

### Étape 3 : Activer le mode moniteur {#enable-monitor-mode}

Avant de passer en mode moniteur, vérifiez quel nom d'interface le système a attribué à l'adaptateur.

```bash
iwconfig
```

Recherchez `wlan0` ou `wlan1`. Utilisez ce nom dans les commandes ci-dessous.

Arrêtez NetworkManager et wpa_supplicant pour qu'ils n'interfèrent pas.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirmez le changement.

```bash
iwconfig
```

Recherchez une entrée comme `wlan0mon` avec `Mode:Monitor`. Quand vous voyez cela, l'adaptateur est prêt pour la capture de paquets.

---

### Étape 4 : Tester l'injection de paquets {#test-packet-injection}

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

Si le test échoue, redémarrez et relancez-le. S'il échoue toujours, confirmez qu'aucun autre processus ne tient l'interface avec `iwconfig`.

---

## Ubuntu 22.04 / 24.04

Le pilote MT7612U est également dans le noyau Ubuntu, mais il peut se trouver dans le paquet `linux-modules-extra` plutôt que dans l'image du noyau de base. Les étapes ci-dessous gèrent les deux cas.

### Étape 1 : Basculer vers le miroir chinois

#### Ubuntu 24.04 (Noble)

Ouvrez le fichier sources au format DEB822 :

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

Sauvegardez avec `Ctrl+O`, puis quittez avec `Ctrl+X`.

#### Ubuntu 22.04 (Jammy)

Ouvrez le fichier sources classique :

```bash
sudo nano /etc/apt/sources.list
```

Remplacez toutes les lignes par :

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Sauvegardez et quittez (`Ctrl+O`, puis `Ctrl+X`).

#### Actualiser l'index des paquets

```bash
sudo apt update
```

---

### Étape 2 : Charger le pilote

Essayez d'abord de charger le module directement.

```bash
sudo modprobe mt76x2u
```

Si cela génère une erreur « Module not found », installez le paquet de modules supplémentaires.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

Vérifiez que l'adaptateur est visible.

```bash
iwconfig
```

Une interface comme `wlan0` ou `wlan1` dans la sortie confirme que le pilote est actif.

---

### Étape 3 : Installer les outils sans fil

Installez aircrack-ng pour le mode moniteur et les tests d'injection.

```bash
sudo apt install -y aircrack-ng
```

---

### Étape 4 : Activer le mode moniteur

Arrêtez les processus qui interfèrent, puis démarrez le mode moniteur.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

> **Remarque :** Votre interface peut être `wlan1` si une autre carte sans fil est présente. Lancez d'abord `iwconfig` pour vérifier.

---

### Étape 5 : Tester l'injection de paquets

```bash
sudo aireplay-ng --test wlan0mon
```

Un résultat réussi affiche `Injection is working!`. Si vous voyez des erreurs d'interface, vérifiez que le mode moniteur est actif avec `iwconfig wlan0mon`.

---

## Debian

Le pilote MT7612U est dans le noyau Debian, mais nécessite parfois le paquet `firmware-misc-nonfree` pour s'initialiser complètement.

### Étape 1 : Basculer vers le miroir chinois

Ouvrez la liste des sources :

```bash
sudo nano /etc/apt/sources.list
```

Supprimez tout et collez ces trois lignes (Debian 12 Bookworm) :

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Sauvegardez avec `Ctrl+O`, puis quittez avec `Ctrl+X`. Actualisez :

```bash
sudo apt update
```

### Étape 2 : Installer le firmware non-libre

Le MT7612U nécessite des fichiers firmware du paquet `firmware-misc-nonfree`. Sans cela, l'adaptateur s'initialise mais peut ne pas s'associer ou passer en mode moniteur.

```bash
sudo apt install -y firmware-misc-nonfree
```

### Étape 3 : Charger le pilote

```bash
sudo modprobe mt76x2u
```

Si le module est manquant, installez d'abord les modules noyau supplémentaires.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

Confirmez que l'interface est apparue.

```bash
iwconfig
```

### Étape 4 : Activer le mode moniteur

```bash
sudo apt install -y aircrack-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirmez le mode moniteur avec `iwconfig` — recherchez `wlan0mon` avec `Mode:Monitor`.

### Étape 5 : Tester l'injection de paquets

```bash
sudo aireplay-ng --test wlan0mon
```

`Injection is working!` confirme que l'adaptateur est pleinement opérationnel.

---

## Raspberry Pi 4B / 5

> L'AWUS036ACM consomme environ 400mW sous charge. Utilisez un hub USB alimenté pour éviter la limitation du Pi.

---

### Étape 1 : Télécharger l'image Kali Linux ARM64

Rendez-vous sur la page officielle de téléchargement Kali ARM :
https://www.kali.org/get-kali/#kali-arm

Choisissez **Raspberry Pi 4 (64-bit)** ou **Raspberry Pi 5 (64-bit)**. N'utilisez pas l'image 32 bits — le 64 bits est requis.

> **Miroir chinois :** Si kali.org est lent, utilisez 华为云 :
> https://repo.huaweicloud.com/kali-images/
> Naviguez jusqu'au dossier de la dernière version et téléchargez l'image ARM64 depuis là.

---

### Étape 2 : Flasher sur MicroSD

Vérifiez d'abord le chemin du périphérique de votre carte.

```bash
lsblk
```

Puis flashez, en remplaçant `/dev/sdX` par le chemin réel de votre carte.

```bash
# Remplacez /dev/sdX par votre carte SD réelle (vérifiez avec lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Attendez que `sync` se termine, puis démarrez. Identifiants par défaut : **kali / kali**.

---

### Étape 3 : Basculer vers le miroir chinois

```bash
sudo nano /etc/apt/sources.list
```

Remplacez le contenu par :

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Sauvegardez et appliquez.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

### Étape 4 : Vérifier le pilote

Après le redémarrage, branchez l'adaptateur et vérifiez.

```bash
lsmod | grep mt76
```

Si `mt76x2u` apparaît, vous avez terminé. Sinon :

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

---

### Étape 5 : Activer le mode moniteur

Sur un Pi avec Wi-Fi intégré, l'AWUS036ACM apparaît comme `wlan1` — la radio intégrée occupe `wlan0`.

```bash
iwconfig
```

Notez le nom de l'interface, puis démarrez le mode moniteur sur celui-ci.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Confirmez avec `iwconfig` — recherchez `wlan1mon` avec `Mode:Monitor`.

---

### Étape 6 : Tester l'injection de paquets

```bash
sudo aireplay-ng --test wlan1mon
```

`Injection is working!` confirme le fonctionnement complet. En cas d'échec, vérifiez que vous utilisez bien un hub alimenté.

---

## Passage USB en machine virtuelle

### VirtualBox

1. Éteignez la VM. Allez dans **Paramètres → USB**.
2. Activez le **contrôleur USB 3.0 (xHCI)**.
3. Cliquez sur **+** pour ajouter un filtre USB.
4. Sélectionnez : **MediaTek Inc. MT7612U** (ID : 0e8d:7612).
5. Démarrez la VM — l'adaptateur apparaît dans Kali.

Lancez `lsusb` dans la VM pour confirmer `0e8d:7612`, puis suivez les étapes Kali ci-dessus.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Démarrez la VM.
2. Menu : **Machine virtuelle → USB & Bluetooth**.
3. Trouvez **MediaTek MT7612U** et cliquez sur **Connecter**.
4. Lancez `lsusb` dans la VM pour confirmer, puis suivez les étapes Kali ci-dessus.

---

## Interface virtuelle (VIF)

C'est là que l'AWUS036ACM surpasse l'ACH. La puce MT7612U bénéficie d'une prise en charge VIF native complète dans le noyau. Vous pouvez faire fonctionner une interface moniteur et une interface managée ou AP sur le même adaptateur simultanément — sans correctifs, sans astuces.

### Créer une deuxième interface virtuelle

Avec l'adaptateur en mode managé sous le nom `wlan0`, ajoutez une interface moniteur à côté.

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

Vérifiez maintenant que les deux interfaces sont actives.

```bash
iwconfig
```

Vous devriez voir à la fois `wlan0` (associé, mode managé) et `mon0` (mode moniteur). L'adaptateur fait les deux en même temps.

### Cas d'utilisation : Surveiller tout en restant connecté

Cela vous permet de capturer le trafic sur `mon0` pendant que `wlan0` reste connecté à un réseau — utile pour l'analyse corrélée.

```bash
sudo airodump-ng mon0
```

`wlan0` continue son association normale pendant que `mon0` capture tout ce qui est à portée.

### Cas d'utilisation : Faux AP + Moniteur

Créez une interface AP et une interface moniteur ensemble.

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

Lancez `iwconfig` pour confirmer que les trois interfaces (`wlan0`, `ap0`, `mon0`) sont actives.

> **Remarque sur hostapd :** Le fonctionnement complet en mode AP nécessite la configuration de `hostapd`. Cela dépasse le cadre de ce guide. Les étapes ci-dessus confirment que l'adaptateur peut créer l'interface — la configuration réelle de l'AP est un sujet distinct.

---

## Dépannage

| Problème | Cause probable | Solution |
|---------|--------------|---------|
| `lsusb` n'affiche pas 0e8d:7612 | Adaptateur non alimenté ou mauvais câble | Essayez un autre port USB. Utilisez un hub alimenté sur Raspberry Pi. |
| `modprobe mt76x2u` indique « Module not found » | Modules supplémentaires manquants dans le noyau | Exécutez `sudo apt install linux-modules-extra-$(uname -r)` |
| L'interface apparaît mais ne s'associe pas | Fichier firmware manquant | Exécutez `sudo apt install firmware-misc-nonfree` (Debian) |
| `airmon-ng start wlan0` échoue | NetworkManager toujours en cours d'exécution | Exécutez d'abord `sudo airmon-ng check kill` |
| Le mode moniteur démarre mais aucun trafic capturé | Mauvais canal ou mauvais nom d'interface | Définir le canal : `iwconfig wlan0mon channel 6` |
| Le test d'injection indique « No Answer » | AP trop éloigné ou mauvaise interface | Rapprochez-vous de l'AP. Utilisez `wlan0mon`, pas `wlan0`. |
| La création d'interface VIF échoue | Pilote pas complètement chargé | Débranchez l'adaptateur, rechargez le module : `sudo rmmod mt76x2u && sudo modprobe mt76x2u` |

## Référence des miroirs chinois

Toutes les ressources utilisées dans ce guide — GitHub non requis :

| Ressource | URL | Utilisation |
|-----------|-----|------------|
| Pilotes officiels Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquets de pilotes, firmware |
| Documentation Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Manuels de produits |
| Miroir 清华大学 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Miroir 阿里云 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recommandé) |
| Miroir 中科大 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recommandé) |
| Miroir 华为云 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Images Kali ARM (sauvegarde) |
| Pilote MT76 (Gitee) | [gitee.com/mirrors/mt76](https://gitee.com/mirrors/mt76) | Compilation manuelle en secours |

## Plus de guides d'adaptateurs Alfa pour la Chine

Ceci fait partie de la série **Alfa China Install Guide**. Chaque article couvre un modèle d'adaptateur :

- [Guide d'installation AWUS036ACH pour la Chine](/fr/blog/awus036ach-china-install-guide/) — RTL8812AU, haute puissance
- AWUS036ACM ← vous êtes ici
- [Guide d'installation AWUS036ACS pour la Chine](/fr/blog/awus036acs-china-install-guide/)
- [Guide d'installation AWUS036AX pour la Chine](/fr/blog/awus036ax-china-install-guide/)
- [Guide d'installation AWUS036AXER pour la Chine](/fr/blog/awus036axer-china-install-guide/)
- [Guide d'installation AWUS036AXM pour la Chine](/fr/blog/awus036axm-china-install-guide/)
- [Guide d'installation AWUS036AXML pour la Chine](/fr/blog/awus036axml-china-install-guide/)
- [Guide d'installation AWUS036EAC pour la Chine](/fr/blog/awus036eacs-china-install-guide/)

Des questions ? Laissez un commentaire ci-dessous ou contactez-nous à [yupitek.com/fr/contact/](https://yupitek.com/fr/contact/)
