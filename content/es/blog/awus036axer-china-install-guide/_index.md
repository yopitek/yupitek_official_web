---
title: "Guía de instalación del controlador ALFA AWUS036AXER para China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Guía paso a paso para instalar los controladores ALFA AWUS036AXER en China utilizando espejos domésticos. Controlador RTL8832BU, adaptador WiFi 6 nano. Cubre Kali Linux, Ubuntu 22/24 (DKMS), Debian y Raspberry Pi."
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
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "¿Qué chip usa el AWUS036AXER? ¿Es igual que el AWUS036AX?"
    answer: "Usa el mismo chip Realtek RTL8832BU y admite WiFi 6, pero con un tamaño más pequeño y portátil."
  - question: "¿El AWUS036AXER necesita instalar controlador en Ubuntu 24.04?"
    answer: "Depende de tu kernel. El kernel de Linux 6.17 y posterior (por ejemplo Ubuntu 24.04 HWE / kernel 6.17) incluye el controlador rtw89_8852bu en el propio kernel: plug-and-play, sin DKMS. Solo en kernels anteriores a 6.17 hay que compilar una vez el controlador comunitario rtl8852bu (morrownr/rtl8852bu-20250826) con DKMS. Comprueba primero con uname -r."
  - question: "¿El AWUS036AXER es adecuado para investigación de seguridad inalámbrica?"
    answer: "Sí. Con el controlador rtw89_8852bu integrado en el kernel 6.17+, el modo monitor y la inyección de paquetes funcionan en nuestras pruebas (Ubuntu 24.04 / kernel 6.17: inyección al 73% en 2,4 GHz y una captura WPA .22000 de extremo a extremo). Nota: en kernels anteriores que usan el controlador comunitario con DKMS, la compatibilidad con el modo monitor puede estar limitada. Solo en redes que poseas o estés autorizado a probar."
  - question: "¿Cuál es el USB ID del AWUS036AXER?"
    answer: "El ID de fabricante del Realtek RTL8832BU es 0bda. El ID de producto es 8832 o 885a según la unidad; confírmalo con lsusb."
  - question: "¿Hace falta VPN para instalar el AWUS036AXER en China?"
    answer: "No necesariamente. Clona el controlador desde el repositorio de GitHub verificado (morrownr/rtl8852bu-20250826); si GitHub va lento, usa un proxy o espejo de confianza. Las herramientas de compilación se pueden seguir instalando con espejos nacionales."
---

El AWUS036AXER es el adaptador WiFi 6 nano de ALFA: un dongle compacto diseñado para permanecer conectado permanentemente a una computadora portátil. Su chip RTL8832BU es compatible con el **controlador rtw89_8852bu integrado en el kernel de Linux 6.17 y posterior** (por ejemplo Ubuntu 24.04 HWE / kernel 6.17): plug-and-play, sin compilar. Solo en **kernels anteriores** (inferiores a 6.17) hay que compilar una vez el controlador comunitario rtl8852bu con DKMS. Esta guía cubre ambos casos. El código fuente del controlador se clona desde el repositorio de GitHub verificado; si GitHub va lento, usa un proxy o espejo de confianza.

{{< tldr >}}
El AWUS036AXER usa el chipset RTL8832BU con WiFi 6. El kernel 6.17+ (incluido Ubuntu 24.04 / kernel 6.17) trae el controlador rtw89_8852bu integrado en el kernel: sin DKMS, con modo monitor e inyección funcionando en las pruebas. Los kernels anteriores necesitan el controlador comunitario rtl8852bu mediante DKMS.
{{< /tldr >}}

> **Nota sobre investigación de seguridad:** Con el **controlador rtw89_8852bu integrado en el kernel 6.17+**, el modo monitor y la inyección de paquetes del AWUS036AXER funcionan en las pruebas (Ubuntu 24.04 / kernel 6.17: inyección al 73% en 2,4 GHz, captura WPA .22000 de extremo a extremo). Solo en kernels anteriores que usan el controlador comunitario con DKMS está limitada la compatibilidad con el modo monitor. Comprueba primero con `uname -r`. Solo en redes que poseas o estés autorizado a probar.

> **Nota sobre el alcance:** El AWUS036AXER tiene una antena integrada no extraíble. Para la investigación de seguridad, los adaptadores con antenas RP-SMA externas (AWUS036ACH, AWUS036ACM) proporcionan un alcance significativamente mejor.

## Antes de comenzar

1. Adaptador **ALFA AWUS036AXER**
2. Cable USB-A
3. Conexión a internet activa

```bash
lsusb
```

Busca una línea como esta (salida de ejemplo; el ID de fabricante siempre es `0bda` y el ID de producto es `8832` o `885a` según la unidad):

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

