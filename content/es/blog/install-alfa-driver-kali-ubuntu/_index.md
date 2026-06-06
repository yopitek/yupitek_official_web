---
title: "Cómo Instalar el Controlador ALFA USB WiFi en Kali Linux y Ubuntu 24.04 (2026)"
description: "Guía completa para instalar controladores de adaptadores ALFA Network en Kali Linux 2024 y Ubuntu 24.04 para chipsets RTL8812AU, MT7612U y MT7921AUN."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["instalación-controlador", "Kali-Linux", "Ubuntu", "RTL8812AU", "ALFA-Network"]
featureimage: "/images/blog/install-alfa-driver-kali-ubuntu.webp"
---

Lograr que un adaptador USB WiFi funcione en Linux casi siempre se reduce a una sola cosa: el controlador. A diferencia de Windows, donde los fabricantes incluyen los controladores en instaladores ejecutables, Linux usa módulos del kernel — código compilado que el sistema operativo carga para comunicarse con el hardware. Entender este modelo hace que la resolución de problemas sea directa y la instalación del controlador sea predecible.

Esta guía cubre la instalación de controladores para todos los chipsets principales de adaptadores USB WiFi de ALFA Network tanto en Kali Linux 2024/2025 como en Ubuntu 24.04 LTS.

---

## Cómo Funcionan los Controladores USB WiFi en Linux

### Módulos del Kernel

Un controlador WiFi de Linux es un **módulo del kernel** — un archivo `.ko` que se carga en el kernel en ejecución al arrancar o a demanda. Cuando conectas un dispositivo USB, el kernel lee su Vendor ID y Product ID USB, busca un módulo coincidente en su base de datos y lo carga automáticamente.

Para chipsets comunes como el MediaTek MT7612U, esto ocurre de forma transparente: conectas el adaptador, se carga un módulo, aparece una interfaz. Para chipsets más nuevos o menos comunes, no existe un módulo en el árbol principal, y debes compilar uno desde el código fuente.

### Controladores Fuera del Árbol Principal

Cuando un controlador no está incluido en el kernel principal (llamado controlador "fuera del árbol" o "externo"), debes:

1. Descargar el código fuente del controlador
2. Compilarlo contra las cabeceras de tu kernel en ejecución
3. Instalar el archivo `.ko` resultante en el directorio de módulos del kernel
4. Cargarlo con `modprobe`

El paso de compilación requiere que las cabeceras de tu kernel estén instaladas y coincidan exactamente con tu kernel en ejecución. Esta es la fuente más común de fallos en la instalación de controladores.

### DKMS: Dynamic Kernel Module Support

Un simple `make install` compila el controlador para tu kernel actual. Cuando Kali o Ubuntu actualiza el kernel — lo cual sucede regularmente — el controlador antiguo ya no se carga, y debes recompilarlo.

**DKMS** resuelve esto registrando el código fuente del controlador con un daemon del sistema que recompila automáticamente los módulos registrados cada vez que se instala un nuevo kernel. Es el enfoque recomendado para cualquier adaptador que requiera un controlador fuera del árbol principal.

---

## Identifica Tu Chipset

El controlador que necesitas depende completamente de tu chipset, no del nombre de marketing del adaptador. Dos adaptadores con el mismo nombre pero diferentes revisiones de hardware pueden usar chipsets diferentes.

### Tabla de Modelos ALFA y Sus Chipsets

| Modelo ALFA | Chipset | USB IDs | Controlador |
|---|---|---|---|
| [AWUS036ACH](/es/products/alfa/awus036ach/) | RTL8812AU | 0bda:8812 | aircrack-ng/rtl8812au |
| [AWUS036ACM](/es/products/alfa/awus036acm/) | MT7612U | 0e8d:7612 | mt76x2u (en el kernel) |
| [AWUS036AX](/es/products/alfa/awus036ax/) | RTL8832BU | 0e8d:885a | OOK driver (<6.14) |
| [AWUS036AXML](/es/products/alfa/awus036axml/) | MT7921AUN | 0e8d:7961 | mt7921u (kernel 5.18+) |

### Identifica Tu Adaptador con lsusb

