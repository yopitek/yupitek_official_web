---
title: "Tarjetas de interfaz de red (NIC) NVIDIA Mellanox ConnectX"
description: "Compare las tarjetas de interfaz de red NVIDIA Mellanox ConnectX-4 Lx, ConnectX-5, ConnectX-6 Dx/Lx y ConnectX-7. Opciones de 10G, 25G, 50G, 100G, 200G y 400G para PCIe Gen3/4/5."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Tarjetas de red ConnectX de Mellanox / NVIDIA: de 10G a 400G

Los adaptadores NVIDIA Mellanox ConnectX proporcionan un ancho de banda y una latencia excelentes para servidores corporativos y clústeres de inteligencia artificial. A continuación se detalla el catálogo completo de modelos disponibles en Yupitek, organizados por velocidad.

---

## Tarjetas de red de 10GbE / 25GbE

Están indicadas para servidores empresariales estándar, entornos de virtualización (como VMware ESXi) y sistemas de almacenamiento NAS de alto rendimiento.

### Modelo de 10G

| Referencia | Gen / Chipset | Puertos | Velocidad | Ranura PCIe | Conector | Protocolo | Soporte (Bracket) |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX4121A-XCAT** | ConnectX-4 Lx | Doble | 10GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Perfil alto |

### Modelos de 25G

![NVIDIA ConnectX-4 Lx 25G](/images/products/mellanox/official/nic/connectx4-lx-25g-official.jpg)
*Adaptador de doble puerto NVIDIA ConnectX-4 Lx 25GbE*

![NVIDIA ConnectX-5 25G](/images/products/mellanox/official/nic/connectx5-25g-official.jpg)
*Adaptador de doble puerto NVIDIA ConnectX-5 25GbE*

| Referencia | Gen / Chipset | Puertos | Velocidad | Ranura PCIe | Conector | Protocolo | Soporte / Factor de forma | Características especiales |
|-------------|---------------|-------|-------|-----------|-----------|----------|-----------------------|------------------|
| **MCX4121A-ACAT** | ConnectX-4 Lx | Doble | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Soporte de perfil alto | Tarjeta PCIe estándar |
| **MCX4121A-ACUT** | ConnectX-4 Lx | Doble | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Soporte de perfil alto | Soporte para UEFI |
| **MCX512A-ACAT** | ConnectX-5 EN | Doble | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Soporte de perfil alto | RoCEv2 mejorado |
| **MCX512A-ACUT** | ConnectX-5 EN | Doble | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Soporte de perfil alto | UEFI (x86/ARM) |
| **MCX631102AN-ADAT**| ConnectX-6 Lx | Doble | 25GbE | PCIe 4.0 x8 | SFP28 | Ethernet | Soporte de perfil alto | Arranque seguro (Secure Boot), sin criptografía |
| **MCX623432AS-ADAB**| ConnectX-6 Lx | Doble | 25GbE | PCIe 4.0 x8 | SFP28 | Ethernet | OCP 3.0 (Tornillo manual)| Arranque seguro (Secure Boot), formato OCP 3.0 |

---

## Tarjetas de red de 50GbE / 100GbE

Diseñadas para almacenamiento de alta velocidad NVMe sobre redes (NVMe-oF), infraestructura hiperconvergente (HCI) y servidores de bases de datos.

![NVIDIA ConnectX-5 100G](/images/products/mellanox/official/nic/connectx5-100g-official.jpg)
*Adaptador NVIDIA ConnectX-5 100GbE*

![NVIDIA ConnectX-6 Dx 100G](/images/products/mellanox/official/nic/connectx6-dx-100g-official.png)
*Adaptador de doble puerto NVIDIA ConnectX-6 Dx 100GbE*

### Modelo de 50G

| Referencia | Gen / Chipset | Puertos | Velocidad | Ranura PCIe | Conector | Protocolo | Soporte (Bracket) |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX515A-GCAT** | ConnectX-5 EN | Único | 50GbE | PCIe 3.0 x16 | QSFP28 | Ethernet | Perfil alto |

### Modelos de 100G

| Referencia | Gen / Chipset | Puertos | Velocidad | Ranura PCIe | Conector | Protocolo | Factor de forma | Características especiales |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX515A-CCAT** | ConnectX-5 EN | Único | 100GbE | PCIe 3.0 x16 | QSFP28 | Ethernet | PCIe de perfil alto | Tarjeta estándar de 100G |
| **MCX555A-ECAT** | ConnectX-5 VPI | Único | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe de perfil alto | EDR IB y 100GbE |
| **MCX516A-CCAT** | ConnectX-5 EN | Doble | 100GbE | PCIe 3.0 x16 | QSFP28 | Ethernet | PCIe de perfil alto | Tarjeta de doble puerto de 100G |
| **MCX516A-CDAT** | ConnectX-5 Ex | Doble | 100GbE | PCIe 4.0 x16 | QSFP28 | Ethernet | PCIe de perfil alto | Interfaz PCIe 4.0 |
| **MCX556A-ECAT** | ConnectX-5 VPI | Doble | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe de perfil alto | EDR IB de doble puerto |
| **MCX556A-EDAT** | ConnectX-5 Ex VPI| Doble | 100G | PCIe 4.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe de perfil alto | PCIe 4.0 y EDR doble |
| **MCX653105A-ECAT**| ConnectX-6 VPI | Único | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe de perfil alto | HDR100 IB y 100GbE |
| **MCX653106A-ECAT**| ConnectX-6 VPI | Doble | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe de perfil alto | HDR100 IB y 100GbE |
| **MCX623106AN-CDAT**| ConnectX-6 Dx | Doble | 100GbE | PCIe 4.0 x16 | QSFP56 | Ethernet | PCIe de perfil alto | Doble puerto SFP56/QSFP56 de 100G |
| **MCX623436AN-CDAB**| ConnectX-6 Dx | Doble | 100GbE | PCIe 4.0 x16 | QSFP56 | Ethernet | OCP 3.0 (Tornillo manual)| Factor de forma OCP |

