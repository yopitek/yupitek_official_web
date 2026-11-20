---
title: "Sin instalar controladores: activar los modos Monitor y AP de los adaptadores ALFA con el controlador integrado en Ubuntu 24.04 + kernel 6.17 (pruebas de rtw88 / rtw89 / mt76)"
slug: alfa-inkernel-driver-monitor-ap-ubuntu-2404
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404.webp"
author: "benny-lai"
tags:
  - alfa-network
  - ubuntu-24-04
  - kernel-6-17
  - in-kernel-driver
  - rtw88
  - rtw89
  - mt76
  - monitor-mode
  - hostapd
  - ap-mode
  - linux-wifi
description: "Tutorial sin instalar controladores en Ubuntu 24.04 / kernel 6.17: activar los modos Monitor y AP de los adaptadores ALFA con los controladores integrados rtw88 / rtw89 / mt76, con los ajustes de compatibilidad del punto de acceso WPA3 y las consideraciones sobre la cadena de herramientas de Kali."
faq:
  - question: "¿Cómo hago que un adaptador ALFA entre en modo monitor en Ubuntu 24.04?"
    answer: "En kernel 6.17 o superior, basta con entregar la interfaz desde la gestión de NetworkManager y cambiarla al modo de interfaz monitor, sin instalar controladores de terceros; las tres familias de controladores probadas en este artículo (rtw88 / rtw89 / mt76) siguen un flujo idéntico, véanse los comandos detallados en los pasos del texto."
  - question: "¿Por qué en Ubuntu no hace falta instalar controladores aparte para los adaptadores ALFA?"
    answer: "Porque los rtw88/rtw89 de Realtek y el mt76 de MediaTek fueron incorporando estos chips USB al soporte integrado del mainline kernel (la versión mínima varía según la tarjeta, de 4.19 a 6.17; en Ubuntu 24.04, AX y AXER requieren kernel 6.17 o superior, por ejemplo el HWE de 24.04.4); con el kernel 6.17 (probado en el GX10) las 9 tarjetas de este artículo vienen integradas y se reconocen al conectarlas, sin compilar y sin DKMS."
  - question: "Si monto un punto de acceso WPA3 con un adaptador ALFA y un iPhone antiguo no conecta, ¿qué hago?"
    answer: "En las pruebas se detectaron dos causas comunes: una, que el sae_pwe de hostapd debe fijarse en 0 en lugar de 2 para ser compatible con los iPhone antiguos; dos, que conservar el ajuste 802.11n puede hacer que los dispositivos antiguos fallen la asociación, por lo que, si prioriza la compatibilidad, se recomienda desactivar 802.11n."
  - question: "¿Qué familia de controlador —rtw88, rtw89 o mt76— admite mesh o IBSS?"
    answer: "En las pruebas, la familia mt76 (como el AWUS036ACM / ACHM) puede crear mesh (802.11s) e IBSS en un solo equipo; el rtw88 de Realtek puede hacer join de IBSS en un solo equipo (según lo probado con el ACH) pero no admite mesh, y el rtw89 ni siquiera declara soporte de IBSS."
draft: false
---

> Este artículo es un tutorial estándar de configuración de red en Linux, que muestra cómo activar los modos Monitor (escucha) y AP (punto de acceso) de los adaptadores WiFi ALFA usando el **controlador integrado (in-kernel)** en un kernel reciente.
> Plataforma de pruebas: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Todos los datos son un extracto de las pruebas de compatibilidad del producto realizadas por Yupitek sobre equipos propios y el WiFi propio de la oficina (SSID `YUPITEK`).
> ⚠️ **Uso legal**: el modo Monitor se limita a escuchar redes propias o autorizadas; para el modo AP, cumpla la normativa de radio local. Este artículo no aborda ninguna operación de ataque contra redes de terceros.

---

## Resumen (TL;DR)

En el ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17), los 9 adaptadores Wi-Fi USB ALFA probados por Yupitek (distribuidor de ALFA Network en Taiwán) funcionan con controladores in-kernel (`rtw88` / `rtw89` / `mt76`) sin instalar controladores, activan los modos Monitor y AP con el mismo flujo y permiten que el iPhone 7 Plus / 15 Pro se conecte con normalidad en AP de 2.4G y 5G; el kernel mínimo va de 4.19 a 6.17 según la tarjeta.

