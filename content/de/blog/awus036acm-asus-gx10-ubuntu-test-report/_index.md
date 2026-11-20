---
title: "AWUS036ACM im Einzelkartentest: MediaTek MT7612U (mt76x2u) auf dem ASUS GX10 + Ubuntu 24.04 (ARM64) – Bericht zu Monitor / Injection / AP und Mesh-Fähigkeit"
slug: awus036acm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acm
  - mt7612u
  - mt76x2u
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - mesh
description: "AWUS036ACM (MT7612U) läuft unter Ubuntu 24.04 ARM64 ohne Treiberinstallation; Dual-Band-Monitor-Modus und aircrack-ng (in Kali gebräuchlich) sind nutzbar, Paket-Injektion 2,4G 63–83 %, 5G 76 %, mit Unterstützung für VIF und Einzelgerät-Mesh / IBSS."
faq:
  - question: "Benötigt der AWUS036ACM unter Ubuntu oder Kali einen Treiber?"
    answer: "Nein. Der MT7612U wird vom kernel-internen Treiber mt76x2u übernommen; unter Ubuntu 24.04 (kernel 6.17) wird er direkt nach dem Einstecken erkannt – ohne DKMS, ohne manuelles Flashen der Firmware. Die Testplattform war Ubuntu 24.04 ARM64; unter Kali gilt bei ausreichend neuem Kernel prinzipiell dasselbe, dies wurde jedoch nicht auf echter Kali-Hardware verifiziert."
  - question: "Kann der AWUS036ACM in den Monitor-Modus wechseln und Paket-Injektion durchführen? Wie hoch ist die Erfolgsrate?"
    answer: "Ja. Sowohl 2,4 GHz als auch 5 GHz können in den Monitor-Modus wechseln und normal mitschneiden; der aireplay-ng-Injektionstest ergab 2,4 GHz 63–83 % und 5 GHz 76 %, was unter den neun Karten im Mittelfeld liegt. Für durchgängig 100 % Injektion in beiden Bändern haben sich im Yopitek-Test AWUS036ACH und AWUS036EACS als beste Wahl erwiesen."
  - question: "Kann der AWUS036ACM gleichzeitig einen Hotspot öffnen und online gehen (VIF)?"
    answer: "Ja. Im Test funktionierten sowohl STA+AP (einerseits mit dem Uplink verbunden, andererseits Hotspot geöffnet) als auch AP+monitor (Hotspot geöffnet und gleichzeitig mitgehört) – hier zeigt sich die relativ vollständige Mehrschnittstellen-Parallelität des mt76-Treibers; der 5-GHz-Hotspot lässt sich bis VHT 80 MHz öffnen."
  - question: "Unterstützt der AWUS036ACM Mesh (802.11s) und IBSS?"
    answer: "Im Einzelbetrieb aufbaubar. Unter Ubuntu 24.04 / kernel 6.17 kann der AWUS036ACM 802.11s-Mesh- und IBSS- (Ad-hoc-)Schnittstellen aufbauen; da jedoch kein zweiter Knoten vorhanden war, wurde die Mehrknoten-Verbindung nicht verifiziert – belegt ist nur der Aufbau im Einzelbetrieb."
  - question: "Kann der AWUS036ACM einen WPA-Handshake erfassen?"
    answer: "Ja. Gegen das eigene AP und das eigene iPhone 7 Plus gelang der End-to-End-Durchlauf: Deauth, vollständige 4-Way-Erfassung (M1–M4) und Export einer hashcat-.22000 mit hcxpcapngtool --all. Nur in eigenen oder autorisierten Netzwerken."
draft: false
---

