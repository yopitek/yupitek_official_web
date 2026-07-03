---
title: "¿Qué es la Inyección de Paquetes? Prueba la Compatibilidad de tu Adaptador WiFi con Kali Linux"
description: "Entiende la inyección de paquetes WiFi, por qué necesitas adaptadores específicos y cómo probar tu ALFA Network con aireplay-ng en Kali Linux."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["inyección-paquetes", "aireplay-ng", "Kali-Linux", "adaptador-WiFi", "ALFA-Network"]
featureimage: "/images/blog/packet-injection-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "¿Qué es la inyección de paquetes WiFi?"
    answer: "La inyección de paquetes es la capacidad de la tarjeta de transmitir tramas 802.11 arbitrarias directamente al medio inalámbrico, permitiendo que herramientas como aireplay-ng construyan y envíen tramas de gestión, control y datos."
  - question: "¿Por qué la mayoría de las tarjetas no pueden inyectar paquetes?"
    answer: "La limitación está en el controlador, no en el hardware. Los controladores de consumo validan las tramas salientes según un modelo de operación estándar; se necesita que el controlador habilite explícitamente la ruta TX sin procesar de mac80211."
  - question: "¿Cómo probar si la tarjeta admite inyección de paquetes?"
    answer: "Primero activa el modo monitor, luego ejecuta aireplay-ng --test wlan0mon. Si la salida muestra Injection is working!, está confirmado. Una tasa de éxito del 80% o superior es fiable."
  - question: "¿Qué tarjetas ALFA admiten inyección de paquetes?"
    answer: "AWUS036ACH (RTL8812AU), AWUS036AXML (MT7921AUN) y AWUS036ACM (MT7612U) la admiten completamente. Con el controlador correcto funcionan en Kali Linux."
  - question: "¿Cómo mejorar una tasa de éxito de inyección inferior al 50%?"
    answer: "Acércate al AP objetivo, bloquea la interfaz de monitor al mismo canal, verifica la configuración de TX Power y comprueba que el controlador sea la versión de aircrack-ng y no la integrada en la distribución."
---La inyección de paquetes es la capacidad de la tarjeta de transmitir tramas 802.11 arbitrarias, limitada por el controlador y no por el hardware. Las tarjetas ALFA con chipsets RTL8812AU, MT7612U y MT7921AUN, con el controlador de aircrack-ng, ofrecen soporte completo.

{{< tldr >}}
La inyección de paquetes es la capacidad de la tarjeta de transmitir tramas 802.11 arbitrarias, limitada por el controlador y no por el hardware. Las tarjetas ALFA con chipsets RTL8812AU, MT7612U y MT7921AUN, con el controlador de aircrack-ng, ofrecen soporte completo.
{{< /tldr >}}


## ¿Qué es la Inyección de Paquetes?

La inyección de paquetes permite al adaptador inalámbrico transmitir tramas 802.11 arbitrarias, y es la capacidad central para ataques de deautenticación y captura de handshakes. Requiere un chipset y un controlador compatibles para funcionar.

La inyección de paquetes — formalmente conocida como **inyección de tramas 802.11** — es la capacidad de un adaptador inalámbrico para transmitir tramas 802.11 arbitrarias en un medio inalámbrico, incluyendo tramas que no se originan en la propia pila de red del adaptador. En operación normal, un controlador inalámbrico construye y transmite únicamente las tramas que el sistema operativo ha generado legítimamente: solicitudes de asociación, tramas de datos para redes conectadas, y similares. La inyección de paquetes omite estas restricciones, permitiendo que una herramienta como `aireplay-ng` construya y envíe cualquier tipo de trama — de gestión, control o datos — con contenido arbitrario, direcciones de origen y destino.

Esta capacidad es esencial para varias clases de evaluación de seguridad inalámbrica:

- **Aceleración de captura de handshakes WPA/WPA2** — Enviar tramas de deautenticación fuerza a los clientes a reautenticarse, generando un nuevo handshake de 4 pasos que puede capturarse y analizarse offline.
- **Verificación de handshakes WPA** — Confirmar que un archivo de handshake capturado está completo y es utilizable para cracking offline.
- **Ataques de reproducción** — Reproducir paquetes ARP capturados para generar tráfico IV (vector de inicialización) para cracking WEP (entornos de prueba heredados).
- **Construcción de AP evil twin / rogue** — Inyectar tramas de beacon y respuesta de sondeo para simular puntos de acceso.
- **Pruebas de DoS** — Evaluar cómo responde una red a las inundaciones de deautenticación en condiciones de prueba autorizadas.

> **Aviso legal:** La inyección de paquetes contra redes o dispositivos que no son de tu propiedad o para los que no tienes permiso escrito explícito para probar es ilegal en la mayoría de las jurisdicciones. Todas las técnicas descritas en este artículo están destinadas únicamente para pruebas de penetración autorizadas, investigación de seguridad en tu propio equipo y estudio académico.

