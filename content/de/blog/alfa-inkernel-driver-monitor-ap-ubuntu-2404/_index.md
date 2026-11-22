---
title: "Ohne Treiberinstallation: ALFA-Karten-Monitor- und AP-Modus unter Ubuntu 24.04 + kernel 6.17 mit in-kernel-Treibern aktivieren (rtw88 / rtw89 / mt76 im Praxistest)"
slug: alfa-inkernel-driver-monitor-ap-ubuntu-2404
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404.webp"
bannerimage: "/images/blog/banner/alfa-inkernel-driver-monitor-ap-ubuntu-2404.webp"
author: "benny-lai"
tags:
  - alfa-network
  - ubuntu-24-04
  - kernel-6-17
  - in-kernel-driver
  - rtw88
  - rtw89
  - mt76
  - monitor-mode
  - hostapd
  - ap-mode
  - linux-wifi
description: "Anleitung für Ubuntu 24.04 / kernel 6.17 ohne Treiberinstallation: Monitor- und AP-Modus von ALFA-Karten mit den in-kernel-Treibern rtw88 / rtw89 / mt76 aktivieren, inklusive WPA3-Hotspot-Kompatibilitätseinstellungen und Hinweisen zur Kali-Toolchain."
faq:
  - question: "Wie bringt man unter Ubuntu 24.04 eine ALFA-Karte in den Monitor-Modus?"
    answer: "Ab kernel 6.17 genügt es, die Schnittstelle der Verwaltung durch den NetworkManager zu übergeben und in den monitor-Schnittstellenmodus zu wechseln, ohne einen Drittanbietertreiber zu installieren; der Ablauf ist bei den drei in diesem Artikel getesteten Treiberfamilien rtw88 / rtw89 / mt76 gleich, die ausführlichen Befehle finden Sie in den Schritten im Text."
  - question: "Warum benötigt eine ALFA-Karte unter Ubuntu keinen zusätzlichen Treiber?"
    answer: "Weil Realtek rtw88/rtw89 und MediaTek mt76 diese USB-Chips nach und nach in die in-kernel-Unterstützung des Mainline-Kernels aufgenommen haben (die Mindestversion unterscheidet sich je Karte, von 4.19 bis 6.17; unter Ubuntu 24.04 benötigen AX und AXER Kernel 6.17 oder höher, z. B. den HWE-Kernel von 24.04.4); mit kernel 6.17 (auf dem GX10 getestet) sind alle 9 Karten dieses Artikels integriert, direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS."
  - question: "Was tun, wenn sich ein älteres iPhone nicht mit einem mit einer ALFA-Karte aufgebauten WPA3-Hotspot verbindet?"
    answer: "Im Test zeigten sich zwei häufige Ursachen: Erstens muss die hostapd-Option sae_pwe auf 0 statt 2 gesetzt werden, um mit älteren iPhones kompatibel zu sein; zweitens kann das Beibehalten der 802.11n-Einstellung bei älteren Geräten die Assoziation scheitern lassen – wenn Kompatibilität Vorrang hat, empfiehlt sich, 802.11n abzuschalten."
  - question: "Welche der Treiberfamilien rtw88, rtw89, mt76 unterstützt Mesh oder IBSS?"
    answer: "Im Test kann die mt76-Familie (wie AWUS036ACM / ACHM) im Einzelbetrieb Mesh (802.11s) und IBSS aufbauen; Realtek rtw88 kann IBSS im Einzelbetrieb joinen (maßgeblich am ACH getestet), unterstützt aber kein Mesh; rtw89 deklariert nicht einmal IBSS-Unterstützung."
draft: false
---

> Dieser Artikel ist eine standardmäßige Linux-Netzwerkkonfigurationsanleitung und zeigt, wie Sie unter einem aktuellen Kernel mit dem **integrierten (in-kernel) Treiber** den Monitor- (Mithör-) und AP- (Hotspot-)Modus einer ALFA-WLAN-Karte aktivieren.
> Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Alle Werte sind Auszüge aus Yopiteks Produktkompatibilitätstests auf eigener Hardware, im eigenen Büro-WLAN (SSID `YUPITEK`).
> ⚠️ **Rechtmäßige Nutzung**: Der Monitor-Modus dient ausschließlich dem Mithören in Netzwerken, die Ihnen gehören oder für die Sie eine Genehmigung haben; im AP-Modus halten Sie bitte die lokalen Funkvorschriften ein. Dieser Artikel umfasst keinerlei Angriffsoperationen gegen fremde Netzwerke.

