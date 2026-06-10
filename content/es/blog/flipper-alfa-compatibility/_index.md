---
title: "Flipper Zero y Flipper One con Adaptadores WiFi ALFA: Guía Completa de Compatibilidad"
description: "¿Puede Flipper Zero usar adaptadores USB WiFi ALFA para inyección de paquetes? No: aquí te explicamos por qué. Flipper One soporta el AWUS036AXML de ALFA con modo monitor completo e inyección. Guía completa con análisis de chipset, compatibilidad de drivers e instrucciones de configuración."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-alfa-compatibility"
tags: ["flipper-zero", "flipper-one", "alfa-network", "wifi-adapter", "monitor-mode", "packet-injection", "kali-linux", "pentesting", "AWUS036AXML", "wireless-security"]
categories: ["Técnica"]
featureimage: "/images/blog/flipper-alfa-compatibility.webp"
---

{{< alert "triangle-exclamation" >}}
**Aviso Legal:** El modo monitor y la inyección de paquetes solo deben realizarse en redes de su propiedad o con autorización escrita explícita para realizar pruebas. La intercepción no autorizada de comunicaciones inalámbricas es ilegal en la mayoría de jurisdicciones. Todas las técnicas descritas en esta guía están destinadas exclusivamente a **pruebas de penetración autorizadas, investigación de seguridad en equipos propios y fines educativos**.
{{< /alert >}}

## Introducción: La pregunta que todo especialista en pentesting se hace

Si posee un Flipper Zero — o está considerando comprar uno — y ha escuchado sobre los legendarios adaptadores USB WiFi de ALFA Network para pruebas de seguridad inalámbrica, probablemente se ha preguntado: **"¿Puedo conectar mi adaptador ALFA a mi Flipper Zero y comenzar a capturar handshakes WPA2?"**

La respuesta corta es que no. Pero la respuesta completa es mucho más interesante.

**Flipper Zero no puede conectar ningún adaptador USB WiFi ALFA.** Esta es una limitación de hardware, no de software. El microcontrolador STM32WB55RG integrado en el Flipper Zero cuenta con un controlador USB que opera exclusivamente en **modo device** — no puede actuar como un host USB para impulsar periféricos externos como adaptadores WiFi.

Pero Flipper Devices ha anunciado un producto completamente nuevo: **Flipper One**. Construido sobre un Rockchip RK3576 con 8 GB de RAM ejecutando Debian Linux completo, Flipper One posee dos puertos USB 3.1 host y puede usar adaptadores ALFA directamente para pruebas de seguridad inalámbrica completas, incluyendo análisis de Wi-Fi 6E en 6 GHz. De hecho, el fundador de Flipper One, Pavel Zhovner, nombró específicamente al **ALFA AWUS036AXML** como adaptador oficial de pruebas en el anuncio del producto.

Este artículo explica el panorama completo de compatibilidad: qué funciona, qué no, por qué, y cómo configurar todo.

---

## Flipper Zero: ¿Por qué no puede usar adaptadores ALFA?

Para entender la limitación, necesita comprender qué hay dentro de un Flipper Zero.

### El Hardware

| Componente | Especificación |
|-----------|--------------|
| **MCU** | STMicroelectronics STM32WB55RG |
| **Arquitectura** | ARM Cortex-M4 (núcleo de aplicación) @ 64 MHz + ARM Cortex-M0+ (núcleo inalámbrico) @ 32 MHz |
| **RAM** | 256 KB (compartida entre núcleos) |
| **Almacenamiento** | 1 MB Flash + MicroSD |
| **Sistema Operativo** | FreeRTOS (sistema operativo en tiempo real) |
| **USB** | USB Type-C, USB 2.0 Full Speed (12 Mbps) |
| **Modo USB** | **Device only** — sin capacidad host ni OTG |

### La Limitación USB

El controlador USB del STM32WB55 es un **USB Full-Speed Device Controller**. Puede presentar el Flipper Zero a una computadora como un dispositivo USB (para transferencia de archivos, actualizaciones de firmware y la interfaz CLI), pero no puede actuar como un host USB. No hay hardware de controlador host en el chip — ninguna modificación de firmware puede añadir esta capacidad.

