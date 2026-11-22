---
title: "L'audit sans fil à l'ère du WPA3-SAE : capacité de capture de handshake des 9 cartes ALFA mesurée, et le piège de compatibilité sae_pwe pour la connexion des iPhone"
slug: alfa-wpa3-sae-handshake-capability-arm64
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-wpa3-sae-handshake-capability-arm64.webp"
bannerimage: "/images/blog/banner/alfa-wpa3-sae-handshake-capability-arm64.webp"
author: "benny-lai"
tags:
  - wpa3-sae
  - wpa-handshake
  - sae-pwe
  - wireless-security
  - alfa-network
  - rtl8821cu
  - hcxpcapngtool
  - wifi-6
description: "Capacité de capture de handshake WPA3-SAE des cartes ALFA sous Ubuntu (extensible à Kali) mesurée : taux d'injection des 9 cartes et résultats de capture .22000 de bout en bout, piège de compatibilité sae_pwe et conseils de choix."
faq:
  - question: "L'AWUS036AXM peut-elle capturer un handshake WPA sous Ubuntu ?"
    answer: "Pas sur cette plateforme. En test, l'AWUS036AXM et l'AWUS036AXML (puce MT7921), du fait de l'échec d'injection, ne peuvent pas émettre de deauth, et toute la chaîne de capture du 4-way handshake se rompt du même coup ; inadaptées à un usage nécessitant la capture de handshake."
  - question: "Quelle carte Wi-Fi ALFA capture le plus fiablement un handshake WPA ?"
    answer: "En test, l'AWUS036EACS est la plus solide : 100 % d'injection sur les deux bandes, 79 ACKs reçus après le deauth, et export réussi d'un fichier .22000 exploitable par hashcat — le bout en bout le plus complet du lot."
  - question: "Pourquoi l'ancien iPhone ne se connecte-t-il pas au point d'accès WPA3-SAE ?"
    answer: "La clé est le paramètre sae_pwe de hostapd : réglé à 2 (H2E forcé), l'iPhone 7 Plus échoue à se connecter ; en revenant à sae_pwe=0 (Hunting-and-Pecking), il complète normalement le 4-way et se connecte."
  - question: "Peut-on encore capturer un 4-way handshake en environnement WPA3 ?"
    answer: "Un environnement WPA3-SAE pur force l'activation du PMF (ieee80211w=2), et les méthodes traditionnelles visant les frames de gestion sont bloquées ; si l'on capture encore un handshake en pratique, c'est le plus souvent parce que la cible tourne en mode de transition WPA2/WPA3, et non en WPA3 pur."
  - question: "Si l'injection 5 GHz d'une carte ALFA ne se mesure pas, est-ce un problème matériel ?"
    answer: "Pas forcément. Le domaine réglementaire par défaut limite la puissance d'émission d'une partie des bandes 5 GHz, empêchant l'injection de « sortir » ; en test, après basculement du domaine réglementaire vers un état émetteur, l'injection 5 GHz auparavant en échec devient utilisable — il est conseillé de vérifier d'abord le réglage du domaine réglementaire avant de conclure à une limite matérielle."
draft: false
---

> Unité de test : Yopitek (distributeur ALFA Network à Taïwan) | Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 | Appareil de test : notre propre iPhone 7 Plus (WPA3 aussi testé sur iPhone 15 Pro) | Cible de test : notre propre Wi-Fi de bureau (SSID YUPITEK, 2,4G ch5 / 5G ch36, 157).
>
> Cet article est une vue d'ensemble des capacités et de la compatibilité des cartes Wi-Fi ALFA. Toutes les captures Monitor / Injection / handshake sont réalisées sur les propres équipements de Yopitek, son propre Wi-Fi de bureau, à destination de ses propres téléphones de test : il s'agit d'une vérification matérielle légitime par le distributeur ; elle ne vise aucun réseau tiers et ne fournit aucune procédure offensive.

## L'essentiel (TL;DR)

Sur les 9 cartes ALFA testées sur ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17), 7 (ACM, ACHM, ACH, ACS, EACS, AX, AXER) ont réalisé la capture de handshake WPA de bout en bout jusqu'au `.22000` ; l'AWUS036EACS a atteint 100 % d'injection bi-bande avec 79 ACKs, tandis que les AXM / AXML à base de MT7921 échouent à l'injection sur cette plateforme.

