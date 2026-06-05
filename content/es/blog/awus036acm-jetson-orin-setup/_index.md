---
title: "¡Sin compilar drivers! Guía práctica plug-and-play del ALFA AWUS036ACM en Jetson Orin Edge AI"
description: "Para clientes de AVALUE AIB-NW01 (NVIDIA Jetson Orin NX/Nano), analizamos en profundidad qué adaptador USB WiFi de ALFA Network es el más adecuado para despliegues de Edge AI, demostrando empíricamente cómo el AWUS036ACM logra un verdadero plug-and-play."
date: 2026-05-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Jetson-Orin", "Edge-AI", "USB-WiFi", "AWUS036ACM", "AVALUE", "AIB-NW01"]
featureimage: "/images/blog/awus036acm-jetson-orin-setup.webp"
---

## Un correo de un cliente revela una cuestión clave

> «Tengo un AVALUE AIB-NW01 (Jetson Orin NX) que voy a desplegar en un entorno sin red cableada. ¿Cuál de vuestros adaptadores USB WiFi funciona directamente?»

Esta es una consulta que Yupitek ha recibido recientemente. La pregunta parece sencilla, pero si has pasado tiempo en la comunidad de desarrolladores de Jetson sabrás que — **los adaptadores USB WiFi en la plataforma NVIDIA Jetson son mucho más problemáticos de lo que imaginas.**

Hemos investigado a fondo: desde la arquitectura del núcleo de Jetson, casos reales en los foros de NVIDIA, reportes de fallos de compilación de drivers en GitHub, hasta datos de pruebas reales en plataformas ARM64. Aquí tienes esta guía de compra.

---

## Opciones de conectividad inalámbrica del AIB-NW01: conoce primero tu plataforma

El AVALUE AIB-NW01 es un **sistema embebido sin ventilador** diseñado específicamente para aplicaciones de Edge AI, disponible en cuatro configuraciones de NVIDIA Jetson Orin SoM. A continuación, sus especificaciones completas de hardware y entorno de software:

### Resumen de especificaciones de hardware

| Elemento | Especificación |
|------|------|
| **Opciones de SoM** | Jetson Orin NX 16GB / NX 8GB / Orin Nano 8GB / Orin Nano 4GB |
| **CPU** | ARM Cortex-A78AE v8.2 64-bit (NX 16GB: 8-core @ 2.0 GHz / NX 8GB: 6-core @ 2.0 GHz / Nano: 6-core @ 1.5 GHz) |
| **GPU** | Arquitectura NVIDIA Ampere (NX: 1024 CUDA Cores + 32 Tensor Cores / Nano 4GB: 512 CUDA Cores + 16 Tensor Cores) |
| **Potencia de cómputo AI** | 100 / 70 / 40 / 20 TOPS (según configuración de SoM) |
| **Memoria** | LPDDR5 (NX 16GB/8GB: 128-bit 102.4 GB/s / Nano 8GB: 128-bit 68 GB/s / Nano 4GB: 64-bit 34 GB/s) |
| **Almacenamiento** | 128GB M.2 2280 NVMe SSD (integrado) |
| **Red** | 2 × GbE RJ-45 (10/100/1000 Mbps) |
| **USB** | 4 × USB 3.1 Type-A, 1 × Micro USB OTG |
| **Pantalla** | 1 × HDMI Type-A |
| **Puertos serie** | 2 × DB9 (RS-232 / RS-485 conmutable por jumper) |
| **Ranuras de expansión** | 1 × M.2 M-Key 2242/2280 (NVMe SSD), 1 × M.2 E-Key 2230 (módulo WiFi/BT), 1 × M.2 B-Key 3042/3052 (módulo 5G/LTE, solo para uso a temperatura ambiente) |
| **SIM** | 1 × ranura Micro SIM |
| **Alimentación** | DC 10~24V (bornera de 2 pines) |
| **Dimensiones** | 125 × 196 × 66 mm (sin soporte de pared) |
| **Peso** | 1.4 kg |
| **Material del chasis** | Aluminio extrusionado + acero, diseño sin ventilador |
| **Temperatura de operación** | -15°C ~ 60°C (según IEC60068, con flujo de aire de 0.5 m/s) |
| **Temperatura de almacenamiento** | -40°C ~ 80°C |
| **Certificaciones** | CE, FCC Class A |

