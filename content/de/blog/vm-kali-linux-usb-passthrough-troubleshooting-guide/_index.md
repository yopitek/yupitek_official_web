---
title: "Kali-Linux-VM erkennt USB-Adapter nicht? USB-Passthrough-Diagnose für VirtualBox/VMware"
description: "Standardisiertes Diagnosehandbuch für USB-Passthrough: VirtualBox Extension Pack, USB-3.0-Controller (xHCI), vboxusers-Gruppe, VMware-USB-Arbitrierung, Diagnoseablauf lsusb→iwconfig→dmesg und FAQ."
date: 2026-08-31
author: benny-lai
lastmod: 2026-08-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "wireless-adapter", "virtual-machine"]
featureimage: /images/blog/vm-kali-linux-usb-passthrough-troubleshooting-guide.webp
faq:
  - question: "Ich habe den Adapter an einen anderen USB-Port gesteckt und jetzt zeigt lsusb nichts mehr. Ist der Adapter kaputt?"
    answer: "Nicht unbedingt. Prüfe zuerst, ob du ihn an einen Port «nur zum Laden» gesteckt hast oder ob der Host das Gerät zum Energiesparen in den Ruhezustand versetzt hat. Stecke ihn wieder an einen normalen USB-Port an der Rückseite des Mainboards oder ziehe ihn einmal ab und wieder an — meist ist er danach wieder da."
  - question: "Das USB-Symbol in der unteren rechten Ecke des VM-Fensters ist leer. Was soll ich tun?"
    answer: "Prüfe der Reihe nach: ① ob die Extension-Pack-Version exakt mit VirtualBox übereinstimmt; ② ob dein Benutzer auf Linux-Hosts in der vboxusers-Gruppe ist (neuer Login nötig); ③ ob der Host den Adapter mit lsusb noch sieht; ④ ob keine andere Software (z. B. ein Treibertool des Hosts) das Gerät belegt."
  - question: "Nach dem Einrichten eines USB-Filters kann der Host den Adapter nicht mehr nutzen. Ist das normal?"
    answer: "Ja, das ist erwartet. Sobald das Gerät an den Guest durchgereicht wurde, gehört die Kontrolle dem Guest und der Host kann es nicht gleichzeitig nutzen. Wenn du den Adapter wieder am Host brauchst, gib ihn über das USB-Symbol im VM-Fenster zurück (release)."
  - question: "lsusb im Guest zeigt den Adapter, aber es gibt keine wlan-Schnittstelle. Welchen Treiber soll ich installieren?"
    answer: "Das hängt vom Chipsatz ab: Der AWUS036AXML (MediaTek MT7921AU) nutzt den im Kernel enthaltenen mt7921u-Treiber — Plug-and-Play ab Kernel 5.18+; stelle zuerst sicher, dass apt install linux-firmware aktuell ist. Der AWUS036ACH (Realtek RTL8812AU) nutzt einen Out-of-Tree-Treiber — installiere den von der Community gepflegten aircrack-ng/rtl8812au und kompiliere ihn mit DKMS (und kümmere dich um die MOK-Signierung für Secure Boot; deaktiviere Secure Boot nicht)."
  - question: "Warum bootet der Guest nach der Auswahl des USB-3.0-Controllers nicht mehr?"
    answer: "Einige ältere Guest-Kernel unterstützen xHCI nur schlecht. Wenn dein Kali eine ältere Version ist, versuche: Herunterfahren → zurück auf USB 2.0 (EHCI) Controller → Booten → Kernel aktualisieren → zurück auf USB 3.0. Halte Kali so aktuell wie möglich — dann ist die xHCI-Unterstützung am vollständigsten."
  - question: "Der Adapter ist auf einem echten Rechner schnell, in der VM aber langsam. Ist das normal?"
    answer: "Ja. In einer VM arbeitet der Adapter ungefähr mit der Geschwindigkeit der Weiterleitung durch die USB-Emulationsschicht, was im Vergleich zur direkten Verbindung an einem echten Rechner etwas Overhead bedeutet. Ein korrekter USB-3.0-Controller (xHCI) und ein aktueller Hypervisor halten diesen Overhead minimal. Bei starkem Leistungsabfall prüfe zuerst, ob der Controller nicht auf USB 1.1 hängen geblieben ist."
---

