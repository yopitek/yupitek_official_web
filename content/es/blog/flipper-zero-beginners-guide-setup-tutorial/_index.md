---
title: "Guía de inicio para Flipper Zero: Desempaquetado, configuración, actualización de firmware y cinco funciones prácticas"
locale: es
hreflang_group: flipper-zero-beginners-guide-setup-tutorial
slug: flipper-zero-beginners-guide-setup-tutorial
published: 2026-08-10
author: Yupitek
category: Technical
tags:
  - Flipper Zero
  - Tutorial
hero_image: /static/img/flipper-zero/hero.webp
hero_alt: "Guía de inicio para Flipper Zero: Desempaquetado, actualización de firmware y prueba de cinco funciones | Yupitek"
seo_description: "¿Qué es Flipper Zero? Desde el desempaquetado, la configuración de microSD, la actualización de firmware con qFlipper, hasta la prueba práctica de las cinco funciones principales: RFID, Sub-GHz, NFC, IR y BadUSB. Una guía completa para iniciarse en Flipper Zero."
---

# Guía de inicio para Flipper Zero: Desempaquetado, configuración, actualización de firmware y cinco funciones prácticas

> TL;DR: Flipper Zero es una herramienta de exploración de hardware de mano que incluye RFID de 125 kHz, Sub-GHz, NFC, infrarrojos y BLE. Se conecta a un ordenador mediante USB-C para simular un teclado (BadUSB). Tras adquirirlo, instale primero la tarjeta microSD, actualice el firmware mediante qFlipper o la aplicación móvil y comience a utilizarlo leyendo tarjetas RFID y controlando dispositivos por infrarrojos. Utilice todas las funciones únicamente en **dispositivos de su propiedad o para los cuales tenga autorización**.

## ¿Qué es Flipper Zero? ¿Para quién es?

Flipper Zero es un dispositivo portátil de tamaño similar a la palma de la mano, posicionado como una «herramienta de exploración de hardware». No es un gadget de consumo general, sino un equipo diseñado para investigadores de ciberseguridad, principiantes en pruebas de penetración, creadores (Makers) e ingenieros de IoT, utilizado para leer, analizar y simular protocolos inalámbricos comunes y señales digitales.

El hardware principal incluye:

- **RFID de 125 kHz**: Lectura y simulación de tarjetas de acceso de baja frecuencia.
- **Inalámbrico Sub-GHz** (Chipset CC1101): Análisis de señales de mandos a distancia, puertas de garaje y sensores IoT en el rango de 300–928 MHz.
- **NFC (13.56 MHz)**: Lectura, escritura y simulación de tarjetas de alta frecuencia.
- **Infrarrojos (IR)**: Aprendizaje y reemisión de códigos de control remoto para televisores, aires acondicionados, etc.
- **BLE**: Emparejamiento y control mediante la aplicación móvil.
- **USB-C**: Conexión al ordenador para actualizar el firmware y simular un teclado (BadUSB / DuckyScript).
- **GPIO / iButton**: Llaves de contacto 1-Wire y expansión de hardware.

Lector ideal: Estudiantes que se preparan para investigar la seguridad inalámbrica, ingenieros que necesitan verificar la fiabilidad de sus propios sistemas de acceso o sensores, y creadores que desean comprender los principios del RFID/NFC. Si simplemente busca un «copiador de mandos a distancia», su función Sub-GHz puede servirle, pero verifique primero la legislación local y el contexto de uso.

## Desempaquetado y configuración inicial: Instale la microSD antes de encenderlo

Flipper Zero no incluye una tarjeta microSD de fábrica, pero se **recomienda encarecidamente** su uso para almacenar el firmware y los datos. Siga estos pasos:

1. **Prepare la tarjeta microSD**: Se recomienda una capacidad de 4 GB o superior, formateada en FAT32 (FAT16/FAT32/exFAT son válidos). Inserte la tarjeta en la ranura inferior del dispositivo con los **contactos metálicos hacia arriba**.
2. **Carga**: Conecte el dispositivo a un cargador o a un ordenador mediante USB-C y cárguelo completamente antes del primer uso.
3. **Encendido**: Mantenga pulsado el botón de retroceso (Back) en la parte trasera del dispositivo durante unos 3 segundos. La aparición de la animación del delfín indica que el encendido se ha completado.
4. **Verifique la versión del sistema**: Acceda a `Configuración → Acerca de` y anote la versión actual del firmware para el siguiente paso de actualización.

> Nota: Flipper Zero se enciende con la interfaz en inglés; algunas versiones de firmware de terceros ofrecen el idioma chino, pero **no se recomienda** que los principiantes utilicen firmware de terceros inicialmente. Familiarícese primero con el flujo de trabajo del firmware oficial antes de considerar otras opciones.

