---
title: "Manual de usuario e instalación ilustrado de la Flipper Zero 5G Expansion Board (v2.0)"
description: "Esta guía es el manual de instalación y operación v2.0 para el módulo de expansión Flipper Zero 5G, equipado con diagramas isométricos de diseño de ingeniería en alta definición para una instalación sin complicaciones de antenas, ranuras y configuraciones de GPIO."
date: 2026-10-18
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-zero-5g-expansion-board-user-manual"
tags: ["Flipper Zero", "5G Expansion Board", "SDRLab", "Tutorial"]
categories: ["Técnico"]
author: "Yupitek"
lastmod: 2026-10-18
featureimage: "/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg"
hideFeatureImage: true
---

# Manual de usuario e instalación ilustrado de la Flipper Zero 5G Expansion Board (v2.0)

> **Destinatarios**: Clientes principiantes sin experiencia previa con este módulo.  
> **Principios de redacción**: Proporcionar diagramas explicativos de alta definición para todos los pasos propensos a errores o con terminología compleja, eliminando conjeturas basadas en texto para lograr una instalación guiada paso a paso sin complicaciones.

---

## 00. Desembalaje y lista de accesorios

¡Le damos la bienvenida al módulo de expansión Flipper Zero 5G! Antes de comenzar, verifique que su paquete contenga los siguientes accesorios.

![Desembalaje de componentes y accesorios](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg)
*Figura 1: Vista general de los accesorios incluidos al desembalar*

### ⚠️ Notas sobre la lista de accesorios
*   **El paquete estándar incluye**:
    1.  Módulo principal de la tarjeta de expansión 5G (5G Expansion Board) x 1
    2.  Antena de látigo de 433 MHz (antena corta negra) x 1
    3.  Antena activa cerámica GPS (antena cuadrada) x 1
    4.  Antena de parche de doble banda WiFi (antena plana negra) x 1
*   **No se incluye (debe prepararlos por su cuenta)**:
    *   **Consola Flipper Zero** (este módulo no incluye la consola principal)
    *   **Tarjeta de memoria MicroSD** (esencial para el funcionamiento del módulo, debe adquirirse por separado)

---

## 01. Conozca su módulo 5G

Antes de conectar las antenas o acoplar la consola principal, dedique un minuto a familiarizarse con las interfaces clave y la distribución del hardware en el módulo.

### Descripción de la interfaz frontal

![Diagrama etiquetado del frente del módulo](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_02_front_interface.jpg)
*Figura 2: Distribución y etiquetado del hardware frontal*

*   **Pantalla LCD (LCD Screen)**: Muestra el estado actual de la conexión, la dirección IP y el modo de funcionamiento.
*   **Interruptor de palanca (Toggle Switch)**: Controla la alimentación de la pantalla del módulo. Muévalo hacia arriba para encenderla.
*   **Ranura para tarjeta MicroSD (SD Card Slot)**: Se utiliza para almacenar los archivos de configuración del firmware del sistema y los datos de registro (Log).
*   **Ranura GPIO**: Conector hembra que se acopla a la parte superior de la consola Flipper Zero.
*   **Indicadores luminosos (LED Indicators)**: Muestran el estado de la alimentación y de la carga.

### Descripción de los puertos de antena laterales

![Diagrama etiquetado de los puertos de antena laterales](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_03_antenna_ports.jpg)
*Figura 3: Posición de los puertos de antena e impresiones de funciones*

*   **433M A**: Para conectar la antena de látigo de 433 MHz.
*   **GPS**: Para conectar la antena cerámica GPS.
*   **2.4G** y **2.4G/5G**: Para conectar la antena de parche de doble banda WiFi.

> ⚠️ **Recordatorio importante sobre las versiones del lote de envío**:  
> La posición de los puertos de antena puede variar ligeramente según el lote de producción, por ejemplo, las ubicaciones de los conectores GPS y WiFi podrían estar invertidas. **Es fundamental que se guíe por la etiqueta impresa real en la carcasa del módulo que ha recibido**. No realice la conexión de memoria para evitar una recepción de señal deficiente o daños en el hardware.

---

## 02. Guía de pasos de instalación (Step-by-Step)

### Paso 1 | Preparación e instalación de la tarjeta de memoria MicroSD

El módulo 5G requiere una tarjeta de memoria para almacenar las configuraciones.

1.  **Orientación de la tarjeta**: Introduzca la tarjeta en la ranura MicroSD con los contactos metálicos hacia abajo y presiónela suavemente hasta que encaje en su lugar.

![Detalle de la ranura para tarjeta MicroSD](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_07_sd_card_slot.jpg)
*Figura 4: Detalle de la orientación correcta para insertar la tarjeta MicroSD*

---

### Paso 2 | Instalación de las tres antenas

Atornille las tres antenas de la configuración estándar en los conectores de antena SMA correspondientes. Tenga cuidado de no aplicar demasiada fuerza, gírelas solo hasta que queden firmemente ajustadas.

![Diagrama de conexión de antenas](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_08_three_antenna_connection.jpg)
*Figura 5: Esquema de fijación de las tres antenas y sus rutas de acoplamiento*

| Tipo de antena | Puerto de antena correspondiente | Instrucciones de instalación |
| :--- | :--- | :--- |
| **Antena cerámica GPS** | **Puerto GPS** | Conector con base cerámica cuadrada y cable largo |
| **Antena de parche de doble banda WiFi** | **Puerto 2.4G/5G** | Antena de parche plana de color negro |
| **Antena de látigo de 433 MHz** | **Puerto 433M A** | Antena rígida corta de tipo látigo de color negro |

