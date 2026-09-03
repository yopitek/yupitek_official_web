---
title: "¿Soporte de la tarjeta inalámbrica ALFA para DD-WRT?"
date: 2026-09-03
draft: false
slug: "alfa-ddwrt-router-compatibility"
tags:
  - "ALFA"
  - "DD-WRT"
  - "Router"
  - "Broadcom"
  - "Atheros"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "Guía de Hardware"
description: "ALFA USB網卡無DD-WRT官方驅動，建議使用OpenWrt。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumen del Problema

Pregunta del cliente: «¿Los adaptadores inalámbricos USB de la serie ALFA pueden utilizarse en routers que han sido flashados con el firmware DD-WRT?»

Conclusión breve: Actualmente, todos los modelos activos de la serie ALFA (AWUS036ACH / ACM / ACHM / ACS / EACS / AX / AXER / AXML / AXM, un total de 9 modelos) no tienen soporte oficial de controladores en DD-WRT y no se recomienda su uso. (Determinante: 9 adaptadores USB de red activos de ALFA) El soporte de WiFi USB en DD-WRT se limita a una cantidad muy reducida de chipsets Atheros / Ralink antiguos y requiere una versión de compilación específica. Si es necesario utilizar un adaptador inalámbrico USB en el router, se recomienda utilizar OpenWrt (ver [Compatibilidad de los adaptadores inalámbricos USB de ALFA con OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)).

## 2. Análisis de Especificaciones y Requisitos del Software Objetivo

### 2.1 ¿Qué es DD-WRT?

DD-WRT es una plataforma de firmware de router de terceros de código abierto, diseñada principalmente para routers con chip WiFi integrado (Broadcom / Atheros / Ralink SoC). Su arquitectura central es el kernel de Linux, aunque los programas de control por defecto solo incluyen los controladores inalámbricos correspondientes al SoC del router objetivo.

### 2.2 Marco de Soporte para WiFi USB en DD-WRT

DD-WRT permite la instalación de controladores adicionales a través del sistema de gestión de paquetes ipkg, pero en la biblioteca de paquetes oficial hay muy pocos controladores de WiFi USB:

| Controlador | Estado en DD-WRT | Chip Correspondiente (Modelos ALFA) |
|---|---|---|
| ath9k_htc | Parcialmente integrado en algunas versiones | Atheros AR9271 (como TP-Link TL-WN722N v1) |
| rt2800usb | Parcialmente integrado en algunas versiones | Ralink RT3070 / RT3370 / RT5370 (antiguos ALFA AWUS036NH) |
| rtl8812au | Sin paquete oficial | Realtek RTL8812AU (AWUS036ACH) |
| mt76 / mt76x2u | Sin paquete oficial | MediaTek MT7612U / MT7610U (AWUS036ACM / ACHM) |
| mt7921u | Sin paquete oficial | MediaTek MT7921AUN (AWUS036AXML / AXM) |
| rtl8852bu / rtw89 | Sin paquete oficial | Realtek RTL8832BU (AWUS036AX / AXER) |

### 2.3 Limitaciones Clave

- El núcleo de DD-WRT prioriza el soporte para WiFi integrado en el router, y el WiFi USB se considera una función secundaria.
- Las versiones de DD-WRT compiladas para diferentes modelos de routers varían, y la disponibilidad de controladores difiere considerablemente.
- Incluso si la comunidad compila y añade controladores, a menudo no se pueden instalar debido a la falta de espacio en Flash / RAM.
- DD-WRT prácticamente no soporta el modo de escucha (Monitor Mode) y la inyección de paquetes (Packet Injection) para WiFi USB.

## 3. Análisis de las Especificaciones y Chipsets de las Tarjetas de Red ALFA

Al 9 de septiembre de 2026, la línea de productos de tarjetas de red USB inalámbricas de ALFA Network en servicio es la siguiente:

