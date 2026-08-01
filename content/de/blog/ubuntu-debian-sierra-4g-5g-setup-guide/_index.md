---
title: "Vollständige Anleitung zur Installation von Sierra 4G/5G-Modulen unter Ubuntu / Debian / Linux Mint: EM7455, EM7565, EM919x, MC7455 und GNSS-Positionierung | Yupitek"
description: "Wie installierst du ein Sierra-4G/5G-Modul unter Ubuntu/Debian/Linux Mint? Diese Anleitung zeigt dir die Installation von ModemManager, den Verbindungsaufbau mit qmicli/mbimcli und das Einrichten der GNSS-Positionierung. Deckt EM7455, EM7565, EM919x und MC7455 ab."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "de"
hreflang_group: "ubuntu-debian-sierra-4g-5g-setup-guide"
slug: "ubuntu-debian-sierra-4g-5g-setup-guide"
tags: ["Sierra Wireless", "Ubuntu", "Debian", "Linux", "GNSS"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/de/products/sierra/"
faq:
  - question: "Kann Ubuntu mit einem Sierra-4G/5G-Modul direkt online gehen?"
    answer: "Ja. Installiere die Pakete modemmanager, libqmi-utils und verwandte Pakete, trage deinen APN in NetworkManager ein und du bist online."
  - question: "Wie aktiviere ich die GNSS-Positionierung eines Sierra-Moduls unter Linux?"
    answer: "Nutze die ModemManager-Befehle: Führe zuerst mmcli -m 0 --location-enable-gps-raw aus und rufe dann die Koordinaten mit --location-get ab. Stelle sicher, dass die GNSS-Antenne angeschlossen ist."
---

Du möchtest ein Sierra Wireless Modul (EM7455, EM7565, MC7455, EM919x) unter Ubuntu, Debian oder Linux Mint installieren? Linux unterstützt diese Geräte nativ. Du musst nur wissen, welche Pakete du brauchst, etwa ModemManager und libqmi-utils. Dieser Artikel behandelt Schritt für Schritt alles: vom Anschließen der Hardware und dem Installieren der Treiber über den Verbindungsaufbau bis zum Aktivieren der GNSS-Positionierung. Ob du einen Drohnen- oder Industriepc baust, folgst du einfach dieser Anleitung.

{{< tldr >}}
Du möchtest ein Sierra Wireless Modul (EM7455, EM7565, MC7455, EM919x) unter Ubuntu, Debian oder Linux Mint installieren? Linux unterstützt diese Geräte nativ. Installiere einfach die richtigen Pakete, ModemManager und libqmi-utils. Vom Anschließen der Hardware und der Treiberinstallation über den Verbindungsaufbau bis zur GNSS-Positionierung: Die Anleitung funktioniert sowohl für Drohnen als auch für Industriecomputer.
{{< /tldr >}}

**In einem Satz: Die Installation dieser Sierra-Module unter Linux ist unkompliziert. Installiere `modemmanager` und die zugehörigen Tools per `apt`, verbinde dich über NetworkManager, und du kannst sogar GPS-Positionen ohne großen Aufwand auslesen.**

Viele bekommen ein EM7455, EM7565, EM919x oder MC7455, stecken es an das Mainboard und wissen dann nicht, wie sie online gehen. Tatsächlich ist die Unterstützung dieser Module unter Linux sehr ausgereift. Sie kommunizieren alle über USB mit den Protokollen QMI oder MBIM. In dieser Anleitung führen wir dich Schritt für Schritt durch die Einrichtung.

> Alle Spezifikationen und technischen Angaben stammen aus der offiziellen Sierra Wireless Dokumentation. Zusammengestellt von Yupitek.

---

## Bevor du loslegst: Kenne deine Hardware

Wenn die Hardware nicht passt, helfen dir keine Softwarebefehle der Welt.

| Modul | Formfaktor | Geschwindigkeitsklasse | Hauptprotokoll unter Linux | Antennenanzahl |
|---|---|---|---|---|
| **EM7455** | M.2 (42 mm lang) | Cat 6 (300/50 Mbit/s) | QMI | 3 (Main, GNSS, Aux) |
| **EM7565** | M.2 (42 mm lang) | Cat 12 (600/150 Mbit/s) | QMI / MBIM | 3 (Main, GNSS, Aux) |
| **EM919x** (5G) | M.2 (**52 mm** lang) | 5G NR / LTE Cat 20 | MBPW und andere Breitbandpakete | 4 oder mehr |
| **MC7455** | mPCIe (älterer Slot) | Cat 6 (300/50 Mbit/s) | QMI | 3 U.FL-Stecker |

**Zwei Hardware-Fallstricke, die du dir merken solltest:**
1. **Das EM919x ist länger**: Mit 52 mm passt es nicht in einen 42-mm-Slot. Wenn du es hineinzwängst, beschädigst du das Board.
2. **Keine Antenne, kein Signal**: Schließe mindestens die Hauptantenne (Main) an. Für die Positionierung brauchst du eine GPS-Antenne, die in den eigenen **GNSS-Anschluss** gehört.

---

## Schritt 1: Die wichtigsten Linux-Tools installieren

Unter Ubuntu / Debian / Linux Mint musst du keine Treiber selbst schreiben oder kompilieren. Die Paketquellen haben alles vorbereitet.

Öffne ein Terminal und führe diese zwei Zeilen aus:
```bash
sudo apt update
sudo apt install modemmanager libqmi-utils libmbim-utils
```
Prüfe nach der Installation, ob der Dienst läuft:
```bash
systemctl status ModemManager
```
Mit diesen Tools versteht dein Linux die 4G/5G-Karte.

---

## Schritt 2: Prüfen, ob das System die Karte erkennt

Stecke die Karte ein, starte den Rechner und führe diese drei Befehle zur Kontrolle aus:

1. **USB-Hardware prüfen:**
   ```bash
   lsusb
   ```
   (Du solltest ein Sierra- oder Qualcomm-Gerät sehen.)

2. **Kernel-Treiber prüfen:**
   ```bash
   dmesg | grep -iE 'qmi|mbim|cdc|wwan'
   ```
   (Wenn `cdc-wdm0` und `wwan0` erscheinen, wurde das Interface erfolgreich eingebunden.)

3. **ModemManager-Status prüfen:**
   ```bash
   mmcli -L
   ```
   (Hier werden die Modems mit ihren Nummern aufgelistet. Notiere dir die Nummer, meistens `0`.)

---

## Schritt 3: Einfach verbinden (mit NetworkManager)

Wenn du die Desktop-Version von Ubuntu oder Mint nutzt, ist der eingebaute Netzwerkmanager am bequemsten.

```bash
# Eine Verbindung anlegen (ersetze "internet" durch den APN deines Anbieters)
nmcli connection add type gsm ifname cdc-wdm0 con-name "mobile" apn "internet"

# Und los geht's!
nmcli connection up mobile
```
Das war's. Mit `ip addr show` kannst du prüfen, ob `wwan0` eine IP bekommen hat.

### (Fortgeschritten) Textmodus-Verbindung ohne Desktop
Auf einem headless Server oder einem Embedded-Board kannst du das Modul direkt mit `qmicli` steuern:
```bash
sudo ip link set wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn=internet,ip-type=ipv4" --client-no-release-cid
sudo dhclient -v wwan0
```

---

## Schritt 4: GPS-Positionierung aktivieren!

Alle diese Module haben ein eingebautes GNSS-Positionierungssystem (Unterstützung für GPS, GLONASS und mehr).
Laut offizieller Spezifikation:
- EM7455 / EM7565 / MC7455: 1 Sekunde Hot Start, 32 Sekunden Cold Start. Horizontale Genauigkeit etwa 2 bis 5 Meter.
- Das 5G-Modul EM919x: schnellerer Cold Start (≤28 Sekunden), etwas bessere Genauigkeit (<4 m bei 95 %).

**So holst du unter Linux am schnellsten Koordinaten ab:**

1. GPS-Funktion aktivieren:
```bash
mmcli -m 0 --location-enable-gps-raw
```
2. Aktuelle Koordinaten abrufen:
```bash
mmcli -m 0 --location-get
```
Deine aktuelle Breiten- und Längengrad werden direkt ausgegeben. Wenn du die Position in Echtzeit an andere Programme streamen willst, kombiniere das mit `gpsd`.

---

## Häufige Stolperfallen und schnelle Lösungen

1. **`mmcli -L` zeigt nichts an**: `ModemManager` ist vielleicht abgestürzt, oder dein USB-Strom reicht einfach nicht für die Karte.
2. **GPS-Positionierung schlägt immer fehl**: Hast du die GPS-Antenne an Main oder Aux gesteckt? Der GNSS-Port ist ein eigener Anschluss!
3. **Das EM919x erreicht nicht die volle Geschwindigkeit**: Es ist eine 5G-Karte, die USB 3.1 Gen 2 und sogar PCIe Gen 3 unterstützt. Steckst du sie in einen USB-2.0-Port, garantiert der Hersteller keine Leistung.

## Fazit

Mit Sierra-Modulen unter Linux zu arbeiten ist nicht so schwer, wie es scheint. Prüfe Slot und Antennen, installiere die `modemmanager`-Paketfamilie, setze den APN und du bist online. Dieser Ablauf passt perfekt für Ingenieure, die mit Edge Computing oder industriellem IoT (IIoT) arbeiten.

## Wo kaufen (Call To Action)

Du willst ein Sierra-Modul in dein Ubuntu-Gerät integrieren? Yupitek bietet komplette Lösungen: Module, Antennen und Adapterplatten, plus technische Unterstützung in der ersten Linie.
Kontaktiere uns: **sales@yupitek.com**
Produkte ansehen: [Sierra Wireless Serie](https://yupitek.com/de/products/sierra/)

{{< faq >}}
