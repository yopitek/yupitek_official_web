---
title: "ALFA AWUS036AX, test carte par carte : rapport sur les capacités Wi-Fi 6 Monitor / Injection / AP sur ASUS GX10 + Ubuntu 24.04 (Realtek RTL8832BU / rtw89_8852bu)"
slug: awus036ax-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ax-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036ax-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ax
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - asus-gx10
  - ubuntu-arm64
description: "AWUS036AX (Wi-Fi 6) testée sous Ubuntu 24.04 ARM64 : sans installation de pilote, Monitor, injection 2,4G 96 %, AP 5G VHT80, WPA3-SAE, handshake de bout en bout (.22000) validé ; pas de prise en charge de l'IBSS / mesh. Plateforme ASUS GX10, RTL8832BU."
faq:
  - question: "L'AWUS036AX nécessite-t-elle l'installation d'un pilote sous Ubuntu 24.04 ARM64 ? Que faire si lsusb affiche 0bda:1a2b ?"
    answer: "Sur le kernel 6.17 testé ici (ASUS GX10), non : le RTL8832BU est pris en charge par le pilote intégré rtw89_8852bu, sans compilation ni DKMS. Si lsusb affiche 0bda:1a2b (mode CD-ROM), exécutez sudo usb_modeswitch -v 0bda -p 1a2b -K pour basculer en mode WLAN."
  - question: "L'AWUS036AX prend-elle en charge le mode monitor et l'injection de paquets ?"
    answer: "Oui. Injection 2,4 GHz 29/30 (96 %) ; en 5 GHz, le test ciblé par AP renvoie Injection is working! ; airodump-ng en saut de fréquence pendant 60 secondes détecte 14 AP et 4 clients. Elle ne prend pas en charge l'active monitor, l'IBSS ni le mesh."
  - question: "L'AWUS036AX peut-elle capturer un handshake WPA ? Les AXM / AXML en MT7921 le peuvent-elles ?"
    answer: "L'AX le peut : sur notre propre AP et notre propre iPhone 7 Plus, aireplay-ng -0 déclenche la reconnexion, airodump-ng capture le M1–M4 complet, hcxpcapngtool exporte le .22000. Les AXM / AXML en MT7921 échouent à l'injection sur cette plateforme et ne le peuvent pas. Uniquement sur des réseaux dont vous êtes propriétaire ou autorisé."
  - question: "L'AWUS036AX peut-elle servir de point d'accès ? Prend-elle en charge le WPA3 ?"
    answer: "Oui. hostapd ouvre un AP en 2,4G (802.11n) et en 5G (VHT 80 MHz), l'iPhone 7 Plus connecté affiche VHT-NSS2 80 MHz ; le WPA3-SAE (ieee80211w=2, sae_pwe=0) connecte l'iPhone 15 Pro en 2,4 GHz, MFP: yes (WPA3 en 5 GHz non testé)."
  - question: "Quelle différence entre l'AWUS036AX et l'AWUS036AXER ? Laquelle choisir ?"
    answer: "Les deux reposent sur RTL8832BU + rtw89_8852bu, avec une matrice de capacités identique ; la différence tient à l'antenne et à la réception : l'AXER a des antennes externes et, dans le même lot de tests, son balayage en saut de fréquence a détecté 63 AP + 12 clients (l'AX : 14 AP + 4 clients). Pour un poste fixe de bureau, choisissez l'AX ; pour la longue portée ou la meilleure réception, l'AXER."
draft: false
---

**L'essentiel (TL;DR)** : selon les tests de Yopitek (distributeur ALFA Network à Taïwan), l'AWUS036AX fonctionne sans installation de pilote sur ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17), avec monitor bi-bande ; injection 2,4G 96 %, AP 5G VHT80, bout en bout .22000 validé, pas de prise en charge de l'IBSS / mesh.