Para usar un adaptador USB WiFi ALFA, un dispositivo necesita:
1. **Hardware de controlador USB Host** — para enumerar y comunicarse con dispositivos USB
2. **Kernel de Linux con soporte de drivers WiFi** — para cargar drivers como `mt7921u`, `mt76` o `rtw88`
3. **Suministro de energía suficiente** — Los adaptadores ALFA típicamente consumen entre 500 mA y 900 mA a 5V

Flipper Zero no cumple con los tres requisitos:
- ❌ Sin controlador USB Host (hardware)
- ❌ Ejecuta FreeRTOS, no Linux — no existe un framework de drivers de kernel
- ⚠️ Salida GPIO 5V limitada a 1.2A total en todos los pines, solo cuando se activa manualmente

> **Veredicto:** Es **físicamente imposible** conectar cualquier adaptador USB WiFi ALFA a un Flipper Zero. Esta no es una limitación que se pueda sortear con software, actualizaciones de firmware o placas de expansión — está grabada en el silicio.

---

## Flipper Zero + WiFi Dev Board: Una Alternación Limitada

Flipper Devices vende una **WiFi Dev Board** oficial basada en el microcontrolador **ESP32-S2**. Esta placa se conecta al header GPIO del Flipper Zero y ofrece capacidades WiFi básicas de 2.4 GHz, pero **no** cambia la situación del host USB.

| Aspecto | Capacidad |
|--------|-----------|
| **Chip WiFi** | ESP32-S2 (Xtensa LX7 single-core, 240 MHz) |
| **Frecuencia** | Solo 2.4 GHz, 802.11 b/g/n |
| **USB Host** | ❌ La WiFi Dev Board no expone USB Host — el ESP32-S2 se conecta al Flipper Zero vía GPIO, no USB |
| **Firmware** | ESP32 Marauder (desarrollado por la comunidad) |

Con el **firmware ESP32 Marauder** instalado, la WiFi Dev Board puede realizar:

- ✅ Ataques de deautenticación (solo 2.4 GHz)
- ✅ Captura PMKID (solo 2.4 GHz)
- ✅ Escaneo de access points y transmisión de SSID
- ✅ Sniffing básico de paquetes (solo 2.4 GHz)

Lo que **no puede** hacer:

- ❌ Usar adaptadores USB ALFA externos (sin USB host)
- ❌ Operar en las bandas de 5 GHz o 6 GHz
- ❌ Lograr el alcance o la fiabilidad de inyección de un adaptador ALFA dedicado
- ❌ Ejecutar herramientas basadas en Linux como aircrack-ng, Kismet o Wireshark

> **Si solo cuenta con un Flipper Zero y necesita pruebas básicas de 2.4 GHz**, la WiFi Dev Board con ESP32 Marauder es un workaround funcional — aunque severamente limitado. Para cualquier cosa más allá de eso, necesita hardware diferente.

---

## Flipper One: La plataforma que ALFA estaba esperando

El **21 de mayo de 2026**, el fundador de Flipper Devices, Pavel Zhovner, publicó una entrada de blog titulada *"Flipper One — We Need Your Help"* anunciando un producto completamente nuevo. Flipper One no es una actualización del Flipper Zero — es una categoría totalmente diferente de dispositivo, diseñado para una capa distinta del stack de protocolos.

> *"Flipper Zero es la Capa 0 — acceso punto a punto sin conexión: NFC, RFID, Sub-GHz, infrarrojo. Flipper One es la Capa 1 — conectividad IP: Wi-Fi, Ethernet, 5G, satellite. No se reemplazan entre sí."*
> — Pavel Zhovner, flipper.net

