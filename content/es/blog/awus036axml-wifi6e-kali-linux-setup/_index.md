---
title: "Guía de instalación de ALFA AWUS036AXML: Pruebas de monitorización e inyección de paquetes en Kali Linux con una tarjeta Wi-Fi 6E"
locale: es
hreflang_group: awus036axml-wifi6e-kali-linux-setup
slug: awus036axml-wifi6e-kali-linux-setup
published: 2026-08-10
author: yupitek
category: technical
tags:
  - AWUS036AXML
  - Kali Linux
hero_image: /static/img/AWUS036AXML/hero.webp
hero_alt: "¿Cómo instalar AWUS036AXML en Kali Linux? Guía de monitorización Wi-Fi 6E e inyección de paquetes | Yupitek"
seo_description: "Guía de instalación de ALFA AWUS036AXML (chipset MT7921AUN) en Kali Linux: driver mt7921u integrado, requisitos del kernel, monitorización, inyección de paquetes y resolución de problemas comunes."
---

# Guía de instalación de ALFA AWUS036AXML: Pruebas de monitorización e inyección de paquetes en Kali Linux con una tarjeta Wi-Fi 6E

> TL;DR: La ALFA AWUS036AXML está equipada con el chipset MediaTek MT7921AUN y funciona en Kali Linux (kernel 5.18+) utilizando el **driver `mt7921u` integrado**, sin necesidad de compilar drivers adicionales. Para un modo de monitorización activa (active monitor mode) e inyección de paquetes estables, se recomienda un kernel 6.12+ y un Hub USB con alimentación. Tras conectarlo, `lsusb` debería mostrar `0e8d:7961`, y a continuación puede cambiar al modo de monitorización con `airmon-ng` o `iw`.

## ¿Por qué las tarjetas Wi-Fi 6E están ganando atención en las pruebas de penetración?

El nuevo **banda de 6 GHz** (5925–7125 MHz) añadido por Wi-Fi 6E es un punto focal en la actualización de redes inalámbricas empresariales en los últimos años: las nuevas generaciones de AP, las salas de conferencias de alta densidad y el IoT industrial están comenzando a desplegar 6 GHz. Para los auditores de ciberseguridad, si el entorno auditado ya ha implementado 6 GHz, su tarjeta de prueba **debe poder escuchar esta banda**; de lo contrario, el alcance de la auditoría perdería una parte significativa.

La AWUS036AXML es la tarjeta USB Wi-Fi 6E lanzada por ALFA Network, que soporta las bandas de 2.4 / 5 / 6 GHz. En comparación con la popular generación anterior AWUS036ACH (RTL8812AU, solo 2.4/5 GHz), la mayor diferencia es la capacidad de monitorización en 6 GHz. Si ya está familiarizado con el proceso de la AWUS036ACH, los pasos de esta guía le resultarán muy familiares.

## Especificaciones de la AWUS036AXML y requisitos de versión

| Elemento | AWUS036AXML | AWUS036ACH (Referencia) | AWUS036ACM (Referencia) |
|---|---|---|---|
| Chipset | MediaTek MT7921AUN | Realtek RTL8812AU | MediaTek MT7612U |
| Bandas | 2.4 / 5 / 6 GHz (Wi-Fi 6E) | 2.4 / 5 GHz | 2.4 / 5 GHz |
| Driver Linux | `mt7921u` (**Integrado en el kernel**) | `88XXau` (Requiere compilación manual/DKMS) | `mt76` (Integrado en el kernel) |
| Kernel recomendado | ≥ 5.18 (Soporte 6 GHz) | 5.x (Versiones anteriores también válidas) | 5.x |
| Modo de monitorización activa | Kernel ≥ 6.12 recomendado | Estándar | Estándar |
| ID USB (lsusb) | `0e8d:7961` | `0bda:8812` | `0e8d:7612` |
| Consumo | Aprox. 2.7 W (Se recomienda Hub con alimentación) | Menor | Menor |
| Inyección de paquetes | Soportada (Se recomienda prueba real) | Soportada | Soportada |

> Nota sobre los requisitos de versión: `mt7921u` se incorporó al kernel principal desde la versión 5.18, y el soporte para la banda de 6 GHz se completó gradualmente con el kernel. Se **recomienda el kernel 6.12+ para el modo de monitorización activa (active monitor mode)**. Kali 2026 viene con un kernel de nivel 6.14 de forma predeterminada, cumpliendo así directamente con los requisitos.

## Preparativos previos

