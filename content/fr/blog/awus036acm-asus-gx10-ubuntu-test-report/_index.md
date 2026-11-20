---
title: "AWUS036ACM, test carte par carte : le MediaTek MT7612U (mt76x2u) sur ASUS GX10 + Ubuntu 24.04 (ARM64) — rapport sur les capacités Monitor / Injection / AP et mesh"
slug: awus036acm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acm
  - mt7612u
  - mt76x2u
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - mesh
description: "L'AWUS036ACM (MT7612U) fonctionne sans installation de pilote sous Ubuntu 24.04 ARM64 : mode monitor bi-bande et aircrack-ng (couramment utilisé sous Kali) disponibles, injection de paquets 2,4G 63–83 %, 5G 76 %, prise en charge des VIF et du mesh / IBSS en local."
faq:
  - question: "L'AWUS036ACM nécessite-t-elle l'installation d'un pilote sous Ubuntu ou Kali ?"
    answer: "Non. Le MT7612U est pris en charge par le pilote mt76x2u intégré au kernel : sous Ubuntu 24.04 (kernel 6.17), la carte est reconnue dès le branchement, sans DKMS ni flashage manuel de firmware. La plateforme de ce test est Ubuntu 24.04 ARM64 ; sous Kali, le comportement devrait être identique dès lors que le kernel est suffisamment récent, mais cela n'a pas été vérifié sur une machine Kali réelle cette fois-ci."
  - question: "L'AWUS036ACM peut-elle passer en mode monitor et faire de l'injection de paquets ? Quel est le taux de réussite ?"
    answer: "Oui. Le mode monitor et la capture fonctionnent correctement en 2,4 GHz comme en 5 GHz ; au test d'injection aireplay-ng, le taux est de 63–83 % en 2,4 GHz et de 76 % en 5 GHz, ce qui la situe en milieu de tableau parmi les neuf cartes. Pour une injection bi-bande à 100 %, les mesures Yopitek désignent l'AWUS036ACH et l'AWUS036EACS comme les meilleures."
  - question: "L'AWUS036ACM peut-elle ouvrir un point d'accès tout en restant connectée à Internet (VIF) ?"
    answer: "Oui. Les deux combinaisons STA+AP (connexion au réseau amont d'un côté, point d'accès de l'autre) et AP+monitor (point d'accès et écoute simultanés) ont été vérifiées. C'est là que la concurrence multi-interface du pilote mt76 est la plus complète ; le point d'accès 5 GHz peut monter jusqu'à VHT 80 MHz."
  - question: "L'AWUS036ACM prend-elle en charge le mesh (802.11s) et l'IBSS ?"
    answer: "Création en local possible. Sous Ubuntu 24.04 / kernel 6.17, l'AWUS036ACM peut créer des interfaces mesh 802.11s et IBSS (Ad-hoc) ; mais faute d'un second nœud cette fois-ci, l'interconnexion multi-nœuds n'a pas été vérifiée, donc on se limite à affirmer la création en local."
  - question: "L'AWUS036ACM peut-elle capturer un handshake WPA ?"
    answer: "Oui. Sur notre propre AP et notre propre iPhone 7 Plus, le test de bout en bout a réussi : deauth, capture complète des 4-way (M1–M4) et export hashcat .22000 avec hcxpcapngtool --all. Uniquement sur des réseaux dont vous êtes propriétaire ou autorisé."
draft: false
---

> Cet article est le compte rendu, réalisé par Yopitek, des tests de compatibilité produit et de capacités de l'ALFA AWUS036ACM sur une plateforme Linux récente, destiné à l'évaluation et au choix de modèle.
> Plateforme de test : ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Toutes les données sont des extraits de mesures réalisées par Yopitek sur **ses propres équipements, son propre réseau Wi-Fi de bureau** (SSID `YUPITEK`, 2,4G ch5 / 5G ch36, ch157) à destination de **ses propres téléphones de test** (Apple iPhone 7 Plus ; le WPA3 a été revérifié avec un iPhone 15 Pro).
> ⚠️ **Déclaration de légalité et de périmètre** : le mode monitor, l'injection et la capture de handshake ne sont réalisés que sur des réseaux et des appareils dont vous êtes propriétaire ou autorisé ; pour le mode AP, respectez la réglementation radio locale. Cet article se concentre sur les capacités, la compatibilité et la configuration de la carte elle-même, et **ne couvre aucune opération offensive visant un réseau tiers**.

