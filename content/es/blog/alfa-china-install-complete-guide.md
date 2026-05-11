---
title: "Guía completa: Instalación de todos los adaptadores WiFi USB Alfa en Linux desde China - Kali, Ubuntu, Raspberry Pi"
date: 2026-04-24
draft: false
slug: "alfa-china-install-complete-guide"
tags: ["alfa", "kali-linux", "ubuntu", "raspberry-pi", "driver", "china", "monitor-mode", "packet-injection", "wireless"]
categories: ["Guías de drivers"]
series: ["alfa-china-install-guide"]
series_order: 9
description: "La guía definitiva para instalar todos los adaptadores WiFi USB Alfa en Linux desde China. Cubre Kali Linux, Ubuntu 22/24, Debian y Raspberry Pi. Sin necesidad de GitHub - solo mirrors nacionales."
---

## Bienvenido a la guía definitiva de instalación de Alfa en Linux

Si estás leyendo esto, probablemente compraste un adaptador WiFi USB Alfa y te encontraste atascado porque:

- Estás en China y no puedes acceder a GitHub
- La instalación del driver parece complicada
- Necesitas habilitar el modo monitor y la inyección de paquetes para pruebas inalámbricas
- No sabes qué driver necesita tu modelo específico de Alfa

Esta guía resuelve **todos esos problemas**. Te llevaremos paso a paso por la instalación de **todos los adaptadores WiFi USB Alfa** en **las principales distribuciones Linux**, usando únicamente **mirrors accesibles desde China**. Sin GitHub. Sin frustraciones.

---

## Por qué existe esta guía

Los adaptadores WiFi USB Alfa son muy populares entre los testers de penetración, ingenieros de redes y entusiastas de las redes inalámbricas. Admiten el modo monitor y la inyección de paquetes — funciones que la mayoría de los adaptadores WiFi de consumo no ofrecen.

Pero aquí está el problema: **La mayoría de las guías de instalación de drivers asumen que puedes acceder a GitHub**. Si estás en China, eso no es posible. Esta guía está diseñada específicamente para usuarios en China, usando únicamente mirrors y recursos que funcionan dentro de la infraestructura de internet del país.

---

## Referencia rápida de modelos

Antes de comenzar, identifiquemos qué adaptador Alfa tienes y qué chip usa:

### Serie AX (Wi-Fi 6 / 802.11ax)

| Modelo | Chipset | Driver | Ideal para |
|-------|---------|--------|----------|
| AWUS036AX | Realtek RTL8832BU | `rtl8832bu` | Uso general, buen alcance |
| AWUS036AXM | Realtek RTL8832BU | `rtl8832bu` | Diseño compacto |
| AWUS036AXML | Realtek RTL8832BU | `rtl8832bu` | Ultra-compacto |
| AWUS036AXER | Realtek RTL8832BU | `rtl8832bu` | Potencia mejorada |

### Serie AC (Wi-Fi 5 / 802.11ac)

| Modelo | Chipset | Driver | Ideal para |
|-------|---------|--------|----------|
| AWUS036ACH | Realtek RTL8812AU | `88XXau` | Alta potencia, gran alcance |
| AWUS036ACM | MediaTek MT7612U | `mt76x2u` | **Mejor soporte VIF**, plug-and-play |
| AWUS036ACS | Realtek RTL8811AU | `8811au` | Opción económica |

### ¿Qué adaptador tienes?

1. Mira la etiqueta en tu adaptador
2. Revisa la caja en la que vino
3. Si lo compraste en línea, consulta tu historial de pedidos

Una vez que conozcas tu modelo, ve directamente a esa sección más abajo o sigue el flujo de trabajo general.

---

## Antes de empezar: Lo que necesitas

Asegúrate de tener todo esto listo antes de comenzar:

1. **Adaptador WiFi USB Alfa** — El modelo correcto para tus necesidades
2. **Cable USB** — El que vino en la caja funciona perfectamente
3. **Hub USB con alimentación** — Necesario si usas Raspberry Pi
4. **Conexión a internet activa** — Para acceder a los mirrors nacionales en China
5. **Privilegios de sudo** — Necesitarás acceso de administrador para instalar los drivers

Conecta el adaptador primero para verificar que tu sistema lo detecta:

```bash
lsusb
```

Busca el vendor ID de tu adaptador en la salida:

- **Los adaptadores Alfa** aparecen como `0e8d` (MediaTek) o `0bda` (Realtek)
- Ejemplo: `Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.`
- Ejemplo: `Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.`

Si ves el ID, tu adaptador ha sido detectado. Pasa a la sección de instalación del driver.

Si no lo ves, prueba con un puerto USB diferente, cambia el cable y ejecuta `lsusb` de nuevo.