> Cet article est un test de compatibilité produit et de capacités réalisé par Yopitek sur **ses propres équipements, son propre Wi-Fi de bureau (SSID `YUPITEK`), ses propres téléphones de test**, portant sur l'ALFA **AWUS036AX** (Realtek RTL8832BU, Wi-Fi 6 2x2).
> Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia` ; appareil de référence Apple iPhone 7 Plus (WPA3 et VIF aussi testés sur iPhone 15 Pro).
> ⚠️ **Usage légal** : le mode monitor et l'injection ne concernent que les réseaux dont vous êtes propriétaire ou autorisé ; pour le mode AP, respectez la réglementation radio locale. Cet article ne couvre aucune opération offensive visant un réseau tiers.

---

## 1. Cette carte et la plateforme de test

L'AWUS036AX est la carte Wi-Fi 6 USB de cette génération chez ALFA, à base de puce Realtek RTL8832BU, 2x2 à deux flux spatiaux, bi-bande 2,4 GHz et 5 GHz. Dans la gamme ALFA, elle partage la même puce et le même pilote (`rtw89_8852bu`) que la version à antennes externes AWUS036AXER, la différence tenant à la forme d'antenne et au gain de réception ; face aux modèles Wi-Fi 6 MediaTek AWUS036AXM / AXML, c'est une filière de puce totalement différente, et les conclusions mesurées diffèrent fortement (voir section 5).

Ce test ne parle pas des débits théoriques de la fiche technique : il répond aux trois questions qui comptent le plus pour la distribution et le terrain d'ingénierie : est-elle facile à installer sur un Linux récent ? Quelles capacités sans fil sont réellement utilisables ? Lesquelles le pilote est-il intrinsèquement incapable de faire, pour ne pas y perdre son temps ? Les conclusions doivent être reproductibles, donc toutes les commandes ont été exécutées une à une sur le GX10 réel le 2026-11-18 ; les « sorties mesurées » ci-dessous sont des extraits réels (adresses MAC masquées par `xx`).

Précisons d'abord le périmètre de test : tout se déroule dans notre propre bureau, sur notre propre réseau `YUPITEK` et nos propres téléphones. Le Monitor ne capture que les paquets de notre environnement, l'Injection et le handshake ne visent que notre propre AP et notre propre iPhone. L'objectif est de vérifier « ce que cette carte peut faire sur cette machine », pas de démontrer une attaque d'un réseau tiers.

---

## 2. Matériel et pilote (Wi-Fi 6, sans installation)

L'avantage le plus concret de cette génération : **reconnue dès le branchement, sans compilation ni DKMS**. Le pilote `rtw89_8852bu` du RTL8832BU est déjà un module in-kernel du kernel 6.17 ; le GX10 le lie au démarrage, sans avoir à récupérer et compiler un projet out-of-tree sur GitHub.

Informations sur la puce et étapes de vérification. D'abord, confirmer avec `lsusb` que la carte s'énumère en mode WLAN :

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
```

Vous devriez voir `ID 0bda:b832 Realtek Semiconductor Corp. 802.11ax WLAN Adapter`. Notre carte de test est apparue directement en mode WLAN, sans rester bloquée en mode CD-ROM ; si la vôtre affiche `0bda:1a2b`, c'est qu'elle est encore en mode CD-ROM, basculez-la en WLAN avec `sudo usb_modeswitch -v 0bda -p 1a2b -K`.

Ensuite, confirmer le chargement du pilote et du firmware :

```bash
sudo dmesg | grep rtw89_8852bu | tail -3
```

La machine charge `rtw89/rtw8852b_fw-1.bin`, firmware version `0.29.29.5`. Pilote et firmware sont intégrés au kernel, sans paquet à installer.

Dernière étape : voir clairement **quels modes d'interface le pilote déclare prendre en charge**, ce qui détermine directement quelles capacités existent et lesquelles sont N/A :

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

La machine liste `managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO`. L'IBSS, le mesh point et l'active-monitor n'y figurent pas. Ce n'est pas un réglage mal fait : le `rtw89_8852bu` ne réalise tout simplement pas ces trois modes, marqués N/A en section 4.

---

## 3. Capacités mesurées : Monitor / Injection / AP / WPA3

D'abord un tableau récapitulatif, chaque case correspondant à un extrait mesuré ci-dessous :

| Capacité | 2,4 GHz | 5 GHz | Extrait mesuré |
|---|---|---|---|
| **Monitor** | ✅ fort | ✅ fort | airodump saut de fréquence 60 s : **14 AP + 4 clients** détectés |
| **Injection** | ✅ **96 %** | ✅ disponible | 2,4G `aireplay-ng --test` 29/30 (96 %) ; 5G par cible `Injection is working!` |
| **Point d'accès** | ✅ 802.11n (HT) | ✅ **VHT 80 MHz** | iPhone 7 Plus connecté : 2,4G MCS 12, 5G VHT-NSS2 80 MHz |
| **WPA3-SAE** | ✅ | Non testé | iPhone 15 Pro connecté, MFP: yes (`sae_pwe=0`) ; testé en 2,4 GHz uniquement |
| **Capture de handshake WPA** | ✅ **bout en bout** | — | deauth de notre propre iPhone → capture du 4-way complet → export hashcat `.22000` |

