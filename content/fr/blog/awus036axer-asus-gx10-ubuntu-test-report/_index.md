---
title: "Rapport de test de l'AWUS036AXER : la carte Wi-Fi 6 à la meilleure réception sur ASUS GX10 + Ubuntu 24.04 (ARM64)"
slug: awus036axer-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axer-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036axer
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - ubuntu-24-04
  - kernel-6-17
  - arm64
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
description: "L'AWUS036AXER fonctionne sans installation de pilote (rtw89_8852bu) sur ASUS GX10 / Ubuntu 24.04 ARM64 : monitor 60 s détecte 63 AP + 12 clients, injection 73 % (2,4G), AP 5G VHT80 et WPA3 tous validés."
faq:
  - question: "L'AWUS036AXER nécessite-t-elle l'installation d'un pilote supplémentaire sous Ubuntu 24.04 ou Kali ?"
    answer: "Sous Ubuntu 24.04 (ARM64, kernel 6.17.0-1014-nvidia), non : le pilote intégré rtw89_8852bu est reconnu dès le branchement, sans compilation ni DKMS (firmware rtw8852b_fw 0.29.29.5). La plateforme de cet article est Ubuntu et non la distribution Kali ; Kali elle-même n'a pas été testée ; les outils Kali courants airmon-ng, kismet, bettercap, wifite, Wireshark sont utilisables sur cette plateforme. Sur un kernel plus ancien, l'intégration n'est pas garantie, vérifiez d'abord la version."
  - question: "L'AWUS036AXER prend-elle en charge le mode monitor ? Quelle est la force de sa réception ?"
    answer: "Oui, le monitor fonctionne en 2,4 GHz comme en 5 GHz. Dans notre propre bureau, un balayage en saut de fréquence de 60 secondes avec airodump-ng a détecté 63 AP et 12 clients : c'est la meilleure réception des neuf cartes testées au même endroit ; l'AWUS036AX à même puce a donné 14 AP + 4 clients lors d'un autre test (deux mesures non simultanées, à titre indicatif)."
  - question: "L'AWUS036AXER peut-elle faire de l'injection de paquets (packet injection) ?"
    answer: "Oui. En 2,4 GHz, aireplay-ng --test donne un taux de réponse de 73 % (22/30) et affiche Injection is working! ; le test par cible en 5 GHz passe aussi ; nous avons réalisé la capture de handshake sur notre propre réseau et nos propres appareils, avec export en .22000. Pour approcher 100 % sur les deux bandes, les mesures sur cette plateforme désignent l'AWUS036EACS, l'ACH et l'ACS comme plus stables. Uniquement sur des réseaux dont vous êtes propriétaire ou autorisé."
  - question: "Quelle différence entre l'AWUS036AXER et l'AWUS036AX ?"
    answer: "Les deux reposent sur le Realtek RTL8832BU et le même rtw89_8852bu, avec une prise en charge des modes et un comportement d'injection identiques sur cette plateforme ; la différence tient à la performance de réception apportée par le réglage et le gain d'antenne (AXER : 63 AP + 12 clients en 60 s ; AX : 14 AP + 4 clients). Les deux ont des antennes intégrées, sans RP-SMA ; référez-vous à la fiche produit pour les spécifications d'antenne."
  - question: "L'AWUS036AXER peut-elle servir d'AP ou ouvrir du WPA3 ? Quels modes ne prend-elle pas en charge ?"
    answer: "Oui. En 2,4 GHz 802.11n et en 5 GHz VHT80 (VHT-NSS2, 351 Mbit), l'iPhone se connecte et est authorized ; le WPA3-SAE avec sae_pwe=0 connecte l'iPhone 15 Pro (en 2,4 GHz ; WPA3 en 5 GHz non testé) ; le STA+AP en parallèle fonctionne. Mais le rtw89_8852bu ne prend pas en charge l'active monitor, l'IBSS ni le mesh."
draft: false
---

