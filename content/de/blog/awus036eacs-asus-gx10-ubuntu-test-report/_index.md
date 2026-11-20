---
title: "ALFA AWUS036EACS im Einzelkartentest: RTL8821CU (BT + WiFi kombiniert) auf dem ASUS GX10 (ARM64 / Ubuntu 24.04) – Monitor · Injection · AP · End-to-End-Handshake"
slug: awus036eacs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036eacs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036eacs
  - rtl8821cu
  - rtw88-8821cu
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036EACS (Bluetooth+Wi-Fi kombiniert) im Praxistest unter Ubuntu 24.04 ARM64: ohne Treiberinstallation, Injektion in beiden Bändern 100 %, Monitor, AP, WPA3-SAE, End-to-End-Handshake (79 ACKs, .22000) bestanden. Inkl. USB-Wiedereinsteck-Risiko. Plattform ASUS GX10, RTL8821CU."
faq:
  - question: "Benötigt der AWUS036EACS unter Ubuntu 24.04 ARM64 einen Treiber?"
    answer: "Auf dem in diesem Artikel getesteten kernel 6.17 (ASUS GX10) nicht: Der RTL8821CU wird vom kernel-internen rtw88_8821cu-Treiber übernommen, direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS; der Schnittstellenname lautet wlx plus MAC und bleibt beim erneuten Einstecken gleich."
  - question: "Wie schlägt sich der AWUS036EACS beim Monitor-Modus und bei der Paket-Injektion?"
    answer: "Monitor ist in 2,4G und 5G stabil, die meisten Kanäle erreichen die vollen 300 frames; aireplay-ng --test ergibt in beiden Bändern 30/30 (100 %). Vor der 5G-Injektion ist iw reg set US nötig, um die TW-Beschränkung des TX aufzuheben."
  - question: "Kann der AWUS036EACS einen WPA-Handshake erfassen?"
    answer: "Ja. Im End-to-End-Praxistest mit eigenem AP und eigenem iPhone 7 Plus: deauth mit 79 empfangenen ACKs, vollständige Erfassung von M1–M4, hcxpcapngtool --all exportiert die .22000 (784 bytes, 2 EAPOL-pairs). Nur in eigenen oder autorisierten Netzwerken."
  - question: "Der AWUS036EACS ist nach dem Einstecken in lsusb sichtbar, aber es erscheint keine wlx-Netzwerkschnittstelle – was tun?"
    answer: "Das ist eine probe-Race-Condition des BT+Wi-Fi-Kombigeräts: Das Bluetooth ist bereits an btusb gebunden, während das rtw88_8821cu des Wi-Fi hängenbleibt. Im Test sind das Neuladen der Module und manuelles bind meist wirkungslos; die zuverlässige Lösung ist, die Karte abzuziehen und in einen anderen USB-Port wieder einzustecken."
  - question: "Unterstützt der AWUS036EACS Mesh, IBSS oder hcxdumptool?"
    answer: "Nein. Bei rtw88 geben active-monitor, IBSS, mesh und P2P -95 zurück oder der join ist wirkungslos; hcxdumptool 8.x lässt sich nur auf 2,4 GHz armen (auf 5 GHz schlägt das Armen fehl), verwenden Sie stattdessen airodump-ng + aireplay-ng. VHT nur 80 MHz. Für Mesh / IBSS wählen Sie AWUS036ACM / ACHM."
draft: false
---

> Testinstanz: Yopitek (ALFA-Network-Distributor Taiwan) | Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Testgerät: eigenes iPhone 7 Plus (WPA3 zusätzlich iPhone 15 Pro) | Testobjekt: eigenes Büro-WLAN (SSID YUPITEK, 2,4G ch5 / 5G ch36, 157).
>
> Dieser Artikel ist ein Fähigkeits- und Kompatibilitäts-Praxistest der Einzelkarte AWUS036EACS. Alle Monitor- / Injection- / Handshake-Erfassungen erfolgten auf Yopiteks eigener Hardware, im eigenen Büro-WLAN, gegen eigene Testgeräte und sind eine legitime Fähigkeitsvalidierung der Hardware durch den Distributor; sie richten sich gegen kein fremdes Netzwerk und liefern keine Angriffsanleitung.

