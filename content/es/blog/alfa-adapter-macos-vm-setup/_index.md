---
title: "Cómo Usar Adaptadores WiFi ALFA en macOS: USB Passthrough con VMware Fusion y Parallels"
description: "Cómo usar adaptadores USB WiFi ALFA en macOS. Cubre soporte nativo de macOS, USB passthrough con VMware Fusion y Parallels Desktop para modo monitor e inyección de paquetes en Kali Linux."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["macos", "vmware-fusion", "parallels", "kali-linux", "usb-passthrough", "alfa-network", "AWUS036AXML"]
featureimage: "/images/blog/alfa-adapter-macos-vm-setup.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "¿Pueden las tarjetas de red ALFA usar el modo monitor de forma nativa en macOS?"
    answer: "No. La arquitectura CoreWLAN e IO80211Family de macOS no admite el modo monitor ni la inyección de paquetes para tarjetas de red de terceros. Debes ejecutar una VM de Kali Linux con tránsito USB."
  - question: "¿Para Mac con Apple Silicon, VMware Fusion o Parallels?"
    answer: "Ambos funcionan, pero Parallels Desktop 19+ suele tener mejor rendimiento de VM ARM64 y estabilidad de tránsito USB en Apple Silicon que VMware Fusion."
  - question: "¿El AWUS036AXML necesita compilación de controlador en una VM de Kali con Apple Silicon?"
    answer: "No. El controlador mt7921u está integrado en el núcleo desde Linux 5.18; Kali ARM64 2024.x y superior lo reconoce automáticamente al conectarlo."
  - question: "¿Puedo usar la ISO estándar de Kali x86_64 en un Mac Intel?"
    answer: "Sí. Los Mac Intel tienen arquitectura x86_64 y pueden usar directamente la ISO oficial de Kali Linux x86_64 de kali.org para crear la VM."
  - question: "¿Es VirtualBox adecuado para pruebas de seguridad en Apple Silicon?"
    answer: "No se recomienda. El soporte de VirtualBox para Apple Silicon sigue siendo experimental y el tránsito USB tiene problemas conocidos. Usa VMware Fusion o Parallels."
---

macOS es un sistema operativo pulido y listo para producción. Sin embargo, no es una plataforma diseñada para la investigación de seguridad inalámbrica. Las dos funciones que definen el kit de herramientas de todo pentester serio — **modo monitor** e **inyección de paquetes** — están completamente ausentes en la pila Wi-Fi de macOS. Los controladores Wi-Fi de Apple exponen una interfaz de red limpia y funcional, y nada más.

{{< tldr >}}
macOS no admite el modo monitor ni la inyección de paquetes de las tarjetas de red ALFA. La solución es ejecutar una VM de Kali Linux en VMware Fusion o Parallels y usar el tránsito USB para pasar la tarjeta a la VM. Apple Silicon requiere una imagen ARM64 de Kali.
{{< /tldr >}}

Los adaptadores ALFA Network cambian esa ecuación en Linux, donde el soporte de controladores es profundo y probado por la comunidad. En macOS, la situación es diferente. Incluso si un adaptador ALFA es reconocido por macOS, la pila de red nativa no te permitirá ponerlo en modo monitor ni inyectar tramas sin procesar. El único camino confiable es ejecutar **Kali Linux dentro de una máquina virtual** y pasar el adaptador USB directamente al SO invitado, omitiendo macOS por completo.

Esta guía explica cómo hacerlo correctamente en los dos principales hipervisores de macOS — VMware Fusion y Parallels Desktop — con atención especial a **Apple Silicon (M1/M2/M3)**, que introduce restricciones de arquitectura ARM que hacen que la selección de adaptador e imagen ISO no sea trivial.

---

## macOS Nativo: Qué Funciona Sin una VM

Antes de pasar directamente a la configuración de una VM, vale la pena entender qué puede y qué no puede hacer macOS con un adaptador ALFA por sí solo.

