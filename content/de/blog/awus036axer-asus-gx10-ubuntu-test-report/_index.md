---
title: "AWUS036AXER Testbericht: die empfangsstärkste Wi-Fi-6-Karte auf dem ASUS GX10 + Ubuntu 24.04 (ARM64)"
slug: awus036axer-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axer-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036axer
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - ubuntu-24-04
  - kernel-6-17
  - arm64
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
description: "AWUS036AXER auf ASUS GX10 / Ubuntu 24.04 ARM64 ohne Treiberinstallation (rtw89_8852bu): monitor findet in 60 Sekunden 63 APs + 12 Clients, Injektion 73 % (2,4G), 5G VHT80-AP und WPA3 beide bestanden."
faq:
  - question: "Benötigt der AWUS036AXER unter Ubuntu 24.04 oder Kali einen separaten Treiber?"
    answer: "Unter Ubuntu 24.04 (ARM64, kernel 6.17.0-1014-nvidia) nicht: Der kernel-interne rtw89_8852bu-Treiber wird direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS (firmware rtw8852b_fw 0.29.29.5). Die Plattform dieses Artikels ist Ubuntu, keine Kali-Distribution; Kali selbst wurde nicht getestet. Die gängigen Kali-Werkzeuge airmon-ng, kismet, bettercap, wifite, Wireshark sind auf dieser Plattform nutzbar. Bei älteren Kerneln ist der eingebaute Support nicht garantiert, prüfen Sie zuerst die Version."
  - question: "Unterstützt der AWUS036AXER den Monitor-Modus? Wie stark ist der Empfang?"
    answer: "Ja, sowohl 2,4 GHz als auch 5 GHz können in den monitor. Wir haben im eigenen Büro mit airodump-ng 60 Sekunden lang einen Frequenzsprung-Scan gemacht und 63 APs sowie 12 Clients gefunden – die empfangsstärkste der neun Karten in unserem Testdurchlauf; der AWUS036AX mit demselben Chip ergab in einer anderen Messung 14 APs + 4 Clients (zwei nicht synchrone Messungen, nur als Anhaltspunkt)."
  - question: "Kann der AWUS036AXER Paket-Injektion (packet injection) durchführen?"
    answer: "Ja. aireplay-ng --test in 2,4 GHz zeigt eine Antwortrate von 73 % (22/30) und Injection is working!, auch der 5-GHz-Einzeltest besteht; wir haben in eigenem Netzwerk und auf eigenem Gerät die Handshake-Erfassung durchgeführt und die .22000 exportiert. Für annähernd 100 % in beiden Bändern sind im Praxistest dieser Plattform AWUS036EACS, ACH und ACS stabiler. Nur in eigenen oder autorisierten Netzwerken."
  - question: "Worin unterscheiden sich AWUS036AXER und AWUS036AX?"
    answer: "Beide nutzen Realtek RTL8832BU und rtw89_8852bu; Modus-Support und Injektionsverhalten sind auf dieser Plattform identisch. Der Unterschied liegt in der Empfangsleistung durch Antennenabstimmung und -gewinn (AXER 60 s 63 APs + 12 Clients, AX 14 APs + 4 Clients). Beide haben eingebaute Antennen, kein RP-SMA; die Antennenspezifikation richtet sich nach der Produktseite."
  - question: "Kann der AWUS036AXER als AP dienen oder WPA3 öffnen? Welche Modi unterstützt er nicht?"
    answer: "Ja. Sowohl 2,4 GHz 802.11n als auch 5 GHz VHT80 (VHT-NSS2, 351 Mbit) haben ein iPhone verbunden und authorized; WPA3-SAE mit sae_pwe=0 lässt das iPhone 15 Pro verbinden (auf 2,4 GHz; WPA3 auf 5 GHz wurde nicht getestet); STA+AP parallel nutzbar. Aber rtw89_8852bu unterstützt active monitor, IBSS und mesh nicht."
draft: false
---

{{< tldr >}}Der AWUS036AXER ist auf ASUS GX10 / Ubuntu 24.04 ARM64 direkt nutzbar (kernel-internes rtw89_8852bu); monitor findet in 60 Sekunden 63 APs + 12 Clients, 2,4-GHz-Injektion 73 %, AP und WPA3 beide bestanden; kein Support für active monitor, IBSS, mesh.{{< /tldr >}}

