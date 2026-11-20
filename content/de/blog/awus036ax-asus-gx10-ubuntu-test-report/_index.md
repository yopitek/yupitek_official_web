---
title: "ALFA AWUS036AX im Einzelkartentest: Wi-Fi-6-Monitor / Injection / AP-Fähigkeiten auf dem ASUS GX10 + Ubuntu 24.04 (Realtek RTL8832BU / rtw89_8852bu)"
slug: awus036ax-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ax-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ax
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - asus-gx10
  - ubuntu-arm64
description: "AWUS036AX (Wi-Fi 6) im Praxistest unter Ubuntu 24.04 ARM64: ohne Treiberinstallation, Monitor, 2,4G-Injektion 96 %, 5G-AP VHT80, WPA3-SAE, End-to-End-Handshake (.22000) bestanden; kein Support für IBSS / mesh. Plattform ASUS GX10, RTL8832BU."
faq:
  - question: "Benötigt der AWUS036AX unter Ubuntu 24.04 ARM64 einen Treiber? Was tun, wenn lsusb 0bda:1a2b anzeigt?"
    answer: "Auf dem in diesem Artikel getesteten kernel 6.17 (ASUS GX10) nicht: Der RTL8832BU wird vom kernel-internen rtw89_8852bu-Treiber übernommen, ohne Kompilieren, ohne DKMS. Wenn lsusb 0bda:1a2b anzeigt (CD-ROM-Modus), führen Sie sudo usb_modeswitch -v 0bda -p 1a2b -K aus, um in den WLAN-Modus zu wechseln."
  - question: "Unterstützt der AWUS036AX den Monitor-Modus und Paket-Injektion?"
    answer: "Ja. 2,4-GHz-Injektion 29/30 (96 %); der 5-GHz-Test gegen einzeln angegebene APs gibt Injection is working! zurück; airodump-ng findet beim Frequenzsprung-Scan über 60 Sekunden 14 APs und 4 Clients. Kein Support für active monitor, IBSS, mesh."
  - question: "Kann der AWUS036AX einen WPA-Handshake erfassen? Können die MT7921-Karten AXM / AXML das?"
    answer: "Der AX kann es: eigener AP plus eigenes iPhone 7 Plus, aireplay-ng -0 löst die Wiederverbindung aus, airodump-ng erfasst vollständig M1–M4, hcxpcapngtool exportiert die .22000. Die MT7921-Karten AXM / AXML scheitern auf dieser Plattform bei der Injektion und schaffen es nicht. Nur in eigenen oder autorisierten Netzwerken."
  - question: "Kann der AWUS036AX als AP-Hotspot dienen? Unterstützt er WPA3?"
    answer: "Ja. hostapd öffnet 2,4G- (802.11n) und 5G- (VHT 80 MHz) AP, das iPhone 7 Plus verbindet sich und zeigt VHT-NSS2 80 MHz; WPA3-SAE (ieee80211w=2, sae_pwe=0) mit dem iPhone 15 Pro auf 2,4 GHz verbunden, MFP: yes (WPA3 auf 5 GHz wurde nicht getestet)."
  - question: "Worin unterscheiden sich AWUS036AX und AWUS036AXER? Welchen soll man wählen?"
    answer: "Beide nutzen RTL8832BU + rtw89_8852bu, die Fähigkeitsmatrix ist identisch; der Unterschied liegt bei Antenne und Empfang: Der AXER hat eine abstimmungsstärkere Antenne und fand im selben Testdurchlauf beim Frequenzsprung 63 APs + 12 Clients (AX: 14 APs + 4 Clients). Für den festen Schreibtisch wählen Sie den AX, für große Distanz oder stärksten Empfang den AXER."
draft: false
---

**Kernaussagen (TL;DR)**: Laut Praxistest von Yopitek (ALFA-Network-Distributor Taiwan) läuft der AWUS036AX am ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17) ohne Treiberinstallation, mit Dual-Band-Monitor; 2,4G-Injektion 96 %, 5G-AP VHT80, End-to-End-.22000 bestanden, kein Support für IBSS / mesh.