---

## Por Qué la Mayoría de los Adaptadores No Pueden Inyectar Paquetes

La limitación no es principalmente el hardware — es el **controlador**. Los controladores inalámbricos estándar para adaptadores de consumo están escritos para cumplir con el modelo de operación normal del estándar 802.11. El controlador valida las tramas salientes, aplica el estado de asociación y rechaza tramas que no se ajustan al flujo esperado.

Para soportar la inyección de paquetes, un controlador debe exponer una ruta de transmisión de tramas en bruto que omita estas verificaciones. El subsistema **mac80211** del kernel proporciona esta capacidad a través del indicador `IEEE80211_HW_SUPPORTS_RAW_TX`, pero solo si el controlador lo habilita explícitamente. La mayoría de los controladores provistos por los fabricantes para adaptadores de consumo no habilitan TX en bruto — no existe un caso de uso de consumo que lo requiera, y habilitarlo introduce potencial de uso indebido.

Además, algunos chipsets usan **firmware propietario** que maneja la capa MAC internamente, haciendo imposible para el controlador del host inyectar tramas arbitrarias aunque el controlador lo desee. Esto es común en chips Broadcom e Intel diseñados para laptops empresariales o de consumo.

---

## Chipsets que Soportan Inyección de Paquetes

Los siguientes chipsets tienen soporte de inyección de paquetes bien establecido en Kali Linux y se usan en adaptadores ALFA Network:

### Realtek RTL8812AU

El chipset más popular para pruebas de penetración a partir de 2024–2026. Doble banda (2.4/5 GHz), 802.11ac, y respaldado por el controlador comunitario `rtl8812au` mantenido en el repositorio GitHub de aircrack-ng. Tanto el modo monitor como la inyección funcionan de manera confiable.

### Mediatek MT7612U

Chipset 802.11ac de doble banda con un controlador bien mantenido integrado en el kernel (`mt76`). El modo monitor y la inyección están soportados en el kernel principal, lo que significa que no se necesita instalación de controlador fuera del árbol en la mayoría de las versiones actuales de Kali Linux.

### Mediatek MT7921AUN (Wi-Fi 6E)

El chipset más nuevo de esta lista, usado en el AWUS036AXML. Soporta tribanda 2.4/5/6 GHz con 802.11ax. El controlador `mt7921u` requiere kernel 5.18 o posterior. El soporte de modo monitor e inyección está confirmado, pero el controlador es más nuevo y puede tener problemas de casos extremos en distribuciones más antiguas.

---

## Probar la Inyección de Paquetes con aireplay-ng

Antes de depender de la inyección en una prueba real, siempre verifica que tu combinación específica de adaptador y controlador funciona correctamente. El soporte de inyección varía según la versión del kernel y la revisión del controlador.

### Prerrequisitos

Tu adaptador ya debe estar en modo monitor. Si no lo está, actívalo primero:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirma que la interfaz de monitor existe:

```bash
iwconfig
# Busca: Mode:Monitor
```

### Ejecutar el test de inyección

```bash
sudo aireplay-ng --test wlan0mon
```

### Salida exitosa

```
09:15:34  Trying broadcast probe requests...
09:15:34  Injection is working!
09:15:36  Found 3 APs

09:15:36  Trying directed probe requests...
09:15:36   AA:BB:CC:DD:EE:01 - channel: 6 - 'HomeNetwork'
09:15:37  Ping (min/avg/max): 1.153ms/5.464ms/12.214ms Power: -62
09:15:37  29/30: 96%

09:15:37   AA:BB:CC:DD:EE:02 - channel: 11 - 'OfficeWiFi'
09:15:38  Ping (min/avg/max): 2.101ms/6.322ms/14.881ms Power: -71
09:15:38  28/30: 93%
```

Una configuración de inyección funcional muestra **"Injection is working!"** seguido de porcentajes exitosos de ping a puntos de acceso cercanos. Los valores por encima del 80% son generalmente confiables. Los valores por debajo del 50% sugieren interferencia, problemas de distancia o problemas con el controlador.

### Salida fallida

```
09:15:34  Trying broadcast probe requests...
09:15:36  No Answer...
09:15:36  Injection is working! (RTL)
09:15:36  Trying directed probe requests...
09:15:37   AA:BB:CC:DD:EE:01 - channel: 6 - 'HomeNetwork'
09:15:39  Failed!
```

O, en escenarios de fallo más completo:

```
09:15:34  Trying broadcast probe requests...
09:15:46  No Answer...
09:15:46  Injection is NOT working!
```

"Injection is NOT working!" es un fallo definitivo. El adaptador no soporta inyección o el controlador no está instalado correctamente.

