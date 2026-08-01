---
title: "Retorno móvil para videovigilancia y cartelería digital: cómo elegir entre Cat 6 y 5G"
description: "¿Qué módulo celular necesitan las cámaras de vigilancia y los carteles digitales? La clave está en el «envío» o la «descarga». Este artículo compara el EM7455 (Cat 6), el EM7565 (Cat 12) y el EM9191 (5G) según las hojas de especificaciones oficiales, para que usted elija con precisión sin gastar dinero de más."
date: 2026-07-31
draft: false
locale: "es"
hreflang_group: "video-surveillance-digital-signage-cellular-backhaul-cat6-to-5g"
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "video-surveillance", "digital-signage", "lte", "5g", "cat-6", "cat-12", "m2", "backhaul"]
featureimage: "/images/products/sierra/sierra_banner.png"
author: "benny-lai"
lastmod: 2026-07-31
related_product: "/es/products/sierra/"
faq:
  - question: "¿Cuánta velocidad de subida se necesita para transmitir el vídeo de cámaras de vigilancia por 4G?"
    answer: "Una cámara 1080p con H.264 consume aproximadamente de 2 a 6 Mbps. Con el EM7455, cuyo límite de subida es de 50 Mbps, puede soportar de forma estable de 4 a 6 cámaras 1080p. Si la demanda es mayor, le recomendamos subir al EM7565."
  - question: "¿Es suficiente Cat 6 para conectar carteles digitales a internet?"
    answer: "Los carteles digitales dependen principalmente de la «descarga». El Cat 6 (como el EM7455) ofrece 300 Mbps de descarga, más que suficiente para actualizar imágenes y vídeos habituales. Si usted empuja archivos de vídeo 4K muy grandes con frecuencia, puede subir al EM7565 (600 Mbps) para acortar el tiempo de descarga."
  - question: "¿Qué hay que tener en cuenta al instalar un módulo 4G/5G dentro de una caja de metal exterior?"
    answer: "Dos puntos clave: refrigeración y alimentación. La temperatura interna del módulo normalmente no debe superar los 90 a 115 °C, y las cajas de metal exteriores se calientan con facilidad, así que debe asegurar una buena conducción del calor. Además, el consumo instantáneo de un módulo 5G puede llegar a 2,7 A, por lo que el convertidor de alimentación debe aguantar esa corriente de pico."
---

# Retorno móvil para videovigilancia y cartelería digital: cómo elegir entre Cat 6 y 5G

**Resumen en una frase: no se deje deslumbrar por el 5G; primero pregúntese si su equipo «sube» datos sin parar o los «baja». Las cámaras de vigilancia envían la imagen continuamente a la nube, así que debe mirar la velocidad de subida (Uplink); los carteles digitales descargan vídeos nuevos para reproducirlos, así que debe mirar la velocidad de descarga (Downlink). Si solo necesita transmitir unas pocas cámaras 1080p, la tarjeta Cat 6 más barata le sobra.**

Muchos propietarios, al licitar el proyecto de red para «cámaras de vigilancia en cruces» o «carteles publicitarios de cadenas de tiendas», abren la conversación diciendo: «¡Póngame el módulo 5G más rápido!»
Y gastan una fortuna para luego descubrir que en realidad no lo necesitaban.

Elegir una tarjeta de red no es elegir un coche de carreras; no se trata de que cuanto más rápida, mejor, sino de «recetar el remedio adecuado a cada caso». En este artículo tomamos los tres módulos M.2 más habituales de Sierra Wireless (EM7455, EM7565 y EM9191) y, con los números de las hojas de especificaciones oficiales, le enseñamos a elegir el más rentable.

> Fuente de los datos técnicos: hojas de especificaciones oficiales de Sierra Wireless. Artículo recopilado por Yupitek (榆閤科技).

---

## Guía rápida de elección en 30 segundos: ¿cuál debe comprar usted?

| Su escenario de aplicación | Foco del tráfico | ¿Qué tarjeta comprar? | ¿Por qué? |
|---|---|---|---|
| **Proyecto pequeño: de 1 a 4 cámaras 1080p** | Subida (UL) | **EM7455 (Cat 6)** | Su límite de subida es de 50 Mbps; de sobra para unas pocas cámaras 1080p, y es la más barata. |
| **Mediano y grande: de 5 a 10 cámaras 1080p o cámaras 4K** | Subida (UL) | **EM7565 (Cat 12)** | Gran salto de subida hasta 150 Mbps, con margen más que suficiente. |
| **Actualización de anuncios en cartelería digital** | Descarga (DL) | **EM7565 (Cat 12)** | Hasta 600 Mbps de descarga; se baja un anuncio 4K de varios GB en un momento. |
| **Monstruo absoluto: emisión en directo de varios 4K a la vez + carteles** | Ambos sentidos rápidos | **EM9191 (5G)** | 5G con la brutal especificación LTE Cat 20; quien no le falte dinero, cómprela. |

---

