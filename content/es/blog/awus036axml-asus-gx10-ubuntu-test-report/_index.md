---
title: "Prueba práctica de la AWUS036AXML: tarjeta combinada Wi-Fi 6 + Bluetooth en ASUS GX10 (ARM64 / Ubuntu 24.04) —— un informe honesto: AP estable, inyección fallida"
slug: awus036axml-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axml-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036axml-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axml
  - mt7921
  - mt7921u
  - wifi-6
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - ap-mode
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036AXML (Wi-Fi+Bluetooth) en ASUS GX10/Ubuntu 24.04 ARM64: AP, WPA3 y monitor funcionan, pero la inyección falla y no se puede capturar el handshake; no se recomienda para pruebas de penetración."
faq:
  - question: "¿La AWUS036AXML puede hacer inyección de paquetes (packet injection)?"
    answer: "En nuestra plataforma de prueba (ASUS GX10/Ubuntu 24.04 ARM64/stock kernel 6.17.0-1014-nvidia) no. aireplay-ng --test devuelve No Answer y Found 0 APs; probando AP por AP con un BSSID concreto solo se obtiene No such BSSID available. Aunque un escaneo normal sí ve ese AP (unos -54 dBm), en el contexto de las herramientas de inyección la tarjeta sigue sin recibir su beacon, así que ni el deauth ni la captura de handshake (0 capturas) son utilizables. La causa de fondo es una regresión de chanctx en mac80211 del kernel 6.16+, no una incapacidad nativa del chip para inyectar; la AWUS036AXM da el mismo resultado. Si necesita inyección, elija las AWUS036EACS, ACH o ACS."
  - question: "¿El Bluetooth de la AWUS036AXML funciona en Ubuntu?"
    answer: "En nuestra máquina el Bluetooth funcionó: con bluetoothctl/hciconfig confirmamos que el controlador hci está UP, pudimos detectar dispositivos BLE y Bluetooth clásico, y Wi-Fi y Bluetooth pueden usarse a la vez (coexistencia). Es un dispositivo combinado Wi-Fi+Bluetooth; un aviso: al reconectar, de vez en cuando se queda atascada en el WiFi probe y no genera la interfaz wlx; basta con reconectarla en otro puerto USB para recuperarla."
  - question: "¿La AWUS036AXML necesita instalar controladores aparte en Ubuntu 24.04?"
    answer: "No. El controlador mt7921u está integrado en el kernel 6.17; al conectarla, dmesg muestra que mt7921u renombra la interfaz a wlx más la MAC (USB ID 0e8d:7961), sin DKMS y sin compilar. El controlador no ofrece los modos IBSS ni mesh."
  - question: "¿La AWUS036AXML puede abrir un AP y admite WPA3?"
    answer: "Sí, y es su uso más estable. Tanto en 2,4 GHz (802.11n, MCS 10) como en 5 GHz VHT80 (VHT-NSS2) el iPhone se conectó y quedó authorized; con WPA3-SAE y sae_pwe=0 logramos conectar un iPhone 15 Pro (MFP: yes; probado en 2,4 GHz y 6 GHz, no en 5 GHz); con STA+AP en concurrencia, el ping del lado STA fue de unos 4,4 ms. Aunque se clasifica como chip Wi-Fi 6, en nuestra máquina probamos además que la banda de 6 GHz es usable (montamos un AP a 6135 MHz y el iPhone 15 Pro se conectó por 802.11ax y obtuvo IP)."
  - question: "¿En qué se diferencian la AWUS036AXML y la AWUS036AXM, y cuál elegir?"
    answer: "En esta plataforma el comportamiento Wi-Fi de ambas es idéntico: usan el mismo mt7921u, la inyección falla igual, el monitor recibe igual de flojo, y AP, WPA3 y VIF funcionan por igual. La diferencia es que la AXML lleva además Bluetooth (probado y funcional en nuestra máquina) y que en nuestra máquina la banda de 6 GHz resultó usable, mientras que el Bluetooth y los 6 GHz de la AXM no se probaron por separado en esta ronda. Para AP puro o conexión general cualquiera de las dos sirve; para inyección o handshake, ninguna de las dos."
draft: false
---

