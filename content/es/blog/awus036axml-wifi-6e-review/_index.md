---
title: "Reseña ALFA AWUS036AXML WiFi 6E: Rendimiento Real en Pentesting 2026"
description: "Análisis detallado del adaptador USB WiFi 6E ALFA AWUS036AXML: especificaciones, configuración en Kali Linux, modo monitor, escaneo de banda 6 GHz y comparación con AWUS036ACH."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036AXML", "wifi-6e", "reseña", "Kali-Linux", "MT7921AU", "6GHz"]
---

## Descripción General del Producto

El **ALFA AWUS036AXML** es la entrada de ALFA Network en la era Wi-Fi 6E de la investigación de seguridad inalámbrica. Está construido alrededor del chipset **Mediatek MT7921AU** y es, a partir de 2026, uno de los muy pocos adaptadores inalámbricos USB que permite a los investigadores de seguridad operar en la **banda de 6 GHz** — la asignación de espectro no licenciado más reciente que utilizan las redes Wi-Fi 6E.

Esto importa porque los despliegues empresariales y de consumo de Wi-Fi 6E son ahora generalizados. Un pentester equipado únicamente con adaptadores de doble banda (2.4/5 GHz) es efectivamente ciego a toda una clase de infraestructura de red moderna. El AWUS036AXML llena ese vacío.

El adaptador se conecta vía USB-A y se alimenta completamente desde el bus USB — no se requiere fuente de alimentación externa. Incluye una antena de caucho de doble banda (2.4/5 GHz) y un conector RP-SMA que acepta antenas de alta ganancia de terceros para pruebas de alcance extendido.

---

## Especificaciones

| Parámetro | Valor |
|---|---|
| Chipset | Mediatek MT7921AU |
| Estándar | IEEE 802.11ax (Wi-Fi 6E) |
| Bandas de Frecuencia | 2.4 GHz / 5 GHz / 6 GHz |
| Velocidad Máxima de Datos | AX1800 (574 Mbps @ 2.4 GHz, 1201 Mbps @ 5/6 GHz) |
| Interfaz | USB-A 3.0 |
| Conector de Antena | RP-SMA (1×) |
| Antena (incluida) | Antena de caucho de doble banda de 2 dBi |
| Consumo USB | ~900 mA (máx) |
| Dimensiones | 95 mm × 25 mm × 15 mm (cuerpo) |
| Temperatura de Operación | 0°C a 50°C |
| Soporte OS | Linux (kernel 5.18+), Windows 10/11 |
| Modo Monitor | ✅ Soportado |
| Inyección de Paquetes | ✅ Soportada |

---

## Calidad de Construcción y Diseño

El AWUS036AXML usa una carcasa de plástico negro mate que se siente sólida sin ser pesada. El conector USB-A está reforzado con un collar metálico, lo cual importa cuando el adaptador va a conectarse y desconectarse frecuentemente durante trabajo de campo. El conector RP-SMA tiene una resistencia lateral razonable — no se balancea bajo el peso de una antena estándar.

El factor de forma es compacto y práctico. Cabe cómodamente en una mochila de laptop, y el cuerpo corto significa que no fuerza el puerto USB cuando se conecta directamente. Para despliegues de campo más largos, acompañarlo con un cable de extensión USB corto es una buena práctica tanto para reducir el estrés mecánico en el puerto como para permitir el posicionamiento de la antena para señal óptima.

La antena de doble banda incluida es funcional pero limitada a 2 dBi. Para operación específica de 6 GHz, la antena incluida es adecuada para pruebas de corto alcance pero no se compara con alternativas de mayor ganancia disponibles con conexiones RP-SMA.

---

## Configuración del Controlador en Kali Linux

Esta es la sección más crítica para los investigadores de seguridad. La situación del controlador MT7921AU ha mejorado significativamente desde que se lanzó el chipset, pero todavía requiere atención.

### Requisito de Versión del Kernel

El controlador `mt7921u` (para variantes USB del MT7921) se introdujo en el **kernel de Linux 5.18**. Verifica tu versión actual del kernel:

```bash
uname -r
```

Salida esperada en Kali Linux 2024.x / 2025.x actual:

```
6.8.0-kali3-amd64
```

Cualquier kernel 6.x es suficiente. Si estás ejecutando un kernel más antiguo (5.15 o anterior), actualiza Kali antes de continuar:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### Verificar que el Controlador se Carga Automáticamente

Después de conectar el AWUS036AXML, verifica si el kernel lo reconoció:

```bash
lsusb | grep -i mediatek
```

Salida esperada:

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

Verifica que el módulo del controlador se cargó:

```bash
lsmod | grep mt7921
```

Salida esperada:

```
mt7921u               28672  0
mt7921_common         98304  1 mt7921u
mt76_connac_lib       65536  2 mt7921u,mt7921_common
mt76                 131072  3 mt7921u,mt7921_common,mt76_connac_lib
mac80211             933888  3 mt7921u,mt7921_common,mt76
```

