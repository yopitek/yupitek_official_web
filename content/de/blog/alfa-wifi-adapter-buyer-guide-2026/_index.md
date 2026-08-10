---
title: "ALFA WLAN-Adapter Kaufberatung 2026: Welches Modell ist das richtige für Sie?"
description: "Vollständige Kaufberatung für ALFA Network USB-WLAN-Adapter 2026. Vergleichen Sie AWUS036ACH, ACM, ACS, AX, AXER, AXM, AXML, EACS in Bezug auf Treiberunterstützung, Monitor-Modus, OS-Kompatibilität und Preis."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-network", "wlan-adapter", "kaufberatung", "kali-linux", "penetration-testing", "monitor-modus"]
featureimage: "/images/blog/alfa-wifi-adapter-buyer-guide-2026.webp"
faq:
  - question: "Was sind die Auswahlkriterien für ALFA-Netzwerkkarten?"
    answer: "Die Auswahlkriterien umfassen die Ausgereiftheit der Chipset-Treiber, die Betriebssystemkompatibilität, die Unterstützung von Monitor Mode und die Sendeleistung; der RTL8812AU-Treiber ist am ausgereiftesten und stabilsten."
  - question: "Welche ALFA-Netzwerkkarten unterstützen Monitor Mode?"
    answer: "ACH, ACM, ACS, AX, AXER, AXM und AXML unterstützen den Monitor Mode und Packet Injection vollständig; EACS (RTL8821CU) unterstützt dies nicht."
  - question: "Sind WiFi 6E/6-Netzwerkkarten notwendig?"
    answer: "Sie sind notwendig, wenn der Audit-Bereich das 6-GHz-Band umfasst. AXML unterstützt Tri-Band AX3000 und erfordert einen Linux-Kernel ≥ 5.18 sowie firmware-misc-nonfree."
  - question: "Was sind die Unterschiede bei der Installation der Treiber für RTL8812AU und MT7612U?"
    answer: "Für RTL8812AU ist eine DKMS-Kompilierung und Installation erforderlich, und nach Kernel-Updates muss eine Neukompilierung erfolgen; MT7612U ist seit Kernel 4.19 im Mainline-Kernel integriert, funktioniert Plug-and-Play und erfordert keine Kompilierung."
  - question: "Welche ALFA-Netzwerkkarte wird 2026 am meisten empfohlen?"
    answer: "Die erste Wahl für Red Teams: AWUS036ACH (500 mW, Dual-Antenne), die preisgünstige Erstwahl: AWUS036ACM, die Erstwahl für Unternehmen mit 6E: AWUS036AXML."
---

Dieser Leitfaden hilft Netzwerksicherheitsingenieuren, IT-Experten und Red-Teamern, im Jahr 2026 den richtigen ALFA Network USB-WLAN-Adapter auszuwählen. Wir decken alle acht aktuellen Modelle ab — [AWUS036ACS](/de/products/alfa/awus036acs/), [AWUS036ACH](/de/products/alfa/awus036ach/), [AWUS036ACM](/de/products/alfa/awus036acm/), [AWUS036EACS](/de/products/alfa/awus036eacs/), [AWUS036AX](/de/products/alfa/awus036ax/), [AWUS036AXER](/de/products/alfa/awus036axer/), [AWUS036AXM](/de/products/alfa/awus036axm/) und [AWUS036AXML](/de/products/alfa/awus036axml/). Wir vergleichen Chipsätze, Treiberreife, Betriebssystemunterstützung und reale Einsatzszenarien, damit Sie weniger Zeit mit der Fehlersuche bei Treibern und mehr Zeit mit Ihrer eigentlichen Arbeit verbringen.

{{< tldr >}}
AWUS036ACH ist die erste Wahl für Red Teams im Jahr 2026: 500 mW, Dual-Antenne AC1200, der RTL8812AU-Treiber ist am ausgereiftesten. Für ein günstiges Modell wählen Sie AWUS036ACM, für Enterprise 6E wählen Sie AWUS036AXML (AX3000 Tri-Band).
{{< /tldr >}}

---

## Wie man wählt: 4 Schlüsselfragen

Bevor Sie eine Produktseite öffnen, beantworten Sie diese vier Fragen. Ihre Antworten werden die meisten Optionen sofort ausschließen.

### (a) Welches Betriebssystem verwenden Sie?

Die Treiberunterstützung ist entscheidend. Benutzer von Kali Linux und Ubuntu mit aktuellen Kerneln haben die größte Auswahl. Die Unterstützung für macOS ist bei allen Modellen eher gering. Windows 10/11 wird im Allgemeinen gut unterstützt. Wenn Sie einen Raspberry Pi oder eine ARM-basierte Plattform verwenden, ist die Wahl des Chipsatzes enorm wichtig.

