---
title: "Comparativa de adaptadores WiFi USB ALFA Network"
description: "Comparativa completa de especificaciones de 9 adaptadores WiFi USB ALFA Network: chipset, controlador Linux, capacidad de monitor / injection / AP, con resultados medidos en un ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17)."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
---

La tabla siguiente compara los 9 adaptadores WiFi USB ALFA Network. Las columnas Monitor, Injection, AP y handshake de extremo a extremo son resultados medidos en las pruebas de Yopitek en un ASUS GX10 (Ubuntu 24.04 LTS / ARM64 / kernel 6.17), con nuestro propio equipo y el WiFi de nuestra propia oficina — no cifras copiadas de las hojas de datos.

## Comparativa completa de especificaciones

En el móvil, desplace la tabla horizontalmente; toque el nombre de un modelo para ir a su página de producto.

| Modelo | Generación WiFi | Chipset | Bandas | Velocidad máx. | USB | Antenas | MIMO | Monitor Mode | Packet Injection | Handshake (prueba GX10) | Controlador Linux | Tipo de controlador | Modo AP | Potencia máx. | Bluetooth | Ideal para |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [AWUS036AXML](/es/products/alfa/awus036axml/) | WiFi 6E | MT7921AUN | 2.4 + 5 + 6 GHz | 3000 Mbps | USB-C 3.2 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Sí | ❌ Falla en el kernel 6.17 estándar | ❌ No (la injection falla) | En el kernel ≥5.18 | En el kernel (Plug & Play) | ✅ Nativo | 3.6W | BT 5.2 | WiFi 6E + Linux + USB-C |
| [AWUS036AXM](/es/products/alfa/awus036axm/) | WiFi 6E | MT7921AUN | 2,4 + 5 + 6 GHz (6 GHz sin probar) | 3000 Mbps | USB-A 3.2 L | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Sí | ❌ Falla en el kernel 6.17 estándar | ❌ No (la injection falla) | En el kernel ≥5.18 | En el kernel (Plug & Play) | ✅ Nativo | 3.6W | BT 5.2 | WiFi 6E + doble antena |
| [AWUS036AX](/es/products/alfa/awus036ax/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1200 Mbps | USB-A 3.2 Gen 1 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Sí | ✅ Sí | ✅ De extremo a extremo (.22000) | En el kernel ≥6.17 | En el kernel (Plug & Play) | ✅ Nativo | 3.6W | — | WiFi 6 + hotspot AP |
| [AWUS036AXER](/es/products/alfa/awus036axer/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1800 Mbps | USB-A 3.2 | Integrada (nano) | 2×2 MIMO | ✅ Sí | ✅ Sí | ✅ De extremo a extremo (.22000) | En el kernel ≥6.17 | En el kernel (Plug & Play) | ✅ Nativo | 3.0W | — | Adaptador de viaje compacto |
| [AWUS036ACH](/es/products/alfa/awus036ach/) | WiFi 5 | RTL8812AU | 2.4 + 5 GHz | 867 Mbps | USB-C 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅✅ El mejor | ✅✅ El mejor | ✅ De extremo a extremo (.22000) | En el kernel ≥6.13 | En el kernel (Plug & Play) | ✅ Nativo | 3.6W | — | Referencia en Kali Linux |
| [AWUS036ACM](/es/products/alfa/awus036acm/) | WiFi 5 | MT7612U | 2.4 + 5 GHz | 867 Mbps | USB-A 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Sí | ✅ Sí | ✅ De extremo a extremo (.22000) | En el kernel ≥4.19 | En el kernel (Plug & Play) | ✅ Nativo | 3.0W | — | Linux plug & play |
| [AWUS036ACHM](/es/products/alfa/awus036achm/) | WiFi 5 | MT7610U | 2.4 + 5 GHz | 433 Mbps | USB 2.0 | 1× RP-SMA 5dBi | 1×1 SISO | ✅ Sí | ✅ 2,4 GHz / ⚠️ 5 GHz solo difusión | ✅ De extremo a extremo (.22000) | En el kernel ≥4.19 | En el kernel (Plug & Play) | ✅ Nativo | — | — | AC600 compacto, Linux plug & play |
| [AWUS036ACS](/es/products/alfa/awus036acs/) | WiFi 5 | RTL8811AU | 2.4 + 5 GHz | 433 Mbps | USB-A 2.0 | 1× RP-SMA 2dBi | 1×1 SISO | ✅ Sí | ✅ Sí | ✅ De extremo a extremo (.22000) | En el kernel ≥6.13 | En el kernel (Plug & Play) | ✅ Nativo (5 GHz probado como 802.11a 20 MHz; VHT80 no probado) | 2.5W | — | Pruebas de seguridad con presupuesto reducido |
| [AWUS036EACS](/es/products/alfa/awus036eacs/) | WiFi 5 | RTL8821CU | 2.4 + 5 GHz | 433 Mbps | USB 2.0 nano | Integrada 2 dBi | 1×1 SISO | ✅ Sí | ✅✅ El mejor | ✅ De extremo a extremo (.22000) | En el kernel ≥6.2 | En el kernel (Plug & Play) | ✅ Nativo (5 GHz probado como 802.11a 20 MHz; VHT80 no probado) | 2.5W | BT 4.2 | WiFi doméstico en Windows + BT |

## Guía de compra rápida — por caso de uso

**🔴 Kali Linux / Pentesting** — El mejor: AWUS036ACH

RTL8812AU — el monitor mode y la packet injection más maduros en Kali; 100 % de injection en ambas bandas en el GX10 (kernel 6.17). Controlador rtw88_8812au en el kernel desde la 6.13. Consejo: en kernels más antiguos, use el controlador DKMS de aircrack-ng fijado al commit estable 63cf0b4.

**🔵 WiFi 6E (Tri-Band) para usuarios avanzados** — El mejor: AWUS036AXML or AWUS036AXM

MT7921AUN — controlador Linux en el kernel desde la 5.18, banda de 6 GHz (verificada en el AXML; AXM sin probar), Bluetooth 5.2. Nota: la packet injection falla en el kernel estándar 6.17 (regresión de mac80211 desde la 6.16), por lo que no es apto para pentesting. Formatos: el AXML tiene un conector USB-C desmontable y un cuerpo de una sola antena con dos salidas; el AXM tiene un formato USB-A en L integrado.

**🌐 Emulación de Soft-AP / Hotspot** — El mejor: AWUS036ACM

MT7612U — compatibilidad con el modo AP plug-and-play mediante el hostapd nativo del kernel de Linux. A diferencia de los adaptadores Realtek, que requieren compilaciones personalizadas de hostapd problemáticas, MediaTek funciona sin fricciones y de forma estable para simular Rogue AP / Evil Twin.

**🟢 Linux de uso diario (Plug & Play)** — El mejor: AWUS036ACM

MT7612U — en el kernel desde la versión 4.19, sin instalar controladores en Ubuntu / Debian / Fedora. La experiencia más sencilla en Linux.

**🟣 Raspberry Pi / Embebido** — El mejor: AWUS036ACM

El bajo consumo y el controlador en el kernel lo hacen ideal para Raspberry Pi. Nota: los modelos de alta potencia (ACH, AXML) consumen hasta 3.6W y requieren un hub USB alimentado para evitar caídas de tensión y reinicios de conexión en la Pi.

**🟡 Seguridad con presupuesto reducido / Principiantes** — El mejor: AWUS036ACS

RTL8811AU — opción de entrada asequible con compatibilidad con monitor mode y packet injection. Antena única, diseño compacto.

**⚡ Adaptador de viaje compacto** — El mejor: AWUS036AXER

Cuerpo nano ultradelgado de solo 10.5g. WiFi 6 (1800 Mbps), USB-A. Adecuado para viajes de negocios, orientado a Windows.

**🏠 Usuario doméstico de Windows + Bluetooth** — El mejor: AWUS036EACS

RTL8821CU — combo de modo dual WiFi 5 + Bluetooth 4.2. Formato nano. Ideal para equipos de escritorio que necesitan WiFi + BT rápidamente sin ranura PCIe.

**🍎 Compatibilidad con macOS** — El mejor: AWUS036ACH or AWUS036AXML

El ACH tiene buena compatibilidad con macOS mediante un controlador de terceros. El MT7921AUN del AXML cuenta con soporte de la comunidad en macOS. Verifique siempre la compatibilidad con su versión de macOS. Los Mac con Intel tienen mejor legado de controladores que la serie M.

## Guía de compra rápida — por plataforma / sistema operativo

| Plataforma / Sistema operativo | Primera opción | Alternativa | Notas |
|---|---|---|---|
| 🐧 Kali Linux | AWUS036ACH | AWUS036ACM | ACH = mejor monitor mode; ACM = compatibilidad de kernel más sencilla. En máquinas virtuales: configure la VM con un controlador USB 3.0 (xHCI) para evitar desconexiones. |
| 🐧 Ubuntu / Debian | AWUS036ACM | AWUS036AXML | MT7612U en el kernel desde la 4.19; MT7921AUN desde la 5.18 |
| 🐧 Raspberry Pi OS | AWUS036ACM | AWUS036ACH | Bajo consumo + controlador en el kernel; no requiere compilación manual. Se recomienda un hub USB alimentado para tarjetas de alta potencia, a fin de evitar reinicios. |
| 🪟 Windows 10 / 11 | AWUS036AX | AWUS036EACS | Rendimiento WiFi 6; el EACS añade un combo con Bluetooth |
| 🍎 macOS | AWUS036ACH | AWUS036AXML | Hay controladores de terceros disponibles; verifique la versión de macOS. Los Mac con Intel tienen controladores heredados; Apple Silicon (M1/M2/M3) solo tiene compatibilidad experimental restringida. |
| 📱 Android / NetHunter | AWUS036ACH | AWUS036ACS | RTL8812AU y RTL8811AU son compatibles con NetHunter; se requiere un adaptador OTG y compilar un kernel personalizado. |

---

Plataforma de pruebas: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia (noviembre de 2026). Los informes por adaptador están en el [blog](/es/blog/).
