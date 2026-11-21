---
title: "Drahtlos-Audit im Zeitalter von WPA3-SAE: Handshake-Erfassungsfähigkeit von 9 ALFA-Karten im Praxistest und die sae_pwe-Kompatibilitätsfalle bei der iPhone-Verbindung"
slug: alfa-wpa3-sae-handshake-capability-arm64
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-wpa3-sae-handshake-capability-arm64.webp"
bannerimage: "/images/blog/banner/alfa-wpa3-sae-handshake-capability-arm64.webp"
author: "benny-lai"
tags:
  - wpa3-sae
  - wpa-handshake
  - sae-pwe
  - wireless-security
  - alfa-network
  - rtl8821cu
  - hcxpcapngtool
  - wifi-6
description: "Praxistest der WPA3-SAE-Handshake-Erfassungsfähigkeit von ALFA-Karten unter Ubuntu (übertragbar auf Kali): Injektionsraten von 9 Karten und End-to-End-.22000-Erfassungsergebnisse, die sae_pwe-Kompatibilitätsfalle und Auswahlempfehlungen."
faq:
  - question: "Kann der AWUS036AXM unter Ubuntu einen WPA-Handshake erfassen?"
    answer: "Auf dieser Plattform nicht. Im Test brach beim AWUS036AXM und AWUS036AXML (MT7921-Chip) wegen fehlgeschlagener Injektion – kein deauth absendbar – die gesamte 4-Way-Handshake-Erfassungskette mit ab, daher sind sie für Zwecke, die eine Handshake-Erfassung erfordern, nicht geeignet."
  - question: "Welche ALFA-Karte erfasst WPA-Handshakes am zuverlässigsten?"
    answer: "Im Test war der AWUS036EACS am solidesten: Die Injection erreichte in beiden Bändern 100 %, nach dem deauth kamen 79 ACK-Rückmeldungen an, und es wurde erfolgreich eine hashcat-taugliche .22000-Datei exportiert – das Modell mit der vollständigsten End-to-End-Verifikation dieser Charge."
  - question: "Warum verbindet sich ein älteres iPhone nicht mit einem WPA3-SAE-Hotspot?"
    answer: "Entscheidend ist die hostapd-Option sae_pwe: Auf 2 gesetzt (erzwungenes H2E) scheitert die Verbindung des iPhone 7 Plus; nach Rückstellung auf sae_pwe=0 (Hunting-and-Pecking) lässt sich der 4-Way-Handshake normal abschließen und die Verbindung herstellen."
  - question: "Lässt sich in einer WPA3-Umgebung noch ein 4-Way-Handshake erfassen?"
    answer: "Eine reine WPA3-SAE-Umgebung erzwingt PMF (ieee80211w=2), traditionelle Methoden gegen Management-Frames werden blockiert; dass sich in der Praxis dennoch ein Handshake erfassen lässt, liegt meist daran, dass das Ziel im WPA2/WPA3-Übergangsmodus läuft und nicht reines WPA3."
  - question: "Die 5-GHz-Injection einer ALFA-Karte lässt sich nicht messen – ist das ein Hardwareproblem?"
    answer: "Nicht unbedingt. Die Standard-Regulierungsdomäne begrenzt die Sendeleistung in Teilen der 5-GHz-Bänder, sodass sich die Injektion „nicht hinausbekommen“ lässt; im Test wurde die zuvor fehlgeschlagene 5-GHz-Injektion nutzbar, nachdem die Regulierungsdomäne in einen sendefähigen Zustand geschaltet wurde – es empfiehlt sich, zuerst die Einstellung der Regulierungsdomäne zu prüfen, bevor man auf eine Hardwarebeschränkung schließt."
draft: false
---

