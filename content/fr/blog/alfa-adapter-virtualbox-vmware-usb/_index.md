---
title: "Passthrough USB d'adaptateur ALFA : Guide d'installation VirtualBox & VMware"
description: "Guide étape par étape pour le passthrough USB d'adaptateur WiFi USB ALFA dans VirtualBox et VMware Workstation pour Kali Linux. Couvre l'AWUS036ACH, l'AWUS036AXML, le filtre USB 3.0, l'Extension Pack et le dépannage."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "passthrough-usb", "kali-linux", "alfa-network", "AWUS036ACH", "AWUS036AXML"]
featureimage: "/images/blog/alfa-adapter-virtualbox-vmware-usb.webp"
---

Faire fonctionner un adaptateur WiFi ALFA à l'intérieur d'une machine virtuelle (VM) n'est pas aussi simple que de le brancher en espérant que le système d'exploitation invité le reconnaisse. Contrairement aux dossiers partagés ou au réseau en pont (bridged), le mode moniteur et l'injection de paquets bruts nécessitent un **contrôle USB complet** — la VM doit posséder exclusivement le périphérique USB, sans le partager via la pile réseau de l'hôte. C'est ce qu'on appelle le passthrough USB, et bien le configurer est l'échec d'installation le plus courant pour les pentesters et les joueurs de CTF travaillant en VM.

Ce guide couvre la configuration complète du passthrough pour **VirtualBox 7.x** et **VMware Workstation 17+ / VMware Fusion 13+**, en ciblant Kali Linux comme système d'exploitation invité. Il traite à la fois de l'AWUS036ACH (chipset RTL8812AU) et de la plus récente AWUS036AXML (chipset MT7921AUN), avec des notes spécifiques par adaptateur lorsque le comportement diffère.

À la fin de ce guide, votre adaptateur ALFA apparaîtra dans Kali via `lsusb`, le bon pilote sera chargé et `airmon-ng` confirmera que le mode moniteur fonctionne.

---

## Prérequis

Avant de commencer, confirmez que votre environnement correspond aux exigences ci-dessous. L'absence de n'importe quel élément — en particulier l'Extension Pack de VirtualBox — est la cause principale de la plupart des échecs de passthrough.

| Exigence | Détails |
|---|---|
| **Hyperviseur** | VirtualBox 7.x + Extension Pack **ou** VMware Workstation 17+ / Fusion 13+ |
| **OS Invité** | Kali Linux 2024.x ou plus récent (testé sur 2024.1–2025.1) |
| **Adaptateur ALFA** | AWUS036ACH, AWUS036AXML, AWUS036ACM, ou tout périphérique RTL8812AU / MT7921AUN |
| **Port USB hôte** | USB 3.0 recommandé (surtout pour l'AWUS036AXML) |
| **OS Hôte** | Windows 10/11, Linux, ou macOS (Fusion) |
| **Accès Sudo** | Requis à l'intérieur de la VM Kali |

{{< alert "circle-info" >}}
Si vous n'avez pas encore installé le pilote dans Kali, effectuez d'abord les étapes de passthrough USB de ce guide. Une fois que l'adaptateur est visible dans la VM, suivez le [Guide d'installation du pilote ALFA](/fr/blog/install-alfa-driver-kali-ubuntu/) pour compiler et charger le bon pilote.
{{< /alert >}}

---

## Passthrough USB VirtualBox — Étape par étape

VirtualBox nécessite un composant supplémentaire — l'**Extension Pack** — pour prendre en charge le passthrough USB 2.0 et USB 3.0. Sans lui, seul l'USB 1.1 (OHCI) est disponible, ce qui est insuffisant pour les adaptateurs ALFA modernes.

### Installer l'Extension Pack de VirtualBox

