---
title: "Del metro a los grandes almacenes: cómo las empresas pueden mejorar la experiencia presencial y el retargeting con YPB03 LINE Beacon"
description: "Guía completa para implementar YPB03 LINE Beacon: registro de HWID, configuración BLE y Webhook en Python para marketing de proximidad OMO."
date: 2026-06-26
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["YPB03", "LINE Beacon", "Bluetooth", "OMO", "IoT", "Proximity Marketing"]
featureimage: "/images/blog/ypb03-line-beacon-tutorial.jpg"
hideFeatureImage: true
---

![YPB03 LINE Beacon Concept Banner](/images/blog/ypb03-line-beacon-tutorial.jpg)

Imagine la siguiente situación: cuando un cliente entra en su tienda física, sin necesidad de descargar ninguna App adicional, LINE en su teléfono muestra automáticamente un mensaje de bienvenida, envía un cupón de descuento del día o le guía hacia los productos destacados. Esto no es magia, sino una aplicación de **LINE Beacon** que combina la tecnología de geolocalización por Bluetooth con la plataforma LINE.

Este artículo guiará a los equipos de marketing empresarial y desarrolladores de proyectos en el uso del dispositivo Bluetooth industrial de largo alcance **YPB03**, desde el registro de una cuenta de desarrollador de LINE y la configuración de los parámetros de difusión Bluetooth, hasta la implementación de un servicio Webhook con Python para la Messaging API. ¡Le ayudará a transformar el tráfico físico presencial en un activo de marketing digital de alto valor!

---

## ¿Por qué elegir YPB03 como dispositivo LINE Beacon?

Existen muchos tipos de Beacon Bluetooth en el mercado, pero para funcionar como un LINE Beacon estable, comercial o para demostraciones de proyectos, las especificaciones de hardware son fundamentales. A continuación, se presentan las características destacadas del hardware de YPB03:

* **Transmisión de ultra largo alcance (240 metros)**: Equipado con una antena de alta ganancia, alcanza una distancia de transmisión de hasta 240 metros en entornos abiertos. Ya sea en pabellones de exposiciones amplios, grandes superficies comerciales o tiendas de varias plantas, la cobertura es sencilla.
* **Autonomía de hasta 10 años**: Con 4 pilas AA estándar y una capacidad total de 5800mAh, puede funcionar cerca de 10 años con la frecuencia de transmisión predeterminada, evitando la carga de mantenimiento que supone el cambio frecuente de pilas.
* **Protección industrial IP65**: La carcasa con diseño sellado de ABS y silicona ofrece resistencia al polvo y a salpicaduras de agua, por lo que su implementación en almacenes húmedos o entornos semiexteriores es totalmente segura.
* **Instalación sencilla**: Incluye soporte de pared con tornillería para fijarlo fácilmente en paredes o pilares.

---

## Aplicaciones de marketing con LINE Beacon y casos reales en Taiwán

LINE Beacon se ha consolidado como una herramienta clave para el marketing OMO (Online-Merge-Offline, integración de los canales online y offline), ya que cubre el punto ciego de las tiendas físicas: la imposibilidad de rastrear el comportamiento del cliente. Además, permite interacciones inmediatas con alto incentivo.

### Aplicaciones habituales de marketing
* **Bienvenida inmediata y precisa**: Cuando el cliente entra en el rango (evento `enter`), se envía de inmediato un mensaje de bienvenida personalizado o un cupón canjeable al instante, interceptando con precisión a los transeúntes a la entrada.
* **Puntos interactivos y recolección de sellos**: Varios Beacon distribuidos en distintas zonas o stands de un centro comercial. Al llegar a un punto específico, el cliente desbloquea niveles o acumula puntos que, al completarse, pueden canjearse en LINE por LINE Points o regalos físicos, aumentando el atractivo de la exploración.
* **Retargeting con datos offline**: Al registrar el momento y la frecuencia con que el cliente entra en contacto con el Beacon, la marca puede realizar campañas de Retargeting a través de la plataforma publicitaria de LINE (LAP) dirigidas a este segmento preciso de clientes que «ya han visitado la tienda física».

### Casos reales en Taiwán

En Taiwán, LINE Beacon ha acumulado experiencias de aplicación muy exitosas en grandes espacios públicos y marcas reconocidas:

1. **Sorpresa en el Metro de Taipéi**:
   El Metro de Taipéi ha implementado LINE Beacon en múltiples estaciones clave de transporte (como la estación de Taipéi, Ximending, Zhongxiao Fuxing, entre otras). Los usuarios que viajan en metro, siempre que tengan activados el Bluetooth y LINE en su teléfono, reciben notificaciones de actividades. Mediante misiones de recolección de sellos como el «Tren Sorpresa del Metro», los usuarios que recopilan los puzles designados pueden canjear LINE Points de forma gratuita. Así, se transforma el tráfico diario de millones de viajes en metro en un activo de marketing digital interactivo de forma fluida.
2. **Festival de las Linternas de Taiwán (exposición inteligente con guía interactiva)**:
   En el «Festival de las Linternas de Taiwán 2023 en Taipéi», los organizadores implementaron hasta **350 LINE Beacon**, cubriendo por completo las cuatro zonas de exposición. Al acercarse los visitantes a una obra de farolillo concreta, LINE mostraba automáticamente una audioguía de la obra, recomendaciones gastronómicas cercanas (integradas con LINE Spot) o vales de taxi (integrados con LINE TAXI). Sin necesidad de hacer cola para recibir un folleto en papel, el teléfono se convertía en un guía personal en la nube.
3. **Captación de tráfico en el aniversario de SOGO**:
   SOGO aprovechó su proximidad a las estaciones de metro y desplegó LINE Beacon en las salidas de metro y los alrededores del centro comercial. Durante la campaña de aniversario, cuando un consumidor potencial se acercaba al centro, su teléfono recibía automáticamente un recordatorio promocional. En apenas 4 días se generaron 5 millones de impresiones y más de 1 millón de alcance efectivo, logrando interceptar a los «transeúntes» fuera del establecimiento y dirigirlos hacia las compras dentro de la tienda.
4. **Campaña de marketing de Let's Café en FamilyMart**:
   FamilyMart aprovechó su densa red de tiendas en toda la isla para implementar Beacon. Junto con una campaña temática, lanzó un juego online que guiaba a los consumidores a activar el LINE Beacon dentro del establecimiento para obtener un cupón de descuento para un café helado de Let's Café, aumentando considerablemente la actividad de los socios y la intención de compra presencial.
5. **Atracción de tráfico en los mostradores de belleza de Shiseido**:
   Shiseido instaló LINE Beacon en múltiples mostradores de grandes almacenes de toda la isla. Cuando un consumidor se acercaba al mostrador de cosméticos, el sistema enviaba automáticamente un vale para canjear muestras de nuevos productos, guiando a los transeúntes a interactuar con el personal del mostrador y aumentando eficazmente la tasa de acercamiento y la conversión posterior de prueba de productos.

---

## Paso 1: Registrar una cuenta oficial de LINE y obtener el Hardware ID (HWID)

Para que LINE reconozca nuestro dispositivo YPB03, primero debemos solicitar en la consola de desarrolladores de LINE un «número de identificación de dispositivo» exclusivo, conocido como Hardware ID (HWID).