**Kernaussagen (TL;DR)**: Der AWUS036EACS läuft am GX10 / Ubuntu 24.04 (kernel 6.17) ohne Treiberinstallation; Injektion in beiden Bändern 100 %, End-to-End-.22000 bestanden (79 ACKs); bei der BT+Wi-Fi-Kombikarte ist auf das Wiedereinstecken zu achten.

## 1. Diese Karte und die Testplattform

Der AWUS036EACS ist ALFAs leichte, mobile Wi-Fi-5-(802.11ac-)USB-Karte, Chip Realtek RTL8821CU, 1x1 Single-Stream, Dual-Band 2,4 GHz und 5 GHz, zudem mit integriertem Bluetooth – also ein BT + WiFi kombiniertes Gerät. Dieser Artikel stellt sie einzeln auf Yopiteks Testtisch und nimmt sie in der Umgebung ASUS GX10 (ARM64) mit Ubuntu 24.04 Punkt für Punkt ab, um die Fragen zu beantworten, die Kunden am meisten umtreiben: Wird der Treiber unter ARM64 erkannt, welche Modi sind nutzbar, wie weit reicht die Leistung?

Zunächst die Positionierung klar gesagt. Dies ist eine Kompatibilitäts- und Fähigkeitsgrenzen-Validierung eigener Ware durch den Distributor, keine Angriffsanleitung. Alle im Text genannten Injection- und Handshake-bezogenen Fähigkeitsmessungen erfolgen ausnahmslos in der eigenen geschlossenen Umgebung gegen eigene Geräte und liefern keinerlei Schritte für Operationen gegen externe Netzwerke.

Testplattform und -methode entsprechen den übrigen Einzelkartenartikeln dieser Charge:

- Rechenplattform: ASUS GX10 (ARM64 / aarch64)
- Betriebssystem: Ubuntu 24.04 LTS, kernel 6.17.0-1014-nvidia
- Treiberstrategie: Verwendung des kernel-internen (in-kernel) Treibers, direkt nach dem Einstecken erkannt, ohne Installation irgendeines Drittanbieter-DKMS-Moduls
- Testgerät: Apple iPhone 7 Plus (WPA3-SAE zusätzlich mit iPhone 15 Pro nachgemessen)
- Testumgebung: eigenes Büro-WLAN, SSID YUPITEK, 2,4 GHz ch5 / 5 GHz ch36, ch157
- Sicherheitsregel: Durchgehend nur die `wlx*`-Schnittstelle bedienen, die interne Uplink-Hauptleitung nicht anfassen; niemals `airmon-ng check kill` ausführen (das schaltet den NetworkManager ab und trennt den GX10 vom Netz)

## 2. Hardware und Treiber: die Wahrheit über das BT + WiFi kombinierte Gerät

Zuerst die Details. Die folgende Tabelle zeigt den tatsächlichen Mount-Status des AWUS036EACS auf kernel 6.17:

| Punkt | Inhalt |
|---|---|
| Chip | Realtek RTL8821CU (1x1 Single-Stream) |
| Generation | Wi-Fi 5 (802.11ac), 2,4 + 5 GHz |
| Kombifunktion | BT + WiFi kombiniertes Gerät (mit integriertem Bluetooth) |
| USB ID | `0bda:c820` |
| Treiber | `rtw88_8821cu` (in-kernel, USB-Unterstützung seit kernel 6.2) |
| Firmware | 24.11.0 (H2C version 12, in dmesg gemessen) |
| VHT-Bandbreite | nur 80 MHz (kein 160 / 80+80) |

Per `iw phy` abgefragt, sind die unterstützten interface modes `managed` / `AP` / `AP/VLAN` / `monitor` (`IBSS` ist aufgeführt, aber der join ist im Test wirkungslos); die Bänder umfassen 2,4 GHz ch1–13 und 5 GHz ch36–165 (davon sind ch52–144 DFS-Bänder); zu den ciphers zählen CCMP-256, GCMP-128 / GCMP-256 und CMAC – damit sind die Voraussetzungen erfüllt, um WPA3 auf der AP-Seite zu fahren.