{{< tldr >}}En ASUS GX10/Ubuntu 24.04 ARM64, la AWUS036AXML tiene AP, WPA3, VIF y monitor pasivo funcionales, y en nuestra máquina el Bluetooth y la banda de 6 GHz también resultaron usables, pero la inyección falló en la prueba (No Answer/Found 0 APs): no puede hacer deauth ni capturar handshakes, no se recomienda para pruebas de penetración; su sitio es el AP puro y la conexión general.{{< /tldr >}}

La ALFA AWUS036AXML es el único modelo combinado «MediaTek Wi-Fi 6 + Bluetooth» de este lote de 9 tarjetas. Comparte generación de chip (MT7921, con el controlador `mt7921u`) con la AWUS036AXM sin Bluetooth; la diferencia está solo en que lleva de más un bloque de Bluetooth. La pregunta más frecuente del cliente siguen siendo las mismas tres: ¿entra en monitor? ¿puede inyectar? ¿puede montar un AP? Este artículo saca la AWUS036AXML por separado y la prueba punto por punto en ASUS GX10 (ARM64) con Ubuntu 24.04, dejando claro de una vez lo que puede y lo que no puede, sobre todo esa limitación clave: **la inyección falla en esta plataforma**.

Dejemos clara la premisa: todas las mediciones se realizaron sobre equipo propio de Yopitek, la Wi-Fi propia de la oficina (SSID `YUPITEK`) y frente a nuestro propio teléfono de prueba (iPhone 7 Plus; para WPA3 se revalidó además con un iPhone 15 Pro). Es una validación de hardware que un distribuidor hace sobre la compatibilidad y los límites de capacidad del producto, no un tutorial de operación contra redes de terceros. Las autopruebas de monitor, AP e inyección de este texto se hicieron todas en un entorno cerrado propio y sobre dispositivos propios.

## 1. Esta tarjeta y la plataforma de prueba

- **Plataforma de cómputo**: ASUS GX10 (ARM64 / aarch64)
- **Sistema operativo**: Ubuntu 24.04 LTS
- **Versión del kernel**: kernel 6.17.0-1014-nvidia
- **Tarjeta probada**: ALFA AWUS036AXML (MediaTek MT7921AUN, Wi-Fi 6 / 2x2 / +BT)
- **Dispositivo de prueba**: Apple iPhone 7 Plus (WPA3-SAE revalidado además con un iPhone 15 Pro)
- **Entorno de prueba**: Wi-Fi propia de la oficina, SSID `YUPITEK`, 2.4GHz ch5 / 5GHz ch36, ch157
- **Periodo de prueba**: mediciones sobre hardware real del 2026-11-16 al 2026-11-18

Todos los resultados se registran como el número o el estado efectivamente medidos, sin deducirlos de la hoja de especificaciones; las direcciones MAC aparecen enmascaradas con `xx` en las salidas.

## 2. Hardware y controlador: MT7921AUN, listo para usar

| Elemento | Especificación |
|---|---|
| Modelo | AWUS036AXML |
| Chip | MediaTek MT7921AUN |
| USB ID | `0e8d:7961` (MediaTek Inc. Wireless_Device) |
| Controlador integrado en el kernel | `mt7921u` |
| Generación / flujos | Wi-Fi 6 / 2x2 (2T2R) |
| Bluetooth | Sí (dispositivo combinado BT + WiFi; en nuestra máquina probamos que el controlador hci está UP, detecta dispositivos BLE y Bluetooth clásico, y hay coexistencia WiFi+BT) |
| Enumeración USB | USB 3 |
| Nombre de interfaz | `wlx<MAC>` (p. ej.: `wlx00c0cabd65b9`) |

La forma de reconocerla es directa: tras conectarla, con `lsusb` se ve el USB ID de MediaTek y con `dmesg` se ve que `mt7921u` se ha montado y ha renombrado la interfaz:

```bash
lsusb | grep 0e8d:7961
# Bus 004 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device

sudo dmesg | grep mt7921u | tail -1
# mt7921u 4-1:1.3 wlx00c0cabd65b9: renamed from wlan0
```

Dos puntos clave. El primero, sin compilar: la AWUS036AXML usa el controlador `mt7921u` integrado en el kernel 6.17 y queda reconocida nada más conectarla, sin tener que lidiar con ningún módulo DKMS out-of-tree en aarch64, lo cual es especialmente cómodo en plataformas ARM64. El segundo, que se enumera como USB 3 (en algunos modelos de la generación anterior el cable OTG era solo USB 2.0), así que el ancho de banda de transferencia no es un cuello de botella.

