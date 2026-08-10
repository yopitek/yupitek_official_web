---
title: "Verwendung von ALFA WiFi-Adaptern auf macOS: USB-Passthrough mit VMware Fusion & Parallels"
description: "So verwenden Sie ALFA USB-WiFi-Adapter auf macOS. Behandelt native macOS-Unterstützung, VMware Fusion USB-Passthrough und Parallels Desktop für Kali Linux Monitor-Modus und Packet-Injection."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["macos", "vmware-fusion", "parallels", "kali-linux", "usb-passthrough", "alfa-network", "AWUS036AXML"]
featureimage: "/images/blog/alfa-adapter-macos-vm-setup.webp"
faq:
  - question: "Können ALFA-Netzwerkkarten auf macOS nativ im Monitor-Mode verwendet werden?"
    answer: "Nein. Die CoreWLAN- und IO80211Family-Architektur von macOS unterstützt weder den Monitor-Mode noch Packet Injection für Drittanbieter-Netzwerkkarten. Es ist erforderlich, Kali Linux in einer VM auszuführen und USB-Passthrough zu nutzen."
  - question: "Sollte man für Apple Silicon Macs VMware Fusion oder Parallels wählen?"
    answer: "Beide sind geeignet, aber Parallels Desktop 19+ bietet auf Apple Silicon in der Regel eine bessere ARM64-VM-Leistung und eine stabilere USB-Passthrough-Funktion als VMware Fusion."
  - question: "Muss der Treiber für die AWUS036AXML in einer Kali VM auf Apple Silicon kompiliert werden?"
    answer: "Nein. Der MT7921AUN-Treiber ist seit Linux 5.18 im Kernel integriert. Ab Kali ARM64 Version 2024.x wird die Karte beim Einstecken automatisch erkannt."
  - question: "Kann man auf Intel Macs das Standard-Kali x86_64 ISO verwenden?"
    answer: "Ja. Intel Macs basieren auf der x86_64-Architektur und können direkt das offizielle Standard-Kali Linux x86_64 ISO von kali.org verwenden, um eine VM zu erstellen."
  - question: "Ist VirtualBox für Sicherheits Tests auf Apple Silicon geeignet?"
    answer: "Nicht empfohlen. Die Unterstützung von VirtualBox für Apple Silicon ist noch experimentell, und USB-Passthrough weist bekannte Probleme auf. Verwenden Sie stattdessen VMware Fusion oder Parallels."
---

macOS ist ein ausgefeiltes Betriebssystem für den professionellen Einsatz. Es ist jedoch keine Plattform, die für die drahtlose Sicherheitsforschung entwickelt wurde. Die beiden Funktionen, die das Toolkit jedes ernsthaften Pentesters definieren – **Monitor-Modus** und **Packet-Injection** – fehlen im macOS Wi-Fi-Stack vollständig. Die Wi-Fi-Treiber von Apple bieten eine saubere, funktionale Netzwerk-Schnittstelle und mehr nicht.

{{< tldr >}}
macOS unterstützt den Monitor-Mode und Packet Injection für ALFA-Netzwerkkarten nicht. Die Lösung besteht darin, eine Kali Linux VM in VMware Fusion oder Parallels auszuführen und die Netzwerkkarte über USB-Passthrough an die VM zu übergeben. Apple Silicon erfordert ein ARM64-Kali-Image.
{{< /tldr >}}

ALFA Network Adapter ändern dieses Szenario unter Linux, wo die Treiberunterstützung umfassend und von der Community getestet ist. Auf macOS sieht die Situation anders aus. Selbst wenn ein ALFA-Adapter von macOS erkannt wird, lässt der native Netzwerk-Stack Sie nicht in den Monitor-Modus wechseln oder rohe Frames injizieren. Der einzige zuverlässige Weg nach vorne besteht darin, **Kali Linux in einer virtuellen Maschine** auszuführen und den USB-Adapter direkt an das Gast-Betriebssystem durchzureichen (Passthrough), wobei macOS vollständig umgangen wird.

