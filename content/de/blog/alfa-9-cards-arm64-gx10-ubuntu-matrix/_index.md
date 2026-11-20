---
title: "Der vollständigste Praxistest 2026: Die komplette Monitor-/Injection-/AP-Matrix von 9 ALFA-WLAN-Karten auf dem ASUS GX10 (ARM64 / Ubuntu 24.04)"
slug: alfa-9-cards-arm64-gx10-ubuntu-matrix
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix.webp"
author: "benny-lai"
tags:
  - alfa-network
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - wifi-6
  - kali-linux
description: "Praxistest von 9 ALFA-Wi-Fi-USB-Karten unter Ubuntu 24.04 ARM64 (GX10): Monitor, Injection, AP und WPA3-SAE, inklusive Kompatibilität mit den in Kali gebräuchlichen Werkzeugen und Auswahlempfehlungen; AWUS036ACH / EACS erreichen 100 % Injektion."
faq:
  - question: "Kann der AWUS036AXM unter Ubuntu Injection (Injektion) durchführen?"
    answer: "Auf dieser Plattform nicht. Im Test schlugen beim AWUS036AXM und AWUS036AXML (beide mit MT7921-Chip) die Injektionen in 2,4 GHz und 5 GHz fehl; die Hauptursache ist die mac80211-chanctx-Regression im stock kernel 6.16+ (nicht chip-bedingt), weshalb sie auf dieser Plattform nicht für Zwecke empfohlen werden, die Injektion oder Handshake-Erfassung erfordern."
  - question: "Welche ALFA-Karte hat unter Ubuntu die höchste Injektionserfolgsrate?"
    answer: "Im Test erreichten der AWUS036ACH und der AWUS036EACS in 2,4 GHz und 5 GHz jeweils 100 % Injektionserfolgsrate – die beiden besten der 9 Karten dieser Charge."
  - question: "Benötigen die 9 ALFA-Karten unter Ubuntu 24.04 einen zusätzlichen Treiber?"
    answer: "Nein. Alle 9 Karten nutzen auf kernel 6.17 ausschließlich kernel-interne (in-kernel) Treiber (rtw88- / rtw89- / mt76-Familie), werden direkt nach dem Einstecken erkannt und benötigen kein kompiliertes DKMS-Modul."
  - question: "Lässt sich mit einer ALFA-Karte unter Ubuntu ein WPA3-SAE-Hotspot aufbauen?"
    answer: "Ja, alle 9 Karten konnten im Test erfolgreich einen WPA3-SAE-Hotspot aufbauen und Geräte verbinden lassen (getestet auf 2,4 GHz bei allen Karten außer dem ACS, der auf 5 GHz getestet wurde; der AXML zusätzlich auf 6 GHz); nur der AWUS036ACHM benötigt die hostapd-Option sae_pwe auf 0 gesetzt, sonst scheitert die Verbindung des älteren iPhone 7 Plus."
  - question: "Können Kali-Linux-Nutzer dieses Ubuntu-Testergebnis als Referenz heranziehen?"
    answer: "Kali Linux basiert auf dem Debian-/Ubuntu-System und verwendet dieselben in-kernel-Treiber rtw88 / rtw89 / mt76, daher können die Treiberkompatibilität und die Fähigkeitsmatrix dieses Artikels grundsätzlich als Referenz für Kali-Nutzer dienen; die Testplattform dieses Artikels war jedoch Ubuntu 24.04 und wurde unter Kali noch nicht offiziell nachgemessen, maßgeblich sind daher spätere Nachmessungen."
draft: false
---

## Kernaussagen (TL;DR)

Yopitek (ALFA-Network-Distributor Taiwan) hat 9 ALFA-USB-WLAN-Adapter auf dem ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17) getestet: Alle 9 beherrschen Monitor-Modus und AP-Betrieb, AWUS036ACH und AWUS036EACS erreichen auf beiden Bändern 100 % Injektion, und die MT7921-basierten AWUS036AXM / AWUS036AXML scheitern auf dieser Plattform an der Injektion.

- **Monitor bei allen nutzbar**: Alle 9 Karten können in den Monitor-Modus wechseln, der Unterschied liegt nur in der Empfangsstärke.
- **Injection ist die Wasserscheide**: Die Realtek-`rtw88`-Karten ACH und EACS erreichen in beiden Bändern 100 % Injektion, ACS folgt knapp dahinter; die MT7921-Karten AXM / AXML schlagen auf dieser Plattform bei der Injektion fehl.
- **End-to-End-Handshake (Erfassung → Export der `.22000`) bei 7 von 9 Karten belegt**: ACM, ACHM, ACH, ACS, EACS, AX, AXER.
- **AP und WPA3-SAE fast durchweg bestanden**: Nur der AWUS036ACHM benötigt `sae_pwe=0`, um mit älteren iPhones kompatibel zu sein.
- **ARM64 ohne Kompilieren**: Alle 9 Karten nutzen die in kernel 6.17 enthaltenen Treiber, direkt nach dem Einstecken einsatzbereit, ohne DKMS.

