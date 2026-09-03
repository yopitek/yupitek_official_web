---
title: "\"Unterstützt das ALFA Wireless Netzwerkadapter OpenWrt?\""
date: 2026-09-03
draft: false
slug: "alfa-openwrt-router-compatibility"
tags:
  - "ALFA"
  - "OpenWrt"
  - "Router"
  - "kmod-mt76"
  - "AWUS036ACM"
  - "AWUS036ACH"
  - "Soft-AP"
categories:
  - "Hardware-Leitfaden"
description: "OpenWrt最佳支持ALFA USB WiFi卡，MT76芯片型直接支持，Realtek需社区驱动，首选MT7612U。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Problemübersicht

Kunde fragt: "Kann das ALFA-Serie USB-WLAN-Netzwerkadapter auf einem OpenWrt-Router verwendet werden?"

Kurze Zusammenfassung: OpenWrt ist die beste Plattform unter den drei großen Drittanbieter-Routertreibersystemen (DD-WRT / OpenWrt / Tomato) für die Unterstützung der ALFA USB WiFi-Netzwerkadapter. MediaTek-Chipmodelle (AWUS036ACM / ACHM / AXML / AXM) werden durch die offiziellen kmod-mt76-Suite direkt unterstützt; Realtek-Chipmodelle (AWUS036ACH / ACS / EACS / AX / AXER) erfordern die Verwendung von von der Community gepflegten out-of-tree-Treiberpaketen, deren Verfügbarkeit von der OpenWrt-Version abhängt. AWUS036ACM (MT7612U) ist die beste Wahl, da der Treiber ausgereift, stabil und sowohl Monitoring als auch Injection unterstützt.

