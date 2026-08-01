---
title: "4G/5G-Failover im Industrie-Router: EM9191 und der Weg ins private 5G | Yupitek"
description: "Wie baust du ein 4G/5G-Failover in deinen Industrie-Router? Am Beispiel EM9191 zeigen wir den Unterschied zwischen privatem 5G-SA-Netz und LTE-Reserve sowie die wichtigsten Punkte bei Frequenzbändern, Antennen und Kühlung."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "de"
hreflang_group: "industrial-router-4g-5g-failover-guide"
slug: "industrial-router-4g-5g-failover-guide"
tags: ["Sierra Wireless", "EM9191", "5G", "LTE", "Failover", "Private 5G"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/de/products/sierra/"
faq:
  - question: "Unterstützt der EM9191 5G-mmWave?"
    answer: "Nein. In der offiziellen Spezifikation steht klar, dass der EM9191 kein FR2 (mmWave) unterstützt. Wenn du Millimeterwellen brauchst, nimm den EM9190."
  - question: "Kann ich den EM9191 in einem privaten 5G-Netz nutzen?"
    answer: "Ja. Private 5G-Netze nutzen meist die SA-Architektur (Standalone), und der EM9191 unterstützt die SA-Architektur in 5G NR FR1 vollständig."
  - question: "Worauf muss ich beim Einbau des EM9191 in einen Router achten?"
    answer: "Vier Punkte: 1. Die Länge beträgt 52 mm, nicht 42 mm. 2. Alle 4 Antennen müssen angeschlossen werden. 3. Das Netzteil muss Spitzenströme von 2,7 A verkraften. 4. Die Kühlung muss stimmen, die Innentemperatur darf 115 °C nicht übersteigen."
---

# 4G/5G-Failover im Industrie-Router: EM9191 und der Weg ins private 5G

**Kurz gesagt: Ein 5G-Modul im Industrie-Router als Backup ist wie eine Versicherung. Das Sierra-Wireless-Modul EM9191 unterstützt sowohl superschnelles 4G (LTE Cat 20) als auch private 5G-Netze (5G SA). Du kannst also heute ganz normal 4G-Backup fahren, und wenn dein Werk später ein privates 5G-Netz bekommt, musst du nicht mal die Hardware tauschen. Nahtloser Übergang!**

Im Werk verbrennt jede Minute Netzausfall bares Geld. Maschinendaten kommen nicht an, das Remote-Monitoring zeigt schwarz, und der Schaden ist schnell teurer als eine zweite Backup-Leitung. Genau deshalb ist Redundanz (Failover) so wichtig. Statt eine zweite physische Glasfaser eines anderen Anbieters zu ziehen, ist eine SIM-Karte mit Mobilfunk die klügere Lösung.

In diesem Artikel schauen wir uns die offizielle Spezifikation (EM919X Product Technical Specification) an und zeigen dir, warum der **EM9191** die perfekte Wahl ist: heute fürs Backup, morgen fürs private Netz.

> Technische Datenquelle: offizielle Sierra-Wireless-Spezifikation. Artikel zusammengestellt von Yupitek.

---

## 30-Sekunden-Überblick: Was kann der EM9191?

| Dein Bedarf | Schafft das der EM9191? | Warum? |
|---|---|---|
| **4G-Backup-Internet** | ✅ Klar | Unterstützt LTE Cat 20 (schnelle 7CC-Aggregation), als Backup mehr als genug. |
| **Anschluss ans private 5G-Netz** | ✅ Klar | Unterstützt die SA-Architektur in 5G FR1 (Sub-6), das Pflichtkriterium für private 5G-Netze. |
| **5G-Millimeterwellen (mmWave)** | ❌ Nein | Steht in der Spezifikation eindeutig drin! Für mmWave nimm den EM9190. |
| **Nur Geld sparen** | ⚠️ Anderes Modell prüfen | Wenn du dir zu 100 % sicher bist, dass du nie 5G brauchst, ist ein reines 4G-Modul (z. B. EM7690 oder EM7565) deutlich günstiger. |

---

## Wie funktioniert Failover?

Ganz einfach: In deinem Router läuft ein Software-Wächter, der dein Hauptnetz (z. B. Glasfaser) ständig anpingt. Wenn er merkt, dass das Hauptnetz tot ist, ruft er: „Umschalten!“ und leitet alle Datenpakete zum EM9191-Modul im Router, raus übers 5G. Sobald das Hauptnetz wieder da ist, fließt der Traffic unauffällig zurück.

**Das heißt: Eine Backup-Leitung muss nicht „immer am schnellsten“ sein, sondern „niemals ausfallen“.** Der Clou am EM9191: Wenn das 5G-Signal schlecht wird, wechselt er von selbst auf 4G und sendet weiter. Kein Verbindungsabbruch.

---

## Warum ist der EM9191 zwei Zukünfte in einem?

Im EM9191 steckt der 5G-Chip Qualcomm SDX55. Laut offizieller Spezifikation unterstützt er die zwei wichtigsten Modi:

1. **LTE Only** (reiner 4G-Modus)
2. **5G NR FR1 SA / NSA** (Standalone und Non-Standalone)

Was bedeutet das?
- **Heute**: Du nutzt ihn als erstklassige 4G-Karte (Cat-20-Niveau), weil das öffentliche 5G noch Funklöcher hat.
- **Morgen**: Wenn dein Unternehmen ein eigenes „privates 5G-Netz“ aufbaut (meist als SA-Architektur, überwiegend im Sub-6-Band), reicht eine Einstellungsänderung, um sich zu verbinden. Kein neues Hardware-Geld!

---

## Das harte Wissen für Ingenieure: 4 Fallstricke vor dem Einbau

Denk nicht, „Modul gekauft, eingesteckt, fertig“. Der EM9191 ist ein Energie- und Kühlungsmonster. Achte bei der Integration auf diese vier Punkte:

### 1. Antennen nicht voll bestückt, halbe Geschwindigkeit
Der EM9191 hat **4 MHF4-Antennenanschlüsse**. Um die volle 4x4-MIMO-Leistung zu nutzen (besonders im 5G-n78-Band), müssen alle 4 Antennen angeschlossen sein! Offiziell empfohlen: Kabeldämpfung unter 0,5 dB. Zieh keine ewig langen Billigkabel.

### 2. Schwaches Netzteil, ständige Abbrüche
Der EM9191 läuft mit 3,3 V. Der Punkt: Beim Datenversand liegt der **Spitzenstrom bei 2,7 A (2700 mA), dauerhaft bei 2 A (2000 mA)**. Wenn die Stromversorgung auf deinem Router-Board schwach ist, bricht die Spannung beim Speedtest ein, und das Modul startet in einer Endlosschleife neu.

### 3. Keine Kühlung, dann hängt er dir
5G-Module werden deutlich heißer als 4G. Laut Spezifikation darf die Innentemperatur **niemals über 115 °C liegen (besser unter 100 °C halten)**. Wenn du ihn in einen Outdoor-Router aus Blech sperrst, überhitzt er im Sommer garantiert. Nimm auf jeden Fall einen Kühlkörper und leite die Wärme ans Gehäuse.

### 4. Slotlänge und Schnittstelle
Es ist ein M.2-Modul, aber mit **52 mm Länge** deutlich länger als die üblichen 42-mm-Module. Die Schnittstelle ist PCIe Gen3 oder USB 3.1 Gen2. Achtung: Altes USB 2.0 wird nicht garantiert unterstützt!

---

## Fazit

Für ein Backup-Netz in der Industrie ist der EM9191 ein „Angriff und Verteidigung“ in einem.
Mit starkem LTE Cat 20 und 5G-SA-Support deckt er perfekt beides ab: „4G-Backup heute“ und „5G-Privatnetz morgen“. Wenn du bei der Integration Stromversorgung (2,7-A-Spitze), Kühlung (115-°C-Grenze) und Antennen (alle 4) im Griff hast, rettet er dir in kritischen Momenten den Hintern.

## Kaufinformationen (Call to Action)

Willst du den EM9191 in deinen Industrie-Router integrieren? Yupitek bietet komplette Hardware-Lösungen und technischen Support und hilft dir bei den kniffligsten Punkten: Kühlung und Antennen.
Schreib uns: **sales@yupitek.com**
Schau dir die Produkte an: [Sierra Wireless Serie](https://yupitek.com/de/products/sierra/)
