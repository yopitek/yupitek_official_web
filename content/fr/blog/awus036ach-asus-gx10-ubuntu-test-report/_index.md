---
title: "AWUS036ACH, test individuel : le Realtek RTL8812AU bi-antenne AC1200 sur ASUS GX10 (ARM64 / Ubuntu 24.04) — rapport complet Monitor · Injection · AP · WPA3"
slug: awus036ach-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ach-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ach
  - rtl8812au
  - rtw88-8812au
  - realtek
  - wifi-5
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - alfa-network
  - asus-gx10
  - arm64
description: "L'AWUS036ACH (RTL8812AU) fonctionne sans DKMS sous Ubuntu 24.04 / kernel 6.17 : mode monitor bi-bande disponible, injection de paquets 100 %, handshake WPA de bout en bout (.22000) prouvé, avec des limites comme le blocage de la réception 5G."
faq:
  - question: "L'AWUS036ACH nécessite-t-elle l'installation d'un pilote sous Kali ou Ubuntu ?"
    answer: "Cela dépend de la version du kernel. À partir du kernel Linux 6.13 (ici Ubuntu 24.04 / kernel 6.17), le pilote rtw88_8812au est intégré : reconnaissance dès le branchement, sans compilation ni DKMS ; en dessous du kernel 6.13, il faut installer lwfinger/rtw88 via DKMS. Sous Kali, vérifiez d'abord la version du kernel avec uname -r ; cela n'a pas été vérifié sur une machine Kali réelle cette fois-ci."
  - question: "Comment se comportent le mode monitor et l'injection de paquets de l'AWUS036ACH ?"
    answer: "Le mode monitor fonctionne en 2,4 GHz comme en 5 GHz ; l'injection dirigée par cible avec aireplay-ng est de 30/30 = 100 % aussi bien en 2,4 GHz (sur 4 AP) qu'en 5 GHz (sur YUPITEK ch36). Avant une injection 5 GHz, réglez le domaine réglementaire pour autoriser l'émission (par exemple iw reg set US) : sous le country 00 par défaut, le 5 GHz interdit l'émission et l'injection ne part pas."
  - question: "L'AWUS036ACH peut-elle capturer un handshake WPA ?"
    answer: "Oui, et c'est prouvé de bout en bout. L'injection est de 100 % sur les deux bandes ; le 2026-11-19, un test complémentaire sur notre propre iPhone 15 Pro, en 5 GHz ch36, a capturé un 4-way handshake complet et exporté 47 hashlines hashcat .22000 via hcxpcapngtool. Uniquement sur des réseaux dont vous êtes propriétaire ou autorisé."
  - question: "Que faire si l'iPhone 7 Plus n'arrive pas à se connecter au point d'accès WPA3 de l'AWUS036ACH ?"
    answer: "hostapd doit être réglé sur sae_pwe=0 avec ieee80211w=2 pour que l'iPhone 7 Plus se connecte ; avec sae_pwe=2 il ne se connecte pas. Le même réglage est également décisif sur l'AWUS036ACHM."
  - question: "Que faire si la réception 5 GHz de l'AWUS036ACH se bloque soudainement (0 paquet capturé) ?"
    answer: "C'est un phénomène connu du rtw88_8812au : après des bascules répétées de mode ou des changements de domaine réglementaire, la réception 5 GHz peut se bloquer, sans récupération logicielle possible ; il faut débrancher/rebrancher physiquement ou redémarrer. Il est conseillé de rebrancher la carte avant un test 5 GHz et de traiter en priorité les points 5 GHz."
draft: false
---

> Unité de test : Yupitek (distributeur ALFA Network à Taïwan) | Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Appareil de test : notre propre Apple iPhone 7 Plus | Cible de test : notre propre Wi-Fi de bureau (SSID `YUPITEK`, 2,4G ch5 / 5G ch36, 157) | Date de test : 2026-11-18.
>
> Cet article relève de la vérification matérielle, par le distributeur, de la compatibilité produit et des limites de capacités : toutes les mesures Monitor / Injection / AP / handshake sont réalisées sur les propres équipements de Yupitek, son propre Wi-Fi de bureau, à destination de ses propres téléphones de test ; elles ne visent aucun réseau tiers et ne fournissent aucune procédure offensive contre un réseau externe. Les données du texte sont des chiffres et des états mesurés sur machine réelle, sans extrapolation à partir des fiches techniques.

