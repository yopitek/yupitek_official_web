---
title: "Flipper Zero & Flipper One avec adaptateurs WiFi ALFA : Guide complet de compatibilité"
description: "Un Flipper Zero peut-il utiliser des adaptateurs WiFi USB ALFA pour l'injection de paquets ? Non — voici pourquoi. Flipper One supporte l'ALFA AWUS036AXML en mode monitor complet avec injection. Guide complet avec analyse des chipsets, compatibilité des pilotes et instructions d'installation."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-alfa-compatibility"
tags: ["flipper-zero", "flipper-one", "alfa-network", "wifi-adapter", "monitor-mode", "packet-injection", "kali-linux", "pentesting", "AWUS036AXML", "wireless-security"]
categories: ["Technical"]
featureimage: "/images/blog/flipper-alfa-compatibility.webp"
---

{{< alert "triangle-exclamation" >}}
**Avis juridique :** Le mode monitor et l'injection de paquets doivent uniquement être effectués sur des réseaux que vous possédez ou pour lesquels vous avez une autorisation écrite explicite pour tester. L'interception non autorisée des communications sans fil est illégale dans la plupart des juridictions. Toutes les techniques décrites dans ce guide sont destinées exclusivement aux **tests de pénétration autorisés, à la recherche en sécurité sur votre propre matériel, et à des fins éducatives**.
{{< /alert >}}

## Introduction : La Question que se Pose Chaque Pentester

Si tu possèdes un Flipper Zero — ou si tu envisages d'en acheter un — et que tu as entendu parler des légendaires adaptateurs WiFi USB d'ALFA Network pour les tests de sécurité sans fil, tu te seras probablement demandé : **« Est-ce que je peux brancher mon adaptateur ALFA sur mon Flipper Zero et commencer à capturer des handshakes WPA2 ? »**

La réponse courte est non, mais la réponse complète est bien plus intéressante.

**Le Flipper Zero ne peut être connecté à aucun adaptateur USB WiFi ALFA.** Il s'agit d'une limitation matérielle, pas logiciel. Le microcontrôleur STM32WB55 à l'intérieur du Flipper Zero dispose d'un contrôleur USB qui fonctionne en **mode device uniquement** — il est physiquement incapable d'agir comme un USB host pour piloter des périphériques externes comme des adaptateurs WiFi.

Mais Flipper Devices a annoncé un produit entièrement nouveau : **Flipper One**. Construit autour d'un Rockchip RK3576 avec 8 Go de RAM et tournant sous Debian Linux complet, Flipper One possède deux ports USB 3.1 host et peut utiliser directement les adaptateurs ALFA pour des tests de sécurité sans fil complets, y compris l'analyse Wi-Fi 6E en 6 GHz. Fait notable, le fondateur de Flipper One, Pavel Zhovner, a lui-même désigné l'**ALFA AWUS036AXML** comme adaptateur de test officiel dans l'annonce du produit.

Cet article explique l'intégralité du tableau de compatibilité : ce qui fonctionne, ce qui ne fonctionne pas, pourquoi, et comment tout installer.

---

## Flipper Zero : Pourquoi Il Ne Peut Pas Utiliser les Adaptateurs ALFA

Pour comprendre cette limitation, il faut savoir ce qu'il y a à l'intérieur d'un Flipper Zero.

### Le Matériel

| Composant | Spécification |
|-----------|--------------|
| **MCU** | STMicroelectronics STM32WB55RG |
| **Architecture** | ARM Cortex-M4 (application core) @ 64 MHz + ARM Cortex-M0+ (wireless core) @ 32 MHz |
| **RAM** | 256 KB (shared between cores) |
| **Storage** | 1 MB Flash + MicroSD |
| **Operating System** | FreeRTOS (real-time operating system) |
| **USB** | USB Type-C, USB 2.0 Full Speed (12 Mbps) |
| **USB Mode** | **Device only** — pas de host ni de OTG |

### La Limite USB

