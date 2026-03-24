---
title: "Evaluación de Seguridad Inalámbrica Empresarial: Un Framework Completo"
description: "Framework completo de evaluación de seguridad inalámbrica empresarial con adaptadores ALFA. Cubre alcance, detección de puntos de acceso no autorizados, auditoría WPA2/WPA3, pruebas PMF e informes para equipos de seguridad TI."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["enterprise", "wireless-security", "penetration-testing", "rogue-AP", "WPA2", "WPA3", "PMF", "ALFA-network"]
---

{{< alert "triangle-exclamation" >}}
**Aviso Legal:** Todas las evaluaciones de seguridad inalámbrica deben realizarse únicamente en redes e infraestructuras para las cuales se haya recibido autorización expresa y por escrito. El monitoreo inalámbrico no autorizado, la inyección de paquetes o el despliegue de puntos de acceso no autorizados es ilegal en la mayoría de las jurisdicciones. Cada fase descrita en este framework asume la existencia de una carta de compromiso debidamente ejecutada, firmada por el propietario del activo, que cubre la ventana de prueba específica y el alcance autorizado. Solo para pruebas autorizadas.
{{< /alert >}}

La evaluación de seguridad inalámbrica empresarial no se trata simplemente de responder "¿podemos descifrar la contraseña?". Una evaluación exhaustiva examina cada capa de su arquitectura inalámbrica: la solidez de los protocolos de autenticación, la integridad de la protección de tramas de administración, la precisión del inventario de puntos de acceso autorizados, la robustez del aislamiento de clientes en los segmentos de red para invitados y la resistencia de la infraestructura 802.1X ante ataques de RADIUS no autorizado.

Este framework cubre el ciclo de vida completo de una evaluación tal como la practican los equipos profesionales de pruebas de penetración en entornos empresariales. Está estructurado en seis fases secuenciales — alcance y pre-compromiso, reconocimiento pasivo, detección de puntos de acceso no autorizados, análisis de handshakes WPA2/WPA3, verificación de PMF, pruebas de aislamiento de clientes y evaluación de EAP/RADIUS — seguidas de una plantilla de informe y una referencia de herramientas. Cada fase está diseñada para ejecutarse con adaptadores ALFA Network, que proporcionan la estabilidad en modo monitor, la capacidad de inyección y la cobertura multibanda que exigen las pruebas inalámbricas de nivel empresarial.

Ya sea que usted sea un CISO que encarga una auditoría inalámbrica anual, un equipo red team interno que prepara una evaluación o una firma externa de pruebas de penetración que incorpora un nuevo cliente empresarial, este framework ofrece una metodología repetible y defendible.

---

## Alcance y Requisitos de Pre-Compromiso

La calidad de cualquier evaluación inalámbrica se determina antes de capturar un solo paquete. Los compromisos con un alcance mal definido desperdician tiempo, generan exposición legal y producen hallazgos que no pueden atribuirse a infraestructuras específicas. Un documento de alcance bien elaborado elimina la ambigüedad y protege tanto al equipo de pruebas como al cliente.

### Qué Debe Incluir el Documento de Alcance

El documento de alcance debe enumerar, como mínimo:

- **Todos los SSIDs bajo prueba**, incluidos los SSIDs corporativos, los de invitados, los dedicados a IoT y cualquier red oculta conocida por el equipo de red
- **Bandas de frecuencia en uso**: 2.4 GHz, 5 GHz y 6 GHz (Wi-Fi 6E) — cada banda puede presentar diferentes modelos de puntos de acceso, comportamientos de controlador y configuraciones de seguridad
- **Perímetro físico**: un mapa del edificio o campus con planos de planta que indiquen la ubicación conocida de los puntos de acceso, especialmente relevante en edificios de múltiples inquilinos donde pueden aparecer SSIDs vecinos en los resultados de escaneo
- **Inventario de puntos de acceso autorizados**: la lista de direcciones MAC (BSSID) de cada punto de acceso legítimo, utilizada como referencia para la detección de puntos de acceso no autorizados
- **Carta de autorización** firmada por el CISO, CTO o propietario delegado del activo, que cubra explícitamente la ventana de prueba (fecha y hora de inicio y fin), los nombres de los miembros del equipo de pruebas y las actividades específicas autorizadas (escaneo pasivo, inyección activa, desautenticación, simulación de punto de acceso no autorizado)

