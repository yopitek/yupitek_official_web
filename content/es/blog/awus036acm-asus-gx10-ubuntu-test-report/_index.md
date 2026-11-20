---
title: "AWUS036ACM, prueba práctica: capacidades de Monitor / Inyección / AP y mesh del MediaTek MT7612U (mt76x2u) en ASUS GX10 + Ubuntu 24.04 (ARM64)"
slug: awus036acm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acm
  - mt7612u
  - mt76x2u
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - mesh
description: "El AWUS036ACM (MT7612U) funciona en Ubuntu 24.04 ARM64 sin instalar controladores: modo monitor en doble banda y aircrack-ng (habitual en Kali) disponibles, inyección de paquetes 2.4G 63–83% y 5G 76%, con soporte de VIF y mesh / IBSS en un solo equipo."
faq:
  - question: "¿El AWUS036ACM necesita instalar controladores en Ubuntu o Kali?"
    answer: "No. El MT7612U lo gestiona el controlador mt76x2u integrado en el kernel; en Ubuntu 24.04 (kernel 6.17) se reconoce nada más conectarlo, sin DKMS y sin cargar firmware a mano. La plataforma de esta prueba es Ubuntu 24.04 ARM64; en Kali, con un kernel suficientemente reciente, el comportamiento debería ser el mismo en principio, pero esta vez no se verificó en Kali sobre hardware real."
  - question: "¿El AWUS036ACM puede entrar en modo monitor y hacer inyección de paquetes? ¿Con qué tasa de éxito?"
    answer: "Sí. Tanto en 2.4GHz como en 5GHz entra en modo monitor y captura con normalidad; en la prueba de inyección con aireplay-ng alcanza 63–83% en 2.4GHz y 76% en 5GHz, un nivel intermedio dentro de las nueve tarjetas. Si necesita 100% de inyección en ambas bandas, en las pruebas de Yupitek destacan el AWUS036ACH y el AWUS036EACS."
  - question: "¿El AWUS036ACM puede crear un punto de acceso y conectarse a Internet al mismo tiempo (VIF)?"
    answer: "Sí. Se verificaron las dos combinaciones: STA+AP (conectado a la red superior por un lado y con punto de acceso abierto por otro) y AP+monitor (punto de acceso abierto y captura simultánea). Aquí es donde la concurrencia de múltiples interfaces del controlador mt76 es más completa; el punto de acceso en 5GHz puede abrirse a VHT 80 MHz."
  - question: "¿El AWUS036ACM admite mesh (802.11s) e IBSS?"
    answer: "Se puede crear en un solo equipo. En Ubuntu 24.04 / kernel 6.17, el AWUS036ACM puede crear interfaces mesh 802.11s e IBSS (Ad-hoc); pero esta vez no había un segundo nodo, así que la interconexión multinodo no se ha verificado y solo podemos afirmar que se crea en local."
  - question: "¿El AWUS036ACM puede capturar el handshake WPA?"
    answer: "Sí. Frente a nuestro propio AP y nuestro propio iPhone 7 Plus, la prueba de extremo a extremo tuvo éxito: deauth, captura del 4-way completo (M1–M4) y exportación de un .22000 para hashcat con hcxpcapngtool --all. Solo en redes propias o autorizadas."
draft: false
---

> Este artículo es el registro de pruebas prácticas de compatibilidad y capacidades del ALFA AWUS036ACM realizadas por Yupitek sobre una plataforma Linux reciente, pensado para la evaluación y selección de modelo.
> Plataforma de prueba: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Todos los datos son extractos de pruebas prácticas realizadas por Yupitek sobre **equipo propio y la Wi-Fi propia de la oficina** (SSID `YUPITEK`, 2.4G ch5 / 5G ch36, ch157) frente a un **teléfono de prueba propio** (Apple iPhone 7 Plus; WPA3 también se verificó con un iPhone 15 Pro).
> ⚠️ **Declaración legal y de alcance**: el modo monitor, la inyección y la captura de handshake solo se realizan en redes y dispositivos propios o para los que se cuenta con autorización; en modo AP, respete la normativa de radio local. Este artículo se centra en las capacidades, la compatibilidad y la configuración de la propia tarjeta, y **no contempla ninguna operación de ataque contra redes de terceros**.

