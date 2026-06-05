---
title: "Unidades de procesamiento de datos (DPU) NVIDIA BlueField"
description: "Descubra las soluciones DPU NVIDIA BlueField. Descargue, acelere e aísle los servicios de red, almacenamiento e infraestructura de seguridad con SmartNIC programables basadas en ARM."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Unidades de procesamiento de datos (DPU) NVIDIA BlueField

Las unidades de procesamiento de datos NVIDIA® BlueField® (DPU) representan una evolución en la arquitectura de centros de datos. Al integrar adaptadores de red ConnectX con núcleos de CPU ARM® programables y motores de aceleración por hardware, las DPU descargan, aceleran y aíslan las tareas de infraestructura, evitando sobrecargar la CPU del servidor.

---

## Inventario de DPU BlueField

Distribuimos unidades DPU BlueField preparadas para virtualización a escala de la nube, almacenamiento definido por software y seguridad de confianza cero.

![NVIDIA BlueField DPU](/images/products/mellanox/official/dpu/bluefield2-dpu-official.jpg)
*Adaptador de infraestructura programable NVIDIA BlueField*

| Referencia | Nombre comercial | Red principal | Núcleos de CPU ARM | Memoria | Interfaz | Protocolo | Factor de forma |
|-------------|----------------|-----------------|---------------|--------|-----------|----------|-------------|
| **900-9D3B6-00CV-AA0** | BlueField-2 DPU | Doble puerto 100GbE / EDR IB | 8 núcleos ARMv8 A72 | 16 GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | PCIe FHHL |
| **900-9D3B6-00CC-EA0** | BlueField-2 DPU | Doble puerto 100GbE / EDR IB | 8 núcleos ARMv8 A72 | 16 GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | PCIe FHHL (Cifrado habilitado) |
| **900-9D3B4-00CC-EA0** | BlueField-2 DPU | Puerto único 100GbE / EDR IB | 8 núcleos ARMv8 A72 | 16 GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | PCIe FHHL (Cifrado habilitado) |

---

## Tecnologías clave de las DPU

### 1. Descarga de tareas de infraestructura (SmartNIC+)
En lugar de destinar ciclos del procesador host a la conmutación de red del hipervisor (OVS), túneles de virtualización (VXLAN, NVGRE) o traducción de direcciones de red (NAT), la DPU ejecuta estas tareas directamente por hardware a velocidad de línea mediante la tecnología **NVIDIA ASAP² (procesamiento y conmutación acelerada de paquetes)**.

### 2. Aceleración de almacenamiento definido por software
Con **NVMe SNAP™ (procesamiento acelerado por red definido por software)**, una DPU BlueField puede presentar almacenamiento de red remoto (a través de RoCEv2 o TCP) al sistema operativo host como si fuera un disco físico NVMe local. Los procesos de emulación, cifrado y compresión se gestionan íntegramente en la DPU, lo que elimina los cuellos de botella de almacenamiento en la virtualización.

### 3. Aislamiento y seguridad de confianza cero (Zero Trust)
La DPU ejecuta su propio sistema operativo Linux independiente (normalmente Ubuntu) en sus núcleos ARM integrados, de forma totalmente aislada del servidor host. Incluso si el sistema operativo principal se ve comprometido, los agentes de seguridad, cortafuegos sin agente y el cifrado de red (IPsec, TLS) que se ejecutan en la DPU continúan funcionando de manera segura y sin alteraciones.

### 4. Entorno de software NVIDIA DOCA
Las DPU BlueField se programan utilizando el entorno de software **NVIDIA DOCA™**, que proporciona API estándar para el desarrollo de aplicaciones aceleradas de red, seguridad, almacenamiento y telemetría.

---

## Casos de uso frecuentes

- **Proveedores de nube de última generación**: permite el alojamiento bare-metal aislando la gestión de la infraestructura en la DPU.
- **Infraestructura hiperconvergente corporativa (HCI)**: descarga las funciones de red superpuesta y almacenamiento (VMware NSX / Proxmox OVS) para maximizar la densidad de máquinas virtuales.
- **Entornos de alta seguridad**: ejecuta análisis de seguridad de red (IDS/IPS) y cargas de trabajo de cifrado directamente en el límite de la red.

---

{{< alert >}}
¿Necesita una cotización del producto? Por favor, [contáctenos](/es/contact/).
{{< /alert >}}
