---
title: "HAK5 WiFi Pineapple Pager × ALFA Network : Guide de compatibilité des cartes Wi-Fi USB externes"
description: "Évaluation approfondie de la compatibilité et guide de configuration étape par étape pour connecter des cartes Wi-Fi USB d'ALFA Network au HAK5 WiFi Pineapple Pager sous OpenWrt. Découvre la compilation croisée MIPS, les limites d'alimentation USB 2.0 et le paramétrage des pilotes."
date: 2026-06-19
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi Pineapple Pager", "ALFA Network", "AWUS036ACM", "AWUS036ACH", "compatibility", "wireless-security"]
featureimage: "/images/blog/hak5-wifi-pineapple-pager-alfa-compatibility.webp"
---

# HAK5 WiFi Pineapple Pager × ALFA Network : Guide de compatibilité des cartes Wi-Fi USB externes

L'audit de sécurité sans fil exige une grande précision, de la polyvalence et un matériel adapté. Le **HAK5 WiFi Pineapple Pager** a attiré l'attention des professionnels de la sécurité en tant qu'outil d'audit ultraportable de poche, propulsé par le puissant moteur **PineAP v8**.

Cependant, pour maximiser la portée des audits, mener des opérations simultanées en double bande (2,4 GHz et 5 GHz) ou effectuer une surveillance passive multicanal sans interrompre les modules radio internes du Pineapple, une question revient souvent : **Puis-je connecter une carte Wi-Fi USB ALFA Network externe au HAK5 Pager ?**

La réponse courte est **oui, mais avec des contraintes matérielles et logicielles majeures**.

Dans ce guide complet, nous allons analyser les limitations techniques (telles que l'architecture du processeur et les limites d'alimentation du port USB), évaluer la compatibilité de la gamme actuelle d'adaptateurs ALFA Network et te fournir des instructions CLI étape par étape pour l'installation des pilotes et le dépannage.

---

## 1. Limitations techniques : ce que tu dois savoir

Avant de brancher une carte Wi-Fi USB de haute puissance sur le HAK5 Pager, tu dois comprendre deux obstacles majeurs : l'architecture du processeur et la puissance disponible sur le port USB.

### 1.1 Architecture du processeur : la contrainte MIPS
Contrairement à un PC classique sous Kali Linux qui fonctionne avec une architecture x86_64, ou à un Raspberry Pi basé sur ARM, le HAK5 Pager est conçu autour d'une puce **MediaTek MT7628AN SoC** (un cœur **MIPS32r2, Little-Endian**, compilé sous la plateforme `mipsel_24kc` dans OpenWrt).

> [!IMPORTANT]
> Comme le Pager OS est basé sur **OpenWrt (version 24.10.1, Kernel 6.6.86)**, il **ne prend pas en charge DKMS** (Dynamic Kernel Module Support). Tu ne peux pas compiler le code source des pilotes hors du noyau directement sur le Pager car le système manque d'outils de développement comme GCC et Make. Tout pilote non natif doit être compilé de manière croisée (cross-compiled) sur une machine Linux externe x86_64 à l'aide du SDK OpenWrt.

### 1.2 Alimentation USB 2.0 : le problème de chute de tension
Le HAK5 Pager dispose d'un seul port USB 2.0 Host. Selon les spécifications officielles de l'USB 2.0, un port standard peut fournir un courant maximum de **500 mA à 5V (2,5W)**.

Les adaptateurs Wi-Fi de haute puissance comme l'ALFA AWUS036ACH (RTL8812AU) ou l'ALFA AWUS036AXML (MT7921AUN) ont besoin de près de **720 mA (3,6W)** d'énergie lors de transmissions intenses (comme l'injection de paquets ou des scans de trafic denses).

> [!WARNING]
> Brancher une carte ALFA de haute puissance directement sur le port USB du Pager provoquera une chute de tension. Cela entraînera des **redémarrages du Pager, des pannes de noyau (Kernel Panic) ou des déconnections de la carte Wi-Fi**. Pour utiliser ces cartes de manière stable, tu **dois** connecter la carte ALFA via un **concentrateur (Hub) USB avec alimentation externe (5V/2A minimum)**.

---

## 2. Tableau de compatibilité des adaptateurs ALFA

Le tableau ci-dessous présente la compatibilité des adaptateurs USB actuels d'ALFA Network avec le HAK5 Pager sous Pager OS (Kernel 6.6) :

