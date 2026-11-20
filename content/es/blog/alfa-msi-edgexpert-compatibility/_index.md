---
title: "¿Son compatibles las tarjetas inalámbricas ALFA con el MSI EdgeXpert (GB10)?"
date: 2026-09-03
draft: false
slug: "alfa-msi-edgexpert-compatibility"
tags:
  - "ALFA"
  - "MSI"
  - "EdgeXpert"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "Guía de Hardware"
description: "9 adaptadores ALFA en el MSI EdgeXpert (GB10): probados en ASUS GX10 con kernel 6.17, usan controladores integrados sin DKMS; AXM/AXML fallan la inyección."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Artículo actualizado con las pruebas de noviembre de 2026 en el GX10: en el ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), los 9 adaptadores ALFA actuales usan controladores integrados en el kernel y funcionan al conectarlos, sin necesidad de DKMS. Datos completos en la [tabla de pruebas ARM64 de los 9 adaptadores ALFA](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Probado solo en el GX10; los demás equipos GB10 no se han probado uno por uno.

## 1. Resumen del Problema

Pregunta del cliente: «¿El adaptador inalámbrico USB de la serie ALFA puede ser utilizado en el supercomputador MSI EdgeXpert (NVIDIA GB10 Grace Blackwell) con capacidad de IA?»

Conclusión breve: El MSI EdgeXpert y el NVIDIA DGX Spark usan el mismo chip GB10 y la misma familia de kernels de NVIDIA. Probamos en el ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia) los 9 adaptadores USB ALFA actuales (AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML): todos usan controladores integrados en el kernel y funcionan al conectarlos, sin compilar nada ni usar DKMS. Se espera el mismo comportamiento, pero solo se probó en el GX10; el MSI EdgeXpert no se ha probado unidad por unidad. Diferencias funcionales: los modelos MediaTek MT7921 (AWUS036AXM / AXML) fallan la inyección de paquetes (packet injection) con el kernel stock 6.17, aunque monitor, AP y WPA3 funcionan; en los otros 7 modelos, monitor e inyección funcionaron en las pruebas. La versión mínima del kernel en la que cada controlador entró en la rama principal varía (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17); solo los kernels antiguos inferiores a esa versión necesitan los controladores DKMS de la comunidad. Nota: Los 4 puertos USB del EdgeXpert son USB Type-C (20Gbps), y los adaptadores ALFA (excepto AXML) necesitan un adaptador USB-C a USB-A.

