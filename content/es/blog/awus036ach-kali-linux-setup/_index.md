---
title: "Guía de Configuración ALFA AWUS036ACH para Kali Linux: Modo Monitor e Inyección de Paquetes (2026)"
description: "Guía paso a paso para instalar ALFA AWUS036ACH en Kali Linux 2024/2025, activar modo monitor con airmon-ng y verificar inyección de paquetes — con comandos completos."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "Kali-Linux", "modo-monitor", "inyección-paquetes", "RTL8812AU"]
---

El ALFA AWUS036ACH se ha ganado su lugar como el adaptador USB WiFi más recomendado en la comunidad de Kali Linux — y con buena razón. Impulsado por el chipset Realtek RTL8812AU, ofrece soporte confiable de modo monitor e inyección de paquetes en el que los profesionales de seguridad han confiado desde 2017. Esta guía te lleva por cada paso, desde desempacarlo hasta tener una configuración verificada y funcional de inyección de paquetes en Kali Linux 2024 y 2025.

---

## Por Qué el AWUS036ACH es la Elección Predeterminada

Antes de entrar en los comandos, vale la pena entender exactamente qué hace especial a este adaptador.

**El Chipset RTL8812AU**

El RTL8812AU de Realtek es un chipset 802.11ac de doble banda (2.4 + 5 GHz) con soporte robusto para las operaciones a nivel de trama que requieren las herramientas de seguridad. El controlador de código abierto mantenido en `aircrack-ng/rtl8812au` en GitHub es el resultado directo de años de colaboración entre el equipo de Aircrack-ng y la comunidad de seguridad Linux en general. Se mantiene activamente, se prueba regularmente contra nuevas versiones del kernel, y tiene soporte explícito para modo monitor e inyección de paquetes integrado desde el principio — no como una ocurrencia tardía.

**Soporte Comunitario desde 2017**

Cuando tengas un problema con el AWUS036ACH, encontrarás respuestas. El adaptador aparece en miles de publicaciones en foros, tutoriales de YouTube, walkthroughs de Hack The Box, materiales de cursos de Offensive Security e issues de GitHub. La base de conocimiento de resolución de problemas no tiene igual entre otros adaptadores.

**Rendimiento AC1200 de Doble Banda**

El adaptador entrega hasta 300 Mbps en 2.4 GHz y 867 Mbps en 5 GHz, con dos antenas RP-SMA desmontables que soportan 2×2 MIMO. Obtienes rendimiento genuino de alto rendimiento cuando lo necesitas, junto con capacidad completa de pentesting.

**USB 3.0**

La interfaz USB 3.0 evita que el adaptador se convierta en un cuello de botella durante capturas de alto ancho de banda o al ejecutar múltiples herramientas concurrentemente.

Puedes encontrarlo en nuestra tienda: [ALFA AWUS036ACH](/es/products/alfa/awus036ach/).

---

## Prerrequisitos

Antes de comenzar, confirma lo siguiente:

- **Kali Linux 2024.x o posterior** (esta guía está probada en Kali 2024.1 hasta 2025.1)
- **Un puerto USB 3.0** — aunque el adaptador funciona en USB 2.0, el rendimiento es limitado. Usa USB 3.0 para mejores resultados.
- **Conexión a internet** para descargar el controlador
- **Acceso root o sudo**
- **Herramientas de compilación instaladas** — cubiertas en el Paso 2

Si ejecutas Kali en una máquina virtual (VMware, VirtualBox, UTM), debes pasar el dispositivo USB a la VM. En VMware: VM → Dispositivos Extraíbles → conecta tu adaptador. En VirtualBox: Configuración → USB → agrega un filtro USB para el dispositivo Realtek.

---

## Paso 1: Conectar el Adaptador y Verificar Detección

Conecta el AWUS036ACH a un puerto USB y ejecuta:

```bash
lsusb
```

Deberías ver una entrada similar a:

```
Bus 001 Device 004: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

Los identificadores importantes son:
- **Vendor ID:** `0bda` (Realtek)
- **Product ID:** `8812` (RTL8812AU)

Si el dispositivo no aparece, prueba un puerto USB o cable diferente. Si aparece con un ID de producto diferente, puede que tengas una revisión de hardware distinta.

También verifica el registro de mensajes del kernel inmediatamente después de conectar:

```bash
dmesg | tail -20
```

Si el controlador ya está cargado (poco probable en una instalación nueva de Kali), verás líneas como:

```
usb 1-1: new high-speed USB device number 4 using xhci_hcd
usbcore: registered new interface driver rtl88XXau
```

Sin el controlador instalado, verás el dispositivo USB detectado pero sin interfaz creada.

---

## Paso 2: Instalar el Controlador RTL8812AU

Hay dos métodos de instalación. **El Método A (controlador aircrack-ng)** se recomienda para Kali Linux. **El Método B (DKMS)** se recomienda si quieres que el controlador persista automáticamente tras actualizaciones del kernel.

### Instalar Dependencias de Compilación

Ambos métodos requieren las mismas dependencias:

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r)
```

