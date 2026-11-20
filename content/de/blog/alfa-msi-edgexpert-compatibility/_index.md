---
title: "Ist der ALFA WLAN-Adapter mit dem MSI EdgeXpert (GB10) kompatibel?"
date: 2026-09-03
draft: false
slug: "alfa-msi-edgexpert-compatibility"
tags:
  - "ALFA"
  - "MSI"
  - "EdgeXpert"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "Hardware-Leitfaden"
description: "ALFA-WLAN-Adapter am MSI EdgeXpert (GB10): Im GX10-Test laufen alle 9 Karten mit Kernel-Treibern ohne DKMS, nur AXM/AXML scheitern bei der Injection."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Dieser Artikel wurde anhand der GX10-Praxistests vom November 2026 aktualisiert: Auf dem ASUS GX10 (Ubuntu 24.04 ARM64, Kernel 6.17.0-1014-nvidia) laufen alle 9 aktuellen ALFA-Adapter mit den im Kernel integrierten Treibern – einstecken und loslegen, kein DKMS nötig. Alle Daten finden Sie in der [Testmatrix der 9 ALFA-Adapter unter ARM64](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Getestet wurde nur auf dem GX10; andere GB10-Modelle wurden nicht einzeln getestet.

## 1. Problemübersicht

Kundenfrage: „Können die USB-WLAN-Adapter der ALFA-Serie am KI-Supercomputer MSI EdgeXpert (NVIDIA GB10 Grace Blackwell) verwendet werden?“

Kurzfazit: Der MSI EdgeXpert und der NVIDIA DGX Spark nutzen denselben GB10-Chip und dieselbe NVIDIA-Kernel-Reihe. Wir haben auf dem ASUS GX10 (Ubuntu 24.04 ARM64, Kernel 6.17.0-1014-nvidia) alle 9 aktuellen ALFA-USB-WLAN-Adapter (AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML) getestet: Alle verwenden die im Kernel integrierten Treiber, funktionieren direkt nach dem Einstecken und benötigen weder Kompilierung noch DKMS. Wir erwarten dasselbe Verhalten, getestet wurde jedoch nur auf dem GX10; der MSI EdgeXpert selbst wurde nicht getestet. Funktionsunterschiede: Die MediaTek-MT7921-Modelle (AWUS036AXM / AXML) scheitern auf dem Stock-Kernel 6.17 bei der Paketinjektion (Packet Injection); Monitor-Modus, AP und WPA3 funktionieren. Bei den übrigen 7 Modellen wurden Monitor-Modus und Injection erfolgreich getestet. Die Kernel-Version, ab der die Treiber im Mainline-Kernel enthalten sind, unterscheidet sich je Adapter (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); nur ältere Kernel unterhalb dieser Version benötigen die DKMS-Treiber der Community. Hinweis: Die 4 USB-Ports des EdgeXpert sind alle USB Type-C (20Gbps); die ALFA-Adapter (außer AXML) benötigen einen USB-C-auf-USB-A-Adapter.

Bewertungsgrundlage: die 9 aktuellen USB-WLAN-Adapter von ALFA (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analyse der Zielhardware-Spezifikation

### 2.1 MSI EdgeXpert Hardware-Spezifikation

| Punkt | Spezifikation |
|---|---|
| Produktname | MSI EdgeXpert (Modell: EdgeXpert-MS-C931 / 59STW u.v.m.) |
| Hauptprozessor | NVIDIA GB10 Grace Blackwell Superchip (DGX Spark-Plattform) |
| CPU | 20-Kern Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | NVIDIA Blackwell-Architektur, 6144 CUDA-Kerne, fünfte Generation Tensor Core, vierte Generation RT Core |
| AI-Leistung | Bis zu 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| System-Speicher | 128GB LPDDR5x Unified Memory (256-bit, 273 GB/s) |
| Speicher | 1TB oder 4TB NVMe M.2 SSD (verschlüsselt, PCIe Gen5) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (bis zu 20Gbps) |
| Displayausgang | 1× HDMI 2.1a (4× DP1.4a über USB-C Alt Mode) |
| Netzwerk | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (QSFP 200GbE, System-zu-System-Interkonnektion) |
| WLAN | Wi-Fi 7 + Bluetooth 5.4 |
| Betriebssystem | NVIDIA DGX OS (basierend auf Ubuntu Linux, Kernel 6.x) |
| Architektur | aarch64 (ARM64) |
| Abmessungen | 151 × 151 × 52 mm (ca. 5.95" × 5.95" × 2.05") |
| Gewicht | Ca. 1.2 kg (2.65 lbs) |
| Stromversorgung | 240W USB-C Netzteil |
| Version | Verbraucher-Version / Industrieversion (EdgeXpert-MS-C931, Breittemperatur / Industriestufe) |

### 2.2 Softwareumgebung: NVIDIA DGX OS

Der MSI EdgeXpert wird mit NVIDIA DGX OS ausgeliefert, identisch mit DGX Spark / ASUS GX10:

| Punkt | Beschreibung |
|---|---|
| Basis | Ubuntu Linux (von NVIDIA angepasst) |
| Kernel | Linux 6.x |
| Architektur | aarch64 (ARM64) |
| Vorinstallierte Software | NVIDIA-KI-Softwarepaket (CUDA, cuDNN, TensorRT, PyTorch, Jupyter u. v. m.) |
| Paketverwaltung | apt |

### 2.3 Unterschiede zum DGX Spark

Der MSI EdgeXpert ist eine OEM-Version der DGX-Spark-Plattform mit identischer Hardware und Software:

| Punkt | MSI EdgeXpert | NVIDIA DGX Spark |
|---|---|---|
| Gehäuse | MSI-eigenes Gehäuse, optional als Industrieversion | NVIDIA-Referenzgehäuse |
| Speicheroptionen | 1TB / 4TB | Bis zu 4TB |
| Zielmarkt | Edge-KI / industrielle KI / Desktop-Entwicklung | Desktop-KI-Entwicklung |
| Zubehör | MSI-Originalzubehör | NVIDIA-Originalzubehör |

Auswirkung auf die ALFA-Kompatibilität: Voraussichtlich keine (getestet nur auf dem GX10, andere GB10-Modelle wurden nicht einzeln getestet). USB-Controller, Kernel-Version und Treiber-Framework sind mit dem DGX Spark identisch.

### 2.4 Bedarf an USB-Type-C-Adaptern

Die 4 USB-Ports des EdgeXpert sind alle Type-C. Alle ALFA-Adapter (außer dem AXML mit USB-C) haben USB Type-A; ein Adapter ist daher erforderlich. Wir empfehlen einen Adapter mit Unterstützung für USB 3.2 Gen 2×2 (20Gbps).

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
| WLAN-Internet für Edge-KI-Gateways | Alle 9 Modelle (z. B. AWUS036ACM / ACHM) | Alle mit integriertem Kernel-Treiber, einstecken und loslegen |
| WLAN-Penetrationstests in Industrieumgebungen | AWUS036EACS / ACH / ACS | Injection im Test 96–100 %, WPA-Handshake End-to-End erfassbar; AXM / AXML nicht wählen (Injection scheitert) |
| Wi-Fi 6 + AP-Hotspot | AWUS036AX / AXER | 2x2, AP mit 80 MHz im Test nutzbar |
| 6-GHz-Band | AWUS036AXML | Im Test WPA3-AP auf 6 GHz möglich; AXM hat denselben Chip, 6 GHz aber nicht getestet |
| Kein externes WLAN nötig | — | Der EdgeXpert hat integriertes Wi-Fi 7; für normale Internetnutzung ist kein externer Adapter nötig |

## 5. Umgebungsanforderungen

### 5.1 Hardwareanforderungen

| Punkt | Anforderung |
|---|---|
| USB-Adapter | USB-C-auf-USB-A-Adapter oder -Kabel (außer AXML), empfohlen mit USB 3.2 Gen 2×2 |
| Stromversorgung | Original-240W-USB-C-Netzteil des MSI EdgeXpert |

### 5.2 Softwareanforderungen

| Punkt | Anforderung |
|---|---|
| DGX-OS-Version | Jede aktuelle Version (Kernel 6.x) |
| Kernel-Version | Kernel 6.17 (getestet mit 6.17.0-1014-nvidia) enthält die Treiber aller 9 Adapter, keine Build-Tools nötig; die Mindestversion unterscheidet sich je Adapter (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), nur darunter ist ein DKMS-Treiber der Community nötig |
| WLAN-Verwaltungstools | iw, network-manager (in DGX OS vorinstalliert) |

## 6. Kompatibilitätsbewertung

### Aktuelle ALFA-Modelle × MSI EdgeXpert (GB10): Kompatibilitätsmatrix

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

Bewertungsgrundlage: Praxistests vom 16. bis 18.11.2026 auf dem ASUS GX10 (Ubuntu 24.04 ARM64, Kernel 6.17.0-1014-nvidia), getestet mit eigenem WLAN und eigenem Smartphone. Der MSI EdgeXpert nutzt denselben GB10-Chip und dieselbe NVIDIA-Kernel-Reihe; wir erwarten dasselbe Verhalten, getestet wurde jedoch nur auf dem GX10, der MSI EdgeXpert selbst wurde nicht getestet. Alle Daten finden Sie in der [Testmatrix der 9 ALFA-Adapter unter ARM64](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 7. Detaillierte Schritt-für-Schritt-Installation

Die Installation auf dem MSI EdgeXpert sollte mit der auf dem NVIDIA DGX Spark identisch sein (die Schritte wurden auf dem GX10 getestet). Hier folgt eine Kurzfassung; die vollständige Anleitung finden Sie in Kapitel 7 des Artikels [Ist der ALFA WLAN-Adapter mit dem NVIDIA DGX Spark kompatibel?](/de/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 MediaTek-Modelle (AWUS036ACM / ACHM / AXM / AXML)

**Schritt 1: Adapter einstecken**

Stecken Sie den ALFA-Adapter über einen USB-C-auf-USB-A-Adapter (AXML direkt) in einen USB-C-Port des EdgeXpert.

**Schritt 2: USB-Erkennung prüfen**

```bash
lsusb
# Beispiel für die erwartete Ausgabe (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Schritt 3: Netzwerkschnittstelle prüfen**

```bash
ip link show
# Eine Schnittstelle, die mit wlx beginnt, sollte automatisch erscheinen (in-kernel-Treiber wird automatisch geladen)
```

**Schritt 4: Mit dem WLAN verbinden**

```bash
nmcli dev wifi connect "SSID" password "Passwort"
```

### 7.2 Realtek-Modelle (AWUS036ACH / ACS / EACS / AX / AXER)

Kernel 6.17 (die im GX10-Test verwendete Version) enthält die Treiber aller Realtek-Modelle; die Schritte sind dieselben wie bei den MediaTek-Modellen, eine Kompilierung ist nicht nötig (Mindestversionen: EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17):

```bash
# 1. Kernel-Version prüfen (ab 6.17 sind die Treiber aller Realtek-Modelle integriert; GX10 im Test: 6.17.0-1014-nvidia)
uname -r

# 2. Nach dem Einstecken des Adapters prüfen, ob der Treiber automatisch geladen wurde
lsusb
lsmod | grep -E "rtw88|rtw89"
ip link show

# 3. Mit dem WLAN verbinden
nmcli dev wifi connect "SSID" password "Passwort"
```

Automatisch geladene Module je Modell: ACH → `rtw88_8812au`, ACS → `rtw88_8821au`, EACS → `rtw88_8821cu`, AX / AXER → `rtw89_8852bu`. Nur wenn `uname -r` unter der Mindestversion des jeweiligen Adapters liegt (ältere Systeme), ist ein von der Community gepflegter DKMS-Treiber nötig (z. B. morrownr/8812au-20210820 für den RTL8812AU).

### 7.3 Monitor-Modus (Penetrationstest)

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

## 8. Häufige Fehler und ihre Behebung

| Symptom | Mögliche Ursache | Fehlerbehebung |
|---|---|---|
| lsusb zeigt keinen ALFA-Adapter an | Defekter USB-C-Adapter / reiner Ladeadapter | Durch einen Adapter mit Datenübertragung ersetzen, z. B. USB 3.2 Gen 2×2; anderen USB-C-Port ausprobieren |
| MediaTek-Chip ohne wlan-Schnittstelle | Modul nicht automatisch geladen / Firmware fehlt | `sudo modprobe mt76x2u`; `sudo apt install linux-firmware`; `dmesg | grep mt76` prüfen |
| Realtek-Adapter ohne wlan-Schnittstelle nach dem Einstecken | Kernel unter der Mindestversion des Adapters (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), passender Treiber nicht integriert | Version mit `uname -r` prüfen; Kernel aktualisieren oder auf dem alten Kernel den DKMS-Treiber der Community installieren |
| Nach wiederholtem Wechsel zwischen Monitor/AP werden keine Signale mehr gefunden | RX-Stillstand (RX stall) | Adapter ab- und wieder anstecken, damit USB neu enumeriert |
| EACS/AXML ohne wlx-Schnittstelle nach erneutem Einstecken | Probe des Bluetooth-+-WLAN-Kombigeräts hängt | An einem anderen USB-Port erneut einstecken |
| WLAN-Geschwindigkeit ist langsam | Adapter unterstützt nur USB 2.0 | Durch einen Adapter mit USB 3.2 Gen 2×2 ersetzen |
| Konflikt zwischen internem Wi-Fi 7 und externem Adapter | Routing-Konflikt | Mit `sudo nmcli radio wifi off` das interne WLAN deaktivieren, bevor Sie den externen Adapter verwenden |
| Instabil bei hohen Temperaturen in Industrieumgebungen | Kühlung / Unterschiede zwischen Industrie- und Standardversion | Industrieversion des EdgeXpert (MS-C931) verwenden; sicherstellen, dass die Umgebungsbedingungen innerhalb der Spezifikation liegen |

## 9. Bekannte Einschränkungen

- Bedarf an USB-Type-C-Adaptern: Alle ALFA-Adapter außer dem AXML benötigen einen USB-C-auf-USB-A-Adapter
- Injection scheitert bei MT7921-Modellen: AWUS036AXM / AXML scheitern auf dem Stock-Kernel 6.17 bei der Paketinjektion, Deauth und Handshake-Erfassung sind nicht möglich; Monitor, AP und WPA3 funktionieren. Hauptursache ist eine mac80211-chanctx-Regression ab Kernel 6.16; gepatchte Community-Treiber sind weiterhin ratenbegrenzt
- Testumfang: Getestet nur auf dem ASUS GX10 (Kernel 6.17.0-1014-nvidia); der MSI EdgeXpert wurde nicht getestet, dasselbe Verhalten wird erwartet
- hcxdumptool nicht nutzbar: Alle Adapter außer dem EACS auf 2,4 GHz melden `failed to arm`; verwenden Sie stattdessen airodump-ng + aireplay-ng
- Mögliche Konflikte mit dem integrierten Wi-Fi 7: Der EdgeXpert hat bereits Wi-Fi 7 + BT 5.4 integriert
- AP-Modus muss manuell eingerichtet werden: DGX OS ist standardmäßig als Entwicklungsumgebung konfiguriert
- 6-GHz-Regulierung: Die Verfügbarkeit von Wi-Fi 6E hängt von der Regulierungsdomäne ab
- Ältere Kernel: Nur Systeme mit einem Kernel unter der Mindestversion des Adapters (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17) benötigen für die Realtek-Modelle DKMS-Treiber der Community, die nach jedem Kernel-Update neu kompiliert werden müssen
- Die Industrieversion beeinflusst die Kompatibilität nicht: Die MSI-Industrieversion (MS-C931) hat dieselbe Hardware-Spezifikation wie die Verbraucherversion, die USB-WLAN-Kompatibilität ist identisch

Widerlegungsbedingungen: Ändert sich die offizielle MSI-Spezifikation (geänderte USB-Ports, Kernel-Version unter 6.x) oder zeigt sich in der Praxis, dass mt76x2u / mt7921u unter DGX OS nicht automatisch geladen werden, muss die Kompatibilitätsmatrix in Kapitel 6 neu geprüft werden; ändert sich nach einem NVIDIA-Kernel-Update das Verhalten der integrierten Treiber, ist ein erneuter Praxistest nötig.

## 10. Referenzquellen (URL)

| Quelle | Beschreibung | URL | Prüfstatus | Prüfdatum |
|---|---|---|---|---|
| MSI EdgeXpert offizieller Online-Shop (US) | Spezifikationen der EdgeXpert-Verbraucherversion | https://us-store.msi.com/MSI-EdgeXpert-Blackwell-AI-Supercomputer | ✅ Geprüft | 2026-09-03 |
| MSI EdgeXpert Online-Shop (TW) | Spezifikationen der EdgeXpert-Verbraucherversion (23STW) | https://tw-store.msi.com/products/edgexpert-23stw-bgb104tg4 | ✅ Geprüft | 2026-09-03 |
| Offizielle Ankündigung von MSI IPC (Industrie-PCs) | Informationen zur Markteinführung des EdgeXpert | https://ipc.msi.com/en/news/146241 | ✅ Geprüft | 2026-09-03 |
| NVIDIA DGX Spark offizielle Seite | Informationen zur GB10-Plattform | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Geprüft | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU-Linux-Treiber | https://github.com/morrownr/8812au-20210820 | ✅ Geprüft | 2026-09-03 |
| ALFA Network Produktübersicht (Yopitek) | Spezifikationen der aktuellen ALFA-Produkte | /de/products/alfa/ | ✅ Geprüft | 2026-09-03 |
| Testmatrix der 9 ALFA-Adapter unter ARM64 (Yopitek) | Praxistest auf ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Praxistest | 2026-11-18 |

Verwandte Artikel: [Ist der ALFA WLAN-Adapter mit dem NVIDIA DGX Spark kompatibel?](/de/blog/alfa-nvidia-dgx-spark-compatibility/) | [Ist der ALFA WLAN-Adapter mit dem ASUS Ascent GX10 (GB10) kompatibel?](/de/blog/alfa-asus-ascent-gx10-compatibility/) | [Ist der ALFA WLAN-Adapter mit dem ALTOS BrainSphere GB10 F1 kompatibel?](/de/blog/alfa-altos-brainsphere-gb10-compatibility/) | [Ist der ALFA WLAN-Adapter mit dem GIGABYTE AI TOP ATOM kompatibel?](/de/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [Ist der ALFA WLAN-Adapter mit dem NVIDIA Jetson Nano kompatibel?](/de/blog/alfa-nvidia-jetson-nano-compatibility/)

Haftungsausschluss: Die Kompatibilitätsbewertung in diesem Artikel basiert auf Praxistests vom November 2026 auf dem ASUS GX10 (Ubuntu 24.04 ARM64, Kernel 6.17.0-1014-nvidia). Der MSI EdgeXpert nutzt denselben GB10-Chip und dieselbe NVIDIA-Kernel-Reihe wie der GX10; wir erwarten dasselbe Verhalten, er wurde jedoch nicht einzeln getestet. Der im GX10-Test verwendete Kernel 6.17 enthält die Treiber aller 9 ALFA-Adapter (die Mindestversion unterscheidet sich je Adapter); nur bei einem Kernel unterhalb dieser Mindestversion sind die DKMS-Treiber der Community nötig. Der EdgeXpert hat bereits integriertes Wi-Fi 7; externe ALFA-Adapter dienen vor allem Penetrationstests oder speziellen Chipsatz-Anforderungen. Monitoring und Injection nur in eigenen oder ausdrücklich autorisierten Netzwerken.
