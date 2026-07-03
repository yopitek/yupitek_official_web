---
title: "Guía de instalación del controlador ALFA AWUS036AX para China: Kali Linux, Ubuntu, Debian y Raspberry Pi"
description: "Guía paso a paso para instalar los controladores ALFA AWUS036AX en China utilizando espejos domésticos. Controlador RTL8832BU, WiFi 6 AX1800. Cubre Kali Linux, Ubuntu 22/24 (nativo en 24.04), Debian y Raspberry Pi. No se requiere GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Guías de controladores"]
series: ["alfa-china-install-guide"]
related_product: "/es/products/alfa/awus036ax/"
series_order: 4
featureimage: "/images/blog/awus036ax-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "¿Qué chip usa el AWUS036AX? ¿Admite WiFi 6?"
    answer: "Usa el chip Realtek RTL8832BU y admite WiFi 6 (802.11ax) de alta velocidad."
  - question: "¿El AWUS036AX necesita instalar controlador en Ubuntu 24.04?"
    answer: "No, el kernel de Ubuntu 24.04 ya admite nativamente RTL8832BU; es plug-and-play."
  - question: "¿El AWUS036AX es adecuado para investigación de seguridad inalámbrica?"
    answer: "No tanto. El soporte del modo monitor de RTL8832BU es limitado; se recomienda usar AWUS036ACM o AWUS036ACH."
  - question: "¿Hace falta VPN para instalar el AWUS036AX en China?"
    answer: "No, descarga el código fuente rtl8852bu desde Gitee e instala las herramientas de compilación con espejos nacionales."
  - question: "¿Cuál es el USB ID del AWUS036AX?"
    answer: "El USB ID de Realtek RTL8832BU es 0bda:8832, puedes confirmarlo con lsusb."
---

El AWUS036AX es el adaptador de doble banda WiFi 6 AX1800 de ALFA. Su chip RTL8832BU está fuera del kernel en versiones de Linux inferiores a 6.14, pero Ubuntu 24.04 (kernel 6.8) lo incluye de forma nativa. Esta guía utiliza espejos de Gitee para kernels más antiguos y el controlador integrado para Ubuntu 24.04. No se requiere GitHub.

{{< tldr >}}
El AWUS036AX usa el chip RTL8832BU y admite WiFi 6. En Ubuntu 24.04 funciona sin controlador; en Kali/Ubuntu 22.04 se descarga rtl8852bu desde Gitee y se compila.
{{< /tldr >}}

> **Nota de investigación de seguridad:** El RTL8832BU tiene un soporte limitado para el modo monitor. Los resultados varían según el kernel y la versión del controlador. Para una inyección de paquetes confiable en Kali Linux, el [AWUS036ACM](/es/blog/awus036acm-china-install-guide/) o el [AWUS036ACH](/es/blog/awus036ach-china-install-guide/) son mejores opciones.

## Antes de comenzar

1. Adaptador **ALFA AWUS036AX**
2. Cable USB-A
3. Conexión a internet activa

```bash
lsusb
```

Busca esto:

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## Elige tu sistema operativo

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

> **NOTA:** Si esa URL de Gitee no carga, busca en Gitee `rtl8852bu` y elige el fork actualizado más recientemente. También puedes descargar archivos desde [files.alfa.com.tw](https://files.alfa.com.tw).

### Paso 4: Compilar e instalar

```bash
sudo ./install-driver.sh
sudo reboot
```

Verifica que el controlador se haya cargado:

```bash
lsmod | grep 88x2bu
iwconfig
```

### Paso 5: Habilitar el modo monitor {#habilitar-el-modo-monitor}

> **Nota:** El soporte del modo monitor es limitado en el RTL8832BU. Los siguientes comandos funcionan en la mayoría de las configuraciones, pero los resultados pueden variar.

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### Paso 6: Probar la inyección de paquetes {#probar-la-inyeccion-de-paquetes}

```bash
sudo aireplay-ng --test wlan1
```

Si la inyección no es confiable, considera el [AWUS036ACM](/es/blog/awus036acm-china-install-guide/) para trabajos de pruebas de penetración.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — controlador en el kernel, no se necesita Gitee

Ubuntu 24.04 incluye el kernel 6.8, que contiene el controlador RTL8832BU de forma nativa.

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

Si el módulo se carga y aparece una interfaz, ya has terminado. Procede con los pasos del modo monitor anteriores.

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

Habilita el modo monitor siguiendo los mismos pasos de Kali anteriores.

---

## Raspberry Pi 4B / 5

Primero cambia al espejo de China:

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

1. **Configuración → USB** → Habilita **Controlador USB 3.0 (xHCI)**.
2. Añade un filtro: **Realtek** (ID: 0bda:885a).
3. Inicia la VM → `lsusb` para confirmar → sigue los pasos de Kali.

### VMware

1. **Máquina virtual → USB y Bluetooth** → Busca **Realtek RTL8832BU** → **Conectar**.
2. `lsusb` para confirmar → sigue los pasos de Kali.

---

## Solución de problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| `lsusb` no muestra 0bda:885a | Adaptador no detectado | Prueba con un puerto USB diferente |
| `install-driver.sh` falla | Faltan los encabezados | `sudo apt install linux-headers-$(uname -r)` |
| La clonación de Gitee falla | Problema de red | Busca en gitee.com `rtl8852bu` |
| Ubuntu 24.04: `modprobe 88x2bu` falla | El módulo no está presente | Instala `linux-modules-extra-$(uname -r)` |
| Modo monitor no confiable | Limitación del RTL8832BU | Usa el AWUS036ACM para trabajos de pentest |

> **Nota sobre VIF:** El controlador del RTL8832BU fuera del kernel no admite interfaces virtuales (VIF).

## Referencia de espejos de China

| Recurso | URL | Uso para |
|---------|-----|----------|
| Controladores oficiales de Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquetes de controladores |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | Controlador RTL8832BU |
| Espejo de la Universidad de Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Espejo de Alibaba Cloud | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| Espejo de la USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| Espejo de Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

{{< faq >}}

## Más guías de adaptadores Alfa para China

- [Guía de instalación de AWUS036ACH en China](/es/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potencia
- [Guía de instalación de AWUS036ACM en China](/es/blog/awus036acm-china-install-guide/) — MT7612U, VIF completo
- [Guía de instalación de AWUS036ACS en China](/es/blog/awus036acs-china-install-guide/) — RTL8811AU, modo monitor
- AWUS036AX ← estás aquí
- [Guía de instalación de AWUS036AXER en China](/es/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [Guía de instalación de AWUS036AXM en China](/es/blog/awus036axm-china-install-guide/) — MT7921AUN, forma en L
- [Guía de instalación de AWUS036AXML en China](/es/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [Guía de instalación de AWUS036EACS en China](/es/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

¿Preguntas? Deja un comentario a continuación o contáctanos en [yupitek.com](https://yupitek.com/es/contact/).

## Referencias

1. [Sitio oficial de Realtek](https://www.realtek.com/)
2. [Sitio oficial de ALFA Network](https://www.alfa.com.tw/)
3. [Documentación oficial de Kali Linux](https://www.kali.org/docs/)
4. [Espejo de rtl8852bu en Gitee](https://gitee.com/mirrors/rtl8852bu)