## L'essentiel (TL;DR)

Mesuré sur ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17) : l'AWUS036ACH fonctionne en mode monitor bi-bande, atteint 30/30 = 100 % d'injection de paquets ciblée par AP sur les deux bandes et monte un point d'accès sur les deux bandes (802.11g pur / 802.11a pur).

- À partir du kernel 6.13, aucune installation de DKMS (ici Ubuntu 24.04 / kernel 6.17) : rtw88_8812au intégré, reconnu dès le branchement.
- Mode monitor bi-bande disponible, injection de paquets par cible de 30/30 = 100 % sur les deux bandes.
- Handshake WPA de bout en bout prouvé : le 2026-11-19, un test complémentaire sur notre propre iPhone 15 Pro, en 5G ch36, a capturé un 4-way complet et exporté 47 hashlines .22000.
- La réception 5 GHz peut se bloquer : seuls un débranchement/rebranchement physique ou un redémarrage y remédient.
- Création d'IBSS en local possible, mais pas de prise en charge du mesh 802.11s, de l'active monitor ni du Wi-Fi Direct (P2P).

## 1. Cette carte et la plateforme de test

L'AWUS036ACH est la carte Wi-Fi USB d'ALFA Network positionnée « bi-antenne à fort gain », à base de puce Realtek RTL8812AU, en Wi-Fi 5 (802.11ac), 2T2R, bi-bande AC1200. Par rapport à la mono-antenne de la même série, l'AWUS036ACHM (MediaTek MT7610U, AC600), l'ACH échange ses deux antennes externes à fort gain contre une meilleure réception et une injection plus stable : c'est un candidat fréquent quand un client demande « monitor longue portée » et « injection sur les deux bandes ».

Plateforme et conditions de test :

- Plateforme de calcul : ASUS GX10 (ARM64 / aarch64)
- Système d'exploitation : Ubuntu 24.04 LTS
- Version du kernel : kernel 6.17.0-1014-nvidia
- Appareil de test : Apple iPhone 7 Plus (2,4G / 5G / WPA3 tous testés sur cet appareil)
- Environnement de test : Wi-Fi de bureau en propre, SSID `YUPITEK` (2,4 GHz ch5 / 5 GHz ch36, ch157)
- Date de test : mesures sur machine réelle le 2026-11-18

On opère exclusivement sur l'interface `wlx*` de la carte ALFA, sans toucher à la carte réseau intégrée qui assure l'accès Internet du GX10, et sans exécuter `airmon-ng check kill` (cette commande arrête NetworkManager et déconnecte la machine).

## 2. Matériel et pilote (puce / USB ID / in-kernel, sans installation)

| Élément | Spécification |
|---|---|
| Modèle | AWUS036ACH |
| Puce | Realtek RTL8812AU |
| USB ID | `0bda:8812` |
| Pilote | `rtw88_8812au` (intégré au kernel, mainline ≥ 6.13) |
| Firmware | `rtw88/rtw8812a_fw.bin` (fourni avec le système) |
| Génération / flux | Wi-Fi 5 (802.11ac) / 2T2R |
| Classe de débit | Bi-bande AC1200 |
| Antenne | Bi-antenne à fort gain (externe) |
| Interface USB | USB 3.0 (énumérée à 5000M en test) |

