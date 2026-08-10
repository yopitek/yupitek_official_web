---
title: "ALFA WLAN-Adapter mit Kali NetHunter: Vollständiger Technischer Leitfaden 2026"
description: "Technische Referenz für ALFA USB WLAN-Adapter mit Kali NetHunter. Smartphone-Kompatibilität für den taiwanesischen Markt, In-Kernel vs DKMS Treiberanalyse, OTG-Einrichtung und verifizierte Testergebnisse."
date: 2026-06-09
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
featureimage: /images/blog/alfa-nethunter-technical-guide-hero.png
tags: ["nethunter", "kali-linux", "alfa-network", "wireless-security", "android", "usb-otg", "monitor-mode", "packet-injection", "mt7610u", "mt7612u", "rtl8812au"]
faq:
  - question: "Welche Smartphone-Voraussetzungen sind für die Kombination von ALFA-WLAN-Netzwerkkarten mit Kali NetHunter erforderlich?"
    answer: "Es wird ein Android-Smartphone mit OTG-Unterstützung benötigt, das gerootet ist und einen Kali NetHunter-Kernel installiert hat. Zu den verifizierten kompatiblen Modellen gehören die Google Pixel-Serie und ältere OnePlus-Flaggschiffmodelle. Die spezifische Kompatibilität hängt von der Kernel-Version und der Position der Treiber für den Netzwerkkarten-Chipsatz ab."
  - question: "Was sind die Unterschiede zwischen den Treibern für MT7610U/MT7612U und RTL8812AU?"
    answer: "Die Treiber für MT7610U/MT7612U befinden sich im Kernel-Baum und sind nach dem Einstecken sofort einsatzbereit, ohne Kompilierung; für RTL8812AU muss der externe Treiber über DKMS kompiliert und installiert werden, und nach Kernel-Updates ist möglicherweise eine Neukompilierung erforderlich. Für den Einsatz in der IT-Sicherheit bietet der im Kernel-Baum integrierte Treiber eine höhere Stabilität."
  - question: "Werden ALFA-Netzwerkkarten auf NetHunter für den Monitor Mode unterstützt?"
    answer: "Ja, MT7610U/MT7612U unterstützen Monitor Mode und Packet Injection. RTL8812AU wird ebenfalls unterstützt, solange der Kernel < 6.12 ist; ab Kernel 6.12 ist die Unterstützung für Monitor Mode jedoch eingeschränkt. Für Sicherheitsforschungen wird vorrangig die Verwendung von MT7610U/MT7612U-Netzwerkkarten empfohlen."
---

Wenn du bereits einen ALFA-Adapter mit NetHunter über die grundlegenden OTG-Anweisungen eingerichtet hast und die Kurzanleitung suchst, deckt unser [OTG-Einrichtungsleitfaden](/de/blog/alfa-adapter-nethunter-android-otg/) die wesentlichen Punkte ab. Dieser Artikel geht tiefer — er ist eine vollständige technische Referenz für Sicherheitsexperten, die vor dem Hardwarekauf die Telefon- und Adapterkompatibilität bewerten müssen, verstehen wollen, welcher Treiberansatz über Kernel-Updates hinweg funktionsfähig bleibt, und verifizierte Testergebnisse einsehen möchten, bevor sie sich für eine bestimmte Kombination entscheiden.

{{< tldr >}}
Der nativen Plug-and-Play-Treiber für MT7610U/MT7612U; für RTL8812AU ist die Kompilierung über DKMS erforderlich. NetHunter-Handys benötigen Root-Zugriff und OTG-Unterstützung; zur Vermeidung von Treiberproblemen wird vorrangig eine MT7612U-Netzwerkkarte empfohlen.
{{< /tldr >}}

Wir konzentrieren uns auf eine Frage, die die meisten NetHunter-Anleitungen auslassen: **Welcher Adapter ist wirklich Plug-and-Play, und welcher schickt dich im ungünstigsten Moment in die Treiberkompilierungs-Hölle?** Die Antwort hängt vom Chipsatz, der Kernel-Version des Telefons und davon ab, ob der Treiber innerhalb des Kernel-Baums ausgeliefert wird oder in einem externen DKMS-Repository liegt. Wenn du das falsch einschätzt, liegt dein Adapter im Rucksack, während du im Feld auf `modprobe`-Fehler starrst. Wenn du es richtig machst, steckst du ihn ein und beginnst mit dem Scannen.

