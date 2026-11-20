---
title: "AWUS036ACH im Einzelkartentest: Realtek RTL8812AU Doppelantenne AC1200 auf dem ASUS GX10 (ARM64 / Ubuntu 24.04) – vollständiger Monitor- · Injection- · AP- · WPA3-Bericht"
slug: awus036ach-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ach-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ach
  - rtl8812au
  - rtw88-8812au
  - realtek
  - wifi-5
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - alfa-network
  - asus-gx10
  - arm64
description: "AWUS036ACH (RTL8812AU) läuft unter Ubuntu 24.04 / kernel 6.17 ohne DKMS; Dual-Band-Monitor-Modus nutzbar, Paket-Injektion 100 %, End-to-End-WPA-Handshake (.22000) nachgewiesen, inklusive Grenzen wie 5G-Empfangshänger."
faq:
  - question: "Benötigt der AWUS036ACH unter Kali oder Ubuntu einen Treiber?"
    answer: "Das hängt von der Kernel-Version ab. Linux-Kernel 6.13 und höher (hier getestet: Ubuntu 24.04 / kernel 6.17) bringt den Treiber rtw88_8812au bereits mit, er wird direkt nach dem Einstecken erkannt – ohne Kompilieren, ohne DKMS; nur unter Kernel unter 6.13 müssen Sie zusätzlich per DKMS lwfinger/rtw88 installieren. Prüfen Sie unter Kali zuerst mit uname -r die Kernel-Version; auf echter Kali-Hardware wurde dies nicht verifiziert."
  - question: "Wie schlagen sich Monitor-Modus und Paket-Injektion des AWUS036ACH?"
    answer: "Sowohl 2,4 GHz als auch 5 GHz können in den Monitor-Modus; die gerichtete aireplay-ng-Injektion pro AP liegt auf 2,4 GHz (gegen 4 APs) wie auf 5 GHz (gegen YUPITEK ch36) bei 30/30 = 100 %. Vor der 5-GHz-Injektion muss die Regulierungsdomäne auf eine Einstellung gesetzt werden, die das Senden erlaubt (z. B. iw reg set US); unter dem Standard country 00 ist das Senden auf 5 GHz gesperrt und die Injektion kommt nicht hinaus."
  - question: "Kann der AWUS036ACH einen WPA-Handshake erfassen?"
    answer: "Ja, und End-to-End ist nachgewiesen. Die Injektion liegt in beiden Bändern bei 100 %; am 19.11.2026 wurde ergänzend auf dem eigenen iPhone 15 Pro auf 5 GHz ch36 ein vollständiger 4-Way-Handshake erfasst und mit hcxpcapngtool in 47 hashcat-.22000-Hashlines exportiert. Nur in eigenen oder autorisierten Netzwerken."
  - question: "Was tun, wenn sich das iPhone 7 Plus nicht mit dem WPA3-Hotspot des AWUS036ACH verbinden kann?"
    answer: "hostapd muss sae_pwe=0 zusammen mit ieee80211w=2 setzen, erst dann verbindet sich das iPhone 7 Plus; mit sae_pwe=2 gelingt die Verbindung nicht. Dieselbe Einstellung ist auch beim AWUS036ACHM entscheidend."
  - question: "Was tun, wenn der 5-GHz-Empfang des AWUS036ACH plötzlich hängt (0 Pakete erfasst)?"
    answer: "Das ist ein bekanntes Verhalten von rtw88_8812au: Nach wiederholtem Moduswechsel oder Änderung der Regulierungsdomäne kann der 5-GHz-Empfang hängen bleiben und ist per Software nicht wiederherstellbar – es hilft nur physisches Aus- und Einstecken oder ein Neustart. Es empfiehlt sich, die Karte vor 5-GHz-Tests neu einzustecken und die 5-GHz-Punkte vorrangig abzuschließen."
draft: false
---

