---
title: "Guía de Mejora de Antenas del Controlador DJI: Amplíe el Alcance con Antenas ALFA (Edición 2026)"
description: "Análisis completo de la mejora de antenas del controlador DJI: qué modelos admiten antenas ALFA directamente, cuáles requieren desmontar la carcasa, comparativa de modelos compatibles, pasos de instalación y consideraciones normativas."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["DJI", "drone", "antenna-upgrade", "RP-SMA", "IPEX4", "range-extension", "ALFA-APA-M25", "ALFA-APA-M25-6E", "ALFA-ARS-25-57A", "ALFA-ARS-NT5B7"]
featureimage: "/images/blog/dji-drone-controller-antenna-upgrade.webp"
author: "benny-lai"
lastmod: 2026-08-31
faq:
  - question: "¿Reemplazar las antenas anula la garantía de DJI?"
    answer: "En el RC-N1, que conserva el conector RP-SMA hembra externo, la antena externa es una pieza de mantenimiento del usuario: el reemplazo en sí difícilmente afecta la garantía del cuerpo del controlador, pero conserve las antenas originales para reinstalarlas al enviarlo a servicio técnico. En los modelos con pantalla (RC2, RC Pro, Smart Controller), abrir la carcasa anula la garantía de inmediato, a diferencia del RC-N1."
  - question: "Mi controlador no tiene conector de antena con rosca visible. ¿Puedo actualizarlo de todos modos?"
    answer: "Sí, pero de otra forma. Los modelos con pantalla (RC2, RC Pro, Smart Controller) usan antenas fijas con conectores internos IPEX/IPEX4: puede conectar antenas ALFA externas desmontando la carcasa y añadiendo cables adaptadores, pero requiere experiencia en DIY/RF, anula la garantía y puede exigir perforar la carcasa (irreversible). Si no tiene esa experiencia, consulte un servicio de modificación profesional o mantenga la configuración original."
  - question: "¿Puedo usar estas antenas ALFA en sistemas FPV que no sean DJI?"
    answer: "Sí. Cualquier sistema de 2.4 GHz o 5.8 GHz compatible con RP-SMA es compatible, incluidos los transmisores y receptores ExpressLRS (ELRS) a 2.4 GHz, los sistemas FrSky R9 (915 MHz, requiere una antena distinta), TBS Crossfire (915 MHz, también incompatible, requiere antena de 900 MHz) y los transmisores de video (VTX) de 5.8 GHz con conector RP-SMA. Al elegir una antena de repuesto, haga coincidir tanto el tipo de conector como la banda de frecuencia."
  - question: "¿Qué diferencia hay entre reemplazar una antena o las dos en el RC-N1 de doble antena?"
    answer: "El sistema OcuSync de DJI usa las dos antenas para recepción de diversidad/MIMO, seleccionando continuamente la de señal más fuerte. Reemplazar solo una crea una configuración asimétrica: el sistema favorecerá la antena mejorada la mayor parte del tiempo, pero el rendimiento es máximo cuando ambas están emparejadas. Se recomienda reemplazar las dos."
  - question: "¿Necesito cambiar alguna configuración en la app DJI después de la mejora?"
    answer: "No. El controlador DJI gestiona automáticamente la selección de antena y de banda de frecuencia. No se requieren cambios de configuración en la app tras el intercambio físico de antena."
  - question: "¿Cómo elijo entre la APA-M25 y la ARS-25-57A?"
    answer: "Si durante el vuelo el controlador apunta de forma estable en una misma dirección, elija la APA-M25 (panel direccional, mayor ganancia). Si suele volar en círculos alrededor del piloto, en órbitas o en pasadas cercanas con grandes cambios de ángulo, o no quiere preocuparse por la orientación de la antena, elija la ARS-25-57A (paleta omnidireccional, sin necesidad de apuntar)."
---

{{< tldr >}}
No todos los controladores DJI permiten actualizar la antena sin abrir la carcasa. **Solo el RC-N1** conserva el conector RP-SMA hembra externo, sobre el que puede enroscar directamente las antenas ALFA a mano. **RC2, RC Pro y Smart Controller** —los modelos con pantalla— tienen antenas fijas que solo ajustan su ángulo; internamente usan conectores microcoaxiales de la serie IPEX, por lo que conectar una antena externa de alta ganancia exige desmontar la carcasa, añadir cables adaptadores y perder la garantía. Esta guía explica qué hacer en cada caso y qué antena ALFA elegir.
{{< /tldr >}}

