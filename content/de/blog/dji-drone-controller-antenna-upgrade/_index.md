---
title: "DJI-Drohnencontroller-Antennen-Upgrade: Reichweite mit ALFA-Antennen erweitern (2026 überarbeitete Ausgabe)"
description: "Der komplette Leitfaden zum Antennen-Upgrade für DJI-Controller – welche Modelle du direkt mit ALFA-Antennen verschrauben kannst, welche eine Gehäuseöffnung erfordern, kompatible Modelle im Vergleich, Installationsschritte und rechtliche Hinweise."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-08-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["DJI", "drone", "antenna-upgrade", "RP-SMA", "IPEX4", "range-extension", "ALFA-APA-M25", "ALFA-APA-M25-6E", "ALFA-ARS-25-57A", "ALFA-ARS-NT5B7"]
featureimage: "/images/blog/dji-drone-controller-antenna-upgrade.webp"
faq:
  - question: "Erlöscht die DJI-Garantie, wenn ich die Antennen tausche?"
    answer: "Bei Modellen mit externem RP-SMA-Anschluss wie dem RC-N1 gelten die externen Antennen als vom Nutzer wartbare Teile – der Tausch selbst beeinträchtigt die Garantie kaum. Bei RC2, RC Pro und Smart Controller erlischt die Garantie dagegen sofort, sobald du das Gehäuse für den Umbau öffnest. Heb die Originalantennen auf, um sie bei einem Reparaturservice wieder anzubauen."
  - question: "Mein Controller hat keinen sichtbaren Gewindeanschluss – kann ich trotzdem upgraden?"
    answer: "Ja, aber nur über eine Gehäuseöffnung plus Adapterkabel. Modelle wie RC2, RC Pro und Smart Controller haben intern IPEX/IPEX4-Mikrokoaxialstecker statt externer RP-SMA-Buchsen. Der Umbau erfordert DIY-/RF-Erfahrung, kostet die Garantie und erfordert möglicherweise eine irreversible Bohrung im Gehäuse."
  - question: "Kann ich diese ALFA-Antennen auch für Nicht-DJI-FPV-Systeme nutzen?"
    answer: "Ja – jedes RP-SMA-kompatible System auf 2,4 GHz oder 5,8 GHz funktioniert damit, zum Beispiel ExpressLRS (ELRS) auf 2,4 GHz oder 5,8-GHz-Videosender (VTX) mit RP-SMA-Anschluss. Achtung: FrSky R9 und TBS Crossfire arbeiten auf 915 MHz und brauchen eine 900-MHz-Antenne. Achte darauf, dass Anschlusstyp und Frequenzband passen."
  - question: "Was bringt es, beim RC-N1 nur eine statt beide Antennen zu tauschen?"
    answer: "Das DJI-OcuSync-System nutzt beide Antennen für den Diversity-/MIMO-Empfang und wählt laufend die Antenne mit dem stärkeren Signal. Nur eine Antenne zu tauschen erzeugt ein asymmetrisches Setup; die beste Leistung erreichst du mit zwei gleichwertigen Antennen. Tausch also am besten beide."
  - question: "Muss ich nach dem Upgrade Einstellungen in der DJI-App ändern?"
    answer: "Nein. Der DJI-Controller verwaltet Antennenauswahl und Frequenzbandwahl automatisch – nach einem rein physischen Antennentausch sind keine App-Konfigurationsänderungen nötig."
  - question: "APA-M25 oder ARS-25-57A – wie entscheide ich mich?"
    answer: "Zeigt dein Controller während des Flugs meist stabil in eine Richtung, nimm die APA-M25 (Richtantennenplatine, höchster Gewinn). Kreisest du oft um die Drohne oder willst dich nicht um die Ausrichtung kümmern, nimm die ARS-25-57A (omnidirektionale Paddelantenne, ohne Ausrichtung)."
---

{{< tldr >}}
Nicht alle DJI-Controller lassen sich ohne Gehäuseöffnung mit neuen Antennen aufrüsten. **Nur der RC-N1** besitzt einen externen RP-SMA-Buchsenanschluss, an dem du ALFA-Antennen direkt von Hand festschrauben kannst. Bei **RC2, RC Pro und Smart Controller** – den Modellen mit Display – sind die Antennen fest verbaut und nur im Winkel verstellbar; intern kommen IPEX-Mikrokoaxialstecker zum Einsatz. Für externe Hochgewinnantennen musst du dort das Gehäuse öffnen und Adapterkabel einbauen – das erlischt die Garantie. Dieser Artikel erklärt beide Szenarien und welche ALFA-Antenne für dich am besten geeignet ist.
{{< /tldr >}}