> **Unterstützte Plattformen**: Windows / Linux / macOS-Hosts mit Oracle VirtualBox / VMware Workstation (Guest = Kali Linux / Debian / Ubuntu)
> **Beispielhardware**: ALFA AWUS036ACH (Realtek RTL8812AU) / ALFA AWUS036AXML (MediaTek MT7921AU)
> **Zweck dieses Artikels**: standardisiertes Diagnosehandbuch für «USB-Passthrough». Die Einschränkungen des USB-Passthrough auf macOS-Hosts werden in Kapitel 5 erklärt.

---

{{< tldr >}}

Viele Kali-Nutzer stecken den Adapter in den Host und sehen in der VM trotzdem keine WLAN-Schnittstelle. **In den meisten Fällen liegt es an einem von drei sehr häufigen Gründen** — die Wahrscheinlichkeit, dass der Adapter selbst defekt ist, ist gering:

1. **Das Extension Pack von VirtualBox ist nicht installiert**: ohne es kann der Guest die USB-2.0/3.0-Controller gar nicht nutzen (das Tempolimit von USB 1.1 liegt bei nur 12 Mbps, für einen Adapter völlig unzureichend).
2. **Der USB-Passthrough ist nicht eingerichtet**: Der Host beansprucht standardmäßig alle USB-Geräte. Der Guest braucht entweder ein manuelles Mounten oder einen «USB-Filter (VM USB Filter)», der den Adapter automatisch übernimmt.
3. **Der Treiber im Guest ist nicht geladen**: Die USB-Ebene ist durchgereicht (`lsusb` sieht das Gerät), aber Linux hat keinen passenden Treiber, daher zeigt `ip link` keine `wlan`-Schnittstelle.

Diagnosereihenfolge: zuerst die Hardware des Hosts, dann der Passthrough im Guest, zuletzt die Treiberebene — die vollständige Diagnose-Merkregel steht in 1.3.

{{< /tldr >}}

---

## 1. Warum nutzt die VM den WLAN-Adapter des Hosts standardmäßig nicht?

### 1.1 Dein USB-Adapter gehört «gleichzeitig» nur einem Betriebssystem

USB arbeitet nach einer **Single-Host-Architektur**: Ein USB-Gerät kann zu einem Zeitpunkt nur von einem «Host-Controller» gesteuert werden. Wenn der Adapter am Host steckt, wird das Gerät zuerst vom **Host-Betriebssystem (Host OS)** enumeriert (enumerate) und übernommen. Der Treiber des Hosts erkennt und steuert es.

Die virtuelle Maschine (Guest VM) ist kein physisches Gerät am USB-Bus; sie ist nur «virtuelle Hardware», die der Hypervisor im Host darstellt. Damit der Guest den USB-Adapter nutzen kann, **muss der Host das Gerät aktiv an den Guest «übergeben»** — dieser Mechanismus heißt **USB-Passthrough (USB Redirection)**.

### 1.2 Was geht beim USB-Passthrough wirklich durch?

Am Beispiel VirtualBox sieht der Passthrough-Ablauf so aus:

```
Physischer USB-Adapter (AWUS036ACH / AWUS036AXML)
       │  steckt in einem physischen USB-Port des Hosts
       ▼
USB-Host-Controller des Host-Betriebssystems (Host OS)
       │  Hypervisor (VirtualBox) fängt ab und leitet um
       ▼
Virtueller USB-Host-Controller (emulierte EHCI / xHCI)
       │  für den Guest (Kali) sieht es aus «als wäre er selbst angeschlossen»
       ▼
USB-Treiber von Kali → WLAN-Treiber → wlan-Schnittstelle
```

Nach erfolgreichem Passthrough **geht die Kontrolle über das Gerät auf der Host-Seite an den Guest über**; der Host verhält sich, als wäre das Gerät «abgezogen», und kann es nicht mehr nutzen. Im Guest erscheint es stattdessen als brandneues USB-Gerät. **Das ist normales Verhalten, kein Bug.** Ein USB-Gerät des Hosts kann nicht gleichzeitig beiden Seiten dienen.

### 1.3 «Wird nicht erkannt» hat eigentlich drei Ebenen

| Ebene | Prüfwerkzeug | Symptom | Bedeutung |
|-------|-------------|---------|-----------|
| **USB-Passthrough-Ebene** | `lsusb` im Guest | `lsusb` zeigt die VID:PID des Adapters gar nicht | Passthrough fehlgeschlagen (Problem mit Extension Pack / Controller / Filter) |
| **Treiberebene** | `dmesg` im Guest | `lsusb` sieht das Gerät, aber `dmesg` meldet Fehler (z. B. fehlende Firmware, `Required key not available`) | Im Guest fehlt ein Treiber oder das Modul lädt nicht |
| **WLAN-Schnittstellenebene** | `iwconfig` / `ip link` im Guest | `lsusb` und `dmesg` sind in Ordnung, aber keine `wlan`-Schnittstelle | Treiber geladen, aber Schnittstelle nicht registriert, oder Modus-/Konfigurationsproblem |

