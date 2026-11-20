---
title: "ALFA AWUS036AX, prueba práctica tarjeta a tarjeta: informe de capacidades Wi-Fi 6 de modo monitor / inyección / AP en ASUS GX10 + Ubuntu 24.04 (Realtek RTL8832BU / rtw89_8852bu)"
slug: awus036ax-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ax-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ax
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - asus-gx10
  - ubuntu-arm64
description: "AWUS036AX (Wi-Fi 6) probado en Ubuntu 24.04 ARM64: integrado en el kernel (sin instalar controlador); modo monitor, inyección 2,4G 96 %, AP 5G VHT80, WPA3-SAE y handshake de extremo a extremo (.22000) superados; no admite IBSS / mesh. Plataforma ASUS GX10, RTL8832BU."
faq:
  - question: "¿Hace falta instalar un controlador para la AWUS036AX en Ubuntu 24.04 ARM64? ¿Qué hago si lsusb muestra 0bda:1a2b?"
    answer: "En el kernel 6.17 probado en este artículo (ASUS GX10), no: el RTL8832BU lo gobierna el controlador integrado rtw89_8852bu, sin compilar ni DKMS. Si lsusb muestra 0bda:1a2b (modo CD-ROM), ejecute sudo usb_modeswitch -v 0bda -p 1a2b -K para pasarlo a WLAN."
  - question: "¿La AWUS036AX admite modo monitor e inyección de paquetes?"
    answer: "Sí. Inyección en 2,4 GHz 29/30 (96 %); en 5 GHz, al indicar el AP uno a uno devuelve Injection is working!; airodump-ng con escaneo por salto de canal de 60 segundos encontró 14 AP y 4 clientes. No admite active monitor, IBSS ni mesh."
  - question: "¿Puede la AWUS036AX capturar un handshake WPA? ¿Y las AXM / AXML con MT7921?"
    answer: "La AX sí: con un AP propio y un iPhone 7 Plus propio, aireplay-ng -0 fuerza la reconexión, airodump-ng captura el M1–M4 completo y hcxpcapngtool genera el .22000. Las AXM / AXML con MT7921 fallan en la inyección en esta plataforma y no pueden hacerlo. Solo en redes propias o autorizadas."
  - question: "¿Puede la AWUS036AX funcionar como punto de acceso (AP)? ¿Admite WPA3?"
    answer: "Sí. hostapd levanta un AP en 2,4G (802.11n) y 5G (VHT 80 MHz); el iPhone 7 Plus se asocia mostrando VHT-NSS2 80 MHz; en WPA3-SAE (ieee80211w=2, sae_pwe=0) el iPhone 15 Pro se asocia en 2.4 GHz con MFP: yes (WPA3 en 5 GHz no se probó)."
  - question: "¿En qué se diferencian la AWUS036AX y la AWUS036AXER? ¿Cuál elegir?"
    answer: "Ambas son RTL8832BU + rtw89_8852bu y comparten matriz de capacidades; la diferencia está en la antena y la recepción: la AXER lleva antena externa y, en la misma tanda de pruebas, su escaneo por salto de canal encontró 63 AP + 12 clientes (la AX, 14 AP + 4 clientes). Para escritorio fijo elija la AX; para largo alcance o máxima recepción, la AXER."
draft: false
---

**Resumen (TL;DR)**: según las pruebas de Yopitek (distribuidor de ALFA Network en Taiwán), la AWUS036AX en ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17) no necesita instalar controlador y funciona en monitor de doble banda; inyección 2,4G 96 %, AP 5G VHT80, captura .22000 de extremo a extremo superada; no admite IBSS / mesh.