- **Kali Linux / Debian:** RTL8812AU (`dkms-rtl8812au`) und MT7921AUN (nativer Kernel ≥ 5.18) sind Ihre beiden primären Chipsatzfamilien für Penetrationstests.
- **Ubuntu 22.04 / 24.04:** Ähnliche Treiberlandschaft, aber Sie müssen möglicherweise HWE-Kernel oder `firmware-misc-nonfree` für MT7921AUN installieren.
- **Windows 10/11:** ALFA liefert signierte Treiber für alle aktuellen Modelle. Die Installation ist unkompliziert.
- **macOS Sonoma:** Nur eine Handvoll Adapter verfügen über von der Community gepflegte Kext-Unterstützung. Rechnen Sie mit Schwierigkeiten; planen Sie einen VM-Arbeitsablauf ein.
- **Raspberry Pi (Kali NetHunter, ARM):** RTL8812AU-Modelle (ACH) und MT7612U-Modelle (ACM) sind die sichere Wahl. MT7921AUN kann funktionieren, erfordert aber das Paket `firmware-misc-nonfree` und einen ausreichend aktuellen Kernel.

### (b) Benötigen Sie den Monitor-Modus und Packet Injection?

Wenn Ihre Antwort "Ja" lautet — und das sollte sie für jede Penetrationstest- oder Wireless-Audit-Arbeit sein — streichen Sie den [AWUS036EACS](/de/products/alfa/awus036eacs/) sofort von Ihrer Liste. Sein RTL8821CU-Chipsatz unterstützt unter Linux weder den Monitor-Modus noch Packet Injection. Jedes andere Modell in diesem Leitfaden unterstützt dies.

### (c) VM oder Bare Metal?

USB-Passthrough in VirtualBox und VMware fügt eine Komplexitätsebene hinzu. Jeder Adapter auf dieser Liste funktioniert mit korrekt konfiguriertem Passthrough, aber RTL8812AU-Adapter (ACH) und MT7612U-Adapter (ACM) haben die längste Erfolgsbilanz in VM-Umgebungen. Wenn Sie das Gerät ausschließlich an eine VM durchreichen, vermeiden Sie Adapter, die auf Firmware-Dateien angewiesen sind, die zur Laufzeit geladen werden — verlorene USB-Verbindungen bedeuten verlorene Firmware.

Siehe [ALFA-Adapter-Einrichtung in VirtualBox und VMware](/de/blog/alfa-adapter-virtualbox-vmware-usb/) für vollständige Installationsanweisungen.

### (d) Budget?

Die Wi-Fi 5 Generation (ACH, ACM, ACS) ist günstiger, hat stabilere Treiber und ist die richtige Wahl, wenn das Budget begrenzt ist oder die Treiberstabilität an erster Stelle steht. Die Wi-Fi 6/6E Generation (AX, AXER, AXM, AXML) ist die Zukunft der Hardware, aber Sie zahlen mehr und müssen einige Grenzfälle bei den Treibern auf Nicht-Mainline-Kerneln in Kauf nehmen.

---

## Vollständige ALFA-Adapter-Vergleichstabelle

<div style="overflow-x: auto;">

| Modell | Wi-Fi Gen | Chip | Max. Speed | Monitor-Modus | Kali-Treiber | Windows | macOS | Antennen | Am besten für |
|---|---|---|---|---|---|---|---|---|---|
| [AWUS036ACS](/de/products/alfa/awus036acs/) | Wi-Fi 5 | RTL8811AU | AC600 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 1× RP-SMA | Leichtes Reise-Kit |
| [AWUS036ACH](/de/products/alfa/awus036ach/) | Wi-Fi 5 | RTL8812AU | AC1200 | ✅✅ Beste | rtl8812au-dkms | ✅ | ⚠️ | 2× RP-SMA | Red-Team Operationen |
| [AWUS036ACM](/de/products/alfa/awus036acm/) | Wi-Fi 5 | MT7612U | AC1200 | ✅ | mt76x2u (≥4.19) | ✅ | ⚠️ | 2× RP-SMA | Linux Plug & Play |
| [AWUS036EACS](/de/products/alfa/awus036eacs/) | Wi-Fi 5 | RTL8821CU | AC1200 | ❌ | rtl88xxcu (OOK) | ✅ | ⚠️ | Integriert 2dBi | Windows Home WiFi + BT |
| [AWUS036AX](/de/products/alfa/awus036ax/) | Wi-Fi 6 | RTL8832BU | AX1200 | ⚠️ Begrenzt | OOK (<6.14) | ✅ | ❌ | Integriert | Windows WiFi 6 |
| [AWUS036AXER](/de/products/alfa/awus036axer/) | Wi-Fi 6 | RTL8832BU | AX1800 | ⚠️ Begrenzt | OOK (<6.14) | ✅ | ❌ | Integriert Nano | Kompakter Reiseadapter |
| [AWUS036AXM](/de/products/alfa/awus036axm/) | Wi-Fi 6E | MT7921AUN | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 2× RP-SMA | Wi-Fi 6E + Dual-Antenne |
| [AWUS036AXML](/de/products/alfa/awus036axml/) | Wi-Fi 6E | MT7921AUN | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 1× RP-SMA | WiFi 6E + Linux + USB-C |

