---
title: "¿Adaptador Wi-Fi inactivo tras actualizar el kernel de Kali Linux? Solución de errores DKMS en RTL8812AU y firmas Secure Boot MOK"
date: 2026-08-18
draft: false
slug: "kali-linux-rtl8812au-dkms-secure-boot-mok-setup"
tags:
  - "Wireless"
  - "Hardware"
categories:
  - "Wireless Hardware"
  - "Technical Guide"
description: "Guía completa para solucionar fallos de compilación DKMS del driver RTL8812AU en Kali Linux y firmar módulos del kernel con MOK bajo Secure Boot."
featureimage: "/images/blog/05_dkms_mok_flow_blueprint.jpg"
author: "benny-lai"
lastmod: 2026-08-18
faq:
  - question: "¿Se debe desactivar Secure Boot cuando se bloquean controladores no firmados?"
    answer: "No es recomendable. La práctica segura es registrar una clave MOK con mokutil para firmar los módulos manteniendo la seguridad activa."
---

![Linux Kernel DKMS and Secure Boot MOK Flowchart](/images/blog/05_dkms_mok_flow_blueprint.jpg)

## Resumen y Contexto Técnico

Guía completa para solucionar fallos de compilación DKMS del driver RTL8812AU en Kali Linux y firmar módulos del kernel con MOK bajo Secure Boot.

### Características Clave y Ventajas Arquitectónicas

- **Plataforma de Hardware**: AWUS036ACH con diseño de radiofrecuencia de alto rendimiento.
- **Compatibilidad de SO**: Compatibilidad total con distribuciones Linux modernas (Kali Linux, Ubuntu, Debian, Raspberry Pi OS).
- **Ventajas Principales**: Antenas de alta ganancia, transmisión RF estable y eliminación de tareas de compilación.

### Análisis Técnico e Implementación

Consulte el plano técnico superior para conocer los esquemas de conexión y especificaciones detalladas. En entornos críticos como robótica, FPV digital o pruebas de seguridad, la alimentación aislada y el soporte nativo garantizan la máxima confiabilidad.

### Lista de Verificación Previa

1. Confirmar la detección del dispositivo mediante `lsusb`.
2. Verificar la instalación de los paquetes de firmware actualizados (`linux-firmware`).
3. Evaluar los niveles de señal y espectro RF en el entorno de despliegue.
4. Cumplir estrictamente con la normativa local de telecomunicaciones.