Actualizar las antenas del controlador de un dron DJI es una de las mejoras de RF más accesibles para los operadores — pero solo si su modelo lo permite. La clave está en el conector: el **RC-N1** conserva un puerto **RP-SMA hembra** externo, el mismo estándar que usan las antenas accesorias de ALFA Network, de modo que puede desenroscar la antena de fábrica y enroscar una ALFA a mano, sin herramientas. En cambio, los modelos con pantalla como **RC2, RC Pro y Smart Controller** usan antenas fijas con conectores internos IPEX/IPEX4: para conectar una antena externa deberá desmontar la carcasa, añadir cables adaptadores y asumir la pérdida de garantía.

Esta guía revisada explica las dos situaciones por separado, compara los modelos de antenas ALFA compatibles, establece expectativas realistas de alcance y aborda el marco legal que debe conocer antes de volar con equipos de alcance extendido.

---

## Entendiendo las Antenas del Controlador DJI

### Rendimiento de la Antena de Fábrica

Las antenas estándar de los controladores DJI son **dipolos omnidireccionales rubber duck** con una ganancia aproximada de **2 dBi**. Están optimizadas para un tamaño compacto y una cobertura amplia, más que para el alcance máximo en una dirección específica. Para la mayoría de los vuelos recreativos a corta distancia su rendimiento es suficiente — pero dejan un margen de señal RF considerable sin aprovechar si usted opera cerca de los límites de su zona de vuelo legal.

### Bandas de Frecuencia

Los sistemas de transmisión **OcuSync 3 (O3)** y **O4** de DJI cubren:

- **2.4 GHz** — mejor penetración de obstáculos, preferida en entornos con RF congestionada
- **5.1 / 5.8 GHz** — mayor throughput y menor latencia, preferida en áreas abiertas

Los controladores de doble o triple banda activan varias bandas simultáneamente y el sistema selecciona automáticamente el canal más limpio.

### Tipos de Conector: Dos Diseños Completamente Distintos

Este es el punto central de la edición revisada. El diseño de antenas de los controladores DJI se divide en dos generaciones con dos arquitecturas completamente diferentes:

**① RP-SMA externo (enroscable directamente)**

Los modelos más antiguos, sin pantalla (por ejemplo, el **RC-N1**), conservan el diseño tradicional: en la base de la antena hay un collar metálico con rosca estriada visible, y el puerto es **RP-SMA hembra (Female)**. La antena correspondiente debe ser **RP-SMA macho (Male)** — exactamente la especificación que ofrecen las antenas accesorias de ALFA. En estos modelos puede retirar la antena de fábrica con la mano y enroscar una antena ALFA directamente, sin necesidad de ninguna herramienta.

**② Conector microcoaxial interno (requiere desmontar la carcasa)**

Los modelos más nuevos con pantalla —**RC2, RC Pro, Smart Controller**— siguen mostrando dos antenas en el exterior, pero son **fijas y solo permiten ajustar el ángulo**; no tienen rosca desmontable. Al abrir la carcasa se comprueba que internamente usan conectores microcoaxiales **IPEX, IPEX4** o similares, soldados directamente a la placa base, y la carcasa no tiene orificios roscados previstos para que el usuario los desenrosque.

> **Dato de contexto:** En las discusiones de la comunidad se ha señalado una hipótesis interesante: la especificación RP-SMA se creó, entre otras razones, precisamente para responder a la restricción estadounidense (FCC) de «antenas no desmontables». Dicho de otro modo, que DJI haya pasado deliberadamente a conectores microcoaxiales internos en lugar de RP-SMA externo en los controladores con pantalla probablemente no responde solo a la impermeabilización o la estética, sino a un **diseño que no prevé que el usuario cambie la antena**. Esto también explica por qué las antenas de los modelos nuevos son cada vez «menos desmontables».