---

## DJI-Controller-Antennen verstehen

### Leistung der Originalantennen

Die meisten DJI-Standardantennen sind **omnidirektionale Gummistab-Dipolantennen** mit etwa **2 dBi** Gewinn. Die Antennen sind auf kompakte Größe und breite Abdeckung optimiert – nicht auf maximale Reichweite in eine einzelne Richtung. Für kurze Freizeitflüge reicht das völlig aus. Wenn du aber oft am Rand des legalen Flugbereichs unterwegs bist, gibt es bei der RF-Signalreserve noch Luft nach oben.

### Frequenzbänder

Die **OcuSync-3- (O3)** und **O4**-Übertragungssysteme von DJI decken folgende Bänder ab:

- **2,4 GHz** – dringt besser durch Hindernisse, geeignet für Umgebungen mit viel RF-Störungen
- **5,1 / 5,8 GHz** – höherer Durchsatz, geringere Latenz, ideal für offenes Gelände

Dual- und Tri-Band-Controller aktivieren mehrere Bänder gleichzeitig; das System wählt automatisch den saubersten Kanal.

### Anschlusstypen: zwei völlig unterschiedliche Designs

Das ist der Kernpunkt dieser überarbeiteten Ausgabe. Die Antennendesigns der DJI-Controller lassen sich in zwei Generationen mit zwei völlig unterschiedlichen Architekturen einteilen:

**① Externes RP-SMA (direkt anschraubbar)**
Ältere Modelle ohne Display (z. B. **RC-N1**) verwenden das klassische Design: An der Antennenwurzel sitzt ein sichtbarer Rändel-Gewindering, die Buchse ist **RP-SMA Female** – die passende Antenne braucht also einen **RP-SMA-Stecker (Male)**. Genau diese Ausführung liefern die ALFA-Zubehörantennen. Bei diesen Modellen kannst du die Originalantenne ohne Werkzeug abschrauben und die ALFA-Antenne direkt von Hand aufschrauben.

**② Interner Mikrokoaxialstecker (Gehäuseöffnung für Umbau nötig)**
Die neueren Modelle mit Display – **RC2, RC Pro, Smart Controller** – zeigen außen zwar weiterhin zwei Antennen, aber diese sind **fest verbaut und nur im Winkel verstellbar**, nicht abschraubbar. Öffnest du das Gehäuse, siehst du: Im Inneren kommen **IPEX-, IPEX4-** oder ähnliche Mikrokoaxialstecker zum Einsatz, die direkt auf der Hauptplatine verlötet sind. Das Gehäuse hat keine Gewindeöffnung vorgesehen, die der Nutzer aufschrauben könnte.

> **Hintergrundwissen:** In Community-Diskussionen gibt es eine interessante These: Der RP-SMA-Standard wurde unter anderem als Reaktion auf die US-amerikanische FCC-Beschränkung „nicht abnehmbare Antennen" entwickelt. Mit anderen Worten: DJI hat bei den Controllern mit Display bewusst auf interne Mikrokoaxialstecker statt externer RP-SMA-Buchsen gesetzt – vermutlich nicht nur wegen Wasserschutz oder Optik, sondern **weil das Design Nutzer davon abhalten soll, die Antennen selbst zu tauschen**. Das erklärt auch, warum die Antennen neuerer Modelle immer „nicht abnehmbarer" werden.

**So erkennst du den Typ:** Schau auf die Antennenwurzel oben am Controller – gibt es einen deutlich sichtbaren Sechskant- oder Rändel-Gewindering aus Metall und lässt sich die Antenne von Hand losschrauben, handelt es sich um externes RP-SMA. Lässt sich die Antenne nur seitlich kippen und ist das Gehäuse durchgehend nahtlos, ist sie intern verbaut – ein Umbau erfordert dann das Öffnen des Gehäuses.

---

## Warum Antennenplatinen die Reichweite erhöhen

### Richtantenne vs. Rundstrahlantenne

Das RF-Abstrahlmuster einer Standard-Gummistabantenne ist annähernd kugelförmig – horizontal 360°, vertikal etwa halbkugelförmig. Das ist ideal, wenn du nicht weißt, wo sich das Ziel befindet. Aber die Drohne fliegt die meiste Zeit vor dir – so verschwendet dieses Abstrahlmuster eine Menge Energie.

Eine **Antennenplatine (Patch-Antenne)** bündelt die RF-Energie in einem kegelförmigen Bereich nach vorne. Energie, die sonst nach hinten, zur Seite oder zum Boden abstrahlt, wird nach vorne umgelenkt – ohne höhere Sendeleistung steigt die effektive Signalstärke in Flugrichtung.

