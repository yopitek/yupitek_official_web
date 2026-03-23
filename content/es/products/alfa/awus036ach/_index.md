---
title: "ALFA AWUS036ACH — Adaptador USB-C Inalámbrico AC1200 Doble Banda de Alta Potencia"
description: "ALFA AWUS036ACH, Realtek RTL8812AU, AC1200 doble banda, USB-C, 2 antenas externas 5 dBi, estándar de oro para investigación de seguridad en Kali Linux, Monitor Mode y Packet Injection."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB-C", "Doble Antena", "Monitor Mode", "Kali Linux", "Investigación de Seguridad"]
---

{{< alert "warning" >}}
**Aviso Legal**: Las funciones de Monitor Mode y Packet Injection son exclusivamente para pruebas de seguridad autorizadas, investigación educativa y pruebas de penetración legales. Asegúrese de contar con autorización explícita de la red objetivo.
{{< /alert >}}

## Descripción del Producto

El AWUS036ACH es el adaptador más icónico de ALFA Network — el estándar de oro para las pruebas de penetración en Kali Linux desde 2017. Impulsado por el probado chipset Realtek RTL8812AU, ofrece soporte sólido para Monitor Mode e inyección de paquetes, un amplificador de potencia integrado para recepción de largo alcance y dos antenas desmontables de 5 dBi. Fue el primer adaptador WiFi 5 del mundo con conector USB Type-C.

> **Nota macOS:** Todos los adaptadores ALFA tienen soporte limitado o nulo para macOS. macOS 11 Big Sur y versiones posteriores, y Apple Silicon (M1/M2/M3) **NO** son compatibles. El soporte máximo es macOS 10.15 Catalina en Mac Intel.

## Características Principales

- Realtek RTL8812AU — chipset más ampliamente probado para investigación de seguridad WiFi
- WiFi 5 (802.11ac) doble banda AC1200 — 867 Mbps en 5 GHz, 300 Mbps en 2.4 GHz
- Amplificador de potencia integrado — hasta 3× el alcance de las tarjetas de laptop típicas
- 2× RP-SMA hembra con 2× antenas duales de 5 dBi desmontables (actualizables)
- Primer adaptador WiFi 5 USB-C del mundo
- Soporte de clip para monitor incluido
- Soporte de inyección de paquetes en Kali Linux desde Kali 2017.1
- Compatible con 802.11a/b/g/n

## Especificaciones Técnicas

| Parámetro | Valor |
|-----------|-------|
| Chipset | Realtek RTL8812AU |
| Estándares WiFi | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bandas de Frecuencia | 2.4 GHz · 5 GHz (doble banda) |
| Velocidad Máxima de Datos | 802.11b: 11 Mbps · 802.11a/g: 54 Mbps · 802.11n: 300 Mbps · 802.11ac: 867 Mbps |
| Velocidad Máxima Combinada | AC1200 (867 + 300 Mbps) |
| Conectores de Antena | 2× RP-SMA hembra |
| Antenas Incluidas | 2× dipolo omnidireccional doble banda, 5 dBi |
| Interfaz USB | Type-C SuperSpeed USB (5 Gbps); compatible con USB 2.0 |
| Amplificador de Potencia | Sí — alcance extendido |
| Seguridad Inalámbrica | WPA3 / WPA2 / WPA / WEP / WPS / 802.1X |
| Accesorios | Clip para monitor · Cable USB |
| País de Origen | Taiwán |

## Compatibilidad con SO

| Sistema Operativo | Estado | Notas |
|-------------------|--------|-------|
| Windows 10 / 11 | ✅ Compatible | Descargar driver desde el sitio de Alfa; soporte WPA3 (driver oct. 2019+) |
| macOS 10.15 Catalina | ⚠️ Limitado | Instalación manual; macOS 11+ y Apple Silicon NO compatibles |
| Ubuntu | ✅ Compatible | Instalación manual RTL8812AU DKMS; integrado en Ubuntu 24.10+ (kernel ≥ 6.14) |
| Kali Linux | ✅ Excelente | Desde Kali 2017.1; Monitor Mode + Packet Injection completo; usar driver aircrack-ng |
| NetHunter (Android) | ✅ Compatible | OTG USB; ampliamente confirmado |

## Hardware Compatible

| Hardware | Estado | Notas |
|----------|--------|-------|
| Raspberry Pi 3B+/4/5 | ✅ Compatible | Driver manual via script morrownr DKMS |
| PC Escritorio/Laptop | ✅ Compatible | USB-C o USB-A (mediante cable incluido) |
| Mac (Intel) | ⚠️ Limitado | Máximo macOS 10.15 Catalina |

## Capacidades Avanzadas

| Función | Estado |
|---------|--------|
| Monitor Mode | ✅ Excelente (estándar de oro — probado por la comunidad desde 2017) |
| Packet Injection | ✅ Excelente |
| Modo Soft AP | ✅ Sí |
| Bluetooth | ❌ No |
| VIF | ⚠️ Limitado (use AWUS036ACM para soporte VIF completo) |

## Contenido del Paquete

- 1× Adaptador AWUS036ACH
- 2× Antenas dipolo doble banda desmontables de 5 dBi
- 1× Cable USB-C a USB-A
- 1× Clip para monitor

## Recursos y Enlaces

| Recurso | Enlace |
|---------|--------|
| Página Oficial del Producto | https://www.alfa.com.tw/products/awus036ach_1 |
| Documentación Oficial | https://docs.alfa.com.tw/Product/AWUS036ACH/ |
| Driver (aircrack-ng, recomendado para Kali) | https://github.com/aircrack-ng/rtl8812au |
| Driver (morrownr, Linux general) | https://github.com/morrownr/8812au-20210708 |

## Descarga de Ficha Técnica

| Documento | Descarga |
|-----------|---------|
| Ficha técnica oficial (PDF) | [📄 Descargar ficha técnica AWUS036ACH](/docs/alfa/AWUS036ACH_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ach_image_1.png" alt="ALFA AWUS036ACH" />
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
¿Necesita una cotización? [Contáctenos](/es/contact/), ofrecemos asesoría de compra detallada.
{{< /alert >}}
