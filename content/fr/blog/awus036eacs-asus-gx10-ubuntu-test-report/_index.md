---
title: "ALFA AWUS036EACS, test individuel : le RTL8821CU (composite BT + WiFi) sur ASUS GX10 (ARM64 / Ubuntu 24.04) — Monitor · Injection · AP · handshake de bout en bout"
slug: awus036eacs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036eacs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036eacs
  - rtl8821cu
  - rtw88-8821cu
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036EACS (composite Bluetooth+Wi-Fi) testée sous Ubuntu 24.04 ARM64 : sans installation de pilote, injection bi-bande 100 %, Monitor, AP, WPA3-SAE, handshake de bout en bout (79 ACKs, .22000) validé. Avec le risque de rebranchement USB. Plateforme ASUS GX10, RTL8821CU."
faq:
  - question: "L'AWUS036EACS nécessite-t-elle l'installation d'un pilote sous Ubuntu 24.04 ARM64 ?"
    answer: "Sur le kernel 6.17 testé ici (ASUS GX10), non : le RTL8821CU est pris en charge par le pilote intégré rtw88_8821cu, reconnu dès le branchement, sans compilation ni DKMS ; l'interface est nommée wlx + MAC, inchangée au rebranchement."
  - question: "Comment se comportent le mode monitor et l'injection de paquets de l'AWUS036EACS ?"
    answer: "Le monitor est stable en 2,4G comme en 5G, la plupart des canaux atteignant 300 frames ; aireplay-ng --test donne 30/30 (100 %) sur les deux bandes. Avant une injection 5G, il faut lever la restriction TW sur le TX via iw reg set US."
  - question: "L'AWUS036EACS peut-elle capturer un handshake WPA ?"
    answer: "Oui. Test de bout en bout sur notre propre AP et notre propre iPhone 7 Plus : le deauth reçoit 79 ACKs, capture du M1–M4 complet, export en .22000 via hcxpcapngtool --all (784 bytes, 2 paires EAPOL). Uniquement sur des réseaux dont vous êtes propriétaire ou autorisé."
  - question: "Que faire si l'AWUS036EACS apparaît dans lsusb après branchement mais sans interface réseau wlx ?"
    answer: "C'est la condition de concurrence de probe d'un composite BT+Wi-Fi : le Bluetooth est déjà lié à btusb, et le rtw88_8821cu du Wi-Fi reste bloqué. En test, recharger le module ou faire un bind manuel est le plus souvent inefficace ; la solution fiable est de débrancher la carte et de la rebrancher sur un autre port USB."
  - question: "L'AWUS036EACS prend-elle en charge le mesh, l'IBSS ou hcxdumptool ?"
    answer: "Non. L'active-monitor, l'IBSS, le mesh et le P2P de rtw88 renvoient -95 ou un join sans effet ; hcxdumptool 8.x ne s'arme qu'en 2,4 GHz (échec en 5 GHz), utilisez airodump-ng + aireplay-ng. Le VHT est limité à 80 MHz. Pour le mesh / IBSS, choisissez l'AWUS036ACM / ACHM."
draft: false
---

> Unité de test : Yopitek (distributeur ALFA Network à Taïwan) | Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Appareil de test : notre propre iPhone 7 Plus (WPA3 aussi testé sur iPhone 15 Pro) | Cible de test : notre propre Wi-Fi de bureau (SSID YUPITEK, 2,4G ch5 / 5G ch36, 157).
>
> Cet article est un test de capacités et de compatibilité de l'AWUS036EACS en carte individuelle. Toutes les captures Monitor / Injection / handshake sont réalisées sur les propres équipements de Yopitek, son propre Wi-Fi de bureau, à destination de ses propres téléphones de test : il s'agit d'une vérification matérielle légitime par le distributeur ; elle ne vise aucun réseau tiers et ne fournit aucune procédure offensive.

**L'essentiel (TL;DR)** : l'AWUS036EACS fonctionne sans installation de pilote sur GX10 / Ubuntu 24.04 (kernel 6.17) ; injection bi-bande 100 %, bout en bout .22000 validé (79 ACKs) ; en tant que carte composite BT+Wi-Fi, attention au rebranchement.

## 1. Cette carte et la plateforme de test