---

## Kernaussagen (TL;DR)

Auf dem ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17) laufen alle 9 von Yopitek (ALFA-Network-Distributor Taiwan) getesteten ALFA-USB-WLAN-Adapter mit in-kernel-Treibern (`rtw88` / `rtw89` / `mt76`) ohne Treiberinstallation, aktivieren Monitor- und AP-Modus mit demselben Ablauf und lassen iPhone 7 Plus / 15 Pro im 2,4G- und 5G-AP normal verbinden; der Mindest-Kernel liegt je nach Karte zwischen 4.19 und 6.17.

- **Auf aktuellen Kerneln ohne Treiberinstallation**: Realtek `rtw88` / `rtw89` und MediaTek `mt76` haben diese ALFA-USB-Chips in die in-kernel-Unterstützung aufgenommen; mit kernel 6.17 (auf dem GX10 getestet) sind alle 9 Karten integriert, die Mindestversion unterscheidet sich je Karte, direkt nach dem Einstecken einsatzbereit, ohne Kompilieren, ohne DKMS.
- **Monitor- und AP-Ablauf bei allen drei Familien gleich**: an den NetworkManager zurückgeben → mit `iw` auf monitor schalten / mit `hostapd` AP starten.
- **Zwei Kompatibilitätsfallen**: Beim Öffnen eines AP empfiehlt sich, 802.11n abzuschalten (`ieee80211n=0`), und für WPA3-SAE `sae_pwe=0` zu verwenden, sonst kann sich ein älteres iPhone nicht verbinden.
- **Abstufung der erweiterten Modi**: Mesh nur bei `mt76`; IBSS im Einzelbetrieb bei `mt76` und `rtw88` (ACH) joinbar, `rtw89` nicht deklariert.
- **Eiserne Plattformregel**: Niemals `airmon-ng check kill` ausführen (trennt den GX10 vom Netz), nur die externe `wlx*`-Schnittstelle bedienen.

## 1. Warum „ohne Treiberinstallation“ das Kernthema dieser Generation ist

Früher war beim Einsatz von USB-WLAN-Karten wie denen von ALFA unter Linux die häufigste Hürde der Treiber. Chips wie RTL8812AU oder MT7610U schafften es jahrelang nicht in den Mainline-Kernel, Nutzer mussten Out-of-Tree-Projekte von GitHub holen (etwa `morrownr/USB-WiFi`, `aircrack-ng/rtl8812au`) und sie dann über DKMS an die aktuelle Kernel-Version gebunden kompilieren. Bei jedem Kernel-Update musste DKMS neu kompilieren; schlug das Kompilieren einmal fehl, verschwand die Karte schlicht. Für Distributor-Verifikationen oder Lehrumgebungen, die einen stabilen Betrieb brauchen, war das ein langanhaltender Schmerzpunkt.

Mit den neueren Mainline-Kerneln kam die Wende: Die drei großen Treiberfamilien Realtek `rtw88`, `rtw89` und MediaTek `mt76` nahmen diese USB-Chips nach und nach offiziell in die in-kernel-Unterstützung auf. Die Mindestversion unterscheidet sich je Karte (siehe Spalte "Min. Kernel" unten); mit kernel 6.17 (auf dem GX10 getestet) sind alle neun in diesem Artikel getesteten Karten integriert, **direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS**. Noch wichtiger: Die ursprünglich beiden meistgenutzten Out-of-Tree-Projekte (die rtl8812au von morrownr und aircrack-ng) verweisen inzwischen beide auf diesen integrierten Treiber, und auch Bug-Reports laufen einheitlich zu `lwfinger/rtw88` zurück. Mit anderen Worten: Der Schritt des manuellen Treiberkompilierens lässt sich auf neuen Kerneln direkt weglassen.