## Actualización del firmware: Versión de escritorio qFlipper y aplicación móvil

La actualización del firmware es el paso más importante para iniciarse en Flipper Zero: el fabricante corrige errores y añade soporte para nuevos protocolos de forma continua. El firmware antiguo podría no leer ciertas tarjetas o señales.

### Método 1: qFlipper para escritorio (Recomendado)

1. Descargue qFlipper para su plataforma correspondiente (Windows / macOS / Linux) desde el sitio web oficial de Flipper.
2. Conecte Flipper Zero al ordenador mediante USB-C y abra qFlipper.
3. Haga clic en el icono de llave inglesa (Controles avanzados) en la esquina superior derecha y seleccione «Canal de actualización de firmware».
4. Seleccione **Release (Estable)** y haga clic en Actualizar.
5. Espere a que finalice la actualización (aproximadamente 5–10 minutos); el dispositivo se reiniciará automáticamente.

### Método 2: Aplicación móvil

1. Instale la aplicación oficial Flipper Mobile (iOS / Android).
2. Active el Bluetooth en el teléfono y empareje el dispositivo con Flipper Zero (en el dispositivo: `Configuración → Bluetooth`).
3. Pulse Actualizar en la aplicación; la actualización se transferirá mediante BLE y tardará aproximadamente 10 minutos.

### ¿Cómo elegir el canal de firmware?

| Canal | Estabilidad | Público objetivo |
|---|---|---|
| Release (Estable) | Alta | **Los principiantes deben elegir siempre esta opción** |
| Release Candidate (RC) | Media | Usuarios que deseen probar nuevas funciones anticipadamente |
| Development (Desarrollo) | Baja | Desarrolladores y probadores |

> ⚠️ No desconecte el cable ni corte la alimentación durante el proceso de actualización. Si el dispositivo se queda atascado en la pantalla de inicio, puede entrar en el modo de recuperación para reinstalar el firmware (pulse Reset dos veces seguidas). Aunque el firmware de terceros (como Xtreme) ofrece funciones ampliadas, puede ser inestable; los principiantes deben utilizar primero la versión estable oficial.

## Prueba práctica de cinco funciones prácticas

### 1. RFID de 125 kHz: Lectura y simulación de tarjetas de baja frecuencia

Las tarjetas de acceso antiguas (125 kHz) suelen tener solo un código ID y carecen de mecanismos de verificación. Flipper Zero cuenta con una antena LF en la parte inferior; basta con acercar la tarjeta para leerla:

1. Menú principal → `RFID 125 kHz` → `Leer`.
2. Coloque la tarjeta plana cerca de la parte inferior del dispositivo. Una lectura correcta mostrará el UID y los datos.
3. Para simular, seleccione `Simular` tras la lectura, lo que permitirá utilizar el dispositivo como tarjeta temporal de sustitución.

### 2. Sub-GHz: Análisis de señales inalámbricas de 300–928 MHz

El transceptor CC1101 integrado puede capturar señales emitidas por mandos a distancia, puertas de garaje y sensores IoT:

1. Menú principal → `Sub-GHz` → `Leer Raw`.
2. Pulse el botón del mando a distancia; la pantalla mostrará la frecuencia y la forma de onda de la señal.
3. Una vez guardada, puede `Reproducir` la reemisión; también puede configurar manualmente la frecuencia para escanear la actividad inalámbrica en el entorno.

### 3. NFC: Lectura, escritura y simulación de tarjetas de 13.56 MHz

El módulo NFC es compatible con estándares comunes de 13.56 MHz y puede leer el UID y los bloques de datos de tarjetas de contacto como las tarjetas de transporte (por ejemplo, EasyCard). La capacidad de simularlas completamente depende del mecanismo de cifrado de la tarjeta:

1. Menú principal → `NFC` → `Leer`.
2. Coloque la tarjeta en la zona de感应 (inducción) de la parte trasera del dispositivo para leer la información.
3. Según el tipo de tarjeta, puede seleccionar `Simular` o `Escribir`.

### 4. IR: Aprendizaje y reemisión de controles remotos por infrarrojos

El dispositivo cuenta con emisor/receptor infrarrojo integrado, capaz de aprender los códigos de control remoto de televisores, aires acondicionados y proyectores, y volver a emitirlos:

1. Menú principal → `Infrarrojos` → `Aprender`.
2. Apunte la ventana infrarroja superior del dispositivo hacia el mando a distancia y pulse el botón. Una vez aprendido, asigne un nombre y guarde.
3. Posteriormente, en `Infrarrojos → Guardados`, podrá reemitir el código en cualquier momento.

