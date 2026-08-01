---
title: "Guía completa para actualizar portátiles Dell / Lenovo con tarjetas 4G/5G: lista de modelos compatibles + guía de instalación | Yupitek"
description: "Guía completa para actualizar portátiles Dell / Lenovo con tarjetas 4G/5G: compara las diferencias de especificaciones entre EM7455 y EM7430 y le enseña a revisar la ranura M.2, las antenas WWAN y la lista blanca del BIOS. Descarga Cat 6 de 300 Mbps, con guía de instalación completa."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "es"
hreflang_group: "dell-lenovo-laptop-4g-5g-upgrade-guide"
slug: "dell-lenovo-laptop-4g-5g-upgrade-guide"
tags: ["Dell", "Lenovo", "4G", "5G", "EM7455", "EM7430", "WWAN", "M.2"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/es/products/sierra/"
faq:
  - question: "¿Puedo instalar directamente el EM7455 / EM7430 en mi portátil Dell / Lenovo?"
    answer: "No basta con fijarse solo en la marca. Deben cumplirse tres condiciones a la vez: que la placa tenga una ranura M.2 B-key (67 pines) WWAN, que el chasis tenga antenas WWAN reservadas y que el BIOS no tenga bloqueada una lista blanca. Se recomienda consultar el manual de servicio oficial y abrir el equipo para confirmarlo."
  - question: "¿En qué se diferencian el EM7455 y el EM7430?"
    answer: "Ambos usan el chipset Qualcomm MDM9230, con velocidad LTE Cat 6 (300/50 Mbps) y empaque M.2 idéntico. La diferencia está en las bandas: el EM7455 se orienta a América/global y el EM7430 a la región Asia-Pacífico, con soporte de TD-SCDMA chino."
  - question: "¿Cuántas antenas necesita la tarjeta?"
    answer: "El módulo tiene 3 conectores RF (Main, GNSS y Aux). Para navegar basta con conectar al menos Main; para velocidad máxima debe conectar Aux; y solo necesitará la antena GNSS si desea usar el posicionamiento GPS."
---

# Guía completa para actualizar portátiles Dell / Lenovo con tarjetas 4G/5G: lista de modelos compatibles + guía de instalación

**Resumen en una frase: para actualizar su portátil con una tarjeta 4G, compruebe primero si tiene antenas y ranura, y luego confirme si el BIOS permite la instalación. En cuanto a la elección: en Taiwán o Asia, puede elegir el EM7455 o el EM7430; ambos están fabricados con el mismo chipset MDM9230, son tarjetas Cat 6 con la misma velocidad, y la única diferencia son las bandas admitidas.**

Muchos amigos que tienen un Dell Latitude o un Lenovo ThinkPad quieren instalar una tarjeta 4G en la ranura WWAN reservada del portátil para no tener que buscar Wi-Fi en los viajes. ¡Pero esto no es tan sencillo! Debe confirmar la especificación de la ranura de la placa, comprobar que las antenas estén preparadas y ver si el fabricante ha bloqueado una «lista blanca».

En este artículo utilizamos las hojas de especificaciones oficiales de Sierra Wireless para comparar el EM7455 y el EM7430, las dos tarjetas más usadas en estas actualizaciones, y le explicamos cómo instalarlas.

> Fuente de datos de especificaciones: hojas de especificaciones oficiales de Sierra Wireless (EM7455 y EM7430). Artículo elaborado por Yupitek.

---

## Autodiagnóstico rápido en 30 segundos: ¿mi portátil admite la instalación?

| Punto de comprobación | ¿Qué es? | ¿Cómo lo reviso? |
|---|---|---|
| **¿La ranura es la correcta?** | Ranura WWAN dedicada M.2 B-key (67 pines) | Abra la tapa inferior y busque una ranura vacía de 42 mm de largo; normalmente lleva la inscripción WWAN. ¡No la inserte en el hueco del Wi-Fi! |
| **¿Hay antenas reservadas?** | El módulo necesita antenas para tener señal | Busque cerca de la ranura terminales de antena pequeños sin usar, en rojo, azul y negro. Si no los hay, comprar la tarjeta será inútil. |
| **Lista blanca del BIOS** | Los fabricantes restringen la instalación a tarjetas certificadas de fábrica | Consulte el «Manual de servicio (Service Manual)» de su modelo en el sitio oficial y revise la lista de módulos WWAN admitidos. |
| **¿Qué es el DW5811e de Dell?** | Es un número de pieza de Dell, no un modelo de tarjeta | El mismo número de pieza puede contener tarjetas distintas; al comprar de segunda mano, fíjese en la inscripción «Sierra EM7455» de la propia tarjeta. |

---

## Duelo de tarjetas: EM7455 vs EM7430

Estas dos tarjetas son prácticamente gemelas. Ambas usan el chipset Qualcomm MDM9230, ambas alcanzan LTE Cat 6 (descarga de hasta 300 Mbps y subida de 50 Mbps) y tienen las mismas dimensiones (empaque M.2 de 42×30 mm y 6.5 g de peso).

**¿En qué se diferencian? ¡La respuesta es: en las bandas!**

| Punto de comparación | EM7455 | EM7430 | Conclusión |
|---|---|---|---|
| **Bandas principales** | Orientado a global y América (FDD sobre todo) | Orientado a Asia-Pacífico (FDD+TDD) | Para Asia, la cobertura del 7430 es más amplia; para viajar a EE. UU., elija el 7455. |
| **3G chino (TD-SCDMA)** | No compatible | Compatible (Band 39) | Solo importa si viaja a China con frecuencia. |
| **Alcance de certificaciones** | Incluye certificaciones de América (FCC/IC/PTCRB), entre otras | Las especificaciones no listan certificaciones americanas | El EM7430 es más bien una variante asiática. |

**Recomendación para usuarios de Taiwán**: ambas tarjetas cubren las bandas 4G principales de Taiwán, y la velocidad práctica es idéntica. Su elección depende de cuál sea más fácil de conseguir en el mercado y de cuál permita la lista blanca del BIOS de su portátil.

---

## Manos a la obra: inspección del espacio interno del portátil

Antes de comprar la tarjeta, vuelva a confirmar el espacio dentro de su portátil:

1. **Tamaño de la ranura**: ambos módulos usan la especificación **M.2 WWAN Type 3042-S3-B**, es decir, 42 mm de largo y 30 mm de ancho.
2. **Límite de grosor**: el módulo no supera 1.50 mm de grosor por encima de la placa de circuito. Preste atención si un SSD o un disipador lo bloquea desde arriba.
3. **Estabilidad del voltaje**: funcionan entre 3.135 V y 4.4 V (normalmente 3.7 V); la placa del portátil suele encargarse de esto. Pero cuide el calor: la compañía recomienda mantener la temperatura interna por debajo de 80 °C (máximo 93 °C).

---

## Guía de instalación: paso a paso

Si ha confirmado que su portátil tiene antenas, que la ranura es la correcta y que no hay problema de lista blanca, ¡instálela con confianza!

1. **Apague y descargue**: apague el equipo, desconecte el cable de alimentación, retire la batería externa si la hay y pulse varias veces el botón de encendido para descargar la electricidad. (¡La protección contra estática es muy importante!)
2. **Abra la tapa inferior**: levante la tapa inferior del portátil y localice la ranura M.2 vacía que dice WWAN.
3. **Inserte la tarjeta**: introduzca el módulo en ángulo de 30 grados, alineando la muesca con la lengüeta a prueba de errores (B-key).
4. **Apriete el tornillo**: presione suavemente para aplanarla y fije el tornillo pequeño.
5. **Conecte las antenas (la parte más difícil)**:
   - El módulo tiene 3 conectores; de izquierda a derecha suelen ser Main (antena principal), GNSS (GPS) y Aux (antena auxiliar).
   - Alinee con cuidado y presione hacia abajo: los conectores MHF4 son muy pequeños y frágiles; si los aplasta, tendrá un problema.
   - Conecte al menos Main; de lo contrario, no habrá señal. Para velocidad máxima, conecte también Aux. Conecte GNSS solo si quiere navegación.
6. **Inserte la tarjeta SIM**: ¡el módulo no tiene ranura para SIM; la ranura SIM está en el lateral del portátil o dentro del compartimento de la batería! Estas dos tarjetas admiten SIM de 1.8 V y 3 V.
7. **Encienda y listo**: vuelva a colocar la tapa, encienda e instale los controladores (Windows 10 lo detectará automáticamente mediante el protocolo MBIM).

---

## Los errores más comunes

- **Comprar la ranura equivocada**: intentar meter a la fuerza una tarjeta mPCIe (como la MC7455) en la ranura M.2.
- **Instalar sin antenas**: asumir que el portátil tiene antenas reservadas, comprar e instalar, y descubrir que no hay cable que conectar: la señal siempre será de 0 barras.
- **Ser rechazado por la lista blanca**: comprar una versión genérica barata y encontrarse al arrancar con una pantalla negra que dice «tarjeta no autorizada».
- **Pensar que soporta 5G**: el EM7455 y el EM7430 son tarjetas LTE 4G puras (Cat 6). Para 5G, busque un módulo como el EM9190, ¡y necesitará conectar 4 antenas o más!

## Conclusión

Actualizar la tarjeta de red de su portátil no es difícil; lo difícil es la «prospección de hardware» previa. Abra primero el portátil para ver si hay antenas y consulte si el fabricante ha bloqueado la lista blanca. Si supera estas dos barreras, el EM7455 o el EM7430 le darán una experiencia de conexión móvil estable y fluida.

## Preguntas frecuentes (FAQ)

{{< faq >}}

## Información de compra (Llamada a la acción)

¿Quiere adquirir tarjetas de la serie Sierra Wireless? ¿O no está seguro de si su equipo industrial las admite? Yupitek ofrece soluciones de hardware completas y soporte técnico.
Escríbanos: **sales@yupitek.com**
Vea los productos: [Serie Sierra Wireless](https://yupitek.com/es/products/sierra/)
