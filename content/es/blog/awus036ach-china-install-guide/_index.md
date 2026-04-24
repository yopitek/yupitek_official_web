---
title: "Guía de instalación del controlador ALFA AWUS036ACH para China: Kali Linux, Ubuntu, Debian y Raspberry Pi"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "driver", "china", "monitor-mode"]
categories: ["Driver Guides"]
series: ["Alfa China Install Guide"]
description: "Guía paso a paso para instalar el controlador ALFA AWUS036ACH en China usando espejos domésticos. Compatible con Kali Linux, Ubuntu 22/24, Debian y Raspberry Pi. No se requiere GitHub."
related_product: "/es/products/alfa/awus036ach/"
---

Acabas de recibir el AWUS036ACH y tu sistema Linux no lo reconoce. Es completamente normal — este chip necesita el controlador RTL8812AU, que no funciona de forma automática. Esta guía te lleva a través de toda la instalación en aproximadamente 30 minutos, usando únicamente espejos domésticos. No se necesita acceso a GitHub.

## Antes de empezar

Asegúrate de tener lo siguiente listo:

1. **ALFA AWUS036ACH** adaptador
2. Cable USB (el que viene en la caja funciona perfectamente)
3. Un hub USB con alimentación propia — obligatorio en Raspberry Pi
4. Conexión a internet activa hacia espejos domésticos

Conecta el adaptador y confirma que tu sistema lo detecta:

```bash
lsusb
```

Busca esta línea en la salida:

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

Si ves `0bda:8812`, el adaptador fue detectado. Ve a la sección de tu OS a continuación.

Si no lo ves, prueba con un puerto USB diferente o cambia el cable, luego ejecuta `lsusb` de nuevo.

## Elige tu sistema operativo

Salta a la sección correcta para tu OS:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

¿Ya instalado? Salta directamente a:

- [Activar el modo monitor](#activar-el-modo-monitor)
- [Probar la inyección de paquetes](#probar-la-inyección-de-paquetes)
- [Reenvío USB para VM](#reenvío-usb-para-máquina-virtual)

---

## Kali Linux

Kali viene con herramientas inalámbricas potentes integradas. Hacer funcionar el controlador AWUS036ACH toma cuatro pasos. Empieza cambiando a un espejo chino rápido para que todas las descargas sean ágiles.

### Paso 1: Cambiar al espejo de China

Abre tu lista de fuentes en el terminal.

```bash
sudo nano /etc/apt/sources.list
```

Borra todo lo que hay ahí y pega esta línea:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Guarda el archivo: presiona **Ctrl+O**, luego Enter, luego Ctrl+X para salir. Actualiza el índice de paquetes.

```bash
sudo apt update
```

> **Espejo de respaldo:** Si 中科大 (USTC) va lento en tu conexión, usa 清华 (Tsinghua) en su lugar:
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Paso 2: Instalar el controlador

El repositorio de paquetes de Kali incluye un controlador DKMS precompilado. Instálalo con un solo comando.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

DKMS recompila automáticamente el controlador cada vez que se actualiza el kernel, por lo que no necesitarás reinstalarlo manualmente después de una actualización.

Verifica que el controlador se cargó correctamente.

```bash
modinfo 88XXau | grep -E "filename|version"
```

Deberías ver una línea `filename` que termina en `.ko` y una línea `version` que muestra una cadena de versión como `5.6.4.2`. Si ambas aparecen, el controlador está listo.

---

### Paso 2 (Alternativo): Compilación manual desde el código fuente

Sigue esta sección solo si `apt install` arriba falló. Primero instala las dependencias de compilación.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Descarga el código fuente del controlador desde Gitee.

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

> **NOTA:** Si esa URL no carga, busca `rtl8812au` en Gitee y elige el fork actualizado más recientemente. También puedes descargar un archivo fuente directamente desde [files.alfa.com.tw](https://files.alfa.com.tw).

Entra al directorio clonado, luego compila e instala.

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

Carga el controlador en el kernel en ejecución.

```bash
sudo modprobe 88XXau
```

---

### Paso 3: Activar el modo monitor {#activar-el-modo-monitor}

Antes de poner el adaptador en modo monitor, verifica qué nombre de interfaz le asignó tu sistema.

```bash
iwconfig
```

Busca una entrada `wlan0` o `wlan1`. Usa ese nombre en los comandos a continuación.

Detén NetworkManager y wpa_supplicant — ambos compiten por el adaptador y bloquearán el modo monitor.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirma que el cambio funcionó.

```bash
iwconfig
```

Busca una entrada como `wlan0mon` con `Mode:Monitor`. Cuando la veas, el adaptador está listo para la captura de paquetes.

---

### Paso 4: Probar la inyección de paquetes {#probar-la-inyección-de-paquetes}

Ejecuta la prueba de inyección contra la interfaz monitor.

```bash
sudo aireplay-ng --test wlan0mon
```

Un resultado exitoso se ve así:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

Si la prueba falla, reinicia el equipo y ejecuta la prueba de nuevo. Si sigue fallando después de reiniciar, confirma que ningún otro proceso está controlando la interfaz — ejecuta `iwconfig` y asegúrate de que solo aparece `wlan0mon`, sin nada más que reclame el adaptador.

---

## Ubuntu 22.04 / 24.04

Ubuntu se divide en dos ramas con diferentes formatos de archivos de paquetes. Los pasos a continuación cubren ambas. Usa **阿里云 (Aliyun)** como tu espejo — es rápido, confiable y mantenido por Alibaba.

### Paso 1: Cambiar al espejo de China

Elige tu versión de Ubuntu y sigue solo ese camino.

#### Ubuntu 24.04 (Noble)

Abre el nuevo archivo de fuentes en formato DEB822:

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Borra todo en el archivo y pega exactamente este contenido:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Guarda con `Ctrl+O`, luego sal con `Ctrl+X`.

#### Ubuntu 22.04 (Jammy)

Abre el archivo de fuentes clásico en su lugar:

```bash
sudo nano /etc/apt/sources.list
```

Reemplaza todas las líneas existentes con:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Guarda y sal de la misma manera (`Ctrl+O`, luego `Ctrl+X`).

#### Actualizar el índice de paquetes

Ejecuta esto para ambas versiones después de editar tu archivo de fuentes:

```bash
sudo apt update
```

---

### Paso 2: Instalar las dependencias de compilación

El controlador se compila desde el código fuente, así que primero necesitas los encabezados del kernel y las herramientas de compilación:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Esto instala gcc, make y los encabezados exactos que coinciden con tu kernel en ejecución. La parte `$(uname -r)` detecta automáticamente tu versión del kernel — no necesitas escribirla manualmente.

---

### Paso 3: Descargar el código fuente del controlador (espejo de China)

Clona el repositorio del controlador desde Gitee, que es accesible dentro de China:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

Luego entra a la carpeta clonada:

```bash
cd rtl8812au
```

> **Nota:** Si esa URL expira o devuelve 404, ve a [gitee.com](https://gitee.com) y busca `rtl8812au`. Elige el fork con la fecha de commit más reciente.

---

### Paso 4: Compilar e instalar

Construye el módulo del kernel desde el código fuente:

```bash
make
```

Instálalo en el sistema:

```bash
sudo make install
```

Registra el módulo con DKMS para que sobreviva a las actualizaciones del kernel:

```bash
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

Carga el módulo en el kernel en ejecución:

```bash
sudo modprobe 88XXau
```

Verifica que el módulo se cargó correctamente:

```bash
modinfo 88XXau | grep filename
```

Deberías ver una ruta que termina en `88XXau.ko` o similar. Si el comando devuelve salida, el controlador está activo.

---

### Paso 5: Activar el modo monitor

Primero, termina todos los procesos que podrían interferir con la interfaz inalámbrica:

```bash
sudo airmon-ng check kill
```

Luego pon el adaptador en modo monitor:

```bash
sudo airmon-ng start wlan0
```

> **Nota:** Tu interfaz puede llamarse `wlan1` en lugar de `wlan0`. Ejecuta primero `iwconfig` para ver todas las interfaces inalámbricas listadas, luego sustituye el nombre correcto en el comando anterior.

---

### Paso 6: Probar la inyección de paquetes

Con el adaptador en modo monitor, ejecuta la prueba de inyección:

```bash
sudo aireplay-ng --test wlan0mon
```

Un resultado exitoso muestra líneas como `Injection is working!`. Si ves errores sobre la interfaz, verifica que el modo monitor esté activo con `iwconfig wlan0mon`.

---

## Debian

El gestor de paquetes de Debian apunta a servidores extranjeros por defecto. Cambiar al espejo 清华大学 (Universidad Tsinghua) hace que las velocidades de descarga pasen de lentas a ultrarrápidas.

### Paso 1: Cambiar al espejo de China

Abre la lista de fuentes:

```bash
sudo nano /etc/apt/sources.list
```

Borra todo adentro y pega estas tres líneas (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Guarda con `Ctrl+O`, luego sal con `Ctrl+X`. Actualiza el índice de paquetes:

```bash
sudo apt update
```

### Paso 2: Instalar las dependencias de compilación

El controlador AWUS036ACH se compila desde el código fuente, necesitas los encabezados del kernel y herramientas de compilación:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Este comando instala automáticamente el paquete de encabezados adaptado a tu versión del kernel en ejecución.

### Paso 3: Descargar el código fuente del controlador (espejo de China)

Clona el repositorio del controlador desde Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

Entra a la carpeta del proyecto:

```bash
cd rtl8812au
```

> **¿No puedes acceder a esa URL?** Busca `rtl8812au` en Gitee y elige el fork actualizado más recientemente.

### Paso 4: Compilar e instalar

Ejecuta estos comandos en secuencia dentro de la carpeta `rtl8812au`:

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

`dkms` registra el controlador para que sobreviva automáticamente a las actualizaciones del kernel.

### Paso 5: Activar el modo monitor

**Termina los procesos que interfieren** antes de cambiar de modo:

```bash
sudo airmon-ng check kill
```

Inicia el modo monitor en tu adaptador:

```bash
sudo airmon-ng start wlan0
```

Si falta `airmon-ng`, instálalo primero:

```bash
sudo apt install -y aircrack-ng
```

Confirma que la interfaz apareció:

```bash
iwconfig
```

Busca una interfaz llamada `wlan0mon` en la salida.

### Paso 6: Probar la inyección de paquetes

```bash
sudo aireplay-ng --test wlan0mon
```

Una secuencia de resultados de prueba de inyección confirma que el adaptador funciona. Estás listo para empezar.

---

## Raspberry Pi 4B / 5

> El AWUS036ACH consume aproximadamente 500mW. Conectarlo directamente a un puerto USB del Raspberry Pi puede hacer que el Pi limite el rendimiento o se reinicie bajo carga. **Usa siempre un hub USB con alimentación propia.**

---

### Paso 1: Descargar la imagen Kali Linux ARM64

Ve a la página oficial de descargas ARM de Kali:
https://www.kali.org/get-kali/#kali-arm

Elige **Raspberry Pi 4 (64-bit)** o **Raspberry Pi 5 (64-bit)** según tu placa. No descargues la imagen de 32 bits — la compilación del controlador requiere un kernel de 64 bits.

> **Espejo de China:** Si kali.org carga lento, prueba 华为云 en su lugar:
> https://repo.huaweicloud.com/kali-images/
> Navega a la carpeta de la última versión y descarga la misma imagen ARM64 desde allí.

---

### Paso 2: Grabar en MicroSD

Inserta tu tarjeta microSD, luego verifica su ruta de dispositivo antes de escribir nada.

```bash
lsblk
```

Encuentra tu tarjeta en la lista — aparecerá como algo así como `sdb` o `mmcblk0`. Luego graba la imagen, reemplazando `/dev/sdX` con tu ruta real.

```bash
# Reemplaza /dev/sdX con tu tarjeta SD real (verifica con lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Espera a que `sync` termine antes de retirar la tarjeta. Arranca el Pi desde la tarjeta. Credenciales por defecto tras el arranque: **kali / kali**.

---

### Paso 3: Cambiar al espejo de China

Después del primer arranque, abre el archivo de fuentes de paquetes.

```bash
sudo nano /etc/apt/sources.list
```

Borra todo en el archivo y reemplázalo con esta única línea:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Guarda: presiona **Ctrl+O**, luego Enter, luego Ctrl+X. Aplica el espejo y actualiza el sistema.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

El reinicio aplica las actualizaciones del kernel antes de instalar el controlador.

---

### Paso 4: Instalar el controlador (ARM64)

El paquete DKMS funciona en ARM64 exactamente igual que en x86 — no se necesitan pasos especiales.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

Si ese comando devuelve un error indicando que el paquete no se encontró, compila el controlador desde el código fuente en su lugar.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

---

### Paso 5: Activar el modo monitor

Antes de tocar el adaptador, verifica qué nombre de interfaz le asignó el Pi.

```bash
iwconfig
```

En un Pi con chip Wi-Fi integrado, el AWUS036ACH aparece como `wlan1` — la radio integrada ocupa `wlan0`. Usa el nombre que reportó `iwconfig` arriba.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Ejecuta `iwconfig` de nuevo y busca una entrada que termine en `mon` — `wlan1mon` en el caso típico del Pi — con `Mode:Monitor`. Eso confirma que el adaptador cambió correctamente.

---

### Paso 6: Probar la inyección de paquetes

```bash
sudo aireplay-ng --test wlan1mon
```

Reemplaza `wlan1mon` con el nombre de interfaz monitor que apareció en el Paso 5. Un adaptador que funciona muestra `Injection is working!`. Si la prueba falla, reinicia e intenta de nuevo. Una mala conexión USB a través de un hub sin alimentación propia es la causa más común en el Pi — verifica que estás usando el hub alimentado.

---

## Reenvío USB para máquina virtual

¿Ejecutas Kali Linux dentro de una VM en macOS o Windows? Necesitas pasar el adaptador USB al sistema operativo invitado.

### VirtualBox

1. Con la VM apagada, ve a **Configuración → USB**.
2. Activa **Controlador USB 3.0 (xHCI)**.
3. Haz clic en el icono **+** para agregar un filtro USB.
4. Selecciona: **Realtek 802.11ac NIC [...]** (ID: 0bda:8812).
5. Inicia la VM — el adaptador aparece dentro de Kali.

Dentro de la VM, ejecuta `lsusb` para confirmar que aparece `0bda:8812`, luego sigue los pasos de Kali Linux anteriores.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Inicia la VM.
2. En el menú: **Máquina virtual → USB y Bluetooth**.
3. Encuentra **Realtek 802.11ac NIC** y haz clic en **Conectar**.
4. El adaptador se desconecta del host y aparece dentro de la VM.

Ejecuta `lsusb` dentro de la VM para confirmar, luego sigue los pasos de Kali Linux anteriores.

### Nota sobre VIF (Interfaz Virtual)

El chip RTL8812AU en el AWUS036ACH tiene soporte VIF limitado en Linux. No puedes ejecutar de forma confiable el modo administrado y el modo monitor (o modo AP) al mismo tiempo en el mismo adaptador.

Si tu flujo de trabajo necesita VIF — por ejemplo, ejecutar APs falsos mientras monitorizas simultáneamente — el AWUS036ACH no es la herramienta correcta. Consulta la [guía de instalación AWUS036ACM](/es/blog/awus036acm-china-install-guide/). Ese adaptador usa el chip MT7612U, que tiene soporte VIF nativo completo en el kernel y maneja interfaces virtuales simultáneas sin parches.

---

## Solución de problemas

| Problema | Causa probable | Solución |
|---------|---------------|---------|
| `lsusb` no muestra 0bda:8812 | Adaptador sin alimentación o cable defectuoso | Prueba un puerto USB diferente. Usa un hub alimentado en Raspberry Pi. |
| `make` falla con errores de encabezados | Encabezados del kernel faltantes o versión incompatible | Ejecuta `sudo apt install linux-headers-$(uname -r)` |
| `modprobe 88XXau` falla | Secure Boot bloqueando módulos sin firmar | Desactiva Secure Boot en el BIOS, o firma el módulo |
| El controlador desaparece después de actualizar el kernel | Controlador no registrado con DKMS | Vuelve a ejecutar `sudo dkms install rtl8812au/$(cat VERSION)` desde el directorio fuente |
| `airmon-ng start wlan0` falla | NetworkManager todavía en ejecución | Ejecuta primero `sudo airmon-ng check kill` |
| El modo monitor inicia pero no captura tráfico | Canal equivocado o nombre de interfaz incorrecto | Verifica la interfaz con `iwconfig`. Establece el canal: `iwconfig wlan0mon channel 6` |
| La prueba de inyección dice "No Answer" | AP demasiado lejos, o interfaz incorrecta | Acércate al AP. Usa `wlan0mon` y no `wlan0` |

## Referencia de espejos de China

Todos los recursos usados en esta guía — sin necesidad de GitHub:

| Recurso | URL | Usado para |
|---------|-----|-----------|
| Controladores oficiales Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquetes de controladores, firmware |
| Documentación Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Manuales de productos |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recomendado) |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recomendado) |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Imágenes Kali ARM (respaldo) |
| Controlador RTL8812AU (Gitee) | [gitee.com/mirrors/rtl8812au](https://gitee.com/mirrors/rtl8812au) | Compilación manual como alternativa |

## Más guías de adaptadores Alfa para China

Esto es parte de la serie **Alfa China Install Guide**. Cada artículo cubre un modelo de adaptador:

- AWUS036ACH ← estás aquí
- [Guía de instalación AWUS036ACM para China](/es/blog/awus036acm-china-install-guide/) — MT7612U, mejor soporte VIF
- [Guía de instalación AWUS036ACS para China](/es/blog/awus036acs-china-install-guide/)
- [Guía de instalación AWUS036AX para China](/es/blog/awus036ax-china-install-guide/)
- [Guía de instalación AWUS036AXER para China](/es/blog/awus036axer-china-install-guide/)
- [Guía de instalación AWUS036AXM para China](/es/blog/awus036axm-china-install-guide/)
- [Guía de instalación AWUS036AXML para China](/es/blog/awus036axml-china-install-guide/)
- [Guía de instalación AWUS036EAC para China](/es/blog/awus036eacs-china-install-guide/)

¿Preguntas? Deja un comentario abajo o contáctanos en [yupitek.com](https://yupitek.com/es/contact/).
