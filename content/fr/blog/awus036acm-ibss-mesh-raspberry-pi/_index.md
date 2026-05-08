---
title: "ALFA AWUS036ACM : Activation d'IBSS Ad Hoc et du Réseau Maillé 802.11s sur Raspberry Pi avec MT7612U"
description: "L'ALFA AWUS036ACM (MT7612U) est le seul adaptateur WiFi USB ALFA actuellement actif qui prend entièrement en charge IBSS Ad Hoc et le réseau maillé 802.11s sur Raspberry Pi — plug-and-play, aucune installation de pilote requise."
date: 2026-03-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA", "AWUS036ACM", "MT7612U", "Raspberry Pi", "IBSS", "Ad Hoc", "802.11s", "Réseau maillé", "Linux", "Sans fil"]
---

# ALFA AWUS036ACM : Activation d'IBSS Ad Hoc et du Réseau Maillé 802.11s sur Raspberry Pi avec MT7612U

Si vous avez déjà essayé de construire un réseau WiFi entre des nœuds Raspberry Pi **sans routeur** — ou créer un maillage sans fil auto-cicatrisant qui achemine automatiquement le trafic à travers les sauts intermédiaires — vous découvrez rapidement que la plupart des adaptateurs WiFi USB ne peuvent pas le faire. Le pilote du noyau n'expose simplement pas les modes nécessaires.

L'**ALFA AWUS036ACM**, alimenté par la puce **MediaTek MT7612U**, est l'exception. Son pilote noyau `mt76` implémente l'interface mac80211 Linux complète, ce qui signifie qu'il prend nativement en charge à la fois le mode **IBSS (Ad Hoc)** et le mode **802.11s Mesh Point** sur Raspberry Pi — prêt à l'emploi, sans compilation de pilote requise.

Ce guide explique exactement comment fonctionnent les deux modes, fournit des instructions de configuration étape par étape, et vous montre quand choisir un mode plutôt que l'autre.
