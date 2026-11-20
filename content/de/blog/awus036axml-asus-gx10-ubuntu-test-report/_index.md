---
title: "AWUS036AXML im Test: Wi-Fi-6-+-Bluetooth-Kombikarte auf dem ASUS GX10 (ARM64 / Ubuntu 24.04) – ein ehrlicher Bericht: AP stabil, Injektion fehlgeschlagen"
slug: awus036axml-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axml-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axml
  - mt7921
  - mt7921u
  - wifi-6
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - ap-mode
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036AXML (Wi-Fi + Bluetooth) im Praxistest auf ASUS GX10 / Ubuntu 24.04 ARM64: AP, WPA3 und Monitor nutzbar, doch die Injektion schlägt fehl und ein Handshake lässt sich nicht erfassen – für Penetrationstests nicht empfohlen."
faq:
  - question: "Kann der AWUS036AXML Paket-Injektion (packet injection) durchführen?"
    answer: "Auf unserer Testplattform (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia) nicht. aireplay-ng --test meldet No Answer, Found 0 APs; der AP-weise Einzeltest ergibt nur No such BSSID available. Selbst wenn ein normaler Scan den AP sieht (etwa -54 dBm), empfängt die Karte im Kontext der Injektionswerkzeuge dessen Beacon nicht, sodass deauth und Handshake-Erfassung (0 Stück) beide nicht nutzbar sind. Die Ursache ist eine mac80211-chanctx-Regression im kernel 6.16+, nicht eine prinzipielle Injektionsunfähigkeit des Chips; der AWUS036AXM liefert dasselbe Ergebnis. Wer Injektion braucht, wählt stattdessen AWUS036EACS, ACH oder ACS."
  - question: "Funktioniert das Bluetooth des AWUS036AXML unter Ubuntu?"
    answer: "Im Test auf dieser Maschine ist Bluetooth nutzbar: mit bluetoothctl / hciconfig bestätigt, dass der hci-Controller UP ist, BLE- und klassische Bluetooth-Geräte gescannt werden können und Wi-Fi und Bluetooth gleichzeitig nutzbar sind (Koexistenz). Es ist ein Wi-Fi-+-Bluetooth-Kombigerät; Hinweis: Beim erneuten Einstecken bleibt es gelegentlich beim WiFi-probe hängen und erzeugt keine wlx-Schnittstelle – an einem anderen USB-Port erneut einstecken stellt es wieder her."
  - question: "Muss man für den AWUS036AXML unter Ubuntu 24.04 einen Treiber nachinstallieren?"
    answer: "Nein. Der mt7921u-Treiber ist in kernel 6.17 enthalten, nach dem Einstecken sieht man in dmesg, wie mt7921u die Schnittstelle in wlx plus MAC umbenennt (USB ID 0e8d:7961), ohne DKMS, ohne Kompilieren. Der Treiber bietet keinen IBSS- und keinen Mesh-Modus."
  - question: "Kann der AWUS036AXML einen AP öffnen und WPA3 unterstützen?"
    answer: "Ja, das ist seine stabilste Anwendung. In 2,4 GHz (802.11n, MCS 10) und 5 GHz VHT80 (VHT-NSS2) konnte sich jeweils ein iPhone verbinden und wurde authorized; WPA3-SAE verbindet das iPhone 15 Pro mit sae_pwe=0 (MFP: yes; getestet auf 2,4 GHz und 6 GHz, nicht auf 5 GHz); bei STA+AP parallel liegt der ping der STA-Seite bei etwa 4,4 ms. Obwohl als Wi-Fi-6-Chip positioniert, war auf dieser Maschine zusätzlich das 6-GHz-Band nutzbar (selbst aufgesetzter 6135-MHz-AP, iPhone 15 Pro verband sich mit 802.11ax und erhielt eine IP)."
  - question: "Worin unterscheiden sich AWUS036AXML und AWUS036AXM, welche sollte man wählen?"
    answer: "Auf dieser Plattform ist das Wi-Fi-Verhalten beider gleich: beide nutzen mt7921u, die Injektion schlägt gleichermaßen fehl, der Monitor-Empfang ist gleichermaßen schwach, AP, WPA3 und VIF sind gleichermaßen nutzbar. Der Unterschied: Der AXML hat zusätzlich Bluetooth (auf dieser Maschine im Test nutzbar) und auf dieser Maschine war das 6-GHz-Band nutzbar, während Bluetooth und 6 GHz des AXM in dieser Runde nicht gesondert getestet wurden. Für reinen AP oder normale Verbindung kann man beide wählen; für Injektion oder Handshake sollte man keine von beiden wählen."
