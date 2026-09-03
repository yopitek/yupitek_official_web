---
title: "Soporte del Adaptador Inalámbrico ALFA para Tomato"
date: 2026-09-03
draft: false
slug: "alfa-tomato-router-compatibility"
tags:
  - "ALFA"
  - "Tomato"
  - "FreshTomato"
  - "Router"
  - "Broadcom"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "Guía de Hardware"
description: "ALFA機型在Tomato上無USB WiFi驅動，不推薦使用；建議改用OpenWrt。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumen del Problema

Pregunta del cliente: «¿Los adaptadores inalámbricos USB de la serie ALFA pueden ser utilizados en routers que han sido flashados con el firmware Tomato?»

Conclusión breve: Actualmente, todos los modelos activos de la serie ALFA no tienen soporte de controladores para Tomato (incluidos las versiones derivadas como FreshTomato y AdvancedTomato), y no se recomienda su uso. Tomato es la plataforma de firmware de terceros para routers que ofrece el menor soporte para WiFi USB, centrando su desarrollo principalmente en el WiFi integrado en los routers con chipsets Broadcom. Si es necesario utilizar una tarjeta de red WiFi USB en un router, se debe optar por OpenWrt.

Determinación del sujeto: Se han evaluado 9 modelos de tarjetas de red USB activos de ALFA (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Análisis de Especificaciones y Requisitos del Software de Objetivo

### 2.1 ¿Qué es Tomato?

Tomato es una carcasa de router de código abierto de larga historia, originalmente desarrollada por Jonathan Zarate, y luego derivada en múltiples ramas:

| Versión Derivada | Estado de Mantenimiento | Plataforma Soportada |
|---|---|---|
| Versión Original Tomato | Mantenimiento detenido (principios de la década de 2010) | Routers Broadcom MIPS |
| Tomato by Shibby | Mantenimiento detenido | Broadcom MIPS / ARM |
| AdvancedTomato | Mantenimiento detenido | Broadcom (versión GUI revisada de Shibby) |
| FreshTomato | Mantenimiento activo | Broadcom MIPS / ARM (BCM47xx / BCM53xx) |
| Toastman Tomato | Mantenimiento detenido | Broadcom MIPS |

### 2.2 Marco de Soporte de WiFi USB en Tomato

La filosofía de diseño central de Tomato es "proporcionar una carcasa de router de código abierto sencilla y estable para routers Broadcom", y su función USB se centra principalmente en lo siguiente:

| Tipo de Función USB | Estado de Soporte |
|---|---|
| Dispositivo de almacenamiento USB (disco duro portátil / disco duro) | ✅ Soporte completo (Samba / FTP / DLNA) |
| Impresora USB | ✅ Soporte (p910nd / CUPS) |
| Módem de datos 3G/4G | ⚠️ Soporte parcial |
| Tarjeta de red WiFi USB | ❌ Casi no soportada |

El núcleo central de Tomato (kernel) incluye por defecto el módulo de control cerrado (wl) del WiFi integrado en los routers Broadcom, sin ningún controlador de WiFi USB. El sistema de gestión de paquetes (ipkg / Optware) tampoco proporciona paquetes de controladores de WiFi USB.

### 2.3 Limitaciones Clave

- Tomato solo soporta routers con procesadores Broadcom, y los puertos USB de los routers Broadcom generalmente se utilizan solo para almacenamiento / impresoras
- Aunque FreshTomato sigue siendo mantenido, el enfoque de desarrollo se centra en la corrección de bugs en la plataforma Broadcom, no en la adición de controladores de WiFi USB
- El espacio del sistema de archivos de Tomato es muy pequeño (generalmente 4-16MB), por lo que incluso si se desea traducir manualmente los controladores, no hay espacio para instalarlos
- Tomato no tiene sistemas de gestión de paquetes modernos como opkg, por lo que no se puede instalar controladores kmod de manera sencilla como en OpenWrt

## 3. Análisis de las Especificaciones y Chipsets de las Tarjetas de Red ALFA

Hasta septiembre de 2026, la línea de productos de tarjetas de red inalámbricas USB de ALFA Network en servicio es la siguiente (evaluación de la madre: 9 modelos):

| Modelo | Nivel Wi-Fi | Chipset | Interfaz | Estado del Controlador Tomato |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ Sin |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ Sin |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ Sin |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ Sin |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ❌ Sin |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ❌ Sin |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ❌ Sin |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ❌ Sin |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ❌ Sin |

## 4. Modelos Aplícables y Chipsets

### 4.1 Modelos ALFA extremadamente antiguos que podrían ser compatibles con Tomato (ya descontinuados)

| Modelo | Chipset | Módulo de controlador Linux | Descripción |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | Teóricamente puede cargarse, pero Tomato no lo incluye por defecto; se requiere la compilación manual del módulo del kernel, lo que reduce enormemente la factibilidad |
| AWUS036H | Realtek RTL8187L | rtl8187 | Lo mismo, solo 2.4GHz / 54Mbps, descontinuado hace más de una década |

⚠️ Incluso estos modelos antiguos, en Tomato se requiere que el usuario compila manualmente los módulos de controladores correspondientes a la versión del kernel, y el espacio del sistema de archivos de Tomato generalmente no es suficiente para la instalación. Esto no es considerado "soporte", sino una "hack extremadamente avanzada".

### 4.2 Modelos en servicio que no son compatibles con Tomato

Todos los modelos ALFA en servicio (véase la tabla del capítulo 3) no son compatibles con Tomato por los siguientes motivos:

- Chipsets Realtek (RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU): Tomato no tiene ningún controlador correspondiente, y tampoco se puede instalar a través del gestor de paquetes
- Chipsets MediaTek (MT7612U / MT7610U / MT7921AUN): Tomato no incluye los controladores mt76 / mt7921, y el equipo de desarrollo de FreshTomato no tiene planes de incluirlos
- Incluso si lsusb puede ver el dispositivo (si Tomato tiene habilitado el núcleo USB), solo se realiza un reconocimiento a nivel de la trama USB, sin poder establecer una interfaz de red

## 5. Requisitos de Entorno

Dado que el modelo ALFA en uso no es compatible con Tomato, en esta sección se detallan las condiciones extremas necesarias en caso de que el cliente insista en intentarlo:

| Ítem | Requisitos |
|---|---|
| Hardware del router | Router con chip Broadcom, con puerto USB 2.0, Flash ≥ 32MB, RAM ≥ 256MB |
| Versión de Tomato | Versión más reciente de FreshTomato (las versiones anteriores tienen soporte USB más deficiente) |
| Entorno de compilación cruzada | Se requiere la configuración de una herramienta de compilación cruzada para la arquitectura Broadcom (MIPS / ARM) de Tomato |
| Código fuente del controlador | Se necesita obtener el código fuente del controlador Linux correspondiente al chip y modificarlo para que sea compatible con la versión del kernel de Tomato |
| Capacidad técnica | Se requiere experiencia en desarrollo de módulos del kernel de Linux, compilación cruzada y depuración |
| Costo de tiempo | Se estima que tomará varias horas hasta varios días, y la probabilidad de éxito es baja |

Conclusión: Para el 99.9% de los usuarios, el uso de la tarjeta WiFi USB ALFA en Tomato es inaceptable.

## 6. Determinación de Compatibilidad

### Matriz de Compatibilidad ALFA Modelos Actuales × Tomato

| Modelo | Chipset | Soporte de Núcleo USB | Detección USB | Conexión STA | Modo AP | Monitor | Evaluación General |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ⚠️ Requiere activar el núcleo USB | ❌ | ❌ | ❌ | ❌ | No compatible |
| AWUS036AXM | MT7921AUN | ⚠️ | ❌ | ❌ | ❌ | ❌ | No compatible |
| AWUS036AX | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | No compatible |
| AWUS036AXER | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | No compatible |
| AWUS036ACH | RTL8812AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | No compatible |
| AWUS036ACHM | MT7610U | ⚠️ | ❌ | ❌ | ❌ | ❌ | No compatible |
| AWUS036ACM | MT7612U | ⚠️ | ❌ | ❌ | ❌ | ❌ | No compatible |
| AWUS036ACS | RTL8811AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | No compatible |
| AWUS036EACS | RTL8811CU | ⚠️ | ❌ | ❌ | ❌ | ❌ | No compatible |

Criterio de determinación: El núcleo oficial de Tomato (incluido FreshTomato) y la biblioteca de paquetes no incluyen ningún controlador de chipsets USB WiFi modernos. El objetivo de diseño de Tomato nunca ha incluido la funcionalidad de expansión USB WiFi.

## 7. Detallados pasos a paso para la configuración

Dado que los modelos actuales de ALFA no son compatibles con Tomato, esta sección proporciona pasos de verificación y alternativas.

### 7.1 Verificación de tu router Tomato para soporte USB WiFi (pasos de depuración)

**Paso 1: Ingresar a la interfaz de administración de Tomato**

Ingrese 192.168.1.1 (o la dirección IP de su router) en el navegador.

**Paso 2: Verificar si el núcleo USB está habilitado**

- Vaya a USB and NAS > USB Support
- Verifique que Core USB Support, USB 2.0 Support, USB 3.0 Support (si hay) estén seleccionados
- Verifique USB Wireless Device Support (si hay esta opción) — La mayoría de las versiones de Tomato no tienen esta opción

**Paso 3: Inserte la tarjeta de red ALFA en el puerto USB del router**

**Paso 4: Verifique la detección USB a través de SSH / Telnet**

```bash
# Verifique si existe lsusb (Tomato por defecto puede no tenerlo)
which lsusb
# Si no hay lsusb, verifique /proc/bus/usb o dmesg
cat /proc/bus/usb/devices
# O
dmesg | grep -i usb
```

**Paso 5: Verifique la interfaz de red**

```bash
ifconfig -a
# Si solo hay vlan0 / br0 / eth0 / eth1 (interfaz interna del router), y no wlan0 / wlan1, significa que el USB WiFi no está siendo conducido
```

**Paso 6: Verifique los módulos del kernel disponibles**

```bash
lsmod
# Se espera que solo haya wl (controlador de WiFi integrado Broadcom), et (controlador de red Ethernet) y otros
# No habrá controladores de WiFi USB como mt76 / rtl8812 / cfg80211 / mac80211
```

**Paso 7: Verifique si se puede instalar un complemento adicional**

```bash
# Tomato utiliza ipkg, pero el contenido de la biblioteca de paquetes es muy limitado
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# El resultado esperado será vacío
```

### 7.2 Alternativas sugeridas

#### Alternativa 1: Cambiar a OpenWrt (altamente recomendado)

Si su modelo de router es compatible con OpenWrt, recomendamos cambiar el firmware de Tomato a OpenWrt. OpenWrt tiene una biblioteca completa de controladores de WiFi USB, compatible con la mayoría de los modelos ALFA.

- Verifique si su router está en la lista de dispositivos compatibles de OpenWrt
- Si es compatible, consulte los pasos de instalación en [¿Es compatible la tarjeta de red inalámbrica ALFA con OpenWrt?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)

#### Alternativa 2: Usar el WiFi interno del router

Tomato tiene un soporte completo para el WiFi interno de los routers Broadcom, si sus necesidades son de navegación general o de punto de acceso, puede usar directamente el WiFi interno del router, sin necesidad de conectar una tarjeta de red ALFA.

#### Alternativa 3: Cambiar de hardware

Si necesita características específicas del WiFi USB (como salida de alta potencia, modo de monitoreo, inyección de paquetes), la plataforma Tomato no puede satisfacer sus necesidades. Recomendamos:

- Usar un router compatible con OpenWrt + tarjeta de red ALFA
- O usar un mini PC x86 con OpenWrt / pfSense + tarjeta de red ALFA
- O usar directamente la tarjeta de red ALFA en un ordenador con Kali Linux / Ubuntu

## 8. Errores Comunes y Soluciones

| Síntoma | Posible Causa | Solución |
|---|---|---|
| La interfaz de gestión de Tomato no tiene la opción "USB Wireless Device Support" | La versión de Tomato no ha traducido el soporte USB WiFi | Esto es normal, no un error; la mayoría de las versiones de Tomato no tienen esta función |
| Después de insertar la tarjeta de red ALFA, dmesg detecta el USB pero no hay interfaz de red | Faltan los controladores | No se puede resolver, Tomato no tiene el controlador correspondiente |
| Quiero instalar manualmente paquetes ipkg pero no puedo encontrar el controlador WiFi | La biblioteca de paquetes de Tomato no tiene el controlador USB WiFi | Esto es normal; se recomienda cambiar a OpenWrt |
| La versión antigua de ALFA (RT3070) se puede detectar en Tomato pero no se puede conectar | Los controladores no están completos / falta el firmware | Incluso con el chip antiguo no se garantiza que sea usable; se recomienda usarlo en OpenWrt |
| Después de actualizar el router a Tomato, el puerto USB solo puede leer memorias USB | La función USB de Tomato está diseñada solo para almacenamiento / impresoras | Esto es el comportamiento esperado; Tomato no admite WiFi USB |

## 9. Limitaciones Conocidas

- **No hay controladores USB WiFi integrados**: El núcleo oficial de Tomato (incluido FreshTomato) no incluye ningún controlador para chips USB WiFi modernos, lo que representa la limitación más fundamental.
- **Vinculación de controladores Broadcom cerrados**: Tomato depende de los controladores wl cerrados de Broadcom y no puede coexistir con controladores USB WiFi basados en la arquitectura mac80211 / cfg80211 de código abierto.
- **Falta de ecosistema de gestión de paquetes**: La biblioteca de paquetes ipkg de Tomato contiene muy pocos paquetes, a diferencia de OpenWrt, que cuenta con miles de paquetes instalables.
- **Espacio insuficiente en Flash / RAM**: La mayoría de los routers Tomato tienen entre 4 y 16 MB de Flash, por lo que no hay espacio suficiente para instalar controladores compilados.
- **Diferentes direcciones de desarrollo**: La prioridad del equipo de desarrollo de FreshTomato es la estabilidad de la plataforma Broadcom, por lo que no destinarán recursos adicionales para la adición de soporte para USB WiFi.
- **No se admite escucha / inyección**: La arquitectura WiFi de Tomato (controlador Broadcom wl) no admite funciones de prueba de penetración y el uso de USB WiFi externo no cambia esta situación.
- **No hay expansión de modo AP**: Incluso si los chips antiguos pueden cargar el controlador, la interfaz de configuración de red de Tomato no admite la configuración del modo AP para USB WiFi.

Condiciones de refutación: Si en el futuro la versión de FreshTomato incluye explícitamente el soporte para controladores USB WiFi en los notas de lanzamiento oficiales o si la comunidad presenta un proyecto de移植 de módulos mt76 / rtl8812au ampliamente validado, la determinación de "no soportado" en el punto 6 de este documento necesitará ser revisada; si FreshTomato cambia a un núcleo basado en mac80211 de código abierto, también se necesitará actualizar la descripción de las limitaciones.

## 10. Referencias URL

| Fuente | Descripción | URL | Estado de verificación | Fecha de verificación |
|---|---|---|---|---|
| Sitio web oficial de FreshTomato | Lista de versiones más recientes y dispositivos compatibles de FreshTomato | https://freshtomato.org/ | ✅ Verificado | 2026-09-03 |
| Documentación oficial de OpenWrt | Configuración de controladores WiFi USB (referencia comparativa) | https://openwrt.org/docs/start | ✅ Verificado | 2026-09-03 |
| Foro oficial de OpenWrt | Discusiones sobre controladores WiFi USB (referencia comparativa) | https://forum.openwrt.org/ | ✅ Verificado | 2026-09-03 |
| Catálogo de productos de ALFA Network (Yupitek) | Especificaciones de productos actuales de ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |

Artículos relacionados: [¿Soporta el adaptador inalámbrico ALFA DD-WRT?](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[¿Soporta el adaptador inalámbrico ALFA OpenWrt?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)｜[¿Soporta el adaptador inalámbrico ALFA NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[¿Soporta el adaptador inalámbrico ALFA NVIDIA Jetson Nano?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Declaración de exención de responsabilidad: La determinación de la compatibilidad de este documento se realiza en función del núcleo oficial de Tomato / FreshTomato y la biblioteca de paquetes. Un número muy reducido de usuarios avanzados pueden lograr la implementación de funciones básicas en chips específicos mediante la compilación cruzada personalizada, pero esto no está dentro del rango de soporte oficial y no se recomienda a los usuarios generales intentar esto. Para escenarios que requieren el uso de WiFi USB en el router, OpenWrt es la única opción de firmware de terceros realmente viable.
