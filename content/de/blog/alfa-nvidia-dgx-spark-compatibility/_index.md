---
title: "\"Unterstützt das ALFA Wireless Netzwerkadapter das NVIDIA DGX Spark (GB10)?\""
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
description: "DGX Spark支持ALFA网卡，MediaTek芯片型无需驱动，Realtek需编译驱动，USB-C to USB-A适配器需用。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Problemübersicht

Kunde fragt: „Kann das ALFA-Serie USB-WLAN-Adapter auf dem NVIDIA DGX Spark (GB10 Grace Blackwell) Personal AI Supercomputer verwendet werden?“

Kurze Zusammenfassung: Der DGX Spark läuft unter NVIDIA DGX OS (basierend auf Ubuntu, Kernel 6.x), die Kompatibilität des ALFA-Adapters ist mit der eines modernen Linux-Desktop-Systems identisch. MediaTek-Chipmodelle (AWUS036ACM / ACHM / AXML / AXM) verwenden in-kernel-Treiber und sind sofort einsatzbereit; Realtek-Chipmodelle (AWUS036ACH / ACS / EACS / AX / AXER) erfordern die Übersetzung eines out-of-tree-Treibers (ARM64 / aarch64-Architektur). Bitte beachten: Alle USB-Ports des DGX Spark sind USB Type-C, während die ALFA-Adapter USB Type-A haben. Es ist ein USB-C to USB-A Adapter oder ein USB-Kabel erforderlich.