> Dieser Artikel ist Yopiteks Kompatibilitäts- und Fähigkeits-Praxistest, durchgeführt auf **eigener Hardware, im eigenen Büro-WLAN (SSID `YUPITEK`), mit eigenem Testgerät**, Testobjekt ist der ALFA **AWUS036AX** (Realtek RTL8832BU, Wi-Fi 6 2x2).
> Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`; Vergleichsgerät Apple iPhone 7 Plus (WPA3 und VIF zusätzlich mit iPhone 15 Pro).
> ⚠️ **Rechtmäßige Nutzung**: Monitor und Injection nur in Netzwerken, die Ihnen gehören oder für die Sie eine Genehmigung haben; im AP-Modus halten Sie bitte die lokalen Funkvorschriften ein. Dieser Artikel umfasst keinerlei Angriffsoperationen gegen fremde Netzwerke.

---

## 1. Diese Karte und die Testplattform

Der AWUS036AX ist ALFAs Wi-Fi-6-(802.11ax-)USB-Karte dieser Generation, mit Realtek-RTL8832BU-Chip, 2x2 mit zwei räumlichen Datenströmen, Dual-Band 2,4 GHz und 5 GHz. In ALFAs Produktlinie teilt er sich mit der Variante mit externen Antennen, dem AWUS036AXER, denselben Chip und denselben Treiber; der Unterschied liegt in der Antennenform und im Empfangsgewinn. Gegenüber den ebenfalls zu Wi-Fi 6 zählenden MediaTek-Modellen AWUS036AXM / AXML ist es ein völlig anderer Chip-Pfad, und die Praxisergebnisse unterscheiden sich stark (Abschnitt 5 geht darauf ein).

Dieser Test behandelt keine theoretischen Datenblatt-Raten, sondern beantwortet nur die drei Dinge, die Distribution und Technikpraxis am meisten umtreiben: Lässt sie sich unter aktuellem Linux gut installieren? Welche Wireless-Fähigkeiten sind wirklich nutzbar? Welche kann der Treiber von Natur aus nicht, sodass man keine Zeit verschwenden sollte? Die Schlussfolgerungen sollen reproduzierbar sein, daher wurden alle Befehle am 18.11.2026 auf echter GX10-Hardware Zeile für Zeile durchgeführt; die „Testausgaben“ im Text sind echte Auszüge (MAC-Adressen mit `xx` maskiert).

Die Testgrenze zuerst klar gesagt: durchgehend im eigenen Büro, gegen das eigene `YUPITEK`-Netzwerk und das eigene Handy. Monitor erfasst nur Pakete der eigenen Umgebung, Injection und Handshake richten sich nur gegen den eigenen AP und das eigene iPhone. Ziel ist zu validieren, „was diese Karte auf dieser Maschine kann“, nicht einen Angriff auf fremde Netzwerke vorzuführen.

---

## 2. Hardware und Treiber (Wi-Fi 6, ohne Installation)

Der praktischste Vorteil dieser Generation ist: **direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS**. Der `rtw89_8852bu`-Treiber des RTL8832BU ist bereits ein in-kernel-Modul von kernel 6.17; der GX10 bindet ihn beim Booten, man muss kein Out-of-Tree-Projekt mehr von GitHub holen und manuell kompilieren.

Chip-Informationen und Validierungsschritte folgen. Zuerst mit `lsusb` bestätigen, dass die Karte im WLAN-Modus aufgezählt wird:

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
```

Erwartungsgemäß erscheint `ID 0bda:b832 Realtek Semiconductor Corp. 802.11ax WLAN Adapter`. Die Karte dieser Testinstanz zeigte sich direkt im WLAN-Modus, ohne im CD-ROM-Modus zu hängen; wenn Ihre Karte `0bda:1a2b` zeigt, steckt sie noch im CD-ROM-Modus – mit `sudo usb_modeswitch -v 0bda -p 1a2b -K` in den WLAN-Modus wechseln.

Anschließend das Laden von Treiber und Firmware bestätigen:

```bash
sudo dmesg | grep rtw89_8852bu | tail -3
```

Auf echter Hardware geladen wird `rtw89/rtw8852b_fw-1.bin`, firmware version `0.29.29.5`. Treiber und Firmware sind beide im Kernel enthalten, es muss kein weiteres Paket installiert werden.