## Resumen (TL;DR)

Según las pruebas de Yupitek (distribuidor de ALFA Network en Taiwán) en ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17), la AWUS036ACM funciona en modo monitor de doble banda, logra una inyección de paquetes del 63–83% en 2.4G y del 76% en 5G, y monta un punto de acceso en ambas bandas (5G a VHT 80 MHz).

- En Ubuntu 24.04 (ARM64) no hace falta instalar controladores: el MT7612U lo gestiona el mt76x2u integrado en el kernel 6.17; se reconoce nada más conectarlo, sin DKMS.
- Modo monitor en doble banda disponible; la inyección de paquetes es 63–83% en 2.4G y 76% en 5G, un nivel intermedio entre las nueve tarjetas.
- Se pueden crear mesh 802.11s e IBSS en un solo equipo, y admite VIF (STA+AP, AP+monitor).
- La captura de handshake WPA es de extremo a extremo (4-way completo, exportado a `.22000` para hashcat); es una de las 7 de 9 tarjetas que lo completaron.
- Si quiere 100% de inyección en ambas bandas, se recomienda el AWUS036ACH o el AWUS036EACS.

---

## 1. Esta tarjeta y la plataforma de prueba

El AWUS036ACM es la tarjeta MediaTek de doble banda dentro de la línea de ALFA, con chip MT7612U, Wi-Fi 5 (802.11ac), 2T2R (dos flujos espaciales) y doble banda 2.4GHz / 5GHz. En la lista de morrownr figura desde hace tiempo como tarjeta recomendada para Kali, y no por sus cifras de rendimiento, sino porque la familia de controladores `mt76` ofrece un soporte relativamente completo de modo monitor, inyección y concurrencia de múltiples interfaces (VIF) en Linux; modos experimentales como el mesh 802.11s, en esta plataforma, solo arrancan en el campo mt76 (las tarjetas Realtek solo pueden crear un IBSS en local y no levantan mesh). Por eso, al evaluar esta tarjeta, lo importante no es la velocidad, sino si el conjunto de capacidades está completo, si las características propias de mt76 realmente se materializan y qué puntos deben marcarse honestamente como límites.

Esta ronda mantiene el mismo escenario operativo: la tarjeta de red integrada del GX10 (`wlP9s9`) se encarga de la salida a Internet y el AWUS036ACM, conectado por USB, asume únicamente las tareas de prueba; al cambiar a monitor o AP no se toca la red del propio equipo. Durante todo el proceso solo se opera sobre la interfaz `wlx*` correspondiente a la tarjeta ALFA, sin tocar la tarjeta integrada de salida a Internet.

| Elemento | Contenido |
|---|---|
| Modelo | AWUS036ACM |
| Chip | MediaTek MT7612U (Wi-Fi 5 / 802.11ac, 2T2R dos flujos) |
| Controlador | `mt76x2u` (integrado en el kernel, incluido en el kernel 6.17) |
| Generación / flujos | Wi-Fi 5 / 2T2R |
| Nota | Tarjeta recomendada para Kali por morrownr |
| Plataforma | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| Dispositivo de prueba | Apple iPhone 7 Plus (WPA3 también probado con iPhone 15 Pro) |
| Entorno de prueba | Wi-Fi propia de oficina, SSID `YUPITEK`, 2.4G ch5 / 5G ch36, ch157 |

> La tabla general de esta ronda no registra los campos de USB ID ni de versión de firmware del AWUS036ACM (marcados como «—»), por lo que este artículo no especula sobre esos dos valores; todos los datos de capacidades que siguen se basan en las filas del ACM de la tabla general.

---

## 2. Hardware y controlador (sin instalación)

Esta tarjeta se reconoce nada más conectarla en el GX10, sin compilar y sin DKMS. El MT7612U lo gestiona directamente el controlador `mt76x2u` integrado en el kernel mainline, sin necesidad de ningún proyecto out-of-tree externo ni de cargar a mano un blob de firmware. Para ARM64, esta es la ventaja más práctica de mt76. Muchos controladores Realtek de terceros no traen binarios precompilados para aarch64 y hay que compilarlos uno mismo contra la versión del kernel; mt76, al ir integrado en el kernel, no se queda bloqueado por dependencias de controlador al actualizar el kernel.

