---
title: "EM7565 im Detail: CBRS-Privatnetz und hohe Upload-Geschwindigkeit, wie wählst du das richtige Firmennetz?"
description: "EM7565 im Detail: Cat 12 mit 600 Mbit/s Download, Cat 13 mit 150 Mbit/s Upload, Qualcomm MDM9250, M.2-Formfaktor, Drei-Antennen-MIMO und Multi-Konstellation-GNSS. Pflichtlektüre für die Auswahl von Firmen-CBRS-Privatnetzen und Industrieroutern, inklusive vollständigem Vergleich von Bändern, Temperaturen und Zertifizierungen. Zusammengestellt von Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em7565", "lte-a", "cat-12", "cat-13", "cbrs", "m2", "gnss", "wwan", "private-lte"]
featureimage: "/images/products/sierra/EM7565_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "Unterstützt der EM7565 CBRS-Privatnetze (Band 48)?"
    answer: "Das offizielle Datenblatt (Rev 8, Oktober 2018) listet Band 48 (3550–3700 MHz, CBRS-Band), markiert B42/B43/B48 zum Zeitpunkt der Veröffentlichung jedoch als disabled, in Erwartung der regulatorischen Freigabe. Für CBRS-Einsätze zählt immer das aktuelle offizielle Datenblatt, die Firmware-Version und der damalige Regulierungsstatus."
  - question: "Wie schnell ist der Upload des EM7565 wirklich?"
    answer: "Der Upload läuft über LTE Cat 13 (2×CA contiguous, 64QAM) mit einem theoretischen Maximum von 150 Mbit/s; der Download über Cat 12 (3×CA, 256QAM) mit 600 Mbit/s. Der reale Durchsatz hängt von Basisstation, Signalqualität und Firmware-Version ab."
  - question: "Hat der EM7565 eingebaute Antennen? Wie viele Antennen brauche ich?"
    answer: "Nein, es gibt keine eingebauten Antennen. Das Modul hat 3 RF-Anschlüsse: Main (Tx/Rx), GNSS und Auxiliary (Diversity/MIMO/GNSS). Für LTE brauchst du mindestens ein externes 2×2-MIMO-Antennensystem; Antennen und Zuleitungen musst du auf der Host-Seite selbst auslegen."
  - question: "In welchem Temperaturbereich arbeitet der EM7565?"
    answer: "Klasse A (3GPP-konform): -30°C bis +70°C; Klasse B (nicht 3GPP): -40°C bis +85°C, mit geeigneter Kühlung und reduzierten Betriebsparametern. Die Innentemperatur des Moduls muss unter 90°C bleiben, empfohlen werden unter 80°C."
  - question: "Kann ich den EM7565 unter Linux verwenden?"
    answer: "Ja. Die USB-Schnittstelle unterstützt QMI (Linux und Android) und MBIM (Windows 8.1/10 und Linux), außerdem gibt es eine AT-Befehlsschnittstelle nach 3GPP TS 27.007 und ein Linux SDK. Die tatsächliche Treiberunterstützung hängt von Distribution und Kernel-Version ab."
---

# EM7565 im Detail: CBRS-Privatnetz und hohe Upload-Geschwindigkeit, wie wählst du das richtige Firmennetz?

Wenn du an deinem Lab-Projekt arbeitest oder gerade ein Projekt für ein Firmen-Privat-LTE- oder CBRS-Netz übernommen hast, wirst du in jeder Diskussionsliste auf das M.2-Modul EM7565 stoßen. Aber Achtung: „Häufig erwähnt" heißt nicht „gekauft, eingesteckt, und schon läuft CBRS".

