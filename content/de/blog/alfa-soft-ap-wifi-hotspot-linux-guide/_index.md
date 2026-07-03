---
title: "ALFA Network Soft AP Komplettanleitung 2026: WiFi-Hotspots auf Kali Linux, Ubuntu, Debian & Raspberry Pi 4/5 einrichten"
description: "Umfassende Untersuchung der Soft AP (hostapd/WiFi-Hotspot) Unterstützung von ALFA Network USB-WLAN-Adaptern auf Kali Linux, Ubuntu, Debian und Raspberry Pi 4/5. Mit vollständigen Einrichtungsanleitungen für AWUS036ACM, AWUS036ACH und AWUS036AXML."
date: 2026-05-21
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Soft-AP", "WiFi-Hotspot", "hostapd", "Kali-Linux", "Ubuntu", "Debian", "Raspberry-Pi", "AWUS036ACM", "AWUS036ACH", "AWUS036AXML", "MT7612U", "RTL8812AU", "MT7921AUN", "Linux-WiFi"]
featureimage: "/images/blog/alfa-soft-ap-wifi-hotspot-linux-guide.webp"
faq:
  - question: "Kann eine ALFA USB-Netzwerkkarte unter Linux als WiFi-Hotspot verwendet werden?"
    answer: "Dies hängt vom Chipsatz ab. Der AWUS036ACM (MT7612U) wird vollständig unterstützt und ist Plug-and-Play, der AWUS036ACH (RTL8812AU) wird bedingt unterstützt, und der AWUS036AXML wird nur teilweise unterstützt und erfordert Anpassungen."
  - question: "Welche ALFA-Netzwerkkarte eignet sich am besten für die Einrichtung eines Soft-AP auf einem Raspberry Pi?"
    answer: "Der AWUS036ACM ist die beste Wahl. Der in-kernel-Treiber ist Plug-and-Play, der Stromverbrauch beträgt nur 400 mA, was für die Stromversorgung des Pi geeignet ist, und er unterstützt WPA3 sowie VIF (Virtual Interface). Er ist auf allen Plattformen stabil."
  - question: "Wie kann ich überprüfen, ob die Netzwerkkarte den AP-Modus unterstützt?"
    answer: "Führen Sie den Befehl `iw list | grep -A 10 'Supported interface modes'` aus. Wenn die Ausgabe `* AP` enthält, unterstützt der Treiber Soft-AP, und hostapd kann ordnungsgemäß funktionieren."
  - question: "Welche Einschränkungen gibt es bei der Soft-AP-Nutzung mit dem RTL8812AU-Treiber?"
    answer: "WPA3 wird nicht unterstützt, es kann nur WPA2-PSK verwendet werden. VIF (Virtual Interface) wird nicht unterstützt, sodass zwei Karten zur Aufgabenteilung erforderlich sind. Der Stromverbrauch beträgt ca. 800 mA, weshalb auf dem Pi ein aktiver USB-Hub erforderlich ist."
  - question: "Was tun, wenn die WiFi-Verbindung beim Betrieb von Soft-AP auf dem AWUS036AXML plötzlich abbricht?"
    answer: "Der im MT7921AUN integrierte Bluetooth 5.2 kann WiFi stören. Führen Sie echo 'install btusb /bin/false' aus, um die Konfiguration in /etc/modprobe.d/ zu schreiben, und starten Sie den Computer neu, um den Bluetooth-Treiber dauerhaft zu deaktivieren."

---
> "Kann ich ALFA USB-WLAN-Adapter als WiFi-Hotspot (Soft AP) auf Kali Linux / Ubuntu / Raspberry Pi nutzen?"

# ALFA Network Soft AP Komplettanleitung 2026: WiFi-Hotspots auf Kali Linux, Ubuntu, Debian & Raspberry Pi 4/5 einrichten

{{< tldr >}}
Die Soft-AP-Kompatibilität der ALFA-Netzwerkkarten hängt vom Treiber des Chipsatzes ab. Der AWUS036ACM ist die stabilste Wahl für alle Plattformen, der AWUS036ACH ist nutzbar, unterstützt jedoch kein WPA3, und für den AWUS036AXML müssen Bluetooth deaktiviert und die Firmware aktualisiert werden. Der RTL8832BU wird nicht empfohlen.
{{< /tldr >}}

Der ALFA AWUS036ACM (MT7612U) ist die beste Wahl für Linux Soft AP: In-Kernel-Treiber für Plug-and-Play, WPA3- und VIF-Unterstützung inklusive. Der RTL8812AU wird mit Einschränkungen unterstützt, der MT7921AUN erfordert manuelle Konfiguration.

## Einleitung

Dies ist eine der häufigsten Fragen, die wir bei Yupitek erhalten. Die Frage klingt einfach, aber die Antwort variiert stark je nach Modell und Chipsatz — **nicht jeder USB-WLAN-Adapter kann im Soft AP-Modus betrieben werden.**

