---
title: "AWUS036ACS, test carte par carte : la carte nomade légère RTL8811AU sur ASUS GX10 + Ubuntu 24.04 (ARM64) — rapport de compatibilité et de capacités"
slug: awus036acs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acs
  - rtl8811au
  - rtw88-8821au
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
description: "AWUS036ACS testée sous Ubuntu 24.04 ARM64 : sans installation de pilote, Monitor, injection (2,4G 100 %, 5G 96 %), AP, WPA3-SAE et handshake de bout en bout (.22000) tous validés. Plateforme ASUS GX10, kernel 6.17, RTL8811AU."
faq:
  - question: "L'AWUS036ACS nécessite-t-elle l'installation d'un pilote sous Ubuntu 24.04 ARM64 ?"
    answer: "Sur le kernel 6.17 testé ici (ASUS GX10), non : le RTL8811AU est pris en charge par le pilote intégré rtw88_8821au, reconnu dès le branchement, sans compilation ni DKMS. Sur un kernel plus ancien, vérifiez d'abord la présence du module avec modinfo rtw88_8821au."
  - question: "L'AWUS036ACS prend-elle en charge le mode monitor et l'injection de paquets ?"
    answer: "Oui. Le monitor fonctionne en 2,4 GHz comme en 5 GHz ; au test aireplay-ng --test, l'injection est de 100 % en 2,4G (30/30) et de 96 % en 5G (29/30, après avoir levé la restriction TW via iw reg set US). L'active monitor n'est pas pris en charge."
  - question: "L'AWUS036ACS peut-elle capturer un handshake WPA et l'exporter en hashcat .22000 ?"
    answer: "Oui. Test de bout en bout sur notre propre AP et notre propre iPhone 7 Plus : deauth dirigé pour déclencher la reconnexion, capture du 4-way complet (M1–M4), puis export en .22000 via hcxpcapngtool --all. Uniquement sur des réseaux dont vous êtes propriétaire ou autorisé."
  - question: "L'AWUS036ACS peut-elle servir de point d'accès ? Prend-elle en charge le WPA3 ?"
    answer: "Oui. hostapd ouvre un point d'accès en 2,4G et en 5G (5G testé en 802.11a à 20 MHz ; VHT80 non testé), l'iPhone 7 Plus se connecte et complète le 4-way ; le WPA3-SAE en 5G (SAE-only, ieee80211w=2, sae_pwe=0) se connecte aussi avec succès (WPA3 en 2,4G non testé)."
  - question: "Quels modes l'AWUS036ACS ne prend-elle pas en charge ? hcxdumptool fonctionne-t-il ?"
    answer: "Elle ne prend pas en charge l'active monitor, l'IBSS, le mesh (802.11s) ni le Wi-Fi Direct (P2P). hcxdumptool 8.x échoue en failed to arm interface ; utilisez airodump-ng + aireplay-ng. Pour le mesh / IBSS, choisissez l'AWUS036ACM / ACHM."
draft: false
---

**L'essentiel (TL;DR)** : selon les tests de Yopitek (distributeur ALFA Network à Taïwan), l'AWUS036ACS fonctionne sans installation de pilote sur ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17), avec monitor et AP bi-bande (AP 5G utilisable : 802.11a, 20 MHz testé ; VHT80 non testé) ; injection 2,4G 100 %, 5G 96 %, bout en bout .22000 validé, pas de prise en charge du mesh / IBSS.

> Cet article est le compte rendu, réalisé par Yopitek, des tests de compatibilité produit et de capacités de l'ALFA AWUS036ACS sur une plateforme Linux récente, destiné à l'évaluation et au choix de modèle.
> Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Toutes les données sont des extraits de mesures réalisées par Yopitek sur **ses propres équipements, son propre réseau Wi-Fi de bureau** (SSID `YUPITEK`, 2,4G ch5 / 5G ch36) à destination de **ses propres téléphones de test** (Apple iPhone 7 Plus) ; les adresses MAC sont partiellement masquées.
> ⚠️ **Déclaration de légalité et de périmètre** : le mode monitor, l'injection et la capture de handshake ne sont réalisés que sur des réseaux et des appareils dont vous êtes propriétaire ou autorisé ; pour le mode AP, respectez la réglementation radio locale. Cet article se concentre sur les capacités, la compatibilité et la configuration de la carte elle-même, et **ne couvre aucune opération offensive visant un réseau tiers**.

---

## 1. Cette carte et la plateforme de test

