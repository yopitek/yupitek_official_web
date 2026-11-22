---
title: "La prueba más completa de 2026: matriz total de Monitor, Injection y AP de 9 adaptadores WiFi ALFA en el ASUS GX10 (ARM64 / Ubuntu 24.04)"
slug: alfa-9-cards-arm64-gx10-ubuntu-matrix
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix.webp"
bannerimage: "/images/blog/banner/alfa-9-cards-arm64-gx10-ubuntu-matrix.webp"
author: "benny-lai"
tags:
  - alfa-network
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - wifi-6
  - kali-linux
description: "Pruebas de 9 adaptadores WiFi USB ALFA en Ubuntu 24.04 ARM64 (GX10): rendimiento en Monitor, Injection, AP y WPA3-SAE, con la compatibilidad de las herramientas habituales de Kali y recomendaciones de selección de modelo. AWUS036ACH / EACS alcanzan el 100% de inyección."
faq:
  - question: "¿El AWUS036AXM puede hacer inyección (injection) en Ubuntu?"
    answer: "En esta plataforma, no. En las pruebas, el AWUS036AXM y el AWUS036AXML (ambos con chip MT7921) fallaron la inyección tanto en 2.4GHz como en 5GHz, por la regresión de chanctx de mac80211 del kernel stock 6.16+ (no por limitación nativa del chip); por ello no se recomiendan en esta plataforma para usos que requieran inyección o captura de handshake."
  - question: "¿Qué adaptador ALFA tiene la mayor tasa de éxito de inyección en Ubuntu?"
    answer: "En las pruebas, el AWUS036ACH y el AWUS036EACS alcanzaron el 100% de éxito de inyección tanto en 2.4GHz como en 5GHz, siendo los dos de mejor rendimiento de los 9 de este lote."
  - question: "¿Los 9 adaptadores ALFA necesitan instalar controladores aparte en Ubuntu 24.04?"
    answer: "No. Los 9 usan sobre el kernel 6.17 el controlador integrado en el kernel (in-kernel) (familias rtw88 / rtw89 / mt76); se reconocen al conectarlos y no requieren compilar módulos DKMS."
  - question: "¿Se puede montar un punto de acceso WPA3-SAE con un adaptador ALFA en Ubuntu?"
    answer: "Sí; en las pruebas, los 9 modelos lograron montar un punto de acceso WPA3-SAE y dejar conectar a los dispositivos (probado en 2.4 GHz en todas las tarjetas salvo la ACS, probada en 5 GHz; la AXML se probó además en 6 GHz); solo el AWUS036ACHM requiere fijar el sae_pwe de hostapd a 0, pues de lo contrario el antiguo iPhone 7 Plus fallará al conectar."
  - question: "¿Los usuarios de Kali Linux pueden tomar como referencia estos resultados de Ubuntu?"
    answer: "Kali Linux se basa en el ecosistema Debian/Ubuntu y usa el mismo conjunto de controladores integrados rtw88 / rtw89 / mt76, por lo que la compatibilidad de controladores y la matriz de capacidades de este artículo pueden servir, en principio, de referencia para los usuarios de Kali; no obstante, la plataforma de prueba de este artículo es Ubuntu 24.04 y aún no se ha reverificado formalmente en Kali, así que considere definitivos los resultados de una futura reverificación."
draft: false
---

## Resumen (TL;DR)

Yopitek (distribuidor de ALFA Network en Taiwán) probó 9 adaptadores Wi-Fi USB ALFA en ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17): los 9 funcionan en modo monitor y como AP, los AWUS036ACH y AWUS036EACS alcanzan el 100% de inyección en ambas bandas, y los AWUS036AXM / AWUS036AXML con MT7921 fallan la inyección en esta plataforma.

