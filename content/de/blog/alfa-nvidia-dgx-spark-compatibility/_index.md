---
title: "Ist der ALFA WLAN-Adapter mit dem NVIDIA DGX Spark (GB10) kompatibel?"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-dgx-spark-compatibility"
tags:
  - "ALFA"
  - "NVIDIA"
  - "DGX-Spark"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "Hardware-Leitfaden"
description: "ALFA-WLAN-Adapter am NVIDIA DGX Spark (GB10): Im GX10-Test laufen alle 9 Karten mit Kernel-Treibern ohne DKMS, nur AXM/AXML scheitern bei der Injection."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Dieser Artikel wurde anhand der GX10-Praxistests vom November 2026 aktualisiert: Auf dem ASUS GX10 (Ubuntu 24.04 ARM64, Kernel 6.17.0-1014-nvidia) laufen alle 9 aktuellen ALFA-Adapter mit den im Kernel integrierten Treibern – einstecken und loslegen, kein DKMS nötig. Alle Daten finden Sie in der [Testmatrix der 9 ALFA-Adapter unter ARM64](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Getestet wurde nur auf dem GX10; andere GB10-Modelle wurden nicht einzeln getestet.

## 1. Problemübersicht

Kundenfrage: „Können die USB-WLAN-Adapter der ALFA-Serie am persönlichen KI-Supercomputer NVIDIA DGX Spark (GB10 Grace Blackwell) verwendet werden?“

Kurzfazit: Der DGX Spark läuft unter NVIDIA DGX OS (basierend auf Ubuntu, Kernel 6.x). Auf dem ASUS GX10, der ebenfalls auf der GB10-Plattform basiert (Ubuntu 24.04 ARM64, Kernel 6.17.0-1014-nvidia), haben wir alle 9 aktuellen ALFA-USB-WLAN-Adapter getestet: Alle verwenden die im Kernel integrierten Treiber, funktionieren direkt nach dem Einstecken und benötigen weder Kompilierung noch DKMS. Der DGX Spark nutzt denselben GB10-Chip und dieselbe NVIDIA-Kernel-Reihe; wir erwarten dasselbe Verhalten, getestet wurde jedoch nur auf dem GX10, der DGX Spark selbst wurde nicht getestet. Funktionsunterschiede: Die MediaTek-MT7921-Modelle (AWUS036AXM / AXML) scheitern auf dem Stock-Kernel 6.17 bei der Paketinjektion; Monitor-Modus, AP und WPA3 funktionieren. Bei den übrigen 7 Modellen wurden Monitor-Modus und Injection erfolgreich getestet. Die Kernel-Version, ab der die Treiber im Mainline-Kernel enthalten sind, unterscheidet sich je Adapter (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); nur ältere Kernel unterhalb dieser Version benötigen die DKMS-Treiber der Community. Hinweis: Alle USB-Ports des DGX Spark sind USB Type-C, die ALFA-Adapter haben USB Type-A; ein USB-C-auf-USB-A-Adapter oder ein entsprechendes Kabel ist erforderlich.

Bewertungsgrundlage: die 9 aktuellen USB-WLAN-Adapter von ALFA (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analyse der Zielhardware-Spezifikation

### 2.1 NVIDIA DGX Spark Hardware-Spezifikation

| Punkt | Spezifikation |
|---|---|
| Produktname | NVIDIA DGX Spark |
| Kernprozessor | NVIDIA GB10 Grace Blackwell Superchip |
| CPU | 20-Kern Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | NVIDIA Blackwell-Architektur, 6144 CUDA-Kerne, fünfte Generation Tensor Core, vierte Generation RT Core |
| AI-Leistung | Bis zu 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| System-Speicher | 128GB LPDDR5x Unified Memory (256-bit, 273 GB/s) |
| Speicher | Bis zu 4TB NVMe M.2 SSD (self-encrypting) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (20Gbps), davon 1 mit PD-Eingang (180W EPR PD3.1) |
| Displayausgang | 1× HDMI 2.1a |
| Netzwerk | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (200G QSFP) |
| WLAN | Wi-Fi 7 (integriert) + Bluetooth 5.4 |
| Betriebssystem | NVIDIA DGX OS (basierend auf Ubuntu Linux, Kernel 6.x) |
| Architektur | aarch64 (ARM64) |
| Abmessungen | 150 × 150 × 50.5 mm (1.13L) |
| Gewicht | ca. 1.2 kg |
| Stromversorgung | 240W USB-C Netzteil |

### 2.2 Softwareumgebung: NVIDIA DGX OS

| Punkt | Beschreibung |
|---|---|
| Basis | Ubuntu Linux (von NVIDIA angepasst) |
| Kernel | Linux 6.x (genaue Version abhängig vom DGX-OS-Update) |
| Architektur | aarch64 (ARM64) |
| Vorinstallierte Software | NVIDIA-KI-Softwarepaket (CUDA, cuDNN, TensorRT, PyTorch, Jupyter u. v. m.) |
| Paketverwaltung | apt (Debian/Ubuntu) |
| Treiber-Framework | Standard-Treiberarchitektur des Linux-Kernels (cfg80211 / mac80211) |

### 2.3 Schlüsselmerkmale: Moderner Kernel + ARM64

Die Softwareumgebung des DGX Spark hat zwei wesentliche Auswirkungen auf die Kompatibilität mit ALFA-Adaptern:

- Kernel 6.x (modern): Kernel 6.17 (die im GX10-Test verwendete Version) enthält die Treiber aller 9 Adapter dieses Artikels, darunter mt76 (MT7612U / MT7610U, 4.19+), mt7921u (MT7921AUN, 5.18+), rtw88 (RTL8821CU 6.2+; RTL8812AU / RTL8811AU 6.13+) und rtw89 (RTL8832BU, 6.17+). Dies steht in deutlichem Kontrast zum Kernel 4.9 des Jetson Nano.
- ARM64-Architektur (aarch64): Mit den im Kernel integrierten Treibern muss auf ARM64 nichts kompiliert werden; nur auf älteren Systemen mit einem Kernel unter der Mindestversion des jeweiligen Adapters müssen für die Realtek-Modelle DKMS-Treiber der Community kompiliert werden (z. B. die morrownr-Reihe; dabei muss im Makefile CONFIG_PLATFORM_ARM64 = y gesetzt sein).

### 2.4 Bedarf an USB-Type-C-Adaptern

Die 4 USB-Ports des DGX Spark sind alle Type-C, während alle ALFA-Adapter (außer dem AXML mit USB-C) eine USB-Type-A-Schnittstelle haben:

| Modell | Schnittstelle | Adapter nötig |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ Kein Adapter nötig (direkt steckbar) |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ USB-C auf USB-A nötig |
| AWUS036AX | USB Type-A / USB 3.2 | ✅ Nötig |
| AWUS036AXER | USB Type-A / USB 3.2 | ✅ Nötig |
| AWUS036ACH | USB Type-A / USB 3.0 | ✅ Nötig |
| AWUS036ACHM | USB Type-A / USB 2.0 | ✅ Nötig |
| AWUS036ACM | USB Type-A / USB 3.0 | ✅ Nötig |
| AWUS036ACS | USB Type-A / USB 2.0 | ✅ Nötig |
| AWUS036EACS | USB Type-A / USB 2.0 | ✅ Nötig |

Empfehlung: Verwenden Sie einen USB-C-auf-USB-A-Adapter oder ein Kabel mit USB 3.2 Gen 2×2 (20Gbps), damit USB-3.x-Modelle wie AWUS036ACH / ACM / AX mit voller Geschwindigkeit arbeiten.

## 3. Analyse der aktuellen ALFA-Adapter: Spezifikationen und Chipsätze

Stand September 2026 umfasst die aktuelle Produktlinie der USB-WLAN-Adapter von ALFA Network folgende Modelle (Bewertungsgrundlage: 9 Modelle):

| Modell | Wi-Fi-Standard | Chipsatz | Schnittstelle | Integrierter Linux-Treiber (Mindest-Kernel) |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E (6 GHz im Test nutzbar) | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ Integriert (mt7921u, 5.18+) |
| AWUS036AXM | Wi-Fi 6E (Herstellerangabe, 6 GHz nicht getestet) | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ Integriert (mt7921u, 5.18+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ Integriert (rtw89_8852bu, 6.17+) |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ Integriert (rtw89_8852bu, 6.17+) |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ Integriert (rtw88_8812au, 6.13+) |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | ✅ Integriert (mt76x0u, 4.19+) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ Integriert (mt76x2u, 4.19+) |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | ✅ Integriert (rtw88_8821au, 6.13+) |
| AWUS036EACS | Wi-Fi 5 (AC600) + Bluetooth | Realtek RTL8821CU | USB 2.0 | ✅ Integriert (rtw88_8821cu, 6.2+) |

Hinweis: Der im GX10-Test verwendete Kernel 6.17 enthält bereits die Treiber aller 9 Adapter; die Mindest-Kernel-Version unterscheidet sich je Adapter (siehe Klammern in der Tabelle). Nur auf älteren Systemen mit einem Kernel unterhalb dieser Mindestversion ist ein von der Community gepflegter DKMS-Treiber nötig.

## 4. Geeignete Modelle und Chipsätze

### 4.1 Empfehlungsstufen

| Empfehlungsstufe | Modell (Chipsatz) | Beschreibung |
|---|---|---|
| ⭐ Erste Wahl für Penetrationstests | AWUS036EACS (RTL8821CU) / AWUS036ACH (RTL8812AU) / AWUS036ACS (RTL8811AU) | Integrierter Treiber, keine Installation; Injection im Test: EACS und ACH auf beiden Bändern 100 %, ACS 2,4 GHz 100 %, 5 GHz 96 %; WPA-Handshake End-to-End erfassbar |
| ✅ Empfohlen | AWUS036ACM (MT7612U) | Integrierter Treiber, keine Installation; Monitor, Injection (2,4 GHz 63–83 %, 5 GHz 76 %), AP und WPA3 nutzbar |
| ✅ Empfohlen | AWUS036ACHM (MT7610U) | Integrierter Treiber, keine Installation; 2,4-GHz-Injection 96–100 %, 5-GHz-Injection nur Broadcast; WPA3-AP erfordert sae_pwe=0 |
| ✅ Empfohlen (Wi-Fi 6) | AWUS036AX / AXER (RTL8832BU) | Integrierter Treiber, keine Installation; starker Monitor-Empfang, Injection nutzbar (2,4 GHz: AX 96 %, AXER 73 %), AP mit 80 MHz |
| ⚠️ Nur für Verbindung/AP | AWUS036AXML / AXM (MT7921AUN) | Integrierter Treiber, keine Installation; Monitor, AP und WPA3 nutzbar, aber Injection scheitert auf dem Stock-Kernel 6.17, daher nicht für Penetrationstests geeignet; AXML ist USB-C und direkt steckbar |

### 4.2 Empfehlungen nach Anwendungsszenario

| Anwendungsszenario | Empfohlenes Modell | Beschreibung |
|---|---|---|
| Allgemeiner WLAN-Internetzugang (am einfachsten) | Alle 9 Modelle (z. B. AWUS036ACM / ACHM) | Alle mit integriertem Kernel-Treiber, einstecken und loslegen |
| WLAN-Penetrationstests / Monitoring / Injection | AWUS036EACS / ACH / ACS | Injection im Test 96–100 %, WPA-Handshake End-to-End erfassbar; AXM / AXML nicht wählen (Injection scheitert) |
| Wi-Fi 6 + AP-Hotspot | AWUS036AX / AXER | 2x2, AP mit 80 MHz im Test nutzbar |
| 6-GHz-Band | AWUS036AXML | Im Test WPA3-AP auf 6 GHz möglich; AXM hat denselben Chip, 6 GHz aber nicht getestet |
| Vorhandenen AWUS036ACH weiter nutzen | AWUS036ACH | Ab Kernel 6.13 ist rtw88_8812au integriert, einstecken und loslegen, Injection auf beiden Bändern im Test 100 % |
| Kein externes WLAN nötig (internes WLAN nutzen) | — | Der DGX Spark hat integriertes Wi-Fi 7; für normalen Internetzugang ist kein externer ALFA-Adapter nötig |

Hinweis: Der DGX Spark hat bereits Wi-Fi 7 + Bluetooth 5.4 integriert; für normalen Internetzugang ist kein externer ALFA-Adapter nötig. Externe ALFA-Adapter werden vor allem für Penetrationstests (Monitoring/Injection), spezielle Chipsatz-Anforderungen oder Szenarien benötigt, in denen das interne WLAN nicht ausreicht.

## 5. Umgebungsanforderungen

### 5.1 Hardwareanforderungen

| Punkt | Anforderung |
|---|---|
| USB-Adapter | USB-C-auf-USB-A-Adapter oder -Kabel (außer AXML) |
| Stromversorgung | Original-240W-USB-C-Netzteil des DGX Spark (USB-Ports liefern ausreichend Strom) |
| Kühlung | Originalkühlung genügt (USB-WLAN erhöht die Systemlast nicht nennenswert) |

### 5.2 Softwareanforderungen

| Punkt | Anforderung |
|---|---|
| DGX-OS-Version | Jede aktuelle Version (Kernel 6.x) |
| Kernel-Version | Kernel 6.17 (GX10 getestet mit 6.17.0-1014-nvidia) enthält die Treiber aller 9 Adapter, keine Build-Tools nötig; die Mindestversion unterscheidet sich je Adapter (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), nur darunter ist ein DKMS-Treiber der Community nötig |
| WLAN-Verwaltungstools | iw, wpa_supplicant, network-manager (in DGX OS vorinstalliert) |

## 6. Kompatibilitätsbewertung

### Aktuelle ALFA-Modelle × NVIDIA DGX Spark (GB10): Kompatibilitätsmatrix

| Modell | Chipsatz | Treiber (im Kernel integriert) | USB-Erkennung | STA-Internet | AP-Modus | Monitor | Packet Injection | Installationsaufwand | Gesamtbewertung |
|---|---|---|---|---|---|---|---|---|---|
| AWUS036EACS | RTL8821CU | rtw88_8821cu | ✅ | ✅ | ✅ | ✅ | ✅ beide Bänder 100 % | Keine Installation | ⭐ Beste |
| AWUS036ACH | RTL8812AU | rtw88_8812au | ✅ | ✅ | ✅ | ✅ | ✅ beide Bänder 100 % | Keine Installation | ⭐ Beste |
| AWUS036ACS | RTL8811AU | rtw88_8821au | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 100 % / 5G 96 % | Keine Installation | ⭐ Beste |
| AWUS036ACM | MT7612U | mt76x2u | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 63–83 % / 5G 76 % | Keine Installation | ✅ Gut |
| AWUS036ACHM | MT7610U | mt76x0u | ✅ | ✅ | ✅ | ✅ | ⚠️ 2.4G 96–100 % / 5G nur Broadcast | Keine Installation | ✅ Gut |
| AWUS036AX | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ starker Empfang | ✅ 2.4G 96 % / 5G nutzbar | Keine Installation | ✅ Gut |
| AWUS036AXER | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ starker Empfang | ✅ 2.4G 73 % / 5G nutzbar | Keine Installation | ✅ Gut |
| AWUS036AXML | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ schwacher Empfang | ❌ Fehlgeschlagen | Keine Installation | ⚠️ Nur Verbindung/AP |
| AWUS036AXM | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ schwacher Empfang | ❌ Fehlgeschlagen | Keine Installation | ⚠️ Nur Verbindung/AP |

Bewertungsgrundlage: Praxistests vom 16. bis 18.11.2026 auf dem ASUS GX10 (Ubuntu 24.04 ARM64, Kernel 6.17.0-1014-nvidia), getestet mit eigenem WLAN und eigenem Smartphone. Der DGX Spark nutzt denselben GB10-Chip und dieselbe NVIDIA-Kernel-Reihe; wir erwarten dasselbe Verhalten, getestet wurde jedoch nur auf dem GX10, der DGX Spark selbst wurde nicht getestet. Alle Daten finden Sie in der [Testmatrix der 9 ALFA-Adapter unter ARM64](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 7. Detaillierte Schritt-für-Schritt-Installation

### 7.1 Vorbereitung

**Schritt 1: DGX Spark starten und anmelden** (per SSH oder direkt mit Tastatur und Monitor)

```bash
ssh username@<dgx-spark-ip>
```

**Schritt 2: Systemarchitektur und Kernel-Version prüfen**

```bash
uname -m
# Erwartet: aarch64
uname -r
# Erwartet: 6.x.x (DGX-OS-Kernel)
```

**Schritt 3: Prüfen, ob der Kernel Version 6.17 oder neuer ist**

Ab Kernel 6.17 sind die Treiber aller 9 Adapter integriert; Build-Tools müssen nicht installiert werden. Die Mindestversion unterscheidet sich je Adapter (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); nur darunter benötigen die Realtek-Modelle DKMS-Treiber der Community (siehe letzter Absatz von 7.3).

### 7.2 Pfad A: MediaTek-Modelle (AWUS036ACM / ACHM / AXML / AXM) — sofort einsatzbereit

**Schritt 1: Adapter einstecken**

Stecken Sie den ALFA-Adapter über einen USB-C-auf-USB-A-Adapter (AXML direkt in den USB-C-Port) in einen USB-Port des DGX Spark.

**Schritt 2: Prüfen, ob der Adapter erkannt wurde**

```bash
lsusb
# Beispiel für die erwartete Ausgabe (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Schritt 3: Prüfen, ob die Netzwerkschnittstelle automatisch angelegt wurde**

```bash
ip link show
# Erwartet: eine Schnittstelle, die mit wlx beginnt (nach MAC-Adresse benannt, in-kernel-Treiber wird automatisch geladen)
```

**Schritt 4: WLAN-Netze scannen** (im Folgenden steht wlan0 als Beispiel; ersetzen Sie es durch den mit `ip link show` ermittelten Schnittstellennamen)

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**Schritt 5: Mit dem WLAN verbinden (über NetworkManager)**

```bash
nmcli dev wifi list
nmcli dev wifi connect "Ihr WLAN-Name" password "Ihr WLAN-Passwort"
```

**Schritt 6: (Optional) Monitor-Modus aktivieren**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info
```

### 7.3 Pfad B: Realtek-Wi-Fi-5-Modelle (AWUS036ACH / ACS / EACS) — ab Kernel 6.13 ohne Installation (EACS ab 6.2)

**Schritt 1: Adapter einstecken und prüfen, ob der Treiber automatisch geladen wurde**

```bash
uname -r          # ACH/ACS benötigen 6.13 oder neuer, EACS 6.2 oder neuer
lsusb
lsmod | grep rtw88
ip link show
```

Automatisch geladene Module je Modell: ACH → `rtw88_8812au`, ACS → `rtw88_8821au`, EACS → `rtw88_8821cu` (der EACS hat zusätzlich Bluetooth, im Test nutzbar).

**Schritt 2: Verbindung wie in 7.2, Schritt 5 (mit nmcli)**

**Schritt 3: (Optional) Monitor-Modus und Injection**

⚠️ Monitoring- und Injection-Tests nur in eigenen oder ausdrücklich autorisierten Netzwerken durchführen.

```bash
sudo apt install -y aircrack-ng
IF=wlx00c0cafe0000   # durch den mit ip link ermittelten Schnittstellennamen ersetzen
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
sudo aireplay-ng --test $IF
```

- Führen Sie `airmon-ng check kill` nicht aus: Es beendet den NetworkManager und trennt den Host vom Netzwerk.
- AWUS036AXM / AXML: `aireplay-ng --test` schlägt auf dem Stock-Kernel 6.17 fehl (Found 0 APs); Deauth und Handshake-Erfassung sind nicht möglich.
- hcxdumptool 8.x meldet auf allen 9 Adaptern außer dem EACS auf 2,4 GHz `failed to arm` (der Treiber unterstützt keinen Active Monitor); verwenden Sie stattdessen airodump-ng + aireplay-ng.

**Nur für ältere Kernel (ACH/ACS unter 6.13, EACS unter 6.2) nötige Schritte**: Nach der Installation von `build-essential git bc dkms` den Community-Treiber kompilieren, z. B. morrownr/8812au-20210820 für den RTL8812AU (im Makefile muss `CONFIG_PLATFORM_ARM64 = y` gesetzt sein). Ist die Kernel-Version ausreichend, verwenden Sie bitte direkt den integrierten Treiber.

### 7.4 Pfad C: Wi-Fi-6-Modelle (AWUS036AX / AXER, RTL8832BU) — ab Kernel 6.17 ohne Installation

```bash
lsusb                      # erwartet: 0bda:b832
lsmod | grep rtw89_8852bu
ip link show
```

GX10-Praxistest: Der integrierte Kernel-Treiber `rtw89_8852bu` wird automatisch geladen, der Monitor-Empfang ist stark, Injection ist nutzbar (2,4 GHz: AX 96 %, AXER 73 %), AP unterstützt 80 MHz. rtw89_8852bu ist erst seit Kernel 6.17 im Mainline-Kernel enthalten; Systeme mit Kernel 6.16 oder älter benötigen den DKMS-Treiber der Community (morrownr/rtl8852bu-20250826).

## 8. Häufige Fehler und ihre Behebung

| Symptom | Mögliche Ursache | Fehlerbehebung |
|---|---|---|
| lsusb zeigt keinen ALFA-Adapter an | Defekter USB-C-Adapter / Wackelkontakt | USB-C-auf-USB-A-Adapter austauschen; sicherstellen, dass der Adapter Datenübertragung unterstützt (nicht nur Laden); anderen USB-C-Port ausprobieren |
| Nach dem Einstecken eines MediaTek-Adapters keine wlan-Schnittstelle | Kernel-Modul nicht automatisch geladen / Firmware fehlt | Manuell laden: `sudo modprobe mt76x2u`; `dmesg | grep mt76` prüfen; Firmware installieren: `sudo apt install linux-firmware` |
| Realtek-Adapter ohne wlan-Schnittstelle nach dem Einstecken | Kernel unter der Mindestversion des Adapters (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), passender Treiber nicht integriert | Version mit `uname -r` prüfen; Kernel aktualisieren oder auf dem alten Kernel den DKMS-Treiber der Community installieren |
| Nach Installation eines DKMS-Treibers auf altem Kernel meldet modprobe Operation not permitted | Secure Boot / Modulsignatur | Modul signieren oder Secure Boot deaktivieren (tritt mit den integrierten Treibern nicht auf) |
| Nach wiederholtem Wechsel zwischen Monitor/AP werden keine Signale mehr gefunden | RX-Stillstand (RX stall) | Adapter ab- und wieder anstecken, damit USB neu enumeriert |
| EACS/AXML ohne wlx-Schnittstelle nach erneutem Einstecken | Probe des Bluetooth-+-WLAN-Kombigeräts hängt | An einem anderen USB-Port erneut einstecken |
| WLAN-Verbindung instabil / langsam | USB-C-Adapter unterstützt nur USB 2.0 | Durch einen Adapter mit USB 3.2 Gen 2×2 ersetzen; sicherstellen, dass der Adapter mit „Data“ und nicht nur mit „Charge Only“ gekennzeichnet ist |
| Konflikt zwischen internem Wi-Fi 7 und externem ALFA-Adapter | Routing-Konflikt zwischen zwei WLAN-Schnittstellen | Internes WLAN deaktivieren: `sudo nmcli radio wifi off` oder im BIOS/UEFI abschalten; alternativ Routing-Prioritäten festlegen |
| 6 GHz (Wi-Fi 6E) nicht nutzbar | Einschränkung der Regulierungsdomäne | Regulierungsdomäne setzen: `sudo iw reg set US` (6 GHz in den USA freigegeben); AXML im Test auf 6 GHz funktionsfähig, AXM nicht getestet |
| AP-Modus startet nicht | Konflikt zwischen NetworkManager und hostapd | Siehe Yopitek-Anleitung zu ALFA Soft AP; die Schnittstelle aus der Verwaltung durch NetworkManager nehmen und hostapd manuell einrichten |
| Adapter verschwindet nach dem Aufwachen | USB-Autosuspend | USB-Autosuspend deaktivieren: `echo 'options usbcore autosuspend=-1' | sudo tee /etc/modprobe.d/usb.conf` |

## 9. Bekannte Einschränkungen

- Bedarf an USB-Type-C-Adaptern: Alle ALFA-Adapter außer dem AXML benötigen einen USB-C-auf-USB-A-Adapter; dessen Qualität beeinflusst Leistung und Stabilität
- Injection scheitert bei MT7921-Modellen: AWUS036AXM / AXML scheitern auf dem Stock-Kernel 6.17 bei der Paketinjektion, Deauth und Handshake-Erfassung sind nicht möglich; Monitor, AP und WPA3 funktionieren. Hauptursache ist eine mac80211-chanctx-Regression ab Kernel 6.16; gepatchte Community-Treiber sind weiterhin ratenbegrenzt
- Testumfang: Getestet nur auf dem ASUS GX10 (Kernel 6.17.0-1014-nvidia); der DGX Spark wurde nicht getestet, dasselbe Verhalten wird erwartet
- hcxdumptool nicht nutzbar: Alle Adapter außer dem EACS auf 2,4 GHz melden `failed to arm`; verwenden Sie stattdessen airodump-ng + aireplay-ng
- Mögliche Konflikte mit dem integrierten Wi-Fi 7: Der DGX Spark hat integriertes Wi-Fi 7; bei gleichzeitiger Nutzung von internem und externem WLAN können Routing- oder Ressourcenkonflikte auftreten
- AP-Modus muss manuell eingerichtet werden: DGX OS ist standardmäßig als Entwicklungsumgebung konfiguriert; der AP-Hotspot-Modus erfordert die manuelle Installation und Einrichtung von hostapd / dnsmasq
- 6-GHz-Regulierung: Die Verfügbarkeit des 6-GHz-Bands von Wi-Fi 6E hängt von der eingestellten Regulierungsdomäne ab; für Taiwan sind die aktuellen Vorschriften zur 6-GHz-Freigabe zu prüfen
- Ältere Kernel: Nur Systeme mit einem Kernel unter der Mindestversion des Adapters (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17) benötigen für die Realtek-Modelle DKMS-Treiber der Community (morrownr), die nach jedem Kernel-Update neu kompiliert werden müssen
- Unterschiede bei Penetrationstests: Im GX10-Test erreichten die Realtek-rtw88-Modelle die höchste Injection-Erfolgsquote (EACS und ACH auf beiden Bändern 100 %); die MediaTek-mt76-Modelle (ACM / ACHM) sind nutzbar; MT7921 (AXM / AXML) scheitert
- Bluetooth: Bluetooth von AWUS036AXML und AWUS036EACS wurde auf dem GX10 erfolgreich getestet; das Bluetooth des AWUS036AXM wurde nicht separat geprüft (der DGX Spark hat bereits BT 5.4 integriert)
- RTL8832BU (AWUS036AX / AXER): Treiber-Maintainer morrownr hat öffentlich empfohlen, die Out-of-Tree-Treiber der rtl8852/32au-Reihe zu meiden (Quelle siehe Kapitel 10). Beim GX10-Test kam jedoch der im Kernel integrierte Treiber `rtw89_8852bu` zum Einsatz; Monitor, Injection, AP und WPA3 funktionieren. Diese Aussage gilt nur für den integrierten Treiber ab Kernel 6.17
- RTL8812AU (AWUS036ACH): Der mac80211-konforme in-kernel-Treiber `rtw88_8812au` wurde in Kernel 6.13 in den Mainline-Kernel aufgenommen und ist ab 6.14 ausgereift (Ankündigung von morrownr). Im GX10-Test mit Kernel 6.17 funktionierte er direkt nach dem Einstecken, Injection auf beiden Bändern 100 %. Der Kundendienst kann Kunden vor der Antwort bitten, `uname -r` mitzuteilen, um zu prüfen, ob Version 6.13 oder neuer vorliegt

Widerlegungsbedingungen: Ändert sich nach einem DGX-OS-Update die Kernel-Version oder der USB-Controller-Treiber, sodass sich das Verhalten ändert, oder ergeben Tests auf einem echten DGX Spark andere Ergebnisse als auf dem GX10, muss die Kompatibilitätsmatrix in Kapitel 6 neu geprüft werden. Behebt ein künftiger Kernel das Injection-Problem von mt7921u, kann die Bewertung von AWUS036AXM / AXML von „Nur Verbindung/AP“ heraufgestuft werden.

## 10. Referenzquellen (URL)

| Quelle | Beschreibung | URL | Prüfstatus | Prüfdatum |
|---|---|---|---|---|
| NVIDIA DGX Spark offizielle Seite | Spezifikationen und Plattforminformationen zum DGX Spark | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Geprüft | 2026-09-03 |
| NVIDIA DGX Dokumentation | Systemarchitektur und Kernel-Version von DGX OS | https://docs.nvidia.com/dgx/dgx-spark | ✅ Geprüft | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU-Linux-Treiber (ARM64-Unterstützung) | https://github.com/morrownr/8812au-20210820 | ✅ Geprüft | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8821CU-Linux-Treiber (für ältere Kernel) | https://github.com/morrownr/8821cu-20210916 | ✅ Geprüft | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU-Linux-Treiber | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Geprüft | 2026-09-03 |
| Linux-Kernel-Dokumentation zum mt76-Treiber | Beschreibung der MediaTek-mt76-/mt7921-Mainline-Treiber (inkl. Kernel-Version, ab der die einzelnen Chips unterstützt werden) | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ Geprüft | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide (Yopitek) | Anleitung zum ALFA-AP-Modus unter Linux | /de/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Geprüft | 2026-09-03 |
| ALFA Network Produktübersicht (Yopitek) | Spezifikationen der aktuellen ALFA-Produkte | /de/products/alfa/ | ✅ Geprüft | 2026-09-03 |
| Testmatrix der 9 ALFA-Adapter unter ARM64 (Yopitek) | Praxistest auf ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Praxistest | 2026-11-18 |
| morrownr/USB-WiFi Issue #314 | Offizielle Stellungnahme des Treiber-Maintainers: Empfehlung, Chips der Reihe rtl8852/32au (RTL8832BU) zu meiden | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Geprüft | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | Aktueller Status des RTL8812AU-Treibers (in Kernel 6.13 in den Mainline-Kernel aufgenommen, ab 6.14 ausgereift) | https://github.com/morrownr/8812au-20210820 | ✅ Geprüft | 2026-09-03 |

Verwandte Artikel: [Ist der ALFA WLAN-Adapter mit dem MSI EdgeXpert kompatibel?](/de/blog/alfa-msi-edgexpert-compatibility/) | [Ist der ALFA WLAN-Adapter mit dem ASUS Ascent GX10 (GB10) kompatibel?](/de/blog/alfa-asus-ascent-gx10-compatibility/) | [Ist der ALFA WLAN-Adapter mit dem ALTOS BrainSphere GB10 F1 kompatibel?](/de/blog/alfa-altos-brainsphere-gb10-compatibility/) | [Ist der ALFA WLAN-Adapter mit dem GIGABYTE AI TOP ATOM kompatibel?](/de/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [Ist der ALFA WLAN-Adapter mit dem NVIDIA Jetson Nano kompatibel?](/de/blog/alfa-nvidia-jetson-nano-compatibility/)

Haftungsausschluss: Die Kompatibilitätsbewertung in diesem Artikel basiert auf Praxistests vom November 2026 auf dem ASUS GX10 (Ubuntu 24.04 ARM64, Kernel 6.17.0-1014-nvidia). Der DGX Spark nutzt denselben GB10-Chip und dieselbe NVIDIA-Kernel-Reihe wie der GX10; wir erwarten dasselbe Verhalten, er wurde jedoch nicht einzeln getestet. Der im GX10-Test verwendete Kernel 6.17 enthält die Treiber aller 9 ALFA-Adapter (die Mindestversion unterscheidet sich je Adapter); nur bei einem Kernel unterhalb dieser Mindestversion sind die DKMS-Treiber der Community nötig (morrownr). Der DGX Spark hat bereits integriertes Wi-Fi 7; externe ALFA-Adapter dienen vor allem Penetrationstests oder speziellen Chipsatz-Anforderungen. Die Qualität des USB-C-Adapters wirkt sich direkt auf die Nutzung aus; wir empfehlen Markenadapter mit der Kennzeichnung USB 3.2 Gen 2×2. Monitoring und Injection nur in eigenen oder ausdrücklich autorisierten Netzwerken.
