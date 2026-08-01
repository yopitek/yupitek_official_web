---
title: "Conectividad celular BVLOS para drones y robots de inspección: cómo lograr un backhaul de baja latencia"
description: "¿Cómo lograr conectividad BVLOS para drones? Este artículo compara el Sierra EM9190, el EM9191 y el EM7565, y analiza la arquitectura 5G SA de baja latencia, la subida de vídeo y el posicionamiento dual L1/L5, para que usted construya soluciones de robots de inspección y drones sin cortes."
date: 2026-07-31
draft: false
locale: "es"
hreflang_group: "drone-bvlos-cellular-connectivity-low-latency-backhaul"
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "drone", "bvlos", "5g", "low-latency", "gnss", "m2", "inspection-robot", "sub-6"]
featureimage: "/images/products/sierra/EM9191_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
related_product: "/es/products/sierra/em9191/"
faq:
  - question: "¿Por qué es imprescindible la conectividad celular para drones en operaciones BVLOS?"
    answer: "Cuando el dron vuela fuera del alcance visual, la señal del mando a distancia se corta. En ese momento, la red 4G/5G es la única solución capaz de ofrecer cobertura amplia, control de baja latencia y transmisión de vídeo de alto ancho de banda."
  - question: "¿Cuál es la diferencia entre el EM9190 y el EM9191?"
    answer: "El EM9190 añade soporte de ondas milimétricas 5G (mmWave), pero requiere antenas de matriz que consumen mucha energía y ocupan espacio. En la mayoría de las regiones sin redes mmWave, la opción más adecuada es el EM9191 (solo 5G Sub-6)."
  - question: "¿Qué módulo conviene para los robots de inspección?"
    answer: "Para inspección en planta, normalmente solo se necesita transmitir imágenes comunes, y el EM7565 (Cat 12, subida de 150 Mbps) es suficiente para cubrir la necesidad, con un coste menor."
---

# Conectividad celular BVLOS para drones y robots de inspección: cómo lograr un backhaul de baja latencia

**Resumen en una frase: para que un dron vuele fuera de su línea de visión, usted necesita un módulo 4G/5G capaz de gestionar a la vez «transmisión de vídeo, control remoto y posicionamiento». Si su dron va a conectarse a una red privada 5G y necesita velocidad de vídeo extrema con posicionamiento ultrapreciso dual L1+L5, elija el EM9191; si solo se trata de un robot de inspección que avanza despacio por la planta, el módulo 4G barato y excelente EM7565 le sobra.**

Cuando el dron o el robot sale de su línea de visión (esto es lo que se llama BVLOS, Beyond Visual Line of Sight), el mando tradicional que usted lleva en la mano deja de servir. En ese momento, la máquina solo puede conectarse a la estación base mediante su tarjeta 4G/5G, enviar imágenes de alta calidad y recibir sus órdenes de control.

En este artículo usamos las hojas de especificaciones oficiales de Sierra Wireless para descifrar el misterio: ¿por qué estos módulos encajan tan bien con drones y robots? ¿Cómo consiguen una latencia baja?

> Fuente de los datos técnicos: hojas de especificaciones oficiales de Sierra Wireless (EM9190/EM9191 y EM7565). Artículo recopilado por Yupitek (榆閤科技).

---

## Selección rápida en 30 segundos: ¿qué módulo instala en el dron o el robot?

| Escenario de aplicación | Módulo recomendado | ¿Por qué elegirlo? |
|---|---|---|
| **Dron de gama alta (necesita red privada 5G)** | **EM9191** | Soporta 5G Sub-6 y la arquitectura de red privada 5G SA, con la máxima velocidad de subida de la categoría LTE Cat 20 y posicionamiento de alta precisión L1+L5 integrado. |
| **Dron de gama alta (mercado estadounidense)** | **EM9190** | El hermano mayor del EM9191; añade soporte de ondas milimétricas (mmWave). Pero en Taiwán no sirve. |
| **Robot de inspección de planta (terrestre)** | **EM7565** | Es un módulo 4G Cat 12, ligero y ahorrador de energía; la inspección de planta no necesita 5G, sería matar moscas a cañonazos; elegirlo es lo más rentable. |

---

## ¿Cómo se consigue la baja latencia? Los secretos de la hoja de especificaciones

Todos sabemos por los videojuegos que el valor de Ping (latencia) es muy importante, y un dron volando en el cielo es aún más sensible a ella; allí la latencia es cuestión de vida o muerte. La hoja de especificaciones no escribe «cuántos milisegundos de latencia», pero contiene estas tres armas capaces de reducirla de forma significativa:

1. **Arquitectura 5G SA (red independiente)**: la serie EM919x soporta la arquitectura SA de tipo Option 2. Es decir, el dron puede conectarse directamente al núcleo 5G sin pasar por las antiguas estaciones base 4G; ese es el arma más poderosa para bajar la latencia.
2. **Control de prioridad QoS QCI**: el módulo admite la configuración QoS de 3GPP R15, lo que significa que usted puede fijar la prioridad de las «órdenes de vuelo» por encima de la «transmisión de vídeo»; así, aunque la red se congestione, la máquina no perderá el control.
3. **Agregación de portadoras de subida (UL CA) con 256QAM**: la transmisión de vídeo depende por completo de la velocidad de subida. La serie EM919x y el EM7565 soportan unir varias bandas en la subida, con la mejor técnica de compresión 256QAM (en EM919x) o 64QAM (en EM7565), para que el vídeo fluya sin tirones.

---

## Dron frente a robot de inspección: la lógica de selección es muy distinta

Lo que vuela en el cielo y lo que camina por el suelo tienen exigencias totalmente diferentes sobre la tarjeta de red.

### Dron (Drone): súper sensible al peso, al calor y al posicionamiento
- **El peso es autonomía**: el EM9191 mide 52 mm de largo y pesa 9 gramos; el EM7565 mide 42 mm y pesa 6,5 gramos.
- **Precisión de posicionamiento**: el dron depende muchísimo del GPS. La serie EM919x integra **GNSS de doble banda L1 + L5**, mucho más preciso que el GPS de banda única tradicional y con buena resistencia a interferencias.
- **Número de antenas**: la serie EM919x necesita las 4 antenas conectadas para explotar la capacidad MIMO; al diseñar la carcasa del dron hay que reservar sitio para esas 4 antenas. Si usted elige el EM9190 con antena mmWave adicional, el peso y el consumo se vuelven aterradores.

### Robot de inspección (Robot): sensible a la estabilidad y al coste
- El robot avanza despacio por el suelo y suele combinar un LiDAR para construir mapas; su dependencia del GPS no es profunda, así que basta el GPS de banda única integrado en el EM7565.
- Dentro del robot hay mucho espacio y una batería grande, pero en la planta normalmente solo hay señal 4G; entonces el EM7565 (Cat 12, subida de 150 Mbps) es más que suficiente, no hace falta forzar el 5G.

---

## Trampas de hardware que debe ver antes de despegar

Si usted es ingeniero de integración de hardware, antes de dibujar el módulo sobre la placa preste atención:

1. **No se deje engañar por el mmWave (ondas milimétricas)**: muchos creen que comprar 5G obliga a hacerse con el EM9190 más caro para jugar con ondas milimétricas. La realidad es que las ondas milimétricas penetran muy mal, y en Taiwán casi no existen redes privadas mmWave. Para el 99% de los drones, el **EM9191** con soporte Sub-6 es la elección perfecta, y le ahorra un montón de problemas con antenas externas.
2. **Cuidado con el sobrecalentamiento y el apagado**: las EM919x son bestias 5G, con límite rojo de temperatura interna en 115 °C (recomendado mantenerse por debajo de 100 °C). En verano, con el sol alto sobre el dron, si usted encierra el módulo en una carcasa de plástico sin circulación de aire, acabará bajando la velocidad o incluso cortándose la conexión.
3. **No escatime en los cables de antena**: la hoja de especificaciones exige una pérdida de antena inferior a 0,5 dB, con impedancia de 50 ohmios. Si usted compra un módulo de gama alta pero lo conecta con cables de antena baratos de mercadillo, la calidad de su vídeo será lamentable.

## Conclusión

Para construir una solución de conectividad fuera de la línea de visión (BVLOS), los módulos de Sierra Wireless ya le empaquetan «ancho de banda de vídeo, arquitectura de baja latencia y posicionamiento de alta precisión» en una pequeña tarjeta M.2.
Quien vuela en el cielo, tiene presupuesto y quiere una red privada 5G, que compre el **EM9191** directamente; quien camina por el suelo y solo necesita transmitir vídeo 1080p con estabilidad, elegir el **EM7565** es lo más tranquilo.

## Información de compra (Llamada a la acción)

¿Está diseñando la placa de comunicaciones de un dron o de un robot de inspección? ¿No sabe cómo planificar las antenas y la refrigeración? Yupitek (榆閤科技) ofrece módulos Sierra Wireless completos y un servicio de consultoría de integración de hardware.
Escríbanos: **sales@yupitek.com**
Vea los productos: [Sección de módulos Sierra Wireless](/es/products/sierra/)

---

## Preguntas frecuentes

{{< faq >}}
