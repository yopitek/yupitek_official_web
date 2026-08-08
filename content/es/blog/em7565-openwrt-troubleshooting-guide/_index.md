---
title: "Sierra ¿EM7565 no detectado en OpenWrt o Raspberry Pi? Guía completa de solución de problemas QMI/MBIM"
description: "¿El EM7565 no se detecta en OpenWrt o Raspberry Pi, o desapareció el puerto QMI? Esta guía lo lleva desde lsusb y dmesg a través de la composición USB, la carga de controladores y los pasos de configuración del EM7565 para resolver problemas de conexión de hardware y software."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "em7565-openwrt-troubleshooting-guide"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/es/products/sierra/em7565/"
faq:
  - question: "¿Cuál es la razón más común por la que el EM7565 no se detecta en OpenWrt?"
    answer: "La causa más común es una alimentación insuficiente (VCC fuera del rango de 3,135 a 4,4 V), por lo que lsusb no muestra nada, o un ajuste de composición USB incorrecto que deja la interfaz QMI deshabilitada."
  - question: "El EM7565 se reinicia constantemente y no arranca. ¿Está dañado?"
    answer: "No necesariamente. Tiene un mecanismo de protección SED: después de 6 reinicios anormales consecutivos entra en un estado protegido, y la recarga del firmware lo restaura."
---

¿Su EM7565 se niega a aparecer en OpenWrt o en una Raspberry Pi? Antes de reemplazar el módulo, recorra el flujo de depuración según la especificación oficial. Esta guía cubre la confirmación del enlace USB físico, la verificación de la composición USB, la carga de los controladores Linux correctos, la exclusión de la interferencia de servicios del sistema y el manejo del complicado estado SED del firmware. Siga estos cinco pasos para identificar rápidamente la causa raíz.

{{< tldr >}}
Cuando el EM7565 no se detecta, revise estas cinco cosas: 1. Confirme la capa USB con `lsusb` (inspeccione la entrega de energía y la placa adaptadora). 2. Confirme la interfaz QMI/MBIM y si existe `/dev/cdc-wdm0`; revise los controladores `qmi_wwan` / `cdc_mbim` y la composición USB. 3. Detenga `ModemManager` para descartar la interferencia de servicios del sistema. 4. Revise la secuencia de alimentación (no conduzca ninguna señal dentro de los 100 ms posteriores al encendido; el rizado debe mantenerse por debajo de 100 mVp-p). 5. Revise el estado del firmware: 6 fallos de arranque consecutivos activan la protección SED, que requiere recargar el firmware. El principio: primero el hardware, luego el software y, por último, el firmware.
{{< /tldr >}}

**El EM7565 es un módulo WWAN M.2 tipo 3042-S3-B 4G LTE-Advanced basado en el Qualcomm MDM9250. Admite tanto interfaces USB QMI como MBIM.** Cuando OpenWrt o una Raspberry Pi no lo detecta, la falla suele estar en uno de tres lugares: el USB no recibe alimentación, la composición USB está atascada en una configuración incorrecta o el controlador Linux no se cargó correctamente. Ocasionalmente, el módulo también entra en un modo de protección después de reinicios repetidos. Siguiendo el manual oficial de Sierra Wireless, hemos armado una secuencia de depuración confiable, paso a paso.

