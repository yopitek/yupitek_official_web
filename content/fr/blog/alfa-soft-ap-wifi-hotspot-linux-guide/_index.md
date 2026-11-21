---
title: "Guide Complet Soft AP ALFA Network 2026 : Créer des Hotspots WiFi sur Kali Linux, Ubuntu, Debian & Raspberry Pi 4/5"
description: "Analyse approfondie du support Soft AP (hostapd/WiFi Hotspot) des adaptateurs USB WiFi ALFA Network sur Kali Linux, Ubuntu, Debian et Raspberry Pi 4/5. Guides de configuration complets pour AWUS036ACM, AWUS036ACH et AWUS036AXML."
date: 2026-05-21
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Soft-AP", "WiFi-Hotspot", "hostapd", "Kali-Linux", "Ubuntu", "Debian", "Raspberry-Pi", "AWUS036ACM", "AWUS036ACH", "AWUS036AXML", "MT7612U", "RTL8812AU", "MT7921AUN", "Linux-WiFi"]
featureimage: "/images/blog/alfa-soft-ap-wifi-hotspot-linux-guide.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "Les cartes USB ALFA peuvent-elles servir de point d'accès WiFi sous Linux ?"
    answer: "Selon le chipset. L'AWUS036ACM (MT7612U) supporte entièrement le Soft AP en plug-and-play, l'AWUS036ACH (RTL8812AU) le supporte avec conditions, et l'AWUS036AXML nécessite des ajustements."
  - question: "Quelle carte ALFA est la mieux adaptée pour un Soft AP sur Raspberry Pi ?"
    answer: "L'AWUS036ACM est le meilleur choix. Pilote intégré plug-and-play, consommation de 400 mA, support WPA3 et VIF, stabilité sur toutes les plateformes."
  - question: "Comment vérifier si la carte supporte le mode AP ?"
    answer: "Exécutez iw list | grep -A 10 'Supported interface modes'. Si la sortie inclut * AP, le pilote supporte le Soft AP et hostapd fonctionnera."
  - question: "Quelles sont les limitations du Soft AP avec le pilote RTL8812AU ?"
    answer: "Pas de support WPA3 (WPA2-PSK uniquement), pas de VIF (nécessite deux cartes), consommation d'environ 800 mA nécessitant un hub USB alimenté sur Pi."
  - question: "Que faire si le WiFi se déconnecte en mode Soft AP avec l'AWUS036AXML ?"
    answer: "Le Bluetooth 5.2 intégré au MT7921AUN interfère avec le WiFi. Désactivez le pilote Bluetooth avec echo 'install btusb /bin/false' dans /etc/modprobe.d/ puis redémarrez."
---

{{< tldr >}}
La compatibilité Soft AP des cartes ALFA dépend du pilote du chipset. L'AWUS036ACM est le choix stable polyvalent, l'AWUS036ACH fonctionne sans WPA3, l'AWUS036AXML nécessite la désactivation du Bluetooth. Le RTL8832BU (AX / AXER) fonctionne avec le pilote intégré à partir du noyau 6.17.
{{< /tldr >}}

> "Puis-je utiliser les adaptateurs USB WiFi ALFA comme hotspot WiFi (Soft AP) sur Kali Linux / Ubuntu / Raspberry Pi ?"




## Introduction

> "Puis-je utiliser les adaptateurs USB WiFi ALFA comme hotspot WiFi (Soft AP) sur Kali Linux / Ubuntu / Raspberry Pi ?"

C'est l'une des questions les plus fréquentes que nous recevons chez Yopitek. La question semble simple, mais la réponse varie considérablement selon le modèle et le chipset — **tous les adaptateurs USB WiFi ne peuvent pas fonctionner en mode Soft AP.**

Cet article rassemble plus de 500 discussions communautaires de GitHub (morrownr/USB-WiFi), des forums techniques Reddit, de la documentation officielle Raspberry Pi et des retours d'utilisateurs réels pour vous donner un rapport honnête et complet sur les adaptateurs ALFA qui fonctionnent, ceux qui ne fonctionnent pas, et le processus complet de configuration étape par étape.

---

## 1. Qu'est-ce que le Soft AP ? Comment ça fonctionne sous Linux {#what-is-softap}

**Soft AP (Software Access Point)** est la capacité de transformer un adaptateur USB WiFi ordinaire en station de base sans fil (Access Point) à l'aide d'un logiciel — principalement **hostapd**. Cela permet à d'autres appareils (téléphones, ordinateurs portables, équipements IoT) de se connecter au réseau sans acheter de routeur ou de matériel AP dédié.

Cette fonctionnalité est précieuse dans plusieurs scénarios :

- **Routeur de voyage / domicile** : En déplacement ou en camping, branchez un adaptateur ALFA sur votre ordinateur portable ou Raspberry Pi et créez instantanément un hotspot WiFi portable
- **Laboratoire de test d'intrusion** : Construisez un Rogue AP isolé pour la recherche en sécurité
- **Relais IoT** : Créez un répéteur dans les zones mortes pour que les capteurs IoT puissent transmettre des données
- **Déploiement Edge AI** : Environnements industriels sans réseau filaire — transformez l'appareil en hotspot pour connecter d'autres équipements
- **Communications d'urgence** : Mettez en place rapidement un réseau temporaire en cas de perte de connectivité

