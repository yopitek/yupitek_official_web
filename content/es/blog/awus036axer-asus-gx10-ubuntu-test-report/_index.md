---
title: "Informe de pruebas de la AWUS036AXER: la tarjeta Wi-Fi 6 con mejor recepción en ASUS GX10 + Ubuntu 24.04 (ARM64)"
slug: awus036axer-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axer-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036axer-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036axer
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - ubuntu-24-04
  - kernel-6-17
  - arm64
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
description: "AWUS036AXER en ASUS GX10/Ubuntu 24.04 ARM64 con controlador integrado en el kernel (rtw89_8852bu): el modo monitor captó 63 AP + 12 clientes en 60 s, inyección al 73 % (2,4G), y el AP 5G VHT80 y WPA3 pasaron sin problemas."
faq:
  - question: "¿La AWUS036AXER necesita instalar controladores aparte en Ubuntu 24.04 o Kali?"
    answer: "En Ubuntu 24.04 (ARM64, kernel 6.17.0-1014-nvidia) no: el controlador integrado rtw89_8852bu la reconoce nada más conectarla, sin compilar y sin DKMS (firmware rtw8852b_fw 0.29.29.5). La plataforma de este artículo es Ubuntu, no la distribución Kali; no probamos Kali como tal. Las herramientas habituales de Kali —airmon-ng, kismet, bettercap, wifite, Wireshark— sí funcionan en esta plataforma. Con un kernel más antiguo no se garantiza que esté integrado, así que confirme antes la versión."
  - question: "¿La AWUS036AXER admite modo monitor? ¿Qué tal es su recepción?"
    answer: "Sí, entra en modo monitor tanto en 2,4 GHz como en 5 GHz. En nuestra oficina hicimos un escaneo por salto de canal de 60 s con airodump-ng y captamos 63 AP y 12 clientes: es la tarjeta con mejor recepción de las nueve que probamos en la misma sesión. La AWUS036AX, con el mismo chip, dio 14 AP + 4 clientes en otra prueba (dos mediciones no simultáneas, solo a título orientativo)."
  - question: "¿La AWUS036AXER puede hacer inyección de paquetes (packet injection)?"
    answer: "Sí. En 2,4 GHz, aireplay-ng --test dio una tasa de respuesta del 73 % (22/30) y mostró Injection is working!; en 5 GHz también pasó la autoprueba AP por AP. En nuestra propia red y con nuestros propios dispositivos completamos la captura del handshake y la exportación a .22000. Si busca acercarse al 100 % en ambas bandas, en esta plataforma las AWUS036EACS, ACH y ACS resultaron más estables. Solo en redes propias o autorizadas."
  - question: "¿En qué se diferencian la AWUS036AXER y la AWUS036AX?"
    answer: "Ambas usan el Realtek RTL8832BU y el mismo rtw89_8852bu, y en esta plataforma su soporte de modos y su comportamiento de inyección son idénticos; la diferencia está en el ajuste de la antena y la ganancia, que marcan la recepción (AXER: 63 AP + 12 clientes en 60 s; AX: 14 AP + 4 clientes). Las dos llevan antena integrada, sin RP-SMA; para las especificaciones de antena, consulte la página del producto."
  - question: "¿La AWUS036AXER puede funcionar como AP o abrir WPA3? ¿Qué modos no admite?"
    answer: "Sí. Tanto en 2,4 GHz 802.11n como en 5 GHz VHT80 (VHT-NSS2, 351 Mbit) el iPhone se conectó y quedó authorized; con WPA3-SAE y sae_pwe=0 logramos conectar un iPhone 15 Pro (en 2,4 GHz; WPA3 en 5 GHz no se probó); la concurrencia STA+AP también funciona. Pero rtw89_8852bu no admite active monitor, IBSS ni mesh."
draft: false
---

{{< tldr >}}La AWUS036AXER funciona nada más conectarla en ASUS GX10/Ubuntu 24.04 ARM64 (rtw89_8852bu integrado); en modo monitor captó 63 AP + 12 clientes en 60 s, la inyección en 2,4 GHz llegó al 73 %, y tanto el AP como WPA3 pasaron; no admite active monitor, IBSS ni mesh.{{< /tldr >}}