**AWUS036AXML (chipset MT7921AUN):** Este adaptador es reconocido por macOS como un dispositivo de red USB genérico. El controlador **MT7921AUN** incluido desde macOS 13 Ventura en adelante detecta el adaptador automáticamente. Aparece en **Preferencias del Sistema → Red** (o **Configuración del Sistema → Red** en Ventura+) como una nueva interfaz, y puede conectarse a redes Wi-Fi como cualquier otro adaptador. En versiones anteriores de macOS, puede que no sea reconocido en absoluto.

**AWUS036ACH (RTL8812AU) y AWUS036ACM (MT7612U) — adaptadores que requieren driver de terceros para macOS:** Estos requieren un controlador de terceros para macOS. Existen varios paquetes de controladores de la comunidad y comerciales, pero la compatibilidad es frágil. Las recompilaciones del controlador tras actualizaciones de punto de macOS son comunes, los requisitos de firma de extensiones del kernel se han endurecido desde macOS 11, y en Apple Silicon la situación es aún más precaria debido a las limitaciones de Rosetta con extensiones del kernel. La instalación funcional es posible pero requiere mucho mantenimiento.

**El límite estricto — sin modo monitor:** Independientemente del adaptador que uses o el controlador que instales, macOS no expone una interfaz de modo monitor sin procesar. El framework CoreWLAN y la arquitectura subyacente de `IO80211Family.kext` no lo soportan para adaptadores de terceros. Herramientas como Wireshark pueden capturar tráfico Wi-Fi en macOS usando el adaptador Airport integrado a través de `en0`, pero eso es solo captura pasiva — no es equivalente al modo monitor de airmon-ng, y la inyección de paquetes no es posible.

{{< alert "circle-info" >}}
Si tu objetivo es simplemente la captura pasiva de tráfico Wi-Fi con fines de depuración (no pruebas de seguridad), macOS sí permite mantener presionada la tecla Opción y hacer clic en el ícono de Wi-Fi en la barra de menú para entrar en un modo de diagnóstico. Esto no reemplaza un flujo de trabajo de modo monitor adecuado.
{{< /alert >}}

Para pruebas de seguridad — escaneo de redes, captura de handshakes WPA, ejecución de ataques de desautenticación o pruebas de inyección — una VM Kali Linux con USB passthrough es la configuración necesaria en macOS.

---

## Apple Silicon (M1/M2/M3) vs Mac Intel

La arquitectura de tu Mac determina qué imagen de Kali Linux necesitas y qué hipervisores son viables. Esta es la fuente más común de confusión para los usuarios de macOS que configuran una VM de pruebas de seguridad.

**Mac Intel (x86_64):**
Los tres principales hipervisores — VMware Fusion, Parallels Desktop y VirtualBox — se ejecutan de forma nativa en Macs Intel. Puedes usar la **ISO de Kali Linux x86_64** estándar de la página de descargas oficial de kali.org. La compilación de controladores dentro de la VM sigue los mismos pasos documentados en todas las guías de Kali en línea, porque la arquitectura coincide.

