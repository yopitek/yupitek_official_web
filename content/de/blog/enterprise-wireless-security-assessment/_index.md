---
title: "Enterprise-Wireless-Security-Assessment: Ein Komplettframework"
description: "Komplettes Enterprise-Wireless-Security-Assessment-Framework mit ALFA-Adapters. Deckt Scoping, Rogue-AP-Erkennung, WPA2/WPA3-Audit, PMF-Testing und Reporting für IT-Sicherheitsteams ab."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["enterprise", "wireless-security", "penetration-testing", "rogue-AP", "WPA2", "WPA3", "PMF", "ALFA-network"]
featureimage: "/images/blog/enterprise-wireless-security-assessment.webp"
faq:
  - question: "Welche Phasen umfasst die Bewertung der drahtlosen Unternehmenssicherheit?"
    answer: "Die vollständige Bewertung umfasst sechs aufeinanderfolgende Phasen: passive Erkundung, Erkennung bösartiger Access Points, WPA2/WPA3-Handshake-Analyse, PMF-Validierung, Client-Isolierungstests und EAP/RADIUS-Bewertung."
  - question: "Welche Genehmigungen sind vor der Durchführung einer drahtlosen Sicherheitsbewertung erforderlich?"
    answer: "Es muss eine schriftliche Genehmigung vorliegen, die vom CISO oder Asset-Besitzer unterzeichnet wurde und den Testzeitraum, die MAC-Adressen der Geräte sowie die spezifischen genehmigten technischen Methoden eindeutig abdeckt; eine mündliche Zustimmung reicht nicht aus."
  - question: "Wie können bösartige Access Points (Rogue APs) erkannt werden?"
    answer: "Die Liste der BSSIDs aus der passiven Erkundung wird mit der Liste der autorisierten Access Points abgeglichen; jede BSSID, die die Unternehmens-SSID sendet, aber nicht in der Liste enthalten ist, gilt als Kandidat für einen bösartigen Access Point."
  - question: "Warum sind Protected Management Frames (PMF) wichtig?"
    answer: "PMF verhindert Deauthentication- und Disassociation-Angriffe, indem es verhindert, dass Angreifer die Client-Verbindung zwangsweise unterbrechen, um Handshakes abzufangen oder Denial-of-Service-Angriffe durchzuführen; in WPA3 ist dies zwingend vorgeschrieben."
  - question: "Welche Risiken birgt der WPA3-Transition-Mode?"
    answer: "Der WPA3-Übergangsmodus akzeptiert sowohl SAE- als auch PSK-Authentifizierung, um die Kompatibilität aufrechtzuerhalten. Angreifer können Beacon-Frames senden, die nur WPA2 unterstützen, um Clients zu einem Downgrade zu zwingen, wodurch die Forward Secrecy unwirksam wird."
---
Beginnen Sie mit der Definition des Umfangs:

# Enterprise-Wireless-Security-Assessment: Ein Komplettframework

{{< tldr >}}
Diese Rahmenstruktur basiert auf dem ALFA Wireless-Adapter und beschreibt detailliert die sechsstufige Methodik für die Bewertung der drahtlosen Unternehmenssicherheit, einschließlich der Abgrenzung des Geltungsbereichs, der Erkennung bösartiger Access Points, der WPA2/WPA3-Audits, der PMF-Tests, der Client-Isolierung und der 802.1X-Bewertung, ergänzt durch Berichtsvorlagen und Definitionen der Schweregrade.
{{< /tldr >}}

Das Enterprise-Wireless-Security-Assessment umfasst sechs aufeinanderfolgende Phasen: passive Aufklärung, Rogue-AP-Erkennung, WPA2/WPA3-Handshake-Analyse, PMF-Verifizierung, Client-Isolationstest und EAP/RADIUS-Bewertung, ausschließlich nach schriftlicher Autorisierung durchzuführen.

Dieser Leitfaden bietet IT-Sicherheitsteams einen strukturierten Ansatz zur Bewertung der drahtlosen Netzwerksicherheit in Unternehmensumgebungen.

---

## Assessmentscoping

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

{{< faq >}}

## Reporting

Erstellen Sie einen Assessmentbericht mit folgenden Abschnitten:

1. **Executive Summary** — Schlüsselrisiken und Empfehlungen
2. **Methodik** — Verwendete Tools und Verfahren
3. **Ergebnisse** — Detaillierte findings
4. **Anhang** — Rohdaten und Scan-Ergebnisse

## Referenzen

1. [aircrack-ng Offizielle Dokumentation](https://www.aircrack-ng.org/)
2. [Wi-Fi Alliance WPA3 Spezifikation](https://www.wi-fi.org/discover-wi-fi/wpa3)
3. [IEEE 802.11w Standard fuer Protected Management Frames](https://standards.ieee.org/ieee/802.11w/4454/)
4. [NIST SP 800-153 WLAN-Sicherheitshinweise](https://csrc.nist.gov/publications/detail/sp/800-153/final)
5. [Kismet WLAN-Erkennungstool](https://www.kismetwireless.net/)