**Monitor (mode monitor / réception) ✅ fort.** Après passage en monitor, de nombreux paquets sont captés en 2,4 GHz comme en 5 GHz (~100 paquets/6 s chacun). Un balayage en saut de fréquence de 60 s avec `airodump-ng --band abg` détecte 14 AP et 4 clients : une réception du même niveau que les ACM / ACHM Wi-Fi 5 d'ALFA, bien supérieure aux deux cartes MediaTek MT7921 (l'AXM / AXML ont une réception faible en test). Pour une prospection sur site ou un inventaire d'occupation de canaux, la réception de cette carte suffit.

**Injection (injection de paquets) ✅ disponible, c'est aussi la différence clé de l'AX face aux modèles MediaTek.** En 2,4 GHz (ch6), `aireplay-ng --test` donne `29/30: 96 %`, `Injection is working!`, taux de réponse 96 %. En 5 GHz (ch36), le test en diffusion peut renvoyer `Found 0 APs` (les AP modernes ne répondent pas aux probe en diffusion, c'est normal), mais un test ciblant le BSSID d'un AP renvoie `Injection is working!`, confirmant l'injection 5 GHz. À l'inverse, les MediaTek AXM / AXML, également Wi-Fi 6, **échouent directement à l'injection** sur cette plateforme (cause principale : une régression de mac80211 chanctx depuis le noyau 6.16, à laquelle s'ajoute un firmware qui verrouille le débit d'injection à 1/6 Mbit/s ; ce n'est pas une limite de la puce elle-même) : un point à bien distinguer lors du choix.

**Point d'accès ✅ les deux bandes, le 5 GHz monte en VHT80.** AP monté avec hostapd : en 2,4 GHz en 802.11n (`ieee80211n=1`, HT20), l'iPhone 7 Plus connecté affiche MCS 12, authorized ; en 5 GHz en VHT 80 MHz (`vht_oper_chwidth=1`, `ht_capab=[HT40+]`), l'iPhone 7 Plus connecté affiche VHT-NSS2 80 MHz, authorized. Les deux bandes portent le client de façon stable, et la bande passante de 80 MHz est effectivement négociée.

**WPA3-SAE ✅ (2,4 GHz ; 5 GHz non testé).** En passant le `wpa_key_mgmt` de l'AP à `SAE`, `ieee80211w=2`, l'iPhone 15 Pro se connecte, MFP (Management Frame Protection) affiché à yes. Un détail de compatibilité : il faut régler `sae_pwe` à `0` (Hunting-and-Pecking) pour que les anciens iPhone se connectent.

