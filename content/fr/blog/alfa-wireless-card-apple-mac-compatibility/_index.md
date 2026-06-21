---
title: "Cartes sans fil ALFA sur Apple Mac (2026) : Le rapport complet de compatibilité pour M1/M2/M3/M4 & Intel"
description: "Guide de compatibilité complet pour l'utilisation des adaptateurs sans fil USB ALFA Network sur Apple Mac (MacBook, MacBook Pro, MacBook Air, Mac Mini, Mac Studio) avec les processeurs Intel et Apple Silicon M1/M2/M3/M4. Découvrez quelles cartes ALFA fonctionnent, pourquoi Apple Silicon n'offre aucun support natif et comment activer le mode moniteur via une VM Linux."
keywords: "carte sans fil ALFA Mac, compatibilité ALFA macOS, adaptateur ALFA Apple Silicon, adaptateur USB WiFi M1 M2 M3 M4, ALFA Network MacBook, mode moniteur Mac, AWUS036ACH Mac, AWUS036ACM Mac, ALFA Network Mac Mini, tests de pénétration Apple Silicon"
author: "Équipe de support technique Yupitek"
date: "2026-06-20"
category: "Guide technique"
tags: ["Wireless Security", "ALFA Network", "Apple Mac", "Penetration Testing", "macOS Compatibility"]
---
Si vous utilisez un Apple Mac — qu'il s'agisse d'un MacBook Pro avec M3 Max, d'un Mac Studio avec M2 Ultra ou d'un Mac Mini basé sur Intel — et que vous souhaitez utiliser un adaptateur sans fil ALFA Network pour l'audit Wi-Fi, le mode moniteur ou l'injection de paquets, vous avez besoin de la réponse définitive à une question : **Quelle carte ALFA fonctionne sur quel Mac ?**

Voici la réponse courte :

> **Mac Apple Silicon (M1/M2/M3/M4) : Aucune carte sans fil ALFA ne fonctionne nativement sur macOS.** Il s'agit d'une limitation architecturale — les extensions du noyau macOS de Realtek sont des binaires x86_64 qui ne peuvent pas être chargés sur le noyau ARM64. Il n'existe pas de correctif, et aucun fabricant n'a prévu de changer cela.
>
> **Mac Intel : Support limité, connectivité client uniquement.** Les versions macOS 10.11–10.15 disposent de pilotes officiels partiels, mais **le mode moniteur et l'injection de paquets ne sont pas supportés sur macOS** — les pilotes n'implémentent tout simplement pas ces fonctionnalités.
>
> **La solution fonctionnelle :** Exécuter Kali Linux ARM dans une VM (UTM/Parallels/VMware) avec transfert USB sur votre Mac Apple Silicon. Le mode moniteur et l'injection de paquets fonctionnent parfaitement dans la VM Linux.

Ce guide fournit la matrice de compatibilité complète, explique les six raisons techniques pour lesquelles Apple Silicon ne peut pas prendre en charge les cartes ALFA nativement, et vous guide à travers la configuration VM qui fonctionne réellement.

---

## 1. La matrice de compatibilité : Quelle carte ALFA fonctionne sur quel Mac ?

