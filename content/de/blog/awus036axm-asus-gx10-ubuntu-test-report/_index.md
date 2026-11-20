---
title: "AWUS036AXM im Einzelkartentest: MediaTek MT7921AU (Wi-Fi 6 2x2) auf dem ASUS GX10 + Ubuntu 24.04 (ARM64) – Monitor-, AP- und WPA3-Fähigkeit und die Injection-Grenze"
slug: awus036axm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axm
  - mt7921
  - mt7921u
  - wifi-6
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - ap-mode
  - wpa3-sae
  - monitor-mode
description: "AWUS036AXM (mt7921u) im Praxistest auf ASUS GX10 / Ubuntu 24.04 ARM64: Monitor, AP und WPA3 nutzbar, doch die Paket-Injektion schlägt fehl – nicht geeignet für Penetrationstests, positioniert als reine AP- und Verbindungskarte."
faq:
  - question: "Kann der AWUS036AXM Paket-Injektion (packet injection) durchführen?"
    answer: "Auf unserer Testplattform (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia) nicht. aireplay-ng --test meldet in 2,4 GHz und 5 GHz No Answer, Found 0 APs, daher sind auch deauth und das Erfassen eines WPA-Handshakes nicht möglich. Die Ursache ist eine mac80211-chanctx-Regression im kernel 6.16+, nicht eine prinzipielle Injektionsunfähigkeit des Chips; der baugleiche AWUS036AXML liefert dasselbe Ergebnis. Wer Injektion braucht, wählt stattdessen die im Test funktionierenden AWUS036EACS, ACH oder ACS."
  - question: "Eignet sich der AWUS036AXM für Penetrationstests oder Kali?"
    answer: "Nicht empfohlen. Monitor ist nutzbar, aber der Empfang ist schwach, Client- und Data-Pakete gehen häufig verloren, und auf dieser Plattform schlägt die Injektion fehl – deauth oder das Erfassen eines Handshakes ist nicht möglich. Die Plattform dieses Artikels ist Ubuntu 24.04, auf der Kali-Distribution selbst wurde nicht getestet. Die Karte eignet sich für reinen AP-Betrieb, normale Verbindungen und WPA3-Hotspots; für Penetrationstests wählen Sie AWUS036EACS, ACH oder ACS."
  - question: "Muss man für den AWUS036AXM unter Ubuntu 24.04 einen Treiber nachinstallieren?"
    answer: "Nein. Der mt7921u-Treiber ist in kernel 6.17 enthalten, die Karte wird direkt nach dem Einstecken erkannt (USB ID 0e8d:7961), ohne DKMS, ohne Kompilieren. Der Treiber bietet keinen IBSS- (Ad-hoc-) und keinen Mesh-Modus; das ist eine Einschränkung, kein Konfigurationsproblem."
  - question: "Kann der AWUS036AXM als AP einen Hotspot öffnen? Unterstützt er WPA3?"
    answer: "Ja, das ist seine beste Anwendung. In 2,4 GHz (802.11n) und 5 GHz VHT80 konnte sich jeweils ein iPhone verbinden und wurde authorized; WPA3-SAE ist auf 2,4 GHz nutzbar (MFP: yes; WPA3 auf 5 GHz wurde nicht getestet), ältere iPhones benötigen sae_pwe=0; auch STA+AP parallel (VIF) ist nutzbar. In dieser Runde wurden nur 2,4 und 5 GHz getestet, 6 GHz und Bluetooth nicht gesondert."
  - question: "Ist der Monitor-Modus des AWUS036AXM brauchbar?"
    answer: "Er kann in den Monitor-Modus wechseln, in 2,4 GHz und 5 GHz werden Beacons empfangen, doch der Empfang ist schwach und die Menge an Client- und Data-Paketen gering; empfohlen wird, einen einzelnen Kanal zu fixieren statt zu springen. Für großräumiges oder weitreichendes Mithören sind in unseren Tests AWUS036AXER und ACH deutlich stärker."
draft: false
---

{{< tldr >}}Der AWUS036AXM ist auf ASUS GX10 / Ubuntu 24.04 ARM64 für Monitor, AP, WPA3 und VIF nutzbar, doch die Paket-Injektion schlägt im Test fehl (No Answer / Found 0 APs) – deauth oder das Erfassen eines Handshakes ist nicht möglich, für Penetrationstests nicht empfohlen; positioniert als reine AP- und Verbindungskarte.{{< /tldr >}}

