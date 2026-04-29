---
title: "Guía de configuración de ALFA AWUS036EACS para China: Instalación en Windows y compatibilidad con Linux"
description: "Guía de configuración de ALFA AWUS036EACS en China. Adaptador nano WiFi 5 + Bluetooth 4.2 RTL8821CU. Controlador de Windows disponible en files.alfa.com.tw. Linux y Kali Linux no son compatibles; consulte las alternativas recomendadas."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036eacs-china-install-guide"
tags: ["alfa", "awus036eacs", "windows", "driver", "china", "bluetooth", "rtl8821cu"]
categories: ["Guías de Controladores"]
series: ["alfa-china-install-guide"]
related_product: "/es/products/alfa/awus036eacs/"
series_order: 8
---

El AWUS036EACS es el adaptador combo nano WiFi 5 + Bluetooth 4.2 de ALFA. Está diseñado para usuarios de Windows que necesitan una actualización inalámbrica compacta. Su chipset RTL8821CU no tiene un controlador de Linux de código abierto confiable: el modo monitor y la inyección de paquetes no son compatibles. Esta guía cubre la instalación de Windows desde fuentes chinas y explica claramente las limitaciones de Linux.

## Usuarios de Linux: lean esto primero

> **El AWUS036EACS no funciona de forma confiable en Kali Linux, Ubuntu, Debian o Raspberry Pi.** El chipset RTL8821CU no tiene un controlador de código abierto mantenido. El modo monitor, la inyección de paquetes y VIF no están disponibles.
>
> Si necesita un adaptador compatible con Linux para investigación de seguridad, use uno de estos en su lugar:
> - **[AWUS036ACM](/es/blog/awus036acm-china-install-guide/)** — Controlador en el núcleo MT7612U, modo monitor completo + VIF
> - **[AWUS036ACS](/es/blog/awus036acs-china-install-guide/)** — RTL8811AU, modo monitor económico

---

## Configuración de Windows 10 / 11

### Paso 1: Descargar el controlador de Alfa

El servidor oficial de controladores de Alfa es accesible desde China:

https://files.alfa.com.tw

Navegue a la carpeta del producto **AWUS036EACS** y descargue el paquete del controlador de Windows (`.zip` o `.exe`).

### Paso 2: Instalar el controlador

1. Extraiga el archivo zip descargado.
2. Haga clic derecho en el instalador `.exe` y seleccione **Ejecutar como administrador**.
3. Siga las instrucciones en pantalla.
4. Reinicie cuando se le solicite.

---

## Detalles de compatibilidad con Linux

### Kali Linux

El RTL8821CU no tiene un controlador DKMS mantenido para los núcleos modernos de Kali. Existen controladores mantenidos por la comunidad, pero son inestables.

**Recomendación:** Use el [AWUS036ACM](/es/blog/awus036acm-china-install-guide/) para trabajos de seguridad en Kali Linux.

---

## Referencia de recursos de China

| Recurso | URL | Uso para |
|----------|-----|---------|
| Controladores oficiales Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Controlador de Windows EACS |

## Más guías de adaptadores Alfa para China

- [AWUS036ACH China Install Guide](/es/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potencia
- AWUS036EACS ← estás aquí

¿Preguntas? Deja un comentario abajo o contáctanos en [yupitek.com](https://yupitek.com/es/contact/).
