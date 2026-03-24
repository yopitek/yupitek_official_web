---
title: "Solución de Firmware AWUS036AXML en Modo Monitor: Resolver Crashes en Modo Activo"
description: "Cómo solucionar los crashes de firmware del AWUS036AXML en modo monitor en Kali Linux. Cubre la actualización de firmware MT7921AUN, requisitos de versión del kernel, alternativas de modo activo vs pasivo, y hcxdumptool."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036AXML", "MT7921AUN", "monitor-mode", "firmware", "kali-linux", "troubleshooting", "wifi-6e"]
---

El **ALFA AWUS036AXML** es el adaptador WiFi 6E insignia de ALFA Network, construido sobre el chipset MediaTek MT7921AUN con soporte tribanda (2.4 / 5 / 6 GHz). Es uno de los pocos adaptadores USB capaces de monitoreo pasivo en la banda de 6 GHz en 2026 y rinde de forma excepcional en casos de uso como reconocimiento de sitios, captura de paquetes y recolección de PMKID.

Sin embargo, hay un problema conocido que sorprende a los usuarios: **los comandos de modo monitor activo provocan un crash del firmware**. Ejecutar herramientas como `aireplay-ng` o `mdk4` hace que la interfaz `wlan0mon` desaparezca por completo, obligándote a desconectar y volver a conectar el adaptador para recuperarlo. No es un defecto de hardware — es una limitación del driver `mt7921u` de Linux y su firmware actual.

Esta guía explica la causa raíz, proporciona pasos de diagnóstico completos y ofrece soluciones concretas y alternativas para seguir trabajando sin interrupciones.

---

## El Problema: Crashes en Modo Monitor Activo

### Síntoma

Tras activar el modo monitor y ejecutar un comando activo como `aireplay-ng --test wlan0mon` o cualquier operación de deautenticación/inyección, la interfaz `wlan0mon` desaparece de la salida de `ip link` e `iwconfig`. El adaptador queda sin respuesta y no puede recuperarse sin desconectarlo físicamente y volverlo a conectar. En algunos casos, `dmesg` muestra un error de firmware o evento de reset inmediatamente después del crash.

Las operaciones pasivas (escaneo con `airodump-ng`, captura de frames en bruto) funcionan correctamente antes y después del crash, siempre que no se active ninguna inyección activa.

### Causa Raíz

El **chipset MT7921AUN** utiliza una arquitectura MAC basada en firmware. El driver `mt7921u` del kernel de Linux depende del firmware embebido del chipset para manejar ciertas operaciones de nivel inferior, incluyendo la inyección de frames en modo monitor. La combinación actual de firmware y driver no implementa completamente la ruta de comandos necesaria para la inyección activa en modo monitor en Linux.

En contraste, el **monitoreo pasivo** (capturar frames que ya están en el aire) no requiere que el firmware transmita nada y funciona sin provocar el crash. El problema está limitado a operaciones de la ruta de transmisión: frames de deautenticación, solicitudes de sondeo, floods de asociación y operaciones activas similares.

{{< alert "triangle-exclamation" >}}
**Bug de crash de firmware conocido.** Este es un problema confirmado en el driver `mt7921u` de Linux a principios de 2026. Afecta al AWUS036AXML y otros adaptadores USB basados en MT7921AUN. Podría resolverse en futuras actualizaciones del kernel o firmware — consulta la [guía de instalación del driver](/es/blog/install-alfa-driver-kali-ubuntu/) para conocer el estado más reciente.
{{< /alert >}}

---

## Diagnóstico: ¿Es Este Tu Problema?

```bash
# Verificar que el adaptador está reconocido
lsusb | grep -i mediatek

# Verificar que el driver está cargado
lsmod | grep mt7921u

# Verificar la versión del kernel (debe ser >= 5.18)
uname -r

# Iniciar el modo monitor
sudo airmon-ng start wlan0

# Probar captura pasiva (debería funcionar)
sudo airodump-ng wlan0mon

# Probar inyección activa (puede causar crash)
sudo aireplay-ng --test wlan0mon
```

