---
title: "SDRLab Flipper Zero Tarjeta de Expansión 5G — Módulo de Seguridad Wi-Fi de Doble Banda"
description: "Tarjeta de expansión Flipper Zero 5G, RTL8720DN Wi-Fi doble banda (2.4+5GHz), BLE 5.0, firmware Deauth preinstalado, alimentado por GPIO, compatible con Momentum/Unleashed."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Expansión Flipper Zero", "5GHz", "Wi-Fi", "Deauth", "Investigación de seguridad"]
---

{{< alert "warning" >}}
**Declaración de uso legal**: Esta tarjeta de expansión es exclusivamente para investigación de seguridad autorizada y uso legal en investigación. Asegúrate de cumplir con las regulaciones locales sobre el uso del espectro de radiofrecuencia.
{{< /alert >}}

## Características

![SDRLab Flipper Zero Tarjeta de Expansión 5G](/images/products/sdrlab/flipper-5g.png)

- **Cobertura de doble banda** — 2,4 GHz + 5 GHz (IEEE 802.11 a/b/g/n); accede a redes 5 GHz modernas anteriormente inaccesibles con módulos de expansión solo de 2,4 GHz
- **Realtek RTL8720DN (módulo AI Thinker BW16)** — SoC de doble banda estándar de la industria con módulo precertificado FCC/CE
- **CPU de doble núcleo** — ARM Cortex-M4 @ 200 MHz gestiona protocolos activos; Cortex-M0 @ 20 MHz ejecuta tareas en segundo plano de bajo consumo
- **Firmware Marauder 5G preinstalado** — incluye modos de escaneo, deauth, inundación de beacon, sniffing (EAPOL/PMKID) y Evil Portal; listo para usar
- **BLE 5.0** — enumeración de dispositivos BLE 5.0 y análisis de balizas junto a la investigación Wi-Fi
- **Alimentado por GPIO** — toma 5 V directamente del header GPIO del Flipper Zero; sin fuente de alimentación externa
- **Ruta de mejora de antena** — conector IPEX (U.FL) en revisiones compatibles para conectar antena externa de alta ganancia
- **Ecosistema de firmware compatible** — compatible con los frameworks de firmware personalizado Momentum y Unleashed
- **Desarrollo con PlatformIO** — soporte completo para desarrollo de firmware personalizado mediante el framework Arduino-compatible Ameba D
- **Rango de operación robusto** — −40°C a 85°C para uso en campo en cualquier clima

## Especificaciones

| Especificación | Valor / Descripción |
|----------------|---------------------|
| Chip principal | Realtek RTL8720DN (módulo AI Thinker BW16) |
| CPU | ARM Cortex-M4 @ 200 MHz + Cortex-M0 @ 20 MHz |
| Estándar Wi-Fi | IEEE 802.11 a/b/g/n (doble banda 2,4 GHz + 5 GHz) |
| Potencia TX Wi-Fi | ~17 dBm (limitado por regulaciones regionales) |
| Bluetooth | BLE 5.0 |
| Flash | 4 MB |
| Fuente de alimentación | GPIO del Flipper Zero (5 V) |
| Consumo de corriente típico | 150–250 mA (escaneo activo) |
| Interfaz de conexión | Pines GPIO estándar del Flipper Zero (2×8 pines) |
| Firmware preinstalado | Marauder 5G (escaneo, Deauth, Beacon, sniffing, Evil Portal) |
| Compatibilidad de firmware | Momentum, Unleashed |
| Desarrollo secundario | PlatformIO (framework Ameba D / RTL8720DN) |
| Temperatura de operación | −40°C a 85°C |
| Interfaz de antena | IPEX (U.FL) o antena PCB integrada (según versión) |
| Factor de forma | Tarjeta de expansión GPIO Flipper Zero |

## Casos de Uso

- **Escaneo Wi-Fi de doble banda** — enumera pasivamente redes 2,4 GHz y 5 GHz; captura SSID, BSSID, canal, RSSI, tipo de cifrado y clientes conectados
- **Investigación de seguridad con Deauth** — envía tramas 802.11 Deauth para probar la resiliencia de la red y evaluar la efectividad de la protección 802.11w/PMF en redes autorizadas
- **Captura de handshake WPA** — sniffing de handshakes EAPOL/PMKID para auditoría de seguridad de redes autorizadas
- **Desarrollo de Evil Portal** — prototipado de escenarios de AP falso con portal cautivo para pruebas de concienciación sobre phishing (solo en entornos autorizados)
- **Pruebas de Beacon Flood** — difusión de SSIDs personalizados para estudiar el impacto de la congestión RF y el comportamiento del cliente
- **Enumeración de dispositivos BLE** — escaneo e identificación de periféricos BLE 5.0 cercanos en paralelo con la investigación Wi-Fi
- **Mapeo de topología de red en malla** — identificación de relaciones entre AP Mesh, canales de backhaul y configuraciones SSID ocultas
- **Investigación de protocolos IoT inalámbricos** — análisis del comportamiento de dispositivos IoT en ambas bandas Wi-Fi en entorno de laboratorio controlado
- **Educación en pruebas de penetración autorizadas** — plataforma de aprendizaje práctico de fundamentos de seguridad Wi-Fi en entornos autorizados

---

{{< alert "warning" >}}
**¿Es la primera vez que usas esta tarjeta?** Sigue nuestra guía paso a paso para principiantes, que cubre requisitos previos, configuración del firmware, tu primer escaneo 5G y todas las funciones clave.
[📖 Abrir manual de usuario en línea](/es/products/sdrlab/flipper-5g/flipper_5G_module.html)
{{< /alert >}}

{{< alert >}}
¿Necesitas cotización? [Contáctanos](/es/contact/)
{{< /alert >}}