> Este artículo es la prueba práctica de compatibilidad y capacidades que Yopitek completó sobre **equipo propio, la Wi-Fi propia de la oficina (SSID `YUPITEK`) y un teléfono de prueba propio**, con la ALFA **AWUS036AX** (Realtek RTL8832BU, Wi-Fi 6 2x2) como objeto de prueba.
> Plataforma de pruebas: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`; dispositivo de referencia Apple iPhone 7 Plus (WPA3 y VIF verificados además con iPhone 15 Pro).
> ⚠️ **Uso legal**: el modo monitor y la inyección solo sobre redes propias o para las que se cuenta con autorización; en modo AP, respete la normativa de radio local. Este artículo no contempla ninguna operación ofensiva contra redes de terceros.

---

## 1. La tarjeta y la plataforma de pruebas

La AWUS036AX es el adaptador USB Wi-Fi 6 de esta generación de ALFA; emplea el chip Realtek RTL8832BU, 2x2 con dos flujos espaciales, y admite doble banda 2,4 GHz y 5 GHz. Dentro de la línea de ALFA, comparte el mismo chip y el mismo controlador con la AWUS036AXER, de antena externa, y la diferencia está en el tipo de antena y la ganancia de recepción; frente a las versiones MediaTek AWUS036AXM / AXML, también Wi-Fi 6, es una línea de chip completamente distinta, con conclusiones de prueba muy diferentes (se detalla en la sección 5).

Esta prueba no habla de las velocidades teóricas de la hoja de especificaciones, solo responde a las tres cosas que más preocupan a la distribución y al terreno de ingeniería: ¿se instala bien en un Linux moderno?, ¿qué capacidades inalámbricas funcionan de verdad?, ¿cuáles son imposibles por naturaleza del controlador y no merece la pena perder tiempo con ellas? La conclusión debe ser reproducible, así que todos los comandos se ejecutaron línea a línea sobre el GX10 real el 2026-11-18, y las «salidas medidas» del texto son extractos reales (con la dirección MAC oculta con `xx`).

Dejemos claros los límites de la prueba: todo se hizo en la oficina propia, contra la red `YUPITEK` propia y teléfonos propios. El modo monitor solo capta paquetes del propio entorno, y la inyección y el handshake solo se dirigen al AP propio y al iPhone propio. El objetivo es verificar «qué puede hacer esta tarjeta en esta máquina», no demostrar ataques contra redes de terceros.

---

## 2. Hardware y controlador (Wi-Fi 6, sin instalación)

La ventaja más tangible de esta generación es: **se reconoce nada más conectarla, sin compilar ni DKMS**. El controlador `rtw89_8852bu` del RTL8832BU ya es un módulo integrado en el kernel 6.17 (in-kernel); el GX10 lo vincula al arrancar, sin necesidad de bajar ningún proyecto out-of-tree de GitHub para compilarlo a mano.

La información del chip y los pasos de verificación son los siguientes. Primero, con `lsusb` confirmamos que la tarjeta se enumera en modo WLAN:

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
```

Lo esperado es ver `ID 0bda:b832 Realtek Semiconductor Corp. 802.11ax WLAN Adapter`. La tarjeta de esta unidad de pruebas apareció directamente en modo WLAN, sin quedar atascada en modo CD-ROM; si la tarjeta que usted recibe muestra `0bda:1a2b`, significa que sigue en modo CD-ROM, y basta con `sudo usb_modeswitch -v 0bda -p 1a2b -K` para pasarla a WLAN.

A continuación, confirmamos la carga del controlador y el firmware:

```bash
sudo dmesg | grep rtw89_8852bu | tail -3
```

Lo que se carga en el equipo real es `rtw89/rtw8852b_fw-1.bin`, firmware version `0.29.29.5`. Tanto el controlador como el firmware vienen integrados con el kernel, sin necesidad de instalar paquetes aparte.

El último paso es ver con claridad **qué modos de interfaz declara admitir** este controlador, lo que determina directamente qué capacidades estarán disponibles y cuáles serán N/A más adelante:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Lo que lista el equipo real es `managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO`. En la lista no aparecen IBSS, mesh point ni active-monitor. No es que falte ajustar una configuración, sino que `rtw89_8852bu` simplemente no implementa estos tres modos; en la sección 4 se marcarán como N/A por este motivo.

---

## 3. Capacidades medidas: modo monitor / inyección / AP / WPA3

Veamos primero una tabla resumen de capacidades; cada celda se corresponde con los extractos de prueba de más abajo:

| Capacidad | 2,4 GHz | 5 GHz | Extracto de la prueba |
|---|---|---|---|
| **Modo monitor** | ✅ fuerte | ✅ fuerte | airodump por salto de canal 60 s encontró **14 AP + 4 clientes** |
| **Inyección** | ✅ **96 %** | ✅ disponible | `aireplay-ng --test` 2,4G 29/30 (96 %); 5G uno a uno `Injection is working!` |
| **Punto de acceso** | ✅ 802.11n (HT) | ✅ **VHT 80 MHz** | iPhone 7 Plus asociado: 2,4G MCS 12, 5G VHT-NSS2 80 MHz |
| **WPA3-SAE** | ✅ | No probado | iPhone 15 Pro asociado, MFP: yes (`sae_pwe=0`); probado solo en 2.4 GHz |
| **Captura de handshake WPA** | ✅ **de extremo a extremo** | — | deauth al iPhone propio → captura del 4-way completo → conversión a `.22000` de hashcat |

