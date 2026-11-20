---
title: "AWUS036ACS im Einzelkartentest: Die leichte Mobilkarte RTL8811AU auf dem ASUS GX10 + Ubuntu 24.04 (ARM64) – Kompatibilitäts- und Fähigkeitsbericht"
slug: awus036acs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acs-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036acs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acs
  - rtl8811au
  - rtw88-8821au
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
description: "AWUS036ACS im Test unter Ubuntu 24.04 ARM64: ohne Treiberinstallation; Monitor, Injektion (2,4G 100 %, 5G 96 %), AP, WPA3-SAE und End-to-End-Handshake (.22000) alle bestanden. Plattform ASUS GX10, kernel 6.17, RTL8811AU."
faq:
  - question: "Benötigt der AWUS036ACS unter Ubuntu 24.04 ARM64 einen Treiber?"
    answer: "Auf dem in diesem Artikel getesteten kernel 6.17 (ASUS GX10) nicht: Der RTL8811AU wird vom integrierten rtw88_8821au getrieben, direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS. Bei älterem Kernel prüfen Sie zuerst mit modinfo rtw88_8821au, ob das Modul vorhanden ist."
  - question: "Unterstützt der AWUS036ACS den Monitor-Modus und Packet Injection?"
    answer: "Ja. Sowohl 2,4 GHz als auch 5 GHz können in den Monitor-Modus; die aireplay-ng --test-Injektion liegt auf 2,4G bei 100 % (30/30), auf 5G bei 96 % (29/30, vorher iw reg set US nötig, um die TW-Beschränkung aufzuheben). Active monitor wird nicht unterstützt."
  - question: "Kann der AWUS036ACS einen WPA-Handshake erfassen und in hashcat .22000 umwandeln?"
    answer: "Ja. Auf dem eigenen AP und dem eigenen iPhone 7 Plus End-to-End getestet: gerichtetes deauth löst eine Neuverbindung aus, der vollständige 4-Way (M1–M4) wird erfasst und dann mit hcxpcapngtool --all in .22000 exportiert. Nur in eigenen oder autorisierten Netzwerken."
  - question: "Kann der AWUS036ACS als AP-Hotspot dienen? Unterstützt er WPA3?"
    answer: "Ja. hostapd öffnet 2,4G- und 5G-Hotspots (5G wurde als 802.11a mit 20 MHz getestet; VHT80 wurde nicht getestet), das iPhone 7 Plus verbindet sich und schließt den 4-Way ab; auch das WPA3-SAE auf 5G (SAE-only, ieee80211w=2, sae_pwe=0) verbindet sich erfolgreich (WPA3 auf 2,4G wurde nicht getestet)."
  - question: "Welche Modi unterstützt der AWUS036ACS nicht? Funktioniert hcxdumptool?"
    answer: "Nicht unterstützt werden active monitor, IBSS, Mesh (802.11s) und Wi-Fi Direct (P2P). hcxdumptool 8.x meldet failed to arm interface, verwenden Sie stattdessen airodump-ng + aireplay-ng. Für Mesh / IBSS wählen Sie AWUS036ACM / ACHM."
draft: false
---

**Kernaussagen (TL;DR)**: Laut Praxistest von Yopitek (ALFA-Network-Distributor Taiwan) läuft der AWUS036ACS auf dem ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17) ohne Treiberinstallation, mit Dual-Band-Monitor und AP (5G-AP nutzbar: 802.11a, 20 MHz getestet; VHT80 nicht getestet); Injektion 2,4G 100 %, 5G 96 %, End-to-End-.22000 bestanden, kein Mesh / IBSS.

> Dieser Artikel ist Yopiteks Protokoll eines praktischen Kompatibilitäts- und Fähigkeitstests des ALFA AWUS036ACS auf einer aktuellen Linux-Plattform, gedacht zur Unterstützung der Produktauswahl.
> Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Alle Werte sind Auszüge aus Yopiteks Praxistests auf **eigener Hardware, im eigenen Büro-WLAN** (SSID `YUPITEK`, 2,4G ch5 / 5G ch36) gegen **eigene Testgeräte** (Apple iPhone 7 Plus); MAC-Adressen sind teilweise verdeckt.
> ⚠️ **Rechtlicher Hinweis und Geltungsbereich**: Monitor, Injection und Handshake-Erfassung erfolgen ausschließlich in Netzwerken und auf Geräten, die Ihnen gehören oder für die Sie eine Genehmigung haben; im AP-Modus halten Sie bitte die lokalen Funkvorschriften ein. Dieser Artikel konzentriert sich auf die Fähigkeiten, Kompatibilität und Konfiguration der Karte selbst und **umfasst keinerlei Angriffsoperationen gegen fremde Netzwerke**.

