---
title: "Guide Complet Soft AP ALFA Network 2026 : Créer des Hotspots WiFi sur Kali Linux, Ubuntu, Debian & Raspberry Pi 4/5"
description: "Analyse approfondie du support Soft AP (hostapd/WiFi Hotspot) des adaptateurs USB WiFi ALFA Network sur Kali Linux, Ubuntu, Debian et Raspberry Pi 4/5. Guides de configuration complets pour AWUS036ACM, AWUS036ACH et AWUS036AXML."
date: 2026-05-21
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Soft-AP", "WiFi-Hotspot", "hostapd", "Kali-Linux", "Ubuntu", "Debian", "Raspberry-Pi", "AWUS036ACM", "AWUS036ACH", "AWUS036AXML", "MT7612U", "RTL8812AU", "MT7921AUN", "Linux-WiFi"]
---



# Guide Complet Soft AP ALFA Network 2026 : Créer des Hotspots WiFi sur Kali Linux, Ubuntu, Debian & Raspberry Pi 4/5

## Introduction

> "Puis-je utiliser les adaptateurs USB WiFi ALFA comme hotspot WiFi (Soft AP) sur Kali Linux / Ubuntu / Raspberry Pi ?"

C'est l'une des questions les plus fréquentes que nous recevons chez Yupitek. La question semble simple, mais la réponse varie considérablement selon le modèle et le chipset — **tous les adaptateurs USB WiFi ne peuvent pas fonctionner en mode Soft AP.**

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

| Component | Function |
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

| Type | Description | Impact on Soft AP |
|------|-------------|-------------------|
| **Pilote In-kernel** | Intégré dans l'arbre source officiel Linux ; se charge automatiquement au démarrage — aucune installation manuelle nécessaire | ✅ Stable à long terme ; survit aux mises à jour du noyau |
| **Pilote Out-of-kernel** | Doit être téléchargé depuis GitHub et compilé manuellement ; peut nécessiter une recompilation après chaque mise à jour du noyau | ⚠️ Peut casser après toute mise à jour du noyau |

**Pour une stabilité à long terme du Soft AP, les pilotes in-kernel sont largement supérieurs aux pilotes out-of-kernel.**

---

## 2. Gamme de produits ALFA et aperçu des chipsets {#product-lineup}

Voici la gamme actuelle de produits ALFA vendus par Yupitek, avec les chipsets et les évaluations préliminaires Soft AP :

| Modèle | Chipset | Type de pilote | Norme WiFi | Évaluation Soft AP |
|-------|---------|-------------|---------------|----------------|
| **AWUS036ACM** | MediaTek MT7612U | In-kernel (noyau 4.19+) | WiFi 5 AC1200 Double bande | ✅ Support complet |
| AWUS036ACH | Realtek RTL8812AU | Out-of-kernel (in-kernel à partir de 6.14+) | WiFi 5 AC1200 Double bande | ⚠️ Conditionnel |
| AWUS036AXML | MediaTek MT7921AUN | In-kernel (5.18+, mode AP 5.19+) | WiFi 6E AX3000 Triple bande | ⚠️ Partiel |
| AWUS036AXM | MediaTek MT7921AUN | In-kernel (idem ci-dessus) | WiFi 6E AX3000 Triple bande | ⚠️ Partiel |
| AWUS036AX | Realtek RTL8832BU | Out-of-kernel (noyau 6.12+ recommandé) | WiFi 6 AX1800 Double bande | ❌ Non recommandé |
| AWUS036AXER | Realtek RTL8832BU | Out-of-kernel (idem ci-dessus) | WiFi 6 AX1800 Double bande | ❌ Non recommandé |

> **Remarque** : L'AWUS036ACHM (MT7610U) a été abandonné et n'est plus répertorié sur la page produit Yupitek. Cet article couvre uniquement les produits actuellement disponibles.

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
> — **morrownr**, mainteneur de la base de connaissances communautaire Linux USB WiFi la plus autorisée sur GitHub

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> — Avis d'utilisateur eBay

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> — Fil de discussion GitHub issue #2

