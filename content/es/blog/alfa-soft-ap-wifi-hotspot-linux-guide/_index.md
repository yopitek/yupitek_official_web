---
title: "Guía Completa de Soft AP ALFA Network 2026: Crear Hotspots WiFi en Kali Linux, Ubuntu, Debian y Raspberry Pi 4/5"
description: "Investigación exhaustiva del soporte Soft AP (hostapd/WiFi Hotspot) de los adaptadores USB WiFi de ALFA Network en Kali Linux, Ubuntu, Debian y Raspberry Pi 4/5. Incluye guías completas de configuración para AWUS036ACM, AWUS036ACH y AWUS036AXML."
date: 2026-05-21
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Soft-AP", "WiFi-Hotspot", "hostapd", "Kali-Linux", "Ubuntu", "Debian", "Raspberry-Pi", "AWUS036ACM", "AWUS036ACH", "AWUS036AXML", "MT7612U", "RTL8812AU", "MT7921AUN", "Linux-WiFi"]
featureimage: "/images/blog/alfa-soft-ap-wifi-hotspot-linux-guide.webp"
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "¿Las tarjetas USB ALFA pueden funcionar como punto de acceso WiFi en Linux?"
    answer: "Depende del chipset. El AWUS036ACM (MT7612U) lo admite completamente y es plug-and-play; el AWUS036ACH (RTL8812AU) lo admite con condiciones; el AWUS036AXML lo admite parcialmente y requiere ajustes."
  - question: "¿Qué tarjeta ALFA es la más adecuada para crear un Soft AP en Raspberry Pi?"
    answer: "El AWUS036ACM es la mejor opción: controlador del núcleo plug-and-play, consumo de solo 400 mA adecuado para la alimentación de la Pi, soporte de WPA3 y VIF, y estabilidad en todas las plataformas."
  - question: "¿Cómo verificar si la tarjeta admite el modo AP?"
    answer: "Ejecuta iw list | grep -A 10 'Supported interface modes'. Si la salida incluye * AP, el controlador admite Soft AP y hostapd funcionará correctamente."
  - question: "¿Qué limitaciones tiene el Soft AP con el controlador RTL8812AU?"
    answer: "No admite WPA3 (solo WPA2-PSK), no admite VIF (necesitas dos tarjetas para separar funciones), y consume unos 800 mA, por lo que en la Pi requiere un concentrador USB con alimentación."
  - question: "¿Qué hacer si el WiFi se desconecta al ejecutar Soft AP con AWUS036AXML?"
    answer: "El MT7921AUN tiene Bluetooth 5.2 integrado que interfiere con el WiFi. Ejecuta echo 'install btusb /bin/false' en /etc/modprobe.d/ para desactivar permanentemente el controlador de Bluetooth y reinicia."
---


{{< tldr >}}
La compatibilidad de Soft AP de las tarjetas ALFA depende del controlador del chip. El AWUS036ACM es la opción estable para todas las plataformas; el AWUS036ACH funciona pero sin WPA3; el AWUS036AXML requiere desactivar Bluetooth y actualizar el firmware; el RTL8832BU (AX / AXER) funciona con el controlador integrado en el kernel 6.17 o superior.
{{< /tldr >}}

> "¿Puedo usar adaptadores USB WiFi ALFA como hotspot WiFi (Soft AP) en Kali Linux / Ubuntu / Raspberry Pi?"



## Introducción

> "¿Puedo usar adaptadores USB WiFi ALFA como hotspot WiFi (Soft AP) en Kali Linux / Ubuntu / Raspberry Pi?"

Esta es una de las preguntas más frecuentes que recibimos en Yopitek. La pregunta parece sencilla, pero la respuesta varía enormemente según el modelo y el chipset — **no todos los adaptadores USB WiFi pueden funcionar en modo Soft AP.**

Este artículo recopila más de 500 discusiones comunitarias de GitHub (morrownr/USB-WiFi), foros técnicos de Reddit, documentación oficial de Raspberry Pi y comentarios de usuarios reales para ofrecer un informe honesto y completo sobre qué adaptadores ALFA funcionan, cuáles no, y el proceso completo de configuración paso a paso.

---

## 1. ¿Qué es Soft AP? Cómo funciona en Linux {#what-is-softap}

**Soft AP (Software Access Point)** es la capacidad de convertir un adaptador USB WiFi ordinario en una estación base inalámbrica (Access Point) usando software — principalmente **hostapd**. Esto permite que otros dispositivos (teléfonos, portátiles, equipos IoT) se conecten a la red sin comprar un router o un AP dedicado.

Esta capacidad es invaluable en varios escenarios:

- **Router de viaje / hogar**: de viaje o de acampada, conecte un adaptador ALFA a su portátil o Raspberry Pi y cree al instante un hotspot WiFi portátil
- **Laboratorio de pruebas de penetración**: monte un Rogue AP aislado para investigación de seguridad
- **Relé IoT**: cree un repetidor en zonas sin cobertura para que los sensores IoT puedan transmitir sus datos
- **Despliegue de IA en el borde**: en entornos industriales sin red cableada, convierta el dispositivo en un hotspot al que se conecten otros equipos
- **Comunicaciones de emergencia**: levante rápidamente una red temporal cuando se pierda la conectividad