**Capture de handshake WPA ✅ bout en bout réussi.** Sur notre propre réseau `YUPITEK`, à destination de notre propre iPhone 7 Plus, flux complet : monitor sur le canal → `aireplay-ng -0` envoie un deauth pour déclencher la reconnexion → `airodump-ng` capture le 4-way complet (M1/M2/M3/M4) → `hcxpcapngtool` exporte au format hashcat `.22000`. C'est parce que cette carte peut injecter que toute la chaîne tient ; une carte dont l'injection échoue (comme l'AXM / AXML) casse dès l'étape du deauth. Les outils Kali courants de cette chaîne de capture de handshake (aircrack-ng, hcxtools) s'exécutent directement sous Ubuntu 24.04 ARM64.

---

## 4. Avancé et limites (les N/A du pilote rtw89)

Cette section dit clairement, d'un coup, « les fonctions avancées possibles » et « ce que le pilote est intrinsèquement incapable de faire », pour éviter de perdre du temps sur le terrain.

| Fonction | État | Commentaire |
|---|---|---|
| **VIF (STA + AP en parallèle)** | ✅ | Interface principale connectée à `YUPITEK`, VIF AP ouverte en même temps (ch36 VHT80), deux interfaces en parallèle ; ping côté STA 3,2 ms |
| **Capture de handshake WPA** | ✅ bout en bout | Capture du M1–M4, `hcxpcapngtool` exporte le `.22000` |
| **Active monitor** | **N/A** | `rtw89_8852bu` n'a pas ce mode (absent des supported modes de `iw phy`) |
| **Ad-hoc (IBSS)** | **N/A** | Non pris en charge par le pilote |
| **Mesh (802.11s)** | **N/A** | Non pris en charge par le pilote |
| **Wi-Fi Direct (P2P)** | ⬜ non testé | Déclaré pris en charge par le pilote, mais nécessite un second équipement, passé ce cycle |

**VIF ✅.** Créez une interface virtuelle AP (MAC différente, unmanaged), gardez l'interface principale connectée au Wi-Fi, ouvrez l'AP sur le même canal. En test, pendant que l'interface principale est connectée à `YUPITEK`, la VIF AP tourne en VHT80 sur ch36, les deux interfaces fonctionnant en parallèle, ping côté STA 3,2 ms. Viable pour « se connecter tout en ouvrant un point d'accès de test ».

**Active monitor / IBSS / Mesh sont N/A, pas en panne.** Ces trois modes n'apparaissent pas dans les supported interface modes de `iw phy info` de la section 2 : le pilote `rtw89_8852bu` ne les implémente tout simplement pas. Une commande comme `sudo iw dev $IF set type ibss` échoue directement, sans solution : ni un paramètre ni un firmware n'y remédient ; pour ces trois modes, il faut changer de filière de puce (par exemple les MediaTek mt76 ACM / ACHM créent un IBSS / mesh en local).

**Une limite au niveau plateforme à connaître : hcxdumptool échoue en `failed to arm` sur le GX10.** Ce n'est pas un problème propre à l'AX. `hcxdumptool 8.x` exige l'active-monitor, or le GX10 a une carte intégrée tri-bande et, à l'énumération des cartes USB, le `-I` est facilement mal mappé sur le phy intégré ; toutes les cartes USB testées échouent à s'armer sur cette machine (seule exception : l'AWUS036EACS en 2,4 GHz). En pratique, **utilisez la suite aircrack-ng** (airodump-ng + aireplay-ng) pour la capture : l'injection de cette carte étant disponible, toute la chaîne se déroule de bout en bout (voir section 3).

**Règle de sécurité (commune à la plateforme GX10) :** n'exécutez jamais `airmon-ng check kill`, il arrête NetworkManager et déconnecte le GX10 d'Internet ; opérez uniquement sur l'interface `wlx*`, sans toucher à la carte réseau intégrée qui assure l'accès Internet.

---

## 5. Cas d'usage et choix de modèle (point d'accès Wi-Fi 6, retour vers le Hub)

Traduisons les conclusions mesurées en conseils de choix : **le point idéal de l'AWUS036AX est le scénario « Wi-Fi 6 + point d'accès » nécessitant en même temps une capacité d'injection.**

| Usage | Adéquation de l'AWUS036AX | Commentaire |
|---|---|---|
| Point d'accès Wi-Fi 6 / accès en périphérie | ★ premier choix | 2x2 VHT80 bi-bande, WPA3-SAE disponible |
| Audit Injection + handshake | ★ à la hauteur | 2,4G 96 %, 5G disponible, capture de bout en bout réussie |
| Meilleure réception / monitor longue portée | ○ suffisant, mais préférer l'AXER | L'AXER à même puce a des antennes externes, meilleure réception |
| Expérimentation mesh / IBSS | ✗ inadaptée | Pilote N/A, préférez les mt76 ACM / ACHM |

**Déploiement typique : en point d'accès Wi-Fi 6, pour faire remonter les appareils en périphérie vers un Hub central.** Avec les capacités AP (VHT80) et VIF éprouvées, déployez le GX10 muni de cette carte en point d'accès Wi-Fi 6 ; les appareils en périphérie (téléphones de test, capteurs IoT) s'y connectent, et le trafic repart via l'interface principale vers le Hub central (gateway). La VIF a prouvé que « l'interface principale remontant au réseau supérieur » et « l'ouverture d'un AP vers le bas » fonctionnent en parallèle, avec une latence de 3,2 ms côté STA : cette topologie est vérifiée comme viable sur cette plateforme. Pour chiffrer modernement le segment d'accès en périphérie, ajoutez simplement le WPA3-SAE.

**Piège à éviter au choix : pour un usage injection / handshake, ne choisissez pas l'AWUS036AXM / AXML.** Ces deux cartes, bien que Wi-Fi 6 2x2 et capables d'ouvrir un AP, **échouent à l'injection** sur cette plateforme (MediaTek MT7921) : impossible de faire un deauth ni de capturer un handshake. Si un client veut simplement une carte d'AP Wi-Fi 6 / de connexion ordinaire, sans aucune injection, les modèles MediaTek conviennent et sont stables ; mais dès que l'usage touche à l'audit sans fil, choisissez l'AX Realtek (ou l'AXER à antennes externes).

