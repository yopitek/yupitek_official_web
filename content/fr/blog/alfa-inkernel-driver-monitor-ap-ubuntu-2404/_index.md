---
title: "Sans installation de pilote : activer les modes Monitor et AP des cartes ALFA avec le pilote in-kernel sous Ubuntu 24.04 + kernel 6.17 (tests rtw88 / rtw89 / mt76)"
slug: alfa-inkernel-driver-monitor-ap-ubuntu-2404
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404.webp"
bannerimage: "/images/blog/banner/alfa-inkernel-driver-monitor-ap-ubuntu-2404.webp"
author: "benny-lai"
tags:
  - alfa-network
  - ubuntu-24-04
  - kernel-6-17
  - in-kernel-driver
  - rtw88
  - rtw89
  - mt76
  - monitor-mode
  - hostapd
  - ap-mode
  - linux-wifi
description: "Tutoriel sans installation de pilote sous Ubuntu 24.04 / kernel 6.17 : activer les modes Monitor et AP des cartes ALFA avec les pilotes in-kernel rtw88 / rtw89 / mt76, avec les réglages de compatibilité des points d'accès WPA3 et les précautions pour la chaîne d'outils Kali."
faq:
  - question: "Comment faire passer une carte ALFA en mode monitor sous Ubuntu 24.04 ?"
    answer: "À partir du kernel 6.17, il suffit de rendre l'interface hors de la gestion de NetworkManager et de la basculer en mode interface monitor, sans installer de pilote tiers ; le flux est identique pour les trois familles de pilotes rtw88 / rtw89 / mt76 testées dans cet article, voir les étapes détaillées du texte."
  - question: "Pourquoi n'a-t-on pas besoin d'installer un pilote pour une carte ALFA sous Ubuntu ?"
    answer: "Parce que les Realtek rtw88 / rtw89 et le MediaTek mt76 ont progressivement intégré ces puces USB au support in-kernel du kernel mainline (version minimale variable selon la carte, de 4.19 à 6.17 ; sous Ubuntu 24.04, les AX et AXER nécessitent un kernel 6.17 ou plus, par exemple le HWE de 24.04.4) ; avec le kernel 6.17 (testé sur le GX10), les 9 cartes de cet article sont intégrées, reconnues dès le branchement, sans compilation ni DKMS."
  - question: "Que faire si l'ancien iPhone ne se connecte pas au point d'accès WPA3 monté avec une carte ALFA ?"
    answer: "Le test révèle deux causes fréquentes : d'abord, le sae_pwe de hostapd doit être réglé à 0 et non à 2 pour être compatible avec les anciens iPhone ; ensuite, conserver le réglage 802.11n peut faire échouer l'association des anciens appareils — en priorité à la compatibilité, il est conseillé de désactiver le 802.11n."
  - question: "Laquelle des familles de pilotes rtw88, rtw89, mt76 prend en charge le mesh ou l'IBSS ?"
    answer: "En test, la famille mt76 (comme les AWUS036ACM / ACHM) crée en local le mesh (802.11s) et l'IBSS ; le Realtek rtw88 peut faire un join IBSS en local (confirmé sur l'ACH) mais ne prend pas en charge le mesh, et le rtw89 ne déclare même pas l'IBSS."
draft: false
---

