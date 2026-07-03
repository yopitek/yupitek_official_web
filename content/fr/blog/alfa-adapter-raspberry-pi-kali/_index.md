---
title: "Adaptateur WiFi ALFA sur Raspberry Pi avec Kali Linux : Guide d'installation"
description: "Installez les adaptateurs WiFi USB ALFA sur Raspberry Pi fonctionnant sous Kali Linux ARM64. Couvre la compilation du pilote RTL8812AU pour l'AWUS036ACH, le mode moniteur et la configuration de test de pénétration portable."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["raspberry-pi", "kali-linux", "alfa-network", "AWUS036ACH", "RTL8812AU", "portable-pentest", "monitor-mode"]
featureimage: "/images/blog/alfa-adapter-raspberry-pi-kali.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Quel Raspberry Pi convient le mieux au pentesting ?"
    answer: "Le Raspberry Pi 5 (4 Go ou 8 Go) est le meilleur choix. Le Pi 4 (4 Go+) fonctionne aussi correctement. Le Pi 3B+ n'est pas assez rapide pour la capture de paquets en temps réel."
  - question: "L'AWUS036ACH nécessite-t-il une compilation de pilote sur Raspberry Pi ?"
    answer: "Oui. Le RTL8812AU n'est pas dans le noyau mainline. Essayez d'abord le paquet DKMS realtek-rtl88xxau-dkms de Kali, sinon compilez manuellement depuis aircrack-ng avec les flags ARM64."
  - question: "Peut-on utiliser wlan0 pour le mode moniteur sur un Pi headless ?"
    answer: "Non recommandé. wlan0 est le WiFi intégré du Pi utilisé pour SSH. airmon-ng check kill coupera SSH. Utilisez wlan1 (carte ALFA) et maintenez la connexion via Ethernet ou tmux."
  - question: "L'AWUS036AXM est-il plug-and-play sur Raspberry Pi ?"
    answer: "Oui. Le pilote MT7921AUN est intégré au noyau depuis 5.18. Installez simplement le paquet firmware-misc-nonfree."
  - question: "Comment alimenter l'AWUS036ACH sur Raspberry Pi ?"
    answer: "L'AWUS036ACH consomme environ 500 mW. Utilisez impérativement un hub USB 3.0 alimenté avec une alimentation USB-C Pi officielle 3A+."
---

{{< tldr >}}
Un Raspberry Pi 4/5 avec Kali Linux ARM64 et une carte ALFA constitue une plateforme de pentesting de poche. L'AWUS036ACH nécessite la compilation du pilote RTL8812AU, tandis que l'AWUS036ACM et l'AWUS036AXM sont plug-and-play. Un hub USB alimenté est indispensable.
{{< /tldr >}}

Un ordinateur portable fonctionnant sous Kali Linux est la station de travail de test de pénétration standard — mais c'est loin d'être la seule option. Un Raspberry Pi 4 ou Pi 5 associé à un adaptateur WiFi USB ALFA vous offre une plateforme compacte, sans ventilateur et à refroidissement passif qui tient dans une poche de veste, fonctionne sur une batterie externe USB-C et peut être laissée sans surveillance dans un environnement cible pendant des heures. Les images Kali Linux ARM64 sont fournies directement par Offensive Security et fonctionnent nativement sur le Pi 4 et le Pi 5 sans émulation, vous donnant accès à l'ensemble des outils : Aircrack-ng, Kismet, Wireshark, Bettercap et le reste des métapaquets Kali standard.

Le principal obstacle est le pilote. Le chipset RTL8812AU à l'intérieur de l'AWUS036ACH n'est pas dans le noyau principal (mainline), ce qui signifie que vous ne pouvez pas brancher l'adaptateur et espérer qu'il fonctionne immédiatement. Vous devez compiler le pilote pour votre noyau ARM64 en cours d'exécution — et les drapeaux de compilation diffèrent de ceux pour x86-64. Ce guide vous accompagne à chaque étape.

