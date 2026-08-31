---
title: "Edge-AI-Bandbreitenengpass überwinden: Hochleistungs-WLAN-Karte für 6GHz-Videostreaming auf dem NVIDIA Jetson Orin Nano"
description: "Die ALFA AWUS036AXML Wi-Fi 6E-Karte auf dem Jetson Orin Nano verlagert Multi-Stream-RTSP-4K-Video in das 6GHz-Band – mit A/B-Tests von iperf3 und GStreamer."
date: 2026-08-31
author: benny-lai
lastmod: 2026-08-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["jetson-orin-nano", "wifi-6e", "awus036axml", "6ghz", "rtsp", "edge-ai", "nvidia"]
featureimage: "/images/blog/jetson-orin-nano-wifi-6e-6ghz-high-bandwidth-streaming.webp"
---

> **Zielplattform**: NVIDIA Jetson Orin Nano Developer Kit, JetPack 6.x (Basis Ubuntu 22.04 LTS, Linux Kernel 5.15 / 6.1)
> **Leitfaden-Hardware**: ALFA AWUS036AXML (MediaTek MT7921AU-Chipsatz, Wi-Fi 6E-Triband-USB-Adapter)
> **Einordnung dieses Artikels**: Diese Lösung ist eine Bench-Test-Bewertung für eine DIY-Open-Source-Plattform für akademische/technische Entwicklung – keine offizielle Unterstützung für ein kommerzielles Produkt und keine offizielle Zertifizierung durch einen Hersteller geschlossener Plattformen.

## Einleitung: Woher kommt die „Bandbreitendecke“ bei Edge-Geräten?

Einen Jetson Orin Nano an einen Access Point (AP) anzuschließen und zwei oder drei IP-Kameras zu betreiben, wirkt ganz normal. Doch wenn du mehrere **4K-Livestreams** tatsächlich in die GPU zur Inferenz schickst, spüren viele zum ersten Mal die Grenzen des drahtlosen Netzwerks:

- Die Bildqualität fällt ständig ab (der Bitrate kommt nicht hoch, das Bild wird neblig oder blockig).
- Die Latenz schwankt, und die „zeitliche Verschiebung“ der Inferenz von Video-KI-Modellen wird immer deutlicher.
- Die Planung hängt, der Bildschirm der Steuerzentrale wird schwarz – und die Ursache ist „drahtloser Paketverlust“.

Dieser Artikel zerlegt die Bandbreiten-Herausforderung von „Multi-Stream-RTSP-4K-Streaming am Edge“ aus drei Blickwinkeln: **physische Schicht → Konfigurationsschicht → Messschicht**. Anschließend zeigt er, wie du den **AWUS036AXML Wi-Fi 6E-Adapter** an einen **Jetson Orin Nano (JetPack / Ubuntu 22.04 LTS)** anschließt und in das saubere **6GHz-Band** wechselst. Am Ende belegen die Daten, „warum 6GHz die erste Wahl für diese Art von Arbeitslast ist“.

Wenn du noch nicht entschieden hast, ob du diese Karte kaufen willst, springe direkt zur „Checkliste zur Kompatibilitätsprüfung vor dem Kauf“ in Kapitel 4 und hake jeden Punkt ab.

---

## 1. Multi-Stream-RTSP-4K-Streaming am Edge: Bandbreiten- und Interferenz-Herausforderungen im drahtlosen Netzwerk

### 1.1 Erst rechnen: Wie viel Bandbreite braucht ein 4K-Stream?

RTSP (Real-Time Streaming Protocol) ist nur ein Protokoll für „Handshake und Steuerung“ – die eigentlichen Videodaten reisen in RTP-Paketen. Am Beispiel typischer kommerzieller IP-Kamera-Ausgänge:

| Kamera-Ausgang | Codec | Realer Durchsatz pro Stream (je nach Qualitätseinstellung) |
|---|---|---|
| 1080p30 | H.264 | ca. 4 – 8 Mbps |
| 4K (2160p)30 | H.264 | ca. 20 – 35 Mbps |
| 4K (2160p)30 | H.265 | ca. 10 – 20 Mbps |
| 4K (2160p)30 (Einstellungen mit hohem Bitrate und niedriger Latenz) | H.264 | bis zu 45 Mbps+ |

