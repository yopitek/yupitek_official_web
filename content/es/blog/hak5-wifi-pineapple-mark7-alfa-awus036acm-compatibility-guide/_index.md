---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM: Guía Completa de Configuración 5GHz (2026)"
description: "Guía completa de compatibilidad para HAK5 WiFi Pineapple MK7 con ALFA AWUS036ACM (MT7612U) — Modo Monitor 5GHz plug-and-play, inyección de paquetes y extensión PineAP. Instrucciones paso a paso con comandos verificados. No requiere compilación de controladores."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "¿WiFi Pineapple Mark VII necesita una tarjeta externa?"
    answer: "Sí. La radio integrada del MK7 solo admite 2.4 GHz. En 2026 la mayoría de redes han migrado a 5 GHz; conectar un AWUS036ACM añade capacidad de monitorización e inyección en 5 GHz."
  - question: "¿Por qué el AWUS036ACM es plug-and-play en el MK7?"
    answer: "El firmware 2.x del MK7 ya incluye el controlador kmod-mt76x2u. El chipset MT7612U está integrado en el kernel desde Linux 4.19; no necesita compilación ni instalación."
  - question: "¿El USB 2.0 del MK7 limita el rendimiento del AWUS036ACM?"
    answer: "USB 2.0 limita el throughput a 150-250 Mbps, pero las cargas de trabajo de pruebas de penetración como captura de paquetes y recolección de handshakes no se ven afectadas. Solo el bridging de alto throughput está limitado."
  - question: "¿Cómo activar el modo monitor en el MK7?"
    answer: "Inicia sesión por SSH y ejecuta airmon-ng start wlan3. La interfaz se renombrará a wlan3mon; verifica el modo con iwconfig."
  - question: "¿Qué tarjetas ALFA son incompatibles con el MK7?"
    answer: "AWUS036AX y AWUS036AXER usan el chip RTL8832BU, y AWUS036EACS usa RTL8811CU; sus controladores no admiten modo monitor ni inyección, por lo que son incompatibles."
---

El HAK5 WiFi Pineapple Mark VII es el estándar de referencia para auditorías de seguridad inalámbrica portátiles. Sin embargo, tiene una limitación importante: la radio integrada funciona exclusivamente en **2,4 GHz**. En 2026, la mayoría de las redes empresariales y domésticas han migrado a 5 GHz.

{{< tldr >}}
El AWUS036ACM usa el chipset MT7612U. El firmware 2.x del MK7 ya incluye el controlador; al conectarlo aparece como interfaz wlan3, con soporte de modo monitor de 5 GHz, inyección de paquetes y extensión PineAP. Se configura en 10 minutos.
{{< /tldr >}}

Aquí es donde entra el **ALFA AWUS036ACM**. Es uno de los pocos adaptadores 802.11ac [confirmados oficialmente como compatibles](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters) por Hak5. Gracias al controlador de kernel `mt76x2u` precargado en el Firmware MK7 2.x, funciona en **plug-and-play sin necesidad de compilar ningún controlador**.

---

## 1. Por qué tu WiFi Pineapple necesita 5 GHz

| Escenario | 2,4 GHz (integrado) | 5 GHz (AWUS036ACM) |
|---|---|---|
| Redes WPA2-Enterprise | Parcialmente presente | **Banda principal de despliegues modernos** |
| Sistemas Mesh domésticos | Fallback legacy | **Banda predeterminada para clientes** |
| Congestión de canales | Extremadamente congestionado (1–11) | Espectro limpio (36–165) |

---

## 2. Plataforma Objetivo

| Componente | Especificación |
|---|---|
| **SoC** | MediaTek MT7628AN (MIPS 24KEc) |
| **RAM** | 256 MB DDR2 |
| **Almacenamiento** | 2 GB eMMC |
| **USB Host** | 1× USB 2.0 Type-A (máx. 480 Mbps) |

> ✅ **Dato importante**: `kmod-mt76x2u` está precargado en el Firmware 2.x. El AWUS036ACM funciona en **plug-and-play**.

---

## 3. ALFA AWUS036ACM — Especificaciones

| Especificación | Detalle |
|---|---|
| **Chipset** | MediaTek MT7612U |
| **USB VID/PID** | `0E8D:7612` |
| **Bandas de frecuencia** | 2,4 GHz + 5 GHz |
| **Velocidad máxima** | 867 Mbps (5 GHz) |
| **Modo Monitor** | ✅ Soportado |
| **Inyección de paquetes** | ✅ Soportada |
| **Antena** | 2× 5 dBi RP-SMA (desmontable) |

---

## 4. Matriz de Compatibilidad — todas las pruebas superadas ✅

---

## 5. Configuración Paso a Paso

```bash
ssh root@172.16.42.1
lsusb                          # Paso 1: Verificar detección USB
lsmod | grep mt76              # Paso 2: Verificar controlador
iw dev                         # Paso 3: Verificar interfaz
airmon-ng check kill           # Paso 4: Activar Modo Monitor
airmon-ng start wlan3
iw wlan3mon set channel 36     # Paso 5: Escanear 5 GHz
airodump-ng --band a wlan3mon
aireplay-ng --test wlan3mon    # Paso 6: Probar inyección
```

---

## 6. Resultados de Validación — todas las pruebas superadas ✅

---

{{< faq >}}

## 7. Recomendación

**El ALFA AWUS036ACM es el mejor adaptador actualmente disponible para extender el WiFi Pineapple Mark VII a 5 GHz.**

👉 [Página del producto ALFA AWUS036ACM](/es/products/alfa/awus036acm/)

Yupitek es distribuidor autorizado de ALFA Network con soporte técnico completo.

*¿Necesitas ayuda con la configuración? Contacta al soporte de Yupitek: [yupitek.com/support](/es/support/)*

## Referencias

1. [Documentación oficial de Hak5 — Lista de adaptadores 802.11ac compatibles](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)
2. [Repositorio del controlador mt76 de OpenWrt — GitHub](https://github.com/openwrt/mt76)
3. [aircrack-ng — Sitio oficial del conjunto de herramientas de seguridad inalámbrica](https://www.aircrack-ng.org/)
4. [Sitio oficial de ALFA Network — Especificaciones del AWUS036ACM](https://www.alfa.com.tw/)
5. [Linux Wireless — Documentación del controlador MT76x2U](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