> Dieser Artikel ist Yupiteks (ALFA-Distributor Taiwan) Kompatibilitäts- und Fähigkeits-Praxistest auf eigener Hardware.
> Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Testumgebung ist das eigene Büro-WLAN (SSID `YUPITEK`), gegen das eigene Testhandy iPhone 7 Plus (WPA3 zusätzlich iPhone 15 Pro).
> ⚠️ **Rechtmäßige Nutzung**: Monitor und Injection nur in Netzwerken und auf Geräten, die Ihnen gehören oder für die Sie eine Genehmigung haben; im AP-Modus halten Sie bitte die lokalen Funkvorschriften ein. Dieser Artikel konzentriert sich auf Kartenfähigkeiten, Kompatibilität, Konfiguration und Auswahl und umfasst keinerlei Angriffsoperationen gegen fremde Netzwerke.

---

## 1. Diese Karte und die Testplattform

Der AWUS036AXER ist ALFAs Wi-Fi-6-(802.11ax-)2x2-USB-Karte mit Realtek-RTL8832BU-Chip (ohne Bluetooth). Er nutzt **denselben Chip und denselben Treiber** (`rtw89_8852bu`) wie der AWUS036AX desselben Herstellers; Modus-Support und Verhalten auf dieser Plattform sind identisch. Der eigentliche Unterschied der beiden liegt in **Antennenabstimmung und -gewinn**, nicht in extern oder eingebaut – der AXER nutzt ein **eingebautes (Nano-)Antennendesign ohne RP-SMA** und holt den Empfang durch Chip- und RF-Abstimmung auf das Maximum. Merken Sie sich die Kernaussage dieses Artikels vorab: Unter den neun ALFA-Karten in unserem Vergleich hat der AXER **den stärksten Empfang**.

Die Testplattform ist der ASUS GX10, ausgestattet mit dem NVIDIA-GB10-Superchip und 128 GB unified memory, Betriebssystem Ubuntu 24.04 LTS, Architektur ARM64 (aarch64), kernel `6.17.0-1014-nvidia`. Alle Ergebnisse wurden am 18.11.2026 auf dieser Maschine auf echter Hardware erzeugt, Testgerät ist das eigene iPhone 7 Plus (WPA3 zusätzlich iPhone 15 Pro), Testnetzwerk ist das eigene Büro-WLAN. Für die Distributor-Validierung ist ARM64 mit einem aktuellen Kernel eine relativ anspruchsvolle Kombination; Abschnitt 2 erklärt, warum diese Generation stattdessen weniger Mühe macht.

Ein Stück Spezifikationskontext: Der AXER ist eine 2x2-(zwei räumliche Datenströme-)Wi-Fi-6-Karte, die zwei räumliche Datenströme gleichzeitig senden und empfangen kann, was auch dem im späteren 5-GHz-AP-Test ausgehandelten VHT-NSS2 entspricht. Doch dass diese Karte diese Runde gewinnt, liegt am Antennendesign und an der RF-Abstimmung, nicht an der Streamzahl (der AX ist ebenfalls 2x2). Chip, Treiber und Plattform sind alle gleich, die Antennenabstimmung ist nahezu die einzige Variable, sodass sich der Empfangsunterschied zwischen AXER und AX sauber auf das eingebaute Antennendesign und die Gewinnabstimmung zurückführen lässt.

---

## 2. Hardware und Treiber (eingebaute Antenne, ohne Treiberinstallation)

Der AWUS036AXER ist unter Ubuntu 24.04 mit kernel 6.17 **direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS**. Der Treiber `rtw89_8852bu` ist bereits ein in-kernel-Modul, die firmware ist `rtw8852b_fw` (Version 0.29.29.5), wird beim Booten geladen, man muss kein Out-of-Tree-Projekt mehr von GitHub holen oder an DKMS binden. Für Distributions- und Schulungsumgebungen, die lange gewartet werden und mehrere Kernel-Updates durchlaufen, ist der Wegfall des Treiberkompilierens ein weniger häufiger Fehlerpunkt.

Der Vergleich mit dem alten Weg macht es greifbarer: Früher waren solche Realtek-USB-Chips meist nicht im Mainline-Kernel, Nutzer mussten ein Out-of-Tree-Projekt von GitHub holen (z. B. `morrownr/USB-WiFi`) und mit DKMS an den aktuellen Kernel gebunden kompilieren, bei jedem Kernel-Update neu, und schlug die Kompilierung fehl, verschwand die Karte sofort. Seit rtw89 offiziell in-kernel aufgenommen wurde, lassen sich diese Schritte auf 6.17 komplett auslassen, und dieselbe Prozedur ist über mehrere Karten mit demselben Treiber hinweg wiederverwendbar.

