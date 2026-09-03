---
title: "Cómo seleccionar el controlador Linux para la tarjeta de red USB ALFA: MediaTek sin necesidad de compilación versus Realtek con necesidad de compilación"
date: 2026-09-03
draft: false
slug: "alfa-usb-wifi-linux-driver-guide"
tags:
  - "ALFA"
  - "Linux-Driver"
  - "MediaTek"
  - "Realtek"
  - "in-kernel"
  - "out-of-tree"
  - "DKMS"
  - "mt76"
  - "rtl8812au"
categories:
  - "Guía de Hardware"
description: "\"技術文件：Yupitek ALFA USB 網卡6款機型支持\""
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

> **Documento de Soporte Técnico · Versión 1.0 (redactado según blog-writing-rules.md v1.0)**
> Máquina madre: En el cuadro de este documento técnico de Yupitek se incluyen 6 modelos de tarjetas de red USB ALFA en servicio (3 modelos MediaTek, 3 modelos Realtek).
> Artículos relacionados: [¿Soporta la tarjeta de red inalámbrica ALFA la NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/) | [¿Soporta la tarjeta de red inalámbrica ALFA OpenWrt?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) | [¿Soporta la tarjeta de red inalámbrica ALFA la NVIDIA Jetson Nano?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/) | [¿Soporta la tarjeta de red inalámbrica ALFA Tomato?](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/) | [¿Soporta la tarjeta de red inalámbrica ALFA DD-WRT?](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)

## Resumen en una frase

**De los 6 modelos revisados, 3 con procesadores MediaTek (MT7610U / MT7612U / MT7921AUN) ya tienen los controladores integrados en el kernel moderno, por lo que son plug and play; mientras que los 3 con procesadores Realtek (RTL8812AU / RTL8811CU / RTL8832BU) requieren la compilación manual de controladores out-of-tree. Si prefiere la facilidad, primero revise el procesador antes de realizar el pedido.**

---

## Primer Acto: Escena - Por qué alguien lo conecta y funciona, y alguien lo compila dos horas

Dos situaciones reales:

- Cliente A conecta **AWUS036ACM** a una máquina de escritorio Ubuntu, ejecuta `lsusb` y NetworkManager muestra wlan0 directamente - sin instalar nada.
- Cliente B conecta **AWUS036ACH** a la misma máquina, la tarjeta de red no responde, debe ir a GitHub para descargar el código fuente, instalar herramientas de compilación, compilar y reiniciar.

La diferencia no radica en la suerte ni en la versión del sistema operativo Linux, sino en **a qué campamento pertenece el chip**: El chip USB WiFi de MediaTek (serie mt76) ya ha sido incluido en el kernel principal de Linux; el chip USB WiFi de Realtek, en cambio, sigue distribuyéndose en forma out-of-tree (fuera del núcleo), dependiendo de la mantenimiento de los repositorios de controladores de la comunidad para su instalación manual.

## Segundo Acto: Mecanismos - ¿En qué se diferencian el in-kernel y el out-of-tree?

### MediaTek: Controlador mt76 de línea principal, listo para usar

El controlador de chip USB de MediaTek está cubierto por el subsistema **mt76** del kernel:

| Modelo | Chipset | Módulo de controlador del kernel | Condiciones de traducción |
|---|---|---|---|
| AWUS036ACHM | MT7610U | mt76x0u | Integrado en el kernel, sin consideraciones de versión |
| AWUS036ACM | MT7612U | mt76x2u | Integrado en el kernel, sin consideraciones de versión |
| AWUS036AXML / AXM | MT7921AUN | mt7921u | **Requiere kernel 5.19+** |

⚠️ Única trampa: **El umbral del kernel para MT7921AUN es 5.19+. Las plataformas antiguas (como JetPack 4.x de Jetson Nano, kernel 4.9) no pueden realizar backport y no son compatibles directamente. Este es el resultado verificado en los documentos técnicos de Jetson Nano (ver [¿Es compatible el adaptador inalámbrico ALFA con NVIDIA Jetson Nano?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/) §7.4).**