**Apple Silicon (M1/M2/M3):**
Apple Silicon es ARM64. Una ISO de Kali x86_64 estándar no arrancará en hardware Apple Silicon incluso dentro de un hipervisor — no hay capa de emulación x86 a nivel de VM (Rosetta solo aplica a aplicaciones macOS en espacio de usuario, no a la virtualización completa del SO). Debes usar la imagen **Kali Linux ARM64**, disponible en [kali.org/get-kali](https://www.kali.org/get-kali/) bajo la sección Apple Silicon / ARM.

| Hipervisor | Mac Intel | Apple Silicon |
|---|---|---|
| VMware Fusion 13+ | ✅ Licencia personal gratuita | ✅ VMs ARM64 compatibles |
| Parallels Desktop 19+ | ✅ | ✅ Mejor rendimiento en Apple Silicon |
| VirtualBox 7.x | ✅ | ⚠️ Experimental en Apple Silicon |

{{< alert "triangle-exclamation" >}}
El soporte de VirtualBox para Apple Silicon sigue marcado como experimental. El USB passthrough en particular tiene problemas conocidos en Macs con chip M. Para flujos de trabajo de pruebas de seguridad, usa VMware Fusion o Parallels Desktop en hardware Apple Silicon.
{{< /alert >}}

**El USB passthrough es independiente de la arquitectura:** El adaptador ALFA en sí es un dispositivo USB. El hecho de que la CPU anfitriona sea x86_64 o ARM64 no afecta cómo funciona el USB passthrough. El adaptador se entrega a la VM invitada a través del bus USB, y el controlador dentro de Kali lo gestiona desde ahí. La arquitectura solo afecta qué imagen de Kali usas y cómo se compilan los controladores dentro de la VM.

---

## Opción A: USB Passthrough con VMware Fusion

VMware Fusion está disponible de forma gratuita para uso personal desde Fusion 13, lo que lo convierte en la recomendación predeterminada para usuarios de macOS que desean un hipervisor sin costo con sólido soporte de USB passthrough.

### Paso 1 — Instalar VMware Fusion 13+

Descarga VMware Fusion desde [vmware.com/products/fusion.html](https://www.vmware.com/products/fusion.html). Durante la instalación, se te pedirá que permitas la extensión del sistema de VMware en **Preferencias del Sistema → Seguridad y Privacidad → General**. Esta aprobación de la extensión es necesaria para que el USB passthrough funcione — sin ella, VMware no puede interceptar eventos USB de la pila USB de macOS.

Tras la aprobación, macOS puede pedir un reinicio. Completa el reinicio antes de continuar.

### Paso 2 — Crear Tu VM de Kali Linux

- **Mac Apple Silicon:** Descarga el ISO del instalador de Kali Linux ARM64 o la imagen ARM precompilada para Parallels/VMware desde kali.org. En VMware Fusion, crea una nueva VM y selecciona el ISO ARM64.
- **Mac Intel:** Descarga el ISO del instalador de Kali Linux x86_64 estándar. Crea una nueva VM y selecciona el ISO como medio de instalación.

Asigna como mínimo **4 GB de RAM** y **40 GB de disco** para una instalación funcional de Kali. Durante la configuración de Kali, instala el conjunto de paquetes predeterminado completo para incluir las herramientas inalámbricas (aircrack-ng, airmon-ng, airodump-ng) listas para usar.

### Paso 3 — Conectar el Adaptador ALFA mediante USB Passthrough

Con la VM de Kali ejecutándose y el adaptador ALFA conectado al puerto USB de tu Mac:

1. VMware Fusion mostrará una ventana emergente: **"Un dispositivo USB está solicitando permiso para conectarse a tu máquina virtual."**
2. Haz clic en **Conectar a [Nombre de la VM]** para entregar el adaptador directamente a la VM de Kali.
3. macOS perderá visibilidad del adaptador en este punto — ahora es propiedad exclusiva de la VM.

{{< alert "circle-info" >}}
Si la ventana emergente no aparece (por ejemplo, el adaptador ya estaba conectado antes de iniciar la VM, o cerraste la ventana emergente), ve al menú de VMware Fusion: **Máquina Virtual → USB y Bluetooth → [Nombre del Adaptador ALFA] → Conectar (Desconectar de Mac)**. Esto reasigna manualmente el dispositivo USB a la VM.
{{< /alert >}}

### Paso 4 — Verificar Dentro de Kali

Abre una terminal en la VM de Kali y confirma que el adaptador es visible:

```bash
lsusb | grep -i mediatek
# AWUS036AXML / MT7921AUN: Bus 001 Device 002: ID 0e8d:7961 MediaTek Inc. ...

lsusb | grep -i realtek
# AWUS036ACH / RTL8812AU: Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. ...
```

Si ninguno de los comandos devuelve resultados, el passthrough no se ha completado — verifica nuevamente el menú de dispositivos de VMware.

### Paso 5 — Cargar el Controlador y Verificar el Modo Monitor

Para MT7921AUN (AWUS036AXML), el controlador está integrado en el kernel de Kali. Para adaptadores RTL8812AU, se requiere la instalación del controlador — consulta la [Guía de Instalación del Controlador](/en/blog/install-alfa-driver-kali-ubuntu/). Una vez que el controlador esté activo:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
```

Una salida en vivo de airodump-ng confirma que el passthrough, la carga del controlador y el modo monitor están funcionando correctamente.

---

## Opción B: USB Passthrough con Parallels Desktop

Parallels Desktop es el hipervisor preferido para Macs Apple Silicon cuando el rendimiento es una prioridad. No es gratuito — se requiere una licencia por suscripción — pero su soporte para VMs ARM64 y la implementación de USB passthrough son más maduros que VMware Fusion en hardware Apple Silicon.

### Paso 1 — Parallels Desktop 19+

Instala Parallels Desktop desde [parallels.com](https://www.parallels.com). El mismo flujo de aprobación de extensión del sistema aplica que con VMware Fusion. Permite la extensión del sistema de Parallels en **Seguridad y Privacidad** y reinicia cuando se te solicite.

### Paso 2 — Crear la VM de Kali Linux ARM64

En Apple Silicon, Parallels trabaja exclusivamente con imágenes de SO invitado ARM64. Descarga la imagen de Kali Linux ARM64 desde kali.org y crea una nueva VM en Parallels usando esa imagen.

{{< alert "circle-info" >}}
Parallels Desktop 19+ puede descargar e instalar directamente Kali Linux ARM desde el asistente de nueva VM en Apple Silicon — es posible que no necesites descargar el ISO manualmente.
{{< /alert >}}

En Macs Intel, el ISO estándar de Kali x86_64 funciona con Parallels sin modificaciones.

### Paso 3 — Conectar el Adaptador ALFA via USB

Con la VM de Kali ejecutándose y el adaptador ALFA conectado:

1. En la barra de menú de macOS, ve a **Dispositivos → USB y Bluetooth**.
2. Encuentra tu adaptador ALFA en la lista (puede aparecer como **Realtek 802.11ac NIC**, **MediaTek Wi-Fi** o similar).
3. Haz clic en él y selecciona **Conectar a Linux** (o el nombre de tu VM).

Parallels desconectará el adaptador de macOS y lo pasará exclusivamente a la VM de Kali.

### Paso 4 — Verificar con lsusb

Dentro de la terminal de la VM de Kali:

```bash
lsusb
ip link show
```

El adaptador ALFA debería aparecer tanto en la salida de `lsusb` como en una nueva interfaz `wlan` en `ip link show`. Si la interfaz no es visible, vuelve a conectar el dispositivo a través del menú Dispositivos de Parallels.

{{< alert "circle-info" >}}
Parallels en Apple Silicon supera consistentemente a VMware Fusion para cargas de trabajo de VM con uso intensivo de E/S. Si ejecutas sesiones largas de airodump-ng o realizas capturas de paquetes intensivas, Parallels generalmente producirá menor uso de CPU.
{{< /alert >}}

---

## Kali en Apple Silicon: Notas sobre Controladores ARM64

Ejecutar Kali ARM64 dentro de una VM en Apple Silicon cambia el entorno de compilación de controladores. La mayoría de las guías en línea asumen x86_64, pero los pasos son casi idénticos — la diferencia clave es qué paquetes están preinstalados y cómo DKMS maneja los encabezados del kernel ARM.

**RTL8812AU en ARM64:**
El controlador RTL8812AU de [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) compila correctamente en ARM64. El proceso de compilación con DKMS es el mismo que en x86_64 — clona el repositorio, ejecuta los comandos `dkms`, y el módulo se compilará contra los encabezados del kernel ARM64:

```bash
sudo apt update && sudo apt install -y dkms linux-headers-$(uname -r) build-essential
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

Espera varios minutos para la compilación. El módulo resultante será específico de arquitectura para tu kernel ARM64.

**MT7921AUN en ARM64:**
El controlador `mt7921u` está **integrado en el kernel desde Linux 5.18** y está incluido en Kali ARM64 2024.x y versiones posteriores. No se necesita compilación manual para el AWUS036AXML en Kali ARM64. El adaptador se reconoce automáticamente tras el USB passthrough.

```bash
dmesg | grep mt7921
# [ 4.123456] mt7921u 1-1:1.0: HW/SW Version: 0x8a108a10, Build Time: ...
```

**Recomendación para Macs con chip M:** Si estás adquiriendo un adaptador ALFA específicamente para usar en un Mac Apple Silicon con Kali en una VM, el **AWUS036AXML (MT7921AUN)** es la mejor opción. Su controlador integrado en el kernel elimina por completo el paso de compilación con DKMS y funciona de manera confiable en compilaciones de Kali ARM64. El AWUS036ACH es funcional pero requiere el controlador RTL8812AU fuera del árbol del kernel, añadiendo una dependencia de mantenimiento en la disponibilidad de encabezados del kernel.

---

## Prueba de Modo Monitor e Inyección

Después de completar el USB passthrough con VMware Fusion o Parallels, ejecuta la siguiente secuencia de comandos para verificar que toda la pila está funcionando — desde la visibilidad USB hasta la activación del modo monitor:

```bash
# 1. Confirm USB device is visible
lsusb

# 2. List wireless interfaces
ip link show

# 3. Kill conflicting processes (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# 4. Start monitor mode on the wireless interface
sudo airmon-ng start wlan1

# 5. Confirm monitor interface was created
ip link show wlan1mon

# 6. Begin passive scan
sudo airodump-ng wlan1mon
```

Una salida exitosa de airodump-ng — que muestra SSIDs, BSSIDs, canales y dispositivos cliente — confirma que el USB passthrough, la carga del controlador, el modo monitor y la recepción de paquetes están funcionando de extremo a extremo.

**Si `wlan1` no aparece tras el passthrough:**

1. Desconecta el adaptador ALFA de tu Mac.
2. Espera cinco segundos y vuelve a conectarlo.
3. Reasígnalo a la VM a través del menú de dispositivos USB del hipervisor (Máquina Virtual → USB y Bluetooth en VMware Fusion; Dispositivos → USB y Bluetooth en Parallels).
4. Ejecuta `lsusb` de nuevo dentro de Kali para confirmar que el dispositivo aparece.

{{< alert "triangle-exclamation" >}}
No intentes `airmon-ng start wlan0` en la interfaz predeterminada `wlan0` dentro de la VM — esa interfaz es típicamente el adaptador de red virtual de VMware/Parallels utilizado para la conectividad a internet, no el adaptador ALFA pasado a través. Usar la interfaz incorrecta cortará la conexión de red de tu VM sin habilitar el modo monitor en el adaptador ALFA.
{{< /alert >}}

---

## Rendimiento y Limitaciones

**Latencia del USB passthrough:** Pasar un dispositivo USB a través de una capa de hipervisor añade aproximadamente 1–2 ms de latencia de procesamiento en comparación con usar el adaptador en Linux bare-metal. Para propósitos de pruebas de seguridad 802.11 — captura de paquetes, recopilación de handshakes, pruebas de inyección — esta latencia no es operacionalmente significativa. Solo importaría en aplicaciones en tiempo real sensibles a la latencia, que las pruebas de seguridad no son.

**Propiedad exclusiva:** macOS no puede compartir el adaptador ALFA con la VM de Kali simultáneamente. Una vez que el adaptador se pasa a la VM, desaparece completamente de macOS. Para devolverlo a macOS (por ejemplo, para usarlo como un adaptador Wi-Fi normal), desconéctalo de la VM a través del menú de dispositivos USB del hipervisor, luego desconecta y vuelve a conectar el adaptador. macOS lo reclamará como una interfaz estándar.

**Consumo de energía:** Ejecutar un adaptador Wi-Fi USB (que transmite energía RF de hasta 100 mW) dentro de una VM en un Mac que también tiene su propia radio Wi-Fi activa es un consumo de energía considerable. Las sesiones largas de airodump-ng o las pruebas de inyección de paquetes pueden drenar la batería de un MacBook significativamente más rápido que la operación normal. **Usa el cargador durante sesiones de prueba prolongadas** — especialmente en MacBooks Apple Silicon, donde la gestión de la batería está estrechamente integrada con el sobre térmico.

**Snapshot de VM antes de probar:** VMware Fusion y Parallels admiten snapshots de VM. Tomar un snapshot de una instalación limpia y configurada de Kali antes de una sesión de prueba te permite revertir a un estado conocido y funcional si una actualización del controlador o un cambio de configuración rompe algo.

---

## Solución de Problemas

| Síntoma | Causa Probable | Solución |
|---|---|---|
| El adaptador ALFA no aparece en el menú USB del hipervisor | Extensión del sistema de macOS no aprobada | **Preferencias del Sistema → Seguridad y Privacidad → General** → Permitir extensión de VMware / Parallels, luego reiniciar |
| `lsusb` no muestra el adaptador ALFA dentro de la VM de Kali | USB passthrough no completado | Conectar manualmente via VM → menú USB y Bluetooth; reconectar adaptador |
| Interfaz `wlan1` no aparece después del passthrough | Controlador no cargado (RTL8812AU) | Instalar controlador RTL8812AU via DKMS; ver [Guía de Instalación del Controlador](/en/blog/install-alfa-driver-kali-ubuntu/) |
| `airmon-ng start wlan1` falla con "Operation not permitted" | NetworkManager reteniendo la interfaz | Ejecutar `sudo airmon-ng check kill` primero; luego reintentar |
| El modo monitor inicia pero airodump-ng no muestra redes | Canal o interfaz incorrectos | Confirmar que `wlan1mon` existe con `ip link show`; probar `sudo airodump-ng --band abg wlan1mon` |
| La VM se congela cuando se conecta el adaptador ALFA | Conflicto del controlador USB (VMware) | Apagar la VM, ir a Configuración de VM → USB, cambiar el controlador de USB 3.0 a USB 2.0, reiniciar la VM |

{{< alert "circle-info" >}}
En Apple Silicon específicamente, si el adaptador ALFA es reconocido pero la interfaz no aparece en Kali, verifica `dmesg | tail -30` inmediatamente después de conectarlo. La salida indicará si el kernel está detectando el dispositivo y qué controlador (si alguno) está intentando vincularse a él.
{{< /alert >}}

---

{{< faq >}}

## Guías Relacionadas

Para hosts con Windows y Linux usando VirtualBox o VMware Workstation, consulta la guía complementaria: [USB Passthrough de Adaptadores ALFA: Guía de Configuración con VirtualBox y VMware](/en/blog/alfa-adapter-virtualbox-vmware-usb/).

Para detalles específicos del adaptador AWUS036AXML recomendado en esta guía, incluyendo benchmarks de rendimiento en la banda de 6 GHz y notas sobre versiones del controlador, consulta la reseña completa: [Reseña ALFA AWUS036AXML WiFi 6E](/en/blog/awus036axml-wifi-6e-review/).

## Referencias

1. [Sitio oficial de ALFA Network](https://www.alfa.com.tw/)
2. [Página de descarga oficial de Kali Linux](https://www.kali.org/get-kali/)
3. [Página del producto VMware Fusion](https://www.vmware.com/products/fusion.html)
4. [Sitio oficial de Parallels Desktop](https://www.parallels.com/)
5. [aircrack-ng rtl8812au 驅動專案](https://github.com/aircrack-ng/rtl8812au)