**Modo monitor (recepción en escucha) ✅ fuerte.** Tras pasar a modo monitor, tanto 2,4 GHz como 5 GHz reciben gran cantidad de paquetes (unos 100 paquetes / 6 segundos en cada banda). Con `airodump-ng --band abg` y un escaneo por salto de canal de 60 segundos, la prueba encontró 14 AP más 4 clientes; su recepción está al mismo nivel que la de las ACM / ACHM Wi-Fi 5 de ALFA, muy por encima de las dos de MediaTek MT7921 (las AXM / AXML tienen una recepción medida más bien débil). Para prospección in situ e inventario de ocupación de canales, la recepción de esta tarjeta es suficiente.

**Inyección (de paquetes) ✅ disponible, y es también la diferencia clave de la AX frente a las versiones MediaTek.** En 2,4 GHz (ch6), ejecutando `aireplay-ng --test`, la prueba da `29/30: 96%`, `Injection is working!`, con una tasa de respuesta del 96 %. En 5 GHz (ch36), la prueba de difusión puede devolver `Found 0 APs` (los AP modernos no responden a las probe de difusión, lo cual es normal), pero al indicar el BSSID del AP uno a uno devuelve `Injection is working!`, lo que confirma que la inyección en 5 GHz está disponible. En cambio, las MediaTek AXM / AXML, también Wi-Fi 6, **fallan directamente en la inyección** en esta plataforma (causa principal: una regresión de mac80211 chanctx desde el kernel 6.16, a lo que se suma un firmware que bloquea la velocidad de inyección en 1/6 Mbps; no es una limitación del chip en sí); hay que distinguir bien este punto al seleccionar el modelo.

**Punto de acceso ✅ se abre en doble banda, y en 5 GHz alcanza VHT80.** Con hostapd levantamos el AP: en 2,4 GHz con 802.11n (`ieee80211n=1`, HT20), el iPhone 7 Plus se asocia y muestra MCS 12, authorized; en 5 GHz con VHT 80 MHz (`vht_oper_chwidth=1`, `ht_capab=[HT40+]`), el iPhone 7 Plus se asocia y muestra VHT-NSS2 80 MHz, authorized. Ambas bandas sostienen al cliente de forma estable, y el ancho de banda de 80 MHz efectivamente se negocia con éxito.

**WPA3-SAE ✅ (2.4 GHz; 5 GHz no probado).** Cambiando el `wpa_key_mgmt` del AP a `SAE` y `ieee80211w=2`, en la prueba el iPhone 15 Pro se asocia y la MFP (Management Frame Protection) muestra yes. Aquí hay un detalle de compatibilidad: hay que fijar `sae_pwe` en `0` (Hunting-and-Pecking) para que los iPhone antiguos puedan conectarse.

**Captura de handshake WPA ✅ éxito de extremo a extremo.** Sobre la red `YUPITEK` propia y contra el iPhone 7 Plus propio se recorrió el flujo completo: monitor grabando ese canal → `aireplay-ng -0` envía un deauth para forzar la reconexión → `airodump-ng` captura el 4-way handshake completo (M1/M2/M3/M4) → con `hcxpcapngtool` se genera el formato `.22000` de hashcat. Como esta tarjeta tiene inyección disponible, toda la cadena se puede recorrer; las tarjetas cuya inyección falla (como las AXM / AXML) se cortan ya en el paso del deauth. Las herramientas habituales de Kali empleadas en esta cadena de captura de handshake (aircrack-ng, hcxtools) se ejecutan directamente sobre Ubuntu 24.04 ARM64.

---

## 4. Funciones avanzadas y limitaciones (apartados N/A del controlador rtw89)

En esta sección dejamos claro de una vez tanto «las funciones avanzadas que se pueden hacer» como «lo que el controlador es incapaz de hacer por naturaleza», para no perder tiempo en campo.

| Función | Estado | Explicación |
|---|---|---|
| **VIF (STA + AP en paralelo)** | ✅ | la interfaz principal conectada a `YUPITEK` y a la vez una VIF de AP (ch36 VHT80), ambas interfaces en paralelo; ping de 3,2 ms en el lado STA |
| **Captura de handshake WPA** | ✅ de extremo a extremo | captura de M1–M4, `hcxpcapngtool` genera el `.22000` |
| **Active monitor** | **N/A** | `rtw89_8852bu` no dispone de este modo (no está en los supported modes de `iw phy`) |
| **Ad-hoc (IBSS)** | **N/A** | el controlador no lo admite |
| **Mesh (802.11s)** | **N/A** | el controlador no lo admite |
| **Wi-Fi Direct (P2P)** | ⬜ no verificado | el controlador declara admitirlo, pero requiere un segundo equipo; se omite esta vez |