### Gewinnberechnung

Am Beispiel der **ALFA APA-M25**:

- **8 dBi** @ 2,4 GHz
- **10 dBi** @ 5,8 GHz

Gegenüber der 2-dBi-Originalantenne liefert die 10-dBi-Antennenplatine in Vorwärtsrichtung etwa **8 dB** mehr Gewinn:

> Mit jedem 3 dB Gewinn verdoppelt sich die effektive Strahlungsleistung in diese Richtung.
> 8 dB Verbesserung ≈ etwa **6-fach** stärkeres Signal in Vorwärtsrichtung.

### Freiraum-Pfadverlust

Bei 5,8 GHz beträgt der Freiraum-Pfadverlust über 1 km Entfernung etwa **113 dB**. Die 10-dBi-Antennenplatine holt 8 dB aus dem Link-Budget zurück und verschiebt den Punkt, an dem der Link unter die minimale Empfangsempfindlichkeit fällt, deutlich nach hinten.

### Kompromisse

Eine Richtantenne muss **in Richtung der Drohne zeigen**. Bei den meisten Sichtflügen ergibt sich das ganz natürlich aus der Haltung des Controllers. Die Strahlbreite der APA-M25 liegt bei etwa 60–70° – genug für typische Flugbögen, ohne ständig neu ausrichten zu müssen.

> **Tipp:** Wenn dein Flugstil viele Rundflüge erfordert (Kreisen um den Piloten, Nahdurchflüge), sind Rundstrahlantennen (z. B. ARS-25-57A, ARS-NT5B7) besser geeignet als Antennenplatinen – ganz ohne ständiges Nachjustieren.

---

## Kompatible ALFA-Antennenmodelle

Alle vier Modelle haben einen **RP-SMA-Stecker (Male)** und unterstützen die von DJI O3/O4 genutzten Frequenzbänder:

### APA-M25 – Dualband 2,4/5 GHz (beste Wahl)

Die erste Wahl der meisten DJI-O3/O4-Piloten: Die Dualband-Abdeckung passt perfekt zu den von DJI genutzten Bändern, und das Verhältnis aus Größe und Leistung eignet sich ideal für den Feldeinsatz.

| Eigenschaft | Spezifikation |
|---|---|
| Gewinn | 8 dBi @ 2,4 GHz / 10 dBi @ 5 GHz |
| Strahlbreite | horizontal 66° / vertikal 16° |
| Abmessungen | 167,3 × 66 × 18 mm |
| Gewicht | 72 g |
| Anschluss | RP-SMA Male |

Mit 72 g verursacht die Antenne auch bei langen Flügen keine spürbare Ermüdung; die Platine liegt flach auf der Oberseite der meisten DJI-Controller auf. Wenn dein Modell **zwei abnehmbare Antennen hat (RC-N1)**, erzielst du mit zwei APA-M25 das beste Ergebnis.

👉 [Produktseite von APA-M25 ansehen](/de/products/alfa/apa-m25/)

### APA-M25-6E – Tri-Band inklusive 6 GHz (zukunftssicher)

Ergänzt die Dualband-Abdeckung der APA-M25 um **6 GHz**.

| Eigenschaft | Spezifikation |
|---|---|
| Gewinn | 8 dBi @ 2,4 GHz / 10 dBi @ 5 GHz / **9 dBi @ 6 GHz** |
| Strahlbreite | horizontal 60° / vertikal ca. 40–45° (je nach Charge leicht abweichend – maßgeblich ist die Angabe auf der Verpackung) |
| Abmessungen/Gewicht | wie APA-M25, 167,3 × 66 × 18 mm, 72 g |
| Anschluss | RP-SMA Male |

**Aktuelle Relevanz für DJI:** Derzeit nutzt keine DJI-Drohne für Endverbraucher 6 GHz als primären Steuer-/Videolink. Diese Antenne lohnt sich, wenn du sie auch für Wi-Fi-6E-Access-Points oder WLAN-Adapter nutzt, wenn du künftige DJI-Systeme mit 6-GHz-Spektrum erwartest oder eine 6-GHz-FPV-Ausrüstung betreibst. Nutzt du sie ausschließlich am DJI-Controller, bietet die Standard-APA-M25 dieselbe praktische Leistung zum geringeren Preis.

👉 [Produktseite von APA-M25-6E ansehen](/de/products/alfa/apa-m25-6e/)

### ARS-25-57A – Dualband-Paddelantenne (Alltags-Upgrade ohne Ausrichtung)

