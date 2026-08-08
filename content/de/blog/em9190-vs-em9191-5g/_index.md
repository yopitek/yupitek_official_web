---
title: "Sierra EM9190 vs EM9191: 5G Sub-6 oder mmWave, was solltest du wählen? Wir räumen mit Internet-Mythen auf"
description: "EM9190 vs EM9191, was wählen? Laut offizieller Spezifikation (41113174 Rev 8): EM9190 unterstützt 5G Sub-6 + mmWave (n257/258/260/261, nur NSA), EM9191 nur Sub-6. Beide mit Qualcomm SDX55, M.2, inklusive Vergleich der taiwanischen 5G-Bänder. Zusammengestellt von Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em9190", "em9191", "5g", "mmwave", "sub-6", "n78", "m2", "gnss", "wwan"]
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "Was ist der genaue Unterschied zwischen EM9190 und EM9191? Welches Modul unterstützt mmWave?"
    answer: "Laut offizieller Spezifikation (41113174, Rev 8) sind die Fähigkeiten bei Sub-6 (FR1), LTE, 3G und GNSS identisch. Der einzige wesentliche Unterschied ist 5G mmWave (FR2): EM9190 unterstützt LTE+FR2 NSA EN-DC (mit QTM525/QTM527 mmWave-Antennenmodulen, nur NSA-Modus), bei EM9191 steht Not supported. mmWave gibt es also nur beim EM9190."
  - question: "Eignet sich der EM9191 für 5G-Anwendungen in Taiwan?"
    answer: "Ja. Das Kernband des taiwanischen 5G-Netzes ist 3,5 GHz, entsprechend 3GPP n78 (3300–3800 MHz, TDD); EM9190 und EM9191 unterstützen beide n78. Das 28-GHz-Band Taiwans (entspricht n257) ist weniger verbreitet; nur für solche Standorte brauchst du EM9190 plus mmWave-Antennenmodul. Für normale 5G-FWA und Industrierouter reicht der EM9191."
  - question: "Ist mmWave beim Kauf des Moduls EM9190 schon dabei?"
    answer: "Nein. Der EM9190 hat keine eingebauten Antennen: Für mmWave brauchst du zusätzlich 1–4 Qualcomm-mmWave-Antennenmodule QTM525 (niedrige Leistung, EIRP 23 dBm) oder QTM527 (hohe Leistung, EIRP 45 dBm). Jedes Modul wird über zwei MHF7S-IF-Kabel angeschlossen (maximal 8 Kabel) und extern mit 3,8V versorgt; außerdem wird FR2 nur im NSA-Modus unterstützt."
  - question: "Wie groß ist der Unterschied im Stromverbrauch der beiden Module?"
    answer: "Laut Tabelle 3-2 der Spezifikation: Spitzenstrom EM9190 (mit mmWave) 5,0A, EM9190 (ohne mmWave) 3,0A, EM9191 2,7A; Dauerstrom jeweils 4,0A, 2,3A und 2,0A. Für batteriebetriebene oder kühlungsbegrenzte Endgeräte ist der EM9191 beim Stromversorgungsdesign deutlich entspannter."
  - question: "Sind die Mainboard-Designs von EM9190 und EM9191 kompatibel?"
    answer: "Sehr weitgehend: beide als M.2 (WWAN Type 3042-S3-B, 52 mm lang), gleiches 75-pin-Interface, gleiche USB-3.1-Gen2-/PCIe-Gen3-Schnittstellen, gleiche 4× MHF4 Sub-6-Antennenports. Der Unterschied: Der EM9190 hat zusätzlich 8× MHF7S-mmWave-IF-Connectoren und QTM-Steuerpins (pin 40/42/44/46/48, beim EM9191 als NC)."
---


Wenn du an der Uni mit deinem Professor ein 5G-Projekt machst oder gerade in der Firma für die Auswahl des 5G-Moduls zuständig bist, wirst du beim Stöbern im Internet sicher oft diesen Satz lesen: „Der EM9190 ist die günstige Sub-6-Version, der EM9191 ist das Flaggschiff mit mmWave (Millimeterwellen)."

**Falsch! Das ist komplett verdreht!**

Dieser Artikel stützt sich nicht auf Online-Weitererzählungen: Unsere einzige Grundlage ist die offizielle Spezifikation von Sierra Wireless, „EM919X/EM7690 Product Technical Specification" (Doc 41113174, Rev 8, Mai 2023). Wir prüfen die Unterschiede der beiden Module Punkt für Punkt. Besonders schauen wir auf die Bänder n78 und 28 GHz, die taiwanische Leser am meisten interessieren, damit du beim Kauf von 5G-Geräten nichts Falsches kaufst.

