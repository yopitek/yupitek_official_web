---
title: "Adaptateurs WiFi ALFA avec Kali NetHunter : Guide Technique Complet 2026"
description: "Référence technique pour les adaptateurs WiFi USB ALFA avec Kali NetHunter. Compatibilité smartphones du marché taïwanais, analyse des pilotes in-kernel vs DKMS, configuration OTG et résultats de tests vérifiés."
date: 2026-06-09
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["nethunter", "kali-linux", "alfa-network", "wireless-security", "android", "usb-otg", "monitor-mode", "packet-injection", "mt7610u", "mt7612u", "rtl8812au"]
---

Si tu as déjà configuré un adaptateur ALFA avec NetHunter en suivant les instructions OTG de base et que tu cherches la version rapide, notre [guide de configuration OTG](/fr/blog/alfa-adapter-nethunter-android-otg/) couvre l'essentiel. Cet article va plus loin — c'est une référence technique complète destinée aux professionnels de la sécurité qui ont besoin d'évaluer la compatibilité téléphone/adaptateur avant d'acheter le matériel, de comprendre quelle approche de pilote survit aux mises à jour du kernel, et de consulter des résultats de tests vérifiés avant de s'engager sur une combinaison spécifique.

Nous nous concentrons sur une question que la plupart des guides NetHunter ignorent : **quel adaptateur est vraiment plug-and-play, et lequel t'envoie dans un cauchemar de compilation de pilotes au pire moment possible ?** La réponse dépend du chipset, de la version du kernel du téléphone, et du fait que le pilote soit inclus dans l'arbre du kernel ou qu'il vive dans un dépôt DKMS externe. Te tromper signifie que ton adaptateur reste dans ton sac pendant que tu fixes des erreurs `modprobe` sur le terrain. Faire le bon choix signifie que tu le branches et que tu commences à scanner.

---

## 1. Exigences Client

### 1.1 Cas d'Usage

Les testeurs d'intrusion mobiles ont besoin d'une configuration qui remplace totalement le laptop. Le téléphone fait tourner Kali NetHunter, l'adaptateur ALFA se connecte via USB OTG, et l'opérateur réalise des évaluations de sécurité Wi-Fi sans transporter de notebook. Le flux de travail principal — survey de site, capture en mode monitor, injection de paquets, collecte de handshakes WPA — doit fonctionner de manière fiable sur batterie.

### 1.2 Exigences Principales

| Exigence | Détail |
|---|---|
| Plateforme | Téléphone Android avec Kali NetHunter (édition complète, kernel personnalisé) |
| Connexion | Câble USB OTG ou hub OTG alimenté |
| Adaptateur | Adaptateur WiFi USB ALFA avec support du mode monitor et de l'injection de paquets |
| Approche pilote | Prioriser les chipsets in-kernel (sans pilote externe) pour éliminer les dépendances de compilation |
| Marché taïwanais | Téléphones officiellement disponibles à Taïwan, modèles 2024–2026 |
| Alimentation | Fonctionnement sur batterie ; hub OTG alimenté fortement recommandé pour une utilisation soutenue |

---

## 2. Analyse du Matériel et des Logiciels Cibles

### 2.1 Téléphones Compatibles NetHunter Disponibles à Taïwan

NetHunter prend en charge plus de 117 modules de périphériques, mais la plupart sont des modèles anciens. Après filtrage pour les appareils qui sont (a) officiellement disponibles à Taïwan, (b) de 2024 ou plus récents, et (c) disposant de kernels NetHunter personnalisés fonctionnels, trois téléphones se démarquent :

| Modèle | Nom de Code | CPU | Versions Kernel | Images Pré-buildées | Disponibilité Taïwan |
|---|---|---|---|---|---|
| **OnePlus 11 5G** | salami | Snapdragon 8 Gen 2 (ARM64) | 2 | 2 | ✅ Disponible via canaux d'import, lancement 2023 |
| **Nothing Phone (1)** | spacewar | Snapdragon 778G+ (ARM64) | 3 | 1 | ✅ Lancé officiellement à Taïwan, communauté active |
| **Samsung Galaxy S20 FE 5G** | r8q | Snapdragon 865 (ARM64) | 5 | 1 | ✅ Vendu à Taïwan — **variante Snapdragon obligatoire** |

