---
title: "Le pilote ALFA est cassé après la mise à jour du noyau ? Voici comment le réparer"
description: "L'adaptateur WiFi USB ALFA ne fonctionne pas après une mise à jour du noyau Linux ? Guide de réparation complet pour les pilotes RTL8812AU, RTL8811AU et MT7921AUN sur Kali Linux et Ubuntu après les mises à jour du noyau."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-driver", "kernel-update", "rtl8812au", "kali-linux", "ubuntu", "dkms", "troubleshooting"]
featureimage: "/images/blog/fix-alfa-driver-kernel-update.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Pourquoi une mise à jour du noyau casse-t-elle les pilotes ALFA ?"
    answer: "Les pilotes tiers comme RTL8812AU sont compilés pour une version spécifique du noyau. Une mise à jour change les symboles du noyau, rendant le module inutilisable. DKMS reconstruit automatiquement, mais nécessite les headers."
  - question: "Comment réparer le pilote RTL8812AU après une mise à jour du noyau ?"
    answer: "Si installé via DKMS, exécutez sudo dkms autoinstall. Vérifiez que linux-headers-$(uname -r) est installé. Sinon, recompilez manuellement depuis le dépôt aircrack-ng."
  - question: "Pourquoi le pilote MT7921AUN échoue-t-il après une mise à jour du noyau ?"
    answer: "Le pilote mt7921u est intégré au noyau, mais le firmware peut être manquant. Installez firmware-misc-nonfree à la dernière version pour restaurer le fonctionnement."
  - question: "Comment prévenir durablement les défaillances de pilote après mise à jour du noyau ?"
    answer: "Pour le RTL8812AU, utilisez DKMS qui reconstruit automatiquement. Pour le MT7921AUN, gardez firmware-misc-nonfree à jour. Utilisez un noyau LTS pour minimiser les ruptures."
  - question: "Comment vérifier qu'un pilote est correctement chargé ?"
    answer: "Exécutez lsmod | grep mt76 pour le MT7612U, lsmod | grep 88XXau pour le RTL8812AU, et iwconfig pour confirmer la présence de l'interface wlan."
---

{{< tldr >}}
La cause principale des défaillances de pilotes ALFA après mise à jour du noyau est la désynchronisation des headers et modules. RTL8812AU se reconstruit via dkms autoinstall, MT7921AUN nécessite firmware-misc-nonfree. Le noyau LTS est la solution long terme.
{{< /tldr >}}

Après une mise à jour du noyau (par exemple via `apt upgrade`), votre adaptateur ALFA n'est peut-être plus reconnu ou le mode moniteur ne fonctionne plus.


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

{{< faq >}}

## Prévention : Recompile automatique

Avec DKMS, le pilote est automatiquement recompile à chaque mise à jour du noyau. Vous n'avez plus à vous soucier des pilotes cassés après les mises à jour.

---

## Références
1. [Pilote officiel aircrack-ng rtl8812au](https://github.com/aircrack-ng/rtl8812au)
2. [Documentation officielle DKMS](https://github.com/dell/dkms)
3. [Documentation de gestion des paquets Kali Linux](https://www.kali.org/docs/general-use/package-management/)
4. [Documentation officielle du noyau Linux](https://www.kernel.org/doc/html/latest/)
5. [Pilote MediaTek MT7921](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek/mt7921)