Der letzte Schritt ist, zuerst klar zu sehen, **welche interface modes dieser Treiber deklariert** – dieser Schritt entscheidet direkt, welche Fähigkeiten später vorhanden und welche N/A sind:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Auf echter Hardware aufgelistet werden `managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO`. In der Liste fehlen IBSS, mesh point und active-monitor. Das ist keine falsche Konfiguration, sondern `rtw89_8852bu` hat diese drei Modi schlicht nicht implementiert; Abschnitt 4 kennzeichnet sie daher als N/A.

---

## 3. Getestete Fähigkeiten: Monitor / Injection / AP / WPA3

Zuerst eine Fähigkeits-Gesamttabelle; jede Zelle entspricht einem Testauszug weiter unten:

| Fähigkeit | 2,4 GHz | 5 GHz | Testauszug |
|---|---|---|---|
| **Monitor** | ✅ stark | ✅ stark | airodump findet beim 60-s-Frequenzsprung **14 APs + 4 Clients** |
| **Injection** | ✅ **96 %** | ✅ nutzbar | 2.4G `aireplay-ng --test` 29/30 (96 %); 5G einzeln `Injection is working!` |
| **AP-Hotspot** | ✅ 802.11n (HT) | ✅ **VHT 80 MHz** | iPhone 7 Plus verbindet: 2,4G MCS 12, 5G VHT-NSS2 80 MHz |
| **WPA3-SAE** | ✅ | Nicht getestet | iPhone 15 Pro verbindet, MFP: yes (`sae_pwe=0`); nur auf 2,4 GHz getestet |
| **WPA-Handshake-Erfassung** | ✅ **End-to-End** | — | deauth des eigenen iPhone → vollständiger 4-way erfasst → Export der hashcat-`.22000` |

**Monitor (Monitor-Modus / Empfang) ✅ stark.** Nach dem Wechsel in den monitor empfangen 2,4 GHz und 5 GHz beide große Mengen Pakete (je ca. 100 Pakete / 6 Sekunden). Mit `airodump-ng --band abg` beim 60-Sekunden-Frequenzsprung wurden im Test 14 APs plus 4 Clients gefunden; die Empfangsleistung ist auf dem Niveau der ALFA-Wi-Fi-5-Karten ACM / ACHM und weit besser als die beiden MediaTek-MT7921-Karten (AXM / AXML zeigen im Test schwächeren Empfang). Für Vor-Ort-Erkundung und Kanalbelegungs-Bestandsaufnahme ist der Empfang dieser Karte ausreichend.

**Injection (Paket-Injektion) ✅ nutzbar – auch dies ist der entscheidende Unterschied des AX gegenüber den MediaTek-Modellen.** In 2,4 GHz (ch6) ergibt `aireplay-ng --test` im Test `29/30: 96 %`, `Injection is working!`, Antwortrate 96 %. In 5 GHz (ch36) kann der Broadcast-Test `Found 0 APs` zurückgeben (moderne APs antworten nicht auf Broadcast-probe, was normal ist), aber der Test gegen eine einzeln angegebene AP-BSSID gibt `Injection is working!` zurück und bestätigt die Nutzbarkeit der 5-GHz-Injektion. Im Gegensatz dazu **scheitert die Injektion schlicht** beim ebenfalls zu Wi-Fi 6 gehörenden MediaTek AXM / AXML auf dieser Plattform (Hauptursache ist eine mac80211-chanctx-Regression ab Kernel 6.16; hinzu kommt, dass die Firmware die Injektionsrate auf 1/6 Mbit/s festlegt; das ist keine Grenze des Chips selbst); das ist bei der Auswahl unbedingt zu unterscheiden.

**AP-Hotspot ✅ in beiden Bändern öffenbar, 5 GHz erreicht VHT80.** Mit hostapd einen AP aufsetzen: 2,4 GHz mit 802.11n (`ieee80211n=1`, HT20), das iPhone 7 Plus zeigt nach dem Verbinden MCS 12, authorized; 5 GHz mit VHT 80 MHz (`vht_oper_chwidth=1`, `ht_capab=[HT40+]`), das iPhone 7 Plus zeigt nach dem Verbinden VHT-NSS2 80 MHz, authorized. Beide Bänder tragen den Client stabil, und die 80-MHz-Bandbreite wird tatsächlich erfolgreich ausgehandelt.

