---
title: "¿El controlador ALFA se rompió tras una actualización del kernel? Guía completa de reparación"
description: "¿El adaptador ALFA USB WiFi no funciona tras una actualización del kernel de Linux? Guía completa de reparación para los controladores RTL8812AU, RTL8811AU y MT7921AUN en Kali Linux y Ubuntu después de actualizaciones del kernel."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-driver", "kernel-update", "rtl8812au", "kali-linux", "ubuntu", "dkms", "troubleshooting"]
---

Ejecutas `sudo apt upgrade`, reinicias y tu adaptador ALFA ha desaparecido. Sin interfaz, sin luces, nada. Esta es la pregunta de soporte más frecuente en torno a los adaptadores ALFA Network USB WiFi en Linux, y las actualizaciones del kernel son casi siempre el culpable. Esta guía te lleva a través de un proceso sistemático de diagnóstico y reparación para las dos familias de chipsets más afectadas: **RTL8812AU** (presente en el AWUS036ACH, ACM y ACS) y **MT7921AUN** (presente en el AWUS036AXM y AXML). Sigue cada sección en orden y tu adaptador estará de vuelta en línea en menos de 15 minutos.

---

## Por qué las actualizaciones del kernel rompen los controladores

Los controladores WiFi en Linux se presentan en dos variantes: controladores **dentro del kernel** que se distribuyen con el árbol fuente del kernel, y controladores **fuera del árbol** que existen fuera de él. Entender cuál tipo tienes explica exactamente por qué las actualizaciones causan problemas.

### Controladores fuera del árbol y DKMS

El chipset RTL8812AU usa un controlador fuera del árbol mantenido por la comunidad (más comúnmente el fork `aircrack-ng/rtl8812au`). Como no forma parte del código fuente del kernel oficial, debe ser **compilado contra las cabeceras de tu kernel en ejecución específico**. Cada vez que cambia la versión del kernel — incluso una versión de parche menor como `6.6.15` → `6.6.20` — el módulo compilado ya no es compatible y el kernel se niega a cargarlo.

**DKMS (Soporte Dinámico de Módulos del Kernel)** es la solución estándar. DKMS registra el código fuente del controlador con un gancho a nivel del sistema que recompila automáticamente los módulos cuando se instala un nuevo paquete del kernel. Cuando DKMS está configurado correctamente, las actualizaciones del kernel son transparentes: reinicias en el nuevo kernel y tu adaptador ya está funcionando.

DKMS puede fallar silenciosamente por dos razones:

1. **Cabeceras del kernel faltantes** — el compilador necesita que `linux-headers-$(uname -r)` esté instalado en el momento en que llega el nuevo kernel. Si las cabeceras llegan después del kernel, DKMS pierde su ventana de compilación.
2. **`dkms.conf` desactualizado** — si el archivo de configuración de la versión del controlador instalado ya no coincide con el árbol fuente, la compilación falla con errores crípticos.

### Controladores dentro del kernel (MT7921AUN)

El chipset MT7921AUN ha estado en el kernel principal desde la versión **5.18**. Eso significa que no se necesita ningún paso de compilación — el kernel ya sabe cómo comunicarse con el hardware. Sin embargo, el controlador todavía depende de un **blob de firmware** (`mt7921u.bin`) proporcionado por un paquete separado. Si ese paquete falta o si una actualización del kernel cambia la API de firmware esperada, el adaptador puede parecer que se carga pero falla al asociarse con cualquier red.

### Comandos de diagnóstico rápido

Antes de tocar nada, ejecuta estos dos comandos para entender tu punto de partida:

```bash
# ¿Qué kernel se está ejecutando actualmente?
uname -r

# ¿Qué módulos DKMS están compilados (y para qué kernels)?
sudo dkms status
```

Si `dkms status` muestra tu controlador RTL8812AU compilado para un kernel *más antiguo* pero no para el actual, has encontrado tu problema.

---

## Paso 1: Diagnosticar tu controlador

Trabaja a través de esta secuencia de diagnóstico de arriba hacia abajo. Cada comprobación reduce la causa raíz antes de que empieces a hacer cambios.

```bash
# Verificar el kernel actual
uname -r

# Comprobar si existe alguna interfaz inalámbrica
ip link show | grep -E "wlan|wlp"

# Comprobar si el módulo del controlador está actualmente cargado
lsmod | grep -E "88XXau|rtl8812au|mt7921u"

# Comprobar el estado de compilación de DKMS para adaptadores RTL8812AU
sudo dkms status

# Escanear el buffer de mensajes del kernel para mensajes de error relevantes
sudo dmesg | grep -E "ALFA|rtl8812|mt7921" | tail -20
```

