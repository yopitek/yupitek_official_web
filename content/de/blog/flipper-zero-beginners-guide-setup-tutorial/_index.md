---
title: "Flipper Zero Einsteiger-Tutorial: Auspacken, Einrichten, Firmware-Update und fünf praktische Funktionen"
locale: de
hreflang_group: flipper-zero-beginners-guide-setup-tutorial
slug: flipper-zero-beginners-guide-setup-tutorial
published: 2026-08-10
author: Yupitek
category: Technical
tags:
  - Flipper Zero
  - Tutorial
hero_image: /static/img/flipper-zero/hero.webp
hero_alt: "Flipper Zero Einsteiger-Tutorial: Auspacken, Firmware-Update und fünf Funktionen im Test | Yupitek"
seo_description: "Was ist Flipper Zero? Von Auspacken, microSD-Einrichtung und qFlipper-Firmware-Update bis hin zu Tests der fünf Funktionen RFID, Sub-GHz, NFC, IR und BadUSB – dieser Leitfaden bringt Sie schnell auf den Stand."
date: 2026-08-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
  - Flipper Zero
  - Tutorial
categories:
  - Technical
lastmod: 2026-08-10
---

# Flipper Zero Einsteiger-Tutorial: Auspacken, Einrichten, Firmware-Update und fünf praktische Funktionen

> TL;DR: Flipper Zero ist ein tragbares Hardware-Entdeckungstool mit eingebauter 125-kHz-RFID-, Sub-GHz-, NFC-, Infrarot- und BLE-Unterstützung. Es kann über USB-C mit einem Computer verbunden werden, um eine Tastatur zu simulieren (BadUSB). Nach dem Kauf installieren Sie zuerst eine microSD-Karte, aktualisieren die Firmware über qFlipper oder die mobile App und beginnen Sie mit dem Auslesen von RFID-Karten und der Infrarot-Fernbedienung. Alle Funktionen sollten Sie nur an Geräten verwenden, die Ihnen gehören oder für die Sie eine Genehmigung haben.

## Was ist Flipper Zero? Für wen ist es geeignet?

Flipper Zero ist ein multifunktionales, handtellergroßes Gerät, das als „Hardware-Entdeckungstool“ positioniert ist. Es ist kein allgemeines Konsumgadget, sondern ein Gerät, das für Sicherheitsforscher, Penetrationstesting-Einsteiger, Maker und IoT-Ingenieure entwickelt wurde, um gängige Funkprotokolle und digitale Signale auszulesen, zu analysieren und zu simulieren.

Die Kernhardware umfasst:

- **125 kHz RFID**: Auslesen und Simulieren von Niederfrequenz-Zutrittskarten
- **Sub-GHz-Funk** (CC1101-Chipsatz): Analyse von Signalen für Fernbedienungen, Garagentore und IoT-Sensoren im Bereich 300–928 MHz
- **NFC (13,56 MHz)**: Auslesen, Schreiben und Simulieren von Hochfrequenzkarten
- **Infrarot (IR)**: Erlernen und Wiederholen von Infrarot-Fernbedienungscode für Fernseher, Klimaanlagen usw.
- **BLE**: Kopplung, Steuerung und Updates über die mobile App
- **USB-C**: Verbindung mit dem Computer zum Firmware-Update und zur Tastatursimulation (BadUSB / DuckyScript)
- **GPIO / iButton**: 1-Wire-Kontaktschlüssel und Hardware-Erweiterungen

Zielgruppe: Studierende, die in die drahtlose Sicherheitsforschung einsteigen wollen, Ingenieure, die die Zuverlässigkeit ihrer eigenen Zutrittskontrollen oder Sensoren überprüfen müssen, und Maker, die die Prinzipien von RFID/NFC verstehen möchten. Wenn Sie lediglich einen „Fernbedienungs-Kopierer“ suchen, kann die Sub-GHz-Funktion dies leisten, aber prüfen Sie bitte vorab die lokalen Gesetze und Anwendungsszenarien.

## Auspacken und Erste Einrichtung: Zuerst die microSD einlegen, dann einschalten

