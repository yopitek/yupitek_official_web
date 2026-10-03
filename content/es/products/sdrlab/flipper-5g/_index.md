---
title: "SDRLab Flipper Zero Tarjeta de Expansión 5G — Módulo de Seguridad Wi-Fi de Doble Banda"
description: "Tarjeta de expansión Flipper Zero 5G, RTL8720DN Wi-Fi doble banda (2.4+5GHz), BLE 5.0, firmware Deauth preinstalado, alimentado por GPIO, compatible con Momentum/Unleashed."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Expansión Flipper Zero", "5GHz", "Wi-Fi", "Deauth", "Investigación de seguridad"]
---

# SDRLab Flipper Zero 5G Expansión — Módulo de Investigación de Seguridad Wi-Fi de Doble Banda

> **Declaración de Uso Legal**: Esta placa de expansión está destinada exclusivamente a la investigación de ciberseguridad autorizada y a fines de investigación legal. Realizar pruebas en redes, dispositivos o infraestructuras que no sean de su propiedad o sin autorización por escrito es ilegal en la mayoría de los países. Asegúrese de cumplir con las normativas locales sobre el uso de frecuencias inalámbricas y utilice este producto de manera responsable y ética.

---

## I. Descripción del Producto

Una placa de expansión de investigación inalámbrica que se conecta a los pines GPIO traseros del Flipper Zero. Complementa las capacidades inalámbricas de su Flipper Zero (que originalmente solo opera en 2.4 GHz) añadiendo cuatro capacidades inalámbricas simultáneas:

- **Wi-Fi de doble banda 2.4 GHz + 5 GHz** (802.11 b/g/n/ax, Wi-Fi 6)
- **Bluetooth BLE 5.0**
- **Radiofrecuencia Sub-GHz de 433 MHz**
- **GPS activo**

Además, incluye una **pantalla TFT a color de 2.8 pulgadas**, una **batería recargable de 800 mAh con soporte para cambio en caliente**, **registro en microSD**, **cuatro conectores de antena SMA y cuatro antenas incluidas**, y viene con el **firmware ESP32 Marauder 5G preinstalado de fábrica**.

No es necesario comprar programadores externos ni compilar firmware manualmente. Conecte el dispositivo, configure tres parámetros y estará listo para usar.

---

## II. Características del Producto

### Cuatro capacidades inalámbricas en un solo dispositivo
- **Wi-Fi de doble banda 2.4 GHz + 5 GHz**: Escanea redes modernas de 5 GHz, superando la limitación de las placas antiguas que solo podían operar en 2.4 GHz.
- **Sub-GHz de 433 MHz (Módulo de radio A07, 10 dBm)**: Ofrece una alternativa para entornos donde la recepción de la radio integrada del Flipper es deficiente.
- **GPS activo**: Permite registrar coordenadas automáticamente durante el mapeo de redes (wardriving). Se alimenta del Flipper cuando está conectado y cambia automáticamente a la batería interna cuando se desconecta.
- **Bluetooth BLE 5.0**: Permite la enumeración de dispositivos BLE y el análisis de balizas, pudiendo realizarse simultáneamente con la investigación de Wi-Fi.

### Pantalla TFT a color de 2.8 pulgadas
Muestra directamente los resultados del escaneo, la intensidad de la señal, el nivel de batería y el uso de la microSD en la propia placa, eliminando la necesidad de depender de la terminal del ordenador. Incluye la interfaz de usuario de Marauder.

### Cuatro conectores de antena SMA, cuatro antenas incluidas
La carcasa trasera tiene serigrafiada claramente la correspondencia de los cuatro conectores:

| Serigrafía | Posición | Uso |
|---|---|---|
| `433M A` | Borde superior izquierdo | Radio de 433 MHz (Módulo A07, 10 dBm) |
| `GPS` | Borde superior derecho | Antena de GPS activo |
| `2.4G` | Ala izquierda | Wi-Fi 2.4 GHz |
| `2.4G/5G` | Ala derecha | Wi-Fi de doble banda 2.4 GHz + 5 GHz |

Los cuatro conectores son hembras SMA atornilladas independientes. **Se incluyen cuatro antenas, todas con una ganancia de 5 dBi**.

### Batería de 800 mAh con cambio en caliente
Viene equipada con una batería de polímero de litio de 800 mAh. Puede operar de forma independiente fuera del Flipper para capturar paquetes y, una vez finalizado, volver a insertarla en el dispositivo principal como placa de expansión. Se carga mediante USB-C, tardando aproximadamente 2 horas en cargarse completamente.