> Enlace del producto: [Serie Sierra Wireless de Yupitek](https://yupitek.com/es/products/sierra/)

## Conclusión rápida: cinco pasos cuando el EM7565 no se detecta

El error más común durante la depuración es saltar directamente a un reflasheo del firmware. **Confirme primero el hardware, luego el software, y solo toque el firmware al final.**

1. **Revise la capa USB**: ejecute `lsusb` para ver si el módulo aparece. Si no aparece, revise la entrega de energía (VCC debe ser de 3,135 a 4,4 V), la placa adaptadora y el cable USB.
2. **Revise la interfaz QMI/MBIM**: ¿`lsusb` muestra el módulo pero no hay `/dev/cdc-wdm0`? Verifique que los controladores `qmi_wwan` / `cdc_mbim` estén cargados y si la composición USB solo expone el modo de diagnóstico.
3. **Revise los servicios del sistema**: el `ModemManager` del sistema puede estar reteniendo el módulo.
4. **Revise la secuencia de alimentación**: no conduzca ninguna señal durante al menos 100 ms después del encendido y mantenga el rizado de alimentación por debajo de 100 mVp-p. El voltaje inestable hace que el enlace USB se caiga y se reconecte repetidamente.
5. **Revise el estado del firmware**: si el módulo se reinicia 6 veces seguidas tras fallos de arranque, entra en el estado de protección SED (Smart Error Detection) y debe recargar el firmware.

## Entender el EM7565: ¿qué tipo de módulo es?

Antes de depurar, aquí hay un resumen rápido del EM7565. Es un módulo M.2 que requiere tres antenas externas (principal, GNSS y auxiliar). Las antenas no están incluidas.

| Elemento | Especificación oficial (Doc# 41110788, Rev 8) |
|---|---|
| **Chipset** | Qualcomm MDM9250 |
| **Factor de forma** | M.2 (3042-S3-B) / 42 × 30 mm, hasta 1,50 mm de grosor, 6,5 g |
| **Pico de descarga** | Cat 12 (3CA, 256QAM) hasta 600 Mbps |
| **Pico de subida** | Cat 13 (2CA, 64QAM) hasta 150 Mbps |
| **Bandas LTE** | B1/2/3/4/5/7/8/9/12/13/18/19/20/26/28/29/30/32/41/46/66 (nota: B42/B43/B48 deshabilitadas en espera de aprobación regulatoria) |
| **Interfaces de host** | USB 2.0 y USB 3.0; comandos QMI / MBIM / AT |
| **Voltaje de alimentación** | VCC 3,135 V (mín.) / 3,3 V (típ.) / 4,4 V (máx.), rizado ≤ 100 mVp-p |
| **Temperatura de operación** | Mantenga la temperatura interna por debajo de 90 °C (idealmente por debajo de 80 °C) |

## Paso 1: Comience en la capa USB

¿El host realmente ve el hardware?

```bash
lsusb
```

Si aparece un dispositivo de Sierra Wireless que comienza con 1199, el enlace de hardware está establecido. Si no aparece nada:

- Revise la fuente de alimentación: la corriente de irrupción del EM7565 al arrancar puede alcanzar de 2,2 A a 2,5 A (corriente máxima de operación 1,5 A). Muchas carcasas adaptadoras USB de Raspberry Pi no pueden suministrar esa corriente.
- Dele tiempo: espere 10 segundos después de conectarlo para que la enumeración USB se complete.

Luego inspeccione el registro del kernel:

```bash
dmesg | tail -50
```

Si ve que `qmi_wwan` crea `/dev/cdc-wdm0`, el módulo está listo para conectarse.

## Paso 2: Revise la composición USB

Si `lsusb` muestra el módulo pero `/dev/cdc-wdm0` nunca aparece, es posible que el módulo tenga los canales QMI/MBIM deshabilitados. Un ajuste llamado composición USB dentro del módulo decide qué canales expone.

Consúltelo con el comando `AT!USBCOMP?`. Un cambio descuidado puede eliminar todos los canales, así que registre los parámetros originales antes de cambiar nada y consulte el manual oficial de comandos AT (Doc# 41111748).

## Paso 3: Descarte la interferencia de ModemManager

En Linux de escritorio o en una Raspberry Pi, un servicio integrado llamado `ModemManager` tiende a capturar el módulo 4G. Una vez que toma el control, sus propios comandos `qmicli` se detienen.

Mientras depura manualmente, deténgalo primero:

```bash
sudo systemctl stop ModemManager
```

Una vez que confirme que el módulo está sano, decida si marca manualmente o devuelve el control a ModemManager.

## Paso 4: ¿Está bloqueado el firmware? (Protección SED)

Si el módulo se reinicia sin cesar después del encendido, es posible que haya entrado en el estado **SED (Smart Error Detection)**.

La especificación oficial es explícita: si ocurren 6 reinicios poco después del arranque, el módulo se estaciona en el bootloader y espera una recarga de firmware. Esto suele deberse a una fuente de alimentación inestable con caídas de voltaje severas.

No asuma que el módulo está muerto. Cambie a una mejor fuente de alimentación y vuelva a flashear el firmware con la herramienta oficial para recuperarlo.

## Cómo marcar con QMI (ejemplo en OpenWrt)

Una vez que haya resuelto los problemas anteriores y aparezca `/dev/cdc-wdm0`, marcar en OpenWrt es sencillo.

1. Instale los paquetes requeridos:

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option
```

2. Configure su APN en `/etc/config/network` (use los valores de su operador):

```text
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

3. Reinicie la red:

```bash
/etc/init.d/network restart
```

Aparece la interfaz `wwan0` y usted está en línea.

## Resumen

Un EM7565 ausente en OpenWrt o en una Raspberry Pi es como reparar una computadora: acierte con el orden y será rápido.

1. **Hardware**: ¿`lsusb` está limpio y el voltaje es estable?
2. **Interfaz**: ¿la composición USB es correcta?
3. **Software**: ¿los controladores están instalados y ModemManager compite por el dispositivo?
4. **Firmware**: ¿demasiados reinicios bloquearon el módulo?

Mientras no vuelva a flashear el firmware a ciegas, la mayoría de los problemas se pueden diagnosticar en diez minutos.

## Información de compra (llamada a la acción)

¿No está seguro de si su placa adaptadora o sus antenas funcionan con el EM7565? Yupitek ofrece la línea completa de productos Sierra Wireless y soluciones integrales de integración de hardware.

Escríbanos por correo: **sales@yupitek.com**

Vea el producto: [Página del producto EM7565](https://yupitek.com/es/products/sierra/em7565/)
