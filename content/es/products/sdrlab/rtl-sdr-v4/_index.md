---
title: "OpenSourceSDRLab RTL-SDR Blog V4 — Receptor SDR de Nivel de Entrada"
description: "RTL-SDR Blog RTL SDR V4, receptor SDR de banda ancha 500kHz–1.766GHz, TCXO de 1PPM, convertidor HF ascendente integrado, la primera opción para iniciarse en investigación RF."
date: 2026-03-12
draft: false
featureimage: "/images/products/sdrlab/rtl-sdr-v4.png"
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "RTL-SDR", "Recepción de radio", "USB", "GNU Radio"]
faq:
  - question: "¿Necesito el modo de muestreo directo para recibir HF en el RTL-SDR Blog V4?"
    answer: "No. El V4 tiene un upconverter integrado en lugar de un circuito de muestreo directo, por lo que las señales HF se upconvierten 28.8 MHz y el controlador maneja el desplazamiento de frecuencia. Habilitar el muestreo directo en un V4 no produce resultados."
  - question: "¿El RTL-SDR Blog V4 necesita controladores especiales?"
    answer: "Sí. El V4 requiere los controladores RTL-SDR Blog, que son compatibles con versiones anteriores de las unidades V3 y anteriores."
  - question: "¿Cómo funciona el bias tee en el RTL-SDR Blog V4?"
    answer: "El bias tee es controlado por software y está clasificado para 4.5 V, suministrando hasta 180 mA de forma continua. En Linux se activa con rtl_biast."
---
## Características
![RTL-SDR Blog RTL SDR V4](/images/products/sdrlab/rtl-sdr-v4.png)
- Sintonizador R828D con tres entradas; un triplexor divide la entrada SMA en las bandas HF, VHF y UHF para mejorar el aislamiento fuera de banda
- Convertidor ascendente HF integrado: HF se convierte 28.8 MHz hacia arriba, sin necesidad del modo de muestreo directo (límite inferior de sintonía 500 kHz)
- Oscilador compensado por temperatura (TCXO) de 1 PPM para una estabilidad de frecuencia significativamente mejorada
- Alimentación Bias-Tee controlable por software para alimentar LNA externo o antena activa
- Filtro notch conmutable para las bandas de radiodifusión AM, FM y DAB que reduce la interferencia de emisoras fuertes
- Carcasa metálica negra conductora que blinda y actúa como disipador, con supresión de ruido USB y protección ESD mejorada
- Incluye kit de antena dipolo multipropósito, listo para usar desde el primer momento

## Especificaciones
| Especificación | Valor / Descripción |
|----------------|---------------------|
| Chip sintonizador | Rafael Micro R828D |
| Chip ADC | RTL2832U |
| Rango de frecuencia | 500 kHz – 1.766 GHz (incluye modo HF) |
| Precisión de frecuencia | TCXO de 1 PPM |
| Puerto RF | SMA |
| Bias-Tee | Habilitado por software, máx. 4.5 V |
| Recepción HF | Convertidor ascendente integrado (HF convertido 28.8 MHz hacia arriba; sin muestreo directo) |
| Carcasa | Carcasa metálica negra conductora (blindaje y disipador) |
| Interfaz | USB (requiere los controladores RTL-SDR Blog) |
| Sistemas operativos | Windows, Linux, macOS, Android |
| Accesorios | Kit de antena dipolo (4× antenas telescópicas (2× de 23 cm–1 m y 2× de 5–13 cm), cable de extensión 3 m, trípode, soporte de ventosa) |

## Casos de Uso
- Seguimiento de aeronaves ADS-B
- Monitoreo marítimo AIS
- Recepción de imágenes de satélites meteorológicos NOAA/Meteor M2
- Radioafición (recepción HF/VHF/UHF)
- Radioastronomía (observación de la línea de hidrógeno)
- Decodificación de voz digital P25 y MotoTRBO
- Rastreo de paquetes APRS y ACARS
- Recepción de radio digital DAB
- Monitoreo del espectro RF e investigación de seguridad

---

{{< alert >}}
¿Necesita una cotización del producto? Por favor, [contáctenos](/es/contact/).
{{< /alert >}}

{{< faq >}}

[Guías de configuración y detalles técnicos — doc.yupitek.com](https://doc.yupitek.com/sdrlab/hardware/rtl-sdr-v4/)

[Guía oficial de RTL-SDR Blog para el V4](https://www.rtl-sdr.com/v4/)

Página oficial del fabricante (OpenSourceSDRLab, no verificada en línea): https://opensourcesdrlab.com/products/rtl-sdr-v4
