---
title: "AWUS036ACHM im Einzelkartentest: MediaTek MT7610U Einzelantenne AC600 auf dem ASUS GX10 (ARM64 / Ubuntu 24.04) – Monitor-, Injection-, AP- und WPA3-Fähigkeiten"
slug: awus036achm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036achm-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036achm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036achm
  - alfa-network
  - mt7610u
  - mt76x0u
  - wifi-5
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - sae-pwe
  - ubuntu-24-04
  - arm64
description: "AWUS036ACHM (MT7610U) läuft unter Ubuntu 24.04 ohne Treiberinstallation; Dual-Band-Monitor-Modus nutzbar, 2,4G Paket-Injektion 96–100 %; für den AP muss 802.11n deaktiviert werden, für WPA3 muss sae_pwe=0 gesetzt werden, damit sich ältere iPhones verbinden."
faq:
  - question: "Benötigt der AWUS036ACHM unter Ubuntu 24.04 einen Treiber?"
    answer: "Nein. Der MT7610U wird vom kernel-internen Treiber mt76x0u übernommen; unter Ubuntu 24.04 (kernel 6.17) wird er direkt nach dem Einstecken erkannt – ohne DKMS, ohne zusätzliche Firmware; mit lsusb ist die USB-ID 0e8d:7610 zu sehen."
  - question: "Kann der AWUS036ACHM in den Monitor-Modus wechseln? Wie viele APs kann er erfassen?"
    answer: "Ja. Sowohl 2,4 GHz als auch 5 GHz können in den Monitor-Modus; mit airodump-ng im kanalhüpfenden Vollband-Scan über 120 Sekunden wurden im Test 19 APs und 14 Clients erfasst, verteilt auf ch1, 2, 5, 6, 36, 149, 157."
  - question: "Wie hoch ist die Paket-Injektionsrate des AWUS036ACHM? Funktioniert 5 GHz?"
    answer: "Auf 2,4 GHz Kanal 6 liegt die gerichtete Injektions-Antwortrate pro AP bei 96–100 % (aireplay-ng --test, 4 APs gefunden). Auf 5 GHz (ch36, ch149) wurde nur die Broadcast-Injektion als nutzbar bestätigt; der gerichtete Test meldet Found 0 APs, ein Prozentwert wurde in dieser Runde nicht ermittelt, die Ursache ist noch zu klären."
  - question: "Was tun, wenn das iPhone beim AP-Betrieb des AWUS036ACHM „Netzwerk kann nicht beigetreten werden“ oder „falsches Passwort“ anzeigt?"
    answer: "Deaktivieren Sie zuerst 802.11n: Fügen Sie der hostapd-Konfiguration nicht ieee80211n=1 und ht_capab hinzu; verwenden Sie für 2,4 GHz reines hw_mode=g und für 5 GHz reines hw_mode=a (20 MHz). Andernfalls erscheint in hostapd wiederholt handle_assoc_cb: STA not found; die Anzeige wirkt wie ein falsches Passwort, ist aber in Wirklichkeit ein fehlgeschlagener 802.11n-Assoziationsaufbau."
  - question: "Warum kann sich ein älteres iPhone nicht mit dem WPA3-SAE des AWUS036ACHM verbinden?"
    answer: "Meist liegt es an der sae_pwe-Einstellung von hostapd. Im Test verbanden sich bei sae_pwe=0 sowohl iPhone 7 Plus als auch iPhone 15 Pro; bei sae_pwe=2 assoziiert sich das iPhone 7 Plus zwar erfolgreich, trennt aber wegen eines fehlgeschlagenen 4-Way-Handshakes die Verbindung, was wie ein falsches Passwort aussieht. Kombinieren Sie dies mit ieee80211w=2 und lassen Sie das iPhone nach der Änderung das Netzwerk zunächst vergessen und sich dann neu verbinden."
draft: false
---

