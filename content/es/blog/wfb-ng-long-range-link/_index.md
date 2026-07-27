---
title: "ALFA AWUS036ACH: Enlace digital de largo alcance para drones con wfb-ng — Tutorial Open Source (2026)"
description: "Con la tarjeta ALFA AWUS036ACH y el software open source wfb-ng, construya un enlace de video digital y telemetría MAVLink de bajo retardo y cifrado para drones. Lista completa de hardware, configuración de Raspberry Pi y solución de problemas de alimentación."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "AWUS036ACH", "wfb-ng", "RTL8812AU", "videotransmisión-digital", "FPV", "monitor-mode", "packet-injection", "MAVLink", "Raspberry-Pi", "enlace-largo-alcance", "telemetría"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "¿En qué se diferencia wfb-ng del WiFi normal?"
    answer: "El WiFi normal requiere asociación (association) y confirmación ACK, lo que es ineficiente y de alta latencia en distancias largas. wfb-ng utiliza inyección de paquetes raw (raw packet injection), evitando el mecanismo de conexión 802.11 y empleando FEC (corrección directa de errores) para combatir la pérdida de paquetes, logrando una latencia de extremo a extremo del orden de decenas de milisegundos."
  - question: "¿Por qué la tarjeta ALFA en el dron necesita alimentación independiente?"
    answer: "La AWUS036ACH consume mucha corriente instantánea durante la transmisión (TX). Si se conecta directamente al puerto USB 2.0 de una Raspberry Pi, la alimentación insuficiente provocará reinicios del puerto de la tarjeta de red, cortes del enlace y corrupción de paquetes. Se recomienda usar un BEC de 5V para alimentación independiente y conectar un capacitor de 470µF de baja ESR entre +5V y GND para filtrar."
  - question: "No hay video ni telemetría tras la conexión, ¿qué hago?"
    answer: "La causa más común es que las claves no coincidan: verifique que drone.key (a bordo) y gs.key (estación terrestre) sean del mismo par. En segundo lugar, confirme que wifi_channel y link_domain sean idénticos en ambos extremos. Use journalctl -xu wifibroadcast@gs para consultar los registros en tiempo real."
  - question: "¿Es obligatorio usar ALFA AWUS036ACH para wfb-ng?"
    answer: "Cualquier tarjeta con chip RTL8812AU funciona en teoría, pero la AWUS036ACH es el hardware probado oficialmente por el proyecto wfb-ng, con el soporte de controladores más estable. En escenarios de alta potencia y largo alcance, el diseño de potencia de ALFA y sus antenas desmontables ofrecen ventajas significativas."
---
> Autor: Equipo técnico de Yupitek (distribuidor autorizado de ALFA Network en Taiwán)
> Público objetivo: Entusiastas de drones, makers, investigadores de seguridad, desarrolladores de drones para agricultura e inspección
> Dificultad: ★★★☆☆ (requiere conocimientos básicos de Linux y control de vuelo)

{{< tldr >}}
wfb-ng es un software open source que convierte tarjetas WiFi como la **ALFA AWUS036ACH** con soporte de monitor mode en un enlace de radio de largo alcance para drones, permitiendo construir una transmisión de video y telemetría MAVLink de bajo retardo y cifrada.
{{< /tldr >}}

---

## 1. ¿Por qué construir un enlace de video digital con una tarjeta ALFA?

Si ha usado FPV analógico tradicional (5.8 GHz), seguro conoce esa «antena de nieve»: la señal se llena de estática al encontrar obstáculos, la imagen se degrada al alejarse y, lo peor, **cualquiera con un receptor puede ver su señal** — sin cifrado ni telemetría de retorno.

Nuestro equipo ha montado enlaces para clientes de agricultura, inspección y formación en seguridad durante el último año, y descubrimos una necesidad recurrente: **¿podemos usar una tarjeta USB ALFA común, con software open source, para construir un enlace de largo alcance «digital, cifrado y simultáneo para video + telemetría»?**

La respuesta es sí, y es más sencillo de lo que cree.

Comparado con el FPV analógico tradicional, usar una tarjeta ALFA con **wfb-ng** ofrece ventajas abrumadoras:

- **Bajo retardo**: el modo de inyección WiFi raw evita el ACK y el handshake de 802.11, logrando una latencia de extremo a extremo de decenas de milisegundos, comparable al FPV analógico.
- **Cifrado digital**: los paquetes de video y telemetría se cifran con libsodium; nadie podrá descifrar su señal sin la clave.
- **Multiplexación en un solo enlace**: con la misma tarjeta y frecuencia, puede transmitir **simultáneamente**:
  - Video en tiempo real (RTP / RTSP)
  - Telemetría MAVLink (bidireccional, controlador ↔ estación terrestre)
  - Un túnel TCP/IP (para VPN, SSH, transferencia de archivos)
- **Diversidad de transmisión (TX diversity)**: se pueden usar múltiples tarjetas para diversidad en transmisión, mejorando la robustez ante obstrucciones.
- **Open source y personalizable**: la tarjeta ALFA AWUS036ACH con wfb-ng ofrece un costo total muy inferior a los sistemas de video digital comerciales (DJI O3 / Walksnail, etc.), y **todo es open source y personalizable**.

{{< alert "circle-info" >}}
Nota: Este artículo no pretende «reemplazar» el sistema de video original de DJI, sino ofrecer una ruta open source práctica para quienes deseen **controlar su propio enlace, tener una redundancia secundaria o construir cargas personalizadas**.
{{< /alert >}}

---

## 2. ¿Qué es esto? Introducción a wfb-ng

**wfb-ng** (Wireless Fibre / WiFi Broadcast – next generation) es un proyecto open source de FPV digital y telemetría. Su idea central es brillante:

> No usa WiFi como una «red», sino como una «radio».

El 802.11 convencional, diseñado para redes de área local, requiere asociación (association), confirmación ACK y retransmisiones — mecanismos que en escenarios de larga distancia, movilidad y señal débil ralentizan la transmisión y reducen el alcance. wfb-ng utiliza en su lugar **inyección de paquetes WiFi raw (raw WiFi injection)**:

- La tarjeta entra en **monitor mode**, sin «conectarse» a nada.
- Inyecta paquetes WiFi de bajo nivel directamente, **sin ACK ni retransmisiones** (usa FEC para corrección de errores).
- Evita las limitaciones de distancia y latencia del 802.11 convencional, llevando el alcance al límite del hardware.

En resumen, convierte una tarjeta USB común en un par de «radios digitales» capaces de transportar video RTP, telemetría MAVLink e incluso un túnel IP.

- Página del proyecto (GitHub): https://github.com/svpcom/wfb-ng.git
- Ampliamente usado en el ecosistema PX4 / ArduPilot para video digital DIY, con una comunidad activa; también es un enlace open source común en la comunidad de drones ucraniana.

---

## 3. El protagonista: ALFA AWUS036ACH

La «radio» de este enlace es la **ALFA AWUS036ACH**.

Utiliza el chip **Realtek RTL8812AU**, compatible con **802.11ac (WiFi 5)** , **doble banda 2.4 GHz / 5 GHz** , interfaz USB 3.0 Type-C y antenas desmontables (RP-SMA). Lo más importante: **el hardware probado oficialmente por wfb-ng usa AWUS036ACH en ambos extremos en modo 5 GHz**. Es decir, es el modelo con el soporte de controladores más estable verificado por los autores del proyecto.

¿Por qué elegirla? Tres razones clave:

1. **Potencia suficiente**: el diseño de alta potencia de ALFA, combinado con antenas externas de alta ganancia, ofrece un rendimiento en largo alcance muy superior al de las tarjetas integradas en portátiles.
2. **Monitor mode + inyección**: el RTL8812AU, con el controlador parcheado (ver más abajo), soporta de forma estable monitor mode e inyección de paquetes raw, requisito imprescindible para wfb-ng.
3. **Versátil y duradera**: interfaz USB, válida tanto para el dron como para la estación terrestre; si una tarjeta se daña, basta con reemplazarla.

{{< alert "triangle-exclamation" >}}
**Atención**: wfb-ng necesita un **controlador parcheado específico** (como `rtl88xxau_wfb`). Los controladores integrados en Linux no pueden entrar en el modo de inyección que wfb-ng requiere. Consulte la instalación en las secciones «Lista de software» y «Configuración paso a paso».
{{< /alert >}}

---

## 4. Lista de hardware (Hardware List)

El enlace completo se divide en dos grupos: **a bordo del dron (Drone)** y **estación terrestre (Ground Station)**.

### A bordo del dron (Drone)