- **Modo monitor disponible en todas**: los 9 adaptadores pueden entrar en modo monitor; la única diferencia está en la potencia de recepción.
- **La inyección es la línea divisoria**: con el controlador `rtw88` de Realtek, el ACH y el EACS alcanzan el 100% de inyección en ambas bandas, seguidos del ACS; el AXM / AXML de MT7921 falla la inyección en esta plataforma.
- **Handshake de extremo a extremo (captura → exportación a `.22000`) demostrado en 7 de 9 modelos**: ACM, ACHM, ACH, ACS, EACS, AX y AXER.
- **AP y WPA3-SAE superados casi por todos**: solo el AWUS036ACHM necesita `sae_pwe=0` para ser compatible con los iPhone antiguos.
- **Sin compilación en ARM64**: los 9 modelos usan el controlador integrado en el kernel 6.17; funcionan nada más conectarlos, sin DKMS.

Yopitek es el distribuidor de ALFA Network en Taiwán. Cuando los clientes eligen un adaptador WiFi USB, las tres preguntas que más repiten son casi siempre las mismas: «¿Esta tarjeta puede entrar en modo monitor en mi entorno Linux? ¿Puede hacer inyección? ¿Puede montar un AP?». En lugar de responder a partir de la hoja de especificaciones, llevamos directamente los 9 adaptadores ALFA en activo a nuestra propia mesa de laboratorio y los probamos uno a uno en un **ASUS GX10 (ARM64)** con **Ubuntu 24.04 LTS**, comparando de una sola vez las cuatro líneas de capacidad —Monitor, Injection, AP y WPA3-SAE— y señalando con honestidad cuáles «no pueden hacer ciertas cosas en esta plataforma».

Conviene aclarar primero el enfoque: todas las pruebas de este artículo se realizaron sobre equipos propios de Yopitek y sobre el WiFi de nuestra propia oficina, usando nuestros propios teléfonos de prueba. Es una validación de hardware por parte de un distribuidor sobre la compatibilidad y los límites de capacidad del producto, no un tutorial de ataque contra redes de terceros. El texto no ofrece ningún paso de operación contra redes externas; la inyección y el handshake se miden exclusivamente en un entorno cerrado propio, sobre dispositivos propios.

Este es un artículo tipo Hub, con la tabla maestra. La configuración paso a paso y la evidencia completa de cada tarjeta se desgranan en artículos individuales por modelo (véase Lecturas adicionales al final).

## Plataforma de pruebas y metodología

- **Plataforma de cómputo**: ASUS GX10 (ARM64 / aarch64)
- **Sistema operativo**: Ubuntu 24.04 LTS
- **Versión del kernel**: kernel 6.17.0-1014-nvidia
- **Estrategia de controladores**: los 9 modelos usan el controlador integrado en el kernel (in-kernel); se reconocen al conectarlos, sin instalar ningún módulo DKMS de terceros
- **Dispositivo de prueba**: Apple iPhone 7 Plus (la compatibilidad WPA3-SAE se verificó adicionalmente con un iPhone 15 Pro)
- **Entorno de prueba**: WiFi propio de la oficina, SSID `YUPITEK`, 2.4GHz ch5 / 5GHz ch36, ch157
- **Periodo de prueba**: mediciones reales del 2026-11-16 al 2026-11-18

En cuanto al método, ejecutamos el mismo conjunto de pasos con cada tarjeta: primero confirmamos la carga del controlador y la generación de la interfaz (`wlx*`), luego verificamos en orden el modo monitor, la inyección, el AP y la conexión WPA3-SAE en 2.4GHz / 5GHz, y por último realizamos la aceptación de la cadena de captura de handshake de extremo a extremo contra nuestro propio teléfono de prueba. Cada resultado se registra con la cifra o el estado realmente medido, no con una suposición basada en la hoja de especificaciones.

Las tablas de este artículo usan la siguiente leyenda:

> ✅ Superado | 🟡 Parcial o posible solo en un equipo | ⚠️ Con limitaciones | ❌ No compatible o prueba fallida | N/A El controlador no ofrece ese modo | ⬜ No probado (falta un segundo equipo)

## 1. Correspondencia entre hardware y controlador

Veamos primero los detalles de hardware de los 9 modelos y el controlador que realmente cargan sobre el kernel 6.17.

