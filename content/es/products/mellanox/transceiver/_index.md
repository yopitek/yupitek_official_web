---
title: "Transceptores ópticos NVIDIA Mellanox LinkX"
description: "Seleccione módulos transceptores ópticos originales NVIDIA Mellanox LinkX. Transceptores de alta velocidad de 25G, 100G, 400G y 800G para redes multimodo y monomodo."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Transceptores ópticos NVIDIA Mellanox LinkX — de 25G a 800G

Los transceptores ópticos NVIDIA LinkX® están diseñados para cumplir con las exigencias de la computación de alto rendimiento, el almacenamiento corporativo y los entornos de gran escala (hyperscale). El uso de transceptores originales asegura la integridad de la señal, una tasa de errores de bits (BER) mínima y compatibilidad completa con los adaptadores ConnectX y los conmutadores Quantum.

---

## Catálogo de transceptores ópticos

A continuación se detalla la lista de modelos de transceptores ópticos disponibles en nuestro inventario.

<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin: 1.5rem 0;">
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/sfp28-25g-transceiver.jpg" alt="Transceptor SFP28 de 25G" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">Transceptor óptico NVIDIA Mellanox 25G SFP28 SR</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/qsfp28-100g-transceiver.jpg" alt="Transceptor QSFP28 de 100G" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">Transceptor óptico NVIDIA Mellanox 100G QSFP28 SR4</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/osfp-400g-transceiver.jpg" alt="Transceptor OSFP de 400G" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">Transceptor óptico NVIDIA 400G OSFP NDR</p>
  </div>
</div>

| Referencia | Velocidad | Interfaz | Conector | Longitud de onda | Tipo de fibra | Distancia máx. | Descripción |
|-------------|-------|-----------|-----------|------------|------------|--------------|-------------|
| **MMA2P00-AS** | 25G | SFP28 | LC Duplex | 850 nm | Multimodo (MMF) | 150 m (OM4) / 100 m (OM3) | Módulo SR de 25GbE |
| **MMA1B00-C100-TG** | 100G | QSFP28 | MPO-12 | 850 nm | Multimodo (MMF) | 100 m (OM4) / 70 m (OM3) | Módulo SR4 de 100GbE, DDMI |
| **MMA4Z00-NS400** | 400G | OSFP | MPO-12 APC| 850 nm | Multimodo (MMF) | 50 m (OM4) | Módulo SR NDR IB/ETH, perfil plano (Flat Top) |
| **MMA4Z00-NS** | 800G | OSFP | 2xMPO-12 APC| 850 nm | Multimodo (MMF) | 50 m (OM4) | Módulo SR Twin-Port 2xNDR, con disipador (Finned) |

---

## Guía de referencia sobre distancias y cableado

### 1. SR frente a SR4 frente a NDR (soluciones multimodo)
- **25G SR (SFP28)**: utiliza un latiguillo de fibra óptica multimodo duplex LC-LC estándar. Utiliza un único carril tanto para la transmisión como para la recepción.
- **100G SR4 (QSFP28)**: utiliza un latiguillo de cinta de fibra MPO de 12 fibras (MPO-12), generalmente con polaridad Tipo B, para transmitir a través de 4 carriles paralelos de 25G.
- **400G/800G NDR (OSFP)**: emplea modulación PAM4 para transmitir un ancho de banda ultraalto a través de conectores MPO-12 APC (contacto físico en ángulo). La cara del extremo en ángulo reduce al mínimo el retorno de reflexiones, lo cual es crítico en velocidades elevadas.

### 2. Monomodo (LR4/FR4) frente a Multimodo (SR/SR4)
- **Multimodo (MMF)**: adecuado para el cableado dentro de un mismo armario o entre armarios cercanos (hasta 100-150 m). Ofrece un menor coste en los transceptores.
- **Monomodo (SMF)**: necesario para distancias superiores a 150 m (hasta 10 km para LR4). Utiliza conectores dúplex LC en fibra de 9/125 µm.

---

## Recomendación técnica: módulos originales frente a compatibles de terceros

Al adquirir transceptores, los clientes suelen preguntar: *«¿Puedo utilizar transceptores compatibles de otros fabricantes?»*

### ¿Por qué recomendamos usar módulos originales NVIDIA LinkX?
1. **Compatibilidad de firmware**: las tarjetas de red NVIDIA ConnectX y los conmutadores Quantum ejecutan sistemas operativos especializados (como MLNX-OS o Onyx). Las actualizaciones de sistema suelen inhabilitar o marcar los módulos de terceros, lo que puede provocar que los puertos de red dejen de funcionar.
2. **Fiabilidad en los diagnósticos (DDM/DOM)**: los módulos originales reportan valores precisos de temperatura, tensión, potencia de transmisión (TX) y potencia de recepción (RX) directamente a los controladores del sistema (iDRAC, HPE iLO o MLNX-OS). Un reporte correcto evita alertas falsas por temperatura.
3. **Soporte de funciones avanzadas**: los módulos LinkX están certificados para admitir funciones críticas como la corrección de errores hacia adelante (FEC) de forma nativa, lo que evita la pérdida de paquetes en bases de datos y cargas de trabajo críticas.

---

¿Necesita latiguillos de fibra óptica compatibles? Consulte nuestro [catálogo de latiguillos de fibra óptica](/es/products/mellanox/cable-fiber/). Si necesita un diseño de red a medida, [contacte con el equipo técnico de Yupitek](/es/contact/).