> Dieser Artikel ist Yopiteks Protokoll eines praktischen Kompatibilitäts- und Fähigkeitstests des ALFA AWUS036ACM auf einer aktuellen Linux-Plattform, gedacht zur Unterstützung der Produktauswahl.
> Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Alle Werte sind Auszüge aus Yopiteks Praxistests auf **eigener Hardware, im eigenen Büro-WLAN** (SSID `YUPITEK`, 2,4G ch5 / 5G ch36, ch157) gegen **eigene Testgeräte** (Apple iPhone 7 Plus; WPA3 zusätzlich mit iPhone 15 Pro nachgemessen).
> ⚠️ **Rechtlicher Hinweis und Geltungsbereich**: Monitor, Injection und Handshake-Erfassung erfolgen ausschließlich in Netzwerken und auf Geräten, die Ihnen gehören oder für die Sie eine Genehmigung haben; im AP-Modus halten Sie bitte die lokalen Funkvorschriften ein. Dieser Artikel konzentriert sich auf die Fähigkeiten, Kompatibilität und Konfiguration der Karte selbst und **umfasst keinerlei Angriffsoperationen gegen fremde Netzwerke**.

## Kernaussagen (TL;DR)

Yopitek (ALFA-Network-Distributor Taiwan) hat auf dem ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17) gemessen: Der AWUS036ACM beherrscht Dual-Band-Monitor-Modus, Paketinjektion mit 63–83 % auf 2,4G und 76 % auf 5G sowie AP-Hotspot auf beiden Bändern (5G mit VHT 80 MHz).

- Ubuntu 24.04 (ARM64) ohne Treiberinstallation: Der MT7612U wird vom kernel-internen mt76x2u (kernel 6.17) übernommen, direkt nach dem Einstecken erkannt, ohne DKMS.
- Dual-Band-Monitor-Modus nutzbar; Paket-Injektion 2,4G 63–83 %, 5G 76 %, im Mittelfeld der neun Karten.
- Im Einzelbetrieb lassen sich 802.11s-Mesh und IBSS aufbauen, mit VIF-Unterstützung (STA+AP, AP+monitor).
- Die WPA-Handshake-Erfassung läuft End-to-End (vollständiger 4-Way, Export als hashcat-`.22000`); der ACM gehört zu den 7 von 9 Karten, die dies geschafft haben.
- Für durchgängig 100 % Injektion in beiden Bändern empfiehlt sich stattdessen AWUS036ACH oder AWUS036EACS.

---

## 1. Diese Karte und die Testplattform

Der AWUS036ACM ist die MediaTek-Dual-Band-Karte der ALFA-Produktlinie, Chip MT7612U, Wi-Fi 5 (802.11ac), 2T2R mit zwei räumlichen Datenströmen, Dual-Band 2,4 GHz / 5 GHz. In morrownrs Liste ist sie seit Langem als empfohlene Kali-Karte geführt – nicht wegen der Durchsatzzahlen, sondern weil die `mt76`-Treiberfamilie unter Linux Monitor, Injection und Mehrschnittstellen-Parallelität (VIF) relativ vollständig unterstützt; experimentelle Modi wie 802.11s-Mesh lassen sich auf dieser Plattform ebenfalls nur im mt76-Lager überhaupt in Betrieb nehmen (Realtek-Karten können nur ein Einzelgerät-IBSS aufbauen, kein Mesh). Bei der Bewertung dieser Karte geht es also nicht um Geschwindigkeit, sondern um die Vollständigkeit des Fähigkeitsspektrums, darum, ob sich die mt76-Besonderheiten tatsächlich realisieren lassen, und darum, welche Punkte ehrlich als Grenzfälle gekennzeichnet werden müssen.

In dieser Runde wird dasselbe Betriebsszenario beibehalten: Die interne Netzwerkkarte des GX10 (`wlP9s9`) übernimmt die Anbindung nach außen, der AWUS036ACM läuft per USB extern und trägt nur die Testaufgaben; der Wechsel in den Monitor- oder AP-Modus berührt das Netzwerk des Hosts selbst nicht. Durchgehend wird nur die zur ALFA-Karte gehörige `wlx*`-Schnittstelle bedient, die interne Uplink-Karte wird nicht angefasst.

| Punkt | Inhalt |
|---|---|
| Modell | AWUS036ACM |
| Chip | MediaTek MT7612U (Wi-Fi 5 / 802.11ac, 2T2R Dual-Stream) |
| Treiber | `mt76x2u` (in-kernel, in kernel 6.17 enthalten) |
| Generation / Streams | Wi-Fi 5 / 2T2R |
| Anmerkung | von morrownr empfohlene Kali-Karte |
| Plattform | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| Testgerät | Apple iPhone 7 Plus (WPA3 zusätzlich iPhone 15 Pro) |
| Testumgebung | eigenes Büro-WLAN, SSID `YUPITEK`, 2,4G ch5 / 5G ch36, ch157 |