{{< tldr >}}L'AWUS036AXER est plug-and-play sur ASUS GX10 / Ubuntu 24.04 ARM64 (rtw89_8852bu intégré) ; le monitor détecte 63 AP + 12 clients en 60 s, l'injection 2,4 GHz est à 73 %, l'AP et le WPA3 passent tous les deux ; pas de prise en charge de l'active monitor, de l'IBSS ni du mesh.{{< /tldr >}}

> Cet article est un test de compatibilité produit et de capacités réalisé par Yopitek (distributeur ALFA à Taïwan) sur ses propres équipements.
> Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. L'environnement de test est notre propre Wi-Fi de bureau (SSID `YUPITEK`), à destination de notre propre téléphone de test iPhone 7 Plus (WPA3 aussi testé sur iPhone 15 Pro).
> ⚠️ **Usage légal** : le mode monitor et l'injection ne concernent que les réseaux et appareils dont vous êtes propriétaire ou autorisé ; pour le mode AP, respectez la réglementation radio locale. Cet article se concentre sur les capacités, la compatibilité, la configuration et le choix de la carte, et ne couvre aucune opération offensive visant un réseau tiers.

---

## 1. Cette carte et la plateforme de test

L'AWUS036AXER est la carte Wi-Fi 6 (802.11ax) 2x2 USB d'ALFA, à base de puce Realtek RTL8832BU (sans Bluetooth). Elle utilise **la même puce et le même pilote** (`rtw89_8852bu`) que l'AWUS036AX du même fabricant, avec une prise en charge des modes et un comportement identiques sur cette plateforme ; leur vraie différence tient au **réglage et au gain d'antenne**, non au fait d'être externe ou interne — l'AXER adopte une **conception à antenne intégrée (Nano), sans RP-SMA**, et pousse la réception au maximum via la puce et le réglage RF. Retenez d'abord la conclusion centrale de cet article : parmi les neuf cartes ALFA comparées au même endroit, l'AXER a **la meilleure réception**.

La plateforme de test est un ASUS GX10, doté de la super-puce NVIDIA GB10 et de 128GB de mémoire unifiée, sous Ubuntu 24.04 LTS, architecture ARM64 (aarch64), kernel `6.17.0-1014-nvidia`. Tous les résultats ont été obtenus sur cette machine réelle le 2026-11-18 ; l'appareil de test est notre propre iPhone 7 Plus (WPA3 aussi testé sur iPhone 15 Pro), le réseau de test est notre propre Wi-Fi de bureau. Pour une validation de distribution, l'ARM64 avec un kernel récent est une combinaison relativement exigeante ; la section 2 ci-dessous explique pourquoi cette génération est au contraire plus simple.

