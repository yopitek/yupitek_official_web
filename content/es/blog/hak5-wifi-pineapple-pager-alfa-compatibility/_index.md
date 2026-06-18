---
title: "HAK5 WiFi Pineapple Pager × ALFA Network: Guía de compatibilidad de tarjetas inalámbricas USB externas"
description: "Evaluación detallada de compatibilidad y guía de configuración paso a paso para conectar tarjetas inalámbricas USB de ALFA Network al HAK5 WiFi Pineapple Pager bajo OpenWrt. Conozca las limitaciones de alimentación USB 2.0, compilación cruzada en arquitectura MIPS y controladores."
date: 2026-06-19
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi Pineapple Pager", "ALFA Network", "AWUS036ACM", "AWUS036ACH", "compatibility", "wireless-security"]
featureimage: "/images/blog/hak5-wifi-pineapple-pager-alfa-compatibility.webp"
---

# HAK5 WiFi Pineapple Pager × ALFA Network: Guía de compatibilidad de tarjetas inalámbricas USB externas

La auditoría de seguridad inalámbrica exige alta precisión, versatilidad y el hardware adecuado. El **HAK5 WiFi Pineapple Pager** ha captado la atención de los profesionales de la seguridad informática como una herramienta de auditoría ultraportátil y de tamaño de bolsillo, impulsada por el potente motor **PineAP v8**.

Sin embargo, para maximizar el rango de auditoría, realizar operaciones simultáneas en doble banda (2.4 GHz y 5 GHz) o llevar a cabo un monitoreo pasivo multicanal sin interrumpir las radios internas de la Pineapple, los expertos en seguridad a menudo se preguntan: **¿Puedo conectar un adaptador inalámbrico externo de ALFA Network al HAK5 Pager?**

La respuesta corta es **sí, pero con advertencias críticas de hardware y software**.

En esta guía detallada, analizaremos las limitaciones técnicas (como la arquitectura de la CPU y los límites de alimentación de los puertos USB), evaluaremos la compatibilidad de la línea actual de adaptadores de ALFA Network y le proporcionaremos instrucciones paso a paso para la instalación de controladores y la resolución de problemas mediante la interfaz de línea de comandos (CLI).

---

## 1. Limitaciones técnicas: lo que usted debe saber

Antes de conectar cualquier adaptador USB de alta potencia al HAK5 Pager, usted debe comprender dos barreras principales: la arquitectura de la CPU y los límites de alimentación del puerto USB.

### 1.1 Arquitectura de la CPU: la restricción MIPS
A diferencia de una computadora estándar con Kali Linux que funciona con arquitectura x86_64, o de una Raspberry Pi basada en ARM, el HAK5 Pager está construido sobre el chip **MediaTek MT7628AN SoC** (un núcleo **MIPS32r2, Little-Endian**, compilado bajo la plataforma `mipsel_24kc` en OpenWrt).

> [!IMPORTANT]
> Dado que Pager OS está basado en **OpenWrt (versión 24.10.1, Kernel 6.6.86)**, **no es compatible con DKMS** (Soporte dinámico de módulos de kernel). Usted no puede compilar código fuente de controladores fuera del kernel directamente en el Pager porque carece de herramientas de desarrollo como GCC y Make. Cualquier controlador no nativo debe compilarse de forma cruzada en una máquina externa x86_64 Linux utilizando el SDK de OpenWrt.

### 1.2 Presupuesto de alimentación USB 2.0: la restricción de voltaje
El HAK5 Pager cuenta con un único puerto USB 2.0 Host. De acuerdo con las especificaciones oficiales de USB 2.0, un puerto estándar puede suministrar una corriente máxima de **500 mA a 5V (2.5W)**.

Los adaptadores inalámbricos de alta potencia como el ALFA AWUS036ACH (RTL8812AU) o el AWUS036AXML (MT7921AUN) requieren hasta **720 mA (3.6W)** de energía bajo condiciones de transmisión intensa (como inyección de paquetes o escaneos de tráfico densos).

> [!WARNING]
> Conectar un adaptador ALFA de alta potencia directamente al puerto USB del Pager provocará una caída de voltaje. Esto causará **reinicios del dispositivo, pánicos de kernel (Kernel Panic) o desconexiones del adaptador**. Para utilizar estos adaptadores de manera estable, usted **debe** conectar la tarjeta ALFA a través de un **concentrador (Hub) USB con alimentación externa (mínimo 5V/2A)**.

---

## 2. Matriz de compatibilidad de adaptadores ALFA

La siguiente tabla evalúa la compatibilidad de los adaptadores USB actuales de ALFA Network con el HAK5 Pager que ejecuta Pager OS (Kernel 6.6):