</div>

**Legende:** ✅ Unterstützt · ⚠️ Begrenzt/Teilweise · ❌ Nicht unterstützt

{{< alert "circle-info" >}}
**Hinweis zu macOS:** Alle ALFA-Adapter stehen vor Treiberherausforderungen unter macOS Ventura und Sonoma. Die gängigste von der Community gepflegte Option ist das Ausführen von Kali Linux in einer VM mit USB-Passthrough. AWUS036EACS (RTL8821CU) kann unter macOS über Drittanbieter-Treiber für Standard-Client-Verbindungen funktionieren, aber der Monitor-Modus wird nicht unterstützt.
{{< /alert >}}

---

## Wi-Fi 5 Adapter (Beste Treiberreife)

Die Wi-Fi 5 Generation blickt auf jahrelange Community-Entwicklung zurück. Wenn Ihre Priorität auf einer absolut stabilen Treiberunterstützung liegt — besonders für CTF-Wettbewerbe, professionelle Audits oder Umgebungen, in denen Sie sich nach einem Kernel-Update keinen defekten Treiber leisten können — fangen Sie hier an.

### AWUS036ACH — Der Red-Team Standard

Der [AWUS036ACH](/de/products/alfa/awus036ach/) bleibt aus gutem Grund der am weitesten verbreitete ALFA-Adapter in der Sicherheits-Community. Sein RTL8812AU-Chipsatz wird vom `aircrack-ng/rtl8812au`-Treiber unterstützt, der seit Jahren mit jedem großen Kali Linux-Release getestet und gepflegt wird.

**Hardware-Spezifikationen:**
- Chipsatz: RTL8812AU (Realtek)
- Zwei abnehmbare RP-SMA Antennenanschlüsse — kompatibel mit dem gesamten ALFA-Antennensortiment
- 500 mW Sendeleistung — die höchste in der Wi-Fi 5 Reihe
- Dual-Band: 2,4 GHz und 5 GHz

**Warum er führend für Red-Teams ist:** 500 mW Sendeleistung kombiniert mit zwei externen Antennen und ausgereifter Injection-Unterstützung bedeutet, dass Sie aus der Ferne arbeiten können, während die Rahmenübertragung zuverlässig bleibt. Tauschen Sie die Standard-Rundstrahlantennen gegen ein [APA-M25](/de/products/alfa/apa-m25/) Richtpanel aus, und Sie haben eine ernsthafte Langstreckenplattform. Die Form mit zwei Antennen ermöglicht zudem echtes 2T2R MIMO, wenn Sie mit Zielnetzwerken verbunden sind.