- **Sin instalar controladores en kernels recientes**: los `rtw88` / `rtw89` de Realtek y el `mt76` de MediaTek ya incorporan estos chips USB de ALFA al soporte integrado en el kernel; con el kernel 6.17 (probado en el GX10) las 9 tarjetas vienen integradas, aunque la versión mínima varía según la tarjeta, funcionan nada más conectarlos, sin compilar y sin DKMS.
- **El flujo de Monitor y AP es idéntico en las tres familias**: devolver a NetworkManager → `iw` para cambiar a monitor / `hostapd` para levantar el AP.
- **Dos trampas de compatibilidad**: al abrir el AP conviene desactivar 802.11n (`ieee80211n=0`) y usar `sae_pwe=0` en WPA3-SAE, o los iPhone antiguos no conectarán.
- **Niveles de los modos avanzados**: mesh solo en `mt76`; IBSS en un solo equipo lo pueden hacer `mt76` y `rtw88` (ACH), `rtw89` no lo declara.
- **Regla de oro de la plataforma**: nunca ejecute `airmon-ng check kill` (dejaría al GX10 sin red); opere solo sobre las interfaces `wlx*` externas.

## 1. Por qué «sin instalar controladores» es la clave de esta generación

Antes, el obstáculo más común al usar adaptadores WiFi USB como los de ALFA en Linux era el controlador. Chips como el RTL8812AU o el MT7610U no estaban en el mainline kernel en sus inicios, y el usuario tenía que descargar un proyecto out-of-tree de GitHub (por ejemplo, `morrownr/USB-WiFi` o `aircrack-ng/rtl8812au`) y compilarlo con DKMS vinculándolo a la versión de kernel en uso. Cada actualización del kernel obligaba a recompilar con DKMS; y si la compilación fallaba, el adaptador desaparecía sin más. Para entornos de validación de distribuidor o de enseñanza que necesitan un mantenimiento estable, ese era un punto doloroso permanente.

Con los mainline kernel recientes la situación dio un giro: las tres grandes familias de controladores —`rtw88` y `rtw89` de Realtek y `mt76` de MediaTek— fueron incorporando oficialmente estos chips USB al soporte integrado en el kernel. La versión mínima varía según la tarjeta (vea la columna "Kernel mínimo" más abajo); con el kernel 6.17 (probado en el GX10) las nueve tarjetas probadas en este artículo vienen integradas: **se reconocen al conectarlas, sin compilar y sin DKMS**. Más importante aún, los dos proyectos out-of-tree más usados (los rtl8812au de morrownr y de aircrack-ng) ahora redirigen hacia este controlador integrado, y los reportes de bugs se unifican en `lwfinger/rtw88`. Dicho de otro modo, el paso de compilar el controlador a mano ya se puede omitir directamente en los kernels recientes.

La comunidad de `lwfinger/rtw88` sigue con un mantenimiento activo y envía correcciones aguas arriba de forma continua, por lo que la estabilidad del controlador integrado se actualiza junto con el kernel: el usuario ya no tiene que mantener su propia rama ni queda bloqueado por un fallo de compilación de DKMS en cada actualización. Para entornos de validación de distribuidor y de enseñanza, un mismo conjunto de pasos de operación es reutilizable en varias tarjetas y a través de varias actualizaciones del kernel, con un coste de mantenimiento claramente menor; esta es la razón por la que este artículo pone el foco en «sin instalar controladores».

Los chips cubiertos por las pruebas de este artículo y su módulo de controlador integrado correspondiente son los siguientes:

| Familia de chip | Modelo de chip | Módulo de controlador integrado | Kernel mínimo | Generación / Flujos | Tarjeta representativa |
|---|---|---|---|---|---|
| **MediaTek mt76** | MT7612U | `mt76x2u` | 4.19 | Wi-Fi 5 / 2T2R | AWUS036ACM |
| **MediaTek mt76** | MT7610U | `mt76x0u` | 4.19 | Wi-Fi 5 / 1T1R | AWUS036ACHM |
| **MediaTek mt76** | MT7921AU | `mt7921u` | 5.18 | Wi-Fi 6 / 2x2 | AWUS036AXM / AXML |
| **Realtek rtw88** | RTL8812AU | `rtw88_8812au` | 6.13 | Wi-Fi 5 / 2T2R | AWUS036ACH |
| **Realtek rtw88** | RTL8811AU | `rtw88_8821au` | 6.13 | Wi-Fi 5 / 1x1 | AWUS036ACS |
| **Realtek rtw88** | RTL8821CU | `rtw88_8821cu` | 6.2 | Wi-Fi 5 / 1x1 (+BT) | AWUS036EACS |
| **Realtek rtw89** | RTL8832BU | `rtw89_8852bu` | 6.17 | Wi-Fi 6 / 2x2 | AWUS036AX / AXER |

> Si el kernel de su sistema está por debajo de la versión mínima de su tarjeta (vea la tabla anterior), entonces sí tendrá que seguir el camino antiguo: instalar un controlador out-of-tree con DKMS (`lwfinger/rtw88` para las tarjetas rtw88). Por ejemplo, en Ubuntu 24.04: el kernel GA 6.8 ya integra los controladores de ACM, ACHM, AXM, AXML y EACS; el HWE 6.14 añade ACH y ACS. AX y AXER requieren kernel 6.17 o superior (por ejemplo, el HWE de 24.04.4). Este artículo se basa en el kernel 6.17 del GX10.

---

## 2. Confirmar que el controlador está cargado y vinculado

Antes de cambiar a cualquier modo, confirme primero que la tarjeta se reconoce correctamente, que el controlador está vinculado y que el nombre de interfaz se ha generado. Tomando como ejemplo el AWUS036ACH de Realtek (`rtw88_8812au`), los cuatro pasos de comprobación son los siguientes.

**Paso uno: confirmar que el dispositivo USB se enumera.** Use `lsusb` para encontrar el USB ID (Realtek suele ser `0bda:xxxx`, MediaTek suele ser `0e8d:xxxx`):

```bash
lsusb | grep 0bda:8812
# Bus 004 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

**Paso dos: confirmar la vinculación del controlador y la velocidad USB.** `lsusb -t` permite ver a la vez el driver vinculado y la velocidad de conexión (`5000M` indica USB 3.0):

```bash
lsusb -t | grep rtw88_8812au
# |__ Port 001: Dev 002, If 0, Class=Vendor Specific Class, Driver=rtw88_8812au, 5000M
```

Para las tarjetas MediaTek se puede usar `dmesg` para observar los mensajes de inicialización del controlador y confirmar a la vez el renombrado de la interfaz:

```bash
sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0
```

**Paso tres: obtener el nombre de la interfaz.** Ubuntu usa nombres predecibles (predictable naming), y las tarjetas externas ALFA son siempre `wlx` seguido de la dirección MAC. Este nombre lo determina la MAC y **no cambia tras desconectar y reconectar**, lo que facilita el scripting. La tarjeta de red integrada de salida a internet tiene otro nombre (en el GX10 es `wlP9s9`); distíngalos con cuidado:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cabca7f5
```

**Paso cuatro: consultar los modos de interfaz que el chip declara soportar.** Este paso determina qué modos se podrán usar después:

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

El rtw88 de Realtek (ACH) listará `IBSS / managed / AP / AP/VLAN / monitor`, pero **no** mesh ni P2P; el mt76 de MediaTek (ACHM) listará además `mesh point / P2P-client / P2P-GO`. Esta lista es la primera fuente directa de las diferencias de capacidad entre familias; véase la sección 5.

---

## 3. Activar el modo Monitor (2.4 GHz / 5 GHz)

El modo Monitor (escucha) hace que el adaptador no se asocie a ningún AP y reciba directamente las tramas 802.11 del aire; se usa a menudo para el diagnóstico de paquetes en la red propia, la inspección del espectro y la evaluación de cobertura de señal. El flujo de activación es idéntico en las tres familias; la diferencia está solo en las advertencias de estabilidad de cada familia (véanse las secciones 5 y 6).