> **Kernpunkt**: 4K ist ein Monster – **jeder Stream verbraucht das 2,5–8-fache der Bandbreite von HD**. Vier gleichzeitige 4K/H.264-Streams auf das Board entsprechen **80–140 Mbps „effektiver Nutzlast“**. Beachte: **effektive Nutzlast**, nicht die drahtlose PHY-Rate – der Unterschied zwischen beiden beträgt fast das Doppelte (siehe 1.3).

### 1.2 Paketverlust ≠ Signalproblem: Das drahtlose Medium ist halbduplex und geteilt

Viele denken: „Wenn das Signal voll ist, gibt es kein Problem.“ Doch in Edge-Umgebungen ist der wahre Killer die **Überlastung**:

- **In 2.4GHz bleiben nur 3 überlappungsfreie Kanäle**: Bluetooth, Mikrowellenherde und die APs der Nachbarwerke drängen sich hier alle. Durch den Backoff-Mechanismus von CSMA/CA halbiert sich der Durchsatz mit jedem weiteren Gerät – und halbiert sich erneut.
- **5GHz ist besser, aber immer noch ein Schlachtfeld**: Die 5GHz-Dichte in Wohnungen, Büros und Fabriken treibt die Kanalauslastung an die Grenze.
- **Drahtlos ist ein geteiltes Medium**: Egal wie hoch die PHY-Rate ist – wenn jemand anderes auf dem Kanal ist, müssen deine Pakete warten. Die TCP-Überlastungssteuerung senkt die Geschwindigkeit dadurch kontinuierlich.

### 1.3 Warum „PHY 2400 Mbps“ nicht „Übertragung von 2400 Mbps“ bedeutet?

Der drahtlose Durchsatz erleidet viele Abschläge – das ist eine physikalische Tatsache:

1. **Protokoll-Overhead**: Wi-Fi-Frame-Header, ACK, Beacon und das CSMA/CA-Konkurrenzfenster fressen etwa 30–50 % der PHY-Rate.
2. **Umgebungsverluste**: Entfernung, Wände und Metallreflexionen zwingen die PHY-Schicht zur automatischen Herabstufung (vom höchsten MCS zum niedrigeren MCS).
3. **Bidirektionale Planung**: Video-Upload (Uplink) und Steuerungs-Download (Downlink) teilen sich denselben drahtlosen Link.

Eine Karte der Klasse 2400 Mbps **liefert in einer sauberen Umgebung also typischerweise 600–900 Mbps echte Nutzlast** – mehr als genug für Multi-Stream-4K (80–140 Mbps). Aber **sobald sie in einen überlasteten 2.4G/5G-Kanal gerät, fallen reale Messungen oft auf 100–300 Mbps** – ein sofortiger Engpass.

### 1.4 Drei „Basiswerte“, die du zuerst messen solltest

Bevor du irgendwelche Hardware änderst, halte die aktuellen Zahlen fest (diese Daten dienen auch als Intake-Übergabe für den After-Sales-Support):

```bash
# 1) Kernel und System
uname -r
grep PRETTY /etc/os-release

# 2) Aktuelle drahtlose Schnittstelle und Signal
iw dev                      # drahtlose Schnittstellen auflisten
iw dev wlan0 link           # aktuellen AP, Kanal, RSSI und Bitrate anzeigen

# 3) Kanalauslastung auf AP-Seite (auf dem AP ausführen oder im AP-WebUI prüfen)
#    Basislinie für Verbindungsprüfung
ping -c 60 -i 1 <AP_GATEWAY_IP>
```

Notiere RSSI, Bitrate, Ping-Latenz und Paketverlustrate der „alten Karte / alten Bandes“ – am Ende von Kapitel 3 vergleichst du sie mit 6GHz.

---

## 2. Einrichtung des AWUS036AXML Wi-Fi 6E unter JetPack (Ubuntu 22.04 LTS)

### 2.1 Prüfe zuerst deine JetPack-Kernel-Version

Der Kernvorteil des AWUS036AXML: **Der `mt7921u`-Treiber des MediaTek MT7921AU-Chipsatzes ist nativ in den Linux-Mainline-Kernel integriert** (seit Kernel 5.18 enthalten) – **kein Treiber-Kompilieren von GitHub nötig**. Aber „native Unterstützung“ hat eine Hürde; prüfe zuerst deine Kernel-Version:

```bash
uname -r
```

Referenztabelle:

| JetPack | Basis-Betriebssystem | Linux Kernel | Unterstützung für AWUS036AXML |
|---|---|---|---|
| JetPack 5.1.x | Ubuntu 20.04 (selbst prüfen) | 5.10 | Treiber muss geprüft werden; wir empfehlen, direkt auf JetPack 6.x zu aktualisieren |
| JetPack 6.0 / 6.1 | Ubuntu 22.04 LTS | 5.15 | Je nach Kernel-Version; zuerst `modinfo mt7921u` ausführen |
| JetPack 6.2+ (empfohlen) | Ubuntu 22.04 LTS | 6.1 | `mt7921u` nativ eingebaut, Plug-and-Play |

Prüfe, ob Treiber und Firmware bereit sind:

```bash
modinfo mt7921u                         # mit Ausgabe = Treiber ist im Kernel eingebaut
sudo apt update
sudo apt install linux-firmware         # sicherstellen, dass die MediaTek-Firmware aktuell ist
sudo reboot
```

> **Unterstützungsgrenze (Support Reduction)**: Der AWUS036AXML **unterstützt kein macOS (weder Intel noch Apple Silicon)**. JetPack läuft nur in der exklusiven Ubuntu-22.04-LTS-Umgebung von Jetson, und alle Befehle in diesem Artikel setzen Linux voraus; wenn dein Entwicklungsrechner ein Mac ist, nutze stattdessen einen beliebigen Linux-Rechner als Edge-Computing-Knoten.

### 2.2 Den Adapter an den Jetson anschließen: USB-Ports und Stromversorgung

Das Jetson Orin Nano Developer Kit bietet 2 USB-3.2-Type-A-Ports (blau) und 2 USB-2.0-Ports. Der AWUS036AXML nutzt eine **USB-C-3.2-Gen1-Schnittstelle** und wird mit einem 2-in-1-Kabel (USB-C auf USB-A) für Strom und Daten geliefert:

```bash
# Nach dem Anschließen prüfen, ob das Gerät auf USB-Ebene erkannt wird (VID:PID des MediaTek MT7921AU ist 0e8d:7961)
lsusb | grep -i mediatek
```

**Stromversorgungs-Hinweis (häufiger Killer in der Praxis)**:

- Der AWUS036AXML verbraucht maximal etwa **2.7W** – das direkte Einstecken in den USB-3.2-Port des Jetson ist normalerweise kein Problem.
- Wenn du mehrere Hochleistungs-Adapter, eine externe SSD und USB-Kameras gleichzeitig betreibst, **empfehlen wir einen USB-Hub mit eigener Stromversorgung (Powered Hub)**, um Spannungseinbrüche zu vermeiden, die den Adapter „kommen und gehen“ lassen.
- Verwende keine Verlängerungskabel oder Frontpanel-Verteiler – je kürzer und dicker das USB-Kabel, desto besser.

### 2.3 Verbindung zum Access Point und Fixierung des Bandes

JetPack verwaltet drahtlose Netzwerke mit NetworkManager:

```bash
# Scannen und Verbinden
nmcli device wifi list
nmcli device wifi connect "DEIN_SSID" password "DEIN_PASSWORT"
```

**Band-Fixierung (entscheidender Schritt)**: Der `nmcli band`-Wert ist `bg` für 2.4GHz und `a` für 5GHz; **das 6GHz von Wi-Fi 6E nutzt `a` (erweitert)**. Der zuverlässigste Weg ist, auf der **AP-Seite** eine dedizierte SSID „**nur 6GHz**“ anzulegen und Band Steering zu deaktivieren; der Client bestätigt dann über den physischen Kanalinhalt, in welchem Band er wirklich verbunden ist:

```bash
# Aktuellen Verbindungskanal prüfen (6GHz-Frequenzen liegen zwischen 5925–7125 MHz)
iw dev wlan0 link

# Saubere Bestätigungsmethode: direkt sehen, in welches Band die Frequenz fällt
iw dev wlan0 link | grep -i freq
#   2.4GHz → 2400-2500 MHz
#   5GHz   → 4900-5900 MHz
#   6GHz   → 5925-7125 MHz (nur Wi-Fi 6E)
```

Wenn du nicht willst, dass der Client in die überlasteten 2.4/5GHz-Bänder roamt, fixiere ihn in den Verbindungseinstellungen:

```bash
nmcli c show --active                       # Verbindungsnamen finden
nmcli con mod "VERBINDUNGSNAME" 802-11-wireless.band a
nmcli con up "VERBINDUNGSNAME"
```