Zuerst bestätigen, dass die Karte korrekt erkannt wird:

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
# Bus 00x Device 00x: ID 0bda:b832 Realtek Semiconductor Corp. 802.11ac WLAN Adapter
```

Die USB-ID im normalen WLAN-Modus ist `0bda:b832`. Sieht man `0bda:1a2b`, steckt die Karte noch im „CD-ROM-Modus“ (CD-ROM mode); einmal `sudo usb_modeswitch -v 0bda -p 1a2b -K` ausführen, um in den WLAN-Modus zu wechseln; die Karte dieser Testinstanz wurde direkt im WLAN-Modus aufgezählt, ohne auf den CD-ROM-Modus zu stoßen.

Der Schnittstellenname nutzt die Benennung `wlx` + MAC (z. B. `wlxAABBCCDDEEFF`) und ändert sich an keiner Maschine, praktisch für feste Skript-Bindung. Abfragen, welche Modi diese Karte unterstützt:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Die im Test gemeldeten Modi sind managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO. Hier fehlen IBSS, mesh und auch active monitor; das ist eine von Natur aus gegebene Einschränkung des rtw89-Treibers, die Abschnitt 4 ehrlich erläutert – treffen Sie bei der Auswahl keine Fehleinschätzung.

Zur Antenne: Der AXER nutzt ein eingebautes (Nano-)Antennendesign ohne RP-SMA; gegenüber dem AX mit demselben Chip liegt der Unterschied in Antennenabstimmung und -gewinn, was sich in der Praxis am direktesten im Empfang niederschlägt. Die monitor-Daten im nächsten Abschnitt machen das deutlich.

---

## 3. Getestete Fähigkeiten

Die Testergebnisse der drei Kernfähigkeiten (Monitor / Injection / AP) und von WPA3 zuerst in einer Tabelle, Details danach Punkt für Punkt:

| Fähigkeit | 2,4 GHz | 5 GHz | Testkern |
|---|---|---|---|
| **Monitor (Mithören)** | ✅ stark | ✅ stark | Frequenzsprung findet **63 APs + 12 Clients**, stärkster Empfang der neun Karten |
| **Injection (Injektion)** | ✅ 73 % | ✅ nutzbar | 2.4G `22/30 73 %`; 5G `Injection is working!` |
| **AP (Hotspot)** | ✅ 802.11n | ✅ VHT 80 MHz | iPhone verbindet; 5G VHT-NSS2, 351 Mbit |
| **WPA3-SAE** | ✅ | Nicht getestet | AP-seitig iPhone 15 Pro verbindet (`sae_pwe=0`); nur auf 2,4 GHz getestet |
| **WPA-Handshake-Erfassung** | ✅ End-to-End | — | eigenes Netzwerk + eigenes Gerät, 4-way (M1–M4) → `.22000` |

### 3-1. Monitor (Highlight dieses Artikels: stärkster Empfang)

Der Wechsel in den monitor ist der Standard-`iw`-Ablauf: zuerst die Schnittstelle in die eigene Verwaltung zurückgeben (`nmcli dev set $IF managed no`), Schnittstelle herunterfahren, monitor type setzen, Schnittstelle hochfahren, Kanal setzen:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36        # 5 GHz; 2,4 GHz nutzt channel 6
sudo timeout 8 tcpdump -l -i $IF -nn -e -c 200
```

2,4 GHz und 5 GHz erreichen je innerhalb von 6 Sekunden die vollen 100 frames. Was den Abstand wirklich ausmacht, ist der Frequenzsprung-Scan: `sudo airodump-ng --band abg $IF` über 60 Sekunden **findet 63 APs plus 12 Clients**. Das ist die Karte dieser Runde, die unter den neun die meisten Ziele erfasst, und spiegelt direkt den Empfangsvorteil durch eingebautes Antennendesign und RF-Abstimmung wider. Für Vor-Ort-Bestandsaufnahme (site survey), Monitor über große Distanz oder Umgebungen mit schwachem Signal ist genau diese Empfangsfähigkeit der Kernwert des AXER.