L'ACH est réellement plug-and-play sur le kernel 6.17 du GX10 : `lsusb` reconnaît `0bda:8812`, le pilote `rtw88_8812au` se lie automatiquement, le firmware `rtw8812a_fw.bin` est déjà fourni avec le système, sans compilation ni DKMS. Ce point est particulièrement important en environnement ARM64. Beaucoup d'anciens pilotes Realtek out-of-tree doivent être compilés depuis les sources sur aarch64, alors que les deux vieux projets morrownr/USB-WiFi et aircrack-ng/rtl8812au redirigent désormais tous deux vers ce pilote intégré, les rapports de bogues se concentrant sur lwfinger/rtw88. Les utilisateurs d'un kernel ≥ 6.13 (dont le 6.17 du GX10) n'ont donc plus à toucher de DKMS tiers ; seul un ancien kernel (< 6.13) nécessite d'installer `lwfinger/rtw88` via DKMS. Ce projet amont est toujours activement maintenu (dernier commit le 2026-10-24, incluant une correction Bluetooth 1T1R du 8812A), signe que le support de cette puce dans le mainline continue d'évoluer : ce n'est pas un vieux pilote figé.

Un détail à surveiller côté connectique : l'ACH est un connecteur mâle USB-A ; utilisez un adaptateur USB-C→A branché directement sur le port USB-C du GX10, en USB 3.0 (énumération à 5000M). La brancher derrière un hub USB 2.0 de clavier/souris la bride et empêche de mesurer le comportement USB3.

Côté modes d'interface, `iw phy` rapporte la prise en charge d'IBSS / managed / AP / AP-VLAN / monitor, mais pas du mesh, du P2P ni de l'active-monitor : cette frontière détermine directement une partie des limites de la section 4.

## 3. Capacités mesurées : Monitor / Injection / AP / WPA3

| Fonction | 2,4 GHz | 5 GHz | Données mesurées |
|---|---|---|---|
| Monitor | ✅ | ✅ | 2,4G ch1/6/11 = 92/214/71 frames ; 5G ch36/149/157 = 260/137/127 frames |
| Injection (probe en diffusion) | ✅ | ✅ | `aireplay-ng --test` probe en diffusion renvoie Injection is working sur les deux bandes |
| Injection (dirigée par cible) | ✅ 30/30 = 100 % | ✅ 30/30 = 100 % | 2,4G sur 4 AP (dont YUPITEK) ; 5G sur YUPITEK ch36 |
| Point d'accès (iPhone 7 Plus) | ✅ 802.11g pur | ✅ 802.11a pur (ch36) | 4-way handshake complet, connecté du premier coup |
| WPA3-SAE AP | ✅ (`sae_pwe=0`) | Non testé | Avec `ieee80211w=2`, iPhone 7 Plus connecté (testé en 2,4 GHz uniquement) |

**Monitor** : en 2,4 GHz sur ch1 / ch6 / ch11, 92 / 214 / 71 frames capturées respectivement ; en 5 GHz sur ch36 / ch149 / ch157, 260 / 137 / 127 frames. Le monitor est correct sur les deux bandes, le volume capturé en 5 GHz dépassant même celui en 2,4 GHz (260 frames sur ch36), conformément au positionnement bi-antenne à fort gain.

**Injection** : c'est le point fort de l'ACH. En 2,4 GHz, `aireplay-ng --test` effectue d'abord une probe en diffusion (renvoie Injection is working, Found 4 APs), puis une injection dirigée par cible : sur les 4 AP dont YUPITEK, le taux de réponse est de 30/30 = 100 %, min/avg/max RTT ~ 4,9 / 39,2 / 99,0 ms, Power ~ -47. L'injection 2,4G de l'ACH bi-antenne est nettement plus stable que celle de l'ACHM mono-antenne. En pratique, pensez à ajouter `--ignore-negative-one` : c'est un phénomène connu (lwfinger/rtw88 #453) : lorsque l'interface STA est ouverte, le canal monitor peut rapporter `-1`, et sans ce drapeau cela serait pris à tort pour un échec d'injection. Par ailleurs, d'après les notes amont, sous injection en forte charge le pilote intégré provoque parfois un USB reset, mais rien de tel n'a été observé sur cette mesure d'environ 90 secondes. En 5 GHz, l'injection dirigée par cible sur YUPITEK (ch36) est également de 30/30 = 100 %, RTT moyen 13,6 ms, Power -69,1. Ce résultat a été mesuré sous le préalable « carte fraîchement branchée + regdomain réglé sur une réglementation autorisant le TX » (détails dans les précautions 5G de la section 4).

