---
title: "Prueba práctica de la AWUS036AXM: capacidades de Monitor / AP / WPA3 y la limitación de inyección del MediaTek MT7921AU (Wi-Fi 6 2x2) en ASUS GX10 + Ubuntu 24.04 (ARM64)"
slug: awus036axm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axm
  - mt7921
  - mt7921u
  - wifi-6
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - ap-mode
  - wpa3-sae
  - monitor-mode
description: "AWUS036AXM (mt7921u) en ASUS GX10/Ubuntu 24.04 ARM64: monitor, AP y WPA3 funcionan, pero la inyección de paquetes falla; no es apta para pruebas de penetración, su sitio es el AP puro y la conexión."
faq:
  - question: "¿La AWUS036AXM puede hacer inyección de paquetes (packet injection)?"
    answer: "En nuestra plataforma de prueba (ASUS GX10/Ubuntu 24.04 ARM64/stock kernel 6.17.0-1014-nvidia) no. aireplay-ng --test devuelve No Answer y Found 0 APs tanto en 2,4 GHz como en 5 GHz, por lo que tampoco es posible hacer deauth ni capturar el handshake WPA. La causa de fondo es una regresión de chanctx en mac80211 del kernel 6.16+, no una incapacidad nativa del chip para inyectar; la AWUS036AXML de la misma serie da el mismo resultado. Si necesita inyección, elija las AWUS036EACS, ACH o ACS, cuya inyección sí funciona en nuestras pruebas."
  - question: "¿La AWUS036AXM sirve para pruebas de penetración o para Kali?"
    answer: "No es recomendable. El modo monitor funciona, pero la recepción es floja y a menudo se pierden paquetes de clientes y de datos; además, en esta plataforma la inyección falla, así que no puede hacer deauth ni capturar handshakes. La plataforma de este artículo es Ubuntu 24.04; no probamos sobre la distribución Kali en sí. Es adecuada para AP puro, conexión general y puntos de acceso WPA3; para pruebas de penetración, elija las AWUS036EACS, ACH o ACS."
  - question: "¿La AWUS036AXM necesita instalar controladores aparte en Ubuntu 24.04?"
    answer: "No. El controlador mt7921u está integrado en el kernel 6.17 y la reconoce nada más conectarla (USB ID 0e8d:7961), sin DKMS y sin compilar. El controlador no ofrece los modos IBSS (Ad-hoc) ni mesh; es una limitación, no un problema de configuración."
  - question: "¿La AWUS036AXM puede abrir un AP? ¿Admite WPA3?"
    answer: "Sí, y es su mejor uso. Tanto en 2,4 GHz (802.11n) como en 5 GHz VHT80 el iPhone se conectó y quedó authorized; WPA3-SAE funciona en 2,4 GHz (MFP: yes; WPA3 en 5 GHz no se probó) y los iPhone antiguos requieren sae_pwe=0; la concurrencia STA+AP (VIF) también funciona. En esta ronda solo probamos 2,4 y 5 GHz; 6 GHz y Bluetooth no se probaron por separado."
  - question: "¿Qué tal es el modo monitor de la AWUS036AXM?"
    answer: "Entra en modo monitor y capta beacons tanto en 2,4 GHz como en 5 GHz, pero la recepción es floja y la cantidad de paquetes de clientes y de datos es escasa, así que conviene fijar un único canal en vez de saltar entre canales. Para monitorización de amplio alcance o larga distancia, en nuestras pruebas la AWUS036AXER y la ACH son claramente mejores."
draft: false
---

{{< tldr >}}En ASUS GX10/Ubuntu 24.04 ARM64, la AWUS036AXM tiene monitor, AP, WPA3 y VIF funcionales, pero la inyección de paquetes falló en la prueba (No Answer/Found 0 APs): no puede hacer deauth ni capturar handshakes, no se recomienda para pruebas de penetración; su sitio es el AP puro y la conexión.{{< /tldr >}}

Yopitek es el distribuidor de ALFA Network en Taiwán. Este es el informe de pruebas tarjeta por tarjeta de la AWUS036AXM, con un objetivo muy sencillo: medir con claridad qué «puede y qué no puede hacer» esta tarjeta Wi-Fi 6 en **ASUS GX10 (ARM64) + Ubuntu 24.04**, para que el cliente que la compre no tenga que adivinarlo a partir de una hoja de especificaciones.

