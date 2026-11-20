---
title: "AWUS036ACH, prueba práctica: informe completo de Monitor, Inyección, AP y WPA3 del Realtek RTL8812AU de doble antena AC1200 en ASUS GX10 (ARM64 / Ubuntu 24.04)"
slug: awus036ach-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ach-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ach
  - rtl8812au
  - rtw88-8812au
  - realtek
  - wifi-5
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - alfa-network
  - asus-gx10
  - arm64
description: "El AWUS036ACH (RTL8812AU) funciona en Ubuntu 24.04 / kernel 6.17 sin DKMS: modo monitor en doble banda disponible, inyección de paquetes al 100% y handshake WPA de extremo a extremo (.22000) ya demostrado, además de límites como el bloqueo de la recepción en 5G."
faq:
  - question: "¿El AWUS036ACH necesita instalar controladores en Kali o Ubuntu?"
    answer: "Depende de la versión del kernel. Linux kernel 6.13 o superior (en esta prueba, Ubuntu 24.04 / kernel 6.17) ya trae integrado el controlador rtw88_8812au; se reconoce nada más conectarlo, sin compilar y sin DKMS; solo con un kernel inferior a 6.13 hay que instalar aparte lwfinger/rtw88 mediante DKMS. En Kali, confirme primero la versión del kernel con uname -r; esta vez no se verificó en Kali sobre hardware real."
  - question: "¿Cómo se comportan el modo monitor y la inyección de paquetes del AWUS036ACH?"
    answer: "Tanto en 2.4GHz como en 5GHz entra en modo monitor; la inyección dirigida por equipo con aireplay-ng es 30/30 = 100% en 2.4GHz (contra 4 AP) y en 5GHz (contra YUPITEK ch36). Antes de inyectar en 5GHz hay que fijar el dominio regulatorio a una configuración que permita emitir (por ejemplo iw reg set US); con el country 00 por defecto, 5GHz tiene prohibido emitir y la inyección no sale."
  - question: "¿El AWUS036ACH puede capturar el handshake WPA?"
    answer: "Sí, y está demostrado de extremo a extremo. La inyección es 100% en ambas bandas; el 2026-11-19, en una prueba adicional sobre un iPhone 15 Pro propio en 5GHz ch36, se capturó un handshake de 4 vías completo y con hcxpcapngtool se exportaron 47 hashlines .22000 de hashcat. Solo en redes propias o autorizadas."
  - question: "¿Qué hago si al abrir un punto de acceso WPA3 con el AWUS036ACH el iPhone 7 Plus no se conecta?"
    answer: "Hay que fijar sae_pwe=0 en hostapd junto con ieee80211w=2 para que el iPhone 7 Plus se conecte; con sae_pwe=2 no se conectará. La misma configuración es también clave en el AWUS036ACHM."
  - question: "¿Qué hago si la recepción en 5GHz del AWUS036ACH se bloquea de repente (captura 0 paquetes)?"
    answer: "Es un fenómeno conocido del rtw88_8812au: tras alternar modos repetidamente o cambiar el dominio regulatorio, la recepción en 5GHz puede bloquearse sin que el software pueda recuperarla; solo cabe desconectar y reconectar físicamente o reiniciar. Se recomienda reconectar la tarjeta antes de las pruebas de 5GHz y completar primero los puntos de 5GHz."
draft: false
---

> Entidad de prueba: Yupitek (distribuidor de ALFA Network en Taiwán) | Plataforma de prueba: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Dispositivo de prueba: Apple iPhone 7 Plus propio | Objetivo de prueba: Wi-Fi propia de la oficina (SSID `YUPITEK`, 2.4G ch5 / 5G ch36, 157) | Fecha de prueba: 2026-11-18.
>
> Este artículo es una verificación de hardware, por parte del distribuidor, de la compatibilidad y los límites de capacidad del producto: todas las mediciones de Monitor / Inyección / AP / handshake se realizaron sobre equipo propio de Yupitek, la Wi-Fi propia de la oficina y un teléfono de prueba propio; no se dirige contra ninguna red de terceros ni se ofrecen pasos de operación de ataque contra redes externas. Todos los datos del texto son cifras y estados medidos sobre hardware real, no inferidos de la hoja de especificaciones.

