---
title: "Dépasser le goulot d'étranglement de la bande passante en IA de périphérie : installez un adaptateur Wi-Fi 6E haute puissance sur le NVIDIA Jetson Orin Nano pour la transmission vidéo 6GHz"
description: "Installez l'adaptateur ALFA AWUS036AXML Wi-Fi 6E sur le Jetson Orin Nano pour faire passer le streaming RTSP 4K dans la bande 6GHz, avec les tests A/B iperf3 et GStreamer."
date: 2026-08-31
author: benny-lai
lastmod: 2026-08-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["jetson-orin-nano", "wifi-6e", "awus036axml", "6ghz", "rtsp", "edge-ai", "nvidia"]
featureimage: "/images/blog/jetson-orin-nano-wifi-6e-6ghz-high-bandwidth-streaming.webp"
---

> **Plateforme cible** : NVIDIA Jetson Orin Nano Developer Kit, JetPack 6.x (base Ubuntu 22.04 LTS, Linux Kernel 5.15 / 6.1)
> **Matériel du guide** : ALFA AWUS036AXML (chipset MediaTek MT7921AU, adaptateur USB tribande Wi-Fi 6E)
> **Portée de cet article** : cette solution est une évaluation bench-test pour une plateforme de développement académique/ingénierie open source de type DIY ; il ne s'agit pas d'un support officiel d'un produit commercial, ni d'une certification officielle d'un fabricant de plateformes fermées.

## Introduction : d'où vient le « plafond de bande passante » des appareils de périphérie ?

Connecter un Jetson Orin Nano à un point d'accès (AP) et faire tourner deux ou trois caméras IP semble banal. Mais quand vous envoyez réellement plusieurs **flux 4K en direct** dans le GPU pour l'inférence, beaucoup ressentent pour la première fois la limite du réseau sans fil :

- La qualité d'image ne cesse de chuter (le bitrate ne monte pas, l'image devient brumeuse ou en blocs).
- La latence fluctue, et le « décalage temporel » de l'inférence des modèles d'IA vidéo devient de plus en plus visible.
- La planification se bloque, l'écran du centre de contrôle devient noir, et en vérifiant, la cause est « perte de paquets sans fil ».

Cet article décompose le défi de bande passante du « streaming RTSP 4K multicanal en périphérie » sous trois angles : **couche physique → couche de configuration → couche de mesure**. Il montre ensuite comment connecter l'**adaptateur AWUS036AXML Wi-Fi 6E** à un **Jetson Orin Nano (JetPack / Ubuntu 22.04 LTS)** et passer dans la **bande 6GHz propre**. Enfin, les données prouvent « pourquoi le 6GHz est le premier choix pour ce type de charge de travail ».

Si vous n'avez pas encore décidé d'acheter cette carte, nous vous recommandons de passer directement à la « Liste de vérification de compatibilité avant achat » du chapitre 4 et de cocher chaque point.

---

## 1. Streaming RTSP 4K multicanal en périphérie : les défis de bande passante et d'interférences du réseau sans fil

### 1.1 D'abord, faites le calcul : combien de bande passante un flux 4K exige-t-il ?

RTSP (Real-Time Streaming Protocol) n'est qu'un protocole de « poignée de main et de contrôle » ; les données vidéo réelles voyagent dans des paquets RTP. En prenant l'exemple des sorties de caméras IP commerciales courantes :

| Sortie caméra | Codec | Débit réel par flux (selon les réglages de qualité) |
|---|---|---|
| 1080p30 | H.264 | Environ 4 – 8 Mbps |
| 4K (2160p)30 | H.264 | Environ 20 – 35 Mbps |
| 4K (2160p)30 | H.265 | Environ 10 – 20 Mbps |
| 4K (2160p)30 (réglages bitrate élevé et faible latence) | H.264 | Jusqu'à 45 Mbps+ |