## ¿Por qué hay que distinguir entre «subida» y «descarga»?

Porque en el mundo 4G/5G, **la velocidad de descarga suele ser de 5 a 6 veces la de subida.**

Tomemos la más básica, la EM7455: la hoja oficial indica 300 Mbps de descarga, pero solo **50 Mbps** de subida.
Si usted se emociona mirando el número de 300 Mbps y decide conectarla a 10 cámaras 4K, el resultado será que se atasca hasta hacerle dudar de la vida, porque las cámaras dependen de esos míseros 50 Mbps.

| Equipo | Su comportamiento de red | La especificación que debe mirar |
|---|---|---|
| **Cámara / NVR** | Envía la imagen continuamente para que otros la vean | **Subida (Uplink, UL)** |
| **Cartel digital** | Descarga los vídeos preparados y los reproduce | **Descarga (Downlink, DL)** |
| **Quiosco interactivo** | Descarga vídeos y a veces envía datos de clics | **Descarga principal, subida secundaria** |

---

## Cálculo práctico: ¿cuánta subida necesita realmente su videovigilancia?

(Nota: los siguientes son valores de experiencia del sector; varían según el códec de compresión y el dinamismo de la imagen)

- 1 canal **1080p (H.264)** consume aproximadamente **de 2 a 6 Mbps**
- 1 canal **4K (H.265)** consume aproximadamente **de 8 a 16 Mbps**

Si usted tiene 6 cámaras 1080p, el cálculo sería: `6 cámaras × 5 Mbps = 30 Mbps`.
Parece que la EM7455 (subida de 50 Mbps) llega justa, ¿verdad? Pues no. **En la realidad es imposible alcanzar el límite teórico.** Teniendo en cuenta la atenuación de la señal, ya estamos en una situación muy ajustada; le recomendamos subir directamente a la EM7565 (subida de 150 Mbps) para ir con seguridad.

---

## Las tres generaciones cara a cara: EM7455 vs EM7565 vs EM9191

Veamos los números de hardware de las hojas de especificaciones oficiales:

| Especificación | EM7455 (Cat 6) | EM7565 (Cat 12) | EM9191 (5G) |
|---|---|---|---|
| **Límite de descarga (DL)** | 300 Mbps | 600 Mbps | Cat 20 (muy rápida) |
| **Límite de subida (UL)** | 50 Mbps | 150 Mbps | Subida de nivel Cat 12 |
| **Número de puertos de antena** | 3 | 3 | 4 (conéctelas todas) |
| **Temperatura máxima de trabajo** | Interior sin superar 93 °C | Interior sin superar 90 °C | Interior sin superar 115 °C |
| **Corriente máxima instantánea** | 1,5 A | 1,5 A (pico de 2,5 A) | Se dispara hasta 2,7 A (2700 mA) |

---

## ¿Va a meter el módulo en una caja de metal exterior? Cuidado con que se achicharre

Al instalar estos módulos en las cajas de las cámaras de vigilancia o de los carteles digitales en la calle, preste atención a estos dos grandes enemigos:

### 1. El módulo «tiene fiebre»
Los tres módulos temen el calor; la recomendación oficial es mantenerlos por debajo de 80 °C a 100 °C. En verano en Taiwán, la temperatura dentro de una caja de metal exterior supera fácilmente los 60 grados. Si usted no le pone un disipador que conduzca el calor hacia fuera, en cuanto se caliente el módulo empezará a bajar la velocidad y acabará apagándose en seco.

### 2. Alimentación suficiente
Especialmente una bestia 5G como la EM9191: al transmitir datos con furia, la corriente instantánea puede alcanzar **2,7 A**.
Si su placa de alimentación escatima en materiales, la tensión caerá y el módulo se reiniciará en bucle sin fin.

---

## Conclusión

Comprar una tarjeta de red es como alquilar un camión: según la carga que vaya a llevar, se alquila el tamaño adecuado.

- **Primero lo barato**: si usted solo hace videovigilancia 1080p (con 4 cámaras o menos), o cartelería digital con textos e imágenes simples, compre la **EM7455** sin pensarlo.
- **Mejor relación calidad-precio**: si hay muchas imágenes de alta definición, o los carteles descargan archivos grandes con frecuencia, los 150 Mbps de subida y 600 Mbps de descarga de la **EM7565** son, sin duda, el punto dulce actual.
- **Guerrero del futuro**: salvo que el propietario exija 5G, o usted tenga varios 4K emitiendo a la vez, no merece la pena plantearse la calurosa y hambrienta de energía **EM9191**.

## Información de compra (Llamada a la acción)

¿Está planificando una solución de red para retorno de vídeo o para cartelería digital? Yupitek (榆閤科技) ofrece módulos Sierra Wireless completos y asesoramiento técnico profesional para calcularle la combinación más rentable.
Escríbanos: **sales@yupitek.com**
Vea los productos: [Sección de productos Sierra Wireless](/es/products/sierra/)

---

## Preguntas frecuentes

{{< faq >}}