---

## 1. Kundenanforderungen

### 1.1 Anwendungsfall

Mobile Penetrationstester benötigen ein Setup, das den Laptop vollständig ersetzt. Das Telefon führt Kali NetHunter aus, der ALFA-Adapter wird per USB-OTG verbunden, und der Bediener führt Wi-Fi-Sicherheitsbewertungen ohne Notebook durch. Der Kern-Workflow — Site Survey, Monitor-Mode-Erfassung, Packet Injection, WPA-Handshake-Sammlung — muss zuverlässig im Akkubetrieb funktionieren.

### 1.2 Kernanforderungen

| Anforderung | Detail |
|---|---|
| Plattform | Android-Telefon mit Kali NetHunter (Full Edition, Custom Kernel) |
| Verbindung | USB-OTG-Kabel oder powered OTG-Hub |
| Adapter | ALFA USB WLAN-Adapter mit Monitor Mode und Packet Injection Unterstützung |
| Treiberansatz | In-Kernel-Chipsätze (treiberlos) priorisieren, um Kompilierungsabhängigkeiten zu vermeiden |
| Taiwan-Markt | Telefone müssen offiziell in Taiwan erhältlich sein, Modelle von 2024–2026 |
| Stromversorgung | Akkubetrieb; powered OTG-Hub wird für den Dauerbetrieb dringend empfohlen |

---

## 2. Ziel-Hardware- & Softwareanalyse

### 2.1 NetHunter-kompatible Telefone in Taiwan erhältlich

NetHunter unterstützt über 117 Gerätemodule, aber die meisten sind ältere Modelle. Nach Filterung auf Geräte, die (a) offiziell in Taiwan erhältlich sind, (b) aus 2024 oder später stammen und (c) funktionierende NetHunter-Custom-Kernel haben, stechen drei Telefone hervor:

| Modell | Codename | CPU | Kernel-Versionen | Vorgefertigte Images | Taiwan-Verfügbarkeit |
|---|---|---|---|---|---|
| **OnePlus 11 5G** | salami | Snapdragon 8 Gen 2 (ARM64) | 2 | 2 | ✅ Über Importkanäle erhältlich, Launch 2023 |
| **Nothing Phone (1)** | spacewar | Snapdragon 778G+ (ARM64) | 3 | 1 | ✅ Offiziell in Taiwan eingeführt, aktive Community |
| **Samsung Galaxy S20 FE 5G** | r8q | Snapdragon 865 (ARM64) | 5 | 1 | ✅ In Taiwan verkauft — **Snapdragon-Variante erforderlich** |

{{< alert "triangle-exclamation" >}}
**Samsung Exynos-Warnung:** Die meisten Samsung-Geräte, die über taiwanesische Mobilfunkanbieter verkauft werden, verwenden Exynos-Chipsätze. NetHunter-Kernel unterstützen nur die Snapdragon-Variante (`r8q`). Überprüfe vor dem Kauf eines Samsung-Geräts für NetHunter das CPU-Modell — wenn in der Beschreibung „Exynos" steht, wird es nicht funktionieren. Importiere ein Snapdragon-Gerät oder wähle stattdessen das OnePlus 11.
{{< /alert >}}

**NetHunter Rootless** läuft auf jedem Android-Gerät ohne Root, kann aber keine externen USB-WLAN-Adapter für den Monitor Mode unterstützen. Wenn du Packet Capture und Injection benötigst, brauchst du die NetHunter Full Edition mit einem Custom Kernel.

### 2.2 Technische Plattformspezifikationen

Mit dem OnePlus 11 5G als Referenzplattform:

| Parameter | Spezifikation |
|---|---|
| CPU-Architektur | ARM64 (aarch64) |
| SoC | Qualcomm Snapdragon 8 Gen 2 (SM8550) |
| USB-Controller | USB 3.1 Gen 1 mit OTG-Unterstützung |
| USB Power Delivery | 5V / 900mA (verwende einen powered OTG-Hub für dauerhaften Adapterbetrieb) |

