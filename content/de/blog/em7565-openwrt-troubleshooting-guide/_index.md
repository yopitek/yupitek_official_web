---
title: "Sierra EM7565 wird unter OpenWrt oder Raspberry Pi nicht erkannt? Vollständiger QMI/MBIM-Fehlerbehebungs-Leitfaden"
description: "EM7565 wird unter OpenWrt oder auf dem Raspberry Pi nicht erkannt oder der QMI-Port ist verschwunden? Dieser Leitfaden führt dich von lsusb und dmesg über die USB-Komposition, das Laden der Treiber und die EM7565-Konfigurationsschritte, um Hardware- und Software-Verbindungsprobleme zu lösen."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "em7565-openwrt-troubleshooting-guide"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/de/products/sierra/em7565/"
faq:
  - question: "Was ist der häufigste Grund, warum der EM7565 unter OpenWrt nicht erkannt wird?"
    answer: "Die häufigste Ursache ist eine unzureichende Stromversorgung (VCC außerhalb des Bereichs 3,135 bis 4,4 V), sodass lsusb nichts anzeigt, oder eine falsche USB-Komposition, die das QMI-Interface deaktiviert lässt."
  - question: "Der EM7565 startet ständig neu und bootet nicht. Ist er defekt?"
    answer: "Nicht unbedingt. Er hat einen SED-Schutzmechanismus: Nach 6 aufeinanderfolgenden abnormalen Neustarts wechselt er in einen geschützten Zustand, und ein Neuladen der Firmware stellt ihn wieder her."
---

Weigert sich dein EM7565, unter OpenWrt oder auf einem Raspberry Pi aufzutauchen? Bevor du das Modul austauschst, arbeite den Debugging-Ablauf aus der offiziellen Spezifikation ab. Dieser Leitfaden behandelt die Bestätigung der USB-Hardwareverbindung, die Prüfung der USB-Komposition, das Laden der richtigen Linux-Treiber, das Ausschließen von Störungen durch Systemdienste und den Umgang mit dem kniffligen SED-Zustand der Firmware. Folge diesen fünf Schritten, um die Ursache schnell zu finden.

{{< tldr >}}
Wenn der EM7565 nicht erkannt wird, prüfe diese fünf Dinge: 1. Bestätige die USB-Ebene mit `lsusb` (prüfe Stromversorgung und Adapterplatine). 2. Prüfe das QMI/MBIM-Interface und ob `/dev/cdc-wdm0` existiert; kontrolliere die Treiber `qmi_wwan` / `cdc_mbim` und die USB-Komposition. 3. Stoppe `ModemManager`, um Störungen durch Systemdienste auszuschließen. 4. Prüfe die Einschaltreihenfolge (sende innerhalb von 100 ms nach dem Einschalten keine Signale; die Restwelligkeit muss unter 100 mVp-p bleiben). 5. Prüfe den Firmware-Zustand: 6 aufeinanderfolgende fehlgeschlagene Boots lösen den SED-Schutz aus, der ein Neuladen der Firmware erfordert. Das Prinzip: zuerst die Hardware, dann die Software, die Firmware zuletzt.
{{< /tldr >}}

**Der EM7565 ist ein M.2-WWAN-Modul vom Typ 3042-S3-B (4G LTE-Advanced) auf Basis des Qualcomm MDM9250. Es unterstützt sowohl QMI- als auch MBIM-USB-Interfaces.** Wenn OpenWrt oder ein Raspberry Pi es nicht erkennt, liegt der Fehler meist an einer von drei Stellen: Der USB-Port ist nicht mit Strom versorgt, die USB-Komposition steckt in einer falschen Konfiguration fest, oder der Linux-Treiber wurde nicht korrekt geladen. Gelegentlich wechselt das Modul nach wiederholten Neustarts auch in einen Schutzmodus. Nach dem offiziellen Handbuch von Sierra Wireless haben wir eine zuverlässige, schrittweise Debugging-Reihenfolge zusammengestellt.

