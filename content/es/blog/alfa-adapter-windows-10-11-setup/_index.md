---
title: "Guía de Configuración del Adaptador ALFA para Windows 10 y Windows 11"
description: "Cómo instalar y configurar adaptadores ALFA USB WiFi en Windows 10/11. Descarga de drivers, modo monitor con Acrylic WiFi, solución de problemas y comparación de adaptadores para usuarios de Windows."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["windows-10", "windows-11", "alfa-network", "adaptador-wifi", "instalacion-driver", "acrylic-wifi"]
---

Los adaptadores USB WiFi de ALFA Network son ampliamente reconocidos en los círculos de investigación de seguridad y redes, pero la mayoría de los tutoriales se enfocan exclusivamente en Linux. La buena noticia para los usuarios de Windows: todos los adaptadores ALFA principales funcionan en Windows 10 y Windows 11 con drivers proporcionados por el fabricante — sin necesidad de compilar código fuente.

La diferencia crítica respecto a Linux es el modo monitor. En Linux, herramientas como `aircrack-ng` y `airodump-ng` aprovechan la captura raw 802.11 con inyección de paquetes. En Windows, el modelo de driver (NDIS) no expone las mismas capacidades de hardware. El modo monitor completo y la inyección de paquetes **no están disponibles de forma nativa en Windows**. Lo que Windows hace bien — y hace muy bien — es la conectividad plug-and-play y el escaneo WiFi con herramientas pulidas como Acrylic WiFi Analyzer.

Esta guía describe la instalación de drivers, el escaneo WiFi y una evaluación honesta de lo que Windows puede y no puede hacer con un adaptador ALFA.

---

## Adaptadores ALFA Compatibles con Windows

Todos los adaptadores listados a continuación están oficialmente soportados en Windows 10 y Windows 11. La disponibilidad de drivers y la compatibilidad con modo monitor varía según el chipset.

| Modelo | Chipset | Windows 10 | Windows 11 | Soporte Modo Monitor |
|---|---|---|---|---|
| [AWUS036ACH](/es/products/alfa/awus036ach/) | RTL8812AU | ✅ Soporte completo | ✅ Soporte completo | ⚠️ Solo escaneo pasivo (Acrylic WiFi Pro) |
| [AWUS036ACM](/es/products/alfa/awus036acm/) | MT7612U | ✅ Soporte completo | ✅ Soporte completo | ⚠️ Solo escaneo pasivo |
| [AWUS036ACS](/es/products/alfa/awus036acs/) | RTL8811AU | ✅ Soporte completo | ✅ Soporte completo | ⚠️ Solo escaneo pasivo |
| [AWUS036AX](/es/products/alfa/awus036ax/) | RTL8832BU | ⚠️ Descarga manual de driver | ✅ Driver incluido | ⚠️ Limitado |
| [AWUS036AXER](/es/products/alfa/awus036axer/) | RTL8832BU | ⚠️ Descarga manual de driver | ✅ Driver incluido | ⚠️ Limitado |
| [AWUS036AXM](/es/products/alfa/awus036axm/) | MT7921AUN | ⚠️ Descarga manual de driver | ✅ Driver incluido | ❌ No soportado |
| [AWUS036AXML](/es/products/alfa/awus036axml/) | MT7921AUN | ⚠️ Descarga manual de driver | ✅ Driver incluido | ❌ No soportado |

{{< alert "circle-info" >}}
Para uso cotidiano en Windows, el AWUS036ACH (RTL8812AU) y el AWUS036ACM (MT7612U) son las opciones más probadas. Ambos reciben drivers con firma WHQL de Realtek/MediaTek y tienen el historial de compatibilidad más amplio con Windows.
{{< /alert >}}

---

## Instalación del Driver

### Método A: Windows Update (Recomendado)

