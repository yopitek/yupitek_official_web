---
title: "NVIDIA Mellanox LinkX optische Transceiver-Module"
description: "Original NVIDIA Mellanox LinkX optische Transceiver-Module auswählen. Schnelle 25G, 100G, 400G und 800G Transceiver für Multimode- und Singlemode-Netzwerke."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox LinkX optische Transceiver-Module – 25G bis 800G

NVIDIA LinkX® optische Transceiver-Module wurden für die strengen Anforderungen von High-Performance Computing, Enterprise-Storage und Hyperscale-Umgebungen entwickelt. Der Einsatz von Original-Transceivern sorgt für optimale Signalintegrität, niedrigste Bitfehlerraten (BER) und vollständige Kompatibilität mit ConnectX-Adaptern und Quantum-Switches.

---

## Portfolio optischer Transceiver-Module

Nachfolgend finden Sie die aktiven optischen Transceiver-Module aus unserem Sortiment.

<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin: 1.5rem 0;">
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/sfp28-25g-transceiver.jpg" alt="25G SFP28 Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA Mellanox 25G SFP28 SR optisches Transceiver-Modul</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/qsfp28-100g-transceiver.jpg" alt="100G QSFP28 Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA Mellanox 100G QSFP28 SR4 optisches Transceiver-Modul</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/osfp-400g-transceiver.jpg" alt="400G OSFP Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA 400G OSFP NDR optisches Transceiver-Modul</p>
  </div>
</div>

| Artikelnummer | Geschwindigkeit | Schnittstelle | Anschluss | Wellenlänge | Fasertyp | Max. Distanz | Beschreibung |
|-------------|-------|-----------|-----------|------------|------------|--------------|-------------|
| **MMA2P00-AS** | 25G | SFP28 | LC Duplex | 850nm | Multimode (MMF) | 150m (OM4) / 100m (OM3) | 25GbE-SR-Modul |
| **MMA1B00-C100-TG** | 100G | QSFP28 | MPO-12 | 850nm | Multimode (MMF) | 100m (OM4) / 70m (OM3) | 100GbE-SR4-Modul, DDMI |
| **MMA4Z00-NS400** | 400G | OSFP | MPO-12 APC| 850nm | Multimode (MMF) | 50m (OM4) | NDR IB/ETH SR-Modul, Flat Top |
| **MMA4Z00-NS** | 800G | OSFP | 2xMPO-12 APC| 850nm | Multimode (MMF) | 50m (OM4) | 2xNDR Twin-Port SR-Modul, Finned |

---

## Entfernungen & Verkabelung: Leitfaden

### 1. SR vs. SR4 vs. NDR (Multimode-Lösungen)
- **25G SR (SFP28)**: Nutzt ein standardmäßiges LC-LC-Duplex-Multimode-Patchkabel. Die Übertragung und der Empfang erfolgen über einen einzigen Kanal (Lane).
- **100G SR4 (QSFP28)**: Nutzt ein 12-adriges MPO (MPO-12) Bandkabel (üblicherweise mit Polarität Typ B), um die Daten über 4 parallele Kanäle mit je 25G zu übertragen.
- **400G/800G NDR (OSFP)**: Nutzt PAM4-Modulation für extrem hohe Bandbreiten über MPO-12-APC-Stecker (mit Schrägschliff). Das angeschrägte Steckerende minimiert Rückreflexionen, was bei diesen Geschwindigkeiten unverzichtbar ist.

### 2. Singlemode (LR4/FR4) vs. Multimode (SR/SR4)
- **Multimode (MMF)**: Ideal für die Verkabelung innerhalb eines Racks oder für kurze Distanzen zwischen Racks (bis zu 100–150 m). Die Anschaffungskosten für die Transceiver sind geringer.
- **Singlemode (SMF)**: Erforderlich bei Distanzen über 150 m (bis zu 10 km bei LR4). Verwendet Duplex-LC-Stecker auf 9/125 µm Glasfaserkabeln.

---

## Technische Beratung: Original-Hersteller (OEM) vs. Drittanbieter-Module

Beim Kauf von Transceivern stellt sich oft die Frage: *„Kann ich auch kompatible oder umprogrammierte Transceiver von Drittanbietern nutzen?“*

### Warum wir Original-NVIDIA-LinkX empfehlen:
1. **Firmware-Kompatibilität**: NVIDIA ConnectX-NICs und Quantum-Switches nutzen spezielle Betriebssysteme (wie MLNX-OS oder Onyx). System-Updates blockieren oder kennzeichnen Drittanbieter-Module häufig, was zum Deaktivieren des Ports führt (Port Status Down).
2. **Zuverlässige Diagnose (DDM/DOM)**: Original-Module melden Temperatur, Spannung sowie Sende- und Empfangsleistung (TX/RX-Leistung) präzise an die Systemcontroller (iDRAC, HPE iLO oder MLNX-OS). Exakte Werte verhindern Fehlalarme bei der Temperaturüberwachung.
3. **Unterstützung erweiterter Funktionen**: LinkX-Module unterstützen wichtige Features wie die Vorwärtsfehlerkorrektur (Forward Error Correction, FEC) ab Werk. Das verhindert Paketverluste bei hohem Datendurchsatz in anspruchsvollen Datenbank-Workloads.

---

Suchen Sie passende Glasfaser-Patchkabel? Besuchen Sie unseren [Katalog für Glasfaser-Patchkabel](/de/products/mellanox/cable-fiber/). Für individuelle Netzwerkkonzepte können Sie sich direkt an die [Yupitek-Ingenieure wenden](/de/contact/).
