---
title: "ACS ACR122U — USB NFC Reader"
description: "ACS ACR122U, USB NFC-Lesegerät mit Unterstützung von ISO 14443 A/B, MIFARE und FeliCa bei 13,56 MHz. Ideal für NFC-Forschung und Anwendungsentwicklung."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["acr"]
tags: ["NFC", "RFID", "ISO 14443", "MIFARE", "USB", "Card Reader"]
faq:
  - question: "Muss ich einen ACS-Treiber für den ACR122U unter Windows installieren?"
    answer: "Nein. ACS gibt an, dass der ACR122U PC/SC-kompatibel ist und den standardmäßigen Microsoft CCID-Treiber verwendet, daher ist unter Windows kein ACS-Treiber erforderlich, da der Treiber bereits in das Betriebssystem integriert ist."
  - question: "Welche Karten und Tags kann der ACR122U lesen und schreiben?"
    answer: "Laut ACS greift er auf Karten des Typs ISO 14443-4 Type A und Type B, MIFARE, FeliCa und alle vier Arten von NFC-Tags (ISO/IEC 18092) zu, mit einer Kartenleseentfernung von bis zu 50 mm, abhängig vom Tag-Typ. Die integrierte Kollisionsvermeidung stellt sicher, dass nur ein Tag gleichzeitig angesprochen wird."
  - question: "Wie programmiere ich den ACR122U in meiner eigenen Anwendung?"
    answer: "Der ACR122U unterstützt PC/SC und CT-API über einen Wrapper auf PC/SC-Basis. Befehle für ISO 18092-Tags sowie für die LED und den Summer werden als Pseudo-APDUs gesendet. ACS listet außerdem Unterstützung für Android 3.1 und höher auf."
---

ACR122U

## Produktübersicht

Der ACR122U ist ein PC-gebundener kontaktloser Smartcard-Leser/Schreiber basierend auf der 13,56 MHz RFID-Technologie. Er entspricht dem ISO/IEC 18092 NFC-Standard und unterstützt MIFARE®, ISO 14443 Typ A/B sowie alle vier NFC-Tag-Typen. Es handelt sich um ein PC/SC- und CCID-konformes Plug-and-Play-USB-Gerät mit einer Zugriffsgeschwindigkeit bis zu 424 Kbps und USB Full Speed (12 Mbps) Schnittstelle. Die Betriebsreichweite beträgt bis zu 50 mm.

## Technische Spezifikationen

| Spezifikation | Details |
|---------------|---------|
| Betriebsfrequenz | 13,56 MHz |
| Betriebsreichweite | Bis zu 50 mm (je nach Tag-Typ) |
| Lese-/Schreibgeschwindigkeit | 106 Kbps / 212 Kbps / 424 Kbps |
| USB-Schnittstelle | USB Full Speed (12 Mbps) |
| Versorgungsspannung | 5V DC geregelt |
| Versorgungsstrom | max. 200 mA / 100 mA normal / 50 mA Standby |
| Antennengröße | 50 mm × 40 mm |
| Abmessungen | 98 × 65 × 12,8 mm |
| Gewicht | 70 g |
| Betriebstemperatur | 0°C – 60°C |
| Luftfeuchtigkeit | max. 90 % (nicht kondensierend) |
| MTBF | 408.500 Std. |
| LED | 1 zweifarbig Rot/Grün (benutzersteuerbar) |
| Summer | Monoton (benutzersteuerbar) |
| SAM-Slot | 1 × ISO 7816-3 (optional) |
| Konformität | PC/SC, CCID, CE, FCC, RoHS |

## Hauptmerkmale

- USB Full Speed-Schnittstelle
- CCID- und PC/SC-konform, Plug-and-Play
- Lese-/Schreibgeschwindigkeit bis zu 424 Kbps
- Eingebaute Antenne, Kartenlesedistanz bis zu 50 mm
- Unterstützt alle 4 NFC-Tag-Typen (ISO/IEC 18092)
- Unterstützt MIFARE Ultralight C, MIFARE Plus, DESFire EV1
- Unterstützt 3 NFC-Modi: Reader/Writer, Card Emulation, Peer-to-Peer
- Integrierte Anti-Kollision (1 Tag gleichzeitig)
- Benutzersteuerbare zweifarbige LED und Summer
- Optionaler ISO 7816-3 SAM-Slot für erhöhte Sicherheit
- Als Modulform für POS/Zugangssteuerung erhältlich
- Unterstützt PC/SC und CT-API

## Unterstützte Tag-Typen

| Tag / Kartentyp | Standard |
|-----------------|----------|
| NFC Tag Typ 1 | ISO 14443 Typ A |
| NFC Tag Typ 2 | ISO 14443 Typ A |
| NFC Tag Typ 3 | FeliCa |
| NFC Tag Typ 4 | ISO 14443 Typ A und B |
| MIFARE Classic (1K, 4K, MINI) | ISO 14443 Typ A |
| MIFARE Ultralight / Ultralight C | ISO 14443 Typ A |
| MIFARE Plus | ISO 14443 Typ A |
| MIFARE DESFire / DESFire EV1 | ISO 14443 Typ A |
| FeliCa | ISO 18092 |
| ISO 14443 Typ A Karten | ISO 14443 |
| ISO 14443 Typ B Karten | ISO 14443 |

## Unterstützte Betriebssysteme

- Windows CE 5.0, Windows Embedded Compact 6.0 / 7
- Windows XP, Vista, 7, 8, 8.1, 10
- Windows Server 2003 / 2008 / 2012 / 2016
- Linux®
- macOS®
- Solaris
- Android™ 3.1 und höher


## 📄 Produktdatenblatt

| Ressource | Link |
|----------|------|
| 📄 ACR122U Datenblatt (PDF) | [PDF herunterladen](/docs/acr/ACR122U_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/acr/acr122u.webp" alt="ACS ACR122U NFC Reader" />
{{< /gallery >}}

---

{{< alert >}}
Benötigen Sie ein Produktangebot? Bitte [kontaktieren Sie uns](/de/contact/).
{{< /alert >}}

{{< faq >}}

[Einrichtungsanleitungen und technische Details — doc.yupitek.com](https://doc.yupitek.com/acs/products/acr122u/)