Yopitek ist der Taiwan-Distributor von ALFA Network. Wenn Kunden eine USB-WLAN-Karte auswählen, sind die drei häufigsten Fragen fast immer dieselben: „Kann diese Karte in meiner Linux-Umgebung in den Monitor-Modus? Kann sie Injection? Kann sie einen AP aufbauen?“ Statt aus dem Datenblatt zu antworten, haben wir die 9 aktuellen ALFA-Karten direkt auf unseren eigenen Labortisch gelegt und in der Umgebung aus **ASUS GX10 (ARM64)** und **Ubuntu 24.04 LTS** eine nach der anderen praktisch getestet; die vier Fähigkeitslinien Monitor, Injection, AP und WPA3-SAE werden auf einen Schlag vergleichend ausgezogen – und ehrlich gekennzeichnet, welche Karten „auf dieser Plattform etwas nicht können“.

Die Positionierung muss vorab klar sein: Alle Tests dieses Artikels wurden auf Yopiteks eigener Hardware und im eigenen Büro-WLAN durchgeführt, Testobjekte sind unsere eigenen Testgeräte. Es handelt sich um eine Hardware-Verifizierung der Produktkompatibilität und der Fähigkeitsgrenzen durch den Distributor, nicht um eine Angriffsanleitung gegen fremde Netzwerke. Der Artikel liefert keinerlei Schritte für Operationen an externen Netzwerken; die Injection- und Handshake-bezogenen Fähigkeiten werden ausnahmslos in einer eigenen, geschlossenen Umgebung und an eigenen Geräten gemessen.

Dies ist ein Hub-Artikel im Gesamttabellen-Format. Die schrittweise Konfiguration und die vollständigen Belege jeder einzelnen Karte werden gesondert in Einzelkarten-Detailartikeln aufgeschlüsselt (siehe weiterführende Literatur am Ende).

## Testplattform und Methode

- **Rechenplattform**: ASUS GX10 (ARM64 / aarch64)
- **Betriebssystem**: Ubuntu 24.04 LTS
- **Kernel-Version**: kernel 6.17.0-1014-nvidia
- **Treiberstrategie**: Alle 9 Karten nutzen den kernel-internen (in-kernel) Treiber, direkt nach dem Einstecken erkannt, ohne Installation irgendeines Drittanbieter-DKMS-Moduls
- **Testgerät**: Apple iPhone 7 Plus (WPA3-SAE-Kompatibilität zusätzlich mit iPhone 15 Pro nachgemessen)
- **Testumgebung**: eigenes Büro-WLAN, SSID `YUPITEK`, 2,4 GHz ch5 / 5 GHz ch36, ch157
- **Testzeitraum**: Messungen an echter Hardware vom 2026-11-16 bis 2026-11-18

Methodisch durchlief jede Karte denselben Ablauf: zuerst Treiberladung und Schnittstellen-Entstehung bestätigen (`wlx*`), dann der Reihe nach Monitor, Injection, AP und WPA3-SAE-Verbindung in 2,4 GHz / 5 GHz verifizieren und zuletzt die End-to-End-Handshake-Erfassungskette gegen das eigene Testgerät abnehmen. Jedes Ergebnis wird mit dem tatsächlich gemessenen Wert oder Zustand protokolliert, nicht aus dem Datenblatt abgeleitet.

Die Tabellen dieses Artikels verwenden die folgende Legende:

> ✅ bestanden | 🟡 teilweise oder im Einzelbetrieb möglich | ⚠️ mit Einschränkung | ❌ nicht unterstützt oder Test fehlgeschlagen | N/A Treiber kennt diesen Modus nicht | ⬜ nicht getestet (zweites Gerät fehlt)

## I. Hardware- und Treiberübersicht

Zuerst die Hardware-Details der 9 Karten und der auf kernel 6.17 tatsächlich geladene Treiber.

