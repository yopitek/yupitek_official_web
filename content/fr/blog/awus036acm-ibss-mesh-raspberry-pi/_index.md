---
title: "ALFA AWUS036ACM : Activation d'IBSS Ad Hoc et du Réseau Maillé 802.11s sur Raspberry Pi avec MT7612U"
description: "L'ALFA AWUS036ACM (MT7612U) est le seul adaptateur WiFi USB ALFA actuellement actif qui prend entièrement en charge IBSS Ad Hoc et le réseau maillé 802.11s sur Raspberry Pi — plug-and-play, aucune installation de pilote requise."
date: 2026-03-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA", "AWUS036ACM", "MT7612U", "Raspberry Pi", "IBSS", "Ad Hoc", "802.11s", "Réseau maillé", "Linux", "Sans fil"]
featureimage: "/images/blog/awus036acm-ibss-mesh-raspberry-pi.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Pourquoi l'AWUS036ACM est-il le seul choix ALFA supportant IBSS/Mesh ?"
    answer: "Son pilote mt76x2u est construit sur mac80211 de Linux, exposant pleinement les types d'interfaces IBSS et Mesh Point. Les autres modèles ALFA utilisent des pilotes hors-noyau qui n'incluent pas ces modes."
  - question: "Quelle est la différence entre IBSS Ad Hoc et 802.11s Mesh ?"
    answer: "IBSS est un réseau peer-to-peer sans AP central, tous les nœuds devant être à portée directe. 802.11s offre le routage multi-saut HWMP et l'auto-cicatrisation."
  - question: "L'AWUS036ACM nécessite-t-il un pilote sur Raspberry Pi ?"
    answer: "Non. Le pilote mt76x2u est intégré au noyau mainline depuis Linux 4.19. Raspberry Pi OS post-2020 est plug-and-play."
  - question: "Le mode IBSS supporte-t-il le chiffrement WPA2 ?"
    answer: "Le mode IBSS du noyau Linux ne supporte pas le WPA2-Personal standard. Utilisez un chiffrement applicatif comme WireGuard ou OpenVPN. Le mode 802.11s supporte SAE."
  - question: "Comment rendre le réseau Mesh persistant après redémarrage ?"
    answer: "Les interfaces créées via iw ne survivent pas au redémarrage. Créez un service systemd pour recréer l'interface et rejoindre le Mesh au démarrage."
---

{{< tldr >}}
L'AWUS036ACM utilise le chipset MT7612U, dont le pilote mt76x2u est construit sur mac80211 et supporte pleinement les modes IBSS Ad Hoc et 802.11s Mesh Point. Cet article détaille les principes, la configuration étape par étape et les cas d'usage.
{{< /tldr >}}

1. [Documentation officielle AWUS036ACM ALFA Network](https://docs.alfa.com.tw/Product/AWUS036ACM/)
2. [Wiki Linux Wireless — Types d'interfaces (VIF)](https://wireless.wiki.kernel.org/en/users/documentation/iw/vif)
3. [Pilote Linux MediaTek mt76](https://wireless.wiki.kernel.org/en/users/drivers/mediatek)
4. [Norme réseau Mesh IEEE 802.11s](https://standards.ieee.org/ieee/802.11s/4469/)
5. [Liste des pilotes intégrés au noyau morrownr USB-WiFi](https://github.com/morrownr/USB-WiFi)


# ALFA AWUS036ACM : Activation d'IBSS Ad Hoc et du Réseau Maillé 802.11s sur Raspberry Pi avec MT7612U

Si vous avez déjà essayé de construire un réseau WiFi entre des nœuds Raspberry Pi **sans routeur** — ou créer un maillage sans fil auto-cicatrisant qui achemine automatiquement le trafic à travers les sauts intermédiaires — vous découvrez rapidement que la plupart des adaptateurs WiFi USB ne peuvent pas le faire. Le pilote du noyau n'expose simplement pas les modes nécessaires.

L'**ALFA AWUS036ACM**, alimenté par la puce **MediaTek MT7612U**, est l'exception. Son pilote noyau `mt76` implémente l'interface mac80211 Linux complète, ce qui signifie qu'il prend nativement en charge à la fois le mode **IBSS (Ad Hoc)** et le mode **802.11s Mesh Point** sur Raspberry Pi — prêt à l'emploi, sans compilation de pilote requise.

Ce guide explique exactement comment fonctionnent les deux modes, fournit des instructions de configuration étape par étape, et vous montre quand choisir un mode plutôt que l'autre.

{{< faq >}}

---

## Références
1. [Documentation officielle AWUS036ACM ALFA Network](https://docs.alfa.com.tw/Product/AWUS036ACM/)
2. [Wiki Linux Wireless — Types d'interfaces (VIF)](https://wireless.wiki.kernel.org/en/users/documentation/iw/vif)
3. [Pilote Linux MediaTek mt76](https://wireless.wiki.kernel.org/en/users/drivers/mediatek)
4. [Norme réseau Mesh IEEE 802.11s](https://standards.ieee.org/ieee/802.11s/4469/)
5. [Liste des pilotes intégrés au noyau morrownr USB-WiFi](https://github.com/morrownr/USB-WiFi)