Al conectar la tarjeta, la interfaz se nombra como `wlx` + MAC (por ejemplo, `wlxXXXXXXXXXXXX`); el nombre queda ligado a la MAC y no cambia al reconectar, lo que resulta útil para fijarlo en scripts. Para confirmar el enlace del controlador y la creación de la interfaz, puede usar la siguiente comprobación genérica (el nombre de la interfaz y el número de phy variarán según la máquina):

```bash
# Localizar el nombre de la interfaz de la tarjeta ALFA (solo las que empiezan por wlx, sin tocar la integrada wlP9s9)
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"

# Confirmar que el controlador enlazado es mt76x2u
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# mt76x2u

# Listar los modos de interfaz que declara soportar ese phy (determina qué capacidades se podrán usar después)
iw phy "$(cat /sys/class/net/$IF/phy80211/name)" info | sed -n '/Supported interface modes/,/Band 1/p'
```

Según las pruebas de esta ronda, los modos de interfaz disponibles en `mt76x2u` son más completos que en el `rtw88` de Realtek: además de managed / AP / monitor, también se levantan en local IBSS y mesh point (véase la sección 4). Esto es lo que da al ACM su base para ejecutar mesh / IBSS en un solo equipo; las tarjetas Realtek de la misma plataforma (como el AWUS036ACH), aunque también pueden crear un IBSS en local, no levantan ni el mesh 802.11s ni el active monitor en esta plataforma.

---

## 3. Capacidades probadas: Monitor / Inyección / AP / WPA3

Primero, la tabla general de capacidades principales (tomada de la fila 1 de la tabla de nueve tarjetas) y luego el desglose punto por punto. Todo se completó sobre el AP propio `YUPITEK` y el iPhone 7 Plus propio.

| Capacidad | 2.4 GHz | 5 GHz | Descripción |
|---|---|---|---|
| Monitor (recepción de escucha) | ✅ | ✅ | Ambas bandas entran en monitor y capturan con normalidad |
| Inyección (de paquetes) | ✅ 63–83% | ✅ 76% | Tasa de éxito de inyección en el test de inyección estándar |
| AP (hostapd) | ✅ | ✅ 80MHz | En 5G puede abrirse a VHT 80 MHz |
| WPA3-SAE (lado AP) | ✅ | No probado | WPA3-SAE se probó solo en 2.4 GHz; 5 GHz no se probó |

### 3-1. Monitor (2.4 GHz + 5 GHz) ✅

Tanto en 2.4 GHz como en 5 GHz entra en monitor y captura paquetes con normalidad; es la capacidad menos discutible de esta tarjeta. Para una tarjeta 2T2R de doble antena, la recepción de escucha es estable en ambas bandas, suficiente para sostener el inventario de canales y el diagnóstico de paquetes sobre el terreno.

### 3-2. Inyección (de paquetes) ✅ (nivel intermedio)

Midiendo la fiabilidad de la inyección de paquetes con el test de inyección estándar, el AWUS036ACM alcanza 63–83% en 2.4 GHz y 76% en 5 GHz. Dentro de las nueve tarjetas es un nivel intermedio, claramente por debajo del Realtek RTL8812AU (AWUS036ACH, 100% en ambas bandas) y del RTL8821CU (AWUS036EACS, 100% en ambas bandas), pero con funcionalidad completa y suficiente en la práctica. El ACM puede inyectar; solo que su estabilidad no es la más alta de la clase. Si un cliente pone por delante «que la tasa de éxito de inyección sea la mejor», esta no es la primera opción (véase la selección de modelo en la sección 5).

Antes de inyectar en 5 GHz, conviene tener en cuenta un detalle de configuración: el dominio regulatorio por defecto bloquea la transmisión activa en parte de las bandas UNII, así que antes de la prueba hay que cambiar el dominio regulatorio a una configuración que permita emitir y, al terminar, volver al dominio local (`iw reg set US` → prueba → `iw reg set TW`). Esto es el requisito previo para que 5 GHz pueda emitir correctamente y no tiene que ver con la capacidad de la propia tarjeta.