---

## 4. AWUS036ACH (RTL8812AU) — Fonctionne, mais avec des compromis {#ach}

### Statut Soft AP : ⚠️ Support conditionnel

Le RTL8812AU est le chipset de test d'intrusion le plus emblématique d'ALFA et un favori de longue date de la communauté Kali Linux. Sa fonctionnalité Soft AP fonctionne — la création de hotspot de base est correcte — mais l'architecture de pilote out-of-kernel de Realtek impose plusieurs limitations persistantes :

### Limitations connues

1. **Pas de support WPA3** : Bien que le pilote RTL8812AU prétende prendre en charge WPA3, plusieurs utilisateurs ont confirmé qu'il ne fonctionne pas réellement. **WPA2-PSK uniquement.**
2. **Pas de support VIF** : Impossible d'exécuter les modes AP + Monitor simultanément sur la même carte. Si vous avez besoin d'AP et de monitoring, vous devez utiliser deux adaptateurs séparés.
3. **Problèmes de pilote Kali Linux 2025.x** : Le dernier pilote aircrack-ng/rtl8812au sur le Kali le plus récent a des problèmes de compatibilité — vous devez revenir à un ancien commit spécifique (`63cf0b4`). La situation peut s'améliorer avec le pilote in-kernel rtw88 du noyau 6.14+.
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
> — GitHub issue #2 user

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> — morrownr technical notes

### Verdict pour ACH

Si vous possédez déjà un AWUS036ACH, il peut servir de Soft AP (la fonction hotspot de base fonctionne). Mais si vous n'avez pas encore acheté et que votre objectif principal est le Soft AP, **optez plutôt pour l'ACM.**

---

## 5. AWUS036AXML / AWUS036AXM (MT7921AUN) — À utiliser avec prudence {#axml}

### Statut Soft AP : ⚠️ Support partiel — Problèmes connus de firmware/pilote

The AWUS036AXML and AWUS036AXM are ALFA's WiFi 6E tri-band flagships, covering 2.4 GHz, 5 GHz, and the new 6 GHz band. Their in-kernel driver `mt7921u` has been in the kernel since version 5.18, with AP mode support officially added in 5.19. However, the MT7921AUN chip also integrates Bluetooth 5.2 — which became the #1 community headache in 2024–2025.

### Jalons de version du noyau pour le mode AP

| Mode | Minimum Kernel |
|------|---------------|
| Managed (normal WiFi) | 5.18+ |
| **AP Mode (Soft AP)** | **5.19+** |
| AP/VLAN | 5.19+ |
| P2P-GO (Wi-Fi Direct AP) | 6.4+ |

### Problèmes connus et solutions

#### Problème 1 : Interférence Bluetooth provoquant des crashs WiFi

On kernels 6.6+, changes to the BT subsystem cause sporadic WiFi crashes with mt7921u. Reproducibility varies by system environment. **The most effective workaround is to disable the btusb driver:**

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

Certains utilisateurs rapportent devoir compiler hostapd depuis git pour un support complet du mode AP WiFi 6. System package manager versions may be incomplete.

#### Problème 4 : Anomalie d'affichage de la puissance Tx en mode AP

`iw` n'affiche que 3 dBm sans ajustement possible, mais la puce a en réalité un amplificateur interne — c'est un problème d'affichage du pilote du noyau, pas une limitation matérielle.

#### Problème 5 : Problèmes de mode Monitor sur certaines versions du noyau

En décembre 2025, le noyau 6.18 et certaines versions antérieures du pilote mt7921u ont des problèmes de mode monitor.

