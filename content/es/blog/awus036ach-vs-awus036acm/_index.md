---
title: "ALFA AWUS036ACH vs AWUS036ACM: Comparación Completa para Kali Linux (2026)"
description: "Comparación detallada del ALFA AWUS036ACH y AWUS036ACM: chipsets, modo monitor, inyección de paquetes, soporte de controladores y cuál es mejor para Kali Linux."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "AWUS036ACM", "comparación", "Kali-Linux", "RTL8812AU"]
featureimage: "/images/blog/awus036ach-vs-awus036acm.webp"
---

## Resumen General

Dos de los adaptadores USB de ALFA Network más populares para pruebas de penetración en Kali Linux se ubican en extremos distintos del espectro entre rendimiento bruto y portabilidad. El **AWUS036ACH** es una bestia de trabajo de alta potencia y doble antena con una historia de controladores probada en batalla. El **AWUS036ACM** es una alternativa compacta con soporte nativo del kernel que sacrifica algo de potencia a cambio de simplicidad y facilidad de uso. Esta guía desglosa cada aspecto que importa para el trabajo real de pentesting.

---

## AWUS036ACH — AC1200, RTL8812AU, Alta Potencia

El [AWUS036ACH](/es/products/alfa/awus036ach/) ha sido un elemento fundamental en la auditoría Wi-Fi profesional y de aficionados desde su lanzamiento. Es el adaptador citado en la mayoría de los tutoriales, cursos y writeups de pentesting inalámbrico de Kali Linux publicados entre 2017 y hoy.

**Especificaciones completas:**
- **Estándar Wi-Fi:** IEEE 802.11a/b/g/n/ac (Wi-Fi 5)
- **Chipset:** Realtek RTL8812AU
- **Bandas de frecuencia:** 2.4 GHz + 5 GHz (doble banda)
- **Rendimiento máximo:** AC1200 (300 + 867 Mbps)
- **Antenas:** 2× conectores RP-SMA desmontables (diversidad de doble antena)
- **Antenas por defecto:** 2× omnidireccionales de 5 dBi
- **Conector USB:** USB-C (compatible con USB 3.0)
- **Potencia TX:** Hasta 30 dBm — una de las más altas entre los adaptadores USB
- **Dimensiones:** Factor de forma más grande (uso en escritorio/viaje)

Los conectores RP-SMA dobles son una ventaja significativa: puedes conectar antenas direccionales u omnidireccionales de alta ganancia para ampliar dramáticamente el alcance, algo crítico en escenarios de auditoría a larga distancia.

---

## AWUS036ACM — AC600, MT7612U, Compacto

El [AWUS036ACM](/es/products/alfa/awus036acm/) apunta a usuarios que priorizan la simplicidad, portabilidad y soporte de controladores nativo del kernel. Usa el chipset MediaTek MT7612U (o MT7612UN), que ha sido parte del kernel principal de Linux desde la versión 4.19 — lo que significa **cero compilación de controladores** en cualquier sistema Kali Linux moderno.

**Especificaciones completas:**
- **Estándar Wi-Fi:** IEEE 802.11a/b/g/n/ac (Wi-Fi 5)
- **Chipset:** MediaTek MT7612U / MT7612UN
- **Bandas de frecuencia:** 2.4 GHz + 5 GHz (doble banda)
- **Rendimiento máximo:** AC600 (150 + 433 Mbps)
- **Antenas:** 1× conector RP-SMA desmontable
- **Antena por defecto:** 1× omnidireccional de 5 dBi
- **Conector USB:** USB-C (compatible con USB 3.0)
- **Potencia TX:** Potencia estándar (menor que el ACH)
- **Dimensiones:** Factor de forma compacto (uso portátil)

La antena única y la menor potencia TX significan menor rendimiento de largo alcance comparado con el ACH, pero la experiencia limpia del controlador del kernel y el cuerpo compacto lo hacen muy práctico para compromisos donde la discreción o la movilidad importan.

---

## Tabla Completa de Comparación de Especificaciones

