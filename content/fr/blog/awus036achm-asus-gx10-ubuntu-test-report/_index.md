---
title: "AWUS036ACHM, test carte par carte : le MediaTek MT7610U mono-antenne AC600 sur ASUS GX10 (ARM64 / Ubuntu 24.04) — capacités Monitor · Injection · AP · WPA3"
slug: awus036achm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036achm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036achm
  - alfa-network
  - mt7610u
  - mt76x0u
  - wifi-5
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - sae-pwe
  - ubuntu-24-04
  - arm64
description: "L'AWUS036ACHM (MT7610U) fonctionne sans installation de pilote sous Ubuntu 24.04 : mode monitor bi-bande disponible, injection de paquets 2,4G 96–100 % ; pour ouvrir un AP il faut désactiver le 802.11n, et pour le WPA3 régler sae_pwe=0 afin que les anciens iPhone se connectent."
faq:
  - question: "L'AWUS036ACHM nécessite-t-elle l'installation d'un pilote sous Ubuntu 24.04 ?"
    answer: "Non. Le MT7610U est pris en charge par le pilote mt76x0u intégré au kernel : sous Ubuntu 24.04 (kernel 6.17), la carte est reconnue dès le branchement, sans DKMS ni firmware additionnel ; lsusb affiche l'USB ID 0e8d:7610."
  - question: "L'AWUS036ACHM peut-elle passer en mode monitor ? Combien d'AP détecte-t-elle ?"
    answer: "Oui. Le mode monitor fonctionne en 2,4 GHz comme en 5 GHz ; avec un balayage pleine bande en saut de fréquence via airodump-ng pendant 120 secondes, elle a détecté 19 AP et 14 clients, répartis sur les ch1, 2, 5, 6, 36, 149, 157."
  - question: "Quel est le taux de réussite d'injection de paquets de l'AWUS036ACHM ? Est-ce possible en 5 GHz ?"
    answer: "En 2,4 GHz sur le canal 6, le taux de réponse par cible est de 96–100 % (aireplay-ng --test, 4 AP trouvés). En 5 GHz (ch36, ch149), seule l'injection en diffusion est confirmée ; le test par cible renvoie Found 0 APs, aucun pourcentage n'a été obtenu cette fois-ci, cause à déterminer."
  - question: "Que faire si l'iPhone affiche « Impossible de rejoindre le réseau » ou « Mot de passe incorrect » lorsque l'AWUS036ACHM ouvre un AP ?"
    answer: "Désactivez d'abord le 802.11n : n'ajoutez pas ieee80211n=1 ni ht_capab dans le fichier de configuration hostapd, utilisez un hw_mode=g pur en 2,4 GHz et un hw_mode=a pur en 5 GHz (20 MHz). Sinon hostapd fait apparaître de façon répétée handle_assoc_cb: STA not found : l'écran ressemble à un mot de passe incorrect, mais c'est en réalité un échec d'association 802.11n."
  - question: "Pourquoi les anciens iPhone n'arrivent-ils pas à se connecter au WPA3-SAE de l'AWUS036ACHM ?"
    answer: "C'est le plus souvent le réglage sae_pwe de hostapd. En test, avec sae_pwe=0 l'iPhone 7 Plus et l'iPhone 15 Pro se connectent tous les deux ; avec sae_pwe=2 l'iPhone 7 Plus s'associe mais le 4-way handshake échoue et il est déconnecté, ce qui ressemble à un mot de passe incorrect. Associez ieee80211w=2, et après modification faites d'abord « oublier ce réseau » à l'iPhone avant de le reconnecter."
draft: false
---

