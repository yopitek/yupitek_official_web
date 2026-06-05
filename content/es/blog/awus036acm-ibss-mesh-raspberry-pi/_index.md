---
title: "ALFA AWUS036ACM: Habilitando Redes IBSS Ad Hoc y 802.11s Mesh en Raspberry Pi con MT7612U"
description: "El ALFA AWUS036ACM (MT7612U) es el único adaptador USB WiFi ALFA actualmente en producción que soporta completamente IBSS Ad Hoc y redes Mesh 802.11s en Raspberry Pi — plug-and-play, sin instalación de controladores."
date: 2026-03-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA", "AWUS036ACM", "MT7612U", "Raspberry Pi", "IBSS", "Ad Hoc", "802.11s", "Redes Mesh", "Linux", "Inalámbrico"]
featureimage: "/images/blog/awus036acm-ibss-mesh-raspberry-pi.webp"
---

# ALFA AWUS036ACM: Habilitando Redes IBSS Ad Hoc y 802.11s Mesh en Raspberry Pi con MT7612U

Si alguna vez intentaste construir una red WiFi entre nodos Raspberry Pi **sin un router** — o crear una malla inalámbrica autorreparable que enrute el tráfico automáticamente a través de saltos intermedios — rápidamente descubres que la mayoría de los adaptadores USB WiFi no pueden hacerlo. El controlador del núcleo simplemente no expone los modos necesarios.

El **ALFA AWUS036ACM**, impulsado por el chipset **MediaTek MT7612U**, es la excepción. Su controlador `mt76` integrado en el núcleo implementa la interfaz mac80211 completa de Linux, lo que significa que soporta de forma nativa tanto el modo **IBSS (Ad Hoc)** como el modo **802.11s Mesh Point** en Raspberry Pi — desde el primer momento, sin necesidad de compilar ningún controlador.

Esta guía explica exactamente cómo funcionan ambos modos, proporciona instrucciones de configuración paso a paso, y te muestra cuándo elegir uno sobre el otro.

---

## Tabla de Contenidos

