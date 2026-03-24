---
title: "Guía de Compra de Adaptadores WiFi ALFA 2026: ¿Qué Modelo Es el Indicado para Ti?"
description: "Guía completa de adaptadores USB WiFi ALFA Network para 2026. Compara AWUS036ACH, ACM, ACS, AX, AXER, AXM, AXML, EACS según soporte de controladores, monitor mode, compatibilidad con sistemas operativos y precio."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-network", "wifi-adapter", "buyer-guide", "kali-linux", "penetration-testing", "monitor-mode"]
---

Esta guía va directo al punto para ingenieros de seguridad de redes, profesionales de TI empresarial y red teamers que necesitan elegir el adaptador USB WiFi ALFA Network correcto en 2026. Cubrimos los ocho modelos actuales en producción — [AWUS036ACS](/en/products/alfa/awus036acs/), [AWUS036ACH](/en/products/alfa/awus036ach/), [AWUS036ACM](/en/products/alfa/awus036acm/), [AWUS036EACS](/en/products/alfa/awus036eacs/), [AWUS036AX](/en/products/alfa/awus036ax/), [AWUS036AXER](/en/products/alfa/awus036axer/), [AWUS036AXM](/en/products/alfa/awus036axm/) y [AWUS036AXML](/en/products/alfa/awus036axml/) — comparando chipsets, madurez de controladores, soporte de sistemas operativos y casos de uso reales, para que pases menos tiempo resolviendo problemas de controladores y más tiempo en el trabajo que importa.

---

## Cómo Elegir: 4 Preguntas Clave

Antes de abrir cualquier página de producto, responde estas cuatro preguntas. Tus respuestas eliminarán la mayoría de las opciones de inmediato.

### (a) ¿Qué sistema operativo usas?

El soporte de controladores lo es todo. Los usuarios de Kali Linux y Ubuntu en kernels recientes tienen la mayor variedad de opciones. El soporte para macOS es escaso en todos los modelos. Windows 10/11 generalmente tiene buen soporte. Si usas Raspberry Pi o una plataforma basada en ARM, la selección del chipset es fundamental.

- **Kali Linux / Debian:** RTL8812AU (`dkms-rtl8812au`) y MT7921AUN (kernel nativo ≥ 5.18) son las dos familias de chipsets principales.
- **Ubuntu 22.04 / 24.04:** El mismo panorama de controladores, aunque es posible que necesites instalar kernels HWE o `firmware-misc-nonfree` para MT7921AUN.
- **Windows 10/11:** ALFA proporciona controladores firmados para todos los modelos actuales. La instalación es sencilla.
- **macOS Sonoma:** Solo un puñado de adaptadores cuenta con soporte de kext mantenido por la comunidad. Prepárate para complicaciones; planifica un flujo de trabajo con máquina virtual.
- **Raspberry Pi (Kali NetHunter, ARM):** Los modelos con RTL8812AU son la opción segura. MT7921AUN puede funcionar, pero requiere el paquete `firmware-misc-nonfree` y un kernel lo suficientemente reciente.

### (b) ¿Necesitas monitor mode e inyección de paquetes?

Si tu respuesta es sí — y para cualquier prueba de penetración o auditoría inalámbrica debería serlo — elimina el [AWUS036EACS](/en/products/alfa/awus036eacs/) de tu lista de inmediato. Su chipset RTL8821CU no admite monitor mode ni inyección de manera confiable en Linux. Todos los demás modelos de esta guía sí lo hacen.

### (c) ¿Máquina virtual o hardware nativo?

El passthrough de USB en VirtualBox y VMware agrega una capa de complejidad. Cualquier adaptador de esta lista funcionará con el passthrough correctamente configurado, pero los adaptadores RTL8812AU (ACH) y MT7612U (ACM) tienen el historial más sólido en entornos de máquina virtual. Si solo vas a usar passthrough hacia una VM, evita adaptadores que dependan de archivos de firmware cargados en tiempo de ejecución — las desconexiones de USB implican perder el firmware.

Consulta [Configuración de adaptador ALFA en VirtualBox y VMware](/en/blog/alfa-adapter-virtualbox-vmware-usb/) para instrucciones completas.

### (d) ¿Presupuesto?