> **Point clé** : le 4K est un monstre — **chaque flux consomme 2,5 à 8 fois la bande passante du HD**. Quatre flux 4K/H.264 entrant simultanément sur la carte équivalent à **80–140 Mbps de « charge utile effective »**. Notez bien : **charge utile effective**, pas le débit PHY sans fil — la différence entre les deux est de près du double (voir 1.3).

### 1.2 Perte de paquets ≠ problème de signal : le support sans fil est semi-duplex et partagé

Beaucoup pensent que « si le signal est plein, il n'y a pas de problème », mais dans les environnements de périphérie, le vrai tueur est la **congestion** :

- **En 2.4GHz, il ne reste que 3 canaux sans chevauchement** : Bluetooth, fours à micro-ondes et points d'accès des usines voisines s'y entassent. Avec le mécanisme de backoff de CSMA/CA, le débit est réduit de moitié, puis encore de moitié, à mesure que les appareils augmentent.
- **Le 5GHz est meilleur, mais reste un champ de bataille** : la densité du 5GHz dans les appartements, bureaux et usines pousse l'utilisation des canaux à l'explosion.
- **Le sans fil est un support partagé** : aussi élevé que soit le débit PHY, si quelqu'un d'autre est sur le canal, vos paquets attendent. Le contrôle de congestion de TCP réduit donc la vitesse en continu.

### 1.3 Pourquoi « PHY 2400 Mbps » n'équivaut pas à « transmission de 2400 Mbps » ?

Le débit sans fil subit de nombreux abattements ; c'est un fait physique :

1. **Frais de protocole (Overhead)** : en-têtes de trames Wi-Fi, ACK, Beacon et fenêtre de contention CSMA/CA consomment environ 30–50 % du débit PHY.
2. **Pertes environnementales** : distance, murs et réflexions métalliques forcent le PHY à se dégrader automatiquement (du MCS le plus élevé au MCS le plus bas).
3. **Planification bidirectionnelle** : l'upload vidéo (uplink) et le download de contrôle (downlink) partagent la même liaison sans fil.

Ainsi, une carte annoncée en classe 2400 Mbps **fournit généralement 600–900 Mbps de charge utile réelle dans un environnement propre** — largement suffisant pour le 4K multicanal (80–140 Mbps). Mais **une fois insérée dans un canal 2.4G/5G congestionné, les mesures réelles tombent souvent à 100–300 Mbps** — un goulot d'étranglement immédiat.

### 1.4 Trois « valeurs de référence » à mesurer d'abord

Avant de modifier le moindre matériel, enregistrez les chiffres actuels (ces données servent aussi de remise Intake pour le support après-vente) :

```bash
# 1) Noyau et système
uname -r
grep PRETTY /etc/os-release

# 2) Interface sans fil et signal actuels
iw dev                      # liste les interfaces sans fil
iw dev wlan0 link           # affiche l'AP, le canal, le RSSI et le bitrate actuels

# 3) Utilisation du canal côté AP (à exécuter sur l'AP, ou consulter son WebUI)
#    Ligne de base de détection de connectivité
ping -c 60 -i 1 <IP_PASSERELLE_AP>
```

Notez le RSSI, le bitrate, la latence ping et le taux de perte de paquets de la « carte ancienne / bande ancienne » — vous les comparerez au 6GHz à la fin du chapitre 3.

---

## 2. Configuration de l'AWUS036AXML Wi-Fi 6E sous JetPack (Ubuntu 22.04 LTS)

### 2.1 Vérifiez d'abord la version du noyau de votre JetPack

L'avantage principal de l'AWUS036AXML est que **le pilote `mt7921u` du chipset MediaTek MT7921AU est intégré nativement au noyau principal de Linux** (inclus depuis Kernel 5.18) — **aucune compilation de pilote depuis GitHub n'est nécessaire**. Mais le « support natif » a un seuil ; vérifiez d'abord la version de votre noyau :

```bash
uname -r
```

Tableau de référence :