### Los cuatro componentes principales del Soft AP en Linux

| Componente | Función |
|-----------|----------|
| **hostapd** | El demonio central que crea el Access Point — gestiona SSID, autenticación, cifrado |
| **nl80211** | La interfaz estándar del subsistema inalámbrico de Linux — el controlador debe admitir este framework para funcionar con hostapd |
| **dnsmasq** | Servidor DHCP que asigna automáticamente direcciones IP a los clientes conectados |
| **iptables / nftables** | Traducción de Direcciones de Red (NAT) — permite a los clientes conectados compartir la red ascendente |

### Concepto clave: Modo Master

**El Modo Master** (también llamado Modo AP o Modo Infraestructura) es una capacidad a nivel de controlador. Si el controlador no admite el Modo Master, hostapd simplemente no puede iniciarse — sin importar cuán perfecta sea su configuración.

Verifique el soporte del modo AP con:

```bash
iw list | grep -A 10 "Supported interface modes"
```

Si la salida incluye `* AP`, el controlador del adaptador admite Soft AP. Si no, ese adaptador no sirve para este propósito.

### 💡 Controladores In-kernel vs Out-of-kernel

Este es el concepto **más importante** al elegir un adaptador Soft AP:

| Tipo | Descripción | Impacto en Soft AP |
|------|-------------|-------------------|
| **Controlador In-kernel** | Integrado en el árbol fuente oficial de Linux; se carga automáticamente al arrancar — sin instalación manual | ✅ Estable a largo plazo; sobrevive a las actualizaciones del kernel |
| **Controlador Out-of-kernel** | Debe descargarse de GitHub y compilarse manualmente; puede necesitar recompilación después de cada actualización del kernel | ⚠️ Puede romperse tras cualquier actualización del kernel |

**Para una estabilidad a largo plazo del Soft AP, los controladores in-kernel son muy superiores a los out-of-kernel.**

---

## 2. Línea de productos ALFA y resumen de chipsets {#product-lineup}

Esta es la línea actual de productos ALFA vendidos por Yopitek, con sus chipsets y una evaluación preliminar de Soft AP:

| Modelo | Chipset | Tipo de controlador | Estándar WiFi | Calificación Soft AP |
|-------|---------|-------------|---------------|----------------|
| **AWUS036ACM** | MediaTek MT7612U | In-kernel (kernel 4.19+) | WiFi 5 AC1200 Doble banda | ✅ Soporte completo |
| AWUS036ACH | Realtek RTL8812AU | Out-of-kernel (in-kernel desde 6.13+) | WiFi 5 AC1200 Doble banda | ⚠️ Condicional |
| AWUS036AXML | MediaTek MT7921AUN | In-kernel (5.18+, modo AP 5.19+) | WiFi 6E AX3000 Triple banda | ⚠️ Parcial |
| AWUS036AXM | MediaTek MT7921AUN | In-kernel (igual que el anterior) | WiFi 6E AX3000 Triple banda | ⚠️ Parcial |
| AWUS036AX | Realtek RTL8832BU | Integrado rtw89_8852bu (kernel 6.17+); kernels anteriores: controlador DKMS de la comunidad | WiFi 6 AX1800 Doble banda | ✅ Funciona (kernel 6.17+) |
| AWUS036AXER | Realtek RTL8832BU | Integrado rtw89_8852bu (kernel 6.17+; igual que AX) | WiFi 6 AX1800 Doble banda | ✅ Funciona (kernel 6.17+) |

> **Nota**: el AWUS036ACHM (MT7610U) se ha descontinuado y ya no figura en la página de productos de Yopitek. Este artículo solo cubre los productos disponibles actualmente.

---

## 3. AWUS036ACM (MT7612U) — ⭐ Recomendación principal {#acm}

### Estado Soft AP: ✅ Soporte completo

El MT7612U es el chipset Soft AP más estable de la línea actual de ALFA. Su controlador `mt76x2u` forma parte del kernel oficial de Linux desde 2018 (kernel 4.19), lo que significa que funciona de inmediato en cualquier sistema razonablemente actual — **sin `git clone`, sin `dkms`, sin recompilar después de actualizaciones del kernel.**

### Ventajas clave

- **Soporte dual WPA2 + WPA3**: el controlador in-kernel de MediaTek admite WPA3 SAE de forma nativa — una ventaja que los controladores de Realtek no pueden igualar
- **Soporte de Interfaz Virtual VIF**: ejecute los modos AP + Managed + Monitor simultáneamente en un solo adaptador — sin necesidad de comprar una segunda tarjeta. Comparta su red mientras monitoriza el espectro inalámbrico al mismo tiempo
- **Consumo ultra bajo**: máximo de ~400mA, perfecto para Raspberry Pi (el subsistema USB del Pi 4 solo proporciona 1200mA en total)
- **Multiplataforma**: ampliamente verificado en Kali Linux 2022.x–2025.x, Ubuntu 22.04/24.04, Debian 11/12 y Raspberry Pi OS (Pi 3B+, 4, 5)

