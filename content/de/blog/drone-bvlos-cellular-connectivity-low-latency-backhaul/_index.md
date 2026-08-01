---
title: "BVLOS-Konnektivität für Drohnen und Inspektionsroboter: So baust du ein Backhaul mit niedriger Latenz | Yupitek"
description: "Wie verbindest du eine Drohne außerhalb der Sichtlinie (BVLOS)? Dieser Artikel vergleicht Sierra EM9190, EM9191 und EM7565: 5G-SA-Architektur mit niedriger Latenz, Video-Upload und Dualband-Positionierung L1/L5 werden analysiert, damit du eine unterbrechungsfreie Lösung für Inspektionsroboter und Drohnen baust."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "de"
hreflang_group: "drone-bvlos-cellular-connectivity-low-latency-backhaul"
slug: "drone-bvlos-cellular-connectivity-low-latency-backhaul"
tags: ["Sierra Wireless", "EM9190", "EM9191", "EM7565", "Drohnen", "BVLOS", "5G", "niedrige Latenz", "GNSS", "LTE"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/de/products/sierra/"
faq:
  - question: "Warum braucht eine Drohne bei BVLOS zwingend eine zellulare Verbindung?"
    answer: "Sobald die Drohne außerhalb der Sichtlinie fliegt, bricht das Funksignal des Controllers ab. Dann ist das 4G/5G-Netz die einzige Lösung, die breite Abdeckung, Steuerung mit niedriger Latenz und Videoübertragung mit hoher Bandbreite bietet."
  - question: "Was ist der Unterschied zwischen EM9190 und EM9191?"
    answer: "Der EM9190 unterstützt zusätzlich 5G-Millimeterwellen (mmWave), benötigt aber sehr stromhungrige und platzraubende Array-Antennen. In Regionen ohne Millimeterwellen-Netz ist der reine 5G-Sub-6-Modul EM9191 die beste Wahl."
  - question: "Welches Modul passt zu einem Inspektionsroboter?"
    answer: "Für die Inspektion eines Werksgeländes reicht meist die Übertragung von normalem Video: Der 4G-Modul EM7565 (Cat 12, Upload 150 Mbit/s) erfüllt die Anforderungen und kostet weniger."
---

Wenn eine Drohne oder ein Roboter deiner Sichtlinie entkommt (das nennt man BVLOS, Beyond Visual Line of Sight), wird dein herkömmlicher Funkcontroller nutzlos. Dann bleibt dem Gerät nur noch die 4G/5G-Netzwerkkarte an Bord: Sie verbindet sich mit der Basisstation, überträgt das hochauflösende Video zurück und empfängt die Befehle von deinem Joystick.

{{< tldr >}}
Nach dem Verlassen der Sichtlinie (BVLOS) nützt der Funkcontroller nichts mehr, und 4G/5G wird zur einzigen Lebensader: Videoübertragung, Steuerbefehle und Koordinaten. Wir zerlegen EM9190, EM9191 und EM7565 und zeigen dir, welche Geheimnisse für niedrige Latenz und präzise L1+L5-Positionierung in den offiziellen Spezifikationen stecken.
{{< /tldr >}}

**Kurz gesagt: Damit eine Drohne außerhalb der Sichtlinie fliegen kann, brauchst du ein 4G/5G-Modul, das „Videoübertragung, Fernsteuerung und Ortung“ gleichzeitig erledigt. Wenn deine Drohne an ein 5G-Privatnetz angebunden werden soll, maximale Videoübertragung und Dualband-Ortung L1+L5 mit höchster Präzision braucht, nimm den EM9191. Wenn es nur ein langsam auf dem Werksgelände kriechender Inspektionsroboter ist, reicht der günstige und zuverlässige 4G-Modul EM7565 völlig aus.**

In diesem Artikel nehmen wir die offiziellen Spezifikationen von Sierra Wireless zur Hand und lüften für dich das Geheimnis: Warum eignen sich diese Module besonders gut für Drohnen und Roboter? Wie schaffen sie die niedrige Latenz?

> Quelle der technischen Daten: offizielle Spezifikationen von Sierra Wireless (EM9190/EM9191, EM7565). Artikel zusammengestellt von Yupitek.

---

## Schnellauswahl in 30 Sekunden: Welches Modul in die Drohne / den Roboter?

| Einsatzszenario | Empfohlenes Modul | Warum gerade das? |
|---|---|---|
| **Top-Drohne (braucht 5G-Privatnetz)** | **EM9191** | Unterstützt 5G Sub-6 und die 5G-SA-Architektur für private Netze, hat die Top-Upload-Geschwindigkeit von LTE Cat 20 und eingebautes hochpräzises L1+L5-Positioning. |
| **Top-Drohne (US-Markt)** | **EM9190** | Der große Bruder des EM9191, unterstützt zusätzlich Millimeterwellen (mmWave). In Taiwan aber unnötig. |
| **Inspektionsroboter auf dem Werksgelände (am Boden)** | **EM7565** | Das ist ein 4G-Cat-12-Modul: leicht und stromsparend. Für die Werksinspektion ist 5G wie mit Kanonen auf Spatzen zu schießen, da ist es am wirtschaftlichsten. |

---

## Wie entsteht die niedrige Latenz? Die Geheimnisse in den Spezifikationen

Gamer wissen, wie wichtig der Ping (Latenz) ist. Für eine Drohne am Himmel kann Latenz über Leben und Tod entscheiden. In den Spezifikationen steht zwar nicht „Latenz in Millisekunden“, aber es gibt drei Waffen, die die Latenz massiv senken:

1. **5G-SA-Architektur (Standalone)**: Die EM919x unterstützen die SA-Architektur (Option 2). Das heißt: Die Drohne verbindet sich direkt mit dem 5G-Kernnetz, ohne Umweg über alte 4G-Basisstationen. Das ist der stärkste Hebel gegen Latenz.
2. **Prioritätssteuerung mit QoS QCI**: Das Modul unterstützt QoS-Einstellungen nach 3GPP R15. Du kannst festlegen, dass „Flugsteuerbefehle“ eine höhere Priorität haben als „Videoübertragung“. Selbst wenn das Netz überlastet ist, verliert das Gerät nicht die Kontrolle.
3. **Uplink Carrier Aggregation (UL CA) und 256QAM**: Video-Backhaul hängt komplett von der Upload-Geschwindigkeit ab. Sowohl die EM919x als auch der EM7565 können mehrere Frequenzbänder beim Upload bündeln und nutzen die fortschrittliche Modulation 256QAM (EM919x) bzw. 64QAM (EM7565), damit das Videobild flüssig und ohne Ruckeln läuft.

---

## Drohne vs. Inspektionsroboter: völlig andere Auswahllogik

Was am Himmel fliegt und was am Boden fährt, stellt ganz unterschiedliche Anforderungen an die Netzwerkkarte.

### Drohne (Drone): extrem empfindlich bei Gewicht, Wärme und Ortung
- **Gewicht ist Flugzeit**: Der EM9191 ist 52 mm lang und wiegt 9 Gramm; der EM7565 ist 42 mm lang und wiegt 6.5 Gramm.
- **Ortungsgenauigkeit**: Drohnen hängen stark vom GPS ab. Die EM919x haben **Dualband-GNSS L1 + L5** eingebaut, das deutlich genauer ist als herkömmliches Singleband-GPS und gut gegen Störungen gewappnet ist.
- **Antennenzahl**: Die EM919x brauchen alle 4 Antennen, um das MIMO-Potenzial auszuschöpfen. Beim Design des Drohnengehäuses musst du Platz für diese 4 Antennen einplanen. Wählst du den EM9190 mit zusätzlichen Millimeterwellen-Antennen, werden Gewicht und Stromverbrauch noch heftiger.

### Inspektionsroboter (Robot): empfindlich bei Stabilität und Kosten
- Der Roboter fährt langsam am Boden, baut die Karte meist mit einem Lidar (LiDAR) auf und ist nicht so tief vom GPS abhängig. Das eingebaute Singleband-GPS des EM7565 reicht völlig.
- Im Bauch des Roboters ist viel Platz und eine große Batterie, aber auf dem Werksgelände gibt es meist nur 4G-Empfang. Da reicht der EM7565 (Cat 12, Upload 150 Mbit/s) locker, da musst du nicht unbedingt auf 5G gehen.

---

## Hardware-Fallen, die du vor dem Einbau beachten musst

Wenn du Hardware-Integrationsingenieur bist: Bevor du das Modul auf die Platine designst, achte auf Folgendes:

1. **Lass dich nicht von mmWave (Millimeterwellen) blenden**: Viele denken, für 5G müsse man den Top-EM9190 mit Millimeterwellen kaufen. Tatsächlich durchdringen Millimeterwellen Hindernisse extrem schlecht, und in Taiwan gibt es praktisch keine mmWave-Privatnetze. Für 99% der Drohnen ist der **EM9191** mit Sub-6-Unterstützung die perfekte Wahl, und er erspart dir einen Haufen Ärger mit externen Antennen.
2. **Pass auf Überhitzung auf**: Die EM919x sind 5G-Giganten, die rote Linie für die Innentemperatur liegt bei 115°C (empfohlen: unter 100°C halten). Wenn eine Drohne im Sommer in der Höhe in der Sonne fliegt und das Modul in einem Kunststoffgehäuse ohne Luftzirkulation steckt, wird es garantiert drosseln oder sogar die Verbindung verlieren.
3. **Spare nicht an Antennenkabeln**: Die Spezifikation verlangt einen Kabelverlust von höchstens 0.5 dB bei 50 Ohm Impedanz. Wer ein Top-Modul kauft, es aber mit Billigkabeln vom Markt verbindet, bekommt nur eine erbärmliche Videoqualität.

## Fazit

Für eine Verbindung außerhalb der Sichtlinie (BVLOS) haben die Sierra-Wireless-Module bereits „Video-Bandbreite, Low-Latency-Architektur und hochpräzise Ortung“ in eine kleine M.2-Karte gepackt.
Fliegst du in der Luft, hast das Budget und willst ans 5G-Privatnetz: Nimm direkt den **EM9191**. Fährst du am Boden und brauchst nur stabiles 1080p-Video: Am entspanntesten ist der **EM7565**.

## Wo kaufen (Call To Action)

Designst du gerade eine Kommunikationsplatine für eine Drohne oder einen Inspektionsroboter? Weißt du nicht, wie du Antennen und Kühlung planen sollst? Yupitek bietet das komplette Sortiment an Sierra-Wireless-Modulen und Beratung für die Hardware-Integration.
Schreib uns: **sales@yupitek.com**
Produkte ansehen: [Sierra Wireless](https://yupitek.com/de/products/sierra/)

{{< faq >}}
