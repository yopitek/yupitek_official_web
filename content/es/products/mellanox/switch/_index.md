---
title: "Conmutadores InfiniBand y Ethernet NVIDIA Mellanox"
description: "Conmutadores de red corporativos de alta densidad. Seleccione conmutadores Mellanox EDR (100G), HDR (200G) y NDR (400G). Diseñados para computación de alto rendimiento y clústeres de IA."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Conmutadores InfiniBand y Ethernet NVIDIA Mellanox — EDR, HDR y NDR

Los conmutadores InfiniBand NVIDIA Mellanox constituyen la columna vertebral de los clústeres modernos de entrenamiento de IA y de los entornos de computación de alto rendimiento (HPC). Con una elevada densidad de puertos, una latencia mínima de conmutación y una gestión avanzada de la congestión, estos equipos facilitan el escalado de sistemas multinodo de forma eficiente.

---

## Catálogo de conmutadores

A continuación se detalla la lista de conmutadores de montaje en bastidor de 1U, tanto gestionables como no gestionables, disponibles en nuestro inventario.

![Switch InfiniBand HDR Mellanox](/images/products/mellanox/official/switch/switch-hdr-40port-official.png)
*Conmutador InfiniBand NVIDIA Mellanox Quantum HDR de 40 puertos*

| Referencia | Generación del chipset | Gestionable | Configuración de puertos | Velocidad del puerto | Factor de forma | Flujo de aire | Fuente de alimentación |
|-------------|--------------------|---------|---------------------|------------|-------------|---------|--------------|
| **MSB7800-ES2F** | Switch-IB 2 (EDR) | Sí (x86) | 36x QSFP28 | 100 Gb/s | 1U estándar | Puerto a alimentación (P2C) | Fuente CA dual |
| **MSB7890-ES2R** | Switch-IB 2 (EDR) | No | 36x QSFP28 | 100 Gb/s | 1U estándar | Alimentación a puerto (C2P) | Fuente CA dual |
| **MQM8700-HS2F** | Quantum (HDR) | Sí (x86) | 40x QSFP56 | 200 Gb/s | 1U estándar | Puerto a alimentación (P2C) | Fuente CA dual |
| **MQM8790-HS2F** | Quantum (HDR) | No | 40x QSFP56 | 200 Gb/s | 1U estándar | Puerto a alimentación (P2C) | Fuente CA dual |
| **MQM9700-NS2F** | Quantum 2 (NDR) | Sí | 32x OSFP (64 puertos NDR) | 400 Gb/s (OSFP) | 1U estándar | Puerto a alimentación (P2C) | Fuente CA dual |
| **MQM9790-NS2F** | Quantum 2 (NDR) | No | 32x OSFP (64 puertos NDR) | 400 Gb/s (OSFP) | 1U estándar | Puerto a alimentación (P2C) | Fuente CA dual |

---

## Comparativa de generaciones InfiniBand

| Generación | Chipset | Velocidad máxima del puerto | Capacidad del conmutador | Tasa de señalización / Modulación | Latencia |
|------------|---------|----------------|-----------------|-----------------------------|---------|
| **EDR** | Switch-IB 2 | 100 Gb/s | 7,2 Tb/s | 25 Gb/s NRZ | 90 ns |
| **HDR** | Quantum | 200 Gb/s | 16,0 Tb/s | 50 Gb/s PAM4 | 130 ns |
| **NDR** | Quantum 2 | 400 Gb/s (listo para 800G) | 51,2 Tb/s | 100 Gb/s PAM4 | 205 ns |

---

## Guía de topología de red InfiniBand

El diseño de un clúster para entrenamiento de IA o simulación física requiere arquitecturas específicas:

![Topología InfiniBand Fat-Tree de NVIDIA Mellanox](/images/products/mellanox/ai-generated/switch_topology@2x.png)

### 1. Topología Fat-Tree (CLOS no bloqueante)
Es la arquitectura estándar en redes InfiniBand. Organiza los conmutadores en niveles jerárquicos (Leaf y Spine) para proporcionar múltiples rutas paralelas de comunicación.
- **No bloqueante (suscripción 1:1)**: cada nodo se comunica a la velocidad máxima del enlace de forma simultánea. Requiere que el ancho de banda hacia los conmutadores troncales (Spine) sea equivalente al ancho de banda descendente hacia los nodos.
- **Sobresuscrita (por ejemplo, 2:1)**: reduce los costes de adquisición al disminuir el número de conexiones con los conmutadores troncales (Spine). Se recomienda para cargas de trabajo donde la comunicación entre procesos sea mayoritariamente local.

### 2. Redes de IA optimizadas por raíl (Rail-Optimized)
En nodos con múltiples GPU (como los sistemas NVIDIA HGX H100 con 8 GPU), cada GPU cuenta con una tarjeta ConnectX dedicada. La optimización por raíl conecta el adaptador de la «GPU 1» de todos los servidores a un conmutador «Rail Switch 1» dedicado, el adaptador de la «GPU 2» al «Rail Switch 2», y así sucesivamente. De esta forma, el patrón de comunicación en anillo que emplean las librerías de aprendizaje profundo (como NCCL) se replica directamente en la red física, minimizando la latencia.

---

## Conmutadores gestionables frente a no gestionables y Subnet Manager (SM)

A diferencia de las redes Ethernet, que son de tipo plug-and-play gracias al protocolo ARP, una red InfiniBand **no puede transferir tráfico si no cuenta con un Subnet Manager (SM) activo**. El SM se encarga de detectar la topología, asignar identificadores locales (LID) y calcular las rutas de envío.
- **Conmutadores gestionables**: cuentan con una CPU interna que ejecuta MLNX-OS/Onyx y aloja un Subnet Manager integrado. Son los idóneos para clústeres independientes pequeños (de hasta unos 36 nodos).
- **Conmutadores no gestionables**: ofrecen una latencia extremadamente baja, pero carecen de CPU integrada. Requieren un SM externo que se ejecute en un servidor host (a través de OpenSM) o en otro conmutador gestionable dentro de la misma infraestructura de red.

---

{{< alert >}}
¿Necesita una cotización del producto? Por favor, [contáctenos](/es/contact/).
{{< /alert >}}
