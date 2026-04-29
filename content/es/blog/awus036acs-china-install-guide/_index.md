---
title: "Guía de instalación del controlador ALFA AWUS036ACS para China: Kali Linux, Ubuntu, Debian y Raspberry Pi"
description: "Guía paso a paso para instalar los controladores ALFA AWUS036ACS en China utilizando espejos domésticos. Controlador DKMS RTL8811AU, modo monitor completo e inyección de paquetes. Cubre Kali Linux, Ubuntu 22/24, Debian y Raspberry Pi. No se requiere GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acs-china-install-guide"
tags: ["alfa", "awus036acs", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "rtl8811au"]
categories: ["Guías de controladores"]
series: ["alfa-china-install-guide"]
related_product: "/es/products/alfa/awus036acs/"
series_order: 3
---

El AWUS036ACS es el adaptador de investigación de seguridad de doble banda compacto de ALFA. Su chip RTL8811AU admite el modo monitor completo y la inyección de paquetes en Kali Linux, pero debido a que el controlador está fuera del kernel, debes compilarlo desde el código fuente. En China, GitHub está bloqueado, por lo que esta guía utiliza exclusivamente espejos de Gitee. No se requiere GitHub.

## Antes de comenzar

Asegúrate de tener esto listo:

1. Adaptador **ALFA AWUS036ACS**
2. Cable USB (USB-A 2.0, el que viene en la caja funciona bien)
3. Conexión a internet activa para llegar a los espejos domésticos

Enchufa el adaptador y luego confirma que tu sistema lo ve:

```bash
lsusb
```

Busca esto en la salida:

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
```

Si ves `0bda:0811`, el adaptador ha sido detectado. Pasa a la sección de tu sistema operativo a continuación.

## Elige tu sistema operativo

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

¿Ya lo instalaste? Salta a:

- [Habilitar el modo monitor](#habilitar-el-modo-monitor)
- [Probar la inyección de paquetes](#probar-la-inyeccion-de-paquetes)
- [Passthrough USB de máquina virtual](#passthrough-usb-de-maquina-virtual)

---

## Kali Linux

### Paso 1: Cambiar al espejo de China

```bash
sudo nano /etc/apt/sources.list
```

Borra lo que haya allí y luego pega:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Guarda con **Ctrl+O**, Enter, luego **Ctrl+X**. Actualiza:

```bash
sudo apt update
```

> **Espejo de respaldo:** `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Paso 2: Instalar dependencias de compilación

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### Paso 3: Clonar el controlador desde Gitee

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
```

> **NOTA:** Si esa URL de Gitee no carga, busca en Gitee `8821au` y elige el fork actualizado más recientemente. También puedes descargar archivos de controladores desde [files.alfa.com.tw](https://files.alfa.com.tw).

---

### Paso 4: Compilar e instalar

```bash
sudo ./install-driver.sh
sudo reboot
```

Después del reinicio, verifica que el controlador se haya cargado.

```bash
lsmod | grep 88XXau
```

Deberías ver un módulo `88XXau` en la lista. Luego confirma que apareció la interfaz.

```bash
iwconfig
```

Busca `wlan0` o `wlan1`.

---

### Paso 5: Habilitar el modo monitor {#habilitar-el-modo-monitor}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Confirma con `iwconfig`: busca `wlan1mon` con `Mode:Monitor`.

---

### Paso 6: Probar la inyección de paquetes {#probar-la-inyeccion-de-paquetes}

```bash
sudo aireplay-ng --test wlan1mon
```

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

---

## Ubuntu 22.04 / 24.04

### Paso 1: Cambiar al espejo de China

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Borra todo y pega:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

Reemplaza todas las líneas con:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
```

---

### Paso 2: Instalar dependencias de compilación

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

---

### Paso 3: Clonar e instalar el controlador desde Gitee

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

---

### Paso 4: Habilitar el modo monitor

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

---

### Paso 5: Probar la inyección de paquetes

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Debian

### Paso 1: Cambiar al espejo de China

```bash
sudo nano /etc/apt/sources.list
```