Die Community `lwfinger/rtw88` wird weiterhin aktiv gepflegt und schickt Korrekturen laufend nach oben; die Stabilität des integrierten Treibers aktualisiert sich dadurch zusammen mit dem Kernel, sodass Nutzer keine eigenen Branches mehr pflegen müssen und auch nicht bei jedem Upgrade an einem DKMS-Kompilierfehler hängenbleiben. Für Distributor-Verifikationen und Lehrumgebungen lässt sich derselbe Bedienungsablauf über mehrere Karten und mehrere Kernel-Updates hinweg wiederverwenden, die Wartungskosten sinken spürbar – auch das ist der Grund, warum dieser Artikel den Schwerpunkt auf „ohne Treiberinstallation“ legt.

Die in diesem Artikel getesteten Chips und die zugehörigen integrierten Treibermodule sind wie folgt:

| Chip-Familie | Chip-Modell | integriertes Treibermodul | Min. Kernel | Generation / Streams | Beispielkarte |
|---|---|---|---|---|---|
| **MediaTek mt76** | MT7612U | `mt76x2u` | 4.19 | Wi-Fi 5 / 2T2R | AWUS036ACM |
| **MediaTek mt76** | MT7610U | `mt76x0u` | 4.19 | Wi-Fi 5 / 1T1R | AWUS036ACHM |
| **MediaTek mt76** | MT7921AUN | `mt7921u` | 5.18 | Wi-Fi 6 / 2x2 | AWUS036AXM / AXML |
| **Realtek rtw88** | RTL8812AU | `rtw88_8812au` | 6.13 | Wi-Fi 5 / 2T2R | AWUS036ACH |
| **Realtek rtw88** | RTL8811AU | `rtw88_8821au` | 6.13 | Wi-Fi 5 / 1x1 | AWUS036ACS |
| **Realtek rtw88** | RTL8821CU | `rtw88_8821cu` | 6.2 | Wi-Fi 5 / 1x1 (+BT) | AWUS036EACS |
| **Realtek rtw89** | RTL8832BU | `rtw89_8852bu` | 6.17 | Wi-Fi 6 / 2x2 | AWUS036AX / AXER |

> Nur wenn der Kernel Ihres Systems unter der Mindestversion Ihrer Karte liegt (siehe Tabelle oben), müssen Sie den alten Weg gehen: einen Out-of-Tree-Treiber per DKMS installieren (für die rtw88-Karten `lwfinger/rtw88`). Beispiel Ubuntu 24.04: Der GA-Kernel 6.8 enthält bereits die Treiber für ACM, ACHM, AXM, AXML und EACS; HWE 6.14 ergänzt ACH und ACS. AX und AXER benötigen Kernel 6.17 oder höher (z. B. den HWE-Kernel von 24.04.4). Dieser Artikel basiert auf dem kernel 6.17 des GX10.

---

## 2. Bestätigen, dass der Treiber geladen und gebunden ist

Bevor Sie in irgendeinen Modus wechseln, bestätigen Sie zuerst, dass die Karte korrekt erkannt, der Treiber gebunden und der Schnittstellenname entstanden ist. Am Beispiel des Realtek AWUS036ACH (`rtw88_8812au`) folgen vier Prüfschritte.

**Schritt eins: Bestätigen, dass das USB-Gerät aufgezählt wurde.** Mit `lsusb` die USB-ID finden (Realtek meist `0bda:xxxx`, MediaTek meist `0e8d:xxxx`):

