---
title: "Guía de actualización de firmware y cambio de bloqueo de marca de Sierra Wireless: el proceso correcto para evitar que el módulo quede inutilizable (Brick) (EM7455 / EM7565 / MC7455) | Yupitek"
description: "Guía completa de actualización de firmware y cambio de bloqueo de marca de los módulos Sierra Wireless (EM7455, EM7565 y MC7455): basada en las hojas de especificaciones oficiales, explica el proceso de flasheo, la verificación con AT+GMR, la copia de seguridad del firmware, el rescate de un módulo inutilizable (SED) y los pasos correctos para evitar fallos de flasheo."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "es"
hreflang_group: "sierra-firmware-update-brand-lock-guide"
slug: "sierra-firmware-update-brand-lock-guide"
tags: ["Sierra Wireless", "Firmware", "EM7455", "EM7565", "MC7455", "Brand Lock", "WWAN"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/es/products/sierra/"
faq:
  - question: "¿Flachear un módulo Sierra Wireless siempre termina dejándolo inutilizable (Brick)?"
    answer: "No necesariamente. Las especificaciones oficiales documentan el mecanismo SED (Smart Error Detection): tras 6 reinicios consecutivos, el módulo entra en modo boot-and-hold a la espera de descargar firmware, y esa es la vía de rescate oficial. Lo habitual es que un módulo quede inutilizable por cortes de corriente durante el flasheo o por flashear un firmware incompatible."
  - question: "¿Se puede cambiar el bloqueo de marca (Dell / Lenovo / Generic)?"
    answer: "Es una práctica habitual en la comunidad: se flashea una imagen de firmware diferente para cambiar la identidad del módulo y hacer que coincida con la lista blanca del BIOS. Antes de operar, asegúrese de confirmar el modelo del módulo y de preparar los archivos correctos."
  - question: "¿Qué hago si el flasheo falla y el módulo se reinicia sin parar?"
    answer: "Espere a que el módulo se reinicie 6 veces seguidas hasta entrar en modo boot-and-hold; después, vuelva a conectarlo por USB y use la herramienta de flasheo para escribir el firmware correcto y recuperarlo."
---

# Guía de actualización de firmware y cambio de bloqueo de marca de Sierra Wireless: el proceso correcto para evitar que el módulo quede inutilizable (Brick)

**Resumen en una frase: el firmware de los módulos Sierra se puede actualizar mediante «actualización inalámbrica del operador (FOTA)» o «flasheo manual por USB». En cuanto al bloqueo de marca que tanto preocupa a muchos (como la diferencia entre la versión especial de Dell o Lenovo y la versión genérica), basta con usar el paquete de firmware correcto para cambiarlo. Mientras compruebe la versión con AT+GMR antes de flashear y no corte la corriente a mitad del proceso, incluso si algo falla, el módulo cuenta con el modo de rescate integrado SED que lo salvará.**

Muchos usuarios compran módulos Sierra Wireless en el mercado de segunda mano y descubren que no funcionan al instalarlos en su portátil o router, y la causa suele ser el «bloqueo de marca (bloqueo OEM)». En este artículo combinamos el «conocimiento técnico documentado en las especificaciones oficiales» con la «experiencia práctica de la comunidad» para enseñarle a flashear el firmware con seguridad.

> Fuente de información técnica: hojas de especificaciones oficiales de Sierra Wireless (EM7455, EM7565 y MC7455). El cambio de bloqueo de marca y las herramientas de terceros forman parte de la experiencia práctica de la comunidad. Artículo elaborado por Yupitek.

---

## Comprenda los conceptos clave del flasheo en 30 segundos

Flashear no es peligroso en sí; lo peligroso es «no hacer copia de seguridad, descargar un archivo equivocado o desconectar la corriente a mitad de proceso».

| Lo que necesita saber | ¿Está en las especificaciones oficiales? | Explicación breve |
|---|---|---|
| **FOTA (actualización inalámbrica)** | ✅ Sí | El operador le envía la actualización directamente, pero depende de que el operador la admita. |
| **Flasheo por USB (herramienta oficial)** | ✅ Sí | Conecta el módulo al ordenador por cable USB y escribe el firmware manualmente; es el método más controlable. |
| **Consultar la versión de firmware (AT+GMR)** | ✅ Sí | Este comando AT muestra la versión actual del firmware; ¡imprescindible antes de flashear! |
| **Bloqueo de marca (Dell/Lenovo)** | ⚠️ No directamente | Las especificaciones solo mencionan el «soporte de etiquetado OEM»; el mecanismo concreto de bloqueo es una lista blanca que define el fabricante del portátil. |
| **qmi-firmware-update** | ⚠️ No | Es la herramienta de flasheo favorita de la comunidad Linux de código abierto. |

---

## ¿Qué es exactamente el bloqueo de marca (bloqueo OEM)?

En pocas palabras: cuando fabricantes como Dell o Lenovo compran módulos a Sierra Wireless, piden que el módulo lleve «su propio logotipo y firmware exclusivo», y además escriben una «lista blanca» en el BIOS del portátil.

Si su módulo es la versión Dell y lo inserta en un portátil Lenovo, el equipo puede quedarse bloqueado al arrancar con un error.
Si su módulo es la versión genérica (Generic) y lo inserta en un portátil con una lista blanca estricta, tampoco funcionará.

**Por eso mucha gente quiere «cambiar el bloqueo de marca»**: en realidad consiste en descargar el firmware de la marca correspondiente (o de la versión genérica) y flashearlo por USB, para que el módulo «finja» ser la versión de otra marca.

> ⚠️ **Aviso**: flashear el firmware de una marca equivocada conlleva riesgos. Antes de empezar, confirme qué versión necesita realmente su placa base.

---

## Antes de flashear: estos tres pasos le alejan del módulo inutilizable

¡No se apresure a flashear en cuanto tenga el archivo! Siga los requisitos de las especificaciones oficiales y haga estos tres pasos:

### 1. Compruebe la versión de firmware actual
Abra un terminal (como minicom o putty), conéctese al puerto AT del módulo e introduzca:
```text
AT+GMR
```
Guarde una captura de pantalla del número de versión que aparezca. Si algo sale mal, sabrá qué versión debe flashear de nuevo.

### 2. Haga una copia de seguridad de la configuración
Aunque las especificaciones no enseñan cómo hacer copias, en la práctica se recomienda anotar la configuración APN y los parámetros PRI actuales.

### 3. Entienda el «apagado seguro»
Desconectar la corriente directamente después de flashear o antes de extraer el módulo es un gran error. Las especificaciones advierten explícitamente de que cortar la corriente a secas daña el sistema de archivos del módulo.
- **EM7455 / EM7565**: debe poner el pin `Full_Card_Power_Off#` en nivel bajo y esperar unos 20 a 25 segundos antes de desconectar la corriente.
- **MC7455**: primero debe enviar el comando `AT!PCOFFEN=0`, después poner `W_DISABLE_N` en nivel bajo y esperar varias decenas de segundos antes de desconectarlo.

---

## Flasheo en la práctica: proceso de flasheo por USB

Si usa `qmi-firmware-update`, la herramienta favorita de la comunidad Linux, el proceso aproximado es el siguiente (consulte siempre la documentación oficial de la herramienta):

1. **Consiga el archivo correcto**: descargue del sitio oficial o solicite al proveedor el paquete de firmware del modelo exacto (los chips del EM7455 y el EM7565 son completamente distintos, ¡nunca mezcle los archivos!).
2. **Conecte el módulo**: asegúrese de que `lsusb` detecta el dispositivo.
3. **Detenga los programas que interfieren**: cierre servicios de red como `ModemManager` para que no ocupen el puerto USB.
4. **Ejecute la herramienta de flasheo**: cargue el archivo y ejecute.
5. **Aleje las manos del teclado**: durante el flasheo el módulo está en «estado inestable»; **está totalmente prohibido cortar la corriente o desconectar el cable.** Este es el momento en que la mayoría de la gente deja el módulo inutilizable.
6. **Reinicie y verifique**: tras flashear, apague con seguridad, reinicie y ejecute `AT+GMR` para comprobar si el número de versión ha cambiado.

---

## ¿Y si el módulo queda inutilizable? (Mecanismo de rescate SED)

Si tras el flasheo el módulo se reinicia sin parar y no entra en el sistema, ¡no se apresure a tirarlo a la basura!

Los módulos Sierra incorporan un mecanismo de rescate llamado **SED (Smart Error Detection)**.
Las especificaciones lo dejan claro: **si el módulo se cuelga y se reinicia 6 veces seguidas al arrancar, deja de intentarlo y entra en modo «boot-and-hold».**
¡Ese modo existe precisamente para dejar la puerta abierta y volver a flashear el firmware!

**Pasos de rescate:**
1. Déjelo reiniciar; al llegar a la sexta vez se quedará en silencio (modo boot-and-hold).
2. Vuelva a conectar el cable USB en ese momento.
3. Abra la herramienta de flasheo, elija un paquete de firmware que sepa que es correcto y flashee de nuevo.
4. Normalmente así consigue revivir el módulo.

> Si ni siquiera consigue conectar por USB, pruebe a activar el restablecimiento de hardware (RESET#). La duración varía según el módulo: el EM7455 tarda unos 3 a 5.5 segundos y el EM7565 de 0.2 a 2.5 segundos; si supera el tiempo, vuelve a iniciar el ciclo, así que tendrá que ajustar el ritmo.

---

## Conclusión

Flashear el firmware de un módulo Sierra Wireless o cambiar el bloqueo de marca es como flashear un teléfono: **hay un proceso estándar y un mecanismo de rescate; mientras no lo haga a lo loco, no pasará nada.**

Los errores más comunes son:
1. Descargar un firmware del modelo equivocado.
2. Dar una patada al cable de alimentación a mitad del flasheo.
3. Olvidar el apagado seguro según el procedimiento estándar.

Mientras compruebe la versión (`AT+GMR`) antes de empezar, tenga el archivo correcto y ofrezca una alimentación estable, podrá dar fácilmente una nueva vida a su tarjeta de red.

## Preguntas frecuentes (FAQ)

{{< faq >}}

## Información de compra (Llamada a la acción)

¿No está seguro de si su módulo es la versión Dell o la de Lenovo? ¿Busca módulos Sierra fiables para actualizar su equipo? Yupitek ofrece soluciones de hardware completas y asesoramiento técnico.
Escríbanos: **sales@yupitek.com**
Vea los productos: [Sección de módulos Sierra Wireless](https://yupitek.com/es/products/sierra/)
