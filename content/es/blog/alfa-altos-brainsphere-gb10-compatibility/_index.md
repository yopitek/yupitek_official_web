---
title: "¿Soporte del Tarjeta de Red Inalámbrica ALFA para el ALTOS BrainSphere GB10 F1?"
date: 2026-09-03
draft: false
slug: "alfa-altos-brainsphere-gb10-compatibility"
tags:
  - "ALFA"
  - "Altos"
  - "BrainSphere-GB10"
  - "NVIDIA-GB10"
  - "AWUS036ACM"
  - "ARM64"
  - "DGX-OS"
categories:
  - "Guía de Hardware"
description: "ALTOS GB10 F1 & NVIDIA DGX Spark 同平台，兼容ALFA网卡，MediaTek芯片即插即用，Realtek需编译驱动，注意端口和转接器。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Resumen del Problema

Pregunta del cliente: «¿El adaptador inalámbrico USB de la serie ALFA puede ser utilizado en la estación de trabajo AI ALTOS BrainSphere GB10 F1 (NVIDIA GB10 Grace Blackwell)?»

Conclusión breve: La estación de trabajo ALTOS BrainSphere GB10 F1 y el NVIDIA DGX Spark comparten la misma plataforma de hardware GB10 y el entorno de software DGX OS, lo que garantiza la total compatibilidad con los adaptadores ALFA (evaluación basada en los 9 adaptadores USB ALFA en servicio). Los modelos con chip MediaTek (AWUS036ACM / ACHM / AXML / AXM, 4 modelos) utilizan controladores in-kernel y son compatibles de fábrica; los modelos con chip Realtek (AWUS036ACH / ACS / EACS / AX / AXER, 5 modelos) requieren la compilación de controladores out-of-tree en ARM64. Nota: El BrainSphere GB10 F1 cuenta con 3 puertos USB-C de datos y 1 puerto USB-C de entrada PD, y los adaptadores ALFA (excepto AXML) deben utilizarse con un adaptador USB-C a USB-A.

## 2. Análisis de la Arquitectura de Especificaciones de Hardware Objetivo

### 2.1 Especificaciones de Hardware de ALTOS BrainSphere GB10 F1

| Ítem | Especificación |
|---|---|
| Nombre del producto | ALTOS BrainSphere GB10 F1 (Acer / Altos Computing) |
| Chip de núcleo | NVIDIA GB10 Grace Blackwell Superchip (Plataforma DGX Spark) |
| CPU | 20 núcleos Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Arquitectura Blackwell de NVIDIA, 6144 núcleos CUDA, quinta generación Tensor Core, cuarta generación RT Core |
| Rendimiento de IA | Hasta 1 PetaFLOP (FP4, Sparse) / 1000 TOPS, soporta modelos de hasta 2000 millones de parámetros |
| Memoria del sistema | 128GB LPDDR5x Memoria unificada (256-bit, 273 GB/s) |
| Almacenamiento | 4TB NVMe M.2 SSD (autosecundado) |
| USB | 3× USB 3.2 Gen 2×2 Type-C (20Gbps, DP Alt Mode) + 1× USB 3.2 Gen 2×2 Type-C (PD entrada, 180W EPR PD3.1) |
| Salida de visualización | 1× HDMI 2.1a |
| Red cableada | 1× 10GbE RJ45 + NVIDIA ConnectX-7 NIC (200G × 2 QSFP) |
| Red inalámbrica | Wi-Fi 7 + Bluetooth 5.4 with LE |
| Sistema operativo | NVIDIA DGX OS (basado en Ubuntu Linux, kernel 6.x) |
| Arquitectura | aarch64 (ARM64) |
| Tamaño | 150 × 150 × 50 mm (1.13L) |
| Peso | < 1.5 kg |
| Consumo máximo | 170W |
| Software incluido | Altos aiGeni (plataforma de desarrollo de IA en un solo clic, soporta TensorFlow / PyTorch / Jupyter / Ollama) |

> Verificación de especificaciones: Las dimensiones / peso / consumo / configuración USB mencionadas anteriormente son consistentes con el Product Sheet PDF oficial de Altos (véase la sección 10 de fuentes de referencia).

### 2.2 Entorno de Software: NVIDIA DGX OS + Altos aiGeni