### 3-3. AP y WPA3-SAE ✅

El AWUS036ACM puede actuar como AP, tanto en 2.4 GHz como en 5 GHz, y en 5 GHz incluso puede abrirse a un ancho de banda de 80 MHz (VHT80). Tras activar WPA3-SAE en el lado AP en 2.4 GHz, el teléfono de prueba propio se conecta con normalidad (WPA3 en 5 GHz no se probó).

Aquí vale la pena contrastarlo con el AWUS036ACHM, el modelo de una sola antena también basado en mt76: el WPA3 del ACHM requiere fijar expresamente el `sae_pwe` de hostapd a 0, de lo contrario el iPhone 7 Plus no logra conectarse. El AWUS036ACM no tuvo esa limitación en esta ronda: WPA3-SAE funciona directamente.

---

## 4. Capacidades avanzadas: VIF / mesh / IBSS en local y sus límites

Un nivel más de profundidad: handshake, interfaz virtual (VIF), active monitor y mesh / IBSS. Esta sección es también donde el AWUS036ACM marca distancia con las tarjetas Realtek.

| Elemento avanzado | Resultado ACM | Descripción |
|---|---|---|
| Captura de handshake WPA | ✅ extremo a extremo (.22000) | Deauth a nuestro iPhone 7 Plus, captura del 4-way completo M1–M4, exportación de `.22000` para hashcat |
| VIF (concurrencia de múltiples interfaces) | ✅ STA+AP / AP+mon | Se puede STA+AP o AP+monitor a la vez |
| Active monitor | 🟡 configurable, ACK sin verificar | El modo se crea, pero el comportamiento de respuesta ACK no se ha verificado |
| Ad-hoc (IBSS) | 🟡 en local | Se crea la interfaz en un solo equipo; la interconexión requiere un segundo equipo |
| Mesh (802.11s) | 🟡 en local | Se crea la interfaz en un solo equipo; la interconexión requiere un segundo equipo |
| Wi-Fi Direct (P2P) | ⬜ requiere un segundo equipo | No probado en esta ronda |

### 4-1. VIF (concurrencia de interfaces virtuales) — el punto fuerte del ACM ✅

Esta tarjeta puede ejecutar dos interfaces virtuales a la vez. En esta ronda se verificaron las dos combinaciones: STA+AP (conectado a la red superior por un lado y con punto de acceso abierto por otro) y AP+monitor (punto de acceso abierto por un lado y captura por otro), adecuadas para escenarios como «conectar y observar a la vez» o «una sola tarjeta actuando de cliente y de estación base simultáneamente». Aquí es donde la concurrencia de múltiples interfaces del controlador `mt76` es más completa.

### 4-2. mesh / IBSS «se puede en local» — la diferencia clave de mt76 🟡

El AWUS036ACM puede levantar en un solo equipo las interfaces de mesh 802.11s y ad-hoc (IBSS); los Realtek `rtw88` / `rtw89` (AWUS036ACH, AWUS036AX, etc.), aunque también crean un IBSS en local, no admiten mesh 802.11s en esta plataforma. Así que, para hacer experimentos de mesh 802.11s, las tarjetas mt76 (ACM / ACHM) ofrecen un punto de partida que las Realtek no tienen.

Hay que marcar bien el límite: lo que se confirma en esta ronda es que «se puede crear la interfaz en un solo equipo»; la interconexión multinodo completa todavía requiere una segunda tarjeta / un segundo nodo y no se ha realizado, por lo que aquí se marca 🟡 (en local) y no ✅.

### 4-3. Límites honestos de las capacidades

- **handshake**: el ACM completó la cadena de extremo a extremo (deauth de un dispositivo propio → captura del 4-way completo M1–M4 → `hcxpcapngtool --all` para exportar el `.22000` de hashcat), aunque su tasa de éxito de inyección (2.4G 63–83% / 5G 76%) es inferior a la de las tarjetas Realtek.
- **active monitor**: el modo puede configurarse, pero el comportamiento de respuesta ACK no se ha verificado en esta ronda (marcado 🟡). A nivel de plataforma, relacionado con esto: `hcxdumptool` 8.x devuelve `failed to arm` en todas las tarjetas salvo el AWUS036EACS en 2.4 GHz (requiere active-monitor, que ni el chip triband integrado de esta plataforma ni los controladores actuales proporcionan), por lo que el flujo de handshake del ACM se hace con `airodump-ng` + `aireplay-ng`.
- **Wi-Fi Direct (P2P)**: no probado en esta ronda; requiere un segundo equipo.

