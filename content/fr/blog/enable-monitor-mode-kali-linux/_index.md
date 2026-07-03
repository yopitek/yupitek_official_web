---
title: "Activer le mode moniteur sur Kali Linux 2026 : Guide complet"
description: "Guide étape par étape pour activer le mode moniteur sur Kali Linux 2024/2025 avec airmon-ng ou la commande iw. Couvre les adaptateurs ALFA compatibles, le dépannage et la vérification avec airodump-ng."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["monitor-mode", "kali-linux", "airmon-ng", "iw", "wifi-adapter", "ALFA-Network"]
featureimage: "/images/blog/enable-monitor-mode-kali-linux.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Quelle est la différence entre le mode moniteur et le mode managed ?"
    answer: "Le mode moniteur permet à la carte de capturer toutes les trames 802.11 dans l'air, contrairement au mode managed qui ne reçoit que les paquets destinés à son propre MAC. C'est la base du pentesting sans fil."
  - question: "Quelle est la différence entre airmon-ng et iw pour activer le mode moniteur ?"
    answer: "airmon-ng gère automatiquement les processus interférents et crée une interface virtuelle wlan0mon. iw modifie directement l'interface existante sans en créer de nouvelle, pour un contrôle plus fin."
  - question: "Que faire si l'interface revient en mode managed après activation du mode moniteur ?"
    answer: "wpa_supplicant ou NetworkManager redémarre en arrière-plan. Exécutez airmon-ng check kill pour terminer ces processus."
  - question: "Quelles cartes ALFA supportent pleinement le mode moniteur sur Kali Linux ?"
    answer: "L'AWUS036ACH (RTL8812AU), l'AWUS036AXML (MT7921AUN) et l'AWUS036ACM (MT7612U) supportent toutes le mode moniteur. L'ACM est plug-and-play."
  - question: "Comment résoudre l'erreur Fixed channel wlan0mon: -1 dans airodump-ng ?"
    answer: "airdump-ng ne peut pas changer de canal. Exécutez iwconfig wlan0mon channel 1 pour définir le canal et terminez les processus wpa_supplicant résiduels."
---

{{< tldr >}}
Le mode moniteur lève la restriction où la carte ne reçoit que ses propres paquets, c'est la base du pentesting sans fil. Utilisez airmon-ng ou iw avec une carte ALFA sur Kali Linux pour l'activer stablement.
{{< /tldr >}}

En mode géré (le mode standard), votre adaptateur communique uniquement avec les points d'accès auxquels il est connecté. En **mode moniteur**, l'adaptateur écoute sur tous les canaux et capture **tous** les trames 802.11 de votre environnement — y compris les poignées, les frames de désauthentification, les requêtes de sonde et plus encore.


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

{{< faq >}}

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

---

## Références
1. [Documentation officielle aircrack-ng](https://www.aircrack-ng.org/documentation.html)
2. [Documentation officielle Kali Linux](https://www.kali.org/docs/)
3. [Sous-système mac80211 Linux Wireless](https://wireless.wiki.kernel.org/en/developers/Documentation/mac80211)
4. [Guide d'utilisation de la commande iw](https://wireless.wiki.kernel.org/en/users/Documentation/iw)