Bessere Leistung als die Gummistabantenne, ohne die Ausrichtungs-Disziplin einer Antennenplatine – der **einfachste Upgrade-Weg**: Originalantenne abschrauben, ARS-25-57A aufschrauben, abheben. Kein Nachjustieren nötig.

| Eigenschaft | Spezifikation |
|---|---|
| Gewinn | 5 dBi @ 2,4 GHz / 7 dBi @ 5 GHz |
| Abstrahlmuster | omnidirektional |
| Abmessungen | 18,5 × 231 mm |
| VSWR | 2,5:1 |
| Betriebstemperatur | −10 °C bis +55 °C |
| Anschluss | RP-SMA Male |

Gegenüber der Originalantenne bringt sie je nach Band eine messbare Verbesserung der Link-Qualität von 3–5 dB – ohne den Aufwand, die Antennenrichtung im Flug zu managen. Ideal für alle, die das Upgrade in einem Schritt erledigen wollen und sich im Flug nicht um die Antennenausrichtung kümmern möchten.

👉 [Produktseite von ARS-25-57A ansehen](/de/products/alfa/ars-25-57a/)

### ARS-NT5B7 – Tri-Band-Dipolantenne (für den Dauereinsatz)

Industrielle omnidirektionale Dipolantenne, die drei moderne WLAN-Bänder abdeckt – leichter und kompakter als eine Antennenplatine.

| Eigenschaft | Spezifikation |
|---|---|
| Gewinn | 4 dBi @ 2,4 GHz / 5 dBi @ 5 GHz / 7 dBi @ 6 GHz |
| Abmessungen/Gewicht | ⌀13 × 196 mm, 20 g |
| Betriebstemperatur | **−40 °C bis +85 °C** (Industriequalität) |
| Anschluss | RP-SMA Male |

Die industrielle Temperaturspezifikation eignet sich für Flüge unter extremen Wetterbedingungen – Bergregionen im Winter, Wüstengebiete im Sommer. Anders als die APA-M25 mit ihrem höheren Vorwärtsgewinn behält die ARS-NT5B7 ein vollständig omnidirektionales Abstrahlmuster – ideal für Situationen, in denen du den Controller nicht präzise ausrichten kannst (Fahrzeugmontage, Stativ, Betrieb durch mehrere Personen). Die schlanke Form bietet im Wind außerdem weniger Luftwiderstand beim Fliegen aus der Hand.

👉 [Produktseite von ARS-NT5B7 ansehen](/de/products/alfa/ars-nt5b7/)

> **Hinweis:** Wir führen auch die Singleband-**APA-M04** (7 dBi @ 2,4 GHz) im Sortiment. Da sie nur 2,4 GHz unterstützt, empfehlen wir sie nicht für DJI-Dual-/Tri-Band-Systeme – deshalb fehlt sie in dieser Empfehlungsliste.

---

## Anschluss-Kompatibilitätsleitfaden

### RP-SMA vs. SMA: der entscheidende Unterschied

Die beiden Anschlüsse sehen fast identisch aus, sind physikalisch und elektrisch aber völlig inkompatibel:

| Merkmal | Standard-SMA | RP-SMA (Reverse-Polarity-SMA) |
|---|---|---|
| Stecker-Mitte | Stift (massiv) | Buchse (Loch) |
| Buchsen-Mitte | Buchse (Loch) | Stift (massiv) |
| Einsatzgebiet | Militär-/Industrie-RF | Consumer-WLAN, DJI RC-N1 u. a. |
| ALFA-Antennen | ❌ nicht verwendet | ✅ alle ALFA-Zubehörantennen |

Der RC-N1 verwendet eine **RP-SMA-Female-Buchse**, die ALFA-Zubehörantennen einen **RP-SMA-Male-Stecker** – die beiden passen direkt zusammen, einfach von Hand festschrauben. **Verwende niemals Standard-SMA-Antennen an einer RP-SMA-Buchse**: Stift und Buchse sind in der Mitte vertauscht, und ein erzwungenes Verbinden kann den Mittelstift verbiegen oder abbrechen – ein irreparabler Schaden.

### Verlängerungskabel

Wenn du die Antennen auf einem Stativ oder einer Bodenstation montieren und den Controller getrennt bedienen möchtest, eignen sich RP-SMA-Verlängerungskabel:

- **RG-316** – verlustarmes Koaxialkabel, flexibel, ideal für den Feldeinsatz bis 50 cm
- **RG-174** – auf kurzen Distanzen etwas geringere Verluste als RG-316, sehr flexibel
- Vermeide generische RG-58-Kabel – bei 5,8 GHz sind die Verluste hoch und fressen den Antennengewinn wieder auf

