---
title: "Wie wählt man den Linux-Treiber für das ALFA USB-Netzwerkadapter: MediaTek ohne Übersetzung versus Realtek mit Übersetzung?"
date: 2026-09-03
draft: false
slug: "alfa-usb-wifi-linux-driver-guide"
tags:
  - "ALFA"
  - "Linux-Driver"
  - "MediaTek"
  - "Realtek"
  - "in-kernel"
  - "out-of-tree"
  - "DKMS"
  - "mt76"
  - "rtl8812au"
categories:
  - "Hardware-Leitfaden"
description: "\"Yupitek ALFA USB 網卡技術文件，涵蓋6款機型（Mediatek、Realtek）\""
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

> **Technikunterstützungs-Dokument · 2026-09-03 Erste Version (gemäß blog-writing-rules.md v1.0 erstellt)**
> Beurteilungsmutter: In diesem technischen Dokument sind 6 Modelle der aktiven Yupitek ALFA USB Netzwerkkarten (3 MediaTek, 3 Realtek) enthalten.
> Verwandte Artikel: [Ist die ALFA WLAN-Karte kompatibel mit NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[Ist die ALFA WLAN-Karte kompatibel mit OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)｜[Ist die ALFA WLAN-Karte kompatibel mit NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)｜[Ist die ALFA WLAN-Karte kompatibel mit Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[Ist die ALFA WLAN-Karte kompatibel mit DD-WRT](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)

## Einleitung

**Von den 6 aufgelisteten Modellen verwenden 3 MediaTek-Chips (MT7610U / MT7612U / MT7921AUN) bereits integrierte Treiber im modernen Kernel und sind sofort einsatzbereit; bei den 3 Realtek-Chips (RTL8812AU / RTL8811CU / RTL8832BU) ist stets eine manuelle Übersetzung des out-of-tree-Treibers erforderlich.** Möchten Sie es einfacher haben? Schauen Sie sich erst das Chipmodell an, bevor Sie bestellen.

---

## Akt I: Szene - Warum funktioniert es für manche sofort und bei anderen dauert es zwei Stunden

Zwei reale Szenarien:

- Kunde A steckt das **AWUS036ACM** in einen Ubuntu-Desktop und führt `lsusb` aus, dann erscheint NetworkManager mit wlan0 - ohne dass irgendetwas installiert wurde.
- Kunde B steckt das **AWUS036ACH** in denselben Rechner und die Netzwerkkarte reagiert nicht, es muss auf GitHub das Originalcode gezogen, Build-Tools installiert, kompiliert und der Rechner neu gestartet werden.

Der Unterschied liegt nicht am Glück oder der Linux-Distribution, sondern daran, **zu welchem Lager das Chipset gehört**: Die MediaTek USB WiFi-Chipset-Treiber (mt76-Serie) sind bereits im Linux-Kernel Mainline integriert; die hochwertigen USB WiFi-Chipset-Treiber von Realtek sind jedoch immer noch in Form von out-of-tree (außerhalb des Kerns) verbreitet und müssen über ein von der Community gepflegtes Treiber-Repo manuell installiert werden.

## Zweiter Akt: Mechanismen – Was ist der Unterschied zwischen in-kernel und out-of-tree?

### MediaTek: mt76 Haupttreiber, einfach zu verwenden

Der MediaTek USB-Chip-Treiber wird durch den Kernel-Subsystem **mt76** abgedeckt:

| Modell | Chipset | Kernel-Treibermodul | Ohne Übersetzungsvoraussetzungen |
|---|---|---|---|
| AWUS036ACHM | MT7610U | mt76x0u | Kernel-integriert, keine Versionsbarriere |
| AWUS036ACM | MT7612U | mt76x2u | Kernel-integriert, keine Versionsbarriere |
| AWUS036AXML / AXM | MT7921AUN | mt7921u | **Benötigt Kernel 5.19+** |

⚠️ Einziger Haken: **Der Kernel-Schwellenwert für MT7921AUN ist 5.19+**. Alte Plattformen (wie Jetson Nano mit JetPack 4.x, Kernel 4.9) können nicht backported und sind direkt nicht verwendbar – das ist ein von uns in der technischen Dokumentation für Jetson Nano bestätigtes Ergebnis (siehe [Ist das ALFA WLAN-Modul kompatibel mit NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/) §7.4).

### Realtek: out-of-tree, immer manuell übersetzt

Realtek USB-Chips haben keine verfügbaren Mainline-Treiber und sind auf von der Community gepflegte Treiber-Repo angewiesen. Der derzeit aktivste Betreuer ist **morrownr**, und in dieser Übersicht sind 3 Chips mit 3 Repo's abgedeckt:

| Modell | Chipset | Treiber-Repo (morrownr betreut) | Überprüfung am 03.09.2026 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | [8812au-20210820](https://github.com/morrownr/8812au-20210820) | ✅ Überprüft |
| AWUS036EACS | RTL8811CU | [8821cu-20210916](https://github.com/morrownr/8821cu-20210916) | ✅ Überprüft |
| AWUS036AX / AXER | RTL8832BU | [rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | ✅ Überprüft |

### Anwendungen in drei typischen Umgebungen

| Umgebung | Kernel | MediaTek-Lager (3 Modelle) | Realtek-Lager (3 Modelle) |
|---|---|---|---|
| GB10 / DGX Spark-ähnliche Plattformen | 6.x + aarch64 | Alle verfügbar (mt76 integriert) | Alle müssen übersetzt werden (ARM64 möglich) |
| Jetson Nano (JetPack 4.x) | 4.9 | 7610U/7612U verfügbar; MT7921AUN **nicht verfügbar** | 8812au kann übersetzt werden (ARM64 unterstützt); andere nicht überprüft |
| OpenWrt-Router | Ab Version | Alle verfügbar (MT7921AUN benötigt 23.05+) | Erforderlich, kmod oder Übersetzung, schwierig |

(Detaillierte Bewertungsmatrizen für jede Umgebung sind unter [Ist das ALFA WLAN-Modul kompatibel mit NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)、[Ist das ALFA WLAN-Modul kompatibel mit NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)、[Ist das ALFA WLAN-Modul kompatibel mit OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) zu finden.)

## Dritter Akt: Werkzeugkiste – Dreiminutenschema zur Bewertung und Installationsanleitung

### Bewertungsübersicht: Wenn du eine Netzwerkkarte hast, mache diese drei Schritte

```bash
# Schritt 1: Überprüfe, ob das System die Netzwerkkarte erkennt (notiere VID:PID)
lsusb

# Schritt 2: Überprüfe, ob der Kernel den passenden Treiber geladen hat
lsmod | grep -E "mt76|rtl8"

# Schritt 3: Überprüfe die Kernel-Version (entscheidet, ob MT7921AUN verwendet werden kann)
uname -r
```

Bewertungslogik (Hauptkörper: Tabelle mit 6 Modellen):

1. `lsusb` zeigt **MediaTek / MT76xx** → in-kernel-Lager, Kernel ≥ 5.19 (MT7921AUN-Modelle) oder jeder moderne Kernel, sofort einsatzbereit.
2. `lsusb` zeigt **Realtek RTL88xx** → out-of-tree-Lager, folge den nachfolgenden Installationsanleitungen.
3. `lsusb` zeigt **keine** neuen Geräte → wechseln Sie den USB-Port/Stecker, um Hardwareprobleme auszuschließen, und überprüfen Sie, ob das Modell Wi-Fi 6 ist (RTL8832BU, einige Chargen benötigen `usb_modeswitch`, dieser Schritt gehört zu den individuellen Modellproblemen und wird hier nicht weiter erörtert).

### Allgemeine Installation für das Realtek-Lager (Beispiel: AWUS036ACH)

```bash
# Schritt 1: Installiere die Übersetzungabhängigkeiten (Debian/Ubuntu)
sudo apt install build-essential dkms linux-headers-$(uname -r)

# Schritt 2: Hol dir den Treiber-Quellcode (Modellbezogene Repo siehe Tabelle)
git clone https://github.com/morrownr/8812au-20210820
cd 8812au-20210820

# Schritt 3: Installiere (DKMS registrieren, Kernel-Wechsel erfordert keine Neuinstallation)
sudo ./install-driver.sh

# Schritt 4: Nach dem Neustart überprüfen
lsmod | grep 88XXau
ip link   # Sollte eine neue wlan-Schnittstelle auftauchen
```

> **Tabelle 1 Schlussfolgerung: Bewertung vor Installation – Schau dir das Chipset an, 90 Sekunden entscheiden, ob du „einfach einstecken und betreiben“ oder „in den Repo übersetzen“ musst, ohne erst gegen die Wand zu rennen.**

### Kaufempfehlung (Schlussfolgerung)

- **Ohne Übersetzung**: Wähle das MediaTek-Lager (AWUS036ACHM / ACM / AXML), moderne Kernel sind alle sofort einsatzbereit.
- **Wi-Fi 6 und ohne Übersetzung**: Wähle AWUS036AXML (MT7921AUN), aber überprüfe vorher, ob der Kernel ≥ 5.19 ist.
- **Spezielle Anforderungen, die nur Realtek erlauben** (z.B. spezifische Monitor-Modus-Toolchains): Reserviere 20–40 Minuten für die Treiberübersetzung und überprüfe, ob die Zielplattform Kernel-Header hat.

## Bekannte Einschränkungen und Einwände

Die Schlussfolgerungen dieses Artikels sind unter folgenden Bedingungen **nicht gültig**, bitte wählen Sie alternative Lösungen:

1. **Kernel 5.19 und älter + MT7921AUN**: mt7921u kann nicht backportiert werden (abhängig von modernen Kernel-Infrastrukturen), die Schlussfolgerung wird umgedreht in "nicht verfügbar". Dies ist die wichtigste Ausnahme in diesem Artikel.
2. **Kein x86/ARM64 Linux** (z.B. einige MIPS-Router): Der morrownr-Repository ist nicht garantiert kompilierbar, bitte priorisieren Sie die kmod von OpenWrt (siehe [Ist das ALFA-WLAN-Modul kompatibel mit OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)).
3. **Repository-Versionen der Treiber**: Der morrownr-Repository wird nach Datum benannt (z.B. rtl8852bu-20250826), es kann zu zukünftigen Änderungen oder Entfernungen kommen; Bitte stellen Sie vor der Installation den aktuellen Repository-Zustand sicher.
4. **Monitor-Modus / AP-Modus-Fähigkeiten**: Unterschiedliche Fähigkeiten von Chips mit verschiedenen Kernel-Versionen (z.B. rtl8812au-ct in OpenWrt 22.03+ hat in 24.10 Crash-Berichte), detaillierte Fähigkeitsmatrizen bitte in spezifischen Umgebungsartikeln überprüfen.
5. **RTL8832BU (AWUS036AX/AXER) ist nicht in den in diesem Artikel genannten 6 Modellen enthalten, aber der Kundenservice wird oft damit in Verbindung gebracht**: Der Treiberpfleger morrownr hat öffentlich erklärt, dass die Chip-Serie "sehr schlechte Treiber sind und es wird vermutet, dass das Chip selbst defekt ist", Linux-Nutzer sollten derzeit davon absehen, nicht nur wegen der "Notwendigkeit der Kompilierung" der Schwierigkeiten, bei der Beantwortung von Kundenanfragen sollten Sie dies ehrlich erklären.

## Referenzquellen

| Quelle | Beschreibung | URL | Überprüfungsstatus | Überprüfungsdatum |
|---|---|---|---|---|
| morrownr/8812au GitHub | RTL8812AU Linux-Treiber | https://github.com/morrownr/8812au-20210820 | ✅ Geprüft | 03.09.2026 |
| morrownr/8821cu GitHub | RTL8811CU Linux-Treiber | https://github.com/morrownr/8821cu-20210916 | ✅ Geprüft | 03.09.2026 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux-Treiber | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Geprüft | 03.09.2026 |
| Yupitek ALFA Produktübersicht | Aktuelle Modelle und Spezifikationen | https://yupitek.com/zh-tw/products/alfa/ | ✅ Geprüft | 03.09.2026 |
| Yupitek Blog: Soft AP Anleitung | AP-Modus Implementierung und Validierung | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Geprüft | 03.09.2026 |
| Diese Website Technische Dokumentation 9 Artikel | Bestimmungsmatrix und Umgebungsvalidierung | Relative Verknüpfungen (siehe Artikelkopf „Verwandte Artikel“) | ✅ Geprüft | 03.09.2026 |

> Kernel mt76 offizielle Wiki-Seite: https://wireless.wiki.kernel.org/en/users/drivers/mediatek （Geprüft, zeigt die unterstützte Chip-Start-Kernel-Version an, kann als schnelle Überprüfung dienen）

## Haftungsausschluss

Dieser Dokument wurde von Yupitek Ltd. technisch aufbereitet und kann aufgrund von Updates des Kernels und der Treiber-Repositorys in Bezug auf Spezifikationen und Treiberstatus variieren. Bitte stellen Sie sicher, dass Sie vor der Installation die offiziellen Repositorys und die Originalhersteller-Spezifikationsseiten verwenden. ALFA Network ist eine offiziell von uns autorisierte Vertriebsmarke.
