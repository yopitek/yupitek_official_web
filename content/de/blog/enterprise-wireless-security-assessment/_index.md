---
title: "Enterprise-Wireless-Security-Assessment: Ein Komplettframework"
description: "Komplettes Enterprise-Wireless-Security-Assessment-Framework mit ALFA-Adapters. Deckt Scoping, Rogue-AP-Erkennung, WPA2/WPA3-Audit, PMF-Testing und Reporting für IT-Sicherheitsteams ab."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["enterprise", "wireless-security", "penetration-testing", "rogue-AP", "WPA2", "WPA3", "PMF", "ALFA-network"]
featureimage: "/images/blog/enterprise-wireless-security-assessment.webp"
---

# Enterprise-Wireless-Security-Assessment: Ein Komplettframework

Dieser Leitfaden bietet IT-Sicherheitsteams einen strukturierten Ansatz zur Bewertung der drahtlosen Netzwerksicherheit in Unternehmensumgebungen.

---

## Assessmentscoping

Beginnen Sie mit der Definition des Umfangs:

1. **Physische Abdeckung** — Welche Gebäude/Bereiche werden assessiert?
2. **Technologien** — Welche Standards sind im Einsatz (802.11n/ac/ax)?
3. **Authentifizierung** — WPA2-PSK, WPA2-Enterprise, WPA3?
4. **Clients** — Wie viele und welche Art von Geräten sind verbunden?

---

## Rogue-AP-Erkennung

```bash
# Alle APs in der Umgebung scannen
sudo airodump-ng wlan0mon -w rogue-scan

# Rogue-APs vom autorisierten Netzwerk identifizieren
sudo wash -i wlan0mon --dump=rogous-wps.txt
```

**Kriterien für Rogue-APs:**
- Nicht in der autorisierten AP-Liste
- Falsche Konfiguration (schwache Verschlüsselung)
- Unbefugter Zugangspunkt

---

## WPA2/WPA3-Audit

| Prüfpunkt | WPA2-Anforderung | WPA3-Anforderung |
|---|---|---|
| **Verschlüsselung** | AES-CCMP | AES-GCMP |
| **SAE** | N/A | Erforderlich |
| **PMF** | Optional | Empfohlen |
| **Transition Mode** | Akzeptabel | Bevorzugt |

---

## Reporting

Erstellen Sie einen Assessmentbericht mit folgenden Abschnitten:

1. **Executive Summary** — Schlüsselrisiken und Empfehlungen
2. **Methodik** — Verwendete Tools und Verfahren
3. **Ergebnisse** — Detaillierte findings
4. **Anhang** — Rohdaten und Scan-Ergebnisse
