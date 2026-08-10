---
title: "ALFA AWUS036AXML Installationsanleitung: Praxis-Test von Monitor-Mode und Packet Injection für Wi-Fi 6E-Netzwerkkarten unter Kali Linux"
locale: de
hreflang_group: awus036axml-wifi6e-kali-linux-setup
slug: awus036axml-wifi6e-kali-linux-setup
published: 2026-08-10
author: Yupitek
category: technical
tags:
  - AWUS036AXML
  - Kali Linux
hero_image: /static/img/AWUS036AXML/hero.webp
hero_alt: "So installieren Sie AWUS036AXML unter Kali Linux? Wi-Fi 6E Monitor-Mode und Packet Injection Tutorial | Yupitek"
seo_description: "Installationsanleitung für ALFA AWUS036AXML (MT7921AUN Chipset) unter Kali Linux: Eingebauter mt7921u-Treiber, Kernel-Anforderungen, Monitor-Mode, Packet Injection Tests und häufige Fehlerbehebung."
---

# ALFA AWUS036AXML Installationsanleitung: Praxis-Test von Monitor-Mode und Packet Injection für Wi-Fi 6E-Netzwerkkarten unter Kali Linux

> TL;DR: Der ALFA AWUS036AXML ist mit dem MediaTek MT7921AUN-Chipset ausgestattet und funktioniert unter Kali Linux (Kernel 5.18+) **mit dem eingebauten `mt7921u`-Treiber**, ohne dass ein separater Treiber kompiliert werden muss. Für einen stabilen aktiven Monitor-Mode (Active Monitor Mode) und Packet Injection wird ein Kernel 6.12+ sowie ein USB-Hub mit externer Stromversorgung empfohlen. Nach dem Einstecken sollte `lsusb` die ID `0e8d:7961` anzeigen. Anschließend können Sie den Monitor-Mode mit `airmon-ng` oder `iw` aktivieren.

## Warum Wi-Fi 6E-Netzwerkkarten zunehmend für Penetrationstests interessant sind

Das neu hinzugefügte **6-GHz-Band** (5925–7125 MHz) von Wi-Fi 6E ist in den letzten Jahren zum Schwerpunkt der Upgrades von Unternehmens-WLAN geworden: Neue Generationen von Access Points (APs), hochdichte Konferenzräume und IoT-Implementierungen in Fabriken setzen zunehmend auf 6 GHz. Für Sicherheitsaudits bedeutet dies: Wenn das zu prüfende Umfeld bereits 6 GHz nutzt, **muss Ihre Test-Netzwerkkarte dieses Band empfangen können** – andernfalls entfällt ein erheblicher Teil des Audit-Umfangs.

Der AWUS036AXML ist eine Wi-Fi 6E USB-Netzwerkkarte von ALFA Network, die das 2,4-/5-/6-GHz-Dreifachband unterstützt. Im Vergleich zum Vorgängermodell AWUS036ACH (RTL8812AU, nur 2,4/5 GHz) ist der größte Unterschied die Ergänzung der 6-GHz-Monitoring-Fähigkeit. Wenn Sie mit dem Workflow des AWUS036ACH vertraut sind, werden die Schritte in diesem Artikel sehr vertraut wirken.

## AWUS036AXML Spezifikationen und Versionsanforderungen

| Merkmal | AWUS036AXML | AWUS036ACH (zum Vergleich) | AWUS036ACM (zum Vergleich) |
|---|---|---|---|
| Chipset | MediaTek MT7921AUN | Realtek RTL8812AU | MediaTek MT7612U |
| Frequenzbänder | 2,4 / 5 / 6 GHz (Wi-Fi 6E) | 2,4 / 5 GHz | 2,4 / 5 GHz |
| Linux-Treiber | `mt7921u` (**im Kernel integriert**) | `88XXau` (muss manuell kompiliert/DKMS) | `mt76` (im Kernel integriert) |
| Empfohlener Kernel | ≥ 5.18 (6-GHz-Unterstützung) | 5.x (ältere Versionen möglich) | 5.x |
| Aktiver Monitor-Mode | Empfohlen ab Kernel ≥ 6.12 | Allgemein verfügbar | Allgemein verfügbar |
| USB-ID (lsusb) | `0e8d:7961` | `0bda:8812` | `0e8d:7612` |
| Stromverbrauch | Ca. 2,7 W (empfohlen: Hub mit Stromversorgung) | Niedriger | Niedriger |
| Packet Injection | Unterstützt (empfohlener Praxis-Test) | Unterstützt | Unterstützt |

