---
title: "Einen 4G/5G-Router mit Raspberry Pi und OpenWrt bauen: Sierra-Modul-Supportmatrix und Setup-Anleitung"
description: "Baue deinen eigenen OpenWrt-Router mit einem Raspberry Pi und Sierra Wireless 4G/5G-Modulen (EM7455, EM7565, EM7511, EM919x, MC7455). Komplette Supportmatrix, QMI/MBIM-Konfiguration, wwan0-Interneteinrichtung sowie Hinweise zu Stromversorgung und Antennen."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "raspberry-pi-openwrt-lte-router"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/de/products/sierra/"
faq:
  - question: "Welches Sierra-Modul sollte ich für einen OpenWrt-Router auf einem Raspberry Pi wählen?"
    answer: "Anfänger sollten mit dem EM7455 starten, denn dazu gibt es viele Tutorials und Probleme lassen sich leicht recherchieren. Für hohen Upload-Durchsatz wählst du den EM7565 oder EM7511, für 5G den EM919x und für alte mPCIe-Slots den MC7455."
  - question: "Was ist der Unterschied zwischen QMI und MBIM?"
    answer: "QMI ist das eigene Protokoll von Qualcomm, während MBIM das spätere standardisierte Protokoll ist. Beide funktionieren unter OpenWrt, aber die meisten Online-Anleitungen verwenden QMI."
  - question: "Was soll ich tun, wenn der Raspberry Pi das Modul nicht erkennt?"
    answer: "Die häufigste Ursache ist eine unzureichende USB-Stromversorgung am Raspberry Pi (der Spitzen-Einschaltstrom kann 2,5 A erreichen). Prüfe die Stromversorgung der Adapterplatine und die Verkabelung und warte etwa zehn Sekunden, bis das Modul den Bootvorgang abgeschlossen hat."
---

Kann ein Raspberry Pi ein Sierra Wireless 4G/5G-Modul in einen voll funktionsfähigen OpenWrt-Router verwandeln? Ja, das kann er. M.2-Module wie EM7455, EM7565, EM7511 und EM919x werden in Linux nativ unterstützt. Installiere `kmod-usb-net-qmi-wwan` oder `kmod-usb-net-cdc-mbim`, konfiguriere `wwan0`, und du bist online. Dieser Artikel behandelt die vollständige Modul-Supportmatrix, die schrittweise Konfiguration und die Fallstricke bei Stromversorgung und Antennen.

{{< tldr >}}
Ein Raspberry Pi mit einem Sierra 4G/5G-Modul ergibt einen zuverlässigen OpenWrt-Router. Die meisten M.2-Module (EM7455, EM7565, EM7511) nutzen USB, der EM919x bringt zusätzlich eine PCIe-Gen3-Lane mit, und der MC7455 ist die mPCIe-Version des EM7455. Unter OpenWrt ist das QMI-Protokoll mit `wwan0` der empfohlene Weg: Installiere `kmod-usb-net-qmi-wwan`, `uqmi` und `luci-proto-qmi`, trage den APN in `/etc/config/network` ein und starte dann das Netzwerk neu. Zur Geschwindigkeit: EM7455 / MC7455 sind LTE Cat 6 (300/50 Mbit/s), EM7565 / EM7511 sind Cat 12 (600/150 Mbit/s) und die EM919x-Familie liefert 5G Sub-6 (der EM9190 ergänzt mmWave).
{{< /tldr >}}

## Vollständige Sierra-Modul-Supportmatrix unter OpenWrt

Bevor du loslegst, prüfe dein Modul anhand dieser Tabelle:

| Modell | Geschwindigkeitsklasse | Basisband-Chip | Formfaktor | Linux-Datenpfad | GNSS-Positionierung |
|---|---|---|---|---|---|
| **EM7455** | LTE Cat 6 (300/50 Mbit/s) | MDM9230 | M.2 (42x30 mm) | QMI (Linux) / MBIM | GPS/GLONASS/BeiDou/Galileo |
| **EM7565** | LTE Cat 12 (600/150 Mbit/s) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM (beide unter Linux) | ergänzt QZSS |
| **EM7511** | LTE Cat 12 (600/150 Mbit/s) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM | ergänzt QZSS |
| **EM919x** (9190/9191/7690) | 5G Sub-6 (9190 ergänzt mmWave) | SDX55 | M.2 (52 mm Länge) | Windows/Linux | L1 + L5 (optional) |
| **MC7455** | LTE Cat 6 (300/50 Mbit/s) | MDM9230 | mPCIe (50,95x30 mm) | QMI / MBIM | GPS/GLONASS/BeiDou/Galileo |

### So wählst du ein Modul

- **Einsteiger**: Wähle den **EM7455**. Anleitungen gibt es reichlich und Probleme lassen sich leicht recherchieren.
- **Hoher Upload-Bedarf (Live-Streaming, Überwachung)**: Wähle den **EM7565** oder **EM7511** für bis zu 150 Mbit/s Upload.
- **5G erforderlich**: Wähle den **EM9190** für 5G-Geschwindigkeiten.
- **Nur alter mPCIe-Slot vorhanden**: Nimm den **MC7455**.