In diesem Artikel verzichten wir auf Marketing-Floskeln. Unsere einzige Grundlage ist das offizielle Datenblatt von Sierra Wireless, „AirPrime EM7565 Product Technical Specification" (Doc 41110788, Rev 8, Oktober 2018). Wir prüfen Punkt für Punkt Chip, Geschwindigkeiten, Bänder, Antennen, Temperaturen und Zertifizierung und sagen dir ehrlich, was der Vorbehalt „in Erwartung der regulatorischen Freigabe" im Datenblatt bedeutet. So unterstützen wir Studierende und Ingenieure aus Systemintegration und Netzwerkarchitektur bei der Kaufentscheidung.

> Produktlink: [EM7565 — Yupitek-Produktseite](/de/products/sierra/em7565/) | Offizielles Datenblatt: [AirPrime EM7565 Product Technical Specification](https://yupitek.com/docs/sierra/EM7565_spec.pdf)

---

## Das Wichtigste zuerst: Was ist der EM7565 eigentlich?

**Der EM7565 ist ein WWAN-Zellularemodul von Sierra Wireless im M.2-Formfaktor mit Qualcomm-MDM9250-Chip. Er erreicht LTE Cat 12 im Download (bis 600 Mbit/s) und Cat 13 im Upload (bis 150 Mbit/s) und bietet zusätzlich Multi-Konstellation-GNSS-Positionierung.**

Direkte Antworten auf die drei wichtigsten Fragen:

| Frage | Direkte Antwort |
|---|---|
| **Kann ich mit dem EM7565 ein CBRS-Privatnetz aufbauen?** | Im Datenblatt ist LTE Band 48 (das 3,5-GHz-Band für CBRS) tatsächlich gelistet, aber zum Zeitpunkt der Veröffentlichung von Rev 8 war es als „disabled, in Erwartung der regulatorischen Freigabe" markiert. Für den kommerziellen Einsatz gelten immer die aktuelle Gesetzeslage und das neueste offizielle Datenblatt. Frag uns vor der Bestellung und prüfe die aktuellen Dokumente! |
| **Wie schnell ist der Upload?** | Bis zu 150 Mbit/s (Cat 13); der Download erreicht bis zu 600 Mbit/s (Cat 12). |
| **Für wen ist er am besten geeignet?** | Für Industrierouter im Firmeneinsatz und Systemintegratoren, die beim Edge Computing „große Datenmengen in die Cloud übertragen" müssen (wegen der hohen Upload-Geschwindigkeit). Wenn du ein Maker bist und mit Raspberry Pi bastelst, geht das auch mit einem M.2-auf-USB-Adapter. |
| **Hat er eingebaute Antennen?** | Nein! Auf der Karte gibt es nur 3 kleine RF-Anschlüsse (Main, GNSS, Auxiliary). Antennen musst du selbst kaufen und die Leitungslayouts selbst entwerfen. |

---

## Die vollständige EM7565-Spezifikationstabelle (direkt mit den offiziellen Daten verglichen)

Ingenieure lieben Zahlen. Alle Werte unten stammen aus dem offiziellen Datenblatt von Sierra Wireless; die Quellenzeilen findest du im Verification Log am Ende des Dokuments.

| Punkt | Spezifikation | Quelle |
|---|---|---|
| **Modell** | AirPrime EM7565 (Dokumentnummer 41110788, Rev 8) | Datenblatt-Titelseite |
| **Formfaktor** | M.2 (WWAN Type 3042-S3-B) | Seite 14 des Datenblatts |
| **Chipsatz** | Qualcomm-MDM9250-Basisbandprozessor | Seite 12 des Datenblatts |
| **Zellularstandard** | LTE: 3GPP Release 11; UMTS: 3GPP Release 9 | Seite 18 des Datenblatts |
| **Download-Maximum** | Cat 12, 3×CA, 256QAM: 600 Mbit/s (Cat 9: 450 Mbit/s) | Seite 12 des Datenblatts |
| **Upload-Maximum** | Cat 13, 2×CA contiguous, 64QAM: 150 Mbit/s | Seite 12 des Datenblatts |
| **Carrier Aggregation** | DL LTE-FDD: 60 MHz; DL LTE-TDD: 60 MHz; UL LTE: 40 MHz (intraband contiguous) | Seite 15 des Datenblatts |
| **MIMO** | 2×2 / 4×2 im Download | Seite 12 des Datenblatts |
| **UMTS-Geschwindigkeiten** | DC-HSPA+ bis 42 Mbit/s Download, bis 11 Mbit/s Upload | Seite 12 des Datenblatts |
| **LTE-Bänder** | B1/B2/B3/B4/B5/B7/B8/B9/B12/B13/B18/B19/B20/B26/B28/B29(DL)/B30(DL)/B32(DL)/B41/B42/B43/B46/B48/B66 (B42/43/48 zum Zeitpunkt der Veröffentlichung als disabled markiert) | Seite 42 des Datenblatts |
| **WCDMA-Bänder** | Band 1/2/4/5/6/8/9/19 | Seite 43–44 des Datenblatts |
| **Schnittstellen** | USB 2.0 + USB 3.0; QMI, MBIM; AT-Befehle | Seite 15, 28 des Datenblatts |
| **SIM** | Dual-SIM (1.8V oder 3V), aber der SIM-Kartenhalter muss von dir bereitgestellt werden | Seite 29 des Datenblatts |
| **Antennenschnittstellen** | 3 RF-Anschlüsse: Main, GNSS, Auxiliary | Seite 37 des Datenblatts |
| **GNSS** | Gleichzeitige Verfolgung von GPS, GLONASS, Galileo, BeiDou, QZSS; Kaltstart 32 Sekunden | Seite 47 des Datenblatts |
| **Abmessungen** | 42±0,15 × 30±0,15 mm | Seite 57 des Datenblatts |
| **Gewicht** | 6,5 g | Seite 57 des Datenblatts |
| **Betriebstemperatur** | Klasse A: -30°C bis +70°C; Klasse B: -40°C bis +85°C (mit Kühlung und Taktreduzierung) | Seite 14, 57 des Datenblatts |
| **Innentemperatur des Moduls** | Muss unter 90°C bleiben, empfohlen unter 80°C | Seite 14 des Datenblatts |
| **Regulierungszertifizierung** | Konform mit FCC (USA), IC (Kanada), NCC (Taiwan), MIC (Japan), RED (EU) usw. | Seite 62 des Datenblatts |

> **Wichtig**: Die obigen Zahlen basieren auf Rev 8 (Oktober 2018). Firmware und Zertifizierung ändern sich mit der Zeit. Wenn du bestellen willst, hol dir vorher bei uns die aktuellen offiziellen Dokumente und prüfe noch einmal.

---

## Das viel diskutierte CBRS-Privatnetz: funktioniert der EM7565 dafür?

**Kurz gesagt: Hardware-seitig ist Unterstützung da, aber Firmware und Regulierung hängen vom aktuellen Stand ab.**

Im Datenblatt ist Band 48 (3550–3700 MHz) für CBRS tatsächlich enthalten, aber (und dieses „aber" ist wichtig) zum Zeitpunkt der Veröffentlichung von Rev 8 waren B42/B43/B48 eindeutig markiert als „disabled as of publication date, support pending regulatory approval" (zum Veröffentlichungsdatum deaktiviert, Unterstützung in Erwartung der regulatorischen Freigabe).

Wir können also nicht pauschal garantieren, dass man das Modul „kauft und direkt ein CBRS-Netz aufbaut". Wenn du ein CBRS-Privatnetz planst, musst du drei Dinge prüfen: ob B48 in der aktuellen Firmware freigeschaltet ist, ob das Gerät der aktuellen FCC-Part-96-Zertifizierung entspricht und ob das komplette System OTA besteht. Bei Bedarf fragst du am besten zuerst bei uns nach dem aktuellen Stand.

---

## Cat 12 Download + Cat 13 Upload: Was bedeutet das für dein Projekt?

**Das Highlight ist eigentlich nicht der Download, sondern die „extrem starke Upload-Fähigkeit"!**

Normalerweise laden wir am Handy viel herunter (Videos schauen, Feed scrollen). Aber in industriellen Anwendungen oder IoT-Projekten müssen Geräte oft „Daten in die Cloud hochladen". Der EM7565 liefert im Upload Cat 13 (bis 150 Mbit/s, 2×CA, 64QAM) und im Download Cat 12 (bis 600 Mbit/s, 3×CA, 256QAM).

Das ist ideal für Szenarien mit **höherem Upload- als Download-Bedarf**: „die Überwachungskamera in der Fabrik soll das Bild in Echtzeit an die Leitstelle übertragen", „die Sensordaten des autonomen Fahrzeugs sollen massenhaft in die Cloud hochgeladen werden". Wenn dein Projekt nur braucht, dass das Gerät ins Internet geht und Daten abruft, reicht ein günstigeres Cat-6-Modul (zum Beispiel EM7455) völlig aus.

---

## Welche Bänder unterstützt der EM7565?

**Kurze Antwort: Insgesamt 24 LTE-Bänder (inklusive B1–B66) und 8 WCDMA-Bänder. Die gängigen Bänder in Taiwan und der Asien-Pazifik-Region sind im Wesentlichen abgedeckt.**

### Die LTE-Bänder im Überblick:

- **Gängige Bänder**: B1, B3, B7, B8, B28 (die meisten taiwanischen und asiatisch-pazifischen Carrier nutzen diese).
- **Nur Download**: B29, B30 (Tx deaktiviert), B32, B46 (LTE-LAA).
- **In Erwartung der regulatorischen Freigabe (zum Zeitpunkt der Veröffentlichung)**: B42, B43, B48 (CBRS).

Wenn dein Projekt in Taiwan läuft, ist die Abdeckung des EM7565 absolut kein Problem. Aber wenn das Labor Privatnetze oder spezielle Bänder (wie B48) testen will, bestelle nicht blind nach dem alten Datenblatt, sondern frag erst nach dem aktuellen Stand.

---

## Drei-Antennen-Design: Die RF-Leitungsführung musst du selbst lösen

**Der EM7565 hat keine eigenen Antennen; die Antennen müssen auf dem Mainboard selbst designed werden.** Er hat drei kleine RF-Anschlüsse: Main (Hauptantenne für Senden/Empfangen), Auxiliary (Diversity-/MIMO-Antenne) und GNSS (Positionsantenne).

Für LTE brauchst du mindestens die beiden Antennen Main und Auxiliary als 2×2 MIMO. Die Anschlüsse sind im I-PEX-MHF4-Standard. Der Hersteller empfiehlt einen VSWR (Spannungsstehwellenverhältnis) von besser als 2:1 und eine Strahlungseffizienz über 50 %. Das heißt: Wenn du im Projekt eigene Platinen fertigst und Antennen auslegst, solltest du dich auf RF-Tests einstellen.

---

## GNSS: Internet und Ortung in einem Chip

Wenn dein Projekt mit „Fahrzeugen" oder „Logistik" zu tun hat, bietet dieses Modul direkt die Verfolgung von fünf Konstellationen (GPS, GLONASS, Galileo, BeiDou, QZSS) mit bis zu 30 gleichzeitig verfolgten Kanälen. Der Kaltstart dauert etwa 32 Sekunden und liefert dir direkt Standard-NMEA-0183-Daten. So sparst du dir den Kauf eines separaten GPS-Moduls und den Platz auf der Platine.

---

## Weitbereichstemperatur-Design: Industrielle Robustheit

Im Industriebetrieb fürchtet man vor allem Wärmeabschaltungen. Der EM7565 hält nach 3GPP-Standard Umgebungstemperaturen von -30°C bis +70°C aus; mit guter Kühlung schafft er im Extremfall -40°C bis +85°C (allerdings mit Leistungseinbußen).

**Tipp aus der Lab-Praxis**: Laut Datenblatt darf die Innentemperatur des Moduls (abfragbar mit `AT!PCTEMP`) **auf keinen Fall 90°C überschreiten, idealerweise bleibt sie unter 80°C**. Wenn du das Modul also in ein kleines Gehäuse steckst und mit vollem Upload laufen lässt, denk an Wärmeleitpads oder einen Lüfter, sonst greift der Schutzmechanismus und reduziert die Geschwindigkeit oder schaltet ab!

---

## Stromversorgung und Leistungsaufnahme: Wähle das Netzteil nicht auf gut Glück

Der EM7565 wird mit 3.135V bis 4.4V versorgt (typisch 3.3V). Achtung: Bei Volllast oder im Einschaltmoment steigt der Strom stark an:

- **Peakstrom**: 1,3A (Mittelwert über 100 Mikrosekunden)
- **Maximalstrom**: 1,5A
- **Kurzzeitiger Einschaltstrom**: 2,2A bis 2,5A

Wenn du also deine eigene Platine designst und einen DC-DC-Abwärtswandler oder ein LDO auswählst, plane die Reserve nach „2,5A Einschaltstrom" ein. Verlass dich nicht auf „nur 2,8mA im Standby" und nimm dann einen Strom-IC, der die Last nicht schafft.

---

## Regulierung und Zertifizierung

Im Datenblatt heißt es, die Konstruktion entspreche den Standards FCC (USA), NCC (Taiwan), RED (EU) usw. und sei mit GCF und PTCRB zertifiziert. Für Unternehmen, die Produkte auf den Markt bringen, spart das viel Zertifizierungsaufwand. Aber denk daran: Zertifiziert ist nur das „Modul". Dein fertiges „Gerät" muss trotzdem die FCC- oder NCC-Prüfung bestehen, sonst ist es nicht legal.

---

## Fazit: Solltest du den EM7565 kaufen?

| Dein Bedarf | Passt der EM7565? | Warum? |
|---|---|---|
| Ich brauche extrem hohe Upload-Geschwindigkeit | ✅ Sehr gut geeignet | Die 150 Mbit/s von Cat 13 sind genau für dich gemacht. |
| Ich will ein CBRS-Privatnetz testen | ⚠️ Erst kurz warten | Hardware-seitig wird B48 unterstützt, aber den Firmware- und Regulierungsstatus klärst du bitte zuerst mit uns. |
| Ich brauche nur Internet und will Textdateien übertragen | ❌ Overkill | Ein günstiges Cat 4 oder Cat 6 (zum Beispiel EM7455) reicht und spart dem Chef Budget. |
| Ich mache Flottenmanagement und brauche präzise Ortung | ✅ Sehr gut geeignet | 4G und Fünf-Konstellationen-Ortung in einem, kein zusätzlicher GPS-Chip nötig. |

### Schnellvergleich: EM7565 vs. EM7455

| Punkt | EM7565 | EM7455 |
|---|---|---|
| Download | 600 Mbit/s (Cat 12, 3×CA) | 300 Mbit/s (Cat 6, 2×CA) |
| Upload | 150 Mbit/s (Cat 13, 2×CA) | 50 Mbit/s (Cat 6) |
| Chip | Qualcomm MDM9250 | Qualcomm MDM9230 |

---

## Schnelles Q&A zu häufigen Fragen

{{< faq >}}

---

## Sprich mit uns über dein Projekt

Diese technische Deep-Dive-Analyse hat das Engineering-Team von Yupitek zusammengestellt. Wenn du gerade ein 4G-Modul für dein Labor auswählst oder dein Firmenprojekt Mengenangebote für den EM7565 und Unterstützung beim Antennendesign braucht, sprich uns gerne an.

- **EM7565-Produktseite**: [https://yupitek.com/de/products/sierra/em7565/](/de/products/sierra/em7565/)
- **Weitere Sierra-Modelle**: [https://yupitek.com/de/products/sierra/](/de/products/sierra/)
- **Kontakt-E-Mail**: sales@yupitek.com
