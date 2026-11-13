---
title: "LAN Turtle Hub"
date: 2026-11-12
draft: false
featureimage: "/images/products/hak5/lan-turtle-hub.jpg"
showBreadcrumbs: true
brands: ["hak5"]
tags: ["Network Audit", "USB-C Ethernet", "Penetration Testing", "WiFi"]
description: "USB-C-Ethernet-Adapter mit integriertem 3-Port-USB-3-Hub, Out-of-Band-WiFi, USB-Abfangen und DuckyScript-Payloads."
---

{{< alert "warning" >}}
**Rechtlicher Hinweis**: LAN Turtle Hub ist ein professionelles Sicherheitsforschungswerkzeug. Ausschließlich für autorisierte Sicherheitstests und Forschungszwecke. Nur für Sicherheitsfachleute mit gültiger schriftlicher Genehmigung bestimmt.
{{< /alert >}}

Der Hak5 LAN Turtle Hub ist ein USB-C-Ethernet-Adapter mit integriertem 3-Port-USB-3-Hub. Er ergänzt Out-of-Band-WiFi, einen umschaltbaren USB-Port zum Abfangen von USB, DuckyScript-Payloads und eine browserbasierte Weboberfläche für autorisierte Netzwerkbewertungen.

## Produktmerkmale

![LAN Turtle Hub](/images/products/hak5/lan-turtle-hub.jpg)

- **Alltägliche Bauform**: Funktioniert als USB-C-Ethernet-Adapter mit 3-Port-USB-3-Hub
- **Fernzugriff**: über WireGuard, OpenVPN, SSH-Tunnel oder Cloud C²
- **Out-of-Band-WiFi**: Eigener Verwaltungskanal als WPA-gesicherter Access Point oder als Client nahegelegener Netzwerke
- **USB-Abfangen**: Ein umschaltbarer USB-A-Port wechselt zwischen Durchleitung zum Ziel und dem internen Linux-System
- **DuckyScript-Payloads**: Bash und DuckyScript mit Root-Zugriff, entwickelt und getestet in der Weboberfläche oder in Payload Studio
- **Weboberfläche**: Payloads ausrollen, VPNs konfigurieren, SSH-Tunnel verwalten und Loot im Browser ansehen

## Technische Daten

| Merkmal | Details |
|---|---|
| USB-C-Ethernet | USB-Ethernet-Adapter mit überbrückter Verbindung zum Zielnetzwerk |
| Ethernet-Port | RJ45, Standard-Kabel Cat5e/6 |
| USB-Hub | 3 × USB-A-3.1-Ports, bis 5 Gbit/s; zwei Hub-Ports, ein umschaltbarer Port |
| Drahtlos | Out-of-Band-WiFi: WPA-gesicherter Verwaltungs-AP oder Client-Modus |
| Stromversorgung | Über das USB-C-Kabel |
| Status-LED | RGB, per Skript steuerbar oder deaktivierbar |
| Standardverwaltung | Weboberfläche http://172.16.84.1:1471, SSH auf 172.16.84.1 |
| Fernzugriff | WireGuard, OpenVPN, SSH-Tunnel, Cloud C² |
| Zielanschluss | USB-C (USB-C-auf-USB-A-Adapter für ältere Hosts) |

## Einsatzszenarien

- Autorisierter Fernzugriff und Persistenztests, von IT-Netzwerken bis zu Heimlaboren
- Bewertung von Man-in-the-Middle-Szenarien und Netzwerkverkehr zwischen Host und Netzwerk
- Tests zum Abfangen von USB-Sticks und zur Dateiverarbeitung mit dem umschaltbaren USB-Port
- Hardware-VPN, das den Verkehr eines Laptops in nicht vertrauenswürdigen Netzwerken durch einen verschlüsselten Tunnel leitet

## Offizielle Dokumentation

| Ressource | Link |
|---|---|
| 📖 Offizielle Dokumentation | [Online ansehen](https://documentation.hak5.org/lan-turtle-hub/getting-started/lan-turtle-hub-basics) |
| 🛒 Produktseite im Hak5-Shop | [Produkt ansehen](https://shop.hak5.org/products/lan-turtle-hub) |

{{< alert >}}
Benötigen Sie ein Produktangebot? Bitte [kontaktieren Sie uns](/de/contact/).
{{< /alert >}}