| Ítem | Contenido |
|---|---|
| OS básico | Ubuntu Linux (personalizado por NVIDIA, DGX OS) |
| Kernel | Linux 6.x |
| Arquitectura | aarch64 (ARM64) |
| Plataforma de IA | Altos aiGeni (despliegue de entorno en un solo clic, copia de seguridad automática, monitoreo en tiempo real, herramientas inteligentes) |
| Marcos preinstalados | TensorFlow, PyTorch, Jupyter, Ollama |
| Gestión de paquetes | apt |

### 2.3 Diferencias con DGX Spark

| Diferencia | BrainSphere GB10 F1 | NVIDIA DGX Spark |
|---|---|---|
| Software incluido | Plataforma de desarrollo de IA Altos aiGeni | Conjunto de software de referencia de NVIDIA |
| Diseño de la estructura | Chasis personalizado por Altos / Acer | Chasis de referencia de NVIDIA |
| Mercado objetivo | Empresas de IA / Instituciones de investigación / Educación | Desarrollo de IA de escritorio |
| Consumo máximo | 170W | Aproximadamente 240W (con conversión de fuente de alimentación) |

Influencia en la compatibilidad con ALFA: Sin impacto. Altos aiGeni es un software de nivel de aplicación y no afecta a los marcos de controladores del kernel. Los controladores de USB, la versión del kernel y la arquitectura de los controladores son completamente iguales a los de DGX Spark.

### 2.4 Necesidad de Adaptadores USB Type-C

Los 4 puertos USB del BrainSphere GB10 F1 son Type-C (3 de datos + 1 de entrada PD), mientras que la serie completa de tarjetas de red ALFA (excepto AXML que es USB-C) son Type-A, por lo que se requiere un adaptador.

## 3. Análisis de las Especificaciones y Chipsets de las Tarjetas de Red ALFA

Hasta septiembre de 2026, la línea de productos de tarjetas de red inalámbricas USB de ALFA Network en servicio es la siguiente:

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

### 4.1 Clasificación de Recomendaciones