Beim Treiber gibt es keine Unklarheit. Die USB-Unterstützung des RTL8821CU wurde seit kernel 6.2 in das Mainline-`rtw88` aufgenommen, der kernel 6.17 des GX10 enthält `rtw88_8821cu` bereits, es wird direkt nach dem Einstecken geladen, ohne Kompilieren oder DKMS. Frühere in-kernel-Versionen hatten einen Bug im AP mode, der durch den macid patch (ab linux-next-20240911) behoben wurde; die drei AP-Modi dieser Runde auf kernel 6.17 wurden im Test alle sauber beendet. Bestätigung:

```bash
lsusb | grep -i '0bda:c820'
# ID 0bda:c820 Realtek Semiconductor Corp. 802.11ac NIC
sudo dmesg | grep -i 8821cu
# rtw88_8821cu ...: Firmware version 24.11.0, H2C version 12 -> renamed from wlan0
```

Nach dem Laden wird die Wi-Fi-Schnittstelle als `wlx` + MAC benannt (z. B. `wlx00c0cab3a52e`), nicht als `wlan0`; der Name bleibt beim erneuten Einstecken gleich und lässt sich in Skripten stabil referenzieren.

Worauf man wirklich achten muss, ist die Sache mit dem „kombinierten Gerät“. Prüft man mit `lsusb -t`, sieht man, dass unter demselben RTL8821CU mehrere USB-interfaces hängen: Die Bluetooth-Funktion ist an `btusb` gebunden, die Wi-Fi-Funktion separat an `rtw88_8821cu`.

```
/:  Bus 0X.Port X: Dev X, Class=root_hub, Driver=xhci-hcd
    |__ Port X: Dev X, If 0, Class=Wireless, Driver=btusb               <- Bluetooth
    |__ Port X: Dev X, If 1, Class=Wireless, Driver=btusb               <- Bluetooth
    |__ Port X: Dev X, If 2, Class=Vendor Specific, Driver=rtw88_8821cu <- Wi-Fi
```

(Bus-/Port-Nummern ändern sich mit der Anzahl der Ein-/Aussteckvorgänge; entscheidend ist, dass interface 0/1 über `btusb` laufen und erst interface 2 das `rtw88_8821cu` des Wi-Fi ist.)

**Das Wiedereinsteck-Risiko des BT + WiFi kombinierten Geräts (vor dem Einsatz unbedingt lesen).** Weil Bluetooth und Wi-Fi sich dasselbe USB-Gerät teilen, kann es an manchen USB-Ports oder bei schnellem Wiedereinstecken dazu kommen, dass das Bluetooth bereits an `btusb` gebunden ist, der probe des Wi-Fi-interface aber hängenbleibt – eine Race-Condition, bei der `lsusb` zwar `0bda:c820` zeigt, aber keine `wlx`-Schnittstelle entsteht. Im Test sind das Neuladen nach `modprobe -r` oder manuelles `bind` meist wirkungslos (`bind` gibt `Operation already in progress` zurück). Es gibt nur eine zuverlässige Lösung: Karte abziehen, in einen anderen USB-Port wieder einstecken; nach dem Portwechsel erfolgt die Aufzählung sauber und die `wlx`-Schnittstelle erscheint normal. Das ist das zusätzliche Betriebsdetail, das man bei dieser Karte gegenüber dem nicht kombinierten AWUS036ACS (RTL8811AU) kennen muss; wer es vorher weiß, hält es nicht fälschlich für einen Kartendefekt.

## 3. Getestete Fähigkeiten: Monitor / Injection / AP / WPA3

Die folgende Tabelle ist die Zusammenfassung der Kernfähigkeiten des AWUS036EACS; jede Zeile wurde am 18.11.2026 auf echter GX10-Hardware ausgeführt:

| Fähigkeit | 2,4 GHz | 5 GHz | Testkern |
|---|---|---|---|
| Monitor | ✅ stark | ✅ stark | die meisten Kanäle voll 300 frames; Community-#453 „ch1 hängt“ nicht reproduziert |
| Injection | ✅ 100 % (30/30) | ✅ 100 % (30/30) | Power 2,4G -38.27 / 5G -76.10; stärkste Injektion der ac-Karten dieser Charge |
| AP-Hotspot | ✅ sauberes Ende | ✅ VHT 80 MHz | `hostapd`-Station, iPhone 7 Plus verbindet sich und schließt den 4-way ab |
| WPA3-SAE (AP-Seite) | ✅ iPhone verbindet sich | Nicht getestet | SAE-only + erzwungenes PMF (`ieee80211w=2`, `sae_pwe=0`) |
| WPA-Handshake-Erfassung | — | ✅ End-to-End | M1–M4 vollständig, deauth empfängt 79 ACKs, Export der `.22000` |

Monitor (Monitor-Modus) ist in 2,4 und 5 GHz stabil. Alle sechs Kanäle einzeln erfasst, erreichen die meisten die vollen 300 frames. Für den 8821cu gibt es hier noch ein sehr wichtiges positives Ergebnis: Das von der rtw88-Community lange verfolgte GitHub-#453 „8821cu bleibt bei kernel ≥6.9 mit STA up im monitor auf ch1 hängen“ trat in der GX10-Umgebung nicht auf; die 5-GHz-Kanäle ch36, ch149 und ch157 erreichen stabil die vollen 300 Frames. Für eine bandübergreifende Spektrumserkundung oder Paketanalyse über 2,4 / 5 GHz lässt sich der Monitor dieser Karte bedenkenlos nutzen.

Die Injection (Paket-Injektion) ist die herausragendste Leistung. Gemessen mit `aireplay-ng --test` ergeben 2,4 GHz und 5 GHz beide 30/30, 100 %, die stärkste Injektion unter den ac-Karten dieser Charge (der ebenfalls 1x1-AWUS036ACS erreicht in 5G nur 96 %). Hier ein Taiwan-spezifisches Detail: Der 5-GHz-TX wird gesperrt, wenn die regulatory domain auf TW steht; vor der Messung mit `iw reg set US` entsperren, nach dem Test mit `iw reg set TW` zurücksetzen.

Beim AP-Hotspot wurden mit `hostapd` jeweils 2,4 GHz (WPA2), 5 GHz (VHT 80 MHz) und WPA3-SAE in drei Varianten aufgebaut; das iPhone 7 Plus konnte sich jeweils verbinden und den 4-way handshake abschließen, und das Herunterfahren der Station endete sauber (`AP-DISABLED` / `TERMINATING`). Das bei manchen Karten auftretende beacon-re-key-Problem trat nicht auf; in diesem Punkt ist 2,4G stabiler als die Schwesterkarte ACS. WPA3 nutzt SAE-only mit erzwungenem PMF (`ieee80211w=2`, `sae_pwe=0`); mit dem iPhone 15 Pro erfolgreich verbunden, bestätigt das die Nutzbarkeit von WPA3-SAE auf der AP-Seite des RTL8821CU.

Die Kali-Toolchain (Plattformebene) lässt sich auf dieser Karte ebenfalls durchgängig betreiben: `airmon-ng` erkennt den EACS (`rtw88_8821cu`), aber auch hier kein `check kill` verwenden; `kismet` startet mit dieser Karte als data source erfolgreich und erzeugt im Test ein `.kismet`-Log von etwa 733 KB; `wifi.recon on` von `bettercap` 2.32 funktioniert normal (die txpower-Warnung ist ignorierbar); `wifite` (git 3.0.0) findet über 10 APs, darunter das eigene YUPITEK (ch5, PWR 84) – diese Version hat kein `--band`-Flag, man muss stattdessen mit `-c 1,6,11,36,149,157` die Kanäle angeben; `Wireshark` / `tshark` 4.x erfassen und analysieren im monitor ch6 real 325 frames; auch die zufällige MAC-Tarnung von `macchanger` funktioniert. Dieser Tooling-Abschnitt entspricht den übrigen Karten der Charge; der Unterschied liegt vor allem bei den vorne genannten Injection- und Monitor-Hardwarefähigkeiten.

## 4. End-to-End-Handshake: Highlight und ehrliche Grenze