Flipper Zero wird ohne microSD-Karte ausgeliefert, die Verwendung einer Speicherkarte für Firmware und Datenspeicherung wird jedoch **dringend empfohlen**. Gehen Sie wie folgt vor:

1. **Vorbereiten der microSD-Karte**: Eine Karte mit mindestens 4 GB wird empfohlen. Das Dateisystem sollte FAT32 sein (FAT16/FAT32/exFAT sind ebenfalls möglich). Legen Sie die Karte mit den **Kontakten nach oben** in den Kartensteckplatz an der Unterseite des Geräts ein.
2. **Aufladen**: Verbinden Sie das Gerät über USB-C mit einem Ladegerät oder einem Computer und laden Sie es vor der ersten Verwendung vollständig auf.
3. **Einschalten**: Drücken Sie die Zurück-Taste (Back) auf der Rückseite des Gehäuses etwa 3 Sekunden lang gedrückt. Wenn die Delfin-Animation auf dem Bildschirm erscheint, ist das Einschalten abgeschlossen.
4. **Systemversion überprüfen**: Gehen Sie zu `Einstellungen → Über`, notieren Sie die aktuelle Firmware-Version für den nächsten Schritt.

> Hinweis: Flipper Zero startet standardmäßig mit einer englischen Benutzeroberfläche. Einige Drittanbieter-Firmwares bieten chinesische Sprachpakete an, aber **Anfängern wird nicht empfohlen**, sich zunächst mit Drittanbieter-Firmwares zu beschäftigen. Warten Sie, bis Sie mit dem offiziellen Firmware-Prozess vertraut sind.

## Firmware-Update: qFlipper Desktop-Version und mobile App

Das Firmware-Update ist der wichtigste Schritt beim Einstieg in Flipper Zero – der Hersteller behebt weiterhin Bugs und fügt neue Protokollunterstützungen hinzu. Ältere Firmwares können möglicherweise bestimmte Karten oder Signale nicht mehr lesen.

### Methode 1: qFlipper Desktop-Version (Empfohlen)

1. Laden Sie qFlipper für Ihre Plattform (Windows / macOS / Linux) von der offiziellen Flipper-Website herunter.
2. Verbinden Sie Flipper Zero über USB-C mit dem Computer und öffnen Sie qFlipper.
3. Klicken Sie auf das Schraubensymbol oben rechts (Erweiterte Einstellungen) und wählen Sie „Firmware-Update-Kanal“.
4. Wählen Sie **Release (Stabile Version)** und klicken Sie auf „Update“.
5. Warten Sie, bis das Update abgeschlossen ist (ca. 5–10 Minuten). Das Gerät startet automatisch neu.

### Methode 2: Mobile App

1. Installieren Sie die offizielle Flipper Mobile App (iOS / Android).
2. Aktivieren Sie Bluetooth auf Ihrem Smartphone und koppeln Sie es mit Flipper Zero (am Gerät: `Einstellungen → Bluetooth`).
3. Tippen Sie in der App auf „Update“. Die Übertragung erfolgt über BLE und dauert etwa 10 Minuten.

### Wie wählt man den Firmware-Kanal?

| Kanal | Stabilität | Zielgruppe |
|---|---|---|
| Release (Stabil) | Hoch | **Neue Benutzer sollten immer dies wählen** |
| Release Candidate (RC) | Mittel | Benutzer, die neue Funktionen vorab testen möchten |
| Development (Entwicklung) | Niedrig | Entwickler und Tester |

> ⚠️ Ziehen Sie während des Updates keine Kabel und schalten Sie das Gerät nicht aus. Falls das Gerät im Startbildschirm hängen bleibt, können Sie den Wiederherstellungsmodus aufrufen und die Firmware neu flashen (zweimal schnell auf Reset drücken). Drittanbieter-Firmwares (wie Xtreme) bieten zwar erweiterte Funktionen, können aber instabil sein. Anfänger sollten zunächst die offizielle stabile Version verwenden.

## Tests der fünf praktischen Funktionen

