---
title: "Sierra EM7455 im Test: Warum es die Lieblings-Sierra-Karte für Makers und Labore ist"
description: "Kompletter EM7455-Test: Spezifikationen, Unterschiede zum EM7430, OpenWrt/Linux-Setup und Dell/Lenovo-Kompatibilität. Technische Daten von Yupitek zusammengestellt."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em7455", "lte-a", "cat-6", "openwrt", "linux", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM7455_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "Unterstützt der EM7455 5G?"
    answer: "Nein. Es ist ein LTE-A-Cat-6-Modul mit maximal 300 Mbit/s. Für 5G schau dir den EM9190 oder EM9191 an."
  - question: "Funktioniert der EM7455 in Taiwan?"
    answer: "Ja, mit den gängigen taiwanesischen Providern, solange deine SIM ein unterstütztes Band nutzt. Tatsächliche Signalstärke und Carrier Aggregation hängen von der Zellenabdeckung ab, also sprich die Kompatibilität vor dem Kauf besser mit uns ab."
  - question: "Was ist der Unterschied zwischen EM7455 und MC7455?"
    answer: "Beide basieren auf demselben Qualcomm-MDM9230-Chipsatz mit identischen Spezifikationen. Der einzige Unterschied ist das Gehäuse: EM7455 ist M.2, MC7455 ist mPCIe. Die Wahl hängt von deinem Steckplatz ab."
  - question: "Was ist der Unterschied zwischen EM7455 und EM7430?"
    answer: "Sie teilen sich denselben MDM9230-Chipsatz und dieselben Kern-Spezifikationen. Der Hauptunterschied liegt in der Bandabdeckung: Der EM7455 deckt Bänder für Amerika und EMEA ab, der EM7430 für den asiatisch-pazifischen Raum."
  - question: "Ist der Dell DW5811e dasselbe wie der EM7455?"
    answer: "Ja. Der DW5811e ist Dells umgelabelter EM7455 auf Basis desselben Qualcomm-MDM9230-Chipsatzes."
---

# Sierra EM7455 im Test: Warum es die Lieblings-Sierra-Karte für Makers und Labore ist

Wenn du schon mal mit einem Raspberry Pi und OpenWrt gespielt hast oder Laborgeräten 4G geben wolltest, hast du bestimmt von der legendären Sierra-EM7455-Karte gehört! Sie ist ein LTE-A-Cat-6-Mobilfunkmodul von Sierra Wireless im M.2-Format mit Qualcomm-MDM9230-Chipsatz: bis zu 300 Mbit/s Download und 50 Mbit/s Upload, eingebautes GNSS und ein Betriebstemperaturbereich, der sogar -40°C bis +85°C übersteht.

Dieser Artikel wurde von Yupitek zusammengestellt und erklärt, warum dieses 4G-LTE-Advanced-Cat-6-Modul im M.2-B-Key-Gehäuse so beliebt ist und wie du Treiber und Konfiguration unter Linux hinbekommst.

