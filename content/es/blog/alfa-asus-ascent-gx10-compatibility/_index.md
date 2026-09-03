---
title: "¿Soporte del Adaptador Inalámbrico ALFA para el ASUS Ascent GX10 (GB10)?"
date: 2026-09-03
draft: false
slug: "alfa-asus-ascent-gx10-compatibility"
tags:
  - "ALFA"
  - "ASUS"
  - "Ascent-GX10"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "Guía de Hardware"
description: "ASUS GX10 & NVIDIA DGX Spark: 同平台，兼容ALFA网卡，MediaTek芯片即插即用，Realtek需编译驱动，GX10全USB-C端口。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumen del Problema

Pregunta del cliente: «¿El adaptador inalámbrico USB de la serie ALFA puede ser utilizado en el supercomputador ASUS Ascent GX10 (NVIDIA GB10 Grace Blackwell) AI?»

Conclusión breve: El ASUS Ascent GX10 y el NVIDIA DGX Spark comparten la misma plataforma de hardware GB10 y el entorno de software DGX OS, lo que garantiza la total compatibilidad con el adaptador ALFA (evaluación basada en los 9 adaptadores USB ALFA en servicio). Los modelos con chip MediaTek (AWUS036ACM / ACHM / AXML / AXM, 4 modelos) utilizan el controlador in-kernel y son compatibles de fábrica; los modelos con chip Realtek (AWUS036ACH / ACS / EACS / AX / AXER, 5 modelos) requieren la compilación del controlador out-of-tree en ARM64. Nota: Todos los puertos USB del GX10 son de tipo USB Type-C (3 puertos de datos + 1 puerto de entrada PD), y los adaptadores ALFA (excepto AXML) necesitan un adaptador USB-C a USB-A.

## 2. Análisis de la Arquitectura de Especificaciones de Hardware Objetivo

### 2.1 Especificaciones de Hardware de ASUS Ascent GX10

| Ítem | Especificación |
|---|---|
| Nombre del producto | ASUS Ascent GX10 |
| Chip de núcleo | NVIDIA GB10 Grace Blackwell Superchip (Plataforma DGX Spark) |
| CPU | 20 núcleos Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Arquitectura Blackwell de NVIDIA, 6144 núcleos CUDA, quinta generación Tensor Core, cuarta generación RT Core |
| Rendimiento de IA | Hasta 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| Memoria del sistema | 128GB LPDDR5x Memoria unificada (256-bit, 273 GB/s) |
| Almacenamiento | Hasta 4TB NVMe M.2 SSD (cifrado) |
| USB | 3× USB 3.2 Gen 2×2 Type-C (20Gbps, DP Alt Mode / DisplayPort 2.1) + 1× USB 3.2 Gen 2×2 Type-C (PD entrada, 180W EPR PD3.1) |
| Salida de visualización | 1× HDMI 2.1 (compatible con DP Alt Mode de USB-C para salida de múltiples pantallas) |
| Red cableada | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (2× 200G QSFP112) |
| Red inalámbrica | Wi-Fi 7 (MediaTek AW-EM637, 2×2 MIMO) + Bluetooth 5.4 |
| Sistema operativo | NVIDIA DGX OS (basado en Ubuntu Linux, kernel 6.x) |
| Arquitectura | aarch64 (ARM64) |
| Tamaño | 150 × 150 × 51 mm (5.91 × 5.91 × 2.01 pulgadas) |
| Peso | 1.48 kg |
| Refrigeración | Sistema de refrigeración patentado de ASUS (ventilador silencioso + tubos de calor) |
| Otros | Ranura de bloqueo Kensington |

> ⚠️ Nota de corrección de especificaciones: El tamaño original del documento se escribió como "150 × 150 × 50 mm" y no se especificó el peso. Después de la verificación, las especificaciones oficiales de ASUS techspec son **150 × 150 × 51 mm / 1.48 kg**, se ha corregido. La versión de HDMI se ajusta a la oficial como 2.1 (el documento original escribió 2.1b, se ha corregido). Ver la sección 10 de la fuente de referencia.