**Interpretando los resultados:**

| Salida | Significado |
|---|---|
| `ip link` no devuelve nada inalámbrico | Módulo del kernel no cargado o hardware no enumerado |
| `lsmod` no muestra módulo coincidente | El módulo falló al cargar — revisa `dmesg` para errores |
| `dkms status` muestra `broken` o faltante para el kernel actual | La compilación de DKMS falló — sigue la corrección RTL8812AU |
| `dmesg` muestra `firmware: failed to load mt7921u` | Paquete de firmware faltante — sigue la corrección MT7921AUN |
| `dmesg` muestra `disagrees about version of symbol` | Módulo compilado contra cabeceras del kernel incorrectas |

{{< alert "triangle-exclamation" >}}
Si `ip link` muestra la interfaz pero desaparece cuando intentas usarla, salta directamente a la tabla de solución de problemas específica del adaptador. Una interfaz visible pero no funcional tiene causas diferentes a una completamente desaparecida.
{{< /alert >}}

---

## Corrección: Controlador RTL8812AU (AWUS036ACH, ACM, ACS, EACS)

El RTL8812AU es el chipset ALFA más ampliamente usado para pruebas de penetración por su soporte de doble banda y modo monitor confiable. Requiere un controlador fuera del árbol y por tanto es el chipset más frecuentemente roto por las actualizaciones del kernel.

### 4.1 — Instalar las cabeceras del kernel

El primer paso, antes de tocar ningún controlador, es asegurarse de que las cabeceras de tu kernel *actual* están instaladas:

```bash
sudo apt update
sudo apt install linux-headers-$(uname -r)
```

Si este comando se ejecuta correctamente, las cabeceras ya están presentes y la recompilación de DKMS puede proceder. Si reporta que el paquete no se encuentra, tu kernel puede ser demasiado nuevo para el snapshot actual del repositorio — ejecuta `sudo apt full-upgrade` primero para obtener las cabeceras coincidentes, luego reinicia antes de continuar.

### 4.2 — Recompilar via DKMS (camino más rápido)

Con las cabeceras en su lugar, pide a DKMS que recompile todos los módulos registrados para el kernel en ejecución:

```bash
sudo dkms autoinstall
```

Observa la salida cuidadosamente. Una compilación exitosa termina con `DKMS: install completed`. Si tiene éxito, recarga el módulo sin reiniciar:

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

Si aparece la interfaz, has terminado. Procede al paso 4.4 para verificar el modo monitor.

### 4.3 — Reinstalación completa desde el código fuente (cuando DKMS falla)

Si `dkms autoinstall` reporta errores, el código fuente del controlador registrado está corrupto o desactualizado. Elimínalo completamente y reinstala desde el último código fuente upstream:

```bash
# Eliminar todas las versiones registradas en DKMS del controlador
sudo dkms remove rtl8812au/5.6.4.2 --all 2>/dev/null

# Clonar el último código fuente del controlador
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# Registrar código fuente con DKMS, compilar e instalar en un paso
sudo make dkms_install
```

{{< alert "triangle-exclamation" >}}
El número de versión `5.6.4.2` en el comando `dkms remove` es una versión común pero la tuya puede diferir. Ejecuta `sudo dkms status` primero y usa la cadena de versión exacta que se muestra en la salida.
{{< /alert >}}

Después de que se complete la compilación:

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

### 4.4 — Verificar el modo monitor

El adaptador está físicamente presente y el controlador está cargado. Confirma que el modo monitor — la función que hace que este adaptador valga la pena para pruebas de seguridad — todavía funciona:

```bash
sudo airmon-ng start wlan0
```

Reemplaza `wlan0` con tu nombre de interfaz real de `ip link`. Una respuesta exitosa muestra `monitor mode vif enabled` con un nuevo nombre de interfaz como `wlan0mon`.

### 4.5 — Método del paquete de Kali (más fácil)

Kali Linux incluye una compilación DKMS preempaquetada del controlador RTL8812AU que se mantiene sincronizada con el kernel de Kali. Si estás en Kali, usa este enfoque en lugar de clonar desde GitHub:

```bash
sudo apt update && sudo apt install realtek-rtl88xxau-dkms
```

Este único comando instala el código fuente del controlador, lo registra con DKMS y lo compila contra el kernel actual. Las futuras ejecuciones de `apt full-upgrade` mantendrán las cabeceras y el controlador sincronizados automáticamente.

---

