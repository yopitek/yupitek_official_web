---
title: "ALFA AWUS036ACH × Raspberry Pi: Kit completo de detección de Remote ID para drones (2026)"
description: "Con ALFA AWUS036ACH y Raspberry Pi, construya un kit legal de detección pasiva de Remote ID para drones. Incluye análisis del estándar ASTM F3411, lista de hardware, configuración paso a paso y aclaración técnica sobre DJI OcuSync."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["Remote-ID", "ALFA-Network", "AWUS036ACH", "detección-drones", "Counter-UAV", "ASTM-F3411", "EN-4709-002", "opendroneid", "unix_rid_capture", "DJI-OcuSync", "Raspberry-Pi"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "¿Por qué la AWUS036ACH es la opción preferida en lugar de tarjetas WiFi 6/6E más nuevas?"
    answer: "La captura de Remote ID requiere un modo monitor estable e inyección de paquetes raw. Actualmente, el controlador más maduro en la comunidad es la rama Realtek rtl88xxau (RTL8812AU / RTL8814AU). Las tarjetas WiFi 6/6E (MediaTek MT7921AUN, Realtek RTL8832BU) aún no tienen controladores de inyección en las principales herramientas de monitoreo, por lo que se omiten. La AWUS036ACH es una opción doblemente validada por la comunidad y este kit."
  - question: "¿Es necesario el nRF52840?"
    answer: "Si solo necesita Remote ID por WiFi (NAN / Beacon), no; la AWUS036ACH es suficiente. Si desea capturar también transmisiones Bluetooth 5 Long Range, necesitará el nRF52840 (con firmware sniffer). Se recomienda incluir este módulo para una cobertura completa."
  - question: "¿Puede este kit decodificar drones DJI?"
    answer: "Puede procesar las transmisiones estándar WiFi/BT Remote ID de DJI. Sin embargo, el DroneID privado de DJI OcuSync no está dentro del protocolo estándar; la tarjeta ALFA no puede decodificarlo. Se necesita un SDR (ANTSDR / HackRF) con un plugin de Kismet. Ambos sistemas se pueden desplegar en paralelo."
  - question: "¿Qué generación de Raspberry Pi se recomienda?"
    answer: "Raspberry Pi 4 (2 GB+) es la más equilibrada. Pi 3B ha sido verificada por el autor de unix_rid_capture en sus pruebas. Pi 5 también funciona (preste atención a la refrigeración y la alimentación). El WiFi integrado de la Pi no puede entrar de forma estable en modo monitor, por lo que es obligatorio usar la AWUS036ACH externa."
  - question: "¿Es legal la recepción pasiva?"
    answer: "Recibir las transmisiones públicas de Remote ID de drones es legal, equivalente a leer información pública. Sin embargo, la interferencia activa (jamming) está estrictamente regulada y no forma parte de este kit."
---
> Equipo técnico de Yupitek | Distribuidor autorizado de ALFA Network en Taiwán

{{< tldr >}}
El kit de detección de Remote ID utiliza el modo monitor de la tarjeta **ALFA AWUS036ACH** para recibir pasivamente la información de identidad y posición que los drones deben transmitir por ley (el equivalente a una «matrícula aérea»), ofreciendo a los gestores de seguridad una herramienta legal y de bajo coste para la conciencia situacional.
{{< /tldr >}}

---

## 1. Por qué necesita un kit de detección de Remote ID

La regulación mundial de drones ha entrado en la era de la «identificación por transmisión». Según los estándares, los drones deben transmitir continuamente su información en el aire:

| Campo transmitido | Descripción |
|---|---|
| ID del UAS / operador | Número de serie o código de registro |
| Posición en tiempo real (latitud, longitud, altitud) | WGS-84 / altitud barométrica |
| Velocidad, rumbo | Velocidad horizontal / vertical |
| Posición del operador | Punto de despegue o posición en tiempo real |

La transmisión se realiza a través de dos tipos de portadoras inalámbricas:

- **Bluetooth**: BT4 Legacy Advertising, BT5 Long Range (Extended Advertising)
- **WiFi**: NAN (Wi-Fi Aware, 2.4 / 5 GHz), Beacon (2.4 / 5 GHz)

Para los gestores de aeropuertos, parques industriales, prisiones, grandes eventos, etc., **recibir pasivamente estas transmisiones públicas** (equivalentes a ver la «matrícula de cola» del dron) es un medio legal y de bajo coste para la conciencia situacional, sin necesidad de interferencias activas.

{{< alert "triangle-exclamation" >}}
**Nota legal**: Todos los métodos de este artículo son de **recepción pasiva de transmisiones públicas**. La interferencia activa (jamming) está estrictamente regulada y no forma parte de este kit, ni se recomienda su uso.
{{< /alert >}}

---

## 2. Posicionamiento del producto: la ruta open source de menor riesgo técnico

Tras evaluar múltiples rutas técnicas, seleccionamos la combinación basada en **ALFA AWUS036ACH**:

- La ALFA AWUS036ACH utiliza el chip **Realtek RTL8812AU**, doble banda 2.4 + 5 GHz (802.11ac), 2×2 MIMO, dos antenas desmontables de 5 dBi de alta ganancia (RP-SMA), con ancho de banda USB 3.0 suficiente.
- El controlador `rtl88xxau` mantenido por la comunidad le permite entrar de forma estable en **modo monitor** y soportar **inyección de paquetes raw** — requisito previo para capturar tramas Wi-Fi RID Beacon / NAN.
- Lo más importante: el README de `sxjack/unix_rid_capture` indica explícitamente **«Probado con un dongle WiFi basado en rtl8812au, un dongle nRF52840 y una Raspberry Pi 3B»** , lo que equivale a que la comunidad ya ha validado el hardware. Replicar su arquitectura para hacer un producto supone el menor riesgo técnico.

---

## 3. Lista de hardware

| Componente | Modelo / Especificación | Función | Necesidad |
|---|---|---|---|
| **Tarjeta principal** | ALFA **AWUS036ACH** (RTL8812AU, doble banda 2.4/5 GHz, USB 3.0, doble antena 5 dBi RP-SMA) | Captura WiFi Remote ID (modo monitor) | **Obligatorio** |
| Ordenador de placa simple | Raspberry Pi 4 (2 GB+ recomendado; 3B / 5 también válido) | Ordenador principal | **Obligatorio** |
| Almacenamiento | microSD 16 GB+ (Samsung / SanDisk Endurance recomendado) | Disco del sistema | **Obligatorio** |
| Captura Bluetooth 5 | **nRF52840** USB Dongle (con firmware sniffer, ej. Nordic Sniffer) | Captura BT5 Long Range Remote ID | Recomendado (opcional) |
| Fuente de alimentación | 5 V / 3 A USB-C (Fuente oficial Pi) | Alimentación | **Obligatorio** |
| Red | Cable Ethernet o credenciales WiFi | Carga / gestión | **Obligatorio** |
| Antena mejorada | ALFA **APA-M25** antena direccional de panel | Aumentar alcance de recepción, reducir ruido | Opcional |

> Nota: La lista original del proyecto comunitario `DroneAware` especifica la **AWUS036N (Ralink RT3070, 2.4 GHz mono-banda)** . Este kit se actualiza a la **AWUS036ACH (doble banda)** , capaz de cubrir tanto **NAN como Beacon** en 2.4 / 5 GHz, ofreciendo una cobertura más completa y mejor capacidad de expansión futura.

---

## 4. Lista de software

| Software / Paquete | Uso | Origen |
|---|---|---|
| Raspberry Pi OS Lite (64-bit) | Sistema operativo (headless) | raspberrypi.com |
| **Controlador rtl88xxau** | Controlador de monitor/inyección para RTL8812AU | [morrownr/8812au-20210629](https://github.com/morrownr/8812au-20210629) |
| `libpcap-dev`, `libbluetooth-dev`, `libncurses-dev` | Dependencias de compilación de `unix_rid_capture` | APT |
| **opendroneid-core-c** | Biblioteca C de codificación/decodificación de mensajes Open Drone ID (ASTM F3411 / EN 4709-002) | [opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| **unix_rid_capture** | Programa de captura RID WiFi/BT para Linux (salida JSON) | [sxjack/unix_rid_capture](https://github.com/sxjack/unix_rid_capture) |
| DroneAware Node (opcional) | Conexión a mapa comunitario en tiempo real | [fduflyer/DroneAware-Node-Releases](https://github.com/fduflyer/DroneAware-Node-Releases) |
| Kismet + plugin ANTSDR (ruta DJI) | Decodificación DJI OcuSync DroneID (requiere hardware SDR) | [kismetwireless/kismet](https://github.com/kismetwireless/kismet) + [alphafox02/antsdr_dji_droneid](https://github.com/alphafox02/antsdr_dji_droneid) |

---

## 5. Enlaces de proyectos en GitHub

```text
# Biblioteca principal de decodificación (codificación/decodificación ASTM F3411 / EN 4709-002)
https://github.com/opendroneid/opendroneid-core-c

# Programa de captura para Linux (programa principal de este kit, verificado rtl8812au + nRF52840 + RPi)
https://github.com/sxjack/unix_rid_capture

# Red de mapas comunitarios en tiempo real (instalación con un clic, subida automática a droneaware.io)
https://github.com/fduflyer/DroneAware-Node-Releases

# Marco de detección inalámbrica (la ruta DJI OcuSync requiere plugin SDR)
https://github.com/kismetwireless/kismet

# Controlador de monitor/inyección RTL8812AU (obligatorio para AWUS036ACH)
https://github.com/morrownr/8812au-20210629
```

---

## 6. Configuración paso a paso

### Paso 1 — Grabación del sistema

Use **Raspberry Pi Imager** para escribir **Raspberry Pi OS Lite (64-bit)** . En el engranaje (configuración avanzada):

- Nombre de host: `droneid-kit`
- Active SSH y configure usuario y contraseña
- Introduzca las credenciales WiFi (para evitar conectar Ethernet más tarde)

### Paso 2 — Conexión y verificación del hardware

Conecte la AWUS036ACH directamente al puerto **USB 3.0** de la Pi (azul / marcado `SS`), asegurándose de que ambas antenas estén bien apretadas. Tras el arranque, acceda por SSH:

```bash
ssh <usuario>@droneid-kit.local
sudo -i
lsusb
```

Debería ver:

```text
Bus 002 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter
```

### Paso 3 — Instalar el controlador de monitor rtl88xxau

```bash
sudo apt update && sudo apt install -y dkms git bc
git clone https://github.com/morrownr/8812au-20210629.git
cd 8812au-20210629
sudo ./install-driver.sh
sudo reboot
```

### Paso 4 — Verificar el modo monitor

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
iwconfig wlan0
```

La salida debería mostrar **`Mode:Monitor`** .

### Paso 5 — Instalar dependencias de compilación

```bash
sudo apt install -y git cmake libncurses-dev libpcap-dev \
  libbluetooth-dev libgps-dev libnl-genl-3-dev libgtest-dev build-essential
```

### Paso 6 — Compilar opendroneid-core-c

```bash
git clone --recursive https://github.com/opendroneid/opendroneid-core-c
cd opendroneid-core-c
mkdir build && cd build
cmake ../.
make -j
# Produce libopendroneid/libopendroneid.so y test/odidtest
```

### Paso 7 — Compilar unix_rid_capture

`unix_rid_capture` necesita `opendroneid.c` / `opendroneid.h`; cópielos desde el paso anterior:

```bash
cd ~
git clone https://github.com/sxjack/unix_rid_capture
cp opendroneid-core-c/libopendroneid/opendroneid.{c,h} unix_rid_capture/
cd unix_rid_capture
cmake .
make
```

### Paso 8 — Ejecutar la captura

Se requieren privilegios de root o `cap_net_raw`:

```bash
sudo setcap cap_net_raw+eip rid_capture
./rid_capture -x > rid_capture.txt        # Capturar y guardar en JSON
```

Salida UDP en tiempo real (abra otro terminal):

```bash
nc -lu 32001
```

### Paso 9 — Visualización de trayectorias (GPX → Google Earth)

```bash
./scripts/rid2gpx.pl < rid_capture.txt      # Generar .gpx
```

Abra con Google Earth para ver la trayectoria de vuelo del dron. Ejemplo típico de JSON detectado:

```json
{
  "mac": "ac:67:b2:09:50:d4",
  "operator": "GBR-OP-ZZZZZZZZZZZZ",
  "uav id": "SERIAL NUMBER",
  "uav latitude": 25.0330,
  "uav longitude": 121.5654,
  "uav altitude": 120,
  "uav heading": 90,
  "uav speed": 8,
  "base latitude": 25.0300,
  "base longitude": 121.5600
}
```

### Paso 10 — (Opcional) Conectar al mapa comunitario DroneAware

```bash
curl -fsSL https://github.com/fduflyer/DroneAware-Node-Releases/releases/latest/download/install.sh | sudo bash
```

{{< alert "circle-info" >}}
**Consejo de seguridad**: Para cualquier script de terceros con `curl ... | sudo bash`, se recomienda descargarlo y revisarlo antes de ejecutarlo: `curl -fsSL <url> -o install.sh && less install.sh && sudo bash install.sh`. El instalador detectará automáticamente la tarjeta USB, solicitará un nombre de nodo y guiará el registro en droneaware.io. Los resultados de detección se muestran en tiempo real en el mapa en vivo.
{{< /alert >}}

---

## 7. Aclaración técnica importante: RID estándar vs DJI OcuSync

Este es el valor profesional del artículo; es importante explicarlo claramente al cliente:

| Ruta | Responsable | Hardware | ¿Se puede usar ALFA AWUS036ACH? |
|---|---|---|---|
| **Remote ID estándar** | Transmisión ASTM F3411 WiFi/BT | AWUS036ACH + nRF52840 | ✅ Sí (tema principal de este artículo) |
| **DJI OcuSync DroneID** | Protocolo privado DJI (WiFi no estándar) | SDR completo (ANTSDR / HackRF / USRP) + plugin Kismet `kismet_cap_antsdr_droneid` | ❌ No |

- La ALFA AWUS036ACH es un **receptor en bandas WiFi (2.4 / 5 / 6 GHz)** , capaz de procesar completamente el RID estándar.
- El DroneID de **OcuSync** privado de DJI **no utiliza el protocolo WiFi estándar**, por lo que **la tarjeta ALFA no puede decodificarlo**; se necesita un SDR que cubra 2.4 / 5.8 GHz (como ANTSDR E200) con el plugin `alphafox02/antsdr_dji_droneid` + Kismet.
- ⚠️ Nota: **El ancho de banda del RTL-SDR está limitado a unos 1.7 GHz**, por lo que no puede ver OcuSync en 2.4 / 5.8 GHz; debe elegir un SDR que soporte altas frecuencias.
- Ambas rutas son **complementarias**: la tarjeta ALFA para detección de transmisiones RID estándar, el SDR para decodificación del protocolo privado DJI, formando un front-end completo de Counter-UAV / RF.

---

{{< faq >}}

---

## Apéndice: Glosario para principiantes (términos clave en lenguaje sencillo)

Si es la primera vez que se encuentra con la tecnología de regulación / antidrones (Counter-UAV), aquí tiene una explicación rápida de los términos más usados en este artículo:

| Término | Explicación sencilla |
|---|---|
| **Remote ID (Identificación Remota)** | La «matrícula aérea» del dron. La normativa exige que los drones transmitan continuamente su identidad, posición, etc., para que las personas en tierra (especialmente los reguladores) sepan «de quién es y hacia dónde va». |
| **ASTM F3411 / EN 4709-002** | Estándares de transmisión Remote ID de EE. UU. y la UE respectivamente, que definen el contenido y formato de la transmisión para garantizar la interoperabilidad entre drones y equipos de detección de diferentes fabricantes. |
| **Detección pasiva (Passive Detection)** | Simplemente «escuchar» la información pública transmitida, sin emitir señales activas para interferir o atacar al dron. Su legalidad es completamente diferente a la interferencia activa (jamming). |
| **monitor mode** | Permite que la tarjeta WiFi no se conecte a ningún router, sino que «simplemente escuche» los paquetes de radio en el aire; es el requisito previo para capturar las transmisiones de Remote ID. |
| **NAN (Wi-Fi Aware) / Beacon** | Dos formatos de trama WiFi que los drones utilizan para transmitir Remote ID. Este kit intenta analizar ambos simultáneamente. |
| **Bluetooth 5 Long Range** | Además de WiFi, algunos drones también transmiten Remote ID por Bluetooth, lo que requiere un nRF52840 adicional para su captura. |
| **DJI OcuSync / DroneID** | Protocolo privado de transmisión de video/telemetría de DJI, **no es WiFi estándar** ni el Remote ID que este artículo resuelve; requiere hardware SDR completamente diferente y plugins para su decodificación, explicado en la sección 7. |
| **SDR (Software Defined Radio)** | Hardware de radio definido por software que permite ajustar el rango de frecuencia de recepción y el método de demodulación mediante software, como ANTSDR o HackRF, capaces de cubrir bandas que la tarjeta ALFA no puede recibir (como DJI OcuSync). |
| **RTL8812AU** | Modelo de chip Realtek que utiliza la tarjeta ALFA AWUS036ACH, determinando su compatibilidad con el modo monitor. |
| **Archivo GPX** | Formato estándar para registrar trayectorias de coordenadas GPS, que se puede abrir directamente con Google Earth para visualizar la ruta de vuelo del dron. |

> En una frase: Este artículo le enseña a convertir la tarjeta ALFA en un «escáner de identidad de drones» — recibir pasivamente la información pública que los drones deben transmitir por ley, un medio legal para la gestión de seguridad perimetral.

---

## Referencias

1. [opendroneid/opendroneid-core-c — Biblioteca C de Open Drone ID Core](https://github.com/opendroneid/opendroneid-core-c)
2. [sxjack/unix_rid_capture — Captura WiFi/BT RID (verificado rtl8812au + nRF52840 + RPi)](https://github.com/sxjack/unix_rid_capture)
3. [fduflyer/DroneAware-Node-Releases — Red comunitaria de detección Remote ID](https://github.com/fduflyer/DroneAware-Node-Releases)
4. [kismetwireless/kismet — Marco de detección inalámbrica](https://github.com/kismetwireless/kismet)
5. [alphafox02/antsdr_dji_droneid — Decodificación SDR DJI OcuSync DroneID](https://github.com/alphafox02/antsdr_dji_droneid)
6. [morrownr/8812au-20210629 — Controlador Linux RTL8812AU de monitor/inyección](https://github.com/morrownr/8812au-20210629)
7. [Página del producto ALFA AWUS036ACH (Yupitek)](https://yupitek.com/es/products/alfa/awus036ach/)
8. [Contacto y pedidos de Yupitek](https://www.yupitek.com/es/contact/)

---

*Este artículo fue preparado por el equipo técnico de Yupitek. La AWUS036ACH y el hardware relacionado están disponibles a través de Yupitek como distribuidor autorizado, con soporte técnico.*
