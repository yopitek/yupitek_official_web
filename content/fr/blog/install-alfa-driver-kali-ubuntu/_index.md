---
title: "Installer le pilote WiFi USB ALFA sur Kali Linux & Ubuntu 24.04 (2026)"
description: "Guide complet d'installation des pilotes d'adaptateur WiFi USB ALFA Network sur Kali Linux 2024 et Ubuntu 24.04 pour les puces RTL8812AU, MT7612U et MT7921AUN, avec des conseils de dépannage."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["driver-install", "kali-linux", "ubuntu", "RTL8812AU", "MT7612U", "MT7921AUN", "ALFA-Network"]
featureimage: "/images/blog/install-alfa-driver-kali-ubuntu.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Quelle est la différence d'installation entre les pilotes MT7612U, MT7921AUN et RTL8812AU ?"
    answer: "Les pilotes MT7612U et MT7921AUN sont intégrés au noyau mainline, plug-and-play. Le RTL8812AU nécessite une installation depuis le GitHub aircrack-ng avec DKMS pour survivre aux mises à jour du noyau."
  - question: "Comment installer le pilote RTL8812AU sur Kali Linux ?"
    answer: "Sur Kali, installez directement le paquet DKMS : sudo apt install realtek-rtl88xxau-dkms. Le pilote se reconstruit automatiquement après chaque mise à jour du noyau."
  - question: "Comment installer le pilote RTL8812AU sur Ubuntu ?"
    answer: "Installez les dépendances de compilation (git, dkms, build-essential, linux-headers), clonez le dépôt aircrack-ng/rtl8812au, compilez avec make, installez avec sudo make install et sudo dkms add."
  - question: "Comment vérifier que le pilote est correctement chargé ?"
    answer: "Exécutez lsmod | grep 88XXau pour le RTL8812AU, lsmod | grep mt76 pour le MT7612U, et iwconfig pour confirmer la présence de l'interface wlan."
  - question: "Que faire si le pilote ne se charge pas après l'installation ?"
    answer: "Vérifiez que linux-headers correspond à la version du noyau. Exécutez sudo modprobe 88XXau (RTL8812AU) ou sudo modprobe mt76x2u (MT7612U). Vérifiez les erreurs dans dmesg."
---

{{< tldr >}}
L'installation du pilote ALFA dépend du chipset : MT7612U et MT7921AUN intégrés au noyau sont plug-and-play, RTL8812AU nécessite l'installation depuis le GitHub aircrack-ng avec DKMS pour survivre aux mises à jour du noyau.
{{< /tldr >}}

| Puce | Repo du pilote | Support DKMS | Temps d'installation |
|---|---|---|---|
| RTL8812AU | aircrack-ng/rtl8812au | ✓ | ~10 min |
| MT7612U | Inclus dans le noyau | N/A | ~2 min |
| MT7921AUN | Inclus dans le noyau | N/A | ~2 min |
| RTL8832BU | aircrack-ng/rtl8832bu | ✓ | ~10 min |


# Installer le pilote WiFi USB ALFA sur Kali Linux & Ubuntu 24.04 (2026)

Ce guide couvre l'installation de tous les principaux pilotes WiFi USB ALFA pour Kali Linux et Ubuntu 24.04.

---

## Aperçu des pilotes

| Puce | Repo du pilote | Support DKMS | Temps d'installation |
|---|---|---|---|
| RTL8812AU | aircrack-ng/rtl8812au | ✓ | ~10 min |
| MT7612U | Inclus dans le noyau | N/A | ~2 min |
| MT7921AUN | Inclus dans le noyau | N/A | ~2 min |
| RTL8832BU | aircrack-ng/rtl8832bu | ✓ | ~10 min |

---

## Installation : RTL8812AU (Recommandé pour Kali)

```bash
# Installer les dépendances
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)

# Cloner et installer le pilote
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
sudo make dkms_install

# Vérifier
dkms status
```

---

## Installation : MT7612U (Plug-and-Play)

Le pilote MT7612U (`mt76`) est inclus dans le noyau Linux主线. Aucun pilote supplémentaire requis :

```bash
# Brancher l'adaptateur et vérifier
lsusb | grep MediaTek

# Charger le module noyau (si pas automatique)
sudo modprobe mt76

# Vérifier
iwconfig
```

---

## Installation : MT7921AUN (Noyau 5.18+)

Le pilote MT7921AUN (`mt7921u`) est inclus dans le noyau主线 à partir de la version 5.18 :

```bash
# Vérifier le module noyau
lsmod | grep mt7921u

# Si non chargé :
sudo modprobe mt7921u

# Mise à jour du firmware pour des performances optimales
sudo apt update && sudo apt install linux-firmware
```

---

{{< faq >}}

## Dépannage

**Problème :** Le pilote ne se charge pas au redémarrage

**Solution :** Assurez-vous que le module est listé dans `/etc/modules` :

```bash
echo "88XXau" | sudo tee -a /etc/modules
```

**Problème :** Erreur DKMS après mise à jour Ubuntu

**Solution :**

```bash
sudo dkms remove rtl8812au/5.6.4.2 --all
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2
```

---

## Références
1. [Pilote officiel aircrack-ng rtl8812au](https://github.com/aircrack-ng/rtl8812au)
2. [Base de connaissances morrownr USB-WiFi](https://github.com/morrownr/USB-WiFi)
3. [Documentation officielle Kali Linux](https://www.kali.org/docs/)
4. [Documentation Ubuntu HWE Kernel](https://wiki.ubuntu.com/Kernel/LTSEnablementStack)
5. [Pilote mt76 Linux Wireless](https://wireless.wiki.kernel.org/en/users/Drivers/mt76)
