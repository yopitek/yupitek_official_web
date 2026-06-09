---
title: "Adaptadores WiFi ALFA con Kali NetHunter: Guía Técnica Completa 2026"
description: "Referencia técnica para adaptadores WiFi USB ALFA con Kali NetHunter. Compatibilidad con smartphones del mercado taiwanés, análisis de controladores in-kernel vs DKMS, configuración OTG y resultados de pruebas verificados."
date: 2026-06-09
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["nethunter", "kali-linux", "alfa-network", "wireless-security", "android", "usb-otg", "monitor-mode", "packet-injection", "mt7610u", "mt7612u", "rtl8812au"]
---

Si ya ha configurado un adaptador ALFA con NetHunter siguiendo las instrucciones básicas de OTG y desea la versión rápida, nuestra [guía de configuración OTG](/es/blog/alfa-adapter-nethunter-android-otg/) cubre los aspectos esenciales. Este artículo profundiza más: es una referencia técnica completa dirigida a profesionales de seguridad que necesitan evaluar la compatibilidad de teléfonos y adaptadores antes de adquirir el hardware, comprender qué enfoque de controlador sigue funcionando tras las actualizaciones del kernel y ver resultados de pruebas verificados antes de comprometerse con una combinación específica.

Nos centramos en una pregunta que la mayoría de las guías de NetHunter omiten: **¿qué adaptador es realmente plug-and-play y cuál le llevará a un laberinto de compilación de controladores en el peor momento posible?** La respuesta depende del chipset, de la versión del kernel del teléfono y de si el controlador se incluye dentro del árbol del kernel o reside en un repositorio DKMS externo. Equivocarse significa que su adaptador se quedará en la mochila mientras usted mira errores de `modprobe` sobre el terreno. Acertar significa que lo conecta y empieza a escanear.

---

## 1. Requisitos del Cliente

### 1.1 Caso de Uso

Los pentesters móviles necesitan una configuración que sustituya completamente el portátil. El teléfono ejecuta Kali NetHunter, el adaptador ALFA se conecta mediante USB OTG y el operador realiza evaluaciones de seguridad Wi-Fi sin necesidad de llevar un ordenador portátil. El flujo de trabajo principal — site survey, captura en monitor mode, packet injection, recolección de handshakes WPA — debe funcionar de forma fiable con batería.

### 1.2 Requisitos Esenciales

| Requisito | Detalle |
|---|---|
| Plataforma | Teléfono Android con Kali NetHunter (edición completa, kernel personalizado) |
| Conexión | Cable USB OTG o hub OTG con alimentación externa |
| Adaptador | Adaptador WiFi USB ALFA con soporte para monitor mode y packet injection |
| Enfoque de controlador | Priorizar chipsets in-kernel (sin controlador externo) para eliminar dependencias de compilación |
| Mercado taiwanés | Teléfonos disponibles oficialmente en Taiwán, modelos 2024–2026 |
| Alimentación | Funcionamiento con batería; se recomienda encarecidamente un hub OTG con alimentación externa para uso sostenido |

---

## 2. Análisis de Hardware y Software Objetivo

### 2.1 Teléfonos Compatibles con NetHunter Disponibles en Taiwán

NetHunter es compatible con más de 117 módulos de dispositivo, pero la mayoría son modelos antiguos. Tras filtrar los dispositivos que (a) están disponibles oficialmente en Taiwán, (b) son de 2024 o posterior, y (c) tienen kernels personalizados de NetHunter funcionales, destacan tres teléfonos:

| Modelo | Nombre en Clave | CPU | Versiones de Kernel | Imágenes Precompiladas | Disponibilidad en Taiwán |
|---|---|---|---|---|---|
| **OnePlus 11 5G** | salami | Snapdragon 8 Gen 2 (ARM64) | 2 | 2 | ✅ Disponible mediante canales de importación, lanzamiento 2023 |
| **Nothing Phone (1)** | spacewar | Snapdragon 778G+ (ARM64) | 3 | 1 | ✅ Lanzado oficialmente en Taiwán, comunidad activa |
| **Samsung Galaxy S20 FE 5G** | r8q | Snapdragon 865 (ARM64) | 5 | 1 | ✅ Vendido en Taiwán — **se requiere variante Snapdragon** |