> Die Gesamttabelle dieser Runde führt für den AWUS036ACM keine USB-ID und keinen Firmware-Versionseintrag (als „—“ markiert); daher werden diese beiden Werte hier nicht spekuliert. Alle folgenden Fähigkeitsdaten richten sich nach den jeweiligen ACM-Zeilen der Gesamttabelle.

---

## 2. Hardware und Treiber (ohne Installation)

Diese Karte wird am GX10 direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS. Der MT7612U wird direkt vom im Mainline-Kernel enthaltenen Treiber `mt76x2u` übernommen, ohne dass ein Out-of-Tree-Projekt eingebunden oder ein Firmware-Blob manuell geflasht werden müsste. Für ARM64 ist das der praktischste Vorteil von mt76. Viele Realtek-Drittanbietertreiber haben unter aarch64 kein Prebuild und müssen selbst gegen die jeweilige Kernel-Version kompiliert werden; mt76 läuft in-kernel, ein Kernel-Upgrade bleibt also nicht an Treiberabhängigkeiten hängen.

Nach dem Einstecken wird die Schnittstelle als `wlx` + MAC benannt (z. B. `wlxXXXXXXXXXXXX`); der Name ist an die MAC gebunden, bleibt beim erneuten Einstecken gleich und eignet sich gut, um in Skripten fest zugewiesen zu werden. Die Treiberbindung und die Entstehung der Schnittstelle lassen sich mit den folgenden allgemeinen Prüfungen bestätigen (Schnittstellenname und phy-Nummer unterscheiden sich je nach Maschine):

```bash
# Schnittstellennamen der ALFA-Karte ermitteln (nur mit wlx beginnend, interne wlP9s9 unberührt)
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"

# Bestätigen, dass der gebundene Treiber mt76x2u ist
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# mt76x2u

# Die von dieser phy deklarierten unterstützten Schnittstellenmodi auflisten (bestimmt, welche Fähigkeiten später nutzbar sind)
iw phy "$(cat /sys/class/net/$IF/phy80211/name)" info | sed -n '/Supported interface modes/,/Band 1/p'
```

Nach dem Test dieser Runde sind die mit `mt76x2u` nutzbaren Schnittstellenmodi vollständiger als bei Realtek `rtw88`: Neben managed / AP / monitor lassen sich auch IBSS und mesh point im Einzelbetrieb aufbauen (siehe Abschnitt 4). Das ist die Grundlage dafür, dass der ACM später Mesh / IBSS im Einzelbetrieb fahren kann; die Realtek-Karten derselben Plattform (wie der AWUS036ACH) können zwar ebenfalls im Einzelbetrieb ein IBSS aufbauen, doch 802.11s-Mesh und active monitor kommen auf dieser Plattform nicht in Betrieb.

---

## 3. Getestete Fähigkeiten: Monitor / Injection / AP / WPA3

Zuerst die zentrale Fähigkeits-Gesamttabelle (aus Zeile 1 der Neun-Karten-Tabelle), danach Punkt für Punkt. Alle Punkte wurden am eigenen `YUPITEK`-AP + eigenem iPhone 7 Plus durchgeführt.

| Fähigkeit | 2,4 GHz | 5 GHz | Erläuterung |
|---|---|---|---|
| Monitor (Mithören/Empfang) | ✅ | ✅ | beide Bänder können in den Monitor-Modus und normal mitschneiden |
| Injection (Paket-Injektion) | ✅ 63–83 % | ✅ 76 % | Injektionserfolgsrate im Standard-Injektionstest |
| AP-Hotspot (hostapd) | ✅ | ✅ 80MHz | 5G bis VHT 80 MHz öffenbar |
| WPA3-SAE (AP-Seite) | ✅ | Nicht getestet | WPA3-SAE wurde nur auf 2,4 GHz getestet; 5 GHz nicht getestet |