**Point d'accès** : AP ouvert avec hostapd, 2,4 GHz en 802.11g pur (`ieee80211n=0`), 5 GHz en 802.11a pur (ch36) ; l'iPhone 7 Plus se connecte du premier coup sur les deux bandes, sans échec d'association ; le log montre les quatre étapes complètes authenticated → associated → AP-STA-CONNECTED → EAPOL-4WAY-HS-COMPLETED. L'expérience de terrain : l'ACH se connecte le plus proprement avec « 802.11n désactivé, g pur / a pur ».

**WPA3-SAE** : pour un AP SAE-only, le paramètre clé est `sae_pwe=0` (hunting-and-pecking) avec `ieee80211w=2`, pour que l'iPhone 7 Plus se connecte ; avec `sae_pwe=2` il ne se connecte pas. C'est le même piège de compatibilité que celui rencontré sur l'ACHM de la même série.

## 4. Capacités avancées et handshake : périmètre réalisable et limites honnêtes

| Capacité avancée | Résultat | Commentaire / preuve |
|---|---|---|
| VIF (STA + monitor simultanés) | ✅ vérifié | Interface principale managed et `mon9` (monitor) up en même temps, la VIF monitor capture 100 frames en 8 s |
| Capture de handshake WPA | ✅ bout en bout (.22000) prouvé | Injection 100 % sur les deux bandes ; test complémentaire du 2026-11-19 en 5G ch36, 4-way complet capturé, 47 hashlines `.22000` exportées par hcxpcapngtool |
| macchanger (changement de MAC) | ✅ | Réglage et restauration d'une MAC aléatoire corrects (nécessite `ip link down` au préalable) |
| Ad-hoc (IBSS) | 🟡 en local | `Joined IBSS` réussi en local ; peer link non testé faute d'un second appareil |
| Active monitor | ❌ | `Operation not supported (-95)` |
| Mesh (802.11s) | ❌ | `Operation not supported (-95)` |
| Wi-Fi Direct (P2P) | ❌ | `Operation not supported (-95)` |

**Il faut être clair sur la capacité de capture de handshake** : l'injection de l'ACH est de 100 % sur les deux bandes, et l'injection est précisément l'amorce de la chaîne de bout en bout « deauth de notre propre téléphone de test → capture complète du 4-way (M1–M4) → export du hashcat `.22000` via hcxpcapngtool ». Le test complémentaire du 2026-11-19, sur notre propre iPhone 15 Pro en 5 GHz ch36, a capturé un 4-way complet et exporté 47 hashlines `.22000` via hcxpcapngtool : la capture de handshake de bout en bout de l'ACH est donc prouvée. Sur le tableau récapitulatif de nos 9 cartes, 7 cartes sur 9 ont un bout en bout (`.22000`) prouvé : AWUS036ACM, AWUS036ACHM, AWUS036ACH, AWUS036ACS, AWUS036EACS, AWUS036AX et AWUS036AXER. Toute capture est limitée aux réseaux dont vous êtes propriétaire ou autorisé.

**VIF** : les drapeaux de `iw phy` indiquent interface combinations are not supported, mais sur machine réelle l'interface principale managed et une interface monitor `mon9` ouverte à côté peuvent être up en même temps ; `mon9` capture 100 frames en 8 secondes, autrement dit « naviguer tout en écoutant » fonctionne sur l'ACH. À signaler toutefois : le phy ne garantit pas cette combinaison ; pour des scénarios longs ou en forte charge, préférez la série mt76 (ACM / ACHM).

**Trois limites à signaler particulièrement :**

