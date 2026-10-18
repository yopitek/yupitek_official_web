---
title: "Flipper Zero 5G Expansion Board Installations- und Benutzerhandbuch (v2.0)"
description: "Dieses Handbuch führt dich Schritt für Schritt durch die Installation und Einrichtung des Flipper Zero 5G Erweiterungsmoduls v2.0. Mit klaren isometrischen Konstruktionszeichnungen gelingt dir die Montage von Antennen, Slots und GPIO-Einstellungen spielend leicht."
date: 2026-10-18
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-zero-5g-expansion-board-user-manual"
tags: ["Flipper Zero", "5G Expansion Board", "SDRLab", "Tutorial"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-10-18
featureimage: "/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg"
hideFeatureImage: true
---

# Flipper Zero 5G Expansion Board Installations- und Benutzerhandbuch (v2.0)

> **Zielgruppe**: Einsteiger, die dieses Modul zum ersten Mal verwenden.  
> **Konzept**: Wir bieten dir für alle fehleranfälligen oder technisch komplexen Schritte hochauflösende Zeichnungen. So musst du nicht raten und installierst alles Schritt für Schritt völlig unkompliziert.

---

## 00. Auspacken und Lieferumfang

Willkommen bei deinem Flipper Zero 5G Erweiterungsmodul! Bevor du startest, überprüfe bitte, ob alle folgenden Teile in deiner Verpackung enthalten sind.

![Lieferumfang und Komponenten](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg)
*Bild 1: Lieferumfang im Überblick*

### ⚠️ Hinweise zum Lieferumfang
*   **Standardmäßig enthalten**:
    1.  5G Expansion Board Hauptmodul x 1
    2.  433MHz-Stabantenne (kurze schwarze Antenne) x 1
    3.  Aktive GPS-Keramikantenne (quadratische Antenne) x 1
    4.  WiFi-Dualband-Patchantenne (flache schwarze Antenne) x 1
*   **Nicht enthalten (musst du selbst vorbereiten)**:
    *   **Flipper Zero Hauptgerät** (das Hauptgerät ist nicht im Lieferumfang enthalten)
    *   **MicroSD-Karte** (für den Betrieb des Moduls zwingend erforderlich, muss separat erworben werden)

---

## 01. Lerne dein 5G-Modul kennen

Nimm dir eine Minute Zeit, um dich mit den Anschlüssen und dem Hardware-Layout des Moduls vertraut zu machen, bevor du Antennen anschließt oder das Modul mit dem Hauptgerät verbindest.

### Schnittstellen auf der Vorderseite

![Vorderseite des Moduls](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_02_front_interface.jpg)
*Bild 2: Hardware-Layout auf der Vorderseite*

*   **Display (LCD-Bildschirm)**: Zeigt den aktuellen Verbindungsstatus, die IP-Adresse und den Betriebsmodus an.
*   **Kippschalter (Toggle Switch)**: Steuert die Stromversorgung des Modul-Bildschirms. Schiebe ihn nach oben, um das Display einzuschalten.
*   **MicroSD-Kartenslot (SD Card Slot)**: Hier steckst du die Speicherkarte für Firmware-Einstellungen und Protokolldaten ein.
*   **GPIO-Stecker**: Die Buchsenleiste, die mit den GPIO-Pins auf der Oberseite des Flipper Zero verbunden wird.
*   **Status-LEDs (LED Indicators)**: Zeigen den Strom- und Ladestatus an.

### Antennenanschlüsse an der Seite

![Seitliche Antennenanschlüsse](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_03_antenna_ports.jpg)
*Bild 3: Positionen und Beschriftungen der Antennenanschlüsse*

*   **433M A**: Anschluss für die 433MHz-Stabantenne.
*   **GPS**: Anschluss für die GPS-Keramikantenne.
*   **2.4G** und **2.4G/5G**: Anschlüsse für die WiFi-Dualband-Patchantenne.

> ⚠️ **Wichtiger Hinweis zu den Produktionschargen**:  
> Die Positionen der Antennenanschlüsse können je nach Produktionscharge leicht variieren. Beispielsweise können die GPS- und WiFi-Anschlüsse vertauscht sein. **Richte dich daher immer nach der aufgedruckten Beschriftung auf dem Gehäuse deines Moduls**. Schließe die Antennen nicht blind an, um Empfangsprobleme oder Hardwareschäden zu vermeiden.

---

## 02. Installationsanleitung (Step-by-Step)

### Schritt 1 | MicroSD-Karte vorbereiten und einsetzen

Das 5G-Modul benötigt eine Speicherkarte, um Einstellungen zu sichern.

1.  **Anforderungen**: Kapazität **bis zu 32 GB**, Dateisystem muss **FAT32** sein.
2.  **Ausrichtung**: Schiebe die MicroSD-Karte mit den Goldkontakten nach unten in den Kartenslot, bis sie spürbar einrastet.

![Detailaufnahme des MicroSD-Kartenslots](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_07_sd_card_slot.jpg)
*Bild 4: Korrekte Ausrichtung beim Einsetzen der MicroSD-Karte*

---

### Schritt 2 | Die drei Antennen montieren

Schraube die drei mitgelieferten Antennen auf die passenden SMA-Anschlüsse. Wende dabei keine übermäßige Kraft an, sondern ziehe sie nur handfest an.

![Antennen-Anschlussplan](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_08_three_antenna_connection.jpg)
*Bild 5: Zuordnung und Anschlusswege der drei Antennen*

| Antennentyp | Passender Anschluss | Montagehinweis |
| :--- | :--- | :--- |
| **GPS-Keramikantenne** | **GPS-Port** | Quadratischer Keramikkopf mit langem Kabel |
| **WiFi-Dualband-Patchantenne** | **2.4G/5G-Port** | Flache, schwarze Patchantenne |
| **433MHz-Stabantenne** | **433M A-Port** | Kurze, starre Stabantenne |

#### ⚠️ Warnung zur Ausrichtung der GPS-Antenne
Die GPS-Antenne empfängt Signale richtungsabhängig. Bei der Montage **muss die Keramikseite (die Seite gegenüber dem doppelseitigen Klebeband) nach oben zum Himmel zeigen**. Andernfalls kann das Modul keine Verbindung zu den Satelliten aufbauen!

![Ausrichtung der GPS-Antenne im Vergleich](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_09_gps_antenna_orientation.jpg)
*Bild 6: Richtige (zum Himmel) und falsche (zum Boden) Ausrichtung der GPS-Antenne*

---

### Schritt 3 | Verbindung mit dem Flipper Zero herstellen

Stecke das 5G-Modul auf die GPIO-Pins an der Oberseite des Flipper Zero.

1.  **Schalte deinen Flipper Zero zuerst aus**, um Hardwareschäden durch Hot-Plugging zu vermeiden.
2.  Richte die GPIO-Pins des Flipper Zero genau an den Buchsen auf der Unterseite des Moduls aus.

![Ausrichtung der GPIO-Verbindung](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_10_gpio_alignment.jpg)
*Bild 7: Positionierung und Ausrichtung der GPIO-Pins*

3.  Drücke das Modul mit gleichmäßigem Druck auf beiden Seiten **vollständig nach unten**.
4.  **Sitz überprüfen**: Betrachte die Verbindung von der Seite. Das Modul muss **plan und ohne sichtbare Lücke** auf dem Flipper Zero aufliegen.

![Überprüfung des GPIO-Sitzes](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_19_gpio_insertion_flat.jpg)
*Bild 8: Korrekt sitzendes Modul ohne Spaltmaß*

---

### Schritt 4 | Software-Einstellungen auf dem Flipper Zero

Schalte den Flipper Zero nach dem Aufstecken wieder ein und konfiguriere die GPIO-Pins in der Software.

Hier zeigen wir dir die Einstellungen am Beispiel der **Momentum-Firmware**:

1.  **Display einschalten**: Schiebe den Kippschalter vorne links am Modul in die Position **UP**.
    ![Kippschalter in Position UP](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_16_toggle_switch_up.jpg)
    *Bild 9: Schalter nach oben umlegen, um die Anzeige zu aktivieren*

2.  **GPS-Pin einstellen**:
    *   Pfad: `Protocol Settings` ➔ `GPIO Pin Settings` ➔ `GPS Pin`
    *   Wert: Ändere den Wert auf **13** oder **14** (je nach beiliegender Anleitung oder Hardwareversion).
3.  **ESP32-Pin einstellen (WiFi/Bluetooth)**:
    *   Pfad: `Protocol Settings` ➔ `GPIO Pin Settings` ➔ `ESP32 Pin`
    *   Wert: Ändere den Wert auf **15, 16**.
4.  **433MHz-Funkmodul konfigurieren**:
    *   Gehe zu `Sub-GHz` ➔ `Advanced Settings` ➔ Ändere Module auf **External** (aktiviert die externe Antenne).

---

### Schritt 5 | Laden und Akkustand prüfen

Dieses Modul besitzt einen eingebauten Akku.

![Vergleich der USB-C-Anschlüsse](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_17_usb_ports_comparison.jpg)
*Bild 10: Ladeanschluss (CHARGE ONLY) oben im Vergleich zum Flash-Anschluss (FLASH ONLY) an der Seite*

*   **Oberer USB-C-Anschluss**: **Nur zum Laden gedacht** (gekennzeichnet mit CHARGE ONLY). Nutze bitte ausschließlich diesen Anschluss zum Aufladen des Akkus.
*   **Seitlicher USB-C-Anschluss**: **Nur für Firmware-Updates gedacht** (gekennzeichnet mit FLASH ONLY). Lade das Modul nicht über diesen Port auf, da der Akku sonst keinen Strom erhält.

#### Bedeutung der Akku-LEDs:
Auf der Vorderseite des Moduls befinden sich vier LEDs, die dir den Ladestand anzeigen:

![Akkustands-LEDs](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_18_battery_led_indicators.jpg)
*Bild 11: Ladestand entsprechend der leuchtenden LEDs*

*   1 LED leuchtet: Ladestand ca. 25% (bitte bald aufladen)
*   2 LEDs leuchten: Ladestand ca. 50%
*   3 LEDs leuchten: Ladestand ca. 75%
*   4 LEDs leuchten: Ladestand 100% (vollständig geladen)

---

## 03. Checkliste bei Problemen (Fehlersuche für Einsteiger)

Falls dein Modul nicht wie gewünscht funktioniert, gehe bitte diese Punkte nacheinander durch:

*   [ ] **Sind die GPIO-Pins vollständig eingesteckt?** (Das Modul muss bündig auf dem Flipper Zero aufliegen, siehe Bild 8)
*   [ ] **Zeigt die GPS-Antenne in die richtige Richtung?** (Die Keramikseite muss zum Himmel zeigen, siehe Bild 6)
*   [ ] **Sind die Antennen am richtigen Port angeschlossen?** (Die Port-Positionen können sich je nach Produktionsreihe unterscheiden. Vergleiche die Anschlüsse mit den Gehäuseaufdrucken, siehe Bild 3)
*   [ ] **Passt die MicroSD-Karte?** (Maximal 32 GB Kapazität, FAT32-Formatierung erforderlich, siehe Bild 4)
*   [ ] **Steht der Display-Schalter auf UP?** (Siehe Bild 9)

---

## 04. Firmware-Updates (Erweiterte Funktionen)

Wenn eine neue Firmware-Version erscheint, kannst du das Modul über den seitlichen USB-C-Anschluss aktualisieren.

1.  Verbinde das Modul über ein USB-C-Kabel mit deinem Computer.
2.  **Wichtige Reihenfolge**: Halte den Flash-Knopf auf der Rückseite oder rechten Seite des Moduls gedrückt, während du das Kabel in den **seitlichen USB-C-Anschluss (FLASH ONLY)** steckst. Dadurch wechselt der Chip in den Bootloader-Modus.

![Ablauf beim Firmware-Flash](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_20_boot_flash_sequence.jpg)
*Bild 12: Boot-Knopf gedrückt halten und gleichzeitig das USB-Kabel anschließen*