| Elemento | Modelo recomendado / Descripción |
|---|---|
| Computadora de a bordo | Raspberry Pi 3B / 3B+ / Zero 2 W / 4 (a elección; para 1080p se recomienda **Pi 4 o Zero 2 W**) |
| Cámara | Raspberry Pi Camera (interfaz CSI) o Logitech C920 (interfaz USB) |
| Módulo WiFi | **ALFA AWUS036ACH** (o cualquier tarjeta con chip RTL8812AU) |
| Alimentación | **BEC de 5V** (para alimentación independiente de la tarjeta; ver «Avisos importantes») |
| Capacitor de filtro | **470µF de baja ESR** (conectado entre +5V y GND de la tarjeta) |
| Controlador de vuelo | Pixhawk (protocolo MAVLink, conectado por UART a la computadora de a bordo) |

### Estación terrestre (Ground Station)

| Elemento | Modelo recomendado / Descripción |
|---|---|
| Computadora | Linux (Ubuntu / Debian x86-64) u otra Raspberry Pi |
| Módulo WiFi | **ALFA AWUS036ACH** |
| Software de monitoreo | Equipo que ejecute **QGroundControl** (puede ser la misma computadora) |

> Nota: Si solo necesita **recepción (RX)** , cualquier tarjeta que soporte monitor mode sirve, incluso un router con OpenWRT. No obstante, la configuración de este artículo se basa en la AWUS036ACH.

---

## 5. Lista de software (Software List)

### Sistemas operativos

- **Raspberry Pi OS** / **Debian** / **Ubuntu** (kernel Linux ≥ 4.x)

### Proyecto principal

- **wfb-ng** (svpcom/wfb-ng): programa principal de video digital / telemetría
- **Controlador parcheado**:
  - RTL8812AU → `svpcom/rtl8812au` (rama **v5.2.20**, instalación con dkms)
  - RTL8812EU → `svpcom/rtl8812eu`
  - Tras cargar el controlador, la tarjeta aparecerá como `rtl88xxau_wfb` (o `rtl8812eu`)

### Paquetes dependientes del sistema

```bash
sudo apt update
sudo apt install -y \
  python3-all libpcap-dev libsodium-dev libevent-dev \
  python3-pip python3-pyroute2 python3-twisted python3-serial \
  python3-all-dev python3-venv iw socat debhelper dh-python \
  fakeroot build-essential python3-msgpack python3-setuptools \
  libgstrtspserver-1.0-dev
```

### Cifrado

- **libsodium**: use `wfb_keygen` para generar `drone.key` (a bordo) y `gs.key` (estación terrestre)

### Visualización en estación terrestre

- **QGroundControl**: monitoreo del estado del controlador de vuelo y la telemetría
- **GStreamer / RTSP**: recepción y reproducción del video transmitido desde el dron

---

## 6. Enlaces GitHub y ficha técnica de la ALFA AWUS036ACH

### Enlaces oficiales

| Elemento | Enlace |
|---|---|
| Proyecto wfb-ng | https://github.com/svpcom/wfb-ng.git |
| Controlador parcheado (RTL8812AU) | https://github.com/svpcom/rtl8812au |
| Controlador parcheado (RTL8812EU) | https://github.com/svpcom/rtl8812eu |
| Página del producto ALFA AWUS036ACH | https://yupitek.com/es/products/alfa/awus036ach/ |
| Tutorial PX4 WFB-ng | https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html |

### Ficha técnica ALFA AWUS036ACH

| Especificación | Detalle |
|---|---|
| Chip | Realtek **RTL8812AU** |
| Estándar inalámbrico | 802.11a / b / g / n / **ac (WiFi 5)** |
| Banda | **2.4 GHz + 5 GHz** doble banda |
| Interfaz | USB 3.0 **Type-C** |
| Antena | 2 × **RP-SMA** desmontables (2T2R MIMO) |
| Monitor mode | Compatible con monitor mode + inyección de paquetes (requiere controlador parcheado wfb-ng) |
| Controlador wfb-ng | `rtl88xxau_wfb` (svpcom/rtl8812au, v5.2.20) |
| Posicionamiento | Tarjeta **probada oficialmente** por wfb-ng (modo 5 GHz en ambos extremos) |

---

## 7. Configuración paso a paso (capítulo principal)

A continuación, cuatro secciones. La ruta **A (inicio rápido con Raspberry Pi)** es la más recomendada, casi como «quemar y usar»; la **B** es para quienes prefieren instalar manualmente la estación terrestre en un escritorio Linux x86; **C / D** tratan sobre el emparejamiento de claves y los archivos de configuración, necesarios en ambas rutas.

### A. Inicio rápido con Raspberry Pi (más recomendado)