---

## 1. Diese Karte und die Testplattform

Der AWUS036ACS ist die leichte, mobile WLAN-Karte der ALFA-Produktlinie, Chip Realtek RTL8811AU, Generation Wi-Fi 5 (802.11ac), 1x1 mit einem räumlichen Datenstrom. Die Positionierung ist schlicht: kompakt, stromsparend, Einzelantenne – eine Karte zum Mitnehmen für die Bestandsaufnahme vor Ort, keine schwere Karte für höchsten Durchsatz oder größte Reichweite. Bei ihrer Bewertung geht es daher nicht darum, „wie schnell sie ist“, sondern darum, „welche praktischen Fähigkeiten bei so leichter Spezifikation noch vollständig nutzbar sind“.

In dieser Testrunde wird sie in ein typisches Betriebsszenario gestellt: Die interne Netzwerkkarte des GX10 (`wlP9s9`) übernimmt die Anbindung nach außen, der AWUS036ACS läuft per USB extern und trägt nur die Testaufgaben. So berührt der Wechsel in den Monitor- oder AP-Modus das Netzwerk des Hosts selbst nicht. Durchgehend wird nur die zur ALFA-Karte gehörige `wlx*`-Schnittstelle bedient, die interne Uplink-Karte wird nicht angefasst.

| Punkt | Inhalt |
|---|---|
| Modell | AWUS036ACS |
| Chip | Realtek RTL8811AU (Wi-Fi 5 / 802.11ac, 1x1 Single-Stream) |
| USB-ID | `0bda:0811` |
| Treiber | `rtw88_8821au` (in-kernel, in kernel 6.17 enthalten) |
| Firmware | 42.4.0 (im dmesg gemessen) |
| Plattform | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| Testgerät | Apple iPhone 7 Plus |

---

## 2. Hardware und Treiber (ohne Installation)

Diese Karte wird am GX10 direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS. Der Chip RTL8811AU / RTL8821AU wurde seit Mainline-Kernel 6.13 offiziell in Realteks kernel-interne `rtw88`-Treiberfamilie aufgenommen; das kernel 6.17 des GX10 bringt das Modul `rtw88_8821au` bereits mit, es muss kein Out-of-Tree-Projekt mehr von GitHub geladen werden. (Anders als in älteren Installationsanleitungen: Frühere Artikel setzten den `morrownr`-Out-of-Tree-Treiber oder einen älteren Kernel voraus und sprachen von einer nötigen DKMS-Kompilierung in Eigenregie; unter dem in-kernel-Treiber von kernel 6.17 ist das nicht mehr nötig.) Das früher gebräuchliche `morrownr/8821au-20210708` ist inzwischen auf legacy umgestellt (nur noch für Kernel unter 6.13 empfohlen, und nach seiner Installation wird der integrierte Treiber geblacklistet); auf neuen Kerneln gibt es keinen Grund mehr, diesen alten Weg zu gehen. Der Vorteil bei den Betriebskosten ist noch konkreter: Der in-kernel-Treiber wird zusammen mit dem Kernel aktualisiert, Nutzer müssen keine eigenen Branches pflegen und bleiben nicht bei jedem Upgrade an einer fehlgeschlagenen DKMS-Kompilierung hängen; derselbe Ablauf lässt sich über mehrere Kernel-Updates hinweg wiederverwenden. Die Firmware kommt mit `linux-firmware` im System mit, an diesem Gerät gemessen 42.4.0, und muss ebenfalls nicht manuell behandelt werden.

Bestätigen, dass die Karte erkannt, der Treiber gebunden und die Schnittstelle entstanden ist:

```bash
lsusb | grep -i 0bda:0811
# Bus 003 Device 004: ID 0bda:0811 Realtek Semiconductor Corp. Realtek 8812AU/8821AU 802.11ac WLAN Adapter

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"
cat /sys/class/net/$IF/phy80211/name
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# IF=wlx00c0cabce039 / phy1 / rtw88_8821au
```