### Les quatre composants essentiels du Soft AP Linux

| Composant | Fonction |
|-----------|----------|
| **hostapd** | Le démon central qui crée l'Access Point — gère le SSID, l'authentification, le chiffrement |
| **nl80211** | L'interface standard du sous-système sans fil Linux — le pilote doit prendre en charge ce framework pour fonctionner avec hostapd |
| **dnsmasq** | Serveur DHCP qui attribue automatiquement des adresses IP aux clients connectés |
| **iptables / nftables** | Traduction d'adresses réseau (NAT) — permet aux clients connectés de partager le réseau amont |

### Concept clé : Mode Master

**Le Mode Master** (également appelé Mode AP ou Mode Infrastructure) est une capacité au niveau du pilote. Si le pilote ne prend pas en charge le Mode Master, hostapd ne peut tout simplement pas démarrer — peu importe la perfection de votre configuration.

Vérifiez la prise en charge du mode AP avec :

```bash
iw list | grep -A 10 "Supported interface modes"
```

Si la sortie inclut `* AP`, le pilote de l'adaptateur prend en charge le Soft AP. Sinon, cet adaptateur est inutilisable à cette fin.

### 💡 Pilotes In-kernel vs Out-of-kernel

C'est le concept **le plus important** lors du choix d'un adaptateur Soft AP :

| Type | Description | Impact sur le Soft AP |
|------|-------------|-------------------|
| **Pilote In-kernel** | Intégré dans l'arbre source officiel Linux ; se charge automatiquement au démarrage — aucune installation manuelle nécessaire | ✅ Stable à long terme ; survit aux mises à jour du noyau |
| **Pilote Out-of-kernel** | Doit être téléchargé depuis GitHub et compilé manuellement ; peut nécessiter une recompilation après chaque mise à jour du noyau | ⚠️ Peut casser après toute mise à jour du noyau |

**Pour une stabilité à long terme du Soft AP, les pilotes in-kernel sont largement supérieurs aux pilotes out-of-kernel.**

---

## 2. Gamme de produits ALFA et aperçu des chipsets {#product-lineup}

Voici la gamme actuelle de produits ALFA vendus par Yopitek, avec les chipsets et les évaluations préliminaires Soft AP :

| Modèle | Chipset | Type de pilote | Norme WiFi | Évaluation Soft AP |
|-------|---------|-------------|---------------|----------------|
| **AWUS036ACM** | MediaTek MT7612U | In-kernel (noyau 4.19+) | WiFi 5 AC1200 Double bande | ✅ Support complet |
| AWUS036ACH | Realtek RTL8812AU | Out-of-kernel (in-kernel à partir de 6.13+) | WiFi 5 AC1200 Double bande | ⚠️ Conditionnel |
| AWUS036AXML | MediaTek MT7921AUN | In-kernel (5.18+, mode AP 5.19+) | WiFi 6E AX3000 Triple bande | ⚠️ Partiel |
| AWUS036AXM | MediaTek MT7921AUN | In-kernel (idem ci-dessus) | WiFi 6E AX3000 Triple bande | ⚠️ Partiel |
| AWUS036AX | Realtek RTL8832BU | Intégré rtw89_8852bu (noyau 6.17+) ; noyaux antérieurs : pilote DKMS communautaire | WiFi 6 AX1800 Double bande | ✅ Fonctionne (noyau 6.17+) |
| AWUS036AXER | Realtek RTL8832BU | Intégré rtw89_8852bu (noyau 6.17+ ; idem AX) | WiFi 6 AX1800 Double bande | ✅ Fonctionne (noyau 6.17+) |

> **Remarque** : L'AWUS036ACHM (MT7610U) a été abandonné et n'est plus répertorié sur la page produit Yopitek. Cet article couvre uniquement les produits actuellement disponibles.

---

## 3. AWUS036ACM (MT7612U) — ⭐ Meilleure recommandation {#acm}

### Statut Soft AP : ✅ Support complet

Le MT7612U est le chipset Soft AP le plus stable de la gamme actuelle d'ALFA. Son pilote `mt76x2u` fait partie du noyau Linux officiel depuis 2018 (noyau 4.19), ce qui signifie qu'il fonctionne immédiatement sur tout système raisonnablement récent — **pas de `git clone`, pas de `dkms`, pas de recompilation après les mises à jour du noyau.**

### Avantages clés

- **Double prise en charge WPA2 + WPA3** : Le pilote in-kernel de MediaTek prend en charge nativement WPA3 SAE — un avantage que les pilotes Realtek ne peuvent égaler
- **Prise en charge VIF (Interface Virtuelle)** : Exécutez les modes AP + Managed + Monitor simultanément sur un seul adaptateur — pas besoin d'acheter une deuxième carte
- **Consommation ultra-faible** : Maximum ~400mA, parfait pour Raspberry Pi (le sous-système USB du Pi 4 ne fournit que 1200mA au total)
- **Multi-plateforme** : Largement vérifié sur Kali Linux 2022.x–2025.x, Ubuntu 22.04/24.04, Debian 11/12 et Raspberry Pi OS (Pi 3B+, 4, 5)

