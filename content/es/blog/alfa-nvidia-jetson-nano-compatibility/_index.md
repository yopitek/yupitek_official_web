---
title: "Soporte del Tarjeta de Red Inalámbrica ALFA para NVIDIA Jetson Nano"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-jetson-nano-compatibility"
tags:
  - "ALFA"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "NVIDIA"
  - "Jetson-Nano"
  - "JetPack"
  - "ARM64"
  - "Linux-WiFi"
categories:
  - "Guía de Hardware"
description: "Jetson Nano supports many ALFA network cards, with limitations on older Linux kernel versions. Realtek models are easy to compile, while MediaTek and Wi-Fi 6E models have compatibility issues."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumen del Problema

Pregunta del cliente: «¿El adaptador inalámbrico USB de la serie ALFA puede utilizarse en la placa de desarrollo NVIDIA Jetson Nano?»

Conclusión breve: El Jetson Nano es compatible con la mayoría de los adaptadores inalámbricos de la serie ALFA, aunque hay limitaciones clave debido a que el kernel Linux 4.9 de JetPack 4.x es una versión más antigua (evaluación: de los 9 modelos de adaptadores USB de ALFA en servicio, 3 son compatibles, 2 requieren compilación avanzada, 2 no han sido verificados y 2 no son compatibles). Los modelos con chip Realtek (AWUS036ACH / ACS / EACS) pueden ser compilados directamente con el driver out-of-tree, lo que los convierte en una opción útil para el Jetson Nano; los modelos MediaTek MT7612U / MT7610U necesitan backport o compilación personalizada del driver mt76. El modelo MT7921AUN de Wi-Fi 6E (AWUS036AXML / AXM) no es compatible en el Jetson Nano debido a que requiere un kernel 5.19 o superior. En escenarios de prueba de penetración, el AWUS036ACH (RTL8812AU) es la opción preferida, mientras que en escenarios de navegación general, se prefiere el AWUS036ACH (estable) o el AWUS036ACM (requiere compilación mt76).

## 2. Análisis de la Arquitectura de Especificaciones de Hardware Objetivo

### 2.1 Especificaciones de Hardware de NVIDIA Jetson Nano

| Ítem | Especificación |
|---|---|
| Módulo | Módulo Jetson Nano (P3448) |
| CPU | Cuatro núcleos ARM Cortex-A57 (ARMv8-A / aarch64) |
| GPU | NVIDIA Maxwell, 128 núcleos CUDA |
| Memoria | 4GB LPDDR4 (64-bit, 25.6 GB/s) |
| Almacenamiento | microSD (placa de desarrollo) / eMMC (módulo de producción) |
| USB | 4x USB 3.0 Type-A + 1x USB 2.0 Micro-B (Modo Dispositivo / Alimentación) |
| Red | 1x Gigabit Ethernet (RJ45) |
| Inalámbrico | Sin WiFi / Bluetooth integrados (requiere conexión USB o M.2) |
| Alimentación | Conector DC 5V/4A (recomendado) o micro-USB 5V/2A |
| Tamaño | 100mm × 80mm (placa de desarrollo) |

### 2.2 Entorno de Software: JetPack 4.x

| Ítem | Contenido |
|---|---|
| Sistema Operativo | Linux for Tegra (L4T), basado en Ubuntu 18.04 LTS |
| Versión del Kernel | Linux 4.9 (L4T R32.x / JetPack 4.6.x) |
| Arquitectura | aarch64 (ARM64) |
| Compilador | GCC 7.5 (predeterminado) / GCC 8 (instalable) |
| Versión más reciente | JetPack 4.6.4 (L4T R32.7.4), en modo de mantenimiento |
| Actualizaciones posteriores | Jetson Nano no admite JetPack 5.x (kernel 5.10) debido a limitaciones de hardware |

### 2.3 Limitaciones Clave: Kernel 4.9

El kernel 4.9 de Jetson Nano es un factor determinante de la compatibilidad:

| Controlador | Versión del kernel que ingresa a mainline | Compatibilidad de Jetson Nano (kernel 4.9) |
|---|---|---|
| mt76x2u (MT7612U) | 4.19 | ❌ Necesita backport / compilación personalizada |
| mt76x0u (MT7610U) | 4.19 | ❌ Necesita backport / compilación personalizada |
| mt7921u (MT7921AUN) | 5.19 | ❌ Inutilizable (diferencias demasiado grandes) |
| rtl8812au (RTL8812AU) | Nunca ingresó a mainline | ✅ Se puede compilar un controlador out-of-tree |
| rtl8821cu (RTL8811CU) | Nunca ingresó a mainline | ✅ Se puede compilar un controlador out-of-tree |
| rtw89 (RTL8832BU) | 5.16 (PCIe) / USB integrado gradualmente | ❌ Necesita compilación personalizada, compatibilidad desconocida |

### 2.4 Limitaciones de Alimentación USB

Los 4 puertos USB 3.0 Type-A de la placa de desarrollo Jetson Nano comparten un presupuesto de alimentación:

- Con alimentación DC (5V/4A), la salida total de los puertos USB es aproximadamente 1.5A (5V)
- Con alimentación micro-USB (5V/2A), la salida total de los puertos USB es solo aproximadamente 0.5A
- Tarjeta de red de alta potencia ALFA (AWUS036ACH) puede alcanzar un pico de 800mA-1A
- Recomendación: usar alimentación DC + Hub USB 3.0 con alimentación, para evitar cortes de energía o reinicios del sistema debido a insuficiencia de alimentación

## 3. Análisis de las Especificaciones y Chipsets de las Tarjetas de Red ALFA

Hasta septiembre de 2026, la línea de productos de tarjetas de red USB inalámbricas de ALFA Network en servicio es la siguiente:

| Modelo | Nivel Wi-Fi | Chipset | Interfaz | Compatibilidad con Jetson Nano |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ Requiere kernel 5.19+, no disponible |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ Igual que el anterior |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Requiere rtl8852bu personalizado, no verificado |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Igual que el anterior |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ Compilación de morrownr/8812au, maduro |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ⚠️ Requiere backport mt76x0u |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ⚠️ Requiere backport mt76x2u |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ✅ Cubierto por el controlador de 8812au |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ✅ Compilación de morrownr/8821cu |

## 4. Modelos Aplicables y Conjuntos de Chip

### 4.1 Clasificación de Recomendación

| Nivel de Recomendación | Modelo (Conjunto de Chip) | Descripción |
|---|---|---|
| ⭐ Recomendación Fuerte (Pruebas de Infiltración) | AWUS036ACH (RTL8812AU) | Controladores maduros, soporte Monitor Mode + Packet Injection, tarjeta de red ALFA más utilizada en Jetson Nano |
| ✅ Recomendación (Conexión a Internet General) | AWUS036ACH (RTL8812AU) | AC1200, instalación de controladores sencilla, estable |
| ✅ Recomendación (Bajo Consumo) | AWUS036EACS (RTL8811CU) | AC600, bajo consumo de USB 2.0, adecuado para conexión a Internet simple |
| ✅ Recomendación (Entrada) | AWUS036ACS (RTL8811AU) | AC433, cubierto por el controlador de 8812au |
| ⚠️ Disponible pero Requiere Traducción Manual | AWUS036ACM (MT7612U) | Requiere backport de controladores mt76 al kernel 4.9, barrera técnica alta |
| ⚠️ Disponible pero Requiere Traducción Manual | AWUS036ACHM (MT7610U) | Como anterior, solo 433Mbps |
| ⚠️ No Verificado / No Recomendado | AWUS036AX / AXER (RTL8832BU) | Wi-Fi 6, requiere traducción rtl8852bu, compatibilidad con kernel 4.9 no verificada |
| ❌ No Disponible | AWUS036AXML / AXM (MT7921AUN) | Wi-Fi 6E, requiere kernel 5.19+, Jetson Nano no puede actualizarse |

### 4.2 Recomendaciones de Escenarios de Uso

