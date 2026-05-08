---
title: "Installer le pilote WiFi USB ALFA sur Kali Linux & Ubuntu 24.04 (2026)"
description: "Guide complet d'installation des pilotes d'adaptateur WiFi USB ALFA Network sur Kali Linux 2024 et Ubuntu 24.04 pour les puces RTL8812AU, MT7612U et MT7921AUN, avec des conseils de dépannage."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["driver-install", "kali-linux", "ubuntu", "RTL8812AU", "MT7612U", "MT7921AUN", "ALFA-Network"]
---

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