### Configuration correcte de hostapd (MT7612U)

Les flags de capacité suivants ont été vérifiés par des années de tests communautaires (morrownr/USB-WiFi). **Ils doivent correspondre exactement aux capacités matérielles réelles du MT7612U :**

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACM (MT7612U)
interface=wlan1
driver=nl80211
ssid=YourNetworkName
hw_mode=a                     # 5GHz; use g for 2.4GHz
channel=36                    # UNII-1, non-DFS, safest choice
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# MT7612U correct HT / VHT capabilities
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42    # Center frequency index for channel 36

# Security: WPA2 + WPA3 mixed mode
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK SAE       # WPA2 + WPA3 dual support
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=YourPassword
```

### ⚠️ Erreur la plus courante

Si `ht_capab` inclut des flags de capacité que le MT7612U ne prend pas réellement en charge, hostapd plantera silencieusement. **Utilisez uniquement la combinaison de flags vérifiée ci-dessus — ne copiez pas les paramètres d'autres chipsets comme le RTL8812AU.** (Source : [GitHub issue #2](https://github.com/morrownr/USB-WiFi/issues/2))

### Avis de la communauté

> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. I have tested the Alfa AWUS036ACM with many different computer systems and Linux distros. In my opinion, it is an outstanding USB WiFi adapter."
> *(Traduction : « L'Alfa AWUS036ACM fonctionne très bien avec le matériel Raspberry Pi. J'ai testé l'Alfa AWUS036ACM avec de nombreux systèmes informatiques et distributions Linux différents. À mon avis, c'est un adaptateur USB WiFi exceptionnel. »)*
> — **morrownr**, mainteneur de la base de connaissances communautaire Linux USB WiFi la plus autorisée sur GitHub

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> *(Traduction : « Cet adaptateur gère parfaitement le mode monitor et l'injection de paquets. Très stable sous Linux avec les noyaux natifs, sans besoin de compiler de pilotes externes. »)*
> — Avis d'utilisateur eBay

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> *(Traduction : « L'ACM est un peu plus polyvalent et plus facile à configurer en mode AP. »)*
> — Fil de discussion GitHub issue #2

---

## 4. AWUS036ACH (RTL8812AU) — Fonctionne, mais avec des compromis {#ach}

### Statut Soft AP : ⚠️ Support conditionnel

Le RTL8812AU est le chipset de test d'intrusion le plus emblématique d'ALFA et un favori de longue date de la communauté Kali Linux. Sa fonctionnalité Soft AP fonctionne — la création de hotspot de base est correcte — mais l'architecture de pilote out-of-kernel de Realtek impose plusieurs limitations persistantes :

### Limitations connues

1. **Pas de support WPA3** : Bien que le pilote RTL8812AU prétende prendre en charge WPA3, plusieurs utilisateurs ont confirmé qu'il ne fonctionne pas réellement. **WPA2-PSK uniquement.**
2. **Pas de support VIF** : Impossible d'exécuter les modes AP + Monitor simultanément sur la même carte. Si vous avez besoin d'AP et de monitoring, vous devez utiliser deux adaptateurs séparés.
3. **Problèmes de pilote Kali Linux 2025.x** : Le dernier pilote aircrack-ng/rtl8812au sur le Kali le plus récent a des problèmes de compatibilité — vous devez revenir à un ancien commit spécifique (`63cf0b4`). La situation peut s'améliorer avec le pilote in-kernel rtw88 du noyau 6.13+.
4. **Consommation élevée** : Maximum ~800mA — sur Raspberry Pi avec plusieurs périphériques USB connectés, cela peut causer une instabilité du système. Utilisez un hub USB alimenté.

### Configuration hostapd (RTL8812AU)

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACH (RTL8812AU)
# NOTE: Completely different capabilities from MT7612U!
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]

# Security: WPA2 only, do NOT add WPA3
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
```

### Installation du pilote (Kali Linux / Ubuntu / Debian)

```bash
sudo apt update && sudo apt install -y dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
# Kali 2025.x requires the older commit
git checkout 63cf0b4
make && sudo make install
sudo modprobe 88XXau
```

### Avis de la communauté

> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine."
> *(Traduction : « Je peux mettre un RTL8812AU (AWUS036AC) à la place et utiliser 'sudo service hostapd restart && sudo service dnsmasq restart', et cela a parfaitement fonctionné. »)*
> — Utilisateur de la GitHub issue #2

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> *(Traduction : « Adaptateurs basés sur le RTL8812AU — le mode AP fonctionne, mais vous perdez la prise en charge de WPA3 et VIF par rapport à MediaTek. »)*
> — Notes techniques de morrownr

### Verdict pour ACH

Si vous possédez déjà un AWUS036ACH, il peut servir de Soft AP (la fonction hotspot de base fonctionne). Mais si vous n'avez pas encore acheté et que votre objectif principal est le Soft AP, **optez plutôt pour l'ACM.**

---

## 5. AWUS036AXML / AWUS036AXM (MT7921AUN) — À utiliser avec prudence {#axml}

### Statut Soft AP : ⚠️ Support partiel — Problèmes connus de firmware/pilote

