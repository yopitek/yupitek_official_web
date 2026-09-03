---
title: "¿Soporte del adaptador inalámbrico ALFA para OpenWrt?"
date: 2026-09-03
draft: false
slug: "alfa-openwrt-router-compatibility"
tags:
  - "ALFA"
  - "OpenWrt"
  - "Router"
  - "kmod-mt76"
  - "AWUS036ACM"
  - "AWUS036ACH"
  - "Soft-AP"
categories:
  - "Guía de Hardware"
description: "OpenWrt: óptimo para AWUS036ACM (MT7612U), soporte completo y estable para WiFi."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumen del Problema

Pregunta del cliente: «¿El adaptador inalámbrico USB de la serie ALFA puede utilizarse en routers con OpenWrt?»

Conclusión breve: OpenWrt es la plataforma de los tres principales sistemas operativos de routers de terceros (DD-WRT / OpenWrt / Tomato) que ofrece la mejor compatibilidad con los adaptadores inalámbricos USB de la serie ALFA. Los modelos con procesador MediaTek (AWUS036ACM / ACHM / AXML / AXM) pueden ser soportados directamente a través del paquete oficial kmod-mt76; los modelos con procesador Realtek (AWUS036ACH / ACS / EACS / AX / AXER) requieren el uso de paquetes de controladores out-of-tree mantenidos por la comunidad, cuya disponibilidad puede variar según la versión de OpenWrt. Se recomienda el AWUS036ACM (MT7612U), ya que su controlador es maduro, estable y soporta escaneo y inyección.