> Este artículo recoge pruebas prácticas de compatibilidad y capacidades que Yopitek (distribuidor de ALFA en Taiwán) realizó sobre su propio equipo.
> Plataforma de prueba: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. El entorno de prueba fue la Wi-Fi propia de la oficina (SSID `YUPITEK`), frente a nuestro teléfono de prueba iPhone 7 Plus (para WPA3 se probó además un iPhone 15 Pro).
> ⚠️ **Uso legal**: el modo monitor y la inyección solo en redes y dispositivos propios o autorizados; en modo AP, respete la normativa de radio local. Este artículo se centra en las capacidades de la tarjeta, su compatibilidad, su configuración y la selección de modelo, y no aborda ninguna operación de ataque contra redes de terceros.

---

## 1. Esta tarjeta y la plataforma de prueba

La AWUS036AXER es una tarjeta USB Wi-Fi 6 (802.11ax) 2x2 de ALFA, basada en el chip Realtek RTL8832BU (sin Bluetooth). Comparte **el mismo chip y el mismo controlador** (`rtw89_8852bu`) con la AWUS036AX de la misma marca, y en esta plataforma su soporte de modos y su comportamiento son idénticos; la verdadera diferencia entre ambas está en el **ajuste de la antena y la ganancia**, no en que una sea externa y otra interna: la AXER usa un **diseño de antena integrada (Nano), sin RP-SMA**, y apura al máximo la recepción a base de chip y ajuste de RF. Conviene retener la conclusión central de este artículo: de las nueve tarjetas ALFA que comparamos en la misma sesión, la AXER es **la de mejor recepción**.

La plataforma de prueba es un ASUS GX10, con el superchip NVIDIA GB10 y 128 GB de memoria unificada, sistema operativo Ubuntu 24.04 LTS, arquitectura ARM64 (aarch64) y kernel `6.17.0-1014-nvidia`. Todos los resultados se obtuvieron el 2026-11-18 en esta misma máquina real; el dispositivo de prueba fue nuestro iPhone 7 Plus (para WPA3 se probó además un iPhone 15 Pro) y la red de prueba fue la Wi-Fi propia de la oficina. Para la validación de un distribuidor, ARM64 con un kernel reciente es una combinación relativamente exigente; en el apartado 2 explicamos por qué esta generación resulta, en cambio, más cómoda.

Un apunte sobre especificaciones: la AXER es una tarjeta Wi-Fi 6 2x2 (dos flujos espaciales), capaz de transmitir y recibir dos flujos a la vez, lo que se corresponde con el VHT-NSS2 que negoció en las pruebas de AP en 5 GHz más adelante. Pero lo que la hizo ganar en esta ronda fue el diseño de la antena y el ajuste de RF, no el número de flujos (la AX también es 2x2). Como el chip, el controlador y la plataforma son todos idénticos, el ajuste de la antena es prácticamente la única variable, de modo que la diferencia de recepción entre la AXER y la AX puede atribuirse limpiamente al diseño de la antena integrada y al ajuste de ganancia.

---

## 2. Hardware y controlador (antena integrada, sin instalar controladores)

En el kernel 6.17 de Ubuntu 24.04, la AWUS036AXER funciona **nada más conectarla, sin compilar y sin DKMS**. El controlador `rtw89_8852bu` ya es un módulo integrado en el kernel y el firmware es `rtw8852b_fw` (versión 0.29.29.5), que se carga al arrancar: no hace falta descargar ningún proyecto out-of-tree de GitHub ni atarse a DKMS. Para entornos de distribución y formación que requieren mantenimiento a largo plazo y sobreviven a varias actualizaciones de kernel, eliminar el paso de compilar el controlador equivale a eliminar uno de los puntos de fallo más habituales.