Si el adaptador desaparece de `ip link` tras `aireplay-ng --test`, has confirmado el bug de crash de firmware.

Verificación adicional mediante logs del kernel:

```bash
sudo dmesg | grep -E "mt7921|firmware|reset" | tail -20
```

Busca mensajes como `mt7921u: firmware crash`, `mt7921u: chip reset` o `usb disconnect` apareciendo inmediatamente después de la llamada a aireplay-ng.

{{< alert "circle-info" >}}
**La captura pasiva no está afectada.** Si `airodump-ng` funciona pero `aireplay-ng` causa crash, esto es exactamente el bug conocido de MT7921AUN. Procede con las soluciones siguientes.
{{< /alert >}}

---

## Solución 1: Actualizar el Paquete de Firmware

El primer paso más impactante es asegurarte de tener los archivos de firmware MT7921 más recientes. Las versiones antiguas de firmware son más propensas al crash; el firmware actualizado mejora la estabilidad para algunas operaciones activas.

```bash
sudo apt update
sudo apt install firmware-misc-nonfree

# O instalar manualmente el último firmware mt7921 desde el repositorio linux-firmware
sudo apt install git
git clone https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
sudo cp linux-firmware/mediatek/mt7921* /lib/firmware/mediatek/
sudo modprobe -r mt7921u
sudo modprobe mt7921u
```

Tras actualizar los archivos de firmware, recarga el driver y vuelve a probar el modo activo:

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

---

## Solución 2: Usar el Kernel Más Reciente

El driver `mt7921u` se mantiene activamente en el kernel Linux principal. Desde 5.18, parches de estabilidad, manejo de comandos de firmware y mejoras en modo monitor se han incluido en actualizaciones del kernel. Ejecutar un kernel más nuevo es una de las formas más fiables de mejorar el comportamiento.

Verifica la versión actual del kernel:

```bash
uname -r
```

Actualiza al último kernel disponible en Kali Linux:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

Objetivo: **kernel 6.1 LTS o más nuevo** para los parches más completos del driver `mt7921u`. El kernel 6.6 y posteriores incluyen mejoras adicionales al stack del driver USB de MediaTek con resultados positivos reportados por la comunidad.

{{< alert "circle-info" >}}
**Mejora en kernel 6.6+.** Varios informes de la comunidad indican que el kernel 6.6 con firmware actualizado reduce (pero no siempre elimina) los crashes en modo activo en MT7921AUN. Después de actualizar, vuelve a ejecutar la secuencia de diagnóstico para evaluar tu combinación específica.
{{< /alert >}}

---

## Alternativa: Usar hcxdumptool (Captura Pasiva de PMKID)

Si las correcciones de firmware no resuelven completamente el crash para tu trabajo, `hcxdumptool` ofrece un flujo de trabajo alternativo altamente efectivo que no requiere ninguna inyección de frames.

`hcxdumptool` opera en **modo pasivo** — captura valores PMKID directamente de los frames de beacon y sondeo transmitidos por los puntos de acceso. No se envían frames de deautenticación, no hay inyección, no hay crash de firmware. El AWUS036AXML maneja perfectamente este flujo de trabajo.