### 3-2. Injection (Injektion)

Die Injection wird mit dem Selbsttest-Modus von aireplay-ng validiert; gemessen wird die Fähigkeit der Karte selbst, kein externer Angriff:

```bash
sudo iw dev $IF set channel 6
sudo aireplay-ng --test $IF
# Found 21 APs
# 22/30:  73%
# Injection is working!
```

2,4-GHz-Antwortrate 73 % (22/30), als nutzbar bewertet. Auch der 5-GHz-Selbsttest gegen einen einzeln angegebenen AP meldet `Injection is working!`. Eine Plattformregel ergänzt: **Vor dem Senden/Injizieren in 5 GHz zuerst `iw reg set US`, um die TX-Leistung zu entsperren, nach dem Test unbedingt `iw reg set TW`, um zurück auf das taiwanische Regulierungsband zu schalten.**

### 3-3. AP-Hotspot (2,4 GHz 802.11n, 5 GHz VHT 80 MHz)

Der AXER kann in beiden Bändern einen hostapd-AP aufsetzen. 2,4 GHz mit `hw_mode=g` + `ieee80211n=1` einen 802.11n-Hotspot öffnen, das iPhone 7 Plus handelt beim Verbinden MCS 15, authorized aus. 5 GHz mit `hw_mode=a` + `ieee80211ac=1` + `vht_oper_chwidth=1` einen VHT-80-MHz-Hotspot öffnen, das iPhone 7 Plus handelt beim Verbinden **VHT-NSS2, 80 MHz, 351 Mbit, authorized** aus. Die Voraussetzung zum AP-Aufbau ist `sudo nmcli dev set $IF managed no`, und das `wpa_passphrase` muss mindestens 8 Zeichen haben, sonst gibt hostapd `invalid WPA passphrase length` zurück.

### 3-4. WPA3-SAE und Handshake-Erfassung

WPA3-SAE wird AP-seitig mit `wpa_key_mgmt=SAE`, `ieee80211w=2`, `sae_pwe=0` gesetzt; im Test verbindet sich das iPhone 15 Pro. **`sae_pwe` ist der Kompatibilitäts-Fallstrick bei dieser Kartencharge**: Manche Geräte verbinden sich bei `sae_pwe=2` (Hash-to-Element) nicht; `sae_pwe=0` ist mit älteren iPhones kompatibel.

Die Handshake-Fähigkeit ist eine End-to-End-Validierung auf dem **eigenen Büro-WLAN (YUPITEK) + eigenem Testgerät**: der vollständige 4-way (M1/M2/M3/M4) erfasst, dann mit `hcxpcapngtool` die hashcat-lesbare `.22000` exportiert. Hier ist ein gemeinsames Phänomen der GX10-Plattform hervorzuheben: **`hcxdumptool` meldet auf dieser Plattform bei allen USB-Karten außer dem AWUS036EACS auf 2,4 GHz `failed to arm`** (Aufzählungskonflikt der internen Tri-Band-Karte des GX10, zudem fehlt dem Treiber active monitor), daher wechselt der Handshake-Ablauf zum aircrack-ng-Paket (airodump-ng + aireplay-ng). Die Injektionsfähigkeit des AXER ist auf diesem Weg ausreichend.

---

## 4. Erweiterte Funktionen und ehrliche Grenzen

**VIF (STA + AP parallel) ✅**: Der AXER kann gleichzeitig als station mit dem Uplink-Wi-Fi verbunden sein und eine AP-VIF öffnen. Im Test ist die Hauptschnittstelle mit YUPITEK verbunden, die AP-VIF läuft parallel in ch36 VHT80, STA-seitig ping 3,5 ms, geeignet für das Szenario „einerseits online, andererseits Hotspot öffnen“.

**Wi-Fi Direct (P2P) nicht getestet (⬜)**: Der Treiber deklariert P2P-client / P2P-GO, doch für eine vollständige Validierung braucht es ein zweites Gegengerät; diese Runde übersprungen, daher nicht als validierte Fähigkeit gelistet. Solche Punkte „vom Treiber deklariert, aber nicht auf echter Hardware durchgeführt“ kennzeichnen wir grundsätzlich ehrlich als nicht getestet und schönen sie nicht zu einem Bestanden.