### Fuera del Alcance por Defecto

A menos que se incluyan explícitamente por escrito, lo siguiente siempre está fuera del alcance:

- **Dispositivos cliente**: laptops, teléfonos celulares y endpoints IoT que se conectan a la red inalámbrica. Los ataques del lado del cliente (captura de credenciales mediante RADIUS no autorizado) solo pueden realizarse en dispositivos de prueba designados, nunca en equipos de usuarios en producción
- **Usuarios de la red de invitados**: las personas que se conectan a un SSID de invitados de acceso público no tienen expectativa de ser sujetos de una prueba de seguridad
- **Redes adyacentes**: los SSIDs pertenecientes a inquilinos vecinos en un edificio compartido, aunque sean visibles en escaneos pasivos

### Recordatorio Legal

{{< alert "triangle-exclamation" >}}
**Siempre obtenga autorización por escrito** que especifique la ventana de prueba exacta (fechas, hora de inicio, hora de fin, zona horaria), los nombres y direcciones MAC del equipo de pruebas, y las técnicas específicas autorizadas. Una aprobación verbal no es suficiente. Guarde la carta de autorización firmada en su expediente de compromiso y téngala accesible durante las pruebas en caso de contacto con las autoridades.
{{< /alert >}}

---

## Fase 1: Reconocimiento Pasivo

### Objetivos

El reconocimiento pasivo establece la realidad del entorno inalámbrico sin transmitir un solo byte. Los objetivos son:

- Identificar cada punto de acceso que transmita dentro del rango, incluidos los que no figuren en el inventario autorizado
- Registrar SSID, BSSID, canal operativo, intensidad de señal y configuraciones de seguridad (tipo de cifrado, estado de PMF)
- Detectar SSIDs ocultos mediante respuestas a solicitudes de sondeo
- Identificar interferencias en canales co-canal y en canales adyacentes que puedan afectar la confiabilidad de las pruebas

Durante el reconocimiento pasivo, **no inyecte, no desautentique, no transmita**. Esta fase es de solo escucha.

### Herramientas

**airodump-ng** es adecuado para escaneos instantáneos y captura de handshakes. Para registro continuo con metadatos más ricos, se prefiere **Kismet** — produce registros estructurados que pueden importarse a herramientas de informes y correlaciona solicitudes de sondeo con identidades de dispositivos a lo largo del tiempo.

```bash
# Passive scan across all bands — DO NOT inject or deauth during recon
sudo airodump-ng wlan0mon --band abg -w enterprise_recon

# Kismet for comprehensive, continuous logging
sudo kismet -c wlan0mon
```

Kismet escribe archivos de base de datos SQLite `.kismet` y capturas `.pcapng` simultáneamente, proporcionándole un registro persistente que sobrevive a la ventana de evaluación.

### Qué Registrar

Para cada punto de acceso descubierto, registre:

| Campo | Notas |
|---|---|
| BSSID | Dirección MAC de la radio del punto de acceso |
| SSID | Nombre de la red (vacío si está oculta) |
| Cifrado | WPA2-PSK, WPA2-Enterprise, WPA3-SAE, WPA3-Enterprise, Abierta |
| Canal | Anote los puntos de acceso de doble radio que aparecen en 2.4 y 5 GHz |
| Señal (dBm) | Útil para estimación de ubicación física |
| Estado PMF | Extraer del RSN IE en las tramas beacon: Requerido / Habilitado / Deshabilitado |
| Fabricante | Derivar del OUI del BSSID — útil para identificar hardware de consumo no autorizado |

### Adaptadores Recomendados