### Paso 3: Clonar el controlador desde GitHub

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
```

> **NOTA:** El controlador upstream mantenido es [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826). Si GitHub va lento, usa un proxy o espejo de confianza. También puedes descargar archivos desde [files.alfa.com.tw](https://files.alfa.com.tw).

### Paso 4: Compilar e instalar

```bash
sudo ./install-driver.sh
sudo reboot
```

Verifique que el controlador se haya cargado:

```bash
lsmod | grep 8852bu
iwconfig
```

### Paso 5: Activar el modo monitor {#enable-monitor-mode}

> **Funciona en el kernel 6.17+:** Con el controlador rtw89_8852bu integrado en el kernel, el modo monitor funciona:
> ```bash
> sudo nmcli dev set wlxXXXX managed no
> sudo ip link set wlxXXXX down
> sudo iw dev wlxXXXX set type monitor
> sudo ip link set wlxXXXX up
> ```
> En kernels anteriores que usan el controlador comunitario con DKMS, la compatibilidad con el modo monitor puede estar limitada: ahí puedes cambiar a un adaptador MediaTek integrado en el kernel, como el [AWUS036ACM](/es/blog/awus036acm-china-install-guide/).

### Paso 6: Probar la inyección de paquetes {#test-packet-injection}

> **Funciona en el kernel 6.17+:** Tras entrar en modo monitor, prueba la inyección con aireplay-ng (73% en 2,4 GHz en las pruebas):
> ```bash
> sudo iw dev wlxXXXX set channel 6
> sudo aireplay-ng --test wlxXXXX
> ```
> Solo en redes que poseas o estés autorizado a probar. En kernels anteriores donde el controlador comunitario con DKMS carece de modo monitor, la inyección tampoco está disponible.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble)

En Ubuntu 24.04, solo un **kernel HWE 6.17 o posterior** (por ejemplo, el HWE de 24.04.4) trae el controlador rtw89_8852bu integrado en el kernel: solo conecta el adaptador, sin compilar. En el **kernel GA 6.8** o el **kernel HWE 6.14** (ninguno incluye este controlador), cambia a un espejo doméstico y compila el controlador comunitario como en Ubuntu 22.04 más abajo, o actualiza a un kernel HWE 6.17 o posterior para obtener el controlador integrado.

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
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

Tras reiniciar, ejecuta `sudo modprobe 8852bu` e `iwconfig`. Si el módulo se carga y aparece una interfaz, has terminado. Nota: esta es la ruta del controlador comunitario con DKMS para kernels anteriores, donde la compatibilidad con el modo monitor puede estar limitada; en el kernel 6.17+ se usa el controlador rtw89_8852bu integrado, con el modo monitor y la inyección funcionando.

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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

Esta ruta compila el controlador comunitario con DKMS, necesaria solo en kernels anteriores a 6.17, donde la compatibilidad con el modo monitor puede estar limitada (consulta el paso 5 de Kali). En el kernel 6.17+ se usa el controlador rtw89_8852bu integrado, con el modo monitor y la inyección funcionando.

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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Passthrough USB de máquina virtual {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Configuración → USB** → Habilitar **USB 3.0 (xHCI)**.
2. Agregar filtro: **Realtek** (ID de fabricante: 0bda, ID de producto: 8832 o 885a).
3. Iniciar VM → `lsusb` para confirmar → seguir los pasos de Kali.

### VMware

1. **Máquina virtual → USB y Bluetooth** → Buscar **Realtek RTL8832BU** → **Conectar**.
2. `lsusb` para confirmar → seguir los pasos de Kali.

---

## Solución de problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| `lsusb` no muestra 0bda:8832 o 0bda:885a | Adaptador no detectado | Pruebe con un puerto USB diferente |
| `install-driver.sh` falla | Faltan encabezados | `sudo apt install linux-headers-$(uname -r)` |
| La clonación de GitHub falla o es lenta | Problema de red | Usa un proxy o espejo de confianza |
| `modprobe 8852bu` falla | Controlador no compilado o no cargado | Vuelve a ejecutar `sudo ./install-driver.sh`, revisa `sudo dkms status` y reinicia |
| El modo monitor / la inyección no funciona | Kernel anterior a 6.17 con el controlador comunitario DKMS rtl8852bu (el modo monitor puede estar limitado) | Comprueba con `uname -r`; usa un kernel 6.17+ (rtw89_8852bu integrado) o el AWUS036ACM en kernels antiguos |

> **Nota sobre VIF:** El controlador fuera del núcleo RTL8832BU no admite interfaces virtuales (VIF).

## Referencia de espejos en China

| Recurso | URL | Uso para |
|---------|-----|---------|
| Controladores oficiales de Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquetes de controladores |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | Controlador RTL8832BU |
| Espejo de la Universidad de Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Espejo de Alibaba Cloud | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| Espejo de USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| Espejo de Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

{{< faq >}}

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

## Referencias

1. [Sitio oficial de Realtek](https://www.realtek.com/)
2. [Sitio oficial de ALFA Network](https://www.alfa.com.tw/)
3. [Documentación oficial de Kali Linux](https://www.kali.org/docs/)
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
