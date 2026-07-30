---
title: "Revisión completa de la EM7455: por qué es la tarjeta Sierra favorita de makers e ingenieros"
date: 2026-07-30
slug: "em7455-review-guide"
tags:
  - em7455
  - sierra-wireless
  - lte-a
  - cat6
  - m2
  - gnss
  - openwrt
  - linux
categories:
  - Reseñas de productos
series:
  - sierra-wireless-selection
series_order: 2
description: "Revisión completa de la EM7455: especificaciones, diferencias con la EM7430, configuración en OpenWrt/Linux, compatibilidad con Dell/Lenovo. Proporcionado por Yupitek."
author: "yupitek"
draft: false
faq:
  - question: "¿La EM7455 es compatible con 5G?"
    answer: "No. La EM7455 es un módem LTE-A Cat 6 con un máximo de 300 Mbps. Si necesita 5G (Sub-6 o mmWave), puede consultar la EM9190 (Sub-6) o la EM9191 (Sub-6 + mmWave)."
  - question: "¿Se puede usar la EM7455 en Latinoamérica?"
    answer: "Por lo general, puede usarse con tarjetas SIM de los operadores móviles principales. El rendimiento real de la señal y las bandas disponibles dependen de la ubicación de la estación base, la planificación de red del operador y la compatibilidad con agregación de portadoras. Le recomendamos que se comunique con nosotros antes de realizar su pedido para confirmar la compatibilidad con su región y operador."
  - question: "¿Cuál es la diferencia entre la EM7455 y la MC7455?"
    answer: "El chip central es el mismo, Qualcomm MDM9230, y las especificaciones son idénticas. La única diferencia es el encapsulado: la EM7455 usa M.2, mientras que la MC7455 usa mPCIe. La elección depende únicamente del tipo de conector de su dispositivo."
  - question: "¿Cuál es la diferencia entre la EM7455 y la EM7430?"
    answer: "Utilizan el mismo chip MDM9230 y las especificaciones principales son idénticas. La diferencia principal radica en la distribución de bandas objetivo: la EM7455 cubre principalmente las bandas de América y EMEA, mientras que la EM7430 cubre las bandas de Asia-Pacífico. Para obtener la lista completa de bandas, consulte con nosotros para confirmar la ficha técnica oficial más reciente."
  - question: "¿La DW5811e de Dell es lo mismo que la EM7455?"
    answer: "Sí, la DW5811e es la versión de Dell de la EM7455, ambas utilizan el mismo chip Qualcomm MDM9230. Según los reportes de la comunidad de usuarios de Dell, la mayoría de las laptops Dell no tienen lista blanca de BIOS, aunque le recomendamos verificar según el modelo específico de su equipo."
---
La EM7455 es un módulo celular LTE-A Cat 6 con conector M.2 de Sierra Wireless, basado en el chip Qualcomm MDM9230, compatible con descargas de hasta 300 Mbps y subidas de 50 Mbps, con GNSS integrado y un rango de temperatura operativa de -40°C a +85°C. Esta revisión es proporcionada por Yupitek con análisis de especificaciones y referencias de configuración.

El Sierra Wireless EM7455 es un módulo 4G LTE-Advanced Cat 6 con encapsulado M.2 B-Key, ampliamente utilizado en routers OpenWrt, estaciones base móviles Raspberry Pi, puertas de enlace industriales y WWAN en laptops comerciales. Los pasos de configuración siguientes son un resumen de los procedimientos comunes de la comunidad y la documentación oficial; verifique los comandos según su versión del sistema operativo y versión de firmware antes de ejecutarlos, y se recomienda realizar una copia de seguridad de la configuración actual antes de comenzar.