### Configuración correcta de hostapd (MT7612U)

Los siguientes flags de capacidad se han verificado durante años de pruebas comunitarias (morrownr/USB-WiFi). **Deben coincidir exactamente con las capacidades reales de hardware del MT7612U:**

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACM (MT7612U)
interface=wlan1
driver=nl80211
ssid=YourNetworkName
hw_mode=a                     # 5GHz; use g for 2.4GHz
channel=36                    # UNII-1, non-DFS, safest choice
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# MT7612U correct HT / VHT capabilities
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42    # Center frequency index for channel 36

# Security: WPA2 + WPA3 mixed mode
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK SAE       # WPA2 + WPA3 dual support
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=YourPassword
```

### ⚠️ Error más común

Si `ht_capab` incluye flags de capacidad que el MT7612U no admite realmente (sobre todo al forzar ciertas configuraciones HT40 sobre USB 2.0), hostapd fallará silenciosamente con mensajes de error muy poco útiles. **Use solo la combinación de flags verificada arriba — no copie configuraciones de otros chipsets como el RTL8812AU.** (Fuente: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2))

### Reseñas de la comunidad

> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. I have tested the Alfa AWUS036ACM with many different computer systems and Linux distros. In my opinion, it is an outstanding USB WiFi adapter."
> *(Traducción: «Alfa AWUS036ACM funciona muy bien con el hardware de Raspberry Pi. He probado el Alfa AWUS036ACM con muchos sistemas informáticos y distribuciones Linux diferentes. En mi opinión, es un adaptador USB WiFi excepcional.»)*
> — **morrownr**, mantenedor de la base de conocimiento comunitaria más autorizada sobre Linux USB WiFi en GitHub

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> *(Traducción: «Este adaptador hace modo monitor e inyección de paquetes a la perfección. Muy estable en Linux con kernels nativos, sin necesidad de compilar controladores externos.»)*
> — reseña de un usuario de eBay

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> *(Traducción: «El ACM es un poco más versátil y más fácil de configurar en modo AP.»)*
> — hilo de discusión del GitHub issue #2

---

## 4. AWUS036ACH (RTL8812AU) — Funciona, pero con concesiones {#ach}

### Estado Soft AP: ⚠️ Soporte condicional

El RTL8812AU es el chipset de pruebas de penetración más emblemático de ALFA y un favorito de larga data de la comunidad Kali Linux. Su función Soft AP sí funciona — crear un hotspot básico no presenta problemas —, pero la arquitectura de controlador out-of-kernel de Realtek impone varias limitaciones persistentes:

### Limitaciones conocidas

1. **Sin soporte WPA3**: aunque el controlador del RTL8812AU afirma admitir WPA3, varios usuarios han confirmado que en realidad no funciona. **Solo WPA2-PSK.**
2. **Sin soporte VIF**: no puede ejecutar los modos AP + Monitor simultáneamente en la misma tarjeta. Si necesita AP y monitorización, deberá usar dos adaptadores distintos.
3. **Problemas del controlador en Kali Linux 2025.x**: el controlador aircrack-ng/rtl8812au más reciente presenta problemas de compatibilidad en el Kali más nuevo — es necesario volver a un commit antiguo concreto (`63cf0b4`). La situación podría mejorar con el controlador in-kernel rtw88 del kernel 6.13+.
4. **Alto consumo de energía**: máximo de ~800mA — en Raspberry Pi con varios dispositivos USB conectados, esto puede causar inestabilidad del sistema. Use un hub USB con alimentación propia.

### Configuración de hostapd (RTL8812AU)

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACH (RTL8812AU)
# NOTE: Completely different capabilities from MT7612U!
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]

# Security: WPA2 only, do NOT add WPA3
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
```

### Instalación del controlador (Kali Linux / Ubuntu / Debian)

```bash
sudo apt update && sudo apt install -y dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
# Kali 2025.x requires the older commit
git checkout 63cf0b4
make && sudo make install
sudo modprobe 88XXau
```

### Reseñas de la comunidad

> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine."
> *(Traducción: «Puedo poner un RTL8812AU (AWUS036AC) en su lugar y usar 'sudo service hostapd restart && sudo service dnsmasq restart', y funcionó perfectamente.»)*
> — usuario del GitHub issue #2

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> *(Traducción: «Adaptadores basados en RTL8812AU: el modo AP funciona, pero se pierde el soporte de WPA3 y VIF en comparación con MediaTek.»)*
> — notas técnicas de morrownr

### Veredicto para ACH

Si ya tiene un AWUS036ACH, puede servir como Soft AP (la función básica de hotspot funciona). Pero si aún no lo ha comprado y su objetivo principal es Soft AP, **elija el ACM en su lugar.**

---

## 5. AWUS036AXML / AWUS036AXM (MT7921AUN) — Proceda con precaución {#axml}

### Estado Soft AP: ⚠️ Soporte parcial — Problemas conocidos de firmware/controlador