## Resumen (TL;DR)

En las pruebas en ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17), la AWUS036ACH funciona en modo monitor de doble banda, logra 30/30 = 100% de inyección de paquetes dirigida por AP en ambas bandas y monta un punto de acceso en ambas bandas (802.11g puro / 802.11a puro).

- Con kernel 6.13 o superior no hace falta instalar DKMS (en esta ocasión Ubuntu 24.04 / kernel 6.17); el rtw88_8812au va integrado y se reconoce nada más conectarlo.
- Modo monitor en doble banda disponible; la inyección de paquetes por equipo es 30/30 = 100% en ambas bandas.
- Handshake WPA de extremo a extremo ya demostrado: el 2026-11-19, en una prueba adicional sobre un iPhone 15 Pro propio en 5G ch36, se capturó un 4-way completo y se exportaron 47 hashlines .22000.
- La recepción en 5GHz puede bloquearse; solo cabe desconectar y reconectar físicamente o reiniciar.
- Puede crear un IBSS en un solo equipo, pero no admite mesh 802.11s, active monitor ni Wi-Fi Direct (P2P).

## 1. Esta tarjeta y la plataforma de prueba

El AWUS036ACH es el adaptador inalámbrico USB de ALFA Network posicionado como «doble antena de alta ganancia», con chip Realtek RTL8812AU y especificación Wi-Fi 5 (802.11ac), 2T2R, doble banda AC1200. Frente al AWUS036ACHM de una sola antena de la misma serie (MediaTek MT7610U, AC600), el ACH, con dos antenas externas de alta ganancia, obtiene una mejor recepción y una inyección más estable, siendo un candidato habitual cuando los clientes preguntan por «monitor de larga distancia» e «inyección en ambas bandas».

La plataforma y las condiciones de esta prueba son:

- Plataforma de cómputo: ASUS GX10 (ARM64 / aarch64)
- Sistema operativo: Ubuntu 24.04 LTS
- Versión del kernel: kernel 6.17.0-1014-nvidia
- Dispositivo de prueba: Apple iPhone 7 Plus (2.4G / 5G / WPA3 probados todos con este equipo)
- Entorno de prueba: Wi-Fi propia de la oficina, SSID `YUPITEK` (2.4GHz ch5 / 5GHz ch36, ch157)
- Fecha de prueba: mediciones sobre hardware real el 2026-11-18

Durante todo el proceso solo se opera sobre la interfaz `wlx*` correspondiente a la tarjeta ALFA, sin tocar la tarjeta de red integrada de salida a Internet del GX10 ni ejecutar `airmon-ng check kill` (ese comando cierra NetworkManager y deja al equipo sin conexión).

## 2. Hardware y controlador (chip / USB ID / integrado en el kernel, sin instalación)

| Elemento | Especificación |
|---|---|
| Modelo | AWUS036ACH |
| Chip | Realtek RTL8812AU |
| USB ID | `0bda:8812` |
| Controlador | `rtw88_8812au` (integrado en el kernel, mainline ≥ 6.13) |
| Firmware | `rtw88/rtw8812a_fw.bin` (incluido en el sistema) |
| Generación / flujos | Wi-Fi 5 (802.11ac) / 2T2R |
| Nivel de ancho de banda | Doble banda AC1200 |
| Antena | Doble antena de alta ganancia (externa) |
| Interfaz USB | USB 3.0 (enumerado en la prueba como 5000M) |

