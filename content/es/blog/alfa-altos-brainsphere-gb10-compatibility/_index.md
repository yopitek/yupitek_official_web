---
title: "¿Son compatibles las tarjetas inalámbricas ALFA con el ALTOS BrainSphere GB10 F1?"
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
description: "9 adaptadores ALFA en el ALTOS BrainSphere GB10 F1: probados en ASUS GX10 con kernel 6.17, usan controladores integrados sin DKMS; EACS/ACH/ACS inyectan mejor."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Artículo actualizado con las pruebas de noviembre de 2026 en el GX10: en el ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), los 9 adaptadores ALFA actuales usan controladores integrados en el kernel y funcionan al conectarlos, sin necesidad de DKMS. Datos completos en la [tabla de pruebas ARM64 de los 9 adaptadores ALFA](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Probado solo en el GX10; los demás equipos GB10 no se han probado uno por uno.

## 1. Resumen del Problema

Pregunta del cliente: «¿El adaptador inalámbrico USB de la serie ALFA puede ser utilizado en la estación de trabajo AI ALTOS BrainSphere GB10 F1 (NVIDIA GB10 Grace Blackwell)?»

Conclusión breve: El ALTOS BrainSphere GB10 F1 y el NVIDIA DGX Spark usan el mismo chip GB10 y la misma familia de kernels de NVIDIA. Probamos en el ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia) los 9 adaptadores USB ALFA actuales (AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML): todos usan controladores integrados en el kernel y funcionan al conectarlos, sin compilar nada ni usar DKMS. Se espera el mismo comportamiento, pero solo se probó en el GX10; el ALTOS BrainSphere GB10 F1 no se ha probado unidad por unidad. Diferencias funcionales: los modelos MediaTek MT7921 (AWUS036AXM / AXML) fallan la inyección de paquetes (packet injection) con el kernel stock 6.17, aunque monitor, AP y WPA3 funcionan; en los otros 7 modelos, monitor e inyección funcionaron en las pruebas. La versión mínima del kernel en la que cada controlador entró en la rama principal varía (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17); solo los kernels antiguos inferiores a esa versión necesitan los controladores DKMS de la comunidad. Nota: El BrainSphere GB10 F1 cuenta con 3 puertos USB-C de datos y 1 puerto USB-C de entrada PD, y los adaptadores ALFA (excepto AXML) deben utilizarse con un adaptador USB-C a USB-A.

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

Influencia en la compatibilidad con ALFA: Sin impacto previsto (probado solo en el GX10; los demás equipos GB10 no se han probado uno por uno). Altos aiGeni es un software de nivel de aplicación y no afecta a los marcos de controladores del kernel. Los controladores de USB, la versión del kernel y la arquitectura de los controladores son completamente iguales a los de DGX Spark.

### 2.4 Necesidad de Adaptadores USB Type-C

Los 4 puertos USB del BrainSphere GB10 F1 son Type-C (3 de datos + 1 de entrada PD), mientras que la serie completa de tarjetas de red ALFA (excepto AXML que es USB-C) son Type-A, por lo que se requiere un adaptador.

## 3. Análisis de las Especificaciones y Chipsets de las Tarjetas de Red ALFA

Hasta septiembre de 2026, la línea de productos de tarjetas de red inalámbricas USB de ALFA Network en servicio es la siguiente:

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
| Conexión inalámbrica en laboratorios de IA empresariales | Cualquiera de los 9 (p. ej. AWUS036ACM / ACHM) | Todos usan controladores integrados en el kernel y funcionan al conectarlos |
| Pruebas de penetración de red inalámbrica / investigación de seguridad | AWUS036EACS / ACH / ACS | Inyección probada al 96–100 %, captura de WPA handshake de extremo a extremo; no elija AXM / AXML (la inyección falla) |
| Wi-Fi 6 + punto de acceso (AP) | AWUS036AX / AXER | AP 2x2 de 80MHz probado y funcional |
| Banda de 6GHz | AWUS036AXML | Probado: crea un AP WPA3 en 6GHz; AXM usa el mismo chip pero 6GHz no se ha probado |
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
| Versión del kernel | El kernel 6.17 (probado: 6.17.0-1014-nvidia) ya integra los controladores de los 9 adaptadores, sin herramientas de compilación; la versión mínima varía según el adaptador (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17) y solo por debajo de ella hace falta instalar los controladores DKMS de la comunidad |
| Herramientas de gestión de red inalámbrica | iw, network-manager (preinstalado en DGX OS) |
| Notas de aiGeni | Si se utiliza el entorno de contenedor de aiGeni, se debe asegurar que los dispositivos USB se hayan montado correctamente en el contenedor (generalmente se recomienda configurarlo en el nivel del host OS) |

