---
title: "¿Su máquina virtual Kali Linux no detecta el adaptador USB externo? Guía de diagnóstico de USB Pass-through en VirtualBox/VMware"
description: "Manual de diagnóstico estandarizado de USB Pass-through: Extension Pack de VirtualBox, controlador USB 3.0 (xHCI), grupo vboxusers, arbitraje USB de VMware, flujo de diagnóstico lsusb→iwconfig→dmesg y preguntas frecuentes."
date: 2026-08-31
author: benny-lai
lastmod: 2026-08-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "wireless-adapter", "virtual-machine"]
featureimage: /images/blog/vm-kali-linux-usb-passthrough-troubleshooting-guide.webp
faq:
  - question: "Cambié el adaptador a otro puerto USB y ahora lsusb no muestra nada. ¿Está dañado el adaptador?"
    answer: "No necesariamente. Compruebe primero si lo conectó a un puerto «solo de carga» o si el host puso el dispositivo en reposo para ahorrar energía. Vuelva a conectarlo a un puerto USB estándar del panel trasero de la placa base, o desenchúfelo y vuelva a enchufarlo una vez; normalmente con eso se restablece."
  - question: "El icono USB en la esquina inferior derecha de la ventana de la VM está vacío. ¿Qué debo hacer?"
    answer: "Compruebe en orden: ① que la versión del Extension Pack coincida exactamente con la de VirtualBox; ② que en hosts Linux su usuario esté en el grupo vboxusers (requiere volver a iniciar sesión); ③ que el host siga viendo el adaptador con lsusb; ④ que ningún otro software (como una utilidad de controladores del host) esté reteniendo el dispositivo."
  - question: "Después de configurar un filtro USB, el host ya no puede usar el adaptador. ¿Es normal?"
    answer: "Sí, es lo esperado. Una vez que el dispositivo se pasa al Guest, el control pertenece al Guest y el host no puede usarlo al mismo tiempo. Cuando necesite el adaptador de nuevo en el host, libérelo (release) desde el icono USB de la ventana de la VM."
  - question: "lsusb dentro del Guest muestra el adaptador, pero no hay interfaz wlan. ¿Qué controlador debo instalar?"
    answer: "Depende del chipset: el AWUS036AXML (MediaTek MT7921AU) usa el controlador mt7921u integrado en el kernel — plug-and-play en Kernel 5.18+; primero asegúrese de que apt install linux-firmware esté actualizado. El AWUS036ACH (Realtek RTL8812AU) usa un controlador fuera del árbol (out-of-tree) — instale el aircrack-ng/rtl8812au mantenido por la comunidad y compílelo con DKMS (y gestione el firmado MOK para Secure Boot; no desactive Secure Boot)."
  - question: "¿Por qué el Guest no arranca después de seleccionar el controlador USB 3.0?"
    answer: "Algunos kernels antiguos de Guest tienen un soporte deficiente de xHCI. Si su Kali es una versión antigua, pruebe: apagar → volver a USB 2.0 (EHCI) Controller → arrancar → actualizar el kernel → volver a USB 3.0. Mantenga Kali lo más actualizado posible para obtener el soporte xHCI más completo."
  - question: "El adaptador es rápido en una máquina física pero lento dentro de la VM. ¿Es normal?"
    answer: "Sí. Dentro de una VM el adaptador rinde aproximadamente a la velocidad del reenvío por la capa de emulación USB, lo que añade algo de sobrecarga (overhead) frente a una conexión directa en una máquina física. Un controlador USB 3.0 (xHCI) correcto y un Hypervisor actualizado mantienen esa sobrecarga al mínimo. Si el rendimiento es muy bajo, confirme primero que el controlador no esté atascado en USB 1.1."
---

> **Plataformas compatibles**: hosts Windows / Linux / macOS con Oracle VirtualBox / VMware Workstation (Guest = Kali Linux / Debian / Ubuntu)
> **Hardware de referencia**: ALFA AWUS036ACH (Realtek RTL8812AU) / ALFA AWUS036AXML (MediaTek MT7921AU)
> **Alcance de este artículo**: manual de diagnóstico estandarizado de «USB Pass-through». Las limitaciones del USB Pass-through en hosts macOS se explican en el capítulo 5.

