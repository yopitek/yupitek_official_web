---
title: "¿Son compatibles las tarjetas inalámbricas ALFA con el NVIDIA DGX Spark (GB10)?"
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
description: "9 adaptadores ALFA en el NVIDIA DGX Spark (GB10): probados en ASUS GX10 con kernel 6.17, controladores integrados sin DKMS; EACS/ACH/ACS inyectan mejor."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Artículo actualizado con las pruebas de noviembre de 2026 en el GX10: en el ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), los 9 adaptadores ALFA actuales usan controladores integrados en el kernel y funcionan al conectarlos, sin necesidad de DKMS. Datos completos en la [tabla de pruebas ARM64 de los 9 adaptadores ALFA](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Probado solo en el GX10; los demás equipos GB10 no se han probado uno por uno.

## 1. Resumen del Problema

Pregunta del cliente: «¿El adaptador inalámbrico USB de la serie ALFA puede ser utilizado en el supercomputador personal AI NVIDIA DGX Spark (GB10 Grace Blackwell)?»

Conclusión breve: El DGX Spark ejecuta NVIDIA DGX OS (basado en Ubuntu, kernel 6.x). Probamos en el ASUS GX10, que usa la misma plataforma GB10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), los 9 adaptadores USB ALFA actuales: todos usan controladores integrados en el kernel y funcionan al conectarlos, sin compilar nada ni usar DKMS. El DGX Spark usa el mismo GB10 y la misma familia de kernels de NVIDIA, por lo que se espera el mismo comportamiento, pero solo se probó en el GX10; el DGX Spark no se ha probado unidad por unidad. Diferencias funcionales: los modelos MediaTek MT7921 (AWUS036AXM / AXML) fallan la inyección de paquetes con el kernel stock 6.17, aunque monitor, AP y WPA3 funcionan; en los otros 7 modelos, monitor e inyección funcionaron en las pruebas. La versión mínima del kernel en la que cada controlador entró en la rama principal varía (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17); solo los kernels antiguos inferiores a esa versión necesitan los controladores DKMS de la comunidad. Nota: Todos los puertos USB del DGX Spark son de tipo USB Type-C, mientras que los adaptadores ALFA son de tipo USB Type-A, por lo que se requiere un adaptador o cable USB-C a USB-A.

