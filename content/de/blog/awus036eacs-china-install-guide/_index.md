---
title: "ALFA AWUS036EACS Einrichtungsanleitung für China: Windows-Installation & Linux-Kompatibilität"
description: "Einrichtungsanleitung für den ALFA AWUS036EACS in China. RTL8821CU WiFi 5 + Bluetooth 4.2 Nano-Adapter. Windows-Treiber verfügbar unter files.alfa.com.tw. Unter Linux-Kernel 6.2+ funktioniert der integrierte rtw88_8821cu-Treiber sofort — Monitor-Modus und Injektion getestet und funktionsfähig."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036eacs-china-install-guide"
tags: ["alfa", "awus036eacs", "windows", "driver", "china", "bluetooth", "rtl8821cu"]
categories: ["Treiber-Anleitungen"]
series: ["alfa-china-install-guide"]
related_product: "/de/products/alfa/awus036eacs/"
series_order: 8
featureimage: "/images/blog/awus036eacs-china-install-guide.webp"
faq:
  - question: "Welchen Chip verwendet der AWUS036EACS? Unterstützt er Bluetooth?"
    answer: "Er verwendet den Realtek RTL8821CU-Chip und unterstützt WiFi 5 sowie Bluetooth 4.2."
  - question: "Ist der AWUS036EACS für die Verwendung unter Linux geeignet?"
    answer: "Ja. Unter Linux-Kernel 6.2+ (z. B. Ubuntu 24.04 HWE / Kernel 6.17) ist der rtw88_8821cu-Treiber im Kernel integriert, ohne Kompilierung und sofort einsatzbereit. Wir haben Monitor-Modus und Paket-Injektion mit 100 % auf beiden Bändern (2,4 GHz / 5 GHz) gemessen, inklusive End-to-End-WPA-.22000-Erfassung, und auch Bluetooth wurde erfolgreich getestet."
  - question: "Wie installiert man den Treiber für den AWUS036EACS unter Windows?"
    answer: "Laden Sie das Windows-Treiberpaket von der offiziellen Alfa-Website files.alfa.com.tw herunter, installieren Sie es mit Administratorrechten und starten Sie den Computer neu."
  - question: "Wie aktiviert man Bluetooth beim AWUS036EACS?"
    answer: "Nach der Treiberinstallation wird es in der Regel automatisch aktiviert; Sie können Bluetooth in den Windows-Einstellungen aktivieren, um Geräte zu verbinden."
  - question: "Welche WLAN-Karte für Sicherheitsstudien unter Linux sollten Sie wählen?"
    answer: "Der AWUS036EACS selbst eignet sich auf Kernel 6.2+ für Monitor-Modus und Paket-Injektion, mit Bluetooth als Bonus. Wenn Sie mehr Auswahl möchten, unterstützen auch AWUS036ACM und AWUS036ACS den Monitor-Modus unter Linux vollständig. Nur in Netzwerken verwenden, die Ihnen gehören oder für die Sie eine Freigabe haben."
---

Der AWUS036EACS ist der Nano WiFi 5 + Bluetooth 4.2 Kombi-Adapter von ALFA. Er ist ein kompaktes drahtloses Upgrade für Windows-Benutzer, und unter Linux-Kernel 6.2+ unterstützt ihn der integrierte rtw88_8821cu-Treiber sofort — ohne Kompilierung. Diese Anleitung deckt die Windows-Installation aus chinesischen Quellen ab und erläutert die Nutzung unter Linux.

{{< tldr >}}
Der AWUS036EACS verwendet den RTL8821CU-Chip, eine Mini-WLAN-Karte mit WiFi 5 und Bluetooth 4.2, die unter Windows einfach zu installieren ist; unter Linux-Kernel 6.2+ ist der rtw88_8821cu-Treiber integriert, sodass Monitor-Modus und Paket-Injektion sofort funktionieren und auch Bluetooth getestet und funktionsfähig ist.
{{< /tldr >}}

> **Der AWUS036EACS funktioniert unter Linux-Kernel 6.2+ sofort.** Kernel 6.2 und neuer (z. B. Ubuntu 24.04 HWE / Kernel 6.17) enthalten den integrierten rtw88_8821cu-Treiber, sodass keine Kompilierung nötig ist. Wir haben Monitor-Modus und Paket-Injektion mit 100 % auf beiden Bändern (2,4 GHz / 5 GHz) gemessen, einen WPA-Handshake End-to-End erfasst (.22000), und auch Bluetooth (BT) ist getestet und funktionsfähig (BR/EDR + BLE scannen beide Geräte und koexistieren mit WiFi). Nur in Netzwerken verwenden, die Ihnen gehören oder für die Sie eine Freigabe haben.
>
> **Betriebshinweis:** Dies ist eine BT+WiFi-Kombikarte. Nach wiederholtem Moduswechsel kann der WiFi-Empfang hängen bleiben (`ip link set up` gibt `Operation already in progress` zurück und `iw ... set channel` gibt `-16 busy` zurück). Ziehen Sie den Adapter vor jeder Testphase ab und stecken Sie ihn in einen anderen USB-Anschluss, um ihn zurückzusetzen.
>
> Weitere Linux-Adapter derselben Serie:
> - **[AWUS036ACM](/de/blog/awus036acm-china-install-guide/)** — MT7612U In-Kernel-Treiber, voller Monitor-Modus + VIF
> - **[AWUS036ACS](/de/blog/awus036acs-china-install-guide/)** — RTL8811AU, preisgünstiger Monitor-Modus


