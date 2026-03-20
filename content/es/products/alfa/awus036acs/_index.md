---
title: "ALFA AWUS036ACS — Adaptador USB AC600 Doble Banda (Investigación de Seguridad Básica)"
description: "ALFA AWUS036ACS, Realtek RTL8811AU, AC600 doble banda USB 2.0, 1× antena RP-SMA desmontable de 2 dBi, compatible con Monitor Mode e inyección de paquetes — ideal para investigación de seguridad básica."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "RP-SMA", "Monitor Mode", "Kali Linux", "Básico"]
---

{{< alert "warning" >}}
**Aviso Legal**: Las funciones de Monitor Mode e inyección de paquetes están destinadas exclusivamente a pruebas de seguridad autorizadas, investigación educativa y pruebas de penetración legales. Asegúrese siempre de contar con el permiso explícito del propietario de la red objetivo antes de utilizarlas.
{{< /alert >}}

## Descripción del Producto

El AWUS036ACS es el punto de entrada más asequible de Alfa en la gama de doble banda 802.11ac con soporte de modo monitor e inyección de paquetes. Equipado con el chipset Realtek RTL8811AU, es compacto y liviano, con una antena RP-SMA desmontable que puede actualizarse para mayor alcance. Aunque no es tan potente como el ACH o el ACM, es una opción práctica para principiantes en investigación de seguridad inalámbrica o usuarios que necesitan un adaptador de 5 GHz económico con capacidad de antena externa.

> **Aviso sobre macOS:** Todos los adaptadores ALFA tienen soporte limitado para macOS. macOS 10.15 Catalina y versiones posteriores, y todos los Mac con Apple Silicon (M1/M2/M3), **no son compatibles**. El AWUS036ACS es compatible hasta macOS 10.14 Mojave (solo Mac Intel).

## Características Principales

- Chipset Realtek RTL8811AU — modo monitor e inyección de paquetes compatibles
- WiFi 5 (802.11ac) doble banda — 2.4 GHz (150 Mbps) + 5 GHz (433 Mbps) = AC600
- 1× conector RP-SMA hembra con 1× antena mini desmontable de 2 dBi — actualizable a antenas de panel o alta ganancia
- Factor de forma compacto — perfil pequeño para fácil portabilidad
- Interfaz USB 2.0 (USB-A) — compatible con cualquier puerto USB
- Compatible con la antena de panel doble banda Alfa APA-M25 para recepción direccional
- Compatible con Kali Linux en Raspberry Pi (KaliPi) — instalación del controlador mediante DKMS

## Especificaciones Técnicas

| Parámetro | Valor |
|---|---|
| Chipset | Realtek RTL8811AU |
| Estándares WiFi | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bandas de Frecuencia | 2.4 GHz (150 Mbps) · 5 GHz (433 Mbps) |
| Velocidad Máxima Combinada | AC600 (150 + 433 Mbps) |
| Conector de Antena | 1× RP-SMA hembra |
| Antena Incluida | 1× dipolo mini doble banda, ganancia de 2 dBi |
| Interfaz USB | USB 2.0 Type-A |
| Sensibilidad de Recepción | 802.11b: −85 dBm · 802.11g: −69 dBm · 802.11n: −68 dBm · 802.11ac: −59 dBm |
| Seguridad Inalámbrica | WPA2 / WPA / WEP / 802.1X |
| País de Origen | Taiwán |

> ⚠️ **NOTA:** Solo USB 2.0 — velocidad máxima del bus de datos 480 Mbps. El rendimiento está limitado a 433 Mbps. Para máxima velocidad, use AWUS036ACM o AWUS036ACH con USB 3.0.

## Compatibilidad con SO

| Sistema Operativo | Estado | Notas |
|---|---|---|
| Windows XP–11 | ✅ Compatible | Controlador disponible en el sitio web de Alfa |
| macOS 10.5–10.14 | ⚠️ Limitado | macOS 10.15+ y Apple Silicon NO compatibles |
| Ubuntu | ✅ Compatible | Requiere instalación manual del controlador DKMS (morrownr/8821au). Sin soporte integrado en el kernel. |
| Kali Linux | ✅ Compatible | Modo monitor + inyección de paquetes compatible. Controlador de la comunidad morrownr GitHub. |
| NetHunter (Android) | ✅ Compatible | Conexión USB OTG; RTL8811AU tiene compatibilidad confirmada con NetHunter |

## Hardware Compatible

| Hardware | Estado | Notas |
|---|---|---|
| Raspberry Pi 3B+/4/5 | ✅ Compatible | Instalación específica para KaliPi disponible vía morrownr DKMS. |
| PC de Escritorio/Portátil | ✅ Compatible | USB-A estándar |
| Mac (Intel) | ⚠️ Limitado | Solo macOS 10.5–10.14 |

## Capacidades Avanzadas

| Función | Estado |
|---|---|
| Modo Monitor | ✅ Sí |
| Inyección de Paquetes | ✅ Sí |
| Modo Soft AP | ✅ Sí |
| Bluetooth | ❌ No |
| VIF | ⚠️ Limitado |

## Contenido del Paquete

- 1× Adaptador AWUS036ACS
- 1× Antena mini dipolo doble banda desmontable de 2 dBi

## Recursos y Enlaces

| Recurso | Enlace |
|---|---|
| Página Oficial del Producto | https://www.alfa.com.tw/products/awus036acs_1 |
| Documentación Oficial | https://docs.alfa.com.tw/Product/AWUS036ACS/ |
| Controlador Linux (RTL8811AU) | https://github.com/morrownr/8821au-20210708 |

## Descarga de Ficha Técnica

[📄 Descargar ficha técnica AWUS036ACS](/docs/alfa/AWUS036ACS_spec.pdf)

## Galería

{{< gallery >}}<img src="/images/products/alfa/awus036acs_image_1.png" alt="ALFA AWUS036ACS" />{{< /gallery >}}

---

{{< alert "info" >}}
¿Necesita una cotización? [Contáctenos](/es/contact/), ofrecemos asesoría de compra detallada.
{{< /alert >}}