| # | Modelo | Chip | USB ID | Controlador (in-kernel) | Firmware | Generación / Flujos | Observaciones |
|---|---|---|---|---|---|---|---|
| 1 | **AWUS036ACM** | MediaTek MT7612U | — | `mt76x2u` | — | Wi-Fi 5 / 2T2R | Tarjeta Kali recomendada por morrownr |
| 2 | **AWUS036ACHM** | MediaTek MT7610U | — | `mt76x0u` | — | Wi-Fi 5 / 1T1R (AC600) | Antena única |
| 3 | **AWUS036ACH** | Realtek RTL8812AU | `0bda:8812` | `rtw88_8812au` | — | Wi-Fi 5 / 2T2R (AC1200) | Doble antena de alta ganancia |
| 4 | **AWUS036ACS** | Realtek RTL8811AU | `0bda:0811` | `rtw88_8821au` | 42.4.0 | Wi-Fi 5 / 1x1 | Ligera y portátil |
| 5 | **AWUS036EACS** | Realtek RTL8821CU | `0bda:c820` | `rtw88_8821cu` | 24.11.0 | Wi-Fi 5 / 1x1 | Combo BT + WiFi |
| 6 | **AWUS036AX** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | — |
| 7 | **AWUS036AXER** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | Mismo chip, antena integrada (Nano) |
| 8 | **AWUS036AXM** | MediaTek MT7921AUN | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | — |
| 9 | **AWUS036AXML** | MediaTek MT7921AUN | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | + BT |

Varios puntos clave:

**Dos grandes familias de controladores.** Los 9 modelos se reparten entre dos conjuntos de controladores integrados en el kernel: MediaTek (`mt76x2u` / `mt76x0u` / `mt7921u`) y Realtek (`rtw88_*` / `rtw89_8852bu`). Las generaciones de chip cubren Wi-Fi 5 (6 modelos) y Wi-Fi 6 (3 modelos: AX y AXER usan `rtw89_8852bu`; AXM y AXML usan `mt7921u`).

**La ventaja más práctica en ARM64 es «sin compilación».** Estos 9 modelos usan el controlador integrado en el kernel 6.17; se reconocen al conectarlos y no requieren tratar con módulos DKMS fuera del árbol (out-of-tree) en aarch64. Esto se nota especialmente en ARM64: muchos controladores Realtek de terceros carecen de binarios precompilados para aarch64 y a menudo hay que compilarlos desde el código fuente ajustándolos a la versión del kernel, con una alta probabilidad de tropiezos. Estas tarjetas eliminan directamente ese proceso.

**Mismo chip, distinto modelo.** El AWUS036AX y el AWUS036AXER comparten el mismo RTL8832BU y el mismo controlador `rtw89_8852bu`; la diferencia está en el diseño de antena (el AXER usa un diseño de antena integrada Nano, sin RP-SMA), lo que se reflejará en las cifras de recepción e inyección más adelante.

**Dos modelos son dispositivos combo BT + WiFi.** El AWUS036EACS (RTL8821CU) y el AWUS036AXML (MT7921AUN) llevan Bluetooth integrado; esta característica tiene un efecto secundario práctico al reconectar la tarjeta, que se explica más adelante en «Consideraciones de plataforma».

## 2. Matriz de capacidades clave: Monitor / Injection / AP / WPA3

Esta es la tabla principal del artículo y la primera que conviene mirar al elegir modelo.