Ein 30-cm-RG-316-Kabel kostet in der Regel weniger als 1 dB Verlust – für die meisten Setups akzeptabel.

---

## Kompatibilitätsreferenztabelle für Controller

| DJI-Controller-Modell | Frequenzbänder | Externes Antennendesign | Interner Anschluss | ALFA-Antenne ohne Gehäuseöffnung? |
|---|---|---|---|---|
| **RC-N1** | 2,4 / 5,8 GHz | abnehmbare Gewindeantenne | RP-SMA Female (extern) | ✅ **Ja**, von Hand festschrauben |
| **RC2** (Air 3 / Air 3S / Mini 4 Pro) | 2,4 / 5,1 / 5,8 GHz | fest, Winkel verstellbar | IPEX4 (intern) | ❌ Nein, Gehäuseöffnung + Adapterkabel + Bohrung nötig |
| **RC Pro** | 2,4 / 5,8 GHz | fest, Winkel verstellbar | interner Mikrostecker (je nach Modell IPEX4 oder ähnlich) | ❌ Nein, Gehäuseöffnung + Adapterkabel nötig |
| **Smart Controller** | 2,4 / 5,8 GHz | fest | IPEX (intern) | ❌ Nein, Gehäuseöffnung + Adapterkabel nötig |
| DJI Goggles 2 | 2,4 / 5,8 GHz | je nach Modell | je nach Modell | bitte einzeln prüfen, nicht in dieser Tabelle abgedeckt |

**Tipp:** Wenn du nicht sicher bist, zu welcher Kategorie dein Controller gehört, schau auf die Antennenwurzel – ein deutlich sichtbarer Rändel-Gewindering, der sich von Hand lösen lässt, bedeutet externes RP-SMA wie beim RC-N1. Lässt sich die Antenne nur kippen und ist das Gehäuse nahtlos, ist sie intern verbaut und erfordert eine Gehäuseöffnung. **Versuche niemals, eine fest verbaute Antenne zu drehen – das kann die Antennenwurzel und die Controller-Buchse beschädigen. Prüfe zuerst dein Modell.**

---

## Reichweitentestergebnisse (realistische Erwartungen)

Die folgenden Werte sind typische Feldbeobachtungen bei freier Sichtlinie. Die tatsächlichen Ergebnisse variieren stark mit lokalen RF-Störungen, Gelände, Wetterbedingungen und dem Drohnenmodell.

| Setup | Typische effektive Reichweite | Anmerkungen |
|---|---|---|
| Original-DJI-Antennen (beide) | 1,5 – 3 km | freie Sichtlinie, wenig Störungen |
| RC-N1 + APA-M25 (eine) + Original | 2,5 – 4 km | Controller in Richtung Drohne gehalten |
| RC-N1 + APA-M25 (beide getauscht) | 4 – 7 km | beide Platinen in Richtung Drohne |
| RC-N1 + ARS-25-57A (beide getauscht) | 2 – 4,5 km | omnidirektional, keine Ausrichtung nötig |
| RC-N1 + ARS-NT5B7 (beide getauscht) | 2 – 4 km | industriell omnidirektional, ähnliches Abstrahlmuster |
| RC2/Smart Controller mit Gehäuseöffnung + externe Hochgewinnantenne | laut Community-Messungen ähnlicher Aufbauten ca. 30–50 % mehr als Original (z. B. 3 km → 4 km) | Gehäuseöffnung und Bohrung nötig; Ergebnis hängt stark von Umbauqualität und Umgebung ab, Werte nur als Richtwert |

**Rechtlicher Reichweiten-Hinweis:** Eine verlängerte Antennenreichweite erlaubt dir nicht, außerhalb der gesetzlichen Grenzen irgendeines Landes zu fliegen. In den meisten Rechtsräumen – Taiwan, EU, USA, Japan, Australien – gilt für Freizeit- und Gewerbeflüge, dass die Drohne während des gesamten Flugs in **Sichtweite (VLOS)** bleiben muss. Die technischen Reichweitenwerte oben können deinen legalen Betriebsbereich weit überschreiten. Der eigentliche Wert eines Antennen-Upgrades liegt in der verbesserten **Zuverlässigkeit und Signalreserve** innerhalb der legalen Sichtweite – nicht darin, die Sichtweite zu durchbrechen.

---

## Rechtliche und regulatorische Hinweise

**Wichtig:** Eine erweiterte RF-Reichweite des Controllers ist keine Erlaubnis, über die gesetzlichen Grenzen hinaus zu fliegen. In den meisten Ländern ist Fliegen außerhalb der Sichtweite (BVLOS) ohne spezielle Genehmigung illegal und wird hart bestraft.

