---
title: "ALFA AWUS036EACS, prueba de tarjeta individual: RTL8821CU (combinado BT + WiFi) en ASUS GX10 (ARM64 / Ubuntu 24.04) — modo monitor, inyección, AP y handshake de extremo a extremo"
slug: awus036eacs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036eacs-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036eacs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036eacs
  - rtl8821cu
  - rtw88-8821cu
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036EACS (combinado Bluetooth + Wi-Fi) probado en Ubuntu 24.04 ARM64: integrado en el kernel (sin instalar controlador); inyección al 100 % en ambas bandas, modo monitor, AP, WPA3-SAE y handshake de extremo a extremo (79 ACKs, .22000) superados. Incluye el riesgo de reenchufe USB. Plataforma ASUS GX10, RTL8821CU."
faq:
  - question: "¿Hace falta instalar un controlador para la AWUS036EACS en Ubuntu 24.04 ARM64?"
    answer: "En el kernel 6.17 probado en este artículo (ASUS GX10), no: el RTL8821CU lo gobierna el controlador integrado rtw88_8821cu; se reconoce nada más conectarlo, sin compilar ni DKMS; el nombre de la interfaz es wlx más la MAC y no cambia tras reenchufar."
  - question: "¿Cómo se comporta la AWUS036EACS en modo monitor e inyección de paquetes?"
    answer: "El modo monitor es estable en 2,4G y 5G, con la mayoría de los canales llenos a 300 tramas; aireplay-ng --test da 30/30 (100 %) en ambas bandas. Antes de inyectar en 5G hay que hacer iw reg set US para levantar la restricción de TW sobre la TX."
  - question: "¿Puede la AWUS036EACS capturar un handshake WPA?"
    answer: "Sí. Prueba de extremo a extremo con un AP propio y un iPhone 7 Plus propio: el deauth recibe 79 ACKs, se captura el M1–M4 completo y hcxpcapngtool --all genera el .22000 (784 bytes, 2 pares EAPOL). Solo en redes propias o autorizadas."
  - question: "¿Qué hago si tras conectar la AWUS036EACS lsusb la ve pero no aparece la interfaz de red wlx?"
    answer: "Es la condición de carrera en el probe de un dispositivo combinado BT+Wi-Fi: el Bluetooth ya está vinculado a btusb y el rtw88_8821cu del Wi-Fi se queda atascado. En la prueba, recargar el módulo o hacer bind manualmente no suele funcionar; la solución fiable es desconectar la tarjeta y reenchufarla en otro puerto USB."
  - question: "¿La AWUS036EACS admite mesh, IBSS o hcxdumptool?"
    answer: "No. El active-monitor, IBSS, mesh y P2P del rtw88 devuelven -95 o el join no es válido; hcxdumptool 8.x solo arranca en 2.4 GHz (en 5 GHz falla el arm), use en su lugar airodump-ng + aireplay-ng. El VHT es solo de 80 MHz. Para mesh / IBSS, elija la AWUS036ACM / ACHM."
draft: false
---

> Unidad de pruebas: Yopitek (distribuidor de ALFA Network en Taiwán) | Plataforma de pruebas: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Dispositivo de prueba: iPhone 7 Plus propio (WPA3 verificado además con iPhone 15 Pro) | Objetivo de prueba: Wi-Fi propia de la oficina (SSID YUPITEK, 2,4G ch5 / 5G ch36, 157).
>
> Este artículo es la prueba práctica de capacidades y compatibilidad de la tarjeta individual AWUS036EACS. Toda la captura de modo monitor / inyección / handshake se realizó sobre equipo propio de Yopitek, la Wi-Fi propia de la oficina y contra un teléfono de prueba propio; se trata de una verificación legítima de las capacidades del hardware por parte del distribuidor, no se dirige contra ninguna red de terceros ni se ofrecen pasos de operación ofensiva.

**Resumen (TL;DR)**: la AWUS036EACS en GX10 / Ubuntu 24.04 (kernel 6.17) no necesita instalar controlador; inyección al 100 % en ambas bandas, captura .22000 de extremo a extremo superada (79 ACKs); como tarjeta combinada BT+Wi-Fi, hay que vigilar el reenchufe.

## 1. La tarjeta y la plataforma de pruebas