### Registro en microSD para análisis posterior
Compatible con tarjetas microSD formateadas en **FAT32 y de hasta 32 GB**. Los paquetes capturados se guardan en formato `.pcap`, compatibles con Wireshark para su análisis; las rutas de wardrive se exportan adicionalmente como `wardrive_*.csv`.

### Firmware Marauder 5G preinstalado de fábrica
Listo para usar fuera de la caja, sin necesidad de adquirir programadores adicionales. La placa conserva un puerto de grabación USB-C para que los usuarios avanzados puedan actualizar el firmware si lo desean.

### Pines dorados y protección contra picos de voltaje (TVS)
Todos los pines de señal están bañados en oro y cuentan con un diodo supresor de transitorios (TVS) integrado en cada pin, proporcionando protección contra picos de voltaje durante la conexión y desconexión del Flipper.

### Compatibilidad con ecosistemas de firmware
Compatible con personalizaciones como Momentum, Unleashed y Xtreme que incluyen aplicaciones WiFi Marauder y GPS.

---

## III. Especificaciones Técnicas

| Especificación | Valor / Descripción |
|---|---|
| **Chip Principal** | **Espressif ESP32-C5** (RISC-V) |
| **CPU** | Núcleo de alto rendimiento RISC-V, hasta 240 MHz, junto con un núcleo de bajo consumo (LP) para tareas en segundo plano |
| **Estándar Wi-Fi** | **IEEE 802.11 b/g/n/ax** (Wi-Fi 6), doble banda 2.4 GHz + 5 GHz |
| **Conector de Antena Wi-Fi** | **4 conectores hembra SMA**: 433M A / GPS / 2.4G / 2.4G+5G. **Incluye 4 antenas, todas de 5 dBi** |
| **Bluetooth** | **BLE 5.0** (⚠️ No soporta Bluetooth Clásico / BR-EDR) |
| **Sub-GHz** | Módulo de radio 433 MHz A07, salida de **10 dBm** |
| **GNSS** | Módulo de GPS activo, **cambio automático de alimentación** (se alimenta del Flipper cuando está conectado, usa la batería interna cuando está desconectado) |
| **Pantalla** | **TFT a color de 2.8 pulgadas**, con interfaz de usuario Marauder integrada |
| **Batería** | **800 mAh de polímero de litio**, con soporte para cambio en caliente |
| **Carga** | USB-C, 5V / 2A, aproximadamente **2 horas** para carga completa (puerto frontal superior) |
| **Salida de Alimentación al Flipper** | 5V / 2.4A |
| **Almacenamiento** | **microSD, formato FAT32, hasta 32 GB** (no soporta exFAT / NTFS) |
| **Interfaz de Conexión** | Pines GPIO estándar del Flipper Zero (**2x8 pines**), pines dorados + protección TVS por pin |
| **Firmware Preinstalado** | **ESP32 Marauder 5G** (código abierto, preinstalado de fábrica) |
| **Compatibilidad de Firmware** | Momentum, Unleashed, Xtreme |
| **Material de la Carcasa** | Plástico impreso en 3D |
| **Colores Disponibles** | Negro / Blanco / Transparente / Rojo / Azul |
| **Dimensiones** | **90 × 58 × 15 mm** (sin incluir antenas) |

### Accesorios Incluidos
- 1 Unidad principal (ensamblada, con carcasa impresa en 3D y pantalla de 2.8 pulgadas)
- 4 Antenas (todas de 5 dBi): 1x `2.4G`, 1x `2.4G+5G` (doble banda), 1x `433M A`, 1x `GPS`
- Conector de pines GPIO para Flipper

### De Compra Separada
- **Flipper Zero Principal** (esta placa es una expansión, no incluye el dispositivo principal)
- **Tarjeta de memoria microSD** (FAT32, hasta 32 GB)

---

## IV. Primeros Pasos: Tres Parámetros Esenciales

La placa viene con el firmware preinstalado y no requiere programación adicional. Una vez conectada al Flipper, solo debe configurar tres pines:

| Función | Ruta de Configuración | Valor |
|---|---|---|
| **GPS** | Momentum → Ajustes de Protocolo → Ajustes de Pines GPIO → **Pin GPS** | **13 o 14** |
| **ESP32 (WiFi / BLE / Marauder)** | Igual que arriba → **Pin ESP32** | **15, 16** |
| **Sub-GHz 433MHz** | Flipper → Sub-GHz → Ajustes Avanzados → **Módulo** | **Externo** |

> ⚠️ **El GPS y el ESP32 utilizan pines UART diferentes y no deben configurarse en el mismo pin**, de lo contrario, el GPS y el Wi-Fi no responderán.

Después de completar la configuración, reinicie el Flipper. En `Apps → GPIO` podrá ver las aplicaciones correspondientes de WiFi Marauder y GPS.