Die herausragende Fähigkeit dieser Karte ist, Injection und Capture zu einer vollständig nutzbaren Kette zu verbinden. Zwischen dem eigenen YUPITEK-AP und dem eigenen iPhone 7 Plus läuft die gesamte Kette auf echter Hardware durch: deauth an das eigene iPhone senden (Injection, im Test 79 empfangene ACKs, was belegt, dass die injizierten Pakete den Client tatsächlich erreichen) → beim Wiederverbinden des iPhone den vollständigen 4-way handshake erfassen (M1, M2, M3, M4 je 1) → mit `hcxpcapngtool --all` die hashcat-formatige `.22000` exportieren (784 bytes, 2 EAPOL-pairs, RC checked). Der gesamte Ablauf dient nur der Validierung der Kartenfähigkeit; das Ziel ist durchgehend der eigene AP und das eigene Handy, kein fremdes Netzwerk ist beteiligt.

In der Praxis sind zwei entscheidende Details festzuhalten: Im Büro senden gleichzeitig mehrere YUPITEK-APs gleichen Namens auf ch36; bei der Erfassung nicht auf `--bssid` fixieren, sondern den gesamten Kanal erfassen, damit nicht gerade der AP herausgefiltert wird, mit dem das iPhone tatsächlich verbunden ist; außerdem ist `hcxpcapngtool` standardmäßig recht streng, man muss `--all` ergänzen, um die `.22000` exportieren zu können.

Auch die ehrlichen Grenzen seien einmal klar genannt:

- **Kein Support für active-monitor / IBSS (Ad-hoc) / Mesh (802.11s) / Wi-Fi Direct (P2P).** Diese Modi geben unter `rtw88` `-95` (Operation not supported) zurück oder lassen sich auflisten, doch der join ist wirkungslos – eine Einschränkung auf Treiberebene, ohne Lösung. Kunden, die Mesh- / IBSS-Experimente brauchen, sollten auf MediaTeks AWUS036ACM / ACHM wechseln.
- **`hcxdumptool` 8.x ist eingeschränkt.** Es benötigt active-monitor; auf dieser Karte lässt es sich nur auf 2,4 GHz armen und scheitert auf 5 GHz (die übrigen Karten der Charge melden alle `failed to arm interface`); auf `airodump-ng` + `aireplay-ng` wechseln reicht – die Injektion dieser Karte ist 100 % und bleibt unberührt.
- **VHT nur 80 MHz.** Single-Stream, kein 160 MHz oder 80+80; die Positionierung ist eine leichte Mobilkarte, nicht die Rolle eines Durchsatz-Boliden.
- **VIF nur teilweise.** Nur ein passiver monitor neben einer managed-Schnittstelle auf demselben Kanal (Software-monitor) funktioniert (im Test 100 frames); unabhängige doppelte VIFs werden nicht unterstützt.

## 5. Einsatzszenarien und Auswahl

Insgesamt ist die Positionierung des AWUS036EACS laut Praxistest sehr klar: Wer Dual-Band-Monitor + Injection + End-to-End-Handshake-Validierung braucht und zugleich eine leichte, mobile Karte mit integriertem Bluetooth möchte, für den ist sie die passende Lösung. Die 100-%-Injektion in beiden Bändern und die sauberen AP- / WPA3-Leistungen reihen sie für Wireless-Audits und Security-Schulungen im autorisierten Rahmen in die Erste-Wahl-Gruppe neben AWUS036ACH und AWUS036ACS ein.

In welchen Fällen eine andere Karte empfehlenswert ist:

- **Wenn vor Ort häufig wieder eingesteckt wird oder die USB-Portqualität des Gehäuses schwankt** → die probe-Race-Condition des Kombigeräts macht mehr Mühe; erwägen Sie den nicht kombinierten AWUS036ACS (RTL8811AU, ebenfalls 1x1 ac, ohne die Bluetooth-Variable).
- **Für Mesh- / IBSS-Experimente** → `rtw88` unterstützt sie nicht, wechseln Sie zu MediaTeks AWUS036ACM / ACHM.
- **Wer stärksten Empfang oder Monitor über große Distanz sucht** → der Doppelantennen-AWUS036ACH oder der Wi-Fi-6-AWUS036AXER passt besser.
- **Warnung**: Wenn der Zweck Injection / Handshake ist, wählen Sie nicht den MT7921-basierten AWUS036AXM / AXML – die Injektion schlägt auf dieser Plattform schlicht fehl.