L'AWUS036AXML et l'AWUS036AXM sont les modèles phares tri-bande WiFi 6E d'ALFA, couvrant les bandes 2.4 GHz, 5 GHz et la nouvelle bande 6 GHz. Leur pilote in-kernel `mt7921u` est présent dans le noyau depuis la version 5.18, avec la prise en charge du mode AP officiellement ajoutée en 5.19. Cependant, la puce MT7921AUN intègre aussi le Bluetooth 5.2 — devenu le casse-tête n° 1 de la communauté en 2024–2025.

### Jalons de version du noyau pour le mode AP

| Mode | Noyau minimum |
|------|---------------|
| Managed (WiFi normal) | 5.18+ |
| **Mode AP (Soft AP)** | **5.19+** |
| AP/VLAN | 5.19+ |
| P2P-GO (Wi-Fi Direct AP) | 6.4+ |

### Problèmes connus et solutions

#### Problème 1 : Interférence Bluetooth provoquant des crashs WiFi

Sur les noyaux 6.6+, des changements dans le sous-système BT provoquent des crashs WiFi sporadiques avec mt7921u. La reproductibilité varie selon l'environnement système. **Le contournement le plus efficace consiste à désactiver le pilote btusb :**

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

#### Problème 2 : Firmware obsolète

Si le firmware MediaTek du système est trop ancien, l'adaptateur peut ne pas être reconnu correctement. Installez le firmware de novembre 2024 ou plus récent :

```bash
# Check current firmware version
dmesg | grep "WM Firmware"
# Should show: Build Time: 20241106151045 or newer

# If outdated, download from kernel.org
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek/
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek/
sudo reboot
```

#### Problème 3 : Exigences de version hostapd

Certains utilisateurs rapportent devoir compiler hostapd depuis git pour un support complet du mode AP WiFi 6. Les versions fournies par le gestionnaire de paquets du système peuvent être incomplètes.

#### Problème 4 : Anomalie d'affichage de la puissance Tx en mode AP

`iw` n'affiche que 3 dBm sans ajustement possible, mais la puce a en réalité un amplificateur interne — c'est un problème d'affichage du pilote du noyau, pas une limitation matérielle.

#### Problème 5 : Problèmes de mode Monitor sur certaines versions du noyau

En décembre 2025, le noyau 6.18 et certaines versions antérieures du pilote mt7921u ont des problèmes de mode monitor.

