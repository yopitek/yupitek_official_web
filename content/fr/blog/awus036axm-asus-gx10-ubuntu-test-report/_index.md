---
title: "AWUS036AXM, test individuel : le MediaTek MT7921AU (Wi-Fi 6 2x2) sur ASUS GX10 + Ubuntu 24.04 (ARM64) — capacités Monitor · AP · WPA3 et limite d'injection"
slug: awus036axm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axm-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036axm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axm
  - mt7921
  - mt7921u
  - wifi-6
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - ap-mode
  - wpa3-sae
  - monitor-mode
description: "AWUS036AXM (mt7921u) testée sur ASUS GX10 / Ubuntu 24.04 ARM64 : monitor, AP et WPA3 disponibles, mais l'injection de paquets échoue ; inadaptée au test d'intrusion, positionnée pour le simple AP et la connexion."
faq:
  - question: "L'AWUS036AXM peut-elle faire de l'injection de paquets (packet injection) ?"
    answer: "Sur notre plateforme de test (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia), non. aireplay-ng --test renvoie No Answer, Found 0 APs en 2,4 GHz comme en 5 GHz ; impossible donc de faire un deauth ni de capturer un handshake WPA. La cause racine est la régression du chanctx de mac80211 à partir du kernel 6.16, et non une incapacité intrinsèque de la puce à injecter ; l'AWUS036AXML de la même série donne le même résultat. Pour de l'injection, choisissez plutôt l'AWUS036EACS, l'ACH ou l'ACS, validées en test."
  - question: "L'AWUS036AXM convient-elle au test d'intrusion ou à Kali ?"
    answer: "Déconseillée. Le monitor fonctionne mais la réception est faible, les paquets client et data sont souvent manqués, et sur cette plateforme l'injection échoue, interdisant le deauth et la capture de handshake. La plateforme de cet article est Ubuntu 24.04, non testée sur la distribution Kali elle-même. Elle convient au simple AP, à la connexion ordinaire et au point d'accès WPA3 ; pour le test d'intrusion, choisissez l'AWUS036EACS, l'ACH ou l'ACS."
  - question: "L'AWUS036AXM nécessite-t-elle l'installation d'un pilote sous Ubuntu 24.04 ?"
    answer: "Non. Le pilote mt7921u est intégré au kernel 6.17, reconnu dès le branchement (USB ID 0e8d:7961), sans DKMS ni compilation. Le pilote ne fournit pas les modes IBSS (Ad-hoc) ni mesh : c'est une limite, pas un problème de configuration."
  - question: "L'AWUS036AXM peut-elle ouvrir un point d'accès ? Prend-elle en charge le WPA3 ?"
    answer: "Oui, c'est son usage de prédilection. En 2,4 GHz (802.11n) et en 5 GHz VHT80, l'iPhone se connecte et est authorized ; le WPA3-SAE est disponible en 2,4 GHz (MFP: yes ; WPA3 en 5 GHz non testé), les anciens iPhone nécessitent sae_pwe=0 ; le STA+AP en parallèle (VIF) fonctionne aussi. Ce cycle ne teste que le 2,4 et le 5 GHz ; le 6 GHz et le Bluetooth n'ont pas été testés séparément."
  - question: "Le mode monitor de l'AWUS036AXM est-il bon ?"
    answer: "Elle passe en monitor et capte des beacons en 2,4 GHz comme en 5 GHz, mais la réception est faible et le volume de paquets client et data réduit ; mieux vaut se verrouiller sur un seul canal plutôt que sauter de fréquence. Pour une écoute large ou longue portée, l'AWUS036AXER et l'ACH sont nettement plus fortes dans nos tests."
draft: false
---

{{< tldr >}}L'AWUS036AXM offre monitor, AP, WPA3 et VIF utilisables sur ASUS GX10 / Ubuntu 24.04 ARM64, mais l'injection de paquets échoue en test (No Answer / Found 0 APs), interdisant le deauth et la capture de handshake ; déconseillée pour le test d'intrusion ; positionnée pour le simple AP et la connexion.{{< /tldr >}}

Yopitek est le distributeur ALFA Network à Taïwan. Cet article est le test carte par carte de l'AWUS036AXM, dans un but simple : mesurer clairement « ce qu'elle peut et ne peut pas faire » sur **ASUS GX10 (ARM64) + Ubuntu 24.04**, pour que les clients à l'achat n'aient pas à deviner d'après la fiche technique.

