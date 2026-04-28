---
title: "ALFA WLAN-Adapter mit Kali NetHunter über USB OTG nutzen"
description: "So verwenden Sie ALFA USB WLAN-Adapter mit Kali NetHunter auf Android über USB OTG. Enthält Informationen zu AWUS036ACH-Treibern, Monitor-Mode-Befehlen, OTG-Kabel-Anforderungen und unterstützten Geräten."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["nethunter", "android", "usb-otg", "kali-linux", "AWUS036ACH", "RTL8812AU", "mobile-pentest"]
---

Dein Android-Handy ist bereits ein leistungsstarker Computer in deiner Tasche. Mit installiertem Kali NetHunter auf einem gerooteten Gerät und einem ALFA WLAN-Adapter, der über USB OTG angeschlossen ist, wird es zu einer wirklich fähigen Pentesting-Plattform im Taschenformat. Kein Laptop erforderlich. Keine sperrige Hardware. Nur dein Handy, ein kurzes OTG-Kabel und ein Adapter, der Monitor Mode und Packet Injection unterstützt.

Diese Anleitung deckt alles ab, was du brauchst, um einen ALFA AWUS036ACH (oder einen kompatiblen Adapter) unter NetHunter zum Laufen zu bringen – von der Hardware-Auswahl über das Laden der Treiber bis hin zur Aktivierung des Monitor Mode und den in der NetHunter-App integrierten Wireless-Tools.

---

## Was ist Kali NetHunter?

Kali NetHunter ist die offizielle mobile Penetrationstest-Plattform von Kali Linux. Anstatt Android zu ersetzen, installiert NetHunter eine Kali Linux chroot-Umgebung oberhalb deiner bestehenden Android-Installation. Dein Handy funktioniert weiterhin als normales Android-Gerät, während es gleichzeitig ein vollständiges Kali Linux Userland mit all seinen Tools ausführt.

**Wichtige Merkmale:**

- Läuft ohne Android zu löschen – deine Apps, Kontakte und Daten bleiben erhalten
- Enthält die NetHunter-App, einen dedizierten Launcher für Angriffsmodule und Hardware-Steuerung
- Bietet ein vollständiges Terminal mit Zugriff auf das Kali-Toolset (Metasploit, Aircrack-ng, Nmap und hunderte weitere)
- Erfordert ein gerootetes Android-Gerät für die volle Funktionalität

**Drei Editionen:**

| Edition | Root erforderlich | Kernel-Mods | Anwendungsfall |
|---|---|---|---|
| NetHunter (Full) | Ja | Ja (Custom-Kernel) | Volle Angriffsfläche, Hardware-Schnittstellen-Unterstützung |
| NetHunter Lite | Ja | Nein | Nur Root-Tools, kein Custom-Kernel erforderlich |
| NetHunter Rootless | Nein | Nein | Begrenzte Tools, keine Hardware-Angriffe |

Für die Unterstützung von USB OTG-Adaptern mit Monitor Mode benötigst du die **Full NetHunter Edition** mit einem Custom-Kernel, der das RTL8812AU-Modul enthält.