El AWUS036AXML y el AWUS036AXM son los buques insignia tribanda WiFi 6E de ALFA, que cubren 2.4 GHz, 5 GHz y la nueva banda de 6 GHz (los 6 GHz se probaron localmente en el AXML; el AXM admite 6E según su especificación, pero los 6 GHz no se probaron). Su controlador in-kernel `mt7921u` está en el kernel desde la versión 5.18, y el soporte del modo AP se añadió oficialmente en la 5.19. Sin embargo, el chip MT7921AUN también integra Bluetooth 5.2 — lo que se convirtió en el principal quebradero de cabeza de la comunidad en 2024–2025.

### Hitos de versión del kernel para el modo AP

| Modo | Kernel mínimo |
|------|---------------|
| Managed (WiFi normal) | 5.18+ |
| **Modo AP (Soft AP)** | **5.19+** |
| AP/VLAN | 5.19+ |
| P2P-GO (Wi-Fi Direct AP) | 6.4+ |

### Problemas conocidos y soluciones

#### Problema 1: Interferencia Bluetooth causando fallos WiFi

En kernels 6.6+, los cambios en el subsistema BT provocan fallos esporádicos de WiFi con mt7921u. La reproducibilidad varía según el entorno del sistema. **La solución alternativa más eficaz es desactivar el controlador btusb:**

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

#### Problema 2: Firmware desactualizado

Si el firmware de MediaTek del sistema es demasiado antiguo, es posible que el adaptador no se reconozca correctamente. Instale un firmware de noviembre de 2024 o posterior:

```bash
# Check current firmware version
dmesg | grep "WM Firmware"
# Should show: Build Time: 20241106151045 or newer

# If outdated, download from kernel.org
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek/
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek/
sudo reboot
```

#### Problema 3: requisitos de versión de hostapd

Algunos usuarios indican que necesitan compilar hostapd desde git para tener soporte completo del modo AP de WiFi 6. Las versiones del gestor de paquetes del sistema pueden estar incompletas.

#### Problema 4: anomalía en la visualización de la potencia de transmisión (Tx Power) en modo AP

`iw` muestra solo 3 dBm sin posibilidad de ajuste, pero el chip en realidad tiene un amplificador interno — es un problema de visualización del controlador del kernel, no una limitación del hardware.

#### Problema 5: problemas del modo monitor en ciertas versiones del kernel

A diciembre de 2025, el kernel 6.18 y algunas versiones anteriores del controlador mt7921u presentan problemas con el modo monitor.

### Reseña de la comunidad

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> *(Traducción: «Tengo un Alfa AXML funcionando como AP en un host RPi3B con ArchLinux ARM aarch64. Es el mt7921 más estable de mi colección. Eso sí, uso hostapd compilado desde git.»)*
> — **fhteagle**, [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

### Veredicto para AXML/AXM

Elija estos modelos si necesita la banda de 6 GHz de WiFi 6E y está dispuesto a ajustar la configuración de vez en cuando. **Para entornos de producción que requieren una estabilidad de Soft AP a toda prueba, elija el ACM en su lugar.**

---

## 6. AWUS036AX / AWUS036AXER (RTL8832BU) — Funciona para Soft AP con kernel 6.17 o superior {#ax}

### Estado Soft AP: ✅ Funciona con kernel 6.17 o superior (los kernels anteriores necesitan el controlador DKMS de la comunidad)

En nuestras pruebas en un ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17) con el controlador integrado `rtw89_8852bu`, el AWUS036AX y el AWUS036AXER (mismo chip, mismo controlador) se comportan igual, y el Soft AP funciona tanto en 2.4 GHz como en 5 GHz.

**Resultados de las pruebas (kernel 6.17):**

1. **Modo AP**: funcionan tanto 2.4 GHz (802.11n) como 5 GHz (VHT 80 MHz)
2. **VIF (STA + AP)**: funciona — una conexión de cliente y una interfaz AP se ejecutan en paralelo en el mismo canal
3. **AP WPA3-SAE**: funciona en 2.4 GHz (iPhone 15 Pro conectado, MFP activado; 5 GHz no probado)
4. **Monitor / inyección**: recepción monitor fuerte en 2.4 y 5 GHz; inyección en 2.4 GHz AX 96% / AXER 73%, 5 GHz utilizable; se logró una captura de handshake WPA de extremo a extremo
5. **No compatible**: IBSS, Mesh, active monitor

**Advertencias:**

- **La versión del kernel es un requisito**: `rtw89_8852bu` está en el kernel desde la 6.17. Los kernels anteriores necesitan el controlador DKMS de la comunidad (rtl8852bu), con el que el modo monitor puede estar limitado y VIF no es compatible.
- **Modo USB**: algunas unidades pueden enumerarse en modo CD-ROM (`0bda:1a2b`) y requerir `usb_modeswitch -v 0bda -p 1a2b -K`; nuestra unidad de prueba se enumeró directamente como adaptador WLAN.
- **Casos comunitarios**: hay menos reportes de Soft AP para este chipset que para MT7612U y RTL8812AU.