**Treiberinstallation unter Kali:**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
```

{{< alert "triangle-exclamation" >}}
Auf Kerneln ≥ 6.2 kann das in älteren Kali-Images enthaltene Standard-Modul `rtl8812au` möglicherweise nicht geladen werden. Installieren Sie immer `dkms-rtl8812au` aus dem Kali-Repository — es verfolgt Kernel-Änderungen und wird bei Kernel-Updates automatisch über DKMS neu erstellt.
{{< /alert >}}

### AWUS036ACM — Die Linux Plug-and-Play Wahl

Der [AWUS036ACM](/de/products/alfa/awus036acm/) verwendet den MediaTek MT7612U Chipsatz — eine andere Familie als der RTL8812AU des ACH. Sein größter Vorteil ist die Unterstützung im Mainline Linux-Kernel seit Kernel 4.19 als `mt76x2u`-Treiber. Das bedeutet: Null Treiberkompilation auf jedem modernen Kali Linux- oder Ubuntu-System. Er wird mit zwei RP-SMA-Anschlüssen für den Dual-Antennen-Betrieb geliefert.

Funktional gesehen sind Monitor-Modus und Injection-Unterstützung für Sicherheitsarbeiten voll gegeben.

Wenn Sie nur einen Antennenanschluss benötigen und nicht die erweiterte Sendeleistung des ACH brauchen, deckt der ACM dieselben Anwendungsfälle für weniger Geld ab. Er ist eine häufige Wahl für Team-Ausstattungen, bei denen Adapter in größeren Mengen für ein Audit-Team gekauft werden.

**Wann Sie ACM gegenüber ACH wählen sollten:** Problemlose Linux-Treiber-Einrichtung, Plug-and-Play unter Ubuntu/Kali ohne Kompilierung, Dual-Antennen-Abdeckung zu einem niedrigeren Preis als beim ACH.

### AWUS036ACS — Leicht und tragbar

Der [AWUS036ACS](/de/products/alfa/awus036acs/) verwendet den RTL8811AU-Chipsatz — eine Stufe unter dem RTL8812AU in Bezug auf die Sendeleistung, aber immer noch voll fähig für den Monitor-Modus und Packet Injection. Sein kompakter Formfaktor und die einzelne Antenne machen ihn zur Wahl für viel reisende Berater, die nicht mehrere RP-SMA-Antennen durch die Flughafensicherheit schleppen möchten.

Der RTL8811AU-Treiber nutzt dasselbe `rtl8812au-dkms` Paket unter Kali, daher ist der Installationsablauf identisch.

**Kompromisse gegenüber ACH/ACM:** Geringere Sendeleistung (weniger Reichweite auf Distanz), einzelne Antenne (kein MIMO), AC600 gegenüber AC1200 maximalem Durchsatz. Für die meisten Capture-and-Inject-Arbeitsabläufe sind diese Unterschiede irrelevant. Für Fernoperationen spielen sie eine Rolle.

### AWUS036EACS — Für den allgemeinen Gebrauch, nicht für Pentesting

Der [AWUS036EACS](/de/products/alfa/awus036eacs/) wird von einem Realtek RTL8821CU Chipsatz angetrieben. Die Unterstützung von Linux-Treibern für den RTL8821CU ist begrenzt — Monitor-Modus und Packet Injection werden nicht unterstützt. Dieser Adapter ist für die Windows-Client-Konnektivität konzipiert und enthält Bluetooth 4.2, nicht für Sicherheitsprüfungstests.

{{< alert "triangle-exclamation" >}}
**Verwenden Sie den AWUS036EACS nicht für Penetrationstests, Red-Team Operationen oder Aufgaben, die den Monitor-Modus oder Packet Injection erfordern.** Er eignet sich für die allgemeine WLAN-Konnektivität, zur Reichweitenverlängerung von DJI-Drohnen-Controllern (wo er häufig eingesetzt wird) und für Windows-fokussierte Umgebungen, in denen ein Standardverhalten als Client-Adapter akzeptabel ist.
{{< /alert >}}

Er verdient seinen Platz auf dieser Liste wegen seiner Bluetooth 4.2 Kombinationsfähigkeit und der direkten Windows-Unterstützung. Unter macOS ist die Unterstützung von Community-Treibern für den RTL8821CU begrenzt und der Monitor-Modus nicht verfügbar.

---

## Wi-Fi 6 Adapter (Windows-fokussiert)

Wi-Fi 6 (802.11ax) brachte deutliche Verbesserungen bei der Leistung in dichten Umgebungen, MU-MIMO-Szenarien und BSS Coloring zur Netzwerkidentifizierung. Der AWUS036AX und AWUS036AXER sind die Wi-Fi 6 Adapter von ALFA, die primär für die Windows-Konnektivität entwickelt wurden.

Beide Wi-Fi 6 ALFA-Adapter verwenden den Realtek RTL8832BU Chipsatz. Unter Linux ist der RTL8832BU-Treiber bei Kerneln unter 6.14 ein Out-of-Kernel (OOK) Treiber, was eine **begrenzte Unterstützung für den Monitor-Modus und Packet Injection** bedeutet. Wenn Ihr Hauptanwendungsfall Penetrationstests unter Linux sind, wählen Sie stattdessen den AWUS036ACH oder AWUS036AXML.

### AWUS036AX — Wi-Fi 6 Windows-Adapter

Der [AWUS036AX](/de/products/alfa/awus036ax/) ist der Wi-Fi 6 Adapter von ALFA mit einer integrierten Antenne (kein externer RP-SMA Anschluss). Er liefert AX1200-Geschwindigkeiten auf den 2,4- und 5-GHz-Bändern und ist bestens für die Konnektivität unter Windows 10/11 geeignet.

**Treiberstatus:**
- Windows: Volle Unterstützung über den von ALFA bereitgestellten Treiber
- Linux Kernel ≥ 6.14: In-Kernel RTL8832BU Treiber
- Linux Kernel < 6.14: Out-of-Kernel Treiber erforderlich
- Monitor-Modus: ⚠️ Begrenzt
- Packet Injection: ⚠️ Begrenzt

{{< alert "triangle-exclamation" >}}
**Hinweis zu Linux-Penetrationstests:** Der AWUS036AX verwendet den RTL8832BU-Chipsatz, der unter Linux-Kerneln unter 6.14 nur begrenzte Unterstützung für den Monitor-Modus und Packet Injection bietet. Für Sicherheitsarbeiten unter Kali Linux verwenden Sie stattdessen den [AWUS036ACH](/de/products/alfa/awus036ach/) (RTL8812AU) oder den [AWUS036AXML](/de/products/alfa/awus036axml/) (MT7921AUN).
{{< /alert >}}

### AWUS036AXER — Kompakter Reise-WLAN-Adapter (Wi-Fi 6)

Der [AWUS036AXER](/de/products/alfa/awus036axer/) verwendet den gleichen RTL8832BU-Chipsatz wie der AWUS036AX, jedoch in einem ultra-kompakten Nano-Formfaktor (10,5g). Die Treibersituation ist identisch — gleicher RTL8832BU, gleiche Linux-Einschränkungen, gleiche Windows-Kompatibilität.

Wählen Sie den AXER gegenüber dem AX, wenn Portabilität der entscheidende Faktor ist: Geschäftsreisen, Setups mit minimalem Platzbedarf oder Situationen, in denen ein kompakter Dongle gegenüber einem normal großen Adapter bevorzugt wird.

---

## Wi-Fi 6E Adapter (Zukunftssicher)

Wi-Fi 6E erweitert 802.11ax in das 6-GHz-Band und bietet Zugriff auf das neue Spektrum von 5,925–7,125 GHz. In der Praxis bedeutet dies weniger Interferenzen, breitere Kanalbandbreiten (bis zu 160 MHz) und Zugriff auf ein Band, das ältere Geräte nicht sehen oder erreichen können. Da Unternehmensnetzwerke zunehmend Wi-Fi 6E-Infrastrukturen bereitstellen, benötigen Auditoren 6E-fähige Adapter, um die gesamte Angriffsfläche zu bewerten.

Beide Wi-Fi 6E ALFA-Adapter erfordern Kernel ≥ 5.18 für die 6-GHz-Unterstützung. Das 6-GHz-Band erfordert eine korrekt eingestellte Regulatory Domain — die Durchsetzung der Vorschriften für 6 GHz ist in den meisten Gerichtsbarkeiten strenger als für 2,4/5 GHz.

### AWUS036AXM — Wi-Fi 6E Einstiegspunkt

Der [AWUS036AXM](/de/products/alfa/awus036axm/) verwendet den MT7921AUN-Chipsatz mit voller Tri-Band-Unterstützung inklusive 6 GHz. Er wird mit zwei RP-SMA-Anschlüssen für den 2T2R-Dual-Antennen-Betrieb geliefert.

Für Anwender, die hauptsächlich in 2,4- und 5-GHz-Umgebungen arbeiten, aber 6-GHz-Fähigkeiten für neue Netzwerkbewertungen wünschen, ohne Flaggschiff-Preise zu zahlen, ist der AXM der logische Einstiegspunkt.

**Bandabdeckung:** 2,4 GHz, 5 GHz, 6 GHz (Tri-Band)
**Antennen:** 2× RP-SMA — austauschbar gegen jede kompatible ALFA-Antenne

### AWUS036AXML — Das Flaggschiff unter den 6E-Adaptern

Der [AWUS036AXML](/de/products/alfa/awus036axml/) ist das aktuelle Flaggschiff von ALFA. Er verfügt über den MT7921AUN-Chipsatz, USB-C 3.2 Konnektivität, Bluetooth 5.2 und einen einzelnen High-Gain RP-SMA Anschluss.

**Wichtigste Spezifikationen:**
- Chipsatz: MT7921AUN (MediaTek)
- 1× RP-SMA Anschluss — kompatibel mit dem gesamten ALFA-Antennensortiment
- Tri-Band: 2,4 GHz + 5 GHz + 6 GHz
- AX3000 Klasse (theoretisch bis zu 3000 Mbps über alle Bänder hinweg)
- USB-C 3.2 — schnellere Bandbreite zum Host-Bus gegenüber USB-A

**Treiberhinweise für AXML:**
- MT7921AUN wird unter der `mt7921u` Treiberfamilie ab Kernel ≥ 5.18 unterstützt.
- Monitor-Modus wird unterstützt; aktiver Monitor mit Firmware hat bei einigen Kerneln Probleme mit dem Neustart der Firmware gezeigt — siehe die [AWUS036AXML Detailbewertung](/de/blog/awus036axml-wifi-6e-review/) für vollständige Testdaten.
- Das 6-GHz-Band im Monitor-Modus erfordert, dass Ihre Regulatory Domain passives Scannen auf 6-GHz-Kanälen zulässt.

{{< alert "triangle-exclamation" >}}
**Hinweis zur AWUS036AXML-Firmware:** Bei Kerneln unter 6.1 kommt es bei einigen Benutzern zu Firmware-Abstürzen, wenn sie den AXML wiederholt zwischen Monitor-Modus und Managed-Modus umschalten. Wenn Ihr Arbeitsablauf häufige Moduswechsel erfordert, verwenden Sie Kernel ≥ 6.1 und installieren Sie das neueste `firmware-misc-nonfree` Paket.
{{< /alert >}}

---

## Tiefer Einblick in die Treiberkompatibilität

<div style="overflow-x: auto;">

| Modell | Chip | Kali-Paket | Ubuntu HWE | RPi ARM | Windows 10/11 |
|---|---|---|---|---|---|
| [AWUS036ACS](/de/products/alfa/awus036acs/) | RTL8811AU | `dkms-rtl8812au` | Manueller Build | ✅ rtl8812au-dkms | ✅ ALFA-Treiber |
| [AWUS036ACH](/de/products/alfa/awus036ach/) | RTL8812AU | `dkms-rtl8812au` | Manueller Build | ✅ rtl8812au-dkms | ✅ ALFA-Treiber |
| [AWUS036ACM](/de/products/alfa/awus036acm/) | MT7612U | `mt76x2u` (In-Kernel) | In-Kernel ≥4.19 | ✅ Nativ | ✅ ALFA-Treiber |
| [AWUS036EACS](/de/products/alfa/awus036eacs/) | RTL8821CU | `rtl88xxcu` (OOK) | OOK | ❌ Nicht unterstützt | ✅ ALFA-Treiber |
| [AWUS036AX](/de/products/alfa/awus036ax/) | RTL8832BU | OOK (<6.14) | OOK (<6.14) | ⚠️ Begrenzt | ✅ ALFA-Treiber |
| [AWUS036AXER](/de/products/alfa/awus036axer/) | RTL8832BU | OOK (<6.14) | OOK (<6.14) | ⚠️ Begrenzt | ✅ ALFA-Treiber |
| [AWUS036AXM](/de/products/alfa/awus036axm/) | MT7921AUN | `firmware-misc-nonfree` | In-Kernel ≥5.18 | ✅ Firmware erf. | ✅ ALFA-Treiber |
| [AWUS036AXML](/de/products/alfa/awus036axml/) | MT7921AUN | `firmware-misc-nonfree` | In-Kernel ≥5.18 | ✅ Firmware erf. | ✅ ALFA-Treiber |

</div>

**RTL8812AU-Kernel-Historie:** Der RTL8812AU-Treiber wurde in Linux 5.2 teilweise in den Mainline-Kernel integriert, jedoch mit erheblichen Einschränkungen — kein Monitor-Modus, keine Injection. Volle Penetrationstest-Fähigkeiten erfordern den Out-of-Tree `rtl8812au`-Treiber, der unter Kali als `dkms-rtl8812au` paketiert ist. Das DKMS-Paket wird bei der Aktualisierung des Kernels automatisch neu erstellt, was es auf Kali Linux-Systemen im Wesentlichen wartungsfrei macht.

**MT7921AUN-Kernel-Historie:** Die native Integration erfolgte in Linux 5.18 über den `mt7921u` USB-Treiber. Die Firmware-Datei `WIFI_MT7961_patch_mcu_1_2_hdr.bin` (und zugehörige Firmware-Blobs) muss in `/lib/firmware/mediatek/` vorhanden sein. Unter Kali werden diese durch `firmware-misc-nonfree` bereitgestellt. Unter Ubuntu 22.04 LTS mit dem Standard-Kernel müssen Sie möglicherweise den HWE-Stack (`linux-generic-hwe-22.04`) installieren, um ≥ 5.18 zu erreichen.

**Besonderheiten beim Raspberry Pi:** Der RTL8812AU-Treiber lässt sich unter Raspberry Pi OS (32-Bit und 64-Bit) mit `dkms-rtl8812au` sauber kompilieren. Er ist die sicherste Wahl für NetHunter-Einsätze. MT7921AUN-Adapter (AXM, AXML) können auf dem Pi 4/5 funktionieren, erfordern aber das Paket `firmware-misc-nonfree` und einen ausreichend aktuellen Raspberry Pi OS-Kernel (Images ab 2023 sollten in Ordnung sein).

---

## Bester ALFA-Adapter nach Anwendungsfall

### Red-Team Operationen

**Empfohlen: [AWUS036ACH](/de/products/alfa/awus036ach/)**

Die 500 mW Sendeleistung des ACH, die zwei Antennen und der kampferprobte RTL8812AU-Treiber machen ihn zum Standard für Red-Team-Einsätze. Sie können sich darauf verlassen, dass er nach einem Kernel-Update funktioniert, zuverlässig an eine VM durchgereicht werden kann und jede RP-SMA-Antenne akzeptiert, die Sie mitbringen. Wenn es das Budget erlaubt und 6E-Abdeckung erforderlich ist, fügen Sie einen [AWUS036AXML](/de/products/alfa/awus036axml/) als Zweitadapter für die 6-GHz-Netzwerkerkennung hinzu.

### CTF-Wettbewerbe

**Empfohlen: [AWUS036ACM](/de/products/alfa/awus036acm/)**

CTF-Wireless-Herausforderungen finden in der Regel in kontrollierten Umgebungen statt, in denen die Sendeleistung nicht die kritische Variable ist. Der ACM bietet volle Monitor-Modus- und Injection-Fähigkeiten bei einer Linux-Treiber-Einrichtung ohne Aufwand (MT7612U In-Kernel seit 4.19). Sein kompakter Formfaktor mit zwei Antennen ist leicht zu packen und einzusetzen. Wenn der CTF Wi-Fi 6 Herausforderungen beinhaltet (noch selten, aber zunehmend), greifen Sie stattdessen zum [AWUS036AXML](/de/products/alfa/awus036axml/).

### Raspberry Pi / Kali NetHunter

**Empfohlen: [AWUS036ACH](/de/products/alfa/awus036ach/) oder [AWUS036ACM](/de/products/alfa/awus036acm/)**

Die RTL8812AU (ACH) und MT7612U (ACM) Adapter haben eine bewährte Erfolgsbilanz auf Raspberry Pi-Hardware. Vermeiden Sie MT7921AUN-Modelle (AXM, AXML) für Pi-Einsätze, es sei denn, Sie haben die Kernel- und Firmware-Kompatibilität auf Ihrem spezifischen Image bestätigt. Der ACH ist die sicherere Wahl, wenn Sie einen dedizierten NetHunter-Pi bauen, der im Feld zuverlässig sein muss.

### Wireless-Audit in Unternehmen

**Empfohlen: [AWUS036AXML](/de/products/alfa/awus036axml/) + [AWUS036ACH](/de/products/alfa/awus036ach/)**

Ein modernes Wireless-Audit in Unternehmen sollte die Bänder 2,4, 5 und 6 GHz abdecken. Der AXML deckt das gesamte Tri-Band-Spektrum inklusive 6E ab, während der ACH ein stabiles, leistungsstarkes Fallback für 5-GHz-Arbeiten bietet. Das gleichzeitige Betreiben beider Adapter mit separaten Capture-Schnittstellen ermöglicht eine vollständige Bandabdeckung ohne Kompromisse bei den Treibern. Verwenden Sie den ACH für aktive Injection-Aufgaben und den AXML für passives 6-GHz-Monitoring.

### DJI-Drohnen Reichweitenverlängerung

**Empfohlen: [AWUS036EACS](/de/products/alfa/awus036eacs/)**

Die Reichweitenverlängerung für DJI-Drohnen über Litchi oder DJI GO ist ein häufiger legitimer Anwendungsfall. Der EACS mit RTL8821CU wird hier empfohlen, da er nativ unter Windows (wo die DJI-Software läuft) ohne zusätzliche Treiber funktioniert und sein Profil für allgemeine Konnektivität für diesen Anwendungsfall geeignet ist. Kein Monitor-Modus erforderlich; Client-Mode-Konnektivität und Sendeleistung sind hier entscheidend. Kombinieren Sie ihn mit einer [APA-M25](/de/products/alfa/apa-m25/) Panel-Antenne für die maximale effektive Reichweite.

---

## Betriebssystem-spezifische Empfehlungen

### Kali Linux

Kali Linux ist die primär unterstützte Plattform für alle ALFA-Adapter, die für Sicherheitsarbeiten verwendet werden. Das Kali-Repository enthält `dkms-rtl8812au` für RTL8812AU/RTL8811AU-Adapter und `firmware-misc-nonfree` für MT7921AUN-Adapter. Halten Sie Ihr Kali-System auf dem neuesten Stand — das DKMS-Paket verfolgt Kernel-Änderungen automatisch.

**Schnell-Einrichtung (RTL8812AU-Familie):**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
sudo modprobe 88XXau
```