draft: false
---

{{< tldr >}}Der AWUS036AXML ist auf ASUS GX10 / Ubuntu 24.04 ARM64 für AP, WPA3, VIF und passiven Monitor nutzbar, Bluetooth und das 6-GHz-Band waren auf dieser Maschine im Test ebenfalls nutzbar, doch die Injektion schlägt im Test fehl (No Answer / Found 0 APs) – deauth oder das Erfassen eines Handshakes ist nicht möglich, für Penetrationstests nicht empfohlen; positioniert als reine AP- und normale Verbindungskarte.{{< /tldr >}}

Der ALFA AWUS036AXML ist unter diesen 9 Karten das einzige „MediaTek Wi-Fi 6 + Bluetooth“-Kombimodell. Er teilt sich mit dem bluetoothlosen AWUS036AXM dieselbe Chipgeneration (MT7921, über den `mt7921u`-Treiber), der Unterschied liegt nur in der zusätzlichen Bluetooth-Einheit. Am häufigsten fragen Kunden immer noch dieselben drei Dinge: Kommt der Monitor rein? Kann er injizieren? Kann er einen AP aufsetzen? Dieser Artikel nimmt den AWUS036AXML einzeln heraus und testet ihn auf dem ASUS GX10 (ARM64) mit Ubuntu 24.04 Punkt für Punkt, um ein für alle Mal klarzustellen, was geht und was nicht – besonders die entscheidendste Einschränkung: **Die Injektion schlägt auf dieser Plattform fehl.**

Zuerst die Positionierung klarstellen: Alle folgenden Messungen wurden auf Yupiteks eigener Hardware, im eigenen Büro-WLAN (SSID `YUPITEK`), gegen unser eigenes Testgerät (iPhone 7 Plus, WPA3 zusätzlich mit iPhone 15 Pro nachgemessen) durchgeführt. Das ist die Hardware-Verifikation von Produktkompatibilität und Fähigkeitsgrenzen durch den Distributor, keine Bedienanleitung gegen fremde Netzwerke. Die Monitor-, AP- und Injection-Selbsttests im Artikel erfolgen ausnahmslos in einer eigenen, geschlossenen Umgebung gegen eigene Geräte.

## 1. Diese Karte und die Testplattform

- **Rechenplattform**: ASUS GX10 (ARM64 / aarch64)
- **Betriebssystem**: Ubuntu 24.04 LTS
- **Kernel-Version**: kernel 6.17.0-1014-nvidia
- **Getestete Karte**: ALFA AWUS036AXML (MediaTek MT7921AUN, Wi-Fi 6 / 2x2 / +BT)
- **Testgerät**: Apple iPhone 7 Plus (WPA3-SAE zusätzlich mit iPhone 15 Pro nachgemessen)
- **Testumgebung**: eigenes Büro-WLAN, SSID `YUPITEK`, 2,4GHz ch5 / 5GHz ch36, ch157
- **Testzeitraum**: 2026-11-16 bis 2026-11-18, Messung an echter Hardware

Alle Ergebnisse sind mit tatsächlich gemessenen Zahlen oder Zuständen protokolliert, nicht aus dem Datenblatt abgeleitet; MAC-Adressen sind in der Ausgabe mit `xx` maskiert.

## 2. Hardware und Treiber: MT7921AUN, nach dem Einstecken nutzbar

