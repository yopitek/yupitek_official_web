---
title: "ALFA AWUS036ACM — Adaptador AC1200 de Doble Banda USB 3.0 (Mejor Plug & Play para Linux)"
description: "ALFA AWUS036ACM, MediaTek MT7612U, AC1200 doble banda USB 3.0, driver integrado en el kernel Linux desde la versión 4.19 (plug & play, sin compilación). Monitor mode, packet injection y VIF completos. Mejor adaptador Alfa para Raspberry Pi."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB 3.0", "Doble Banda", "Monitor Mode", "Kali Linux", "Raspberry Pi"]
---

{{< alert "warning" >}}
**Aviso Legal**: Las funciones de Monitor Mode e Inyección de Paquetes (Packet Injection) son exclusivamente para pruebas de seguridad autorizadas, investigación educativa y pruebas de penetración legítimas. Asegúrese de contar con la autorización explícita del propietario de la red objetivo.
{{< /alert >}}

## Descripción del Producto

El AWUS036ACM es la primera recomendación para usuarios de Linux que buscan una configuración sin complicaciones. Su chipset MediaTek MT7612U está integrado en el kernel de Linux desde la versión 4.19, lo que significa que funciona de inmediato en Ubuntu, Kali Linux, Raspberry Pi OS, Arch Linux y prácticamente cualquier distribución moderna sin compilar una sola línea de código. Tiene el mismo tamaño físico y configuración de antenas que el AWUS036ACH, pero utiliza el driver estable integrado en el kernel de MediaTek. Monitor mode, packet injection y VIF (Interfaz Virtual) están completamente soportados.

> **Aviso macOS:** Todos los adaptadores ALFA tienen soporte limitado o nulo para macOS. macOS 11+ y Apple Silicon (M1/M2/M3) **NO son compatibles**. El AWUS036ACM es compatible hasta macOS 10.12 Sierra como máximo — más restrictivo que la mayoría de otros modelos.

## Características Principales

- Chipset MediaTek MT7612U — driver Linux integrado en el kernel desde la versión 4.19 (plug & play, sin compilación)
- WiFi 5 (802.11ac) doble banda AC1200 — hasta 867 Mbps en 5 GHz, 300 Mbps en 2.4 GHz
- 2× conectores RP-SMA hembra con 2× antenas duales de banda de 5 dBi desmontables — formato físico idéntico al AWUS036ACH
- Interfaz USB 3.0 (USB-A)
- Soporte completo de monitor mode, packet injection y modo AP
- Soporte de VIF (Interfaz Virtual) en Kali Linux
- Cable de extensión USB 3.0 incluido
- Cumple con TAA — apto para adquisición gubernamental de EE. UU. (compatible con GSA)
- Funciona de inmediato en Raspberry Pi OS — sin instalación de drivers

## Especificaciones Técnicas

| Parámetro | Valor |
|-----------|-------|
| Chipset | MediaTek MT7612U |
| Estándares WiFi | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bandas de Frecuencia | 2.4 GHz (2.412–2.472 GHz) · 5 GHz (5.15–5.825 GHz) |
| Anchos de Canal | 20 / 40 / 80 MHz |
| Velocidad Máxima | 5 GHz: hasta 867 Mbps · 2.4 GHz: hasta 300 Mbps |
| Velocidad Máxima Combinada | AC1200 (867 + 300 Mbps) |
| Conectores de Antena | 2× RP-SMA hembra |
| Antenas Incluidas | 2× dipolo de doble banda, 5 dBi |
| Interfaz USB | USB 3.0 Type-A (retrocompatible con USB 2.0) |
| Potencia de Salida | 802.11a: 20 dBm · 802.11b: 23 dBm · 802.11g: 23 dBm · 802.11n: 21 dBm · 802.11ac: 20 dBm |
| Sensibilidad de Recepción | 802.11a: −92 dBm · 802.11b: −97 dBm · 802.11g: −90 dBm · 802.11n: −90 dBm |
| Seguridad Inalámbrica | WPA2 / WPA / WEP / WPA-PSK / 802.1X |
| LED | Sí (alimentación + actividad WLAN) |
| Accesorios | Cable de extensión USB 3.0 |
| País de Origen | Taiwán |

