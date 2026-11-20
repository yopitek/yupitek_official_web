---
title: "Auditoría inalámbrica en la era WPA3-SAE: pruebas de la capacidad de captura de handshake de 9 tarjetas ALFA y el campo de minas de compatibilidad sae_pwe con la conexión del iPhone"
slug: alfa-wpa3-sae-handshake-capability-arm64
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-wpa3-sae-handshake-capability-arm64.webp"
author: "benny-lai"
tags:
  - wpa3-sae
  - wpa-handshake
  - sae-pwe
  - wireless-security
  - alfa-network
  - rtl8821cu
  - hcxpcapngtool
  - wifi-6
description: "Pruebas de la capacidad de captura de handshake WPA3-SAE de los adaptadores ALFA en Ubuntu (extensible a Kali): tasa de inyección de los 9 modelos y resultados de captura .22000 de extremo a extremo, el campo de minas de compatibilidad sae_pwe y recomendaciones de selección."
faq:
  - question: "¿El AWUS036AXM puede capturar el handshake WPA en Ubuntu?"
    answer: "En esta plataforma, no. En las pruebas, el AWUS036AXM y el AWUS036AXML (chip MT7921), al fallar la inyección y no poder enviar el deauth, cortan toda la cadena de captura del 4-way handshake, por lo que no son aptos para usos que requieran captura de handshake."
  - question: "¿Qué adaptador ALFA captura el handshake WPA de forma más fiable?"
    answer: "En las pruebas, el AWUS036EACS es el más sólido: la inyección en ambas bandas alcanza el 100%, tras el deauth recibió 79 ACKs de confirmación y logró exportar un archivo .22000 utilizable por hashcat, siendo el modelo con la verificación de extremo a extremo más completa de este lote."
  - question: "¿Por qué un iPhone antiguo no conecta a un punto de acceso WPA3-SAE?"
    answer: "La clave está en el parámetro sae_pwe de hostapd: fijado en 2 (forzando H2E), el iPhone 7 Plus falla la conexión; al volver a sae_pwe=0 (Hunting-and-Pecking), puede completar con normalidad el 4-way handshake y conectar."
  - question: "¿En un entorno WPA3 aún se puede capturar el 4-way handshake?"
    answer: "Un entorno WPA3-SAE puro fuerza la activación de PMF (ieee80211w=2) y las técnicas tradicionales dirigidas a las management frames quedan bloqueadas; que en la práctica aún se pueda capturar el handshake se debe en su mayoría a que el objetivo corre en modo de transición WPA2/WPA3, y no en WPA3 puro."
  - question: "No logro medir la inyección en 5GHz de un adaptador ALFA, ¿es un problema de hardware?"
    answer: "No necesariamente. El dominio regulatorio por defecto limita la potencia de transmisión de parte de las bandas de 5GHz, de modo que la inyección «no sale»; en las pruebas, tras cambiar el dominio regulatorio a un estado que permite transmitir, la inyección en 5GHz que antes fallaba pasó a ser usable, por lo que se recomienda confirmar primero el ajuste del dominio regulatorio antes de juzgar si se trata de una limitación de hardware."
draft: false
---

> Unidad de pruebas: Yupitek (distribuidor de ALFA Network en Taiwán) | Plataforma de pruebas: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 | Dispositivo de prueba: iPhone 7 Plus propio (WPA3 verificado adicionalmente con iPhone 15 Pro) | Objetivo de prueba: WiFi propio de la oficina (SSID YUPITEK, 2.4G ch5 / 5G ch36, 157).
>
> Este artículo es una visión general de las capacidades y la compatibilidad de los adaptadores WiFi ALFA. Toda captura de Monitor / Injection / handshake se realiza sobre equipos propios de Yupitek, el WiFi propio de la oficina y teléfonos de prueba propios; es una validación de capacidad legítima de un distribuidor sobre su hardware, no se dirige a ninguna red de terceros ni ofrece pasos de operación de ataque.

## Resumen (TL;DR)

De las 9 tarjetas ALFA probadas en ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17), 7 (ACM, ACHM, ACH, ACS, EACS, AX, AXER) completaron la captura de handshake WPA de extremo a extremo hasta el `.22000`; la AWUS036EACS alcanzó el 100% de inyección en ambas bandas con 79 ACKs, mientras que las AXM / AXML con MT7921 fallan la inyección en esta plataforma.