```bash
lsusb | grep 0bda:8812
# Bus 004 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

**Schritt zwei: Treiberbindung und USB-Rate bestätigen.** `lsusb -t` zeigt zugleich den gebundenen Treiber und die Verbindungsgeschwindigkeit (`5000M` bedeutet USB 3.0):

```bash
lsusb -t | grep rtw88_8812au
# |__ Port 001: Dev 002, If 0, Class=Vendor Specific Class, Driver=rtw88_8812au, 5000M
```

Bei MediaTek-Karten lässt sich stattdessen mit `dmesg` die Treiberinitialisierung beobachten und zugleich die Schnittstellenumbenennung bestätigen:

```bash
sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0
```

**Schritt drei: Den Schnittstellennamen ermitteln.** Ubuntu verwendet vorhersagbare Benennung (predictable naming), eine externe ALFA-Karte ist stets `wlx` plus MAC-Adresse. Dieser Name wird durch die MAC bestimmt und **ändert sich nach dem erneuten Ein- und Ausstecken nicht**, was die Skriptbarkeit erleichtert. Die interne Uplink-Karte trägt einen anderen Namen (am GX10 `wlP9s9`), unbedingt klar unterscheiden:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cabca7f5
```

**Schritt vier: Die vom Chip deklarierten unterstützten Schnittstellenmodi abfragen.** Dieser Schritt bestimmt, welche Modi später nutzbar sind:

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Realtek rtw88 (ACH) listet `IBSS / managed / AP / AP/VLAN / monitor`, aber **kein** Mesh und P2P; MediaTek mt76 (ACHM) listet zusätzlich `mesh point / P2P-client / P2P-GO`. Diese Liste ist die Primärquelle für die Fähigkeitsunterschiede zwischen den Familien, siehe Abschnitt 5.

---

## 3. Monitor-Modus aktivieren (2,4 GHz / 5 GHz)

Der Monitor- (Mithör-)Modus lässt die Karte sich mit keinem AP assoziieren und direkt die 802.11-Frames aus der Luft empfangen – häufig genutzt für Paketdiagnose, Spektrumsinspektion und Signalabdeckungsbewertung im eigenen Netz. Der Aktivierungsablauf ist bei allen drei Familien gleich, der Unterschied liegt nur in den familienspezifischen Stabilitätshinweisen (siehe Abschnitte 5 und 6).