| Escenario de Uso | Modelo Recomendado | Descripción |
|---|---|---|
| Pruebas de Infiltración / Monitoreo / Inyección Inalámbrica | AWUS036ACH | Controladores RTL8812AU que soportan Monitor + Injection, verificación comunitaria exhaustiva |
| Control Inalámbrico de Robots / Drones | AWUS036ACH o AWUS036EACS | Conexión estable, baja latencia |
| Conexión a Internet en Puntos de Acceso IoT | AWUS036EACS / ACS | Bajo consumo, USB 2.0 suficiente, ahorro de energía |
| Necesidad de Conexión a Internet de Alta Velocidad en 5GHz | AWUS036ACH | AC1200, 867Mbps en 5GHz |
| Necesidad de Wi-Fi 6 / 6E | ❌ Sin opciones disponibles | Jetson Nano no admite chips Wi-Fi 6/6E modernos |

## 5. Requisitos de Entorno

### 5.1 Requisitos de Hardware

| Ítem | Requisitos Mínimos | Recomendado |
|---|---|---|
| Placa de desarrollo Jetson Nano | Versión B01 / A02 | B01 (2 puertos CSI de cámara) |
| Tipo de alimentación | 5V/2A micro-USB | Conector DC de 5V/4A (requerido cuando se utilizan múltiples dispositivos USB) |
| Hub USB | No es necesario | Hub USB 3.0 con alimentación (al usar tarjetas de red de alta potencia) |
| Refrigeración | Placa de refrigeración (incluso por defecto) | Ventilador + placa de refrigeración (para cargas pesadas a largo plazo) |
| Almacenamiento | 16GB microSD | 32GB+ UHS-I microSD (requerido para espacio de compilación de controladores) |

### 5.2 Requisitos de Software

| Ítem | Requisitos |
|---|---|
| Versión de JetPack | 4.6.x (L4T R32.7.x) |
| Herramientas de núcleo | build-essential, git, bc, libssl-dev, flex, bison |
| Código fuente del Kernel | Se requiere descargar el código fuente del kernel correspondiente a la versión L4T (para la compilación de mt76 backport) |
| Red | Conexión a red有线网络 (durante el período de compilación a través de la toma Ethernet Gigabit) |

## 6. Determinación de Compatibilidad

### Matriz de Compatibilidad entre Modelos Actuales de ALFA y NVIDIA Jetson Nano

| Modelo | Procesador | Método de Control | Detección de USB | Conexión STA | Modo AP | Monitor | Dificultad de Instalación | Evaluación General |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | Compilación 8812au | ✅ | ✅ | ✅ | ✅ | Media | ⭐ Mejor |
| AWUS036ACS | RTL8811AU | Cubrimiento 8812au | ✅ | ✅ | ⚠️ | ❌ | Media | ✅ Buena |
| AWUS036EACS | RTL8811CU | Compilación 8821cu | ✅ | ⚠️ | ❌ | ❌ | Media | ✅ Buena |
| AWUS036ACM | MT7612U | Backport mt76x2u | ✅ | ✅ | ✅ | ✅ | Alta | ⚠️ Disponible |
| AWUS036ACHM | MT7610U | Backport mt76x0u | ✅ | ✅ | ⚠️ | ⚠️ | Alta | ⚠️ Disponible |
| AWUS036AX | RTL8832BU | Compilación rtl8852bu | ⚠️ | ❌ | ❌ | ❌ | Alta | ❌ No recomendado |
| AWUS036AXER | RTL8832BU | Igual que anterior | ⚠️ | ❌ | ❌ | ❌ | Alta | ❌ No recomendado |
| AWUS036AXML | MT7921AUN | Necesita kernel 5.19+ | ❌ | ❌ | ❌ | ❌ | — | ❌ No disponible |
| AWUS036AXM | MT7921AUN | Igual que anterior | ❌ | ❌ | ❌ | ❌ | — | ❌ No disponible |

Criterios de Determinación: Disponibilidad de controladores para el kernel 4.9 de JetPack 4.x de NVIDIA Jetson Nano + Informes de pruebas de la comunidad (Foro de NVIDIA Jetson Nano, issue de GitHub morrownr). MT7921AUN se considera no disponible debido a que NVIDIA Jetson Nano no puede actualizarse al kernel 5.19+.

## 7. Detallados pasos a paso para la configuración