El ACH es realmente plug-and-play en el kernel 6.17 del GX10: `lsusb` reconoce `0bda:8812`, el controlador `rtw88_8812au` se enlaza automáticamente, el firmware `rtw8812a_fw.bin` ya viene incluido en el sistema, sin compilar y sin DKMS. Esto es especialmente importante en un entorno ARM64. Muchos controladores Realtek out-of-tree antiguos hay que compilarlos desde el código fuente en aarch64, y los dos proyectos veteranos morrownr/USB-WiFi y aircrack-ng/rtl8812au ahora ya redirigen a este controlador integrado, con los informes de errores concentrados en lwfinger/rtw88. Por eso los usuarios con kernel ≥ 6.13 (incluido el 6.17 del GX10) ya no tienen que lidiar con DKMS de terceros; solo con un kernel antiguo (< 6.13) hay que instalar aparte `lwfinger/rtw88` mediante DKMS. Este proyecto upstream sigue en mantenimiento activo (el commit más reciente es del 2026-10-24, con una corrección de Bluetooth 1T1R para el 8812A), lo que indica que el soporte de este chip en el mainline se sigue actualizando y no es un controlador antiguo sin mantenimiento.

Hay un detalle a tener en cuenta en la conexión física: el ACH es un conector macho USB-A; use un adaptador USB-C→A conectado directamente al puerto USB-C del GX10, por USB 3.0 (la enumeración muestra 5000M). Si lo conecta detrás del hub USB 2.0 del teclado y el ratón, quedará limitado en velocidad y no podrá medir el comportamiento de USB3.

En cuanto a los modos de interfaz, `iw phy` informa que admite IBSS / managed / AP / AP-VLAN / monitor, pero no mesh, P2P ni active-monitor, y esta frontera determina directamente parte de los límites de la sección 4.

## 3. Capacidades probadas: Monitor / Inyección / AP / WPA3

| Función | 2.4 GHz | 5 GHz | Datos medidos |
|---|---|---|---|
| Monitor | ✅ | ✅ | 2.4G ch1/6/11 = 92/214/71 frames; 5G ch36/149/157 = 260/137/127 frames |
| Inyección (probe por difusión) | ✅ | ✅ | `aireplay-ng --test` broadcast probe devuelve Injection is working en ambas bandas |
| Inyección (dirigida por equipo) | ✅ 30/30 = 100% | ✅ 30/30 = 100% | 2.4G contra 4 AP (incluido YUPITEK); 5G contra YUPITEK ch36 |
| AP (iPhone 7 Plus) | ✅ 802.11g puro | ✅ 802.11a puro (ch36) | handshake de 4 vías completado, conectado al primer intento |
| WPA3-SAE AP | ✅ (`sae_pwe=0`) | No probado | con `ieee80211w=2`, el iPhone 7 Plus se conecta (probado solo en 2.4 GHz) |

**Monitor**: en 2.4GHz capturó 92 / 214 / 71 frames en ch1 / ch6 / ch11 respectivamente; en 5GHz capturó 260 / 137 / 127 frames en ch36 / ch149 / ch157. El monitor es normal en ambas bandas, y la captura en 5GHz es incluso mayor que en 2.4GHz (260 frames en ch36), lo que concuerda con el posicionamiento de doble antena de alta ganancia.

**Inyección**: este es el punto fuerte del ACH. En 2.4GHz, `aireplay-ng --test` hace primero un broadcast probe (informa Injection is working, Found 4 APs) y luego la inyección dirigida por equipo; frente a los 4 AP, incluido YUPITEK, la tasa de respuesta es 30/30 = 100% en todos, con RTT min/avg/max de unos 4.9 / 39.2 / 99.0 ms y Power de unos -47. La inyección en 2.4G del ACH de doble antena es claramente más estable que la del ACHM de una sola antena. En la práctica hay que recordar añadir `--ignore-negative-one`: es un fenómeno conocido de lwfinger/rtw88 #453: con la interfaz STA abierta, el monitor channel puede informar `-1`, y sin esa flag se interpretaría por error como un fallo de inyección. Además, según los registros upstream, bajo inyección con carga alta el controlador integrado tiene de vez en cuando un USB reset, pero en la medición de unos 90 segundos de esta vez no se observó. En 5GHz, la inyección dirigida por equipo contra YUPITEK (ch36) es igualmente 30/30 = 100%, con RTT medio de 13.6 ms y Power -69.1. Este resultado se midió bajo la premisa de «tarjeta recién reconectada + regdomain fijado a una normativa que permite TX» (los detalles en las notas de 5G de la sección 4).