| JetPack | Système d'exploitation de base | Linux Kernel | Support de l'AWUS036AXML |
|---|---|---|---|
| JetPack 5.1.x | Ubuntu 20.04 (à vérifier soi-même) | 5.10 | Pilote à vérifier ; nous recommandons de passer directement à JetPack 6.x |
| JetPack 6.0 / 6.1 | Ubuntu 22.04 LTS | 5.15 | Selon la version du noyau ; exécutez d'abord `modinfo mt7921u` |
| JetPack 6.2+ (recommandé) | Ubuntu 22.04 LTS | 6.1 | `mt7921u` intégré nativement, plug and play |

Vérifiez que le pilote et le firmware sont prêts :

```bash
modinfo mt7921u                         # avec sortie = le pilote est intégré au noyau
sudo apt update
sudo apt install linux-firmware         # garantir le firmware MediaTek le plus récent
sudo reboot
```

> **Limite de support (Support Reduction)** : l'AWUS036AXML **ne prend pas en charge macOS (ni Intel ni Apple Silicon)**. JetPack ne fonctionne que dans l'environnement Ubuntu 22.04 LTS exclusif de Jetson, et toutes les commandes de cet article supposent Linux ; si votre machine de développement est un Mac, utilisez n'importe quelle machine Linux comme nœud de calcul de périphérie.

### 2.2 Connexion de l'adaptateur au Jetson : ports USB et alimentation

Le Jetson Orin Nano Developer Kit offre 2 ports USB 3.2 Type-A (bleus) et 2 ports USB 2.0. L'AWUS036AXML utilise une interface **USB-C 3.2 Gen1** et est livré avec un câble 2-en-1 (USB-C vers USB-A) pour l'alimentation et les données :

```bash
# Après branchement, confirmez que la couche USB reconnaît l'appareil (le VID:PID du MediaTek MT7921AU est 0e8d:7961)
lsusb | grep -i mediatek
```

**Avertissement d'alimentation (un tueur fréquent en pratique)** :

- L'AWUS036AXML consomme environ **2.7W au maximum** ; le branchement direct sur le port USB 3.2 du Jetson ne pose généralement pas de problème.
- Si vous utilisez plusieurs adaptateurs haute puissance, un SSD externe et des caméras USB en même temps, **nous recommandons un hub USB avec alimentation indépendante (Powered Hub)** pour éviter les chutes de tension instantanées qui font « apparaître et disparaître » l'adaptateur.
- N'utilisez pas de câbles d'extension ni de répartiteurs de panneau avant ; plus le câble USB est court et épais, mieux c'est.

### 2.3 Connexion au point d'accès et verrouillage de la bande

JetPack gère les réseaux sans fil avec NetworkManager :

```bash
# Analyse et connexion
nmcli device wifi list
nmcli device wifi connect "VOTRE_SSID" password "VOTRE_MOT_DE_PASSE"
```

**Verrouillage de la bande (étape cruciale)** : la valeur `nmcli band` est `bg` pour le 2.4GHz et `a` pour le 5GHz ; **le 6GHz du Wi-Fi 6E utilise `a` (étendu)**. La méthode la plus fiable consiste à créer un SSID dédié « **6GHz uniquement** » du **côté du point d'accès** et à désactiver Band Steering, puis à confirmer à quelle bande le client s'est réellement connecté via le contenu du canal physique :

```bash
# Confirmez le canal de connexion actuel (les fréquences 6GHz se situent entre 5925–7125 MHz)
iw dev wlan0 link

# Une façon propre de confirmer : regardez dans quelle bande tombe la fréquence
iw dev wlan0 link | grep -i freq
#   2.4GHz → 2400-2500 MHz
#   5GHz   → 4900-5900 MHz
#   6GHz   → 5925-7125 MHz (exclusif au Wi-Fi 6E)
```

Si vous ne voulez pas que le client erre vers les 2.4/5GHz congestionnés, fixez-le dans les paramètres de connexion :

```bash
nmcli c show --active                       # trouvez le nom de la connexion
nmcli con mod "NOM_CONNEXION" 802-11-wireless.band a
nmcli con up "NOM_CONNEXION"
```