## Compatibilidad con SO

| SO | Estado | Notas |
|----|--------|-------|
| Windows XP–11 | ✅ Compatible | Driver desde el sitio web de Alfa. Se recomienda Windows 10/11. |
| macOS 10.7–10.12 | ⚠️ Limitado | Soporte oficial hasta macOS 10.12 Sierra. macOS 11+ y Apple Silicon NO compatibles. |
| Ubuntu 19.04+ | ✅ Plug & Play | Driver mt76 integrado en el kernel (kernel ≥ 4.19). Sin instalación de driver en Ubuntu 20.04 LTS y posteriores. |
| Kali Linux 2019.3+ | ✅ Plug & Play | Driver integrado en el kernel. Monitor mode confirmado. VIF compatible. El modo AP en 5 GHz puede requerir el parámetro de módulo `disable_usb_sg`. |
| NetHunter (Android) | ✅ Compatible | OTG USB; el driver integrado en el kernel ofrece mayor compatibilidad con Android que los adaptadores RTL. |

## Hardware Compatible

| Hardware | Estado | Notas |
|----------|--------|-------|
| Raspberry Pi 3B+/4/5 | ✅ Excelente | Funciona de inmediato en Raspberry Pi OS — sin instalación de driver. Mejor adaptador Alfa para Pi. |
| PC de escritorio/portátil | ✅ Compatible | USB-A estándar, con cable de extensión incluido. |
| Mac (Intel) | ⚠️ Limitado | Solo macOS 10.7–10.12. |

## Capacidades Avanzadas

| Función | Estado |
|---------|--------|
| Monitor Mode | ✅ Sí (integrado en kernel, sin pasos adicionales en distribuciones modernas) |
| Packet Injection | ✅ Sí |
| Modo Soft AP | ✅ Sí (AP en 5 GHz: añadir parámetro `disable_usb_sg` para mejor rendimiento) |
| Bluetooth | ❌ No |
| VIF (Interfaz Virtual) | ✅ Sí (soporte VIF completo en Kali) |

## Contenido del Paquete

- 1× Adaptador AWUS036ACM
- 2× Antenas dipolo de doble banda de 5 dBi desmontables
- 1× Cable de extensión USB 3.0
- 1× CD de driver (Windows)

## Recursos y Enlaces

| Recurso | Enlace |
|---------|--------|
| Página oficial del producto | https://www.alfa.com.tw/products/awus036acm_1 |
| Documentación oficial | https://docs.alfa.com.tw/Product/AWUS036ACM/ |
| Información del driver Linux (integrado en kernel) | Driver mt76 — incluido en el kernel Linux ≥ 4.19, sin instalación necesaria |

## Descarga de Ficha Técnica

| Documento | Descarga |
|-----------|----------|
| Ficha técnica oficial (PDF) | [📄 Descargar ficha técnica AWUS036ACM](/docs/alfa/AWUS036ACM_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036acm_image_1.png" alt="ALFA AWUS036ACM" />
{{< /gallery >}}

---

## Accesorios de Antena Compatibles

Todos los adaptadores USB ALFA utilizan un conector RP-SMA estándar. Mejora con una antena externa opcional para mayor alcance y ganancia:

| Antena | Frecuencia | Ganancia | Tipo |
|--------|-----------|----------|------|
| [ALFA APA-M04](/es/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | Panel interior direccional |
| [ALFA APA-M25](/es/products/alfa/apa-m25/) | 2.4 / 5 GHz | 7 dBi | Panel interior dual banda |
| [ALFA APA-M25-6E](/es/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 7 dBi | Panel interior tri banda |
| [ARS 25-57A](/es/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 2.5 / 7 dBi | Omnidireccional exterior |
| [ARS NT5B7](/es/products/alfa/ars-nt5b7/) | 2.4 / 5 GHz | 5 / 7 dBi | Omnidireccional |

{{< alert >}}
¿Necesita una cotización del producto? Por favor, [contáctenos](/es/contact/).
{{< /alert >}}