> Produktlinks: [EM9190 — Yupitek-Produktseite](/de/products/sierra/em9190/) | [EM9191 — Yupitek-Produktseite](/de/products/sierra/em9191/) | Offizielle Spezifikation: [EM919X/EM7690 Product Technical Specification](https://yupitek.com/docs/sierra/EM919x.pdf)

---

## Mythos widerlegt: Was ist der echte Unterschied zwischen EM9190 und EM9191?

**Kurz gesagt: EM9190 und EM9191 sind Geschwister aus derselben Familie (gleiche Serie, gleicher Basisband-Chip). Beide unterstützen 5G Sub-6, 4G LTE und GNSS-Positionierung. Der einzige Unterschied: Der EM9190 unterstützt zusätzlich 5G mmWave (Millimeterwellen, FR2), der EM9191 nicht.**

Für mmWave musst du nach dem Kauf des EM9190 noch zusätzlich Antennenmodule Qualcomm QTM525 oder QTM527 anschließen (und es läuft nur im NSA-Modus).

| Deine Frage | Die richtige Antwort laut offizieller Spezifikation |
|---|---|
| **Was ist der Unterschied zwischen den beiden Karten?** | Nur mmWave (FR2). In der Spezifikation des EM9190 steht „LTE+FR2 NSA EN-DC Supported"; beim EM9191 steht „Not supported". Alles andere, Sub-6-Bänder, LTE usw., ist komplett identisch. |
| **Hat der EM9190 mmWave?** | Ja. Aber das bedeutet nicht, dass du mmWave einfach mit dem Kauf der Karte bekommst: Du musst extern Qualcomm-mmWave-Antennenmodule anschließen (maximal 4 Stück), unterstützt werden n257/n258/n260/n261, und es läuft nur im NSA-Modus (nicht autonomes Netz). |
| **Hat der EM9191 mmWave?** | Nein. In der offiziellen Tabelle 1-1 steht klar „Not supported", und alle mmWave-bezogenen Signalpins auf der Platine sind NC (nicht verbunden). |
| **Welches Modul kaufst du für ein 5G-Projekt in Taiwan?** | Taiwanisches 5G läuft meist auf 3,5 GHz (n78), das beide Module unterstützen; 28 GHz (entspricht n257) ist in Taiwan seltener. Nur wenn du genau dazu experimentierst, brauchst du den EM9190 plus mmWave-Antennen. |
| **Welches Modul passt zu wem?** | **EM9190**: US-/JP-Markt, Labortests für Millimeterwellen, Outdoor-CPE mit extrem großer Bandbreite.<br>**EM9191**: Projekte in Taiwan oder Asien mit Sub-6, wenn das Modul wenig Strom verbrauchen soll und das Budget begrenzt ist. |

> **Noch einmal deutlich**: Glaub bitte nicht mehr der Online-Aussage, dass „der EM9191 das mmWave-Flaggschiff ist". In der offiziellen Spezifikation steht schwarz auf weiß, dass **nur der EM9190 mmWave-Fähigkeit hat**. Ein Fehlkauf wäre peinlich.

---

## Geschwister aus einer Familie: Wie unterscheidest du EM9190 / EM9191 / EM7690?

Eigentlich gibt es in der EM91-Familie drei Brüder. Laut Spezifikation:

- **EM9190**: Vollausstattung (LTE + 5G Sub-6 + 5G mmWave)
- **EM9191**: praktisches Standardmodell (LTE + 5G Sub-6, ohne mmWave)
- **EM7690**: abgespeckte Version (nur LTE, kein 5G)

In diesem Artikel vergleichen wir hauptsächlich die ersten beiden 5G-Brüder; EM7690 erwähnen wir nur, damit du weißt, dass es ihn gibt.

---

## Harte Spezifikationsvergleichstabelle (aus der offiziellen 41113174 Rev 8)

Alle Zahlen unten stammen aus der offiziellen Spezifikation. Wenn du Ingenieur bist, schau direkt auf diese Tabelle:

| Punkt | EM9190 | EM9191 | Quelle |
|---|---|---|---|
| **5G NR Sub-6 (FR1)** | ✓ | ✓ | Table 1-2 |
| **5G NR mmWave (FR2)** | ✓ (nur NSA-Modus, externes Antennenmodul nötig) | ✗ | Table 1-1 |
| **FR2-Millimeterwellen-Bänder** | n257 / n258 / n260 / n261 | — | Table 1-2 |
| **FR1-Sub-6-Bänder** | n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n38/n40/n41/n48/n66/n71/n77/n78/n79 | bei beiden identisch | Table 4-4 |
| **Kern-Basisband-Chip** | Qualcomm SDX55 | Qualcomm SDX55 | Figure 3-1 |
| **Zellularstandard** | 5G 3GPP Release 15; LTE Release 15 | bei beiden identisch | Table 2-1 |
| **Formfaktor** | M.2 (WWAN Type 3042-S3-B, 52 mm lang) | bei beiden identisch | §1.2 |
| **Computer-/Mainboard-Interface** | USB 3.1 Gen2, PCIe Gen3 Single-Lane | bei beiden identisch | §1.3 |
| **Sub-6-Antennenports** | 4× MHF4 (MAIN/MIMO1/MIMO2/AUX) | bei beiden identisch | §4.1 |
| **mmWave-Antennenports** | 8× MHF7S (maximal 4 externe Antennenmodule) | keine | §4.1 |
| **Maximaler Momentanverbrauch (Peak)** | 5,0A (mit mmWave) / 3,0A (ohne) | 2,7A | Table 3-2 |
| **Betriebstemperatur** | -30°C bis +70°C (Klasse A); -40°C bis +85°C (Klasse B, mit Leistungsabfall) | bei beiden identisch | Table 7-1 |
| **Positionierung (GNSS)** | L1 (GPS/GLONASS usw.) + L5 (optional) | bei beiden identisch | Table 4-13 |

> **Kleiner Hinweis**: Diese Spezifikation stammt aus Mai 2023. Einige Bänder (wie n7, n8, n20 usw.) können sich je nach Firmware oder geliefertem SKU unterscheiden. Bevor du für ein echtes Projekt bestellst, fordere bei uns die aktuellen offiziellen Dokumente an und vergleiche.

---

## mmWave gibt es nicht einfach mit dem Modul: die versteckten Kosten des EM9190

Viele Studierende und Maker denken, man kauft den EM9190 und kann sofort Millimeterwellen testen. Das ist ein großer Irrtum.

In der Spezifikation steht es klar: „**Der EM9190 unterstützt 5G mmWave nur in Kombination mit optionalen Qualcomm-mmWave-Antennenmodulen.**" Außerdem wird nur der NSA-Modus (nicht autonomes Netz) unterstützt, du brauchst also zwingend ein 4G-LTE-Signal als Anker (Anchor).

### Wie konfigurierst du die Millimeterwellen-Antennen?

Du musst Qualcomm-Antennenmodule QTM525 (Low-Power-Version) oder QTM527 (High-Power-Version) kaufen. Verschiedene Antennenmodule unterstützen zudem verschiedene Bänder (siehe offizielle Tabelle 4-2):

- Wenn dein Labor **n257** testen will (das 28-GHz-Band in Taiwan), musst du QTM525-2, QTM525-5 oder QTM527-2 kaufen; wenn du QTM527-1 kaufst, gibt es kein n257!

**Falle für Ingenieure**:
Wenn du den EM9190 als Outdoor-5G-Empfänger (CPE) einsetzen willst, musst du vielleicht alle 4 High-Power-Antennen QTM527 montieren. Das bedeutet: 8 teure MHF7S-Kabel verlegen, eine separate 3,8V-Stromversorgung für diese Antennen designen und eine starke Kühlung einplanen. Diese Entwicklungskosten sind oft deutlich höher als der Preis der Karte selbst!

---

## Wenn du in Taiwan 5G machst, reicht eigentlich der EM9191

**Denn die Hauptfrequenz des taiwanischen 5G ist 3,5 GHz (also n78 in der 3GPP-Sprache), und sowohl EM9190 als auch EM9191 unterstützen n78 perfekt.**

Wenn dein Projekt einfach nur 5G in Taiwan nutzen will oder du Industrierouter für normale Kunden baust:

- Beide Module unterstützen das taiwanische 5G n78 (3300–3800 MHz).
- Beide Module unterstützen die bestehenden taiwanischen 4G-Bänder (als NSA-Anker kein Problem).

**Warum empfehlen wir dir den Kauf des EM9191?**
Weil du, wenn du keine Millimeterwellen brauchst, kein Geld für den EM9190 ausgeben solltest. Außerdem hat der EM9191 keine mmWave-Hardware, sein Spitzenstrom liegt nur bei 2,7A und ist damit deutlich entspannter als beim EM9190 (siehe nächster Abschnitt), und die Stromversorgung der Platine wird viel weniger belastet.

---

## Stromverbrauch im Vergleich: versaue das Stromversorgungsdesign nicht

Wer Hardware baut, weiß: Wenn das Netzteil nicht liefert, startet das Gerät neu. Nach den Daten der offiziellen Tabelle 3-2:

| Verbrauchsparameter | EM9190 (mit mmWave) | EM9190 (ohne mmWave) | EM9191 |
|---|---|---|---|
| Spitzen-Momentanstrom | 5,0A | 3,0A | 2,7A |
| Dauerstrom | 4,0A | 2,3A | 2,0A |

Alle Module laufen mit 3.135V bis 4.4V (üblicherweise für 3.3V ausgelegt). Du siehst: Wenn der EM9190 mmWave einschaltet, schießt der Momentanstrom auf 5,0A! Das ist eine große Herausforderung für batteriebetriebene oder kleine Geräte. Wenn du nur 5G Sub-6 fahren willst, musst du beim EM9191 nur den Peak von 2,7A bewältigen, das Stromversorgungsdesign wird deutlich einfacher.

---

## Pin-Design der Platine: kann man ein Design für beide teilen?

**Das Sub-6-Design kann geteilt werden.**

Beide Module sind im M.2-Formfaktor (52 mm lang, etwas länger als die üblichen 42 mm bei Notebooks, achte auf den mechanischen Platz) und haben denselben 75-pin-Interface.

Der einzige Unterschied: Um die vielen mmWave-Antennen anzusteuern, nutzt der EM9190 einige ursprünglich freie Pins (zum Beispiel QTM_PON auf pin 40/42/44/46 und die 1.9V-Versorgung auf pin 48). Beim EM9191 sind diese Pins leer (NC).
Du kannst also problemlos zuerst eine universelle Platine für den EM9191 designen und, falls du eines Tages wirklich Millimeterwellen brauchst, einfach die zusätzlichen Steuerleitungen für den EM9190 ergänzen.

---

## Fazit: Welches Modul solltest du kaufen?

| Deine Anforderungen | Nimm den EM9190 | Nimm den EM9191 |
|---|---|---|
| Du musst mmWave-Bänder wie 28 GHz testen | ✅ Nur er (denk an den Antennen-Zusatzkauf) | ❌ Nicht unterstützt |
| Projekt in Taiwan, nur 5G Sub-6 (n78) | Geht (aber etwas verschwenderisch) | ✅ Empfohlen, spart Geld und Strom |
| Stromversorgung der Platine schafft keinen großen Strom | ⚠️ Peak kann 5,0A erreichen | ✅ Peak 2,7A ist leichter zu schaffen |

**Leitfaden gegen Fehlkäufe**:

1. Verwechsle es nicht mehr: Nur der EM9190 hat mmWave.
2. Der Kauf des EM9190 bedeutet nicht, dass mmWave schon da ist: Du brauchst zusätzlich spezielle Antennen und Kabel.
3. Viele Bänder (wie n7, n8, n28) unterliegen Firmware-Versionen und Regionsbeschränkungen. Frag vor dem Kauf unbedingt beim Lieferanten nach, ob dein SKU diese Bänder freischalten kann.

---

## Schnelles Q&A zu häufigen Fragen

{{< faq >}}

---

## Kaufbedarf oder Fragen? Sprich uns an

Wenn du nach diesem Artikel noch Fragen zur Hardware-Integration hast oder euer Labor/eure Firma diese beiden 5G-Module einkaufen will, kontaktiere gerne das Engineering-Team von Yupitek. Wir bieten auch passende Antennen und Adapterplatinen an.

- **EM9190-Produktseite (das echte Flaggschiff mit mmWave)** : [https://yupitek.com/de/products/sierra/em9190/](/de/products/sierra/em9190/)
- **EM9191-Produktseite (die praktische Sub-6-Version)** : [https://yupitek.com/de/products/sierra/em9191/](/de/products/sierra/em9191/)
- **Alle Sierra-Modelle** : [https://yupitek.com/de/products/sierra/](/de/products/sierra/)
- **Kontakt-E-Mail** : sales@yupitek.com