Ce tableau est la référence définitive. Il évalue les 9 adaptateurs sans fil ALFA actuellement disponibles (non EOL) de la [gamme de produits ALFA de Yupitek](https://yupitek.com/en/products/alfa/) selon quatre scénarios de déploiement.

### 1.1 Matrice de compatibilité complète

| Modèle ALFA | Chipset | Apple Silicon (macOS natif) | Mac Intel (macOS natif) | VM + Transfert USB (Kali ARM) | Raspberry Pi + Kali |
|:---|:---|:---:|:---:|:---:|:---:|
| **AWUS036ACH** | Realtek RTL8812AU | ❌ | ⚠️ Client uniquement (≤10.15) | ✅ Meilleur moniteur/injection | ✅ |
| **AWUS036ACM** | MediaTek MT7612U | ❌ | ⚠️ Client uniquement (≤10.12) | ✅ Plug & Play | ✅ Plug & Play |
| **AWUS036AXML** | MediaTek MT7921AUN | ❌ | ❌ | ✅ Wi-Fi 6E | ✅ |
| **AWUS036AXM** | MediaTek MT7921AUN | ❌ | ❌ | ✅ | ✅ |
| **AWUS036ACHM** | MediaTek MT7610U | ❌ | ❌ | ✅ | ✅ |
| **AWUS036ACS** | Realtek RTL8811AU | ❌ | ⚠️ Client uniquement (≤10.14) | ✅ | ✅ |
| **AWUS036AX** | Realtek RTL8832BU | ❌ | ❌ | ⚠️ Limité | ⚠️ Limité |
| **AWUS036AXER** | Realtek RTL8832BU | ❌ | ❌ | ⚠️ Limité | ⚠️ Limité |
| **AWUS036EACS** | Realtek RTL8821CU | ❌ | ⚠️ Client uniquement | ❌ Pas de mode moniteur | ⚠️ Non recommandé |

**Légende :** ✅ = Vérifié fonctionnel | ⚠️ = Limité / nécessite des conditions | ❌ = Non supporté

### 1.2 Verdict rapide par CPU Mac

| CPU Mac | Puis-je utiliser des cartes ALFA sur macOS ? | Puis-je utiliser le mode moniteur ? | Solution recommandée |
|:---|:---|:---|:---|
| **Apple Silicon M1/M2/M3/M4** | ❌ Non — limitation architecturale | ❌ Pas sur macOS | ✅ VM Linux avec transfert USB |
| **Intel (macOS 10.11–10.15)** | ⚠️ Limité — client uniquement, pas de mode moniteur | ❌ Non supporté | ✅ VM Linux avec transfert USB |
| **Intel (macOS 11+)** | ⚠️ Extension kext tierce uniquement (chris1111) | ❌ Non supporté | ✅ VM Linux avec transfert USB |

> [!IMPORTANT]
> **Conclusion :** Quel que soit le Mac que vous possédez, **le mode moniteur et l'injection de paquets nécessitent Linux**. L'approche VM + transfert USB est la solution universelle qui fonctionne sur chaque Mac, du MacBook Pro Intel 2012 au Mac Studio M4 2025.

---

## 2. Pourquoi Apple Silicon échoue : Le mur d'architecture à 6 couches

Si vous vous demandez si une future mise à jour de macOS pourrait résoudre ce problème — elle ne le fera pas. L'incompatibilité n'est pas un bug attendant d'être corrigé. C'est le résultat cumulatif de **six décisions de conception délibérées d'Apple** qui ensemble rendent les adaptateurs USB Wi-Fi tiers architecturalement impossibles sur Apple Silicon.

### Couche 1 : IO80211Controller est une API privée

Apple n'a jamais publié l'interface de programmation du noyau (KPI) pour les pilotes Wi-Fi natifs. La hiérarchie de classes ressemble à ceci :

```
IOService
  └─ IONetworkController
       └─ IOEthernetController        ← KPI publique
            └─ IO80211Controller      ← PRIVÉE (Apple interne uniquement)
```

Les fournisseurs tiers ont historiquement sous-classé directement `IOEthernetController`, c'est pourquoi les adaptateurs USB Wi-Fi sur macOS apparaissent comme des interfaces « Ethernet » plutôt que de s'intégrer à l'icône Wi-Fi de la barre de menus, AirDrop, Sidecar ou Find My.

### Couche 2 : NetworkingDriverKit ne supporte que l'Ethernet

Le remplacement moderne d'Apple pour les extensions du noyau est **DriverKit** — des pilotes en espace utilisateur qui ne risquent pas la stabilité du noyau. La famille réseau, `NetworkingDriverKit`, indique explicitement dans la [documentation officielle d'Apple](https://developer.apple.com/documentation/networkingdriverkit) :

> « Utilisez NetworkingDriverKit pour développer des pilotes pour les adaptateurs Ethernet USB. Notez que **l'Ethernet est la seule interface réseau actuellement prise en charge par NetworkingDriverKit.** »

Il n'existe pas de classe `IOUserNetworkWiFi`. Aucun framework Wi-Fi DriverKit n'existe. Même si Realtek ou MediaTek investissait l'effort d'ingénierie pour écrire un pilote DriverKit, **il n'existe pas de framework Apple dans lequel le connecter**.

### Couche 3 : La combinaison USB + kext réseau non supportée depuis Big Sur

La page des [extensions du noyau dépréciées](https://developer.apple.com/support/kernel-extensions/) d'Apple indique :

> « La combinaison utilisant les KPI IONetworkingFamily ainsi que n'importe quelle KPI USB (IOUSBHostFamily ou IOUSBFamily) est **non supportée dans macOS Big Sur**. »

C'est précisément la combinaison KPI que nécessite chaque extension du noyau USB Wi-Fi. La seule échappatoire est de désactiver entièrement SIP ou d'utiliser des profils MDM — aucun n'est approprié pour les produits grand public.

### Couche 4 : Le kext de Realtek est uniquement x86_64

Le pilote macOS de Realtek est fourni sous forme de `RtWlanU.kext`, compilé exclusivement pour **x86_64**. Les Mac Apple Silicon exécutent un noyau **ARM64**. Les extensions du noyau s'exécutent dans l'espace noyau — **Rosetta 2 ne peut pas traduire les extensions du noyau**.

Un utilisateur dans la [discussion chris1111 #128](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter/discussions/128) a documenté l'échec exact sur un M1 MacBook Air avec Ventura 13.1 et un ALFA AWUS1900 :

```
Domain=KMErrorDomain Code=71
Incompatible architecture: Binary is for x86_64, but needed arm64
Kext com.realtek.driver.RtWlanU v1830.32.b27
```

### Couche 5 : Realtek a abandonné le développement du pilote macOS

Le mainteneur de [chris1111/Wireless-USB-Big-Sur-Adapter](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) — la distribution communautaire de facto des pilotes Wi-Fi macOS de Realtek — indique explicitement dans le README :

> **« Il semble que cela ne fonctionne pas sur Mac M1, M2, M3, M4 avec puce Apple, fonctionnant uniquement pour Mac Intel. »**

Et en réponse à un utilisateur demandant si le support M1 pouvait être ajouté :

> « Les extensions kext héritées doivent être réécrites pour les Mac M1 (elles ne fonctionneront pas même via Rosetta 2), ce qui signifie que c'est aux grandes entreprises de mettre à jour leurs pilotes pour supporter M1. »

Realtek n'a pas fourni de kext arm64, de pilote DriverKit ou de plan public pour le support Apple Silicon. L'incitation économique est négligeable : chaque Mac Apple Silicon dispose déjà d'un Wi-Fi intégré.

### Couche 6 : Le chargement de kext sur Apple Silicon est volontairement hostile

Même si un kext arm64 existait, son chargement sur Apple Silicon nécessite :

1. Éteindre le Mac
2. **Appuyer et maintenir** le bouton d'alimentation jusqu'à l'apparition des options de démarrage
3. Entrer en mode One True Recovery (1TR)
4. Passer à une politique de **Sécurité réduite**
5. Activer « Autoriser la gestion par l'utilisateur des extensions du noyau des développeurs identifiés »
6. Redémarrer, installer le kext, l'approuver dans les Réglages système
7. **Redémarrer à nouveau** pour reconstruire l'Auxiliary Kernel Collection (AuxKC)

Selon le guide d'Apple [Extension sécurisée du noyau](https://support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web), ce flux est délibérément difficile : « La combinaison des exigences 1TR et mot de passe rend difficile pour les attaquants logiciels commençant depuis macOS d'injecter des kexts. »

> [!IMPORTANT]
> **Conclusion :** Aucune carte ALFA — et aucun adaptateur USB Wi-Fi tiers d'aucun fabricant — ne fonctionne nativement sur Apple Silicon macOS. Cela ne changera pas à moins qu'Apple publie un framework Wi-Fi DriverKit (ce qu'ils n'ont pas fait) ET qu'un fabricant écrive un pilote pour celui-ci (aucun ne l'a fait).

---

## 3. Mac Intel : Ce qui fonctionne encore (et ce qui ne fonctionne pas)

Si votre équipe utilise encore des Mac Intel, la situation est meilleure — mais seulement pour la connectivité Wi-Fi basique, pas pour l'audit de sécurité.

### 4.1 Chronologie du support des versions macOS

| Modèle ALFA | Chipset | Limite macOS officielle | Pilote communautaire (chris1111) |
|------------|---------|---------------------|------------------------------|
| AWUS036ACH | RTL8812AU | 10.15 Catalina | 11 Big Sur – 26 Tahoe (Intel uniquement) |
| AWUS036ACS | RTL8811AU | 10.14 Mojave | 11 Big Sur – 26 Tahoe (Intel uniquement) |
| AWUS036ACM | MT7612U | **10.12 Sierra** | ❌ Non supporté (MediaTek) |
| AWUS036ACHM | MT7610U | ❌ Aucun | ❌ Non supporté (MediaTek) |
| AWUS036AX/AXER | RTL8832BU | ❌ Aucun | ❌ Aucun |
| AWUS036AXML/AXM | MT7921AUN | ❌ Aucun | ❌ Aucun |

### 4.2 Le paradoxe du mode moniteur

Voici le problème critique pour les professionnels de la sécurité : **même quand le pilote s'installe avec succès sur les Mac Intel, le mode moniteur et l'injection de paquets ne fonctionnent pas.**

Les pilotes macOS d'ALFA n'implémentent que la connectivité client — ils n'implémentent pas les API du mode moniteur. Cela a été confirmé dans une [discussion Superuser](https://superuser.com/questions/1597114/alfa-wifi-network-card-monitor-mode-on-mac-os) où un utilisateur avait installé avec succès le pilote AWUS036EAC mais ne pouvait pas entrer en mode moniteur :

> *« Qu'est-ce qui vous fait penser qu'ALFA a intégré le support du mode moniteur dans leur pilote macOS ? Les API du mode moniteur sont différentes selon les OS. Je suppose qu'ils n'ont simplement pas pris la peine de l'implémenter pour macOS. »*

Cela crée un paradoxe : **vous achetez une carte ALFA spécialement pour le mode moniteur et l'injection de paquets, mais les pilotes macOS ne supportent ni l'un ni l'autre.** La carte Wi-Fi intégrée du Mac supporte en fait le mode moniteur (via l'utilitaire `airport`), mais les pilotes d'ALFA ne l'implémentent pas pour leur matériel.

> [!WARNING]
> Si votre objectif est l'audit de sécurité sans fil (mode moniteur, injection de paquets, capture de handshake, attaques deauth), **macOS ne peut pas le faire — sur aucun Mac, Intel ou Apple Silicon, avec aucune carte ALFA.** Vous avez besoin de Linux.

### 4.3 Le pilote chris1111 : Dernier recours pour les Mac Intel

Pour les Mac Intel exécutant macOS 11 Big Sur ou une version ultérieure, la seule option est le projet [chris1111/Wireless-USB-Big-Sur-Adapter](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) — une distribution communautaire du kext de Realtek.

**Prérequis :**
- Mac Intel uniquement (PAS Apple Silicon)
- System Integrity Protection (SIP) doit être désactivé
- Le kext n'est pas signé par Realtek/ALFA/Apple

**Cartes supportées :** AWUS036ACH (RTL8812AU) et AWUS036ACS (RTL8811AU) uniquement.

Rokland (distributeur américain d'ALFA) [met fortement en garde](https://store.rokland.com/blogs/news/apple-mac-os-11-big-sur-compatibility-update-for-alfa-awus036ach-other-products) : *« Nous vous déconseillons FORTEMENT d'utiliser ce pilote si votre Mac est votre ordinateur principal et critique pour votre activité. »*

---

## 4. La solution fonctionnelle : VM + Transfert USB

Puisque macOS ne peut pas exécuter les cartes ALFA nativement (et même s'il le pouvait, le mode moniteur ne fonctionnerait pas), la solution pratique pour les équipes de sécurité basées sur Mac est d'exécuter **Linux dans une machine virtuelle** et de transférer la carte ALFA via USB.

Cette approche fonctionne sur **tous les Mac Apple Silicon** (M1/M2/M3/M4) et tous les Mac Intel. Le mode moniteur et l'injection de paquets fonctionnent de manière identique à une machine Linux native.

### 5.1 Ce dont vous aurez besoin

| Composant | Recommandation | Coût |
|-----------|---------------|------|
| Logiciel VM | [UTM](https://mac.getutm.app/) (gratuit, open-source) | Gratuit |
| Alternative | Parallels Desktop ou VMware Fusion (ARM) | 99 $/an |
| ISO Linux | [Kali Linux ARM64](https://www.kali.org/get-kali/) | Gratuit |
| Carte ALFA | AWUS036ACH (meilleure) ou AWUS036ACM (Plug & Play) | 40–70 $ |
| Adaptateur USB | Adaptateur USB-C vers USB-A (si la carte ALFA a une fiche USB-A) | 10 $ |

### 5.2 Configuration étape par étape

#### Étape 1 : Créer une VM Kali Linux ARM

Téléchargez l'installateur Kali Linux ARM64 et créez une nouvelle VM dans UTM :
- **Architecture :** ARM64 (aarch64)
- **RAM :** 2 Go minimum (4 Go recommandé)
- **CPU :** 2+ cœurs
- **Contrôleur USB :** USB 3.0 (xHCI) — **c'est critique**

> [!IMPORTANT]
> Vous devez configurer le contrôleur USB de la VM comme **USB 3.0 (xHCI)**, pas USB 2.0. Les contrôleurs USB 2.0 causent des déconnexions intermittentes avec les cartes ALFA haute puissance, surtout pendant l'injection de paquets.

#### Étape 2 : Installer le pilote ALFA dans la VM

**Pour AWUS036ACH (RTL8812AU) :**

Si votre noyau Kali est **≥6.14**, le pilote mainline `rtw88` est déjà inclus — aucune installation nécessaire. Pour les noyaux plus anciens :

```bash
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r) git
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
sudo ./install-driver.sh
```

**Pour AWUS036ACM (MT7612U) — Zéro installation :**

Le pilote MediaTek MT7612U est dans le noyau Linux depuis la version 4.19. Branchez-le et ça fonctionne :

```bash
lsusb
# Bus 001 Device 005: ID 0e8d:7612 MediaTek Inc.

iw dev
# wlan0 devrait apparaître automatiquement
```

**Pour AWUS036AXML / AWUS036AXM (MT7921AUN) :**

Dans le noyau depuis Linux 5.18, mais nécessite des fichiers de firmware :

```bash
sudo apt install -y firmware-misc-nonfree
# Vérifier que le firmware existe :
ls /lib/firmware/mediatek/
# WIFI_MT7922_patch_mcu_1_1_hdr.bin
# WIFI_RAM_CODE_MT7922_1.bin
```

#### Étape 3 : Configurer le transfert USB

1. Branchez la carte ALFA dans le port USB-C/Thunderbolt de votre Mac (utilisez un adaptateur USB-C vers USB-A si nécessaire)
2. Dans UTM : barre de menus VM → USB → sélectionner l'appareil ALFA → assigner à la VM
3. Dans Parallels : Paramètres VM → Matériel → USB & Bluetooth → cocher « USB 3.0 » → assigner l'appareil ALFA à la VM

#### Étape 4 : Vérifier le mode moniteur et l'injection de paquets

```bash
# Vérifier que l'appareil est reconnu dans la VM
lsusb
# Bus 003 Device 005: ID 0bda:8812 Realtek ... RTL8812AU

# Activer le mode moniteur
sudo airmon-ng start wlan0
# (mac80211 monitor mode vif enabled for [phy1]wlan0 on [phy1]wlan0mon)

# Confirmer que le mode moniteur est actif
iw dev wlan0mon info
# Mode: monitor

# Tester la capacité d'injection de paquets
sudo aireplay-ng --test wlan0mon
# « Injection is working! » confirme le succès
```

### 5.3 Problèmes connus et dépannage

| Problème | Cause | Solution |
|-------|-------|----------|
| La carte se déconnecte lors de scans intensifs | Bug de commutation de mode USB 3.0 (morrownr/USB-WiFi #676) | Utiliser un hub USB 2.0 entre la carte et le Mac |
| `airmon-ng` ne voit pas la carte | Mauvais contrôleur USB dans les paramètres VM | Définir USB VM sur USB 3.0 (xHCI), pas USB 2.0 |
| Le pilote ne compile pas dans la VM | En-têtes de noyau manquants | `sudo apt install linux-headers-$(uname -r)` |
| Carte reconnue mais pas de mode moniteur | Chipset RTL8832BU (AWUS036AX/AXER) | Ce chipset a un support limité du mode moniteur ; utiliser AWUS036ACH à la place |

### 5.4 Alternative : Raspberry Pi comme nœud pentest dédié

Pour les équipes qui préfèrent une solution matérielle dédiée, un **Raspberry Pi 4 ou 5** sous Kali Linux constitue un excellent nœud d'audit sans fil portable. Le Mac est utilisé uniquement comme terminal SSH.

**Avantages :**
- Contourne complètement les problèmes de pilotes macOS
- AWUS036ACM est plug-and-play sur Pi (pilote intégré au noyau, zéro installation)
- Coût : Pi 5 + carte ALFA < 200 USD
- Portable et n'affecte pas la machine de travail principale

```bash
# Depuis votre Mac, connectez-vous en SSH au Pi :
ssh kali@192.168.1.100

# Exécutez l'audit sans fil sur le Pi :
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
sudo aireplay-ng --test wlan1mon
```

---

## 5. Guide matériel USB : Quel port utiliser sur quel Mac

Les cartes ALFA sont des appareils USB 2.0 ou USB 3.0, généralement avec un connecteur USB-A, consommant entre 500 mA (2,5 W) et 900 mA (4,5 W). Tous les ports USB Mac ne fournissent pas suffisamment d'alimentation — et le Mac Mini M4 (2024) présente une particularité critique que vous devez connaître.

### 6.1 Référence d'alimentation des ports USB Mac

| Modèle Mac | Ports USB-A | Alimentation USB-A | Ports USB-C/TB | Alimentation USB-C | Connexion directe ALFA ? |
|-----------|-------------|-------------|----------------|-------------|-------------------|
| MacBook 12" (2015–2017) | ❌ Aucun | N/A | 1× USB-C 3.1 Gen 1 | 900 mA | ❌ Adaptateur nécessaire |
| MacBook Air Intel (2010–2017) | ✅ 2× | 900 mA | 1× TB1/TB2 | N/A | ✅ Direct |
| MacBook Air Intel (2018–2020) | ❌ Aucun | N/A | 2× TB3 | 15 W / 7,5 W | ❌ Adaptateur nécessaire |
| MacBook Air M1/M2/M3 | ❌ Aucun | N/A | 2× TB/USB 4 | 15 W / 7,5 W | ❌ Adaptateur nécessaire |
| MacBook Pro Intel (2012–2015) | ✅ 2× | 900 mA | 2× TB2 | N/A | ✅ Direct (meilleure ère) |
| MacBook Pro Intel (2016–2019) | ❌ Aucun | N/A | 4× TB3 | 15 W / 7,5 W | ❌ Adaptateur nécessaire |
| MacBook Pro M1 (2020) | ❌ Aucun | N/A | 2× TB/USB 4 | 15 W / 7,5 W | ❌ Adaptateur nécessaire |
| MacBook Pro M1 Pro/Max (2021+) | ❌ Aucun | N/A | 3× TB4 | 15 W par port | ❌ Adaptateur nécessaire |
| MacBook Pro M2/M3/M4 Pro/Max | ❌ Aucun | N/A | 3× TB4 ou TB5 | 15 W+ par port | ❌ Adaptateur nécessaire |
| Mac Mini Intel (2014) | ✅ 4× | 900 mA | 2× TB2 | N/A | ✅ Direct |
| Mac Mini Intel (2018) | ✅ 2× | 900 mA | 4× TB3 | 15 W / 7,5 W | ✅ Direct |
| Mac Mini M1 (2020) | ✅ 2× | 900 mA | 2× TB/USB 4 | 15 W / 7,5 W | ✅ Direct |
| Mac Mini M2/M2 Pro (2023) | ✅ 2× | 900 mA | 2–4× TB4 | 15 W par port | ✅ Direct |
| **Mac Mini M4/M4 Pro (2024)** | **❌ Aucun** | **N/A** | Avant : 2× USB-C / Arrière : 3× TB4 ou TB5 | **Avant : 500 mA / Arrière : 900 mA+** | **❌ Ports TB arrière uniquement** |
| Mac Studio (toutes générations) | ✅ 2× (arrière) | 900 mA | 4× TB4 ou TB5 (arrière) | 15 W par port | ✅ Direct |

### 6.2 Avertissement critique : Mac Mini M4 (2024)

Le Mac Mini M4/M4 Pro est le **premier Mac Mini sans ports USB-A**. Plus important encore, les deux ports USB-C avant ne fournissent que **~500 mA** — insuffisant pour les cartes ALFA USB 3.0 qui nécessitent 900 mA.

> [!WARNING]
> Sur Mac Mini M4, **branchez toujours les cartes ALFA dans les ports Thunderbolt 4/5 arrière** en utilisant un adaptateur USB-C vers USB-A. Les ports USB-C avant (500 mA) provoqueront une instabilité d'alimentation et des coupures de connexion avec les cartes ALFA haute puissance.

### 6.3 Règles d'allocation d'alimentation Thunderbolt

- **Thunderbolt 3 (Mac Intel, 2016–2020) :** 15 W (3 A) pour les deux premiers ports, 7,5 W (1,5 A) pour les ports supplémentaires — selon le principe du premier arrivé, premier servi. Branchez votre carte ALFA en premier pour obtenir les 15 W complets.
- **Thunderbolt 4 (Apple Silicon, 2021+) :** 15 W (3 A) par port — sans limites d'allocation.
- **Ports USB-A (tous les Mac qui en ont) :** Toujours 900 mA (spec USB 3.0) — suffisant pour toute carte ALFA.

---

## 6. Recommandations d'achat par cas d'utilisation

### 7.1 Pour les utilisateurs de Mac Apple Silicon (M1/M2/M3/M4)

| Cas d'utilisation | Carte recommandée | Pourquoi | Méthode de configuration |
|----------|-----------------|-----|--------------| 
| **Meilleur mode moniteur & injection** | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | RTL8812AU — standard or de Kali Linux, pilote le plus mature | VM + Transfert USB |
| **Meilleure expérience Plug & Play** | [AWUS036ACM](https://yupitek.com/en/products/alfa/awus036acm/) | MT7612U — dans le noyau depuis Linux 4.19, zéro installation de pilote | VM + Transfert USB |
| **Tests WiFi 6E / 6 GHz** | [AWUS036AXML](https://yupitek.com/en/products/alfa/awus036axml/) | MT7921AUN — dans le noyau depuis Linux 5.18, tri-bande + BT 5.2 | VM + Transfert USB |
| **Budget / débutant** | [AWUS036ACS](https://yupitek.com/en/products/alfa/awus036acs/) | RTL8811AU — abordable, supporte mode moniteur + injection | VM + Transfert USB |
| **Nœud dédié portable** | [AWUS036ACM](https://yupitek.com/en/products/alfa/awus036acm/) | Zéro install sur Raspberry Pi, faible consommation (600 mA) | Raspberry Pi + Kali |

### 7.2 Pour les utilisateurs de Mac Intel (Connectivité client uniquement)

| Version macOS | Carte recommandée | Méthode de pilote | Limitation |
|---------------|-----------------|---------------|------------|
| 10.15 Catalina ou antérieur | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | Pilote ALFA officiel | Client uniquement — pas de mode moniteur |
| 11 Big Sur ou ultérieur | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | [Pilote chris1111](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) (désactiver SIP) | Client uniquement — pas de mode moniteur |

> [!IMPORTANT]
> Pour l'audit de sécurité sans fil sur **tout** Mac (Intel ou Apple Silicon), vous avez toujours besoin de Linux — soit dans une VM, soit sur un Raspberry Pi. Les pilotes macOS ne supportent pas le mode moniteur ou l'injection de paquets, point final.

### 7.3 Cartes à éviter pour les utilisateurs Mac

| Carte | Pourquoi éviter |
|------|-----------| 
| AWUS036AX / AWUS036AXER (RTL8832BU) | Support du mode moniteur limité et instable sous Linux ; pas de pilote macOS |
| AWUS036EACS (RTL8821CU) | Ne supporte **pas** du tout le mode moniteur — inadapté à l'audit de sécurité |
| AWUS036ACHM (MT7610U) | Pas de pilote macOS (chris1111 ne supporte pas MediaTek) ; nécessite compilation Linux |

---

## 7. FAQ : Cartes sans fil ALFA sur Apple Mac

> [!NOTE]
> Cette section FAQ est structurée pour l'Answer Engine Optimization (AEO). Chaque question reçoit une réponse définitive dans la première phrase afin que les moteurs de recherche alimentés par l'IA (ChatGPT, Perplexity, Google AI Overviews) puissent citer ces réponses directement.

### L'ALFA AWUS036ACH fonctionne-t-il sur Mac M1/M2/M3/M4 ?

**Non.** L'AWUS036ACH (RTL8812AU) ne fonctionne nativement sur aucun Mac Apple Silicon. Le pilote macOS de Realtek est compilé uniquement pour x86_64 et ne peut pas être chargé sur le noyau ARM64. Cependant, il fonctionne parfaitement dans une VM Linux (UTM/Parallels) avec transfert USB, incluant le support complet du mode moniteur et de l'injection de paquets.

### Puis-je utiliser des cartes sans fil ALFA pour le mode moniteur sur macOS ?

**Non.** Les pilotes macOS d'ALFA n'implémentent pas le mode moniteur ou l'injection de paquets — ils ne supportent que la connectivité client Wi-Fi basique. Cela s'applique à toutes les versions de macOS sur les Mac Intel et Apple Silicon. Pour le mode moniteur, vous devez utiliser Linux (soit dans une VM, soit sur un appareil séparé comme un Raspberry Pi).

### Quelle carte sans fil ALFA est la meilleure pour les utilisateurs Mac ?

Pour les utilisateurs Mac effectuant des audits de sécurité sans fil, l'**AWUS036ACH** (RTL8812AU) est le meilleur choix — c'est le standard or de Kali Linux pour le mode moniteur et l'injection de paquets. Pour une installation zéro plug & play dans une VM Linux, l'**AWUS036ACM** (MT7612U) est recommandé car son pilote est dans le noyau Linux depuis la version 4.19.

### Pourquoi ma carte ALFA ne fonctionne-t-elle pas sur mon MacBook Pro M3 ?

Les Mac Apple Silicon (M1/M2/M3/M4) utilisent un noyau ARM64 qui ne peut pas charger les extensions de noyau x86_64. Le pilote Wi-Fi macOS de Realtek est uniquement pour x86_64, et Rosetta 2 ne peut pas traduire les extensions de noyau. De plus, le framework NetworkingDriverKit d'Apple ne supporte que l'Ethernet, pas le Wi-Fi — il n'existe donc pas non plus de chemin DriverKit moderne. Realtek a abandonné le développement du pilote macOS.

### Existe-t-il un adaptateur USB Wi-Fi qui fonctionne sur Apple Silicon macOS ?

**Non.** En 2026, aucun adaptateur USB Wi-Fi tiers d'aucun fabricant (ALFA, TP-Link, Netgear, ASUS, etc.) ne fonctionne nativement sur Apple Silicon macOS. Il s'agit d'une limitation architecturale, pas d'un problème de disponibilité de pilotes. La recommandation officielle d'Apple est d'utiliser un routeur de voyage avec Ethernet à la place.

### Puis-je utiliser le Wi-Fi intégré du Mac pour le mode moniteur ?

**Oui, mais avec des limitations.** Le Wi-Fi intégré de macOS supporte le mode moniteur basique via l'utilitaire `airport` (`sudo airport en0 sniff 11`). Cependant, il ne capture que sur un canal à la fois, ne supporte pas l'injection de paquets, et l'antenne interne a une portée limitée. Pour l'audit sans fil professionnel, un adaptateur ALFA externe dans une VM Linux est nécessaire.

### Quelle est la façon la plus simple de faire fonctionner les cartes ALFA sur un Mac ?

La méthode la plus simple est : installer [UTM](https://mac.getutm.app/) (gratuit) → créer une VM Kali Linux ARM → brancher un AWUS036ACM (MT7612U) → l'assigner à la VM via le transfert USB. Le pilote MT7612U est dans le noyau depuis Linux 4.19, donc aucune installation de pilote n'est nécessaire — ça fonctionne immédiatement.

### Ai-je besoin d'un hub USB alimenté pour les cartes ALFA sur Mac ?

Sur les Mac avec ports USB-A (Mac Mini, Mac Studio, anciens MacBook Pro/Air), non — la sortie 900 mA est suffisante. Sur les Mac avec uniquement des ports USB-C/Thunderbolt, la sortie 15 W (3 A) est plus que suffisante. La seule exception concerne les ports USB-C avant du Mac Mini M4, qui ne fournissent que 500 mA — utilisez plutôt les ports Thunderbolt arrière.

---

## 8. Ressources & Liens de pilotes

### Ressources officielles

| Ressource | URL |
|----------|-----|
| Site officiel Yupitek | [https://www.yupitek.com](https://www.yupitek.com) |
| Page produits ALFA Yupitek | [https://yupitek.com/en/products/alfa/](https://yupitek.com/en/products/alfa/) |
| ALFA Network Officiel | [https://www.alfa.com.tw](https://www.alfa.com.tw) |
| Tableau comparatif ALFA Yupitek | [https://yupitek.com/alfa_compare.html](https://yupitek.com/alfa_compare.html) |

### Dépôts de pilotes Linux (GitHub)

| Chipset | Modèles ALFA | Dépôt GitHub | Type de pilote |
|---------|-------------|-------------------|-------------|
| RTL8812AU | AWUS036ACH, AWUS036ACS | [morrownr/8812au-20210820](https://github.com/morrownr/8812au-20210820) | DKMS (recommandé) |
| RTL8812AU | AWUS036ACH | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) | Communauté (déprécié) |
| RTL8812AU | AWUS036ACH | [lwfinger/rtw88](https://github.com/lwfinger/rtw88) | Mainline (noyau ≥6.14) |
| MT7612U | AWUS036ACM | Linux intégré au noyau (`mt76`) | Dans le noyau (≥4.19) |
| MT7921AUN | AWUS036AXML, AWUS036AXM | Linux intégré au noyau (`mt7921u`) | Dans le noyau (≥5.18) |
| MT7610U | AWUS036ACHM | [imzyxwvu/mt7610u](https://github.com/imzyxwvu/mt7610u) | Hors noyau |
| RTL8832BU | AWUS036AX, AWUS036AXER | [morrownr/USB-WiFi](https://github.com/morrownr/USB-WiFi) | Support limité |

### Pilote macOS (Mac Intel uniquement)

| Pilote | URL | macOS supporté | Apple Silicon |
|--------|-----|-----------------|---------------|
| chris1111 Wireless-USB-Big-Sur-Adapter | [GitHub](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) | Catalina – Tahoe 26 | ❌ Intel uniquement |

### Documentation développeur Apple

| Document | URL |
|----------|-----|
| Extensions du noyau dépréciées | [developer.apple.com/support/kernel-extensions/](https://developer.apple.com/support/kernel-extensions/) |
| NetworkingDriverKit (Ethernet uniquement) | [developer.apple.com/documentation/networkingdriverkit](https://developer.apple.com/documentation/networkingdriverkit) |
| Extension sécurisée du noyau | [support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web](https://support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web) |

### Logiciels VM

| Logiciel | URL | Coût |
|----------|-----|------|
| UTM | [mac.getutm.app](https://mac.getutm.app/) | Gratuit |
| Parallels Desktop | [parallels.com](https://www.parallels.com/) | 99 $/an |
| VMware Fusion | [vmware.com](https://www.vmware.com/products/fusion.html) | Gratuit pour usage personnel |

---

*Cet article est basé sur des recherches techniques compilées à partir de la documentation développeur Apple, des dépôts GitHub (chris1111, aircrack-ng, morrownr), des spécifications produits ALFA Network, des rapports de la communauté Reddit/GitHub et de la documentation de tests réels. Toutes les recommandations de produits sont basées sur la gamme de produits ALFA actuellement en stock de Yupitek.*

*⚠️ Les équipements et techniques décrits dans cet article sont destinés uniquement aux audits de sécurité des informations autorisés et aux tests de pénétration légaux. Les utilisateurs doivent s'assurer de la conformité avec les lois et réglementations locales.*

---
*Version de l'article : 1.0 | 2026-06-20 | Yupitek Ltd.*