---

## Matériel recommandé

Toutes les combinaisons de modèle de Pi, d'adaptateur et d'alimentation ne fonctionnent pas de manière fiable. Le tableau ci-dessous reflète ce qui fonctionne bien et les compromis à prévoir.

| Composant | Recommandé | Notes |
|---|---|---|
| Nano-ordinateur | Raspberry Pi 5 (4 Go ou 8 Go) | Le Pi 4 (4 Go+) fonctionne bien ; le Pi 3B+ est trop lent pour les captures en temps réel |
| Adaptateur principal | ALFA AWUS036ACH | Chipset RTL8812AU ; meilleur support de pilote ARM ; bi-bande AC1200 |
| Adaptateur alternatif | ALFA AWUS036ACM | Chipset MT7612U ; pilote intégré au noyau (mt76x2u) ; prêt à l'emploi sur Kali ARM64 |
| Adaptateur WiFi 6 | ALFA AWUS036AXM ou AXML | Chipset MT7921AUN ; natif dans le noyau depuis 5.18 ; nécessite firmware-misc-nonfree |
| Hub USB | Hub USB 3.0 alimenté | L'AWUS036ACH consomme ~500 mW ; peut provoquer des baisses de tension sur les ports USB du Pi sans hub |
| Stockage | MicroSD 32 Go+ (Classe 10 / A2) | Les cartes classées A2 offrent un démarrage et des opérations apt nettement plus rapides |
| Alimentation | Alimentation officielle Pi USB-C (≥ 3 A) | Les adaptateurs tiers sont une source courante de problèmes de stabilité |

{{< alert "triangle-exclamation" >}}
L'AWUS036ACH est un périphérique USB à haute consommation de courant. Le brancher directement sur un Raspberry Pi 4 ou Pi 5 sans hub USB alimenté peut provoquer un ralentissement (throttling) du Pi ou son redémarrage sous charge. Utilisez toujours un hub alimenté lors de l'utilisation de l'AWUS036ACH aux côtés d'autres périphériques USB.
{{< /alert >}}

---

## Installation de Kali Linux ARM64 sur Raspberry Pi

### Télécharger l'image ARM

