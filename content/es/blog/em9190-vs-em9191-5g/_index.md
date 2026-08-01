---
title: "EM9190 vs EM9191: ¿5G Sub-6 o mmWave? Desmontamos los mitos de internet"
description: "¿Cómo elegir entre EM9190 y EM9191? Según la hoja de especificaciones oficial (41113174 Rev 8): el EM9190 admite 5G Sub-6 y mmWave (n257/258/260/261, solo NSA), mientras que el EM9191 solo admite Sub-6. Ambos usan el Qualcomm SDX55 en formato M.2. Incluye referencia de bandas 5G de Taiwán, preparado por Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em9190", "em9191", "5g", "mmwave", "sub-6", "n78", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM9190_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "¿Cuál es la diferencia real entre el EM9190 y el EM9191? ¿Cuál admite mmWave?"
    answer: "Según la hoja de especificaciones oficial (41113174, Rev 8), ambos módulos comparten las mismas capacidades en Sub-6 (FR1), LTE, 3G y GNSS. La única diferencia importante es el 5G mmWave (FR2): el EM9190 admite LTE+FR2 NSA EN-DC (con un módulo de antena QTM525/QTM527, solo en modo NSA), mientras que el EM9191 está marcado como Not supported. Por lo tanto, el EM9190 es el que tiene mmWave."
  - question: "¿Es adecuado el EM9191 para aplicaciones 5G en Taiwán?"
    answer: "Sí. La banda central del 5G en Taiwán es 3.5 GHz, que corresponde a n78 según 3GPP (3300–3800 MHz, TDD), y tanto el EM9190 como el EM9191 admiten n78. La banda de 28 GHz (correspondiente a n257) tiene poco despliegue en Taiwán, y solo en esos escenarios se necesita el EM9190 con módulos de antena mmWave. Para FWA 5G y routers industriales convencionales, el EM9191 es suficiente."
  - question: "¿Comprar el EM9190 incluye mmWave automáticamente?"
    answer: "No. El EM9190 no tiene antenas integradas. El mmWave requiere añadir de 1 a 4 módulos de antena opcionales de Qualcomm: QTM525 (baja potencia, EIRP 23 dBm) o QTM527 (alta potencia, EIRP 45 dBm), cada uno conectado por dos cables IF MHF7S (hasta 8 en total), alimentados desde una fuente externa de 3.8 V; además, FR2 solo funciona en modo NSA."
  - question: "¿Cuánta diferencia hay en el consumo entre los dos módulos?"
    answer: "Según la Table 3-2 de la hoja de especificaciones: la corriente pico es 5.0 A para el EM9190 con mmWave, 3.0 A sin mmWave y 2.7 A para el EM9191; la corriente continua es 4.0 A, 2.3 A y 2.0 A respectivamente. Para dispositivos con alimentación por batería o con limitaciones térmicas, el EM9191 facilita el diseño de la fuente de alimentación."
  - question: "¿Pueden compartir diseño de placa base el EM9190 y el EM9191?"
    answer: "En gran medida sí. Ambos son M.2 (WWAN Type 3042-S3-B, 52 mm de largo) con el mismo layout de 75 pines, las mismas interfaces USB 3.1 Gen2 / PCIe Gen3 y los mismos 4 puertos de antena Sub-6 MHF4. La diferencia: el EM9190 añade 8 conectores IF MHF7S para mmWave y pines de control QTM (pines 40/42/44/46/48, NC en el EM9191)."
---

# EM9190 vs EM9191: ¿5G Sub-6 o mmWave? Desmontamos los mitos de internet

Si usted trabaja en un proyecto 5G con su profesor en la universidad, o es responsable de la selección de módulos 5G en su empresa, seguramente ha leído esta frase una y otra vez: «El EM9190 es la versión económica de Sub-6; el EM9191 es el modelo insignia con mmWave (ondas milimétricas)».

**¡Error! Es exactamente al revés.**