> Resultado de las pruebas de Yopitek (ASUS GX10, kernel 6.17): con el controlador integrado, el AWUS036AX / AWUS036AXER tienen una recepción monitor fuerte e inyección de paquetes funcional, por lo que también sirven para pruebas de penetración. El soporte limitado de monitor solo se aplica a kernels anteriores con el controlador DKMS de la comunidad.
>
> Actualización: con el kernel stock 6.16 o posterior (probado en 6.17), el AWUS036AXML funciona en modo monitor, AP, WPA3 y VIF, pero la prueba de inyección de paquetes falló (aireplay-ng --test: Found 0 APs / No Answer). La causa es una regresión de mac80211 chanctx, no el propio chip. Si necesita inyección, use AWUS036ACH, EACS, ACS o AX.

---

## 7. Matriz de compatibilidad de plataformas {#compat-matrix}

### AWUS036ACM (MT7612U)

| Plataforma | Soft AP | Notas |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ✅ | Controlador in-kernel, plug-and-play, kernel 5.x / 6.x |
| Ubuntu 22.04 / 24.04 | ✅ | In-kernel, sin configuración, use LTS |
| Debian 11 / 12 | ✅ | In-kernel, estable |
| Raspberry Pi 4 (RPi OS) | ✅ | Menor consumo (400mA), verificación a largo plazo de morrownr. Preferible el puerto USB 3.0 del Pi 4 |
| Raspberry Pi 5 (RPi OS) | ✅ | Mismo controlador que el Pi 4, estable |

### AWUS036ACH (RTL8812AU)

| Plataforma | Soft AP | Notas |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ⚠️ | Requiere controlador externo; 2025.x necesita el commit `63cf0b4`. El rtw88 del kernel 6.13+ puede mejorarlo |
| Ubuntu 22.04 / 24.04 | ⚠️ | Puede requerir instalar manualmente el controlador rtw88 o aircrack-ng |
| Debian 11 / 12 | ⚠️ | Igual que el anterior |
| Raspberry Pi 4 | ⚠️ | Funciona, pero con alto consumo (800mA); use un hub USB con alimentación propia |
| Raspberry Pi 5 | ⚠️ | Igual; las diferencias del controlador USB del Pi 5 pueden afectar al comportamiento |

### AWUS036AXML / AWUS036AXM (MT7921AUN)

| Plataforma | Soft AP | Notas |
|----------|---------|-------|
| Kali Linux 2022.x (kernel 5.18+) | ✅ | Desactive btusb y actualice el firmware |
| Kali Linux 2024.x / 2025.x | ⚠️ | Conflicto BT/WiFi en kernel 6.11+, inestable |
| Ubuntu 24.04 (kernel 6.8+) | ⚠️ | Problemas reportados a finales de 2024 |
| Ubuntu 25.04 / CachyOS (kernel 6.14+) | ✅ | Plug-and-play, mejora notable con el kernel nuevo |
| Debian 12 | ⚠️ | Depende de la versión del kernel |
| Raspberry Pi 4 / 5 | ⚠️ | Hay casos de éxito, pero verifique el firmware y desactive BT |

### AWUS036AX / AWUS036AXER (RTL8832BU)

| Plataforma | Soft AP | Notas |
|----------|---------|-------|
| Kali Linux | ✅ | rtw89_8852bu integrado desde el kernel 6.17; los kernels anteriores necesitan el controlador DKMS de la comunidad |
| Ubuntu / Debian | ✅ | Ubuntu 24.04 necesita el kernel HWE 6.17+ (GA 6.8 / HWE 6.14 necesitan el controlador DKMS de la comunidad); Debian necesita kernel 6.17+ |
| Raspberry Pi 4 / 5 | ⚠️ | No probado en Pi; los kernels anteriores a 6.17 necesitan el controlador DKMS de la comunidad |

---

## 8. Guía completa de configuración de Soft AP (AWUS036ACM) {#setup-guide}

A continuación se presenta una guía completa paso a paso para configurar un Soft AP de 5GHz con el AWUS036ACM en Raspberry Pi 4.

### Paso 1: Verificar la detección del adaptador y el controlador

```bash
# Confirm the adapter is detected
lsusb | grep MediaTek
# Expected: Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U

# Check driver loaded
dmesg | grep mt76
# Expected: mt76x2u 1-1.4:1.0 wlx00c0ca9821a5: renamed from wlan0

# Confirm AP mode support
iw list | grep -A 10 "Supported interface modes"
# Check that output includes "* AP"
```

### Paso 2: Instalar paquetes requeridos

```bash
sudo apt update
sudo apt install -y hostapd dnsmasq iptables
```

### Paso 3: Configurar hostapd

Cree `/etc/hostapd/hostapd.conf`:

```ini
interface=wlan0
driver=nl80211
ssid=Yupitek_AP
hw_mode=a                       # a=5GHz, g=2.4GHz
channel=36                      # UNII-1, non-DFS, safest choice
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# HT/VHT settings (MT7612U specific)
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42

# WPA2 + WPA3 mixed mode
wpa=2
wpa_passphrase=MySecurePassword123
wpa_key_mgmt=WPA-PSK SAE
wpa_pairwise=CCMP
rsn_pairwise=CCMP

auth_algs=1
macaddr_acl=0
ignore_broadcast_ssid=0
```