1. **Acceder a la plataforma LINE Developers**:
   Inicie sesión en [LINE Developers Console](https://developers.line.biz/) con su cuenta de LINE.
2. **Crear un Provider y un Channel**:
   - Cree un nuevo **Provider** (puede usar el nombre de su estudio o proyecto académico).
   - Dentro de ese Provider, cree un Channel de tipo **Messaging API** (esto creará una cuenta oficial de LINE, también denominada LINE Bot).
3. **Acceder al panel de gestión de la cuenta oficial de LINE**:
   - Inicie sesión en [LINE Official Account Manager](https://manager.line.me/).
   - Seleccione la cuenta oficial que acaba de crear y haga clic en «Configuración» en la esquina superior derecha.
   - En el menú lateral, localice «Messaging API» y confirme que la API esté activada.
4. **Solicitar el dispositivo LINE Beacon**:
   - En la misma página de configuración de Messaging API, haga clic en **«Register LINE Beacon device»** (registro de dispositivo LINE Beacon asociado).
   - Siga las instrucciones en pantalla para enviar la solicitud. El sistema de LINE generará de forma aleatoria un **Hardware ID (HWID)** de **5 bytes (10 caracteres hexadecimales)** (por ejemplo: `0123456789`). Anote este HWID, ya que lo utilizaremos al configurar los parámetros Bluetooth.

---

## Paso 2: Configurar el dispositivo YPB03 con la App BeaconSET+

Una vez obtenido el HWID, debemos «escribir» este número en el Beacon Bluetooth YPB03 y hacer que difunda según el formato especificado por LINE.

### 1. Instalar la herramienta de configuración
Descargue e instale en su teléfono el software oficial de configuración de Minew:
* Usuarios de iOS: busquen **BeaconSET+** en la App Store
* Usuarios de Android: busquen **BeaconSET+** en Google Play

### 2. Conectarse al YPB03
1. Active la función Bluetooth del teléfono y abra la App **BeaconSET+**.
2. En la lista de dispositivos, busque el que se llama `YPB03` o el que corresponda a su dirección MAC.
3. Haga clic en conectar; la App solicitará una contraseña. La contraseña predeterminada es `minew123` (recomendamos cambiarla tras la conexión para garantizar la seguridad).

### 3. Configurar el SLOT de difusión LINE Simple Beacon
YPB03 admite la difusión simultánea en varios canales. Vamos a configurar uno de los SLOT en el formato exclusivo de LINE:
1. Tras la conexión, seleccione un SLOT de difusión no utilizado.
2. Cambie el **Frame Type** a **Service Data**.
3. Configure los dos parámetros clave siguientes:
   * **Service UUID**: introduzca `FE6F` (es el Service UUID estándar exclusivo de LINE Beacon).
   * **Data Value**: introduzca los datos hexadecimales de 9 bytes ya ensamblados. La fórmula de ensamblaje es:
     $$\text{Data Value} = \text{Service UUID (FE6F)} + \text{su HWID de 5 bytes} + \text{marca final (7F00)}$$
     *Ejemplo: si su HWID es `0123456789`, deberá introducir en el campo Data Value: `FE6F01234567897F00`*.
4. Tras completar la configuración, haga clic en **Save** en la esquina superior derecha.
5. Desconecte. En este momento, ¡YPB03 ya está difundiendo oficialmente la señal LINE Beacon!

---

## Paso 3: Escribir el código del Webhook en Python para recibir señales

Cuando el teléfono del usuario se acerca al YPB03, la App de LINE detecta la difusión Bluetooth y envía una petición HTTP POST (es decir, un Webhook) a través de la plataforma LINE hacia nuestro servidor backend.

A continuación, utilizaremos **Flask**, el framework web ligero de Python, para montar este servidor Webhook y analizar los eventos de proximidad del usuario.

### 1. Instalar las dependencias necesarias
Ejecute el siguiente comando en la terminal para instalar Flask:
```bash
pip install Flask
```

### 2. Escribir el código (`app.py`)
Cree un archivo `app.py` y pegue el siguiente código:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# LINE Developers 註冊的 HWID（這裡改為您申請到的 HWID）
TARGET_HWID = "0123456789"

@app.route("/callback", methods=["POST"])
def callback():
    # 取得 LINE 平台傳過來的 JSON 資料
    body = request.get_json()
    
    if not body or "events" not in body:
        return jsonify({"status": "error", "message": "No events found"}), 400

    # 巡檢所有的事件
    for event in body["events"]:
        # 篩選事件類型為 beacon 的事件
        if event.get("type") == "beacon":
            user_id = event["source"].get("userId")
            reply_token = event.get("replyToken")
            
            beacon_data = event.get("beacon", {})
            hwid = beacon_data.get("hwid")
            beacon_type = beacon_data.get("type") # enter (進入), stay (逗留), banner (點擊橫幅)
            
            print(f"收到 Beacon 事件！使用者 ID: {user_id}")
            print(f"設備 HWID: {hwid} | 觸發類型: {beacon_type}")
            
            # 判斷是否為我們的 YPB03 設備
            if hwid == TARGET_HWID:
                if beacon_type == "enter":
                    print("--> 使用者進入了 YPB03 範圍！觸發迎賓機制。")
                    # 在這裡，您可以呼叫 LINE Messaging API 送出歡迎折價券給 user_id
                elif beacon_type == "stay":
                    print("--> 使用者持續在範圍內...")
                elif beacon_type == "banner":
                    print("--> 使用者點擊了聊天室上方的 LINE Beacon 橫幅！")
                    
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # 本地測試執行在 5000 端口
    app.run(port=5000)
```

### 3. Prueba local y exposición a Internet
La plataforma LINE necesita que el Webhook se entregue a una URL HTTPS pública. Durante la fase de desarrollo, podemos utilizar **ngrok** para crear un túnel que exponga nuestro servicio local a Internet:
1. Inicie el servicio de Python:
   ```bash
   python app.py
   ```
2. Descargue y ejecute ngrok para mapear el puerto local 5000 a una URL pública:
   ```bash
   ngrok http 5000
   ```
3. ngrok proporcionará una URL aleatoria que empieza por `https://` (por ejemplo, `https://xxxx.ngrok-free.app`). Copie esta URL, añada `/callback` al final y péguela en el campo **Webhook URL** del Channel en LINE Developers Console (por ejemplo, `https://xxxx.ngrok-free.app/callback`). Luego, haga clic en **Verify** para probar la conexión.

---

## Verificación y pruebas sobre el terreno

1. Confirme que el **Bluetooth** del teléfono esté activado.
2. Verifique que LINE esté instalado en el teléfono y que, en la configuración, se haya aceptado activar la función de recepción de **LINE Beacon** (ruta: App de LINE -> Configuración -> Privacidad -> LINE Beacon -> marcar para aceptar).
3. Añada su cuenta oficial de LINE como amiga.
4. Con el teléfono en la mano, acérquese lentamente al rango de difusión del YPB03 (en este momento, puede reducir manualmente la potencia de transmisión para facilitar las pruebas en interiores).
5. Consulte la consola de Python y verá los mensajes de log en tiempo real:
   ```text
   收到 Beacon 事件！使用者 ID: U1234567890abcdef...
   設備 HWID: 0123456789 | 觸發類型: enter
   --> 使用者進入了 YPB03 範圍！觸發迎賓機制。
   ```

---

## Tabla de parámetros clave de YPB03

| Parámetro técnico | Valor de especificación / configuración | Descripción |
| :--- | :--- | :--- |
| **Especificación Bluetooth** | BLE 5.0 (nRF52 series) | Transmisión de bajo consumo y alta eficiencia |
| **Service UUID predeterminado** | `0xFE6F` | Identificador de servicio exclusivo de LINE Beacon |
| **Herramienta de configuración** | **BeaconSET+** | Admite configuración inalámbrica en iOS y Android |
| **Nivel de protección** | IP65 | Diseño resistente al polvo y salpicaduras, apto para entornos industriales o semiexteriores |
| **Especificación de alimentación** | 4 × pilas AA (5800mAh) | Autonomía de hasta 10 años (según el intervalo de difusión) |
| **Fórmula del campo Service Data** | `FE6F` + `[HWID de 5 bytes]` + `7F00` | Valor hexadecimal que se escribe en BeaconSET+ |

---

## Preguntas frecuentes (FAQ)

#### P: ¿YPB03 solo se puede utilizar como LINE Beacon?
**R**: No. YPB03 es un dispositivo Beacon Bluetooth multifunción. Además de admitir el protocolo LINE Simple Beacon, también puede activar simultáneamente la difusión estándar **iBeacon** y **Eddystone**. Los desarrolladores pueden usar un SLOT para difundir iBeacon con fines de geolocalización para una App propia, y otro SLOT para difundir LINE Beacon con fines de marketing sin necesidad de instalación.

#### P: Al configurar BeaconSET+, ¿por qué el teléfono no detecta el dispositivo YPB03?
**R**: Verifique los siguientes puntos:
1. Asegúrese de que YPB03 tenga las pilas instaladas y esté encendido (normalmente, dispone de un botón lateral en el encendido o el LED parpadea la primera vez que recibe corriente).
2. El Bluetooth y el servicio de ubicación (GPS) del teléfono deben estar activados, y debe concederse permiso de ubicación a la App BeaconSET+.
3. Si el dispositivo ya está conectado y en uso por otro teléfono, no se podrá detectar temporalmente; asegúrese de que los demás dispositivos de configuración estén desconectados.

#### P: ¿Cuál es la diferencia entre el evento `stay` y el evento `enter` de LINE Beacon?
**R**:
- Evento **`enter`**: se activa una sola vez cuando el usuario «entra por primera vez» en el rango de cobertura Bluetooth del Beacon. Es ideal para enviar mensajes de bienvenida o cupones del día.
- Evento **`stay`**: cuando el usuario permanece dentro del rango de señal del Beacon, la plataforma LINE envía un evento `stay` aproximadamente cada 10 segundos. Puede utilizarse para calcular el tiempo de permanencia del usuario en esa zona, pero en escenarios de alta concurrencia conviene prestar atención a la capacidad del servidor.

---

## Conclusión

Gracias al Beacon Bluetooth industrial YPB03, los establecimientos físicos pueden, con el mínimo coste de mantenimiento y sin necesidad de desarrollar una App propia, interactuar de forma fluida con la gran base de usuarios de LINE y lograr una integración perfecta entre los canales online y offline (OMO). Ya sea para una demostración de proyecto académico o para un despliegue comercial a gran escala, YPB03 es la opción de referencia por su estabilidad y cobertura.

Para obtener una oferta del dispositivo YPB03 o conocer más soluciones IoT personalizadas, le invitamos a [ponerse en contacto con nosotros a través del sitio web oficial de Yupitek](https://www.yupitek.com/es/contact/).