**Cómo identificarlo:** observe la base de las antenas en la parte superior del controlador. Si hay un collar metálico con rosca estriada (hexagonal o moleteada) y la antena se afloja girándola a mano, es RP-SMA externo. Si la antena solo se inclina de lado a lado para ajustar el ángulo y la carcasa es continua y sin costuras, es un diseño interno que exige desmontar la carcasa para modificarlo.

---

## Por Qué las Antenas de Panel Mejoran el Alcance

### Direccional vs. Omnidireccional

Una antena rubber duck estándar irradia energía RF en un patrón aproximadamente esférico — 360° en el plano horizontal y aproximadamente hemisférico en vertical. Esto es ideal cuando no sabe dónde está el objetivo, pero la mayoría del tiempo el dron está frente a usted: esa forma de radiación desperdicia buena parte de la energía.

Una **antena de panel (patch)** concentra la energía RF en un cono orientado hacia adelante. La energía que de otro modo irradiaría hacia atrás, hacia los lados o hacia el suelo se redirige hacia el frente — aumentando la intensidad de señal efectiva en la dirección de vuelo **sin incrementar la potencia de transmisión**.

### Cálculo de Ganancia

Tomemos la **ALFA APA-M25** como ejemplo:

- **8 dBi** @ 2.4 GHz
- **10 dBi** @ 5.8 GHz

Frente a la antena de fábrica de 2 dBi, el panel de 10 dBi aporta unos **8 dB de ganancia adicional** en la dirección frontal:

> Cada 3 dB de ganancia duplica aproximadamente la potencia radiada efectiva en esa dirección.
> Una mejora de 8 dB ≈ intensidad de señal frontal **6 veces mayor**.

### Pérdida en el Espacio Libre

A 5.8 GHz, la pérdida en el espacio libre a 1 km es de aproximadamente **113 dB**. Un panel de 10 dBi recupera 8 dB de ese presupuesto de enlace, lo que retrasa de forma significativa el punto en que el enlace cae por debajo de la sensibilidad mínima de recepción.

### La Compensación

Las antenas direccionales exigen **mantener el panel orientado hacia el dron**. Para la mayoría de los vuelos en línea de visión directa esto se consigue con la postura natural de agarre; el ancho de haz de la APA-M25 es de unos 60–70°, suficiente para cubrir los arcos de vuelo típicos sin necesidad de reapuntar constantemente.

> **Consejo:** Si su patrón de vuelo exige grandes barridos en azimut (órbitas alrededor del piloto, pasadas cercanas), una antena omnidireccional (como la ARS-25-57A o la ARS-NT5B7) es más adecuada que un panel, porque no requiere ajustar la orientación de forma continua.

---

## Antenas ALFA Compatibles

Las cuatro antenas siguientes son todas **RP-SMA macho** y soportan las bandas que usan los sistemas O3/O4 de DJI:

### APA-M25 — Doble Banda 2.4/5 GHz (Mejor Opción)

La recomendación principal para la mayoría de los pilotos con DJI O3/O4: su cobertura de doble banda coincide perfectamente con las bandas que usa DJI, y su relación tamaño-rendimiento es excelente para uso en campo.

| Característica | Especificación |
|---|---|
| Ganancia | 8 dBi @ 2.4 GHz / 10 dBi @ 5 GHz |
| Ancho de haz | Horizontal 66° / Vertical 16° |
| Dimensiones | 167.3 × 66 × 18 mm |
| Peso | 72 g |
| Conector | RP-SMA Macho |

Con 72 gramos, no añade fatiga apreciable en vuelos prolongados, y el panel se asienta plano sobre la parte superior de la mayoría de los controladores DJI durante el vuelo. Si su modelo es **de doble antena y desmontable (RC-N1)**, reemplazar ambas por APA-M25 ofrece el mejor resultado.

👉 [Ver la página del producto APA-M25](/es/products/alfa/apa-m25/)

### APA-M25-6E — Triple Banda con 6 GHz (A Prueba de Futuro)

Añade soporte de la **banda de 6 GHz** a la base de doble banda de la APA-M25.