| Punkt | Spezifikation |
|---|---|
| Modell | AWUS036AXML |
| Chip | MediaTek MT7921AUN |
| USB ID | `0e8d:7961` (MediaTek Inc. Wireless_Device) |
| in-kernel Treiber | `mt7921u` |
| Generation / Streams | Wi-Fi 6 / 2x2 (2T2R) |
| Bluetooth | ja (BT-+-WiFi-Kombigerät; auf dieser Maschine im Test hci-Controller UP, BLE- und klassische Bluetooth-Geräte scannbar, WiFi+BT koexistenzfähig) |
| USB-Aufzählung | USB 3 |
| Schnittstellenbenennung | `wlx<MAC>` (z. B. `wlx00c0cabd65b9`) |

Die Erkennung ist direkt: Nach dem Einstecken sieht man mit `lsusb` die MediaTek-USB-ID und in `dmesg`, wie `mt7921u` geladen wird und die Schnittstelle umbenennt:

```bash
lsusb | grep 0e8d:7961
# Bus 004 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device

sudo dmesg | grep mt7921u | tail -1
# mt7921u 4-1:1.3 wlx00c0cabd65b9: renamed from wlan0
```

Zwei Kernpunkte. Erstens ohne Kompilieren: Der AWUS036AXML läuft über den in kernel 6.17 enthaltenen `mt7921u`-Treiber, wird direkt nach dem Einstecken erkannt und erfordert auf aarch64 keinerlei Out-of-Tree-DKMS-Modul – das ist auf der ARM64-Plattform besonders bequem. Zweitens wird er per USB 3 aufgezählt (bei einigen Modellen der Vorgängergeneration hatte das OTG-Kabel nur USB 2.0), die Übertragungsbandbreite ist kein Flaschenhals.

Ein oft missverstandener Punkt zur Ergänzung: Der AWUS036AXML ist als Wi-Fi-6- (nicht 6E-)Chip positioniert, aber **auf dieser Maschine war das 6-GHz-Band im Test nutzbar** – wir setzten selbst einen AP auf 6135 MHz auf, das iPhone 15 Pro verband sich mit 802.11ax und erhielt eine IP. Auch Bluetooth war im Test nutzbar: `hciconfig` / `bluetoothctl` zeigten den hci-Controller im Zustand UP, BLE- und klassische Bluetooth-Geräte waren scannbar, Wi-Fi und Bluetooth laufen gleichzeitig (Koexistenz).

Prüft man noch die unterstützten Schnittstellenmodi, zeigt sich ein für die Auswahl bedeutsames Detail: Es gibt weder IBSS noch mesh point:

```bash
iw phy <phyN> info | sed -n '/Supported interface modes/,/Band 1/p'
```
```
Supported interface modes:
    * managed
    * AP
    * AP/VLAN
    * monitor
    * P2P-client / P2P-GO / P2P-device
```

Das heißt: managed, AP, monitor und P2P sind vorhanden, doch die beiden Modi ad-hoc (IBSS) und 802.11s mesh bietet der `mt7921u`-Treiber schlicht nicht. Kunden, die Mesh- / IBSS-Experimente machen wollen, schließen diese Karte direkt aus (und schauen auf den `mt76`-basierten ACM / ACHM).

## 3. Getestete Fähigkeiten: Monitor / AP / WPA3 und die ehrliche Grenze der Injektion

Die Kernfähigkeiten auf einen Blick:

| Fähigkeit | 2,4GHz | 5GHz | Erläuterung |
|---|---|---|---|
| Monitor | ✅ (schwach) | ✅ (schwach) | Beacons mitschneidbar; Client- / Data-Pakete gehen häufig verloren |
| **Injection** | ❌ **fehlgeschlagen** | ❌ **fehlgeschlagen** | `aireplay-ng` Injektion / deauth nicht funktionsfähig; Ursache: mac80211-chanctx-Regression im kernel 6.16+ (nicht chipbedingt) |
| AP-Hotspot | ✅ inkl. 802.11n | ✅ VHT80 (80MHz) | iPhone 7 Plus verbunden, `authorized: yes` |
| WPA3-SAE | ✅ | Nicht getestet | iPhone 15 Pro verbunden, `MFP: yes` (`sae_pwe=0`); zusätzlich auf 6 GHz getestet (ch37, 6135 MHz) |

### Monitor: beide Bänder kommen rein, aber der Empfang ist schwach