Esto instala las cabeceras del kernel correspondientes al kernel en ejecución, que el proceso de compilación del controlador requiere.

### Método A: Instalación Directa (controlador aircrack-ng — Recomendado para Kali)

```bash
# Clonar el controlador mantenido por aircrack-ng
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au

# Compilar el controlador
make

# Instalar el controlador
sudo make install

# Cargar el módulo del controlador
sudo modprobe 88XXau
```

Verificar que el módulo se cargó:

```bash
lsmod | grep 88XXau
```

Salida esperada:

```
88XXau               3461120  0
cfg80211             1081344  1 88XXau
```

Ahora debería aparecer una interfaz inalámbrica:

```bash
ip link show
# o
iwconfig
```

Deberías ver una nueva interfaz — típicamente `wlan0` o `wlan1` si tienes otras interfaces inalámbricas.

### Método B: Instalación con DKMS (Persiste Tras Actualizaciones del Kernel)

Con el `make install` estándar, el módulo del controlador se compila solo para tu kernel actual. Si Kali actualiza el kernel — lo cual sucede regularmente vía `apt upgrade` — el controlador deja de funcionar hasta que vuelvas a compilarlo.

DKMS (Dynamic Kernel Module Support) resuelve esto recompilando automáticamente el controlador cada vez que se instala un nuevo kernel.

```bash
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au

# Usar el script de instalación DKMS
sudo make dkms_install
```

También puedes registrarlo manualmente en DKMS:

```bash
# Obtener la versión del controlador
grep MODULE_VERSION Makefile | head -1
# Ejemplo de salida: v5.6.4.2

# Copiar fuente al directorio DKMS
sudo cp -r ../rtl8812au /usr/src/rtl8812au-5.6.4.2

# Registrar con DKMS
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2
```

Verificar el registro DKMS:

```bash
dkms status
# Esperado: rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

---

## Paso 3: Activar Modo Monitor

Con el controlador cargado y la interfaz visible, estás listo para activar el modo monitor.

### Método A: airmon-ng (Recomendado)

Primero, termina todos los procesos que puedan interferir con el modo monitor:

```bash
sudo airmon-ng check kill
```

Esto detiene NetworkManager, wpa_supplicant y otros daemons que retienen la interfaz. Salida esperada:

```
Killing these processes:
  PID Name
  1234 NetworkManager
  1235 wpa_supplicant
```

Ahora activa el modo monitor:

```bash
sudo airmon-ng start wlan0
```

Reemplaza `wlan0` con el nombre real de tu interfaz si es diferente. Salida esperada:

```
PHY     Interface   Driver      Chipset
phy0    wlan0       88XXau      Realtek Semiconductor Corp. RTL8812AU

                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)
```

La interfaz en modo monitor se llama `wlan0mon`.

### Método B: iw (Manual)

Si prefieres no terminar NetworkManager, o si airmon-ng no está disponible:

```bash
# Bajar la interfaz
sudo ip link set wlan0 down

# Cambiar a modo monitor
sudo iw dev wlan0 set type monitor

# Subirla de nuevo
sudo ip link set wlan0 up
```

Para especificar un canal al activar el modo monitor:

```bash
sudo iw dev wlan0 set channel 6
```

---

## Paso 4: Verificar el Modo Monitor

Confirma que la interfaz está en modo monitor:

```bash
iwconfig
```

Busca la entrada `wlan0mon` (o `wlan0`). Debería mostrar:

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

El indicador clave es `Mode:Monitor`. Si muestra `Mode:Managed`, el modo monitor no está activo.

También puedes usar:

```bash
iw dev wlan0mon info
```

La salida esperada incluye:

```
type monitor
```

### Verificar con Airodump-ng

Ejecuta un escaneo rápido para confirmar que el adaptador está capturando tráfico:

```bash
sudo airodump-ng wlan0mon
```

Deberías ver inmediatamente redes WiFi apareciendo en la salida. Presiona `Ctrl+C` para detener.

---

## Paso 5: Probar Inyección de Paquetes

La inyección de paquetes es la capacidad de transmitir tramas 802.11 arbitrarias. Usa el test de inyección de aireplay-ng:

```bash
sudo aireplay-ng --test wlan0mon
```

Esto difunde tramas de prueba y escucha respuestas de puntos de acceso cercanos. Un resultado exitoso luce así:

```
15:42:11  Trying broadcast probe requests...
15:42:11  Injection is working!
15:42:12  Found 3 APs