| Característica | AWUS036ACH | AWUS036ACM |
|---|---|---|
| **Estándar Wi-Fi** | 802.11ac (Wi-Fi 5) | 802.11ac (Wi-Fi 5) |
| **Chipset** | RTL8812AU | MT7612U / MT7612UN |
| **Bandas de Frecuencia** | 2.4 GHz + 5 GHz | 2.4 GHz + 5 GHz |
| **Rendimiento Máximo** | AC1200 | AC600 |
| **Conectores RP-SMA** | 2× | 1× |
| **Potencia TX** | Hasta 30 dBm | Estándar |
| **Tipo USB** | USB-C | USB-C |
| **Fuente del Controlador** | Fuera del árbol (DKMS) | Kernel principal (4.19+) |
| **Instalación del Controlador** | Compilación manual | Plug-and-play |
| **Modo Monitor** | ★★★★★ | ★★★★☆ |
| **Inyección de Paquetes** | ★★★★★ | ★★★★☆ |
| **Factor de Forma** | Más grande | Compacto |
| **Rango de Precio** | ~$40–50 | ~$30–40 |

---

## Análisis Profundo del Chipset

### RTL8812AU (AWUS036ACH)

El Realtek RTL8812AU es uno de los chipsets más extensamente probados en la investigación de seguridad inalámbrica. El controlador mantenido por la comunidad se encuentra en [github.com/aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) y ha sido activamente desarrollado y parcheado desde 2017.

**Instalación en Kali Linux:**

```bash
sudo apt update
sudo apt install dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

Después de la instalación, el módulo persiste tras las actualizaciones del kernel vía DKMS. El controlador soporta:

- **Modo monitor** — completamente funcional, extremadamente confiable
- **Inyección de tramas** — todos los tipos de inyección (deauth, beacon, probe, data)
- **Múltiples interfaces virtuales** — ejecutar monitor + administrado simultáneamente
- **Captura de handshake WPA3-SAE** — confirmado funcionando en combinaciones recientes de kernel/controlador

La principal compensación es que **debes recompilar** (o DKMS lo maneja automáticamente) cuando se instala un nuevo kernel. Ocasionalmente, una nueva versión del kernel de Kali rompe temporalmente la compilación hasta que el controlador se actualiza. Es una preocupación operativa manejable pero real.

### MT7612U (AWUS036ACM)

El controlador MT7612U de MediaTek (`mt76x2u`) fue integrado al kernel principal de Linux en la versión **4.19 (octubre de 2018)**. Esto significa que en cualquier instalación de Kali Linux con kernel 4.19 o posterior — lo que cubre cada versión de Kali desde finales de 2018 — el AWUS036ACM es **plug-and-play**.

```bash
# Verificar que el módulo está cargado
lsmod | grep mt76x2u

# Carga manual si es necesario
sudo modprobe mt76x2u
```

Características clave del controlador:

- **No requiere compilación** — ideal para entornos con acceso restringido o sin conexión a internet
- **Modo monitor** — soportado y funcional
- **Inyección de paquetes** — soportada, generalmente confiable
- **Estabilidad** — los controladores nativos del kernel tienden a ser más estables tras las actualizaciones del kernel
- **Soporte comunitario** — en crecimiento, aunque menor que el ecosistema RTL8812AU

Un matiz: la variante MT7612UN (usada en algunos lotes de ACM) se comporta idénticamente en Linux, ya que ambas son manejadas por el mismo módulo `mt76x2u`.

---

## Comparación del Modo Monitor

Ambos adaptadores soportan modo monitor, pero hay diferencias prácticas.

**AWUS036ACH (RTL8812AU):**

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
# Crea wlan0mon en modo monitor
iwconfig wlan0mon
```

El cambio de canales en modo monitor es inmediato y confiable. La interfaz maneja entornos de captura de alto tráfico (APs densos, muchos clientes) sin pérdida de paquetes a tasas de captura normales.

**AWUS036ACM (MT7612U):**

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# O vía airmon-ng:
sudo airmon-ng start wlan0
```

El modo monitor es funcional y ha sido confirmado funcionando con Wireshark, tcpdump, airodump-ng y kismet. Sin embargo, algunos usuarios reportan necesitar usar `iw` directamente en lugar de airmon-ng para resultados más confiables en ciertas versiones del kernel.

---

## Comparación de Inyección de Paquetes

**AWUS036ACH:** La inyección de paquetes es uno de sus puntos más fuertes. Todos los modos de ataque de aireplay-ng funcionan de manera confiable:

```bash
# Probar inyección
sudo aireplay-ng --test wlan0mon