> Unité de test : Yopitek (distributeur ALFA Network à Taïwan) | Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia` | Appareil de test : notre propre iPhone 7 Plus (WPA3 aussi testé sur iPhone 15 Pro) | Cible de test : notre propre Wi-Fi de bureau (SSID `YUPITEK`, 2,4G ch5 / 5G ch36, 157).
>
> Cet article est une vérification matérielle, par le distributeur, de la compatibilité produit et des limites de capacités. Tous les tests Monitor / Injection / AP / WPA3 sont réalisés sur les propres équipements de Yopitek, son propre Wi-Fi de bureau, à destination de ses propres téléphones de test : il s'agit d'une vérification de capacités légitime ; elle ne vise aucun réseau tiers et ne fournit aucune procédure offensive. Dans ce texte, l'injection n'envoie que des probe request pour un autotest de capacité, pas de paquets offensifs.

## L'essentiel (TL;DR)

Mesuré sur ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17) : l'AWUS036ACHM fonctionne en mode monitor bi-bande, atteint 96–100 % d'injection de paquets sur 2,4G (sur 5G, seule l'injection broadcast a été vérifiée) et monte un point d'accès sur les deux bandes (802.11n doit être désactivé).

- Sous Ubuntu 24.04, aucune installation de pilote : le MT7610U est pris en charge par le mt76x0u intégré au kernel 6.17, reconnu dès le branchement, sans DKMS ni firmware additionnel.
- Mode monitor bi-bande disponible ; injection de paquets 2,4G 96–100 %.
- En 5 GHz, seule l'injection en diffusion est confirmée ; le taux de réponse par cible n'a pas été obtenu cette fois-ci (cause à déterminer).
- Pour ouvrir un AP il faut désactiver le 802.11n ; pour le WPA3 il faut régler `sae_pwe=0`, afin que les anciens iPhone se connectent.
- Mono-antenne 1T1R (AC600) : débit et positionnement ne sont pas de la même catégorie que les ACM / ACH 2T2R.

## 1. Cette carte et cette plateforme

L'AWUS036ACHM est la carte mono-antenne AC600 d'ALFA, à base de puce MediaTek MT7610U, prise en charge par le pilote Linux intégré `mt76x0u`. C'est la sœur à flux unique de l'AWUS036ACM (MT7612U, 2T2R) : en termes de spécifications, c'est une 1T1R (AC600), avec un flux spatial en moins, mais en échange un format plus compact et une réception longue portée reconnue par la communauté. La communauté morrownr/USB-WiFi l'inscrit dans sa liste de cartes recommandées pour Kali et dans « The Short List », en annotant VIF, Active monitor et WPA3 tous en Yes, Very Long range, flux unique, in-kernel.

Nous l'avons branchée sur un ASUS GX10 (NVIDIA GB10, 128GB UMA, ARM64), et mesuré point par point le Monitor, l'Injection, l'AP et le WPA3-SAE sous Ubuntu 24.04 LTS, kernel 6.17. D'abord la conclusion : cette carte est utilisable sur cette plateforme, et ses capacités en 2,4 GHz sont assez complètes. Mais deux pièges de compatibilité sont à connaître d'avance : pour ouvrir un AP il faut désactiver le 802.11n, et pour le WPA3 il faut régler `sae_pwe=0` ; par ailleurs, l'injection par cible en 5 GHz n'a été confirmée qu'en diffusion cette fois-ci. Le tableau ci-dessous en donne un aperçu global :

| Capacité | 2,4 GHz | 5 GHz |
|---|---|---|
| Monitor (écoute) | ✅ | ✅ |
| Injection | ✅ 96–100 % | ⚠️ diffusion uniquement, taux par cible non obtenu |
| Point d'accès | ✅ (802.11g pur requis) | ✅ (802.11a pur, 20 MHz, requis) |
| WPA3-SAE | ✅ (`sae_pwe=0` requis) | Non testé |

> Légende : ✅ test réussi | 🟡 partiel ou tenable en local | ⚠️ avec limite | ❌ non pris en charge ou échec.

## 2. Matériel et pilote (sans installation)

Une fois l'ACHM branchée sur le GX10, le `mt76x0u` intégré au kernel 6.17 la reconnaît directement, sans DKMS, sans firmware additionnel, et sans compiler de pilote out-of-tree depuis GitHub. Les trois commandes pour confirmer la carte :

```bash
lsusb | grep 0e8d:7610
# Bus 003 Device 005: ID 0e8d:7610 MediaTek Inc. WiFi

sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cababcd2
```

L'interface est nommée d'après la MAC (`wlx<MAC>`) ; le nom ne change pas d'un rebranchement à l'autre et peut être référencé directement dans un script. Les modes d'interface déclarés par `iw phy info` incluent `managed`, `AP`, `monitor`, `mesh point`, `IBSS`, `P2P-client`, `P2P-GO`, couvrant tous les scénarios testés dans cet article.

Les deux règles de sécurité communes à la plateforme s'appliquent aussi à l'ACHM : premièrement, n'exécutez jamais `airmon-ng check kill`, qui arrête NetworkManager et déconnecte le GX10 d'Internet ; deuxièmement, opérez uniquement sur l'interface `wlx*`, sans toucher au `wlP9s9` intégré (la ligne principale d'accès Internet du GX10). Pour passer en monitor ou en AP, utilisez systématiquement `iw` avec `nmcli dev set $IF managed no`, sans toucher à la carte réseau principale du système.

## 3. Capacités mesurées : Monitor / Injection / AP / WPA3

### 3-1. Monitor (2,4 + 5 GHz) ✅

L'écoute fonctionne correctement sur les deux bandes. En 2,4 GHz sur le canal 6, la limite de capture de 300 paquets est atteinte en 8 secondes ; en 5 GHz, cela dépend de l'activité par fréquence : ch36 (5180) atteint 300 en 8 secondes, 5745 capture 254, 5785 capture 54 (peu de paquets sur un canal signifie généralement qu'aucun AP n'y est actif à cet instant, pas un problème de carte).

Le balayage pleine bande en saut de fréquence est ce qui révèle le mieux la capacité de réception d'une carte mono-antenne :

```bash
sudo timeout -s INT 120 airodump-ng --band abg $IF
```

En 120 secondes, elle a détecté 19 stations de base et 14 clients, répartis sur ch1/2/5/6/36/149/157. Pour une carte AC600 à flux unique, cette couverture suffit à constituer une source d'écoute stable, et confirme l'évaluation « Very Long range » que lui donne la communauté.

### 3-2. Injection (2,4 + 5 GHz)

C'est là que les deux bandes de l'ACHM diffèrent le plus, et un point à surveiller tout particulièrement lors du choix de modèle.

En 2,4 GHz sur le canal 6, l'autotest de capacité `aireplay-ng --test` donne un beau résultat :

```text
Injection is working!
Found 4 APs
30/30: 100%
```

Le taux de réponse des quatre stations de base se situe entre 96 et 100 % : capacité d'injection complète.

Mais en 5 GHz (ch36 et ch149 tous deux essayés), c'est différent :

```text
Injection is working!
Found 0 APs
```

Autrement dit, l'injection en diffusion fonctionne en 5 GHz (le pilote renvoie `Injection is working!`), mais le taux de réponse par cible de `aireplay-ng --test` renvoie `Found 0 APs` sur les deux canaux 5G : aucun pourcentage n'a été obtenu cette fois-ci. C'est le phénomène observé sur cette carte mono-antenne sur cette plateforme, cause à investiguer ; nous ne lui inventons pas un chiffre que nous n'avons pas mesuré. Pour être honnête : si votre usage nécessite une injection par cible stable en 5 GHz, l'ACHM n'a cette fois-ci confirmé un taux d'injection complet qu'en 2,4 GHz.

### 3-3. Point d'accès (2,4 + 5 GHz) ✅ — mais il faut désactiver le 802.11n

Le premier piège de compatibilité de l'ACHM est ici. Pour ouvrir un AP, n'ajoutez pas `ieee80211n=1` ni `ht_capab` dans le fichier de configuration hostapd : le 2,4 GHz en `hw_mode=g` pur, le 5 GHz en `hw_mode=a` pur (20 MHz). Une configuration 2,4 GHz minimale fonctionnelle ressemble à ceci :

```ini
interface=wlx00c0cababcd2
driver=nl80211
ssid=ALFA-TEST-ACHM-24
# 802.11g pur, ne pas ajouter ieee80211n=1 ni ht_capab
hw_mode=g
channel=6
country_code=TW
wmm_enabled=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=remplacez-par-votre-mot-de-passe-d-au-moins-8-caracteres
```

En test, l'iPhone 7 Plus se connecte sur les deux bandes : en 2,4 GHz on voit `AP-STA-CONNECTED` puis `EAPOL-4WAY-HS-COMPLETED` ; en 5 GHz (ch36, 20 MHz) on mesure -71 dBm, rx 54 Mbit, `authorized: yes`.

À l'inverse, si le fichier de configuration conserve `ieee80211n=1`, hostapd fait apparaître de façon répétée `handle_assoc_cb: STA not found`, l'écran de l'iPhone affiche « Impossible de rejoindre le réseau » ou « Mot de passe incorrect », mais c'est en réalité un échec d'association 802.11n, pas un problème de mot de passe. Il suffit de retirer le 802.11n. L'ACHM étant une carte mono-antenne, l'AP 5 GHz utilise ici 20 MHz, le VHT80 n'a pas été essayé.

### 3-4. WPA3-SAE ✅ — mais il faut `sae_pwe=0` (le piège de compatibilité le plus facile à déclencher)

Le second piège de compatibilité de l'ACHM, et celui qui mérite le plus d'être traité à part. Pour le WPA3-SAE, hostapd contrôle via `sae_pwe` la manière de dériver l'élément de mot de passe (password element) : `0` utilise uniquement le Hunting-and-Pecking classique, `1` uniquement le Hash-to-Element (H2E), `2` les deux à la fois (Hunting-and-Pecking et H2E). Cette différence détermine directement si l'ancien iPhone se connecte ou non :

```ini
wpa=2
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
# PMF obligatoire en WPA3
ieee80211w=2
# Clé : compatibilité avec les anciens terminaux comme l'iPhone 7 Plus
sae_pwe=0
sae_password=remplacez-par-votre-mot-de-passe
```

Comparatif mesuré :

- `sae_pwe=0` : l'iPhone 15 Pro et l'iPhone 7 Plus **se connectent tous les deux** (`authorized: yes`, `MFP: yes`).
- `sae_pwe=2` : l'iPhone 7 Plus **s'associe mais le 4-way handshake échoue et il est déconnecté**, ce qui ressemble là encore à un « mot de passe incorrect » ; l'iPhone 15 Pro, lui, se connecte.

La conclusion est directe : pour être compatible avec les anciens iPhone (dont des modèles de 2016 comme l'iPhone 7 Plus), hostapd doit impérativement régler `sae_pwe=0`. Après modification, faites d'abord « oublier ce réseau » à l'iPhone avant de le reconnecter, pour éviter qu'un état d'association résiduel ne provoque un faux échec. Ce point est signalé spécifiquement sur le tableau récapitulatif des 9 cartes, où le champ WPA3 de l'ACHM porte un « ✅* » avec astérisque.

## 4. Avancé et limites

Un tableau d'abord pour synthétiser toute la couverture et l'état de l'ACHM cette fois-ci, les paragraphes suivants détaillant l'essentiel :

| Fonction | État | Point clé de ce test |
|---|---|---|
| Monitor (2,4 + 5 GHz) | ✅ | Saut de fréquence 120 s : 19 AP + 14 clients détectés |
| Injection 2,4 GHz | ✅ | Taux de réponse 96–100 % |
| Injection 5 GHz | ⚠️ | Diffusion disponible, taux par cible non obtenu |
| AP (2,4 + 5 GHz) | ✅ | iPhone connecté sur les deux bandes, 802.11n à désactiver |
| WPA3-SAE | ✅* | Testé en 2,4 GHz (5 GHz non testé) ; anciens et nouveaux iPhone connectés, `sae_pwe=0` requis |
| VIF (STA+AP, AP+monitor) | ✅ | Point d'accès tout en naviguant, téléchargement 198 Mbit/s |
| Capture de handshake WPA | ✅ de bout en bout (.22000, en 5 GHz ch36) | Deauth de notre iPhone, capture complète des 4-way M1–M4, export hashcat `.22000` |
| Active monitor | 🟡 | Écoute configurable, ACK non vérifié |
| Ad-hoc (IBSS) | 🟡 | Créé en local, non interconnecté à un second poste |
| Mesh (802.11s) | 🟡 | Rejoint en local, pas de peer link |
| Wi-Fi Direct (P2P) | ⬜ | Nécessite un second équipement, passé |

> ✅* = WPA3-SAE disponible mais `sae_pwe=0` requis ; voir section 3-4.

**VIF (interfaces virtuelles, même canal, 2 interfaces au maximum).** L'ACHM permet de découper une même carte en plusieurs interfaces fonctionnant en parallèle, à condition que chaque VIF utilise une MAC différente, que la VIF AP ne soit pas gérée par NetworkManager, et que toutes les VIF soient sur le même canal ; l'ACHM impose en plus de désactiver le 802.11n sur l'AP. Les deux combinaisons ont été testées :

- **STA + AP (naviguer et servir de point d'accès en même temps)** : pendant que l'iPhone 7 Plus est connecté à l'AP (-66 dBm, authorized), l'interface principale est connectée à YUPITEK, ping 30/30, moyenne 3,2 ms, téléchargement 198 Mbit/s.
- **AP + Monitor** : écoute tout en gardant l'AP ouvert, 300 frames capturées en 8 secondes, dont 46 beacons de notre propre AP.

**Capture de handshake.** L'ACHM a mené à terme la chaîne de bout en bout en 5 GHz (ch36) : deauth de notre iPhone, capture complète des 4-way (M1–M4) et export hashcat `.22000`. Elle fait partie des 7 cartes sur 9 qui l'ont réussie (ACM, ACHM, ACH, ACS, EACS, AX, AXER). Son taux de réponse par cible en 5 GHz (`aireplay-ng --test`) n'a toutefois toujours pas été obtenu.

**Mesh / IBSS (création en local possible).** C'est le point qui distingue la famille mt76 des Realtek rtw88/rtw89. L'IBSS (Ad-hoc) donne `Joined IBSS` en ~9 secondes et peut émettre des beacons ; le Mesh (802.11s) peut entrer en `type mesh point` et émettre des mesh beacons. Les deux tiennent ici en local, sans interconnexion à un second poste (passé faute d'un second équipement), d'où le 🟡. Les cartes Realtek rtw88/rtw89 (comme l'AWUS036ACH) peuvent certes monter un IBSS en local sur cette plateforme, mais ne prennent pas en charge le mesh 802.11s ; pour une expérimentation mesh 802.11s, les deux cartes mt76 ACM et ACHM sont au contraire parmi les rares choix possibles.

**Active monitor 🟡.** Configurable, écoute correcte, mais le comportement d'ACK nécessite un second équipement pour être vérifié : non vérifié cette fois-ci.

**Outils Kali (au niveau plateforme, communs aux autres cartes).** `airmon-ng`, `kismet`, `bettercap`, `wifite` (version git), Wireshark/tshark peuvent tous utiliser l'ACHM comme source ; seul `hcxdumptool` échoue en `failed to arm interface` sur cette plateforme (sauf l'AWUS036EACS en 2,4 GHz ; le pilote intégré n'a pas de support active-monitor), utilisez alors `airodump-ng` avec la suite aircrack-ng. En ARM64, à noter aussi : `aircrack-ng` manque souvent de paquet précompilé et doit être compilé depuis les sources, et `wifite` est conseillé en version GitHub pour contourner le conflit de dépendances apt.

## 5. Cas d'usage et choix de modèle (retour vers le Hub)

Replacée dans le contexte de choix des 9 cartes, la position de l'ACHM est claire :

**Adaptée à**

- **Expérimentation mesh (802.11s)** : le pilote mt76 crée un mesh 802.11s (et un IBSS) en local ; les cartes Realtek montent un IBSS en local mais pas le mesh 802.11s.
- **Monitor longue portée à flux unique** : saut de fréquence 120 s, 19 AP + 14 clients détectés, « Very Long range » selon la communauté.
- **Injection 2,4 GHz, et AP / point d'accès WPA3** : injection 2,4G 96–100 %, et une fois le WPA3 réglé correctement avec `sae_pwe=0`, anciens et nouveaux iPhone se connectent.

**À surveiller (limites honnêtes)**

- L'injection par cible en 5 GHz n'a été confirmée qu'en diffusion cette fois-ci, sans pourcentage.
- Pour ouvrir un AP il faut désactiver le 802.11n, et pour le WPA3 régler `sae_pwe=0` ; un mauvais réglage de l'un ou l'autre fera « ressembler à un mot de passe incorrect » sur un ancien iPhone.
- Mono-antenne 1T1R : débit et positionnement ne sont pas de la même catégorie que les ACM / ACH 2T2R.

**Repères de choix** : si votre besoin central est une injection stable sur les deux bandes plus un handshake de bout en bout, les AWUS036EACS / AWUS036ACH / AWUS036ACS des 9 cartes sont plus adaptées ; pour du Wi-Fi 6 + point d'accès, voyez l'AWUS036AX / AWUS036AXER ; si vous visez l'expérimentation mesh / IBSS en local ou l'écoute longue portée, l'ACHM (ou sa sœur 2T2R ACM) est le bon outil. Enfin, un rappel pour éviter le piège : pour de l'injection / du handshake, ne choisissez pas l'AWUS036AXM / AXML, dont l'injection MT7921 échoue sur cette plateforme.

Pour la matrice complète des 9 modèles (matériel, pilote, Monitor / Injection / AP / WPA3) et l'évaluation de choix par usage, voyez le tableau Hub : [Matrice de test des 9 cartes Wi-Fi ALFA sur ARM64 / GX10](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Questions fréquentes (FAQ)

**Q : L'AWUS036ACHM nécessite-t-elle l'installation d'un pilote sous Ubuntu 24.04 ?**
Non. Le MT7610U est pris en charge par le pilote mt76x0u intégré au kernel : sous Ubuntu 24.04 (kernel 6.17), la carte est reconnue dès le branchement, sans DKMS ni firmware additionnel ; lsusb affiche l'USB ID 0e8d:7610.

**Q : L'AWUS036ACHM peut-elle passer en mode monitor ? Combien d'AP détecte-t-elle ?**
Oui. Le mode monitor fonctionne en 2,4 GHz comme en 5 GHz ; avec un balayage pleine bande en saut de fréquence via airodump-ng pendant 120 secondes, elle a détecté 19 AP et 14 clients, répartis sur les ch1, 2, 5, 6, 36, 149, 157.

**Q : Quel est le taux de réussite d'injection de paquets de l'AWUS036ACHM ? Est-ce possible en 5 GHz ?**
En 2,4 GHz sur le canal 6, le taux de réponse par cible est de 96–100 % (aireplay-ng --test, 4 AP trouvés). En 5 GHz (ch36, ch149), seule l'injection en diffusion est confirmée ; le test par cible renvoie Found 0 APs, aucun pourcentage n'a été obtenu cette fois-ci, cause à déterminer.

**Q : Que faire si l'iPhone affiche « Impossible de rejoindre le réseau » ou « Mot de passe incorrect » lorsque l'AWUS036ACHM ouvre un AP ?**
Désactivez d'abord le 802.11n : n'ajoutez pas ieee80211n=1 ni ht_capab dans le fichier de configuration hostapd, utilisez un hw_mode=g pur en 2,4 GHz et un hw_mode=a pur en 5 GHz (20 MHz). Sinon hostapd fait apparaître de façon répétée handle_assoc_cb: STA not found : l'écran ressemble à un mot de passe incorrect, mais c'est en réalité un échec d'association 802.11n.

**Q : Pourquoi les anciens iPhone n'arrivent-ils pas à se connecter au WPA3-SAE de l'AWUS036ACHM ?**
C'est le plus souvent le réglage sae_pwe de hostapd. En test, avec sae_pwe=0 l'iPhone 7 Plus et l'iPhone 15 Pro se connectent tous les deux ; avec sae_pwe=2 l'iPhone 7 Plus s'associe mais le 4-way handshake échoue et il est déconnecté, ce qui ressemble à un mot de passe incorrect. Associez ieee80211w=2, et après modification faites d'abord « oublier ce réseau » à l'iPhone avant de le reconnecter.

## 6. Pour aller plus loin

- [Tableau Hub] Matrice complète Monitor · Injection · AP et évaluation de choix des 9 cartes Wi-Fi ALFA sur ASUS GX10 (ARM64 / Ubuntu 24.04) → [/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Modèle sœur] Test carte par carte de l'AWUS036ACM (MT7612U / 2T2R) — lien interne à venir (placeholder)
- [Tutoriel plateforme] Sans installation de pilote : activer Monitor et AP des cartes ALFA avec le pilote in-kernel sous Ubuntu 24.04 + kernel 6.17 — lien interne à venir (placeholder)
- [Dossier] Capacité de capture de handshake à l'ère du WPA3-SAE et piège de compatibilité `sae_pwe` — lien interne à venir (placeholder)

---

*Unité de test : Yopitek (distributeur ALFA Network à Taïwan) — https://www.yupitek.com | Environnement de test : ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Appareil de test : Apple iPhone 7 Plus (WPA3 aussi testé sur iPhone 15 Pro). Données issues des rapports de tests sur machine réelle du 2026-11-16 au 11-18 ; elles ne visent aucun réseau tiers et ne fournissent aucune procédure offensive.*
