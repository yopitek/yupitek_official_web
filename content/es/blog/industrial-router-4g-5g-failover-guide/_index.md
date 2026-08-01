---
title: "Cómo hacer failover de red 4G/5G en un router industrial: ejemplo práctico de 5G privada con EM9191"
description: "¿Cómo implementa un router industrial el failover de red 4G/5G? Este artículo explica la diferencia entre la arquitectura de red privada 5G SA y el respaldo LTE, tomando como ejemplo la EM9191, e incluye los puntos clave de integración: bandas, antenas y disipación térmica."
date: 2026-07-31
draft: false
locale: "es"
hreflang_group: "industrial-router-4g-5g-failover-guide"
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em9191", "5g", "lte", "failover", "private-network", "m2", "wwan", "sub-6"]
featureimage: "/images/products/sierra/EM9191_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
related_product: "/es/products/sierra/em9191/"
faq:
  - question: "¿Admite el EM9191 5G mmWave (ondas milimétricas)?"
    answer: "No. La hoja de especificaciones oficial indica claramente que el EM9191 no admite las bandas FR2 (mmWave). Si usted necesita mmWave, debe elegir el EM9190."
  - question: "¿Puede usarse el EM9191 en una red 5G privada?"
    answer: "Sí. Las redes privadas 5G se basan principalmente en la arquitectura SA (Standalone) independiente, y el EM9191 admite por completo la arquitectura SA de 5G NR FR1."
  - question: "¿Qué debe tenerse en cuenta al integrar el EM9191 en un router?"
    answer: "Cuatro puntos clave: 1. Su longitud es de 52 mm, no de 42 mm. 2. Deben conectarse las 4 antenas. 3. La fuente debe soportar una corriente instantánea de 2.7 A. 4. La refrigeración debe mantener la temperatura interna por debajo de 115 °C."
---

# Cómo hacer failover de red 4G/5G en un router industrial: ejemplo práctico de 5G privada con EM9191

**Resumen en una frase: añadir un módulo 5G a su router industrial como respaldo es como contratar un seguro. El módulo EM9191 de Sierra Wireless admite a la vez 4G de altísima velocidad (LTE Cat 20) y redes privadas 5G (5G SA). Así usted puede operar el respaldo 4G hoy y, cuando su planta construya la red privada 5G en el futuro, seguirá funcionando con el mismo módulo, sin cambiar hardware.**

En una fábrica, cada minuto de corte de red cuesta dinero. Los datos de las máquinas no llegan al servidor, la supervisión remota se queda a oscuras, y esa pérdida supera con creces el coste de una línea de respaldo. Por eso la redundancia de red (failover) es tan importante. En lugar de contratar una segunda fibra física de otro operador, la opción más inteligente es insertar una tarjeta SIM y usar la red móvil.

En este artículo tomamos como base la hoja de especificaciones oficial (EM919X Product Technical Specification) para explicarle por qué el módulo **EM9191** es la elección perfecta hoy para el respaldo y mañana para la red privada.

> Fuente de los datos técnicos: hoja de especificaciones oficial de Sierra Wireless. Artículo elaborado por Yupitek (榆閤科技).

---

## Lectura rápida en 30 segundos: ¿qué puede hacer el EM9191?

| Su necesidad | ¿El EM9191 es adecuado? | ¿Por qué? |
|---|---|---|
| **Respaldo de internet por 4G** | ✅ Perfecto | Admite LTE Cat 20 (agregación de 7CC muy potente); esta velocidad es más que suficiente para un respaldo. |
| **Conectarse a una red 5G privada** | ✅ Perfecto | Admite la arquitectura SA en bandas 5G FR1 (Sub-6), requisito imprescindible de las redes privadas 5G. |
| **5G mmWave (ondas milimétricas)** | ❌ No lo soporta | La hoja oficial lo indica claramente: no soporta mmWave. Si usted lo necesita, compre el EM9190. |
| **Solo quiere ahorrar costes** | ⚠️ Puede considerar otro modelo | Si está 100% seguro de que nunca usará 5G, un módulo solo 4G (por ejemplo EM7690 o EM7565) le saldrá mucho más barato. |

---

## ¿Cómo funciona el failover de respaldo?

En resumen, dentro de su router hay un vigilante de software que comprueba (hace ping) constantemente su red principal (por ejemplo, la fibra óptica).
Cuando detecta que la red principal ha caído, da la orden: «¡cambiar!» y desvía todos los paquetes de datos hacia el módulo EM9191 instalado en el router, que los envía por 5G. Cuando la red principal se recupera, vuelve a pasar el tráfico a ella discretamente.