| # | Modelo | Monitor 2.4G | Monitor 5G | **Injection 2.4G** | **Injection 5G** | AP 2.4G | AP 5G | WPA3-SAE |
|---|---|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ | ✅ | ✅ 63–83% | ✅ 76% | ✅ | ✅ 80MHz | ✅ 2.4G |
| 2 | AWUS036ACHM | ✅ | ✅ | ✅ 96–100% | ⚠️ solo broadcast | ✅ | ✅ | ✅* 2.4G |
| 3 | AWUS036ACH | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ | ✅ 2.4G |
| 4 | AWUS036ACS | ✅ | ✅ | ✅ **100%** | ✅ 96% | ✅ | ✅ (802.11a, 20 MHz; VHT80 no probado) | ✅ 5G |
| 5 | AWUS036EACS | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ (802.11a, 20 MHz; VHT80 no probado) | ✅ 2.4G |
| 6 | AWUS036AX | ✅ fuerte | ✅ fuerte | ✅ 96% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 7 | AWUS036AXER | ✅ fuerte | ✅ fuerte | ✅ 73% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 8 | AWUS036AXM | ✅ débil | ✅ débil | ❌ **falla** | ❌ **falla** | ✅ | ✅ 80MHz | ✅ 2.4G |
| 9 | AWUS036AXML | ✅ débil | ✅ débil | ❌ **falla** | ❌ **falla** | ✅ | ✅ 80MHz | ✅ 2.4G / 6G |

> \* El WPA3 del AWUS036ACHM requiere `sae_pwe=0`; con `sae_pwe=2` el iPhone 7 Plus no logra conectar.
>
> Columna WPA3-SAE: la banda indicada es la realmente probada (2.4G en todas las tarjetas salvo la ACS, probada en 5G; la AXML se probó además en 6G). Las demás bandas no se probaron.

Lectura punto por punto:

**Monitor: disponible en los 9 modelos, con diferencias de recepción.** Tanto en 2.4GHz como en 5GHz, los 9 pueden entrar en modo monitor sin excepción. La diferencia está en la agresividad del escaneo y la sensibilidad de recepción: el AX / AXER de Wi-Fi 6 tienen la mejor recepción y el escaneo más agresivo; el AXM / AXML de MT7921 entran en monitor, pero rinden relativamente peor. Si solo necesita captura pasiva o un inventario del espectro, los 9 sirven.

**Injection: la brecha empieza aquí.** La serie `rtw88` de Realtek es la que mejor rinde: ACH y EACS alcanzan el **100%** en 2.4GHz / 5GHz, y el ACS logra 2.4GHz 100% / 5GHz 96%. El ACM de MediaTek `mt76` es usable pero con cifras en la franja media (2.4GHz 63–83%, 5GHz 76%); el ACHM solo puede hacer broadcast en 5GHz y no puede inyectar contra un objetivo concreto. El AX / AXER de `rtw89` pueden inyectar, aunque la tasa de inyección en 2.4GHz del AXER (73%) queda bastante por debajo de la del AX (96%).

