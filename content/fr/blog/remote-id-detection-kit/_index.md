---
title: "ALFA AWUS036ACH × Raspberry Pi : Kit de détection Remote ID standard pour drones – Guide complet (2026)"
description: "Construis un kit de détection Remote ID passif et légal avec l'ALFA AWUS036ACH et un Raspberry Pi. Couvre l'analyse du standard ASTM F3411, la liste du matériel, la configuration pas à pas, et une clarification technique entre DJI OcuSync et le RID standard."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["Remote-ID", "ALFA-Network", "AWUS036ACH", "détection-drone", "Counter-UAV", "ASTM-F3411", "EN-4709-002", "opendroneid", "unix_rid_capture", "DJI-OcuSync", "Raspberry-Pi"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "Pourquoi l'AWUS036ACH est-il le premier choix plutôt que des adaptateurs Wi-Fi 6/6E plus récents ?"
    answer: "La capture Remote ID nécessite un mode monitor stable et une injection de paquets bruts. La branche de pilotes communautaire la plus mature est actuellement Realtek rtl88xxau (RTL8812AU / RTL8814AU). Les chipsets Wi-Fi 6/6E (MediaTek MT7921AUN, Realtek RTL8832BU) n'ont pas de pilotes d'injection dans la chaîne d'outils de pénétration/sniffing grand public. L'AWUS036ACH est doublement vérifié par la communauté et par ce kit."
  - question: "Le nRF52840 est-il obligatoire ?"
    answer: "Pour le Wi-Fi Remote ID uniquement (NAN / Beacon), non — l'AWUS036ACH suffit. Pour capturer simultanément les diffusions Bluetooth 5 Long Range, tu as besoin du nRF52840 (flashé avec le firmware sniffer). Nous recommandons d'inclure ce module pour une couverture complète."
  - question: "Ce kit peut-il décoder les drones DJI ?"
    answer: "Il traite les diffusions Remote ID Wi-Fi/BT standard de DJI. Cependant, le DroneID OcuSync propriétaire de DJI ne fait pas partie du protocole standard — l'adaptateur ALFA ne peut pas le décoder. Tu auras besoin d'un SDR séparé (ANTSDR / HackRF) avec un plugin Kismet. Les deux peuvent être déployés côte à côte."
  - question: "Quelle génération de Raspberry Pi dois-je utiliser ?"
    answer: "Le Raspberry Pi 4 (2 Go+) offre le meilleur équilibre. Le Pi 3B a été validé par l'auteur d'unix_rid_capture lors de ses tests. Le Pi 5 fonctionne aussi (surveille le refroidissement et l'alimentation). Le WiFi intégré du Pi ne peut pas passer de manière fiable en mode monitor — un AWUS036ACH externe est nécessaire."
  - question: "La réception passive est-elle légale ?"
    answer: "La réception des informations Remote ID diffusées publiquement par les drones est légale — équivalent à la lecture d'informations publiquement accessibles. Le brouillage actif (jamming) est en revanche strictement réglementé et ne fait pas partie de ce kit."
---
> Équipe technique Yupitek | Distributeur officiel ALFA Network, Taïwan

{{< tldr >}}
Le kit de détection Remote ID utilise le mode monitor de l'adaptateur **ALFA AWUS036ACH** pour recevoir passivement les informations d'identité et de position que les drones sont légalement tenus de diffuser — considère-le comme un « lecteur de plaques d'immatriculation » pour l'espace aérien. Il offre aux gestionnaires de sécurité un outil de connaissance situationnelle légal et peu coûteux.
{{< /tldr >}}

---

## 1. Pourquoi tu as besoin d'un kit de détection Remote ID

La réglementation des drones dans le monde entier est entrée dans l'ère de l'« identité diffusée ». Les normes exigent que les drones diffusent en continu les informations suivantes pendant le vol :

| Champ diffusé | Description |
|---|---|
| ID UAS / opérateur | Numéro de série ou code d'enregistrement |
| Position actuelle (latitude, longitude, altitude) | WGS-84 / altitude barométrique |
| Vitesse et cap | Vitesse horizontale / verticale |
| Position de l'opérateur | Point de décollage ou position actuelle |

La diffusion utilise deux types de porteuses radio :

- **Bluetooth** : BT4 Legacy Advertising, BT5 Long Range (Extended Advertising)
- **Wi-Fi** : NAN (Wi-Fi Aware, 2,4 / 5 GHz), Beacon (2,4 / 5 GHz)

Pour les gestionnaires de sites dans les aéroports, les zones industrielles, les prisons et les grands événements, **recevoir passivement ces diffusions publiques** (essentiellement voir la « plaque d'immatriculation » d'un drone) est une approche conforme et peu coûteuse pour la connaissance situationnelle — aucune interférence active n'est nécessaire.

{{< alert "triangle-exclamation" >}}
**Note légale** : Toutes les méthodes décrites dans ce guide sont de la **réception passive de données diffusées publiquement**. Le brouillage actif (jamming) est strictement réglementé dans toutes les juridictions et ne fait ni partie de ce kit ni n'est recommandé.
{{< /alert >}}

---

## 2. Positionnement du produit : la voie open-source au risque le plus faible

Après avoir évalué plusieurs approches techniques, nous avons choisi une configuration centrée sur l'**ALFA AWUS036ACH** :

- L'AWUS036ACH utilise le chipset **Realtek RTL8812AU**, double bande 2,4 + 5 GHz (802.11ac), 2×2 MIMO, deux antennes RP-SMA détachables à gain élevé de 5 dBi, et une bande passante USB 3.0 amplement suffisante.
- Le pilote `rtl88xxau` maintenu par la communauté fournit un **mode monitor** stable et l'**injection de paquets bruts (raw packet injection)** — la condition préalable à la capture des trames Wi-Fi RID Beacon / NAN.
- Point crucial : le README de `sxjack/unix_rid_capture` **indique explicitement : « Testé avec un dongle WiFi basé sur rtl8812au, un dongle nRF52840 et un Raspberry Pi 3B »**. La communauté a déjà effectué la validation matérielle pour nous. Reproduire leur architecture pour un kit industrialisé est la voie au risque le plus faible.

---

## 3. Liste du matériel

| Élément | Modèle / Spécification | Rôle | Nécessité |
|---|---|---|---|
| **Adaptateur principal** | ALFA **AWUS036ACH** (RTL8812AU, double bande 2,4/5 GHz, USB 3.0, deux antennes RP-SMA 5 dBi) | Capture Wi-Fi Remote ID (mode monitor) | **Obligatoire** |
| Ordinateur monocarte | Raspberry Pi 4 (2 Go+ recommandé ; 3B / 5 fonctionnent aussi) | Hôte de calcul | **Obligatoire** |
| Stockage | microSD 16 Go+ (Samsung / SanDisk Endurance recommandé) | Disque système | **Obligatoire** |
| Capture Bluetooth 5 | **nRF52840** Dongle USB (flashé avec firmware sniffer, ex. Nordic Sniffer) | Capture Remote ID BT5 Long Range | Recommandé (optionnel) |
| Alimentation | 5 V / 3 A USB-C (bloc d'alimentation officiel Pi) | Alimentation | **Obligatoire** |
| Réseau | Câble Ethernet ou identifiants WiFi | Upload / gestion | **Obligatoire** |
| Amélioration d'antenne | ALFA **APA-M25** antenne directionnelle panneau | Portée de réception étendue, réjection du bruit ambiant | Optionnel |

> Note : Le projet communautaire `DroneAware` spécifiait à l'origine l'**AWUS036N (Ralink RT3070, 2,4 GHz mono-bande)**. Ce kit est mis à niveau vers l'**AWUS036ACH (double bande)** pour couvrir à la fois les méthodes de transmission Wi-Fi RID **NAN et Beacon** en 2,4 GHz et 5 GHz — couverture plus large et meilleure pérennité.

---

## 4. Liste logicielle

| Logiciel / Paquet | Objectif | Source |
|---|---|---|
| Raspberry Pi OS Lite (64-bit) | Système d'exploitation (headless) | raspberrypi.com |
| **Pilote rtl88xxau** | Pilote moniteur/injection RTL8812AU | [morrownr/8812au-20210629](https://github.com/morrownr/8812au-20210629) |
| `libpcap-dev`, `libbluetooth-dev`, `libncurses-dev` | Dépendances de compilation pour `unix_rid_capture` | APT |
| **opendroneid-core-c** | Bibliothèque C de codage/décodage des messages Open Drone ID (ASTM F3411 / EN 4709-002) | [opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| **unix_rid_capture** | Programme de capture RID Wi-Fi/BT Linux (sortie JSON) | [sxjack/unix_rid_capture](https://github.com/sxjack/unix_rid_capture) |
| DroneAware Node (optionnel) | Intégration en un clic à la carte communautaire en temps réel | [fduflyer/DroneAware-Node-Releases](https://github.com/fduflyer/DroneAware-Node-Releases) |
| Kismet + plugin ANTSDR (voie DJI) | Décodage du DroneID DJI OcuSync (nécessite un SDR) | [kismetwireless/kismet](https://github.com/kismetwireless/kismet) + [alphafox02/antsdr_dji_droneid](https://github.com/alphafox02/antsdr_dji_droneid) |

---

## 5. Liens des projets GitHub

```text
# Bibliothèque de décodage principale (codage/décodage des messages ASTM F3411 / EN 4709-002)
https://github.com/opendroneid/opendroneid-core-c

# Programme de capture Linux (logiciel principal de ce kit, validé sur rtl8812au + nRF52840 + RPi)
https://github.com/sxjack/unix_rid_capture

# Réseau de cartes communautaire en temps réel (installation en un clic, téléversement automatique vers droneaware.io)
https://github.com/fduflyer/DroneAware-Node-Releases

# Framework de détection sans fil (la voie DJI OcuSync nécessite un plugin SDR)
https://github.com/kismetwireless/kismet

# Pilote moniteur/injection RTL8812AU (requis pour l'AWUS036ACH)
https://github.com/morrownr/8812au-20210629
```

---

## 6. Configuration pas à pas

### Étape 1 — Flasher le système

Utilise **Raspberry Pi Imager** pour écrire **Raspberry Pi OS Lite (64-bit)**. Clique sur l'icône engrenage (paramètres avancés) :

- Nom d'hôte : `droneid-kit`
- Active SSH et définis les identifiants
- Saisis les identifiants WiFi (évite d'avoir à brancher un câble Ethernet ensuite)

### Étape 2 — Connecter et vérifier le matériel

Branche l'AWUS036ACH directement sur le port **USB 3.0** du Pi (bleu / marqué `SS`). Assure-toi que les deux antennes sont bien serrées. Après le démarrage, connecte-toi en SSH :

```bash
ssh <user>@droneid-kit.local
sudo -i
lsusb
```

Tu devrais voir :

```text
Bus 002 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter
```

### Étape 3 — Installer le pilote moniteur rtl88xxau

```bash
sudo apt update && sudo apt install -y dkms git bc
git clone https://github.com/morrownr/8812au-20210629.git
cd 8812au-20210629
sudo ./install-driver.sh
sudo reboot
```

### Étape 4 — Vérifier le mode monitor

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
iwconfig wlan0
```

La sortie doit afficher **`Mode:Monitor`**.

### Étape 5 — Installer les dépendances de compilation

```bash
sudo apt install -y git cmake libncurses-dev libpcap-dev \
  libbluetooth-dev libgps-dev libnl-genl-3-dev libgtest-dev build-essential
```

### Étape 6 — Compiler opendroneid-core-c

```bash
git clone --recursive https://github.com/opendroneid/opendroneid-core-c
cd opendroneid-core-c
mkdir build && cd build
cmake ../.
make -j
# Produit libopendroneid/libopendroneid.so et test/odidtest
```

### Étape 7 — Compiler unix_rid_capture

`unix_rid_capture` nécessite `opendroneid.c` / `opendroneid.h`. Copie-les depuis l'étape précédente :

```bash
cd ~
git clone https://github.com/sxjack/unix_rid_capture
cp opendroneid-core-c/libopendroneid/opendroneid.{c,h} unix_rid_capture/
cd unix_rid_capture
cmake .
make
```

### Étape 8 — Lancer la capture

Les privilèges root ou `cap_net_raw` sont requis :

```bash
sudo setcap cap_net_raw+eip rid_capture
./rid_capture -x > rid_capture.txt        # Capturer et enregistrer en JSON
```

Sortie UDP en direct (ouvre un autre terminal) :

```bash
nc -lu 32001
```

### Étape 9 — Visualiser les trajectoires de vol (GPX → Google Earth)

```bash
./scripts/rid2gpx.pl < rid_capture.txt      # Générer le .gpx
```

Ouvre le fichier .gpx dans Google Earth pour voir la trajectoire de vol du drone. Une entrée JSON de détection typique ressemble à :

```json
{
  "mac": "ac:67:b2:09:50:d4",
  "operator": "GBR-OP-ZZZZZZZZZZZZ",
  "uav id": "SERIAL NUMBER",
  "uav latitude": 25.0330,
  "uav longitude": 121.5654,
  "uav altitude": 120,
  "uav heading": 90,
  "uav speed": 8,
  "base latitude": 25.0300,
  "base longitude": 121.5600
}
```

### Étape 10 — (Optionnel) Se connecter à la carte communautaire DroneAware

```bash
curl -fsSL https://github.com/fduflyer/DroneAware-Node-Releases/releases/latest/download/install.sh | sudo bash
```

{{< alert "circle-info" >}}
**Note de sécurité** : Pour tout script tiers `curl ... | sudo bash`, nous recommandons de le télécharger et de le vérifier d'abord : `curl -fsSL <url> -o install.sh && less install.sh && sudo bash install.sh`. Le programme d'installation détecte automatiquement les adaptateurs USB, demande un nom de nœud et te guide à travers l'inscription sur droneaware.io. Les détections apparaissent sur la carte en direct en temps réel.
{{< /alert >}}

---

## 7. Clarification technique importante : RID standard vs. DJI OcuSync

C'est là que l'expertise compte — assure-toi que tes clients comprennent la différence :

| Voie | Ce qu'elle couvre | Matériel | Fonctionne avec ALFA AWUS036ACH ? |
|---|---|---|---|
| **Remote ID standard** | Diffusion ASTM F3411 Wi-Fi / BT | AWUS036ACH + nRF52840 | ✅ Oui (sujet principal de cet article) |
| **DJI OcuSync DroneID** | Protocole propriétaire DJI (pas du Wi-Fi standard) | SDR complet (ANTSDR / HackRF / USRP) + plugin Kismet `kismet_cap_antsdr_droneid` | ❌ Non |

- L'ALFA AWUS036ACH est un **récepteur de bande Wi-Fi (2,4 / 5 / 6 GHz)**. Il traite complètement le RID standard.
- Le **DroneID OcuSync** propriétaire de DJI n'utilise pas les protocoles Wi-Fi standard. **L'adaptateur ALFA ne peut pas le décoder**. Tu as besoin d'un SDR couvrant les fréquences 2,4 / 5,8 GHz (ex. ANTSDR E200) avec le plugin `alphafox02/antsdr_dji_droneid` + Kismet.
- ⚠️ Note : **Le RTL-SDR standard a une limite de bande passante d'environ 1,7 GHz** — il ne peut pas voir l'OcuSync à 2,4 / 5,8 GHz. Tu dois choisir un SDR qui supporte des fréquences plus élevées.
- Les deux voies sont **complémentaires** : l'adaptateur ALFA gère la détection des diffusions RID standard, tandis que le SDR s'occupe du protocole propriétaire DJI — formant ensemble un front-end complet de connaissance situationnelle Counter-UAV / RF.

---

{{< faq >}}

---

## Annexe : Glossaire pour débutants

Si tu débutes dans la réglementation des drones et la technologie anti-drone (Counter-UAV), voici une explication rapide des termes utilisés dans ce guide :

| Terme | Explication simple |
|---|---|
| **Remote ID** | La « plaque d'immatriculation numérique » d'un drone. La réglementation exige que les drones diffusent en continu leur identité, leur position et d'autres informations afin que les personnes au sol — en particulier les autorités — puissent voir « à qui appartient ce drone et où il va ». |
| **ASTM F3411 / EN 4709-002** | Les normes américaine et européenne respectivement pour les spécifications de diffusion Remote ID. Elles définissent les informations qui doivent être diffusées et leur format, garantissant l'interopérabilité entre les différentes marques de drones et les équipements de détection. |
| **Détection passive (Passive Detection)** | Se contenter d'« écouter » les messages diffusés publiquement. Aucun signal actif n'est émis pour interférer avec le drone ou l'attaquer. Légalement très différent du brouillage actif (jamming). |
| **Mode monitor** | Un état dans lequel un adaptateur WiFi cesse d'essayer de se connecter à des points d'accès et se met à « écouter passivement » tous les paquets radio dans les airs — la condition préalable à la capture des diffusions Remote ID. |
| **NAN (Wi-Fi Aware) / Beacon** | Deux formats de trames WiFi que les drones utilisent pour diffuser le Remote ID. Ce kit tente de décoder les deux. |
| **Bluetooth 5 Long Range** | En plus du WiFi, certains drones diffusent le Remote ID via Bluetooth. Un dongle nRF52840 supplémentaire est nécessaire pour les capturer. |
| **DJI OcuSync / DroneID** | Le protocole propriétaire de transmission vidéo et télémétrie de DJI. Ce n'est **pas** du WiFi standard et ce n'est **pas** le protocole Remote ID traité dans cet article. Il nécessite un matériel SDR et des plugins complètement différents — voir la section 7 pour les détails. |
| **SDR (Software Defined Radio)** | Un récepteur radio universel dont la gamme de fréquences et les méthodes de démodulation peuvent être configurées par logiciel. Des appareils comme ANTSDR et HackRF peuvent couvrir des bandes de fréquences que l'adaptateur ALFA ne peut pas atteindre (comme le DJI OcuSync). |
| **RTL8812AU** | Le chipset Realtek à l'intérieur de l'ALFA AWUS036ACH. Ce circuit détermine si l'adaptateur prend en charge le mode monitor. |
| **Fichier GPX** | Un format standard pour enregistrer des traces de coordonnées GPS. Tu peux l'ouvrir directement dans Google Earth et des logiciels similaires pour visualiser la trajectoire de vol d'un drone. |

> En une phrase : Ce guide t'apprend à transformer un adaptateur ALFA en « scanner d'identité de drone » — réception passive des informations publiques que les drones sont légalement tenus de diffuser. Une méthode légale pour la gestion de la sécurité des sites.

---

## Références

1. [opendroneid/opendroneid-core-c — Open Drone ID Core C Library](https://github.com/opendroneid/opendroneid-core-c)
2. [sxjack/unix_rid_capture — Capture RID WiFi/BT (validé rtl8812au + nRF52840 + RPi)](https://github.com/sxjack/unix_rid_capture)
3. [fduflyer/DroneAware-Node-Releases — Réseau de détection Remote ID communautaire](https://github.com/fduflyer/DroneAware-Node-Releases)
4. [kismetwireless/kismet — Framework de détection sans fil](https://github.com/kismetwireless/kismet)
5. [alphafox02/antsdr_dji_droneid — Décodeur SDR DroneID DJI OcuSync](https://github.com/alphafox02/antsdr_dji_droneid)
6. [morrownr/8812au-20210629 — Pilote moniteur/injection RTL8812AU Linux](https://github.com/morrownr/8812au-20210629)
7. [Page produit ALFA AWUS036ACH (Yupitek)](https://yupitek.com/fr/products/alfa/awus036ach/)
8. [Contact et commande (Yupitek)](https://www.yupitek.com/fr/contact/)

---

*Cet article a été compilé par l'équipe technique Yupitek. L'AWUS036ACH et le matériel associé sont disponibles auprès de Yupitek avec une distribution autorisée et un support technique.*
