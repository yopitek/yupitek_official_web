---
title: "Vollständiger Leitfaden zur Auswahl von Sierra Wireless Mobilfunkmodulen: Von LTE Cat 4 bis 5G mmWave"
date: 2026-07-30
slug: "sierra-wireless-selections"
tags:
  - sierra-wireless
  - mobilfunkmodul
  - 4g-lte
  - 5g-nr
  - auswahlleitfaden
  - em7455
  - em9190
  - m2-pcie
  - funkkommunikation
categories:
  - Produktauswahl-Leitfaden
series:
  - sierra-wireless-selection
series_order: 1
description: "Yupitek präsentiert einen umfassenden Vergleich von zehn Sierra Wireless (Semtech) Mobilfunkmodulen der EM/MC-Serie, von LTE Cat 4 bis 5G mmWave. EM7455, EM9190, MC7455 und mehr."
author: "yupitek"
draft: false
faq:
  - question: "Welche Sierra Wireless Modelle gibt es und worin unterscheiden sie sich?"
    answer: "Sierra Wireless hat zwei Serien (EM und MC) mit insgesamt zehn Modulen, die von LTE Cat 4 / Cat 6 / Cat 12 bis zu 5G Sub-6 und mmWave reichen. Der Hauptunterschied liegt im Formfaktor: EM kommt im M.2-Format, MC im mPCIe-Format. Bei gleichem Chipsatz (z. B. EM7455 und MC7455) sind die Leistungsdaten identisch – nur der Steckplatz ist anders."
  - question: "Sind das EM7455 und das MC7455 derselbe Chip?"
    answer: "Ja. Beide nutzen den Qualcomm MDM9230 Chipsatz, mit identischen Download-/Upload-Spitzenwerten von 300 / 50 Mbps und 2×CA Carrier Aggregation. Der einzige Unterschied: Das EM7455 kommt als M.2, das MC7455 als mPCIe."
  - question: "Muss ich bei 5G zwingend mmWave (EM9191) wählen? Funktioniert das in Deutschland?"
    answer: "Nicht unbedingt. Deutsche Mobilfunknetze setzen derzeit auf Sub-6. mmWave (n260/n261) wird primär in den USA eingesetzt. Für deutsche Anwendungen reicht das EM9190 (Sub-6 5G zum fairen Preis) völlig aus. Das EM9191 ist nur nötig, wenn du explizit mmWave-Unterstützung brauchst."
  - question: "Wie wähle ich zwischen M.2 und mPCIe Mobilfunkmodulen?"
    answer: "Das hängt vom Steckplatz deines Geräts ab. Laptops und moderne Embedded-Mainboards haben meist M.2 B-Key Steckplätze – dann nimm die EM-Serie. Ältere Industrierouter oder Industriesteuerungen mit mPCIe-Slot brauchen die MC-Serie. Wenn dein Board nur M.2 hat, du aber ein MC-Modul verwenden willst, brauchst du einen M.2-auf-mPCIe-Adapter."
  - question: "Wo kann ich Sierra Wireless in Deutschland kaufen?"
    answer: "In Deutschland und Europa kannst du alle Sierra Wireless Mobilfunkmodule über Yupitek beziehen. Besuche unsere Produktseiten für Modellinfos und Preise, oder schreib uns direkt an: sales@yupitek.com"
---

Die Auswahl des richtigen Mobilfunkmoduls kann überwältigend sein: Datenblätter mit unzähligen Nummern, ähnliche Modellbezeichnungen, und die große Frage, ob das Modul überhaupt in dein Gerät passt. In diesem Artikel erklären wir dir alle zehn aktuellen und langlebigen Sierra Wireless Module auf einen Blick – von LTE Cat 4 bis 5G mmWave.

Sierra Wireless gehört heute zu Semtech. Dieser Leitfaden wurde von Yupitek zusammengestellt und umfasst zehn Sierra Wireless Mobilfunkmodule: EM7430, EM7455, EM7511, EM7565, EM9190, EM9191, MC7304, MC7350, MC7354, MC7455. Die EM-Serie verwendet M.2, die MC-Serie mPCIe als Formfaktor.

Die technischen Daten basieren auf öffentlich zugänglichen Quellen und wurden von Yupitek für dich aufbereitet.

