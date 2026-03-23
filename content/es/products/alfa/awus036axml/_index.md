---
title: "ALFA AWUS036AXML — Adaptador USB Wi-Fi 6E Tribanda USB-C"
description: "ALFA AWUS036AXML con chipset MediaTek MT7921AUN. Wi-Fi 6E tribanda (2.4/5/6 GHz), interfaz USB-C, Bluetooth 5.2, soporte Monitor Mode en Kali Linux."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6E", "USB-C", "802.11ax", "Tribanda", "Bluetooth 5.2", "6GHz", "Kali Linux"]
---

{{< alert "warning" >}}
**Aviso Legal**: Las funciones de Monitor Mode y Packet Injection son exclusivamente para pruebas de seguridad autorizadas, investigación educativa y pruebas de penetración legales. Asegúrese de contar con autorización explícita de la red objetivo.
{{< /alert >}}

## Descripción del Producto

El AWUS036AXML incorpora el chipset MediaTek MT7921AUN con soporte Wi-Fi 6E tribanda (2.4 GHz / 5 GHz / 6 GHz), alcanzando hasta 3000 Mbps de rendimiento combinado, más Bluetooth 5.2 integrado. La interfaz USB-C incluye un cable 2-in-1 USB-C/USB-A y soporte de clip de pantalla.

> **Nota macOS:** Todos los adaptadores ALFA tienen soporte limitado o nulo para macOS. macOS 11 Big Sur y versiones posteriores, y Apple Silicon (M1/M2/M3) **NO** son compatibles. El soporte máximo es macOS 10.15 Catalina en Mac Intel.

## Características Principales

- Wi-Fi 6E Tribanda: 2.4 / 5 / 6 GHz
- Chipset MediaTek MT7921AUN
- Hasta 3000 Mbps de rendimiento combinado
- Bluetooth 5.2 (chip combinado)
- Interfaz USB-C (USB 3.2 Gen 1, 5 Gbps)
- Cable 2-in-1 USB-C/USB-A incluido
- 1× antena RP-SMA desmontable
- Soporte de clip de pantalla incluido
- WPA3/WPA2/WPA/WEP/WPS
- Monitor Mode en Kali Linux (kernel ≥ 5.18)

## Especificaciones Técnicas

| Elemento | Especificación |
|----------|----------------|
| Chipset | MediaTek MT7921AUN |
| Estándares WiFi | IEEE 802.11 a/b/g/n/ac/ax (WiFi 6E) |
| Bandas de frecuencia | 2.4 GHz (20/40 MHz) · 5 GHz (20/40/80 MHz) · 6 GHz (20/40/80 MHz) |
| Velocidad máxima | 2.4GHz: 600 Mbps · 5GHz: 1200 Mbps · 6GHz: 1200 Mbps · Total: 3000 Mbps |
| Bluetooth | BT 5.2 (chip combinado) |
| Conector de antena | 1× RP-SMA female (desmontable) |
| Interfaz USB | USB 3.2 Gen 1 Type-C (5 Gbps) |
| Cable | 2-in-1 USB-C/USB-A |
| Seguridad inalámbrica | WPA3 / WPA2 / WPA / WEP / WPS |
| País de origen | Taiwán |

## Compatibilidad con SO

| SO | Estado | Notas |
|----|--------|-------|
| Windows 10 | ✅ Compatible | Solo 2.4 GHz y 5 GHz; 6 GHz no disponible en Win10 |
| Windows 11 | ✅ Compatible | Tribanda completa incluyendo 6 GHz |
| macOS | ❌ No compatible | Sin soporte para macOS 11+ ni Apple Silicon |
| Ubuntu | ✅ Compatible | Driver mt7921u integrado en kernel ≥ 5.18 (Ubuntu 22.10+) |
| Kali Linux | ✅ Compatible | Monitor mode ≥ kernel 5.18; monitor mode activo ≥ 6.12; inyección de paquetes soportada |
| NetHunter (Android) | ⚠️ Parcial | OTG; depende del kernel |

## Hardware Compatible

| Hardware | Estado | Notas |
|----------|--------|-------|
| Raspberry Pi 3B+/4/5 | ✅ Compatible | Pi OS actualizado (kernel ≥ 5.18); puede necesitar copia de firmware |
| PC de escritorio/portátil | ✅ Compatible | USB-C o USB-A mediante cable 2-in-1 incluido |
| Mac Intel | ⚠️ Limitado | Máximo macOS 10.15 Catalina |

## Capacidades Avanzadas

| Función | Estado |
|---------|--------|
| Monitor Mode | ✅ Sí (kernel ≥ 5.18; modo activo ≥ 6.12) |
| Packet Injection | ✅ Sí |
| Soft AP Mode | ✅ Sí |
| Bluetooth | ✅ BT 5.2 |
| VIF | ✅ Sí |

## Contenido de la Caja

- 1× Adaptador AWUS036AXML
- 1× Antena dipolo desmontable
- 1× Cable 2-in-1 USB-C/USB-A
- 1× Soporte de clip de pantalla

## Recursos y Enlaces

| Recurso | Enlace |
|---------|--------|
| Página oficial del producto | https://www.alfa.com.tw/products/awus036axml |
| Documentación oficial | https://docs.alfa.com.tw/ |
| Driver Linux (integrado en kernel) | mt7921u — integrado en Linux kernel ≥ 5.18 |

## Descarga de Ficha Técnica

| Documento | Descarga |
|------|------|
| Ficha técnica oficial (PDF) | [📄 Descargar ficha técnica de AWUS036AXML](/docs/alfa/AWUS036AXML_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axml_image_1.png" alt="ALFA AWUS036AXML" />
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
¿Necesita una cotización? [Contáctenos](/es/contact/)
{{< /alert >}}