1. **Pas de prise en charge de l'Active monitor, du Mesh (802.11s) ni du Wi-Fi Direct (P2P)** : les trois renvoient `Operation not supported (-95)` en test. Pour ces trois capacités, utilisez une carte de la série mt76 (le phy des ACM / ACHM déclare mesh / P2P / active-monitor).
2. **Blocage du RX 5G (phénomène connu du `rtw88_8812au`)** : à la première insertion, le monitor / l'injection 5G fonctionnent, mais après des bascules répétées de mode ou un changement de regdomain, la réception 5G peut se bloquer (0 paquet capturé), sans récupération logicielle possible : il faut débrancher/rebrancher physiquement ou redémarrer. Il est conseillé de rebrancher une fois avant un test 5G et de traiter en priorité les points 5G. Un complément sur le préalable à l'émission d'injection 5G : sous `country 00` par défaut, le 5G est entièrement en passive / no-IR (TX interdit), et l'injection dirigée ne part tout simplement pas ; réglez une réglementation autorisant le TX (`iw reg set US` déverrouille ch36 / ch149, `TW` n'autorise qu'à partir de ch149, sans ch36), puis remettez `TW` après le test. « Carte fraîchement branchée » signifie un débranchement/rebranchement physique jusqu'à ré-énumération USB : `dmesg` doit montrer `USB disconnect` et `renamed from wlan0`, et le numéro de bus doit changer ; si le 5G est déjà bloqué, aireplay renvoie `No such BSSID available`.
3. **hcxdumptool échoue en `failed to arm` sur toutes les cartes de cette plateforme, sauf l'AWUS036EACS en 2,4 GHz** : parce qu'il exige l'active-monitor, que ni rtw88, ni rtw89, ni mt7921u ne prennent en charge ; pour capturer un handshake, passez par airodump-ng + aireplay-ng.

### Compatibilité de la chaîne d'outils (Kali)

Un filtrage rapide des outils Kali courants a été réalisé sur l'ACH (cible : notre propre `YUPITEK`), avec les résultats suivants :