### Entorno de software

| Elemento | Especificación |
|------|------|
| **Sistema operativo** | Ubuntu 20.04.6 LTS (Focal Fossa) |
| **NVIDIA SDK** | JetPack 5.0 (incluye CUDA 11.4, cuDNN 8.4, TensorRT 8.4) |
| **Kernel de Linux** | 5.10.x-tegra (kernel Tegra personalizado por NVIDIA, **no es el kernel estándar de Ubuntu**) |
| **Arquitectura de CPU** | ARM64 (aarch64) |
| **Recursos AI SDK** | [github.com/Avalue-Technology](https://github.com/Avalue-Technology/repositories.directory) |

> **Aviso importante**: La plataforma Jetson utiliza un kernel personalizado mantenido por NVIDIA llamado `linux-tegra`, no el kernel estándar de Ubuntu. Esto tiene profundas implicaciones en la compatibilidad de drivers de terceros — consulta más abajo «Los tres grandes desafíos de los adaptadores USB WiFi en Jetson Orin».

Este equipo ofrece tres vías de conectividad inalámbrica:

### M.2 2230 E-Key (ranura para módulo WiFi)

**Ventajas**: Alta velocidad, integrado en la placa base, no ocupa puertos USB
**Desventajas**: Requiere desmontar el equipo, los conectores de antena están fijados dentro del chasis, difícil de reemplazar, la compatibilidad del módulo debe verificarse caso por caso

### USB 3.1 Type-A (4 puertos)

**Ventajas**: Hot-plug, sin necesidad de desmontar, las antenas pueden colocarse en la posición óptima de señal, se puede compartir entre dispositivos
**Desventajas**: Los adaptadores USB son más voluminosos, la velocidad máxima depende de la interfaz USB

### 5G M.2 B-Key (opcional)

**Ventajas**: Conectividad independiente, no depende de la infraestructura WiFi local
**Desventajas**: Coste elevado, requiere tarjeta SIM y plan de datos, configuración compleja

Para la mayoría de escenarios de despliegue de Edge AI — fase de POC, vigilancia exterior, líneas de producción — **el adaptador USB WiFi es la opción más flexible y de menor coste.**

Pero surge la pregunta: ¿puedo comprar cualquier adaptador USB WiFi, enchufarlo al Jetson y que funcione?

La respuesta es: **no necesariamente. Y la probabilidad de fracaso es mucho más alta de lo que imaginas.**

---

## Los tres grandes desafíos de los adaptadores USB WiFi en Jetson Orin

La mayoría de artículos sobre USB WiFi solo hablan de Linux x86, pero la plataforma Jetson es un mundo completamente distinto.

### Desafío uno: tu kernel no es el kernel de Ubuntu

Jetson ejecuta el **kernel Tegra Linux personalizado por NVIDIA**, no el kernel estándar de Ubuntu. Esto significa que:

- `apt install linux-headers-$(uname -r)` muy probablemente **no podrá obtener los kernel headers correspondientes**
- NVIDIA aplica parches al kernel que pueden romper la ABI requerida por drivers de terceros
- El entorno de compilación de módulos del kernel es completamente diferente al de un PC de escritorio x86

Un adaptador USB que «soporta Linux» **no garantiza que pueda compilarse con éxito en Jetson**.

### Desafío dos: la compilación de drivers de terceros en Jetson falla con frecuencia

Caso real en GitHub (abril de 2025): en JetPack 6.2 (kernel 5.15.148-tegra), tanto `make` como `dkms` del driver RTL8812EU fallaban. El análisis de la comunidad reveló que — **los parches del kernel de NVIDIA en JetPack rompen la ABI de cfg80211**, impidiendo que los drivers WiFi de terceros se compilen correctamente.

> Fuente: [GitHub issue #421 — RTL8812EU Driver Compilation Failed on Jetson Orin Nano](https://github.com/svpcom/wfb-ng/issues/421)

### Desafío tres: una actualización de JetPack puede dejar tu adaptador «inservible»

Caso del foro de NVIDIA (octubre de 2024): el RTL8188EUS funcionaba perfectamente en JetPack 5.1.x, pero tras actualizar a JetPack 6 **dejó de ser reconocido por completo**. La solución fue recompilar manualmente el driver desde GitHub — pero ¿y si la próxima versión de JetPack vuelve a cambiar la API del kernel?

> Fuente: [Jetson Orin Nano — JetPack 6 no soporta RTL8188EUS](https://nvidia-jetson.piveral.com/jetson-orin-nano/jetpack-6-doesnt-support-rtl8188eus/)

### La lección en resumen

> **En la plataforma Jetson, la única opción verdaderamente fiable es usar un adaptador USB WiFi cuyo driver esté integrado en el kernel de Linux (in-kernel).**

Porque NVIDIA está obligado a mantener la compatibilidad de los drivers integrados en el kernel — esta es la única garantía de que tu adaptador seguirá funcionando tras una actualización de JetPack.

---

## Panorama de compatibilidad de chipsets: una tabla para verlo claro

A continuación, un resumen de la compatibilidad de los chipsets de adaptadores USB WiFi de ALFA Network más comunes en Jetson Orin:

| Chipset | Modelo ALFA | Tipo de driver | Requisito mínimo de kernel | Conclusión para Jetson Orin |
|------|-----------|----------|-----------------|------------------|
| **MT7612U** | **AWUS036ACM** | **In-kernel (mt76x2u)** | **4.19+** | ✅ Compatibilidad perfecta, plug-and-play |
| RTL8812AU | AWUS036ACH | Out-of-tree (requiere compilación) | Compilación manual necesaria | ⚠️ Considerable pero con riesgo de compilación |
| RTL8811AU | AWUS036ACS | Out-of-tree (requiere compilación) | Compilación manual necesaria | ⚠️ Mismos problemas que RTL8812AU |
| RTL8812BU | AWUS036AX | Out-of-tree (requiere compilación) | Compilación manual necesaria | ⚠️ Requiere compilación, problemas conocidos |
| MT7921AU | AWUS036AXM | In-kernel (mt7921u) | **5.18+** | ❌ K5.10/5.15 no cumple el requisito |
| RTL8832CU | AWUS036AXER | Out-of-tree (requiere compilación) | Compilación manual necesaria | ❌ No recomendado, soporte ARM64 incierto |

Fuente de datos: [Tabla de soporte de chipsets USB WiFi de morrownr](https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Chipsets.md)

---

## Recomendación principal: ALFA AWUS036ACM (MediaTek MT7612U)

### Ficha técnica rápida

| Elemento | Contenido |
|------|------|
| Chipset | MediaTek MT7612U / MT7612UN |
| Especificación WiFi | 802.11ac (WiFi 5) doble banda AC1200 |
| Rendimiento pico | 5 GHz: 867 Mbps / 2.4 GHz: 300 Mbps |
| Antena | 2 × RP-SMA desmontables de 5 dBi doble banda |
| Interfaz | USB 3.0 (conector USB-C) |
| Potencia de transmisión | Potencia estándar, adecuada para conexión directa al puerto USB |

**Página del producto**: https://yupitek.com/en/products/alfa/awus036acm/

### Razón uno para recomendarlo: la única solución verdaderamente «sin drivers»

El chipset MT7612U que utiliza el AWUS036ACM tiene su driver `mt76x2u` integrado en la línea principal del kernel desde **Linux Kernel 4.19 (octubre de 2018)**. El AIB-NW01 ejecuta la versión de kernel 5.10.x, por lo tanto:

**Enchufas y funciona. Sin compilar, sin configurar.**

Esto es crucial en la plataforma Jetson — evitas por completo los tres grandes desafíos mencionados anteriormente (kernel personalizado, fallos de compilación, obsolescencia tras actualización).

### Razón dos: empíricamente verificado en plataformas ARM64

Un usuario de GitHub probó el AWUS036ACM en un entorno ARM64 + Kernel 5.10.198:

```
$ lsusb | grep MediaTek
ID 0e8d:7612 MediaTek Inc. MT7612U

$ dmesg | grep mt76
mt76x2u 1-1:1.0 wlx00c0ca9821a5: renamed from wlan0
```

**Funciona nada más sacarlo de la caja**, el módulo se llama `mt76x2u`, sin ningún paso adicional.

> Fuente: [GitHub issue #574 — AWUS036ACM en ARM64 K5.10](https://github.com/morrownr/USB-WiFi/issues/574)

### Razón tres: soporte completo de funciones profesionales

Este adaptador no solo sirve para conectarse a Internet, también soporta funciones profesionales completas de red inalámbrica:

- Modo monitor (Monitor mode) — para diagnóstico y análisis de redes
- Inyección de paquetes (Packet injection) — para pruebas de penetración e investigación
- Modo AP — permite convertir el AIB-NW01 en un punto de acceso WiFi (en 5 GHz puede requerir el parámetro de módulo `disable_usb_sg`)
- VIF (Virtual Interface) — permite ejecutar simultáneamente interfaces monitor + managed en el mismo adaptador

### Razón cuatro: flexibilidad de antenas sin comparación

El diseño con 2 antenas externas RP-SMA significa que puedes:

- Sustituirlas por antenas de alta ganancia (ej. 9 dBi) para ampliar la cobertura
- Usar antenas direccionales para concentrar la señal en una dirección específica
- Extender las antenas fuera de un chasis metálico mediante cables de prolongación (especialmente importante en armarios industriales)

---

## Cinco beneficios concretos del AWUS036ACM

### Beneficio uno: conexión inmediata, despliegue sin demora

Nada más insertarlo, el sistema lo reconoce como interfaz `wlan0` (o `wlx...`). El usuario solo necesita tres comandos:

```bash
# Escanear redes disponibles
sudo nmcli device wifi list

# Conectar
sudo nmcli device wifi connect "Tu_SSID" password "Tu_Contraseña"
```

Sin compilar, sin reiniciar, sin instalar ningún paquete.

### Beneficio dos: evita todas las limitaciones de los módulos WiFi M.2

| Módulo WiFi M.2 | Adaptador USB WiFi (AWUS036ACM) |
|---------------|--------------------------|
| Requiere desmontar el equipo | Externo, sin desmontar |
| Antena fijada dentro del chasis | Antena colocable en la posición óptima de señal |
| Difícil de reemplazar | Hot-plug, se cambia en segundos |
| Solo utilizable en ese equipo | Compartible entre dispositivos |

### Beneficio tres: adecuado para todo tipo de escenarios de despliegue industrial

El AWUS036ACM puede manejar los escenarios típicos de proyectos de Edge AI:

- **Líneas de producción** — ¿No hay puerto de red cableado junto al equipo? Enchúfalo y tendrás conexión inalámbrica
- **Vigilancia exterior** — WiFi es el único canal de retorno de datos
- **Despliegues temporales** — Fase de POC, sin querer desmontar para instalar un módulo M.2
- **Vehículos autónomos** — AGV/AMR necesitan conectividad inalámbrica estable

### Beneficio cuatro: el menor coste de mantenimiento a largo plazo

Las ventajas de usar un driver in-kernel son muy prácticas:

- El adaptador sigue funcionando tras actualizar JetPack (NVIDIA mismo mantiene los drivers integrados en el kernel)
- No hay que preocuparse por DKMS ni compilar drivers uno mismo
- Las actualizaciones de seguridad del kernel no se ven bloqueadas
- Se ahorran costes posteriores de mantenimiento y soporte

### Beneficio cinco: cobertura de señal optimizable según necesidades

El diseño con 2 antenas externas RP-SMA convierte este adaptador en una solución inalámbrica adaptable. Según el entorno de despliegue, puedes:

- Sustituir por antenas de alta ganancia (ej. 9 dBi) para ampliar la cobertura
- Usar antenas direccionales para concentrar la señal
- Colocar las antenas fuera del chasis metálico mediante cables de prolongación (escenarios de armario industrial)
- Usar antenas con base magnética adheribles a superficies metálicas

---

## Pasos de instalación: literalmente solo tres

### Paso 1: Insertar

Conecta el AWUS036ACM a un puerto USB 3.0 Type-A del AIB-NW01.

### Paso 2: Verificar que el driver se ha cargado

```bash
lsusb | grep MediaTek
# Salida esperada: ID 0e8d:7612 MediaTek Inc. MT7612U

dmesg | grep mt76
# Salida esperada: mt76x2u 1-1:1.0 wlx...: renamed from wlan0
```

### Paso 3: Conectarse al WiFi

```bash
# Escanear redes disponibles
sudo nmcli device wifi list

# Conectar
sudo nmcli device wifi connect "Tu_SSID" password "Tu_Contraseña"

# Verificar estado de la conexión
ip addr show wlx...
```

Hecho. Tu Jetson Orin ya está conectado a la red.

---

## Consideraciones y transparencia

### El AWUS036ACM es WiFi 5 (AC1200)

No es la opción más rápida del mercado. El AWUS036AXM (WiFi 6E, MT7921AU) es teóricamente más rápido, pero en el kernel 5.10 del AIB-NW01 **no funciona** (requiere Kernel 5.18+). Para las necesidades de ancho de banda de la mayoría de aplicaciones de Edge AI (transferencia de datos, actualización de modelos, SSH remoto), AC1200 es más que suficiente.

### Evidencia experimental en ARM64

La verificación del GitHub issue #574 se realizó en un **Odroid M1** (ARM64 + Kernel 5.10), no directamente en un AIB-NW01. Ambos comparten la misma arquitectura de kernel y pila de drivers, por lo que tenemos una alta confianza en que los resultados sean equivalentes. Aun así, recomendamos que cada usuario realice una verificación en su propio equipo.

### Escenarios aplicables para otros modelos

El AWUS036ACH (RTL8812AU) y el AWUS036AX (RTL8812BU) no es que no funcionen, simplemente requieren compilar el driver manualmente en Jetson. Si tienes experiencia con entornos de compilación y estás dispuesto a mantener el driver, estos modelos también merecen consideración.

---

## Conclusión: la solución más sencilla suele ser la mejor

Volviendo a la pregunta inicial del cliente: ¿qué adaptador USB WiFi de ALFA es el más adecuado para el AVALUE AIB-NW01?

La respuesta es el **ALFA AWUS036ACM**.

No porque sea el más rápido o el más barato — sino porque es, en una plataforma tan peculiar como Jetson, **la única solución que verdaderamente funciona con solo enchufarlo**. En una plataforma donde incluso compilar un driver falla con frecuencia, el driver in-kernel es el rey.

### Actúa ahora

- Consulta los detalles del producto: https://yupitek.com/en/products/alfa/awus036acm/
- Soporte técnico: Yupitek ofrece soporte técnico local en Taiwán, no dudes en contactarnos

### Lecturas recomendadas

- [AWUS036ACH vs AWUS036ACM: comparativa completa de drivers RTL8812AU vs MT7612U](https://yupitek.com/en/blog/awus036ach-vs-awus036acm/)
- [Tabla general de compatibilidad Linux de ALFA Network](https://docs.alfa.com.tw/Support/Compat/)
- [Lista oficial de módulos WiFi validados por NVIDIA (AGX Orin)](https://forums.developer.nvidia.com/t/wi-fi-6-6e-7-modules-that-have-been-validated-with-agx-orin-devkits/313431)

---

> **Etiquetas**: #JetsonOrin #EdgeAI #ALFANetwork #USBWiFi #AWUS036ACM #Yupitek
>
> **Autor**: Yupitek Ltd — Distribuidor autorizado de ALFA Network en Taiwán
>
> **Aviso legal**: Los datos de esta investigación están actualizados a mayo de 2026. La plataforma Jetson y el kernel de Linux están en continua evolución; se recomienda verificar el soporte del driver in-kernel con la última versión de JetPack antes de realizar el despliegue.