La AWUS036EACS es el adaptador USB Wi-Fi 5 (802.11ac) ligero y portátil de ALFA; su chip es el Realtek RTL8821CU, un único flujo 1x1, doble banda 2,4 GHz y 5 GHz, y además integra Bluetooth, por lo que es un dispositivo combinado BT + WiFi. En este artículo la ponemos sola sobre la mesa de laboratorio de Yopitek y la verificamos punto por punto en un entorno ASUS GX10 (ARM64) con Ubuntu 24.04, respondiendo a las preguntas que más preocupan al cliente: ¿reconoce el controlador en ARM64?, ¿en qué modos puede entrar?, ¿hasta dónde llega su rendimiento?

Dejemos claro primero el posicionamiento. Esto es una verificación de compatibilidad y de los límites de capacidad que el distribuidor hace sobre su propia mercancía, no un tutorial ofensivo. Todas las mediciones de capacidad de inyección y handshake de este texto se realizan en un entorno cerrado propio y contra dispositivos propios, y no se ofrece ningún paso de operación contra redes externas.

La plataforma y la metodología de pruebas se ajustan a las de los demás artículos de tarjeta individual de esta tanda:

- Plataforma de cómputo: ASUS GX10 (ARM64 / aarch64)
- Sistema operativo: Ubuntu 24.04 LTS, kernel 6.17.0-1014-nvidia
- Estrategia de controlador: usar el controlador integrado en el kernel (in-kernel); se reconoce nada más conectarlo, sin instalar ningún módulo DKMS de terceros
- Dispositivo de prueba: Apple iPhone 7 Plus (el WPA3-SAE se verificó además con un iPhone 15 Pro)
- Entorno de prueba: Wi-Fi propia de la oficina, SSID YUPITEK, 2,4 GHz ch5 / 5 GHz ch36, ch157
- Regla de seguridad: en todo momento solo se opera la interfaz `wlx*`, sin tocar la línea principal integrada de salida a Internet; nunca se ejecuta `airmon-ng check kill` (apagaría NetworkManager y dejaría al GX10 sin conexión externa)

## 2. Hardware y controlador: la verdad sobre un dispositivo combinado BT + WiFi

Veamos primero el detalle. La siguiente tabla es el estado real de carga de la AWUS036EACS en el kernel 6.17:

| Elemento | Contenido |
|---|---|
| Chip | Realtek RTL8821CU (un único flujo 1x1) |
| Generación | Wi-Fi 5 (802.11ac), 2,4 + 5 GHz |
| Función combinada | dispositivo combinado BT + WiFi (incluye Bluetooth) |
| USB ID | `0bda:c820` |
| Controlador | `rtw88_8821cu` (integrado en el kernel; USB admitido desde el kernel 6.2) |
| Firmware | 24.11.0 (H2C version 12, medido en dmesg) |
| Ancho de banda VHT | solo 80 MHz (sin 160 / 80+80) |

Consultando con `iw phy`, los modos de interfaz admitidos son `managed` / `AP` / `AP/VLAN` / `monitor` (`IBSS` aparece listado pero en la prueba el join no es válido); la cobertura de bandas abarca 2,4 GHz ch1–13 y 5 GHz ch36–165 (los ch52–144 son banda DFS); entre los cifrados figuran CCMP-256, GCMP-128 / GCMP-256 y CMAC, de modo que reúne las condiciones para ejecutar WPA3 en el lado AP.

En cuanto al controlador no hay incógnitas. El soporte USB del RTL8821CU se integró en el `rtw88` mainline a partir del kernel 6.2; el kernel 6.17 del GX10 ya incorpora el `rtw88_8821cu`, que se carga nada más conectarlo, sin compilar ni DKMS. Las versiones integradas tempranas tuvieron un bug en el modo AP, ya corregido por el macid patch (desde linux-next-20240911); en esta ocasión, sobre el kernel 6.17, los tres modos de AP cerraron correctamente en la prueba. Forma de comprobarlo:

```bash
lsusb | grep -i '0bda:c820'
# ID 0bda:c820 Realtek Semiconductor Corp. 802.11ac NIC
sudo dmesg | grep -i 8821cu
# rtw88_8821cu ...: Firmware version 24.11.0, H2C version 12 -> renamed from wlan0
```

Una vez cargada, la interfaz Wi-Fi se nombra como `wlx` + MAC (por ejemplo `wlx00c0cab3a52e`), y no `wlan0`; el nombre no cambia tras reenchufar, así que se puede referenciar de forma estable al escribir scripts.

Lo que de verdad hay que vigilar es el hecho de que sea un «dispositivo combinado». Inspeccionándolo con `lsusb -t`, se ve que bajo un mismo chip RTL8821CU cuelgan varias interfaces USB: la función Bluetooth está vinculada a `btusb` y la función Wi-Fi, por separado, a `rtw88_8821cu`.

