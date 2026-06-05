---
title: "Guía de instalación del controlador ALFA AWUS036AXER para China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Guía paso a paso para instalar los controladores ALFA AWUS036AXER en China utilizando espejos domésticos. Controlador RTL8832BU, adaptador WiFi 6 nano. Cubre Kali Linux, Ubuntu 22/24 (integrado en 24.04), Debian y Raspberry Pi. No se requiere GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axer-china-install-guide"
tags: ["alfa", "awus036axer", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 5
related_product: "/es/products/alfa/awus036axer/"
featureimage: "/images/blog/awus036axer-china-install-guide.webp"
---

El AWUS036AXER es el adaptador WiFi 6 nano de ALFA: un dongle compacto diseñado para permanecer conectado permanentemente a una computadora portátil. Su chip RTL8832BU está fuera del núcleo en versiones de Linux inferiores a 6.14, pero se incluye de forma nativa en Ubuntu 24.04 (núcleo 6.8). Esta guía utiliza espejos de Gitee para núcleos más antiguos. No se requiere GitHub.

> **Nota de investigación de seguridad:** El RTL8832BU tiene soporte limitado para el modo monitor. Los resultados varían según la versión del núcleo y del controlador. Para una inyección de paquetes confiable en Kali Linux, el [AWUS036ACM](/es/blog/awus036acm-china-install-guide/) o el [AWUS036ACH](/es/blog/awus036ach-china-install-guide/) son mejores opciones.

> **Nota sobre el alcance:** El AWUS036AXER tiene una antena integrada no extraíble. Para la investigación de seguridad, los adaptadores con antenas RP-SMA externas (AWUS036ACH, AWUS036ACM) proporcionan un alcance significativamente mejor.

## Antes de comenzar

1. Adaptador **ALFA AWUS036AXER**
2. Cable USB-A
3. Conexión a internet activa

```bash
lsusb
```

Busque:

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## Elija su sistema operativo

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

### Paso 1: Cambiar al espejo de China

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Paso 2: Instalar dependencias de compilación

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

### Paso 3: Clonar el controlador desde Gitee

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

> **NOTA:** Si esa URL de Gitee no carga, busque en Gitee `rtl8852bu` y elija el fork actualizado más recientemente. También puede descargar archivos desde [files.alfa.com.tw](https://files.alfa.com.tw).

### Paso 4: Compilar e instalar

```bash
sudo ./install-driver.sh
sudo reboot
```

Verifique que el controlador se haya cargado:

```bash
lsmod | grep 88x2bu
iwconfig
```

### Paso 5: Activar el modo monitor {#enable-monitor-mode}

> **Nota:** El soporte del modo monitor es limitado en el RTL8832BU. Los siguientes comandos funcionan en la mayoría de las configuraciones, pero los resultados pueden variar.

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### Paso 6: Probar la inyección de paquetes {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

Si la inyección no es confiable, considere el [AWUS036ACM](/es/blog/awus036acm-china-install-guide/) para trabajos de pruebas de penetración.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — controlador en el núcleo, no se necesita Gitee

Ubuntu 24.04 incluye el núcleo 6.8, que contiene el controlador RTL8832BU de forma nativa.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```bash
sudo apt update
sudo modprobe 88x2bu
iwconfig
```

Si el módulo se carga y aparece una interfaz, ha terminado. Continúe con los pasos del modo monitor anteriores.

---

### Ubuntu 22.04 (Jammy) — se requiere DKMS

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

Active el modo monitor igual que en los pasos de Kali anteriores.

---

## Raspberry Pi 4B / 5

Cambie al espejo de China primero:

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Passthrough USB de máquina virtual {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Configuración → USB** → Habilitar **USB 3.0 (xHCI)**.
2. Agregar filtro: **Realtek** (ID: 0bda:885a).
3. Iniciar VM → `lsusb` para confirmar → seguir los pasos de Kali.

### VMware

1. **Máquina virtual → USB y Bluetooth** → Buscar **Realtek RTL8832BU** → **Conectar**.
2. `lsusb` para confirmar → seguir los pasos de Kali.

---

## Solución de problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| `lsusb` no muestra 0bda:885a | Adaptador no detectado | Pruebe con un puerto USB diferente |
| `install-driver.sh` falla | Faltan encabezados | `sudo apt install linux-headers-$(uname -r)` |
| La clonación de Gitee falla | Problema de red | Busque en gitee.com `rtl8852bu` |
| Ubuntu 24.04: `modprobe 88x2bu` falla | El módulo no está presente | Instale `linux-modules-extra-$(uname -r)` |
| Modo monitor poco confiable | Limitación de RTL8832BU | Use AWUS036ACM para trabajos de pentest |

> **Nota sobre VIF:** El controlador fuera del núcleo RTL8832BU no admite interfaces virtuales (VIF).

## Referencia de espejos en China

| Recurso | URL | Uso para |
|---------|-----|---------|
| Controladores oficiales de Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquetes de controladores |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | Controlador RTL8832BU |
| Espejo de la Universidad de Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Espejo de Alibaba Cloud | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| Espejo de USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| Espejo de Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

## Más guías de adaptadores Alfa para China

- [Guía de instalación de AWUS036ACH en China](/es/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potencia
- [Guía de instalación de AWUS036ACM en China](/es/blog/awus036acm-china-install-guide/) — MT7612U, VIF completo
- [Guía de instalación de AWUS036ACS en China](/es/blog/awus036acs-china-install-guide/) — RTL8811AU, modo monitor
- [Guía de instalación de AWUS036AX en China](/es/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- AWUS036AXER ← estás aquí
- [Guía de instalación de AWUS036AXM en China](/es/blog/awus036axm-china-install-guide/) — MT7921AUN, forma en L
- [Guía de instalación de AWUS036AXML en China](/es/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [Guía de instalación de AWUS036EACS en China](/es/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

¿Preguntas? Deje un comentario a continuación o contáctenos en [yupitek.com](https://yupitek.com/es/contact/).