| Característica | Especificación |
|---|---|
| Ganancia | 8 dBi @ 2.4 GHz / 10 dBi @ 5 GHz / **9 dBi @ 6 GHz** |
| Ancho de haz | Horizontal 60° / Vertical aprox. 40–45° (varía ligeramente según el lote; consulte el etiquetado del embalaje) |
| Dimensiones / Peso | Igual que la APA-M25: 167.3 × 66 × 18 mm, 72 g |
| Conector | RP-SMA Macho |

**Relevancia actual para DJI:** ningún dron de consumo DJI utiliza hoy 6 GHz como enlace principal de control/video. Esta antena merece la pena si: también la usará con puntos de acceso o adaptadores Wi-Fi 6E, prevé futuros sistemas DJI que incorporen espectro de 6 GHz, o utiliza configuraciones FPV con enlaces de 6 GHz. Si hoy la usará solo con un controlador DJI, la APA-M25 estándar ofrece el mismo rendimiento práctico a menor costo.

👉 [Ver la página del producto APA-M25-6E](/es/products/alfa/apa-m25-6e/)

### ARS-25-57A — Paleta de Doble Banda (Mejora Cotidiana, Sin Apuntar)

Rinde mejor que una rubber duck y no exige la conciencia direccional de un panel: es **la ruta de actualización más simple** — desenrosque la antena de fábrica, enrosque la ARS-25-57A y vuele, sin ajustar la orientación.

| Característica | Especificación |
|---|---|
| Ganancia | 5 dBi @ 2.4 GHz / 7 dBi @ 5 GHz |
| Patrón de radiación | Omnidireccional |
| Dimensiones | 18.5 × 231 mm |
| VSWR | 2.5:1 |
| Temperatura de operación | −10°C ~ +55°C |
| Conector | RP-SMA Macho |

Frente a la antena de fábrica aporta una mejora medible de 3–5 dB en la calidad del enlace (según la banda), sin la carga operativa de gestionar la orientación de un panel. Es ideal para quien quiere completar la mejora en un solo paso y no pensar en la dirección de la antena durante el vuelo.

👉 [Ver la página del producto ARS-25-57A](/es/products/alfa/ars-25-57a/)

### ARS-NT5B7 — Dipolo de Triple Banda (Para Todo Clima)

Dipolo omnidireccional de grado industrial que cubre las tres bandas Wi-Fi modernas; más ligera y compacta que un panel.

| Característica | Especificación |
|---|---|
| Ganancia | 4 dBi @ 2.4 GHz / 5 dBi @ 5 GHz / 7 dBi @ 6 GHz |
| Dimensiones / Peso | ⌀13 × 196 mm, 20 g |
| Temperatura de operación | **−40°C ~ +85°C** (grado industrial) |
| Conector | RP-SMA Macho |

Su especificación de temperatura industrial la hace apta para volar en condiciones climáticas extremas — montañas en invierno, desiertos en verano. Donde la APA-M25 ofrece mayor ganancia frontal, la ARS-NT5B7 mantiene un patrón completamente omnidireccional, útil cuando no es posible apuntar el controlador con precisión (montaje en vehículo, trípode, operación con varios pilotos). Su perfil delgado también ofrece menos resistencia al viento al volar a mano con viento fuerte.

👉 [Ver la página del producto ARS-NT5B7](/es/products/alfa/ars-nt5b7/)

> **Nota:** También distribuimos la **APA-M04** de banda única (7 dBi @ 2.4 GHz), pero como solo soporta 2.4 GHz no la recomendamos para los sistemas de doble/triple banda de DJI, por lo que no figura en esta lista de recomendaciones.

---

## Guía de Compatibilidad de Conectores

### RP-SMA vs SMA: Distinción Crítica

Son casi idénticos en apariencia, pero física y eléctricamente incompatibles:

| Característica | SMA Estándar | RP-SMA (SMA de Polaridad Inversa) |
|---|---|---|
| Centro del conector macho | Pin (sólido) | Socket (hueco) |
| Centro del conector hembra | Socket (hueco) | Pin (sólido) |
| Uso típico | RF militar/industrial | Wi-Fi de consumo, DJI RC-N1, etc. |
| Antenas ALFA | ❌ No se usa | ✅ Toda la gama de antenas accesorias ALFA |