| Modèle ALFA | Puce | Bandes supportées | Consommation USB | Statut sous Kernel 6.6 | Méthode d'installation | Support de Monitor et Injection | Verdict & recommandation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AWUS036ACM** | MediaTek **MT7612U** | 2,4 GHz / 5 GHz | ~600 mA (Hub requis) | **Intégré au Kernel (Natif)** | Installation via `opkg` | ✅ Oui / ✅ Oui | 🏆 **Le standard absolu / Meilleur choix** |
| **AWUS036ACH** | Realtek **RTL8812AU** | 2,4 GHz / 5 GHz | ~720 mA (Hub alimenté requis) | Hors Kernel | Compilation croisée avec SDK | ✅ Oui / ✅ Oui | ⭐⭐ **Pour utilisateurs avancés** (Bug wiphy existant sur MIPS) |
| **AWUS036AXML** | MediaTek **MT7921AUN** | 2,4 / 5 / 6 GHz (Wi-Fi 6E) | ~720 mA (Hub alimenté requis) | **Intégré au Kernel (Natif)** | Installation via `opkg` + firmware manuel | ✅ Oui / ✅ Oui | ⭐⭐⭐ **Grand potentiel**, mais consommation élevée |
| **AWUS036ACHM** | MediaTek **MT7610U** | 2,4 GHz / 5 GHz | ~400 mA (Alimentation directe) | Partiellement intégré | Installation via `opkg` | ✅ Oui / ✅ Oui | ⭐⭐⭐ **Bonne option économique** |
| **AWUS036ACS** | Realtek **RTL8811AU** | 2,4 GHz / 5 GHz | ~500 mA (Limite) | Hors Kernel | Compilation croisée avec SDK | ✅ Oui / ✅ Oui | ⭐⭐ **Moyen** (Nécessite la compilation du pilote) |
| **AWUS036EACS** | Realtek **RTL8821CU** | 2,4 GHz / 5 GHz | ~500 mA | Hors Kernel | Non recommandé | ❌ **Pas de mode moniteur** | ❌ **Incompatible / Ne pas utiliser** |

---

## 3. Guide de configuration étape par étape

Voici les commandes CLI détaillées pour configurer les adaptateurs recommandés.

### 3.1 Scénario A : AWUS036ACM (MT7612U) — Plug & Play (Recommandé)

L'**AWUS036ACM** est le meilleur choix absolu pour le HAK5 Pager. Le pilote `mt76` de MediaTek est intégré de façon native dans le Kernel 6.6, éliminant le besoin de compiler.

#### Étape 1 : Brancher le matériel
1. Connecte le Hub USB avec alimentation externe au port USB du HAK5 Pager.
2. Connecte l'AWUS036ACM au Hub.
3. Connecte-toi au Pager via SSH :
   ```bash
   ssh root@172.16.42.1
   ```