### 7.1 Trabajo previo: Actualización del sistema y entorno de compilación

**Paso 1: Iniciar y acceder a Jetson Nano mediante SSH**

```bash
ssh username@<jetson-nano-ip>
```

**Paso 2: Actualizar paquetes del sistema**

```bash
sudo apt update
sudo apt upgrade -y
```

**Paso 3: Instalar herramientas de compilación y dependencias**

```bash
sudo apt install -y build-essential git bc libssl-dev flex bison dkms
```

**Paso 4: Confirmar la versión del kernel**

```bash
uname -r
# Salida esperada: 4.9.337-tegra (o similar a 4.9.x-tegra)
```

### 7.2 Ruta A: Modelos de chip Realtek (AWUS036ACH / ACS / EACS) — Recomendado

Tomando como ejemplo AWUS036ACH (RTL8812AU):

**Paso 1: Descargar el código fuente del controlador**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**Paso 2: (Opcional) Ajustar parámetros de compilación para ARM64**

Edite Makefile y asegúrese de que la siguiente configuración esté activada:

```
CONFIG_PLATFORM_ARM64 = y
```

(En la mayoría de las versiones recientes de Makefile se detecta automáticamente aarch64)

**Paso 3: Compilar e instalar**

```bash
make
sudo make install
```

**Paso 4: Cargar el módulo del controlador**

```bash
sudo modprobe 8812au
# O reiniciar
sudo reboot
```

**Paso 5: Insertar la tarjeta de red ALFA y confirmar la interfaz de red**

```bash
ip link show
# Salida esperada: wlan0
# Si no aparece, revise dmesg
dmesg | grep -i "8812au\|rtl8812\|usb"
```

**Paso 6: Escanear redes WiFi (verificación de funcionalidad)**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**Paso 7: Conectar a una red WiFi (usando NetworkManager / nmcli)**

```bash
# Jetson Nano tiene instalado por defecto NetworkManager
nmcli dev wifi list
nmcli dev wifi connect "Nombre de su WiFi" password "Contraseña de su WiFi"
```

**Paso 8: (Opcional) Configurar como punto de acceso (AP) (pruebas de penetración)**

```bash
# Instalar hostapd y dnsmasq
sudo apt install -y hostapd dnsmasq
# Consulte la guía de ALFA Soft AP
# https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/
```