El contraste con el camino antiguo lo deja más claro: antes, chips USB de Realtek como este rara vez llegaban al kernel mainline, y el usuario tenía que descargar un proyecto out-of-tree de GitHub (por ejemplo `morrownr/USB-WiFi`) y compilarlo con DKMS contra el kernel actual, recompilando en cada actualización de kernel; si la compilación fallaba, la tarjeta sencillamente desaparecía. Desde que rtw89 se integró oficialmente en el kernel, todos esos pasos pueden omitirse por completo en 6.17, y el mismo procedimiento se reutiliza en varias tarjetas que comparten controlador.

Primero confirme que la tarjeta se reconoce correctamente:

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
# Bus 00x Device 00x: ID 0bda:b832 Realtek Semiconductor Corp. 802.11ac WLAN Adapter
```

El USB ID en modo WLAN normal es `0bda:b832`. Si ve `0bda:1a2b`, significa que la tarjeta sigue en «modo CD-ROM» (CD-ROM mode); ejecute una vez `sudo usb_modeswitch -v 0bda -p 1a2b -K` para pasarla a modo WLAN. En nuestra unidad de prueba, esta tarjeta se enumeró directamente en modo WLAN y no nos topamos con el modo CD-ROM.

El nombre de la interfaz usa la convención `wlx` + MAC (por ejemplo `wlxAABBCCDDEEFF`), que no cambia en ninguna máquina donde se conecte, lo cual facilita fijar el enlace en los scripts. Para consultar qué modos admite esta tarjeta:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Los modos reportados en la prueba fueron managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO. No hay IBSS, ni mesh, ni active monitor: es una limitación nativa del controlador rtw89, que explicamos con honestidad en el apartado 4, para que no se interprete mal al elegir modelo.

En cuanto a la antena: la AXER usa un diseño de antena integrada (Nano), sin RP-SMA, y frente a la AX con el mismo chip la diferencia está en el ajuste de la antena y la ganancia, que en la práctica se refleja directamente en la calidad de recepción. Los datos de monitor del siguiente apartado lo dejan claro.

---

## 3. Capacidades probadas

Primero resumimos en una tabla las tres capacidades centrales (Monitor / Inyección / AP) y el resultado de WPA3; los detalles se desarrollan punto por punto a continuación:

| Capacidad | 2,4 GHz | 5 GHz | Claves de la prueba |
|---|---|---|---|
| **Monitor (escucha)** | ✅ fuerte | ✅ fuerte | El escaneo por salto de canal captó **63 AP + 12 clientes**, la mejor recepción de las nueve tarjetas |
| **Inyección** | ✅ 73% | ✅ funciona | 2,4G `22/30 73%`; 5G `Injection is working!` |
| **AP (punto de acceso)** | ✅ 802.11n | ✅ VHT 80 MHz | El iPhone se conecta; 5G VHT-NSS2, 351 Mbit |
| **WPA3-SAE** | ✅ | No probado | Del lado del AP, el iPhone 15 Pro se conecta (`sae_pwe=0`); probado solo en 2.4 GHz |
| **Captura de handshake WPA** | ✅ de extremo a extremo | — | Red propia + dispositivo propio, 4-way (M1–M4) → `.22000` |

### 3-1. Monitor (lo destacado de este artículo: la mejor recepción)

Pasar a monitor sigue el flujo estándar de `iw`: primero devuelva la interfaz a su propio control (`nmcli dev set $IF managed no`), bájela, fije el tipo monitor, súbala y ponga el canal:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36        # 5 GHz; para 2,4 GHz use channel 6
sudo timeout 8 tcpdump -l -i $IF -nn -e -c 200
```

Tanto en 2,4 GHz como en 5 GHz se llenaron 100 frames en menos de 6 segundos. Lo que de verdad marca la diferencia es el escaneo por salto de canal: `sudo airodump-ng --band abg $IF` durante 60 segundos **captó 63 AP más 12 clientes**. Es la tarjeta que atrapó más objetivos de las nueve de esta ronda, un reflejo directo de la ventaja de recepción que aportan el diseño de antena integrada y el ajuste de RF. Para inventario en campo (site survey), escucha a larga distancia o entornos con señal débil, esta capacidad de recepción es el valor central de la AXER.