L'AWUS036EACS est la carte Wi-Fi 5 (802.11ac) USB nomade légère d'ALFA, à base de puce Realtek RTL8821CU, 1x1 flux unique, bi-bande 2,4 GHz et 5 GHz, avec un Bluetooth intégré : c'est un dispositif composite BT + WiFi. Cet article la place seule sur le banc d'essai de Yopitek, pour la passer point par point en revue dans un environnement ASUS GX10 (ARM64) sous Ubuntu 24.04, et répondre aux questions qui comptent le plus pour les clients : le pilote est-il reconnu sous ARM64, quels modes sont accessibles, jusqu'où va la performance.

Précisons d'abord le positionnement. Il s'agit d'une vérification, par le distributeur, de la compatibilité et des limites de capacités de son propre produit, pas d'un tutoriel offensif. Toutes les mesures de capacités liées à l'injection et au handshake sont réalisées dans un environnement fermé en propre, à destination de nos propres appareils, sans fournir aucune procédure visant un réseau externe.

Plateforme et méthode de test, alignées sur les autres articles individuels de ce lot :

- Plateforme de calcul : ASUS GX10 (ARM64 / aarch64)
- Système d'exploitation : Ubuntu 24.04 LTS, kernel 6.17.0-1014-nvidia
- Stratégie de pilote : utilisation du pilote intégré (in-kernel), reconnu dès le branchement, sans aucun module DKMS tiers
- Appareil de test : Apple iPhone 7 Plus (WPA3-SAE aussi revérifié sur iPhone 15 Pro)
- Environnement de test : Wi-Fi de bureau en propre, SSID YUPITEK, 2,4 GHz ch5 / 5 GHz ch36, ch157
- Règle de sécurité : on opère uniquement sur l'interface `wlx*`, sans toucher à la ligne principale d'accès Internet intégrée ; n'exécutez jamais `airmon-ng check kill` (il arrête NetworkManager et déconnecte le GX10 d'Internet)

## 2. Matériel et pilote : la vérité sur le composite BT + WiFi

D'abord les détails. Le tableau ci-dessous montre l'état réel du montage de l'AWUS036EACS sur le kernel 6.17 :

| Élément | Contenu |
|---|---|
| Puce | Realtek RTL8821CU (1x1 flux unique) |
| Génération | Wi-Fi 5 (802.11ac), 2,4 + 5 GHz |
| Fonction composite | Dispositif composite BT + WiFi (Bluetooth intégré) |
| USB ID | `0bda:c820` |
| Pilote | `rtw88_8821cu` (in-kernel, USB pris en charge depuis le kernel 6.2) |
| Firmware | 24.11.0 (H2C version 12, mesuré via dmesg) |
| Bande passante VHT | 80 MHz seulement (pas de 160 / 80+80) |

Via `iw phy`, les modes d'interface pris en charge sont `managed` / `AP` / `AP/VLAN` / `monitor` (l'`IBSS` est listé mais, en test, le join reste sans effet) ; la couverture des bandes est 2,4 GHz ch1–13 et 5 GHz ch36–165 (dont ch52–144 en bandes DFS) ; les ciphers incluent CCMP-256, GCMP-128 / GCMP-256 et CMAC, réunissant les conditions pour faire tourner le WPA3 côté AP.

Côté pilote, aucun doute. Le support USB du RTL8821CU a été intégré au `rtw88` mainline depuis le kernel 6.2 ; le kernel 6.17 du GX10 embarque déjà `rtw88_8821cu`, chargé dès le branchement, sans compilation ni DKMS. Les premières versions in-kernel avaient un bug en mode AP, corrigé par le macid patch (depuis linux-next-20240911) ; cette fois-ci, sur le kernel 6.17, les trois modes AP se terminent proprement en test. Vérification :

```bash
lsusb | grep -i '0bda:c820'
# ID 0bda:c820 Realtek Semiconductor Corp. 802.11ac NIC
sudo dmesg | grep -i 8821cu
# rtw88_8821cu ...: Firmware version 24.11.0, H2C version 12 -> renamed from wlan0
```

Une fois l'interface Wi-Fi chargée, elle est nommée `wlx` + MAC (par exemple `wlx00c0cab3a52e`) et non `wlan0` ; le nom ne change pas d'un rebranchement à l'autre et peut être référencé de façon stable dans un script.

Ce à quoi il faut vraiment prêter attention, c'est le « dispositif composite ». En examinant avec `lsusb -t`, on voit plusieurs interfaces USB sous une même puce RTL8821CU : la fonction Bluetooth liée à `btusb`, la fonction Wi-Fi liée à `rtw88_8821cu`.