L'AWUS036ACS est la carte Wi-Fi nomade légère de la gamme ALFA, à base de puce Realtek RTL8811AU, de génération Wi-Fi 5 (802.11ac), 1x1 à flux spatial unique. Son positionnement est direct : format compact, faible consommation, mono-antenne — c'est la carte que l'on emporte pour un inventaire sur site, pas la carte lourde qui vise le débit maximal ou la plus grande portée. L'évaluer, ce n'est donc pas se demander « à quelle vitesse va-t-elle », mais « avec des spécifications aussi légères, quelles capacités pratiques restent pleinement utilisables ».

Ce cycle de tests la place dans un scénario d'exploitation typique : la carte intégrée du GX10 (`wlP9s9`) assure l'accès Internet, l'AWUS036ACS, branchée en USB, ne porte que la charge de test. Ainsi, le passage en monitor ou en AP ne touche jamais au réseau de la machine hôte. On opère exclusivement sur l'interface `wlx*` de la carte ALFA, sans toucher à la carte réseau intégrée.

| Élément | Contenu |
|---|---|
| Modèle | AWUS036ACS |
| Puce | Realtek RTL8811AU (Wi-Fi 5 / 802.11ac, 1x1 flux unique) |
| USB ID | `0bda:0811` |
| Pilote | `rtw88_8821au` (in-kernel, intégré au kernel 6.17) |
| Firmware | 42.4.0 (mesuré via dmesg) |
| Plateforme | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| Appareil de test | Apple iPhone 7 Plus |

---

## 2. Matériel et pilote (sans installation)

Cette carte est reconnue dès le branchement sur le GX10, sans compilation ni DKMS. La puce RTL8811AU / RTL8821AU a été officiellement intégrée à la famille de pilotes in-kernel `rtw88` de Realtek depuis le kernel mainline 6.13 ; le 6.17 du GX10 embarque déjà le module `rtw88_8821au`, sans avoir à récupérer de projet out-of-tree sur GitHub. (Contrairement aux anciens guides d'installation : les articles anciens supposaient le pilote out-of-tree `morrownr` ou un kernel plus ancien et préconisaient une compilation DKMS manuelle ; avec le pilote in-kernel du kernel 6.17, ce n'est plus nécessaire.) L'ancien `morrownr/8821au-20210708`, courant autrefois, est désormais passé en legacy (recommandé seulement pour les kernels < 6.13, et son installation met le pilote intégré en blacklist) ; inutile de reprendre cette vieille voie sur un kernel récent. L'avantage en coût d'exploitation est plus concret encore : le pilote in-kernel se met à jour avec le kernel, l'utilisateur n'a pas à maintenir sa propre branche et ne reste pas bloqué à chaque montée de version sur un échec de compilation DKMS, et la même procédure se réutilise sur plusieurs mises à jour du kernel. Le firmware est fourni avec le système par `linux-firmware` ; la mesure locale donne 42.4.0, sans traitement manuel.

Confirmer que la carte est reconnue, que le pilote est lié et que l'interface est créée :

```bash
lsusb | grep -i 0bda:0811
# Bus 003 Device 004: ID 0bda:0811 Realtek Semiconductor Corp. Realtek 8812AU/8821AU 802.11ac WLAN Adapter

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"
cat /sys/class/net/$IF/phy80211/name
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# IF=wlx00c0cabce039 / phy1 / rtw88_8821au
```

La version du firmware se confirme via `dmesg` (mesurée à 42.4.0) :

```bash
sudo dmesg | grep -i 8821au
# rtw88_8821au ... Firmware version 42.4.0, H2C version 0
```