**VIF ✅.** Creamos una interfaz virtual de AP (MAC distinta, unmanage), con la interfaz principal manteniéndose conectada al Wi-Fi y abriendo el AP en el mismo canal. En la prueba, mientras la interfaz principal está conectada a `YUPITEK`, la VIF de AP corre VHT80 en ch36; las dos interfaces funcionan en paralelo, con un ping de 3,2 ms en el lado STA. Es viable para el escenario de «por un lado conectado a Internet, por otro con un punto de acceso de prueba abierto».

**Active monitor / IBSS / Mesh son N/A, no están averiados.** Estos tres modos no aparecen en los supported interface modes del `iw phy info` de la sección 2, lo que significa que el controlador `rtw89_8852bu` simplemente no los implementa. Comandos como `sudo iw dev $IF set type ibss` fallan directamente, y no hay solución: no es algo que un parámetro o el firmware puedan arreglar; para usar estos tres modos hay que cambiar de línea de chip (por ejemplo, las ACM / ACHM con mt76 de MediaTek pueden crear IBSS / mesh en un solo equipo).

**Una limitación a nivel de plataforma que conviene conocer de antemano: hcxdumptool da `failed to arm` en el GX10.** No es un problema exclusivo de la AX. `hcxdumptool 8.x` necesita active-monitor, y como el GX10 lleva una tarjeta de red integrada de tres bandas, al enumerar las tarjetas USB es fácil que la opción `-I` se mapee por error a la phy integrada, de modo que todas las tarjetas USB probadas fallan el arm en esta máquina (la única excepción es el AWUS036EACS en 2.4 GHz). En la práctica, lo recomendable es **usar la suite aircrack-ng** (airodump-ng + aireplay-ng) para la captura; con la inyección disponible de esta tarjeta, toda la cadena se recorre igualmente de extremo a extremo (véase la sección 3).

**Regla de seguridad (común a la plataforma GX10):** nunca ejecute `airmon-ng check kill`, que apagaría NetworkManager y dejaría al GX10 sin conexión externa; al operar, toque solo la interfaz `wlx*`, sin tocar la tarjeta integrada de la línea principal de salida a Internet.

---

## 5. Casos de uso y selección de modelo (punto de acceso Wi-Fi 6, con retorno al Hub)

Convirtamos las conclusiones de la prueba en recomendaciones de selección: **el punto dulce de la AWUS036AX es el escenario de «Wi-Fi 6 + punto de acceso» que además necesita capacidad de inyección.**

| Uso | Idoneidad de la AWUS036AX | Explicación |
|---|---|---|
| Punto de acceso Wi-Fi 6 / acceso de borde | ★ primera elección | 2x2 VHT80 de doble banda, WPA3-SAE disponible |
| Auditoría de inyección + handshake | ★ a la altura | 2,4G 96 %, 5G disponible, captura de extremo a extremo exitosa |
| Máxima recepción / monitor de largo alcance | ○ suficiente, pero la primera elección es la AXER | la AXER, con el mismo chip, lleva antena externa y recibe mejor |
| Experimentos de mesh / IBSS | ✗ no aplicable | el controlador es N/A; elija las ACM / ACHM con mt76 |

**Despliegue típico: como punto de acceso Wi-Fi 6, para que los dispositivos de borde retornen al Hub central.** Usando las capacidades de AP (VHT80) y VIF ya probadas, se despliega el GX10 con esta tarjeta como un punto de acceso Wi-Fi 6; los dispositivos de borde (teléfonos de prueba, sensores IoT) se asocian a él y su tráfico vuelve, a través de la interfaz principal, al Hub central (gateway). La VIF ya demostró en la prueba que «la interfaz principal retorna a la red superior» y «abrir un AP hacia abajo» pueden funcionar en paralelo, con una latencia de 3,2 ms en el lado STA; esta topología se verificó como viable en esta plataforma. Para el tramo de acceso de borde, basta con añadir cifrado moderno con WPA3-SAE.