### 3-1. Monitor (2,4 GHz + 5 GHz) ✅

Sowohl 2,4 GHz als auch 5 GHz können normal in den Monitor-Modus wechseln und Pakete mitschneiden – die unstrittigste Fähigkeit dieser Karte. Für eine 2T2R-Karte mit zwei Antennen ist der Mithörempfang in beiden Bändern stabil und reicht aus, um eine Kanalbestandsaufnahme vor Ort und eine Paketdiagnose zu tragen.

### 3-2. Injection (Paket-Injektion) ✅ (Mittelfeld-Niveau)

Gemessen mit dem Standard-Injektionstest liegt die Zuverlässigkeit der Paket-Injektion des AWUS036ACM bei 2,4 GHz bei 63–83 % und bei 5 GHz bei 76 %. Unter den neun Karten ist das Mittelfeld, deutlich unter Realtek RTL8812AU (AWUS036ACH, beide Bänder 100 %) und RTL8821CU (AWUS036EACS, beide Bänder 100 %), aber funktional vollständig und in der Praxis ausreichend. Der ACM kann injizieren, nur ist die Stabilität nicht die höchste der Klasse; wenn ein Kunde „maximale Injektionserfolgsrate“ an erste Stelle setzt, ist er nicht die erste Wahl (siehe Auswahl in Abschnitt 5).

Vor der 5-GHz-Injektion ist ein Konfigurationsdetail zu beachten: Die Standard-Regulierungsdomäne sperrt das aktive Senden in Teilen der UNII-Bänder; vor dem Test muss die Regulierungsdomäne daher auf eine Einstellung umgestellt werden, die das Senden erlaubt, und nach dem Test wieder auf die lokale Domäne zurückgesetzt werden (`iw reg set US` → Test → `iw reg set TW`). Das ist die Voraussetzung dafür, ob 5 GHz überhaupt normal senden kann, und hat nichts mit der Fähigkeit der Karte selbst zu tun.

### 3-3. AP-Hotspot und WPA3-SAE ✅

Der AWUS036ACM kann als AP dienen, in 2,4 GHz wie in 5 GHz, wobei 5 GHz zudem bis 80 MHz Bandbreite (VHT80) geöffnet werden kann. Nach Aktivierung von WPA3-SAE auf der AP-Seite (auf 2,4 GHz) kann sich das eigene Testgerät normal verbinden (WPA3 auf 5 GHz wurde nicht getestet).

Hier lohnt der Vergleich mit dem ebenfalls auf mt76 basierenden Einzelantennen-Modell AWUS036ACHM: Bei ACHM muss für WPA3 die hostapd-Option `sae_pwe` eigens auf 0 gesetzt werden, sonst kann sich das iPhone 7 Plus nicht verbinden. Der AWUS036ACM stieß in dieser Runde nicht auf diese Einschränkung, WPA3-SAE war direkt nutzbar.

---

## 4. Erweiterte Fähigkeiten: VIF / Mesh / IBSS im Einzelbetrieb und Grenzen

Eine Ebene tiefer betrachten wir Handshake, virtuelle Schnittstellen (VIF), active monitor und Mesh / IBSS. Dieser Abschnitt ist auch die Stelle, an der der AWUS036ACM sich von den Realtek-Karten absetzt.

| Erweiterter Punkt | ACM-Ergebnis | Erläuterung |
|---|---|---|
| WPA-Handshake-Erfassung | ✅ End-to-End (.22000) | Deauth des eigenen iPhone 7 Plus, vollständiger 4-Way M1–M4, Export als hashcat-`.22000` |
| VIF (Mehrschnittstellen-Parallelität) | ✅ STA+AP / AP+mon | gleichzeitig STA+AP oder AP+monitor möglich |
| Active monitor | 🟡 konfigurierbar, ACK nicht verifiziert | Modus aufbaubar, ACK-Antwortverhalten nicht verifiziert |
| Ad-hoc (IBSS) | 🟡 Einzelbetrieb | Schnittstelle im Einzelbetrieb aufbaubar, Verbindung erfordert zweites Gerät |
| Mesh (802.11s) | 🟡 Einzelbetrieb | Schnittstelle im Einzelbetrieb aufbaubar, Verbindung erfordert zweites Gerät |
| Wi-Fi Direct (P2P) | ⬜ zweites Gerät nötig | in dieser Runde nicht getestet |