```
/:  Bus 0X.Port X: Dev X, Class=root_hub, Driver=xhci-hcd
    |__ Port X: Dev X, If 0, Class=Wireless, Driver=btusb               <- Bluetooth
    |__ Port X: Dev X, If 1, Class=Wireless, Driver=btusb               <- Bluetooth
    |__ Port X: Dev X, If 2, Class=Vendor Specific, Driver=rtw88_8821cu <- Wi-Fi
```

(Les numéros de Bus/Port changent selon le nombre de branchements ; l'essentiel est que les interfaces 0/1 passent par `btusb` et que l'interface 2 soit le `rtw88_8821cu` du Wi-Fi.)

**Le risque de rebranchement du composite BT + WiFi (à lire avant tout déploiement).** Parce que le Bluetooth et le Wi-Fi partagent le même dispositif USB, sur certains ports USB ou en cas de rebranchement rapide, il peut arriver que le Bluetooth soit déjà lié à `btusb` mais que la probe de l'interface Wi-Fi reste bloquée, créant une condition de concurrence où `lsusb` voit bien `0bda:c820` mais sans que l'interface `wlx` n'apparaisse. En test, un rechargement après `modprobe -r` ou un `bind` manuel sont le plus souvent inefficaces (le `bind` renvoie `Operation already in progress`). Il n'existe qu'une solution fiable : débrancher la carte et la rebrancher sur un autre port USB ; après changement de port, l'énumération est propre et l'interface `wlx` apparaît normalement. C'est le détail d'exploitation supplémentaire à connaître sur cette carte par rapport à l'AWUS036ACS non composite (RTL8811AU) ; le savoir à l'avance évite de le prendre à tort pour une panne de carte.

## 3. Capacités mesurées : Monitor / Injection / AP / WPA3

Le tableau ci-dessous résume les capacités clés mesurées de l'AWUS036EACS, chaque ligne ayant été exécutée sur machine réelle sur le GX10 le 2026-11-18 :

| Capacité | 2,4GHz | 5GHz | Point clé mesuré |
|---|---|---|---|
| Monitor | ✅ fort | ✅ fort | La plupart des canaux au max de 300 frames ; le « ch1 bloqué » #453 de la communauté non reproduit |
| Injection | ✅ 100 % (30/30) | ✅ 100 % (30/30) | Power 2,4G -38,27 / 5G -76,10 ; meilleure injection des cartes ac de ce lot |
| Point d'accès | ✅ fermeture propre | ✅ VHT 80MHz | `hostapd` monte la station, iPhone 7 Plus connecté et 4-way complet |
| WPA3-SAE (côté AP) | ✅ iPhone connecté | Non testé | SAE-only + PMF obligatoire (`ieee80211w=2`, `sae_pwe=0`) |
| Capture de handshake WPA | — | ✅ bout en bout | M1–M4 complet, deauth reçoit 79 ACKs, export `.22000` |

Le Monitor (mode monitor) est stable en 2,4 et 5 GHz. Capture canal par canal sur six canaux : la plupart atteignent le maximum de 300 frames. Pour le 8821cu, un résultat positif important ici : le GitHub #453 que la communauté rtw88 suit de longue date, « le 8821cu reste bloqué en monitor sur ch1 quand le STA est up, sur kernel ≥6.9 », ne se reproduit pas dans cet environnement GX10 ; ch36, ch149 et ch157 en 5 GHz atteignent tous 300 frames de façon stable. Pour une prospection spectrale ou une analyse de paquets à cheval sur 2,4 / 5 GHz, le monitor de cette carte s'utilise en toute confiance.

L'Injection (injection de paquets) est ce qu'elle a de plus remarquable. Mesurée avec `aireplay-ng --test`, elle est de 30/30, 100 % en 2,4 GHz comme en 5 GHz : c'est la meilleure injection des cartes ac de ce lot (l'AWUS036ACS, aussi 1x1, n'atteint que 96 % en 5G). Un détail local à Taïwan : le TX 5 GHz est verrouillé quand le regulatory domain est réglé sur TW ; déverrouillez via `iw reg set US` avant la mesure, puis restaurez via `iw reg set TW` après.