- Con la difusión de WPA3-SAE, el foco de la auditoría pasa de «si se puede o no hacer monitor» a «la capacidad de captura de handshake de extremo a extremo» y «la compatibilidad de endpoint de `sae_pwe`».
- **El `.22000` de extremo a extremo está demostrado en 7 de 9 modelos**: ACM, ACHM, ACH, ACS, EACS, AX, AXER; entre ellos, el EACS es el más sólido (100% de inyección en ambas bandas, 79 ACKs).
- **El AXM / AXML (MT7921) falla la inyección en esta plataforma**, no puede hacer deauth, no captura handshake; evítelos sin falta para uso de auditoría.
- Campo de minas de `sae_pwe`: los iPhone antiguos necesitan `sae_pwe=0` para conectar; antes de inyectar en 5G, `iw reg set US` para desbloquear la TX.
- El WPA3 puro fuerza PMF (`ieee80211w=2`); que sobre el terreno aún se pueda capturar se debe en su mayoría a que el objetivo corre en modo de transición WPA2/WPA3.

## 1. La difusión de WPA3-SAE ha elevado por completo el listón de la auditoría inalámbrica

Durante la última década, la auditoría inalámbrica dentro de un alcance autorizado (authorized wireless audit) giraba casi siempre en torno al 4-way handshake de WPA2-PSK: capturar un handshake completo y el backend ya podía comparar sin conexión. Pero desde que la certificación Wi-Fi 6 incorporó WPA3 como requisito obligatorio, SAE (Simultaneous Authentication of Equals, conocido como Dragonfly) reemplaza progresivamente a PSK y estrecha cada vez más ese viejo camino de «capturar el handshake y verificar sin conexión».

Para los distribuidores y los ingenieros de primera línea, WPA3-SAE trae tres cambios prácticos:

1. **PMF (Protected Management Frame) pasa a ser obligatorio**. La especificación WPA3-SAE fuerza activar `ieee80211w=2`, las management frames quedan protegidas, y la práctica tradicional de «soltar un deauth y tirar al dispositivo de la red» queda directamente bloqueada en un entorno WPA3 puro.
2. **El modo de transición (transition mode) conserva el 4-way**. En la realidad, una gran cantidad de AP corren en modo de transición mixto WPA2/WPA3 y, por compatibilidad con los dispositivos antiguos, conservan el 4-way handshake de WPA2; esta es también la razón principal de que la auditoría autorizada aún pueda capturar el handshake hoy en día. Poder capturar o no el handshake depende en gran parte del modo en que esté el objetivo sobre el terreno.
3. **La compatibilidad de endpoint se convierte en el nuevo campo de minas**. SAE tiene distintas formas de derivar el password element (controladas por `sae_pwe`); si se configura mal un parámetro del AP, ni siquiera el propio iPhone antiguo conecta, y ya no digamos reproducir en la auditoría el comportamiento de conexión del endpoint del cliente.

Por ello, cuando un cliente pregunta «qué tarjeta ALFA sirve para la auditoría autorizada relacionada con WPA3», la respuesta ya no es tan simple como «si puede o no hacer monitor», sino que depende de dos cosas: **la capacidad de captura de handshake de extremo a extremo** y **la compatibilidad con los parámetros WPA3-SAE y los endpoints reales**. Este informe es precisamente la tabla de capacidades que resulta tras probar 9 tarjetas ALFA sobre una misma plataforma ARM64.

## 2. Qué significa «capacidad de captura de handshake de extremo a extremo» (nivel conceptual)

Primero desglosamos la capacidad en tres tramos, de forma puramente conceptual, sin involucrar ningún comando de operación contra redes de terceros:

- **Primer tramo: Injection (inyección activa)**. El adaptador tiene que poder «emitir hacia fuera» una management frame concreta para provocar que un cliente ya conectado vuelva a asociarse. Muchas tarjetas solo pueden hacer monitor pasivo (recibir paquetes), pero no inyección (emisión activa). Es el tramo donde más fácil se atasca toda la cadena. En este lote de pruebas cuantificamos la tasa de éxito de inyección con `aireplay-ng --test`, y en la prueba de handshake verificamos si la trama llegó de verdad mediante el número de ACKs devueltos por el cliente.
- **Segundo tramo: captura del 4-way handshake**. Cuando el cliente se reasocia, WPA intercambia cuatro mensajes EAPOL (M1–M4). El adaptador, en modo monitor, debe recoger las cuatro tramas completas, sin que falte ninguna.
- **Tercer tramo: exportar al `.22000` de hashcat**. Convertir el pcap capturado al formato `.22000` de hashcat con `hcxpcapngtool --all`, para que el backend haga la verificación sin conexión.

**Solo cuando los tres tramos funcionan sobre equipo real se considera «de extremo a extremo»**: enviar de verdad un deauth (inyección) al propio iPhone 7 Plus → recoger los M1–M4 completos → exportar el `.22000` a disco. Poder solo recibir pero no emitir, o no recoger las cuatro tramas, o no poder exportar el archivo, no cuenta como extremo a extremo. Este artículo no enumera ningún comando de ataque paso a paso; la siguiente tabla solo responde a una pregunta: qué tarjeta recorre esta cadena de capacidad hasta el final.

Tomando como ejemplo el EACS, el más sólido de este lote, un extremo a extremo exitoso tiene este aspecto: tras enviar el deauth, el cliente devuelve **79 ACKs** (confirmando que la trama llegó efectivamente a ese teléfono), `aircrack-ng` determina que YUPITEK tiene 1 handshake, las cuatro tramas M1 / M2 / M3 / M4 del EAPOL reciben 1 copia cada una, la MAC del cliente capturada empieza con el OUI de Apple (confirmando que es ese iPhone 7 Plus), y por último `hcxpcapngtool --all` exporta un `.22000` de unos 784 bytes. Si falta una sola de estas cuatro condiciones, la captura no cuenta. Por eso «poder hacer monitor» y «poder capturar de extremo a extremo» son dos cosas completamente distintas.

## 3. Tabla comparativa de la capacidad de handshake de las 9 tarjetas

| # | Modelo | Chip / Generación | Injection 2.4G | Injection 5G | Capacidad de captura de handshake WPA |
|---|---|---|---|---|---|
| 1 | AWUS036ACM | MT7612U / Wi-Fi 5 · 2T2R | usable 63–83% | usable 76% | **`.22000` de extremo a extremo demostrado** (menor tasa de inyección) |
| 2 | AWUS036ACHM | MT7610U / Wi-Fi 5 · 1T1R | usable 96–100% | solo broadcast | **`.22000` de extremo a extremo demostrado (en 5 GHz ch36)** |
| 3 | **AWUS036ACH** | RTL8812AU / Wi-Fi 5 · 2T2R | **100%** | **100%** | **`.22000` de extremo a extremo demostrado (reverificado el 2026-11-19)** |
| 4 | **AWUS036ACS** | RTL8811AU / Wi-Fi 5 · 1x1 | **100%** | 96% | **`.22000` de extremo a extremo demostrado** |
| 5 | **AWUS036EACS** | RTL8821CU / Wi-Fi 5 · 1x1 | **100%** | **100%** | **`.22000` de extremo a extremo demostrado (79 ACKs)** |
| 6 | **AWUS036AX** | RTL8832BU / Wi-Fi 6 · 2x2 | 96% | usable | **`.22000` de extremo a extremo demostrado** |
| 7 | **AWUS036AXER** | RTL8832BU / Wi-Fi 6 · 2x2 | 73% | usable | **`.22000` de extremo a extremo demostrado** |
| 8 | AWUS036AXM | MT7921AU / Wi-Fi 6 · 2x2 | falla | falla | No compatible: la inyección falla, no puede capturar |
| 9 | AWUS036AXML | MT7921AUN / Wi-Fi 6 · 2x2 | falla | falla | No compatible: la inyección falla, no puede capturar |

**Dos grupos, de un vistazo:**

