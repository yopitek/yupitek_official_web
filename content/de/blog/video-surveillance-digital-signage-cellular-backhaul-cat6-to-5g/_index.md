---
title: "Mobiles Backhaul für Videoüberwachung und Digital Signage: Wie wählst du zwischen Cat 6 und 5G? | Yupitek"
description: "Welches Mobilfunkmodul brauchen Kameras und Digital Signage? Der Schlüssel liegt darin, ob der Traffic nach oben oder unten fließt! Dieser Artikel vergleicht EM7455 (Cat 6), EM7565 (Cat 12) und EM9191 (5G) anhand der offiziellen Spezifikationen, damit du präzise auswählst und kein Geld verbrennst."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "de"
hreflang_group: "video-surveillance-digital-signage-cellular-backhaul-cat6-to-5g"
slug: "video-surveillance-digital-signage-cellular-backhaul-cat6-to-5g"
tags: ["Sierra Wireless", "EM7455", "EM7565", "EM9191", "4G Videoüberwachung", "Digital Signage", "5G Video-Backhaul", "Cat 6", "LTE"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/de/products/sierra/"
faq:
  - question: "Wie viel Upload braucht eine Überwachungskamera bei 4G-Backhaul?"
    answer: "Ein 1080p-H.264-Stream belegt etwa 2~6 Mbit/s. Mit dem EM7455 (Upload-Limit 50 Mbit/s) lassen sich stabil etwa 4~6 1080p-Streams übertragen. Bei größerem Bedarf empfiehlt sich das Upgrade auf den EM7565."
  - question: "Reicht Cat 6 für die Anbindung von Digital Signage?"
    answer: "Digital Signage arbeitet hauptsächlich mit Downloads. Cat 6 (z.B. EM7455) liefert 300 Mbit/s Download, das reicht für normale Bild- und Video-Updates locker. Wer häufig sehr große 4K-Videodateien ausliefern muss, kann auf den EM7565 (600 Mbit/s) upgraden, um die Downloadzeit zu verkürzen."
  - question: "Worauf muss ich achten, wenn ich ein 4G/5G-Modul in einen Außenkasten einbaue?"
    answer: "Zwei Punkte sind entscheidend: Kühlung und Stromversorgung. Die Innentemperatur des Moduls darf meist nicht über 90°C~115°C steigen. In Außenkästen droht schnell Überhitzung, also braucht es einen guten Wärmeabfluss. Außerdem kann ein 5G-Modul kurzzeitig bis zu 2.7A ziehen, das Netzteil muss diesen Stromstoß aushalten."
---

Überwachungskameras schicken Bilder ins Backend, und digitale Werbetafeln am Straßenrand laden die neuesten Werbespots herunter. Wie viel 4G/5G-Modul braucht man dafür wirklich? Der entscheidende Punkt ist nicht „je schneller, desto besser“, sondern die Frage, wohin der Traffic fließt: nach oben oder nach unten. Wir nehmen drei bekannte Sierra-Wireless-Module als Beispiel, EM7455, EM7565 und EM9191, und zeigen dir anhand der echten Zahlen aus den offiziellen Spezifikationen, ob du Cat 6, Cat 12 oder gleich 5G brauchst.

{{< tldr >}}
Kameras senden Bilder ans Backend, Werbetafeln laden die neuesten Werbespots herunter. Der Schlüssel ist nicht „je schneller, desto besser“, sondern die Richtung des Traffics: hoch oder runter. Wir nehmen EM7455, EM7565 und EM9191 als Beispiel und zeigen dir anhand der offiziellen Spezifikationen, ob du Cat 6, Cat 12 oder direkt 5G brauchst.
{{< /tldr >}}

**Kurz gesagt: Verliebe dich nicht sofort in 5G. Frag dich zuerst, ob dein Gerät „viel hochlädt“ oder „viel runterlädt“. Eine Kamera überträgt ständig Bilder in die Cloud: Achte auf die Upload-Geschwindigkeit (Uplink). Eine Werbetafel lädt ständig neue Videos herunter: Achte auf die Download-Geschwindigkeit (Downlink). Wenn du nur ein paar 1080p-Bilder übertragen willst, reicht die günstigste Cat-6-Karte locker!**

Viele Betreiber sagen bei der Vergabe von Netzwerkprojekten für „Straßenkameras“ oder „Werbetafeln von Filialketten“ sofort: „Gib mir das schnellste 5G-Modul!“
Am Ende geben sie viel Geld aus und stellen fest, dass sie es gar nicht brauchen.

Die Auswahl einer Netzwerkkarte ist keine Sportwagenwahl. Es geht nicht um maximale Geschwindigkeit, sondern darum, das passende Mittel für die Aufgabe zu wählen. In diesem Artikel nehmen wir die drei gängigsten M.2-Module von Sierra Wireless (EM7455, EM7565, EM9191) unter die Lupe und zeigen dir anhand der Zahlen aus den offiziellen Spezifikationen, wie du am wirtschaftlichsten auswählst.

> Quelle der technischen Daten: offizielle Spezifikationen von Sierra Wireless. Artikel zusammengestellt von Yupitek.

---

## Schnellauswahl in 30 Sekunden: Welche Karte solltest du kaufen?

| Dein Einsatzszenario | Haupt-Traffic | Welche Karte? | Warum? |
|---|---|---|---|
| **Kleines Projekt: 1~4 Kameras 1080p** | Upload (UL) | **EM7455 (Cat 6)** | Das Upload-Limit liegt bei 50 Mbit/s, das reicht locker für ein paar 1080p-Kameras, und es ist am günstigsten. |
| **Mittel bis groß: 5~10 Kameras 1080p oder 4K** | Upload (UL) | **EM7565 (Cat 12)** | Der Upload springt auf 150 Mbit/s, die Reserven sind großzügig. |
| **Werbe-Updates auf Digital Signage** | Download (DL) | **EM7565 (Cat 12)** | Bis zu 600 Mbit/s Download: Ein 4K-Werbespot mit ein paar GB ist im Nu geladen. |
| **Das Monster: Multi-4K-Livestream + Werbetafel** | Beide Richtungen schnell | **EM9191 (5G)** | 5G plus die brutale Ausstattung von LTE Cat 20. Wenn das Geld keine Rolle spielt, kauf genau die. |

---

## Warum muss man „Upload“ und „Download“ unterscheiden?

Weil in der 4G/5G-Welt **die Download-Geschwindigkeit meist das 5- bis 6-Fache der Upload-Geschwindigkeit ist!**

Nehmen wir den einfachsten EM7455: Die offizielle Spezifikation nennt 300 Mbit/s Download, aber nur **50 Mbit/s** Upload.
Wenn du voller Begeisterung auf die 300 Mbit/s schaust und beschließt, damit 10 4K-Kameras anzubinden, wirst du garantiert an deinen Zweifeln scheitern. Denn die Kameras brauchen genau die mageren 50 Mbit/s!

| Gerät | Sein Netzwerkverhalten | Auf welchen Wert achten |
|---|---|---|
| **Kamera / NVR** | Sendet ständig Bilder nach außen | **Upload (Uplink, UL)** |
| **Digital Signage** | Lädt fertige Videos herunter und spielt sie ab | **Download (Downlink, DL)** |
| **Interaktiver Kiosk** | Lädt Videos, sendet gelegentlich Klickdaten | **Download zuerst, Upload zweitrangig** |

---

## Rechnen wir: Wie viel Upload brauchen Kameras wirklich?

(Hinweis: Das sind Erfahrungswerte aus der Branche, sie variieren je nach Codec und Bewegungsdynamik im Bild)

- 1 Stream **1080p (H.264)** = etwa **2~6 Mbit/s**
- 1 Stream **4K (H.265)** = etwa **8~16 Mbit/s**

Hast du 6 Kameras 1080p, ergibt das `6 Kameras × 5 Mbit/s = 30 Mbit/s`.
Da wirkt der EM7455 (Upload 50 Mbit/s) gerade so passend? Falsch! **In der Praxis ist das theoretische Limit nie erreichbar.** Mit Signal-Dämpfung gerechnet ist das schon eine sehr angespannte Lage. Empfehlung: Steig direkt auf den EM7565 (Upload 150 Mbit/s) um, dann wird es stabil.

---

## Drei Generationen im Vergleich: EM7455 vs EM7565 vs EM9191

Schauen wir uns die Hardware-Zahlen aus den offiziellen Spezifikationen an:

| Spezifikation | EM7455 (Cat 6) | EM7565 (Cat 12) | EM9191 (5G) |
|---|---|---|---|
| **Download-Limit (DL)** | 300 Mbit/s | 600 Mbit/s | Cat 20 (sehr schnell) |
| **Upload-Limit (UL)** | 50 Mbit/s | 150 Mbit/s | Upload auf Cat-12-Niveau |
| **Anzahl Antennenanschlüsse** | 3 | 3 | 4 (alle anschließen) |
| **Max. Betriebstemperatur** | innen max. 93°C | innen max. 90°C | innen max. 115°C |
| **Spitzenstrom** | 1.5A | 1.5A (Stoß 2.5A) | hoch bis 2.7A (2700 mA) |

---

## Modul in einem Außenkasten? Pass auf, dass es nicht „gar“ wird!

Wenn du diese Module in Kästen für Straßenkameras oder Digital Signage einbaust, achte auf diese zwei Hauptgegner:

### 1. Es „fiebert“
Alle drei Module fürchten Hitze. Der Hersteller empfiehlt, die Temperatur möglichst unter 80°C~100°C zu halten. Im taiwanesischen Sommer wird es in einem Außenkasten locker über 60 Grad heiß. Wenn du kein Kühlpad aufklebst und die Wärme nicht abführst, drosselt das Modul bei Hitze die Geschwindigkeit und hängt am Ende komplett.

### 2. Gib dem Netzteil ausreichend Reserven
Vor allem der 5G-Koloss EM9191 kann beim aktiven Datenverkehr kurzzeitig bis zu **2.7A** ziehen! Wenn dein Netzteil zu knapp dimensioniert ist, bricht die Spannung ein und das Modul startet sich in einer Endlosschleife neu.

---

## Fazit

Eine Netzwerkkarte zu kaufen ist wie einen LKW zu mieten: Je nachdem, wie viel Fracht du transportieren willst, mietest du die passende Größe.

- **Sparsamkeit zuerst**: Wenn du nur 1080p-Kameras (bis 4 Stück) oder eine Werbetafel mit Text und einfachen Bildern betreibst, kauf mit geschlossenen Augen den **EM7455**.
- **Bestes Preis-Leistungs-Verhältnis**: Wenn du viele und hochauflösende Bilder hast oder die Werbetafel oft große Dateien zieht, ist der **EM7565** mit 150 Mbit/s Upload und 600 Mbit/s Download aktuell der Sweet Spot.
- **Kämpfer für die Zukunft**: Nur wenn der Auftraggeber ausdrücklich 5G verlangt oder du mehrere 4K-Streams gleichzeitig live senden musst, denk über das heiße und stromhungrige 5G-Modul **EM9191** nach.

## Wo kaufen (Call To Action)

Planst du eine Lösung für Video-Backhaul oder die Anbindung von Digital Signage? Yupitek bietet das komplette Sortiment an Sierra-Wireless-Modulen und professionelle technische Beratung, damit du die wirtschaftlichste Kombination zusammenstellst!
Schreib uns: **sales@yupitek.com**
Produkte ansehen: [Sierra Wireless](https://yupitek.com/de/products/sierra/)

{{< faq >}}