### VLOS-Anforderungen (Sichtflug)

| Rechtsraum | Standard-Limit | BVLOS-Genehmigung |
|---|---|---|
| Taiwan (CAA) | Sichtweite muss eingehalten werden | Ausnahme/Genehmigung erforderlich |
| USA (FAA Part 107) | Sichtweite muss eingehalten werden | BVLOS-Ausnahme erforderlich |
| EU (EASA) | Sichtweite muss eingehalten werden | spezielle Betriebsgenehmigung erforderlich |
| Japan (MLIT) | Sichtweite muss eingehalten werden | Level-4-Zertifizierung erforderlich |

### Auswirkungen auf die Typgenehmigung

Der Austausch der externen Antennen kann den **CE-, FCC- oder lokalen Typgenehmigungsstatus** des Controllers beeinflussen. Der Controller wurde mit den Originalantennen typgenehmigt; eine Antenne mit höherem Gewinn kann dazu führen, dass das System die für das Band zertifizierte äquivalente isotrope Strahlungsleistung (EIRP) überschreitet.

- Taiwan: Funkgeräte, die die EIRP-Grenzwerte der NCC (National Communications Commission) überschreiten, verstoßen gegen das Telekommunikationsverwaltungsgesetz.
- USA: FCC Part 15 begrenzt die EIRP nicht lizenzierter Geräte.
- **ALFA-Antennen werden als Zubehör-Ersatzteile verkauft** – Installation, Konformitätsprüfung und rechtliche Verantwortung liegen beim Endnutzer.
- Bei Modellen mit Gehäuseöffnung (RC2/RC Pro/Smart Controller) kommen zusätzlich **Garantieverlust** und **irreversible Bohrungen im Gehäuse** dazu – überlege dir das vorher gut.

**Praktisch erklärt:** Bei den meisten DJI-Controllern, die innerhalb ihres EIRP-Budgets arbeiten, ändert der Tausch der 2-dBi-Originalantenne gegen eine ALFA-Hochgewinnantenne den Antennengewinn – die Sendeleistung des Controllers bleibt aber unverändert. Ob die resultierende EIRP deine lokalen Grenzwerte überschreitet, hängt von der ursprünglich zertifizierten Ausgangsleistung deines Controller-Modells ab. Schau in die Regulierungsdokumente deines DJI-Controllers, um den zertifizierten EIRP-Wert zu finden.

---

## Installationsschritte

Je nach Modell unterscheidet sich die Installation stark. Prüfe zuerst in der „Kompatibilitätsreferenztabelle für Controller" oben, zu welcher Kategorie dein Modell gehört, und folge dann dem passenden Abschnitt.

### A. RC-N1 (externes RP-SMA, ohne Gehäuseöffnung)

**Was du brauchst:** eine ALFA-Antenne mit RP-SMA-Male-Stecker und deinen DJI-Controller.

1. **Schalte den Controller aus** – bevor du irgendeine Antennenverbindung löst, muss das Gerät aus sein.
2. **Greife die Originalantenne am Ansatz nahe dem Controller-Gehäuse** – nicht am Antennenschaft.
3. **Drehe gegen den Uhrzeigersinn**, um die Antenne abzuschrauben – nach 3–4 Umdrehungen sollte sie sich lösen.
4. **Prüfe die RP-SMA-Female-Buchse** auf Schmutz oder verbogene Stifte.
5. Schraube den **RP-SMA-Male-Stecker der ALFA-Antenne** von Hand im Uhrzeigersinn in die Buchse.
6. **Ziehe handfest an** – fester Sitz, aber kein Werkzeug und kein Überdrehen. SMA/RP-SMA-Anschlüsse sind nur für Handfestigkeit ausgelegt.
7. Hat dein Controller zwei Buchsen, **wiederhole die Schritte für die zweite Antenne**.
8. **Heb die Originalantennen gut auf** – für einen Reparaturservice musst du sie wieder anbauen.
9. Schalte ein und teste auf einem sicheren, freien Gelände Signalstärke und Flugverhalten.

**Antennenausrichtung:**
- Antennenplatine (APA-M25/APA-M25-6E): Die Vorderseite zeigt zum Hauptflugbereich; zwei Platinen kannst du parallel im gleichen Winkel oder in einem leichten V (ca. 15°) montieren, um die horizontale Abdeckung zu verbreitern.
- Dipol-/Paddelantennen (ARS-NT5B7, ARS-25-57A): vertikal montieren für die beste omnidirektionale Abdeckung in der Horizontalebene.

