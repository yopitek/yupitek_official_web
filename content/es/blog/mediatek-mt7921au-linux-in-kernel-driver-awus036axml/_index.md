---
title: "Deje de recompilar controladores: por qué MT7921AU es la elección para Linux y Kali"
description: "Compare MediaTek MT7921AU (controlador mt7921u integrado en el kernel) con Realtek RTL8812AU (compilación con DKMS) y descubra por qué el ALFA AWUS036AXML es la opción plug-and-play en Kali Linux."
date: 2026-08-31
author: benny-lai
lastmod: 2026-08-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["mt7921au", "kali-linux", "linux", "awus036axml", "monitor-mode", "dkms", "driver", "mediatek"]
featureimage: /images/blog/mediatek-mt7921au-linux-in-kernel-driver-awus036axml.webp
---

> **Producto cubierto**: ALFA AWUS036AXML (MediaTek MT7921AU / MT7921AUN) ｜ **Unidad de comparación**: ALFA AWUS036ACH (Realtek RTL8812AU)
> **Para quién es**: pruebas de penetración con Kali Linux, desarrollo embebido en Linux, usuarios de Raspberry Pi / computadoras de placa única
> **Objetivo del artículo**: entender la diferencia entre «soporte nativo en el kernel» y «compilación de controladores con DKMS» antes de comprar, y dedicar menos tiempo a la instalación y la resolución de problemas.

---

## La apertura: aquellos días de «recompilar el controlador tras cada actualización del sistema»

Si ha usado un adaptador USB con un chipset de la clase Realtek RTL8812AU (como el popular AWUS036ACH), probablemente haya vivido una experiencia parecida:

1. Instala el controlador mantenido por la comunidad; internet y la monitorización funcionan bien.
2. Un día ejecuta `sudo apt upgrade` y el kernel de Linux pasa a una versión nueva.
3. Tras reiniciar, el adaptador desaparece del sistema: no hay ninguna interfaz Wi-Fi (`wlan0` / `wlan1`).
4. Solo le queda **volver a descargar el código fuente, instalar DKMS y recompilar el módulo del kernel**, perdiendo toda la tarde.

El problema no está en el producto, sino en la forma en que existe el controlador. La mayoría de los controladores Linux de Realtek no están incluidos en el kernel de Linux (mainline). Para usarlos, hay que «acoplar» código fuente externo al sistema. Cada vez que el kernel se actualiza, ese acople debe recompilarse; de lo contrario, deja de coincidir con la nueva versión del kernel y falla.

Y el protagonista de hoy — el ALFA AWUS036AXML con MediaTek MT7921AU — sigue un camino completamente distinto: su controlador **vive de forma nativa dentro del kernel de Linux**.

---

## 1. Por qué falla la compilación del controlador Realtek al actualizar el kernel de Linux

### 1.1 La esencia: los módulos del kernel (Kernel Module) están ligados a una versión concreta

El kernel de Linux carga los controladores de dispositivos dinámicamente como «módulos». La clave es: **un módulo se compila para una versión específica del kernel**. Tras una actualización mayor del kernel (por ejemplo, 6.8 → 6.9), los módulos antiguos normalmente no pueden cargarse en el kernel nuevo; hay que recompilarlos.

### 1.2 DKMS: el salvavidas de la recompilación automática y sus nuevas trampas

DKMS (Dynamic Kernel Module Support) existe precisamente para resolver el dolor de «el kernel se actualiza y el módulo hay que recompilarlo». En cada actualización del kernel, **recompila el controlador automáticamente por usted**. Suena muy bien, pero en la práctica todavía se encuentra con:

- **Problemas de cadena de herramientas**: compilar requiere `build-essential`, `dkms` y las cabeceras nativas del kernel (`linux-headers-$(uname -r)`). Si falta algo, la compilación de DKMS falla directamente.
- **Incompatibilidad de versiones**: lo peor es que el kernel se actualice antes de que el controlador de GitHub se ponga al día con los nuevos cambios de API. Nunca se sabe si el próximo `apt upgrade` será el que pise esa mina.
- **Secure Boot / firma de módulos del kernel**: si el sistema tiene Secure Boot activado, los módulos sin firmar son rechazados y la interfaz del adaptador ni siquiera aparece. No se resuelve desactivando la protección; lo correcto es importar un certificado autofirmado mediante el mecanismo MOK (Machine Owner Key). Un trámite más.
- **Ansiedad por elegir la versión comunitaria**: el mismo chipset tiene varias ramas en GitHub — `aircrack-ng/rtl8812au`, `morrownr/8812au-20210820`, entre otras — con versiones y rangos de soporte de kernel distintos. Si elige mal, la compilación habrá sido en vano.

### 1.3 Su tiempo es el verdadero coste

Si solo compila una vez en la instalación, no hay problema; pero **mientras el sistema siga actualizándose, ese controlador es una responsabilidad de mantenimiento permanente**. Para los profesionales de pruebas de penetración y los desarrolladores embebidos, el tiempo valioso no debe gastarse en recompilar el controlador de un adaptador, sino en desarrollar herramientas y scripts.

---

## 2. MediaTek MT7921AU: por qué funciona «soporte nativo, plug-and-play»

### 2.1 Cómo se logra el soporte nativo: mt76 y mt7921u

Los controladores de chipsets Wi-Fi de MediaTek llevan mucho tiempo integrados en el marco de controladores inalámbricos mt76 del kernel de Linux. La serie MT7921 incluye versiones PCIe y USB:

- La serie MT7921 entró en el kernel principal (mainline) desde Linux Kernel 5.12 (versiones PCIe / M.2);
- El AWUS036AXML usa el controlador `mt7921u` para USB, incluido de forma nativa en mainline desde Linux Kernel 5.18.

En otras palabras, **no hay que descargar código fuente de GitHub, ni usar DKMS, ni compilar nada**. Con tal de que el kernel de su distribución sea lo bastante nuevo, conecte el adaptador, añada los archivos de firmware y listo. La interfaz aparecerá en `ip link`.

### 2.2 Solo necesita firmware — no el código fuente del controlador

Mucha gente cree que «no compilar» significa «no instalar nada». No es así: «no hace falta compilar el controlador» no significa «no hay que instalar absolutamente nada». El MT7921AU necesita **archivos de firmware**, no el código fuente del controlador. El firmware se gestiona como un paquete de la distribución; normalmente basta un comando:

```bash
sudo apt update
sudo apt install linux-firmware firmware-misc-nonfree   # familia Debian / Kali
sudo reboot
```

Lo habitual en Ubuntu:

```bash
sudo apt update
sudo apt install linux-firmware
sudo reboot
```

El firmware es un paquete que «sigue a la distribución»; una actualización del kernel no puede romperlo. Esa es la diferencia fundamental en coste de mantenimiento frente a un «controlador DKMS».

Los requisitos mínimos de kernel por distribución, de un vistazo:

| Sistema operativo / distribución | Kernel mínimo | ¿Hay que compilar el controlador? |
|---|---|---|
| Kali Linux (Rolling) | 6.x (incluye `mt7921u`) | No, basta añadir firmware |
| Debian 12 | 6.1 LTS | No |
| Ubuntu 22.04+ / 24.04 LTS | 5.18 o superior (se recomienda kernel HWE) | No |
| Raspberry Pi OS (Bookworm) | 6.1 LTS | No |
| Distribuciones Linux antiguas | Inferior a 5.18 | Requiere despliegue adicional; no recomendado |
| Windows 10 / 11 | — | Controlador del fabricante |
| macOS (Intel / Apple Silicon) | No compatible | **Sin controlador: no lo compre** |

> **⚠️ La advertencia de soporte más importante antes de comprar**: el AWUS036AXML **no es compatible con macOS**. Ni en Intel ni en Apple Silicon existe hoy un controlador de MT7921AU para macOS. Si macOS es su entorno principal, esta clase de adaptadores USB Wi-Fi 6 / 6E no le sirve — descártelo directamente, no lo descubra después de comprarlo.