### 4-4. Notas de operación en la plataforma (GX10 ARM64, relativas al ACM)

1. **No corte su propia red**: nunca ejecute `airmon-ng check kill` (cierra NetworkManager y deja al GX10 sin conexión); opere solo sobre `wlx*`, sin tocar la `wlP9s9` integrada de salida a Internet.
2. **Resolución de RX stall**: si tras alternar repetidamente entre monitor / AP de pronto no detecta nada, basta con **desconectar y reconectar** la tarjeta una vez para recuperarla (re-enumeración USB; el nombre de la interfaz lo determina la MAC y no cambia).
3. **Desbloqueo de TX en 5 GHz**: antes de la inyección en 5 GHz, configure el dominio regulatorio correcto para desbloquear la potencia de TX y, al terminar, vuelva al dominio local.
4. **Técnica de captura de handshake**: en la oficina suele haber varios AP con el mismo nombre; en la práctica es más estable no fijar un único `--bssid` y capturar el canal entero; para la conversión use `hcxpcapngtool --all`.
5. **Cadena de herramientas en ARM64**: `aircrack-ng` hay que compilarlo desde el código fuente; para `wifite` use la versión git 3.0.0 (evita el conflicto de dependencias de apt).

Las herramientas de Kali a nivel de plataforma (`airmon-ng`, `kismet`, `bettercap`, `wifite` versión git, Wireshark / tshark) pueden usar el ACM como fuente de datos con normalidad; la única excepción es el mencionado `hcxdumptool`, que requiere active-monitor.

---

## 5. Escenarios de uso y selección de modelo (vuelta al Hub)

Al contrastar las capacidades anteriores con el posicionamiento del producto, el papel del AWUS036ACM queda bastante claro: una tarjeta Wi-Fi 5 2T2R equilibrada en capacidades, sin instalar controladores y con las ventajas exclusivas de mesh / IBSS / VIF de mt76. ¿En qué escenarios conviene usarla?

- **La primera opción para experimentos de mesh (802.11s)**: entre estas nueve tarjetas, solo las mt76 ACM / ACHM pueden crear una interfaz de mesh 802.11s en un solo equipo; los Realtek `rtw88` / `rtw89` pueden crear un IBSS en local, pero no admiten mesh 802.11s. Para hacer experimentos de mesh, el ACM es el punto de partida correcto.
- **Cuando se necesita concurrencia VIF**: tanto STA+AP como AP+monitor funcionan, adecuado para que una sola tarjeta actúe de cliente y AP a la vez, o para conectar y monitorizar al mismo tiempo.
- **Cuando se valora una operación sin controladores**: `mt76x2u` integrado en el kernel; una actualización de kernel no bloquea el controlador y en ARM64 evita la molestia de compilar módulos out-of-tree.
- **Escenarios en los que no es la mejor opción**: si la necesidad central es «la máxima tasa de éxito de inyección», la inyección del ACM (2.4G 63–83% / 5G 76%) no es la más alta de la clase; se recomienda el Realtek AWUS036EACS / ACH / ACS; y si busca la mejor recepción / monitor de larga distancia, mire el AWUS036AXER / ACH.

En comparación con la misma familia, las diferencias de posicionamiento son estas:

| Necesidad | Tarjeta recomendada | Motivo |
|---|---|---|
| Experimentos de mesh (802.11s) en un solo equipo | **AWUS036ACM** / AWUS036ACHM | El controlador `mt76` puede crear mesh 802.11s en local (Realtek solo IBSS en local, sin mesh) |
| Concurrencia VIF (STA+AP / AP+mon) | **AWUS036ACM** | La concurrencia de múltiples interfaces funciona |
| 100% de inyección en ambas bandas / handshake de extremo a extremo | AWUS036EACS, AWUS036ACH, AWUS036ACS | La mejor inyección en ambas bandas, extremo a extremo `.22000` ya evidenciado |
| Máxima recepción / monitor de larga distancia | AWUS036AXER, AWUS036ACH | El escaneo por salto de canal detecta más objetivos / doble antena de alta ganancia |