Dejemos clara la premisa: todas las pruebas se realizaron sobre equipo propio de Yopitek y la Wi-Fi propia de la oficina, frente a nuestros propios teléfonos de prueba. Es una validación de hardware que un distribuidor hace sobre la compatibilidad y los límites de capacidad del producto, no un tutorial de ataque contra redes de terceros. El texto no ofrece ningún procedimiento de operación contra redes externas; las mediciones relacionadas con monitor e inyección se hicieron siempre en un entorno cerrado propio y sobre dispositivos propios.

Lo primero que hay que saber de esta tarjeta: **en esta plataforma, su inyección falla**. Si su uso requiere inyección o captura de handshake, puede saltar directamente a los apartados cuatro y cinco para ver la conclusión de selección; si lo que busca es una conexión estable y montar un AP, la AWUS036AXM cumplirá a la perfección.

## 1. La tarjeta y la plataforma de prueba

La AWUS036AXM usa el chip MediaTek **MT7921AU** con el controlador integrado en el kernel **mt7921u**, y sus especificaciones son **Wi-Fi 6 (802.11ax), 2x2** de doble flujo espacial. La **AWUS036AXML** del mismo chip (MT7921AUN, que además lleva Bluetooth) se comporta exactamente igual en esta plataforma en cuanto a monitor Wi-Fi/AP/inyección, y ambas pueden tomarse como referencia mutua; la diferencia es que la AXML lleva además Bluetooth y, en nuestra máquina, la banda de 6 GHz resultó usable, mientras que en la AXM no probamos por separado ni 6 GHz ni Bluetooth en esta ronda.

- **Plataforma de cómputo**: ASUS GX10 (ARM64 / aarch64)
- **Sistema operativo**: Ubuntu 24.04 LTS
- **Versión del kernel**: kernel 6.17.0-1014-nvidia
- **Dispositivo de prueba**: Apple iPhone 7 Plus (WPA3-SAE y VIF revalidados además con un iPhone 15 Pro)
- **Entorno de prueba**: Wi-Fi propia de la oficina, SSID `YUPITEK`, 2.4GHz ch5 / 5GHz ch36
- **Periodo de prueba**: mediciones sobre hardware real del 2026-11-16 al 2026-11-18

## 2. Hardware y controlador (listo para usar, sin instalar)

El controlador mt7921u ya viene integrado en el kernel 6.17, y la AWUS036AXM queda reconocida nada más conectarla al GX10, sin necesidad de DKMS ni de compilar ningún controlador de terceros. Esto es lo más cómodo de esta generación de tarjetas MediaTek en ARM64.

| Elemento | Contenido |
|---|---|
| Modelo | AWUS036AXM |
| Chip | MediaTek MT7921AU |
| USB ID | `0e8d:7961` |
| Controlador (integrado en el kernel) | `mt7921u` |
| Generación / flujos | Wi-Fi 6 (802.11ax) / 2x2 |
| Modos de interfaz | managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO / P2P-device |
| Modos no admitidos | IBSS (Ad-hoc), Mesh (802.11s) |

Confirme que la tarjeta se reconoce:

```bash
lsusb | grep 0e8d:7961
```

La salida esperada es `ID 0e8d:7961 MediaTek Inc. Wireless_Device`. Observe también que, entre los modos de interfaz que lista `iw phy info`, no aparecen IBSS ni mesh point: es una limitación nativa del mt7921u, no un problema de configuración; para escenarios de mesh / IBSS, use la AWUS036ACM / ACHM del controlador `mt76`.

## 3. Capacidades probadas: Monitor / AP / WPA3, y la explicación honesta del fallo de inyección

Primero, una matriz de las capacidades centrales; luego lo desarrollamos punto por punto.

| Capacidad | 2,4 GHz | 5 GHz | Nota de la prueba |
|---|---|---|---|
| Monitor (escucha) | ✅ funciona (recepción floja) | ✅ funciona (recepción floja) | Capta beacons, pero el volumen de client / data frame es escaso |
| **Inyección** | ❌ **falla en esta plataforma** | ❌ **falla en esta plataforma** | Causa de fondo: regresión de chanctx en mac80211 del kernel 6.16+ (no nativa del chip) |
| AP (punto de acceso) | ✅ incl. 802.11n (HT20) | ✅ VHT 80 MHz | iPhone 7 Plus conectado sobre hardware real, authorized |
| WPA3-SAE | ✅ | No probado | MFP: yes, `sae_pwe=0` compatible con iPhone antiguos; probado solo en 2.4 GHz |
| VIF (STA + AP) | ✅ | ✅ | Una tarjeta, doble función; ping de 17 ms del lado STA |

### Monitor (escucha) ✅ funciona, pero con recepción floja