Pega (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Paso 2: Instalar dependencias de compilación

```bash
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
```

### Paso 3: Clonar e instalar

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### Paso 4: Habilitar el modo monitor

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Confirma: `iwconfig` → busca `wlan1mon` con `Mode:Monitor`.

### Paso 5: Probar la inyección de paquetes

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Raspberry Pi 4B / 5

### Paso 1: Descargar y flashear Kali ARM64

Oficial: https://www.kali.org/get-kali/#kali-arm — elige Raspberry Pi 4/5 64-bit.

Espejo de China: https://repo.huaweicloud.com/kali-images/

```bash
lsblk
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Credenciales por defecto: **kali / kali**.

### Paso 2: Cambiar al espejo de China

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### Paso 3: Instalar dependencias de compilación

```bash
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
```

### Paso 4: Clonar e instalar el controlador

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### Paso 5: Habilitar el modo monitor

En una Pi con Wi-Fi integrado, el AWUS036ACS aparece como `wlan1`.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

### Paso 6: Probar la inyección de paquetes

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Passthrough USB de máquina virtual {#virtual-machine-usb-passthrough}

### VirtualBox

1. Apaga la VM → **Configuración → USB** → Habilita **Controlador USB 2.0**.
2. Haz clic en **+** → Selecciona: **Realtek** (ID: 0bda:0811).
3. Inicia la VM. Ejecuta `lsusb` para confirmar `0bda:0811`, luego sigue los pasos de Kali anteriores.

### VMware Fusion / Workstation

1. **Máquina virtual → USB y Bluetooth** → Busca **Realtek 8811AU** → **Conectar**.
2. Ejecuta `lsusb` para confirmar, luego sigue los pasos de Kali anteriores.

---

## Solución de problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| `lsusb` no muestra 0bda:0811 | El adaptador no tiene energía o el cable está mal | Prueba con un puerto USB diferente |
| `install-driver.sh` falla | Faltan los encabezados | Ejecuta `sudo apt install linux-headers-$(uname -r)` |
| La clonación de Gitee falla | Problema de red | Busca en gitee.com `8821au`, prueba con un fork diferente |
| `airmon-ng start` falla | NetworkManager se está ejecutando | Ejecuta `sudo airmon-ng check kill` primero |
| No hay tráfico en modo monitor | Canal incorrecto | Establece el canal: `iwconfig wlan1mon channel 6` |
| Inyección "No Answer" | El AP está demasiado lejos | Acércate. Usa `wlan1mon`, no `wlan1`. |

> **Nota sobre VIF:** El controlador RTL8811AU no admite interfaces virtuales (VIF). El modo monitor y administrado simultáneos no están disponibles en este adaptador.

## Referencia de espejos de China

| Recurso | URL | Uso para |
|---------|-----|----------|
| Controladores oficiales de Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquetes de controladores |
| Documentación de Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Manuales de productos |
| Controlador 8821au (Gitee) | [gitee.com/mirrors/8821au](https://gitee.com/mirrors/8821au) | Controlador RTL8811AU |
| Espejo de la Universidad de Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Espejo de Alibaba Cloud | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recomendado) |
| Espejo de la USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recomendado) |
| Espejo de Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Imágenes Kali ARM |

## Más guías de adaptadores Alfa para China

- [Guía de instalación de AWUS036ACH en China](/es/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potencia
- [Guía de instalación de AWUS036ACM en China](/es/blog/awus036acm-china-install-guide/) — MT7612U, VIF completo
- AWUS036ACS ← estás aquí
- [Guía de instalación de AWUS036AX en China](/es/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [Guía de instalación de AWUS036AXER en China](/es/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [Guía de instalación de AWUS036AXM en China](/es/blog/awus036axm-china-install-guide/) — MT7921AUN, forma en L
- [Guía de instalación de AWUS036AXML en China](/es/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [Guía de instalación de AWUS036EACS en China](/es/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

¿Preguntas? Deja un comentario a continuación o contáctanos en [yupitek.com](https://yupitek.com/es/contact/).