1. Ouvrez [virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads).
2. Sous **VirtualBox Extension Pack**, cliquez sur **All supported platforms** pour télécharger le fichier `.vbox-extpack`. La version doit correspondre exactement à votre version de VirtualBox installée.
3. Ouvrez VirtualBox, allez dans **Fichier → Paramètres → Extensions** (sur macOS : **VirtualBox → Réglages → Extensions**).
4. Cliquez sur l'icône **+**, parcourez jusqu'au fichier `.vbox-extpack` téléchargé et installez-le. Acceptez la licence lorsque vous y êtes invité.

Pour vérifier que l'Extension Pack est actif depuis la ligne de commande :

```bash
VBoxManage list extpacks
```

Sortie attendue :

```
Extension Packs: 1
Pack no. 0:   Oracle VirtualBox Extension Pack
Version:      7.0.x
...
Usable:       true
```

{{< alert "triangle-exclamation" >}}
Si le champ **Usable** affiche `false`, la version de l'Extension Pack ne correspond pas à votre version de VirtualBox. Désinstallez et réinstallez la version correcte.
{{< /alert >}}

### Ajouter votre utilisateur au groupe vboxusers (Hôtes Linux uniquement)

Sur les hôtes Linux, votre compte utilisateur doit être membre du groupe `vboxusers` pour accéder aux périphériques USB.

```bash
sudo usermod -aG vboxusers $USER && newgrp vboxusers
```

Après avoir exécuté cela, **déconnectez-vous et reconnectez-vous** (ou redémarrez) pour que le changement de groupe prenne effet. Vous pouvez vérifier avec :

```bash
groups $USER
```

La sortie doit inclure `vboxusers`.

### Activer le contrôleur USB dans les paramètres de la VM

1. Éteignez votre VM Kali si elle est en cours d'exécution.
2. Sélectionnez la VM, cliquez sur **Configuration → USB**.
3. Cochez **Activer le contrôleur USB**.
4. Sélectionnez **Contrôleur USB 3.0 (xHCI)** dans les boutons radio.

{{< alert "circle-info" >}}
L'USB 3.0 (xHCI) est requis pour l'AWUS036AXML. Pour l'AWUS036ACH, l'USB 2.0 (EHCI) est techniquement suffisant car l'adaptateur lui-même est en USB 2.0, mais l'utilisation de l'xHCI ne cause aucun dommage et maintient votre configuration cohérente.
{{< /alert >}}

### Ajouter un filtre de périphérique USB

Un filtre de périphérique USB indique à VirtualBox de capturer automatiquement l'adaptateur ALFA chaque fois qu'il est branché, sans nécessiter d'intervention manuelle à chaque session.

1. Dans le même panneau **Configuration → USB**, cliquez sur l'icône **+** (Ajouter un filtre USB à partir d'un périphérique).
2. Branchez votre adaptateur ALFA maintenant s'il n'est pas déjà connecté. VirtualBox l'affichera dans la liste déroulante.
3. Sélectionnez le périphérique. Il apparaît généralement sous le nom **"Realtek 802.11ac NIC"** (AWUS036ACH) ou **"MediaTek Corp. 802.11 b/g/n"** (AWUS036AXML).
4. Cliquez sur **OK** pour enregistrer.

Le filtre stocke l'ID du vendeur et du produit. La prochaine fois que la VM démarrera avec l'adaptateur branché, VirtualBox le fera passer automatiquement.

### Démarrer la VM et vérifier avec lsusb

Démarrez votre VM Kali. Une fois le bureau chargé, ouvrez un terminal et exécutez :

```bash
lsusb
```

Vous devriez voir une ligne ressemblant à :

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

ou pour l'AWUS036AXML :