| Outil | État | Commentaire |
|---|---|---|
| airmon-ng | ✅ | Liste correctement `phy2 / wlx... / rtw88_8812au / RTL8812AU 2T2R` |
| Wireshark / tshark | ✅ | `tshark -i $IF` capture des beacons (dont YUPITEK), 20 packets captured |
| kismet | ✅ installé | `/usr/bin/kismet`, démarrable comme data source |
| bettercap | ✅ installé | `/usr/bin/bettercap` |
| hcxdumptool | ⚠️ | Installé, mais `failed to arm` sur cette plateforme (exige l'active-monitor, voir ci-dessus) |
| macchanger | ✅ | GNU 1.7.0 ; `-r` aléatoire, `-p` restauration, corrects en test |
| wifite | ❌ non installé | Commande absente de la machine, à installer (version git conseillée, pour éviter le conflit de dépendances apt avec l'aircrack-ng compilé maison) |

La conclusion est simple : airmon-ng reconnaît et gère correctement l'ACH ; pour le monitor général et la chaîne de capture, la suite aircrack-ng (airodump-ng + aireplay-ng) est la plus stable ; hcxdumptool, qui exige l'active-monitor, ne peut pas s'armer sur cette plateforme — ne vous bloquez pas dessus.

## 5. Cas d'usage et conseils de choix (retour au Hub)

Replacée dans toute la gamme produit, la position de l'ACH est claire : bi-antenne à fort gain, injection 100 % sur les deux bandes, handshake WPA de bout en bout (.22000) prouvé — le choix pragmatique pour un client « qui veut une injection stable et une meilleure réception ».

- **Test d'intrusion (injection + handshake)** : le groupe de tête est AWUS036EACS / AWUS036ACH / AWUS036ACS, les trois ayant une injection bi-bande de haut niveau.
- **Meilleure réception / monitor longue portée** : AWUS036AXER et AWUS036ACH, l'ACH se distinguant par son fort gain bi-antenne.
- **Besoin de mesh 802.11s / active-monitor / P2P** : l'ACH (Realtek rtw88) ne les fait pas (renvoie `-95` en test) ; utilisez une carte à pilote mt76, AWUS036ACM / AWUS036ACHM ; l'IBSS de l'ACH ne se monte qu'en local, le peer-link n'est pas testé.
- **Besoin d'un simple AP ou d'une connexion ordinaire, sans injection** : les MediaTek AWUS036AXM / AXML sont plus stables, mais attention : leur injection échoue sur cette plateforme, inadaptée à un usage d'intrusion.

Un rappel pour éviter le piège : si le besoin du client est clairement l'injection et le handshake, ne choisissez pas l'AWUS036AXM / AXML (l'injection des puces MT7921 échoue en test sur cette plateforme, impossible de faire un deauth ni de capturer un handshake) ; pour ce besoin, l'ACH est au contraire un candidat sûr. Lors du choix, ne regardez pas seulement les chiffres de débit : la stabilité de réception apportée par le fort gain bi-antenne fait souvent une différence plus sensible sur la distance d'écoute réelle que sur la fiche technique. Pour la décision de choix et les pièges communs à la plateforme, voyez le tableau Hub : [Matrice complète Monitor · Injection · AP des 9 cartes Wi-Fi ALFA sur ASUS GX10 (ARM64)](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Questions fréquentes (FAQ)

**Q : L'AWUS036ACH nécessite-t-elle l'installation d'un pilote sous Kali ou Ubuntu ?**
Cela dépend de la version du kernel. À partir du kernel Linux 6.13 (ici Ubuntu 24.04 / kernel 6.17), le pilote rtw88_8812au est intégré : reconnaissance dès le branchement, sans compilation ni DKMS ; en dessous du kernel 6.13, il faut installer lwfinger/rtw88 via DKMS. Sous Kali, vérifiez d'abord la version du kernel avec uname -r ; cela n'a pas été vérifié sur une machine Kali réelle cette fois-ci.

**Q : Comment se comportent le mode monitor et l'injection de paquets de l'AWUS036ACH ?**
Le mode monitor fonctionne en 2,4 GHz comme en 5 GHz ; l'injection dirigée par cible avec aireplay-ng est de 30/30 = 100 % aussi bien en 2,4 GHz (sur 4 AP) qu'en 5 GHz (sur YUPITEK ch36). Avant une injection 5 GHz, réglez le domaine réglementaire pour autoriser l'émission (par exemple iw reg set US) : sous le country 00 par défaut, le 5 GHz interdit l'émission et l'injection ne part pas.

**Q : L'AWUS036ACH peut-elle capturer un handshake WPA ?**
Oui, et c'est prouvé de bout en bout. L'injection est de 100 % sur les deux bandes ; le 2026-11-19, un test complémentaire sur notre propre iPhone 15 Pro, en 5 GHz ch36, a capturé un 4-way handshake complet et exporté 47 hashlines hashcat .22000 via hcxpcapngtool. Uniquement sur des réseaux dont vous êtes propriétaire ou autorisé.

**Q : Que faire si l'iPhone 7 Plus n'arrive pas à se connecter au point d'accès WPA3 de l'AWUS036ACH ?**
hostapd doit être réglé sur sae_pwe=0 avec ieee80211w=2 pour que l'iPhone 7 Plus se connecte ; avec sae_pwe=2 il ne se connecte pas. Le même réglage est également décisif sur l'AWUS036ACHM.

**Q : Que faire si la réception 5 GHz de l'AWUS036ACH se bloque soudainement (0 paquet capturé) ?**
C'est un phénomène connu du rtw88_8812au : après des bascules répétées de mode ou des changements de domaine réglementaire, la réception 5 GHz peut se bloquer, sans récupération logicielle possible ; il faut débrancher/rebrancher physiquement ou redémarrer. Il est conseillé de rebrancher la carte avant un test 5 GHz et de traiter en priorité les points 5 GHz.

## 6. Pour aller plus loin

- Tableau Hub : [Matrice complète des 9 cartes Wi-Fi ALFA sur ARM64](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Activer Monitor et AP sans installation de pilote sous Ubuntu (ARM64) : [placeholder](/fr/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- Capture de handshake WPA3-SAE et compatibilité `sae_pwe` : [placeholder](/fr/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Comparaison avec la carte sœur : test individuel de l'AWUS036ACHM (mono-antenne AC600) [placeholder]
- Chemin de preuve complet de ce modèle (interne) : `AWUS036ACH_evidence/` (énumération p0, comportement p1_gx10, dépannage retest)

<!-- hreflang : zh-TW est la version principale ; zh-CN / en / ja / ko / de / fr / es à générer et à compléter avec rel=alternate après finalisation de la version principale. -->