**WPA3-SAE ✅ (2,4 GHz; 5 GHz nicht getestet).** Setzt man `wpa_key_mgmt` des AP auf `SAE` und `ieee80211w=2`, verbindet sich im Test das iPhone 15 Pro, MFP (Management Frame Protection) zeigt yes. Hier ein Kompatibilitätsdetail: `sae_pwe` muss auf `0` (Hunting-and-Pecking) gesetzt werden, erst dann verbinden sich ältere iPhones.

**WPA-Handshake-Erfassung ✅ End-to-End erfolgreich.** Im eigenen `YUPITEK`-Netzwerk gegen das eigene iPhone 7 Plus den vollständigen Ablauf durchlaufen: monitor-seitig den Kanal mitschneiden → `aireplay-ng -0` sendet deauth und löst die Wiederverbindung aus → `airodump-ng` erfasst den vollständigen vierfachen Handshake (M1/M2/M3/M4) → mit `hcxpcapngtool` die hashcat-`.22000` exportieren. Weil die Injektion dieser Karte nutzbar ist, läuft die gesamte Kette durch; bei Karten mit fehlgeschlagener Injektion (wie AXM / AXML) bricht sie beim deauth-Schritt ab. Die in dieser Handshake-Erfassungskette genutzten gängigen Kali-Werkzeuge (aircrack-ng, hcxtools) laufen direkt unter Ubuntu 24.04 ARM64.

---

## 4. Erweitert und Grenzen (die N/A-Punkte des rtw89-Treibers)

Dieser Abschnitt sagt „die nutzbaren erweiterten Funktionen“ und „was der Treiber von Natur aus nicht kann“ auf einmal klar heraus, um vor Ort keine Zeit zu verschwenden.

| Funktion | Status | Erläuterung |
|---|---|---|
| **VIF (STA + AP parallel)** | ✅ | Hauptschnittstelle mit `YUPITEK` verbunden, zugleich AP-VIF geöffnet (ch36 VHT80), beide Schnittstellen parallel; STA-seitig ping 3,2 ms |
| **WPA-Handshake-Erfassung** | ✅ End-to-End | M1–M4 erfasst, `hcxpcapngtool` exportiert die `.22000` |
| **Active monitor** | **N/A** | `rtw89_8852bu` hat diesen Modus nicht (nicht in den supported modes von `iw phy`) |
| **Ad-hoc (IBSS)** | **N/A** | Treiber unterstützt es nicht |
| **Mesh (802.11s)** | **N/A** | Treiber unterstützt es nicht |
| **Wi-Fi Direct (P2P)** | ⬜ nicht getestet | Treiber deklariert Support, erfordert aber ein zweites Gerät, in dieser Runde übersprungen |

**VIF ✅.** Eine AP-virtuelle Schnittstelle erstellen (andere MAC, unmanage), die Hauptschnittstelle bleibt mit Wi-Fi verbunden, AP im selben Kanal geöffnet. Im Test ist die Hauptschnittstelle mit `YUPITEK` verbunden, während die AP-VIF in ch36 VHT80 läuft; beide Schnittstellen arbeiten parallel, STA-seitig ping 3,2 ms. Für das Szenario „einerseits online, andererseits Test-Hotspot öffnen“ machbar.

**Active monitor / IBSS / Mesh sind N/A, nicht defekt.** Diese drei Modi erscheinen nicht in den supported interface modes von `iw phy info` aus Abschnitt 2, das heißt, der Treiber `rtw89_8852bu` hat sie schlicht nicht implementiert. Ein Befehl wie `sudo iw dev $IF set type ibss` schlägt direkt fehl, und es gibt keine Lösung: Das lässt sich weder mit Parametern noch mit Firmware retten; wer diese drei Modi braucht, muss den Chip-Pfad wechseln (z. B. MediaTeks mt76 ACM / ACHM, die im Einzelbetrieb IBSS / mesh aufbauen können).