### Realtek: Out-of-tree, siempre traducción manual

El chip USB de Realtek no tiene un controlador de línea principal disponible, dependiendo de los repositorios de mantenimiento comunitario. Actualmente, el mantenedor más activo es **morrownr**, y esta revisión cubre 3 chips y 3 repositorios:

| Modelo | Chipset | Repositorio de controladores (mantenido por morrownr) | Revisión del 3 de septiembre de 2026 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | [8812au-20210820](https://github.com/morrownr/8812au-20210820) | ✅ Revisado |
| AWUS036EACS | RTL8811CU | [8821cu-20210916](https://github.com/morrownr/8821cu-20210916) | ✅ Revisado |
| AWUS036AX / AXER | RTL8832BU | [rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | ✅ Revisado |

### Aplicación en tres entornos típicos

| Entorno | Kernel | Campaña MediaTek (3 modelos) | Campaña Realtek (3 modelos) |
|---|---|---|---|
| GB10 / DGX Spark | 6.x + aarch64 | Todos disponibles (mt76 integrado) | Todos necesitan compilación (ARM64 compatible) |
| Jetson Nano (JetPack 4.x) | 4.9 | 7610U/7612U disponibles; MT7921AUN **no disponible** | 8812au قابل برای ترجمه (پشتیبانی ARM64); بقیه تایید نشده |
| Router OpenWrt | Versión | Todos disponibles (MT7921AUN necesita 23.05+) | Necesita kmod correspondiente o compilación, dificultad alta |

（Matriz de determinación completa de cada entorno en [¿Es compatible el adaptador inalámbrico ALFA con NVIDIA DGX Spark?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)、[¿Es compatible el adaptador inalámbrico ALFA con NVIDIA Jetson Nano?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)、[¿Es compatible el adaptador inalámbrico ALFA con OpenWrt?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/).）

## Tercera Escena: Herramientas - Proceso de Detección en Tres Minutos y Pasos de Instalación

### Tabla de Detección: Al obtener una tarjeta de red, realice estos tres pasos

```bash
# Paso 1: Verifique que el sistema reconozca la tarjeta de red (registre VID:PID)
lsusb

# Paso 2: Verifique si el kernel ha cargado el controlador correspondiente
lsmod | grep -E "mt76|rtl8"

# Paso 3: Verifique la versión del kernel (determine si el MT7921AUN puede utilizarse)
uname -r
```

Lógica de detección (matriz principal: los 6 modelos de la tabla superior):

1. `lsusb` muestra **MediaTek / MT76xx** → campamento in-kernel, kernel ≥ 5.19 (modelos MT7921AUN) o cualquier kernel reciente, plug and play.
2. `lsusb` muestra **Realtek RTL88xx** → campamento out-of-tree, siga los pasos de instalación a continuación.
3. `lsusb` **no muestra** nuevos dispositivos → primero cambie el puerto / cable USB para descartar problemas de hardware, luego verifique si el modelo es RTL8832BU de Wi-Fi 6 (algunos lotes requieren `usb_modeswitch`, este paso es un problema de modelo individual, no se detalla aquí, no se incluye en la matriz de revisión).

### Instalación General para el Campamento Realtek (a ejemplo de AWUS036ACH)

```bash
# Paso 1: Instale las dependencias de compilación (Debian/Ubuntu)
sudo apt install build-essential dkms linux-headers-$(uname -r)

# Paso 2: Obtenga el código fuente del controlador (repo correspondiente al modelo, véase la tabla superior)
git clone https://github.com/morrownr/8812au-20210820
cd 8812au-20210820

# Paso 3: Instale (registre DKMS, no es necesario reinstalar al cambiar el kernel)
sudo ./install-driver.sh

# Paso 4: Verifique después de reiniciar
lsmod | grep 88XXau
ip link   # Debería aparecer una nueva interfaz wlan
```

> **Tabla 1: Conclusión: La detección precede a la instalación - primero revise el chip, 90 segundos para determinar si es "plug and play" o "compilar en el repo", sin necesidad de golpear una pared.**

### Recomendaciones de Compra (conclusión)

- **Sin compilación**: Elegir el campamento MediaTek (AWUS036ACHM / ACM / AXML), todos los kernel recientes son plug and play.
- **Wi-Fi 6 y sin compilación**: Elegir AWUS036AXML (MT7921AUN), pero primero verifique que el kernel sea ≥ 5.19.
- **Tiene necesidades especiales y solo puede usar Realtek** (como herramientas específicas de monitor mode): Reserve 20-40 minutos para la compilación del controlador, y verifique que la plataforma objetivo tenga los headers del kernel.

## Condiciones conocidas y condiciones de objeción

La conclusión de este artículo no se aplica en las siguientes condiciones, por favor, adopte alternativas:

1. **Kernel 5.19 o anterior + MT7921AUN**: mt7921u no puede realizar backport (depende de la infraestructura del kernel moderno), la conclusión se invierte a "no disponible". Esto es la excepción más importante de este artículo.
2. **No x86/ARM64 Linux** (como ciertos routers MIPS): el repositorio morrownr no garantiza que sea compilable, debe priorizarse el kmod de OpenWrt (ver [¿Soporta ALFA la tarjeta inalámbrica OpenWrt?](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)).
3. **Versión evolutiva del repositorio de controladores**: el repositorio morrownr se nombra con la fecha (como rtl8852bu-20250826), puede que en el futuro se modifique o elimine; antes de instalar, verifique la situación actual del repositorio.
4. **Capacidad de modo monitor / modo AP**: las capacidades varían según el chip y la versión del kernel (por ejemplo, rtl8812au-ct en OpenWrt 22.03+ tiene informes de fallos en 24.10), la matriz de capacidades detallada se encuentra en artículos específicos para cada entorno.
5. **RTL8832BU (AWUS036AX/AXER) no está incluido en los 6 modelos enumerados en este artículo, pero a menudo se pregunta en el servicio al cliente**: el mantenedor de controladores morrownr ha expresado públicamente que la serie de chips "es un controlador muy malo, sospechando que hay problemas en el chip en sí", se recomienda a los usuarios de Linux evitarla en la actualidad, no solo por la dificultad de compilación, y al responder a los clientes debe explicar esto de manera honesta.

## Referencias

| Fuente | Descripción | URL | Estado de verificación | Fecha de verificación |
|---|---|---|---|---|
| morrownr/8812au GitHub | Controlador RTL8812AU para Linux | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 2026-09-03 |
| morrownr/8821cu GitHub | Controlador RTL8811CU para Linux | https://github.com/morrownr/8821cu-20210916 | ✅ Verificado | 2026-09-03 |
| morrownr/rtl8852bu GitHub | Controlador RTL8832BU para Linux | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Verificado | 2026-09-03 |
| Yupitek ALFA Productos | Catálogo de modelos y especificaciones | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 2026-09-03 |
| Yupitek Blog: Guía Soft AP | Documentación de verificación del modo AP | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verificado | 2026-09-03 |
| Documentos técnicos de este sitio 9 artículos | Matrices de determinación y base de verificación del entorno | Enlaces relativos (ver artículos relacionados en la parte superior de este documento) | ✅ Verificado | 2026-09-03 |

> Página oficial de wiki kernel mt76: https://wireless.wiki.kernel.org/en/users/drivers/mediatek （Verificado, lista las versiones de kernel de inicio que soportan cada chip, puede usarse como referencia rápida)

## Aviso Legal

Este documento ha sido compilado por el departamento de soporte técnico de Yupitek Ltd, y las especificaciones y estado de los controladores pueden variar según las actualizaciones del kernel y los repositorios de controladores. Antes de la instalación, por favor, consulte los repositorios oficiales y las páginas de especificaciones del fabricante. ALFA Network es una marca autorizada por nuestra empresa.