> **Avertissement réglementaire** : la disponibilité de la bande 6GHz dépend des réglementations de votre pays/région et du **firmware du point d'accès**. À Taïwan, par exemple, la NCC a ouvert la plage **5945–6425 MHz** pour le 6GHz, **uniquement en intérieur à faible puissance** — pas la plage complète de 5925–7125 MHz. Si `iw reg get` affiche un domaine réglementaire (regulatory domain) sans 6GHz, ou si l'AP n'a pas activé le 6GHz, l'adaptateur ne se connectera tout simplement pas — ce n'est pas une panne matérielle, c'est un problème réglementaire/de configuration.

---

## 3. 6GHz vs 2.4G/5G congestionnés : mesure de la bande passante et de la latence

> L'esprit de la mesure : **le même Jetson, le même adaptateur, le même AP, la même distance** — seule la bande change, toutes les autres conditions restent identiques. Ainsi, l'écart mesuré est l'écart de la « bande » elle-même.

### 3.1 Concevez votre expérience contrôlée

| Variable | Méthode de contrôle |
|---|---|
| Emplacement de l'AP | Fixe ; les trois bandes partagent le même AP Wi-Fi 6E |
| Distance | Fixe (par exemple 3 mètres en ligne droite sans obstacle) |
| Période | Même jour, heures similaires (la congestion 2.4/5GHz se mesure sur site) |
| Adaptateur | Le même AWUS036AXML, seul le SSID change |
| Environnement d'interférences | On conserve les interférences existantes (c'est tout l'intérêt de la « mesure réelle ») |

### 3.2 Mesure 1 : RSSI et débit de liaison unique (iperf3)

Installez iperf3 sur le Jetson et connectez-le à une machine réceptrice :

```bash
# Côté récepteur (par exemple un autre ordinateur ou serveur)
iperf3 -s

# Côté Jetson (client, exécution bidirectionnelle de 60 secondes)
iperf3 -c <IP_RÉCEPTEUR> -t 60 -R     # -R mesure reverse (upload du Jetson)
```

Exécutez-le une fois sur chaque **SSID 2.4GHz, SSID 5GHz et SSID 6GHz**, en notant `sender Mbps` et `receiver Mbps`. Vous pouvez aussi observer d'abord la qualité de la liaison :

```bash
iw dev wlan0 link                              # RSSI + bitrate PHY actuel
iw dev wlan0 station dump | grep -E "signal|tx bitrate|rx bitrate"
```

### 3.3 Mesure 2 : connectivité et latence (ping)

```bash
ping -c 60 -i 1 <IP_RÉCEPTEUR> | tail -2
```

Notez pour les trois groupes : **latence moyenne (ms)**, **taux de perte de paquets (%)** et **gigue de latence (max-min)**.

### 3.4 Mesure 3 : streaming RTSP 4K multicanal réel (test de charge GStreamer)

Le débit et la latence ne sont que des indicateurs indirects ; **ce qu'il faut vraiment vérifier, c'est « combien de flux 4K peuvent être décodés simultanément sans perte d'images »**. JetPack inclut le plugin de décodage matériel NVIDIA pour GStreamer 1.0 (`nvv4l2decoder`) :

```bash
# Utilisez l'élément perf pour compter le taux réel d'images décodées (échantillonnage toutes les 1 seconde)
gst-launch-1.0 \
  rtspsrc location="rtsp://IP_CAMÉRA/stream" ! \
  rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! \
  perf print-stats=true ! fakesink
```

Ouvrez plusieurs terminaux, un par flux 4K, et observez le GPU/la mémoire avec `nvidia-smi` (`tegrastats` sur Jetson) :

```bash
sudo tegrastats
```

**Critères d'évaluation** :
- Si le `perf` de chaque flux affiche un **taux d'images dropped/rendered (FPS) qui se rapproche de manière stable du taux source (30fps)** → réussi.
- Si sur 2.4/5GHz des images sont perdues ou la qualité chute, et qu'après passage en 6GHz la stabilité revient → c'est la preuve mesurée de la « congestion de bande ».

### 3.5 Un exemple de résultats de mesure attendus