**La limitación honesta más importante: la inyección del MT7921 (AXM / AXML) falla en esta plataforma.** No es que los parámetros estén mal ajustados ni que el chip sea incapaz de inyectar por diseño; la causa principal es la regresión de chanctx de mac80211 en el kernel 6.16+. Aunque la comunidad logra que el mismo modelo funcione con controladores de git / parcheados, el firmware bloquea la tasa (ver morrownr/USB-WiFi #387, morrownr/mt76 #18). En esta plataforma, al fallar la inyección, estos dos modelos no pueden hacer deauth y, por tanto, no pueden completar la cadena de captura de handshake. Para usos que requieran inyección, descarte directamente estas dos tarjetas en esta plataforma.

**AP y WPA3: superados casi por todos.** Los 9 pueden actuar como AP y la mayoría admite VHT80 (80MHz) en 5GHz; la conexión WPA3-SAE también funciona en todos en la banda probada (véase la nota bajo la tabla). Lo único a tener en cuenta es el AWUS036ACHM: en WPA3 hay que fijar `sae_pwe` de hostapd a 0; de lo contrario, el antiguo iPhone 7 Plus no logrará conectar (con el iPhone 15 Pro sí conecta en la reverificación, lo que indica una diferencia de ajuste de compatibilidad).

## 3. Resumen de funciones avanzadas y capacidad de handshake

Profundicemos un nivel más y veamos el handshake de extremo a extremo, la interfaz virtual (VIF), el active monitor y mesh / IBSS.

| # | Modelo | Captura de handshake WPA | VIF | Active monitor | Ad-hoc (IBSS) | Mesh (802.11s) |
|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ **extremo a extremo** (.22000) | ✅ STA+AP / AP+mon | 🟡 configurable, ACK no verificado | 🟡 en local | 🟡 en local |
| 2 | AWUS036ACHM | ✅ **extremo a extremo** (.22000, en 5 GHz ch36) | ✅ | 🟡 | 🟡 en local | 🟡 en local |
| 3 | AWUS036ACH | ✅ **extremo a extremo** (.22000) | ✅ STA+mon | ❌ -95 | 🟡 en local | ❌ -95 |
| 4 | AWUS036ACS | ✅ **extremo a extremo** (.22000) | ✅ | ❌ -95 | ❌ | ❌ -95 |
| 5 | AWUS036EACS | ✅ **extremo a extremo** (.22000, 79 ACKs) | 🟡 monitor pasivo + managed en el mismo canal (monitor por software); sin VIF dual independiente | ❌ -95 | ❌ | ❌ -95 |
| 6 | AWUS036AX | ✅ **extremo a extremo** (.22000) | ✅ STA+AP | N/A | N/A | N/A |
| 7 | AWUS036AXER | ✅ **extremo a extremo** (.22000) | ✅ STA+AP | N/A | N/A | N/A |
| 8 | AWUS036AXM | ❌ la inyección falla | ✅ | 🟡 | N/A | N/A |
| 9 | AWUS036AXML | ❌ la inyección falla | ✅ | 🟡 | N/A | N/A |

Aquí «extremo a extremo» tiene una definición precisa: usar la tarjeta para ejecutar inyección contra el **iPhone 7 Plus propio de Yopitek** (conectado a nuestro SSID `YUPITEK`), capturar el 4-way handshake completo (M1–M4) y luego convertirlo al formato `.22000` de hashcat con `hcxpcapngtool --all`. El punto de aceptación de la «capacidad de pruebas de penetración» es que toda la cadena funcione de principio a fin, no que «pueda entrar en monitor».

- **Superan el extremo a extremo (7 de 9 modelos)**: ACM, ACHM, ACH, ACS, EACS, AX y AXER pueden generar el `.22000`; entre ellos, el EACS recibió 79 ACKs, con la realimentación de señal más sólida; el ACH alcanza el 100% de inyección en ambas bandas y, en la reverificación del 2026-11-19, exportó un `.22000` de 47 líneas de hashline. El ACHM lo completó en 5GHz (ch36); el ACM lo completó aunque su tasa de éxito de inyección es menor.
- **Cadena rota en el extremo a extremo**: AXM / AXML, al fallar la inyección, cortan toda la cadena del handshake. Esto confirma de nuevo que el MT7921 no es adecuado para pruebas de penetración en esta plataforma.
- **VIF (coexistencia de interfaces virtuales)**: los 9 admiten alguna forma de interfaces concurrentes; Realtek rtw89 puede correr STA + AP simultáneamente, mientras que el EACS solo admite un monitor pasivo junto a una interfaz managed en el mismo canal (monitor por software), no VIF duales independientes.
- **Active monitor (con informe de ACK)**: el ACH / ACS / EACS de `rtw88` devuelven -95 (no compatible); el AX / AXER de `rtw89` no ofrecen este modo en el controlador (N/A); `mt76` / `mt7921u` son parcialmente compatibles (🟡).
- **Mesh (802.11s)**: solo el ACM / ACHM de `mt76` pueden establecerlo en un solo equipo (🟡, se necesita una segunda tarjeta para verificar por completo la interconexión); el `rtw88` de Realtek devuelve -95 (no compatible) y los controladores de `rtw89` y `mt7921u` no ofrecen este modo. Para experimentos de mesh, MediaTek `mt76` es la única opción de este lote.
- **IBSS (Ad-hoc)**: el ACM / ACHM de `mt76` y el ACH de `rtw88` pueden hacer join en un solo equipo (🟡); el EACS lista el iftype pero en la práctica el join no funciona, y el AX / AXER de `rtw89` carecen del iftype IBSS (N/A).

### Compatibilidad a nivel de herramientas Kali / aircrack (común a la plataforma)

Las siguientes herramientas se comportan a nivel de plataforma en los 9 modelos, con independencia de cada tarjeta:

| Herramienta | Estado | Descripción |
|---|---|---|
| airmon-ng | ✅ | Detecta / gestiona todas las tarjetas; **prohibido `check kill`** (apaga NetworkManager y deja al GX10 sin red) |
| kismet | ✅ | Cada tarjeta puede arrancar como data source y generar un log `.kismet` |
| bettercap | ✅ | `wifi.recon` y el channel hopper funcionan con normalidad |
| wifite (git 3.0.0) | ✅ | Puede escanear y construir la lista de objetivos (hay que usar la versión de git; la de apt entra en conflicto con el aircrack-ng compilado a mano) |
| Wireshark / tshark | ✅ | Captura y análisis en monitor con normalidad |
| **hcxdumptool 8.x** | ⚠️ | **failed to arm en todas las tarjetas salvo el EACS en 2.4 GHz (en 5 GHz falla)**: requiere active-monitor, y `rtw88` / `rtw89` / `mt7921u` no lo admiten → usar `airodump-ng` + `aireplay-ng` |

Nota ARM64: `aircrack-ng` debe compilarse desde el código fuente y para `wifite` se recomienda la versión git 3.0.0, para esquivar el conflicto de dependencias entre el paquete de apt y la versión compilada a mano.

## 4. Recomendaciones de selección según el uso

Condensemos las tres tablas anteriores en «elija directamente según el uso».

| Uso | Primera opción | Descripción |
|---|---|---|
| **Pruebas de penetración (inyección + handshake)** | **AWUS036EACS** / AWUS036ACS / AWUS036ACH | Mejor inyección en ambas bandas (EACS y ACH al 100%); el `.22000` de extremo a extremo lo respaldan EACS, ACS y ACH (ACH reverificado el 2026-11-19) |
| **Máxima recepción / monitor de larga distancia** | **AWUS036AXER** / AWUS036ACH | El AXER captó 63 AP + 12 clientes en un solo escaneo por salto de canal; el ACH es de doble antena y alta ganancia |
| **Wi-Fi 6 + punto de acceso (AP)** | AWUS036AX / AWUS036AXER | 2x2 VHT80, AP estable e inyección usable |
| **AP puro / conexión general (sin inyección)** | AWUS036AXM / AWUS036AXML | MediaTek ofrece una conexión estable, pero **la inyección falla**; no apto para uso de penetración |
| **Experimentos mesh / IBSS** | AWUS036ACM / AWUS036ACHM | El controlador `mt76` puede establecer mesh e IBSS en un solo equipo (el ACH de `rtw88` solo puede hacer join de IBSS en local, sin mesh; el `rtw89` no declara ninguno de los dos) |

Unas frases en lenguaje llano a modo de resumen:

- **Para pruebas de penetración y captura de handshake**: hay 7 de 9 modelos con el `.22000` de extremo a extremo ya registrado en disco como evidencia —**AWUS036EACS** (el más sólido, 79 ACKs), **AWUS036ACS**, los de Wi-Fi 6 AWUS036AX / AWUS036AXER, **AWUS036ACM** y **AWUS036ACHM** (5 GHz), y **AWUS036ACH** (100% de inyección en ambas bandas; en la reverificación del 2026-11-19 exportó un `.22000` de 47 líneas de hashline).
- **Para la mayor distancia de recepción y la captura más amplia**: el AWUS036AXER (Wi-Fi 6, diseño de antena integrada Nano + afinado del chip, con el escaneo por salto de canal más agresivo) o el AWUS036ACH de doble antena y alta ganancia.
- **Para montar un punto de acceso Wi-Fi 6**: AWUS036AX / AWUS036AXER, 2x2 VHT80 y con soporte simultáneo de inyección.
- **Si solo quiere una conexión estable / usarlo como simple AP**: la solución MediaTek del AWUS036AXM / AWUS036AXML ofrece una conexión estable, sin problemas para el uso diario.
- **Para experimentar con mesh**: en este lote solo lo logran el AWUS036ACM / AWUS036ACHM de `mt76` (para IBSS en un solo equipo, además, el AWUS036ACH de `rtw88` puede hacer join).

**Aviso clave (la regla más importante)**: si su uso es **inyección o handshake**, **no elija el AWUS036AXM / AWUS036AXML**. El MT7921 falla la inyección en esta plataforma —ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel stock 6.17)— por la regresión de chanctx de mac80211 en el kernel 6.16+ (no por limitación nativa del chip), no por un problema de configuración; aunque la comunidad logra que el mismo modelo funcione con controladores de git / parcheados, el firmware bloquea la tasa, y bajo el kernel stock de esta plataforma sigue sin poder inyectar. Déjelos para escenarios de «solo conexión / solo AP».

