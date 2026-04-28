---
title: "ALFA-Adapter USB-Passthrough: VirtualBox & VMware Setup-Anleitung"
description: "Schritt-für-Schritt-Anleitung für den ALFA USB-WLAN-Adapter USB-Passthrough in VirtualBox und VMware Workstation für Kali Linux. Behandelt AWUS036ACH, AWUS036AXML, USB 3.0-Filter, Extension Pack und Fehlerbehebung."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "alfa-network", "AWUS036ACH", "AWUS036AXML"]
---

Den Betrieb eines ALFA-WLAN-Adapters in einer virtuellen Maschine (VM) einzurichten, ist nicht so einfach wie das bloße Einstecken in der Hoffnung, dass das Gast-Betriebssystem ihn erkennt. Im Gegensatz zu freigegebenen Ordnern oder Bridge-Netzwerken erfordern der Monitor-Modus und die Paket-Injektion eine **vollständige USB-Kontrolle** — die VM muss exklusiven Zugriff auf das USB-Gerät haben und darf es nicht über den Netzwerkstack des Hosts teilen. Dies nennt man USB-Passthrough. Diesen Prozess korrekt einzurichten, ist die häufigste Hürde für Pentesters und CTF-Spieler, die in VMs arbeiten.

Diese Anleitung deckt das vollständige Passthrough-Setup für **VirtualBox 7.x** und **VMware Workstation 17+ / VMware Fusion 13+** ab, wobei Kali Linux als Gast-Betriebssystem dient. Wir gehen sowohl auf den AWUS036ACH (RTL8812AU-Chipsatz) als auch auf den neueren AWUS036AXML (MT7921AUN-Chipsatz) ein, mit spezifischen Hinweisen für beide Adapter.

Am Ende wird Ihr ALFA-Adapter in Kali über `lsusb` angezeigt, der richtige Treiber wird geladen sein und `airmon-ng` wird bestätigen, dass der Monitor-Modus funktioniert.

---

## Voraussetzungen

Bevor Sie beginnen, vergewissern Sie sich, dass Ihre Umgebung den folgenden Anforderungen entspricht. Das Fehlen einer dieser Komponenten — insbesondere des VirtualBox Extension Packs — ist die Hauptursache für die meisten Passthrough-Fehler.

| Anforderung | Details |
|---|---|
| **Hypervisor** | VirtualBox 7.x + Extension Pack **oder** VMware Workstation 17+ / Fusion 13+ |
| **Gast-Betriebssystem** | Kali Linux 2024.x oder neuer (getestet mit 2024.1–2025.1) |
| **ALFA-Adapter** | AWUS036ACH, AWUS036AXML, AWUS036ACM oder jedes RTL8812AU / MT7921AUN Gerät |
| **Host-USB-Anschluss** | USB 3.0 empfohlen (besonders für AWUS036AXML) |
| **Host-Betriebssystem** | Windows 10/11, Linux oder macOS (Fusion) |
| **Sudo-Zugriff** | Erforderlich innerhalb der Kali-VM |

{{< alert "circle-info" >}}
Falls Sie den Treiber in Kali noch nicht installiert haben, führen Sie zuerst die USB-Passthrough-Schritte in dieser Anleitung aus. Sobald der Adapter in der VM sichtbar ist, folgen Sie der [ALFA-Treiber-Installationsanleitung](/de/blog/install-alfa-driver-kali-ubuntu/), um den korrekten Treiber zu kompilieren und zu laden.
{{< /alert >}}

---

## VirtualBox USB-Passthrough — Schritt für Schritt

VirtualBox benötigt eine zusätzliche Komponente — das **Extension Pack** —, um USB 2.0 und USB 3.0 Passthrough zu unterstützen. Ohne dieses ist nur USB 1.1 (OHCI) verfügbar, was für moderne ALFA-Adapter nicht ausreicht.

### Installieren Sie das VirtualBox Extension Pack

1. Öffnen Sie [virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads).
2. Klicken Sie unter **VirtualBox Extension Pack** auf **All supported platforms**, um die Datei `.vbox-extpack` herunterzuladen. Die Version muss exakt mit Ihrer installierten VirtualBox-Version übereinstimmen.
3. Öffnen Sie VirtualBox, gehen Sie zu **Datei → Einstellungen → Zusatzpakete** (auf macOS: **VirtualBox → Einstellungen → Erweiterungen**).
4. Klicken Sie auf das **+**-Symbol, suchen Sie das heruntergeladene `.vbox-extpack` und installieren Sie es. Akzeptieren Sie die Lizenzbedingungen.