---

{{< tldr >}}

Muchos usuarios de Kali conectan el adaptador al host y, sin embargo, no ven ninguna interfaz inalámbrica dentro de la máquina virtual. **En la mayoría de los casos la causa es una de tres razones muy comunes**; la probabilidad de que el adaptador esté dañado es baja:

1. **El Extension Pack de VirtualBox no está instalado**: sin él, el Guest no puede usar los controladores USB 2.0/3.0 en absoluto (el límite de velocidad de USB 1.1 es de solo 12 Mbps, insuficiente para un adaptador).
2. **El USB Pass-through no está configurado**: el host «acapara» todos los dispositivos USB por defecto. El Guest necesita un montaje manual o un «filtro USB (VM USB Filter)» que se haga cargo del adaptador automáticamente.
3. **El controlador dentro del Guest no está cargado**: la capa USB pasó (`lsusb` lo ve), pero Linux no tiene el controlador correspondiente, así que `ip link` no muestra ninguna interfaz `wlan`.

Orden de diagnóstico: primero el hardware del host, luego el Pass-through del Guest y por último la capa de controladores — la regla mnemotécnica completa está en 1.3.

{{< /tldr >}}

---

## 1. ¿Por qué la máquina virtual no usa por defecto el adaptador inalámbrico del host?

### 1.1 Su adaptador USB «a la vez» pertenece a un solo sistema operativo

USB funciona con una arquitectura de **host único (single host)**: un dispositivo USB solo puede ser controlado por un «controlador host (Host Controller)» en un mismo momento. Cuando el adaptador está conectado al host, el dispositivo es enumerado (enumerate) y asumido primero por el **sistema operativo del host (Host OS)**. El controlador del host lo reconoce y lo controla.

La máquina virtual (Guest VM) no es un dispositivo físico en el bus USB; es «hardware falso» que el hipervisor (Hypervisor) representa dentro del host. Por eso, para que el Guest use el adaptador USB, **el host debe «entregar» el dispositivo al Guest de forma activa** — este mecanismo se llama **USB Pass-through (USB Redirection)**.

### 1.2 ¿Qué atraviesa realmente el USB Pass-through?

Con VirtualBox, el flujo del Pass-through es el siguiente:

```
Adaptador USB físico (AWUS036ACH / AWUS036AXML)
       │  conectado a un puerto USB físico del host
       ▼
Controlador host USB del sistema operativo del host (Host OS)
       │  el Hypervisor (VirtualBox) lo intercepta y redirige
       ▼
Controlador host USB virtual (EHCI / xHCI emulado)
       │  el Guest (Kali) lo ve «como si estuviera conectado a sí mismo»
       ▼
Controlador USB de Kali → controlador inalámbrico → interfaz wlan
```

Tras un Pass-through exitoso, **el control del dispositivo en el host se transfiere al Guest**; el host se comporta como si el dispositivo hubiera sido «retirado» y ya no puede usarlo. En el Guest, en cambio, aparece como un dispositivo USB completamente nuevo. **Esto es un comportamiento normal, no un bug.** Un dispositivo USB del host no puede usarse en ambos lados a la vez.

### 1.3 «No lo detecta» tiene en realidad tres niveles

| Nivel | Herramienta de comprobación | Síntoma | Significado |
|-------|----------------------------|---------|-------------|
| **Nivel de Pass-through USB** | `lsusb` dentro del Guest | `lsusb` no muestra el VID:PID del adaptador en absoluto | Falló el Pass-through (problema de Extension Pack / controlador / filtro) |
| **Nivel de controlador** | `dmesg` dentro del Guest | `lsusb` lo ve, pero `dmesg` muestra errores (falta firmware, `Required key not available`) | Falta el controlador dentro del Guest o el módulo no cargó |
| **Nivel de interfaz inalámbrica** | `iwconfig` / `ip link` dentro del Guest | `lsusb` y `dmesg` están bien, pero no hay interfaz `wlan` | El controlador cargó pero la interfaz no se registró, o hay un problema de modo/configuración |