Dieser Leitfaden beschreibt, wie Sie dies bei beiden großen macOS-Hypervisoren – VMware Fusion und Parallels Desktop – korrekt durchführen, mit besonderem Augenmerk auf **Apple Silicon (M1/M2/M3)**, das ARM-Architekturbeschränkungen einführt, die die Auswahl von Adaptern und ISO-Dateien nicht trivial machen.

---

## macOS Nativ: Was ohne VM funktioniert

Bevor Sie direkt zur Einrichtung einer VM übergehen, lohnt es sich zu verstehen, was macOS mit einem ALFA-Adapter alleine tun kann und was nicht.

**AWUS036AXML (MT7921AUN Chipsatz):** Dieser Adapter wird von macOS als generisches USB-Netzwerkgerät erkannt. Der **MT7921AUN**-Treiber, der mit macOS 13 Ventura und neuer ausgeliefert wird, erkennt den Adapter automatisch. Er erscheint in den **Systemeinstellungen → Netzwerk** als neue Schnittstelle und kann wie jeder andere Adapter eine Verbindung zu Wi-Fi-Netzwerken herstellen. Auf älteren macOS-Versionen wird er möglicherweise überhaupt nicht erkannt.

**AWUS036ACH (RTL8812AU) und AWUS036ACM (MT7612U) – Adapter, die macOS-Treiber von Drittanbietern benötigen:** Diese erfordern einen Treiber von Drittanbietern für macOS. Es existieren mehrere Treiberpakete von der Community oder kommerziellen Anbietern, aber die Kompatibilität ist fragil. Neuinstallationen der Treiber nach macOS-Punkt-Updates sind üblich, die Anforderungen an die Signierung von Kernel-Erweiterungen wurden seit macOS 11 verschärft, und auf Apple Silicon ist die Situation aufgrund von Rosetta-Einschränkungen bei Kernel-Erweiterungen noch instabiler. Eine funktionale Installation ist möglich, aber wartungsintensiv.

**Die harte Grenze – kein Monitor-Modus:** Unabhängig davon, welchen Adapter Sie verwenden oder welchen Treiber Sie installieren, stellt macOS keine Schnittstelle für den rohen Monitor-Modus zur Verfügung. Das CoreWLAN-Framework und die zugrunde liegende `IO80211Family.kext`-Architektur unterstützen dies für Adapter von Drittanbietern nicht. Tools wie Wireshark können den Wi-Fi-Verkehr auf macOS mit dem integrierten Airport-Adapter über `en0` erfassen, aber das ist nur eine passive Erfassung – es entspricht nicht dem Monitor-Modus von airmon-ng, und Packet-Injection ist nicht möglich.

{{< alert "circle-info" >}}
Wenn Ihr Ziel lediglich die passive Erfassung von Wi-Fi-Verkehr zu Debugging-Zwecken ist (keine Sicherheitstests), können Sie unter macOS die Optionstaste gedrückt halten und auf das Wi-Fi-Menüleistensymbol klicken, um in einen Diagnosemodus zu gelangen. Dies ist kein Ersatz für einen echten Monitor-Modus-Workflow.
{{< /alert >}}

Für Sicherheitstests – das Scannen nach Netzwerken, das Erfassen von WPA-Handshakes, das Durchführen von Deauthentication-Angriffen oder das Testen von Injektionen – ist eine Kali-Linux-VM mit USB-Passthrough die erforderliche Konfiguration auf macOS.

---

## Apple Silicon (M1/M2/M3) vs. Intel-Mac

Die Architektur Ihres Macs bestimmt, welches Kali-Linux-Image Sie benötigen und welche Hypervisoren geeignet sind. Dies ist die häufigste Ursache für Verwirrung bei macOS-Benutzern, die eine VM für Sicherheitstests einrichten.