El RC-N1 usa un puerto **RP-SMA hembra** y las antenas accesorias ALFA usan **RP-SMA macho**: son directamente compatibles y se enroscan a mano. **No use nunca una antena SMA estándar en un puerto RP-SMA**: la orientación del pin/socket central está invertida y forzar la conexión puede doblar o romper el pin central, causando un daño irreparable.

### Cables de Extensión

Si desea montar la antena en un trípode o en un soporte de estación de tierra mientras opera el controlador por separado, puede usar un cable de extensión RP-SMA:

- **RG-316** — coaxial de baja pérdida, flexible, adecuado para uso en campo hasta 50 cm
- **RG-174** — pérdida ligeramente menor que RG-316 en distancias cortas, muy flexible
- Evite el cable genérico RG-58 — su pérdida a 5.8 GHz es alta y anularía la ganancia de la antena

Un cable RG-316 de 30 cm añade típicamente menos de 1 dB de pérdida, aceptable para la mayoría de las configuraciones.

---

## Tabla de Compatibilidad de Controladores

| Modelo de Controlador DJI | Bandas de Frecuencia | Diseño de Antena Externa | Conector Interno | ¿Antena ALFA Externa Sin Abrir la Carcasa? |
|---|---|---|---|---|
| **RC-N1** | 2.4 / 5.8 GHz | Antena roscada desmontable | RP-SMA hembra (externa) | ✅ **Sí**, basta enroscarla a mano |
| **RC2** (Air 3 / Air 3S / Mini 4 Pro) | 2.4 / 5.1 / 5.8 GHz | Fija, ángulo ajustable | IPEX4 (interna) | ❌ No, requiere desmontar + adaptador + perforación |
| **RC Pro** | 2.4 / 5.8 GHz | Fija, ángulo ajustable | Conector micro interno (IPEX4 o similar según modelo) | ❌ No, requiere desmontar + adaptador |
| **Smart Controller** | 2.4 / 5.8 GHz | Fija | IPEX (interna) | ❌ No, requiere desmontar + adaptador |
| DJI Goggles 2 | 2.4 / 5.8 GHz | Según modelo | Según modelo | Verifíquelo individualmente; esta tabla no lo cubre |

**Consejo:** Si no está seguro de a qué categoría pertenece su controlador, observe la base de la antena: si hay un collar con rosca estriada visible que se afloja a mano, es un diseño externo como el del RC-N1; si la antena solo se inclina para ajustar el ángulo y la carcasa es continua y sin costuras, es un diseño interno que exige desmontar la carcasa. **Intentar girar a la fuerza una antena de diseño interno puede dañar la base de la antena y el puerto del controlador; no lo intente sin confirmar antes el modelo.**

---

## Resultados de Pruebas de Alcance (Expectativas del Mundo Real)

Las cifras siguientes son observaciones de campo típicas en entornos con línea de visión directa despejada. Los resultados reales varían significativamente según la interferencia de RF local, el terreno, las condiciones atmosféricas y el modelo de dron.

| Configuración | Alcance Efectivo Típico | Notas |
|---|---|---|
| Antenas DJI de fábrica (ambas) | 1.5 – 3 km | Línea de visión despejada, entorno de baja interferencia |
| RC-N1 + APA-M25 (una) + fábrica | 2.5 – 4 km | Controlador apuntando hacia el dron |
| RC-N1 + APA-M25 (ambas reemplazadas) | 4 – 7 km | Ambos paneles apuntando al dron |
| RC-N1 + ARS-25-57A (ambas reemplazadas) | 2 – 4.5 km | Omnidireccional, sin necesidad de apuntar |
| RC-N1 + ARS-NT5B7 (ambas reemplazadas) | 2 – 4 km | Omni industrial, patrón de radiación similar |
| RC2/Smart Controller con modificación de carcasa + antena externa de alta ganancia | Según mediciones de la comunidad con arquitecturas similares, aprox. 30–50 % más que la de fábrica (p. ej., de 3 km a 4 km) | Requiere desmontar y perforar; el resultado varía según la calidad de la modificación y el entorno; datos solo de referencia |

