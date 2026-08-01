---
title: "Guía completa de instalación de módulos Sierra 4G/5G en Ubuntu / Debian / Linux Mint: configuración de EM7455, EM7565, EM919x y MC7455 con posicionamiento GNSS | Yupitek"
description: "¿Cómo instalar módulos Sierra 4G/5G en Ubuntu/Debian/Linux Mint? Esta guía le enseña a instalar ModemManager, a usar qmicli/mbimcli para la conexión y a configurar el posicionamiento GNSS. Cubre EM7455, EM7565, EM919x y MC7455."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "ubuntu-debian-sierra-4g-5g-setup-guide"
tags: ["Sierra Wireless", "Ubuntu", "Debian", "Linux", "GNSS"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/es/products/sierra/"
faq:
  - question: "¿Puedo usar los módulos Sierra 4G/5G directamente en Ubuntu para conectarme a internet?"
    answer: "Sí. Basta con instalar los paquetes modemmanager y libqmi-utils, entre otros, y rellenar el APN en NetworkManager para conectarse."
  - question: "¿Cómo activo el posicionamiento GNSS de los módulos Sierra en Linux?"
    answer: "Use los comandos de ModemManager: primero mmcli -m 0 --location-enable-gps-raw y luego --location-get para obtener las coordenadas. Asegúrese de que la antena GNSS esté bien conectada."
---

¿Quiere instalar los módulos de Sierra Wireless (EM7455, EM7565, MC7455 o EM919x) en Ubuntu, Debian o Linux Mint? En realidad, Linux es compatible de forma nativa con estos dispositivos; solo necesita saber qué paquetes instalar (como ModemManager y libqmi-utils). Este artículo le guía paso a paso: desde cómo conectar el hardware, instalar los controladores y conectarse a internet, hasta cómo activar el posicionamiento GNSS. Ya sea que trabaje con drones o con ordenadores industriales, siga la guía y no se equivocará.

{{< tldr >}}
Linux es compatible de forma nativa con los módulos de Sierra Wireless (EM7455, EM7565, MC7455 o EM919x); solo necesita instalar los paquetes correctos como ModemManager y libqmi-utils. La guía cubre la conexión del hardware, la instalación de controladores, la conexión a internet y la activación del posicionamiento GNSS. Tanto para drones como para ordenadores industriales, seguirla correctamente garantiza el resultado.
{{< /tldr >}}

**Resumen en una frase: instalar estos módulos Sierra en Linux es muy sencillo. Basta con instalar `modemmanager` y las herramientas relacionadas mediante `apt`, y podrá conectarse a internet con NetworkManager, ¡incluso leer el posicionamiento GPS con facilidad!**

Muchas personas reciben una EM7455, EM7565, EM919x o MC7455, la insertan en la placa y no saben cómo configurarla para navegar. En realidad, el soporte de estos módulos en Linux es muy maduro. Todos se comunican por USB mediante los protocolos QMI o MBIM. A continuación le acompañamos paso a paso en su configuración.

> Las cifras y las bases técnicas provienen de las especificaciones oficiales de Sierra Wireless. Artículo elaborado por Yupitek.

---

## Antes de empezar: entienda el hardware que tiene

Si el hardware no es correcto, de nada servirán los comandos de software.

| Módulo | Ranura de montaje | Categoría de velocidad | Protocolo principal en Linux | Número de antenas |
|---|---|---|---|---|
| **EM7455** | M.2 (42 mm de largo) | Cat 6 (300/50 Mbps) | QMI | 3 (Main, GNSS, Aux) |
| **EM7565** | M.2 (42 mm de largo) | Cat 12 (600/150 Mbps) | QMI / MBIM | 3 (Main, GNSS, Aux) |
| **EM919x** (5G) | M.2 (largo de **52 mm**) | 5G NR / LTE Cat 20 | Conjuntos de banda ancha como MBPW | 4 o más |
| **MC7455** | mPCIe (ranura de modelo antiguo) | Cat 6 (300/50 Mbps) | QMI | 3 conectores U.FL |

**Dos puntos clave para evitar errores de hardware:**
1. **La EM919x es más larga**: mide 52 mm; no intente insertarla a la fuerza en una abertura de 42 mm o dañará la placa.
2. **Sin antena no hay señal**: conecte al menos la antena principal (Main). Si además quiere usar el posicionamiento, debe comprar una antena GPS y conectarla al puerto **GNSS**.

---

## Paso 1: instale las herramientas esenciales de Linux

En Ubuntu / Debian / Linux Mint no necesita escribir código ni compilar controladores; los repositorios de paquetes ya lo tienen todo preparado.

Abra la terminal y ejecute estas dos líneas:
```bash
sudo apt update
sudo apt install modemmanager libqmi-utils libmbim-utils
```
Tras la instalación, confirme que el servicio está en marcha:
```bash
systemctl status ModemManager
```
Con estas herramientas, su Linux podrá comprender esta tarjeta 4G/5G.

---

## Paso 2: confirme que el sistema detecta la tarjeta

Inserte la tarjeta y, tras el arranque, use estos tres comandos para comprobarlo:

1. **Compruebe el hardware USB:**
   ```bash
   lsusb
   ```
   (Debería ver un dispositivo relacionado con Sierra o Qualcomm)

2. **Compruebe el controlador del kernel:**
   ```bash
   dmesg | grep -iE 'qmi|mbim|cdc|wwan'
   ```
   (Si ve `cdc-wdm0` y `wwan0`, la carga se ha realizado correctamente)

3. **Compruebe el estado de ModemManager:**
   ```bash
   mmcli -L
   ```
   (Se mostrará una lista con nombres y números de módems; anote ese número, que normalmente es `0`)

---

## Paso 3: conexión muy sencilla (con NetworkManager)

Si usa la versión de escritorio de Ubuntu o Mint, la herramienta de gestión de red integrada es la opción más cómoda.

```bash
# Añada una conexión nueva (sustituya "internet" por el APN de su operador)
nmcli connection add type gsm ifname cdc-wdm0 con-name "mobile" apn "internet"

# ¡Actívala!
nmcli connection up mobile
```
¡Así de simple! Puede usar `ip addr show` para ver si `wwan0` ha obtenido una dirección IP.

### (Avanzado) Conexión por texto en entornos sin interfaz gráfica
En servidores sin pantalla (headless) o en placas embebidas, puede usar `qmicli` directamente:
```bash
sudo ip link set wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn=internet,ip-type=ipv4" --client-no-release-cid
sudo dhclient -v wwan0
```

---

## Paso 4: ¡active el posicionamiento GPS!

Estos módulos incorporan un potente sistema de posicionamiento GNSS integrado (compatible con GPS, GLONASS, etc.).
Según la especificación oficial:
- EM7455 / EM7565 / MC7455: arranque en caliente en 1 segundo, arranque en frío en 32 segundos. La precisión horizontal es de aproximadamente 2 a 5 metros.
- EM919x (5G): arranque en frío más rápido (≤28 segundos) y precisión ligeramente superior (<4 m al 95 %).

**La forma más rápida de obtener coordenadas en Linux:**

1. Active la función GPS:
```bash
mmcli -m 0 --location-enable-gps-raw
```
2. Obtenga las coordenadas actuales:
```bash
mmcli -m 0 --location-get
```
¡La pantalla mostrará la latitud y la longitud actuales! Si desea transmitirlas en tiempo real a otras aplicaciones, puede combinarlo con `gpsd`.

---

## Problemas comunes y primeros auxilios

1. **`mmcli -L` no muestra nada**: puede que `ModemManager` se haya detenido, o que la alimentación USB de su equipo no sea suficiente para la tarjeta.
2. **El posicionamiento GPS falla continuamente**: ¿ha conectado la antena GPS al puerto Main o Aux? ¡GNSS tiene su propio conector dedicado!
3. **La velocidad de la EM919x no despega**: es una tarjeta 5G que admite USB 3.1 Gen 2 e incluso PCIe Gen 3. Si la conecta a un puerto USB 2.0, el fabricante no garantiza el rendimiento.

## Conclusión

Trabajar con módulos Sierra en Linux no es tan difícil como podría imaginar. Compruebe la ranura del hardware y la antena, instale los paquetes de la familia `modemmanager` y ajuste el APN para navegar sin problemas. Este flujo es ideal para ingenieros que trabajan en computación perimetral (Edge Computing) o Internet de las Cosas industrial (IIoT).

## Información de compra (Llamada a la acción)

¿Quiere integrar módulos Sierra en su dispositivo Ubuntu? Yupitek ofrece soluciones completas de módulos, antenas y placas adaptadoras, además de soporte técnico de primera línea.
Escríbanos: **sales@yupitek.com**
Vea los productos: [Serie Sierra Wireless](https://yupitek.com/es/products/sierra/)

{{< faq >}}
