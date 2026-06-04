---
title: "Beacon Sensor de Movimento YPB02 BLE"
description: "Beacon Sensor de Movimento YPB02 BLE. Bluetooth Low Energy BLE 5.0, para localização, controle de presença e rastreamento."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yupitek", "CR2477", "Waterproof", "Sensor", "Accelerometer"]
---

## Visão geral do produto

O **YPB02** é um beacon Bluetooth® (BLE 5.0) com um **acelerômetro LIS3DH de 3 eixos** integrado. Compartilha a mesma bateria CR2477 e gabinete IP67 do YPB01, mas adiciona telemetria e detecção de movimento.

O beacon pode ser configurado para transmitir dados de aceleração em tempo real ou encurtar o intervalo de sinal apenas quando estiver em movimento ou vibrando.

---

## Principais recursos

* **Sensor de aceleração de 3 eixos:** Sensor LIS3DH que mede movimento e inclinação nos eixos X, Y, Z.
* **Transmissão ativa por gatilhos:** Envia sinal apenas em movimento, dispara alertas de queda ou altera o intervalo para 100 ms ao se mover.
* **Proteção IP67:** Resistente a poeira e imersão em água.
* **Bateria substituível:** Gabinete rotativo permite troca rápida de pilha CR2477.

---

## Gatilho de movimento e telemetria

Através do sensor LIS3DH, o YPB02 suporta:
1. **Sinal baseado em atividade:** Transmite quadros padrão e ativa dados de movimento apenas em deslocamento.
2. **Modo duplo:** Fica em suspensão quando parado e transmite a 100 ms em movimento.
3. **Calibração:** Os limites de sensibilidade podem ser ajustados via app.

---

## Guia de configuração

A configuração é feita sem fio pelo aplicativo **BeaconSET+**:
1. Instale o **BeaconSET+**.
2. Ative o Bluetooth e a localização.
3. Conecte-se após buscar o MAC correspondente.
4. Insira a senha de administrador para salvar os ajustes.

## Technical Specifications

| :--- | :--- | :--- |
| **Chip Model** | nRF52 series | Ultra-low power consumption |
| **Bluetooth Version** | BLE 5.0 | High efficiency and speed |
| **Waterproof Level** | IP67 | Splash and dust resistant (1m immersion) |
| **Sensor** | LIS3DH 3-axis accelerometer | X, Y, Z axes telemetry |
| **Transmission Range** | Up to 100 meters | Open space |
| **Antenna Impedance** | 50 ohm | On-board / PCB Antenna |
| **Power Source** | 1 × CR2477 coin battery | Replaceable (3.0V, 1000mAh) |
| **Operating Voltage** | 1.8V - 3.9V | DC |
| **Peak Current** | 5.3 mA | Tested at 0dBm transmission power |
| **Dimensions** | Φ39 × 15.5 mm | Compact circular shape |
| **Default Settings** | UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms | Configurable via App |

---

## Galeria do produto

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb02.png" alt="Yupitek YPB02" />
{{< /gallery >}}

---

{{< alert >}}
Precisa de um orçamento personalizado ou solução de integração? Entre em contato diretamente com nossa equipe de vendas pelo e-mail: **sales@yupitek.com**
{{< /alert >}}