**Offiziell unterstützte Geräte** umfassen Modelle von OnePlus, Google Pixel und ausgewählte Samsung Galaxy-Geräte. Die vollständige und aktuelle Liste findest du auf der [offiziellen NetHunter-Geräteseite](https://www.kali.org/docs/nethunter/).

**USB OTG ist eine zwingende Voraussetzung.** Bevor du Hardware kaufst, stelle sicher, dass dein spezifisches Gerätemodell USB OTG unterstützt. Die meisten modernen Geräte tun dies, aber einige Budget-Modelle und ältere Hardware unterstützen dies möglicherweise nicht.

---

## Hardware-Anforderungen

Das richtige Setup bedeutet, auf jeder Ebene kompatible Hardware zu wählen. Eine Inkompatibilität irgendwo in der Kette – Gerät, Kabel oder Adapter – führt dazu, dass der Adapter nie in `lsusb` erscheint, es zu Verbindungsabbrüchen kommt oder die Treiber versagen.

| Artikel | Anforderung | Hinweise |
|---|---|---|
| Android-Gerät | Gerootet, NetHunter-unterstützt, USB OTG fähig | OTG-Unterstützung vor dem Kauf prüfen; Full NetHunter mit Custom-Kernel erforderlich |
| USB OTG Kabel / Adapter | USB-C OTG oder Micro-USB OTG je nach Geräteanschluss | Qualität ist wichtig – billige Kabel verursachen Verbindungsabbrüche |
| ALFA WLAN-Adapter | AWUS036ACH oder AWUS036ACM empfohlen | AWUS036ACH (RTL8812AU) hat die beste Unterstützung im NetHunter-Kernel; AWUS036ACM (MT7612U) ebenfalls kompatibel |
| Aktiver USB OTG Hub | Dringend empfohlen | Verhindert, dass der Adapter den Akku leert und sorgt für USB-Stabilität |

{{< alert "triangle-exclamation" >}}
Der AWUS036ACH verbraucht etwa **500mW** über den USB-Port. Wenn du ihn direkt über den Handy-Akku ohne dedizierte Stromquelle betreibst, wird dein Akku deutlich schneller leer und der Adapter könnte bei Last zurückgesetzt werden oder die Verbindung trennen. Ein aktiver OTG-Hub – einer, der Strom von einem Netzteil bezieht und die Daten zum Handy weiterleitet – beseitigt dieses Problem vollständig.
{{< /alert >}}

**Hinweise zur Wahl eines aktiven OTG-Hubs:**

Suche nach einem Hub, der explizit als USB OTG mit "Power Delivery Passthrough" beworben wird. Das bedeutet, dass der Hub 5V von einem USB-Ladegerät bezieht, die angeschlossenen Geräte über das Ladegerät versorgt (statt über das Handy) und dennoch die Daten zwischen dem Handy und den angeschlossenen Geräten überträgt. Nicht alle USB-Hubs unterstützen dies – prüfe die Produktspezifikationen vor dem Kauf sorgfältig.

---

## Unterstützte ALFA-Adapter für NetHunter

Der Custom-Kernel von NetHunter enthält vorkompilierte Kernelmodule für einen bestimmten Satz von Chipsätzen. Die RTL8812AU-Chipsatzfamilie hat die stärkste Unterstützung, da sie früh integriert wurde und aktiv gepflegt wird.

| Adapter | Chipsatz | NetHunter-Unterstützung | Hinweise |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | ✅ Beste Unterstützung | NetHunter-Kernel enthält das `88XXau`-Modul; Monitor Mode und Packet Injection voll unterstützt |
| AWUS036ACM | MT7612U | ✅ Gute Unterstützung | Alternativer Chipsatz; funktioniert im Allgemeinen; prüfe dies für deinen spezifischen Geräte-Kernel |
| AWUS036ACS | RTL8811AU | ✅ Funktioniert | Gleiche Treiberfamilie wie RTL8812AU; geringerer Stromverbrauch (~300mW); Single-Band 2.4/5 GHz |
| AWUS036AXM | MT7921AUN | ⚠️ Begrenzt | WLAN 6E-Adapter; Verfügbarkeit der Kernelmodule hängt vom Gerät und der Kernel-Version ab |
| AWUS036AXML | MT7921AUN | ⚠️ Begrenzt | Gleicher Chipsatz wie AXM; nicht universell in NetHunter-Kerneln unterstützt |

**Empfehlung:** Für einen zuverlässigen Betrieb unter NetHunter solltest du bei RTL8812AU-basierten Adaptern bleiben. Der `88XXau`-Treiber ist in den meisten NetHunter-Custom-Kerneln enthalten, es gibt eine umfangreiche Community-Dokumentation dazu und die Fehlerbehebung ist gut verstanden. Die WLAN 6E-Adapter sind technisch beeindruckend, aber das Kompatibilitätsrisiko für ein mobiles Pentest-Setup, bei dem Zuverlässigkeit wichtiger ist als roher Durchsatz, nicht wert.

Wenn du Dual-Band AC1200-Fähigkeit mit breiter NetHunter-Kompatibilität möchtest, ist der **AWUS036ACH** die richtige Wahl.

---

## Einrichtungsschritte

Die folgenden Schritte setzen voraus, dass du ein gerootetes Android-Gerät mit installiertem Full NetHunter sowie ein USB OTG-Kabel oder einen aktiven Hub bereit hast.

### Schritt 1: NetHunter-App öffnen

Starte die NetHunter-App auf deinem Android-Gerät. Navigiere zu **Kali Services**, um sicherzustellen, dass die chroot-Umgebung läuft. Wenn sie nicht läuft, tippe auf **Start**, um sie zu aktivieren. Die chroot-Umgebung muss aktiv sein, damit der Kernel USB-Geräte für Kali-Tools bereitstellen kann.

### Schritt 2: ALFA-Adapter über OTG verbinden

Stecke dein USB OTG-Kabel oder deinen Hub in den USB-Anschluss des Handys und verbinde dann den ALFA-Adapter mit dem OTG-Kabel oder Hub. Wenn du einen aktiven Hub verwendest, schließe zuerst das Netzteil des Hubs an eine Steckdose an.

### Schritt 3: USB-Berechtigung erteilen

Android zeigt einen Berechtigungsdialog an und fragt, ob die NetHunter-App auf das USB-Gerät zugreifen darf. Tippe auf **OK** und setze ein Häkchen bei **Immer erlauben**, wenn du diesen Dialog in Zukunft überspringen möchtest. Wenn du diesen Dialog schließt, ohne die Berechtigung zu erteilen, kann die Kali chroot-Umgebung nicht auf den Adapter zugreifen.

### Schritt 4: Adapter mit `lsusb` überprüfen

Öffne das NetHunter-Terminal und führe folgenden Befehl aus:

```bash
lsusb
```

Du solltest einen Eintrag sehen, der **Realtek Semiconductor** zusammen mit der Geräte-ID enthält. Für den AWUS036ACH sieht das in etwa so aus:

```
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

Wenn das Realtek-Gerät nicht erscheint, liegt das Problem an der Hardware – überprüfe das OTG-Kabel, versuche ein anderes Kabel oder stelle sicher, dass OTG in den Entwickleroptionen deines Geräts aktiviert ist.

### Schritt 5: Treiber laden

```bash
sudo modprobe 88XXau
```

Auf den meisten NetHunter-Builds wird der Treiber automatisch geladen, wenn der Adapter erkannt wird. Wenn die Schnittstelle nach dem Anschließen des Adapters nicht erscheint, führe diesen Befehl manuell aus. Das `88XXau`-Modul ist der von Aircrack-ng gepflegte RTL8812AU-Treiber, der in den Custom-Kernel von NetHunter integriert ist.

### Schritt 6: Schnittstelle überprüfen

```bash
ip link show | grep wlan
```

Du solltest `wlan1` sehen (oder `wlan2`, wenn dein Gerät ein integriertes WLAN-Interface auf `wlan0` hat). Vergewissere dich, dass die Schnittstelle aufgelistet ist, bevor du versuchst, den Monitor Mode zu aktivieren.

### Schritt 7: Monitor Mode aktivieren

```bash
sudo airmon-ng start wlan1
```

Wenn `airmon-ng` Prozesse meldet, die den Monitor Mode stören könnten, beende diese zuerst (siehe den Befehlsabschnitt unten) und führe den Befehl dann erneut aus. Die Schnittstelle wird nach der Aktivierung des Monitor Mode in `wlan1mon` umbenannt.

---

## Monitor Mode-Befehle auf NetHunter

Die folgende Befehlssequenz deckt den gesamten Workflow ab – von der Überprüfung des Adapters bis hin zur aktiven Erfassung:

```bash
# Prüfen, ob der Adapter vom System erkannt wird
lsusb | grep -i realtek

# Treiber laden, falls er nach dem Anschließen nicht automatisch geladen wurde
sudo modprobe 88XXau

# Prozesse beenden, die den Monitor Mode stören (NetworkManager, wpa_supplicant, etc.)
sudo airmon-ng check kill

# Monitor Mode auf der ALFA-Adapter-Schnittstelle starten
sudo airmon-ng start wlan1

# Alle sichtbaren Netzwerke scannen (Strg+C zum Stoppen)
sudo airodump-ng wlan1mon

# Datenverkehr eines bestimmten Netzwerks erfassen
# -c: Kanal, --bssid: MAC-Adresse des Ziel-APs, -w: Präfix der Ausgabedatei
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan1mon
```

**Um den Monitor Mode zu beenden und in den Managed Mode zurückzukehren:**

```bash
sudo airmon-ng stop wlan1mon
```

**Um die Adapter-Fähigkeiten zu prüfen und zu bestätigen, dass der Monitor Mode aktiv ist:**

```bash
iwconfig wlan1mon
```

Die Ausgabe sollte `Mode:Monitor` zeigen, wenn alles korrekt funktioniert.

---

## NetHunter WLAN-Angriffe (Nur für autorisierte Tests)

Die NetHunter-App enthält integrierte grafische Oberflächen für mehrere WLAN-fokussierte Angriffsmodule. Diese sind ohne die Eingabe von Terminalbefehlen zugänglich, was sie nützlich für Demonstrationen oder Einsätze im Feld macht.

{{< alert "triangle-exclamation" >}}
Alle WLAN-Sicherheitstests dürfen **nur an Netzwerken und Geräten durchgeführt werden, die dir gehören oder für die du eine ausdrückliche schriftliche Genehmigung hast**. Der unbefugte Zugriff auf Computernetzwerke ist in den meisten Ländern illegal. Die hier beschriebenen Tools dienen ausschließlich autorisierten Penetrationstests, der Sicherheitsforschung und Bildungszwecken. Yupitek übernimmt keine Haftung für Missbrauch.
{{< /alert >}}

**WiFi Evil Portal (WPS3):** Direkt im Hauptmenü der NetHunter-App verfügbar. Erstellt einen gefälschten Access Point mit einem Captive Portal zum Abfangen von Zugangsdaten bei autorisierten Social-Engineering-Assessments. Erfordert einen externen Adapter mit Unterstützung für den AP-Modus.

**MANA Rogue AP Toolkit:** Zu finden unter **NetHunter-App > Wireless Attacks > MANA Toolkit**. MANA erweitert das Standard-Konzept eines Rogue-APs um KARMA-Angriffe und SSL-Stripping-Fähigkeiten. Für die volle Funktionalität ist ein kompatibler externer WLAN-Adapter erforderlich – der interne Android-WLAN-Chip reicht für die meisten MANA-Konfigurationen nicht aus.

Beide Module kommunizieren direkt mit deinem ALFA-Adapter, weshalb die Unterstützung externer Adapter für die praktische Nutzung dieser integrierten Tools unerlässlich ist.

---

## Akku- und Energiemanagement

Der Betrieb eines AWUS036ACH an einem Handy stellt hohe Anforderungen an den Akku und das USB-Stromversorgungssystem. Hier ist, was dich erwartet und wie du es optimieren kannst:

**Stromverbrauch:** Der AWUS036ACH verbraucht während der aktiven Nutzung kontinuierlich etwa 500mW. Bei einem typischen 3.500 mAh Android-Akku verdoppelt dies in etwa die Entladerate im Vergleich zur normalen Handynutzung.

**Nutzung eines aktiven OTG-Hubs:** Dies ist die effektivste Lösung. Der Hub bezieht Strom von einem Netzteil und versorgt den ALFA-Adapter. Der USB-Port des Handys überträgt nur Daten, aber keinen Strom an den Adapter. Der Akkuverbrauch normalisiert sich nahezu.

**Betrieb während des Ladens:** Wenn kein aktiver Hub verfügbar ist, kannst du den Akkuverbrauch mildern, indem du das Handy gleichzeitig über einen USB-C Hub mit Power Delivery (PD) Passthrough auflädst. Dies erfordert einen Hub, der sowohl Daten-Passthrough (für die OTG-Funktion) als auch gleichzeitiges Laden unterstützt – solche Hubs sind verfügbar, erfordern aber eine sorgfältige Auswahl.

**Display-Management:** Der Bildschirm ist der andere große Stromverbraucher im Feldeinsatz. Stelle das Display-Timeout auf 30 Sekunden (**Einstellungen > Display > Ruhezustand**) und reduziere die Helligkeit auf das Minimum. In Kombination mit einem aktiven Hub ermöglicht dies eine mehrstündige Betriebsdauer.

**Thermische Überlegungen:** Ein längerer Betrieb des Adapters in einer Handyhülle kann zu Hitzestau führen. Wenn der Thermoschutz des Handys den USB-Controller drosselt, kann es zu Verbindungsabbrüchen kommen. Entferne die Handyhülle bei längeren Capture-Sessions.

---

## Fehlerbehebung

**Adapter wird nicht erkannt (`lsusb` zeigt nichts an):**
1. Überprüfe, ob USB OTG aktiviert ist – siehe **Einstellungen > Entwickleroptionen > OTG** (der Ort variiert je nach Android-Version und Hersteller)
2. Versuche ein anderes OTG-Kabel – die Kabelqualität ist eine häufige Fehlerquelle
3. Teste den Adapter an einem anderen USB-Gerät, um sicherzustellen, dass der Adapter selbst funktioniert
4. Stelle sicher, dass dein Gerät USB OTG unterstützt, indem du die Herstellerangaben prüfst

**Treiber wird nicht geladen (kein `wlan1`-Interface nach `modprobe`):**
1. Prüfe `dmesg` im NetHunter-Terminal auf USB- und Treiberfehlermeldungen: `dmesg | tail -30`
2. Stelle sicher, dass die NetHunter chroot-Umgebung läuft und du die Befehle darin ausführst
3. Vergewissere dich, dass dein NetHunter-Build das `88XXau`-Modul enthält: `find /lib/modules -name "*88XX*"`

**`wlan1`-Interface verschwindet während der Nutzung:**
Dies ist fast immer ein USB-Stromproblem. Der Adapter zieht mehr Strom, als der USB-Port des Handys liefern kann. Verwende einen aktiven OTG-Hub. Als vorübergehende Maßnahme kannst du die Sendeleistung mit `sudo iw dev wlan1 set txpower fixed 1000` (setzt sie auf 10 dBm) reduzieren.

**Fehler "Permission denied" (Zugriff verweigert):**
Stelle sicher, dass du die Befehle als Root in der NetHunter chroot-Umgebung ausführst. Führe zuerst `sudo su` aus und dann die Befehle. Alternativ kannst du jedem Befehl ein `sudo` voranstellen.

**Monitor Mode startet, aber in `airodump-ng` erscheinen keine Netzwerke:**
1. Überprüfe, ob der Kanal richtig eingestellt ist – versuche `sudo airodump-ng --band abg wlan1mon`, um alle Bänder zu scannen
2. Stelle sicher, dass `airmon-ng check kill` ausgeführt wurde, bevor der Monitor Mode gestartet wurde
3. Überprüfe, ob die Antenne richtig mit dem Adapter verbunden ist

---

## Verwandte Anleitungen

Für andere Plattformen und Anwendungsfälle mit ALFA-Adaptern:

- [AWUS036ACH Einrichtungsanleitung unter Kali Linux (Desktop/Laptop)](/de/blog/awus036ach-kali-linux-setup/)
- [ALFA-Adapter mit Raspberry Pi und Kali nutzen](/de/blog/alfa-adapter-raspberry-pi-kali/)