**Eine Einschränkung auf Plattformebene vorab: hcxdumptool meldet auf dem GX10 `failed to arm`.** Das ist kein AX-spezifisches Problem. `hcxdumptool 8.x` benötigt active-monitor, und da der GX10 eine interne Tri-Band-Karte hat, wird bei der USB-Kartenaufzählung leicht per `-I` fälschlich auf die interne phy gemappt; alle getesteten USB-Karten schlagen auf dieser Maschine beim arm fehl (einzige Ausnahme: AWUS036EACS auf 2,4 GHz). Die Praxis besteht darin, **stattdessen das aircrack-ng-Paket** (airodump-ng + aireplay-ng) für die Erfassung zu verwenden; da die Injektion dieser Karte nutzbar ist, läuft die gesamte Kette dennoch End-to-End durch (siehe Abschnitt 3).

**Sicherheitsregel (gemeinsam für die GX10-Plattform):** Führen Sie niemals `airmon-ng check kill` aus, es schaltet den NetworkManager ab und trennt den GX10 vom Netz; bedienen Sie beim Arbeiten nur die `wlx*`-Schnittstelle, fassen Sie die interne Uplink-Hauptkarte nicht an.

---

## 5. Einsatzszenarien und Auswahl (Wi-Fi-6-AP-Hotspot, zurück zum Hub)

Die Praxis-Schlussfolgerung in eine Auswahlempfehlung übersetzt: **Der Sweet Spot des AWUS036AX ist das Szenario „Wi-Fi 6 + AP-Hotspot“, das zugleich Injektionsfähigkeit braucht.**

| Zweck | Eignung des AWUS036AX | Erläuterung |
|---|---|---|
| Wi-Fi-6-AP-Hotspot / Edge-Zugang | ★ Erste Wahl | 2x2 VHT80 dual-band öffenbar, WPA3-SAE nutzbar |
| Injection + Handshake-Audit | ★ geeignet | 2,4G 96 %, 5G nutzbar, End-to-End-Erfassung erfolgreich |
| Stärkster Empfang / Monitor über große Distanz | ○ ausreichend, aber erste Wahl ist AXER | der AXER mit demselben Chip hat externe Antennen, stärkerer Empfang |
| mesh / IBSS-Experiment | ✗ ungeeignet | Treiber N/A, stattdessen mt76 ACM / ACHM wählen |

**Typischer Einsatz: als Wi-Fi-6-Hotspot, damit Edge-Geräte sich mit dem zentralen Hub verbinden.** Mit den getesteten AP- (VHT80) und VIF-Fähigkeiten lässt sich der GX10 mit dieser Karte als Wi-Fi-6-Zugangspunkt aufstellen; nachdem Edge-Geräte wie Testhandys und IoT-Sensoren sich verbunden haben, fließt der Verkehr über die Hauptschnittstelle zurück zum zentralen Hub (gateway). Der VIF-Test hat bereits belegt, dass „die Hauptschnittstelle verbindet sich zurück zum übergeordneten Netz“ und „nach unten einen AP öffnen“ parallel möglich sind, STA-seitig Latenz 3,2 ms; diese Topologie wurde auf dieser Plattform als machbar validiert. Für den Edge-Zugang noch moderne Verschlüsselung drauflegen, WPA3-SAE hinzufügen genügt.

**Auswahl-Warnung: Für Injection- / Handshake-Zwecke nicht den AWUS036AXM / AXML wählen.** Diese beiden sind zwar ebenfalls Wi-Fi 6 2x2 und der AP lässt sich öffnen, aber die MediaTek MT7921 **scheitert auf dieser Plattform bei der Injektion**, kann nicht deauthen und erfasst keinen Handshake. Wenn der Kunde nur eine reine Wi-Fi-6-AP- / normale Verbindungskarte will und Injection gar nicht berührt, sind die MediaTek-Modelle stabil und in Ordnung; sobald der Zweck aber Wireless-Audit berührt, sollte man den Realtek-AX (oder den AXER mit externen Antennen) wählen.

**Wie unterscheidet man ihn vom AXER mit demselben Chip?** Chip, Treiber und Fähigkeitsmatrix sind identisch; der AXER ist die Variante mit externen Antennen, Empfang und Monitor über große Distanz sind stärker (im selben Testdurchlauf fand der AXER beim Frequenzsprung 63 APs + 12 Clients). Für den festen Schreibtisch mit geringem Antennenbedarf den AX wählen; für Distanz und stärksten Empfang zum AXER greifen.

