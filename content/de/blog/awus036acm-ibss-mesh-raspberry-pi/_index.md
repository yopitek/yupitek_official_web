---
title: "ALFA AWUS036ACM: IBSS Ad Hoc und 802.11s Mesh-Netzwerk auf Raspberry Pi mit MT7612U aktivieren"
description: "Der ALFA AWUS036ACM (MT7612U) ist der einzige aktuell aktive ALFA USB-WiFi-Adapter, der IBSS Ad Hoc und 802.11s Mesh-Netzwerk vollständig auf Raspberry Pi unterstützt — Plug-and-Play, keine Treiberinstallation erforderlich."
date: 2026-03-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA", "AWUS036ACM", "MT7612U", "Raspberry Pi", "IBSS", "Ad Hoc", "802.11s", "Mesh-Netzwerk", "Linux", "Drahtlos"]
---

# ALFA AWUS036ACM: IBSS Ad Hoc und 802.11s Mesh-Netzwerk auf Raspberry Pi mit MT7612U aktivieren

Wenn Sie je versucht haben, ein WiFi-Netzwerk zwischen Raspberry-Pi-Knoten **ohne Router** aufzubauen — oder ein selbstheilendes drahtloses Mesh zu erstellen, das Traffic automatisch durch Zwischenknoten routet — entdecken Sie schnell, dass die meisten USB-WiFi-Adapter dies nicht können. Der Kernel-Treiber exponiert die notwendigen Modi einfach nicht.

Der **ALFA AWUS036ACM**, angetrieben vom **MediaTek MT7612U-Chipsatz**, ist die Ausnahme. Sein in-Kernel `mt76`-Treiber implementiert die vollständige Linux mac80211-Schnittstelle, was bedeutet, dass er sowohl **IBSS (Ad Hoc)**-Modus als auch **802.11s Mesh Point**-Modus auf Raspberry Pi nativ unterstützt — sofort einsatzbereit, ohne Treiberkompilierung.

Dieser Leitfaden erklärt genau, wie beide Modi funktionieren, bietet schrittweise Einrichtungsanleitungen und zeigt Ihnen, wann Sie den einen oder anderen Modus wählen sollen.
