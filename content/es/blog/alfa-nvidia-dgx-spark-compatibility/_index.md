---
title: "Soporte del Tarjeta Inalámbrica ALFA para NVIDIA DGX Spark (GB10)"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-dgx-spark-compatibility"
tags:
  - "ALFA"
  - "NVIDIA"
  - "DGX-Spark"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "Guía de Hardware"
description: "DGX Spark支持ALFA网卡，MediaTek芯片型无需驱动，Realtek需编译驱动，USB-C转USB-A适配器需用。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumen del Problema

Pregunta del cliente: «¿El adaptador inalámbrico USB de la serie ALFA puede ser utilizado en el supercomputador personal AI NVIDIA DGX Spark (GB10 Grace Blackwell)?»

Conclusión breve: El DGX Spark ejecuta NVIDIA DGX OS (basado en Ubuntu, kernel 6.x), y la compatibilidad del adaptador ALFA con este sistema es similar a la de sistemas de escritorio modernos basados en Linux. Los modelos con chip MediaTek (AWUS036ACM / ACHM / AXML / AXM) utilizan el controlador in-kernel, por lo que son compatibles de fábrica; los modelos con chip Realtek (AWUS036ACH / ACS / EACS / AX / AXER) requieren la compilación de un controlador out-of-tree (para arquitecturas ARM64 / aarch64). Nota: Todos los puertos USB del DGX Spark son de tipo USB Type-C, mientras que los adaptadores ALFA son de tipo USB Type-A, por lo que se requiere un adaptador o cable USB-C to USB-A.