- Avec la généralisation du WPA3-SAE, le cœur de l'audit passe de « peut-on faire du monitor » à « la capacité de capture de handshake de bout en bout » et « la compatibilité de terminal `sae_pwe` ».
- **Bout en bout `.22000` prouvé pour 7 cartes sur 9** : ACM, ACHM, ACH, ACS, EACS, AX, AXER ; l'EACS étant la plus solide (injection bi-bande 100 %, 79 ACKs).
- **L'AXM / AXML (MT7921) échouent à l'injection sur cette plateforme**, ne peuvent pas faire de deauth, ne capturent pas de handshake — à éviter absolument pour l'audit.
- Piège `sae_pwe` : les anciens iPhone nécessitent `sae_pwe=0` pour se connecter ; avant une injection 5G, déverrouillez le TX via `iw reg set US`.
- Le WPA3 pur force le PMF (`ieee80211w=2`) ; si l'on capture encore sur le terrain, c'est le plus souvent parce que la cible tourne en mode de transition WPA2/WPA3.

## 1. La généralisation du WPA3-SAE a relevé toute la barre de l'audit sans fil

Pendant la dernière décennie, l'audit sans fil autorisé (authorized wireless audit) tournait presque entièrement autour du 4-way handshake du WPA2-PSK : capturer une poignée de main complète, et le back-end pouvait comparer hors ligne. Mais depuis que la certification Wi-Fi 6 a intégré le WPA3 comme élément obligatoire, le SAE (Simultaneous Authentication of Equals, surnommé Dragonfly) remplace progressivement le PSK, et bouche de plus en plus l'ancienne voie « capturer la poignée de main, vérifier hors ligne ».

Pour les distributeurs et les ingénieurs de première ligne, le WPA3-SAE apporte trois changements pratiques :

1. **Le PMF (Protected Management Frame) devient obligatoire**. La norme WPA3-SAE force l'activation de `ieee80211w=2` ; les management frames sont protégés, et l'ancienne pratique « un deauth improvisé pour déconnecter un appareil » est directement bloquée en environnement WPA3 pur.
2. **Le mode de transition (transition mode) conserve le 4-way**. Dans la réalité, de nombreux AP tournent en mode de transition mixte WPA2/WPA3, conservant le 4-way handshake du WPA2 pour la compatibilité avec les anciens appareils : c'est la principale raison pour laquelle l'audit autorisé capture encore des poignées de main aujourd'hui. Pouvoir capturer ou non dépend en grande partie du mode dans lequel la cible du terrain est configurée.
3. **La compatibilité de terminal devient un nouveau piège**. Le SAE a différentes manières de dériver l'élément de mot de passe (contrôlées par `sae_pwe`) ; un mauvais paramètre d'AP, et même votre propre ancien iPhone ne se connecte pas, sans parler de reproduire le comportement de connexion du terminal client sur le terrain d'audit.

Ainsi, quand un client demande « quelle carte ALFA utiliser pour un audit autorisé lié au WPA3 », la réponse n'est plus aussi simple que « peut-elle faire du monitor » ; il faut regarder deux choses : **la capacité de capture de handshake de bout en bout**, et **la compatibilité avec les paramètres WPA3-SAE et les terminaux réels**. Ce rapport est le comparatif de capacités établi après des tests des 9 cartes ALFA sur une même plateforme ARM64.

## 2. Ce qu'on entend par « capacité de capture de handshake de bout en bout » (niveau conceptuel)

Décomposons d'abord la capacité en trois segments, en explication purement conceptuelle, sans aucune commande d'opération visant un réseau tiers :