> Erläuterung zu den Versionsanforderungen: `mt7921u` ist seit Kernel 5.18 im Mainline-Kernel enthalten, die Unterstützung für das 6-GHz-Band wurde schrittweise ergänzt. **Für den aktiven Monitor-Mode (Active Monitor Mode) wird ein Kernel 6.12+ empfohlen.** Der Standardkernel von Kali 2026 ist bereits auf Version 6.14, was die Anforderungen direkt erfüllt.

## Vorbereitung

1. **Kali Linux 2024.x oder höher** (empfohlen: auf den neuesten Stand bringen: `sudo apt update && sudo apt full-upgrade -y`).
2. Prüfen Sie die Kernel-Version: `uname -r`. Wenn sie unter 5.18 liegt, führen Sie zunächst ein System-Upgrade durch.
3. Verfügbaren USB 3.0-Port nutzen. Wenn Sie einen Raspberry Pi oder einen USB-Hub verwenden, **empfehlen wir einen Hub mit externer Stromversorgung** (der AWUS036AXML verbraucht ca. 2,7 W; unzureichende Stromversorgung führt dazu, dass die Karte nicht erkannt wird).
4. Rechtliche Testberechtigung: Alle Befehle in dieser Anleitung dürfen nur in Netzwerken verwendet werden, die Ihnen gehören oder für die Sie eine ausdrückliche Genehmigung haben.

## Schritt 1: Netzwerkkarte anschließen und Systemerkennung prüfen

Stecken Sie die Netzwerkkarte ein und prüfen Sie mit `lsusb`, ob das Gerät erkannt wird:

```bash
lsusb
```

In der erwarteten Ausgabe sollte Folgendes erscheinen:

```text
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

`0e8d:7961` ist die USB-ID des MT7921AUN. Wenn Sie diese nicht sehen, prüfen Sie zunächst die Stromversorgung (wechseln Sie den USB-Port oder verwenden Sie einen Hub mit Stromversorgung) und versuchen Sie es erneut.

Prüfen Sie, ob der Treiber geladen wurde:

```bash
lsmod | grep mt7921
dmesg | grep -i mt7921 | tail -20
```

Der Standardkernel von Kali 2026 enthält `mt7921u`. Normalerweise wird er beim Einstecken automatisch geladen, **es müssen keine Treiber heruntergeladen oder kompiliert werden** – dies ist der größte Unterschied zum AWUS036ACH (RTL8812AU erfordert die manuelle Installation von `88XXau`).

## Schritt 2: Drahtlose Schnittstelle bestätigen

```bash
ip link show
# oder
iwconfig
```

Sie sollten eine neue drahtlose Schnittstelle sehen,通常是 `wlan0` oder `wlan1` (abhängig von der Anzahl der vorhandenen Schnittstellen). Das folgende Beispiel basiert auf `wlan1`. Ersetzen Sie diesen Namen durch den tatsächlichen Namen Ihrer Schnittstelle.

## Schritt 3: Monitor-Mode aktivieren

### Methode 1: airmon-ng (Empfohlen)

```bash
# Beenden Sie Dienste, die möglicherweise stören
sudo airmon-ng check kill

# Aktivieren Sie den Monitor-Mode (ersetzen Sie wlan1 durch Ihren Schnittstellennamen)
sudo airmon-ng start wlan1
```

Nach erfolgreicher Aktivierung erscheint die virtuelle Schnittstelle `wlan1mon`.

### Methode 2: iw (Präzise Steuerung)

```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

Diese Methode ändert die vorhandene Schnittstelle direkt, ohne `wlan1mon` zu erstellen.