| # | Modell | Chip | USB ID | Treiber (in-kernel) | Firmware | Generation / Streams | Anmerkung |
|---|---|---|---|---|---|---|---|
| 1 | **AWUS036ACM** | MediaTek MT7612U | — | `mt76x2u` | — | Wi-Fi 5 / 2T2R | von morrownr empfohlene Kali-Karte |
| 2 | **AWUS036ACHM** | MediaTek MT7610U | — | `mt76x0u` | — | Wi-Fi 5 / 1T1R (AC600) | Einzelantenne |
| 3 | **AWUS036ACH** | Realtek RTL8812AU | `0bda:8812` | `rtw88_8812au` | — | Wi-Fi 5 / 2T2R (AC1200) | Doppelantenne mit hohem Gewinn |
| 4 | **AWUS036ACS** | Realtek RTL8811AU | `0bda:0811` | `rtw88_8821au` | 42.4.0 | Wi-Fi 5 / 1x1 | leicht und mobil |
| 5 | **AWUS036EACS** | Realtek RTL8821CU | `0bda:c820` | `rtw88_8821cu` | 24.11.0 | Wi-Fi 5 / 1x1 | BT + WiFi kombiniert |
| 6 | **AWUS036AX** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | — |
| 7 | **AWUS036AXER** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | gleicher Chip, eingebettete Antenne (Nano) |
| 8 | **AWUS036AXM** | MediaTek MT7921AU | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | — |
| 9 | **AWUS036AXML** | MediaTek MT7921AUN | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | + BT |

Einige Kernpunkte:

**Zwei große Treiberlager.** Die 9 Karten verteilen sich auf zwei in-kernel-Treibersätze: MediaTek (`mt76x2u` / `mt76x0u` / `mt7921u`) und Realtek (`rtw88_*` / `rtw89_8852bu`). Die Chip-Generationen umfassen Wi-Fi 5 (6 Karten) und Wi-Fi 6 (3 Karten: AX, AXER über `rtw89_8852bu`; AXM, AXML über `mt7921u`).

**Der praktischste Vorteil unter ARM64 ist „ohne Kompilieren“.** Diese 9 Karten nutzen auf kernel 6.17 allesamt in-kernel-Treiber, werden direkt nach dem Einstecken erkannt und erfordern unter aarch64 keine Out-of-Tree-DKMS-Module. Das macht sich unter ARM64 besonders bemerkbar: Vielen Realtek-Drittanbietertreibern fehlt das aarch64-Prebuild, sie müssen oft aus dem Quellcode gegen die Kernel-Version kompiliert werden, mit hoher Fehlerwahrscheinlichkeit. Diese Kartencharge erspart genau diesen Ablauf.

**Gleicher Chip, unterschiedliches Modell.** Der AWUS036AX und der AWUS036AXER verwenden denselben RTL8832BU und denselben `rtw89_8852bu`-Treiber, der Unterschied liegt im Antennendesign (AXER mit eingebettetem Nano-Antennendesign, ohne RP-SMA), was sich in den späteren Empfangs- und Injektionszahlen widerspiegelt.

**Zwei Karten sind BT-+-WiFi-Kombigeräte.** Der AWUS036EACS (RTL8821CU) und der AWUS036AXML (MT7921AUN) bringen zugleich Bluetooth mit; diese Eigenschaft hat beim erneuten Einstecken einen praktischen Nebeneffekt, der später unter „Hinweise zur Plattform“ erläutert wird.

## II. Zentrale Fähigkeitsmatrix: Monitor / Injection / AP / WPA3

Dies ist die Haupttabelle des Artikels und zugleich die, die man bei der Auswahl zuerst ansehen sollte.

| # | Modell | Monitor 2.4G | Monitor 5G | **Injection 2.4G** | **Injection 5G** | AP 2.4G | AP 5G | WPA3-SAE |
|---|---|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ | ✅ | ✅ 63–83% | ✅ 76% | ✅ | ✅ 80MHz | ✅ 2.4G |
| 2 | AWUS036ACHM | ✅ | ✅ | ✅ 96–100% | ⚠️ nur Broadcast | ✅ | ✅ | ✅* 2.4G |
| 3 | AWUS036ACH | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ | ✅ 2.4G |
| 4 | AWUS036ACS | ✅ | ✅ | ✅ **100%** | ✅ 96% | ✅ | ✅ (802.11a, 20 MHz; VHT80 nicht getestet) | ✅ 5G |
| 5 | AWUS036EACS | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ (802.11a, 20 MHz; VHT80 nicht getestet) | ✅ 2.4G |
| 6 | AWUS036AX | ✅ stark | ✅ stark | ✅ 96% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 7 | AWUS036AXER | ✅ stark | ✅ stark | ✅ 73% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 8 | AWUS036AXM | ✅ schwach | ✅ schwach | ❌ **fehlgeschlagen** | ❌ **fehlgeschlagen** | ✅ | ✅ 80MHz | ✅ 2.4G |
| 9 | AWUS036AXML | ✅ schwach | ✅ schwach | ❌ **fehlgeschlagen** | ❌ **fehlgeschlagen** | ✅ | ✅ 80MHz | ✅ 2.4G / 6G |