### Community Review

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> — **fhteagle**, [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

### Verdict pour AXML/AXM

Choisissez-les si vous avez besoin de la bande 6 GHz du WiFi 6E et êtes prêt à ajuster occasionnellement les paramètres. **Pour les environnements de production nécessitant une stabilité Soft AP à toute épreuve, choisissez plutôt l'ACM.**

---

## 6. AWUS036AX / AWUS036AXER (RTL8832BU) — Non recommandé pour le Soft AP {#ax}

### Statut Soft AP : ❌ Non recommandé

Bien qu'ils soient des adaptateurs WiFi 6, la puce RTL8832BU est un dispositif "multi-state" — elle s'énumère comme stockage de masse USB par défaut, nécessitant un USB mode switch sous Linux avant de fonctionner comme adaptateur sans fil.

**Problèmes clés :**

1. **Dispositif multi-state** : Ajoute de la complexité au déploiement — n'apparaît pas comme adaptateur réseau au branchement
2. **Limitations du mode Monitor** : Support incomplet en dessous du noyau 6.14
3. **Cas communautaires Soft AP minimes** : Presque aucun cas réel de Soft AP RTL8832BU n'existe, compared to abundant MT7612U and RTL8812AU examples
4. **La documentation communautaire le déconseille explicitement**: morrownr/USB-WiFi marks this chipset as "not recommended for penetration testing"

> La documentation officielle de Yupitek indique clairement : « L'AWUS036AX / AWUS036AXER avec chipset RTL8832BU a un support limité du mode monitor en dessous du noyau 6.14 et n'est pas recommandé pour les tests d'intrusion. Utilisez plutôt l'AWUS036ACH ou l'AWUS036AXML. »

---

## 7. Matrice de compatibilité des plateformes {#compat-matrix}

### AWUS036ACM (MT7612U)

| Platform | Soft AP | Notes |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ✅ | In-kernel, plug-and-play, kernel 5.x / 6.x |
| Ubuntu 22.04 / 24.04 | ✅ | In-kernel, zero config, use LTS |
| Debian 11 / 12 | ✅ | In-kernel, stable |
| Raspberry Pi 4 (RPi OS) | ✅ | Lowest power (400mA), long-term morrownr verification. Pi 4 USB 3.0 port preferred |
| Raspberry Pi 5 (RPi OS) | ✅ | Same driver as Pi 4, stable |

### AWUS036ACH (RTL8812AU)

| Platform | Soft AP | Notes |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ⚠️ | Needs external driver; 2025.x requires commit `63cf0b4`. Kernel 6.14+ rtw88 may improve |
| Ubuntu 22.04 / 24.04 | ⚠️ | May need manual rtw88 or aircrack-ng driver installation |
| Debian 11 / 12 | ⚠️ | Same as above |
| Raspberry Pi 4 | ⚠️ | Works but high power (800mA); use powered USB hub |
| Raspberry Pi 5 | ⚠️ | Same; Pi 5 USB controller differences may affect behavior |

### AWUS036AXML / AWUS036AXM (MT7921AUN)

| Platform | Soft AP | Notes |
|----------|---------|-------|
| Kali Linux 2022.x (kernel 5.18+) | ✅ | Disable btusb, update firmware |
| Kali Linux 2024.x / 2025.x | ⚠️ | Kernel 6.11+ BT/WiFi conflict, unstable |
| Ubuntu 24.04 (kernel 6.8+) | ⚠️ | Issues reported late 2024 |
| Ubuntu 25.04 / CachyOS (kernel 6.14+) | ✅ | Plug-and-play, significant new-kernel improvement |
| Debian 12 | ⚠️ | Depends on kernel version |
| Raspberry Pi 4 / 5 | ⚠️ | Success cases exist but verify firmware + disable BT |

### AWUS036AX / AWUS036AXER (RTL8832BU)

| Platform | Soft AP | Notes |
|----------|---------|-------|
| Kali Linux | ❌ | Multi-state, USB mode switch needed, minimal community cases |
| Ubuntu / Debian | ❌ | Same |
| Raspberry Pi 4 / 5 | ❌ | Same |

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

Create `/etc/hostapd/hostapd.conf`:

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

Create `/etc/dnsmasq.conf`:

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

**Solution**: Remove excess flags. For MT7612U (ACM), the safest approach is to use the verified configuration from Section 3. **Do not copy ht_capab from other chipsets.**

---

### Q2 : Les clients se connectent mais ne peuvent pas accéder à Internet

**Symptôme** : WiFi connecté, IP obtenue, mais `ping 8.8.8.8` n'obtient aucune réponse

**Checklist**:

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

**Possible Causes**:

1. **Using DFS channels (100–144)**: MT7612U / MT7610U lack DFS support — use UNII-1 channels (36–48)
2. **Insufficient transmit power**: Ensure antennas are properly tightened on RP-SMA connectors
3. **USB power insufficient** (Raspberry Pi): Use official 5A power supply or powered USB hub

---

### Q4 : hostapd redémarre constamment sur Raspberry Pi

**Symptom**: `dmesg` shows frequent USB reset messages

**Likely Cause**: USB port power insufficient (especially with AWUS036ACH high-power chipset, max 800mA)

**Solution**:
- Use official Pi 5A power supply
- Use a powered USB hub
- Plug adapter into USB 3.0 port (Pi 4 only)

---

### Q5 : Le WiFi de l'AWUS036AXML/AXM chute soudainement ou ne démarre pas

**Likely Cause**: Bluetooth subsystem interfering with WiFi (MT7921AUN has built-in BT 5.2)

**Solution**: Permanently disable Bluetooth driver

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## 10. Analyse technique approfondie : VIF, WPA3, Canaux DFS {#technical}

### VIF (Interface Virtuelle) : Une carte, plusieurs rôles

VIF (Virtual Interface) permet à un seul adaptateur physique de fonctionner avec plusieurs interfaces logiques simultanément. For example: one interface connects to the upstream router (managed mode) while another serves as an AP (master mode) for other devices.

Three common scenarios:

| Scenario | VIF Required? | Best Adapter |
|----------|--------------|--------------|
| Basic NAT routing (eth0 upstream + wlan AP) | ❌ No | Any AP-capable adapter |
| Wireless bridging (WiFi receive + WiFi AP simultaneously) | ✅ Yes | ACM (MT7612U) |
| Monitor + AP simultaneously (security research / Rogue AP) | ✅ Yes | ACM (MT7612U) |

**VIF Practical Example (MT7612U):**

```bash
# Create an additional AP virtual interface alongside existing wlan1
sudo iw phy phy1 interface add ap0 type __ap
sudo ip link set ap0 up
# Now wlan1 can connect upstream while ap0 runs hostapd
```

Only MediaTek in-kernel drivers (mt76x2u, mt7921u) fully support VIF. Realtek out-of-kernel drivers essentially lack this capability — if you need AP + Monitor simultaneously, you must use two separate adapters.

---

### Comparaison du support WPA3

| Chipset | Corresponding Model | WPA2 | WPA3 |
|---------|-------------------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ Native SAE support |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ Native SAE support |
| RTL8812AU | AWUS036ACH | ✅ | ❌ Claims support but doesn't work |
| RTL8832BU | AWUS036AX / AXER | ✅ | ⚠️ Unconfirmed |

---

### Sélection des canaux Soft AP 5GHz : Éviter DFS

Les canaux DFS (Dynamic Frequency Selection) (ch100–ch140) nécessitent une détection radar au niveau du noyau. Le MT7612U et les chipsets similaires n'ont pas de support DFS. Pour le mode AP 5GHz, choisissez :

| Band | Recommended Channels | Reason |
|------|---------------------|--------|
| **UNII-1** | **36, 40, 44, 48** | Tous les chipsets pris en charge ; choix le plus sûr |
| UNII-2 (DFS) | 52–144 | La plupart non pris en charge ; non recommandé |
| UNII-3 | 149–165 | Support partiel (selon la région) |

---

## 11. Cas réels de la communauté {#real-cases}

### Cas 1 : RPi4B + AWUS036ACM = AP domestique 5GHz stable à long terme

**Source**: morrownr/7612u GitHub knowledge base
**Scenario**: morrownr long-term uses RPi4B + AWUS036ACM as a home 5GHz AP, paired with Pi's built-in 2.4GHz for dual-band service
**Result**: Long-term stable operation, no restarts needed, rated "outstanding"
**Configuration**: hostapd + dnsmasq + iptables NAT

### Cas 2 : RPi3B+ + ACM — Crash initial, corrigé

**Source**: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
**Problem**: hostapd crashed when run over USB 2.0 on RPi3B+
**Root Cause**: `ht_capab` contained HT40 flags unsupported under USB 2.0 bandwidth limits
**Solution**: Removed excess flags; successfully launched on Kali Linux

### Cas 3 : Pi PwnBox + AWUS036ACH = Rogue AP Red Team

**Source**: GitHub koutto/pi-pwnbox-rogueap
**Scenario**: RPi3B+ Rogue AP platform: one RTL8812AU (AWUS036ACH) for AP, another RT3070 (AWUS036NEH) for packet injection attacks
**Key Finding**: Because RTL8812AU lacks VIF, two separate adapters were required (unlike ACM which handles both on a single card)

### Cas 4 : AWUS036AXML AP stable sur RPi3B ArchLinux ARM

**Source**: [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
**Scenario**: User successfully ran AWUS036AXML in AP mode on RPi3B ArchLinux aarch64
**Quote**: "It's the most stable mt7921 in my collection."
**Key Requirements**: hostapd compiled from git + btusb disabled

### Cas 5 : AWUS036ACHM (MT7610U, abandonné) AP pleine vitesse sur Pi4

**Source**: [GitHub Discussion #31](https://github.com/morrownr/USB-WiFi/discussions/31)
**Problem**: Initial config only achieved 65 Mbps link speed, far below AC 5GHz full speed
**Solution**: Added correct `vht_oper_chwidth=1` and `vht_oper_centr_freq_seg0_idx`; achieved 433 Mbps link rate
**Relevance for ACM**: The same VHT parameter configuration is critical for MT7612U (ACM) as well

---

## 12. Recommandations d'achat et verdict final {#recommendations}

### Matrice de décision rapide

| Évaluation | Modèle | Idéal pour | En un mot |
|--------|-------|----------|-----------|
| 🥇 **Premier choix** | **AWUS036ACM** | Tout le monde, surtout les débutants Soft AP | Stable toutes plateformes, zéro tracas |
| 🥈 Utilisable | AWUS036ACH | Utilisateurs possédant déjà ce modèle | Nécessite un pilote, pas de WPA3 |
| 🥉 Avancé | AWUS036AXML | Utilisateurs ayant besoin du WiFi 6E prêts à bricoler | Avantage 6GHz, corrections manuelles nécessaires |
| ❌ À éviter | AWUS036AX / AXER | N/A | Soft AP non validé par la communauté |

### 🎯 Guide de décision

- **Besoin d'un Soft AP stable sur Kali / Ubuntu / Debian / Raspberry Pi 4 ou 5 ?**
  → Prenez l'**AWUS036ACM**, sans hésitation.

- **Vous possédez déjà un AWUS036ACH et voulez essayer le Soft AP ?**
  → Ça fonctionne, mais uniquement WPA2, et vous devrez installer le pilote. If you accept those limits, go ahead.

- **Besoin du WiFi 6E (bande 6 GHz) et prêt à configurer ?**
  → AWUS036AXML — n'oubliez pas de désactiver le pilote BT et de vérifier le noyau ≥ 6.6 LTS.

- **Objectif principal est le Soft AP, pas le test d'intrusion ?**
  → L'AWUS036ACM est le seul choix avec une vérification communautaire étendue sur toutes les plateformes.

---

### Conclusion

Le facteur central dans la construction d'un Soft AP n'est pas la vitesse WiFi ou le nombre d'antennes — **c'est la prise en charge du mode AP par le pilote du chipset.**

Parmi tous les produits ALFA que nous avons étudiés, l'**AWUS036ACM (MT7612U)** est le seul adaptateur qui satisfait simultanément : pilote in-kernel, WPA3 natif, interfaces virtuelles VIF, faible consommation et stabilité multi-plateforme. C'est l'étalon-or du Soft AP.

L'AWUS036ACH (RTL8812AU) fonctionne si vous acceptez les limitations. L'AWUS036AXML/AXM (MT7921AUN) a un grand potentiel mais la maturité du pilote est encore en cours. AWUS036AX/AXER (RTL8832BU) — not recommended for this use case.

**Si c'est votre première configuration d'un Soft AP sur Raspberry Pi ou Kali Linux — choisissez l'ACM. Vous ne le regretterez pas.**

---

### Liens d'achat

- [AWUS036ACM — Soft AP Top Pick](/en/products/alfa/awus036acm/)
- [AWUS036ACH — Classic Pentesting Adapter](/en/products/alfa/awus036ach/)
- [AWUS036AXML — WiFi 6E Tri-Band Flagship](/en/products/alfa/awus036axml/)
- [ALFA Network Full Product Line](/en/products/alfa/)

### Lectures complémentaires

- [AWUS036ACH vs AWUS036ACM: Full Chipset Driver Comparison](/en/blog/awus036ach-vs-awus036acm/)
- [AWUS036ACM IBSS & Mesh on Raspberry Pi](/en/blog/)
- [morrownr/USB-WiFi — The Authoritative Linux USB WiFi Knowledge Base](https://github.com/morrownr/USB-WiFi) (4,100+ stars)
- [morrownr/7612u — MT7612U Reference (incl. RPi4B Bridged AP Tutorial)](https://github.com/morrownr/7612u)
- [DeepWiki — morrownr/USB-WiFi Auto-Curated Knowledge Base](https://deepwiki.com/morrownr/USB-WiFi)

---

### 📚 Sources de données

This article aggregates information from:
- **morrownr/USB-WiFi** GitHub knowledge base (4,100+ stars) with complete iw_list records
- **morrownr/7612u** — MT7612U Bridged AP on RPi4B tutorial
- **GitHub issue tracker** — issue #2 (ACM AP config), #476 (AXML AP testing), Discussion #31 (ACHM full-speed AP)
- **koutto/pi-pwnbox-rogueap** — Alfa adapter RogueAP implementation case
- **Rokland** authorized retailer Linux support pages
- **Lab401** technical reviews and 2025 pentesting best-pick reports
- **Raspberry Pi Official Forum** — Pi 4/5 USB WiFi compatibility discussions
- **Yupitek existing blog** — ACM China Install Guide, AXML WiFi 6E Review, Kali Linux 2026 best adapters

---

> **Tags**: #ALFANetwork #SoftAP #WiFiHotspot #hostapd #KaliLinux #Ubuntu #Debian #RaspberryPi #AWUS036ACM #AWUS036ACH #AWUS036AXML #MT7612U #RTL8812AU #MT7921AUN #Yupitek
>
> **Auteur** : Yupitek Ltd — Distributeur Agréé ALFA Network Taiwan
>
> **Avertissement** : Données de recherche à jour en mai 2026. Linux kernels and distributions continue to evolve; driver support may change with new versions. Verify target platform kernel version and driver compatibility before deployment.
>
> **Support technique** : Pour les problèmes de configuration Soft AP, contactez le support technique Yupitek Taiwan. Demandes de produits : [yupitek.com](https://yupitek.com/fr/).