> Cet article est un tutoriel standard de configuration réseau Linux, montrant comment activer les modes Monitor (écoute) et AP (point d'accès) des cartes Wi-Fi ALFA avec le pilote **intégré (in-kernel)** sur un kernel récent.
> Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Toutes les données sont des extraits de tests de compatibilité produit réalisés par Yopitek sur ses propres équipements et son propre Wi-Fi de bureau (SSID `YUPITEK`).
> ⚠️ **Usage légal** : le mode monitor ne concerne que l'écoute de réseaux dont vous êtes propriétaire ou autorisé ; pour le mode AP, respectez la réglementation radio locale. Cet article ne couvre aucune opération offensive visant un réseau tiers.

---

## L'essentiel (TL;DR)

Sur l'ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17), les 9 adaptateurs Wi-Fi USB ALFA testés par Yopitek (distributeur ALFA Network à Taïwan) tournent tous sur des pilotes in-kernel (`rtw88` / `rtw89` / `mt76`) sans installation de pilote, activent les modes Monitor et AP avec le même flux et laissent l'iPhone 7 Plus / 15 Pro se connecter normalement en AP 2,4G et 5G ; le kernel minimal va de 4.19 à 6.17 selon la carte.

- **Sans installation de pilote sur un kernel récent** : les Realtek `rtw88` / `rtw89` et le MediaTek `mt76` ont intégré ces puces USB ALFA au support in-kernel ; avec le kernel 6.17 (testé sur le GX10), les 9 cartes sont intégrées, la version minimale variant selon la carte, prêtes à l'emploi, sans compilation ni DKMS.
- **Le flux Monitor et AP est identique pour les trois familles** : rendre la main à NetworkManager → `iw` pour passer en monitor / `hostapd` pour monter un AP.
- **Deux pièges de compatibilité** : pour ouvrir un AP, il est conseillé de désactiver le 802.11n (`ieee80211n=0`), et d'utiliser `sae_pwe=0` pour le WPA3-SAE, sans quoi les anciens iPhone ne se connectent pas.
- **Classement des modes avancés** : le mesh n'existe que sur `mt76` ; l'IBSS en local se joint sur `mt76` et `rtw88` (ACH), le `rtw89` ne le déclare pas.
- **Règle d'or de la plateforme** : n'exécutez jamais `airmon-ng check kill` (il déconnecte le GX10), opérez uniquement sur l'interface externe `wlx*`.

## 1. Pourquoi « sans installation de pilote » est le point clé de cette génération

Par le passé, le principal obstacle à l'usage de cartes Wi-Fi USB comme les ALFA sous Linux était le pilote. Des puces comme le RTL8812AU ou le MT7610U n'entraient pas, à l'origine, dans le kernel mainline ; l'utilisateur devait récupérer un projet out-of-tree sur GitHub (par exemple `morrownr/USB-WiFi`, `aircrack-ng/rtl8812au`), puis le compiler via DKMS contre la version du kernel courant. À chaque mise à jour du kernel, DKMS devait recompiler ; dès qu'une compilation échouait, la carte disparaissait. Pour une validation de distribution ou un environnement d'enseignement exigeant une exploitation stable, c'était un point de douleur durable.

Avec les kernels mainline récents, la situation bascule : les trois grandes familles de pilotes Realtek `rtw88`, `rtw89` et MediaTek `mt76` intègrent progressivement ces puces USB au support in-kernel. La version minimale varie selon la carte (voir la colonne "Kernel min." ci-dessous) ; avec le kernel 6.17 (testé sur le GX10), les neuf cartes testées dans cet article sont intégrées, **reconnues dès le branchement, sans compilation ni DKMS**. Plus important encore, les deux projets out-of-tree les plus utilisés (les rtl8812au de morrownr et d'aircrack-ng) redirigent désormais vers ce pilote intégré, et les rapports de bogues reviennent uniformément vers `lwfinger/rtw88`. Autrement dit, l'étape de compilation manuelle du pilote peut désormais être entièrement supprimée sur un kernel récent.

La communauté `lwfinger/rtw88` est toujours activement maintenue et continue de remonter ses correctifs en amont ; la stabilité du pilote intégré se met donc à jour avec le kernel, l'utilisateur n'a plus à maintenir sa propre branche ni à rester bloqué à chaque montée de version sur un échec de compilation DKMS. Pour une validation de distribution et un environnement d'enseignement, la même procédure se réutilise sur plusieurs cartes et plusieurs mises à jour du kernel, le coût de maintenance baisse nettement — c'est pourquoi cet article met l'accent sur le « sans installation de pilote ».

Les puces couvertes par ce test et leurs modules de pilote intégrés correspondants :

| Famille de puce | Modèle de puce | Module de pilote intégré | Kernel min. | Génération / flux | Carte représentative |
|---|---|---|---|---|---|
| **MediaTek mt76** | MT7612U | `mt76x2u` | 4.19 | Wi-Fi 5 / 2T2R | AWUS036ACM |
| **MediaTek mt76** | MT7610U | `mt76x0u` | 4.19 | Wi-Fi 5 / 1T1R | AWUS036ACHM |
| **MediaTek mt76** | MT7921AUN | `mt7921u` | 5.18 | Wi-Fi 6 / 2x2 | AWUS036AXM / AXML |
| **Realtek rtw88** | RTL8812AU | `rtw88_8812au` | 6.13 | Wi-Fi 5 / 2T2R | AWUS036ACH |
| **Realtek rtw88** | RTL8811AU | `rtw88_8821au` | 6.13 | Wi-Fi 5 / 1x1 | AWUS036ACS |
| **Realtek rtw88** | RTL8821CU | `rtw88_8821cu` | 6.2 | Wi-Fi 5 / 1x1 (+BT) | AWUS036EACS |
| **Realtek rtw89** | RTL8832BU | `rtw89_8852bu` | 6.17 | Wi-Fi 6 / 2x2 | AWUS036AX / AXER |

> Si le kernel de votre système est inférieur à la version minimale de votre carte (voir le tableau ci-dessus), vous devez emprunter l'ancienne voie : installer un pilote out-of-tree via DKMS (`lwfinger/rtw88` pour les cartes rtw88). Exemple avec Ubuntu 24.04 : le kernel GA 6.8 intègre déjà les pilotes des ACM, ACHM, AXM, AXML et EACS ; le HWE 6.14 ajoute les ACH et ACS. Les AX et AXER nécessitent un kernel 6.17 ou plus (par exemple le HWE de 24.04.4). Cet article se base sur le kernel 6.17 du GX10.

---

## 2. Confirmer que le pilote est chargé et lié

Avant de basculer dans un quelconque mode, confirmez que la carte est correctement reconnue, que le pilote est lié et que l'interface est créée. Avec l'exemple de la Realtek AWUS036ACH (`rtw88_8812au`), les quatre étapes de vérification :

**Étape 1 : confirmer que le dispositif USB est énuméré.** Cherchez l'USB ID avec `lsusb` (Realtek est souvent `0bda:xxxx`, MediaTek souvent `0e8d:xxxx`) :

```bash
lsusb | grep 0bda:8812
# Bus 004 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

**Étape 2 : confirmer la liaison du pilote et le débit USB.** `lsusb -t` montre à la fois le pilote lié et la vitesse de connexion (`5000M` signifie USB 3.0) :

```bash
lsusb -t | grep rtw88_8812au
# |__ Port 001: Dev 002, If 0, Class=Vendor Specific Class, Driver=rtw88_8812au, 5000M
```

Pour une carte MediaTek, utilisez plutôt `dmesg` pour observer les messages d'initialisation du pilote et confirmer le renommage de l'interface :

```bash
sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0
```

**Étape 3 : obtenir le nom de l'interface.** Ubuntu utilise le nommage prévisible (predictable naming) ; la carte externe ALFA est toujours `wlx` + adresse MAC. Ce nom, déterminé par la MAC, **ne change pas d'un rebranchement à l'autre**, ce qui facilite la scriptisation. La carte réseau intégrée qui assure l'accès Internet porte un autre nom (`wlP9s9` sur le GX10) ; distinguez-les bien :

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cabca7f5
```

**Étape 4 : interroger les modes d'interface déclarés par la puce.** Cette étape détermine quels modes seront ensuite disponibles :

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Le Realtek rtw88 (ACH) liste `IBSS / managed / AP / AP/VLAN / monitor`, mais **pas** le mesh ni le P2P ; le MediaTek mt76 (ACHM) liste en plus `mesh point / P2P-client / P2P-GO`. Cette liste est la première source des différences de capacités entre familles, voir section 5.

---

## 3. Activer le mode Monitor (2,4 GHz / 5 GHz)

Le mode Monitor (écoute) fait recevoir à la carte les frames 802.11 directement de l'air, sans s'associer à aucun AP ; il est couramment utilisé pour le diagnostic de paquets, la ronde spectrale et l'évaluation de couverture de son propre réseau. Le flux d'activation est identique pour les trois familles, seules les précautions de stabilité propres à chacune diffèrent (voir sections 5 et 6).

**Étapes d'activation génériques :**

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no      # rendre à notre propre gestion, éviter que NetworkManager intervienne
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
iw dev $IF info | grep type
# type monitor
```

Voir `type monitor` signifie que la bascule a réussi. Spécifiez ensuite le canal à écouter. En **2,4 GHz**, utilisez `set channel` :

```bash
sudo iw dev $IF set channel 6
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch6.pcap
tcpdump -r /tmp/mon-ch6.pcap | wc -l
```

En **5 GHz**, spécifier par fréquence est moins source d'erreur (ch36 = 5180 MHz) :

```bash
sudo iw dev $IF set freq 5180
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch36.pcap
tcpdump -r /tmp/mon-ch36.pcap | wc -l
```

**Résultat attendu (extrait mesuré) :** l'AWUS036ACH capture 92 / 214 / 71 frames sur ch1 / ch6 / ch11 ; en 5 GHz, 260 / 137 / 127 frames sur ch36 / ch149 / ch157, ce qui montre que l'écoute 2,4G et 5G est normale. La MediaTek ACHM, avec un balayage en saut de fréquence `airodump-ng --band abg` de 120 secondes, trouve 19 stations de base et 14 clients autour de ch1/5/6/36/149/157. Capturer 0 paquet sur un canal signifie généralement qu'aucun AP n'y est actif à cet instant, pas une panne de carte.

Une fois en mode monitor, les outils de diagnostic standard courants fonctionnent directement sur l'interface `wlx*` : `airmon-ng` liste les cartes et l'état des pilotes, `kismet` sert de source de données pour une écoute en temps réel et produit un log `.kismet`, `Wireshark` et `tshark` analysent les paquets capturés, et `bettercap` fait la ronde de canaux. Ces outils sont tous utilisables en test sur les trois familles, bien adaptés à l'inventaire de l'occupation des canaux et de la couverture de signal de son propre environnement sans fil. La seule chose à noter : `hcxdumptool` 8.x échoue en `failed to arm` pour les trois familles sur cette plateforme, sauf l'EACS en 2,4 GHz (le pilote intégré ne fournit pas l'active-monitor) ; pour une fonction similaire, utilisez `airodump-ng` avec la suite aircrack-ng.

> **Rappel 5 GHz :** sous le regdomain par défaut (`country 00`), de nombreux canaux 5 GHz sont en passive/no-IR : l'écoute est possible, mais la transmission active est limitée. Pour un test 5 GHz ultérieur dans un cadre autorisé, déverrouillez d'abord via `sudo iw reg set US`, puis remettez via `sudo iw reg set TW` après le test. Le Realtek `rtw88_8812au` a aussi un phénomène connu de RX-stuck 5G (plus aucun paquet reçu en 5G après des bascules répétées de mode) ; le cas échéant, débranchez/rebranchez la carte une fois et traitez le 5G en priorité.

---

## 4. Activer le mode AP / point d'accès (2,4 GHz / 5 GHz)

Le mode AP (point d'accès) utilise `hostapd` pour transformer la carte en station de base Wi-Fi. Le flux est identique pour les trois familles : rendre d'abord l'interface à NetworkManager, puis démarrer avec un fichier de configuration `hostapd`. Voici la configuration minimale générique.

**4-1. 2,4 GHz (802.11g pur)**

Créez le fichier de configuration `/tmp/ap24.conf` :

```ini
interface=wlx00c0cabca7f5
driver=nl80211
ssid=ALFA-AP-24G
hw_mode=g
channel=6
country_code=TW
auth_algs=1
ieee80211n=0
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=<votre-mot-de-passe-d-au-moins-8-caracteres>
```

Démarrage :

```bash
sudo nmcli dev set $IF managed no
sudo hostapd /tmp/ap24.conf
```

Lorsqu'un client se connecte, `hostapd` affiche dans l'ordre `authenticated` → `associated` → `AP-STA-CONNECTED` → `EAPOL-4WAY-HS-COMPLETED` ; la dernière ligne signifie que le 4-way handshake est complet et la connexion réussie.

**4-2. 5 GHz (802.11a pur, ch36)**

Passez la configuration ci-dessus en 5 GHz :

```ini
ssid=ALFA-AP-5G
hw_mode=a
channel=36
```

Les cartes 2x2 (comme les rtw89 AX/AXER, les mt76 ACM/AXM) peuvent ajouter une configuration VHT80 pour monter à 80 MHz de bande passante ; pour une carte mono-antenne ou pour la compatibilité, restez en 20 MHz a pur.

**4-3. Deux réglages de compatibilité clés**

1. **Pour ouvrir un AP, il est conseillé de désactiver le 802.11n** (`ieee80211n=0`, en g pur / a pur). En test, un ancien client (iPhone 7 Plus) échoue à s'associer et affiche à tort « mot de passe incorrect » quand `ieee80211n=1` est conservé, alors qu'il s'agit en réalité de `handle_assoc_cb: STA not found` ; retirer le 802.11n permet de se connecter du premier coup.
2. **Pour le WPA3-SAE, utilisez `sae_pwe=0`** (hunting-and-pecking). Avec `sae_pwe=2` (H2E forcé), le handshake de clé échoue sur les anciens modèles. Exemple de section WPA3 :

```ini
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
ieee80211w=2
sae_pwe=0
```

Ces deux pièges se rencontrent de la même façon sur les cartes Realtek et MediaTek : ils relèvent de la compatibilité du client, pas d'une différence de pilote. Les neuf cartes testées dans cet article permettent à l'iPhone 7 Plus / 15 Pro de se connecter normalement en AP 2,4G et 5G.

**4-4. Naviguer et servir de point d'accès en même temps (STA + AP)**

La famille mt76 permet avec une seule carte de se connecter à un Wi-Fi existant et de créer en parallèle une VIF AP servant de relais. En test, l'ACHM ouvre un point d'accès 5 GHz permettant à l'iPhone de se connecter pendant que l'interface principale reste connectée à YUPITEK, avec un téléchargement toujours de 198 Mbit/s et un ping moyen de 3,2 ms. Cette combinaison exige trois conditions : la VIF AP doit utiliser une MAC différente, le nom d'interface doit rester au format `wlx`, et toutes les VIF doivent être sur le même canal. Cette combinaison n'est pas garantie par le phy sur les cartes Realtek (le managed + monitor de rtw88 est utilisable, mais le STA + AP n'est pas stable) ; pour un point d'accès relais, préférez la famille mt76.

---

## 5. Différences et limites des trois familles de puces

Les trois modes de base managed / monitor / AP sont pris en charge par les trois familles, avec des performances identiques. La différence porte sur les **modes d'interface avancés** (mesh, IBSS, active monitor, P2P) : cela dépend entièrement de la déclaration du pilote, indépendamment du nombre d'antennes de la carte. Voici la synthèse des tests.

| Mode avancé | MediaTek mt76 | Realtek rtw88 | Realtek rtw89 |
|---|---|---|---|
| Monitor (2,4G/5G) | ✅ | ✅ | ✅ |
| AP (hostapd) | ✅ | ✅ | ✅ |
| Ad-hoc / IBSS (en local) | 🟡 création en local | 🟡 création en local | ❌ non déclaré par le pilote |
| Mesh (802.11s, en local) | 🟡 création en local | ❌ `-95` non pris en charge | ❌ non déclaré par le pilote |
| Active monitor | 🟡 configurable | ❌ `-95` non pris en charge | N/A |
| Wi-Fi Direct (P2P) | nécessite un second appareil | ❌ `-95` non pris en charge | N/A |

**MediaTek mt76 (ACM / ACHM / AXM / AXML)** est la famille la plus complète en modes avancés. `iw phy info` déclare déjà `mesh point`, `IBSS`, `P2P-client/GO`. En test, on obtient en local `Joined IBSS`, `type mesh point` et l'émission des beacons correspondants (le peer link avec un second poste n'est pas vérifié faute d'un second équipement). Si votre usage est une expérimentation mesh ou IBSS en local, la famille mt76 est le premier choix. Attention particulière : le MT7921 Wi-Fi 6 (AXM/AXML), bien que complet en modes et stable en AP, ne peut pas faire d'injection de frames sur cette plateforme (cause principale : la régression du chanctx de mac80211 du stock kernel 6.16+, pas intrinsèque à la puce ; un pilote git / patché sur le même modèle peut fonctionner dans la communauté, mais le firmware verrouille le débit, correspond à morrownr/USB-WiFi #387, morrownr/mt76 #18), inadapté aux tests avancés nécessitant l'injection.

**Realtek rtw88 (ACH / ACS / EACS)** prend en charge `IBSS / managed / AP / AP/VLAN / monitor`. L'IBSS se crée en local (`Joined IBSS`, confirmé sur l'ACH ; l'EACS liste l'iftype mais le join est sans effet en test), mais **le mesh (802.11s), l'active monitor et le Wi-Fi Direct renvoient tous `Operation not supported (-95)` en test**. Une autre caractéristique propre à rtw88 est la VIF : bien que les drapeaux de `iw phy` indiquent « interface combinations are not supported », l'ACH permet en test d'avoir les deux interfaces managed + monitor up en même temps, la VIF monitor capturant 100 frames — « naviguer tout en écoutant » est viable ; mais le phy ne garantit pas cette combinaison, pour une forte charge sur la durée préférez la famille mt76.

**Realtek rtw89 (AX / AXER)** est la famille Wi-Fi 6 la plus récente de cet article ; le monitor et l'AP (avec VHT80) sont bons, la sensibilité de réception forte. Mais en modes avancés, l'active monitor / mesh / IBSS / P2P ne sont pas déclarés au niveau du pilote (N/A) ; pour ces expérimentations en local, utilisez une carte mt76. Le positionnement du rtw89 est l'écoute et le point d'accès Wi-Fi 6 stables, pas la plateforme d'expérimentation des modes d'interface avancés.

> Le choix en une phrase : **pour le mesh / IBSS en local → mt76 (ACM / ACHM) ; pour un point d'accès Wi-Fi 6 et une forte réception → rtw89 (AX / AXER) ; pour le bi-bande polyvalent et la VIF → rtw88 (ACH).**

---

## 6. Précautions de sécurité de la plateforme (GX10 + Ubuntu ARM64)

Sur une machine de type GX10, « carte intégrée pour l'accès Internet, carte ALFA externe pour les tests », les points suivants sont des règles d'or d'exploitation ; les suivre évite de se déconnecter soi-même.

1. **N'exécutez jamais `airmon-ng check kill`.** Cette commande arrête NetworkManager et coupe du même coup la connexion Internet du GX10. Cet article utilise exclusivement `iw` et `nmcli dev set <interface> managed no`, sans toucher à `check kill`.
2. **Opérez uniquement sur `wlx*`, ne touchez jamais au `wlP9s9` intégré.** Le `wlP9s9` est la ligne principale d'accès Internet du GX10 ; toute action down / changement de mode ne doit viser que l'interface `wlx*` de l'ALFA ; avant une commande, confirmez la cible avec `echo $IF`.
3. **Récupérez un RX stall par débranchement/rebranchement.** Si, après des bascules répétées monitor / AP, plus rien n'est détecté, c'est généralement un blocage de réception du pilote (particulièrement fréquent en 5G Realtek). Le logiciel ne récupère généralement pas ; **débranchez/rebranchez physiquement** la carte une fois, l'USB se ré-énumère et le nom d'interface reste cohérent car la MAC ne change pas.
4. **Changez de port USB pour les cartes composites BT+WiFi.** Les dispositifs composites Bluetooth + Wi-Fi comme l'EACS, l'AXML ont parfois leur probe Wi-Fi bloquée au rebranchement, sans créer d'interface `wlx` ; changer de port USB rétablit généralement la situation.
5. **Réglez le regdomain avant une émission 5 GHz.** Sous `country 00` par défaut, le 5 GHz est le plus souvent en no-IR, transmission active interdite. Avant un test dans un cadre autorisé, déverrouillez via `sudo iw reg set US`, puis remettez via `sudo iw reg set TW` après le test.
6. **Précautions de paquets ARM64.** Le GX10 est en aarch64 ; `aircrack-ng` manque souvent de wheel/paquet précompilé et doit être compilé depuis les sources ; `wifite` est conseillé en version GitHub pour contourner le conflit de dépendances apt. Par ailleurs, `hcxdumptool` 8.x échoue en `failed to arm` pour les trois familles sur cette plateforme, sauf l'EACS en 2,4 GHz (le pilote intégré n'a pas de support active-monitor) ; pour la capture d'écoute, utilisez `airodump-ng` avec la suite aircrack-ng.

**Revenir au mode normal après le test :**

```bash
sudo pkill hostapd 2>/dev/null
sudo ip link set $IF down
sudo iw dev $IF set type managed
sudo ip link set $IF up
sudo nmcli dev set $IF managed yes
iw dev $IF info | grep type      # attendu : type managed
```

---

## Questions fréquentes (FAQ)

**Q : Comment faire passer une carte ALFA en mode monitor sous Ubuntu 24.04 ?**
R : À partir du kernel 6.17, il suffit de rendre l'interface hors de la gestion de NetworkManager et de la basculer en mode interface monitor, sans installer de pilote tiers ; le flux est identique pour les trois familles de pilotes rtw88 / rtw89 / mt76 testées dans cet article, voir les étapes détaillées du texte.

**Q : Pourquoi n'a-t-on pas besoin d'installer un pilote pour une carte ALFA sous Ubuntu ?**
R : Parce que les Realtek `rtw88` / `rtw89` et le MediaTek `mt76` ont progressivement intégré ces puces USB au support in-kernel du kernel mainline (version minimale variable selon la carte, de 4.19 à 6.17 ; sous Ubuntu 24.04, les AX et AXER nécessitent un kernel 6.17 ou plus, par exemple le HWE de 24.04.4) ; avec le kernel 6.17 (testé sur le GX10), les 9 cartes de cet article sont intégrées, reconnues dès le branchement, sans compilation ni DKMS.

**Q : Que faire si l'ancien iPhone ne se connecte pas au point d'accès WPA3 monté avec une carte ALFA ?**
R : Le test révèle deux causes fréquentes : d'abord, le `sae_pwe` de hostapd doit être réglé à 0 et non à 2 pour être compatible avec les anciens iPhone ; ensuite, conserver le réglage 802.11n peut faire échouer l'association des anciens appareils — en priorité à la compatibilité, il est conseillé de désactiver le 802.11n.

**Q : Laquelle des familles de pilotes `rtw88`, `rtw89`, `mt76` prend en charge le mesh ou l'IBSS ?**
R : En test, la famille `mt76` (comme les AWUS036ACM / ACHM) crée en local le mesh (802.11s) et l'IBSS ; le Realtek `rtw88` peut faire un join IBSS en local (confirmé sur l'ACH) mais ne prend pas en charge le mesh, et le `rtw89` ne déclare même pas l'IBSS.

## 7. Pour aller plus loin

- Comparaison complète des capacités et évaluation globale des neuf cartes ALFA → [Hub d'évaluation des cartes Wi-Fi ALFA (tableau récapitulatif)](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Tutoriel pas à pas de la carte représentative Realtek rtw88 → [Test individuel de l'AWUS036ACH](/fr/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- Tutoriel pas à pas de la carte représentative MediaTek mt76 → [Test individuel de l'AWUS036ACHM](/fr/blog/awus036achm-asus-gx10-ubuntu-test-report/)

---

*Unité de test : Yopitek (distributeur ALFA Network à Taïwan) — https://www.yupitek.com | Environnement de test : ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Appareil de test : Apple iPhone 7 Plus (WPA3 aussi testé sur iPhone 15 Pro)*