Determinación del sujeto: Se evalúan 9 adaptadores USB de la serie ALFA en uso (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Análisis de la Arquitectura de Especificaciones de Hardware Objetivo

### 2.1 Especificaciones de Hardware de NVIDIA DGX Spark

| Ítem | Especificación |
|---|---|
| Nombre del producto | NVIDIA DGX Spark |
| Chip de núcleo | NVIDIA GB10 Grace Blackwell Superchip |
| CPU | 20-core Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Arquitectura Blackwell de NVIDIA, 6144 núcleos CUDA, quinta generación Tensor Core, cuarta generación RT Core |
| Rendimiento de IA | Hasta 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| Memoria del sistema | 128GB LPDDR5x Memoria unificada (256-bit, 273 GB/s) |
| Almacenamiento | Hasta 4TB NVMe M.2 SSD (autosecundado) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (20Gbps), de los cuales 1 soporta entrada PD (180W EPR PD3.1) |
| Salida de visualización | 1× HDMI 2.1a |
| Red cableada | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (200G QSFP) |
| Red inalámbrica | Wi-Fi 7 (integrado) + Bluetooth 5.4 |
| Sistema operativo | NVIDIA DGX OS (basado en Ubuntu Linux, kernel 6.x) |
| Arquitectura | aarch64 (ARM64) |
| Tamaño | 150 × 150 × 50.5 mm (1.13L) |
| Peso | Aproximadamente 1.2 kg |
| Alimentación | Fuente de alimentación USB-C de 240W |

### 2.2 Entorno de Software: NVIDIA DGX OS

| Ítem | Descripción |
|---|---|
| Base | Ubuntu Linux (personalizado por NVIDIA) |
| Kernel | Linux 6.x (versión específica según la actualización de DGX OS) |
| Arquitectura | aarch64 (ARM64) |
| Software preinstalado | Conjunto de software de IA de NVIDIA (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Gestión de paquetes | apt (sistema Debian/Ubuntu) |
| Framework de controladores | Arquitectura estándar de controladores del kernel Linux (cfg80211 / mac80211) |

### 2.3 Características Clave: Kernel Moderno + ARM64

El entorno de software de DGX Spark tiene dos influencias clave sobre la compatibilidad con las tarjetas de red ALFA:

- Kernel 6.x (moderno): Todos los controladores de WiFi que entren en el mainline se pueden usar directamente, incluyendo mt76 (MT7612U / MT7610U) y mt7921u (MT7921AUN). Esto contrasta marcadamente con el kernel 4.9 de Jetson Nano.
- Arquitectura ARM64 (aarch64): Los controladores out-of-tree de Realtek (8812au / 8821cu / rtl8852bu) necesitan ser compilados en ARM64. El upstream de estos controladores (morrownr) ya soporta la compilación en ARM64, pero se debe confirmar que CONFIG_PLATFORM_ARM64 = y esté en el Makefile.

### 2.4 Necesidades de Conexión de Adaptador USB Type-C

Los 4 puertos USB de DGX Spark son Type-C, mientras que toda la serie de tarjetas de red ALFA (excepto AXML que es USB-C) tienen interfaz USB Type-A:

| Modelo | Especificación de interfaz | ¿Necesita adaptador? |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ No necesita adaptador (se puede insertar directamente) |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ Necesita USB-C to USB-A |
| AWUS036AX | USB Type-A / USB 3.2 | ✅ Necesita |
| AWUS036AXER | USB Type-A / USB 3.2 | ✅ Necesita |
| AWUS036ACH | USB Type-A / USB 3.0 | ✅ Necesita |
| AWUS036ACHM | USB Type-A / USB 2.0 | ✅ Necesita |
| AWUS036ACM | USB Type-A / USB 3.0 | ✅ Necesita |
| AWUS036ACS | USB Type-A / USB 2.0 | ✅ Necesita |
| AWUS036EACS | USB Type-A / USB 2.0 | ✅ Necesita |

Recomendación: Utilice un conector o cable USB-C to USB-A compatible con USB 3.2 Gen 2×2 (20Gbps) para asegurar que los modelos AWUS036ACH / ACM / AX entre otros puedan funcionar a toda velocidad.

## 3. Análisis de las Especificaciones y Chipsets de las Tarjetas de Red ALFA

Hasta septiembre de 2026, la línea de productos de tarjetas de red inalámbricas USB de ALFA Network en servicio es la siguiente (evaluación de la placa base: 9 modelos):

| Modelo | Nivel Wi-Fi | Chipset | Interfaz | Estado del Controlador Linux |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel (mt7921u, kernel 5.19+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel (mt7921u) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 (kernel 5.16+, soporte USB en desarrollo) o out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Igual que el anterior |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree (morrownr/8812au, requiere compilación ARM64) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel (mt76x2u)⭐ Recomendado |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree (8812au cubre) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree (morrownr/8821cu) |

## 4. Modelos Aplicables y Conjuntos de Chip

### 4.1 Clasificación de Recomendaciones

| Nivel de Recomendación | Modelo (Conjunto de Chip) | Descripción |
|---|---|---|
| ⭐ Recomendación Fuerte | AWUS036ACM (MT7612U) | Controlador in-kernel, listo para usar, AC1200 dual banda, soporta AP / Monitor / Injection |
| ✅ Recomendado | AWUS036ACHM (MT7610U) | Controlador in-kernel, bajo consumo de energía, AC433 dual banda |
| ✅ Recomendado (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | Controlador in-kernel, Wi-Fi 6E, AXML con conexión USB-C directa |
| ⚠️ Disponible pero requiere compilación | AWUS036ACH (RTL8812AU) | Requiere compilación de morrownr/8812au (ARM64),完成后功能完整（包括 Monitor / Injection） |
| ⚠️ Disponible pero requiere compilación | AWUS036ACS (RTL8811AU) | Cubierto por el controlador 8812au |
| ⚠️ Disponible pero requiere atención | AWUS036EACS (RTL8811CU) | Requiere compilación de morrownr/8821cu (ARM64) |
| ⚠️ Disponible pero requiere atención | AWUS036AX / AXER (RTL8832BU) | El kernel 6.x de rtw89 puede ya soportar USB; si no es necesario compilar out-of-tree |

### 4.2 Recomendaciones de Escenarios de Uso

| Escenario de Uso | Modelo Recomendado | Descripción |
|---|---|---|
| Conexión inalámbrica general (más simple) | AWUS036ACM / ACHM | Controlador in-kernel, sin necesidad de compilación, listo para usar |
| Pruebas de penetración inalámbrica / escaneo / inyección | AWUS036ACH o AWUS036ACM | Ambos soportan Monitor + Injection; ACH requiere compilación, ACM listo para usar |
| Wi-Fi 6E / Banda 6GHz | AWUS036AXML / AXM | Controlador in-kernel MT7921AUN, soportado por completo en el kernel 6.x |
| Ya tiene AWUS036ACH y desea seguir utilizando | AWUS036ACH | Compilar el controlador ARM64 es suficiente, todas las funciones son completas |
| No necesita WiFi externo (usar interno) | — | DGX Spark ya tiene Wi-Fi 7 + Bluetooth 5.4 integrados, no es necesario conectar una tarjeta de red ALFA para la navegación general |
Nota: DGX Spark ya tiene Wi-Fi 7 + Bluetooth 5.4 integrados, no es necesario conectar una tarjeta de red ALFA para escenarios de navegación general. La conexión externa de ALFA se necesita principalmente para: pruebas de penetración (escaneo/inyección), necesidades de chipsets especiales o escenarios donde el Wi-Fi integrado no es suficiente.

## 5. Requisitos de Entorno

### 5.1 Requisitos de Hardware

| Ítem | Requisitos |
|---|---|
| Conector USB | Conector USB-C a USB-A o cable de transmisión (excepto AXML) |
| Alimentación | Fuente de alimentación USB-C de 240W de fábrica para DGX Spark (alimentación suficiente en el puerto USB) |
| Refrigeración | Refrigeración de fábrica suficiente (el USB WiFi no aumentará significativamente la carga del sistema) |

### 5.2 Requisitos de Software

| Ítem | Requisitos |
|---|---|
| Versión de DGX OS | Cualquier versión en servicio (kernel 6.x) |
| Herramientas de compilación (requeridas para el chip Realtek) | build-essential, git, bc, dkms |
| Herramientas de gestión inalámbrica | iw, wpa_supplicant, network-manager (preinstalado en DGX OS) |
| Red | Red有线网络（期间需要10GbE）或内置Wi-Fi 7联网 |

## 6. Determinación de Compatibilidad

### Matriz de Compatibilidad entre Modelos en Servicio de ALFA y NVIDIA DGX Spark (GB10)

| Modelo | Chipset | Método de Control | Detección de USB | STA de Conexión a Internet | Modo AP | Monitor | Dificultad de Instalación | Evaluación General |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel (mt76x2u) | ✅ | ✅ | ✅ | ✅ | Sin instalación | ⭐ Mejor |
| AWUS036ACHM | MT7610U | in-kernel (mt76x0u) | ✅ | ✅ | ✅ | ⚠️ Limitado | Sin instalación | ✅ Bueno |
| AWUS036AXML | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ Limitado | Sin instalación | ✅ Bueno |
| AWUS036AXM | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ Limitado | Sin instalación | ✅ Bueno |
| AWUS036ACH | RTL8812AU | out-of-tree (8812au) | ✅ | ✅ | ✅ | ✅ | Moderado (compilación) | ⚠️ Disponible |
| AWUS036ACS | RTL8811AU | out-of-tree (8812au) | ✅ | ✅ | ⚠️ | ❌ | Moderado (compilación) | ⚠️ Disponible |
| AWUS036EACS | RTL8811CU | out-of-tree (8821cu) | ✅ | ⚠️ | ❌ | ❌ | Moderado (compilación) | ⚠️ Disponible |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Moderado-Alto | ⚠️ Disponible |
| AWUS036AXER | RTL8832BU | Igual que anterior | ✅ | ⚠️ | ⚠️ | ❌ | Moderado-Alto | ⚠️ Disponible |

Criterios de Determinación: Disponibilidad del kernel 6.x de DGX OS para los controladores principales + soporte de ARM64 para el controlador morrownr. Los chipsets MediaTek, debido a que los controladores ya han sido incluidos en el mainline, son compatibles de fábrica en el kernel 6.x. Los chipsets Realtek requieren la compilación de controladores out-of-tree, pero el soporte de compilación ARM64 ya ha sido proporcionado por el upstream.

## 7. Detallado paso a paso de la configuración

### 7.1 Trabajo previo

**Paso 1: Iniciar y acceder a DGX Spark** (a través de SSH o conexión directa a teclado y pantalla)

```bash
ssh username@<dgx-spark-ip>
```

**Paso 2: Confirmar la arquitectura del sistema y la versión del kernel**

```bash
uname -m
# Esperado: aarch64
uname -r
# Esperado: 6.x.x (kernel de DGX OS)
```

**Paso 3: (Requiere chip Realtek) Instalar herramientas de compilación**

```bash
sudo apt update
sudo apt install -y build-essential git bc dkms
```

### 7.2 Ruta A: Modelos con chip MediaTek (AWUS036ACM / ACHM / AXML / AXM) — Listo para usar sin abrir

**Paso 1: Insertar la tarjeta de red**

Utilice un adaptador USB-C a USB-A para (AXML puede insertarse directamente en el puerto USB-C), y conecte la tarjeta de red ALFA al puerto USB de DGX Spark.

**Paso 2: Confirmar que la tarjeta de red se detecta**

```bash
lsusb
# Salida esperada (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Paso 3: Confirmar que la interfaz de red se ha creado automáticamente**

```bash
ip link show
# Esperado: wlan0 o wlp... (controlador de kernel cargado automáticamente)
```

**Paso 4: Escanear redes WiFi**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**Paso 5: Conectar a una red WiFi (usando NetworkManager**)

```bash
nmcli dev wifi list
nmcli dev wifi connect "Nombre de tu WiFi" password "Contraseña de tu WiFi"
```

**Paso 6: (Opcional) Activar modo monitor**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info
```

### 7.3 Ruta B: Modelos con chip Realtek (AWUS036ACH / ACS / EACS) — Requiere compilación

Tomando AWUS036ACH (RTL8812AU) como ejemplo:

**Paso 1: Descargar el código fuente del controlador**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**Paso 2: Confirmar la opción de compilación para ARM64**

Edite Makefile, asegúrese de que `CONFIG_PLATFORM_ARM64 = y` (la mayoría de las versiones nuevas detectan automáticamente aarch64).

**Paso 3: Compilar e instalar**

```bash
make
sudo make install
sudo modprobe 8812au
```

**Paso 4: Insertar la tarjeta de red ALFA (a través de un adaptador USB-C a USB-A), confirmar la interfaz**

```bash
ip link show
# Esperado: wlan0
```

**Paso 5: Método de conexión igual que en el Paso 5 de la Ruta 7.2 (usando nmcli**)

**Paso 6: (Opcional) Modo monitor y inyección**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

### 7.4 Ruta C: Modelos Wi-Fi 6 (AWUS036AX / AXER, RTL8832BU)

**Paso 1: Verificar si el kernel ya tiene soporte para rtw89 USB**

```bash
# Verifique después de insertar la tarjeta de red
lsusb
dmesg | grep -i "rtw89\|rtl8852\|8832"
ip link show
# Si wlan0 aparece automáticamente, el rtw89 del kernel 6.x ya tiene soporte y se puede usar directamente
```

**Paso 2: Si el kernel no tiene soporte automático, compilar el controlador out-of-tree**

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
# Asegúrese de que CONFIG_PLATFORM_ARM64 = y
make
sudo make install
sudo modprobe rtl8852bu
```

## 8. Errores Comunes y Soluciones

| Síntoma | Posible Causa | Solución |
|---|---|---|
| No se ve la tarjeta de red ALFA en lsusb | Adaptador USB-C defectuoso / Conexión inestable | Cambiar el adaptador USB-C a USB-A; verificar que el adaptador es compatible con la transferencia de datos (no solo carga); intentar con un puerto USB-C diferente |
| Después de insertar el chip MediaTek, no hay interfaz wlan | El módulo del kernel no se carga automáticamente / Firmware faltante | Cargar manualmente: `sudo modprobe mt76x2u`; verificar `dmesg | grep mt76`; instalar firmware: `sudo apt install linux-firmware` |
| El driver de Realtek informa de errores al ejecutar make aarch64-linux-gnu-gcc: not found | Configuración de compilación cruzada incorrecta | Confirmar la compilación nativa en DGX Spark (no compilación cruzada); no debe establecerse CROSS_COMPILE en Makefile |
| modprobe 8812au informa de Operation not permitted | Secure Boot / Firmware firmado | DGX Spark no tiene habilitado por defecto Secure Boot; si está habilitado, firmar el módulo o deshabilitar Secure Boot |
| Conexión WiFi inestable / velocidad lenta | El adaptador USB-C solo admite USB 2.0 | Cambiar a un adaptador que admite USB 3.2 Gen 2×2; verificar que el adaptador esté marcado como «Data» y no como «Charge Only» |
| El Wi-Fi interno y el ALFA externo chocan | Colisión de interfaces inalámbricas | Desactivar el Wi-Fi interno: `sudo nmcli radio wifi off` o desactivar en BIOS/UEFI; o configurar el orden de prioridad de las rutas |
| No se puede usar 6GHz (Wi-Fi 6E) | Restricciones del dominio regulatorio | Establecer el dominio regulatorio: `sudo iw reg set US` (Estados Unidos abre 6GHz); verificar que el firmware del AWUS036AXML/AXM admite 6GHz |
| Falla al iniciar el modo AP | Conflictos entre NetworkManager y hostapd | Referirse a la guía de Yupitek ALFA Soft AP; desactivar NetworkManager para gestionar la interfaz y configurar manualmente hostapd |
| La tarjeta de red desaparece después de despertar | Suspensión automática de USB | Desactivar la suspensión automática de USB: `echo 'options usbcore autosuspend=-1' | sudo tee /etc/modprobe.d/usb.conf` |

## 9. Restricciones Conocidas

- **Requisito de adaptador USB Type-C**: Además de AXML, todos los tarjetas de red ALFA requieren un adaptador USB-C a USB-A, la calidad del adaptador puede afectar el rendimiento y la estabilidad.
- **Traducción manual de chipsets Realtek**: RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU no han sido incluidos en el mainline, requieren la traducción de controladores out-of-tree en ARM64.
- **Posible conflicto con Wi-Fi externo**: DGX Spark incluye Wi-Fi 7 integrado, y al usar simultáneamente Wi-Fi interno y externo puede ocurrir conflictos de enrutamiento o recursos.
- **Configuración manual del modo AP**: DGX OS se preconfigura como entorno de desarrollo, el modo de punto de acceso (AP) requiere la instalación y configuración manual de hostapd / dnsmasq.
- **Restricciones regulatorias de 6GHz**: La disponibilidad del rango de frecuencia 6GHz de Wi-Fi 6E depende de la configuración regulatoria de la región, se debe confirmar la situación de apertura de 6GHz en Taiwán según la última regulación.
- **Actualización de controladores dependiente de componentes superiores**: Los controladores out-of-tree de Realtek son mantenidos por la comunidad (morrownr), después de la actualización del kernel de DGX OS puede ser necesario recompilar.
- **Diferencias en las pruebas de penetración**: La función de inyección de la serie MediaTek mt76 ha mejorado en el kernel 6.x, pero RTL8812au sigue siendo la opción tradicional preferida por la comunidad de pruebas de penetración.
- **Función Bluetooth**: La función Bluetooth 5.2 del AWUS036AXM no ha sido verificada ampliamente en DGX OS (DGX Spark incluye BT 5.4 integrado).
- ⚠️ **Se recomienda evitar el uso de RTL8832BU (AWUS036AX/AXER)**: El mantenedor del controlador, morrownr, ha emitido una declaración oficial indicando que la serie rtl8852/32au "es un controlador muy malo, sospechando problemas en el chip en sí", recomendando a los usuarios de Linux evitar su uso en la actualidad (fuente en la sección 10). La calificación "⚠️ Utilizable pero con precauciones" de estos modelos en las secciones 4 y 6 debe entenderse como un consenso del sector que tiende a no recomendarlos, no solo por problemas de instalación.
- **Determinación de "out-of-tree" de RTL8812AU**: La información proporcionada para 2026 es inicial; en realidad, el controlador in-kernel compatible con el estándar mac80211 de este chip se integró en el kernel 6.13 y alcanzó madurez en la versión 6.14 (anuncio oficial de morrownr), si DGX OS utiliza un núcleo 6.14 o superior, AWUS036ACH tiene la oportunidad de utilizarse sin necesidad de recompilación, se recomienda a los servicios de atención al cliente que antes de responder pidan a los clientes que informen `uname -r` para confirmar.

Condiciones de refutación: Si después de la actualización de DGX OS cambia la versión del kernel o el controlador del controlador USB, o si el mantenimiento del controlador morrownr de la rama ARM64 se detiene, se debe revisar nuevamente la matriz de compatibilidad de la sección 6; si el soporte USB de rtw89 se implementa completamente en el kernel 6.x, la calificación de AWUS036AX / AXER puede ser actualizada de "utilizable pero con precauciones" a "disponible".

## 10. Referencias URL

| Fuente | Descripción | URL | Estado de verificación | Fecha de verificación |
|---|---|---|---|---|
| Página oficial de NVIDIA DGX Spark | Especificaciones y plataforma de DGX Spark | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| Documentos de NVIDIA DGX | Arquitectura del sistema operativo DGX y versión del kernel | https://docs.nvidia.com/dgx/dgx-spark | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Controladores Linux para RTL8812AU (soporte ARM64) | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| morrownr/8821cu GitHub | Controladores Linux para RTL8811CU | https://github.com/morrownr/8821cu-20210916 | ✅ Verificado | 2026-09-03 |
| morrownr/rtl8852bu GitHub | Controladores Linux para RTL8832BU | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Verificado | 2026-09-03 |
| Documentos de controladores mt76 del kernel Linux | Documentación de los controladores MediaTek mt76 / mt7921 mainline (versión de kernel de inicio de soporte para cada chip) | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ Verificado | 2026-09-03 |
| Guía de Linux para Soft AP WiFi Hotspot ALFA (Yupitek) | Guía de configuración del modo AP en Linux para ALFA | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verificado | 2026-09-03 |
| Catálogo de productos de Network ALFA (Yupitek) | Especificaciones de productos actuales de ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |
| Issue #314 de morrownr/USB-WiFi | Declaración oficial del mantenedor de controladores: se recomienda evitar los chips rtl8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Verificado | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | Anuncios más recientes sobre el estado del controlador RTL8812AU (incorporado en la línea principal del kernel 6.13, maduro en calidad para el kernel 6.14) | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |

Artículos relacionados: [¿Soporta la tarjeta inalámbrica ALFA el MSI EdgeXpert?](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)｜[¿Soporta la tarjeta inalámbrica ALFA el ASUS Ascent GX10?](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[¿Soporta la tarjeta inalámbrica ALFA el ALTOS BrainSphere GB10 F1?](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[¿Soporta la tarjeta inalámbrica ALFA el GIGABYTE AI TOP ATOM?](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[¿Soporta la tarjeta inalámbrica ALFA el NVIDIA Jetson Nano?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Aviso legal: La determinación de compatibilidad de este documento se realiza con base en NVIDIA DGX OS (kernel 6.x, aarch64). Los controladores de chips MediaTek son del kernel Linux mainline, con alta estabilidad; los controladores de chips Realtek son mantenidos por la comunidad (morrownr), y su estabilidad real puede variar según la versión. DGX Spark ya incluye Wi-Fi 7, y la conexión de tarjetas de red ALFA se utiliza principalmente para pruebas de penetración o necesidades de chips especiales. La calidad del adaptador USB-C afectará directamente la experiencia de uso, se recomienda elegir adaptadores con marca y etiqueta USB 3.2 Gen 2×2.