- **Extremo a extremo demostrado (captura → `.22000` en disco, 7 de 9 modelos)**: AWUS036ACM, AWUS036ACHM, AWUS036ACH, AWUS036ACS, AWUS036EACS, AWUS036AX y AWUS036AXER. Entre ellos, el EACS tiene el 100% de inyección en ambas bandas y recibió 79 ACKs tras el deauth, siendo la tarjeta con la capacidad de handshake más sólida de este lote; el AWUS036ACH (RTL8812AU, doble antena de alta ganancia) tiene el 100% de inyección en ambas bandas y, en la reverificación del 2026-11-19, exportó un `.22000` de 47 líneas de hashline, quedando a la par del EACS como primera opción para pruebas de penetración. **Siete modelos completaron la captura de handshake de extremo a extremo: ACM, ACHM, ACH, ACS, EACS, AX, AXER.** El ACM inyecta a una tasa menor (2.4G 63–83% / 5G 76%) y el ACHM lo completó en 5 GHz (ch36), pero ambos produjeron un `.22000`.
- **No pueden capturar (2 modelos)**: AWUS036AXM y AWUS036AXML (el MT7921 falla la inyección en esta plataforma, no puede hacer deauth y, naturalmente, tampoco puede capturar el handshake).

Hay que señalar en particular al **AXM / AXML**: ambos son Wi-Fi 6, con monitor y AP normales, pero solo la inyección no funciona en esta plataforma; la causa principal es la regresión de chanctx de mac80211 del kernel stock 6.16+ (no una limitación nativa del chip); aunque la comunidad logra que el mismo modelo funcione con controladores de git / parcheados, el firmware bloquea la tasa (ver morrownr/USB-WiFi #387, morrownr/mt76 #18). Para navegar o montar un punto de acceso no hay problema, pero **para cualquier uso de auditoría que requiera inyección o captura de handshake, evítelos sin excepción en esta plataforma**.

## 4. Campo de minas de compatibilidad WPA3-SAE: con un parámetro mal puesto, ni tu propio iPhone conecta

Más allá de la capacidad, la compatibilidad de parámetros de WPA3-SAE es donde más fácil se naufraga sobre el terreno. En este lote de pruebas tropezamos con dos minas clave:

### 4-1. El ACHM necesita obligatoriamente `sae_pwe=0`, o el iPhone 7 Plus no conecta

La derivación del password element de SAE tiene distintas formas, que hostapd controla con `sae_pwe`. Al montar el AWUS036ACHM como WPA3-SAE puro (`wpa_key_mgmt=SAE` + PMF forzado `ieee80211w=2`), en cuanto `sae_pwe` se fijaba en `2`, **el iPhone 7 Plus no conectaba en absoluto**; tras volver a `sae_pwe=0` (Hunting-and-Pecking, compatible con endpoints antiguos), el iPhone 7 Plus (iOS 15) conectó sin problemas y completó el 4-way.

El sentido de esta mina es: cuando quiera «reproducir» en la auditoría un entorno WPA3 con endpoints principalmente de iOS antiguo, el `sae_pwe` del lado del AP debe acompañar la capacidad del endpoint; de lo contrario, lo que obtendrá será un falso negativo de «no conecta», en lugar de una conclusión real de compatibilidad. Las pruebas del AP WPA3-SAE del EACS y el ACS también usaron `sae_pwe=0` + `ieee80211w=2`, y el iPhone 7 Plus conectó en ambos casos; `sae_pwe=0` es justamente el valor seguro que este lote verificó contra los endpoints de iPhone antiguos.

### 4-2. Antes de la inyección en 5G, `iw reg set US` para desbloquear la TX

La segunda mina tiene que ver con el dominio regulatorio (regulatory domain). El `reg=TW` por defecto bloquea la TX de parte de las bandas UNII, de modo que la inyección / deauth de 5 GHz «no sale». En este lote, antes de hacer inyección en 5G siempre `iw reg set US` para desbloquear la TX, y al terminar, de inmediato `iw reg set TW` para restaurar. La inyección en 5G del ACS pasó de fallar a un 96% tras el desbloqueo, y el EACS y el ACH subieron directamente al 100%. Olvidar desbloquear el reg hace que una tarjeta con una capacidad de inyección normal se juzgue erróneamente como «5G inutilizable».

### 4-3. A propósito: el PMF es obligatorio en WPA3

La especificación WPA3-SAE fuerza `ieee80211w=2` (Management Frame Protection). Esto significa que, en un entorno WPA3 puro, las técnicas tradicionales dirigidas a las management frames quedan bloqueadas por el PMF; que la auditoría real aún pueda capturar el 4-way se debe en su mayoría a que el objetivo sigue corriendo en modo de transición WPA2/WPA3. Tenga en cuenta este punto al elegir la tarjeta para no hacerse falsas expectativas con un objetivo WPA3 puro.

## 5. Visión general de la cadena de herramientas: la que realmente funciona en una plataforma ARM64

Más allá de la capacidad del hardware, la cadena de herramientas de la plataforma también influye en la eficiencia de la auditoría. A continuación, varias conclusiones prácticas que este lote obtuvo sobre el GX10 (ARM64):

- **Para la conversión, siempre `hcxpcapngtool --all`**. Los parámetros por defecto son más estrictos y suelen devolver «not enough M1» sin exportar el archivo; añadiendo `--all` se puede exportar de forma estable el `.22000` a partir de los M1–M4 completos.
- **Con varios AP del mismo nombre en la oficina, no fije `--bssid`**. En la oficina de Yupitek hay varios AP YUPITEK con el mismo nombre en el mismo canal, y el iPhone se conecta al de señal más fuerte. Si al capturar fija un único BSSID con `--bssid`, es muy probable que filtre precisamente el AP al que el iPhone está realmente conectado y que toda la captura quede en nada. La conclusión de las pruebas es **no fijar el BSSID y capturar directamente todo el canal**, y luego seleccionar el handshake completo del archivo en disco.
- **`hcxdumptool` 8.x da `failed to arm` en esta plataforma, salvo el EACS en 2.4 GHz (en 5 GHz falla)**. rtw88 / rtw89 / mt7921u no ofrecen active-monitor, y hcxdumptool 8.x lo necesita; la solución es cambiar al flujo clásico de aircrack-ng con `airodump-ng` + `aireplay-ng`.
- **Si tras alternar modos repetidamente no detecta nada, primero desconecte y reconecte la tarjeta**. rtw88 / rtw89 pueden sufrir un RX stall (escaneo de 0 paquetes) tras alternar repetidamente monitor / AP; la reenumeración del USB lo recupera, y el nombre de interfaz, que depende de la MAC, no cambia tras la reconexión. Antes de capturar el handshake, lo primero recomendable es volver a conectar la tarjeta una vez.
- **Los dispositivos combo BT+WiFi (EACS / AXML) tienen una condición de carrera al reconectar**. Las tarjetas combo con Bluetooth, al reconectarlas o al enchufarlas en ciertos puertos USB, sufren un bloqueo del probe de la función WiFi y no generan la interfaz `wlx`; la solución es cambiar de puerto USB y reconectar, pues `modprobe` o el bind manual suelen ser inútiles.
- **Detalles de instalación de herramientas en ARM64**. aircrack-ng a menudo carece de paquete precompilado en aarch64 y debe compilarse desde el código fuente; wifite se usa en su versión de git (la de apt entra en conflicto de dependencias con el aircrack-ng compilado a mano).
- **Regla de seguridad: nunca `airmon-ng check kill`**. El GX10 sale a internet por la tarjeta de red integrada, y `check kill` apagaría también NetworkManager y dejaría la máquina sin red. Este lote opera en todo momento solo sobre la interfaz `wlx*` de la tarjeta ALFA, sin tocar la línea principal integrada de salida a internet.

## 6. Resumen de selección: para auditoría relacionada con WPA3, qué modelos elegir

Mirando en conjunto la capacidad, la compatibilidad y la cadena de herramientas de la plataforma, para el uso de «auditoría autorizada relacionada con WPA3» la recomendación de este lote es:

| Escenario de necesidad | Modelo recomendado | Razón |
|---|---|---|
| Primera opción integral (inyección + handshake de extremo a extremo) | **AWUS036EACS** | 100% de inyección en ambas bandas, 79 ACKs recibidos tras el deauth, `.22000` de extremo a extremo demostrado; lo único a tener en cuenta es que, al ser un combo BT+WiFi, a veces hay que cambiar de puerto USB al reconectar |
| Alta ganancia / larga distancia + inyección fuerte | **AWUS036ACH** | RTL8812AU de doble antena, 100% de inyección en ambas bandas, fuerte capacidad de recepción |
| Ligero y portátil | **AWUS036ACS** | Flujo único, `.22000` de extremo a extremo demostrado, 96% de inyección en 5G |
| Necesidad de Wi-Fi 6 | **AWUS036AX / AWUS036AXER** | 2x2 VHT80, `.22000` de extremo a extremo demostrado; el AXER, con diseño de antena integrada (Nano) + afinado del chip, tiene la mayor cobertura de escaneo |
| **A evitar sin falta** | AWUS036AXM / AWUS036AXML | El MT7921 falla la inyección en esta plataforma, no puede capturar handshake |

Resumen en una frase: **para auditoría relacionada con WPA3, primero el EACS, luego el ACH / ACS; si necesita Wi-Fi 6, elija AX / AXER; evite sin falta el AXM / AXML.** De las siete tarjetas que completaron la captura de handshake de extremo a extremo, todas las de Realtek (rtw88 / rtw89) pueden inyectar, y las MediaTek ACM y ACHM (mt76) también lo lograron; el AXM / AXML de MT7921 no. Al seleccionar, reconocer el chip es más fiable que reconocer el nombre del modelo.

## Preguntas frecuentes (FAQ)

**P: ¿El AWUS036AXM puede capturar el handshake WPA en Ubuntu?**
R: En esta plataforma, no. En las pruebas, el AWUS036AXM y el AWUS036AXML (chip MT7921), al fallar la inyección y no poder enviar el deauth, cortan toda la cadena de captura del 4-way handshake, por lo que no son aptos para usos que requieran captura de handshake.

**P: ¿Qué adaptador ALFA captura el handshake WPA de forma más fiable?**
R: En las pruebas, el AWUS036EACS es el más sólido: la inyección en ambas bandas alcanza el 100%, tras el deauth recibió 79 ACKs de confirmación y logró exportar un archivo `.22000` utilizable por hashcat, siendo el modelo con la verificación de extremo a extremo más completa de este lote.

**P: ¿Por qué un iPhone antiguo no conecta a un punto de acceso WPA3-SAE?**
R: La clave está en el parámetro `sae_pwe` de hostapd: fijado en 2 (forzando H2E), el iPhone 7 Plus falla la conexión; al volver a `sae_pwe=0` (Hunting-and-Pecking), puede completar con normalidad el 4-way handshake y conectar.

**P: ¿En un entorno WPA3 aún se puede capturar el 4-way handshake?**
R: Un entorno WPA3-SAE puro fuerza la activación de PMF (`ieee80211w=2`) y las técnicas tradicionales dirigidas a las management frames quedan bloqueadas; que en la práctica aún se pueda capturar el handshake se debe en su mayoría a que el objetivo corre en modo de transición WPA2/WPA3, y no en WPA3 puro.

**P: No logro medir la inyección en 5GHz de un adaptador ALFA, ¿es un problema de hardware?**
R: No necesariamente. El dominio regulatorio por defecto limita la potencia de transmisión de parte de las bandas de 5GHz, de modo que la inyección «no sale»; en las pruebas, tras cambiar el dominio regulatorio a un estado que permite transmitir, la inyección en 5GHz que antes fallaba pasó a ser usable, por lo que se recomienda confirmar primero el ajuste del dominio regulatorio antes de juzgar si se trata de una limitación de hardware.

## 7. Lecturas adicionales

- [Tabla maestra de pruebas ARM64 y valoración de selección de 9 adaptadores WiFi ALFA](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Informes de pruebas por modelo: [Informe de pruebas del AWUS036EACS](/es/blog/awus036eacs-asus-gx10-ubuntu-test-report/), [Informe de pruebas del AWUS036ACS](/es/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*Todas las pruebas de este artículo se realizaron sobre el WiFi propio de la oficina de Yupitek (SSID YUPITEK) y contra un iPhone 7 Plus propio; constituyen una validación de capacidad legítima de un distribuidor sobre los adaptadores WiFi ALFA. Los datos proceden de los informes de pruebas reales del 2026-11-16 al 11-18, no se dirigen a ninguna red de terceros ni ofrecen pasos de operación de ataque. Unidad de pruebas: Yupitek (distribuidor de ALFA Network en Taiwán) — https://www.yupitek.com*