### 3-2. Inyección

La inyección se valida con el modo de autoprueba de aireplay-ng, que mide la capacidad de la propia tarjeta, no un ataque hacia el exterior:

```bash
sudo iw dev $IF set channel 6
sudo aireplay-ng --test $IF
# Found 21 APs
# 22/30:  73%
# Injection is working!
```

La tasa de respuesta en 2,4 GHz fue del 73 % (22/30), que se considera funcional. En 5 GHz, la autoprueba AP por AP también reportó `Injection is working!`. Una regla general de la plataforma: **antes de transmitir/inyectar en 5 GHz, ejecute `iw reg set US` para desbloquear la potencia de TX, y al terminar recuerde volver con `iw reg set TW` a la banda de la normativa de Taiwán**.

### 3-3. Punto de acceso (AP) (2,4 GHz 802.11n, 5 GHz VHT 80 MHz)

La AXER puede levantar un AP con hostapd en ambas bandas. En 2,4 GHz, con `hw_mode=g` + `ieee80211n=1` levanta un punto de acceso 802.11n; el iPhone 7 Plus se conectó negociando MCS 15 y quedó authorized. En 5 GHz, con `hw_mode=a` + `ieee80211ac=1` + `vht_oper_chwidth=1` levanta un punto de acceso VHT 80 MHz; el iPhone 7 Plus se conectó negociando **VHT-NSS2, 80 MHz, 351 Mbit, authorized**. El requisito previo para levantar el AP es `sudo nmcli dev set $IF managed no`, y la `wpa_passphrase` debe tener al menos 8 caracteres; de lo contrario, hostapd devuelve `invalid WPA passphrase length`.

### 3-4. WPA3-SAE y captura de handshake

Para WPA3-SAE, del lado del AP se configuran `wpa_key_mgmt=SAE`, `ieee80211w=2` y `sae_pwe=0`; en la prueba, el iPhone 15 Pro se conectó. **`sae_pwe` es el campo minado de compatibilidad de este lote de tarjetas ALFA**: algunos dispositivos no conectan con `sae_pwe=2` (Hash-to-Element), y poner `sae_pwe=0` recupera la compatibilidad con iPhone más antiguos.

La capacidad de handshake se validó de extremo a extremo sobre la **Wi-Fi propia de la oficina (YUPITEK) + nuestro propio dispositivo de prueba**: capturamos el 4-way completo (M1/M2/M3/M4) y luego, con `hcxpcapngtool`, lo exportamos al formato `.22000` que hashcat puede leer. Aquí conviene señalar un fenómeno común a la plataforma GX10: **`hcxdumptool` da `failed to arm` con todas las tarjetas USB en esta plataforma salvo el AWUS036EACS en 2.4 GHz** (conflicto de enumeración de la tarjeta de red integrada triple banda del GX10, sumado a que el controlador carece de active monitor), así que el flujo de handshake se desvía a la suite aircrack-ng (airodump-ng + aireplay-ng). La capacidad de inyección de la AXER es suficiente por esta vía.

---

## 4. Funciones avanzadas y limitaciones honestas

**VIF (STA + AP en concurrencia) ✅**: la AXER puede, a la vez, actuar como station conectada a la Wi-Fi ascendente y abrir una interfaz virtual (VIF) de AP. En la prueba, la interfaz principal conectada a YUPITEK y una VIF de AP en ch36 VHT80 funcionaron en concurrencia, con un ping de 3,5 ms del lado STA; adecuado para escenarios de «conectado a la red y abriendo un punto de acceso al mismo tiempo».

**Wi-Fi Direct (P2P) no probado (⬜)**: el controlador declara P2P-client / P2P-GO, pero validarlo por completo requiere un segundo equipo para el emparejamiento, así que en esta ronda lo omitimos y no lo contamos como capacidad verificada. Los puntos de este tipo —«el controlador declara soporte, pero no se ha ejecutado sobre hardware real»— los marcamos siempre honestamente como no probados, sin inflarlos haciéndolos pasar por aprobados.