Dieser Artikel fasst über 500 Community-Diskussionen von GitHub (morrownr/USB-WiFi), Reddit, dem Raspberry Pi Forum und Nutzerfeedback zusammen, um einen ehrlichen, umfassenden Bericht darüber zu geben, welche ALFA-Adapter funktionieren, welche nicht, und die komplette Schritt-für-Schritt-Einrichtung.

---

## 1. Was ist Soft AP? So funktioniert es unter Linux {#what-is-softap}

**Soft AP (Software Access Point)** verwandelt einen gewöhnlichen USB-WLAN-Adapter in eine drahtlose Basisstation (Access Point) — hauptsächlich mit **hostapd**. Andere Geräte (Handys, Laptops, IoT-Geräte) können sich verbinden, ohne einen dedizierten Router zu benötigen.

Diese Funktion ist in folgenden Szenarien äußerst nützlich:

- **Reise-/Heimrouter**: Unterwegs oder beim Camping — ALFA-Adapter einstecken und sofort einen tragbaren WiFi-Hotspot erstellen
- **Penetrationstest-Labor**: Isoliertes Rogue AP für Sicherheitsforschung aufbauen
- **IoT-Relais**: Repeater in Funklöchern für die Datenübertragung von Sensoren
- **Edge-KI-Bereitstellung**: Industrieumgebungen ohne Kabelnetzwerk — Gerät als Hotspot nutzen
- **Notfallkommunikation**: Schnelles Aufbauen eines temporären Netzwerks bei Verbindungsausfall

### Die vier Kernkomponenten von Linux Soft AP

| Komponente | Funktion |
|-----------|----------|
| **hostapd** | Der zentrale Daemon für den Access Point — verwaltet SSID, Authentifizierung, Verschlüsselung |
| **nl80211** | Standard-Linux-Wireless-Schnittstelle — der Treiber muss dieses Framework unterstützen, um mit hostapd zu arbeiten |
| **dnsmasq** | DHCP-Server für die automatische IP-Adresszuweisung an verbundene Clients |
| **iptables / nftables** | Network Address Translation (NAT) — Clients teilen das Upstream-Netzwerk |

### Schlüsselkonzept: Master Mode

**Master Mode** (auch AP Mode oder Infrastructure Mode) ist eine Treiber-Fähigkeit. Unterstützt der Treiber keinen Master Mode, kann hostapd nicht starten — egal wie perfekt die Konfiguration ist.

AP-Modus-Unterstützung prüfen mit:

```bash
iw list | grep -A 10 "Supported interface modes"
```

Wenn die Ausgabe `* AP` enthält, unterstützt der Treiber des Adapters Soft AP. Wenn nicht, ist der Adapter für diesen Zweck unbrauchbar.

### 💡 In-Kernel vs Out-of-Kernel Treiber

Dies ist das **wichtigste** Konzept bei der Auswahl eines Soft AP-Adapters:

| Type | Description | Impact on Soft AP |
|------|-------------|-------------------|
| **In-Kernel Treiber** | In den offiziellen Linux-Kernel integriert; lädt automatisch beim Booten — keine manuelle Installation | ✅ Langzeitstabil; übersteht Kernel-Upgrades |
| **Out-of-Kernel Treiber** | Muss von GitHub heruntergeladen und manuell kompiliert werden; nach Kernel-Updates möglicherweise Neukompilierung nötig | ⚠️ Kann nach jedem Kernel-Update brechen |

**Für langfristige Soft AP-Stabilität sind In-Kernel-Treiber den Out-of-Kernel-Treibern weit überlegen.**

---

## 2. ALFA Produktlinie & Chipsatz-Übersicht {#product-lineup}

Hier ist die aktuelle ALFA-Produktlinie von Yupitek mit Chipsätzen und vorläufiger Soft AP-Bewertung:

| Model | Chipset | Driver Type | WiFi Standard | Soft AP Rating |
|-------|---------|-------------|---------------|----------------|
| **AWUS036ACM** | MediaTek MT7612U | In-Kernel (Kernel 4.19+) | WiFi 5 AC1200 Dual-Band | ✅ Volle Unterstützung |
| AWUS036ACH | Realtek RTL8812AU | Out-of-Kernel (ab 6.14+ In-Kernel) | WiFi 5 AC1200 Dual-Band | ⚠️ Bedingt |
| AWUS036AXML | MediaTek MT7921AUN | In-Kernel (5.18+, AP-Modus 5.19+) | WiFi 6E AX3000 Tri-Band | ⚠️ Teilweise |
| AWUS036AXM | MediaTek MT7921AUN | In-Kernel (wie oben) | WiFi 6E AX3000 Tri-Band | ⚠️ Teilweise |
| AWUS036AX | Realtek RTL8832BU | Out-of-Kernel (Kernel 6.12+ empfohlen) | WiFi 6 AX1800 Dual-Band | ❌ Nicht empfohlen |
| AWUS036AXER | Realtek RTL8832BU | Out-of-Kernel (wie oben) | WiFi 6 AX1800 Dual-Band | ❌ Nicht empfohlen |

> **Hinweis**: AWUS036ACHM (MT7610U) wurde eingestellt und ist nicht mehr auf der Yupitek-Produktseite gelistet. Dieser Artikel behandelt nur aktuell verfügbare Produkte.