Bewertungsgrundlage: ALFA hat derzeit 9 aktive USB-Netzwerkadapter (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analyse der Software-Spezifikationen und Anforderungen

### 2.1 Was ist OpenWrt?

OpenWrt ist ein hochmodularer Open-Source-Router-Härtling, der den Linux-Kernel und das opkg-Paketmanagementsystem verwendet. Im Gegensatz zu DD-WRT / Tomato werden die Treiber bei OpenWrt in Form von einzeln installierbaren Kernel-Modulen (kmod) als Pakete bereitgestellt. Benutzer können USB-WLAN-Treiber nach Bedarf installieren, ohne den gesamten Firmwarecode neu zu kompilieren.

### 2.2 USB-WLAN-Treiber-Framework von OpenWrt

Die offizielle Paketbibliothek von OpenWrt enthält die folgenden USB-WLAN-Treiber:

| Treiber-Paket | Quelle | Abgedeckte Chips / Modelle | Wartungsstatus |
|---|---|---|---|
| kmod-mt76-usb + kmod-mt76x2u | Offiziell in-kernel | MediaTek MT7612U (AWUS036ACM) | Aktiv, stabil |
| kmod-mt76-usb + kmod-mt76x0u | Offiziell in-kernel | MediaTek MT7610U (AWUS036ACHM) | Aktiv |
| kmod-mt7921u | Offiziell in-kernel | MediaTek MT7921AUN (AWUS036AXML / AXM) | Ab Version 23.05 verfügbar |
| kmod-rtl8812au-ct | Gemeinschaft out-of-tree | Realtek RTL8812AU / RTL8811AU (AWUS036ACH / ACS) | Gemeinschaftswartung, im Kernel 24.10 Crash-Berichte |
| kmod-rtl8821cu | Gemeinschaft out-of-tree | Realtek RTL8811CU (AWUS036EACS) | Gemeinschaftswartung |
| kmod-rtw89 / kmod-rtl8852bu | In der Entwicklung | Realtek RTL8832BU (AWUS036AX / AXER) | rtw89 USB-Unterstützung wird schrittweise integriert, benötigt neueren Kernel |

### 2.3 Voraussetzung: USB-Kernunterstützung

Bevor Sie den WLAN-Treiber installieren, müssen Sie sicherstellen, dass OpenWrt USB-Kernunterstützung aktiviert hat:

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

Die meisten modernen OpenWrt-Versionen enthalten bereits kmod-usb-core, aber usbutils (stellt die lsusb-Anweisung bereit) müssen Sie manuell installieren.

## 3. Analyse der aktuellen ALFA Netzwerkkarte-Spezifikationen und Chipsets

Bis September 2026 umfasst die aktive USB-WLAN-Produktlinie von ALFA Network wie folgt (Bewertungsgrundlage: 9 Modelle):

| Modell | Wi-Fi-Stufe | Chipset | Schnittstelle | OpenWrt-Treiberpaket |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | kmod-mt7921u (23.05+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | kmod-mt7921u (23.05+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | kmod-rtw89 (in der Entwicklung) / Eigenentwicklung rtl8852bu |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Wie oben |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | kmod-rtl8812au-ct (Community) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | kmod-mt76x0u (offiziell) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | kmod-mt76x2u (offiziell)⭐ Empfohlen |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | kmod-rtl8812au-ct (Abdeckung) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | kmod-rtl8821cu (Community) |

## 4. Geeignete Modelle und Chipsets

### 4.1 Empfehlungsstufen

| Empfehlungsstufe | Modell (Chipset) | Beschreibung |
|---|---|---|
| ⭐ Stark empfohlen | AWUS036ACM (MT7612U) | Offizielle Treiber reif und stabil, unterstützt AP / STA / Monitor / Injection, beste Wahl auf OpenWrt |
| ✅ Empfohlen | AWUS036ACHM (MT7610U) | Offizielle Treiber, Dualband aber nur 433Mbps, geeignet für Low-Power-Szenarien |
| ✅ Empfohlen (neue Version) | AWUS036AXML / AXM (MT7921AUN) | Wi-Fi 6E, offizielle Treiber, benötigt OpenWrt 23.05+ und kernel 5.15+ |
| ⚠️ Verwendbar aber mit Vorsicht | AWUS036ACH (RTL8812AU) | Gemeinschaftstreiber, Kernel-Crash-Berichte in Version 24.10, empfohlen 23.05 zu verwenden |
| ⚠️ Verwendbar aber mit Vorsicht | AWUS036ACS (RTL8811AU) | Wie oben, durch 8812au Treiber abgedeckt |
| ⚠️ Verwendbar aber mit Vorsicht | AWUS036EACS (RTL8811CU) | Gemeinschaftstreiber, Stabilität mittelmäßig |
| ❌ Nicht empfohlen | AWUS036AX / AXER (RTL8832BU) | Wi-Fi 6, rtw89 USB-Unterstützung noch in der Entwicklung, nicht direkt in den meisten OpenWrt-Versionen verwendbar |

### 4.2 Hardwareanforderungen für Router

| Punkt | Mindestanforderung | Empfohlene Anforderung |
|---|---|---|
| USB-Anschluss | USB 2.0 (AWUS036ACHM / ACS / EACS) | USB 3.0 (AWUS036ACH / ACM / AX-Serie) |
| Flash | 16MB (Treiber + Abhängigkeitspakete) | 32MB+ |
| RAM | 128MB | 256MB+ (AP-Modus + mehrere Benutzer) |
| OpenWrt-Version | 21.02+ | 23.05.x (Stabilversion) |

## 5. Umgebungsanforderungen

### 5.1 Software-Umgebung

- Stabile OpenWrt-Version: 23.05.x (Kernel 5.15) oder 24.10.x (Kernel 6.6)
- Paketquellen: Offizielle opkg-Paketbibliothek (https://downloads.openwrt.org/releases/{version}/packages/{arch}/)
- Netzwerkverbindung: Während der Installation der Treiber muss der Router online sein (über den WAN-Port)

### 5.2 Hardware-Umgebung

- OpenWrt-kompatibler Router mit USB 2.0 / 3.0-Port
- Hochleistungsmodelle (AWUS036ACH) werden empfohlen, einen mit Strom versorgten USB 3.0 Hub zu verwenden, um eine unzureichende Stromversorgung des Router-USB-Ports zu vermeiden
- AWUS036AXML hat einen USB-C-Anschluss, bitte stellen Sie sicher, dass der Router einen USB-C-Port hat oder verwenden Sie einen USB-C to USB-A-Adapter

## 6. Kompatibilitätsbewertung

### ALFA laufende Modelle × OpenWrt Kompatibilitätsmatrix

| Modell | Chipset | Treibermethode | USB-Erkennung | STA-Internet | AP-Modus | Monitor | Mindestversion | Gesamtbewertung |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | kmod-mt76x2u | ✅ | ✅ | ✅ | ✅ | 21.02+ | ⭐ Bestes |
| AWUS036ACHM | MT7610U | kmod-mt76x0u | ✅ | ✅ | ✅ | ⚠️ begrenzt | 21.02+ | ✅ Gut |
| AWUS036AXML | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ begrenzt | 23.05+ | ✅ Gut |
| AWUS036AXM | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ begrenzt | 23.05+ | ✅ Gut |
| AWUS036ACH | RTL8812AU | kmod-rtl8812au-ct | ✅ | ✅ | ✅ | ⚠️ begrenzt | 22.03+（24.10 gibt crash） | ⚠️ Verwendbar |
| AWUS036ACS | RTL8811AU | kmod-rtl8812au-ct | ✅ | ✅ | ⚠️ | ❌ | 22.03+ | ⚠️ Verwendbar |
| AWUS036EACS | RTL8811CU | kmod-rtl8821cu | ✅ | ⚠️ | ❌ | ❌ | 23.05+ | ⚠️ Verwendbar |
| AWUS036AX | RTL8832BU | rtw89（in der Entwicklung） | ⚠️ | ❌ | ❌ | ❌ | Bedarf eigener Übersetzung | ❌ Nicht empfohlen |
| AWUS036AXER | RTL8832BU | rtw89（in der Entwicklung） | ⚠️ | ❌ | ❌ | ❌ | Bedarf eigener Übersetzung | ❌ Nicht empfohlen |

Bewertungsgrundlage: Verwendbarkeit der kmod-Pakete im OpenWrt-Offiziellen Paketarchiv (23.05 / 24.10) + Benutzerberichte im OpenWrt-Forum. Die Treiber für Realtek-Chips werden von der Community gepflegt, ihre Stabilität und Funktionalität erreichen nicht die von MediaTek mt76-Serie.

## 7. Detaillierte Step-by-Step-Einstellungen

### 7.1 Vorarbeiten: Aktivieren der USB-Kernunterstützung

**Schritt 1: SSH-Anmeldung am OpenWrt-Router**

```bash
ssh root@192.168.1.1
```

**Schritt 2: Aktualisierung der Paketquellen und Installation der USB-Kernunterstützung**

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

**Schritt 3: Einfügen der ALFA Netzwerkkarte und Überprüfung der USB-Erkennung**

```bash
lsusb
# Erwarteter Ausgabebeschreibung (AWUS036ACM / MT7612U):
# Bus 002 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

### 7.2 Pfad A: MediaTek-Chipsätze (AWUS036ACM / ACHM / AXML / AXM)

Beispiel: AWUS036ACM (MT7612U):

**Schritt 1: Installation der Treibersuite**

```bash
# AWUS036ACM (MT7612U)
opkg install kmod-mt76-usb kmod-mt76x2u

# AWUS036ACHM (MT7610U) — Ändern
# opkg install kmod-mt76-usb kmod-mt76x0u

# AWUS036AXML / AXM (MT7921AUN) — Ändern (erfordert 23.05+)
# opkg install kmod-mt7921u
```

**Schritt 2: Installation der drahtlosen Verwaltungstools**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**Schritt 3: Überprüfung der Netzwerkschnittstelle**

```bash
iw dev
# Erwarteter Ausgabebeschreibung: wlan0 oder wlan1 Schnittstelle
```

**Schritt 4: Scannen der附近的 WiFi (Funktionstest)**

```bash
iw dev wlan0 scan | grep -E "SSID|signal"
```

**Schritt 5: Einstellung als STA-Client-Modus (Verbindung zu einem bestehenden AP)**

Bearbeiten Sie /etc/config/wireless:

```text
config wifi-device 'radio1'
       option type 'mac80211'
       option path 'platform/usb1/1-1/1-1:1.0'
       option channel 'auto'
       option htmode 'VHT80'

config wifi-iface 'wifinet2'
       option device 'radio1'
       option mode 'sta'
       option network 'wwan'
       option ssid 'deinWiFiName'
       option encryption 'psk2'
       option key 'deinWiFiPasswort'
```

**Schritt 6: Neustart des drahtlosen Dienstes**

```bash
/etc/init.d/network restart
```

**Schritt 7: Einstellung als AP-Modus (Netzwerkfreigabe)**

Bearbeiten Sie /etc/config/wireless, ändern Sie das Modus auf ap:

```text
config wifi-iface 'wifinet2'
   option device 'radio1'
   option mode 'ap'
   option network 'lan'
   option ssid 'ALFA-OpenWrt-AP'
   option encryption 'psk2'
   option key 'deinHotspotPasswort'
```

**Schritt 8: Aktivierung des Monitor-Modus (PENETRATIONSTEST)**

```bash
opkg install aircrack-ng
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
iw dev wlan0 set channel 6
# Überprüfung
iw dev wlan0 info
# type sollte monitor anzeigen
```

### 7.3 Pfad B: Realtek-Chipsätze (AWUS036ACH / ACS / EACS)

Beispiel: AWUS036ACH (RTL8812AU):

**Schritt 1: Installation der Community-Treiber**

```bash
opkg update
opkg install kmod-rtl8812au-ct

# AWUS036EACS (RTL8811CU) — Ändern
# opkg install kmod-rtl8821cu
```

**Schritt 2: Installation der drahtlosen Verwaltungstools**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**Schritt 3: Überprüfung der Schnittstelle**

```bash
iw dev
# Beachten: Die Schnittstelle des kmod-rtl8812au-ct-Treibers kann wlan0 oder wlan1 sein
```

Die Konfiguration ist wie in Schritt 7.2 von 5 bis 7 (STA / AP-Modus-Einstellungen).

**Schritt 4: Monitor-Modus**

```bash
# rtl8812au-ct-Treiber unterstützt den Monitor-Modus
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
# Paketinjektionsfunktion ist begrenzt, empfohlen ist der Einsatz von mt76-Chipsätzen für PENETRATIONSTEST
```

**Schritt 5: Bei Kernel-Crash (bekanntes Problem in Version 24.10)**

```bash
# Zurück auf die stabile Version 23.05 oder Verwendung von selbst kompilierten Treibern
# Überprüfen Sie die Crash-Protokolle
logread | grep -i "panic\|crash\|rtl8812"
```

### 7.4 Pfad C: Wi-Fi 6-Modelle (AWUS036AX / AXER, RTL8832BU)

⚠️ Dieser Pfad erfordert eine angepasste OpenWrt-Kompilierung und ist nicht für den durchschnittlichen Benutzer geeignet.

**Schritt 1: Überprüfung, ob die OpenWrt-Version rtw89 USB-Unterstützung enthält**

```bash
opkg list | grep rtw89
# Kein Ergebnis bedeutet, dass die Version diese nicht enthält
```

**Schritt 2: Wenn erforderlich, selbst kompilierte OpenWrt-Images**

Fügen Sie kmod-rtw89 und das zugehörige Firmware-Paket hinzu.

**Alternativvorschlag**: Für den Bedarf an Wi-Fi 6 USB-Netzwerkkarten in OpenWrt-Routern ist derzeit AWUS036AXML (MT7921AUN) die beste Alternative.

## 8. Häufige Fehler und ihre Behebung

| Symptom | Mögliche Ursache | Fehlerbehebung |
|---|---|---|
| lsusb zeigt keine ALFA Netzwerkkarte an | USB-Kern nicht installiert / unzureichende Stromversorgung | Überprüfen Sie, ob kmod-usb-core, kmod-usb2 und kmod-usb3 installiert sind; verwenden Sie einen mit Strom versorgten USB-Hub |
| lsusb zeigt die Karte an, aber iw dev zeigt keine Schnittstelle an | Treiber nicht installiert / inkompatibler Treiber | Installieren Sie die entsprechenden kmod-Pakete; überprüfen Sie dmesg auf fehlende Firmware-Fehlermeldungen |
| opkg install kmod-mt76x2u gibt "kernel version mismatch" aus | OpenWrt-Version und Paketbibliotheksversion stimmen nicht überein | Führen Sie opkg update aus und versuchen Sie es erneut; überprüfen Sie, ob die Firmware-Version mit der Paketbibliotheksarchitektur übereinstimmt |
| AP-Modus kann nicht gestartet werden (hostapd-Fehler) | Treiber unterstützt AP nicht / falsche Kanal-Einstellungen | Überprüfen Sie, ob der Chip den AP-Modus unterstützt; versuchen Sie, den Kanal zu fixieren (z.B. 6 oder 149); überprüfen Sie den Regulatory Domain |
| Monitor-Modus kann keine Pakete injizieren | Treiber unterstützt keine Injektion / Kanal-Kollision | MediaTek mt76-Serie unterstützt am besten; Realtek 8812au-ct hat begrenzte Injektionsfunktionen; überprüfen Sie airmon-ng check kill |
| AWUS036ACH bricht bei hoher Leistung ab | Unzureichende USB-Stromversorgung | Verwenden Sie einen mit Strom versorgten USB 3.0 Hub; stellen Sie in /etc/config/wireless option txpower '20' ein, um die Leistung zu reduzieren |
| Kernel-Panic nach der Installation von rtl8812au-ct auf 24.10 | Bekannte Treiberkompatibilitätsprobleme | Wechseln Sie zu einer stabilen Version 23.05.x; oder verfolgen Sie das GitHub-Issue, um nach Reparaturen zu suchen |
| MT7921 (AXML/AXM) kann 6GHz nicht verwenden | Regulatory Domain-Beschränkung / Kernel-Version | Erfordert Kernel 5.19+ und korrekte Wi-Fi 6E Regulatory Domain-Einstellungen; 6GHz-Unterstützung in OpenWrt 23.05 ist noch in der Testphase |

## 9. Bekannte Einschränkungen

- Realtek-Chip-Treiber für Community-Wartung: kmod-rtl8812au-ct, kmod-rtl8821cu werden nicht offiziell von OpenWrt gewartet, Stabilität und Update-Zeitplan können nicht gewährleistet werden
- 24.10 Version von rtl8812au-ct hat Kernel-Crash-Berichte: Es wird empfohlen, Realtek-Chip-Nutzer auf 23.05.x zu bleiben
- Unzureichende Unterstützung für Wi-Fi 6 (RTL8832BU): rtw89 USB-Treiber ist noch in der Entwicklung, die meisten OpenWrt-Versionen können AWUS036AX / AXER nicht direkt verwenden
- Leistungseinschränkungen im AP-Modus: Bei der Verwendung von USB WiFi als AP ist die Durchsatzrate niedriger als die integrierte WiFi des Routers (USB-Bandbreite + Treiber-Overhead)
- Unterschiedliche Funktionalität von Überwachung/Injection: MediaTek mt76-Serie unterstützt am umfassendsten; Injection-Funktion von Realtek-Chips ist begrenzt und nicht für professionelle Penetrationstests geeignet
- Router-Hardware-Ressourcen: Bei niedrigwertigen Routern (16MB Flash / 128MB RAM) kann nach der Installation des Treibers möglicherweise nicht genügend Speicherplatz vorhanden sein, was andere Funktionen beeinträchtigen kann
- Störungen durch USB 3.0: USB 3.0-Geräte können Störungen im 2.4GHz WiFi verursachen, daher wird empfohlen, USB 2.0-Ports oder gut isolierte USB-Hubs zu verwenden
- Verwendung mehrerer Netzwerkkarten gleichzeitig: Bei der Verwendung von Router-integrierter WiFi + USB WiFi gleichzeitig können Kanalkonflikte oder Ressourcenkonkurrenz auftreten
- ⚠️ **RTL8832BU (AWUS036AX/AXER) Treiberpfleger haben öffentlich empfohlen, die Verwendung zu vermeiden**: Wie im Abschnitt 4.1 gekennzeichnet, "❌ Nicht empfohlen", der Grund ist nicht nur, dass rtw89 USB noch in der Entwicklung ist, sondern auch, dass der Treiberpfleger morrownr öffentlich erklärt hat, dass die Chipserie "sehr schlechter Treiber ist und es gibt Zweifel an den Problemen des Chips selbst", daher wird empfohlen, Linux-Nutzer derzeit zu vermeiden (Quelle siehe Abschnitt 10)
- **Begriffserklärung für Kernel-Versionsschwellenwerte erforderlich**: Die Formulierung im Abschnitt 4.1 "MT7921AUN benötigt OpenWrt 23.05+ und kernel 5.15+" ist leicht irreführend - der mt7921u-Treiber selbst erfordert auf dem Desktop-Linux tatsächlich **kernel 5.19+** (siehe Originalwortlaut des Treiberpflegers), aber die offiziellen OpenWrt-Pakete werden oft durch das Backport-Verfahren frühzeitig aufgenommen, daher hat OpenWrt 23.05 (obwohl basierend auf kernel 5.15) immer noch Benutzerberichte, dass die Installation von kmod-mt7921u erfolgreich ist. **Bitte beurteilen Sie nach den tatsächlichen Ergebnissen der `opkg list`-Abfrage der Kundenversion, nicht nach der Kernel-Version**

Widerspruchskonditionen: Wenn OpenWrt nachfolgende Paketupdates das Problem mit dem Kernel-Crash in der Version 24.10 von rtl8812au-ct behebt, können die Empfehlungen in Abschnitt 4.1 und Abschnitt 6 für AWUS036ACH auf "beibehalten von 23.05" aktualisiert werden; wenn die offizielle Unterstützung von rtw89 USB in die OpenWrt-Offizielspeicherbank aufgenommen wird, muss die "Nicht empfohlene" Bewertung von AWUS036AX / AXER überprüft werden; wenn die offizielle Unterstützung von MT7921 für die 6GHz-Vollfunktion bekannt gegeben wird, müssen die Einschränkungen für AXML / AXM aktualisiert werden.

## 10. Referenzquellen URL

| Quelle | Beschreibung | URL | Überprüfungsstatus | Überprüfungsdatum |
|---|---|---|---|---|
| OpenWrt offizielle Dokumentation | OpenWrt offizieller Dokumentationseintrag (WLAN-Einstellungen / Paketverwaltung) | https://openwrt.org/docs/start | ✅ Geprüft | 2026-09-03 |
| OpenWrt offizieller Forum | USB WiFi Treiber Diskussionseintrag | https://forum.openwrt.org/ | ✅ Geprüft | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux Treiber Quellcode | https://github.com/morrownr/8812au-20210820 | ✅ Geprüft | 2026-09-03 |
| ALFA Network Produktübersicht (Yupitek) | ALFA aktuelle Produkt规格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ Geprüft | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | Treiberbetreuer offizielle Erklärung: Empfehlung, rtl8852/32au (RTL8832BU) Chip zu meiden | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Geprüft | 2026-09-03 |
| morrownr/USB-WiFi Diskussion #292 | mt7921u.ko benötigt Kernel 5.19+ für Anzeige im Kernel (Originalwortlaut des Treiberbetreuers) | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ Geprüft | 2026-09-03 |
| OpenWrt offizieller Forum — Best USB WiFi dongle for Raspberry Pi 4B | Benutzerberichte über erfolgreiche Installation von kmod-mt7921u in OpenWrt 23.05.0 | https://forum.openwrt.org/t/best-usb-wifi-dongle-for-raspberry-pi-4b/160103 | ✅ Geprüft | 2026-09-03 |

Verwandte Artikel: [Ist das ALFA Wireless Netzwerkadapter kompatibel mit DD-WRT](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[Ist das ALFA Wireless Netzwerkadapter kompatibel mit Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[Ist das ALFA Wireless Netzwerkadapter kompatibel mit NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[Ist das ALFA Wireless Netzwerkadapter kompatibel mit NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Haftungsausschluss: Die Kompatibilitätsbestimmungen in diesem Dokument basieren auf der offiziellen OpenWrt 23.05.x / 24.10.x Paketbibliothek. Die Verfügbarkeit von Paketen kann je nach Routerarchitektur (ath79 / ramips / mvebu / x86) variieren. Realtek Chip Treiber werden von der Community gepflegt und die tatsächliche Stabilität kann mit der Version variieren. Es wird empfohlen, MediaTek Chip Modelle (AWUS036ACM als erstes) als bevorzugte Wahl für OpenWrt USB WiFi zu verwenden.