Der AWUS036AXML kann in 2,4GHz (ch1 / 6 / 11) und 5GHz (ch36 / 149 / 157) in den Monitor-Modus wechseln, das Mitschneiden von Beacons ist kein Problem. Der Einrichtungsablauf ist der standardmäßige `iw dev`-Vierschritt:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36     # für 2.4GHz stattdessen set channel 6
```

Ehrlich gesagt: Der Monitor-Empfang ist deutlich schwächer als beim MT7612U (ACM) derselben Charge oder beim Wi-Fi-6-AXER. Beacons werden erfasst, doch Client- / Data-Pakete gehen häufig verloren; beim Frequenzsprung-Scan mit `airodump-ng` werden leicht einige APs übersehen. In der Praxis empfiehlt sich, einen einzelnen Kanal zu fixieren (`-c <ch>`) statt zu springen, dann wird die Ausbeute stabiler. Außerdem meldet `iw info` im Monitor-Modus eine txpower von nur 3 dBm; das ist ein **Meldeartefakt** (die Hardware sendet tatsächlich mit etwa 20–23 dBm, per `txpower_sku` verifiziert) und nicht etwa eine echte Drosselung auf 3 dBm – darauf geht der spätere Abschnitt „Hinweise“ nochmals ein.

### AP-Hotspot: 2,4GHz inkl. HT, 5GHz schafft VHT80

AP ist der stabilste Teil des AWUS036AXML. In 2,4GHz lässt sich 802.11n (HT) direkt beibehalten, man muss nicht wie beim einantennigen ACHM das HT abschalten; in 5GHz lässt sich bis VHT 80MHz öffnen. In beiden Bändern verband sich im Test das iPhone 7 Plus, `authorized: yes`.

Die zentrale hostapd-Konfiguration für 5GHz VHT80:

```
hw_mode=a
channel=36
ieee80211ac=1
ht_capab=[HT40+][SHORT-GI-20][SHORT-GI-40]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42
vht_capab=[SHORT-GI-80]
```

Nach dem Verbinden war es im Test VHT-NSS2, 80MHz. Für die 2,4GHz-Variante `hw_mode` auf `g` und `channel=6` umstellen, `ieee80211n=1` und `ht_capab=[HT20]` beibehalten; das iPhone verband sich mit MCS 10 (802.11n).

### WPA3-SAE: nutzbar, denken Sie an sae_pwe=0

`wpa_key_mgmt` des AP auf `SAE` umstellen, `ieee80211w=2` und `sae_pwe=0` ergänzen, dann lässt sich WPA3-SAE aktivieren. Im Test verband sich das iPhone 15 Pro auf 2,4 GHz (und auf 6 GHz; 5 GHz nicht getestet), `authorized: yes`, `MFP: yes`. `sae_pwe=0` dient der Kompatibilität mit älteren iPhones – derselbe Fallstrick wie beim ACHM; bei `sae_pwe=2` können sich ältere Geräte oft nicht verbinden.

### VIF: einerseits online, andererseits Hotspot, machbar

Der AWUS036AXML unterstützt den Parallelbetrieb mehrerer Schnittstellen. Ein AP-VIF (andere MAC, unmanage) aufbauen, die Hauptschnittstelle mit dem WLAN verbinden, den AP auf demselben Kanal öffnen – im Test lag beim Verbinden des iPhone 7 Plus mit dem AP-VIF der ping der STA zu `YUPITEK` bei 4,4 ms. Für den Bedarf „mit einer Karte zugleich online gehen + einen Hotspot teilen“ ist das gegeben.

### Ehrliche Grenze: Die Injektion schlägt auf dieser Plattform fehl

Das ist der am klarsten darzulegende Punkt des AWUS036AXML (und seines bluetoothlosen Zwillings AXM). Auf dem ASUS GX10 + kernel 6.17 führten wir in unserer eigenen Testumgebung einen Injection-Selbsttest durch, das Ergebnis war ein Fehlschlag:

```bash
sudo aireplay-ng --test $IF
```
```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

Selbst beim AP-weisen Test mit der BSSID des eigenen AP kommt nur `No such BSSID available` zurück. Der springende Punkt: Ein normaler Scan sieht den AP durchaus (Signal -54 dBm), doch sobald es in den Kontext der Injektionswerkzeuge geht, „hört“ diese Karte das Beacon des Ziels nicht, der deauth lässt sich nicht senden, und die Zahl der erfassten 4-Way-Handshakes ist 0.