## 6. Determinación de Compatibilidad

### Matriz de Compatibilidad ALFA Modelos en Servicio × ALTOS BrainSphere GB10 F1

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

Criterio de Determinación: pruebas en equipo real del 16 al 18 de noviembre de 2026 en el ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), usando redes Wi-Fi y teléfonos propios. El ALTOS BrainSphere GB10 F1 usa el mismo GB10 y la misma familia de kernels de NVIDIA, por lo que se espera el mismo comportamiento, pero solo se probó en el GX10; el ALTOS BrainSphere GB10 F1 no se ha probado unidad por unidad. Datos completos en la [tabla de pruebas ARM64 de los 9 adaptadores ALFA](/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 7. Detallados Pasos a Paso

Los pasos de instalación del ALTOS BrainSphere GB10 F1 deberían ser idénticos a los de NVIDIA DGX Spark (los pasos se probaron en el GX10). A continuación, se presenta una versión resumida; para los pasos completos, consulte el Capítulo 7 de [¿Soporta el adaptador inalámbrico ALFA el NVIDIA DGX Spark?](/es/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modelos con chip MediaTek (AWUS036ACM / ACHM / AXM / AXML)

- Utilice el adaptador USB-C a USB-A (AXML se puede insertar directamente) para conectar la tarjeta de red ALFA al puerto USB-C del BrainSphere.
- Verifique la detección: `lsusb`
- Verifique la interfaz: `ip link show` (debería aparecer automáticamente una interfaz que empieza por wlx)
- Conéctese a WiFi: `nmcli dev wifi connect "SSID" password "contraseña"`

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

### 7.4 Uso de WiFi en el Contenedor aiGeni (Avanzado)

Si necesita usar la tarjeta de red ALFA en el contenedor Docker de Altos aiGeni:

1. En el host OS (DGX OS), verifique que el controlador se haya cargado automáticamente y complete la conexión WiFi.
2. Al iniciar el contenedor, utilice `--network=host` o monte la interfaz de red correspondiente.
3. Recomendamos que el acceso a Internet se realice en el nivel del host OS, mientras que el contenedor utiliza `--network=bridge` para compartir la red.

## 8. Errores Comunes y Soluciones

| Síntoma | Posible Causa | Solución |
|---|---|---|
| No se ve la tarjeta de red ALFA en `lsusb` | Adaptador USB-C defectuoso / Solo soporte de carga | Cambiar a un adaptador USB 3.2 Gen 2×2 compatible con transferencia de datos; intentar con un puerto USB-C diferente |
| Chip MediaTek sin interfaz wlan | Módulo no se carga automáticamente / Firmware faltante | Ejecutar `sudo modprobe mt76x2u`; `sudo apt install linux-firmware`; verificar `dmesg | grep mt76` |
| El adaptador Realtek no muestra interfaz wlan al conectarlo | Kernel inferior a la versión mínima del adaptador (EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), sin el controlador correspondiente integrado | Compruebe la versión con `uname -r`; actualice el kernel o, en kernels antiguos, instale los controladores DKMS de la comunidad |
| Tras alternar varias veces entre monitor / AP no se detecta ninguna señal | Bloqueo de recepción (RX stall) | Desconecte y vuelva a conectar el adaptador para que el USB se enumere de nuevo |
| EACS / AXML sin interfaz wlx tras reconectar | Se atasca el probe del dispositivo compuesto Bluetooth + Wi-Fi | Conéctelo en otro puerto USB |
| Velocidad de WiFi lenta | Adaptador solo soporta USB 2.0 | Cambiar a un adaptador USB 3.2 Gen 2×2 |
| Conflictos entre Wi-Fi 7 integrado y externo | Conflictos de red | Ejecutar `sudo nmcli radio wifi off` para desactivar el WiFi integrado antes de usar el externo |
| No se ve WiFi en el contenedor aiGeni | Problema con el modo de red del contenedor | Usar `--network=host`; o permitir que el contenedor comparta la red después de conectarse al host OS |
| No se puede usar la banda de 6GHz | Restricciones del dominio regulatorio | Ejecutar `sudo iw reg set US`; confirmar las últimas regulaciones |

## 9. Restricciones Conocidas

- Necesidad de adaptador USB Type-C: Además de AXML, todos los tarjetas de red ALFA requieren un adaptador USB-C a USB-A.
- Fallo de inyección en los modelos MT7921: AWUS036AXM / AXML fallan la inyección de paquetes con el kernel stock 6.17, por lo que no se puede hacer deauth ni capturar el handshake; monitor, AP y WPA3 funcionan. La causa principal es una regresión de mac80211 chanctx a partir del kernel 6.16; el controlador parcheado por la comunidad todavía tiene limitaciones de velocidad.
- Alcance de las pruebas: solo se probó en el ASUS GX10 (kernel 6.17.0-1014-nvidia); el ALTOS BrainSphere GB10 F1 no se ha probado unidad por unidad; se espera el mismo comportamiento.
- hcxdumptool no funciona: todos los adaptadores salvo el EACS en 2.4 GHz muestran `failed to arm`; use airodump-ng + aireplay-ng en su lugar.
- Posible conflicto con Wi-Fi 7 integrado: BrainSphere ya incluye Wi-Fi 7 + BT 5.4.
- Configuración manual del modo AP: DGX OS predeterminado es un entorno de desarrollo.
- Restricciones regulatorias de 6GHz: La disponibilidad de Wi-Fi 6E depende de la región regulatoria.
- Kernels antiguos: solo en sistemas con kernel inferior a la versión mínima del adaptador (EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17) los modelos Realtek necesitan los controladores DKMS de la comunidad, que deben recompilarse tras cada actualización del kernel.
- Aislamiento de contenedores aiGeni: Si se utiliza WiFi en contenedores aiGeni, se debe prestar atención a los espacios de nombres de red y la carga de dispositivos; se recomienda gestionar WiFi a nivel del host OS.
- Diferencias en software Altos no afectan la compatibilidad: aiGeni es una plataforma de capa de aplicación, y no afecta la compatibilidad del controlador USB WiFi del kernel.

Condiciones de refutación: Las siguientes determinaciones se basan en DGX OS (basado en Ubuntu, kernel 6.x). Si Altos cambia en el futuro a un OS propio no basado en Ubuntu, o si hay cambios en la versión mayor del kernel de DGX OS, la determinación sobre los controladores integrados debe volver a probarse en equipo real.

## 10. Referencias URL

| Fuente | Descripción | URL | Estado de verificación | Fecha de verificación |
|---|---|---|---|---|
| Hoja de Producto Oficial de ALTOS BrainSphere GB10 F1 | Especificaciones de hardware (170W / 50mm / configuración USB) | https://www.altoscomputing.com/filepic/pdf/Altos_BrainSphere_GB10_F1_Product_Sheet_TW.pdf | ✅ Verificado | 2026-09-03 |
| Sitio web oficial de Altos Computing | Información del producto BrainSphere GB10 F1 | https://www.altoscomputing.com/en-Us | ✅ Verificado | 2026-09-03 |
| Página oficial de NVIDIA DGX Spark | Información sobre la plataforma GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verificado | 2026-09-03 |
| morrownr/8812au GitHub | Controladores Linux para RTL8812AU | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| Catálogo de productos de ALFA Network (Yopitek) | Especificaciones de productos actuales de ALFA | /es/products/alfa/ | ✅ Verificado | 2026-09-03 |
| Tabla de pruebas ARM64 de los 9 adaptadores ALFA (Yopitek) | Pruebas en equipo real: ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/es/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Probado | 2026-11-18 |

Artículos relacionados: [¿Soporta la tarjeta inalámbrica ALFA la plataforma NVIDIA DGX Spark?](/es/blog/alfa-nvidia-dgx-spark-compatibility/) | [¿Soporta la tarjeta inalámbrica ALFA la plataforma ASUS Ascent GX10?](/es/blog/alfa-asus-ascent-gx10-compatibility/) | [¿Soporta la tarjeta inalámbrica ALFA la plataforma GIGABYTE AI TOP ATOM?](/es/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [¿Soporta la tarjeta inalámbrica ALFA la plataforma MSI EdgeXpert?](/es/blog/alfa-msi-edgexpert-compatibility/)

Declaración de exención de responsabilidad: La determinación de compatibilidad de este artículo se basa en las pruebas en equipo real realizadas en noviembre de 2026 en el ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia). El ALTOS BrainSphere GB10 F1 y el GX10 usan el mismo GB10 y la misma familia de kernels de NVIDIA, por lo que se espera el mismo comportamiento, pero no se ha probado unidad por unidad. Altos aiGeni es un software de nivel de aplicación que no afecta la compatibilidad de los controladores. El kernel 6.17 probado en el GX10 ya integra los controladores de los 9 adaptadores ALFA (la versión mínima varía según el adaptador); solo con un kernel inferior a la versión mínima del adaptador hacen falta los controladores DKMS de la comunidad. El BrainSphere incluye Wi-Fi 7, por lo que un ALFA externo se usa principalmente para pruebas de penetración o necesidades de chipset específicas. La escucha y la inyección deben limitarse a redes propias o para las que se tenga autorización.