**Die drei nicht unterstützten Modi (N/A)**: Der Treiber `rtw89_8852bu` **bietet weder active monitor noch Ad-hoc (IBSS) noch Mesh (802.11s)**. `iw dev $IF set type ibss` oder `mp` schlagen direkt fehl; das ist eine Einschränkung auf Treiberebene, die sich nicht per Konfiguration umgehen lässt. Wer Mesh- oder IBSS-Experimente braucht, schaut auf die MediaTek-mt76-Reihe (wie AWUS036ACM / ACHM).

**Gemeinsame Plattformhinweise:**

- Führen Sie niemals `airmon-ng check kill` aus, es schaltet den NetworkManager ab und trennt den GX10 vom Netz. Bedienen Sie nur die `wlx*`-Schnittstelle, fassen Sie die interne Uplink-Karte nicht an.
- Wenn nach wiederholtem Wechsel zwischen monitor/AP plötzlich nichts mehr gescannt wird (RX-Stall), genügt es, die Karte **einmal aus- und wieder einzustecken** (USB-Neuaufzählung; der Schnittstellenname ist durch die MAC bestimmt und ändert sich nicht).
- Auf der ARM64-Plattform muss aircrack-ng aus dem Quellcode kompiliert werden; wifite in der git-Version verwenden, um apt-Abhängigkeitskonflikte zu umgehen.

**Kali-Tool-Kompatibilität**: airmon-ng, kismet 2026.10, bettercap 2.32, wifite (git), Wireshark / tshark 4.2 können den AXER alle normal als Datenquelle oder Verwaltungsschnittstelle verwenden.

---

## 5. Einsatzszenarien und Auswahlempfehlung

Die Positionierung in einem Satz: **Der AXER ist eine Wi-Fi-6-Karte mit Empfangs-Ausrichtung.** Er hat denselben Chip wie der AX, die Funktionen sind identisch, der Unterschied liegt im Empfangsvorteil durch Antennenabstimmung und -gewinn, sodass die Auswahllogik klar ist:

| Ihr Bedarf | AXER erste Wahl? | Erläuterung |
|---|---|---|
| Stärkster Empfang / Monitor über große Distanz / Vor-Ort-Bestandsaufnahme | ✅ **Erste Wahl** | Frequenzsprung findet 63 APs + 12 Clients, stärkste der neun Karten; kann mit AWUS036ACH (Doppelantenne, hoher Gewinn) ergänzt werden |
| Wi-Fi 6 + AP-Hotspot | ✅ geeignet | 2x2, 5G VHT80; auf Niveau des AWUS036AX |
| Injection + End-to-End-Handshake | 🟡 nutzbar | 2,4G 73 % nutzbar; für annähernd 100 % in beiden Bändern sind AWUS036EACS / ACH / ACS stabiler |
| mesh / IBSS-Experiment | ❌ ungeeignet | rtw89 unterstützt es nicht, stattdessen AWUS036ACM / ACHM (mt76) verwenden |

Typisches Einsatzszenario: Den AXER als **entfernten Wireless-Monitorknoten** einsetzen, an Stellen mit schwächerem Signal oder größerer Distanz platzieren und mit dem Empfangsvorteil seiner eingebauten Antenne die APs / Clients vor Ort möglichst vollständig erfassen; die Scan-Ergebnisse werden dann zur zentralen Prüfung am Hauptrechner zusammengeführt. Da es eine eingebaute (Nano-)Antenne ohne RP-SMA ist, lässt sich die Antenne nicht wechseln; wenn höherer Gewinn oder stärkere Richtwirkung nötig ist, ergänzen Sie den AXER mit dem Doppelantennen-AWUS036ACH mit hohem Gewinn.

Umgekehrt: Wenn der Zweck reiner AP oder normale Verbindung ist und keinerlei Injektion braucht, sind auch MediaTeks AWUS036AXM / AXML nutzbar; aber **sobald Injektion oder Handshake im Spiel ist, wählen Sie nicht den AXM / AXML** – ihre Injektion schlägt auf dieser Plattform fehl (Hauptursache ist eine mac80211-chanctx-Regression ab Kernel 6.16; hinzu kommt, dass die Firmware die Injektionsrate auf 1/6 Mbit/s festlegt; das ist keine Grenze des Chips selbst). Der AXER ist genau das Gegenteil: Injektion nutzbar und zugleich stärkster Empfang.