> Testinstanz: Yupitek (ALFA-Network-Distributor Taiwan) | Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Testgerät: eigenes Apple iPhone 7 Plus | Testobjekt: eigenes Büro-WLAN (SSID `YUPITEK`, 2,4G ch5 / 5G ch36, 157) | Testdatum: 18.11.2026.
>
> Dieser Artikel ist eine Hardware-Verifizierung der Produktkompatibilität und Fähigkeitsgrenzen durch den Distributor: Alle Monitor- / Injection- / AP- / Handshake-Messungen wurden auf Yupiteks eigener Hardware, im eigenen Büro-WLAN und gegen eigene Testgeräte durchgeführt; sie richten sich gegen kein fremdes Netzwerk und liefern keine Anleitung zu Angriffsoperationen gegen externe Netzwerke. Alle Daten im Text sind an echter Hardware gemessene Zahlen und Zustände, nicht aus Datenblättern abgeleitet.

## Kernaussagen (TL;DR)

Gemessen auf dem ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17): Der AWUS036ACH beherrscht Dual-Band-Monitor-Modus, erreicht auf beiden Bändern 30/30 = 100 % gerichtete Paketinjektion pro AP und betreibt einen AP-Hotspot auf beiden Bändern (reines 802.11g / reines 802.11a).

- Ab kernel 6.13 ohne DKMS (hier Ubuntu 24.04 / kernel 6.17), rtw88_8812au ist integriert, direkt nach dem Einstecken erkannt.
- Dual-Band-Monitor-Modus nutzbar, die gerichtete Paket-Injektion pro AP liegt in beiden Bändern bei 30/30 = 100 %.
- End-to-End-WPA-Handshake nachgewiesen: Am 19.11.2026 ergänzend auf dem eigenen iPhone 15 Pro, 5G ch36, ein vollständiger 4-Way erfasst, 47 .22000-Hashlines exportiert.
- Der 5-GHz-Empfang kann hängen bleiben, hilft nur physisches Aus- und Einstecken oder Neustart.
- Im Einzelbetrieb lässt sich ein IBSS aufbauen, aber 802.11s-Mesh, active monitor und Wi-Fi Direct (P2P) werden nicht unterstützt.

## 1. Diese Karte und die Testplattform

Der AWUS036ACH ist die von ALFA Network als „Doppelantenne mit hohem Gewinn“ positionierte USB-WLAN-Karte, mit Realtek-RTL8812AU-Chip, spezifiziert als Wi-Fi 5 (802.11ac), 2T2R, Dual-Band AC1200. Gegenüber dem einantennigen AWUS036ACHM derselben Serie (MediaTek MT7610U, AC600) tauscht der ACH mit zwei externen Hochgewinn-Antennen besseren Empfang und eine stabilere Injection-Leistung ein und ist ein häufiger Kandidat, wenn Kunden nach „Monitor über große Distanz“ und „Dual-Band-Injektion“ fragen.

Testplattform und -bedingungen dieser Runde:

- Rechenplattform: ASUS GX10 (ARM64 / aarch64)
- Betriebssystem: Ubuntu 24.04 LTS
- Kernel-Version: kernel 6.17.0-1014-nvidia
- Testgerät: Apple iPhone 7 Plus (2.4G / 5G / WPA3 alle mit diesem Gerät getestet)
- Testumgebung: eigenes Büro-WLAN, SSID `YUPITEK` (2,4GHz ch5 / 5GHz ch36, ch157)
- Testdatum: Hardware-Messung am 18.11.2026

Durchgehend wird nur die zur ALFA-Karte gehörige `wlx*`-Schnittstelle bedient, die interne Netzwerkkarte des GX10 für den Uplink nach außen wird nicht angefasst, und `airmon-ng check kill` wird nicht ausgeführt (dieser Befehl schaltet den NetworkManager ab und trennt den Host vom Netz).

## 2. Hardware und Treiber (Chip / USB-ID / in-kernel, ohne Installation)