Alcance de la evaluación: Se evalúan 9 adaptadores USB de la serie ALFA en uso (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

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

- Kernel 6.x (moderno): el kernel 6.17 (versión probada en el GX10) ya integra los controladores de los 9 adaptadores de este artículo, incluidos mt76 (MT7612U / MT7610U, 4.19+), mt7921u (MT7921AUN, 5.18+), rtw88 (RTL8821CU 6.2+; RTL8812AU / RTL8811AU 6.13+) y rtw89 (RTL8832BU, 6.17+). Esto contrasta marcadamente con el kernel 4.9 de Jetson Nano.
- Arquitectura ARM64 (aarch64): con los controladores integrados en el kernel no hace falta compilar nada en ARM64; solo en sistemas antiguos con kernel inferior a la versión mínima del adaptador los modelos Realtek necesitan compilar los controladores DKMS de la comunidad (como la serie de morrownr; hay que confirmar que el Makefile tenga CONFIG_PLATFORM_ARM64 = y).

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

Hasta septiembre de 2026, la línea de productos de tarjetas de red inalámbricas USB de ALFA Network en servicio es la siguiente (universo evaluado: 9 modelos):

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

### 4.2 Recomendaciones de Escenarios de Uso

| Escenario de Uso | Modelo Recomendado | Descripción |
|---|---|---|
| Conexión inalámbrica general (más simple) | Cualquiera de los 9 (p. ej. AWUS036ACM / ACHM) | Todos usan controladores integrados en el kernel y funcionan al conectarlos |
| Pruebas de penetración inalámbrica / escaneo / inyección | AWUS036EACS / ACH / ACS | Inyección probada al 96–100 %, captura de WPA handshake de extremo a extremo; no elija AXM / AXML (la inyección falla) |
| Wi-Fi 6 + punto de acceso (AP) | AWUS036AX / AXER | AP 2x2 de 80MHz probado y funcional |
| Banda de 6GHz | AWUS036AXML | Probado: crea un AP WPA3 en 6GHz; AXM usa el mismo chip pero 6GHz no se ha probado |
| Ya tiene AWUS036ACH y desea seguir utilizándolo | AWUS036ACH | A partir del kernel 6.13 incluye rtw88_8812au integrado: funciona al conectarlo, con inyección probada al 100 % en ambas bandas |
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
| Versión del kernel | El kernel 6.17 (probado: 6.17.0-1014-nvidia) ya integra los controladores de los 9 adaptadores, sin herramientas de compilación; la versión mínima varía según el adaptador (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17) y solo por debajo de ella hace falta instalar los controladores DKMS de la comunidad |
| Herramientas de gestión inalámbrica | iw, wpa_supplicant, network-manager (preinstalado en DGX OS) |

## 6. Determinación de Compatibilidad

### Matriz de Compatibilidad entre Modelos en Servicio de ALFA y NVIDIA DGX Spark (GB10)

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

Criterios de Determinación: pruebas en equipo real del 16 al 18 de noviembre de 2026 en el ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), usando redes Wi-Fi y teléfonos propios. El DGX Spark usa el mismo GB10 y la misma familia de kernels de NVIDIA, por lo que se espera el mismo comportamiento, pero solo se probó en el GX10; el DGX Spark no se ha probado unidad por unidad. Datos completos en la [tabla de pruebas ARM64 de los 9 adaptadores ALFA](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

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

**Paso 3: Confirme que la versión del kernel sea 6.17 o superior**

A partir del kernel 6.17 están integrados los controladores de los 9 adaptadores y no hace falta instalar herramientas de compilación. La versión mínima varía según el adaptador (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17); solo por debajo de ella los modelos Realtek necesitan los controladores DKMS de la comunidad (véase el último párrafo de 7.3).

### 7.2 Ruta A: Modelos con chip MediaTek (AWUS036ACM / ACHM / AXML / AXM) — Listo para usar

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
# Esperado: una interfaz que empieza por wlx (nombrada según la MAC; controlador de kernel cargado automáticamente)
```

**Paso 4: Escanear redes WiFi** (en el ejemplo se usa wlan0; sustitúyalo por el nombre de interfaz que muestre `ip link show`)

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**Paso 5: Conectar a una red WiFi (usando NetworkManager)**

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

### 7.3 Ruta B: Modelos Realtek Wi-Fi 5 (AWUS036ACH / ACS / EACS) — sin instalación desde kernel 6.13 (EACS desde 6.2)

**Paso 1: Conectar el adaptador y verificar que el controlador se cargó automáticamente**

```bash
uname -r          # ACH / ACS requieren 6.13 o superior; EACS, 6.2 o superior
lsusb
lsmod | grep rtw88
ip link show
```

Módulo que se carga automáticamente en cada modelo: ACH → `rtw88_8812au`, ACS → `rtw88_8821au`, EACS → `rtw88_8821cu` (el EACS incluye además Bluetooth, que funcionó en las pruebas).

**Paso 2: Método de conexión igual que en el Paso 5 de 7.2 (usando nmcli)**

**Paso 3: (Opcional) Modo monitor e inyección**

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

**Pasos necesarios solo con kernels antiguos (ACH / ACS por debajo de 6.13, EACS por debajo de 6.2)**: instale `build-essential git bc dkms` y compile el controlador de la comunidad; por ejemplo, para el RTL8812AU use morrownr/8812au-20210820 (confirme que el Makefile tenga `CONFIG_PLATFORM_ARM64 = y`). Si la versión es suficiente, use directamente el controlador integrado.

### 7.4 Ruta C: Modelos Wi-Fi 6 (AWUS036AX / AXER, RTL8832BU) — sin instalación desde kernel 6.17

```bash
lsusb                      # debería aparecer 0bda:b832
lsmod | grep rtw89_8852bu
ip link show
```

Pruebas en el GX10: el controlador integrado `rtw89_8852bu` se carga automáticamente, la recepción en monitor es buena, la inyección funciona (2.4GHz: AX 96 %, AXER 73 %) y el AP admite 80MHz. rtw89_8852bu entró en la rama principal recién en el kernel 6.17; los sistemas con kernel 6.16 o inferior necesitan el controlador DKMS de la comunidad (morrownr/rtl8852bu-20250826).

## 8. Errores Comunes y Soluciones

| Síntoma | Posible Causa | Solución |
|---|---|---|
| No se ve la tarjeta de red ALFA en lsusb | Adaptador USB-C defectuoso / Conexión inestable | Cambiar el adaptador USB-C a USB-A; verificar que el adaptador es compatible con la transferencia de datos (no solo carga); intentar con un puerto USB-C diferente |
| Después de insertar el chip MediaTek, no hay interfaz wlan | El módulo del kernel no se carga automáticamente / Firmware faltante | Cargar manualmente: `sudo modprobe mt76x2u`; verificar `dmesg | grep mt76`; instalar firmware: `sudo apt install linux-firmware` |
| El adaptador Realtek no muestra interfaz wlan al conectarlo | Kernel inferior a la versión mínima del adaptador (EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), sin el controlador correspondiente integrado | Compruebe la versión con `uname -r`; actualice el kernel o, en kernels antiguos, instale los controladores DKMS de la comunidad |
| Tras instalar un controlador DKMS en un kernel antiguo, modprobe informa de Operation not permitted | Secure Boot / firma de módulos | Firme el módulo o deshabilite Secure Boot (con los controladores integrados esto no ocurre) |
| Tras alternar varias veces entre monitor / AP no se detecta ninguna señal | Bloqueo de recepción (RX stall) | Desconecte y vuelva a conectar el adaptador para que el USB se enumere de nuevo |
| EACS / AXML sin interfaz wlx tras reconectar | Se atasca el probe del dispositivo compuesto Bluetooth + Wi-Fi | Conéctelo en otro puerto USB |
| Conexión WiFi inestable / velocidad lenta | El adaptador USB-C solo admite USB 2.0 | Cambiar a un adaptador que admite USB 3.2 Gen 2×2; verificar que el adaptador esté marcado como «Data» y no como «Charge Only» |
| El Wi-Fi interno y el ALFA externo chocan | Colisión de interfaces inalámbricas | Desactivar el Wi-Fi interno: `sudo nmcli radio wifi off` o desactivar en BIOS/UEFI; o configurar el orden de prioridad de las rutas |
| No se puede usar 6GHz (Wi-Fi 6E) | Restricciones del dominio regulatorio | Establecer el dominio regulatorio: `sudo iw reg set US` (Estados Unidos abre 6GHz); el AXML funcionó en 6GHz en las pruebas; el AXM no se ha probado |
| Falla al iniciar el modo AP | Conflictos entre NetworkManager y hostapd | Referirse a la guía de Yopitek ALFA Soft AP; desactivar NetworkManager para gestionar la interfaz y configurar manualmente hostapd |
| La tarjeta de red desaparece después de despertar | Suspensión automática de USB | Desactivar la suspensión automática de USB: `echo 'options usbcore autosuspend=-1' | sudo tee /etc/modprobe.d/usb.conf` |

## 9. Restricciones Conocidas

- **Requisito de adaptador USB Type-C**: Además de AXML, todos los tarjetas de red ALFA requieren un adaptador USB-C a USB-A, la calidad del adaptador puede afectar el rendimiento y la estabilidad.
- **Fallo de inyección en los modelos MT7921**: AWUS036AXM / AXML fallan la inyección de paquetes con el kernel stock 6.17, por lo que no se puede hacer deauth ni capturar el handshake; monitor, AP y WPA3 funcionan. La causa principal es una regresión de mac80211 chanctx a partir del kernel 6.16; el controlador parcheado por la comunidad todavía tiene limitaciones de velocidad.
- **Alcance de las pruebas**: solo se probó en el ASUS GX10 (kernel 6.17.0-1014-nvidia); el DGX Spark no se ha probado unidad por unidad; se espera el mismo comportamiento.
- **hcxdumptool no funciona**: todos los adaptadores salvo el EACS en 2.4 GHz muestran `failed to arm`; use airodump-ng + aireplay-ng en su lugar.
- **Posible conflicto con Wi-Fi externo**: DGX Spark incluye Wi-Fi 7 integrado, y al usar simultáneamente Wi-Fi interno y externo puede ocurrir conflictos de enrutamiento o recursos.
- **Configuración manual del modo AP**: DGX OS se preconfigura como entorno de desarrollo, el modo de punto de acceso (AP) requiere la instalación y configuración manual de hostapd / dnsmasq.
- **Restricciones regulatorias de 6GHz**: La disponibilidad del rango de frecuencia 6GHz de Wi-Fi 6E depende de la configuración regulatoria de la región, se debe confirmar la situación de apertura de 6GHz en Taiwán según la última regulación.
- **Kernels antiguos**: solo en sistemas con kernel inferior a la versión mínima del adaptador (EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17) los modelos Realtek necesitan los controladores DKMS de la comunidad (morrownr), que deben recompilarse tras cada actualización del kernel.
- **Diferencias en las pruebas de penetración**: en las pruebas en el GX10, la mayor tasa de éxito de inyección fue la de los modelos Realtek rtw88 (EACS y ACH, 100 % en ambas bandas); los modelos MediaTek mt76 (ACM / ACHM) funcionan; los MT7921 (AXM / AXML) fallan.
- **Función Bluetooth**: el Bluetooth del AWUS036AXML y del AWUS036EACS funcionó en las pruebas en el GX10; el Bluetooth del AWUS036AXM no se verificó por separado (DGX Spark incluye BT 5.4 integrado).
- **RTL8832BU (AWUS036AX / AXER)**: el mantenedor de controladores morrownr recomendó públicamente evitar los controladores out-of-tree de la serie rtl8852/32au (fuente en la sección 10). En las pruebas en el GX10 se usó el controlador integrado en el kernel `rtw89_8852bu`, con el que monitor, inyección, AP y WPA3 funcionan; esta conclusión solo se aplica al controlador integrado del kernel 6.17 o superior.
- **RTL8812AU (AWUS036ACH)**: el controlador in-kernel `rtw88_8812au`, conforme al estándar mac80211, se integró en el kernel 6.13 y alcanzó madurez a partir de la 6.14 (anuncio de morrownr). En las pruebas en el GX10 con kernel 6.17 funcionó al conectarlo, con inyección al 100 % en ambas bandas. Antes de responder, el servicio de atención al cliente puede pedir al cliente que informe el resultado de `uname -r` para confirmar si es 6.13 o superior.

Condiciones de refutación: si tras una actualización de DGX OS cambia la versión del kernel o el controlador del controlador USB y el comportamiento es distinto, o si en un DGX Spark real se obtienen resultados diferentes a los del GX10, se debe revisar nuevamente la matriz de compatibilidad de la sección 6; si en el futuro el kernel corrige el problema de inyección de mt7921u, la calificación de AWUS036AXM / AXML puede pasar de "solo conexión / AP" a una superior.

## 10. Referencias URL

| Fuente | Descripción | URL | Estado de verificación | Fecha de verificación |
|---|---|---|---|---|
| Página oficial de NVIDIA DGX Spark | Especificaciones y plataforma de DGX Spark | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| Documentos de NVIDIA DGX | Arquitectura del sistema operativo DGX y versión del kernel | https://docs.nvidia.com/dgx/dgx-spark | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Controladores Linux para RTL8812AU (soporte ARM64) | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| morrownr/8821cu GitHub | Controladores Linux para RTL8821CU (para kernels antiguos) | https://github.com/morrownr/8821cu-20210916 | ✅ Verificado | 2026-09-03 |
| morrownr/rtl8852bu GitHub | Controladores Linux para RTL8832BU | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Verificado | 2026-09-03 |
| Documentos de controladores mt76 del kernel Linux | Documentación de los controladores MediaTek mt76 / mt7921 mainline (versión de kernel de inicio de soporte para cada chip) | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ Verificado | 2026-09-03 |
| Guía de Linux para Soft AP WiFi Hotspot ALFA (Yopitek) | Guía de configuración del modo AP en Linux para ALFA | /es/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verificado | 2026-09-03 |
| Catálogo de productos de Network ALFA (Yopitek) | Especificaciones de productos actuales de ALFA | /es/products/alfa/ | ✅ Verificado | 2026-09-03 |
| Tabla de pruebas ARM64 de los 9 adaptadores ALFA (Yopitek) | Pruebas en equipo real: ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Probado | 2026-11-18 |
| Issue #314 de morrownr/USB-WiFi | Declaración oficial del mantenedor de controladores: se recomienda evitar los chips rtl8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Verificado | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | Anuncios más recientes sobre el estado del controlador RTL8812AU (incorporado en la línea principal del kernel 6.13, maduro en calidad para el kernel 6.14) | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |

Artículos relacionados: [¿Soporta la tarjeta inalámbrica ALFA el MSI EdgeXpert?](/es/blog/alfa-msi-edgexpert-compatibility/) | [¿Soporta la tarjeta inalámbrica ALFA el ASUS Ascent GX10?](/es/blog/alfa-asus-ascent-gx10-compatibility/) | [¿Soporta la tarjeta inalámbrica ALFA el ALTOS BrainSphere GB10 F1?](/es/blog/alfa-altos-brainsphere-gb10-compatibility/) | [¿Soporta la tarjeta inalámbrica ALFA el GIGABYTE AI TOP ATOM?](/es/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [¿Soporta la tarjeta inalámbrica ALFA el NVIDIA Jetson Nano?](/es/blog/alfa-nvidia-jetson-nano-compatibility/)

Aviso legal: La determinación de compatibilidad de este artículo se basa en las pruebas en equipo real realizadas en noviembre de 2026 en el ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia). El DGX Spark y el GX10 usan el mismo GB10 y la misma familia de kernels de NVIDIA, por lo que se espera el mismo comportamiento, pero no se ha probado unidad por unidad. El kernel 6.17 probado en el GX10 ya integra los controladores de los 9 adaptadores ALFA (la versión mínima varía según el adaptador); solo con un kernel inferior a la versión mínima del adaptador hacen falta los controladores DKMS de la comunidad (morrownr). DGX Spark ya incluye Wi-Fi 7, y la conexión de tarjetas de red ALFA se utiliza principalmente para pruebas de penetración o necesidades de chips especiales. La calidad del adaptador USB-C afectará directamente la experiencia de uso; se recomienda elegir adaptadores con marca y etiqueta USB 3.2 Gen 2×2. La escucha y la inyección deben limitarse a redes propias o para las que se tenga autorización.