> Testinstanz: Yopitek (ALFA-Network-Distributor Taiwan) | Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 | Testgerät: eigenes iPhone 7 Plus (WPA3 zusätzlich iPhone 15 Pro) | Testobjekt: eigenes Büro-WLAN (SSID YUPITEK, 2,4G ch5 / 5G ch36, 157).
>
> Dieser Artikel ist eine Übersicht über Fähigkeiten und Kompatibilität der ALFA-WLAN-Karten. Alle Monitor-/Injection-/Handshake-Erfassungen erfolgten auf Yopiteks eigener Hardware, im eigenen Büro-WLAN und gegen eigene Testgeräte; es handelt sich um eine rechtmäßige Fähigkeitsverifizierung der Hardware durch den Distributor, nicht gegen irgendein fremdes Netzwerk gerichtet und ohne Angriffsschritte.

## Kernaussagen (TL;DR)

Von den 9 auf dem ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17) getesteten ALFA-Karten haben 7 (ACM, ACHM, ACH, ACS, EACS, AX, AXER) die End-to-End-Erfassung des WPA-Handshakes bis zum `.22000` geschafft; der AWUS036EACS erreichte Dual-Band-Injektion 100 % mit 79 ACKs, während die MT7921-basierten AXM / AXML auf dieser Plattform an der Injektion scheitern.

- Nach der Verbreitung von WPA3-SAE verschiebt sich der Audit-Schwerpunkt von „kann man monitoren“ hin zur „End-to-End-Handshake-Erfassungsfähigkeit“ und zur „`sae_pwe`-Endgerätkompatibilität“.
- **End-to-End-`.22000` bei 7 von 9 Karten belegt**: ACM, ACHM, ACH, ACS, EACS, AX, AXER; davon ist EACS am solidesten (Dual-Band-Injektion 100 %, 79 ACKs).
- **AXM / AXML (MT7921) schlagen auf dieser Plattform bei der Injektion fehl**, können kein deauth, erfassen keinen Handshake, für Audit-Zwecke unbedingt meiden.
- `sae_pwe`-Falle: Ältere iPhones benötigen `sae_pwe=0`, um sich zu verbinden; vor der 5G-Injektion zuerst mit `iw reg set US` das TX entsperren.
- Reines WPA3 erzwingt PMF (`ieee80211w=2`); dass sich vor Ort dennoch erfassen lässt, liegt meist daran, dass das Ziel im WPA2/WPA3-Übergangsmodus läuft.

## 1. Die Verbreitung von WPA3-SAE hat die Hürde für Drahtlos-Audits insgesamt angehoben

In den letzten zehn Jahren drehte sich das autorisierte Drahtlos-Audit (authorized wireless audit) fast ausschließlich um den 4-Way-Handshake von WPA2-PSK: einmal einen vollständigen Handshake erfassen, und das Backend kann offline abgleichen. Doch seit die Wi-Fi-6-Zertifizierung WPA3 als Pflichtbestandteil aufgenommen hat, verdrängt SAE (Simultaneous Authentication of Equals, umgangssprachlich Dragonfly) nach und nach PSK und verengt den alten Weg „Handshake erfassen, offline verifizieren“ immer mehr.

Für Distributoren und Ingenieure an der Front bringt WPA3-SAE drei praktische Veränderungen:

1. **PMF (Protected Management Frame) wird Pflicht.** Die WPA3-SAE-Spezifikation erzwingt `ieee80211w=2`, Management-Frames sind geschützt, und die traditionelle Methode „mal eben ein deauth, um ein Gerät offline zu werfen“ wird in einer reinen WPA3-Umgebung direkt blockiert.
2. **Der Übergangsmodus (transition mode) behält den 4-Way bei.** In der Realität fahren sehr viele APs einen gemischten WPA2/WPA3-Übergangsmodus und behalten zur Kompatibilität mit älteren Geräten den WPA2-4-Way-Handshake bei – das ist auch der Hauptgrund, warum sich bei autorisierten Audits derzeit noch Handshakes erfassen lassen. Ob sich ein Handshake erfassen lässt, hängt zu einem großen Teil davon ab, in welchem Modus das Ziel vor Ort läuft.
3. **Endgerätkompatibilität wird zur neuen Falle.** SAE hat verschiedene Herleitungsweisen für das password element (gesteuert durch `sae_pwe`); ist der AP-Parameter einmal falsch gesetzt, verbindet sich nicht einmal das eigene ältere iPhone, geschweige denn, dass sich das Verbindungsverhalten des Kunden-Endgeräts in einer Audit-Situation nachstellen ließe.

