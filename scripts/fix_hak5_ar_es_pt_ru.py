#!/usr/bin/env python3
"""Fix HAK5 _index.md for ar, es, pt, ru — add all missing product cards."""

import re

BASE = "/home/yopitek/Project/yupitek_official_web"

# EN reference: all 17 HAK5 hrefs
EN_PRODUCTS_ORDER = [
    "wifi-pineapple-mark7", "wifi-pineapple-enterprise", "usb-rubber-ducky",
    "bash-bunny", "shark-jack", "key-croc", "packet-squirrel",
    "omg-cable", "omg-plug", "omg-adapter", "omg-programmer", "omg-unBlocker",
    "malicious-cable-detector", "screen-crab", "plunder-bug",
    "wifi-pineapple-pager", "shark-jack-cable"
]

# Translations for each language
CARDS = {
    "wifi-pineapple-mark7": {
        "title": "WiFi Pineapple Mark VII",
        "image": "/images/products/hak5/wifi-pineapple.png",
        "ar": "منصة مراجعة الشبكات اللاسلكية الاحترافية، 802.11 a/b/g/n/ac ثنائي النطاق.",
        "es": "Plataforma profesional de auditoría de redes inalámbricas, 802.11 a/b/g/n/ac dual-band.",
        "pt": "Plataforma profissional de auditoria de redes sem fio, 802.11 a/b/g/n/ac dual-band.",
        "ru": "Профессиональная платформа аудита беспроводных сетей, 802.11 a/b/g/n/ac, dual-band.",
    },
    "wifi-pineapple-enterprise": {
        "title": "WiFi Pineapple Enterprise",
        "image": "/images/products/hak5/wifi-pineapple-enterprise.png",
        "ar": "منصة تدقيق شبكات لاسلكية من الدرجة المؤسسية مع تصميم هوائي محسّن للتقييمات الأمنية الواسعة النطاق.",
        "es": "Plataforma de auditoría inalámbrica de grado empresarial con diseño de antena mejorado para evaluaciones de seguridad a gran escala.",
        "pt": "Plataforma de auditoria sem fio de nível empresarial com design de antena aprimorado para avaliações de segurança em larga escala.",
        "ru": "Корпоративная платформа аудита беспроводных сетей с улучшенной антенной для масштабных оценок безопасности.",
    },
    "usb-rubber-ducky": {
        "title": "USB Rubber Ducky",
        "image": "/images/products/hak5/usb-rubber-ducky.png",
        "ar": "أداة HID Injection معيارية في الصناعة — تبدو مثل محرك USB عادي.",
        "es": "Herramienta estándar de inyección HID — similar a una memoria USB convencional.",
        "pt": "Ferramenta padrão de injeção HID — parece um pendrive USB convencional.",
        "ru": "Стандартный инструмент HID-инъекций — выглядит как обычная USB-флешка.",
    },
    "bash-bunny": {
        "title": "Bash Bunny Mark II",
        "image": "/images/products/hak5/bash-bunny.png",
        "ar": "منصة هجوم USB متعددة الوظائف تدعم HID Injection ومشاركة الشبكة.",
        "es": "Plataforma de ataque USB multifuncional con inyección HID y emulación de dispositivos.",
        "pt": "Plataforma de ataque USB multifuncional com injeção HID e emulação de dispositivos.",
        "ru": "Многофункциональная USB-платформа для атак: HID-инъекции, сетевые модули.",
    },
    "shark-jack": {
        "title": "Shark Jack",
        "image": "/images/products/hak5/shark-jack.png",
        "ar": "أداة مراجعة شبكات سلكية محمولة للنشر السريع في البيئات المادية.",
        "es": "Herramienta portátil de auditoría de redes cableadas para despliegue rápido.",
        "pt": "Ferramenta portátil de auditoria de redes com fio para implantação rápida.",
        "ru": "Портативный инструмент аудита проводных сетей для быстрого развёртывания.",
    },
    "key-croc": {
        "title": "Key Croc",
        "image": "/images/products/hak5/key-croc.png",
        "ar": "مسجل لوحة مفاتيح وأداة حقن HID مع Wi-Fi مدمج للوصول عن بُعد.",
        "es": "Registrador de teclas y herramienta de inyección HID con Wi-Fi integrado para acceso remoto.",
        "pt": "Registrador de teclas e ferramenta de injeção HID com Wi-Fi integrado para acesso remoto.",
        "ru": "Кейлоггер и инструмент HID-инъекций со встроенным Wi-Fi для удалённого доступа.",
    },
    "packet-squirrel": {
        "title": "Packet Squirrel Mark II",
        "image": "/images/products/hak5/packet-squirrel.png",
        "ar": "جهاز اختبار الاعتراض على الشبكة يدعم نفق VPN والتقاط الحزم ومعالجة DNS.",
        "es": "Dispositivo de pruebas de intermediario de red con soporte para túnel VPN, captura de paquetes y manipulación DNS.",
        "pt": "Dispositivo de teste man-in-the-middle de rede com suporte a túnel VPN, captura de pacotes e manipulação DNS.",
        "ru": "Устройство для атак «человек посередине» с поддержкой VPN-туннелирования, перехвата пакетов и DNS.",
    },
    "omg-cable": {
        "title": "O.MG Cable",
        "image": "/images/products/hak5/omg-cable.png",
        "ar": "يبدو ككابل شحن عادي — يدعم HID Injection عن بعد وتسجيل لوحة المفاتيح.",
        "es": "Disfrazado como cable de carga estándar — soporta inyección HID remota y registro de teclas.",
        "pt": "Disfarçado como cabo de carregamento padrão — suporta injeção HID remota e registro de teclas.",
        "ru": "Маскируется под зарядный кабель — поддерживает удалённую HID-инъекцию и кейлоггинг.",
    },
    "omg-plug": {
        "title": "O.MG Plug",
        "image": "/images/products/hak5/omg-plug.png",
        "ar": "جهاز O.MG بشكل رأس شاحن مع إمكانية التحكم عن بُعد.",
        "es": "Dispositivo O.MG en factor de forma de cargador, oculto en una cabeza de carga con capacidad de control remoto.",
        "pt": "Dispositivo O.MG no formato de carregador, oculto em uma cabeça de carregamento com controle remoto.",
        "ru": "Устройство O.MG в форм-факторе зарядного устройства с возможностью удалённого управления.",
    },
    "omg-adapter": {
        "title": "O.MG Adapter",
        "image": "/images/products/hak5/omg-adapter.png",
        "ar": "جهاز O.MG كمحول USB يمكن توصيله بالأجهزة المستهدفة بسهولة.",
        "es": "Dispositivo O.MG como adaptador USB, fácilmente adjuntable a dispositivos objetivo.",
        "pt": "Dispositivo O.MG como adaptador USB, facilmente conectável a dispositivos alvo.",
        "ru": "Устройство O.MG в виде USB-адаптера, легко подключаемого к целевым устройствам.",
    },
    "omg-programmer": {
        "title": "O.MG Programmer",
        "image": "/images/products/hak5/omg-programmer.png",
        "ar": "مبرمج مخصص لكابل O.MG — يستخدم لكتابة البرامج الثابتة بـ DuckyScript.",
        "es": "Programador dedicado para O.MG Cable — usado para flashear firmware DuckyScript.",
        "pt": "Programador dedicado para O.MG Cable — usado para gravar firmware DuckyScript.",
        "ru": "Специализированный программатор для O.MG Cable — прошивка DuckyScript.",
    },
    "omg-unBlocker": {
        "title": "O.MG UnBlocker",
        "image": "/images/products/hak5/omg-unBlocker.png",
        "ar": "يتجاوز أجهزة حظر بيانات USB — لاختبار حلول الشحن فقط بشكل شرعي.",
        "es": "Evita dispositivos de bloqueo de datos USB — para pruebas legítimas de soluciones de solo carga.",
        "pt": "Contorna dispositivos de bloqueio de dados USB — para testes legítimos de soluções somente de carregamento.",
        "ru": "Обходит USB-блокировщики данных — для легитимного тестирования решений «только зарядка».",
    },
    "malicious-cable-detector": {
        "title": "Malicious Cable Detector",
        "image": "/images/products/hak5/malicious-cable-detector.png",
        "ar": "ماسح لاكتشاف الكابلات الخبيثة المقنّعة، يساعد في تحديد أجهزة O.MG.",
        "es": "Escáner para detectar cables maliciosos disfrazados, ayuda a identificar dispositivos tipo O.MG.",
        "pt": "Scanner para detectar cabos maliciosos disfarçados, ajudando a identificar dispositivos do tipo O.MG.",
        "ru": "Сканер для обнаружения замаскированных вредоносных кабелей, идентифицирует устройства O.MG.",
    },
    "screen-crab": {
        "title": "Screen Crab",
        "image": "/images/products/hak5/screen-crab.png",
        "ar": "جهاز التقاط HDMI بين الطرفين — يلتقط محتوى الشاشة بصمت مع إرسال لاسلكي عن بُعد.",
        "es": "Dispositivo de captura HDMI intermediario — captura silenciosamente el contenido de pantalla con transmisión remota Wi-Fi.",
        "pt": "Dispositivo de captura HDMI intermediário — captura silenciosamente o conteúdo da tela com transmissão remota Wi-Fi.",
        "ru": "Устройство перехвата HDMI — скрытно захватывает содержимое экрана с Wi-Fi-передачей.",
    },
    "plunder-bug": {
        "title": "Plunder Bug LAN Tap",
        "image": "/images/products/hak5/plunder-bug.png",
        "ar": "جهاز مراقبة شبكة محمول — يعكس حركة مرور الشبكة السلكية عبر USB-C في الوقت الفعلي.",
        "es": "Dispositivo de monitoreo de red portátil — duplica el tráfico de red cableado a través de USB-C en tiempo real.",
        "pt": "Dispositivo de monitoramento de rede portátil — espelha o tráfego de rede com fio via USB-C em tempo real.",
        "ru": "Портативный сетевой мониторинг — зеркалирует трафик проводной сети через USB-C в реальном времени.",
    },
    "wifi-pineapple-pager": {
        "title": "WiFi Pineapple Pager",
        "image": "/images/products/hak5/wifi-pineapple-pager.png",
        "ar": "أداة اختبار اختراق Wi-Fi ثلاثية النطاق بحجم الجيب، تدعم DuckyScript وشاشة ملونة 2.4\" وتنبيهات بالاهتزاز، تعمل باستقلالية تامة.",
        "es": "Herramienta de pentesting Wi-Fi tri-banda de bolsillo con payloads DuckyScript, pantalla a color de 2.4\" y alertas de vibración — completamente autónoma.",
        "pt": "Ferramenta de pentesting Wi-Fi tri-band de bolso com payloads DuckyScript, tela colorida de 2,4\" e alertas de vibração — totalmente autônoma.",
        "ru": "Карманный три-диапазонный Wi-Fi пентестинг инструмент с DuckyScript, цветным дисплеем 2.4\" и виброоповещениями.",
    },
    "shark-jack-cable": {
        "title": "Shark Jack Cable",
        "image": "/images/products/hak5/shark-jack-cable.png",
        "ar": "نسخة الكابل من Shark Jack للاتصال المباشر بمنافذ الشبكة.",
        "es": "Versión cable del Shark Jack para conexión directa a puertos de red.",
        "pt": "Versão cabo do Shark Jack para conexão direta a portas de rede.",
        "ru": "Кабельная версия Shark Jack для прямого подключения к сетевым портам.",
    },
}