### 2.3 Softwareumgebung

| Komponente | Anforderung | Empfohlene Version |
|---|---|---|
| Host-OS | Android mit Kali-Chroot | Android 11+ |
| NetHunter | Full Edition (Custom Kernel) | 2024.4 (neueste stabile Version) |
| Linux-Kernel | Gerätespezifischer Custom Kernel | 5.x oder höher bevorzugt |
| Vorinstallierte Treiber | Siehe Abschnitt 4 für die Matrix | — |
| DKMS | Nur für RTL8812AU-basierte Adapter erforderlich | Kernel-Header müssen übereinstimmen |
| Wireless-Tools | aircrack-ng, Kismet, MANA Toolkit | Im NetHunter-Chroot enthalten |
| Root | Für volle Funktionalität erforderlich | Magisk 26.0+ |

---

## 3. ALFA-Adapter-Spezifikationen & Treiberquellen

### 3.1 AWUS036ACHM — Top-Empfehlung für NetHunter

| Parameter | Spezifikation |
|---|---|
| Chipsatz | **MediaTek MT7610U** |
| USB VID/PID | `0x0e8d:0x7610` |
| Bänder | 2,4 GHz + 5 GHz (AC433) |
| Max. Datenrate | 150 Mbps (2,4 GHz) / 433 Mbps (5 GHz) |
| USB | USB 2.0 |
| Monitor Mode | ✅ Vollständige Unterstützung |
| Packet Injection | ✅ Vollständige Unterstützung |
| Antenne | 1× abnehmbare High-Gain-Antenne (RP-SMA) |
| Treiber | **In-Kernel** — keine Installation erforderlich |
| Kernel-Modul | `mt76x0u` |
| Kernel-Anforderung | Linux 4.19+ |
| Produktseite | [/de/products/alfa/awus036achm/](/de/products/alfa/awus036achm/) |

Der MT7610U-Chipsatz wird von der Kali- und NetHunter-Community breit empfohlen, weil sein `mt76x0u`-Treiber seit Version 4.19 im Mainline-Linux-Kernel enthalten ist. Du steckst ihn ein, der Kernel erkennt ihn und du kannst loslegen. Keine Kompilierungstoolchain, keine Kernel-Header, kein DKMS — einfach `lsusb`-Bestätigung, gefolgt von `airmon-ng start`.

### 3.2 AWUS036ACM — Leistungsstarke Alternative

