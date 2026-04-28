---
title: "Guide Complet : Installation de tous les adaptateurs WiFi USB Alfa sous Linux en Chine - Kali, Ubuntu, Raspberry Pi"
date: 2026-04-24
draft: false
slug: "alfa-china-install-complete-guide"
tags: ["alfa", "kali-linux", "ubuntu", "raspberry-pi", "driver", "china", "monitor-mode", "packet-injection", "wireless"]
categories: ["Guides de Pilotes"]
series: ["Alfa China Install Guide"]
description: "Le guide ultime pour installer tous les adaptateurs WiFi USB Alfa sous Linux en Chine. Couvre Kali Linux, Ubuntu 22/24, Debian et Raspberry Pi. Aucun GitHub requis - utilisez uniquement des miroirs domestiques."
---

## Bienvenue dans le guide ultime d'installation d'Alfa sous Linux

Si vous lisez ceci, c'est probablement parce que vous avez acheté un adaptateur WiFi USB Alfa et que vous vous retrouvez bloqué car :

- Vous êtes en Chine et vous ne pouvez pas accéder à GitHub
- L'installation du pilote semble compliquée
- Vous devez activer le mode moniteur et l'injection de paquets pour des tests sans fil
- Vous ne savez pas de quel pilote votre modèle Alfa spécifique a besoin

Ce guide résout **tous ces problèmes**. Nous vous accompagnerons dans l'installation de **chaque adaptateur WiFi USB Alfa** sur **toutes les distributions Linux majeures**, en utilisant uniquement des **miroirs accessibles en Chine**. Pas de GitHub. Pas de frustration.

---

## Pourquoi ce guide existe

Les adaptateurs WiFi USB Alfa sont populaires parmi les testeurs d'intrusion, les ingénieurs réseau et les passionnés du sans fil. Ils prennent en charge le mode moniteur et l'injection de paquets — des fonctionnalités que la plupart des adaptateurs WiFi grand public n'ont pas.

Mais voici le problème : **la plupart des guides d'installation supposent que vous pouvez accéder à GitHub**. Si vous êtes en Chine, ce n'est pas possible. Ce guide est spécifiquement conçu pour les utilisateurs chinois, en utilisant uniquement des miroirs et des ressources qui fonctionnent au sein de l'infrastructure internet de la Chine.

---

## Référence Rapide des Modèles

Avant de commencer, identifions l'adaptateur Alfa que vous possédez et la puce qu'il utilise :

### Série AX (Wi-Fi 6 / 802.11ax)

| Modèle | Chipset | Pilote | Idéal Pour |
|-------|---------|--------|----------|
| AWUS036AX | Realtek RTL8832BU | `rtl8832bu` | Utilisation générale, bonne portée |
| AWUS036AXM | Realtek RTL8832BU | `rtl8832bu` | Design compact |

### Série AC (Wi-Fi 5 / 802.11ac)

| Modèle | Chipset | Pilote | Idéal Pour |
|-------|---------|--------|----------|
| AWUS036ACH | Realtek RTL8812AU | `88XXau` | Haute puissance, excellente portée |
| AWUS036ACM | MediaTek MT7612U | `mt76x2u` | **Meilleur support VIF**, plug-and-play |

---

## Avant de commencer : Ce dont vous avez besoin

Assurez-vous d'avoir ces éléments prêts avant de commencer :

1. **Adaptateur WiFi USB Alfa** — Le bon modèle pour vos besoins
2. **Câble USB** — Celui fourni dans la boîte fonctionne parfaitement
3. **Concentrateur USB alimenté** — Requis si vous êtes sur Raspberry Pi
4. **Connexion Internet active** — Pour accéder aux miroirs domestiques en Chine
5. **Privilèges Sudo** — Vous aurez besoin d'un accès administrateur

Branchez d'abord l'adaptateur pour vérifier que votre système le voit :

```bash
lsusb
```

---

## Référence des Miroirs Accessibles en Chine

Toutes les ressources de ce guide utilisent ces miroirs accessibles en Chine :

| Ressource | URL | Utilisation |
|----------|-----|---------|
| **Téléchargements officiels Alfa** | [files.alfa.com.tw](https://files.alfa.com.tw) | Packs de pilotes, micrologiciels |
| **Miroir Université Tsinghua** | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| **Miroir Aliyun** | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recommandé) |
| **Gitee (alternative à GitHub)** | [gitee.com](https://gitee.com) | Code source des pilotes |

---

## Installation sur Kali Linux

Kali Linux est livré avec des outils sans fil pré-installés. Faire fonctionner les adaptateurs Alfa ne prend que quelques étapes.

### Étape 1 : Passer au miroir chinois

```bash
sudo nano /etc/apt/sources.list
```

Remplacez tout par ceci :
`deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

```bash
sudo apt update
```

### Étape 2 : Installer le pilote par chipset

#### Série AX (RTL8832BU)
`sudo apt install -y rtl8832bu-dkms`

#### Série AC - Realtek (RTL8812AU / RTL8811AU)
`sudo apt install -y realtek-rtl88xxau-dkms`

---

## Dépannage

| Problème | Cause probable | Solution |
|---------|-------------|-----|
| `lsusb` n'affiche pas l'ID | Mauvais câble | Essayer un autre port USB |
| Le mode moniteur ne démarre pas | Conflit NetworkManager | Exécuter `sudo airmon-ng check kill` |

---

## Notes Finales

Ce guide couvre **tous les adaptateurs WiFi USB Alfa** sur **toutes les distributions Linux majeures**, en utilisant **uniquement des ressources accessibles en Chine**.

**Des questions ou des problèmes ?** Consultez les guides spécifiques aux modèles dans notre série, ou contactez-nous sur [yupitek.com](https://yupitek.com/fr/contact/).

---

*Dernière mise à jour : 24 avril 2026*