| Modelo ALFA | Chipset | Bandas soportadas | Consumo USB | Estado en Kernel 6.6 | Método de instalación | Soporte de Monitor e Inyección | Veredicto y recomendación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AWUS036ACM** | MediaTek **MT7612U** | 2.4 GHz / 5 GHz | ~600 mA (Requiere Hub) | **Integrado en Kernel (Nativo)** | Instalación vía `opkg` | ✅ Sí / ✅ Sí | 🏆 **Estándar de oro / La mejor opción** |
| **AWUS036ACH** | Realtek **RTL8812AU** | 2.4 GHz / 5 GHz | ~720 mA (Requiere Hub con energía) | Fuera del Kernel | Compilación cruzada con SDK | ✅ Sí / ✅ Sí | ⭐⭐ **Solo usuarios avanzados** (Existe bug wiphy en MIPS) |
| **AWUS036AXML** | MediaTek **MT7921AUN** | 2.4 / 5 / 6 GHz (Wi-Fi 6E) | ~720 mA (Requiere Hub con energía) | **Integrado en Kernel (Nativo)** | Instalación vía `opkg` + firmware manual | ✅ Sí / ✅ Sí | ⭐⭐⭐ **Gran potencial**, pero alto consumo |
| **AWUS036ACHM** | MediaTek **MT7610U** | 2.4 GHz / 5 GHz | ~400 mA (Alimentación directa) | Integrado parcialmente | Instalación vía `opkg` | ✅ Sí / ✅ Sí | ⭐⭐⭐ **Excelente opción económica** |
| **AWUS036ACS** | Realtek **RTL8811AU** | 2.4 GHz / 5 GHz | ~500 mA (Al límite) | Fuera del Kernel | Compilación cruzada con SDK | ✅ Sí / ✅ Sí | ⭐⭐ **Intermedio** (Requiere compilar controlador) |
| **AWUS036EACS** | Realtek **RTL8821CU** | 2.4 GHz / 5 GHz | ~500 mA | Fuera del Kernel | No recomendado | ❌ **No soporta modo monitor** | ❌ **Incompatible / No usar** |

---

## 3. Guía de configuración paso a paso

A continuación se detallan los comandos de CLI para configurar los adaptadores más recomendados.

### 3.1 Escenario A: AWUS036ACM (MT7612U) — Plug & Play (Recomendado)

El **AWUS036ACM** es la mejor opción absoluta para el HAK5 Pager. El conjunto de controladores `mt76` de MediaTek está integrado de forma nativa en el Kernel 6.6 de Linux, eliminando la necesidad de realizar compilaciones.

#### Paso 1: Conectar el hardware
1. Conecte el Hub USB con alimentación externa al puerto USB del HAK5 Pager.
2. Conecte el AWUS036ACM al Hub.
3. Acceda al Pager a través de SSH:
   ```bash
   ssh root@172.16.42.1
   ```