Beurteilung der Hauptkriterien: ALFA hat derzeit 9 aktive USB-WLAN-Adapter (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analyse der Zielhardware-Spezifikation

### 2.1 NVIDIA DGX Spark Hardware-Spezifikation

| Projekt | Spezifikation |
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

| Projekt | Beschreibung |
|---|---|
| Basis | Ubuntu Linux (NVIDIA angepasst) |
| Kernel | Linux 6.x (genaue Version variiert mit DGX OS-Update) |
| Architektur | aarch64 (ARM64) |
| Vorinstallierte Software | NVIDIA AI Software-Paket (CUDA, cuDNN, TensorRT, PyTorch, Jupyter u.v.m.) |
| Paketverwaltung | apt (Debian/Ubuntu) |
| Treiberrahmen | Standard Linux Kernel Driver-Architektur (cfg80211 / mac80211) |

### 2.3 Schlüsselmerkmale: Moderne Kernel + ARM64

Die Softwareumgebung von DGX Spark hat zwei Schlüsselwirkungen auf die Kompatibilität mit ALFA Netzwerken:

- Kernel 6.x (modern): Alle in den Mainline aufgenommenen WiFi-Treiber können direkt verwendet werden, einschließlich mt76 (MT7612U / MT7610U) und mt7921u (MT7921AUN). Dies bildet einen scharfen Kontrast zum Kernel 4.9 auf dem Jetson Nano.
- ARM64 (aarch64) Architektur: Realtek out-of-tree Treiber (8812au / 8821cu / rtl8852bu) müssen auf ARM64 kompiliert werden. Der Upstream (morrownr) dieser Treiber unterstützt ARM64-Kompilierung, aber es muss geprüft werden, dass CONFIG_PLATFORM_ARM64 = y im Makefile eingestellt ist.

### 2.4 Bedarf an USB Type-C Adaptern

Die 4 USB-Ports von DGX Spark sind alle Type-C, während die gesamte ALFA-Serie Netzwerke (außer AXML als USB-C) USB Type-A-Schnittstellen haben:

| Modell | Schnittstellen-Spezifikation | Braucht Adapter |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ Kein Adapter erforderlich (kann direkt eingesteckt werden) |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ Braucht USB-C to USB-A |
| AWUS036AX | USB Type-A / USB 3.2 | ✅ Braucht |
| AWUS036AXER | USB Type-A / USB 3.2 | ✅ Braucht |
| AWUS036ACH | USB Type-A / USB 3.0 | ✅ Braucht |
| AWUS036ACHM | USB Type-A / USB 2.0 | ✅ Braucht |
| AWUS036ACM | USB Type-A / USB 3.0 | ✅ Braucht |
| AWUS036ACS | USB Type-A / USB 2.0 | ✅ Braucht |
| AWUS036EACS | USB Type-A / USB 2.0 | ✅ Braucht |

Empfehlung: Verwenden Sie einen USB-C to USB-A Adapter oder Übertragungsleitung, die USB 3.2 Gen 2×2 (20Gbps) unterstützt, um sicherzustellen, dass die USB 3.x Modelle wie AWUS036ACH / ACM / AX vollwertig funktionieren können.

## 3. Analyse der aktuellen ALFA Netzwerkkarte-Spezifikationen und Chipsets

Bis September 2026 umfasst die aktive USB-WLAN-Produktlinie von ALFA Network wie folgt (Bewertungsgrundlage: 9 Modelle):

| Modell | Wi-Fi-Stufe | Chipset | Schnittstelle | Linux-Treiberstatus |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel (mt7921u, Kernel 5.19+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel (mt7921u) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 (Kernel 5.16+, USB-Unterstützung wird schrittweise integriert) oder out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Wie oben |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree (morrownr/8812au, benötigt ARM64-Übersetzung) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel (mt76x2u)⭐ Empfohlen |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree (8812au abgedeckt) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree (morrownr/8821cu) |

## 4. Verwendbare Modelle und Chipsets

### 4.1 Empfohlene Kategorien

| Empfohlene Kategorie | Modell (Chipset) | Beschreibung |
|---|---|---|
| ⭐ Stark empfohlen | AWUS036ACM (MT7612U) | In-kernel-Treiber, sofort einsatzbereit, AC1200 Dualband, unterstützt AP / Monitor / Injection |
| ✅ Empfohlen | AWUS036ACHM (MT7610U) | In-kernel-Treiber, niedriger Energieverbrauch, AC433 Dualband |
| ✅ Empfohlen (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | In-kernel-Treiber, Wi-Fi 6E, AXML ist USB-C direkt steckbar |
| ⚠️ Verwendbar, aber Anpassung erforderlich | AWUS036ACH (RTL8812AU) | Erfordert Anpassung von morrownr/8812au (ARM64), nach Abschluss sind alle Funktionen vollständig (einschließlich Monitor / Injection) |
| ⚠️ Verwendbar, aber Anpassung erforderlich | AWUS036ACS (RTL8811AU) | Wird von 8812au-Treiber abgedeckt |
| ⚠️ Verwendbar, aber Anpassung erforderlich | AWUS036EACS (RTL8811CU) | Erfordert Anpassung von morrownr/8821cu (ARM64) |
| ⚠️ Verwendbar, aber zu beachten | AWUS036AX / AXER (RTL8832BU) | Kernel 6.x möglicherweise bereits rtw89 unterstützt; ohne Anpassung out-of-tree |

### 4.2 Empfohlene Anwendungsszenarien

| Anwendungsszenario | Empfohlenes Modell | Beschreibung |
|---|---|---|
| Allgemeines WLAN-Internet (am einfachsten) | AWUS036ACM / ACHM | In-kernel-Treiber, ohne Anpassung, sofort einsatzbereit |
| WLAN-Penetrationstests / Monitoring / Injection | AWUS036ACH oder AWUS036ACM | Beide unterstützen Monitor + Injection; ACH erfordert Anpassung, ACM sofort einsatzbereit |
| Wi-Fi 6E / 6GHz-Band | AWUS036AXML / AXM | MT7921AUN in-kernel-Treiber, kernel 6.x vollständig unterstützt |
| AWUS036ACH bereits vorhanden und weiter verwenden möchten | AWUS036ACH | Anpassung des ARM64-Treibers erforderlich, alle Funktionen vollständig |
| Kein externes WiFi erforderlich (verwenden Sie internes WiFi) | — | DGX Spark ist bereits mit Wi-Fi 7 + Bluetooth 5.4 ausgestattet, für allgemeine Internet-Szenarien ist kein externes ALFA-Netzwerk erforderlich |
| Hauptanwendung ist Penetrationstest (Monitoring/Injection), spezifische Chipset-Anforderungen oder internes WiFi nicht ausreichend | — | DGX Spark ist bereits mit Wi-Fi 7 + Bluetooth 5.4 ausgestattet, für allgemeine Internet-Szenarien ist kein externes ALFA-Netzwerk erforderlich |

Hinweis: DGX Spark ist bereits mit Wi-Fi 7 + Bluetooth 5.4 ausgestattet, für allgemeine Internet-Szenarien ist kein externes ALFA-Netzwerk erforderlich. Der Hauptbedarf für die Verwendung von externen ALFA-Netzwerken ist: Penetrationstests (Monitoring/Injection), spezifische Chipset-Anforderungen oder Szenarien, bei denen das interne WiFi nicht ausreichend ist.

## 5. Umgebungsanforderungen

### 5.1 Hardwareanforderungen

| Projekt | Anforderung |
|---|---|
| USB-Adapter | USB-C to USB-A-Adapter oder -Kabel (außer AXML) |
| Stromversorgung | DGX Spark Originalhersteller 240W USB-C Stromversorgungsadapter (USB-Port liefert ausreichend Strom) |
| Kühlung | Originalkühlung genügt (USB WiFi erhöht das Systemlast nicht erheblich) |

### 5.2 Softwareanforderungen

| Projekt | Anforderung |
|---|---|
| DGX OS Version | Jegliche aktive Version (Kernel 6.x) |
| Übersetzungstools (für Realtek-Chips erforderlich) | build-essential, git, bc, dkms |
| Drahtlosverwaltungstools | iw, wpa_supplicant, network-manager (vorgängig auf DGX OS installiert) |
| Netzwerk | Während der Übersetzung des Treibers ist ein kabelgebundenes Netzwerk (10GbE) oder eine integrierte Wi-Fi 7-Verbindung erforderlich |

## 6. Kompatibilitätsbewertung

### ALFA laufende Modelle × NVIDIA DGX Spark（GB10）Kompatibilitätsmatrix

| Modell | Chipset | Treibermethode | USB-Erkennung | STA-Internet | AP-Modus | Monitor | Installationskomplexität | Gesamtbewertung |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel（mt76x2u） | ✅ | ✅ | ✅ | ✅ | Ohne Installation | ⭐ Bestes |
| AWUS036ACHM | MT7610U | in-kernel（mt76x0u） | ✅ | ✅ | ✅ | ⚠️ begrenzt | Ohne Installation | ✅ Gut |
| AWUS036AXML | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ begrenzt | Ohne Installation | ✅ Gut |
| AWUS036AXM | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ begrenzt | Ohne Installation | ✅ Gut |
| AWUS036ACH | RTL8812AU | out-of-tree（8812au） | ✅ | ✅ | ✅ | ✅ | Mittel (Übersetzung) | ⚠️ Verwendbar |
| AWUS036ACS | RTL8811AU | out-of-tree（8812au） | ✅ | ✅ | ⚠️ | ❌ | Mittel (Übersetzung) | ⚠️ Verwendbar |
| AWUS036EACS | RTL8811CU | out-of-tree（8821cu） | ✅ | ⚠️ | ❌ | ❌ | Mittel (Übersetzung) | ⚠️ Verwendbar |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Mittel-Hoch | ⚠️ Verwendbar |
| AWUS036AXER | RTL8832BU | Gleiches wie oben | ✅ | ⚠️ | ⚠️ | ❌ | Mittel-Hoch | ⚠️ Verwendbar |

Bewertungsgrundlage: Verwendbarkeit der Mainline-Treiber im DGX OS Kernel 6.x + Unterstützung für ARM64 im morrownr-Treiber. MediaTek-Chips, da die Treiber bereits in den Mainline integriert sind, funktionieren sofort mit Kernel 6.x. Realtek-Chips erfordern die Übersetzung der out-of-tree-Treiber, aber die ARM64-Übersetzung wird von den Upstream-Unterstützern bereitgestellt.

## 7. Detailliertes Step-by-Step Setup

### 7.1 Vorarbeiten

**Schritt 1: Booten und Anmelden bei DGX Spark** (durch SSH oder direkte Verbindung über Tastatur und Monitor)

```bash
ssh username@<dgx-spark-ip>
```

**Schritt 2: Überprüfen der Systemarchitektur und Kernel-Version**

```bash
uname -m
# Erwartung: aarch64
uname -r
# Erwartung: 6.x.x (DGX OS Kernel)
```

**Schritt 3: (Nur für Realtek-Chips) Installation der Übersetzungstools**

```bash
sudo apt update
sudo apt install -y build-essential git bc dkms
```

### 7.2 Pfad A: MediaTek-Chipsätze (AWUS036ACM / ACHM / AXML / AXM) — Aus der Box nutzbar

**Schritt 1: Netzwerkkarte einstecken**

Verwenden Sie einen USB-C to USB-A Adapter (AXML kann direkt in den USB-C-Anschluss eingesteckt werden) und stecken Sie die ALFA-Netzwerkkarte in den USB-Anschluss des DGX Spark.

**Schritt 2: Überprüfen, ob die Netzwerkkarte erkannt wurde**

```bash
lsusb
# Erwarteter Ausgabebeispiel (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Schritt 3: Überprüfen, ob das Netzwerkinterface automatisch erstellt wurde**

```bash
ip link show
# Erwarteter Ausgabe (in-kernel-Treiber automatisch geladen):
# wlan0 oder wlp...
```

**Schritt 4: WiFi-Netzwerke scannen**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**Schritt 5: Verbindung zum WiFi herstellen (verwenden Sie NetworkManager)**

```bash
nmcli dev wifi list
nmcli dev wifi connect "Ihr WiFi-Name" password "Ihr WiFi-Passwort"
```

**Schritt 6: (Optional) Monitor-Modus aktivieren**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info
```

### 7.3 Pfad B: Realtek-Chipsätze (AWUS036ACH / ACS / EACS) — Erfordert Kompilierung

Beispiel mit AWUS036ACH (RTL8812AU):

**Schritt 1: Herunterladen der Treiber-Quellcodes**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**Schritt 2: Überprüfen der ARM64-Kompilierungsoptionen**

Bearbeiten Sie Makefile, um sicherzustellen, dass `CONFIG_PLATFORM_ARM64 = y` (meistens wird aarch64 automatisch erkannt).

**Schritt 3: Kompilieren und Installieren**

```bash
make
sudo make install
sudo modprobe 8812au
```

**Schritt 4: ALFA-Netzwerkkarte einstecken (durch USB-C to USB-A Adapter), Überprüfen des Interfaces**

```bash
ip link show
# Erwarteter Ausgabe: wlan0
```

**Schritt 5: Verbindung herstellen, wie in Schritt 7.2 Schritt 5 (verwenden Sie nmcli)**

**Schritt 6: (Optional) Monitor-Modus und Injection**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

### 7.4 Pfad C: Wi-Fi 6-Modelle (AWUS036AX / AXER, RTL8832BU)

**Schritt 1: Überprüfen, ob der Kernel bereits rtw89 USB-Unterstützung hat**

```bash
# Nach dem Einstecken der Netzwerkkarte überprüfen
lsusb
dmesg | grep -i "rtw89\|rtl8852\|8832"
ip link show
# Wenn wlan0 automatisch erscheint, bedeutet das, dass der rtw89 im Kernel 6.x unterstützt wird und direkt verwendet werden kann
```

**Schritt 2: Wenn der Kernel nicht automatisch unterstützt, kompilieren Sie den out-of-tree-Treiber**

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
# Überprüfen, dass CONFIG_PLATFORM_ARM64 = y
make
sudo make install
sudo modprobe rtl8852bu
```

## 8. Häufige Fehler und ihre Behebung

| Symptom | Mögliche Ursache | Behebungsmethode |
|---|---|---|
| lsusb zeigt keine ALFA Netzwerkkarte an | Defekter USB-C Adapter / schlechter Kontakt | Ersetzen Sie den USB-C to USB-A Adapter; stellen Sie sicher, dass der Adapter Datenübertragung unterstützt (nicht nur Laden); probieren Sie verschiedene USB-C Ports aus |
| Nach dem Einlegen des MediaTek-Chips ist keine wlan-Schnittstelle vorhanden | Kernel-Modul wurde nicht automatisch geladen / Firmware fehlt | Manuelle Ladevorgang: `sudo modprobe mt76x2u`; Überprüfen Sie `dmesg | grep mt76`; Firmware installieren: `sudo apt install linux-firmware` |
| Realtek-Treiber gibt Fehler bei make aus aarch64-linux-gnu-gcc: not found | Fehler in der Cross-Compile-Einstellung | Stellen Sie sicher, dass Sie auf dem DGX Spark nativ kompilieren (nicht cross-kompilieren); Makefile sollte CROSS_COMPILE nicht setzen |
| modprobe 8812au gibt Fehler Operation not permitted aus | Secure Boot / Modul-Signatur | DGX Spark deaktiviert Secure Boot standardmäßig; wenn Secure Boot aktiviert ist, müssen Sie das Modul signieren oder Secure Boot deaktivieren |
| WiFi-Verbindung instabil / langsam | USB-C Adapter unterstützt nur USB 2.0 | Ersetzen Sie den Adapter, der USB 3.2 Gen 2×2 unterstützt; stellen Sie sicher, dass der Adapter mit "Data" und nicht nur mit "Charge Only" gekennzeichnet ist |
| Internes Wi-Fi und externer ALFA stoßen aufeinander | Konflikt zwischen zwei drahtlosen Schnittstellen | Deaktivieren Sie das interne WiFi: `sudo nmcli radio wifi off` oder deaktivieren Sie es im BIOS/UEFI; oder stellen Sie die Reihenfolge der Routen ein |
| 6GHz (Wi-Fi 6E) kann nicht verwendet werden | Regulatory Domain-Beschränkung | Regulatorischen Bereich einstellen: `sudo iw reg set US` (6GHz in den USA freigegeben); überprüfen Sie, ob das Firmware des AWUS036AXML/AXM den 6GHz unterstützt |
| AP-Modus kann nicht gestartet werden | Konflikt zwischen NetworkManager und hostapd | Beziehen Sie sich auf das Yupitek ALFA Soft AP Handbuch; deaktivieren Sie NetworkManager, um die Schnittstelle zu verwalten, und stellen Sie hostapd manuell ein |
| Netzwerkkarte verschwindet nach dem Aufwachen | USB-Autostopp | Deaktivieren Sie den USB-Autostopp: `echo 'options usbcore autosuspend=-1' | sudo tee /etc/modprobe.d/usb.conf` |

## 9. Bekannte Einschränkungen

- USB Type-C Adapterbedarf: Alle ALFA Netzwerkkarten außer der AXML benötigen einen USB-C to USB-A Adapter, die Qualität des Adapters beeinflusst die Leistung und Stabilität.
- Manuelle Übersetzung der Realtek-Chips: RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU sind nicht in den Mainline aufgenommen, müssen auf ARM64 out-of-tree Treiber kompiliert werden.
- Mögliche Konflikte mit internem Wi-Fi 7: DGX Spark ist mit Wi-Fi 7 ausgestattet, bei der Verwendung von internem und externem WiFi gleichzeitig können Routing- oder Ressourcenkonflikte auftreten.
- Manuelle Einstellung des AP-Modus: DGX OS ist standardmäßig als Entwicklungs-Umgebung konfiguriert, der AP Hotspot-Modus muss manuell mit hostapd / dnsmasq installiert und eingerichtet werden.
- 6GHz-Regelung: Die Verfügbarkeit des 6GHz-Bandes von Wi-Fi 6E hängt von den regionalen Regelungseinstellungen ab, die 6GHz-Öffnungsbedingungen in Taiwan müssen überprüft werden.
- Abhängigkeit von Treiberupdates: Der out-of-tree Treiber von Realtek wird von der Community (morrownr) gepflegt, nach Kernel-Updates von DGX OS kann eine Neukompilierung erforderlich sein.
- Unterschiede in der Durchdringungstestfunktion: Die Injektionsfunktion der MediaTek mt76-Serie wurde im Kernel 6.x verbessert, aber RTL8812au bleibt die traditionelle Wahl der Durchdringungstest-Community.
- Bluetooth-Funktion: Die Bluetooth 5.2-Funktion von AWUS036AXM wurde auf DGX OS nicht weit verbreitet validiert (DGX Spark ist mit BT 5.4 ausgestattet).
- ⚠️ **RTL8832BU (AWUS036AX/AXER) Treiberpfleger hat eine Empfehlung gegen die Verwendung veröffentlicht**: Der Treiberpfleger morrownr hat in einer offiziellen Erklärung festgestellt, dass die rtl8852/32au-Serie "sehr schlechte Treiber sind und es wird vermutet, dass es Probleme mit dem Chip selbst gibt", empfiehlt Linux-Nutzern, derzeit wegzukommen (Quelle siehe Kapitel 10). Die in Kapitel 4 und 6 enthaltenen "⚠️ Verwendbar aber mit Vorsicht" Bewertungen sollten als Branchenconsens verstanden werden, dass eine Empfehlung gegen die Verwendung gegeben wird, und nicht nur ein Problem mit der Installation.
- In diesem Dokument zitierte RTL8812AU "out-of-tree" wurde als Anfang 2026 Information bewertet; tatsächlich wurde der mac80211-kompatible in-kernel Treiber für diesen Chip bereits in **kernel 6.13 in den Mainline aufgenommen und ab 6.14 qualitativ ausgereift** (offizielle Ankündigung von morrownr), wenn DGX OS 6.14+ Kerne verwendet, besteht für AWUS036ACH die Möglichkeit, ohne Kompilierung verwendet zu werden, empfehle ich, dass der Kundendienst vor der Antwort den Kunden auffordert, `uname -r` zu berichten, um zu bestätigen.

Widerspruchsbedingungen: Falls nach DGX OS-Updates die Kernel-Version oder die USB-Controller-Treiber geändert werden und der morrownr-Treiber die ARM64-Branchenpflege einstellt, muss das Kompatibilitätsmatrix in Kapitel 6 neu überprüft werden; falls die rtw89 USB-Unterstützung im Kernel 6.x offiziell vollständig implementiert wird, kann die Bewertung von AWUS036AX / AXER von "verwendbar aber mit Vorsicht" aufgestuft werden.

## 10. Referenzquellen URL

| Quelle | Beschreibung | URL | Überprüfungsstatus | Überprüfungsdatum |
|---|---|---|---|---|
| NVIDIA DGX Spark Offizielle Seite | DGX Spark Spezifikationen und Plattforminformationen | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Geprüft | 2026-09-03 |
| NVIDIA DGX Dokumentation | DGX OS Systemarchitektur und Kernel-Version | https://docs.nvidia.com/dgx/dgx-spark | ✅ Geprüft | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux Treiber (ARM64 Unterstützung) | https://github.com/morrownr/8812au-20210820 | ✅ Geprüft | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8811CU Linux Treiber | https://github.com/morrownr/8821cu-20210916 | ✅ Geprüft | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux Treiber | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Geprüft | 2026-09-03 |
| Linux kernel mt76 Treiberdokumentation | MediaTek mt76 / mt7921 Mainline Treiberbeschreibung (mit Unterstützung für verschiedene Chips und Kernel-Versionen) | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ Geprüft | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide (Yupitek) | ALFA AP-Modus-Einrichtung unter Linux | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Geprüft | 2026-09-03 |
| ALFA Network Produktübersicht (Yupitek) | ALFA aktuelle Produkt规格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ Geprüft | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | Offizielle Erklärung des Treiberpflegers: Empfehlung, RTL8852/32au (RTL8832BU) Chip zu vermeiden | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Geprüft | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | RTL8812AU Treiberstatus neueste Ankündigung (Kernel 6.13 in Mainline aufgenommen, 6.14 Qualitätsreif) | https://github.com/morrownr/8812au-20210820 | ✅ Geprüft | 2026-09-03 |

Verwandte Artikel: [Ist das ALFA Wireless Netzwerkadapter kompatibel mit MSI EdgeXpert](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)｜[Ist das ALFA Wireless Netzwerkadapter kompatibel mit ASUS Ascent GX10](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[Ist das ALFA Wireless Netzwerkadapter kompatibel mit ALTOS BrainSphere GB10 F1](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[Ist das ALFA Wireless Netzwerkadapter kompatibel mit GIGABYTE AI TOP ATOM](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[Ist das ALFA Wireless Netzwerkadapter kompatibel mit NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Haftungsausschluss: Die Kompatibilitätsbestimmungen basieren auf NVIDIA DGX OS (Kernel 6.x, aarch64). MediaTek Chips Treiber sind für Linux Mainline, stabil; Realtek Chips Treiber werden von der Community gepflegt (morrownr), die tatsächliche Stabilität kann mit der Version variieren. DGX Spark ist mit Wi-Fi 7 integriert, externe ALFA Netzwerkkarten werden hauptsächlich für Penetrationstests oder spezielle Chip-Gruppen verwendet. Die Qualität des USB-C Adapter kann den Benutzererlebnis direkt beeinflussen, daher wird empfohlen, Adapter mit Marke und Markierung USB 3.2 Gen 2×2 zu wählen.