Alcance de la evaluación: Se evalúan los 9 adaptadores USB ALFA en servicio (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Análisis de la Arquitectura de Especificaciones de Hardware Objetivo

### 2.1 Especificaciones de Hardware de MSI EdgeXpert

| Ítem | Especificación |
|---|---|
| Nombre del producto | MSI EdgeXpert (Modelos: EdgeXpert-MS-C931 / 59STW, etc.) |
| Chip de núcleo | NVIDIA GB10 Grace Blackwell Superchip (Plataforma DGX Spark) |
| CPU | 20-core Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | NVIDIA Blackwell, 6144 núcleos CUDA, quinta generación Tensor Core, cuarta generación RT Core |
| Rendimiento de IA | Hasta 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| Memoria del sistema | 128GB LPDDR5x Memoria unificada (256-bit, 273 GB/s) |
| Almacenamiento | 1TB o 4TB NVMe M.2 SSD (autosecundado, PCIe Gen5) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (hasta 20Gbps) |
| Salida de visualización | 1× HDMI 2.1a (4× DP1.4a a través de USB-C Alt Mode) |
| Red cableada | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (QSFP 200GbE, interconexión de sistemas) |
| Red inalámbrica | Wi-Fi 7 + Bluetooth 5.4 |
| Sistema operativo | NVIDIA DGX OS (basado en Ubuntu Linux, kernel 6.x) |
| Arquitectura | aarch64 (ARM64) |
| Tamaño | 151 × 151 × 52 mm (aproximadamente 5.95" × 5.95" × 2.05") |
| Peso | Aproximadamente 1.2 kg (2.65 lbs) |
| Alimentación | Fuente de alimentación USB-C de 240W |
| Versión | Versión de consumo / Versión industrial (EdgeXpert-MS-C931, opciones de temperatura amplia / industrial) |

### 2.2 Entorno de Software: NVIDIA DGX OS

MSI EdgeXpert viene preinstalado con NVIDIA DGX OS, idéntico a DGX Spark / ASUS GX10:

| Ítem | Descripción |
|---|---|
| Base | Ubuntu Linux (personalizado por NVIDIA) |
| Kernel | Linux 6.x |
| Arquitectura | aarch64 (ARM64) |
| Software preinstalado | Pila de software de IA de NVIDIA (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Gestión de paquetes | apt |

### 2.3 Diferencias con DGX Spark

MSI EdgeXpert es una versión OEM de la plataforma DGX Spark, con hardware y software completamente idénticos:

| Ítem | MSI EdgeXpert | NVIDIA DGX Spark |
|---|---|---|
| Diseño de la institución | Chasis personalizado por MSI, opciones de versión industrial | Chasis de referencia de NVIDIA |
| Opciones de almacenamiento | 1TB / 4TB | Hasta 4TB |
| Mercado objetivo | IA en la frontera / IA industrial / desarrollo de escritorio | Desarrollo de IA de escritorio |
| Accesorios | Accesorios originales de MSI | Accesorios originales de NVIDIA |

Influencia en la compatibilidad con ALFA: Sin impacto previsto (probado solo en el GX10; los demás equipos GB10 no se han probado uno por uno). Los controladores USB, la versión del kernel y el framework de controladores son completamente idénticos a los de DGX Spark.

### 2.4 Necesidad de Adaptador USB Type-C

Las 4 puertos USB del EdgeXpert son Type-C, mientras que la serie completa de tarjetas de red ALFA (excepto AXML, que es USB-C) son USB Type-A, por lo que se requiere un adaptador. Se recomienda elegir un adaptador que soporte USB 3.2 Gen 2×2 (20Gbps).

## 3. Análisis de las Especificaciones y Chipsets de las Tarjetas de Red ALFA

Al 9 de septiembre de 2026, la línea de productos de tarjetas de red USB inalámbricas de ALFA Network en servicio es la siguiente (evaluación de la madre: 9 modelos):

| Modelo | Nivel Wi-Fi | Chipset | Interfaz | Controlador Linux integrado (versión mínima del kernel) |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E (6GHz probado y funcional) | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ Integrado (mt7921u, 5.18+) |
| AWUS036AXM | Wi-Fi 6E (según el fabricante; 6GHz no probado) | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ Integrado (mt7921u, 5.18+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ Integrado (rtw89_8852bu, 6.17+) |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ Integrado (rtw89_8852bu, 6.17+) |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ Integrado (rtw88_8812au, 6.13+) |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | ✅ Integrado (mt76x0u, 4.19+) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ Integrado (mt76x2u, 4.19+) |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | ✅ Integrado (rtw88_8821au, 6.13+) |
| AWUS036EACS | Wi-Fi 5 (AC600) + Bluetooth | Realtek RTL8821CU | USB 2.0 | ✅ Integrado (rtw88_8821cu, 6.2+) |

Nota: el kernel 6.17 probado en el GX10 ya integra los controladores de los 9 adaptadores; la versión mínima del kernel varía según el adaptador (véase el paréntesis de la tabla). Solo en sistemas antiguos con un kernel inferior a la versión mínima del adaptador hace falta instalar los controladores DKMS mantenidos por la comunidad.

## 4. Modelos Aplicables y Conjuntos de Chip

### 4.1 Clasificación de Recomendaciones

| Nivel de Recomendación | Modelo (Conjunto de Chip) | Descripción |
|---|---|---|
| ⭐ Primera opción para pentesting | AWUS036EACS (RTL8821CU) / AWUS036ACH (RTL8812AU) / AWUS036ACS (RTL8811AU) | Controlador integrado, sin instalación; inyección probada: EACS y ACH 100 % en ambas bandas, ACS 100 % en 2.4GHz y 96 % en 5GHz; captura de WPA handshake de extremo a extremo |
| ✅ Recomendado | AWUS036ACM (MT7612U) | Controlador integrado, sin instalación; monitor, inyección (2.4GHz 63–83 %, 5GHz 76 %), AP y WPA3 funcionan |
| ✅ Recomendado | AWUS036ACHM (MT7610U) | Controlador integrado, sin instalación; inyección en 2.4GHz 96–100 %, en 5GHz solo funciona la de broadcast; el AP WPA3 requiere sae_pwe=0 |
| ✅ Recomendado (Wi-Fi 6) | AWUS036AX / AXER (RTL8832BU) | Controlador integrado, sin instalación; buena recepción en monitor, inyección funcional (2.4GHz: AX 96 %, AXER 73 %), AP con 80MHz |
| ⚠️ Solo para conexión / AP | AWUS036AXML / AXM (MT7921AUN) | Controlador integrado, sin instalación; monitor, AP y WPA3 funcionan, pero la inyección falla con el kernel stock 6.17, no apto para pentesting; AXML se conecta directamente por USB-C |

### 4.2 Sugerencias de Escenarios de Uso

| Escenario de Uso | Modelo Recomendado | Descripción |
|---|---|---|
| Conexión inalámbrica en puertas de enlace AI de borde | Cualquiera de los 9 (p. ej. AWUS036ACM / ACHM) | Todos usan controladores integrados en el kernel y funcionan al conectarlos |
| Pruebas de penetración inalámbrica en entornos industriales | AWUS036EACS / ACH / ACS | Inyección probada al 96–100 %, captura de WPA handshake de extremo a extremo; no elija AXM / AXML (la inyección falla) |
| Wi-Fi 6 + punto de acceso (AP) | AWUS036AX / AXER | AP 2x2 de 80MHz probado y funcional |
| Banda de 6GHz | AWUS036AXML | Probado: crea un AP WPA3 en 6GHz; AXM usa el mismo chip pero 6GHz no se ha probado |
| No se requiere Wi-Fi externo | — | EdgeXpert ya tiene Wi-Fi 7 integrado, generalmente no se requiere conexión externa |

## 5. Requisitos de Entorno

### 5.1 Requisitos de Hardware

| Ítem | Requisitos |
|---|---|
| Adaptador USB | Adaptador USB-C a USB-A o cable de transmisión (excepto AXML), se recomienda que soporte USB 3.2 Gen 2×2 |
| Alimentación | Fuente de alimentación USB-C de 240W de fábrica MSI EdgeXpert |

### 5.2 Requisitos de Software

| Ítem | Requisitos |
|---|---|
| Versión de DGX OS | Cualquier versión en servicio (kernel 6.x) |
| Versión del kernel | El kernel 6.17 (probado: 6.17.0-1014-nvidia) ya integra los controladores de los 9 adaptadores, sin herramientas de compilación; la versión mínima varía según el adaptador (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17) y solo por debajo de ella hace falta instalar los controladores DKMS de la comunidad |
| Herramientas de gestión de red inalámbrica | iw, network-manager (preinstalado en DGX OS) |

## 6. Determinación de Compatibilidad

### Matriz de Compatibilidad entre Modelos en Servicio de ALFA y MSI EdgeXpert (GB10)

| Modelo | Chipset | Controlador (integrado en el kernel) | Detección USB | Conexión STA | Modo AP | Monitor | Inyección de paquetes | Dificultad de Instalación | Evaluación General |
|---|---|---|---|---|---|---|---|---|---|
| AWUS036EACS | RTL8821CU | rtw88_8821cu | ✅ | ✅ | ✅ | ✅ | ✅ 100 % en ambas bandas | Sin instalación | ⭐ Mejor |
| AWUS036ACH | RTL8812AU | rtw88_8812au | ✅ | ✅ | ✅ | ✅ | ✅ 100 % en ambas bandas | Sin instalación | ⭐ Mejor |
| AWUS036ACS | RTL8811AU | rtw88_8821au | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 100 % / 5G 96 % | Sin instalación | ⭐ Mejor |
| AWUS036ACM | MT7612U | mt76x2u | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 63–83 % / 5G 76 % | Sin instalación | ✅ Bueno |
| AWUS036ACHM | MT7610U | mt76x0u | ✅ | ✅ | ✅ | ✅ | ⚠️ 2.4G 96–100 % / 5G solo broadcast | Sin instalación | ✅ Bueno |
| AWUS036AX | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ Buena recepción | ✅ 2.4G 96 % / 5G funcional | Sin instalación | ✅ Bueno |
| AWUS036AXER | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ Buena recepción | ✅ 2.4G 73 % / 5G funcional | Sin instalación | ✅ Bueno |
| AWUS036AXML | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ Recepción débil | ❌ Falla | Sin instalación | ⚠️ Solo conexión / AP |
| AWUS036AXM | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ Recepción débil | ❌ Falla | Sin instalación | ⚠️ Solo conexión / AP |

Criterio de Determinación: pruebas en equipo real del 16 al 18 de noviembre de 2026 en el ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), usando redes Wi-Fi y teléfonos propios. El MSI EdgeXpert usa el mismo GB10 y la misma familia de kernels de NVIDIA, por lo que se espera el mismo comportamiento, pero solo se probó en el GX10; el MSI EdgeXpert no se ha probado unidad por unidad. Datos completos en la [tabla de pruebas ARM64 de los 9 adaptadores ALFA](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 7. Detallados Pasos a Paso

Los pasos de instalación de MSI EdgeXpert deberían ser idénticos a los de NVIDIA DGX Spark (los pasos se probaron en el GX10). A continuación, se presenta una versión resumida; para los pasos completos, consulte el Capítulo 7 de [ALFA Tarjeta de Red Inalámbrica y Compatibilidad con NVIDIA DGX Spark](/es/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modelos con chip MediaTek (AWUS036ACM / ACHM / AXM / AXML)

**Paso 1: Insertar la tarjeta de red**

Utilice un adaptador USB-C a USB-A (AXML se puede insertar directamente) para conectar la tarjeta de red ALFA a la toma USB-C de EdgeXpert.

**Paso 2: Confirmar la detección de USB**

```bash
lsusb
# Salida esperada (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Paso 3: Confirmar la interfaz de red**

```bash
ip link show
# Debería aparecer una interfaz que empieza por wlx (controlador in-kernel cargado automáticamente)
```

**Paso 4: Conectar a WiFi**

```bash
nmcli dev wifi connect "SSID" password "contraseña"
```

### 7.2 Modelos con chip Realtek (AWUS036ACH / ACS / EACS / AX / AXER)

El kernel 6.17 (versión probada en el GX10) ya integra los controladores de todos los modelos Realtek; los pasos son los mismos que para los modelos MediaTek y no hace falta compilar nada (versiones mínimas: EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17):

```bash
# 1. Verifique la versión del kernel (desde 6.17 están integrados los controladores de todos los modelos Realtek; el GX10 probado usa 6.17.0-1014-nvidia)
uname -r

# 2. Tras conectar el adaptador, verifique que el controlador se cargó automáticamente
lsusb
lsmod | grep -E "rtw88|rtw89"
ip link show

# 3. Conéctese a WiFi
nmcli dev wifi connect "SSID" password "contraseña"
```

Módulo que se carga automáticamente en cada modelo: ACH → `rtw88_8812au`, ACS → `rtw88_8821au`, EACS → `rtw88_8821cu`, AX / AXER → `rtw89_8852bu`. Solo si `uname -r` es inferior a la versión mínima del adaptador (sistemas antiguos) hace falta instalar los controladores DKMS mantenidos por la comunidad (por ejemplo, morrownr/8812au-20210820 para el RTL8812AU).

### 7.3 Modo de Escucha (Pruebas de Penetración)

⚠️ Realice pruebas de escucha e inyección solo en redes propias o para las que tenga autorización.

```bash
sudo apt install -y aircrack-ng
IF=wlx00c0cafe0000   # sustitúyalo por el nombre de interfaz que muestre ip link
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
sudo aireplay-ng --test $IF
```

- No ejecute `airmon-ng check kill`: detiene NetworkManager y deja el equipo sin conexión externa.
- Con el kernel stock 6.17, `aireplay-ng --test` falla en AWUS036AXM / AXML (Found 0 APs): no se puede hacer deauth ni capturar el handshake.
- hcxdumptool 8.x muestra `failed to arm` en los 9 adaptadores salvo el EACS en 2.4 GHz (el controlador no admite active monitor); use airodump-ng + aireplay-ng en su lugar.

## 8. Errores Comunes y Soluciones

| Síntoma | Posibles Causas | Solución |
|---|---|---|
| No se ve la tarjeta de red ALFA en `lsusb` | Adaptador USB-C defectuoso / Solo soporte de carga | Cambiar a un conector USB 3.2 Gen 2×2 que soporte transferencia de datos; probar con un puerto USB-C diferente |
| Chip MediaTek sin interfaz wlan | Módulo no se carga automáticamente / Firmware faltante | Ejecutar `sudo modprobe mt76x2u`; `sudo apt install linux-firmware`; verificar `dmesg | grep mt76` |
| El adaptador Realtek no muestra interfaz wlan al conectarlo | Kernel inferior a la versión mínima del adaptador (EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), sin el controlador correspondiente integrado | Compruebe la versión con `uname -r`; actualice el kernel o, en kernels antiguos, instale los controladores DKMS de la comunidad |
| Tras alternar varias veces entre monitor / AP no se detecta ninguna señal | Bloqueo de recepción (RX stall) | Desconecte y vuelva a conectar el adaptador para que el USB se enumere de nuevo |
| EACS / AXML sin interfaz wlx tras reconectar | Se atasca el probe del dispositivo compuesto Bluetooth + Wi-Fi | Conéctelo en otro puerto USB |
| Velocidad de WiFi lenta | Adaptador solo soporta USB 2.0 | Cambiar a un conector USB 3.2 Gen 2×2 |
| Conflictos entre Wi-Fi 7 integrado y externo | Conflictos de red | Ejecutar `sudo nmcli radio wifi off` para desactivar el WiFi integrado antes de usar el externo |
| Inestabilidad en entornos industriales de alta temperatura | Disipación de calor / Diferencias en la versión industrial | Confirmar el uso de EdgeXpert industrial (MS-C931); asegurar que la temperatura del entorno esté dentro de los parámetros especificados |

## 9. Restricciones Conocidas

- Necesidad de adaptador USB Type-C: Además de AXML, todas las tarjetas de red ALFA requieren un adaptador USB-C a USB-A.
- Fallo de inyección en los modelos MT7921: AWUS036AXM / AXML fallan la inyección de paquetes con el kernel stock 6.17, por lo que no se puede hacer deauth ni capturar el handshake; monitor, AP y WPA3 funcionan. La causa principal es una regresión de mac80211 chanctx a partir del kernel 6.16; el controlador parcheado por la comunidad todavía tiene limitaciones de velocidad.
- Alcance de las pruebas: solo se probó en el ASUS GX10 (kernel 6.17.0-1014-nvidia); el MSI EdgeXpert no se ha probado unidad por unidad; se espera el mismo comportamiento.
- hcxdumptool no funciona: todos los adaptadores salvo el EACS en 2.4 GHz muestran `failed to arm`; use airodump-ng + aireplay-ng en su lugar.
- Posible conflicto con Wi-Fi 7 integrado: EdgeXpert incluye Wi-Fi 7 + BT 5.4.
- Configuración manual del modo AP: DGX OS se configura por defecto como entorno de desarrollo.
- Restricciones regulatorias de 6GHz: La disponibilidad de Wi-Fi 6E depende de la región regulatoria.
- Kernels antiguos: solo en sistemas con kernel inferior a la versión mínima del adaptador (EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17) los modelos Realtek necesitan los controladores DKMS de la comunidad, que deben recompilarse tras cada actualización del kernel.
- Diferencias en la versión industrial no afectan la compatibilidad: La versión industrial de MSI (MS-C931) tiene las mismas especificaciones hardware que la versión de consumo, y la compatibilidad USB WiFi es la misma.

Condiciones de refutación: Si la página de especificaciones oficial de MSI cambia (ajuste de especificaciones de puertos USB, versión del kernel inferior a 6.x), o si se encuentra que mt76x2u / mt7921u no se carga automáticamente en DGX OS durante las pruebas en el campo, el cuadro de compatibilidad del capítulo 6 debe revisarse nuevamente; si tras una actualización del kernel de NVIDIA cambia el comportamiento de los controladores integrados, será necesario volver a probarlos en equipo real.

## 10. Referencias URL

| Fuente | Descripción | URL | Estado de verificación | Fecha de verificación |
|---|---|---|---|---|
| MSI EdgeXpert Tienda Oficial (US) | Especificaciones de la versión de consumo de EdgeXpert | https://us-store.msi.com/MSI-EdgeXpert-Blackwell-AI-Supercomputer | ✅ Verificado | 2026-09-03 |
| MSI EdgeXpert Tienda (TW) | Especificaciones de la versión de consumo de EdgeXpert (23STW) | https://tw-store.msi.com/products/edgexpert-23stw-bgb104tg4 | ✅ Verificado | 2026-09-03 |
| MSI Computadoras Industriales Anuncios Oficiales | Información de lanzamiento de productos EdgeXpert | https://ipc.msi.com/en/news/146241 | ✅ Verificado | 2026-09-03 |
| NVIDIA DGX Spark Página Oficial | Información sobre la plataforma GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Controladores Linux para RTL8812AU | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| ALFA Network Catálogo de Productos (Yopitek) | Especificaciones de productos actuales de ALFA | /es/products/alfa/ | ✅ Verificado | 2026-09-03 |
| Tabla de pruebas ARM64 de los 9 adaptadores ALFA (Yopitek) | Pruebas en equipo real: ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Probado | 2026-11-18 |

Artículos relacionados: [¿Soporta la tarjeta inalámbrica ALFA NVIDIA DGX Spark?](/es/blog/alfa-nvidia-dgx-spark-compatibility/) | [¿Soporta la tarjeta inalámbrica ALFA ASUS Ascent GX10?](/es/blog/alfa-asus-ascent-gx10-compatibility/) | [¿Soporta la tarjeta inalámbrica ALFA ALTOS BrainSphere GB10 F1?](/es/blog/alfa-altos-brainsphere-gb10-compatibility/) | [¿Soporta la tarjeta inalámbrica ALFA GIGABYTE AI TOP ATOM?](/es/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [¿Soporta la tarjeta inalámbrica ALFA NVIDIA Jetson Nano?](/es/blog/alfa-nvidia-jetson-nano-compatibility/)

Declaración de exención de responsabilidad: La determinación de compatibilidad de este artículo se basa en las pruebas en equipo real realizadas en noviembre de 2026 en el ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia). El MSI EdgeXpert y el GX10 usan el mismo GB10 y la misma familia de kernels de NVIDIA, por lo que se espera el mismo comportamiento, pero no se ha probado unidad por unidad. El kernel 6.17 probado en el GX10 ya integra los controladores de los 9 adaptadores ALFA (la versión mínima varía según el adaptador); solo con un kernel inferior a la versión mínima del adaptador hacen falta los controladores DKMS de la comunidad. El EdgeXpert incluye Wi-Fi 7, por lo que un ALFA externo se usa principalmente para pruebas de penetración o necesidades de chipset específicas. La escucha y la inyección deben limitarse a redes propias o para las que se tenga autorización.
