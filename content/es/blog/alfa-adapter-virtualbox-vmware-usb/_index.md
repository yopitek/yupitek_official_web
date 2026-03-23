---
title: "ALFA Adaptador USB Passthrough: Guía de Configuración para VirtualBox y VMware"
description: "Guía paso a paso para configurar el USB passthrough del adaptador ALFA WiFi en VirtualBox y VMware Workstation para Kali Linux. Cubre AWUS036ACH, AWUS036AXML, filtro USB 3.0, Extension Pack y solución de problemas."
date: 2026-04-15
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "alfa-network", "AWUS036ACH", "AWUS036AXML"]
---

Ejecutar un adaptador ALFA WiFi dentro de una máquina virtual no es tan sencillo como conectarlo y esperar que el sistema operativo invitado lo detecte. A diferencia de las carpetas compartidas o la red en modo puente, el modo monitor y la inyección de paquetes en bruto requieren **control total del USB** — la VM debe poseer el dispositivo de forma exclusiva, no compartirlo a través de la pila de red del host. Esto se llama USB passthrough, y configurarlo correctamente es el fallo de configuración más común para los pentesters y jugadores de CTF que trabajan en VMs.

Esta guía cubre la configuración completa del passthrough para **VirtualBox 7.x** y **VMware Workstation 17+ / VMware Fusion 13+**, con Kali Linux como sistema operativo invitado. Abarca tanto el AWUS036ACH (chipset RTL8812AU) como el más reciente AWUS036AXML (chipset MT7921AU), con notas específicas por adaptador cuando el comportamiento difiere.

Al finalizar, tu adaptador ALFA aparecerá dentro de Kali a través de `lsusb`, el controlador correcto estará cargado y `airmon-ng` confirmará que el modo monitor funciona.

---

## Prerrequisitos

Antes de comenzar, confirma que tu entorno cumple los siguientes requisitos. La ausencia de cualquier elemento — especialmente el Extension Pack de VirtualBox — es la causa raíz de la mayoría de los fallos de passthrough.

| Requisito | Detalles |
|---|---|
| **Hipervisor** | VirtualBox 7.x + Extension Pack **o** VMware Workstation 17+ / Fusion 13+ |
| **SO Invitado** | Kali Linux 2024.x o posterior (probado en 2024.1 a 2025.1) |
| **Adaptador ALFA** | AWUS036ACH, AWUS036AXML, AWUS036ACM o cualquier dispositivo RTL8812AU / MT7921AU |
| **Puerto USB del host** | USB 3.0 recomendado (especialmente para AWUS036AXML) |
| **SO del host** | Windows 10/11, Linux o macOS (Fusion) |
| **Acceso Sudo** | Requerido dentro de la VM de Kali |

{{< alert "circle-info" >}}
Si todavía no has instalado el controlador dentro de Kali, completa primero los pasos de USB passthrough de esta guía. Una vez que el adaptador sea visible dentro de la VM, sigue la [Guía de Instalación del Controlador ALFA](/es/blog/install-alfa-driver-kali-ubuntu/) para compilar y cargar el controlador correcto.
{{< /alert >}}

---

## USB Passthrough en VirtualBox — Paso a Paso

VirtualBox requiere un componente adicional — el **Extension Pack** — para soportar USB 2.0 y USB 3.0 passthrough. Sin él, solo está disponible USB 1.1 (OHCI), que es insuficiente para los adaptadores ALFA modernos.

### Instalar el VirtualBox Extension Pack

1. Abre [virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads).
2. Bajo **VirtualBox Extension Pack**, haz clic en **All supported platforms** para descargar el archivo `.vbox-extpack`. La versión debe coincidir exactamente con tu versión de VirtualBox instalada.
3. Abre VirtualBox, ve a **Archivo → Preferencias → Extensiones** (en macOS: **VirtualBox → Ajustes → Extensiones**).
4. Haz clic en el icono **+**, navega hasta el `.vbox-extpack` descargado e instálalo. Acepta la licencia cuando se solicite.

Para verificar que el Extension Pack está activo desde la línea de comandos:

```bash
VBoxManage list extpacks
```

Salida esperada:

```
Extension Packs: 1
Pack no. 0:   Oracle VirtualBox Extension Pack
Version:      7.0.x
...
Usable:       true
```

{{< alert "triangle-exclamation" >}}
Si el campo **Usable** muestra `false`, la versión del Extension Pack no coincide con la versión de VirtualBox. Desinstala y reinstala la versión correcta.
{{< /alert >}}

### Añadir el Usuario al Grupo vboxusers (Solo Hosts Linux)

En hosts Linux, tu cuenta de usuario debe ser miembro del grupo `vboxusers` para acceder a dispositivos USB.

```bash
sudo usermod -aG vboxusers $USER && newgrp vboxusers
```

Después de ejecutar esto, **cierra sesión y vuelve a iniciarla** (o reinicia) para que el cambio de grupo surta efecto. Puedes verificar con:

```bash
groups $USER
```

La salida debe incluir `vboxusers`.

### Habilitar el Controlador USB en Configuración de VM

1. Apaga tu VM de Kali si está en funcionamiento.
2. Selecciona la VM, haz clic en **Configuración → USB**.
3. Marca **Habilitar Controlador USB**.
4. Selecciona **Controlador USB 3.0 (xHCI)** de los botones de radio.

{{< alert "circle-info" >}}
USB 3.0 (xHCI) es necesario para el AWUS036AXML. Para el AWUS036ACH, USB 2.0 (EHCI) es técnicamente suficiente ya que el adaptador en sí es USB 2.0, pero usar xHCI no causa problemas y mantiene tu configuración consistente.
{{< /alert >}}

### Añadir un Filtro de Dispositivo USB

Un filtro de dispositivo USB le indica a VirtualBox que capture automáticamente el adaptador ALFA cada vez que se conecte, sin intervención manual en cada sesión.

1. En el mismo panel de **Configuración → USB**, haz clic en el icono **+** (Añadir filtro USB desde dispositivo).
2. Conecta tu adaptador ALFA ahora si no está ya conectado. VirtualBox lo mostrará en el menú desplegable.
3. Selecciona el dispositivo. Normalmente aparece como **"Realtek 802.11ac NIC"** (AWUS036ACH) o **"MediaTek Corp. 802.11 b/g/n"** (AWUS036AXML).
4. Haz clic en **Aceptar** para guardar.

### Iniciar la VM y Verificar con lsusb

Inicia tu VM de Kali. Una vez que el escritorio cargue, abre una terminal y ejecuta:

```bash
lsusb
```

Deberías ver una línea similar a:

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

o para AWUS036AXML:

```
Bus 002 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

### Cargar el Controlador

**AWUS036ACH (RTL8812AU):**

```bash
sudo modprobe 88XXau
```

Si falla (módulo no encontrado), instala el paquete DKMS primero:

```bash
sudo apt update && sudo apt install -y realtek-rtl88xxau-dkms
sudo modprobe 88XXau
```

**AWUS036AXML (MT7921AU):**

```bash
sudo modprobe mt7921u
```

### Verificar el Modo Monitor

```bash
sudo airmon-ng start wlan1
sudo iwconfig wlan1mon
```

El campo **Mode** debe mostrar `Monitor`.

### Errores Comunes en VirtualBox

| Error | Causa | Solución |
|---|---|---|
| "No hay dispositivos USB disponibles" en configuración USB | Extension Pack no instalado o versión no coincide | Instalar la versión correcta del Extension Pack |
| Adaptador no capturado / no visible en lsusb | Usuario no está en el grupo `vboxusers` (host Linux) | `sudo usermod -aG vboxusers $USER`, luego cerrar/abrir sesión |
| "El dispositivo USB está ocupado con una solicitud anterior" | Otro proceso en el host está usando el dispositivo | Desconectar y reconectar el adaptador antes de iniciar la VM |
| El dispositivo sigue desconectándose dentro de la VM | Controlador USB 3.0 no habilitado; VM usando OHCI | Cambiar a USB 3.0 (xHCI) en Configuración VM → USB |
| Filtro añadido pero el dispositivo no se captura automáticamente | Filtro creado antes de instalar el Extension Pack | Eliminar el filtro, instalar Extension Pack, re-añadir el filtro |

---

## USB Passthrough en VMware Workstation / VMware Fusion

VMware maneja el USB passthrough de forma diferente a VirtualBox. No hay una extensión separada que instalar — el soporte USB 2.0 y 3.0 está integrado en VMware Workstation 17+ y Fusion 13+. El mecanismo principal es el **servicio USB Arbitrator**, que monitorea los eventos USB del host y enruta los dispositivos a las VMs.

### Conectar el Adaptador a través del Menú de Dispositivos

Cuando conectas tu adaptador ALFA mientras una VM está en ejecución, VMware normalmente muestra un popup preguntando qué VM debe poseer el dispositivo. Si lo pierdes:

1. Con la VM de Kali en ejecución, ve a **VM → Dispositivos Extraíbles** en la barra de menú.
2. Expande la lista, localiza tu adaptador ALFA (p.ej., **Realtek 802.11ac NIC**).
3. Haz clic en **Conectar (Desconectar del Host)**.

### VMware Fusion (macOS)

1. Ve a **Máquina Virtual → USB y Bluetooth**.
2. Localiza el adaptador ALFA en la lista.
3. Cambia la conexión a **Conectar a Linux** (o el nombre de tu VM de Kali).

### Verificar y Cargar el Controlador

Una vez conectado, verifica dentro de Kali:

```bash
lsusb
```

Luego carga el controlador apropiado como se describe en la sección de VirtualBox arriba.

### Verificar el Servicio USB Arbitrator de VMware

Si el adaptador ALFA no aparece en el menú **Dispositivos Extraíbles**, es posible que el servicio USB arbitrator no esté en ejecución. En hosts Linux:

```bash
sudo systemctl status vmware-usbarbitrator
```

Si está detenido:

```bash
sudo systemctl start vmware-usbarbitrator
sudo systemctl enable vmware-usbarbitrator
```

### Habilitar USB 3.0 en VMware

Abre el archivo `.vmx` de tu VM de Kali y confirma o añade:

```
usb_xhci.present = "TRUE"
```

{{< alert "triangle-exclamation" >}}
Se requiere la versión de hardware de VMware 14 o posterior para el soporte USB 3.0 (xHCI). Si tu VM fue creada con una versión de hardware más antigua, actualízala mediante **VM → Administrar → Cambiar compatibilidad de hardware**.
{{< /alert >}}

### Errores Comunes en VMware

| Error | Causa | Solución |
|---|---|---|
| Adaptador no en el menú de Dispositivos Extraíbles | USB arbitrator no en ejecución | Iniciar el servicio `vmware-usbarbitrator` |
| El dispositivo se conecta y desconecta inmediatamente | El controlador del SO host recupera el dispositivo | Deshabilitar el controlador WiFi del host para el adaptador, o reconectar más rápido |
| "El dispositivo ya está en uso por el host" | El SO host reclamó el dispositivo | Expulsar del host antes de conectar en la VM |
| Sin velocidad USB 3.0 dentro de la VM | Versión de hardware de VM < 14 o xHCI no habilitado | Actualizar versión de hardware, añadir `usb_xhci.present = "TRUE"` al .vmx |
| El modo monitor falla incluso después del passthrough | Controlador incorrecto o faltante dentro de Kali | Seguir la [Guía de Instalación del Controlador](/es/blog/install-alfa-driver-kali-ubuntu/) |

---

## Notas Específicas por Adaptador

### AWUS036ACH (RTL8812AU)

El AWUS036ACH es un dispositivo **USB 2.0** y es uno de los adaptadores más probados en entornos VM. Tanto VirtualBox como VMware lo gestionan de forma fiable. Paquete de controlador: `realtek-rtl88xxau-dkms`. Nombre del módulo: `88XXau`.

### AWUS036AXML (MT7921AU)

El AWUS036AXML es un dispositivo **USB 3.0** que soporta WiFi 6E y tiene algunos casos especiales en entornos VM. **Debe** usar el controlador USB 3.0 (xHCI). Paquete de firmware: `firmware-misc-nonfree`. Algunas unidades tempranas experimentan congelaciones periódicas bajo la arbitrariedad USB 3.0 de VirtualBox. VMware Workstation tiende a manejar el AWUS036AXML de forma más fiable que VirtualBox para USB 3.0 passthrough.

Revisión completa: [Revisión AWUS036AXML WiFi 6E](/es/blog/awus036axml-wifi-6e-review/).

### AWUS036ACM (RTL8812AU, Antena Única)

Se comporta de forma idéntica al AWUS036ACH desde la perspectiva del controlador y el passthrough. Usa el mismo módulo `88XXau` y la misma configuración de VirtualBox/VMware.

---

## Consejos de Rendimiento

**Deshabilitar el autosuspend de USB en el host:**

```bash
echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend
```

**Asignar recursos adecuados a la VM:**
- **Al menos 2 núcleos de CPU** (4 recomendados)
- **2 GB de RAM** (4 GB si ejecutas escritorio completo de Kali)

**Tomar un snapshot de la VM antes de los compromisos de pentesting.**

{{< alert "circle-info" >}}
Para sesiones de captura superiores a 30 minutos, considera usar un hub USB con alimentación propia entre el adaptador y tu host. Proporciona energía estable y previene caídas de voltaje que pueden causar que el adaptador se desconecte durante capturas críticas.
{{< /alert >}}

---

## Comparativa Honesta: Bare Metal vs VM

| Característica | Kali Bare Metal | VirtualBox + Kali | VMware + Kali |
|---|---|---|---|
| **Soporte de controladores** | Completo, directo | Bueno (con Extension Pack) | Bueno (USB integrado) |
| **Estabilidad modo monitor** | Excelente | Bueno | Bueno–Excelente |
| **Fiabilidad inyección de paquetes** | Excelente | Bueno (pérdida de frames ocasional) | Bueno–Excelente |
| **Tiempo de configuración** | Alto (hardware dedicado) | Bajo–Medio | Bajo–Medio |
| **Portabilidad** | Baja | Alta (snapshots, portátil) | Alta |
| **Uso en CTF / laboratorio** | Excesivo | Ideal | Ideal |
| **Pentesting profesional** | Recomendado | Aceptable | Aceptable |

---

## Referencia Rápida de Solución de Problemas

| Síntoma | Causa más probable | Solución |
|---|---|---|
| `lsusb` no muestra nada dentro de Kali | USB passthrough no configurado | Añadir filtro USB (VBox) o conectar vía Dispositivos Extraíbles (VMware) |
| "No hay dispositivos USB" en configuración VirtualBox | Extension Pack faltante o versión no coincide | Instalar Extension Pack coincidente |
| Adaptador visible en `lsusb` pero sin interfaz `wlan` | Controlador no cargado | `sudo modprobe 88XXau` o `sudo modprobe mt7921u` |
| `modprobe: FATAL: Module 88XXau not found` | Paquete DKMS no instalado | `sudo apt install realtek-rtl88xxau-dkms` |
| La interfaz aparece y desaparece | Autosuspend USB o arbitrariedad VBox xHCI | Deshabilitar autosuspend; probar controlador USB 2.0 para ACH |
| `airmon-ng` inicia pero el modo monitor falla silenciosamente | Controlador incorrecto o conflicto con network manager | `sudo airmon-ng check kill`, luego reintentar |
| El filtro USB de VirtualBox no captura al arrancar | Filtro añadido antes de instalar Extension Pack | Eliminar filtro, instalar Extension Pack, re-añadir |
| VMware pierde el dispositivo durante sesiones largas | El servicio USB arbitrator de VMware se detiene | Re-habilitar y configurar para inicio automático |

---

## Próximos Pasos

- **Instalar o actualizar el controlador:** [Guía de Instalación del Controlador ALFA para Kali y Ubuntu](/es/blog/install-alfa-driver-kali-ubuntu/)
- **Configuración completa del AWUS036ACH:** [Guía de Configuración AWUS036ACH Kali Linux](/es/blog/awus036ach-kali-linux-setup/)
- **Revisión de hardware del AWUS036AXML:** [Revisión AWUS036AXML WiFi 6E](/es/blog/awus036axml-wifi-6e-review/)