Das ist kein falsch eingestellter Parameter und kein Defekt einer einzelnen Karte. Die wahre Ursache liegt auf der **Softwareebene**: Seit kernel 6.16 tritt im channel context (chanctx) von mac80211 eine Regression auf, durch die der Stock-Treiber im Injektionsszenario die Ziel-Beacons nicht empfängt, worauf `aireplay-ng` auf `No Answer` erkennt – es ist **keine prinzipielle Injektionsunfähigkeit des MT7921-Chips**. Das Phänomen ist in morrownr/USB-WiFi issue #387 dokumentiert, die Ursachenanalyse in morrownr/mt76 issue #18. Community-Tests zeigen, dass sich am selben Modell mit einem git- / gepatchten Treiber active monitor plus Injektion zum Laufen bringen lässt, doch die MT7921-Firmware sperrt die Injektion weiterhin auf die Basisraten 1 Mbps / 6 Mbps und erlaubt keine Injektion mit HT- / VHT-Raten; AXM und AXML sind auf **stock kernel 6.17** gleichermaßen betroffen und mit Stand 2026-11-18 nicht durch Parameteränderung lösbar.

Daher kann der AWUS036AXML alles, was Injection voraussetzt – wie deauth, WPA-Handshake-Erfassung, auf Injektion beruhende Penetrationstests – auf dieser Plattform nicht leisten. Für solche Einsatzzwecke verwenden Sie ein Modell mit im Test nutzbarer Injektion (siehe Auswahl unten).

### Übersicht der weiteren erweiterten Modi

| Erweiterte Funktion | Status | Erläuterung |
|---|---|---|
| VIF (STA + AP parallel) | ✅ | gleicher Kanal ch36; beim iPhone-Verbinden STA ping 4,4 ms |
| WPA-Handshake-Erfassung | ❌ | Injektion fehlgeschlagen → deauth nicht sendbar, handshake 0 |
| Active monitor | 🟡 | `set monitor active` wird akzeptiert, ACK nicht verifiziert |
| Ad-hoc (IBSS) | N/A | `mt7921u`-Treiber bietet diesen Modus nicht |
| Mesh (802.11s) | N/A | `mt7921u`-Treiber bietet diesen Modus nicht |
| Wi-Fi Direct (P2P) | ⬜ | Treiber deklariert Unterstützung, zweites Gerät erforderlich, übersprungen |

## 4. Hinweise zur Bluetooth-Kombikarte und geeignete / ungeeignete Einsatzzwecke

### Praktische Nebenwirkungen der BT-+-WiFi-Kombikarte

Der AWUS036AXML enthält Bluetooth und ist eines der beiden Kombigeräte dieser Charge (das andere ist Realteks EACS). Bluetooth wurde auf dieser Maschine bereits als nutzbar getestet (hci-Controller UP, BLE- und klassische Bluetooth-Geräte scannbar, Koexistenz mit Wi-Fi, siehe oben); hier ergänzend eine praktische Nebenwirkung des Kombigeräts: Beim erneuten Einstecken bleibt es gelegentlich beim WiFi-probe hängen und erzeugt keine `wlx`-Schnittstelle; das Symptom ist, dass `ls /sys/class/net` nach dem Ein-/Ausstecken lange keine Karte zeigt. Die Lösung ist einfach: **an einem anderen USB-Port** erneut einstecken, dann wird in der Regel normal aufgezählt.

Noch ein kleiner Handgriff zum Merken: Wenn das Telefon im AP-Modus Ihre SSID plötzlich nicht mehr findet, genügt es, die Karte **einmal aus- und wieder einzustecken**, keine Konfigurationsänderung nötig. (Hinweis: Die zuvor erwähnten im Monitor-Modus gemeldeten 3 dBm sind ein Artefakt, nicht die reale Leistung, und nicht die Hauptursache für das Verschwinden der SSID.)

### Plattform-Sicherheitsregeln

