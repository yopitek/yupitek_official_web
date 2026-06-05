---
title: "Cómo usar adaptadores ALFA WiFi con Kali NetHunter mediante USB OTG en Android"
description: "Guía completa para usar adaptadores ALFA USB WiFi con Kali NetHunter en Android vía USB OTG. Incluye driver AWUS036ACH, comandos de modo monitor, requisitos del cable OTG y dispositivos compatibles."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["nethunter", "android", "usb-otg", "kali-linux", "AWUS036ACH", "RTL8812AU", "mobile-pentest"]
featureimage: "/images/blog/alfa-adapter-nethunter-android-otg.webp"
---

Tu teléfono Android ya es una computadora potente que cabe en tu bolsillo. Con Kali NetHunter instalado en un dispositivo con root y un adaptador ALFA WiFi conectado mediante USB OTG, se convierte en una plataforma de pruebas de penetración de bolsillo genuinamente capaz. Sin laptop, sin hardware voluminoso. Solo tu teléfono, un cable OTG corto y un adaptador que soporte modo monitor e inyección de paquetes.

Esta guía cubre todo lo que necesitas para que un ALFA AWUS036ACH (o adaptador compatible) funcione con NetHunter — desde la selección del hardware hasta la carga del driver, la activación del modo monitor y las herramientas inalámbricas integradas en la app de NetHunter.

---

## ¿Qué es Kali NetHunter?

Kali NetHunter es la plataforma oficial de pruebas de penetración móvil de Kali Linux. En lugar de reemplazar Android, NetHunter instala un entorno chroot de Kali Linux sobre tu instalación Android existente. Tu teléfono continúa funcionando como un dispositivo Android normal mientras ejecuta simultáneamente un userland completo de Kali Linux con todas sus herramientas.

**Características clave:**

- Funciona sin borrar Android — tus apps, contactos y datos permanecen intactos
- Incluye la app NetHunter, un lanzador dedicado para módulos de ataque y control de hardware
- Proporciona una terminal completa con acceso al conjunto de herramientas de Kali (Metasploit, Aircrack-ng, Nmap y cientos más)
- Requiere un dispositivo Android con root para funcionalidad completa

**Tres ediciones:**

| Edición | Requiere Root | Modificaciones al kernel | Caso de uso |
|---|---|---|---|
| NetHunter (Completo) | Sí | Sí (kernel personalizado) | Superficie de ataque completa, soporte de interfaz de hardware |
| NetHunter Lite | Sí | No | Herramientas solo con root, sin kernel personalizado |
| NetHunter Rootless | No | No | Herramientas limitadas, sin ataques de hardware |

Para soporte de adaptador USB OTG con modo monitor, necesitas la **edición NetHunter completa** con un kernel personalizado que incluya el módulo RTL8812AU.

