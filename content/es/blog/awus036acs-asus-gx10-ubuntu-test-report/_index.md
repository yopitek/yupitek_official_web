---
title: "AWUS036ACS, prueba práctica tarjeta a tarjeta: informe de compatibilidad y capacidades del adaptador ligero RTL8811AU en ASUS GX10 + Ubuntu 24.04 (ARM64)"
slug: awus036acs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acs
  - rtl8811au
  - rtw88-8821au
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
description: "AWUS036ACS probado en Ubuntu 24.04 ARM64: integrado en el kernel (sin instalar controlador); modo monitor, inyección (2,4G 100 %, 5G 96 %), AP, WPA3-SAE y captura de handshake de extremo a extremo (.22000) superados. Plataforma ASUS GX10, kernel 6.17, RTL8811AU."
faq:
  - question: "¿Hace falta instalar un controlador para la AWUS036ACS en Ubuntu 24.04 ARM64?"
    answer: "En el kernel 6.17 probado en este artículo (ASUS GX10), no: el RTL8811AU lo gobierna el controlador integrado rtw88_8821au; se reconoce nada más conectarlo, sin compilar ni DKMS. Con un kernel más antiguo, verifique primero con modinfo rtw88_8821au que el módulo existe."
  - question: "¿La AWUS036ACS admite modo monitor e inyección de paquetes?"
    answer: "Sí. Hace modo monitor tanto en 2,4 GHz como en 5 GHz; aireplay-ng --test da una tasa de éxito de inyección del 100 % en 2,4G (30/30) y del 96 % en 5G (29/30, tras hacer iw reg set US para levantar la restricción de TW). No admite active monitor."
  - question: "¿Puede la AWUS036ACS capturar un handshake WPA y convertirlo al formato .22000 de hashcat?"
    answer: "Sí. Prueba de extremo a extremo sobre un AP propio y un iPhone 7 Plus propio: un deauth dirigido fuerza la reconexión, se captura el 4-way completo (M1–M4) y luego hcxpcapngtool --all genera el .22000. Solo en redes propias o autorizadas."
  - question: "¿Puede la AWUS036ACS funcionar como punto de acceso (AP)? ¿Admite WPA3?"
    answer: "Sí. Con hostapd se levantan puntos de acceso en 2,4G y 5G (el ancho de canal en 5G no se confirmó); el iPhone 7 Plus se asocia y completa el 4-way; también se asocia correctamente en WPA3-SAE a 5G (SAE-only, ieee80211w=2, sae_pwe=0); WPA3 en 2,4G no se probó."
  - question: "¿Qué modos no admite la AWUS036ACS? ¿Funciona hcxdumptool?"
    answer: "No admite active monitor, IBSS, mesh (802.11s) ni Wi-Fi Direct (P2P). hcxdumptool 8.x devuelve failed to arm interface; use en su lugar airodump-ng + aireplay-ng. Para mesh / IBSS, elija la AWUS036ACM / ACHM."
draft: false
---

**Resumen (TL;DR)**: según las pruebas de Yopitek (distribuidor de ALFA Network en Taiwán), la AWUS036ACS en ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17) no necesita instalar controlador y funciona en monitor y AP de doble banda (AP 5G utilizable, ancho de canal no confirmado); inyección 2,4G 100 %, 5G 96 %, captura .22000 de extremo a extremo superada; no admite mesh / IBSS.

> Este artículo es el registro de pruebas prácticas de compatibilidad y capacidades que Yopitek realizó sobre la ALFA AWUS036ACS en una plataforma Linux moderna, pensado como apoyo para la selección de modelo.
> Plataforma de pruebas: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Todos los datos son extractos de pruebas reales de Yopitek, realizadas sobre **equipo propio y la Wi-Fi propia de la oficina** (SSID `YUPITEK`, 2,4G ch5 / 5G ch36) contra un **teléfono de prueba propio** (Apple iPhone 7 Plus); las direcciones MAC están parcialmente ocultas.
> ⚠️ **Declaración legal y de alcance**: la captura de modo monitor, inyección y handshake se realiza únicamente sobre redes y dispositivos propios o para los que se cuenta con autorización; en modo AP, respete la normativa de radio local. Este artículo se centra en las capacidades, la compatibilidad y la configuración de la propia tarjeta, y **no contempla ninguna operación ofensiva contra redes de terceros**.

---

## 1. La tarjeta y la plataforma de pruebas