Conecta tu adaptador y ejecuta:

```bash
lsusb
```

Ejemplo de salida:

```
Bus 003 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
Bus 003 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/bgn/ac
```

Cruza el valor `ID xx:xx` con la tabla anterior para confirmar tu chipset.

---

## Prepara Tu Sistema

Sin importar qué chipset tengas, instala primero los prerrequisitos comunes de compilación:

**Kali Linux:**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r)
```

**Ubuntu 24.04:**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r) \
    linux-headers-generic
```

Confirma que las cabeceras están instaladas para tu kernel en ejecución exacto:

```bash
uname -r
# Ejemplo: 6.6.9-amd64

ls /lib/modules/$(uname -r)/build
# Debe existir — si no, las cabeceras no están instaladas
```

---

## Controlador RTL8812AU (AWUS036ACH)

El RTL8812AU requiere un controlador fuera del árbol principal. Existen dos forks mantenidos por la comunidad; elige según tu sistema operativo.

### Opción A: aircrack-ng/rtl8812au (Kali Linux — Recomendado)

Este fork es mantenido por el equipo de Aircrack-ng con compatibilidad explícita con Kali y soporte optimizado de inyección de paquetes:

```bash
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
make
sudo make install
sudo modprobe 88XXau
```

Verifica que la interfaz apareció:

```bash
ip link show | grep wlan
# Debería mostrar wlan0 o similar
```

### Opción B: morrownr/8812au-20210708 (Ubuntu 24.04 — Recomendado)

El fork de morrownr está optimizado para Ubuntu e incluye un conveniente script de instalación con integración DKMS:

```bash
git clone https://github.com/morrownr/8812au-20210708
cd 8812au-20210708
sudo ./install-driver.sh
```

El script de instalación maneja el registro DKMS automáticamente. Después de ejecutarlo:

```bash
# Reiniciar para cargar el nuevo módulo
sudo reboot

# Después del reinicio, verificar
lsmod | grep 8812au
```

### Registro Manual DKMS (Cualquier Fork)

Si prefieres control manual:

```bash
# Clonar controlador (usa cualquiera de los dos forks)
git clone https://github.com/aircrack-ng/rtl8812au

# Obtener versión del Makefile
grep "^MODULE_VERSION" rtl8812au/Makefile
# Anota la versión, ej. v5.6.4.2 → usa 5.6.4.2

# Copiar fuente al directorio DKMS
sudo cp -r rtl8812au /usr/src/rtl8812au-5.6.4.2

# Registrar, compilar, instalar
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2

# Verificar
dkms status
# Esperado: rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

### Salida Esperada de lsusb y lsmod

Después de una instalación exitosa:

```bash
lsusb
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU ...

