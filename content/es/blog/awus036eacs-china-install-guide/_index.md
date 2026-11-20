---
title: "Guía de configuración de ALFA AWUS036EACS para China: Instalación en Windows y compatibilidad con Linux"
description: "Guía de configuración de ALFA AWUS036EACS en China. Adaptador nano WiFi 5 + Bluetooth 4.2 RTL8821CU. Controlador de Windows disponible en files.alfa.com.tw. En el kernel de Linux 6.2+ el controlador integrado rtw88_8821cu funciona al conectarlo; modo monitor e inyección probados y funcionando."
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
featureimage: "/images/blog/awus036eacs-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "¿Qué chip usa el AWUS036EACS? ¿Adite Bluetooth?"
    answer: "Usa el chip Realtek RTL8821CU, admite WiFi 5 y Bluetooth 4.2."
  - question: "¿Se recomienda el AWUS036EACS para Linux?"
    answer: "Sí. En el kernel de Linux 6.2+ (por ejemplo, Ubuntu 24.04 HWE / kernel 6.17) el controlador rtw88_8821cu está integrado en el kernel, sin compilación y listo al conectarlo. Medimos el modo monitor y la inyección de paquetes al 100 % en ambas bandas (2,4 GHz / 5 GHz) con captura WPA .22000 de extremo a extremo, y el Bluetooth también se probó con éxito."
  - question: "¿Cómo se instala el controlador del AWUS036EACS en Windows?"
    answer: "Descarga el paquete de controladores de Windows desde el sitio oficial de Alfa files.alfa.com.tw, instálalo como administrador y reinicia."
  - question: "¿Cómo activar el Bluetooth del AWUS036EACS?"
    answer: "Tras instalar el controlador se activa automáticamente; abre el interruptor de Bluetooth en la configuración de Windows para conectar dispositivos."
  - question: "Si necesito una tarjeta de investigación de seguridad inalámbrica para Linux, ¿cuál elegir?"
    answer: "El propio AWUS036EACS funciona para modo monitor e inyección de paquetes en el kernel 6.2+, con Bluetooth como extra. Si quieres más opciones, AWUS036ACM y AWUS036ACS también admiten completamente el modo monitor en Linux. Úsalo solo en redes de tu propiedad o para las que tengas autorización."
---

El AWUS036EACS es el adaptador combo nano WiFi 5 + Bluetooth 4.2 de ALFA. Es una actualización inalámbrica compacta para usuarios de Windows, y en el kernel de Linux 6.2+ el controlador integrado rtw88_8821cu lo admite al conectarlo (sin compilación). Esta guía cubre la instalación de Windows desde fuentes chinas y el uso en Linux.

{{< tldr >}}
El AWUS036EACS usa el chip RTL8821CU, una tarjeta mini WiFi 5 con Bluetooth 4.2. La instalación en Windows es sencilla; en el kernel de Linux 6.2+ el controlador rtw88_8821cu está integrado, por lo que el modo monitor y la inyección de paquetes funcionan al conectarlo, y el Bluetooth también está probado y funcionando.
{{< /tldr >}}

> **El AWUS036EACS funciona al conectarlo en el kernel de Linux 6.2+.** Los kernels 6.2 y posteriores (por ejemplo, Ubuntu 24.04 HWE / kernel 6.17) incluyen el controlador integrado rtw88_8821cu, así que no hace falta compilar nada. Medimos el modo monitor y la inyección de paquetes al 100 % en ambas bandas (2,4 GHz / 5 GHz), capturamos un handshake WPA de extremo a extremo (.22000), y el Bluetooth (BT) también está probado y funcionando (BR/EDR + BLE escanean dispositivos y coexisten con el WiFi). Úsalo solo en redes de tu propiedad o para las que tengas autorización.
>
> **Consejo práctico:** Es una tarjeta combo BT+WiFi. Tras cambiar de modo repetidamente, la recepción WiFi puede bloquearse (`ip link set up` devuelve `Operation already in progress` y `iw ... set channel` devuelve `-16 busy`). Antes de cada fase de prueba, desconecta el adaptador y vuelve a conectarlo en otro puerto USB para restablecerlo.
>
> Otros adaptadores Linux de la misma serie:
> - **[AWUS036ACM](/es/blog/awus036acm-china-install-guide/)** — Controlador en el núcleo MT7612U, modo monitor completo + VIF
> - **[AWUS036ACS](/es/blog/awus036acs-china-install-guide/)** — RTL8811AU, modo monitor económico


