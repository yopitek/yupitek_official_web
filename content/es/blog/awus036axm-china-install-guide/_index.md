---
title: "Guía de instalación del controlador ALFA AWUS036AXM para China: Kali Linux, Ubuntu, Debian y Raspberry Pi"
description: "Guía paso a paso para instalar los controladores ALFA AWUS036AXM en China utilizando espejos domésticos. Controlador en el núcleo MT7921AUN WiFi 6, soporte para modo monitor y VIF (este adaptador no admite inyección de paquetes). Cubre Kali Linux, Ubuntu 22/24, Debian y Raspberry Pi. No se requiere GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axm-china-install-guide"
tags: ["alfa", "awus036axm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6", "vif"]
categories: ["Guías de Controladores"]
series: ["alfa-china-install-guide"]
related_product: "/es/products/alfa/awus036axm/"
series_order: 6
featureimage: "/images/blog/awus036axm-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "¿Qué chip usa el AWUS036AXM? ¿Admite WiFi 6?"
    answer: "Usa el chip MediaTek MT7921AUN y admite WiFi 6 (doble banda 2.4G/5G Hz). Probamos 2.4/5 GHz; los 6 GHz no se verificaron."
  - question: "¿El controlador del AWUS036AXM necesita instalación manual?"
    answer: "No, el controlador mt7921u está integrado en el kernel desde Linux 5.18; solo necesitas instalar el paquete de firmware."
  - question: "¿El AWUS036AXM admite interfaces virtuales (VIF)?"
    answer: "Sí, el MT7921AUN admite completamente el VIF nativo del núcleo; puede conectarse a la red y monitorizar paquetes simultáneamente."
  - question: "¿Por qué falla la carga del controlador del AWUS036AXM en Ubuntu 22.04?"
    answer: "El kernel 5.15 predeterminado de Ubuntu 22.04 es demasiado antiguo; necesitas instalar el kernel HWE para actualizar a 5.18 o superior."
  - question: "¿Cuál es el USB ID del AWUS036AXM?"
    answer: "El USB ID del MediaTek MT7921AUN es 0e8d:7961, puedes confirmarlo con lsusb."
---

El AWUS036AXM es el adaptador WiFi 6 de ALFA con un conector USB-A en forma de L que ahorra espacio. Su chip MT7921AUN utiliza el controlador `mt7921u`, integrado en el núcleo Linux desde la versión 5.18. El conector en forma de L mantiene libres los puertos USB adyacentes en las computadoras portátiles. Esta guía cubre la configuración completa: firmware, verificación del controlador, modo monitor y VIF, sin tocar GitHub. Nota: la inyección de paquetes no funciona en este adaptador (ver más abajo).

{{< tldr >}}
El AWUS036AXM usa el chip MT7921AUN y admite WiFi 6 (2.4/5 GHz). El controlador `mt7921u` está integrado en el núcleo, sin compilación. Tras instalar el paquete de firmware, el modo monitor, AP/WPA3 y VIF funcionan (verificado); sin embargo, la inyección de paquetes falla con el kernel stock 6.17, por lo que el AWUS036AXM no es adecuado para inyección / pruebas de penetración (para inyección, usa el AWUS036ACM / ACS / AX en su lugar).
{{< /tldr >}}

Asegúrate de tener esto listo:


## Antes de comenzar

Asegúrate de tener esto listo:

1. Adaptador **ALFA AWUS036AXM**
2. Un concentrador USB con alimentación: obligatorio si estás en Raspberry Pi
3. Conexión a Internet activa para acceder a los espejos domésticos

Conecta el adaptador y confirma que tu sistema lo ve:

```bash
lsusb
```

Busca esto en la salida:

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

Si ves `0e8d:7961`, el adaptador ha sido detectado. Pasa a la sección de tu sistema operativo a continuación.

## Elige tu sistema operativo

Salta a la sección correcta para tu SO:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

El controlador MT7921AUN ya está en el núcleo de Kali. Todo lo que necesitas es el paquete de firmware de MediaTek, disponible en los espejos domésticos.

### Paso 1: Cambiar al espejo de China

Abre tu lista de fuentes en la terminal.

```bash
sudo nano /etc/apt/sources.list
```

Elimina lo que haya y pega esta línea:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Guarda: presiona **Ctrl+O**, luego Enter, luego Ctrl+X para salir. Actualiza el índice de paquetes.

