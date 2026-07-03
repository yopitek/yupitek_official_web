---
title: "ALFA-Adapter Setup-Anleitung für Windows 10 und Windows 11"
description: "So installieren und konfigurieren Sie ALFA USB-WLAN-Adapter unter Windows 10/11. Treiber-Download, Monitor-Modus mit Acrylic WiFi, Fehlerbehebung und Adaptervergleich für Windows-Nutzer."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["windows-10", "windows-11", "alfa-network", "wifi-adapter", "driver-install", "acrylic-wifi"]
featureimage: "/images/blog/alfa-adapter-windows-10-11-setup.webp"
faq:
  - question: "Unterstützt Windows den Monitor Mode für ALFA-Netzwerkkarten?"
    answer: "Windows unterstützt keinen vollständigen Monitor Mode nativ. Das NDIS-Treibermodell ermöglicht keine Rohdaten-Erfassung von 802.11-Paketen; lediglich Acrylic WiFi Pro kann passive Scans durchführen. Für den vollständigen Monitor Mode ist Kali Linux erforderlich."
  - question: "Ist Packet Injection unter Windows möglich?"
    answer: "Nein. Derzeit unterstützt kein Windows-Treiber die Packet Injection von Rohdaten-802.11-Paketen für ALFA-Netzwerkkarten. Diese Funktion ist nur unter Linux verfügbar."
  - question: "Welche ALFA-Netzwerkkarte hat die beste Kompatibilität unter Windows?"
    answer: "Die AWUS036ACH (RTL8812AU) und AWUS036ACM (MT7612U) verfügen über WHQL-signierte Treiber und weisen die umfassendsten Kompatibilitätsaufzeichnungen für Windows 10/11 auf, was Plug-and-Play am stabilsten macht."
  - question: "Erfordert Windows 11 die manuelle Installation des MT7921AUN-Treibers?"
    answer: "Nein. Der MT7921AUN-Treiber ist bereits im Windows 11-Treiberrepository (Build 22000 und höher) integriert. Nach dem Einstecken der Netzwerkkarte wird der Treiber innerhalb weniger Minuten automatisch bezogen."
  - question: "Was tun, wenn der Geräte-Manager Code 43 anzeigt?"
    answer: "Nach der Deinstallation des Treibers und einem Neustart stecken Sie die Netzwerkkarte erneut ein und installieren den Treiber manuell mit Methode B. Wenn weiterhin Fehlercode 43 auftritt und dies auf mehreren Geräten identisch ist, deutet dies in der Regel auf einen Hardwaredefekt hin."

---

ALFA Network USB-WLAN-Adapter sind in Sicherheitsforschungs- und Netzwerkkreisen bestens bekannt, aber die meisten Anleitungen konzentrieren sich ausschließlich auf Linux. Die gute Nachricht für Windows-Nutzer: Jeder gängige ALFA-Adapter funktioniert unter Windows 10 und Windows 11 mit den vom Hersteller bereitgestellten Treibern — eine Kompilierung aus dem Quellcode ist nicht erforderlich.

{{< tldr >}}
ALFA-Netzwerkkarten können unter Windows 10/11 per Plug-and-Play mit WiFi verbunden werden, aber das NDIS-Treibermodell unterstützt keinen vollständigen Monitor Mode und keine Packet Injection. Für Sicherheitstests wechseln Sie bitte zu Kali Linux (nativ oder per USB-Passthrough in einer VM). Windows eignet sich für die tägliche Verbindung und WiFi-Kartierung.
{{< /tldr >}}

Der entscheidende Unterschied zu Linux ist der Monitor-Modus. Unter Linux nutzen Tools wie `aircrack-ng` und `airodump-ng` die rohe 802.11-Erfassung mit Paket-Injektion. Unter Windows stellt das Treibermodell (NDIS) nicht dieselben Hardware-Funktionen bereit. Vollständiger Monitor-Modus und Paket-Injektion sind **nativ unter Windows nicht verfügbar**. Was Windows jedoch sehr gut beherrscht, ist Plug-and-Play-Konnektivität und WLAN-Scanning mit ausgereiften Tools wie Acrylic WiFi Analyzer.

Diese Anleitung führt Sie durch die Treiberinstallation, das WLAN-Scanning und bietet eine ehrliche Einschätzung dessen, was Windows mit einem ALFA-Adapter leisten kann und was nicht.

