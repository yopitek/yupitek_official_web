---
title: "OpenSourceSDRLab RTL-SDR Blog V4 — Einsteiger-SDR-Empfänger"
description: "RTL-SDR Blog RTL SDR V4, 500kHz–1,766GHz Breitband-SDR-Empfänger, 1PPM TCXO, eingebauter HF-Aufwärtskonverter — die erste Wahl für den Einstieg in die RF-Forschung."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "RTL-SDR", "Radio Reception", "USB", "GNU Radio"]
faq:
  - question: "Benötige ich den Direct-Sampling-Modus, um HF auf dem RTL-SDR Blog V4 zu empfangen?"
    answer: "Nein. Der V4 verfügt über einen integrierten Upconverter anstelle einer Direct-Sampling-Schaltung, daher werden HF-Signale um 28.8 MHz hochgesetzt und der Treiber übernimmt die Frequenzverschiebung. Das Aktivieren des Direct-Sampling-Modus auf einem V4 führt zu keinen Ergebnissen."
  - question: "Benötigt der RTL-SDR Blog V4 spezielle Treiber?"
    answer: "Ja. Der V4 erfordert die RTL-SDR Blog Treiber, die abwärtskompatibel zu V3 und älteren Geräten sind."
  - question: "Wie funktioniert der Bias Tee auf dem RTL-SDR Blog V4?"
    answer: "Der Bias Tee ist softwaregesteuert und für 4.5 V ausgelegt, wobei er bis zu 180 mA kontinuierlich liefert. Unter Linux wird er mit rtl_biast geschaltet."
---

## Funktionen

![RTL-SDR Blog RTL SDR V4](/images/products/sdrlab/rtl-sdr-v4.png)

- R828D-Tuner mit drei Eingängen; ein Triplexer teilt den SMA-Eingang in die Bänder HF, VHF und UHF auf und verbessert die Außerband-Isolation
- Eingebauter HF-Aufwärtskonverter: HF wird um 28,8 MHz hochgesetzt, der Direct-Sampling-Modus ist nicht nötig (untere Abstimmgrenze 500 kHz)
- 1 PPM Temperaturkompensierter Kristalloszillator (TCXO) für deutlich verbesserte Frequenzstabilität
- Softwaregesteuerter Bias-Tee speist externe LNAs oder aktive Antennen
- Schaltbarer Notch-Filter für die Rundfunkbänder AM, FM und DAB reduziert Störungen durch starke Sender
- Leitfähiges schwarzes Metallgehäuse dient als Abschirmung und Kühlkörper, dazu USB-Rauschunterdrückung und verbesserter ESD-Schutz
- Mitgelieferte Mehrzweck-Dipolantenne — sofort einsatzbereit

## Spezifikationen

| Spezifikation | Wert / Beschreibung |
|---------------|---------------------|
| Tuner-Chip | Rafael Micro R828D |
| ADC-Chip | RTL2832U |
| Frequenzbereich | 500 kHz – 1,766 GHz (inkl. HF-Modus) |
| Frequenzgenauigkeit | 1 PPM TCXO |
| RF-Anschluss | SMA |
| Bias-Tee | Softwareaktiviert, max. 4,5 V |
| HF-Empfang | Eingebauter Aufwärtskonverter (HF um 28,8 MHz hochgesetzt; kein Direct Sampling nötig) |
| Gehäuse | Leitfähiges schwarzes Metallgehäuse (Abschirmung und Kühlkörper) |
| Schnittstelle | USB (RTL-SDR Blog Treiber erforderlich) |
| Betriebssystem | Windows, Linux, macOS, Android |
| Zubehör | Dipolantenne-Kit (4× Teleskopantennen (2× 23 cm–1 m, 2× 5–13 cm), 3 m Verlängerungskabel, Stativ, Saugnapfhalterung) |

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

[Offizielle RTL-SDR-Blog-Anleitung zum V4](https://www.rtl-sdr.com/v4/)

**Originalhersteller-Shopseite (OpenSourceSDRLab)**: https://opensourcesdrlab.com/products/rtl-sdr-v4