1. **Kali Linux 2024.x o superior** (se recomienda actualizar a la última versión: `sudo apt update && sudo apt full-upgrade -y`).
2. Verifique la versión del kernel: `uname -r`. Si es inferior a 5.18, actualice el sistema primero.
3. Un puerto USB 3.0 disponible; si se conecta a una Raspberry Pi o a un Hub USB, **se recomienda usar un Hub con alimentación** (el consumo de la AWUS036AXML es de aprox. 2.7 W; la falta de alimentación puede provocar que el sistema no la detecte).
4. Permisos de prueba legales: Todos los comandos de esta guía están destinados únicamente a entornos de red de su propiedad o para los que tenga autorización.

## Paso 1: Conectar la tarjeta y confirmar que el sistema la detecta

Después de insertar la tarjeta, utilice `lsusb` para confirmar si el dispositivo ha sido reconocido:

```bash
lsusb
```

En la salida esperada debería aparecer:

```text
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

`0e8d:7961` es el ID USB del MT7921AUN. Si no aparece, verifique primero la alimentación (cambie de puerto USB o añada un Hub con alimentación) e intente de nuevo.

Confirme que el driver se ha cargado:

```bash
lsmod | grep mt7921
dmesg | grep -i mt7921 | tail -20
```

El kernel predeterminado de Kali 2026 incluye `mt7921u`; en condiciones normales, se carga al conectarlo, **sin necesidad de descargar o compilar ningún driver** —esta es la mayor diferencia con la AWUS036ACH (RTL8812AU, que requiere la instalación manual de `88XXau`).

## Paso 2: Confirmar la interfaz inalámbrica

```bash
ip link show
# O bien
iwconfig
```

Debería ver una nueva interfaz inalámbrica, generalmente `wlan0` o `wlan1` (dependiendo del número de interfaces existentes en el sistema). El siguiente ejemplo utiliza `wlan1`; sustitúyalo por el nombre real si es necesario.

## Paso 3: Activar el modo de monitorización

### Método 1: airmon-ng (Recomendado)

```bash
# Detener servicios que puedan interferir
sudo airmon-ng check kill

# Activar el modo de monitorización (cambie wlan1 por el nombre de su interfaz)
sudo airmon-ng start wlan1
```

Tras el éxito, aparecerá la interfaz virtual `wlan1mon`.

### Método 2: iw (Control preciso)

```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

Este método modifica la interfaz existente directamente y no crea `wlan1mon`.

## Paso 4: Confirmar que el modo de monitorización está activo

```bash
iwconfig
```

El campo clave debe ser `Mode:Monitor`:

```text
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.412 GHz  Tx-Power=30 dBm
          Power Management:off
```

También puede confirmar `type monitor` con `iw dev`. A continuación, realice una prueba de extremo a extremo con `airodump-ng`:

```bash
sudo airodump-ng wlan1mon
```

Si puede ver la lista de BSSID circundantes (incluyendo canales, intensidad de señal y tipo de cifrado), el modo de monitorización funciona correctamente. **Escanear la banda de 6 GHz**:

```bash
sudo airodump-ng --band 6g wlan1mon
```

> Nota: El escaneo de 6 GHz requiere que su driver/kernel de la tarjeta soporte dicha banda (el kernel 6.12+ es más estable); si `--band 6g` no es compatible, escanee primero la banda de 5 GHz (`--band a`) para confirmar el funcionamiento básico y vuelva a intentarlo tras actualizar el kernel.

## Paso 5: Prueba de inyección de paquetes

```bash
sudo aireplay-ng --test wlan1mon
```

La línea clave de la salida esperada es:

```text
Injection is working!
```

Una tasa de éxito superior al 80 % indica un funcionamiento fiable; si es inferior al 50 %, verifique la orientación de la antena, la alimentación USB o utilice un puerto USB 3.0 conectado directamente.

## Nota adicional para Raspberry Pi: Plataforma portátil de auditoría Wi-Fi

La AWUS036AXML también es compatible con Raspberry Pi 3B+ / 4 / 5 (listada en la página oficial del producto), lo que la hace adecuada para formar un kit de herramientas de auditoría portátil. Puntos clave a tener en cuenta:

- **Alimentación**: La alimentación USB de la Pi es limitada; se recomienda usar un Hub USB con alimentación para evitar que la tarjeta no se detecte intermitentemente.
- **Sistema**: La imagen oficial de Kali ARM64 (para Raspberry Pi) es suficiente; tras la instalación, el driver `mt7921u` sigue siendo interno.
- **Verificación**: Si `lsusb` muestra `0e8d:7961` y `lsmod | grep mt7921` produce salida, la plataforma está lista.

