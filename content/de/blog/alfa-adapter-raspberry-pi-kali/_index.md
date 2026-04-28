---
title: "ALFA WLAN-Adapter am Raspberry Pi mit Kali Linux: Einrichtungsanleitung"
description: "Installieren Sie ALFA USB WLAN-Adapter auf einem Raspberry Pi mit Kali Linux ARM64. Enthält Kompilierung des RTL8812AU-Treibers für AWUS036ACH, Monitor Mode und portable Pentesting-Setups."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["raspberry-pi", "kali-linux", "alfa-network", "AWUS036ACH", "RTL8812AU", "portable-pentest", "monitor-mode"]
---

Ein Laptop mit Kali Linux ist der Standard-Arbeitsplatz für Pentesting – aber bei weitem nicht die einzige Option. Ein Raspberry Pi 4 oder Pi 5 kombiniert mit einem ALFA USB WLAN-Adapter bietet dir eine kompakte, lüfterlose und passiv gekühlte Plattform, die in eine Jackentasche passt, über eine USB-C Powerbank betrieben werden kann und stundenlang unbeaufsichtigt in einer Zielumgebung gelassen werden kann. Kali Linux ARM64-Images kommen direkt von Offensive Security und laufen nativ auf dem Pi 4 und Pi 5 ohne Emulation. Dir steht das volle Toolset zur Verfügung: Aircrack-ng, Kismet, Wireshark, Bettercap und der Rest der Standard-Kali-Metapakete.

Das größte Hindernis ist oft der Treiber. Der RTL8812AU-Chipsatz im AWUS036ACH befindet sich nicht im Mainline-Kernel. Das bedeutet, du kannst den Adapter nicht einfach einstecken und erwarten, dass er funktioniert. Du musst den Treiber für deinen laufenden ARM64-Kernel selbst kompilieren – und die Kompilierungs-Flags unterscheiden sich von denen für x86-64. Diese Anleitung führt dich durch jeden einzelnen Schritt.

---

## Empfohlene Hardware

Nicht jede Kombination aus Pi-Modell, Adapter und Netzteil funktioniert zuverlässig. Die folgende Tabelle zeigt, was gut funktioniert und welche Kompromisse zu erwarten sind.

| Komponente | Empfohlen | Hinweise |
|---|---|---|
| Einplatinencomputer | Raspberry Pi 5 (4 GB oder 8 GB) | Pi 4 (4 GB+) funktioniert gut; Pi 3B+ ist zu langsam für Echtzeit-Captures |
| Hauptadapter | ALFA AWUS036ACH | RTL8812AU Chipsatz; beste ARM-Treiberunterstützung; Dual-Band AC1200 |
| Alternativer Adapter | ALFA AWUS036ACM | MT7612U Chipsatz; Treiber im Kernel (mt76x2u); Plug-and-Play unter Kali ARM64 |
| WLAN 6 Adapter | ALFA AWUS036AXM oder AXML | MT7921AUN Chipsatz; nativ im Kernel seit 5.18; benötigt firmware-misc-nonfree |
| USB-Hub | Aktiver USB 3.0 Hub | AWUS036ACH verbraucht ~500 mW; kann Pi USB-Ports ohne Hub überlasten |
| Speicher | MicroSD 32 GB+ (Class 10 / A2) | A2-zertifizierte Karten bieten spürbar schnelleres Booten und apt-Vorgänge |
| Netzteil | Offizielles Pi USB-C Netzteil (≥ 3 A) | Netzteile von Drittanbietern sind eine häufige Ursache für Stabilitätsprobleme |

{{< alert "triangle-exclamation" >}}
Der AWUS036ACH ist ein USB-Gerät mit hohem Stromverbrauch. Wenn du ihn ohne einen aktiven USB-Hub direkt an einen Raspberry Pi 4 oder Pi 5 anschließt, kann dies dazu führen, dass der Pi unter Last drosselt oder neu startet. Verwende immer einen aktiven Hub, wenn du den AWUS036ACH zusammen mit anderen USB-Peripheriegeräten betreibst.
{{< /alert >}}

---

## Kali Linux ARM64 auf dem Raspberry Pi installieren

### Das ARM-Image herunterladen

