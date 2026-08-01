---
title: "Cómo construir un router 4G/5G con Raspberry Pi y OpenWrt: matriz de compatibilidad de módulos Sierra y guía de configuración"
description: "Construya su propio router OpenWrt con una Raspberry Pi y módulos 4G/5G de Sierra Wireless (EM7455, EM7565, EM7511, EM919x, MC7455). Matriz de compatibilidad completa, configuración QMI/MBIM, conexión a internet con wwan0, además de pautas de alimentación y antenas."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "raspberry-pi-openwrt-lte-router"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/es/products/sierra/"
faq:
  - question: "¿Qué módulo Sierra debo elegir para un router OpenWrt en una Raspberry Pi?"
    answer: "Los principiantes deben comenzar con el EM7455 porque abundan los tutoriales y los problemas son fáciles de investigar. Elija el EM7565 o el EM7511 para una alta velocidad de subida, el EM919x para 5G, y el MC7455 para ranuras mPCIe heredadas."
  - question: "¿Cuál es la diferencia entre QMI y MBIM?"
    answer: "QMI es el protocolo de Qualcomm, mientras que MBIM es el protocolo estandarizado posterior. Ambos funcionan en OpenWrt, pero la mayoría de las guías en línea usan QMI."
  - question: "¿Qué debo hacer si la Raspberry Pi no detecta el módulo?"
    answer: "La causa más común es una alimentación USB insuficiente en la Raspberry Pi (la corriente de irrupción máxima puede alcanzar 2,5 A). Revise la entrega de energía de la placa adaptadora y el cableado, y espere unos diez segundos para que el módulo termine de iniciarse."
---

¿Puede una Raspberry Pi convertir un módulo 4G/5G de Sierra Wireless en un router OpenWrt totalmente funcional? Sí, puede. Los módulos M.2 como el EM7455, EM7565, EM7511 y EM919x son compatibles de forma nativa en Linux. Instale `kmod-usb-net-qmi-wwan` o `kmod-usb-net-cdc-mbim`, configure `wwan0`, y estará en línea. Este artículo cubre la matriz de compatibilidad completa de módulos, la configuración paso a paso, y los errores de alimentación y antenas que debe evitar.

{{< tldr >}}
Una Raspberry Pi con un módulo Sierra 4G/5G forma un router OpenWrt confiable. La mayoría de los módulos M.2 (EM7455, EM7565, EM7511) usan USB, el EM919x añade un carril PCIe Gen3, y el MC7455 es la versión mPCIe del EM7455. En OpenWrt, el protocolo QMI con `wwan0` es la ruta recomendada: instale `kmod-usb-net-qmi-wwan`, `uqmi` y `luci-proto-qmi`, configure el APN en `/etc/config/network`, y reinicie la red. En cuanto a velocidad: el EM7455 y el MC7455 son LTE Cat 6 (300/50 Mbps), el EM7565 y el EM7511 son Cat 12 (600/150 Mbps), y la familia EM919x ofrece 5G Sub-6 (el EM9190 añade mmWave).
{{< /tldr >}}

## Matriz de compatibilidad completa de módulos Sierra en OpenWrt

Antes de comenzar, verifique su módulo en esta tabla:

| Modelo | Clase de velocidad | Chip baseband | Factor de forma | Ruta de datos en Linux | Posicionamiento GNSS |
|---|---|---|---|---|---|
| **EM7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | M.2 (42x30 mm) | QMI (Linux) / MBIM | GPS/GLONASS/BeiDou/Galileo |
| **EM7565** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM (ambos en Linux) | añade QZSS |
| **EM7511** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM | añade QZSS |
| **EM919x** (9190/9191/7690) | 5G Sub-6 (el 9190 añade mmWave) | SDX55 | M.2 (52 mm de largo) | Windows/Linux | L1 + L5 (opcional) |
| **MC7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | mPCIe (50,95x30 mm) | QMI / MBIM | GPS/GLONASS/BeiDou/Galileo |

### Cómo elegir un módulo

- **Makers que comienzan**: elija el **EM7455**. Hay muchas guías y los problemas son fáciles de investigar.
- **Alta demanda de subida (streaming en vivo, vigilancia)**: elija el **EM7565** o el **EM7511** para hasta 150 Mbps de subida.
- **Se requiere 5G**: elija el **EM9190** para velocidades 5G.
- **Solo ranura mPCIe heredada**: opte por el **MC7455**.

## Tres formas de conectar el hardware