> Testinstanz: Yopitek (ALFA-Network-Distributor Taiwan) | Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia` | Testgerät: eigenes iPhone 7 Plus (WPA3 zusätzlich iPhone 15 Pro) | Testobjekt: eigenes Büro-WLAN (SSID `YUPITEK`, 2,4G ch5 / 5G ch36, 157).
>
> Dieser Artikel ist eine Hardware-Verifizierung der Produktkompatibilität und Fähigkeitsgrenzen durch den Distributor. Alle Monitor- / Injection- / AP- / WPA3-Tests wurden auf Yopiteks eigener Hardware, im eigenen Büro-WLAN und gegen eigene Testgeräte durchgeführt und stellen eine legitime Fähigkeitsverifizierung dar; sie richten sich gegen kein fremdes Netzwerk und liefern keine Anleitung zu Angriffsoperationen. Die Injektion im Text sendet nur Probe Requests zur Selbstprüfung der Fähigkeit, keine Angriffspakete.

## Kernaussagen (TL;DR)

Gemessen auf dem ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17): Der AWUS036ACHM beherrscht Dual-Band-Monitor-Modus, erreicht 96–100 % Paketinjektion auf 2,4G (auf 5G nur Broadcast-Injektion bestätigt) und betreibt einen AP-Hotspot auf beiden Bändern (802.11n muss deaktiviert werden).

- Ubuntu 24.04 ohne Treiberinstallation: Der MT7610U wird vom kernel-internen mt76x0u (kernel 6.17) übernommen, direkt nach dem Einstecken erkannt, ohne DKMS, ohne zusätzliche Firmware.
- Dual-Band-Monitor-Modus nutzbar; 2,4G Paket-Injektion 96–100 %.
- Auf 5 GHz wurde nur die Broadcast-Injektion bestätigt; die gerichtete Antwortrate pro AP wurde in dieser Runde nicht ermittelt (Ursache noch zu klären).
- Für den AP-Betrieb muss 802.11n deaktiviert werden; für WPA3 muss `sae_pwe=0` gesetzt werden, damit sich ältere iPhones verbinden.
- Einzelantenne 1T1R (AC600), Durchsatz und Positionierung liegen in einer anderen Klasse als die 2T2R-Modelle ACM / ACH.

## 1. Diese Karte und diese Plattform

Der AWUS036ACHM ist ALFAs Einzelantennen-AC600-Karte, Chip MediaTek MT7610U, zugehöriger Linux-interner Treiber `mt76x0u`. Sie ist das Single-Stream-Schwestermodell des AWUS036ACM (MT7612U, 2T2R): Spezifiziert als 1T1R (AC600), mit einem räumlichen Datenstrom weniger, dafür kompakter und mit dem von der Community anerkannten Fernbereichsempfang. Die Community morrownr/USB-WiFi führt sie in der Kali-Empfehlungsliste und in „The Short List“ und markiert VIF, Active monitor und WPA3 jeweils mit Yes, Very Long range, Single-Stream, in-kernel.

Wir haben sie an den ASUS GX10 (NVIDIA GB10, 128GB UMA, ARM64) angeschlossen und unter Ubuntu 24.04 LTS, kernel 6.17 Monitor, Injection, AP und WPA3-SAE Punkt für Punkt gemessen. Das Fazit vorweg: Diese Karte ist auf dieser Plattform nutzbar, und ihre 2,4-GHz-Fähigkeiten sind recht vollständig. Doch zwei Kompatibilitätsfallen sollten Sie vorab kennen: Für den AP-Betrieb muss 802.11n deaktiviert werden, für WPA3 muss `sae_pwe=0` gesetzt werden; außerdem wurde die gerichtete 5-GHz-Injektion in dieser Runde nur als Broadcast bestätigt. Die folgende Tabelle gibt einen Gesamtüberblick:

| Fähigkeit | 2,4 GHz | 5 GHz |
|---|---|---|
| Monitor (Mitschnitt) | ✅ | ✅ |
| Injection (Injektion) | ✅ 96–100 % | ⚠️ nur Broadcast nutzbar, gerichtete Antwortrate nicht ermittelt |
| AP-Hotspot | ✅ (nur reines 802.11g) | ✅ (nur reines 802.11a, 20 MHz) |
| WPA3-SAE | ✅ (erfordert `sae_pwe=0`) | Nicht getestet |

> Legende: ✅ im Test bestanden | 🟡 teilweise oder im Einzelbetrieb möglich | ⚠️ mit Einschränkung | ❌ nicht unterstützt oder fehlgeschlagen.

## 2. Hardware und Treiber (ohne Installation)

Nach dem Einstecken des ACHM am GX10 erkennt der im kernel 6.17 enthaltene `mt76x0u` die Karte direkt, ohne DKMS, ohne zusätzliche Firmware, ohne von GitHub einen Out-of-Tree-Treiber kompilieren zu müssen. Die drei Befehle zur Bestätigung der Karte:

```bash
lsusb | grep 0e8d:7610
# Bus 003 Device 005: ID 0e8d:7610 MediaTek Inc. WiFi

sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cababcd2
```

Der Schnittstellenname wird nach der MAC benannt (`wlx<MAC>`), bleibt beim erneuten Einstecken gleich und kann in Skripten direkt gebunden werden. Die von `iw phy info` deklarierten unterstützten Schnittstellenmodi umfassen `managed`, `AP`, `monitor`, `mesh point`, `IBSS`, `P2P-client`, `P2P-GO` und decken alle in diesem Artikel getesteten Szenarien ab.

Die beiden plattformübergreifenden Sicherheitsregeln gelten für den ACHM ebenso: Erstens niemals `airmon-ng check kill` ausführen – das schaltet den NetworkManager ab und trennt den GX10 nach außen vom Netz; zweitens durchgehend nur die `wlx*`-Schnittstelle bedienen und die interne `wlP9s9` (GX10-Uplink nach außen) nicht anfassen. Für Monitor / AP grundsätzlich `iw` zusammen mit `nmcli dev set $IF managed no` verwenden und die Haupt-Netzwerkkarte des Systems nicht berühren.

## 3. Getestete Fähigkeiten: Monitor / Injection / AP / WPA3

### 3-1. Monitor (2,4 + 5 GHz) ✅

Der Mitschnitt funktioniert in beiden Bändern normal. Auf 2,4 GHz Kanal 6 wurde in 8 Sekunden die Erfassungsobergrenze von 300 Paketen erreicht; auf 5 GHz je nach Frequenzaktivität unterschiedlich: ch36 (5180) in 8 Sekunden 300 erreicht, 5745 mit 254, 5785 mit 54 (wenige Pakete auf einem Kanal bedeuten meist, dass dort aktuell kein aktiver AP sendet, nicht ein Problem der Karte).

Ein kanalhüpfender Vollband-Scan zeigt die Empfangsstärke einer Einzelantennen-Karte am besten:

```bash
sudo timeout -s INT 120 airodump-ng --band abg $IF
```

Im Test wurden in 120 Sekunden 19 Basisstationen und 14 Clients erfasst, verteilt auf ch1/2/5/6/36/149/157. Für eine Single-Stream-AC600-Karte reicht diese Abdeckung aus, um als stabile Mitschnittquelle zu dienen, und bestätigt die „Very Long range“-Bewertung der Community.

### 3-2. Injection (2,4 + 5 GHz)

Hier liegt der auffälligste Unterschied des ACHM zwischen den beiden Bändern, und ein Punkt, auf den man bei der Auswahl besonders achten sollte.

Die Selbstprüfung der Fähigkeit mit `aireplay-ng --test` auf 2,4 GHz Kanal 6 liefert ein schönes Ergebnis:

```text
Injection is working!
Found 4 APs
30/30: 100%
```

Die Antwortrate der vier Basisstationen liegt bei 96–100 %, die Injektionsfähigkeit ist vollständig.

Doch beim Wechsel auf 5 GHz (ch36 und ch149 wurden beide probiert) sieht es anders aus:

```text
Injection is working!
Found 0 APs
```

Das heißt: Die Broadcast-Injektion auf 5 GHz ist nutzbar (der Treiber meldet `Injection is working!`), doch die gerichtete Antwortrate pro AP von `aireplay-ng --test` ist auf beiden 5G-Kanälen `Found 0 APs`; ein Prozentwert wurde in dieser Runde nicht ermittelt. Das ist das gemessene Verhalten dieser Einzelantennen-Karte ACHM auf dieser Plattform; die Ursache ist noch zu klären, und wir ergänzen keine nicht gemessene Zahl. Ehrlich gesagt: Wenn Ihr Einsatzzweck eine stabile gerichtete 5-GHz-Injektion erfordert, wurde beim ACHM in dieser Runde eine vollständige Injektionsrate nur auf 2,4 GHz bestätigt.

### 3-3. AP-Hotspot (2,4 + 5 GHz) ✅ — aber 802.11n muss deaktiviert werden

Hier liegt die erste Kompatibilitätsfalle des ACHM. Fügen Sie beim AP-Betrieb der hostapd-Konfiguration nicht `ieee80211n=1` und `ht_capab` hinzu: 2,4 GHz läuft über reines `hw_mode=g`, 5 GHz über reines `hw_mode=a` (20 MHz). Eine minimale funktionsfähige 2,4-GHz-Konfiguration sieht so aus:

```ini
interface=wlx00c0cababcd2
driver=nl80211
ssid=ALFA-TEST-ACHM-24
# reines 802.11g, kein ieee80211n=1 oder ht_capab hinzufügen
hw_mode=g
channel=6
country_code=TW
wmm_enabled=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=bitte-durch-eigenes-Passwort-mit-mind-8-Zeichen-ersetzen
```

Im Test verband sich das iPhone 7 Plus in beiden Bändern: Auf 2,4 GHz war `AP-STA-CONNECTED` gefolgt von `EAPOL-4WAY-HS-COMPLETED` zu sehen; auf 5 GHz (ch36, 20 MHz) wurden -71 dBm, rx 54 Mbit, `authorized: yes` gemessen.

Umgekehrt: Behält die Konfiguration `ieee80211n=1` bei, wirft hostapd wiederholt `handle_assoc_cb: STA not found`, das iPhone zeigt „Netzwerk kann nicht beigetreten werden“ oder „falsches Passwort“, doch das ist in Wirklichkeit ein fehlgeschlagener 802.11n-Assoziationsaufbau, kein Passwortproblem. Entfernen Sie einfach 802.11n. Der ACHM ist eine Einzelantennen-Karte; der 5-GHz-AP wurde in dieser Runde mit 20 MHz betrieben, VHT80 wurde nicht getestet.

### 3-4. WPA3-SAE ✅ — aber `sae_pwe=0` ist Pflicht (die am leichtesten übersehene Kompatibilitätsfalle)

Die zweite und am ehesten gesondert erwähnenswerte Kompatibilitätsfalle des ACHM. Bei WPA3-SAE steuert hostapd über `sae_pwe` die Herleitungsmethode des Password Element: `0` nutzt nur das klassische Hunting-and-Pecking, `1` nur Hash-to-Element (H2E), `2` beides parallel (sowohl Hunting-and-Pecking als auch H2E). Der Unterschied entscheidet unmittelbar darüber, ob sich ältere iPhones verbinden:

```ini
wpa=2
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
# WPA3 erzwingt PMF
ieee80211w=2
# entscheidend: kompatibel zu älteren Endgeräten wie dem iPhone 7 Plus
sae_pwe=0
sae_password=bitte-durch-eigenes-Passwort-ersetzen
```

Gegenüberstellung aus dem Test:

- `sae_pwe=0`: iPhone 15 Pro und iPhone 7 Plus **verbinden sich beide** (`authorized: yes`, `MFP: yes`).
- `sae_pwe=2`: Das iPhone 7 Plus **assoziiert sich erfolgreich, trennt aber wegen eines fehlgeschlagenen 4-Way-Schlüssel-Handshakes die Verbindung** und sieht oberflächlich wieder wie „falsches Passwort“ aus; das iPhone 15 Pro kann sich hingegen verbinden.

Das Fazit ist eindeutig: Um zu älteren iPhones (einschließlich Modellen von 2016 wie dem iPhone 7 Plus) kompatibel zu sein, muss hostapd zwingend `sae_pwe=0` setzen. Lassen Sie das iPhone nach der Änderung das Netzwerk zunächst „vergessen“ und sich dann neu verbinden, um Fehlanzeigen durch zurückgebliebene Assoziationszustände zu vermeiden. Dieser Punkt ist in der Gesamttabelle der 9 Modelle in der WPA3-Spalte des ACHM mit „✅*“ samt Sternchen besonders markiert.

## 4. Erweiterte Fähigkeiten und Grenzen

Zunächst fasst eine Tabelle den vollständigen Abdeckungsumfang und Status des ACHM in dieser Runde zusammen, danach werden die Schwerpunkte vertieft:

| Funktion | Status | Schwerpunkt des Tests |
|---|---|---|
| Monitor (2,4 + 5 GHz) | ✅ | Kanalhüpfen 120 s: 19 APs + 14 Clients erfasst |
| Injection 2,4 GHz | ✅ | Antwortrate 96–100 % |
| Injection 5 GHz | ⚠️ | Broadcast nutzbar, gerichtete Antwortrate nicht ermittelt |
| AP (2,4 + 5 GHz) | ✅ | iPhone in beiden Bändern verbunden, 802.11n muss deaktiviert werden |
| WPA3-SAE | ✅* | auf 2,4 GHz getestet (5 GHz nicht getestet); neue und alte iPhones verbinden sich, `sae_pwe=0` erforderlich |
| VIF (STA+AP, AP+monitor) | ✅ | online und zugleich Hotspot, Download 198 Mbit/s |
| WPA-Handshake-Erfassung | ✅ End-to-End (.22000, auf 5 GHz ch36) | Deauth des eigenen iPhone, vollständiger 4-Way M1–M4, Export als hashcat-`.22000` |
| Active monitor | 🟡 | Mitschnitt konfigurierbar, ACK nicht verifiziert |
| Ad-hoc (IBSS) | 🟡 | im Einzelbetrieb aufbaubar, nicht mit zweitem Gerät verbunden |
| Mesh (802.11s) | 🟡 | im Einzelbetrieb beitretbar, kein Peer-Link |
| Wi-Fi Direct (P2P) | ⬜ | zweites Gerät erforderlich, übersprungen |

> ✅* = WPA3-SAE nutzbar, aber `sae_pwe=0` erforderlich; siehe Abschnitt 3-4.

**VIF (virtuelle Schnittstellen, gleicher Kanal, max. 2 Schnittstellen).** Der ACHM unterstützt es, aus einer Karte mehrere gleichzeitig laufende Schnittstellen abzuspalten, sofern jede VIF eine andere MAC verwendet, die AP-VIF nicht dem NetworkManager übergeben wird und alle VIFs denselben Kanal nutzen; beim ACHM muss zudem beim AP 802.11n deaktiviert sein. Beide Kombinationen wurden getestet:

- **STA + AP (gleichzeitig online und Hotspot)**: Während sich das iPhone 7 Plus mit dem AP verbindet (-66 dBm, authorized), ist die Hauptschnittstelle mit YUPITEK verbunden, ping 30/30, avg 3,2 ms, Download 198 Mbit/s.
- **AP + Monitor**: Mitschnitt bei laufendem AP, in 8 Sekunden 300 Frames erfasst, darunter 46 Beacons des eigenen APs.

**Handshake-Erfassung.** Der ACHM hat die End-to-End-Kette auf 5 GHz (ch36) durchlaufen: Deauth des eigenen iPhone, Erfassung eines vollständigen 4-Way (M1–M4) und Export einer hashcat-`.22000`. Er gehört zu den 7 von 9 Karten mit End-to-End-Ergebnis (ACM, ACHM, ACH, ACS, EACS, AX, AXER). Die gerichtete Antwortrate der 5-GHz-Injektion (`aireplay-ng --test`) wurde weiterhin nicht ermittelt.

**Mesh / IBSS (im Einzelbetrieb aufbaubar).** Das ist der Unterschied der mt76-Familie gegenüber Realtek rtw88/rtw89. Das IBSS (Ad-hoc) meldet nach etwa 9 Sekunden `Joined IBSS` und kann Beacons aussenden; Mesh (802.11s) kann in den `type mesh point` wechseln und Mesh-Beacons aussenden. Beide kamen in dieser Runde nur im Einzelbetrieb zustande, ohne Verbindung mit einem zweiten Gerät (mangels zweitem Gerät übersprungen), daher die Markierung 🟡. Die Realtek-Karten rtw88/rtw89 (wie der AWUS036ACH) können auf dieser Plattform zwar ein Einzelgerät-IBSS aufbauen, unterstützen aber kein 802.11s-Mesh; für 802.11s-Mesh-Experimente sind die beiden mt76-Karten ACM und ACHM daher die wenigen verfügbaren Optionen.

**Active monitor 🟡.** Konfigurierbar, Mitschnitt funktioniert, doch das ACK-Antwortverhalten erfordert zur Verifizierung ein zweites Gerät und wurde in dieser Runde nicht verifiziert.

**Kali-Werkzeuge (Plattformebene, mit anderen Karten gemeinsam).** `airmon-ng`, `kismet`, `bettercap`, `wifite` (git-Version), Wireshark/tshark können den ACHM alle als Quelle verwenden; nur `hcxdumptool` meldet auf dieser Plattform `failed to arm interface` (Ausnahme: AWUS036EACS auf 2,4 GHz; der interne Treiber bietet keine active-monitor-Unterstützung); erfassen Sie daher mit `airodump-ng` zusammen mit der aircrack-ng-Suite. Unter ARM64 ist zusätzlich zu beachten: `aircrack-ng` hat oft kein Prebuilt-Package und muss aus dem Quellcode kompiliert werden; für `wifite` empfiehlt sich die GitHub-Version, um apt-Abhängigkeitskonflikte zu umgehen.

## 5. Einsatzszenarien und Auswahl (zurück zum Hub)

Stellt man den ACHM zurück in den Auswahlkontext der 9 Modelle, ist seine Position klar:

**Geeignet**

- **Mesh- (802.11s-)Experimente**: Der mt76-Treiber kann im Einzelbetrieb 802.11s-Mesh (und IBSS) aufbauen; Realtek-Karten können ein Einzelgerät-IBSS aufbauen, aber kein 802.11s-Mesh.
- **Single-Stream-Monitor-Mitschnitt über große Distanz**: Kanalhüpfen 120 s, 19 APs + 14 Clients erfasst, von der Community als Very Long range bewertet.
- **2,4-GHz-Injektion sowie AP- / WPA3-Hotspot**: 2,4G-Injektion 96–100 %, bei korrekt gesetztem WPA3 `sae_pwe=0` verbinden sich neue wie alte iPhones.

**Zu beachten (ehrliche Grenzen)**

- Die gerichtete 5-GHz-Injektion wurde in dieser Runde nur als Broadcast bestätigt, ohne Prozentwert.
- Für den AP-Betrieb muss 802.11n deaktiviert, für WPA3 `sae_pwe=0` gesetzt werden; sind beide Einstellungen falsch, sieht es beim alten iPhone jeweils „wie ein falsches Passwort“ aus.
- Einzelantenne 1T1R, Durchsatz und Positionierung liegen in einer anderen Klasse als die 2T2R-Modelle ACM / ACH.

**Auswahlhinweis**: Wenn Ihr Kernbedarf stabile Dual-Band-Injektion plus End-to-End-Handshake ist, sind unter den 9 Modellen AWUS036EACS / AWUS036ACH / AWUS036ACS passender; für Wi-Fi 6 + AP-Hotspot schauen Sie auf AWUS036AX / AWUS036AXER; wer vor allem Mesh- / IBSS-Einzelgerät-Experimente oder Mitschnitt über große Distanz will, für den ist der ACHM (oder sein 2T2R-Schwestermodell ACM) das richtige Werkzeug. Abschließend ein Warnhinweis: Wählen Sie für Injection- / Handshake-Zwecke nicht den AWUS036AXM / AXML – die MT7921-Injektion dieser beiden schlägt auf dieser Plattform fehl.

Die vollständige Matrix aus Hardware, Treiber, Monitor / Injection / AP / WPA3 aller 9 Modelle und die nach Einsatzzweck gegliederte Auswahl-Gesamtbewertung finden Sie in der Hub-Gesamttabelle: [9 ALFA-WLAN-Karten im Gesamttest-Matrix ARM64 / GX10](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Häufig gestellte Fragen (FAQ)

**F: Benötigt der AWUS036ACHM unter Ubuntu 24.04 einen Treiber?**
Nein. Der MT7610U wird vom kernel-internen Treiber mt76x0u übernommen; unter Ubuntu 24.04 (kernel 6.17) wird er direkt nach dem Einstecken erkannt – ohne DKMS, ohne zusätzliche Firmware; mit lsusb ist die USB-ID 0e8d:7610 zu sehen.

**F: Kann der AWUS036ACHM in den Monitor-Modus wechseln? Wie viele APs kann er erfassen?**
Ja. Sowohl 2,4 GHz als auch 5 GHz können in den Monitor-Modus; mit airodump-ng im kanalhüpfenden Vollband-Scan über 120 Sekunden wurden im Test 19 APs und 14 Clients erfasst, verteilt auf ch1, 2, 5, 6, 36, 149, 157.

**F: Wie hoch ist die Paket-Injektionsrate des AWUS036ACHM? Funktioniert 5 GHz?**
Auf 2,4 GHz Kanal 6 liegt die gerichtete Injektions-Antwortrate pro AP bei 96–100 % (aireplay-ng --test, 4 APs gefunden). Auf 5 GHz (ch36, ch149) wurde nur die Broadcast-Injektion als nutzbar bestätigt; der gerichtete Test meldet Found 0 APs, ein Prozentwert wurde in dieser Runde nicht ermittelt, die Ursache ist noch zu klären.

**F: Was tun, wenn das iPhone beim AP-Betrieb des AWUS036ACHM „Netzwerk kann nicht beigetreten werden“ oder „falsches Passwort“ anzeigt?**
Deaktivieren Sie zuerst 802.11n: Fügen Sie der hostapd-Konfiguration nicht ieee80211n=1 und ht_capab hinzu; verwenden Sie für 2,4 GHz reines hw_mode=g und für 5 GHz reines hw_mode=a (20 MHz). Andernfalls erscheint in hostapd wiederholt handle_assoc_cb: STA not found; die Anzeige wirkt wie ein falsches Passwort, ist aber in Wirklichkeit ein fehlgeschlagener 802.11n-Assoziationsaufbau.

**F: Warum kann sich ein älteres iPhone nicht mit dem WPA3-SAE des AWUS036ACHM verbinden?**
Meist liegt es an der sae_pwe-Einstellung von hostapd. Im Test verbanden sich bei sae_pwe=0 sowohl iPhone 7 Plus als auch iPhone 15 Pro; bei sae_pwe=2 assoziiert sich das iPhone 7 Plus zwar erfolgreich, trennt aber wegen eines fehlgeschlagenen 4-Way-Handshakes die Verbindung, was wie ein falsches Passwort aussieht. Kombinieren Sie dies mit ieee80211w=2 und lassen Sie das iPhone nach der Änderung das Netzwerk zunächst vergessen und sich dann neu verbinden.

## 6. Weiterführende Literatur

- [Hub-Gesamttabelle] Vollständige Monitor- · Injection- · AP-Matrix und Auswahl-Gesamtbewertung der 9 ALFA-WLAN-Karten auf dem ASUS GX10 (ARM64 / Ubuntu 24.04) → [/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Schwestermodell] AWUS036ACM (MT7612U / 2T2R) im Einzelkartentest — interner Link folgt (Platzhalter)
- [Plattform-Anleitung] Ohne Treiberinstallation: ALFA-WLAN-Karten-Monitor und -AP unter Ubuntu 24.04 + kernel 6.17 mit dem in-kernel-Treiber aktivieren — interner Link folgt (Platzhalter)
- [Schwerpunkt] Handshake-Erfassungsfähigkeit im WPA3-SAE-Zeitalter und die `sae_pwe`-Kompatibilitätsfalle — interner Link folgt (Platzhalter)

---

*Testinstanz: Yopitek (ALFA-Network-Distributor Taiwan) — https://www.yupitek.com | Testumgebung: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Testgerät: Apple iPhone 7 Plus (WPA3 zusätzlich iPhone 15 Pro). Die Daten stammen aus den Hardware-Testberichten vom 16.–18.11.2026, richten sich gegen kein fremdes Netzwerk und liefern keine Anleitung zu Angriffsoperationen.*
