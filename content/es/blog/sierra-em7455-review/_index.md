---
title: "Reseña completa del Sierra EM7455: por qué es la tarjeta Sierra favorita de makers y laboratorios"
description: "Reseña completa del EM7455: especificaciones, diferencias con el EM7430, configuración en OpenWrt/Linux, compatibilidad con Dell/Lenovo. Información técnica recopilada por Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em7455", "lte-a", "cat-6", "openwrt", "linux", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM7455_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "¿El EM7455 admite 5G?"
    answer: "No. Es un módulo LTE-A Cat 6 con una velocidad máxima de 300 Mbps. Si necesita 5G, debe considerar el EM9190 o el EM9191."
  - question: "¿El EM7455 funciona en nuestra región?"
    answer: "Puede usarse con los operadores principales de la región, pero la señal real y las bandas admitidas dependen de la ubicación de las estaciones base; le recomendamos confirmar la compatibilidad entre su zona y su operador antes de realizar el pedido."
  - question: "¿Cuál es la diferencia entre el EM7455 y el MC7455?"
    answer: "Ambos usan el chipset Qualcomm MDM9230, con especificaciones completamente idénticas. La única diferencia es el formato externo: el EM7455 usa M.2 y el MC7455 usa mPCIe. La elección depende únicamente de la ranura de su dispositivo."
  - question: "¿Cuál es la diferencia entre el EM7455 y el EM7430?"
    answer: "Usan el mismo chipset MDM9230 y las especificaciones principales son iguales. La diferencia clave está en las bandas: el EM7455 cubre las bandas de América y EMEA, mientras que el EM7430 cubre las bandas de Asia-Pacífico."
  - question: "¿El Dell DW5811e es un EM7455?"
    answer: "Sí. El DW5811e es la versión con la marca de Dell del EM7455, con el mismo chipset Qualcomm MDM9230 en su interior."
---

# Reseña completa del Sierra EM7455: por qué es la tarjeta Sierra favorita de makers y laboratorios

Si usted usa Raspberry Pi con OpenWrt, o quiere actualizar los equipos del laboratorio a conectividad 4G, seguro que ha oído hablar de la legendaria tarjeta Sierra EM7455. Es un módulo celular LTE-A Cat 6 en formato M.2 de Sierra Wireless, equipado con el chipset Qualcomm MDM9230, que admite hasta 300 Mbps de descarga y 50 Mbps de subida, e incluye posicionamiento GNSS integrado. Su temperatura de funcionamiento soporta incluso entornos extremos de -40°C a +85°C.

Este artículo ha sido recopilado por Yupitek para explicarle por qué este módulo 4G LTE-Advanced Cat 6 en formato M.2 B-Key es tan popular, y cómo dejar listos el controlador y la configuración en sistemas Linux.

