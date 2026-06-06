---
title: "Qu'est-ce que l'injection de paquets ? Tester la compatibilité de votre adaptateur WiFi avec Kali Linux"
description: "Comprenez l'injection de paquets WiFi, pourquoi elle nécessite des adaptateurs spécifiques, comment tester votre adaptateur ALFA Network avec aireplay-ng et quelles puces supportent l'injection sur Kali Linux."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["packet-injection", "aireplay-ng", "kali-linux", "wifi-adapter", "RTL8812AU", "ALFA-Network"]
featureimage: "/images/blog/packet-injection-guide.webp"
---

# Qu'est-ce que l'injection de paquets ? Tester la compatibilité de votre adaptateur WiFi avec Kali Linux

L'injection de paquets est l'une des capacités les plus importantes pour les adaptateurs de test de pénétration. Elle vous permet d'envoyer n'importe quelles trames 802.11 dans le réseau sans fil — y compris les frames de désauthentification, la manipulation des poignées et plus encore.

---

## Qu'est-ce que l'injection de paquets ?

L'injection de paquets est la capacité d'un adaptateur WiFi à **envoyer n'importe quelles trames** — pas seulement celles qui lui sont destinées. Cela permet des attaques telles que :

- **Attaques de désauthentification** — Couper les connexions des clients
- **Authentification fake** — Créer des points d'accès fake
- **Rejeu de paquets** — Rejouer les paquets capturés
- **Extraction de poignées** — Capturer les poignées WPA

---

## Test avec aireplay-ng

Le test standard pour l'injection de paquets :

```bash
# Activer le mode moniteur
sudo airmon-ng start wlan0

# Démarrer le test d'injection
sudo aireplay-ng --test wlan0mon
```

**Taux de succès :**
- Plus de 80% pour les AP proches : Acceptable
- Plus de 95% pour les AP proches : Excellent
- Moins de 50% : Vérifier le pilote et la distance

---

## Support des puces

| Puce | Support d'injection | Fiabilité |
|---|---|---|
| RTL8812AU | ✓ | ★★★★★ |
| RTL8811AU | ✓ | ★★★★★ |
| MT7921AUN | ✓ | ★★★★☆ |
| MT7612U | ✓ | ★★★★☆ |
| RTL8832BU | ✓ | ★★★★☆ |

---

## Problèmes courants

**Problème :** Taux d'injection faible

**Solution :** Désactivez l'économie d'énergie :

```bash
sudo iwconfig wlan0mon power off
```

**Problème :** "Opération non autorisée"

**Solution :** Assurez-vous de travailler en tant que root ou avec sudo.

---

## Résumé

L'injection de paquets est un outil indispensable pour tout coffre de test de pénétration. Avec le bon adaptateur ALFA et une configuration correcte, vous pouvez injecter des paquets de manière fiable dans pratiquement n'importe quel environnement WiFi.