## Linux-Benutzer: Bitte zuerst lesen

> **Der AWUS036EACS funktioniert unter Linux-Kernel 6.2+ sofort.** Kernel 6.2 und neuer (z. B. Ubuntu 24.04 HWE / Kernel 6.17) enthalten den integrierten rtw88_8821cu-Treiber, sodass keine Kompilierung nötig ist. Wir haben Monitor-Modus und Paket-Injektion mit 100 % auf beiden Bändern (2,4 GHz / 5 GHz) gemessen, einen WPA-Handshake End-to-End erfasst (.22000), und auch Bluetooth (BT) ist getestet und funktionsfähig (BR/EDR + BLE scannen beide Geräte und koexistieren mit WiFi). Nur in Netzwerken verwenden, die Ihnen gehören oder für die Sie eine Freigabe haben.
>
> **Betriebshinweis:** Dies ist eine BT+WiFi-Kombikarte. Nach wiederholtem Moduswechsel kann der WiFi-Empfang hängen bleiben (`ip link set up` gibt `Operation already in progress` zurück und `iw ... set channel` gibt `-16 busy` zurück). Ziehen Sie den Adapter vor jeder Testphase ab und stecken Sie ihn in einen anderen USB-Anschluss, um ihn zurückzusetzen.
>
> Weitere Linux-Adapter derselben Serie:
> - **[AWUS036ACM](/de/blog/awus036acm-china-install-guide/)** — MT7612U In-Kernel-Treiber, voller Monitor-Modus + VIF
> - **[AWUS036ACS](/de/blog/awus036acs-china-install-guide/)** — RTL8811AU, preisgünstiger Monitor-Modus

---

## Windows 10 / 11 Einrichtung

### Schritt 1: Treiber von Alfa herunterladen

Der offizielle Alfa-Treiber-Server ist von China aus erreichbar:

https://files.alfa.com.tw

Navigieren Sie zum Produktordner **AWUS036EACS** und laden Sie das Windows-Treiberpaket herunter (`.zip` oder `.exe`).

### Schritt 2: Treiber installieren

1. Entpacken Sie die heruntergeladene Zip-Datei.
2. Klicken Sie mit der rechten Maustaste auf den Installer `.exe` und wählen Sie **Als Administrator ausführen**.
3. Folgen Sie den Anweisungen auf dem Bildschirm.
4. Starten Sie neu, wenn Sie dazu aufgefordert werden.

---

## Details zur Linux-Kompatibilität

Unter **Kernel 6.2+** wird der RTL8821CU vom integrierten Modul `rtw88_8821cu` angesteuert, es muss also nichts kompiliert werden — einstecken und er wird erkannt. Prüfen Sie Ihre Kernel-Version zuerst mit `uname -r`.

### Kali Linux

Mit einem 6.2+-Kernel wird der integrierte `rtw88_8821cu`-Treiber automatisch geladen. Wir haben Monitor-Modus und Paket-Injektion mit 100 % auf beiden Bändern (2,4 GHz / 5 GHz) getestet und einen WPA-Handshake End-to-End erfasst (.22000). Nur in Netzwerken verwenden, die Ihnen gehören oder für die Sie eine Freigabe haben.

```bash
sudo nmcli dev set wlxXXXX managed no
sudo ip link set wlxXXXX down
sudo iw dev wlxXXXX set type monitor
sudo ip link set wlxXXXX up
```

### Ubuntu / Debian / Raspberry Pi

Sobald der Kernel 6.2 oder neuer ist (einschließlich ARM64-Builds wie beim Raspberry Pi), übernimmt der integrierte `rtw88_8821cu`-Treiber den Adapter ohne Kompilierung. Auf einem älteren Kernel aktualisieren Sie auf den HWE-Kernel, um den integrierten Treiber zu erhalten.

### Betriebshinweis (BT+WiFi-Kombikarte)

Da der EACS Bluetooth und WiFi auf einem Chip vereint, kann wiederholter Moduswechsel den WiFi-Empfang blockieren — `ip link set up` gibt `Operation already in progress` zurück und `iw ... set channel` gibt `-16 busy` zurück. Ziehen Sie den Adapter vor jeder Testphase ab und stecken Sie ihn in einen anderen USB-Anschluss, um den Zustand zu löschen. Bluetooth (BR/EDR + BLE) ist getestet, funktionsfähig und koexistiert mit WiFi.

---

## China Mirror Referenz

| Ressource | URL | Verwendung für |
|----------|-----|---------|
| Offizielle Alfa Treiber | [files.alfa.com.tw](https://files.alfa.com.tw) | EACS Windows-Treiber |

---

{{< faq >}}

## Weitere Alfa Adapter Anleitungen für China

- [AWUS036ACH China Install Guide](/de/blog/awus036ach-china-install-guide/) — RTL8812AU, High Power
- AWUS036EACS ← Sie sind hier

Fragen? Hinterlassen Sie unten einen Kommentar oder kontaktieren Sie uns auf [yupitek.com](https://yupitek.com/de/contact/).

## Referenzen

1. [ALFA Network Offizielle Website](https://www.alfa.com.tw/)
2. [Alfa OffizielleTreiber-Download](https://files.alfa.com.tw)
3. [Realtek Offizielle Website](https://www.realtek.com/)
