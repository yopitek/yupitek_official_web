---
title: "Sierra-Wireless-Kaufberatung für Mobilfunkmodule: Von LTE Cat 4 bis 5G mmWave"
description: "Der komplette Vergleich von zehn Sierra-Wireless-(Semtech-)Mobilfunkmodulen der Serien EM/MC: von LTE Cat 4 bis 5G mmWave mit Spezifikationen, Gehäusetypen und Auswahlhilfe. Technische Daten von Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "lte", "5g", "mmwave", "m2", "mpcie", "module-selection"]
featureimage: "/images/products/sierra/sierra_banner.png"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "Welche Sierra-Wireless-Module gibt es, und worin unterscheiden sie sich?"
    answer: "Sierra Wireless bietet aktuell zehn Module in zwei Serien, EM und MC, über LTE Cat 4, Cat 6, Cat 12 bis 5G Sub-6 und mmWave. Der größte Unterschied ist das Gehäuse: EM-Module verwenden M.2, MC-Module mPCIe. Modelle mit demselben Chipsatz, etwa EM7455 und MC7455, leisten identisch und unterscheiden sich nur in der Steckplatzform."
  - question: "Sind EM7455 und MC7455 derselbe Chip?"
    answer: "Ja. Beide nutzen den Qualcomm-MDM9230-Chipsatz mit identischen 300/50 Mbit/s Spitzenwerten und 2×CA Carrier Aggregation. Der einzige Unterschied ist das Gehäuse: EM7455 ist M.2, MC7455 ist mPCIe."
  - question: "Muss ich für 5G unbedingt mmWave (EM9191) nehmen? Funktioniert es in Taiwan?"
    answer: "Nicht unbedingt. Taiwans 5G-Netze setzen aktuell vor allem auf Sub-6, während mmWave hauptsächlich in US-typischen Umgebungen (Bänder n260/n261) ausgebaut ist. Für die meisten Projekte in Taiwan reicht der EM9190 (preisgünstiges 5G Sub-6); den EM9191 braucht man nur bei echten US-mmWave-Testanforderungen."
  - question: "Wie wähle ich zwischen M.2- und mPCIe-Mobilfunkmodulen?"
    answer: "Das hängt vom Steckplatz deines Geräts ab. Laptops und moderne Embedded-Boards nutzen meist M.2 B-Key, also nimm die EM-Serie. Ältere Industrierouter und Panel-PCs mit mPCIe-Steckplatz nehmen die MC-Serie. Wenn dein Board nur M.2 hat, du aber ein MC-Modul willst, brauchst du einen M.2-auf-mPCIe-Adapter."
  - question: "Wo kann ich Sierra-Wireless-Module kaufen?"
    answer: "Du kannst die komplette Sierra-Wireless-Mobilfunkmodul-Reihe über Yupitek beziehen. Schau auf den Yupitek-Produktseiten nach Modellen und Preisen oder schreib direkt an sales@yupitek.com."
---

# Sierra-Wireless-Kaufberatung für Mobilfunkmodule: Von LTE Cat 4 bis 5G mmWave

Ob du als Student an einem IoT-Projekt arbeitest oder in der Laborentwicklung Netzwerkhardware baust, das Schlimmste beim Kauf eines Mobilfunkmoduls ist immer dasselbe: Man starrt eine Stunde auf Spezifikationstabellen, die Modellnummern verschwimmen, und am Ende kauft man das falsche Gehäuse, das gar nicht ins Gerät passt.

Dieser Leitfaden stellt alle zehn aktuellen und langlebigen Sierra-Wireless-Module (heute Teil von Semtech) vor, vom Einstiegsmodell LTE Cat 4 bis hin zu 5G mmWave. Alle hier behandelten EM-Module verwenden das M.2-Gehäuse, die MC-Serie kommt im mPCIe-Format.

Die technischen Daten dieses Artikels wurden von Yupitek zusammengestellt.

## Die Zehn-Module-Übersicht: Schau direkt auf die Zahlen

Zuerst die wichtigste Tabelle! Alle Werte stammen aus den offiziellen Spec-Sheets, damit du direkt vergleichen kannst. Ein Hinweis: Die Spitzenwerte für den Uplink (Upload) von EM9190/EM9191 können je nach Quelle leicht abweichen. Wenn du wirklich für ein Projekt einkaufst, schau lieber ins aktuelle offizielle Spec-Sheet oder frag direkt bei uns nach (Links im Anhang).