**Los tres modos no admitidos (N/A)**: el controlador `rtw89_8852bu` **no ofrece active monitor, Ad-hoc (IBSS) ni Mesh (802.11s)**. `iw dev $IF set type ibss` o `mp` fallan directamente; es una limitación de la capa del controlador, imposible de sortear por configuración. Si el uso es experimentar con mesh o IBSS, habría que mirar la serie MediaTek mt76 (como la AWUS036ACM / ACHM).

**Notas comunes a la plataforma:**

- Nunca ejecute `airmon-ng check kill`: apaga NetworkManager y deja al GX10 sin conexión al exterior. Opere solo la interfaz `wlx*` y no toque la tarjeta de red integrada que da la conexión a Internet.
- Si tras alternar varias veces entre monitor/AP deja de captar nada de repente (RX stall), basta con **desconectar y volver a conectar** la tarjeta para recuperarla (reenumeración USB; el nombre de la interfaz lo determina la MAC y no cambia).
- En plataformas ARM64, aircrack-ng debe compilarse desde el código fuente; use la versión git de wifite para sortear los conflictos de dependencias de apt.

**Compatibilidad con herramientas de Kali**: airmon-ng, kismet 2026.10, bettercap 2.32, wifite (git) y Wireshark / tshark 4.2 pueden usar la AXER normalmente como fuente de datos o interfaz de gestión.

---

## 5. Escenarios de uso y recomendaciones de selección

En una frase: **la AXER es una tarjeta Wi-Fi 6 orientada a la recepción**. Comparte chip con la AX y tiene las mismas funciones; la diferencia es la ventaja de recepción que aportan el ajuste de antena y la ganancia, así que la lógica de selección es muy clara:

| Su necesidad | ¿La AXER es la primera opción? | Explicación |
|---|---|---|
| Máxima recepción / monitor a larga distancia / inventario en campo | ✅ **Primera opción** | El escaneo por salto de canal captó 63 AP + 12 clientes, la mejor de las nueve; se puede complementar con la AWUS036ACH (doble antena de alta ganancia) |
| Wi-Fi 6 + punto de acceso | ✅ Adecuada | 2x2, 5G VHT80; al mismo nivel que la AWUS036AX |
| Inyección + handshake de extremo a extremo | 🟡 Funcional | 2,4G al 73 %, funcional; si busca acercarse al 100 % en ambas bandas, las AWUS036EACS / ACH / ACS son más estables |
| Experimentos de mesh / IBSS | ❌ No apta | rtw89 no lo admite; use la AWUS036ACM / ACHM (mt76) |

Escenario típico de despliegue: usar la AXER como **nodo remoto de monitorización inalámbrica**, colocado en puntos con señal más débil o más alejados, aprovechando la ventaja de recepción de su antena integrada para captar lo más completos posible los AP / clientes del lugar, y luego centralizar los resultados del escaneo en un host central para revisarlos de forma unificada. Como la antena es integrada (Nano), sin RP-SMA, no se puede cambiar; cuando se necesite más ganancia o más directividad, basta con complementarla con la AWUS036ACH de doble antena y alta ganancia.

A la inversa: si el uso es solo AP o conexión general y no se necesita nada de inyección, las MediaTek AWUS036AXM / AXML también sirven; pero **en cuanto entre en juego la inyección o el handshake, no elija las AXM / AXML**, porque en esta plataforma la inyección falla (causa principal: una regresión de mac80211 chanctx desde el kernel 6.16, a lo que se suma un firmware que bloquea la velocidad de inyección en 1/6 Mbps; no es una limitación del chip en sí). La AXER es justo lo contrario: la inyección funciona y, además, tiene la mejor recepción.