---

## Häufig gestellte Fragen (FAQ)

**F: Benötigt der AWUS036AX unter Ubuntu 24.04 ARM64 einen Treiber? Was tun, wenn lsusb 0bda:1a2b anzeigt?**
Auf dem in diesem Artikel getesteten kernel 6.17 (ASUS GX10) nicht: Der RTL8832BU wird vom kernel-internen rtw89_8852bu-Treiber übernommen, ohne Kompilieren, ohne DKMS. Wenn lsusb `0bda:1a2b` anzeigt (CD-ROM-Modus), führen Sie `sudo usb_modeswitch -v 0bda -p 1a2b -K` aus, um in den WLAN-Modus zu wechseln.

**F: Unterstützt der AWUS036AX den Monitor-Modus und Paket-Injektion?**
Ja. 2,4-GHz-Injektion 29/30 (96 %); der 5-GHz-Test gegen einzeln angegebene APs gibt `Injection is working!` zurück; airodump-ng findet beim Frequenzsprung-Scan über 60 Sekunden 14 APs und 4 Clients. Kein Support für active monitor, IBSS, mesh.

**F: Kann der AWUS036AX einen WPA-Handshake erfassen? Können die MT7921-Karten AXM / AXML das?**
Der AX kann es: eigener AP plus eigenes iPhone 7 Plus, `aireplay-ng -0` löst die Wiederverbindung aus, `airodump-ng` erfasst vollständig M1–M4, `hcxpcapngtool` exportiert die .22000. Die MT7921-Karten AXM / AXML scheitern auf dieser Plattform bei der Injektion und schaffen es nicht. Nur in eigenen oder autorisierten Netzwerken.

**F: Kann der AWUS036AX als AP-Hotspot dienen? Unterstützt er WPA3?**
Ja. `hostapd` öffnet 2,4G- (802.11n) und 5G- (VHT 80 MHz) AP, das iPhone 7 Plus verbindet sich und zeigt VHT-NSS2 80 MHz; WPA3-SAE (ieee80211w=2, sae_pwe=0) mit dem iPhone 15 Pro auf 2,4 GHz verbunden, MFP: yes (WPA3 auf 5 GHz wurde nicht getestet).

**F: Worin unterscheiden sich AWUS036AX und AWUS036AXER? Welchen soll man wählen?**
Beide nutzen RTL8832BU + rtw89_8852bu, die Fähigkeitsmatrix ist identisch; der Unterschied liegt bei Antenne und Empfang: Der AXER hat eine abstimmungsstärkere Antenne und fand im selben Testdurchlauf beim Frequenzsprung 63 APs + 12 Clients (AX: 14 APs + 4 Clients). Für den festen Schreibtisch wählen Sie den AX, für große Distanz oder stärksten Empfang den AXER.

---

## 6. Weiterführende Literatur

- „Fähigkeits-Gesamttabelle von 9 ALFA-WLAN-Karten auf ASUS GX10 + Ubuntu ARM64“ – Monitor / Injection / AP / Handshake aller Modelle auf einmal gegenübergestellt → [Gesamttabellen-Hub](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Ohne Treiberinstallation: Monitor und AP unter Ubuntu 24.04 + kernel 6.17 mit dem in-kernel-Treiber aktivieren](/de/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/) – gemeinsamer Konfigurationsablauf für rtw88 / rtw89 / mt76
- [AWUS036AXER im Einzelkartentest](/de/blog/awus036axer-asus-gx10-ubuntu-test-report/) – Variante mit demselben Chip und externen Antennen, Vergleich bei Empfang und Monitor über große Distanz
- [Praxistest der WPA3-SAE-Handshake-Erfassungsfähigkeit und sae_pwe-Kompatibilität](/de/blog/alfa-wpa3-sae-handshake-capability-arm64/) – die `sae_pwe`-Fallstricke bei der iPhone-Verbindung

---

*Testinstanz: Yopitek (ALFA-Distributor) — https://www.yupitek.com | Testumgebung: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 | Vergleichsgerät: Apple iPhone 7 Plus (WPA3 / VIF zusätzlich iPhone 15 Pro)*