So überprüfen Sie über die Befehlszeile, ob das Extension Pack aktiv ist:

```bash
VBoxManage list extpacks
```

Erwartete Ausgabe:

```
Extension Packs: 1
Pack no. 0:   Oracle VirtualBox Extension Pack
Version:      7.0.x
...
Usable:       true
```

{{< alert "triangle-exclamation" >}}
Wenn das Feld **Usable** den Wert `false` anzeigt, stimmt die Version des Extension Packs nicht mit Ihrer VirtualBox-Version überein. Deinstallieren Sie es und installieren Sie die korrekte Version neu.
{{< /alert >}}

### Fügen Sie Ihren Benutzer der Gruppe vboxusers hinzu (nur Linux-Hosts)

Auf Linux-Hosts muss Ihr Benutzerkonto Mitglied der Gruppe `vboxusers` sein, um auf USB-Geräte zugreifen zu können.

```bash
sudo usermod -aG vboxusers $USER && newgrp vboxusers
```

Nachdem Sie diesen Befehl ausgeführt haben, **melden Sie sich ab und wieder an** (oder starten Sie neu), damit die Gruppenänderung wirksam wird. Sie können dies überprüfen mit:

```bash
groups $USER
```

Die Ausgabe sollte `vboxusers` enthalten.

### Aktivieren Sie den USB-Controller in den VM-Einstellungen

1. Schalten Sie Ihre Kali-VM aus, falls sie läuft.
2. Wählen Sie die VM aus und klicken Sie auf **Einstellungen → USB**.
3. Aktivieren Sie **USB-Controller aktivieren**.
4. Wählen Sie **USB-3.0-Controller (xHCI)** aus den Optionen aus.

{{< alert "circle-info" >}}
USB 3.0 (xHCI) ist für den AWUS036AXML erforderlich. Für den AWUS036ACH reicht technisch gesehen USB 2.0 (EHCI) aus, da der Adapter selbst ein USB 2.0-Gerät ist, aber die Verwendung von xHCI schadet nicht und sorgt für eine konsistente Konfiguration.
{{< /alert >}}

### Einen USB-Gerätefilter hinzufügen

Ein USB-Gerätefilter weist VirtualBox an, den ALFA-Adapter jedes Mal automatisch zu erfassen, wenn er eingesteckt wird, ohne dass in jeder Sitzung ein manueller Eingriff erforderlich ist.

1. Klicken Sie im selben Bereich **Einstellungen → USB** auf das **+**-Symbol (USB-Filter von einem Gerät hinzufügen).
2. Stecken Sie Ihren ALFA-Adapter jetzt ein, falls er noch nicht angeschlossen ist. VirtualBox zeigt ihn im Dropdown-Menü an.
3. Wählen Sie das Gerät aus. Es erscheint normalerweise als **"Realtek 802.11ac NIC"** (AWUS036ACH) oder **"MediaTek Corp. 802.11 b/g/n"** (AWUS036AXML).
4. Klicken Sie auf **OK**, um zu speichern.

Der Filter speichert die Hersteller- (Vendor) und Produkt-ID. Wenn die VM das nächste Mal mit eingestecktem Adapter startet, wird VirtualBox ihn automatisch durchreichen.

### Starten Sie die VM und überprüfen Sie dies mit lsusb

Starten Sie Ihre Kali-VM. Sobald der Desktop geladen ist, öffnen Sie ein Terminal und führen Sie folgenden Befehl aus:

```bash
lsusb
```

Sie sollten eine Zeile sehen, die in etwa so aussieht:

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

oder für den AWUS036AXML:

```
Bus 002 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

Falls das Gerät nicht erscheint, konsultieren Sie die Fehlerbehebungstabelle am Ende dieses Abschnitts.

### Den Treiber laden

**AWUS036ACH (RTL8812AU):**

```bash
sudo modprobe 88XXau
```

Falls dies fehlschlägt (Modul nicht gefunden), installieren Sie zuerst das DKMS-Paket:

```bash
sudo apt update && sudo apt install -y realtek-rtl88xxau-dkms
sudo modprobe 88XXau
```

**AWUS036AXML (MT7921AUN):**

```bash
sudo modprobe mt7921u
```

Der MT7921AUN-Treiber ist seit Version 5.18 im Haupt-Kernel (Mainline) enthalten. Kali 2024.x wird mit einem ausreichend aktuellen Kernel ausgeliefert, aber Sie benötigen möglicherweise noch die Firmware:

```bash
sudo apt install -y firmware-misc-nonfree
```

### Monitor-Modus überprüfen

Wenn der Treiber geladen ist, bestätigen Sie den Namen der Schnittstelle:

```bash
ip link show
```

Suchen Sie nach einer Schnittstelle namens `wlan0`, `wlan1` oder ähnlich. Aktivieren Sie dann den Monitor-Modus:

```bash
sudo airmon-ng start wlan1
```

Eine erfolgreiche Ausgabe endet mit dem Namen der Monitor-Schnittstelle (z. B. `wlan1mon`). Überprüfen Sie dies:

```bash
sudo iwconfig wlan1mon
```

Das Feld **Mode** sollte `Monitor` anzeigen.

### Häufige Fehler in VirtualBox

| Fehler | Ursache | Lösung |
|---|---|---|
| "Keine USB-Geräte verfügbar" in den USB-Einstellungen | Extension Pack nicht installiert oder Versionskonflikt | Passende Version des Extension Packs installieren |
| Adapter wird nicht erfasst / in lsusb nicht sichtbar | Benutzer nicht in der Gruppe `vboxusers` (Linux-Host) | `sudo usermod -aG vboxusers $USER`, dann ab-/anmelden |
| "USB-Gerät wird bereits von einer anderen Instanz verwendet" | Ein anderer Prozess auf dem Host verwendet das Gerät | Adapter aus- und wieder einstecken, bevor die VM gestartet wird |
| Gerät verliert ständig die Verbindung in der VM | USB-3.0-Controller nicht aktiviert; VM nutzt OHCI | In den VM-Einstellungen unter USB auf USB 3.0 (xHCI) umstellen |
| Filter hinzugefügt, aber Gerät wird nicht automatisch erfasst | Filter wurde vor der Installation des Extension Packs erstellt | Filter löschen und nach der Installation des Extension Packs neu hinzufügen |

---

## VMware Workstation / VMware Fusion USB-Passthrough

VMware handhabt USB-Passthrough anders als VirtualBox. Es muss keine separate Erweiterung installiert werden — die Unterstützung für USB 2.0 und 3.0 ist in VMware Workstation 17+ und Fusion 13+ integriert. Der Hauptmechanismus ist der **USB-Arbitrator-Dienst**, der USB-Ereignisse auf dem Host überwacht und Geräte an die VMs weiterleitet.

### Verbinden Sie den Adapter über das Gerätemenü

Wenn Sie Ihren ALFA-Adapter einstecken, während eine VM läuft, zeigt VMware normalerweise ein Popup-Fenster an, in dem gefragt wird, welche VM das Gerät übernehmen soll. Falls Sie das Popup verpassen:

1. Gehen Sie bei laufender Kali-VM in der Menüleiste auf **VM → Wechselmedien**.
2. Erweitern Sie die Liste und suchen Sie Ihren ALFA-Adapter (z. B. **Realtek 802.11ac NIC**).
3. Klicken Sie auf **Verbinden (Vom Host trennen)**.

Das Gerät wird vom Host-Betriebssystem getrennt und steht exklusiv der VM zur Verfügung.

### VMware Fusion (macOS)

Unter macOS mit VMware Fusion:

1. Gehen Sie zu **Virtuelle Maschine → USB & Bluetooth**.
2. Suchen Sie den ALFA-Adapter in der Liste.
3. Schalten Sie die Verbindung auf **Mit Linux verbinden** um (oder den Namen Ihrer Kali-VM).

Alternativ können Sie in den VM-Einstellungen von Fusion unter **USB & Bluetooth** die Option **Neue USB-Geräte automatisch verbinden** aktivieren, damit Fusion Geräte ohne Rückfrage an die aktive VM durchreicht.

### Überprüfen und Treiber laden

Sobald die Verbindung hergestellt ist, überprüfen Sie dies innerhalb von Kali:

```bash
lsusb
```

Laden Sie dann den entsprechenden Treiber wie im Abschnitt VirtualBox oben beschrieben (Schritte 3.6 und 3.7 gelten identisch).

### Überprüfen Sie den VMware USB-Arbitrator-Dienst

Falls der ALFA-Adapter nicht im Menü **Wechselmedien** erscheint, läuft möglicherweise der USB-Arbitrator-Dienst nicht. Auf Linux-Hosts:

```bash
sudo systemctl status vmware-usbarbitrator
```

Falls er gestoppt ist:

```bash
sudo systemctl start vmware-usbarbitrator
sudo systemctl enable vmware-usbarbitrator
```

Öffnen Sie auf Windows-Hosts die **Dienste** (`services.msc`), suchen Sie den **VMware USB Arbitration Service** und stellen Sie ihn auf **Automatisch (Start)**.

### USB 3.0 in VMware aktivieren

Überprüfen Sie für den AWUS036AXML und andere USB 3.0-Geräte, ob Ihre VM-Hardwareversion xHCI unterstützt. Öffnen Sie die Datei `.vmx` Ihrer Kali-VM (im VM-Ordner) und bestätigen oder ergänzen Sie:

```
usb_xhci.present = "TRUE"
```

In der VMware Workstation GUI: **VM → Einstellungen → USB-Controller** und wählen Sie **USB 3.1** aus dem Dropdown-Menü. Die VM muss ausgeschaltet sein, um diese Einstellung zu ändern.

{{< alert "triangle-exclamation" >}}
Die VMware-Hardwareversion 14 oder neuer ist für die USB 3.0 (xHCI)-Unterstützung erforderlich. Falls Ihre VM mit einer älteren Hardwareversion erstellt wurde, aktualisieren Sie diese über **VM → Verwalten → Hardware-Kompatibilität ändern**.
{{< /alert >}}

### Häufige Fehler in VMware

| Fehler | Ursache | Lösung |
|---|---|---|
| Adapter nicht im Menü Wechselmedien | USB-Arbitrator läuft nicht | Dienst `vmware-usbarbitrator` starten |
| Gerät verbindet sich und trennt sich sofort wieder | Host-Treiber übernimmt das Gerät wieder | Host-WLAN-Treiber für den Adapter deaktivieren oder schneller aus- und einstecken |
| "Gerät wird bereits vom Host verwendet" | Host-Betriebssystem hat das Gerät beansprucht | Gerät vom Host auswerfen (z. B. Host-Netzwerkadapter deaktivieren), bevor in der VM verbunden wird |
| Keine USB 3.0-Geschwindigkeit in der VM | VM-Hardwareversion < 14 oder xHCI nicht aktiviert | Hardwareversion aktualisieren, `usb_xhci.present = "TRUE"` zur .vmx hinzufügen |
| Monitor-Modus schlägt trotz Passthrough fehl | Falscher oder fehlender Treiber in Kali | Folgen Sie der [Treiber-Installationsanleitung](/de/blog/install-alfa-driver-kali-ubuntu/) |

---

## Hinweiss zu spezifischen Adaptern

### AWUS036ACH (RTL8812AU)

Der AWUS036ACH ist ein **USB 2.0**-Gerät und einer der am besten getesteten Adapter in VM-Umgebungen. Sowohl VirtualBox als auch VMware handhaben ihn zuverlässig.

- USB-Controller: Sowohl USB 2.0 (EHCI) als auch USB 3.0 (xHCI) funktionieren einwandfrei.
- Treiberpaket: `realtek-rtl88xxau-dkms` (in den Kali-Repos verfügbar). Modulname: `88XXau`.
- Auf einigen neueren Kerneln (6.x) benötigt das DKMS-Paket möglicherweise einen Patch. Besuchen Sie die GitHub-Seite von [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) für den aktuellen Status.
- Monitor-Modus und Paket-Injektion sind im VM-Passthrough sehr stabil.

Sie finden den Adapter in unserem Shop: [ALFA AWUS036ACH](/de/products/alfa/awus036ach/).

### AWUS036AXML (MT7921AUN)

Der AWUS036AXML ist ein **USB 3.0**-Gerät, das WiFi 6E unterstützt. Er ist neuer und weist in VM-Umgebungen einige Besonderheiten auf.

- USB-Controller: **Muss** USB 3.0 (xHCI) verwenden. USB 2.0 Passthrough führt dazu, dass das Gerät mit reduzierter Leistung arbeitet und kann zum Scheitern des Firmware-Ladens führen.
- Treiber: `mt7921u` ist im Haupt-Kernel (5.18+) enthalten. Kali 2024.x beinhaltet ihn. Firmware-Paket: `firmware-misc-nonfree`.
- **Bekanntes Problem**: Bei einigen frühen AWUS036AXML-Einheiten kommt es unter VirtualBox USB 3.0-Arbitrierung zu periodischen Abstürzen. Falls die Schnittstelle in `ip link` verschwindet und wieder auftaucht, versuchen Sie als Diagnoseschritt, den VirtualBox USB-Controller auf USB 2.0 umzustellen. Wenn dies die Verbindung stabilisiert, handelt es sich um ein xHCI-Arbitrierungsproblem von VirtualBox und nicht um ein Treiberproblem.
- VMware Workstation handhabt den AWUS036AXML beim USB 3.0-Passthrough meist zuverlässiger als VirtualBox.

Vollständiger Testbericht: [AWUS036AXML WiFi 6E Testbericht](/de/blog/awus036axml-wifi-6e-review/).

### AWUS036ACM (MT7612U, Doppelantenne)

Der AWUS036ACM verwendet den MediaTek MT7612U-Chipsatz mit einem im Kernel integrierten Treiber (`mt76x2u`, integriert seit Kernel 4.19). Es ist keine Treiberinstallation erforderlich — sobald das Passthrough konfiguriert ist, ist der Adapter in der VM Plug-and-Play-fähig. Falls das Modul nicht automatisch geladen wird, führen Sie `sudo modprobe mt76x2u` aus. Der AWUS036ACM verfügt über zwei RP-SMA-Antennenanschlüsse.

---

## Tipps zur Leistungssteigerung

Den Adapter in die VM zu bekommen, ist nur der erste Schritt. Eine stabile Leistung während tatsächlicher Pentesting-Sitzungen erfordert einige zusätzliche Optimierungsschritte.

**Verwenden Sie den richtigen USB-Filtertyp.** Verwenden Sie für den AWUS036AXML in VirtualBox immer einen USB 3.0-Filter (stellen Sie sicher, dass der xHCI-Controller ausgewählt ist). Ein USB 2.0-Filter an einem USB 3.0-Gerät führt dazu, dass das Gerät nur mit USB 2.0-Geschwindigkeit arbeitet, was den Durchsatz halbiert.

**Deaktivieren Sie das USB-Autosuspend auf dem Host.** Linux-Hosts können das USB-Gerät aggressiv in den Ruhezustand versetzen, wodurch die VM den Zugriff verliert. Deaktivieren Sie dies auf der Host-Ebene:

```bash
echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend
```

Um dies über Neustarts hinweg dauerhaft zu machen, fügen Sie es zu `/etc/rc.local` hinzu oder erstellen Sie eine udev-Regel.

**Weisen Sie der VM ausreichend Ressourcen zu.** Paket-Injektion und Erfassungslasten sind CPU-intensiv. Weisen Sie mindestens Folgendes zu:
- **2 CPU-Kerne** (4 empfohlen für parallele Tools wie `hcxdumptool` + `hashcat`)
- **2 GB RAM** (4 GB, wenn ein vollständiger Kali-Desktop mit GUI-Tools ausgeführt wird)

**Erstellen Sie einen VM-Snapshot vor Einsätzen.** Erstellen Sie vor jedem Pentest einen Snapshot Ihrer Kali-VM. Falls ein Treiberabsturz oder ein fehlerhaftes Firmware-Update Ihr Setup beschädigt, bringt Sie das Zurückspielen des Snapshots in Sekunden in einen funktionierenden Zustand zurück.

**Halten Sie den Adapter kühl.** ALFA-Adapter mit Hochleistungsantennen erzeugen bei dauerhafter Injektion Hitze. In einer VM kann das Host-Betriebssystem das USB-Gerät drosseln, wenn es thermische Probleme oder Stromversorgungsprobleme erkennt. Verwenden Sie den Adapter in einer gut belüfteten Umgebung.

{{< alert "circle-info" >}}
Erwägen Sie bei Erfassungssitzungen, die länger als 30 Minuten dauern, die Verwendung eines aktiven USB-Hubs mit eigener Stromversorgung zwischen dem Adapter und Ihrem Host. Dies sorgt für eine stabile Stromversorgung und verhindert Spannungsabfälle, die zum Verbindungsabbruch führen könnten.
{{< /alert >}}

---

## Bare Metal vs. VM: Ein ehrlicher Vergleich

Virtuelle Maschinen führen eine zusätzliche Komplexitätsebene zwischen Ihrem Adapter und dem Kernel ein. Hier ist eine ehrliche Einschätzung für Sicherheitsexperten:

| Merkmal | Bare-Metal Kali | VirtualBox + Kali | VMware + Kali |
|---|---|---|---|
| **Treiber-Unterstützung** | Vollständig, direkt | Gut (mit Extension Pack) | Gut (integriertes USB) |
| **Monitor-Modus Stabilität** | Exzellent | Gut | Gut–Exzellent |
| **Paket-Injektion Zuverlässigkeit** | Exzellent | Gut (gelegentlicher Frame-Verlust) | Gut–Exzellent |
| **USB 3.0 Durchsatz** | Volle Geschwindigkeit | Nahezu voll | Nahezu voll |
| **Setup-Aufwand** | Hoch (dedizierte Hardware) | Gering–Mittel | Gering–Mittel |
| **Portabilität** | Gering (dedizierter Rechner) | Hoch (Snapshots, Portabilität) | Hoch |
| **Ressourcen-Overhead** | Keiner | Mittel | Gering–Mittel |
| **CTF / Labor-Einsatz** | Übertrieben | Ideal | Ideal |
| **Professionelle Einsätze** | Empfohlen | Akzeptabel | Akzeptabel |

**Fazit:** Für CTF-Wettbewerbe, Laborübungen und Lernumgebungen ist eine VM mit korrektem USB-Passthrough bequem und leistungsfähig genug. Für professionelle Penetrationstests, bei denen es auf Zuverlässigkeit und forensische Integrität ankommt, ist ein dedizierter Kali-Laptop oder eine Bare-Metal-Installation die zuverlässigere Wahl. Die Frame-Verluste und gelegentlichen USB-Arbitrierungsprobleme in VMs können die Zuverlässigkeit zeitkritischer Angriffe wie PMKID-Erfassung oder Deauthentication-Flooding beeinträchtigen.

---

## Kurzreferenz zur Fehlerbehebung

| Symptom | Wahrscheinlichste Ursache | Lösung |
|---|---|---|
| `lsusb` zeigt in Kali nichts an | USB-Passthrough nicht konfiguriert | USB-Filter hinzufügen (VBox) oder über Wechselmedien verbinden (VMware) |
| "Keine USB-Geräte" in VirtualBox | Extension Pack fehlt oder Versionskonflikt | Passendes Extension Pack installieren |
| Adapter in `lsusb` sichtbar, aber kein `wlan`-Interface | Treiber nicht geladen | `sudo modprobe 88XXau` oder `sudo modprobe mt7921u` |
| `modprobe: FATAL: Module 88XXau not found` | DKMS-Paket nicht installiert | `sudo apt install realtek-rtl88xxau-dkms` |
| Interface erscheint und verschwindet wieder | USB-Autosuspend oder VBox xHCI-Arbitrierung | Autosuspend deaktivieren; USB 2.0-Controller für ACH versuchen |
| `airmon-ng` startet, aber Monitor-Modus schlägt fehl | Falscher Treiber oder Konflikt mit Netzwerk-Manager | `sudo airmon-ng check kill`, dann erneut versuchen |
| VirtualBox USB-Filter erfasst nicht beim Booten | Filter vor dem Extension Pack hinzugefügt | Filter löschen, Extension Pack installieren, Filter neu hinzufügen |
| VMware verliert Gerät bei langen Sitzungen | VMware USB-Arbitrator-Dienst stoppt | Dienst wieder aktivieren und auf Autostart setzen |

---

## Nächste Schritte

Nachdem USB-Passthrough konfiguriert und der Monitor-Modus verifiziert wurde, können Sie fortfahren:

- **Treiber installieren oder aktualisieren:** [ALFA-Treiber-Installationsanleitung für Kali & Ubuntu](/de/blog/install-alfa-driver-kali-ubuntu/)
- **Vollständiges AWUS036ACH Setup:** [AWUS036ACH Kali Linux Setup-Anleitung](/de/blog/awus036ach-kali-linux-setup/)
- **Hardware-Testbericht zum AWUS036AXML:** [AWUS036AXML WiFi 6E Testbericht](/de/blog/awus036axml-wifi-6e-review/)

Falls Sie noch überlegen, welchen Adapter Sie für VM-basiertes Pentesting kaufen sollen: Der AWUS036ACH bleibt aufgrund seines ausgereiften USB 2.0-Passthrough-Verhaltens und des kampferprobten Treibers die zuverlässigste Wahl. Der AWUS036AXML bietet die bessere Leistung, sobald alles konfiguriert ist, erfordert aber eine sorgfältigere USB 3.0-Konfiguration.