**Recordatorio de límite legal:** El alcance extendido por la antena no autoriza volar más allá de los límites legales de ningún país. En la mayoría de las jurisdicciones —incluidas Taiwán, la Unión Europea, EE. UU., Japón y Australia— las operaciones de drones recreativas y comerciales exigen mantener **línea de visión directa (VLOS)** con la aeronave en todo momento. Las cifras técnicas anteriores pueden superar con creces su límite legal de operación. El valor de la mejora de antena es aumentar la **fiabilidad del enlace y el margen de señal dentro de su alcance legal**, no superar el límite de visión directa.

---

## Consideraciones Legales y Regulatorias

**Importante:** Extender el alcance RF de su controlador no otorga ningún permiso para volar más allá de los límites establecidos por la ley. En la mayoría de los países, volar más allá de la línea de visión directa (BVLOS) sin autorización específica es ilegal y conlleva sanciones graves.

### Requisitos de VLOS

| Jurisdicción | Límite Estándar | Autorización BVLOS |
|---|---|---|
| Taiwán (CAA) | VLOS requerida | Exención/permiso requerido |
| EE. UU. (FAA Part 107) | VLOS requerida | Exención BVLOS requerida |
| Unión Europea (EASA) | VLOS requerida | Autorización de operación específica |
| Japón (MLIT) | VLOS requerida | Certificación de Nivel 4 requerida |

### Implicaciones de la Certificación de Tipo

Reemplazar las antenas externas del controlador puede afectar su estado de **certificación CE, FCC u homologación local**. El controlador fue certificado con sus antenas de fábrica; instalar una antena de mayor ganancia puede hacer que el sistema supere la potencia isotrópica radiada efectiva (EIRP) certificada para su banda.

- Taiwán: operar equipos de radio que superen los límites de EIRP de la NCC (Comisión Nacional de Comunicaciones) viola la Ley de Gestión de Telecomunicaciones.
- EE. UU.: las reglas FCC Part 15 restringen el EIRP de los dispositivos sin licencia.
- **Las antenas ALFA se venden como piezas de repuesto accesorias**; la instalación, la verificación de cumplimiento y la responsabilidad legal recaen en el usuario final.
- Si su modelo exige desmontar la carcasa (RC2/RC Pro/Smart Controller), se añaden además la **pérdida de garantía** y la **perforación irreversible de la carcasa**; evalúe ambas antes de empezar.

**Nota práctica:** En la mayoría de los controladores DJI que operan dentro de su presupuesto de EIRP diseñado, sustituir la antena de fábrica de 2 dBi por un panel ALFA de alta ganancia cambia la ganancia de la antena, pero la potencia de salida del transmisor permanece igual. Que el EIRP resultante supere o no los límites locales depende de la potencia de salida certificada original de su modelo concreto; consulte la documentación regulatoria de su controlador DJI para conocer sus valores de EIRP certificados.

---

## Pasos de Instalación

La instalación difiere mucho según el modelo. Primero confirme a qué categoría pertenece su controlador con la «Tabla de Compatibilidad de Controladores» anterior y luego siga la sección correspondiente.

### A. RC-N1 (RP-SMA externo, sin desmontar la carcasa)

**Lo que necesita:** una antena ALFA con conector RP-SMA macho y su controlador DJI.

1. **Apague el controlador** — asegúrese de que esté apagado antes de desconectar cualquier antena.
2. **Sujete la antena de fábrica por la base**, cerca del cuerpo del controlador — no por el cuerpo de la antena.
3. **Gire en sentido antihorario** para desenroscar; debería soltarse después de 3–4 vueltas.
4. **Inspeccione el puerto RP-SMA hembra** para confirmar que no haya residuos ni pines doblados.
5. **Enrosque a mano el conector RP-SMA macho de la antena ALFA** en el puerto, girando en sentido horario.
6. **Apriete hasta quedar firme a mano** — contacto sólido, pero sin herramientas ni fuerza excesiva; los conectores SMA/RP-SMA están diseñados solo para apriete manual.
7. Si el controlador tiene dos puertos, **repita los pasos con la segunda antena**.
8. **Guarde las antenas de fábrica en un lugar seguro** — las necesitará si envía el controlador a servicio técnico.
9. Encienda y pruebe en un campo abierto y seguro para confirmar la intensidad de señal y el comportamiento de vuelo.