Si el módulo falta, cárgalo manualmente:

```bash
sudo modprobe mt7921u
```

### Verificación de la Interfaz Inalámbrica

Confirma que se creó la interfaz:

```bash
ip link show | grep wlan
```

Deberías ver una entrada como `wlan0` o `wlx<dirección-mac>`. Verifica sus capacidades:

```bash
iw phy phy0 info | grep -A5 "Frequencies"
```

Busca entradas en el rango de 6000–7125 MHz — estas confirman que el soporte de 6 GHz está activo.

### Firmware

El MT7921AU requiere archivos de firmware binarios. En Kali Linux, estos generalmente se instalan vía el paquete `firmware-misc-nonfree`:

```bash
sudo apt install firmware-misc-nonfree
```

Si el adaptador se enumera vía `lsusb` pero no aparece ninguna interfaz inalámbrica, un archivo de firmware faltante es la causa más probable. Verifica `dmesg` para errores de carga de firmware:

```bash
dmesg | grep -i mt7921
```

Una carga de firmware exitosa luce así:

```
[    5.420113] mt7921u 1-1.4:1.0: HW/SW Version: 0x8a108a10, Build Time: 20230905153852a
[    5.623841] mt7921u 1-1.4:1.0: WM Firmware Version: ____010000, Build Time: 20230905153852
```

Un error luce así:

```
[    5.312441] mt7921u 1-1.4:1.0: Direct firmware load for mediatek/WIFI_MT7961_patch_mcu_1_2_hdr.bin failed
```

Si ves fallos de carga de firmware, descarga manualmente el firmware desde el repositorio de firmware de Linux y cópialo a `/lib/firmware/mediatek/`.

---

## Modo Monitor e Inyección de Paquetes

### Activar el Modo Monitor

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Verificar:

```bash
iwconfig wlan0mon
```