## Schritt 4: Bestätigung, dass der Monitor-Mode aktiv ist

```bash
iwconfig
```

Das entscheidende Feld sollte `Mode:Monitor` lauten:

```text
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.412 GHz  Tx-Power=30 dBm
          Power Management:off
```

Sie können auch `iw dev` verwenden, um `type monitor` zu bestätigen. Führen Sie anschließend einen End-to-End-Test mit `airodump-ng` durch:

```bash
sudo airodump-ng wlan1mon
```

Wenn Sie eine Liste der umgebenden BSSIDs (inklusive Kanal, Signalstärke und Verschlüsselungstyp) sehen, funktioniert der Monitor-Mode korrekt. **Scannen Sie das 6-GHz-Band:**

```bash
sudo airodump-ng --band 6g wlan1mon
```

> Hinweis: Das Scannen des 6-GHz-Bands erfordert, dass Ihr Netzwerkkarten-Treiber/Kernel dieses Band unterstützt (Kernel 6.12+ ist stabiler). Wenn `--band 6g` nicht unterstützt wird, scannen Sie zunächst das 5-GHz-Band (`--band a`), um die Grundfunktionen zu bestätigen, und versuchen Sie es nach einem Kernel-Update erneut.

## Schritt 5: Packet Injection Test

```bash
sudo aireplay-ng --test wlan1mon
```

Die entscheidende Zeile in der erwarteten Ausgabe lautet:

```text
Injection is working!
```

Eine Erfolgsrate von über 80 % zeigt eine zuverlässige Funktion an. Wenn sie unter 50 % liegt, prüfen Sie die Antennenausrichtung, die USB-Stromversorgung oder verwenden Sie einen direkten USB 3.0-Port.

## Raspberry Pi Hinweis: Tragbare Wi-Fi-Audit-Plattform

Der AWUS036AXML unterstützt auch Raspberry Pi 3B+ / 4 / 5 (laut offizieller Produktseite) und eignet sich gut für den Aufbau tragbarer Audit-Tools. Wichtige Hinweise:

- **Stromversorgung**: Die USB-Stromversorgung des Pi ist begrenzt. Verwenden Sie einen USB-Hub mit externer Stromversorgung, um das gelegentliche Nicht-Erkennen zu vermeiden.
- **System**: Das offizielle Kali ARM64-Image (für Raspberry Pi) reicht aus. Nach der Installation wird ebenfalls der integrierte `mt7921u`-Treiber verwendet.
- **Verifizierung**: Wenn `lsusb` `0e8d:7961` anzeigt und `lsmod | grep mt7921` eine Ausgabe liefert, ist die Plattform einsatzbereit.

## Häufige Fehlerbehebung

**F: `lsusb` zeigt `0e8d:7961` nicht an?**
In 99 % der Fällen liegt dies an unzureichender Stromversorgung oder einer lockeren Verbindung. Wechseln Sie zu einem direkten USB 3.0-Port. Wenn Sie einen Hub verwenden, wechseln Sie zu einem Hub mit Stromversorgung. Falls dies nicht hilft, verwenden Sie ein kürzeres USB-Kabel.

**F: Nach Aktivierung des Monitor-Mode wechselt die Schnittstelle automatisch zurück zu „managed“?**
Normalerweise übernimmt NetworkManager / wpa_supplicant im Hintergrund die Kontrolle wieder. Führen Sie `sudo airmon-ng check kill` erneut aus oder stoppen Sie manuell `sudo systemctl stop NetworkManager wpa_supplicant`.

**F: `iwconfig` zeigt `Mode:Managed` an oder die Schnittstelle verschwindet?**
Der Treiber wurde möglicherweise nicht korrekt geladen oder der Kernel ist zu alt. Prüfen Sie zunächst mit `lsmod | grep mt7921`, ob das Modul geladen ist, und bestätigen Sie mit `uname -r`, dass der Kernel ≥ 5.18 ist.