> \* Beim AWUS036ACHM muss für WPA3 `sae_pwe=0` gesetzt werden; bei `sae_pwe=2` kann sich das iPhone 7 Plus nicht verbinden.
>
> WPA3-SAE-Spalte: Angegeben ist das tatsächlich getestete Band (2,4G bei allen Karten außer dem ACS, getestet auf 5G; der AXML zusätzlich auf 6G). Andere Bänder wurden nicht getestet.

Punkt für Punkt:

**Monitor: Alle 9 Karten nutzbar, Unterschied in der Empfangsstärke.** Ob 2,4 GHz oder 5 GHz – alle 9 Karten können ohne Ausnahme in den Monitor-Modus. Der Unterschied liegt in der Aktivität beim Scannen und der Empfangsempfindlichkeit: Die Wi-Fi-6-Karten AX / AXER empfangen am stärksten und scannen am aktivsten; die MT7921-Karten AXM / AXML können in den Monitor-Modus, sind aber relativ schwach. Wer nur passives Mithören oder eine Spektrum-Bestandsaufnahme braucht, kann alle 9 Karten verwenden.

**Injection: Hier beginnt der Abstand aufzugehen.** Die Realtek-`rtw88`-Serie schneidet am besten ab: ACH und EACS erreichen in 2,4 GHz / 5 GHz jeweils **100 %**, ACS liegt bei 2,4 GHz 100 % / 5 GHz 96 %. Der MediaTek-`mt76`-ACM ist nutzbar, aber die Zahlen liegen im Mittelfeld (2,4 GHz 63–83 %, 5 GHz 76 %); der ACHM kann in 5 GHz nur senden (Broadcast) und keine Injektion gegen ein bestimmtes Ziel. Die `rtw89`-Karten AX / AXER können injizieren, wobei die 2,4-GHz-Injektionsrate des AXER (73 %) deutlich niedriger liegt als die des AX (96 %).