> **Regulatorischer Hinweis**: Ob das 6GHz-Band verfügbar ist, hängt von den Vorschriften deines Landes/deiner Region und der **AP-Firmware** ab. In Taiwan zum Beispiel hat die NCC für 6GHz den Bereich **5945–6425 MHz** freigegeben, **nur für den Einsatz in Innenräumen mit geringer Leistung** – nicht den vollen Bereich 5925–7125 MHz. Wenn `iw reg get` eine Regulatory Domain ohne 6GHz anzeigt oder der AP 6GHz nicht aktiviert hat, verbindet sich die Karte einfach nicht – das ist kein Hardware-Fehler, sondern ein regulatorisches/Konfigurationsproblem.

---

## 3. 6GHz vs. überlastete 2.4G/5G: gemessene Bandbreite und Latenz

> Der Geist der Messung: **derselbe Jetson, dieselbe Karte, derselbe AP, dieselbe Entfernung** – nur das Band wechselt, alle anderen Bedingungen bleiben gleich. Nur so ist der gemessene Unterschied der Unterschied des „Bandes“ selbst.

### 3.1 Gestalte dein kontrolliertes Experiment

| Variable | Kontrollmethode |
|---|---|
| AP-Position | Fix; alle drei Bänder teilen sich denselben Wi-Fi-6E-AP |
| Entfernung | Fix (z. B. 3 Meter in gerader Linie ohne Hindernisse) |
| Zeitfenster | Gleicher Tag, ähnliche Uhrzeit (Überlastung von 2.4/5GHz wird vor Ort gemessen) |
| Adapter | Derselbe AWUS036AXML, nur die SSID wechselt |
| Interferenz-Umgebung | Bestehende Störungen bleiben (genau das ist der Sinn der „echten Messung“) |

### 3.2 Messung 1: RSSI und Durchsatz der Einzelverbindung (iperf3)

Installiere iperf3 auf dem Jetson und verbinde ihn mit einem Empfangsrechner:

```bash
# Empfängerseite (z. B. ein anderer Computer oder Server)
iperf3 -s

# Jetson-Seite (Client, 60-Sekunden-Lauf bidirektional)
iperf3 -c <EMPFÄNGER_IP> -t 60 -R     # -R misst reverse (Jetson-Upload)
```

Führe den Test jeweils einmal auf **2.4GHz-SSID, 5GHz-SSID und 6GHz-SSID** aus und notiere `sender Mbps` und `receiver Mbps`. Du kannst auch zuerst die Verbindungsqualität prüfen:

```bash
iw dev wlan0 link                              # RSSI + aktueller PHY-Bitrate
iw dev wlan0 station dump | grep -E "signal|tx bitrate|rx bitrate"
```

### 3.3 Messung 2: Verbindung und Latenz (ping)

```bash
ping -c 60 -i 1 <EMPFÄNGER_IP> | tail -2
```

Notiere für alle drei Gruppen: **durchschnittliche Latenz (ms)**, **Paketverlustrate (%)** und **Latenz-Jitter (max-min)**.

### 3.4 Messung 3: echtes Multi-Stream-RTSP-4K-Streaming (GStreamer-Stresstest)

Durchsatz und Latenz sind nur indirekte Indikatoren; **wirklich zu prüfen ist, „wie viele 4K-Streams gleichzeitig dekodiert werden können, ohne Frames zu verlieren“**. JetPack enthält das NVIDIA-Hardware-Dekodierungs-Plugin für GStreamer 1.0 (`nvv4l2decoder`):

```bash
# Mit dem perf-Element die tatsächliche Dekodier-Framerate zählen (Abtastung alle 1 Sekunde)
gst-launch-1.0 \
  rtspsrc location="rtsp://KAMERA_IP/stream" ! \
  rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! \
  perf print-stats=true ! fakesink
```

Öffne mehrere Terminals, je eines pro 4K-Stream, und beobachte GPU/Speicher mit `nvidia-smi` (auf Jetson: `tegrastats`):

```bash
sudo tegrastats
```

**Bewertungskriterien**:
- Zeigt das `perf` jedes Streams eine **dropped/rendered-Framerate (FPS), die sich stabil der Quellrate (30fps) annähert** → bestanden.
- Wenn auf 2.4/5GHz Frames verloren gehen oder die Qualität fällt und sich nach dem Wechsel auf 6GHz die Stabilität erholt → das ist der gemessene Beweis für „Band-Überlastung“.

### 3.5 Ein Beispiel für erwartbare Messergebnisse

