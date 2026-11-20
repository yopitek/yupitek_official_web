---
title: "ALFA AWUS036EACS — Adaptador USB Nano AC600 + Bluetooth 4.2"
description: "ALFA AWUS036EACS, chipset Realtek RTL8821CU, AC600 doble banda, USB 2.0 Nano, Bluetooth 4.2. Controlador mainline rtw88_8821cu desde el kernel 6.2; en GX10 se superaron el monitor mode y la inyección en ambas bandas."
date: 2026-03-12
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "Nano", "Bluetooth 4.2", "Windows", "Hogar"]
---

## Descripción del Producto

El AWUS036EACS es el adaptador combinado de WiFi + Bluetooth ultracompacto de Alfa, diseñado para usuarios domésticos y de oficina que desean ambas conectividades en un único dongle USB discreto. Construido alrededor del chipset Realtek RTL8821CU, integra WiFi de doble banda AC600 y Bluetooth 4.2 en un factor de forma nano con soporte de controladores integrado en Windows. Su modo Soft AP le permite compartir la conexión a internet. En Linux, el controlador mainline rtw88_8821cu está incluido desde el kernel 6.2. En las pruebas con GX10 (Ubuntu 24.04, kernel 6.17), el monitor mode y la inyección de paquetes alcanzaron el 100 % en 2.4 GHz y 5 GHz, la captura de un handshake WPA de extremo a extremo tuvo éxito, y Bluetooth y Wi-Fi funcionaron a la vez.

> ⚠️ **Nota:** AWUS036EACS está diseñado para uso doméstico en Windows, pero también funciona en Linux con el controlador mainline rtw88_8821cu (kernel 6.2 o superior). Sin puerto RP-SMA — antena no actualizable.

## Características Principales

- WiFi doble banda AC600 802.11ac + Bluetooth 4.2 en un único adaptador USB nano
- Plug-and-play en Windows — el controlador integrado se instala automáticamente
- Modo Soft AP — crea un punto de acceso WiFi directamente desde el adaptador
- Ultracompacto y portátil — desaparece en cualquier puerto USB
- Doble banda: 2.4 GHz (150 Mbps) + 5 GHz (433 Mbps)
- Antena integrada de 2 dBi — sin conector RP-SMA externo
- Ideal para PCs de escritorio, sistemas embebidos o PCs domésticos que necesitan WiFi + BT en el mínimo espacio
- Bluetooth 4.2 soporta transmisión de audio, teclados, ratones y otros periféricos

## Especificaciones Técnicas

| Parámetro | Valor |
|-----------|-------|
| Chipset | Realtek RTL8821CU |
| Estándares WiFi | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bluetooth | BT 4.2 (2.4 GHz) |
| Bandas de Frecuencia | WiFi: 2.4 GHz · 5 GHz · BT: 2.4 GHz |
| Velocidad Máxima | 802.11b: 11 Mbps · 802.11g: 54 Mbps · 802.11n: 150 Mbps · 802.11ac: 433 Mbps |
| Velocidad Combinada Máxima | AC600 (150 + 433 Mbps) |
| Antena | Integrada, 2 dBi (no desmontable, sin RP-SMA) |
| Interfaz USB | USB 2.0 |
| Potencia de Salida | 17 dBm típico |
| Sensibilidad de Recepción | 802.11b: −85 dBm · 802.11g: −69 dBm · 802.11n: −68 dBm · 802.11ac: −59 dBm |
| Seguridad Inalámbrica | WEP / WPA-PSK / WPA2-PSK / 802.1X |
| Temperatura de Operación | −10°C a 60°C |
| Factor de Forma | Nano / perfil bajo |
| País de Origen | Taiwán |

## Compatibilidad con SO

| Sistema Operativo | Estado | Notas |
|------------------|--------|-------|
| Windows XP–10 | ✅ Compatible | Controlador integrado; plug and play. Consulte la página de controladores de Alfa para Windows 11. |
| macOS | ⚠️ Limitado | Rango de versiones exacto por confirmar. Sin soporte para Apple Silicon. |
| Ubuntu / Linux | ✅ Kernel 6.2 o superior | Controlador mainline rtw88_8821cu, sin instalación (probado en GX10, Ubuntu 24.04, kernel 6.17). |
| Kali Linux | ✅ Compatible | Monitor mode e inyección de paquetes verificados en GX10 (Ubuntu 24.04, kernel 6.17): 100 % en ambas bandas, captura de handshake WPA de extremo a extremo con éxito. No probado en un Kali real. |
| NetHunter (Android) | ❌ No recomendado | RTL8821CU no confirmado compatible con NetHunter. |

## Hardware Compatible

| Hardware | Estado | Notas |
|----------|--------|-------|
| Raspberry Pi | ⚠️ No probado | No probado por nosotros; el kernel 6.2 o superior incluye el controlador mainline rtw88_8821cu. |
| PC de escritorio / Portátil | ✅ Compatible | Solo se recomienda Windows. |
| Embebido / IoT (Windows) | ⚠️ Solo Windows | El diseño compacto se adapta a sistemas Windows embebidos. |

## Capacidades Avanzadas

| Función | Estado |
|---------|--------|
| Modo Monitor | ✅ Sí (prueba GX10: 100 % en ambas bandas) |
| Inyección de Paquetes | ✅ Sí (prueba GX10: 100 % en ambas bandas) |
| Modo Soft AP | ✅ Sí |
| Bluetooth | ✅ BT 4.2 (utilizable a la vez que el Wi-Fi) |
| VIF | 🟡 Parcial (monitor pasivo + managed en el mismo canal; sin VIF dual independiente) |

## Contenido del Paquete

- 1× Adaptador nano AWUS036EACS

## Recursos y Enlaces

| Recurso | Enlace |
|---------|--------|
| Página Oficial del Producto | https://www.alfa.com.tw/products/awus036eacs_1 |
| Documentación Oficial | https://docs.alfa.com.tw/Product/AWUS036EACS/ |

## Descarga de Ficha Técnica

Ficha técnica próximamente disponible.

{{< gallery >}}
  <img src="/images/products/alfa/awus036eacs_image_1.png" alt="ALFA AWUS036EACS" />
{{< /gallery >}}

---

## Accesorios de Antena Compatibles

Todos los adaptadores USB ALFA utilizan un conector RP-SMA estándar. Mejora con una antena externa opcional para mayor alcance y ganancia:

| Antena | Frecuencia | Ganancia | Tipo |
|--------|-----------|----------|------|
| [ALFA APA-M04](/es/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | Panel interior direccional |
| [ALFA APA-M25](/es/products/alfa/apa-m25/) | 2.4 / 5 GHz | 8 / 10 dBi | Panel interior dual banda |
| [ALFA APA-M25-6E](/es/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 8 / 10 / 9 dBi | Panel interior tri banda |
| [ARS 25-57A](/es/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 5 / 7 dBi | Omnidireccional exterior |
| [ARS NT5B7](/es/products/alfa/ars-nt5b7/) | 2.4 / 5 / 6 GHz | 4 / 5 / 7 dBi | Omnidireccional |

{{< alert >}}
¿Necesita una cotización del producto? Por favor, [contáctenos](/es/contact/).
{{< /alert >}}