- Führen Sie auf keinen Fall `airmon-ng check kill` aus: Es schaltet den NetworkManager ab und trennt den gesamten GX10 vom Netz. Bedienen Sie beim Arbeiten nur die externe `wlx*`-Schnittstelle und fassen Sie die interne Uplink-Hauptleitung nicht an.
- `hcxdumptool 8.x` meldet auf dieser Maschine `failed to arm` (außer AWUS036EACS auf 2,4 GHz) (Aufzählungskonflikt der internen Tri-Band-Karte des GX10 + Treiber ohne active-monitor); das ist ein plattformweites Problem und hat nichts mit dem AXML zu tun; bei Bedarf einer ähnlichen Funktion `airodump-ng` mit anderen aircrack-ng-Werkzeugen verwenden.
- ARM64-Ergänzung: `aircrack-ng` muss aus dem Quellcode kompiliert werden, für `wifite` empfiehlt sich die git-Version, um apt-Abhängigkeitskonflikte zu umgehen.

### Übersicht geeignet / ungeeignet

| Geeignetes Szenario | Ungeeignetes Szenario |
|---|---|
| reiner AP / Hotspot (2,4G inkl. HT, 5G VHT80) | injection / deauth |
| WPA3-SAE-Hotspot | WPA-Handshake-Erfassung |
| normale managed-Verbindung | Haupt-Penetrationstestkarte mit Injektion als Voraussetzung |
| passiver Monitor / Spektrum-Bestandsaufnahme (einzelnen Kanal fixieren) | mesh / IBSS Experiment |
| STA + AP parallel (VIF, einerseits online, andererseits teilen) | weitreichendes Mitschneiden mit starkem Empfang |

## 5. Auswahlempfehlung (zurück zur Gesamttabelle)

Stellt man den AWUS036AXML in das Gesamtbild der 9 Karten, ist seine Positionierung klar: MediaTek stabil in der Verbindung, ohne Kompilieren, in beiden Bändern AP bis VHT80 – eine tüchtige „reine Verbindungs- / reine AP“-Karte; sobald Injection ins Spiel kommt, ist das nicht sein Metier.

| Bedarf | Empfohlenes Modell |
|---|---|
| reiner AP / normale Verbindung (ohne Injektion) | **AWUS036AXML / AWUS036AXM** (diese Karte geeignet) |
| injection + handshake (Penetrationstest) | AWUS036EACS / AWUS036ACH / AWUS036ACS |
| mesh / IBSS Experiment | AWUS036ACM / AWUS036ACHM |
| stärkster Empfang / Monitor über große Distanz | AWUS036AXER / AWUS036ACH |

Wenn Sie zwischen den 9 Karten abwägen, finden Sie die vollständige Matrix aus Monitor / Injection / AP / WPA3 und die zweckabhängige Auswahl in der Gesamttabelle:

- [Vollständigster Praxistest 2026: 9 ALFA-WLAN-Karten auf ASUS GX10 in der Gesamtmatrix](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

Eine Warnung in einem Satz: **Für Injection oder Handshake wählen Sie nicht den AWUS036AXML / AWUS036AXM**; für reine Verbindung oder Hotspot-Aufbau ist er sehr brauchbar.

## Häufig gestellte Fragen (FAQ)

**F1. Kann der AWUS036AXML Paket-Injektion (packet injection) durchführen?**
Auf unserer Testplattform (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia) nicht. `aireplay-ng --test` meldet `No Answer`, `Found 0 APs`; der AP-weise Einzeltest ergibt nur `No such BSSID available`. Selbst wenn ein normaler Scan den AP sieht (etwa -54 dBm), empfängt die Karte im Kontext der Injektionswerkzeuge dessen Beacon nicht, sodass deauth und Handshake-Erfassung (0 Stück) beide nicht nutzbar sind. Die Ursache ist eine mac80211-chanctx-Regression im kernel 6.16+, nicht eine prinzipielle Injektionsunfähigkeit des Chips; der AWUS036AXM liefert dasselbe Ergebnis. Wer Injektion braucht, wählt stattdessen AWUS036EACS, ACH oder ACS.

**F2. Funktioniert das Bluetooth des AWUS036AXML unter Ubuntu?**
Im Test auf dieser Maschine ist Bluetooth nutzbar: mit `bluetoothctl` / `hciconfig` bestätigt, dass der hci-Controller UP ist, BLE- und klassische Bluetooth-Geräte gescannt werden können und Wi-Fi und Bluetooth gleichzeitig nutzbar sind (Koexistenz). Es ist ein Wi-Fi-+-Bluetooth-Kombigerät; Hinweis: Beim erneuten Einstecken bleibt es gelegentlich beim WiFi-probe hängen und erzeugt keine `wlx`-Schnittstelle – an einem anderen USB-Port erneut einstecken stellt es wieder her.

**F3. Muss man für den AWUS036AXML unter Ubuntu 24.04 einen Treiber nachinstallieren?**
Nein. Der mt7921u-Treiber ist in kernel 6.17 enthalten, nach dem Einstecken sieht man in dmesg, wie mt7921u die Schnittstelle in `wlx` plus MAC umbenennt (USB ID `0e8d:7961`), ohne DKMS, ohne Kompilieren. Der Treiber bietet keinen IBSS- und keinen Mesh-Modus.

**F4. Kann der AWUS036AXML einen AP öffnen und WPA3 unterstützen?**
Ja, das ist seine stabilste Anwendung. In 2,4 GHz (802.11n, MCS 10) und 5 GHz VHT80 (VHT-NSS2) konnte sich jeweils ein iPhone verbinden und wurde authorized; WPA3-SAE verbindet das iPhone 15 Pro mit `sae_pwe=0` (`MFP: yes`; getestet auf 2,4 GHz und 6 GHz, nicht auf 5 GHz); bei STA+AP parallel liegt der ping der STA-Seite bei etwa 4,4 ms. Obwohl als Wi-Fi-6-Chip positioniert, war auf dieser Maschine zusätzlich das 6-GHz-Band nutzbar (selbst aufgesetzter 6135-MHz-AP, iPhone 15 Pro verband sich mit 802.11ax und erhielt eine IP).

**F5. Worin unterscheiden sich AWUS036AXML und AWUS036AXM, welche sollte man wählen?**
Auf dieser Plattform ist das Wi-Fi-Verhalten beider gleich: beide nutzen mt7921u, die Injektion schlägt gleichermaßen fehl, der Monitor-Empfang ist gleichermaßen schwach, AP, WPA3 und VIF sind gleichermaßen nutzbar. Der Unterschied: Der AXML hat zusätzlich Bluetooth (auf dieser Maschine im Test nutzbar) und auf dieser Maschine war das 6-GHz-Band nutzbar, während Bluetooth und 6 GHz des AXM in dieser Runde nicht gesondert getestet wurden. Für reinen AP oder normale Verbindung kann man beide wählen; für Injektion oder Handshake sollte man keine von beiden wählen.

## Weiterführende Literatur

(Links gehen nach und nach online, in Arbeit)

- Bluetoothlose Variante mit gleichem Chip: [AWUS036AXM im Einzelkartentest](/de/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- Alternativen mit nutzbarer Injektion: [AWUS036EACS im Einzelkartentest](/de/blog/awus036eacs-asus-gx10-ubuntu-test-report/), [AWUS036ACH im Einzelkartentest](/de/blog/awus036ach-asus-gx10-ubuntu-test-report/), [AWUS036ACS im Einzelkartentest](/de/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- Themenartikel: [Ohne Treiberinstallation: Monitor- und AP-Modus unter Ubuntu (ARM64) aktivieren](/de/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- Themenartikel: [WPA3-SAE-Verbindung und Handshake-Praxis (in eigener Umgebung verifiziert)](/de/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Gesamttabellen-Hub: [9 ALFA-Karten auf ASUS GX10 in der Gesamtmatrix](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

---

*Testinstanz: Yupitek (ALFA-Network-Distributor Taiwan) | Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Testgerät: Apple iPhone 7 Plus (WPA3 zusätzlich iPhone 15 Pro) | Testumgebung: eigenes Büro-WLAN (SSID YUPITEK). Dieser Artikel dient der Verifikation von Produktkompatibilität und -fähigkeit, keine Bedienanleitung gegen fremde Netzwerke.*