| Punkt | Spezifikation |
|---|---|
| Modell | AWUS036ACH |
| Chip | Realtek RTL8812AU |
| USB-ID | `0bda:8812` |
| Treiber | `rtw88_8812au` (kernel-intern, mainline ≥ 6.13) |
| Firmware | `rtw88/rtw8812a_fw.bin` (im System enthalten) |
| Generation / Streams | Wi-Fi 5 (802.11ac) / 2T2R |
| Bandbreitenklasse | Dual-Band AC1200 |
| Antenne | Doppelantenne mit hohem Gewinn (extern) |
| USB-Schnittstelle | USB 3.0 (im Test als 5000M aufgezählt) |

Der ACH ist am 6.17-kernel des GX10 echtes Plug-and-Play: `lsusb` erkennt `0bda:8812`, der Treiber `rtw88_8812au` bindet sich automatisch, die Firmware `rtw8812a_fw.bin` ist im System enthalten, ohne Kompilieren, ohne DKMS. Das ist für die ARM64-Umgebung besonders wichtig. Viele alte Out-of-Tree-Realtek-Treiber müssen unter aarch64 aus dem Quellcode kompiliert werden, doch die beiden alten Projekte morrownr/USB-WiFi und aircrack-ng/rtl8812au verweisen inzwischen beide auf diesen integrierten Treiber, und Bug-Reports konzentrieren sich auf lwfinger/rtw88. Daher müssen Nutzer ab kernel ≥ 6.13 (einschließlich des 6.17 des GX10) kein Drittanbieter-DKMS mehr anfassen; nur unter altem Kernel (< 6.13) ist eine zusätzliche DKMS-Installation von `lwfinger/rtw88` nötig. Dieses Upstream-Projekt wird aktuell weiterhin aktiv gepflegt (letzter Commit 24.10.2026, enthält u. a. eine Bluetooth-1T1R-Korrektur für den 8812A), was bedeutet, dass die Mainline-Unterstützung dieses Chips laufend aktualisiert wird und kein eingestellter alter Treiber ist.

Bei der Hardware-Verbindung ist ein Detail zu beachten: Der ACH hat einen USB-A-Stecker; verwenden Sie einen USB-C→A-Adapter und stecken Sie ihn direkt in den USB-C-Port des GX10, damit USB 3.0 läuft (Aufzählung zeigt 5000M). Schließen Sie ihn hinter einem USB-2.0-Hub von Tastatur/Maus an, wird er gedrosselt und das USB3-Verhalten lässt sich nicht messen.

Bei den Schnittstellenmodi meldet `iw phy` Unterstützung für IBSS / managed / AP / AP-VLAN / monitor, aber kein mesh, P2P und active-monitor; diese Grenze bestimmt unmittelbar einen Teil der Einschränkungen in Abschnitt 4.

## 3. Getestete Fähigkeiten: Monitor / Injection / AP / WPA3

| Funktion | 2,4 GHz | 5 GHz | Messdaten |
|---|---|---|---|
| Monitor | ✅ | ✅ | 2.4G ch1/6/11 = 92/214/71 frames; 5G ch36/149/157 = 260/137/127 frames |
| Injection (Broadcast-Probe) | ✅ | ✅ | `aireplay-ng --test` broadcast probe meldet in beiden Bändern Injection is working |
| Injection (gerichtet pro AP) | ✅ 30/30 = 100% | ✅ 30/30 = 100% | 2.4G gegen 4 APs (inkl. YUPITEK); 5G gegen YUPITEK ch36 |
| AP-Hotspot (iPhone 7 Plus) | ✅ reines 802.11g | ✅ reines 802.11a (ch36) | 4-Way-Handshake abgeschlossen, beim ersten Versuch verbunden |
| WPA3-SAE AP | ✅ (`sae_pwe=0`) | Nicht getestet | mit `ieee80211w=2`, iPhone 7 Plus verbunden (nur auf 2,4 GHz getestet) |

**Monitor**: Auf 2,4 GHz wurden in ch1 / ch6 / ch11 jeweils 92 / 214 / 71 Frames erfasst; auf 5 GHz in ch36 / ch149 / ch157 260 / 137 / 127 Frames. Der Monitor funktioniert in beiden Bändern normal, der 5-GHz-Empfang liegt sogar über dem 2,4-GHz-Empfang (ch36 mit 260 Frames erfasst), passend zur Positionierung als Doppelantenne mit hohem Gewinn.