```
Bus 002 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

Si le périphérique n'apparaît pas, consultez le tableau de dépannage à la fin de cette section.

### Charger le pilote

**AWUS036ACH (RTL8812AU) :**

```bash
sudo modprobe 88XXau
```

Si cela échoue (module non trouvé), installez d'abord le paquet DKMS :

```bash
sudo apt update && sudo apt install -y realtek-rtl88xxau-dkms
sudo modprobe 88XXau
```

**AWUS036AXML (MT7921AUN) :**

```bash
sudo modprobe mt7921u
```

Le pilote MT7921AUN est inclus dans le noyau principal depuis la version 5.18. Kali 2024.x est livré avec un noyau assez récent pour l'inclure, mais vous pourriez également avoir besoin du firmware :

```bash
sudo apt install -y firmware-misc-nonfree
```

### Vérifier le mode moniteur

Une fois le pilote chargé, confirmez le nom de l'interface :

```bash
ip link show
```

Recherchez une interface nommée `wlan0`, `wlan1` ou similaire. Activez ensuite le mode moniteur :

```bash
sudo airmon-ng start wlan1
```

La sortie réussie se termine par le nom de l'interface moniteur (ex: `wlan1mon`). Vérifiez :

```bash
sudo iwconfig wlan1mon
```

Le champ **Mode** doit afficher `Monitor`.

### Erreurs courantes VirtualBox

| Erreur | Cause | Solution |
|---|---|---|
| "Aucun périphérique USB disponible" dans les paramètres USB | Extension Pack non installé ou version non correspondante | Installer la version correspondante de l'Extension Pack |
| Adaptateur non capturé / non visible dans lsusb | Utilisateur non présent dans le groupe `vboxusers` (hôte Linux) | `sudo usermod -aG vboxusers $USER`, puis déconnexion/reconnexion |
| "Le périphérique USB est occupé par une requête précédente" | Un autre processus sur l'hôte utilise le périphérique | Débrancher et rebrancher l'adaptateur avant de démarrer la VM |
| Le périphérique se déconnecte sans cesse dans la VM | Contrôleur USB 3.0 non activé ; VM utilisant l'OHCI | Passer au contrôleur USB 3.0 (xHCI) dans Configuration → USB |
| Filtre ajouté mais périphérique non capturé auto | Filtre créé avant l'installation de l'Extension Pack | Supprimer et rajouter le filtre après avoir installé l'Extension Pack |

---

## Passthrough USB VMware Workstation / VMware Fusion

VMware gère le passthrough USB différemment de VirtualBox. Il n'y a pas d'extension séparée à installer — le support USB 2.0 et 3.0 est intégré dans VMware Workstation 17+ et Fusion 13+. Le mécanisme principal est le **service d'arbitrage USB**, qui surveille les événements USB de l'hôte et route les périphériques vers les VM.

### Connecter l'adaptateur via le menu Périphériques

Lorsque vous branchez votre adaptateur ALFA alors qu'une VM est en cours d'exécution, VMware affiche généralement une fenêtre contextuelle demandant quelle VM doit posséder le périphérique. Si vous manquez la fenêtre :

1. Avec la VM Kali en cours d'exécution, allez dans **VM → Périphériques amovibles** dans la barre de menu.
2. Développez la liste, localisez votre adaptateur ALFA (ex: **Realtek 802.11ac NIC**).
3. Cliquez sur **Connecter (Déconnecter de l'hôte)**.

Le périphérique se déconnectera du système d'exploitation hôte et deviendra exclusivement disponible pour la VM.

### VMware Fusion (macOS)

Sur macOS avec VMware Fusion :

1. Allez dans **Machine virtuelle → USB et Bluetooth**.
2. Localisez l'adaptateur ALFA dans la liste.
3. Basculez la connexion sur **Connecter à Linux** (ou le nom de votre VM Kali).

Alternativement, dans les réglages de la VM de Fusion sous **USB et Bluetooth**, activez **Connecter automatiquement les nouveaux périphériques USB** pour que Fusion passe les périphériques à la VM active sans demander.

### Vérifier et charger le pilote

Une fois connecté, vérifiez dans Kali :

```bash
lsusb
```

Chargez ensuite le pilote approprié comme décrit dans la section VirtualBox ci-dessus (les étapes 3.6 et 3.7 s'appliquent de manière identique).

### Vérifier le service d'arbitrage USB VMware

Si l'adaptateur ALFA n'apparaît pas dans le menu **Périphériques amovibles**, le service d'arbitrage USB n'est peut-être pas en cours d'exécution. Sur les hôtes Linux :

```bash
sudo systemctl status vmware-usbarbitrator
```

S'il est arrêté :

```bash
sudo systemctl start vmware-usbarbitrator
sudo systemctl enable vmware-usbarbitrator
```

Sur les hôtes Windows, ouvrez les **Services** (`services.msc`), localisez **Service d'arbitrage USB VMware**, et réglez-le sur **Automatique (début)**.

### Activer l'USB 3.0 dans VMware

Pour l'AWUS036AXML et d'autres périphériques USB 3.0, vérifiez que la version matérielle de votre VM prend en charge l'xHCI. Ouvrez le fichier `.vmx` de votre VM Kali (situé dans le dossier de la VM) et confirmez ou ajoutez :

```
usb_xhci.present = "TRUE"
```

Dans l'interface graphique de VMware Workstation : **VM → Paramètres → Contrôleur USB**, et sélectionnez **USB 3.1** dans la liste déroulante. La VM doit être éteinte pour modifier ce réglage.

{{< alert "triangle-exclamation" >}}
La version matérielle VMware 14 ou plus récente est requise pour le support USB 3.0 (xHCI). Si votre VM a été créée avec une version matérielle plus ancienne, mettez-la à jour via **VM → Gérer → Changer la compatibilité matérielle**.
{{< /alert >}}

### Erreurs courantes VMware

| Erreur | Cause | Solution |
|---|---|---|
| L'adaptateur n'est pas dans le menu Périphériques amovibles | L'arbitre USB n'est pas lancé | Démarrer le service `vmware-usbarbitrator` |
| Le périphérique se connecte puis se déconnecte aussitôt | Le pilote de l'hôte reprend le périphérique | Désactiver le pilote WiFi de l'hôte pour l'adaptateur, ou débrancher/rebrancher plus vite |
| "Périphérique déjà utilisé par l'hôte" | L'hôte a réclamé le périphérique | Éjecter de l'hôte (ex: désactiver l'adaptateur réseau hôte) avant de connecter dans la VM |
| Pas de vitesse USB 3.0 dans la VM | Version matérielle VM < 14 ou xHCI non activé | Mettre à jour la version matérielle, ajouter `usb_xhci.present = "TRUE"` au .vmx |
| Le mode moniteur échoue même après le passthrough | Pilote incorrect ou manquant dans Kali | Suivre le [Guide d'installation du pilote](/fr/blog/install-alfa-driver-kali-ubuntu/) |

---

## Notes spécifiques aux adaptateurs

### AWUS036ACH (RTL8812AU)

L'AWUS036ACH est un périphérique **USB 2.0** et l'un des adaptateurs les mieux testés dans les environnements de VM. VirtualBox et VMware le gèrent tous deux de manière fiable.

- Contrôleur USB : l'USB 2.0 (EHCI) ou l'USB 3.0 (xHCI) fonctionnent tous deux très bien.
- Paquet de pilote : `realtek-rtl88xxau-dkms` (disponible dans les dépôts Kali). Nom du module : `88XXau`.
- Sur certains noyaux récents (6.x), le paquet DKMS peut nécessiter un patch. Consultez la page GitHub [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) pour l'état le plus récent.
- Le mode moniteur et l'injection de paquets sont très stables en passthrough VM.

Vous pouvez trouver cet adaptateur dans notre boutique : [ALFA AWUS036ACH](/fr/products/alfa/awus036ach/).

### AWUS036AXML (MT7921AUN)

L'AWUS036AXML est un périphérique **USB 3.0** prenant en charge le WiFi 6E. Elle est plus récente et présente quelques cas particuliers dans les environnements de VM.

- Contrôleur USB : **doit** utiliser l'USB 3.0 (xHCI). Le passthrough USB 2.0 fait fonctionner le périphérique avec des capacités réduites et peut provoquer des échecs de chargement du firmware.
- Pilote : `mt7921u` est dans le noyau principal (5.18+). Kali 2024.x l'inclut. Paquet de firmware : `firmware-misc-nonfree`.
- **Problème connu** : Certaines premières unités AWUS036AXML subissent des gels périodiques sous l'arbitrage USB 3.0 de VirtualBox. Si vous voyez l'interface disparaître et réapparaître dans `ip link`, essayez de passer le contrôleur USB de VirtualBox en USB 2.0 comme étape de diagnostic. Si cela stabilise la situation, il s'agit d'un problème d'arbitrage xHCI de VirtualBox plutôt que d'un problème de pilote.
- VMware Workstation a tendance à gérer l'AWUS036AXML de manière plus fiable que VirtualBox pour le passthrough USB 3.0.

Test complet : [Test de l'AWUS036AXML WiFi 6E](/fr/blog/awus036axml-wifi-6e-review/).

### AWUS036ACM (MT7612U, Double Antenne)

L'AWUS036ACM utilise le chipset MediaTek MT7612U avec un pilote intégré au noyau (`mt76x2u`, intégré depuis le noyau 4.19). Aucune installation de pilote n'est nécessaire — une fois le passthrough configuré, l'adaptateur est prêt à l'emploi (plug-and-play) dans la VM. Si le module ne se charge pas automatiquement, lancez `sudo modprobe mt76x2u`. L'AWUS036ACM possède deux ports d'antenne RP-SMA.

---

## Conseils de performance

Faire entrer l'adaptateur dans la VM est la première étape. Obtenir des performances stables pendant les sessions réelles de pentest ou de capture nécessite quelques étapes d'optimisation supplémentaires.

**Utilisez le bon type de filtre USB.** Pour l'AWUS036AXML, utilisez toujours un filtre USB 3.0 dans VirtualBox (assurez-vous que le contrôleur xHCI est sélectionné). Un filtre USB 2.0 sur un périphérique USB 3.0 forcera le périphérique à négocier à la vitesse USB 2.0, divisant par deux le débit.

**Désactivez l'autosuspend USB sur l'hôte.** Les hôtes Linux peuvent suspendre agressivement le périphérique USB, faisant perdre l'accès à la VM. Désactivez cela au niveau de l'hôte :

```bash
echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend
```

Pour que cela persiste après les redémarrages, ajoutez-le à `/etc/rc.local` ou créez une règle udev.

**Allouez des ressources VM adéquates.** Les charges de travail d'injection et de capture de paquets sont gourmandes en CPU. Allouez au minimum :
- **2 cœurs de CPU** (4 recommandés pour les outils parallèles comme `hcxdumptool` + `hashcat`)
- **2 Go de RAM** (4 Go si vous utilisez un bureau Kali complet avec des outils graphiques)

**Prenez un snapshot de la VM avant les engagements.** Avant de commencer toute session de pentest, faites un snapshot de votre VM Kali. Si un crash de pilote ou une mise à jour de firmware corrompt votre installation, revenir au snapshot vous ramène à un état connu fonctionnel en quelques secondes.

**Gardez l'adaptateur au frais.** Les adaptateurs ALFA avec des antennes à gain élevé génèrent de la chaleur lors d'injections prolongées. Dans une VM, l'OS hôte peut brider le périphérique USB s'il détecte des problèmes thermiques ou de puissance. Utilisez l'adaptateur dans un environnement bien ventilé.

{{< alert "circle-info" >}}
Pour les sessions de capture de plus de 30 minutes, envisagez d'utiliser un hub USB alimenté entre l'adaptateur et votre hôte. Il fournit une alimentation stable et évite les chutes de tension qui peuvent provoquer la déconnexion de l'adaptateur lors de captures critiques.
{{< /alert >}}

---

## Bare Metal vs VM : Comparaison honnête

Les machines virtuelles introduisent une couche de complexité entre votre adaptateur et le noyau. Voici une évaluation honnête pour les professionnels de la sécurité qui prennent des décisions d'infrastructure :

| Caractéristique | Kali en Bare Metal | VirtualBox + Kali | VMware + Kali |
|---|---|---|---|
| **Support pilote** | Complet, direct | Bon (avec Extension Pack) | Bon (USB intégré) |
| **Stabilité mode moniteur** | Excellente | Bonne | Bonne–Excellente |
| **Fiabilité injection paquets** | Excellente | Bonne (pertes de trames occasionnelles) | Bonne–Excellente |
| **Débit USB 3.0** | Pleine vitesse | Presque pleine | Presque pleine |
| **Temps d'installation** | Élevé (matériel dédié) | Bas–Moyen | Bas–Moyen |
| **Portabilité** | Basse (machine dédiée) | Haute (snapshots, portabilité) | Haute |
| **Surcharge ressources** | Aucune | Moyenne | Basse–Moyenne |
| **Usage CTF / labo** | Trop | Idéal | Idéal |
| **Engagements pro** | Recommandé | Acceptable | Acceptable |

**Conclusion :** Pour les compétitions CTF, la pratique en laboratoire et les environnements d'apprentissage, une VM avec un passthrough USB correct est pratique et capable. Pour les missions professionnelles de test d'intrusion où la fiabilité et l'intégrité forensique comptent, un ordinateur portable Kali dédié ou une installation en bare-metal est le choix le plus fiable. La perte de trames et les hoquets occasionnels d'arbitrage USB dans les VM peuvent affecter la fiabilité des attaques sensibles au temps comme la capture PMKID ou le flooding de désauthentification.

---

## Référence rapide de dépannage

| Symptôme | Cause la plus probable | Solution |
|---|---|---|
| `lsusb` ne montre rien dans Kali | Passthrough USB non configuré | Ajouter un filtre USB (VBox) ou connecter via Périphériques amovibles (VMware) |
| "Aucun périphérique USB" dans les paramètres VirtualBox | Extension Pack manquant ou version non correspondante | Installer la version correspondante de l'Extension Pack |
| Adaptateur visible dans `lsusb` mais pas d'interface `wlan` | Pilote non chargé | `sudo modprobe 88XXau` ou `sudo modprobe mt7921u` |
| `modprobe: FATAL: Module 88XXau not found` | Paquet DKMS non installé | `sudo apt install realtek-rtl88xxau-dkms` |
| L'interface apparaît puis disparaît | Autosuspend USB ou arbitrage xHCI VBox | Désactiver l'autosuspend ; essayer le contrôleur USB 2.0 pour ACH |
| `airmon-ng` démarre mais le mode moniteur échoue silencieusement | Mauvais pilote ou conflit avec le gestionnaire de réseau | `sudo airmon-ng check kill`, puis réessayer |
| Le filtre USB VirtualBox ne capture pas au démarrage | Filtre ajouté avant l'Extension Pack | Supprimer le filtre, installer l'Extension Pack, rajouter le filtre |
| VMware perd le périphérique lors de longues sessions | Le service d'arbitrage USB VMware s'arrête | Réactiver et régler sur démarrage automatique |

---

## Étapes suivantes

Avec le passthrough USB configuré et le mode moniteur vérifié, vous êtes prêt à continuer :

- **Installer ou mettre à jour le pilote :** [Guide d'installation du pilote ALFA pour Kali & Ubuntu](/fr/blog/install-alfa-driver-kali-ubuntu/)
- **Guide complet de configuration de l'AWUS036ACH :** [Guide d'installation de l'AWUS036ACH sous Kali Linux](/fr/blog/awus036ach-kali-linux-setup/)
- **Test matériel de l'AWUS036AXML :** [Test de l'AWUS036AXML WiFi 6E](/fr/blog/awus036axml-wifi-6e-review/)

Si vous hésitez encore sur l'adaptateur à acheter pour du pentesting basé sur VM, l'AWUS036ACH reste le choix le plus fiable en raison de son comportement mature en passthrough USB 2.0 et de son pilote éprouvé sur le terrain. L'AWUS036AXML est plus performante une fois que tout fonctionne, mais nécessite une configuration USB 3.0 plus minutieuse.
