---
title: "Le pilote ALFA est cassé après la mise à jour du noyau ? Voici comment le réparer"
description: "L'adaptateur WiFi USB ALFA ne fonctionne pas après une mise à jour du noyau Linux ? Guide de réparation complet pour les pilotes RTL8812AU, RTL8811AU et MT7921AUN sur Kali Linux et Ubuntu après les mises à jour du noyau."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-driver", "kernel-update", "rtl8812au", "kali-linux", "ubuntu", "dkms", "troubleshooting"]
featureimage: "/images/blog/fix-alfa-driver-kernel-update.webp"
---

# Le pilote ALFA est cassé après la mise à jour du noyau ? Voici comment le réparer

Une mise à jour du noyau Linux casse fréquemment les pilotes WiFi USB ALFA, en particulier si vous avez installé le pilote sans DKMS. Ce guide vous explique la cause et la solution.

---

## Le problème

Après une mise à jour du noyau (par exemple via `apt upgrade`), votre adaptateur ALFA n'est peut-être plus reconnu ou le mode moniteur ne fonctionne plus.

**Cause :** L'ancien pilote a été compilé pour l'ancien noyau et ne correspond pas au nouveau noyau.

---

## Diagnostic rapide

```bash
# Vérifier si l'adaptateur est reconnu
lsusb | grep -E "0bda|Realtek"

# Vérifier si le pilote est chargé
lsmod | grep -E "88XXau|mt7921u|mt76"

# Vérifier le statut DKMS
dkms status
```

---

## Solution 1 : Recompiler le pilote (rapide)

```bash
cd /chemin/vers/rtl8812au
make clean
make
sudo make install
sudo modprobe 88XXau
```

---

## Solution 2 : Installer DKMS (permanent)

Pour une solution durable, nous recommandons l'installation DKMS :

```bash
# Supprimer et réinstaller DKMS
sudo dkms remove rtl8812au/5.6.4.2 --all
cd rtl8812au
sudo make dkms_install

# Vérifier
dkms status
# Attendu : rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

---

## Prévention : Recompile automatique

Avec DKMS, le pilote est automatiquement recompile à chaque mise à jour du noyau. Vous n'avez plus à vous soucier des pilotes cassés après les mises à jour.
