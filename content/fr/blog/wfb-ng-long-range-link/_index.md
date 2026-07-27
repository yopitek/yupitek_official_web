---
title: "Liaison numérique FPV et télémétrie longue distance DIY avec ALFA AWUS036ACH et wfb-ng (2026)"
description: "Construis une liaison vidéo numérique et télémétrie MAVLink longue distance, à faible latence et chiffrée, avec l'adaptateur ALFA AWUS036ACH et le logiciel open-source wfb-ng. Liste complète du matériel, guide d'installation Raspberry Pi et dépannage d'alimentation."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "AWUS036ACH", "wfb-ng", "RTL8812AU", "liaison-vidéo-drone", "FPV-numérique", "FPV", "monitor-mode", "packet-injection", "MAVLink", "Raspberry-Pi", "longue-distance", "liaison-télémétrie"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "Quelle est la différence entre wfb-ng et le WiFi classique ?"
    answer: "Le WiFi standard nécessite une association et des accusés de réception (ACK), ce qui est inefficace sur de longues distances. wfb-ng contourne ces mécanismes 802.11 en utilisant l'injection de paquets bruts avec correction d'erreur FEC, ramenant la latence de bout en bout à quelques dizaines de millisecondes."
  - question: "Pourquoi l'adaptateur ALFA embarqué a-t-il besoin de sa propre alimentation ?"
    answer: "L'AWUS036ACH consomme un courant important pendant les bursts d'émission (TX). Branché directement sur un port USB 2.0 d'un Raspberry Pi, les chutes de tension réinitialisent l'adaptateur, coupent la liaison ou corrompent les paquets. Utilise un BEC 5V dédié et ajoute un condensateur 470µF basse ESR entre +5V et GND."
  - question: "J'ai une connexion mais ni vidéo ni télémétrie — que faire ?"
    answer: "La cause la plus fréquente est une discordance de clés — vérifie que drone.key sur le drone correspond à gs.key sur la station au sol. Assure-toi aussi que wifi_channel et link_domain sont identiques des deux côtés. Consulte les logs en temps réel avec journalctl -xu wifibroadcast@gs."
  - question: "Suis-je obligé d'utiliser l'ALFA AWUS036ACH pour wfb-ng ?"
    answer: "Tout adaptateur basé sur RTL8812AU peut théoriquement fonctionner, mais l'AWUS036ACH est le matériel officiellement testé par le projet wfb-ng. Son support pilote est le plus stable, surtout pour les scénarios longue distance où la conception haute puissance d'ALFA et ses antennes détachables offrent un avantage certain."
---
> Auteur : Équipe technique Yupitek (distributeur officiel ALFA Network, Taïwan)
> Public cible : Passionnés de drones, makers, chercheurs en sécurité, développeurs de drones agricoles et d'inspection
> Difficulté : ★★★☆☆ (connaissances de base Linux et contrôleur de vol requises)

{{< tldr >}}
wfb-ng est un logiciel open-source qui transforme les adaptateurs WiFi compatibles mode monitor — comme l'**ALFA AWUS036ACH** — en radios longue distance spécialisées pour drones. Tu peux ainsi construire une liaison vidéo et télémétrie MAVLink à faible latence et chiffrée avec du matériel standard.
{{< /tldr >}}

---

## 1. Pourquoi construire une liaison FPV numérique avec une carte ALFA ?

Si tu as déjà utilisé du FPV analogique (vidéo analogique 5,8 GHz), tu connais le scénario : un obstacle bloque le signal et l'écran se remplit de neige, la portée chute, et **n'importe qui avec un récepteur peut voir ton flux** — pas de chiffrement, pas de retour télémétrie.

Au cours de l'année écoulée, notre équipe a installé des liaisons pour des opérateurs agricoles, des équipes d'inspection et des clients en formation sécurité. Une question revenait sans cesse : **Puis-je utiliser un adaptateur USB ALFA standard avec un logiciel open-source pour construire une liaison numérique, chiffrée et longue distance qui transporte à la fois la vidéo et la télémétrie ?**