**A evitar al seleccionar: para usos de inyección / handshake, no elija la AWUS036AXM / AXML.** Aunque estas dos también son Wi-Fi 6 2x2 y el AP se abre, el MediaTek MT7921 **falla en la inyección** en esta plataforma, no puede hacer deauth ni capturar handshake. Si el cliente solo quiere un AP Wi-Fi 6 sencillo o una tarjeta de conexión normal y no toca la inyección en absoluto, las versiones MediaTek son estables y no hay problema; pero en cuanto el uso roce la auditoría inalámbrica, hay que elegir la AX de Realtek (o la AXER de antena externa).

**¿Cómo distinguirla de la AXER, con el mismo chip?** Ambas coinciden en chip, controlador y matriz de capacidades; la AXER es la versión de antena externa, con mejor recepción y monitor de largo alcance (en la misma tanda de pruebas, la AXER encontró por salto de canal 63 AP + 12 clientes). Para escritorio fijo y poca exigencia de antena, elija la AX; para ganar distancia y máxima recepción, vaya a por la AXER.

---

## Preguntas frecuentes (FAQ)

**P: ¿Hace falta instalar un controlador para la AWUS036AX en Ubuntu 24.04 ARM64? ¿Qué hago si lsusb muestra 0bda:1a2b?**
En el kernel 6.17 probado en este artículo (ASUS GX10), no: el RTL8832BU lo gobierna el controlador integrado rtw89_8852bu, sin compilar ni DKMS. Si lsusb muestra `0bda:1a2b` (modo CD-ROM), ejecute `sudo usb_modeswitch -v 0bda -p 1a2b -K` para pasarlo a WLAN.

**P: ¿La AWUS036AX admite modo monitor e inyección de paquetes?**
Sí. Inyección en 2,4 GHz 29/30 (96 %); en 5 GHz, al indicar el AP uno a uno devuelve `Injection is working!`; airodump-ng con escaneo por salto de canal de 60 segundos encontró 14 AP y 4 clientes. No admite active monitor, IBSS ni mesh.

**P: ¿Puede la AWUS036AX capturar un handshake WPA (paquetes de handshake)? ¿Y las AXM / AXML con MT7921?**
La AX sí: con un AP propio y un iPhone 7 Plus propio, `aireplay-ng -0` fuerza la reconexión, `airodump-ng` captura el M1–M4 completo y `hcxpcapngtool` genera el .22000. Las AXM / AXML con MT7921 fallan en la inyección en esta plataforma y no pueden hacerlo. Solo en redes propias o autorizadas.

**P: ¿Puede la AWUS036AX funcionar como punto de acceso (AP)? ¿Admite WPA3?**
Sí. `hostapd` levanta un AP en 2,4G (802.11n) y 5G (VHT 80 MHz); el iPhone 7 Plus se asocia mostrando VHT-NSS2 80 MHz; en WPA3-SAE (ieee80211w=2, sae_pwe=0) el iPhone 15 Pro se asocia en 2.4 GHz con MFP: yes (WPA3 en 5 GHz no se probó).

**P: ¿En qué se diferencian la AWUS036AX y la AWUS036AXER? ¿Cuál elegir?**
Ambas son RTL8832BU + rtw89_8852bu y comparten matriz de capacidades; la diferencia está en la antena y la recepción: la AXER lleva antena externa y, en la misma tanda de pruebas, su escaneo por salto de canal encontró 63 AP + 12 clientes (la AX, 14 AP + 4 clientes). Para escritorio fijo elija la AX; para largo alcance o máxima recepción, la AXER.

---

## 6. Lecturas adicionales

- «Tabla general de capacidades de 9 adaptadores inalámbricos ALFA en ASUS GX10 + Ubuntu ARM64» —— comparación de una vez del modo monitor / inyección / AP / handshake de todos los modelos → [Hub de la tabla general](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Integrado en el kernel: habilitar los modos monitor y AP con el controlador integrado en Ubuntu 24.04 + kernel 6.17](/es/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/) —— flujo de configuración común a rtw88 / rtw89 / mt76
- [AWUS036AXER, prueba práctica tarjeta a tarjeta](/es/blog/awus036axer-asus-gx10-ubuntu-test-report/) —— versión de antena externa con el mismo chip, comparación de recepción y monitor de largo alcance
- [Prueba de la capacidad de captura de handshake WPA3-SAE y compatibilidad de sae_pwe](/es/blog/alfa-wpa3-sae-handshake-capability-arm64/) —— el campo de minas de `sae_pwe` para la conexión de iPhone

---

*Unidad de pruebas: Yopitek (distribuidor de ALFA) — https://www.yupitek.com | Entorno de pruebas: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 | Dispositivo de referencia: Apple iPhone 7 Plus (WPA3 / VIF verificados además con iPhone 15 Pro)*