Modes d'interface déclarés (décisifs pour les capacités suivantes) :

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
# IBSS / managed / AP / AP/VLAN / monitor
```

Cette liste affiche `IBSS / managed / AP / AP/VLAN / monitor`. À signaler ici : bien que l'IBSS soit listé, en test après un `ibss join`, `iw link` affiche Not connected — la connexion ne tient pas ; le mesh, l'active-monitor et le P2P ne figurent carrément pas dans la liste (détails en section 4, limites). C'est l'état actuel du matériel et du pilote du RTL8811AU, indépendant du nombre d'antennes.

Couverture des bandes : 2,4 GHz ch1–13 (ch14 disabled) ; 5 GHz ch36–165 (dont ch52–144 marqués radar / DFS). Le regdomain par défaut est `TW`, avec une puissance TX de 30 dBm en 2,4 GHz, 23 dBm en 5 GHz UNII-1/2, 30 dBm en UNII-3.

---

## 3. Capacités mesurées : Monitor / Injection / AP / WPA3

Voici d'abord le tableau récapitulatif des capacités clés, puis le détail point par point. Tous les points ont été réalisés sur notre propre point d'accès YUPITEK et notre propre iPhone 7 Plus.

| Capacité | 2,4 GHz | 5 GHz |
|---|---|---|
| Monitor (écoute en réception) | ✅ forte | ✅ forte |
| Injection (injection de paquets) | ✅ **100 %** (30/30) | ✅ **96 %** (29/30, après déverrouillage reg) |
| Point d'accès (hostapd) | ✅ iPhone connecté + handshake complet | ✅ **stable** (802.11a, 20 MHz testé ; VHT80 non testé) |
| AP WPA3-SAE | Non testé | ✅ iPhone connecté (SAE-only + PMF) |

### 3-1. Monitor (mode monitor, 2,4 GHz + 5 GHz) ✅

Après passage en monitor, une capture de durée fixe a été réalisée sur six canaux : la réception est correcte partout. Les canaux fréquentés atteignent la limite de capture de 300 trames en 6 secondes :

| Canal | Trames capturées |
|---|---|
| ch1 / 2412 | 300 |
| ch6 / 2437 | 300 |
| ch11 / 2462 | 146 |
| ch36 / 5180 | 300 |
| ch149 / 5745 | 141 |
| ch157 / 5785 | 154 |

La réception est stable en 2,4 GHz comme en 5 GHz. Pour une carte nomade mono-antenne, cette performance de réception suffit à un inventaire de canaux sur site et à un diagnostic de paquets. Le faible nombre de trames sur ch11, ch149, ch157 vient du trafic radio momentanément faible sur ces canaux, pas d'un défaut de réception ; les canaux fréquentés ch1, ch6, ch36 atteignent la limite de 300 trames en 6 secondes — la réception n'est manifestement pas son goulot d'étranglement.

### 3-2. Injection (injection de paquets) ✅

Test d'injection dirigée avec `aireplay-ng --test` sur notre propre AP YUPITEK. En 2,4 GHz, 100 % (30/30, `Injection is working!`) ; en 5 GHz, 96 % (29/30). Un détail de configuration en 5 GHz : le `reg=TW` par défaut verrouille la transmission active sur une partie des bandes UNII ; avant le test, déverrouillez via `sudo iw reg set US`, puis remettez `sudo iw reg set TW` après le test.

```bash
# 2,4 GHz (YUPITEK est en réalité sur ch5 / 2432)
sudo iw dev $IF set freq 2432
sudo aireplay-ng --test --ignore-negative-one -a <YUPITEK-BSSID> $IF
# Injection is working!  30/30: 100%  Power: -60.00
```

Qu'une carte mono-antenne atteigne 100 % en 2,4 GHz et 96 % en 5 GHz constitue déjà une capacité d'injection très fiable, et c'est ce qui lui permet de réaliser ensuite la capture de handshake de bout en bout.

### 3-3. Point d'accès (2,4 GHz / 5 GHz) ✅

Avec `hostapd`, la carte devient une station de base ; les trois configurations permettent à l'iPhone 7 Plus de se connecter et de compléter le 4-way handshake (`EAPOL-4WAY-HS-COMPLETED`) :

- **5 GHz (802.11a, 20 MHz testé ; VHT80 non testé)** : la configuration la plus stable, iPhone connecté, handshake complet, fermeture propre en `AP-DISABLED`.
- **2,4 GHz (WPA2-PSK)** : iPhone connecté, handshake complet, fermeture propre après déconnexion. Une observation honnête : lors d'un cycle précédent, avec la même configuration, un `key not allowed / Failed to set beacon parameters` était apparu après la déconnexion du STA et avait interrompu le service, mais le retest n'a pas pu le reproduire ; nous l'imputons à un re-key de beacon occasionnel du rtw88_8821au, pas à un défaut systématique. Pour des scénarios de reconnexions longues et fréquentes, restez vigilant, ou passez simplement à un AP 5 GHz.
- **WPA3-SAE (5 GHz, PMF obligatoire ; 2,4 GHz non testé)** : les réglages clés sont `wpa_key_mgmt=SAE` (WPA3 pur, sans fallback WPA2), `ieee80211w=2` (Management Frame Protection obligatoire), `sae_pwe=0` (compatibilité avec les anciens terminaux). L'iPhone 7 Plus (iOS 15) se connecte en SAE avec succès. L'AP n'ouvre que le SAE, sans repli WPA2 : réussir l'association prouve donc que le handshake d'authentification SAE tient. Le WPA3-SAE côté AP avec RTL8811AU + rtw88_8821au est utilisable.

---

## 4. Capacité de handshake de bout en bout et limites

### 4-1. Capture de handshake de bout en bout ✅

C'est le test intégré qui vérifie si l'injection et la capture « se chaînent » réellement, mené de bout en bout sur notre propre AP YUPITEK et notre propre iPhone 7 Plus, dans un cadre autorisé. Le flux : monitor sur le canal cible → envoi d'un deauth dirigé vers notre propre appareil pour déclencher la reconnexion → capture du 4-way complet (M1–M4) → export du `.22000` lisible par hashcat via `hcxpcapngtool --all`.

Résultat mesuré : `aircrack-ng` retient 1 handshake sur YUPITEK, les quatre messages EAPOL M1–M4 sont tous présents, le client est un OUI Apple (`b8:53:ac`, confirmé comme étant l'iPhone 7 Plus), et le `.22000` exporté s'injecte directement dans hashcat. L'AWUS036ACS dispose donc d'une capacité complète de capture de handshake de bout en bout.

Deux points pratiques méritent d'être notés (configuration pas à pas détaillée dans un article dédié) :

1. **Quand plusieurs AP homonymes partagent le même canal au bureau, ne verrouillez pas une seule station avec `--bssid`** ; capturez tout le canal pour ne pas manquer l'appareil connecté à une autre.
2. `hcxpcapngtool` est assez strict par défaut et peut renvoyer « not enough M1 » ; ajoutez `--all` pour exporter le `.22000` depuis les M1–M4 complets.

Les outils Kali courants de cette chaîne de capture de handshake (aircrack-ng, hcxtools) s'exécutent directement sous Ubuntu 24.04 ARM64 ; airodump-ng, aireplay-ng et hcxpcapngtool fonctionnent tous normalement.

### 4-2. VIF (interfaces virtuelles) ✅

`iw dev $IF interface add mon9 type monitor` crée une VIF monitor qui capture 100 frames ; un script créant par ailleurs « interface principale connectée à YUPITEK en STA + une VIF AP » montre qu'une puce unique peut jouer simultanément les rôles de STA et d'AP.

### 4-3. Limites honnêtes (remontées mesurées)

| Mode / outil avancé | État | Mesure |
|---|---|---|
| Active monitor | ❌ non pris en charge | `iw set monitor active` → `Operation not supported (-95)` |
| Ad-hoc (IBSS) | ❌ non pris en charge | Mode listé mais `iw link` = Not connected après `ibss join` |
| Mesh (802.11s) | ❌ non pris en charge | `set type mp` → `-95` |
| Wi-Fi Direct (P2P) | ❌ non pris en charge | `interface add type __p2pcl` → `-95` |
| hcxdumptool 8.x | ⚠️ impossible à armer | `failed to arm interface` : rtw88_8821au ne fournit pas l'active-monitor ; utilisez airodump-ng + aireplay-ng |

Deux autres limites d'exploitation à connaître. Le flux unique 1x1 fixe son plafond théorique (HT Max RX 150 Mbps, VHT80 ~ 433 Mbps) : le débit n'est de toute façon pas son point fort. Après des bascules répétées entre monitor / AP, le RX est parfois brièvement dégradé (plus rien n'est détecté) ; un débranchement/rebranchement physique de la carte y remédie, et le nom d'interface, déterminé par la MAC, reste inchangé.

---

## 5. Cas d'usage et choix de modèle (nomade léger, retour vers le Hub)

En rapportant ces capacités au positionnement produit, le rôle de l'AWUS036ACS est clair : une carte nomade aux capacités complètes mais axée sur la légèreté. À quels scénarios la destiner ?

- **Inventaire rapide sur site / diagnostic nomade** : mono-antenne, compacte, basse consommation, adaptée à l'inventaire de canaux, à la ronde de signal et au diagnostic de paquets en déplacement. Associée à une plateforme centrale comme le GX10, la carte nomade capture sur site et renvoie les données au Hub pour une analyse centralisée : répartition des rôles claire.
- **Enseignement et validation** : elle couvre toute la ligne principale Monitor / Injection / AP / WPA3-SAE / handshake de bout en bout, idéale comme carte de démonstration et de validation dans un cadre autorisé.
- **Scénarios inadaptés** : besoin de débit maximal, de la plus grande portée, ou de mesh / IBSS / P2P / active-monitor — ce n'est pas le bon choix.

Léger ne signifie pas amputé. Aucune capacité de la ligne principale ne manque ; ce qui est sacrifié, c'est le plafond de débit et les modes d'interface avancés. Le choix dépend donc de ce que vous voulez : « l'emporter partout » ou « saturer le débit ».

Par rapport à la même famille, les différences de positionnement sont les suivantes :

| Besoin | Carte conseillée | Raison |
|---|---|---|
| Nomade léger + ligne principale complète | **AWUS036ACS** | Injection 2,4G 100 %, 5G 96 %, handshake de bout en bout disponible, mono-antenne légère |
| Injection bi-bande à 100 % / validation d'intrusion plus robuste | AWUS036EACS, AWUS036ACH | Injection 100 % sur les deux bandes, l'EACS intègre en plus le BT |
| Meilleure réception / monitor longue portée | AWUS036AXER, AWUS036ACH | Saut de fréquence captant plus de cibles / fort gain bi-antenne |
| Expérimentation mesh / IBSS en local | AWUS036ACM, AWUS036ACHM | Le pilote mt76 crée en local (le Realtek rtw88 ne le fait pas) |

Le choix en une phrase : pour la légèreté avec une ligne principale complète, l'AWUS036ACS est le bon choix nomade ; pour une injection bi-bande à 100 % ou une validation d'intrusion plus lourde, orientez-vous vers l'EACS / ACH.

---

## Questions fréquentes (FAQ)

**Q : L'AWUS036ACS nécessite-t-elle l'installation d'un pilote sous Ubuntu 24.04 ARM64 ?**
Sur le kernel 6.17 testé ici (ASUS GX10), non : le RTL8811AU est pris en charge par le pilote intégré rtw88_8821au, reconnu dès le branchement, sans compilation ni DKMS. Sur un kernel plus ancien, vérifiez d'abord la présence du module avec `modinfo rtw88_8821au`.

**Q : L'AWUS036ACS prend-elle en charge le mode monitor et l'injection de paquets ?**
Oui. Le monitor fonctionne en 2,4 GHz comme en 5 GHz ; au test `aireplay-ng --test`, l'injection est de 100 % en 2,4G (30/30) et de 96 % en 5G (29/30, après avoir levé la restriction TW via `iw reg set US`). L'active monitor n'est pas pris en charge.

**Q : L'AWUS036ACS peut-elle capturer un handshake WPA et l'exporter en hashcat .22000 ?**
Oui. Test de bout en bout sur notre propre AP et notre propre iPhone 7 Plus : deauth dirigé pour déclencher la reconnexion, capture du 4-way complet (M1–M4), puis export en .22000 via `hcxpcapngtool --all`. Uniquement sur des réseaux dont vous êtes propriétaire ou autorisé.

**Q : L'AWUS036ACS peut-elle servir de point d'accès ? Prend-elle en charge le WPA3 ?**
Oui. `hostapd` ouvre un point d'accès en 2,4G et en 5G (5G testé en 802.11a à 20 MHz ; VHT80 non testé), l'iPhone 7 Plus se connecte et complète le 4-way ; le WPA3-SAE en 5G (SAE-only, ieee80211w=2, sae_pwe=0) se connecte aussi avec succès (WPA3 en 2,4G non testé).

**Q : Quels modes l'AWUS036ACS ne prend-elle pas en charge ? hcxdumptool fonctionne-t-il ?**
Elle ne prend pas en charge l'active monitor, l'IBSS, le mesh (802.11s) ni le Wi-Fi Direct (P2P). hcxdumptool 8.x échoue en failed to arm interface ; utilisez airodump-ng + aireplay-ng. Pour le mesh / IBSS, choisissez l'AWUS036ACM / ACHM.

---

## 6. Pour aller plus loin

- Comparaison complète des capacités et évaluation globale des neuf cartes ALFA → [Hub d'évaluation des cartes Wi-Fi ALFA (tableau récapitulatif)](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Sans installation de pilote : activer Monitor / AP sous Ubuntu 24.04 + kernel 6.17 (tests rtw88 / rtw89 / mt76)](/fr/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- [Tutoriel pas à pas WPA3-SAE et capture de handshake de bout en bout](/fr/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Carte composite BT+WiFi de la même famille → [Test carte par carte de l'AWUS036EACS](/fr/blog/awus036eacs-asus-gx10-ubuntu-test-report/)

---

*Unité de test : Yopitek (distributeur ALFA Network à Taïwan) — https://www.yupitek.com | Environnement de test : ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Appareil de test : Apple iPhone 7 Plus*