**Die wichtigste ehrliche Einschränkung: Die MT7921-Injektion (AXM / AXML) schlägt auf dieser Plattform fehl.** Das liegt weder an falsch eingestellten Parametern noch daran, dass der Chip prinzipiell nicht injizieren könnte – die Hauptursache ist die mac80211-chanctx-Regression in kernel 6.16+; dieselben Modelle laufen in der Community zwar mit git-/patched-Treibern, doch die Firmware sperrt dann die Datenrate (entsprechend morrownr/USB-WiFi #387, morrownr/mt76 #18). Da die Injektion auf dieser Plattform fehlschlägt, können diese beiden Karten kein deauth durchführen und damit die Handshake-Erfassungskette nicht zu Ende bringen. Für Einsatzzwecke, die Injektion erfordern, sind diese beiden Karten auf dieser Plattform direkt auszuschließen.

**AP und WPA3: fast vollständig bestanden.** Alle 9 Karten können als AP dienen, die meisten unterstützen 5 GHz VHT80 (80 MHz); auch die WPA3-SAE-Verbindung lässt sich bei allen auf dem getesteten Band herstellen (siehe Hinweis unter der Tabelle). Das Einzige, worauf zu achten ist, ist der AWUS036ACHM: Für WPA3 muss die hostapd-Option `sae_pwe` auf 0 gesetzt werden, sonst kann sich das ältere iPhone 7 Plus nicht verbinden (mit dem iPhone 15 Pro nachgemessen klappt die Verbindung, es handelt sich um einen Kompatibilitäts-Einstellungsunterschied).

## III. Zusammenfassung erweiterter Funktionen und Handshake-Fähigkeit

Eine Ebene tiefer betrachten wir End-to-End-Handshake, virtuelle Schnittstellen (VIF), active monitor und Mesh / IBSS.

| # | Modell | WPA-Handshake-Erfassung | VIF | Active monitor | Ad-hoc (IBSS) | Mesh (802.11s) |
|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ **End-to-End** (.22000) | ✅ STA+AP / AP+mon | 🟡 konfigurierbar, ACK nicht verifiziert | 🟡 Einzelbetrieb | 🟡 Einzelbetrieb |
| 2 | AWUS036ACHM | ✅ **End-to-End** (.22000, auf 5 GHz ch36) | ✅ | 🟡 | 🟡 Einzelbetrieb | 🟡 Einzelbetrieb |
| 3 | AWUS036ACH | ✅ **End-to-End** (.22000) | ✅ STA+mon | ❌ -95 | 🟡 Einzelbetrieb | ❌ -95 |
| 4 | AWUS036ACS | ✅ **End-to-End** (.22000) | ✅ | ❌ -95 | ❌ | ❌ -95 |
| 5 | AWUS036EACS | ✅ **End-to-End** (.22000, 79 ACKs) | 🟡 passiver monitor + managed auf demselben Kanal (Software-monitor); keine unabhängigen doppelten VIFs | ❌ -95 | ❌ | ❌ -95 |
| 6 | AWUS036AX | ✅ **End-to-End** (.22000) | ✅ STA+AP | N/A | N/A | N/A |
| 7 | AWUS036AXER | ✅ **End-to-End** (.22000) | ✅ STA+AP | N/A | N/A | N/A |
| 8 | AWUS036AXM | ❌ Injektion fehlgeschlagen | ✅ | 🟡 | N/A | N/A |
| 9 | AWUS036AXML | ❌ Injektion fehlgeschlagen | ✅ | 🟡 | N/A | N/A |

Das „End-to-End“ hat hier eine klare Definition: mit der jeweiligen Karte eine Injektion gegen das **eigene iPhone 7 Plus von Yopitek** (verbunden mit der eigenen `YUPITEK`-SSID) durchführen, den vollständigen 4-Way-Handshake (M1–M4) erfassen und ihn dann mit `hcxpcapngtool --all` in das hashcat-Format `.22000` umwandeln. Ob die gesamte Kette durchläuft, ist der Abnahmepunkt für „Penetrationstest-Fähigkeit“, nicht schon das bloße „in den Monitor-Modus wechseln können“.

- **End-to-End bestanden (7 von 9 Karten)**: ACM, ACHM, ACH, ACS, EACS, AX und AXER können alle eine `.22000` erzeugen, wobei EACS 79 ACKs empfing und die solideste Signalrückmeldung lieferte; ACH injiziert in beiden Bändern 100 % und wurde am 2026-11-19 nachgemessen, mit Export einer `.22000` von 47 Hashlines. Der ACHM hat es auf 5 GHz (ch36) geschafft; der ACM hat es trotz niedrigerer Injektionserfolgsrate geschafft.
- **End-to-End-Kette unterbrochen**: AXM / AXML – da die Injektion fehlschlägt, bricht die gesamte Handshake-Kette mit ab. Das bestätigt erneut: MT7921 eignet sich auf dieser Plattform nicht für Penetrationstest-Zwecke.
- **VIF (Koexistenz virtueller Schnittstellen)**: Alle 9 Karten unterstützen die Koexistenz mehrerer Schnittstellen in irgendeiner Form; Realtek rtw89 kann STA + AP gleichzeitig fahren, der EACS dagegen nur einen passiven monitor neben einer managed-Schnittstelle auf demselben Kanal (Software-monitor), keine unabhängigen doppelten VIFs.
- **Active monitor (mit ACK-Rückmeldung)**: Die `rtw88`-Karten ACH / ACS / EACS melden -95 (nicht unterstützt); bei den `rtw89`-Karten AX / AXER kennt der Treiber diesen Modus nicht (N/A); `mt76` / `mt7921u` sind teilweise möglich (🟡).
- **Mesh (802.11s)**: Nur die `mt76`-Karten ACM / ACHM können es im Einzelbetrieb aufbauen (🟡, für die vollständige Verbindungsverifikation ist eine zweite Karte nötig); Realtek `rtw88` meldet -95 (nicht unterstützt), bei `rtw89` und `mt7921u` kennt der Treiber diesen Modus nicht. Für Mesh-Experimente ist MediaTek `mt76` die einzige Option dieser Charge.
- **IBSS (Ad-hoc)**: Die `mt76`-Karten ACM / ACHM und die `rtw88`-Karte ACH können im Einzelbetrieb joinen (🟡); der EACS listet zwar den iftype, doch der Join ist im Test wirkungslos; die `rtw89`-Karten AX / AXER haben keinen IBSS-iftype (N/A).

### Kompatibilität auf Kali-/aircrack-Werkzeugebene (plattformübergreifend)

Die folgenden Werkzeuge zeigen auf allen 9 Karten ein plattformweites Verhalten, unabhängig von der einzelnen Karte:

| Werkzeug | Status | Erläuterung |
|---|---|---|
| airmon-ng | ✅ | bei allen Karten erkenn-/verwaltbar; **niemals `check kill`** (schaltet den NetworkManager ab und trennt den GX10 vom Netz) |
| kismet | ✅ | jede Karte kann als Data Source gestartet werden und erzeugt ein `.kismet`-Log |
| bettercap | ✅ | `wifi.recon` und channel hopper funktionieren normal |
| wifite (git 3.0.0) | ✅ | kann scannen und eine Zielliste aufbauen (git-Version nötig, apt-Version kollidiert mit dem selbst kompilierten aircrack-ng) |
| Wireshark / tshark | ✅ | Monitor-Erfassung und Analyse normal |
| **hcxdumptool 8.x** | ⚠️ | **bei allen Karten failed to arm, außer EACS auf 2,4 GHz (5 GHz scheitert)**: erfordert active-monitor, das `rtw88` / `rtw89` / `mt7921u` allesamt nicht unterstützen → stattdessen `airodump-ng` + `aireplay-ng` verwenden |

ARM64-Ergänzung: `aircrack-ng` muss aus dem Quellcode kompiliert werden, für `wifite` empfiehlt sich die git-Version 3.0.0, um den Abhängigkeitskonflikt zwischen apt-Paket und selbst kompilierter Version zu umgehen.

## IV. Auswahlempfehlung nach Einsatzzweck

Die obigen drei Tabellen auf „nach Zweck direkt auswählen“ verdichtet.

| Zweck | Erste Wahl | Erläuterung |
|---|---|---|
| **Penetrationstest (Injection + Handshake)** | **AWUS036EACS** / AWUS036ACS / AWUS036ACH | beste Dual-Band-Injektion (EACS, ACH erreichen 100 %); End-to-End-`.22000` belegt durch EACS, ACS, ACH (ACH am 2026-11-19 nachgemessen) |
| **Stärkster Empfang / Monitor über große Distanz** | **AWUS036AXER** / AWUS036ACH | AXER erfasst per Frequenzsprung in einem Durchgang 63 APs + 12 Clients; ACH mit Doppelantenne und hohem Gewinn |
| **Wi-Fi 6 + AP-Hotspot** | AWUS036AX / AWUS036AXER | 2x2 VHT80, AP stabil und Injektion nutzbar |
| **Reiner AP / normale Verbindung (keine Injektion nötig)** | AWUS036AXM / AWUS036AXML | MediaTek-Verbindung stabil, aber **Injektion schlägt fehl**, nicht für Penetrationszwecke geeignet |
| **Mesh- / IBSS-Experiment** | AWUS036ACM / AWUS036ACHM | Der `mt76`-Treiber kann im Einzelbetrieb Mesh und IBSS aufbauen (die `rtw88`-Karte ACH kann nur IBSS im Einzelbetrieb joinen, kein Mesh; `rtw89` deklariert beides nicht) |

Einige Sätze im Klartext:

- **Wer Penetrationstests machen und Handshakes erfassen will**: End-to-End-`.22000` mit Dateiablage belegt bei 7 von 9 Karten – **AWUS036EACS** (am solidesten, 79 ACKs), **AWUS036ACS**, die Wi-Fi-6-Karten AWUS036AX / AWUS036AXER, **AWUS036ACM** und **AWUS036ACHM** (5 GHz) sowie **AWUS036ACH** (Dual-Band-Injektion 100 %, am 2026-11-19 nachgemessen, mit Export einer `.22000` von 47 Hashlines).
- **Wer die größte Empfangsreichweite und das breiteste Mithören will**: AWUS036AXER (Wi-Fi 6, eingebettetes Nano-Antennendesign + Chip-Abstimmung, aktivster Frequenzsprung-Scan) oder der AWUS036ACH mit Doppelantenne und hohem Gewinn.
- **Wer einen Wi-Fi-6-Hotspot aufbauen will**: AWUS036AX / AWUS036AXER, 2x2 VHT80 und zugleich Injektion unterstützt.
- **Wer nur eine stabile Verbindung / einen schlichten AP will**: Die MediaTek-Lösung des AWUS036AXM / AWUS036AXML verbindet stabil, für den Alltag kein Problem.
- **Wer Mesh ausprobieren will**: In dieser Charge schaffen das nur die `mt76`-Karten AWUS036ACM / AWUS036ACHM (für IBSS im Einzelbetrieb kann zusätzlich die `rtw88`-Karte AWUS036ACH joinen).

**Fallstrick vermeiden (der wichtigste Punkt)**: Wenn Ihr Einsatzzweck **Injection oder Handshake** ist, **wählen Sie bitte nicht den AWUS036AXM / AWUS036AXML**. MT7921 schlägt auf dieser Plattform – ASUS GX10 (ARM64 / Ubuntu 24.04 / stock kernel 6.17) – bei der Injektion fehl; die Hauptursache ist die mac80211-chanctx-Regression in kernel 6.16+ (nicht chip-bedingt), kein Konfigurationsproblem; dieselben Modelle laufen in der Community zwar mit git-/patched-Treibern, doch die Firmware sperrt dann die Datenrate, sodass unter dem stock kernel dieser Plattform weiterhin keine Injektion möglich ist. Heben Sie diese Karten für Szenarien mit „reiner Verbindung / reinem AP“ auf.

## V. Hinweise zur Plattform (GX10 ARM64 in der Praxis)

Diese Punkte sind beim Betrieb dieser Kartencharge auf dem ASUS GX10 + Ubuntu 24.04 (ARM64) für alle 9 Karten gemeinsame Praxisregeln:

1. **Trennen Sie nicht Ihr eigenes Netzwerk**: Führen Sie auf keinen Fall `airmon-ng check kill` aus, es schaltet den NetworkManager ab und trennt den gesamten GX10 vom Netz. Bedienen Sie beim Arbeiten nur die externe `wlx*`-Schnittstelle und fassen Sie die interne Uplink-Hauptleitung nicht an.
2. **RX-Stall beheben**: Wenn nach wiederholtem Wechsel zwischen monitor / AP plötzlich nichts mehr gescannt wird, ist das meist ein RX-Stall; es genügt, die Karte einmal aus- und wieder einzustecken (USB-Neuaufzählung; der Schnittstellenname ist nach der MAC benannt und ändert sich nicht).
3. **BT-+-WiFi-Kombigeräte**: EACS und AXML bringen zugleich Bluetooth mit; beim erneuten Einstecken bleibt es gelegentlich beim WiFi-Probe hängen und es entsteht keine `wlx`-Schnittstelle; ein anderer USB-Port löst das meist.
4. **5-GHz-TX entsperren**: Vor der 5-GHz-Injektion in der eigenen Umgebung muss zuerst die korrekte Regulierungsdomäne (regulatory domain) gesetzt werden, um die TX-Leistung zu entsperren; nach dem Test auf die lokale Domäne zurücksetzen. Das ist die Voraussetzung dafür, ob 5 GHz überhaupt normal senden kann.
5. **Technik der Handshake-Erfassung**: Im Büro gibt es oft mehrere APs mit gleichem Namen; in der Praxis ist es stabiler, nicht auf eine einzelne BSSID zu fixieren, sondern den gesamten Kanal zu erfassen; für den Export `hcxpcapngtool --all` verwenden.
6. **hcxdumptool plattformweit failed to arm (Ausnahme: EACS auf 2,4 GHz)**: Weder die interne Tri-Band-Karte noch die genannten Treiber unterstützen active-monitor, daher direkt auf die aircrack-ng-Suite (`airodump-ng` + `aireplay-ng`) umsteigen.
7. **Kompilierdetails unter ARM64**: `aircrack-ng` muss aus dem Quellcode kompiliert werden, `wifite` in der git-Version verwenden, um apt-Abhängigkeitskonflikte zu umgehen.

Noch einmal die Positionierung betont: Die oben genannten Injection-/deauth-/Handshake-Fähigkeiten wurden allesamt in Yopiteks eigener, geschlossener Umgebung und an eigenen Testgeräten gemessen, mit dem Zweck, Produktfähigkeiten und Kompatibilitätsgrenzen zu verifizieren. Dieser Artikel liefert und empfiehlt keine solchen Operationen an irgendeinem fremden Netzwerk.

## Fazit

Auf der Plattform ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17) lässt sich die Gesamtbewertung der 9 ALFA-Karten auf drei Sätze verdichten: **Monitor bei allen nutzbar, AP und WPA3 fast durchweg bestanden, die Wasserscheide liegt bei der Injection.** Für professionelle Zwecke, die Injektion und Handshake erfordern, sind die Realtek-`rtw88`-Karten EACS / ACH / ACS die stabilste Wahl; für Empfang und Wi-Fi 6 schauen Sie auf AXER / AX; die MT7921-Karten AXM / AXML bleiben Szenarien mit reiner Verbindung vorbehalten. Durchweg ohne Kompilieren, direkt nach dem Einstecken einsatzbereit – das ist der größte gemeinsame Vorteil dieser Kartencharge unter ARM64.

