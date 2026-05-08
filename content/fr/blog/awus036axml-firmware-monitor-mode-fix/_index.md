---
title: "Correction de firmware du mode moniteur AWUS036AXML : Résoudre les plantages en mode actif"
description: "Comment corriger les plantages de firmware du mode moniteur AWUS036AXML sur Kali Linux. Couvre la mise à jour du firmware MT7921AUN, les exigences de version de noyau, l'astuce mode actif vs passif et l'alternative hcxdumptool."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036AXML", "MT7921AUN", "monitor-mode", "firmware", "kali-linux", "troubleshooting", "wifi-6e"]
---

# Correction de firmware du mode moniteur AWUS036AXML : Résoudre les plantages en mode actif

L'AWUS036AXML avec la puce MT7921AUN offre des performances Wi-Fi 6E de premier ordre sous Kali Linux, mais présente quelques problèmes liés au firmware en mode moniteur actif. Ce guide vous montre comment les résoudre.

---

## Le problème : Plantages liés au firmware en mode actif

Lorsque vous utilisez l'AWUS036AXML en mode moniteur actif (surveillance et envoi de trames simultanément), des plantages aléatoires peuvent survenir, attribuables à un support firmware insuffisant pour la surveillance active sur le MT7921AUN.

**Symptômes :**
- Le mode moniteur démarre avec succès, mais plante après quelques minutes
- `hcxdumptool` affiche "Firmware not responding"
- L'injection de paquets fonctionne, mais avec une latence accrue

**Solution :** Mettez à jour le firmware MT7921AUN vers la dernière version.

---

## Processus de mise à jour du firmware

```bash
# Vérifier la version actuelle du firmware
modinfo mt7921u | grep version

# Mettre à jour le package linux-firmware
sudo apt update && sudo apt install --reinstall linux-firmware

# Recharger le module
sudo modprobe -r mt7921u
sudo modprobe mt7921u

# Vérifier
dmesg | grep mt7921u
```

---

## Astuce mode actif vs passif

Si la mise à jour du firmware seule ne suffit pas, vous pouvez basculer entre la surveillance active et passive :

```bash
# Mode moniteur passif (stable, mais sans envoi de trames)
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up

# Mode moniteur actif (avec envoi de trames)
sudo airmon-ng start wlan0
```

---

## Alternative hcxdumptool

En alternative aux outils de mode moniteur standards, vous pouvez utiliser `hcxdumptool`, qui fonctionne mieux avec le firmware MT7921AUN :

```bash
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1
```