**Comment la distinguer de l'AXER à même puce ?** Puce, pilote et matrice de capacités sont identiques ; l'AXER est la version à antennes externes, meilleure en réception et en monitor longue portée (dans le même lot, l'AXER a détecté 63 AP + 12 clients en saut de fréquence). Pour un poste fixe de bureau sans fort besoin d'antenne, choisissez l'AX ; pour allonger la portée ou maximiser la réception, prenez l'AXER.

---

## Questions fréquentes (FAQ)

**Q : L'AWUS036AX nécessite-t-elle l'installation d'un pilote sous Ubuntu 24.04 ARM64 ? Que faire si lsusb affiche 0bda:1a2b ?**
Sur le kernel 6.17 testé ici (ASUS GX10), non : le RTL8832BU est pris en charge par le pilote intégré rtw89_8852bu, sans compilation ni DKMS. Si lsusb affiche `0bda:1a2b` (mode CD-ROM), exécutez `sudo usb_modeswitch -v 0bda -p 1a2b -K` pour basculer en mode WLAN.

**Q : L'AWUS036AX prend-elle en charge le mode monitor et l'injection de paquets ?**
Oui. Injection 2,4 GHz 29/30 (96 %) ; en 5 GHz, le test ciblé par AP renvoie `Injection is working!` ; airodump-ng en saut de fréquence pendant 60 secondes détecte 14 AP et 4 clients. Elle ne prend pas en charge l'active monitor, l'IBSS ni le mesh.

**Q : L'AWUS036AX peut-elle capturer un handshake WPA ? Les AXM / AXML en MT7921 le peuvent-elles ?**
L'AX le peut : sur notre propre AP et notre propre iPhone 7 Plus, `aireplay-ng -0` déclenche la reconnexion, `airodump-ng` capture le M1–M4 complet, `hcxpcapngtool` exporte le .22000. Les AXM / AXML en MT7921 échouent à l'injection sur cette plateforme et ne le peuvent pas. Uniquement sur des réseaux dont vous êtes propriétaire ou autorisé.

**Q : L'AWUS036AX peut-elle servir de point d'accès ? Prend-elle en charge le WPA3 ?**
Oui. `hostapd` ouvre un AP en 2,4G (802.11n) et en 5G (VHT 80 MHz), l'iPhone 7 Plus connecté affiche VHT-NSS2 80 MHz ; le WPA3-SAE (ieee80211w=2, sae_pwe=0) connecte l'iPhone 15 Pro en 2,4 GHz, MFP: yes (WPA3 en 5 GHz non testé).

**Q : Quelle différence entre l'AWUS036AX et l'AWUS036AXER ? Laquelle choisir ?**
Les deux reposent sur RTL8832BU + rtw89_8852bu, avec une matrice de capacités identique ; la différence tient à l'antenne et à la réception : l'AXER a des antennes externes et, dans le même lot de tests, son balayage en saut de fréquence a détecté 63 AP + 12 clients (l'AX : 14 AP + 4 clients). Pour un poste fixe de bureau, choisissez l'AX ; pour la longue portée ou la meilleure réception, l'AXER.

---

## 6. Pour aller plus loin

- « Tableau récapitulatif des capacités des 9 cartes Wi-Fi ALFA sur ASUS GX10 + Ubuntu ARM64 » — comparaison en une fois de tous les modèles Monitor / Injection / AP / handshake → [Tableau Hub](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Sans installation de pilote : activer Monitor et AP avec le pilote in-kernel sous Ubuntu 24.04 + kernel 6.17](/fr/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/) — flux de configuration commun à rtw88 / rtw89 / mt76
- [Test carte par carte de l'AWUS036AXER](/fr/blog/awus036axer-asus-gx10-ubuntu-test-report/) — version à antennes externes de la même puce, comparaison de la réception et du monitor longue portée
- [Capacité de capture de handshake WPA3-SAE mesurée et compatibilité sae_pwe](/fr/blog/alfa-wpa3-sae-handshake-capability-arm64/) — le piège du `sae_pwe` pour la connexion des iPhone

---

*Unité de test : Yopitek (distributeur ALFA) — https://www.yupitek.com | Environnement de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 | Appareil de référence : Apple iPhone 7 Plus (WPA3 / VIF aussi testés sur iPhone 15 Pro)*