## Drei Möglichkeiten, die Hardware anzuschließen

### A. Raspberry Pi 5 + M.2-HAT (PCIe)

Der Pi 5 hat PCIe, sodass du mit einer M.2-HAT+-Trägerplatine ein M.2-WWAN-Modul direkt einstecken kannst (vergewissere dich, dass es ein B-Key ist).

### B. Raspberry Pi 4B oder älter + USB-WWAN-Adaptergehäuse

EM-Serien-Module unterstützen auch USB 2.0/3.0, daher ist ein M.2-zu-USB-Gehäuse (meist mit eingebautem SIM-Slot) am USB-Port des Pi der einfachste und zugänglichste Weg.

### C. MC7455 (mPCIe)-Adapter

Der MC7455 nutzt die ältere mPCIe-Schnittstelle, daher brauchst du eine mPCIe-zu-USB- oder mPCIe-zu-M.2-Adapterplatine.

> ⚠️ **Stromversorgung ist die größte Falle**: Das Modul zieht 3,135 bis 4,4 V (typischerweise 3,3 V). Ein „Modul nicht erkannt"-Fehler bedeutet meist, dass die USB-Stromversorgung des Raspberry Pi nicht genug Leistung liefert. Der Einschaltstrom kann auf 2,5 A ansteigen, also plane ausreichend Reserven bei deiner Stromquelle ein.

## QMI und MBIM verstehen

Beide Protokolle steuern, wie das 4G/5G-Modul sich mit dem Netzwerk verbindet:

- **QMI**: Qualcomms eigenes Protokoll, das in den meisten Linux/OpenWrt-Anleitungen verwendet wird (das Interface erscheint als `wwan0`).
- **MBIM**: das spätere standardisierte Protokoll, das sowohl unter Windows als auch unter Linux nutzbar ist (das Interface erscheint ebenfalls als `wwan0`).

**Welches nehmen?** Die meisten Nutzer können direkt QMI verwenden. Wechsle nur dann zu MBIM, wenn es deine Firmware ausdrücklich verlangt.

## Praxis Teil 1: QMI unter OpenWrt konfigurieren

Vier Schritte, keine Kompilierung nötig.

### 1. Pakete installieren

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi
```

### 2. Prüfen, ob der Raspberry Pi das Modul erkennt

```bash
lsusb                                  # nach einem Sierra-Gerät suchen
ls /dev/cdc-wdm*                       # QMI-Kontrollkanal
dmesg | grep qmi_wwan                  # prüfen, ob der Treiber geladen wurde
ip link show wwan0                     # prüfen, ob das Interface erschienen ist
```

### 3. Die Netzwerkkonfiguration (`/etc/config/network`) anpassen

Füge einen QMI-Abschnitt hinzu und ersetze den APN durch den deines Anbieters:

```bash
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option auth 'none'
```

### 4. Netzwerk neu starten

```bash
/etc/init.d/network restart
ifup wwan
```

Fertig. Sobald `wwan0` eine IP-Adresse erhält, bist du online.

## Antennen und SIM: Diese Punkte nicht überspringen

Das Modul hat **keine eingebaute Antenne**, und die Antennenqualität wirkt sich direkt auf deinen Durchsatz aus.

- **Hauptantenne**: Pflicht.
- **Hilfsantenne (Aux)**: erforderlich für MIMO-Geschwindigkeiten; ohne sie sinkt der Durchsatz.
- **GNSS-Antenne**: nur für Positionierungsanwendungen. Verwechsle sie nicht mit der Hauptantenne.

## Häufige Fallstricke (Pflichtlektüre für Anfänger)

1. **`lsusb` zeigt nichts an**: In 99 % der Fälle liegt es an unzureichender Stromversorgung, einer locker sitzenden Adapterplatine oder einem defekten Kabel.
2. **Zu ungeduldig**: Das Modul braucht Zeit zum Booten. Warte nach dem Einstecken 10 Sekunden, bevor du Befehle ausführst.
3. **5G-Module (EM919x) werden heiß**: Temperaturen um 100 °C sind normal (max. 115 °C), also plane Kühlung ein.
4. **ModemManager-Konflikte**: Wenn du manuell an einem normalen Linux-System arbeitest, stoppe zuerst `ModemManager` (`systemctl stop ModemManager`), damit er das Modul nicht übernimmt.

## Zusammenfassung

Ein Sierra-Modul mit einem Raspberry Pi unter OpenWrt zu betreiben ist ein Checklisten-Prozess. Prüfe die Hardware (Formfaktor, Spannung, Antennen), installiere die QMI/MBIM-Treiber und trage dann den APN ein. Wir hoffen, diese Anleitung erspart deinem Projekt ein paar Umwege und bringt deinen Raspberry Pi auf volle 4G/5G-Geschwindigkeit.

## Kaufinformationen (Aufruf zum Handeln)

Wenn du EM7455-, EM7565- oder EM7511-Module oder passende M.2-Adapterplatinen und Antennen brauchst: Yupitek bietet komplette Hardware-Lösungen und technische Beratung.

Schreib uns: **sales@yupitek.com**

Produkte ansehen: [Yupitek Sierra Wireless Serie](https://yupitek.com/en/products/sierra/)