Kali Linux stellt eigene ARM64-Images für den Raspberry Pi unter [https://www.kali.org/get-kali/#kali-arm](https://www.kali.org/get-kali/#kali-arm) bereit. Lade das Image mit der Bezeichnung **Raspberry Pi 4 (64-bit)** oder **Raspberry Pi 5 (64-bit)** herunter. Verwende nicht das 32-bit Image – der ARM64-Kernel ist für die in dieser Anleitung beschriebenen Treiber-Build-Schritte erforderlich.

### Auf MicroSD-Karte flashen

Du kannst das Image entweder mit dem grafischen Tool "Raspberry Pi Imager" oder über die Befehlszeile mit `dd` flashen:

```bash
# Ersetze /dev/sdX durch dein tatsächliches SD-Karten-Gerät (prüfen mit lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Wähle im Raspberry Pi Imager **Eigenes Image** → wähle die Kali `.img.xz` Datei → wähle deine SD-Karte → Schreiben.

### Erster Start und Ersteinrichtung

Lege die SD-Karte ein, schließe einen Monitor und eine Tastatur an (oder richte den Headless-Zugriff über eine serielle Konsole ein) und schalte den Pi ein. Die Standard-Zugangsdaten sind:

- **Benutzername:** `kali`
- **Passwort:** `kali`

Nach dem Einloggen führst du `kali-tweaks` aus und folgst den Anweisungen, um die Standardkonfiguration abzusichern. Aktualisiere dann das System vollständig, bevor du dich an die Treiber wagst:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

{{< alert "circle-info" >}}
Wenn du planst, über SSH statt mit Tastatur und Monitor auf den Pi zuzugreifen, aktiviere SSH vor dem ersten Booten, indem du eine leere Datei namens `ssh` in der `/boot`-Partition der SD-Karte erstellst. Dies ist derselbe Mechanismus wie beim Standard Raspberry Pi OS.
{{< /alert >}}

---

## RTL8812AU-Treiber unter Kali ARM64 installieren (AWUS036ACH)

Der RTL8812AU-Treiber ist nicht im offiziellen Linux-Kernel enthalten. Unter ARM64 musst du ihn entweder aus dem Quellcode kompilieren oder die von Kali paketierte DKMS-Version installieren. Beide Wege werden hier beschrieben – beginne mit dem Paket-Ansatz und greife nur auf den manuellen Build zurück, wenn es zu Problemen mit der Kernel-Version kommt.

### Option 1: Kali-Paket (Empfohlener Startpunkt)

Kali Linux bietet eine DKMS-paketierte Version des RTL8812AU-Treibers an, die die Neukompilierung bei jedem Kernel-Update automatisch übernimmt.

```bash
sudo apt install realtek-rtl88xxau-dkms
```

Nach der Installation startest du neu und prüfst, ob das Modul geladen wurde:

```bash
sudo modprobe 88XXau
ip link show
```

Wenn du ein `wlan1`-Interface siehst (vorausgesetzt `wlan0` ist der integrierte Adapter des Pi), funktioniert der Treiber. Dieses Paket hinkt der GitHub-Quelle manchmal ein paar Wochen hinterher, ist aber der einfachste Weg für den Einstieg.

{{< alert "circle-info" >}}
Das Kali-Paket reicht normalerweise für die meisten ARM64-Setups aus. Fahre nur mit dem manuellen Build fort, wenn das DKMS-Paket nicht gegen deine aktuelle Kernel-Version kompiliert werden kann (prüfen mit `uname -r`).
{{< /alert >}}

### Option 2: Manueller Build aus dem Quellcode (ARM64)

Falls das DKMS-Paket fehlschlägt – meist weil dein Kernel neuer ist als die letzte getestete Version des Pakets – baue den Treiber direkt aus dem Aircrack-ng-Fork auf GitHub. Dies ist die maßgebliche Quelle für die ARM64-Unterstützung.

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)

git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# Plattform-Flags von x86 auf ARM64 umstellen
sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/' Makefile
sed -i 's/CONFIG_PLATFORM_ARM64_RPI = n/CONFIG_PLATFORM_ARM64_RPI = y/' Makefile

sudo make dkms_install
```

Die `sed`-Befehle sind der entscheidende Unterschied zu einem x86-64 Build. Ohne sie nutzt das Makefile x86-Pfade, und das resultierende Modul wird unter ARM64 nicht geladen.

Nach einem erfolgreichen Build lädst du das Modul und prüfst es:

```bash
sudo modprobe 88XXau
ip link show
```

Du solltest ein neues Interface sehen – normalerweise `wlan1`. Wenn `ip link show` das Interface anzeigt, funktioniert der Treiber korrekt.

---

## MT7921AUN am Raspberry Pi (AWUS036AXM / AXML)

Der MediaTek MT7921AUN Chipsatz, der in den AWUS036AXM und AXML Adaptern verwendet wird, ist seit Kernel-Version 5.18 im offiziellen Kernel enthalten. Kali Linux ARM64-Images nutzen einen Kernel, der weit über dieser Schwelle liegt. Das bedeutet, der Treiber wird automatisch geladen, wenn du den Adapter einsteckst – kein Kompilieren nötig.

Der einzige zusätzliche Schritt ist die Installation der Closed-Source-Firmware, die der MT7921AUN benötigt:

```bash
sudo apt install firmware-misc-nonfree
sudo reboot
```

Prüfe nach dem Neustart, ob der Adapter erkannt wird und das Interface bereit ist:

```bash
lsusb
sudo modprobe mt7921u
ip link show
```

Wenn `lsusb` ein MediaTek-Gerät anzeigt und `ip link show` ein neues WLAN-Interface auflistet, ist der Adapter bereit. Die Unterstützung für den Monitor Mode beim MT7921AUN hat sich seit Kernel 5.18 deutlich verbessert, kann aber bei bestimmten Packet-Injection-Tests weniger zuverlässig sein als RTL8812AU-basierte Adapter. Für maximale Kompatibilität mit älteren Pentesting-Workflows bleibt der AWUS036ACH die bessere Wahl.

---

## Monitor Mode am Raspberry Pi aktivieren

Der Raspberry Pi hat ein integriertes WLAN-Interface (`wlan0`). Behalte dieses für den Netzwerkzugriff (z. B. SSH) bei. Nutze den ALFA-Adapter (`wlan1`) ausschließlich für den Monitor Mode und Packet Capture. Versetze niemals `wlan0` in den Monitor Mode, wenn du den Pi ohne Monitor ("headless") betreibst – du würdest sofort deine SSH-Verbindung verlieren.

```bash
# Prozesse beenden, die mit dem Monitor Mode in Konflikt stehen (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# Monitor Mode auf der ALFA-Adapter-Schnittstelle aktivieren
sudo airmon-ng start wlan1

# Überprüfen, ob der Monitor Mode aktiv ist
sudo iwconfig wlan1mon

# Erfassung auf allen Kanälen starten
sudo airodump-ng wlan1mon
```

{{< alert "circle-info" >}}
`airmon-ng start wlan1` erstellt ein neues Interface namens `wlan1mon`. Führe alle weiteren Tools immer gegen `wlan1mon` aus, nicht gegen `wlan1`. Den Namen des Interfaces kannst du mit `iwconfig` oder `ip link show` bestätigen.
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
Das Ausführen von `airmon-ng check kill` stoppt den NetworkManager und wpa_supplicant. Wenn du über `wlan0` per SSH verbunden bist, wird dadurch auch deine SSH-Sitzung beendet. Verbinde dich bei Headless-Setups über Ethernet oder eine zweite kabelgebundene Schnittstelle, bevor du diese Befehle ausführst, oder nutze `tmux`, damit deine Sitzung einen Verbindungsabbruch übersteht.
{{< /alert >}}

Um den Monitor Mode zu deaktivieren und in den Managed Mode zurückzukehren:

```bash
sudo airmon-ng stop wlan1mon
sudo systemctl start NetworkManager
```

---

## Tipps für portable Pentest-Setups

Die Hardware zum Laufen zu bringen, ist nur die halbe Miete. Diese praktischen Tipps machen den Unterschied zwischen einem stabilen Feld-Kit und einem frustrierenden Kabelsalat.

**Netzwerkarchitektur:** Nutze `wlan0` (das integrierte WLAN des Pi), um deine Management-Verbindung aufrechtzuerhalten – verbinde dich per SSH von einem Laptop im selben LAN oder Hotspot. Widme `wlan1` (den ALFA-Adapter) vollständig deinen Pentesting-Aktivitäten. Vermische diese beiden Rollen niemals.

**Headless-Betrieb:** Vermeide es, im Feld Tastatur, Maus und Monitor anzuschließen. Konfiguriere SSH beim ersten Booten und greife auf alles über einen Terminal-Emulator auf deinem Laptop zu. `tmux`-Sitzungen bleiben auch bei Verbindungsabbrüchen bestehen, was bei instabilen Netzwerkbedingungen unbezahlbar ist.

**Stromversorgung:** Verwende das offizielle Raspberry Pi USB-C Netzteil mit mindestens 3 A. Für den AWUS036ACH solltest du einen aktiven USB-Hub mit 2,5 A oder mehr hinzufügen. Eine hochwertige USB-C Powerbank (65 W+) kann den Pi, den Hub und den Adapter gleichzeitig für 4–6 Stunden mit Strom versorgen, je nach Auslastung.

**Speicher:** Schreibe Kismet-Logs und Capture-Dateien auf eine USB-SSD statt auf die MicroSD-Karte. MicroSD-Karten haben begrenzte Schreibzyklen und verschleißen schnell bei dauerhaften Logging-Vorgängen. Eine am aktiven Hub angeschlossene USB 3.0 SSD ist schneller und langlebiger.

**Gehäuse:** Wähle ein Pi-Gehäuse mit offenen USB-Ports oder Aussparungen, die den aktiven Hub aufnehmen können. Aluminiumgehäuse mit passiven Kühlrippen helfen dabei, die Hitze bei dauerhaften Captures zu bewältigen.

---

## Kismet auf dem Raspberry Pi ausführen

Kismet ist ein passiver WLAN-Scanner, der als Hintergrundserver läuft und eine browserbasierte Weboberfläche bietet. Er eignet sich hervorragend für Headless-Pi-Einsätze: Du lässt den Pi laufen und prüfst das Web-Interface von jedem Gerät im selben Netzwerk.

```bash
sudo apt install kismet

# Kismet mit dem ALFA-Adapter im Monitor Mode starten
kismet -c wlan1
```

{{< alert "circle-info" >}}
Kismet versetzt das Interface selbst in den Monitor Mode, wenn du den Namen des Interfaces direkt übergibst. Du musst `airmon-ng start` nicht ausführen, bevor du Kismet startest. Kismet verwaltet den Lebenszyklus des Interfaces intern.
{{< /alert >}}

Sobald Kismet läuft, kannst du auf das Web-Interface von jedem Browser in deinem Netzwerk zugreifen:

```
http://raspberrypi.local:2501
```

Beim ersten Start fordert Kismet dich auf, einen Admin-Benutzernamen und ein Passwort zu erstellen. Nach dem Einloggen kannst du erkannte Netzwerke, verbundene Clients, die Signalstärkenhistorie und GPS-Daten (falls ein GPS-Dongle angeschlossen ist) anzeigen.

Kismet speichert standardmäßig alles in `.kismet`-Datenbankdateien unter `~/.kismet/`. Diese können später zur Analyse exportiert oder zu WiGLE hochgeladen werden.

---

## Anwendungsfall: Wardriving-Setup

Ein Raspberry Pi, auf dem Kismet mit einem ALFA-Adapter und einem GPS-Dongle läuft, ist ein komplettes, eigenständiges Wardriving-Kit – kleiner und günstiger als jedes dedizierte Wardriving-Gerät.

**Benötigte Komponenten:**
- Raspberry Pi 4 oder Pi 5
- ALFA AWUS036ACH
- USB GPS-Dongle (u-blox Chipsätze funktionieren gut mit Kismet)
- Aktiver USB-Hub
- USB-C Powerbank (65 W+, mit Pass-Through-Ladefunktion)

**Einrichtungsschritte:**

1. Kismet und die GPS-Pakete installieren:

```bash
sudo apt install kismet gpsd gpsd-clients
```

2. `gpsd` so konfigurieren, dass es von deinem GPS-Dongle liest:

```bash
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
```

3. Kismet mit GPS-Unterstützung starten:

```bash
kismet -c wlan1 --gps=gpsd:host=localhost,port=2947
```

4. Montiere den Pi, den Hub, den Adapter und die Powerbank in einer Tasche oder einem Gehäuse und platziere es in deinem Fahrzeug. Greife über den Hotspot deines Handys oder ein Tablet, das mit demselben WLAN wie der Pi verbunden ist, auf die Kismet-Weboberfläche zu.

Kismet protokolliert die GPS-Koordinaten für jedes erkannte Netzwerk. Exportiere die `.kismet`-Datenbank mit `kismetdb_to_wigle` (im Lieferumfang von Kismet enthalten) in das WiGLE-CSV-Format und lade sie zur Kartierung auf WiGLE hoch.

{{< alert "triangle-exclamation" >}}
Beachte immer die lokalen Gesetze, bevor du Netzwerk-Scanning-Aktivitäten durchführst. In vielen Ländern ist Wardriving mit rein passiven Scans legal; aktives Probing oder das unbefugte Verbinden mit Netzwerken ist es nicht. Kenne deine lokalen Vorschriften.
{{< /alert >}}

---

## Weiterführende Informationen

Die vollständige Anleitung zur Installation des RTL8812AU-Treibers unter Kali Linux (Desktop) und Ubuntu findest du in unserem Guide [ALFA-Treiber unter Kali Linux & Ubuntu installieren](/de/blog/install-alfa-driver-kali-ubuntu/). Wenn du dich noch nicht für einen Adapter entschieden hast, deckt der [ALFA WLAN-Adapter Kaufratgeber 2026](/de/blog/alfa-wifi-adapter-buyer-guide-2026/) jedes aktuelle Modell mit Chipsatz-Details und Anwendungsempfehlungen ab.