### B. RC2 / RC Pro / Smart Controller (intern, Gehäuseöffnung erforderlich)

> ⚠️ **Dieser Vorgang öffnet das Controller-Gehäuse und erfordert möglicherweise Bohrungen – ein irreversibler Umbau, der sofort zum Verlust der DJI-Garantie führt.** Er richtet sich nur an Nutzer mit DIY-/RF-Umbau-Erfahrung. Wenn du dich mit dem Öffnen nicht sicher fühlst, wende dich an einen professionellen Umbau-Service oder bleib beim Originalzustand.

**Was du brauchst:**
- IPEX- (oder IPEX4-, je nach Modell prüfen) Female → RP-SMA-Female (Bulkhead)-Adapterkabel × 2
- Kreuzschlitzschraubendreher
- Bohrer oder Cuttermesser (falls du eine Bohrung für die RP-SMA-Basis ins Gehäuse machen musst; Durchmesser je nach Adapter, meist ca. 6–8 mm)
- ALFA-Antennen × 2 (empfohlen: APA-M25 oder ARS-25-57A)
- Heißkleber oder wasserfesten Kleber (Adapter fixieren, Bohrung gegen Staub und Feuchtigkeit abdichten)
- Smart Controller zusätzlich: Heißluftföhn (zum Erweichen und Ablösen der seitlichen Polster)

**Schritte:**

1. **Ausschalten und Akku entfernen/stromlos machen** – vermeidet Kurzschlussrisiken.
2. **Gehäuse öffnen:** Entferne die Befestigungsschrauben auf der Rückseite (beim Smart Controller zuerst mit dem Heißluftföhn die seitlichen Polster lösen, dann die Schrauben der Rückabdeckung), öffne die Clips vorsichtig – ziehe nie mit Gewalt an Flachbandkabeln.
3. **Originale Antennenanschlüsse lokalisieren:** Finde die IPEX/IPEX4-Antennenanschlüsse auf der Hauptplatine.
4. **Originale Stecker abziehen:** senkrecht und sanft ziehen, um die Buchse auf der Platine nicht zu beschädigen.
5. **Bohrposition wählen** (falls nötig): eine Stelle an der Seite oder Oberseite des Gehäuses, die Griff und Innenraum nicht beeinträchtigt.
6. **Bohren und Basis probeweise montieren**, auf sauberen Sitz prüfen, Grate entfernen.
7. **Adapterkabel anschließen:** Die IPEX-Seite kommt an die Originalbuchse auf der Hauptplatine, die RP-SMA-Female-Seite wird von innen durchs Gehäuse geschraubt, das Gewinde schaut außen heraus.
8. **Am besten beide Antennen umbauen**, damit die Diversity-/MIMO-Empfangswege nicht asymmetrisch werden.
9. **Gegen Staub abdichten:** Die Kanten der Bohrung verstärken, damit keine Fremdkörper und Feuchtigkeit eindringen.
10. **Gehäuse wieder zusammensetzen** und alle Originalschrauben festziehen.
11. **ALFA-Antennen aufschrauben** – von Hand, ohne übermäßige Kraft.
12. **Einschalten und testen** – Signal- und Reichweitentest auf sicherem, freiem Gelände.

---

## Häufig gestellte Fragen

**Frage: Erlöscht die DJI-Garantie, wenn ich die Antennen tausche?**

Antwort: Bei Modellen mit externem RP-SMA-Anschluss wie dem RC-N1 gelten die externen Antennen als vom Nutzer wartbare Teile – der Tausch selbst beeinträchtigt die Garantie des Controllers kaum. Heb die Originalantennen aber auf, um sie bei einem Reparaturservice wieder anzubauen. **Bei RC2, RC Pro und Smart Controller – Modellen, die für den Umbau geöffnet werden müssen – erlischt die Garantie sofort mit dem Öffnen des Gehäuses.** Das ist ein fundamentaler Unterschied zum RC-N1. Prüfe also zuerst dein Modell, bevor du dich entscheidest.

**Frage: Mein Controller hat keinen sichtbaren Gewindeanschluss – kann ich trotzdem upgraden?**

Antwort: Ja, aber auf anderem Weg. Modelle wie RC2, RC Pro und Smart Controller haben zwar keinen externen Gewindeanschluss, lassen sich aber trotzdem über eine Gehäuseöffnung plus Adapterkabel mit ALFA-Antennen verbinden. Das erfordert etwas DIY-/RF-Umbau-Erfahrung, kostet die Garantie und erfordert möglicherweise eine irreversible Bohrung im Gehäuse. Wenn du diese Erfahrung nicht hast, wende dich an einen professionellen Umbau-Service oder bleib beim Originalzustand.