| Band | PHY-Bitrate | iperf3 real Upload/Download | Ping Ø/Jitter | Ergebnis Multi-Stream-4K |
|---|---|---|---|---|
| 2.4GHz (überlastetes Büro) | 300 Mbps | 80–120 Mbps | 8 ms / hoher Jitter, gelegentliche Verluste | Qualitätsabfall, nebliges Bild |
| 5GHz (mittlere Auslastung) | 800 Mbps | 400–550 Mbps | 3 ms / mittel | Läuft mühsam, gelegentliches Ruckeln |
| 6GHz (saubere dedizierte SSID) | 1200 Mbps | 700–900 Mbps | 1–2 ms / stabil | 2–4 4K-Streams, alles grün |

> Das ist der typische Kontrast zwischen „sauber und überlastet“. **Der Wert von 6GHz liegt darin, dass es ein brandneues Band ist, das fast niemand nutzt.** In Umgebungen mit vielen Kameras und überfüllten Wi-Fi-Geräten wird dieser Vorteil sofort zu stabiler Multi-Stream-4K-Kapazität.

---

## 4. Checkliste zur Kompatibilitätsprüfung vor dem Kauf (Pre-Purchase Checklist)

> Hake jeden Punkt vor der Bestellung ab. **Diese Liste vor dem Kauf auszufüllen, spart das Zehnfache an Aufwand gegenüber der Fehlersuche nach dem Kauf.**

### Schritt 1: Bestätige deine Edge-Computing-Plattform

| Prüfpunkt | So prüfst du | Ergebnis |
|---|---|---|
| Plattform-Modell | `cat /proc/device-tree/model` | \_\_\_\_\_ |
| JetPack-Version | `cat /etc/nv_tegra_release` (JetPack 6.x = L4T 36.x) | \_\_\_\_\_ |
| Linux Kernel | `uname -r` | \_\_\_\_\_ |
| Ist `mt7921u` eingebaut? | `modinfo mt7921u` | mit Ausgabe / ohne Ausgabe |

> Wenn `uname -r` unter 5.18 liegt und `modinfo mt7921u` keine Ausgabe liefert: aktualisiere zuerst JetPack (empfohlen 6.2+, Kernel 6.1), bevor wir über die Karte sprechen. **Kompiliere keine Nicht-Mainline-Treiber gewaltsam auf einem alten Kernel** – das macht sie nur zum Helden eines weiteren Fehlersuche-Artikels.

### Schritt 2: Bestätige deine drahtlose Umgebung

| Prüfpunkt | Optionen / Bedingungen |
|---|---|
| Unterstützt der AP Wi-Fi 6E (6GHz)? | Ja / Nein (ohne 6GHz-AP sind die Vorteile dieses Artikels nicht erreichbar) |
| Ist 6GHz auf AP-Seite aktiviert? | Ja / Nein (inkl. Regulatory-Domain-/Country-Code-Einstellungen) |
| Gibt es eine dedizierte SSID „nur 6GHz“ oder eine auf 6GHz fixierbare SSID? | Ja / Nein |
| Schätzung des Gesamtverkehrs der Kameras | Wie viele 4K-Streams? H.264/H.265? Gesamt ca. \_\_\_ Mbps |
| Entfernung und Hindernisse | Wie viele Meter? Gibt es Wände/metallische Abschirmungen? |

### Schritt 3: Bestätige den Unterstützungsumfang der Betriebssysteme

| Plattform | Unterstützungsstatus |
|---|---|
| Ubuntu 22.04 / 24.04 | ✅ Natives `mt7921u` (Kernel 5.18+; gilt für JetPack 6.2+) |
| Kali Linux | ✅ Native Unterstützung (Monitor Mode / Packet Injection) |
| Windows 11 | ✅ (6GHz-Band erfordert Windows 11 oder neuer) |
| Windows 10 | ✅ (aber ohne 6GHz-Band; nur 2.4/5GHz) |
| macOS (Intel / Apple Silicon) | ❌ **Nicht unterstützt** (kein MT7921AU-Treiber für macOS; nicht dafür kaufen) |
| Raspberry Pi / andere Linux-SBCs | ✅ (Kernel 5.18+, `linux-firmware` installieren) |

> **Erinnerung an die Unterstützungsgrenze**: Der AWUS036AXML **unterstützt kein macOS**. Wenn dein Hauptentwicklungsrechner ein Mac ist, funktioniert die Wi-Fi-Funktion dieser Karte auf deinem Mac nicht; stelle sicher, dass du einen Linux-Rechner oder eine Linux-SBC als Nutzungsplattform hast.

### Schritt 4: Stromversorgungs- und Port-Check