**Intel-Mac (x86_64):**
Alle drei großen Hypervisoren – VMware Fusion, Parallels Desktop und VirtualBox – laufen nativ auf Intel-Macs. Sie können die Standard-**Kali Linux x86_64 ISO** von der offiziellen kali.org-Downloadseite verwenden. Die Treiberkompilierung innerhalb der VM folgt den gleichen Schritten, die in jedem Kali-Leitfaden online dokumentiert sind, da die Architektur übereinstimmt.

**Apple Silicon (M1/M2/M3):**
Apple Silicon ist ARM64. Eine Standard-x86_64-Kali-ISO wird auf Apple-Silicon-Hardware nicht booten, auch nicht innerhalb eines Hypervisors – es gibt keine x86-Emulationsschicht auf VM-Ebene (Rosetta gilt nur für Anwendungen im macOS-Benutzerbereich, nicht für die vollständige OS-Virtualisierung). Sie müssen das **Kali Linux ARM64**-Image verwenden, das unter [kali.org/get-kali](https://www.kali.org/get-kali/) im Abschnitt Apple Silicon / ARM verfügbar ist.

| Hypervisor | Intel-Mac | Apple Silicon |
|---|---|---|
| VMware Fusion 13+ | ✅ Kostenlose persönliche Lizenz | ✅ ARM64-VMs unterstützt |
| Parallels Desktop 19+ | ✅ | ✅ Beste Apple Silicon Performance |
| VirtualBox 7.x | ✅ | ⚠️ Experimentell auf Apple Silicon |

{{< alert "triangle-exclamation" >}}
Die VirtualBox-Unterstützung für Apple Silicon wird immer noch als experimentell eingestuft. Insbesondere USB-Passthrough hat bekannte Probleme auf M-Chip-Macs. Verwenden Sie für Sicherheitstests auf Apple-Silicon-Hardware VMware Fusion oder Parallels Desktop.
{{< /alert >}}

**USB-Passthrough ist architekturunabhängig:** Der ALFA-Adapter selbst ist ein USB-Gerät. Ob die Host-CPU x86_64 oder ARM64 ist, hat keinen Einfluss darauf, wie USB-Passthrough funktioniert. Der Adapter wird über den USB-Bus an die Gast-VM übergeben, und der Treiber innerhalb von Kali übernimmt von dort aus. Die Architektur beeinflusst nur, welches Kali-Image Sie verwenden und wie die Treiber innerhalb der VM kompiliert werden.

---

## Option A: VMware Fusion USB-Passthrough

VMware Fusion ist seit Version 13 für den persönlichen Gebrauch kostenlos erhältlich und ist damit die Standardempfehlung für macOS-Benutzer, die einen kostenlosen Hypervisor mit solider USB-Passthrough-Unterstützung suchen.

### Schritt 1 – Installieren Sie VMware Fusion 13+

Laden Sie VMware Fusion von [vmware.com/products/fusion.html](https://www.vmware.com/products/fusion.html) herunter. Während der Installation werden Sie aufgefordert, die VMware-Systemerweiterung in den **Systemeinstellungen → Datenschutz & Sicherheit** zu erlauben. Diese Genehmigung ist erforderlich, damit USB-Passthrough funktioniert – ohne sie kann VMware keine USB-Ereignisse vom macOS USB-Stack abfangen.

Nach der Genehmigung fordert macOS möglicherweise einen Neustart an. Schließen Sie den Neustart ab, bevor Sie fortfahren.

### Schritt 2 – Erstellen Sie Ihre Kali-Linux-VM

- **Apple Silicon Mac:** Laden Sie den Kali Linux ARM64 Installer oder das vorgefertigte Parallels/VMware ARM-Image von kali.org herunter. Erstellen Sie in VMware Fusion eine neue VM und wählen Sie die ARM64-ISO aus.
- **Intel-Mac:** Laden Sie die Standard-Kali Linux x86_64 ISO herunter. Erstellen Sie eine neue VM und wählen Sie die ISO als Installationsmedium aus.

Weisen Sie mindestens **4 GB RAM** und **40 GB Festplattenspeicher** für eine funktionale Kali-Installation zu. Installieren Sie während des Kali-Setups den vollständigen Standard-Paketsatz, um die Wireless-Tools (aircrack-ng, airmon-ng, airodump-ng) sofort einsatzbereit zu haben.

### Schritt 3 – Verbinden Sie den ALFA-Adapter über USB-Passthrough

Bei laufender Kali-VM und eingestecktem ALFA-Adapter an Ihrem Mac:

1. VMware Fusion zeigt ein Pop-up an: **"Ein USB-Gerät möchte eine Verbindung zu Ihrer virtuellen Maschine herstellen."**
2. Klicken Sie auf **Mit [VM-Name] verbinden**, um den Adapter direkt an die Kali-VM zu übergeben.
3. macOS verliert an diesem Punkt die Sichtbarkeit des Adapters – er gehört nun exklusiv der VM.

{{< alert "circle-info" >}}
Wenn das Pop-up nicht erscheint (z. B. wenn der Adapter bereits vor dem Start der VM eingesteckt war), gehen Sie in der VMware Fusion-Menüleiste auf: **Virtuelle Maschine → USB & Bluetooth → [ALFA-Adaptername] → Verbinden (Von Mac trennen)**. Dies weist das USB-Gerät der VM manuell zu.
{{< /alert >}}

### Schritt 4 – Überprüfung innerhalb von Kali

Öffnen Sie ein Terminal in der Kali-VM und bestätigen Sie, dass der Adapter sichtbar ist:

```bash
lsusb | grep -i mediatek
# AWUS036AXML / MT7921AUN: Bus 001 Device 002: ID 0e8d:7961 MediaTek Inc. ...

lsusb | grep -i realtek
# AWUS036ACH / RTL8812AU: Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. ...
```

Wenn keiner der Befehle eine Ausgabe liefert, wurde das Passthrough nicht abgeschlossen – überprüfen Sie das VMware-Gerätemenü erneut.

### Schritt 5 – Treiber laden und Monitor-Modus verifizieren

Für den MT7921AUN (AWUS036AXML) ist der Treiber in den Kali-Kernel integriert. Für RTL8812AU-Adapter ist eine Treiberinstallation erforderlich – siehe den [Treiber-Installationsleitfaden](/de/blog/install-alfa-driver-kali-ubuntu/). Sobald der Treiber aktiv ist:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
```

Eine Live-Scan-Ausgabe von airodump-ng bestätigt, dass Passthrough, Laden des Treibers und Monitor-Modus einwandfrei funktionieren.

---

## Option B: Parallels Desktop USB-Passthrough

Parallels Desktop ist der bevorzugte Hypervisor für Apple-Silicon-Macs, wenn die Leistung Priorität hat. Er ist nicht kostenlos – eine Abonnementlizenz ist erforderlich –, aber seine ARM64-VM-Unterstützung und USB-Passthrough-Implementierung sind ausgereifter als bei VMware Fusion auf Apple-Silicon-Hardware.

### Schritt 1 – Parallels Desktop 19+

Installieren Sie Parallels Desktop von [parallels.com](https://www.parallels.com). Der gleiche Ablauf für die Genehmigung der Systemerweiterung gilt wie bei VMware Fusion. Erlauben Sie die Parallels-Systemerweiterung unter **Datenschutz & Sicherheit** und starten Sie nach Aufforderung neu.

### Schritt 2 – Kali-Linux-ARM64-VM erstellen

Auf Apple Silicon arbeitet Parallels ausschließlich mit ARM64-Gast-OS-Images. Laden Sie das Kali Linux ARM64-Image von kali.org herunter und erstellen Sie in Parallels eine neue VM mit diesem Image.

{{< alert "circle-info" >}}
Parallels Desktop 19+ kann Kali Linux ARM direkt über den neuen VM-Assistenten auf Apple Silicon herunterladen und installieren – Sie müssen die ISO möglicherweise nicht manuell herunterladen.
{{< /alert >}}

Auf Intel-Macs funktioniert die Standard-x86_64-Kali-ISO ohne Modifikation mit Parallels.

### Schritt 3 – ALFA-Adapter über USB verbinden

Bei laufender Kali-VM und eingestecktem ALFA-Adapter:

1. Gehen Sie in der macOS-Menüleiste auf **Geräte → USB & Bluetooth**.
2. Suchen Sie Ihren ALFA-Adapter in der Liste (er kann als **Realtek 802.11ac NIC**, **MediaTek Wi-Fi** oder ähnlich erscheinen).
3. Klicken Sie darauf und wählen Sie **Mit Linux verbinden** (oder Ihren VM-Namen).

Parallels trennt den Adapter von macOS und übergibt ihn exklusiv an die Kali-VM.

### Schritt 4 – Verifizierung mit lsusb

Im Terminal der Kali-VM:

```bash
lsusb
ip link show
```

Der ALFA-Adapter sollte in der `lsusb`-Ausgabe und als neue `wlan`-Schnittstelle in der `ip link show`-Ausgabe erscheinen. Wenn die Schnittstelle nicht sichtbar ist, verbinden Sie das Gerät über das Parallels-Gerätemenü erneut.

{{< alert "circle-info" >}}
Parallels auf Apple Silicon übertrifft VMware Fusion bei I/O-intensiven VM-Workloads konsequent. Wenn Sie lange airodump-ng-Sitzungen ausführen oder umfangreiche Paketerfassungen durchführen, erzeugt Parallels im Allgemeinen einen geringeren CPU-Overhead.
{{< /alert >}}

---

## Kali auf Apple Silicon: ARM64-Treiberhinweise

Das Ausführen von Kali ARM64 in einer VM auf Apple Silicon ändert die Umgebung für die Treiberkompilierung. Die meisten Online-Leitfäden gehen von x86_64 aus, aber die Schritte sind fast identisch – der Hauptunterschied besteht darin, welche Pakete vorinstalliert sind und wie DKMS mit ARM-Kernel-Headern umgeht.

**RTL8812AU auf ARM64:**
Der RTL8812AU-Treiber von [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) lässt sich auf ARM64 korrekt kompilieren. Der DKMS-Build-Prozess ist derselbe wie auf x86_64 – klonen Sie das Repo, führen Sie `dkms`-Befehle aus, und das Modul wird gegen die ARM64-Kernel-Header erstellt:

```bash
sudo apt update && sudo apt install -y dkms linux-headers-$(uname -r) build-essential
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

Planen Sie einige Minuten für die Kompilierung ein. Das resultierende Modul ist architekturspezifisch für Ihren ARM64-Kernel.

**MT7921AUN auf ARM64:**
Der `mt7921u`-Treiber ist **seit Linux 5.18 im Kernel integriert** und in Kali ARM64 2024.x und neuer enthalten. Für den AWUS036AXML auf Kali ARM64 ist keine manuelle Kompilierung erforderlich. Der Adapter wird nach dem USB-Passthrough automatisch erkannt.

```bash
dmesg | grep mt7921
# [ 4.123456] mt7921u 1-1:1.0: HW/SW Version: 0x8a108a10, Build Time: ...
```

**Empfehlung für M-Chip-Macs:** Wenn Sie einen ALFA-Adapter speziell für die Verwendung auf einem Apple-Silicon-Mac mit Kali in einer VM kaufen, ist der **AWUS036AXML (MT7921AUN)** die bessere Wahl. Sein integrierter Treiber macht den DKMS-Kompilierungsschritt überflüssig und funktioniert zuverlässig auf ARM64-Kali-Builds. Der AWUS036ACH ist funktional, erfordert aber den RTL8812AU-Out-of-Tree-Treiber, was eine Wartungsabhängigkeit von der Verfügbarkeit der Kernel-Header mit sich bringt.

---

## Monitor-Modus und Injektionstest

Nach Abschluss des USB-Passthrough mit entweder VMware Fusion oder Parallels führen Sie die folgende Befehlsfolge aus, um zu überprüfen, ob der gesamte Stack funktioniert – von der USB-Sichtbarkeit bis zur Aktivierung des Monitor-Modus:

```bash
# 1. Bestätigen, dass das USB-Gerät sichtbar ist
lsusb

# 2. Liste der drahtlosen Schnittstellen anzeigen
ip link show

# 3. Konfliktbehaftete Prozesse beenden (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# 4. Monitor-Modus auf der drahtlosen Schnittstelle starten
sudo airmon-ng start wlan1

# 5. Bestätigen, dass die Monitor-Schnittstelle erstellt wurde
ip link show wlan1mon

# 6. Passiven Scan starten
sudo airodump-ng wlan1mon
```

Eine erfolgreiche airodump-ng-Ausgabe – mit SSIDs, BSSIDs, Kanälen und Client-Geräten – bestätigt, dass USB-Passthrough, Laden des Treibers, Monitor-Modus und Paketempfang durchgängig funktionieren.

**Wenn `wlan1` nach dem Passthrough nicht erscheint:**

1. Trennen Sie den ALFA-Adapter von Ihrem Mac.
2. Warten Sie fünf Sekunden und stecken Sie ihn wieder ein.
3. Weisen Sie ihn der VM über das USB-Gerätemenü des Hypervisors erneut zu (Virtuelle Maschine → USB & Bluetooth in VMware Fusion; Geräte → USB & Bluetooth in Parallels).
4. Führen Sie `lsusb` innerhalb von Kali erneut aus, um zu bestätigen, dass das Gerät erscheint.

{{< alert "triangle-exclamation" >}}
Versuchen Sie nicht, `airmon-ng start wlan0` auf der Standard-Schnittstelle `wlan0` innerhalb der VM auszuführen – diese Schnittstelle ist normalerweise der virtuelle VMware/Parallels-Netzwerkadapter für die Internetverbindung, nicht der durchgereichte ALFA-Adapter. Die Verwendung der falschen Schnittstelle unterbricht die Netzwerkverbindung Ihrer VM, ohne den Monitor-Modus auf dem ALFA-Adapter zu aktivieren.
{{< /alert >}}

---

## Leistung und Einschränkungen

**USB-Passthrough-Latenz:** Das Durchreichen eines USB-Geräts durch eine Hypervisor-Schicht fügt im Vergleich zur Verwendung des Adapters auf nativem Linux eine Verarbeitungs-Latenz von etwa 1–2 ms hinzu. Für 802.11-Sicherheitstests – Paketerfassung, Handshake-Sammlung, Injektionstests – ist diese Latenz betrieblich nicht signifikant. Sie würde nur bei latenzkritischen Echtzeitanwendungen eine Rolle spielen, was Sicherheitstests nicht sind.

**Exklusiver Besitz:** macOS kann den ALFA-Adapter nicht gleichzeitig mit der Kali-VM teilen. Sobald der Adapter an die VM durchgereicht wurde, verschwindet er vollständig aus macOS. Um ihn an macOS zurückzugeben (beispielsweise um ihn als normalen Wi-Fi-Adapter zu verwenden), trennen Sie ihn über das USB-Gerätemenü des Hypervisors von der VM und ziehen Sie den Adapter dann ab und stecken Sie ihn wieder ein. macOS wird ihn wieder als Standard-Schnittstelle beanspruchen.

**Stromverbrauch:** Der Betrieb eines USB-Wi-Fi-Adapters (der HF-Energie mit bis zu 100 mW sendet) innerhalb einer VM auf einem Mac, auf dem auch ein eigenes Wi-Fi-Radio läuft, stellt einen erheblichen Stromverbrauch dar. Lange airodump-ng-Sitzungen oder Injektionstests können den Akku eines MacBooks deutlich schneller entladen als im Normalbetrieb. **Verwenden Sie das Ladegerät bei längeren Testsitzungen** – insbesondere bei Apple-Silicon-MacBooks, bei denen das Batteriemanagement eng mit dem thermischen Bereich integriert ist.

**VM-Snapshot vor dem Test:** Sowohl VMware Fusion als auch Parallels unterstützen VM-Snapshots. Wenn Sie vor einer Testsitzung einen Snapshot einer sauberen, konfigurierten Kali-Installation erstellen, können Sie zu einem bekannten funktionierenden Zustand zurückkehren, falls ein Treiber-Update oder eine Konfigurationsänderung etwas beschädigt.

---

## Fehlerbehebung

| Symptom | Wahrscheinliche Ursache | Lösung |
|---|---|---|
| ALFA-Adapter erscheint nicht im Hypervisor-USB-Menü | macOS-Systemerweiterung nicht genehmigt | **Systemeinstellungen → Datenschutz & Sicherheit** → VMware / Parallels Erweiterung erlauben, dann neu starten |
| `lsusb` zeigt keinen ALFA-Adapter innerhalb der Kali-VM | USB-Passthrough nicht abgeschlossen | Manuell über das Menü VM → USB & Bluetooth verbinden; Adapter neu einstecken |
| Schnittstelle `wlan1` fehlt nach Passthrough | Treiber nicht geladen (RTL8812AU) | Installieren Sie den RTL8812AU-Treiber über DKMS; siehe [Treiber-Installationsleitfaden](/de/blog/install-alfa-driver-kali-ubuntu/) |
| `airmon-ng start wlan1` schlägt fehl mit "Operation not permitted" | NetworkManager blockiert die Schnittstelle | Führen Sie zuerst `sudo airmon-ng check kill` aus; dann erneut versuchen |
| Monitor-Modus startet, aber airodump-ng zeigt keine Netzwerke | Falscher Kanal oder falsche Schnittstelle | Bestätigen Sie mit `ip link show`, dass `wlan1mon` existiert; versuchen Sie `sudo airodump-ng --band abg wlan1mon` |
| VM friert ein, wenn der ALFA-Adapter eingesteckt wird | USB-Controller-Konflikt (VMware) | VM herunterfahren, zu VM-Einstellungen → USB gehen, Controller von USB 3.0 auf USB 2.0 umstellen, VM neu starten |

{{< alert "circle-info" >}}
Speziell auf Apple Silicon: Wenn der ALFA-Adapter erkannt wird, aber die Schnittstelle in Kali nicht erscheint, überprüfen Sie unmittelbar nach dem Einstecken `dmesg | tail -30`. Die Ausgabe zeigt an, ob der Kernel das Gerät erkennt und welcher Treiber (falls vorhanden) versucht, sich daran zu binden.
{{< /alert >}}

---

{{< faq >}}

## Verwandte Leitfäden

Für Windows- und Linux-Hosts mit VirtualBox oder VMware Workstation siehe den Begleit-Leitfaden: [ALFA Adapter USB Passthrough: VirtualBox & VMware Setup-Leitfaden](/de/blog/alfa-adapter-virtualbox-vmware-usb/).

Für adapterspezifische Details zum AWUS036AXML, der in diesem Leitfaden empfohlen wird, einschließlich Benchmarks für das 6-GHz-Band und Hinweisen zur Treiberversion, siehe den vollständigen Testbericht: [ALFA AWUS036AXML WiFi 6E Testbericht](/de/blog/awus036axml-wifi-6e-review/).

## Referenzen

1. [ALFA Network Offizielle Website](https://www.alfa.com.tw/)
2. [Kali Linux Offizielle Download-Seite](https://www.kali.org/get-kali/)
3. [VMware Fusion Produktseite](https://www.vmware.com/products/fusion.html)
4. [Parallels Desktop Offizielle Website](https://www.parallels.com/)
5. [aircrack-ng rtl8812au Treiber-Projekt](https://github.com/aircrack-ng/rtl8812au)