**Frage: Kann ich diese ALFA-Antennen auch für Nicht-DJI-FPV-Systeme nutzen?**

Antwort: Ja – jedes RP-SMA-kompatible System auf 2,4 GHz oder 5,8 GHz funktioniert damit, zum Beispiel:

- **ExpressLRS (ELRS)**-Sender und -Empfänger auf 2,4 GHz
- **FrSky R9**-Systeme (Achtung: R9 arbeitet auf 915 MHz – andere Frequenz, andere Antenne nötig)
- **TBS Crossfire** (915 MHz – ebenfalls nicht kompatibel, hier brauchst du eine 900-MHz-Antenne)
- 5,8-GHz-**Videosender (VTX)** mit RP-SMA-Anschluss

Achte beim Ersatzkauf darauf, dass sowohl der **Anschlusstyp** als auch das **Frequenzband** passen.

**Frage: Was bringt es, beim RC-N1 nur eine statt beide Antennen zu tauschen?**

Antwort: Das DJI-OcuSync-System nutzt beide Antennen für den **Diversity-/MIMO-Empfang** und wählt laufend die Antenne mit dem stärkeren Signal. Nur eine Antenne zu tauschen erzeugt ein asymmetrisches Setup mit deutlich unterschiedlicher Leistung der beiden Antennen. Das System bevorzugt meist die aufgebaute Antenne, aber die beste Leistung erreichst du mit zwei gleichwertigen Antennen – tausch also am besten beide.

**Frage: Muss ich nach dem Upgrade Einstellungen in der DJI-App ändern?**

Antwort: Nein. Der DJI-Controller verwaltet Antennenauswahl und Frequenzbandwahl automatisch – nach einem rein physischen Antennentausch sind keine App-Konfigurationsänderungen nötig.

**Frage: APA-M25 oder ARS-25-57A – wie entscheide ich mich?**

Antwort: Wenn dein Controller während des Flugs meist stabil in eine Richtung zeigt, nimm die **APA-M25** (Richtantennenplatine, höchster Gewinn). Wenn du oft kreist, umrundest oder Nahdurchflüge fliegst – oder dich nicht um die Antennenausrichtung kümmern willst –, nimm die **ARS-25-57A** (omnidirektionale Paddelantenne, ohne Ausrichtung).

---

## Fazit

Beim Antennen-Upgrade für DJI-Controller klaffen Aufwand und Wirkung je nach Modell weit auseinander. **RC-N1** und andere Modelle mit externem RP-SMA-Anschluss gehören zu den einfachsten und kosteneffektivsten RF-Verbesserungen für Drohnenpiloten: von Hand aufschrauben, fertig – ganz ohne Werkzeug. Die neueren Modelle mit Display – **RC2, RC Pro, Smart Controller** – setzen dagegen auf fest verbaute, interne Antennen. Wer dort wirklich eine Hochgewinnantenne anschließen will, muss das Gehäuse öffnen, Adapterkabel einbauen und die Garantie verlieren – das solltest du dir vor dem ersten Handgriff klar machen.

Unabhängig von deinem Modell gilt: Das Ziel eines Antennen-Upgrades ist mehr **Zuverlässigkeit und Link-Reserve** innerhalb des legalen Flugbereichs – nicht das Durchbrechen der regulatorischen Grenzen. Flieg verantwortungsvoll, heb die Originalteile auf und genieß die verbesserte Link-Qualität.

---

## Referenzen

1. [DJI Offizielle Website — Controller-Produktspezifikationen](https://www.dji.com/)
2. [DJI RC 2 Support-Seite](https://www.dji.com/support/product/rc-2)
3. [FCC Part 15 — Vorschriften für unlizenzierte Funkgeräte](https://www.fcc.gov/engineering-technology-laboratory-division/general/radio-spectrum-and-rulemaking)
4. [ALFA Network Offizielle Website — Antennen-Zubehörspezifikationen](https://www.alfa.com.tw/)
5. [Taiwanische National Communications Commission (NCC) — Telekommunikationsverwaltungsgesetz](https://www.ncc.gov.tw/)
6. [IEEE-802.11-Standarddokumente — WLAN-Spezifikationen](https://standards.ieee.org/ieee/802.11/)
7. mavicpilots.com-Community-Threads: „RC2 / RC external antenna mod", „RC 2 and RC Pro controller external antennae", „Connecting external antennas to the RC Plus" (2024)
8. Alientech — „How to modify antenna of the DJI smart controller" Umbau-Tutorial (2019)