- **AWUS036AXML** — Tribanda (2.4/5/6 GHz), necesario para detectar puntos de acceso Wi-Fi 6E que operan en canales de 6 GHz. Esencial en entornos empresariales modernos que despliegan infraestructura Wi-Fi 6E
- **AWUS036ACH** — Doble banda (2.4/5 GHz), chipset RTL8812AU confiable, excelente para entornos donde no se utiliza 6 GHz y se prefiere la máxima compatibilidad con las herramientas existentes

---

## Fase 2: Detección de Puntos de Acceso No Autorizados

Un punto de acceso no autorizado es cualquier AP que opere dentro de su entorno y que no figure en el inventario de puntos de acceso autorizados. Dos categorías son operacionalmente relevantes:

1. **Punto de acceso no autorizado conectado a la red interna** — un empleado bien intencionado conecta un router de consumo, o un atacante que ha obtenido acceso físico instala un AP oculto en una toma Ethernet. Estos puntos de acceso están en su red interna y eluden todos los controles perimetrales.
2. **AP gemelo malicioso (evil twin)** — un AP que transmite un SSID de apariencia legítima (idéntico o muy similar al SSID corporativo) operado por un atacante para capturar credenciales o realizar ataques de intermediario (man-in-the-middle). Estos generalmente no están conectados a su red.

### Método de Detección

Compare la lista de BSSIDs del reconocimiento pasivo con el inventario de puntos de acceso autorizados proporcionado durante el alcance. Cualquier BSSID que transmita un SSID corporativo y no figure en el inventario es un candidato a punto de acceso no autorizado.

```bash
# Filter scan output for corporate SSID to isolate all APs broadcasting it
sudo airodump-ng wlan0mon | grep "CorporateSSID"

# Compare discovered BSSIDs against authorized list (example using diff)
# Save airodump BSSID column to discovered.txt, authorized list to authorized.txt
diff <(sort discovered.txt) <(sort authorized.txt)
```

Cualquier BSSID que aparezca en `discovered.txt` pero no en `authorized.txt` es un hallazgo.

### Detección Basada en Desautenticación (Si Está Autorizada)

Si la desautenticación está explícitamente dentro del alcance, puede utilizar el comportamiento de reconexión del cliente para determinar si un punto de acceso no autorizado está conectado a la red interna: desautentique un cliente del AP sospechoso y observe si el cliente se reasocía a un AP legítimo en el mismo SSID. Si el cliente realiza un roaming limpio, el AP no autorizado puede compartir la misma red de backend. Si el cliente no logra reconectarse, es probable que el AP no autorizado sea un AP aislado (escenario de evil twin).

### Validación del WIDS

Si la organización ha desplegado un Sistema de Detección/Prevención de Intrusiones Inalámbricas (WIDS/WIPS), esta fase debe incluir una prueba controlada para verificar que el WIDS detecta el AP de prueba no autorizado dentro de una ventana de tiempo aceptable. Despliegue un AP de prueba con el SSID corporativo usando una dirección MAC que no figure en el inventario y mida la latencia de detección. Una ventana de detección superior a 60 segundos representa una brecha significativa en la cobertura.

---

## Fase 3: Análisis de Handshakes WPA2/WPA3

### WPA2: Captura del Handshake de 4 Vías

Capturar el handshake de 4 vías de WPA2 permite verificar de forma offline que la frase de contraseña de la red cumple con la política de complejidad de contraseñas de la organización. Esto no es un respaldo al descifrado de contraseñas como objetivo del compromiso — más bien, es una verificación de cumplimiento: ¿puede el hash capturado ser descifrado en un tiempo razonable por un adversario utilizando hardware de consumo?

```bash
# Target specific AP on channel 6 and write capture to file
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w handshake wlan0mon

# Convert captured .cap to hashcat format for offline audit
hcxpcapngtool -o hash.hc22000 handshake-01.cap
```