> **Merkregel**: Schau zuerst in `lsusb`, ob «das Gerät in den Guest durchgereicht wurde», dann in `ip link`, ob «der Treiber es erkennt». **Verdächtige nicht gleich den Adapter.**

---

## 2. VirtualBox: erst das Extension Pack installieren, dann den USB-3.0-Controller einstellen

### 2.1 Das Erweiterungspaket (Extension Pack) ist Pflicht

Das Basis-Paket von VirtualBox **enthält nur die Emulation des USB-1.1-Controllers (OHCI)**, und die Übertragungsrate von USB 1.1 reicht für einen Adapter nicht aus. **Die USB-2.0- (EHCI) und USB-3.0-Controller (xHCI) gibt es nur mit dem offiziellen «Erweiterungspaket (Extension Pack)» von Oracle.**

Die Symptome ohne Extension Pack sind typisch: In den Guest-Einstellungen lässt sich kein USB-2.0-/USB-3.0-Controller wählen, oder beim Mounten des Adapters erscheint «Geräteverbindung zur virtuellen Maschine fehlgeschlagen (error code E_FAIL / VERR_PDM_NO_USB_PORTS)».

### 2.2 Die Version muss «exakt» übereinstimmen

Die Version des Extension Packs **muss exakt mit der Version des VirtualBox-Hauptprogramms übereinstimmen** (z. B. benötigt VirtualBox 7.0.20 das Extension Pack 7.0.20). Schon eine abweichende Nebenversion kann Installation oder Laden scheitern lassen.

```bash
# Aktuelle VirtualBox-Version anzeigen
vboxmanage --version
```