**Paso 9: Activar el modo de escucha (pruebas de penetración)**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# Verificación
sudo iw dev wlan0 info
# type debe mostrar monitor
# Prueba de inyección de paquetes
sudo aireplay-ng --test wlan0
```

### 7.3 Ruta B: Modelos de chip MediaTek (AWUS036ACM / ACHM) — Avanzado

Tomando como ejemplo AWUS036ACM (MT7612U), se necesita backport del controlador mt76:

**Paso 1: Descargar el código fuente del kernel de Jetson Nano**

```bash
# Descargar el código fuente del kernel correspondiente a la versión de L4T
# Por ejemplo, para L4T R32.7.4:
wget https://developer.nvidia.com/embedded/l4t/r32_release_v7.4/sources/public_sources.tbz2
tar -xjf public_sources.tbz2
cd Linux_for_Tegra/source/public
tar -xjf kernel_src.tbz2
```

**Paso 2: Preparar el entorno de compilación del kernel**

```bash
cd kernel/kernel-4.9
# Generar configuración predeterminada
make tegra_defconfig
# Activar opciones relacionadas con mt76 en menuconfig
make menuconfig
# Navegue a: Device Drivers > Network device support > Wireless LAN
# Seleccione: <M> MediaTek MT76x2U USB support
# Seleccione: <M> MediaTek MT76x0U USB support
```

**Paso 3: Compilar los módulos del kernel**

```bash
make modules_prepare
make M=drivers/net/wireless/mediatek/mt76 modules
```

**Paso 4: Instalar los módulos**

```bash
sudo make M=drivers/net/wireless/mediatek/mt76 modules_install
sudo depmod -a
```

**Paso 5: Cargar el controlador**

```bash
sudo modprobe mt76x2u
# Insertar AWUS036ACM
dmesg | grep mt76
ip link show
```

⚠️ Advertencia: Backport de mt76 al kernel 4.9 puede encontrar errores de compilación y necesitar correcciones manuales en el código fuente. Esta es una operación avanzada y se recomienda solo a usuarios con experiencia en la compilación del kernel. Si encuentra dificultades, se recomienda cambiar a AWUS036ACH (RTL8812AU).

### 7.4 Ruta C: Modelos Wi-Fi 6 / 6E (AWUS036AX / AXER / AXML / AXM)

- AWUS036AXML / AXM (MT7921AUN): No disponible. El kernel 4.9 de Jetson Nano no se puede actualizar a 5.19+, y el controlador mt7921u no se puede backport (diferencias demasiado grandes, dependencias de infraestructura del kernel moderno).
- AWUS036AX / AXER (RTL8832BU): No recomendado. Teóricamente, se puede intentar compilar el controlador morrownr/rtl8852bu, pero la compatibilidad con el kernel 4.9 no ha sido verificada por la comunidad y es posible que las funciones Wi-Fi 6 no funcionen correctamente. Si se necesita Wi-Fi 6, se recomienda usar Jetson Orin Nano (JetPack 5.x, kernel 5.10+) o una computadora x86.

## 8. Errores Comunes y Soluciones

| Síntoma | Posible Causa | Solución |
|---|---|---|
| Después de insertar la tarjeta de red, dmesg no muestra ninguna reacción | Falta de alimentación USB / Contacto inadecuado | Utilizar alimentación DC (5V/4A); Cambiar el puerto USB; Utilizar un Hub USB con alimentación |
| Error al compilar 8812au con make: gcc: error: unrecognized command line option | Versión de GCC muy antigua | Instalar GCC 8: `sudo apt install gcc-8 g++-8` y especificar `CC = gcc-8` en el Makefile |
| modprobe 8812au informa de Required key not available | Secure Boot activado (el Jetson Nano generalmente no tiene este problema) | Confirmar que el Jetson Nano no tiene activado Secure Boot; refirmar el módulo o desactivar Secure Boot |
| La interfaz wlan0 aparece pero no puede escanear AP | No se ha configurado el dominio regulatorio / Faltan los controladores del firmware | Configurar el dominio regulatorio: `sudo iw reg set TW`; verificar si dmesg muestra errores de carga de firmware |
| Al usar alta potencia de salida, el sistema se reinicia o la tarjeta de red se desconecta | Falta de alimentación USB | Utilizar alimentación DC + Hub USB con alimentación; reducir el TX Power: `sudo iw dev wlan0 set txpower fixed 2000` |
| En modo de escucha, aireplay-ng --test muestra Injection is working! pero el ataque es ineficaz | Funcionalidad de inyección del controlador limitada / Colisión de canales | La función de inyección de RTL8812AU es básicamente utilizable; confirmar que `airmon-ng check kill` ha detenido NetworkManager; intentar diferentes canales |
| Falla al compilar mt76 backport | La diferencia entre el kernel 4.9 y el código original de mt76 es demasiado grande | Intentar usar una versión más antigua de mt76 (correspondiente al commit de kernel 4.19); o usar AWUS036ACH |
| Después de que el sistema se despierta, la tarjeta de red desaparece | Configuración de ahorro de energía USB | Desactivar el apagado automático USB: `echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |
| No se puede usar el 5GHz de AWUS036ACH | Restricciones de dominio regulatorio / Tabla de canales del controlador | Configurar `sudo iw reg set US` (EE. UU. tiene más canales de 5GHz abiertos); confirmar que el canal utilizado está permitido por las regulaciones locales |

## 9. Limitaciones Conocidas