### 4-1. VIF (Parallelität virtueller Schnittstellen) – die Stärke des ACM ✅

Diese Karte kann zwei virtuelle Schnittstellen gleichzeitig betreiben. In dieser Runde funktionierten im Test sowohl STA+AP (einerseits mit dem Uplink verbunden, andererseits Hotspot geöffnet) als auch AP+monitor (einerseits Hotspot geöffnet, andererseits mithörend) – geeignet für Szenarien wie „verbinden und gleichzeitig beobachten“ oder „mit einer Karte zugleich Client und Basisstation sein“. Hier zeigt sich die relativ vollständige Mehrschnittstellen-Parallelität des `mt76`-Treibers.

### 4-2. Mesh / IBSS „im Einzelbetrieb möglich“ – der entscheidende mt76-Unterschied 🟡

Der AWUS036ACM kann im Einzelbetrieb 802.11s-Mesh- und Ad-hoc- (IBSS-)Schnittstellen aufbauen; Realtek `rtw88` / `rtw89` (AWUS036ACH, AWUS036AX u. a.) können zwar ebenfalls im Einzelbetrieb ein IBSS aufbauen, unterstützen auf dieser Plattform jedoch kein 802.11s-Mesh. Wer also 802.11s-Mesh-Experimente machen will, hat mit einer mt76-Karte (ACM / ACHM) einen Ausgangspunkt, den Realtek-Karten nicht bieten.

Die Grenze ist klar zu kennzeichnen: In dieser Runde bestätigt ist „Schnittstelle im Einzelbetrieb aufbaubar“; die vollständige Mehrknoten-Verbindung erfordert noch eine zweite Karte / einen zweiten Knoten und wurde noch nicht durchgeführt, daher die Markierung 🟡 (Einzelbetrieb) statt ✅.

### 4-3. Ehrliche Fähigkeitsgrenzen

- **Handshake**: Der ACM hat die vollständige End-to-End-Kette durchlaufen (deauth des eigenen Geräts → Erfassung des vollständigen 4-Way M1–M4 → `hcxpcapngtool --all`-Export der hashcat-`.22000`), obwohl seine Injektionserfolgsrate (2,4G 63–83 % / 5G 76 %) niedriger ist als die der Realtek-Karten.
- **active monitor**: Der Modus lässt sich einrichten, doch das ACK-Antwortverhalten wurde in dieser Runde nicht verifiziert (Markierung 🟡). Damit zusammenhängend: Das Plattform-Werkzeug `hcxdumptool` 8.x meldet auf allen Karten außer dem AWUS036EACS auf 2,4 GHz `failed to arm` (es erfordert active-monitor, den die interne Tri-Band-Karte dieser Plattform und die aktuellen Treiber nicht bereitstellen), weshalb der ACM-Handshake-Ablauf auf `airodump-ng` + `aireplay-ng` umgestellt wurde.
- **Wi-Fi Direct (P2P)**: in dieser Runde nicht getestet, zweites Gerät erforderlich.

### 4-4. Hinweise zum Plattformbetrieb (GX10 ARM64, ACM-relevant)

1. **Trennen Sie nicht Ihr eigenes Netzwerk**: Führen Sie niemals `airmon-ng check kill` aus (das schaltet den NetworkManager ab und trennt den GX10 vom Netz); bedienen Sie nur `wlx*` und fassen Sie die interne Uplink-Karte `wlP9s9` nicht an.
2. **RX-Stall beheben**: Wenn nach wiederholtem Wechsel zwischen monitor / AP plötzlich nichts mehr gescannt wird, genügt es, die Karte **einmal aus- und wieder einzustecken** (USB-Neuaufzählung; der Schnittstellenname ist durch die MAC bestimmt und bleibt gleich).
3. **5-GHz-TX entsperren**: Vor der 5-GHz-Injektion die korrekte Regulierungsdomäne setzen, um die TX-Leistung zu entsperren, nach dem Test auf die lokale Domäne zurücksetzen.
4. **Handshake-Erfassungstechnik**: Im Büro gibt es oft mehrere APs mit gleichem Namen; in der Praxis ist es stabiler, nicht auf eine einzelne `--bssid` zu fixieren, sondern den gesamten Kanal zu erfassen; für den Export `hcxpcapngtool --all` verwenden.
5. **ARM64-Toolchain**: `aircrack-ng` muss aus dem Quellcode kompiliert werden; `wifite` in der git-Version 3.0.0 verwenden (umgeht apt-Abhängigkeitskonflikte).