### 1. 125 kHz RFID: Auslesen und Simulieren von Niederfrequenzkarten

Ältere Zutrittskarten (125 kHz) verfügen oft nur über eine ID-Codierung ohne Verifizierungsmechanismus. Flipper Zero verfügt an der Unterseite über eine LF-Antenne, die zum Auslesen einfach an die Karte gehalten wird:

1. Hauptmenü → `125 kHz RFID` → `Lesen`.
2. Legen Sie die Karte flach an die Unterseite des Geräts. Bei erfolgreichem Auslesen werden UID und Daten angezeigt.
3. Um die Karte zu simulieren, wählen Sie nach dem Auslesen `Emulieren`. Das Gerät fungiert nun als temporäre Ersatzkarte.

### 2. Sub-GHz: Analyse von 300–928 MHz-Funksignalen

Der eingebaute CC1101-Transceiver kann Signale von Fernbedienungen, Garagentoren und IoT-Sensoren erfassen:

1. Hauptmenü → `Sub-GHz` → `Raw lesen`.
2. Drücken Sie eine Taste an der Fernbedienung. Auf dem Bildschirm werden Frequenz und Signalwellenform angezeigt.
3. Nach dem Speichern können Sie das Signal über `Wiedergeben` erneut senden. Sie können auch manuell Frequenzen einstellen, um Funkaktivitäten in der Umgebung zu scannen.

### 3. NFC: Auslesen, Schreiben und Simulieren von 13,56-MHz-Karten

Das NFC-Modul unterstützt gängige 13,56-MHz-Standards. Es kann die UID und Datenblöcke von kontaktlosen Karten wie TransLink-Karten auslesen (ob eine vollständige Simulation möglich ist, hängt vom Verschlüsselungsmechanismus der Karte ab):

1. Hauptmenü → `NFC` → `Lesen`.
2. Halten Sie die Karte an den Induktionsbereich auf der Rückseite des Geräts, um die Karteninformationen auszulesen.
3. Je nach Kartentyp können Sie `Emulieren` oder `Schreiben` auswählen.

### 4. IR: Erlernen und Wiederholen von Infrarot-Fernbedienungen

Das eingebaute Infrarot-Sende-/Empfangsmodul kann Fernbedienungscode für Fernseher, Klimaanlagen und Beamer lernen und erneut senden:

1. Hauptmenü → `Infrarot` → `Lernen`.
2. Richten Sie die Infrarot-Öffnung am oberen Rand des Geräts auf die Fernbedienung und drücken Sie eine Taste. Nach erfolgreichem Lernen wird der Code benannt und gespeichert.
3. Unter `Infrarot → Gespeichert` können Sie den Code jederzeit erneut senden.

### 5. BadUSB / DuckyScript: USB-C-Tastatursimulation

Wenn das Gerät mit einem Computer verbunden ist, kann Flipper Zero eine USB-Tastatur simulieren und DuckyScript-Skripte ausführen (automatische Eingabe von Befehlen):

1. Legen Sie `.txt`-Skripte (im DuckyScript-Format) in den Ordner `badusb/` auf der microSD-Karte ab.
2. Verbinden Sie das Ziel-Computergerät über USB-C. Gehen Sie im Hauptmenü zu `BadUSB` und wählen Sie das Skript zur Ausführung aus.

> ⚠️ **BadUSB ist eine hochsensible Funktion**: Skripte werden als Tastatureingaben auf dem Computer ausgeführt, was gleichbedeutend damit ist, „dass jemand vor dem Computer sitzt und tippt“. Verwenden Sie diese Funktion nur auf Ihrem eigenen Computer oder in Umgebungen, die ausdrücklich für Tests freigegeben sind.

## Hinweise zur rechtmäßigen Verwendung (Wichtig)

Flipper Zero ist an sich ein legales Werkzeug, aber die Anwendungsszenarien haben klare rechtliche Grenzen:

- **Kopieren/Simulieren von Zutrittskarten und Fernbedienungen**: Dies darf nur für Systeme erfolgen, die Ihnen gehören oder für die Sie eine Administratorgenehmigung haben. Das unbefugte Auslesen oder Simulieren von Zutrittskarten oder Garagenfernbedienungen Dritter kann in Taiwan strafrechtliche Konsequenzen nach sich ziehen (z. B. Verletzung des Geheimnisses, Telekommunikationsgesetz oder Datenschutzgesetze).
- **BadUSB**: Das unbefugte Ausführen von Skripten auf fremden Computern ist rechtswidrig.
- **Signalstörungen**: Das vorsätzliche Stören anderer Funkgeräte (z. B. Garagentore) birgt ebenfalls rechtliche Risiken.

**Die Regel ist einfach: Testen Sie nur Ihre eigenen Geräte oder solche, für die Sie eine schriftliche Genehmigung haben.**

## Häufig gestellte Fragen (FAQ)

**F1: Muss ich bei Flipper Zero zuerst eine microSD-Karte einlegen?**
Nicht zwingend, aber dringend empfohlen. Die meisten Apps, Signalbibliotheken und BadUSB-Skripte werden auf der microSD gespeichert. Ohne Karte sind die Funktionen stark eingeschränkt.

**F2: Kann das Firmware-Update das Gerät unbrauchbar machen (Bricking)?**
Das Risiko bei der offiziellen stabilen Firmware ist extrem gering. Solange während des Updates keine Stromunterbrechung oder Kabeltrennung erfolgt, ist ein Fehlschlagen fast ausgeschlossen. Im Fehlerfall können Sie den Wiederherstellungsmodus aufrufen, um die Firmware neu zu flashen.

**F3: Kann ich TransLink-Karten kopieren?**
Die meisten modernen Wertkarten sind verschlüsselt und durch Schlüssel geschützt. Flipper Zero kann nur die UID oder unverschlüsselte Blöcke auslesen, eine vollständige Kopie ist nicht möglich. Zudem ist das unbefugte Kopieren von Wertkarten selbst rechtswidrig.

**F4: Was ist der Unterschied zwischen Flipper Zero und SDR (Software Defined Radio)?**
Flipper Zero verfügt über einen eingebauten Sub-GHz-Transceiver, der auf gängige Protokolle (OOK/ASK/FSK usw.) spezialisiert ist und eine intuitive Bedienung bietet. SDR-Geräte (wie HackRF, RTL-SDR) haben einen breiteren Frequenzbereich und ermöglichen die Anzeige des Rohspektrums, erfordern jedoch einen Computer und tieferes Hintergrundwissen. Beide sind sich ergänzende Werkzeuge.

**F5: Wo kann man Flipper Zero kaufen?**
Yupitek (Yuhé Technology) bietet Flipper Zero-Produkte und Zubehör an und bietet technische Beratung. Für Fragen zur Einrichtung können Sie uns nach dem Kauf unter sales@yupitek.com kontaktieren.

**F6: Kann ich Drittanbieter-Firmware installieren?**
Ja, das ist möglich, aber für Anfänger nicht empfohlen. Drittanbieter-Firmwares (wie Xtreme) bieten eine verbesserte Benutzeroberfläche und zusätzliche Funktionen, aber Stabilität und Sicherheit müssen selbst bewertet werden. Zudem kann der Support für offizielle Updates verloren gehen.

## Zusammenfassung

Der Einstieg in Flipper Zero ist unkompliziert: **microSD einlegen → Offizielle stabile Firmware aktualisieren → Mit RFID-Auslesen und IR-Fernbedienung beginnen → Nach Einarbeitung Sub-GHz und BadUSB erkunden**. Es ist ein hervorragender Ausgangspunkt, um Funkprotokolle und Hardware-Sicherheit zu verstehen. Denken Sie jedoch immer daran: Je leistungsfähiger die Funktion, desto größer die Selbstkontrolle – testen Sie nur Geräte, für die Sie berechtigt sind.

Wenn Sie Flipper Zero oder Zubehör benötigen, senden Sie uns bitte eine E-Mail an [sales@yupitek.com](mailto:sales@yupitek.com). Yupitek bietet Produkt- und technische Beratungsdienstleistungen an.