### 2.3 Por qué el «soporte nativo» importa especialmente a los desarrolladores de Kali

En Kali Linux, las actualizaciones del kernel son muy frecuentes (es una distribución Rolling). Los usuarios de RTL8812AU contienen la respiración en cada actualización continua. `mt7921u`, en cambio, se mantiene y se prueba junto con el kernel — **por muy nuevo que sea el kernel, el controlador va a la par**. ALFA posicionó este producto para pruebas de seguridad: el modo monitor (Monitor Mode) y la inyección de paquetes (Packet Injection) son funciones estándar listas para usar.

---

## 3. AWUS036AXML en Kali Linux: plug-and-play y modo monitor en la práctica

### 3.1 Conectar, confirmar, trabajar: tres pasos

Conecte el adaptador a un puerto USB-C (con el cable 2-in-1 USB-C/USB-A incluido) y ejecute:

```bash
lsusb                 # debería ver un dispositivo MediaTek con ID 0e8d:7961
ip link               # debería aparecer una interfaz wlanX
sudo apt install linux-firmware firmware-misc-nonfree
sudo reboot
```

Tras reiniciar, confirme la interfaz:

```bash
iwconfig              # wlanX debería mostrar modo Managed
ip addr show wlanX    # obtiene dirección con normalidad
```

Incluso para la conexión por defecto, NetworkManager de las distribuciones habituales (incluida Kali) lo ve directamente — **no hace falta ningún sitio de código fuente en GitHub**.

La primera vez que conecté el AXML en Kali, ver `0e8d:7961` en `lsusb` me tranquilizó — sin clone, sin compilar; tras reiniciar, la interfaz apareció sola.

### 3.2 Pruebas de modo monitor e inyección de paquetes

Suponga que su interfaz es `wlan1`:

```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iw dev wlan1 info     # confirme que type muestra monitor
```

¡Enhorabuena! `wlan1` ahora está en estado de monitorización pasiva de tramas 802.11, y puede continuar con Wireshark o el conjunto aircrack-ng.

A continuación, pruebe la inyección de paquetes:

```bash
sudo aireplay-ng --test wlan1
```

Ver `Injection is working!` (o una salida equivalente) significa que la inyección funciona. En el controlador nativo `mt7921u`, esta capacidad es intrínseca: no requiere Hacks adicionales.

### 3.3 Modo fusión (VIF / Fusion): gestionar y monitorizar a la vez

Muchos escenarios de penetración requieren que el adaptador «actúe como cliente de internet y monitorice al mismo tiempo». El controlador nativo lo soporta mediante interfaces virtuales (Virtual Interface):

```bash
sudo iw dev wlan1 interface add mon0 type monitor
sudo ip link set mon0 up
```

Así, `wlan1` permanece en modo managed (para navegar) y `mon0` se encarga de la monitorización. Lograr esto de forma estable con un controlador RTL8812AU suele exigir tocar muchos archivos de configuración — el controlador nativo le regala esta capacidad directamente.

> **⚠️ La línea roja del uso legal**: los objetivos de prueba del modo monitor, la inyección de paquetes, Evil Twin y demás capacidades **son únicamente las redes que usted posee o para las que tiene autorización explícita** (su propio laboratorio, un segmento de pruebas autorizado por su empresa). Cualquier reconocimiento o intrusión no autorizada en redes puede violar las leyes locales. Respete los límites legales; este artículo es una explicación técnica con fines académicos y de ingeniería.

---

## 4. Hoja de evaluación previa a la compra: ¿«nativo sin compilar» o «adaptador DKMS»?

Para reducir los costes de soporte tras la compra, haga primero esta evaluación sencilla y luego decida entre el AWUS036AXML y el AWUS036ACH.

### 4.1 Comparación rápida de los dos adaptadores

