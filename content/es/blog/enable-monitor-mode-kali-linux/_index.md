---
title: "Cómo Activar el Modo Monitor en Kali Linux 2026: Guía Completa de Adaptadores WiFi"
description: "Guía paso a paso para activar modo monitor en Kali Linux 2024/2025 con airmon-ng o el comando iw. Adaptadores ALFA compatibles, solución de problemas y verificación."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["modo-monitor", "Kali-Linux", "airmon-ng", "iw", "adaptador-WiFi", "ALFA-Network"]
featureimage: "/images/blog/enable-monitor-mode-kali-linux.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "¿En qué se diferencia el modo monitor del modo gestionado?"
    answer: "El modo monitor permite a la tarjeta capturar todas las tramas 802.11 en el aire, sin la restricción del modo gestionado que solo recibe paquetes con su propia MAC. Es la base de las pruebas de penetración inalámbrica."
  - question: "¿Qué diferencia hay entre airmon-ng e iw para activar el modo monitor?"
    answer: "airmon-ng gestiona automáticamente los procesos que interfieren y crea una interfaz virtual wlan0mon; iw modifica directamente la interfaz existente sin crear una nueva, ideal cuando se necesita control preciso."
  - question: "¿Qué hacer si la interfaz vuelve automáticamente al modo gestionado?"
    answer: "Lo causa wpa_supplicant o NetworkManager reiniciándose en segundo plano. Ejecuta airmon-ng check kill para detener estos procesos y resolver el problema."
  - question: "¿Qué tarjetas ALFA admiten completamente el modo monitor en Kali Linux?"
    answer: "AWUS036ACH (RTL8812AU), AWUS036AXML (MT7921AUN) y AWUS036ACM (MT7612U) lo admiten completamente; el ACM es plug-and-play."
  - question: "¿Cómo resolver el error Fixed channel wlan0mon: -1 en airodump-ng?"
    answer: "Indica que airodump-ng no puede cambiar de canal. Ejecuta iwconfig wlan0mon channel 1 para especificar el canal y termina los procesos wpa_supplicant residuales."
---El modo monitor elimina la restricción de la tarjeta de solo recibir sus propios paquetes; es la base de las pruebas de penetración inalámbrica. Usando airmon-ng o iw con una tarjeta ALFA puedes activarlo de forma estable en Kali Linux.

{{< tldr >}}
El modo monitor elimina la restricción de la tarjeta de solo recibir sus propios paquetes; es la base de las pruebas de penetración inalámbrica. Usando airmon-ng o iw con una tarjeta ALFA puedes activarlo de forma estable en Kali Linux.
{{< /tldr >}}


## Qué es el Modo Monitor y Por Qué es Fundamental para Pentesting

El modo monitor permite al adaptador inalámbrico capturar todas las tramas 802.11 en el aire, y es la base para el funcionamiento de herramientas como airodump-ng, Wireshark y Kismet. En Kali Linux se activa mediante airmon-ng o el comando iw.

El modo monitor es un modo de operación especial para las tarjetas de interfaz de red (NIC) inalámbricas que permite al adaptador capturar **todas** las tramas 802.11 en el aire — no sólo las dirigidas a tu dispositivo. En el modo "administrado" normal, tu adaptador solo recibe paquetes destinados a su dirección MAC y descarta todo lo demás. El modo monitor elimina ese filtro por completo.

Para los pentesters de seguridad inalámbrica, el modo monitor es fundamental. Sin él, herramientas como **airodump-ng**, **Wireshark** (en modo de captura inalámbrica) o **Kismet** no pueden interceptar tráfico de red de forma pasiva. El modo monitor permite:

- **Reconocimiento pasivo** — Escanear todos los puntos de acceso y clientes cercanos sin transmitir ninguna trama.
- **Captura de handshakes** — Escuchar los handshakes de 4 pasos WPA/WPA2 durante la autenticación de clientes.
- **Ataques de deautenticación** — Enviar tramas de gestión 802.11 (requiere inyección de paquetes además del modo monitor).
- **Detección de APs rogue** — Identificar puntos de acceso no autorizados en una red.
- **Análisis de protocolo** — Inspección profunda de tramas de gestión, control y datos 802.11.

