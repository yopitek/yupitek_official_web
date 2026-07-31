---
title: "Guía completa para elegir módulos celulares Sierra Wireless: de LTE Cat 4 a 5G mmWave"
description: "Comparativa de especificaciones y recomendaciones de selección de los diez módulos celulares de las series EM/MC de Sierra Wireless (Semtech), desde LTE Cat 4 hasta 5G mmWave. Para adquirir módulos Sierra Wireless, contacte a Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "lte", "5g", "mmwave", "m2", "mpcie", "module-selection"]
featureimage: "/images/products/sierra/sierra_banner.png"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "¿Qué modelos ofrece Sierra Wireless y en qué se diferencian?"
    answer: "Sierra Wireless cuenta con dos series, EM y MC, con un total de diez módulos que abarcan desde LTE Cat 4 / Cat 6 / Cat 12 hasta 5G Sub-6 y mmWave. La mayor diferencia está en el formato: los EM usan M.2 y los MC usan mPCIe. Los modelos que comparten chipset (como EM7455 y MC7455) tienen el mismo rendimiento y solo difieren en la forma del conector."
  - question: "¿El EM7455 y el MC7455 usan el mismo chipset?"
    answer: "Sí. Ambos usan el chipset Qualcomm MDM9230, con picos de descarga/subida idénticos de 300 / 50 Mbps y soporte de agregación de portadoras 2×CA; las especificaciones son exactamente iguales. La única diferencia es que el EM7455 usa formato M.2 y el MC7455 usa mPCIe."
  - question: "¿Es obligatorio elegir un módulo 5G mmWave (EM9191)? ¿Funciona en nuestra región?"
    answer: "No necesariamente. Las redes 5G de la región se basan principalmente en Sub-6, mientras que mmWave se despliega sobre todo en entornos de especificación estadounidense (como n260/n261). Para la mayoría de aplicaciones, el EM9190 (5G Sub-6 económico) es suficiente; el EM9191 solo es necesario si hay requisitos de mmWave de especificación estadounidense."
  - question: "¿Cómo elegir entre módulos celulares M.2 y mPCIe?"
    answer: "Depende de la ranura de su dispositivo. Las laptops y las placas embebidas modernas suelen usar M.2 B-Key, así que elija la serie EM; los routers industriales antiguos o los equipos de automatización con ranura mPCIe usan la serie MC. Si su placa solo tiene M.2 y quiere usar MC, necesitará una placa adaptadora M.2 a mPCIe."
  - question: "¿Dónde comprar módulos Sierra Wireless?"
    answer: "Puede adquirir toda la serie de módulos celulares Sierra Wireless a través de Yupitek. Visite la página de productos del sitio oficial de Yupitek para consultar modelos y precios, o escríbanos directamente a: sales@yupitek.com"
---

# Guía completa para elegir módulos celulares Sierra Wireless: de LTE Cat 4 a 5G mmWave

Tanto si es un estudiante trabajando en un proyecto de IoT como un ingeniero desarrollando equipos de redes en el laboratorio, ¿qué es lo que más teme al comprar un módulo de comunicación? Exacto: «leer la hoja de especificaciones por horas, no distinguir los modelos y, al final, comprar el formato equivocado que ni siquiera entra en la máquina».

Este artículo explica de una vez los diez módulos de Sierra Wireless (hoy perteneciente a Semtech), tanto los actuales como los longevos, y le guía desde el LTE Cat 4 básico hasta el 5G mmWave. Todos los módulos de la serie EM mencionados aquí usan formato M.2, mientras que la serie MC usa mPCIe.

La información técnica de este artículo ha sido recopilada y proporcionada por Yupitek.

## Tabla de especificaciones de los diez modelos: los datos hablan por sí solos

¡Aquí está la tabla clave! Las cifras se han tomado de las hojas de especificaciones oficiales para que pueda compararlas directamente. Un aviso: el pico de subida de los modelos EM9190/EM9191 puede variar ligeramente según la fuente. Si va a comprar para un proyecto real, le recomendamos revisar la hoja de especificaciones oficial más reciente o consultarnos directamente (enlaces en el apéndice, al final del artículo).

