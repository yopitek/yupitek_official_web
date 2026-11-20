---
title: "Test de l'AWUS036AXML : la carte composite Wi-Fi 6 + Bluetooth sur ASUS GX10 (ARM64 / Ubuntu 24.04) — un rapport honnête : AP stable, injection en échec"
slug: awus036axml-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axml-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036axml-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axml
  - mt7921
  - mt7921u
  - wifi-6
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - ap-mode
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036AXML (Wi-Fi + Bluetooth) testée sur ASUS GX10 / Ubuntu 24.04 ARM64 : AP, WPA3 et monitor disponibles, mais l'injection échoue et la capture de handshake est impossible ; déconseillée pour le test d'intrusion."
faq:
  - question: "L'AWUS036AXML peut-elle faire de l'injection de paquets (packet injection) ?"
    answer: "Sur notre plateforme de test (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia), non. aireplay-ng --test renvoie No Answer, Found 0 APs ; le test par cible sur un AP désigné ne donne que No such BSSID available. Même si un balayage ordinaire voit cet AP (environ -54 dBm), en situation d'outil d'injection la carte ne reçoit pas son beacon, donc le deauth et la capture de handshake (0 capturé) sont inutilisables. La cause racine est la régression du chanctx de mac80211 à partir du kernel 6.16, et non une incapacité intrinsèque de la puce à injecter ; l'AWUS036AXM donne le même résultat. Pour de l'injection, choisissez l'AWUS036EACS, l'ACH ou l'ACS."
  - question: "Le Bluetooth de l'AWUS036AXML fonctionne-t-il sous Ubuntu ?"
    answer: "Le Bluetooth est utilisable en test machine : avec bluetoothctl / hciconfig, le contrôleur hci est UP, il détecte des appareils BLE et Bluetooth classiques, et le Wi-Fi et le Bluetooth fonctionnent simultanément (coexistence). C'est un dispositif composite Wi-Fi + Bluetooth ; rappel : au rebranchement, la probe WiFi se bloque parfois sans créer d'interface wlx, il suffit de rebrancher sur un autre port USB pour récupérer."
  - question: "L'AWUS036AXML nécessite-t-elle l'installation d'un pilote sous Ubuntu 24.04 ?"
    answer: "Non. Le pilote mt7921u est intégré au kernel 6.17 ; après branchement, dmesg montre mt7921u renommer l'interface en wlx + MAC (USB ID 0e8d:7961), sans DKMS ni compilation. Le pilote ne fournit pas les modes IBSS ni mesh."
  - question: "L'AWUS036AXML peut-elle ouvrir un AP et prend-elle en charge le WPA3 ?"
    answer: "Oui, c'est son usage le plus stable. En 2,4 GHz (802.11n, MCS 10) et en 5 GHz VHT80 (VHT-NSS2), l'iPhone se connecte et est authorized ; le WPA3-SAE avec sae_pwe=0 connecte l'iPhone 15 Pro (MFP: yes ; testé en 2,4 GHz et 6 GHz, pas en 5 GHz) ; en STA+AP parallèle, le ping côté STA est d'environ 4,4 ms. Bien que positionnée comme puce Wi-Fi 6, sa bande 6 GHz s'est révélée utilisable en test machine (AP maison à 6135 MHz, iPhone 15 Pro connecté en 802.11ax avec obtention d'une IP)."
  - question: "Quelle différence entre l'AWUS036AXML et l'AWUS036AXM, et laquelle choisir ?"
    answer: "Sur cette plateforme, le comportement Wi-Fi des deux est identique : même mt7921u, injection également en échec, réception monitor également faible, AP, WPA3 et VIF également disponibles. La différence est que l'AXML a un Bluetooth (utilisable en test machine) et une bande 6 GHz utilisable en test machine, alors que le Bluetooth et le 6 GHz de l'AXM n'ont pas été testés séparément ce cycle. Pour un pur AP ou une connexion ordinaire, n'importe laquelle convient ; pour l'injection ou le handshake, aucune des deux ne convient."
draft: false
---