```
/:  Bus 0X.Port X: Dev X, Class=root_hub, Driver=xhci-hcd
    |__ Port X: Dev X, If 0, Class=Wireless, Driver=btusb               <- Bluetooth
    |__ Port X: Dev X, If 1, Class=Wireless, Driver=btusb               <- Bluetooth
    |__ Port X: Dev X, If 2, Class=Vendor Specific, Driver=rtw88_8821cu <- Wi-Fi
```

(La numeración de Bus/Port cambia con cada conexión; lo importante es que las interfaces 0/1 van por `btusb` y la interfaz 2 es la Wi-Fi del `rtw88_8821cu`.)

**El riesgo de reenchufe de un dispositivo combinado BT + WiFi (lectura obligatoria antes del despliegue).** Como Bluetooth y Wi-Fi comparten el mismo dispositivo USB, en ciertos puertos USB o al reenchufar con rapidez puede ocurrir que el Bluetooth ya se haya vinculado a `btusb` pero el probe de la interfaz de Wi-Fi se quede atascado, con la condición de carrera resultante: `lsusb` ve el `0bda:c820` pero no se genera la interfaz `wlx`. En la prueba, recargar tras `modprobe -r` o hacer `bind` manualmente no suele funcionar (`bind` devuelve `Operation already in progress`). Solo hay una solución fiable: desconectar la tarjeta y reenchufarla en otro puerto USB; tras el cambio de puerto la enumeración queda limpia y la interfaz `wlx` aparece con normalidad. Este es el detalle operativo extra que conviene conocer de esta tarjeta frente a la AWUS036ACS (RTL8811AU), que no es combinada; sabiéndolo de antemano no se confundirá con una avería de la tarjeta.

## 3. Capacidades medidas: modo monitor / inyección / AP / WPA3

La siguiente tabla es el resumen de las capacidades clave medidas de la AWUS036EACS; cada fila se ejecutó el 2026-11-18 sobre el GX10 real:

| Capacidad | 2,4 GHz | 5 GHz | Puntos clave de la prueba |
|---|---|---|---|
| Modo monitor | ✅ fuerte | ✅ fuerte | la mayoría de los canales llenos a 300 tramas; el «ch1 bloqueado» del hilo #453 de la comunidad no se reprodujo |
| Inyección | ✅ 100 % (30/30) | ✅ 100 % (30/30) | Power 2,4G -38,27 / 5G -76,10; la inyección más fuerte entre las tarjetas ac de esta tanda |
| Punto de acceso | ✅ cierre limpio | ✅ 802.11a, 20 MHz (VHT80 no probado) | `hostapd` levanta la estación; el iPhone 7 Plus se asocia y completa el 4-way |
| WPA3-SAE (lado AP) | ✅ iPhone asociado | No probado | SAE-only + PMF forzado (`ieee80211w=2`, `sae_pwe=0`) |
| Captura de handshake WPA | — | ✅ de extremo a extremo | M1–M4 completos, el deauth recibe 79 ACKs, se genera el `.22000` |

El modo monitor es estable tanto en 2,4 como en 5 GHz. Capturando uno a uno en los seis canales, la mayoría reciben el cupo completo de 300 tramas. Para el 8821cu, aquí hay además un resultado positivo muy importante: el GitHub #453 que la comunidad de rtw88 lleva tiempo siguiendo («el 8821cu, en kernel ≥6.9 y con la STA up, se queda bloqueado en modo monitor en ch1») no se reprodujo en este entorno GX10; en 5 GHz, los ch36, ch149 y ch157 reciben con estabilidad las 300 tramas completas. Para hacer prospección de espectro o análisis de paquetes entre 2,4 / 5 GHz, el modo monitor de esta tarjeta se puede usar con confianza.

La inyección de paquetes es lo más llamativo. Medida con `aireplay-ng --test`, tanto 2,4 GHz como 5 GHz dan 30/30, 100 %, la inyección más fuerte entre las tarjetas ac de esta tanda (la AWUS036ACS, también 1x1, solo alcanza el 96 % en 5G). Aquí hay un detalle local de Taiwán: la TX de 5 GHz queda bloqueada cuando el dominio regulatorio está en TW; antes de medir, haga `iw reg set US` para desbloquear, y al terminar restaure con `iw reg set TW`.

