---
title: "Correction de firmware du mode moniteur AWUS036AXML : Résoudre les plantages en mode actif"
description: "Comment corriger les plantages de firmware du mode moniteur AWUS036AXML sur Kali Linux. Couvre la mise à jour du firmware MT7921AUN, les exigences de version de noyau, l'astuce mode actif vs passif et l'alternative hcxdumptool."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036AXML", "MT7921AUN", "monitor-mode", "firmware", "kali-linux", "troubleshooting", "wifi-6e"]
featureimage: "/images/blog/awus036axml-firmware-monitor-mode-fix.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Pourquoi l'AWUS036AXML plante-t-il en mode moniteur actif ?"
    answer: "Le MT7921AUN utilise une architecture MAC basée firmware. La combinaison actuelle du pilote mt7921u et du firmware n'implémente pas complètement les chemins de commandes nécessaires à l'injection active. L'interface disparaît après aireplay-ng."
  - question: "Comment réparer le plantage en mode actif du MT7921AUN ?"
    answer: "Mettez à jour firmware-misc-nonfree, passez au noyau 6.6+ et évitez les déauth floods à haut débit. Cela améliore mais n'élimine pas nécessairement le plantage."
  - question: "Comment hcxdumptool capture-t-il le PMKID sans injection de paquets ?"
    answer: "hcxdumptool en mode passif extrait le PMKID des beacon et probe response diffusés par l'AP, sans transmettre aucun paquet, évitant le plantage du firmware."
  - question: "Quelles sont les limitations du mode moniteur passif de l'AWUS036AXML ?"
    answer: "Le mode passif capture les beacon, handshake et PMKID, mais ne peut pas exécuter les déauth, probe requests ou association floods. Ces opérations actives nécessitent l'AWUS036ACH."
  - question: "Quelles versions du noyau améliorent la stabilité du MT7921AUN ?"
    answer: "Le noyau 6.1 LTS ou plus récent inclut plusieurs correctifs mt7921u. Le noyau 6.6+ apporte des améliorations supplémentaires à la pile de pilotes USB MediaTek."
---

{{< tldr >}}
Le pilote mt7921u de l'AWUS036AXML provoque un plantage du firmware lors de l'injection active de paquets. Cet article explique la cause racine, les étapes de diagnostic, et les solutions de contournement.
{{< /tldr >}}

Lorsque vous utilisez l'AWUS036AXML en mode moniteur actif (surveillance et envoi de trames simultanément), des plantages aléatoires peuvent survenir, attribuables à un support firmware insuffisant pour la surveillance active sur le MT7921AUN.


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

{{< faq >}}

## Alternative hcxdumptool

En alternative aux outils de mode moniteur standards, vous pouvez utiliser `hcxdumptool`, qui fonctionne mieux avec le firmware MT7921AUN :

```bash
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1
```

---

## Références
1. [Dépôt firmware Linux (kernel.org)](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git)
2. [Pilote mt76 du noyau Linux](https://wireless.wiki.kernel.org/en/users/drivers/mediatek)
3. [Suite d'outils aircrack-ng](https://www.aircrack-ng.org/)
4. [Projet GitHub hcxdumptool](https://github.com/ZerBea/hcxdumptool)
5. [Support officiel ALFA Network](https://www.alfa.com.tw/)