Un complément de contexte sur les spécifications : l'AXER est une carte Wi-Fi 6 2x2 (deux flux spatiaux), capable d'émettre et recevoir deux flux spatiaux à la fois, ce qui correspond au VHT-NSS2 négocié plus loin dans le test d'AP 5 GHz. Mais si cette carte l'emporte dans ce cycle, c'est grâce à la conception d'antenne et au réglage RF, pas au nombre de flux (l'AX est aussi 2x2). Puce, pilote et plateforme étant tous identiques, le réglage d'antenne est quasiment la seule variable : l'écart de réception entre l'AXER et l'AX peut donc être proprement imputé à la conception d'antenne intégrée et au réglage de gain.

---

## 2. Matériel et pilote (antenne intégrée, sans installation de pilote)

L'AWUS036AXER est **reconnue dès le branchement, sans compilation ni DKMS** sur le kernel 6.17 d'Ubuntu 24.04. Le pilote `rtw89_8852bu` est déjà un module in-kernel, avec le firmware `rtw8852b_fw` (version 0.29.29.5), chargé au démarrage, sans avoir à récupérer un projet out-of-tree sur GitHub ni à lier un DKMS. Pour des environnements de distribution et d'enseignement qui exigent une exploitation à long terme sur plusieurs mises à jour du kernel, supprimer l'étape de compilation du pilote, c'est supprimer l'un des points de panne les plus fréquents.

La comparaison avec l'ancienne voie le rend plus sensible : par le passé, ce genre de puce USB Realtek n'entrait généralement pas dans le kernel mainline, et l'utilisateur devait récupérer un projet out-of-tree sur GitHub (par exemple `morrownr/USB-WiFi`) puis le compiler via DKMS contre le kernel courant, à recompiler à chaque mise à jour du kernel, la carte disparaissant dès qu'une compilation échouait. Une fois rtw89 officiellement intégré in-kernel, ces étapes se suppriment entièrement sur le 6.17, et la même procédure se réutilise sur plusieurs cartes à même pilote.

D'abord, confirmer que la carte est correctement reconnue :

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
# Bus 00x Device 00x: ID 0bda:b832 Realtek Semiconductor Corp. 802.11ac WLAN Adapter
```

L'USB ID en mode WLAN normal est `0bda:b832`. Si vous voyez `0bda:1a2b`, c'est que la carte est encore en « mode CD-ROM » ; exécutez une fois `sudo usb_modeswitch -v 0bda -p 1a2b -K` pour basculer en mode WLAN ; notre carte de test s'est énumérée directement en mode WLAN, sans rencontrer le mode CD-ROM.

L'interface est nommée `wlx` + MAC (par exemple `wlxAABBCCDDEEFF`), inchangée quelle que soit la machine, facile à référencer dans un script. Pour voir les modes pris en charge :

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Les modes rapportés sont managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO. Pas d'IBSS, pas de mesh, pas d'active monitor : c'est une limite intrinsèque du pilote rtw89, expliquée honnêtement en section 4 — ne vous y trompez pas au moment du choix.

Côté antenne : l'AXER adopte une conception à antenne intégrée (Nano), sans RP-SMA ; par rapport à l'AX à même puce, la différence tient au réglage et au gain d'antenne, dont le reflet le plus direct en pratique est la réception. Les données de monitor de la section suivante l'illustrent clairement.

---

## 3. Capacités mesurées

Voici d'abord un tableau des résultats mesurés pour les trois capacités centrales (Monitor / Injection / AP) et le WPA3, le détail suivant point par point :

| Capacité | 2,4 GHz | 5 GHz | Point clé mesuré |
|---|---|---|---|
| **Monitor (écoute)** | ✅ fort | ✅ fort | Saut de fréquence : **63 AP + 12 clients**, meilleure réception des neuf cartes |
| **Injection** | ✅ 73 % | ✅ disponible | 2,4G `22/30 73 %` ; 5G `Injection is working!` |
| **AP (point d'accès)** | ✅ 802.11n | ✅ VHT 80 MHz | iPhone connecté ; 5G VHT-NSS2, 351 Mbit |
| **WPA3-SAE** | ✅ | Non testé | Côté AP, iPhone 15 Pro connecté (`sae_pwe=0`) ; testé en 2,4 GHz uniquement |
| **Capture de handshake WPA** | ✅ bout en bout | — | Réseau et appareils en propre, 4-way (M1–M4) → `.22000` |

### 3-1. Monitor (le point fort de cet article : la meilleure réception)

Passer en monitor suit le flux `iw` standard : rendre d'abord l'interface à sa propre gestion (`nmcli dev set $IF managed no`), descendre l'interface, régler le type monitor, remonter l'interface, régler le canal :

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36        # 5 GHz ; en 2,4 GHz, channel 6
sudo timeout 8 tcpdump -l -i $IF -nn -e -c 200
```

En 2,4 GHz comme en 5 GHz, 100 frames sont captées en 6 secondes. Ce qui creuse vraiment l'écart, c'est le balayage en saut de fréquence : `sudo airodump-ng --band abg $IF` sur 60 secondes **détecte 63 AP et 12 clients**. C'est la carte qui capte le plus de cibles de ce cycle sur les neuf, reflet direct de l'avantage de réception apporté par la conception à antenne intégrée et le réglage RF. Pour une prospection de site (site survey), une écoute longue portée, ou un environnement à signal faible, cette capacité de réception est le cœur de la valeur de l'AXER.

### 3-2. Injection

L'injection se vérifie avec le mode d'autotest d'aireplay-ng, qui mesure la capacité de la carte elle-même, pas une attaque externe :

```bash
sudo iw dev $IF set channel 6
sudo aireplay-ng --test $IF
# Found 21 APs
# 22/30:  73%
# Injection is working!
```

Taux de réponse de 73 % (22/30) en 2,4 GHz, jugé disponible. En 5 GHz, l'autotest par cible sur un AP désigné renvoie aussi `Injection is working!`. Un rappel général de plateforme : **avant d'émettre/injecter en 5 GHz, déverrouillez la puissance TX via `iw reg set US`, puis repassez aux bandes réglementaires de Taïwan via `iw reg set TW` après le test**.

### 3-3. Point d'accès (2,4 GHz 802.11n, 5 GHz VHT 80 MHz)

L'AXER peut monter un AP hostapd sur les deux bandes. En 2,4 GHz avec `hw_mode=g` + `ieee80211n=1`, AP 802.11n ouvert, l'iPhone 7 Plus se connecte et négocie MCS 15, authorized. En 5 GHz avec `hw_mode=a` + `ieee80211ac=1` + `vht_oper_chwidth=1`, AP VHT 80 MHz ouvert, l'iPhone 7 Plus se connecte et négocie **VHT-NSS2, 80 MHz, 351 Mbit, authorized**. Le préalable à l'ouverture de l'AP est `sudo nmcli dev set $IF managed no`, et `wpa_passphrase` doit faire au moins 8 caractères, sans quoi hostapd renvoie `invalid WPA passphrase length`.

### 3-4. WPA3-SAE et capture de handshake

Pour le WPA3-SAE, côté AP, réglez `wpa_key_mgmt=SAE`, `ieee80211w=2`, `sae_pwe=0` ; en test, l'iPhone 15 Pro se connecte. **Le `sae_pwe` est le piège de compatibilité de ce lot de cartes ALFA** : certains appareils ne se connectent pas avec `sae_pwe=2` (Hash-to-Element) ; régler `sae_pwe=0` assure la compatibilité avec les iPhone plus anciens.

La capacité de handshake est une vérification de bout en bout sur **notre propre Wi-Fi de bureau (YUPITEK) + nos propres appareils de test** : capture du 4-way complet (M1/M2/M3/M4), puis export en `.22000` lisible par hashcat via `hcxpcapngtool`. À signaler ici un phénomène commun à la plateforme GX10 : **`hcxdumptool` échoue en `failed to arm` sur toutes les cartes USB de cette plateforme, sauf l'AWUS036EACS en 2,4 GHz** (conflit d'énumération de la carte intégrée tri-bande du GX10, plus l'absence d'active monitor dans le pilote), le flux de handshake passe donc par la suite aircrack-ng (airodump-ng + aireplay-ng). La capacité d'injection de l'AXER suffit pour cette voie.