**F: Es werden keine Netzwerke im 6-GHz-Band gefunden?**
Bestätigen Sie zunächst mit `iw dev wlan1mon info`, welche Bänder unterstützt werden. 6-GHz-Umgebungen sind noch selten (neue Bereitstellungen), und der Fortschritt der Lizenzfreigabe für 6 GHz in Taiwan richtet sich nach den Ankündigungen der NCC. Sie können die Funktion der Netzwerkkarte zunächst mit 2,4/5 GHz verifizieren.

**F: Im Vergleich zum AWUS036ACH, welche Karte sollte ich kaufen?**
Wenn das zu prüfende Umfeld bereits 6 GHz nutzt → Wählen Sie den AWUS036AXML. Wenn nur 2,4/5 GHz benötigt werden und das Budget im Vordergrund steht → Der AWUS036ACH ist immer noch eine sehr ausgereifte Wahl. Beide Karten sind unter Kali einsatzbereit; der Unterschied liegt im Bandumfang und der Treiberinstallation (AXML ist integriert und erfordert keine Kompilierung).

## Häufig gestellte Fragen (FAQ)

**F1: Muss ich für den AWUS036AXML unter Kali Linux einen separaten Treiber installieren?**
Nein. Er verwendet den im Kernel integrierten `mt7921u`-Treiber (Kernel 5.18+). Er ist sofort nach dem Einstecken einsatzbereit und erfordert keine Kompilierung eines DKMS-Treibers wie beim AWUS036ACH.

**F2: Unterstützt der AWUS036AXML den Monitor-Mode?**
Ja. Er kann mit `airmon-ng` oder `iw` aktiviert werden. Für den aktiven Monitor-Mode (z. B. Tests im Zusammenhang mit Deauthentication) wird ein Kernel 6.12+ empfohlen.

**F3: Kann das 6-GHz-Band von Wi-Fi 6E in Taiwan für Audits verwendet werden?**
Das 6-GHz-Band ist ein reguliertes Band. Bitte prüfen Sie vor der Nutzung den Fortschritt der Freigabe des 6-GHz-Bands durch die NCC und die Lizenzbestimmungen. Führen Sie Tests nur in Umgebungen durch, für die Sie berechtigt sind.

**F4: Was tun, wenn die Netzwerkkarte am Raspberry Pi nicht erkannt wird?**
Prüfen Sie zunächst die Stromversorgung – der AWUS036AXML verbraucht ca. 2,7 W. Verwenden Sie einen USB-Hub mit externer Stromversorgung und ein qualitativ hochwertiges USB-Kabel.

**F5: Was ist der Unterschied zwischen AWUS036AXML und AWUS036ACH?**
Der AXML ist Wi-Fi 6E (zusätzliches 6-GHz-Band) und verfügt über einen im Kernel integrierten Treiber. Der ACH ist ein Dual-Band-Gerät (2,4/5 GHz) und erfordert die manuelle Installation des Treibers für den RTL8812AU. Beide sind ausgereifte Audit-Netzwerkkarten unter Kali.

## Zusammenfassung

Der Installationsprozess für den AWUS036AXML ist einfacher als erwartet: **Kernel 5.18+ → Einstecken und sofort einsatzbereit (`mt7921u`) → Bestätigung von `0e8d:7961` → Monitor-Mode mit airmon-ng wechseln → Injection mit aireplay-ng verifizieren**. Der Kernunterschied zum AWUS036ACH liegt im 6-GHz-Band und dem treiberfreien Betrieb ohne Kompilierung – wenn Ihr Audit-Umfang bereits die Wi-Fi 6E-Generation erreicht hat, ist diese Karte die richtige Wahl, um die Bandabdeckung zu vervollständigen. Denken Sie daran, alle Tests nur in legal autorisierten Umgebungen durchzuführen.

Die ALFA Network-Serie von Netzwerkkarten wird in Taiwan von Yupitek (Yuhé Technology) verkauft und technisch unterstützt. Für den AWUS036AXML oder begleitende Stromversorgungs-Hubs und Antennen senden Sie uns gerne eine E-Mail an [sales@yupitek.com](mailto:sales@yupitek.com).