15:42:12  Trying directed probe requests...
15:42:12  aa:bb:cc:dd:ee:ff - channel: 6 - 'HomeNetwork' - 30/30: 100%
15:42:13  11:22:33:44:55:66 - channel: 11 - 'OfficeWiFi' - 28/30: 93%
```

El porcentaje indica la tasa de inyección exitosa. Cualquier valor por encima del 80% para APs cercanos es aceptable. El 100% es típico cuando estás dentro del rango.

Si ves `Injection is working!` en la salida, tu configuración está completa y lista para usar con toda la suite Aircrack-ng.

### Prueba de Inyección en Doble Banda (5 GHz)

Para probar la inyección en 5 GHz, especifica el canal:

```bash
# Cambiar a un canal de 5 GHz (ej. canal 36)
sudo iwconfig wlan0mon channel 36
# o
sudo iw dev wlan0mon set channel 36

# Ejecutar test de inyección
sudo aireplay-ng --test wlan0mon
```

---

## Solución de Problemas

### "Interface not found" / No aparece interfaz wlan después de instalar el controlador

**Causa:** El módulo del controlador no se cargó correctamente.

**Solución:**

```bash
# Verificar errores de carga del módulo
dmesg | grep -i 88XX
dmesg | grep -i rtl

# Intentar cargar el módulo manualmente
sudo modprobe 88XXau

# Si modprobe falla, verificar dependencias faltantes
modinfo 88XXau

# Recompilar el controlador
cd rtl8812au
make clean && make && sudo make install
```

También confirma que las cabeceras del kernel coinciden con tu kernel en ejecución:

```bash
uname -r
ls /lib/modules/$(uname -r)/build
```

Si el directorio `build` no existe, reinstala las cabeceras:

```bash
sudo apt install linux-headers-$(uname -r)
```

---

### "Operation not permitted" al activar modo monitor

**Causa:** No estás ejecutando como root, o falta un permiso.

**Solución:**

Siempre usa `sudo` con airmon-ng y aireplay-ng:

```bash
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

Si ya estás ejecutando como root, confirma que tu usuario de Kali es realmente root:

```bash
whoami
# Debería mostrar: root
```

---

### "No module named rtl8812au" / DKMS falla después de actualizar el kernel

**Causa:** DKMS no recompiló el controlador para el nuevo kernel.

**Solución:**

```bash
# Verificar estado DKMS
dkms status

# Si rtl8812au muestra "built" pero no "installed" para el nuevo kernel:
sudo dkms install rtl8812au/5.6.4.2 -k $(uname -r)

# Si falla, eliminar y reinstalar:
sudo dkms remove rtl8812au/5.6.4.2 --all
cd /path/to/rtl8812au
sudo make dkms_install
```

---

### El modo monitor inicia pero no se captura tráfico

**Causa:** Canal incorrecto, interferencia o problema de dominio regulatorio.

**Solución:**

```bash
# Verificar canal actual
iwconfig wlan0mon

# Configurar canal manualmente
sudo iwconfig wlan0mon channel 1

# Verificar dominio regulatorio
iw reg get

# Configurar dominio regulatorio permisivo (usar responsablemente)
sudo iw reg set BO
```

---

### Tasa de inyección baja (por debajo del 50%)

**Causa:** Distancia del AP, interferencia o problema de gestión de energía.

**Solución:**

```bash
# Deshabilitar gestión de energía en la interfaz
sudo iwconfig wlan0mon power off

# Aumentar potencia TX (verificar regulaciones locales antes de usar)
sudo iw dev wlan0mon set txpower fixed 3000  # 30 dBm
```

---

## Restaurar el Modo Administrado

Cuando termines las pruebas y quieras volver a conectarte a redes normalmente:

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

O con iw:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

---

## Resumen

| Paso | Comando |
|---|---|
| Verificar detección | `lsusb \| grep Realtek` |
| Instalar dependencias | `sudo apt install git dkms build-essential linux-headers-$(uname -r)` |
| Clonar controlador | `git clone https://github.com/aircrack-ng/rtl8812au` |
| Compilar e instalar | `make && sudo make install` |
| Cargar módulo | `sudo modprobe 88XXau` |
| Terminar procesos que interfieren | `sudo airmon-ng check kill` |
| Activar modo monitor | `sudo airmon-ng start wlan0` |
| Verificar modo monitor | `iwconfig wlan0mon` |
| Probar inyección | `sudo aireplay-ng --test wlan0mon` |

El [ALFA AWUS036ACH](/es/products/alfa/awus036ach/) combinado con Kali Linux 2024+ y el controlador RTL8812AU de aircrack-ng sigue siendo la configuración de adaptador WiFi más confiable y mejor documentada en la comunidad de pruebas de penetración. Una vez que hayas verificado que la inyección funciona, estás listo para usar toda la suite Aircrack-ng, Wireshark, Kismet, Bettercap y cualquier otra herramienta que requiera modo monitor o inyección de paquetes.