Yupitek ist der Taiwan-Distributor von ALFA Network. Dies ist der Einzelkartentest des AWUS036AXM mit einem ganz einfachen Ziel: klar zu messen, was diese Wi-Fi-6-Karte auf dem **ASUS GX10 (ARM64) + Ubuntu 24.04** kann und was nicht, damit kaufende Kunden nicht aus dem Datenblatt raten müssen.

Zuerst die Positionierung klarstellen: Alle folgenden Tests wurden auf Yupiteks eigener Hardware, im eigenen Büro-WLAN, gegen unsere eigenen Testgeräte durchgeführt. Das ist die Hardware-Verifikation von Produktkompatibilität und Fähigkeitsgrenzen durch den Distributor, keine Angriffsanleitung gegen fremde Netzwerke. Der Artikel liefert keinerlei Bedienschritte gegen externe Netzwerke; die Monitor- und injektionsbezogenen Messungen erfolgen ausnahmslos in einer eigenen, geschlossenen Umgebung gegen eigene Geräte.

Das Wichtigste zu dieser Karte zuerst: **Ihre Injection auf dieser Plattform schlägt fehl.** Wenn Ihr Einsatzzweck Injektion oder Handshake-Erfassung umfasst, können Sie direkt zu Abschnitt vier und fünf zur Auswahlentscheidung springen; wenn Sie eine stabile Verbindung und einen AP-Aufbau brauchen, ist der AWUS036AXM eine sehr tüchtige Karte.

## 1. Karte und Testplattform

Der AWUS036AXM verwendet den MediaTek-**MT7921AU**-Chip, läuft über den kernel-internen **mt7921u**-Treiber und hat als Spezifikation **Wi-Fi 6 (802.11ax), 2x2** zwei räumliche Datenströme. Der chipgleiche **AWUS036AXML** (MT7921AUN, zusätzlich mit Bluetooth) verhält sich auf dieser Plattform bei Wi-Fi-Monitor / AP / Injektion exakt gleich, beide Karten können sich gegenseitig als Referenz dienen; der Unterschied ist, dass der AXML zusätzlich Bluetooth hat und im Test auf dieser Maschine das 6-GHz-Band nutzbar war, während 6 GHz und Bluetooth des AXM in dieser Runde nicht gesondert getestet wurden.

- **Rechenplattform**: ASUS GX10 (ARM64 / aarch64)
- **Betriebssystem**: Ubuntu 24.04 LTS
- **Kernel-Version**: kernel 6.17.0-1014-nvidia
- **Testgerät**: Apple iPhone 7 Plus (WPA3-SAE und VIF zusätzlich mit iPhone 15 Pro nachgemessen)
- **Testumgebung**: eigenes Büro-WLAN, SSID `YUPITEK`, 2,4GHz ch5 / 5GHz ch36
- **Testzeitraum**: 2026-11-16 bis 2026-11-18, Messung an echter Hardware

## 2. Hardware und Treiber (ohne Installation nutzbar)

Der mt7921u-Treiber ist bereits in kernel 6.17 enthalten, der AWUS036AXM wird direkt nach dem Einstecken in den GX10 erkannt, ohne DKMS, ohne selbst einen Drittanbietertreiber zu kompilieren. Das ist der bequemste Aspekt dieser MediaTek-Kartengeneration auf ARM64.

| Punkt | Inhalt |
|---|---|
| Modell | AWUS036AXM |
| Chip | MediaTek MT7921AU |
| USB ID | `0e8d:7961` |
| Treiber (in-kernel) | `mt7921u` |
| Generation / Streams | Wi-Fi 6 (802.11ax) / 2x2 |
| Schnittstellenmodi | managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO / P2P-device |
| Nicht unterstützte Modi | IBSS (Ad-hoc), Mesh (802.11s) |

Bestätigen, dass die Karte erkannt wird:

```bash
lsusb | grep 0e8d:7961
```

Die erwartete Ausgabe ist `ID 0e8d:7961 MediaTek Inc. Wireless_Device`. Beachten Sie außerdem, dass in den von `iw phy info` aufgelisteten Schnittstellenmodi weder IBSS noch mesh point vorkommen; das ist eine prinzipielle Einschränkung des mt7921u, kein Konfigurationsproblem; für Mesh- / IBSS-Szenarien verwenden Sie stattdessen den `mt76`-basierten AWUS036ACM / ACHM.