Tanto en 2,4GHz como en 5GHz puede pasar a modo monitor, y en ambas capta beacons. Pero hay que decirlo con honestidad: la recepción de la AWUS036AXM es claramente más débil que la de la AWUS036ACM / ACHM en la misma plataforma; en la prueba el número de frames fue escaso y capturó pocos paquetes de clientes y de datos. En la práctica recomendamos **fijar un único canal** para la captura, sin saltar entre canales: los resultados serán algo más estables.

Hay además un punto fácil de malinterpretar: en modo monitor, `txpower` reporta 3 dBm, lo cual es un artefacto de lectura (el TX real del hardware ronda los 20 dBm, verificado con `txpower_sku`) y no significa que la transmisión esté realmente limitada a tan poco. La AWUS036AXM no está pensada para captura de amplio alcance; para barrer ancho y recibir lejos, mire la AWUS036AXER, con mejor ajuste de antena y salto de canal más agresivo, o la AWUS036ACH de doble antena y alta ganancia: ambas tienen una recepción en modo monitor claramente superior en la misma plataforma.

### AP (punto de acceso) ✅ este es el punto fuerte de la AXM

En 2,4GHz, el AP puede abrir a la vez 802.11n (HT20); el iPhone 7 Plus se conectó negociando MCS 7 y quedó authorized. En 5GHz puede subir hasta **VHT 80 MHz**, con el iPhone conectado como VHT-NSS2 y authorized. Tanto en 2,4G como en 5G, la AWUS036AXM es estable como punto de acceso: es la capacidad que más justifica su compra en esta plataforma.

### WPA3-SAE ✅

Del lado del AP abrimos WPA3-SAE y el iPhone 7 Plus se conectó con éxito, con el MFP (Management Frame Protection) mostrando `yes`. Recordatorio práctico: poner `sae_pwe=0` lo hace compatible con dispositivos más antiguos como el iPhone 7 Plus; con `sae_pwe=2`, los iPhone antiguos pueden no conectar.

### VIF (STA + AP, una tarjeta con doble función) ✅

La AWUS036AXM puede, a la vez, actuar como STA conectada a una Wi-Fi existente y abrir una interfaz virtual (VIF) de AP. En la prueba, con el iPhone 15 Pro conectado a la VIF de AP, el ping del lado STA hacia `YUPITEK` fue de unos 17 ms, con conexión normal. Para la necesidad de «una tarjeta que a la vez da Internet y comparte punto de acceso», funciona.

### Inyección ❌ falla en esta plataforma —— esta es la línea divisoria para la selección

Esta es la cuestión más importante de la AWUS036AXM, y la que más honestidad exige. La salida de `aireplay-ng --test` en la prueba fue:

```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

Falla igual en 2,4GHz y en 5GHz. Aclaremos primero un malentendido común: que en modo monitor `iw` reporte solo 3 dBm de txpower es un **artefacto de lectura**; el TX real del hardware ronda los 20–23 dBm (verificado con `txpower_sku`), la potencia de transmisión no está rebajada y no es la causa del fallo. La causa de fondo está en la **capa de software**: a partir del kernel 6.16, el channel context (chanctx) de mac80211 sufrió una regresión que impide al controlador stock recibir los beacons del objetivo en escenarios de active monitor/inyección, por lo que `aireplay-ng` concluye `No Answer`. Se trata de **una regresión del lado del kernel, no de una incapacidad nativa del chip MT7921 para inyectar**. El fenómeno está documentado en morrownr/USB-WiFi issue #387, y el análisis de la causa de fondo en morrownr/mt76 issue #18.

Hay que añadir que las pruebas de la comunidad indican que, usando un controlador git/parcheado en el mismo modelo, sí es posible hacer funcionar el active monitor junto con la inyección; pero aun así, el firmware del MT7921 **mantiene la inyección bloqueada a las tasas base de 1 Mbps/6 Mbps**, sin poder inyectar a tasas HT/VHT. Dicho de otro modo, incluso sorteando la regresión del kernel, la capacidad de inyección de esta tarjeta queda limitada. Frente a las tarjetas rtw89 de Realtek (como la AWUS036AX/AXER), cuya inyección sí funciona con la misma suite aircrack-ng en la misma plataforma GX10, esta vía del MT7921 no funciona sobre **stock kernel 6.17**.

Lo subrayamos una vez más: no se trata del fallo de una tarjeta concreta ni de una configuración mal ajustada. La AWUS036AXML del mismo chip se comporta exactamente igual, y en stock kernel 6.17 ni cambiar parámetros, ni cambiar de canal, ni cambiar el dominio regulatorio la recuperan: la causa de fondo es la regresión de chanctx en mac80211 del kernel 6.16+, sumada al bloqueo de tasa de inyección del firmware, y no un defecto de hardware del chip. Consecuencia directa: en esta plataforma, la AWUS036AXM **no puede hacer deauth ni capturar handshakes WPA de forma activa**. Si necesita esas capacidades, use la solución Realtek / mt76x del siguiente apartado.

En cuanto a las funciones avanzadas, el resumen es el siguiente:

| Función avanzada | Estado | Explicación |
|---|---|---|
| Captura de handshake WPA | ❌ | No disponible por el fallo de inyección; use la ACM / ACHM / ACH / ACS / EACS |
| VIF (STA + AP) | ✅ | Doble función en una tarjeta, funciona |
| Active monitor | 🟡 | `set monitor active` se acepta, pero no se verificó el ACK |
| Ad-hoc (IBSS) | N/A | mt7921u no lo admite |
| Mesh (802.11s) | N/A | mt7921u no lo admite |
| Wi-Fi Direct (P2P) | ⬜ | El controlador declara soporte, no probado por falta de un segundo equipo |

### Seguridad de operación y consejos prácticos

Unos cuantos puntos prácticos para operar esta tarjeta en el GX10; tenerlos presentes evita muchos tropiezos:

- **No deje sin red su propia máquina**: nunca ejecute `airmon-ng check kill`, porque apaga NetworkManager y deja sin conexión a todo el GX10. Al operar, toque solo la interfaz externa `wlx*` y no toque la línea principal de conexión a Internet integrada del GX10.
- **La contraseña del AP debe tener 8 o más caracteres**: de lo contrario, hostapd devuelve `invalid WPA passphrase length` y no arranca.
- **Cuando el teléfono no capte el SSID**: basta con desconectar y volver a conectar la tarjeta para reiniciarla, o acercar el teléfono (los 3 dBm que reporta el modo monitor son un artefacto, no la potencia real, y no son la causa).
- **Resolver un RX stall**: si tras alternar varias veces entre monitor / AP deja de captar nada de repente, suele ser un RX stall; basta con desconectar y volver a conectar la tarjeta una vez para recuperarla (el nombre de la interfaz se basa en la MAC y no cambia).

## 4. Usos adecuados e inadecuados

Condensando todas las mediciones anteriores en una frase: la AWUS036AXM es una excelente tarjeta de «conexión / AP», pero no es una tarjeta de «inyección / ataque-defensa».

**Usos adecuados**

- Conexión diaria estable (Wi-Fi 6, 2x2)
- Montar puntos de acceso 2.4GHz / 5GHz (incl. 802.11n y VHT80)
- Validación de compatibilidad WPA3-SAE y pruebas de despliegue
- STA + AP, doble función en una tarjeta (VIF)
- Necesidades ligeras de monitor con captura pasiva de beacons

**Usos inadecuados (a evitar)**

- inyección / deauth
- Captura de handshake WPA, ejercicios activos de ataque-defensa
- Experimentos que requieran IBSS (Ad-hoc) o Mesh
- Captura de monitor de amplio alcance, larga distancia y alta sensibilidad

**El aviso más importante**: si su uso es **inyección o handshake**, **no elija la AWUS036AXM (ni la AWUS036AXML del mismo chip)**. En la plataforma ASUS GX10 (ARM64 / Ubuntu 24.04 / stock kernel 6.17), el MT7921 falla en la inyección; la causa de fondo es la regresión de chanctx en mac80211 del kernel 6.16+, no una incapacidad nativa del chip para inyectar; a fecha de 2026-11-18, en el entorno stock no se resuelve ajustando parámetros, así que resérvela para escenarios de «conexión pura / AP puro».

## 5. Recomendaciones de selección (AP puro/conexión)

| Su necesidad | Opción recomendada | Motivo |
|---|---|---|
| AP puro / conexión estable (sin inyección) | **AWUS036AXM** / AWUS036AXML | MediaTek, conexión estable, buen desempeño en AP y WPA3 |
| Pruebas de penetración (inyección + handshake) | AWUS036EACS / AWUS036ACH / AWUS036ACS | Inyección funcional en ambas bandas, handshake de extremo a extremo que sí funciona |
| Máxima recepción / monitor a larga distancia | AWUS036AXER / AWUS036ACH | La AXER hace un escaneo por salto de canal agresivo; la ACH, doble antena de alta ganancia |
| Wi-Fi 6 + AP y además inyección | AWUS036AX / AWUS036AXER | 2x2 VHT80, AP estable e inyección funcional |
| Experimentos de mesh / IBSS | AWUS036ACM / AWUS036ACHM | El controlador `mt76` permite crearlos en local |

En román paladino: para conexión estable y para hacer de AP, la AWUS036AXM cumple de sobra; en cuanto haya inyección o handshake de por medio, cambie a las Realtek EACS / ACH / ACS. Para la comparativa completa de este mismo lote de tarjetas en ARM64 y la matriz global de Monitor / Inyección / AP / WPA3 de las 9 tarjetas, vea el Hub de la tabla global:

- [La prueba práctica más completa de 2026: matriz global de 9 tarjetas Wi-Fi ALFA en ASUS GX10 (ARM64 / Ubuntu 24.04)](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

Insistimos en la premisa: todas las mediciones de monitor / inyección de este artículo se realizaron en el entorno cerrado propio de Yopitek, sobre nuestros propios dispositivos de prueba, con el fin de validar las capacidades del producto y sus límites de compatibilidad; no ofrecemos ni recomendamos realizar esas operaciones contra ninguna red de terceros.

## Preguntas frecuentes (FAQ)

**Q1. ¿La AWUS036AXM puede hacer inyección de paquetes (packet injection)?**
En nuestra plataforma de prueba (ASUS GX10/Ubuntu 24.04 ARM64/stock kernel 6.17.0-1014-nvidia) no. `aireplay-ng --test` devuelve `No Answer` y `Found 0 APs` tanto en 2,4 GHz como en 5 GHz, por lo que tampoco es posible hacer deauth ni capturar el handshake WPA. La causa de fondo es una regresión de chanctx en mac80211 del kernel 6.16+, no una incapacidad nativa del chip para inyectar; la AWUS036AXML de la misma serie da el mismo resultado. Si necesita inyección, elija las AWUS036EACS, ACH o ACS, cuya inyección sí funciona en nuestras pruebas.

**Q2. ¿La AWUS036AXM sirve para pruebas de penetración o para Kali?**
No es recomendable. El modo monitor funciona, pero la recepción es floja y a menudo se pierden paquetes de clientes y de datos; además, en esta plataforma la inyección falla, así que no puede hacer deauth ni capturar handshakes. La plataforma de este artículo es Ubuntu 24.04; no probamos sobre la distribución Kali en sí. Es adecuada para AP puro, conexión general y puntos de acceso WPA3; para pruebas de penetración, elija las AWUS036EACS, ACH o ACS.

**Q3. ¿La AWUS036AXM necesita instalar controladores aparte en Ubuntu 24.04?**
No. El controlador mt7921u está integrado en el kernel 6.17 y la reconoce nada más conectarla (USB ID `0e8d:7961`), sin DKMS y sin compilar. El controlador no ofrece los modos IBSS (Ad-hoc) ni mesh; es una limitación, no un problema de configuración.

**Q4. ¿La AWUS036AXM puede abrir un AP? ¿Admite WPA3?**
Sí, y es su mejor uso. Tanto en 2,4 GHz (802.11n) como en 5 GHz VHT80 el iPhone se conectó y quedó authorized; WPA3-SAE funciona en 2,4 GHz (`MFP: yes`; WPA3 en 5 GHz no se probó) y los iPhone antiguos requieren `sae_pwe=0`; la concurrencia STA+AP (VIF) también funciona. En esta ronda solo probamos 2,4 y 5 GHz; 6 GHz y Bluetooth no se probaron por separado.

**Q5. ¿Qué tal es el modo monitor de la AWUS036AXM?**
Entra en modo monitor y capta beacons tanto en 2,4 GHz como en 5 GHz, pero la recepción es floja y la cantidad de paquetes de clientes y de datos es escasa, así que conviene fijar un único canal en vez de saltar entre canales. Para monitorización de amplio alcance o larga distancia, en nuestras pruebas la AWUS036AXER y la ACH son claramente mejores.

## 6. Lecturas adicionales

Los siguientes artículos relacionados irán publicándose (enlaces en construcción):

- «Sin instalar controladores: activar los modos Monitor y AP en Ubuntu (ARM64)» → [`/es/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/es/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- «Capacidad WPA3-SAE y práctica de handshake (validado en entorno propio)» → [`/es/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/es/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- «Prueba práctica de la AWUS036AXML (mismo chip MT7921 + BT)» → (en construcción)
- «Por qué el mt7921u no puede inyectar en el kernel 6.16+: la regresión de chanctx y el bloqueo de velocidad del firmware» → (en construcción)

---

*Unidad de prueba: Yopitek (distribuidor de ALFA) | Plataforma: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Dispositivo de prueba: Apple iPhone 7 Plus (WPA3 / VIF revalidados además con un iPhone 15 Pro)*