Si quiere ver de una vez la matriz completa de las nueve tarjetas y su comparativa cruzada, vuelva a la página de evaluación global → [`/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

---

## Preguntas frecuentes (FAQ)

**Q1. ¿La AWUS036AXER necesita instalar controladores aparte en Ubuntu 24.04 o Kali?**
En Ubuntu 24.04 (ARM64, kernel 6.17.0-1014-nvidia) no: el controlador integrado `rtw89_8852bu` la reconoce nada más conectarla, sin compilar y sin DKMS (firmware `rtw8852b_fw` 0.29.29.5). La plataforma de este artículo es Ubuntu, no la distribución Kali; no probamos Kali como tal. Las herramientas habituales de Kali —airmon-ng, kismet, bettercap, wifite, Wireshark— sí funcionan en esta plataforma. Con un kernel más antiguo no se garantiza que esté integrado, así que confirme antes la versión.

**Q2. ¿La AWUS036AXER admite modo monitor? ¿Qué tal es su recepción?**
Sí, entra en modo monitor tanto en 2,4 GHz como en 5 GHz. En nuestra oficina hicimos un escaneo por salto de canal de 60 s con airodump-ng y captamos 63 AP y 12 clientes: es la tarjeta con mejor recepción de las nueve que probamos en la misma sesión. La AWUS036AX, con el mismo chip, dio 14 AP + 4 clientes en otra prueba (dos mediciones no simultáneas, solo a título orientativo).

**Q3. ¿La AWUS036AXER puede hacer inyección de paquetes (packet injection)?**
Sí. En 2,4 GHz, `aireplay-ng --test` dio una tasa de respuesta del 73 % (22/30) y mostró `Injection is working!`; en 5 GHz también pasó la autoprueba AP por AP. En nuestra propia red y con nuestros propios dispositivos completamos la captura del handshake y la exportación a `.22000`. Si busca acercarse al 100 % en ambas bandas, en esta plataforma las AWUS036EACS, ACH y ACS resultaron más estables. Solo en redes propias o autorizadas.

**Q4. ¿En qué se diferencian la AWUS036AXER y la AWUS036AX?**
Ambas usan el Realtek RTL8832BU y el mismo `rtw89_8852bu`, y en esta plataforma su soporte de modos y su comportamiento de inyección son idénticos; la diferencia está en la recepción que marcan el ajuste de antena y la ganancia (AXER: 63 AP + 12 clientes en 60 s; AX: 14 AP + 4 clientes). Las dos llevan antena integrada, sin RP-SMA; para las especificaciones de antena, consulte la página del producto.

**Q5. ¿La AWUS036AXER puede funcionar como AP o abrir WPA3? ¿Qué modos no admite?**
Sí. Tanto en 2,4 GHz 802.11n como en 5 GHz VHT80 (VHT-NSS2, 351 Mbit) el iPhone se conectó y quedó authorized; con WPA3-SAE y `sae_pwe=0` logramos conectar un iPhone 15 Pro (en 2,4 GHz; WPA3 en 5 GHz no se probó); la concurrencia STA+AP también funciona. Pero `rtw89_8852bu` no admite active monitor, IBSS ni mesh.

---

## 6. Lecturas adicionales

- Matriz global de las nueve tarjetas ALFA y tabla de selección (comparativa completa de Monitor / Inyección / AP) → `/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`
- Prueba práctica de la AWUS036AX con el mismo chip (distinto ajuste de antena) → `/es/blog/awus036ax-asus-gx10-ubuntu-test-report/`
- Sin instalar controladores: activar los modos Monitor y AP con el controlador integrado en el kernel → `/es/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`
- Capacidad de captura de handshake en la era WPA3-SAE y compatibilidad de `sae_pwe` → `/es/blog/alfa-wpa3-sae-handshake-capability-arm64/`

<!-- Los enlaces internos de Lecturas adicionales se completarán con las URL hreflang definitivas una vez cerrada la edición; los de arriba son slugs placeholder en es. -->

---

*Unidad de prueba: Yopitek (distribuidor de ALFA) — https://www.yupitek.com | Plataforma de prueba: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Dispositivo de prueba: Apple iPhone 7 Plus (para WPA3 se probó además un iPhone 15 Pro)*