wfb-ng proporciona imágenes preempaquetadas para Raspberry Pi. Queme una para el dron y otra para la estación terrestre, y estarán listas al encender.

**1. Descargar y quemar la imagen**

Vaya a la página de **Releases** de wfb-ng en GitHub, descargue el archivo `*.img.gz` más reciente, descomprímalo y quémelo en **dos** tarjetas SD (una para el dron, otra para la estación terrestre).

```bash
# Descomprimir la imagen (ejemplo; el nombre depende de la Release real)
gunzip wfb-ng-*.img.gz
# Use Raspberry Pi Imager, dd o balenaEtcher para quemar la SD
```

**2. Insertar la tarjeta, encender y acceder por SSH**

Inserte la ALFA AWUS036ACH en ambas tarjetas, encienda y acceda por SSH (IP y credenciales predeterminadas):

```bash
ssh pi@192.168.0.111
# Contraseña: raspberry
```

**3. Activar el servicio de estación terrestre (Ground Station)**

Ejecute en la **Pi de la estación terrestre**:

```bash
sudo systemctl enable wifibroadcast@gs
sudo systemctl enable rtsp
sudo systemctl enable fpv-video
sudo systemctl enable osd
sudo reboot
```

**4. Activar el servicio de a bordo (Drone)**

Ejecute en la **Pi del dron**:

```bash
sudo systemctl enable wifibroadcast@drone
sudo systemctl enable fpv-camera
sudo reboot
```

**5. Supervisar el estado del enlace en la estación terrestre**

```bash
wfb-cli gs
```

> Si ve información de conexión, canal y tasa de pérdida de paquetes, el enlace está activo. Abra QGroundControl para ver la telemetría y el video.

---

### B. Instalación manual en Debian / Ubuntu (estación terrestre)

Si usa un escritorio o portátil Linux x86-64 como estación terrestre, puede instalarlo manualmente.

**1. Instalar dkms y el controlador parcheado**

```bash
git clone -b v5.2.20 https://github.com/svpcom/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh
```

**2. Confirmar que el controlador wfb-ng ha tomado el control de la tarjeta**

```bash
# Debería ver wlan0 con MTU de 2312
ifconfig

# El controlador debería mostrar rtl88xxau_wfb (RTL8812AU) o rtl8812eu (RTL8812EU)
ethtool -i wlan0
```

{{< alert "triangle-exclamation" >}}
Si `ethtool -i wlan0` muestra el controlador genérico `rtl8812au` en lugar de `rtl88xxau_wfb`, el controlador parcheado no se instaló correctamente y wfb-ng no podrá entrar en modo de inyección. Revise si hubo errores en la instalación con dkms.
{{< /alert >}}

**3. Ejecutar el script de instalación oficial**

```bash
curl -o install_gs.sh https://raw.githubusercontent.com/svpcom/wfb-ng/refs/heads/master/scripts/install_gs.sh
sudo bash ./install_gs.sh
```

**4. Supervisar el enlace**

```bash
wfb-cli gs
```

---

### C. Claves y emparejamiento

El video y la telemetría de wfb-ng están cifrados. El dron y la estación terrestre deben usar las **claves correspondientes** para comunicarse.

```bash
# Generar claves (genérelas en el dron y luego distribúyalas)
wfb_keygen

# drone.key → colóquelo en el dron
# gs.key     → colóquelo en la estación terrestre
# Ambas deben coincidir; de lo contrario, el enlace aparecerá «conectado pero sin datos»
```

> Si usó el **script de instalación automática de la sección B (install_gs.sh)** , este generará y configurará las claves automáticamente. En la instalación manual, asegúrese de que `drone.key` y `gs.key` sean el mismo par.

---

### D. Archivo de configuración: /etc/wifibroadcast.cfg

`/etc/wifibroadcast.cfg` es el archivo de configuración principal de wfb-ng. Estos son los parámetros que más se ajustan:

```ini
[common]
# Canal 165 = 5825 MHz (banda de 5.8 GHz)
wifi_channel = 165

# Código de país 'BO' (Bolivia) para desbloquear la máxima potencia de transmisión
wifi_region = 'BO'

[drone]
# link_domain debe ser «exactamente igual» en dron y estación terrestre
link_domain = "my_wfb_link_01"

[drone_mavlink]
# Recibir MAVLink desde el UART del controlador de vuelo (configurar UART a 1500000 baudios)
peer = 'serial:ttyS0:1500000'

[drone_video]
peer = 'listen://0.0.0.0:5602'

[gs]
# Ídem, ambos extremos deben coincidir
link_domain = "my_wfb_link_01"
```