---

## Tarjetas de red de 200GbE / 400GbE

Adaptadores de alto rendimiento diseñados para nodos de servidores GPU de inteligencia artificial (como las arquitecturas NVIDIA HGX/DGX), sistemas financieros de alta frecuencia (HFT) e infraestructuras de red HPC.

![NVIDIA ConnectX-7 400G](/images/products/mellanox/official/nic/connectx7-400g-official.png)
*Adaptador OSFP de 400G NVIDIA ConnectX-7*

### Modelos de 200G

| Referencia | Gen / Chipset | Puertos | Velocidad | Ranura PCIe | Conector | Protocolo | Factor de forma | Características especiales |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX653105A-HDAT**| ConnectX-6 VPI | Único | 200G | PCIe 4.0 x16 | QSFP56 | VPI (IB/ETH) | PCIe de perfil alto | HDR IB y 200GbE |
| **MCX653106A-HDAT**| ConnectX-6 VPI | Doble | 200G | PCIe 4.0 x16 | QSFP56 | VPI (IB/ETH) | PCIe de perfil alto | Puerto doble HDR/200G |
| **MCX623105A-VDAT**| ConnectX-6 Dx | Único | 200GbE | PCIe 4.0 x16 | QSFP56 | Ethernet | PCIe de perfil alto | Puerto único de 200G |
| **MCX75310AAS-HEAT**| ConnectX-7 IB | Único | 200G | PCIe 5.0 x16 | OSFP | InfiniBand | PCIe de perfil alto | NDR200, tecnología Socket Direct |
| **MCX755106AS-HEAT**| ConnectX-7 VPI | Doble | 200G | PCIe 5.0 x16 | QSFP112 | VPI (IB/ETH) | PCIe de perfil alto | 1 puerto IB, 2.º puerto VPI |
| **MCX753436MS-HEAB**| ConnectX-7 VPI | Doble | 200G | PCIe 5.0 x16 | QSFP112 | VPI (IB/ETH) | OCP 3.0 (Tornillo manual)| OCP Multi-Host / Socket Direct |

### Modelos de 400G

| Referencia | Gen / Chipset | Puertos | Velocidad | Ranura PCIe | Conector | Protocolo | Factor de forma | Características especiales |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX75310AAS-NEAT**| ConnectX-7 IB | Único | 400Gb/s| PCIe 5.0 x16 | OSFP | InfiniBand | PCIe de perfil alto | NDR InfiniBand |
| **MCX75510AAS-NEAT**| ConnectX-7 IB | Único | 400Gb/s| PCIe 5.0 x16 | OSFP | InfiniBand | PCIe de perfil alto | NDR OSFP, listo para Socket Direct |

---

## Guía de selección técnica

Al elegir un adaptador ConnectX, tenga en cuenta los siguientes aspectos clave:

### 1. Modo de protocolo (VPI frente a EN)
- **Adaptadores EN:** Solo son compatibles con redes Ethernet.
- **Adaptadores VPI (Virtual Protocol Interconnect):** Se pueden configurar mediante firmware para funcionar en redes InfiniBand o Ethernet, lo que proporciona mayor flexibilidad en la implementación.

### 2. Requisitos de ancho de banda PCIe
Asegúrese de que la versión de PCIe y el ancho de ranura de su servidor admitan la tarjeta a la velocidad máxima:
- Una tarjeta de red de doble puerto de 100G requiere PCIe 4.0 x16 para que ambos puertos funcionen a su capacidad máxima simultáneamente.
- Aunque las tarjetas PCIe 4.0 son retrocompatibles con ranuras PCIe 3.0, el rendimiento máximo se verá limitado por el estándar PCIe 3.0 (aproximadamente 64 Gbps para x8 y 128 Gbps para x16).

### 3. Factor de forma OCP 3.0 frente a PCIe estándar
Los modelos con sufijos como `-ADAB`, `-CDAB` o `-HEAB` utilizan el formato **OCP NIC 3.0**. Estas tarjetas están diseñadas para ranuras dedicadas de servidores (habituales en las generaciones más recientes de Supermicro, Dell, HPE y Lenovo) y no se pueden instalar en una ranura PCIe estándar.

---

¿Busca cables compatibles? Consulte nuestros catálogos de [cables DAC](/es/products/mellanox/cable-dac/) y [cables AOC](/es/products/mellanox/cable-aoc/). Para consultar precios y disponibilidad de stock, [solicite un presupuesto](/es/contact/).