> Produktlink: [Yupitek Sierra Wireless Serie](https://yupitek.com/en/products/sierra/)

## Schnellfazit: Fünf Schritte, wenn der EM7565 nicht erkannt wird

Der häufigste Fehler beim Debugging ist, sofort zur Neuflashen der Firmware zu springen. **Bestätige zuerst die Hardware, dann die Software, und fasse die Firmware erst zuletzt an.**

1. **Prüfe die USB-Ebene**: Führe `lsusb` aus, um zu sehen, ob das Modul auftaucht. Wenn nicht, prüfe die Stromversorgung (VCC muss 3,135 bis 4,4 V betragen), die Adapterplatine und das USB-Kabel.
2. **Prüfe das QMI/MBIM-Interface**: `lsusb` zeigt das Modul, aber es gibt kein `/dev/cdc-wdm0`? Verifiziere, dass die Treiber `qmi_wwan` / `cdc_mbim` geladen sind, und ob die USB-Komposition nur den Diagnosemodus freigibt.
3. **Prüfe die Systemdienste**: Der systemeigene `ModemManager` könnte das Modul blockieren.
4. **Prüfe die Einschaltreihenfolge**: Sende nach dem Einschalten mindestens 100 ms lang keine Signale und halte die Restwelligkeit unter 100 mVp-p. Instabile Spannung führt dazu, dass die USB-Verbindung immer wieder abbricht und neu aufgebaut wird.
5. **Prüfe den Firmware-Zustand**: Wenn das Modul nach fehlgeschlagenen Boots 6-mal hintereinander neu startet, wechselt es in den SED-Schutzzustand (Smart Error Detection), und du musst die Firmware neu laden.

## Den EM7565 verstehen: Was für ein Modul ist das?

Vor dem Debugging hier ein kurzer Überblick über den EM7565. Es ist ein M.2-Modul, das drei externe Antennen benötigt (Main, GNSS, Aux). Antennen sind nicht im Lieferumfang enthalten.

| Punkt | Offizielle Spezifikation (Doc# 41110788, Rev 8) |
|---|---|
| **Chipsatz** | Qualcomm MDM9250 |
| **Formfaktor** | M.2 (3042-S3-B) / 42 × 30 mm, bis 1,50 mm dick, 6,5 g |
| **Download-Spitze** | Cat 12 (3CA, 256QAM) bis 600 Mbit/s |
| **Upload-Spitze** | Cat 13 (2CA, 64QAM) bis 150 Mbit/s |
| **LTE-Bänder** | B1/2/3/4/5/7/8/9/12/13/18/19/20/26/28/29/30/32/41/46/66 (Hinweis: B42/B43/B48 wurden bis zur behördlichen Freigabe deaktiviert) |
| **Host-Interfaces** | USB 2.0 und USB 3.0; QMI / MBIM / AT-Befehle |
| **Versorgungsspannung** | VCC 3,135 V (min.) / 3,3 V (typ.) / 4,4 V (max.), Restwelligkeit ≤ 100 mVp-p |
| **Betriebstemperatur** | Halte die interne Temperatur unter 90 °C (idealerweise unter 80 °C) |

## Schritt 1: Beginne auf der USB-Ebene

Sieht der Host die Hardware überhaupt?

```bash
lsusb
```

Wenn ein Sierra-Wireless-Gerät erscheint, das mit 1199 beginnt, steht die Hardwareverbindung. Wenn nichts angezeigt wird:

- Prüfe die Stromversorgung: Der Einschaltstrom des EM7565 beim Booten kann 2,2 bis 2,5 A erreichen (max. Betriebsstrom 1,5 A). Viele USB-Adaptergehäuse für den Raspberry Pi schaffen das nicht.
- Gib ihm Zeit: Warte nach dem Einstecken 10 Sekunden, damit die USB-Enumeration abgeschlossen werden kann.

Dann prüfe das Kernel-Log:

```bash
dmesg | tail -50
```

Wenn du siehst, dass `qmi_wwan` `/dev/cdc-wdm0` erstellt, ist das Modul bereit für die Verbindung.

## Schritt 2: USB-Komposition prüfen

Wenn `lsusb` das Modul anzeigt, aber `/dev/cdc-wdm0` nie erscheint, sind die QMI/MBIM-Kanäle im Modul möglicherweise deaktiviert. Eine Einstellung namens USB composition im Modul legt fest, welche Kanäle es freigibt.

Frage sie mit dem Befehl `AT!USBCOMP?` ab. Unachtsames Umschalten kann alle Kanäle entfernen, also dokumentiere die ursprünglichen Parameter, bevor du etwas änderst, und konsultiere das offizielle AT-Befehlshandbuch (Doc#41111748).

## Schritt 3: ModemManager-Störungen ausschließen

Auf Desktop-Linux oder einem Raspberry Pi neigt der eingebaute Dienst `ModemManager` dazu, sich das 4G-Modul zu schnappen. Sobald er die Kontrolle übernimmt, hängen deine eigenen `qmicli`-Befehle.

Stoppe ihn bei der manuellen Fehlersuche zuerst:

```bash
sudo systemctl stop ModemManager
```

Sobald du bestätigt hast, dass das Modul gesund ist, entscheide, ob du manuell einwählst oder die Kontrolle an ModemManager zurückgibst.

## Schritt 4: Ist die Firmware gesperrt? (SED-Schutz)

Wenn das Modul nach dem Einschalten endlos neu startet, könnte es in den Zustand **SED (Smart Error Detection)** gewechselt sein.

Die offizielle Spezifikation ist eindeutig: Wenn kurz nach dem Boot 6 Neustarts auftreten, parkt sich das Modul im Bootloader und wartet auf ein Firmware-Neuladen. Ursache ist meist eine instabile Stromversorgung mit starken Spannungseinbrüchen.

Geh nicht davon aus, dass das Modul tot ist. Wechsle zu einer besseren Stromversorgung und flashe die Firmware mit dem offiziellen Tool neu, um es wiederherzustellen.

## So wählst du dich per QMI ein (OpenWrt-Beispiel)

Sobald du die oben genannten Probleme gelöst hast und `/dev/cdc-wdm0` erscheint, ist das Einwählen unter OpenWrt unkompliziert.

1. Installiere die benötigten Pakete:

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option
```

2. Trage deinen APN in `/etc/config/network` ein (verwende die Werte deines Anbieters):

```text
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

3. Starte das Netzwerk neu:

```bash
/etc/init.d/network restart
```

Das Interface `wwan0` erscheint, und du bist online.

## Zusammenfassung

Ein fehlender EM7565 unter OpenWrt oder auf einem Raspberry Pi ist wie das Reparieren eines Computers: Halte dich an die richtige Reihenfolge, und es geht schnell.

1. **Hardware**: Ist `lsusb` sauber und die Spannung stabil?
2. **Interface**: Ist die USB-Komposition korrekt?
3. **Software**: Sind die Treiber installiert und kämpft ModemManager um das Gerät?
4. **Firmware**: Hat zu viele Neustarts das Modul gesperrt?

Solange du die Firmware nicht blind neu flashst, lassen sich die meisten Probleme innerhalb von zehn Minuten diagnostizieren.

## Kaufinformationen (Aufruf zum Handeln)

Nicht sicher, ob deine Adapterplatine oder deine Antennen mit dem EM7565 funktionieren? Yupitek bietet die komplette Sierra-Wireless-Produktlinie und umfassende Hardware-Integrationslösungen.

Schreib uns: **sales@yupitek.com**

Produkt ansehen: [EM7565-Produktseite](https://yupitek.com/en/products/sierra/em7565/)