**Los tres errores más comunes:**

1. **`wifi_channel` debe coincidir en ambos extremos**: aquí usamos 165 (5825 MHz, 5.8 GHz), configúrelo igual en dron y estación terrestre.
2. **`link_domain` debe coincidir en ambos extremos**: es el «identificador» del enlace; si no es idéntico, no habrá conexión.
3. **La velocidad en baudios del UART del controlador de vuelo debe ser 1500000**: `peer = 'serial:ttyS0:1500000'` requiere que el UART del controlador también esté a 1500000 baudios, de lo contrario no se recibirá MAVLink.

{{< alert "triangle-exclamation" >}}
**Atención**: `wifi_region = 'BO'` sirve para desbloquear la potencia máxima de transmisión, pero **no implica que su uso sea legal en su país**. Consulte la sección «Aviso legal» más abajo.
{{< /alert >}}

---

## 8. Notas de implementación / problemas comunes

Esta sección recoge los problemas reales que encontramos al implementar el sistema. Léala con atención.

### ⚠️ Problema 1: Alimentación insuficiente de la tarjeta de red → reinicios del puerto y pérdida masiva de paquetes

La AWUS036ACH **consume mucha corriente instantánea durante la transmisión (TX)** . Si se conecta directamente a un puerto USB 2.0 estándar de la Raspberry Pi, la alimentación USB de la Pi no puede sostener el pico de corriente, lo que provoca: **reinicio del puerto de la tarjeta, cortes del enlace, corrupción de paquetes y congelación de la imagen**.

Solución (imprescindible en el dron):

- Alimente la tarjeta **directamente desde un BEC de 5V** (no desde el USB de la Pi); conecte la salida del BEC a la tarjeta.
- Conecte un **capacitor de 470µF de baja ESR entre +5V y GND** de la tarjeta para filtrar los picos de corriente durante la transmisión.
- En la estación terrestre, si usa un **puerto USB 3.0 de un portátil con el cable USB 3.0 original**, normalmente puede alimentarla directamente sin BEC adicional.

> Este paso es la clave de la «estabilidad». Hemos visto a muchas personas estancadas en la pérdida de paquetes por no haber resuelto la alimentación.

### Problema 2: Error de cifrado / sin conexión

Si `wfb-cli gs` muestra conexión pero **no hay video ni telemetría**, suele deberse a una de estas dos causas:

- **Claves incorrectas**: verifique que `drone.key` (dron) y `gs.key` (estación terrestre) sean el mismo par.
- **Canal o link_domain inconsistentes**: `wifi_channel` y `link_domain` deben ser idénticos en ambos extremos.

Comando de diagnóstico:

```bash
# Consulte los registros en tiempo real del servicio de la estación terrestre
journalctl -xu wifibroadcast@gs
```

### ⚠️ Problema 3: Aviso legal (muy importante)

Este enlace transmite ondas de radio activamente y, por tanto, está sujeto a la normativa de equipos de radio.

- **Antes de usarlo, asegúrese de que su legislación local permita la potencia y las bandas de frecuencia para este uso de WiFi.**
- Taiwán, China, Estados Unidos y Europa tienen sus propias regulaciones sobre la potencia de transmisión, los canales disponibles y las «transmisiones sin conexión» en la banda ISM de 5.8 GHz.
- `wifi_region = 'BO'` sirve para desbloquear el límite de potencia del hardware, pero **no implica legalidad en su país**. Ajuste el canal y la potencia según la normativa de su país; reduzca la potencia o cambie a un canal legal si es necesario.
- Use únicamente en entornos legales (como terrenos propios, recintos cerrados para pruebas o formación). No interfiera con las comunicaciones de terceros.

---

## 9. Conclusión

En resumen, con una ALFA AWUS036ACH y el software open source wfb-ng, hemos construido un sistema que ofrece:

- **Ventaja en costo**: el material de este enlace DIY cuesta mucho menos que las soluciones de video digital comerciales.
- **Open source**: todo el código, los controladores y la configuración son públicos y verificables.
- **Personalizable**: canal, potencia, claves y modo de exposición de MAVLink, todo bajo su control.
- **Largo alcance**: video digital + telemetría en un solo enlace, con un alcance real en 5 GHz muy superior al analógico, resistencia a obstrucciones y cifrado.