> Produktlink: [EM7455 — Yupitek-Produktseite](/de/products/sierra/em7455/) | Offizielles Spec-Sheet: [AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## Die komplette EM7455-Spezifikation: Alle harten Zahlen auf einen Blick

Die Zahlen unten stammen aus der offiziellen Sierra-Wireless-Spezifikation. Wie immer gilt: Wenn du für ein echtes Projekt bestellst, frag vorher nach dem aktuellen offiziellen Dokument, besonders bei Punkten, die sich ändern können, wie Bänder oder Firmware-Versionen.

| Punkt | Spezifikation |
|---|---|
| **Modell** | AirPrime EM7455 |
| **Mobilfunkstandard** | LTE-A Cat 6 |
| **Chipsatz** | Qualcomm MDM9230 (Snapdragon X7 LTE) |
| **Download-Spitzenwert** | 300 Mbit/s (LTE-A, 2×CA) |
| **Upload-Spitzenwert** | 50 Mbit/s (LTE-A) |
| **Carrier Aggregation** | 2×CA (mehrere Kombinationen, Details im offiziellen AT-Command-Referenzdokument) |
| **Gehäuse** | PCI Express M.2 B-Key (52-Pin) |
| **Abmessungen** | 42 × 30 × 2.3 mm |
| **Betriebstemperatur** | -40°C ~ +85°C (Industriequalität) |
| **GNSS** | GPS, GLONASS, BeiDou, Galileo |
| **Host-Interface** | USB 3.0 / USB 2.0 High Speed |
| **LTE-Bänder** | Gängige Bänder für Amerika und EMEA (Europa/Mittlerer Osten/Afrika); die vollständige Bandliste bitte gegen das aktuelle offizielle Spec-Sheet bestätigen |
| **3G-WCDMA-Bänder** | Bitte gegen das aktuelle offizielle Spec-Sheet bestätigen |
| **Generische VID:PID** | `1199:9079` (EM7455, Standardversion) |
| **Dell DW5811e VID:PID** | `413c:81b6` (Markenversion; verlässlich per `lsusb` an deinem Gerät prüfen) |
| **Linux-Treiber** | `qcserial`, `qmi_wwan`, `cdc_mbim` (in den meisten gängigen Distributionen enthalten) |
| **Generische Firmware** | Aktuelle Version vom offiziellen source.sierrawireless.com verwenden |
| **Provider-Zertifizierungen** | Variieren je nach Region (z. B. AT&T, Verizon, Vodafone); aktuelle Liste bei uns anfragen |

---

## Für welche Projekte ist der EM7455 geeignet?

**Kurz gesagt, der EM7455 ist die Rettung für drei klassische Anwendungen: (1) eigenen 4G-LTE-Router auf Open-Source-Firmware wie OpenWrt oder ROOter bauen, (2) die WWAN-Karte in einem Dell- oder Lenovo-Laptop upgraden, (3) IoT-Gateways oder Telematik-Tracker in Industrieprojekten aufbauen.**

Sein größter Vorteil: ein sehr ausgereiftes Linux-Treiber-Ökosystem, massenhaft Tutorials in der Community und breite Bandunterstützung.

### Wenn du Maker oder Student bist

| Anwendung | Wie kombinieren | Warum diese Karte |
|---|---|---|
| 4G-Router mit Raspberry Pi | Raspberry Pi 4/5 + M.2-zu-USB-Adapter + OpenWrt / ROOter | Felsenfeste OpenWrt-Community-Unterstützung, starkes `uqmi`-Paket |
| GL.iNet-Router-Upgrade | GL-MT1300 / GL-AR750S + USB-Adapter | Community-Diskussionen zur `create_connect.sh` für ROOter: einfach abschauen |
| Tragbarer LTE-Hotspot für draußen | Akkubetrieb + USB-Adapter + Mini-Router | Geringe Wärmeentwicklung, gutes thermisches Verhalten, ideal für Objekt-Tracking im Außeneinsatz |

### Für Enterprise- oder Industrieprojekte

| Anwendung | Wie kombinieren | Warum diese Karte |
|---|---|---|
| Industrierouter | Industrie-Gateway mit M.2-Steckplatz (z. B. Advantech) | Robust, beruhigende -40~85°C-Temperaturspezifikation, genug Bänder |
| Telematik / Flotte | Fahrzeug-Gateway + GNSS-Antenne | Eingebautes GPS/GLONASS: Konnektivität und Ortung auf einer Karte |
| WWAN-Upgrade im Laptop | Dell Latitude / Lenovo ThinkPad | M.2 B-Key steckt direkt; Linux erkennt die Karte meist plug-and-play |
| WAN-Failover | OpenWrt / pfSense mit Dual-WAN-Failover | Unterstützt QMI/MBIM-Dualmodus (pfSense-Unterstützung ist Glückssache, OpenWrt ist sicherer) |

---

## EM7455 vs. EM7430: Was ist wirklich anders?

Diese Frage kommt sehr oft. Tatsächlich **nutzen EM7455 und EM7430 exakt denselben Qualcomm-MDM9230-Chipsatz, die Kern-Spezifikationen (Cat 6, 300/50 Mbit/s, 2×CA, GNSS) sind identisch. Der echte Unterschied liegt in den Ziel-Bändern der jeweiligen Modelle.** Der EM7455 ist für Amerika und EMEA (Europa/Mittlerer Osten/Afrika) gedacht, der EM7430 für den asiatisch-pazifischen Raum (APAC).

| Punkt | EM7455 | EM7430 |
|---|---|---|
| **Chipsatz** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **Mobilfunkstandard** | LTE-A Cat 6 | LTE-A Cat 6 |
| **Download-Spitzenwert** | 300 Mbit/s | 300 Mbit/s |
| **Upload-Spitzenwert** | 50 Mbit/s | 50 Mbit/s |
| **Carrier Aggregation** | 2×CA | 2×CA |
| **Gehäuse** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **Zielregion** | Amerika, EMEA | Asiatisch-pazifischer Raum (APAC) |

**Kurzer Auswahltipp:** Wenn die SIM-Karten deines Projekts oder deiner Geräte vor allem in Nordamerika oder Europa genutzt werden, nimm den **EM7455**; im asiatisch-pazifischen Raum (wie Taiwan, Japan, Australien) passt theoretisch der **EM7430** besser. Weil die Bandverteilung bei taiwanesischen Providern aber speziell ist, frag vor der Bestellung besser bei uns nach, welche Karte zu deinem Provider passt.

---

## EM7455 vs. MC7455: Identischer Chip, nur anderer Anschluss

Wie oben erwähnt, nutzen EM7455 (M.2) und MC7455 (mPCIe) denselben Qualcomm MDM9230, elektrisch sind sie komplett identisch. Der einzige Unterschied ist die „Haut", also das Gehäuse:

| Punkt | EM7455 | MC7455 |
|---|---|---|
| **Gehäuse** | M.2 (B-Key) | Mini PCIe (mPCIe) |
| **Abmessungen** | 42 × 30 × 2.3 mm | 51 × 30 × 3.5 mm |
| **Geeignet für** | WWAN-Steckplätze in Laptops, moderne Dev-Boards | mPCIe-Steckplätze älterer Panel-PCs |
| **Generische VID:PID** | `1199:9079` | `1199:9071` |

**Ganz einfach: Nimm die Karte, die zu deinem Gerätesteckplatz passt.** Falls du dich vertan hast, rettet meist eine Adapterplatine (M.2-auf-mPCIe oder umgekehrt).

---

## Einrichtung unter Linux (Ubuntu / Debian / Linux Mint)

Der EM7455 wird unter gängigen Linux-Systemen sehr gut unterstützt. Unten stehen die üblichen Basis-Schritte aus der Community. Denk daran: Jede Maschine hat eine andere OS-Version und einen anderen Kernel, also teste zuerst auf einem Nicht-Produktionssystem.

### Schritt 1: Prüfen, ob die Hardware erkannt wird

```bash
lsusb | grep -i sierra
# Du solltest eine Ausgabe sehen wie: Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### Schritt 2: Nötige Werkzeuge installieren

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### Schritt 3: USB-Modus auf QMI umstellen

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# Prüfen, ob die Umstellung geklappt hat
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# Du solltest sehen: USB composition 6: DM, NMEA, AT, QMI
```

> Wenn dein Provider den MBIM-Modus verlangt, such dir den Befehl `AT!USBCOMP` und verbinde dich stattdessen mit `mbimcli`.

### Schritt 4: FCC-Auth freischalten

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# Für vollautomatische Abwicklung über ModemManager:
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### Schritt 5: Über NetworkManager verbinden

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn 'DEIN_APN'
sudo nmcli connection up 'EM7455 LTE'
```

### Schritt 6: Manuelle QMI-Verbindung (für fortgeschrittene Fehlersuche)

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='DEIN_APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## QMI unter OpenWrt einrichten

Der EM7455 genießt in der OpenWrt-Community hohes Ansehen. Wenn du einen Router mit OpenWrt-Firmware hast, hier die Standard-QMI-Einrichtung.

### Notwendige Pakete installieren

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### Netzwerkkonfiguration bearbeiten

Öffne `/etc/config/network` und füge diesen Interface-Block hinzu:

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'DEIN_APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### Netzwerk neu starten

```bash
/etc/init.d/network restart
```

Wenn du lieber mit der Maus arbeitest (LuCI-Web-Interface): unter „Network" → „Interfaces" ein neues Interface anlegen, Protokoll „QMI" wählen, Gerät `/dev/cdc-wdm0` auswählen und deinen APN eintragen, fertig.

> Tipp für Raspberry-Pi-Fans: Probier unbedingt ROOter aus (eine OpenWrt-basierte Firmware, die speziell auf 4G/5G-Routing ausgelegt ist) — viele praktische Konfigurations-Hooks sind schon eingebaut.

---

## Kompatibilität mit Marken-Laptops: Dell und Lenovo

### Dell-Laptops (diese Karte heißt DW5811e)

Im Netz stößt man oft auf den Dell DW5811e. Das ist Dells umgelabelter EM7455 (VID `413c`, PID `81b6`) mit demselben MDM9230-Chip im Inneren, und die meisten Linux-`qmi_wwan`-Treiber erkennen ihn schon lange.

```bash
lsusb | grep 413c
# Du solltest etwas sehen wie: Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

Gute Nachricht: Laut Community-Berichten haben die meisten Dell-Laptops (Latitude, Precision usw.) keine lästige BIOS-Whitelist, die Karte funktioniert also meist direkt nach dem Einstecken.

### Lenovo-Laptops (die nervige Whitelist)

Bei einem Lenovo ThinkPad ist Vorsicht geboten. Lenovo erzwingt manchmal eine BIOS-Whitelist, die nur Original-FRU-Karten von Lenovo zulässt. Einige Foren-Mitglieder haben AT-Befehle geteilt, die die Sperre umgehen, für alle mit Abenteuerlust:

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **Warnung: Diese Befehle stammen aus Foren. Falsch ausgeführt können sie deine Karte in einen Ziegel verwandeln!** Wenn du nicht zu den Fortgeschrittenen gehörst, die gern Hardware auseinandernehmen und Risiken eingehen, frag uns vor der Bestellung nach sichereren Alternativen.

---

## Welche Plattformen werden unterstützt? Alles in einer Tabelle

| Deine Plattform | Unterstützungsgrad | Verbindungsart | Hinweis |
|---|---|---|---|
| Raspberry Pi + OpenWrt | ✅✅ sehr stabil, viele Tutorials | QMI / MBIM | Du brauchst eine kleine M.2-zu-USB-Adapterplatine |
| Raspberry Pi + ROOter | ✅✅ | QMI | Absolut empfehlenswert für Pi-Nutzer |
| Ubuntu / Debian | ✅✅ | ModemManager / QMI | Sehr wahrscheinlich plug-and-play |
| DD-WRT | ⚠️ Glückssache | QMI / PPP | Kaum Community-Diskussionen, nichts für Anfänger |
| pfSense | ⚠️ Wundertüte | QMI / PPP | Eher zu OpenWrt greifen, weniger Gefummel |
| Dell-Laptops | ✅ | QMI / MBIM | Linux erkennt sie praktisch immer |
| Lenovo-Laptops | ⚠️ Eventuell Umgehung nötig | QMI | Achtung BIOS-Whitelist, unbedachte Befehle riskieren Ziegelsteine |

---

## Wo finde ich weitere Ressourcen?

Wenn du bei deinem Projekt hängen bleibst, lohnt sich ein Blick in diese Open-Source-Communities:

- **danielewoods GitHub**: sehr vollständige Skripte und Diskussionen zu EM7455/MC7455.
- **Gentoo Wiki**: eine sehr detaillierte Troubleshooting-Basis von der Linux-Community.
- **OpenWrt LTE Wiki**: die offizielle Dokumentation, unbedingt lesen, bevor du das Netzwerk konfigurierst.

## Häufig gestellte Fragen

{{< faq >}}

---

## Einkauf fürs Labor? Sprich uns an

Dieser Artikel wurde vom Engineering-Team von Yupitek zusammengestellt. Ob Universitätsprojekt, Laborprogramm oder Enterprise-Großbestellung von EM7455 oder anderen Sierra-Modulen — komm gern auf uns zu!

- **Karte ansehen**: [https://yupitek.com/de/products/sierra/em7455/](/de/products/sierra/em7455/)
- **Alle Sierra-Modelle**: [https://yupitek.com/de/products/sierra/](/de/products/sierra/)
- **Uns schreiben**: sales@yupitek.com
