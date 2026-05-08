---
title: "Activer le mode moniteur sur Kali Linux 2026 : Guide complet"
description: "Guide étape par étape pour activer le mode moniteur sur Kali Linux 2024/2025 avec airmon-ng ou la commande iw. Couvre les adaptateurs ALFA compatibles, le dépannage et la vérification avec airodump-ng."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["monitor-mode", "kali-linux", "airmon-ng", "iw", "wifi-adapter", "ALFA-Network"]
---

# Activer le mode moniteur sur Kali Linux 2026 : Guide complet

Le mode moniteur est l'une des fonctionnalités les plus importantes pour le test de pénétration sous Linux. Il permet à votre adaptateur WiFi de capturer tout le trafic sans fil de votre environnement — pas seulement celui qui vous est destiné.

---

## Qu'est-ce que le mode moniteur ?

En mode géré (le mode standard), votre adaptateur communique uniquement avec les points d'accès auxquels il est connecté. En **mode moniteur**, l'adaptateur écoute sur tous les canaux et capture **tous** les trames 802.11 de votre environnement — y compris les poignées, les frames de désauthentification, les requêtes de sonde et plus encore.

---

## Méthode A : airmon-ng (Recommandé)

```bash
# Vérifier et tuer les processus gênants
sudo airmon-ng check kill

# Démarrer le mode moniteur
sudo airmon-ng start wlan0

# Vérifier
iwconfig
```

Vous devriez voir `wlan0mon` comme interface de mode moniteur.

---

## Méthode B : iw (Manuel)

```bash
# Déplacer l'interface
sudo ip link set wlan0 down

# Basculer en mode moniteur
sudo iw dev wlan0 set type monitor

# Remonter
sudo ip link set wlan0 up
```

---

## Vérification avec airodump-ng

```bash
sudo airodump-ng wlan0mon
```

Vous devriez immédiatement voir des réseaux WiFi apparaître dans la sortie. Appuyez sur `Ctrl+C` pour arrêter.

---

## Adaptateurs ALFA compatibles

| Adaptateur | Puce | airmon-ng | iw |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | ✓ | ✓ |
| AWUS036AXML | MT7921AUN | ✓ | ✓ |
| AWUS036ACM | MT7612U | ✓ | ✓ |
| AWUS036AX | RTL8832BU | ✓ | ✓ |

---

## Dépannage

**Problème :** Interface non trouvée

**Solution :** Assurez-vous que le pilote est chargé :

```bash
lsmod | grep -E "88XXau|mt7921u|mt76"
```

**Problème :** Le mode moniteur démarre mais aucun trafic capturé

**Solution :** Vérifiez le canal actuel et définissez-le manuellement :

```bash
iwconfig wlan0mon
sudo iwconfig wlan0mon channel 6
```