## 3. Getestete Fähigkeiten: Monitor / AP / WPA3 und die ehrliche Erklärung zum Injection-Fehlschlag

Zuerst eine zentrale Fähigkeitsmatrix, danach Punkt für Punkt.

| Fähigkeit | 2,4 GHz | 5 GHz | Testanmerkung |
|---|---|---|---|
| Monitor (Mithören) | ✅ nutzbar (Empfang schwächer) | ✅ nutzbar (Empfang schwächer) | Beacons werden empfangen, Client- / Data-Frames gering |
| **Injection (Injektion)** | ❌ **auf dieser Plattform fehlgeschlagen** | ❌ **auf dieser Plattform fehlgeschlagen** | Ursache: mac80211-chanctx-Regression im kernel 6.16+ (nicht chipbedingt) |
| AP (Hotspot) | ✅ inkl. 802.11n (HT20) | ✅ VHT 80 MHz | iPhone 7 Plus verbunden, authorized |
| WPA3-SAE | ✅ | Nicht getestet | MFP: yes, `sae_pwe=0` kompatibel mit älteren iPhones; nur auf 2,4 GHz getestet |
| VIF (STA + AP) | ✅ | ✅ | eine Karte, zwei Funktionen, STA-Seite ping 17 ms |

### Monitor (Mithören) ✅ nutzbar, aber Empfang schwach

Sowohl 2,4GHz als auch 5GHz können in den Monitor-Modus wechseln und empfangen beide Beacons. Ehrlich gesagt: Der Empfang des AWUS036AXM ist deutlich schwächer als der des AWUS036ACM / ACHM derselben Plattform, die gemessene Frame-Zahl ist gering und die Erfassungsmenge an Client- und Data-Paketen niedrig. In der Praxis empfiehlt sich, **einen einzelnen Kanal zu fixieren** und nicht zu springen, dann wird die Ausbeute etwas stabiler.

Es gibt noch einen leicht fehlzudeutenden Punkt: Im Monitor-Modus meldet `txpower` 3 dBm – das ist ein Meldeartefakt (die Hardware sendet tatsächlich mit etwa 20 dBm, per `txpower_sku` verifiziert) und bedeutet nicht, dass die Sendeleistung wirklich so weit gedrosselt wäre. Der AWUS036AXM ist ohnehin nicht für großräumiges Mitschneiden ausgelegt; wer breit scannen und weit empfangen will, schaut auf den AWUS036AXER mit stärker abgestimmten Antennen und aktiverem Frequenzsprung oder den AWUS036ACH mit Doppelantenne und hohem Gewinn – beide empfangen im Monitor-Modus derselben Plattform deutlich stärker.

### AP (Hotspot) ✅ die Paradedisziplin des AXM

Im 2,4GHz-AP-Betrieb lässt sich zugleich 802.11n (HT20) aktivieren, das iPhone 7 Plus handelte MCS 7 aus und wurde authorized. 5GHz lässt sich bis **VHT 80 MHz** öffnen, das iPhone verband sich als VHT-NSS2 und wurde authorized. Egal ob 2,4G oder 5G, der AWUS036AXM ist als Hotspot stabil – das ist seine kaufenswerteste Fähigkeit auf dieser Plattform.

### WPA3-SAE ✅

Mit WPA3-SAE auf der AP-Seite verband sich das iPhone 7 Plus erfolgreich, MFP (Management Frame Protection) zeigte `yes`. Praxishinweis: `sae_pwe=0` setzen macht es mit älteren Geräten wie dem iPhone 7 Plus kompatibel; bei `sae_pwe=2` kann sich ein älteres iPhone womöglich nicht verbinden.

### VIF (STA + AP, eine Karte zwei Funktionen) ✅

Der AWUS036AXM kann gleichzeitig als STA ein vorhandenes WLAN nutzen und eine AP-virtuelle Schnittstelle (VIF) öffnen. Im Test lag beim Verbinden des iPhone 15 Pro mit dem AP-VIF der ping der STA-Seite zu `YUPITEK` bei etwa 17 ms, die Verbindung war normal. Für den Bedarf „mit einer Karte zugleich online gehen und einen Hotspot teilen“ ist das nutzbar.

### Injection (Injektion) ❌ auf dieser Plattform fehlgeschlagen – das ist die Wasserscheide der Auswahl