{{< alert "triangle-exclamation" >}}
**Advertencia sobre Samsung Exynos:** La mayoría de los dispositivos Samsung vendidos a través de operadores taiwaneses utilizan chipsets Exynos. Los kernels de NetHunter solo admiten la variante Snapdragon (`r8q`). Antes de adquirir un dispositivo Samsung para NetHunter, verifique el modelo de CPU: si la ficha técnica indica "Exynos", no funcionará. Adquiera una unidad Snapdragon mediante importación o elija el OnePlus 11 en su lugar.
{{< /alert >}}

**NetHunter Rootless** se ejecuta en cualquier dispositivo Android sin necesidad de root, pero no admite adaptadores WiFi USB externos para monitor mode. Si necesita packet capture e injection, necesita la edición completa de NetHunter con un kernel personalizado.

### 2.2 Especificaciones Técnicas de la Plataforma

Usando el OnePlus 11 5G como plataforma de referencia:

| Parámetro | Especificación |
|---|---|
| Arquitectura de CPU | ARM64 (aarch64) |
| SoC | Qualcomm Snapdragon 8 Gen 2 (SM8550) |
| Controlador USB | USB 3.1 Gen 1 con soporte OTG |
| Alimentación USB | 5V / 900mA (utilice un hub OTG con alimentación externa para un funcionamiento sostenido del adaptador) |

### 2.3 Entorno de Software

| Componente | Requisito | Versión Recomendada |
|---|---|---|
| SO Anfitrión | Android con Kali chroot | Android 11+ |
| NetHunter | Edición completa (kernel personalizado) | 2024.4 (última estable) |
| Kernel Linux | Kernel personalizado específico del dispositivo | 5.x o posterior preferible |
| Controladores Precargados | Consulte la Sección 4 para la matriz | — |
| DKMS | Requerido solo para adaptadores basados en RTL8812AU | Los kernel headers deben coincidir |
| Herramientas Inalámbricas | aircrack-ng, Kismet, MANA Toolkit | Proporcionadas por NetHunter chroot |
| Root | Requerido para funcionalidad completa | Magisk 26.0+ |

---

## 3. Especificaciones de los Adaptadores ALFA y Fuentes de Controladores

### 3.1 AWUS036ACHM — Mejor Opción para NetHunter

| Parámetro | Especificación |
|---|---|
| Chipset | **MediaTek MT7610U** |
| USB VID/PID | `0x0e8d:0x7610` |
| Bandas | 2.4 GHz + 5 GHz (AC433) |
| Velocidad Máxima de Datos | 150 Mbps (2.4 GHz) / 433 Mbps (5 GHz) |
| USB | USB 2.0 |
| Monitor Mode | ✅ Soporte completo |
| Packet Injection | ✅ Soporte completo |
| Antena | 1× de alta ganancia desmontable (RP-SMA) |
| Controlador | **In-kernel** — no requiere instalación |
| Módulo del Kernel | `mt76x0u` |
| Requisito de Kernel | Linux 4.19+ |
| Página de Producto | [/es/products/alfa/awus036achm/](/es/products/alfa/awus036achm/) |

El chipset MT7610U es ampliamente recomendado por las comunidades de Kali y NetHunter porque su controlador `mt76x0u` está en el kernel principal de Linux desde la versión 4.19. Lo conecta, el kernel lo reconoce y empieza a trabajar. Sin toolchain de compilación, sin kernel headers, sin DKMS — solo la confirmación de `lsusb` seguida de `airmon-ng start`.

### 3.2 AWUS036ACM — Alternativa de Alto Rendimiento