## Häufig gestellte Fragen (FAQ)

**F: Kann der AWUS036AXM unter Ubuntu Injection (Injektion) durchführen?**
A: Auf dieser Plattform nicht. Im Test schlugen beim AWUS036AXM und AWUS036AXML (beide mit MT7921-Chip) die Injektionen in 2,4 GHz und 5 GHz fehl; die Hauptursache ist die mac80211-chanctx-Regression im stock kernel 6.16+ (nicht chip-bedingt), weshalb sie auf dieser Plattform nicht für Zwecke empfohlen werden, die Injektion oder Handshake-Erfassung erfordern.

**F: Welche ALFA-Karte hat unter Ubuntu die höchste Injektionserfolgsrate?**
A: Im Test erreichten der AWUS036ACH und der AWUS036EACS in 2,4 GHz und 5 GHz jeweils 100 % Injektionserfolgsrate – die beiden besten der 9 Karten dieser Charge.

**F: Benötigen die 9 ALFA-Karten unter Ubuntu 24.04 einen zusätzlichen Treiber?**
A: Nein. Alle 9 Karten nutzen auf kernel 6.17 ausschließlich kernel-interne (in-kernel) Treiber (rtw88- / rtw89- / mt76-Familie), werden direkt nach dem Einstecken erkannt und benötigen kein kompiliertes DKMS-Modul.