{{< alert "circle-info" >}}
**Aviso de Disponibilidad:** Flipper One se encuentra actualmente en **developer preview**. La disponibilidad general, precios y distribución regional serán anunciados mediante crowdfunding. Siga [flipper.net](https://flipper.net) y el [Flipper One Developer Portal](https://docs.flipper.net/one) para actualizaciones.
{{< /alert >}}

### Especificaciones de Hardware

| Componente | Especificación |
|-----------|--------------|
| **CPU** | Rockchip RK3576: 4× Cortex-A72 + 4× Cortex-A53, hasta 2.2 GHz |
| **GPU** | ARM Mali-G52 MC3 (OpenGL ES 3.2, Vulkan 1.2) |
| **NPU** | 6 TOPS @ INT8 (puede ejecutar LLMs locales) |
| **Co-procesador** | Raspberry Pi RP2350B (dual M33 + dual RISC-V) para display/botones/energía |
| **RAM** | 8 GB LPDDR5 |
| **Almacenamiento** | 64 GB UFS 2.2 + MicroSD |
| **Sistema Operativo** | Debian 13 (Trixie) — Flipper Devices indica que apuntará al Linux Kernel 7.0 mainline sin dependencias de patches fuera del árbol |
| **USB Host** | USB-C2 + USB-A, ambos USB 3.1 (5 Gbps), ambos con capacidad host |
| **WiFi Integrado** | Wi-Fi 6E vía MT7921AUN (2.4/5/6 GHz, 2×2 MIMO) |
| **Ethernet** | 2× RJ45 Gigabit (soporta sniffing inline/MITM) |
| **Expansión M.2** | Key-B: PCIe 2.1 ×1 / USB 3.1 / SATA3 / tarjeta SIM |

### ¿Por qué Flipper One funciona con adaptadores ALFA?

A diferencia de Flipper Zero, Flipper One cumple con los tres requisitos:

1. ✅ **Controlador USB 3.1 Host**: Dos puertos USB con capacidad host que pueden enumerar y alimentar dispositivos externos
2. ✅ **Debian Linux completo**: Kernel de Linux estándar con soporte de drivers in-kernel para `mt7921u`, `mt76` y `rtw88`
3. ✅ **Energía suficiente**: Los puertos USB pueden entregar energía estándar bus; el GPIO proporciona 5V @ 2A y 3.3V @ 2A con protección eFuse

El ancho de banda USB 3.1 (5 Gbps) es más que suficiente — incluso el adaptador ALFA más rápido (AWUS036AXML en AXE3000) se limita al throughput práctico de USB 3.0 de ~1.2 Gbps.

### Entorno de Software

Flipper One ejecuta un entorno Debian estándar, lo que significa que puede instalar herramientas de seguridad inalámbrica directamente vía `apt`:

```bash
sudo apt update
sudo apt install aircrack-ng kismet wireshark hcxdumptool hashcat
```

Flipper One también introduce los **Flipper OS Profiles** — un sistema basado en snapshots que le permite crear entornos limpios y aislados. Puede mantener un perfil dedicado de "Pentest" con todas sus herramientas inalámbricas, y cambiar a un perfil limpio para uso diario sin contaminación cruzada.

---

## Adaptadores ALFA Recomendados para Flipper One

No todos los adaptadores ALFA funcionan por igual para pruebas de seguridad inalámbrica. Los factores clave son el **chipset**, la **maturidad del driver** y el **soporte in-kernel** (es decir, sin necesidad de compilar DKMS).

### ⭐⭐⭐⭐⭐ Opción Destacada: AWUS036AXML (Wi-Fi 6E)

| Espec | Detalle |
|------|--------|
| **Chipset** | MediaTek MT7921AUN |
| **Bands** | 2.4 / 5 / 6 GHz (Wi-Fi 6E) |
| **Max Speed** | AXE3000 (teórico), ~1.2 Gbps práctico |
| **Driver** | `mt7921u` — in-kernel desde Linux 5.18 |
| **DKMS Requerido** | ❌ No |
| **Antena** | Dual RP-SMA (reemplazable) + Bluetooth 5.2 |

> **Por qué es la mejor:** Este es el adaptador que el creador de Flipper One probó específicamente. El driver `mt7921u` está en el kernel mainline sin necesidad de patches de vendor. Soporta las tres bandas WiFi (2.4/5/6 GHz), lo que lo hace futuro-proof para evaluaciones de seguridad de Wi-Fi 6E. El modo monitor y la inyección de paquetes son estables y están bien probados.

### ⭐⭐⭐⭐⭐ Mejor Valor: AWUS036ACM (Wi-Fi 5 AC1200)

| Espec | Detalle |
|------|--------|
| **Chipset** | MediaTek MT7612U |
| **Bands** | 2.4 / 5 GHz (Wi-Fi 5) |
| **Max Speed** | AC1200 (300 + 867 Mbps) |
| **Driver** | `mt76` — in-kernel desde Linux 4.19 |
| **DKMS Requerido** | ❌ No |
| **Antena** | Dual 5 dBi RP-SMA (reemplazable) |

> **Por qué es la mejor opción en costo-beneficio:** El chipset MT7612U está ampliamente probado en la comunidad de pentesting. El driver `mt76` lleva años en el kernel y es excepcionalmente estable. El modo monitor y la inyección funcionan perfectamente en kernel 6.5 y superiores. A un precio menor que el AXML, ofrece la mejor relación precio-capacidad para pruebas de 2.4/5 GHz.

### ⭐⭐⭐⭐ Opción Ligera: AWUS036ACHM (Wi-Fi 5 AC433)

| Espec | Detalle |
|------|--------|
| **Chipset** | MediaTek MT7610U |
| **Bands** | 2.4 / 5 GHz (Wi-Fi 5) |
| **Max Speed** | AC433 (teórico) |
| **Driver** | `mt76` — in-kernel desde Linux 4.19 |
| **DKMS Requerido** | ❌ No |
| **Antena** | Single high-gain RP-SMA (reemplazable) |

> **Por qué es la opción más ligera:** La opción más portátil — USB 2.0, una sola antena, menor consumo de energía. Usa la misma familia de drivers `mt76` que el ACM. Ideal para trabajo de campo donde el tamaño y la eficiencia energética importan más que el throughput crudo. **Nota:** En plataformas ARM64 (incluido RK3576), ejecutar `airodump-ng` y `aireplay-ng` simultáneamente puede provocar un bug conocido de caída de interface (issue #379 de morrownr). Usar con conocimiento de causa.

### ⭐⭐⭐ Alternativa: AWUS036ACH (Wi-Fi 5 AC1200, RTL8812AU)

| Espec | Detalle |
|------|--------|
| **Chipset** | Realtek RTL8812AU |
| **Bands** | 2.4 / 5 GHz (Wi-Fi 5) |
| **Max Speed** | AC1200 (300 + 867 Mbps) |
| **Driver** | `rtw88` — in-kernel en el kernel planificado de Flipper One; sistemas más antiguos pueden requerir DKMS |
| **DKMS Requerido** | ❌ No requerido en Flipper One / ⚠️ Kernels más antiguos pueden requerir [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) DKMS |
| **Antena** | Dual 6 dBi RP-SMA (alto TX power) |

> **Por qué es una alternativa:** El chipset RTL8812AU tiene una larga trayectoria en pentesting. Se espera que sea soportado en el kernel planificado de Flipper One sin módulos DKMS adicionales. Para sistemas más antiguos, el driver DKMS de aircrack-ng sigue disponible. Las antenas de alta ganancia de 6 dBi proporcionan un excelente alcance, aunque los adaptadores basados en MediaTek generalmente se prefieren por su soporte de driver in-kernel más maduro.

### ⚠️ No Recomendado para Pentesting

Los siguientes modelos de ALFA utilizan chipsets Realtek con drivers de Linux inmaduros o inestables para modo monitor e inyección de paquetes. **Evite estos modelos para trabajo de seguridad inalámbrica en Flipper One:**

| Modelo | Chipset | Problema |
|-------|---------|-------|
| AWUS036AX | RTL8832BU | Chip Wi-Fi 6, soporte de driver aún en desarrollo en 2026 |
| AWUS036AXER | RTL8832BU | Mismos problemas de chipset que AWUS036AX |
| AWUS036ACS | RTL8811AU | Modo monitor limitado, inyección inestable |
| AWUS036EACS | RTL8811CU | Modo monitor limitado, inyección inestable |

---

## Guía de Configuración: Flipper One + ALFA AWUS036AXML

Esta guía asume que cuenta con un Flipper One ejecutando Debian Linux con el adaptador conectado físicamente a un puerto host USB.

### Paso 1: Verificar que el Adaptador sea Reconocido

```bash
# Verificar enumeración del dispositivo USB
lsusb
# Salida esperada (ejemplo):
# Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device

# Listar interfaces inalámbricas
iw dev
# Esperado: wlan0 (o wlan1 si el WiFi integrado ocupa wlan0)

# Verificación alternativa
ip link show
```

### Paso 2: Confirmar que el Driver Está Cargado

```bash
# Para AWUS036AXML / AWUS036AXM (MT7921AUN):
lsmod | grep mt7921u

# Para AWUS036ACM / AWUS036ACHM (MT7612U / MT7610U):
lsmod | grep mt76

# Para AWUS036ACH (RTL8812AU):
lsmod | grep rtw88

# Verificar versión del kernel (debería ser 6.12+ para mejor soporte de MT7921AUN):
uname -r
```

Si el módulo del driver aparece listado, está cargado y listo. No se necesita instalación adicional — todos estos son drivers in-kernel.

### Paso 3: Habilitar el Modo Monitor

```bash
# Detener procesos interferentes (NetworkManager, wpa_supplicant, etc.)
# Nota: Esto también desconectará el WiFi integrado de Flipper One — utilice un
# Flipper OS Profile dedicado para pentesting para no interrumpir su conexión normal.
sudo airmon-ng check kill

# Iniciar modo monitor en el adaptador
sudo airmon-ng start wlan0
# La interfaz se renombrará a wlan0mon

# Verificar que el modo monitor esté activo
iw dev wlan0mon info
# Debería mostrar: type monitor
```

Método manual (si prefiere no usar airmon-ng):

```bash
sudo ip link set wlan0 down
sudo iw wlan0 set monitor none
sudo ip link set wlan0 up
```

### Paso 4: Probar la Inyección de Paquetes

```bash
# Verificar capacidad de inyección
sudo aireplay-ng --test wlan0mon
# Buscar: "Injection is working!"

# Realizar un escaneo básico
sudo airodump-ng wlan0mon

# Escanear todas las bandas soportadas (solo AWUS036AXML)
sudo airodump-ng --band abg wlan0mon     # 2.4 GHz + 5 GHz
sudo airodump-ng --band 6 wlan0mon       # 6 GHz (aircrack-ng 1.7+)

# Dirigirse a un canal específico
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF wlan0mon
```

### Paso 5: Capturar un Handshake WPA2

```bash
# Terminal 1: Iniciar captura en el canal objetivo
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# Terminal 2: Enviar deauth para forzar reconexión
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon

# Verificar captura de handshake en Terminal 1:
# "WPA handshake: AA:BB:CC:DD:EE:FF" aparecerá cuando se capture
```

### Paso 6: Volver a la Operación Normal

```bash
# Detener modo monitor y restaurar modo managed
sudo airmon-ng stop wlan0mon

# Reiniciar servicios de red
sudo systemctl restart NetworkManager
```

### Descripción de la Arquitectura

El diagrama que aparece a continuación muestra la arquitectura completa de pentest inalámbrico con Flipper One y adaptadores ALFA:

![Flipper One + Adaptadores ALFA WiFi — Arquitectura de Pentest](diagram/flipper-alfa-topology.svg)

*Topología: Plataforma Flipper One → Adaptadores USB ALFA → Toolchain de pentest → Capacidades inalámbricas*

---

## Flipper Zero vs. Flipper One: Comparación Lado a Lado

| Característica | Flipper Zero | Flipper One |
|---------|:-----------:|:----------:|
| **Sistema Operativo** | FreeRTOS | Debian 13 (Trixie) |
| **CPU** | STM32WB55 (Cortex-M4, 64 MHz) | RK3576 (8-core ARM, 2.2 GHz) |
| **RAM** | 256 KB | 8 GB LPDDR5 |
| **Almacenamiento** | 1 MB Flash + MicroSD | 64 GB UFS 2.2 + MicroSD |
| **GPU / NPU** | ❌ | Mali-G52 GPU + 6 TOPS NPU |
| **USB Host** | ❌ Solo device | ✅ USB-C2 + USB-A (USB 3.1) |
| **Soporte Adaptadores ALFA** | ❌ | ✅ |
| **WiFi Integrado** | ❌ (Solo BLE) | ✅ Wi-Fi 6E (MT7921AUN) |
| **WiFi 5 GHz / 6 GHz** | ❌ | ✅ |
| **Ethernet Gigabit** | ❌ | ✅ 2× RJ45 |
| **Modo Monitor** | ❌ (nativo) | ✅ |
| **Inyección de Paquetes** | ❌ (nativo) | ✅ |
| **Expansión M.2** | ❌ | ✅ Key-B (PCIe / USB 3.1 / SATA) |
| **Precio** | ~$169 USD (en producción) | Developer preview (crowdfunding por definir) |

---

## Conclusión: La Herramienta Adecuada para Cada Trabajo

Si está intentando usar adaptadores WiFi ALFA para pruebas de seguridad inalámbrica, **Flipper Zero es la plataforma incorrecta** — no por culpa suya. Fue diseñado para un propósito diferente: pruebas de acceso control offline (NFC, RFID, Sub-GHz, infrarrojo). Excelle en esas tareas, pero la capacidad de host USB nunca formó parte de su diseño.

Para el caso de uso específico de **Monitor Mode y Packet Injection con adaptadores ALFA**, tiene dos caminos:

| Camino | Plataforma | Adaptador ALFA | Capacidad |
|------|----------|-------------|------------|
| **Óptimo** | Flipper One | AWUS036AXML (MT7921AUN) | 2.4/5/6 GHz completo, driver in-kernel, soporte oficial |
| **Mejor costo** | Flipper One | AWUS036ACM (MT7612U) | 2.4/5 GHz completo, driver in-kernel, probado y estable |
| **Workaround** | Flipper Zero + WiFi Dev Board | Ninguno (ESP32-S2 integrado) | Solo 2.4 GHz, alcance limitado, capacidades básicas |

**Flipper One representa un salto generacional** — lleva el poder completo de un entorno Debian Linux con capacidad de host USB 3.1 a una plataforma portátil diseñada para un propósito específico. Al combinarse con un ALFA AWUS036AXML (el adaptador que el creador de Flipper One probó específicamente), obtiene un kit completo de evaluación de seguridad inalámbrica en su bolsillo.

---

### Dónde Comprar

Todos los adaptadores ALFA recomendados están disponibles en Yupitek — un distribuidor autorizado de ALFA Network. Explore la selección completa o compare modelos:

- [Adaptadores USB WiFi ALFA — Catálogo Completo](https://yupitek.com/es/products/alfa/) — Todos los modelos con especificaciones y precios
- [Comparación de Productos ALFA](/es/alfa_compare/) — Comparación lado a lado de chipset, banda y driver

### Lecturas Complementarias

- [Entrada Oficial de Blog de Flipper One](https://blog.flipper.net/flipper-one-we-need-your-help/) — Pavel Zhovner, mayo 2026
- [Portal de Desarrollo de Flipper One](https://docs.flipper.net/one) — Especificaciones técnicas y documentación
- [¿Qué es la Inyección de Paquetes?](/es/blog/packet-injection-guide/) — Nuestra guía sobre fundamentos de packet injection
- [Reseña del AWUS036AXML WiFi 6E](/es/blog/awus036axml-wifi-6e-review/) — Reseña en profundidad de nuestro adaptador flagship
- [Comparación de Productos ALFA](/es/alfa_compare/) — Especificaciones lado a lado de todos los modelos ALFA

---

*Para preguntas previas a la compra sobre compatibilidad entre Flipper One y adaptadores ALFA, contacte al soporte de Yupitek en support@yupitek.com o llame al +886-2-87325338.*