Envíe el hash `.hc22000` resultante a un auditor de contraseñas offline contra la lista de palabras y el conjunto de reglas aprobados por la organización. Si la frase de contraseña es recuperable con listas de contraseñas comunes (rockyou, variaciones del nombre de la empresa, recorridos de teclado), repórtelo como hallazgo Medio o Alto dependiendo del nivel de acceso a la red del SSID.

### WPA3: SAE y Modo de Transición

WPA3 utiliza Autenticación Simultánea de Iguales (SAE), que proporciona secreto hacia adelante y es resistente a ataques de diccionario offline. Sin embargo, muchas organizaciones despliegan el **Modo de Transición WPA3** para mantener la compatibilidad con clientes WPA2 — este modo acepta tanto autenticación SAE como PSK. Pruebe si un atacante puede forzar a un cliente WPA3 a realizar un downgrade a WPA2 presentando una baliza (beacon) exclusiva de WPA2 para el mismo SSID; un downgrade exitoso es un hallazgo Alto.

Para más detalles sobre las pruebas específicas de WPA3, consulte nuestra [guía de pruebas de seguridad WPA3](/es/blog/wpa3-security-testing-alfa-2026/).

---

## Fase 4: Pruebas de PMF (Tramas de Administración Protegidas)

### Por Qué Importa el PMF

Las Tramas de Administración Protegidas (PMF) 802.11w previenen los ataques de desautenticación y desasociación. Sin PMF, un atacante puede enviar tramas de desautenticación falsificadas a cualquier cliente, forzando la desconexión y habilitando la captura de handshakes, la captura de credenciales mediante un AP no autorizado o una simple denegación de servicio. PMF es obligatorio en WPA3 y opcional (pero muy recomendado) en WPA2.

### Procedimiento de Prueba

Intente un ataque de desautenticación contra un cliente de prueba asociado a cada SSID bajo evaluación. El resultado revela si PMF está habilitado:

```bash
# Attempt deauthentication flood against AP
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF wlan0mon

# If connected test client disconnects: PMF NOT enforced — reportable finding
# If test client remains connected: PMF enforced — pass
```

Realice siempre esta prueba contra equipos de prueba designados, nunca contra clientes en producción.

### Documentación del Estado de PMF

Documente cada SSID con su nivel de aplicación de PMF:

| SSID | Cifrado | Estado PMF | Hallazgo |
|---|---|---|---|
| Corp-WiFi | WPA2-Enterprise | Habilitado (no requerido) | Medio |
| Corp-WiFi-6E | WPA3-Enterprise | Requerido | Aprobado |
| CorpGuest | WPA2-PSK | Deshabilitado | Alto |

**PMF Deshabilitado en cualquier SSID** es como mínimo un hallazgo Medio. PMF Deshabilitado en un SSID corporativo con acceso a recursos internos es Alto. Para detalles completos sobre la metodología de pruebas de PMF, consulte nuestra [guía de inyección de paquetes](/es/blog/packet-injection-guide/).

---

## Fase 5: Pruebas de Aislamiento de Clientes

### Aislamiento en la Red de Invitados

Los SSIDs de invitados deben aplicar el aislamiento de clientes — la imposibilidad de que un cliente invitado se comunique directamente con otro cliente invitado. Sin aislamiento, un actor malicioso en la red de invitados puede realizar envenenamiento ARP, suplantación de LLMNR/NBT-NS o ataques directos contra otros invitados.

**Procedimiento de prueba:**

1. Conecte dos dispositivos de prueba dedicados (no dispositivos de usuarios en producción) al SSID de invitados
2. Desde el Dispositivo A, intente un ping ICMP a la dirección IP del Dispositivo B
3. Desde el Dispositivo A, intente un escaneo ARP de la subred de invitados

Un SSID de invitados que falla el aislamiento de clientes (los pings tienen éxito entre dispositivos de prueba) es un hallazgo Alto.

### Aislamiento de Invitados a Red Interna

Verifique que la red de invitados no pueda alcanzar rangos de red interna:

```bash
# From a test device on guest SSID, ARP scan the internal network range
sudo arp-scan -l --interface wlan0
# Zero responses from internal range = pass
# Any response from internal range = Critical finding
```

