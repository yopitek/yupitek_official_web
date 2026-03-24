---
title: "Adaptador ALFA WiFi en Raspberry Pi con Kali Linux: Guía de Configuración"
description: "Instala adaptadores ALFA USB WiFi en Raspberry Pi con Kali Linux ARM64. Cubre la compilación del controlador RTL8812AU del AWUS036ACH, modo monitor y configuración de pentesting portátil."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["raspberry-pi", "kali-linux", "alfa-network", "AWUS036ACH", "RTL8812AU", "portable-pentest", "monitor-mode"]
---

Un portátil con Kali Linux es la estación de trabajo estándar para pentesting — pero está lejos de ser la única opción. Una Raspberry Pi 4 o Pi 5 combinada con un adaptador ALFA USB WiFi te proporciona una plataforma compacta, sin ventilador y con refrigeración pasiva que cabe en el bolsillo de una chaqueta, funciona con una batería portátil USB-C y puede dejarse desatendida en un entorno objetivo durante horas. Las imágenes de Kali Linux ARM64 se distribuyen directamente desde Offensive Security y se ejecutan de forma nativa en la Pi 4 y Pi 5 sin emulación, dándote el conjunto completo de herramientas: Aircrack-ng, Kismet, Wireshark, Bettercap y el resto de los metapaquetes estándar de Kali.

El principal obstáculo es el controlador. El chipset RTL8812AU del AWUS036ACH y AWUS036ACM no está en el kernel principal, lo que significa que no puedes enchufar el adaptador y esperar que funcione. Debes compilar el controlador contra tu kernel ARM64 en ejecución — y los indicadores de compilación difieren de x86-64. Esta guía te lleva a través de cada paso.

---

## Hardware Recomendado

No todas las combinaciones de modelos de Pi, adaptadores y fuentes de alimentación funcionan de manera confiable. La siguiente tabla refleja lo que se sabe que funciona bien y qué concesiones esperar.

| Componente | Recomendado | Notas |
|---|---|---|
| Ordenador de placa única | Raspberry Pi 5 (4 GB u 8 GB) | Pi 4 (4 GB+) funciona bien; Pi 3B+ es demasiado lento para capturas en tiempo real |
| Adaptador principal | ALFA AWUS036ACH | Chipset RTL8812AU; mejor soporte de controlador ARM; dual-band AC1200 |
| Adaptador alternativo | ALFA AWUS036ACM | Variante RTL8812AU; soporte de controlador similar; consumo ligeramente menor |
| Adaptador WiFi 6 | ALFA AWUS036AXM o AXML | Chipset MT7921U; nativo en kernel desde 5.18; necesita firmware-misc-nonfree |
| Hub USB | Hub USB 3.0 con alimentación | AWUS036ACH consume ~500 mW; puede causar caídas de tensión en Pi sin hub |
| Almacenamiento | MicroSD 32 GB+ (Clase 10 / A2) | Las tarjetas A2 son notablemente más rápidas en arranque y operaciones apt |
| Fuente de alimentación | Fuente oficial Pi USB-C (≥ 3 A) | Los adaptadores de terceros son una causa común de problemas de estabilidad |

{{< alert "triangle-exclamation" >}}
El AWUS036ACH es un dispositivo USB de alta corriente. Conectarlo directamente a una Raspberry Pi 4 o Pi 5 sin un hub USB con alimentación puede provocar que la Pi reduzca su rendimiento o se reinicie bajo carga. Utiliza siempre un hub con alimentación cuando uses el AWUS036ACH junto con otros periféricos USB.
{{< /alert >}}

---

## Instalación de Kali Linux ARM64 en Raspberry Pi

### Descarga de la Imagen ARM