### Paso 4: Configurar dnsmasq (DHCP)

Cree `/etc/dnsmasq.conf`:

```ini
interface=wlan0
dhcp-range=192.168.10.2,192.168.10.100,255.255.255.0,12h
dhcp-option=3,192.168.10.1
dhcp-option=6,8.8.8.8,8.8.4.4
```

### Paso 5: Establecer IP estática y NAT

```bash
# Assign static IP to wlan0
sudo ip addr add 192.168.10.1/24 dev wlan0

# Enable IP forwarding
sudo sysctl net.ipv4.ip_forward=1

# Configure NAT (assuming eth0 is the upstream interface)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Persist iptables rules
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```

### Paso 6: Iniciar servicios

```bash
sudo systemctl unmask hostapd
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# Check service status
sudo systemctl status hostapd
sudo systemctl status dnsmasq

# Enable auto-start on boot
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```

Una vez completado, busque WiFi en su teléfono o portátil — debería ver el SSID `Yupitek_AP`.

---

## 9. Solución de problemas comunes {#troubleshooting}

### P1: hostapd falla inmediatamente al iniciar

**Síntoma**: `sudo systemctl status hostapd` muestra `exited` o `failed`

**Causa probable**: `hostapd.conf` contiene flags de capacidad que el chipset no admite

**Solución**: elimine los flags sobrantes. Para el MT7612U (ACM), lo más seguro es usar la configuración verificada de la Sección 3. **No copie ht_capab de otros chipsets.**

---

### P2: Los clientes se conectan pero no pueden acceder a Internet

**Síntoma**: WiFi conectado, IP obtenida, pero `ping 8.8.8.8` no obtiene respuesta

**Lista de comprobación**:

```bash
# 1. Check IP forwarding enabled
cat /proc/sys/net/ipv4/ip_forward
# Should output: 1

# 2. Check NAT rules exist
sudo iptables -t nat -L POSTROUTING -v
# Should see MASQUERADE rule

# 3. Confirm upstream interface is working
ping -I eth0 8.8.8.8
```

---

### P3: AP de 5GHz no visible o inestable

**Causas posibles**:

1. **Uso de canales DFS (100–144)**: MT7612U / MT7610U no admiten DFS — use canales UNII-1 (36–48)
2. **Potencia de transmisión insuficiente**: asegúrese de que las antenas estén bien apretadas en los conectores RP-SMA
3. **Alimentación USB insuficiente** (Raspberry Pi): use la fuente de alimentación oficial de 5A o un hub USB con alimentación propia

---

### P4: hostapd se reinicia constantemente en Raspberry Pi

**Síntoma**: `dmesg` muestra mensajes frecuentes de reinicio de USB

**Causa probable**: alimentación insuficiente del puerto USB (sobre todo con el chipset de alto consumo del AWUS036ACH, máx. 800mA)

**Solución**:
- Use la fuente de alimentación oficial de 5A para Pi
- Use un hub USB con alimentación propia
- Conecte el adaptador a un puerto USB 3.0 (solo Pi 4)

---

### P5: El WiFi de AWUS036AXML/AXM se cae repentinamente o no inicia

**Causa probable**: el subsistema Bluetooth interfiere con el WiFi (el MT7921AUN integra BT 5.2)

**Solución**: desactive permanentemente el controlador Bluetooth

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## 10. Análisis técnico: VIF, WPA3, Canales DFS {#technical}

### VIF (Interfaz Virtual): Una tarjeta, múltiples roles

VIF (Virtual Interface) permite que un único adaptador físico funcione con varias interfaces lógicas a la vez. Por ejemplo: una interfaz se conecta al router ascendente (modo managed) mientras otra actúa como AP (modo master) para otros dispositivos.

Tres escenarios habituales:

| Escenario | ¿Requiere VIF? | Mejor adaptador |
|----------|--------------|--------------|
| Enrutamiento NAT básico (eth0 ascendente + wlan AP) | ❌ No | Cualquier adaptador compatible con AP |
| Puente inalámbrico (recepción WiFi + WiFi AP simultáneamente) | ✅ Sí | ACM (MT7612U) |
| Monitor + AP simultáneamente (investigación de seguridad / Rogue AP) | ✅ Sí | ACM (MT7612U) |

**Ejemplo práctico de VIF (MT7612U):**

```bash
# Create an additional AP virtual interface alongside existing wlan1
sudo iw phy phy1 interface add ap0 type __ap
sudo ip link set ap0 up
# Now wlan1 can connect upstream while ap0 runs hostapd
```

Solo los controladores in-kernel de MediaTek (mt76x2u, mt7921u) admiten VIF por completo. Los controladores out-of-kernel de Realtek carecen básicamente de esta capacidad — si necesita AP + Monitor simultáneamente, deberá usar dos adaptadores distintos.

---

### Comparación de soporte WPA3