## 5. Consideraciones de plataforma (práctica en GX10 ARM64)

Estos son los puntos prácticos comunes a los 9 modelos al operar este lote de tarjetas en un ASUS GX10 + Ubuntu 24.04 (ARM64):

1. **No corte su propia red**: nunca ejecute `airmon-ng check kill`; apaga NetworkManager y deja a todo el GX10 sin red. Al operar, toque solo las interfaces `wlx*` externas y no toque la línea principal integrada de salida a internet.
2. **Resolución de RX stall**: tras alternar repetidamente entre monitor / AP, si de repente no detecta nada, suele tratarse de un RX stall; basta con desconectar y volver a conectar la tarjeta una vez para recuperarla (el USB se reenumera y el nombre de interfaz, basado en la MAC, no cambia).
3. **Dispositivos combo BT + WiFi**: el EACS y el AXML llevan Bluetooth integrado; al reconectarlos, a veces se quedan atascados en el probe de WiFi y no generan la interfaz `wlx`; cambiar de puerto USB suele resolverlo.
4. **Desbloqueo de TX en 5GHz**: antes de hacer inyección en 5GHz en un entorno propio, hay que configurar el dominio regulatorio correcto para desbloquear la potencia de TX, y restaurar el dominio local al terminar la prueba. Es el prerrequisito para que el 5GHz pueda transmitir correctamente.
5. **Truco para la captura de handshake**: en la oficina suele haber varios AP con el mismo nombre; en la práctica es más estable no fijar un único BSSID y capturar todo el canal, usando `hcxpcapngtool --all` al convertir.
6. **hcxdumptool con failed to arm en toda la plataforma (la excepción es el EACS en 2.4 GHz)**: las tarjetas integradas de triple banda y los controladores citados no admiten active-monitor; cambie directamente al paquete aircrack-ng (`airodump-ng` + `aireplay-ng`).
7. **Detalles de compilación en ARM64**: `aircrack-ng` debe compilarse desde el código fuente, y `wifite` se usa en su versión de git para esquivar el conflicto de dependencias de apt.

