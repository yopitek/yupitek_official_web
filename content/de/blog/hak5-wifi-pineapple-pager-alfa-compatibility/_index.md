---
title: "HAK5 WiFi Pineapple Pager × ALFA Network: Kompatibilitätsleitfaden für externe USB-WLAN-Adapter"
description: "Detaillierte Kompatibilitätsanalyse und Schritt-für-Schritt-Installationsanleitung für die Verbindung externer ALFA Network USB-WLAN-Karten mit dem HAK5 WiFi Pineapple Pager unter OpenWrt. Erfahre mehr über MIPS-Cross-Compilation, USB 2.0-Stromgrenzen und Modulkonfigurationen."
date: 2026-06-19
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi Pineapple Pager", "ALFA Network", "AWUS036ACM", "AWUS036ACH", "compatibility", "wireless-security"]
featureimage: "/images/blog/hak5-wifi-pineapple-pager-alfa-compatibility.webp"
faq:
  - question: "Kann der HAK5 WiFi Pineapple Pager eine externe ALFA-Netzwerkkarte verwenden?"
    answer: "Ja, jedoch sind die Einschränkungen der MIPS-Architektur und die USB 2.0-Stromversorgung zu beachten. Der AWUS036ACM ist die erste Wahl, da der im Kernel integrierte Treiber am stabilsten ist."
  - question: "Warum benötigt der Pager ein externes USB-Hub mit Stromversorgung?"
    answer: "Der Pager verfügt nur über USB 2.0-Schnittstellen mit einer maximalen Ausgabe von 500 mA. Hochleistungs-ALFA-Netzwerkkarten erreichen Spitzenwerte von bis zu 720 mA. Ein direkter Anschluss kann zu Neustarts oder Kernel-Panics führen."
  - question: "Warum ist der AWUS036ACM die erste Wahl für den Pager?"
    answer: "Der MT7612U-Treiber ist im OpenWrt 6.6-Kernel integriert. Auf dem Pager kann er direkt über opkg installiert werden, ohne Cross-Kompilierung, was ihn am stabilsten und zuverlässigsten macht."
  - question: "Welche Einschränkungen gibt es bei der Treiberinstallation auf der MIPS-Architektur?"
    answer: "Der Pager basiert auf dem MIPS32-basierten MT7628AN, unterstützt kein DKMS und verfügt über keine GCC-Toolchain. Nicht im Kernel integrierte Treiber müssen auf einem externen x86-Host cross-kompiliert werden."
  - question: "Welche bekannten Probleme gibt es mit dem RTL8812AU-Treiber auf dem Pager?"
    answer: "Auf der MIPS-Plattform liegt ein Kernfehler in wiphy_register für den RTL8812AU vor, der dazu führt, dass die Schnittstelle nicht geladen werden kann. Es ist erforderlich, einen Community-Patch anzuwenden. Wir empfehlen stattdessen die Verwendung des AWUS036ACM."
---
Bevor du eine leistungsstarke USB-WLAN-Karte an den HAK5 Pager anschließt, solltest du zwei wesentliche Hürden verstehen: die CPU-Architektur und das Strombudget des USB-Ports.

# HAK5 WiFi Pineapple Pager × ALFA Network: Kompatibilitätsleitfaden für externe USB-WLAN-Adapter

{{< tldr >}}
Der Pager verwendet MIPS-Architektur und unterstützt kein DKMS. Der AWUS036ACM ist dank des im OpenWrt 6.6-Kernel integrierten MT7612U-Treibers Plug-and-Play-fähig. Für den AWUS036ACH ist eine Cross-Kompilierung erforderlich, zudem besteht ein wiphy-Bug. Die USB 2.0-Stromversorgung liefert nur 500 mA, weshalb ein externes Hub benötigt wird.
{{< /tldr >}}

Der HAK5 WiFi Pineapple Pager lässt sich mit externen ALFA-Adaptern erweitern. Erste Wahl ist der AWUS036ACM mit In-Kernel-Treiber für maximale Stabilität; leistungsstarke Adapter erfordern einen aktiv gespeisten USB-Hub, um Kernel-Abstürze zu vermeiden.

Die Überprüfung der WLAN-Sicherheit (Penetration Testing) erfordert höchste Präzision, Vielseitigkeit und die passende Hardware. Der **HAK5 WiFi Pineapple Pager** hat als ultrakompaktes Handheld-Sicherheitswerkzeug mit der leistungsstarken **PineAP v8** Engine das Interesse von IT-Sicherheitsexperten geweckt.