La generación Wi-Fi 5 (ACH, ACM, ACS) es más económica, tiene controladores más estables y es la elección correcta si el presupuesto es una restricción o si la estabilidad del controlador es lo primordial. La generación Wi-Fi 6/6E (AX, AXER, AXM, AXML) es hacia donde se dirige el hardware, pero pagas más y aceptas algunos casos límite de controladores en kernels no principales.

---

## Tabla Comparativa Completa de Adaptadores ALFA

<div style="overflow-x: auto;">

| Modelo | Generación Wi-Fi | Chipset | Velocidad Máx. | Monitor Mode | Controlador Kali | Windows | macOS | Antenas | Ideal Para |
|---|---|---|---|---|---|---|---|---|---|
| [AWUS036ACS](/en/products/alfa/awus036acs/) | Wi-Fi 5 | RTL8811AU | AC600 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 1× RP-SMA | Kit de viaje liviano |
| [AWUS036ACH](/en/products/alfa/awus036ach/) | Wi-Fi 5 | RTL8812AU | AC1200 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 2× RP-SMA | Operaciones de red team |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | Wi-Fi 5 | MT7612U | AC1200 | ✅ | mt76x2u (≥4.19) | ✅ | ⚠️ | 2× RP-SMA | Doble banda económico |
| [AWUS036EACS](/en/products/alfa/awus036eacs/) | Wi-Fi 5 | RTL8821CU | AC1200 | ⚠️ | rtl88xxcu | ✅ | ✅ | 1× RP-SMA | Uso general (sin inyección) |
| [AWUS036AX](/en/products/alfa/awus036ax/) | Wi-Fi 6 | RTL8832BU | AX1800 | ✅ | OOK (<6.14) | ✅ | ❌ | Integrated | Auditoría Wi-Fi 6 |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | Wi-Fi 6 | RTL8832BU | AX1800 | ✅ | OOK (<6.14) | ✅ | ❌ | Integrated nano | Wi-Fi 6 de largo alcance |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | Wi-Fi 6E | MT7921AUN | AX1800 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 2× RP-SMA | Entrada Wi-Fi 6E |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | Wi-Fi 6E | MT7921AUN | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 1× RP-SMA | Flagship 6E |

</div>

**Leyenda:** ✅ Compatible · ⚠️ Limitado/parcial · ❌ No compatible

{{< alert "circle-info" >}}
**Nota sobre macOS:** Todos los adaptadores ALFA enfrentan desafíos con los controladores en macOS Ventura y Sonoma. La opción más común mantenida por la comunidad es ejecutar Kali Linux en una VM con passthrough de USB. AWUS036EACS es la excepción — puede funcionar mediante el controlador nativo de Realtek para macOS, pero sin monitor mode.
{{< /alert >}}

---

## Adaptadores Wi-Fi 5 (Mayor Madurez de Controladores)

La generación Wi-Fi 5 cuenta con años de desarrollo comunitario. Si tu prioridad es la estabilidad absoluta del controlador — especialmente para CTF, auditorías profesionales o entornos donde no puedes permitirte un controlador roto tras una actualización de kernel — empieza aquí.

### AWUS036ACH — El Estándar para Red Teams

El [AWUS036ACH](/en/products/alfa/awus036ach/) sigue siendo el adaptador ALFA más ampliamente utilizado en la comunidad de seguridad, y con razón. Su chipset RTL8812AU es compatible con el controlador `aircrack-ng/rtl8812au`, que ha sido mantenido y probado contra cada versión mayor de Kali Linux durante años.

**Especificaciones de hardware:**
- Chipset: RTL8812AU (Realtek)
- Dos conectores RP-SMA de antena desmontables — compatibles con toda la línea de antenas ALFA
- Potencia de transmisión de 500 mW — la más alta en la línea Wi-Fi 5
- Doble banda: 2.4 GHz y 5 GHz

**Por qué lidera para red teams:** 500 mW de potencia de transmisión combinados con antenas externas duales y soporte de inyección maduro significan que puedes trabajar a distancia manteniendo una entrega confiable de tramas. Reemplaza las antenas omnidireccionales estándar por un panel direccional [APA-M25](/en/products/alfa/apa-m25/) y tendrás una plataforma de largo alcance seria. El factor de forma de dos antenas también habilita un MIMO 2T2R adecuado al asociarse con redes objetivo.