### 2.2 Entorno de Software: NVIDIA DGX OS

| Ítem | Contenido |
|---|---|
| OS básico | Ubuntu Linux (personalizado por NVIDIA) |
| Kernel | Linux 6.x |
| Arquitectura | aarch64 (ARM64) |
| Software preinstalado | Conjunto de software de IA de NVIDIA (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Gestión de paquetes | apt |

### 2.3 Diferencias con DGX Spark

| Diferencia | ASUS GX10 | NVIDIA DGX Spark |
|---|---|---|
| Diseño de refrigeración | Sistema de refrigeración patentado de ASUS | Refrigeración de referencia de NVIDIA |
| Diseño de la estructura | Chasis personalizado por ASUS | Chasis de referencia de NVIDIA |
| Módulo inalámbrico | MediaTek AW-EM637 (Wi-Fi 7) | Módulo inalámbrico de nivel similar de Wi-Fi 7 |
| Accesorios | Accesorios de fábrica de ASUS | Accesorios de fábrica de NVIDIA |
| Garantía | Garantía de ASUS | Garantía de NVIDIA |
| Influencia en la compatibilidad con ALFA | Sin impacto. Los controladores de USB, la versión del kernel y el framework de controladores son completamente iguales a los de DGX Spark.

### 2.4 Necesidades de Conexión de Adaptador USB Type-C

Los 4 puertos USB de GX10 son Type-C:

- 3 puertos de datos (compatible con DP Alt Mode, puede conectarse a pantallas)
- 1 puerto de entrada PD (para alimentación)

La serie completa de tarjetas de red de ALFA (excepto AXML que es USB-C) son USB Type-A, se requiere un adaptador.

## 3. Análisis de las Especificaciones y Chipsets de las Tarjetas de Red ALFA

Hasta septiembre de 2026, la línea de productos de tarjetas de red USB inalámbricas de ALFA Network en servicio es la siguiente:

| Modelo | Nivel Wi-Fi | Chipset | Interfaz | Estado del Controlador Linux |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel (mt7921u) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel (mt7921u) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 / out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Igual que el anterior |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree (8812au) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel (mt76x2u)⭐ Recomendado |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree (8812au cubierto) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree (8821cu) |

## 4. Modelos Aplicables y Conjuntos de Chip

### 4.1 Clasificación de Recomendación

| Nivel de Recomendación | Modelo (Conjunto de Chip) | Descripción |
|---|---|---|
| ⭐ Recomendación Fuerte | AWUS036ACM (MT7612U) | Controlador in-kernel, plug and play, AC1200 dual band, soporte para AP / Monitor / Injection |
| ✅ Recomendado | AWUS036ACHM (MT7610U) | Controlador in-kernel, bajo consumo de energía, AC433 dual band |
| ✅ Recomendado (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | Controlador in-kernel, Wi-Fi 6E, AXML con conexión USB-C directa |
| ⚠️ Disponible pero requiere compilación | AWUS036ACH (RTL8812AU) | Requiere la compilación de morrownr/8812au (ARM64) para que todas las funciones sean completas |
| ⚠️ Disponible pero requiere compilación | AWUS036ACS / EACS | Requiere la compilación de controladores out-of-tree |
| ⚠️ Disponible pero con atención | AWUS036AX / AXER (RTL8832BU) | El kernel 6.x de rtw89 puede ya soportar; no es necesario compilar |

### 4.2 Sugerencias de Escenarios de Uso

| Escenario de Uso | Modelo Recomendado | Descripción |
|---|---|---|
| Conexión inalámbrica general (más simple) | AWUS036ACM / ACHM | Controlador in-kernel, sin necesidad de compilación |
| Pruebas de penetración inalámbrica / escaneo / inyección | AWUS036ACH o AWUS036ACM | Ambos soportan Monitor + Injection |
| Wi-Fi 6E / 6GHz | AWUS036AXML / AXM | Controlador in-kernel MT7921AUN |
| No se necesita Wi-Fi externo | — | GX10 tiene Wi-Fi 7 integrado, no es necesario conectar Wi-Fi externo para navegar |

## 5. Requisitos de Entorno

### 5.1 Requisitos de Hardware

| Ítem | Requisitos |
|---|---|
| Adaptador USB | Adaptador USB-C a USB-A o cable de transmisión (excepto AXML), se recomienda que soporte USB 3.2 Gen 2×2 |
| Alimentación | Fuente de alimentación USB-C de fábrica ASUS GX10 (180W EPR PD3.1) |

### 5.2 Requisitos de Software

| Ítem | Requisitos |
|---|---|
| Versión de DGX OS | Cualquier versión en servicio (kernel 6.x) |
| Herramientas de compilación (requeridas para el chip Realtek) | build-essential, git, bc, dkms |
| Herramientas de gestión inalámbrica | iw, network-manager (preinstalado en DGX OS) |

## 6. Determinación de Compatibilidad

### Matriz de Compatibilidad entre Modelos en Servicio ALFA × ASUS Ascent GX10 (GB10)

| Modelo | Chipset | Modo de Control | Detección USB | Conexión STA | Modo AP | Monitor | Dificultad de Instalación | Evaluación General |
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

Criterio de Determinación: ASUS GX10 y DGX Spark comparten la misma plataforma de hardware GB10 y el DGX OS (kernel 6.x, aarch64), por lo que la determinación de compatibilidad es completamente idéntica a la de DGX Spark.

## 7. Detallados pasos a paso

Los pasos de instalación del ASUS GX10 son idénticos a los de NVIDIA DGX Spark. A continuación, se presenta una versión resumida; para los pasos completos, consulte el Capítulo 7 de [ALFA: Tarjeta inalámbrica compatible con NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modelos de chip MediaTek (listo para usar)

- Utilice un adaptador USB-C a USB-A (AXML se puede insertar directamente) para conectar la tarjeta de red ALFA al puerto USB-C del GX10.
- Verifique la detección: `lsusb`
- Verifique la interfaz: `ip link show` (debería aparecer wlan0 automáticamente)
- Conéctese a WiFi: `nmcli dev wifi connect "SSID" password "contraseña"`

### 7.2 Modelos de chip Realtek (requiere compilación)

Tomando como ejemplo AWUS036ACH (RTL8812AU):

```bash
# 1. Instale las herramientas de compilación
sudo apt update && sudo apt install -y build-essential git bc dkms

# 2. Descargue y compile el controlador
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
# Verifique que CONFIG_PLATFORM_ARM64 = y en Makefile
make
sudo make install
sudo modprobe 8812au

# 3. Verifique la interfaz después de insertar la tarjeta de red
ip link show

# 4. Conéctese a WiFi
nmcli dev wifi connect "SSID" password "contraseña"
```

### 7.3 Modo de escucha (pruebas de penetración)

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

## 8. Errores Comunes y Soluciones

| Síntoma | Posible Causa | Solución |
|---|---|---|
| `lsusb` no muestra la tarjeta de red ALFA | Adaptador USB-C defectuoso / Solo soporte de carga | Cambiar a un adaptador USB 3.2 Gen 2×2 compatible con transferencia de datos; intentar con un puerto USB-C diferente |
| Chip MediaTek sin interfaz wlan | Módulo no se carga automáticamente / Firmware faltante | Ejecutar `sudo modprobe mt76x2u`; `sudo apt install linux-firmware`; verificar `dmesg | grep mt76` |
| Falla en la compilación del controlador Realtek | Configuración de compilación cruzada incorrecta | Confirmar la compilación nativa en GX10; el Makefile no debe configurar CROSS_COMPILE |
| Velocidad de WiFi lenta | Adaptador solo compatible con USB 2.0 | Cambiar a un adaptador USB 3.2 Gen 2×2 |
| Conflictos entre Wi-Fi interno y externo | Conflictos de red | Ejecutar `sudo nmcli radio wifi off` para desactivar el WiFi interno antes de usar el externo |
| No se puede usar el rango de 6GHz | Restricciones del dominio regulatorio | Ejecutar `sudo iw reg set US`; confirmar las últimas regulaciones |

## 9. Restricciones Conocidas

- Necesidad de adaptador USB Type-C: Además de AXML, todos los tarjetas de red ALFA requieren un adaptador USB-C a USB-A.
- Necesidad de traducción manual de chip Realtek: RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU no han sido incluidos en el mainline.
- Posible conflicto con Wi-Fi 7 integrado: GX10 incluye Wi-Fi 7 (MediaTek AW-EM637).
- Configuración manual del modo AP: DGX OS se configura por defecto como entorno de desarrollo.
- Restricciones regulatorias de 6GHz: La disponibilidad de Wi-Fi 6E depende de la región regulatoria.
- Actualizaciones de controladores dependen de componentes superiores: Los controladores out-of-tree de Realtek son mantenidos por la comunidad, y requieren ser recompilados después de las actualizaciones del kernel.
- Diferencias en hardware de ASUS no afectan la compatibilidad: Las diferencias en el diseño de disipación y mecánico no afectan la compatibilidad del controlador USB WiFi.

Condiciones de refutación: Las determinaciones anteriores se basan en DGX OS (basado en Ubuntu, kernel 6.x). Si ASUS lanzara futuras versiones de firmware no compatibles con DGX OS (como versiones propias de Android o sistemas personalizados), se requeriría una revisión de las determinaciones.

## 10. Referencias URL

| Fuente | Descripción | URL | Estado de verificación | Fecha de verificación |
|---|---|---|---|---|
| ASUS Ascent GX10 Especificaciones Técnicas Oficiales | Especificaciones de hardware GX10 (150×150×51mm / 1.48kg / configuración USB / HDMI 2.1) | https://www.asus.com/ph/networking-iot-servers/desktop-ai-supercomputer/ultra-small-ai-supercomputers/asus-ascent-gx10/techspec/ | ✅ Verificado | 2026-09-03 |
| ASUS Ascent GX10 Página de Producto Oficial (Reino Unido) | Página de producto GX10 (150 × 150 × 51mm) | https://uk.store.asus.com/asus-ascent-gx105004-33389.html | ✅ Verificado | 2026-09-03 |
| NVIDIA DGX Spark Página Oficial | Información sobre la plataforma GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Controladores Linux para RTL8812AU | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Guía Linux (Yupitek) | Guía para el modo AP de ALFA en Linux | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verificado | 2026-09-03 |
| ALFA Network Catálogo de Productos (Yupitek) | Especificaciones de productos actuales de ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |

Artículos relacionados: [¿Soporta la tarjeta inalámbrica ALFA a NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[¿Soporta la tarjeta inalámbrica ALFA a ALTOS BrainSphere GB10 F1?](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[¿Soporta la tarjeta inalámbrica ALFA a GIGABYTE AI TOP ATOM?](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[¿Soporta la tarjeta inalámbrica ALFA a MSI EdgeXpert?](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)

Aviso legal: La determinación de la compatibilidad de este documento se realiza con base en el NVIDIA DGX OS preinstalado en ASUS Ascent GX10 (kernel 6.x, aarch64). El GX10 y el DGX Spark comparten la misma plataforma de hardware, por lo que la compatibilidad es completamente idéntica. Los controladores de chip MediaTek son de Linux mainline, lo que garantiza una alta estabilidad; los controladores de chip Realtek son mantenidos por la comunidad. El GX10 incluye Wi-Fi 7, y el uso de ALFA se limita principalmente a pruebas de penetración o necesidades de chip específicas.