Précisons d'abord le positionnement : tous les tests ci-dessous sont réalisés sur les propres équipements de Yopitek, son propre Wi-Fi de bureau, à destination de nos propres téléphones de test. C'est une vérification matérielle, par le distributeur, de la compatibilité et des limites de capacités du produit, pas un tutoriel offensif visant un réseau tiers. Le texte ne fournit aucune procédure contre un réseau externe ; les mesures de monitor et d'injection sont toutes réalisées en environnement fermé en propre, à destination de nos propres appareils.

La première chose à savoir sur cette carte : **son injection échoue sur cette plateforme**. Si votre usage implique l'injection ou la capture de handshake, passez directement aux sections 4 et 5 pour la conclusion de choix ; si vous cherchez une connexion stable et un AP, l'AWUS036AXM sera une carte très compétente.

## 1. La carte et la plateforme de test

L'AWUS036AXM utilise la puce MediaTek **MT7921AU** et le pilote intégré **mt7921u**, en **Wi-Fi 6 (802.11ax), 2x2** à deux flux spatiaux. L'**AWUS036AXML** à même puce (MT7921AUN, avec en plus le Bluetooth) a exactement le même comportement Wi-Fi monitor / AP / injection sur cette plateforme ; les deux se recoupent, la différence étant que l'AXML a un Bluetooth et que, en test machine, sa bande 6 GHz est utilisable, tandis que le 6 GHz et le Bluetooth de l'AXM n'ont pas été testés séparément ce cycle.

- **Plateforme de calcul** : ASUS GX10 (ARM64 / aarch64)
- **Système d'exploitation** : Ubuntu 24.04 LTS
- **Version du kernel** : kernel 6.17.0-1014-nvidia
- **Appareil de test** : Apple iPhone 7 Plus (WPA3-SAE et VIF aussi revérifiés sur iPhone 15 Pro)
- **Environnement de test** : Wi-Fi de bureau en propre, SSID `YUPITEK`, 2,4 GHz ch5 / 5 GHz ch36
- **Période de test** : mesures sur machine réelle du 2026-11-16 au 2026-11-18

## 2. Matériel et pilote (prêt à l'emploi sans installation)

Le pilote mt7921u est déjà intégré au kernel 6.17 ; l'AWUS036AXM est reconnue dès le branchement sur le GX10, sans DKMS ni compilation d'un pilote tiers. C'est ce que cette génération de cartes MediaTek a de plus pratique en ARM64.

| Élément | Contenu |
|---|---|
| Modèle | AWUS036AXM |
| Puce | MediaTek MT7921AU |
| USB ID | `0e8d:7961` |
| Pilote (in-kernel) | `mt7921u` |
| Génération / flux | Wi-Fi 6 (802.11ax) / 2x2 |
| Modes d'interface | managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO / P2P-device |
| Modes non pris en charge | IBSS (Ad-hoc), Mesh (802.11s) |

Confirmer que la carte est reconnue :

```bash
lsusb | grep 0e8d:7961
```

Sortie attendue : `ID 0e8d:7961 MediaTek Inc. Wireless_Device`. À noter aussi : les modes d'interface listés par `iw phy info` n'incluent ni IBSS ni mesh point — c'est une limite intrinsèque du mt7921u, pas un problème de configuration ; pour les scénarios mesh / IBSS, utilisez les `mt76` AWUS036ACM / ACHM.

## 3. Capacités mesurées : Monitor / AP / WPA3, et l'explication honnête de l'échec d'injection

D'abord une matrice des capacités centrales, puis le détail point par point.