Adicionalmente, intente la resolución DNS de nombres de host internos y conexiones TCP directas a interfaces de administración internas (SSH, paneles de administración HTTP). Cualquier conexión exitosa desde el segmento de invitados a la infraestructura interna es un hallazgo Crítico.

---

## Fase 6: Evaluación de EAP/RADIUS (SSIDs Empresariales)

### Autenticación 802.1X y el Ataque de RADIUS No Autorizado

WPA2-Enterprise y WPA3-Enterprise utilizan autenticación EAP 802.1X, donde los clientes se autentican ante un servidor RADIUS. El control de seguridad crítico es la **validación del certificado del servidor**: cada cliente debe verificar el certificado del servidor RADIUS antes de enviar credenciales. Si los clientes no validan el certificado, un atacante puede desplegar un AP no autorizado con un servidor RADIUS falso y capturar hashes NTLMv2 o credenciales EAP.

### Procedimiento de Prueba

Despliegue un AP no autorizado usando `hostapd-wpe` configurado con el SSID corporativo. Esto crea un AP compatible con 802.1X respaldado por un servidor RADIUS no autorizado que registra todos los intentos de autenticación:

```bash
# Install hostapd-wpe
sudo apt install hostapd-wpe

# Configure with the corporate SSID and appropriate channel
# Edit /etc/hostapd-wpe/hostapd-wpe.conf with target SSID/channel details
sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf

# Monitor for captured credential hashes in the output
```

**Hallazgo Crítico:** Si algún cliente (incluyendo clientes de prueba que se hayan conectado previamente al SSID 802.1X de producción) se conecta al RADIUS no autorizado sin mostrar una advertencia de certificado, o si el usuario acepta una advertencia de certificado y se capturan credenciales, esto es un hallazgo Crítico. Indica que los clientes no están aplicando el anclaje de certificados (certificate pinning) ni una validación adecuada de la cadena de certificados.

**Remediación:** Despliegue el anclaje de certificados mediante perfiles de configuración MDM (Administración de Dispositivos Móviles) que especifiquen el certificado exacto del servidor RADIUS o la CA emisora. Asegúrese de que los usuarios finales reciban capacitación de concientización sobre el rechazo de solicitudes de certificados inesperadas.

---

## Referencia del Kit de Herramientas de Evaluación

Las siguientes herramientas cubren el flujo de trabajo completo de evaluación inalámbrica empresarial. Todas son compatibles con los adaptadores ALFA Network en modo monitor. Para la configuración del adaptador, consulte nuestra guía sobre [cómo habilitar el modo monitor en Kali Linux](/es/blog/enable-monitor-mode-kali-linux/).

| Herramienta | Propósito | Adaptador Recomendado | Comando Principal |
|---|---|---|---|
| airodump-ng | Escaneo pasivo, captura de handshakes | Cualquier ALFA (AWUS036AXML / AWUS036ACH) | `sudo airodump-ng wlan0mon --band abg` |
| hcxdumptool | Captura de PMKID, captura pasiva de handshakes | AWUS036AXML (Wi-Fi 6E) | `sudo hcxdumptool -i wlan0mon -o out.pcapng` |
| hcxpcapngtool | Convertir capturas a formato hashcat | N/A (post-procesamiento) | `hcxpcapngtool -o hash.hc22000 cap.pcapng` |
| Kismet | Registro continuo, correlación de SSID/clientes | AWUS036ACH | `sudo kismet -c wlan0mon` |
| aireplay-ng | Pruebas de PMF, inyección de desautenticación | AWUS036ACH | `sudo aireplay-ng --deauth 10 -a BSSID wlan0mon` |
| hostapd-wpe | AP no autorizado / RADIUS no autorizado para pruebas EAP | AWUS036ACH | `sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf` |
| Wireshark | Análisis a nivel de paquetes de capturas | Cualquiera (mediante archivo de captura) | `wireshark -r handshake-01.cap` |
| arp-scan | Verificación de aislamiento de invitados/red interna | Cualquiera | `sudo arp-scan -l --interface wlan0` |