lsmod | grep 88XXau
# 88XXau    3461120  0
```

---

## Controlador MT7612U (AWUS036ACM, AWUS036ACX)

El chipset MT7612U es el más fácil de los cuatro para hacer funcionar porque su controlador ha sido parte del kernel principal de Linux desde la versión **4.19**. En Kali Linux 2022+ y Ubuntu 20.04+, no se necesita instalar ningún controlador en absoluto.

### Verificar Versión del Kernel

```bash
uname -r
```

Si la salida es 4.19 o superior (lo cual será el caso en cualquier Kali o Ubuntu moderno), el módulo `mt76x2u` está disponible.

### Cargar el Módulo

```bash
sudo modprobe mt76x2u
```

Verificar que se cargó:

```bash
lsmod | grep mt76x2u
# mt76x2u    86016  0
# mt76x2_common    61440  1 mt76x2u
# mt76_usb    40960  1 mt76x2u
```

Una interfaz inalámbrica debería aparecer inmediatamente:

```bash
ip link show
# wlan0: ...
```

### Hacer que el Módulo Cargue al Inicio

En la mayoría de los sistemas, el módulo se carga automáticamente cuando se detecta el adaptador. Para asegurarte explícitamente de que cargue al inicio:

```bash
echo "mt76x2u" | sudo tee -a /etc/modules
```

### Sin Compilación Necesaria

Esta es la gran ventaja del chipset MT7612U: cero compilación, sin código fuente del controlador, sin depender de las cabeceras del kernel. Funciona desde el primer momento en cada distribución compatible. Para usuarios que no quieren lidiar con la gestión de controladores, el [AWUS036ACM](/es/products/alfa/awus036acm/) es el adaptador de pentesting más plug-and-play disponible.

---

## Controlador MT7921AUN (AWUS036AXM, AWUS036AXML — Wi-Fi 6E)

El MT7921AUN es el chipset Wi-Fi 6E de MediaTek. Su controlador Linux, `mt7921u`, se integró al kernel principal en la **versión 5.18**.

### Verificar Versión del Kernel

```bash
uname -r
```

**Kali Linux 2022.2 y posterior** incluye kernel 5.18 o más nuevo — compatible.
**Ubuntu 22.04 LTS** incluye kernel 5.15 — **no compatible** sin actualizar el kernel.
**Ubuntu 24.04 LTS** incluye kernel 6.8 — totalmente compatible.

### Cargar el Módulo (Kernel 5.18+)

```bash
sudo modprobe mt7921u
```

Verificar:

```bash
lsmod | grep mt7921u
# mt7921u    57344  0
# mt7921_common    196608  1 mt7921u
```

### Ubuntu 22.04: Ruta de Actualización del Kernel

Si estás en Ubuntu 22.04 con kernel 5.15, tienes dos opciones:

**Opción A: Kernel HWE** (recomendado)

```bash
sudo apt install linux-generic-hwe-22.04
sudo reboot
```

El kernel HWE (Hardware Enablement) para Ubuntu 22.04 es 6.2+, que soporta mt7921u.

**Opción B: Actualizar a Ubuntu 24.04**

Ubuntu 24.04 LTS incluye kernel 6.8 y soporte completo de mt7921u. Esta es la solución más limpia a largo plazo.

### Estado de Wi-Fi 6E y Modo Monitor

A partir de 2026, el controlador mt7921u proporciona soporte estable para modo administrado (conectarse a redes) en bandas de 2.4 GHz, 5 GHz y 6 GHz. El soporte de modo monitor en 2.4 y 5 GHz es funcional. El **modo monitor en 6 GHz** aún está madurando — verifica el estado actual en el rastreador de issues del controlador del kernel `mt76` antes de depender de él para evaluaciones en 6 GHz.

---

---

## DKMS: Mantener los Controladores Funcionando Tras Actualizaciones del Kernel

Tanto Kali Linux como Ubuntu actualizan el kernel regularmente. Sin DKMS, tus controladores fuera del árbol principal (RTL8812AU) dejan de funcionar después de una actualización del kernel hasta que recompiles manualmente.

Con DKMS correctamente configurado, la recompilación ocurre automáticamente durante `apt upgrade`.

### Verificar que DKMS Gestiona Tu Controlador

```bash
dkms status
```

Ejemplo de salida con controladores correctamente gestionados:

```
rtl8812au/5.6.4.2, 6.6.9-amd64: installed
8814au/5.8.7.4, 6.6.9-amd64: installed
```

### Qué Sucede Durante una Actualización del Kernel

```
apt upgrade
→ Nuevo paquete del kernel descargado
→ Hook DKMS activado
→ Fuente rtl8812au recompilada para el nuevo kernel
→ Nuevo .ko instalado
→ Sistema reinicia con el nuevo kernel
→ Controlador se carga automáticamente
```

Si DKMS falla durante una actualización (visible vía `dkms status` mostrando "built" pero no "installed"), reinstala manualmente:

```bash
sudo dkms install rtl8812au/5.6.4.2 -k $(uname -r)
```

---

## Solución de Problemas

| Síntoma | Causa Probable | Solución |
|---|---|---|
| No aparece interfaz wlan al conectar | Controlador no cargado | `sudo modprobe 88XXau` o `sudo modprobe mt76x2u` |
| `modprobe: FATAL: Module not found` | Controlador no compilado para el kernel actual | Recompilar o ejecutar `sudo dkms install` |
| Interfaz aparece pero desaparece en segundos | Gestión de energía interfiriendo | `sudo iwconfig wlan0 power off` |
| `make` falla con "linux/module.h not found" | Cabeceras del kernel no instaladas | `sudo apt install linux-headers-$(uname -r)` |
| `make` falla con incompatibilidad de versión | Cabeceras no coinciden con el kernel | `uname -r` vs `ls /lib/modules` — reinstalar cabeceras coincidentes |
| Dispositivo aparece en lsusb pero sin interfaz | Módulo cargado pero interfaz no creada | Verificar `dmesg \| tail -30` para errores |
| Modo monitor falla: "Operation not supported" | Versión del controlador no soporta modo monitor | Usar el fork aircrack-ng en lugar del controlador empaquetado por la distro |
| Test de inyección aireplay-ng: 0% | Interfaz no está en modo monitor | Verificar con `iwconfig`, volver a ejecutar `airmon-ng start` |
| Controlador funciona pero se detiene al reiniciar | Módulo no agregado al initramfs | `sudo update-initramfs -u` o usar DKMS |
| Fallo de compilación DKMS tras actualización del kernel | Cabeceras faltantes para el nuevo kernel | `sudo apt install linux-headers-$(uname -r)` |

### Comandos de Diagnóstico Detallados

```bash
# Verificar todos los módulos inalámbricos cargados
lsmod | grep -E "8812|8814|mt76|mt79"