Wenn ein Kunde also fragt „Welche ALFA-Karte eignet sich für ein autorisiertes WPA3-bezogenes Audit“, ist die Antwort nicht mehr so einfach „kann man monitoren“, sondern hängt von zwei Dingen ab: der **End-to-End-Handshake-Erfassungsfähigkeit** und der **Kompatibilität mit WPA3-SAE-Parametern und echten Endgeräten**. Dieser Bericht ist die Fähigkeitsübersicht, die nach einem Praxistest von 9 ALFA-Karten auf derselben ARM64-Plattform zusammengestellt wurde.

## 2. Was „End-to-End-Handshake-Erfassungsfähigkeit“ bedeutet (Konzeptebene)

Hier wird die Fähigkeit zunächst in drei Abschnitte zerlegt, rein konzeptionell, ohne irgendwelche Operationsbefehle gegen fremde Netzwerke:

- **Abschnitt eins: Injection (aktives Einspeisen).** Die Karte muss einen bestimmten Management-Frame „hinausbekommen“ können, um einen bereits verbundenen Client zu einer erneuten Assoziation zu veranlassen. Viele Karten können nur passiv monitoren (Pakete empfangen), aber keine Injection (aktiv senden). Das ist der am leichtesten blockierende Abschnitt der gesamten Kette. Diese Charge quantifiziert die Injektionserfolgsrate mit `aireplay-ng --test` und verifiziert im Handshake-Test anhand der vom Client zurückgemeldeten ACKs, ob der Frame tatsächlich ankam.
- **Abschnitt zwei: 4-Way-Handshake-Erfassung.** Wenn ein Client sich erneut assoziiert, tauscht WPA vier EAPOL-Nachrichten aus (M1–M4). Die Karte muss im Monitor-Modus diese vier Frames vollständig einsammeln, keiner darf fehlen.
- **Abschnitt drei: Export der hashcat-`.22000`.** Das erfasste pcap mit `hcxpcapngtool --all` in das hashcat-Format `.22000` umwandeln und dem Backend zur Offline-Verifikation übergeben.

**Erst wenn alle drei Abschnitte an echter Hardware durchlaufen, gilt es als „End-to-End“**: tatsächlich ein deauth (Injection) an das eigene iPhone 7 Plus senden → die vollständigen M1–M4 einsammeln → die `.22000` exportieren und ablegen. Nur empfangen und nicht senden können, oder die vier Frames nicht vollständig einsammeln, oder die Datei nicht exportieren können – nichts davon zählt als End-to-End. Dieser Artikel listet keine schrittweisen Angriffsbefehle; die folgende Übersicht beantwortet nur eine Frage: Welche Karte kommt auf dieser Fähigkeitskette durch.

Am Beispiel des solidesten EACS dieser Charge sieht ein erfolgreiches End-to-End so aus: Nach dem Senden des deauth meldete der Client **79 ACKs** zurück (Bestätigung, dass die Frames tatsächlich an diesem Handy ankamen), `aircrack-ng` stellte für YUPITEK 1 Handshake fest, von den EAPOL-Frames M1 / M2 / M3 / M4 kam jeweils 1 an, die erfasste Client-MAC begann mit der Apple-OUI (Bestätigung, dass es genau dieses iPhone 7 Plus war), und zuletzt exportierte `hcxpcapngtool --all` eine `.22000` von rund 784 Bytes. Fehlt eine dieser vier Bedingungen, zählt diese Erfassung nicht. Das ist auch der Grund, warum „monitoren können“ und „End-to-End erfassen können“ zwei völlig verschiedene Dinge sind.

## 3. Übersichtstabelle der Handshake-Fähigkeit der 9 Karten