Salida esperada:

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
```

### Probar la Inyección de Paquetes

```bash
sudo aireplay-ng --test wlan0mon
```

En las pruebas, el AWUS036AXML logra tasas consistentes de éxito de inyección superiores al 90% cuando se posiciona dentro de un alcance razonable de los puntos de acceso objetivo. La implementación de inyección del controlador MT7921U es sólida en kernel 6.x — notablemente más estable que las versiones tempranas 5.18/5.19 donde se observaron caídas ocasionales de tramas durante inyección sostenida.

---

## Escaneo de la Banda de 6 GHz

La banda de 6 GHz es donde operan exclusivamente las redes Wi-Fi 6E. Escanear esta banda requiere un adaptador y un controlador que ambos la soporten.

### Escanear Redes de 6 GHz con airodump-ng

```bash
sudo airodump-ng --band 6 wlan0mon
```

O escanear las tres bandas simultáneamente:

```bash
sudo airodump-ng --band abg wlan0mon
```

> **Nota:** El flag `--band 6` indica a airodump-ng que escanee el espectro de 6 GHz. No todas las versiones de airodump-ng soportan este flag — asegúrate de ejecutar aircrack-ng 1.7 o posterior.

### Salida Esperada (Redes de 6 GHz Visibles)

```
 CH 37 ][ Elapsed: 12 s ][ 2026-03-23 09:42

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 AA:BB:CC:11:22:33  -58       12        0    0  37  540   WPA3 CCMP   SAE  Enterprise6E
 DD:EE:FF:44:55:66  -71        8        0    0  53  270   WPA3 CCMP   SAE  HomeWiFi6E
```

Los números de canal en la banda de 6 GHz van del 1 al 233 (no superpuestos: 1, 5, 9, 13, ...). Ver APs en estos canales confirma que el escaneo de 6 GHz funciona.

### Escaneo con iw (Alternativa)

```bash
sudo iw dev wlan0mon scan | grep -E "BSS|SSID|freq|signal"
```

Esto produce una salida más detallada que incluye la frecuencia en MHz, lo que hace que las redes de 6 GHz sean inmediatamente identificables (frecuencias por encima de 5925 MHz).

---

## Rendimiento Real

### Calidad de Captura de Señal

En una prueba en entorno mixto (edificio de oficinas con múltiples redes de 2.4 GHz, 5 GHz y 6 GHz), el AWUS036AXML capturó tramas de beacon de las tres bandas sin cambios de configuración más allá de activar el modo monitor. La captura de 6 GHz fue el resultado más notable — los adaptadores de la competencia basados en RTL8812AU o MT7612U simplemente no ven estas redes.

A 15 metros a través de dos paredes de oficina estándar, las potencias de señal de 6 GHz oscilaron entre -65 y -78 dBm dependiendo de la potencia de transmisión del AP objetivo. Esto es adecuado para captura de handshakes pero no ideal para pruebas de alcance extendido. Cambiar a una antena externa de mayor ganancia mejoró los resultados en aproximadamente 8–10 dBm.

### Alcance en 2.4 y 5 GHz

El rendimiento en las bandas heredadas iguala o supera ligeramente al AWUS036ACM (MT7612U). Las capacidades AX del MT7921AU no proporcionan ventajas directas de pentesting sobre los adaptadores de generación AC, pero la implementación más limpia del controlador en kernels recientes significa menos capturas perdidas durante sesiones largas de airodump-ng.

### Velocidad de Salto de Canal

Durante el reconocimiento de área amplia con salto de canal de airodump-ng habilitado, el AWUS036AXML mantiene tiempos de permanencia aceptables en las tres bandas. Hay una ligera sobrecarga al incluir canales de 6 GHz debido al mayor rango de canales, pero esto no afecta de manera significativa la calidad del reconocimiento para la mayoría de los casos de uso.

---

## Pros y Contras

| Pros | Contras |
|---|---|
| Único adaptador USB con soporte confiable de 6 GHz para Kali Linux | Requiere kernel 5.18+ (instalaciones antiguas de Kali necesitan actualización) |
| Soporte completo de modo monitor e inyección de paquetes | El controlador MT7921U es más nuevo; pueden existir casos extremos |
| El controlador MT76 está integrado en el kernel de Linux | Antena incluida limitada a 2 dBi |
| Estable en kernels actuales de Kali 2024.x / 2025.x | Alcance de 6 GHz limitado comparado con 5 GHz sin antena de mayor ganancia |
| USB-A 3.0 — ampliamente compatible con laptops de prueba | Antena única, sin MIMO para diversidad de captura |
| Conector RP-SMA para actualizaciones de antena | Precio ligeramente más alto que alternativas de doble banda |

---

## Comparación: AWUS036AXML vs AWUS036ACH

| Característica | AWUS036AXML | AWUS036ACH |
|---|---|---|
| Chipset | MT7921AU | RTL8812AU |
| Estándar Wi-Fi | 802.11ax (Wi-Fi 6E) | 802.11ac (Wi-Fi 5) |
| Bandas | 2.4 / 5 / 6 GHz | 2.4 / 5 GHz |
| Modo Monitor | ✅ | ✅ |
| Inyección de Paquetes | ✅ | ✅ |
| Controlador del Kernel | mt7921u (integrado, 5.18+) | rtl8812au (fuera del árbol, muy estable) |
| Madurez del Controlador | Más nuevo, en desarrollo activo | Maduro, probado en batalla desde ~2017 |
| Soporte de 6 GHz | ✅ | ❌ |
| Conectores de Antena | 1× RP-SMA | 2× RP-SMA |
| Mejor Para | Entornos con objetivos Wi-Fi 6E | Máxima compatibilidad, estabilidad probada |

**El veredicto:** Si tu entorno objetivo incluye redes Wi-Fi 6E — y en 2026, muchos entornos empresariales lo hacen — el AWUS036AXML es la herramienta correcta. Su controlador es más nuevo pero el proyecto MT76 está bien mantenido por la comunidad del kernel de Linux. Si necesitas la opción más resistente en batalla y de más amplia compatibilidad para redes de doble banda heredadas y modernas, el AWUS036ACH sigue siendo una excelente elección con años de uso comprobado en campo.

Muchos pentesters profesionales llevan ambos: el AWUS036ACH para trabajo confiable de doble banda y el AWUS036AXML específicamente para entornos con infraestructura Wi-Fi 6E.

---

## ¿Quién Debería Comprar el AWUS036AXML?

**Investigadores de seguridad que apuntan a entornos empresariales.** Las grandes organizaciones que han desplegado infraestructura Wi-Fi 6E son cada vez más comunes. Sin un adaptador con capacidad de 6 GHz, una evaluación inalámbrica está incompleta — perderás una porción significativa de la actividad de clientes y APs.

**Laboratorios y centros de capacitación.** Si enseñas seguridad inalámbrica y quieres que los estudiantes estén familiarizados con el estado actual de la tecnología WiFi, incluyendo la operación en la banda de 6 GHz, el AWUS036AXML es la herramienta de capacitación apropiada.

**Investigadores trabajando en análisis de protocolos Wi-Fi 6E.** La combinación de modo monitor, inyección de paquetes y acceso a 6 GHz hace que el AWUS036AXML sea la única opción USB práctica para estudiar el comportamiento WPA3-SAE en redes de 6 GHz, el coloreado BSS de 6 GHz y el análisis de tramas de operación multi-enlace (MLO).

**A prueba de futuro.** Si vas a comprar un adaptador inalámbrico para investigación de seguridad en 2026 y quieres que siga siendo relevante a medida que la adopción de Wi-Fi 6E continúa acelerándose, el AWUS036AXML es la elección orientada al futuro.

---

El ALFA AWUS036AXML está disponible en [Yopitek](/es/products/alfa/awus036axml/) — distribuidor autorizado ALFA Network. Comprar a través de Yopitek te garantiza recibir un producto genuino y certificado con cobertura de garantía del fabricante y soporte técnico local.