Wer die vollständige Matrix und den Quervergleich aller neun Karten auf einmal sehen möchte, kehrt zur Gesamtbewertungsseite zurück → [`/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

---

## Häufig gestellte Fragen (FAQ)

**F1. Benötigt der AWUS036AXER unter Ubuntu 24.04 oder Kali einen separaten Treiber?**
Unter Ubuntu 24.04 (ARM64, kernel 6.17.0-1014-nvidia) nicht: Der kernel-interne `rtw89_8852bu`-Treiber wird direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS (firmware `rtw8852b_fw` 0.29.29.5). Die Plattform dieses Artikels ist Ubuntu, keine Kali-Distribution; Kali selbst wurde nicht getestet. Die gängigen Kali-Werkzeuge airmon-ng, kismet, bettercap, wifite, Wireshark sind auf dieser Plattform nutzbar. Bei älteren Kerneln ist der eingebaute Support nicht garantiert, prüfen Sie zuerst die Version.

**F2. Unterstützt der AWUS036AXER den Monitor-Modus? Wie stark ist der Empfang?**
Ja, sowohl 2,4 GHz als auch 5 GHz können in den monitor. Wir haben im eigenen Büro mit airodump-ng 60 Sekunden lang einen Frequenzsprung-Scan gemacht und 63 APs sowie 12 Clients gefunden – die empfangsstärkste der neun Karten in unserem Testdurchlauf; der AWUS036AX mit demselben Chip ergab in einer anderen Messung 14 APs + 4 Clients (zwei nicht synchrone Messungen, nur als Anhaltspunkt).

**F3. Kann der AWUS036AXER Paket-Injektion (packet injection) durchführen?**
Ja. `aireplay-ng --test` in 2,4 GHz zeigt eine Antwortrate von 73 % (22/30) und `Injection is working!`, auch der 5-GHz-Einzeltest besteht; wir haben in eigenem Netzwerk und auf eigenem Gerät die Handshake-Erfassung durchgeführt und die `.22000` exportiert. Für annähernd 100 % in beiden Bändern sind im Praxistest dieser Plattform AWUS036EACS, ACH und ACS stabiler. Nur in eigenen oder autorisierten Netzwerken.

**F4. Worin unterscheiden sich AWUS036AXER und AWUS036AX?**
Beide nutzen Realtek RTL8832BU und `rtw89_8852bu`; Modus-Support und Injektionsverhalten sind auf dieser Plattform identisch. Der Unterschied liegt in der Empfangsleistung durch Antennenabstimmung und -gewinn (AXER 60 s 63 APs + 12 Clients, AX 14 APs + 4 Clients). Beide haben eingebaute Antennen, kein RP-SMA; die Antennenspezifikation richtet sich nach der Produktseite.

**F5. Kann der AWUS036AXER als AP dienen oder WPA3 öffnen? Welche Modi unterstützt er nicht?**
Ja. Sowohl 2,4 GHz 802.11n als auch 5 GHz VHT80 (VHT-NSS2, 351 Mbit) haben ein iPhone verbunden und authorized; WPA3-SAE mit `sae_pwe=0` lässt das iPhone 15 Pro verbinden (auf 2,4 GHz; WPA3 auf 5 GHz wurde nicht getestet); STA+AP parallel nutzbar. Aber `rtw89_8852bu` unterstützt active monitor, IBSS und mesh nicht.

---

## 6. Weiterführende Literatur

- Gesamtmatrix und Auswahl-Gesamttabelle der neun ALFA-Karten (vollständiger Monitor- · Injection- · AP-Vergleich) → `/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`
- Praxistest des AWUS036AX mit demselben Chip (andere Antennenabstimmung) → `/de/blog/awus036ax-asus-gx10-ubuntu-test-report/`
- Ohne Treiberinstallation: Monitor- und AP-Modus mit dem in-kernel-Treiber aktivieren → `/de/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`
- Handshake-Erfassungsfähigkeit im Zeitalter von WPA3-SAE und `sae_pwe`-Kompatibilität → `/de/blog/alfa-wpa3-sae-handshake-capability-arm64/`

<!-- Interne Links der weiterführenden Literatur erhalten nach Finalisierung die offiziellen hreflang-URLs; die obigen sind de-slug-Platzhalter. -->

---

*Testinstanz: Yupitek (ALFA-Distributor) — https://www.yupitek.com | Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Testgerät: Apple iPhone 7 Plus (WPA3 zusätzlich iPhone 15 Pro)*