**Injection**: Das ist die Stärke des ACH. Auf 2,4 GHz macht `aireplay-ng --test` zuerst eine Broadcast-Probe (meldet Injection is working, Found 4 APs), dann gerichtet pro AP; gegen die 4 APs einschließlich YUPITEK liegt die Antwortrate jeweils bei 30/30 = 100 %, min/avg/max RTT etwa 4,9 / 39,2 / 99,0 ms, Power etwa -47. Die 2,4G-Injektion des Doppelantennen-ACH ist deutlich stabiler als beim einantennigen ACHM. In der Praxis ist daran zu denken, `--ignore-negative-one` hinzuzufügen: Das ist ein bekanntes Verhalten aus lwfinger/rtw88 #453: Bei aktiver STA-Schnittstelle kann der monitor channel `-1` melden; ohne dieses Flag wird das fälschlich als Injektionsfehler gewertet. Zudem gibt es laut Upstream-Aufzeichnungen unter hoher Injection-Last gelegentlich einen USB-Reset des integrierten Treibers, was bei der etwa 90-sekündigen Messung dieser Runde jedoch nicht beobachtet wurde. Auf 5 GHz ist die gerichtete Injektion gegen YUPITEK (ch36) ebenfalls 30/30 = 100 %, durchschnittliche RTT 13,6 ms, Power -69,1. Das ist unter der Voraussetzung „neu eingesteckte Karte + regdomain auf eine TX erlaubende Regulierung gesetzt“ gemessen (Details siehe die 5G-Hinweise in Abschnitt 4).

**AP-Hotspot**: Betrieben mit hostapd, läuft 2,4 GHz über reines 802.11g (`ieee80211n=0`), 5 GHz über reines 802.11a (ch36); das iPhone 7 Plus verband sich in beiden Bändern beim ersten Versuch, ohne Assoziationsfehler; im Log sind die vollständigen vier Schritte authenticated → associated → AP-STA-CONNECTED → EAPOL-4WAY-HS-COMPLETED zu sehen. Die Praxiserfahrung: Der ACH verbindet sich am saubersten mit der Einstellung „802.11n deaktiviert, reines g / reines a“.

**WPA3-SAE**: Bei einem SAE-only-AP ist der entscheidende Parameter `sae_pwe=0` (hunting-and-pecking) zusammen mit `ieee80211w=2`, erst dann verbindet sich das iPhone 7 Plus; mit `sae_pwe=2` gelingt die Verbindung nicht. Das ist dieselbe Kompatibilitätsfalle, in die auch der ACHM derselben Serie tappt.

## 4. Erweiterte Fähigkeiten und Handshake: machbarer Rahmen und ehrliche Grenzen

| Erweiterte Fähigkeit | Ergebnis | Erläuterung / Beleg |
|---|---|---|
| VIF (STA + monitor gleichzeitig) | ✅ im Test nutzbar | Hauptschnittstelle managed und `mon9` (monitor) gleichzeitig up, monitor-VIF erfasst in 8 s 100 Frames |
| WPA-Handshake-Erfassung | ✅ End-to-End (.22000) nachgewiesen | Injektion in beiden Bändern 100 %; am 19.11.2026 ergänzend auf 5G ch36 vollständigen 4-Way erfasst, hcxpcapngtool exportiert 47 `.22000`-Hashlines |
| macchanger (MAC ändern) | ✅ | zufällige MAC setzen und wiederherstellen funktionieren (vorher `ip link down` nötig) |
| Ad-hoc (IBSS) | 🟡 Einzelbetrieb | im Einzelbetrieb `Joined IBSS` erfolgreich; Peer-Link mangels zweitem Gerät nicht getestet |
| Active monitor | ❌ | `Operation not supported (-95)` |
| Mesh (802.11s) | ❌ | `Operation not supported (-95)` |
| Wi-Fi Direct (P2P) | ❌ | `Operation not supported (-95)` |