**Dicho de otro modo, la línea de respaldo no busca «ser siempre la más rápida», sino «no cortarse jamás».**
Lo inteligente del EM9191 es que, si la señal 5G es deficiente, baja automáticamente a 4G y sigue transmitiendo, garantizando que la conexión no se interrumpa.

---

## ¿Por qué el EM9191 compra dos futuros a la vez?

El EM9191 incorpora el chip 5G Qualcomm SDX55. En la especificación oficial, el chip admite a la vez los dos modos más importantes:

1. **LTE Only** (modo solo 4G)
2. **5G NR FR1 SA / NSA** (red 5G independiente y no independiente)

¿Qué significa esto?
- **Hoy**: puede usarlo como una tarjeta 4G de primera categoría (nivel Cat 20), porque las redes públicas 5G todavía tienen zonas muertas.
- **Mañana**: cuando su empresa decida construir una «red 5G privada» (que normalmente usa arquitectura SA independiente y, en su mayoría, bandas Sub-6), bastará con cambiar la configuración para conectarse a ella, sin gastar un euro más en hardware nuevo.

---

## Conocimiento técnico para ingenieros: 4 trampas a evitar antes de integrarlo

No piense que comprar el módulo e insertarlo es el final del trabajo. El EM9191 es una pieza que consume mucha energía y genera mucho calor; al integrarlo en el router preste atención a estos cuatro puntos:

### 1. Antenas incompletas, velocidad a la mitad
El EM9191 tiene **4 puertos de antena MHF4**. Para aprovechar toda su capacidad 4x4 MIMO (sobre todo la banda n78 de 5G), debe conectar las 4 antenas por completo. Además, la recomendación oficial es que la pérdida de los cables se mantenga dentro de 0.5 dB; no use cables largos de mala calidad.

### 2. Fuente de alimentación insuficiente, corte al conectar
El EM9191 funciona a 3.3 V. Y aquí está lo importante: **la corriente pico instantánea al transmitir datos alcanza 2.7 A (2700 mA), y la corriente continua es de 2 A (2000 mA)**. Si el diseño de alimentación de la placa de su router es deficiente, en cuanto el módulo acelere la tensión caerá y el módulo se reiniciará sin parar.

### 3. Refrigeración deficiente, espere el sobrecalentamiento
Los módulos 5G calientan mucho más que los 4G. La norma oficial dice que la temperatura interna **nunca debe superar los 115 °C (mejor mantenerla por debajo de 100 °C)**. Si lo encierra en una carcasa metálica exterior, el sol del verano le garantiza un cierre por calor. Prepare un disipador térmico que conduzca el calor hacia el chasis.

### 4. Longitud del zócalo e interfaces
Es formato M.2, pero su longitud es de **52 mm**, más largo que los módulos de 42 mm que se usaban antes. Las interfaces pueden ser PCIe Gen3 o USB 3.1 Gen2. Atención: no se garantiza el soporte del antiguo USB 2.0.

---

## Conclusión

Cuando busca una red de respaldo para equipos industriales, el EM9191 es una elección excelente «para atacar y para defender» al mismo tiempo.
Gracias a su potente soporte de LTE Cat 20 y 5G SA, cubre a la perfección el «respaldo 4G de hoy» y la «red 5G privada del mañana». Si usted cuida la alimentación (pico de 2.7 A), la refrigeración (límite rojo de 115 °C) y las antenas (las 4 conectadas), el módulo le salvará en los momentos críticos.

## Información de compra (Call To Action)

¿Quiere integrar el EM9191 en su router industrial? Yupitek (榆閤科技) ofrece soluciones de hardware completas y soporte técnico de primera línea para resolverle los problemas más difíciles de refrigeración y antenas.
Escríbanos: **sales@yupitek.com**
Vea los productos: [Productos de la serie Sierra Wireless](/es/products/sierra/)

---

## Preguntas frecuentes rápidas

{{< faq >}}

---

## ¿Necesita comprar o consultar? Hable con nosotros

Si después de leer este artículo le quedan dudas sobre la integración de hardware, o su empresa necesita adquirir el módulo EM9191, puede contactar al equipo de ingeniería de Yupitek. También disponemos de las antenas y las placas adaptadoras correspondientes.

- **Página del módulo EM9191**: [https://yupitek.com/es/products/sierra/em9191/](/es/products/sierra/em9191/)
- **Todos los modelos Sierra**: [https://yupitek.com/es/products/sierra/](/es/products/sierra/)
- **Correo de contacto**: sales@yupitek.com