La réponse est oui — et c'est plus simple que tu ne le penses.

Comparé au FPV analogique traditionnel, wfb-ng sur un adaptateur ALFA offre plusieurs avantages décisifs :

- **Faible latence** : L'injection WiFi brute contourne les ACK et le handshake 802.11. La latence de bout en bout tombe à quelques dizaines de millisecondes — la sensation FPV est proche de l'analogique.
- **Chiffrement numérique** : Les paquets vidéo et télémétrie sont chiffrés avec libsodium. Même si quelqu'un capture le signal, il ne peut pas décoder ton flux ni tes données de vol.
- **Une liaison, plusieurs flux** : Un seul adaptateur sur une fréquence gère :
  - La vidéo en direct (RTP / RTSP)
  - La télémétrie MAVLink (bidirectionnelle, contrôleur de vol ↔ station au sol)
  - Un tunnel TCP/IP (pour VPN, SSH ou transfert de fichiers)
- **Diversité d'émission (TX diversity)** : Plusieurs adaptateurs peuvent travailler ensemble pour améliorer la résistance aux obstructions.
- **Open source, entièrement personnalisable** : L'ALFA AWUS036ACH associé à wfb-ng ne coûte qu'une fraction des systèmes FPV numériques commerciaux (DJI O3, Walksnail, etc.) — et chaque ligne de code est ouverte.

{{< alert "circle-info" >}}
Ce guide n'a pas pour but de remplacer le système FPV DJI. C'est une voie open-source pratique pour ceux qui veulent **maîtriser leur liaison, créer une redondance secondaire ou réaliser des charges utiles personnalisées**.
{{< /alert >}}

---

## 2. Ce que c'est : wfb-ng expliqué

**wfb-ng** (Wireless Fibre / WiFi Broadcast – next generation) est un projet open-source de FPV numérique et de télémétrie avec une idée centrale ingénieuse :

> Il n'utilise pas le WiFi comme un « réseau ». Il utilise le WiFi comme une « radio ».

Le 802.11 standard a été conçu pour les réseaux locaux — association, ACK, retransmission. Sur de longues distances, avec des véhicules en mouvement et des signaux faibles, ces mécanismes deviennent un handicap. wfb-ng adopte une approche différente avec l'**injection WiFi brute (raw WiFi injection)** :

- L'adaptateur passe en **mode monitor** — il ne se « connecte » à rien.
- Il injecte directement des trames WiFi brutes. **Pas d'ACK, pas de retransmission** (FEC — correction d'erreur directe — compense les pertes de paquets).
- Cela contourne les limites de portée et de latence du 802.11 standard, poussant la distance et la stabilité jusqu'à la limite physique du matériel.

En termes simples : il transforme un adaptateur USB courant en une paire de « radios numériques » capables de transporter de la vidéo RTP, de la télémétrie MAVLink et même un tunnel IP.

- Page du projet (GitHub) : https://github.com/svpcom/wfb-ng.git
- Largement utilisé dans l'écosystème PX4 / ArduPilot pour le FPV numérique DIY. Communauté active, également utilisée dans la communauté ukrainienne de drones.

---

## 3. La star : ALFA AWUS036ACH

La « radio » de cette liaison est l'**ALFA AWUS036ACH**.

Il utilise le chipset **Realtek RTL8812AU** avec **802.11ac (WiFi 5)**, **double bande 2,4 GHz / 5 GHz**, USB 3.0 Type-C et antennes RP-SMA détachables. Point crucial : **Le matériel de test officiel de wfb-ng utilise l'AWUS036ACH aux deux extrémités en mode 5 GHz**. Cet adaptateur a été validé par l'auteur du projet pour le support pilote le plus stable.

Trois raisons de ce choix :