| Chipset | Modelo correspondiente | WPA2 | WPA3 |
|---------|-------------------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ Soporte nativo de SAE |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ Soporte nativo de SAE |
| RTL8812AU | AWUS036ACH | ✅ | ❌ Afirma soportarlo, pero no funciona |
| RTL8832BU | AWUS036AX / AXER | ✅ | ✅ Probado en el kernel 6.17 (`sae_pwe=0`, MFP activado) |

---

### Selección de canales Soft AP 5GHz: Evitar DFS

Los canales DFS (Dynamic Frequency Selection) (ch100–ch140) requieren detección de radar a nivel de kernel. El MT7612U y chipsets similares no admiten DFS. Para el modo AP en 5GHz, elija:

| Banda | Canales recomendados | Motivo |
|------|---------------------|--------|
| **UNII-1** | **36, 40, 44, 48** | Compatibles con todos los chipsets; la opción más segura |
| UNII-2 (DFS) | 52–144 | Mayormente no compatibles; no recomendado |
| UNII-3 | 149–165 | Soporte parcial (según la región) |

---

## 11. Casos reales de la comunidad {#real-cases}

### Caso 1: RPi4B + AWUS036ACM = AP doméstico de 5GHz estable a largo plazo

**Fuente**: base de conocimiento morrownr/7612u en GitHub
**Escenario**: morrownr usa desde hace tiempo un RPi4B + AWUS036ACM como AP doméstico de 5GHz, combinado con el 2.4GHz integrado del Pi para ofrecer servicio de doble banda
**Resultado**: funcionamiento estable a largo plazo, sin necesidad de reinicios, calificado como "excepcional"
**Configuración**: hostapd + dnsmasq + iptables NAT

### Caso 2: RPi3B+ + ACM — fallo inicial, solucionado

**Fuente**: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
**Problema**: hostapd fallaba al ejecutarse sobre USB 2.0 en RPi3B+
**Causa raíz**: `ht_capab` contenía flags HT40 no admitidos dentro de los límites de ancho de banda de USB 2.0
**Solución**: se eliminaron los flags sobrantes; se inició correctamente en Kali Linux

### Caso 3: Pi PwnBox + AWUS036ACH = Rogue AP de Red Team

**Fuente**: GitHub koutto/pi-pwnbox-rogueap
**Escenario**: plataforma Rogue AP en RPi3B+: un RTL8812AU (AWUS036ACH) para el AP y otro RT3070 (AWUS036NEH) para ataques de inyección de paquetes
**Hallazgo clave**: como el RTL8812AU carece de VIF, se necesitaron dos adaptadores distintos (a diferencia del ACM, que gestiona ambas funciones con una sola tarjeta)

### Caso 4: AP estable con AWUS036AXML en RPi3B con ArchLinux ARM