Die Plattform-Kali-Werkzeuge (`airmon-ng`, `kismet`, `bettercap`, `wifite` git-Version, Wireshark / tshark) können den ACM alle normal als Data Source verwenden; die einzige Ausnahme ist das zuvor erwähnte, active-monitor erfordernde `hcxdumptool`.

---

## 5. Einsatzszenarien und Auswahl (zurück zum Hub)

Überträgt man die obigen Fähigkeiten auf die Produktpositionierung, ist die Rolle des AWUS036ACM eigentlich sehr klar: eine Wi-Fi-5-2T2R-Karte mit ausgewogenen Fähigkeiten, ohne Treiberinstallation und mit dem exklusiven mt76-Vorteil bei Mesh / IBSS / VIF. Wofür also sollte man sie einsetzen?

- **Erste Wahl für Mesh- (802.11s-)Experimente**: Unter diesen neun Karten können nur die mt76-Karten ACM / ACHM im Einzelbetrieb eine 802.11s-Mesh-Schnittstelle aufbauen; Realtek `rtw88` / `rtw89` können zwar ein Einzelgerät-IBSS aufbauen, unterstützen aber kein 802.11s-Mesh. Für Mesh-Experimente ist der ACM der richtige Ausgangspunkt.
- **Bedarf an VIF-Parallelität**: STA+AP und AP+monitor funktionieren beide, geeignet, um mit einer Karte zugleich Client und AP zu sein oder verbunden zu bleiben und zugleich mitzuhören.
- **Wert auf treiberfreien Betrieb**: In-kernel `mt76x2u`, ein Kernel-Upgrade bleibt nicht am Treiber hängen, unter ARM64 entfällt das lästige Kompilieren von Out-of-Tree-Modulen.
- **Szenarien, in denen er nicht die beste Lösung ist**: Wenn der Kernbedarf „höchste Injektionserfolgsrate“ lautet, ist die Injektion des ACM (2,4G 63–83 % / 5G 76 %) nicht die höchste der Klasse – dann empfiehlt sich stattdessen Realtek AWUS036EACS / ACH / ACS; wer stärksten Empfang / Monitor über große Distanz sucht, schaut auf AWUS036AXER / ACH.

Im Vergleich mit der eigenen Produktfamilie ergeben sich folgende Positionierungsunterschiede:

| Bedarf | Empfohlene Karte | Grund |
|---|---|---|
| Mesh- (802.11s-)Einzelgerät-Experiment | **AWUS036ACM** / AWUS036ACHM | Der `mt76`-Treiber kann im Einzelbetrieb 802.11s-Mesh aufbauen (Realtek nur Einzelgerät-IBSS, kein Mesh) |
| VIF-Parallelität (STA+AP / AP+mon) | **AWUS036ACM** | Mehrschnittstellen-Parallelität funktioniert |
| Durchgängig 100 % Dual-Band-Injektion / End-to-End-Handshake | AWUS036EACS, AWUS036ACH, AWUS036ACS | beste Dual-Band-Injektion, `.22000`-End-to-End belegt |
| Stärkster Empfang / Monitor über große Distanz | AWUS036AXER, AWUS036ACH | mehr Ziele durch Frequenzsprünge / hoher Gewinn durch Doppelantenne |