| Bande | PHY bitrate | iperf3 réel upload/download | ping moyen/gigue | Résultat streaming 4K multicanal |
|---|---|---|---|---|
| 2.4GHz (bureau congestionné) | 300 Mbps | 80–120 Mbps | 8 ms / gigue élevée, pertes occasionnelles | Chute de qualité, image brumeuse |
| 5GHz (occupation modérée) | 800 Mbps | 400–550 Mbps | 3 ms / moyenne | Fonctionne difficilement, saccades occasionnelles |
| 6GHz (SSID dédié propre) | 1200 Mbps | 700–900 Mbps | 1–2 ms / stable | 2–4 flux 4K, tout au vert |

> C'est le contraste typique entre « propre et congestionné ». **La valeur du 6GHz réside dans le fait que c'est une bande toute neuve que presque personne n'utilise.** Dans les environnements denses en caméras et saturés d'appareils Wi-Fi, cet avantage se transforme immédiatement en capacité stable pour le 4K multicanal.

---

## 4. Liste de vérification de compatibilité avant achat (Pre-Purchase Checklist)

> Cochez chaque point avant de commander. **Remplir cette liste avant d'acheter économise dix fois l'effort de dépannage après l'achat.**

### Étape 1 : confirmez votre plateforme de calcul de périphérie

| Élément de vérification | Comment vérifier | Résultat |
|---|---|---|
| Modèle de plateforme | `cat /proc/device-tree/model` | \_\_\_\_\_ |
| Version JetPack | `cat /etc/nv_tegra_release` (JetPack 6.x = L4T 36.x) | \_\_\_\_\_ |
| Linux Kernel | `uname -r` | \_\_\_\_\_ |
| `mt7921u` intégré ? | `modinfo mt7921u` | avec sortie / sans sortie |

> Si `uname -r` est inférieur à 5.18 et que `modinfo mt7921u` ne produit aucune sortie : mettez d'abord à jour JetPack (recommandé 6.2+, Kernel 6.1) avant de parler de la carte. **Ne compilez pas de force des pilotes non principaux sur un ancien noyau** — cela n'en ferait que le héros d'un autre article de dépannage.

### Étape 2 : confirmez votre environnement sans fil

| Élément de vérification | Options / conditions |
|---|---|
| L'AP prend-il en charge le Wi-Fi 6E (6GHz) ? | Oui / Non (sans AP 6GHz, les bénéfices de cet article sont inaccessibles) |
| Le 6GHz est-il activé côté AP ? | Oui / Non (y compris les réglages regulatory domain / country code) |
| Existe-t-il un SSID dédié « 6GHz uniquement » ou verrouillable en 6GHz ? | Oui / Non |
| Estimation du trafic total des caméras | Combien de flux 4K ? H.264/H.265 ? Total environ \_\_\_ Mbps |
| Distance et obstacles | Combien de mètres ? Y a-t-il des murs/obstructions métalliques ? |

### Étape 3 : confirmez la couverture de support des systèmes d'exploitation