1. **Assez de puissance** : La conception haute puissance caractéristique d'ALFA, combinée à des antennes externes à gain élevé, offre des performances longue distance bien supérieures à toute carte interne d'ordinateur portable.
2. **Mode monitor + injection** : Avec le pilote patché (voir ci-dessous), le RTL8812AU supporte de façon fiable le mode monitor et l'injection de paquets bruts — la condition préalable pour wfb-ng.
3. **Universel et robuste** : Le format USB fonctionne aussi bien sur le drone qu'à la station au sol. Pas besoin d'acheter différents adaptateurs pour différentes machines. Si l'un tombe en panne, on le remplace simplement.

{{< alert "triangle-exclamation" >}}
**Note** : wfb-ng nécessite un **pilote patché** (ex. `rtl88xxau_wfb`). Le pilote standard du noyau Linux ne peut pas activer le mode d'injection nécessaire à wfb-ng. Les instructions d'installation se trouvent dans les sections « Liste logicielle » et « Configuration pas à pas ».
{{< /alert >}}

---

## 4. Liste du matériel

La liaison se divise en deux parties : **Drone (embarqué)** et **Station au sol**.

### Drone (embarqué)

| Élément | Modèle recommandé / Remarques |
|---|---|
| Ordinateur embarqué | Raspberry Pi 3B / 3B+ / Zero 2 W / 4 (pour du 1080p, utilise un **Pi 4 ou Zero 2 W**) |
| Caméra | Raspberry Pi Camera (CSI) ou Logitech C920 (USB) |
| Adaptateur WiFi | **ALFA AWUS036ACH** (ou tout adaptateur basé sur RTL8812AU) |
| Alimentation | **BEC 5V** (alimentation dédiée pour l'adaptateur — voir le conseil de dépannage) |
| Condensateur de filtrage | **Condensateur 470µF basse ESR** (entre +5V et GND de l'adaptateur) |
| Contrôleur de vol | Pixhawk ou similaire (MAVLink sur UART vers l'ordinateur embarqué) |

### Station au sol

| Élément | Modèle recommandé / Remarques |
|---|---|
| Ordinateur | Machine Linux (Ubuntu / Debian x86-64), ou un autre Raspberry Pi |
| Adaptateur WiFi | **ALFA AWUS036ACH** |
| Logiciel de supervision | Machine exécutant **QGroundControl** (peut être le même que l'ordinateur de la station au sol) |

> Remarque : Pour les configurations **réception seule (RX)**, tout adaptateur supportant le mode monitor fonctionne — même un routeur flashé avec OpenWRT. Cependant, la configuration officiellement testée et ce guide utilisent l'AWUS036ACH.

---

## 5. Liste logicielle

### Système d'exploitation

- **Raspberry Pi OS** / **Debian** / **Ubuntu** (noyau Linux ≥ 4.x)

### Projets principaux

- **wfb-ng** (svpcom/wfb-ng) : Programme principal FPV numérique / télémétrie
- **Pilote patché** :
  - RTL8812AU → `svpcom/rtl8812au` (branche **v5.2.20**, installation via dkms)
  - RTL8812EU → `svpcom/rtl8812eu`
  - Après chargement, l'adaptateur apparaît sous le nom `rtl88xxau_wfb` (ou `rtl8812eu`)

### Dépendances système

```bash
sudo apt update
sudo apt install -y \
  python3-all libpcap-dev libsodium-dev libevent-dev \
  python3-pip python3-pyroute2 python3-twisted python3-serial \
  python3-all-dev python3-venv iw socat debhelper dh-python \
  fakeroot build-essential python3-msgpack python3-setuptools \
  libgstrtspserver-1.0-dev
```

### Chiffrement

- **libsodium** : Utilise `wfb_keygen` pour générer `drone.key` (drone) et `gs.key` (station au sol)

### Lecture à la station au sol

- **QGroundControl** : Supervision du statut du contrôleur de vol et de la télémétrie
- **GStreamer / RTSP** : Réception et lecture de la vidéo en direct du drone

---

## 6. Liens GitHub et fiche technique ALFA AWUS036ACH

### Liens officiels

| Élément | Lien |
|---|---|
| Projet wfb-ng | https://github.com/svpcom/wfb-ng.git |
| Pilote patché (RTL8812AU) | https://github.com/svpcom/rtl8812au |
| Pilote patché (RTL8812EU) | https://github.com/svpcom/rtl8812eu |
| Page produit ALFA AWUS036ACH | https://yupitek.com/fr/products/alfa/awus036ach/ |
| Tutoriel PX4 WFB-ng | https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html |

### Fiche technique ALFA AWUS036ACH

| Spécification | Détail |
|---|---|
| Chipset | Realtek **RTL8812AU** |
| Standard sans fil | 802.11a / b / g / n / **ac (WiFi 5)** |
| Fréquence | **2,4 GHz + 5 GHz** double bande |
| Interface | USB 3.0 **Type-C** |
| Antenne | 2 × détachable **RP-SMA** (2T2R MIMO) |
| Mode monitor | Supporte le mode monitor + l'injection de paquets (nécessite le pilote patché wfb-ng) |
| Pilote wfb-ng | `rtl88xxau_wfb` (svpcom/rtl8812au, v5.2.20) |
| Statut | Adaptateur **officiellement testé par wfb-ng** (5 GHz aux deux extrémités) |

---

## 7. Configuration pas à pas

Cette section comporte quatre parties. **La voie A (Raspberry Pi Quick Start)** est la plus recommandée — une expérience presque « prête à l'emploi ». **La voie B** est pour l'installation manuelle sur station au sol Linux x86. **Les voies C et D** concernent l'appairage des clés et la configuration ; les deux voies les utilisent.

### A. Raspberry Pi Quick Start (Recommandé)

wfb-ng fournit des images Raspberry Pi préconstruites. Flashes-en une pour le drone et une pour la station au sol — elles fonctionnent dès le démarrage.

**1. Télécharger et flasher l'image**

Rends-toi sur la page **Releases** GitHub de wfb-ng, télécharge la dernière `*.img.gz`, extrais-la et flashes-la sur **deux** cartes SD (une pour le drone, une pour la station au sol).

```bash
# Extraire l'image (le nom du fichier varie selon la release)
gunzip wfb-ng-*.img.gz
# Flasher sur la carte SD avec Raspberry Pi Imager, dd ou balenaEtcher
```

**2. Insérer l'adaptateur, démarrer, se connecter en SSH**

Branche un ALFA AWUS036ACH sur les deux cartes, allume-les et connecte-toi en SSH (IP et identifiants par défaut ci-dessous) :

```bash
ssh pi@192.168.0.111
# Mot de passe : raspberry
```

**3. Activer les services de la station au sol**

Sur le **Pi de la station au sol**, exécute :

```bash
sudo systemctl enable wifibroadcast@gs
sudo systemctl enable rtsp
sudo systemctl enable fpv-video
sudo systemctl enable osd
sudo reboot
```

**4. Activer les services du drone**

Sur le **Pi du drone**, exécute :

```bash
sudo systemctl enable wifibroadcast@drone
sudo systemctl enable fpv-camera
sudo reboot
```

**5. Surveiller l'état de la liaison depuis la station au sol**

```bash
wfb-cli gs
```

> Quand tu vois les informations de connexion, de canal et de perte de paquets, la liaison est active. Ouvre QGroundControl pour accéder à la télémétrie et à la vidéo.

---

### B. Installation manuelle de la station au sol Debian / Ubuntu

Si tu utilises un ordinateur de bureau ou un portable Linux x86-64 comme station au sol, installe manuellement.

**1. Installer dkms et le pilote patché**

```bash
git clone -b v5.2.20 https://github.com/svpcom/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh
```

**2. Vérifier que l'adaptateur utilise le pilote wfb-ng**

```bash
# Devrait afficher wlan0 avec MTU 2312
ifconfig

# Le nom du pilote doit être rtl88xxau_wfb (RTL8812AU) ou rtl8812eu (RTL8812EU)
ethtool -i wlan0
```

{{< alert "triangle-exclamation" >}}
Si `ethtool -i wlan0` affiche `rtl8812au` au lieu de `rtl88xxau_wfb`, le pilote patché n'est pas correctement installé et wfb-ng ne pourra pas entrer en mode injection. Vérifie l'installation dkms pour les erreurs.
{{< /alert >}}

**3. Exécuter le script d'installation automatique officiel**

```bash
curl -o install_gs.sh https://raw.githubusercontent.com/svpcom/wfb-ng/refs/heads/master/scripts/install_gs.sh
sudo bash ./install_gs.sh
```

**4. Surveiller la liaison**

```bash
wfb-cli gs
```

---

### C. Appairage des clés

La vidéo et la télémétrie wfb-ng sont chiffrées. Le drone et la station au sol doivent utiliser des **clés correspondantes** pour communiquer.

```bash
# Générer les clés (à faire sur le drone, puis distribuer)
wfb_keygen

# Placer drone.key sur le drone
# Placer gs.key sur la station au sol
# Les deux doivent correspondre — sinon la liaison affiche « connecté » mais aucune donnée
```

> Si tu as utilisé **le script d'installation automatique de la voie B (install_gs.sh)**, il génère et configure les clés automatiquement. Pour une installation manuelle, assure-toi que `drone.key` et `gs.key` appartiennent à la même paire.

---

### D. Le fichier de configuration clé : /etc/wifibroadcast.cfg

`/etc/wifibroadcast.cfg` est le fichier de configuration central de wfb-ng. Voici les paramètres que tu devras le plus souvent ajuster :

```ini
[common]
# Canal 165 = 5825 MHz (bande 5,8 GHz)
wifi_channel = 165

# Définir le code pays sur 'BO' (Bolivie) pour débloquer la puissance TX maximale
wifi_region = 'BO'

[drone]
# link_domain doit être IDENTIQUE sur le drone et la station au sol
link_domain = "my_wfb_link_01"

[drone_mavlink]
# Recevoir MAVLink depuis l'UART du contrôleur de vol (régler l'UART à 1500000 bauds)
peer = 'serial:ttyS0:1500000'

[drone_video]
peer = 'listen://0.0.0.0:5602'

[gs]
# Même réglage que ci-dessus — doit correspondre au drone
link_domain = "my_wfb_link_01"
```

**Les trois erreurs les plus fréquentes :**

1. **`wifi_channel` doit être identique des deux côtés** : Ce guide utilise 165 (5825 MHz, 5,8 GHz). Configure-le à l'identique sur le drone et la station au sol.
2. **`link_domain` doit être identique des deux côtés** : C'est l'identifiant de la liaison. Des valeurs différentes signifient aucune connexion.
3. **Le débit en bauds de l'UART du contrôleur de vol doit être à 1500000** : `peer = 'serial:ttyS0:1500000'` nécessite que l'UART du contrôleur de vol soit également configuré à 1500000 bauds, sinon MAVLink ne fonctionnera pas.

{{< alert "triangle-exclamation" >}}
**Note** : `wifi_region = 'BO'` débloque la puissance TX maximale, mais **cela ne signifie pas que c'est légal dans ton pays**. Consulte l'avertissement réglementaire ci-dessous.
{{< /alert >}}

---

## 8. Remarques pratiques et pièges courants

Cette section couvre les problèmes que nous avons réellement rencontrés lors de déploiements réels. À lire absolument.

### Piège 1 : Alimentation insuffisante de l'adaptateur → réinitialisations et pertes de paquets

L'AWUS036ACH consomme **un courant important pendant les bursts d'émission (TX)**. Branché sur un port USB 2.0 standard d'un Raspberry Pi, l'alimentation USB du Pi ne peut pas soutenir l'appel de courant. Résultat : **le port de l'adaptateur est réinitialisé, la liaison tombe, les paquets sont corrompus, la vidéo se fige**.

Solution (obligatoire côté drone) :

- Alimente l'adaptateur **directement via un BEC 5V** (pas depuis le port USB du Pi). Connecte la sortie du BEC à l'adaptateur.
- Ajoute un **condensateur 470µF basse ESR entre +5V et GND** au niveau de l'adaptateur pour absorber les pics de courant TX.
- Côté station au sol, un **port USB 3.0 d'un ordinateur portable avec le câble USB 3.0 d'origine** suffit généralement — pas de BEC supplémentaire nécessaire.

> Cette unique étape détermine si ta liaison est stable. Nous avons vu d'innombrables cas de perte de paquets causés par une mauvaise alimentation.

### Piège 2 : Erreurs de chiffrement / pas de connexion

Si `wfb-cli gs` affiche « connecté » mais **il n'y a ni vidéo ni télémétrie**, les causes sont presque toujours :

- **Discordance de clés** : Vérifie que `drone.key` sur le drone correspond à `gs.key` sur la station au sol.
- **Discordance de canal ou de link_domain** : Les deux extrémités doivent avoir des paramètres `wifi_channel` et `link_domain` identiques.

Commande de débogage :

```bash
# Consulter les logs de la station au sol pour les erreurs de chiffrement/connexion
journalctl -xu wifibroadcast@gs
```

### Piège 3 : Conformité réglementaire (important)

Cette liaison émet activement des ondes radio. C'est un équipement de transmission sans fil.

- **Vérifie que la réglementation locale autorise ce type de transmission WiFi au niveau de puissance et sur les fréquences que tu prévois d'utiliser.**
- Taïwan, la Chine, l'UE et les États-Unis ont chacun leurs propres règles concernant la puissance d'émission, les canaux disponibles et les transmissions « sans association » dans la bande ISM 5,8 GHz.
- Le réglage `wifi_region = 'BO'` débloque le plafond de puissance matériel, mais **ne le rend pas légal dans ton pays**. Ajuste les canaux et la puissance pour te conformer à la réglementation radio locale.
- Utilise la liaison uniquement dans des environnements autorisés (terrains agricoles privés, zones d'essai fermées, installations de formation). Ne perturbe pas les autres communications.

---

## 9. Conclusion

Avec un seul ALFA AWUS036ACH et le projet open-source wfb-ng, nous avons construit une liaison qui offre :

- **Avantage de coût** : Le coût total des composants est bien inférieur à toute solution FPV numérique commerciale.
- **Open source** : Chaque ligne de code, chaque pilote, chaque configuration est publiquement accessible.
- **Entièrement personnalisable** : Canaux, puissance, clés de chiffrement, routage MAVLink — tout est sous ton contrôle.
- **Longue portée** : Vidéo numérique et télémétrie sur une seule liaison, portée testée sur le terrain en 5 GHz bien supérieure à l'analogique, avec chiffrement et résistance aux obstructions.

Pour l'agriculture, l'inspection, la formation en sécurité, ou tous ceux qui veulent comprendre comment fonctionne réellement le FPV numérique sous le capot, c'est une voie qui vaut la peine d'être explorée.

Notre équipe continuera à partager ses notes d'implémentation de liaisons drone avec adaptateurs ALFA sur ce blog. Si tu rencontres des problèmes lors de l'installation, n'hésite pas à nous contacter — **construire soi-même est le moyen le plus rapide d'apprendre**.

---

{{< faq >}}

---

## Annexe : Glossaire pour débutants

Si c'est la première fois que tu découvres la technologie des liaisons drone, voici une explication rapide des termes utilisés dans ce guide :

| Terme | Explication simple |
|---|---|
| **FPV** (First Person View) | Un flux vidéo en direct de la caméra du drone vers un écran ou des lunettes au sol — comme si tu étais assis dans le cockpit. |
| **FPV numérique vs FPV analogique** | L'analogique, c'est comme la vieille télévision : un signal faible donne de la neige et n'importe qui peut capter. Le numérique encode la vidéo en paquets de données — chiffrable, meilleure résistance aux interférences, mais nécessite du matériel et une configuration plus complexes. |
| **Mode monitor** | Les adaptateurs WiFi normaux ne font que se connecter à des points d'accès. Le mode monitor permet à l'adaptateur d'écouter et d'émettre des signaux radio bruts sans s'associer à rien — le fondement de ce guide. |
| **Injection de paquets (packet injection)** | En mode monitor, tu peux injecter des trames radio personnalisées directement dans les airs sans passer par les procédures normales de connexion WiFi. wfb-ng utilise ce mécanisme pour envoyer la vidéo et la télémétrie. |
| **wfb-ng** | Logiciel open-source qui transforme un adaptateur WiFi en liaison radio spécialisée pour drone. Le logiciel central de ce guide. |
| **FEC (Forward Error Correction)** | L'émetteur envoie des données redondantes supplémentaires. Si des paquets sont perdus, le récepteur reconstruit les données originales à partir de la redondance — pas besoin de retransmission (trop lente sur les liaisons longue distance à grande vitesse). |
| **MAVLink** | Le protocole standard que les contrôleurs de vol de drone (Pixhawk, etc.) utilisent pour communiquer avec les stations au sol — pour le statut de vol, les commandes et les données de télémétrie. |
| **RTP / RTSP** | Protocoles standards pour diffuser de la vidéo en direct sur un réseau. Ta caméra IP et ton système de sécurité utilisent probablement le même type de protocole. |
| **Chiffrement libsodium** | La bibliothèque de chiffrement open-source utilisée dans ce guide pour chiffrer la vidéo et la télémétrie. Seuls le drone et la station au sol appairés peuvent déchiffrer le contenu. |
| **Diversité d'émission (TX diversity)** | Utilisation de plusieurs adaptateurs pour émettre les mêmes données simultanément. Si le signal d'un adaptateur est bloqué, un autre prend le relais — comme un système de double redondance. |
| **BEC (Battery Eliminator Circuit)** | Un module régulateur de tension qui abaisse la tension de la batterie du drone aux 5 V dont l'adaptateur a besoin, en gérant les pics de courant élevés sans chute de tension. |
| **RTL8812AU** | Le chipset Realtek à l'intérieur de l'ALFA AWUS036ACH. Ce circuit détermine si l'adaptateur supporte le mode monitor et l'injection de paquets. |

> En une phrase : wfb-ng transforme l'adaptateur ALFA en une station radio dédiée au drone, permettant à la vidéo et aux données de vol de parcourir de longues distances sur une liaison open-source et chiffrée — ton propre canal privé.

---

## Références

- **Projet wfb-ng (svpcom/wfb-ng)** : https://github.com/svpcom/wfb-ng.git
- **Page produit ALFA AWUS036ACH** : https://yupitek.com/fr/products/alfa/awus036ach/
- **Pilote patché (RTL8812AU)** : https://github.com/svpcom/rtl8812au
- **Pilote patché (RTL8812EU)** : https://github.com/svpcom/rtl8812eu
- **Tutoriel PX4 WFB-ng** : https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html

---

*Cet article a été rédigé par l'équipe technique Yupitek (distributeur officiel ALFA Network, Taïwan), sur la base de la documentation officielle de wfb-ng et de l'expérience pratique. Avant de construire ta liaison, vérifie la réglementation radio locale et ajuste la puissance d'émission et les fréquences en conséquence.*
