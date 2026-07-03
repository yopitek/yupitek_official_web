---
title: "ALFA AWUS036ACH vs. AWUS036ACM: Vollständiger Vergleich für Kali Linux (2026)"
description: "Detaillierter Vergleich von ALFA AWUS036ACH und AWUS036ACM — Chipsätze, Monitor-Modus, Paket-Injektion, Treiber-Support und welcher besser für Kali Linux Penetrationstests geeignet ist."
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "AWUS036ACM", "Vergleich", "kali-linux", "RTL8812AU", "MT7612U"]
series: ["alfa-china-install-guide"]
series_order: 10
slug: "awus036ach-vs-awus036acm"
featureimage: "/images/blog/awus036ach-vs-awus036acm.webp"
faq:
  - question: "Gibt es Unterschiede bei der Treiberinstallation zwischen dem AWUS036ACH und dem AWUS036ACM?"
    answer: "Der AWUS036ACH verwendet den RTL8812AU-Chip und erfordert die Installation des aircrack-ng-Community-Treibers über DKMS, was nach Kernel-Updates möglicherweise eine Neukompilierung erfordert; der Treiber für den MT7612U des AWUS036ACM ist seit Kernel 4.19 im Mainline integriert, sodass Plug-and-Play ohne Kompilierung möglich ist."
  - question: "Welches Modell ist besser für die Monitor Mode-Überwachung geeignet?"
    answer: "Der Monitor Mode des AWUS036ACH ist stabiler; die Dual-Antennen und die hohe Leistung von 30 dBm führen in Umgebungen mit vielen Access Points zu einer geringeren Paketverlustrate. Der AWUS036ACM unterstützt ebenfalls den Monitor Mode, hat jedoch eine niedrigere Leistung der Single-Antenne und eignet sich besser für die Erfassung in kurzer Entfernung."
  - question: "Sollte ein Anfänger den AWUS036ACH oder den AWUS036ACM wählen?"
    answer: "Anfängern wird der AWUS036ACM empfohlen, da der MT7612U-Kernel-Nativtreiber Plug-and-Play ohne Kompilierung bietet. Wählen Sie stattdessen den AWUS036ACH, wenn Sie das stärkste Signal und die meisten Anleitungen wünschen und mit dem DKMS-Kompilierungsprozess vertraut sind."
  - question: "Welches Modell wird für eine VM-Umgebung empfohlen?"
    answer: "Für VM-Umgebungen wird der AWUS036ACM empfohlen, da der Kernel-Nativtreiber nach der USB-Weiterleitung sofort erkannt und verwendet werden kann, ohne dass Toolchains innerhalb der virtuellen Maschine installiert oder kompiliert werden müssen. Der AWUS036ACH erfordert die zusätzliche Installation des Treibers innerhalb der VM, um verwendet zu werden."

---Der AWUS036ACH eignet sich für professionelle Aufgaben, mit dem RTL8812AU-Treiber, 30 dBm Dual-Antennen und der stärksten Monitor Mode Packet Injection; der AWUS036ACM ist für Portabilität gedacht, mit dem MT7612U-Kern, nativem Treiber ohne Kompilierung und einem Preis von ca. 30–40 $.

{{< tldr >}}
Der AWUS036ACH eignet sich für professionelle Aufgaben, mit dem RTL8812AU-Treiber, 30 dBm Dual-Antennen und der stärksten Monitor Mode Packet Injection; der AWUS036ACM ist für Portabilität gedacht, mit dem MT7612U-Kern, nativem Treiber ohne Kompilierung und einem Preis von ca. 30–40 $.
{{< /tldr >}}


## Überblick

Für professionelle Penetrationstests wählen Sie den [AWUS036ACH](/de/products/alfa/awus036ach/): ausgereifter RTL8812AU-Treiber, 30 dBm Dual-Antenne für stärkste Überwachung und Packet Injection. Für Plug-and-Play-Mobilität den [AWUS036ACM](/de/products/alfa/awus036acm/): MT7612U nativer Kernel-Treiber, ab Kernel 4.19 sofort einsatzbereit ohne Kompilierung.