---

## Adaptadores ALFA que Soportan Inyección de Paquetes

Todos los modelos principales de adaptadores [ALFA Network](/es/products/alfa/) soportan inyección de paquetes cuando se usan con el controlador correcto en Kali Linux:

| Modelo | Chipset | Banda | Soporte de Inyección |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | 2.4 / 5 GHz | ✅ Completo |
| AWUS036AXML | MT7921AUN | 2.4 / 5 / 6 GHz | ✅ Completo (kernel 5.18+) |
| AWUS036ACM | MT7612U | 2.4 / 5 GHz | ✅ Completo |

---

## Fallos Comunes en el Test de Inyección y Sus Soluciones

### "Injection is NOT working!" inmediatamente después de iniciar el modo monitor

La causa más común es NetworkManager o wpa_supplicant todavía ejecutándose en segundo plano. Termínalos y vuelve a intentarlo:

```bash
sudo airmon-ng check kill
sudo airmon-ng stop wlan0mon
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

### Porcentaje de éxito bajo (por debajo del 50%)

- **Distancia:** Acércate a un punto de acceso cercano y vuelve a probar.
- **Incompatibilidad de canal:** Fija tu interfaz de monitor al mismo canal que el AP que estás probando: `sudo iwconfig wlan0mon channel 6`
- **Problemas del controlador:** Reinstala el controlador fuera del árbol principal. Para RTL8812AU: clona desde `https://github.com/aircrack-ng/rtl8812au` y ejecuta `sudo make dkms_install`.

### El módulo del kernel no se carga

```bash
sudo modprobe -r rtl8812au
sudo modprobe rtl8812au
dmesg | tail -20
```

Verifica `dmesg` para mensajes de error sobre el módulo. Los archivos de firmware faltantes son un problema común — instala `firmware-linux-nonfree` o el paquete de firmware específico del chipset.

### El adaptador no aparece después de conectarlo

```bash
lsusb
dmesg | tail -30
```

Si `lsusb` muestra el dispositivo pero no aparece ninguna interfaz inalámbrica en `ip link`, el controlador falló al vincularse. Esto generalmente significa que el controlador no está instalado o que el módulo del kernel falló al cargar.

---

## Casos de Uso: Aplicar la Inyección en Pruebas Autorizadas

### Captura de Handshake WPA2

El uso más común de inyección en pentesting profesional. Comienza a capturar en el canal del AP objetivo con airodump-ng, luego envía tramas de deauth con aireplay-ng para forzar una reconexión del cliente:

```bash
# Terminal 1: Capturar
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w handshake wlan0mon

# Terminal 2: Deauth (enviar 5 tramas de deauth a un cliente específico)
sudo aireplay-ng --deauth 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
```

Cambia al Terminal 1 y observa el mensaje `WPA handshake: AA:BB:CC:DD:EE:FF` en la esquina superior derecha de airodump-ng.

### Pruebas de Deautenticación (Evaluación DoS)

Los evaluadores de seguridad prueban la resiliencia inalámbrica enviando inundaciones de deauth para evaluar si los clientes se reasocian de forma segura y si el AP registra o mitiga el ataque. Siempre se realiza bajo una declaración de trabajo firmada.

---

{{< faq >}}

## Uso Responsable

La inyección de paquetes es una capacidad poderosa. Sus aplicaciones legítimas en pruebas de penetración autorizadas están bien establecidas — captura de handshakes, verificación de controles de seguridad inalámbrica y prueba del comportamiento del cliente. Su uso indebido es tanto dañino como ilegal.

Siempre asegúrate de contar con:
- Autorización escrita del propietario de la red antes de realizar pruebas
- Una declaración de trabajo claramente delimitada que incluya pruebas inalámbricas
- Conocimiento de las leyes locales que rigen las pruebas de seguridad inalámbrica

Las herramientas descritas en este artículo (aireplay-ng, airodump-ng, aircrack-ng) están incluidas en Kali Linux específicamente para pruebas de seguridad autorizadas. Úsalas en consecuencia.

---

Para adaptadores inalámbricos con soporte confirmado de inyección de paquetes, explora la [gama de productos ALFA Network en Yopitek](/es/products/alfa/) — distribuidor autorizado ALFA Network.

## Referencias

1. [Sitio y documentación oficial de aircrack-ng](https://www.aircrack-ng.org/)
2. [Manual de uso de aireplay-ng](https://www.aircrack-ng.org/doku.php?id=aireplay-ng)
3. [Documentación oficial de Kali Linux](https://www.kali.org/docs/)
4. [Documentación del subsistema mac80211 de Linux](https://wireless.wiki.kernel.org/en/developers/Documentation/mac80211)
5. [Recursos del estándar IEEE 802.11](https://standards.ieee.org/ieee/802.11/)