Kali Linux maintient des images ARM64 de première main pour Raspberry Pi sur [https://www.kali.org/get-kali/#kali-arm](https://www.kali.org/get-kali/#kali-arm). Téléchargez l'image étiquetée **Raspberry Pi 4 (64-bit)** ou **Raspberry Pi 5 (64-bit)**. N'utilisez pas l'image 32 bits — le noyau ARM64 est requis pour les étapes de construction du pilote dans ce guide.

### Flasher sur la MicroSD

Vous pouvez flasher avec l'outil graphique Raspberry Pi Imager ou `dd` depuis la ligne de commande :

```bash
# Remplacez /dev/sdX par votre périphérique de carte SD réel (vérifiez avec lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Avec Raspberry Pi Imager, sélectionnez **Utiliser personnalisé** → choisissez le fichier Kali `.img.xz` → sélectionnez votre carte SD → écrire.

### Premier démarrage et configuration initiale

Insérez la carte SD, connectez un moniteur et un clavier (ou configurez d'abord un accès sans écran via une console série), et mettez sous tension. Les identifiants par défaut sont :

- **Nom d'utilisateur :** `kali`
- **Mot de passe :** `kali`

Après vous être connecté, lancez `kali-tweaks` et suivez les invites pour sécuriser la configuration par défaut. Ensuite, mettez le système à jour complètement avant de toucher aux pilotes :

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

{{< alert "circle-info" >}}
Si vous prévoyez d'accéder au Pi via SSH plutôt qu'avec un clavier et un moniteur, activez le SSH avant le premier démarrage en plaçant un fichier vide nommé `ssh` dans la partition `/boot` de la carte SD. C'est le même mécanisme que pour le système d'exploitation Raspberry Pi standard.
{{< /alert >}}

---

## Installation du pilote RTL8812AU sur Kali ARM64 (AWUS036ACH)

Le pilote RTL8812AU n'est pas inclus dans le noyau Linux principal. Sur ARM64, vous devez soit compiler à partir des sources, soit installer la version DKMS packagée par Kali. Les deux voies sont couvertes ci-dessous — commencez par l'approche par paquet et ne vous repliez sur la construction manuelle que si vous rencontrez des incompatibilités de version de noyau.

### Option 1 : Paquet Kali (Point de départ recommandé)

Kali Linux propose une version packagée DKMS du pilote RTL8812AU qui gère automatiquement la recompilation à chaque mise à jour du noyau.

```bash
sudo apt install realtek-rtl88xxau-dkms
```

Après l'installation, redémarrez et vérifiez que le module est chargé :

```bash
sudo modprobe 88XXau
ip link show
```

Si vous voyez une interface `wlan1` (en supposant que `wlan0` est l'adaptateur intégré du Pi), le pilote fonctionne. Ce paquet peut avoir quelques semaines de retard sur la source GitHub, mais c'est le point de départ avec le moins de friction.

{{< alert "circle-info" >}}
Le paquet Kali est généralement suffisant pour la plupart des configurations ARM64. Ne procédez à la construction manuelle ci-dessous que si le paquet DKMS ne parvient pas à compiler pour votre version actuelle du noyau, que vous pouvez vérifier avec `uname -r`.
{{< /alert >}}

### Option 2 : Construction manuelle à partir des sources (ARM64)

Si le paquet DKMS échoue — le plus souvent parce que votre noyau est plus récent que la dernière version testée du paquet — construisez directement à partir du fork Aircrack-ng sur GitHub. C'est la source faisant autorité pour le support ARM64.

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)

git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# Changer les drapeaux de plateforme de x86 à ARM64
sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/' Makefile
sed -i 's/CONFIG_PLATFORM_ARM64_RPI = n/CONFIG_PLATFORM_ARM64_RPI = y/' Makefile

sudo make dkms_install
```

Les commandes `sed` constituent la différence critique par rapport à une construction x86-64. Sans elles, le Makefile utilise par défaut les chemins de plateforme x86 et le module résultant ne se chargera pas sur ARM64.

Après une construction réussie, chargez le module et vérifiez :

```bash
sudo modprobe 88XXau
ip link show
```

Vous devriez voir une nouvelle interface — typiquement `wlan1` — listée. Si `ip link show` affiche l'interface, le pilote fonctionne correctement.

---

## MT7921AUN sur Raspberry Pi (AWUS036AXM / AXML)

Le chipset MediaTek MT7921AUN utilisé dans les adaptateurs AWUS036AXM et AXML est présent dans le noyau principal depuis la version 5.18. Les images Kali Linux ARM64 sont livrées avec un noyau bien au-dessus de ce seuil, ce qui signifie que le pilote se charge automatiquement lorsque vous branchez l'adaptateur — aucune compilation n'est nécessaire.

La seule étape supplémentaire est l'installation du micrologiciel (firmware) propriétaire dont l'MT7921AUN a besoin :

```bash
sudo apt install firmware-misc-nonfree
sudo reboot
```

Après le redémarrage, vérifiez que l'adaptateur est détecté et que l'interface est active :

```bash
lsusb
sudo modprobe mt7921u
ip link show
```

Si `lsusb` affiche un périphérique MediaTek et `ip link show` liste une nouvelle interface sans fil, l'adaptateur est prêt. Le support du mode moniteur sur l'MT7921AUN s'est considérablement amélioré depuis le noyau 5.18 mais peut être moins fiable que les adaptateurs basés sur RTL8812AU pour certains tests d'injection de paquets. Pour une compatibilité maximale avec les anciens flux de travail de test de pénétration, l'AWUS036ACH reste le choix le plus solide.

---

## Activation du mode moniteur sur Raspberry Pi

Le Raspberry Pi possède une interface WiFi intégrée (`wlan0`). Gardez-la connectée à votre réseau pour l'accès SSH. Utilisez l'adaptateur ALFA (`wlan1`) exclusivement pour le mode moniteur et la capture de paquets. Ne mettez jamais `wlan0` en mode moniteur sur un Pi sans écran — vous perdriez votre connexion SSH.

```bash
# Tuer les processus qui entrent en conflit avec le mode moniteur (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# Activer le mode moniteur sur l'interface de l'adaptateur ALFA
sudo airmon-ng start wlan1

# Vérifier que le mode moniteur est actif
sudo iwconfig wlan1mon

# Commencer la capture sur tous les canaux
sudo airodump-ng wlan1mon
```

{{< alert "circle-info" >}}
`airmon-ng start wlan1` crée une nouvelle interface appelée `wlan1mon`. Exécutez toujours les outils suivants sur `wlan1mon`, pas `wlan1`. Vous pouvez confirmer le nom de l'interface avec `iwconfig` ou `ip link show`.
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
L'exécution de `airmon-ng check kill` arrête NetworkManager et wpa_supplicant. Si vous êtes connecté via SSH via `wlan0`, cela coupera également votre session SSH. Pour les configurations sans écran, connectez-vous via Ethernet ou une deuxième interface filaire avant d'exécuter ces commandes, ou utilisez `tmux` pour que votre session survive à une déconnexion.
{{< /alert >}}

Pour désactiver le mode moniteur et restaurer le mode géré :

```bash
sudo airmon-ng stop wlan1mon
sudo systemctl start NetworkManager
```

---

## Conseils pour une configuration de test portable

Faire fonctionner le matériel n'est que la moitié du travail. Ces choix pratiques font la différence entre un kit de terrain stable et un tas de câbles frustrant.

**Architecture réseau :** Utilisez `wlan0` (le WiFi intégré du Pi) pour maintenir votre connexion de gestion — connectez-vous en SSH au Pi depuis un ordinateur portable sur le même réseau local ou hotspot. Dédiez `wlan1` (l'adaptateur ALFA) entièrement à l'activité de test de pénétration. Ne mélangez jamais les deux rôles.

**Fonctionnement sans écran :** Évitez de connecter un clavier, une souris et un moniteur sur le terrain. Configurez le SSH dès le premier démarrage, et accédez à tout via un émulateur de terminal sur votre ordinateur portable. Les sessions `tmux` persistent après les reconnexions, ce qui est inestimable lorsque les conditions de réseau sont instables.

**Alimentation :** Utilisez l'alimentation officielle Raspberry Pi USB-C de 3 A minimum. Pour l'AWUS036ACH, ajoutez un hub USB alimenté de 2,5 A ou plus. Une batterie externe USB-C de qualité (65 W+) peut alimenter simultanément le Pi, le hub et l'adaptateur pendant 4 à 6 heures selon la charge.

**Stockage :** Écrivez les journaux Kismet et les fichiers de capture sur un SSD USB plutôt que sur la carte MicroSD. Les cartes MicroSD ont des cycles d'écriture limités et se dégradent rapidement sous des charges de travail de journalisation soutenues. Un SSD USB 3.0 attaché au hub alimenté est plus rapide et plus durable.

**Boîtier :** Sélectionnez un boîtier Pi avec des ports USB ouverts ou des découpes permettant d'accueillir le hub alimenté. Les boîtiers en aluminium avec des ailettes de dissipateur thermique passives aident à gérer la température lors de captures prolongées.

---

## Exécution de Kismet sur Raspberry Pi

Kismet est un scanner WiFi passif qui fonctionne comme un serveur d'arrière-plan et expose une interface utilisateur Web basée sur un navigateur. Il est bien adapté aux déploiements de Pi sans écran : vous laissez le Pi fonctionner et vérifiez l'interface Web depuis n'importe quel appareil sur le même réseau.

```bash
sudo apt install kismet

# Lancer Kismet en utilisant l'adaptateur ALFA en mode moniteur
kismet -c wlan1
```

{{< alert "circle-info" >}}
Kismet mettra lui-même l'interface en mode moniteur si vous passez directement le nom de l'interface. Vous n'avez pas besoin d'exécuter `airmon-ng start` avant de lancer Kismet. Kismet gère le cycle de vie de l'interface en interne.
{{< /alert >}}

Une fois lancé, accédez à l'interface utilisateur Web de Kismet depuis n'importe quel navigateur de votre réseau :

```
http://raspberrypi.local:2501
```

Lors de la première exécution, Kismet vous invite à créer un nom d'utilisateur et un mot de passe administrateur. Après vous être connecté, vous pouvez visualiser les réseaux détectés, les clients associés, l'historique de la force du signal et les données GPS si un dongle GPS est connecté.

Kismet enregistre tout dans des fichiers de base de données `.kismet` dans `~/.kismet/` par défaut. Ceux-ci peuvent être exportés plus tard pour analyse ou téléchargement sur WiGLE.

---

## Cas d'utilisation : Configuration de wardriving

Un Raspberry Pi faisant fonctionner Kismet avec un adaptateur ALFA et un dongle GPS constitue un kit de wardriving complet et autonome — plus petit et moins cher que n'importe quel appareil de wardriving dédié.

**Composants requis :**
- Raspberry Pi 4 ou Pi 5
- ALFA AWUS036ACH
- Dongle USB GPS (les chipsets u-blox fonctionnent bien avec Kismet)
- Hub USB alimenté
- Batterie externe USB-C (65 W+, avec charge pass-through)

**Étapes de configuration :**

1. Installez Kismet et les paquets GPS :

```bash
sudo apt install kismet gpsd gpsd-clients
```

2. Configurez `gpsd` pour lire à partir de votre dongle GPS :

```bash
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
```

3. Démarrez Kismet avec le support GPS :

```bash
kismet -c wlan1 --gps=gpsd:host=localhost,port=2947
```

4. Montez le Pi, le hub, l'adaptateur et la batterie dans un sac ou un boîtier et placez-le dans votre véhicule. Accédez à l'interface Web de Kismet depuis le hotspot de votre téléphone ou une tablette connectée au même réseau WiFi que le Pi.

Kismet enregistre les coordonnées GPS pour chaque réseau détecté. Exportez la base de données `.kismet` au format CSV WiGLE en utilisant `kismetdb_to_wigle` (inclus avec Kismet) et téléchargez-la sur WiGLE pour la cartographie.

{{< alert "triangle-exclamation" >}}
Conformez-vous toujours aux lois locales avant de mener toute activité de balayage réseau. Dans de nombreuses juridictions, le wardriving avec balayage passif uniquement est légal ; le sondage actif ou la connexion à des réseaux sans autorisation ne l'est pas. Connaissez vos réglementations locales.
{{< /alert >}}

---

{{< faq >}}

## Lectures complémentaires

Pour le guide complet d'installation du pilote RTL8812AU sur Kali Linux et Ubuntu (bureau), consultez notre guide [Installer le pilote ALFA sur Kali Linux & Ubuntu](/fr/blog/install-alfa-driver-kali-ubuntu/). Si vous hésitez encore sur l'adaptateur à acheter, le [Guide d'achat d'adaptateurs WiFi ALFA 2026](/fr/blog/alfa-wifi-adapter-buyer-guide-2026/) couvre chaque modèle actuel avec les détails du chipset et les recommandations d'utilisation.

---

## Références
1. [Téléchargement officiel Kali Linux ARM](https://www.kali.org/get-kali/#kali-arm)
2. [Projet pilote aircrack-ng rtl8812au](https://github.com/aircrack-ng/rtl8812au)
3. [Site officiel Raspberry Pi](https://www.raspberrypi.com/)
4. [Documentation pilote mt76 du noyau Linux](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
5. [Site officiel ALFA Network](https://www.alfa.com.tw/)