---

## 4. Fonctions avancées et limites honnêtes

**VIF (STA + AP en parallèle) ✅** : l'AXER peut à la fois être station connectée au Wi-Fi amont et ouvrir une VIF AP. En test, l'interface principale connectée à YUPITEK et la VIF AP ouverte en ch36 VHT80 fonctionnent en parallèle, ping côté STA 3,5 ms, adapté au scénario « se connecter tout en ouvrant un point d'accès ».

**Wi-Fi Direct (P2P) non testé (⬜)** : le pilote déclare P2P-client / P2P-GO, mais une vérification complète nécessite un second équipement d'appairage, passé ce cycle ; nous ne le comptons donc pas dans les capacités vérifiées. Pour ce genre de point « déclaré pris en charge par le pilote mais non exécuté sur machine réelle », nous le marquons honnêtement comme non testé, sans le gonfler en réussite.

**Les trois modes non pris en charge (N/A)** : le pilote `rtw89_8852bu` **ne fournit pas l'active monitor, l'Ad-hoc (IBSS) ni le Mesh (802.11s)**. `iw dev $IF set type ibss` ou `mp` échoue directement : c'est une limite au niveau du pilote, impossible à contourner par configuration. Pour une expérimentation mesh ou IBSS, tournez-vous vers la série MediaTek mt76 (comme l'AWUS036ACM / ACHM).

