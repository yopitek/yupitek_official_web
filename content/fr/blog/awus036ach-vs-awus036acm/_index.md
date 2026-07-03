---
title: "ALFA AWUS036ACH vs AWUS036ACM : Comparaison complète pour Kali Linux (2026)"
description: "Comparaison détaillée des ALFA AWUS036ACH et AWUS036ACM — puces, mode moniteur, injection de paquets, support des pilotes, et lequel est meilleur pour les tests de pénétration Kali Linux."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "AWUS036ACM", "comparison", "kali-linux", "RTL8812AU", "MT7612U"]
featureimage: "/images/blog/awus036ach-vs-awus036acm.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Quelle est la différence d'installation entre les pilotes AWUS036ACH et AWUS036ACM ?"
    answer: "L'AWUS036ACH (RTL8812AU) nécessite une compilation DKMS du pilote aircrack-ng, avec recompilation possible après mise à jour du noyau. L'AWUS036ACM (MT7612U) a son pilote intégré au noyau depuis 4.19, plug-and-play."
  - question: "Lequel est le mieux pour le mode moniteur ?"
    answer: "L'AWUS036ACH offre un mode moniteur plus stable avec ses doubles antennes et 30 dBm, réduisant les pertes de paquets en environnement dense. L'ACM supporte aussi le mode moniteur mais avec une puissance inférieure."
  - question: "Un débutant doit-il choisir ACH ou ACM ?"
    answer: "Un débutant doit choisir l'AWUS036ACM : pilote MT7612U natif au noyau, plug-and-play sans compilation. Pour le signal le plus puissant et les ressources pédagogiques, choisissez l'AWUS036ACH."
  - question: "Lequel recommander en environnement VM ?"
    answer: "En VM, l'AWUS036ACM est recommandé : après USB passthrough, le pilote natif est immédiatement reconnu sans compilation. L'ACH nécessite l'installation du pilote dans la VM."
---

{{< tldr >}}
L'AWUS036ACH convient aux missions professionnelles avec son pilote RTL8812AU, 30 dBm double antenne, mode moniteur et injection les plus puissants. L'AWUS036ACM privilégie la portabilité avec son pilote MT7612U natif, sans compilation, à environ 30-40 $.
{{< /tldr >}}

| Caractéristique | AWUS036ACH | AWUS036ACM |
|---|---|---|
| **Puce** | RTL8812AU | MT7612U |
| **Norme** | IEEE 802.11ac (Wi-Fi 5) | IEEE 802.11ac (Wi-Fi 5) |
| **Bandes** | 2,4 GHz + 5 GHz | 2,4 GHz + 5 GHz |
| **Débit max** | AC1200 | AC1200 |
| **Antennes** | 2× RP-SMA détachables | 2× RP-SMA détachables |
| **Mode IBSS** | Limité | Plein support |
| **Mode Mesh** | Limité | Plein support (802.11s) |


# ALFA AWUS036ACH vs AWUS036ACM : Comparaison complète pour Kali Linux (2026)

Lors du choix entre les deux appareils phares d'ALFA pour Kali Linux, il est important de comprendre leurs différences clés. Cet article compare l'AWUS036ACH et l'AWUS036ACM en détail.

---

## Aperçu des puces

| Caractéristique | AWUS036ACH | AWUS036ACM |
|---|---|---|
| **Puce** | RTL8812AU | MT7612U |
| **Norme** | IEEE 802.11ac (Wi-Fi 5) | IEEE 802.11ac (Wi-Fi 5) |
| **Bandes** | 2,4 GHz + 5 GHz | 2,4 GHz + 5 GHz |
| **Débit max** | AC1200 | AC1200 |
| **Antennes** | 2× RP-SMA détachables | 2× RP-SMA détachables |
| **Mode IBSS** | Limité | Plein support |
| **Mode Mesh** | Limité | Plein support (802.11s) |

---

## Quand choisir l'AWUS036ACH ?

- Tests de pénétration Wi-Fi quotidien
- Besoin d'un mode moniteur très stable
- Injection de paquets fiable
- Environnements virtuels (VirtualBox, VMware)
- Recherche de sécurité et tests WPA2/WPA3

---

## Quand choisir l'AWUS036ACM ?

- Réseaux maillés Raspberry Pi (802.11s)
- Topologies Ad Hoc
- Projets IoT et déploiements Raspberry Pi
- Pas besoin de compilation de pilote (mt76 intégré au noyau)
- Environnements nécessitant à la fois le mode moniteur et le maillage

---

{{< faq >}}

## Conclusion

Pour la plupart des tests de pénétration, l'AWUS036ACH reste le choix de référence. Pour les projets basés sur Raspberry Pi et les réseaux maillés, l'AWUS036ACM est un choix excellent et souvent supérieur.

---

## Références
1. [Dépôt GitHub aircrack-ng rtl8812au](https://github.com/aircrack-ng/rtl8812au)
2. [Pilote MT76 du noyau Linux](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76)
3. [Site officiel ALFA Network](https://www.alfa.com.tw)
4. [Yupitek — Distributeur agréé ALFA Network Taiwan](https://www.yupitek.com)