> **Regla mnemotécnica**: primero mire `lsusb` para saber «si el dispositivo pasó al Guest» y luego `ip link` para saber «si el controlador lo reconoce». **No empiece sospechando que el adaptador está dañado.**

---

## 2. VirtualBox: instale primero el Extension Pack y luego configure el controlador USB 3.0

### 2.1 El paquete de extensión (Extension Pack) es imprescindible

El paquete base de VirtualBox **solo incluye la emulación del controlador USB 1.1 (OHCI)**, y la velocidad de transferencia de USB 1.1 no es suficiente para un adaptador. **Los controladores USB 2.0 (EHCI) y USB 3.0 (xHCI) solo están disponibles con el «paquete de extensión (Extension Pack)» oficial de Oracle.**

Los síntomas de no tener el Extension Pack son típicos: en la configuración del Guest no se puede elegir el controlador USB 2.0 / USB 3.0, o al montar el adaptador aparece «fallo de conexión del dispositivo a la máquina virtual (error code E_FAIL / VERR_PDM_NO_USB_PORTS)».

### 2.2 La versión debe coincidir «exactamente»

La versión del Extension Pack **debe coincidir exactamente con la versión del programa principal de VirtualBox** (por ejemplo, VirtualBox 7.0.20 requiere el Extension Pack 7.0.20). Incluso una diferencia de una versión menor puede provocar un fallo de instalación o de carga.

```bash
# Ver la versión actual de VirtualBox
vboxmanage --version
```