Le contrôleur USB du STM32WB55 est un **USB Full-Speed Device Controller**. Il peut présenter le Flipper Zero à un ordinateur comme un périphérique USB (pour le transfert de fichiers, les mises à jour du firmware et l'interface CLI), mais il ne peut pas agir comme un USB host. Il n'y a aucun contrôleur host sur la puce — aucune modification du firmware ne peut ajouter cette capacité.

Pour utiliser un adaptateur USB WiFi ALFA, un appareil doit avoir :
1. **Un contrôleur USB Host hardware** — pour énumérer et communiquer avec les périphériques USB
2. **Un noyau Linux avec le support des pilotes WiFi** — pour charger les pilotes comme `mt7921u`, `mt76`, ou `rtw88`
3. **Un apport d'énergie suffisant** — Les adaptateurs ALFA consomment typiquement entre 500 mA et 900 mA à 5V

Le Flipper Zero échoue sur les trois points :
- ❌ Pas de contrôleur USB Host (hardware)
- ❌ Tourne sous FreeRTOS, pas Linux — aucun framework de pilotes noyau n'existe
- ⚠️ Le GPIO en 5V est limité à 1,2A total sur toutes les broches, et seulement si activé manuellement

> **Verdict :** Il est **physiquement impossible** de brancher un quelconque adaptateur USB WiFi ALFA sur un Flipper Zero. Il ne s'agit pas d'une limitation contournable par logiciel, mises à jour du firmware ou cartes d'extension — cela est gravé dans le silicium.

---

## Flipper Zero + WiFi Dev Board : Une Alternative Limitée

Flipper Devices vend un **WiFi Dev Board** officiel basé sur le microcontrôleur **ESP32-S2**. Cette carte se branche sur le header GPIO du Flipper Zero et offre des capacités WiFi basiques en 2,4 GHz — mais elle **ne change pas** la situation du USB host.

| Aspect | Capacité |
|--------|-----------|
| **WiFi Chip** | ESP32-S2 (Xtensa LX7 single-core, 240 MHz) |
| **Fréquence** | 2,4 GHz uniquement, 802.11 b/g/n |
| **USB Host** | ❌ Le WiFi Dev Board n'expose pas de USB Host — l'ESP32-S2 se connecte au Flipper Zero via GPIO, pas USB |
| **Firmware** | ESP32 Marauder (community-developed) |

Avec le **firmware ESP32 Marauder** installé, le WiFi Dev Board peut effectuer :

- ✅ Des attaques de deauthentication (2,4 GHz uniquement)
- ✅ La capture de PMKID (2,4 GHz uniquement)
- ✅ Le scanning des access points et le broadcasting SSID
- ✅ Le sniffing basique de paquets (2,4 GHz uniquement)

Ce qu'il **ne peut pas** faire :

- ❌ Utiliser des adaptateurs USB ALFA externes (pas de USB host)
- ❌ Fonctionner sur les bandes 5 GHz ou 6 GHz
- ❌ Atteindre la portée ou la fiabilité d'injection d'un ALFA dédié
- ❌ Exécuter des outils basés sur Linux comme aircrack-ng, Kismet ou Wireshark

> **Si tu n'as qu'un Flipper Zero et que tu as besoin de tests basiques en 2,4 GHz**, le WiFi Dev Board avec ESP32 Marauder est une solution fonctionnelle — mais fortement limitée. Pour tout le reste, il te faut un autre matériel.

---

## Flipper One : La Plateforme pour laquelle ALFA Attendait

Le **21 mai 2026**, le fondateur de Flipper Devices, Pavel Zhovner, a publié un article de blog intitulé *"Flipper One — We Need Your Help"* annonçant un produit complètement nouveau. Flipper One n'est pas une mise à niveau du Flipper Zero — c'est une catégorie d'appareil entièrement différente, conçue pour une couche différente de la stack de protocoles.

> *"Flipper Zero est la couche 0 — contrôle d'accès hors-ligne point à point : NFC, RFID, Sub-GHz, infrared. Flipper One est la couche 1 — connectivité IP : Wi-Fi, Ethernet, 5G, satellite. Ils ne se remplacent pas l'un l'autre."*
> — Pavel Zhovner, flipper.net

{{< alert "circle-info" >}}
**Note de disponibilité :** Flipper One est actuellement en **développeur preview**. La disponibilité générale, le prix et la distribution régionale seront annoncés via crowdfunding. Suis [flipper.net](https://flipper.net) et le [Flipper One Developer Portal](https://docs.flipper.net/one) pour les mises à jour.
{{< /alert >}}

### Spécifications Matérielles

| Composant | Spécification |
|-----------|--------------|
| **CPU** | Rockchip RK3576 : 4× Cortex-A72 + 4× Cortex-A53, jusqu'à 2,2 GHz |
| **GPU** | ARM Mali-G52 MC3 (OpenGL ES 3.2, Vulkan 1.2) |
| **NPU** | 6 TOPS @ INT8 (peut exécuter des LLMs locaux) |
| **Co-processor** | Raspberry Pi RP2350B (dual M33 + dual RISC-V) pour display/buttons/power |
| **RAM** | 8 GB LPDDR5 |
| **Storage** | 64 GB UFS 2.2 + MicroSD |
| **Operating System** | Debian 13 (Trixie) — Flipper Devices indique qu'il ciblera le noyau Linux mainline 7.0 sans dépendances de patch out-of-tree |
| **USB Host** | USB-C2 + USB-A, les deux USB 3.1 (5 Gbps), tous les deux host-capable |
| **WiFi intégré** | Wi-Fi 6E via MT7921AUN (2.4/5/6 GHz, 2×2 MIMO) |
| **Ethernet** | 2× RJ45 Gigabit (supporte inline/MitM sniffing) |
| **M.2 Expansion** | Key-B : PCIe 2.1 ×1 / USB 3.1 / SATA3 / SIM card |

### Pourquoi Flipper One Fonctionne avec les Adaptateurs ALFA

Contrairement au Flipper Zero, Flipper One satisfait les trois exigences :

1. ✅ **Contrôleur USB 3.1 Host** : Deux ports USB host-capable capables d'énumérer et d'alimenter des périphériques externes
2. ✅ **Debian Linux complet** : Noyau Linux standard avec support des pilotes in-kernel pour `mt7921u`, `mt76`, et `rtw88`
3. ✅ **Apport d'énergie suffisant** : Les ports USB peuvent fournir l'énergie bus standard ; le GPIO fournit 5V @ 2A et 3.3V @ 2A avec protection eFuse

La bande passante USB 3.1 (5 Gbps) est amplement suffisante — même le plus rapide des adaptateurs ALFA (AWUS036AXML à AXE3000) est limité par le débit pratique de USB 3.0 à environ 1,2 Gbps.

### Environnement Logiciel

Flipper One exécute un environnement Debian standard, ce qui signifie que tu peux installer les outils de sécurité sans fil directement via `apt` :

```bash
sudo apt update
sudo apt install aircrack-ng kismet wireshark hcxdumptool hashcat
```

Flipper One introduit aussi les **Flipper OS Profiles** — un système basé sur les snapshots qui te permet de créer des environnements propres et isolés. Tu peux maintenir un profil "Pentest" dédié avec tous tes outils sans fil, et basculer vers un propre profile pour l'usage quotidien sans contamination croisée.

---

## Adaptateurs ALFA Recommandés pour Flipper One

Tous les adaptateurs ALFA ne fonctionnent pas également bien pour les tests de sécurité sans fil. Les critères clés sont le **chipset**, la **maturité du driver**, et le **support in-kernel** (ce qui signifie qu'aucune compilation DKMS n'est requise).

### ⭐⭐⭐⭐⭐ Top Pick : AWUS036AXML (Wi-Fi 6E)

| Spéc | Détail |
|------|--------|
| **Chipset** | MediaTek MT7921AUN |
| **Bands** | 2.4 / 5 / 6 GHz (Wi-Fi 6E) |
| **Max Speed** | AXE3000 (theoretical), ~1,2 Gbps practical |
| **Driver** | `mt7921u` — in-kernel depuis Linux 5.18 |
| **DKMS Required** | ❌ Non |
| **Antenna** | Dual RP-SMA (remplaçable) + Bluetooth 5.2 |

> **Pourquoi c'est le meilleur :** C'est l'adaptateur que le créateur de Flipper One a testé en priorité. Le pilote `mt7921u` est dans le noyau mainline sans aucun patch vendor requis. Il supporte les trois bandes WiFi (2.4/5/6 GHz), ce qui le rend ready for the future pour les assessments de sécurité Wi-Fi 6E. Le mode monitor et l'injection de paquets sont stables et bien testés.

### ⭐⭐⭐⭐⭐ Best Value : AWUS036ACM (Wi-Fi 5 AC1200)

| Spéc | Détail |
|------|--------|
| **Chipset** | MediaTek MT7612U |
| **Bands** | 2.4 / 5 GHz (Wi-Fi 5) |
| **Max Speed** | AC1200 (300 + 867 Mbps) |
| **Driver** | `mt76` — in-kernel depuis Linux 4.19 |
| **DKMS Required** | ❌ Non |
| **Antenna** | Dual 5 dBi RP-SMA (remplaçable) |

> **Pourquoi c'est le meilleur rapport qualité/prix :** Le chipset MT7612U est éprouvé dans la communauté pentest. Le pilote `mt76` est dans le noyau depuis des années et est exceptionnellement stable. Le mode monitor et l'injection fonctionnent parfaitement à partir du noyau 6.5 et plus. À un prix inférieur à celui de l'AXML, il offre le meilleur ratio prix/capacité pour les tests 2.4/5 GHz.

### ⭐⭐⭐⭐ Lightweight Pick : AWUS036ACHM (Wi-Fi 5 AC433)

| Spéc | Détail |
|------|--------|
| **Chipset** | MediaTek MT7610U |
| **Bands** | 2.4 / 5 GHz (Wi-Fi 5) |
| **Max Speed** | AC433 (theoretical) |
| **Driver** | `mt76` — in-kernel depuis Linux 4.19 |
| **DKMS Required** | ❌ Non |
| **Antenna** | Single high-gain RP-SMA (remplaçable) |

> **Pourquoi c'est le choix léger :** L'option la plus portable — USB 2.0, une seule antenne, consommation la plus faible. Utilise la même famille de pilotes `mt76` que l'ACM. Idéal pour le field work où la taille et l'efficacité énergétique comptent plus que le débit brut. **Note :** Sur les plateformes ARM64 (incluant RK3576), l'exécution simultanée de `airodump-ng` et `aireplay-ng` peut déclencher un bug connu de drop d'interface (morrownr issue #379). À utiliser avec cette connaissance.

### ⭐⭐⭐ Alternative : AWUS036ACH (Wi-Fi 5 AC1200, RTL8812AU)

| Spéc | Détail |
|------|--------|
| **Chipset** | Realtek RTL8812AU |
| **Bands** | 2.4 / 5 GHz (Wi-Fi 5) |
| **Max Speed** | AC1200 (300 + 867 Mbps) |
| **Driver** | `rtw88` — in-kernel sur le noyau prévu de Flipper One ; les systèmes plus anciens peuvent nécessiter DKMS |
| **DKMS Required** | ❌ Non requis sur Flipper One / ⚠️ Les noyaux plus anciens peuvent nécessiter [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) DKMS |
| **Antenna** | Dual 6 dBi RP-SMA (puissance TX élevée) |

> **Pourquoi c'est une alternative :** Le chipset RTL8812AU a une longue histoire dans le pentesting. Il devrait être supporté sur le noyau prévu de Flipper One sans modules DKMS supplémentaires. Pour les systèmes plus anciens, le pilote DKMS aircrack-ng reste disponible. Les antennes high-gain 6 dBi offrent une excellente portée, bien que les adaptateurs basés sur MediaTek soient généralement préférés pour leur support de pilotes in-kernel plus mature.

### ⚠️ Non Recommandé pour le Pentesting

Les modèles ALFA suivants utilisent des chipsets Realtek avec des pilotes Linux immatures ou instables pour le mode monitor et l'injection de paquets. **À éviter pour les travaux de sécurité sans fil sur Flipper One :**

| Modèle | Chipset | Problème |
|--------|---------|----------|
| AWUS036AX | RTL8832BU | Chipset Wi-Fi 6, le support driver est encore en développement en 2026 |
| AWUS036AXER | RTL8832BU | Mêmes problèmes de chipset que AWUS036AX |
| AWUS036ACS | RTL8811AU | Mode monitor limité, injection instable |
| AWUS036EACS | RTL8811CU | Mode monitor limité, injection instable |

---

## Guide d'Installation : Flipper One + ALFA AWUS036AXML

Ce guide suppose que tu as un Flipper One sous Debian Linux avec l'adaptateur physiquement connecté à un port USB host.

### Étape 1 : Vérifier que l'Adaptateur est Reconnu

```bash
# Check USB device enumeration
lsusb
# Expected output (example):
# Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device

# List wireless interfaces
iw dev
# Expected: wlan0 (or wlan1 if built-in WiFi occupies wlan0)

# Alternative check
ip link show
```

### Étape 2 : Confirmer que le Driver est Chargé

```bash
# Pour AWUS036AXML / AWUS036AXM (MT7921AUN) :
lsmod | grep mt7921u

# Pour AWUS036ACM / AWUS036ACHM (MT7612U / MT7610U) :
lsmod | grep mt76

# Pour AWUS036ACH (RTL8812AU) :
lsmod | grep rtw88

# Check kernel version (should be 6.12+ for best MT7921AUN support):
uname -r
```

Si le driver est listé, il est chargé et prêt. Aucune installation supplémentaire n'est nécessaire — ce sont tous des pilotes in-kernel.

### Étape 3 : Activer le Mode Monitor

```bash
# Kill interfering processes (NetworkManager, wpa_supplicant, etc.)
# Note: This will also disconnect Flipper One's built-in WiFi — use a dedicated
# Flipper OS Profile for pentesting to avoid disrupting your normal network connection.
sudo airmon-ng check kill

# Start monitor mode on the adapter
sudo airmon-ng start wlan0
# Interface renamed to wlan0mon

# Verify monitor mode is active
iw dev wlan0mon info
# Should show: type monitor
```

Méthode manuelle (si tu préfères ne pas utiliser airmon-ng) :

```bash
sudo ip link set wlan0 down
sudo iw wlan0 set monitor none
sudo ip link set wlan0 up
```

### Étape 4 : Tester l'Injection de Paquets

```bash
# Test injection capability
sudo aireplay-ng --test wlan0mon
# Look for: "Injection is working!"

# Perform a basic scan
sudo airodump-ng wlan0mon

# Scan all supported bands (AWUS036AXML only)
sudo airodump-ng --band abg wlan0mon     # 2.4 GHz + 5 GHz
sudo airodump-ng --band 6 wlan0mon       # 6 GHz (aircrack-ng 1.7+)

# Target a specific channel
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF wlan0mon
```

### Étape 5 : Capturer un Handshake WPA2

```bash
# Terminal 1: Start capture on target channel
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# Terminal 2: Send deauth to force reconnection
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon

# Check for handshake capture in Terminal 1:
# "WPA handshake: AA:BB:CC:DD:EE:FF" appears when captured
```

### Étape 6 : Retourner en Mode Normal

```bash
# Stop monitor mode and restore managed mode
sudo airmon-ng stop wlan0mon

# Restart network services
sudo systemctl restart NetworkManager
```

### Vue d'Architecture

Le diagramme ci-dessous montre l'architecture complète de pentest sans fil avec Flipper One et les adaptateurs ALFA :

![Flipper One + ALFA WiFi Adapters Pentest Architecture](diagram/flipper-alfa-topology.svg)

*Topology: Flipper One platform → ALFA USB adapters → pentest toolchain → wireless capabilities*

---

## Flipper Zero vs. Flipper One : Comparaison Côté à Côté

| Feature | Flipper Zero | Flipper One |
|---------|:-----------:|:----------:|
| **Operating System** | FreeRTOS | Debian 13 (Trixie) |
| **CPU** | STM32WB55 (Cortex-M4, 64 MHz) | RK3576 (8-core ARM, 2,2 GHz) |
| **RAM** | 256 KB | 8 GB LPDDR5 |
| **Storage** | 1 MB Flash + MicroSD | 64 GB UFS 2.2 + MicroSD |
| **GPU / NPU** | ❌ | Mali-G52 GPU + 6 TOPS NPU |
| **USB Host** | ❌ Device only | ✅ USB-C2 + USB-A (USB 3.1) |
| **ALFA Adapter Support** | ❌ | ✅ |
| **Built-in WiFi** | ❌ (BLE only) | ✅ Wi-Fi 6E (MT7921AUN) |
| **5 GHz / 6 GHz WiFi** | ❌ | ✅ |
| **Gigabit Ethernet** | ❌ | ✅ 2× RJ45 |
| **Monitor Mode** | ❌ (native) | ✅ |
| **Packet Injection** | ❌ (native) | ✅ |
| **M.2 Expansion** | ❌ | ✅ Key-B (PCIe / USB 3.1 / SATA) |
| **Price** | ~169 USD (in production) | Developer preview (crowdfunding TBA) |

---

## Conclusion : Le Bon Outil pour le Bon Usage

Si tu cherches à utiliser des adaptateurs WiFi ALFA pour les tests de sécurité sans fil, **Flipper Zero n'est pas la bonne plateforme** — et ce n'est pas sa faute. Il a été conçu pour un autre usage : les tests de contrôle d'accès offline (NFC, RFID, Sub-GHz, infrared). Il excelle dans ces tâches, mais la capacité USB host n'a jamais fait partie de sa conception.

Pour le cas d'usage spécifique de **Monitor Mode et Packet Injection avec les adaptateurs ALFA**, tu as deux chemins :

| Path | Platform | ALFA Adapter | Capability |
|------|----------|-------------|------------|
| **Best** | Flipper One | AWUS036AXML (MT7921AUN) | Full 2.4/5/6 GHz, in-kernel driver, official support |
| **Value** | Flipper One | AWUS036ACM (MT7612U) | Full 2.4/5 GHz, in-kernel driver, proven stable |
| **Workaround** | Flipper Zero + WiFi Dev Board | None (ESP32-S2 built-in) | 2.4 GHz only, limited range, basic capabilities |

**Flipper One représente un bond générationnel** — il apporte toute la puissance d'un environnement Debian Linux avec la capacité USB 3.1 host dans une plateforme matérielle portable et conçue à cet effet. Associé à un ALFA AWUS036AXML (l'adaptateur que le créateur de Flipper One a spécifiquement testé), tu obtiens une boîte à outils complète d'assessment de sécurité sans fil dans ta poche.

---

### Où Acheter

Tous les adaptateurs ALFA recommandés sont disponibles chez Yupitek, un distributeur autorisé d'ALFA Network. Parcourt la sélection complète ou compare les modèles :

- [Adaptateurs WiFi USB ALFA — Catalogue Complet](https://yupitek.com/en/products/alfa/) — Tous les modèles avec specs et pricing
- [Comparaison Produits ALFA](/en/alfa_compare/) — Comparaison côte à côte des chipsets, bandes et pilotes

### Pour Aller Plus Loin

- [Article Officiel Flipper One](https://blog.flipper.net/flipper-one-we-need-your-help/) — Pavel Zhovner, mai 2026
- [Flipper One Developer Portal](https://docs.flipper.net/one) — Spécifications techniques et documentation
- [Qu'est-ce que le Packet Injection ?](/en/blog/packet-injection-guide/) — Notre guide sur les fondamentaux du packet injection
- [AWUS036AXML Wi-Fi 6E Review](/en/blog/awus036axml-wifi-6e-review/) — Review détaillée de notre adaptateur phare
- [Comparaison Produits ALFA](/en/alfa_compare/) — Specs côte à côte pour tous les modèles ALFA

---

*Pour les questions pré-vente concernant la compatibilité entre Flipper One et les adaptateurs ALFA, contacte le support Yupitek à support@yupitek.com ou appelle le +886-2-87325338.*