## Resolución de problemas comunes

**P: ¿Qué hago si `lsusb` no muestra `0e8d:7961`?**
En el 99 % de los casos se debe a falta de alimentación o a una conexión floja. Cambie a un puerto USB 3.0 conectado directamente; si usa un Hub, cambie a uno con alimentación; si persiste el problema, pruebe con un cable USB más corto.

**P: ¿La interfaz vuelve automáticamente a "managed" tras activar el modo de monitorización?**
Normalmente es porque NetworkManager / wpa_supplicant recupera el control en segundo plano. Vuelva a ejecutar `sudo airmon-ng check kill` o detenga manualmente `sudo systemctl stop NetworkManager wpa_supplicant`.

**P: `iwconfig` muestra `Mode:Managed` o la interfaz desaparece?**
Es posible que el driver no se haya cargado correctamente o que el kernel sea demasiado antiguo. Primero confirme el módulo con `lsmod | grep mt7921` y verifique que el kernel sea ≥ 5.18 con `uname -r`.

**P: ¿No se detectan redes en 6 GHz?**
Confirme primero las bandas soportadas con `iw dev wlan1mon info`; los entornos de 6 GHz son menos comunes (nuevos despliegues) y el progreso de apertura de la banda de 6 GHz en Taiwán debe seguirse según los anuncios de la NCC. También puede verificar primero el funcionamiento de la tarjeta en 2.4/5 GHz.

**P: Comparada con la AWUS036ACH, ¿cuál debería comprar?**
Si el entorno auditado ya tiene 6 GHz → elija la AWUS036AXML; si solo necesita 2.4/5 GHz y la prioridad es el presupuesto → la AWUS036ACH sigue siendo una opción muy madura. Ambas son tarjetas de auditoría maduras en Kali; la diferencia radica en la cobertura de bandas y en la instalación del driver (AXML es interno y no requiere compilación).

## Preguntas frecuentes (FAQ)

**P1: ¿Requiere la AWUS036AXML instalar drivers adicionales en Kali Linux?**
No. Utiliza el driver `mt7921u` integrado en el kernel (kernel 5.18+); se conecta y funciona de inmediato; no es necesario compilar un driver DKMS como en el caso de la AWUS036ACH.

**P2: ¿La AWUS036AXML soporta el modo de monitorización?**
Sí. Puede activarlo con `airmon-ng` o `iw`; para realizar un modo de monitorización activa (como pruebas relacionadas con deauth), se recomienda el kernel 6.12+.

**P3: ¿Se puede utilizar la banda de 6 GHz de Wi-Fi 6E para auditorías en Taiwán?**
La banda de 6 GHz está regulada; antes de usarla, confirme el progreso de apertura y las normas de licencia de la NCC para la banda de 6 GHz, y realice pruebas únicamente en entornos para los que tenga autorización.

**P4: ¿Qué hago si no detecta la tarjeta al conectarla a una Raspberry Pi?**
Verifique primero la alimentación: el consumo de la AWUS036AXML es de aprox. 2.7 W; se recomienda usar un Hub USB con alimentación y un cable USB de buena calidad.

**P5: ¿En qué se diferencia la AWUS036AXML de la AWUS036ACH?**
La AXML es Wi-Fi 6E (incluye 6 GHz) y su driver está integrado en el kernel; la ACH es de doble banda (2.4/5 GHz) y el RTL8812AU requiere la instalación manual del driver. Ambas son tarjetas de auditoría maduras en Kali.

## Conclusión

El proceso de instalación de la AWUS036AXML es más sencillo de lo que imagina: **kernel 5.18+ → conectar y usar (driver `mt7921u`) → confirmar `0e8d:7961` → cambiar a monitorización con airmon-ng → validar la inyección con aireplay-ng**. La diferencia fundamental con la AWUS036ACH radica en la banda de 6 GHz y en el driver que no requiere compilación; si su alcance de auditoría ya ha entrado en la era Wi-Fi 6E, esta tarjeta es la opción para completar la cobertura de bandas. Recuerde realizar todas las pruebas únicamente en entornos con autorización legal.

La serie de tarjetas de ALFA Network se comercializa y cuenta con soporte técnico en Taiwán a través de Yupitek (Yuhé Technology); si necesita la AWUS036AXML o los Hubs de alimentación y antenas compatibles, no dude en escribir a [sales@yupitek.com](mailto:sales@yupitek.com).