Zwei der beliebtesten ALFA Network USB-Adapter für Kali Linux Penetrationstests befinden sich an unterschiedlichen Punkten des Spektrums zwischen roher Leistung und Portabilität. Der **AWUS036ACH** ist ein leistungsstarkes Arbeitstier mit zwei Antennen und einer bewährten Treiberhistorie. Der **AWUS036ACM** ist eine kompakte, Kernel-native Alternative, die etwas Leistung gegen Einfachheit und Benutzerfreundlichkeit eintauscht. Diese Anleitung schlüsselt jeden Aspekt auf, der für echte Pentesting-Arbeit wichtig ist.

---

## AWUS036ACH — AC1200, RTL8812AU, Hohe Leistung

Der [AWUS036ACH](/de/products/alfa/awus036ach/) ist seit seiner Veröffentlichung ein fester Bestandteil der professionellen und hobbymäßigen Wi-Fi-Auditierung. Er ist der Adapter, der in der Mehrheit der zwischen 2017 und heute veröffentlichten Kali Linux Wireless Pentesting Tutorials, Kurse und Write-ups zitiert wird.

**Vollständige Spezifikationen:**
- **Wi-Fi-Standard:** IEEE 802.11a/b/g/n/ac (Wi-Fi 5)
- **Chipsatz:** Realtek RTL8812AU
- **Frequenzbänder:** 2,4 GHz + 5 GHz (Dualband)
- **Maximaler Durchsatz:** AC1200 (300 + 867 Mbps)
- **Antennen:** 2× abnehmbare RP-SMA-Anschlüsse (Dual-Antennen-Diversity)
- **Standard-Antennen:** 2× 5 dBi omnidirektional
- **USB-Anschluss:** USB-C (USB 3.0 kompatibel)
- **Sendeleistung (TX power):** Bis zu 30 dBm — eine der höchsten unter den USB-Adaptern
- **Abmessungen:** Größerer Formfaktor (Desktop-/Reisegebrauch)

Die dualen RP-SMA-Anschlüsse sind ein erheblicher Vorteil: Sie können leistungsstarke Richtantennen oder omnidirektionale Antennen anbringen, um die Reichweite dramatisch zu erhöhen, was für Audits über große Distanzen entscheidend ist.

---

## AWUS036ACM — AC600, MT7612U, Kompakt

Der [AWUS036ACM](/de/products/alfa/awus036acm/) richtet sich an Benutzer, die Wert auf Einfachheit, Portabilität und Kernel-nativen Treiber-Support legen. Er verwendet den MediaTek MT7612U (oder MT7612UN) Chipsatz, der seit Version 4.19 Teil des Haupt-Linux-Kernels ist — was bedeutet: **keine Treiberkompilierung** auf jedem modernen Kali Linux System.

**Vollständige Spezifikationen:**
- **Wi-Fi-Standard:** IEEE 802.11a/b/g/n/ac (Wi-Fi 5)
- **Chipsatz:** MediaTek MT7612U / MT7612UN
- **Frequenzbänder:** 2,4 GHz + 5 GHz (Dualband)
- **Maximaler Durchsatz:** AC600 (150 + 433 Mbps)
- **Antennen:** 1× abnehmbarer RP-SMA-Anschluss
- **Standard-Antenne:** 1× 5 dBi omnidirektional
- **USB-Anschluss:** USB-C (USB 3.0 kompatibel)
- **Sendeleistung (TX power):** Standardleistung (niedriger als ACH)
- **Abmessungen:** Kompakter Formfaktor (portabler Einsatz)

Die einzelne Antenne und die geringere Sendeleistung bedeuten eine reduzierte Langstreckenleistung im Vergleich zum ACH, aber die saubere Kernel-Treiber-Erfahrung und das kompakte Gehäuse machen ihn sehr praktisch für Einsätze, bei denen Unauffälligkeit oder Mobilität wichtig sind.

