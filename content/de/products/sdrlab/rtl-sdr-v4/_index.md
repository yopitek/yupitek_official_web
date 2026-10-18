---
title: "OpenSourceSDRLab RTL-SDR Blog V4 — Einsteiger-SDR-Empfänger"
description: "RTL-SDR Blog RTL SDR V4, 500kHz–1,7GHz Breitband-SDR-Empfänger, 1PPM TCXO, eingebauter HF-Aufwärtskonverter, USB 2.0 — die erste Wahl für den Einstieg in die RF-Forschung."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "RTL-SDR", "Radio Reception", "USB", "GNU Radio"]
faq:
  - question: "Benötige ich den Direct-Sampling-Modus, um HF auf dem RTL-SDR Blog V4 zu empfangen?"
    answer: "Nein. Der V4 verfügt über einen integrierten Upconverter anstelle einer Direct-Sampling-Schaltung, daher werden HF-Signale um 28.8 MHz hochgesetzt und der Treiber übernimmt die Frequenzverschiebung. Das Aktivieren des Direct-Sampling-Modus auf einem V4 führt zu keinen Ergebnissen."
  - question: "Benötigt der RTL-SDR Blog V4 spezielle Treiber?"
    answer: "Ja. Der V4 erfordert die RTL-SDR Blog Treiber, die abwärtskompatibel zu V3 und älteren Geräten sind. Der Standard-Osmocom-Zweig unterstützt nun ebenfalls den V4."
  - question: "Wie funktioniert der Bias Tee auf dem RTL-SDR Blog V4?"
    answer: "Der Bias Tee ist softwaregesteuert und für 4.5 V ausgelegt, wobei er bis zu 180 mA kontinuierlich liefert. Unter Linux wird er mit rtl_biast geschaltet. Aktivieren Sie ihn nicht mit einer DC-kurzgeschlossenen Antenne, es sei denn, ein LNA oder ein stromversorgtes Gerät ist in der Kette vorhanden."
---

## Funktionen

![RTL-SDR Blog RTL SDR V4](/images/products/sdrlab/rtl-sdr-v4.png)

- Verbesserter R828D-Tuner liefert niedrigeres Rauschen und bessere Empfindlichkeit im Vergleich zum vorherigen R820T/R860
- Eingebauter Aufwärtskonverter ermöglicht HF-Empfang bis hinunter zu 500 kHz (Standard-RTL-SDR-Dongles starten bei 24 MHz)
- 1 PPM Temperaturkompensierter Kristalloszillator (TCXO) für deutlich verbesserte Frequenzstabilität
- Softwaregesteuerter Bias-Tee speist externe LNAs oder aktive Antennen
- Triple-Notch-Frontend-Filter unterdrückt effektiv Rundfunk FM/AM/DAB-Störungen
- Neu gestaltetes rauscharmes PCB mit verbessertem ESD-Schutz und passivgekühltem Aluminiumgehäuse
- Mitgelieferte Mehrzweck-Dipolantenne — sofort einsatzbereit

## Spezifikationen

| Spezifikation | Wert / Beschreibung |
|---------------|---------------------|
| Tuner-Chip | Rafael Micro R828D |
| ADC-Chip | RTL2832U |
| Frequenzbereich | 500 kHz – 1,7 GHz (inkl. HF-Modus) |
| Maximale Bandbreite | 3,2 MHz (stabil bei 2,4 MHz) |
| ADC-Auflösung | 8-bit |
| Frequenzgenauigkeit | 1 PPM TCXO |
| RF-Anschluss | SMA Female (F) |
| Bias-Tee | Softwareaktiviert, max. 4,5 V |
| HF-Empfang | Eingebauter Aufwärtskonverter mit 28,8-MHz-Tiefpassfilter |
| Gehäuse | Aluminiumlegierung, passivgekühlt |
| Schnittstelle | USB 2.0 (RTL-SDR Blog Treiber erforderlich) |
| Betriebssystem | Windows, Linux, macOS, Android |
| Zubehör | Dipolantenne-Kit (2× Teleskopantennen, 3 m Verlängerungskabel, Stativ, Saugnapfhalterung) |

## Anwendungsfälle

- ADS-B Flugzeug-Tracking
- Maritimes AIS-Schiffsmonitoring
- NOAA / Meteor M2 Wettersatelliten-Bildempfang
- Amateurfunk (HF/VHF/UHF Empfang)
- Radioastronomie (Wasserstofflinie-Beobachtung)
- P25 und MotoTRBO digitale Sprachdekodierung
- APRS und ACARS Paket-Tracking
- DAB-Digitalradio-Empfang
- RF-Spektrum-Monitoring und Sicherheitsforschung

---

{{< alert >}}
Benötigen Sie ein Produktangebot? Bitte [kontaktieren Sie uns](/de/contact/).
{{< /alert >}}

{{< faq >}}

[Einrichtungsanleitungen und technische Details — doc.yupitek.com](https://doc.yupitek.com/sdrlab/hardware/rtl-sdr-v4/)