**F: Lässt sich mit einer ALFA-Karte unter Ubuntu ein WPA3-SAE-Hotspot aufbauen?**
A: Ja, alle 9 Karten konnten im Test erfolgreich einen WPA3-SAE-Hotspot aufbauen und Geräte verbinden lassen (getestet auf 2,4 GHz bei allen Karten außer dem ACS, der auf 5 GHz getestet wurde; der AXML zusätzlich auf 6 GHz); nur der AWUS036ACHM benötigt die hostapd-Option `sae_pwe` auf 0 gesetzt, sonst scheitert die Verbindung des älteren iPhone 7 Plus.

**F: Können Kali-Linux-Nutzer dieses Ubuntu-Testergebnis als Referenz heranziehen?**
A: Kali Linux basiert auf dem Debian-/Ubuntu-System und verwendet dieselben in-kernel-Treiber rtw88 / rtw89 / mt76, daher können die Treiberkompatibilität und die Fähigkeitsmatrix dieses Artikels grundsätzlich als Referenz für Kali-Nutzer dienen; die Testplattform dieses Artikels war jedoch Ubuntu 24.04 und wurde unter Kali noch nicht offiziell nachgemessen, maßgeblich sind daher spätere Nachmessungen.

## Weiterführende Literatur

Dieser Artikel ist der Gesamttabellen-Hub. Die folgenden Detailartikel und Einzelkartentests gehen nach und nach online (Links in Arbeit):