**AP**: abriendo el punto de acceso con hostapd, en 2.4GHz con 802.11g puro (`ieee80211n=0`) y en 5GHz con 802.11a puro (ch36), el iPhone 7 Plus se conecta al primer intento en ambas bandas, sin fallo de asociación; en el log se ve la secuencia completa de cuatro pasos authenticated → associated → AP-STA-CONNECTED → EAPOL-4WAY-HS-COMPLETED. La experiencia práctica es: el ACH conecta de la forma más limpia con la configuración de «802.11n desactivado, g puro / a puro».

**WPA3-SAE**: al abrir un AP solo SAE, el parámetro clave es `sae_pwe=0` (hunting-and-pecking) junto con `ieee80211w=2` para que el iPhone 7 Plus se conecte; con `sae_pwe=2` no se conecta. Es la misma trampa de compatibilidad que pisa el ACHM de la misma serie.

## 4. Capacidades avanzadas y handshake: alcance viable y límites honestos

| Capacidad avanzada | Resultado | Descripción / evidencia |
|---|---|---|
| VIF (STA + monitor a la vez) | ✅ verificado y disponible | La interfaz principal managed y `mon9` (monitor) up a la vez; la VIF monitor captura 100 frames en 8 s |
| Captura de handshake WPA | ✅ extremo a extremo (.22000) ya demostrado | Inyección 100% en ambas bandas; el 2026-11-19, prueba adicional en 5G ch36 capturó un 4-way completo, hcxpcapngtool exportó 47 hashlines `.22000` |
| macchanger (cambiar MAC) | ✅ | La configuración y restauración de MAC aleatoria son normales (hay que hacer antes `ip link down`) |
| Ad-hoc (IBSS) | 🟡 en local | `Joined IBSS` correcto en local; peer link no probado por falta de un segundo dispositivo |
| Active monitor | ❌ | `Operation not supported (-95)` |
| Mesh (802.11s) | ❌ | `Operation not supported (-95)` |
| Wi-Fi Direct (P2P) | ❌ | `Operation not supported (-95)` |

**Hay que dejar clara la capacidad de captura de handshake**: la inyección del ACH es 100% en ambas bandas, y la inyección es precisamente el extremo que dispara el flujo de trabajo de extremo a extremo «deauth del teléfono de prueba propio → captura del 4-way completo (M1–M4) → exportar el `.22000` de hashcat con hcxpcapngtool». El 2026-11-19, en una prueba adicional sobre un iPhone 15 Pro propio en 5GHz ch36, se capturó un handshake de 4 vías completo y con hcxpcapngtool se exportaron 47 hashlines `.22000`, por lo que la captura de handshake de extremo a extremo del ACH queda demostrada. En nuestra tabla general de 9 tarjetas, hay 7 de 9 con el extremo a extremo (`.22000`) ya demostrado: AWUS036ACM, AWUS036ACHM, AWUS036ACH, AWUS036ACS, AWUS036EACS, AWUS036AX y AWUS036AXER. Todas las capturas se limitan a redes propias o autorizadas.

**VIF**: las flags de `iw phy` indican interface combinations are not supported, pero en hardware real la interfaz principal managed y la interfaz monitor `mon9` abierta aparte pueden estar up a la vez; `mon9` captura 100 frames en 8 segundos, es decir, «navegar y capturar a la vez» funciona en el ACH. Hay que advertir que el phy no garantiza esta combinación; para escenarios de larga duración o carga alta, se recomienda pasar a la familia mt76 (ACM / ACHM).

**Tres límites que conviene marcar especialmente:**