#### Paso 2: Verificar el reconocimiento del dispositivo
Ejecute el comando `lsusb` para confirmar que el sistema reconoce el chipset de MediaTek:
```bash
lsusb
# Debería mostrar la siguiente línea:
# Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

#### Paso 3: Instalar los módulos del kernel a través de opkg
Actualice el gestor de paquetes e instale las dependencias del controlador de MediaTek USB:
```bash
opkg update
opkg install kmod-mt76x2u kmod-mt76-usb firmware-utils
```

#### Paso 4: Corregir el bug de caída de USB Scatter-Gather en arquitectura MIPS
En los enrutadores OpenWrt basados en MIPS, el controlador `mt76-usb` puede presentar caídas durante la carga del firmware si la función USB Scatter-Gather (USB SG) está activada.

> [!TIP]
> Para garantizar la estabilidad de la conexión y evitar fallas de carga del firmware (error `-110`), usted debe desactivar la función USB Scatter-Gather configurando un parámetro del módulo del kernel.

Cree el archivo `/etc/modules.d/mt76-usb-sg` e introduzca el parámetro de desactivación:
```bash
echo "mt76-usb disable_usb_sg=1" > /etc/modules.d/mt76-usb-sg
```
Reinicie el HAK5 Pager para aplicar los cambios:
```bash
reboot
```

#### Paso 5: Verificar el modo monitor y la inyección de paquetes
Una vez reiniciado el dispositivo, acceda de nuevo por SSH y ejecute:
```bash
iw dev
# Busque la nueva interfaz inalámbrica (por ejemplo, wlan2)
```

Para activar el modo monitor:
```bash
ip link set wlan2 down
iw dev wlan2 set monitor none
ip link set wlan2 up
```
Verifique el estado de la interfaz:
```bash
iw dev wlan2 info
# Debería mostrar: "type monitor"
```

---

### 3.2 Escenario B: AWUS036ACH (RTL8812AU) — Compilación avanzada mediante SDK

El **AWUS036ACH** es una opción de referencia para Kali Linux debido a su alta sensibilidad y potencia, pero no es compatible de forma nativa en OpenWrt Kernel 6.6. Debe compilarse de forma cruzada.

#### Requisitos previos
- Una computadora de desarrollo con Ubuntu 22.04 o Debian 12 (x86_64).
- El SDK de OpenWrt para el objetivo `ramips/mt76x8` (que coincida con el procesador del Pager).

#### Paso 1: Descargar el SDK de OpenWrt en la máquina de desarrollo
En su host de compilación (Ubuntu):
```bash
wget https://downloads.openwrt.org/releases/24.10.1/targets/ramips/mt76x8/openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
tar --zstd -xf openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
cd openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64
```

#### Paso 2: Importar el repositorio del controlador rtl8812au
```bash
git clone https://github.com/aircrack-ng/rtl8812au.git package/kernel/rtl8812au
./scripts/feeds update -a
./scripts/feeds install -a
```

#### Paso 3: Configurar y compilar el módulo del kernel
Abra el menú de configuración del SDK y seleccione el controlador inalámbrico:
```bash
make menuconfig
# Vaya a: Kernel modules -> Wireless Drivers -> Seleccione kmod-rtl8812au
```
Compile el paquete:
```bash
make package/kernel/rtl8812au/compile V=s
```

#### Paso 4: Transferir e instalar el paquete en el Pager
El paquete de instalación `.ipk` compilado se ubicará en el directorio `bin/packages/mipsel_24kc/`. Transfiéralo al Pager:
```bash
scp bin/packages/mipsel_24kc/base/kmod-rtl8812au*.ipk root@172.16.42.1:/tmp/
ssh root@172.16.42.1 "opkg install /tmp/kmod-rtl8812au*.ipk"
```

> [!CAUTION]
> En la arquitectura MIPS, el controlador fuera del kernel `rtl8812au` puede presentar fallas con errores del tipo `wiphy_register`, impidiendo que la interfaz se registre en el sistema. Si experimenta esto, deberá aplicar parches (patches) directamente al código fuente antes de la compilación. Le recomendamos encarecidamente utilizar el adaptador **AWUS036ACM** para evitar estas dificultades.

---

## 4. Capacidades de auditoría inalámbrica desbloqueadas

Al conectar un adaptador ALFA compatible al HAK5 Pager, usted desbloquea múltiples funciones avanzadas de auditoría:

1. **Monitoreo en la banda de 5 GHz**: A pesar de que la radio interna del Pager pueda tener un soporte limitado según su versión, añadir una tarjeta externa de doble banda garantiza la captura de enlaces (handshakes) WPA/WPA2 y solicitudes de sondeo (probe requests) en la banda de 5 GHz.
2. **Radio de ataque dedicada**: Usted puede reservar la radio interna del dispositivo exclusivamente para el engaño de clientes (AP falso / Evil Twin / KARMA) mientras asigna la tarjeta ALFA externa (`wlan2`) a la inyección constante de paquetes de desasociación (Deauth).
3. **Integración profunda con PineAP**: Puede seleccionar el adaptador externo como la interfaz de auditoría principal en la interfaz Web de PineAP o mediante la CLI, lo que acelera el tráfico y respuesta de clientes hasta 100 veces.

---

## 5. Conclusión y veredicto

La integración de una tarjeta inalámbrica de ALFA Network con el HAK5 WiFi Pineapple Pager le permite crear una estación móvil de auditoría discreta y potente. Sin embargo, los detalles de hardware son críticos:

- **Para despliegues rápidos y sin complicaciones**: Adquiera el [ALFA AWUS036ACM](https://yupitek.com/en/products/alfa/awus036acm) por la estabilidad de su controlador MediaTek bajo OpenWrt Kernel 6.6 y su facilidad de instalación.
- **Estabilidad de energía**: Asegúrese siempre de contar con un **Hub USB con alimentación externa** para garantizar la salida de señal óptima de las tarjetas inalámbricas de alta potencia y evitar desconexiones inesperadas.

Si desea realizar consultas técnicas adicionales, cotizaciones de hardware o requiere compilaciones personalizadas a través del SDK de OpenWrt, no dude en ponerse en contacto con el **Equipo de Soporte Técnico de Yupitek**:

- 🌐 Sitio web oficial: [www.yupitek.com](https://www.yupitek.com)
- 📧 Correo de soporte: [sales@yupitek.com](mailto:sales@yupitek.com)
- 📞 Teléfono: +886-2-87325338
- 📍 Dirección de la compañía: 1F., No. 72, Ln. 34, Fuyang St., Xinyi Dist., Taipei City, Taiwán