## L'essentiel (TL;DR)

Mesuré par Yopitek (distributeur ALFA Network à Taïwan) sur ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17) : l'AWUS036ACM fonctionne en mode monitor bi-bande, atteint 63–83 % d'injection de paquets sur 2,4G et 76 % sur 5G, et monte un point d'accès sur les deux bandes (5G en VHT 80 MHz).

- Sous Ubuntu 24.04 (ARM64), aucune installation de pilote : le MT7612U est pris en charge par le mt76x2u intégré au kernel 6.17, reconnu dès le branchement, sans DKMS.
- Mode monitor bi-bande disponible ; injection de paquets 63–83 % en 2,4G et 76 % en 5G, soit un milieu de tableau parmi les neuf cartes.
- Création en local d'interfaces mesh 802.11s et IBSS, et prise en charge des VIF (STA+AP, AP+monitor).
- La capture de handshake WPA est de bout en bout (4-way complet, export hashcat `.22000`) ; l'une des 7 cartes sur 9 qui l'ont menée à terme.
- Pour une injection bi-bande à 100 %, préférez l'AWUS036ACH ou l'AWUS036EACS.

---

## 1. Cette carte et la plateforme de test

L'AWUS036ACM est la carte bi-bande MediaTek de la gamme ALFA, à base de puce MT7612U, Wi-Fi 5 (802.11ac), 2T2R (deux flux spatiaux), bi-bande 2,4 GHz / 5 GHz. Elle figure de longue date comme carte recommandée pour Kali dans la liste de morrownr — non pour ses chiffres de débit, mais parce que la famille de pilotes `mt76` offre un support Linux relativement complet du mode monitor, de l'injection et de la concurrence multi-interface (VIF) ; les modes expérimentaux comme le mesh 802.11s ne tiennent d'ailleurs, sur cette plateforme, que dans le camp mt76 (les cartes Realtek ne savent monter qu'un IBSS en local et n'arrivent pas à démarrer le mesh). Évaluer cette carte, c'est donc moins regarder la vitesse que vérifier si l'éventail de capacités est complet, si les particularités du mt76 se concrétisent vraiment, et quels points doivent être honnêtement marqués comme limites.

Ce cycle reprend le même scénario d'exploitation : la carte intégrée du GX10 (`wlP9s9`) assure l'accès Internet, tandis que l'AWUS036ACM, branchée en USB, ne porte que la charge de test ; le passage en monitor ou en AP ne touche jamais au réseau de la machine hôte. On opère exclusivement sur l'interface `wlx*` de la carte ALFA, sans jamais toucher à la carte réseau intégrée qui assure la connectivité.

| Élément | Contenu |
|---|---|
| Modèle | AWUS036ACM |
| Puce | MediaTek MT7612U (Wi-Fi 5 / 802.11ac, 2T2R bi-flux) |
| Pilote | `mt76x2u` (in-kernel, intégré au kernel 6.17) |
| Génération / flux | Wi-Fi 5 / 2T2R |
| Remarque | Carte recommandée Kali par morrownr |
| Plateforme | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| Appareil de test | Apple iPhone 7 Plus (WPA3 aussi testé sur iPhone 15 Pro) |
| Environnement de test | Wi-Fi de bureau en propre, SSID `YUPITEK`, 2,4G ch5 / 5G ch36, ch157 |

> Le tableau récapitulatif de ce cycle n'a pas renseigné les champs USB ID ni version de firmware de l'AWUS036ACM (marqués « — ») ; cet article ne spécule donc pas sur ces deux valeurs. Toutes les données de capacités ci-dessous proviennent des lignes ACM du tableau récapitulatif.

---

## 2. Matériel et pilote (sans installation)