Determinación del sujeto: Se evalúan 9 adaptadores inalámbricos USB de la serie ALFA en uso (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Análisis de las Especificaciones y Requisitos del Software Objetivo

### 2.1 ¿Qué es OpenWrt?

OpenWrt es una distribución de firmware de router de código abierto altamente modular, que utiliza el kernel de Linux y el sistema de gestión de paquetes opkg. A diferencia de DD-WRT / Tomato, los controladores de OpenWrt se proporcionan en forma de paquetes de módulos del kernel (kmod) que se pueden instalar de manera independiente, lo que permite a los usuarios instalar controladores de WiFi USB sin necesidad de recompilar toda la imagen del firmware.

### 2.2 Marco de Controladores de WiFi USB de OpenWrt

La biblioteca de paquetes oficial de OpenWrt incluye los siguientes controladores de WiFi USB:

| Paquete de controlador | Origen | Cubre chip / modelo | Estado de mantenimiento |
|---|---|---|---|
| kmod-mt76-usb + kmod-mt76x2u | Oficial in-kernel | MediaTek MT7612U (AWUS036ACM) | Activo, estable |
| kmod-mt76-usb + kmod-mt76x0u | Oficial in-kernel | MediaTek MT7610U (AWUS036ACHM) | Activo |
| kmod-mt7921u | Oficial in-kernel | MediaTek MT7921AUN (AWUS036AXML / AXM) | Disponible en versiones 23.05+ |
| kmod-rtl8812au-ct | Comunidad out-of-tree | Realtek RTL8812AU / RTL8811AU (AWUS036ACH / ACS) | Mantenido por la comunidad, se han reportado crashes de kernel en la versión 24.10 |
| kmod-rtl8821cu | Comunidad out-of-tree | Realtek RTL8811CU (AWUS036EACS) | Mantenido por la comunidad |
| kmod-rtw89 / kmod-rtl8852bu | En desarrollo | Realtek RTL8832BU (AWUS036AX / AXER) | Soporte USB de rtw89 gradualmente integrado, requiere kernel más nuevo |

### 2.3 Prerrequisitos: Soporte del Núcleo USB

Antes de instalar los controladores de WiFi, es necesario asegurarse de que OpenWrt tenga habilitado el soporte del núcleo USB:

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

La mayoría de las versiones modernas de OpenWrt ya incluyen predeterminadamente kmod-usb-core, pero usbutils (que proporciona la instrucción lsusb) debe instalarse manualmente.

## 3. Análisis de las Especificaciones y Chipsets de las Tarjetas de Red ALFA

Hasta septiembre de 2026, la línea de productos de tarjetas de red inalámbricas USB de ALFA Network en servicio es la siguiente (evaluación de la madre: 9 modelos):

| Modelo | Nivel Wi-Fi | Chipset | Interfaz | Paquete de Controladores OpenWrt |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | kmod-mt7921u (23.05+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | kmod-mt7921u (23.05+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | kmod-rtw89 (en desarrollo) / rtl8852bu personalizado |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Igual que el anterior |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | kmod-rtl8812au-ct (comunidad) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | kmod-mt76x0u (oficial) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | kmod-mt76x2u (oficial)⭐ Recomendado |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | kmod-rtl8812au-ct (cubriendo) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | kmod-rtl8821cu (comunidad) |

## 4. Modelos Aplicables y Conjuntos de Chip

### 4.1 Clasificación de Recomendación

| Nivel de Recomendación | Modelo (Conjunto de Chip) | Descripción |
|---|---|---|
| ⭐ Recomendación Fuerte | AWUS036ACM (MT7612U) | Controladores oficiales maduros y estables, soporta AP / STA / Monitor / Injection, la mejor opción en OpenWrt |
| ✅ Recomendado | AWUS036ACHM (MT7610U) | Controladores oficiales, dual banda pero solo 433Mbps, adecuado para escenarios de bajo consumo de energía |
| ✅ Recomendado (Versión Nueva) | AWUS036AXML / AXM (MT7921AUN) | Wi-Fi 6E, controladores oficiales, requiere OpenWrt 23.05+ y kernel 5.15+ |
| ⚠️ Disponible pero con Precaución | AWUS036ACH (RTL8812AU) | Controladores de la comunidad, versión 24.10 con informes de crash de kernel, se recomienda usar 23.05 |
| ⚠️ Disponible pero con Precaución | AWUS036ACS (RTL8811AU) | Como el 8812au, cubierto por el controlador 8812au |
| ⚠️ Disponible pero con Precaución | AWUS036EACS (RTL8811CU) | Controladores de la comunidad, estabilidad media |
| ❌ No Recomendado | AWUS036AX / AXER (RTL8832BU) | Wi-Fi 6, soporte rtw89 USB en desarrollo, la mayoría de las versiones de OpenWrt no se pueden usar directamente |

### 4.2 Requisitos de Hardware del Router

| Ítem | Requisitos Mínimos | Requisitos Recomendados |
|---|---|---|
| Puerto USB | USB 2.0 (AWUS036ACHM / ACS / EACS) | USB 3.0 (AWUS036ACH / ACM / AX Series) |
| Flash | 16MB (instalación de controladores + paquetes dependientes) | 32MB+ |
| RAM | 128MB | 256MB+ (modo AP + múltiples usuarios) |
| Versión de OpenWrt | 21.02+ | 23.05.x (versión estable) |

## 5. Requisitos de Entorno

### 5.1 Entorno de Software

- Versión estable de OpenWrt: 23.05.x (kernel 5.15) o 24.10.x (kernel 6.6)
- Repositorios de paquetes: Repositorio oficial de paquetes opkg (https://downloads.openwrt.org/releases/{version}/packages/{arch}/)
- Conexión a red: Durante la instalación del controlador, el router debe estar conectado a Internet (a través de la interfaz WAN)

### 5.2 Entorno de Hardware

- Router compatible con OpenWrt que cuente con una interfaz USB 2.0 / 3.0
- Modelos de alta potencia (AWUS036ACH) se recomienda utilizar un Hub USB 3.0 con alimentación, para evitar una insuficiente alimentación en el puerto USB del router
- AWUS036AXML es una interfaz USB-C, se debe asegurar que el router tenga una interfaz USB-C o utilizar un adaptador USB-C a USB-A

## 6. Determinación de la Compatibilidad

### Matriz de Compatibilidad ALFA Modelos Actuales × OpenWrt

| Modelo | Procesador | Método de Control | Detección de USB | Conexión STA | Modo AP | Monitor | Versión Mínima | Evaluación General |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | kmod-mt76x2u | ✅ | ✅ | ✅ | ✅ | 21.02+ | ⭐ Mejor |
| AWUS036ACHM | MT7610U | kmod-mt76x0u | ✅ | ✅ | ✅ | ⚠️ Limitada | 21.02+ | ✅ Buena |
| AWUS036AXML | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ Limitada | 23.05+ | ✅ Buena |
| AWUS036AXM | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ Limitada | 23.05+ | ✅ Buena |
| AWUS036ACH | RTL8812AU | kmod-rtl8812au-ct | ✅ | ✅ | ✅ | ⚠️ Limitada | 22.03+（24.10 con fallo） | ⚠️ Disponible |
| AWUS036ACS | RTL8811AU | kmod-rtl8812au-ct | ✅ | ✅ | ⚠️ | ❌ | 22.03+ | ⚠️ Disponible |
| AWUS036EACS | RTL8811CU | kmod-rtl8821cu | ✅ | ⚠️ | ❌ | ❌ | 23.05+ | ⚠️ Disponible |
| AWUS036AX | RTL8832BU | rtw89（en desarrollo） | ⚠️ | ❌ | ❌ | ❌ | Necesario compilación personalizada | ❌ No recomendado |
| AWUS036AXER | RTL8832BU | rtw89（en desarrollo） | ⚠️ | ❌ | ❌ | ❌ | Necesario compilación personalizada | ❌ No recomendado |

Criterios de Determinación: Disponibilidad de paquetes kmod en el repositorio oficial de OpenWrt (23.05 / 24.10) + Informes de usuarios en el foro de OpenWrt. Los controladores de chips Realtek son mantenidos por la comunidad, su estabilidad y funcionalidad no alcanzan a la serie MediaTek mt76.

## 7. Detallados pasos a paso para la configuración

### 7.1 Preparativos previos: Activar soporte de núcleo USB

**Paso 1: Iniciar sesión en el router OpenWrt mediante SSH**

```bash
ssh root@192.168.1.1
```

**Paso 2: Actualizar el repositorio de paquetes y instalar el soporte de núcleo USB**

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

**Paso 3: Insertar la tarjeta de red ALFA y confirmar la detección USB**

```bash
lsusb
# Salida esperada de ejemplo (AWUS036ACM / MT7612U):
# Bus 002 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

### 7.2 Ruta A: Modelos de chip MediaTek (AWUS036ACM / ACHM / AXML / AXM)

Tomando como ejemplo AWUS036ACM (MT7612U):

**Paso 1: Instalar el paquete de controladores**

```bash
# AWUS036ACM (MT7612U)
opkg install kmod-mt76-usb kmod-mt76x2u

# AWUS036ACHM (MT7610U) — Cambiar por
# opkg install kmod-mt76-usb kmod-mt76x0u

# AWUS036AXML / AXM (MT7921AUN) — Cambiar por (requiere 23.05+)
# opkg install kmod-mt7921u
```

**Paso 2: Instalar herramientas de gestión inalámbrica**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**Paso 3: Confirmar la creación de la interfaz de red**

```bash
iw dev
# Esperada salida: wlan0 o wlan1
```

**Paso 4: Escanear redes WiFi cercanas (verificación de funcionalidad)**

```bash
iw dev wlan0 scan | grep -E "SSID|signal"
```

**Paso 5: Configurar como cliente STA (conectar a un AP existente)**

Editar /etc/config/wireless:

```text
config wifi-device 'radio1'
       option type 'mac80211'
       option path 'platform/usb1/1-1/1-1:1.0'
       option channel 'auto'
       option htmode 'VHT80'

config wifi-iface 'wifinet2'
       option device 'radio1'
       option mode 'sta'
       option network 'wwan'
       option ssid 'Nombre de tu WiFi'
       option encryption 'psk2'
       option key 'Contraseña de tu WiFi'
```

**Paso 6: Reiniciar el servicio de red**

```bash
/etc/init.d/network restart
```

**Paso 7: Configurar como punto de acceso (AP) para compartir red**

Editar /etc/config/wireless, cambiar mode a ap:

```text
config wifi-iface 'wifinet2'
   option device 'radio1'
   option mode 'ap'
   option network 'lan'
   option ssid 'ALFA-OpenWrt-AP'
   option encryption 'psk2'
   option key 'Contraseña de tu punto de acceso'
```

**Paso 8: Activar el modo de escucha (para pruebas de penetración)**

```bash
opkg install aircrack-ng
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
iw dev wlan0 set channel 6
# Verificación
iw dev wlan0 info
# type debe mostrar monitor
```

### 7.3 Ruta B: Modelos de chip Realtek (AWUS036ACH / ACS / EACS)

Tomando como ejemplo AWUS036ACH (RTL8812AU):

**Paso 1: Instalar el controlador comunitario**

```bash
opkg update
opkg install kmod-rtl8812au-ct

# AWUS036EACS (RTL8811CU) — Cambiar por
# opkg install kmod-rtl8821cu
```

**Paso 2: Instalar herramientas de gestión inalámbrica**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**Paso 3: Confirmar la interfaz**

```bash
iw dev
# Notar: la interfaz del controlador kmod-rtl8812au-ct puede ser wlan0 o wlan1
```

La configuración es similar a la Ruta 7.2, pasos 5-7 (modo STA / AP).

**Paso 4: Modo de escucha**

```bash
# El controlador kmod-rtl8812au-ct admite el modo de escucha
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
# La funcionalidad de inyección de paquetes es limitada, se recomienda usar chips mt76 para pruebas de penetración
```

**Paso 5: Si se encuentra un kernel crash (problema conocido en la versión 24.10)**

```bash
# Regresar a la versión 23.05 estable, o usar un controlador compilado a mano
# Revisar los registros de crash
logread | grep -i "panic\|crash\|rtl8812"
```

### 7.4 Ruta C: Modelos Wi-Fi 6 (AWUS036AX / AXER, RTL8832BU)

⚠️ Esta ruta requiere una compilación personalizada de OpenWrt, no adecuada para usuarios normales.

**Paso 1: Confirmar si la versión de OpenWrt incluye soporte USB para rtw89**

```bash
opkg list | grep rtw89
# Si no hay resultados, la versión no incluye el soporte
```

**Paso 2: Si es necesario, compilar el imagen del sistema OpenWrt**

Añadir kmod-rtw89 y el firmware correspondiente.

**Sugerencia alternativa**: Para necesidades de tarjetas USB Wi-Fi 6 en routers OpenWrt, se recomienda usar AWUS036AXML (MT7921AUN) como alternativa.

## 8. Errores Comunes y Soluciones

| Síntoma | Posible Causa | Solución |
|---|---|---|
| No se ve la tarjeta de red ALFA en lsusb | No se ha instalado el núcleo USB / Falta de alimentación | Verifique que haya instalado kmod-usb-core kmod-usb2 kmod-usb3; utilice un Hub USB con alimentación |
| Se ve en lsusb pero iw dev no tiene interfaz | No se ha instalado el controlador / Controlador incompatibles | Instale el paquete kmod correspondiente; revise dmesg en busca de errores de falta de firmware |
| opkg install kmod-mt76x2u informa de 'mismatch de versión del kernel' | La versión de OpenWrt no coincide con la versión de la biblioteca de paquetes | Ejecute opkg update y vuelva a intentarlo; verifique que la versión del firmware coincida con la arquitectura de la biblioteca de paquetes |
| Falla al iniciar el modo AP (error de hostapd) | Controlador no admite AP / Configuración de canal incorrecta | Verifique que el chip admite el modo AP; intente fijar el canal (como 6 o 149); revise el Regulatory Domain |
| No se puede inyectar paquetes en modo monitor | Controlador no admite inyección / Colisión de canales | MediaTek mt76 serie admite la mejor inyección; la función de inyección de Realtek 8812au-ct es limitada; verifique airmon-ng check kill |
| AWUS036ACH se desconecta cuando se usa alta potencia | Falta de alimentación USB | Utilice un Hub USB 3.0 con alimentación; configure option txpower '20' en /etc/config/wireless para reducir la potencia |
| Kernel panic después de instalar rtl8812au-ct en 24.10 | Problemas de compatibilidad conocidos del controlador | Regrese a la versión estable 23.05.x; o siga el issue en GitHub para esperar la corrección |
| MT7921 (AXML/AXM) no puede usar la banda de 6GHz | Restricciones del Regulatory Domain / Versión del kernel | Necesita kernel 5.19+ y configuración correcta de la región regulatoria Wi-Fi 6E; el soporte de 6GHz en OpenWrt 23.05 aún está en pruebas |

## 9. Limitaciones Conocidas

- **Controladores de chip Realtek para mantenimiento de la comunidad**: kmod-rtl8812au-ct y kmod-rtl8821cu no son mantenidos oficialmente por OpenWrt, por lo que su estabilidad y cronograma de actualizaciones no pueden garantizarse.
- **Informe de fallo de kernel en la versión 24.10 de rtl8812au-ct**: Se recomienda a los usuarios de chips Realtek mantenerse en la versión 23.05.x.
- **Soporte insuficiente para Wi-Fi 6 (RTL8832BU)**: El controlador USB rtw89 está en desarrollo, y la mayoría de las versiones de OpenWrt no pueden usar directamente AWUS036AX / AXER.
- **Restricciones en el rendimiento del modo AP**: Al usar WiFi USB como AP, la tasa de transferencia es menor que la del WiFi integrado en el router (ancho de banda del bus USB + sobrecarga del controlador).
- **Diferencias en las funciones de escucha/inyección**: La serie MediaTek mt76 ofrece el soporte más completo; las funciones de inyección del chip Realtek son limitadas y no son adecuadas para pruebas de penetración profesional.
- **Recursos de hardware del router**: En routers de bajo nivel (16MB Flash / 128MB RAM), la instalación del controlador puede resultar en espacio insuficiente, afectando a otras funciones.
- **Interferencia de USB 3.0**: Los dispositivos USB 3.0 pueden interferir con el WiFi de 2.4GHz, por lo que se recomienda usar puertos USB 2.0 o un Hub USB bien aislado.
- **Uso simultáneo de múltiples tarjetas de red**: Al usar simultáneamente WiFi integrado en el router y WiFi USB, pueden aparecer conflictos de canales o competencia por recursos.
- ⚠️ **El mantenedor del controlador RTL8832BU (AWUS036AX/AXER) ha recomendado evitar su uso**: La sección 4.1 de este documento señala con un "❌ No recomendado", la razón no es solo que rtw89 USB esté en desarrollo, sino que el mantenedor morrownr ha expresado públicamente que la serie de chips "es un mal controlador, sospechando que hay problemas en el chip en sí", recomendando a los usuarios de Linux evitar su uso en la actualidad (ver sección 10).
- **Aclaración necesaria sobre los términos de umbral de versión del kernel**: La expresión "MT7921AUN requiere OpenWrt 23.05+ y kernel 5.15+" en la sección 4.1 puede ser engañosa — el controlador mt7921u realmente necesita **kernel 5.19+** en sistemas Linux de escritorio (ver declaración del mantenedor), pero el paquete oficial de OpenWrt a menudo recoge anticipadamente a través del mecanismo de backport, por lo que OpenWrt 23.05 (aunque se indica con un kernel base de 5.15) aún tiene informes de usuarios que han instalado con éxito kmod-mt7921u. **La determinación debe basarse en los resultados reales de la consulta `opkg list` de la versión del cliente, no en la versión del kernel**.

Condiciones de refutación: Si el paquete posterior de OpenWrt actualiza y corrige el problema de kernel crash en la versión 24.10 de rtl8812au-ct, las recomendaciones de la sección 4.1 y la sección 6 para AWUS036ACH pueden actualizarse de "mantenerse en 23.05"; si el soporte de rtw89 USB se integra formalmente en el repositorio oficial de OpenWrt, la determinación "no recomendado" para AWUS036AX / AXER debe revisarse; si se publica una declaración oficial de soporte completo de 6GHz para MT7921, se debe actualizar la descripción de las limitaciones de AXML / AXM.

## 10. Referencias URL

| Fuente | Descripción | URL | Estado de revisión | Fecha de revisión |
|---|---|---|---|---|
| Documentación oficial de OpenWrt | Entrada de documentos oficiales de OpenWrt (configuración inalámbrica / gestión de paquetes) | https://openwrt.org/docs/start | ✅ Revisado | 2026-09-03 |
| Foro oficial de OpenWrt | Entrada de discusión sobre controladores WiFi USB | https://forum.openwrt.org/ | ✅ Revisado | 2026-09-03 |
| morrownr/8812au GitHub | Fuente de controladores Linux RTL8812AU | https://github.com/morrownr/8812au-20210820 | ✅ Revisado | 2026-09-03 |
| Catálogo de productos de ALFA Network (Yupitek) | Especificaciones de productos actuales de ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Revisado | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | Declaración oficial del mantenedor de controladores: se recomienda evitar los chips rtl8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Revisado | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko solo aparecerá en el núcleo con kernel 5.19+ (palabras del mantenedor) | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ Revisado | 2026-09-03 |
| Foro oficial de OpenWrt — Mejor dongle USB WiFi para Raspberry Pi 4B | Informes de usuarios sobre la instalación exitosa de kmod-mt7921u en OpenWrt 23.05.0 | https://forum.openwrt.org/t/mejor-dongle-usb-wifi-para-raspberry-pi-4b/160103 | ✅ Revisado | 2026-09-03 |

Artículos relacionados: [¿Soporta el adaptador inalámbrico ALFA DD-WRT?](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[¿Soporta el adaptador inalámbrico ALFA Tomato?](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[¿Soporta el adaptador inalámbrico ALFA NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[¿Soporta el adaptador inalámbrico ALFA NVIDIA Jetson Nano?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Declaración de exención de responsabilidad: La determinación de compatibilidad de este documento se realiza según la biblioteca oficial de paquetes de OpenWrt 23.05.x / 24.10.x. La disponibilidad de paquetes puede variar según la arquitectura del router (ath79 / ramips / mvebu / x86, etc.). Los controladores de chips Realtek son mantenidos por la comunidad, y su estabilidad puede variar según la versión. Se recomienda utilizar modelos de chips MediaTek (AWUS036ACM como opción preferente) como elección prioritaria para el OpenWrt USB WiFi.