**Orientación de la antena:**
- Antenas de panel (APA-M25/APA-M25-6E): la cara frontal debe apuntar hacia la zona de vuelo principal; con dos paneles, móntelos al mismo ángulo o en una ligera forma de V (unos 15° de separación) para ampliar la cobertura horizontal.
- Antenas de dipolo/paleta (ARS-NT5B7, ARS-25-57A): instálelas en posición vertical para obtener la mejor cobertura omnidireccional en el plano horizontal.

### B. RC2 / RC Pro / Smart Controller (diseño interno, requiere desmontar la carcasa)

> ⚠️ **Este procedimiento desmonta la carcasa del controlador y puede exigir perforarla: es una modificación irreversible que anula la garantía de DJI de inmediato.** Se recomienda solo a usuarios con experiencia en DIY/modificaciones de RF. Si no está seguro de poder desmontar el equipo, consulte un servicio de modificación profesional o mantenga la configuración original.

**Lo que necesita:**
- Cables adaptadores IPEX (o IPEX4, según el modelo) hembra → RP-SMA hembra (bulkhead) × 2
- Destornillador de cruz
- Taladro o cúter (si debe perforar la carcasa para instalar la base RP-SMA; el diámetro depende de la especificación del adaptador, normalmente unos 6–8 mm)
- Antenas ALFA × 2 (se recomienda APA-M25 o ARS-25-57A)
- Pegamento termofusible o sellador impermeable (para fijar la base del adaptador y reforzar el orificio contra polvo y humedad)
- Para el Smart Controller, además: pistola de aire caliente (para ablandar y retirar las almohadillas laterales)

**Pasos:**

1. **Apague y retire la batería/desconecte la alimentación** para evitar riesgo de cortocircuito.
2. **Desmonte la carcasa**: retire los tornillos de fijación de la parte trasera (en el Smart Controller, primero retire las almohadillas laterales con la pistola de aire caliente y luego los tornillos de la tapa trasera), abra con cuidado los enganches y no tire con fuerza de los cables planos.
3. **Localice los conectores de antena originales**: encuentre los conectores IPEX/IPEX4 de antena en la placa base.
4. **Desconecte los conectores originales**: tire verticalmente y con suavidad para no dañar el zócalo de la placa.
5. **Elija la posición del orificio** (si es necesario): un lateral o la parte superior de la carcasa que no afecte al agarre ni al espacio interno.
6. **Perfore y pruebe el montaje de la base**, verificando el ajuste y eliminando las rebabas.
7. **Conecte los cables adaptadores**: el extremo IPEX vuelve al zócalo original de la placa; el extremo RP-SMA hembra se fija desde el interior de la carcasa, dejando la rosca visible en el exterior.
8. **Haga las dos antenas** para evitar una recepción de diversidad/MIMO asimétrica.
9. **Selle contra el polvo**: refuerce el borde del orificio para impedir la entrada de objetos extraños y humedad.
10. **Vuelva a montar la carcasa** y atornille todos los tornillos originales.
11. **Enrosque las antenas ALFA** a mano, sin aplicar fuerza excesiva.
12. **Encienda y pruebe** en un campo abierto y seguro, verificando señal y alcance.

---

## Preguntas Frecuentes

**P: ¿Reemplazar las antenas anula la garantía de DJI?**

R: En los modelos con conector RP-SMA hembra externo, como el RC-N1, la antena externa es una pieza de mantenimiento del usuario: el reemplazo en sí difícilmente afecta la garantía del cuerpo del controlador, pero conserve las antenas originales para reinstalarlas al enviarlo a servicio técnico. **En los modelos que exigen desmontar la carcasa (RC2, RC Pro, Smart Controller), abrirla anula la garantía de inmediato** — a diferencia del RC-N1. Confirme primero su modelo antes de decidir.

**P: Mi controlador no tiene conector de antena con rosca visible. ¿Puedo actualizarlo de todos modos?**

R: Sí, pero de otra forma. Modelos como RC2, RC Pro y Smart Controller no tienen conector roscado externo, pero aun así puede conectar antenas ALFA externas desmontando la carcasa y añadiendo cables adaptadores. Requiere cierta experiencia en DIY/modificaciones de RF, anula la garantía y puede exigir perforar la carcasa (irreversible). Si no tiene esa experiencia, consulte un servicio de modificación profesional o mantenga la configuración original.