| Parámetro | Especificación |
|---|---|
| Chipset | **MediaTek MT7612U** |
| USB VID/PID | `0x0e8d:0x7612` |
| Bandas | 2.4 GHz + 5 GHz (AC1200) |
| Velocidad Máxima de Datos | 300 Mbps (2.4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| Monitor Mode | ✅ Soporte completo |
| Packet Injection | ✅ Confirmado estable en Kali 2024.3 / 2025.1 |
| Antena | 2× antenas duales (RP-SMA), MIMO 2T2R |
| Controlador | **In-kernel** — no requiere instalación |
| Módulo del Kernel | `mt76x2u` |
| Requisito de Kernel | Linux 4.19+ |
| Página de Producto | [/es/products/alfa/awus036acm/](/es/products/alfa/awus036acm/) |

El ACM añade doble banda AC1200 con MIMO 2T2R y rendimiento USB 3.0. El controlador `mt76x2u` también está en el kernel principal desde la versión 4.19. Una advertencia: algunos kernels personalizados más antiguos de NetHunter (notablemente el kernel del OnePlus 7T en la versión 4.14) se compilaron sin el módulo `mt76x2u`. En cualquier kernel 4.19 o posterior esto no es un problema, pero compruébelo con `lsmod | grep mt76x2u` si su dispositivo ejecuta una compilación de kernel más antigua.

### 3.3 AWUS036ACH — Mayor Soporte de la Comunidad

| Parámetro | Especificación |
|---|---|
| Chipset | **Realtek RTL8812AU** |
| USB VID/PID | `0x0bda:0x8812` |
| Bandas | 2.4 GHz + 5 GHz (AC1200) |
| Velocidad Máxima de Datos | 300 Mbps (2.4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| Monitor Mode | ✅ Soporte completo |
| Packet Injection | ✅ Soporte completo |
| Antena | 2× 5dBi externas (RP-SMA) |
| Controlador | DKMS externo (precompilado en la mayoría de kernels NetHunter) |
| Módulo del Kernel | `88XXau` |
| Repositorio del Controlador | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| Página de Producto | [/es/products/alfa/awus036ach/](/es/products/alfa/awus036ach/) |

El ACH ha sido el estándar de facto para configuraciones de Kali y NetHunter durante años. La mayoría de los kernels personalizados de NetHunter incluyen el módulo `88XXau` precompilado, por lo que normalmente no necesita compilar desde el código fuente. Sin embargo, si su versión de kernel no lo incluye, necesitará un entorno de compilación funcional con kernel headers coincidentes — exactamente el tipo de cadena de dependencias que los chipsets MT7610U y MT7612U evitan. Sus dos antenas de 5dBi le otorgan el mayor alcance de señal de toda la gama, lo cual es relevante para escenarios de captura de largo alcance.

### 3.4 AWUS036ACS — Factor de Forma Compacto

| Parámetro | Especificación |
|---|---|
| Chipset | Realtek RTL8811AU |
| USB VID/PID | `0x0bda:0x0811` |
| Bandas | 2.4 GHz + 5 GHz (AC433) |
| USB | USB 2.0 |
| Monitor Mode | ✅ Compatible (misma familia de controladores que RTL8812AU) |
| Packet Injection | ✅ Compatible |
| Antena | Interna, cuerpo ultra delgado de 55 mm |
| Consumo Eléctrico | ~300mW — el más bajo de la gama |
| Controlador | Externo (repositorio aircrack-ng compartido con RTL8812AU) |
| Página de Producto | [/es/products/alfa/awus036acs/](/es/products/alfa/awus036acs/) |

El ACS es la opción más portátil. Con un consumo de 300mW es el menos exigente para las baterías de los teléfonos, y su factor de forma delgado desaparece en un bolsillo. El compromiso es el rendimiento AC433 de flujo único y la dependencia del controlador DKMS externo compartida con la familia RTL8812AU.

### 3.5 Adaptadores No Recomendados para NetHunter

| Adaptador | Chipset | Motivo |
|---|---|---|
| AWUS036AX / AWUS036AXER | RTL8832BU | Requiere kernel 6.14+; estabilidad de monitor mode no verificada en kernels Android |
| AWUS036AXML / AWUS036AXM | MT7921AUN | El soporte WiFi 6E / 6 GHz es inestable en las compilaciones actuales del kernel de NetHunter; no apto como adaptador principal de pentest |

### 3.6 Repositorios de Código Fuente de los Controladores

| Chipset | Controlador | Fuente |
|---|---|---|
| MT7610U | `mt76x0u` (in-kernel) | [torvalds/linux — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| MT7612U | `mt76x2u` (in-kernel) | Mismo árbol del kernel que el anterior |
| RTL8812AU | `88XXau` (externo) | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| RTL8811AU | `88XXau` (externo, compartido) | Mismo repositorio de aircrack-ng |

---

## 4. Análisis de Compatibilidad de Controladores

### 4.1 In-Kernel vs DKMS Externo

La decisión más importante al elegir un adaptador para NetHunter es si el controlador reside dentro del árbol del kernel o fuera de él. He aquí el motivo:

| | In-Kernel (MT7610U, MT7612U) | DKMS Externo (RTL8812AU, RTL8811AU) |
|---|---|---|
| Plug-and-play | ✅ Sí — reconocido al insertarlo | ⚠️ Depende de que el kernel tenga `88XXau` precompilado |
| Sobrevive a actualizaciones del kernel | ✅ Sí — el controlador es parte de la compilación del kernel | ❌ Puede fallar tras una actualización del kernel; requiere recompilación |
| Necesita linux-headers | ❌ No | ✅ Sí, si se requiere compilación manual |
| Necesita DKMS | ❌ No | ✅ Sí, si no está precompilado en el kernel |
| Documentación de la comunidad | Moderada | Extensa (ACH tiene la mayor cantidad de tutoriales) |
| Riesgo de fallo sobre el terreno | Bajo | Moderado (dependencia de compilación) |

**Conclusión:** Si desea el menor riesgo posible de problemas de controladores sobre el terreno, elija un adaptador MT7610U o MT7612U. El controlador ya está en el kernel — no hay nada que compilar, nada que se rompa durante una actualización y nada que solucionar cuando esté en el sitio del cliente.

### 4.2 Matriz de Soporte de Módulos del Kernel NetHunter

| Dispositivo | Kernel NetHunter | MT7610U (`mt76x0u`) | MT7612U (`mt76x2u`) | RTL8812AU (`88XXau`) |
|---|---|---|---|---|
| OnePlus 11 5G | Kernel Android 13 | ✅ Compatible | ✅ Compatible | ✅ Compatible |
| Samsung S20 FE (Snapdragon) | Kernel Android 12 (4.19) | ✅ Compatible | ✅ Compatible | ✅ Compatible (verifique informes de XDA) |
| Nothing Phone (1) | Kernel Android 12/13 | ✅ Compatible | Verifique la configuración del kernel | ✅ Compatible |
| OnePlus 7/7T | 4.14 (más antiguo) | ✅ Compatible | ⚠️ Podría faltar en la compilación | ✅ Compatible |

Fuentes: NetHunter GitLab, informes de la comunidad de XDA Forums (2024–2026).

### 4.3 Problemas Conocidos

**Problema 1: La interfaz MT7612U no aparece en kernels antiguos**

Síntoma: `lsusb` muestra `0e8d:7612` pero `ip link` no lista ningún `wlan1`.  
Causa raíz: El kernel personalizado se compiló sin el módulo `mt76x2u`. Esto afecta a algunos kernels NetHunter basados en 4.14 (era del OnePlus 7T).  
Solución: Utilice una compilación del kernel que incluya el módulo, o cambie al AWUS036ACHM (MT7610U) que tiene un soporte más amplio en kernels antiguos.

**Problema 2: El brownout de alimentación USB causa desconexiones del adaptador**

Síntoma: El adaptador desaparece durante el escaneo, `dmesg` muestra errores de reinicio USB.  
Causa raíz: El puerto USB del teléfono no puede mantener el consumo de corriente del adaptador, especialmente para adaptadores USB 3.0 (ACH consume ~500mW).  
Solución: Utilice un hub OTG con alimentación externa que suministre 5V al adaptador desde un cargador de pared mientras transmite los datos al teléfono.

**Problema 3: Adaptador insertado antes de iniciar el chroot**

Síntoma: Android muestra el diálogo de permiso USB, pero las herramientas de Kali no pueden acceder al adaptador.  
Causa raíz: El entorno chroot de NetHunter debe estar en ejecución antes de que los dispositivos USB se expongan a él.  
Solución: Inicie el chroot primero (Kali Services → Start), luego conecte el adaptador y conceda el permiso USB.

---

## 5. Guía de Configuración

### 5.1 Requisitos Previos

Antes de conectar cualquier hardware, verifique:

```bash
# Confirme que el dispositivo tiene root
su -c "id"

# Verifique la versión del chroot de NetHunter
cat /kali/etc/os-release
# Debería mostrar Kali Linux with NetHunter

# Confirme que USB OTG está habilitado
# Ajustes → Opciones de Desarrollador → OTG (la ubicación exacta varía según la versión de Android)
```

### 5.2 Secuencia de Conexión del Hardware

El orden importa:

1. Inicie la **aplicación NetHunter** → abra **Kali Services** → pulse **Start** para levantar el chroot
2. Conecte el **hub OTG con alimentación externa** al puerto USB de su teléfono
3. Conecte el **adaptador ALFA** al hub OTG
4. Cuando aparezca el diálogo de permiso USB de Android, pulse **OK** y marque **Permitir siempre**

{{< alert "circle-info" >}}
Se recomienda encarecidamente un hub OTG con alimentación externa para un funcionamiento sostenido. El AWUS036ACH consume aproximadamente 500mW — alimentarlo directamente desde la batería del teléfono acelera significativamente el drenaje y puede causar inestabilidad USB. Un hub que transmita los datos mientras toma la alimentación de un cargador de pared elimina ambos problemas.
{{< /alert >}}

### 5.3 Verificar la Detección del Adaptador

```bash
# Liste los dispositivos USB — confirme que el adaptador aparece
lsusb

# Salida esperada por modelo:
# AWUS036ACHM: Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.
# AWUS036ACM:  Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U
# AWUS036ACH:  Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp.
```

Si el adaptador no aparece: pruebe con un cable OTG diferente, verifique que OTG está habilitado en las opciones de desarrollador o pruebe el adaptador en un ordenador para confirmar que funciona.

### 5.4 Cargar el Controlador

**Para MT7610U (AWUS036ACHM) — se carga automáticamente en la mayoría de los kernels:**

```bash
# Verifique la carga automática
lsmod | grep mt76

# Carga manual si es necesario (poco común)
sudo modprobe mt76x0u
```

**Para MT7612U (AWUS036ACM) — se carga automáticamente en kernel 4.19+:**

```bash
# Verifique
lsmod | grep mt76

# Carga manual si es necesario
sudo modprobe mt76x2u
```

**Para RTL8812AU (AWUS036ACH) — precompilado en la mayoría de los kernels NetHunter:**

```bash
# Cargue el módulo precompilado
sudo modprobe 88XXau

# Verifique que se cargó
lsmod | grep 88XX
```

### 5.5 Confirmar la Interfaz de Red

```bash
# Liste las interfaces inalámbricas
ip link show | grep wlan

# O utilice iw
iw dev

# El adaptador externo suele aparecer como wlan1
# (wlan0 suele ser el WiFi integrado del teléfono)
```

### 5.6 Activar Monitor Mode

```bash
# Termine los procesos que interfieren
sudo airmon-ng check kill

# Inicie monitor mode en el adaptador
sudo airmon-ng start wlan1

# Verifique que monitor mode está activo
iwconfig wlan1mon
# Salida esperada: Mode:Monitor

# Escanee redes cercanas (solo pruebas autorizadas)
sudo airodump-ng wlan1mon

# Escanee todas las bandas (2.4 GHz + 5 GHz)
sudo airodump-ng --band abg wlan1mon
```

### 5.7 Volver a Managed Mode

```bash
sudo airmon-ng stop wlan1mon
sudo service NetworkManager restart
```

---

## 6. Topología de la Aplicación

![Diagrama de arquitectura NetHunter + ALFA](/images/blog/nethunter-topology.png)

---

## 7. Resultados de Validación

### 7.1 Matriz de Pruebas

Las siguientes combinaciones han sido verificadas mediante pruebas de la comunidad y documentación del fabricante:

| Teléfono | Adaptador ALFA | Chipset | Monitor Mode | Packet Injection | Estado |
|---|---|---|---|---|---|
| OnePlus 11 5G | AWUS036ACHM | MT7610U | ✅ | ✅ | Verificado |
| OnePlus 11 5G | AWUS036ACM | MT7612U | ✅ | ✅ | Verificado |
| OnePlus 11 5G | AWUS036ACH | RTL8812AU | ✅ | ✅ | Verificado |
| Samsung S20 FE (Snapdragon) | AWUS036ACH | RTL8812AU | ✅ | ⚠️ | Informes de la comunidad — verifique la configuración del kernel |
| Samsung S20 FE (Snapdragon) | AWUS036ACHM | MT7610U | ✅ | ✅ | Informes de la comunidad |
| Nothing Phone (1) | AWUS036ACHM | MT7610U | ✅ | ✅ | Informes de la comunidad |

Fuentes: XDA Forums, Reddit r/NetHunter, Kali NetHunter GitLab Issues (2024–2026).

### 7.2 Salida Esperada de `lsusb`

```
# AWUS036ACHM
Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.

# AWUS036ACM
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter

# AWUS036ACH
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
```

### 7.3 Verificación de Monitor Mode

```bash
# Salida esperada de iwconfig en caso de éxito
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.437 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

---

## 8. Recomendaciones

### 8.1 Mejor Opción: OnePlus 11 5G + AWUS036ACHM

Esta combinación tiene la menor fricción de todas las configuraciones probadas. El OnePlus 11 es el buque insignia más reciente con soporte oficial de kernel NetHunter que aún puede conseguir para el mercado taiwanés. El chipset MT7610U del AWUS036ACHM utiliza el controlador `mt76x0u` — está en el kernel principal desde la versión 4.19, no requiere compilación alguna y la comunidad internacional de seguridad (Lab401, base de datos USB-WiFi de morrownr) lo clasifica consistentemente como la opción más segura para Kali y NetHunter. El adaptador es compacto, de antena única y funciona con USB 2.0, lo cual es una ventaja en escenarios móviles — menor consumo eléctrico, menos calor, menos cosas que pueden fallar.

### 8.2 Opción de Rendimiento: OnePlus 11 5G + AWUS036ACM

Si necesita rendimiento de doble banda AC1200 con MIMO 2T2R para captura en 5 GHz con alcance, el ACM le ofrece eso sin abandonar el ecosistema de controladores in-kernel. El controlador `mt76x2u` del MT7612U también está en el kernel principal desde la versión 4.19. El compromiso: USB 3.0 consume más energía y el cuerpo de doble antena es más grande. Verifique que el kernel incluya `mt76x2u` — en el OnePlus 11 esto está confirmado.

### 8.3 Favorito de la Comunidad: Cualquier Dispositivo NetHunter + AWUS036ACH

El ACH tiene la mayor cantidad de tutoriales, la base de resolución de problemas de la comunidad más amplia y la mejor documentación de terceros de todos los adaptadores del ecosistema NetHunter. Sus dos antenas de 5dBi le otorgan el mayor alcance de señal de la gama ALFA. La mayoría de los kernels NetHunter precompilan el módulo `88XXau`, por lo que rara vez se necesita compilación. Si valora el soporte de la comunidad y la captura de largo alcance por encima de la simplicidad plug-and-play, esta es la elección.

### 8.4 Selección por Escenario

| Escenario | Combinación Recomendada | Justificación |
|---|---|---|
| Primera configuración con NetHunter, minimizar riesgos | OnePlus 11 + AWUS036ACHM | Controlador in-kernel, sin compilación, factor de forma más reducido |
| Captura de doble banda con alcance | OnePlus 11 + AWUS036ACM | AC1200 + MIMO, sigue siendo in-kernel |
| Site survey de largo alcance, máxima cantidad de tutoriales | Cualquier dispositivo compatible + AWUS036ACH | Antena más potente, mayor soporte de la comunidad |
| Ultra portátil, consumo más bajo | Cualquier dispositivo compatible + AWUS036ACS | Consumo de 300mW, cabe en cualquier bolsillo |

### 8.5 Recursos de Soporte

| Recurso | Enlace |
|---|---|
| Yupitek — distribuidor autorizado de ALFA en Taiwán | [yupitek.com](https://www.yupitek.com) |
| Páginas oficiales de productos ALFA Network | [alfa.com.tw](https://www.alfa.com.tw) |
| Controlador MT7610U (árbol del kernel) | [torvalds/linux — mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| Controlador RTL8812AU (aircrack-ng) | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| Dispositivos compatibles con NetHunter | [nethunter.kali.org/device-kernels.html](https://nethunter.kali.org/device-kernels.html) |
| Documentación oficial de NetHunter | [kali.org/docs/nethunter/](https://www.kali.org/docs/nethunter/) |
| Foro de XDA NetHunter | [xdaforums.com/tags/nethunter/](https://xdaforums.com/tags/nethunter/) |
| Catálogo de productos ALFA de Yupitek | [/es/products/alfa/](/es/products/alfa/) |

---

## Apéndice: Resolución Rápida de Problemas

**El adaptador no aparece en `lsusb`:**
1. Confirme que OTG está habilitado en Opciones de Desarrollador
2. Pruebe con un cable OTG diferente — la calidad del cable es el punto de fallo más común
3. Utilice un hub OTG con alimentación externa
4. Verifique que el chroot de NetHunter se ha iniciado

**El dispositivo aparece en `lsusb` pero no hay interfaz `wlan1`:**

```bash
# Revise los mensajes del kernel en busca de errores de controlador
dmesg | tail -30 | grep -E "usb|mt76|rtl|88XX"

# Verifique si el módulo del kernel existe
find /lib/modules -name "mt76*" 2>/dev/null
find /lib/modules -name "*88XX*" 2>/dev/null

# Intente la carga manual
sudo modprobe mt76x0u   # MT7610U
sudo modprobe mt76x2u   # MT7612U
sudo modprobe 88XXau    # RTL8812AU
```

**El monitor mode se inicia pero no aparecen redes:**

```bash
# Primero termine los procesos que interfieren
sudo airmon-ng check kill

# Vuelva a escanear todas las bandas
sudo airodump-ng --band abg wlan1mon

# Verifique la configuración de canales
sudo iw dev wlan1mon info
```

**El adaptador se desconecta durante el uso (reinicio USB):**

```bash
# Solución temporal — reduzca la potencia de transmisión
sudo iw dev wlan1 set txpower fixed 1000  # 10 dBm

# Solución permanente — utilice un hub OTG con alimentación externa
```

---

## Guías Relacionadas

- [Configuración básica OTG con adaptadores ALFA y NetHunter](/es/blog/alfa-adapter-nethunter-android-otg/)
- [Guía de compra de adaptadores WiFi ALFA 2026](/es/blog/alfa-wifi-adapter-buyer-guide-2026/)
- [Instalación de controladores ALFA en Kali Linux y Ubuntu](/es/blog/install-alfa-driver-kali-ubuntu/)
- [Uso de adaptadores ALFA con Raspberry Pi y Kali](/es/blog/alfa-adapter-raspberry-pi-kali/)

---

*Este documento ha sido elaborado por **Yupitek Ltd** — distribuidor autorizado de ALFA Network para Taiwán.*  
*Datos actualizados a 2026-06-09. Las versiones del kernel Linux y NetHunter se actualizan periódicamente; verifique las fuentes oficiales para obtener la información de compatibilidad más reciente.*