La AWUS036ACS es el adaptador inalámbrico ligero y portátil de la línea de ALFA; su chip es el Realtek RTL8811AU, generación Wi-Fi 5 (802.11ac), un único flujo espacial 1x1. Su posicionamiento es muy directo: tamaño reducido, bajo consumo, una sola antena; es la tarjeta para salir a campo a hacer inventario in situ, no la tarjeta pesada para exprimir el máximo rendimiento o el mayor alcance. Por eso, al evaluarla, la pregunta no es «cuánto corre», sino «con unas especificaciones tan ligeras, qué capacidades prácticas siguen estando completas y disponibles».

Esta ronda de pruebas la coloca en un escenario de operación típico: la tarjeta integrada del GX10 (`wlP9s9`) se encarga de la conexión a Internet, y la AWUS036ACS, por USB externo, solo asume las tareas de prueba. Así, al pasar a modo monitor o AP no se toca la propia red del equipo anfitrión. En todo momento solo se manipula la interfaz `wlx*` correspondiente a la tarjeta ALFA, sin tocar la tarjeta integrada de salida a Internet.

| Elemento | Contenido |
|---|---|
| Modelo | AWUS036ACS |
| Chip | Realtek RTL8811AU (Wi-Fi 5 / 802.11ac, un único flujo 1x1) |
| USB ID | `0bda:0811` |
| Controlador | `rtw88_8821au` (integrado en el kernel, incluido en el kernel 6.17) |
| Firmware | 42.4.0 (medido en dmesg) |
| Plataforma | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| Dispositivo de prueba | Apple iPhone 7 Plus |

---

## 2. Hardware y controlador (sin instalación)

Esta tarjeta se reconoce nada más conectarla en el GX10, sin compilar ni DKMS. El chip RTL8811AU / RTL8821AU se integró oficialmente en la familia de controladores `rtw88` de Realtek, incluidos en el kernel (in-kernel), a partir del kernel mainline 6.13; el 6.17 que monta el GX10 ya incorpora el módulo `rtw88_8821au`, por lo que no hace falta bajar ningún proyecto out-of-tree de GitHub. (A diferencia de las guías de instalación antiguas: los artículos tempranos partían del controlador out-of-tree de `morrownr` o de un kernel más antiguo y afirmaban que había que compilar por DKMS; con el controlador integrado en el kernel 6.17 eso ya no es necesario.) El conocido `morrownr/8821au-20210708` es ahora legacy (solo se recomienda en kernels anteriores al 6.13, y además al instalarlo pone en la lista negra el controlador integrado); en kernels nuevos no hay por qué volver a ese camino antiguo. La ventaja en coste operativo es aún más tangible: el controlador integrado en el kernel se actualiza junto con el propio kernel, el usuario no tiene que mantener su propia rama, ni se queda atascado en una compilación DKMS fallida en cada actualización; el mismo procedimiento se reutiliza a lo largo de varias actualizaciones de kernel. El firmware lo trae `linux-firmware` con el sistema; en esta prueba la versión medida es 42.4.0, y tampoco hay que gestionarlo manualmente.

Comprobamos que la tarjeta ha sido reconocida, que el controlador está vinculado y que la interfaz se ha creado:

```bash
lsusb | grep -i 0bda:0811
# Bus 003 Device 004: ID 0bda:0811 Realtek Semiconductor Corp. Realtek 8812AU/8821AU 802.11ac WLAN Adapter

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"
cat /sys/class/net/$IF/phy80211/name
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# IF=wlx00c0cabce039 / phy1 / rtw88_8821au
```

La versión del firmware se puede verificar con `dmesg` (medida: 42.4.0):

```bash
sudo dmesg | grep -i 8821au
# rtw88_8821au ... Firmware version 42.4.0, H2C version 0
```