### A. Raspberry Pi 5 + HAT M.2 (PCIe)

La Pi 5 tiene PCIe, por lo que una placa portadora HAT+ M.2 le permite conectar un módulo WWAN M.2 directamente (confirme que sea de tecla B).

### B. Raspberry Pi 4B o anterior + carcasa adaptadora USB WWAN

Los módulos de la serie EM también admiten USB 2.0/3.0, por lo que una carcasa de M.2 a USB (normalmente con ranura SIM integrada) conectada al puerto USB de la Pi es la ruta más simple y accesible.

### C. Adaptador MC7455 (mPCIe)

El MC7455 usa la interfaz mPCIe más antigua, por lo que necesita una placa adaptadora de mPCIe a USB o de mPCIe a M.2.

> ⚠️ **La alimentación es la trampa más grande**: el módulo consume de 3,135 a 4,4 V (normalmente 3,3 V). Un error de "módulo no detectado" suele significar que la fuente USB de la Raspberry Pi no puede entregar suficiente energía. La corriente de irrupción puede dispararse hasta 2,5 A, así que deje un amplio margen en su fuente de alimentación.

## Entender QMI y MBIM

Ambos protocolos controlan cómo se conecta el módulo 4G/5G a la red:

- **QMI**: el protocolo propio de Qualcomm, usado por la mayoría de las guías de Linux/OpenWrt (la interfaz aparece como `wwan0`).
- **MBIM**: el protocolo estandarizado posterior, utilizable tanto en Windows como en Linux (la interfaz también aparece como `wwan0`).

**¿Cuál usar?** La mayoría de los usuarios pueden usar QMI directamente. Cambie a MBIM solo si su firmware lo requiere específicamente.

## Práctica, Parte 1: Configurar QMI en OpenWrt

Cuatro pasos, sin necesidad de compilar.

### 1. Instalar los paquetes

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi
```

### 2. Confirmar que la Raspberry Pi detecta el módulo

```bash
lsusb                                  # busque un dispositivo Sierra
ls /dev/cdc-wdm*                       # canal de control QMI
dmesg | grep qmi_wwan                  # compruebe que el controlador cargó
ip link show wwan0                     # compruebe que la interfaz apareció
```

### 3. Configurar el archivo de red (`/etc/config/network`)

Añada una sección QMI y reemplace el APN por el de su operador:

```bash
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option auth 'none'
```

### 4. Reiniciar la red

```bash
/etc/init.d/network restart
ifup wwan
```

Listo. Una vez que `wwan0` obtenga una dirección IP, estará en línea.

## Antenas y SIM: no las omita

El módulo **no tiene antena integrada**, y la calidad de la antena determina directamente su rendimiento.

- **Antena principal**: obligatoria.
- **Antena auxiliar (Aux)**: necesaria para velocidades MIMO; omitirla reduce el rendimiento.
- **Antena GNSS**: solo para casos de uso de posicionamiento. No la confunda con la antena principal.

## Errores comunes (lectura obligatoria para principiantes)

1. **`lsusb` no muestra nada**: el 99% de las veces se debe a alimentación insuficiente, una placa adaptadora floja o un cable defectuoso.
2. **Demasiada impaciencia**: el módulo necesita tiempo para iniciarse. Espere 10 segundos después de conectarlo antes de ejecutar comandos.
3. **Los módulos 5G (EM919x) generan mucho calor**: temperaturas en torno a 100 °C son comunes (máximo 115 °C), así que planifique la refrigeración.
4. **Conflictos con ModemManager**: al trabajar manualmente en un sistema Linux estándar, detenga `ModemManager` primero (`systemctl stop ModemManager`) para que no se apodere del módulo.

## Resumen

Conducir un módulo Sierra desde una Raspberry Pi con OpenWrt es un proceso de lista de verificación. Verifique el hardware (factor de forma, voltaje, antenas), instale los controladores QMI/MBIM y luego configure el APN. Esperamos que esta guía ahorre algunos desvíos a su proyecto y lleve su Raspberry Pi a la velocidad 4G/5G completa.

## Información de compra (llamada a la acción)

Si necesita módulos EM7455, EM7565 o EM7511, o placas adaptadoras M.2 y antenas compatibles, Yupitek ofrece soluciones de hardware completas y consultoría técnica.

Escríbanos por correo: **sales@yupitek.com**

Vea los productos: [Serie Sierra Wireless de Yupitek](https://yupitek.com/es/products/sierra/)