| Nivel de Recomendación | Modelo (Conjunto de Chip) | Descripción |
|---|---|---|
| ⭐ Recomendación Fuerte | AWUS036ACM (MT7612U) | Controlador in-kernel, listo para usar, AC1200 dual banda, soporte AP / Monitor / Injection |
| ✅ Recomendado | AWUS036ACHM (MT7610U) | Controlador in-kernel, bajo consumo de energía, AC433 dual banda |
| ✅ Recomendado (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | Controlador in-kernel, Wi-Fi 6E, AXML con conexión USB-C directa |
| ⚠️ Disponible pero requiere compilación | AWUS036ACH (RTL8812AU) | Requiere compilación de morrownr/8812au (ARM64),完成后功能完整 |
| ⚠️ Disponible pero requiere compilación | AWUS036ACS / EACS | Requiere compilación de controlador out-of-tree correspondiente |
| ⚠️ Disponible pero con atención | AWUS036AX / AXER (RTL8832BU) | El rtw89 del kernel 6.x puede ya soportar; no requiere compilación |

### 4.2 Sugerencias de Escenarios de Uso

| Escenario de Uso | Modelo Recomendado | Descripción |
|---|---|---|
| Laboratorio de Internet sin cables de empresa AI | AWUS036ACM / ACHM | Controlador in-kernel, estable, sin mantenimiento, adecuado para entornos empresariales |
| Pruebas de penetración de red inalámbrica / investigación de seguridad | AWUS036ACH o AWUS036ACM | Ambos soportan Monitor + Injection |
| Wi-Fi 6E / Banda de 6GHz | AWUS036AXML / AXM | Controlador in-kernel MT7921AUN |
| No se requiere Wi-Fi externo | — | BrainSphere ya tiene Wi-Fi 7 integrado, generalmente no es necesario conectar Wi-Fi externo |

## 5. Requisitos de Entorno

### 5.1 Requisitos de Hardware

| Ítem | Requisitos |
|---|---|
| Adaptador USB | Adaptador USB-C a USB-A o cable de transmisión (excepto AXML), se recomienda que soporte USB 3.2 Gen 2×2 |
| Alimentación | Fuente de alimentación USB-C de fábrica ALTOS (180W EPR PD3.1) |

### 5.2 Requisitos de Software

| Ítem | Requisitos |
|---|---|
| Versión de DGX OS | Cualquier versión en servicio (kernel 6.x) |
| Herramientas de compilación (requeridas para el chip Realtek) | build-essential, git, bc, dkms |
| Herramientas de gestión de red inalámbrica | iw, network-manager (preinstalado en DGX OS) |
| Notas de aiGeni | Si se utiliza el entorno de contenedor de aiGeni, se debe asegurar que los dispositivos USB se hayan montado correctamente en el contenedor (generalmente se recomienda configurarlo en el nivel del host OS) |

## 6. Determinación de Compatibilidad

### Matriz de Compatibilidad ALFA Modelos en Servicio × ALTOS BrainSphere GB10 F1

| Modelo | Chipset | Modo de Control | Detección USB | Conexión STA | Modo AP | Monitor | Dificultad de Instalación | Evaluación General |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel（mt76x2u） | ✅ | ✅ | ✅ | ✅ | Sin instalación | ⭐ Mejor |
| AWUS036ACHM | MT7610U | in-kernel（mt76x0u） | ✅ | ✅ | ✅ | ⚠️ Limitado | Sin instalación | ✅ Bueno |
| AWUS036AXML | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ Limitado | Sin instalación | ✅ Bueno |
| AWUS036AXM | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ Limitado | Sin instalación | ✅ Bueno |
| AWUS036ACH | RTL8812AU | out-of-tree（8812au） | ✅ | ✅ | ✅ | ✅ | Moderado（compilación） | ⚠️ Disponible |
| AWUS036ACS | RTL8811AU | out-of-tree（8812au） | ✅ | ✅ | ⚠️ | ❌ | Moderado（compilación） | ⚠️ Disponible |
| AWUS036EACS | RTL8811CU | out-of-tree（8821cu） | ✅ | ⚠️ | ❌ | ❌ | Moderado（compilación） | ⚠️ Disponible |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Moderado-Alto | ⚠️ Disponible |
| AWUS036AXER | RTL8832BU | Igual que anterior | ✅ | ⚠️ | ⚠️ | ❌ | Moderado-Alto | ⚠️ Disponible |

Criterio de Determinación: ALTOS BrainSphere GB10 F1 y DGX Spark comparten la misma plataforma de hardware GB10 y el DGX OS (kernel 6.x, aarch64), por lo que la determinación de compatibilidad es completamente idéntica a la de DGX Spark. Altos aiGeni es un software de nivel de aplicación, que no afecta la compatibilidad de los controladores.

## 7. Detallados Pasos a Paso

Los pasos de instalación del ALTOS BrainSphere GB10 F1 son idénticos a los de NVIDIA DGX Spark. A continuación, se presenta una versión resumida; para los pasos completos, consulte el Capítulo 7 de [¿Soporta el adaptador inalámbrico ALFA el NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modelos de Chip MediaTek (Listo para usar)

- Utilice el adaptador USB-C a USB-A (AXML se puede insertar directamente) para conectar la tarjeta de red ALFA al puerto USB-C del BrainSphere.
- Verifique la detección: `lsusb`
- Verifique la interfaz: `ip link show` (debería aparecer wlan0 automáticamente)
- Conéctese a WiFi: `nmcli dev wifi connect "SSID" password "contraseña"`

### 7.2 Modelos de Chip Realtek (Requiere compilación)

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

### 7.3 Modo de Escucha (Pruebas de Infiltración)

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

### 7.4 Uso de WiFi en el Contenedor aiGeni (Avanzado)

Si necesita usar la tarjeta de red ALFA en el contenedor Docker de Altos aiGeni:

1. Complete la instalación del controlador y la conexión a WiFi en el host OS (DGX OS).
2. Al iniciar el contenedor, utilice `--network=host` o monte la interfaz de red correspondiente.
3. Recomendamos que el acceso a Internet se realice en el nivel del host OS, mientras que el contenedor utiliza `--network=bridge` para compartir la red.

## 8. Errores Comunes y Soluciones

| Síntoma | Posible Causa | Solución |
|---|---|---|
| No se ve la tarjeta de red ALFA en `lsusb` | Adaptador USB-C defectuoso / Solo soporte de carga | Cambiar a un adaptador USB 3.2 Gen 2×2 compatible con transferencia de datos; intentar con un puerto USB-C diferente |
| Chip MediaTek sin interfaz wlan | Módulo no se carga automáticamente / Firmware faltante | Ejecutar `sudo modprobe mt76x2u`; `sudo apt install linux-firmware`; verificar `dmesg | grep mt76` |
| Falla en la compilación del controlador Realtek | Configuración de compilación cruzada incorrecta | Confirmar la compilación nativa en BrainSphere; el Makefile no debe configurar CROSS_COMPILE |
| Velocidad de WiFi lenta | Adaptador solo soporta USB 2.0 | Cambiar a un adaptador USB 3.2 Gen 2×2 |
| Conflictos entre Wi-Fi 7 integrado y externo | Conflictos de red | Ejecutar `sudo nmcli radio wifi off` para desactivar el WiFi integrado antes de usar el externo |
| No se ve WiFi en el contenedor aiGeni | Problema con el modo de red del contenedor | Usar `--network=host`; o permitir que el contenedor comparta la red después de conectarse al host OS |
| No se puede usar la banda de 6GHz | Restricciones del dominio regulatorio | Ejecutar `sudo iw reg set US`; confirmar las últimas regulaciones |

## 9. Restricciones Conocidas

- Necesidad de adaptador USB Type-C: Además de AXML, todos los tarjetas de red ALFA requieren un adaptador USB-C a USB-A.
- Traducción manual de chips Realtek: RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU no han sido incluidos en el mainline.
- Posible conflicto con Wi-Fi 7 integrado: BrainSphere ya incluye Wi-Fi 7 + BT 5.4.
- Configuración manual del modo AP: DGX OS predeterminado es un entorno de desarrollo.
- Restricciones regulatorias de 6GHz: La disponibilidad de Wi-Fi 6E depende de la región regulatoria.
- Actualizaciones de controladores dependen de componentes superiores: Los controladores out-of-tree de Realtek son mantenidos por la comunidad, y deben ser recompilados después de las actualizaciones del kernel.
- Aislamiento de contenedores aiGeni: Si se utiliza WiFi en contenedores aiGeni, se debe prestar atención a los espacios de nombres de red y la carga de dispositivos; se recomienda gestionar WiFi a nivel del host OS.
- Diferencias en software Altos no afectan la compatibilidad: aiGeni es una plataforma de capa de aplicación, y no afecta la compatibilidad del controlador USB WiFi del kernel.

Condiciones de refutación: Las siguientes determinaciones se basan en DGX OS (basado en Ubuntu, kernel 6.x). Si Altos cambia en el futuro a un OS propio no basado en Ubuntu, o si hay cambios en la versión mayor del kernel de DGX OS, se debe revalidar la determinación in-kernel / out-of-tree.

## 10. Referencias URL

| Fuente | Descripción | URL | Estado de verificación | Fecha de verificación |
|---|---|---|---|---|
| Hoja de Producto Oficial de ALTOS BrainSphere GB10 F1 | Especificaciones de hardware (170W / 50mm / configuración USB) | https://www.altoscomputing.com/filepic/pdf/Altos_BrainSphere_GB10_F1_Product_Sheet_TW.pdf | ✅ Verificado | 2026-09-03 |
| Sitio web oficial de Altos Computing | Información del producto BrainSphere GB10 F1 | https://www.altoscomputing.com/en-Us | ✅ Verificado | 2026-09-03 |
| Página oficial de NVIDIA DGX Spark | Información sobre la plataforma GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Controladores Linux para RTL8812AU | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| Catálogo de productos de ALFA Network (Yupitek) | Especificaciones de productos actuales de ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |

Artículos relacionados: [¿Soporta la tarjeta inalámbrica ALFA la plataforma NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[¿Soporta la tarjeta inalámbrica ALFA la plataforma ASUS Ascent GX10?](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[¿Soporta la tarjeta inalámbrica ALFA la plataforma GIGABYTE AI TOP ATOM?](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[¿Soporta la tarjeta inalámbrica ALFA la plataforma MSI EdgeXpert?](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)

Declaración de exención de responsabilidad: La determinación de la compatibilidad de este documento se realiza con base en el NVIDIA DGX OS preinstalado en ALTOS BrainSphere GB10 F1 (kernel 6.x, aarch64). BrainSphere y DGX Spark comparten la misma plataforma de hardware, por lo que la compatibilidad es completamente consistente. Altos aiGeni es un software de nivel de aplicación, que no afecta la compatibilidad de los controladores. Los controladores de chip MediaTek son del mainline de Linux, lo que garantiza una alta estabilidad; los controladores de chip Realtek son mantenidos por la comunidad. BrainSphere incluye Wi-Fi 7, y el uso de ALFA externo se destina principalmente a pruebas de penetración o necesidades de chip específicas.