Doch um die Reichweite der Audits zu maximieren, Dualband-Scans (2,4 GHz & 5 GHz) durchzuführen oder passives Multikanal-Monitoring ohne Unterbrechung der internen Funkmodule des Pineapples zu betreiben, stellen sich viele Experten die Frage: **Kann ich eine externe ALFA Network WLAN-Karte an den HAK5 Pager anschließen?**

Die kurze Antwort lautet: **Ja – aber mit wichtigen technischen Einschränkungen bei Hardware und Software**.

In diesem umfassenden Leitfaden analysieren wir die technischen Hürden (wie die CPU-Architektur und die Stromversorgung des USB-Ports), bewerten die Kompatibilität der aktuellen ALFA-Adapter und zeigen dir eine Schritt-für-Schritt-Anleitung für die CLI-Installation und Fehlerbehebung.

---

## 1. Technische Einschränkungen: Was du wissen musst

### 1.1 CPU-Architektur: Die MIPS-Einschränkung
Im Gegensatz zu einem typischen Kali-Linux-PC mit x86_64-Architektur oder einem Raspberry Pi mit ARM-Prozessor basiert der HAK5 Pager auf dem **MediaTek MT7628AN SoC** (einem **MIPS32r2, Little-Endian** Core, der unter OpenWrt als `mipsel_24kc`-Plattform kompiliert wird).

> [!IMPORTANT]
> Da das Pager OS auf **OpenWrt (Version 24.10.1, Kernel 6.6.86)** basiert, **unterstützt es kein DKMS** (Dynamic Kernel Module Support). Du kannst Treiber-Quellcode nicht direkt auf dem Pager kompilieren, da dem System Compiler-Werkzeuge wie GCC und Make fehlen. Jeder externe Treiber muss auf einem externen Linux-System (x86_64) mittels OpenWrt SDK kreuzkompiliert (cross-compiled) werden.

### 1.2 USB 2.0-Strombudget: Spannungsabfall
Der HAK5 Pager verfügt über einen einzigen USB 2.0-Host-Port. Nach den offiziellen USB 2.0-Spezifikationen kann ein Standard-Port maximal **500 mA bei 5V (2,5W)** liefern.

Leistungsstarke WLAN-Adapter wie der ALFA AWUS036ACH (RTL8812AU) oder der AWUS036AXML (MT7921AUN) benötigen unter Last (z. B. bei der Paketinjektion oder intensiven Netzwerkscans) bis zu **720 mA (3,6W)**.

> [!WARNING]
> Schließt du einen solchen Hochleistungs-Adapter direkt an den USB-Port des Pagers an, kommt es zu einem Spannungsabfall. Dies führt zu **Geräteneustarts, Kernel-Panics oder plötzlichen Verbindungsabbrüchen der WLAN-Karte**. Für einen stabilen Betrieb **musst** du den ALFA-Adapter über einen **aktiven USB-Hub mit externer Stromversorgung (mindestens 5V/2A)** anschließen.

---

## 2. Kompatibilitätsmatrix der ALFA-Adapter

Die folgende Tabelle zeigt die Kompatibilität aktueller ALFA Network USB-Adapter mit dem HAK5 Pager unter Pager OS (Kernel 6.6):

| ALFA-Modell | Chipsatz | Frequenzbänder | USB-Stromaufnahme | Status unter Kernel 6.6 | Installationsmethode | Monitor- & Injektionsmodus | Bewertung & Empfehlung |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AWUS036ACM** | MediaTek **MT7612U** | 2,4 GHz / 5 GHz | ~600 mA (Hub benötigt) | **Nativ im Kernel (In-Kernel)** | Installation via `opkg` | ✅ Ja / ✅ Ja | 🏆 **Goldstandard / Beste Wahl** |
| **AWUS036ACH** | Realtek **RTL8812AU** | 2,4 GHz / 5 GHz | ~720 mA (Aktiver Hub nötig) | Out-of-Kernel | Cross-Compilation via SDK | ✅ Ja / ✅ Ja | ⭐⭐ **Nur für Fortgeschrittene** (MIPS wiphy-Bug vorhanden) |
| **AWUS036AXML** | MediaTek **MT7921AUN** | 2,4 / 5 / 6 GHz (Wi-Fi 6E) | ~720 mA (Aktiver Hub nötig) | **Nativ im Kernel (In-Kernel)** | Installation via `opkg` + manuelle Firmware | ✅ Ja / ✅ Ja | ⭐⭐⭐ **Großes Potenzial**, aber hoher Verbrauch |
| **AWUS036ACHM** | MediaTek **MT7610U** | 2,4 GHz / 5 GHz | ~400 mA (Direktstrom möglich) | Teilweise im Kernel | Installation via `opkg` | ✅ Ja / ✅ Ja | ⭐⭐⭐ **Gute Budget-Option** |
| **AWUS036ACS** | Realtek **RTL8811AU** | 2,4 GHz / 5 GHz | ~500 mA (Grenzwertig) | Out-of-Kernel | Cross-Compilation via SDK | ✅ Ja / ✅ Ja | ⭐⭐ **Mittelmäßig** (Treiber-Kompilierung nötig) |
| **AWUS036EACS** | Realtek **RTL8821CU** | 2,4 GHz / 5 GHz | ~500 mA | Out-of-Kernel | Nicht empfohlen | ❌ **Kein Monitor-Modus** | ❌ **Inkompatibel / Nicht nutzen** |