**Instalación del controlador en Kali:**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
```

{{< alert "triangle-exclamation" >}}
En kernels ≥ 6.2, el módulo `rtl8812au` incluido en imágenes antiguas de Kali puede fallar al cargar. Instala siempre `dkms-rtl8812au` desde el repositorio de Kali — rastrea los cambios del kernel y se reconstruye automáticamente en cada actualización mediante DKMS.
{{< /alert >}}

### AWUS036ACM — La Opción Económica de Doble Banda

El [AWUS036ACM](/en/products/alfa/awus036acm/) usa el chipset MT7612U (MediaTek) — una familia diferente al RTL8812AU del ACH — y viene con dos conectores RP-SMA para operación 2T2R a un precio más bajo. El controlador mt76x2u está integrado en el kernel desde la versión 4.19, sin necesidad de compilar nada. El soporte de monitor mode e inyección de paquetes es completo.

Si solo necesitas un puerto de antena y no requieres la potencia de transmisión extendida del ACH, el ACM cubre los mismos casos de uso por menos dinero. Es una elección común para despliegues en kits donde se compran adaptadores en cantidad para un equipo de auditoría.

**Cuándo elegir ACM sobre ACH:** Restricciones de presupuesto, uso por un solo operador, situaciones donde la diversidad de antenas no es prioritaria.

### AWUS036ACS — Liviano y Portátil

El [AWUS036ACS](/en/products/alfa/awus036acs/) usa el chipset RTL8811AU — un escalón por debajo del RTL8812AU en potencia de transmisión, pero completamente capaz de monitor mode e inyección de paquetes. Su factor de forma compacto y su antena única lo convierten en la opción de viaje para consultores con mucha movilidad que no quieren lidiar con múltiples antenas RP-SMA en la seguridad del aeropuerto.

El controlador RTL8811AU comparte el mismo paquete `rtl8812au-dkms` en Kali, por lo que el proceso de instalación es idéntico.

**Ventajas y desventajas vs. ACH/ACM:** Menor potencia de transmisión (menos alcance a distancia), antena única (sin MIMO), AC600 vs. AC1200 de rendimiento máximo. Para la mayoría de flujos de trabajo de captura e inyección, estas diferencias son irrelevantes. Para operaciones de largo alcance, sí importan.

### AWUS036EACS — Uso General, No para Pentesting

El [AWUS036EACS](/en/products/alfa/awus036eacs/) está impulsado por un chipset Realtek RTL8821CU y usa el controlador de kernel `rtl88xxcu`. Este chipset fue diseñado para conectividad de cliente, no para manipulación de paquetes. El soporte de monitor mode bajo `rtl88xxcu` no es confiable, y la inyección de paquetes no está disponible en la configuración estándar del controlador.

{{< alert "triangle-exclamation" >}}
**No uses AWUS036EACS para pruebas de penetración, operaciones de red team ni ninguna tarea que requiera monitor mode o inyección de paquetes.** Es adecuado para conectividad inalámbrica general, extensión del rango del controlador de drones DJI (donde se usa frecuentemente), y despliegues con prioridad en Windows donde el comportamiento estándar de adaptador cliente es aceptable.
{{< /alert >}}

Merece su lugar en esta lista por su compatibilidad con macOS — la situación del controlador RTL8821CU en macOS es mejor que la de otros chipsets de la gama — y para despliegues de conectividad empresarial o para consumidores donde el adaptador se usa puramente como cliente.

---

## Adaptadores Wi-Fi 6 (El Punto Óptimo Actual)

Wi-Fi 6 (802.11ax) trajo mejoras significativas en el rendimiento en entornos densos, escenarios MU-MIMO con muchos objetivos y BSS Coloring para la identificación de redes. Para los auditores inalámbricos, los adaptadores Wi-Fi 6 son cada vez más relevantes a medida que los despliegues empresariales han migrado agresivamente a infraestructura 802.11ax.

Ambos adaptadores ALFA Wi-Fi 6 (AX, AXER) usan el chipset Realtek RTL8832BU. En Linux, el controlador RTL8832BU está fuera del kernel (OOK) en versiones inferiores a 6.14 — el monitor mode y la inyección de paquetes son limitados. Estos adaptadores están diseñados principalmente para conectividad en Windows.

### AWUS036AX — La Opción Limpia de Wi-Fi 6

El [AWUS036AX](/en/products/alfa/awus036ax/) es el adaptador Wi-Fi 6 AX1800 de ALFA: antena integrada (sin conector RP-SMA), chipset RTL8832BU y operación en bandas de 2.4 y 5 GHz. Soporte completo en Windows; en Linux el controlador es OOK en kernels < 6.14.

**Estado del controlador:**
- Kernel ≥ 6.14: controlador RTL8832BU integrado en el kernel, sin paquetes adicionales necesarios
- Kernel < 6.14: OOK (Out-of-Kernel) — se requiere compilar e instalar el controlador RTL8832BU manualmente
- Monitor mode: ⚠️ Limitado
- Inyección de paquetes: ⚠️ Limitada

**Nota práctica sobre monitor mode:** El RTL8832BU tiene soporte de monitor mode limitado en Linux. El controlador está fuera del kernel (OOK) en versiones inferiores a 6.14 — el monitor mode y la inyección de paquetes no funcionan con fiabilidad. Para auditorías Wi-Fi 6 en Linux, verifica las capacidades en tu kernel específico antes de un compromiso real.

{{< alert "circle-info" >}}
**Verificación del kernel:** Ejecuta `uname -r` para confirmar tu versión de kernel antes de comprar. En Kali 2024.x con kernel ≥ 6.14, el controlador RTL8832BU estará integrado. En kernels < 6.14, se requiere compilar el controlador OOK de RTL8832BU.
{{< /alert >}}

### AWUS036AXER — Variante de Alcance Extendido

El [AWUS036AXER](/en/products/alfa/awus036axer/) es idéntico en hardware al AWUS036AX en chipset y configuración de antenas (nano integrada), pero añade amplificación de RF mejorada para un mayor alcance operativo. La situación del controlador es idéntica — mismo RTL8832BU, misma ruta de soporte del kernel, mismo comportamiento de monitor mode e inyección limitados.

Elige AXER sobre AX cuando el alcance sea el factor decisivo: relevamientos de sitio en campus grandes, evaluaciones en exteriores o escenarios donde el punto de acceso está a distancia. El sobrecosto es moderado y justificado si el alcance importa para tu despliegue.

---

## Adaptadores Wi-Fi 6E (A Prueba de Futuro)

Wi-Fi 6E extiende 802.11ax a la banda de 6 GHz, proporcionando acceso al nuevo espectro de 5.925–7.125 GHz. En la práctica, esto significa menos interferencia, anchos de canal más amplios (hasta 160 MHz) y acceso a una banda que los equipos más antiguos no pueden ver ni alcanzar. A medida que las redes empresariales despliegan infraestructura Wi-Fi 6E, los auditores necesitan adaptadores con capacidad 6E para evaluar la superficie de ataque completa.

Ambos adaptadores ALFA Wi-Fi 6E requieren kernel ≥ 5.18 para soporte de la banda de 6 GHz. La banda de 6 GHz requiere que el dominio regulatorio esté configurado correctamente — la aplicación regulatoria para 6 GHz es más estricta que para 2.4/5 GHz en la mayoría de las jurisdicciones.

### AWUS036AXM — Punto de Entrada a Wi-Fi 6E

El [AWUS036AXM](/en/products/alfa/awus036axm/) usa el chipset MT7921AUN con soporte para la banda de 6 GHz habilitado. Viene con dos conectores RP-SMA para operación 2T2R.

Para operadores que principalmente trabajan en entornos de 2.4 y 5 GHz pero quieren capacidad 6 GHz para evaluaciones de redes emergentes sin pagar precios flagship, el AXM es el punto de entrada lógico.

**Cobertura de bandas:** 2.4 GHz, 5 GHz, 6 GHz (tri-banda)
**Antenas:** 2× RP-SMA — intercambiables con cualquier antena ALFA compatible

### AWUS036AXML — El Adaptador Flagship 6E

El [AWUS036AXML](/en/products/alfa/awus036axml/) es el adaptador de gama más alta de ALFA en la actualidad. Cuenta con el chipset MT7921AUN (MediaTek), interfaz USB-C 3.2, Bluetooth 5.2 y un conector RP-SMA de alta ganancia para la conexión de antenas externas.

**Especificaciones clave:**
- Chipset: MT7921AUN (MediaTek)
- 1× conector RP-SMA de alta ganancia
- USB-C 3.2, Bluetooth 5.2
- Tri-banda: 2.4 GHz + 5 GHz + 6 GHz
- Clase AX3000 (hasta 3000 Mbps teóricos entre bandas)
- Mayor potencia de salida en la línea ALFA 6E

**Notas del controlador para AXML:**
- MT7921AUN es compatible bajo la misma familia de controladores `mt7921u` en kernel ≥ 5.18
- Monitor mode es compatible; el monitor activo con firmware ha mostrado problemas de reinicio de firmware en algunos kernels — consulta la [reseña detallada del AWUS036AXML](/en/blog/awus036axml-wifi-6e-review/) para datos completos de pruebas
- La banda de 6 GHz en monitor mode requiere que tu dominio regulatorio permita el escaneo pasivo en canales de 6 GHz

{{< alert "triangle-exclamation" >}}
**Nota de firmware del AWUS036AXML:** En kernels inferiores a 6.1, algunos usuarios experimentan bloqueos de firmware al cambiar el AXML repetidamente entre monitor mode y modo administrado. Si tu flujo de trabajo requiere cambios frecuentes de modo, ejecuta kernel ≥ 6.1 e instala el paquete `firmware-misc-nonfree` más reciente.
{{< /alert >}}

---

## Análisis Detallado de Compatibilidad de Controladores

<div style="overflow-x: auto;">

| Modelo | Chipset | Paquete Kali | Ubuntu HWE | RPi ARM | Windows 10/11 |
|---|---|---|---|---|---|
| [AWUS036ACS](/en/products/alfa/awus036acs/) | RTL8811AU | `dkms-rtl8812au` | Compilación manual | ✅ rtl8812au-dkms | ✅ Controlador ALFA |
| [AWUS036ACH](/en/products/alfa/awus036ach/) | RTL8812AU | `dkms-rtl8812au` | Compilación manual | ✅ rtl8812au-dkms | ✅ Controlador ALFA |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | MT7612U | `mt76x2u (in-kernel)` | Integrado en kernel | ✅ mt76x2u (≥4.19) | ✅ Controlador ALFA |
| [AWUS036EACS](/en/products/alfa/awus036eacs/) | RTL8821CU | `rtl88xxcu` | Integrado en kernel | ⚠️ Limitado | ✅ Integrado |
| [AWUS036AX](/en/products/alfa/awus036ax/) | RTL8832BU | `firmware-misc-nonfree` | Kernel ≥ 5.18 | ⚠️ req. firmware | ✅ Controlador ALFA |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | RTL8832BU | `firmware-misc-nonfree` | Kernel ≥ 5.18 | ⚠️ req. firmware | ✅ Controlador ALFA |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | MT7921AUN | `firmware-misc-nonfree` | Kernel ≥ 5.18 | ⚠️ req. firmware | ✅ Controlador ALFA |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | MT7921AUN | `firmware-misc-nonfree` | Kernel ≥ 5.18 | ⚠️ req. firmware | ✅ Controlador ALFA |

</div>

**Historial del kernel RTL8812AU:** El controlador RTL8812AU fue parcialmente integrado al kernel principal en Linux 5.2, pero con limitaciones importantes — sin monitor mode, sin inyección. La capacidad completa para pruebas de penetración requiere el controlador `rtl8812au` fuera del árbol principal, empaquetado como `dkms-rtl8812au` en Kali. El paquete DKMS se reconstruye automáticamente cuando se actualiza el kernel, lo que lo hace prácticamente libre de mantenimiento en sistemas Kali Linux.

**Historial del kernel MT7921AUN:** La integración nativa llegó en Linux 5.18 mediante el controlador USB `mt7921u`. El archivo de firmware `WIFI_MT7961_patch_mcu_1_2_hdr.bin` (y blobs de firmware relacionados) deben estar presentes en `/lib/firmware/mediatek/`. En Kali, son instalados por `firmware-misc-nonfree`. En Ubuntu 22.04 LTS con el kernel predeterminado, es posible que necesites instalar la pila HWE (`linux-generic-hwe-22.04`) para alcanzar ≥ 5.18.

**Especificaciones para Raspberry Pi:** El controlador RTL8812AU compila limpiamente en Raspberry Pi OS (32 bits y 64 bits) usando `dkms-rtl8812au`. Es la opción más segura para despliegues de NetHunter. Los adaptadores MT7921AUN pueden funcionar en Pi 4/5 pero requieren `firmware-misc-nonfree` y un kernel de Raspberry Pi OS lo suficientemente reciente (las imágenes de 2023 en adelante deberían funcionar bien).

---

## Mejor Adaptador ALFA Según Caso de Uso

### Operaciones de Red Team

**Recomendado: [AWUS036ACH](/en/products/alfa/awus036ach/)**

La potencia de transmisión de 500 mW del ACH, sus antenas duales y el probado controlador RTL8812AU lo convierten en la opción predeterminada para compromisos de red team. Puedes confiar en que funcionará después de una actualización del kernel, que pasará por una VM de forma confiable y que aceptará cualquier antena RP-SMA que traigas. Si el presupuesto lo permite y la cobertura 6E está en el alcance, agrega un [AWUS036AXML](/en/products/alfa/awus036axml/) como adaptador secundario para el descubrimiento de redes en 6 GHz.

### Competencias CTF

**Recomendado: [AWUS036ACM](/en/products/alfa/awus036acm/)**

Los desafíos inalámbricos en CTF suelen involucrar entornos controlados donde la potencia de transmisión no es la variable crítica. El ACM proporciona capacidad completa de monitor mode e inyección de paquetes a un precio más bajo. Su factor de forma compacto de antena única es fácil de empacar y desplegar. Si el CTF incluye desafíos Wi-Fi 6 (aún poco comunes pero en crecimiento), usa el [AWUS036AX](/en/products/alfa/awus036ax/).

### Raspberry Pi / Kali NetHunter

**Recomendado: [AWUS036ACH](/en/products/alfa/awus036ach/) o [AWUS036ACM](/en/products/alfa/awus036acm/)**

Ambos adaptadores RTL8812AU tienen un historial comprobado en hardware Raspberry Pi. Evita los modelos MT7921AUN para despliegues en Pi a menos que hayas confirmado la compatibilidad del kernel y firmware en tu imagen específica. El ACH es la opción más segura si estás construyendo un Pi NetHunter dedicado que necesita ser confiable en campo.

### Auditoría Inalámbrica Empresarial

**Recomendado: [AWUS036AXML](/en/products/alfa/awus036axml/) + [AWUS036ACH](/en/products/alfa/awus036ach/)**

Una auditoría inalámbrica empresarial moderna debe cubrir las bandas de 2.4, 5 y 6 GHz. El AXML cubre el espectro completo tri-banda incluyendo 6E, mientras que el ACH proporciona un respaldo estable y de alta potencia para el trabajo en 5 GHz. Ejecutar ambos simultáneamente con interfaces de captura separadas te da cobertura completa de bandas sin compromisos en los controladores. Usa el ACH para tareas de inyección activa y el AXML para monitoreo pasivo en 6 GHz.

### Extensión de Alcance de Drones DJI

**Recomendado: [AWUS036EACS](/en/products/alfa/awus036eacs/)**

La extensión de alcance de DJI mediante Litchi o DJI GO es un caso de uso legítimo común. El EACS con RTL8821CU se recomienda específicamente aquí porque funciona de forma nativa en Windows (donde corre el software de DJI) sin controladores adicionales, y su perfil de conectividad de propósito general es ideal para este caso de uso. No se requiere monitor mode; la conectividad en modo cliente y la potencia de transmisión son lo que importa. Combínalo con una antena panel [APA-M25](/en/products/alfa/apa-m25/) para maximizar el alcance efectivo.

---

## Recomendaciones por Sistema Operativo

### Kali Linux

Kali Linux es la plataforma de soporte principal para todos los adaptadores ALFA usados en trabajos de seguridad. El repositorio de Kali incluye `dkms-rtl8812au` para adaptadores RTL8812AU/RTL8811AU y `firmware-misc-nonfree` para adaptadores MT7921AUN/MT7921AUN. Mantén tu instalación de Kali actualizada — el paquete DKMS rastrea los cambios del kernel automáticamente.

**Configuración rápida (familia RTL8812AU):**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
sudo modprobe 88XXau
```