Un apunte que suele malinterpretarse: la AWUS036AXML se clasifica como chip Wi-Fi 6 (no 6E), pero **en nuestra máquina probamos que la banda de 6 GHz es usable**: montamos un AP a 6135 MHz y el iPhone 15 Pro se conectó por 802.11ax y obtuvo IP. El Bluetooth también se probó y funciona: con `hciconfig`/`bluetoothctl` se ve el estado del controlador hci como UP, se detectan dispositivos BLE y Bluetooth clásico, y Wi-Fi y Bluetooth pueden funcionar a la vez (coexistencia).

Consultando una vez más los modos de interfaz admitidos, aparece un detalle relevante para la selección: no hay IBSS, ni tampoco mesh point:

```bash
iw phy <phyN> info | sed -n '/Supported interface modes/,/Band 1/p'
```
```
Supported interface modes:
    * managed
    * AP
    * AP/VLAN
    * monitor
    * P2P-client / P2P-GO / P2P-device
```

Es decir: managed, AP, monitor y P2P están todos, pero los dos modos ad-hoc (IBSS) y mesh 802.11s el controlador `mt7921u` sencillamente no los ofrece. Para el cliente que quiera experimentar con mesh / IBSS, esta tarjeta queda directamente descartada (mire la ACM / ACHM del controlador `mt76`).

## 3. Capacidades probadas: Monitor / AP / WPA3, y la limitación honesta de la inyección

Las capacidades centrales de un vistazo:

| Capacidad | 2.4GHz | 5GHz | Explicación |
|---|---|---|---|
| Monitor | ✅ (floja) | ✅ (floja) | Puede captar beacons; a menudo se pierden paquetes de client / data |
| **Inyección** | ❌ **falla** | ❌ **falla** | `aireplay-ng` no logra inyectar / deauth; causa de fondo: regresión de chanctx en mac80211 del kernel 6.16+ (no nativa del chip) |
| AP (punto de acceso) | ✅ incl. 802.11n | ✅ VHT80 (80MHz) | iPhone 7 Plus conectado, `authorized: yes` |
| WPA3-SAE | ✅ | No probado | iPhone 15 Pro conectado, `MFP: yes` (`sae_pwe=0`); probado también en 6 GHz (ch37, 6135 MHz) |

### Monitor: entra en ambas bandas, pero la recepción es floja

La AWUS036AXML entra en modo monitor tanto en 2.4GHz (ch1 / 6 / 11) como en 5GHz (ch36 / 149 / 157), y captar beacons no es problema. El flujo de configuración son los cuatro pasos estándar de `iw dev`:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36     # para 2.4GHz use set channel 6
```

Dicho con honestidad: su recepción en monitor es claramente más débil que la del MT7612U (ACM) del mismo lote o la de la AXER Wi-Fi 6. Capta beacons, pero a menudo se pierden paquetes de client / data; al escanear por salto de canal con `airodump-ng` es fácil que se le escapen algunos AP. En la práctica recomendamos fijar un único canal (`-c <ch>`) en vez de saltar entre canales: los resultados serán algo más estables. Además, en modo monitor `iw info` reporta solo 3 dBm de txpower, lo cual es un **artefacto de lectura** (el TX real del hardware ronda los 20–23 dBm, verificado con `txpower_sku`) y no significa que la potencia esté realmente limitada a 3 dBm; de esto hablamos más abajo en «Notas».

### AP: en 2.4GHz con HT, en 5GHz alcanza VHT80

El AP es lo más estable de la AWUS036AXML. En 2.4GHz se puede mantener directamente 802.11n (HT), sin tener que desactivarlo como en la ACHM de una sola antena; en 5GHz se puede subir a VHT 80MHz. En ambas bandas, en la prueba el iPhone 7 Plus se conectó y quedó `authorized: yes`.

Ajustes clave de hostapd para VHT80 en 5GHz:

```
hw_mode=a
channel=36
ieee80211ac=1
ht_capab=[HT40+][SHORT-GI-20][SHORT-GI-40]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42
vht_capab=[SHORT-GI-80]
```

Tras conectarse, se midió VHT-NSS2, 80MHz. Para la versión de 2.4GHz, cambie `hw_mode` a `g` y `channel=6`, mantenga `ieee80211n=1` y `ht_capab=[HT20]`, y el iPhone se conecta como MCS 10 (802.11n).

### WPA3-SAE: funciona, recuerde sae_pwe=0

Cambie el `wpa_key_mgmt` del AP a `SAE`, añada `ieee80211w=2` y `sae_pwe=0` y ya puede abrir WPA3-SAE. En la prueba, el iPhone 15 Pro se conectó en 2.4 GHz (y en 6 GHz; 5 GHz no se probó) con `authorized: yes` y `MFP: yes`. `sae_pwe=0` es para la compatibilidad con iPhone antiguos; es el mismo campo minado que en la ACHM: con `sae_pwe=2`, los equipos antiguos a menudo no conectan.

### VIF: a la vez conectado a Internet y como punto de acceso, viable

La AWUS036AXML admite la concurrencia de múltiples interfaces. Creando una VIF de AP (con MAC distinta, unmanage), con la interfaz principal conectada a la Wi-Fi y el AP en el mismo canal, en la prueba, con el iPhone 7 Plus conectado a la VIF de AP, el ping del STA hacia `YUPITEK` fue de 4,4 ms. Para la necesidad de «una tarjeta que a la vez da Internet + comparte punto de acceso», se cumple.

### Limitación honesta: la inyección falla en esta plataforma

Esta es la cuestión que más hay que dejar clara de la AWUS036AXML (y de su gemela sin Bluetooth, la AXM). En ASUS GX10 + kernel 6.17 hicimos una autoprueba de inyección sobre nuestro propio entorno de prueba, y el resultado fue un fallo:

```bash
sudo aireplay-ng --test $IF
```
```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