Cette carte est reconnue dès le branchement sur le GX10, sans compilation ni DKMS. Le MT7612U est directement pris en charge par le pilote `mt76x2u` intégré au kernel mainline : aucun projet out-of-tree à ajouter, aucun blob de firmware à flasher manuellement. Pour l'ARM64, c'est l'avantage le plus concret du mt76. Beaucoup de pilotes Realtek tiers n'ont pas de binaire précompilé pour aarch64 et doivent être compilés contre la version du kernel ; le mt76, étant in-kernel, ne se retrouve pas bloqué par une dépendance de pilote lors d'une montée de version du kernel.

Une fois la carte branchée, l'interface est nommée `wlx` + MAC (par exemple `wlxXXXXXXXXXXXX`) ; le nom est lié à la MAC et ne change pas d'un rebranchement à l'autre, ce qui facilite son référencement fixe dans un script. Pour confirmer la liaison du pilote et la création de l'interface, utilisez ces vérifications génériques (les noms d'interface et les numéros de phy diffèrent d'une machine à l'autre) :

```bash
# Trouver le nom d'interface de la carte ALFA (uniquement les noms en wlx, sans toucher à wlP9s9)
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"

# Confirmer que le pilote lié est bien mt76x2u
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# mt76x2u

# Lister les modes d'interface déclarés par ce phy (décisif pour les capacités suivantes)
iw phy "$(cat /sys/class/net/$IF/phy80211/name)" info | sed -n '/Supported interface modes/,/Band 1/p'
```

D'après ce cycle de tests, les modes d'interface disponibles sous `mt76x2u` sont plus complets que sous le Realtek `rtw88` : outre managed / AP / monitor, l'IBSS et le mesh point se montent aussi en local (voir section 4). C'est ce qui permet ensuite à l'ACM de faire tourner mesh / IBSS en local ; la carte Realtek de la même plateforme (comme l'AWUS036ACH) peut certes établir un IBSS en local, mais le mesh 802.11s et l'active monitor n'y démarrent pas.

---

## 3. Capacités mesurées : Monitor / Injection / AP / WPA3

Voici d'abord le tableau récapitulatif des capacités clés (tiré de la 1re ligne du tableau des neuf cartes), puis le détail point par point. Tous les points ont été réalisés sur notre propre point d'accès `YUPITEK` et notre propre iPhone 7 Plus.

| Capacité | 2,4 GHz | 5 GHz | Commentaire |
|---|---|---|---|
| Monitor (écoute en réception) | ✅ | ✅ | Passage en monitor et capture corrects sur les deux bandes |
| Injection (injection de paquets) | ✅ 63–83 % | ✅ 76 % | Taux de réussite d'injection au test d'injection standard |
| Point d'accès (hostapd) | ✅ | ✅ 80MHz | Le 5G monte jusqu'à VHT 80 MHz |
| WPA3-SAE (côté AP) | ✅ | Non testé | WPA3-SAE testé uniquement en 2,4 GHz ; 5 GHz non testé |

### 3-1. Monitor (2,4 GHz + 5 GHz) ✅

Le mode monitor et la capture fonctionnent correctement en 2,4 GHz comme en 5 GHz : c'est la capacité la moins discutable de cette carte. Pour une carte 2T2R à deux antennes, la réception en écoute sur les deux bandes est stable, suffisante pour soutenir un inventaire de canaux sur site et un diagnostic de paquets.

### 3-2. Injection (injection de paquets) ✅ (niveau milieu de tableau)

Au test d'injection standard mesurant la fiabilité de l'injection de paquets, l'AWUS036ACM obtient 63–83 % en 2,4 GHz et 76 % en 5 GHz. Parmi les neuf cartes, cela la place en milieu de tableau, nettement derrière les Realtek RTL8812AU (AWUS036ACH, 100 % sur les deux bandes) et RTL8821CU (AWUS036EACS, 100 % sur les deux bandes), mais avec une fonctionnalité complète et suffisante en pratique. L'ACM sait injecter, sa stabilité n'est simplement pas la meilleure de la classe ; si un client place « le meilleur taux de réussite d'injection » au premier rang, ce n'est pas le premier choix (voir section 5, choix de modèle).

Avant d'injecter en 5 GHz, un détail de configuration mérite attention : le domaine réglementaire par défaut verrouille la transmission active sur une partie des bandes UNII. Avant le test, il faut basculer le domaine réglementaire sur un réglage autorisant l'émission, puis le remettre sur le domaine local une fois le test terminé (`iw reg set US` → test → `iw reg set TW`). C'est un préalable à l'émission correcte en 5 GHz, indépendant des capacités de la carte.