Kali Linux mantiene imágenes ARM64 de primera parte para Raspberry Pi en [https://www.kali.org/get-kali/#kali-arm](https://www.kali.org/get-kali/#kali-arm). Descarga la imagen etiquetada como **Raspberry Pi 4 (64-bit)** o **Raspberry Pi 5 (64-bit)**. No uses la imagen de 32 bits — el kernel ARM64 es necesario para los pasos de compilación del controlador en esta guía.

### Escritura en la MicroSD

Puedes escribir con la herramienta GUI Raspberry Pi Imager o con `dd` desde la línea de comandos:

```bash
# Reemplaza /dev/sdX con tu dispositivo de tarjeta SD real (verifica con lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Con Raspberry Pi Imager: selecciona **Usar imagen personalizada** → elige el archivo `.img.xz` de Kali → selecciona tu tarjeta SD → escribe.

### Primer Arranque y Configuración Inicial

Inserta la tarjeta SD, conecta monitor y teclado (o configura el acceso headless primero), y enciende. Las credenciales predeterminadas son:

- **Usuario:** `kali`
- **Contraseña:** `kali`

Después de iniciar sesión, ejecuta `kali-tweaks` y sigue las indicaciones para reforzar la configuración predeterminada. Luego actualiza el sistema completamente antes de tocar ningún controlador:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

{{< alert "circle-info" >}}
Si planeas acceder a la Pi a través de SSH, activa SSH antes del primer arranque colocando un archivo vacío llamado `ssh` en la partición `/boot` de la tarjeta SD. Este es el mismo mecanismo que el Raspberry Pi OS estándar.
{{< /alert >}}

---

## Instalación del Controlador RTL8812AU en Kali ARM64 (AWUS036ACH / ACM)

El controlador RTL8812AU no está incluido en el kernel Linux principal. En ARM64 debes compilar desde el código fuente o instalar la versión DKMS empaquetada por Kali. Ambos métodos se describen a continuación — comienza con el enfoque del paquete y recurre a la compilación manual solo si encuentras incompatibilidades de versión de kernel.

### Opción 1: Paquete Kali (Punto de Partida Recomendado)

Kali Linux incluye una versión DKMS empaquetada del controlador RTL8812AU que gestiona la recompilación automáticamente cuando el kernel se actualiza.

```bash
sudo apt install realtek-rtl88xxau-dkms
```

Después de la instalación, reinicia y verifica que el módulo se cargó:

```bash
sudo modprobe 88XXau
ip link show
```

Si ves una interfaz `wlan1` (asumiendo que `wlan0` es el adaptador incorporado de la Pi), el controlador está funcionando. Este paquete puede estar unos días por detrás de la versión en GitHub, pero es el punto de partida con menos fricción.

{{< alert "circle-info" >}}
El paquete de Kali suele ser suficiente para la mayoría de las configuraciones ARM64. Solo procede con la compilación manual si el paquete DKMS no compila contra tu versión de kernel actual, que puedes verificar con `uname -r`.
{{< /alert >}}

### Opción 2: Compilación Manual desde el Código Fuente (ARM64)

Si el paquete DKMS falla — más comúnmente porque tu kernel es más nuevo que la última versión probada del paquete — compila directamente desde el fork de Aircrack-ng en GitHub. Esta es la fuente oficial para el soporte ARM64.

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)

git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# Cambiar los indicadores de plataforma de x86 a ARM64
sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/' Makefile
sed -i 's/CONFIG_PLATFORM_ARM64_RPI = n/CONFIG_PLATFORM_ARM64_RPI = y/' Makefile

sudo make dkms_install
```

Los comandos `sed` son la diferencia crítica respecto a una compilación x86-64. Sin ellos, el Makefile usa rutas de plataforma x86 por defecto y el módulo resultante no cargará en ARM64.

Después de una compilación exitosa, carga el módulo y verifica:

```bash
sudo modprobe 88XXau
ip link show
```

Deberías ver una nueva interfaz — típicamente `wlan1`. Si `ip link show` muestra la interfaz, el controlador funciona correctamente.

---

## MT7921U en Raspberry Pi (AWUS036AXM / AXML)

El chipset MediaTek MT7921U usado en los AWUS036AXM y AXML está en el kernel principal desde la versión 5.18. Las imágenes de Kali Linux ARM64 incluyen un kernel muy por encima de ese umbral, lo que significa que el controlador se carga automáticamente cuando enchufas el adaptador — sin necesidad de compilación.

El único paso adicional necesario es instalar el firmware de código cerrado que requiere el MT7921U:

```bash
sudo apt install firmware-misc-nonfree
sudo reboot
```

Después de reiniciar, verifica que el adaptador se detecta y la interfaz está activa:

```bash
lsusb
sudo modprobe mt7921u
ip link show
```

Si `lsusb` muestra un dispositivo MediaTek e `ip link show` lista una nueva interfaz inalámbrica, el adaptador está listo. El soporte del modo monitor en el MT7921U ha mejorado significativamente desde el kernel 5.18, pero puede ser menos fiable que los adaptadores basados en RTL8812AU para ciertos tests de inyección de paquetes. Para máxima compatibilidad con flujos de trabajo de pentesting más antiguos, el AWUS036ACH sigue siendo la opción más sólida.

---

## Habilitar el Modo Monitor en Raspberry Pi

La Raspberry Pi tiene una interfaz WiFi integrada (`wlan0`). Mantenla conectada a tu red para el acceso SSH. Usa el adaptador ALFA (`wlan1`) exclusivamente para modo monitor y captura de paquetes. Nunca pongas `wlan0` en modo monitor en una Pi headless — perderás tu conexión SSH.

```bash
# Terminar los procesos que interfieren con el modo monitor (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# Habilitar el modo monitor en la interfaz del adaptador ALFA
sudo airmon-ng start wlan1

# Verificar que el modo monitor está activo
sudo iwconfig wlan1mon

# Comenzar a capturar en todos los canales
sudo airodump-ng wlan1mon
```

{{< alert "circle-info" >}}
`airmon-ng start wlan1` crea una nueva interfaz llamada `wlan1mon`. Ejecuta siempre las herramientas posteriores contra `wlan1mon`, no `wlan1`. Puedes confirmar el nombre de la interfaz con `iwconfig` o `ip link show`.
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
Ejecutar `airmon-ng check kill` detiene NetworkManager y wpa_supplicant. Si estás conectado por SSH a través de `wlan0`, esto también interrumpirá tu sesión SSH. Para configuraciones headless, conéctate a través de Ethernet o una segunda interfaz cableada antes de ejecutar estos comandos, o usa `tmux` para que tu sesión sobreviva a una desconexión.
{{< /alert >}}

Para deshabilitar el modo monitor y restaurar el modo administrado:

```bash
sudo airmon-ng stop wlan1mon
sudo systemctl start NetworkManager
```

---

## Consejos para la Configuración de Pentesting Portátil

Hacer funcionar el hardware es solo la mitad del trabajo. Estas elecciones prácticas marcan la diferencia entre un kit de campo estable y un montón frustrante de cables.

**Arquitectura de red:** Usa `wlan0` (WiFi integrado de la Pi) para mantener tu conexión de gestión — accede a la Pi por SSH desde un portátil en la misma LAN o punto de acceso. Dedica `wlan1` (adaptador ALFA) completamente a la actividad de pentesting. Nunca mezcles los dos roles.

**Operación headless:** Evita conectar teclado, ratón y monitor en el campo. Configura SSH en el primer arranque y accede a todo a través de un emulador de terminal en tu portátil. Las sesiones de `tmux` persisten tras la reconexión, lo cual es invaluable cuando las condiciones de red son inestables.

**Alimentación:** Usa la fuente de alimentación oficial USB-C de Raspberry Pi con un mínimo de 3 A. Para el AWUS036ACH, añade un hub USB con alimentación de 2.5 A o más. Una batería portátil USB-C de calidad (65 W+) puede alimentar la Pi, el hub y el adaptador simultáneamente durante 4-6 horas según la carga.

**Almacenamiento:** Escribe los registros de Kismet y los archivos de captura en un USB SSD en lugar de la tarjeta MicroSD. Las tarjetas MicroSD tienen ciclos de escritura limitados y se degradan rápidamente bajo cargas de registro sostenidas. Un USB 3.0 SSD conectado al hub con alimentación es más rápido y duradero.

**Carcasa:** Elige una carcasa para Pi con puertos USB abiertos o ranuras que acomoden el hub con alimentación. Las carcasas de aluminio con aletas de disipador pasivo ayudan a gestionar la temperatura durante capturas prolongadas.

---

## Ejecutar Kismet en Raspberry Pi

Kismet es un escáner WiFi pasivo que se ejecuta como servidor en segundo plano y expone una interfaz web basada en navegador. Es muy adecuado para despliegues de Pi headless: dejas la Pi funcionando y revisas la interfaz web desde cualquier dispositivo en la misma red.

```bash
sudo apt install kismet

# Lanzar Kismet usando el adaptador ALFA en modo monitor
kismet -c wlan1
```

{{< alert "circle-info" >}}
Kismet pondrá la interfaz en modo monitor por sí mismo si pasas el nombre de la interfaz directamente. No necesitas ejecutar `airmon-ng start` antes de lanzar Kismet. Kismet gestiona el ciclo de vida de la interfaz internamente.
{{< /alert >}}

Una vez en ejecución, accede a la interfaz web de Kismet desde cualquier navegador en tu red:

```
http://raspberrypi.local:2501
```

En el primer arranque, Kismet te pide crear un nombre de usuario y contraseña de administrador. Después de iniciar sesión, puedes ver redes detectadas, clientes asociados, historial de intensidad de señal y datos GPS si hay un dongle GPS conectado.

Kismet registra todo en archivos de base de datos `.kismet` en `~/.kismet/` por defecto. Estos pueden exportarse posteriormente para análisis o carga en WiGLE.

---

## Caso de Uso: Configuración de Wardriving

Una Raspberry Pi ejecutando Kismet con un adaptador ALFA y un dongle GPS es un kit completo de wardriving autocontenido — más pequeño y barato que cualquier dispositivo dedicado de wardriving.

**Componentes necesarios:**
- Raspberry Pi 4 o Pi 5
- ALFA AWUS036ACH (o AWUS036ACM)
- Dongle GPS USB (los chipsets u-blox funcionan bien con Kismet)
- Hub USB con alimentación
- Batería portátil USB-C (65 W+, con carga pass-through)

**Pasos de configuración:**

1. Instalar Kismet y los paquetes GPS:

```bash
sudo apt install kismet gpsd gpsd-clients
```

2. Configurar `gpsd` para leer desde tu dongle GPS:

```bash
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
```

3. Iniciar Kismet con soporte GPS:

```bash
kismet -c wlan1 --gps=gpsd:host=localhost,port=2947
```

4. Monta la Pi, el hub, el adaptador y la batería en una bolsa o carcasa y colócalo en tu vehículo. Accede a la interfaz web de Kismet desde el punto de acceso de tu teléfono o una tablet conectada a la misma red WiFi que la Pi.

Los registros de Kismet capturan coordenadas GPS para cada red detectada. Exporta la base de datos `.kismet` al formato CSV de WiGLE usando `kismetdb_to_wigle` (incluido con Kismet) y súbela a WiGLE para mapear.

{{< alert "triangle-exclamation" >}}
Cumple siempre con las leyes locales antes de realizar cualquier actividad de escaneo de redes. En muchas jurisdicciones, el wardriving con escaneo solo pasivo es legal; el sondeo activo o la conexión a redes sin autorización no lo es. Conoce las regulaciones locales de tu zona.
{{< /alert >}}

---

## Lectura Adicional

Para la guía completa de instalación del controlador RTL8812AU en Kali Linux y Ubuntu de escritorio, consulta la guía [Instalar Controlador ALFA en Kali Linux y Ubuntu](/es/blog/install-alfa-driver-kali-ubuntu/). Si aún estás decidiendo qué adaptador comprar, la [Guía de Compra de Adaptadores ALFA WiFi 2026](/es/blog/alfa-wifi-adapter-buyer-guide-2026/) cubre cada modelo actual con detalles del chipset y recomendaciones por caso de uso.
