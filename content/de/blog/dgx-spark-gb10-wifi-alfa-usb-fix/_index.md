---
title: "DGX Spark WLAN-Probleme? In 10 Minuten gelöst mit dem ALFA USB-Adapter"
description: "WLAN-Probleme am NVIDIA DGX Spark in zehn Minuten lösen: Ein ALFA-USB-Adapter ohne Treiberinstallation hilft auch bei ASUS GX10 und anderen GB10-Servern."
date: 2026-05-20
author: "benny-lai"
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["dgx-spark", "gb10", "ai-server", "wifi", "alfa-network", "tutorial", "asus-ascent-gx10", "msi-edgexpert", "hp-zgx-nano", "altos-brainsphere", "gigabyte-ai-top-atom"]
featureimage: "/images/blog/dgx-spark-gb10-wifi-alfa-usb-fix.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
faq:
  - question: "Warum kann sich der DGX Spark nicht mit Wi-Fi verbinden?"
    answer: "Der DGX Spark verwendet den integrierten MediaTek MT7925 Wi-Fi 7-Chip, doch der wpa_supplicant im OOBE-Phase ist zu stark reduziert und mit bestimmten AP-Herstellern (insbesondere UniFi) inkompatibel. Eine Verbindung mit WPA2-Enterprise ist nahezu ausgeschlossen."
  - question: "Gilt die Lösung mit der ALFA USB-Netzwerkkarte für alle GB10 AI Server?"
    answer: "Ja. Alle AI Edge Server, die den NVIDIA GB10 Grace Blackwell Superchip verwenden (ASUS, MSI, HP, ALTOS, GIGABYTE), nutzen denselben MT7925 Wi-Fi-Chip. Die Lösung mit der ALFA AWUS036ACM sollte daher bei allen Modellen funktionieren (getestet nur auf dem ASUS GX10, andere Modelle wurden nicht einzeln getestet)."
  - question: "Muss der Treiber für die AWUS036ACM auf dem DGX Spark installiert werden?"
    answer: "Nein. Der mt76-Treiber für den MT7612U ist seit Linux Kernel 4.19 im Hauptzweig des Kernel-Quellbaums enthalten. Der Kernel 6.17+ von DGX OS unterstützt dies nativ vollständig, und der Treiber wird beim Einstecken in den USB-Anschluss automatisch geladen."
  - question: "Wie lange dauert die Behebung der Wi-Fi-Probleme mit der ALFA USB-Netzwerkkarte?"
    answer: "Weniger als zehn Minuten. Nach dem Anschließen über einen USB-C-auf-USB-A-Adapter an den USB-C-Port des GX10 lädt das System den Treiber automatisch. Die Verbindung zum WiFi kann anschließend durch Scannen und Herstellen der Verbindung über den nmcli-Befehl abgeschlossen werden. Es ist weder das Kompilieren eines Treibers noch ein Neustart erforderlich."
  - question: "Können Sie auf dem DGX Spark auch andere ALFA-Netzwerkkarten verwenden?"
    answer: "Ja. Wir haben auf dem ASUS GX10 (GB10, Ubuntu 24.04 ARM64, Kernel 6.17) alle 9 aktuellen ALFA-Adapter getestet: Alle verwenden die im Kernel integrierten Treiber, funktionieren direkt nach dem Einstecken und benötigen kein DKMS; der AWUS036ACH nutzt den integrierten Treiber rtw88_8812au. AWUS036AXM / AXML scheitern auf dem Stock-Kernel 6.17 jedoch bei der Paketinjektion und eignen sich nur für Verbindung und AP. Andere GB10-Modelle wurden nicht einzeln getestet."
---