- **Versión del Kernel congelada en 4.9**: El Jetson Nano no es compatible con JetPack 5.x, no puede actualizar el kernel, lo que es la raíz de todos los problemas de compatibilidad
- **MT7921AUN (Wi-Fi 6E) completamente inutilizable**: Requiere kernel 5.19+, no puede backportarse a 4.9
- **Necesidad de backport manual de MediaTek mt76**: Los usuarios de AWUS036ACM / ACHM deben compilar el módulo del kernel ellos mismos, lo que representa un alto umbral técnico
- ⚠️ **Recomendación explícita del mantenedor del driver de Wi-Fi 6 (RTL8832BU)**: El mantenedor morrownr en su anuncio oficial ha señalado que la serie rtl8852/32au "es un mal driver, sospechando problemas en el chip mismo", y ha recomendado a los usuarios de Linux evitar este chip en la actualidad (ver el capítulo 10 para la fuente). Esto es más grave que simplemente "la compatibilidad con kernel 4.9 no está verificada"; la evaluación de AWUS036AX / AXER en este documento y otros documentos relacionados debe entenderse como "no recomendado" en lugar de "puede intentarse pero es más complicado"
- **Limitaciones de alimentación USB**: Cuatro puertos USB comparten aproximadamente 1.5A (alimentación DC), los tarjetas de red de alta potencia deben usar un Hub con fuente de alimentación
- **Rendimiento en modo AP**: La potencia del CPU del Jetson Nano es limitada, y la tasa de transferencia del USB WiFi como AP puede ser menor de lo esperado
- **Diferencias en funciones de escucha/inyección**: RTL8812AU ofrece el mejor soporte; las funciones de inyección de los chips MediaTek en el backport del kernel 4.9 pueden ser inestables
- **Mantenimiento a largo plazo**: JetPack 4.x ha entrado en modo de mantenimiento, no habrá nuevas funciones ni actualizaciones de drivers
- **Función Bluetooth**: La función Bluetooth 5.2 de AWUS036AXM no está verificada en el Jetson Nano (requiere soporte de BlueZ)
- **Disipación de calor**: Al usar el USB WiFi de alta potencia durante un largo período, la temperatura total del Jetson Nano puede aumentar, se recomienda instalar un ventilador

Condiciones de refutación: Las evaluaciones anteriores se basan en JetPack 4.6.x (kernel 4.9). Si NVIDIA libera soporte de JetPack 5.x para el Jetson Nano en el futuro (actualmente no es soportado oficialmente) o si la comunidad presenta un backport de kernel 5.x estable, la evaluación de incompatibilidad en el capítulo 4 debe revisarse nuevamente.

## 10. Referencias URL

| Fuente | Descripción | URL | Estado de verificación | Fecha de verificación |
|---|---|---|---|---|
| Página oficial de NVIDIA Jetson Nano | Especificaciones del hardware de Jetson Nano | https://developer.nvidia.com/embedded/jetson-nano | ✅ Verificado | 2026-09-03 |
| Página oficial de NVIDIA JetPack SDK | Información sobre versiones de JetPack y kernel | https://developer.nvidia.com/embedded/jetpack | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Controladores Linux para RTL8812AU (compatibles con Jetson Nano) | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| morrownr/8821cu GitHub | Controladores Linux para RTL8811CU | https://github.com/morrownr/8821cu-20210916 | ✅ Verificado | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide（Yupitek） | Guía de configuración del modo AP de ALFA en Linux | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verificado | 2026-09-03 |
| ALFA Network Product Overview（Yupitek） | Especificaciones de los productos actuales de ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | Declaración oficial del mantenedor de controladores: se recomienda evitar el chip rtl8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Verificado | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko solo aparecerá en el núcleo con kernel 5.19+ (palabras del mantenedor de controladores) | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ Verificado | 2026-09-03 |

Artículos relacionados: [¿Es compatible el adaptador inalámbrico ALFA con NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)（Comparación con plataforma GB10, entorno de kernel 6.x）｜[¿Es compatible el adaptador inalámbrico ALFA con OpenWrt?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)

Aviso legal: La determinación de compatibilidad de este documento se realiza con base en Jetson Nano JetPack 4.6.x (kernel 4.9). Los controladores para chips Realtek son mantenidos por la comunidad (morrownr), y la estabilidad real puede variar según la versión. La operación de backport para el chip MediaTek mt76 requiere experiencia en compilación de kernel y no se garantiza un 100% de éxito. Si se necesita soporte para Wi-Fi 6/6E o kernel moderno, se recomienda actualizar a la serie Jetson Orin (JetPack 5.x+) o utilizar computadoras x86.