Para aplicaciones de agricultura, inspección, formación en seguridad o simplemente para quienes deseen comprender «el principio detrás del video digital», esta es una ruta que vale la pena explorar.

Nuestro equipo seguirá compartiendo en el blog notas prácticas sobre el uso de tarjetas ALFA en enlaces para drones. Si encuentra problemas durante la instalación, no dude en dejar un comentario — **la práctica es la forma más rápida de aprender**.

---

{{< faq >}}

---

## Apéndice: Glosario para principiantes (términos clave en lenguaje sencillo)

Si es la primera vez que se encuentra con esta tecnología, aquí tiene una explicación rápida de los términos más usados en este artículo:

| Término | Explicación sencilla |
|---|---|
| **FPV** (First Person View) | «Visión en primera persona»: es como estar sentado en el «asiento del piloto» del dron, viendo en tiempo real lo que ve la cámara a bordo en su pantalla o gafas. |
| **Video digital vs. Video analógico** | El video analógico es como la televisión antigua: señal deficiente = pantalla llena de estática, y cualquiera puede interceptarla. El video digital convierte la imagen en paquetes de datos que pueden cifrarse y resisten mejor el ruido, aunque el hardware y la configuración son más complejos. |
| **monitor mode** | Una tarjeta WiFi normal solo puede «conectarse» a un router. El monitor mode le permite «escuchar y enviar señales de radio directamente sin conectarse a nada»; es la base técnica de este artículo. |
| **packet injection (inyección de paquetes)** | En monitor mode, consiste en «lanzar» paquetes de radio personalizados al aire sin pasar por el flujo normal de conexión WiFi. wfb-ng usa este mecanismo para transmitir video y telemetría. |
| **wfb-ng** | Software open source que «transforma» una tarjeta WiFi en una radio específica para drones, en lugar de usarla como red normal. Es el núcleo de este artículo. |
| **FEC (Forward Error Correction, corrección directa de errores)** | Consiste en enviar información adicional «de respaldo» durante la transmisión; aunque algunos paquetes se pierdan, el receptor puede reconstruir la imagen original sin solicitar retransmisiones (que ralentizarían la transmisión en escenarios de larga distancia y alta velocidad). |
| **MAVLink** | Protocolo de «lenguaje común» entre el controlador de vuelo del dron (como Pixhawk) y la estación terrestre, para transmitir el estado de vuelo y enviar comandos. |
| **RTP / RTSP** | Protocolos comunes para transmitir video en tiempo real por red; muchas cámaras IP y sistemas de vigilancia los utilizan. |
| **Cifrado libsodium** | Biblioteca de cifrado open source usada en este artículo para cifrar video y telemetría, garantizando que solo el dron y la estación terrestre con las claves correspondientes puedan descifrar el contenido. |
| **TX diversity (diversidad de transmisión)** | Usar varias tarjetas para transmitir los mismos datos simultáneamente; si una señal queda obstruida, otra puede compensarla, como un «doble seguro». |
| **BEC (Battery Eliminator Circuit)** | Módulo regulador de voltaje que reduce la tensión de la batería del dron a los 5 V que necesita la tarjeta, soportando los picos de corriente para evitar cortes por inestabilidad. |
| **RTL8812AU** | Modelo de chip Realtek que utiliza la tarjeta ALFA AWUS036ACH, determinando su compatibilidad con monitor mode e inyección de paquetes. |

> En una frase: wfb-ng «disfraza» la tarjeta ALFA de emisora de radio dedicada para el dron, permitiendo transmitir video y datos de control a larga distancia de forma open source y cifrada — un «canal privado» que usted (el operador) construye activamente.

---

## Referencias

- **Proyecto wfb-ng (svpcom/wfb-ng)**: https://github.com/svpcom/wfb-ng.git
- **Página del producto ALFA AWUS036ACH**: https://yupitek.com/es/products/alfa/awus036ach/
- **Controlador parcheado (RTL8812AU)**: https://github.com/svpcom/rtl8812au
- **Controlador parcheado (RTL8812EU)**: https://github.com/svpcom/rtl8812eu
- **Documentación PX4 WFB-ng**: https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html

---

*Este artículo fue escrito por el equipo técnico de Yupitek (distribuidor autorizado de ALFA Network en Taiwán), basado en la documentación oficial de wfb-ng y la experiencia práctica. Antes de implementarlo, asegúrese de cumplir con la normativa de radiofrecuencia de su país y ajuste la potencia y los canales según corresponda.*