---

## Elige tu sistema operativo

Ve directamente a la sección correspondiente a tu OS:

- [Kali Linux](#instalación-en-kali-linux)
- [Ubuntu 22.04 / 24.04](#instalación-en-ubuntu-2204--2404)
- [Debian 12 (Bookworm)](#instalación-en-debian-12-bookworm)
- [Raspberry Pi OS (64-bit)](#instalación-en-raspberry-pi-os)

¿Ya tienes el driver instalado? Salta a las secciones avanzadas:

- [Habilitar modo monitor](#habilitar-el-modo-monitor-en-cualquier-adaptador)
- [Probar inyección de paquetes](#probar-la-inyección-de-paquetes)
- [Soporte de interfaz virtual (VIF)](#soporte-de-interfaz-virtual-vif)
- [Paso de USB a máquinas virtuales](#paso-de-usb-a-máquinas-virtuales)

---

## Referencia de mirrors accesibles desde China

Todos los recursos de esta guía usan los siguientes mirrors accesibles desde China:

| Recurso | URL | Para qué se usa |
|----------|-----|---------|
| **Descargas oficiales Alfa** | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquetes de drivers, firmware |
| **Documentación Alfa** | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Manuales de productos, en inglés |
| **清华大学镜像 (Tsinghua)** | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| **阿里云镜像 (Aliyun)** | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recomendado) |
| **中科大镜像 (USTC)** | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recomendado) |
| **华为云镜像** | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Imágenes Kali ARM (alternativa) |
| **Gitee (alternativa a GitHub)** | [gitee.com](https://gitee.com) | Código fuente de drivers |

---

## Instalación en Kali Linux

Kali Linux viene con las herramientas inalámbricas preinstaladas. Hacer que los adaptadores Alfa funcionen solo requiere unos pocos pasos.

### Paso 1: Cambiar al mirror de China

Abre tu lista de fuentes:

```bash
sudo nano /etc/apt/sources.list
```

Reemplaza todo el contenido con esto:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Guarda: **Ctrl+O**, Enter, luego **Ctrl+X**. Actualiza:

```bash
sudo apt update
```

> **Mirror alternativo:** Si 中科大 (USTC) es lento, usa 清华 (Tsinghua):
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

### Paso 2: Instalar el driver según el chipset

#### Serie AX (RTL8832BU)

```bash
sudo apt install -y rtl8832bu-dkms
```

#### Serie AC - Realtek (RTL8812AU / RTL8811AU)

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### Serie AC - MediaTek (MT7612U)

El driver MT7612U está integrado en el kernel de Kali. Verifica que esté cargado:

```bash
lsmod | grep mt76
```

Si ves `mt76x2u`, ya terminaste. Si no:

```bash
sudo modprobe mt76x2u
```

### Paso 3: Verificar que el driver está cargado

Ejecuta `lsusb` de nuevo. Tu adaptador debería aparecer. Luego comprueba las interfaces inalámbricas:

```bash
iwconfig
```

Busca `wlan0` o `wlan1`. Si la interfaz aparece, el driver está funcionando.

### Paso 4: Habilitar el modo monitor

Detén los procesos que interfieren:

```bash
sudo airmon-ng check kill
```

Inicia el modo monitor:

```bash
sudo airmon-ng start wlan0
```

Verifica:

```bash
iwconfig
```

Busca `wlan0mon` con `Mode:Monitor`. ¡Listo!

---

## Instalación en Ubuntu 22.04 / 24.04

### Paso 1: Cambiar al mirror de China

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Reemplaza con:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Guarda con **Ctrl+O**, sal con **Ctrl+X**.

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

Reemplaza con:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Guarda y sal.

#### Actualizar el índice de paquetes

```bash
sudo apt update
```

### Paso 2: Instalar dependencias de compilación

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### Paso 3: Instalar el driver

#### Serie AX (RTL8832BU)

Clona desde Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### Serie AC - Realtek (RTL8812AU)

Clona desde Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### Serie AC - MediaTek (MT7612U)

El driver está integrado en el kernel de Ubuntu. Cárgalo:

```bash
sudo modprobe mt76x2u
```

### Paso 4: Habilitar el modo monitor

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

Busca `wlan0mon` con `Mode:Monitor`.

---

## Instalación en Debian 12 (Bookworm)

### Paso 1: Cambiar al mirror de China

```bash
sudo nano /etc/apt/sources.list
```

Reemplaza con:

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Guarda y sal. Actualiza:

```bash
sudo apt update
```

### Paso 2: Instalar firmware no libre

```bash
sudo apt install -y firmware-misc-nonfree
```

### Paso 3: Instalar dependencias de compilación

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### Paso 4: Instalar el driver

#### Serie AX (RTL8832BU)

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### Serie AC - Realtek (RTL8812AU)

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### Serie AC - MediaTek (MT7612U)

```bash
sudo modprobe mt76x2u
```

### Paso 5: Instalar Aircrack-ng

```bash
sudo apt install -y aircrack-ng
```

### Paso 6: Habilitar el modo monitor

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

Busca `wlan0mon` con `Mode:Monitor`.

---

## Instalación en Raspberry Pi OS

> **IMPORTANTE:** El AWUS036ACH consume ~500mW. El AWUS036ACM consume ~400mW. **Usa siempre un hub USB con alimentación** para evitar que la Pi se limite o se cuelgue bajo carga.

### Paso 1: Descargar la imagen Kali Linux ARM64

Ve a: https://www.kali.org/get-kali/#kali-arm

Elige **Raspberry Pi 4 (64-bit)** o **Raspberry Pi 5 (64-bit)**. NO uses 32-bit — se requiere 64-bit.

> **Mirror de China:** Si kali.org es lento, usa 华为云: https://repo.huaweicloud.com/kali-images/

### Paso 2: Grabar en MicroSD

Comprueba la ruta de tu tarjeta SD:

```bash
lsblk
```

Graba la imagen (reemplaza `/dev/sdX` con la ruta real de tu tarjeta):

```bash
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Espera a que `sync` finalice. Arranca la Pi. Credenciales predeterminadas: **kali / kali**.

### Paso 3: Cambiar al mirror de China

```bash
sudo nano /etc/apt/sources.list
```

Reemplaza con:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Guarda y aplica:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### Paso 4: Instalar el driver

#### Serie AX (RTL8832BU)

```bash
sudo apt install -y rtl8832bu-dkms
```

#### Serie AC - Realtek (RTL8812AU)

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### Serie AC - MediaTek (MT7612U)

```bash
sudo modprobe mt76x2u
```

### Paso 5: Habilitar el modo monitor

En una Pi con Wi-Fi integrado, el adaptador Alfa aparece como `wlan1`:

```bash
iwconfig
```

Luego:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
iwconfig
```

Busca `wlan1mon` con `Mode:Monitor`.

---

## Habilitar el modo monitor en cualquier adaptador

Una vez instalado el driver, habilitar el modo monitor es sencillo:

### Paso 1: Verificar el nombre de tu interfaz

```bash
iwconfig
```

Anota si es `wlan0` o `wlan1`.

### Paso 2: Detener los procesos que interfieren

```bash
sudo airmon-ng check kill
```

### Paso 3: Iniciar el modo monitor

```bash
sudo airmon-ng start wlan0
```

Reemplaza `wlan0` con el nombre real de tu interfaz si es diferente.

### Paso 4: Verificar

```bash
iwconfig
```

Busca tu interfaz terminada en `mon` (como `wlan0mon`) con `Mode:Monitor`.

---

## Probar la inyección de paquetes

Esto confirma que tu adaptador puede enviar paquetes fabricados — esencial para las pruebas inalámbricas.

```bash
sudo aireplay-ng --test wlan0mon
```

**Una respuesta exitosa se ve así:**

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

**Si falla:**
- Reinicia y vuelve a intentarlo
- Confirma que ningún otro proceso tiene la interfaz (`iwconfig`)
- Acércate más a un AP WiFi para la prueba
- Asegúrate de usar `wlan0mon`, no `wlan0`

---

## Soporte de interfaz virtual (VIF)

VIF (Virtual Interface Functionality) te permite ejecutar múltiples interfaces en un solo adaptador de forma simultánea. Por ejemplo:

- **Modo administrado** (`wlan0`) + **Modo monitor** (`mon0`) al mismo tiempo
- Funcionar mientras sigues conectado a una red Y capturando tráfico

### ¿Qué adaptadores admiten VIF?

| Chipset | Soporte VIF | Notas |
|---------|-------------|-------|
| **MT7612U (AWUS036ACM)** | ✅ Soporte nativo completo | Mejor opción para flujos de trabajo VIF |
| **RTL8812AU (AWUS036ACH)** | ⚠️ Limitado | No puede ejecutar modo administrado + monitor simultáneamente |
| **RTL8832BU (serie AX)** | ⚠️ Limitado | Consulta la documentación del modelo específico |

### Crear una interfaz virtual (MT7612U)

Si tienes el AWUS036ACM (MT7612U):

```bash
# Crear interfaz monitor mientras wlan0 permanece en modo administrado
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

Verifica que ambas interfaces estén activas:

```bash
iwconfig
```

Deberías ver:
- `wlan0` — modo administrado (asociado al AP)
- `mon0` — modo monitor (capturando todo el tráfico)

### Casos de uso

**Capturar tráfico mientras permaneces conectado:**

```bash
sudo airodump-ng mon0
```

Tu `wlan0` continúa funcionando con normalidad mientras `mon0` captura todo.

**AP falso + Monitor:**

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

---

## Paso de USB a máquinas virtuales

¿Ejecutas Linux dentro de una VM? Necesitas pasar el adaptador USB al sistema invitado.

### VirtualBox

1. Apaga la VM
2. Ve a **Configuración → USB**
3. Habilita el **controlador USB 3.0 (xHCI)**
4. Haz clic en **+** para añadir un filtro USB
5. Selecciona tu adaptador Alfa (ID: `0bda:8812` o `0e8d:7612`)
6. Inicia la VM

Dentro de la VM, ejecuta `lsusb` para confirmar y luego sigue los pasos de Kali Linux anteriores.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Inicia la VM
2. Menú: **Virtual Machine → USB & Bluetooth**
3. Encuentra tu adaptador Alfa y haz clic en **Connect**
4. El adaptador aparece dentro de la VM

Ejecuta `lsusb` para confirmar y luego sigue los pasos de instalación del driver.

---

## Solución de problemas

| Problema | Causa probable | Solución |
|---------|-------------|-----|
| `lsusb` no muestra el ID del adaptador | Cable defectuoso o sin alimentación | Prueba con otro puerto USB. Usa hub con alimentación en la Pi. |
| `modprobe` dice "Module not found" | Módulos del kernel faltantes | Ejecuta `sudo apt install linux-modules-extra-$(uname -r)` |
| El driver funciona pero no cambia a modo monitor | NetworkManager interfiere | Ejecuta `sudo airmon-ng check kill` primero |
| El modo monitor inicia pero no captura nada | Interfaz o canal incorrecto | Ejecuta `iwconfig`. Establece el canal: `iwconfig wlan0mon channel 6` |
| La prueba de inyección falla | Usando la interfaz incorrecta | Usa `wlan0mon`, no `wlan0` |
| La creación de VIF falla | Driver no completamente cargado | Desconecta y vuelve a conectar el adaptador, o recarga el módulo |

---

## Apéndice: Lista completa de modelos Alfa

| Modelo | Chipset | Driver | Fuente del mirror en China |
|-------|---------|--------|---------------------|
| AWUS036ACH | RTL8812AU | `88XXau` | Gitee: mirrors/rtl8812au |
| AWUS036ACM | MT7612U | `mt76x2u` | Driver integrado en el kernel |
| AWUS036ACS | RTL8811AU | `8811au` | Gitee: mirrors/rtl8811au |
| AWUS036AX | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXM | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXML | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXER | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036EAC | RTL8814AU | `8814au` | Gitee: mirrors/rtl8814au |

---

## Notas finales

Esta guía cubre **todos los adaptadores WiFi USB Alfa** en **las principales distribuciones Linux**, usando **únicamente recursos accesibles desde China**. Ahora deberías poder:

✅ Instalar drivers para cualquier adaptador Alfa  
✅ Habilitar el modo monitor en Kali, Ubuntu, Debian o Raspberry Pi  
✅ Probar la inyección de paquetes  
✅ Usar interfaces virtuales (VIF) con los modelos compatibles  
✅ Pasar adaptadores a máquinas virtuales  

**¿Preguntas o problemas?** Consulta las guías específicas de cada modelo en nuestra serie, o contáctanos en [yupitek.com](https://yupitek.com/es/contact/).

---

## Guías relacionadas

Esta es parte de la serie **Alfa China Install Guide**:

- [Guía de instalación AWUS036ACH desde China](/es/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potencia
- [Guía de instalación AWUS036ACM desde China](/es/blog/awus036acm-china-install-guide/) — MT7612U, mejor soporte VIF
- [Guía de instalación AWUS036ACS desde China](/es/blog/awus036acs-china-install-guide/) — RTL8811AU, opción económica
- [Guía de instalación AWUS036AX desde China](/es/blog/awus036ax-china-install-guide/) — Wi-Fi 6, RTL8832BU
- [Guía de instalación AWUS036AXM desde China](/es/blog/awus036axm-china-install-guide/) — Wi-Fi 6, diseño compacto
- [Guía de instalación AWUS036AXML desde China](/es/blog/awus036axml-china-install-guide/) — Wi-Fi 6, ultra-compacto
- [Guía de instalación AWUS036AXER desde China](/es/blog/awus036axer-china-install-guide/) — Wi-Fi 6, potencia mejorada
- [Guía de instalación AWUS036EAC desde China](/es/blog/awus036eacs-china-install-guide/) — RTL8814AU, alta potencia

---

*Última actualización: 24 de abril de 2026*