{{< tldr >}}L'AWUS036AXML offre AP, WPA3, VIF et monitor passif utilisables sur ASUS GX10 / Ubuntu 24.04 ARM64, le Bluetooth et la bande 6 GHz étant aussi utilisables en test machine, mais l'injection échoue en test (No Answer / Found 0 APs), interdisant le deauth et la capture de handshake ; déconseillée pour le test d'intrusion ; positionnée pour le simple AP et la connexion ordinaire.{{< /tldr >}}

L'ALFA AWUS036AXML est le seul modèle composite « MediaTek Wi-Fi 6 + Bluetooth » de ce lot de 9 cartes. Elle partage la génération de puce (MT7921, pilote `mt7921u`) de l'AWUS036AXM sans Bluetooth, la différence étant un jeu Bluetooth en plus. Les clients posent le plus souvent les trois mêmes questions : peut-elle passer en monitor ? peut-elle injecter ? peut-elle monter un AP ? Cet article isole l'AWUS036AXML pour la tester point par point sur ASUS GX10 (ARM64) sous Ubuntu 24.04, et dire clairement ce qu'elle peut et ne peut pas faire, en particulier la limite la plus décisive : **l'injection échoue sur cette plateforme**.

Précisons d'abord le positionnement : toutes les mesures ci-dessous sont réalisées sur les propres équipements de Yopitek, son propre Wi-Fi de bureau (SSID `YUPITEK`), à destination de nos propres téléphones de test (iPhone 7 Plus, WPA3 aussi revérifié sur iPhone 15 Pro). C'est une vérification matérielle, par le distributeur, de la compatibilité et des limites de capacités du produit, pas un tutoriel d'opérations visant un réseau tiers. Les autotests de monitor, AP et injection du texte sont tous réalisés en environnement fermé en propre, à destination de nos propres appareils.

## 1. Cette carte et la plateforme de test

- **Plateforme de calcul** : ASUS GX10 (ARM64 / aarch64)
- **Système d'exploitation** : Ubuntu 24.04 LTS
- **Version du kernel** : kernel 6.17.0-1014-nvidia
- **Carte testée** : ALFA AWUS036AXML (MediaTek MT7921AUN, Wi-Fi 6 / 2x2 / +BT)
- **Appareil de test** : Apple iPhone 7 Plus (WPA3-SAE aussi revérifié sur iPhone 15 Pro)
- **Environnement de test** : Wi-Fi de bureau en propre, SSID `YUPITEK`, 2,4 GHz ch5 / 5 GHz ch36, ch157
- **Période de test** : mesures sur machine réelle du 2026-11-16 au 2026-11-18

Tous les résultats sont consignés sous forme de chiffres ou d'états réellement mesurés, sans extrapolation de fiche technique ; les adresses MAC sont masquées par `xx` dans les sorties.

## 2. Matériel et pilote : MT7921AUN, prêt à l'emploi