---

## 3. Schritt-für-Schritt-Installationsanleitung

Hier findest du die genauen CLI-Befehle zur Einrichtung der empfohlenen WLAN-Adapter.

### 3.1 Szenario A: AWUS036ACM (MT7612U) — Plug & Play (Empfohlen)

Der **AWUS036ACM** ist die beste Wahl für den HAK5 Pager. Die MediaTek `mt76`-Treiberfamilie ist bereits nativ in das Linux-Kernel 6.6 integriert, sodass kein Compiler-Vorgang erforderlich ist.

#### Schritt 1: Hardware verbinden
1. Schließe den aktiven USB-Hub an den USB-Port des HAK5 Pagers an.
2. Stecke den AWUS036ACM in den Hub.
3. Verbinde dich per SSH mit dem Pager:
   ```bash
   ssh root@172.16.42.1
   ```

#### Schritt 2: Geräteerkennung prüfen
Führe `lsusb` aus, um sicherzustellen, dass das System den MediaTek-Chipsatz erkennt:
```bash
lsusb
# Die Ausgabe sollte folgende Zeile enthalten:
# Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

#### Schritt 3: Kernel-Module über opkg installieren
Aktualisiere die Paketlisten und installiere die notwendigen Module für den MT76 USB-Treiber:
```bash
opkg update
opkg install kmod-mt76x2u kmod-mt76-usb firmware-utils
```

#### Schritt 4: Behebung des USB Scatter-Gather-Absturzes auf MIPS-Systemen
Auf MIPS-basierten OpenWrt-Routern kann der `mt76-usb`-Treiber beim Laden der Firmware abstürzen, wenn USB Scatter-Gather (USB SG) aktiviert ist (führt zu Fehler `-110`).

> [!TIP]
> Um eine stabile Verbindung zu garantieren und Firmware-Ladefehler zu vermeiden, solltest du USB Scatter-Gather über Kernel-Modulparameter deaktivieren.

Erstelle die Datei `/etc/modules.d/mt76-usb-sg` und trage den Deaktivierungsparameter ein:
```bash
echo "mt76-usb disable_usb_sg=1" > /etc/modules.d/mt76-usb-sg
```
Starte den HAK5 Pager neu, um die Änderungen zu übernehmen:
```bash
reboot
```

#### Schritt 5: Monitor-Modus und Paketinjektion überprüfen
Verbinde dich nach dem Neustart wieder per SSH und führe aus:
```bash
iw dev
# Suche nach dem neuen WLAN-Interface (z. B. wlan2)
```

So aktivierst du den Monitor-Modus:
```bash
ip link set wlan2 down
iw dev wlan2 set monitor none
ip link set wlan2 up
```
Überprüfe den Status des Interfaces:
```bash
iw dev wlan2 info
# Die Ausgabe sollte enthalten: "type monitor"
```

---

### 3.2 Szenario B: AWUS036ACH (RTL8812AU) — Manuelle SDK-Kompilierung

Der **AWUS036ACH** bietet unter Kali Linux hervorragende Sende- und Empfangseigenschaften, wird jedoch im OpenWrt Kernel 6.6 nicht nativ unterstützt. Eine Cross-Compilation ist erforderlich.

#### Voraussetzungen
- Ein Linux-System mit Ubuntu 22.04 oder Debian 12 (x86_64) für die Kompilierung.
- Das passende OpenWrt SDK für das Ziel `ramips/mt76x8` (passend zum Pager-Prozessor).

#### Schritt 1: OpenWrt SDK auf dem Build-System herunterladen
Auf deinem Ubuntu-Kompilierungssystem:
```bash
wget https://downloads.openwrt.org/releases/24.10.1/targets/ramips/mt76x8/openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
tar --zstd -xf openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
cd openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64
```

#### Schritt 2: Quellcode des rtl8812au-Treibers hinzufügen
```bash
git clone https://github.com/aircrack-ng/rtl8812au.git package/kernel/rtl8812au
./scripts/feeds update -a
./scripts/feeds install -a
```

#### Schritt 3: Modul konfigurieren und bauen
Öffne das SDK-Konfigurationsmenü und wähle den WLAN-Treiber aus:
```bash
make menuconfig
# Gehe zu: Kernel modules -> Wireless Drivers -> Markiere kmod-rtl8812au
```
Starte den Kompilierungsvorgang:
```bash
make package/kernel/rtl8812au/compile V=s
```

#### Schritt 4: Paket übertragen und installieren
Das fertige Installationspaket `.ipk` befindet sich im Verzeichnis `bin/packages/mipsel_24kc/`. Kopiere es auf den Pager:
```bash
scp bin/packages/mipsel_24kc/base/kmod-rtl8812au*.ipk root@172.16.42.1:/tmp/
ssh root@172.16.42.1 "opkg install /tmp/kmod-rtl8812au*.ipk"
```

> [!CAUTION]
> Auf MIPS-Architekturen kann der Out-of-Kernel-Treiber `rtl8812au` Fehler beim Geräteregistrierungsprozess (`wiphy_register`) verursachen, sodass die WLAN-Karte nicht im System auftaucht. Um dies zu lösen, musst du vor dem Bauen MIPS-spezifische Treiber-Patches anwenden. Wir raten dir daher dringend, stattdessen den **AWUS036ACM** zu verwenden.

---

## 4. Erweiterte Penetration-Testing-Möglichkeiten

Sobald du einen kompatiblen ALFA-Adapter an deinen HAK5 Pager anschließt, gewinnst du deutliche Vorteile für deine Sicherheitsaudits:

1. **Erweiterter Scan im 5 GHz-Band**: Da die internen Antennen des Pagers je nach Ausstattung eingeschränkt sein können, stellt ein externer Dualband-Adapter sicher, dass du WPA/WPA2-Handshakes abfangen und Probe-Anfragen auf den modernen 5-GHz-Frequenzen überwachen kannst.
2. **Dedizierter Angriffssender**: Nutze das interne Funkmodul des Pagers für Client-Täuschungen (Rogue AP / Evil Twin / KARMA-Angriffe) und konfiguriere die externe ALFA-WLAN-Karte (`wlan2`) parallel als stabilen Sender für Deauthentifizierungs-Pakete (Deauth).
3. **Optimierte PineAP-Integration**: Du kannst den externen Adapter direkt über die CLI oder die Weboberfläche als Hauptschnittstelle für PineAP deklarieren, was die Reaktionszeit und die Client-Übernahme bis zu 100-fach beschleunigt.

---

{{< faq >}}

## 5. Fazit & Empfehlungen

Die Kombination eines ALFA Network WLAN-Adapters mit dem HAK5 WiFi Pineapple Pager ermöglicht dir den Aufbau einer unauffälligen, extrem leistungsstarken mobilen Audit-Station. Beachte dabei die folgenden Punkte:

- **Für den schnellen, unkomplizierten Einsatz**: Kaufe den [ALFA AWUS036ACM](https://yupitek.com/de/products/alfa/awus036acm). Seine MediaTek-Treiber laufen unter dem OpenWrt-Kernel 6.6 absolut stabil und er ist sofort einsatzbereit.
- **Stabile Stromversorgung**: Verwende immer einen hochwertigen **aktiven USB-Hub**, um die volle Sendeleistung der Hochleistungskarten zu gewährleisten und Verbindungsabbrüche zu verhindern.

Bei weiteren technischen Fragen, Hardware-Bestellungen oder Anfragen zu maßgeschneiderten OpenWrt-Kompilierungen wende dich einfach an das **Yupitek-Support-Team**:

- 🌐 Offizielle Website: [www.yupitek.com](https://www.yupitek.com)
- 📧 Support-E-Mail: [sales@yupitek.com](mailto:sales@yupitek.com)
- 📞 Telefonnummer: +886-2-87325338
- 📍 Adresse: 1F., No. 72, Ln. 34, Fuyang St., Xinyi Dist., Taipei City, Taiwan

## Referenzen

1. [Hak5 Offizielle Dokumentation — WiFi Pineapple Produktdokumentation](https://documentation.hak5.org/)
2. [OpenWrt Offizielle Website — OpenWrt 24.10 Distribution](https://openwrt.org/)
3. [OpenWrt mt76 Treiber-Repository — GitHub](https://github.com/openwrt/mt76)
4. [aircrack-ng/rtl8812au — Community-Treiber GitHub-Repository](https://github.com/aircrack-ng/rtl8812au)
5. [ALFA Network Offizielle Website](https://www.alfa.com.tw/)