| Parameter | Spezifikation |
|---|---|
| Chipsatz | **MediaTek MT7612U** |
| USB VID/PID | `0x0e8d:0x7612` |
| Bänder | 2,4 GHz + 5 GHz (AC1200) |
| Max. Datenrate | 300 Mbps (2,4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| Monitor Mode | ✅ Vollständige Unterstützung |
| Packet Injection | ✅ Stabil bestätigt auf Kali 2024.3 / 2025.1 |
| Antenne | 2× Dual-Antennen (RP-SMA), MIMO 2T2R |
| Treiber | **In-Kernel** — keine Installation erforderlich |
| Kernel-Modul | `mt76x2u` |
| Kernel-Anforderung | Linux 4.19+ |
| Produktseite | [/de/products/alfa/awus036acm/](/de/products/alfa/awus036acm/) |

Der ACM bietet AC1200 Dual-Band mit MIMO 2T2R und USB-3.0-Durchsatz. Der `mt76x2u`-Treiber ist ebenfalls seit Kernel 4.19 im Mainline. Ein Vorbehalt: Einige ältere NetHunter-Custom-Kernel (insbesondere der OnePlus-7T-Kernel bei Version 4.14) wurden ohne das `mt76x2u`-Modul kompiliert. Bei jedem Kernel 4.19 oder höher ist das kein Problem, aber überprüfe mit `lsmod | grep mt76x2u`, falls dein Gerät einen älteren Kernel-Build verwendet.

### 3.3 AWUS036ACH — Größte Community-Unterstützung

| Parameter | Spezifikation |
|---|---|
| Chipsatz | **Realtek RTL8812AU** |
| USB VID/PID | `0x0bda:0x8812` |
| Bänder | 2,4 GHz + 5 GHz (AC1200) |
| Max. Datenrate | 300 Mbps (2,4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| Monitor Mode | ✅ Vollständige Unterstützung |
| Packet Injection | ✅ Vollständige Unterstützung |
| Antenne | 2× 5dBi extern (RP-SMA) |
| Treiber | Externes DKMS (in den meisten NetHunter-Kernels vorkompiliert) |
| Kernel-Modul | `88XXau` |
| Treiber-Repo | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| Produktseite | [/de/products/alfa/awus036ach/](/de/products/alfa/awus036ach/) |

Der ACH ist seit Jahren der De-facto-Standard für Kali- und NetHunter-Setups. Die meisten NetHunter-Custom-Kernel liefern das `88XXau`-Modul vorkompiliert aus, sodass du normalerweise nicht aus dem Quellcode bauen musst. Falls deine Kernel-Version es jedoch nicht enthält, benötigst du eine funktionierende Kompilierungsumgebung mit passenden Kernel-Headern — genau die Art von Abhängigkeitskette, die die MT7610U- und MT7612U-Chipsätze vermeiden. Die dualen 5dBi-Antennen bieten die stärkste Signalreichweite im Sortiment, was für Long-Range-Capture-Szenarien relevant ist.

### 3.4 AWUS036ACS — Kompakte Bauform

| Parameter | Spezifikation |
|---|---|
| Chipsatz | Realtek RTL8811AU |
| USB VID/PID | `0x0bda:0x0811` |
| Bänder | 2,4 GHz + 5 GHz (AC433) |
| USB | USB 2.0 |
| Monitor Mode | ✅ Unterstützt (gleiche Treiberfamilie wie RTL8812AU) |
| Packet Injection | ✅ Unterstützt |
| Antenne | Intern, 55 mm ultraflaches Gehäuse |
| Leistungsaufnahme | ~300mW — niedrigste im Sortiment |
| Treiber | Extern (gemeinsames aircrack-ng-Repo mit RTL8812AU) |
| Produktseite | [/de/products/alfa/awus036acs/](/de/products/alfa/awus036acs/) |

Der ACS ist die portabelste Option. Mit 300mW Leistungsaufnahme belastet er den Telefonakku am wenigsten, und sein schlankes Gehäuse verschwindet in der Hosentasche. Der Kompromiss: Single-Stream-AC433-Leistung und die externe DKMS-Treiberabhängigkeit, die mit der RTL8812AU-Familie geteilt wird.

### 3.5 Für NetHunter nicht empfohlene Adapter

| Adapter | Chipsatz | Grund |
|---|---|---|
| AWUS036AX / AWUS036AXER | RTL8832BU | Erfordert Kernel 6.14+; Monitor-Mode-Stabilität auf Android-Kernels unbestätigt |
| AWUS036AXML / AWUS036AXM | MT7921AUN | WiFi-6E-/6-GHz-Unterstützung in aktuellen NetHunter-Kernel-Builds instabil; als primärer Pentest-Adapter nicht geeignet |

### 3.6 Treiberquellcode-Repositories

| Chipsatz | Treiber | Quelle |
|---|---|---|
| MT7610U | `mt76x0u` (In-Kernel) | [torvalds/linux — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| MT7612U | `mt76x2u` (In-Kernel) | Gleicher Kernel-Baum wie oben |
| RTL8812AU | `88XXau` (extern) | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| RTL8811AU | `88XXau` (extern, gemeinsam) | Gleiches aircrack-ng-Repository |

---

## 4. Treiberkompatibilitätsanalyse

### 4.1 In-Kernel vs. Externes DKMS

Die wichtigste Entscheidung bei der Auswahl eines Adapters für NetHunter ist, ob der Treiber innerhalb des Kernel-Baums liegt oder außerhalb. Hier ist der Grund:

| | In-Kernel (MT7610U, MT7612U) | Externes DKMS (RTL8812AU, RTL8811AU) |
|---|---|---|
| Plug-and-Play | ✅ Ja — wird beim Einstecken erkannt | ⚠️ Hängt davon ab, ob der Kernel `88XXau` vorkompiliert hat |
| Übersteht Kernel-Updates | ✅ Ja — Treiber ist Teil des Kernel-Builds | ❌ Kann nach Kernel-Update brechen; erfordert Neukompilierung |
| Benötigt linux-headers | ❌ Nein | ✅ Ja, falls manuelle Kompilierung erforderlich |
| Benötigt DKMS | ❌ Nein | ✅ Ja, falls nicht im Kernel vorkompiliert |
| Community-Dokumentation | Mittel | Umfangreich (ACH hat die meisten Tutorials) |
| Risiko von Feldausfällen | Gering | Mittel (Kompilierungsabhängigkeit) |

**Fazit:** Wenn du das geringstmögliche Risiko von Treiberproblemen im Feld haben möchtest, wähle einen MT7610U- oder MT7612U-Adapter. Der Treiber ist bereits im Kernel — es gibt nichts zu kompilieren, nichts, was bei einem Update kaputtgehen kann, und nichts, was du vor Ort troubleshooten musst.

### 4.2 NetHunter-Kernel-Modul-Unterstützungsmatrix

| Gerät | NetHunter-Kernel | MT7610U (`mt76x0u`) | MT7612U (`mt76x2u`) | RTL8812AU (`88XXau`) |
|---|---|---|---|---|
| OnePlus 11 5G | Android-13-Kernel | ✅ Unterstützt | ✅ Unterstützt | ✅ Unterstützt |
| Samsung S20 FE (Snapdragon) | Android-12-Kernel (4.19) | ✅ Unterstützt | ✅ Unterstützt | ✅ Unterstützt (XDA-Berichte prüfen) |
| Nothing Phone (1) | Android-12/13-Kernel | ✅ Unterstützt | Kernel-Konfiguration prüfen | ✅ Unterstützt |
| OnePlus 7/7T | 4.14 (älter) | ✅ Unterstützt | ⚠️ Könnte im Build fehlen | ✅ Unterstützt |

Quellen: NetHunter GitLab, XDA Forums Community-Berichte (2024–2026).

### 4.3 Bekannte Probleme

**Problem 1: MT7612U-Interface erscheint nicht auf älteren Kernels**

Symptom: `lsusb` zeigt `0e8d:7612`, aber `ip link` listet kein `wlan1`.  
Ursache: Der Custom Kernel wurde ohne das `mt76x2u`-Modul kompiliert. Dies betrifft einige 4.14-basierte NetHunter-Kernel (OnePlus-7T-Ära).  
Behebung: Verwende einen Kernel-Build, der das Modul enthält, oder wechsle zum AWUS036ACHM (MT7610U), der breitere Unterstützung auf älteren Kernels hat.

**Problem 2: USB-Spannungseinbruch verursacht Adapterabbrüche**

Symptom: Adapter verschwindet mitten im Scan, `dmesg` zeigt USB-Reset-Fehler.  
Ursache: Der USB-Port des Telefons kann die Stromaufnahme des Adapters nicht dauerhaft liefern, insbesondere bei USB-3.0-Adaptern (ACH zieht ~500mW).  
Behebung: Verwende einen powered OTG-Hub, der den Adapter mit 5V von einem Netzteil versorgt und gleichzeitig Daten an das Telefon weiterleitet.

**Problem 3: Adapter eingesteckt, bevor das Chroot gestartet wurde**

Symptom: Android zeigt USB-Berechtigungsdialog, aber Kali-Tools können nicht auf den Adapter zugreifen.  
Ursache: Die NetHunter-Chroot-Umgebung muss laufen, bevor USB-Geräte für sie freigegeben werden.  
Behebung: Starte zuerst das Chroot (Kali Services → Start), verbinde dann den Adapter und erteile die USB-Berechtigung.

---

## 5. Einrichtungsanleitung

### 5.1 Voraussetzungen

Bevor du Hardware anschließt, überprüfe:

```bash
# Bestätige, dass das Gerät gerootet ist
su -c "id"

# Überprüfe die NetHunter-Chroot-Version
cat /kali/etc/os-release
# Sollte Kali Linux mit NetHunter anzeigen

# Bestätige, dass USB-OTG aktiviert ist
# Einstellungen → Entwickleroptionen → OTG (genaue Position variiert je nach Android-Version)
```

### 5.2 Hardware-Anschlussreihenfolge

Die Reihenfolge ist wichtig:

1. Starte die **NetHunter-App** → öffne **Kali Services** → tippe auf **Start**, um das Chroot zu starten
2. Verbinde den **powered OTG-Hub** mit dem USB-Port deines Telefons
3. Stecke den **ALFA-Adapter** in den OTG-Hub
4. Wenn der Android-USB-Berechtigungsdialog erscheint, tippe auf **OK** und aktiviere **Immer erlauben**

{{< alert "circle-info" >}}
Ein powered OTG-Hub wird für den Dauerbetrieb dringend empfohlen. Der AWUS036ACH zieht ungefähr 500mW — ihn direkt über den Telefonakku zu betreiben, beschleunigt die Entladung erheblich und kann USB-Instabilität verursachen. Ein Hub, der Daten durchleitet und gleichzeitig Strom von einem Netzteil bezieht, beseitigt beide Probleme.
{{< /alert >}}

### 5.3 Adaptererkennung überprüfen

```bash
# Liste USB-Geräte auf — bestätige, dass der Adapter erscheint
lsusb

# Erwartete Ausgabe nach Modell:
# AWUS036ACHM: Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.
# AWUS036ACM:  Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U
# AWUS036ACH:  Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp.
```

Wenn der Adapter nicht erscheint: Probiere ein anderes OTG-Kabel, überprüfe, ob OTG in den Entwickleroptionen aktiviert ist, oder teste den Adapter an einem Computer, um seine Funktionsfähigkeit zu bestätigen.

### 5.4 Treiber laden

**Für MT7610U (AWUS036ACHM) — lädt auf den meisten Kernels automatisch:**

```bash
# Automatisches Laden überprüfen
lsmod | grep mt76

# Manuelles Laden, falls nötig (selten)
sudo modprobe mt76x0u
```

**Für MT7612U (AWUS036ACM) — lädt automatisch auf Kernel 4.19+:**

```bash
# Überprüfen
lsmod | grep mt76

# Manuelles Laden, falls nötig
sudo modprobe mt76x2u
```

**Für RTL8812AU (AWUS036ACH) — in den meisten NetHunter-Kernels vorkompiliert:**

```bash
# Vorkompiliertes Modul laden
sudo modprobe 88XXau

# Überprüfen, ob es geladen wurde
lsmod | grep 88XX
```

### 5.5 Netzwerkinterface bestätigen

```bash
# Drahtlose Interfaces auflisten
ip link show | grep wlan

# Oder iw verwenden
iw dev

# Der externe Adapter erscheint typischerweise als wlan1
# (wlan0 ist normalerweise das eingebaute WLAN des Telefons)
```

### 5.6 Monitor Mode aktivieren

```bash
# Störende Prozesse beenden
sudo airmon-ng check kill

# Monitor Mode auf dem Adapter starten
sudo airmon-ng start wlan1

# Überprüfen, ob Monitor Mode aktiv ist
iwconfig wlan1mon
# Erwartete Ausgabe: Mode:Monitor

# Netzwerke in der Nähe scannen (nur autorisierte Tests)
sudo airodump-ng wlan1mon

# Alle Bänder scannen (2,4 GHz + 5 GHz)
sudo airodump-ng --band abg wlan1mon
```

### 5.7 Zurück in den Managed Mode

```bash
sudo airmon-ng stop wlan1mon
sudo service NetworkManager restart
```

---

## 6. Anwendungstopologie

<img src="/images/blog/nethunter-topology.png" alt="NetHunter + ALFA Application Topology Diagram" loading="eager" style="max-width:100%;height:auto;display:block">

---

## 7. Validierungsergebnisse

### 7.1 Testmatrix

Die folgenden Kombinationen wurden durch Community-Tests und Herstellerdokumentation verifiziert:

| Telefon | ALFA-Adapter | Chipsatz | Monitor Mode | Packet Injection | Status |
|---|---|---|---|---|---|
| OnePlus 11 5G | AWUS036ACHM | MT7610U | ✅ | ✅ | Verifiziert |
| OnePlus 11 5G | AWUS036ACM | MT7612U | ✅ | ✅ | Verifiziert |
| OnePlus 11 5G | AWUS036ACH | RTL8812AU | ✅ | ✅ | Verifiziert |
| Samsung S20 FE (Snapdragon) | AWUS036ACH | RTL8812AU | ✅ | ⚠️ | Community-Berichte — Kernel-Konfiguration prüfen |
| Samsung S20 FE (Snapdragon) | AWUS036ACHM | MT7610U | ✅ | ✅ | Community-Berichte |
| Nothing Phone (1) | AWUS036ACHM | MT7610U | ✅ | ✅ | Community-Berichte |

Quellen: XDA Forums, Reddit r/NetHunter, Kali NetHunter GitLab Issues (2024–2026).

### 7.2 Erwartete `lsusb`-Ausgabe

```
# AWUS036ACHM
Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.

# AWUS036ACM
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter

# AWUS036ACH
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
```

### 7.3 Monitor-Mode-Verifizierung

```bash
# Erwartete iwconfig-Ausgabe bei Erfolg
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.437 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

---

## 8. Empfehlungen

### 8.1 Top-Empfehlung: OnePlus 11 5G + AWUS036ACHM

Diese Kombination hat die geringste Reibung aller getesteten Setups. Das OnePlus 11 ist das neueste Flaggschiff mit offizieller NetHunter-Kernel-Unterstützung, das du für den taiwanesischen Markt noch beziehen kannst. Der MT7610U-Chipsatz des AWUS036ACHM verwendet den `mt76x0u`-Treiber — er ist seit 4.19 im Mainline-Kernel, erfordert keinerlei Kompilierung und die internationale Sicherheits-Community (Lab401, morrownr USB-WiFi-Datenbank) stuft ihn durchgängig als sicherste Wahl für Kali und NetHunter ein. Der Adapter ist kompakt, hat eine einzelne Antenne und läuft über USB 2.0, was in mobilen Szenarien ein Vorteil ist — geringere Leistungsaufnahme, weniger Wärme, weniger Fehlerquellen.

### 8.2 Leistungs-Empfehlung: OnePlus 11 5G + AWUS036ACM

Wenn du Dual-Band-AC1200-Leistung mit MIMO 2T2R für 5-GHz-Erfassung auf Entfernung benötigst, bietet dir der ACM das, ohne das In-Kernel-Treiber-Ökosystem zu verlassen. Der `mt76x2u`-Treiber des MT7612U ist ebenfalls seit 4.19 im Mainline. Der Kompromiss: USB 3.0 zieht mehr Strom und das Dual-Antennen-Gehäuse ist größer. Überprüfe, ob der Kernel `mt76x2u` enthält — beim OnePlus 11 ist dies bestätigt.

### 8.3 Community-Favorit: Jedes NetHunter-Gerät + AWUS036ACH

Der ACH hat die meisten Tutorials, die größte Community-Fehlerbehebungsbasis und die beste Drittanbieter-Dokumentation aller Adapter im NetHunter-Ökosystem. Seine dualen 5dBi-Antennen bieten die stärkste Signalreichweite im ALFA-Sortiment. Die meisten NetHunter-Kernel kompilieren das `88XXau`-Modul vor, sodass eine Kompilierung selten erforderlich ist. Wenn du Community-Unterstützung und Long-Range-Capture über Plug-and-Play-Einfachheit stellst, ist dies die richtige Wahl.

### 8.4 Szenariobasierte Auswahl

| Szenario | Empfohlene Kombination | Begründung |
|---|---|---|
| Erstes NetHunter-Setup, Risiko minimieren | OnePlus 11 + AWUS036ACHM | In-Kernel-Treiber, keine Kompilierung, kleinste Bauform |
| Dual-Band-Erfassung mit Reichweite | OnePlus 11 + AWUS036ACM | AC1200 + MIMO, weiterhin In-Kernel |
| Long-Range-Survey, maximale Tutorials | Jedes unterstützte Gerät + AWUS036ACH | Stärkste Antenne, breiteste Community-Unterstützung |
| Ultraportabel, niedrigste Leistungsaufnahme | Jedes unterstützte Gerät + AWUS036ACS | 300mW Verbrauch, passt in jede Tasche |

### 8.5 Support-Ressourcen

| Ressource | Link |
|---|---|
| Yupitek — ALFA autorisierter Distributor Taiwan | [yupitek.com](https://www.yupitek.com) |
| ALFA Network offizielle Produktseiten | [alfa.com.tw](https://www.alfa.com.tw) |
| MT7610U-Treiber (Kernel-Baum) | [torvalds/linux — mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| RTL8812AU-Treiber (aircrack-ng) | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| NetHunter unterstützte Geräte | [nethunter.kali.org/device-kernels.html](https://nethunter.kali.org/device-kernels.html) |
| NetHunter offizielle Dokumentation | [kali.org/docs/nethunter/](https://www.kali.org/docs/nethunter/) |
| XDA NetHunter-Forum | [xdaforums.com/tags/nethunter/](https://xdaforums.com/tags/nethunter/) |
| Yupitek ALFA-Produktkatalog | [/de/products/alfa/](/de/products/alfa/) |

---

## Anhang: Schnelle Fehlerbehebung

**Adapter nicht in `lsusb`:**
1. Bestätige, dass OTG in den Entwickleroptionen aktiviert ist
2. Probiere ein anderes OTG-Kabel — die Kabelqualität ist die häufigste Fehlerquelle
3. Verwende einen powered OTG-Hub
4. Überprüfe, ob das NetHunter-Chroot gestartet wurde

**Gerät erscheint in `lsusb`, aber kein `wlan1`-Interface:**

```bash
# Kernel-Meldungen auf Treiberfehler prüfen
dmesg | tail -30 | grep -E "usb|mt76|rtl|88XX"

# Überprüfen, ob das Kernel-Modul existiert
find /lib/modules -name "mt76*" 2>/dev/null
find /lib/modules -name "*88XX*" 2>/dev/null

# Manuelles Laden versuchen
sudo modprobe mt76x0u   # MT7610U
sudo modprobe mt76x2u   # MT7612U
sudo modprobe 88XXau    # RTL8812AU
```

**Monitor Mode startet, aber keine Netzwerke erscheinen:**

```bash
# Zuerst störende Prozesse beenden
sudo airmon-ng check kill

# Alle Bänder neu scannen
sudo airodump-ng --band abg wlan1mon

# Kanaleinstellungen überprüfen
sudo iw dev wlan1mon info
```

**Adapter trennt sich während der Nutzung (USB-Reset):**

```bash
# Temporäre Lösung — Sendeleistung reduzieren
sudo iw dev wlan1 set txpower fixed 1000  # 10 dBm

# Dauerhafte Lösung — powered OTG-Hub verwenden
```

---

{{< faq >}}

## Verwandte Anleitungen

- [Grundlegende OTG-Einrichtung mit ALFA-Adaptern und NetHunter](/de/blog/alfa-adapter-nethunter-android-otg/)
- [ALFA WLAN-Adapter Kaufberatung 2026](/de/blog/alfa-wifi-adapter-buyer-guide-2026/)
- [ALFA-Treiber unter Kali Linux und Ubuntu installieren](/de/blog/install-alfa-driver-kali-ubuntu/)
- [ALFA-Adapter mit Raspberry Pi und Kali verwenden](/de/blog/alfa-adapter-raspberry-pi-kali/)

---

*Dieses Dokument wurde von **Yupitek Ltd** erstellt — ALFA Network autorisierter Distributor für Taiwan.*  
*Datenstand: 09.06.2026. Linux-Kernel- und NetHunter-Versionen werden regelmäßig aktualisiert; überprüfe die offiziellen Quellen für die neuesten Kompatibilitätsinformationen.*

## Referenzen

1. [Kali NetHunter Offizielle Dokumentation](https://www.kali.org/docs/nethunter/) — NetHunter Installations- und Kernel-Flash-Anleitung
2. [Linux Kernel mt76 Treiber-Quellcode](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek/mt76) — MT7610U/MT7612U Mainline-Treiber
3. [aircrack-ng RTL8812AU Treiber](https://github.com/aircrack-ng/rtl8812au) — DKMS Externes Treiber-Repository
4. [ALFA Network Offizielle Website](https://alfa.com.tw/) — Produktspezifikationen und Treiber-Downloads
5. [Android USB OTG Offizielle Dokumentation](https://developer.android.com/guide/topics/connectivity/usb) — OTG-API und Hardware-Anforderungen