Windows Update es la ruta más sencilla para la mayoría de los adaptadores. Al conectar un adaptador ALFA compatible, Windows consulta automáticamente Windows Update en busca de un driver NDIS correspondiente.

1. Conecta el adaptador ALFA a un puerto USB 3.0.
2. Espera 30–60 segundos. Windows mostrará una notificación: *"Software del controlador del dispositivo instalado correctamente"* (Windows 10) o completará el proceso de forma silenciosa en Windows 11.
3. Abre el **Administrador de dispositivos** (`Win + X` → Administrador de dispositivos).
4. Expande **Adaptadores de red**. Deberías ver el adaptador listado (p. ej., *"Realtek 8812AU Wireless LAN 802.11ac USB NIC"* o *"MediaTek Wi-Fi 6 MT7921U Wireless LAN Card"*).
5. Si el adaptador aparece con un ícono de advertencia amarillo, continúa con el Método B.

{{< alert "circle-info" >}}
Windows Update requiere una conexión a internet activa para descargar los drivers. Si estás configurando una máquina de laboratorio aislada, descarga el paquete de drivers en otro equipo y transfiérelo manualmente antes de usar el Método B.
{{< /alert >}}

### Método B: Instalación Manual del Driver — RTL8812AU (AWUS036ACH / AWUS036ACM / AWUS036ACS)