Insistimos de nuevo en el enfoque: las capacidades de inyección / deauth / handshake descritas se miden íntegramente en un entorno cerrado propio de Yopitek, sobre dispositivos de prueba propios, con el fin de validar las capacidades del producto y los límites de compatibilidad. Este artículo no ofrece ni recomienda realizar dichas operaciones contra ninguna red de terceros.

## Conclusión

En esta plataforma —ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17)—, la valoración global de las 9 tarjetas ALFA se puede condensar en tres frases: **el Monitor está disponible en todas, el AP y el WPA3 los superan casi todas, y la línea divisoria está en la Injection.** Para usos profesionales que requieren inyección y handshake, el EACS / ACH / ACS de Realtek `rtw88` son la opción más fiable; para recepción y Wi-Fi 6, mire al AXER / AX; el AXM / AXML de MT7921 quedan para escenarios de simple conexión. Sin compilación en todos y funcionando nada más conectarlos: esa es la mayor virtud común de este lote de tarjetas en ARM64.

## Preguntas frecuentes (FAQ)

**P: ¿El AWUS036AXM puede hacer inyección (injection) en Ubuntu?**
R: En esta plataforma, no. En las pruebas, el AWUS036AXM y el AWUS036AXML (ambos con chip MT7921) fallaron la inyección tanto en 2.4GHz como en 5GHz, por la regresión de chanctx de mac80211 del kernel stock 6.16+ (no por limitación nativa del chip); por ello no se recomiendan en esta plataforma para usos que requieran inyección o captura de handshake.