- **Segment 1 : Injection (injection active)**. La carte doit pouvoir « émettre » des frames de gestion spécifiques pour amener un client déjà connecté à se réassocier. Beaucoup de cartes ne font que du monitor passif (recevoir des paquets) sans pouvoir injecter (émettre activement). C'est le segment le plus susceptible de bloquer toute la chaîne. Ce lot de tests quantifie le taux de réussite d'injection avec `aireplay-ng --test`, et vérifie, dans le test de handshake, via le nombre d'ACKs renvoyés par le client, si les frames sont réellement parvenus.
- **Segment 2 : Capture du 4-way handshake**. Lorsque le client se réassocie, le WPA échange quatre messages EAPOL (M1–M4). En mode monitor, la carte doit capturer ces quatre frames au complet, sans en manquer un seul.
- **Segment 3 : Export en hashcat `.22000`**. Convertir le pcap capturé au format hashcat `.22000` avec `hcxpcapngtool --all`, pour une vérification hors ligne par le back-end.

**Les trois segments doivent tenir sur machine réelle pour que ce soit « de bout en bout »** : envoyer réellement un deauth vers notre propre iPhone 7 Plus (injection) → capturer les M1–M4 complets → exporter et déposer le `.22000`. Ne capturer sans pouvoir émettre, ou ne pas réunir les quatre frames, ou ne pas réussir l'export, ne compte pas comme bout en bout. Cet article ne liste aucune commande offensive pas à pas ; le comparatif ci-dessous répond à une seule question : quelle carte parvient au bout de cette chaîne de capacités.