Das ist der wichtigste und am ehrlichsten darzulegende Punkt des AWUS036AXM. Die Ausgabe des Tests `aireplay-ng --test` lautet:

```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

In 2,4GHz und 5GHz derselbe Fehlschlag. Zuerst ein verbreitetes Missverständnis aufklären: Dass `iw` im Monitor-Modus als txpower nur 3 dBm meldet, ist ein **Meldeartefakt**; die Hardware sendet tatsächlich mit etwa 20–23 dBm (per `txpower_sku` verifiziert), die Sendeleistung wurde nicht gedrosselt und ist nicht die Hauptursache des Fehlschlags. Die wahre Ursache liegt auf der **Softwareebene**: Seit kernel 6.16 tritt im channel context (chanctx) von mac80211 eine Regression auf, durch die der Stock-Treiber im active-monitor- / Injektionsszenario die Ziel-Beacons nicht empfängt, worauf `aireplay-ng` auf `No Answer` erkennt. Das ist eine **Regression auf Kernel-Seite, keine prinzipielle Injektionsunfähigkeit des MT7921-Chips**. Das Phänomen ist in morrownr/USB-WiFi issue #387 dokumentiert, die Ursachenanalyse in morrownr/mt76 issue #18.

Zu ergänzen ist: Community-Tests zeigen, dass sich am selben Modell mit einem git- / gepatchten Treiber active monitor plus Injektion tatsächlich zum Laufen bringen lässt; doch selbst dann sperrt die MT7921-Firmware die Injektion **auf die Basisraten 1 Mbps / 6 Mbps** und erlaubt keine Injektion mit HT- / VHT-Raten. Anders gesagt: Selbst wenn man die Kernel-Regression umgeht, bleibt die Injektionsfähigkeit dieser Karte eingeschränkt. Im Vergleich dazu funktioniert die Injektion bei den Realtek-rtw89-Karten (wie AWUS036AX / AXER) mit derselben aircrack-ng-Suite auf derselben GX10-Plattform; der MT7921-Weg ist auf **stock kernel 6.17** nicht gangbar.

Nochmals betont: Das ist kein Defekt einer einzelnen Karte und kein falsch eingestellter Parameter. Der chipgleiche AWUS036AXML verhält sich exakt gleich; auf stock kernel 6.17 lässt sich das weder durch Parameteränderung noch durch Kanalwechsel noch durch Umstellen der regulatory domain retten – die Ursache ist die mac80211-chanctx-Regression im kernel 6.16+ plus die Injektions-Ratensperre der Firmware, kein Hardwaredefekt des Chips. Die direkte Folge: Der AWUS036AXM kann auf dieser Plattform **keinen deauth senden und keinen WPA-Handshake aktiv erfassen**. Wer diese Fähigkeiten braucht, verwendet die Realtek- / mt76x-Lösung aus dem nächsten Abschnitt.

Zu den erweiterten Funktionen hier die Übersicht:

| Erweiterte Funktion | Status | Erläuterung |
|---|---|---|
| WPA-Handshake-Erfassung | ❌ | wegen Injektionsfehlschlag nicht nutzbar, stattdessen ACM / ACHM / ACH / ACS / EACS |
| VIF (STA + AP) | ✅ | eine Karte zwei Funktionen nutzbar |
| Active monitor | 🟡 | `set monitor active` wird akzeptiert, ACK nicht verifiziert |
| Ad-hoc (IBSS) | N/A | mt7921u unterstützt es nicht |
| Mesh (802.11s) | N/A | mt7921u unterstützt es nicht |
| Wi-Fi Direct (P2P) | ⬜ | Treiber deklariert Unterstützung, mangels zweitem Gerät nicht getestet |

### Betriebssicherheit und Praxishinweise

Ein paar praktische Kernpunkte für den Betrieb dieser Karte am GX10 – vorab genannt, erspart Fallstricke:

- **Trennen Sie nicht Ihr eigenes Netzwerk**: Führen Sie auf keinen Fall `airmon-ng check kill` aus, es schaltet den NetworkManager ab und trennt den gesamten GX10 vom Netz. Bedienen Sie beim Arbeiten nur die externe `wlx*`-Schnittstelle und fassen Sie die interne Uplink-Hauptleitung des GX10 nicht an.
- **AP-Passwort mindestens 8 Zeichen**: Andernfalls meldet hostapd `invalid WPA passphrase length` und startet nicht.
- **Wenn das Telefon die SSID nicht findet**: Die Karte einmal aus- und wieder einstecken, um sie zurückzusetzen, oder das Telefon näher bringen (die im Monitor-Modus gemeldeten 3 dBm sind ein Artefakt, nicht die reale Leistung, und nicht die Hauptursache).
- **RX-Stall beheben**: Wenn nach wiederholtem Wechsel zwischen monitor / AP plötzlich nichts mehr gescannt wird, liegt meist ein RX-Stall vor; die Karte einmal aus- und wieder einstecken stellt den Zustand wieder her (der Schnittstellenname ist nach MAC benannt und ändert sich nicht).

## 4. Geeignete und ungeeignete Einsatzzwecke

Die obigen Messungen auf einen Satz verdichtet: Der AWUS036AXM ist eine ausgezeichnete „Verbindungs- / AP“-Karte, aber keine „Injektions- / Angriffs-und-Abwehr“-Karte.

**Geeignete Einsatzzwecke**

- stabile alltägliche Verbindung (Wi-Fi 6, 2x2)
- Aufbau von 2,4GHz- / 5GHz-AP-Hotspots (inkl. 802.11n und VHT80)
- WPA3-SAE-Kompatibilitätsprüfung und Deployment-Test
- STA + AP, eine Karte zwei Funktionen (VIF)
- leichter Monitor-Bedarf zum passiven Mitschneiden von Beacons

**Ungeeignete Einsatzzwecke (Warnung)**

- injection / deauth
- WPA-Handshake-Erfassung, aktive Angriffs-und-Abwehr-Übungen
- Experimente, die IBSS (Ad-hoc) oder Mesh erfordern
- großräumiges Monitor-Mitschneiden mit langer Reichweite und hoher Empfindlichkeit

**Die wichtigste Warnung**: Wenn Ihr Einsatzzweck **Injection oder Handshake** ist, **wählen Sie nicht den AWUS036AXM (oder den chipgleichen AWUS036AXML)**. Die Injektion des MT7921 schlägt auf der Plattform ASUS GX10 (ARM64 / Ubuntu 24.04 / stock kernel 6.17) fehl; die Ursache ist die mac80211-chanctx-Regression im kernel 6.16+, nicht eine prinzipielle Injektionsunfähigkeit des Chips. In der Stock-Umgebung mit Stand 2026-11-18 lässt sich das nicht durch Parameteränderung lösen – überlassen Sie die Karte dem Szenario „reine Verbindung / reiner AP“.

## 5. Auswahlempfehlung (reiner AP / Verbindung)

| Ihr Bedarf | Empfohlene Wahl | Grund |
|---|---|---|
| reiner AP / stabile Verbindung (ohne Injektion) | **AWUS036AXM** / AWUS036AXML | MediaTek stabil in der Verbindung, gute AP- und WPA3-Leistung |
| Penetrationstest (injection + handshake) | AWUS036EACS / AWUS036ACH / AWUS036ACS | Dual-Band-Injektion nutzbar, End-to-End-Handshake läuft durch |
| stärkster Empfang / Monitor über große Distanz | AWUS036AXER / AWUS036ACH | AXER scannt aktiv mit Frequenzsprung, ACH mit Doppelantenne und hohem Gewinn |
| Wi-Fi 6 + AP und Injektion erforderlich | AWUS036AX / AWUS036AXER | 2x2 VHT80, AP stabil und Injektion nutzbar |
| mesh / IBSS Experiment | AWUS036ACM / AWUS036ACHM | `mt76`-Treiber im Einzelbetrieb aufbaubar |

Ein Satz im Klartext: Für stabile Verbindung und AP-Betrieb ist der AWUS036AXM sehr tüchtig; sobald Injektion oder Handshake ins Spiel kommen, wechseln Sie zu Realteks EACS / ACH / ACS. Den vollständigen Vergleich dieser Kartencharge auf ARM64 sowie die volle Matrix aus Monitor / Injection / AP / WPA3 für 9 Modelle finden Sie im Gesamttabellen-Hub:

- [Vollständigster Praxistest 2026: 9 ALFA-WLAN-Karten auf ASUS GX10 (ARM64 / Ubuntu 24.04) in der Gesamtmatrix](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

Nochmals betont die Positionierung: Alle monitor- / injektionsbezogenen Messungen dieses Artikels erfolgen ausnahmslos in Yupiteks eigener, geschlossener Umgebung gegen eigene Testgeräte, zum Zweck der Verifikation von Produktfähigkeit und Kompatibilitätsgrenzen – die genannten Operationen gegen fremde Netzwerke werden weder bereitgestellt noch empfohlen.

## Häufig gestellte Fragen (FAQ)

**F1. Kann der AWUS036AXM Paket-Injektion (packet injection) durchführen?**
Auf unserer Testplattform (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia) nicht. `aireplay-ng --test` meldet in 2,4 GHz und 5 GHz `No Answer`, `Found 0 APs`, daher sind auch deauth und das Erfassen eines WPA-Handshakes nicht möglich. Die Ursache ist eine mac80211-chanctx-Regression im kernel 6.16+, nicht eine prinzipielle Injektionsunfähigkeit des Chips; der baugleiche AWUS036AXML liefert dasselbe Ergebnis. Wer Injektion braucht, wählt stattdessen die im Test funktionierenden AWUS036EACS, ACH oder ACS.

**F2. Eignet sich der AWUS036AXM für Penetrationstests oder Kali?**
Nicht empfohlen. Monitor ist nutzbar, aber der Empfang ist schwach, Client- und Data-Pakete gehen häufig verloren, und auf dieser Plattform schlägt die Injektion fehl – deauth oder das Erfassen eines Handshakes ist nicht möglich. Die Plattform dieses Artikels ist Ubuntu 24.04, auf der Kali-Distribution selbst wurde nicht getestet. Die Karte eignet sich für reinen AP-Betrieb, normale Verbindungen und WPA3-Hotspots; für Penetrationstests wählen Sie AWUS036EACS, ACH oder ACS.

**F3. Muss man für den AWUS036AXM unter Ubuntu 24.04 einen Treiber nachinstallieren?**
Nein. Der mt7921u-Treiber ist in kernel 6.17 enthalten, die Karte wird direkt nach dem Einstecken erkannt (USB ID `0e8d:7961`), ohne DKMS, ohne Kompilieren. Der Treiber bietet keinen IBSS- (Ad-hoc-) und keinen Mesh-Modus; das ist eine Einschränkung, kein Konfigurationsproblem.

**F4. Kann der AWUS036AXM als AP einen Hotspot öffnen? Unterstützt er WPA3?**
Ja, das ist seine beste Anwendung. In 2,4 GHz (802.11n) und 5 GHz VHT80 konnte sich jeweils ein iPhone verbinden und wurde authorized; WPA3-SAE ist auf 2,4 GHz nutzbar (`MFP: yes`; WPA3 auf 5 GHz wurde nicht getestet), ältere iPhones benötigen `sae_pwe=0`; auch STA+AP parallel (VIF) ist nutzbar. In dieser Runde wurden nur 2,4 und 5 GHz getestet, 6 GHz und Bluetooth nicht gesondert.

**F5. Ist der Monitor-Modus des AWUS036AXM brauchbar?**
Er kann in den Monitor-Modus wechseln, in 2,4 GHz und 5 GHz werden Beacons empfangen, doch der Empfang ist schwach und die Menge an Client- und Data-Paketen gering; empfohlen wird, einen einzelnen Kanal zu fixieren statt zu springen. Für großräumiges oder weitreichendes Mithören sind in unseren Tests AWUS036AXER und ACH deutlich stärker.

## 6. Weiterführende Literatur

Die folgenden verwandten Artikel gehen nach und nach online (Links in Arbeit):

- „Ohne Treiberinstallation: Monitor- und AP-Modus unter Ubuntu (ARM64) aktivieren“ → [`/de/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/de/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- „WPA3-SAE-Fähigkeit und Handshake-Praxis (in eigener Umgebung verifiziert)“ → [`/de/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/de/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- „AWUS036AXML im Einzelkartentest (gleicher MT7921-Chip + BT)“ → (in Arbeit)
- „Warum mt7921u ab Kernel 6.16 nicht injizieren kann: die chanctx-Regression und die Ratensperre der Firmware erklärt“ → (in Arbeit)

---

*Testinstanz: Yupitek (ALFA-Distributor) | Plattform: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Testgerät: Apple iPhone 7 Plus (WPA3 / VIF zusätzlich iPhone 15 Pro)*