#### ⚠️ Advertencia sobre la orientación de la antena GPS
La antena GPS es direccional. Al instalarla, **el lado cerámico (que suele ser el lado opuesto al adhesivo de doble cara, o el lado sin texto) debe apuntar hacia arriba, hacia el cielo**. ¡De lo contrario, no se podrá establecer el posicionamiento con éxito!

![Comparación de la orientación de la antena GPS](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_09_gps_antenna_orientation.jpg)
*Figura 6: Comparación entre la colocación correcta (hacia el cielo) e incorrecta (hacia el suelo) de la antena GPS*

---

### Paso 3 | Acoplamiento con la consola Flipper Zero

Inserte el módulo 5G en los pines GPIO situados en la parte superior de la Flipper Zero.

1.  En primer lugar, **apague la Flipper Zero** para evitar que la conexión en caliente cause daños en el hardware.
2.  Alinee los pines GPIO de la parte superior de la Flipper Zero con la ranura en la parte inferior del módulo.

![Diagrama de alineación GPIO](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_10_gpio_alignment.jpg)
*Figura 7: Posición de acoplamiento y líneas de alineación de GPIO*

3.  Aplique una presión uniforme con ambas manos para **empujar el módulo por completo hacia abajo**.
4.  **Verificación de la nivelación**: Una vez completado, observe desde el lateral. El módulo debe quedar **completamente acoplado con la Flipper Zero, sin dejar ninguna holgura o espacio intermedio**.

![Confirmación de ajuste al insertar GPIO](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_19_gpio_insertion_flat.jpg)
*Figura 8: Estado de acoplamiento correcto, totalmente insertado y sin holguras*

---

### Paso 4 | Configuración de software en la Flipper Zero

Una vez realizado el acoplamiento, encienda la Flipper Zero y proceda a configurar los pines de software (GPIO Pin).

Tomando como ejemplo el firmware **Momentum**, acceda a la siguiente ruta para realizar los ajustes:

1.  **Encendido de la pantalla**: Mueva el interruptor de palanca ubicado en la parte frontal izquierda del módulo a la posición **UP**.
    ![Detalle del interruptor de pantalla en posición UP](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_16_toggle_switch_up.jpg)
    *Figura 9: Interruptor de palanca de la pantalla colocado en posición UP para activar la visualización*

2.  **Configuración de GPS Pin**:
    *   Ruta: `Protocol Settings` ➔ `GPIO Pin Settings` ➔ `GPS Pin`
    *   Valor: Cambie a **13** o **14** (según las instrucciones del manual o del envío de hardware).
3.  **Configuración de ESP32 Pin (funciones de WiFi/Bluetooth)**:
    *   Ruta: `Protocol Settings` ➔ `GPIO Pin Settings` ➔ `ESP32 Pin`
    *   Valor: Cambie a **15, 16**.
4.  **Configuración del módulo de radiofrecuencia de 433 MHz**:
    *   Acceda a `Sub-GHz` ➔ `Advanced Settings` ➔ Cambie Module a **External** (para habilitar la antena externa).

---

### Paso 5 | Carga y verificación de batería

Este módulo cuenta con una batería recargable integrada.

![Comparación y advertencia sobre los puertos USB-C](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_17_usb_ports_comparison.jpg)
*Figura 10: Comparación entre el puerto superior exclusivo para carga (CHARGE ONLY) y el puerto lateral exclusivo para grabación de firmware (FLASH ONLY)*

*   **Puerto USB-C superior**: **Exclusivo para carga** (etiquetado como CHARGE ONLY). ¡Asegúrese de conectar el cable en este puerto para cargar el dispositivo!
*   **Puerto USB-C lateral**: **Exclusivo para grabación de firmware** (etiquetado como FLASH ONLY). No lo utilice para la carga diaria, ya que no suministrará energía a la batería.

#### Estado de los indicadores LED de batería:
En el frente del módulo se encuentran 4 indicadores luminosos de batería que indican el nivel de carga restante.

![Explicación de los indicadores de batería](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_18_battery_led_indicators.jpg)
*Figura 11: Nivel de carga restante correspondiente a los 4 indicadores LED*

---

## 03. Lista de verificación de errores comunes (Resolución de problemas para principiantes)

Si su módulo no funciona correctamente, verifique uno a uno los siguientes elementos:

*   [ ] **¿Están los pines GPIO totalmente insertados hasta el fondo?** (El módulo y la parte superior de la Flipper Zero deben quedar perfectamente acoplados y sin espacios, consulte la Figura 8)
*   [ ] **¿Es correcta la orientación de la antena GPS?** (El lado cerámico debe apuntar hacia el cielo, consulte la Figura 6)
*   [ ] **¿Ha conectado las antenas en los puertos correctos?** (Las posiciones pueden variar según el lote, verifique el texto impreso en la carcasa, consulte la Figura 3)
*   [ ] **¿Ha colocado el interruptor de la pantalla en la posición UP?** (Consulte la Figura 9)

---

## 04. Actualización y grabación de firmware (Funciones avanzadas)

Cuando se publique una nueva versión oficial del firmware, deberá realizar la grabación del mismo a través del puerto USB-C lateral.

1.  Prepare un cable USB-C conectado a su computadora.
2.  **Paso crítico**: Al mismo tiempo que conecta el cable al **puerto USB-C lateral (FLASH ONLY)** del módulo, **mantenga presionado el botón de grabación** ubicado en la parte posterior o derecha del módulo para que el chip acceda al modo de grabación Boot.

![Botón de grabación de firmware y secuencia de inserción](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_20_boot_flash_sequence.jpg)
*Figura 12: Diagrama de la secuencia para mantener presionado el botón de grabación mientras se inserta el cable USB*
