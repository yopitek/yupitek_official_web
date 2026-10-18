---
title: "OpenSourceSDRLab RTL-SDR Blog V4 — Receptor SDR de Nivel de Entrada"
description: "RTL-SDR Blog RTL SDR V4, receptor SDR de banda ancha 500kHz–1.7GHz, TCXO de 1PPM, convertidor HF ascendente integrado, USB 2.0, la primera opción para iniciarse en investigación RF."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "RTL-SDR", "Recepción de radio", "USB", "GNU Radio"]
faq:
  - question: "¿Necesito el modo de muestreo directo para recibir HF en el RTL-SDR Blog V4?"
    answer: "No. El V4 tiene un upconverter integrado en lugar de un circuito de muestreo directo, por lo que las señales HF se upconvierten 28.8 MHz y el controlador maneja el desplazamiento de frecuencia. Habilitar el muestreo directo en un V4 no produce resultados."
  - question: "¿El RTL-SDR Blog V4 necesita controladores especiales?"
    answer: "Sí. El V4 requiere los controladores RTL-SDR Blog, que son compatibles con versiones anteriores de las unidades V3 y anteriores. La rama Osmocom predeterminada ahora también admite el V4."
  - question: "¿Cómo funciona el bias tee en el RTL-SDR Blog V4?"
    answer: "El bias tee es controlado por software y está clasificado para 4.5 V, suministrando hasta 180 mA de forma continua. En Linux se activa con rtl_biast. No lo habilite con una antena en cortocircuito DC a menos que haya un LNA o un dispositivo alimentado en la cadena."
---
## Características
![RTL-SDR Blog RTL SDR V4](/images/products/sdrlab/rtl-sdr-v4.png)
- Utiliza el sintonizador R828D mejorado, con menor ruido y mejor sensibilidad respecto al R820T/R860 de generación anterior
- Convertidor ascendente integrado que permite recepción HF desde 500 kHz (el RTL-SDR estándar solo llega hasta 24 MHz como mínimo)
- Oscilador compensado por temperatura (TCXO) de 1 PPM para una estabilidad de frecuencia significativamente mejorada
- Alimentación Bias-Tee controlable por software para alimentar LNA externo o antena activa
- Diseño de filtrado frontal de tres vías que suprime eficazmente interferencias de FM/AM/DAB broadcast
- PCB de bajo ruido rediseñado con protección ESD mejorada y carcasa de aluminio con disipación pasiva de calor
- Incluye kit de antena dipolo multipropósito, listo para usar desde el primer momento

## Especificaciones
| Especificación | Valor / Descripción |
|----------------|---------------------|
| Chip sintonizador | Rafael Micro R828D |
| Chip ADC | RTL2832U |
| Rango de frecuencia | 500 kHz – 1.7 GHz (incluye modo HF) |
| Ancho de banda máximo | 3.2 MHz (estable a 2.4 MHz) |
| Resolución ADC | 8-bit |
| Precisión de frecuencia | TCXO de 1 PPM |
| Puerto RF | SMA hembra (F) |
| Bias-Tee | Habilitado por software, máx. 4.5 V |
| Recepción HF | Convertidor ascendente integrado con filtro pasa-bajos de 28.8 MHz |
| Carcasa | Aluminio con disipación pasiva |
| Interfaz | USB 2.0 (requiere driver exclusivo de RTL-SDR Blog) |
| Sistemas operativos | Windows, Linux, macOS, Android |
| Accesorios | Kit de antena dipolo (2× antenas telescópicas, cable de extensión 3 m, trípode, soporte de ventosa) |

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