No todos los adaptadores inalámbricos soportan el modo monitor. La capacidad está determinada por el **chipset** y el **controlador** compilado en el kernel. Los adaptadores de grado de consumidor vendidos para uso doméstico casi nunca son compatibles. Los adaptadores específicamente comercializados para investigación de seguridad — como la línea ALFA Network — están construidos con chipsets y controladores que exponen el modo monitor de forma limpia.

---

## Prerrequisitos

Antes de activar el modo monitor, confirma lo siguiente:

1. Estás ejecutando **Kali Linux** (se recomienda 2024.1 o posterior) con un kernel compatible.
2. Tu adaptador inalámbrico está conectado (adaptadores USB) o instalado (PCIe/mini-PCIe).
3. Tienes privilegios de **root o sudo**.
4. Has identificado el nombre de tu interfaz: ejecuta `ip link` o `iwconfig` y anota la interfaz inalámbrica (comúnmente `wlan0`, `wlan1` o `wlx...`).

```bash
ip link show
```

Busca una entrada que comience con `wlan` o que tenga un nombre largo basado en MAC que comience con `wlx`.

---

## Método 1: Activar Modo Monitor con airmon-ng

`airmon-ng` es parte de la suite **aircrack-ng** y es la herramienta más común para activar y desactivar el modo monitor en Kali Linux. Maneja automáticamente muchos casos especiales, incluyendo la detención de procesos que interfieren con el cambio de modo.

### Paso 1 — Terminar los procesos que interfieren

NetworkManager, wpa_supplicant y dhclient compiten con el modo monitor. Termínalos primero:

```bash
sudo airmon-ng check kill
```

Salida esperada:

```
Killing these processes:
  PID Name
  812 wpa_supplicant
  934 NetworkManager
```

> **Nota:** Esto interrumpirá tus conexiones de red existentes. Si necesitas acceso a internet durante la prueba, usa una conexión por cable o un segundo adaptador inalámbrico en modo administrado.

### Paso 2 — Iniciar el modo monitor

```bash
sudo airmon-ng start wlan0
```

Salida esperada:

```
PHY     Interface   Driver      Chipset
phy0    wlan0       rtl8812au   Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac

(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
(mac80211 station mode vif disabled for [phy0]wlan0)
```

El adaptador ahora está en modo monitor y se ha creado una nueva interfaz virtual — típicamente **wlan0mon**.

### Paso 3 — Especificar un canal (opcional pero recomendado)

Por defecto, el adaptador salta entre canales. Fíjalo a un canal específico para captura dirigida:

```bash
sudo iwconfig wlan0mon channel 6
```

---

## Método 2: Activar Modo Monitor con iw

El comando `iw` es la utilidad moderna de configuración inalámbrica de bajo nivel. Este método te da más control directo y es útil cuando `airmon-ng` no está disponible o presenta problemas.

```bash
# Bajar la interfaz
sudo ip link set wlan0 down

# Configurar modo monitor
sudo iw dev wlan0 set type monitor

# Subir la interfaz de nuevo
sudo ip link set wlan0 up
```

Los tres comandos encadenados:

```bash
sudo ip link set wlan0 down && sudo iw dev wlan0 set type monitor && sudo ip link set wlan0 up
```

Esto modifica la interfaz `wlan0` existente en su lugar en lugar de crear una nueva interfaz `wlan0mon`. Verifica que el cambio fue aplicado:

```bash
iw dev wlan0 info
```

Busca `type monitor` en la salida.

---

## Verificar el Modo Monitor

### Usando iwconfig

```bash
iwconfig
```

Una interfaz en modo monitor mostrará:

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

El campo clave es **Mode:Monitor**.

### Usando iw dev

```bash
iw dev
```

Busca `type monitor` bajo la entrada de tu interfaz. Si muestra `type managed`, el modo monitor no se aplicó correctamente.

---

## Prueba con airodump-ng

Una vez que el modo monitor está activo, pruébalo de extremo a extremo con `airodump-ng`:

```bash
sudo airodump-ng wlan0mon
```

Deberías ver inmediatamente una lista en vivo de puntos de acceso cercanos desplazándose por la pantalla, mostrando BSSID, canal, potencia de señal (PWR), tipo de cifrado y ESSID. Si la pantalla está en blanco o muestra un error, consulta la sección de solución de problemas abajo.

Para escanear solo la banda de 5 GHz:

```bash
sudo airodump-ng --band a wlan0mon
```