```bash
sudo apt install hcxdumptool hcxtools

# Captura pasiva — sin deauth, sin crash de firmware
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1

# Convertir al formato hashcat
hcxpcapngtool -o hash.hc22000 capture.pcapng

# Crackear con hashcat
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

Este flujo de trabajo captura PMKIDs de frames de beacon sin transmitir nada — completamente pasivo desde la perspectiva del medio inalámbrico.

{{< alert "circle-info" >}}
**La captura de PMKID funciona en todas las redes WPA2/WPA3 modernas.** Los puntos de acceso transmiten PMKIDs en sus frames de beacon independientemente de si hay algún cliente asociado. Solo necesitas estar dentro del rango del AP — no se necesita ningún cliente. Ideal para escenarios donde la deautenticación no es una opción.
{{< /alert >}}

---

## Alternativa: Usar AWUS036ACH para Inyección Activa

Para tareas que genuinamente requieren inyección activa de frames (captura forzada de handshake WPA, enumeración WPS, y operaciones similares), el **AWUS036ACH** (chipset RTL8812AU) es la solución establecida con soporte de driver maduro y bien probado en Kali Linux.

Configuración profesional recomendada con doble adaptador:

- **AWUS036AXML** → escaneo pasivo y captura en 5 GHz / 6 GHz
- **AWUS036ACH** → inyección activa en 2.4 GHz / 5 GHz

Esta combinación te da cobertura completa en todas las bandas, con la inyección manejada por el RTL8812AU (cuyo soporte en modo activo en Linux lleva años siendo estable), mientras el AWUS036AXML se encarga del descubrimiento en 6 GHz y la captura pasiva de alta calidad.

Consulta la [reseña del AWUS036AXML](/es/blog/awus036axml-wifi-6e-review/) y la [guía de inyección de paquetes](/es/blog/packet-injection-guide/) para detalles de configuración de ambos adaptadores.

---

## Cuándo Funciona el Modo Activo

Vale la pena señalar que el modo activo no siempre falla. Varias condiciones reportadas por miembros de la comunidad producen comportamiento estable o casi estable en MT7921AUN:

- **Kernel 6.6 o más nuevo** con firmware-misc-nonfree 20240610 o más nuevo
- Evitar `aireplay-ng --deauth` en modo ráfaga (los floods de deauth con alta tasa de paquetes son más propensos a provocar crashes que las operaciones de un solo frame)
- Usar `--deauth 1` o `--deauth 3` en lugar de streams de deauth continuos
- Asegurarse de que el adaptador esté conectado a un puerto USB 3.0 (las restricciones de ancho de banda de USB 2.0 añaden estrés al pipeline de comandos del firmware)
- Operar en 2.4 GHz en lugar de 5 GHz para inyección (la banda de menor frecuencia parece más estable en algunas versiones del driver)

{{< alert "triangle-exclamation" >}}
**Prueba antes de compromisos de producción.** Incluso cuando el modo activo parece funcionar, el firmware del MT7921AUN puede crashear a mitad de operación bajo carga. Siempre ten un plan de recuperación (adaptador de respaldo o flujo de trabajo solo-pasivo) cuando uses el AWUS036AXML para operaciones activas.
{{< /alert >}}

---

## Verificar Si Tu Firmware Está Actualizado

```bash
# Comprobar la fecha del archivo de firmware actual
ls -la /lib/firmware/mediatek/mt7921*

# Comprobar la versión del driver
modinfo mt7921u | grep -E "version|filename"

# Comprobar los mensajes del kernel para la carga del firmware
sudo dmesg | grep mt7921
```

Con una carga exitosa del firmware, la salida de `dmesg` debería mostrar algo como:

```
mt7921u 1-2.3:1.0: firmware init done
mt7921u 1-2.3:1.0: HW/SW Version: ...
```

---

## Resumen: Mejores Casos de Uso del AWUS036AXML

- ✅ **Escaneo pasivo WiFi 6E y captura PCAP** — funciona perfectamente
- ✅ **Captura PMKID con hcxdumptool** — sin inyección, sin crash de firmware
- ✅ **Descubrimiento de redes en 6 GHz** — escaneo pasivo con airodump-ng en la banda de 6 GHz
- ✅ **Levantamiento de sitio WiFi 6E y análisis de interferencias** — monitoreo pasivo tribanda
- ✅ **Captura básica de handshake WPA2** — captura pasiva del tráfico existente
- ⚠️ **Inyección activa de frames** — usa AWUS036ACH hasta que el firmware de MT7921AUN madure
- ⚠️ **Floods de deautenticación** — riesgo de crash; prueba cuidadosamente en kernel 6.6+
- ⭐ **Mejor flujo de trabajo: llevar tanto AWUS036AXML + AWUS036ACH** para cobertura completa de todas las bandas y operaciones

---

## Guías Relacionadas

- [Reseña Completa del AWUS036AXML](/es/blog/awus036axml-wifi-6e-review/)
- [Guía de Inyección de Paquetes](/es/blog/packet-injection-guide/)
- [Guía de Instalación de Drivers](/es/blog/install-alfa-driver-kali-ubuntu/)