**P: ¿Qué adaptador ALFA tiene la mayor tasa de éxito de inyección en Ubuntu?**
R: En las pruebas, el AWUS036ACH y el AWUS036EACS alcanzaron el 100% de éxito de inyección tanto en 2.4GHz como en 5GHz, siendo los dos de mejor rendimiento de los 9 de este lote.

**P: ¿Los 9 adaptadores ALFA necesitan instalar controladores aparte en Ubuntu 24.04?**
R: No. Los 9 usan sobre el kernel 6.17 el controlador integrado en el kernel (in-kernel) (familias rtw88 / rtw89 / mt76); se reconocen al conectarlos y no requieren compilar módulos DKMS.

**P: ¿Se puede montar un punto de acceso WPA3-SAE con un adaptador ALFA en Ubuntu?**
R: Sí; en las pruebas, los 9 modelos lograron montar un punto de acceso WPA3-SAE y dejar conectar a los dispositivos (probado en 2.4 GHz en todas las tarjetas salvo la ACS, probada en 5 GHz; la AXML se probó además en 6 GHz); solo el AWUS036ACHM requiere fijar el `sae_pwe` de hostapd a 0, pues de lo contrario el antiguo iPhone 7 Plus fallará al conectar.

**P: ¿Los usuarios de Kali Linux pueden tomar como referencia estos resultados de Ubuntu?**
R: Kali Linux se basa en el ecosistema Debian/Ubuntu y usa el mismo conjunto de controladores integrados rtw88 / rtw89 / mt76, por lo que la compatibilidad de controladores y la matriz de capacidades de este artículo pueden servir, en principio, de referencia para los usuarios de Kali; no obstante, la plataforma de prueba de este artículo es Ubuntu 24.04 y aún no se ha reverificado formalmente en Kali, así que considere definitivos los resultados de una futura reverificación.

## Lecturas adicionales

Este artículo es la tabla maestra (Hub). Los siguientes artículos en profundidad e informes de pruebas por tarjeta se irán publicando (enlaces en construcción):

- «Sin instalar controladores: activar los modos Monitor y AP en Ubuntu (ARM64)» → [`/es/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/es/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- «Práctica de captura de handshake WPA3-SAE (verificado en entorno propio)» → [`/es/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/es/blog/alfa-wpa3-sae-handshake-capability-arm64/)

9 informes de pruebas en profundidad por tarjeta:

- [Informe de pruebas del AWUS036ACM](/es/blog/awus036acm-asus-gx10-ubuntu-test-report/)
- [Informe de pruebas del AWUS036ACHM](/es/blog/awus036achm-asus-gx10-ubuntu-test-report/)
- [Informe de pruebas del AWUS036ACH](/es/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- [Informe de pruebas del AWUS036ACS](/es/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- [Informe de pruebas del AWUS036EACS](/es/blog/awus036eacs-asus-gx10-ubuntu-test-report/)
- [Informe de pruebas del AWUS036AX](/es/blog/awus036ax-asus-gx10-ubuntu-test-report/)
- [Informe de pruebas del AWUS036AXER](/es/blog/awus036axer-asus-gx10-ubuntu-test-report/)
- [Informe de pruebas del AWUS036AXM](/es/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- [Informe de pruebas del AWUS036AXML](/es/blog/awus036axml-asus-gx10-ubuntu-test-report/)

---

*Unidad de pruebas: Yopitek (distribuidor de ALFA Network en Taiwán) | Plataforma de pruebas: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Dispositivo de prueba: Apple iPhone 7 Plus (WPA3 verificado adicionalmente con iPhone 15 Pro) | Entorno de prueba: WiFi propio de la oficina. Este artículo es una validación de compatibilidad y capacidades del producto, no un tutorial de operación contra redes de terceros.*