Para capturar una red específica y guardar la salida para análisis posterior:

```bash
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
```

---

## Tabla de Compatibilidad de Adaptadores ALFA

Los adaptadores [ALFA Network](/es/products/alfa/) son el estándar de la industria para pruebas inalámbricas en Kali Linux. Los siguientes modelos soportan completamente el modo monitor:

| Modelo | Chipset | Banda | Modo Monitor | Inyección | Notas |
|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | 2.4 / 5 GHz | ✅ | ✅ | El más popular para pentesting |
| AWUS036AXML | MT7921AUN | 2.4 / 5 / 6 GHz | ✅ | ✅ | Wi-Fi 6E, requiere kernel 5.18+ |
| AWUS036ACM | MT7612U | 2.4 / 5 GHz | ✅ | ✅ | Excelente soporte de controlador Linux |

Todos los modelos listados arriba tienen soporte de controlador verificado en Kali Linux 2024.x y 2025.x. Para chipsets como RTL8812AU, puede que necesites instalar el controlador desde el repositorio GitHub de Aircrack-ng si tu versión del kernel es muy reciente.

---

## Solución de Problemas

### "Cannot enable monitor mode" o la interfaz desaparece

Esto generalmente ocurre cuando NetworkManager reclama la interfaz. Ejecuta `airmon-ng check kill` nuevamente y vuelve a intentarlo. Si el problema persiste, detén NetworkManager manualmente:

```bash
sudo systemctl stop NetworkManager
sudo systemctl stop wpa_supplicant
```

### El modo monitor revierte a modo administrado

Algunos controladores restablecen automáticamente al modo administrado después de unos segundos. Esto generalmente significa que wpa_supplicant se reinició en segundo plano. Verifica los procesos en ejecución:

```bash
ps aux | grep -E "wpa_supplicant|NetworkManager"
```

Termina los procesos encontrados por PID, luego vuelve a activar el modo monitor.

### El nombre de la interfaz es diferente después de airmon-ng

En algunos sistemas, la nueva interfaz puede llamarse `wlan0mon`, `mon0` u otro nombre completamente distinto. Siempre verifica con `iwconfig` o `iw dev` después de ejecutar `airmon-ng start` para confirmar el nombre real de la interfaz antes de usarla con airodump-ng.

### Error "Fixed channel wlan0mon: -1" en airodump-ng

Esto significa que airodump-ng no puede cambiar canales. Intenta:

```bash
sudo iwconfig wlan0mon channel 1
```

Si falla, termina cualquier proceso de wpa_supplicant restante y vuelve a intentarlo.

### Problemas del controlador RTL8812AU en kernels más nuevos

El controlador RTL8812AU integrado en el kernel en versiones muy recientes a veces carece de soporte completo de modo monitor. Instala el controlador comunitario:

```bash
sudo apt install dkms git
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

Reinicia después de la instalación.

---

## Desactivar el Modo Monitor al Terminar

Siempre restaura tu adaptador al modo administrado cuando termines las pruebas. Dejarlo en modo monitor evita la conectividad normal de red.

### Con airmon-ng:

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

### Con iw:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

Verifica que la interfaz volvió al modo administrado con `iwconfig` y reconéctate a tu red.

---

{{< faq >}}

## Resumen

Activar el modo monitor en Kali Linux es un proceso de dos pasos: detener los servicios que interfieren y luego cambiar el modo de la interfaz usando `airmon-ng` o `iw`. La clave del éxito es usar un adaptador con un chipset compatible. Los adaptadores ALFA Network con chipsets RTL8812AU, MT7921AUN, MT7612U proporcionan la experiencia más confiable desde el primer momento en Kali Linux.

Explora la gama completa de [adaptadores inalámbricos ALFA Network disponibles en Yopitek](/es/products/alfa/) — distribuidor autorizado ALFA Network — para encontrar el adaptador adecuado para tu investigación de seguridad inalámbrica.

## Referencias

1. [Documentación oficial de aircrack-ng](https://www.aircrack-ng.org/documentation.html)
2. [Documentación oficial de Kali Linux](https://www.kali.org/docs/)
3. [Subsistema mac80211 de Linux Wireless](https://wireless.wiki.kernel.org/en/developers/Documentation/mac80211)
4. [Manual del comando iw](https://wireless.wiki.kernel.org/en/users/Documentation/iw)