> Enlace del producto: [EM7455 — Página de producto Yupitek](https://yupitek.com/zh-tw/products/sierra/em7455/) | Ficha técnica oficial: [AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## Tabla de especificaciones completa de la EM7455

Las siguientes cifras están recopiladas de las especificaciones oficiales de Sierra Wireless y fuentes públicas. Le recomendamos solicitar los documentos oficiales más recientes para una revisión detallada antes de realizar su pedido, especialmente las bandas y versiones de firmware, que pueden cambiar con el tiempo.

| Elemento | Especificación |
|---|---|
| **Modelo** | AirPrime EM7455 |
| **Estándar celular** | LTE-A Cat 6 |
| **Conjunto de chips** | Qualcomm MDM9230 (Snapdragon X7 LTE) |
| **Pico de descarga** | 300 Mbps (LTE-A, 2×CA) |
| **Pico de subida** | 50 Mbps (LTE-A) |
| **Agregación de portadoras** | 2×CA (admite múltiples combinaciones; consulte la referencia oficial de comandos AT) |
| **Encapsulado** | PCI Express M.2 B-Key (52-pin) |
| **Dimensiones** | 42 × 30 × 2.3 mm |
| **Temperatura operativa** | -40°C ~ +85°C (grado industrial) |
| **GNSS** | GPS, GLONASS, BeiDou, Galileo |
| **Interfaz de comunicación** | USB 3.0 / USB 2.0 High Speed |
| **Bandas LTE** | Cubre las bandas principales de América y EMEA (Europa/Oriente Medio/África). Para la lista completa de bandas, consulte con nosotros para obtener la ficha técnica oficial más reciente |
| **Bandas 3G WCDMA** | Consulte con nosotros para confirmar la ficha técnica oficial más reciente |
| **VID:PID genérico** | `1199:9079` (EM7455, versión estándar) |
| **Dell DW5811e VID:PID** | `413c:81b6` (versión de marca; verifique con `lsusb` en su equipo) |
| **Controladores Linux** | `qcserial`, `qmi_wwan`, `cdc_mbim` (incluidos en las principales distribuciones; consulte la documentación de su distribución para la versión mínima de kernel) |
| **Firmware genérico** | Consulte la versión más reciente en source.sierrawireless.com oficial. No fijamos un número de versión específico para evitar información desactualizada |
| **Certificaciones de operadores** | Sujetas a cambios según el operador y la región (como AT&T, Verizon, T-Mobile, Bell, Rogers, Telus, Vodafone, etc.). Consulte con nosotros para confirmar la lista de certificaciones más reciente en su región |

---

## ¿Para qué usos es adecuada la EM7455?

**La EM7455 es ideal para tres usos principales: (1) construir routers 4G LTE personalizados (OpenWrt / ROOter), (2) actualizar WWAN en laptops (Dell / Lenovo), (3) puertas de enlace industriales para IoT y telemática vehicular.** Sus ventajas principales son la madurez de los controladores Linux, la abundancia de recursos comunitarios y la amplia cobertura de bandas de América y EMEA.

### Escenarios para makers

| Aplicación | Equipo recomendado | Motivo |
|---|---|---|
| Router Raspberry Pi 4G | Raspberry Pi 4/5 + placa adaptadora M.2→USB + OpenWrt / ROOter | La EM7455 tiene buena compatibilidad en la comunidad OpenWrt con el paquete maduro uqmi |
| Actualización de router GL.iNet | GL-MT1300 / GL-AR750S + adaptador USB | La comunidad tiene discusiones sobre el enlace con ROOter y `create_connect.sh` como referencia |
| Punto de acceso LTE portátil para exteriores | Alimentación por batería + adaptador USB + router pequeño | La EM7455 genera poco calor y disipa bien, adecuada para rastreo de objetos |

### Escenarios empresariales / industriales

| Aplicación | Equipo recomendado | Motivo |
|---|---|---|
| Routers industriales | Puerta de enlace industrial con conector M.2 (como Advantech, Cincoze) | Amplio rango de temperatura -40~85°C y cobertura extensa de bandas |
| Telemática vehicular | Puerta de enlace vehicular + antena GNSS | GPS/GLONASS/BeiDou/Galileo integrados: un solo módulo resuelve conectividad y localización |
| Actualización WWAN en laptops | Dell Latitude / Precision / Lenovo ThinkPad | Inserción directa M.2 B-Key con alto soporte de controladores Linux |
| WAN de respaldo | OpenWrt / pfSense doble WAN para respaldo | Soporte de modo dual QMI/MBIM, aunque el soporte de pfSense es relativamente más débil; se recomienda evaluar OpenWrt primero |

---

## Diferencia entre la EM7455 y la EM7430

**La EM7455 y la EM7430 utilizan el mismo chip Qualcomm MDM9230, y las especificaciones principales son idénticas (Cat 6, 300/50 Mbps, 2×CA, GNSS). La diferencia principal está en la distribución de bandas objetivo: la EM7455 cubre principalmente las bandas de América y EMEA, mientras que la EM7430 cubre las bandas de Asia-Pacífico (APAC).**

| Elemento | EM7455 | EM7430 |
|---|---|---|
| **Conjunto de chips** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **Estándar celular** | LTE-A Cat 6 | LTE-A Cat 6 |
| **Pico de descarga** | 300 Mbps | 300 Mbps |
| **Pico de subida** | 50 Mbps | 50 Mbps |
| **Agregación de portadoras** | 2×CA | 2×CA |
| **Encapsulado** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **Región objetivo** | América, EMEA (Europa/Oriente Medio/África) | Asia-Pacífico (APAC) |
| **Lista completa de bandas** | Consulte con nosotros para confirmar la ficha técnica oficial más reciente | Consulte con nosotros para confirmar la ficha técnica oficial más reciente |

> Se recomienda utilizar la ficha técnica oficial más reciente para obtener la lista precisa de bandas de cada módulo. No incluimos números de banda específicos aquí para evitar imprecisiones debido a actualizaciones de versión. Si conoce su operador y los requisitos de banda en su región, no dude en contactarnos para confirmar cuál módulo es más adecuado.

**Recomendación de selección**: Si su operador de SIM se encuentra principalmente en América del Norte o Europa, evalúe primero la **EM7455**. Si utiliza principalmente operadores en la región de Asia-Pacífico (como Taiwán, Japón, Australia), evalúe primero la **EM7430**. Debido a la distribución de bandas de los operadores en el mercado latinoamericano, le recomendamos que se comunique con nosotros antes de realizar su pedido para confirmar las bandas que necesita.

---

## EM7455 vs MC7455: el mismo chip, solo cambia el encapsulado

La EM7455 (M.2) y la MC7455 (mPCIe) utilizan el mismo conjunto de chips Qualcomm MDM9230, y las especificaciones eléctricas principales son idénticas. La diferencia principal es la **interfaz de encapsulado**:

| Elemento | EM7455 | MC7455 |
|---|---|---|
| **Encapsulado** | M.2 (B-Key) | Mini PCIe (mPCIe) |
| **Dimensiones** | 42 × 30 × 2.3 mm | 51 × 30 × 3.5 mm |
| **Dispositivos adecuados** | Ranura WWAN de laptops, placas base M.2 modernas | Ranuras mPCIe de routers industriales antiguos |
| **VID:PID genérico** | `1199:9079` | `1199:9071` |

**La elección depende únicamente del conector de su dispositivo**. Si su placa solo tiene M.2, elija la EM7455. Si solo tiene mPCIe, elija la MC7455. Puede usar una placa adaptadora (M.2→mPCIe o mPCIe→M.2) si elige el encapsulado incorrecto.

---

## Configuración en Linux (Ubuntu / Debian / Linux Mint)

La EM7455 tiene buen soporte de controladores en las distribuciones principales de Linux. Los siguientes pasos son los procedimientos básicos comunes en la comunidad; los detalles pueden variar según su entorno (versión de la distribución, versión del kernel, versión del firmware). Se recomienda verificar en un entorno de prueba antes de implementar en un sistema de producción.

### Paso 1: Detección de hardware

```bash
lsusb | grep -i sierra
# La salida esperada es similar a: Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### Paso 2: Instalación de paquetes de herramientas

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### Paso 3: Cambiar el modo de composición USB a QMI

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# Verificar el modo de composición
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# El resultado esperado es similar a: USB composition 6: DM, NMEA, AT, QMI
```

> Si necesita el modo MBIM (requerido por algunos operadores), puede consultar la configuración `AT!USBCOMP` relacionada y usar `mbimcli` en su lugar; consulte la documentación oficial de referencia de comandos AT para los valores exactos.

### Paso 4: Desbloqueo de autenticación FCC

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# Para usar la automatización integrada de ModemManager:
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### Paso 5: Conexión con NetworkManager

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn 'SU_APN'
sudo nmcli connection up 'EM7455 LTE'
```

### Paso 6: Conexión QMI manual (avanzado/solución de problemas)

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='SU_APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## Configuración de OpenWrt con QMI

La EM7455 es uno de los modelos con buena compatibilidad según los informes de la comunidad de OpenWrt. A continuación se muestra un ejemplo básico de configuración en modo QMI.

### Instalación de paquetes

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### Editar el archivo de configuración de red

Edite `/etc/config/network` y agregue la siguiente configuración de interfaz:

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'SU_APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### Reiniciar la red

```bash
/etc/init.d/network restart
```

Si usa la interfaz web LUCI: Red → Interfaces → Agregar nueva interfaz → seleccione el protocolo "QMI", el dispositivo `/dev/cdc-wdm0`, e ingrese el APN.

> ROOter (firmware de enrutamiento celular basado en OpenWrt) tiene casos de soporte documentados por la comunidad para módulos Sierra QMI, con enlaces integrados `create_connect.sh`. Si es usuario de Raspberry Pi, puede evaluar el uso directo del firmware ROOter. Para el alcance del soporte oficial, consulte los anuncios oficiales de ROOter.

---

## Compatibilidad con equipos de marca: laptops Dell / Lenovo

### Laptops Dell (DW5811e corresponde a la plataforma EM7455)

La DW5811e de Dell es la versión de marca Dell de la EM7455 (VID `413c`, PID `81b6`), ambas utilizan el mismo chip Qualcomm MDM9230. La mayoría de las distribuciones principales de Linux han incluido los identificadores de las versiones de marca más comunes en el controlador `qmi_wwan`. Se recomienda verificar prácticamente si se necesita configuración adicional:

```bash
lsusb | grep 413c
# La salida esperada es similar a: Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

Según informes de la comunidad, la mayoría de los modelos Dell (Latitude, Precision, XPS) no imponen lista blanca de BIOS, y la DW5811e se puede instalar y usar directamente en la mayoría de los casos. Sin embargo, la situación puede variar según el modelo y la versión de BIOS, por lo que se recomienda verificar según el modelo real de su equipo.

### Laptops Lenovo (EM7455 FRU)

La comunidad ha informado sobre restricciones de lista blanca de BIOS en los ThinkPad de Lenovo: algunos modelos solo reconocen módulos con la versión Lenovo FRU. A continuación se muestra un ejemplo de comandos AT que han aparecido en discusiones comunitarias como intento de eludir esta restricción:

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **No hemos verificado las fuentes originales ni la exactitud de estos comandos de forma individual, y se trata de operaciones que modifican el comportamiento del firmware subyacente del módulo. Una ejecución incorrecta podría dejar el módulo inutilizable (lo que se conoce como "bricking" o "dejar el módulo inservible").** Estos son ejemplos recopilados de discusiones públicas de la comunidad, no procedimientos verificados por Yupitek. Si tiene intención de probarlos, le recomendamos encarecidamente: confirme y respalde la versión actual del firmware, opere solo en un entorno de prueba no crítico, y asuma la responsabilidad de los riesgos. Si no está seguro, comuníquese directamente con nosotros para discutir sus necesidades y las soluciones disponibles.

### Modelos ThinkPad (modelos reportados por la comunidad para estas configuraciones)

La siguiente lista se ha recopilado de discusiones comunitarias; la aplicabilidad real y la necesidad de actualizaciones de BIOS/firmware dependen de las especificaciones oficiales y la versión de BIOS de su modelo. Le recomendamos verificar con nosotros o con los canales oficiales de Lenovo antes de realizar la compra:

- Serie 60: T460 / T460s / T460p / T560 / X260 / X1 Carbon 4th Gen / X1 Yoga 1st Gen
- Serie 70: T470 / T480 / T570 / T580 / X270 / X280 / X1 Carbon 5th/6th Gen / P51 / P52

---

## Resumen de compatibilidad de plataformas

| Plataforma | Nivel de soporte | Método de conexión | Notas |
|---|---|---|---|
| Raspberry Pi + OpenWrt | ✅✅ Muchos casos comunitarios | QMI / MBIM | Requiere placa adaptadora M.2→USB |
| Raspberry Pi + ROOter | ✅✅ | QMI (enganches integrados según informes comunitarios) | Recomendado para usuarios de Raspberry Pi |
| Ubuntu/Debian/Linux Mint | ✅✅ | ModemManager / QMI | Buen soporte de controladores en distribuciones principales |
| DD-WRT | ⚠️ Soporte más débil | QMI / PPP | Requiere una versión BETA más reciente; casos comunitarios limitados |
| pfSense / FreeBSD | ⚠️ Soporte más débil | QMI / PPP (principalmente mediante comandos AT) | Controladores celulares nativos limitados en FreeBSD; requiere evaluación caso por caso |
| Laptops Dell (DW5811e) | ✅ | QMI / MBIM | La mayoría de las distribuciones principales lo reconocen; se recomienda prueba práctica en algunos modelos |
| Laptops Lenovo | ⚠️ Requiere configuración adicional | QMI | Algunos modelos tienen restricciones de lista blanca de BIOS; mayor riesgo en el manejo; ver explicación arriba |

---

## Recursos comunitarios y lecturas adicionales

A continuación se presentan los recursos públicos disponibles relacionados con la EM7455, tanto comunitarios como oficiales, para mayor investigación:

- **danielewood/sierra-wireless-modems**: Scripts de configuración y debates comunitarios sobre EM7455/MC7455: [GitHub](https://github.com/danielewood/sierra-wireless-modems)
- **Gentoo Wiki — Sierra EM7455 (Dell DW5560)**: Configuración de Linux recopilada por la comunidad (incluye opciones de kernel, actualización de firmware, solución de problemas): [Wiki](https://wiki.gentoo.org/wiki/Sierra_EM7455_(Dell_wireless_modem_DW5560))
- **OpenWrt LTE Wiki**: Lista oficial de soporte de módems LTE y configuración: [OpenWrt LTE Guide](https://openwrt.org/docs/guide-user/network/wan/wwan/ltedongle)
- **bkerler/SierraWirelessGen**: Herramientas relacionadas con el modo de ingeniería, que pueden involucrar configuración de PRI y bandas: [GitHub](https://github.com/bkerler/SierraWirelessGen)

> El contenido de los enlaces de terceros anteriores no es mantenido por Yupitek. Evalúe su precisión y vigencia de forma independiente antes de usarlos.

---

## Preguntas frecuentes

**P1: ¿La EM7455 es compatible con 5G?**
No. La EM7455 es un módem LTE-A Cat 6 con un máximo de 300 Mbps. Si necesita 5G (Sub-6 o mmWave), puede consultar la EM9190 (Sub-6) o la EM9191 (Sub-6 + mmWave).

**P2: ¿Se puede usar la EM7455 en Latinoamérica?**
Por lo general, puede usarse con tarjetas SIM de los operadores móviles principales. El rendimiento real de la señal y las bandas disponibles dependen de la ubicación de la estación base, la planificación de red del operador y la compatibilidad con agregación de portadoras. Le recomendamos que se comunique con nosotros antes de realizar su pedido para confirmar la compatibilidad con su región y operador.

**P3: ¿Cuál es la diferencia entre la EM7455 y la MC7455?**
El chip central es el mismo, Qualcomm MDM9230, y las especificaciones son idénticas. La única diferencia es el encapsulado: la EM7455 usa M.2, mientras que la MC7455 usa mPCIe. La elección depende únicamente del tipo de conector de su dispositivo.

**P4: ¿Qué hago si Ubuntu no detecta la EM7455?**
Primero, verifique si `lsusb` muestra `1199:9079`. Si no aparece, intente usar un puerto USB 2.0 (en algunos casos, USB 3.0 puede causar interferencia). Luego, verifique que los controladores `qcserial` y `qmi_wwan` estén cargados con `lsmod | grep qmi`. También puede intentar detener ModemManager (`systemctl stop ModemManager`) y ejecutar `qmicli` manualmente para solucionar problemas. Si el problema persiste, comuníquese con nosotros para obtener ayuda.

**P5: ¿La DW5811e de Dell es lo mismo que la EM7455?**
Sí, la DW5811e es la versión de Dell de la EM7455, ambas utilizan el mismo chip Qualcomm MDM9230. La versión de Dell tiene una mayor disponibilidad en el mercado de segunda mano a un costo relativamente menor. Según los reportes de la comunidad de usuarios de Dell, la mayoría de las laptops Dell no tienen lista blanca de BIOS, aunque le recomendamos verificar según el modelo específico de su equipo.

---

## Contacto para compras

La información de especificaciones y configuración de la EM7455 anterior ha sido preparada por Yupitek. Si necesita adquirir la EM7455, EM7430, MC7455 o cualquier módulo celular de la serie Sierra Wireless, visite la página del producto para consultar precios o contactar al equipo técnico.

- **Página del producto**: [https://yupitek.com/zh-tw/products/sierra/em7455/](https://yupitek.com/zh-tw/products/sierra/em7455/)
- **Todos los productos**: [https://yupitek.com/zh-tw/products/sierra/](https://yupitek.com/zh-tw/products/sierra/)
- **Correo electrónico**: sales@yupitek.com