**Die Handshake-Erfassungsfähigkeit muss klar benannt werden**: Die Injektion des ACH ist in beiden Bändern 100 %, und die Injektion ist gerade der auslösende Teil der End-to-End-Workflow-Kette „deauth des eigenen Testgeräts → Erfassung des vollständigen 4-Way (M1–M4) → Export einer hashcat-`.22000` mit hcxpcapngtool“. Am 19.11.2026 wurde ergänzend auf dem eigenen iPhone 15 Pro, 5 GHz ch36, ein vollständiger 4-Way-Handshake erfasst und mit hcxpcapngtool in 47 `.22000`-Hashlines exportiert; damit ist die End-to-End-Handshake-Erfassung des ACH nachgewiesen. In unserer Gesamttabelle der 9 Karten ist End-to-End (`.22000`) bei 7 von 9 Modellen nachgewiesen: AWUS036ACM, AWUS036ACHM, AWUS036ACH, AWUS036ACS, AWUS036EACS, AWUS036AX und AWUS036AXER. Jede Erfassung erfolgt ausschließlich in eigenen oder autorisierten Netzwerken.

**VIF**: Die Flags von `iw phy` schreiben interface combinations are not supported, doch an echter Hardware können die managed-Hauptschnittstelle und die separat geöffnete monitor-Schnittstelle `mon9` gleichzeitig up sein; `mon9` erfasste in 8 Sekunden 100 Frames – „online und zugleich mitschneiden“ funktioniert am ACH also. Zu beachten ist: Die phy garantiert diese Kombination nicht; für lang andauernde oder hochlastige Szenarien empfiehlt sich die mt76-Serie (ACM / ACHM).

**Drei besonders zu kennzeichnende Grenzen:**

1. **Keine Unterstützung für Active monitor, Mesh (802.11s) und Wi-Fi Direct (P2P)**: Alle drei meldeten im Test `Operation not supported (-95)`. Wer diese drei Fähigkeiten benötigt, wechselt zur mt76-Serie (die phy von ACM / ACHM deklariert mesh / P2P / active-monitor).
2. **5G-RX-Hänger (bekanntes Verhalten von `rtw88_8812au`)**: Direkt nach dem Einstecken funktionieren 5G monitor / injection normal, doch nach wiederholtem Moduswechsel oder Änderung der regdomain kann der 5G-Empfang hängen bleiben (0 Pakete erfasst) und ist per Software nicht wiederherstellbar – es hilft nur physisches Aus- und Einstecken oder ein Neustart. Es empfiehlt sich, die Karte vor 5G-Tests einmal aus- und einzustecken und die 5G-Punkte vorrangig abzuschließen. Hier noch die Voraussetzung, damit die 5G-Injektion hinauskommt: Unter dem Standard `country 00` ist 5G komplett passive / no-IR (TX gesperrt), die gerichtete Injektion kommt schlicht nicht hinaus; setzen Sie auf eine TX erlaubende Regulierung (`iw reg set US` entsperrt ch36 / ch149, `TW` gibt nur ch149 aufwärts frei, ohne ch36) und nach dem Test wieder auf `TW` zurück. „Neu eingesteckte Karte“ bedeutet physisches Aus- und Einstecken bis zur USB-Neuaufzählung: `dmesg` muss `USB disconnect` und `renamed from wlan0` zeigen und die Bus-Nummer muss sich ändern, erst dann zählt es; ist 5G bereits hängen geblieben, meldet aireplay `No such BSSID available`.
3. **hcxdumptool meldet auf dieser Plattform bei allen Karten außer dem AWUS036EACS auf 2,4 GHz `failed to arm`**: Da es active-monitor benötigt, das weder rtw88 noch rtw89 noch mt7921u unterstützt; erfassen Sie Handshakes stattdessen über den Weg airodump-ng + aireplay-ng.

### Toolchain-Kompatibilität (Kali)