| Modell | Mobilfunkstandard | Chipsatz | Spitzenwerte Download / Upload | Carrier Aggregation | 5G | mmWave | Gehäuse | GNSS | Hinweis |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](/de/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbit/s | 2×CA | — | — | M.2 | ✓ | Einstiegs-Cat-6 (tatsächliche Bandkonfiguration bitte anfragen) |
| [EM7455](/de/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbit/s | 2×CA | — | — | M.2 | ✓ | Der Beliebteste in der Open-Source-Community, die meisten Tutorials |
| [EM7511](/de/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbit/s | 3×CA | — | — | M.2 | ✓ | Cat 12 mit hohem Uplink |
| [EM7565](/de/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbit/s | 3×CA | — | — | M.2 | ✓ | Unterstützt CBRS/LAA-Bänder, die meisten Bänder und höchster Uplink |
| [EM9190](/de/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | 2.5 Gbit/s Download (Upload-Spitzenwert auf Anfrage) | 8×CA | ✓ | — | M.2 | ✓ | Preisgünstiger Einstieg in 5G Sub-6 |
| [EM9191](/de/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | bis 4.5 Gbit/s Download inkl. mmWave / 2.5 Gbit/s Sub-6 (Upload-Spitzenwert auf Anfrage) | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | Flaggschiff-5G mit Millimeterwellen |
| [MC7304](/de/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbit/s | — | — | — | mPCIe | ✓ | Einstiegs-Cat-4 (kurz vor EOL, Produktionsende) |
| [MC7350](/de/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbit/s | — | — | — | mPCIe | ✓ | Cat 4, für Nordamerika-Bänder |
| [MC7354](/de/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbit/s | — | — | — | mPCIe | ✓ | Cat 4, globale Bänder |
| [MC7455](/de/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbit/s | 2×CA | — | — | mPCIe | ✓ | Praktisch die mPCIe-Version des EM7455 |

> Hinweis: EM9190 und EM9191 teilen sich dasselbe Spezifikationsdokument (EM919x/EM7690). EM9190 ist das preisgünstige 5G Sub-6, EM9191 kommt mit mmWave als Flaggschiff. Das offizielle Spec-Sheet kann nur nach Login heruntergeladen werden; die Download-Spitzenwerte oben stammen aus öffentlichen Quellen. Für Upload-Spitzenwerte und andere Details bestätige vor der Bestellung besser die aktuelle Version bei uns.

## Erste Hürde: Was unterscheidet die EM-Serie (M.2) von der MC-Serie (mPCIe)?

Genau hier stolpert fast jeder Anfänger! Falsch gekauft, nicht eingesteckt bekommen, sehr peinlich.

**EM-Serie = M.2-B-Key-Gehäuse.** Stell dir die Schnittstelle vor, in die in einem Laptop die SSD gesteckt wird: sehr kompakt (etwa 30×42 mm). Diese Module sind für WWAN-Steckplätze in Laptops und Embedded-M.2-Anschlüsse gedacht; genau die verbauen die meisten neueren Industrie-Mainboards und Mini-PCs.

**MC-Serie = Mini-PCIe-Gehäuse (mPCIe).** Sieht aus wie die Erweiterungskarten älterer Computer und passt in die mPCIe-Steckplätze älterer Industrierouter und Panel-PCs. Hat dein Board nur einen M.2-Steckplatz, brauchst du für ein MC-Modul eine separate Adapterplatine (M.2-auf-mPCIe).

**Das haben sie gemeinsam:** Beide brauchen eine externe SIM-Kartenhalterung und Antennen. Die Antennenanschlüsse sind üblicherweise U.FL, Standardkonfiguration ist 2×2 MIMO (eine Hauptantenne plus eine Diversity-Antenne) plus eine zusätzliche GNSS-Antenne für die Positionsbestimmung.

**Die häufigste Frage:** Worin unterscheiden sich EM7455 und MC7455 wirklich? Antwort: „Derselbe Chip, nur das Gehäuse." Beide Karten verwenden den Qualcomm MDM9230 mit identischen Spezifikationen. Die Wahl hängt also wirklich nur davon ab, wie dein Board aussieht.

## Unsere Empfehlung nach Projekt oder Anwendungsszenario

### 1. Eigenen Router / CPE bauen (mit OpenWrt oder ROOter)

**Empfehlung: [EM7455](/de/products/sierra/em7455/) / [MC7455](/de/products/sierra/mc7455/)**
Ganz einfach: Im Open-Source-Umfeld gibt es für diese Module die meisten Ressourcen. Wenn du ROOter nutzt (eine Firmware auf OpenWrt-Basis), sind Tutorials und QMI/MBIM-Konfigurationsbeispiele sehr vollständig, und bei Problemen rettet dich eine schnelle Internetsuche.

### 2. WWAN-Karte in einem älteren Laptop upgraden

**Empfehlung: [EM7430](/de/products/sierra/em7430/) / [EM7455](/de/products/sierra/em7455/)**
Beide kommen im M.2-Format und passen in die WWAN-Steckplätze von Business-Laptops wie Dell, Lenovo und anderen. Der EM7455 ist auf dem Gebrauchtmarkt oft besonders günstig und der Favorit beim Upgrade (aber frag vor der Bestellung nach, ob die Bänder zu deinem Provider passen).

### 3. Industrierouter / IoT-Gateways (brauchen Robustheit und weiten Temperaturbereich)

**Empfehlung: EM75-Serie ([EM7511](/de/products/sierra/em7511/), [EM7565](/de/products/sierra/em7565/)), [EM9190](/de/products/sierra/em9190/)/[EM9191](/de/products/sierra/em9191/), [MC7455](/de/products/sierra/mc7455/)**
Bei Industrieprojekten zählen vor allem der weite Temperaturbereich (denk an raue Umgebungen von -40°C bis +85°C), vollständige Zertifizierungen und langfristige Verfügbarkeit. Cat-12- und 5G-Module bieten mehr Uplink-Bandbreite und bessere Zukunftsperspektiven. Die aktuellen Temperaturspezifikationen bitte immer gegen die neuesten offiziellen Dokumente prüfen.

### 4. Vernetzte Fahrzeuge / Flotten-Tracking (braucht GNSS)

**Empfehlung: [EM7455](/de/products/sierra/em7455/) / [EM7565](/de/products/sierra/em7565/) / [EM9191](/de/products/sierra/em9191/)**
Telematik-Projekte brauchen meist präzise Positionsbestimmung. Alle drei haben eingebautes GNSS und lösen Konnektivität und Ortung mit einer Karte. Brauchst du 5G-Bandbreite, nimm direkt den EM9191.

### 5. Private 5G-Netze / CBRS-Experimente

**Empfehlung: [EM9191](/de/products/sierra/em9191/) (CBRS-Bänder), [EM7565](/de/products/sierra/em7565/) (CBRS/LAA-Bänder)**
Wenn du im Labor CBRS (das gemeinsam genutzte US-Band bei 3.5 GHz) oder LAA erforschst, unterstützen beide Module das auf Hardwareebene. Aber ein echtes Privatnetz vor Ort zu testen hängt von lokalen Vorschriften und der Provider-Umgebung ab, also sprich die technischen Details vor der Einführung besser mit uns durch.

### 6. Videoüberwachung / HD-Video-Backhaul

**Empfehlung: [EM9190](/de/products/sierra/em9190/) / [EM9191](/de/products/sierra/em9191/)**
Weil 5G so viel Bandbreite bietet (bis 2.5 Gbit/s Download in Sub-6, mit mmWave bis 4.5 Gbit/s), sind diese Module ideal für Echtzeit-Backhaul mehrerer Videostreams oder 4K-Streaming.

### 7. Reparatur alter Geräte / Ersatzteile für alte Labormaschinen (Cat 4)

**Empfehlung: [MC7304](/de/products/sierra/mc7304/) / [MC7350](/de/products/sierra/mc7350/) / [MC7354](/de/products/sierra/mc7354/)**
Das ist die erste Wahl für die Wartung alter Geräte mit mPCIe-Steckplatz. Aber um ehrlich zu sein: Die MC73xx-Serie steht kurz vor dem EOL (Produktionsende). Für langfristige Projekte ist der Umstieg auf [EM7455](/de/products/sierra/em7455/) oder [EM7565](/de/products/sierra/em7565/) die sicherere Wahl.

## Immer noch unsicher? Sprich uns an

Wenn du nach dem Lesen immer noch nicht weißt, was du nehmen sollst: In Taiwan kannst du alle zehn Mobilfunkmodule der Serien EM/MC über Yupitek beziehen, inklusive Antennen, SIM-Adapter oder Evaluierungsboards. Ob Spezifikationen prüfen, Bänder vergleichen oder Angebot und technischen Support für dein Projekt einholen, wir helfen dir.

## Häufig gestellte Fragen

{{< faq >}}

## Anhang: Offizielle Spec-Sheets aller zehn Modelle

Die Links unten führen in die offizielle technische Bibliothek von Sierra Wireless (source.sierrawireless.com). **Für den Download einiger PDFs ist eine Registrierung nötig.** Die Zahlen im Artikel stammen aus öffentlichen Quellen; wenn du besonders feine Details Punkt für Punkt bestätigen willst (z. B. die Upload-Spitzenwerte von EM9190/EM9191), kontaktiere uns und wir teilen die aktuellen offiziellen Dokumente.

- **EM7430**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7430_product_technical_specification/
- **EM7455**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7455_product_technical_specification/
- **EM7511**: https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7511_product_technical_specification/
- **EM7565**: https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7565_product_technical_specification/
- **EM9190 / EM9191**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_em919x-7690_product_technical_specification/
- **MC7304**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7304_product_technical_specification_and_customer_design_guidelines/
- **MC7350**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_mc7455_product_technical_specification/