---

## Vergleichstabelle der Spezifikationen

| Feature | AWUS036ACH | AWUS036ACM |
|---|---|---|
| **Wi-Fi-Standard** | 802.11ac (Wi-Fi 5) | 802.11ac (Wi-Fi 5) |
| **Chipsatz** | RTL8812AU | MT7612U / MT7612UN |
| **Frequenzbänder** | 2,4 GHz + 5 GHz | 2,4 GHz + 5 GHz |
| **Max. Durchsatz** | AC1200 | AC600 |
| **RP-SMA-Anschlüsse** | 2× | 1× |
| **Sendeleistung (TX)** | Bis zu 30 dBm | Standard |
| **USB-Typ** | USB-C | USB-C |
| **Treiber-Quelle** | Out-of-tree (DKMS) | Haupt-Kernel (4.19+) |
| **Treiber-Installation**| Manuelle Kompilierung | Plug-and-Play |
| **Monitor-Modus** | ★★★★★ | ★★★★☆ |
| **Paket-Injektion** | ★★★★★ | ★★★★☆ |
| **Formfaktor** | Größer | Kompakt |
| **Preisklasse** | ~$40–50 | ~$30–40 |

---

## Chipsatz-Deep-Dive

### RTL8812AU (AWUS036ACH)

Der Realtek RTL8812AU ist einer der am intensivsten getesteten Chipsätze in der Wireless-Security-Forschung. Der von der Community gepflegte Treiber wird auf [github.com/aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) gehostet und wird seit 2017 aktiv entwickelt und gepatcht.

**Installation unter Kali Linux:**

```bash
sudo apt update
sudo apt install dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

Nach der Installation bleibt das Modul über DKMS auch bei Kernel-Updates erhalten. Der Treiber unterstützt:

- **Monitor-Modus** — voll funktionsfähig, extrem zuverlässig
- **Frame-Injektion** — alle Injektionstypen (Deauth, Beacon, Probe, Data)
- **Mehrere virtuelle Schnittstellen** — Monitor + Managed gleichzeitig betreiben
- **WPA3-SAE Handshake Capture** — bestätigt funktionsfähig in aktuellen Kernel/Treiber-Kombinationen

Der Haupt-Kompromiss besteht darin, dass Sie **neu kompilieren müssen** (oder DKMS übernimmt es automatisch), wenn ein neuer Kernel installiert wird. Gelegentlich unterbricht eine neue Kali-Kernel-Version vorübergehend den Build, bis der Treiber aktualisiert wird. Dies ist ein handhabbares, aber reales betriebliches Anliegen.

### MT7612U (AWUS036ACM)

Der MediaTek MT7612U Treiber (`mt76x2u`) wurde in Version **4.19 (Oktober 2018)** in den Haupt-Linux-Kernel integriert. Das bedeutet, dass der AWUS036ACM auf jeder Kali Linux Installation mit einem Kernel 4.19 oder neuer — was jede Kali-Version seit Ende 2018 abdeckt — **Plug-and-Play** ist.

```bash
# Überprüfen, ob das Modul geladen ist
lsmod | grep mt76x2u

# Manuelles Laden bei Bedarf
sudo modprobe mt76x2u
```

Wichtige Treiber-Eigenschaften:

- **Keine Kompilierung erforderlich** — ideal für luftgekühlte (air-gapped) oder eingeschränkte Umgebungen
- **Monitor-Modus** — unterstützt und funktionsfähig
- **Paket-Injektion** — unterstützt, allgemein zuverlässig
- **Stabilität** — Kernel-native Treiber neigen dazu, bei Kernel-Updates stabiler zu sein
- **Community-Support** — wachsend, wenn auch kleiner als das RTL8812AU-Ökosystem

Eine Nuance: Die MT7612UN-Variante (die in einigen ACM-Chargen verwendet wird) verhält sich unter Linux identisch, da beide vom selben `mt76x2u`-Modul gehandhabt werden.

---

## Vergleich des Monitor-Modus

Beide Adapter unterstützen den Monitor-Modus, aber es gibt praktische Unterschiede.

**AWUS036ACH (RTL8812AU):**

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
# Erstellt wlan0mon im Monitor-Modus
iwconfig wlan0mon
```