En cuanto al punto de acceso, con `hostapd` montamos por separado 2,4 GHz (WPA2), 5 GHz (802.11a, 20 MHz; VHT80 no probado) y WPA3-SAE; el iPhone 7 Plus se asocia y completa el 4-way handshake en los tres, y el cierre de la estación es limpio (`AP-DISABLED` / `TERMINATING`). No aparece el problema de re-key de beacon que tienen algunas tarjetas, y en este aspecto de 2,4G es más estable que su tarjeta hermana ACS. El WPA3 usa SAE-only con PMF forzado (`ieee80211w=2`, `sae_pwe=0`); el iPhone 15 Pro se asocia correctamente, lo que confirma que el WPA3-SAE del RTL8821CU en el lado AP está disponible.

La cadena de herramientas de Kali (a nivel de plataforma) también funciona bien sobre esta tarjeta: `airmon-ng` detecta la EACS (`rtw88_8821cu`), pero tampoco hay que usar `check kill`; `kismet` arranca correctamente con esta tarjeta como data source y en la prueba genera un log `.kismet` de unos 733 KB; el `wifi.recon on` de `bettercap` 2.32 funciona con normalidad (la advertencia de txpower se puede ignorar); `wifite` (git 3.0.0) escanea más de 10 AP, incluido el propio YUPITEK (ch5, PWR 84), y como esta versión no tiene el flag `--band`, hay que indicar los canales con `-c 1,6,11,36,149,157`; `Wireshark` / `tshark` 4.x captura y analiza 325 tramas en modo monitor ch6; y la suplantación de MAC aleatoria con `macchanger` también funciona. Este apartado de la capa de herramientas coincide con el de las demás tarjetas de la tanda; las diferencias recaen sobre todo en las capacidades de hardware de inyección y monitor comentadas antes.

## 4. Handshake de extremo a extremo: puntos fuertes y limitaciones honestas

La capacidad estrella de esta tarjeta es encadenar la inyección y la captura en una cadena completa y utilizable. Entre el AP propio YUPITEK y el iPhone 7 Plus propio, la cadena entera se ejecutó en el equipo real: enviar un deauth al iPhone propio (inyección; en la prueba se reciben 79 ACKs, lo que confirma que los paquetes inyectados llegan de verdad al cliente) → al reconectarse, el iPhone completa el 4-way handshake íntegro (M1, M2, M3, M4, uno de cada) → con `hcxpcapngtool --all` se genera el `.22000` en formato hashcat (784 bytes, 2 pares EAPOL, RC checked). Todo el proceso tiene como único fin verificar la capacidad de la tarjeta; el objetivo es en todo momento el AP propio y un teléfono propio, y no contempla ninguna red de terceros.

En la práctica, dos detalles clave conviene anotar: la oficina tiene a la vez varios AP YUPITEK con el mismo nombre en ch36, así que al capturar no acote con `--bssid`, capture todo el canal directamente para no filtrar el AP al que el iPhone está realmente asociado; además, `hcxpcapngtool` es estricto por defecto, hay que añadir `--all` para que genere el `.22000`.

También hay que exponer de una vez las limitaciones honestas:

- **No admite active-monitor / IBSS (Ad-hoc) / Mesh (802.11s) / Wi-Fi Direct (P2P).** En `rtw88` estos modos devuelven `-95` (Operation not supported), o aparecen listados pero el join no es válido; es una limitación a nivel de controlador, sin solución. Los clientes que necesiten experimentar con mesh / IBSS deben pasarse a la AWUS036ACM / ACHM de MediaTek.
- **`hcxdumptool` 8.x es limitado.** Necesita active-monitor; en esta tarjeta solo arranca en 2.4 GHz y falla el arm en 5 GHz (el resto de tarjetas de la tanda devuelven todas `failed to arm interface`); use en su lugar `airodump-ng` + `aireplay-ng`, que con la inyección al 100 % de esta tarjeta no se ve afectado.
- **VHT solo de 80 MHz.** Un único flujo, sin 160 MHz ni 80+80; su posicionamiento es el de un adaptador ligero y portátil, no el de exprimir el rendimiento.
- **VIF parcial.** Solo funciona un monitor pasivo junto a una interfaz managed en el mismo canal (monitor por software; 100 tramas en la prueba); no se admiten VIF duales independientes.

## 5. Casos de uso y selección de modelo