{{< alert "triangle-exclamation" >}}
**Avertissement Samsung Exynos :** La plupart des appareils Samsung vendus via les opérateurs taïwanais utilisent des chipsets Exynos. Les kernels NetHunter ne prennent en charge que la variante Snapdragon (`r8q`). Avant d'acheter un appareil Samsung pour NetHunter, vérifie le modèle du CPU — si l'annonce indique « Exynos », ça ne fonctionnera pas. Importe une unité Snapdragon ou choisis le OnePlus 11 à la place.
{{< /alert >}}

**NetHunter Rootless** fonctionne sur n'importe quel appareil Android sans root, mais il ne peut pas prendre en charge les adaptateurs WiFi USB externes pour le mode monitor. Si tu as besoin de capture de paquets et d'injection, tu as besoin de l'édition NetHunter complète avec un kernel personnalisé.

### 2.2 Spécifications Techniques de la Plateforme

En utilisant le OnePlus 11 5G comme plateforme de référence :

| Paramètre | Spécification |
|---|---|
| Architecture CPU | ARM64 (aarch64) |
| SoC | Qualcomm Snapdragon 8 Gen 2 (SM8550) |
| Contrôleur USB | USB 3.1 Gen 1 avec support OTG |
| Alimentation USB | 5V / 900mA (utilise un hub OTG alimenté pour un fonctionnement soutenu de l'adaptateur) |

### 2.3 Environnement Logiciel

| Composant | Exigence | Version Recommandée |
|---|---|---|
| OS hôte | Android avec chroot Kali | Android 11+ |
| NetHunter | Édition complète (kernel personnalisé) | 2024.4 (dernière stable) |
| Kernel Linux | Kernel personnalisé spécifique à l'appareil | 5.x ou ultérieur de préférence |
| Pilotes préchargés | Voir Section 4 pour la matrice | — |
| DKMS | Requis uniquement pour les adaptateurs basés sur RTL8812AU | Les headers du kernel doivent correspondre |
| Outils sans fil | aircrack-ng, Kismet, MANA Toolkit | Fournis par le chroot NetHunter |
| Root | Requis pour la fonctionnalité complète | Magisk 26.0+ |

---

## 3. Spécifications des Adaptateurs ALFA et Sources des Pilotes

### 3.1 AWUS036ACHM — Choix Principal pour NetHunter

| Paramètre | Spécification |
|---|---|
| Chipset | **MediaTek MT7610U** |
| USB VID/PID | `0x0e8d:0x7610` |
| Bandes | 2,4 GHz + 5 GHz (AC433) |
| Débit max | 150 Mbps (2,4 GHz) / 433 Mbps (5 GHz) |
| USB | USB 2.0 |
| Mode Monitor | ✅ Support complet |
| Injection de paquets | ✅ Support complet |
| Antenne | 1× amovible haut gain (RP-SMA) |
| Pilote | **In-kernel** — aucune installation requise |
| Module kernel | `mt76x0u` |
| Kernel requis | Linux 4.19+ |
| Page produit | [/fr/products/alfa/awus036achm/](/fr/products/alfa/awus036achm/) |

Le chipset MT7610U est largement recommandé par les communautés Kali et NetHunter car son pilote `mt76x0u` est intégré au kernel Linux mainline depuis la version 4.19. Tu le branches, le kernel le reconnaît, et tu commences à travailler. Pas de chaîne de compilation, pas de headers kernel, pas de DKMS — juste une confirmation `lsusb` suivie de `airmon-ng start`.

### 3.2 AWUS036ACM — Alternative Haute Performance

| Paramètre | Spécification |
|---|---|
| Chipset | **MediaTek MT7612U** |
| USB VID/PID | `0x0e8d:0x7612` |
| Bandes | 2,4 GHz + 5 GHz (AC1200) |
| Débit max | 300 Mbps (2,4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| Mode Monitor | ✅ Support complet |
| Injection de paquets | ✅ Confirmé stable sur Kali 2024.3 / 2025.1 |
| Antenne | 2× antennes duales (RP-SMA), MIMO 2T2R |
| Pilote | **In-kernel** — aucune installation requise |
| Module kernel | `mt76x2u` |
| Kernel requis | Linux 4.19+ |
| Page produit | [/fr/products/alfa/awus036acm/](/fr/products/alfa/awus036acm/) |

L'ACM ajoute le dual-band AC1200 avec MIMO 2T2R et le débit USB 3.0. Le pilote `mt76x2u` est également mainline depuis le kernel 4.19. Une réserve : certains anciens kernels NetHunter personnalisés (notamment le kernel du OnePlus 7T en version 4.14) ont été compilés sans le module `mt76x2u`. Sur n'importe quel kernel 4.19 ou ultérieur, ce n'est pas un problème, mais vérifie avec `lsmod | grep mt76x2u` si ton appareil utilise un kernel plus ancien.

### 3.3 AWUS036ACH — Support Communautaire le Plus Large

| Paramètre | Spécification |
|---|---|
| Chipset | **Realtek RTL8812AU** |
| USB VID/PID | `0x0bda:0x8812` |
| Bandes | 2,4 GHz + 5 GHz (AC1200) |
| Débit max | 300 Mbps (2,4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| Mode Monitor | ✅ Support complet |
| Injection de paquets | ✅ Support complet |
| Antenne | 2× externes 5dBi (RP-SMA) |
| Pilote | DKMS externe (pré-compilé dans la plupart des kernels NetHunter) |
| Module kernel | `88XXau` |
| Dépôt du pilote | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| Page produit | [/fr/products/alfa/awus036ach/](/fr/products/alfa/awus036ach/) |

L'ACH est le standard de facto pour les configurations Kali et NetHunter depuis des années. La plupart des kernels NetHunter personnalisés sont livrés avec le module `88XXau` pré-compilé, donc tu n'as généralement pas besoin de compiler depuis les sources. Cependant, si ta version du kernel ne l'inclut pas, tu auras besoin d'un environnement de compilation fonctionnel avec les headers du kernel correspondants — exactement le type de chaîne de dépendances que les chipsets MT7610U et MT7612U évitent. Les deux antennes 5dBi lui donnent la portée de signal la plus élevée de la gamme, ce qui est important pour les scénarios de capture longue distance.

### 3.4 AWUS036ACS — Format Compact

| Paramètre | Spécification |
|---|---|
| Chipset | Realtek RTL8811AU |
| USB VID/PID | `0x0bda:0x0811` |
| Bandes | 2,4 GHz + 5 GHz (AC433) |
| USB | USB 2.0 |
| Mode Monitor | ✅ Supporté (même famille de pilotes que RTL8812AU) |
| Injection de paquets | ✅ Supportée |
| Antenne | Interne, corps ultra-fin de 55 mm |
| Consommation | ~300mW — la plus basse de la gamme |
| Pilote | Externe (dépôt aircrack-ng partagé avec RTL8812AU) |
| Page produit | [/fr/products/alfa/awus036acs/](/fr/products/alfa/awus036acs/) |

L'ACS est l'option la plus portable. Avec une consommation de 300mW, c'est le moins exigeant pour les batteries de téléphone, et son format fin disparaît dans une poche. Le compromis : des performances AC433 single-stream et la dépendance au pilote DKMS externe partagée avec la famille RTL8812AU.

### 3.5 Adaptateurs Non Recommandés pour NetHunter

| Adaptateur | Chipset | Raison |
|---|---|---|
| AWUS036AX / AWUS036AXER | RTL8832BU | Nécessite kernel 6.14+ ; stabilité du mode monitor non vérifiée sur les kernels Android |
| AWUS036AXML / AWUS036AXM | MT7921AUN | Support WiFi 6E / 6 GHz instable dans les builds NetHunter actuelles ; inadapté comme adaptateur de pentest principal |

### 3.6 Dépôts des Sources des Pilotes

| Chipset | Pilote | Source |
|---|---|---|
| MT7610U | `mt76x0u` (in-kernel) | [torvalds/linux — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| MT7612U | `mt76x2u` (in-kernel) | Même arbre kernel que ci-dessus |
| RTL8812AU | `88XXau` (externe) | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| RTL8811AU | `88XXau` (externe, partagé) | Même dépôt aircrack-ng |

---

## 4. Analyse de Compatibilité des Pilotes

### 4.1 In-Kernel vs DKMS Externe

La décision la plus importante quand tu choisis un adaptateur pour NetHunter est de savoir si le pilote réside dans l'arbre du kernel ou à l'extérieur. Voici pourquoi :

| | In-Kernel (MT7610U, MT7612U) | DKMS Externe (RTL8812AU, RTL8811AU) |
|---|---|---|
| Plug-and-play | ✅ Oui — reconnu à l'insertion | ⚠️ Dépend du fait que le kernel ait `88XXau` pré-compilé |
| Survit aux mises à jour du kernel | ✅ Oui — le pilote fait partie du build kernel | ❌ Peut casser après mise à jour ; nécessite recompilation |
| Nécessite linux-headers | ❌ Non | ✅ Oui, si compilation manuelle requise |
| Nécessite DKMS | ❌ Non | ✅ Oui, si non pré-compilé dans le kernel |
| Documentation communautaire | Modérée | Large (l'ACH a le plus de tutoriels) |
| Risque d'échec sur le terrain | Faible | Modéré (dépendance de compilation) |

**En résumé :** Si tu veux le risque le plus bas possible de problèmes de pilotes sur le terrain, choisis un adaptateur MT7610U ou MT7612U. Le pilote est déjà dans le kernel — il n'y a rien à compiler, rien qui peut casser lors d'une mise à jour, et rien à dépanner quand tu es sur site.

### 4.2 Matrice de Support des Modules Kernel NetHunter

| Appareil | Kernel NetHunter | MT7610U (`mt76x0u`) | MT7612U (`mt76x2u`) | RTL8812AU (`88XXau`) |
|---|---|---|---|---|
| OnePlus 11 5G | Kernel Android 13 | ✅ Supporté | ✅ Supporté | ✅ Supporté |
| Samsung S20 FE (Snapdragon) | Kernel Android 12 (4.19) | ✅ Supporté | ✅ Supporté | ✅ Supporté (vérifier les rapports XDA) |
| Nothing Phone (1) | Kernel Android 12/13 | ✅ Supporté | Vérifier la config kernel | ✅ Supporté |
| OnePlus 7/7T | 4.14 (ancien) | ✅ Supporté | ⚠️ Peut être absent du build | ✅ Supporté |

Sources : NetHunter GitLab, rapports communautaires XDA Forums (2024–2026).

### 4.3 Problèmes Connus

**Problème 1 : L'interface MT7612U n'apparaît pas sur les anciens kernels**

Symptôme : `lsusb` montre `0e8d:7612` mais `ip link` n'affiche aucun `wlan1`.  
Cause racine : Le kernel personnalisé a été compilé sans le module `mt76x2u`. Cela affecte certains kernels NetHunter basés sur 4.14 (ère OnePlus 7T).  
Solution : Utilise un build kernel qui inclut le module, ou passe au AWUS036ACHM (MT7610U) qui a un support plus large sur les anciens kernels.

**Problème 2 : La chute de tension USB provoque des déconnexions de l'adaptateur**

Symptôme : L'adaptateur disparaît en milieu de scan, `dmesg` montre des erreurs de reset USB.  
Cause racine : Le port USB du téléphone ne peut pas maintenir la consommation de courant de l'adaptateur, surtout pour les adaptateurs USB 3.0 (l'ACH consomme ~500mW).  
Solution : Utilise un hub OTG alimenté qui fournit 5V à l'adaptateur depuis un chargeur secteur tout en transmettant les données au téléphone.

**Problème 3 : Adaptateur inséré avant le démarrage du chroot**

Symptôme : Android affiche la boîte de dialogue de permission USB, mais les outils Kali ne peuvent pas accéder à l'adaptateur.  
Cause racine : L'environnement chroot NetHunter doit être en cours d'exécution avant que les périphériques USB lui soient exposés.  
Solution : Démarre le chroot d'abord (Kali Services → Start), puis connecte l'adaptateur et accorde la permission USB.

---

## 5. Guide de Configuration

### 5.1 Prérequis

Avant de connecter un quelconque matériel, vérifie :

```bash
# Confirmer que l'appareil est rooté
su -c "id"

# Vérifier la version du chroot NetHunter
cat /kali/etc/os-release
# Doit afficher Kali Linux avec NetHunter

# Confirmer que l'USB OTG est activé
# Paramètres → Options développeur → OTG (l'emplacement exact varie selon la version Android)
```

### 5.2 Séquence de Connexion Matérielle

L'ordre est important :

1. Lance l'**application NetHunter** → ouvre **Kali Services** → appuie sur **Start** pour démarrer le chroot
2. Connecte le **hub OTG alimenté** au port USB de ton téléphone
3. Branche l'**adaptateur ALFA** dans le hub OTG
4. Quand la boîte de dialogue de permission USB Android apparaît, appuie sur **OK** et coche **Toujours autoriser**

{{< alert "circle-info" >}}
Un hub OTG alimenté est fortement recommandé pour un fonctionnement soutenu. L'AWUS036ACH consomme environ 500mW — l'alimenter directement depuis la batterie du téléphone accélère significativement la décharge et peut causer une instabilité USB. Un hub qui transmet les données tout en tirant l'alimentation d'un chargeur secteur élimine les deux problèmes.
{{< /alert >}}

### 5.3 Vérifier la Détection de l'Adaptateur

```bash
# Lister les périphériques USB — confirmer que l'adaptateur apparaît
lsusb

# Sortie attendue par modèle :
# AWUS036ACHM: Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.
# AWUS036ACM:  Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U
# AWUS036ACH:  Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp.
```

Si l'adaptateur n'apparaît pas : essaie un autre câble OTG, vérifie que l'OTG est activé dans les options développeur, ou teste l'adaptateur sur un ordinateur pour confirmer qu'il est fonctionnel.

### 5.4 Charger le Pilote

**Pour MT7610U (AWUS036ACHM) — chargement automatique sur la plupart des kernels :**

```bash
# Vérifier le chargement automatique
lsmod | grep mt76

# Chargement manuel si nécessaire (rare)
sudo modprobe mt76x0u
```

**Pour MT7612U (AWUS036ACM) — chargement automatique sur kernel 4.19+ :**

```bash
# Vérifier
lsmod | grep mt76

# Chargement manuel si nécessaire
sudo modprobe mt76x2u
```

**Pour RTL8812AU (AWUS036ACH) — pré-compilé dans la plupart des kernels NetHunter :**

```bash
# Charger le module pré-compilé
sudo modprobe 88XXau

# Vérifier qu'il est chargé
lsmod | grep 88XX
```

### 5.5 Confirmer l'Interface Réseau

```bash
# Lister les interfaces sans fil
ip link show | grep wlan

# Ou utiliser iw
iw dev

# L'adaptateur externe apparaît généralement comme wlan1
# (wlan0 est habituellement le WiFi intégré du téléphone)
```

### 5.6 Activer le Mode Monitor

```bash
# Tuer les processus interférents
sudo airmon-ng check kill

# Démarrer le mode monitor sur l'adaptateur
sudo airmon-ng start wlan1

# Vérifier que le mode monitor est actif
iwconfig wlan1mon
# Sortie attendue : Mode:Monitor

# Scanner les réseaux à proximité (tests autorisés uniquement)
sudo airodump-ng wlan1mon

# Scanner toutes les bandes (2,4 GHz + 5 GHz)
sudo airodump-ng --band abg wlan1mon
```

### 5.7 Revenir au Mode Managed

```bash
sudo airmon-ng stop wlan1mon
sudo service NetworkManager restart
```

---

## 6. Topologie Applicative

![Diagramme d'architecture NetHunter + ALFA](/images/blog/nethunter-topology.png)

---

## 7. Résultats de Validation

### 7.1 Matrice de Tests

Les combinaisons suivantes ont été vérifiées via des tests communautaires et la documentation des fabricants :

| Téléphone | Adaptateur ALFA | Chipset | Mode Monitor | Injection Paquets | Statut |
|---|---|---|---|---|---|
| OnePlus 11 5G | AWUS036ACHM | MT7610U | ✅ | ✅ | Vérifié |
| OnePlus 11 5G | AWUS036ACM | MT7612U | ✅ | ✅ | Vérifié |
| OnePlus 11 5G | AWUS036ACH | RTL8812AU | ✅ | ✅ | Vérifié |
| Samsung S20 FE (Snapdragon) | AWUS036ACH | RTL8812AU | ✅ | ⚠️ | Rapports communautaires — vérifier la config kernel |
| Samsung S20 FE (Snapdragon) | AWUS036ACHM | MT7610U | ✅ | ✅ | Rapports communautaires |
| Nothing Phone (1) | AWUS036ACHM | MT7610U | ✅ | ✅ | Rapports communautaires |

Sources : XDA Forums, Reddit r/NetHunter, Kali NetHunter GitLab Issues (2024–2026).

### 7.2 Sortie `lsusb` Attendue

```
# AWUS036ACHM
Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.

# AWUS036ACM
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter

# AWUS036ACH
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
```

### 7.3 Vérification du Mode Monitor

```bash
# Sortie iwconfig attendue en cas de succès
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.437 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

---

## 8. Recommandations

### 8.1 Choix Principal : OnePlus 11 5G + AWUS036ACHM

Cette combinaison a la friction la plus basse de toutes les configurations testées. Le OnePlus 11 est le flagship le plus récent avec support officiel du kernel NetHunter que tu peux encore obtenir pour le marché taïwanais. Le chipset MT7610U de l'AWUS036ACHM utilise le pilote `mt76x0u` — il est dans le kernel mainline depuis la 4.19, ne nécessite aucune compilation, et la communauté internationale de sécurité (Lab401, base de données USB-WiFi de morrownr) le classe systématiquement comme le choix le plus sûr pour Kali et NetHunter. L'adaptateur est compact, mono-antenne, et fonctionne en USB 2.0, ce qui est un avantage en scénario mobile — consommation plus faible, moins de chaleur, moins de risques de panne.

### 8.2 Choix Performance : OnePlus 11 5G + AWUS036ACM

Si tu as besoin de performances dual-band AC1200 avec MIMO 2T2R pour la capture 5 GHz à distance, l'ACM te les donne sans quitter l'écosystème des pilotes in-kernel. Le pilote `mt76x2u` du MT7612U est également mainline depuis la 4.19. Le compromis : l'USB 3.0 consomme plus et le corps à double antenne est plus volumineux. Vérifie que le kernel inclut `mt76x2u` — sur le OnePlus 11, c'est confirmé.

### 8.3 Favori de la Communauté : N'importe Quel Appareil NetHunter + AWUS036ACH

L'ACH a le plus de tutoriels, la plus grande base de dépannage communautaire, et la meilleure documentation tierce de tous les adaptateurs de l'écosystème NetHunter. Ses deux antennes 5dBi lui donnent la portée de signal la plus élevée de la gamme ALFA. La plupart des kernels NetHunter pré-compilent le module `88XXau`, donc la compilation est rarement nécessaire. Si tu valorises le support communautaire et la capture longue distance plus que la simplicité plug-and-play, c'est le bon choix.

### 8.4 Sélection par Scénario

| Scénario | Combinaison Recommandée | Justification |
|---|---|---|
| Première config NetHunter, minimiser les risques | OnePlus 11 + AWUS036ACHM | Pilote in-kernel, pas de compilation, format le plus compact |
| Capture dual-band avec portée | OnePlus 11 + AWUS036ACM | AC1200 + MIMO, toujours in-kernel |
| Survey longue distance, maximum de tutoriels | N'importe quel appareil supporté + AWUS036ACH | Antenne la plus puissante, support communautaire le plus large |
| Ultra-portable, consommation minimale | N'importe quel appareil supporté + AWUS036ACS | 300mW de consommation, tient dans n'importe quelle poche |

### 8.5 Ressources de Support

| Ressource | Lien |
|---|---|
| Yupitek — distributeur agréé ALFA Taïwan | [yupitek.com](https://www.yupitek.com) |
| Pages produits officielles ALFA Network | [alfa.com.tw](https://www.alfa.com.tw) |
| Pilote MT7610U (arbre kernel) | [torvalds/linux — mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| Pilote RTL8812AU (aircrack-ng) | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| Appareils supportés NetHunter | [nethunter.kali.org/device-kernels.html](https://nethunter.kali.org/device-kernels.html) |
| Documentation officielle NetHunter | [kali.org/docs/nethunter/](https://www.kali.org/docs/nethunter/) |
| Forum XDA NetHunter | [xdaforums.com/tags/nethunter/](https://xdaforums.com/tags/nethunter/) |
| Catalogue produits ALFA Yupitek | [/fr/products/alfa/](/fr/products/alfa/) |

---

## Annexe : Dépannage Rapide

**Adaptateur absent de `lsusb` :**
1. Confirme que l'OTG est activé dans les Options développeur
2. Essaie un autre câble OTG — la qualité du câble est le point de défaillance le plus courant
3. Utilise un hub OTG alimenté
4. Vérifie que le chroot NetHunter a été démarré

**Le périphérique apparaît dans `lsusb` mais pas d'interface `wlan1` :**

```bash
# Vérifier les messages kernel pour les erreurs de pilote
dmesg | tail -30 | grep -E "usb|mt76|rtl|88XX"

# Vérifier que le module kernel existe
find /lib/modules -name "mt76*" 2>/dev/null
find /lib/modules -name "*88XX*" 2>/dev/null

# Tenter un chargement manuel
sudo modprobe mt76x0u   # MT7610U
sudo modprobe mt76x2u   # MT7612U
sudo modprobe 88XXau    # RTL8812AU
```

**Le mode monitor démarre mais aucun réseau n'apparaît :**

```bash
# Tuer d'abord les processus interférents
sudo airmon-ng check kill

# Rescanner toutes les bandes
sudo airodump-ng --band abg wlan1mon

# Vérifier les paramètres de canal
sudo iw dev wlan1mon info
```

**L'adaptateur se déconnecte pendant l'utilisation (reset USB) :**

```bash
# Solution temporaire — réduire la puissance de transmission
sudo iw dev wlan1 set txpower fixed 1000  # 10 dBm

# Solution permanente — utiliser un hub OTG alimenté
```

---

## Guides Connexes

- [Configuration OTG de base avec les adaptateurs ALFA et NetHunter](/fr/blog/alfa-adapter-nethunter-android-otg/)
- [Guide d'achat des adaptateurs WiFi ALFA 2026](/fr/blog/alfa-wifi-adapter-buyer-guide-2026/)
- [Installer les pilotes ALFA sur Kali Linux et Ubuntu](/fr/blog/install-alfa-driver-kali-ubuntu/)
- [Utiliser les adaptateurs ALFA avec Raspberry Pi et Kali](/fr/blog/alfa-adapter-raspberry-pi-kali/)

---

*Ce document a été préparé par **Yupitek Ltd** — distributeur agréé ALFA Network pour Taïwan.*  
*Données à jour au 09/06/2026. Les versions du kernel Linux et de NetHunter sont mises à jour régulièrement ; vérifie les sources officielles pour les dernières informations de compatibilité.*