Die zehn Module decken LTE Cat 4 / 6 / 12 bis 5G Sub-6 und mmWave ab. EM und MC unterscheiden sich nur im Formfaktor: EM ist M.2, MC ist mPCIe.

## Zehn Modelle im Vergleich – Die Spezifikationstabelle

Hier findest du die Übersichtstabelle mit allen technischen Daten basierend auf den offiziellen Spec Sheets, damit du direkt vergleichen kannst. Bei EM9190/EM9191 weichen die Upload-Spitzenwerte je nach Quelle leicht ab – bitte prüf vor dem Kauf die aktuellsten offiziellen Spec Sheets oder frag bei uns nach (siehe Anhang).

| Modell | Mobilfunkstandard | Chip | Download / Upload Spitze | Carrier Aggregation | 5G | mmWave | Formfaktor | GNSS | Hinweise |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](https://yupitek.com/de/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | Einstiegs-Cat 6 (bitte Frequenzbänder vor Kauf mit uns abstimmen) |
| [EM7455](https://yupitek.com/de/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | Beliebtestes Modul in der Community, viele Tutorials |
| [EM7511](https://yupitek.com/de/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | Hoher Upload, Cat 12 |
| [EM7565](https://yupitek.com/de/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | CBRS/LAA-Bänder (Zertifizierungsumfang bitte erfragen), meiste Frequenzbänder, höchster Upload |
| [EM9190](https://yupitek.com/de/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | Download 2.5 Gbps (Upload auf Anfrage) | 8×CA | ✓ | — | M.2 | ✓ | Sub-6 5G Einstieg zum fairen Preis |
| [EM9191](https://yupitek.com/de/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | Download bis 4.5 Gbps (mit mmWave) / Sub-6 2.5 Gbps (Upload auf Anfrage) | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | High-End 5G inklusive mmWave |
| [MC7304](https://yupitek.com/de/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Einstiegs-Cat 4 (nahe EOL) |
| [MC7350](https://yupitek.com/de/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4, Nordamerika-Bänder |
| [MC7354](https://yupitek.com/de/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4, Weltweit-Bänder |
| [MC7455](https://yupitek.com/de/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | mPCIe-Version des EM7455 |

> Hinweis: EM9190 und EM9191 teilen sich dasselbe EM919x/EM7690 Spec Sheet. Das EM9190 ist der Sub-6-Einstieg, das EM9191 die mmWave-Flaggschiff-Variante. Das offizielle Spec Sheet ist hinter einem Login. Die hier zitierten Download-Spitzenwerte stammen aus öffentlichen Quellen. Detailwerte wie Upload-Peaks klären wir vor der Bestellung gerne mit der aktuellsten Version für dich.

## EM-Serie (M.2) vs MC-Serie (mPCIe) – Der Formfaktor-Unterschied

Das ist die erste Entscheidung bei der Auswahl – und auch die, bei der die meisten Fehler passieren.

**EM-Serie = M.2 B-Key Formfaktor**: Kompakt (ca. 30×42 mm), speziell für den WWAN-Slot von Laptops und Embedded-M.2-Steckplätze entwickelt. Moderne Industrie-Mainboards und Mini-PCs setzen fast alle auf M.2.

**MC-Serie = Mini PCIe (mPCIe) Formfaktor**: Sieht aus wie eine typische PC-Erweiterungskarte und passt in ältere Industrierouter und Steuerungen mit mPCIe-Slot. Wenn dein Board nur M.2 hat, brauchst du für ein MC-Modul einen M.2-auf-mPCIe-Adapter.

**Gemeinsame Hardware-Anforderungen**: Beide Formfaktoren benötigen einen externen SIM-Kartenhalter und Antennen. Die Antennenanschlüsse sind meist U.FL, typische Konfiguration ist 2×2 MIMO (Hauptantenne + Diversitätsantenne) plus eine GNSS-Positionsantenne.

**Eine häufig gestellte Frage**: EM7455 und MC7455 sind „derselbe Chip, nur anderer Formfaktor" – beide nutzen den Qualcomm MDM9230 mit identischen Spezifikationen. Der Unterschied liegt wirklich nur in M.2 vs. mPCIe. Welches du wählst, entscheidet allein der Steckplatz in deinem Gerät.

## Auswahl nach Anwendungsszenario

### Wireless-Router / CPE (OpenWrt / ROOter)

**Empfehlung**: [EM7455](https://yupitek.com/de/products/sierra/em7455/) / [MC7455](https://yupitek.com/de/products/sierra/mc7455/)
Begründung: Die größte Community-Unterstützung. ROOter (das auf OpenWrt basierende Cellular-Router-Firmware) bietet die umfangreichsten Tutorials und QMI/MBIM-Konfigurationsbeispiele. Wenn du ein Problem hast, findest du online garantiert eine Lösung.

### Laptop WWAN Upgrade

**Empfehlung**: [EM7430](https://yupitek.com/de/products/sierra/em7430/) / [EM7455](https://yupitek.com/de/products/sierra/em7455/)
Begründung: Beide im M.2-Format, passend für die WWAN-Steckplätze von Dell, Lenovo und anderen Business-Notebooks. Das EM7455 ist besonders bekannt, die Bandkonfiguration gut dokumentiert und gebraucht günstig zu haben – die ideale Wahl für ein Upgrade (Frequenzkompatibilität mit deinem Netzbetreiber klären wir vor der Bestellung gerne mit dir).

### Industrierouter / Gateways (Weitbereichstemperatur, Zertifizierungen, Langzeitverfügbarkeit)

**Empfehlung**: EM75-Serie ([EM7511](https://yupitek.com/de/products/sierra/em7511/), [EM7565](https://yupitek.com/de/products/sierra/em7565/)), [EM9190](https://yupitek.com/de/products/sierra/em9190/)/[EM9191](https://yupitek.com/de/products/sierra/em9191/), [MC7455](https://yupitek.com/de/products/sierra/mc7455/)
Begründung: Im industriellen Umfeld zählen Weitbereichstemperatur (−40°C Optionen), vollständige Zertifizierungen und garantierte Langzeitverfügbarkeit. Cat 12 und 5G-Module bieten höheren Upload und Zukunftssicherheit. Die genauen Temperaturspezifikationen und Zertifizierungslisten findest du im offiziellen Spec Sheet – wir schicken dir gerne die aktuelle Version für deine Auswahl.

### Connected Car / Flotten-Telematik (GNSS-Ortung)

**Empfehlung**: [EM7455](https://yupitek.com/de/products/sierra/em7455/) / [EM7565](https://yupitek.com/de/products/sierra/em7565/) / [EM9191](https://yupitek.com/de/products/sierra/em9191/)
Begründung: Alle drei haben integriertes GNSS und eignen sich perfekt für Fahrzeug-Tracking und Positionsrückmeldung. Für 5G-Anwendungen mit hoher Bandbreite im Fahrzeug nimm das EM9191.

### 5G Private Network / CBRS-Privatnetz

**Empfehlung**: [EM9191](https://yupitek.com/de/products/sierra/em9191/) (unterstützt CBRS-Bänder), [EM7565](https://yupitek.com/de/products/sierra/em7565/) (unterstützt CBRS/LAA-Bänder)
Begründung: CBRS (das US-3,5-GHz-Shared-Spektrum) und LAA sind typische Anforderungen für private Netzwerke. EM9191 und EM7565 unterstützen die entsprechenden Bänder hardwareseitig. Die konkrete Bandabstimmung und Zertifizierung hängt von den lokalen Vorschriften und der Netzumgebung ab – sprich uns bitte für eine vollständige technische Bewertung an.

### Videoüberwachung / Digital Signage mit hoher Bandbreite

**Empfehlung**: [EM9190](https://yupitek.com/de/products/sierra/em9190/) / [EM9191](https://yupitek.com/de/products/sierra/em9191/)
Begründung: 5G mit hoher Bandbreite (Download bis Sub-6 2.5 Gbps, mit mmWave bis 4.5 Gbps) ist ideal für die gleichzeitige Übertragung mehrerer Videostreams in Echtzeit und 4K-Digital-Signage-Inhalte.

### Ersatzteilbeschaffung / Langzeitbevorratung (Cat 4)

**Empfehlung**: [MC7304](https://yupitek.com/de/products/sierra/mc7304/) / [MC7350](https://yupitek.com/de/products/sierra/mc7350/) / [MC7354](https://yupitek.com/de/products/sierra/mc7354/)
Begründung: Die erste Wahl für die Reparatur älterer Geräte mit mPCIe-Cat-4-Modulen. Aber wir müssen dich ehrlich warnen: Die MC73xx-Serie nähert sich dem EOL (End of Life). Für die Langzeitbevorratung raten wir zu einer Migration auf [EM7455](https://yupitek.com/de/products/sierra/em7455/) oder [EM7565](https://yupitek.com/de/products/sierra/em7565/), um von einer längeren Verfügbarkeit zu profitieren.

## Kontakt & Kaufberatung

Du bist dir noch unsicher? Über Yupitek kannst du alle zehn EM/MC-Sierra-Mobilfunkmodule beziehen – inklusive passender Antennen, SIM-Adapter und Entwicklungsboards. Wir helfen dir bei der Spezifikationsprüfung, dem Frequenzbandvergleich, der Preisgestaltung und der technischen Integration.

## Häufig gestellte Fragen (FAQ)

**F1: Welche Sierra Wireless Modelle gibt es und worin unterscheiden sie sich?**
Sierra Wireless hat zwei Serien (EM und MC) mit insgesamt zehn Modulen, die von LTE Cat 4 / Cat 6 / Cat 12 bis zu 5G Sub-6 und mmWave reichen. Der Hauptunterschied liegt im Formfaktor: EM kommt im M.2-Format, MC im mPCIe-Format. Bei gleichem Chipsatz (z. B. EM7455 und MC7455) sind die Leistungsdaten identisch – nur der Steckplatz ist anders.

**F2: Sind das EM7455 und das MC7455 derselbe Chip?**
Ja. Beide nutzen den Qualcomm MDM9230 Chipsatz, mit identischen Download-/Upload-Spitzenwerten von 300 / 50 Mbps und 2×CA Carrier Aggregation. Der einzige Unterschied: Das EM7455 kommt als M.2, das MC7455 als mPCIe.

**F3: Muss ich bei 5G zwingend mmWave (EM9191) wählen? Funktioniert das in Deutschland?**
Nicht unbedingt. Deutsche Mobilfunknetze setzen derzeit auf Sub-6. mmWave (n260/n261) wird primär in den USA eingesetzt. Für deutsche Anwendungen reicht das EM9190 (Sub-6 5G zum fairen Preis) völlig aus. Das EM9191 ist nur nötig, wenn du explizit mmWave-Unterstützung brauchst.

**F4: Wie wähle ich zwischen M.2 und mPCIe Mobilfunkmodulen?**
Das hängt vom Steckplatz deines Geräts ab. Laptops und moderne Embedded-Mainboards haben meist M.2 B-Key Steckplätze – dann nimm die EM-Serie. Ältere Industrierouter oder Industriesteuerungen mit mPCIe-Slot brauchen die MC-Serie. Wenn dein Board nur M.2 hat, du aber ein MC-Modul verwenden willst, brauchst du einen M.2-auf-mPCIe-Adapter.

**F5: Wo kann ich Sierra Wireless in Deutschland kaufen?**
In Deutschland und Europa kannst du alle Sierra Wireless Mobilfunkmodule über Yupitek beziehen. Besuche unsere Produktseiten für Modellinfos und Preise, oder schreib uns direkt an: sales@yupitek.com

## Anhang: Offizielle Spec Sheet Links für alle zehn Modelle

Die folgenden Links führen zu Sierra Wireless offizieller technischer Dokumentation (source.sierrawireless.com). **Einige Dokumente sind nur nach Login als PDF herunterladbar.** Die hier zitierten technischen Daten stammen aus öffentlich zugänglichen Quellen. Wenn du die finalen Spezifikationen Punkt für Punkt prüfen musst (besonders die Upload-Peaks von EM9190/EM9191), frag uns bitte direkt nach den offiziellen Unterlagen:

- **EM7430**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7430_product_technical_specification/
- **EM7455**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7455_product_technical_specification/
- **EM7511**: https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7511_product_technical_specification/
- **EM7565**: https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7565_product_technical_specification/
- **EM9190 / EM9191**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_em919x-7690_product_technical_specification/
- **MC7304**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7304_product_technical_specification_and_customer_design_guidelines/
- **MC7350**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_mc7455_product_technical_specification/