En conjunto, la prueba deja claro el posicionamiento de la AWUS036EACS: cuando se necesita verificación de modo monitor + inyección en doble banda y handshake de extremo a extremo, y además se quiere un adaptador portátil, compacto y con Bluetooth integrado, es la solución adecuada. Su inyección al 100 % en ambas bandas y su limpio comportamiento de AP / WPA3 la sitúan, junto a la AWUS036ACH y la AWUS036ACS, en el grupo de primera elección para auditoría inalámbrica y docencia de seguridad dentro del alcance autorizado.

En qué casos conviene elegir otra:

- **Si en campo se va a reenchufar con frecuencia, o la calidad de los puertos USB del chasis es dispar** → la condición de carrera del probe de un dispositivo combinado añade molestias; puede plantearse la AWUS036ACS (RTL8811AU), no combinada, también 1x1 ac y sin la variable añadida del Bluetooth.
- **Para experimentar con mesh / IBSS** → `rtw88` no lo admite; pásese a la AWUS036ACM / ACHM de MediaTek.
- **Para buscar la máxima recepción o un monitor de largo alcance** → la AWUS036ACH de doble antena o la AWUS036AXER de Wi-Fi 6 son más adecuadas.
- **A evitar**: si el uso es inyección / handshake, no elija la AWUS036AXM / AXML con MT7921, cuya inyección falla directamente en esta plataforma.

Si quiere ver de una vez la comparativa transversal de modo monitor / inyección / AP / WPA3 de las 9 tarjetas ALFA y la matriz de selección completa, vuelva a la tabla general: [La prueba más completa de 2026: matriz total de 9 adaptadores inalámbricos ALFA en ASUS GX10](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Preguntas frecuentes (FAQ)

**P: ¿Hace falta instalar un controlador para la AWUS036EACS en Ubuntu 24.04 ARM64?**
En el kernel 6.17 probado en este artículo (ASUS GX10), no: el RTL8821CU lo gobierna el controlador integrado rtw88_8821cu; se reconoce nada más conectarlo, sin compilar ni DKMS; el nombre de la interfaz es wlx más la MAC y no cambia tras reenchufar.

**P: ¿Cómo se comporta la AWUS036EACS en modo monitor y en inyección de paquetes?**
El modo monitor es estable en 2,4G y 5G, con la mayoría de los canales llenos a 300 tramas; `aireplay-ng --test` da 30/30 (100 %) en ambas bandas. Antes de inyectar en 5G hay que hacer `iw reg set US` para levantar la restricción de TW sobre la TX.

**P: ¿Puede la AWUS036EACS capturar un handshake WPA (paquetes de handshake)?**
Sí. Prueba de extremo a extremo con un AP propio y un iPhone 7 Plus propio: el deauth recibe 79 ACKs, se captura el M1–M4 completo y `hcxpcapngtool --all` genera el .22000 (784 bytes, 2 pares EAPOL). Solo en redes propias o autorizadas.

**P: ¿Qué hago si tras conectar la AWUS036EACS lsusb la ve pero no aparece la interfaz de red wlx?**
Es la condición de carrera en el probe de un dispositivo combinado BT+Wi-Fi: el Bluetooth ya está vinculado a btusb y el rtw88_8821cu del Wi-Fi se queda atascado. En la prueba, recargar el módulo o hacer bind manualmente no suele funcionar; la solución fiable es desconectar la tarjeta y reenchufarla en otro puerto USB.

**P: ¿La AWUS036EACS admite mesh, IBSS o hcxdumptool?**
No. El active-monitor, IBSS, mesh y P2P del rtw88 devuelven -95 o el join no es válido; hcxdumptool 8.x solo arranca en 2.4 GHz (en 5 GHz falla el arm), use en su lugar airodump-ng + aireplay-ng. El VHT es solo de 80 MHz. Para mesh / IBSS, elija la AWUS036ACM / ACHM.

---

## 6. Lecturas adicionales

- [La prueba más completa de 2026: matriz total de modo monitor, inyección y AP de 9 adaptadores inalámbricos ALFA en ASUS GX10 (ARM64 / Ubuntu 24.04)](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/) (tabla general del Hub)
- [Auditoría inalámbrica en la era WPA3-SAE: prueba de la capacidad de captura de handshake de 9 tarjetas ALFA](/es/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- [Integrado en el kernel: habilitar los modos monitor y AP de los adaptadores ALFA con el controlador integrado en Ubuntu 24.04 + kernel 6.17](/es/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- También tarjeta USB ac de rtw88 → [Informe de prueba de tarjeta individual AWUS036ACS (RTL8811AU)](/es/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*Unidad de pruebas: Yopitek (distribuidor de ALFA Network en Taiwán) — https://www.yupitek.com*