| Prüfpunkt | Empfehlung |
|---|---|
| Direkt am USB-Port des Hosts | Möglich (2.7W, geringer Verbrauch) |
| Mehrere Geräte gleichzeitig | **Powered USB Hub mit eigener Stromversorgung** verwenden |
| Antennenplatzierung | Zwei RP-SMA-5dBi-Rundstrahlantennen aufrecht, ≥ 5cm vom Metallgehäuse entfernt |

### Intake-Informationspaket für den Kundenservice

Wenn nach dem Kauf weiterhin Probleme auftreten, füge bei der Kontaktaufnahme mit dem technischen Support **alles auf einmal** bei: Plattform-Modell, JetPack-/Kernel-Version, `lsusb`-Ausgabe, `modinfo mt7921u`-Ergebnis, RSSI/Bitrate aus `iw dev wlan0 link` sowie AP-Modell mit Band-Einstellungen. Diese Informationen ermöglichen es dem Support, direkt zu beurteilen, ob es sich um „Regulierung nicht freigegeben“, „AP-Konfiguration“ oder „Hardware“ handelt.

---

## 5. Haftungsausschluss und Sicherheits-Rotlinien

Diese Lösung ist eine **Bench-Test-Bewertung für eine DIY-Open-Source-Plattform für akademische/technische Entwicklung** – keine offizielle Unterstützung für ein kommerzielles Produkt und kein Versprechen einer „plug-and-play-fähigen kommerziellen Turn-Key-Lösung“.

- **Kein macOS-Support**: Der AWUS036AXML hat keinen macOS-Treiber; die Abläufe dieses Artikels sind auf einem Mac nicht nutzbar.
- **Keine Behauptung offizieller Kompatibilität mit bestimmten geschlossenen Plattformen**: Dieser Artikel beschreibt nur den Jetson Orin Nano als Open-Source-Entwicklungsboard und allgemeine Linux-Umgebungen; wenn dein Ziel ein **kommerzielles Closed-Source-System (Drohnen/Roboter/Video)** ist, stellt der Inhalt dieses Artikels keine offizielle Zertifizierung durch dessen Hersteller dar; für drahtlose Umbauten wende dich an den technischen Support des Herstellers.
- **Keine sicherheitskritischen Systeme**: Wenn deine Anwendung zu industriellen sicherheitskritischen Steuerungssystemen (Safety-critical control systems) gehört, integriere die drahtlose Videoübertragung nicht direkt in die Sicherheitsschleife; halte kabelgebundene oder bestehende Sicherheitskanäle aufrecht.
- **Keine Anleitung zum Deaktivieren von Systemschutz**: Alle Einstellungen in diesem Artikel funktionieren bei aktiviertem Schutz; deaktiviere keine Firewalls, Secure Boot oder Ähnliches, um Netzwerkprobleme zu umgehen.
- **Einhaltung der Funkvorschriften**: Die Nutzung von 6GHz muss den Vorschriften deines Landes/deiner Region entsprechen; dieser Artikel erklärt nur die technische Konfiguration und stellt keine regulatorische Beratung dar.

---

## Fazit und Hardware-Empfehlungen

Wenn Multi-Stream-4K-Video in eine Edge-KI-Plattform gelangt, liegt der Engpass oft nicht an der Rechenleistung, sondern an der **drahtlosen Nutzlastkapazität und der Sauberkeit der Kanäle**. 2.4G/5G sind längst von Geräten überschwemmt; **das 6GHz von Wi-Fi 6E bietet einen brandneuen, störungsfreien Kanal** – kombiniert mit einer Karte mit nativem Treiber ohne Kompilierung kann der Jetson Orin Nano stabil 2–4 4K-Streams aufnehmen und das Problem der „Bandbreitendecke“ mit einem Schlag nach hinten verschieben.

**Empfohlene Hardware**: ALFA AWUS036AXML (MediaTek MT7921AU, native Unterstützung ohne Kompilierung ab Linux Kernel 5.18+, Wi-Fi 6E-Triband, zwei RP-SMA-5dBi-Hochgewinnantennen, 2.7W geringer Verbrauch). Der AWUS036AXMR auf derselben Chipsatz-Architektur ist das antennenlose Embedded-Modell – geeignet für platzbeschränkte Rack-Edge-Knoten.

**Nächster Schritt**: Führe zuerst die „Basiswert-Messungen“ aus Kapitel 1 durch, dann hake die Liste aus Kapitel 4 ab – bringe die Messdaten ins Feld und lass die Daten über deine Band-Strategie entscheiden.