## Corrección: Controlador MT7921AUN (AWUS036AXM, AXML)

El chipset MT7921AUN (Wi-Fi 6E) toma un camino completamente diferente. Como es un **controlador dentro del kernel** desde Linux 5.18, no hay DKMS, no hay compilación y no hay clonación de GitHub. Las actualizaciones del kernel no deberían romperlo — pero los problemas de empaquetado de firmware a veces sí lo hacen.

### 5.1 — Instalar el paquete de firmware

El módulo del kernel (`mt7921u.ko`) ya está presente, pero necesita un binario de firmware del espacio de usuario para inicializar el hardware:

```bash
sudo apt install firmware-misc-nonfree
```

En Ubuntu, este paquete se encuentra en el componente de repositorio `non-free`. Si el comando falla, asegúrate de tener habilitadas las fuentes non-free en `/etc/apt/sources.list`.

### 5.2 — Recargar el controlador

Después de instalar el firmware, fuerza una recarga del controlador sin reiniciar:

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
```

Luego comprueba la interfaz:

```bash
ip link show | grep -E "wlan|wlp"
```

### 5.3 — Verificar tu versión del kernel

El controlador MT7921AUN requiere el kernel **5.18 o posterior**. Si instalaste una imagen mínima de Kali o Ubuntu que se publicó antes de esta versión del kernel, el módulo simplemente no existe:

```bash
uname -r
# La salida debe ser 5.18.x o superior
```

Si tu kernel es anterior a 5.18, actualízalo (paso 5.4).

### 5.4 — Actualizar el kernel

```bash
sudo apt update && sudo apt full-upgrade && sudo reboot
```

{{< alert "triangle-exclamation" >}}
Usa `full-upgrade` en lugar de `upgrade`. El subcomando `upgrade` retiene los paquetes que requieren eliminar otros — esto a menudo significa que el propio paquete del kernel queda retenido. `full-upgrade` permite la resolución de dependencias necesaria.
{{< /alert >}}

### 5.5 — Verificar después del reinicio

Después de reiniciar en el nuevo kernel, confirma que todo funciona:

```bash
sudo modprobe mt7921u
ip link show
sudo dmesg | grep mt7921 | tail -10
```

Una salida de `dmesg` saludable muestra el firmware cargándose correctamente y el dispositivo USB registrándose como interfaz de red.

---

## Mantener los controladores activos tras futuras actualizaciones

La prevención es más sencilla que la reparación. Estas prácticas evitan que las actualizaciones del kernel vuelvan a romper tu adaptador.

**Usa siempre `full-upgrade` en Kali rolling:**

```bash
sudo apt update && sudo apt full-upgrade
```

El comando `full-upgrade` garantiza que cuando se instala un nuevo paquete del kernel, el paquete `linux-headers` coincidente se instala en la *misma transacción*. Los ganchos de DKMS se activan durante la instalación del paquete — si las cabeceras llegan en una ejecución posterior de `apt` después del kernel, DKMS pierde la compilación.

**Instalar el metapaquete de DKMS:**

```bash
sudo apt install dkms linux-headers-generic
```

Esto trae `linux-headers-generic` como dependencia del paquete DKMS, para que las cabeceras siempre se mantengan actualizadas junto con el kernel.

**Pila del kernel HWE de Ubuntu:**

En Ubuntu LTS, la pila del kernel de Habilitación de Hardware recibe actualizaciones más frecuentes y mejor soporte de hardware que el kernel GA. Instálalo una vez y las actualizaciones se manejan automáticamente:

```bash
sudo apt install linux-generic-hwe-24.04
```

**Verificar que la autoinstalación de DKMS esté habilitada:**

```bash
cat /etc/dkms/framework.conf | grep autoinstall
```

Si esta línea está comentada o establecida en `no`, DKMS no recompilará los módulos automáticamente. Descoméntala o establécela en `yes` en `/etc/dkms/framework.conf`.

---

## Tabla de solución de problemas específica del adaptador

| Síntoma | Chipset probable | Causa raíz | Comando rápido |
|---|---|---|---|
| Interfaz desaparece después del reinicio | RTL8812AU | Compilación DKMS falló | `sudo dkms autoinstall` |
| Interfaz desaparece, `dmesg` muestra error de firmware | MT7921AUN | Paquete de firmware faltante | `sudo apt install firmware-misc-nonfree` |
| Interfaz aparece pero desaparece después de 30s | RTL8812AU | Versión de módulo incompatible | `sudo dkms remove --all && sudo make dkms_install` |
| Modo monitor falla con `SIOCSIFFLAGS` | RTL8812AU | Rama de controlador incorrecta | Clonar `aircrack-ng/rtl8812au` y reinstalar |
| `iwconfig` no muestra extensiones inalámbricas | Cualquiera | Módulo no cargado | `sudo modprobe 88XXau` o `sudo modprobe mt7921u` |
| Interfaz presente pero no encuentra redes | MT7921AUN | Kernel < 5.18 | `sudo apt full-upgrade && sudo reboot` |
| `dkms status` muestra `broken` | RTL8812AU | Desajuste fuente/cabeceras | `sudo apt install linux-headers-$(uname -r)` luego recompilar |
| Potencia TX limitada a 20 dBm | RTL8812AU | Bloqueo de dominio regulatorio | `sudo iw reg set US` (ajusta según tu región) |

---

## Si nada funciona: método de instalación limpia

Cuando múltiples intentos de recompilación han fallado y `dkms status` muestra una salida confusa de varias instalaciones parciales, empezar desde cero es más rápido que depurar:

```bash
# Purgar el paquete de Kali si estaba instalado
sudo apt purge realtek-rtl88xxau-dkms