Modos de interfaz declarados como compatibles (esto determina qué capacidades estarán disponibles más adelante):

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
# IBSS / managed / AP / AP/VLAN / monitor
```

Esta lista muestra `IBSS / managed / AP / AP/VLAN / monitor`. Conviene advertir algo: aunque la lista incluye IBSS, en la prueba, tras `ibss join`, `iw link` muestra Not connected y no llega a conectar; mesh, active-monitor y P2P ni siquiera aparecen en la lista (véanse las limitaciones en la sección 4). Es el estado actual del hardware y el controlador del RTL8811AU, y no tiene que ver con el número de antenas.

Cobertura de bandas: 2,4 GHz ch1–13 (ch14 deshabilitado); 5 GHz ch36–165 (los ch52–144 marcados como radar / DFS). El dominio regulatorio por defecto es `TW`, con potencia de TX de 30 dBm en 2,4 GHz, 23 dBm en UNII-1/2 de 5 GHz y 30 dBm en UNII-3.

---

## 3. Capacidades medidas: modo monitor / inyección / AP / WPA3

Veamos primero la tabla resumen de capacidades clave y luego las desglosamos una a una. Todos los apartados se completaron sobre el AP propio YUPITEK y un iPhone 7 Plus propio.

| Capacidad | 2,4 GHz | 5 GHz |
|---|---|---|
| Modo monitor (recepción en escucha) | ✅ fuerte | ✅ fuerte |
| Inyección (de paquetes) | ✅ **100 %** (30/30) | ✅ **96 %** (29/30, hay que desbloquear reg antes) |
| Punto de acceso (hostapd) | ✅ iPhone asociado + handshake completado | ✅ **estable** (ancho de canal no confirmado) |
| AP WPA3-SAE | No probado | ✅ iPhone asociado (SAE-only + PMF) |

### 3-1. Modo monitor (2,4 GHz + 5 GHz) ✅

Tras pasar a modo monitor, se hizo una captura de duración fija en cada uno de los seis canales, y la recepción fue correcta en todos. Los canales con más tráfico alcanzan el límite de 300 tramas en menos de 6 segundos:

| Canal | Tramas capturadas |
|---|---|
| ch1 / 2412 | 300 |
| ch6 / 2437 | 300 |
| ch11 / 2462 | 146 |
| ch36 / 5180 | 300 |
| ch149 / 5745 | 141 |
| ch157 / 5785 | 154 |

Tanto 2,4 GHz como 5 GHz reciben con estabilidad. Para un adaptador portátil de una sola antena, esta recepción basta para cubrir el inventario de canales in situ y el diagnóstico de paquetes. El bajo número de tramas en ch11, ch149 y ch157 se debe a que en ese momento esos canales tenían poco tráfico en el aire, no a que la tarjeta no reciba; en los canales con más tráfico (ch1, ch6, ch36) alcanza el tope de 300 tramas en seis segundos, de modo que la recepción no es su cuello de botella.

### 3-2. Inyección (de paquetes) ✅

Prueba de inyección dirigida con `aireplay-ng --test` contra el AP propio YUPITEK. En 2,4 GHz llega al 100 % (30/30, `Injection is working!`) y en 5 GHz al 96 % (29/30). En 5 GHz hay un detalle de configuración a tener en cuenta: el `reg=TW` por defecto bloquea la transmisión activa en parte de las bandas UNII; antes de la prueba, haga `sudo iw reg set US` para desbloquear, y al terminar vuelva a `sudo iw reg set TW`.

```bash
# 2,4 GHz (YUPITEK realmente en ch5 / 2432)
sudo iw dev $IF set freq 2432
sudo aireplay-ng --test --ignore-negative-one -a <YUPITEK-BSSID> $IF
# Injection is working!  30/30: 100%  Power: -60.00
```

Que un adaptador de una sola antena consiga el 100 % en 2,4 GHz y el 96 % en 5 GHz ya es una capacidad de inyección bastante fiable, y es también la base que le permite completar más adelante la captura de handshake de extremo a extremo.

### 3-3. Punto de acceso (2,4 GHz / 5 GHz) ✅

Con `hostapd` convertimos la tarjeta en estación base; las tres configuraciones permitieron que el iPhone 7 Plus se asociara correctamente y completara el 4-way handshake (`EAPOL-4WAY-HS-COMPLETED`):

- **5 GHz (ancho de canal no confirmado)**: la configuración más estable; el iPhone se asocia, el handshake se completa y `AP-DISABLED` cierra limpiamente.
- **2,4 GHz (WPA2-PSK)**: el iPhone se asocia, el handshake se completa y, tras la desconexión, cierra limpiamente. Aquí anotamos con honestidad una incidencia: en una ronda anterior con la misma configuración apareció una vez `key not allowed / Failed to set beacon parameters` tras la desconexión de la STA, con el consiguiente aborto; al repetir la prueba no se pudo reproducir, por lo que se concluye que es un re-key de beacon esporádico del rtw88_8821au, no un defecto permanente. Aun así, conviene vigilarlo en escenarios de reconexión prolongada y de alta frecuencia, o directamente usar un AP en 5 GHz.
- **WPA3-SAE (5 GHz, PMF forzado; 2,4 GHz no probado)**: la configuración clave es `wpa_key_mgmt=SAE` (WPA3 puro, sin fallback a WPA2), `ieee80211w=2` (Management Frame Protection forzado) y `sae_pwe=0` (compatibilidad con clientes antiguos). El iPhone 7 Plus (iOS 15) se asoció correctamente mediante SAE. Como el AP solo ofrece SAE, sin ruta de reserva a WPA2, el hecho de completar la asociación demuestra que el handshake de autenticación SAE se establece. El WPA3-SAE del RTL8811AU + rtw88_8821au en el lado AP está disponible.

---

## 4. Capacidad de handshake de extremo a extremo y limitaciones

### 4-1. Captura de handshake de extremo a extremo ✅

Esta es la prueba integral que verifica si la inyección y la captura realmente «se encadenan»; todo el proceso se realiza sobre el AP propio YUPITEK, el iPhone 7 Plus propio y bajo autorización. El flujo es: monitor en el canal objetivo → enviar un deauth dirigido al dispositivo propio para forzar la reconexión → capturar el 4-way completo (M1–M4) → usar `hcxpcapngtool --all` para generar el `.22000` legible por hashcat.

Resultado medido: `aircrack-ng` determina que YUPITEK obtuvo 1 handshake, con los cuatro mensajes EAPOL M1–M4 completos; el cliente es un OUI de Apple (`b8:53:ac`, confirmado como el iPhone 7 Plus), y el `.22000` generado se puede pasar directamente a hashcat. Esto demuestra que la AWUS036ACS cuenta con una capacidad de captura de handshake de extremo a extremo completa.

Merece la pena anotar dos puntos prácticos (la configuración paso a paso completa se trata en otro artículo):

1. **Cuando en la oficina hay varios AP con el mismo nombre en el mismo canal, no acote a uno solo con `--bssid`**; capture todo el canal para no perder el dispositivo que está asociado a otro de ellos.
2. `hcxpcapngtool` es estricto por defecto y puede devolver «not enough M1»; añadiendo `--all` genera el `.22000` a partir de los M1–M4 completos.

Las herramientas habituales de Kali empleadas en esta cadena de captura de handshake (aircrack-ng, hcxtools) se ejecutan directamente sobre Ubuntu 24.04 ARM64; airodump-ng, aireplay-ng y hcxpcapngtool funcionan todos con normalidad.

### 4-2. VIF (interfaz virtual) ✅

`iw dev $IF interface add mon9 type monitor` permite crear una VIF de monitor y capturar 100 tramas; además, con un script que crea «interfaz principal conectada a YUPITEK como STA + una VIF de AP», un único chip puede hacer de STA y de AP a la vez.

### 4-3. Limitaciones honestas (reportadas en la prueba)

| Modo / herramienta avanzada | Estado | Prueba |
|---|---|---|
| Active monitor | ❌ no admitido | `iw set monitor active` → `Operation not supported (-95)` |
| Ad-hoc (IBSS) | ❌ no admitido | el modo aparece listado pero tras `ibss join`, `iw link` = Not connected |
| Mesh (802.11s) | ❌ no admitido | `set type mp` → `-95` |
| Wi-Fi Direct (P2P) | ❌ no admitido | `interface add type __p2pcl` → `-95` |
| hcxdumptool 8.x | ⚠️ no puede hacer arm | `failed to arm interface`: rtw88_8821au no ofrece active-monitor; use airodump-ng + aireplay-ng |

Hay además dos limitaciones operativas que conviene conocer. El único flujo 1x1 fija su límite teórico (HT Max RX 150 Mbps, VHT80 unos 433 Mbps), de modo que el rendimiento nunca ha sido su fuerte. Tras alternar repetidamente entre monitor y AP, la recepción (RX) a veces se degrada brevemente (no escanea nada); en ese caso, basta con desconectar y reconectar físicamente la tarjeta una vez para recuperarla, y como el nombre de la interfaz lo determina la MAC, se mantiene igual tras el reenchufe.

---

## 5. Casos de uso y selección de modelo (ligera y portátil, con retorno al Hub)

Si contrastamos estas capacidades con el posicionamiento del producto, el papel de la AWUS036ACS queda claro: una tarjeta portátil de capacidades completas pero orientada ante todo a la ligereza. ¿En qué escenarios encaja?

- **Inventario rápido in situ / diagnóstico portátil**: una sola antena, tamaño pequeño y bajo consumo; sirve para salir a campo a hacer inventario de canales, inspección de señal o diagnóstico de paquetes. Combinada con una plataforma central como el GX10, el adaptador portátil captura in situ y devuelve los datos al Hub para el análisis centralizado, con un reparto de tareas claro.
- **Docencia y verificación**: recorre por completo la línea principal de modo monitor / inyección / AP / WPA3-SAE / handshake de extremo a extremo, por lo que es idónea como tarjeta de demostración y de verificación dentro del alcance autorizado.
- **Escenarios en los que no encaja**: cuando se necesita el máximo rendimiento, el mayor alcance, o mesh / IBSS / P2P / active-monitor, esta tarjeta no es la elección correcta.

Ligera no equivale a funciones recortadas. No le falta ni una de las capacidades de la línea principal; lo que se ha sacrificado es el techo de rendimiento y los modos de interfaz avanzados. Así que elegirla o no depende de si lo que busca es «llevarla encima» o «correr a tope».

Frente al resto de la misma familia, las diferencias de posicionamiento son estas:

| Necesidad | Tarjeta recomendada | Motivo |
|---|---|---|
| Ligera y portátil + línea principal completa | **AWUS036ACS** | inyección 2,4G 100 %, 5G 96 %, handshake de extremo a extremo disponible, una sola antena y ligera |
| Inyección al 100 % en ambas bandas / verificación de pentest más robusta | AWUS036EACS, AWUS036ACH | inyección al 100 % en ambas bandas; la EACS incluye además BT |
| Máxima recepción / monitor de largo alcance | AWUS036AXER, AWUS036ACH | el escaneo por salto de canal encuentra más objetivos / doble antena de alta ganancia |
| Experimentos de mesh / IBSS en local | AWUS036ACM, AWUS036ACHM | el controlador mt76 permite crearlos en un solo equipo (el rtw88 de Realtek no los admite) |

Selección en una frase: si busca ligereza y a la vez una línea principal completa, la AWUS036ACS es una buena opción portátil; si busca inyección al 100 % en ambas bandas o una verificación de pentest más exigente, vaya hacia la EACS / ACH.

---

## Preguntas frecuentes (FAQ)

**P: ¿Hace falta instalar un controlador para la AWUS036ACS en Ubuntu 24.04 ARM64?**
En el kernel 6.17 probado en este artículo (ASUS GX10), no: el RTL8811AU lo gobierna el controlador integrado rtw88_8821au; se reconoce nada más conectarlo, sin compilar ni DKMS. Con un kernel más antiguo, verifique primero con `modinfo rtw88_8821au` que el módulo existe.

**P: ¿La AWUS036ACS admite modo monitor y packet injection (inyección de paquetes)?**
Sí. Hace modo monitor tanto en 2,4 GHz como en 5 GHz; `aireplay-ng --test` da una tasa de inyección del 100 % en 2,4G (30/30) y del 96 % en 5G (29/30, tras hacer `iw reg set US` para levantar la restricción de TW). No admite active monitor.

**P: ¿Puede la AWUS036ACS capturar un handshake WPA (paquetes de handshake) y convertirlo al .22000 de hashcat?**
Sí. Prueba de extremo a extremo sobre un AP propio y un iPhone 7 Plus propio: un deauth dirigido fuerza la reconexión, se captura el 4-way completo (M1–M4) y luego `hcxpcapngtool --all` genera el .22000. Solo en redes propias o autorizadas.

**P: ¿Puede la AWUS036ACS funcionar como punto de acceso (AP)? ¿Admite WPA3?**
Sí. `hostapd` levanta puntos de acceso en 2,4G y 5G (el ancho de canal en 5G no se confirmó); el iPhone 7 Plus se asocia y completa el 4-way; también se asocia correctamente en WPA3-SAE a 5G (SAE-only, ieee80211w=2, sae_pwe=0); WPA3 en 2,4G no se probó.

**P: ¿Qué modos no admite la AWUS036ACS? ¿Funciona hcxdumptool?**
No admite active monitor, IBSS, mesh (802.11s) ni Wi-Fi Direct (P2P). hcxdumptool 8.x devuelve failed to arm interface; use en su lugar airodump-ng + aireplay-ng. Para mesh / IBSS, elija la AWUS036ACM / ACHM.

---

## 6. Lecturas adicionales

- Comparativa de capacidades completa y valoración de selección de las nueve tarjetas ALFA → [Hub de valoración de adaptadores inalámbricos ALFA (tabla general)](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Integrado en el kernel: habilitar modo monitor / AP en Ubuntu 24.04 + kernel 6.17 (rtw88 / rtw89 / mt76, probado)](/es/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- [Tutorial paso a paso de WPA3-SAE y captura de handshake de extremo a extremo](/es/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Tarjeta combinada BT+WiFi de la misma familia → [AWUS036EACS, prueba práctica tarjeta a tarjeta](/es/blog/awus036eacs-asus-gx10-ubuntu-test-report/)

---

*Unidad de pruebas: Yopitek (distribuidor de ALFA Network en Taiwán) — https://www.yupitek.com | Entorno de pruebas: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Dispositivo de prueba: Apple iPhone 7 Plus*