Wer die horizontale Monitor- / Injection- / AP- / WPA3-Gegenüberstellung aller 9 ALFA-Karten und die vollständige Auswahlmatrix auf einmal sehen möchte, kehrt zur Gesamttabelle zurück: [Der umfassendste Praxistest 2026: Die Gesamtmatrix von 9 ALFA-WLAN-Karten auf dem ASUS GX10](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Häufig gestellte Fragen (FAQ)

**F: Benötigt der AWUS036EACS unter Ubuntu 24.04 ARM64 einen Treiber?**
Auf dem in diesem Artikel getesteten kernel 6.17 (ASUS GX10) nicht: Der RTL8821CU wird vom kernel-internen rtw88_8821cu-Treiber übernommen, direkt nach dem Einstecken erkannt, ohne Kompilieren, ohne DKMS; der Schnittstellenname lautet wlx plus MAC und bleibt beim erneuten Einstecken gleich.

**F: Wie schlägt sich der AWUS036EACS beim Monitor-Modus und bei der Paket-Injektion?**
Monitor ist in 2,4G und 5G stabil, die meisten Kanäle erreichen die vollen 300 frames; `aireplay-ng --test` ergibt in beiden Bändern 30/30 (100 %). Vor der 5G-Injektion ist `iw reg set US` nötig, um die TW-Beschränkung des TX aufzuheben.

**F: Kann der AWUS036EACS einen WPA-Handshake erfassen?**
Ja. Im End-to-End-Praxistest mit eigenem AP und eigenem iPhone 7 Plus: deauth mit 79 empfangenen ACKs, vollständige Erfassung von M1–M4, `hcxpcapngtool --all` exportiert die .22000 (784 bytes, 2 EAPOL-pairs). Nur in eigenen oder autorisierten Netzwerken.

**F: Der AWUS036EACS ist nach dem Einstecken in lsusb sichtbar, aber es erscheint keine wlx-Netzwerkschnittstelle – was tun?**
Das ist eine probe-Race-Condition des BT+Wi-Fi-Kombigeräts: Das Bluetooth ist bereits an btusb gebunden, während das rtw88_8821cu des Wi-Fi hängenbleibt. Im Test sind das Neuladen der Module und manuelles bind meist wirkungslos; die zuverlässige Lösung ist, die Karte abzuziehen und in einen anderen USB-Port wieder einzustecken.

**F: Unterstützt der AWUS036EACS Mesh, IBSS oder hcxdumptool?**
Nein. Bei rtw88 geben active-monitor, IBSS, mesh und P2P -95 zurück oder der join ist wirkungslos; hcxdumptool 8.x lässt sich nur auf 2,4 GHz armen (auf 5 GHz schlägt das Armen fehl), verwenden Sie stattdessen airodump-ng + aireplay-ng. VHT nur 80 MHz. Für Mesh / IBSS wählen Sie AWUS036ACM / ACHM.

---

## 6. Weiterführende Literatur

- [Der umfassendste Praxistest 2026: Die vollständige Monitor- · Injection- · AP-Matrix von 9 ALFA-WLAN-Karten auf dem ASUS GX10 (ARM64 / Ubuntu 24.04)](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/) (Hub-Gesamttabelle)
- [Wireless-Audit im Zeitalter von WPA3-SAE: Praxistest der Handshake-Erfassungsfähigkeit von 9 ALFA-Karten](/de/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- [Ohne Treiberinstallation: Monitor- und AP-Modus der ALFA-Karten unter Ubuntu 24.04 + kernel 6.17 mit dem in-kernel-Treiber aktivieren](/de/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- Ebenfalls eine rtw88-USB-ac-Karte → [AWUS036ACS im Einzelkartentest-Bericht (RTL8811AU)](/de/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*Testinstanz: Yopitek (ALFA-Network-Distributor Taiwan) — https://www.yupitek.com*