### 3-3. Point d'accès et WPA3-SAE ✅

L'AWUS036ACM peut servir de point d'accès, en 2,4 GHz comme en 5 GHz, le 5 GHz montant même à 80 MHz de bande passante (VHT80). Une fois le WPA3-SAE activé côté AP en 2,4 GHz, notre téléphone de test s'y connecte correctement (le WPA3 en 5 GHz n'a pas été testé).

Une comparaison vaut la peine ici avec le modèle mono-antenne mt76 AWUS036ACHM : sur l'ACHM, le WPA3 exige de régler spécifiquement le `sae_pwe` de hostapd à 0, sans quoi l'iPhone 7 Plus ne se connecte pas. L'AWUS036ACM n'a pas rencontré cette limite ce cycle-ci : le WPA3-SAE fonctionne directement.

---

## 4. Capacités avancées : VIF / mesh / IBSS en local et limites

Allons une couche plus loin avec le handshake, les interfaces virtuelles (VIF), l'active monitor et le mesh / IBSS. Cette section est aussi celle où l'AWUS036ACM creuse l'écart avec les cartes Realtek.

| Élément avancé | Résultat ACM | Commentaire |
|---|---|---|
| Capture de handshake WPA | ✅ de bout en bout (.22000) | Deauth de notre iPhone 7 Plus, capture complète des 4-way M1–M4, export hashcat `.22000` |
| VIF (concurrence multi-interface) | ✅ STA+AP / AP+mon | STA+AP ou AP+monitor simultanés possibles |
| Active monitor | 🟡 configurable, ACK non vérifié | Le mode se monte, le comportement d'ACK n'est pas vérifié |
| Ad-hoc (IBSS) | 🟡 en local | Interface créée en local, interconnexion nécessite un second poste |
| Mesh (802.11s) | 🟡 en local | Interface créée en local, interconnexion nécessite un second poste |
| Wi-Fi Direct (P2P) | ⬜ nécessite un second poste | Non testé ce cycle |

### 4-1. VIF (concurrence d'interfaces virtuelles) — le point fort de l'ACM ✅

Cette carte sait faire tourner deux interfaces virtuelles en même temps. Ce cycle a vérifié les deux combinaisons STA+AP (connexion au réseau amont d'un côté, point d'accès de l'autre) et AP+monitor (point d'accès d'un côté, écoute de l'autre), adaptées aux scénarios « se connecter tout en observant » ou « une seule carte servant à la fois de client et de station de base ». C'est là que la concurrence multi-interface du pilote `mt76` est la plus complète.

### 4-2. Mesh / IBSS « possible en local » — la différence clé du mt76 🟡

L'AWUS036ACM peut monter en local des interfaces mesh 802.11s et ad-hoc (IBSS) ; les Realtek `rtw88` / `rtw89` (AWUS036ACH, AWUS036AX, etc.) peuvent certes aussi établir un IBSS en local, mais ne prennent pas en charge le mesh 802.11s sur cette plateforme. Pour une expérimentation mesh 802.11s, les cartes mt76 (ACM / ACHM) disposent donc d'un point de départ que les cartes Realtek n'ont pas.

Soyons précis sur la limite : ce cycle a confirmé « la création d'interface en local » ; l'interconnexion multi-nœuds complète nécessite encore une seconde carte / un second nœud, non réalisée ici, d'où le 🟡 (en local) plutôt qu'un ✅.

### 4-3. Les limites honnêtes des capacités

- **handshake** : l'ACM a mené à terme toute la chaîne de bout en bout (deauth de notre propre appareil → capture complète des 4-way M1–M4 → `hcxpcapngtool --all` pour exporter le hashcat `.22000`), même si son taux de réussite d'injection (2,4G 63–83 % / 5G 76 %) est inférieur à celui des cartes Realtek.
- **active monitor** : le mode se monte, mais le comportement d'ACK n'a pas été vérifié ce cycle (marqué 🟡). À noter : au niveau de la plateforme, `hcxdumptool` 8.x échoue en `failed to arm` sur toutes les cartes sauf l'AWUS036EACS en 2,4 GHz (il exige l'active-monitor, que la carte intégrée tri-bande de la plateforme et les pilotes actuels ne fournissent pas) ; le processus de handshake de l'ACM passe donc par `airodump-ng` + `aireplay-ng`.
- **Wi-Fi Direct (P2P)** : non testé ce cycle, nécessite un second équipement.