1. [¿Qué son IBSS y 802.11s Mesh — y por qué importan?](#1-what-are-ibss-and-80211s-mesh)
2. [Especificaciones de Hardware del ALFA AWUS036ACM](#2-alfa-awus036acm-hardware-specifications)
3. [El Controlador MT7612U en Raspberry Pi](#3-the-mt7612u-driver-on-raspberry-pi)
4. [Modo 1: Redes IBSS Ad Hoc](#4-mode-1-ibss-ad-hoc-networking)
5. [Modo 2: Redes 802.11s Mesh Point](#5-mode-2-80211s-mesh-point-networking)
6. [Casos de Uso Reales](#6-real-world-use-cases)
7. [Por Qué el AWUS036ACM es la Única Opción ALFA para Esto](#7-why-the-awus036acm-is-the-only-alfa-choice-for-this)
8. [Preguntas Frecuentes y Solución de Problemas](#8-faq-and-troubleshooting)
9. [Dónde Comprar](#9-where-to-buy)

---

## 1. ¿Qué son IBSS y 802.11s Mesh?

### IBSS — Independent Basic Service Set (Modo Ad Hoc)

Cuando conectas tu laptop a un router WiFi doméstico, tu adaptador está en modo **Managed (Station)** — habla con un único Punto de Acceso central. IBSS es lo opuesto: es la especificación IEEE 802.11 para **redes inalámbricas punto a punto sin infraestructura central**.

En modo IBSS:

- Los dispositivos se comunican **directamente** entre sí, sin ningún AP ni router de por medio
- Cualquier par de dispositivos en el mismo SSID y canal pueden intercambiar datos
- La red es autónoma — no se necesita conexión a internet
- Las IPs se asignan de forma estática (o mediante un daemon DHCP sencillo que tú mismo ejecutas)
- El primer dispositivo en "unirse" al IBSS se convierte en el originador del BSSID (el identificador de celda)

Piénsalo como crear una LAN inalámbrica privada instantánea entre un pequeño número de nodos Pi — un pipeline de dos nodos, un clúster de tres sensores, o un kit de comunicación portátil desplegado en campo.

**Limitaciones de IBSS que debes conocer:**
- Todos los nodos deben estar dentro del alcance de radio directo entre sí — no hay reenvío multi-salto automático
- El cifrado WPA2 estándar no está disponible en modo IBSS (WEP es técnicamente posible pero no recomendado; la mayoría de los despliegues usan seguridad en la capa de aplicación)
- Escala prácticamente hasta 3–5 nodos antes de que el rendimiento se degrade

### 802.11s Mesh Point — La Alternativa Escalable

802.11s es una enmienda IEEE separada que define **redes mesh inalámbricas verdaderas**. A diferencia de IBSS, una red 802.11s mesh:

- Descubre automáticamente los nodos vecinos y construye una tabla de enrutamiento
- Reenvía el tráfico a través de saltos intermedios para alcanzar nodos fuera del alcance directo
- Se autorreparala cuando un nodo desaparece — otras rutas se utilizan automáticamente
- Usa el **Hybrid Wireless Mesh Protocol (HWMP)** para la selección de rutas por defecto

```
Ejemplo: malla de 4 nodos

  [Pi A] ──── [Pi B] ──── [Pi C]
                │
              [Pi D]

Pi A puede alcanzar Pi C a través de Pi B, automáticamente.
Pi A puede alcanzar Pi D a través de Pi B, automáticamente.
Si Pi B falla, la malla intenta encontrar rutas alternativas.
```

802.11s es la opción correcta cuando tienes más de 3–4 nodos, cuando los nodos están distribuidos en un área más grande, o cuando quieres que la red sea resiliente sin gestión manual.

### Por Qué Es Difícil Encontrar un Adaptador que Funcione

Los dos modos anteriores requieren que el controlador WiFi esté construido sobre la capa de MAC por software **mac80211** de Linux — el stack 802.11 oficial del núcleo. Solo los controladores compatibles con mac80211 exponen IBSS y mesh point como tipos de interfaz utilizables.

Muchos adaptadores USB WiFi populares usan **controladores fuera del núcleo** que implementan su propio stack inalámbrico simplificado y deliberadamente omiten el soporte de IBSS y mesh. Incluso algunos controladores integrados en el núcleo para chipsets más nuevos no exponen estos modos.

El MT7612U es uno de los pocos chipsets donde la respuesta es un **sí** claro e inequívoco para ambos.

---

## 2. Especificaciones de Hardware del ALFA AWUS036ACM

El AWUS036ACM es el adaptador USB 3.0 de doble banda AC1200 de ALFA Network, diseñado para usuarios avanzados de Linux y desarrolladores embebidos.

![ALFA AWUS036ACM](/images/products/alfa/awus036acm.png)

### Especificaciones Principales

| Parámetro | Valor |
|---|---|
| **Chipset** | MediaTek MT7612U |
| **Estándar WiFi** | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| **Bandas de Frecuencia** | 2.4 GHz (2.412–2.472 GHz) + 5 GHz (5.15–5.825 GHz) |
| **Anchos de Canal** | 20 / 40 / 80 MHz |
| **Velocidad Máx. (5 GHz)** | 867 Mbps (802.11ac) |
| **Velocidad Máx. (2.4 GHz)** | 300 Mbps (802.11n) |
| **Velocidad Combinada** | AC1200 (867 + 300 Mbps) |
| **Interfaz USB** | USB 3.0 Tipo-A (compatible con USB 2.0) |
| **Antenas** | 2× conectores RP-SMA hembra, 2× dipolo de doble banda 5 dBi (desmontables) |
| **USB VID/PID** | 0e8d:7612 |
| **Indicadores LED** | Energía + actividad WLAN |
| **Accesorios Incluidos** | Cable de extensión USB 3.0, CD de controladores (Windows) |
| **Dimensiones** | 62 × 85.3 × 24 mm |
| **Peso** | 60 g |
| **País de Origen** | Taiwán (Alfa Network Inc.) |

### Potencia de Transmisión

| Estándar | Potencia TX |
|---|---|
| 802.11a | 20 dBm |
| 802.11b | 23 dBm |
| 802.11g | 23 dBm |
| 802.11n | 21 dBm |
| 802.11ac | 20 dBm |

### Sensibilidad de Recepción

| Estándar | Sensibilidad |
|---|---|
| 802.11a | −92 dBm |
| 802.11b | −97 dBm |
| 802.11g | −90 dBm |
| 802.11n | −90 dBm |
| 802.11ac | −86 dBm |

### Modos de Interfaz Soportados (Lista Completa)

Esta es la tabla de capacidades clave. El controlador MT7612U / mt76x2u soporta todos los modos de interfaz mac80211 principales:

| Modo | Soportado | Descripción |
|---|---|---|
| **IBSS** | ✅ Sí | Ad Hoc punto a punto, sin necesidad de AP |
| **Managed (Station)** | ✅ Sí | Modo cliente estándar |
| **AP** | ✅ Sí | Punto de Acceso por software (hostapd) |
| **AP/VLAN** | ✅ Sí | LAN virtual sobre AP |
| **Monitor** | ✅ Sí | Captura pasiva + inyección de paquetes |
| **Mesh Point** | ✅ Sí | Redes mesh multi-salto 802.11s |
| **P2P-client** | ✅ Sí | Cliente Wi-Fi Direct |
| **P2P-GO** | ✅ Sí | Propietario de Grupo Wi-Fi Direct |

### Seguridad Inalámbrica
WPA2 / WPA / WEP / WPA-PSK / 802.1X / WEP de 64–128 bits

### Sistemas Operativos Soportados

| SO | Estado | Notas |
|---|---|---|
| Raspberry Pi OS (2020+) | ✅ Plug & Play | Sin instalación de controladores |
| Ubuntu 20.04 LTS+ | ✅ Plug & Play | Controlador mt76 integrado en el núcleo |
| Kali Linux 2019.3+ | ✅ Plug & Play | Monitor + inyección + VIF completos |
| Debian 11+ | ✅ Funciona | Puede requerir firmware-misc-nonfree |
| Arch Linux | ✅ Plug & Play | Integrado en el núcleo desde 4.19 |
| Windows 10/11 | ✅ Soportado | Controlador oficial desde el sitio de Alfa |
| Android NetHunter | ✅ Soportado | USB OTG |
| macOS 11+ / Apple Silicon | ❌ No soportado | Solo macOS 10.7–10.12 |

---

## 3. El Controlador MT7612U en Raspberry Pi

### Controlador: mt76x2u (Parte de la Familia mt76)

El MediaTek MT7612U es manejado por el controlador `mt76x2u`, que forma parte del proyecto de controladores **mt76**, mantenido por MediaTek e integrado en el núcleo Linux principal.

**Los números clave:**
- Integrado en el núcleo desde: **Linux kernel 4.19** (lanzado en octubre de 2018)
- Raspberry Pi OS viene con el núcleo **5.15+** (Pi 4/5) y **5.10+** (Pi 3B+) — ambos muy por encima de 4.19
- **No se necesita ningún paso de instalación en ninguna versión moderna de Raspberry Pi OS**

### Cómo Verificar que el Controlador está Cargado

Después de conectar el AWUS036ACM, ejecuta:

```bash
lsusb
```

Busca la entrada:
```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

Luego confirma que el controlador está activo:

```bash
dmesg | grep mt76
```

Salida esperada (condensada):
```
mt76x2u 1-1.4:1.0: ASIC revision: 76120044
mt76x2u 1-1.4:1.0: Firmware Version: 0.1
mt76x2u 1-1.4:1.0: loaded firmware from mediatek/mt7662u_rom_patch.bin
```

Lista la nueva interfaz:
```bash
iw dev
```

Deberías ver una nueva interfaz (típicamente `wlan1` si el WiFi integrado del Pi es `wlan0`):
```
phy#1
    Interface wlan1
        ifindex 4
        wdev 0x100000001
        addr xx:xx:xx:xx:xx:xx
        type managed
        channel 6 (2437 MHz), width: 20 MHz (no HT), center1: 2437 MHz
```

Verifica la lista completa de capacidades del adaptador:
```bash
iw phy phy1 info | grep -A 20 "Supported interface modes"
```

Verás:
```
Supported interface modes:
     * IBSS
     * managed
     * AP
     * AP/VLAN
     * monitor
     * mesh point
     * P2P-client
     * P2P-GO
```

### Por Qué la Arquitectura del Controlador Importa

La pila de controladores del AWUS036ACM se ve así:

```
Tu Aplicación (ping, iperf3, batman-adv...)
        ↓
nl80211 / cfg80211  ← API de configuración WiFi del núcleo
        ↓
mac80211            ← capa MAC por software IEEE 802.11
        ↓
mt76x2u             ← controlador de hardware USB MT7612U
        ↓
MediaTek MT7612U    ← chip físico (2×2 MIMO, USB 3.0)
```

**mac80211** es la implementación del núcleo Linux de la máquina de estados 802.11 completa — gestiona la administración de balizas, construcción de tramas, ahorro de energía, descubrimiento de pares IBSS y enrutamiento de rutas mesh. Los controladores construidos sobre mac80211 heredan automáticamente todas estas capacidades.

Los controladores que eluden mac80211 (controladores fuera del núcleo de Realtek, por ejemplo) implementan únicamente los modos que ellos deciden exponer — e IBSS y mesh point casi siempre se omiten.

---

## 4. Modo 1: Redes IBSS Ad Hoc

### Cómo Funciona IBSS

En modo IBSS, cada adaptador gestiona sus propias tramas 802.11. Cuando dos adaptadores se configuran en el mismo SSID y canal:

1. El primer dispositivo genera un **BSSID** aleatorio (el ID de celda IBSS)
2. Transmite balizas en el canal elegido
3. El segundo dispositivo escanea, encuentra la baliza, y **se une** a la celda
4. Ambos dispositivos pueden intercambiar tramas de datos directamente — sin un AP en el medio

Desde la perspectiva del SO, la interfaz IBSS se comporta como una interfaz Ethernet ordinaria — asignas IPs y usas TCP/IP con normalidad.

### IBSS vs. Modo Managed de un Vistazo

| Característica | IBSS (Ad Hoc) | Managed (Station) |
|---|---|---|
| ¿Se necesita AP central? | ❌ No | ✅ Sí |
| ¿Se requiere internet? | ❌ No | Usualmente sí |
| Complejidad de configuración | Baja | Muy baja |
| Máx. nodos prácticos | 3–5 | Ilimitado (vía AP) |
| Soporte WPA2 | ❌ No | ✅ Sí |
| Ideal para | Clústeres Pi aislados, kits de campo | Redes domésticas/de oficina |

### Paso a Paso: Red IBSS con Dos Raspberry Pi

Este ejemplo crea un enlace directo a 5 GHz entre dos unidades Raspberry Pi. Ajusta las IPs y el SSID según tu despliegue.

**En ambos nodos — identifica la interfaz correcta:**

```bash
iw dev
```

El AWUS036ACM típicamente aparece como `wlan1` (si el WiFi integrado del Pi es `wlan0`). Confirma verificando la dirección MAC contra `lsusb`. En todos los comandos a continuación, reemplaza `wlan1` con el nombre real de tu interfaz.

---

#### Nodo 1 (Pi #1 — IP: 192.168.88.1)

**Paso 1 — Detén NetworkManager / wpa_supplicant para evitar interferencias:**

```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
```

**Paso 2 — Baja la interfaz:**

```bash
sudo ip link set wlan1 down
```

**Paso 3 — Configura la interfaz en modo IBSS:**

```bash
sudo iw dev wlan1 set type ibss
```

**Paso 4 — Vuelve a subir la interfaz:**

```bash
sudo ip link set wlan1 up
```

**Paso 5 — Únete (o crea) la celda IBSS en el Canal 36 de 5 GHz:**

```bash
sudo iw dev wlan1 ibss join RaspberryMesh 5180
```

> **Referencia de frecuencias:**
> - 5180 MHz = Canal 36 de 5 GHz (canal interior común, buen rendimiento)
> - 5200 MHz = Canal 40 de 5 GHz
> - 2412 MHz = Canal 1 de 2.4 GHz (mayor alcance, menor velocidad)
> - 2437 MHz = Canal 6 de 2.4 GHz

**Paso 6 — Asigna una dirección IP estática:**

```bash
sudo ip addr add 192.168.88.1/24 dev wlan1
```

---

#### Nodo 2 (Pi #2 — IP: 192.168.88.2)

Ejecuta los mismos comandos, cambiando únicamente la dirección IP:

```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
sudo ip link set wlan1 down
sudo iw dev wlan1 set type ibss
sudo ip link set wlan1 up
sudo iw dev wlan1 ibss join RaspberryMesh 5180
sudo ip addr add 192.168.88.2/24 dev wlan1
```

---

#### Verificar el Enlace

En el Nodo 1:
```bash
iw dev wlan1 link
```

Salida esperada (una vez que el Nodo 2 se ha unido):
```
Connected to xx:xx:xx:xx:xx:xx (on wlan1)
    IBSS cell ID/AP: xx:xx:xx:xx:xx:xx
    SSID: RaspberryMesh
    freq: 5180
    RX: 1204 bytes (12 packets)
    TX: 852 bytes (8 packets)
    signal: -48 dBm
    tx bitrate: 300.0 MBit/s MCS 15 40MHz
```

Prueba la conectividad:
```bash
ping -c 4 192.168.88.2
```

```
PING 192.168.88.2 (192.168.88.2) 56(84) bytes of data.
64 bytes from 192.168.88.2: icmp_seq=1 ttl=64 time=1.84 ms
64 bytes from 192.168.88.2: icmp_seq=2 ttl=64 time=1.92 ms
64 bytes from 192.168.88.2: icmp_seq=3 ttl=64 time=2.01 ms
64 bytes from 192.168.88.2: icmp_seq=4 ttl=64 time=1.88 ms
```

Prueba el rendimiento con iperf3:
```bash
# En el Nodo 2 (servidor):
iperf3 -s

# En el Nodo 1 (cliente):
iperf3 -c 192.168.88.2 -t 10
```

### Hacer IBSS Persistente Tras Reinicios

Crea `/etc/systemd/system/ibss-mesh.service` en cada nodo:

```ini
[Unit]
Description=IBSS Ad Hoc Mesh Network
After=network.target
Wants=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sleep 5
ExecStart=/bin/bash -c '\
  ip link set wlan1 down && \
  iw dev wlan1 set type ibss && \
  ip link set wlan1 up && \
  iw dev wlan1 ibss join RaspberryMesh 5180 && \
  ip addr add 192.168.88.1/24 dev wlan1'
ExecStop=/bin/bash -c '\
  iw dev wlan1 ibss leave && \
  ip link set wlan1 down'

[Install]
WantedBy=multi-user.target
```

Habilítalo:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ibss-mesh.service
sudo systemctl start ibss-mesh.service
```

> **Nota:** Cambia la dirección IP en el archivo de servicio para cada nodo (`.1`, `.2`, `.3`, etc.)

### Agregar un Tercer Nodo

Para el Nodo 3, usa el mismo procedimiento con la IP `192.168.88.3`. Los tres nodos deben estar dentro del alcance de radio directo entre sí. Para enrutar el tráfico entre el Nodo 1 y el Nodo 3 a través del Nodo 2, habilita el reenvío IP en el Nodo 2:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

---

## 5. Modo 2: Redes 802.11s Mesh Point

### Cómo Funciona 802.11s

La enmienda 802.11s añade una **capa de coordinación mesh** directamente en el MAC 802.11. En lugar de que todos los nodos hablen con un AP central, cada nodo:

1. Descubre los nodos mesh vecinos transmitiendo tramas **Mesh Beacon** en el canal y `mesh_id` elegidos
2. Ejecuta **HWMP (Hybrid Wireless Mesh Protocol)** para calcular la mejor ruta hacia cada destino
3. Encapsula las tramas de datos con un **Mesh Header** que incluye las direcciones MAC de origen y destino más un número de secuencia mesh
4. Reenvía las tramas a través de saltos intermedios automáticamente cuando el destino está fuera del alcance directo

El núcleo Linux expone esto a través del tipo de interfaz `mp` (mesh point) en `iw`, y la propia implementación 80211s del núcleo gestiona todo el emparejamiento y la administración de rutas.

### 802.11s Comparado con IBSS

| Característica | IBSS (Ad Hoc) | 802.11s Mesh Point |
|---|---|---|
| Estándar IEEE | 802.11 IBSS | 802.11s |
| Enrutamiento multi-salto | ❌ Solo manual | ✅ Automático (HWMP) |
| Alcance entre nodos | Todos en rango directo | Se extiende más allá de un salto |
| Escalabilidad | 3–5 nodos prácticos | 10+ nodos con batman-adv |
| Complejidad de configuración | Baja | Media |
| Autorreparación | ❌ No | ✅ Sí |
| Ideal para | Configuraciones simples de 2–3 nodos | Sistemas distribuidos más grandes |

### Paso a Paso: Mesh 802.11s Multi-Nodo

Este ejemplo construye una malla de tres nodos en el Canal 36 de 5 GHz. Cada nodo descubre automáticamente a los demás y establece rutas.

---

#### En Cada Nodo — Crea la Interfaz Mesh

**Paso 1 — Identifica el nombre del dispositivo físico (phy):**

```bash
iw dev
```

Busca el phy asociado con el AWUS036ACM (típicamente `phy1`):
```
phy#1
    Interface wlan1
        ...
```

**Paso 2 — Añade una nueva interfaz mesh point llamada `mesh0`:**

```bash
sudo iw phy phy1 interface add mesh0 type mp mesh_id RaspberryMesh
```

> Esto crea una nueva interfaz virtual `mesh0` en la misma radio física que `wlan1`. La `wlan1` original puede permanecer en modo managed para acceso a internet simultáneamente — esto es VIF (Virtual Interface) en acción.

**Paso 3 — Establece el canal de operación (Canal 36 de 5 GHz):**

```bash
sudo iw dev mesh0 set channel 36
```

**Paso 4 — Sube la interfaz mesh:**

```bash
sudo ip link set mesh0 up
```

**Paso 5 — Asigna una dirección IP única por nodo:**

```bash
# Nodo 1:
sudo ip addr add 10.88.0.1/24 dev mesh0

# Nodo 2:
sudo ip addr add 10.88.0.2/24 dev mesh0

# Nodo 3:
sudo ip addr add 10.88.0.3/24 dev mesh0
```

---

#### Verificar la Formación de la Malla

**Comprueba que se han descubierto los pares:**

```bash
iw dev mesh0 station dump
```

Salida de ejemplo (el Nodo 1 ve al Nodo 2 y al Nodo 3):
```
Station xx:xx:xx:xx:xx:02 (on mesh0)
    inactive time:  120 ms
    rx bytes:       4820
    tx bytes:       3560
    signal:         -52 dBm
    tx bitrate:     300.0 MBit/s MCS 15 40MHz
    mesh plink:     ESTAB
    mesh local PS mode: ACTIVE

Station xx:xx:xx:xx:xx:03 (on mesh0)
    mesh plink:     ESTAB
```

**Inspecciona las rutas mesh:**

```bash
iw dev mesh0 mpath dump
```

```
DEST ADDR         NEXT HOP          IFACE   SN      METRIC  QLEN    EXPTIME         DTIM    DRET    FLAGS
xx:xx:xx:xx:xx:02 xx:xx:xx:xx:xx:02 mesh0   32      1158    0       0       100     0       0x4
xx:xx:xx:xx:xx:03 xx:xx:xx:xx:xx:02 mesh0   18      2316    0       0       100     0       0x14
```

> El siguiente salto del Nodo 3 es el Nodo 2 — lo que significa que el Nodo 1 alcanza al Nodo 3 a través del Nodo 2 automáticamente.

**Ping a través de la malla:**

```bash
# Desde el Nodo 1:
ping -c 4 10.88.0.3
```

### Avanzado: Añadir batman-adv para Enrutamiento Mesh en Capa 2

Para despliegues en producción, reemplazar el HWMP integrado del núcleo con **batman-adv** proporciona enrutamiento más avanzado, mejor rendimiento bajo movilidad, y compatibilidad con herramientas de red de mayor nivel.

**Instala batman-adv:**

```bash
sudo apt install batctl
```

**Carga el módulo:**

```bash
sudo modprobe batman-adv
```

**Configura la interfaz mesh como esclava de batman-adv:**

```bash
# Sube mesh0 sin IP primero
sudo ip link set mesh0 up
sudo batctl if add mesh0

# Sube la interfaz batman
sudo ip link set bat0 up

# Asigna la IP a la interfaz batman (no a mesh0)
sudo ip addr add 10.88.0.1/24 dev bat0
```

**Consulta la tabla de enrutamiento de batman:**

```bash
sudo batctl n    # Vecinos
sudo batctl o    # Tabla de originadores (todos los nodos conocidos)
sudo batctl tg   # Tabla de traducción (mapeo MAC → IP)
```

### Hacer 802.11s Mesh Persistente

Crea `/etc/systemd/system/mesh-point.service`:

```ini
[Unit]
Description=802.11s Mesh Point Network
After=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sleep 5
ExecStart=/bin/bash -c '\
  iw phy phy1 interface add mesh0 type mp mesh_id RaspberryMesh && \
  iw dev mesh0 set channel 36 && \
  ip link set mesh0 up && \
  ip addr add 10.88.0.1/24 dev mesh0'
ExecStop=/bin/bash -c '\
  ip link set mesh0 down && \
  iw dev mesh0 del'

[Install]
WantedBy=multi-user.target
```

Habilítalo:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mesh-point.service
sudo systemctl start mesh-point.service
```

---

## 6. Casos de Uso Reales

### Caso de Uso 1 — Red de Sensores Fuera de la Red Eléctrica (Agricultura Inteligente / Monitoreo Ambiental)

**Escenario:** Tres unidades Raspberry Pi desplegadas a lo largo de un campo, cada una con sensores de humedad del suelo, temperatura y humedad ambiental. No hay infraestructura celular ni WiFi disponible.

**Configuración:** IBSS en el Canal 1 de 2.4 GHz (2412 MHz) para máximo alcance. Cada nodo recolecta datos de sensores y los envía a un nodo registrador central (Nodo 1) cada 30 segundos.

**Por qué el AWUS036ACM:** Las antenas de 5 dBi y la potencia TX de 23 dBm en 2.4 GHz otorgan al adaptador un alcance superior al promedio — útil para cubrir las distancias entre hileras en un campo. Con actualizaciones opcionales de antenas RP-SMA (por ejemplo, Yagi direccionales), el alcance puede extenderse significativamente.

**Pipeline de datos de ejemplo:**
```
[Sensor Pi A] ──IBSS──> [Edge Pi B (logger)]
[Sensor Pi C] ──IBSS──> [Edge Pi B (logger)]
```

---

### Caso de Uso 2 — Comunicación en Clúster de Drones / Robots

**Escenario:** Dos o tres drones o robots terrestres basados en Raspberry Pi necesitan compartir datos de telemetría y coordinar acciones sin pasar por una estación terrestre.

**Configuración:** IBSS en el Canal 36 de 5 GHz (5180 MHz) para baja latencia y alto rendimiento. Cada unidad transmite video H.264 1080p a ~5 Mbps más telemetría a <100 Kbps.

**Por qué 5 GHz:** A velocidades AC1200 (867 Mbps en 5 GHz), el AWUS036ACM tiene más que suficiente margen para múltiples flujos de video simultáneos. La banda de 5 GHz también evita la interferencia congestionada de 2.4 GHz común en áreas urbanas.

**Topología:**
```
[Drone 1 / 192.168.88.1] ──5GHz IBSS──> [Drone 2 / 192.168.88.2]
```

---

### Caso de Uso 3 — Kit de Respuesta a Desastres / Comunicación de Emergencia

**Escenario:** Un equipo de despliegue rápido llega a un lugar sin infraestructura. Cada miembro del equipo porta una Raspberry Pi Zero 2W + AWUS036ACM + batería portátil. En 60 segundos, una malla multi-nodo funcional está activa para comunicación de texto, intercambio de archivos y coordinación.

**Configuración:** 802.11s Mesh en 2.4 GHz para máximo alcance a través de edificios y obstáculos. batman-adv gestiona el enrutamiento para que el equipo no tenga que administrar IPs manualmente.

**Por qué 802.11s / batman-adv:** Cuando los miembros del equipo se mueven, la topología de la malla cambia. batman-adv actualiza automáticamente las rutas. No hay un único punto de falla.

---

### Caso de Uso 4 — Backbone de Clúster de Cómputo con Raspberry Pi

**Escenario:** Un desarrollador ejecuta un clúster de cómputo estilo Beowulf usando 4–6 unidades Raspberry Pi 4. Quiere una interconexión dedicada de baja latencia separada de la red Ethernet principal.

**Configuración:** 802.11s Mesh en 5 GHz usando mesh_id `ClusterBackbone`. Cada nodo se comunica a través de la malla para mensajería entre procesos (MPI, Redis pub/sub, ZeroMQ).

**Por qué una malla dedicada:** Separar el tráfico del clúster de la red principal evita saturar el switch Ethernet compartido y permite la red del clúster incluso cuando la red principal no está disponible.

---

### Caso de Uso 5 — Laboratorio de Investigación en Seguridad / Entorno de Pruebas Aislado

**Escenario:** Un evaluador de penetración o investigador de seguridad quiere simular una red IBSS 802.11 privada para probar vulnerabilidades específicas de ad hoc o validar herramientas de detección.

**Configuración:** IBSS en un canal limpio, aislado del WiFi de producción, usando el modo monitor del AWUS036ACM simultáneamente a través de un VIF. Una interfaz en IBSS (participando en la red), otra en monitor (capturando todas las tramas para análisis en Wireshark).

```bash
# Crear interfaz monitor junto a IBSS
sudo iw phy phy1 interface add mon0 type monitor
sudo ip link set mon0 up
# Capturar:
sudo tcpdump -i mon0 -w capture.pcap
```

---

## 7. Por Qué el AWUS036ACM es la Única Opción ALFA para Esto

### El Factor Decisivo: Conformidad con mac80211

Si un adaptador USB WiFi soporta IBSS y mesh 802.11s en Linux depende enteramente de la arquitectura de su controlador. Solo los **controladores en el núcleo basados en mac80211** exponen estos modos. Los controladores que implementan su propio stack WiFi (la mayoría de los controladores fuera del núcleo de Realtek) simplemente no incluyen la funcionalidad IBSS o mesh.

### Dónde Está Cada Adaptador ALFA Activo

| Modelo | Chipset | Controlador | IBSS | Mesh 802.11s | Notas |
|---|---|---|---|---|---|
| **AWUS036ACM** | MT7612U | mt76x2u (en núcleo ≥ 4.19) | ✅ | ✅ | **La única opción** |
| AWUS036ACH | RTL8812AU | rtw88 (en núcleo ≥ 6.14) | ✅ (solo núcleo ≥ 6.14) | ❌ | Nuevo controlador en núcleo; sin mesh point |
| AWUS036ACS | RTL8811AU | rtl8812au-dkms (OOK) | ❌ | ❌ | Controlador fuera del núcleo; sin IBSS/mesh |
| AWUS036AX | RTL8832BU | rtw88 (en núcleo) | ❌ | ❌ | Sin soporte para Raspberry Pi |
| AWUS036AXER | RTL8832BU | rtw88 (en núcleo) | ❌ | ❌ | Sin soporte para Raspberry Pi |
| AWUS036AXM | MT7921AUN | mt7921u (en núcleo ≥ 5.18) | ❌ | ❌ | mt7921u no expone IBSS |
| AWUS036AXML | MT7921AUN | mt7921u (en núcleo ≥ 5.18) | ❌ | ❌ | mt7921u no expone IBSS |
| ~~AWUS036ACHM~~ | ~~MT7610U~~ | ~~mt76x0u~~ | ~~✅~~ | ~~✅~~ | **Fin de Vida — descontinuado** |
| ~~AWUS1900~~ | ~~RTL8814AU~~ | ~~OOK~~ | ~~Limitado~~ | ~~❌~~ | **Fin de Vida — descontinuado** |

### Qué Significa Esto para Ti

El AWUS036ACHM (MT7610U) fue el adaptador ALFA anterior que soportaba estos modos — ahora está descontinuado. No existe ningún otro adaptador USB ALFA fabricado actualmente que proporcione IBSS y Mesh 802.11s plug-and-play en Raspberry Pi.

**El AWUS036ACM no es simplemente la mejor opción — es la única opción en la línea actual de ALFA para este caso de uso.**

Además, el AWUS036ACM ofrece:
- **AC1200 de doble banda** — soporta IBSS/mesh tanto en 2.4 GHz (alcance) como en 5 GHz (rendimiento)
- **USB 3.0** — aprovechamiento completo del ancho de banda en los puertos USB 3.0 de Pi 4/5
- **2× antenas RP-SMA desmontables** — actualiza a antenas direccionales de alta ganancia para extender el alcance de la malla mucho más allá de los dipolos de 5 dBi incluidos
- **Soporte VIF** — ejecuta el backbone mesh y el modo AP simultáneamente en un solo adaptador
- **Funciona en Raspberry Pi 3B+, 4 y 5** — consistente en todas las generaciones de Pi

---

## 8. Preguntas Frecuentes y Solución de Problemas

**P: Mi Pi solo muestra `wlan0`. ¿Dónde está `wlan1`?**

La interfaz del AWUS036ACM aparece después de conectar el adaptador. Ejecuta `iw dev` tras conectarlo. Si no aparece en 10 segundos, revisa `dmesg | grep -i mt76` para mensajes de error. En Raspberry Pi OS Lite, puede que necesites `sudo apt install iw` si el paquete no está instalado.

---

**P: `iw dev wlan1 set type ibss` devuelve "Device or resource busy"**

NetworkManager o `wpa_supplicant` está ocupando la interfaz. Detenlos:
```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
```
Luego reintenta. En Raspberry Pi OS con escritorio, `dhcpcd` también puede retener la interfaz — añade `denyinterfaces wlan1` a `/etc/dhcpcd.conf` y reinicia `dhcpcd`.

---

**P: `iw phy phy1 interface add mesh0 type mp` devuelve "Operation not supported"**

El nombre phy del adaptador puede no ser `phy1`. Ejecuta `iw dev` para verificar en qué phy está el AWUS036ACM y sustituye el nombre correcto.

---

**P: IBSS está configurado pero el ping entre nodos falla**

Verifica:
1. Ambos nodos están en la **misma frecuencia exacta** (por ejemplo, ambos en `5180`, no uno en `5180` y otro en `5200`)
2. Ambos nodos tienen **direcciones IP distintas** en la misma subred
3. No hay un firewall bloqueando ICMP — revisa con `sudo iptables -L`
4. Ejecuta `iw dev wlan1 link` para confirmar que el ID de celda IBSS (BSSID) coincide en ambos nodos

---

**P: La interfaz mesh0 desaparece tras reiniciar**

Las interfaces virtuales creadas con `iw` no persisten entre reinicios. Usa el servicio systemd mostrado en la [Sección 5](#making-80211s-mesh-persistent) para recrearlas automáticamente.

---

**P: ¿Puedo usar cifrado WPA2 sobre IBSS?**

El WPA2-Personal estándar (PSK) no está soportado en modo IBSS por el núcleo Linux. Para IBSS seguro, puedes usar cifrado en la capa de aplicación (WireGuard, OpenVPN o túneles SSH). El mesh 802.11s sí soporta SAE (autenticación estilo WPA3) con `wpa_supplicant`.

---

**P: ¿Puede el AWUS036ACM estar en modo IBSS y managed simultáneamente?**

Sí — para eso existe VIF (Virtual Interface). Puedes mantener `wlan1` en modo managed conectado a tu router doméstico para acceso a internet, mientras añades una segunda interfaz virtual en modo IBSS o mesh para la red Pi-a-Pi:

```bash
# wlan1 permanece como managed (internet)
# Añade segunda interfaz para IBSS
sudo iw phy phy1 interface add adhoc0 type ibss
sudo ip link set adhoc0 up
sudo iw dev adhoc0 ibss join LocalNet 5180
sudo ip addr add 192.168.88.1/24 dev adhoc0
```

---

**P: ¿Cuál es el alcance máximo que puedo lograr?**

Con las antenas de 5 dBi incluidas, espera entre 20–50 m en exteriores en campo abierto en 5 GHz, y entre 50–100 m en 2.4 GHz. Al reemplazar las antenas con antenas direccionales RP-SMA de alta ganancia (disponibles por separado), el alcance puede extenderse a varios cientos de metros en condiciones de línea de visión directa. Los conectores RP-SMA del AWUS036ACM son de tamaño estándar y compatibles con una amplia gama de antenas de terceros.

---

**P: ¿Funciona en Raspberry Pi Zero 2W?**

Sí — la Raspberry Pi Zero 2W tiene un puerto USB-A completo (mediante adaptador OTG) y ejecuta Raspberry Pi OS con un núcleo muy por encima de 4.19. El AWUS036ACM funciona allí, pero ten en cuenta que el puerto USB del Zero 2W es solo USB 2.0, lo que limita el ancho de banda a aproximadamente 300–400 Mbps en la práctica. Para tráfico de control IBSS/mesh y datos de sensores, esto es más que suficiente.

---

## 9. Dónde Comprar

El ALFA AWUS036ACM está disponible en [yupitek.com](https://yupitek.com) — el distribuidor oficial de ALFA Network. Comprar a través de un distribuidor autorizado garantiza que recibes hardware genuino con la garantía estándar de Alfa Network Inc.

**Página del producto:** [ALFA AWUS036ACM en Yupitek](https://yupitek.com)

Incluido en la caja:
- 1× Adaptador AWUS036ACM
- 2× Antenas dipolo de doble banda 5 dBi desmontables (RP-SMA)
- 1× Cable de extensión USB 3.0
- 1× CD de controladores (Windows)

---

## Resumen

| Característica | AWUS036ACM |
|---|---|
| Chipset | MediaTek MT7612U |
| WiFi | AC1200 (867 + 300 Mbps), doble banda |
| IBSS Ad Hoc | ✅ Todas las versiones de Raspberry Pi OS desde 2020 |
| Mesh 802.11s | ✅ Plug & play |
| Controlador en núcleo | ✅ mt76x2u (desde el núcleo 4.19) |
| Plug & Play en Pi | ✅ Sin instalación necesaria |
| Antenas desmontables | ✅ 2× 5 dBi RP-SMA |
| Único modelo ALFA activo con IBSS + Mesh | ✅ Sí |

Si necesitas construir una red inalámbrica entre nodos Raspberry Pi — ya sea un enlace directo entre dos dispositivos o una malla multi-salto autorreparable — el ALFA AWUS036ACM es el adaptador que lo hace posible.

---

*Artículo del Equipo Técnico de Yupitek · [yupitek.com](https://yupitek.com)*

*Referencias: [Documentación Oficial de Alfa Network](https://docs.alfa.com.tw/Product/AWUS036ACM/) · [Linux Wireless Wiki — Tipos de Interfaz](https://wireless.wiki.kernel.org/en/users/documentation/iw/vif) · [Controlador Linux MediaTek mt76](https://wireless.wiki.kernel.org/en/users/drivers/mediatek) · [Lista de Controladores En-Núcleo USB-WiFi de morrownr](https://github.com/morrownr/USB-WiFi)*