Für die in Kali gebräuchlichen Werkzeuge wurde ein Schnelldurchlauf gegen den ACH gemacht (Umgebungsziel ist das eigene `YUPITEK`), mit folgendem Ergebnis:

| Werkzeug | Status | Erläuterung |
|---|---|---|
| airmon-ng | ✅ | listet korrekt `phy2 / wlx... / rtw88_8812au / RTL8812AU 2T2R` |
| Wireshark / tshark | ✅ | `tshark -i $IF` erfasst Beacons (inkl. YUPITEK), 20 packets captured |
| kismet | ✅ installiert | `/usr/bin/kismet`, als data source startbar |
| bettercap | ✅ installiert | `/usr/bin/bettercap` |
| hcxdumptool | ⚠️ | installiert, aber auf dieser Plattform `failed to arm` (benötigt active-monitor, siehe oben) |
| macchanger | ✅ | GNU 1.7.0; `-r` zufällig, `-p` wiederherstellen, im Test normal |
| wifite | ❌ nicht installiert | auf diesem Gerät kein solcher Befehl, muss separat installiert werden (empfohlen die git-Version, um apt-Abhängigkeitskonflikte mit dem selbst kompilierten aircrack-ng zu umgehen) |

Das Fazit ist schlicht: airmon-ng erkennt und verwaltet den ACH korrekt; der übliche Monitor- und Erfassungsablauf ist über die aircrack-ng-Suite (airodump-ng + aireplay-ng) am stabilsten; das active-monitor benötigende hcxdumptool kann auf dieser Plattform nicht armen, verbeißen Sie sich nicht darin.

## 5. Einsatzszenarien und Auswahlempfehlung (zurück zur Hub-Gesamttabelle)

Stellt man den ACH zurück in die gesamte Produktlinie, ist seine Positionierung klar: Doppelantenne mit hohem Gewinn, Dual-Band-Injektion 100 %, End-to-End-WPA-Handshake (.22000) nachgewiesen – eine pragmatische Wahl für Kunden, die „stabile Injektion und zugleich stärkeren Empfang“ wollen.

- **Penetrationstest (Injection + Handshake)**: Erste Wahl ist die Gruppe AWUS036EACS / AWUS036ACH / AWUS036ACS, deren Dual-Band-Injektion bei allen dreien im oberen Bereich liegt.
- **Stärkster Empfang / Monitor über große Distanz**: AWUS036AXER und AWUS036ACH, wobei der ACH durch die Doppelantenne mit hohem Gewinn hervorsticht.
- **Bedarf an 802.11s-Mesh / active-monitor / P2P**: Der ACH (Realtek rtw88) kann das nicht (im Test `-95`); wechseln Sie zum mt76-Treiber AWUS036ACM / AWUS036ACHM; das IBSS des ACH ist nur im Einzelbetrieb aufbaubar, der Peer-Link ungetestet.
- **Nur reiner AP oder normale Verbindung, kein Injection**: Die MediaTek-Modelle AWUS036AXM / AXML sind stabiler, aber beachten Sie, dass bei ihnen auf dieser Plattform die Injektion fehlschlägt; für Penetrationszwecke sind sie ungeeignet.