| Modelo | Estándar celular | Chipset | Pico descarga / subida | Agregación de portadoras | 5G | mmWave | Formato | GNSS | Notas |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](/es/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | Cat 6 de nivel de entrada (consulte la configuración real de bandas) |
| [EM7455](/es/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | El más popular en la comunidad de código abierto |
| [EM7511](/es/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | Cat 12 con alta subida |
| [EM7565](/es/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | Compatible con bandas CBRS/LAA, la mayor cantidad de bandas y la subida más alta |
| [EM9190](/es/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | Descarga 2.5 Gbps (pico de subida: consulte) | 8×CA | ✓ | — | M.2 | ✓ | 5G Sub-6 económico de nivel de entrada |
| [EM9191](/es/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | Descarga hasta 4.5 Gbps (con mmWave) / Sub-6 2.5 Gbps (pico de subida: consulte) | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | 5G de gama alta, incluye también mmWave |
| [MC7304](/es/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4 de nivel de entrada (próximo al fin de ciclo EOL) |
| [MC7350](/es/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4, centrado en bandas de Norteamérica |
| [MC7354](/es/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4, centrado en bandas globales |
| [MC7455](/es/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | En pocas palabras, la versión mPCIe del EM7455 |

> Nota: el EM9190 y el EM9191 comparten la misma hoja de especificaciones EM919x/EM7690. El EM9190 es el 5G Sub-6 económico, mientras que el EM9191 añade mmWave y es el modelo de gama alta. La hoja de especificaciones oficial requiere iniciar sesión para descargarla; los picos de descarga de la tabla anterior se han recopilado de fuentes públicas. Para detalles como los picos de subida, le recomendamos confirmar la versión más reciente con nosotros antes de realizar el pedido.

## Primera barrera: ¿cuál es la diferencia entre las series EM (M.2) y MC (mPCIe)?

Este es, sin duda, el punto donde más se equivocan los principiantes. Comprar el modelo equivocado y que no entre en la ranura es muy frustrante.

**La serie EM = formato M.2 B-Key**: imagine el mismo tipo de interfaz que usa un SSD dentro de una laptop. Es muy compacto (aproximadamente 30×42 mm) y está diseñado específicamente para ranuras WWAN de portátiles y ranuras M.2 embebidas. La mayoría de las placas industriales y mini PC más recientes usan este formato.

**La serie MC = formato Mini PCIe (mPCIe)**: su aspecto recuerda a las tarjetas de expansión de las computadoras de antes. Es más adecuada para las ranuras mPCIe de routers industriales antiguos o equipos de automatización industrial. Si su placa solo tiene ranura M.2 y quiere usar la serie MC, necesitará comprar una placa adaptadora aparte (M.2 a mPCIe).

**Puntos en común**: ambos formatos requieren un soporte SIM externo y antenas. Los conectores de antena suelen ser U.FL, y la configuración estándar es 2×2 MIMO (una antena principal + una antena de diversidad), más una antena GNSS adicional para posicionamiento.

**La pregunta más frecuente**: ¿cuál es la diferencia real entre el EM7455 y el MC7455? La respuesta es: «el mismo chipset, solo cambia el formato». Ambas tarjetas usan el Qualcomm MDM9230 con especificaciones idénticas, así que la elección depende únicamente de la forma de su placa.

## Según su proyecto o caso de uso, le recomendamos así:

### 1. Montar su propio router inalámbrico / CPE (con OpenWrt o ROOter)

**Recomendados: [EM7455](/es/products/sierra/em7455/) / [MC7455](/es/products/sierra/mc7455/)**
La razón es simple: es el que más recursos tiene en las comunidades de código abierto. Si usa ROOter (un firmware basado en OpenWrt), encontrará tutoriales completos y ejemplos de configuración QMI/MBIM; ante cualquier problema, una búsqueda rápida en Google lo resolverá.

### 2. Actualizar la tarjeta WWAN de una laptop antigua

**Recomendados: [EM7430](/es/products/sierra/em7430/) / [EM7455](/es/products/sierra/em7455/)**
Ambos usan formato M.2, ideales para las ranuras WWAN de laptops empresariales como Dell o Lenovo. El EM7455, en particular, suele tener un buen precio en el mercado de segunda mano y es la opción preferida para actualizar (pero confirme con nosotros antes de pedir que las bandas reales coincidan con su operador).

### 3. Routers industriales / gateways IoT (que requieren robustez y amplio rango de temperatura)

**Recomendados: serie EM75 ([EM7511](/es/products/sierra/em7511/), [EM7565](/es/products/sierra/em7565/)), [EM9190](/es/products/sierra/em9190/)/[EM9191](/es/products/sierra/em9191/), [MC7455](/es/products/sierra/mc7455/)**
En proyectos industriales lo que más importa es el amplio rango de temperatura (por ejemplo, entornos exigentes de -40°C a +85°C), certificaciones completas y disponibilidad a largo plazo. Los módulos Cat 12 y 5G ofrecen mayor ancho de banda de subida y mejor escalabilidad futura. Para las especificaciones exactas de temperatura, consulte siempre la documentación oficial más reciente.

### 4. Conectividad vehicular / seguimiento de flotas (requiere posicionamiento GNSS)

**Recomendados: [EM7455](/es/products/sierra/em7455/) / [EM7565](/es/products/sierra/em7565/) / [EM9191](/es/products/sierra/em9191/)**
Los proyectos de conectividad vehicular suelen requerir posicionamiento preciso; estos tres modelos incluyen GNSS integrado y resuelven de una vez la conectividad y la geolocalización. Si necesita el gran ancho de banda del 5G, el EM9191 es la elección segura.

### 5. Redes privadas 5G / experimentos con redes privadas CBRS

**Recomendados: [EM9191](/es/products/sierra/em9191/) (compatible con bandas CBRS), [EM7565](/es/products/sierra/em7565/) (compatible con bandas CBRS/LAA)**
Si investiga CBRS (banda compartida de 3,5 GHz de especificación estadounidense) o LAA en el laboratorio, ambos modelos la admiten a nivel de hardware. Tenga en cuenta que probar redes privadas en su región depende de la normativa local y del entorno de telecomunicaciones; le recomendamos discutir los detalles técnicos con nosotros antes de la implantación.

### 6. Videovigilancia / retransmisión de audio y vídeo de alta calidad

**Recomendados: [EM9190](/es/products/sierra/em9190/) / [EM9191](/es/products/sierra/em9191/)**
El ancho de banda 5G es amplio (hasta 2,5 Gbps de descarga en Sub-6 y hasta 4,5 Gbps con mmWave), lo que lo hace ideal para retransmitir múltiples flujos de vídeo en tiempo real o streaming 4K.

### 7. Reparación de equipos antiguos / repuestos para máquinas de laboratorio antiguas (Cat 4)

**Recomendados: [MC7304](/es/products/sierra/mc7304/) / [MC7350](/es/products/sierra/mc7350/) / [MC7354](/es/products/sierra/mc7354/)**
Es la primera opción para reparar equipos antiguos con formato mPCIe. Pero seamos honestos: la serie MC73xx se acerca al final de su ciclo de vida (EOL). Para proyectos a largo plazo, le recomendamos considerar el [EM7455](/es/products/sierra/em7455/) o el [EM7565](/es/products/sierra/em7565/) como opción más segura.

## ¿Sigue sin tenerlo claro? Podemos ayudarle

Si después de leer todo esto aún no sabe qué elegir, puede adquirir estos diez módulos celulares de las series EM/MC a través de Yupitek, que también le provee antenas, adaptadores SIM o placas de evaluación. Tanto para confirmar especificaciones, comparar bandas como para cotizaciones y soporte técnico de su proyecto, puede contar con nosotros.

## Preguntas frecuentes (FAQ)

{{< faq >}}

## Apéndice: hojas de especificaciones oficiales de los diez modelos

Los siguientes enlaces apuntan a la biblioteca técnica oficial de Sierra Wireless (source.sierrawireless.com). **Algunos documentos requieren registro e inicio de sesión para descargar el PDF**. Los datos del artículo se han recopilado de fuentes públicas; si necesita confirmar especificaciones muy detalladas (por ejemplo, los picos de subida del EM9190/EM9191), le sugerimos contactarnos directamente para solicitar los documentos oficiales más recientes.

- **EM7430**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7430_product_technical_specification/
- **EM7455**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7455_product_technical_specification/
- **EM7511**: https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7511_product_technical_specification/
- **EM7565**: https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7565_product_technical_specification/
- **EM9190 / EM9191**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_em919x-7690_product_technical_specification/
- **MC7304**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7304_product_technical_specification_and_customer_design_guidelines/
- **MC7350**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_mc7455_product_technical_specification/
