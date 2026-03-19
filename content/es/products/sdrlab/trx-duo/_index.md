---
title: "SDRLab TRX-duo — Plataforma SDR ZYNQ de Doble Canal y 16-bit"
description: "SDRLab TRX-duo, plataforma SDR ADC/DAC de 16-bit y doble canal, Xilinx Zynq 7010 SoC, compatible con Red Pitaya, muestreo directo 10kHz–60MHz, ideal para investigación avanzada de comunicaciones HF."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "TRX-duo", "ZYNQ", "Red Pitaya", "ADC 16-bit"]
---
## Características
![SDRLab TRX-duo](/images/products/sdrlab/trx-duo.png)
- Diseño transceptor de doble canal (2 RX + 2 TX), compatible con el ecosistema de software de Red Pitaya
- Equipado con 2× LTC2208 ADC de alta precisión de 16-bit para alto rango dinámico y alta sensibilidad
- DAC de 14-bit para transmisión en doble canal
- Xilinx Zynq 7010 SoC integrado (ARM Cortex-A9 de doble núcleo + FPGA) que permite ejecutar software de decodificación directamente en el dispositivo
- Compatible con despliegue remoto en red para configurar estaciones receptoras SDR remotas
- Compatible con los principales softwares: HDSDR, SDR#, PowerSDR, SDR Console V3
- Precio aproximadamente la mitad del SDRlab 122-16 oficial de Red Pitaya (aprox. USD $622)

## Especificaciones
| Especificación | Valor / Descripción |
|----------------|---------------------|
| Procesador | ARM Cortex-A9 de doble núcleo (Zynq 7010 SoC) |
| FPGA | Xilinx Zynq 7010 |
| Memoria (RAM) | 512 MB |
| Rango de frecuencia de recepción | 10 kHz – 60 MHz (muestreo directo) |
| Canales de recepción | 2 (conectores SMA) |
| Resolución ADC | 16-bit (LTC2208) |
| Tasa de muestreo ADC | 125 MS/s |
| Voltaje de fondo de escala ADC | 0.5 Vpp / −2 dBm |
| Rango de voltaje de entrada | Máx. 50 V DC (acoplamiento AC), 1 Vpp RF |
| Protección de entrada | Transformador RF + acoplamiento AC |
| Canales de transmisión | 2 |
| Resolución DAC | 14-bit |
| Tasa de muestreo DAC | 125 MS/s |
| Voltaje de salida de transmisión | 1 Vpp / +4 dBm |
| Impedancia de carga de transmisión | 50 Ω |
| Potencia de transmisión | Aprox. 2.5 mW (requiere amplificador de potencia externo) |
| Ethernet | 1 Gbit |
| USB | Type-C (USB 2.0) |
| Wi-Fi | Requiere dongle Wi-Fi externo (no incluido) |
| GPIO de expansión | E/S digital × 16, entrada analógica × 4, salida analógica × 4 |
| Rango de voltaje de entrada analógica | 0–3.3 V |
| Rango de voltaje de salida analógica | 0–1.8 V |
| Tasa de muestreo entrada analógica | 100 kS/s / 12-bit |
| Interfaces de comunicación | I2C, UART, SPI |
| Salida de alimentación de expansión | +3.3 V |
| Sistema operativo | Linux embebido (firmware Red Pitaya) |

## Casos de Uso
- Transceptor de radioafición HF (onda corta) en modos CW, SSB, AM, FM
- Monitoreo de señales débiles WSPR en múltiples bandas (hasta 8 bandas simultáneas)
- Configuración de estaciones receptoras SDR remotas (acceso remoto completo por red)
- Análisis espectral HF e investigación de señales
- Desarrollo de software compatible con HPSDR
- Experimentación en comunicaciones de radioafición (concursos, radioastronomía)

---

{{< gallery >}}
  <img src="/images/products/sdrlab/trx-duo.png" alt="SDRLab TRX-duo" />
{{< /gallery >}}

---

{{< alert >}}
¿Necesitas cotización? [Contáctanos](/es/contact/)
{{< /alert >}}