1. **No admite Active monitor, Mesh (802.11s) ni Wi-Fi Direct (P2P)**: los tres devuelven en la prueba `Operation not supported (-95)`. Si necesita estas tres capacidades, pase a las tarjetas de la familia mt76 (el phy del ACM / ACHM declara mesh / P2P / active-monitor).
2. **Bloqueo de RX en 5G (fenómeno conocido del `rtw88_8812au`)**: recién conectada la tarjeta, el monitor / inyección en 5G es normal, pero tras alternar modos repetidamente o cambiar el regdomain, la recepción en 5G puede bloquearse (captura 0 paquetes) sin que el software pueda recuperarla; solo cabe desconectar y reconectar físicamente o reiniciar. Se recomienda desconectar y reconectar una vez antes de las pruebas de 5G y completar primero los puntos de 5G. Añadimos aquí la premisa para que la inyección en 5G pueda salir: con el `country 00` por defecto, 5G está todo en passive / no-IR (TX prohibido) y la inyección dirigida directamente no sale; hay que fijar una normativa que permita TX (`iw reg set US` desbloquea ch36 / ch149; `TW` solo permite de ch149 en adelante, sin ch36) y, al terminar, volver a `TW`. Y «tarjeta recién reconectada» significa una desconexión y reconexión física hasta la re-enumeración USB: `dmesg` tiene que mostrar `USB disconnect` y `renamed from wlan0`, y el número de bus debe cambiar para que cuente; si 5G ya está bloqueado, aireplay devuelve `No such BSSID available`.
3. **hcxdumptool devuelve `failed to arm` en todas las tarjetas de esta plataforma salvo el AWUS036EACS en 2.4 GHz**: porque requiere active-monitor, que rtw88 / rtw89 / mt7921u no admiten; para capturar el handshake, use la vía airodump-ng + aireplay-ng.

### Compatibilidad de la cadena de herramientas (Kali)

Se hizo un cribado rápido de las herramientas habituales de Kali sobre el ACH (con el entorno objetivo en la propia `YUPITEK`), con estos resultados:

| Herramienta | Estado | Descripción |
|---|---|---|
| airmon-ng | ✅ | Lista correctamente `phy2 / wlx... / rtw88_8812au / RTL8812AU 2T2R` |
| Wireshark / tshark | ✅ | `tshark -i $IF` captura beacons (incluido YUPITEK), 20 packets captured |
| kismet | ✅ instalado | `/usr/bin/kismet`, se puede arrancar como data source |
| bettercap | ✅ instalado | `/usr/bin/bettercap` |
| hcxdumptool | ⚠️ | Instalado, pero en esta plataforma `failed to arm` (requiere active-monitor, véase arriba) |
| macchanger | ✅ | GNU 1.7.0; `-r` aleatorio, `-p` restaura, normal en la prueba |
| wifite | ❌ no instalado | No existe el comando en el equipo, hay que instalarlo aparte (se recomienda la versión git para evitar el conflicto de dependencias de apt con el aircrack-ng compilado a mano) |

La conclusión es sencilla: airmon-ng reconoce y gestiona correctamente el ACH, y el flujo general de monitor y captura es más estable por la vía de la suite aircrack-ng (airodump-ng + aireplay-ng); hcxdumptool, que requiere active-monitor, no puede hacer arm en esta plataforma, así que no se obsesione con él.

## 5. Escenarios de uso y recomendaciones de selección (vuelta al Hub de la tabla general)

Al situar el ACH de nuevo en toda la línea de producto, su posicionamiento queda claro: doble antena de alta ganancia, inyección al 100% en ambas bandas, handshake WPA de extremo a extremo (.22000) ya demostrado; es la opción pragmática para el cliente que «necesita inyección estable y además quiere una recepción más fuerte».

- **Pruebas de penetración (inyección + handshake)**: el grupo preferente es AWUS036EACS / AWUS036ACH / AWUS036ACS; los tres rinden alto en inyección en ambas bandas.
- **Máxima recepción / monitor de larga distancia**: AWUS036AXER y AWUS036ACH, destacando el ACH por su doble antena de alta ganancia.
- **Cuando se necesita mesh 802.11s / active-monitor / P2P**: el ACH (Realtek rtw88) no puede (la prueba devuelve `-95`); use las tarjetas con controlador mt76 AWUS036ACM / AWUS036ACHM; el IBSS del ACH solo se crea en local y el peer-link no se ha probado.
- **Cuando solo se necesita AP puro o una conexión normal, sin inyección**: los MediaTek AWUS036AXM / AXML son más estables, pero tenga en cuenta que su inyección falla en esta plataforma y no sirven para usos de penetración.