# Eliminar todas las entradas DKMS para rtl8812au
for ver in $(sudo dkms status | grep rtl8812au | awk -F'[,/]' '{print $2}' | tr -d ' '); do
    sudo dkms remove rtl8812au/$ver --all
done

# Eliminar el directorio fuente sobrante si está presente
sudo rm -rf /usr/src/rtl8812au*

# Limpiar cualquier caché de módulos obsoleto
sudo depmod -a

# Clonar e instalar desde cero
git clone https://github.com/aircrack-ng/rtl8812au.git /tmp/rtl8812au
cd /tmp/rtl8812au
sudo make dkms_install
sudo modprobe 88XXau
ip link show | grep wlan
```

{{< alert "triangle-exclamation" >}}
El bucle que elimina entradas DKMS fallará silenciosamente si no se encuentran versiones — eso está bien. El paso importante es `sudo rm -rf /usr/src/rtl8812au*` que elimina cualquier árbol fuente que pueda estar en un estado roto.
{{< /alert >}}

---

## Lista de comprobación de prevención

Usa esta lista antes de cada actualización del sistema para evitar sorpresas durante un compromiso:

**Antes de `apt upgrade`:**

```bash
# Ver exactamente qué paquetes del kernel están pendientes
apt list --upgradable 2>/dev/null | grep linux-image
```

Si viene un nuevo kernel, planifica un reinicio de prueba antes de cualquier trabajo en producción.

**Después de cada actualización y reinicio:**

```bash
# Confirmar que el adaptador ha regresado
ip link show | grep -E "wlan|wlp"

# Confirmar que el modo monitor sigue funcionando
sudo airmon-ng check
```

**Mantén un respaldo:**
- Ten una unidad USB con una imagen Kali Live (o un segundo adaptador con un controlador que funcione). Los problemas de conectividad durante un compromiso programado son costosos — un respaldo físico tarda minutos en prepararse y puede salvar el trabajo.

**Fijar paquetes de controladores críticos en Kali:**

```bash
# Evitar que un paquete de controlador específico sea eliminado automáticamente durante las actualizaciones
sudo apt-mark hold realtek-rtl88xxau-dkms
```

Libera el bloqueo antes de actualizar explícitamente el controlador:

```bash
sudo apt-mark unhold realtek-rtl88xxau-dkms && sudo apt upgrade realtek-rtl88xxau-dkms
```

---

## Resumen

Los fallos de controladores ALFA tras actualizaciones del kernel siguen un patrón predecible y tienen soluciones predecibles. Los adaptadores RTL8812AU necesitan `dkms autoinstall` (o un clon limpio de `aircrack-ng/rtl8812au`) más cabeceras del kernel coincidentes. Los adaptadores MT7921AUN necesitan `firmware-misc-nonfree` y un kernel 5.18 o posterior. La solución a largo plazo en ambos casos es asegurarse de que `apt full-upgrade` — no `apt upgrade` — sea tu comando de actualización estándar, lo que mantiene cabeceras y kernels sincronizados.

---

**Guías relacionadas:**
- [Cómo instalar el controlador ALFA USB WiFi en Kali Linux y Ubuntu](/es/blog/install-alfa-driver-kali-ubuntu/) — empieza aquí si nunca has instalado el controlador antes
- [Guía de configuración AWUS036ACH en Kali Linux](/es/blog/awus036ach-kali-linux-setup/) — guía completa de configuración incluyendo verificación de modo monitor e inyección de paquetes