Ein Warnhinweis in einem Satz: Wenn der Kundenbedarf eindeutig Injection und Handshake ist, wählen Sie nicht den AWUS036AXM / AXML (die Injektion des MT7921-Chips schlägt auf dieser Plattform im Test fehl, kein deauth und keine Handshake-Erfassung möglich); für diesen Bedarf ist der ACH hingegen ein solider Kandidat. Schauen Sie bei der Auswahl auch nicht nur auf die Bandbreitenzahlen – die durch die Doppelantenne mit hohem Gewinn gewonnene Empfangsstabilität macht bei der tatsächlichen Mitschnitt-Reichweite oft spürbarer einen Unterschied als die Datenblatt-Spezifikation. Auswahlentscheidung und plattformübergreifende Fallstricke finden Sie in der Hub-Gesamttabelle: [Vollständige Monitor- · Injection- · AP-Matrix der 9 ALFA-WLAN-Karten auf dem ASUS GX10 (ARM64)](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Häufig gestellte Fragen (FAQ)

**F: Benötigt der AWUS036ACH unter Kali oder Ubuntu einen Treiber?**
Das hängt von der Kernel-Version ab. Linux-Kernel 6.13 und höher (hier getestet: Ubuntu 24.04 / kernel 6.17) bringt den Treiber rtw88_8812au bereits mit, er wird direkt nach dem Einstecken erkannt – ohne Kompilieren, ohne DKMS; nur unter Kernel unter 6.13 müssen Sie zusätzlich per DKMS lwfinger/rtw88 installieren. Prüfen Sie unter Kali zuerst mit uname -r die Kernel-Version; auf echter Kali-Hardware wurde dies nicht verifiziert.

**F: Wie schlagen sich Monitor-Modus und Paket-Injektion des AWUS036ACH?**
Sowohl 2,4 GHz als auch 5 GHz können in den Monitor-Modus; die gerichtete aireplay-ng-Injektion pro AP liegt auf 2,4 GHz (gegen 4 APs) wie auf 5 GHz (gegen YUPITEK ch36) bei 30/30 = 100 %. Vor der 5-GHz-Injektion muss die Regulierungsdomäne auf eine Einstellung gesetzt werden, die das Senden erlaubt (z. B. iw reg set US); unter dem Standard country 00 ist das Senden auf 5 GHz gesperrt und die Injektion kommt nicht hinaus.

**F: Kann der AWUS036ACH einen WPA-Handshake erfassen?**
Ja, und End-to-End ist nachgewiesen. Die Injektion liegt in beiden Bändern bei 100 %; am 19.11.2026 wurde ergänzend auf dem eigenen iPhone 15 Pro, 5 GHz ch36, ein vollständiger 4-Way-Handshake erfasst und mit hcxpcapngtool in 47 hashcat-.22000-Hashlines exportiert. Nur in eigenen oder autorisierten Netzwerken.

**F: Was tun, wenn sich das iPhone 7 Plus nicht mit dem WPA3-Hotspot des AWUS036ACH verbinden kann?**
hostapd muss sae_pwe=0 zusammen mit ieee80211w=2 setzen, erst dann verbindet sich das iPhone 7 Plus; mit sae_pwe=2 gelingt die Verbindung nicht. Dieselbe Einstellung ist auch beim AWUS036ACHM entscheidend.

**F: Was tun, wenn der 5-GHz-Empfang des AWUS036ACH plötzlich hängt (0 Pakete erfasst)?**
Das ist ein bekanntes Verhalten von rtw88_8812au: Nach wiederholtem Moduswechsel oder Änderung der Regulierungsdomäne kann der 5-GHz-Empfang hängen bleiben und ist per Software nicht wiederherstellbar – es hilft nur physisches Aus- und Einstecken oder ein Neustart. Es empfiehlt sich, die Karte vor 5-GHz-Tests neu einzustecken und die 5-GHz-Punkte vorrangig abzuschließen.

## 6. Weiterführende Literatur

- Hub-Gesamttabelle: [9 ALFA-WLAN-Karten im ARM64-Gesamttest-Matrix](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Monitor und AP unter Ubuntu (ARM64) ohne Treiberinstallation aktivieren: [placeholder](/de/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- WPA3-SAE-Handshake-Erfassung und `sae_pwe`-Kompatibilität: [placeholder](/de/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Schwesterkarten-Vergleich: AWUS036ACHM (Einzelantenne AC600) im Einzelkartentest [placeholder]
- Vollständiger Beleg-Pfad dieses Modells (intern): `AWUS036ACH_evidence/` (p0 Aufzählung, p1_gx10 Verhalten, retest Fehlersuche)

<!-- hreflang: zh-TW ist die Hauptvorlage; zh-CN / en / ja / ko / de / fr / es werden nach Fertigstellung der Hauptvorlage generiert und mit rel=alternate ergänzt. -->