Un aviso en una frase para evitar trampas: si la necesidad del cliente es claramente inyección y handshake, no elija el AWUS036AXM / AXML (la inyección del chip MT7921 falla en esta plataforma en la prueba, no puede hacer deauth ni capturar handshake); para esa necesidad, el ACH es más bien el candidato seguro. Al seleccionar modelo, tampoco se fije solo en las cifras de ancho de banda: la estabilidad de recepción que aporta la doble antena de alta ganancia a menudo se nota más en la distancia de captura real que en las especificaciones sobre el papel. Para la decisión de selección y las trampas comunes a la plataforma, véase el Hub de la tabla general: [9 adaptadores inalámbricos ALFA en ASUS GX10 (ARM64), matriz completa de Monitor, Inyección y AP](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Preguntas frecuentes (FAQ)

**P: ¿El AWUS036ACH necesita instalar controladores en Kali o Ubuntu?**
Depende de la versión del kernel. Linux kernel 6.13 o superior (en esta prueba, Ubuntu 24.04 / kernel 6.17) ya trae integrado el controlador rtw88_8812au; se reconoce nada más conectarlo, sin compilar y sin DKMS; solo con un kernel inferior a 6.13 hay que instalar aparte lwfinger/rtw88 mediante DKMS. En Kali, confirme primero la versión del kernel con uname -r; esta vez no se verificó en Kali sobre hardware real.

**P: ¿Cómo se comportan el modo monitor y la inyección de paquetes del AWUS036ACH?**
Tanto en 2.4GHz como en 5GHz entra en modo monitor; la inyección dirigida por equipo con aireplay-ng es 30/30 = 100% en 2.4GHz (contra 4 AP) y en 5GHz (contra YUPITEK ch36). Antes de inyectar en 5GHz hay que fijar el dominio regulatorio a una configuración que permita emitir (por ejemplo iw reg set US); con el country 00 por defecto, 5GHz tiene prohibido emitir y la inyección no sale.

**P: ¿El AWUS036ACH puede capturar el handshake WPA?**
Sí, y está demostrado de extremo a extremo. La inyección es 100% en ambas bandas; el 2026-11-19, en una prueba adicional sobre un iPhone 15 Pro propio en 5GHz ch36, se capturó un handshake de 4 vías completo y con hcxpcapngtool se exportaron 47 hashlines .22000 de hashcat. Solo en redes propias o autorizadas.

**P: ¿Qué hago si al abrir un punto de acceso WPA3 con el AWUS036ACH el iPhone 7 Plus no se conecta?**
Hay que fijar sae_pwe=0 en hostapd junto con ieee80211w=2 para que el iPhone 7 Plus se conecte; con sae_pwe=2 no se conectará. La misma configuración es también clave en el AWUS036ACHM.

**P: ¿Qué hago si la recepción en 5GHz del AWUS036ACH se bloquea de repente (captura 0 paquetes)?**
Es un fenómeno conocido del rtw88_8812au: tras alternar modos repetidamente o cambiar el dominio regulatorio, la recepción en 5GHz puede bloquearse sin que el software pueda recuperarla; solo cabe desconectar y reconectar físicamente o reiniciar. Se recomienda reconectar la tarjeta antes de las pruebas de 5GHz y completar primero los puntos de 5GHz.

## 6. Lecturas adicionales

- Hub de la tabla general: [9 adaptadores inalámbricos ALFA, matriz completa en ARM64](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Activar Monitor y AP en Ubuntu (ARM64) sin instalar controladores: [placeholder](/es/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- Captura de handshake WPA3-SAE y compatibilidad de `sae_pwe`: [placeholder](/es/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Comparación con la tarjeta hermana: AWUS036ACHM (una sola antena AC600), prueba práctica [placeholder]
- Ruta completa de evidencia de este modelo (interna): `AWUS036ACH_evidence/` (p0 enumeración, p1_gx10 comportamiento, retest de diagnóstico)

<!-- hreflang: zh-TW es el texto principal; zh-CN / en / ja / ko / de / fr / es se generarán y se añadirá rel=alternate una vez cerrado este texto. -->