**Schnell-Einrichtung (MT7921AUN-Familie — AXM, AXML):**
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
# Neustart oder Modul neu laden:
sudo modprobe mt7921u
```

**Monitor-Modus aktivieren:**
```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

### Ubuntu 24.04 LTS

Ubuntu 24.04 wird mit Kernel 6.8 ausgeliefert. MT7921AUN-Adapter (AXM, AXML) funktionieren direkt, sobald `firmware-misc-nonfree` installiert ist:
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

Die RTL8812AU-Unterstützung unter Ubuntu erfordert das Erstellen des DKMS-Moduls:
```bash
sudo apt install -y git dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && sudo make dkms_install
```

### Windows 11

Alle ALFA-Adapter werden mit Windows 10/11 kompatiblen Treibern geliefert. Laden Sie das Treiberpaket von der ALFA Network Website herunter oder installieren Sie es über Windows Update für MT7921AUN (Microsoft stellt einen WHQL-signierten Inbox-Treiber bereit). RTL8812AU-Adapter erfordern das von ALFA bereitgestellte Realtek-Treiberpaket; Windows Update-Treiber für den RTL8812AU sind nicht konsistent verfügbar.

Für die Verwendung mit Tools wie Acrylic Wi-Fi, inSSIDer oder der Windows-Version von Wireshark bieten die ALFA-Treiber einen funktionalen Monitor-Modus-Wrapper unter Windows über den NDIS-Monitor-Modus — auch wenn dieser für aktive Injection-Arbeiten wesentlich weniger leistungsfähig ist als der Linux-Monitor-Modus.

