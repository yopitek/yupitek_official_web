---
title: "AWUS036ACHM, prueba práctica: capacidades de Monitor, Inyección, AP y WPA3 del MediaTek MT7610U de una sola antena AC600 en ASUS GX10 (ARM64 / Ubuntu 24.04)"
slug: awus036achm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036achm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036achm
  - alfa-network
  - mt7610u
  - mt76x0u
  - wifi-5
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - sae-pwe
  - ubuntu-24-04
  - arm64
description: "El AWUS036ACHM (MT7610U) funciona en Ubuntu 24.04 sin instalar controladores: modo monitor en doble banda disponible, inyección de paquetes en 2.4G del 96–100%; para abrir el AP hay que desactivar 802.11n, y para WPA3 hay que fijar sae_pwe=0 para que se conecten los iPhone antiguos."
faq:
  - question: "¿El AWUS036ACHM necesita instalar controladores en Ubuntu 24.04?"
    answer: "No. El MT7610U lo gestiona el controlador mt76x0u integrado en el kernel; en Ubuntu 24.04 (kernel 6.17) se reconoce nada más conectarlo, sin DKMS y sin firmware adicional; con lsusb se ve el USB ID 0e8d:7610."
  - question: "¿El AWUS036ACHM puede entrar en modo monitor? ¿Cuántos AP detecta?"
    answer: "Sí. Tanto en 2.4GHz como en 5GHz entra en modo monitor; con un escaneo por salto de canal de toda la banda de 120 segundos con airodump-ng detectó 19 AP y 14 clientes, distribuidos en ch1, 2, 5, 6, 36, 149, 157."
  - question: "¿Cuál es la tasa de éxito de inyección de paquetes del AWUS036ACHM? ¿Funciona en 5GHz?"
    answer: "En el canal 6 de 2.4GHz, la tasa de respuesta de inyección por equipo es del 96–100% (aireplay-ng --test, encontró 4 AP). En 5GHz (ch36, ch149) solo se verificó que la inyección por difusión funciona; la prueba por equipo devuelve Found 0 APs y esta vez no se obtuvo un porcentaje, con la causa pendiente de investigar."
  - question: "¿Qué hago si al abrir el AP del AWUS036ACHM el iPhone muestra «No se puede conectar a la red» o «Contraseña incorrecta»?"
    answer: "Primero desactive 802.11n: en el archivo de configuración de hostapd no añada ieee80211n=1 ni ht_capab, use hw_mode=g puro en 2.4GHz y hw_mode=a puro en 5GHz (20 MHz). De lo contrario, hostapd mostrará repetidamente handle_assoc_cb: STA not found; en pantalla parece una contraseña incorrecta, pero en realidad es un fallo de asociación 802.11n."
  - question: "¿Por qué los iPhone antiguos no se conectan al WPA3-SAE del AWUS036ACHM?"
    answer: "Casi siempre es la configuración sae_pwe de hostapd. En las pruebas, con sae_pwe=0 se conectan tanto el iPhone 7 Plus como el iPhone 15 Pro; con sae_pwe=2 el iPhone 7 Plus se asocia correctamente pero el handshake de 4 vías falla y se desconecta, con aspecto de contraseña incorrecta. Use ieee80211w=2 junto con ello y, tras cambiar la configuración, haga que el iPhone olvide primero la red y vuelva a conectarse."
draft: false
---