---

## Plantilla de Informe

### Resumen Ejecutivo

El resumen ejecutivo debe ser legible por un CTO o CISO sin conocimientos previos de seguridad inalámbrica. Debe incluir:

- **Calificación de riesgo general**: Crítico / Alto / Medio / Bajo — derivada de la severidad del hallazgo confirmado más alto
- **Recuento de hallazgos clave** por nivel de severidad
- **Declaración de brecha de cumplimiento**: referencia a cualquier estándar relevante (PCI-DSS 4.0 Requisito 11.2, ISO/IEC 27001 A.13.1, NIST 800-153) e indicación de si el entorno inalámbrico evaluado cumple con esos requisitos
- **Elementos de acción inmediata**: hallazgos que requieren remediación antes del próximo día hábil

### Tabla de Hallazgos

Todos los hallazgos técnicos deben presentarse en una tabla estandarizada que mapee cada hallazgo a una severidad, la infraestructura afectada y una recomendación de remediación concreta:

| ID | Severidad | Hallazgo | SSID(s) Afectado(s) | Recomendación |
|---|---|---|---|---|
| WL-01 | Crítico | El SSID de invitados no tiene aislamiento de clientes; los dispositivos de prueba se comunicaron directamente | CorpGuest | Habilitar el aislamiento de clientes AP en el controlador WLAN; verificar mediante nueva prueba |
| WL-02 | Crítico | Los clientes 802.1X se conectan al RADIUS no autorizado sin advertencia de certificado | Corp-WiFi | Desplegar anclaje de certificados mediante MDM; configurar el ancla de confianza de la CA del servidor RADIUS |
| WL-03 | Alto | PMF deshabilitado en el SSID corporativo; el ataque de desautenticación tuvo éxito | Corp-WiFi | Habilitar PMF Requerido en todos los SSIDs WPA2; actualizar a WPA3 donde el hardware lo permita |
| WL-04 | Alto | Se detectó un AP no autorizado con SSID corporativo en un BSSID que no figura en el inventario | Corp-WiFi-5G | Investigar el AP físico; desplegar alerta WIDS para BSSIDs desconocidos |
| WL-05 | Medio | La frase de contraseña WPA2 es recuperable con un diccionario común en menos de 4 horas | Corp-IoT | Aplicar una frase de contraseña aleatoria de 16+ caracteres; rotar trimestralmente |
| WL-06 | Bajo | El fabricante/modelo del AP es identificable por el OUI del beacon y las respuestas de sondeo | Todos | Considerar la ofuscación de la huella del AP si el modelo de amenaza lo justifica |

### Definiciones de Severidad para Hallazgos Inalámbricos

| Severidad | Definición | Ejemplo |
|---|---|---|
| Crítico | Vía inmediata y explotable para la captura de credenciales o acceso a la red interna | SSID con autenticación abierta, sin cifrado, brecha de invitados a red interna, éxito del RADIUS no autorizado 802.1X |
| Alto | Falla significativa de control que requiere remediación inmediata | WPA2 con PMF Deshabilitado, AP no autorizado confirmado en la red, éxito del ataque de downgrade a WPA3 |
| Medio | Brecha de control que aumenta el riesgo pero requiere condiciones adicionales para ser explotada | Política de contraseñas débil, Modo de Transición WPA3 sin protección contra downgrade |
| Bajo | Brecha informacional o de defensa en profundidad | Identificación del modelo del AP, divulgación de información del SSID |

---

## Recursos Relacionados

- [Guía de Inyección de Paquetes: Probando su Adaptador WiFi con aireplay-ng](/es/blog/packet-injection-guide/)
- [Pruebas de Seguridad WPA3 con Adaptadores ALFA (2026)](/es/blog/wpa3-security-testing-alfa-2026/)
- [Habilitar el Modo Monitor en Kali Linux](/es/blog/enable-monitor-mode-kali-linux/)