Selección en una frase: si quiere jugar con mesh / IBSS, necesita concurrencia VIF y además una operación sin controladores, el AWUS036ACM es la tarjeta mt76 más idónea del lote; si quiere 100% de inyección en ambas bandas, tire hacia el EACS / ACH. Para la comparación horizontal completa de las nueve tarjetas y la decisión de selección, véase [Hub de evaluación de adaptadores inalámbricos ALFA (tabla general de nueve tarjetas)](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

---

## Preguntas frecuentes (FAQ)

**P: ¿El AWUS036ACM necesita instalar controladores en Ubuntu o Kali?**
No. El MT7612U lo gestiona el controlador mt76x2u integrado en el kernel; en Ubuntu 24.04 (kernel 6.17) se reconoce nada más conectarlo, sin DKMS y sin cargar firmware a mano. La plataforma de esta prueba es Ubuntu 24.04 ARM64; en Kali, con un kernel suficientemente reciente, el comportamiento debería ser el mismo en principio, pero esta vez no se verificó en Kali sobre hardware real.

**P: ¿El AWUS036ACM puede entrar en modo monitor y hacer inyección de paquetes? ¿Con qué tasa de éxito?**
Sí. Tanto en 2.4GHz como en 5GHz entra en modo monitor y captura con normalidad; en la prueba de inyección con aireplay-ng alcanza 63–83% en 2.4GHz y 76% en 5GHz, un nivel intermedio dentro de las nueve tarjetas. Si necesita 100% de inyección en ambas bandas, en las pruebas de Yupitek destacan el AWUS036ACH y el AWUS036EACS.

**P: ¿El AWUS036ACM puede crear un punto de acceso y conectarse a Internet al mismo tiempo (VIF)?**
Sí. Se verificaron las dos combinaciones: STA+AP (conectado a la red superior por un lado y con punto de acceso abierto por otro) y AP+monitor (punto de acceso abierto y captura simultánea). Aquí es donde la concurrencia de múltiples interfaces del controlador mt76 es más completa; el punto de acceso en 5GHz puede abrirse a VHT 80 MHz.

**P: ¿El AWUS036ACM admite mesh (802.11s) e IBSS?**
Se puede crear en un solo equipo. En Ubuntu 24.04 / kernel 6.17, el AWUS036ACM puede crear interfaces mesh 802.11s e IBSS (Ad-hoc); pero esta vez no había un segundo nodo, así que la interconexión multinodo no se ha verificado y solo podemos afirmar que se crea en local.

**P: ¿El AWUS036ACM puede capturar el handshake WPA?**
Sí. Frente a nuestro propio AP y nuestro propio iPhone 7 Plus, la prueba de extremo a extremo tuvo éxito: deauth, captura del 4-way completo (M1–M4) y exportación de un .22000 para hashcat con hcxpcapngtool --all. Solo en redes propias o autorizadas.

---

## 6. Lecturas adicionales

- Comparación completa de capacidades y evaluación de selección de las nueve tarjetas ALFA → [Hub de evaluación de adaptadores inalámbricos ALFA (tabla general de nueve tarjetas)](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Sin instalar controladores: activar Monitor / AP en Ubuntu 24.04 + kernel 6.17 (pruebas de rtw88 / rtw89 / mt76) (placeholder, enlace en construcción)
- Tutorial paso a paso de WPA3-SAE y captura de handshake de extremo a extremo (placeholder, enlace en construcción)
- El modelo de una sola antena también basado en mt76 → prueba práctica del AWUS036ACHM (placeholder, enlace en construcción)

---

*Entidad de prueba: Yupitek (distribuidor de ALFA Network en Taiwán) — https://www.yupitek.com | Entorno de prueba: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Dispositivo de prueba: Apple iPhone 7 Plus (WPA3 también probado con iPhone 15 Pro)*