**Configuración rápida (familia MT7921AUN):**
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
# Reinicia o recarga el módulo:
sudo modprobe mt7921u
```

**Habilitar monitor mode:**
```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

### Ubuntu 24.04 LTS

Ubuntu 24.04 viene con el kernel 6.8. Los adaptadores MT7921AUN funcionarán de inmediato una vez que se instale `firmware-misc-nonfree`:
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

El soporte de RTL8812AU en Ubuntu requiere compilar el módulo DKMS:
```bash
sudo apt install -y git dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && sudo make dkms_install
```

### Windows 11

Todos los adaptadores ALFA vienen con controladores compatibles con Windows 10/11. Descarga el paquete de controladores desde el sitio web de ALFA Network o instala vía Windows Update para MT7921AUN (Microsoft proporciona un controlador de bandeja firmado con WHQL). Los adaptadores RTL8812AU requieren el paquete de controladores Realtek suministrado por ALFA; los controladores de Windows Update para RTL8812AU están disponibles de manera inconsistente.

Para su uso con herramientas como Acrylic Wi-Fi, inSSIDer o la versión Windows de Wireshark, los controladores ALFA proporcionan un envoltorio funcional de monitor mode en Windows mediante NDIS monitor mode — aunque esto es considerablemente menos capaz que el monitor mode de Linux para trabajos de inyección activa.