Incluso probando AP por AP con el BSSID de nuestro propio AP, solo devuelve `No such BSSID available`. La clave es que: un escaneo normal sí ve claramente ese AP (señal de -54 dBm), pero en cuanto se entra en el contexto de una herramienta de inyección, la tarjeta «no oye» el beacon del objetivo, el deauth no sale y el número de capturas del 4-way handshake es 0.

Esto no es un parámetro mal ajustado ni el fallo de una tarjeta concreta. La verdadera causa de fondo está en la **capa de software**: a partir del kernel 6.16, el channel context (chanctx) de mac80211 sufrió una regresión que impide al controlador stock recibir los beacons del objetivo en el contexto de inyección, por lo que `aireplay-ng` concluye `No Answer`, y **no es una incapacidad nativa del chip MT7921 para inyectar**. El fenómeno está documentado en morrownr/USB-WiFi issue #387, y el análisis de la causa de fondo en morrownr/mt76 issue #18. Las pruebas de la comunidad indican que, con un controlador git/parcheado en el mismo modelo, se puede hacer funcionar el active monitor junto con la inyección, pero el firmware del MT7921 mantiene la inyección bloqueada a las tasas base de 1 Mbps/6 Mbps, sin poder inyectar a HT/VHT; la AXM y la AXML caen igual en esto sobre **stock kernel 6.17**, y a fecha de 2026-11-18 no hay forma de resolverlo ajustando parámetros.

Por tanto, toda capacidad que implique inyección —como el deauth, la captura de handshake WPA o las pruebas de penetración que parten de la inyección— la AWUS036AXML no las puede hacer en esta plataforma. Para esos usos, elija un modelo cuya inyección sí funcione en nuestras pruebas (ver la selección más abajo).

### Vistazo al resto de modos avanzados

| Función avanzada | Estado | Explicación |
|---|---|---|
| VIF (STA + AP en concurrencia) | ✅ | Mismo canal ch36; con el iPhone conectado, ping STA de 4,4 ms |
| Captura de handshake WPA | ❌ | La inyección falla → el deauth no sale, handshake 0 |
| Active monitor | 🟡 | `set monitor active` se acepta, pero no se verificó el ACK |
| Ad-hoc (IBSS) | N/A | El controlador `mt7921u` no tiene este modo |
| Mesh (802.11s) | N/A | El controlador `mt7921u` no tiene este modo |
| Wi-Fi Direct (P2P) | ⬜ | El controlador declara soporte, requiere un segundo equipo, omitido |

## 4. Notas sobre la tarjeta combinada Bluetooth y usos adecuados/inadecuados

### Efecto secundario práctico de la tarjeta combinada BT + WiFi