## Usuarios de Linux: lean esto primero

> **El AWUS036EACS funciona al conectarlo en el kernel de Linux 6.2+.** Los kernels 6.2 y posteriores (por ejemplo, Ubuntu 24.04 HWE / kernel 6.17) incluyen el controlador integrado rtw88_8821cu, así que no hace falta compilar nada. Medimos el modo monitor y la inyección de paquetes al 100 % en ambas bandas (2,4 GHz / 5 GHz), capturamos un handshake WPA de extremo a extremo (.22000), y el Bluetooth (BT) también está probado y funcionando (BR/EDR + BLE escanean dispositivos y coexisten con el WiFi). Úsalo solo en redes de tu propiedad o para las que tengas autorización.
>
> **Consejo práctico:** Es una tarjeta combo BT+WiFi. Tras cambiar de modo repetidamente, la recepción WiFi puede bloquearse (`ip link set up` devuelve `Operation already in progress` y `iw ... set channel` devuelve `-16 busy`). Antes de cada fase de prueba, desconecta el adaptador y vuelve a conectarlo en otro puerto USB para restablecerlo.
>
> Otros adaptadores Linux de la misma serie:
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

En el **kernel 6.2+**, el RTL8821CU lo controla el módulo integrado `rtw88_8821cu`, así que no hay nada que compilar: conéctalo y se reconoce. Comprueba primero tu versión de kernel con `uname -r`.

### Kali Linux

Con un kernel 6.2+, el controlador integrado `rtw88_8821cu` se carga automáticamente. Probamos el modo monitor y la inyección de paquetes al 100 % en ambas bandas (2,4 GHz / 5 GHz) y capturamos un handshake WPA de extremo a extremo (.22000). Úsalo solo en redes de tu propiedad o para las que tengas autorización.

```bash
sudo nmcli dev set wlxXXXX managed no
sudo ip link set wlxXXXX down
sudo iw dev wlxXXXX set type monitor
sudo ip link set wlxXXXX up
```

### Ubuntu / Debian / Raspberry Pi

En cuanto el kernel es 6.2 o posterior (incluidas las compilaciones ARM64 como en Raspberry Pi), el controlador integrado `rtw88_8821cu` gestiona el adaptador sin compilación. En un kernel más antiguo, actualiza al kernel HWE para obtener el controlador integrado.

### Consejo práctico (tarjeta combo BT+WiFi)

Como el EACS reúne Bluetooth y WiFi en un solo chip, cambiar de modo repetidamente puede bloquear la recepción WiFi: `ip link set up` devuelve `Operation already in progress` y `iw ... set channel` devuelve `-16 busy`. Antes de cada fase de prueba, desconecta el adaptador y vuelve a conectarlo en otro puerto USB para limpiar el estado. El Bluetooth (BR/EDR + BLE) está probado, funciona y coexiste con el WiFi.

---

## Referencia de recursos de China

| Recurso | URL | Uso para |
|----------|-----|---------|
| Controladores oficiales Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Controlador de Windows EACS |

{{< faq >}}

## Más guías de adaptadores Alfa para China

- [AWUS036ACH China Install Guide](/es/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potencia
- AWUS036EACS ← estás aquí

¿Preguntas? Deja un comentario abajo o contáctanos en [yupitek.com](https://yupitek.com/es/contact/).

## Referencias

1. [Sitio oficial de ALFA Network](https://www.alfa.com.tw/)
2. [Descarga oficial de controladores de Alfa](https://files.alfa.com.tw)
3. [Sitio oficial de Realtek](https://www.realtek.com/)