**Fuente**: [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
**Escenario**: un usuario ejecutó con éxito el AWUS036AXML en modo AP en un RPi3B con ArchLinux aarch64
**Cita**: "Es el mt7921 más estable de mi colección."
**Requisitos clave**: hostapd compilado desde git + btusb desactivado

### Caso 5: AP a velocidad completa con AWUS036ACHM (MT7610U, descontinuado) en Pi4

**Fuente**: [GitHub Discussion #31](https://github.com/morrownr/USB-WiFi/discussions/31)
**Problema**: la configuración inicial solo alcanzaba 65 Mbps de velocidad de enlace, muy por debajo de la velocidad completa de AC en 5GHz
**Solución**: se añadieron los valores correctos de `vht_oper_chwidth=1` y `vht_oper_centr_freq_seg0_idx`; se alcanzó una velocidad de enlace de 433 Mbps
**Relevancia para el ACM**: la misma configuración de parámetros VHT es igualmente crucial para el MT7612U (ACM)

---

{{< faq >}}

## 12. Recomendaciones de compra y veredicto final {#recommendations}

### Matriz de decisión rápida

| Calificación | Modelo | Ideal para | En una frase |
|--------|-------|----------|-----------|
| 🥇 **Mejor opción** | **AWUS036ACM** | Todos, especialmente principiantes en Soft AP | Estable en todas las plataformas, sin complicaciones |
| 🥈 Utilizable | AWUS036ACH | Usuarios que ya poseen este modelo | Necesita controlador, sin WPA3 |
| 🥉 Avanzado | AWUS036AXML | Usuarios que necesitan WiFi 6E dispuestos a ajustar | Ventaja 6GHz, correcciones manuales necesarias |
| ✅ Funciona con kernel 6.17+ | AWUS036AX / AXER | AP Wi-Fi 6; monitor e inyección también utilizables | Controlador integrado; AP 2.4 / 5 GHz y VIF probados, WPA3 probado en 2.4 GHz |

### 🎯 Guía de decisión

- **¿Necesita un Soft AP estable en Kali / Ubuntu / Debian / Raspberry Pi 4 o 5?**
  → Elija el **AWUS036ACM**, sin discusión.

- **¿Ya tiene un AWUS036ACH y quiere probar Soft AP?**
  → Funciona, pero solo con WPA2, y tendrá que instalar el controlador. Si acepta esas limitaciones, adelante.

- **¿Necesita WiFi 6E (banda de 6 GHz) y está dispuesto a configurar?**
  → AWUS036AXML — recuerde desactivar el controlador BT y verificar que el kernel sea ≥ 6.6 LTS.

- **¿El objetivo principal es Soft AP y no las pruebas de penetración?**
  → El AWUS036ACM es la única opción con amplia verificación comunitaria en todas las plataformas.

---

### Conclusión

El factor central para construir un Soft AP no es la velocidad WiFi ni el número de antenas — **es el soporte del modo AP del controlador del chipset.**

Entre todos los productos ALFA que investigamos, el **AWUS036ACM (MT7612U)** es el único adaptador que satisface simultáneamente: controlador in-kernel, WPA3 nativo, interfaces virtuales VIF, bajo consumo y estabilidad multiplataforma. Es el estándar de referencia para Soft AP.

El AWUS036ACH (RTL8812AU) funciona si acepta sus limitaciones. El AWUS036AXML/AXM (MT7921AUN) tiene un gran potencial, pero la madurez del controlador todavía está en desarrollo. El AWUS036AX/AXER (RTL8832BU) funciona bien con kernel 6.17 o superior gracias al controlador integrado (AP, VIF y WPA3 probados); los kernels anteriores necesitan el controlador DKMS de la comunidad.

**Si es la primera vez que configura un Soft AP en Raspberry Pi o Kali Linux — elija ACM. No se arrepentirá.**

---

### Enlaces de compra

- [AWUS036ACM — Mejor opción Soft AP](/es/products/alfa/awus036acm/)
- [AWUS036ACH — Adaptador clásico de pentesting](/es/products/alfa/awus036ach/)
- [AWUS036AXML — Flagship tribanda WiFi 6E](/es/products/alfa/awus036axml/)
- [Línea completa de productos ALFA Network](/es/products/alfa/)

### Lecturas adicionales

- [AWUS036ACH vs AWUS036ACM: comparación completa de controladores de chipset](/es/blog/awus036ach-vs-awus036acm/)
- [AWUS036ACM: IBSS y Mesh en Raspberry Pi](/es/blog/)
- [morrownr/USB-WiFi — La base de conocimiento de referencia sobre Linux USB WiFi](https://github.com/morrownr/USB-WiFi) (más de 4,100 estrellas)
- [morrownr/7612u — Referencia del MT7612U (incluye tutorial de Bridged AP en RPi4B)](https://github.com/morrownr/7612u)
- [DeepWiki — Base de conocimiento de morrownr/USB-WiFi con curación automática](https://deepwiki.com/morrownr/USB-WiFi)

---

### 📚 Fuentes de datos

Este artículo recopila información de:
- Base de conocimiento **morrownr/USB-WiFi** en GitHub (más de 4,100 estrellas) con registros completos de iw_list
- **morrownr/7612u** — tutorial de Bridged AP con MT7612U en RPi4B
- **Issue tracker de GitHub** — issue #2 (configuración AP del ACM), #476 (pruebas AP del AXML), Discussion #31 (AP a velocidad completa del ACHM)
- **koutto/pi-pwnbox-rogueap** — caso de implementación de RogueAP con adaptador Alfa
- Páginas de soporte Linux del distribuidor **Rokland**
- Análisis técnicos de **Lab401** e informes de las mejores opciones de pentesting de 2025
- **Foro oficial de Raspberry Pi** — discusiones sobre compatibilidad de USB WiFi con Pi 4/5
- **Blog de Yopitek** — guía de instalación del ACM en China, reseña del AXML WiFi 6E, mejores adaptadores para Kali Linux 2026

---

> **Etiquetas**: #ALFANetwork #SoftAP #WiFiHotspot #hostapd #KaliLinux #Ubuntu #Debian #RaspberryPi #AWUS036ACM #AWUS036ACH #AWUS036AXML #MT7612U #RTL8812AU #MT7921AUN #Yopitek
>
> **Autor**: Yopitek Ltd — Distribuidor Autorizado ALFA Network Taiwan
>
> **Aviso legal**: Datos de investigación actualizados a mayo de 2026. Los kernels de Linux y las distribuciones siguen evolucionando; el soporte de controladores puede cambiar con nuevas versiones. Verifique la versión del kernel y la compatibilidad del controlador en la plataforma de destino antes del despliegue.
>
> **Soporte técnico**: para problemas de configuración de Soft AP, contacte con el soporte técnico de Yopitek Taiwán. Consultas sobre productos: [yupitek.com](https://yupitek.com/es/).

## Referencias

1. [Repositorio de conocimiento morrownr/USB-WiFi en GitHub](https://github.com/morrownr/USB-WiFi)
2. [Documentación oficial de hostapd](https://w1.fi/cgit/hostap/)
3. [Controlador mt76 de Linux Wireless](https://wireless.wiki.kernel.org/en/users/Drivers/mt76)
4. [Documentación oficial de Raspberry Pi](https://www.raspberrypi.com/documentation/)
5. [Documentación oficial de Kali Linux](https://www.kali.org/docs/)