En este artículo no nos basamos en lo que circula en internet. Sacamos la hoja de especificaciones oficial de Sierra Wireless, la EM919X/EM7690 Product Technical Specification (Doc 41113174, Rev 8, mayo de 2023), la usamos como único estándar y revisamos las diferencias entre ambos módulos punto por punto. Prestaremos especial atención a las dos bandas que más interesan al lector: n78 y la banda de 28 GHz, para que no compre el módulo 5G equivocado.

> Páginas de producto: [EM9190 — Yupitek](/es/products/sierra/em9190/) | [EM9191 — Yupitek](/es/products/sierra/em9191/) | Hoja de especificaciones oficial: [EM919X/EM7690 Product Technical Specification](https://yupitek.com/docs/sierra/EM919x.pdf)

---

## Desmontando el mito: ¿cuál es la diferencia real?

**En resumen, el EM9190 y el EM9191 son de la misma familia: misma serie, mismo chip de banda base. Ambos admiten 5G Sub-6, 4G LTE y posicionamiento GNSS. La única diferencia: el EM9190 añade 5G mmWave (FR2) y el EM9191 no.**

Para tener mmWave en el EM9190, además debe emparejarlo con un módulo de antena Qualcomm QTM525 o QTM527 (y solo funciona en modo NSA).

| Su pregunta | La respuesta correcta según la hoja de especificaciones oficial |
|---|---|
| **¿Cuál es la diferencia entre las dos tarjetas?** | La diferencia está en mmWave (FR2). La especificación del EM9190 indica «LTE+FR2 NSA EN-DC Supported»; la del EM9191 indica «Not supported». Todo lo demás, incluidas las bandas Sub-6 y LTE, es idéntico. |
| **¿Tiene el EM9190 mmWave?** | Sí. Pero no directamente al comprarlo: necesita añadir un módulo de antena mmWave de Qualcomm (hasta 4), que cubre n257/n258/n260/n261, y solo funciona en modo NSA (red no autónoma). |
| **¿Tiene el EM9191 mmWave?** | No. La Table 1-1 lo marca explícitamente como «Not supported», y todos los pines de señal relacionados con mmWave en la placa están NC (sin conexión). |
| **¿Cuál compro para un proyecto 5G en Taiwán?** | El 5G de Taiwán opera mayoritariamente en 3.5 GHz (n78), que ambos módulos admiten. La banda de 28 GHz (n257) es poco común en Taiwán; solo para ese tipo de experimentos necesitaría el EM9190 con antenas mmWave. |
| **¿Quién debería comprar cuál?** | **EM9190**: mercados de EE. UU. y Japón, pruebas de mmWave en laboratorio, equipos CPE exteriores que necesitan un ancho de banda enorme.<br>**EM9191**: proyectos Sub-6 en Taiwán o Asia, menor consumo, presupuestos ajustados. |

> **Lo repetimos una vez más**: deje de creer la historia de que «el EM9191 es el buque insignia con mmWave». La hoja de especificaciones oficial dice por escrito que **el EM9190 es el que tiene capacidad mmWave**. Confundirlos es un error caro.

---

## Tres hermanos de una misma familia: cómo distinguir EM9190 / EM9191 / EM7690

La familia EM91 tiene tres integrantes. Según la hoja de especificaciones:

- **EM9190**: el paquete completo (LTE + 5G Sub-6 + 5G mmWave)
- **EM9191**: el modelo estándar práctico (LTE + 5G Sub-6, sin mmWave)
- **EM7690**: el modelo reducido (solo LTE, sin 5G)

Este artículo se centra en los dos hermanos 5G. El EM7690 se menciona solo para que usted tenga el contexto completo.

---

## Tabla comparativa de especificaciones (según la oficial 41113174 Rev 8)

Todas las cifras siguientes provienen de la hoja de especificaciones oficial. Si usted es ingeniero, esta tabla es la vía más rápida:

| Elemento | EM9190 | EM9191 | Fuente |
|---|---|---|---|
| **5G NR Sub-6 (FR1)** | ✓ | ✓ | Table 1-2 |
| **5G NR mmWave (FR2)** | ✓ (solo modo NSA, requiere módulos de antena externos) | ✗ | Table 1-1 |
| **Bandas mmWave FR2** | n257 / n258 / n260 / n261 | — | Table 1-2 |
| **Bandas Sub-6 FR1** | n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n38/n40/n41/n48/n66/n71/n77/n78/n79 | Igual en ambos | Table 4-4 |
| **Chip de banda base** | Qualcomm SDX55 | Qualcomm SDX55 | Figure 3-1 |
| **Estándar celular** | 5G 3GPP Release 15; LTE Release 15 | Igual en ambos | Table 2-1 |
| **Formato** | M.2 (WWAN Type 3042-S3-B, 52 mm de largo) | Igual en ambos | §1.2 |
| **Interfaz de host** | USB 3.1 Gen2, PCIe Gen3 de un carril | Igual en ambos | §1.3 |
| **Puertos de antena Sub-6** | 4× MHF4 (MAIN/MIMO1/MIMO2/AUX) | Igual en ambos | §4.1 |
| **Puertos de antena mmWave** | 8× MHF7S (hasta 4 módulos de antena externos) | Ninguno | §4.1 |
| **Corriente pico máxima** | 5.0 A (con mmWave) / 3.0 A (sin) | 2.7 A | Table 3-2 |
| **Temperatura de funcionamiento** | -30 °C a +70 °C (Clase A); -40 °C a +85 °C (Clase B, rendimiento reducido) | Igual en ambos | Table 7-1 |
| **GNSS** | L1 (GPS/GLONASS etc.) + L5 (opcional) | Igual en ambos | Table 4-13 |

> **Pequeño recordatorio**: esta hoja de especificaciones es de mayo de 2023. Algunas bandas (como n7, n8, n20 y otras) varían según el firmware o el SKU enviado. Antes de pedir para un proyecto, solicítenos los documentos oficiales más recientes para comparar.

---

## El mmWave no viene incluido: el costo oculto del EM9190

Muchos estudiantes y makers creen que comprar el EM9190 permite probar las ondas milimétricas de inmediato. Es un gran error.

La hoja de especificaciones lo dice claramente: «**El EM9190 admite 5G mmWave solo cuando se empareja con los módulos de antena mmWave opcionales de Qualcomm.**» Además, solo funciona en modo NSA (red no autónoma), por lo que necesita una señal 4G LTE como ancla (anchor) para poder conectarse.

### ¿Cómo se configuran las antenas mmWave?

Debe comprar módulos de antena Qualcomm QTM525 (versión de baja potencia) o QTM527 (versión de alta potencia). Y los distintos módulos de antena cubren distintas bandas (consulte la Table 4-2 de la hoja de especificaciones oficial):

- Si su laboratorio quiere probar **n257** (la banda de 28 GHz), debe comprar el QTM525-2, el QTM525-5 o el QTM527-2. Si compra el QTM527-1, no tendrá n257.

**El obstáculo que los ingenieros deben tener en cuenta**:
Si va a construir un receptor 5G exterior (CPE) basado en el EM9190, probablemente necesite montar 4 antenas QTM527 de alta potencia. Eso significa 8 costosos cables MHF7S, diseñar una alimentación externa de 3.8 V para esas antenas y una refrigeración muy potente. ¡El costo de desarrollo de esta parte suele ser mucho mayor que el de la propia tarjeta!

---

## ¿Va a desplegar 5G en Taiwán? Con el EM9191 es suficiente

**Porque el pilar del 5G en Taiwán es la banda de 3.5 GHz (es decir, n78 según 3GPP), y tanto el EM9190 como el EM9191 admiten n78 perfectamente.**

Si su proyecto solo necesita 5G en Taiwán, o está fabricando routers industriales para clientes comunes:

- Ambos módulos admiten el n78 5G de Taiwán (3300–3800 MHz).
- Ambos admiten las bandas 4G actuales de Taiwán (funcionan perfectamente como ancla NSA).

**¿Por qué recomendamos comprar el EM9191?**
Porque si no va a usar ondas milimétricas, pagar por el EM9190 es tirar el dinero. Además, al no tener hardware mmWave, la corriente pico del EM9191 es solo de 2.7 A, mucho más fácil de manejar en el diseño de la fuente de alimentación que el EM9190 (detalles en la siguiente sección).

---

## Comparación de consumo: no estropee el diseño de la fuente

Todo el que fabrica hardware sabe que una fuente insuficiente provoca reinicios aleatorios. Según los datos oficiales de la Table 3-2:

| Parámetro de consumo | EM9190 (con mmWave) | EM9190 (sin mmWave) | EM9191 |
|---|---|---|---|
| Corriente pico instantánea | 5.0 A | 3.0 A | 2.7 A |
| Corriente continua | 4.0 A | 2.3 A | 2.0 A |

Todos los módulos funcionan con 3.135 V a 4.4 V (normalmente diseñados a 3.3 V). Como puede ver, si activa mmWave en el EM9190, la corriente instantánea se dispara hasta 5.0 A. Eso es un gran desafío para dispositivos con batería o de tamaño compacto. Si solo necesita 5G Sub-6, elegir el EM9191 significa manejar una pico de 2.7 A, y el diseño de la fuente de alimentación se simplifica enormemente.

---

## Diseño de pines de la placa: ¿pueden compartir diseño?

**Sí, puede compartir el diseño de Sub-6.**

Ambos módulos usan el formato M.2 (52 mm de largo, un poco más largo que los 42 mm de los portátiles, así que vigile el espacio mecánico) con el mismo layout de 75 pines.

La única diferencia: para controlar sus antenas mmWave, el EM9190 utiliza pines que normalmente estarían vacíos, como QTM_PON en los pines 40/42/44/46 y la alimentación de 1.9 V en el pin 48. Estos pines están NC en el EM9191. Por lo tanto, primero puede diseñar una placa universal para el EM9191 y, cuando realmente vaya a experimentar con mmWave, añadir las líneas de control que necesita el EM9190.

---

## Conclusión: ¿cuál debería comprar?

| Su requisito | Elija EM9190 | Elija EM9191 |
|---|---|---|
| Necesito probar bandas mmWave como 28 GHz | ✅ La única opción (no olvide añadir las antenas) | ❌ No compatible |
| Proyecto en Taiwán que solo usa 5G Sub-6 (n78) | Funciona (pero es un desperdicio) | ✅ Recomendado, más barato y eficiente |
| La fuente de la placa no aguanta corrientes altas | ⚠️ El pico puede llegar a 5.0 A | ✅ El pico de 2.7 A es mucho más manejable |

**Guía para evitar trampas**:

1. No se confunda más: el EM9190 es el que tiene mmWave.
2. Comprar el EM9190 no le da mmWave; también tiene que comprar las antenas especiales y pasar el cableado.
3. Muchas bandas (n7, n8, n28 y otras) están limitadas por la versión de firmware y la región. Confirme con su proveedor si su SKU puede desbloquear esas bandas antes de comprar.

---

## Preguntas frecuentes rápidas

{{< faq >}}

---

## ¿Necesita comprar o discutir? Hable con nosotros

Si tras leer este artículo le quedan dudas de integración de hardware, o su laboratorio/empresa necesita comprar estos dos módulos 5G, no dude en contactar al equipo de ingeniería de Yupitek. También disponemos de las antenas y placas adaptadoras correspondientes.

- **Página del producto EM9190 (el verdadero buque insignia con mmWave)**: [https://yupitek.com/es/products/sierra/em9190/](/es/products/sierra/em9190/)
- **Página del producto EM9191 (el modelo Sub-6 práctico)**: [https://yupitek.com/es/products/sierra/em9191/](/es/products/sierra/em9191/)
- **Todos los modelos Sierra**: [https://yupitek.com/es/products/sierra/](/es/products/sierra/)
- **Correo de contacto**: sales@yupitek.com