> 📌 Dieser Artikel wurde anhand der GX10-Praxistests vom November 2026 aktualisiert: Auf dem ASUS GX10 (Ubuntu 24.04 ARM64, Kernel 6.17.0-1014-nvidia) laufen alle 9 aktuellen ALFA-Adapter mit den im Kernel integrierten Treibern – einstecken und loslegen, kein DKMS nötig. Alle Daten finden Sie in der [Testmatrix der 9 ALFA-Adapter unter ARM64](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Getestet wurde nur auf dem GX10; andere GB10-Modelle wurden nicht einzeln getestet.

Ihr lang erwarteter **NVIDIA DGX Spark** (Codename Project DIGITS) ist endlich angekommen.

{{< tldr >}}
Der integrierte MT7925 Wi-Fi 7-Chip der NVIDIA DGX Spark und aller GB10 AI Server weist bekannte Verbindungsdefekte auf. Die Lösung besteht darin, eine ALFA AWUS036ACM USB-Netzwerkkarte einzustecken. Der mt76-Treiber ist seit Kernel 4.19 im Kernel-Quellbaum enthalten, sodass DGX OS Kernel 6.17+ Plug-and-Play unterstützt und die Verbindung innerhalb von zehn Minuten hergestellt ist.
{{< /tldr >}}

Auspacken, Strom anschließen, der OOBE-Bildschirm (Ersteinrichtung) erscheint — alles läuft reibungslos. Sie wählen Ihr WLAN-Netzwerk, geben das Passwort ein, der Bildschirm dreht sich dreißig Sekunden lang...

**„Keine Verbindung zu diesem Netzwerk möglich."**

Nochmal versuchen. Neustart. Zurücksetzen. Immer noch Fehler.

Sie sind nicht allein. In den [NVIDIA Developer Foren](https://forums.developer.nvidia.com) beschweren sich **Dutzende von Threads** über genau dasselbe: Das WLAN des DGX Spark ist defekt.

Das ist kein Konfigurationsfehler. Das ist ein bekannter Konstruktionsfehler des DGX Spark.

---

## Ursache: Warum ist das DGX Spark WLAN so unzuverlässig?

Der DGX Spark — und jeder andere KI-Server, der auf dem **NVIDIA GB10 Grace Blackwell Superchip** basiert — verwendet den **MediaTek MT7925 Wi-Fi 7 Chip**. Auf dem Papier erstklassige Hardware.

Das Problem liegt in der Softwareschicht.

### Drei fatale Schwachstellen

**① Der OOBE WLAN-Supplicant ist zu stark reduziert**

Die Ersteinrichtung des DGX Spark verwendet einen minimalen `wpa_supplicant`, dem die meisten Enterprise-Authentifizierungsfunktionen fehlen. Dadurch kann die Association mit bestimmten Access Points — insbesondere Ubiquiti UniFi — überhaupt nicht abgeschlossen werden.

NVIDIA hat dieses Problem in den **DGX Spark Release Notes (Update April 2026)** ausdrücklich dokumentiert, und es ist zum Zeitpunkt dieses Artikels noch nicht behoben.

**② WPA2-Enterprise ist inkompatibel**

Wenn Ihr Büro oder Labor WPA2-Enterprise verwendet (in Unternehmensumgebungen üblich), wird das eingebaute WLAN des DGX Spark mit ziemlicher Sicherheit scheitern. Dies lässt sich nicht durch eine Konfigurationsdatei beheben — es handelt sich um eine doppelte Einschränkung auf Treiber- und Supplicant-Ebene.

**③ Zufällige „No Wi-Fi Adapter Found"-Fehler**

Mehrere Benutzer in den NVIDIA-Foren (Thread #356183) berichten, dass der DGX Spark während des normalen Betriebs plötzlich „Kein WLAN-Adapter gefunden" anzeigt und ein vollständiger Neustart erforderlich ist. Schlimmer noch: **Das System stellt nach einem Verbindungsabbruch keine automatische Wiederverbindung her** — Sie müssen `nmcli`-Befehle manuell ausführen.

| Problem | Auswirkung |
|------|------|
| OOBE kann keine Enterprise-APs verbinden | UniFi / WPA2-Enterprise — vollständig defekt |
| Zufälliger „No Wi-Fi Adapter Found" | Neustart erforderlich, unterbricht den Entwicklungs-Workflow |
| Keine automatische Wiederverbindung | Fernverwaltung wird unbrauchbar |
| Release Notes bestätigen das Problem | NVIDIA-offiziell, kein Einzelfall |

> 💡 **Die gute Nachricht: Während diese Softwareprobleme kurzfristig nicht vollständig behoben werden, gibt es eine einfache, stabile und vollständig kompatible Hardware-Lösung.**

---

## Nicht nur DGX Spark — Alle GB10 AI Edge Server teilen denselben WLAN-Chip

Der DGX Spark erhält die ganze Aufmerksamkeit, einfach weil es NVIDIAs eigene Marke ist und zuerst ausgeliefert wurde. Aber in Wirklichkeit verwendet **jeder AI Edge Server mit dem NVIDIA GB10 Grace Blackwell Superchip** genau denselben **MediaTek MT7925 Wi-Fi 7 Chip** — derselbe Treiber-Stack, dieselben `wpa_supplicant`-Einschränkungen, dieselben Kompatibilitätsprobleme.

Derzeit sind sechs GB10 AI Edge Server auf dem Markt erhältlich:

### GB10 AI Edge Server — Vollständiger Spezifikationsvergleich

Alle Modelle teilen diese Kernspezifikationen:

| Komponente | Spezifikation |
|----------|------|
| Superchip | **NVIDIA GB10 Grace Blackwell** |
| CPU | **20-Core Arm** (10× Cortex-X925 + 10× Cortex-A725) |
| GPU | **NVIDIA Blackwell GPU**, 5th Gen Tensor Cores / 4th Gen RT Cores |
| KI-Leistung | **1 PFLOP FP4** (1000 TOPS AI) |
| Systemspeicher | **128 GB LPDDR5x** Unified, 256-Bit, 273 GB/s Bandbreite |
| Speicherverbindung | **NVLink-C2C** (5× PCIe 5.0 Bandbreite) |
| NIC | **NVIDIA ConnectX-7** SmartNIC (200G × 2 QSFP) |
| Ethernet | **1× 10GbE RJ-45** |
| WLAN-Chip | **MediaTek MT7925** Wi-Fi 7 (2×2) |
| Bildschirmausgabe | **1× HDMI 2.1a** |
| Betriebssystem | **NVIDIA DGX OS** (Ubuntu Linux-basiert) |
| Stromversorgung | **240W** USB-C externes Netzteil |
| Dual-Unit Stacking | Unterstützt (bis zu 405B Parameter-Modelle) |

Hier sind die Unterschiede zwischen den Marken:

| Merkmal | **ASUS ASCENT GX10** | **MSI EdgeXpert** | **NVIDIA DGX Spark** | **HP ZGX Nano G1n** | **ALTOS BrainSphere GB10 F1** | **GIGABYTE AI TOP ATOM** |
|------|----------------------|-------------------|----------------------|---------------------|------------------------------|--------------------------|
| Speicher | 1TB / 2TB / 4TB NVMe | 1TB / 4TB NVMe | 1TB / 4TB NVMe | 1TB / 2TB / 4TB NVMe | 4TB NVMe | 1TB / 4TB NVMe (max. Gen5) |
| WLAN-Modul | AW-EM637 (Wi-Fi 7) | Wi-Fi 7 | Wi-Fi 7 | MT7925 (Wi-Fi 7) | Wi-Fi 7 | Wi-Fi 7 |
| Bluetooth | BT 5.4 | BT 5.3 | BT 5.4 | BT 5.4 | BT 5.4 LE | BT 5.4 |
| USB | 4× USB 3.2 Gen 2×2 Type-C | 4× USB 3.2 Type-C | 4× USB Type-C | 4× USB Type-C | 4× USB 3.2 Gen 2×2 Type-C | 4× USB 3.2 Gen 2×2 Type-C |
| Abmessungen | 150×150×51mm | 151×151×52mm | 150×150×50,5mm | 150×150×51mm | 150×150×50mm | 150×150×50,5mm |
| Gewicht | 1,48 kg | 1,2 kg | 1,2 kg | 1,25 kg | < 1,5 kg | 1,2 kg |
| Mitgelieferte Software | — | — | — | HP ZGX Toolkit | Altos aiGeni Plattform | — |

> ⚠️ **Fazit**: Egal welchen GB10 AI Edge Server Sie gekauft haben, das eingebaute WLAN ist derselbe MediaTek MT7925-Chip, und alle können auf dieselben Verbindungsprobleme stoßen. Die unten beschriebene ALFA USB-Adapter-Lösung **sollte mit allen sechs Modellen funktionieren** (getestet nur auf dem ASUS GX10, andere Modelle wurden nicht einzeln getestet).

---

## Die Lösung: Ein USB-WLAN-Adapter, zehn Minuten

NVIDIA testet offiziell nur DGX OS (basierend auf Ubuntu 24.04). **Alle GB10-Plattformen verwenden die ARM64 (aarch64) Architektur** mit Kernel **Version 6.17 oder neuer**.

Das bedeutet, Ihr USB-WLAN-Adapter muss drei Anforderungen erfüllen:

1. ✅ **Im Kernel integrierter Linux-Treiber** — keine Kompilierung, kein DKMS
2. ✅ **Volle ARM64 (aarch64) Unterstützung** — Plug-and-Play auf GB10
3. ✅ **Bewährte Stabilität** — von der Community umfassend validiert

Alle 9 aktuellen ALFA-USB-Adapter erfüllen auf dem im GX10-Test verwendeten Kernel 6.17 diese drei Punkte (GX10-Praxistest, siehe „Weitere ALFA-Adapter“ am Ende des Artikels). Dieser Artikel nimmt den AWUS036ACM als Beispiel, da er sich am besten als Verwaltungsnetzwerk eignet.

### 🥇 Empfehlung: ALFA AWUS036ACM

| Element | Detail |
|------|------|
| Chipsatz | **MediaTek MT7612U** |
| Treiber | **Linux Kernel integriertes mt76** (seit Kernel 4.19) |
| Frequenzbänder | Dual-Band 2,4 GHz + 5 GHz (AC1200) |
| Antenne | 2× RP-SMA abnehmbar 5 dBi (aufrüstbar) |
| Schnittstelle | USB 3.0 Type-A |
| Monitor-Modus | ✅ Volle Unterstützung |
| AP-Modus | ✅ Unterstützt |
| TAA-konform | ✅ Erfüllt US-Behörden-Beschaffungsstandards |

#### Warum dieser? Sechs Gründe

**1. Plug-and-Play ohne Treiberinstallation**

Der mt76-Treiber ist seit Version 4.19 Teil des mainline Linux Kernels. Der Kernel 6.17 des DGX Spark unterstützt ihn nativ. In einen USB-Port einstecken, und das System **lädt den Treiber automatisch** — Sie installieren nichts.

**2. Auf ARM64 in der Praxis getestet**

Der MT7612U wurde jahrelang auf ARM-Plattformen getestet — Raspberry Pi OS (aarch64), Ubuntu Server (ARM64) und mehr. Wir haben ihn außerdem auf dem ASUS GX10 mit GB10-Plattform (Kernel 6.17) getestet: Nach dem Einstecken wird `mt76x2u` automatisch geladen, Patches sind nicht nötig.

**3. Keine Kompilierung, keine Konfiguration**

Der mt76-Treiber ist seit Jahren im Mainline-Kernel; auch nach einem Kernel-Update von DGX OS funktioniert der ACM weiterhin per Plug-and-Play. (Die Realtek-Modelle benötigen auf Kernel 6.17 ebenfalls keine Kompilierung; die Mindestversion unterscheidet sich je Adapter, nur darunter ist DKMS nötig.)

**4. Unterstützt Monitor-Modus und Paketinjektion**

Wenn Sie Kali Linux VMs auf Ihrem DGX Spark für Sicherheitsforschung betreiben möchten, unterstützt der ACM Monitor-Modus, Paketinjektion und virtuelle Schnittstellen (VIF). Im GX10-Test lag die Injection-Erfolgsquote bei 2,4 GHz 63–83 % und 5 GHz 76 %; wenn Injection der Hauptzweck ist, schneiden AWUS036EACS und ACH (beide Bänder 100 %) besser ab.

**5. Austauschbare Antennen**

Zwei abnehmbare RP-SMA-Antennen. Wird mit 5 dBi geliefert, und Sie können bei Bedarf auf 7 dBi oder 9 dBi High-Gain-Antennen aufrüsten — perfekt für Edge-Bereitstellungen in Serverräumen oder Fabriken mit schwachen WLAN-Signalen.

**6. TAA-Konformität**

Wenn Ihre Organisation behördliche Beschaffungsanforderungen hat, ist der ALFA AWUS036ACM einer der wenigen externen USB-WLAN-Adapter mit **TAA-Konformität**.

---

## Praxisanleitung: In 10 Minuten von „Kein WLAN" zu Dual-Netzwerk

Hier ist der komplette Workflow für die Verwendung des ALFA AWUS036ACM auf Ihrem DGX Spark:

### Schritt 1: USB-Adapter einstecken

Die USB-Ports des DGX Spark sind alle USB-C; stecken Sie den AWUS036ACM daher über einen USB-C-auf-USB-A-Adapter (mit Datenübertragung) ein.

Öffnen Sie ein Terminal und führen Sie aus:

```bash
dmesg | tail -20
```

Sie sollten eine ähnliche Ausgabe sehen:

Die folgende dmesg-Ausgabe stammt aus einem Test der AWUS036ACM auf einem ASUS GX10 (Kernel 6.17.0-1014-nvidia); die MAC-Adresse ist maskiert:

```
usb 5-1: new high-speed USB device number 2 using xhci-hcd
usb 5-1: New USB device found, idVendor=0e8d, idProduct=7612, bcdDevice= 1.00
mt76x2u 5-1:1.0: ASIC revision: 76120044
mt76x2u 5-1:1.0: ROM patch build: 20141115060606a
mt76x2u 5-1:1.0: Firmware Version: 0.0.00
usbcore: registered new interface driver mt76x2u
mt76x2u 5-1:1.0 wlxXXXXXXXXXXXX: renamed from wlan0
```

**Das ist das Signal, dass der Treiber automatisch geladen wurde.** Sie haben nichts installiert.

### Schritt 2: Bestätigen, dass der Adapter erkannt wird

```bash
nmcli device status
```

Sie sollten `wlan1` (oder `wlx...`) mit dem Status `disconnected` in der Liste sehen.

### Schritt 3: Mit WLAN verbinden

```bash
# Verfügbare Netzwerke scannen
nmcli device wifi list

# Mit Ihrer SSID verbinden (ersetzen Sie „MyLabWiFi")
sudo nmcli device wifi connect "MyLabWiFi" password "your-password"

# Verbindungsstatus überprüfen
nmcli connection show --active
```

### Schritt 4: Automatische Verbindung beim Start aktivieren

Wenn der vorherige Schritt erfolgreich war, speichert `nmcli` das Verbindungsprofil automatisch. Es wird bei jedem weiteren Start automatisch verbunden.

Überprüfen, ob das Profil gespeichert ist:

```bash
nmcli connection show
```

Sehen Sie Ihre SSID in der Liste — fertig. Vom Einstecken des USB-Adapters bis zur stabilen WLAN-Verbindung **dauert es insgesamt weniger als zehn Minuten**.

---

## Das ist eine echte KI-Server-Netzwerkarchitektur

Mit dem AWUS036ACM wird Ihr DGX Spark-Netzwerk-Setup zu einer professionellen **Dual-Netzwerk-Architektur** aufgewertet:

{{< mermaid >}}
%%{init:{"theme":"dark","themeVariables":{"primaryColor":"#2d1f4e","primaryTextColor":"#e2d9f3","primaryBorderColor":"#7c3aed","lineColor":"#9d6dff","secondaryColor":"#1a1030","tertiaryColor":"#0e0818","background":"#0e0818","mainBkg":"#1e1040","nodeBorder":"#7c3aed","clusterBkg":"#150d2a","titleColor":"#c4b5fd","edgeLabelBackground":"#1a1030","attributeBackgroundColorEven":"#1e1040","attributeBackgroundColorOdd":"#150d2a"}}}%%
flowchart TD
    subgraph sub1["🌐 Netzwerkebene"]
        direction LR
        A["⚡ 10GbE / ConnectX-7<br/>Modelltraining · Große Datenübertragung"]
        B["📡 ALFA AWUS036ACM<br/>SSH-Verwaltung · Jupyter · Systemupdates"]
    end

    C["🖥️ DGX Spark / GB10<br/>ARM64 | 128GB | 20-Core CPU"]

    subgraph sub2["🎯 Anwendungsfälle"]
        D["🤖 KI-Entwickler<br/>Inferenz + SSH parallel"]
        E["🔐 Sicherheitslabor<br/>LLM-Training + Penetrationstests"]
        F["🚀 Edge-Bereitstellung<br/>Produktionsnetzwerk + Isoliertes Management"]
    end

    A -->|Hochgeschwindigkeitsdaten| C
    B -->|Management-Link| C
    C --> D
    C --> E
    C --> F
{{< /mermaid >}}

**Warum den Datenverkehr aufteilen?**

KI-Modelltraining erzeugt massiven Netzwerkverkehr — Herunterladen vortrainierter Gewichte, Synchronisieren von Datensätzen, verteilte Trainingskommunikation. Wenn Sie dies mit SSH-Verwaltung auf derselben Leitung mischen:

- SSH-Sitzungen werden träge oder laufen in Timeout
- 10GbE-Bandbreite wird durch Verwaltungsverkehr verschwendet
- Wenn die Hauptverbindung ausfällt (z.B. beim Hängenbleiben eines Modell-Downloads), können Sie nicht einmal remote darauf zugreifen, um es zu beheben

Mit der Aufteilung **bleibt Ihre Verwaltungsverbindung unabhängig von der Modell-Workload stabil**.

---

## Drei Szenarien, ein Adapter

### Szenario A: KI-Entwickler
```
10GbE → Modellinferenz, Datentransfer
ALFA ACM → SSH, Jupyter Notebook, Systemupdates
```

### Szenario B: Sicherheitsforschungslabor (nur in eigenen oder ausdrücklich autorisierten Netzwerken)
```
GB10 → LLM-Feinabstimmung ausführen
Kali Linux VM → USB-Durchleitung ALFA ACM → Drahtlose Penetrationstests
```

### Szenario C: Edge-Bereitstellung (Fabrik / Lager)
```
10GbE → Produktionsnetzwerk
ALFA ACM + High-Gain-Antennen → Büro-Verwaltungs-WLAN
```

---

## FAQ

**F: Der MT7612U des AWUS036ACM und der eingebaute MT7925 des GB10 sind doch beide von MediaTek — sind sie nicht dasselbe?**

A: Gleicher Hersteller, völlig unterschiedliche Treiberarchitektur. Der MT7925 verwendet den `mt7925e`-Treiber, einen neueren PCIe-Schnittstellentreiber, der noch verfeinert wird. Der MT7612U verwendet den `mt76` USB-Treiber, der seit Kernel 4.19 ausgereift und extrem stabil ist.

**F: Funktioniert dieser Adapter auch außerhalb von DGX OS?**

A: Absolut. Der MT7612U-Treiber ist Teil des mainline Linux Kernels — Ubuntu, Debian, Raspberry Pi OS, Kali Linux, Fedora, Arch Linux — alles mit Kernel 4.19 oder neuer. Plug-and-Play auf allen.

---

## Weitere ALFA-Adapter: Ergebnisse des GX10-Praxistests

Wir haben auf dem ASUS GX10 (Ubuntu 24.04 ARM64, Kernel 6.17.0-1014-nvidia) alle 9 aktuellen ALFA-Adapter getestet: Alle verwenden die im Kernel integrierten Treiber, funktionieren direkt nach dem Einstecken und benötigen kein DKMS. Andere GB10-Modelle (DGX Spark, MSI EdgeXpert, GIGABYTE AI TOP ATOM, ALTOS BrainSphere, HP ZGX Nano) nutzen denselben GB10-Chip und dieselbe NVIDIA-Kernel-Reihe; wir erwarten dasselbe Verhalten, sie wurden jedoch nicht einzeln getestet.

| Modell | Chip | Integrierter Treiber | Packet Injection (GX10-Test) | Geeignet für |
|------|------|----------|----------------------|----------|
| AWUS036ACM | MediaTek MT7612U | mt76x2u | ✅ 2.4G 63–83 % / 5G 76 % | Verwaltungsnetzwerk, AP, Penetrationstests |
| AWUS036ACHM | MediaTek MT7610U | mt76x0u | ⚠️ 2.4G 96–100 % / 5G nur Broadcast | Verwaltungsnetzwerk, AP |
| AWUS036ACH | Realtek RTL8812AU | rtw88_8812au | ✅ beide Bänder 100 % | Penetrationstests, Empfang über große Entfernungen |
| AWUS036ACS | Realtek RTL8811AU | rtw88_8821au | ✅ 2.4G 100 % / 5G 96 % | Penetrationstests, mobiler Einsatz |
| AWUS036EACS | Realtek RTL8821CU (mit Bluetooth) | rtw88_8821cu | ✅ beide Bänder 100 % | Penetrationstests |
| AWUS036AX | Realtek RTL8832BU | rtw89_8852bu | ✅ 2.4G 96 % | Wi-Fi-6-Verbindung, AP |
| AWUS036AXER | Realtek RTL8832BU | rtw89_8852bu | ✅ 2.4G 73 % | Wi-Fi-6-Verbindung, AP, Monitor-Empfang |
| AWUS036AXM | MediaTek MT7921AUN | mt7921u | ❌ Fehlgeschlagen | Nur Verbindung, AP |
| AWUS036AXML | MediaTek MT7921AUN | mt7921u | ❌ Fehlgeschlagen | Nur Verbindung, AP (6 GHz im Test nutzbar) |

AWUS036AXM / AXML scheitern auf dem Stock-Kernel 6.17 bei der Paketinjektion (Monitor, AP und WPA3 funktionieren) und eignen sich nicht für Penetrationstests. Die Kernel-Version, ab der die Treiber im Mainline-Kernel enthalten sind, unterscheidet sich je Adapter (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); nur darunter sind DKMS-Treiber der Community nötig. Alle Daten finden Sie in der [Testmatrix der 9 ALFA-Adapter unter ARM64](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

---

{{< faq >}}

## Zusammenfassung: Egal welchen GB10 Sie haben, in 10 Minuten online

Ob Sie einen NVIDIA DGX Spark, ASUS ASCENT GX10, MSI EdgeXpert, HP ZGX Nano, ALTOS BrainSphere GB10 F1 oder GIGABYTE AI TOP ATOM gekauft haben — diese GB10 AI Edge Server sind phänomenale KI-Entwicklungsmaschinen: 128 GB Unified Memory, 20-Core ARM CPU, ConnectX-7 200GbE-Netzwerk. Aber sie alle teilen denselben MediaTek MT7925 WLAN-Chip und können alle am selben ersten Schritt scheitern.

Die ALFA AWUS036ACM-Lösung ist fast absurd einfach: **Einstecken, fertig.**

Aber genau diese Einfachheit ist es, was echte Engineering-Produktivität ausmacht — Sie sollten keine WLAN-Treiber debuggen. Sie sollten Modelle trainieren.

Im Vergleich zu anderen Ansätzen ist der Vorteil klar:

| Ansatz | Zeit | Zuverlässigkeit | Wartung |
|------|------|--------|---------|
| Warten auf NVIDIA WLAN-Treiber-Fix | Unbekannt (Monate?) | Unsicher | Gering |
| Einen WLAN-Bridge kaufen | 30 Min Einrichtung | Mittel | Mittel |
| **ALFA AWUS036ACM** | **< 10 Min** | **Höchste** | **Null** |

Zehn Minuten, ein USB-Adapter, und Ihr KI-Server ist wirklich online.

---

> 📌 **ALFA AWUS036ACM auf Lager** → [Yopitek Produktseite](/de/products/alfa/awus036acm/)
>
> Yopitek Ltd ist autorisierter ALFA Network Distributor in Taiwan
> Für Bestellungen oder technische Anfragen: sales@yupitek.com

---

*Quellen: NVIDIA DGX Spark Release Notes, NVIDIA Developer Foren, morrownr/USB-WiFi GitHub, ALFA Network Docs, Linux Kernel Wireless Documentation*

## Referenzen

1. [NVIDIA DGX Spark Offizielle Dokumentation](https://developer.nvidia.com/dgx-spark)
2. [NVIDIA Developer Forums](https://forums.developer.nvidia.com/)
3. [morrownr/USB-WiFi GitHub-Projekt](https://github.com/morrownr/USB-WiFi)
4. [Linux Kernel Wireless Documentation](https://wireless.wiki.kernel.org/)
5. [ALFA Network Offizielle Website](https://www.alfa.com.tw/)