Auswahl in einem Satz: Wer Mesh / IBSS betreiben, VIF-Parallelität nutzen und zugleich treiberfrei warten möchte, für den ist der AWUS036ACM die passendste mt76-Karte dieser Charge; wer durchgängig 100 % Dual-Band-Injektion braucht, geht Richtung EACS / ACH. Den vollständigen Quervergleich aller neun Karten und die Auswahlentscheidung finden Sie im [Gesamtbewertungs-Hub der ALFA-WLAN-Karten (Neun-Karten-Tabelle)](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

---

## Häufig gestellte Fragen (FAQ)

**F: Benötigt der AWUS036ACM unter Ubuntu oder Kali einen Treiber?**
Nein. Der MT7612U wird vom kernel-internen Treiber mt76x2u übernommen; unter Ubuntu 24.04 (kernel 6.17) wird er direkt nach dem Einstecken erkannt – ohne DKMS, ohne manuelles Flashen der Firmware. Die Testplattform war Ubuntu 24.04 ARM64; unter Kali gilt bei ausreichend neuem Kernel prinzipiell dasselbe, dies wurde jedoch nicht auf echter Kali-Hardware verifiziert.

**F: Kann der AWUS036ACM in den Monitor-Modus wechseln und Paket-Injektion durchführen? Wie hoch ist die Erfolgsrate?**
Ja. Sowohl 2,4 GHz als auch 5 GHz können in den Monitor-Modus wechseln und normal mitschneiden; der aireplay-ng-Injektionstest ergab 2,4 GHz 63–83 % und 5 GHz 76 %, was unter den neun Karten im Mittelfeld liegt. Für durchgängig 100 % Injektion in beiden Bändern haben sich im Yopitek-Test AWUS036ACH und AWUS036EACS als beste Wahl erwiesen.

**F: Kann der AWUS036ACM gleichzeitig einen Hotspot öffnen und online gehen (VIF)?**
Ja. Im Test funktionierten sowohl STA+AP (einerseits mit dem Uplink verbunden, andererseits Hotspot geöffnet) als auch AP+monitor (Hotspot geöffnet und gleichzeitig mitgehört) – hier zeigt sich die relativ vollständige Mehrschnittstellen-Parallelität des mt76-Treibers; der 5-GHz-Hotspot lässt sich bis VHT 80 MHz öffnen.

**F: Unterstützt der AWUS036ACM Mesh (802.11s) und IBSS?**
Im Einzelbetrieb aufbaubar. Unter Ubuntu 24.04 / kernel 6.17 kann der AWUS036ACM 802.11s-Mesh- und IBSS- (Ad-hoc-)Schnittstellen aufbauen; da jedoch kein zweiter Knoten vorhanden war, wurde die Mehrknoten-Verbindung noch nicht verifiziert – belegt ist nur der Aufbau im Einzelbetrieb.

**F: Kann der AWUS036ACM einen WPA-Handshake erfassen?**
Ja. Gegen das eigene AP und das eigene iPhone 7 Plus gelang der End-to-End-Durchlauf: Deauth, vollständige 4-Way-Erfassung (M1–M4) und Export einer hashcat-.22000 mit hcxpcapngtool --all. Nur in eigenen oder autorisierten Netzwerken.

---

## 6. Weiterführende Literatur

- Vollständiger Fähigkeitsvergleich und Gesamtbewertung der neun ALFA-Karten → [Gesamtbewertungs-Hub der ALFA-WLAN-Karten (Neun-Karten-Tabelle)](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Ohne Treiberinstallation: Monitor / AP unter Ubuntu 24.04 + kernel 6.17 aktivieren (rtw88 / rtw89 / mt76 im Praxistest) (Platzhalter, Link in Arbeit)
- Schritt-für-Schritt-Anleitung zu WPA3-SAE und End-to-End-Handshake-Erfassung (Platzhalter, Link in Arbeit)
- Das ebenfalls auf mt76 basierende Einzelantennen-Modell → AWUS036ACHM im Einzelkartentest (Platzhalter, Link in Arbeit)

---

*Testinstanz: Yopitek (ALFA-Network-Distributor Taiwan) — https://www.yupitek.com | Testumgebung: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Testgerät: Apple iPhone 7 Plus (WPA3 zusätzlich iPhone 15 Pro)*