#### Étape 2 : Vérifier la détection de la carte
Exécute la commande `lsusb` pour confirmer que le système détecte la puce MediaTek :
```bash
lsusb
# Tu devrais voir la ligne suivante :
# Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

#### Étape 3 : Installer les pilotes via opkg
Mets à jour le gestionnaire de paquets et installe les modules requis pour le pilote USB MT76 :
```bash
opkg update
opkg install kmod-mt76x2u kmod-mt76-usb firmware-utils
```

#### Étape 4 : Corriger le bug USB Scatter-Gather sur architecture MIPS
Sur les routeurs OpenWrt basés sur MIPS, le pilote `mt76-usb` peut planter lors du chargement du firmware si l'option USB Scatter-Gather (USB SG) est activée.

> [!TIP]
> Pour assurer la stabilité de la connexion sans fil et éviter les erreurs de chargement du firmware (erreur `-110`), tu dois désactiver la fonction USB Scatter-Gather en configurant un paramètre de module du noyau.

Crée le fichier `/etc/modules.d/mt76-usb-sg` et insère le paramètre de désactivation :
```bash
echo "mt76-usb disable_usb_sg=1" > /etc/modules.d/mt76-usb-sg
```
Redémarre le HAK5 Pager pour appliquer les modifications :
```bash
reboot
```

#### Étape 5 : Vérifier le mode moniteur et l'injection de paquets
Après le redémarrage, connecte-toi à nouveau en SSH et exécute :
```bash
iw dev
# Cherche la nouvelle interface sans fil (ex: wlan2)
```

Activer le mode moniteur :
```bash
ip link set wlan2 down
iw dev wlan2 set monitor none
ip link set wlan2 up
```
Vérifier l'état de l'interface :
```bash
iw dev wlan2 info
# La ligne suivante doit apparaître : "type monitor"
```

---

### 3.2 Scénario B : AWUS036ACH (RTL8812AU) — Compilation croisée via SDK

L'**AWUS036ACH** est une référence sur Kali Linux grâce à sa haute sensibilité, mais il n'est pas supporté nativement sous OpenWrt Kernel 6.6. Il doit être compilé de manière croisée.

#### Prérequis
- Un PC de développement sous Ubuntu 22.04 ou Debian 12 (x86_64).
- Le SDK OpenWrt correspondant à la cible `ramips/mt76x8` (celle du processeur du Pager).

#### Étape 1 : Télécharger le SDK OpenWrt sur le PC de compilation
Sur ta machine de compilation (Ubuntu) :
```bash
wget https://downloads.openwrt.org/releases/24.10.1/targets/ramips/mt76x8/openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
tar --zstd -xf openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
cd openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64
```

#### Étape 2 : Ajouter les sources du pilote rtl8812au
```bash
git clone https://github.com/aircrack-ng/rtl8812au.git package/kernel/rtl8812au
./scripts/feeds update -a
./scripts/feeds install -a
```

#### Étape 3 : Configurer et compiler le module du noyau
Ouvre le menu de configuration du SDK et sélectionne le pilote sans fil :
```bash
make menuconfig
# Va dans : Kernel modules -> Wireless Drivers -> Sélectionne kmod-rtl8812au
```
Compile le paquet :
```bash
make package/kernel/rtl8812au/compile V=s
```

#### Étape 4 : Transférer et installer le paquet sur le Pager
Le paquet d'installation `.ipk` compilé se trouve dans le dossier `bin/packages/mipsel_24kc/`. Copie-le sur le Pager :
```bash
scp bin/packages/mipsel_24kc/base/kmod-rtl8812au*.ipk root@172.16.42.1:/tmp/
ssh root@172.16.42.1 "opkg install /tmp/kmod-rtl8812au*.ipk"
```

> [!CAUTION]
> Sur l'architecture MIPS, le pilote hors-noyau `rtl8812au` peut provoquer des erreurs d'enregistrement du périphérique (`wiphy_register`), empêchant la carte d'apparaître sur le système. Pour y remédier, tu devras appliquer des correctifs (patches) spécifiques pour MIPS avant de lancer la compilation. C'est pourquoi nous te conseillons fortement de choisir plutôt l'**AWUS036ACM**.

---

## 4. Capacités d'audit de sécurité libérées

Connecter une carte ALFA compatible à ton HAK5 Pager te permet de débloquer plusieurs fonctionnalités avancées :

1. **Surveillance de la bande 5 GHz** : Les modules radio internes du Pager pouvant être limités selon ta version, l'ajout d'une carte externe double bande te garantit de pouvoir capturer les liaisons (handshakes) WPA/WPA2 et d'écouter les requêtes de sonde (probe requests) sur les fréquences modernes de 5 GHz.
2. **Radio d'attaque dédiée** : Tu peux réserver la radio interne du Pager pour simuler des points d'accès (Rogue AP / Evil Twin / KARMA) tout en configurant la carte ALFA externe (`wlan2`) pour l'injection continue de paquets de désassociation (Deauth).
3. **Intégration poussée avec PineAP** : Tu peux configurer la carte externe comme l'interface de surveillance principale dans l'interface Web PineAP ou via la CLI, ce qui accélère la capture des clients jusqu'à 100 fois.

---

## 5. Conclusion & Conseils d'achat

L'association d'une carte Wi-Fi d'ALFA Network avec le HAK5 WiFi Pineapple Pager te permet de déployer une station d'audit mobile discrète et très efficace. Reste toutefois vigilant sur les détails suivants :

- **Pour un déploiement rapide et stable** : Achète l'[ALFA AWUS036ACM](https://yupitek.com/en/products/alfa/awus036acm). Ses pilotes MediaTek intégrés fonctionnent parfaitement sous OpenWrt Kernel 6.6.
- **Stabilité de l'alimentation** : Utilise toujours un **Hub USB avec alimentation externe** de bonne qualité pour garantir le signal de sortie des cartes Wi-Fi de haute puissance et éviter les déconnections.

Si tu as d'autres questions techniques, besoin de devis matériel ou de compilations personnalisées via le SDK OpenWrt, contacte l'**Équipe de Support Technique de Yupitek** :

- 🌐 Site officiel : [www.yupitek.com](https://www.yupitek.com)
- 📧 E-mail du support : [sales@yupitek.com](mailto:sales@yupitek.com)
- 📞 Téléphone : +886-2-87325338
- 📍 Adresse : 1F., No. 72, Ln. 34, Fuyang St., Xinyi Dist., Taipei City, Taiwan