Die Firmware-Version lässt sich aus `dmesg` bestätigen (gemessen 42.4.0):

```bash
sudo dmesg | grep -i 8821au
# rtw88_8821au ... Firmware version 42.4.0, H2C version 0
```

Die deklarierten unterstützten Schnittstellenmodi (sie bestimmen, welche Fähigkeiten später nutzbar sind):

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
# IBSS / managed / AP / AP/VLAN / monitor
```

Diese Liste führt `IBSS / managed / AP / AP/VLAN / monitor` auf. Hier ist besonders zu beachten: Obwohl die Liste IBSS aufführt, zeigt `iw link` nach einem `ibss join` im Test dennoch Not connected – es kommt keine Verbindung zustande; mesh, active-monitor und P2P stehen gar nicht erst auf der Liste (Details siehe die Grenzen in Abschnitt 4). Das ist der Hardware- und Treiberstand des RTL8811AU und hat nichts mit der Antennenzahl zu tun.

Bandabdeckung: 2,4 GHz ch1–13 (ch14 disabled); 5 GHz ch36–165 (davon ch52–144 als radar / DFS markiert). Die Standard-regdomain ist `TW`, TX-Leistung 2,4 GHz 30 dBm, 5 GHz UNII-1/2 23 dBm, UNII-3 30 dBm.

---

## 3. Getestete Fähigkeiten: Monitor / Injection / AP / WPA3

Zuerst die zentrale Fähigkeits-Gesamttabelle, danach Punkt für Punkt. Alle Punkte wurden am eigenen YUPITEK-AP + eigenem iPhone 7 Plus durchgeführt.

| Fähigkeit | 2,4 GHz | 5 GHz |
|---|---|---|
| Monitor (Mithören/Empfang) | ✅ stark | ✅ stark |
| Injection (Paket-Injektion) | ✅ **100 %** (30/30) | ✅ **96 %** (29/30, reg vorher entsperren) |
| AP-Hotspot (hostapd) | ✅ iPhone verbunden + Handshake abgeschlossen | ✅ **stabil** (802.11a, 20 MHz getestet; VHT80 nicht getestet) |
| AP WPA3-SAE | Nicht getestet | ✅ iPhone verbunden (SAE-only + PMF) |

### 3-1. Monitor (Monitor-Modus, 2,4 GHz + 5 GHz) ✅

Nach dem Wechsel in den Monitor-Modus wurde auf sechs Kanälen je eine Erfassung fester Länge durchgeführt, der Empfang war durchweg normal. Beliebte Kanäle erreichen in 6 Sekunden die Erfassungsobergrenze von 300 Frames:

| Kanal | erfasste Frames |
|---|---|
| ch1 / 2412 | 300 |
| ch6 / 2437 | 300 |
| ch11 / 2462 | 146 |
| ch36 / 5180 | 300 |
| ch149 / 5745 | 141 |
| ch157 / 5785 | 154 |

Sowohl 2,4 GHz als auch 5 GHz empfangen stabil. Für eine Einzelantennen-Mobilkarte reicht dieses Empfangsverhalten für die Kanalbestandsaufnahme vor Ort und die Paketdiagnose. Die niedrigeren Frame-Zahlen auf ch11, ch149 und ch157 kommen daher, dass auf diesen Kanälen aktuell ohnehin wenig Funkverkehr herrscht, nicht daher, dass die Karte nichts empfängt; die beliebten ch1, ch6, ch36 füllen in sechs Sekunden die 300-Frame-Obergrenze – der Empfang ist offensichtlich nicht ihr Engpass.

### 3-2. Injection (Paket-Injektion) ✅

Mit `aireplay-ng --test` wird ein gerichteter Injektionstest gegen den eigenen YUPITEK-AP gemacht. Auf 2,4 GHz werden 100 % erreicht (30/30, `Injection is working!`), auf 5 GHz 96 % (29/30). Auf 5 GHz ist ein Konfigurationsdetail zu beachten: Das Standard-`reg=TW` sperrt das aktive Senden in Teilen der UNII-Bänder; vor dem Test zuerst mit `sudo iw reg set US` entsperren und nach dem Test mit `sudo iw reg set TW` zurücksetzen.

```bash
# 2,4 GHz (YUPITEK tatsächlich auf ch5 / 2432)
sudo iw dev $IF set freq 2432
sudo aireplay-ng --test --ignore-negative-one -a <YUPITEK-BSSID> $IF
# Injection is working!  30/30: 100%  Power: -60.00
```

Dass eine Einzelantennen-Karte auf 2,4 GHz 100 % und auf 5 GHz 96 % erreicht, ist bereits eine recht zuverlässige Injektionsfähigkeit und zugleich die Grundlage dafür, dass sie später die End-to-End-Handshake-Erfassung bewältigen kann.

### 3-3. AP-Hotspot (2,4 GHz / 5 GHz) ✅

Mit `hostapd` wird die Karte zur Basisstation; bei allen drei Konfigurationen verbindet sich das iPhone 7 Plus erfolgreich und schließt den 4-Way-Handshake ab (`EAPOL-4WAY-HS-COMPLETED`):

- **5 GHz (802.11a, 20 MHz getestet; VHT80 nicht getestet)**: die stabilste Konfiguration, iPhone verbunden, Handshake abgeschlossen, `AP-DISABLED` sauberer Abschluss.
- **2,4 GHz (WPA2-PSK)**: iPhone verbunden, Handshake abgeschlossen, nach dem Trennen sauber geschlossen. Hier wird ehrlich ein Umstand notiert: In einer vorherigen Runde trat bei derselben Konfiguration nach dem Trennen der STA einmal `key not allowed / Failed to set beacon parameters` auf und brach ab; beim Nachtest ließ es sich nicht reproduzieren, bewertet als gelegentliches beacon re-key von rtw88_8821au, kein fester Defekt. Bei Szenarien mit langer Dauer und häufiger Neuverbindung sollte man dennoch aufmerksam bleiben oder gleich einen 5-GHz-AP verwenden.
- **WPA3-SAE (5 GHz, PMF erzwungen; 2,4 GHz nicht getestet)**: Entscheidende Einstellungen sind `wpa_key_mgmt=SAE` (reines WPA3, kein WPA2-Fallback), `ieee80211w=2` (erzwungener Management Frame Protection), `sae_pwe=0` (kompatibel zu älteren Endgeräten). Das iPhone 7 Plus (iOS 15) verbindet sich per SAE erfolgreich. Da der AP nur SAE öffnet und keinen WPA2-Rückweg hat, bedeutet eine gelungene Assoziation, dass der SAE-Authentifizierungs-Handshake zustande kommt. RTL8811AU + rtw88_8821au ist auf der AP-Seite WPA3-SAE-tauglich.

---

## 4. End-to-End-Handshake-Fähigkeit und Grenzen

### 4-1. End-to-End-Handshake-Erfassung ✅

Das ist der zusammenfassende Test, ob Injektion plus Erfassung tatsächlich „zusammengeführt“ werden können, durchgehend auf dem eigenen YUPITEK-AP, dem eigenen iPhone 7 Plus und unter autorisierter Voraussetzung durchgeführt. Der Ablauf ist: zum Zielkanal monitoren → dem eigenen Gerät ein gerichtetes deauth senden, um eine Neuverbindung auszulösen → den vollständigen 4-Way (M1–M4) erfassen → mit `hcxpcapngtool --all` in eine hashcat-lesbare `.22000` exportieren.

Testergebnis: `aircrack-ng` stellt für YUPITEK 1 Handshake fest, die vier EAPOL-Nachrichten M1–M4 sind alle vollständig, der Client ist eine Apple-OUI (`b8:53:ac`, bestätigt als iPhone 7 Plus), die exportierte `.22000` kann direkt an hashcat gefüttert werden. Das bedeutet, dass der AWUS036ACS über eine vollständige End-to-End-Handshake-Erfassungsfähigkeit verfügt.

Zwei Testpunkte sind festzuhalten (die vollständige Schritt-für-Schritt-Konfiguration siehe gesonderter Artikel):

1. **Wenn im Büro mehrere APs mit gleichem Namen auf demselben Kanal liegen, nicht mit `--bssid` auf einen einzelnen fixieren**, sondern den gesamten Kanal erfassen, damit kein auf einem anderen AP verbundenes Gerät übersehen wird.
2. `hcxpcapngtool` ist standardmäßig strenger und kann „not enough M1“ melden; mit `--all` wird aus dem vollständigen M1–M4 eine `.22000` exportiert.

Die für diese Handshake-Erfassungskette genutzten, in Kali gebräuchlichen Werkzeuge (aircrack-ng, hcxtools) laufen direkt unter Ubuntu 24.04 ARM64; airodump-ng, aireplay-ng und hcxpcapngtool funktionieren alle normal.

### 4-2. VIF (virtuelle Schnittstellen) ✅

`iw dev $IF interface add mon9 type monitor` kann eine monitor-VIF aufbauen und erfasste 100 Frames; zusätzlich wurde per Skript „Hauptschnittstelle mit YUPITEK als STA verbunden + eine AP-VIF“ aufgebaut – ein Einzelchip kann zugleich STA und AP spielen.

### 4-3. Ehrliche Grenzen (gemessene Meldungen)

| Erweiterter Modus / Werkzeug | Status | Messung |
|---|---|---|
| Active monitor | ❌ nicht unterstützt | `iw set monitor active` → `Operation not supported (-95)` |
| Ad-hoc (IBSS) | ❌ nicht unterstützt | Modus aufgelistet, aber nach `ibss join` zeigt `iw link` = Not connected |
| Mesh (802.11s) | ❌ nicht unterstützt | `set type mp` → `-95` |
| Wi-Fi Direct (P2P) | ❌ nicht unterstützt | `interface add type __p2pcl` → `-95` |
| hcxdumptool 8.x | ⚠️ kann nicht armen | `failed to arm interface`: rtw88_8821au bietet kein active-monitor; verwenden Sie airodump-ng + aireplay-ng |

Außerdem sind zwei betriebliche Grenzen zu kennen. Der Single-Stream 1x1 bestimmt die theoretische Obergrenze (HT Max RX 150 Mbps, VHT80 etwa 433 Mbps), Durchsatz ist ohnehin nicht ihre Stärke. Nach wiederholtem Wechsel zwischen monitor / AP kann der RX gelegentlich kurzzeitig degraded sein (nichts wird gescannt); dann stellt ein einmaliges physisches Aus- und Einstecken der Karte den Zustand wieder her, der Schnittstellenname wird durch die MAC bestimmt und bleibt beim Aus- und Einstecken gleich.

---

## 5. Einsatzszenarien und Auswahl (leicht und mobil, zurück zum Hub)

Überträgt man diese Fähigkeiten auf die Produktpositionierung, ist die Rolle des AWUS036ACS klar: eine Karte mit vollständigen Fähigkeiten, die aber vor allem auf Mobilität setzt. Wofür eignet sie sich also?

- **Schnelle Bestandsaufnahme vor Ort / mobile Diagnose**: Einzelantenne, kleines Format, geringer Stromverbrauch – geeignet, um unterwegs Kanalbestandsaufnahmen, Signalkontrollen und Paketdiagnosen durchzuführen. In Kombination mit einer zentralen Plattform wie dem GX10 erfasst die Mobilkarte vor Ort und spielt die Daten zur zentralen Analyse an den Hub zurück – eine klare Arbeitsteilung.
- **Schulung und Verifizierung**: Monitor / Injection / AP / WPA3-SAE / End-to-End-Handshake – diese gesamte Hauptlinie bewältigt sie, geeignet als Demonstrations- und Verifizierungskarte im autorisierten Rahmen.
- **Ungeeignete Szenarien**: Für höchsten Durchsatz, größte Reichweite oder Bedarf an Mesh / IBSS / P2P / active-monitor ist diese Karte nicht die richtige Wahl.

Leicht heißt nicht funktionsreduziert. An der Hauptlinie fehlt ihr keine einzige Fähigkeit; abgewogen wurden die Durchsatz-Obergrenze und die erweiterten Schnittstellenmodi. Ob Sie sie wählen, hängt also davon ab, ob Sie „mitnehmen“ oder „voll ausfahren“ wollen.

Im Vergleich mit der eigenen Produktfamilie ergeben sich folgende Positionierungsunterschiede:

| Bedarf | Empfohlene Karte | Grund |
|---|---|---|
| Leicht und mobil + vollständige Hauptlinie | **AWUS036ACS** | 2,4G-Injektion 100 %, 5G 96 %, End-to-End-Handshake nutzbar, Einzelantenne und leicht |
| Durchgängig 100 % Dual-Band-Injektion / robustere Penetrationsverifizierung | AWUS036EACS, AWUS036ACH | Injektion in beiden Bändern 100 %, EACS zusätzlich mit BT |
| Stärkster Empfang / Monitor über große Distanz | AWUS036AXER, AWUS036ACH | mehr Ziele durch Frequenzsprünge / hoher Gewinn durch Doppelantenne |
| Mesh- / IBSS-Einzelgerät-Experiment | AWUS036ACM, AWUS036ACHM | mt76-Treiber im Einzelbetrieb aufbaubar (Realtek rtw88 nicht unterstützt) |

Auswahl in einem Satz: Wer leicht und zugleich vollständige Hauptlinien-Fähigkeiten will, für den ist der AWUS036ACS die passende mobile Wahl; wer durchgängig 100 % Dual-Band-Injektion oder eine schwerere Penetrationsverifizierung braucht, geht Richtung EACS / ACH.

---

## Häufig gestellte Fragen (FAQ)

**F: Benötigt der AWUS036ACS unter Ubuntu 24.04 ARM64 einen Treiber?**
Auf dem in diesem Artikel getesteten kernel 6.17 (ASUS GX10) nicht: Der RTL8811AU wird vom integrierten rtw88_8821au getrieben, direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS. Bei älterem Kernel prüfen Sie zuerst mit `modinfo rtw88_8821au`, ob das Modul vorhanden ist.

**F: Unterstützt der AWUS036ACS den Monitor-Modus und Packet Injection?**
Ja. Sowohl 2,4 GHz als auch 5 GHz können in den Monitor-Modus; die `aireplay-ng --test`-Injektion liegt auf 2,4G bei 100 % (30/30), auf 5G bei 96 % (29/30, vorher `iw reg set US` nötig, um die TW-Beschränkung aufzuheben). Active monitor wird nicht unterstützt.

**F: Kann der AWUS036ACS einen WPA-Handshake erfassen und in hashcat .22000 umwandeln?**
Ja. Auf dem eigenen AP und dem eigenen iPhone 7 Plus End-to-End getestet: gerichtetes deauth löst eine Neuverbindung aus, der vollständige 4-Way (M1–M4) wird erfasst und dann mit `hcxpcapngtool --all` in .22000 exportiert. Nur in eigenen oder autorisierten Netzwerken.

**F: Kann der AWUS036ACS als AP-Hotspot dienen? Unterstützt er WPA3?**
Ja. `hostapd` öffnet 2,4G- und 5G-Hotspots (5G wurde als 802.11a mit 20 MHz getestet; VHT80 wurde nicht getestet), das iPhone 7 Plus verbindet sich und schließt den 4-Way ab; auch das WPA3-SAE auf 5G (SAE-only, ieee80211w=2, sae_pwe=0) verbindet sich erfolgreich (WPA3 auf 2,4G wurde nicht getestet).

**F: Welche Modi unterstützt der AWUS036ACS nicht? Funktioniert hcxdumptool?**
Nicht unterstützt werden active monitor, IBSS, Mesh (802.11s) und Wi-Fi Direct (P2P). hcxdumptool 8.x meldet failed to arm interface, verwenden Sie stattdessen airodump-ng + aireplay-ng. Für Mesh / IBSS wählen Sie AWUS036ACM / ACHM.

---

## 6. Weiterführende Literatur

- Vollständiger Fähigkeitsvergleich und Gesamtbewertung der neun ALFA-Karten → [Gesamtbewertungs-Hub der ALFA-WLAN-Karten (Gesamttabelle)](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Ohne Treiberinstallation: Monitor / AP unter Ubuntu 24.04 + kernel 6.17 aktivieren (rtw88 / rtw89 / mt76 im Praxistest)](/de/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- [Schritt-für-Schritt-Anleitung zu WPA3-SAE und End-to-End-Handshake-Erfassung](/de/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- BT+WiFi-Kombikarte derselben Familie → [AWUS036EACS im Einzelkartentest](/de/blog/awus036eacs-asus-gx10-ubuntu-test-report/)

---

*Testinstanz: Yopitek (ALFA-Network-Distributor Taiwan) — https://www.yupitek.com | Testumgebung: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Testgerät: Apple iPhone 7 Plus*