---

## Kompatible ALFA-Adapter für Windows

Alle unten aufgeführten Adapter werden offiziell unter Windows 10 und Windows 11 unterstützt. Die Verfügbarkeit von Treibern und die Fähigkeit zum Monitor-Modus variieren je nach Chipsatz.

<div class="table-nowrap" style="overflow-x: auto;">

| Modell | Chipsatz | Windows 10 | Windows 11 | Monitor-Modus Unterstützung |
|---|---|---|---|---|
| [AWUS036ACH](/de/products/alfa/awus036ach/) | RTL8812AU | ✅ Volle Unterstützung | ✅ Volle Unterstützung | ⚠️ Nur passiver Scan (Acrylic WiFi Pro) |
| [AWUS036ACM](/de/products/alfa/awus036acm/) | MT7612U | ✅ Volle Unterstützung | ✅ Volle Unterstützung | ⚠️ Nur passiver Scan |
| [AWUS036ACS](/de/products/alfa/awus036acs/) | RTL8811AU | ✅ Volle Unterstützung | ✅ Volle Unterstützung | ⚠️ Nur passiver Scan |
| [AWUS036AX](/de/products/alfa/awus036ax/) | RTL8832BU | ⚠️ Manueller Treiber-Download | ✅ Integrierter Treiber | ⚠️ Eingeschränkt |
| [AWUS036AXER](/de/products/alfa/awus036axer/) | RTL8832BU | ⚠️ Manueller Treiber-Download | ✅ Integrierter Treiber | ⚠️ Eingeschränkt |
| [AWUS036AXM](/de/products/alfa/awus036axm/) | MT7921AUN | ⚠️ Manueller Treiber-Download | ✅ Integrierter Treiber | ❌ Nicht unterstützt |
| [AWUS036AXML](/de/products/alfa/awus036axml/) | MT7921AUN | ⚠️ Manueller Treiber-Download | ✅ Integrierter Treiber | ❌ Nicht unterstützt |

</div>

{{< alert "circle-info" >}}
Für den täglichen Einsatz unter Windows sind der AWUS036ACH (RTL8812AU) und der AWUS036ACM (MT7612U) die am besten erprobten Optionen. Beide erhalten von Realtek/MediaTek WHQL-signierte Treiber und weisen die beste Windows-Kompatibilität auf.
{{< /alert >}}

---

## Installation des Treibers

### Methode A: Windows Update (Empfohlen)

Windows Update ist für die meisten Adapter der einfachste Weg. Wenn Sie einen unterstützten ALFA-Adapter anschließen, fragt Windows automatisch bei Windows Update nach einem passenden NDIS-Treiber.

1. Stecken Sie den ALFA-Adapter in einen USB 3.0-Anschluss.
2. Warten Sie 30–60 Sekunden. Windows zeigt eine Benachrichtigung an: *"Gerätetreibersoftware wurde erfolgreich installiert"* (Windows 10) oder schließt den Vorgang unter Windows 11 lautlos ab.
3. Öffnen Sie den **Geräte-Manager** (`Win + X` → Geräte-Manager).
4. Erweitern Sie den Bereich **Netzwerkadapter**. Sie sollten den Adapter dort gelistet sehen (z. B. *"Realtek 8812AU Wireless LAN 802.11ac USB NIC"* oder *"MediaTek Wi-Fi 6 MT7921AUN Wireless LAN Card"*).
5. Falls der Adapter mit einem gelben Warnsymbol erscheint, fahren Sie mit Methode B fort.

{{< alert "circle-info" >}}
Windows Update benötigt eine aktive Internetverbindung, um Treiber herunterzuladen. Falls Sie einen isolierten Labor-Rechner einrichten, laden Sie das Treiberpaket auf einem anderen Computer herunter und übertragen Sie es manuell, bevor Sie Methode B anwenden.
{{< /alert >}}

### Methode B: Manuelle Treiberinstallation — RTL8812AU (AWUS036ACH / AWUS036ACS)