**Dispositivos oficialmente compatibles** incluyen modelos de OnePlus, Google Pixel y algunos Samsung Galaxy seleccionados. Para la lista completa y actualizada, consulta la [página oficial de dispositivos NetHunter](https://www.kali.org/docs/nethunter/).

**El soporte USB OTG es un requisito obligatorio.** Antes de comprar hardware, verifica que tu modelo de dispositivo específico soporte USB OTG.

---

## Requisitos de hardware

Configurar correctamente este setup significa elegir hardware compatible en cada nivel. Un desajuste en cualquier punto de la cadena — dispositivo, cable o adaptador — resultará en que el adaptador nunca aparezca en `lsusb`, desconexiones intermitentes o fallos del driver.

| Elemento | Requisito | Notas |
|---|---|---|
| Dispositivo Android | Con root, compatible con NetHunter, con soporte USB OTG | Verificar soporte OTG antes de comprar; se requiere NetHunter completo con kernel personalizado |
| Cable / adaptador USB OTG | USB-C OTG o Micro-USB OTG según el puerto del dispositivo | La calidad importa — los cables baratos causan desconexiones intermitentes |
| Adaptador ALFA WiFi | Se recomienda AWUS036ACH o AWUS036ACM | AWUS036ACH (RTL8812AU) tiene mejor soporte de módulo de kernel en NetHunter; AWUS036ACM (MT7612U) también compatible |
| Hub USB OTG con alimentación | Muy recomendado | Previene el agotamiento de la batería del teléfono e inestabilidad USB |

{{< alert "triangle-exclamation" >}}
El AWUS036ACH consume aproximadamente **500mW** del puerto USB. Alimentarlo directamente desde la batería del teléfono sin una fuente de alimentación dedicada agotará tu batería significativamente más rápido y puede causar que el adaptador se reinicie o desconecte bajo carga. Un hub OTG con alimentación propia — que toma energía del enchufe de la pared y pasa los datos al teléfono — elimina este problema por completo.
{{< /alert >}}

**Al elegir un hub OTG con alimentación:**

Busca un hub explícitamente comercializado con soporte de paso de alimentación USB OTG. Esto significa que el hub toma 5V de un cargador USB, alimenta los dispositivos conectados desde el cargador (no desde el teléfono) y aún así pasa datos entre el teléfono y los dispositivos conectados. No todos los hubs USB soportan esto — revisa las especificaciones del producto cuidadosamente antes de comprar.

---

## Adaptadores ALFA compatibles con NetHunter

El kernel personalizado de NetHunter incluye módulos de kernel precompilados para un conjunto específico de chipsets. La familia de chipsets RTL8812AU tiene el soporte más sólido porque se integró temprano y se mantiene activamente.

| Adaptador | Chipset | Soporte NetHunter | Notas |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | ✅ Mejor soporte | El kernel NetHunter incluye el módulo `88XXau`; modo monitor e inyección de paquetes totalmente soportados |
| AWUS036ACM | MT7612U | ✅ Buen soporte | Chipset alternativo; generalmente funciona; verificar con el kernel del dispositivo específico |
| AWUS036ACS | RTL8811AU | ✅ Funciona | Misma familia de driver que RTL8812AU; menor consumo de energía (~300mW) |
| AWUS036AXM | MT7921AUN | ⚠️ Limitado | Adaptador WiFi 6E; disponibilidad del módulo de kernel depende del dispositivo y versión de kernel |
| AWUS036AXML | MT7921AUN | ⚠️ Limitado | Mismo chipset que AXM; no soportado universalmente en kernels NetHunter |

**Recomendación:** Para operación confiable con NetHunter, usa adaptadores basados en RTL8812AU. Si necesitas capacidad dual-band AC1200 con amplia compatibilidad NetHunter, el **AWUS036ACH** es la elección correcta.

---

## Pasos de configuración

Los siguientes pasos asumen que tienes un dispositivo Android con root y NetHunter completo instalado, y un cable OTG o hub listo para usar.

### Paso 1: Abrir la app NetHunter

Lanza la app NetHunter en tu dispositivo Android. Navega a **Kali Services** para verificar que el entorno chroot está ejecutándose. Si no está en ejecución, toca **Start** para iniciarlo. El chroot debe estar activo antes de que el kernel pueda exponer dispositivos USB a las herramientas de Kali.

### Paso 2: Conectar el adaptador ALFA mediante OTG

Conecta el cable OTG o hub al puerto USB del teléfono, luego conecta el adaptador ALFA al cable OTG o hub. Si usas un hub con alimentación, conecta primero el adaptador de corriente del hub a la pared.

### Paso 3: Conceder permiso USB

Android mostrará un diálogo de permisos preguntando si se permite que la app NetHunter acceda al dispositivo USB. Toca **Aceptar** y marca **Permitir siempre** si quieres saltarte este aviso en sesiones futuras. Si cierras este diálogo sin conceder permiso, el adaptador no será accesible desde el chroot de Kali.

### Paso 4: Verificar el adaptador con `lsusb`

Abre la terminal NetHunter y ejecuta:

```bash
lsusb
```

Debes ver una entrada que contenga **Realtek Semiconductor** junto con el ID del dispositivo. Para el AWUS036ACH, espera algo como:

```
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

Si el dispositivo Realtek no aparece, el problema está a nivel de hardware — revisa el cable OTG, prueba con un cable diferente, o verifica que OTG esté habilitado en las opciones de desarrollador de tu dispositivo.

### Paso 5: Cargar el driver

```bash
sudo modprobe 88XXau
```

En la mayoría de las compilaciones de NetHunter, el driver se carga automáticamente cuando se detecta el adaptador. Si la interfaz no aparece después de conectar el adaptador, ejecuta este comando manualmente.

### Paso 6: Verificar la interfaz

```bash
ip link show | grep wlan
```

Debes ver `wlan1` (o `wlan2` si la interfaz WiFi integrada de tu dispositivo usa `wlan0`).

### Paso 7: Activar el modo monitor

```bash
sudo airmon-ng start wlan1
```

Si `airmon-ng` informa procesos que podrían interferir con el modo monitor, termínalos primero (ver la sección de comandos a continuación) y luego vuelve a ejecutar este comando. La interfaz se renombrará a `wlan1mon` después de activar el modo monitor.

---

## Comandos de modo monitor en NetHunter

```bash
# Verificar que el adaptador es reconocido por el sistema
lsusb | grep -i realtek

# Cargar driver manualmente si no se cargó automáticamente al conectar el adaptador
sudo modprobe 88XXau

# Terminar procesos que interfieren con el modo monitor (NetworkManager, wpa_supplicant, etc.)
sudo airmon-ng check kill

# Iniciar modo monitor en la interfaz del adaptador ALFA
sudo airmon-ng start wlan1

# Escanear todas las redes visibles (presiona Ctrl+C para detener)
sudo airodump-ng wlan1mon

# Capturar tráfico de una red específica
# -c: canal, --bssid: dirección MAC del AP objetivo, -w: prefijo de archivo de salida
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan1mon
```

---

## Ataques WiFi con NetHunter (solo para pruebas autorizadas)

{{< alert "triangle-exclamation" >}}
Todas las pruebas de seguridad inalámbrica deben realizarse **únicamente en redes y dispositivos que poseas o para los que tengas autorización escrita explícita para probar**. El acceso no autorizado a redes informáticas es ilegal en la mayoría de las jurisdicciones del mundo. Las herramientas descritas aquí son solo para pruebas de penetración autorizadas, investigación de seguridad y fines educativos. Yupitek no acepta ninguna responsabilidad por uso indebido.
{{< /alert >}}

**WiFi Evil Portal (WPS3):** Disponible directamente en el menú principal de la app NetHunter. Crea un punto de acceso falso con un portal cautivo para captura de credenciales durante evaluaciones autorizadas de ingeniería social. Requiere un adaptador externo con soporte de modo AP.

**MANA Rogue AP Toolkit:** Ubicado en **app NetHunter > Wireless Attacks > MANA Toolkit**. MANA extiende el concepto de AP falso estándar con ataques de estilo KARMA y capacidades de SSL stripping. La funcionalidad completa requiere un adaptador WiFi externo compatible — el chip WiFi interno de Android no es suficiente para la mayoría de las configuraciones de MANA.

---

## Gestión de batería y energía

**Consumo de energía:** El AWUS036ACH consume aproximadamente 500mW continuamente durante el uso activo. Con una batería Android típica de 3,500 mAh, esto duplicará aproximadamente tu tasa de descarga en comparación con el uso normal del teléfono.

**Usar un hub OTG con alimentación:** Esta es la solución más efectiva. El hub toma energía del enchufe de la pared y la suministra al adaptador ALFA. El puerto USB del teléfono solo transporta datos.

**Gestión de pantalla:** Configura el tiempo de espera de pantalla a 30 segundos (**Ajustes > Pantalla > Suspensión**) y reduce el brillo al mínimo.

**Consideraciones térmicas:** El uso prolongado del adaptador dentro de una funda puede causar acumulación de calor. Si la protección térmica del teléfono limita el controlador USB, pueden ocurrir desconexiones del adaptador. Retira la funda del teléfono durante sesiones de captura prolongadas.

---

## Solución de problemas

**Adaptador no reconocido (`lsusb` no muestra nada):**
1. Verificar que USB OTG está habilitado — revisar **Ajustes > Opciones de desarrollador > OTG**
2. Probar con un cable OTG diferente — la calidad del cable es una causa común de fallo
3. Confirmar que tu dispositivo soporta USB OTG

**Driver no carga (sin interfaz `wlan1` después de `modprobe`):**
1. Revisar mensajes de error en `dmesg` en la terminal NetHunter: `dmesg | tail -30`
2. Verificar que el chroot de NetHunter está en ejecución
3. Confirmar que tu compilación de NetHunter incluye el módulo `88XXau`: `find /lib/modules -name "*88XX*"`

**La interfaz `wlan1` desaparece durante el uso:**
Casi siempre es un problema de energía USB. Usa un hub OTG con alimentación.

**Errores de permiso denegado:**
Asegúrate de ejecutar comandos como root en el chroot de NetHunter. Ejecuta `sudo su` primero, luego los comandos.

**El modo monitor inicia pero no aparecen redes en `airodump-ng`:**
1. Probar `sudo airodump-ng --band abg wlan1mon` para escanear todas las bandas
2. Verificar que se ejecutó `airmon-ng check kill` antes de iniciar el modo monitor

---

## Guías relacionadas

- [Guía de configuración del AWUS036ACH en Kali Linux (escritorio/laptop)](/es/blog/awus036ach-kali-linux-setup/)
- [Usar adaptadores ALFA con Raspberry Pi y Kali](/es/blog/alfa-adapter-raspberry-pi-kali/)