Das Umschalten der Kanäle im Monitor-Modus erfolgt sofort und zuverlässig. Die Schnittstelle bewältigt Umgebungen mit hohem Datenverkehr (viele APs und Clients) ohne Paketverlust bei normalen Capture-Raten.

**AWUS036ACM (MT7612U):**

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# Oder über airmon-ng:
sudo airmon-ng start wlan0
```

Der Monitor-Modus ist funktionsfähig und wurde mit Wireshark, tcpdump, airodump-ng und kismet bestätigt. Einige Benutzer berichten jedoch, dass sie für die zuverlässigsten Ergebnisse bei bestimmten Kernel-Versionen `iw` direkt anstelle von airmon-ng verwenden müssen.

---

## Vergleich der Paket-Injektion

**AWUS036ACH:** Paket-Injektion ist eines der stärksten Verkaufsargumente. Alle aireplay-ng Angriffsmodi funktionieren zuverlässig:

```bash
# Injektion testen
sudo aireplay-ng --test wlan0mon

# Deauthentication-Angriff
sudo aireplay-ng -0 5 -a [BSSID] wlan0mon

# WPA-Handshake-Capture via Deauth
sudo airodump-ng -c [CH] --bssid [BSSID] -w capture wlan0mon &
sudo aireplay-ng -0 3 -a [BSSID] wlan0mon
```

**AWUS036ACM:** Die Injektion funktioniert über alle Standard-Angriffstypen hinweg, obwohl einige Benutzer berichtet haben, dass Injektionen mit sehr hohen Raten bei bestimmten Kernel-Versionen gelegentlich zum Stillstand der Schnittstelle führen können. Für typische Pentesting-Workflows (kontrollierte Deauth, PMKID-Capture, KRACK-Tests) ist die Leistung zuverlässig.

---

## Komplexität der Treiber-Installation

Diese Tabelle sollte das Erste sein, was Sie prüfen — sie bestimmt, wie viel Einrichtungsaufwand Sie am ersten Tag und nach jedem Kernel-Update haben werden.

| Aufgabe | AWUS036ACH | AWUS036ACM |
|---|---|---|
| Frische Kali-Installation, Adapter einstecken | Nicht erkannt — Treiberinstallation nötig | Sofort erkannt |
| Nach Kernel-Update | DKMS baut automatisch neu (meistens) | Keine Aktion nötig |
| Offline-Rechner (Air-gapped) | Erfordert Vorbereitung von Offline-Paketen | Funktioniert nativ |
| Kali Live-USB | Treiber muss in der Sitzung installiert werden | Funktioniert sofort |
| VirtualBox/VMware Passthrough | Funktioniert nach Treiberinstallation im Gast | Funktioniert sofort im Gast |
| Raspberry Pi / ARM | DKMS + ARM-Header erforderlich | Plug-and-Play auf Pi 4/5 |

Das Zero-Install-Erlebnis des ACM ist ein echter Vorteil in Szenarien wie Live-Boot-Umgebungen, von Kunden bereitgestellten Rechnern oder CTF-Wettbewerben, in denen Zeit und Einfachheit entscheidend sind.

---

## Größe und Portabilität

Der **AWUS036ACH** hat eine deutlich größere Platine und ein größeres Gehäuse. Dies liegt zum Teil an den dualen RP-SMA-Anschlüssen und den größeren Leistungskomponenten, die für den 30-dBm-Ausgang erforderlich sind. Er passt problemlos in eine Laptoptasche, ist aber kein "Taschenadapter".

Der **AWUS036ACM** ist deutlich kompakter. Er kann diskret bei physischen Sicherheitsüberprüfungen oder in Umgebungen verwendet werden, in denen ein großer USB-Adapter Aufmerksamkeit erregen würde. Er verbraucht auch weniger Strom, was bei längerem Feldeinsatz über den Laptop-Akku wichtig ist.

---

## Preis vs. Wert

Mit etwa 40–50 € verlangt der **AWUS036ACH** einen Aufpreis, vor allem für seine Konfiguration mit zwei Antennen, die hohe Sendeleistung und die bewährte Treiber-Tradition. Für professionelle Einsätze, bei denen Zuverlässigkeit und Signalstärke die Qualität der Ergebnisse direkt beeinflussen, ist der Aufpreis gerechtfertigt.

Der **AWUS036ACM** bietet für ca. 30–40 € einen exzellenten Wert für folgende Zielgruppen:
- Studenten, die Wireless-Security lernen und Plug-and-Play-Einfachheit wollen
- Tester, die primär in Umgebungen mit geringer Entfernung arbeiten
- Teams, die einen Backup- oder Zweitadapter benötigen
- Jeder, der Wert auf einen sauberen Workflow ohne Kompilierung legt

---

## Fazit

**Red Teamer und professionelle Pentester → AWUS036ACH.** Das RTL8812AU-Treiber-Ökosystem wird in offensiven Tools besser unterstützt, und die Injektion mit zwei Antennen ist in realen Bewertungen messbar zuverlässiger. Wenn die Erfolgsraten der Injektion bei einem bezahlten Auftrag zählen, gewinnt der ACH.

**CTF-Studenten und Erstbenutzer von Kali → AWUS036ACM.** Keine Kompilierung unter Kali 2023.3+. Wenn Sie noch nie ein Kernel-Modul kompiliert haben, fangen Sie hier an — es gibt nichts, was Sie kaputt machen können.

**Benutzer von Raspberry Pi und ARM-Plattformen → AWUS036ACM.** MT7612U ist seit Kernel 4.x im Linux-Kernel-Baum enthalten. Plug-and-Play auf Pi 4/5, Odroid und Orange Pi. Der ACH funktioniert auch, erfordert aber die Kompilierung des Out-of-tree RTL8812AU-Treibers mit ARM-spezifischen Headern.

---

{{< faq >}}

## Raspberry Pi und ARM-Kompatibilität

Wenn Sie Kali auf einem Raspberry Pi 4, Pi 5 oder einem anderen ARM-Einplatinencomputer ausführen, ist der MT7612U-Chipsatz im AWUS036ACM die klare Wahl. Er ist seit Kernel 4.x im Linux-Kernel-Baum enthalten — Plug-and-Play unter Raspberry Pi OS, Kali ARM und Ubuntu Server ARM.

Der RTL8812AU (AWUS036ACH) erfordert Out-of-tree-Treiber unter ARM. Der Kompilierungsprozess ist der gleiche wie unter x86, aber Sie müssen die korrekten Header für Ihren ARM-Kernel installieren:

```bash
sudo apt install linux-headers-$(uname -r) bc
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && make && sudo make install
```

Eine vollständige Einrichtungsanleitung finden Sie unter [ALFA USB WiFi auf Raspberry Pi 4 & Pi 5](/de/blog/alfa-adapter-raspberry-pi-kali/).

## Referenzen

1. aircrack-ng Community-gepflegt RTL8812AU Treiber-Repository — [github.com/aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au)
2. Linux Kernel Mainline MT76 Treiber (`mt76x2u`, integriert ab Kernel 4.19) — [kernel.org — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76)
3. ALFA Network Offizielle Website und Produktspezifikationen — [alfa.com.tw](https://www.alfa.com.tw)
4. Yupitek — ALFA Network Autorisierter Haendler in Taiwan — [yupitek.com](https://www.yupitek.com)