```bash
sudo apt update
```

---

### Paso 2: Instalar el firmware

El MT7921AUN requiere archivos de firmware de `firmware-misc-nonfree` y `linux-firmware`.

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### Paso 3: Verificar el controlador

Después del reinicio, conecta el adaptador y verifica.

```bash
lsmod | grep mt7921
```

Deberías ver `mt7921u` en la salida. Luego confirma que apareció una interfaz inalámbrica.

```bash
iwconfig
```

Busca `wlan0` o `wlan1`.

---

### Paso 4: Activar el modo monitor {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

Busca `Mode:Monitor` en la interfaz.

---

### Paso 5: Acerca de la inyección de paquetes {#test-packet-injection}

⚠️ **El AWUS036AXM no admite la inyección de paquetes.** Con el kernel stock 6.17, `sudo aireplay-ng --test wlan1` falla: la causa principal es una regresión de mac80211 chanctx desde el kernel 6.16 (no una limitación propia del chip). Los controladores parcheados por la comunidad permiten que la inyección funcione, pero el firmware sigue bloqueando la tasa (1/6 Mbps) y no se pueden inyectar tramas HT/VHT.

Por tanto, el AWUS036AXM es adecuado para conexión normal, puntos de acceso AP y captura en modo monitor, pero **no para inyección de paquetes ni pruebas de penetración**. Si necesitas inyección, usa el AWUS036ACM / ACHM / ACS / ACH / AX / EACS en su lugar. Úsalo solo en redes propias o autorizadas.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — Núcleo 6.8, conectar y usar

Ubuntu 24.04 incluye el controlador nativamente.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Cambia a los espejos de Aliyun:
`URIs: http://mirrors.aliyun.com/ubuntu/`

```bash
sudo apt update
sudo apt install -y linux-firmware
sudo reboot
```

---

### Ubuntu 22.04 (Jammy) — Se requiere núcleo HWE

Ubuntu 22.04 requiere el núcleo HWE para tener soporte nativo.

```bash
sudo apt update
sudo apt install -y linux-generic-hwe-22.04
sudo reboot
```

Luego instala el firmware:
`sudo apt install -y linux-firmware`

---

## Debian

Cambia al espejo de Tsinghua:

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

---

## Raspberry Pi 4B / 5

> El AWUS036AXM consume hasta 2.7W. Usa siempre un concentrador USB con alimentación.

Utiliza la imagen Kali ARM64 de los espejos de Huawei:
https://repo.huaweicloud.com/kali-images/

Luego cambia al espejo de USTC e instala el firmware como en la sección de Kali.

---

## Interfaz virtual (VIF) {#virtual-interface-vif}

El MT7921AUN tiene soporte nativo completo para VIF. Puedes ejecutar una interfaz de monitor y una interfaz gestionada al mismo tiempo.

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
iwconfig
```

---

## Solución de problemas

| Problema | Causa probable | Solución |
|---------|-------------|-----|
| `lsusb` no muestra 0e8d:7961 | Falta alimentación | Prueba otro puerto o concentrador con corriente |
| El modo monitor falla | Interfaz activa | Ejecuta `sudo ip link set wlan1 down` primero |

## Referencia de espejos de China

| Recurso | URL | Uso para |
|----------|-----|---------|
| Controladores oficiales Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Paquetes de controladores |
| Espejo de Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Espejo de Aliyun | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |

{{< faq >}}

## Más guías de adaptadores Alfa para China

- [AWUS036ACH China Install Guide](/es/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potencia
- [AWUS036ACM China Install Guide](/es/blog/awus036acm-china-install-guide/) — MT7612U, VIF completo
- [AWUS036ACS China Install Guide](/es/blog/awus036acs-china-install-guide/) — RTL8811AU, modo monitor
- [AWUS036AX China Install Guide](/es/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER China Install Guide](/es/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- AWUS036AXM ← estás aquí
- [AWUS036AXML China Install Guide](/es/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS China Install Guide](/es/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

¿Preguntas? Deja un comentario abajo o contáctanos en [yupitek.com](https://yupitek.com/es/contact/).

## Referencias

1. [Controlador mt7921 del núcleo Linux](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [Documentación oficial de aircrack-ng](https://www.aircrack-ng.org/)
3. [Sitio oficial de ALFA Network](https://www.alfa.com.tw/)
4. [Documentación oficial de Kali Linux](https://www.kali.org/docs/)