| Elemento de evaluación | AWUS036AXML (MT7921AU) | AWUS036ACH (RTL8812AU) |
|---|---|---|
| Especificación inalámbrica | Wi-Fi 6E tribanda (2.4/5/6 GHz) | AC1200 doble banda (2.4/5 GHz) |
| Interfaz USB | USB-C (USB 3.2 Gen 1) | USB 3.0 Type-A |
| Controlador Linux | `mt7921u` **nativo en kernel 5.18+** | Requiere compilación externa con DKMS |
| Dificultad de instalación | Basta añadir firmware | Cadena de herramientas + compilación + (con Secure Boot) firma |
| Impacto de la actualización del kernel | Ninguno | Recompilar tras cada actualización |
| Modo monitor | Soporte nativo | Compatible |
| Inyección de paquetes | Soporte nativo | Compatible |
| macOS | No compatible | No compatible |
| Público objetivo | Linux / Kali / embebido modernos | Sistemas antiguos o escenarios de 2.4/5 GHz |

### 4.2 Lista de decisión en medio minuto

Cuantas más casillas coincidan con la descripción, **más adecuado es elegir directamente el AWUS036AXML**:

- [ ] Mi sistema principal es **Kali Linux / Ubuntu / Debian** con kernel 5.18 o superior.
- [ ] Quiero que **funcione al conectarlo**, sin tocar `dkms`, `github clone` ni cadenas de herramientas de compilación.
- [ ] Necesito el soporte nativo de la familia `mt76` y que las actualizaciones del kernel no afecten al adaptador.
- [ ] Necesito la **banda de 6 GHz** (entorno con router Wi-Fi 6E).
- [ ] Usos principales: monitorización, inyección de paquetes, Soft AP, modo fusión (VIF).
- [ ] Usaré el cable 2-in-1 USB-C / USB-A incluido con un portátil o una computadora de placa única.

Por el contrario, si no necesita 6 GHz, su sistema tiene un kernel antiguo inferior a 5.18 y domina el flujo de mantenimiento de DKMS, el AWUS036ACH sigue teniendo su lugar. Pero prepárese: en cada actualización del kernel, el controlador habrá que recompilarlo.

---

## 5. Conclusión

Para los desarrolladores modernos de Linux y Kali, el tiempo es el mayor coste. **El MediaTek MT7921AU (AWUS036AXML) le quita de encima la carga interminable del «mantenimiento del controlador»**. El controlador vive en el kernel, el firmware llega en un solo paquete, la monitorización y la inyección funcionan desde el primer momento — no hay que temer las actualizaciones continuas del kernel.

Antes de comprar, confirme solo dos cosas: **kernel del sistema ≥ 5.18** y **que no sea macOS**. Del resto se encarga el controlador nativo.

---

## Apéndice: intake rápido de resolución de problemas (para soporte y usuarios)

Si la interfaz no aparece tras conectar el adaptador, revise en orden:

1. ¿Aparece `0e8d:7961` (MediaTek) en `lsusb`? → Si no, cambie de puerto USB o revise la alimentación.
2. Ejecute `sudo apt install linux-firmware firmware-misc-nonfree` y reinicie → el firmware no instalado es la causa número uno.
3. ¿Aparece `wlanX` en `ip link`? → Si no, compruebe si la versión del kernel (`uname -r`) es ≥ 5.18.
4. **Confirme primero que el sistema operativo no es macOS** — este producto no tiene controlador para macOS; no lo envíe a reparar por este motivo.
5. Si todo lo anterior es normal y la monitorización sigue sin funcionar, compruebe si está usando el modo managed por error (`iw dev wlanX info` para revisar type).

> Aviso legal: el soporte de controladores y las versiones de kernel descritos en este artículo se basan en Linux mainline y en los paquetes oficiales de las principales distribuciones; el empaquetado y la configuración del kernel pueden variar ligeramente entre distribuciones. Este artículo no constituye ninguna promesa oficial de compatibilidad con plataformas o marcas comerciales de código cerrado. Realice todas las pruebas funcionales en un entorno legalmente autorizado.