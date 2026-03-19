---
title: "SDRLab TRX-duo — Plataforma SDR Dual-Channel 16-bit com ZYNQ"
description: "SDRLab TRX-duo, plataforma SDR dual-channel 16-bit ADC/DAC, SoC Xilinx Zynq 7010, compatível com Red Pitaya, amostragem direta de 10kHz–60MHz. Ideal para pesquisa avançada de comunicações HF."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "TRX-duo", "ZYNQ", "Red Pitaya", "16-bit ADC"]
---
## Características

![SDRLab TRX-duo](/images/products/sdrlab/trx-duo.png)

- Design de transceptor dual-channel (2 RX + 2 TX), compatível com o ecossistema de software Red Pitaya
- Dois ADCs LTC2208 de alta precisão de 16 bits, oferecendo alta faixa dinâmica e elevada sensibilidade
- DAC de 14 bits para transmissão em dois canais
- SoC Xilinx Zynq 7010 embarcado (ARM Cortex-A9 dual-core + FPGA), permitindo executar software de decodificação diretamente no dispositivo
- Suporte a implantação remota via rede para criação de estações SDR remotas
- Compatível com os principais softwares: HDSDR, SDR#, PowerSDR, SDR Console V3
- Cerca de metade do preço do Red Pitaya SDRlab 122-16 oficial (aproximadamente US$ 622)

## Especificações

| Item | Valor / Descrição |
|------|-------------------|
| Processador | ARM Cortex-A9 dual-core (SoC Zynq 7010) |
| FPGA | Xilinx Zynq 7010 |
| Memória (RAM) | 512 MB |
| Faixa de Recepção | 10 kHz – 60 MHz (amostragem direta) |
| Canais de Recepção | 2 (conectores SMA) |
| Resolução ADC | 16 bits (LTC2208) |
| Taxa de Amostragem ADC | 125 MS/s |
| Tensão Full-Scale ADC | 0,5 Vpp / −2 dBm |
| Faixa de Tensão de Entrada | DC máx. 50 V (acoplamento AC), 1 Vpp RF |
| Proteção de Entrada | Transformador RF + acoplamento AC |
| Canais de Transmissão | 2 |
| Resolução DAC | 14 bits |
| Taxa de Amostragem DAC | 125 MS/s |
| Tensão de Saída TX | 1 Vpp / +4 dBm |
| Impedância de Carga TX | 50 Ω |
| Potência de Transmissão | Aprox. 2,5 mW (amplificador de potência externo necessário) |
| Ethernet | 1 Gbit |
| USB | Type-C (USB 2.0) |
| Wi-Fi | Requer dongle Wi-Fi externo (não incluso) |
| GPIO de Expansão | 16× E/S digital, 4× entrada analógica, 4× saída analógica |
| Faixa de Tensão de Entrada Analógica | 0–3,3 V |
| Faixa de Tensão de Saída Analógica | 0–1,8 V |
| Taxa de Amostragem Analógica | 100 kS/s / 12 bits |
| Interfaces de Comunicação | I2C, UART, SPI |
| Saída de Alimentação de Expansão | +3,3 V |
| Sistema Operacional | Linux embarcado (firmware Red Pitaya) |

## Casos de Uso

- Transceptor HF para radioamadores (CW, SSB, AM, FM)
- Monitoramento de sinais fracos WSPR em múltiplas bandas (até 8 bandas simultâneas)
- Criação de estação SDR remota com acesso total via rede
- Análise de espectro HF e pesquisa de sinais
- Desenvolvimento de software compatível com HPSDR
- Experimentos de comunicação em radioamadorismo (concursos, observação astronômica)

---

{{< alert >}}
Tem interesse neste produto? [Entre em contato](/pt/contact/) para obter preços.
{{< /alert >}}