Descargue el `Oracle_VM_VirtualBox_Extension_Pack-<versión>.vbox-extpack` correspondiente desde la página oficial de descargas de Oracle (https://www.virtualbox.org/wiki/Downloads) y luego:

```bash
# Opción 1: instalación por GUI (programa principal de VirtualBox → Archivo → Herramientas → Extension Pack Manager → Instalar)
# Opción 2: instalación por comando
sudo VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-*.vbox-extpack

# Confirmar la instalación
VBoxManage list extpacks
```

> Durante la instalación se muestra la licencia de Oracle (Personal Use and Evaluation License); el uso personal es gratuito; en entornos comerciales, siga los términos de la licencia.

### 2.3 Host Linux: añádase al grupo vboxusers

En un host Linux, para que VirtualBox acceda a los dispositivos USB, **el usuario debe pertenecer al grupo `vboxusers`**. Muchas personas instalan el paquete de extensión y aun así fallan: el bloqueo está en los permisos.

```bash
# Unirse al grupo (sustituya <user> por su nombre de usuario)
sudo usermod -aG vboxusers $USER

# Cerrar sesión y volver a iniciarla (o reiniciar) para que el grupo surta efecto; comprobarlo
id $USER
```

### 2.4 Configurar el controlador USB 3.0 (xHCI)

1. Seleccione su máquina virtual Kali → **Configuración (Settings) → Puertos (Ports) → USB**.
2. Marque «Enable USB Controller» y elija **USB 3.0 (xHCI) Controller**.
   - El AWUS036AXML es de especificación USB 3.2 Gen 1 (USB-C): **seleccione obligatoriamente USB 3.0 (xHCI)**; elegir USB 2.0 limitará la velocidad de transferencia.
   - El AWUS036ACH es de interfaz USB Type-A y funciona con los controladores USB 2.0 y USB 3.0; para una mejor velocidad de transferencia, elija también USB 3.0 (xHCI).
3. Tras modificar el controlador, **apague y encienda** (no ejecute un reinicio dentro del Guest) para aplicar los cambios.

### 2.5 Montaje manual y comparación con VMware

Al iniciar la máquina virtual Kali, fíjese en el **icono USB de la esquina inferior derecha de la ventana** (una clavija USB):

1. Haga clic en el icono USB → se mostrarán los dispositivos USB actualmente conectados al host.
2. Su adaptador debería aparecer como `Realtek 802.11ac NIC` (ACH) o `ALFA AWUS036AXML` / MediaTek (AXML).
3. Haga clic en él una vez y el dispositivo se «entregará» a Kali.

Si la lista está vacía, hay un problema en la capa de Pass-through: vuelva a comprobar 2.2 / 2.3 / 2.4 (incluido el controlador USB no habilitado) o ejecute directamente la hoja de trabajo del capítulo 6.

**Comparación con VMware**: VMware Workstation / Fusion **no necesita** un paquete de extensión adicional para el USB Pass-through, pero hay dos puntos de comprobación habituales:

1. **Servicio del host**: en hosts Linux, confirme que `vmware-usbarbitrator` (el servicio de arbitraje USB) está en ejecución:
   ```bash
   sudo systemctl status vmware-usbarbitrator
   # Si no está en ejecución, inícielo y actívelo para el arranque automático
   sudo systemctl enable --now vmware-usbarbitrator
   ```
2. **Configuración de la máquina virtual**: Configuración de la VM → USB Controller → marque **USB 3.1 (o USB 3.0)**.
3. **Conexión manual**: menú de la ventana de VMware → **Dispositivos extraíbles (Removable Devices) → su adaptador → Conectar (Connect)**.

> **Punto clave de comparación**: VirtualBox se atasca en «no hay Extension Pack instalado»; VMware se atasca en «el servicio de arbitraje no está en ejecución» o «el controlador USB 3.0 no está activado». Confirme primero qué producto usa y luego revise el punto correspondiente.

---

## 3. Tres pasos con herramientas de diagnóstico: lsusb → iwconfig → dmesg

Tras completar la configuración del Pass-through, use tres comandos para localizar el problema en la «capa de Pass-through» o en la «capa de controladores».

### Paso 0: confirme primero el hardware en el host (no culpe al adaptador)

Abra una terminal en el **sistema operativo del host** y ejecute:

```bash
lsusb
```

Resultado esperado (según el modelo):

```
# AWUS036ACH (Realtek RTL8812AU)
Bus ... ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
# o AWUS036AXML (MediaTek MT7921AU)
Bus ... ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

- El host lo ve → el hardware y el cable están bien; el problema está en el Pass-through o en el controlador del Guest.
- El host tampoco lo ve → **revise primero el host** (cambie de puerto USB, cambie de cable, haga una prueba cruzada en otro equipo) y luego considere abrir un ticket de soporte.

### Paso 1: lsusb en el Guest — ¿el Pass-through tuvo éxito?

Ejecute **dentro de la máquina virtual Kali**:

```bash
lsusb
```

- Ve el mismo VID:PID → **Pass-through exitoso**, vaya al paso 2.
- No lo ve → **Pass-through fallido**: vuelva al capítulo 2 (Extension Pack / controlador / grupo vboxusers) o compruebe si otro software del host está ocupando el adaptador.

### Paso 2: iwconfig / ip link — ¿apareció la interfaz inalámbrica?

```bash
iwconfig
# o (versiones más recientes)
iw dev
ip link
```

- Aparece una interfaz `wlan0` / `wlx...` → **todo conectado**, puede empezar a usarlo.
- No hay interfaz inalámbrica pero `lsusb` lo ve → el problema está en la **capa de controladores del Guest**; vaya al paso 3.

### Paso 3: dmesg — ¿por qué falló la capa de controladores?

```bash
# Observar los mensajes recientes del kernel
sudo dmesg | tail -30
# Filtrar los mensajes relacionados con USB y redes inalámbricas
sudo dmesg | grep -iE "usb|wlan|8812|mt7921|rtl" | tail -30
```

Comparación de resultados habituales de `dmesg`:

| Mensaje de `dmesg` | Causa | Solución |
|--------------------|-------|----------|
| `usb 3-1: new high-speed USB device ...` sin nada después | El dispositivo se enumeró, pero no hay controlador disponible | Instale el controlador correspondiente dentro del Guest (ver FAQ Q4) |
| `Direct firmware load failed` / `firmware_loading` | Falta el archivo de firmware | `apt install firmware-realtek` y vuelva a cargar el módulo |
| `Required key not available` | Secure Boot activado y el módulo no está firmado | Firme con una clave MOK (no desactive Secure Boot) |
| `disagrees about version of symbol` | La versión del controlador no coincide con el kernel | Recompile e instale con DKMS |

> **Comprensión clave**: que `lsusb` vea el dispositivo solo demuestra que «el USB Pass-through funcionó»; **no significa que el controlador esté cargado**. El caso habitual de «Pass-through exitoso pero sin wlan» es exactamente esto: no hay controlador correspondiente dentro del Guest.

---

## 4. Filtro USB de la VM: montaje automático al conectar + problemas de desconexión

### 4.1 ¿Por qué configurar un filtro USB (USB Filter)?

El problema del montaje manual (capítulo 2, 2.5): **hay que volver a hacer clic cada vez que se reinicia la máquina virtual Kali**. Con un «filtro USB» configurado, en cuanto el adaptador se conecta (o la VM arranca), VirtualBox **transfiere automáticamente los dispositivos que coinciden al Guest**.

Método de configuración (VirtualBox):

1. Configuración de la VM → USB → haga clic en **«+» para añadir un filtro → seleccione su adaptador**.
2. VirtualBox rellena automáticamente una regla de filtro (campos de ID de proveedor / ID de producto / número de serie):
   - **Nombre (Name)**: por ejemplo `ALFA AWUS036AXML` o `AWUS036ACH`
   - **ID de proveedor (Vendor ID)**: `0bda` para AWUS036ACH, `0e8d` para AWUS036AXML
   - **ID de producto (Product ID)**: `8812` para AWUS036ACH, `7961` para AWUS036AXML
3. Si tiene varios adaptadores del mismo modelo, complete también el campo «número de serie (Serial Number)» para evitar filtrar el otro.

> Consejo: haga clic derecho en el filtro → **Editar filtro**; puede dejar solo el Vendor ID y el Product ID (coincidencia flexible) o añadir el número de serie (coincidencia exacta).

### 4.2 Desconexiones frecuentes: normalmente es un problema de alimentación o del controlador

Los adaptadores de alta potencia (el AWUS036ACH consume una corriente transitoria mayor durante monitorización/inyección; el AWUS036AXML es de especificación USB 3) pueden sufrir ocasionalmente «pérdida del dispositivo / desconexión» dentro de la VM. Estas son las causas y soluciones típicas:

| Síntoma | Causa | Solución |
|---------|-------|----------|
| Falta de alimentación tras el Pass-through y pérdidas constantes | La capacidad de alimentación que emula el controlador USB virtual es conservadora, o el puerto del host no suministra suficiente | Use en el host un **puerto USB del panel trasero de la placa base** o un Hub USB con alimentación independiente |
| El adaptador aparece y desaparece | El **ahorro de energía USB (autosuspend)** del host durmió el dispositivo | Desactive en la configuración del host la suspensión automática USB «de ese dispositivo» (no desactive las protecciones de seguridad generales del sistema) |
| Fallo inmediato al montar con una serie de error code | Controlador mal elegido (USB 1.1/2.0 no soporta un dispositivo USB 3) | Cambie a «USB 3.0 (xHCI) Controller» y reinicie tras apagar |
| El adaptador falla al despertar el host de la suspensión (sleep) | La redirección USB del Hypervisor se rompió durante la suspensión del host | Evite la suspensión del host durante el uso; o vuelva a montar una vez tras despertar |

### 4.3 Recordatorio de seguridad

Para reducir las pérdidas de dispositivo, puede desactivar la suspensión automática de **un único dispositivo USB**, pero solo a nivel de «ese dispositivo». **No** desactive las protecciones de seguridad a nivel de sistema (firewall, Secure Boot) para ahorrarse molestias: el coste sería desproporcionado.

---

## 5. Limitaciones del host macOS y límites de plataforma

### 5.1 El USB Pass-through en hosts macOS tiene limitaciones inherentes

Ejecutar una máquina virtual desde un host macOS con USB Pass-through es **la combinación con más probabilidades de atascarse**. Compruebe primero su situación:

| Host macOS | VirtualBox | VMware Fusion |
|------------|-----------|---------------|
| **Apple Silicon (M1/M2/M3/M4)** | ⚠️ **Soporte de USB Pass-through limitado / incompleto** — una de las limitaciones conocidas anunciadas oficialmente; incluso con el controlador del adaptador en buen estado, la capa de Pass-through puede no funcionar directamente | ⚠️ Soporte más completo, pero se recomienda primero «conectar directamente al host» para confirmar que el adaptador funciona en macOS |
| **Intel (Intel Mac)** | ✅ Disponible, pero primero debe completar el proceso de **aprobación de extensiones de kernel (Kernel Extension)** (Ajustes del sistema → Seguridad y privacidad → permitir las extensiones de kernel relacionadas con Oracle) e instalar el Extension Pack exactamente coincidente con la versión | ✅ Disponible |

**Recomendación**: si su host es macOS, haga de «conectar directamente al host → `system_profiler SPUSBDataType` → confirmar que el adaptador funciona en el host» la primera puerta de todo diagnóstico. **No incluya en la lista de diagnóstico de la VM los modelos no compatibles con macOS**; perderá mucho tiempo.

### 5.2 Límites de plataforma (Support Boundary)

| Plataforma | Estado de soporte | Explicación |
|------------|-------------------|-------------|
| Host Windows + VirtualBox / VMware + Guest Kali | ✅ Soportado | Todos los procedimientos de este capítulo aplican |
| Host Linux + VirtualBox / VMware + Guest Kali | ✅ Soportado | Recuerde el grupo vboxusers (VB) y el servicio vmware-usbarbitrator (VMware) |
| **macOS (Apple Silicon)** + VirtualBox | ⚠️ **USB Pass-through limitado** | Se recomienda cambiar a VMware Fusion o usar un host Linux／Windows |
| macOS (Intel) + VirtualBox | ✅ Soportado | Requiere aprobación de extensiones de kernel + Extension Pack coincidente con la versión |
| **Guest es macOS** | ❌ No recomendado | Este artículo asume Guests Linux como Kali / Debian / Ubuntu |

> **Límite de soporte**: al diagnosticar, confirme siempre primero «si el adaptador funciona en el host» y luego hable de los problemas de configuración de la VM. Si el host no detecta el adaptador, ninguna configuración de la VM lo arreglará — el siguiente paso entonces es un problema de controlador del host (puede consultar otros artículos de diagnóstico de controladores de este sitio).

---

## 6. Hoja de trabajo estándar de diagnóstico: ejecútela antes de abrir un ticket (Intake de soporte)

> Cuando se encuentre con «la VM no detecta el adaptador», complete la siguiente tabla en orden y anote los resultados. **Ejecute toda la hoja de trabajo antes de decidir si abre un ticket de soporte técnico** — muchas veces se resuelve solo, y además reduce drásticamente el tiempo de ida y vuelta con el soporte.

### Paso 1: comprobación del hardware del host

| Elemento | Comando | Campo de registro |
|----------|---------|-------------------|
| Sistema operativo y arquitectura del host | `uname -a` / `systeminfo` | \_\_\_\_\_ |
| ¿El host ve el adaptador? | `lsusb` en el host | VID:PID \_\_\_\_\_ |
| Puerto USB y cable | Cambie de puerto y de cable y pruebe de nuevo | Resultado \_\_\_\_\_ |

### Paso 2: comprobación de la capa de virtualización (Hypervisor)

| Elemento | Acción | Campo de registro |
|----------|--------|-------------------|
| Software de virtualización y versión | VirtualBox: `vboxmanage --version` ／ VMware: Help → About | \_\_\_\_\_ |
| ¿Coincide la versión del Extension Pack? | VirtualBox: `VBoxManage list extpacks` | Versión \_\_\_\_\_ |
| Permisos / servicios del host | Host Linux: `id` para ver vboxusers; VMware: `systemctl status vmware-usbarbitrator` | \_\_\_\_\_ |
| Configuración del controlador USB | VirtualBox: ¿USB 3.0 (xHCI) Controller marcado? | Sí / No |

### Paso 3: comprobación del resultado del Pass-through

| Elemento | Comando | Campo de registro |
|----------|---------|-------------------|
| ¿El Guest ve el adaptador? | `lsusb` dentro del Guest | \_\_\_\_\_ |
| ¿Apareció la interfaz inalámbrica? | `iwconfig` / `ip link` dentro del Guest | \_\_\_\_\_ |
| Mensajes de la capa de controladores | `sudo dmesg \| tail -30` dentro del Guest | \_\_\_\_\_ |
| Kernel del Guest en uso | `uname -r` | \_\_\_\_\_ |

### Paso 4: diagnóstico y registro

- `lsusb` (Guest) no lo ve → problema de **capa de Pass-through** → repase el capítulo 2 y el paso 2.
- `lsusb` lo ve pero `ip link` no muestra wlan → problema de **capa de controladores** → repase el paso 3 del capítulo 3.
- Todo normal pero inestable → problema de **alimentación / ahorro de energía / controlador** → capítulo 4.

### Paquete de información para el Intake de soporte

Antes de llamar al soporte técnico／enviar el ticket, adjunte la siguiente información de una vez para que el soporte entre directamente en materia:

> **SO del host + arquitectura, software de virtualización y versión, si el Extension Pack está instalado y su versión, salida de `lsusb` del host, salida de `lsusb` del Guest, salida de `ip link` / `iwconfig` del Guest, mensajes de `dmesg` relevantes, modelo del adaptador y método de conexión (USB-C / USB-A, directo o mediante Hub)**

---

## 7. Preguntas frecuentes (FAQ)

**P1: Cambié el adaptador a otro puerto USB y ahora `lsusb` no muestra nada. ¿Está dañado el adaptador?**
No necesariamente. Compruebe primero si lo conectó a un puerto «solo de carga» o si el host puso el dispositivo en reposo para ahorrar energía. Vuelva a conectarlo a un puerto USB estándar del panel trasero de la placa base, o desenchúfelo y vuelva a enchufarlo una vez; normalmente con eso se restablece.

**P2: El icono USB en la esquina inferior derecha de la ventana de la VM está vacío. ¿Qué debo hacer?**
Compruebe en orden: ① que la versión del Extension Pack coincida exactamente con la de VirtualBox; ② que en hosts Linux su usuario esté en el grupo `vboxusers` (requiere volver a iniciar sesión); ③ que el host siga viendo el adaptador con `lsusb`; ④ que ningún otro software (como una utilidad de controladores del host) esté reteniendo el dispositivo.

**P3: Después de configurar un filtro USB, el host ya no puede usar el adaptador. ¿Es normal?**
Sí, es lo esperado. Una vez que el dispositivo se pasa al Guest, el control pertenece al Guest y el host no puede usarlo al mismo tiempo. Cuando necesite el adaptador de nuevo en el host, libérelo (release) desde el icono USB de la ventana de la VM.

**P4: `lsusb` dentro del Guest muestra el adaptador, pero no hay interfaz wlan. ¿Qué controlador debo instalar?**
Depende del chipset:
- **AWUS036AXML (MediaTek MT7921AU)**: usa el controlador `mt7921u` integrado en el kernel — plug-and-play en Kernel 5.18+; primero asegúrese de que `apt install linux-firmware` esté actualizado.
- **AWUS036ACH (Realtek RTL8812AU)**: usa un controlador fuera del árbol (out-of-tree) — instale el `aircrack-ng/rtl8812au` mantenido por la comunidad y compílelo con DKMS (y gestione el firmado MOK para Secure Boot; no desactive Secure Boot).

**P5: ¿Por qué el Guest no arranca después de seleccionar el controlador USB 3.0?**
Algunos kernels antiguos de Guest tienen un soporte deficiente de xHCI. Si su Kali es una versión antigua, pruebe: apagar → volver a USB 2.0 (EHCI) Controller → arrancar → actualizar el kernel → volver a USB 3.0. Mantenga Kali lo más actualizado posible para obtener el soporte xHCI más completo.

**P6: El adaptador es rápido en una máquina física pero lento dentro de la VM. ¿Es normal?**
Sí. Dentro de una VM el adaptador rinde aproximadamente a la velocidad del reenvío por la capa de emulación USB, lo que añade algo de sobrecarga (overhead) frente a una conexión directa en una máquina física. Un controlador USB 3.0 (xHCI) correcto y un Hypervisor actualizado mantienen esa sobrecarga al mínimo. Si el rendimiento es muy bajo, confirme primero que el controlador no esté atascado en USB 1.1.

---

## 8. Conclusión y recomendaciones de hardware

Más del 90% de los casos de «la VM no detecta el adaptador externo» se deben a una **configuración de Pass-through** o a un **controlador del Guest** mal hecho; el fallo de hardware es raro. Ejecute las acciones de este artículo en orden:

1. **Confirme primero el hardware con `lsusb` en el host.**
2. **Instale siempre el Extension Pack de versión coincidente en VirtualBox** y únase al grupo `vboxusers` en hosts Linux; en VMware, confirme que el servicio `vmware-usbarbitrator` está en ejecución.
3. **Configure el controlador USB en USB 3.0 (xHCI)** y use un filtro USB para que el adaptador se monte automáticamente.
4. **Localice el nivel dentro del Guest con `lsusb → iwconfig / ip link → dmesg`**; si falta un controlador, instálelo — deje de adivinar que el adaptador está dañado.

**Hardware recomendado**: el ALFA AWUS036AXML (MediaTek MT7921AU) tiene en Kali con kernel más reciente un **controlador integrado en el kernel, plug-and-play**, y es el que menos molestias da tras el Pass-through en la VM. El ALFA AWUS036ACH (Realtek RTL8812AU) también es útil, pero recuerde compilar el controlador de la comunidad con DKMS dentro del Guest y gestionar el firmado de Secure Boot (puede consultar el artículo de diagnóstico DKMS de RTL8812AU de este sitio). Para ambos se recomienda usar en el host un puerto／Hub USB con alimentación independiente, para eliminar de una vez la variable de «pérdida del dispositivo».

**Siguiente paso**: guarde una copia de la hoja de trabajo del capítulo 6 en el escritorio de su máquina virtual Kali; cada vez que «no detecte el adaptador», ejecútela completa primero y luego decida si abre un ticket de soporte técnico — siga la tabla; los datos curan todo.

---

## Recursos de referencia

| Recurso | Enlace |
|---------|--------|
| Página oficial de descargas de Oracle VirtualBox (Extension Pack) | https://www.virtualbox.org/wiki/Downloads |
| Manual oficial de VirtualBox: configuración USB y filtros | https://www.virtualbox.org/manual/ (busque el capítulo «USB») |
| Manual de VirtualBox: limitaciones conocidas (incluidas las de USB Pass-through en Apple Silicon) | https://www.virtualbox.org/manual/ (Changelog / Limitations) |
| Comando de instalación del Extension Pack de VirtualBox | `vboxmanage help extpack` |
| Controlador comunitario aircrack-ng RTL8812AU (para AWUS036ACH dentro del Guest) | https://github.com/aircrack-ng/rtl8812au |
| Página oficial del producto ALFA AWUS036ACH | https://www.alfa.com.tw/products/awus036ach_1 |
| Página oficial del producto ALFA AWUS036AXML | https://www.alfa.com.tw/ |
| Soporte técnico de Yupitek | https://yupitek.com/ |

> **Declaración de uso legal**: activar operaciones de seguridad como el modo monitor y la inyección de paquetes dentro de la máquina virtual está limitado a redes de su propiedad o con autorización explícita para pruebas. El usuario debe cumplir las leyes locales y asegurarse de que todas las pruebas tengan una base de autorización legal.