**Précautions communes à la plateforme :**

- N'exécutez jamais `airmon-ng check kill`, il arrête NetworkManager et déconnecte le GX10 d'Internet. Opérez uniquement sur l'interface `wlx*`, sans toucher à la carte réseau intégrée qui assure l'accès Internet.
- Si après des bascules répétées monitor/AP plus rien n'est détecté (RX stall), **débranchez et rebranchez** la carte une fois pour récupérer (ré-énumération USB, le nom d'interface est déterminé par la MAC et ne change pas).
- Sur plateforme ARM64, aircrack-ng doit être compilé depuis les sources ; utilisez wifite en version git pour contourner le conflit de dépendances apt.

**Compatibilité des outils Kali** : airmon-ng, kismet 2026.10, bettercap 2.32, wifite (git), Wireshark / tshark 4.2 utilisent tous l'AXER normalement comme source de données ou interface de gestion.

---

## 5. Cas d'usage et conseils de choix

Positionnement en une phrase : **l'AXER est une carte Wi-Fi 6 « orientée réception ».** Même puce et mêmes fonctions que l'AX, la différence étant l'avantage de réception apporté par le réglage et le gain d'antenne — la logique de choix est donc claire :

| Votre besoin | L'AXER est-elle le premier choix ? | Commentaire |
|---|---|---|
| Meilleure réception / monitor longue portée / prospection sur site | ✅ **premier choix** | Saut de fréquence : 63 AP + 12 clients, la meilleure des neuf cartes ; complémentaire avec l'AWUS036ACH (fort gain bi-antenne) |
| Wi-Fi 6 + point d'accès | ✅ adaptée | 2x2, 5G VHT80 ; même niveau que l'AWUS036AX |
| Injection + handshake de bout en bout | 🟡 disponible | 2,4G 73 % disponible ; pour approcher 100 % sur les deux bandes, l'AWUS036EACS / ACH / ACS sont plus stables |
| Expérimentation mesh / IBSS | ❌ inadaptée | rtw89 ne la prend pas en charge, utilisez l'AWUS036ACM / ACHM (mt76) |

Scénario typique de mise en œuvre : utiliser l'AXER comme **nœud de surveillance sans fil distant**, placé sur un point à signal faible ou éloigné, en comptant sur l'avantage de réception de son antenne intégrée pour capter au mieux les AP / clients du site, les résultats de balayage étant ensuite regroupés sur une machine centrale pour examen unifié. Son antenne étant intégrée (Nano), sans RP-SMA, elle n'est pas remplaçable ; pour un gain plus élevé ou une directivité plus forte, complétez avec l'AWUS036ACH à fort gain bi-antenne.