### 4-4. Précautions d'exploitation sur la plateforme (GX10 ARM64, propres à l'ACM)

1. **Ne coupez pas votre propre réseau** : n'exécutez jamais `airmon-ng check kill` (il arrête NetworkManager et déconnecte le GX10 d'Internet) ; ne touchez qu'aux `wlx*`, jamais au `wlP9s9` intégré qui assure la connectivité.
2. **Dépannage du RX stall** : si, après avoir basculé plusieurs fois entre monitor / AP, plus rien n'est détecté, il suffit de **débrancher et rebrancher** la carte une fois (ré-énumération USB ; le nom d'interface, déterminé par la MAC, ne change pas).
3. **Déverrouillage du TX 5 GHz** : avant une injection 5 GHz, réglez le bon domaine réglementaire pour déverrouiller la puissance d'émission, puis remettez le domaine local après le test.
4. **Technique de capture de handshake** : au bureau, plusieurs AP portent souvent le même nom ; en pratique, plutôt que de verrouiller un seul `--bssid`, il est plus robuste de capturer tout le canal ; pour l'export, utilisez `hcxpcapngtool --all`.
5. **Chaîne d'outils ARM64** : `aircrack-ng` doit être compilé depuis les sources ; utilisez `wifite` en version git 3.0.0 (pour contourner le conflit de dépendances apt).

Au niveau de la plateforme, les outils Kali (`airmon-ng`, `kismet`, `bettercap`, `wifite` version git, Wireshark / tshark) utilisent tous l'ACM comme source de données sans problème ; la seule exception est le `hcxdumptool` évoqué, qui requiert l'active-monitor.

---

## 5. Cas d'usage et choix de modèle (retour vers le Hub)

En rapportant les capacités ci-dessus au positionnement produit, le rôle de l'AWUS036ACM est en fait très clair : une carte Wi-Fi 5 2T2R aux capacités équilibrées, sans installation de pilote, et dotée en propre des avantages mt76 mesh / IBSS / VIF. À quels scénarios la destiner ?

- **Premier choix pour l'expérimentation mesh (802.11s)** : parmi ces neuf cartes, seules les mt76 ACM / ACHM savent créer une interface mesh 802.11s en local ; les Realtek `rtw88` / `rtw89` peuvent monter un IBSS en local mais ne prennent pas en charge le mesh 802.11s. Pour une expérimentation mesh, l'ACM est le bon point de départ.
- **Besoin de concurrence VIF** : STA+AP et AP+monitor tiennent, adaptés à une carte unique servant à la fois de client et d'AP, ou à « se connecter tout en écoutant ».
- **Priorité à l'exploitation sans pilote** : `mt76x2u` in-kernel, pas de blocage de pilote lors d'une montée de version du kernel, et en ARM64 on évite la corvée de compiler des modules out-of-tree.
- **Scénarios où ce n'est pas la meilleure solution** : si le besoin central est « le taux de réussite d'injection le plus élevé », l'injection de l'ACM (2,4G 63–83 % / 5G 76 %) n'est pas la meilleure de la classe ; préférez les Realtek AWUS036EACS / ACH / ACS ; pour la meilleure réception / le monitor longue portée, voyez l'AWUS036AXER / ACH.

Par rapport à la même famille, les différences de positionnement sont les suivantes :