**P: ¿Puedo usar estas antenas ALFA en sistemas FPV que no sean DJI?**

R: Sí. Cualquier sistema de 2.4 GHz o 5.8 GHz compatible con RP-SMA es compatible, incluidos:

- **ExpressLRS (ELRS)**: transmisores y receptores que operan a 2.4 GHz
- **Sistemas FrSky R9** (nota: R9 opera a 915 MHz — una frecuencia distinta que requiere otra antena)
- **TBS Crossfire** (915 MHz — también incompatible; requiere una antena de 900 MHz)
- **Transmisores de video (VTX)** de 5.8 GHz con conector RP-SMA

Al elegir una antena de repuesto, haga coincidir tanto el tipo de conector **como** la banda de frecuencia.

**P: ¿Qué diferencia hay entre reemplazar una antena o las dos en el RC-N1 de doble antena?**

R: El sistema OcuSync de DJI usa las dos antenas para **recepción de diversidad/MIMO**, seleccionando continuamente la de señal más fuerte. Reemplazar solo una con un panel de alta ganancia crea una configuración asimétrica, con una diferencia de rendimiento notable entre ambas. El sistema favorecerá la antena mejorada la mayor parte del tiempo, pero el rendimiento es máximo cuando ambas están emparejadas; se recomienda reemplazar las dos.

**P: ¿Necesito cambiar alguna configuración en la app DJI después de la mejora?**

R: No. El controlador DJI gestiona automáticamente la selección de antena y de banda de frecuencia. No se requieren cambios de configuración en la app tras el intercambio físico de antena.

**P: ¿Cómo elijo entre la APA-M25 y la ARS-25-57A?**

R: Si durante el vuelo el controlador apunta de forma estable en una misma dirección, elija la **APA-M25** (panel direccional, mayor ganancia). Si suele volar en órbitas alrededor del piloto, en círculos o en pasadas cercanas con grandes cambios de ángulo, o no quiere preocuparse por la orientación de la antena, elija la **ARS-25-57A** (paleta omnidireccional, sin necesidad de apuntar).

---

## Conclusión

La mejora de antenas del controlador DJI ofrece resultados y complejidad muy distintos según el modelo. Los controladores que conservan el conector RP-SMA externo, como el **RC-N1**, representan una de las mejoras de RF más accesibles y rentables para los operadores de drones: basta enroscar a mano, sin ninguna herramienta. En cambio, los modelos más nuevos con pantalla —**RC2, RC Pro, Smart Controller**— han pasado a antenas fijas de diseño interno: si realmente desea conectar una antena externa de alta ganancia, deberá desmontar la carcasa, añadir cables adaptadores y asumir la pérdida de garantía — algo que debe conocer bien antes de empezar.

Sea cual sea su modelo, el objetivo de la mejora de antena es aumentar la **fiabilidad y el margen de enlace dentro de su zona de vuelo legal**, no superar el alcance que permiten las regulaciones. Vuele de manera responsable, conserve las piezas originales en lugar seguro y disfrute de una mejor calidad de enlace.

---

## Referencias

1. [Sitio oficial de DJI — Especificaciones de controladores remotos](https://www.dji.com/)
2. [Página de soporte de DJI RC 2](https://www.dji.com/support/product/rc-2)
3. [FCC Part 15 — Normativa de dispositivos de radiofrecuencia sin licencia](https://www.fcc.gov/engineering-technology-laboratory-division/general/radio-spectrum-and-rulemaking)
4. [Sitio oficial de ALFA Network — Especificaciones de accesorios de antena](https://www.alfa.com.tw/)
5. [Comisión Nacional de Comunicaciones de Taiwán (NCC) — Ley de Gestión de Telecomunicaciones](https://www.ncc.gov.tw/)
6. [Documentación del estándar IEEE 802.11 — Especificaciones de redes de área local inalámbricas](https://standards.ieee.org/ieee/802.11/)
7. Hilos de la comunidad mavicpilots.com: «RC2 / RC external antenna mod», «RC 2 and RC Pro controller external antennae», «Connecting external antennas to the RC Plus» (2024)
8. Alientech — Tutorial de modificación «How to modify antenna of the DJI smart controller» (2019)