Côté point d'accès, trois configurations montées avec `hostapd` — 2,4 GHz (WPA2), 5 GHz (VHT 80 MHz), WPA3-SAE : l'iPhone 7 Plus se connecte et complète le 4-way handshake dans les trois, avec une fermeture propre (`AP-DISABLED` / `TERMINATING`). Pas de problème de re-key de beacon comme sur certaines cartes ; sur ce point, le 2,4G est plus stable que sur la carte sœur ACS. Le WPA3 adopte un SAE-only avec PMF obligatoire (`ieee80211w=2`, `sae_pwe=0`) ; l'iPhone 15 Pro se connecte avec succès, confirmant que le WPA3-SAE côté AP du RTL8821CU est utilisable.

La chaîne d'outils Kali (au niveau plateforme) démarre aussi correctement sur cette carte : `airmon-ng` détecte l'EACS (`rtw88_8821cu`), mais n'utilisez pas `check kill` ; `kismet` démarre avec succès en l'utilisant comme data source, produisant un log `.kismet` d'environ 733 KB ; le `wifi.recon on` de `bettercap` 2.32 fonctionne normalement (l'avertissement txpower est ignorable) ; `wifite` (git 3.0.0) détecte plus de 10 AP, dont notre YUPITEK (ch5, PWR 84) — cette version n'a pas le drapeau `--band`, utilisez `-c 1,6,11,36,149,157` pour spécifier les canaux ; `Wireshark` / `tshark` 4.x capture et analyse 325 frames en monitor ch6 ; l'usurpation de MAC aléatoire de `macchanger` fonctionne aussi. Cette couche d'outils est identique aux autres cartes du lot ; la différence tient surtout aux capacités matérielles d'injection et de monitor évoquées plus haut.

## 4. Handshake de bout en bout : point fort et limites honnêtes

La capacité marquante de cette carte est de chaîner l'injection et la capture en une chaîne complète et utilisable. Entre notre propre AP YUPITEK et notre propre iPhone 7 Plus, toute la chaîne a tourné sur machine réelle : envoi d'un deauth vers notre propre iPhone (injection ; 79 ACKs reçus en test, confirmant que les paquets injectés atteignent bien le client) → à la reconnexion de l'iPhone, capture du 4-way handshake complet (M1, M2, M3, M4, un de chaque) → export en `.22000` au format hashcat via `hcxpcapngtool --all` (784 bytes, 2 paires EAPOL, RC checked). Tout le flux sert uniquement à vérifier la capacité de la carte ; la cible reste de bout en bout notre propre AP et notre propre téléphone, sans aucun réseau tiers impliqué.

En pratique, deux détails clés à noter : plusieurs AP homonymes YUPITEK sont sur ch36 au bureau, donc à la capture ne verrouillez pas de `--bssid`, capturez directement tout le canal pour ne pas filtrer celui auquel l'iPhone est réellement connecté ; par ailleurs `hcxpcapngtool` est assez strict par défaut, il faut ajouter `--all` pour exporter le `.22000`.

Les limites honnêtes, dites clairement d'un coup :

- **Pas de prise en charge de l'active-monitor / IBSS (Ad-hoc) / Mesh (802.11s) / Wi-Fi Direct (P2P).** Sous `rtw88`, ces modes renvoient `-95` (Operation not supported) ou se listent sans que le join soit effectif : limite au niveau du pilote, sans solution. Les clients ayant besoin d'expérimenter le mesh / IBSS doivent passer aux MediaTek AWUS036ACM / ACHM.
- **`hcxdumptool` 8.x limité.** Il exige l'active-monitor ; sur cette carte il ne s'arme qu'en 2,4 GHz et échoue en `failed to arm` en 5 GHz (les autres cartes du lot échouent toutes en `failed to arm interface`) ; utilisez `airodump-ng` + `aireplay-ng`, l'injection de cette carte étant à 100 %, cela n'a aucun impact.
- **VHT limité à 80 MHz.** Flux unique, pas de 160 MHz ni de 80+80 : le positionnement est bien une carte nomade légère, pas un rôle axé débit.
- **VIF partielle.** Seule une interface monitor passive fonctionnant en parallèle d'une interface managed sur le même canal (monitor logiciel) marche (100 frames en test) ; les doubles VIF indépendantes ne sont pas prises en charge.

## 5. Cas d'usage et choix de modèle

Au vu des mesures, le positionnement de l'AWUS036EACS est clair : si vous avez besoin de valider Monitor + Injection + handshake de bout en bout sur les deux bandes, tout en voulant une carte nomade légère avec Bluetooth intégré, c'est la bonne solution. L'injection bi-bande à 100 % et des performances AP / WPA3 propres la placent, pour l'audit sans fil et l'enseignement en cybersécurité dans un cadre autorisé, dans le groupe de tête aux côtés de l'AWUS036ACH et de l'AWUS036ACS.