**Allgemeine Aktivierungsschritte:**

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no      # an uns selbst zurückgeben, um Eingriffe des NetworkManager zu vermeiden
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
iw dev $IF info | grep type
# type monitor
```

`type monitor` zu sehen bedeutet, dass der Wechsel erfolgreich war. Geben Sie anschließend den zu überwachenden Kanal an. **2,4 GHz** mit `set channel`:

```bash
sudo iw dev $IF set channel 6
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch6.pcap
tcpdump -r /tmp/mon-ch6.pcap | wc -l
```

**5 GHz** über die Frequenzangabe ist weniger fehleranfällig (ch36 = 5180 MHz):

```bash
sudo iw dev $IF set freq 5180
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch36.pcap
tcpdump -r /tmp/mon-ch36.pcap | wc -l
```

**Erwartetes Ergebnis (Auszug aus dem Praxistest):** Der AWUS036ACH erfasste auf ch1 / ch6 / ch11 jeweils 92 / 214 / 71 Frames; in 5 GHz auf ch36 / ch149 / ch157 jeweils 260 / 137 / 127 Frames, was bedeutet, dass das Mithören in 2,4G und 5G normal funktioniert. Der MediaTek ACHM fand mit `airodump-ng --band abg` bei einem 120-Sekunden-Frequenzsprung-Scan im Bereich ch1/5/6/36/149/157 19 Basisstationen und 14 Clients. Dass auf einem Kanal 0 Pakete erfasst werden, bedeutet meist nur, dass auf diesem Kanal gerade kein AP ist, nicht einen Kartendefekt.

Nach dem Wechsel in den Monitor-Modus laufen die gängigen Standard-Diagnosewerkzeuge direkt auf der `wlx*`-Schnittstelle: `airmon-ng` listet Karten- und Treiberstatus auf, `kismet` kann als Datenquelle in Echtzeit mithören und ein `.kismet`-Log erzeugen, `Wireshark` und `tshark` analysieren die erfassten Pakete, `bettercap` kann eine Kanalinspektion durchführen. Diese Werkzeuge waren im Test bei allen drei Familien nutzbar und eignen sich gut, um die Kanalnutzung und Signalabdeckung der eigenen Funkumgebung zu erfassen. Das Einzige, worauf zu achten ist: `hcxdumptool` 8.x meldet auf dieser Plattform bei allen drei Familien außer dem EACS auf 2,4 GHz `failed to arm` (der integrierte Treiber stellt kein active-monitor bereit); wird eine ähnliche Funktion benötigt, verwenden Sie stattdessen `airodump-ng` zusammen mit der aircrack-ng-Suite.

> **5-GHz-Hinweis:** Unter der Standard-regdomain (`country 00`) sind viele 5-GHz-Kanäle passive/no-IR, Mithören ist möglich, aber aktives Senden ist eingeschränkt. Wenn Sie anschließend 5-GHz-Tests im autorisierten Rahmen durchführen wollen, zuerst mit `sudo iw reg set US` entsperren und nach dem Test mit `sudo iw reg set TW` zurücksetzen. Der Realtek `rtw88_8812au` hat zudem ein bekanntes 5G-RX-stuck-Phänomen (nach wiederholtem Moduswechsel empfängt 5G keine Pakete mehr); tritt es auf, die Karte einmal physisch aus- und einstecken und dann 5G vorrangig durchführen.

---

## 4. AP- / Hotspot-Modus aktivieren (2,4 GHz / 5 GHz)

Der AP- (Hotspot-)Modus macht die Karte mit `hostapd` zu einer Wi-Fi-Basisstation. Der Ablauf ist bei allen drei Familien gleich: zuerst die Schnittstelle dem NetworkManager übergeben, dann mit einer `hostapd`-Konfigurationsdatei starten. Im Folgenden die allgemeine Minimalkonfiguration.

**4-1. 2,4 GHz (reines 802.11g)**

Konfigurationsdatei `/tmp/ap24.conf` anlegen:

```ini
interface=wlx00c0cabca7f5
driver=nl80211
ssid=ALFA-AP-24G
hw_mode=g
channel=6
country_code=TW
auth_algs=1
ieee80211n=0
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=<Ihr Passwort, mindestens 8 Zeichen>
```

Starten:

```bash
sudo nmcli dev set $IF managed no
sudo hostapd /tmp/ap24.conf
```

Wenn sich ein Client verbindet, gibt `hostapd` der Reihe nach `authenticated` → `associated` → `AP-STA-CONNECTED` → `EAPOL-4WAY-HS-COMPLETED` aus; die letzte Zeile zu sehen bedeutet, dass der Vier-Wege-Handshake abgeschlossen und die Verbindung erfolgreich ist.

**4-2. 5 GHz (reines 802.11a, ch36)**

Die obige Konfiguration auf 5 GHz ändern:

```ini
ssid=ALFA-AP-5G
hw_mode=a
channel=36
```

2x2-Karten (wie die rtw89-Karten AX/AXER, die mt76-Karten ACM/AXM) können zusätzlich eine VHT80-Einstellung ergänzen, um auf 80 MHz Bandbreite hochzuziehen; bei Einzelantenne oder wenn Kompatibilität gefragt ist, genügt reines a mit 20 MHz.

**4-3. Zwei entscheidende Kompatibilitätseinstellungen**

1. **Beim Öffnen eines AP empfiehlt sich, 802.11n abzuschalten** (`ieee80211n=0`, reines g / reines a). Im Test scheiterte die Assoziation älterer Clients (iPhone 7 Plus), wenn `ieee80211n=1` beibehalten wurde, und meldete fälschlich „falsches Passwort“; tatsächlich war es `handle_assoc_cb: STA not found`; nach Entfernen von 802.11n klappte die Verbindung gleich beim ersten Mal.
2. **Für WPA3-SAE bitte `sae_pwe=0` verwenden** (hunting-and-pecking). Mit `sae_pwe=2` (erzwungenes H2E) schlägt der Schlüssel-Handshake älterer Geräte fehl. Beispiel für den WPA3-Abschnitt:

```ini
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
ieee80211w=2
sae_pwe=0
```

Diese beiden Fallen treten bei Realtek- wie bei MediaTek-Karten gleichermaßen auf, es handelt sich um Client-Kompatibilität, nicht um einen Treiberunterschied. Die neun in diesem Artikel getesteten Karten ließen im 2,4G- und 5G-AP-Betrieb das iPhone 7 Plus / 15 Pro allesamt normal verbinden.

**4-4. Gleichzeitig online sein und Hotspot bereitstellen (STA + AP)**

Die mt76-Familie unterstützt es, mit einer Karte zugleich ein bestehendes Wi-Fi zu nutzen und zusätzlich einen AP-VIF als Relay-Hotspot aufzubauen. Im Test öffnete der ACHM, während die Hauptschnittstelle mit YUPITEK verbunden war, einen 5-GHz-Hotspot und ließ ein iPhone verbinden; der Download lag noch bei 198 Mbit/s, der Ping im Mittel bei 3,2 ms. Diese Kombination erfordert drei Bedingungen: Der AP-VIF muss eine andere MAC verwenden, der Schnittstellenname muss das `wlx`-Format behalten, und alle VIFs müssen auf demselben Kanal sein. Bei Realtek-Karten ist diese Kombination nicht per phy garantiert (bei rtw88 funktioniert zwar managed + monitor, doch STA + AP ist nicht stabil); für einen Relay-Hotspot empfiehlt sich vorrangig die mt76-Familie.

---

## 5. Unterschiede und Grenzen der drei Chip-Familien

Die grundlegenden drei Modi managed / monitor / AP unterstützen alle drei Familien, mit einheitlichem Verhalten. Der Unterschied liegt bei den **erweiterten Schnittstellenmodi** (Mesh, IBSS, active monitor, P2P): Das hängt allein von der Treiberdeklaration ab und nicht von der Antennenzahl der Karte. Im Folgenden die zusammengefasste Praxismessung.

| Erweiterter Modus | MediaTek mt76 | Realtek rtw88 | Realtek rtw89 |
|---|---|---|---|
| Monitor (2.4G/5G) | ✅ | ✅ | ✅ |
| AP (hostapd) | ✅ | ✅ | ✅ |
| Ad-hoc / IBSS (Einzelbetrieb) | 🟡 im Einzelbetrieb aufbaubar | 🟡 im Einzelbetrieb aufbaubar | ❌ Treiber nicht deklariert |
| Mesh (802.11s, Einzelbetrieb) | 🟡 im Einzelbetrieb aufbaubar | ❌ `-95` nicht unterstützt | ❌ Treiber nicht deklariert |
| Active monitor | 🟡 konfigurierbar | ❌ `-95` nicht unterstützt | N/A |
| Wi-Fi Direct (P2P) | zweites Gerät nötig | ❌ `-95` nicht unterstützt | N/A |

**MediaTek mt76 (ACM / ACHM / AXM / AXML)** ist die Familie mit den vollständigsten erweiterten Modi. `iw phy info` deklariert bereits `mesh point`, `IBSS`, `P2P-client/GO`. Im Test ließen sich im Einzelbetrieb `Joined IBSS`, `type mesh point` erreichen und die entsprechenden Beacons aussenden (der peer link mit einem zweiten Gerät blieb mangels zweitem Gerät unverifiziert). Wenn Ihr Zweck ein Mesh- oder IBSS-Einzelgerät-Experiment ist, ist die mt76-Familie erste Wahl. Besonders zu beachten: Der Wi-Fi-6-MT7921 (AXM/AXML) hat zwar vollständige Modi und einen stabilen AP, kann aber auf dieser Plattform keine Frame-Injection (Hauptursache ist die mac80211-chanctx-Regression im stock kernel 6.16+, nicht chip-bedingt; dieselben Modelle laufen in der Community mit git-/patched-Treibern, doch die Firmware sperrt die Datenrate, entsprechend morrownr/USB-WiFi #387, morrownr/mt76 #18) und eignet sich nicht für erweiterte Tests, die Injektion erfordern.

**Realtek rtw88 (ACH / ACS / EACS)** unterstützt `IBSS / managed / AP / AP/VLAN / monitor`. IBSS ist im Einzelbetrieb aufbaubar (`Joined IBSS`, maßgeblich am ACH getestet; der EACS listet zwar den iftype, doch der Join ist im Test wirkungslos), aber **Mesh (802.11s), active monitor und Wi-Fi Direct melden im Test allesamt `Operation not supported (-95)`**. Ein weiteres rtw88-spezifisches Merkmal ist VIF: Obwohl das `iw phy`-Flag „interface combinations are not supported“ schreibt, ließen sich am ACH im Test die beiden Schnittstellen managed + monitor gleichzeitig up setzen, der monitor-VIF erfasste 100 Frames, „online sein und zugleich mithören“ ist möglich; da diese Kombination jedoch per phy nicht garantiert ist, empfiehlt sich für langen Betrieb unter hoher Last weiterhin die mt76-Familie.

**Realtek rtw89 (AX / AXER)** ist die neueste Wi-Fi-6-Familie dieses Artikels, Monitor und AP (inkl. VHT80) zeigen gute Leistung und die Empfangsempfindlichkeit ist stark. Bei den erweiterten Modi sind active monitor / mesh / IBSS / P2P jedoch bereits auf Treiberebene nicht deklariert (N/A), weshalb Sie für diese Einzelgerät-Experimente auf mt76-Karten umsteigen sollten. Die Positionierung von rtw89 ist stabiles Wi-Fi-6-Mithören und -Hotspot, nicht eine Experimentierplattform für erweiterte Schnittstellenmodi.

> Auswahl in einem Satz: **Für Mesh / IBSS im Einzelbetrieb → mt76 (ACM / ACHM); für Wi-Fi-6-Hotspot und starken Empfang → rtw89 (AX / AXER); für Dual-Band-Universalität und VIF → rtw88 (ACH).**

---

## 6. Sicherheitshinweise zur Plattform (GX10 + Ubuntu ARM64)

Auf Maschinen wie dem GX10, bei denen „die interne Karte den Uplink übernimmt und die externe ALFA-Karte für Tests dient“, sind die folgenden Punkte eiserne Betriebsregeln; nur wer sie befolgt, trennt sich nicht selbst vom Netz.

1. **Führen Sie niemals `airmon-ng check kill` aus.** Dieser Befehl schaltet den NetworkManager ab und unterbricht damit auch die Außenverbindung des GX10. Dieser Artikel verwendet durchgehend nur `iw` und `nmcli dev set <Schnittstelle> managed no`, fasst `check kill` nicht an.
2. **Nur `wlx*` bedienen, niemals die interne `wlP9s9` anfassen.** `wlP9s9` ist die Uplink-Hauptleitung des GX10; jede down-/Moduswechsel-Aktion darf nur auf die `wlx*`-Schnittstelle der ALFA-Karte angewendet werden; vor einem Befehl unbedingt mit `echo $IF` das Ziel bestätigen.
3. **RX-Stall durch Aus- und Einstecken beheben.** Wird nach wiederholtem Wechsel zwischen monitor / AP nichts mehr gescannt, ist es meist ein Empfangs-Hänger des Treibers (bei Realtek 5G besonders häufig). Software kann das meist nicht retten, daher die Karte direkt **einmal physisch aus- und einstecken**; der USB wird neu aufgezählt, der Schnittstellenname bleibt dank unveränderter MAC konsistent.
4. **BT+WiFi-Kombikarte: USB-Port wechseln.** Bei Kombigeräten aus Bluetooth und Wi-Fi wie EACS, AXML bleibt beim erneuten Einstecken gelegentlich der WiFi-Probe hängen und es entsteht keine `wlx`-Schnittstelle; ein anderer USB-Port löst das meist.
5. **Vor dem 5-GHz-Senden regdomain setzen.** Unter dem Standard `country 00` sind viele 5-GHz-Kanäle no-IR und verbieten aktives Senden. Vor Tests im autorisierten Rahmen mit `sudo iw reg set US` entsperren, nach dem Test mit `sudo iw reg set TW` zurücksetzen.
6. **ARM64-Pakethinweise.** Der GX10 ist aarch64, `aircrack-ng` fehlt oft ein prebuilt wheel/package und muss aus dem Quellcode kompiliert werden; für `wifite` empfiehlt sich die GitHub-Version, um apt-Abhängigkeitskonflikte zu umgehen. Außerdem meldet `hcxdumptool` 8.x auf dieser Plattform bei allen drei Familien außer dem EACS auf 2,4 GHz `failed to arm` (der integrierte Treiber hat keine active-monitor-Unterstützung); für die Mithör-Erfassung bitte `airodump-ng` zusammen mit der aircrack-ng-Suite verwenden.

**Nach dem Test in den Normalmodus zurückkehren:**

```bash
sudo pkill hostapd 2>/dev/null
sudo ip link set $IF down
sudo iw dev $IF set type managed
sudo ip link set $IF up
sudo nmcli dev set $IF managed yes
iw dev $IF info | grep type      # erwartet type managed
```

---

## Häufig gestellte Fragen (FAQ)

**F: Wie bringt man unter Ubuntu 24.04 eine ALFA-Karte in den Monitor-Modus?**
A: Ab kernel 6.17 genügt es, die Schnittstelle der Verwaltung durch den NetworkManager zu übergeben und in den monitor-Schnittstellenmodus zu wechseln, ohne einen Drittanbietertreiber zu installieren; der Ablauf ist bei den drei in diesem Artikel getesteten Treiberfamilien rtw88 / rtw89 / mt76 gleich, die ausführlichen Befehle finden Sie in den Schritten im Text.

**F: Warum benötigt eine ALFA-Karte unter Ubuntu keinen zusätzlichen Treiber?**
A: Weil Realtek `rtw88`/`rtw89` und MediaTek `mt76` diese USB-Chips nach und nach in die in-kernel-Unterstützung des Mainline-Kernels aufgenommen haben (die Mindestversion unterscheidet sich je Karte, von 4.19 bis 6.17; unter Ubuntu 24.04 benötigen AX und AXER Kernel 6.17 oder höher, z. B. den HWE-Kernel von 24.04.4); mit kernel 6.17 (auf dem GX10 getestet) sind alle 9 Karten dieses Artikels integriert, direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS.

**F: Was tun, wenn sich ein älteres iPhone nicht mit einem mit einer ALFA-Karte aufgebauten WPA3-Hotspot verbindet?**
A: Im Test zeigten sich zwei häufige Ursachen: Erstens muss die hostapd-Option `sae_pwe` auf 0 statt 2 gesetzt werden, um mit älteren iPhones kompatibel zu sein; zweitens kann das Beibehalten der 802.11n-Einstellung bei älteren Geräten die Assoziation scheitern lassen – wenn Kompatibilität Vorrang hat, empfiehlt sich, 802.11n abzuschalten.

**F: Welche der Treiberfamilien `rtw88`, `rtw89`, `mt76` unterstützt Mesh oder IBSS?**
A: Im Test kann die `mt76`-Familie (wie AWUS036ACM / ACHM) im Einzelbetrieb Mesh (802.11s) und IBSS aufbauen; Realtek `rtw88` kann IBSS im Einzelbetrieb joinen (maßgeblich am ACH getestet), unterstützt aber kein Mesh; `rtw89` deklariert nicht einmal IBSS-Unterstützung.

## 7. Weiterführende Literatur

- Vollständiger Fähigkeitsvergleich und Gesamtbewertung der neun ALFA-Karten → [Gesamtbewertungs-Hub der ALFA-WLAN-Karten (Gesamttabelle)](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Schrittanleitung zur Realtek-rtw88-Beispielkarte → [AWUS036ACH Einzelkartentest](/de/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- Schrittanleitung zur MediaTek-mt76-Beispielkarte → [AWUS036ACHM Einzelkartentest](/de/blog/awus036achm-asus-gx10-ubuntu-test-report/)

---

*Testinstanz: Yopitek (ALFA-Network-Distributor Taiwan) — https://www.yupitek.com | Testumgebung: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Testgerät: Apple iPhone 7 Plus (WPA3 zusätzlich iPhone 15 Pro)*