### 5. BadUSB / DuckyScript: Simulación de teclado USB-C

Al conectarse a un ordenador, Flipper Zero puede simular un teclado USB y ejecutar scripts de DuckyScript (entrada automática de comandos):

1. Coloque el script `.txt` (con sintaxis DuckyScript) en la carpeta `badusb/` de la tarjeta microSD.
2. Conecte el dispositivo al ordenador objetivo mediante USB-C, acceda al menú principal → `BadUSB` y seleccione el script para ejecutarlo.

> ⚠️ **BadUSB es una función altamente sensible**: Los scripts se ejecutan en el ordenador mediante entrada de teclado, lo que equivale a «alguien sentado frente al ordenador escribiendo». Úselo únicamente en su propio ordenador o en entornos de prueba con autorización explícita.

## Recordatorio de uso legal (Obligatorio)

Flipper Zero es una herramienta legal, pero existen límites legales claros en su uso:

- **Copiar/simular tarjetas de acceso y mandos a distancia**: Solo se permite para sistemas de su propiedad o con autorización del administrador. Leer o simular sin autorización las tarjetas de acceso de terceros o los mandos de garaje puede implicar responsabilidad penal por violación de la intimidad, la Ley de Telecomunicaciones o leyes de protección de datos personales en Taiwán.
- **BadUSB**: Ejecutar scripts en el ordenador de otra persona sin autorización constituye un acto ilegal.
- **Interferencia de señales**: Interferir deliberadamente en dispositivos inalámbricos de terceros (como puertas de garaje) conlleva riesgos legales.

**El principio es sencillo: pruebe solo sus propios dispositivos o aquellos para los que tenga autorización por escrito.**

## Preguntas frecuentes (FAQ)

**P1: ¿Es obligatorio instalar una tarjeta microSD en Flipper Zero?**
No es obligatorio, pero se recomienda encarecidamente. La mayoría de las aplicaciones, bibliotecas de señales y scripts de BadUSB se almacenan en la microSD; sin la tarjeta, las funciones se verán significativamente limitadas.

**P2: ¿La actualización del firmware puede inutilizar el dispositivo (brick)?**
El riesgo con el firmware estable oficial es extremadamente bajo; si no se corta la alimentación ni se desconecta el cable durante la actualización, el proceso casi nunca falla. En caso de anomalía, puede reinstalar el firmware mediante el modo de recuperación.

**P3: ¿Se puede copiar una tarjeta EasyCard?**
La mayoría de las tarjetas de transporte de nueva generación tienen cifrado y protección de claves. Flipper Zero solo puede leer el UID o bloques no cifrados, por lo que no puede copiarlas completamente. Además, copiar tarjetas de transporte sin autorización es ilegal.

**P4: ¿Cuál es la diferencia entre Flipper Zero y un SDR (Radio Definida por Software)?**
Flipper Zero incluye un transceptor Sub-GHz diseñado para protocolos comunes (OOK/ASK/FSK, etc.), con una operación intuitiva. Un SDR (como HackRF o RTL-SDR) ofrece un rango de frecuencias más amplio y permite visualizar el espectro original, pero requiere un ordenador y conocimientos técnicos más profundos. Ambas son herramientas complementarias.

**P5: ¿Dónde puedo comprar Flipper Zero?**
Yupitek (Yuhé Technology) ofrece productos Flipper Zero y accesorios relacionados, además de asesoramiento técnico. Tras la compra, puede enviar un correo electrónico a sales@yupitek.com para consultar dudas sobre la configuración.

**P6: ¿Se puede instalar firmware de terceros?**
Sí, pero no se recomienda para principiantes. El firmware de terceros (como Xtreme) ofrece una interfaz mejorada y funciones adicionales, pero la estabilidad y la seguridad deben evaluarse por cuenta propia, y es posible perder el soporte de actualización del fabricante.

## Conclusión

La ruta de inicio con Flipper Zero es sencilla: **instale la microSD → actualice el firmware estable oficial → comience a jugar con la lectura de RFID y el control por IR → una vez familiarizado, explore Sub-GHz y BadUSB**. Es un punto de partida excelente para comprender los protocolos inalámbricos y la seguridad de hardware, pero recuerde siempre: cuanto más potente sea la herramienta, mayor debe ser la autodisciplina; pruebe únicamente dispositivos de los que tenga permiso.

Si necesita Flipper Zero o accesorios relacionados, no dude en enviar un correo electrónico a [sales@yupitek.com](mailto:sales@yupitek.com). Yupitek ofrece servicios de asesoramiento de productos y técnicos.