Dans quels cas préférer une autre carte :

- **Rebranchements fréquents sur site, ou ports USB de qualité inégale** → la condition de concurrence de probe du dispositif composite peut compliquer les choses ; envisagez l'AWUS036ACS non composite (RTL8811AU, aussi 1x1 ac, sans la variable Bluetooth en plus).
- **Expérimentation mesh / IBSS** → `rtw88` ne la prend pas en charge, passez aux MediaTek AWUS036ACM / ACHM.
- **Meilleure réception ou monitor longue portée** → l'AWUS036ACH bi-antenne ou l'AWUS036AXER Wi-Fi 6 sont plus adaptées.
- **Piège à éviter** : pour un usage d'injection / handshake, ne choisissez pas les MT7921 AWUS036AXM / AXML, dont l'injection échoue directement sur cette plateforme.

Pour voir d'un coup la comparaison transversale Monitor / Injection / AP / WPA3 des 9 cartes ALFA et la matrice de choix complète, revenez au tableau récapitulatif : [Le test le plus complet de 2026 : la matrice complète des 9 cartes Wi-Fi ALFA sur ASUS GX10](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Questions fréquentes (FAQ)

**Q : L'AWUS036EACS nécessite-t-elle l'installation d'un pilote sous Ubuntu 24.04 ARM64 ?**
Sur le kernel 6.17 testé ici (ASUS GX10), non : le RTL8821CU est pris en charge par le pilote intégré rtw88_8821cu, reconnu dès le branchement, sans compilation ni DKMS ; l'interface est nommée wlx + MAC, inchangée au rebranchement.

**Q : Comment se comportent le mode monitor et l'injection de paquets de l'AWUS036EACS ?**
Le monitor est stable en 2,4G comme en 5G, la plupart des canaux atteignant 300 frames ; `aireplay-ng --test` donne 30/30 (100 %) sur les deux bandes. Avant une injection 5G, il faut lever la restriction TW sur le TX via `iw reg set US`.

**Q : L'AWUS036EACS peut-elle capturer un handshake WPA ?**
Oui. Test de bout en bout sur notre propre AP et notre propre iPhone 7 Plus : le deauth reçoit 79 ACKs, capture du M1–M4 complet, export en .22000 via `hcxpcapngtool --all` (784 bytes, 2 paires EAPOL). Uniquement sur des réseaux dont vous êtes propriétaire ou autorisé.

**Q : Que faire si l'AWUS036EACS apparaît dans lsusb après branchement mais sans interface réseau wlx ?**
C'est la condition de concurrence de probe d'un composite BT+Wi-Fi : le Bluetooth est déjà lié à btusb, et le rtw88_8821cu du Wi-Fi reste bloqué. En test, recharger le module ou faire un bind manuel est le plus souvent inefficace ; la solution fiable est de débrancher la carte et de la rebrancher sur un autre port USB.

**Q : L'AWUS036EACS prend-elle en charge le mesh, l'IBSS ou hcxdumptool ?**
Non. L'active-monitor, l'IBSS, le mesh et le P2P de rtw88 renvoient -95 ou un join sans effet ; hcxdumptool 8.x ne s'arme qu'en 2,4 GHz (échec en 5 GHz), utilisez airodump-ng + aireplay-ng. Le VHT est limité à 80 MHz. Pour le mesh / IBSS, choisissez l'AWUS036ACM / ACHM.

---

## 6. Pour aller plus loin

- [Le test le plus complet de 2026 : la matrice complète Monitor · Injection · AP des 9 cartes Wi-Fi ALFA sur ASUS GX10 (ARM64 / Ubuntu 24.04)](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/) (tableau Hub)
- [L'audit sans fil à l'ère du WPA3-SAE : capacité de capture de handshake des 9 cartes ALFA mesurée](/fr/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- [Sans installation de pilote : activer les modes Monitor et AP des cartes ALFA avec le pilote in-kernel sous Ubuntu 24.04 + kernel 6.17](/fr/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- Autre carte USB ac rtw88 de la même famille → [Rapport de test individuel de l'AWUS036ACS (RTL8811AU)](/fr/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*Unité de test : Yopitek (distributeur ALFA Network à Taïwan) — https://www.yupitek.com*