1. Besuchen Sie die [ALFA Network Download-Seite](https://www.alfa.com.tw/service_1.html) oder das Realtek-Treiberarchiv und laden Sie den neuesten Windows WHQL-Treiber für RTL8812AU herunter.
2. Entpacken Sie das `.zip`-Archiv in einen lokalen Ordner (z. B. `C:\Treiber\RTL8812AU`).
3. Führen Sie die `.exe`-Installationsdatei als Administrator aus. Bestätigen Sie die Benutzerkontensteuerung (UAC).
4. Folgen Sie dem Installationsassistenten. Lassen Sie den Standard-Installationspfad unverändert.
5. Starten Sie den Rechner nach Abschluss der Installation neu.
6. Öffnen Sie den **Geräte-Manager** → **Netzwerkadapter**. Vergewissern Sie sich, dass der Adapter ohne Warnsymbol erscheint.

So überprüfen Sie die Treiberversion:

1. Rechtsklick auf den Adapter im Geräte-Manager → **Eigenschaften**.
2. Klicken Sie auf den Reiter **Treiber**.
3. Notieren Sie sich die **Treiberversion** und das **Treiberdatum** für spätere Zwecke.

### Methode B: Manuelle Treiberinstallation — MT7921AUN (AWUS036AXM / AWUS036AXML)

Der MediaTek MT7921AUN-Treiber ist im Treiberspeicher von Windows 11 (Build 22000+) bereits enthalten. Für Windows 10:

1. Laden Sie das MediaTek MT7921 Treiberpaket von der [offiziellen MediaTek-Website](https://www.mediatek.com/products/home-networking/wi-fi-6-6e) oder der Support-Seite von ALFA Network herunter.
2. Entpacken Sie das Paket und führen Sie `Setup.exe` als Administrator aus.
3. Starten Sie nach der Installation neu.

{{< alert "circle-info" >}}
Nutzer von Windows 11 mit MT7921AUN-Adaptern (AWUS036AXM, AWUS036AXML) erhalten normalerweise innerhalb weniger Minuten nach dem Einstecken einen funktionierenden Treiber, selbst bei einer Neuinstallation — ein manueller Download ist nicht erforderlich.
{{< /alert >}}

### Häufige Fehlercodes im Geräte-Manager

| Fehlercode | Bedeutung | Erste Lösung |
|---|---|---|
| **Code 43** | Treiber meldete einen Fehler | Treiber deinstallieren → Neustart → Neu installieren |
| **Code 10** | Gerät kann nicht gestartet werden | Anderen USB-Port versuchen; "Selektives USB-Energiesparen" deaktivieren |
| **Code 28** | Keine Treiber installiert | Windows Update ausführen oder Treiber manuell installieren |
| **Code 45** | Gerät nicht angeschlossen | Adapter erneut verbinden; anderes USB-Kabel versuchen, falls eine Verlängerung genutzt wird |

---

## Verwendung des ALFA-Adapters für WLAN-Scanning unter Windows

### WLAN-Scanning über die native Windows-Befehlszeile

Windows verfügt über einen integrierten Befehl zum Scannen von WLAN-Netzwerken, der keine zusätzliche Software erfordert:

```cmd
netsh wlan show networks mode=bssid
```

Dies listet alle sichtbaren SSIDs zusammen mit der BSSID (MAC-Adresse), Signalstärke, Funktyp, Kanal und Authentifizierungstyp auf. Dies ist nützlich für eine schnelle Diagnose, bietet aber keine Echtzeit-Kanalgrafiken oder Erkennung versteckter SSIDs.

### Acrylic WiFi Analyzer (Kostenlos)

Für eine ernsthafte WLAN-Analyse unter Windows wird das Tool [Acrylic WiFi Analyzer](https://www.acrylicwifi.com/) empfohlen. Die kostenlose Version bietet:

- Echtzeit-Scanning in den Frequenzbereichen 2,4 GHz, 5 GHz und 6 GHz
- Kanalbelegungsgrafiken — erkennen Sie sofort überlastete Kanäle
- Erkennung versteckter SSIDs (zeigt Netzwerke an, die leere SSIDs senden)
- Signalverlaufscharts für einzelne Access Points
- Hersteller-OUI-Suche zur Identifizierung von BSSIDs

Acrylic WiFi funktioniert mit jedem Windows-kompatiblen WLAN-Adapter, einschließlich aller oben aufgeführten ALFA-Modelle. Seine NDIS-Treibererweiterung integriert sich direkt in den Windows-Wireless-Stack, weshalb es auch ohne Monitor-Modus im Linux-Stil funktioniert.

{{< alert "circle-info" >}}
Acrylic WiFi Analyzer ist für das passive Scanning das nächste Windows-Äquivalent zu Tools wie `airodump-ng`. Wenn Ihr Workflow WLAN-Vermessung, Standortanalyse oder Kanalplanung umfasst, deckt es fast alles ab, was Sie benötigen, ohne Windows verlassen zu müssen.
{{< /alert >}}

### Wireshark-Erfassung unter Windows

Wireshark kann mit Hilfe von Npcap WLAN-Datenverkehr unter Windows erfassen (siehe den entsprechenden Abschnitt unten). Ohne echten Monitor-Modus erfassen Sie jedoch nur:

- Frames, die an Ihren Adapter adressiert sind (Unicast an Ihre MAC-Adresse)
- Broadcast- und Multicast-Frames in Ihrem verbundenen Netzwerk

Sie erfassen **keinen** Datenverkehr zwischen anderen Geräten, es sei denn, diese befinden sich in derselben Broadcast-Domäne und Wireshark läuft im Promiscuous-Modus in einem geswitchten Netzwerk. Die Erfassung vollständiger 802.11-Frames (Management-Frames, Beacon-Frames von fremden APs) ist eingeschränkt.

---

## Monitor-Modus unter Windows (Die ehrliche Wahrheit)

Hier müssen die Erwartungen klar definiert werden.

**Der Monitor-Modus unter Windows unterscheidet sich grundlegend vom Linux Monitor-Modus.**

Unter Linux stellen Treiber wie `aircrack-ng/rtl8812au` eine echte Monitor-Modus-Schnittstelle (`wlan0mon`) bereit, die alle 802.11-Frames in der Funkumgebung empfängt — Management-Frames, Daten-Frames von anderen Netzwerken, Probe-Requests und Beacon-Frames —, ohne dass eine Verbindung (Assoziierung) erforderlich ist. Der Adapter unterstützt zudem Paket-Injektion: das Senden von rohen 802.11-Frames auf Hardware-Ebene.

Unter Windows stellt das NDIS-Treibermodell diese Funktionen nicht bereit. Die zwei praktischen Ansätze für das Monitoring unter Windows sind:

**Ansatz A: Acrylic WiFi Pro + kompatibler Treiber**

Acrylic WiFi Pro verwendet eine benutzerdefinierte NDIS-Treibererweiterung, um *passives 802.11-Scanning* zu ermöglichen. Damit können Sie Beacon-Frames und Probe-Responses von Access Points empfangen, mit denen Sie nicht verbunden sind — ausreichend für RF-Vermessungen, Kanalanalysen und die Aufzählung von APs. Paket-Injektion oder vollständige Handshake-Erfassung werden **nicht** unterstützt.

**Ansatz B: Kali Linux Live-USB**

Für Workflows, die einen vollständigen Monitor-Modus mit Paket-Injektion erfordern — WPA-Handshake-Erfassung, Deauth-Tests, Beacon-Flooding —, ist Kali Linux die richtige Plattform. Sie haben zwei Möglichkeiten:

- Booten eines **Kali Linux Live-USB** auf demselben Rechner (Bare Metal, voller Hardware-Zugriff)
- Betrieb einer **Kali Linux VM** (VMware oder VirtualBox) mit USB-Passthrough, um den ALFA-Adapter direkt an den USB-Stack der VM durchzureichen.

Detaillierte Anweisungen zur VM-Einrichtung finden Sie in der [Anleitung für VirtualBox/VMware USB-Passthrough](/de/blog/alfa-adapter-virtualbox-vmware-usb/).

{{< alert "triangle-exclamation" >}}
Falls Ihr Workflow Monitor-Modus + Paket-Injektion erfordert — für WPA-Handshake-Erfassung, Deauthentication-Frames oder aktive 802.11-Angriffe —, kann Windows dies nicht zuverlässig leisten. Kali Linux (Bare Metal oder VM mit USB-Passthrough) ist hierfür die richtige Plattform. Derzeit unterstützt kein Windows-Treiber eine rohe 802.11-Injektion für ALFA-Adapter.
{{< /alert >}}

---

## Fehlerbehebung

### Adapter wird überhaupt nicht erkannt

1. Versuchen Sie einen anderen USB-Port — vorzugsweise USB 3.0 (blauer Anschluss). Einigen USB-Hubs fehlt die nötige Leistung für Dual-Band-Adapter.
2. Öffnen Sie den Geräte-Manager und suchen Sie unter **Andere Geräte** nach einem Eintrag mit einem gelben Fragezeichen. Dies bestätigt, dass Windows die Hardware erkennt, aber kein Treiber vorhanden ist.
3. Rechtsklick → **Treiber aktualisieren** → **Auf meinem Computer nach Treibern suchen** und wählen Sie den Ordner mit dem manuell heruntergeladenen Treiber aus.
4. Falls im Geräte-Manager gar nichts erscheint (auch nicht unter Andere Geräte), versuchen Sie ein anderes USB-Kabel (falls eine Verlängerung genutzt wird) oder testen Sie den Adapter an einem anderen Computer, um einen Hardwaredefekt auszuschließen.

### Adapter im Geräte-Manager sichtbar, aber keine Netzwerke gefunden

1. Deaktivieren Sie vorübergehend die Windows Defender Firewall, um sicherzustellen, dass sie die Initialisierung des Adapters nicht blockiert. Nach dem Test wieder aktivieren.
2. Rechtsklick auf den Adapter im Geräte-Manager → **Eigenschaften** → Reiter **Erweitert**. Suchen Sie nach Einstellungen für den **Wireless Mode** oder das **Frequenzband**. Wenn dort nur 5 GHz eingestellt ist, sehen Sie in einer reinen 2,4 GHz-Umgebung keine Netzwerke.
3. Vergewissern Sie sich, dass der Adapter nicht deaktiviert ist: Rechtsklick → **Gerät aktivieren**.
4. Führen Sie `netsh wlan show interfaces` in einer Eingabeaufforderung mit Administratorrechten aus, um den Betriebszustand des Adapters zu prüfen.

### Langsame Geschwindigkeiten oder häufige Verbindungsabbrüche unter Windows 11

Der **Connected Standby** (Modern Standby) von Windows 11 kann USB-WLAN-Adapter stören, indem USB-Geräte aggressiv in den Ruhezustand versetzt werden.

Deaktivieren Sie das selektive USB-Energiesparen:

1. Öffnen Sie **Systemsteuerung** → **Energieoptionen** → **Energiesparplaneinstellungen ändern** → **Erweiterte Energieeinstellungen ändern**.
2. Erweitern Sie **USB-Einstellungen** → **Einstellung für selektives USB-Energiesparen**.
3. Stellen Sie beide Optionen (**Auf Akku** und **Netzbetrieb**) auf **Deaktiviert**.
4. Klicken Sie auf **Übernehmen** → **OK** und starten Sie den Rechner neu.

### Code 43: Treiber meldete Fehler

1. Öffnen Sie den Geräte-Manager, Rechtsklick auf den Adapter → **Gerät deinstallieren**. Aktivieren Sie die Option *"Treibersoftware für dieses Gerät löschen"*, falls verfügbar.
2. Ziehen Sie den Adapter ab.
3. Starten Sie den Computer neu.
4. Stecken Sie den Adapter wieder ein.
5. Installieren Sie den Treiber gemäß Methode B neu.

Falls Code 43 nach einer sauberen Neuinstallation weiterhin besteht, versuchen Sie einen anderen USB-Port oder testen Sie das Gerät an einem anderen Rechner. Ein dauerhafter Code 43 auf mehreren Rechnern deutet meist auf einen Hardwaredefekt des Adapters hin.

---

## ALFA-Adapter + Wireshark Setup

Wireshark unter Windows benötigt **Npcap** als Bibliothek zur Paketerfassung. WinPcap (die veraltete Alternative) wird nicht mehr gepflegt und unterstützt moderne Windows-Versionen nicht zuverlässig.

### Schritt 1: Installieren Sie Npcap

1. Laden Sie Npcap von [https://npcap.com/](https://npcap.com/) herunter (kostenlos für den persönlichen und pädagogischen Gebrauch).
2. Führen Sie das Installationsprogramm als Administrator aus.
3. Aktivieren Sie während der Installation die Option **"Install Npcap in WinPcap API-compatible mode"**, falls Sie ältere Tools parallel zu Wireshark nutzen möchten.
4. Starten Sie neu.

### Schritt 2: Konfigurieren Sie Wireshark

1. Öffnen Sie Wireshark. Ihr ALFA-Adapter erscheint in der Liste der Schnittstellen.
2. Doppelklicken Sie auf die Schnittstelle des Adapters, um die Erfassung zu starten.
3. Um nach 802.11-Management-Frames (Beacon-Frames, Probe-Requests) zu filtern, nutzen Sie den Wireshark-Anzeigefilter:

```
wlan.fc.type == 0
```

4. Speziell für Probe-Requests:

```
wlan.fc.type_subtype == 0x0004
```

{{< alert "circle-info" >}}
Der Filter `wlan.fc.type` funktioniert nur, wenn Wireshark tatsächliche 802.11-Frames mit sichtbaren Headern empfängt. Unter Windows ohne Monitor-Modus zeigen die meisten Erfassungen Ethernet II-Frames, selbst über WLAN — die NDIS-Schicht entfernt den 802.11-Header, bevor die Frames an Npcap übergeben werden. Eine vollständige Erfassung des 802.11-Headers erfordert eine echte Monitor-Modus-Schnittstelle, wie sie unter Linux verfügbar ist.
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
Das Erfassen von Netzwerkverkehr ohne Genehmigung ist in den meisten Ländern illegal. Erfassen Sie nur Datenverkehr in Netzwerken, die Ihnen gehören oder für die Sie eine ausdrückliche schriftliche Erlaubnis zum Testen haben.
{{< /alert >}}

---

## Zusammenfassung: Windows vs. Linux für ALFA-Adapter

| Merkmal | Windows 10/11 | Kali Linux |
|---|---|---|
| **Plug & Play** | ✅ Automatische Treiberinstallation | ⚠️ Variiert je nach Chipsatz |
| **WLAN-Scanning** | ✅ Acrylic WiFi / netsh | ✅ airodump-ng / iwlist |
| **Monitor-Modus** | ⚠️ Nur passiv (Acrylic Pro) | ✅ Voller Monitor-Modus |
| **Paket-Injektion** | ❌ Nicht unterstützt | ✅ Volle Injektion |
| **Wireshark-Erfassung** | ⚠️ Eingeschränkt (keine 802.11-Header) | ✅ Volle 802.11-Erfassung |
| **WPA-Handshake-Erfassung** | ❌ Nicht zuverlässig | ✅ aircrack-ng / hcxdumptool |
| **Bester Einsatzbereich** | Täglicher Gebrauch, WLAN-Vermessung, Kanalanalyse | Sicherheitstests, CTF-Herausforderungen, Penetrationstests |

Fazit: Windows ist eine exzellente Plattform für ALFA-Adapter, wenn Ihr Ziel Netzwerkkonnektivität, WLAN-Analyse und Kanalplanung ist. Sobald Ihr Workflow jedoch rohe 802.11-Paket-Injektion oder WPA-Handshake-Erfassung erfordert, sollten Sie auf Kali Linux wechseln — entweder nativ oder über eine VM mit USB-Passthrough.

---

{{< faq >}}

## Verwandte Anleitungen

- [VirtualBox & VMware USB-Passthrough für ALFA-Adapter](/de/blog/alfa-adapter-virtualbox-vmware-usb/) — Kali Linux in einer VM mit voller ALFA-Adapter-Unterstützung betreiben
- [Treiber-Installationsanleitung für Kali Linux & Ubuntu](/de/blog/install-alfa-driver-kali-ubuntu/) — Vollständige chipsatzspezifische Treiberinstallation
- [ALFA WLAN-Adapter Kaufberatung 2026](/de/blog/alfa-wifi-adapter-buyer-guide-2026/) — Welcher Adapter ist der richtige für Sie?

## Referenzen

1. [ALFA Network Offizielle Treiber-Downloads](https://www.alfa.com.tw/service_1.html)
2. [Microsoft NDIS Treiber-Dokumentation](https://learn.microsoft.com/windows-hardware/drivers/network/ndis-drivers)
3. [Acrylic WiFi Analyzer Offizielle Website](https://www.acrylicwifi.com/)
4. [Npcap Offizielle Website](https://npcap.com/)
5. [Wireshark Offizielle Dokumentation](https://www.wireshark.org/docs/)