### Avis de la communauté

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> *(Traduction : « J'ai un Alfa AXML qui tourne en AP sur un hôte RPi3B sous ArchLinux ARM aarch64. C'est le mt7921 le plus stable de ma collection. J'utilise toutefois hostapd compilé depuis git. »)*
> — **fhteagle**, [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

### Verdict pour AXML/AXM

Choisissez-les si vous avez besoin de la bande 6 GHz du WiFi 6E et êtes prêt à ajuster occasionnellement les paramètres. **Pour les environnements de production nécessitant une stabilité Soft AP à toute épreuve, choisissez plutôt l'ACM.**

---

## 6. AWUS036AX / AWUS036AXER (RTL8832BU) — Utilisable en Soft AP à partir du noyau 6.17 {#ax}

### Statut Soft AP : ✅ Fonctionne à partir du noyau 6.17 (les noyaux plus anciens nécessitent le pilote DKMS communautaire)

Lors de nos tests sur un ASUS GX10 (Ubuntu 24.04 ARM64, noyau 6.17) avec le pilote intégré `rtw89_8852bu`, l'AWUS036AX et l'AWUS036AXER (même puce, même pilote) se comportent de façon identique, et le Soft AP fonctionne en 2,4 GHz comme en 5 GHz.

**Résultats des tests (noyau 6.17) :**

1. **Mode AP** : 2,4 GHz (802.11n) et 5 GHz (VHT 80 MHz) fonctionnent tous deux
2. **VIF (STA + AP)** : fonctionne — une connexion cliente et une interface AP tournent en parallèle sur le même canal
3. **AP WPA3-SAE** : fonctionne en 2,4 GHz (iPhone 15 Pro connecté, MFP activé ; 5 GHz non testé)
4. **Monitor / injection** : réception monitor forte en 2,4 et 5 GHz ; injection en 2,4 GHz AX 96 % / AXER 73 %, 5 GHz utilisable ; une capture de handshake WPA de bout en bout a réussi
5. **Non pris en charge** : IBSS, Mesh, active monitor

**Points d'attention :**

- **La version du noyau est un prérequis** : `rtw89_8852bu` est intégré au noyau à partir de la 6.17. Les noyaux plus anciens nécessitent le pilote DKMS communautaire (rtl8852bu), avec lequel le mode monitor peut être limité et le VIF n'est pas pris en charge.
- **Mode USB** : certaines unités peuvent s'énumérer en mode CD-ROM (`0bda:1a2b`) et nécessiter `usb_modeswitch -v 0bda -p 1a2b -K` ; notre unité de test s'est énumérée directement comme adaptateur WLAN.
- **Cas communautaires** : les retours Soft AP pour ce chipset restent moins nombreux que pour le MT7612U et le RTL8812AU.

> Résultat des tests Yopitek (ASUS GX10, noyau 6.17) : avec le pilote intégré, l'AWUS036AX / AWUS036AXER offrent une forte réception monitor et une injection de paquets fonctionnelle, et sont donc aussi utilisables pour les tests d'intrusion. Le support monitor limité ne concerne que les noyaux plus anciens utilisant le pilote DKMS communautaire.
>
> Complément : avec le noyau stock 6.16 et ultérieur (6.17 testé), l'AWUS036AXML fonctionne en mode monitor, AP, WPA3 et VIF, mais le test d'injection de paquets a échoué (aireplay-ng --test : Found 0 APs / No Answer). La cause est une régression mac80211 chanctx, et non la puce elle-même. Pour l'injection, utilisez plutôt l'AWUS036ACH, l'EACS, l'ACS ou l'AX.

---

## 7. Matrice de compatibilité des plateformes {#compat-matrix}

### AWUS036ACM (MT7612U)

| Plateforme | Soft AP | Remarques |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ✅ | Pilote in-kernel, plug-and-play, noyau 5.x / 6.x |
| Ubuntu 22.04 / 24.04 | ✅ | In-kernel, aucune configuration, utilisez une LTS |
| Debian 11 / 12 | ✅ | Pilote in-kernel, stable |
| Raspberry Pi 4 (RPi OS) | ✅ | Consommation la plus faible (400mA), vérifié sur le long terme par morrownr. Port USB 3.0 du Pi 4 recommandé |
| Raspberry Pi 5 (RPi OS) | ✅ | Même pilote que le Pi 4, stable |

### AWUS036ACH (RTL8812AU)

| Plateforme | Soft AP | Remarques |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ⚠️ | Pilote externe requis ; 2025.x nécessite le commit `63cf0b4`. rtw88 du noyau 6.13+ pourrait améliorer la situation |
| Ubuntu 22.04 / 24.04 | ⚠️ | Installation manuelle du pilote rtw88 ou aircrack-ng parfois nécessaire |
| Debian 11 / 12 | ⚠️ | Idem ci-dessus |
| Raspberry Pi 4 | ⚠️ | Fonctionne, mais consommation élevée (800mA) ; utilisez un hub USB alimenté |
| Raspberry Pi 5 | ⚠️ | Idem ; les différences du contrôleur USB du Pi 5 peuvent affecter le comportement |

### AWUS036AXML / AWUS036AXM (MT7921AUN)

| Plateforme | Soft AP | Remarques |
|----------|---------|-------|
| Kali Linux 2022.x (noyau 5.18+) | ✅ | Désactivez btusb, mettez à jour le firmware |
| Kali Linux 2024.x / 2025.x | ⚠️ | Conflit BT/WiFi sur noyau 6.11+, instable |
| Ubuntu 24.04 (noyau 6.8+) | ⚠️ | Problèmes signalés fin 2024 |
| Ubuntu 25.04 / CachyOS (noyau 6.14+) | ✅ | Plug-and-play, nette amélioration avec les nouveaux noyaux |
| Debian 12 | ⚠️ | Dépend de la version du noyau |
| Raspberry Pi 4 / 5 | ⚠️ | Des cas de succès existent, mais vérifiez le firmware et désactivez le BT |

### AWUS036AX / AWUS036AXER (RTL8832BU)

| Plateforme | Soft AP | Remarques |
|----------|---------|-------|
| Kali Linux | ✅ | rtw89_8852bu intégré à partir du noyau 6.17 ; noyaux plus anciens : pilote DKMS communautaire |
| Ubuntu / Debian | ✅ | Ubuntu 24.04 nécessite le noyau HWE 6.17+ (GA 6.8 / HWE 6.14 : pilote DKMS communautaire) ; Debian nécessite un noyau 6.17+ |
| Raspberry Pi 4 / 5 | ⚠️ | Non testé sur Pi ; les noyaux inférieurs à 6.17 nécessitent le pilote DKMS communautaire |

---

## 8. Guide complet de configuration Soft AP (AWUS036ACM) {#setup-guide}

Voici un guide complet, étape par étape, pour configurer un Soft AP 5GHz avec l'AWUS036ACM sur Raspberry Pi 4.

### Étape 1 : Vérifier la détection de l'adaptateur et le pilote

```bash
# Confirm the adapter is detected
lsusb | grep MediaTek
# Expected: Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U

# Check driver loaded
dmesg | grep mt76
# Expected: mt76x2u 1-1.4:1.0 wlx00c0ca9821a5: renamed from wlan0

# Confirm AP mode support
iw list | grep -A 10 "Supported interface modes"
# Check that output includes "* AP"
```

### Étape 2 : Installer les paquets requis

```bash
sudo apt update
sudo apt install -y hostapd dnsmasq iptables
```

### Étape 3 : Configurer hostapd

Créez `/etc/hostapd/hostapd.conf` :

```ini
interface=wlan0
driver=nl80211
ssid=Yupitek_AP
hw_mode=a                       # a=5GHz, g=2.4GHz
channel=36                      # UNII-1, non-DFS, safest choice
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# HT/VHT settings (MT7612U specific)
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42

# WPA2 + WPA3 mixed mode
wpa=2
wpa_passphrase=MySecurePassword123
wpa_key_mgmt=WPA-PSK SAE
wpa_pairwise=CCMP
rsn_pairwise=CCMP

auth_algs=1
macaddr_acl=0
ignore_broadcast_ssid=0
```

### Étape 4 : Configurer dnsmasq (DHCP)

Créez `/etc/dnsmasq.conf` :

```ini
interface=wlan0
dhcp-range=192.168.10.2,192.168.10.100,255.255.255.0,12h
dhcp-option=3,192.168.10.1
dhcp-option=6,8.8.8.8,8.8.4.4
```

### Étape 5 : Définir l'IP statique et le NAT

```bash
# Assign static IP to wlan0
sudo ip addr add 192.168.10.1/24 dev wlan0

# Enable IP forwarding
sudo sysctl net.ipv4.ip_forward=1

# Configure NAT (assuming eth0 is the upstream interface)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Persist iptables rules
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```

### Étape 6 : Démarrer les services

```bash
sudo systemctl unmask hostapd
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# Check service status
sudo systemctl status hostapd
sudo systemctl status dnsmasq

# Enable auto-start on boot
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```

Une fois terminé, recherchez le WiFi sur votre téléphone ou ordinateur portable — vous devriez voir le SSID `Yupitek_AP`.

---

## 9. Dépannage courant {#troubleshooting}

### Q1 : hostapd plante immédiatement au démarrage

**Symptôme** : `sudo systemctl status hostapd` affiche `exited` ou `failed`

**Cause probable** : `hostapd.conf` contient des flags de capacité que le chipset ne prend pas en charge

**Solution** : Supprimez les flags superflus. Pour le MT7612U (ACM), l'approche la plus sûre consiste à utiliser la configuration vérifiée de la section 3. **Ne copiez pas le ht_capab d'autres chipsets.**

---

### Q2 : Les clients se connectent mais ne peuvent pas accéder à Internet

**Symptôme** : WiFi connecté, IP obtenue, mais `ping 8.8.8.8` n'obtient aucune réponse

**Liste de vérification** :

```bash
# 1. Check IP forwarding enabled
cat /proc/sys/net/ipv4/ip_forward
# Should output: 1

# 2. Check NAT rules exist
sudo iptables -t nat -L POSTROUTING -v
# Should see MASQUERADE rule

# 3. Confirm upstream interface is working
ping -I eth0 8.8.8.8
```

---

### Q3 : AP 5GHz non visible ou instable

**Causes possibles** :

1. **Utilisation de canaux DFS (100–144)** : MT7612U / MT7610U ne prennent pas en charge le DFS — utilisez les canaux UNII-1 (36–48)
2. **Puissance d'émission insuffisante** : vérifiez que les antennes sont bien serrées sur les connecteurs RP-SMA
3. **Alimentation USB insuffisante** (Raspberry Pi) : utilisez l'alimentation officielle 5A ou un hub USB alimenté

---

### Q4 : hostapd redémarre constamment sur Raspberry Pi

**Symptôme** : `dmesg` affiche de fréquents messages de réinitialisation USB

**Cause probable** : alimentation insuffisante du port USB (notamment avec le chipset gourmand de l'AWUS036ACH, 800mA max.)

**Solution** :
- Utilisez l'alimentation officielle 5A du Pi
- Utilisez un hub USB alimenté
- Branchez l'adaptateur sur un port USB 3.0 (Pi 4 uniquement)

---

### Q5 : Le WiFi de l'AWUS036AXML/AXM chute soudainement ou ne démarre pas

**Cause probable** : le sous-système Bluetooth interfère avec le WiFi (le MT7921AUN intègre le BT 5.2)

**Solution** : désactivez définitivement le pilote Bluetooth

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## 10. Analyse technique approfondie : VIF, WPA3, Canaux DFS {#technical}

### VIF (Interface Virtuelle) : Une carte, plusieurs rôles

VIF (Virtual Interface) permet à un seul adaptateur physique de fonctionner avec plusieurs interfaces logiques simultanément. Par exemple : une interface se connecte au routeur amont (mode managed) tandis qu'une autre sert d'AP (mode master) pour d'autres appareils.

Trois scénarios courants :

| Scénario | VIF requis ? | Meilleur adaptateur |
|----------|--------------|--------------|
| Routage NAT basique (eth0 en amont + wlan AP) | ❌ Non | Tout adaptateur compatible AP |
| Pont sans fil (réception WiFi + WiFi AP simultanément) | ✅ Oui | ACM (MT7612U) |
| Monitor + AP simultanément (recherche en sécurité / Rogue AP) | ✅ Oui | ACM (MT7612U) |

**Exemple pratique de VIF (MT7612U) :**

```bash
# Create an additional AP virtual interface alongside existing wlan1
sudo iw phy phy1 interface add ap0 type __ap
sudo ip link set ap0 up
# Now wlan1 can connect upstream while ap0 runs hostapd
```

Seuls les pilotes in-kernel MediaTek (mt76x2u, mt7921u) prennent entièrement en charge le VIF. Les pilotes out-of-kernel Realtek n'ont pratiquement pas cette capacité — si vous avez besoin d'AP + Monitor simultanément, vous devez utiliser deux adaptateurs séparés.

---

### Comparaison du support WPA3

| Chipset | Modèle correspondant | WPA2 | WPA3 |
|---------|-------------------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ Prise en charge native de SAE |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ Prise en charge native de SAE |
| RTL8812AU | AWUS036ACH | ✅ | ❌ Prise en charge annoncée mais non fonctionnelle |
| RTL8832BU | AWUS036AX / AXER | ✅ | ✅ Testé sur le noyau 6.17 (`sae_pwe=0`, MFP activé) |

---

### Sélection des canaux Soft AP 5GHz : Éviter DFS

Les canaux DFS (Dynamic Frequency Selection) (ch100–ch140) nécessitent une détection radar au niveau du noyau. Le MT7612U et les chipsets similaires n'ont pas de support DFS. Pour le mode AP 5GHz, choisissez :

| Bande | Canaux recommandés | Raison |
|------|---------------------|--------|
| **UNII-1** | **36, 40, 44, 48** | Tous les chipsets pris en charge ; choix le plus sûr |
| UNII-2 (DFS) | 52–144 | La plupart non pris en charge ; non recommandé |
| UNII-3 | 149–165 | Support partiel (selon la région) |

---

## 11. Cas réels de la communauté {#real-cases}

### Cas 1 : RPi4B + AWUS036ACM = AP domestique 5GHz stable à long terme

**Source** : base de connaissances GitHub morrownr/7612u
**Scénario** : morrownr utilise depuis longtemps un RPi4B + AWUS036ACM comme AP domestique 5GHz, associé au 2.4GHz intégré du Pi pour un service double bande
**Résultat** : fonctionnement stable à long terme, aucun redémarrage nécessaire, jugé « exceptionnel »
**Configuration** : hostapd + dnsmasq + iptables NAT

### Cas 2 : RPi3B+ + ACM — Crash initial, corrigé

**Source** : [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
**Problème** : hostapd plantait lorsqu'il fonctionnait via USB 2.0 sur RPi3B+
**Cause racine** : `ht_capab` contenait des flags HT40 non pris en charge dans les limites de bande passante de l'USB 2.0
**Solution** : suppression des flags superflus ; lancement réussi sous Kali Linux

### Cas 3 : Pi PwnBox + AWUS036ACH = Rogue AP Red Team

**Source** : GitHub koutto/pi-pwnbox-rogueap
**Scénario** : plateforme Rogue AP sur RPi3B+ : un RTL8812AU (AWUS036ACH) pour l'AP, un autre RT3070 (AWUS036NEH) pour les attaques par injection de paquets
**Constat clé** : le RTL8812AU ne prenant pas en charge le VIF, deux adaptateurs séparés ont été nécessaires (contrairement à l'ACM, qui gère les deux sur une seule carte)

### Cas 4 : AWUS036AXML AP stable sur RPi3B ArchLinux ARM

**Source** : [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
**Scénario** : un utilisateur a fait fonctionner avec succès l'AWUS036AXML en mode AP sur RPi3B sous ArchLinux aarch64
**Citation** : « C'est le mt7921 le plus stable de ma collection. »
**Prérequis clés** : hostapd compilé depuis git + btusb désactivé

### Cas 5 : AWUS036ACHM (MT7610U, abandonné) AP pleine vitesse sur Pi4

**Source** : [GitHub Discussion #31](https://github.com/morrownr/USB-WiFi/discussions/31)
**Problème** : la configuration initiale n'atteignait qu'un débit de liaison de 65 Mbps, bien en dessous du plein débit AC en 5GHz
**Solution** : ajout des paramètres corrects `vht_oper_chwidth=1` et `vht_oper_centr_freq_seg0_idx` ; débit de liaison de 433 Mbps atteint
**Pertinence pour l'ACM** : la même configuration des paramètres VHT est également essentielle pour le MT7612U (ACM)

---

{{< faq >}}

## 12. Recommandations d'achat et verdict final {#recommendations}

### Matrice de décision rapide

| Évaluation | Modèle | Idéal pour | En un mot |
|--------|-------|----------|-----------|
| 🥇 **Premier choix** | **AWUS036ACM** | Tout le monde, surtout les débutants Soft AP | Stable toutes plateformes, zéro tracas |
| 🥈 Utilisable | AWUS036ACH | Utilisateurs possédant déjà ce modèle | Nécessite un pilote, pas de WPA3 |
| 🥉 Avancé | AWUS036AXML | Utilisateurs ayant besoin du WiFi 6E prêts à bricoler | Avantage 6GHz, corrections manuelles nécessaires |
| ✅ Fonctionne à partir du noyau 6.17 | AWUS036AX / AXER | AP Wi-Fi 6 ; monitor et injection également utilisables | Pilote intégré ; AP 2,4 / 5 GHz et VIF testés, WPA3 testé en 2,4 GHz |

### 🎯 Guide de décision

- **Besoin d'un Soft AP stable sur Kali / Ubuntu / Debian / Raspberry Pi 4 ou 5 ?**
  → Prenez l'**AWUS036ACM**, sans hésitation.

- **Vous possédez déjà un AWUS036ACH et voulez essayer le Soft AP ?**
  → Ça fonctionne, mais uniquement WPA2, et vous devrez installer le pilote. Si vous acceptez ces limites, allez-y.

- **Besoin du WiFi 6E (bande 6 GHz) et prêt à configurer ?**
  → AWUS036AXML — n'oubliez pas de désactiver le pilote BT et de vérifier le noyau ≥ 6.6 LTS.

- **Objectif principal est le Soft AP, pas le test d'intrusion ?**
  → L'AWUS036ACM est le seul choix avec une vérification communautaire étendue sur toutes les plateformes.

---

### Conclusion

Le facteur central dans la construction d'un Soft AP n'est pas la vitesse WiFi ou le nombre d'antennes — **c'est la prise en charge du mode AP par le pilote du chipset.**

Parmi tous les produits ALFA que nous avons étudiés, l'**AWUS036ACM (MT7612U)** est le seul adaptateur qui satisfait simultanément : pilote in-kernel, WPA3 natif, interfaces virtuelles VIF, faible consommation et stabilité multi-plateforme. C'est l'étalon-or du Soft AP.

L'AWUS036ACH (RTL8812AU) fonctionne si vous acceptez les limitations. L'AWUS036AXML/AXM (MT7921AUN) a un grand potentiel mais la maturité du pilote est encore en cours. L'AWUS036AX/AXER (RTL8832BU) fonctionne bien à partir du noyau 6.17 avec le pilote intégré (AP et VIF testés, WPA3 testé en 2,4 GHz) ; les noyaux plus anciens nécessitent le pilote DKMS communautaire.

**Si c'est votre première configuration d'un Soft AP sur Raspberry Pi ou Kali Linux — choisissez l'ACM. Vous ne le regretterez pas.**

---

### Liens d'achat

- [AWUS036ACM — Premier choix pour le Soft AP](/fr/products/alfa/awus036acm/)
- [AWUS036ACH — L'adaptateur de pentest classique](/fr/products/alfa/awus036ach/)
- [AWUS036AXML — Le modèle phare tri-bande WiFi 6E](/fr/products/alfa/awus036axml/)
- [Gamme complète ALFA Network](/fr/products/alfa/)

### Lectures complémentaires

- [AWUS036ACH vs AWUS036ACM : comparaison complète des pilotes de chipset](/en/blog/awus036ach-vs-awus036acm/)
- [AWUS036ACM : IBSS et Mesh sur Raspberry Pi](/en/blog/)
- [morrownr/USB-WiFi — La base de connaissances de référence sur Linux USB WiFi](https://github.com/morrownr/USB-WiFi) (plus de 4,100 étoiles)
- [morrownr/7612u — Référence MT7612U (avec tutoriel Bridged AP sur RPi4B)](https://github.com/morrownr/7612u)
- [DeepWiki — Base de connaissances morrownr/USB-WiFi organisée automatiquement](https://deepwiki.com/morrownr/USB-WiFi)

---

### 📚 Sources de données

Cet article rassemble des informations provenant de :
- Base de connaissances GitHub **morrownr/USB-WiFi** (plus de 4,100 étoiles) avec des relevés iw_list complets
- **morrownr/7612u** — tutoriel Bridged AP MT7612U sur RPi4B
- **Suivi des issues GitHub** — issue #2 (configuration AP de l'ACM), #476 (tests AP de l'AXML), Discussion #31 (AP pleine vitesse de l'ACHM)
- **koutto/pi-pwnbox-rogueap** — cas d'implémentation RogueAP avec un adaptateur Alfa
- Pages de support Linux du revendeur **Rokland**
- Tests techniques de **Lab401** et sélections des meilleurs choix pentest 2025
- **Forum officiel Raspberry Pi** — discussions sur la compatibilité USB WiFi des Pi 4/5
- **Blog Yopitek** — guide d'installation de l'ACM en Chine, test de l'AXML WiFi 6E, meilleurs adaptateurs Kali Linux 2026

---

> **Étiquettes** : #ALFANetwork #SoftAP #WiFiHotspot #hostapd #KaliLinux #Ubuntu #Debian #RaspberryPi #AWUS036ACM #AWUS036ACH #AWUS036AXML #MT7612U #RTL8812AU #MT7921AUN #Yopitek
>
> **Auteur** : Yopitek Ltd — Distributeur Agréé ALFA Network Taiwan
>
> **Avertissement** : Données de recherche à jour en mai 2026. Les noyaux Linux et les distributions continuent d'évoluer ; la prise en charge des pilotes peut changer avec les nouvelles versions. Vérifiez la version du noyau et la compatibilité du pilote sur la plateforme cible avant tout déploiement.
>
> **Support technique** : Pour les problèmes de configuration Soft AP, contactez le support technique Yopitek Taiwan. Demandes de produits : [yupitek.com](https://yupitek.com/fr/).

---

## Références
1. [Base de connaissances GitHub morrownr/USB-WiFi](https://github.com/morrownr/USB-WiFi)
2. [Documentation officielle hostapd](https://w1.fi/cgit/hostap/)
3. [Pilote mt76 Linux Wireless](https://wireless.wiki.kernel.org/en/users/Drivers/mt76)
4. [Documentation officielle Raspberry Pi](https://www.raspberrypi.com/documentation/)
5. [Documentation officielle Kali Linux](https://www.kali.org/docs/)