**La microSD debe formatearse manualmente a FAT32** y debe confirmar que el almacenamiento de PCAP está habilitado en `Device → Settings`.

---

## V. Entornos de Aplicación

- **Escaneo de Wi-Fi de doble banda**: Enumeración pasiva de redes 2.4 GHz y 5 GHz; captura de SSID, BSSID, canal, RSSI, tipo de cifrado y clientes conectados.
- **Captura de handshakes WPA**: Sniffing de paquetes de handshake EAPOL/PMKID, utilizado para auditorías de seguridad en redes autorizadas.
- **Pruebas de Deauth**: Envío de paquetes Deauth para probar la resiliencia de la red, exclusivo para redes propias o autorizadas.
- **Enumeración de dispositivos BLE**: Escaneo e identificación de dispositivos periféricos BLE 5.0 cercanos, compatible con la investigación de Wi-Fi simultánea.
- **Mapeo de topología de red Wardrive**: Registros de Wi-Fi y dispositivos marcados con GPS, exportados en CSV para análisis posterior.
- **Investigación de radiofrecuencia 433 MHz**: Operación a través del menú Sub-GHz del Flipper, ideal para entornos donde la recepción integrada del Flipper es deficiente.
- **Simulación de Evil Portal**: Diseño de prototipos y pruebas de páginas de entrada en entornos autorizados.
- **Investigación de protocolos inalámbricos IoT**: Análisis del comportamiento de dispositivos IoT en doble banda en entornos de laboratorio controlados.

---

## VI. Limitaciones Conocidas (Por favor, tenga en cuenta)

- **La estabilidad del Deauth en 5 GHz depende de la versión del firmware**. El firmware Marauder de código abierto para el ESP32-C5 está mejorando continuamente el soporte para deauth en 5 GHz. Se recomienda realizar pruebas de deauth principalmente en **2.4 GHz**; para 5 GHz, se sugiere utilizar principalmente escaneo, monitoreo de señales y registro de wardrive. El rendimiento real depende de la versión del firmware instalada.
- **La antena GPS tiene directividad**, a pesar de que el producto se anuncia como omnidireccional. Oriente la antena hacia el cielo despejado para obtener una posición precisa. El primer arranque en frío puede tardar varios minutos en descargar los datos efemérides de los satélites. El rendimiento en interiores es deficiente; se recomienda su uso al aire libre o cerca de ventanas.
- **La hora reportada por el GPS es UTC+0**, y el menú del firmware no tiene opción de ajuste de zona horaria. Para la hora de Taiwán (UTC+8), debe sumar 8 horas manualmente.
- **La microSD solo soporta FAT32**, no soporta exFAT ni NTFS, y tiene un límite de capacidad de 32 GB.
- **El GPS y el ESP32 utilizan pines UART diferentes** (GPS: 13 o 14; ESP32: 15, 16). No deben configurarse en el mismo pin, de lo contrario, el GPS y el Wi-Fi no responderán.
- **El Bluetooth solo soporta BLE 5.0**. El hardware ESP32-C5 no cuenta con Bluetooth Clásico (BR/EDR), por lo que no puede emparejarse con altavoces, auriculares o sistemas de coche tradicionales.
- **Los dos puertos USB-C tienen funciones distintas**: El puerto frontal superior es para carga (5V/2A); el puerto frontal izquierdo es exclusivamente para la grabación de firmware y no carga la batería. Conectar el cable al puerto incorrecto no cargará el dispositivo, pero tampoco dañará el equipo principal.
- **Cambio automático de alimentación del GPS**: Se alimenta del Flipper cuando está conectado y usa la batería interna cuando está desconectado. Puede haber un reinicio breve durante el cambio, lo cual es un comportamiento normal.

---

## VII. Especificaciones Pendientes de Confirmación

Los siguientes elementos carecen de documentación oficial escrita suficiente por parte del fabricante en este momento. Por esta razón, no se especifican valores numéricos en esta página para evitar engaños:

| Elemento | Estado |
|---|---|
| Potencia de transmisión Wi-Fi (dBm) | En confirmación con el fabricante |
| Corriente de trabajo activa (mA) | En confirmación con el fabricante |
| Rango de temperatura de operación | En confirmación con el fabricante |
| Número de segmentos del indicador de batería (individual o múltiple) | En verificación con unidad real |

Estos elementos se actualizarán una vez confirmados.

---

**Enlace a la página del producto**: https://yupitek.com/zh-tw/products/sdrlab/flipper-5g/
**Manual de uso completo**: https://doczhtw.yupitek.com/sdrlab/expansion/5g-board/