> Entidad de prueba: Yupitek (distribuidor de ALFA Network en Taiwán) | Plataforma de prueba: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia` | Dispositivo de prueba: iPhone 7 Plus propio (WPA3 también probado con iPhone 15 Pro) | Objetivo de prueba: Wi-Fi propia de la oficina (SSID `YUPITEK`, 2.4G ch5 / 5G ch36, 157).
>
> Este artículo es una verificación de hardware, por parte del distribuidor, de la compatibilidad y los límites de capacidad del producto. Todas las pruebas de Monitor / Inyección / AP / WPA3 se realizaron sobre equipo propio de Yupitek, la Wi-Fi propia de la oficina y un teléfono de prueba propio; se trata de una verificación legítima de capacidades, no se dirige contra ninguna red de terceros ni se ofrecen pasos de operación de ataque. La inyección del texto solo envía probe requests como autocomprobación de capacidad, no envía paquetes de ataque.

## Resumen (TL;DR)

En las pruebas en ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17), la AWUS036ACHM funciona en modo monitor de doble banda, logra una inyección de paquetes del 96–100% en 2.4G (en 5G solo se verificó la inyección broadcast) y monta un punto de acceso en ambas bandas (hay que desactivar 802.11n).

- En Ubuntu 24.04 no hace falta instalar controladores: el MT7610U lo gestiona el mt76x0u integrado en el kernel 6.17; se reconoce nada más conectarlo, sin DKMS y sin firmware adicional.
- Modo monitor en doble banda disponible; inyección de paquetes en 2.4G del 96–100%.
- En 5GHz solo se verificó la inyección por difusión; esta vez no se obtuvo la tasa de respuesta por equipo (causa pendiente de investigar).
- Para abrir el AP hay que desactivar 802.11n; para WPA3 hay que fijar `sae_pwe=0` para que se conecten los iPhone antiguos.
- Una sola antena 1T1R (AC600); su rendimiento y posicionamiento no están al nivel del ACM / ACH 2T2R.

## 1. Esta tarjeta y esta plataforma

El AWUS036ACHM es la tarjeta AC600 de una sola antena de ALFA, con chip MediaTek MT7610U, correspondiente al controlador integrado de Linux `mt76x0u`. Es la versión hermana de un solo flujo del AWUS036ACM (MT7612U, 2T2R): en especificaciones es 1T1R (AC600), con un flujo espacial menos, a cambio de un tamaño más pequeño y de la recepción de larga distancia reconocida por la comunidad. La comunidad morrownr/USB-WiFi la incluye en la lista de recomendadas para Kali y en «The Short List», y la marca con VIF, Active monitor y WPA3 como Yes, Very Long range, un solo flujo e integrado en el kernel.

La conectamos al ASUS GX10 (NVIDIA GB10, 128GB UMA, ARM64) y, sobre Ubuntu 24.04 LTS, kernel 6.17, medimos punto por punto Monitor, Inyección, AP y WPA3-SAE. La conclusión primero: esta tarjeta es utilizable en esta plataforma y sus capacidades en 2.4GHz son además bastante completas. Pero hay dos trampas de compatibilidad que conviene conocer de antemano: para abrir el AP hay que desactivar 802.11n, y para WPA3 hay que fijar `sae_pwe=0`; además, la inyección por equipo en 5GHz esta vez solo se verificó por difusión. La tabla siguiente es un vistazo general:

| Elemento de capacidad | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor (captura lateral) | ✅ | ✅ |
| Inyección | ✅ 96–100% | ⚠️ solo difusión disponible, tasa de respuesta por equipo sin obtener |
| AP | ✅ (requiere 802.11g puro) | ✅ (requiere 802.11a puro, 20 MHz) |
| WPA3-SAE | ✅ (requiere `sae_pwe=0`) | No probado |

> Leyenda: ✅ prueba superada | 🟡 parcial o válido en un solo equipo | ⚠️ con limitaciones | ❌ no admitido o fallido.

## 2. Hardware y controlador (sin instalación)

Tras conectar el ACHM al GX10, el `mt76x0u` integrado en el kernel 6.17 lo reconoce directamente, sin necesidad de DKMS, sin firmware adicional y sin compilar un controlador out-of-tree desde GitHub. Los tres comandos para confirmar la tarjeta de red:

```bash
lsusb | grep 0e8d:7610
# Bus 003 Device 005: ID 0e8d:7610 MediaTek Inc. WiFi

sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cababcd2
```

El nombre de la interfaz se compone con la MAC (`wlx<MAC>`), no cambia al reconectar la tarjeta, por lo que se puede fijar directamente al escribir scripts. Los modos de interfaz que declara `iw phy info` incluyen `managed`, `AP`, `monitor`, `mesh point`, `IBSS`, `P2P-client`, `P2P-GO`, que cubren todos los escenarios que este artículo va a probar.

Las dos reglas de seguridad comunes a la plataforma también aplican al ACHM: primera, nunca ejecute `airmon-ng check kill`, porque cierra NetworkManager y deja al GX10 sin conexión externa; segunda, opere durante todo el proceso solo sobre la interfaz `wlx*`, sin tocar la `wlP9s9` integrada (la línea principal de salida a Internet del GX10). Para entrar en monitor / AP use siempre `iw` junto con `nmcli dev set $IF managed no`, sin tocar la tarjeta de red principal del sistema.

## 3. Capacidades probadas: Monitor / Inyección / AP / WPA3

### 3-1. Monitor (2.4 + 5 GHz) ✅

La captura lateral en ambas bandas es normal. En el canal 6 de 2.4GHz, en 8 segundos se alcanza el límite de captura de 300 paquetes; en 5GHz depende de la actividad de cada frecuencia: ch36 (5180) alcanza 300 en 8 segundos, 5745 captura 254 y 5785 captura 54 (que un canal tenga pocos paquetes suele indicar que en ese momento no hay un AP activo en ese canal, no un problema de la tarjeta).

El escaneo por salto de canal de toda la banda es lo que mejor muestra la capacidad de recepción de una tarjeta de una sola antena:

```bash
sudo timeout -s INT 120 airodump-ng --band abg $IF
```

En la prueba de 120 segundos detectó 19 estaciones base y 14 clientes, distribuidos en ch1/2/5/6/36/149/157. Para una tarjeta AC600 de un solo flujo, esta cobertura es suficiente para servir de fuente de captura estable, y concuerda con la valoración de «Very Long range» que le da la comunidad.

### 3-2. Inyección (2.4 + 5 GHz)

Aquí es donde más se nota la diferencia entre las dos bandas del ACHM, y es también un punto al que prestar especial atención al seleccionar modelo.

La autocomprobación de capacidad con `aireplay-ng --test` en el canal 6 de 2.4GHz da un resultado excelente:

```text
Injection is working!
Found 4 APs
30/30: 100%
```

La tasa de respuesta de las cuatro estaciones base se sitúa en el 96–100%: capacidad de inyección completa.

Pero al pasar a 5GHz (se probaron tanto ch36 como ch149) la cosa cambia:

```text
Injection is working!
Found 0 APs
```

Es decir, la inyección por difusión en 5GHz funciona (el controlador informa `Injection is working!`), pero la tasa de respuesta por equipo de `aireplay-ng --test` es `Found 0 APs` en los dos canales de 5G, y esta vez no se obtuvo un porcentaje. Este es el fenómeno medido con esta tarjeta de una sola antena, el ACHM, en esta plataforma; la causa queda pendiente de investigar y no le añadimos una cifra que no se midió. Siendo honestos: si su uso requiere una inyección por equipo estable en 5GHz, el ACHM esta vez solo verificó una tasa de inyección completa en 2.4GHz.

### 3-3. AP (2.4 + 5 GHz) ✅ — pero hay que desactivar 802.11n

La primera trampa de compatibilidad del ACHM está aquí. Al abrir el AP, en el archivo de configuración de hostapd no añada `ieee80211n=1` ni `ht_capab`: use `hw_mode=g` puro en 2.4GHz y `hw_mode=a` puro en 5GHz (20 MHz). Una configuración mínima funcional de 2.4GHz tiene este aspecto:

```ini
interface=wlx00c0cababcd2
driver=nl80211
ssid=ALFA-TEST-ACHM-24
# 802.11g puro, no añada ieee80211n=1 ni ht_capab
hw_mode=g
channel=6
country_code=TW
wmm_enabled=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=cambie esto por su contraseña de al menos 8 caracteres
```

En la prueba, el iPhone 7 Plus se conectó en ambas bandas: en 2.4GHz se ve `AP-STA-CONNECTED` seguido de `EAPOL-4WAY-HS-COMPLETED`; en 5GHz (ch36, 20 MHz) se midió -71 dBm, rx 54 Mbit, `authorized: yes`.

A la inversa, si el archivo de configuración conserva `ieee80211n=1`, hostapd lanza repetidamente `handle_assoc_cb: STA not found`, en pantalla el iPhone muestra «No se puede conectar a la red» o «Contraseña incorrecta», pero eso en realidad es un fallo de asociación 802.11n, no un problema de contraseña. Basta con quitar 802.11n. El ACHM es una tarjeta de una sola antena; para el AP en 5GHz esta vez se usó 20 MHz, sin probar VHT80.

### 3-4. WPA3-SAE ✅ — pero hay que fijar `sae_pwe=0` (la trampa de compatibilidad más fácil de pisar)

La segunda trampa de compatibilidad del ACHM, y la que más merece tratarse por separado. En hostapd, WPA3-SAE controla con `sae_pwe` el método de derivación del elemento de contraseña (password element): `0` usa solo el Hunting-and-Pecking tradicional, `1` usa solo Hash-to-Element (H2E) y `2` admite ambos a la vez (Hunting-and-Pecking y H2E). La diferencia determina directamente si los iPhone antiguos logran conectarse:

```ini
wpa=2
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
# WPA3 fuerza PMF
ieee80211w=2
# Clave: compatibilidad con endpoints antiguos como el iPhone 7 Plus
sae_pwe=0
sae_password=cambie esto por su contraseña
```

Contraste de la prueba:

- `sae_pwe=0`: el iPhone 15 Pro y el iPhone 7 Plus **se conectan ambos** (`authorized: yes`, `MFP: yes`).
- `sae_pwe=2`: el iPhone 7 Plus **se asocia correctamente pero el handshake de 4 vías falla y se desconecta**, lo que de nuevo parece en apariencia una «contraseña incorrecta»; el iPhone 15 Pro, en cambio, sí se conecta.

La conclusión es directa: para ser compatible con los iPhone antiguos (incluidos modelos de 2016 como el iPhone 7 Plus), hostapd tiene que fijar `sae_pwe=0`. Tras cambiar la configuración, haga que el iPhone «olvide esta red» y vuelva a conectarse, para evitar que un estado de asociación residual provoque un fallo falso. Este punto está marcado en la tabla general de las 9 tarjetas: el campo WPA3 del ACHM lleva un «✅*» con asterisco de forma especial.

## 4. Avanzado y límites

Primero una tabla que resume la cobertura y el estado completos del ACHM en esta ronda, y luego los párrafos siguientes desarrollan los puntos clave:

| Función | Estado | Puntos clave de esta prueba |
|---|---|---|
| Monitor (2.4 + 5 GHz) | ✅ | Salto de canal 120 s, detectó 19 AP + 14 clientes |
| Inyección 2.4 GHz | ✅ | Tasa de respuesta 96–100% |
| Inyección 5 GHz | ⚠️ | Difusión disponible, tasa de respuesta por equipo sin obtener |
| AP (2.4 + 5 GHz) | ✅ | iPhone conecta en ambas bandas, hay que desactivar 802.11n |
| WPA3-SAE | ✅* | Probado en 2.4 GHz (5 GHz no probado); iPhone nuevos y antiguos conectan, hay que fijar `sae_pwe=0` |
| VIF (STA+AP, AP+monitor) | ✅ | Navegar y servir de punto de acceso a la vez, descarga 198 Mbit/s |
| Captura de handshake WPA | ✅ extremo a extremo (.22000, en 5 GHz ch36) | Deauth a nuestro iPhone, captura del 4-way completo M1–M4, exportación de `.22000` para hashcat |
| Active monitor | 🟡 | Captura configurable, ACK sin verificar |
| Ad-hoc (IBSS) | 🟡 | Se crea en local, sin interconexión con un segundo equipo |
| Mesh (802.11s) | 🟡 | Se une en local, sin peer link |
| Wi-Fi Direct (P2P) | ⬜ | Requiere un segundo equipo, omitido |

> ✅* = WPA3-SAE disponible pero requiere `sae_pwe=0`; véase la sección 3-4.

**VIF (interfaces virtuales, mismo canal, máximo 2 interfaces).** El ACHM admite dividir una misma tarjeta en varias interfaces funcionando a la vez, siempre que cada VIF use una MAC distinta, la VIF de AP no se deje gestionar a NetworkManager y todas las VIF estén en el mismo canal; el ACHM, además, necesita desactivar 802.11n en el AP. Se probaron las dos combinaciones:

- **STA + AP (navegar y servir de punto de acceso a la vez)**: mientras el iPhone 7 Plus se conecta al AP (-66 dBm, authorized), la interfaz principal se conecta a YUPITEK, con ping 30/30, avg 3.2 ms y descarga de 198 Mbit/s.
- **AP + Monitor**: captura con el AP abierto; en 8 segundos captura 300 frames, entre ellos 46 beacons del AP propio.

**Captura de handshake.** El ACHM completó la cadena de extremo a extremo en 5 GHz (ch36): deauth a nuestro iPhone, captura del 4-way completo (M1–M4) y exportación de un `.22000` para hashcat. Es una de las 7 de 9 tarjetas que completaron el extremo a extremo (ACM, ACHM, ACH, ACS, EACS, AX, AXER). La tasa de respuesta por equipo de inyección en 5GHz (`aireplay-ng --test`) sigue sin obtenerse.

**mesh / IBSS (se crea en local).** Este es el punto diferencial de la familia mt76 frente a los Realtek rtw88/rtw89. El IBSS (Ad-hoc) hace `Joined IBSS` en unos 9 segundos y puede emitir beacon; el Mesh (802.11s) puede entrar en `type mesh point` y emitir mesh beacon. Ambos, esta vez, se establecen en local, sin interconexión con un segundo equipo (omitido por falta de un segundo equipo), por lo que se marcan 🟡. Las tarjetas Realtek rtw88/rtw89 (como el AWUS036ACH), aunque en esta plataforma pueden crear un IBSS en local, no admiten mesh 802.11s, así que para hacer experimentos de mesh 802.11s, el ACM y el ACHM, estas dos tarjetas mt76, son de las pocas opciones.

**Active monitor 🟡.** Configurable, captura normal, pero el comportamiento de respuesta ACK requiere un segundo equipo para verificarse y esta vez no se verificó.

**Herramientas de Kali (a nivel de plataforma, comunes a otras tarjetas).** `airmon-ng`, `kismet`, `bettercap`, `wifite` (versión git) y Wireshark/tshark pueden usar el ACHM como fuente; solo `hcxdumptool` devuelve en esta plataforma `failed to arm interface` (salvo el AWUS036EACS en 2.4 GHz; el controlador integrado no admite active-monitor); para capturar, use `airodump-ng` junto con la suite aircrack-ng. En ARM64 hay que tener en cuenta además: `aircrack-ng` a menudo carece de paquete precompilado y hay que compilarlo desde el código fuente, y para `wifite` se recomienda la versión de GitHub para esquivar el conflicto de dependencias de apt.

## 5. Escenarios de uso y selección de modelo (vuelta al Hub)

Al situar el ACHM de nuevo en el contexto de selección de las 9 tarjetas, su posición queda clara:

**Adecuado para**

- **Experimentos de mesh (802.11s)**: el controlador mt76 puede crear mesh 802.11s (e IBSS) en local; las tarjetas Realtek pueden crear un IBSS en local, pero no llegan al mesh 802.11s.
- **Captura de monitor de un solo flujo a larga distancia**: salto de canal 120 s, detectó 19 AP + 14 clientes, la comunidad lo valora como Very Long range.
- **Inyección en 2.4GHz, y AP / punto de acceso WPA3**: inyección en 2.4G del 96–100%, y con `sae_pwe=0` bien configurado los iPhone nuevos y antiguos se conectan en WPA3.

**A tener en cuenta (límites honestos)**

- La inyección por equipo en 5GHz esta vez solo se verificó por difusión, sin porcentaje.
- Para abrir el AP hay que desactivar 802.11n y para WPA3 hay que fijar `sae_pwe=0`; cualquiera de los dos mal ajustado hará que el iPhone antiguo «parezca tener una contraseña incorrecta».
- Una sola antena 1T1R; su rendimiento y posicionamiento no están al nivel del ACM / ACH 2T2R.

**Guía de selección**: si su necesidad central es inyección estable en ambas bandas más handshake de extremo a extremo, dentro de las 9 tarjetas el AWUS036EACS / AWUS036ACH / AWUS036ACS son más adecuados; si quiere Wi-Fi 6 + punto de acceso AP, mire el AWUS036AX / AWUS036AXER; si lo suyo son experimentos de mesh / IBSS en un solo equipo o captura de larga distancia, el ACHM (o su hermana 2T2R, el ACM) es la herramienta correcta. Un último aviso para evitar trampas: para usos de inyección / handshake no elija el AWUS036AXM / AXML, porque la inyección de sus MT7921 falla en esta plataforma.

Para la matriz completa de los 9 modelos de hardware, controlador, Monitor / Inyección / AP / WPA3 y la evaluación de selección según el uso, véase la tabla general del Hub: [9 adaptadores inalámbricos ALFA, matriz general de pruebas en ARM64 / GX10](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Preguntas frecuentes (FAQ)

**P: ¿El AWUS036ACHM necesita instalar controladores en Ubuntu 24.04?**
No. El MT7610U lo gestiona el controlador mt76x0u integrado en el kernel; en Ubuntu 24.04 (kernel 6.17) se reconoce nada más conectarlo, sin DKMS y sin firmware adicional; con lsusb se ve el USB ID 0e8d:7610.

**P: ¿El AWUS036ACHM puede entrar en modo monitor? ¿Cuántos AP detecta?**
Sí. Tanto en 2.4GHz como en 5GHz entra en modo monitor; con un escaneo por salto de canal de toda la banda de 120 segundos con airodump-ng detectó 19 AP y 14 clientes, distribuidos en ch1, 2, 5, 6, 36, 149, 157.

**P: ¿Cuál es la tasa de éxito de inyección de paquetes del AWUS036ACHM? ¿Funciona en 5GHz?**
En el canal 6 de 2.4GHz, la tasa de respuesta de inyección por equipo es del 96–100% (aireplay-ng --test, encontró 4 AP). En 5GHz (ch36, ch149) solo se verificó que la inyección por difusión funciona; la prueba por equipo devuelve Found 0 APs y esta vez no se obtuvo un porcentaje, con la causa pendiente de investigar.

**P: ¿Qué hago si al abrir el AP del AWUS036ACHM el iPhone muestra «No se puede conectar a la red» o «Contraseña incorrecta»?**
Primero desactive 802.11n: en el archivo de configuración de hostapd no añada ieee80211n=1 ni ht_capab, use hw_mode=g puro en 2.4GHz y hw_mode=a puro en 5GHz (20 MHz). De lo contrario, hostapd mostrará repetidamente handle_assoc_cb: STA not found; en pantalla parece una contraseña incorrecta, pero en realidad es un fallo de asociación 802.11n.

**P: ¿Por qué los iPhone antiguos no se conectan al WPA3-SAE del AWUS036ACHM?**
Casi siempre es la configuración sae_pwe de hostapd. En las pruebas, con sae_pwe=0 se conectan tanto el iPhone 7 Plus como el iPhone 15 Pro; con sae_pwe=2 el iPhone 7 Plus se asocia correctamente pero el handshake de 4 vías falla y se desconecta, con aspecto de contraseña incorrecta. Use ieee80211w=2 junto con ello y, tras cambiar la configuración, haga que el iPhone olvide primero la red y vuelva a conectarse.

## 6. Lecturas adicionales

- [Tabla general del Hub] Matriz completa de Monitor, Inyección y AP de los 9 adaptadores inalámbricos ALFA en ASUS GX10 (ARM64 / Ubuntu 24.04) y evaluación de selección → [/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Modelo hermano] AWUS036ACM (MT7612U / 2T2R), prueba práctica — enlace interno pendiente (placeholder)
- [Tutorial de plataforma] Sin instalar controladores: activar Monitor y AP de los adaptadores ALFA con el controlador integrado en Ubuntu 24.04 + kernel 6.17 — enlace interno pendiente (placeholder)
- [Monográfico] Capacidad de captura de handshake en la era WPA3-SAE y las trampas de compatibilidad de `sae_pwe` — enlace interno pendiente (placeholder)

---

*Entidad de prueba: Yupitek (distribuidor de ALFA Network en Taiwán) — https://www.yupitek.com | Entorno de prueba: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Dispositivo de prueba: Apple iPhone 7 Plus (WPA3 también probado con iPhone 15 Pro). Datos tomados de los informes de pruebas sobre hardware real del 2026-11-16 al 11-18; no se dirige contra ninguna red de terceros ni se ofrecen pasos de operación de ataque.*