| # | Modell | Chip / Generation | Injection 2.4G | Injection 5G | WPA-Handshake-Erfassungsfähigkeit |
|---|---|---|---|---|---|
| 1 | AWUS036ACM | MT7612U / Wi-Fi 5 · 2T2R | nutzbar 63–83% | nutzbar 76% | **End-to-End-`.22000` belegt** (niedrigere Injektionsrate) |
| 2 | AWUS036ACHM | MT7610U / Wi-Fi 5 · 1T1R | nutzbar 96–100% | nur Broadcast | **End-to-End-`.22000` belegt (auf 5 GHz ch36)** |
| 3 | **AWUS036ACH** | RTL8812AU / Wi-Fi 5 · 2T2R | **100%** | **100%** | **End-to-End `.22000` belegt (am 2026-11-19 nachgemessen)** |
| 4 | **AWUS036ACS** | RTL8811AU / Wi-Fi 5 · 1x1 | **100%** | 96% | **End-to-End `.22000` belegt** |
| 5 | **AWUS036EACS** | RTL8821CU / Wi-Fi 5 · 1x1 | **100%** | **100%** | **End-to-End `.22000` belegt (79 ACKs)** |
| 6 | **AWUS036AX** | RTL8832BU / Wi-Fi 6 · 2x2 | 96% | nutzbar | **End-to-End `.22000` belegt** |
| 7 | **AWUS036AXER** | RTL8832BU / Wi-Fi 6 · 2x2 | 73% | nutzbar | **End-to-End `.22000` belegt** |
| 8 | AWUS036AXM | MT7921AUN / Wi-Fi 6 · 2x2 | fehlgeschlagen | fehlgeschlagen | nicht unterstützt: Injektion fehlgeschlagen, keine Erfassung möglich |
| 9 | AWUS036AXML | MT7921AUN / Wi-Fi 6 · 2x2 | fehlgeschlagen | fehlgeschlagen | nicht unterstützt: Injektion fehlgeschlagen, keine Erfassung möglich |

**Zwei Ränge, auf einen Blick verständlich:**

- **End-to-End belegt (Erfassung → `.22000`-Ablage, 7 von 9 Karten)**: AWUS036ACM, AWUS036ACHM, AWUS036ACH, AWUS036ACS, AWUS036EACS, AWUS036AX und AWUS036AXER. Davon injiziert der EACS in beiden Bändern 100 % und empfing nach dem deauth 79 ACKs – die Karte mit der solidesten Handshake-Fähigkeit dieser Charge; der AWUS036ACH (RTL8812AU, Doppelantenne mit hohem Gewinn) injiziert in beiden Bändern 100 % und wurde am 2026-11-19 nachgemessen, mit Export einer `.22000` von 47 Hashlines – gleichauf mit dem EACS als erste Wahl für Penetrationstests. **Sieben Modelle haben die End-to-End-Handshake-Erfassung abgeschlossen: ACM, ACHM, ACH, ACS, EACS, AX, AXER.** Der ACM injiziert mit niedrigerer Rate (2,4G 63–83 % / 5G 76 %), der ACHM schaffte es auf 5 GHz (ch36); beide erzeugten eine `.22000`.
- **Keine Erfassung möglich (2 Karten)**: AWUS036AXM und AWUS036AXML (MT7921 schlägt auf dieser Plattform bei der Injektion fehl, kann kein deauth und naturgemäß auch keinen Handshake erfassen).