---

## 3. AWUS036ACM (MT7612U) — ⭐ Beste Empfehlung {#acm}

### Soft AP Status: ✅ Volle Unterstützung

Der MT7612U ist der stabilste Soft AP-Chipsatz in ALFAs aktueller Produktlinie. Der Treiber `mt76x2u` ist seit 2018 (Kernel 4.19) im offiziellen Linux-Kernel — **einstecken und loslegen**, kein `git clone`, kein `dkms`, kein Neukompilieren nach Kernel-Upgrades.

### Kernvorteile

- **WPA2 + WPA3 Doppelunterstützung**: MediaTeks In-Kernel-Treiber unterstützt WPA3 SAE nativ — ein Vorteil, den Realtek-Treiber nicht bieten
- **VIF Unterstützung**: AP + Managed + Monitor gleichzeitig auf einem Adapter — keine zweite Karte erforderlich. Teilen Sie Ihr Netzwerk und überwachen Sie gleichzeitig das Funkspektrum
- **Extrem niedriger Stromverbrauch**: Maximal ~400mA, ideal für Raspberry Pi (Pi 4 USB-Subsystem liefert nur 1200mA insgesamt)
- **Plattformübergreifend**: Umfassend verifiziert auf Kali Linux 2022.x–2025.x, Ubuntu 22.04/24.04, Debian 11/12 und Raspberry Pi OS (Pi 3B+, 4, 5)

### Korrekte hostapd-Konfiguration (MT7612U)

Die folgenden Capability-Flags wurden durch jahrelange Community-Tests (morrownr/USB-WiFi) verifiziert. **Sie müssen exakt mit den tatsächlichen Hardware-Fähigkeiten des MT7612U übereinstimmen:**

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACM (MT7612U)
interface=wlan1
driver=nl80211
ssid=YourNetworkName
hw_mode=a                     # 5GHz; use g for 2.4GHz
channel=36                    # UNII-1, non-DFS, safest choice
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# MT7612U correct HT / VHT capabilities
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42    # Center frequency index for channel 36

# Security: WPA2 + WPA3 mixed mode
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK SAE       # WPA2 + WPA3 dual support
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=YourPassword
```

### ⚠️ Häufigster Fehler

Wenn `ht_capab` Capability-Flags enthält, die MT7612U nicht unterstützt (besonders beim Erzwingen bestimmter HT40-Konfigurationen über USB 2.0), stürzt hostapd still ab mit sehr wenig hilfreichen Fehlermeldungen. **Verwenden Sie nur die oben verifizierte Flag-Kombination — kopieren Sie keine Einstellungen von anderen Chipsätzen wie RTL8812AU.** (Quelle: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2))

### Community-Bewertungen

> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. I have tested the Alfa AWUS036ACM with many different computer systems and Linux distros. In my opinion, it is an outstanding USB WiFi adapter."
> — **morrownr**, Maintainer der maßgeblichen Linux USB WiFi Community-Wissensdatenbank auf GitHub

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> — eBay-Nutzerbewertung

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> — GitHub issue #2 Diskussionsthread

---

## 4. AWUS036ACH (RTL8812AU) — Funktioniert, aber mit Kompromissen {#ach}

### Soft AP Status: ⚠️ Bedingte Unterstützung

Der RTL8812AU ist ALFAs kultigster Penetrationstest-Chipsatz und ein langjähriger Favorit der Kali Linux Community. Seine Soft AP-Funktionalität funktioniert — grundlegende Hotspot-Erstellung ist in Ordnung — aber Realteks Out-of-Kernel-Treiberarchitektur bringt mehrere hartnäckige Einschränkungen mit sich:

### Bekannte Einschränkungen

1. **Keine WPA3-Unterstützung**: Obwohl der RTL8812AU-Treiber WPA3-Unterstützung anzeigt, haben mehrere Benutzer bestätigt, dass es nicht funktioniert. **Nur WPA2-PSK.**
2. **Keine VIF-Unterstützung**: AP + Monitor-Modus können nicht gleichzeitig auf derselben Karte ausgeführt werden. Für gleichzeitiges AP und Monitoring sind zwei separate Adapter erforderlich.
3. **Kali Linux 2025.x Treiberprobleme**: Der neueste aircrack-ng/rtl8812au-Treiber auf dem neuesten Kali hat Kompatibilitätsprobleme — Sie müssen auf einen spezifischen alten Commit (`63cf0b4`) zurückrollen. Die Situation kann sich mit Kernel 6.14+s In-Kernel-rtw88-Treiber verbessern.
4. **Hoher Stromverbrauch**: Maximal ~800mA — auf Raspberry Pi mit mehreren USB-Geräten kann dies Systeminstabilität verursachen. Verwenden Sie einen aktiven USB-Hub.

### hostapd-Konfiguration (RTL8812AU)

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACH (RTL8812AU)
# NOTE: Completely different capabilities from MT7612U!
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]

# Security: WPA2 only, do NOT add WPA3
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
```

### Treiberinstallation (Kali Linux / Ubuntu / Debian)

