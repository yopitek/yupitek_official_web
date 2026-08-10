---
title: "ALFA AWUS036ACM: IBSS Ad Hoc und 802.11s Mesh-Netzwerk auf Raspberry Pi mit MT7612U aktivieren"
description: "Der ALFA AWUS036ACM (MT7612U) ist der einzige aktuell aktive ALFA USB-WiFi-Adapter, der IBSS Ad Hoc und 802.11s Mesh-Netzwerk vollständig auf Raspberry Pi unterstützt — Plug-and-Play, keine Treiberinstallation erforderlich."
date: 2026-03-27
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA", "AWUS036ACM", "MT7612U", "Raspberry Pi", "IBSS", "Ad Hoc", "802.11s", "Mesh-Netzwerk", "Linux", "Drahtlos"]
featureimage: "/images/blog/awus036acm-ibss-mesh-raspberry-pi.webp"
faq:
  - question: "Warum ist der AWUS036ACM die einzige Wahl bei ALFA, die IBSS/Mesh unterstützt?"
    answer: "Sein mt76x2u-Treiber basiert auf Linux mac80211 und unterstützt vollständig die IBSS- und Mesh Point-Schnittstellentypen; andere ALFA-Modelle verwenden meist Out-of-Kernel-Treiber, die diese Modi nicht enthalten."
  - question: "Was ist der Unterschied zwischen IBSS Ad Hoc und 802.11s Mesh?"
    answer: "IBSS ist ein Peer-to-Peer-Netzwerk ohne zentralen AP, bei dem alle Knoten im direkten Kommunikationsbereich liegen müssen; 802.11s verfügt über HWMP-automatisches Multi-Hop-Routing und Selbstheilungsfähigkeiten, die über den Single-Hop-Bereich hinausgehen."
  - question: "Muss der AWUS036ACM auf einem Raspberry Pi getrieben werden?"
    answer: "Nein. Der mt76x2u-Treiber ist seit Linux Kernel 4.19 im Mainline enthalten, und Versionen von Raspberry Pi OS ab 2020 sind Plug-and-Play, ohne dass Installationsschritte erforderlich sind."
  - question: "Unterstützt der IBSS-Modus WPA2-Verschlüsselung?"
    answer: "Der IBSS-Modus im Linux-Kernel unterstützt kein Standard-WPA2-Personal. Für eine sichere Verbindung können Anwendungsschicht-Verschlüsselungen wie WireGuard oder OpenVPN verwendet werden, während 802.11s SAE unterstützt."
  - question: "Wie stellt man sicher, dass das Mesh-Netzwerk nach einem Neustart weiterhin funktioniert?"
    answer: "Über iw erstellte virtuelle Schnittstellen werden nach einem Neustart nicht beibehalten. Es muss ein systemd-Dienst (z. B. mesh-point.service) erstellt werden, der die Schnittstelle beim Systemstart automatisch neu erstellt und dem Mesh-Netzwerk hinzufügt."
---
1. [Alfa Network AWUS036ACM Offizielle Dokumentation](https://docs.alfa.com.tw/Product/AWUS036ACM/) 2. [Linux Wireless Wiki — Schnittstellentypen (VIF)](https://wireless.wiki.kernel.org/en/users/documentation/iw/vif) 3. [MediaTek mt76 Linux Treiber](https://wireless.wiki.kernel.org/en/users/drivers/mediatek) 4. [IEEE 802.11s Mesh NetzwerkStandard](https://standards.ieee.org/ieee/802.11s/4469/) 5. [morrownr USB-WiFi Liste der In-Kernel-Treiber](https://github.com/morrownr/USB-WiFi)

# ALFA AWUS036ACM: IBSS Ad Hoc und 802.11s Mesh-Netzwerk auf Raspberry Pi mit MT7612U aktivieren

{{< tldr >}}
Der AWUS036ACM verwendet den MT7612U-Chipsatz, dessen mt76x2u-Treiber auf Linux mac80211 aufbaut und den IBSS Ad Hoc- sowie den 802.11s Mesh Point-Modus vollständig unterstützt. Dieser Artikel erläutert detailliert die Funktionsweise beider Modi, die schrittweise Konfiguration und die praktischen Anwendungsszenarien.
{{< /tldr >}}

Der ALFA AWUS036ACM mit MediaTek MT7612U-Chipsatz ist der einzige USB-WiFi-Adapter im aktuellen ALFA-Sortiment, der auf dem Raspberry Pi vollständige IBSS-Ad-Hoc- und 802.11s-Mesh-Netzwerkunterstützung bietet, Plug-and-Play ohne Treiberinstallation.

Wenn Sie je versucht haben, ein WiFi-Netzwerk zwischen Raspberry-Pi-Knoten **ohne Router** aufzubauen — oder ein selbstheilendes drahtloses Mesh zu erstellen, das Traffic automatisch durch Zwischenknoten routet — entdecken Sie schnell, dass die meisten USB-WiFi-Adapter dies nicht können. Der Kernel-Treiber exponiert die notwendigen Modi einfach nicht.

Der **ALFA AWUS036ACM**, angetrieben vom **MediaTek MT7612U-Chipsatz**, ist die Ausnahme. Sein in-Kernel `mt76`-Treiber implementiert die vollständige Linux mac80211-Schnittstelle, was bedeutet, dass er sowohl **IBSS (Ad Hoc)**-Modus als auch **802.11s Mesh Point**-Modus auf Raspberry Pi nativ unterstützt — sofort einsatzbereit, ohne Treiberkompilierung.

Dieser Leitfaden erklärt genau, wie beide Modi funktionieren, bietet schrittweise Einrichtungsanleitungen und zeigt Ihnen, wann Sie den einen oder anderen Modus wählen sollen.

---

{{< faq >}}

## Referenzen