**Pasos de activación comunes:**

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no      # se lo devolvemos a nuestra propia gestión para evitar que NetworkManager intervenga
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
iw dev $IF info | grep type
# type monitor
```

Ver `type monitor` significa que el cambio tuvo éxito. A continuación, especifique el canal a escuchar. En **2.4 GHz** se usa `set channel`:

```bash
sudo iw dev $IF set channel 6
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch6.pcap
tcpdump -r /tmp/mon-ch6.pcap | wc -l
```

En **5 GHz** especificar la frecuencia es menos propenso a errores (ch36 = 5180 MHz):

```bash
sudo iw dev $IF set freq 5180
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch36.pcap
tcpdump -r /tmp/mon-ch36.pcap | wc -l
```

**Resultado esperado (extracto de las pruebas):** el AWUS036ACH captó en ch1 / ch6 / ch11 respectivamente 92 / 214 / 71 tramas; en 5 GHz, el ch36 / ch149 / ch157 captó respectivamente 260 / 137 / 127 tramas, lo que indica que la escucha funciona con normalidad tanto en 2.4G como en 5G. El ACHM de MediaTek, con un escaneo por salto de canal de 120 segundos usando `airodump-ng --band abg`, pudo encontrar en la zona de ch1/5/6/36/149/157 unas 19 estaciones base y 14 clientes. Captar 0 paquetes en un canal suele significar solo que en ese momento no hay AP en ese canal, no que el adaptador esté averiado.

Tras cambiar al modo monitor, las herramientas estándar de diagnóstico más comunes funcionan directamente sobre la interfaz `wlx*`: `airmon-ng` sirve para listar el estado de las tarjetas y los controladores, `kismet` puede usarse como fuente de datos para capturar en tiempo real y generar un log `.kismet`, `Wireshark` y `tshark` se encargan de analizar los paquetes capturados y `bettercap` puede hacer inspección de canales. Estas herramientas se verificaron como funcionales en las tres familias y son muy útiles para inventariar el uso de canales y la cobertura de señal del entorno inalámbrico propio. Lo único a tener en cuenta es que `hcxdumptool` 8.x da `failed to arm` en esta plataforma con las tres familias, salvo el EACS en 2.4 GHz (el controlador integrado no ofrece active-monitor); si necesita una función similar, use `airodump-ng` junto con el paquete aircrack-ng.

> **Aviso sobre 5 GHz:** bajo el regdomain por defecto (`country 00`), muchos canales de 5 GHz son passive/no-IR; la escucha es posible, pero la transmisión activa está restringida. Si después va a hacer pruebas de 5 GHz dentro de un alcance autorizado, primero `sudo iw reg set US` para desbloquear y, al terminar, `sudo iw reg set TW` para restaurar. El `rtw88_8812au` de Realtek tiene además un fenómeno conocido de RX atascado en 5G (tras alternar modos repetidamente deja de recibir paquetes en 5G); cuando ocurra, desconecte y reconecte físicamente la tarjeta una vez y haga el 5G con prioridad.

---

## 4. Activar el modo AP / punto de acceso (2.4 GHz / 5 GHz)

El modo AP (punto de acceso) usa `hostapd` para convertir el adaptador en una estación base WiFi. El flujo es el mismo en las tres familias: primero entregar la interfaz desde NetworkManager y luego arrancar con un archivo de configuración de `hostapd`. A continuación, la configuración mínima común.

**4-1. 2.4 GHz (802.11g puro)**

Cree el archivo de configuración `/tmp/ap24.conf`:

```ini
interface=wlx00c0cabca7f5
driver=nl80211
ssid=ALFA-AP-24G
hw_mode=g
channel=6
country_code=TW
auth_algs=1
ieee80211n=0
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=<su contraseña, al menos 8 caracteres>
```

Arranque:

```bash
sudo nmcli dev set $IF managed no
sudo hostapd /tmp/ap24.conf
```

Cuando un cliente se conecta, `hostapd` emite en orden `authenticated` → `associated` → `AP-STA-CONNECTED` → `EAPOL-4WAY-HS-COMPLETED`; ver la última línea significa que el 4-way handshake se completó y la conexión tuvo éxito.

**4-2. 5 GHz (802.11a puro, ch36)**

Modifique la configuración anterior para 5 GHz:

```ini
ssid=ALFA-AP-5G
hw_mode=a
channel=36
```

Las tarjetas 2x2 (como el AX/AXER de rtw89 o el ACM/AXM de mt76) pueden añadir la configuración VHT80 para subir a un ancho de banda de 80 MHz; con antena única o cuando se busca compatibilidad, basta con mantener 20 MHz en «a» puro.

**4-3. Dos ajustes de compatibilidad clave**

1. **Al abrir el AP conviene desactivar 802.11n** (`ieee80211n=0`, usando g puro / a puro). En las pruebas, un cliente antiguo (iPhone 7 Plus) con `ieee80211n=1` conservado fallaba la asociación y mostraba en pantalla el error engañoso «contraseña incorrecta», cuando en realidad era `handle_assoc_cb: STA not found`; al quitar 802.11n conectaba a la primera.
2. **Para WPA3-SAE use `sae_pwe=0`** (hunting-and-pecking). Con `sae_pwe=2` (forzando H2E) el handshake de clave de los equipos antiguos falla. Ejemplo del bloque WPA3:

```ini
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
ieee80211w=2
sae_pwe=0
```

Estas dos trampas aparecen igual en las tarjetas Realtek y MediaTek; se trata de compatibilidad del cliente, no de diferencias de controlador. Las nueve tarjetas probadas en este artículo logran que el iPhone 7 Plus / 15 Pro conecte con normalidad bajo AP tanto en 2.4G como en 5G.

**4-4. Navegar y hacer de punto de acceso a la vez (STA + AP)**

La familia mt76 admite usar una sola tarjeta para conectarse al WiFi existente y, a la vez, crear otra VIF de AP como punto de acceso de retransmisión. En las pruebas, el ACHM, con la interfaz principal conectada a YUPITEK, abrió a la vez un punto de acceso de 5 GHz para que el iPhone conectara, con una descarga aún de 198 Mbit/s y un ping medio de 3,2 ms. Esta combinación debe cumplir tres condiciones: la VIF de AP debe usar una MAC distinta, el nombre de interfaz debe mantener el formato `wlx`, y todas las VIF deben estar en el mismo canal. En las tarjetas Realtek esta combinación no está garantizada por el phy (en rtw88, managed + monitor sí funciona, pero STA + AP no es estable); para montar un punto de acceso de retransmisión se recomienda elegir preferentemente la familia mt76.

---

## 5. Diferencias y limitaciones de las tres familias de chips

Los tres modos básicos —managed / monitor / AP— los admiten las tres familias con un comportamiento idéntico. Las diferencias están en los **modos de interfaz avanzados** (mesh, IBSS, active monitor, P2P): esto depende por completo de lo que declare el controlador y no tiene relación con el número de antenas de la tarjeta. A continuación, el resumen de las pruebas.

| Modo avanzado | MediaTek mt76 | Realtek rtw88 | Realtek rtw89 |
|---|---|---|---|
| Monitor (2.4G/5G) | ✅ | ✅ | ✅ |
| AP (hostapd) | ✅ | ✅ | ✅ |
| Ad-hoc / IBSS (en local) | 🟡 se puede crear en local | 🟡 se puede crear en local | ❌ el controlador no lo declara |
| Mesh (802.11s, en local) | 🟡 se puede crear en local | ❌ `-95` no compatible | ❌ el controlador no lo declara |
| Active monitor | 🟡 configurable | ❌ `-95` no compatible | N/A |
| Wi-Fi Direct (P2P) | requiere un segundo dispositivo | ❌ `-95` no compatible | N/A |

**MediaTek mt76 (ACM / ACHM / AXM / AXML)** es la familia más completa en modos avanzados. `iw phy info` ya declara `mesh point`, `IBSS` y `P2P-client/GO`. En las pruebas, en un solo equipo se logró `Joined IBSS`, `type mesh point` y la emisión del beacon correspondiente (el peer link con un segundo equipo no se verificó por falta de ese segundo equipo). Si su uso es un experimento de mesh o IBSS en un solo equipo, la familia mt76 es la primera opción. Hay que prestar especial atención al MT7921 de Wi-Fi 6 (AXM/AXML): aunque sus modos son completos y el AP es estable, en esta plataforma no puede hacer inyección de tramas (la causa principal es la regresión de chanctx de mac80211 del kernel stock 6.16+, no una limitación nativa del chip; aunque la comunidad logra que el mismo modelo funcione con controladores de git / parcheados, el firmware bloquea la tasa, ver morrownr/USB-WiFi #387, morrownr/mt76 #18), por lo que no es apto para pruebas avanzadas que requieran inyección.

**Realtek rtw88 (ACH / ACS / EACS)** admite `IBSS / managed / AP / AP/VLAN / monitor`. El IBSS se puede crear en un solo equipo (`Joined IBSS`, según lo probado con el ACH; el EACS lista el iftype pero en la práctica el join no funciona), pero **mesh (802.11s), active monitor y Wi-Fi Direct devuelven los tres en las pruebas `Operation not supported (-95)`**. Otra característica propia de rtw88 es la VIF: aunque el flag de `iw phy` dice «interface combinations are not supported», en las pruebas del ACH las dos interfaces managed + monitor pudieron estar up a la vez y la VIF de monitor captó 100 tramas, así que «navegar y capturar a la vez» es viable; no obstante, el phy no garantiza esta combinación, y para pruebas prolongadas con carga alta se recomienda la familia mt76.

**Realtek rtw89 (AX / AXER)** es la familia Wi-Fi 6 más reciente de este artículo; monitor y AP (incluido VHT80) rinden bien y la sensibilidad de recepción es fuerte. Pero en los modos avanzados, active monitor / mesh / IBSS / P2P no están declarados en la capa del controlador (N/A), así que para esos experimentos en un solo equipo use una tarjeta mt76. El posicionamiento de rtw89 es la escucha y el punto de acceso Wi-Fi 6 estables, no la plataforma de experimentación de modos de interfaz avanzados.

> La selección en una frase: **para mesh / IBSS en un solo equipo → mt76 (ACM / ACHM); para punto de acceso Wi-Fi 6 y recepción fuerte → rtw89 (AX / AXER); para uso general de doble banda y VIF → rtw88 (ACH).**

---

## 6. Consideraciones de seguridad de la plataforma (GX10 + Ubuntu ARM64)

En máquinas de tipo «la tarjeta de red integrada se encarga de la salida a internet y la tarjeta ALFA externa hace de banco de pruebas» como el GX10, los siguientes puntos son reglas de oro operativas: síganlas para no quedarse sin red.

1. **Nunca ejecute `airmon-ng check kill`.** Este comando apaga NetworkManager y, con ello, corta la conexión a internet del GX10. Este artículo usa en todo momento solo `iw` y `nmcli dev set <interfaz> managed no`, sin tocar `check kill`.
2. **Opere solo `wlx*`, nunca toque la `wlP9s9` integrada.** La `wlP9s9` es la línea principal de salida a internet del GX10; cualquier acción de down / cambio de modo solo puede aplicarse a la interfaz `wlx*` de ALFA, y antes de lanzar el comando confirme siempre el objetivo con `echo $IF`.
3. **Recupere el RX stall desconectando y reconectando.** Si tras alternar repetidamente monitor / AP no detecta nada, suele tratarse de un bloqueo de recepción del controlador (especialmente frecuente en el 5G de Realtek). El software no suele poder recuperarlo; **desconecte y reconecte físicamente** la tarjeta una vez: el USB se reenumera y el nombre de interfaz se mantiene, pues la MAC no cambia.
4. **Cambie de puerto USB con las tarjetas combo BT+WiFi.** En dispositivos combo de Bluetooth más Wi-Fi como el EACS o el AXML, al reconectar a veces el probe de WiFi se bloquea y no genera la interfaz `wlx`; cambiar de puerto USB suele normalizarlo.
5. **Fije el regdomain antes de transmitir en 5 GHz.** Bajo el `country 00` por defecto, el 5 GHz suele ser no-IR y la transmisión activa está prohibida. Antes de probar dentro de un alcance autorizado, `sudo iw reg set US` para desbloquear, y al terminar `sudo iw reg set TW` para restaurar.
6. **Cuidado con los paquetes en ARM64.** El GX10 es aarch64; `aircrack-ng` a menudo carece de wheel/paquete precompilado y debe compilarse desde el código fuente; para `wifite` se recomienda la versión de GitHub para esquivar el conflicto de dependencias de apt. Además, `hcxdumptool` 8.x da `failed to arm` en esta plataforma con las tres familias, salvo el EACS en 2.4 GHz (el controlador integrado no soporta active-monitor); para la captura de escucha, use `airodump-ng` junto con el paquete aircrack-ng.

**Restaurar el modo normal tras terminar las pruebas:**

```bash
sudo pkill hostapd 2>/dev/null
sudo ip link set $IF down
sudo iw dev $IF set type managed
sudo ip link set $IF up
sudo nmcli dev set $IF managed yes
iw dev $IF info | grep type      # esperado: type managed
```

---

## Preguntas frecuentes (FAQ)

**P: ¿Cómo hago que un adaptador ALFA entre en modo monitor en Ubuntu 24.04?**
R: En kernel 6.17 o superior, basta con entregar la interfaz desde la gestión de NetworkManager y cambiarla al modo de interfaz monitor, sin instalar controladores de terceros; las tres familias de controladores probadas en este artículo (rtw88 / rtw89 / mt76) siguen un flujo idéntico, véanse los comandos detallados en los pasos del texto.

**P: ¿Por qué en Ubuntu no hace falta instalar controladores aparte para los adaptadores ALFA?**
R: Porque los `rtw88`/`rtw89` de Realtek y el `mt76` de MediaTek fueron incorporando estos chips USB al soporte integrado del mainline kernel (la versión mínima varía según la tarjeta, de 4.19 a 6.17; en Ubuntu 24.04, AX y AXER requieren kernel 6.17 o superior, por ejemplo el HWE de 24.04.4); con el kernel 6.17 (probado en el GX10) las 9 tarjetas de este artículo vienen integradas y se reconocen al conectarlas, sin compilar y sin DKMS.

**P: Si monto un punto de acceso WPA3 con un adaptador ALFA y un iPhone antiguo no conecta, ¿qué hago?**
R: En las pruebas se detectaron dos causas comunes: una, que el `sae_pwe` de hostapd debe fijarse en 0 en lugar de 2 para ser compatible con los iPhone antiguos; dos, que conservar el ajuste 802.11n puede hacer que los dispositivos antiguos fallen la asociación, por lo que, si prioriza la compatibilidad, se recomienda desactivar 802.11n.

**P: ¿Qué familia de controlador —`rtw88`, `rtw89` o `mt76`— admite mesh o IBSS?**
R: En las pruebas, la familia `mt76` (como el AWUS036ACM / ACHM) puede crear mesh (802.11s) e IBSS en un solo equipo; el `rtw88` de Realtek puede hacer join de IBSS en un solo equipo (según lo probado con el ACH) pero no admite mesh, y el `rtw89` ni siquiera declara soporte de IBSS.

## 7. Lecturas adicionales

- Comparativa completa de capacidades y valoración de selección de las nueve tarjetas ALFA → [Hub comparativo de adaptadores WiFi ALFA (tabla maestra)](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Tutorial paso a paso de la tarjeta representativa de Realtek rtw88 → [Informe de pruebas del AWUS036ACH](/es/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- Tutorial paso a paso de la tarjeta representativa de MediaTek mt76 → [Informe de pruebas del AWUS036ACHM](/es/blog/awus036achm-asus-gx10-ubuntu-test-report/)

---

*Unidad de pruebas: Yupitek (distribuidor de ALFA Network en Taiwán) — https://www.yupitek.com | Entorno de prueba: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Dispositivo de prueba: Apple iPhone 7 Plus (WPA3 verificado adicionalmente con iPhone 15 Pro)*