Besonders zu benennen sind **AXM / AXML**: Beide sind Wi-Fi 6, Monitor und AP funktionieren normal, nur die Injection funktioniert auf dieser Plattform nicht – die Hauptursache ist die mac80211-chanctx-Regression im stock kernel 6.16+ (nicht chip-bedingt); dieselben Modelle laufen in der Community zwar mit git-/patched-Treibern, doch die Firmware sperrt dann die Datenrate (entsprechend morrownr/USB-WiFi #387, morrownr/mt76 #18). Reines Surfen und Hotspot sind kein Problem, aber **für jeden Audit-Zweck, der Injektion oder Handshake-Erfassung erfordert, auf dieser Plattform grundsätzlich meiden**.

## 4. WPA3-SAE-Kompatibilitätsfalle: Falsch gesetzte Parameter, und nicht einmal das eigene iPhone verbindet sich

Über die Fähigkeit hinaus ist die Parameterkompatibilität von WPA3-SAE die Stelle, an der man vor Ort am leichtesten scheitert. Diese Charge stolperte im Test über zwei entscheidende Fallen:

### 4-1. Der ACHM muss `sae_pwe=0` haben, sonst verbindet sich das iPhone 7 Plus nicht

Die Herleitung des SAE-password-element erfolgt auf verschiedene Weisen, hostapd steuert sie mit `sae_pwe`. Als diese Charge den AWUS036ACHM als reines WPA3-SAE (`wpa_key_mgmt=SAE` + erzwungenes PMF `ieee80211w=2`) aufbaute, konnte sich, sobald `sae_pwe` auf `2` gesetzt war, **das iPhone 7 Plus direkt nicht verbinden**; erst nach Rückstellung auf `sae_pwe=0` (Hunting-and-Pecking, kompatibel mit älteren Endgeräten) verband sich das iPhone 7 Plus (iOS 15) erfolgreich und schloss den 4-Way ab.

Die Bedeutung dieser Falle: Wenn Sie in einer Audit-Situation eine WPA3-Umgebung mit überwiegend älteren iOS-Endgeräten „nachstellen“ wollen, muss der `sae_pwe` auf AP-Seite der Endgerätfähigkeit entsprechen, sonst erhalten Sie ein falsch negatives „verbindet sich nicht“ statt einer echten Kompatibilitätsaussage. Die WPA3-SAE-AP-Tests von EACS und ACS verwendeten ebenfalls `sae_pwe=0` + `ieee80211w=2`, das iPhone 7 Plus konnte sich jeweils verbinden; `sae_pwe=0` ist der in dieser Charge an älteren iPhone-Endgeräten verifizierte sichere Wert.

### 4-2. Vor der 5G-Injektion zuerst mit `iw reg set US` das TX entsperren

Die zweite Falle hängt mit der Regulierungsdomäne (regulatory domain) zusammen. Das standardmäßige `reg=TW` sperrt das TX in Teilen der UNII-Bänder, sodass sich die 5-GHz-Injection / das deauth „nicht hinausbekommen“ lassen. Diese Charge entsperrte vor jeder 5G-Injektion zuerst mit `iw reg set US` das TX und stellte nach dem Test sofort mit `iw reg set TW` zurück. Die 5G-Injektion des ACS ging nach dem Entsperren von fehlgeschlagen auf 96 %, EACS und ACH gingen direkt auf 100 %. Wer das Entsperren der reg vergisst, stuft eine Karte mit normaler Injektionsfähigkeit fälschlich als „5G nicht nutzbar“ ein.

### 4-3. Nebenbei bemerkt: PMF ist bei WPA3 Pflicht

Die WPA3-SAE-Spezifikation erzwingt `ieee80211w=2` (Management Frame Protection). Das bedeutet, dass in einer reinen WPA3-Umgebung traditionelle Methoden gegen Management-Frames von PMF blockiert werden; dass sich in realen Audits dennoch ein 4-Way erfassen lässt, liegt meist daran, dass das Ziel weiterhin im WPA2/WPA3-Übergangsmodus läuft. Nehmen Sie diesen Punkt bei der Kartenauswahl mit auf, um keine falschen Erwartungen an reine WPA3-Ziele zu stellen.

## 5. Überblick über die Toolchain: Was auf der ARM64-Plattform tatsächlich läuft

Über die Hardware-Fähigkeit hinaus beeinflusst die Plattform-Toolchain die Audit-Effizienz ebenso. Im Folgenden einige Praxiserkenntnisse, die diese Charge auf dem GX10 (ARM64) zusammengetragen hat:

- **Der Export immer mit `hcxpcapngtool --all`.** Die Standardparameter sind strenger und melden oft „not enough M1“, sodass sich keine Datei exportieren lässt; erst mit `--all` lässt sich aus vollständigen M1–M4 stabil eine `.22000` exportieren.
- **Bei mehreren APs mit gleichem Namen im Büro nicht auf `--bssid` fixieren.** Im Yopitek-Büro gibt es auf demselben Kanal mehrere gleichnamige YUPITEK-APs, und das iPhone verbindet sich mit dem stärksten Signal. Fixiert man bei der Erfassung mit `--bssid` auf eine einzelne BSSID, filtert man womöglich genau den AP heraus, mit dem das iPhone tatsächlich verbunden ist, und die gesamte Erfassung geht leer aus. Die Praxiserkenntnis lautet: **nicht auf die BSSID fixieren, direkt den gesamten Kanal erfassen** und dann aus der Ablage den vollständigen Handshake herauspicken.
- **`hcxdumptool` 8.x meldet auf dieser Plattform `failed to arm`, außer beim EACS auf 2,4 GHz (auf 5 GHz scheitert es).** Weder rtw88 / rtw89 noch mt7921u stellen active-monitor bereit, das hcxdumptool 8.x jedoch benötigt; die Lösung ist, auf den traditionellen aircrack-ng-Ablauf aus `airodump-ng` + `aireplay-ng` umzusteigen.
- **Wird nach wiederholtem Moduswechsel nichts mehr gescannt, zuerst die Karte aus- und einstecken.** Bei rtw88 / rtw89 kann nach wiederholtem Wechsel zwischen monitor / AP ein RX-Stall auftreten (0 Pakete gescannt); eine USB-Neuaufzählung stellt es wieder her, und der Schnittstellenname ist durch die MAC bestimmt und ändert sich nach dem Aus- und Einstecken nicht. Vor der Handshake-Erfassung empfiehlt es sich, als Erstes die Karte einmal neu einzustecken.
- **BT+WiFi-Kombigeräte (EACS / AXML) haben beim erneuten Einstecken ein Race.** Kombikarten mit Bluetooth bleiben beim erneuten Einstecken oder an bestimmten USB-Ports bei der Probe der WiFi-Funktion hängen und erzeugen keine `wlx`-Schnittstelle; die Lösung ist, an einem anderen USB-Port neu einzustecken, `modprobe` oder manuelles bind sind meist wirkungslos.
- **Feinheiten der Werkzeuginstallation unter ARM64.** aircrack-ng fehlt unter aarch64 oft ein prebuilt-Paket und muss aus dem Quellcode kompiliert werden; wifite in der git-Version verwenden (die apt-Version kollidiert mit dem selbst kompilierten aircrack-ng).
- **Sicherheitsregel: niemals `airmon-ng check kill`.** Der GX10 nutzt für den Uplink die interne Karte, `check kill` schaltet auch den NetworkManager mit ab und trennt den Host vom Netz. Diese Charge bediente durchgehend nur die `wlx*`-Schnittstelle der ALFA-Karte, ohne die interne Uplink-Hauptleitung anzufassen.

## 6. Auswahlfazit: Welche Karten für ein WPA3-bezogenes Audit

Fähigkeit, Kompatibilität und Plattform-Toolchain zusammengenommen, lautet die Empfehlung dieser Charge für den Zweck „autorisiertes WPA3-bezogenes Audit“:

| Bedarfsszenario | Empfohlenes Modell | Grund |
|---|---|---|
| Umfassende erste Wahl (Injection + End-to-End-Handshake) | **AWUS036EACS** | Dual-Band-Injektion 100 %, deauth empfing 79 ACKs, End-to-End-`.22000` belegt; einziger Punkt: als BT+WiFi-Kombigerät muss beim erneuten Einstecken gelegentlich der USB-Port gewechselt werden |
| Hoher Gewinn / große Distanz + starke Injektion | **AWUS036ACH** | RTL8812AU mit Doppelantenne, Dual-Band-Injektion 100 %, starke Empfangsfähigkeit |
| Leicht und mobil | **AWUS036ACS** | Single-Stream, End-to-End-`.22000` belegt, 5G-Injektion 96 % |
| Wi-Fi-6-Bedarf | **AWUS036AX / AWUS036AXER** | 2x2 VHT80, End-to-End-`.22000` belegt; AXER mit eingebettetem Nano-Antennendesign + Chip-Abstimmung, breiteste Scan-Abdeckung |
| **Unbedingt meiden** | AWUS036AXM / AWUS036AXML | MT7921 schlägt auf dieser Plattform bei der Injektion fehl, keine Handshake-Erfassung möglich |

Fazit in einem Satz: **Für ein WPA3-bezogenes Audit vorrangig EACS, dann ACH / ACS; für Wi-Fi 6 AX / AXER wählen; AXM / AXML unbedingt meiden.** Von den sieben Karten mit abgeschlossener End-to-End-Handshake-Erfassung können alle Realtek-Karten (rtw88 / rtw89) injizieren, auch die MediaTek-Karten ACM und ACHM (mt76) haben es geschafft; die MT7921-Karten AXM / AXML nicht. Bei der Auswahl ist der Chip ein genaueres Kriterium als der Modellname.

## Häufig gestellte Fragen (FAQ)

**F: Kann der AWUS036AXM unter Ubuntu einen WPA-Handshake erfassen?**
A: Auf dieser Plattform nicht. Im Test brach beim AWUS036AXM und AWUS036AXML (MT7921-Chip) wegen fehlgeschlagener Injektion – kein deauth absendbar – die gesamte 4-Way-Handshake-Erfassungskette mit ab, daher sind sie für Zwecke, die eine Handshake-Erfassung erfordern, nicht geeignet.

**F: Welche ALFA-Karte erfasst WPA-Handshakes am zuverlässigsten?**
A: Im Test war der AWUS036EACS am solidesten: Die Injection erreichte in beiden Bändern 100 %, nach dem deauth kamen 79 ACK-Rückmeldungen an, und es wurde erfolgreich eine hashcat-taugliche `.22000`-Datei exportiert – das Modell mit der vollständigsten End-to-End-Verifikation dieser Charge.

**F: Warum verbindet sich ein älteres iPhone nicht mit einem WPA3-SAE-Hotspot?**
A: Entscheidend ist die hostapd-Option `sae_pwe`: Auf 2 gesetzt (erzwungenes H2E) scheitert die Verbindung des iPhone 7 Plus; nach Rückstellung auf `sae_pwe=0` (Hunting-and-Pecking) lässt sich der 4-Way-Handshake normal abschließen und die Verbindung herstellen.

**F: Lässt sich in einer WPA3-Umgebung noch ein 4-Way-Handshake erfassen?**
A: Eine reine WPA3-SAE-Umgebung erzwingt PMF (`ieee80211w=2`), traditionelle Methoden gegen Management-Frames werden blockiert; dass sich in der Praxis dennoch ein Handshake erfassen lässt, liegt meist daran, dass das Ziel im WPA2/WPA3-Übergangsmodus läuft und nicht reines WPA3.

**F: Die 5-GHz-Injection einer ALFA-Karte lässt sich nicht messen – ist das ein Hardwareproblem?**
A: Nicht unbedingt. Die Standard-Regulierungsdomäne begrenzt die Sendeleistung in Teilen der 5-GHz-Bänder, sodass sich die Injektion „nicht hinausbekommen“ lässt; im Test wurde die zuvor fehlgeschlagene 5-GHz-Injektion nutzbar, nachdem die Regulierungsdomäne in einen sendefähigen Zustand geschaltet wurde – es empfiehlt sich, zuerst die Einstellung der Regulierungsdomäne zu prüfen, bevor man auf eine Hardwarebeschränkung schließt.

## 7. Weiterführende Literatur

- [Gesamttabelle und Auswahl-Gesamtbewertung des ARM64-Praxistests von 9 ALFA-WLAN-Karten](/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Einzelkartentests der jeweiligen Modelle: [AWUS036EACS Einzelkartentest](/de/blog/awus036eacs-asus-gx10-ubuntu-test-report/), [AWUS036ACS Einzelkartentest](/de/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*Alle Tests dieses Artikels erfolgten in Yopiteks eigenem Büro-WLAN (SSID YUPITEK) gegen das eigene iPhone 7 Plus und sind eine rechtmäßige Fähigkeitsverifizierung der ALFA-WLAN-Karten durch den Distributor. Die Daten stammen aus den Hardware-Testberichten vom 2026-11-16 bis 11-18, sind gegen kein fremdes Netzwerk gerichtet und liefern keine Angriffsschritte. Testinstanz: Yopitek (ALFA-Network-Distributor Taiwan) — https://www.yupitek.com*