| Capacité | 2,4 GHz | 5 GHz | Remarque mesurée |
|---|---|---|---|
| Monitor (écoute) | ✅ disponible (réception faible) | ✅ disponible (réception faible) | Capte des beacons, volume de client / data frame réduit |
| **Injection** | ❌ **échec sur cette plateforme** | ❌ **échec sur cette plateforme** | Cause racine : régression du chanctx de mac80211 à partir du kernel 6.16 (pas intrinsèque à la puce) |
| AP (point d'accès) | ✅ avec 802.11n (HT20) | ✅ VHT 80 MHz | iPhone 7 Plus connecté sur machine, authorized |
| WPA3-SAE | ✅ | Non testé | MFP: yes, `sae_pwe=0` compatible avec les anciens iPhone ; testé en 2,4 GHz uniquement |
| VIF (STA + AP) | ✅ | ✅ | Carte à double usage, ping côté STA 17 ms |

### Monitor (écoute) ✅ disponible, mais réception faible

On passe en mode monitor en 2,4 GHz comme en 5 GHz, et on y capte des beacons. Mais soyons honnêtes : la réception de l'AWUS036AXM est nettement plus faible que celle des AWUS036ACM / ACHM de la même plateforme, le nombre de frames mesuré est réduit, et le volume capturé de paquets client et data est faible. En pratique, il vaut mieux **se verrouiller sur un seul canal** pour l'écoute, sans saut de fréquence, pour des résultats plus stables.

Un point facile à mal interpréter : en mode monitor, `txpower` rapporte 3 dBm, un artefact de rapport (le TX matériel réel est d'environ 20 dBm, vérifié via `txpower_sku`), qui ne signifie pas que l'émission est réellement bridée aussi bas. L'AWUS036AXM n'est de toute façon pas conçue pour l'écoute large ; pour balayer large et capter loin, tournez-vous vers l'AWUS036AXER (réglage d'antenne plus fort, saut de fréquence plus agressif) ou l'AWUS036ACH (fort gain bi-antenne), dont la réception en monitor est nettement supérieure sur la même plateforme.

### AP (point d'accès) ✅ c'est le scénario de prédilection de l'AXM

En 2,4 GHz, l'AP peut activer le 802.11n (HT20) ; l'iPhone 7 Plus connecté négocie MCS 7, authorized. En 5 GHz, elle monte jusqu'à **VHT 80 MHz** ; l'iPhone connecté est en VHT-NSS2, authorized. En 2,4G comme en 5G, l'AWUS036AXM est stable en point d'accès : c'est la capacité la plus intéressante à l'achat sur cette plateforme.

### WPA3-SAE ✅

Côté AP, avec le WPA3-SAE activé, l'iPhone 7 Plus se connecte avec succès, MFP (Management Frame Protection) à `yes`. Rappel pratique : régler `sae_pwe=0` assure la compatibilité avec les appareils plus anciens comme l'iPhone 7 Plus ; avec `sae_pwe=2`, les anciens iPhone risquent de ne pas se connecter.

### VIF (STA + AP, carte à double usage) ✅

L'AWUS036AXM peut à la fois être STA connectée à un Wi-Fi existant et ouvrir une interface virtuelle AP (VIF). En test, pendant que l'iPhone 15 Pro est connecté à la VIF AP, le ping du côté STA vers `YUPITEK` est d'environ 17 ms, connexion normale. Pour le besoin « une carte qui navigue et partage un point d'accès en même temps », c'est disponible.

### Injection ❌ échec sur cette plateforme — c'est la ligne de partage pour le choix

C'est la ligne la plus importante et celle qui mérite le plus d'honnêteté sur l'AWUS036AXM. En test, la sortie de `aireplay-ng --test` est :

```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

Même échec en 2,4 GHz comme en 5 GHz. Clarifions d'abord un malentendu courant : en mode monitor, le fait que `iw` rapporte un txpower de seulement 3 dBm est un **artefact de rapport**, le TX matériel réel est d'environ 20–23 dBm (vérifié via `txpower_sku`), la puissance d'émission n'est pas bridée, ce n'est pas la cause principale de l'échec. La vraie cause racine est **au niveau logiciel** : après le kernel 6.16, le channel context (chanctx) de mac80211 a connu une régression qui empêche le pilote stock de recevoir les beacons cibles en situation d'active monitor / injection, `aireplay-ng` conclut donc `No Answer`. C'est une **régression côté kernel, pas une incapacité intrinsèque de la puce MT7921 à injecter**. Le phénomène est consigné dans morrownr/USB-WiFi issue #387, l'analyse de cause racine dans morrownr/mt76 issue #18.

À compléter : des tests communautaires indiquent qu'en passant à un pilote git / patché sur le même modèle, on peut effectivement faire fonctionner l'active monitor avec injection ; mais même ainsi, le firmware MT7921 **verrouille l'injection sur les débits de base de 1 Mbps / 6 Mbps**, sans injection aux débits HT / VHT. Autrement dit, même en contournant la régression du kernel, la capacité d'injection de cette carte reste limitée. En comparaison, les cartes Realtek rtw89 (comme l'AWUS036AX / AXER) ont une injection disponible avec la même suite aircrack-ng sur la même plateforme GX10 ; cette voie MT7921 ne passe pas sur le **stock kernel 6.17**.

Encore une fois, ce n'est pas une panne de carte isolée ni un réglage erroné. L'AWUS036AXML à même puce se comporte exactement de la même façon ; sur le stock kernel 6.17, changer les paramètres, le canal ou le domaine réglementaire n'y change rien — la cause racine est la régression du chanctx de mac80211 à partir du kernel 6.16, plus le verrouillage du débit d'injection par le firmware, et non un défaut matériel de la puce. Conséquence directe : l'AWUS036AXM **ne peut pas faire de deauth ni capturer activement un handshake WPA** sur cette plateforme. Pour ces capacités, utilisez la solution Realtek / mt76x de la section suivante.

Quant aux fonctions avancées, voici le récapitulatif :

| Fonction avancée | État | Commentaire |
|---|---|---|
| Capture de handshake WPA | ❌ | Indisponible du fait de l'échec d'injection, utilisez ACM / ACHM / ACH / ACS / EACS |
| VIF (STA + AP) | ✅ | Carte à double usage disponible |
| Active monitor | 🟡 | `set monitor active` accepté, ACK non vérifié |
| Ad-hoc (IBSS) | N/A | Non pris en charge par mt7921u |
| Mesh (802.11s) | N/A | Non pris en charge par mt7921u |
| Wi-Fi Direct (P2P) | ⬜ | Déclaré pris en charge par le pilote, non testé faute d'un second équipement |

### Sécurité d'exploitation et rappels pratiques

Quelques points pratiques pour manipuler cette carte sur le GX10, à connaître à l'avance pour éviter les pièges :

- **Ne coupez pas votre propre réseau** : n'exécutez jamais `airmon-ng check kill`, il arrête NetworkManager et déconnecte tout le GX10. Opérez uniquement sur l'interface externe `wlx*`, sans toucher à la ligne principale d'accès Internet intégrée du GX10.
- **Le mot de passe de l'AP doit faire au moins 8 caractères** : sinon hostapd renvoie `invalid WPA passphrase length` et ne démarre pas.
- **Si le téléphone ne détecte pas le SSID** : réinitialisez en débranchant/rebranchant la carte une fois, ou rapprochez le téléphone (le 3 dBm rapporté en monitor est un artefact, pas la puissance réelle, et n'est pas la cause principale).
- **Dépannage du RX stall** : si, après des bascules répétées monitor / AP, plus rien n'est détecté, c'est généralement un RX stall ; débranchez/rebranchez la carte une fois pour récupérer (le nom d'interface, nommé d'après la MAC, ne change pas).

## 4. Usages adaptés et inadaptés

Résumons les mesures ci-dessus en une phrase : l'AWUS036AXM est une excellente carte « connexion / AP », mais pas une carte « injection / offensive ».

**Usages adaptés**

- Connexion quotidienne stable (Wi-Fi 6, 2x2)
- Montage d'un point d'accès 2,4 GHz / 5 GHz (avec 802.11n et VHT80)
- Vérification de compatibilité WPA3-SAE et tests de déploiement
- STA + AP à double usage (VIF)
- Besoin de monitor léger en écoute passive de beacons

**Usages inadaptés (pièges à éviter)**

- injection / deauth
- Capture de handshake WPA, exercices offensifs actifs
- Expérimentations nécessitant l'IBSS (Ad-hoc) ou le Mesh
- Écoute large longue portée et haute sensibilité

**Le piège le plus important à éviter** : si votre usage est l'**injection ou le handshake**, **ne choisissez pas l'AWUS036AXM (ni l'AWUS036AXML à même puce)**. Le MT7921 échoue à l'injection sur la plateforme ASUS GX10 (ARM64 / Ubuntu 24.04 / stock kernel 6.17) ; la cause racine est la régression du chanctx de mac80211 à partir du kernel 6.16, et non une incapacité intrinsèque de la puce à injecter ; au 2026-11-18, l'environnement stock ne se corrige pas par réglage — réservez-la aux scénarios « pure connexion / pur AP ».

## 5. Conseils de choix (pur AP / connexion)

| Votre besoin | Choix conseillé | Raison |
|---|---|---|
| Pur AP / connexion stable (sans injection) | **AWUS036AXM** / AWUS036AXML | MediaTek stable en connexion, bonnes performances AP et WPA3 |
| Test d'intrusion (injection + handshake) | AWUS036EACS / AWUS036ACH / AWUS036ACS | Injection disponible sur les deux bandes, handshake de bout en bout fonctionnel |
| Meilleure réception / monitor longue portée | AWUS036AXER / AWUS036ACH | L'AXER est agressive en saut de fréquence, l'ACH a un fort gain bi-antenne |
| Wi-Fi 6 + AP avec injection | AWUS036AX / AWUS036AXER | 2x2 VHT80, AP stable et injection disponible |
| Expérimentation mesh / IBSS | AWUS036ACM / AWUS036ACHM | Le pilote `mt76` crée en local |

En clair : pour une connexion stable ou un AP, l'AWUS036AXM est très compétente ; dès que l'injection ou le handshake entrent en jeu, passez aux Realtek EACS / ACH / ACS. Pour la comparaison complète de ce lot de cartes sur ARM64 et la matrice complète Monitor / Injection / AP / WPA3 des 9 modèles, voyez le tableau Hub :

- [Le test le plus complet de 2026 : la matrice complète des 9 cartes Wi-Fi ALFA sur ASUS GX10 (ARM64 / Ubuntu 24.04)](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

Rappelons encore le positionnement : toutes les mesures de monitor / injection de cet article sont réalisées en environnement fermé en propre chez Yopitek, à destination de nos propres appareils de test, dans le but de vérifier les capacités du produit et les limites de compatibilité ; nous ne fournissons ni ne conseillons les opérations ci-dessus contre un quelconque réseau tiers.

## Questions fréquentes (FAQ)

**Q1. L'AWUS036AXM peut-elle faire de l'injection de paquets (packet injection) ?**
Sur notre plateforme de test (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia), non. `aireplay-ng --test` renvoie `No Answer`, `Found 0 APs` en 2,4 GHz comme en 5 GHz ; impossible donc de faire un deauth ni de capturer un handshake WPA. La cause racine est la régression du chanctx de mac80211 à partir du kernel 6.16, et non une incapacité intrinsèque de la puce à injecter ; l'AWUS036AXML de la même série donne le même résultat. Pour de l'injection, choisissez plutôt l'AWUS036EACS, l'ACH ou l'ACS, validées en test.

**Q2. L'AWUS036AXM convient-elle au test d'intrusion ou à Kali ?**
Déconseillée. Le monitor fonctionne mais la réception est faible, les paquets client et data sont souvent manqués, et sur cette plateforme l'injection échoue, interdisant le deauth et la capture de handshake. La plateforme de cet article est Ubuntu 24.04, non testée sur la distribution Kali elle-même. Elle convient au simple AP, à la connexion ordinaire et au point d'accès WPA3 ; pour le test d'intrusion, choisissez l'AWUS036EACS, l'ACH ou l'ACS.

**Q3. L'AWUS036AXM nécessite-t-elle l'installation d'un pilote sous Ubuntu 24.04 ?**
Non. Le pilote mt7921u est intégré au kernel 6.17, reconnu dès le branchement (USB ID `0e8d:7961`), sans DKMS ni compilation. Le pilote ne fournit pas les modes IBSS (Ad-hoc) ni mesh : c'est une limite, pas un problème de configuration.

**Q4. L'AWUS036AXM peut-elle ouvrir un point d'accès ? Prend-elle en charge le WPA3 ?**
Oui, c'est son usage de prédilection. En 2,4 GHz (802.11n) et en 5 GHz VHT80, l'iPhone se connecte et est authorized ; le WPA3-SAE est disponible en 2,4 GHz (`MFP: yes` ; WPA3 en 5 GHz non testé), les anciens iPhone nécessitent `sae_pwe=0` ; le STA+AP en parallèle (VIF) fonctionne aussi. Ce cycle ne teste que le 2,4 et le 5 GHz ; le 6 GHz et le Bluetooth n'ont pas été testés séparément.

**Q5. Le mode monitor de l'AWUS036AXM est-il bon ?**
Elle passe en monitor et capte des beacons en 2,4 GHz comme en 5 GHz, mais la réception est faible et le volume de paquets client et data réduit ; mieux vaut se verrouiller sur un seul canal plutôt que sauter de fréquence. Pour une écoute large ou longue portée, l'AWUS036AXER et l'ACH sont nettement plus fortes dans nos tests.

## 6. Pour aller plus loin

Les articles connexes ci-dessous seront mis en ligne progressivement (liens en construction) :

- « Sans installation de pilote : activer les modes Monitor et AP sous Ubuntu (ARM64) » → [`/fr/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/fr/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- « Capacité WPA3-SAE et pratique du handshake (vérifié en environnement propre) » → [`/fr/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/fr/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- « Test individuel de l'AWUS036AXML (même puce MT7921 + BT) » → (en construction)
- « Pourquoi le mt7921u ne peut pas injecter sous le noyau 6.16+ : la régression chanctx et le verrouillage du débit par le firmware » → (en construction)

---

*Unité de test : Yopitek (distributeur ALFA) | Plateforme : ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Appareil de test : Apple iPhone 7 Plus (WPA3 / VIF aussi testés sur iPhone 15 Pro)*