Avec l'EACS, la plus solide du lot, un bout en bout réussi ressemble à ceci : après l'envoi du deauth, le client renvoie **79 ACKs** (confirmant que les frames parviennent bien à ce téléphone), `aircrack-ng` retient 1 handshake sur YUPITEK, les quatre frames EAPOL M1 / M2 / M3 / M4 sont reçus une fois chacun, la MAC du client capturé commence par un OUI Apple (confirmant que c'est bien cet iPhone 7 Plus), et enfin `hcxpcapngtool --all` exporte un `.22000` d'environ 784 bytes. Si l'une de ces quatre conditions manque, la capture ne compte pas. C'est aussi pourquoi « pouvoir faire du monitor » et « pouvoir capturer de bout en bout » sont deux choses totalement différentes.

## 3. Tableau comparatif de la capacité de handshake des 9 cartes

| # | Modèle | Puce / génération | Injection 2,4G | Injection 5G | Capacité de capture de handshake WPA |
|---|---|---|---|---|---|
| 1 | AWUS036ACM | MT7612U / Wi-Fi 5 · 2T2R | disponible 63–83% | disponible 76% | **bout en bout `.22000` prouvé** (taux d'injection plus faible) |
| 2 | AWUS036ACHM | MT7610U / Wi-Fi 5 · 1T1R | disponible 96–100% | diffusion uniquement | **bout en bout `.22000` prouvé (en 5 GHz ch36)** |
| 3 | **AWUS036ACH** | RTL8812AU / Wi-Fi 5 · 2T2R | **100%** | **100%** | **bout en bout `.22000` prouvé (revérifié le 2026-11-19)** |
| 4 | **AWUS036ACS** | RTL8811AU / Wi-Fi 5 · 1x1 | **100%** | 96% | **bout en bout `.22000` prouvé** |
| 5 | **AWUS036EACS** | RTL8821CU / Wi-Fi 5 · 1x1 | **100%** | **100%** | **bout en bout `.22000` prouvé (79 ACKs)** |
| 6 | **AWUS036AX** | RTL8832BU / Wi-Fi 6 · 2x2 | 96% | disponible | **bout en bout `.22000` prouvé** |
| 7 | **AWUS036AXER** | RTL8832BU / Wi-Fi 6 · 2x2 | 73% | disponible | **bout en bout `.22000` prouvé** |
| 8 | AWUS036AXM | MT7921AUN / Wi-Fi 6 · 2x2 | échec | échec | non pris en charge : injection en échec, capture impossible |
| 9 | AWUS036AXML | MT7921AUN / Wi-Fi 6 · 2x2 | échec | échec | non pris en charge : injection en échec, capture impossible |

**Deux niveaux, visibles d'un coup d'œil :**

- **Bout en bout prouvé (capture → dépôt de fichier `.22000`, 7 cartes sur 9)** : AWUS036ACM, AWUS036ACHM, AWUS036ACH, AWUS036ACS, AWUS036EACS, AWUS036AX et AWUS036AXER. L'EACS, avec 100 % d'injection sur les deux bandes et 79 ACKs reçus au deauth, est la plus solide en capacité de handshake du lot ; l'AWUS036ACH (RTL8812AU, fort gain bi-antenne), à 100 % d'injection sur les deux bandes, a exporté un `.22000` de 47 hashlines en revérification le 2026-11-19, au même rang que l'EACS comme premier choix de test d'intrusion. **Sept modèles ont mené à terme la capture de handshake de bout en bout : ACM, ACHM, ACH, ACS, EACS, AX, AXER.** L'ACM injecte à un taux plus faible (2,4G 63–83 % / 5G 76 %) et l'ACHM l'a réussie en 5 GHz (ch36), mais les deux ont produit un `.22000`.
- **Capture impossible (2 cartes)** : AWUS036AXM et AWUS036AXML (le MT7921 échoue à l'injection sur cette plateforme, ne peut pas faire de deauth et ne capture donc naturellement pas de handshake).

À nommer en particulier : l'**AXM / AXML**. Les deux sont Wi-Fi 6, leur monitor et leur AP sont normaux, mais l'injection seule ne fonctionne pas sur cette plateforme — la cause principale est la régression du chanctx de mac80211 du stock kernel 6.16+ (pas intrinsèque à la puce) ; un pilote git / patché sur le même modèle peut fonctionner dans la communauté, mais le firmware verrouille le débit (correspond à morrownr/USB-WiFi #387, morrownr/mt76 #18). La navigation et le point d'accès ne posent aucun problème, mais **pour tout usage d'audit nécessitant l'injection ou la capture de handshake, à éviter systématiquement sur cette plateforme**.

## 4. Pièges de compatibilité WPA3-SAE : un mauvais paramètre, et même votre propre iPhone ne se connecte pas

Au-delà de la capacité, la compatibilité des paramètres WPA3-SAE est l'endroit le plus propice au dérapage sur le terrain. Ce lot de tests a buté sur deux pièges clés :

### 4-1. L'ACHM exige `sae_pwe=0`, sans quoi l'iPhone 7 Plus ne se connecte pas

La dérivation de l'élément de mot de passe du SAE a différentes méthodes, contrôlées par `sae_pwe` dans hostapd. En montant l'AWUS036ACHM en WPA3-SAE pur (`wpa_key_mgmt=SAE` + PMF obligatoire `ieee80211w=2`), dès que `sae_pwe` est réglé à `2`, **l'iPhone 7 Plus ne se connecte tout simplement pas** ; en revenant à `sae_pwe=0` (Hunting-and-Pecking, compatible avec les anciens terminaux), l'iPhone 7 Plus (iOS 15) se connecte alors sans problème et complète le 4-way.

L'intérêt de ce piège : pour « reproduire » sur un terrain d'audit un environnement WPA3 dominé par d'anciens terminaux iOS, le `sae_pwe` côté AP doit s'accorder aux capacités du terminal, sans quoi vous obtiendrez un faux négatif « ne se connecte pas », au lieu d'une vraie conclusion de compatibilité. Les tests d'AP WPA3-SAE de l'EACS et de l'ACS adoptent aussi `sae_pwe=0` + `ieee80211w=2`, et l'iPhone 7 Plus se connecte dans les deux cas ; `sae_pwe=0` est la valeur sûre vérifiée sur les anciens terminaux iPhone dans ce lot.

### 4-2. Avant une injection 5G, déverrouillez le TX via `iw reg set US`

Le second piège concerne le domaine réglementaire (regulatory domain). Le `reg=TW` par défaut verrouille le TX sur une partie des bandes UNII, empêchant l'injection / le deauth 5 GHz de « sortir ». Ce lot déverrouille systématiquement le TX via `iw reg set US` avant une injection 5G, puis restaure immédiatement via `iw reg set TW` après le test. L'injection 5G de l'ACS passe d'échec à 96 % après déverrouillage, l'EACS et l'ACH montent directement à 100 %. Oublier de déverrouiller le reg ferait prendre une carte à l'injection normale pour une carte « 5G inutilisable ».

### 4-3. À noter au passage : le PMF est obligatoire en WPA3

La norme WPA3-SAE force `ieee80211w=2` (Management Frame Protection). Cela signifie qu'en environnement WPA3 pur, les méthodes traditionnelles visant les management frames sont bloquées par le PMF ; si l'audit réel capture encore un 4-way, c'est le plus souvent parce que la cible tourne encore en mode de transition WPA2/WPA3. Intégrez ce point au choix de carte pour ne pas nourrir de fausses attentes face à une cible WPA3 pure.

## 5. Vue d'ensemble de la chaîne d'outils : celle qui tourne réellement en ARM64

Au-delà des capacités matérielles, la chaîne d'outils de la plateforme influe aussi sur l'efficacité de l'audit. Voici quelques enseignements tirés de ce lot sur le GX10 (ARM64) :

- **Export systématique avec `hcxpcapngtool --all`**. Les paramètres par défaut sont assez stricts et renvoient souvent « not enough M1 » sans exporter ; en ajoutant `--all`, on exporte le `.22000` de façon stable à partir des M1–M4 complets.
- **Quand plusieurs AP homonymes sont au bureau, ne verrouillez pas `--bssid`**. Le bureau de Yopitek a plusieurs AP YUPITEK homonymes sur un même canal, et l'iPhone se connecte au signal le plus fort. Verrouiller un seul BSSID avec `--bssid` à la capture risque de filtrer celui auquel l'iPhone est réellement connecté et de faire échouer toute la capture. La conclusion mesurée est de **ne pas verrouiller de BSSID et de capturer directement tout le canal**, puis de sélectionner la poignée de main complète dans le fichier déposé.
- **`hcxdumptool` 8.x échoue en `failed to arm` sur cette plateforme, sauf l'EACS en 2,4 GHz (échec en 5 GHz)**. Ni rtw88, ni rtw89, ni mt7921u ne fournissent l'active-monitor, que hcxdumptool 8.x exige ; la solution est de passer au flux aircrack-ng traditionnel `airodump-ng` + `aireplay-ng`.
- **Si plus rien n'est détecté après des bascules répétées de mode, débranchez/rebranchez d'abord la carte**. Les rtw88 / rtw89 peuvent connaître un RX stall (balayage à 0 paquet) après des bascules répétées monitor / AP ; une ré-énumération USB y remédie, et le nom d'interface, déterminé par la MAC, ne change pas au rebranchement. Avant de capturer un handshake, il est conseillé de rebrancher la carte une fois en premier.
- **Les dispositifs composites BT+WiFi (EACS / AXML) ont une condition de concurrence au rebranchement**. Les cartes composites avec Bluetooth peuvent, au rebranchement ou sur certains ports USB, avoir leur fonction Wi-Fi bloquée en probe, sans créer d'interface `wlx` ; la solution est de rebrancher sur un autre port USB, `modprobe` ou le bind manuel étant le plus souvent inefficaces.
- **Subtilités d'installation d'outils en ARM64**. aircrack-ng manque souvent de paquet précompilé en aarch64 et doit être compilé depuis les sources ; wifite s'utilise en version git (la version apt entre en conflit de dépendances avec l'aircrack-ng compilé maison).
- **Règle de sécurité : jamais de `airmon-ng check kill`**. Le GX10 accède à Internet via sa carte intégrée ; `check kill` arrête NetworkManager et déconnecte la machine. Ce lot opère exclusivement sur l'interface `wlx*` de la carte ALFA, sans toucher à la ligne principale d'accès Internet intégrée.

## 6. Synthèse du choix : pour un audit lié au WPA3, quels modèles choisir

En considérant ensemble la capacité, la compatibilité et la chaîne d'outils de la plateforme, pour un usage « d'audit autorisé lié au WPA3 », la recommandation de ce lot est :

| Scénario de besoin | Modèle conseillé | Raison |
|---|---|---|
| Premier choix global (injection + handshake de bout en bout) | **AWUS036EACS** | Injection bi-bande 100 %, 79 ACKs au deauth, bout en bout `.22000` prouvé ; seul point à surveiller : dispositif composite BT+WiFi, changer parfois de port USB au rebranchement |
| Fort gain / longue portée + injection forte | **AWUS036ACH** | RTL8812AU bi-antenne, injection bi-bande 100 %, forte capacité de réception |
| Nomade léger | **AWUS036ACS** | Flux unique, bout en bout `.22000` prouvé, injection 5G 96 % |
| Besoin Wi-Fi 6 | **AWUS036AX / AWUS036AXER** | 2x2 VHT80, bout en bout `.22000` prouvé ; l'AXER à antenne intégrée (Nano) + réglage de la puce a la plus large couverture de balayage |
| **À éviter absolument** | AWUS036AXM / AWUS036AXML | Le MT7921 échoue à l'injection sur cette plateforme, capture de handshake impossible |

En une phrase : **pour un audit lié au WPA3, priorité à l'EACS, puis l'ACH / ACS ; pour le Wi-Fi 6, choisissez l'AX / AXER ; évitez absolument l'AXM / AXML.** Parmi les sept cartes ayant mené à terme la capture de handshake de bout en bout, les Realtek (rtw88 / rtw89) peuvent toutes injecter, et côté MediaTek l'ACM et l'ACHM (mt76) y sont aussi parvenues ; les MT7921 AXM / AXML en sont incapables. Au moment du choix, reconnaître la puce est plus fiable que reconnaître le nom du modèle.

## Questions fréquentes (FAQ)

**Q : L'AWUS036AXM peut-elle capturer un handshake WPA sous Ubuntu ?**
R : Pas sur cette plateforme. En test, l'AWUS036AXM et l'AWUS036AXML (puce MT7921), du fait de l'échec d'injection, ne peuvent pas émettre de deauth, et toute la chaîne de capture du 4-way handshake se rompt du même coup ; inadaptées à un usage nécessitant la capture de handshake.

**Q : Quelle carte Wi-Fi ALFA capture le plus fiablement un handshake WPA ?**
R : En test, l'AWUS036EACS est la plus solide : 100 % d'injection sur les deux bandes, 79 ACKs reçus après le deauth, et export réussi d'un fichier `.22000` exploitable par hashcat — le bout en bout le plus complet du lot.

**Q : Pourquoi l'ancien iPhone ne se connecte-t-il pas au point d'accès WPA3-SAE ?**
R : La clé est le paramètre `sae_pwe` de hostapd : réglé à 2 (H2E forcé), l'iPhone 7 Plus échoue à se connecter ; en revenant à `sae_pwe=0` (Hunting-and-Pecking), il complète normalement le 4-way et se connecte.

**Q : Peut-on encore capturer un 4-way handshake en environnement WPA3 ?**
R : Un environnement WPA3-SAE pur force l'activation du PMF (`ieee80211w=2`), et les méthodes traditionnelles visant les frames de gestion sont bloquées ; si l'on capture encore un handshake en pratique, c'est le plus souvent parce que la cible tourne en mode de transition WPA2/WPA3, et non en WPA3 pur.

**Q : Si l'injection 5 GHz d'une carte ALFA ne se mesure pas, est-ce un problème matériel ?**
R : Pas forcément. Le domaine réglementaire par défaut limite la puissance d'émission d'une partie des bandes 5 GHz, empêchant l'injection de « sortir » ; en test, après basculement du domaine réglementaire vers un état émetteur, l'injection 5 GHz auparavant en échec devient utilisable — il est conseillé de vérifier d'abord le réglage du domaine réglementaire avant de conclure à une limite matérielle.

## 7. Pour aller plus loin

- [Tableau récapitulatif des 9 cartes Wi-Fi ALFA mesurées en ARM64 et évaluation globale de choix](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Tests individuels par modèle : [Test individuel de l'AWUS036EACS](/fr/blog/awus036eacs-asus-gx10-ubuntu-test-report/), [Test individuel de l'AWUS036ACS](/fr/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*Tous les tests de cet article sont réalisés sur le propre Wi-Fi de bureau de Yopitek (SSID YUPITEK), à destination de notre propre iPhone 7 Plus : il s'agit d'une vérification matérielle légitime des cartes Wi-Fi ALFA par le distributeur. Données issues des rapports de tests sur machine réelle du 2026-11-16 au 11-18 ; elles ne visent aucun réseau tiers et ne fournissent aucune procédure offensive. Unité de test : Yopitek (distributeur ALFA Network à Taïwan) — https://www.yupitek.com*