### macOS Sonoma

Es gibt im Jahr 2026 keinen offiziell unterstützten ALFA-Adapter für macOS Sonoma. Es existieren Community-Kext-Projekte für den RTL8812AU, diese sind jedoch unsigniert und erfordern das Deaktivieren des Systemintegritätsschutzes (SIP). Die praktische Empfehlung lautet, Kali Linux in einer VM (Parallels, VMware Fusion oder UTM) mit USB-Passthrough zum ALFA-Adapter auszuführen.

Der AWUS036EACS mit RTL8821CU hat möglicherweise eine begrenzte macOS-Treiberunterstützung über Community-Projekte, aber der Monitor-Modus ist auf keiner Plattform verfügbar.

### Raspberry Pi / Kali NetHunter

Auf dem Raspberry Pi 4 und Pi 5 mit Kali NetHunter:

```bash
# Für RTL8812AU-Adapter (ACH, ACS):
sudo apt update && sudo apt install -y dkms-rtl8812au

# Für MT7921AUN-Adapter (AXM, AXML — Pi 5 mit aktuellem Kernel empfohlen):
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

{{< alert "circle-info" >}}
Wenn Sie einen dedizierten NetHunter-Dropbox bauen, verwenden Sie den [AWUS036ACH](/de/products/alfa/awus036ach/) oder [AWUS036ACM](/de/products/alfa/awus036acm/). Die RTL8812AU (ACH) und MT7612U (ACM) Treiber lassen sich zuverlässig auf ARM kompilieren und haben keine Abhängigkeit von Firmware-Dateien. MT7921AUN-Modelle (AXM, AXML) sind auf dem Pi funktionsfähig, fügen jedoch eine Abhängigkeit von Firmware-Dateien hinzu, die bei Offline-Einsätzen Kopfschmerzen bereiten kann.
{{< /alert >}}

---

{{< faq >}}

## Abschließende Empfehlung

Nach der Bewertung aller acht Adapter in Bezug auf Treiberreife, Hardware-Fähigkeiten und reale Anwendungsfälle sind dies die drei Optionen, die für die meisten Profis in Frage kommen:

**Budget-Wahl: [AWUS036ACM](/de/products/alfa/awus036acm/)**
Der MT7612U-Adapter mit zwei RP-SMA-Anschlüssen bietet volle Unterstützung für den Monitor-Modus und Packet Injection bei einer Linux-Treiber-Einrichtung ohne Konfiguration (In-Kernel seit 4.19). Ideal für Berater, die ein zuverlässiges, problemloses Werkzeug suchen, oder für Teams, die Adapter in größeren Mengen kaufen.

**Vielseitige Wahl: [AWUS036ACH](/de/products/alfa/awus036ach/)**
Der RTL8812AU-Adapter mit zwei Antennen und 500 mW ist der am häufigsten empfohlene Einzeladapter für Sicherheitsexperten. Er deckt 2,4 und 5 GHz ab, akzeptiert externe Antennen, hat den ausgereiftesten Treiber-Stack aller Adapter auf dieser Liste und kostet nur unwesentlich mehr als der ACM. Wenn Sie nur einen Adapter kaufen und noch nicht genau wissen, was Sie benötigen, nehmen Sie diesen.

**Flaggschiff / Zukunftssichere Wahl: [AWUS036AXML](/de/products/alfa/awus036axml/)**
Wenn Ihr Audit-Umfang Wi-Fi 6E-Infrastrukturen umfasst — was bei jedem Auftrag ab 2026 der Fall sein sollte — ist der AXML der einzige Adapter, der Ihnen USB-C 3.2, 6-GHz-Fähigkeit und Bluetooth 5.2 in einem Paket bietet. Kombinieren Sie ihn mit einem ACH für ein Zwei-Adapter-Kit, das jedes Band von 2,4 GHz bis 6 GHz ohne Kompromisse abdeckt. Für 6E-Abdeckung mit zwei Antennen sollten Sie stattdessen den AWUS036AXM in Betracht ziehen.

Detaillierte Anleitungen zur Einrichtung und Konfiguration finden Sie unter:
- [ALFA-Treiber unter Kali Linux und Ubuntu installieren](/de/blog/install-alfa-driver-kali-ubuntu/)
- [ALFA-Treiber nach Kernel-Update reparieren](/de/blog/fix-alfa-driver-kernel-update/)
- [Monitor-Modus unter Kali Linux aktivieren](/de/blog/enable-monitor-mode-kali-linux/)
- [AWUS036AXML Wi-Fi 6E Testbericht und Treibertests](/de/blog/awus036axml-wifi-6e-review/)
---

## Referenzen

1. aircrack-ng — RTL8812AU Treiber-Quellcode-Repository: [https://github.com/aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au)
2. Wi-Fi Alliance — Offizielles technisches Dokument zu Wi-Fi 6E: [https://www.wi-fi.org/](https://www.wi-fi.org/)
3. ALFA Network Offizielle Website: [https://www.alfa.com.tw](https://www.alfa.com.tw)
4. torvalds/linux — MT7921AUN KernelTreiber-Quellcode: [https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76)