| Modelo | Nivel Wi-Fi | Chipset | Interfaz | Estado del Controlador Linux |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | Linux in-kernel (mt7921u, requiere kernel 5.12+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | Linux in-kernel (mt7921u, requiere kernel 5.12+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree (rtl8852bu / rtw89) |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree (rtl8852bu / rtw89) |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | Out-of-tree (8812au, mantenida por morrownr) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | Linux in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | Linux in-kernel (mt76x2u) |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | Out-of-tree (8812au cubierto) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | Out-of-tree (8821cu, mantenida por morrownr) |

## 4. Modelos Aplicables y Chipsets

### 4.1 Modelos ALFA Posibles en DD-WRT (Descontinuados / Antiguos)

| Modelo | Chipset | Controlador | Estado de DD-WRT |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | Algunas versiones de DD-WRT incluyen de fábrica, solo 2.4GHz / 150Mbps |
| AWUS036H | Realtek RTL8187L | rtl8187 | Muy antiguo, algunas versiones lo soportan, solo 2.4GHz / 54Mbps |
| AWUS050NH | Atheros AR9170 | carl9170 / ar9170usb | Muy antiguo, dual banda, pero ha dejado de producirse hace años |

### 4.2 Modelos Actuales No Disponibles en DD-WRT

Todos los modelos actuales de ALFA (véase la tabla del capítulo 3) no están oficialmente soportados por DD-WRT, por los siguientes motivos:

- Chipsets Realtek (RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU): DD-WRT no tiene paquetes de controladores out-of-tree correspondientes
- Chipsets MediaTek (MT7612U / MT7610U / MT7921AUN): DD-WRT no ha integrado los controladores mt76 / mt7921
- Incluso si el router tiene un puerto USB y el nivel de hardware puede identificar el dispositivo (se puede ver VID/PID con lsusb), sin controladores no se puede establecer la interfaz de red

## 5. Requisitos de Entorno

Si el cliente desea intentar usar la tarjeta de red ALFA en DD-WRT, debe cumplir con los siguientes requisitos:

| Ítem | Requisito |
|---|---|
| Hardware del router | Debe tener un puerto USB 2.0 / 3.0 y DD-WRT debe tener habilitado el soporte para el núcleo USB (Servicios > USB) |
| Versión de DD-WRT | Debe ser la versión más reciente de BrainSlayer / Kong compatible con el router, ya que las versiones anteriores tienen menos controladores |
| Espacio de Flash | Al menos 16MB de espacio de Flash (la mayoría de los routers de entrada tienen solo 4-8MB, lo que no permite la instalación de controladores adicionales) |
| RAM | Al menos 128MB de RAM (el controlador de WiFi USB y hostapd ocuparán memoria) |
| Alimentación | El puerto USB debe proporcionar suficiente corriente (cuando el AWUS036ACH tiene una salida de alta potencia puede alcanzar 800mA+, se recomienda usar un Hub USB con fuente de alimentación) |

## 6. Determinación de Compatibilidad

### Matriz de Compatibilidad ALFA Modelos Actuales × DD-WRT

| Modelo | Chipset | Detección de Puertos USB | Carga de Controladores | STA de Conexión a Internet | Modo AP | Monitor | Evaluación General |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ✅（lsusb） | ❌ | ❌ | ❌ | ❌ | No soportado |
| AWUS036AXM | MT7921AUN | ✅ | ❌ | ❌ | ❌ | ❌ | No soportado |
| AWUS036AX | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | No soportado |
| AWUS036AXER | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | No soportado |
| AWUS036ACH | RTL8812AU | ✅ | ❌ | ❌ | ❌ | ❌ | No soportado |
| AWUS036ACHM | MT7610U | ✅ | ❌ | ❌ | ❌ | ❌ | No soportado |
| AWUS036ACM | MT7612U | ✅ | ❌ | ❌ | ❌ | ❌ | No soportado |
| AWUS036ACS | RTL8811AU | ✅ | ❌ | ❌ | ❌ | ❌ | No soportado |
| AWUS036EACS | RTL8811CU | ✅ | ❌ | ❌ | ❌ | ❌ | No soportado |

Criterio de Evaluación: La biblioteca oficial de DD-WRT y la compilación predeterminada del núcleo no incluyen los controladores de WiFi USB para los chips mencionados anteriormente. La visualización de dispositivos en lsusb solo indica la identificación a nivel de la placa de conexión USB y no garantiza la funcionalidad de la red.

## 7. Detallados pasos a paso para la configuración

Dado que los modelos actuales de ALFA no son compatibles con DD-WRT, esta sección proporciona dos rutas alternativas:

### Ruta A: Confirmar si su router DD-WRT realmente no es compatible (pasos de depuración)

**Paso 1: Ingresar a la interfaz de administración de DD-WRT**

Ingrese `192.168.1.1` (o la dirección IP de su router) en el navegador.

**Paso 2: Activar la soporte USB**

- Vaya a Services > USB
- Marque Core USB Support、USB 2.0 Support、USB 3.0 Support (si está disponible)
- Marque USB Wireless Device Support (si está disponible)
- Haga clic en Save > Apply Settings

**Paso 3: Inserte la tarjeta de red ALFA en el puerto USB del router**

**Paso 4: Ingrese al router a través de SSH para verificar**

```bash
# Verifique si el dispositivo USB se detectó
lsusb
# La salida esperada debe incluir el VID/PID de la tarjeta de red ALFA, por ejemplo:
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter

# Verifique si se creó una interfaz de red
ip link show
# Si no hay nuevas interfaces de red como wlan0 / wlan1, significa que el controlador no se ha cargado

# Verifique los registros del núcleo
dmesg | tail -30
# Si aparece "no driver" o solo hay mensajes de enumeración de USB, verifique que falta el controlador
```

**Paso 5: Verifique los módulos de controladores WiFi disponibles**

```bash
# Liste los controladores inalámbricos cargados
lsmod | grep -E "ath|rt2|rtl|mt76|mac80211|cfg80211"
# Si solo hay controladores de WiFi integrados en el router (como wl / b43 / ath9k), significa que falta el controlador WiFi USB
```

**Paso 6: Intente instalar el controlador comunitario (si está disponible)**

```bash
ipkg update
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# Si el resultado de la búsqueda está vacío, verifique que la versión de DD-WRT no tiene controladores disponibles
```

### Ruta B: Solución alternativa sugerida — Cambiar a OpenWrt

Si el cliente necesita usar la tarjeta de red WiFi ALFA USB en el router, se recomienda encarecidamente cambiar el firmware del router de DD-WRT a OpenWrt. OpenWrt tiene una biblioteca de controladores WiFi USB activa, que admite chips MT7612U / MT7610U / RTL8812AU, entre otros. Para obtener los pasos detallados, consulte [¿Es compatible la tarjeta de red inalámbrica ALFA con OpenWrt?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/).

## 8. Errores Comunes y Soluciones

| Síntoma | Posibles Causas | Solución |
|---|---|---|
| No se ve la tarjeta de red ALFA en lsusb | Falta de alimentación USB / Contacto inadecuado / DD-WRT no ha activado el núcleo USB | Verificar en Services > USB si se ha activado; cambiar el puerto USB o usar un Hub USB con alimentación |
| Se ve en lsusb pero no hay interfaz wlan con ip link | Faltan los controladores para el chip correspondiente | Confirmar si la versión de DD-WRT tiene el controlador correspondiente; en la mayoría de los casos, no hay solución, se recomienda cambiar a OpenWrt |
| Hay interfaz wlan pero no se puede escanear AP | Los controladores no son completamente compatibles / Conflictos en modo de escucha | Revisar dmesg para ver si hay errores en la carga del firmware; confirmar la configuración de Regulatory Domain |
| Se pierden los ajustes después de reiniciar el router | Espacio insuficiente en NVRAM de DD-WRT | Evitar instalar controladores adicionales en routers de bajo nivel; considerar actualizar el hardware o cambiar a OpenWrt |
| AWUS036ACH se desconecta cuando se usa salida de alta potencia | Falta de alimentación del puerto USB | Usar un Hub USB 3.0 con alimentación; reducir la configuración de TX Power |

## 9. Limitaciones Conocidas

- **Falta de controladores**: DD-WRT oficial no proporciona controladores USB WiFi para los modelos activos de ALFA, lo cual es la limitación más fundamental.
- **Recursos de hardware**: La mayoría de los routers que pueden flashed con DD-WRT tienen un Flash (4-16MB) y RAM (32-128MB) limitados, incluso con controladores, puede que no sea posible instalarlos.
- **No soporte para Monitor Mode y Packet Injection**: La arquitectura USB WiFi de DD-WRT no admite Monitor Mode y Packet Injection necesarios para las pruebas de penetración.
- **Inestabilidad en modo AP**: Incluso si los chips Ralink antiguos pueden funcionar, el modo AP de USB WiFi en DD-WRT suele presentar problemas de desconexión y rendimiento.
- **Fragmentación de versiones**: Las versiones de compilación de DD-WRT para diferentes modelos de routers difieren significativamente, lo que no garantiza que un controlador de una versión funcione en otra.
- **No mantenimiento activo**: El ritmo de desarrollo de DD-WRT se ha ralentizado, por lo que la posibilidad de agregar nuevos controladores USB WiFi es baja.
- **Complemento**: Incluso dejando de lado las limitaciones propias de DD-WRT, el mantenedor de los controladores de los modelos AWUS036AX / AXER (RTL8832BU), morrownr, ha recomendado abiertamente a los usuarios de Linux evitar esta serie de chips (ver [¿Es compatible el router inalámbrico ALFA con OpenWrt?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) Capítulo 9), y no es solo un problema del plataforma DD-WRT.

Condiciones de rebate: Si el cliente utiliza versiones de compilación comunitarias con controladores adicionales como BrainSlayer / Kong, las condiciones de soporte podrían ser diferentes; esta determinación se realiza con base en las versiones oficialmente publicadas.

## 10. Referencias URL

| Fuente | Descripción | URL | Estado de verificación | Fecha de verificación |
|---|---|---|---|---|
| Wiki oficial de DD-WRT | Entrada principal de instalación / soporte / FAQ | https://wiki.dd-wrt.com/wiki/Main_Page | ✅ Verificado | 2026-09-03 |
| Wiki oficial de DD-WRT — Instalación | Instrucciones de instalación (con soporte USB) | https://wiki.dd-wrt.com/wiki/Installation | ✅ Verificado a través de la liga desde la página principal | 2026-09-03 |
| Documentos oficiales de OpenWrt | Referencia de comparación de WiFi USB | https://openwrt.org/docs/start | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Controladores Linux para RTL8812AU (no integrados en DD-WRT) | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| Catálogo de productos de ALFA Network (Yupitek) | Especificaciones de productos actuales de ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |

Artículos relacionados: [¿Soporta el adaptador inalámbrico ALFA OpenWrt?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) | [¿Soporta el adaptador inalámbrico ALFA Tomato?](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)

Aviso legal: La determinación de la compatibilidad de este documento se realiza en función del estado del controlador del chip y la biblioteca de paquetes oficiales de DD-WRT. Existe una gran cantidad de versiones de compilación personalizadas en la comunidad de DD-WRT, y si el cliente utiliza una versión no oficial, los resultados reales pueden ser diferentes. Se recomienda al cliente utilizar OpenWrt como opción preferente para el WiFi USB en los routers.
