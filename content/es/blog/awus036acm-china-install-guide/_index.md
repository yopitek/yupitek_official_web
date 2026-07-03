---
title: "Guía de instalación del controlador ALFA AWUS036ACM para China: Kali Linux, Ubuntu, Debian y Raspberry Pi"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acm-china-install-guide"
tags: ["alfa", "awus036acm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "vif"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 2
description: "Guía paso a paso para instalar los controladores ALFA AWUS036ACM en China usando espejos nacionales. Controlador MT7612U integrado en el kernel, soporte VIF completo. Cubre Kali Linux, Ubuntu 22/24, Debian y Raspberry Pi. No se requiere GitHub."
related_product: "/es/products/alfa/awus036acm/"
featureimage: "/images/blog/awus036acm-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "¿Qué chip usa el AWUS036ACM? ¿Necesita instalar controlador?"
    answer: "Usa el chip MediaTek MT7612U. El controlador mt76x2u está integrado en el kernel de Linux desde la versión 4.19; en la mayoría de los casos es plug-and-play."
  - question: "¿El AWUS036ACM admite interfaces virtuales (VIF)?"
    answer: "Sí, el MT7612U admite completamente el VIF nativo del núcleo, puede ejecutar simultáneamente una interfaz de monitor y una interfaz gestionada, sin necesidad de parches."
  - question: "¿Hace falta VPN para instalar el AWUS036ACM en China?"
    answer: "No, el controlador ya está integrado en el núcleo; solo necesitas instalar el paquete de firmware firmware-misc-nonfree desde un espejo nacional."
  - question: "¿Cuánto consume el AWUS036ACM en Raspberry Pi?"
    answer: "Consumo máximo aprox. 400 mW. Se recomienda usar un concentrador USB con alimentación independiente para evitar la limitación de velocidad de la Raspberry Pi."
  - question: "¿Por qué en Debian el AWUS036ACM se detecta pero no funciona?"
    answer: "Falta el paquete de firmware firmware-misc-nonfree; tras instalarlo, la tarjeta se inicializa correctamente."
---

El AWUS036ACM es uno de los adaptadores Alfa más fáciles de configurar en Linux. Su chip MT7612U usa el controlador `mt76x2u`, que está integrado en el kernel de Linux desde la versión 4.19. En la mayoría de los sistemas modernos, el adaptador funciona con dos o tres comandos. Esta guía cubre la configuración completa — verificación del controlador, modo monitor, inyección de paquetes y VIF — usando únicamente espejos nacionales. No se requiere GitHub.

{{< tldr >}}
El AWUS036ACM con chip MT7612U tiene el controlador integrado en el núcleo sin compilar. Admite modo monitor, inyección de paquetes y VIF simultáneo. En China solo necesitas instalar el paquete de firmware.
{{< /tldr >}}

Asegúrate de tener lo siguiente listo:


## Antes de empezar

Asegúrate de tener lo siguiente listo:

1. El adaptador **ALFA AWUS036ACM**
2. Cable USB (el que viene en la caja funciona bien)
3. Un hub USB con alimentación — requerido si usas Raspberry Pi
4. Conexión a Internet activa para acceder a los espejos nacionales

Conecta el adaptador y confirma que tu sistema lo detecta:

```bash
lsusb
```

Busca esto en la salida:

```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.
```

Si ves `0e8d:7612`, el adaptador está detectado. Ve a la sección de tu sistema operativo a continuación.

Si no lo ves, prueba con otro puerto USB o cambia el cable, luego ejecuta `lsusb` de nuevo.

## Elige tu sistema operativo

Ve directamente a la sección correcta para tu OS:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

¿Ya instalado? Salta a:

- [Activar modo monitor](#enable-monitor-mode)
- [Probar inyección de paquetes](#test-packet-injection)
- [Interfaz virtual (VIF)](#virtual-interface-vif)
- [Passthrough USB en máquina virtual](#virtual-machine-usb-passthrough)

---

## Kali Linux

El controlador MT7612U ya está en el kernel de Kali. En la mayoría de los casos el adaptador funciona en el momento en que lo conectas. Los pasos a continuación verifican que el controlador está cargado y te guían a través del modo monitor.

### Paso 1: Cambiar al espejo de China

Abre tu lista de fuentes en el terminal.

```bash
sudo nano /etc/apt/sources.list
```

Elimina lo que haya allí, luego pega esta línea:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Guardar: presiona **Ctrl+O**, luego Enter, luego Ctrl+X para salir. Actualiza el índice de paquetes.

```bash
sudo apt update
```

> **Espejo de respaldo:** Si 中科大 (USTC) está lento, usa 清华 (Tsinghua) en su lugar:
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Paso 2: Verificar el controlador

Comprueba si el módulo se cargó automáticamente al conectar el adaptador.

```bash
lsmod | grep mt76
```

Deberías ver una salida que contenga `mt76x2u`. Si no aparece nada, cárgalo manualmente.

```bash
sudo modprobe mt76x2u
```

Ejecuta `lsmod | grep mt76` de nuevo para confirmar. Luego verifica que el adaptador está activo.

```bash
iwconfig
```

Busca una interfaz inalámbrica — típicamente `wlan0` o `wlan1`. Si la interfaz aparece con un ESSID o `unassociated`, el controlador está funcionando.

---

### Paso 2 (Alternativa): Instalar módulos adicionales del kernel

Si `modprobe mt76x2u` da un error "Module not found", tu build del kernel puede no tener los módulos MT76. Instálalos desde el espejo de China.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
```

Después de que la instalación se complete, carga el módulo de nuevo.

```bash
sudo modprobe mt76x2u
```

Si el paquete no está disponible para tu versión exacta del kernel, compila el controlador desde las fuentes.

```bash
sudo apt install -y git build-essential libssl-dev
git clone https://gitee.com/mirrors/mt76.git
cd mt76
make
sudo make install
sudo modprobe mt76x2u
```

> **NOTA:** Si esa URL de Gitee no carga, busca `mt76` en Gitee y elige el fork actualizado más recientemente. También puedes descargar archivos de controladores directamente desde [files.alfa.com.tw](https://files.alfa.com.tw).

---

### Paso 3: Activar modo monitor {#enable-monitor-mode}

Antes de cambiar al modo monitor, comprueba qué nombre de interfaz asignó el sistema al adaptador.

```bash
iwconfig
```

Busca `wlan0` o `wlan1`. Usa ese nombre en los comandos a continuación.

Detén NetworkManager y wpa_supplicant para que no interfieran.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirma el cambio.

```bash
iwconfig
```

Busca una entrada como `wlan0mon` con `Mode:Monitor`. Cuando lo veas, el adaptador está listo para captura de paquetes.

---

### Paso 4: Probar inyección de paquetes {#test-packet-injection}

Ejecuta el test de inyección contra la interfaz monitor.

```bash
sudo aireplay-ng --test wlan0mon
```

Un resultado exitoso se ve así:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

Si el test falla, reinicia y ejecútalo de nuevo. Si sigue fallando, confirma que ningún otro proceso tiene la interfaz con `iwconfig`.

---

## Ubuntu 22.04 / 24.04

El controlador MT7612U también está en el kernel de Ubuntu, pero puede estar en el paquete `linux-modules-extra` en lugar de en la imagen base del kernel. Los pasos a continuación manejan ambos casos.

### Paso 1: Cambiar al espejo de China

#### Ubuntu 24.04 (Noble)

Abre el archivo de fuentes en formato DEB822:

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Elimina todo y pega:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Guarda con `Ctrl+O`, luego sal con `Ctrl+X`.

#### Ubuntu 22.04 (Jammy)

Abre el archivo de fuentes clásico:

```bash
sudo nano /etc/apt/sources.list
```

Reemplaza todas las líneas con:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Guarda y sal (`Ctrl+O`, luego `Ctrl+X`).

#### Actualizar el índice de paquetes

```bash
sudo apt update
```

---

### Paso 2: Cargar el controlador

Intenta cargar el módulo directamente primero.

```bash
sudo modprobe mt76x2u
```

Si da un error "Module not found", instala el paquete de módulos adicionales.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

Verifica que el adaptador es visible.

```bash
iwconfig
```

Una interfaz como `wlan0` o `wlan1` en la salida confirma que el controlador está activo.

---

### Paso 3: Instalar herramientas inalámbricas

Instala aircrack-ng para modo monitor y pruebas de inyección.

```bash
sudo apt install -y aircrack-ng
```

---

### Paso 4: Activar modo monitor

Mata los procesos que interfieren, luego inicia el modo monitor.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

> **Nota:** Tu interfaz puede ser `wlan1` si hay otra tarjeta inalámbrica presente. Ejecuta `iwconfig` primero para verificar.

---

### Paso 5: Probar inyección de paquetes

```bash
sudo aireplay-ng --test wlan0mon
```

Un resultado exitoso muestra `Injection is working!`. Si ves errores de interfaz, verifica que el modo monitor está activo con `iwconfig wlan0mon`.

---

## Debian

El controlador MT7612U está en el kernel de Debian pero a veces requiere el paquete `firmware-misc-nonfree` para inicializarse completamente.

### Paso 1: Cambiar al espejo de China

Abre la lista de fuentes:

```bash
sudo nano /etc/apt/sources.list
```

Elimina todo y pega estas tres líneas (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Guarda con `Ctrl+O`, luego sal con `Ctrl+X`. Actualiza:

```bash
sudo apt update
```

### Paso 2: Instalar firmware no libre

El MT7612U requiere archivos de firmware del paquete `firmware-misc-nonfree`. Sin esto, el adaptador se inicializa pero puede no asociarse o cambiar al modo monitor.

```bash
sudo apt install -y firmware-misc-nonfree
```

### Paso 3: Cargar el controlador

```bash
sudo modprobe mt76x2u
```

Si falta el módulo, instala primero los módulos adicionales del kernel.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

Confirma que la interfaz apareció.

```bash
iwconfig
```

### Paso 4: Activar modo monitor

```bash
sudo apt install -y aircrack-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirma el modo monitor con `iwconfig` — busca `wlan0mon` con `Mode:Monitor`.

### Paso 5: Probar inyección de paquetes

```bash
sudo aireplay-ng --test wlan0mon
```

`Injection is working!` confirma que el adaptador está completamente operativo.

---

## Raspberry Pi 4B / 5

> El AWUS036ACM consume alrededor de 400mW bajo carga. Usa un hub USB con alimentación para evitar que el Pi haga throttling.

---

### Paso 1: Descargar imagen Kali Linux ARM64

Ve a la página oficial de descargas Kali ARM:
https://www.kali.org/get-kali/#kali-arm

Elige **Raspberry Pi 4 (64-bit)** o **Raspberry Pi 5 (64-bit)**. No uses la imagen de 32 bits — se requiere 64 bits.

> **Espejo de China:** Si kali.org está lento, usa 华为云:
> https://repo.huaweicloud.com/kali-images/
> Navega hasta la carpeta de la última versión y descarga la imagen ARM64 desde allí.

---

### Paso 2: Flashear en MicroSD

Verifica primero la ruta del dispositivo de tu tarjeta.

```bash
lsblk
```

Luego flashea, reemplazando `/dev/sdX` con la ruta real de tu tarjeta.

```bash
# Reemplaza /dev/sdX con tu tarjeta SD real (verifica con lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Espera a que `sync` se complete, luego arranca. Credenciales predeterminadas: **kali / kali**.

---

### Paso 3: Cambiar al espejo de China

```bash
sudo nano /etc/apt/sources.list
```

Reemplaza el contenido con:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Guarda y aplica.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

### Paso 4: Verificar el controlador

Después del reinicio, conecta el adaptador y comprueba.

```bash
lsmod | grep mt76
```

Si aparece `mt76x2u`, has terminado. Si no:

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

---

### Paso 5: Activar modo monitor

En un Pi con Wi-Fi integrado, el AWUS036ACM aparece como `wlan1` — la radio integrada ocupa `wlan0`.

```bash
iwconfig
```

Anota el nombre de la interfaz, luego inicia el modo monitor en ella.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Confirma con `iwconfig` — busca `wlan1mon` con `Mode:Monitor`.

---

### Paso 6: Probar inyección de paquetes

```bash
sudo aireplay-ng --test wlan1mon
```

`Injection is working!` confirma la operación completa. Si falla, comprueba que estás usando un hub con alimentación.

---

## Passthrough USB en máquina virtual

### VirtualBox

1. Apaga la VM. Ve a **Configuración → USB**.
2. Habilita el **Controlador USB 3.0 (xHCI)**.
3. Haz clic en **+** para añadir un filtro USB.
4. Selecciona: **MediaTek Inc. MT7612U** (ID: 0e8d:7612).
5. Inicia la VM — el adaptador aparece dentro de Kali.

Ejecuta `lsusb` en la VM para confirmar `0e8d:7612`, luego sigue los pasos de Kali anteriores.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Inicia la VM.
2. Menú: **Máquina virtual → USB y Bluetooth**.
3. Encuentra **MediaTek MT7612U** y haz clic en **Conectar**.
4. Ejecuta `lsusb` en la VM para confirmar, luego sigue los pasos de Kali anteriores.

---

## Interfaz virtual (VIF)

Aquí es donde el AWUS036ACM supera al ACH. El chip MT7612U tiene soporte VIF completo nativo del kernel. Puedes ejecutar una interfaz monitor y una interfaz administrada o AP en el mismo adaptador simultáneamente — sin parches, sin trucos.

### Crear una segunda interfaz virtual

Con el adaptador en modo administrado como `wlan0`, añade una interfaz monitor junto a ella.

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

Ahora verifica que ambas interfaces están activas.

```bash
iwconfig
```

Deberías ver tanto `wlan0` (asociado, modo administrado) como `mon0` (modo monitor). El adaptador está haciendo ambas cosas al mismo tiempo.

### Caso de uso: Monitorear mientras permaneces conectado

Esto te permite capturar tráfico en `mon0` mientras `wlan0` permanece conectado a una red — útil para análisis correlacionado.

```bash
sudo airodump-ng mon0
```

`wlan0` continúa su asociación normal mientras `mon0` captura todo en rango.

### Caso de uso: AP falso + Monitor

Crea una interfaz AP y una interfaz monitor juntas.

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

Ejecuta `iwconfig` para confirmar que las tres interfaces (`wlan0`, `ap0`, `mon0`) están activas.

> **Nota sobre hostapd:** La operación completa de AP requiere configurar `hostapd`. Eso está fuera del alcance de esta guía. Los pasos anteriores confirman que el adaptador puede crear la interfaz — la configuración real del AP es un tema separado.

---

## Solución de problemas

| Problema | Causa probable | Solución |
|---------|--------------|---------|
| `lsusb` no muestra 0e8d:7612 | Adaptador sin alimentación o cable defectuoso | Prueba un puerto USB diferente. Usa un hub con alimentación en Raspberry Pi. |
| `modprobe mt76x2u` dice "Module not found" | Al kernel le faltan módulos adicionales | Ejecuta `sudo apt install linux-modules-extra-$(uname -r)` |
| La interfaz aparece pero no se asocia | Archivo de firmware faltante | Ejecuta `sudo apt install firmware-misc-nonfree` (Debian) |
| `airmon-ng start wlan0` falla | NetworkManager todavía en ejecución | Ejecuta primero `sudo airmon-ng check kill` |
| El modo monitor inicia pero no se captura tráfico | Canal o nombre de interfaz incorrecto | Establece el canal: `iwconfig wlan0mon channel 6` |
| El test de inyección dice "No Answer" | AP demasiado lejos o interfaz incorrecta | Acércate al AP. Usa `wlan0mon`, no `wlan0`. |
| La creación de interfaz VIF falla | Controlador no completamente cargado | Desconecta el adaptador, recarga el módulo: `sudo rmmod mt76x2u && sudo modprobe mt76x2u` |

## Referencia de espejos de China

Todos los recursos usados en esta guía — no se requiere GitHub:

| Recurso | URL | Para usar con |
|---------|-----|--------------|
| Controladores oficiales Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquetes de controladores, firmware |
| Documentación Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Manuales de producto |
| Espejo 清华大学 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Espejo 阿里云 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recomendado) |
| Espejo 中科大 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recomendado) |
| Espejo 华为云 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Imágenes Kali ARM (respaldo) |
| Controlador MT76 (Gitee) | [gitee.com/mirrors/mt76](https://gitee.com/mirrors/mt76) | Compilación manual como respaldo |

{{< faq >}}

## Más guías de adaptadores Alfa para China

Esta es parte de la serie **Alfa China Install Guide**. Cada artículo cubre un modelo de adaptador:

- [Guía de instalación AWUS036ACH para China](/es/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potencia
- AWUS036ACM ← estás aquí
- [Guía de instalación AWUS036ACS para China](/es/blog/awus036acs-china-install-guide/)
- [Guía de instalación AWUS036AX para China](/es/blog/awus036ax-china-install-guide/)
- [Guía de instalación AWUS036AXER para China](/es/blog/awus036axer-china-install-guide/)
- [Guía de instalación AWUS036AXM para China](/es/blog/awus036axm-china-install-guide/)
- [Guía de instalación AWUS036AXML para China](/es/blog/awus036axml-china-install-guide/)
- [Guía de instalación AWUS036EAC para China](/es/blog/awus036eacs-china-install-guide/)

¿Preguntas? Deja un comentario abajo o contáctanos en [yupitek.com/es/contact/](https://yupitek.com/es/contact/)

## Referencias

1. [Controlador mt76 del núcleo Linux](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [Documentación oficial de aircrack-ng](https://www.aircrack-ng.org/)
3. [Sitio oficial de ALFA Network](https://www.alfa.com.tw/)
4. [Documentación oficial de Kali Linux](https://www.kali.org/docs/)
5. [Paquete firmware-misc-nonfree de Debian](https://packages.debian.org/bookworm/firmware-misc-nonfree)