> Enlace al producto: [Página del EM7455 en Yupitek](/es/products/sierra/em7455/) | Hoja de especificaciones oficial: [AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## Tabla de especificaciones completa del EM7455: los datos técnicos de un vistazo

Las cifras siguientes se han tomado de la hoja de especificaciones oficial de Sierra Wireless. Como siempre decimos, si va a hacer un pedido real para un proyecto, le recomendamos solicitarnos primero la versión más reciente de los documentos oficiales para comparar, especialmente los elementos que pueden cambiar, como bandas o versiones de firmware.

| Elemento | Especificación |
|---|---|
| **Modelo** | AirPrime EM7455 |
| **Estándar celular** | LTE-A Cat 6 |
| **Chipset** | Qualcomm MDM9230 (Snapdragon X7 LTE) |
| **Pico de descarga** | 300 Mbps (LTE-A, 2×CA) |
| **Pico de subida** | 50 Mbps (LTE-A) |
| **Agregación de portadoras** | 2×CA (admite varias combinaciones; consulte la referencia oficial de comandos AT) |
| **Formato** | PCI Express M.2 B-Key (52 pines) |
| **Dimensiones** | 42 × 30 × 2.3 mm |
| **Temperatura de funcionamiento** | -40°C ~ +85°C (grado industrial) |
| **GNSS** | GPS, GLONASS, BeiDou, Galileo |
| **Interfaz de comunicación** | USB 3.0 / USB 2.0 High Speed |
| **Bandas LTE** | Cubre las bandas principales de América y EMEA (Europa/Medio Oriente/África); para la lista detallada, consulte la hoja de especificaciones oficial más reciente |
| **Bandas 3G WCDMA** | Consulte la hoja de especificaciones oficial más reciente |
| **VID:PID genérico** | `1199:9079` (EM7455, versión general) |
| **VID:PID del Dell DW5811e** | `413c:81b6` (versión de marca; verifique con `lsusb` en su equipo real) |
| **Controlador Linux** | `qcserial`, `qmi_wwan`, `cdc_mbim` (incluidos en la mayoría de las distribuciones principales) |
| **Firmware genérico** | Use la versión más reciente del sitio oficial source.sierrawireless.com |
| **Certificaciones de operadores** | Varían según la región (p. ej., AT&T, Verizon, Vodafone); consulte la lista más reciente |

---

## ¿Para qué proyectos es adecuado el EM7455?

**En resumen, el EM7455 es la solución ideal para estas tres aplicaciones: (1) montar su propio router 4G LTE con sistemas de código abierto (como OpenWrt o ROOter), (2) actualizar la tarjeta WWAN de laptops Dell o Lenovo, y (3) gateways IoT o seguimiento vehicular en laboratorios de automatización industrial.**

Su mayor ventaja es que los controladores Linux están muy maduros, hay muchísimos recursos de aprendizaje en la comunidad y cubre un amplio rango de bandas.

### Si usted es maker o estudiante trabajando en un proyecto

| Aplicación | Cómo montarla | Por qué elegirla |
|---|---|---|
| Router 4G con Raspberry Pi | Raspberry Pi 4/5 + placa M.2 a USB + OpenWrt / ROOter | Compatibilidad muy estable en la comunidad OpenWrt, y el paquete uqmi es fácil de usar |
| Actualizar router GL.iNet | GL-MT1300 / GL-AR750S + adaptador USB | En Internet encontrará discusiones sobre la configuración `create_connect.sh` de ROOter que puede aprovechar |
| Punto de acceso LTE portátil para exteriores | Alimentación por batería + adaptador USB + router pequeño | Bajo calor y buena disipación, ideal para seguimiento de objetos al aire libre |

### Si es un proyecto empresarial o una aplicación industrial

| Aplicación | Cómo montarla | Por qué elegirla |
|---|---|---|
| Router industrial | Gateway industrial con ranura M.2 (p. ej., Advantech) | Robusto, el amplio rango de temperatura de -40 a 85°C da confianza y tiene bandas suficientes |
| Telemetría vehicular | Gateway de vehículo + antena GNSS | Funciones de posicionamiento integradas como GPS/GLONASS; conectividad y geolocalización con una sola tarjeta |
| Actualización WWAN de laptop | Serie Dell Latitude / Lenovo ThinkPad | Se inserta directamente en M.2 B-Key; muy alta probabilidad de funcionar al instante en Linux |
| WAN de respaldo | Respaldo WAN dual con OpenWrt / pfSense | Admite modos duales QMI/MBIM (aunque el soporte de pfSense no es fiable; recomendamos OpenWrt) |

---

## ¿Cuál es la diferencia real entre el EM7455 y el EM7430?

Es una pregunta muy frecuente. En realidad, **el EM7455 y el EM7430 usan exactamente el mismo chipset Qualcomm MDM9230, por lo que las especificaciones principales (como Cat 6, 300/50 Mbps, 2×CA, GNSS) son idénticas. La mayor diferencia es que «están orientados a bandas de mercados distintos»**. El EM7455 está pensado principalmente para América y Europa/Medio Oriente/África (EMEA), mientras que el EM7430 está pensado principalmente para la región Asia-Pacífico (APAC).

| Elemento | EM7455 | EM7430 |
|---|---|---|
| **Chipset** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **Estándar celular** | LTE-A Cat 6 | LTE-A Cat 6 |
| **Pico de descarga** | 300 Mbps | 300 Mbps |
| **Pico de subida** | 50 Mbps | 50 Mbps |
| **Agregación de portadoras** | 2×CA | 2×CA |
| **Formato** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **Región objetivo** | América, EMEA | Asia-Pacífico (APAC) |

**Consejo rápido de selección**: si la SIM de su proyecto o dispositivo se basa principalmente en Norteamérica o Europa, elija el **EM7455**; si está en la región Asia-Pacífico (como Taiwán, Japón o Australia), en teoría el **EM7430** es más adecuado. No obstante, dado que la configuración de bandas de los operadores de su región es particular, lo mejor es consultarnos antes de pedir para confirmar qué tarjeta se adapta mejor a su operador.

---

## EM7455 vs MC7455: el mismo chipset, solo cambia la forma de los pines

Como ya mencionamos, el EM7455 (M.2) y el MC7455 (mPCIe) usan el mismo Qualcomm MDM9230 y sus especificaciones eléctricas son completamente iguales. La única diferencia es la «piel» (el formato):

| Elemento | EM7455 | MC7455 |
|---|---|---|
| **Formato** | M.2 (B-Key) | Mini PCIe (mPCIe) |
| **Dimensiones** | 42 × 30 × 2.3 mm | 51 × 30 × 3.5 mm |
| **Dispositivos adecuados** | Ranura WWAN de laptop, placas de desarrollo modernas | Ranuras mPCIe de equipos industriales antiguos |
| **VID:PID genérico** | `1199:9079` | `1199:9071` |

**Esta decisión es sencilla: elija la tarjeta según la forma de la ranura de su dispositivo.** Y si se equivoca, siempre puede comprar una placa adaptadora (M.2 a mPCIe o a la inversa) para resolverlo.

---

## ¿Cómo configurarla en Linux? (válido para Ubuntu / Debian / Linux Mint)

El EM7455 tiene un soporte excelente en los sistemas Linux más comunes. A continuación compartimos los pasos básicos de configuración que usa la comunidad. Recuerde que la versión del sistema operativo o del kernel varía en cada máquina; le recomendamos probar primero en un equipo de test y no directamente en un entorno de producción.

### Paso 1: comprobar que el hardware se detecta

```bash
lsusb | grep -i sierra
# Debería ver una salida similar a esta: Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### Paso 2: instalar las herramientas necesarias

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### Paso 3: cambiar el modo USB a QMI

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# Verifique si el cambio de modo se realizó correctamente
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# Debería ver: USB composition 6: DM, NMEA, AT, QMI
```

> Si algún operador específico exige el modo MBIM, puede consultar el comando `AT!USBCOMP` y usar `mbimcli` para conectarse.

### Paso 4: desbloquear la autenticación FCC

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# Si usa ModemManager y quiere la automatización completa:
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### Paso 5: conectarse con NetworkManager

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn 'YOUR_APN'
sudo nmcli connection up 'EM7455 LTE'
```

### Paso 6: conexión QMI manual (para un diagnóstico avanzado)

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='YOUR_APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## Si usa OpenWrt, puede configurar QMI así

El EM7455 tiene muy buena reputación en la comunidad OpenWrt. Si tiene un router con OpenWrt, puede seguir este método de configuración QMI.

### Instalar los paquetes necesarios

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### Editar el archivo de configuración de red

Abra `/etc/config/network` y añada esta configuración de interfaz:

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'YOUR_APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### Reiniciar la red

```bash
/etc/init.d/network restart
```

Si prefiere usar el ratón (interfaz web LUCI): vaya a «Red» → «Interfaces» → añada una nueva interfaz, elija el protocolo «QMI», el dispositivo `/dev/cdc-wdm0`, introduzca su APN y listo.

> Consejo: si es usuario de Raspberry Pi, le recomendamos encarecidamente probar ROOter (un firmware basado en OpenWrt especializado en routing 4G/5G), que incluye muchos enganches de configuración ya preparados.

---

## Compatibilidad con laptops de marca: Dell y Lenovo

### Laptops Dell (la tarjeta llamada DW5811e es esta)

En Internet se ve con frecuencia el Dell DW5811e: en realidad es la versión con la marca de Dell del EM7455 (la VID cambia a `413c` y la PID a `81b6`), y el chipset interior es exactamente el mismo MDM9230. La mayoría de los controladores `qmi_wwan` de Linux ya lo reconocen desde hace tiempo.

```bash
lsusb | grep 413c
# Debería ver una salida similar a esta: Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

La buena noticia es que, según las discusiones de la comunidad, la mayoría de las laptops Dell (como Latitude, Precision, etc.) no suelen tener una molesta lista blanca de BIOS bloqueada, así que a menudo se puede insertar la tarjeta y usarla directamente.

### Laptops Lenovo (la molesta lista blanca)

Si usa un Lenovo ThinkPad, tenga cuidado. Lenovo a veces configura una lista blanca en el BIOS que solo permite tarjetas con la FRU original de Lenovo. Algunos expertos de los foros han compartido comandos AT para sortear la restricción, para los que quieran asumir el reto:

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **Advertencia: estos comandos provienen de foros; si se ejecutan incorrectamente pueden dejar la tarjeta inservible.** Si usted no es del tipo que disfruta desarmando hardware y asumiendo riesgos, le recomendamos consultarnos antes de pedir si existe una alternativa más segura.

---

## ¿Qué plataformas admite? Una tabla para verlo todo

| Su plataforma | Nivel de soporte | Método de conexión | Notas |
|---|---|---|---|
| Raspberry Pi + OpenWrt | ✅✅ Muy estable, muchos tutoriales | QMI / MBIM | Necesitará comprar una placa pequeña M.2 a USB |
| Raspberry Pi + ROOter | ✅✅ | QMI | Muy recomendado para usuarios de Raspberry Pi |
| Ubuntu / Debian | ✅✅ | ModemManager / QMI | Probabilidad muy alta de funcionar al instante |
| DD-WRT | ⚠️ Depende de la suerte | QMI / PPP | Hay pocas discusiones; no lo recomendamos para principiantes |
| pfSense | ⚠️ Poco fiable | QMI / PPP | Recomendamos evaluar migrar a OpenWrt para evitar dolores de cabeza |
| Laptops Dell | ✅ | QMI / MBIM | Linux suele detectarlas sin problema |
| Laptops Lenovo | ⚠️ Puede requerir trabajo | QMI | Cuidado con la lista blanca del BIOS; comandos al azar pueden dañar la tarjeta |

---

## ¿Dónde encontrar más recursos?

Si se atasca en su proyecto, puede buscar en estas comunidades de código abierto:

- **GitHub de danielewood**: scripts y discusiones muy completos sobre EM7455/MC7455.
- **Gentoo Wiki**: los expertos de Linux han recopilado allí una resolución de problemas muy detallada.
- **OpenWrt LTE Wiki**: la documentación oficial, imprescindible antes de configurar la red.

## Preguntas frecuentes (FAQ)

{{< faq >}}

---

## ¿Quiere comprar para su laboratorio? Estamos a su disposición

Este artículo ha sido recopilado por el equipo de ingeniería de Yupitek. Ya sea un proyecto universitario, un plan de laboratorio o una compra en volumen de EM7455 u otros módulos Sierra para su empresa, ¡puede consultarnos!

- **Vea esta tarjeta**: [https://yupitek.com/es/products/sierra/em7455/](/es/products/sierra/em7455/)
- **Vea todos los modelos Sierra**: [https://yupitek.com/es/products/sierra/](/es/products/sierra/)
- **Escríbanos**: sales@yupitek.com