### macOS Sonoma

No existe ningún adaptador ALFA con soporte oficial para macOS Sonoma en 2026. Existen proyectos kext de la comunidad para RTL8812AU, pero no están firmados y requieren deshabilitar System Integrity Protection (SIP). La recomendación práctica es ejecutar Kali Linux en una VM (Parallels, VMware Fusion o UTM) con passthrough de USB al adaptador ALFA.

El AWUS036EACS con RTL8821CU tiene el soporte de macOS más funcional a través del kext de Realtek para macOS, pero solo para conectividad estándar de cliente — no para monitor mode.

### Raspberry Pi / Kali NetHunter

En Raspberry Pi 4 y Pi 5 ejecutando Kali NetHunter:

```bash
# Para adaptadores RTL8812AU:
sudo apt update && sudo apt install -y dkms-rtl8812au

# Para adaptadores MT7921AUN (se recomienda Pi 5 con kernel reciente):
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

{{< alert "circle-info" >}}
Si estás construyendo una caja de despliegue NetHunter dedicada, usa el [AWUS036ACH](/en/products/alfa/awus036ach/) o el [AWUS036ACM](/en/products/alfa/awus036acm/). El controlador RTL8812AU del ACH y el mt76x2u del ACM compilan de forma confiable en ARM sin dependencia de archivos de firmware. Los modelos MT7921AUN son funcionales en Pi, pero agregan una dependencia en archivos de firmware que puede causar problemas en despliegues sin conexión a internet.
{{< /alert >}}

---

## Recomendación Final

Tras evaluar los ocho adaptadores en madurez de controladores, capacidad de hardware y casos de uso reales, estas son las tres opciones que cubren a la mayoría de los profesionales:

**Opción Económica: [AWUS036ACM](/en/products/alfa/awus036acm/)**
El adaptador RTL8812AU de antena única ofrece soporte completo de monitor mode e inyección de paquetes al precio más bajo en la línea de doble banda. Ideal para consultores que quieren una herramienta confiable sin gastar de más, o para equipos que compran adaptadores en cantidad.

**Opción Versátil: [AWUS036ACH](/en/products/alfa/awus036ach/)**
El adaptador RTL8812AU de antena dual y 500 mW es el adaptador individual más recomendado para profesionales de seguridad. Cubre 2.4 y 5 GHz, acepta antenas externas, tiene la pila de controladores más madura de cualquier adaptador en esta lista y cuesta solo un poco más que el ACM. Si vas a comprar un solo adaptador y aún no sabes exactamente qué necesitas, cómpra este.

**Opción Empresarial / A Prueba de Futuro: [AWUS036AXML](/en/products/alfa/awus036axml/)**
Si el alcance de tu auditoría incluye infraestructura Wi-Fi 6E — lo cual debería para cualquier compromiso que comience en 2026 — el AXML es el único adaptador que te ofrece capacidad 6 GHz de antena dual. Combínalo con un ACH para un kit de dos adaptadores que cubre todas las bandas desde 2.4 GHz hasta 6 GHz sin compromisos.

Para instrucciones detalladas de configuración, consulta:
- [Instalar controlador ALFA en Kali Linux y Ubuntu](/en/blog/install-alfa-driver-kali-ubuntu/)
- [Reparar controlador ALFA después de actualización del kernel](/en/blog/fix-alfa-driver-kernel-update/)
- [Habilitar monitor mode en Kali Linux](/en/blog/enable-monitor-mode-kali-linux/)
- [Reseña y pruebas del controlador AWUS036AXML Wi-Fi 6E](/en/blog/awus036axml-wifi-6e-review/)