- „Ohne Treiberinstallation: Monitor- und AP-Modus unter Ubuntu (ARM64) aktivieren“ → [`/de/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/de/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- „WPA3-SAE-Handshake-Erfassung in der Praxis (in eigener Umgebung verifiziert)“ → [`/de/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/de/blog/alfa-wpa3-sae-handshake-capability-arm64/)

9 Einzelkarten-Detailtests:

- [AWUS036ACM Einzelkartentest](/de/blog/awus036acm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACHM Einzelkartentest](/de/blog/awus036achm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACH Einzelkartentest](/de/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- [AWUS036ACS Einzelkartentest](/de/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- [AWUS036EACS Einzelkartentest](/de/blog/awus036eacs-asus-gx10-ubuntu-test-report/)
- [AWUS036AX Einzelkartentest](/de/blog/awus036ax-asus-gx10-ubuntu-test-report/)
- [AWUS036AXER Einzelkartentest](/de/blog/awus036axer-asus-gx10-ubuntu-test-report/)
- [AWUS036AXM Einzelkartentest](/de/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- [AWUS036AXML Einzelkartentest](/de/blog/awus036axml-asus-gx10-ubuntu-test-report/)

---

*Testinstanz: Yopitek (ALFA-Network-Distributor Taiwan) | Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Testgerät: Apple iPhone 7 Plus (WPA3 zusätzlich iPhone 15 Pro) | Testumgebung: eigenes Büro-WLAN. Dieser Artikel dient der Verifizierung von Produktkompatibilität und -fähigkeit, nicht als Anleitung für Operationen an fremden Netzwerken.*