| Élément | Spécification |
|---|---|
| Modèle | AWUS036AXML |
| Puce | MediaTek MT7921AUN |
| USB ID | `0e8d:7961` (MediaTek Inc. Wireless_Device) |
| Pilote in-kernel | `mt7921u` |
| Génération / flux | Wi-Fi 6 / 2x2 (2T2R) |
| Bluetooth | Oui (dispositif composite BT + WiFi ; en test machine, contrôleur hci UP, détection d'appareils BLE et Bluetooth classiques, coexistence WiFi+BT) |
| Énumération USB | USB 3 |
| Nommage d'interface | `wlx<MAC>` (ex. : `wlx00c0cabd65b9`) |

La reconnaissance est directe : après branchement, `lsusb` affiche l'USB ID MediaTek, et `dmesg` montre `mt7921u` chargé renommant l'interface :

```bash
lsusb | grep 0e8d:7961
# Bus 004 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device

sudo dmesg | grep mt7921u | tail -1
# mt7921u 4-1:1.3 wlx00c0cabd65b9: renamed from wlan0
```

Deux points clés. D'abord, sans compilation : l'AWUS036AXML utilise le pilote `mt7921u` intégré au kernel 6.17, reconnue dès le branchement, sans avoir à gérer de module DKMS out-of-tree sur aarch64 — particulièrement pratique en ARM64. Ensuite, elle s'énumère en USB 3 (le câble OTG de certains modèles de génération précédente n'était qu'en USB 2.0), la bande passante de transfert n'est donc pas un goulot d'étranglement.

Un point souvent mal compris : l'AWUS036AXML est positionnée comme puce Wi-Fi 6 (pas 6E), mais **sa bande 6 GHz s'est révélée utilisable en test machine** — nous avons monté un AP maison à 6135 MHz, et l'iPhone 15 Pro s'y est connecté en 802.11ax avec obtention d'une IP. Le Bluetooth est également utilisable en test : `hciconfig` / `bluetoothctl` montrent le contrôleur hci en état UP, détectant des appareils BLE et Bluetooth classiques, le Wi-Fi et le Bluetooth fonctionnant simultanément (coexistence).

Vérifions aussi les modes d'interface pris en charge : un détail utile au choix apparaît, à savoir l'absence d'IBSS et de mesh point :

```bash
iw phy <phyN> info | sed -n '/Supported interface modes/,/Band 1/p'
```
```
Supported interface modes:
    * managed
    * AP
    * AP/VLAN
    * monitor
    * P2P-client / P2P-GO / P2P-device
```

Autrement dit, managed, AP, monitor, P2P sont présents, mais les deux modes ad-hoc (IBSS) et mesh 802.11s ne sont tout simplement pas fournis par le pilote `mt7921u`. Les clients souhaitant expérimenter le mesh / IBSS écartent directement cette carte (voyez les `mt76` ACM / ACHM).

## 3. Capacités mesurées : Monitor / AP / WPA3, et la limite honnête de l'injection

Les capacités centrales d'un coup :

| Capacité | 2,4GHz | 5GHz | Commentaire |
|---|---|---|---|
| Monitor | ✅ (faible) | ✅ (faible) | Écoute de beacons possible ; paquets client / data souvent manqués |
| **Injection** | ❌ **échec** | ❌ **échec** | `aireplay-ng` injection / deauth non fonctionnel ; cause racine : régression du chanctx de mac80211 à partir du kernel 6.16 (pas intrinsèque à la puce) |
| AP (point d'accès) | ✅ avec 802.11n | ✅ VHT80 (80MHz) | iPhone 7 Plus connecté, `authorized: yes` |
| WPA3-SAE | ✅ | Non testé | iPhone 15 Pro connecté, `MFP: yes` (`sae_pwe=0`) ; aussi testé en 6 GHz (ch37, 6135 MHz) |

### Monitor : les deux bandes passent, mais la réception est faible

L'AWUS036AXML passe en mode monitor en 2,4 GHz (ch1 / 6 / 11) comme en 5 GHz (ch36 / 149 / 157), l'écoute de beacons se fait sans problème. Le flux de configuration est le `iw dev` standard en quatre étapes :

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36     # en 2,4GHz, utilisez set channel 6
```

Une remarque honnête : sa réception en monitor est nettement plus faible que celle du MT7612U (ACM) du même lot ou de l'AXER Wi-Fi 6. Les beacons sont captés, mais les paquets client / data sont souvent manqués ; avec un balayage en saut de fréquence via `airodump-ng`, certains AP sont facilement ratés. En pratique, mieux vaut se verrouiller sur un seul canal (`-c <ch>`) plutôt que sauter de fréquence, pour des résultats plus stables. Par ailleurs, en mode monitor, `iw info` rapporte un txpower de seulement 3 dBm, un **artefact de rapport** (le TX matériel réel est d'environ 20–23 dBm, vérifié via `txpower_sku`), et non une puissance réellement bridée à 3 dBm — point repris dans les « précautions » plus loin.

### AP : 2,4 GHz avec HT, le 5 GHz monte en VHT80

L'AP est le domaine le plus stable de l'AWUS036AXML. En 2,4 GHz, on peut conserver directement le 802.11n (HT), sans avoir à le désactiver comme sur l'ACHM mono-antenne ; en 5 GHz, elle monte jusqu'à VHT 80 MHz. Sur les deux bandes, l'iPhone 7 Plus se connecte, `authorized: yes`.

Configuration clé hostapd du VHT80 5 GHz :

```
hw_mode=a
channel=36
ieee80211ac=1
ht_capab=[HT40+][SHORT-GI-20][SHORT-GI-40]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42
vht_capab=[SHORT-GI-80]
```

En test, la connexion est en VHT-NSS2, 80 MHz. Pour la version 2,4 GHz, passez `hw_mode` à `g`, `channel=6`, conservez `ieee80211n=1` et `ht_capab=[HT20]` ; l'iPhone se connecte en MCS 10 (802.11n).

### WPA3-SAE : disponible, pensez à sae_pwe=0

En passant le `wpa_key_mgmt` de l'AP à `SAE`, avec `ieee80211w=2` et `sae_pwe=0`, le WPA3-SAE s'ouvre. En test, l'iPhone 15 Pro se connecte en 2,4 GHz (et en 6 GHz ; 5 GHz non testé), `authorized: yes`, `MFP: yes`. Le `sae_pwe=0` sert à la compatibilité avec les anciens iPhone, même piège que sur l'ACHM : avec `sae_pwe=2`, les anciens modèles ne se connectent souvent pas.

### VIF : naviguer et servir de point d'accès en même temps, viable

L'AWUS036AXML prend en charge la coexistence de plusieurs interfaces. Créez une VIF AP (MAC différente, unmanaged), gardez l'interface principale connectée au Wi-Fi, ouvrez l'AP sur le même canal : en test, pendant que l'iPhone 7 Plus est connecté à la VIF AP, le ping du côté STA vers `YUPITEK` est de 4,4 ms. Pour le besoin « une carte qui navigue + partage un point d'accès en même temps », c'est établi.

### Limite honnête : l'injection échoue sur cette plateforme

C'est la ligne la plus importante à clarifier pour l'AWUS036AXML (et son jumeau sans Bluetooth, l'AXM). Sur ASUS GX10 + kernel 6.17, nous avons fait un autotest d'injection sur notre propre environnement : échec.

```bash
sudo aireplay-ng --test $IF
```
```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

Même en ciblant le BSSID de notre propre AP, le test par cible ne renvoie que `No such BSSID available`. Le point clé : un balayage ordinaire voit pourtant cet AP (signal -54 dBm), mais dès qu'on entre dans la situation d'un outil d'injection, cette carte « n'entend » plus le beacon de la cible, le deauth ne part pas, et le nombre de 4-way handshakes capturés est de 0.

Ce n'est pas un réglage mal fait ni une panne de carte isolée. La vraie cause racine est **au niveau logiciel** : après le kernel 6.16, le channel context (chanctx) de mac80211 a connu une régression qui empêche le pilote stock de recevoir les beacons cibles en situation d'injection, `aireplay-ng` conclut donc `No Answer` — et ce **n'est pas une incapacité intrinsèque de la puce MT7921 à injecter**. Le phénomène est consigné dans morrownr/USB-WiFi issue #387, l'analyse de cause racine dans morrownr/mt76 issue #18. Des tests communautaires indiquent qu'un pilote git / patché sur le même modèle peut faire fonctionner l'active monitor avec injection, mais le firmware MT7921 verrouille toujours l'injection sur les débits de base de 1 Mbps / 6 Mbps, sans injection HT / VHT ; l'AXM et l'AXML sont toutes deux touchées sur le **stock kernel 6.17**, sans correction possible par réglage au 2026-11-18.

Ainsi, toute capacité impliquant l'injection — deauth, capture de handshake WPA, test d'intrusion fondé sur l'injection — est impossible pour l'AWUS036AXML sur cette plateforme. Pour ces usages, utilisez un modèle à injection validée en test (voir le choix ci-dessous).

### Vue d'ensemble des autres modes avancés

| Fonction avancée | État | Commentaire |
|---|---|---|
| VIF (STA + AP coexistants) | ✅ | Même canal ch36 ; ping STA 4,4 ms à la connexion iPhone |
| Capture de handshake WPA | ❌ | Injection en échec → deauth ne part pas, handshake 0 |
| Active monitor | 🟡 | `set monitor active` accepté, ACK non vérifié |
| Ad-hoc (IBSS) | N/A | Mode absent du pilote `mt7921u` |
| Mesh (802.11s) | N/A | Mode absent du pilote `mt7921u` |
| Wi-Fi Direct (P2P) | ⬜ | Déclaré pris en charge par le pilote, nécessite un second équipement, passé |

## 4. Précautions du composite Bluetooth et usages adaptés / inadaptés

### Effet secondaire pratique de la carte composite BT + WiFi

L'AWUS036AXML intègre un Bluetooth : c'est l'un des deux dispositifs composites de ce lot (l'autre étant l'EACS de Realtek). Le Bluetooth est déjà vérifié utilisable en test machine (contrôleur hci UP, détection d'appareils BLE et Bluetooth classiques, coexistence avec le Wi-Fi, voir plus haut) ; ajoutons ici un effet secondaire pratique du dispositif composite : au rebranchement, la probe WiFi se bloque parfois sans créer d'interface `wlx`, symptôme où, après débranchement/rebranchement, `ls /sys/class/net` n'affiche pas la carte. La solution est simple : **changez de port USB** et rebranchez, l'énumération se fait alors normalement.

Un autre petit geste à retenir : en mode AP, si le téléphone ne détecte soudain plus votre SSID, réinitialisez en **débranchant/rebranchant** la carte une fois, sans changer la configuration. (Rappel : le 3 dBm rapporté en monitor évoqué plus haut est un artefact, pas la puissance réelle, et n'est pas la cause de la disparition du SSID.)

### Règles de sécurité de la plateforme

- N'exécutez jamais `airmon-ng check kill` : il arrête NetworkManager et déconnecte tout le GX10. Opérez uniquement sur l'interface externe `wlx*`, sans toucher à la ligne principale d'accès Internet intégrée.
- `hcxdumptool 8.x` échoue en `failed to arm` sur cette machine (sauf l'AWUS036EACS en 2,4 GHz ; conflit d'énumération de la carte intégrée tri-bande du GX10 + absence d'active-monitor dans le pilote) : c'est un défaut commun à toute la plateforme, sans rapport avec l'AXML ; pour une fonction similaire, utilisez `airodump-ng` avec d'autres outils aircrack-ng.
- Complément ARM64 : `aircrack-ng` doit être compilé depuis les sources, et `wifite` est conseillé en version git pour contourner le conflit de dépendances apt.

### Vue d'ensemble adapté / inadapté

| Scénario adapté | Scénario inadapté |
|---|---|
| Pur AP / point d'accès (2,4G avec HT, 5G VHT80) | injection / deauth |
| Point d'accès WPA3-SAE | Capture de handshake WPA |
| Connexion managed ordinaire | Carte principale de test d'intrusion fondé sur l'injection |
| Monitor passif / inventaire spectral (verrouillé sur un seul canal) | Expérimentation mesh / IBSS |
| STA + AP coexistants (VIF, naviguer et partager en même temps) | Écoute longue portée nécessitant une forte réception |

## 5. Conseils de choix (retour au tableau récapitulatif)

Replacée dans la vue d'ensemble des 9 cartes, l'AWUS036AXML a un positionnement clair : MediaTek stable en connexion, sans compilation, les deux bandes montant en VHT80 en AP — une carte compétente « pure connexion / pur AP » ; dès que l'injection entre en jeu, ce n'est plus son terrain.

| Besoin | Modèle conseillé |
|---|---|
| Pur AP / connexion ordinaire (sans injection) | **AWUS036AXML / AWUS036AXM** (cette carte convient) |
| injection + handshake (test d'intrusion) | AWUS036EACS / AWUS036ACH / AWUS036ACS |
| Expérimentation mesh / IBSS | AWUS036ACM / AWUS036ACHM |
| Meilleure réception / monitor longue portée | AWUS036AXER / AWUS036ACH |

Si vous arbitrez entre les 9 cartes, pour la matrice complète Monitor / Injection / AP / WPA3 et le choix par usage, voyez le tableau récapitulatif :

- [Le test le plus complet de 2026 : la matrice complète des 9 cartes Wi-Fi ALFA sur ASUS GX10](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

Un piège à éviter en une phrase : **pour l'injection ou le handshake, ne choisissez pas l'AWUS036AXML / AWUS036AXM** ; pour la pure connexion ou le montage d'un point d'accès, elle est très utile.

## Questions fréquentes (FAQ)

**Q1. L'AWUS036AXML peut-elle faire de l'injection de paquets (packet injection) ?**
Sur notre plateforme de test (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia), non. `aireplay-ng --test` renvoie `No Answer`, `Found 0 APs` ; le test par cible sur un AP désigné ne donne que `No such BSSID available`. Même si un balayage ordinaire voit cet AP (environ -54 dBm), en situation d'outil d'injection la carte ne reçoit pas son beacon, donc le deauth et la capture de handshake (0 capturé) sont inutilisables. La cause racine est la régression du chanctx de mac80211 à partir du kernel 6.16, et non une incapacité intrinsèque de la puce à injecter ; l'AWUS036AXM donne le même résultat. Pour de l'injection, choisissez l'AWUS036EACS, l'ACH ou l'ACS.

**Q2. Le Bluetooth de l'AWUS036AXML fonctionne-t-il sous Ubuntu ?**
Le Bluetooth est utilisable en test machine : avec `bluetoothctl` / `hciconfig`, le contrôleur hci est UP, il détecte des appareils BLE et Bluetooth classiques, et le Wi-Fi et le Bluetooth fonctionnent simultanément (coexistence). C'est un dispositif composite Wi-Fi + Bluetooth ; rappel : au rebranchement, la probe WiFi se bloque parfois sans créer d'interface `wlx`, il suffit de rebrancher sur un autre port USB pour récupérer.

**Q3. L'AWUS036AXML nécessite-t-elle l'installation d'un pilote sous Ubuntu 24.04 ?**
Non. Le pilote mt7921u est intégré au kernel 6.17 ; après branchement, dmesg montre mt7921u renommer l'interface en `wlx` + MAC (USB ID `0e8d:7961`), sans DKMS ni compilation. Le pilote ne fournit pas les modes IBSS ni mesh.

**Q4. L'AWUS036AXML peut-elle ouvrir un AP et prend-elle en charge le WPA3 ?**
Oui, c'est son usage le plus stable. En 2,4 GHz (802.11n, MCS 10) et en 5 GHz VHT80 (VHT-NSS2), l'iPhone se connecte et est authorized ; le WPA3-SAE avec `sae_pwe=0` connecte l'iPhone 15 Pro (`MFP: yes` ; testé en 2,4 GHz et 6 GHz, pas en 5 GHz) ; en STA+AP parallèle, le ping côté STA est d'environ 4,4 ms. Bien que positionnée comme puce Wi-Fi 6, sa bande 6 GHz s'est révélée utilisable en test machine (AP maison à 6135 MHz, iPhone 15 Pro connecté en 802.11ax avec obtention d'une IP).

**Q5. Quelle différence entre l'AWUS036AXML et l'AWUS036AXM, et laquelle choisir ?**
Sur cette plateforme, le comportement Wi-Fi des deux est identique : même mt7921u, injection également en échec, réception monitor également faible, AP, WPA3 et VIF également disponibles. La différence est que l'AXML a un Bluetooth (utilisable en test machine) et une bande 6 GHz utilisable en test machine, alors que le Bluetooth et le 6 GHz de l'AXM n'ont pas été testés séparément ce cycle. Pour un pur AP ou une connexion ordinaire, n'importe laquelle convient ; pour l'injection ou le handshake, aucune des deux ne convient.

## Pour aller plus loin

(Liens mis en ligne progressivement, en construction)

- Version sans Bluetooth à même puce : [Test individuel de l'AWUS036AXM](/fr/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- Alternatives à injection disponible : [Test individuel de l'AWUS036EACS](/fr/blog/awus036eacs-asus-gx10-ubuntu-test-report/), [Test individuel de l'AWUS036ACH](/fr/blog/awus036ach-asus-gx10-ubuntu-test-report/), [Test individuel de l'AWUS036ACS](/fr/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- Article thématique : [Sans installation de pilote : activer les modes Monitor et AP sous Ubuntu (ARM64)](/fr/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- Article thématique : [Connexion WPA3-SAE et pratique du handshake (vérifié en environnement propre)](/fr/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Tableau Hub : [La matrice complète des 9 cartes ALFA sur ASUS GX10](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

---

*Unité de test : Yopitek (distributeur ALFA Network à Taïwan) | Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Appareil de test : Apple iPhone 7 Plus (WPA3 aussi testé sur iPhone 15 Pro) | Environnement de test : Wi-Fi de bureau en propre (SSID YUPITEK). Cet article est une vérification de compatibilité produit et de capacités, pas un tutoriel d'opérations visant un réseau tiers.*