| Plateforme | Statut de support |
|---|---|
| Ubuntu 22.04 / 24.04 | ✅ `mt7921u` natif (Kernel 5.18+ ; s'applique à JetPack 6.2+) |
| Kali Linux | ✅ Support natif (Monitor Mode / Packet Injection) |
| Windows 11 | ✅ (la bande 6GHz nécessite Windows 11 ou plus récent) |
| Windows 10 | ✅ (mais sans bande 6GHz ; 2.4/5GHz uniquement) |
| macOS (Intel / Apple Silicon) | ❌ **Non pris en charge** (pas de pilote MT7921AU pour macOS ; ne l'achetez pas pour cela) |
| Raspberry Pi / autres SBC Linux | ✅ (Kernel 5.18+, nécessite l'installation de `linux-firmware`) |

> **Rappel de la limite de support** : l'AWUS036AXML **ne prend pas en charge macOS**. Si votre machine de développement principale est un Mac, la fonction Wi-Fi de cette carte ne fonctionnera pas sur votre Mac ; assurez-vous d'avoir une machine Linux ou une SBC Linux comme plateforme d'utilisation.

### Étape 4 : vérification de l'alimentation et des ports

| Élément de vérification | Recommandation |
|---|---|
| Branchement direct sur le port USB de la machine | Possible (2.7W, faible consommation) |
| Plusieurs appareils simultanés | Utilisez un **hub USB avec alimentation indépendante (Powered USB Hub)** |
| Placement des antennes | Deux antennes omnidirectionnelles RP-SMA 5dBi à la verticale, à ≥ 5cm du châssis métallique |

### Paquet d'informations Intake pour le service client

Si vous rencontrez encore des problèmes après l'achat, joignez **tout d'un coup** lors de la prise de contact avec le support technique : modèle de plateforme, version JetPack/noyau, sortie de `lsusb`, résultat de `modinfo mt7921u`, RSSI/bitrate de `iw dev wlan0 link`, et le modèle de l'AP avec ses réglages de bande. Ces informations leur permettent de déterminer directement s'il s'agit d'une « réglementation non ouverte », d'une « configuration de l'AP » ou d'un « matériel ».

---

## 5. Avertissement et lignes rouges de sécurité

Cette solution est une **évaluation bench-test pour une plateforme de développement académique/ingénierie open source de type DIY** — pas un support officiel d'un produit commercial, et aucune promesse de « solution commerciale turn-key prête à l'emploi ».

- **Pas de support macOS** : l'AWUS036AXML n'a pas de pilote macOS ; les procédures de cet article ne peuvent pas être utilisées sur un Mac.
- **Aucune revendication de compatibilité officielle avec des plateformes fermées spécifiques** : cet article ne décrit que le Jetson Orin Nano comme carte de développement open source et les environnements Linux généraux ; si votre cible est un **système commercial fermé (drones/robots/vidéo)**, le contenu de cet article ne représente pas la certification officielle de son fabricant ; pour la conversion sans fil, contactez le support technique du fabricant.
- **Aucun système critique pour la sécurité** : si votre application relève de systèmes de contrôle critiques pour la sécurité industrielle (Safety-critical control systems), n'intégrez pas la transmission vidéo sans fil directement dans la boucle de sécurité ; conservez les canaux filaires ou les canaux de sécurité existants.
- **Aucune instruction pour désactiver les protections système** : tous les réglages de cet article fonctionnent avec les protections activées ; ne désactivez pas le pare-feu, Secure Boot ou autres pour contourner des problèmes réseau.
- **Respect de la réglementation radio** : l'utilisation du 6GHz doit être conforme aux normes de votre pays/région ; cet article n'explique que la configuration technique et ne constitue pas un conseil réglementaire.

---

## Conclusion et recommandations matérielles

Lorsque la vidéo 4K multicanal entre dans une plateforme d'IA de périphérie, le goulot d'étranglement ne se situe souvent pas dans la puissance de calcul, mais dans la **capacité de charge sans fil et la propreté des canaux**. Les 2.4G/5G sont déjà submergés d'appareils ; **le 6GHz du Wi-Fi 6E offre un canal tout neuf sans interférences** — associé à un adaptateur à pilote natif sans compilation, le Jetson Orin Nano peut absorber de manière stable 2–4 flux 4K, repoussant d'un coup le problème du « plafond de bande passante ».

**Matériel recommandé** : ALFA AWUS036AXML (MediaTek MT7921AU, support natif sans compilation sur Linux Kernel 5.18+, Wi-Fi 6E tribande, double antenne RP-SMA 5dBi à haut gain, faible consommation 2.7W). L'AWUS036AXMR, basé sur la même architecture de chipset, est le modèle embarqué sans antennes, adapté aux nœuds de périphérie en rack à espace limité.

**Prochaine étape** : exécutez d'abord les « mesures de référence » du chapitre 1, puis cochez la liste du chapitre 4 — emportez les données de mesure sur le terrain et laissez les données décider de votre stratégie de bande.