```bash
sudo apt update && sudo apt install -y dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
# Kali 2025.x requires the older commit
git checkout 63cf0b4
make && sudo make install
sudo modprobe 88XXau
```

### Community-Bewertungen

> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine."
> — GitHub issue #2 user

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> — morrownr technical notes

### Urteil für ACH

Wenn Sie bereits einen AWUS036ACH besitzen, kann er als Soft AP dienen (grundlegende Hotspot-Funktion funktioniert). Aber wenn Sie noch nicht gekauft haben und Ihr Hauptziel Soft AP ist, **nehmen Sie den ACM.**

---

## 5. AWUS036AXML / AWUS036AXM (MT7921AUN) — Mit Vorsicht vorgehen {#axml}

### Soft AP Status: ⚠️ Teilweise Unterstützung — Bekannte Firmware-/Treiberprobleme

AWUS036AXML und AWUS036AXM sind ALFAs WiFi 6E Tri-Band-Flaggschiffe mit 2,4 GHz, 5 GHz und dem neuen 6 GHz-Band. Der In-Kernel-Treiber `mt7921u` ist seit Kernel 5.18 enthalten, mit AP-Modus-Unterstützung offiziell hinzugefügt in 5.19. Allerdings integriert der MT7921AUN-Chip auch Bluetooth 5.2 — was zum größten Community-Kopfzerbrechen 2024–2025 wurde.

### AP-Modus Kernel-Versions-Meilensteine

| Mode | Minimum Kernel |
|------|---------------|
| Managed (normal WiFi) | 5.18+ |
| **AP Mode (Soft AP)** | **5.19+** |
| AP/VLAN | 5.19+ |
| P2P-GO (Wi-Fi Direct AP) | 6.4+ |

### Bekannte Probleme und Lösungen

#### Problem 1: Bluetooth-Interferenz verursacht WiFi-Abstürze

Auf Kernels 6.6+ verursachen Änderungen am BT-Subsystem sporadische WiFi-Abstürze mit mt7921u. Reproduzierbarkeit variiert je nach Systemumgebung. **Die effektivste Problemumgehung ist das Deaktivieren des btusb-Treibers:**

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

#### Problem 2: Veraltete Firmware

Wenn die MediaTek-Firmware des Systems zu alt ist, wird der Adapter möglicherweise nicht korrekt erkannt. Installieren Sie Firmware von November 2024 oder neuer:

```bash
# Check current firmware version
dmesg | grep "WM Firmware"
# Should show: Build Time: 20241106151045 or newer

# If outdated, download from kernel.org
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek/
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek/
sudo reboot
```

#### Problem 3: hostapd-Versionsanforderungen

Einige Benutzer berichten, dass hostapd aus Git kompiliert werden muss, um vollständige WiFi 6 AP-Modus-Unterstützung zu erhalten. Systempaketmanager-Versionen können unvollständig sein.

#### Problem 4: Tx Power-Anzeigeanomalie im AP-Modus

`iw` zeigt nur 3 dBm ohne Anpassungsmöglichkeit an, aber der Chip hat tatsächlich einen internen Verstärker — dies ist ein Kernel-Treiber-Anzeigeproblem, keine Hardware-Einschränkung.

#### Problem 5: Monitor-Modus-Probleme auf bestimmten Kernel-Versionen

Stand Dezember 2025 haben Kernel 6.18 und einige frühere mt7921u-Treiberversionen Monitor-Modus-Probleme.