À l'inverse, si l'usage est un simple AP ou une connexion ordinaire, sans aucun besoin d'injection, les MediaTek AWUS036AXM / AXML conviennent aussi ; mais **dès que l'injection ou le handshake entrent en jeu, ne choisissez pas l'AXM / AXML**, dont l'injection échoue sur cette plateforme (cause principale : une régression de mac80211 chanctx depuis le noyau 6.16, à laquelle s'ajoute un firmware qui verrouille le débit d'injection à 1/6 Mbit/s ; ce n'est pas une limite de la puce elle-même). L'AXER est exactement l'inverse : injection disponible et réception la meilleure.

Pour voir d'un coup la matrice complète et la comparaison croisée des neuf cartes, revenez à la page d'évaluation globale → [`/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

---

## Questions fréquentes (FAQ)

**Q1. L'AWUS036AXER nécessite-t-elle l'installation d'un pilote supplémentaire sous Ubuntu 24.04 ou Kali ?**
Sous Ubuntu 24.04 (ARM64, kernel 6.17.0-1014-nvidia), non : le pilote intégré `rtw89_8852bu` est reconnu dès le branchement, sans compilation ni DKMS (firmware `rtw8852b_fw` 0.29.29.5). La plateforme de cet article est Ubuntu et non la distribution Kali ; Kali elle-même n'a pas été testée ; les outils Kali courants airmon-ng, kismet, bettercap, wifite, Wireshark sont utilisables sur cette plateforme. Sur un kernel plus ancien, l'intégration n'est pas garantie, vérifiez d'abord la version.

**Q2. L'AWUS036AXER prend-elle en charge le mode monitor ? Quelle est la force de sa réception ?**
Oui, le monitor fonctionne en 2,4 GHz comme en 5 GHz. Dans notre propre bureau, un balayage en saut de fréquence de 60 secondes avec airodump-ng a détecté 63 AP et 12 clients : c'est la meilleure réception des neuf cartes testées au même endroit ; l'AWUS036AX à même puce a donné 14 AP + 4 clients lors d'un autre test (deux mesures non simultanées, à titre indicatif).

**Q3. L'AWUS036AXER peut-elle faire de l'injection de paquets (packet injection) ?**
Oui. En 2,4 GHz, `aireplay-ng --test` donne un taux de réponse de 73 % (22/30) et affiche `Injection is working!` ; le test par cible en 5 GHz passe aussi ; nous avons réalisé la capture de handshake sur notre propre réseau et nos propres appareils, avec export en `.22000`. Pour approcher 100 % sur les deux bandes, les mesures sur cette plateforme désignent l'AWUS036EACS, l'ACH et l'ACS comme plus stables. Uniquement sur des réseaux dont vous êtes propriétaire ou autorisé.

**Q4. Quelle différence entre l'AWUS036AXER et l'AWUS036AX ?**
Les deux reposent sur le Realtek RTL8832BU et le même `rtw89_8852bu`, avec une prise en charge des modes et un comportement d'injection identiques sur cette plateforme ; la différence tient à la performance de réception apportée par le réglage et le gain d'antenne (AXER : 63 AP + 12 clients en 60 s ; AX : 14 AP + 4 clients). Les deux ont des antennes intégrées, sans RP-SMA ; référez-vous à la fiche produit pour les spécifications d'antenne.

**Q5. L'AWUS036AXER peut-elle servir d'AP ou ouvrir du WPA3 ? Quels modes ne prend-elle pas en charge ?**
Oui. En 2,4 GHz 802.11n et en 5 GHz VHT80 (VHT-NSS2, 351 Mbit), l'iPhone se connecte et est authorized ; le WPA3-SAE avec `sae_pwe=0` connecte l'iPhone 15 Pro (en 2,4 GHz ; WPA3 en 5 GHz non testé) ; le STA+AP en parallèle fonctionne. Mais le `rtw89_8852bu` ne prend pas en charge l'active monitor, l'IBSS ni le mesh.

---

## 6. Pour aller plus loin

- Matrice complète des neuf cartes ALFA et tableau de choix (comparaison Monitor · Injection · AP) → `/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`
- Test de l'AWUS036AX à même puce (réglage d'antenne différent) → `/fr/blog/awus036ax-asus-gx10-ubuntu-test-report/`
- Sans installation de pilote : activer les modes Monitor et AP avec le pilote in-kernel → `/fr/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`
- Capacité de capture de handshake à l'ère du WPA3-SAE et compatibilité `sae_pwe` → `/fr/blog/alfa-wpa3-sae-handshake-capability-arm64/`

<!-- Les liens internes de la section « Pour aller plus loin » recevront leurs URL hreflang définitives après finalisation ; ci-dessus, des slugs placeholder. -->

---

*Unité de test : Yopitek (distributeur ALFA) — https://www.yupitek.com | Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Appareil de test : Apple iPhone 7 Plus (WPA3 aussi testé sur iPhone 15 Pro)*