| Besoin | Carte conseillée | Raison |
|---|---|---|
| Expérimentation mesh (802.11s) en local | **AWUS036ACM** / AWUS036ACHM | Le pilote `mt76` crée un mesh 802.11s en local (Realtek ne fait que l'IBSS en local, pas le mesh) |
| Concurrence VIF (STA+AP / AP+mon) | **AWUS036ACM** | Concurrence multi-interface établie |
| Injection bi-bande à 100 % / handshake de bout en bout | AWUS036EACS, AWUS036ACH, AWUS036ACS | Meilleure injection sur les deux bandes, bout en bout `.22000` déjà prouvé |
| Meilleure réception / monitor longue portée | AWUS036AXER, AWUS036ACH | Saut de fréquence captant plus de cibles / forte gain à deux antennes |

Le choix en une phrase : pour jouer avec le mesh / IBSS, pour la concurrence VIF, et pour une exploitation sans pilote, l'AWUS036ACM est la carte mt76 la plus adaptée du lot ; pour une injection bi-bande à 100 %, orientez-vous vers l'EACS / ACH. Pour la comparaison transversale complète des neuf cartes et la décision de choix de modèle, voyez le [Hub d'évaluation des cartes Wi-Fi ALFA (tableau des neuf cartes)](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

---

## Questions fréquentes (FAQ)

**Q : L'AWUS036ACM nécessite-t-elle l'installation d'un pilote sous Ubuntu ou Kali ?**
Non. Le MT7612U est pris en charge par le pilote mt76x2u intégré au kernel : sous Ubuntu 24.04 (kernel 6.17), la carte est reconnue dès le branchement, sans DKMS ni flashage manuel de firmware. La plateforme de ce test est Ubuntu 24.04 ARM64 ; sous Kali, le comportement devrait être identique dès lors que le kernel est suffisamment récent, mais cela n'a pas été vérifié sur une machine Kali réelle cette fois-ci.

**Q : L'AWUS036ACM peut-elle passer en mode monitor et faire de l'injection de paquets ? Quel est le taux de réussite ?**
Oui. Le mode monitor et la capture fonctionnent correctement en 2,4 GHz comme en 5 GHz ; au test d'injection aireplay-ng, le taux est de 63–83 % en 2,4 GHz et de 76 % en 5 GHz, ce qui la situe en milieu de tableau parmi les neuf cartes. Pour une injection bi-bande à 100 %, les mesures Yopitek désignent l'AWUS036ACH et l'AWUS036EACS comme les meilleures.

**Q : L'AWUS036ACM peut-elle ouvrir un point d'accès tout en restant connectée à Internet (VIF) ?**
Oui. Les deux combinaisons STA+AP (connexion au réseau amont d'un côté, point d'accès de l'autre) et AP+monitor (point d'accès et écoute simultanés) ont été vérifiées. C'est là que la concurrence multi-interface du pilote mt76 est la plus complète ; le point d'accès 5 GHz peut monter jusqu'à VHT 80 MHz.

**Q : L'AWUS036ACM prend-elle en charge le mesh (802.11s) et l'IBSS ?**
Création en local possible. Sous Ubuntu 24.04 / kernel 6.17, l'AWUS036ACM peut créer des interfaces mesh 802.11s et IBSS (Ad-hoc) ; mais faute d'un second nœud cette fois-ci, l'interconnexion multi-nœuds n'a pas été vérifiée, donc on se limite à affirmer la création en local.

**Q : L'AWUS036ACM peut-elle capturer un handshake WPA ?**
Oui. Sur notre propre AP et notre propre iPhone 7 Plus, le test de bout en bout a réussi : deauth, capture complète des 4-way (M1–M4) et export hashcat .22000 avec hcxpcapngtool --all. Uniquement sur des réseaux dont vous êtes propriétaire ou autorisé.

---

## 6. Pour aller plus loin

- Comparaison complète des capacités et évaluation globale des neuf cartes ALFA → [Hub d'évaluation des cartes Wi-Fi ALFA (tableau des neuf cartes)](/fr/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Sans installation de pilote : activer Monitor / AP sous Ubuntu 24.04 + kernel 6.17 (tests rtw88 / rtw89 / mt76) (placeholder, lien en construction)
- Tutoriel pas à pas WPA3-SAE et capture de handshake de bout en bout (placeholder, lien en construction)
- Le modèle mono-antenne mt76 → test carte par carte de l'AWUS036ACHM (placeholder, lien en construction)

---

*Unité de test : Yopitek (distributeur ALFA Network à Taïwan) — https://www.yupitek.com | Environnement de test : ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Appareil de test : Apple iPhone 7 Plus (WPA3 aussi testé sur iPhone 15 Pro)*