### Community Review

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> — **fhteagle**, [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

### Urteil für AXML/AXM

Wählen Sie diese, wenn Sie das 6 GHz-Band von WiFi 6E benötigen und bereit sind, gelegentlich Einstellungen anzupassen. **Für Produktionsumgebungen, die felsenfeste Soft AP-Stabilität erfordern, wählen Sie stattdessen ACM.**

---

## 6. AWUS036AX / AWUS036AXER (RTL8832BU) — Nicht für Soft AP empfohlen {#ax}

### Soft AP Status: ❌ Nicht empfohlen

Trotz WiFi 6-Spezifikation ist der RTL8832BU-Chip ein "Multi-State"-Gerät — er listet sich standardmäßig als USB-Massenspeicher und benötigt einen USB Mode Switch unter Linux, bevor er als WLAN-Adapter funktioniert.

**Hauptprobleme:**

1. **Multi-State-Gerät**: Fügt Bereitstellungskomplexität hinzu — erscheint beim Einstecken nicht als Netzwerkadapter
2. **Monitor-Modus-Einschränkungen**: Unvollständige Unterstützung unter Kernel 6.14
3. **Minimale Soft AP Community-Fälle**: Fast keine realen RTL8832BU Soft AP-Fälle, im Vergleich zu zahlreichen MT7612U- und RTL8812AU-Beispielen
4. **Community-Dokumentation rät explizit ab**: morrownr/USB-WiFi markiert diesen Chipsatz als "nicht für Penetrationstests empfohlen"

> Die offizielle Dokumentation von Yupitek stellt klar: "AWUS036AX / AWUS036AXER mit RTL8832BU-Chipsatz hat eingeschränkte Monitor-Modus-Unterstützung unter Kernel 6.14 und wird nicht für Penetrationstests empfohlen. Verwenden Sie stattdessen AWUS036ACH oder AWUS036AXML."

---

## 7. Plattform-Kompatibilitätsmatrix {#compat-matrix}

### AWUS036ACM (MT7612U)

| Platform | Soft AP | Notes |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ✅ | In-kernel, plug-and-play, kernel 5.x / 6.x |
| Ubuntu 22.04 / 24.04 | ✅ | In-kernel, zero config, use LTS |
| Debian 11 / 12 | ✅ | In-kernel, stable |
| Raspberry Pi 4 (RPi OS) | ✅ | Lowest power (400mA), long-term morrownr verification. Pi 4 USB 3.0 port preferred |
| Raspberry Pi 5 (RPi OS) | ✅ | Same driver as Pi 4, stable |

### AWUS036ACH (RTL8812AU)

| Platform | Soft AP | Notes |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ⚠️ | Needs external driver; 2025.x requires commit `63cf0b4`. Kernel 6.14+ rtw88 may improve |
| Ubuntu 22.04 / 24.04 | ⚠️ | May need manual rtw88 or aircrack-ng driver installation |
| Debian 11 / 12 | ⚠️ | Same as above |
| Raspberry Pi 4 | ⚠️ | Works but high power (800mA); use powered USB hub |
| Raspberry Pi 5 | ⚠️ | Same; Pi 5 USB controller differences may affect behavior |

### AWUS036AXML / AWUS036AXM (MT7921AUN)

| Platform | Soft AP | Notes |
|----------|---------|-------|
| Kali Linux 2022.x (kernel 5.18+) | ✅ | Disable btusb, update firmware |
| Kali Linux 2024.x / 2025.x | ⚠️ | Kernel 6.11+ BT/WiFi conflict, unstable |
| Ubuntu 24.04 (kernel 6.8+) | ⚠️ | Issues reported late 2024 |
| Ubuntu 25.04 / CachyOS (kernel 6.14+) | ✅ | Plug-and-play, significant new-kernel improvement |
| Debian 12 | ⚠️ | Depends on kernel version |
| Raspberry Pi 4 / 5 | ⚠️ | Success cases exist but verify firmware + disable BT |

### AWUS036AX / AWUS036AXER (RTL8832BU)

| Platform | Soft AP | Notes |
|----------|---------|-------|
| Kali Linux | ❌ | Multi-state, USB mode switch needed, minimal community cases |
| Ubuntu / Debian | ❌ | Same |
| Raspberry Pi 4 / 5 | ❌ | Same |

---

## 8. Vollständige Soft AP Einrichtungsanleitung (AWUS036ACM) {#setup-guide}

Im Folgenden finden Sie eine vollständige Schritt-für-Schritt-Anleitung zur Einrichtung eines 5GHz Soft AP mit AWUS036ACM auf Raspberry Pi 4.

### Schritt 1: Adaptererkennung und Treiber überprüfen

```bash
# Bestätigen, dass der Adapter erkannt wurde
lsusb | grep MediaTek
# Erwartet: Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U

# Prüfen, ob der Treiber geladen ist
dmesg | grep mt76
# Erwartet: mt76x2u 1-1.4:1.0 wlx00c0ca9821a5: renamed from wlan0

# AP-Modus-Unterstützung bestätigen
iw list | grep -A 10 "Supported interface modes"
# Prüfen, dass die Ausgabe "* AP" enthält
```

### Schritt 2: Erforderliche Pakete installieren

```bash
sudo apt update
sudo apt install -y hostapd dnsmasq iptables
```

### Schritt 3: hostapd konfigurieren

Erstellen Sie `/etc/hostapd/hostapd.conf`:

```ini
interface=wlan0
driver=nl80211
ssid=Yupitek_AP
hw_mode=a                       # a=5GHz, g=2.4GHz
channel=36                      # UNII-1, non-DFS, safest choice
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# HT/VHT settings (MT7612U specific)
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42

# WPA2 + WPA3 mixed mode
wpa=2
wpa_passphrase=MySecurePassword123
wpa_key_mgmt=WPA-PSK SAE
wpa_pairwise=CCMP
rsn_pairwise=CCMP

auth_algs=1
macaddr_acl=0
ignore_broadcast_ssid=0
```

### Schritt 4: dnsmasq (DHCP) konfigurieren

Erstellen Sie `/etc/dnsmasq.conf`:

```ini
interface=wlan0
dhcp-range=192.168.10.2,192.168.10.100,255.255.255.0,12h
dhcp-option=3,192.168.10.1
dhcp-option=6,8.8.8.8,8.8.4.4
```

### Schritt 5: Statische IP und NAT einrichten

```bash
# Statische IP für wlan0 zuweisen
sudo ip addr add 192.168.10.1/24 dev wlan0

# IP-Weiterleitung aktivieren
sudo sysctl net.ipv4.ip_forward=1

# NAT konfigurieren (eth0 als Upstream-Interface angenommen)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# iptables-Regeln persistent speichern
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```

### Schritt 6: Dienste starten

```bash
sudo systemctl unmask hostapd
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# Dienststatus prüfen
sudo systemctl status hostapd
sudo systemctl status dnsmasq

# Automatischen Start beim Booten aktivieren
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```

Nach Abschluss suchen Sie auf Ihrem Telefon oder Laptop nach WiFi — Sie sollten die SSID `Yupitek_AP` sehen.

---

## 9. Häufige Fehlerbehebung {#troubleshooting}

### Q1: hostapd stürzt sofort nach dem Start ab

**Symptom**: `sudo systemctl status hostapd` zeigt `exited` oder `failed`

**Wahrscheinliche Ursache**: `hostapd.conf` enthält Capability-Flags, die der Chipsatz nicht unterstützt

**Lösung**: Entfernen Sie überflüssige Flags. Für MT7612U (ACM) ist die sicherste Vorgehensweise die Verwendung der verifizierten Konfiguration aus Abschnitt 3. **Kopieren Sie kein ht_capab von anderen Chipsätzen.**

---

### Q2: Clients verbinden sich, können aber nicht ins Internet

**Symptom**: WiFi verbunden, IP erhalten, aber `ping 8.8.8.8` erhält keine Antwort

**Checkliste**:

```bash
# 1. Prüfen, ob IP-Weiterleitung aktiviert ist
cat /proc/sys/net/ipv4/ip_forward
# Sollte ausgeben: 1

# 2. Prüfen, ob NAT-Regeln existieren
sudo iptables -t nat -L POSTROUTING -v
# Sollte MASQUERADE-Regel zeigen

# 3. Bestätigen, dass das Upstream-Interface funktioniert
ping -I eth0 8.8.8.8
```

---

### Q3: 5GHz AP nicht sichtbar oder instabil

**Mögliche Ursachen**:

1. **Verwendung von DFS-Kanälen (100–144)**: MT7612U / MT7610U haben keine DFS-Unterstützung — verwenden Sie UNII-1-Kanäle (36–48)
2. **Unzureichende Sendeleistung**: Stellen Sie sicher, dass die Antennen richtig an den RP-SMA-Anschlüssen befestigt sind
3. **USB-Stromversorgung unzureichend** (Raspberry Pi): Verwenden Sie das offizielle 5A-Netzteil oder einen aktiven USB-Hub

---

### Q4: hostapd startet auf Raspberry Pi ständig neu

**Symptom**: `dmesg` zeigt häufige USB-Reset-Meldungen

**Wahrscheinliche Ursache**: USB-Port-Stromversorgung unzureichend (besonders bei AWUS036ACH Hochleistungs-Chipsatz, max. 800mA)

**Lösung**:
- Offizielles Pi 5A-Netzteil verwenden
- Aktiven USB-Hub verwenden
- Adapter in USB 3.0-Port einstecken (nur Pi 4)

---

### Q5: AWUS036AXML/AXM WiFi fällt plötzlich aus oder startet nicht

**Wahrscheinliche Ursache**: Bluetooth-Subsystem stört WiFi (MT7921AUN hat eingebautes BT 5.2)

**Lösung**: Bluetooth-Treiber dauerhaft deaktivieren

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## 10. Technischer Deep Dive: VIF, WPA3, DFS-Kanäle {#technical}

### VIF (Virtuelle Schnittstelle): Eine Karte, mehrere Rollen

VIF (Virtual Interface) ermöglicht es einem einzelnen physischen Adapter, mit mehreren logischen Schnittstellen gleichzeitig zu arbeiten. Zum Beispiel: eine Schnittstelle verbindet sich mit dem Upstream-Router (Managed-Modus), während eine andere als AP (Master-Modus) für andere Geräte dient.

Drei häufige Szenarien:

| Scenario | VIF Required? | Best Adapter |
|----------|--------------|--------------|
| Grundlegendes NAT-Routing (eth0 Upstream + wlan AP) | ❌ Nein | Jeder AP-fähige Adapter |
| Drahtlose Überbrückung (WiFi-Empfang + WiFi AP gleichzeitig) | ✅ Ja | ACM (MT7612U) |
| Monitor + AP gleichzeitig (Sicherheitsforschung / Rogue AP) | ✅ Ja | ACM (MT7612U) |

**VIF Praxisbeispiel (MT7612U):**

```bash
# Zusätzliches AP virtuelles Interface neben bestehendem wlan1 erstellen
sudo iw phy phy1 interface add ap0 type __ap
sudo ip link set ap0 up
# Jetzt kann wlan1 Upstream verbinden, während ap0 hostapd ausführt
```

Nur MediaTek In-Kernel-Treiber (mt76x2u, mt7921u) unterstützen VIF vollständig. Realtek Out-of-Kernel-Treiber haben diese Fähigkeit im Wesentlichen nicht — wenn Sie AP + Monitor gleichzeitig benötigen, müssen Sie zwei separate Adapter verwenden.

---

### WPA3-Unterstützungsvergleich

| Chipset | Corresponding Model | WPA2 | WPA3 |
|---------|-------------------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ Native SAE-Unterstützung |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ Native SAE-Unterstützung |
| RTL8812AU | AWUS036ACH | ✅ | ❌ Behauptet Unterstützung, funktioniert aber nicht |
| RTL8832BU | AWUS036AX / AXER | ✅ | ⚠️ Unbestätigt |

---

### 5GHz Soft AP Kanalwahl: DFS vermeiden

DFS (Dynamic Frequency Selection)-Kanäle (ch100–ch140) erfordern Kernel-Level-Radardetektion. MT7612U und ähnliche Chipsätze haben keine DFS-Unterstützung. Für den 5GHz AP-Modus wählen Sie:

| Band | Recommended Channels | Reason |
|------|---------------------|--------|
| **UNII-1** | **36, 40, 44, 48** | Alle Chipsätze unterstützt; sicherste Wahl |
| UNII-2 (DFS) | 52–144 | Meist nicht unterstützt; nicht empfohlen |
| UNII-3 | 149–165 | Teilweise Unterstützung (regionsabhängig) |

---

## 11. Praxisbeispiele aus der Community {#real-cases}

### Fall 1: RPi4B + AWUS036ACM = Langzeitstabiler Heim-5GHz-AP

**Quelle**: morrownr/7612u GitHub Wissensdatenbank
**Szenario**: morrownr verwendet langfristig RPi4B + AWUS036ACM als Heim-5GHz-AP, gepaart mit dem eingebauten 2,4GHz des Pi für Dual-Band-Service
**Ergebnis**: Langzeitstabiler Betrieb, keine Neustarts erforderlich, als "hervorragend" bewertet
**Konfiguration**: hostapd + dnsmasq + iptables NAT

### Fall 2: RPi3B+ + ACM — Anfänglicher Absturz, behoben

**Source**: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
**Problem**: hostapd crashed when run over USB 2.0 on RPi3B+
**Root Cause**: `ht_capab` contained HT40 flags unsupported under USB 2.0 bandwidth limits
**Solution**: Removed excess flags; successfully launched on Kali Linux

### Fall 3: Pi PwnBox + AWUS036ACH = Red Team Rogue AP

**Source**: GitHub koutto/pi-pwnbox-rogueap
**Scenario**: RPi3B+ Rogue AP platform: one RTL8812AU (AWUS036ACH) for AP, another RT3070 (AWUS036NEH) for packet injection attacks
**Key Finding**: Because RTL8812AU lacks VIF, two separate adapters were required (unlike ACM which handles both on a single card)

### Fall 4: AWUS036AXML Stabiler AP auf RPi3B ArchLinux ARM

**Source**: [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
**Scenario**: User successfully ran AWUS036AXML in AP mode on RPi3B ArchLinux aarch64
**Quote**: "It's the most stable mt7921 in my collection."
**Key Requirements**: hostapd compiled from git + btusb disabled

### Fall 5: AWUS036ACHM (MT7610U, eingestellt) Volle Geschwindigkeit AP auf Pi4

**Source**: [GitHub Discussion #31](https://github.com/morrownr/USB-WiFi/discussions/31)
**Problem**: Initial config only achieved 65 Mbps link speed, far below AC 5GHz full speed
**Solution**: Added correct `vht_oper_chwidth=1` and `vht_oper_centr_freq_seg0_idx`; achieved 433 Mbps link rate
**Relevance for ACM**: The same VHT parameter configuration is critical for MT7612U (ACM) as well

---

{{< faq >}}

## 12. Kaufempfehlungen & Endgültiges Urteil {#recommendations}

### Schnelle Entscheidungsmatrix

| Rating | Model | Best For | One-Liner |
|--------|-------|----------|-----------|
| 🥇 **Top-Empfehlung** | **AWUS036ACM** | Alle, besonders Erstnutzer von Soft AP | All-Plattform-stabil, null Aufwand |
| 🥈 Nutzbar | AWUS036ACH | Benutzer, die dieses Modell bereits besitzen | Benötigt Treiber, kein WPA3 |
| 🥉 Fortgeschritten | AWUS036AXML | Benutzer, die WiFi 6E benötigen und bereit sind zu basteln | 6GHz-Vorteil, manuelle Korrekturen nötig |
| ❌ Überspringen | AWUS036AX / AXER | N/A | Soft AP nicht community-validiert |

### 🎯 Entscheidungsleitfaden

- **Benötigen Sie einen stabilen Soft AP auf Kali / Ubuntu / Debian / Raspberry Pi 4 oder 5?**
  → Nehmen Sie den **AWUS036ACM**, ohne Diskussion.

- **Besitzen Sie bereits einen AWUS036ACH und möchten Soft AP ausprobieren?**
  → Es funktioniert, aber nur WPA2, und Sie müssen den Treiber installieren. Wenn Sie diese Einschränkungen akzeptieren, los geht's.

- **Benötigen Sie WiFi 6E (6 GHz-Band) und sind bereit, Dinge zu konfigurieren?**
  → AWUS036AXML — denken Sie daran, den BT-Treiber zu deaktivieren und Kernel ≥ 6.6 LTS zu überprüfen.

- **Hauptzweck ist Soft AP, nicht Penetrationstest?**
  → AWUS036ACM ist die einzige Wahl mit umfassender Community-Verifizierung auf allen Plattformen.

---

### Fazit

Der Kernfaktor beim Aufbau eines Soft AP ist nicht die WiFi-Geschwindigkeit oder die Antennenanzahl — **es ist die AP-Modus-Unterstützung des Chipsatztreibers.**

Unter allen von uns untersuchten ALFA-Produkten ist **AWUS036ACM (MT7612U)** der einzige Adapter, der gleichzeitig erfüllt: In-Kernel-Treiber, natives WPA3, VIF virtuelle Schnittstellen, geringer Stromverbrauch und plattformübergreifende Stabilität. Er ist der Goldstandard für Soft AP.

AWUS036ACH (RTL8812AU) funktioniert, wenn Sie die Einschränkungen akzeptieren. AWUS036AXML/AXM (MT7921AUN) hat großes Potenzial, aber die Treiberreife ist noch in Arbeit. AWUS036AX/AXER (RTL8832BU) — nicht für diesen Anwendungsfall empfohlen.

**Wenn Sie zum ersten Mal einen Soft AP auf Raspberry Pi oder Kali Linux einrichten — wählen Sie ACM. Sie werden es nicht bereuen.**

---

### Kauf-Links

- [AWUS036ACM — Soft AP Top Pick](/de/products/alfa/awus036acm/)
- [AWUS036ACH — Classic Pentesting Adapter](/de/products/alfa/awus036ach/)
- [AWUS036AXML — WiFi 6E Tri-Band Flagship](/de/products/alfa/awus036axml/)
- [ALFA Network Full Product Line](/de/products/alfa/)

### Weiterführende Literatur

- [AWUS036ACH vs AWUS036ACM: Full Chipset Driver Comparison](/en/blog/awus036ach-vs-awus036acm/)
- [AWUS036ACM IBSS & Mesh on Raspberry Pi](/en/blog/)
- [morrownr/USB-WiFi — Die maßgebliche Linux USB WiFi Wissensdatenbank](https://github.com/morrownr/USB-WiFi) (4.100+ Sterne)
- [morrownr/7612u — MT7612U Referenz (inkl. RPi4B Bridged AP Tutorial)](https://github.com/morrownr/7612u)
- [DeepWiki — morrownr/USB-WiFi Auto-kuratierte Wissensdatenbank](https://deepwiki.com/morrownr/USB-WiFi)

---

### 📚 Datenquellen

Dieser Artikel aggregiert Informationen aus:
- **morrownr/USB-WiFi** GitHub Wissensdatenbank (4.100+ Sterne) mit vollständigen iw_list-Aufzeichnungen
- **morrownr/7612u** — MT7612U Bridged AP auf RPi4B Tutorial
- **GitHub Issue Tracker** — issue #2 (ACM AP Konfiguration), #476 (AXML AP Tests), Discussion #31 (ACHM Volllast-AP)
- **koutto/pi-pwnbox-rogueap** — Alfa Adapter RogueAP Implementierungsfall
- **Rokland** autorisierter Händler Linux-Support-Seiten
- **Lab401** technische Bewertungen und 2025 Pentesting Best-Pick-Berichte
- **Raspberry Pi Offizielles Forum** — Pi 4/5 USB WiFi Kompatibilitätsdiskussionen
- **Yupitek bestehender Blog** — ACM China Installationsanleitung, AXML WiFi 6E Review, Kali Linux 2026 beste Adapter

---

> **Tags**: #ALFANetwork #SoftAP #WiFiHotspot #hostapd #KaliLinux #Ubuntu #Debian #RaspberryPi #AWUS036ACM #AWUS036ACH #AWUS036AXML #MT7612U #RTL8812AU #MT7921AUN #Yupitek
>
> **Autor**: Yupitek Ltd — ALFA Network Autorisierter Distributor Taiwan
>
> **Haftungsausschluss**: Forschungsdaten aktuell Stand Mai 2026. Linux-Kernel und Distributionen entwickeln sich weiter; Treiberunterstützung kann sich mit neuen Versionen ändern. Überprüfen Sie die Kernel-Version und Treiberkompatibilität der Zielplattform vor der Bereitstellung.
>
> **Technischer Support**: Bei Problemen mit der Soft AP-Einrichtung kontaktieren Sie den technischen Support von Yupitek Taiwan. Produktanfragen: [yupitek.com](https://yupitek.com/de/).

## Referenzen

1. [morrownr/USB-WiFi GitHub Wissensdatenbank](https://github.com/morrownr/USB-WiFi)
2. [hostapd Offizielle Dokumentation](https://w1.fi/cgit/hostap/)
3. [Linux Wireless mt76 Treiber](https://wireless.wiki.kernel.org/en/users/Drivers/mt76)
4. [Raspberry Pi Offizielle Dokumentation](https://www.raspberrypi.com/documentation/)
5. [Kali Linux Offizielle Dokumentation](https://www.kali.org/docs/)