# Verificar mensajes del kernel para eventos USB e inalámbricos
dmesg | grep -iE "rtl|mt76|mt79|usb 802|wlan"

# Listar todas las interfaces inalámbricas
iw dev

# Verificar qué controlador usa una interfaz específica
ethtool -i wlan0 | grep driver

# Verificar detalles del dispositivo USB
lsusb -v -d 0bda:8812 2>/dev/null | grep -E "idVendor|idProduct|iProduct"

# Verificar estado DKMS de todos los módulos registrados
dkms status
```

---

## Referencia Rápida: Qué Controlador para Cada Adaptador

| Lo que tienes | Chipset | Kali Linux | Ubuntu 24.04 |
|---|---|---|---|
| [AWUS036ACH](/es/products/alfa/awus036ach/) | RTL8812AU | `aircrack-ng/rtl8812au` | `morrownr/8812au-20210708` |
| [AWUS036ACM](/es/products/alfa/awus036acm/) | MT7612U | Integrado (`mt76x2u`) | Integrado (`mt76x2u`) |
| [AWUS036AX](/es/products/alfa/awus036ax/) | RTL8832BU | OOK (<6.14) | OOK (<6.14) |
| [AWUS036AXML](/es/products/alfa/awus036axml/) | MT7921AUN | Integrado (`mt7921u`, kernel 5.18+) | Integrado (`mt7921u`, kernel 6.8) |

---

## Asegúrate de Obtener Hardware Genuino

Los problemas con controladores a veces son causados por adaptadores falsificados que reportan incorrectamente sus USB IDs o usan chipsets inferiores que no coinciden con el modelo declarado. Los adaptadores genuinos de ALFA Network de distribuidores autorizados se comportan exactamente como está documentado.

Yopitek es un distribuidor autorizado de ALFA Network. Explora la [gama completa de productos ALFA Network](/es/products/alfa/) para asegurarte de comprar hardware genuino con garantía del fabricante y compatibilidad predecible de controladores.

---

## Resumen

La instalación de controladores WiFi en Linux sigue un árbol de decisión simple:

1. **Identifica tu chipset** con `lsusb` y la tabla de mapeo de arriba
2. **¿MT7612U o MT7921AUN (en kernel 5.18+)?** → Solo ejecuta `modprobe`, listo
3. **¿RTL8812AU?** → Clona el repositorio apropiado, ejecuta `make && sudo make install`, activa DKMS para persistencia
4. **¿Algo no funciona?** → Revisa la tabla de solución de problemas, verifica que las cabeceras coincidan con el kernel, revisa `dmesg`

La belleza de los adaptadores ALFA Network es que los cuatro chipsets principales tienen soluciones de controladores bien documentadas y activamente mantenidas. Nunca te quedas en territorio sin soporte.
