---
title: "Qu'est-ce que l'injection de paquets ? Tester la compatibilité de votre adaptateur WiFi avec Kali Linux"
description: "Comprenez l'injection de paquets WiFi, pourquoi elle nécessite des adaptateurs spécifiques, comment tester votre adaptateur ALFA Network avec aireplay-ng et quelles puces supportent l'injection sur Kali Linux."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["packet-injection", "aireplay-ng", "kali-linux", "wifi-adapter", "RTL8812AU", "ALFA-Network"]
featureimage: "/images/blog/packet-injection-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Qu'est-ce que l'injection de paquets ?"
    answer: "L'injection de paquets est la capacité d'une carte réseau à transmettre des trames 802.11 arbitraires. Limitée par le pilote, pas par le matériel. Les cartes ALFA avec chipsets RTL8812AU, MT7612U et MT7921AUN supportent l'injection via les pilotes aircrack-ng."
  - question: "Comment tester si l'injection de paquets fonctionne ?"
    answer: "Exécutez sudo aireplay-ng --test wlan0mon. Une sortie 'Injection is working!' confirme le fonctionnement. Un taux de réussite supérieur à 80% indique une fiabilité correcte."
  - question: "Quelle carte ALFA est la meilleure pour l'injection de paquets ?"
    answer: "L'AWUS036ACH (RTL8812AU) avec 30 dBm et double antenne offre l'injection la plus puissante. L'AWUS036ACM (MT7612U) est plus simple avec son pilote intégré au noyau."
  - question: "Pourquoi l'injection de paquets échoue-t-elle parfois ?"
    answer: "Causes possibles : pilote non chargé ou inadéquat, interface en mode managed au lieu de monitor, alimentation USB insuffisante, ou distance trop importante de l'AP cible."
  - question: "L'injection de paquets est-elle légale ?"
    answer: "L'injection de paquets sur des réseaux que vous ne possédez pas ou sans autorisation écrite est illégale dans la plupart des pays. N'utilisez ces techniques que sur vos propres réseaux ou avec autorisation explicite."
---

{{< tldr >}}
L'injection de paquets est la capacité d'une carte à transmettre des trames 802.11 arbitraires, limitée par le pilote. Les cartes ALFA avec chipsets RTL8812AU, MT7612U et MT7921AUN supportent l'injection via les pilotes aircrack-ng.
{{< /tldr >}}

L'injection de paquets est la capacité d'un adaptateur WiFi à **envoyer n'importe quelles trames** — pas seulement celles qui lui sont destinées. Cela permet des attaques telles que :


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

{{< faq >}}

## Résumé

L'injection de paquets est un outil indispensable pour tout coffre de test de pénétration. Avec le bon adaptateur ALFA et une configuration correcte, vous pouvez injecter des paquets de manière fiable dans pratiquement n'importe quel environnement WiFi.

---

## Références
1. [Site et documentation officielle aircrack-ng](https://www.aircrack-ng.org/)
2. [Guide d'utilisation aireplay-ng](https://www.aircrack-ng.org/doku.php?id=aireplay-ng)
3. [Documentation officielle Kali Linux](https://www.kali.org/docs/)
4. [Documentation sous-système mac80211 Linux](https://wireless.wiki.kernel.org/en/developers/Documentation/mac80211)
5. [Ressources norme IEEE 802.11](https://standards.ieee.org/ieee/802.11/)