La AWUS036AXML incorpora Bluetooth, y es uno de los dos dispositivos combinados de este lote (el otro es la EACS de Realtek). El Bluetooth ya se probó y funciona en nuestra máquina (controlador hci UP, detecta dispositivos BLE y Bluetooth clásico, coexiste con Wi-Fi, ver antes); aquí añadimos un efecto secundario práctico de los dispositivos combinados: al reconectar, de vez en cuando se queda atascada en el WiFi probe y no genera la interfaz `wlx`, con el síntoma de que tras desconectar y reconectar `ls /sys/class/net` no termina de ver la tarjeta. La solución es muy simple: **reconectar en otro puerto USB**, y suele enumerar con normalidad.

Otro pequeño gesto que conviene recordar: si en modo AP el teléfono deja de captar de repente tu SSID, basta con **desconectar y volver a conectar** la tarjeta para reiniciarla, sin tocar la configuración. (Nota: como se dijo antes, los 3 dBm que reporta el monitor son un artefacto, no la potencia real, y no son la causa de que desaparezca el SSID.)

### Reglas de seguridad de la plataforma

- Nunca ejecute `airmon-ng check kill`: apaga NetworkManager y deja sin conexión a todo el GX10. Al operar, toque solo la interfaz externa `wlx*` y no toque la línea principal de conexión a Internet integrada.
- `hcxdumptool 8.x` da `failed to arm` en esta máquina (salvo el AWUS036EACS en 2.4 GHz) (conflicto de enumeración de la tarjeta integrada triple banda del GX10 + controlador sin active-monitor); es un achaque común a toda la plataforma, ajeno a la AXML; cuando necesite una función similar, use `airodump-ng` junto con otras herramientas de aircrack-ng.
- Apunte para ARM64: `aircrack-ng` debe compilarse desde el código fuente, y para `wifite` se recomienda la versión git para sortear los conflictos de dependencias de apt.

### Vistazo de usos adecuados / inadecuados

| Escenario adecuado | Escenario inadecuado |
|---|---|
| AP / punto de acceso puro (2.4G con HT, 5G VHT80) | inyección / deauth |
| Punto de acceso WPA3-SAE | Captura de handshake WPA |
| Conexión managed general | Tarjeta principal para pruebas de penetración basadas en inyección |
| Monitor pasivo / inventario del espectro (fijando un único canal) | mesh / IBSS experimental |
| STA + AP en concurrencia (VIF, conectado y compartiendo a la vez) | Captura a larga distancia que requiera recepción potente |

## 5. Recomendaciones de selección (de vuelta a la tabla global)

Poniendo la AWUS036AXML de nuevo en el panorama de las 9 tarjetas, su posición es muy clara: MediaTek, con conexión estable, sin compilar, y con AP en ambas bandas que alcanza VHT80; es una competente tarjeta de «conexión pura / AP puro»; en cuanto se roce la inyección, deja de ser su terreno.

| Necesidad | Modelo recomendado |
|---|---|
| AP puro / conexión general (sin inyección) | **AWUS036AXML / AWUS036AXM** (esta tarjeta es apta) |
| inyección + handshake (pruebas de penetración) | AWUS036EACS / AWUS036ACH / AWUS036ACS |
| Experimentos de mesh / IBSS | AWUS036ACM / AWUS036ACHM |
| Máxima recepción / monitor a larga distancia | AWUS036AXER / AWUS036ACH |

Si está decidiendo entre las 9, para la matriz global completa de Monitor / Inyección / AP / WPA3 y la selección según el uso, consulte la tabla global:

- [La prueba práctica más completa de 2026: matriz global de 9 tarjetas Wi-Fi ALFA en ASUS GX10](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

Un aviso en una frase: **para inyección o handshake, no elija la AWUS036AXML / AWUS036AXM**; para conexión pura o montar un punto de acceso, es muy buena.

## Preguntas frecuentes (FAQ)

**Q1. ¿La AWUS036AXML puede hacer inyección de paquetes (packet injection)?**
En nuestra plataforma de prueba (ASUS GX10/Ubuntu 24.04 ARM64/stock kernel 6.17.0-1014-nvidia) no. `aireplay-ng --test` devuelve `No Answer` y `Found 0 APs`; probando AP por AP con un BSSID concreto solo se obtiene `No such BSSID available`. Aunque un escaneo normal sí ve ese AP (unos -54 dBm), en el contexto de las herramientas de inyección la tarjeta sigue sin recibir su beacon, así que ni el deauth ni la captura de handshake (0 capturas) son utilizables. La causa de fondo es una regresión de chanctx en mac80211 del kernel 6.16+, no una incapacidad nativa del chip para inyectar; la AWUS036AXM da el mismo resultado. Si necesita inyección, elija las AWUS036EACS, ACH o ACS.

**Q2. ¿El Bluetooth de la AWUS036AXML funciona en Ubuntu?**
En nuestra máquina el Bluetooth funcionó: con `bluetoothctl`/`hciconfig` confirmamos que el controlador hci está UP, pudimos detectar dispositivos BLE y Bluetooth clásico, y Wi-Fi y Bluetooth pueden usarse a la vez (coexistencia). Es un dispositivo combinado Wi-Fi+Bluetooth; un aviso: al reconectar, de vez en cuando se queda atascada en el WiFi probe y no genera la interfaz `wlx`; basta con reconectarla en otro puerto USB para recuperarla.

**Q3. ¿La AWUS036AXML necesita instalar controladores aparte en Ubuntu 24.04?**
No. El controlador mt7921u está integrado en el kernel 6.17; al conectarla, dmesg muestra que mt7921u renombra la interfaz a `wlx` más la MAC (USB ID `0e8d:7961`), sin DKMS y sin compilar. El controlador no ofrece los modos IBSS ni mesh.

**Q4. ¿La AWUS036AXML puede abrir un AP y admite WPA3?**
Sí, y es su uso más estable. Tanto en 2,4 GHz (802.11n, MCS 10) como en 5 GHz VHT80 (VHT-NSS2) el iPhone se conectó y quedó authorized; con WPA3-SAE y `sae_pwe=0` logramos conectar un iPhone 15 Pro (`MFP: yes`; probado en 2,4 GHz y 6 GHz, no en 5 GHz); con STA+AP en concurrencia, el ping del lado STA fue de unos 4,4 ms. Aunque se clasifica como chip Wi-Fi 6, en nuestra máquina probamos además que la banda de 6 GHz es usable (montamos un AP a 6135 MHz y el iPhone 15 Pro se conectó por 802.11ax y obtuvo IP).

**Q5. ¿En qué se diferencian la AWUS036AXML y la AWUS036AXM, y cuál elegir?**
En esta plataforma el comportamiento Wi-Fi de ambas es idéntico: usan el mismo mt7921u, la inyección falla igual, el monitor recibe igual de flojo, y AP, WPA3 y VIF funcionan por igual. La diferencia es que la AXML lleva además Bluetooth (probado y funcional en nuestra máquina) y que en nuestra máquina la banda de 6 GHz resultó usable, mientras que el Bluetooth y los 6 GHz de la AXM no se probaron por separado en esta ronda. Para AP puro o conexión general cualquiera de las dos sirve; para inyección o handshake, ninguna de las dos.

## Lecturas adicionales

(Los enlaces irán publicándose, en construcción)

- Versión sin Bluetooth del mismo chip: [Prueba práctica de la AWUS036AXM](/es/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- Alternativas con inyección funcional: [Prueba práctica de la AWUS036EACS](/es/blog/awus036eacs-asus-gx10-ubuntu-test-report/), [Prueba práctica de la AWUS036ACH](/es/blog/awus036ach-asus-gx10-ubuntu-test-report/), [Prueba práctica de la AWUS036ACS](/es/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- Artículo temático: [Sin instalar controladores: activar los modos Monitor y AP en Ubuntu (ARM64)](/es/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- Artículo temático: [Conexión WPA3-SAE y práctica de handshake (validado en entorno propio)](/es/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Hub de la tabla global: [Matriz global de 9 tarjetas ALFA en ASUS GX10](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

---

*Unidad de prueba: Yopitek (distribuidor de ALFA Network en Taiwán) | Plataforma de prueba: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Dispositivo de prueba: Apple iPhone 7 Plus (para WPA3 se probó además un iPhone 15 Pro) | Entorno de prueba: Wi-Fi propia de la oficina (SSID YUPITEK). Este artículo es una validación de compatibilidad y capacidades del producto, no un tutorial de operación contra redes de terceros.*