Lade das passende `Oracle_VM_VirtualBox_Extension_Pack-<Version>.vbox-extpack` von der offiziellen Oracle-Downloadseite (https://www.virtualbox.org/wiki/Downloads) herunter und dann:

```bash
# Variante 1: GUI-Installation (VirtualBox-Hauptprogramm → Datei → Tools → Extension Pack Manager → Installieren)
# Variante 2: Installation per Befehl
sudo VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-*.vbox-extpack

# Installation bestätigen
VBoxManage list extpacks
```

> Bei der Installation wird die Oracle-Lizenz angezeigt (Personal Use and Evaluation License); die private Nutzung ist kostenlos, in kommerziellen Umgebungen richte dich nach dem Lizenzinhalt.

### 2.3 Linux-Host: dich selbst in die vboxusers-Gruppe aufnehmen

Auf einem Linux-Host muss **dein Benutzer zur Gruppe `vboxusers` gehören**, damit VirtualBox auf USB-Geräte zugreifen kann. Viele installieren das Erweiterungspaket und scheitern trotzdem — der Haken sind die Rechte.

```bash
# Der Gruppe beitreten (<user> durch deinen Benutzernamen ersetzen)
sudo usermod -aG vboxusers $USER

# Ab- und wieder anmelden (oder neu starten), damit die Gruppe wirkt; bestätigen
id $USER
```

### 2.4 Den USB-3.0-Controller (xHCI) einstellen

1. Wähle deine Kali-VM → **Einstellungen (Settings) → Ports → USB**.
2. Hake «Enable USB Controller» an und wähle **USB 3.0 (xHCI) Controller**.
   - Der AWUS036AXML hat die Spezifikation USB 3.2 Gen 1 (USB-C): **wähle unbedingt USB 3.0 (xHCI)**; USB 2.0 würde die Übertragungsrate begrenzen.
   - Der AWUS036ACH hat eine USB-Type-A-Schnittstelle und funktioniert mit USB-2.0- und USB-3.0-Controllern; für die bessere Übertragungsrate wähle ebenfalls USB 3.0 (xHCI).
3. Nach der Controller-Änderung **aus- und wieder einschalten** (kein Reboot im Guest), damit die Änderung greift.

### 2.5 Manuelles Mounten und der VMware-Vergleich

Nach dem Start der Kali-VM achte auf das **USB-Symbol in der unteren rechten Ecke des Fensters** (ein USB-Stecker):

1. Klicke auf das USB-Symbol → es listet die aktuell am Host angeschlossenen USB-Geräte auf.
2. Dein Adapter sollte etwa als `Realtek 802.11ac NIC` (ACH) oder `ALFA AWUS036AXML` / MediaTek (AXML) erscheinen.
3. Klicke einmal darauf, das Gerät wird an Kali «übergeben».

Ist die Liste leer, liegt ein Problem in der Passthrough-Ebene vor — prüfe 2.2 / 2.3 / 2.4 (inklusive nicht aktiviertem USB-Controller) oder führe direkt das Diagnosearbeitsblatt aus Kapitel 6 aus.

**VMware-Vergleich**: VMware Workstation / Fusion **braucht kein** zusätzliches Erweiterungspaket für den USB-Passthrough, aber es gibt zwei häufige Prüfpunkte:

1. **Host-Dienst**: Prüfe auf Linux-Hosts, ob `vmware-usbarbitrator` (der USB-Arbitrierungsdienst) läuft:
   ```bash
   sudo systemctl status vmware-usbarbitrator
   # Falls er nicht läuft: starten und für den Autostart aktivieren
   sudo systemctl enable --now vmware-usbarbitrator
   ```
2. **VM-Einstellungen**: VM-Einstellungen → USB Controller → **USB 3.1 (oder USB 3.0)** anhaken.
3. **Manuelle Verbindung**: Menü des VMware-Fensters → **Wechselmedien (Removable Devices) → dein Adapter → Verbinden (Connect)**.

> **Vergleichskern**: VirtualBox hängt bei «kein Extension Pack installiert»; VMware hängt bei «Arbitrierungsdienst läuft nicht» oder «USB-3.0-Controller aus». Prüfe zuerst, welches Produkt du nutzt, und dann den passenden Punkt.

---

## 3. Drei Diagnoseschritte: lsusb → iwconfig → dmesg

Nach der Passthrough-Einrichtung grenzen drei Befehle das Problem auf «Passthrough-Ebene» oder «Treiberebene» ein.

### Schritt 0: zuerst die Hardware am Host bestätigen (gib nicht dem Adapter die Schuld)

Öffne ein Terminal im **Host-Betriebssystem** und führe aus:

```bash
lsusb
```

Erwartete Ausgabe (je nach Modell):

```
# AWUS036ACH (Realtek RTL8812AU)
Bus ... ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
# oder AWUS036AXML (MediaTek MT7921AU)
Bus ... ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

- Der Host sieht ihn → Hardware und Kabel sind in Ordnung; das Problem liegt beim Passthrough oder Guest-Treiber.
- Auch der Host sieht ihn nicht → **zuerst den Host prüfen** (anderen USB-Port, anderes Kabel, Kreuztest an einem anderen Rechner), dann ein Support-Ticket erwägen.

### Schritt 1: lsusb im Guest — ist der Passthrough gelungen?

Führe **in der Kali-VM** aus:

```bash
lsusb
```

- Gleiche VID:PID sichtbar → **Passthrough erfolgreich**, weiter zu Schritt 2.
- Nicht sichtbar → **Passthrough fehlgeschlagen**: zurück zu Kapitel 2 (Extension Pack / Controller / vboxusers-Gruppe) oder prüfen, ob andere Host-Software den Adapter belegt.

### Schritt 2: iwconfig / ip link — ist die WLAN-Schnittstelle da?

```bash
iwconfig
# oder (neuere Versionen)
iw dev
ip link
```

- Eine `wlan0`- / `wlx...`-Schnittstelle erscheint → **alles durchgängig**, du kannst loslegen.
- Keine WLAN-Schnittstelle, aber `lsusb` sieht das Gerät → das Problem liegt in der **Treiberebene des Guests**; weiter zu Schritt 3.

### Schritt 3: dmesg — warum scheitert die Treiberebene?

```bash
# Die letzten Kernel-Meldungen ansehen
sudo dmesg | tail -30
# USB- und WLAN-bezogene Meldungen filtern
sudo dmesg | grep -iE "usb|wlan|8812|mt7921|rtl" | tail -30
```

Häufige `dmesg`-Ergebnisse im Vergleich:

| `dmesg`-Meldung | Ursache | Lösung |
|-----------------|---------|--------|
| `usb 3-1: new high-speed USB device ...` ohne Fortsetzung | Gerät enumeriert, aber kein Treiber verfügbar | Passenden Treiber im Guest installieren (siehe FAQ Q4) |
| `Direct firmware load failed` / `firmware_loading` | Firmware-Datei fehlt | `apt install firmware-realtek`, dann Modul neu laden |
| `Required key not available` | Secure Boot aktiv, Modul nicht signiert | Mit MOK-Schlüssel signieren (Secure Boot nicht deaktivieren) |
| `disagrees about version of symbol` | Treiberversion passt nicht zum Kernel | Mit DKMS neu kompilieren und installieren |

> **Kernverständnis**: `lsusb` sieht das Gerät — das beweist nur «der USB-Passthrough hat funktioniert», **bedeutet aber nicht, dass der Treiber geladen ist**. Der häufige Fall «Passthrough ok, aber kein wlan» ist genau das: im Guest fehlt der passende Treiber.

---

## 4. USB-VM-Filter: automatisches Mounten beim Einstecken + Verbindungsprobleme

### 4.1 Warum einen USB-Filter (USB Filter) einrichten?

Das Problem beim manuellen Mounten (Kapitel 2, 2.5): **bei jedem Neustart der Kali-VM musst du erneut klicken**. Mit eingerichtetem «USB-Filter» überträgt VirtualBox **passende Geräte automatisch in den Guest**, sobald der Adapter eingesteckt wird (oder die VM bootet).

Einrichtung (VirtualBox):

1. VM-Einstellungen → USB → rechts auf **«+» Filter hinzufügen → deinen Adapter auswählen**.
2. VirtualBox füllt automatisch eine Filterregel aus (Felder Vendor ID / Product ID / Seriennummer):
   - **Name**: z. B. `ALFA AWUS036AXML` oder `AWUS036ACH`
   - **Vendor ID**: für AWUS036ACH `0bda`, für AWUS036AXML `0e8d`
   - **Product ID**: für AWUS036ACH `8812`, für AWUS036AXML `7961`
3. Bei mehreren Adaptern desselben Modells auch das Feld «Seriennummer (Serial Number)» ausfüllen, damit nicht der andere gefiltert wird.

> Tipp: Rechtsklick auf den Filter → **Filter bearbeiten** — du kannst nur Vendor ID und Product ID behalten (lockere Übereinstimmung) oder die Seriennummer ergänzen (exakte Übereinstimmung).

### 4.2 Häufige Verbindungsabbrüche: meist Strom- oder Controllerproblem

Hochleistungsadapter (der AWUS036ACH zieht beim Monitor-/Injection-Betrieb höheren Momentanstrom; der AWUS036AXML hat USB-3-Spezifikation) können in der VM gelegentlich «während der Nutzung abfallen / sich trennen». Typische Ursachen und Gegenmaßnahmen:

| Erscheinung | Ursache | Gegenmaßnahme |
|-------------|---------|---------------|
| Nach dem Passthrough zu wenig Strom, ständige Abfälle | Die emulierte Stromversorgung des virtuellen USB-Controllers ist konservativ, oder der Host-Port liefert zu wenig | Am Host einen **USB-Port an der Mainboard-Rückseite** oder einen USB-Hub mit eigener Stromversorgung nutzen |
| Adapter mal da, mal weg | Der **USB-Energiesparmodus (autosuspend)** des Hosts hat das Gerät schlafen gelegt | In den Host-Einstellungen den USB-Autosuspend «für dieses Gerät» deaktivieren (die systemweiten Sicherheitsfunktionen nicht abschalten) |
| Mounten schlägt sofort fehl, lange error code-Kette | Falscher Controller gewählt (USB 1.1/2.0 trägt kein USB-3-Gerät) | Auf «USB 3.0 (xHCI) Controller» umstellen und nach dem Herunterfahren neu starten |
| Adapter nach dem Aufwachen des Hosts aus dem Standby (sleep) tot | Beim Host-Schlaf ist die USB-Umleitung des Hypervisors abgerissen | Host-Standby während der Nutzung vermeiden; oder nach dem Aufwachen einmal neu mounten |

### 4.3 Sicherheitshinweis

Um Abfälle zu reduzieren, kannst du den Autosuspend **eines einzelnen USB-Geräts** deaktivieren, aber nur auf der Ebene «dieses Geräts». **Deaktiviere nicht** die systemweiten Sicherheitsfunktionen (Firewall, Secure Boot), um dir Arbeit zu sparen — der Preis wäre unverhältnismäßig.

---

## 5. Einschränkungen des macOS-Hosts und Plattform-Grenzen

### 5.1 USB-Passthrough auf macOS-Hosts hat angeborene Grenzen

Eine VM von einem macOS-Host aus mit USB-Passthrough zu betreiben, ist **die Kombination, die am ehesten hakt**. Prüfe zuerst deine Situation:

| macOS-Host | VirtualBox | VMware Fusion |
|------------|-----------|---------------|
| **Apple Silicon (M1/M2/M3/M4)** | ⚠️ **USB-Passthrough-Unterstützung eingeschränkt / unvollständig** — eine der offiziell bekannten Einschränkungen; selbst mit funktionierendem Adaptertreiber kann die Passthrough-Ebene direkt unbrauchbar sein | ⚠️ Vollständigere Unterstützung, aber trotzdem zuerst «direkt am Host einstecken» und prüfen, ob der Adapter unter macOS funktioniert |
| **Intel (Intel Mac)** | ✅ Nutzbar, aber zuerst den **Kernel-Extension-Freigabeprozess** durchlaufen (Systemeinstellungen → Sicherheit und Datenschutz → Oracle-bezogene Kernel-Erweiterungen erlauben) und ein exakt versionsgleiches Extension Pack installieren | ✅ Nutzbar |

**Empfehlung**: Ist dein Host ein macOS, mach «direkt am Host einstecken → `system_profiler SPUSBDataType` → Adapter am Host funktioniert bestätigen» zum ersten Tor jeder Diagnose. **Nimm Modelle, die unter macOS nicht unterstützt werden, nicht in die VM-Diagnoseliste auf** — das kostet viel Zeit.

### 5.2 Plattform-Grenzen (Support Boundary)

| Plattform | Support-Status | Erläuterung |
|-----------|----------------|-------------|
| Windows-Host + VirtualBox / VMware + Kali-Guest | ✅ Unterstützt | Alle Abläufe dieses Kapitels gelten |
| Linux-Host + VirtualBox / VMware + Kali-Guest | ✅ Unterstützt | vboxusers-Gruppe (VB) und vmware-usbarbitrator-Dienst (VMware) nicht vergessen |
| **macOS (Apple Silicon)** + VirtualBox | ⚠️ **USB-Passthrough eingeschränkt** | Wechsel zu VMware Fusion oder Nutzung eines Linux／Windows-Hosts empfohlen |
| macOS (Intel) + VirtualBox | ✅ Unterstützt | Kernel-Extension-Freigabe + versionsgleiches Extension Pack nötig |
| **Guest ist macOS** | ❌ Nicht empfohlen | Dieser Artikel setzt Linux-Guests wie Kali / Debian / Ubuntu voraus |

> **Support-Grenze**: Bestätige bei der Diagnose immer zuerst «funktioniert der Adapter am Host», bevor du über VM-Einstellungen sprichst. Wenn der Host den Adapter selbst nicht erkennt, rettet keine VM-Einstellung etwas — der nächste Schritt ist dann ein Treiberproblem des Hosts (siehe andere Treiber-Diagnoseartikel auf dieser Website).

---

## 6. Standard-Diagnosearbeitsblatt: vor der Meldung einmal durchlaufen (Support-Intake)

> Bei «VM erkennt Adapter nicht» die folgende Tabelle der Reihe nach abarbeiten und die Ergebnisse notieren. **Das Arbeitsblatt komplett durchlaufen, bevor du entscheidest, ein Support-Ticket zu eröffnen** — oft löst es sich von selbst, und es verkürzt den Support-Hin und Her erheblich.

### Schritt 1: Hardware-Check des Hosts

| Prüfpunkt | Befehl | Notizfeld |
|-----------|--------|-----------|
| Host-Betriebssystem und Architektur | `uname -a` / `systeminfo` | \_\_\_\_\_ |
| Sieht der Host den Adapter? | `lsusb` am Host | VID:PID \_\_\_\_\_ |
| USB-Port und Kabel | Port und Kabel wechseln, erneut testen | Ergebnis \_\_\_\_\_ |

### Schritt 2: Check der Virtualisierungs-Ebene (Hypervisor)

| Prüfpunkt | Aktion | Notizfeld |
|-----------|--------|-----------|
| Virtualisierungssoftware und Version | VirtualBox: `vboxmanage --version` ／ VMware: Help → About | \_\_\_\_\_ |
| Extension-Pack-Version passend? | VirtualBox: `VBoxManage list extpacks` | Version \_\_\_\_\_ |
| Host-Rechte / Dienst | Linux-Host: `id` auf vboxusers prüfen; VMware: `systemctl status vmware-usbarbitrator` | \_\_\_\_\_ |
| USB-Controller-Einstellung | VirtualBox: USB 3.0 (xHCI) Controller angehakt? | Ja / Nein |

### Schritt 3: Check des Passthrough-Ergebnisses

| Prüfpunkt | Befehl | Notizfeld |
|-----------|--------|-----------|
| Sieht der Guest den Adapter? | `lsusb` im Guest | \_\_\_\_\_ |
| WLAN-Schnittstelle da? | `iwconfig` / `ip link` im Guest | \_\_\_\_\_ |
| Treiberebenen-Meldungen | `sudo dmesg \| tail -30` im Guest | \_\_\_\_\_ |
| Verwendeter Guest-Kernel | `uname -r` | \_\_\_\_\_ |

### Schritt 4: Bewertung und Notiz

- `lsusb` (Guest) sieht nichts → **Passthrough-Ebene**-Problem → Kapitel 2 und Schritt 2 wiederholen.
- `lsusb` sieht das Gerät, `ip link` kein wlan → **Treiberebene**-Problem → Schritt 3 aus Kapitel 3 wiederholen.
- Alles normal, aber instabil → **Strom / Energiesparen / Controller**-Problem → Kapitel 4.

### Support-Intake-Informationspaket

Bevor du den Support anrufst／das Ticket abschickst, füge folgende Informationen auf einmal bei, damit der Support direkt zur Sache kommt:

> **Host-OS + Architektur, Virtualisierungssoftware und Version, ob ein Extension Pack installiert ist und welche Version, `lsusb`-Ausgabe des Hosts, `lsusb`-Ausgabe des Guests, `ip link`- / `iwconfig`-Ausgabe des Guests, relevante `dmesg`-Meldungen, Adaptermodell und Verbindungsart (USB-C / USB-A, direkt oder über Hub)**

---

## 7. Häufige Fragen (FAQ)

**F1: Ich habe den Adapter an einen anderen USB-Port gesteckt und jetzt zeigt `lsusb` nichts mehr. Ist der Adapter kaputt?**
Nicht unbedingt. Prüfe zuerst, ob du ihn an einen Port «nur zum Laden» gesteckt hast oder ob der Host das Gerät zum Energiesparen in den Ruhezustand versetzt hat. Stecke ihn wieder an einen normalen USB-Port an der Rückseite des Mainboards oder ziehe ihn einmal ab und wieder an — meist ist er danach wieder da.

**F2: Das USB-Symbol in der unteren rechten Ecke des VM-Fensters ist leer. Was soll ich tun?**
Prüfe der Reihe nach: ① ob die Extension-Pack-Version exakt mit VirtualBox übereinstimmt; ② ob dein Benutzer auf Linux-Hosts in der `vboxusers`-Gruppe ist (neuer Login nötig); ③ ob der Host den Adapter mit `lsusb` noch sieht; ④ ob keine andere Software (z. B. ein Treibertool des Hosts) das Gerät belegt.

**F3: Nach dem Einrichten eines USB-Filters kann der Host den Adapter nicht mehr nutzen. Ist das normal?**
Ja, das ist erwartet. Sobald das Gerät an den Guest durchgereicht wurde, gehört die Kontrolle dem Guest und der Host kann es nicht gleichzeitig nutzen. Wenn du den Adapter wieder am Host brauchst, gib ihn über das USB-Symbol im VM-Fenster zurück (release).

**F4: `lsusb` im Guest zeigt den Adapter, aber es gibt keine wlan-Schnittstelle. Welchen Treiber soll ich installieren?**
Das hängt vom Chipsatz ab:
- **AWUS036AXML (MediaTek MT7921AU)**: nutzt den im Kernel enthaltenen `mt7921u`-Treiber — Plug-and-Play ab Kernel 5.18+; stelle zuerst sicher, dass `apt install linux-firmware` aktuell ist.
- **AWUS036ACH (Realtek RTL8812AU)**: nutzt einen Out-of-Tree-Treiber — installiere den von der Community gepflegten `aircrack-ng/rtl8812au` und kompiliere ihn mit DKMS (und kümmere dich um die MOK-Signierung für Secure Boot; deaktiviere Secure Boot nicht).

**F5: Warum bootet der Guest nach der Auswahl des USB-3.0-Controllers nicht mehr?**
Einige ältere Guest-Kernel unterstützen xHCI nur schlecht. Wenn dein Kali eine ältere Version ist, versuche: Herunterfahren → zurück auf USB 2.0 (EHCI) Controller → Booten → Kernel aktualisieren → zurück auf USB 3.0. Halte Kali so aktuell wie möglich — dann ist die xHCI-Unterstützung am vollständigsten.

**F6: Der Adapter ist auf einem echten Rechner schnell, in der VM aber langsam. Ist das normal?**
Ja. In einer VM arbeitet der Adapter ungefähr mit der Geschwindigkeit der Weiterleitung durch die USB-Emulationsschicht, was im Vergleich zur direkten Verbindung an einem echten Rechner etwas Overhead bedeutet. Ein korrekter USB-3.0-Controller (xHCI) und ein aktueller Hypervisor halten diesen Overhead minimal. Bei starkem Leistungsabfall prüfe zuerst, ob der Controller nicht auf USB 1.1 hängen geblieben ist.

---

## 8. Fazit und Hardware-Empfehlungen

Mehr als 90 % der Fälle von «VM erkennt externen Adapter nicht» liegen an **Passthrough-Einstellungen** oder **Guest-Treibern**, die nicht sauber gemacht wurden — Hardwaredefekte sind selten. Führe die Schritte dieses Artikels der Reihe nach aus:

1. **Zuerst die Hardware per `lsusb` am Host bestätigen.**
2. **Bei VirtualBox immer ein versionsgleiches Extension Pack installieren** und auf Linux-Hosts der `vboxusers`-Gruppe beitreten; bei VMware prüfen, dass der `vmware-usbarbitrator`-Dienst läuft.
3. **Den USB-Controller auf USB 3.0 (xHCI) stellen** und per USB-Filter den Adapter automatisch mounten lassen.
4. **Im Guest die Ebene per `lsusb → iwconfig / ip link → dmesg` lokalisieren**; fehlt ein Treiber, installiere ihn — und rate nicht mehr, dass der Adapter kaputt ist.

**Empfohlene Hardware**: Der ALFA AWUS036AXML (MediaTek MT7921AU) hat auf Kali mit neuerem Kernel einen **im Kernel enthaltenen Treiber, Plug-and-Play** — nach dem Passthrough in der VM am wenigsten Aufwand. Der ALFA AWUS036ACH (Realtek RTL8812AU) ist ebenfalls brauchbar, aber denke daran, den Community-Treiber im Guest per DKMS zu kompilieren und die Secure-Boot-Signierung zu behandeln (siehe den RTL8812AU-DKMS-Diagnoseartikel dieser Website). Für beide wird empfohlen, am Host einen USB-Port／Hub mit eigener Stromversorgung zu nutzen, um die Variable «Adapter fällt ab» auf einen Schlag auszuschließen.

**Nächster Schritt**: Speichere eine Kopie des Arbeitsblatts aus Kapitel 6 auf dem Desktop deiner Kali-VM; bei jedem «Adapter wird nicht erkannt» erst das Ganze durchlaufen und dann entscheiden, ob du ein Support-Ticket eröffnest — folge der Tabelle, Daten heilen alles.

---

## Referenzressourcen

| Ressource | Link |
|-----------|------|
| Offizielle Oracle-VirtualBox-Downloadseite (Extension Pack) | https://www.virtualbox.org/wiki/Downloads |
| Offizielles VirtualBox-Handbuch: USB-Einstellungen und Filter | https://www.virtualbox.org/manual/ (Kapitel «USB» suchen) |
| VirtualBox-Handbuch: bekannte Einschränkungen (inkl. USB-Passthrough-Einschränkungen auf Apple Silicon) | https://www.virtualbox.org/manual/ (Changelog / Limitations) |
| Installationsbefehl für das VirtualBox Extension Pack | `vboxmanage help extpack` |
| Community-Treiber aircrack-ng RTL8812AU (für AWUS036ACH im Guest) | https://github.com/aircrack-ng/rtl8812au |
| Offizielle Produktseite ALFA AWUS036ACH | https://www.alfa.com.tw/products/awus036ach_1 |
| Offizielle Produktseite ALFA AWUS036AXML | https://www.alfa.com.tw/ |
| Yupitek-Techniksupport | https://yupitek.com/ |

> **Hinweis zur legalen Nutzung**: Das Aktivieren von Sicherheitsoperationen wie Monitor-Modus und Paketinjektion in der VM ist nur in Netzwerken zulässig, die dir gehören oder für die du eine ausdrückliche Testfreigabe hast. Der Nutzer muss die lokalen Gesetze einhalten und sicherstellen, dass alle Tests eine rechtliche Grundlage haben.