1. Visita la [página de descargas de ALFA Network](https://www.alfa.com.tw/service_1.html) o el archivo de drivers de Realtek y descarga el último driver WHQL de Windows para RTL8812AU.
2. Extrae el archivo `.zip` en una carpeta local (p. ej., `C:\Drivers\RTL8812AU`).
3. Ejecuta el instalador `.exe` como Administrador. Acepta el aviso de UAC.
4. Sigue el asistente de instalación. Cuando se te solicite, mantén la ruta de instalación predeterminada.
5. Reinicia el equipo cuando el instalador finalice.
6. Abre el **Administrador de dispositivos** → **Adaptadores de red**. Confirma que el adaptador aparece sin ícono de advertencia.

Para verificar la versión del driver:

1. Haz clic derecho en el adaptador dentro del Administrador de dispositivos → **Propiedades**.
2. Haz clic en la pestaña **Controlador**.
3. Anota la **Versión del controlador** y la **Fecha del controlador** para futuras referencias.

### Método B: Instalación Manual del Driver — MT7921AUN (AWUS036AXM / AWUS036AXML)

El driver MT7921AUN de MediaTek está incluido en el almacén de drivers de Windows 11 (build 22000+). Para Windows 10:

1. Descarga el paquete de drivers MediaTek MT7921 desde el [sitio oficial de MediaTek](https://www.mediatek.com/products/home-networking/wi-fi-6-6e) o la página de soporte de ALFA Network.
2. Extrae el paquete y ejecuta `Setup.exe` como Administrador.
3. Reinicia el equipo después de la instalación.

{{< alert "circle-info" >}}
Los usuarios de Windows 11 con adaptadores MT7921AUN (AWUS036AXM, AWUS036AXML) generalmente obtienen un driver funcional pocos minutos después de conectar el adaptador, incluso en una instalación nueva — no se requiere descarga manual.
{{< /alert >}}

### Códigos de Error Comunes en el Administrador de Dispositivos

| Código de Error | Significado | Primera Solución |
|---|---|---|
| **Código 43** | El driver reportó una falla | Desinstalar driver → reiniciar → reinstalar |
| **Código 10** | El dispositivo no puede iniciarse | Probar un puerto USB diferente; deshabilitar la suspensión selectiva de USB |
| **Código 28** | No hay drivers instalados | Ejecutar Windows Update o instalar el driver manualmente |
| **Código 45** | Dispositivo no conectado | Reconectar el adaptador; probar un cable USB diferente si se usa extensión |

---

## Uso del Adaptador ALFA para Escaneo WiFi en Windows

### Escaneo por Línea de Comandos Nativo de Windows

Windows incluye un comando de escaneo WiFi integrado que no requiere software adicional:

```cmd
netsh wlan show networks mode=bssid
```

Este comando muestra todos los SSID visibles junto con el BSSID (dirección MAC), intensidad de señal, tipo de radio, canal y tipo de autenticación. Es útil para diagnósticos rápidos, pero carece de gráficas de canales en tiempo real o detección de SSID ocultos.

### Acrylic WiFi Analyzer (Gratuito)

Para un análisis WiFi serio en Windows, [Acrylic WiFi Analyzer](https://www.acrylicwifi.com/) es la herramienta recomendada. La versión gratuita ofrece:

- Escaneo en tiempo real en las bandas de 2.4 GHz, 5 GHz y 6 GHz
- Gráficas de ocupación de canales — identifica al instante los canales congestionados
- Detección de SSID ocultos (muestra redes que transmiten SSIDs vacíos)
- Gráficas de historial de señal para puntos de acceso individuales
- Búsqueda de OUI del fabricante para identificación de BSSID

Acrylic WiFi funciona con cualquier adaptador WiFi compatible con Windows, incluyendo todos los modelos ALFA listados anteriormente. Su extensión de driver NDIS se integra directamente con la pila inalámbrica de Windows, razón por la cual funciona sin necesitar el modo monitor al estilo Linux.

{{< alert "circle-info" >}}
Acrylic WiFi Analyzer es el equivalente en Windows más cercano a herramientas como `airodump-ng` para escaneo pasivo. Si tu flujo de trabajo incluye relevamientos WiFi, análisis de sitio o planificación de canales, cubre casi todo lo que necesitas sin salir de Windows.
{{< /alert >}}

### Captura con Wireshark en Windows

Wireshark puede capturar tráfico WiFi en Windows con la ayuda de Npcap (consulta la sección dedicada más adelante). Sin embargo, sin modo monitor verdadero, solo capturas:

- Tramas dirigidas a tu adaptador (unicast hacia tu MAC)
- Tramas broadcast y multicast en la red a la que estás asociado

**No** capturas el tráfico entre otros dispositivos a menos que estén en el mismo dominio de broadcast y Wireshark esté ejecutándose en modo promiscuo sobre una red conmutada. La captura completa de tramas 802.11 (tramas de gestión, tramas beacon de APs externos) está restringida.

---

## Modo Monitor en Windows (La Verdad Sin Rodeos)

Aquí es donde es necesario gestionar las expectativas con claridad.

**El modo monitor en Windows es fundamentalmente diferente al modo monitor en Linux.**

En Linux, drivers como `aircrack-ng/rtl8812au` exponen una interfaz de modo monitor verdadero (`wlan0mon`) que recibe todas las tramas 802.11 del entorno de radio — tramas de gestión, tramas de datos de otras redes, solicitudes de sondeo y tramas beacon — sin requerir asociación. El adaptador también soporta inyección de paquetes: envío de tramas 802.11 raw a nivel de hardware.

En Windows, el modelo de driver NDIS no expone estas capacidades. Los dos enfoques prácticos para monitoreo basado en Windows son:

**Enfoque A: Acrylic WiFi Pro + driver compatible**

Acrylic WiFi Pro utiliza una extensión de driver NDIS personalizada para habilitar el *escaneo 802.11 pasivo*. Esto permite recibir tramas beacon y respuestas de sondeo de puntos de acceso a los que no estás conectado — suficiente para relevamientos de RF, análisis de canales y enumeración de APs. **No** soporta inyección de paquetes ni captura completa de handshakes.

**Enfoque B: Kali Linux en USB live**

Para flujos de trabajo que requieren modo monitor completo con inyección de paquetes — captura de handshakes WPA, pruebas de deautenticación, inundación de beacons — la plataforma correcta es Kali Linux. Tienes dos opciones:

- Arrancar un **USB live de Kali Linux** en la misma máquina (bare metal, acceso completo al hardware)
- Ejecutar una **VM de Kali Linux** (VMware o VirtualBox) con passthrough USB para entregar el adaptador ALFA directamente a la pila USB de la VM

Consulta la [guía de passthrough USB en VirtualBox/VMware](/es/blog/alfa-adapter-virtualbox-vmware-usb/) para instrucciones detalladas de configuración de la VM.

{{< alert "triangle-exclamation" >}}
Si tu flujo de trabajo requiere modo monitor + inyección de paquetes — para captura de handshakes WPA, tramas de deautenticación o cualquier ataque 802.11 activo — Windows no puede hacer esto de forma confiable. Kali Linux (bare metal o VM con passthrough USB) es la plataforma correcta. Ningún driver de Windows soporta actualmente inyección 802.11 raw para adaptadores ALFA.
{{< /alert >}}

---

## Solución de Problemas

### El Adaptador No es Reconocido en Absoluto

1. Prueba un puerto USB diferente — preferiblemente USB 3.0 (puerto azul). Algunos hubs USB no suministran suficiente energía para adaptadores de doble banda.
2. Abre el Administrador de dispositivos y busca en **Otros dispositivos** alguna entrada con un signo de interrogación amarillo. Esto confirma que Windows detecta el hardware pero carece de driver.
3. Haz clic derecho → **Actualizar driver** → **Buscar software de controlador en mi equipo** y apunta a la carpeta del driver descargado manualmente.
4. Si no aparece nada en el Administrador de dispositivos ni siquiera en Otros dispositivos, prueba un cable USB diferente (si usas extensión) o prueba el adaptador en otro equipo para descartar una falla de hardware.

### El Adaptador Aparece en el Administrador de Dispositivos pero No Encuentra Redes

1. Deshabilita temporalmente el Firewall de Windows Defender para confirmar que no está bloqueando la inicialización del adaptador. Vuelve a habilitarlo después de la prueba.
2. En el Administrador de dispositivos, haz clic derecho en el adaptador → **Propiedades** → pestaña **Opciones avanzadas**. Busca la configuración de **Modo inalámbrico** o **Banda**. Si está configurado solo en 5 GHz, no verás redes en un entorno solo de 2.4 GHz.
3. Confirma que el adaptador no está deshabilitado: haz clic derecho → **Habilitar dispositivo**.
4. Ejecuta `netsh wlan show interfaces` en un Símbolo del sistema con privilegios elevados para verificar el estado operativo del adaptador.

### Velocidades Lentas o Desconexiones Frecuentes en Windows 11

El **Connected Standby** de Windows 11 (Modern Standby) puede interferir con los adaptadores USB WiFi al suspender agresivamente los dispositivos USB.

Para deshabilitar la suspensión selectiva de USB:

1. Abre el **Panel de control** → **Opciones de energía** → **Cambiar la configuración del plan** → **Cambiar la configuración avanzada de energía**.
2. Expande **Configuración USB** → **Configuración de suspensión selectiva de USB**.
3. Establece en **Deshabilitado** tanto para **Con batería** como para **Conectado a la corriente**.
4. Haz clic en **Aplicar** → **Aceptar**, luego reinicia el equipo.

### Código 43: El Driver Reportó una Falla

1. Abre el Administrador de dispositivos, haz clic derecho en el adaptador → **Desinstalar dispositivo**. Marca la opción *"Eliminar el software del controlador para este dispositivo"* si aparece.
2. Desconecta el adaptador.
3. Reinicia el equipo.
4. Vuelve a conectar el adaptador.
5. Reinstala el driver usando el Método B descrito anteriormente.

Si el Código 43 persiste después de una reinstalación limpia, prueba un puerto USB diferente o prueba en otro equipo. Un Código 43 persistente en múltiples equipos generalmente indica una falla de hardware en el propio adaptador.

---

## Configuración de Adaptador ALFA + Wireshark

Wireshark en Windows requiere **Npcap** como su biblioteca de captura de paquetes. WinPcap (la alternativa heredada) está desactualizado y no soporta de forma confiable las versiones modernas de Windows.

### Paso 1: Instalar Npcap

1. Descarga Npcap desde [https://npcap.com/](https://npcap.com/) (gratuito para uso personal y educativo).
2. Ejecuta el instalador como Administrador.
3. Durante la instalación, marca **"Install Npcap in WinPcap API-compatible mode"** si planeas usar herramientas heredadas junto con Wireshark.
4. Reinicia el equipo.

### Paso 2: Configurar Wireshark

1. Abre Wireshark. Tu adaptador ALFA aparecerá en la lista de interfaces.
2. Haz doble clic en la interfaz del adaptador para iniciar una captura.
3. Para filtrar tramas de gestión 802.11 (tramas beacon, solicitudes de sondeo), usa el filtro de visualización de Wireshark:

```
wlan.fc.type == 0
```

4. Para filtrar específicamente las solicitudes de sondeo:

```
wlan.fc.type_subtype == 0x0004
```

{{< alert "circle-info" >}}
El filtro `wlan.fc.type` solo funciona cuando Wireshark recibe tramas 802.11 reales con encabezados visibles. En Windows sin modo monitor, la mayoría de las capturas muestran tramas Ethernet II incluso sobre WiFi — la capa NDIS elimina el encabezado 802.11 antes de pasar las tramas a Npcap. La captura completa del encabezado 802.11 requiere una interfaz de modo monitor verdadero, disponible en Linux.
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
Capturar tráfico de red sin autorización es ilegal en la mayoría de las jurisdicciones. Solo captura tráfico en redes que sean de tu propiedad o para las que tengas permiso escrito explícito para realizar pruebas.
{{< /alert >}}

---

## Resumen: Windows vs Linux para Adaptadores ALFA

| Característica | Windows 10/11 | Kali Linux |
|---|---|---|
| **Plug & play** | ✅ Instalación automática de driver | ⚠️ Varía según chipset |
| **Escaneo WiFi** | ✅ Acrylic WiFi / netsh | ✅ airodump-ng / iwlist |
| **Modo monitor** | ⚠️ Solo pasivo (Acrylic Pro) | ✅ Modo monitor completo |
| **Inyección de paquetes** | ❌ No soportado | ✅ Inyección completa |
| **Captura con Wireshark** | ⚠️ Limitado (sin encabezados 802.11) | ✅ Captura 802.11 completa |
| **Captura de handshake WPA** | ❌ No confiable | ✅ aircrack-ng / hcxdumptool |
| **Mejor caso de uso** | Conectividad diaria, relevamiento WiFi, análisis de canales | Pruebas de seguridad, desafíos CTF, pruebas de penetración |

La conclusión es clara: Windows es una excelente plataforma para adaptadores ALFA cuando tu objetivo es la conectividad de red, el análisis WiFi y la planificación de canales. En el momento en que tu flujo de trabajo requiera inyección de tramas 802.11 raw o captura de handshakes WPA, cambia a Kali Linux — ya sea de forma nativa o mediante una VM con passthrough USB.

---

## Guías Relacionadas

- [Passthrough USB en VirtualBox y VMware para Adaptadores ALFA](/es/blog/alfa-adapter-virtualbox-vmware-usb/) — Ejecuta Kali Linux en una VM con soporte completo para adaptadores ALFA
- [Guía de Instalación de Drivers para Kali Linux y Ubuntu](/es/blog/install-alfa-driver-kali-ubuntu/) — Instalación completa de drivers por chipset
- [Guía de Compra de Adaptadores WiFi ALFA 2026](/es/blog/alfa-wifi-adapter-buyer-guide-2026/) — Qué adaptador es el adecuado para tu caso de uso