LANG_FOOTERS = {
    "ar": "للاستفسار عن الأسعار، [تواصل معنا](/ar/contact/).",
    "es": "¿Necesita una cotización? [Contáctenos](/es/contact/)",
    "pt": "Precisa de um orçamento? [Entre em contato](/pt/contact/)",
    "ru": "Нужна цена? [Свяжитесь с нами](/ru/contact/)",
}


def get_existing_hrefs(content, lang):
    """Extract the product slugs already present in the file."""
    pattern = rf'href="/{lang}/products/hak5/([^/"]+)/'
    return set(re.findall(pattern, content))


def build_card_block(lang, slug):
    card = CARDS[slug]
    title = card["title"]
    image = card["image"]
    desc = card[lang]
    href = f"/{lang}/products/hak5/{slug}/"
    return (
        f'  {{{{< card title="{title}" href="{href}" image="{image}" >}}}}\n'
        f'    {desc}\n'
        f'  {{{{< /card >}}}}'
    )


for lang in ["ar", "es", "pt", "ru"]:
    path = f"{BASE}/content/{lang}/products/hak5/_index.md"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    existing = get_existing_hrefs(content, lang)
    missing_slugs = [s for s in EN_PRODUCTS_ORDER if s not in existing]

    print(f"\n{lang}: existing={sorted(existing)}")
    print(f"{lang}: missing={missing_slugs}")

    if not missing_slugs:
        print(f"{lang}: already complete, skipping")
        continue

    # Build the new cards to add
    new_cards = "\n".join(build_card_block(lang, slug) for slug in missing_slugs)

    # Insert before {{< /card-group >}}
    if "{{< /card-group >}}" in content:
        content = content.replace(
            "{{< /card-group >}}",
            new_cards + "\n{{< /card-group >}}"
        )
    else:
        print(f"WARNING: {{{{< /card-group >}}}} not found in {lang}!")
        continue

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"{lang}: wrote updated file ✓")

print("\nDone!")