# Ataque de deautenticación
sudo aireplay-ng -0 5 -a [BSSID] wlan0mon

# Captura de handshake WPA vía deauth
sudo airodump-ng -c [CH] --bssid [BSSID] -w capture wlan0mon &
sudo aireplay-ng -0 3 -a [BSSID] wlan0mon
```

**AWUS036ACM:** La inyección funciona en todos los tipos de ataque estándar, aunque algunos usuarios han reportado que inyectar a tasas muy altas puede ocasionalmente hacer que la interfaz se detenga en ciertas versiones del kernel. Para flujos de trabajo típicos de pentesting (deauth controlada, captura PMKID, pruebas KRACK), funciona de manera confiable.

---

## Complejidad de Instalación del Controlador

| Tarea | AWUS036ACH | AWUS036ACM |
|---|---|---|
| Kali recién instalado, conectar el adaptador | No reconocido — necesita instalar controlador | Reconocido inmediatamente |
| Tras actualización del kernel | DKMS reconstruye automáticamente (generalmente) | No se necesita acción |
| Máquina sin acceso a internet | Requiere preparación de paquetes offline | Funciona de forma nativa |
| Kali Live USB | Debe instalar controlador en la sesión | Funciona desde el primer momento |
| Passthrough de VirtualBox/VMware | Funciona después de instalar el controlador en el guest | Funciona inmediatamente en el guest |

La experiencia de instalación cero del ACM es una ventaja genuina en escenarios como entornos de arranque en vivo, máquinas proporcionadas por clientes o configuraciones de competencias CTF donde el tiempo y la simplicidad son primordiales.

---

## Tamaño y Portabilidad

El **AWUS036ACH** tiene una PCB y carcasa notablemente más grandes. Esto se debe en parte a los conectores RP-SMA dobles y a los componentes de potencia más grandes necesarios para la salida de 30 dBm. Cabe fácilmente en una mochila de laptop pero no es un adaptador de "bolsillo".

El **AWUS036ACM** es significativamente más compacto. Puede usarse discretamente durante compromisos de seguridad física o en entornos donde un adaptador USB grande llamaría la atención. También consume menos energía, lo que importa cuando se trabaja con batería de laptop durante trabajo de campo prolongado.

---

## Precio vs Valor

A aproximadamente $40–50, el **AWUS036ACH** cobra un precio premium principalmente por su configuración de doble antena, alta potencia TX y probada herencia de controladores. Para compromisos profesionales donde la confiabilidad y la potencia de señal afectan directamente la calidad del trabajo entregado, el precio premium está justificado.

El **AWUS036ACM** a ~$30–40 ofrece excelente valor para los siguientes perfiles:
- Estudiantes aprendiendo seguridad inalámbrica que quieren simplicidad plug-and-play
- Testers que principalmente trabajan en entornos de proximidad cercana
- Equipos que necesitan un adaptador de respaldo o secundario
- Cualquiera que priorice un flujo de trabajo limpio y sin compilación

---

## Veredicto

**Elige el [AWUS036ACH](/es/products/alfa/awus036ach/) para:**
- Compromisos de pruebas de penetración profesionales y serios
- Máxima confiabilidad en modo monitor e inyección de paquetes
- Evaluaciones de largo alcance con soporte de antena externa (RP-SMA doble)
- Entornos donde la potencia de señal importa (auditorías en estacionamientos, apuntado direccional)
- Máxima compatibilidad con guías, cursos y documentación existentes

**Elige el [AWUS036ACM](/es/products/alfa/awus036acm/) para:**
- Simplicidad plug-and-play sin compilación de controladores
- Compromisos portátiles y de bajo perfil
- Configuraciones con presupuesto ajustado o adaptadores secundarios
- Flujos de trabajo con Kali Live USB
- Situaciones donde se prefiere la estabilidad nativa del kernel sobre los controladores comunitarios

Si solo puedes tener un adaptador, el **AWUS036ACH** es la elección más sólida para pentesting. Si quieres un compañero de viaje confiable con cero fricción de configuración, el **AWUS036ACM** merece su lugar en el kit de herramientas.
