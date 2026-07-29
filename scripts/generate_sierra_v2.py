#!/usr/bin/env python3
"""
Generate Sierra Wireless cellular module product pages across 10 locales.
zh-tw is the source language; translation data drives all other locales.
"""
import os

# ── Constants ────────────────────────────────────────────────────────────────

LANGUAGES = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]

PRODUCTS = ["em7430", "em7455", "em7511", "em7565", "em9190", "em9191",
            "mc7304", "mc7350", "mc7354", "mc7455"]

PARENT_NAMES = {
    "zh-tw": "產品", "zh-cn": "产品", "en": "Products", "ja": "製品",
    "ar": "المنتجات", "es": "Productos", "pt": "Produtos",
    "ru": "Продукты", "de": "Produkte", "fr": "Produits"
}


# ── Section headers (locale mapping) ─────────────────────────────────────────

SECTION_HEADERS = {
    "zh-tw": {
        "法律免責聲明": "法律免責聲明", "產品概述": "產品概述",
        "主要特點": "主要特點", "技術規格": "技術規格",
        "作業系統支援": "作業系統支援", "包裝內容": "包裝內容",
        "資源與連結": "資源與連結", "產品線": "產品線",
        "規格比較": "規格比較",
    },
    "zh-cn": {
        "法律免責聲明": "法律免责声明", "產品概述": "产品概述",
        "主要特點": "主要特点", "技術規格": "技术规格",
        "作業系統支援": "操作系统支持", "包裝內容": "包装内容",
        "資源與連結": "资源与链接", "產品線": "产品线",
        "規格比較": "规格比较",
    },
    "en": {
        "法律免責聲明": "Legal Disclaimer", "產品概述": "Product Overview",
        "主要特點": "Key Features", "技術規格": "Technical Specifications",
        "作業系統支援": "OS Support", "包裝內容": "Package Contents",
        "資源與連結": "Resources & Links", "產品線": "Product Line",
        "規格比較": "Specification Comparison",
    },
    "ja": {
        "法律免責聲明": "法的免責事項", "產品概述": "製品概要",
        "主要特點": "主な特長", "技術規格": "技術仕様",
        "作業系統支援": "対応OS", "包裝內容": "同梱内容",
        "資源與連結": "リソースとリンク", "產品線": "製品ライン",
        "規格比較": "仕様比較",
    },
    "ar": {
        "法律免責聲明": "إخلاء المسؤولية القانوني",
        "產品概述": "نظرة عامة على المنتج",
        "主要特點": "الميزات الرئيسية",
        "技術規格": "المواصفات الفنية",
        "作業系統支援": "دعم أنظمة التشغيل",
        "包裝內容": "محتويات العبوة",
        "資源與連結": "الموارد والروابط",
        "產品線": "مجموعة المنتجات",
        "規格比較": "مقارنة المواصفات",
    },
    "es": {
        "法律免責聲明": "Aviso Legal",
        "產品概述": "Descripción del Producto",
        "主要特點": "Características Principales",
        "技術規格": "Especificaciones Técnicas",
        "作業系統支援": "Sistemas Operativos Compatibles",
        "包裝內容": "Contenido del Paquete",
        "資源與連結": "Recursos y Enlaces",
        "產品線": "Línea de Productos",
        "規格比較": "Comparativa de Especificaciones",
    },
    "pt": {
        "法律免責聲明": "Aviso Legal",
        "產品概述": "Visão Geral do Produto",
        "主要特點": "Principais Recursos",
        "技術規格": "Especificações Técnicas",
        "作業系統支援": "Suporte a SO",
        "包裝內容": "Conteúdo da Embalagem",
        "資源與連結": "Recursos e Links",
        "產品線": "Linha de Produtos",
        "規格比較": "Comparação de Especificações",
    },
    "ru": {
        "法律免責聲明": "Юридическое предупреждение",
        "產品概述": "Обзор продукта",
        "主要特點": "Ключевые особенности",
        "技術規格": "Технические характеристики",
        "作業系統支援": "Поддержка ОС",
        "包裝內容": "Комплектация",
        "資源與連結": "Ресурсы и ссылки",
        "產品線": "Линейка продуктов",
        "規格比較": "Сравнение характеристик",
    },
    "de": {
        "法律免責聲明": "Rechtlicher Hinweis",
        "產品概述": "Produktübersicht",
        "主要特點": "Hauptmerkmale",
        "技術規格": "Technische Spezifikationen",
        "作業系統支援": "Betriebssystemunterstützung",
        "包裝內容": "Lieferumfang",
        "資源與連結": "Ressourcen und Links",
        "產品線": "Produktlinie",
        "規格比較": "Spezifikationsvergleich",
    },
    "fr": {
        "法律免責聲明": "Avis de non-responsabilité légal",
        "產品概述": "Présentation du produit",
        "主要特點": "Caractéristiques principales",
        "技術規格": "Spécifications techniques",
        "作業系統支援": "Systèmes d'exploitation supportés",
        "包裝內容": "Contenu de l'emballage",
        "資源與連結": "Ressources et liens",
        "產品線": "Gamme de produits",
        "規格比較": "Comparaison des spécifications",
    },
}


# ── Spec labels per locale ───────────────────────────────────────────────────

SPEC_LABELS = {
    "zh-tw": {
        "晶片型號": "晶片型號", "蜂窩標準": "蜂窩標準", "下載速度": "下載速度",
        "上傳速度": "上傳速度", "載波聚合": "載波聚合", "5G 支援": "5G 支援",
        "mmWave 支援": "mmWave 支援", "LTE 類別": "LTE 類別", "介面": "介面",
        "外型規格": "外型規格", "尺寸": "尺寸", "重量": "重量",
        "工作溫度": "工作溫度", "驅動程式": "驅動程式", "GNSS": "GNSS",
        "認證": "認證", "地區": "地區", "功耗": "功耗",
        "天線介面": "天線介面", "供電電壓": "供電電壓", "韌體更新": "韌體更新",
    },
    "zh-cn": {
        "晶片型號": "芯片型号", "蜂窩標準": "蜂窝标准", "下載速度": "下载速度",
        "上傳速度": "上传速度", "載波聚合": "载波聚合", "5G 支援": "5G 支持",
        "mmWave 支援": "mmWave 支持", "LTE 類別": "LTE 类别", "介面": "接口",
        "外型規格": "外形规格", "尺寸": "尺寸", "重量": "重量",
        "工作溫度": "工作温度", "驅動程式": "驱动程序", "GNSS": "GNSS",
        "認證": "认证", "地區": "地区", "功耗": "功耗",
        "天線介面": "天线接口", "供電電壓": "供电电压", "韌體更新": "固件更新",
    },
    "en": {
        "晶片型號": "Chipset", "蜂窩標準": "Cellular Standard",
        "下載速度": "Download Speed", "上傳速度": "Upload Speed",
        "載波聚合": "Carrier Aggregation", "5G 支援": "5G Support",
        "mmWave 支援": "mmWave Support", "LTE 類別": "LTE Category",
        "介面": "Interface", "外型規格": "Form Factor", "尺寸": "Dimensions",
        "重量": "Weight", "工作溫度": "Operating Temperature",
        "驅動程式": "Driver", "GNSS": "GNSS",
        "認證": "Certifications", "地區": "Region", "功耗": "Power Consumption",
        "天線介面": "Antenna Interface", "供電電壓": "Supply Voltage",
        "韌體更新": "Firmware Update",
    },
    "ja": {
        "晶片型號": "チップセット", "蜂窩標準": "セルラー規格",
        "下載速度": "ダウンロード速度", "上傳速度": "アップロード速度",
        "載波聚合": "キャリアアグリゲーション", "5G 支援": "5G対応",
        "mmWave 支援": "ミリ波対応", "LTE 類別": "LTEカテゴリ",
        "介面": "インターフェース", "外型規格": "フォームファクタ",
        "尺寸": "寸法", "重量": "重量", "工作溫度": "動作温度",
        "驅動程式": "ドライバー", "GNSS": "GNSS",
        "認證": "認証", "地區": "地域", "功耗": "消費電力",
        "天線介面": "アンテナインターフェース", "供電電壓": "供給電圧",
        "韌體更新": "ファームウェア更新",
    },
    "ar": {
        "晶片型號": "رقاقة", "蜂窩標準": "معيار الشبكة الخلوية",
        "下載速度": "سرعة التحميل", "上傳速度": "سرعة الرفع",
        "載波聚合": "تجميع الموجات", "5G 支援": "دعم 5G",
        "mmWave 支援": "دعم mmWave", "LTE 類別": "فئة LTE",
        "介面": "الواجهة", "外型規格": "شكل المنتج", "尺寸": "الأبعاد",
        "重量": "الوزن", "工作溫度": "درجة حرارة التشغيل",
        "驅動程式": "برنامج التشغيل", "GNSS": "GNSS",
        "認證": "الشهادات", "地區": "المنطقة", "功耗": "استهلاك الطاقة",
        "天線介面": "واجهة الهوائي", "供電電壓": "جهد الإمداد",
        "韌體更新": "تحديث البرامج الثابتة",
    },
    "es": {
        "晶片型號": "Chipset", "蜂窩標準": "Estándar Celular",
        "下載速度": "Velocidad de Descarga", "上傳速度": "Velocidad de Carga",
        "載波聚合": "Agregación de Portadoras", "5G 支援": "Soporte 5G",
        "mmWave 支援": "Soporte mmWave", "LTE 類別": "Categoría LTE",
        "介面": "Interfaz", "外型規格": "Factor de Forma",
        "尺寸": "Dimensiones", "重量": "Peso",
        "工作溫度": "Temperatura de Operación", "驅動程式": "Controlador",
        "GNSS": "GNSS", "認證": "Certificaciones", "地區": "Región",
        "功耗": "Consumo de Energía", "天線介面": "Interfaz de Antena",
        "供電電壓": "Voltaje de Alimentación",
        "韌體更新": "Actualización de Firmware",
    },
    "pt": {
        "晶片型號": "Chipset", "蜂窩標準": "Padrão Celular",
        "下載速度": "Velocidade de Download", "上傳速度": "Velocidade de Upload",
        "載波聚合": "Agregação de Portadoras", "5G 支援": "Suporte 5G",
        "mmWave 支援": "Suporte mmWave", "LTE 類別": "Categoria LTE",
        "介面": "Interface", "外型規格": "Fator de Forma",
        "尺寸": "Dimensões", "重量": "Peso",
        "工作溫度": "Temperatura de Operação", "驅動程式": "Driver",
        "GNSS": "GNSS", "認證": "Certificações", "地區": "Região",
        "功耗": "Consumo de Energia", "天線介面": "Interface de Antena",
        "供電電壓": "Tensão de Alimentação",
        "韌體更新": "Atualização de Firmware",
    },
    "ru": {
        "晶片型號": "Чипсет", "蜂窩標準": "Сотовый стандарт",
        "下載速度": "Скорость загрузки", "上傳速度": "Скорость отдачи",
        "載波聚合": "Агрегация несущих", "5G 支援": "Поддержка 5G",
        "mmWave 支援": "Поддержка mmWave", "LTE 類別": "Категория LTE",
        "介面": "Интерфейс", "外型規格": "Форм-фактор",
        "尺寸": "Размеры", "重量": "Вес",
        "工作溫度": "Рабочая температура", "驅動程式": "Драйвер",
        "GNSS": "GNSS", "認證": "Сертификация", "地區": "Регион",
        "功耗": "Энергопотребление", "天線介面": "Антенный интерфейс",
        "供電電壓": "Напряжение питания",
        "韌體更新": "Обновление прошивки",
    },
    "de": {
        "晶片型號": "Chipsatz", "蜂窩標準": "Mobilfunkstandard",
        "下載速度": "Downloadgeschwindigkeit", "上傳速度": "Uploadgeschwindigkeit",
        "載波聚合": "Trägeraggregation", "5G 支援": "5G-Unterstützung",
        "mmWave 支援": "mmWave-Unterstützung", "LTE 類別": "LTE-Kategorie",
        "介面": "Schnittstelle", "外型規格": "Bauform", "尺寸": "Abmessungen",
        "重量": "Gewicht", "工作溫度": "Betriebstemperatur",
        "驅動程式": "Treiber", "GNSS": "GNSS",
        "認證": "Zertifizierungen", "地區": "Region", "功耗": "Stromverbrauch",
        "天線介面": "Antennenschnittstelle", "供電電壓": "Versorgungsspannung",
        "韌體更新": "Firmware-Update",
    },
    "fr": {
        "晶片型號": "Chipset", "蜂窩標準": "Norme cellulaire",
        "下載速度": "Débit descendant", "上傳速度": "Débit montant",
        "載波聚合": "Agrégation de porteuses", "5G 支援": "Support 5G",
        "mmWave 支援": "Support mmWave", "LTE 類別": "Catégorie LTE",
        "介面": "Interface", "外型規格": "Facteur de forme",
        "尺寸": "Dimensions", "重量": "Poids",
        "工作溫度": "Température de fonctionnement", "驅動程式": "Pilote",
        "GNSS": "GNSS", "認證": "Certifications", "地區": "Région",
        "功耗": "Consommation électrique", "天線介面": "Interface antenne",
        "供電電壓": "Tension d'alimentation",
        "韌體更新": "Mise à jour du firmware",
    },
}


# ── Legal disclaimers per locale ─────────────────────────────────────────────

LEGAL = {
    "zh-tw": "**法律免責聲明**：本產品為蜂窩通訊模組，使用前請確保符合當地法規與電信監理要求。未經授權的修改或使用可能違反法律。",
    "zh-cn": "**法律免责声明**：本产品为蜂窝通讯模块，使用前请确保符合当地法规与电信监管要求。未经授权的修改或使用可能违反法律。",
    "en": "**Legal Disclaimer**: This is a cellular communication module. Ensure compliance with local regulations and telecommunications requirements before use. Unauthorized modification or use may violate applicable laws.",
    "ja": "**法的免責事項**：本製品はセルラー通信モジュールです。ご使用の前に現地の規制および電気通信要件に準拠していることを確認してください。許可されていない改造や使用は法律違反となる可能性があります。",
    "ar": "**إخلاء المسؤولية القانوني**: هذه وحدة اتصالات خلوية. تأكد من الامتثال للوائح المحلية ومتطلبات الاتصالات قبل الاستخدام. قد يؤدي التعديل أو الاستخدام غير المصرح به إلى انتهاك القوانين.",
    "es": "**Aviso Legal**: Este es un módulo de comunicación celular. Asegúrese de cumplir con las regulaciones locales y los requisitos de telecomunicaciones antes de su uso. La modificación o uso no autorizado puede violar las leyes aplicables.",
    "pt": "**Aviso Legal**: Este é um módulo de comunicação celular. Certifique-se de cumprir os regulamentos locais e requisitos de telecomunicações antes do uso. Modificação ou uso não autorizado pode violar as leis aplicáveis.",
    "ru": "**Юридическое предупреждение**: Это модуль сотовой связи. Перед использованием убедитесь в соблюдении местных нормативных требований и требований к телекоммуникациям. Несанкционированная модификация или использование может нарушить законодательство.",
    "de": "**Rechtlicher Hinweis**: Dies ist ein Mobilfunkmodul. Stellen Sie vor der Verwendung die Einhaltung der örtlichen Vorschriften und Telekommunikationsanforderungen sicher. Unbefugte Änderungen oder Nutzung können gegen geltendes Recht verstoßen.",
    "fr": "**Avis de non-responsabilité légal** : Ce module de communication cellulaire. Assurez-vous de respecter les réglementations locales et les exigences en matière de télécommunications avant utilisation. Toute modification ou utilisation non autorisée peut enfreindre les lois applicables.",
}

# ── CTA per locale ──────────────────────────────────────────────────────────

CTA = {
    "zh-tw": "需要詢問產品報價？請來信[與我們聯絡](/zh-tw/contact/)",
    "zh-cn": "需要询问产品报价？请来信[与我们联系](/zh-cn/contact/)",
    "en": "Need a product quotation? Please [contact us](/en/contact/)",
    "ja": "製品のお見積もりをご希望ですか？[お問い合わせ](/ja/contact/)ください",
    "ar": "هل تحتاج إلى عرض سعر للمنتج؟ يرجى [الاتصال بنا](/ar/contact/)",
    "es": "Necesita una cotización del producto? Por favor [contáctenos](/es/contact/)",
    "pt": "Precisa de uma cotação do produto? [Entre em contato](/pt/contact/)",
    "ru": "Нужно коммерческое предложение? [Свяжитесь с нами](/ru/contact/)",
    "de": "Benötigen Sie ein Produktangebot? Bitte [kontaktieren Sie uns](/de/contact/)",
    "fr": "Besoin d'un devis pour le produit ? Veuillez [nous contacter](/fr/contact/)",
}

# ── Overview page data per locale ────────────────────────────────────────────

OVERVIEW_DATA = {
    "zh-tw": {
        "title": "Sierra Wireless 蜂窩模組系列",
        "desc": "代理 Sierra Wireless 全系列工業級蜂窩模組：EM7430、EM7455、EM7511、EM7565、EM9190、EM9191、MC7304、MC7350、MC7354、MC7455。適用於 IoT、M2M、路由器和行動寬頻應用。",
        "intro": "Sierra Wireless 是工業蜂窩模組領域的全球領導品牌，提供從 LTE Cat 4 到 5G NR 的完整產品線。Yupitek 代理 Sierra Wireless 全系列蜂窩模組，適用於物聯網 (IoT) 終端、工業路由器、閘道器、車聯網及行動寬頻設備，支援全球各大電信頻段。",
        "prod_title": "產品線",
        "card_desc": "工業級蜂窩模組，適用於 IoT、M2M 與行動寬頻應用。",
    },
    "zh-cn": {
        "title": "Sierra Wireless 蜂窝模块系列",
        "desc": "代理 Sierra Wireless 全系列工业级蜂窝模块：EM7430、EM7455、EM7511、EM7565、EM9190、EM9191、MC7304、MC7350、MC7354、MC7455。适用于 IoT、M2M、路由器和移动宽带应用。",
        "intro": "Sierra Wireless 是工业蜂窝模块领域的全球领导品牌，提供从 LTE Cat 4 到 5G NR 的完整产品线。Yupitek 代理 Sierra Wireless 全系列蜂窝模块，适用于物联网 (IoT) 终端、工业路由器、网关、车联网及移动宽带设备，支持全球各大电信频段。",
        "prod_title": "产品线",
        "card_desc": "工业级蜂窝模块，适用于 IoT、M2M 与移动宽带应用。",
    },
    "en": {
        "title": "Sierra Wireless Cellular Module Series",
        "desc": "Authorized distributor of Sierra Wireless industrial cellular modules: EM7430, EM7455, EM7511, EM7565, EM9190, EM9191, MC7304, MC7350, MC7354, MC7455. Ideal for IoT, M2M, routers, and mobile broadband applications.",
        "intro": "Sierra Wireless is a global leader in industrial cellular modules, offering a complete product line from LTE Cat 4 to 5G NR. Yupitek distributes the full Sierra Wireless cellular module portfolio, suitable for IoT terminals, industrial routers, gateways, connected vehicles, and mobile broadband devices with support for major global carrier bands.",
        "prod_title": "Product Line",
        "card_desc": "Industrial cellular modules for IoT, M2M, and mobile broadband applications.",
    },
    "ja": {
        "title": "Sierra Wireless セルラーモジュールシリーズ",
        "desc": "Sierra Wireless 産業用セルラーモジュールを取り扱い：EM7430、EM7455、EM7511、EM7565、EM9190、EM9191、MC7304、MC7350、MC7354、MC7455。IoT、M2M、ルーター、モバイルブロードバンド用途に最適。",
        "intro": "Sierra Wireless は産業用セルラーモジュールの世界的リーダーであり、LTE Cat 4 から 5G NR までの完全な製品ラインを提供しています。Yupitek は Sierra Wireless の全セルラーモジュールポートフォリオを取り扱い、IoT端末、産業用ルーター、ゲートウェイ、コネクテッドビークル、モバイルブロードバンド機器に適しています。",
        "prod_title": "製品ライン",
        "card_desc": "IoT、M2M、モバイルブロードバンド用途向け産業用セルラーモジュール。",
    },
    "ar": {
        "title": "سلسلة وحدات Sierra Wireless الخلوية",
        "desc": "موزع معتمد لوحدات Sierra Wireless الخلوية الصناعية: EM7430، EM7455، EM7511، EM7565، EM9190، EM9191، MC7304، MC7350، MC7354، MC7455. مثالية لتطبيقات IoT و M2M وأجهزة التوجيه والنطاق العريض المتنقل.",
        "intro": "Sierra Wireless هي شركة رائدة عالمياً في مجال الوحدات الخلوية الصناعية، وتقدم مجموعة منتجات كاملة من LTE Cat 4 إلى 5G NR. تقوم Yupitek بتوزيع مجموعة وحدات Sierra Wireless الخلوية الكاملة، المناسبة لأجهزة IoT وأجهزة التوجيه الصناعية والبوابات والمركبات المتصلة وأجهزة النطاق العريض المتنقل.",
        "prod_title": "مجموعة المنتجات",
        "card_desc": "وحدات خلوية صناعية لتطبيقات IoT و M2M والنطاق العريض المتنقل.",
    },
    "es": {
        "title": "Serie de Módulos Celulares Sierra Wireless",
        "desc": "Distribuidor autorizado de módulos celulares industriales Sierra Wireless: EM7430, EM7455, EM7511, EM7565, EM9190, EM9191, MC7304, MC7350, MC7354, MC7455. Ideales para IoT, M2M, enrutadores y aplicaciones de banda ancha móvil.",
        "intro": "Sierra Wireless es líder mundial en módulos celulares industriales, ofreciendo una línea completa desde LTE Cat 4 hasta 5G NR. Yupitek distribuye el portafolio completo de módulos celulares Sierra Wireless, adecuados para terminales IoT, enrutadores industriales, pasarelas, vehículos conectados y dispositivos de banda ancha móvil.",
        "prod_title": "Línea de Productos",
        "card_desc": "Módulos celulares industriales para aplicaciones IoT, M2M y banda ancha móvil.",
    },
    "pt": {
        "title": "Série de Módulos Celulares Sierra Wireless",
        "desc": "Distribuidor autorizado de módulos celulares industriais Sierra Wireless: EM7430, EM7455, EM7511, EM7565, EM9190, EM9191, MC7304, MC7350, MC7354, MC7455. Ideal para IoT, M2M, roteadores e aplicações de banda larga móvel.",
        "intro": "A Sierra Wireless é líder global em módulos celulares industriais, oferecendo uma linha completa de produtos desde LTE Cat 4 até 5G NR. A Yupitek distribui o portfólio completo de módulos celulares Sierra Wireless, adequados para terminais IoT, roteadores industriais, gateways, veículos conectados e dispositivos de banda larga móvel.",
        "prod_title": "Linha de Produtos",
        "card_desc": "Módulos celulares industriais para aplicações IoT, M2M e banda larga móvel.",
    },
    "ru": {
        "title": "Серия сотовых модулей Sierra Wireless",
        "desc": "Авторизованный дистрибьютор промышленных сотовых модулей Sierra Wireless: EM7430, EM7455, EM7511, EM7565, EM9190, EM9191, MC7304, MC7350, MC7354, MC7455. Идеально подходит для IoT, M2M, маршрутизаторов и мобильного широкополосного доступа.",
        "intro": "Sierra Wireless — мировой лидер в области промышленных сотовых модулей, предлагающий полную линейку продуктов от LTE Cat 4 до 5G NR. Yupitek распространяет весь портфель сотовых модулей Sierra Wireless, подходящих для терминалов IoT, промышленных маршрутизаторов, шлюзов, подключенных транспортных средств и устройств мобильной широкополосной связи.",
        "prod_title": "Линейка продуктов",
        "card_desc": "Промышленные сотовые модули для IoT, M2M и мобильного широкополосного доступа.",
    },
    "de": {
        "title": "Sierra Wireless Mobilfunkmodul Serie",
        "desc": "Autorisierter Distributor von Sierra Wireless Industrie-Mobilfunkmodulen: EM7430, EM7455, EM7511, EM7565, EM9190, EM9191, MC7304, MC7350, MC7354, MC7455. Ideal für IoT, M2M, Router und mobile Breitbandanwendungen.",
        "intro": "Sierra Wireless ist ein weltweit führender Anbieter von industriellen Mobilfunkmodulen und bietet eine vollständige Produktpalette von LTE Cat 4 bis 5G NR. Yupitek vertreibt das gesamte Sierra Wireless Mobilfunkmodul-Portfolio, geeignet für IoT-Endgeräte, Industrierouter, Gateways, vernetzte Fahrzeuge und mobile Breitbandgeräte.",
        "prod_title": "Produktlinie",
        "card_desc": "Industrielle Mobilfunkmodule für IoT-, M2M- und mobile Breitbandanwendungen.",
    },
    "fr": {
        "title": "Série de modules cellulaires Sierra Wireless",
        "desc": "Distributeur agréé des modules cellulaires industriels Sierra Wireless : EM7430, EM7455, EM7511, EM7565, EM9190, EM9191, MC7304, MC7350, MC7354, MC7455. Idéal pour l'IoT, le M2M, les routeurs et les applications mobiles à large bande.",
        "intro": "Sierra Wireless est un leader mondial des modules cellulaires industriels, offrant une gamme complète de produits allant de la LTE Cat 4 à la 5G NR. Yupitek distribue l'ensemble du portefeuille de modules cellulaires Sierra Wireless, adaptés aux terminaux IoT, routeurs industriels, passerelles, véhicules connectés et appareils mobiles à large bande.",
        "prod_title": "Gamme de produits",
        "card_desc": "Modules cellulaires industriels pour les applications IoT, M2M et mobiles à large bande.",
    },
}


# ── Comparison table headers per locale ───────────────────────────────────────

COMP_HEADERS = {
    "zh-tw": ["型號", "蜂窩標準", "晶片組", "下載速度", "上傳速度", "載波聚合", "5G 支援", "mmWave"],
    "zh-cn": ["型号", "蜂窝标准", "芯片组", "下载速度", "上传速度", "载波聚合", "5G 支持", "mmWave"],
    "en": ["Model", "Cellular Standard", "Chipset", "Download", "Upload", "CA", "5G", "mmWave"],
    "ja": ["型番", "セルラー規格", "チップセット", "ダウンロード", "アップロード", "CA", "5G", "ミリ波"],
    "ar": ["الموديل", "المعيار", "الرقاقة", "التحميل", "الرفع", "CA", "5G", "mmWave"],
    "es": ["Modelo", "Estándar", "Chipset", "Descarga", "Subida", "CA", "5G", "mmWave"],
    "pt": ["Modelo", "Padrão", "Chipset", "Download", "Upload", "CA", "5G", "mmWave"],
    "ru": ["Модель", "Стандарт", "Чипсет", "Загрузка", "Отдача", "CA", "5G", "mmWave"],
    "de": ["Modell", "Standard", "Chipsatz", "Download", "Upload", "CA", "5G", "mmWave"],
    "fr": ["Modèle", "Norme", "Chipset", "Descendant", "Montant", "CA", "5G", "mmWave"],
}

# ── Comparison table rows (shared values) ────────────────────────────────────

COMP_ROWS = [
    ["EM7430", "LTE-A Cat 6", "Qualcomm MDM9230", "300 Mbps", "50 Mbps", "2×CA", "—", "—"],
    ["EM7455", "LTE-A Cat 6", "Qualcomm MDM9230", "300 Mbps", "50 Mbps", "2×CA", "—", "—"],
    ["EM7511", "LTE-A Pro Cat 12", "Qualcomm SDX20", "600 Mbps", "150 Mbps", "3×CA", "—", "—"],
    ["EM7565", "LTE-A Pro Cat 12", "Qualcomm SDX20", "600 Mbps", "150 Mbps", "3×CA", "—", "—"],
    ["EM9190", "5G NR Sub-6", "Qualcomm SDX55", "2.5 Gbps", "900 Mbps", "8×CA", "✅", "—"],
    ["EM9191", "5G NR Sub-6 + mmWave", "Qualcomm SDX55", "2.5 Gbps", "900 Mbps", "8×CA", "✅", "✅ n260/n261"],
    ["MC7304", "LTE-A Cat 4", "Qualcomm MDM9215", "150 Mbps", "50 Mbps", "—", "—", "—"],
    ["MC7350", "LTE-A Cat 4", "Qualcomm MDM9215", "150 Mbps", "50 Mbps", "—", "—", "—"],
    ["MC7354", "LTE-A Cat 4", "Qualcomm MDM9215", "150 Mbps", "50 Mbps", "—", "—", "—"],
    ["MC7455", "LTE-A Cat 6", "Qualcomm MDM9230", "300 Mbps", "50 Mbps", "2×CA", "—", "—"],
]

# ── Technical product specs (universal) ─────────────────────────────────────

PRODUCT_SPECS = {
    "em7430": [
        ("晶片型號", "Qualcomm MDM9230"),
        ("蜂窩標準", "LTE-Advanced Cat 6"),
        ("下載速度", "300 Mbps (LTE)"),
        ("上傳速度", "50 Mbps (LTE)"),
        ("載波聚合", "2×CA (2×20 MHz)"),
        ("LTE 類別", "Cat 6"),
        ("介面", "USB 3.0 / PCIe Gen2 / I2S / UART"),
        ("外型規格", "M.2 3042 Key B"),
        ("尺寸", "42 × 30 × 2.3 mm"),
        ("重量", "6.5 g"),
        ("工作溫度", "-40°C ~ +85°C"),
        ("GNSS", "GPS / GLONASS / BeiDou"),
        ("地區", "全球 (多頻段)"),
        ("供電電壓", "3.135V ~ 4.4V"),
        ("天線介面", "4 × IPEX MHF4"),
        ("韌體更新", "USB / FOTA"),
    ],
    "em7455": [
        ("晶片型號", "Qualcomm MDM9230"),
        ("蜂窩標準", "LTE-Advanced Cat 6"),
        ("下載速度", "300 Mbps (LTE)"),
        ("上傳速度", "50 Mbps (LTE)"),
        ("載波聚合", "2×CA (2×20 MHz)"),
        ("LTE 類別", "Cat 6"),
        ("介面", "USB 3.0 / PCIe Gen2 / I2S / UART"),
        ("外型規格", "M.2 3042 Key B"),
        ("尺寸", "42 × 30 × 2.3 mm"),
        ("重量", "6.5 g"),
        ("工作溫度", "-40°C ~ +85°C"),
        ("GNSS", "GPS / GLONASS / BeiDou"),
        ("地區", "全球 (含 B14 FirstNet)"),
        ("供電電壓", "3.135V ~ 4.4V"),
        ("天線介面", "4 × IPEX MHF4"),
        ("韌體更新", "USB / FOTA"),
    ],
    "em7511": [
        ("晶片型號", "Qualcomm SDX20"),
        ("蜂窩標準", "LTE-Advanced Pro Cat 12"),
        ("下載速度", "600 Mbps (LTE)"),
        ("上傳速度", "150 Mbps (LTE)"),
        ("載波聚合", "3×CA (3×20 MHz)"),
        ("LTE 類別", "Cat 12"),
        ("介面", "USB 3.1 / PCIe Gen3 / I2S / UART / RGMII"),
        ("外型規格", "M.2 3042 Key B"),
        ("尺寸", "42 × 30 × 2.3 mm"),
        ("重量", "6.8 g"),
        ("工作溫度", "-40°C ~ +85°C"),
        ("GNSS", "GPS / GLONASS / BeiDou / Galileo"),
        ("地區", "全球 (多頻段)"),
        ("供電電壓", "3.135V ~ 4.4V"),
        ("天線介面", "4 × IPEX MHF4"),
        ("韌體更新", "USB / FOTA"),
    ],
    "em7565": [
        ("晶片型號", "Qualcomm SDX20"),
        ("蜂窩標準", "LTE-Advanced Pro Cat 12"),
        ("下載速度", "600 Mbps (LTE)"),
        ("上傳速度", "150 Mbps (LTE)"),
        ("載波聚合", "3×CA (3×20 MHz)"),
        ("LTE 類別", "Cat 12"),
        ("介面", "USB 3.1 / PCIe Gen3 / I2S / UART / RGMII"),
        ("外型規格", "M.2 3042 Key B"),
        ("尺寸", "42 × 30 × 2.3 mm"),
        ("重量", "6.8 g"),
        ("工作溫度", "-40°C ~ +85°C"),
        ("GNSS", "GPS / GLONASS / BeiDou / Galileo"),
        ("地區", "全球 (多頻段)"),
        ("供電電壓", "3.135V ~ 4.4V"),
        ("天線介面", "4 × IPEX MHF4"),
        ("韌體更新", "USB / FOTA"),
    ],
    "em9190": [
        ("晶片型號", "Qualcomm SDX55"),
        ("蜂窩標準", "5G NR Sub-6 + LTE-A Pro Cat 22"),
        ("下載速度", "2.5 Gbps (5G) / 2.0 Gbps (LTE)"),
        ("上傳速度", "900 Mbps (5G) / 150 Mbps (LTE)"),
        ("載波聚合", "8×CA (LTE) + NR CA"),
        ("LTE 類別", "Cat 22"),
        ("5G 支援", "✅ 5G NR Sub-6 (n1/2/3/5/7/8/12/20/25/28/38/41/48/66/71/77/78/79)"),
        ("介面", "USB 3.1 / PCIe Gen3 / I2S / UART / RGMII"),
        ("外型規格", "M.2 3042 Key B"),
        ("尺寸", "42 × 30 × 2.3 mm"),
        ("重量", "7.2 g"),
        ("工作溫度", "-40°C ~ +85°C"),
        ("GNSS", "GPS / GLONASS / BeiDou / Galileo / QZSS"),
        ("地區", "全球 (多頻段)"),
        ("供電電壓", "3.135V ~ 4.4V"),
        ("天線介面", "4 × IPEX MHF4"),
        ("韌體更新", "USB / FOTA"),
    ],
    "em9191": [
        ("晶片型號", "Qualcomm SDX55"),
        ("蜂窩標準", "5G NR Sub-6 + mmWave + LTE-A Pro Cat 22"),
        ("下載速度", "2.5 Gbps (5G) / 2.0 Gbps (LTE)"),
        ("上傳速度", "900 Mbps (5G) / 150 Mbps (LTE)"),
        ("載波聚合", "8×CA (LTE) + NR CA"),
        ("LTE 類別", "Cat 22"),
        ("5G 支援", "✅ 5G NR Sub-6 + mmWave (n260/n261)"),
        ("mmWave 支援", "✅ n260 (39 GHz) / n261 (28 GHz)"),
        ("介面", "USB 3.1 / PCIe Gen3 / I2S / UART / RGMII"),
        ("外型規格", "M.2 3042 Key B"),
        ("尺寸", "42 × 30 × 2.3 mm"),
        ("重量", "7.2 g"),
        ("工作溫度", "-40°C ~ +85°C"),
        ("GNSS", "GPS / GLONASS / BeiDou / Galileo / QZSS"),
        ("地區", "全球 (多頻段)"),
        ("供電電壓", "3.135V ~ 4.4V"),
        ("天線介面", "6 × IPEX MHF4"),
        ("韌體更新", "USB / FOTA"),
    ],
    "mc7304": [
        ("晶片型號", "Qualcomm MDM9215"),
        ("蜂窩標準", "LTE-A Cat 4"),
        ("下載速度", "150 Mbps (LTE)"),
        ("上傳速度", "50 Mbps (LTE)"),
        ("載波聚合", "不支援"),
        ("LTE 類別", "Cat 4"),
        ("介面", "USB 2.0 / UART / SPI"),
        ("外型規格", "Mini PCIe Full Size"),
        ("尺寸", "51 × 30 × 4.7 mm"),
        ("重量", "8.5 g"),
        ("工作溫度", "-40°C ~ +85°C"),
        ("GNSS", "GPS / GLONASS"),
        ("地區", "全球 (多頻段)"),
        ("供電電壓", "3.135V ~ 4.4V"),
        ("天線介面", "2 × IPEX MHF4"),
        ("韌體更新", "USB / FOTA"),
    ],
    "mc7350": [
        ("晶片型號", "Qualcomm MDM9215"),
        ("蜂窩標準", "LTE-A Cat 4"),
        ("下載速度", "150 Mbps (LTE)"),
        ("上傳速度", "50 Mbps (LTE)"),
        ("載波聚合", "不支援"),
        ("LTE 類別", "Cat 4"),
        ("介面", "USB 2.0 / UART / SPI"),
        ("外型規格", "Mini PCIe Full Size"),
        ("尺寸", "51 × 30 × 4.7 mm"),
        ("重量", "8.5 g"),
        ("工作溫度", "-40°C ~ +85°C"),
        ("GNSS", "GPS / GLONASS"),
        ("地區", "全球 (多頻段)"),
        ("供電電壓", "3.135V ~ 4.4V"),
        ("天線介面", "2 × IPEX MHF4"),
        ("韌體更新", "USB / FOTA"),
    ],
    "mc7354": [
        ("晶片型號", "Qualcomm MDM9215"),
        ("蜂窩標準", "LTE-A Cat 4"),
        ("下載速度", "150 Mbps (LTE)"),
        ("上傳速度", "50 Mbps (LTE)"),
        ("載波聚合", "不支援"),
        ("LTE 類別", "Cat 4"),
        ("介面", "USB 2.0 / UART / SPI"),
        ("外型規格", "Mini PCIe Full Size"),
        ("尺寸", "51 × 30 × 4.7 mm"),
        ("重量", "8.5 g"),
        ("工作溫度", "-40°C ~ +85°C"),
        ("GNSS", "GPS / GLONASS"),
        ("地區", "全球 (多頻段)"),
        ("供電電壓", "3.135V ~ 4.4V"),
        ("天線介面", "2 × IPEX MHF4"),
        ("韌體更新", "USB / FOTA"),
    ],
    "mc7455": [
        ("晶片型號", "Qualcomm MDM9230"),
        ("蜂窩標準", "LTE-Advanced Cat 6"),
        ("下載速度", "300 Mbps (LTE)"),
        ("上傳速度", "50 Mbps (LTE)"),
        ("載波聚合", "2×CA (2×20 MHz)"),
        ("LTE 類別", "Cat 6"),
        ("介面", "USB 3.0 / UART / SPI"),
        ("外型規格", "Mini PCIe Full Size"),
        ("尺寸", "51 × 30 × 4.7 mm"),
        ("重量", "8.8 g"),
        ("工作溫度", "-40°C ~ +85°C"),
        ("GNSS", "GPS / GLONASS / BeiDou"),
        ("地區", "全球 (多頻段)"),
        ("供電電壓", "3.135V ~ 4.4V"),
        ("天線介面", "4 × IPEX MHF4"),
        ("韌體更新", "USB / FOTA"),
    ],
}


# ── OS support data ─────────────────────────────────────────────────────────

OS_ROWS = {
    "em7430": [
        ("Windows 10/11", "✅", "經 Sierra Wireless 驅動程式認證"),
        ("Linux (Kernel ≥ 4.4)", "✅", "核心內建 QMI_WWAN / option 驅動"),
        ("Android", "✅", "可透過 USB OTG 連接"),
        ("OpenWrt", "✅", "需安裝 kmod-usb-net-qmi-wwan"),
    ],
    "em7455": [
        ("Windows 10/11", "✅", "經 Sierra Wireless 驅動程式認證"),
        ("Linux (Kernel ≥ 4.4)", "✅", "核心內建 QMI_WWAN / option 驅動"),
        ("Android", "✅", "可透過 USB OTG 連接"),
        ("OpenWrt", "✅", "需安裝 kmod-usb-net-qmi-wwan"),
    ],
    "em7511": [
        ("Windows 10/11", "✅", "經 Sierra Wireless 驅動程式認證"),
        ("Linux (Kernel ≥ 4.8)", "✅", "核心內建 QMI_WWAN / MBIM 驅動"),
        ("Android", "✅", "可透過 USB OTG 連接"),
        ("OpenWrt", "✅", "需安裝 kmod-usb-net-qmi-wwan"),
        ("Yocto / Buildroot", "✅", "支援 SDK 整合"),
    ],
    "em7565": [
        ("Windows 10/11", "✅", "經 Sierra Wireless 驅動程式認證"),
        ("Linux (Kernel ≥ 4.8)", "✅", "核心內建 QMI_WWAN / MBIM 驅動"),
        ("Android", "✅", "可透過 USB OTG 連接"),
        ("OpenWrt", "✅", "需安裝 kmod-usb-net-qmi-wwan"),
        ("Yocto / Buildroot", "✅", "支援 SDK 整合"),
    ],
    "em9190": [
        ("Windows 10/11", "✅", "經 Sierra Wireless 驅動程式認證"),
        ("Linux (Kernel ≥ 5.10)", "✅", "核心內建 MHIM / QMI_WWAN 驅動"),
        ("Android", "✅", "可透過 USB OTG 連接"),
        ("OpenWrt", "✅", "需安裝 kmod-usb-net-qmi-wwan"),
        ("Yocto / Buildroot", "✅", "支援 SDK 整合"),
    ],
    "em9191": [
        ("Windows 10/11", "✅", "經 Sierra Wireless 驅動程式認證"),
        ("Linux (Kernel ≥ 5.10)", "✅", "核心內建 MHIM / QMI_WWAN 驅動"),
        ("Android", "✅", "可透過 USB OTG 連接"),
        ("OpenWrt", "✅", "需安裝 kmod-usb-net-qmi-wwan"),
        ("Yocto / Buildroot", "✅", "支援 SDK 整合"),
    ],
    "mc7304": [
        ("Windows 10/11", "✅", "經 Sierra Wireless 驅動程式認證"),
        ("Linux (Kernel ≥ 3.10)", "✅", "核心內建 option 驅動"),
        ("Android", "✅", "可透過 USB OTG 連接"),
        ("OpenWrt", "✅", "需安裝 kmod-usb-serial-option"),
    ],
    "mc7350": [
        ("Windows 10/11", "✅", "經 Sierra Wireless 驅動程式認證"),
        ("Linux (Kernel ≥ 3.10)", "✅", "核心內建 option 驅動"),
        ("Android", "✅", "可透過 USB OTG 連接"),
        ("OpenWrt", "✅", "需安裝 kmod-usb-serial-option"),
    ],
    "mc7354": [
        ("Windows 10/11", "✅", "經 Sierra Wireless 驅動程式認證"),
        ("Linux (Kernel ≥ 3.10)", "✅", "核心內建 option 驅動"),
        ("Android", "✅", "可透過 USB OTG 連接"),
        ("OpenWrt", "✅", "需安裝 kmod-usb-serial-option"),
    ],
    "mc7455": [
        ("Windows 10/11", "✅", "經 Sierra Wireless 驅動程式認證"),
        ("Linux (Kernel ≥ 4.4)", "✅", "核心內建 QMI_WWAN / option 驅動"),
        ("Android", "✅", "可透過 USB OTG 連接"),
        ("OpenWrt", "✅", "需安裝 kmod-usb-net-qmi-wwan"),
    ],
}

# ── Package contents (universal data, zh-tw base) ───────────────────────────

PACKAGE = {
    "em7430": ["1 × EM7430 蜂窩模組", "1 × 文件包裝"],
    "em7455": ["1 × EM7455 蜂窩模組", "1 × 文件包裝"],
    "em7511": ["1 × EM7511 蜂窩模組", "1 × 文件包裝"],
    "em7565": ["1 × EM7565 蜂窩模組", "1 × 文件包裝"],
    "em9190": ["1 × EM9190 蜂窩模組", "1 × 文件包裝"],
    "em9191": ["1 × EM9191 蜂窩模組", "1 × 文件包裝"],
    "mc7304": ["1 × MC7304 蜂窩模組", "1 × 文件包裝"],
    "mc7350": ["1 × MC7350 蜂窩模組", "1 × 文件包裝"],
    "mc7354": ["1 × MC7354 蜂窩模組", "1 × 文件包裝"],
    "mc7455": ["1 × MC7455 蜂窩模組", "2 × 文件包裝"],
}

# ── Resources (universal data, zh-tw base) ──────────────────────────────────

# Current URLs: Sierra Wireless (Semtech) products are listed at source.sierrawireless.com
# The old www.sierrawireless.com/products/* URLs are all 404.
# Spec sheets are direct PDF links from Sierra's download center.
RESOURCES = {
    "em7430": [
        ("官方產品頁面", "https://source.sierrawireless.com/devices/em-series/em7430/"),
        ("技術規格書 (PDF)", "https://source.sierrawireless.com/-/media/support_downloads/airprime/74xx/4116235-airprime-em7430-product-technical-specification-r12.ashx"),
    ],
    "em7455": [
        ("官方產品頁面", "https://source.sierrawireless.com/devices/em-series/em7455/"),
        ("技術規格書 (PDF)", "https://source.sierrawireless.com/-/media/support_downloads/airprime/74xx/4116236-airprime-em7455-product-technical-specification-r15.ashx"),
    ],
    "em7511": [
        ("官方產品頁面", "https://source.sierrawireless.com/devices/em-series/em7511/"),
        ("技術規格書 (PDF)", "https://source.sierrawireless.com/-/media/support_downloads/airprime/hardware_specs_user_guides/41112028-em7511-product-technical-specification-r14.ashx"),
    ],
    "em7565": [
        ("官方產品頁面", "https://source.sierrawireless.com/devices/em-series/em7565/"),
        ("技術規格書 (PDF)", "https://source.sierrawireless.com/-/media/support_downloads/airprime/hardware_specs_user_guides/41110788-em7565-product-technical-specification-r16.ashx"),
    ],
    "em9190": [
        ("官方產品頁面", "https://source.sierrawireless.com/devices/em-series/em9190/"),
        ("技術規格書 (PDF)", "https://source.sierrawireless.com/-/media/support_downloads/airprime/hardware_specs_user_guides/41113174-em919x-em7690-product-technical-specification-r11.ashx"),
    ],
    "em9191": [
        ("官方產品頁面", "https://source.sierrawireless.com/devices/em-series/em9191/"),
        ("技術規格書 (PDF)", "https://source.sierrawireless.com/-/media/support_downloads/airprime/hardware_specs_user_guides/41113174-em919x-em7690-product-technical-specification-r11.ashx"),
    ],
    "mc7304": [
        ("官方產品頁面", "https://source.sierrawireless.com/devices/mc-series/mc7304/"),
        ("技術規格書 (PDF)", "https://source.sierrawireless.com/-/media/support_downloads/airprime/hardware_specs_user_guides/airprime_mc7304_product_technical_specification_and_customer_design_guidelines_rev12_0.ashx"),
    ],
    "mc7350": [
        ("官方產品頁面", "https://source.sierrawireless.com/devices/mc-series/mc7350/"),
        ("技術規格書 (PDF)", "https://source.sierrawireless.com/-/media/support_downloads/airprime/hardware_specs_user_guides/airprime_mc7350_product_technical_specification_and_customer_design_guidelines_rev4_0.ashx"),
    ],
    "mc7354": [
        ("官方產品頁面", "https://source.sierrawireless.com/devices/mc-series/mc7354/"),
        ("技術規格書 (PDF)", "https://source.sierrawireless.com/-/media/support_downloads/airprime/hardware_specs_user_guides/4114635_airprime-mc7354-product-technical-specification_r9.ashx"),
    ],
    "mc7455": [
        ("官方產品頁面", "https://source.sierrawireless.com/devices/mc-series/mc7455/"),
        ("技術規格書 (PDF)", "https://source.sierrawireless.com/-/media/support_downloads/airprime/74xx/4116238-mc7455-pts-r15.ashx"),
    ],
}


# ── zh-tw product content (features, overviews, titles) ──────────────────────

PRODUCT_ZH = {
    "em7430": {
        "title": "EM7430 LTE-A Cat 6 蜂窩模組",
        "desc": "EM7430 採用 Qualcomm MDM9230 晶片組，支援 LTE-A Cat 6 高達 300 Mbps 下載速度，M.2 封裝，適用於工業路由器與閘道器。",
        "overview": (
            "EM7430 是 Sierra Wireless 推出的 LTE-Advanced Cat 6 蜂窩模組，採用 Qualcomm MDM9230 晶片組，"
            "支援 2×20 MHz 載波聚合 (2×CA)，下載速度最高可達 300 Mbps，上傳最高 50 Mbps。\n\n"
            "此模組採用標準 M.2 3042 Key B 封裝，適用於工業路由器、物聯網閘道器、行動熱點及視訊監控等應用。"
            "支援 USB 3.0 及 PCIe Gen2 介面，提供靈活的系統整合方案。\n\n"
            "EM7430 支援全球主要 LTE 頻段 (B1–5/7/8/12/13/20/25/26/29/30/41)，"
            "適合於世界各地部署的 IoT 設備與 M2M 終端。"
        ),
        "features": [
            "採用 Qualcomm MDM9230 晶片組，成熟穩定",
            "LTE-A Cat 6，支援 2×CA 載波聚合",
            "下載速度高達 300 Mbps，上傳 50 Mbps",
            "M.2 3042 Key B 工業級封裝",
            "支援 USB 3.0 與 PCIe Gen2 雙介面",
            "內建 GPS / GLONASS / BeiDoU GNSS",
            "寬溫設計 -40°C ~ +85°C",
            "支援 FOTA 韌體無線更新",
        ],
        "tags": ["LTE", "Cat 6", "Cellular", "Module", "EM7430", "IoT", "M.2"],
    },
    "em7455": {
        "title": "EM7455 LTE-A Cat 6 蜂窩模組",
        "desc": "EM7455 採用 Qualcomm MDM9230 晶片組，支援 LTE-A Cat 6 與 FirstNet B14 頻段，M.2 封裝，適用於工業路由器與閘道器。",
        "overview": (
            "EM7455 是 Sierra Wireless 推出的 LTE-Advanced Cat 6 蜂窩模組，採用 Qualcomm MDM9230 晶片組，"
            "支援 2×20 MHz 載波聚合 (2×CA)，下載速度最高可達 300 Mbps，上傳最高 50 Mbps。\n\n"
            "此模組採用標準 M.2 3042 Key B 封裝，與 EM7430 同系列但特別支援 Band 14 (FirstNet)，"
            "適合美國公共安全網路應用。支援 USB 3.0 及 PCIe Gen2 介面。\n\n"
            "EM7455 支援全球主要 LTE 頻段 (B1–5/7/8/12/13/14/20/25/26/29/30/41)，"
            "廣泛應用於企業路由、車聯網與公共安全通訊。"
        ),
        "features": [
            "採用 Qualcomm MDM9230 晶片組",
            "LTE-A Cat 6，支援 2×CA 載波聚合",
            "下載速度高達 300 Mbps，上傳 50 Mbps",
            "支援 Band 14 FirstNet 公共安全頻段",
            "M.2 3042 Key B 工業級封裝",
            "支援 USB 3.0 與 PCIe Gen2 雙介面",
            "內建 GPS / GLONASS / BeiDou GNSS",
            "寬溫設計 -40°C ~ +85°C",
        ],
        "tags": ["LTE", "Cat 6", "Cellular", "Module", "EM7455", "FirstNet", "M.2"],
    },
    "em7511": {
        "title": "EM7511 LTE-A Pro Cat 12 蜂窩模組",
        "desc": "EM7511 採用 Qualcomm SDX20 晶片組，支援 LTE-A Pro Cat 12 高達 600 Mbps，M.2 封裝，適用於高效能工業應用。",
        "overview": (
            "EM7511 是 Sierra Wireless 推出的 LTE-Advanced Pro Cat 12 蜂窩模組，採用 Qualcomm SDX20 晶片組，"
            "支援 3×20 MHz 載波聚合 (3×CA)，下載速度最高可達 600 Mbps，上傳最高 150 Mbps。\n\n"
            "此模組採用標準 M.2 3042 Key B 封裝，整合 USB 3.1、PCIe Gen3 及 RGMII 介面，"
            "提供更高的系統頻寬。SDX20 數據機相較前代產品提供了更低的功耗與更優的 RF 性能。\n\n"
            "EM7511 支援全球 LTE 頻段與 License-Assisted Access (LAA)，"
            "適合需要高頻寬的影片監控、企業分支機構及行動熱點應用。"
        ),
        "features": [
            "採用 Qualcomm SDX20 數據機晶片",
            "LTE-A Pro Cat 12，支援 3×CA 載波聚合",
            "下載速度高達 600 Mbps，上傳 150 Mbps",
            "支援 256QAM DL / 64QAM UL",
            "M.2 3042 Key B 工業級封裝",
            "支援 USB 3.1、PCIe Gen3、RGMII",
            "內建 GPS / GLONASS / BeiDou / Galileo",
            "寬溫設計 -40°C ~ +85°C",
        ],
        "tags": ["LTE", "Cat 12", "Cellular", "Module", "EM7511", "SDX20", "M.2"],
    },
    "em7565": {
        "title": "EM7565 LTE-A Pro Cat 12 蜂窩模組",
        "desc": "EM7565 採用 Qualcomm SDX20 晶片組，支援 LTE-A Pro Cat 12 600 Mbps 與雙頻 GNSS，M.2 封裝，適用於高效能工業路由器。",
        "overview": (
            "EM7565 是 Sierra Wireless 推出的 LTE-Advanced Pro Cat 12 蜂窩模組，採用 Qualcomm SDX20 晶片組，"
            "支援 3×20 MHz 載波聚合 (3×CA)，DL 256QAM 與 UL 64QAM，下載速度最高 600 Mbps，上傳最高 150 Mbps。\n\n"
            "EM7565 採用標準 M.2 3042 Key B 封裝，相較 EM7511 增加了對更多載波聚合組合的支援。"
            "其 SDX20 平台提供強大的 RF 性能與極低的功耗，適合全天候運作的工業設備。\n\n"
            "支援全球主要 LTE 頻段，包括 B14 FirstNet 及 B71 600 MHz 頻段，"
            "適用於工業路由器、關鍵任務通訊與專業行動熱點。"
        ),
        "features": [
            "採用 Qualcomm SDX20 數據機晶片",
            "LTE-A Pro Cat 12，支援 3×CA",
            "下載速度高達 600 Mbps，上傳 150 Mbps",
            "支援 256QAM DL / 64QAM UL / LAA",
            "M.2 3042 Key B 工業級封裝",
            "支援 USB 3.1、PCIe Gen3、RGMII",
            "支援 FirstNet B14 與 B71 頻段",
            "雙頻 GNSS (GPS + Galileo)",
        ],
        "tags": ["LTE", "Cat 12", "Cellular", "Module", "EM7565", "SDX20", "M.2"],
    },
    "em9190": {
        "title": "EM9190 5G NR Sub-6 蜂窩模組",
        "desc": "EM9190 採用 Qualcomm SDX55 晶片組，支援 5G NR Sub-6 高達 2.5 Gbps 與 LTE Cat 22，M.2 封裝，適用於次世代工業應用。",
        "overview": (
            "EM9190 是 Sierra Wireless 推出的旗艦級 5G NR Sub-6 蜂窩模組，採用 Qualcomm SDX55 晶片組，"
            "支援 5G SA/NSA 模式，下載速度最高可達 2.5 Gbps (5G) / 2.0 Gbps (LTE Cat 22)，"
            "上傳最高 900 Mbps (5G)。\n\n"
            "此模組支援類別 22 LTE (8×CA) 與廣泛的 5G NR Sub-6 頻段，"
            "涵蓋 n1/2/3/5/7/8/12/20/25/28/38/41/48/66/71/77/78/79。"
            "採用標準 M.2 3042 Key B 封裝，提供完整的 5G 連線能力。\n\n"
            "EM9190 搭載先進的功率管理與散熱設計，適用於高效能工業路由器、CPE、"
            "企業級閘道器與 5G 行動熱點。"
        ),
        "features": [
            "採用 Qualcomm SDX55 5G 數據機晶片",
            "支援 5G NR Sub-6 SA/NSA 雙模",
            "5G 下載高達 2.5 Gbps，上傳 900 Mbps",
            "LTE Cat 22 下載高達 2.0 Gbps",
            "支援 8×CA 載波聚合",
            "M.2 3042 Key B 工業級封裝",
            "支援 USB 3.1、PCIe Gen3、RGMII",
            "多頻 GNSS (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
        "tags": ["5G", "Sub-6", "Cellular", "Module", "EM9190", "SDX55", "M.2", "IoT"],
    },
    "em9191": {
        "title": "EM9191 5G NR Sub-6 + mmWave 蜂窩模組",
        "desc": "EM9191 採用 Qualcomm SDX55 晶片組，支援 5G NR Sub-6 與 mmWave (n260/n261)，M.2 封裝，適用於最高階 5G 應用。",
        "overview": (
            "EM9191 是 Sierra Wireless 推出的旗艦級 5G NR 蜂窩模組，採用 Qualcomm SDX55 晶片組，"
            "同時支援 Sub-6 與 mmWave (n260 39GHz / n261 28GHz)，提供最全面的 5G 覆蓋。\n\n"
            "下載速度最高可達 2.5 Gbps (5G) / 2.0 Gbps (LTE Cat 22)，"
            "上傳最高 900 Mbps (5G)。支援 6 組天線介面以滿足 mmWave 波束成型需求。\n\n"
            "EM9191 支援所有 Sub-6 頻段 (同 EM9190) 加上 mmWave 高頻頻段，"
            "搭配多頻 GNSS 系統，適合需要最低延遲與最高頻寬的工業 4.0、"
            "智慧醫療與邊緣運算應用。"
        ),
        "features": [
            "採用 Qualcomm SDX55 5G 數據機晶片",
            "支援 5G NR Sub-6 + mmWave (n260/n261)",
            "5G 下載高達 2.5 Gbps，上傳 900 Mbps",
            "LTE Cat 22 下載高達 2.0 Gbps",
            "支援 8×CA 與 mmWave 波束成型",
            "6 組天線介面 (含 mmWave 天線)",
            "M.2 3042 Key B 工業級封裝",
            "多頻 GNSS (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
        "tags": ["5G", "mmWave", "Sub-6", "Cellular", "Module", "EM9191", "SDX55", "M.2"],
    },
    "mc7304": {
        "title": "MC7304 LTE-A Cat 4 蜂窩模組",
        "desc": "MC7304 採用 Qualcomm MDM9215 晶片組，支援 LTE-A Cat 4 150 Mbps，Mini PCIe 封裝，適用於傳統工業閘道器與路由器。",
        "overview": (
            "MC7304 是 Sierra Wireless 推出的 LTE-Advanced Cat 4 蜂窩模組，採用 Qualcomm MDM9215 晶片組，"
            "支援下載速度最高 150 Mbps，上傳最高 50 Mbps。\n\n"
            "此模組採用標準 Mini PCIe Full Size 封裝，相容於大量現有工業主機板與嵌入式平台。"
            "支援 USB 2.0、UART 及 SPI 介面，適合預算敏感但仍需可靠 LTE 連線的應用。\n\n"
            "MC7304 支援全球主要 LTE 頻段，廣泛應用於工業閘道器、自動販賣機、數位看板與遠端監控。"
        ),
        "features": [
            "採用 Qualcomm MDM9215 晶片組",
            "LTE-A Cat 4，下載高達 150 Mbps",
            "上傳速度最高 50 Mbps",
            "Mini PCIe Full Size 標準封裝",
            "支援 USB 2.0、UART、SPI 介面",
            "內建 GPS / GLONASS GNSS",
            "寬溫設計 -40°C ~ +85°C",
            "成熟穩定，廣泛的軟體支援",
        ],
        "tags": ["LTE", "Cat 4", "Cellular", "Module", "MC7304", "Mini PCIe", "IoT"],
    },
    "mc7350": {
        "title": "MC7350 LTE-A Cat 4 蜂窩模組",
        "desc": "MC7350 採用 Qualcomm MDM9215 晶片組，支援 LTE-A Cat 4 150 Mbps，Mini PCIe 封裝，適用於全球佈署的 IoT 應用。",
        "overview": (
            "MC7350 是 Sierra Wireless 推出的 LTE-Advanced Cat 4 蜂窩模組，採用 Qualcomm MDM9215 晶片組，"
            "支援下載速度最高 150 Mbps，上傳最高 50 Mbps。\n\n"
            "此模組採用標準 Mini PCIe Full Size 封裝。MC7350 與 MC7304 同系列，"
            "預設支援更廣泛的全球頻段組合。支援 USB 2.0、UART 及 SPI 介面。\n\n"
            "MC7350 經過全球各主要電信業者的認證，適用於工業路由器、資產追蹤、"
            "智慧電表與遠端醫療設備。"
        ),
        "features": [
            "採用 Qualcomm MDM9215 晶片組",
            "LTE-A Cat 4，下載高達 150 Mbps",
            "上傳速度最高 50 Mbps",
            "Mini PCIe Full Size 標準封裝",
            "支援 USB 2.0、UART、SPI 介面",
            "全球電信業者廣泛認證",
            "內建 GPS / GLONASS GNSS",
            "寬溫設計 -40°C ~ +85°C",
        ],
        "tags": ["LTE", "Cat 4", "Cellular", "Module", "MC7350", "Mini PCIe", "IoT"],
    },
    "mc7354": {
        "title": "MC7354 LTE-A Cat 4 蜂窩模組",
        "desc": "MC7354 採用 Qualcomm MDM9215 晶片組，支援 LTE-A Cat 4 150 Mbps，Mini PCIe 封裝，適用於工業 IoT 與 M2M 通訊。",
        "overview": (
            "MC7354 是 Sierra Wireless 推出的 LTE-Advanced Cat 4 蜂窩模組，採用 Qualcomm MDM9215 晶片組，"
            "支援下載速度最高 150 Mbps，上傳最高 50 Mbps。\n\n"
            "此模組採用標準 Mini PCIe Full Size 封裝。MC7354 主要差異在於其支援的特定頻段組合，"
            "適用於特定區域的運營商網路。支援 USB 2.0、UART 及 SPI 介面。\n\n"
            "MC7354 適用於工業自動化、交通運輸、智慧電網及基礎設施監控等需要穩定 LTE 連線的產業應用。"
        ),
        "features": [
            "採用 Qualcomm MDM9215 晶片組",
            "LTE-A Cat 4，下載高達 150 Mbps",
            "上傳速度最高 50 Mbps",
            "Mini PCIe Full Size 標準封裝",
            "支援 USB 2.0、UART、SPI 介面",
            "特定區域運營商頻段優化",
            "內建 GPS / GLONASS GNSS",
            "寬溫設計 -40°C ~ +85°C",
        ],
        "tags": ["LTE", "Cat 4", "Cellular", "Module", "MC7354", "Mini PCIe", "IoT"],
    },
    "mc7455": {
        "title": "MC7455 LTE-A Cat 6 蜂窩模組",
        "desc": "MC7455 採用 Qualcomm MDM9230 晶片組，支援 LTE-A Cat 6 300 Mbps，Mini PCIe 封裝，適用於高效能工業應用。",
        "overview": (
            "MC7455 是 Sierra Wireless 推出的 LTE-Advanced Cat 6 蜂窩模組，採用 Qualcomm MDM9230 晶片組，"
            "支援 2×20 MHz 載波聚合 (2×CA)，下載速度最高可達 300 Mbps，上傳最高 50 Mbps。\n\n"
            "此模組採用標準 Mini PCIe Full Size 封裝，是 MC 系列中最高階的型號。"
            "支援 USB 3.0、UART 及 SPI 介面，提供快速的資料傳輸能力。\n\n"
            "MC7455 支援全球主要 LTE 頻段與 FirstNet B14，廣泛應用於高效能工業路由器、"
            "車載通訊系統、專網基地台及企業級連網解決方案。"
        ),
        "features": [
            "採用 Qualcomm MDM9230 晶片組",
            "LTE-A Cat 6，支援 2×CA 載波聚合",
            "下載速度高達 300 Mbps，上傳 50 Mbps",
            "Mini PCIe Full Size 標準封裝",
            "支援 USB 3.0、UART、SPI 介面",
            "支援 FirstNet B14 頻段",
            "內建 GPS / GLONASS / BeiDou GNSS",
            "寬溫設計 -40°C ~ +85°C",
        ],
        "tags": ["LTE", "Cat 6", "Cellular", "Module", "MC7455", "Mini PCIe", "IoT"],
    },
}


# ── English product content (overviews, features) ───────────────────────────
# Used as fallback for all non-zh-tw locales; better than showing zh-tw text.

PRODUCT_EN = {
    "em7430": {
        "desc": "EM7430 LTE-A Cat 6 cellular module with Qualcomm MDM9230, 300 Mbps download, M.2 form factor, ideal for industrial IoT and M2M applications.",
        "overview": (
            "The EM7430 is Sierra Wireless' LTE-Advanced Cat 6 cellular module, powered by the Qualcomm MDM9230 chipset, "
            "supporting 2×20 MHz carrier aggregation (2×CA) with download speeds up to 300 Mbps and upload up to 50 Mbps.\n\n"
            "This module uses a standard M.2 3042 Key B form factor, ideal for industrial routers, IoT gateways, mobile hotspots, "
            "and video surveillance applications. It supports USB 3.0 and PCIe Gen2 interfaces for flexible system integration.\n\n"
            "The EM7430 supports major global LTE bands (B1–5/7/8/12/13/20/25/26/29/30/41), "
            "making it suitable for IoT devices and M2M terminals deployed worldwide."
        ),
        "features": [
            "Qualcomm MDM9230 chipset for proven reliability",
            "LTE-A Cat 6 with 2×CA carrier aggregation",
            "Download up to 300 Mbps, upload up to 50 Mbps",
            "M.2 3042 Key B industrial-grade form factor",
            "USB 3.0 and PCIe Gen2 dual interface support",
            "Integrated GPS / GLONASS / BeiDou GNSS",
            "Wide temperature range -40°C ~ +85°C",
            "FOTA firmware over-the-air update support",
        ],
    },
    "em7455": {
        "desc": "EM7455 LTE-A Cat 6 cellular module with Qualcomm MDM9230, 300 Mbps download, Band 14 FirstNet support, M.2 form factor for public safety and enterprise routing.",
        "overview": (
            "The EM7455 is Sierra Wireless' LTE-Advanced Cat 6 cellular module, powered by the Qualcomm MDM9230 chipset, "
            "supporting 2×20 MHz carrier aggregation (2×CA) with download speeds up to 300 Mbps and upload up to 50 Mbps.\n\n"
            "This module uses a standard M.2 3042 Key B form factor. It is part of the same family as the EM7430 but specifically supports "
            "Band 14 (FirstNet), making it ideal for US public safety network applications. It supports USB 3.0 and PCIe Gen2 interfaces.\n\n"
            "The EM7455 supports major global LTE bands (B1–5/7/8/12/13/14/20/25/26/29/30/41), "
            "widely used in enterprise routing, connected vehicles, and public safety communications."
        ),
        "features": [
            "Qualcomm MDM9230 chipset",
            "LTE-A Cat 6 with 2×CA carrier aggregation",
            "Download up to 300 Mbps, upload up to 50 Mbps",
            "Band 14 FirstNet public safety band support",
            "M.2 3042 Key B industrial-grade form factor",
            "USB 3.0 and PCIe Gen2 dual interface support",
            "Integrated GPS / GLONASS / BeiDou GNSS",
            "Wide temperature range -40°C ~ +85°C",
        ],
    },
    "em7511": {
        "desc": "EM7511 LTE-A Pro Cat 12 cellular module with Qualcomm SDX20, 600 Mbps download, M.2 form factor for high-bandwidth enterprise and industrial applications.",
        "overview": (
            "The EM7511 is Sierra Wireless' LTE-Advanced Pro Cat 12 cellular module, powered by the Qualcomm SDX20 chipset, "
            "supporting 3×20 MHz carrier aggregation (3×CA) with download speeds up to 600 Mbps and upload up to 150 Mbps.\n\n"
            "This module uses a standard M.2 3042 Key B form factor with USB 3.1, PCIe Gen3, and RGMII interfaces, "
            "providing higher system bandwidth. The SDX20 modem delivers lower power consumption and superior RF performance compared to previous generations.\n\n"
            "The EM7511 supports global LTE bands and License-Assisted Access (LAA), "
            "ideal for high-bandwidth video surveillance, enterprise branch offices, and mobile hotspot applications."
        ),
        "features": [
            "Qualcomm SDX20 modem chipset",
            "LTE-A Pro Cat 12 with 3×CA carrier aggregation",
            "Download up to 600 Mbps, upload up to 150 Mbps",
            "256QAM DL / 64QAM UL support",
            "M.2 3042 Key B industrial-grade form factor",
            "USB 3.1, PCIe Gen3, RGMII interface support",
            "Integrated GPS / GLONASS / BeiDou / Galileo",
            "Wide temperature range -40°C ~ +85°C",
        ],
    },
    "em7565": {
        "desc": "EM7565 LTE-A Pro Cat 12 cellular module with Qualcomm SDX20, 600 Mbps download, FirstNet B14 support, M.2 form factor for mission-critical communications.",
        "overview": (
            "The EM7565 is Sierra Wireless' LTE-Advanced Pro Cat 12 cellular module, powered by the Qualcomm SDX20 chipset, "
            "supporting 3×20 MHz carrier aggregation (3×CA), DL 256QAM and UL 64QAM, with download speeds up to 600 Mbps and upload up to 150 Mbps.\n\n"
            "The EM7565 uses a standard M.2 3042 Key B form factor and offers broader carrier aggregation support compared to the EM7511. "
            "Its SDX20 platform delivers excellent RF performance with extremely low power consumption, ideal for 24/7 industrial operation.\n\n"
            "It supports major global LTE bands including B14 FirstNet and B71 600 MHz, "
            "suitable for industrial routers, mission-critical communications, and professional mobile hotspots."
        ),
        "features": [
            "Qualcomm SDX20 modem chipset",
            "LTE-A Pro Cat 12 with 3×CA carrier aggregation",
            "Download up to 600 Mbps, upload up to 150 Mbps",
            "256QAM DL / 64QAM UL / LAA support",
            "M.2 3042 Key B industrial-grade form factor",
            "USB 3.1, PCIe Gen3, RGMII interface support",
            "FirstNet B14 and B71 band support",
            "Dual-band GNSS (GPS + Galileo)",
        ],
    },
    "em9190": {
        "desc": "EM9190 5G NR Sub-6 cellular module with Qualcomm SDX55, 2.5 Gbps download, M.2 form factor for next-generation industrial and 5G applications.",
        "overview": (
            "The EM9190 is Sierra Wireless' flagship 5G NR Sub-6 cellular module, powered by the Qualcomm SDX55 chipset, "
            "supporting 5G SA/NSA modes with download speeds up to 2.5 Gbps (5G) / 2.0 Gbps (LTE Cat 22) "
            "and upload up to 900 Mbps (5G).\n\n"
            "This module supports Category 22 LTE (8×CA) with extensive 5G NR Sub-6 band coverage including "
            "n1/2/3/5/7/8/12/20/25/28/38/41/48/66/71/77/78/79. "
            "It uses a standard M.2 3042 Key B form factor for complete 5G connectivity.\n\n"
            "The EM9190 features advanced power management and thermal design, "
            "suitable for high-performance industrial routers, CPE, enterprise gateways, and 5G mobile hotspots."
        ),
        "features": [
            "Qualcomm SDX55 5G modem chipset",
            "5G NR Sub-6 SA/NSA dual mode support",
            "5G download up to 2.5 Gbps, upload 900 Mbps",
            "LTE Cat 22 download up to 2.0 Gbps",
            "8×CA carrier aggregation support",
            "M.2 3042 Key B industrial-grade form factor",
            "USB 3.1, PCIe Gen3, RGMII support",
            "Multi-band GNSS (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "em9191": {
        "desc": "EM9191 5G NR Sub-6 + mmWave cellular module with Qualcomm SDX55, 2.5 Gbps download, supporting n260/n261 for comprehensive 5G coverage.",
        "overview": (
            "The EM9191 is Sierra Wireless' flagship 5G NR cellular module, powered by the Qualcomm SDX55 chipset, "
            "supporting both Sub-6 and mmWave (n260 39GHz / n261 28GHz) for the most comprehensive 5G coverage.\n\n"
            "Download speeds reach up to 2.5 Gbps (5G) / 2.0 Gbps (LTE Cat 22) "
            "with upload up to 900 Mbps (5G). It supports 6 antenna interfaces for mmWave beamforming requirements.\n\n"
            "The EM9191 supports all Sub-6 bands (same as EM9190) plus mmWave high-frequency bands, "
            "paired with multi-band GNSS. Ideal for Industry 4.0, smart healthcare, "
            "and edge computing applications requiring the lowest latency and highest bandwidth."
        ),
        "features": [
            "Qualcomm SDX55 5G modem chipset",
            "5G NR Sub-6 + mmWave (n260/n261) support",
            "5G download up to 2.5 Gbps, upload 900 Mbps",
            "LTE Cat 22 download up to 2.0 Gbps",
            "8×CA and mmWave beamforming support",
            "6 antenna interfaces (including mmWave antennas)",
            "M.2 3042 Key B industrial-grade form factor",
            "Multi-band GNSS (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "mc7304": {
        "desc": "MC7304 LTE-A Cat 4 cellular module with Qualcomm MDM9215, 150 Mbps download, Mini PCIe form factor for budget-sensitive industrial applications.",
        "overview": (
            "The MC7304 is Sierra Wireless' LTE-Advanced Cat 4 cellular module, powered by the Qualcomm MDM9215 chipset, "
            "supporting download speeds up to 150 Mbps and upload up to 50 Mbps.\n\n"
            "This module uses a standard Mini PCIe Full Size form factor, compatible with a wide range of existing "
            "industrial motherboards and embedded platforms. It supports USB 2.0, UART, and SPI interfaces, "
            "ideal for budget-sensitive applications requiring reliable LTE connectivity.\n\n"
            "The MC7304 supports major global LTE bands, widely deployed in industrial gateways, "
            "vending machines, digital signage, and remote monitoring applications."
        ),
        "features": [
            "Qualcomm MDM9215 chipset",
            "LTE-A Cat 4 with download up to 150 Mbps",
            "Upload speed up to 50 Mbps",
            "Mini PCIe Full Size standard form factor",
            "USB 2.0, UART, SPI interface support",
            "Integrated GPS / GLONASS GNSS",
            "Wide temperature range -40°C ~ +85°C",
            "Proven reliability with broad software support",
        ],
    },
    "mc7350": {
        "desc": "MC7350 LTE-A Cat 4 cellular module with Qualcomm MDM9215, 150 Mbps download, Mini PCIe form factor with broad global carrier certification.",
        "overview": (
            "The MC7350 is Sierra Wireless' LTE-Advanced Cat 4 cellular module, powered by the Qualcomm MDM9215 chipset, "
            "supporting download speeds up to 150 Mbps and upload up to 50 Mbps.\n\n"
            "This module uses a standard Mini PCIe Full Size form factor. The MC7350 is in the same family as the MC7304 "
            "but features broader global band support by default. It supports USB 2.0, UART, and SPI interfaces.\n\n"
            "The MC7350 is certified by major global carriers, making it suitable for industrial routers, "
            "asset tracking, smart meters, and remote healthcare devices."
        ),
        "features": [
            "Qualcomm MDM9215 chipset",
            "LTE-A Cat 4 with download up to 150 Mbps",
            "Upload speed up to 50 Mbps",
            "Mini PCIe Full Size standard form factor",
            "USB 2.0, UART, SPI interface support",
            "Broad global carrier certification",
            "Integrated GPS / GLONASS GNSS",
            "Wide temperature range -40°C ~ +85°C",
        ],
    },
    "mc7354": {
        "desc": "MC7354 LTE-A Cat 4 cellular module with Qualcomm MDM9215, 150 Mbps download, Mini PCIe form factor optimized for regional carrier band combinations.",
        "overview": (
            "The MC7354 is Sierra Wireless' LTE-Advanced Cat 4 cellular module, powered by the Qualcomm MDM9215 chipset, "
            "supporting download speeds up to 150 Mbps and upload up to 50 Mbps.\n\n"
            "This module uses a standard Mini PCIe Full Size form factor. The MC7354 differs from other MC series modules "
            "in its specific band combination support, optimized for particular regional carrier networks. "
            "It supports USB 2.0, UART, and SPI interfaces.\n\n"
            "The MC7354 is ideal for industrial automation, transportation, smart grid, "
            "and infrastructure monitoring applications requiring reliable LTE connectivity."
        ),
        "features": [
            "Qualcomm MDM9215 chipset",
            "LTE-A Cat 4 with download up to 150 Mbps",
            "Upload speed up to 50 Mbps",
            "Mini PCIe Full Size standard form factor",
            "USB 2.0, UART, SPI interface support",
            "Optimized for regional carrier band combinations",
            "Integrated GPS / GLONASS GNSS",
            "Wide temperature range -40°C ~ +85°C",
        ],
    },
    "mc7455": {
        "desc": "MC7455 LTE-A Cat 6 cellular module with Qualcomm MDM9230, 300 Mbps download, Mini PCIe form factor for high-performance industrial and vehicle communication systems.",
        "overview": (
            "The MC7455 is Sierra Wireless' LTE-Advanced Cat 6 cellular module, powered by the Qualcomm MDM9230 chipset, "
            "supporting 2×20 MHz carrier aggregation (2×CA) with download speeds up to 300 Mbps and upload up to 50 Mbps.\n\n"
            "This module uses a standard Mini PCIe Full Size form factor and is the highest-performing model in the MC series. "
            "It supports USB 3.0, UART, and SPI interfaces for fast data throughput.\n\n"
            "The MC7455 supports major global LTE bands including FirstNet B14, "
            "widely deployed in high-performance industrial routers, vehicle communication systems, "
            "private network base stations, and enterprise connectivity solutions."
        ),
        "features": [
            "Qualcomm MDM9230 chipset",
            "LTE-A Cat 6 with 2×CA carrier aggregation",
            "Download up to 300 Mbps, upload up to 50 Mbps",
            "Mini PCIe Full Size standard form factor",
            "USB 3.0, UART, SPI interface support",
            "FirstNet B14 band support",
            "Integrated GPS / GLONASS / BeiDou GNSS",
            "Wide temperature range -40°C ~ +85°C",
        ],
    },
}


# ── Japanese product content ──────────────────────────────────────────

PRODUCT_JA = {
    "em7430": {
        "title": "EM7430 LTE-A Cat 6 セルラーモジュール",
        "desc": "EM7430 は Qualcomm MDM9230 チップセットを採用し、LTE-A Cat 6 最大 300 Mbps のダウンロード速度に対応する M.2 パッケージのセルラーモジュールで、産業用ルーターや IoT ゲートウェイに最適です。",
        "overview": (
            "EM7430 は、Sierra Wireless が提供する LTE-Advanced Cat 6 セルラーモジュールです。Qualcomm MDM9230 チップセットを採用し、"
            "2×20 MHz キャリアアグリゲーション（2×CA）に対応、ダウンロード速度は最大 300 Mbps、アップロードは最大 50 Mbps です。\n\n"
            "本モジュールは標準 M.2 3042 Key B パッケージを採用しており、産業用ルーター、IoT ゲートウェイ、モバイルホットスポット、"
            "およびビデオ監視アプリケーションに最適です。USB 3.0 および PCIe Gen2 インターフェースに対応し、柔軟なシステム統合が可能です。\n\n"
            "EM7430 はグローバル主要 LTE 周波数帯（B1–5/7/8/12/13/20/25/26/29/30/41）に対応しており、"
            "世界中で展開される IoT デバイスおよび M2M 端末に適しています。"
        ),
        "features": [
            "Qualcomm MDM9230 チップセットを採用、安定した性能",
            "LTE-A Cat 6、2×CA キャリアアグリゲーション対応",
            "ダウンロード最大 300 Mbps、アップロード 50 Mbps",
            "M.2 3042 Key B 産業用パッケージ",
            "USB 3.0 と PCIe Gen2 デュアルインターフェース対応",
            "GPS / GLONASS / BeiDou GNSS 内蔵",
            "広温度範囲 -40°C ~ +85°C",
            "FOTA ファームウェア無線更新対応",
        ],
    },
    "em7455": {
        "title": "EM7455 LTE-A Cat 6 セルラーモジュール",
        "desc": "EM7455 は Qualcomm MDM9230 チップセットを採用し、LTE-A Cat 6 最大 300 Mbps、FirstNet B14 に対応する M.2 パッケージのセルラーモジュールで、産業用ルーターやゲートウェイに最適です。",
        "overview": (
            "EM7455 は、Sierra Wireless が提供する LTE-Advanced Cat 6 セルラーモジュールです。Qualcomm MDM9230 チップセットを採用し、"
            "2×20 MHz キャリアアグリゲーション（2×CA）に対応、ダウンロード速度は最大 300 Mbps、アップロードは最大 50 Mbps です。\n\n"
            "本モジュールは標準 M.2 3042 Key B パッケージを採用しており、EM7430 と同系列ですが、特に Band 14（FirstNet）に対応している点が特徴で、"
            "米国の公共安全ネットワークアプリケーションに最適です。USB 3.0 および PCIe Gen2 インターフェースに対応しています。\n\n"
            "EM7455 はグローバル主要 LTE 周波数帯（B1–5/7/8/12/13/14/20/25/26/29/30/41）に対応しており、"
            "エンタープライズルーティング、コネクテッドビークル、公共安全通信に幅広く利用されています。"
        ),
        "features": [
            "Qualcomm MDM9230 チップセット採用",
            "LTE-A Cat 6、2×CA キャリアアグリゲーション対応",
            "ダウンロード最大 300 Mbps、アップロード 50 Mbps",
            "Band 14 FirstNet 公共安全周波数帯対応",
            "M.2 3042 Key B 産業用パッケージ",
            "USB 3.0 と PCIe Gen2 デュアルインターフェース対応",
            "GPS / GLONASS / BeiDou GNSS 内蔵",
            "広温度範囲 -40°C ~ +85°C",
        ],
    },
    "em7511": {
        "title": "EM7511 LTE-A Pro Cat 12 セルラーモジュール",
        "desc": "EM7511 は Qualcomm SDX20 チップセットを採用し、LTE-A Pro Cat 12 最大 600 Mbps に対応する M.2 パッケージのセルラーモジュールで、高性能な産業用アプリケーションに最適です。",
        "overview": (
            "EM7511 は、Sierra Wireless が提供する LTE-Advanced Pro Cat 12 セルラーモジュールです。Qualcomm SDX20 チップセットを採用し、"
            "3×20 MHz キャリアアグリゲーション（3×CA）に対応、ダウンロード速度は最大 600 Mbps、アップロードは最大 150 Mbps です。\n\n"
            "本モジュールは標準 M.2 3042 Key B パッケージを採用し、USB 3.1、PCIe Gen3、RGMII インターフェースに対応しており、"
            "より高いシステム帯域幅を提供します。SDX20 モデムは、従来世代と比較して低消費電力と優れた RF 性能を実現しています。\n\n"
            "EM7511 はグローバル LTE 周波数帯および License-Assisted Access（LAA）に対応しており、"
            "高帯域幅を必要とするビデオ監視、エンタープライズブランチオフィス、およびモバイルホットスポットアプリケーションに最適です。"
        ),
        "features": [
            "Qualcomm SDX20 モデムチップセット採用",
            "LTE-A Pro Cat 12、3×CA キャリアアグリゲーション対応",
            "ダウンロード最大 600 Mbps、アップロード 150 Mbps",
            "256QAM DL / 64QAM UL 対応",
            "M.2 3042 Key B 産業用パッケージ",
            "USB 3.1、PCIe Gen3、RGMII 対応",
            "GPS / GLONASS / BeiDou / Galileo 内蔵",
            "広温度範囲 -40°C ~ +85°C",
        ],
    },
    "em7565": {
        "title": "EM7565 LTE-A Pro Cat 12 セルラーモジュール",
        "desc": "EM7565 は Qualcomm SDX20 チップセットを採用し、LTE-A Pro Cat 12 最大 600 Mbps とデュアルバンド GNSS に対応する M.2 パッケージのセルラーモジュールで、高性能産業用ルーターに最適です。",
        "overview": (
            "EM7565 は、Sierra Wireless が提供する LTE-Advanced Pro Cat 12 セルラーモジュールです。Qualcomm SDX20 チップセットを採用し、"
            "3×20 MHz キャリアアグリゲーション（3×CA）、DL 256QAM、UL 64QAM に対応、ダウンロード速度は最大 600 Mbps、アップロードは最大 150 Mbps です。\n\n"
            "EM7565 は標準 M.2 3042 Key B パッケージを採用しており、EM7511 と比較してより多くのキャリアアグリゲーションの組み合わせに対応しています。"
            "SDX20 プラットフォームは優れた RF 性能と極めて低い消費電力を提供し、24 時間 365 日稼働する産業用機器に最適です。\n\n"
            "グローバル主要 LTE 周波数帯に加え、B14 FirstNet および B71 600 MHz に対応しており、"
            "産業用ルーター、ミッションクリティカルな通信、プロフェッショナルモバイルホットスポットに適しています。"
        ),
        "features": [
            "Qualcomm SDX20 モデムチップセット採用",
            "LTE-A Pro Cat 12、3×CA 対応",
            "ダウンロード最大 600 Mbps、アップロード 150 Mbps",
            "256QAM DL / 64QAM UL / LAA 対応",
            "M.2 3042 Key B 産業用パッケージ",
            "USB 3.1、PCIe Gen3、RGMII 対応",
            "FirstNet B14 および B71 周波数帯対応",
            "デュアルバンド GNSS（GPS + Galileo）",
        ],
    },
    "em9190": {
        "title": "EM9190 5G NR Sub-6 セルラーモジュール",
        "desc": "EM9190 は Qualcomm SDX55 チップセットを採用し、5G NR Sub-6 最大 2.5 Gbps と LTE Cat 22 に対応する M.2 パッケージのセルラーモジュールで、次世代産業用アプリケーションに最適です。",
        "overview": (
            "EM9190 は、Sierra Wireless が提供するフラッグシップ 5G NR Sub-6 セルラーモジュールです。Qualcomm SDX55 チップセットを採用し、"
            "5G SA/NSA モードに対応、ダウンロード速度は最大 2.5 Gbps（5G）/ 2.0 Gbps（LTE Cat 22）、"
            "アップロードは最大 900 Mbps（5G）です。\n\n"
            "本モジュールはカテゴリー 22 LTE（8×CA）と幅広い 5G NR Sub-6 周波数帯（n1/2/3/5/7/8/12/20/25/28/38/41/48/66/71/77/78/79）"
            "に対応しています。標準 M.2 3042 Key B パッケージを採用し、完全な 5G 接続性を提供します。\n\n"
            "EM9190 は高度な電力管理と放熱設計を備えており、高性能産業用ルーター、CPE、"
            "エンタープライズゲートウェイ、5G モバイルホットスポットに適しています。"
        ),
        "features": [
            "Qualcomm SDX55 5G モデムチップセット採用",
            "5G NR Sub-6 SA/NSA デュアルモード対応",
            "5G ダウンロード最大 2.5 Gbps、アップロード 900 Mbps",
            "LTE Cat 22 ダウンロード最大 2.0 Gbps",
            "8×CA キャリアアグリゲーション対応",
            "M.2 3042 Key B 産業用パッケージ",
            "USB 3.1、PCIe Gen3、RGMII 対応",
            "マルチバンド GNSS（GPS + GLONASS + BeiDou + Galileo + QZSS）",
        ],
    },
    "em9191": {
        "title": "EM9191 5G NR Sub-6 + mmWave セルラーモジュール",
        "desc": "EM9191 は Qualcomm SDX55 チップセットを採用し、5G NR Sub-6 と mmWave（n260/n261）に対応する M.2 パッケージのセルラーモジュールで、最上位の 5G アプリケーションに最適です。",
        "overview": (
            "EM9191 は、Sierra Wireless が提供するフラッグシップ 5G NR セルラーモジュールです。Qualcomm SDX55 チップセットを採用し、"
            "Sub-6 と mmWave（n260 39GHz / n261 28GHz）の両方に対応、最も包括的な 5G カバレッジを提供します。\n\n"
            "ダウンロード速度は最大 2.5 Gbps（5G）/ 2.0 Gbps（LTE Cat 22）、"
            "アップロードは最大 900 Mbps（5G）です。mmWave ビームフォーミング要件を満たすため、6 つのアンテナインターフェースをサポートしています。\n\n"
            "EM9191 は EM9190 と同様のすべての Sub-6 周波数帯に加え、mmWave 高周波数帯に対応しています。"
            "マルチバンド GNSS と組み合わせることで、最低遅延と最高帯域幅を必要とする Industry 4.0、"
            "スマートヘルスケア、エッジコンピューティングアプリケーションに最適です。"
        ),
        "features": [
            "Qualcomm SDX55 5G モデムチップセット採用",
            "5G NR Sub-6 + mmWave（n260/n261）対応",
            "5G ダウンロード最大 2.5 Gbps、アップロード 900 Mbps",
            "LTE Cat 22 ダウンロード最大 2.0 Gbps",
            "8×CA および mmWave ビームフォーミング対応",
            "6 つのアンテナインターフェース（mmWave アンテナ含む）",
            "M.2 3042 Key B 産業用パッケージ",
            "マルチバンド GNSS（GPS + GLONASS + BeiDou + Galileo + QZSS）",
        ],
    },
    "mc7304": {
        "title": "MC7304 LTE-A Cat 4 セルラーモジュール",
        "desc": "MC7304 は Qualcomm MDM9215 チップセットを採用し、LTE-A Cat 4 最大 150 Mbps に対応する Mini PCIe パッケージのセルラーモジュールで、コスト重視の産業用ゲートウェイやルーターに最適です。",
        "overview": (
            "MC7304 は、Sierra Wireless が提供する LTE-Advanced Cat 4 セルラーモジュールです。Qualcomm MDM9215 チップセットを採用し、"
            "ダウンロード速度は最大 150 Mbps、アップロードは最大 50 Mbps です。\n\n"
            "本モジュールは標準 Mini PCIe Full Size パッケージを採用しており、既存の産業用マザーボードや組み込みプラットフォームとの"
            "幅広い互換性を持ちます。USB 2.0、UART、SPI インターフェースに対応し、予算に制約がありつつも信頼性の高い LTE 接続が必要なアプリケーションに最適です。\n\n"
            "MC7304 はグローバル主要 LTE 周波数帯に対応しており、産業用ゲートウェイ、自動販売機、"
            "デジタルサイネージ、遠隔監視アプリケーションに幅広く採用されています。"
        ),
        "features": [
            "Qualcomm MDM9215 チップセット採用",
            "LTE-A Cat 4、ダウンロード最大 150 Mbps",
            "アップロード速度最大 50 Mbps",
            "Mini PCIe Full Size 標準パッケージ",
            "USB 2.0、UART、SPI インターフェース対応",
            "GPS / GLONASS GNSS 内蔵",
            "広温度範囲 -40°C ~ +85°C",
            "信頼性の高い安定動作、広範なソフトウェア対応",
        ],
    },
    "mc7350": {
        "title": "MC7350 LTE-A Cat 4 セルラーモジュール",
        "desc": "MC7350 は Qualcomm MDM9215 チップセットを採用し、LTE-A Cat 4 最大 150 Mbps に対応する Mini PCIe パッケージのセルラーモジュールで、グローバル展開の IoT アプリケーションに最適です。",
        "overview": (
            "MC7350 は、Sierra Wireless が提供する LTE-Advanced Cat 4 セルラーモジュールです。Qualcomm MDM9215 チップセットを採用し、"
            "ダウンロード速度は最大 150 Mbps、アップロードは最大 50 Mbps です。\n\n"
            "本モジュールは標準 Mini PCIe Full Size パッケージを採用しています。MC7350 は MC7304 と同系列であり、"
            "デフォルトでより広範なグローバル周波数帯の組み合わせに対応しています。USB 2.0、UART、SPI インターフェースに対応しています。\n\n"
            "MC7350 は世界各国の主要通信事業者から認証を取得しており、産業用ルーター、資産追跡、"
            "スマートメーター、遠隔医療機器に適しています。"
        ),
        "features": [
            "Qualcomm MDM9215 チップセット採用",
            "LTE-A Cat 4、ダウンロード最大 150 Mbps",
            "アップロード速度最大 50 Mbps",
            "Mini PCIe Full Size 標準パッケージ",
            "USB 2.0、UART、SPI インターフェース対応",
            "グローバル通信事業者の幅広い認証",
            "GPS / GLONASS GNSS 内蔵",
            "広温度範囲 -40°C ~ +85°C",
        ],
    },
    "mc7354": {
        "title": "MC7354 LTE-A Cat 4 セルラーモジュール",
        "desc": "MC7354 は Qualcomm MDM9215 チップセットを採用し、LTE-A Cat 4 最大 150 Mbps に対応する Mini PCIe パッケージのセルラーモジュールで、産業用 IoT および M2M 通信に最適です。",
        "overview": (
            "MC7354 は、Sierra Wireless が提供する LTE-Advanced Cat 4 セルラーモジュールです。Qualcomm MDM9215 チップセットを採用し、"
            "ダウンロード速度は最大 150 Mbps、アップロードは最大 50 Mbps です。\n\n"
            "本モジュールは標準 Mini PCIe Full Size パッケージを採用しています。MC7354 の主な特徴は、特定の地域の通信事業者ネットワーク向けに"
            "最適化された周波数帯の組み合わせです。USB 2.0、UART、SPI インターフェースに対応しています。\n\n"
            "MC7354 は、安定した LTE 接続を必要とする産業オートメーション、交通運輸、"
            "スマートグリッド、インフラ監視などの産業用アプリケーションに最適です。"
        ),
        "features": [
            "Qualcomm MDM9215 チップセット採用",
            "LTE-A Cat 4、ダウンロード最大 150 Mbps",
            "アップロード速度最大 50 Mbps",
            "Mini PCIe Full Size 標準パッケージ",
            "USB 2.0、UART、SPI インターフェース対応",
            "特定地域の通信事業者向け周波数帯最適化",
            "GPS / GLONASS GNSS 内蔵",
            "広温度範囲 -40°C ~ +85°C",
        ],
    },
    "mc7455": {
        "title": "MC7455 LTE-A Cat 6 セルラーモジュール",
        "desc": "MC7455 は Qualcomm MDM9230 チップセットを採用し、LTE-A Cat 6 最大 300 Mbps に対応する Mini PCIe パッケージのセルラーモジュールで、高性能な産業用アプリケーションに最適です。",
        "overview": (
            "MC7455 は、Sierra Wireless が提供する LTE-Advanced Cat 6 セルラーモジュールです。Qualcomm MDM9230 チップセットを採用し、"
            "2×20 MHz キャリアアグリゲーション（2×CA）に対応、ダウンロード速度は最大 300 Mbps、アップロードは最大 50 Mbps です。\n\n"
            "本モジュールは標準 Mini PCIe Full Size パッケージを採用しており、MC シリーズの中で最高性能のモデルです。"
            "USB 3.0、UART、SPI インターフェースに対応し、高速データ転送を実現します。\n\n"
            "MC7455 はグローバル主要 LTE 周波数帯と FirstNet B14 に対応しており、高性能産業用ルーター、"
            "車載通信システム、プライベートネットワーク基地局、エンタープライズ接続ソリューションに幅広く採用されています。"
        ),
        "features": [
            "Qualcomm MDM9230 チップセット採用",
            "LTE-A Cat 6、2×CA キャリアアグリゲーション対応",
            "ダウンロード最大 300 Mbps、アップロード 50 Mbps",
            "Mini PCIe Full Size 標準パッケージ",
            "USB 3.0、UART、SPI インターフェース対応",
            "FirstNet B14 周波数帯対応",
            "GPS / GLONASS / BeiDou GNSS 内蔵",
            "広温度範囲 -40°C ~ +85°C",
        ],
    },
}



# ── German product content (Sie-Form) ────────────────────────────────

PRODUCT_DE = {
    "em7430": {
        "title": "EM7430 LTE-A Cat 6 Mobilfunkmodul",
        "desc": "Das EM7430 ist ein LTE-A Cat 6 Mobilfunkmodul mit Qualcomm MDM9230 Chipsatz, 300 Mbps Downlink, M.2-Bauform, ideal für industrielle Router und IoT-Gateways.",
        "overview": (
            "Das EM7430 ist ein LTE-Advanced Cat 6 Mobilfunkmodul von Sierra Wireless. Es verwendet den Qualcomm MDM9230 Chipsatz "
            "und unterstützt 2×20 MHz Carrier Aggregation (2×CA) mit Download-Geschwindigkeiten von bis zu 300 Mbps und Upload bis zu 50 Mbps.\n\n"
            "Dieses Modul verwendet die standard M.2 3042 Key B Bauform und eignet sich ideal für industrielle Router, IoT-Gateways, mobile Hotspots "
            "und Videoüberwachungsanwendungen. Es unterstützt USB 3.0- und PCIe Gen2-Schnittstellen für eine flexible Systemintegration.\n\n"
            "Das EM7430 unterstützt die wichtigsten globalen LTE-Bänder (B1–5/7/8/12/13/20/25/26/29/30/41) "
            "und ist damit für weltweit eingesetzte IoT-Geräte und M2M-Endgeräte geeignet."
        ),
        "features": [
            "Qualcomm MDM9230 Chipsatz für bewährte Zuverlässigkeit",
            "LTE-A Cat 6 mit 2×CA Carrier Aggregation",
            "Download bis zu 300 Mbps, Upload bis zu 50 Mbps",
            "M.2 3042 Key B industrielle Bauform",
            "USB 3.0- und PCIe Gen2-Dualinterface-Unterstützung",
            "Integriertes GPS / GLONASS / BeiDou GNSS",
            "Weiter Temperaturbereich -40°C ~ +85°C",
            "FOTA Firmware-Over-the-Air-Update-Unterstützung",
        ],
    },
    "em7455": {
        "title": "EM7455 LTE-A Cat 6 Mobilfunkmodul",
        "desc": "Das EM7455 ist ein LTE-A Cat 6 Mobilfunkmodul mit Qualcomm MDM9230 Chipsatz, 300 Mbps Downlink, Band 14 FirstNet-Unterstützung, M.2-Bauform für öffentliche Sicherheit und Enterprise-Routing.",
        "overview": (
            "Das EM7455 ist ein LTE-Advanced Cat 6 Mobilfunkmodul von Sierra Wireless. Es verwendet den Qualcomm MDM9230 Chipsatz "
            "und unterstützt 2×20 MHz Carrier Aggregation (2×CA) mit Download-Geschwindigkeiten von bis zu 300 Mbps und Upload bis zu 50 Mbps.\n\n"
            "Dieses Modul verwendet die standard M.2 3042 Key B Bauform. Es gehört zur gleichen Familie wie das EM7430, unterstützt jedoch speziell "
            "Band 14 (FirstNet), was es ideal für US-amerikanische öffentliche Sicherheitsnetzwerke macht. Es unterstützt USB 3.0- und PCIe Gen2-Schnittstellen.\n\n"
            "Das EM7455 unterstützt die wichtigsten globalen LTE-Bänder (B1–5/7/8/12/13/14/20/25/26/29/30/41) "
            "und wird häufig in Enterprise-Routing, Connected Vehicles und öffentlichen Sicherheitskommunikationssystemen eingesetzt."
        ),
        "features": [
            "Qualcomm MDM9230 Chipsatz",
            "LTE-A Cat 6 mit 2×CA Carrier Aggregation",
            "Download bis zu 300 Mbps, Upload bis zu 50 Mbps",
            "Band 14 FirstNet für öffentliche Sicherheitsnetze",
            "M.2 3042 Key B industrielle Bauform",
            "USB 3.0- und PCIe Gen2-Dualinterface-Unterstützung",
            "Integriertes GPS / GLONASS / BeiDou GNSS",
            "Weiter Temperaturbereich -40°C ~ +85°C",
        ],
    },
    "em7511": {
        "title": "EM7511 LTE-A Pro Cat 12 Mobilfunkmodul",
        "desc": "Das EM7511 ist ein LTE-A Pro Cat 12 Mobilfunkmodul mit Qualcomm SDX20 Chipsatz, 600 Mbps Downlink, M.2-Bauform für bandbreitenintensive Unternehmens- und Industrieanwendungen.",
        "overview": (
            "Das EM7511 ist ein LTE-Advanced Pro Cat 12 Mobilfunkmodul von Sierra Wireless. Es verwendet den Qualcomm SDX20 Chipsatz "
            "und unterstützt 3×20 MHz Carrier Aggregation (3×CA) mit Download-Geschwindigkeiten von bis zu 600 Mbps und Upload bis zu 150 Mbps.\n\n"
            "Dieses Modul verwendet die standard M.2 3042 Key B Bauform mit USB 3.1-, PCIe Gen3- und RGMII-Schnittstellen "
            "für höhere Systembandbreite. Das SDX20 Modem bietet im Vergleich zu Vorgängergenerationen geringeren Stromverbrauch und bessere HF-Leistung.\n\n"
            "Das EM7511 unterstützt globale LTE-Bänder und License-Assisted Access (LAA) und ist ideal "
            "für bandbreitenintensive Videoüberwachung, Enterprise-Filialen und mobile Hotspot-Anwendungen."
        ),
        "features": [
            "Qualcomm SDX20 Modem-Chipsatz",
            "LTE-A Pro Cat 12 mit 3×CA Carrier Aggregation",
            "Download bis zu 600 Mbps, Upload bis zu 150 Mbps",
            "256QAM DL / 64QAM UL Unterstützung",
            "M.2 3042 Key B industrielle Bauform",
            "USB 3.1-, PCIe Gen3-, RGMII-Schnittstellenunterstützung",
            "Integriertes GPS / GLONASS / BeiDou / Galileo",
            "Weiter Temperaturbereich -40°C ~ +85°C",
        ],
    },
    "em7565": {
        "title": "EM7565 LTE-A Pro Cat 12 Mobilfunkmodul",
        "desc": "Das EM7565 ist ein LTE-A Pro Cat 12 Mobilfunkmodul mit Qualcomm SDX20, 600 Mbps Downlink, FirstNet B14-Unterstützung, M.2-Bauform für missionkritische Kommunikation.",
        "overview": (
            "Das EM7565 ist ein LTE-Advanced Pro Cat 12 Mobilfunkmodul von Sierra Wireless. Es verwendet den Qualcomm SDX20 Chipsatz "
            "und unterstützt 3×20 MHz Carrier Aggregation (3×CA), DL 256QAM und UL 64QAM mit Download-Geschwindigkeiten von bis zu 600 Mbps und Upload bis zu 150 Mbps.\n\n"
            "Das EM7565 verwendet die standard M.2 3042 Key B Bauform und bietet im Vergleich zum EM7511 eine breitere Carrier-Aggregation-Unterstützung. "
            "Die SDX20-Plattform liefert hervorragende HF-Leistung bei extrem niedrigem Stromverbrauch, ideal für den 24/7-Industriebetrieb.\n\n"
            "Es unterstützt wichtige globale LTE-Bänder einschließlich B14 FirstNet und B71 600 MHz "
            "und eignet sich für industrielle Router, missionkritische Kommunikation und professionelle mobile Hotspots."
        ),
        "features": [
            "Qualcomm SDX20 Modem-Chipsatz",
            "LTE-A Pro Cat 12 mit 3×CA Carrier Aggregation",
            "Download bis zu 600 Mbps, Upload bis zu 150 Mbps",
            "256QAM DL / 64QAM UL / LAA Unterstützung",
            "M.2 3042 Key B industrielle Bauform",
            "USB 3.1-, PCIe Gen3-, RGMII-Schnittstellenunterstützung",
            "FirstNet B14 und B71 Bandunterstützung",
            "Dualband GNSS (GPS + Galileo)",
        ],
    },
    "em9190": {
        "title": "EM9190 5G NR Sub-6 Mobilfunkmodul",
        "desc": "Das EM9190 ist ein 5G NR Sub-6 Mobilfunkmodul mit Qualcomm SDX55, 2.5 Gbps Downlink, M.2-Bauform für zukunftsweisende Industrie- und 5G-Anwendungen.",
        "overview": (
            "Das EM9190 ist das Flaggschiff-5G-NR-Sub-6-Mobilfunkmodul von Sierra Wireless. Es verwendet den Qualcomm SDX55 Chipsatz, "
            "unterstützt 5G SA/NSA-Modi mit Download-Geschwindigkeiten von bis zu 2.5 Gbps (5G) / 2.0 Gbps (LTE Cat 22) "
            "und Upload bis zu 900 Mbps (5G).\n\n"
            "Dieses Modul unterstützt Category 22 LTE (8×CA) mit umfassender 5G NR Sub-6-Bandabdeckung einschließlich "
            "n1/2/3/5/7/8/12/20/25/28/38/41/48/66/71/77/78/79. "
            "Es verwendet die standard M.2 3042 Key B Bauform für vollständige 5G-Konnektivität.\n\n"
            "Das EM9190 verfügt über fortschrittliches Energiemanagement und thermisches Design "
            "und eignet sich für Hochleistungs-Industrierouter, CPE, Enterprise-Gateways und 5G-Mobilfunk-Hotspots."
        ),
        "features": [
            "Qualcomm SDX55 5G Modem-Chipsatz",
            "5G NR Sub-6 SA/NSA Dual-Mode-Unterstützung",
            "5G Download bis zu 2.5 Gbps, Upload 900 Mbps",
            "LTE Cat 22 Download bis zu 2.0 Gbps",
            "8×CA Carrier Aggregation Unterstützung",
            "M.2 3042 Key B industrielle Bauform",
            "USB 3.1-, PCIe Gen3-, RGMII-Unterstützung",
            "Multiband-GNSS (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "em9191": {
        "title": "EM9191 5G NR Sub-6 + mmWave Mobilfunkmodul",
        "desc": "Das EM9191 ist ein 5G NR Sub-6 + mmWave Mobilfunkmodul mit Qualcomm SDX55, 2.5 Gbps Downlink, n260/n261-Unterstützung für umfassende 5G-Abdeckung.",
        "overview": (
            "Das EM9191 ist das Flaggschiff-5G-NR-Mobilfunkmodul von Sierra Wireless. Es verwendet den Qualcomm SDX55 Chipsatz, "
            "der sowohl Sub-6 als auch mmWave (n260 39GHz / n261 28GHz) unterstützt und damit die umfassendste 5G-Abdeckung bietet.\n\n"
            "Download-Geschwindigkeiten erreichen bis zu 2.5 Gbps (5G) / 2.0 Gbps (LTE Cat 22) "
            "mit Upload bis zu 900 Mbps (5G). Es unterstützt 6 Antennenschnittstellen für mmWave-Beamforming-Anforderungen.\n\n"
            "Das EM9191 unterstützt alle Sub-6-Bänder (wie das EM9190) plus mmWave-Hochfrequenzbänder, "
            "gepaart mit Multiband-GNSS. Ideal für Industrie 4.0, Smart Healthcare "
            "und Edge-Computing-Anwendungen mit höchsten Anforderungen an Leistung und Bandbreite."
        ),
        "features": [
            "Qualcomm SDX55 5G Modem-Chipsatz",
            "5G NR Sub-6 + mmWave (n260/n261) Unterstützung",
            "5G Download bis zu 2.5 Gbps, Upload 900 Mbps",
            "LTE Cat 22 Download bis zu 2.0 Gbps",
            "8×CA und mmWave-Beamforming-Unterstützung",
            "6 Antennenschnittstellen (inkl. mmWave-Antennen)",
            "M.2 3042 Key B industrielle Bauform",
            "Multiband-GNSS (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "mc7304": {
        "title": "MC7304 LTE-A Cat 4 Mobilfunkmodul",
        "desc": "Das MC7304 ist ein LTE-A Cat 4 Mobilfunkmodul mit Qualcomm MDM9215 Chipsatz, 150 Mbps Downlink, Mini-PCIe-Bauform für kostensensible Industrieanwendungen.",
        "overview": (
            "Das MC7304 ist ein LTE-Advanced Cat 4 Mobilfunkmodul von Sierra Wireless. Es verwendet den Qualcomm MDM9215 Chipsatz "
            "und unterstützt Download-Geschwindigkeiten von bis zu 150 Mbps und Upload bis zu 50 Mbps.\n\n"
            "Dieses Modul verwendet die standard Mini PCIe Full Size Bauform und ist mit einer Vielzahl vorhandener "
            "Industrie-Mainboards und eingebetteter Plattformen kompatibel. Es unterstützt USB 2.0-, UART- und SPI-Schnittstellen "
            "und ist ideal für preissensible Anwendungen, die zuverlässige LTE-Konnektivität benötigen.\n\n"
            "Das MC7304 unterstützt wichtige globale LTE-Bänder und wird häufig in Industrie-Gateways, "
            "Verkaufsautomaten, digitaler Beschilderung und Fernüberwachungsanwendungen eingesetzt."
        ),
        "features": [
            "Qualcomm MDM9215 Chipsatz",
            "LTE-A Cat 4 mit Download bis zu 150 Mbps",
            "Upload-Geschwindigkeit bis zu 50 Mbps",
            "Mini PCIe Full Size Standard-Bauform",
            "USB 2.0-, UART-, SPI-Schnittstellenunterstützung",
            "Integriertes GPS / GLONASS GNSS",
            "Weiter Temperaturbereich -40°C ~ +85°C",
            "Bewährte Zuverlässigkeit mit breiter Softwareunterstützung",
        ],
    },
    "mc7350": {
        "title": "MC7350 LTE-A Cat 4 Mobilfunkmodul",
        "desc": "Das MC7350 ist ein LTE-A Cat 4 Mobilfunkmodul mit Qualcomm MDM9215 Chipsatz, 150 Mbps Downlink, Mini-PCIe-Bauform mit breiter globaler Carrier-Zertifizierung.",
        "overview": (
            "Das MC7350 ist ein LTE-Advanced Cat 4 Mobilfunkmodul von Sierra Wireless. Es verwendet den Qualcomm MDM9215 Chipsatz "
            "und unterstützt Download-Geschwindigkeiten von bis zu 150 Mbps und Upload bis zu 50 Mbps.\n\n"
            "Dieses Modul verwendet die standard Mini PCIe Full Size Bauform. Das MC7350 gehört zur gleichen Familie wie das MC7304, "
            "bietet jedoch standardmäßig eine breitere globale Bandunterstützung. Es unterstützt USB 2.0-, UART- und SPI-Schnittstellen.\n\n"
            "Das MC7350 ist von großen globalen Carriern zertifiziert und eignet sich für industrielle Router, "
            "Asset-Tracking, Smart Meter und Fernüberwachung im Gesundheitswesen."
        ),
        "features": [
            "Qualcomm MDM9215 Chipsatz",
            "LTE-A Cat 4 mit Download bis zu 150 Mbps",
            "Upload-Geschwindigkeit bis zu 50 Mbps",
            "Mini PCIe Full Size Standard-Bauform",
            "USB 2.0-, UART-, SPI-Schnittstellenunterstützung",
            "Breite globale Carrier-Zertifizierung",
            "Integriertes GPS / GLONASS GNSS",
            "Weiter Temperaturbereich -40°C ~ +85°C",
        ],
    },
    "mc7354": {
        "title": "MC7354 LTE-A Cat 4 Mobilfunkmodul",
        "desc": "Das MC7354 ist ein LTE-A Cat 4 Mobilfunkmodul mit Qualcomm MDM9215 Chipsatz, 150 Mbps Downlink, Mini-PCIe-Bauform, optimiert für regionale Carrier-Bandkombinationen.",
        "overview": (
            "Das MC7354 ist ein LTE-Advanced Cat 4 Mobilfunkmodul von Sierra Wireless. Es verwendet den Qualcomm MDM9215 Chipsatz "
            "und unterstützt Download-Geschwindigkeiten von bis zu 150 Mbps und Upload bis zu 50 Mbps.\n\n"
            "Dieses Modul verwendet die standard Mini PCIe Full Size Bauform. Das MC7354 unterscheidet sich von anderen MC-Serie-Modulen "
            "durch seine spezifischen Bandkombinationen, die für bestimmte regionale Carrier-Netzwerke optimiert sind. "
            "Es unterstützt USB 2.0-, UART- und SPI-Schnittstellen.\n\n"
            "Das MC7354 ist ideal für Industrieautomation, Transportwesen, Smart Grid "
            "und Infrastrukturüberwachungsanwendungen, die zuverlässige LTE-Konnektivität erfordern."
        ),
        "features": [
            "Qualcomm MDM9215 Chipsatz",
            "LTE-A Cat 4 mit Download bis zu 150 Mbps",
            "Upload-Geschwindigkeit bis zu 50 Mbps",
            "Mini PCIe Full Size Standard-Bauform",
            "USB 2.0-, UART-, SPI-Schnittstellenunterstützung",
            "Optimiert für regionale Carrier-Bandkombinationen",
            "Integriertes GPS / GLONASS GNSS",
            "Weiter Temperaturbereich -40°C ~ +85°C",
        ],
    },
    "mc7455": {
        "title": "MC7455 LTE-A Cat 6 Mobilfunkmodul",
        "desc": "Das MC7455 ist ein LTE-A Cat 6 Mobilfunkmodul mit Qualcomm MDM9230 Chipsatz, 300 Mbps Downlink, Mini-PCIe-Bauform für Hochleistungs-Industrie- und Fahrzeugkommunikationssysteme.",
        "overview": (
            "Das MC7455 ist ein LTE-Advanced Cat 6 Mobilfunkmodul von Sierra Wireless. Es verwendet den Qualcomm MDM9230 Chipsatz "
            "und unterstützt 2×20 MHz Carrier Aggregation (2×CA) mit Download-Geschwindigkeiten von bis zu 300 Mbps und Upload bis zu 50 Mbps.\n\n"
            "Dieses Modul verwendet die standard Mini PCIe Full Size Bauform und ist das leistungsstärkste Modell der MC-Serie. "
            "Es unterstützt USB 3.0-, UART- und SPI-Schnittstellen für schnellen Datendurchsatz.\n\n"
            "Das MC7455 unterstützt wichtige globale LTE-Bänder einschließlich FirstNet B14 "
            "und wird häufig in Hochleistungs-Industrieroutern, Fahrzeugkommunikationssystemen, "
            "privaten Netzwerk-Basisstationen und Enterprise-Konnektivitätslösungen eingesetzt."
        ),
        "features": [
            "Qualcomm MDM9230 Chipsatz",
            "LTE-A Cat 6 mit 2×CA Carrier Aggregation",
            "Download bis zu 300 Mbps, Upload bis zu 50 Mbps",
            "Mini PCIe Full Size Standard-Bauform",
            "USB 3.0-, UART-, SPI-Schnittstellenunterstützung",
            "FirstNet B14 Bandunterstützung",
            "Integriertes GPS / GLONASS / BeiDou GNSS",
            "Weiter Temperaturbereich -40°C ~ +85°C",
        ],
    },
}


# ── French product content ──────────────────────────────────────────

PRODUCT_FR = {
    "em7430": {
        "title": "EM7430 LTE-A Cat 6 Module cellulaire",
        "desc": "Le module cellulaire EM7430 LTE-A Cat 6 est \u00e9quip\u00e9 du chipset Qualcomm MDM9230, avec t\u00e9l\u00e9chargement \u00e0 300 Mbps, format M.2, id\u00e9al pour les routeurs industriels et les passerelles IoT.",
        "overview": (
            "L'EM7430 est un module cellulaire LTE-Advanced Cat 6 de Sierra Wireless. Il est \u00e9quip\u00e9 du chipset Qualcomm MDM9230 "
            "et prend en charge l'agr\u00e9gation de porteuses 2\u00d720 MHz (2\u00d7CA) avec des vitesses de t\u00e9l\u00e9chargement allant jusqu'\u00e0 300 Mbps et un upload jusqu'\u00e0 50 Mbps.\n\n"
            "Ce module utilise un format standard M.2 3042 Key B, id\u00e9al pour les routeurs industriels, les passerelles IoT, les points d'acc\u00e8s mobiles "
            "et les applications de vid\u00e9osurveillance. Il prend en charge les interfaces USB 3.0 et PCIe Gen2 pour une int\u00e9gration syst\u00e8me flexible.\n\n"
            "L'EM7430 prend en charge les principales bandes LTE mondiales (B1\u20135/7/8/12/13/20/25/26/29/30/41), "
            "ce qui le rend adapt\u00e9 aux appareils IoT et aux terminaux M2M d\u00e9ploy\u00e9s dans le monde entier."
        ),
        "features": [
            "Chipset Qualcomm MDM9230 pour une fiabilit\u00e9 \u00e9prouv\u00e9e",
            "LTE-A Cat 6 avec agr\u00e9gation de porteuses 2\u00d7CA",
            "T\u00e9l\u00e9chargement jusqu'\u00e0 300 Mbps, upload jusqu'\u00e0 50 Mbps",
            "Format industriel M.2 3042 Key B",
            "Prise en charge des interfaces USB 3.0 et PCIe Gen2",
            "GNSS int\u00e9gr\u00e9 GPS / GLONASS / BeiDou",
            "Large plage de temp\u00e9rature -40\u00b0C ~ +85\u00b0C",
            "Mise \u00e0 jour FOTA du firmware par liaison radio",
        ],
    },
    "em7455": {
        "title": "EM7455 LTE-A Cat 6 Module cellulaire",
        "desc": "Le module cellulaire EM7455 LTE-A Cat 6 est \u00e9quip\u00e9 du chipset Qualcomm MDM9230, avec t\u00e9l\u00e9chargement \u00e0 300 Mbps et prise en charge de la bande 14 FirstNet, format M.2 pour la s\u00e9curit\u00e9 publique et le routage d'entreprise.",
        "overview": (
            "L'EM7455 est un module cellulaire LTE-Advanced Cat 6 de Sierra Wireless. Il est \u00e9quip\u00e9 du chipset Qualcomm MDM9230 "
            "et prend en charge l'agr\u00e9gation de porteuses 2\u00d720 MHz (2\u00d7CA) avec des vitesses de t\u00e9l\u00e9chargement allant jusqu'\u00e0 300 Mbps et un upload jusqu'\u00e0 50 Mbps.\n\n"
            "Ce module utilise un format standard M.2 3042 Key B. Il fait partie de la m\u00eame famille que l'EM7430 mais prend sp\u00e9cifiquement en charge "
            "la bande 14 (FirstNet), ce qui le rend id\u00e9al pour les applications de r\u00e9seaux de s\u00e9curit\u00e9 publique am\u00e9ricains. Il prend en charge les interfaces USB 3.0 et PCIe Gen2.\n\n"
            "L'EM7455 prend en charge les principales bandes LTE mondiales (B1\u20135/7/8/12/13/14/20/25/26/29/30/41) "
            "et est largement utilis\u00e9 dans le routage d'entreprise, les v\u00e9hicules connect\u00e9s et les communications de s\u00e9curit\u00e9 publique."
        ),
        "features": [
            "Chipset Qualcomm MDM9230",
            "LTE-A Cat 6 avec agr\u00e9gation de porteuses 2\u00d7CA",
            "T\u00e9l\u00e9chargement jusqu'\u00e0 300 Mbps, upload jusqu'\u00e0 50 Mbps",
            "Prise en charge de la bande 14 FirstNet pour la s\u00e9curit\u00e9 publique",
            "Format industriel M.2 3042 Key B",
            "Prise en charge des interfaces USB 3.0 et PCIe Gen2",
            "GNSS int\u00e9gr\u00e9 GPS / GLONASS / BeiDou",
            "Large plage de temp\u00e9rature -40\u00b0C ~ +85\u00b0C",
        ],
    },
    "em7511": {
        "title": "EM7511 LTE-A Pro Cat 12 Module cellulaire",
        "desc": "Le module cellulaire EM7511 LTE-A Pro Cat 12 est \u00e9quip\u00e9 du chipset Qualcomm SDX20, avec t\u00e9l\u00e9chargement \u00e0 600 Mbps, format M.2 pour les applications industrielles et d'entreprise \u00e0 large bande passante.",
        "overview": (
            "L'EM7511 est un module cellulaire LTE-Advanced Pro Cat 12 de Sierra Wireless. Il est \u00e9quip\u00e9 du chipset Qualcomm SDX20 "
            "et prend en charge l'agr\u00e9gation de porteuses 3\u00d720 MHz (3\u00d7CA) avec des vitesses de t\u00e9l\u00e9chargement allant jusqu'\u00e0 600 Mbps et un upload jusqu'\u00e0 150 Mbps.\n\n"
            "Ce module utilise un format standard M.2 3042 Key B avec des interfaces USB 3.1, PCIe Gen3 et RGMII "
            "pour une bande passante syst\u00e8me plus \u00e9lev\u00e9e. Le modem SDX20 offre une consommation d'\u00e9nergie r\u00e9duite et des performances RF sup\u00e9rieures par rapport aux g\u00e9n\u00e9rations pr\u00e9c\u00e9dentes.\n\n"
            "L'EM7511 prend en charge les bandes LTE mondiales et License-Assisted Access (LAA), id\u00e9al "
            "pour la vid\u00e9osurveillance \u00e0 large bande passante, les succursales d'entreprise et les applications de points d'acc\u00e8s mobiles."
        ),
        "features": [
            "Chipset modem Qualcomm SDX20",
            "LTE-A Pro Cat 12 avec agr\u00e9gation de porteuses 3\u00d7CA",
            "T\u00e9l\u00e9chargement jusqu'\u00e0 600 Mbps, upload jusqu'\u00e0 150 Mbps",
            "Prise en charge 256QAM DL / 64QAM UL",
            "Format industriel M.2 3042 Key B",
            "Prise en charge des interfaces USB 3.1, PCIe Gen3, RGMII",
            "GNSS int\u00e9gr\u00e9 GPS / GLONASS / BeiDou / Galileo",
            "Large plage de temp\u00e9rature -40\u00b0C ~ +85\u00b0C",
        ],
    },
    "em7565": {
        "title": "EM7565 LTE-A Pro Cat 12 Module cellulaire",
        "desc": "Le module cellulaire EM7565 LTE-A Pro Cat 12 est \u00e9quip\u00e9 du chipset Qualcomm SDX20, avec t\u00e9l\u00e9chargement \u00e0 600 Mbps et prise en charge FirstNet B14, format M.2 pour les communications critiques.",
        "overview": (
            "L'EM7565 est un module cellulaire LTE-Advanced Pro Cat 12 de Sierra Wireless. Il est \u00e9quip\u00e9 du chipset Qualcomm SDX20 "
            "et prend en charge l'agr\u00e9gation de porteuses 3\u00d720 MHz (3\u00d7CA), DL 256QAM et UL 64QAM avec des vitesses de t\u00e9l\u00e9chargement allant jusqu'\u00e0 600 Mbps et un upload jusqu'\u00e0 150 Mbps.\n\n"
            "L'EM7565 utilise un format standard M.2 3042 Key B et offre une prise en charge plus large de l'agr\u00e9gation de porteuses par rapport \u00e0 l'EM7511. "
            "La plateforme SDX20 offre d'excellentes performances RF avec une consommation d'\u00e9nergie extr\u00eamement faible, id\u00e9ale pour un fonctionnement industriel 24h/24 et 7j/7.\n\n"
            "Il prend en charge les principales bandes LTE mondiales, y compris B14 FirstNet et B71 600 MHz, "
            "ce qui le rend adapt\u00e9 aux routeurs industriels, aux communications critiques et aux points d'acc\u00e8s mobiles professionnels."
        ),
        "features": [
            "Chipset modem Qualcomm SDX20",
            "LTE-A Pro Cat 12 avec agr\u00e9gation de porteuses 3\u00d7CA",
            "T\u00e9l\u00e9chargement jusqu'\u00e0 600 Mbps, upload jusqu'\u00e0 150 Mbps",
            "Prise en charge 256QAM DL / 64QAM UL / LAA",
            "Format industriel M.2 3042 Key B",
            "Prise en charge des interfaces USB 3.1, PCIe Gen3, RGMII",
            "Prise en charge des bandes FirstNet B14 et B71",
            "GNSS double bande (GPS + Galileo)",
        ],
    },
    "em9190": {
        "title": "EM9190 5G NR Sub-6 Module cellulaire",
        "desc": "Le module cellulaire EM9190 5G NR Sub-6 est \u00e9quip\u00e9 du chipset Qualcomm SDX55, avec t\u00e9l\u00e9chargement \u00e0 2.5 Gbps, format M.2 pour les applications industrielles et 5G de nouvelle g\u00e9n\u00e9ration.",
        "overview": (
            "L'EM9190 est le module cellulaire 5G NR Sub-6 phare de Sierra Wireless. Il est \u00e9quip\u00e9 du chipset Qualcomm SDX55, "
            "prend en charge les modes 5G SA/NSA avec des vitesses de t\u00e9l\u00e9chargement allant jusqu'\u00e0 2.5 Gbps (5G) / 2.0 Gbps (LTE Cat 22) "
            "et un upload jusqu'\u00e0 900 Mbps (5G).\n\n"
            "Ce module prend en charge la cat\u00e9gorie 22 LTE (8\u00d7CA) avec une couverture \u00e9tendue des bandes 5G NR Sub-6, y compris "
            "n1/2/3/5/7/8/12/20/25/28/38/41/48/66/71/77/78/79. "
            "Il utilise un format standard M.2 3042 Key B pour une connectivit\u00e9 5G compl\u00e8te.\n\n"
            "L'EM9190 dispose d'une gestion avanc\u00e9e de l'alimentation et d'une conception thermique optimis\u00e9e, "
            "ce qui le rend adapt\u00e9 aux routeurs industriels haute performance, CPE, passerelles d'entreprise et points d'acc\u00e8s mobiles 5G."
        ),
        "features": [
            "Chipset modem 5G Qualcomm SDX55",
            "Prise en charge du mode double 5G NR Sub-6 SA/NSA",
            "T\u00e9l\u00e9chargement 5G jusqu'\u00e0 2.5 Gbps, upload 900 Mbps",
            "T\u00e9l\u00e9chargement LTE Cat 22 jusqu'\u00e0 2.0 Gbps",
            "Prise en charge de l'agr\u00e9gation de porteuses 8\u00d7CA",
            "Format industriel M.2 3042 Key B",
            "Prise en charge USB 3.1, PCIe Gen3, RGMII",
            "GNSS multibande (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "em9191": {
        "title": "EM9191 5G NR Sub-6 + mmWave Module cellulaire",
        "desc": "Le module cellulaire EM9191 5G NR Sub-6 + mmWave est \u00e9quip\u00e9 du chipset Qualcomm SDX55, avec t\u00e9l\u00e9chargement \u00e0 2.5 Gbps, prenant en charge n260/n261 pour une couverture 5G compl\u00e8te.",
        "overview": (
            "L'EM9191 est le module cellulaire 5G NR phare de Sierra Wireless. Il est \u00e9quip\u00e9 du chipset Qualcomm SDX55, "
            "prenant en charge \u00e0 la fois le Sub-6 et le mmWave (n260 39GHz / n261 28GHz) pour la couverture 5G la plus compl\u00e8te.\n\n"
            "Les vitesses de t\u00e9l\u00e9chargement atteignent jusqu'\u00e0 2.5 Gbps (5G) / 2.0 Gbps (LTE Cat 22) "
            "avec un upload jusqu'\u00e0 900 Mbps (5G). Il prend en charge 6 interfaces d'antenne pour les besoins de formation de faisceaux mmWave.\n\n"
            "L'EM9191 prend en charge toutes les bandes Sub-6 (comme l'EM9190) plus les bandes haute fr\u00e9quence mmWave, "
            "associ\u00e9es \u00e0 un GNSS multibande. Id\u00e9al pour l'Industrie 4.0, la sant\u00e9 connect\u00e9e "
            "et les applications de edge computing n\u00e9cessitant la plus faible latence et la plus grande bande passante."
        ),
        "features": [
            "Chipset modem 5G Qualcomm SDX55",
            "Prise en charge 5G NR Sub-6 + mmWave (n260/n261)",
            "T\u00e9l\u00e9chargement 5G jusqu'\u00e0 2.5 Gbps, upload 900 Mbps",
            "T\u00e9l\u00e9chargement LTE Cat 22 jusqu'\u00e0 2.0 Gbps",
            "Prise en charge 8\u00d7CA et formation de faisceaux mmWave",
            "6 interfaces d'antenne (antennes mmWave incluses)",
            "Format industriel M.2 3042 Key B",
            "GNSS multibande (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "mc7304": {
        "title": "MC7304 LTE-A Cat 4 Module cellulaire",
        "desc": "Le module cellulaire MC7304 LTE-A Cat 4 est \u00e9quip\u00e9 du chipset Qualcomm MDM9215, avec t\u00e9l\u00e9chargement \u00e0 150 Mbps, format Mini PCIe pour les applications industrielles \u00e9conomiques.",
        "overview": (
            "Le MC7304 est un module cellulaire LTE-Advanced Cat 4 de Sierra Wireless. Il est \u00e9quip\u00e9 du chipset Qualcomm MDM9215 "
            "et prend en charge des vitesses de t\u00e9l\u00e9chargement allant jusqu'\u00e0 150 Mbps et un upload jusqu'\u00e0 50 Mbps.\n\n"
            "Ce module utilise un format standard Mini PCIe Full Size, compatible avec une large gamme de "
            "cartes m\u00e8res industrielles et de plateformes embarqu\u00e9es existantes. Il prend en charge les interfaces USB 2.0, UART et SPI, "
            "id\u00e9al pour les applications soucieuses de leur budget n\u00e9cessitant une connectivit\u00e9 LTE fiable.\n\n"
            "Le MC7304 prend en charge les principales bandes LTE mondiales et est largement d\u00e9ploy\u00e9 dans les passerelles industrielles, "
            "les distributeurs automatiques, l'affichage num\u00e9rique et les applications de surveillance \u00e0 distance."
        ),
        "features": [
            "Chipset Qualcomm MDM9215",
            "LTE-A Cat 4 avec t\u00e9l\u00e9chargement jusqu'\u00e0 150 Mbps",
            "Vitesse d'upload jusqu'\u00e0 50 Mbps",
            "Format standard Mini PCIe Full Size",
            "Prise en charge des interfaces USB 2.0, UART, SPI",
            "GNSS int\u00e9gr\u00e9 GPS / GLONASS",
            "Large plage de temp\u00e9rature -40\u00b0C ~ +85\u00b0C",
            "Fiabilit\u00e9 \u00e9prouv\u00e9e avec un large support logiciel",
        ],
    },
    "mc7350": {
        "title": "MC7350 LTE-A Cat 4 Module cellulaire",
        "desc": "Le module cellulaire MC7350 LTE-A Cat 4 est \u00e9quip\u00e9 du chipset Qualcomm MDM9215, avec t\u00e9l\u00e9chargement \u00e0 150 Mbps, format Mini PCIe avec une large certification mondiale des op\u00e9rateurs.",
        "overview": (
            "Le MC7350 est un module cellulaire LTE-Advanced Cat 4 de Sierra Wireless. Il est \u00e9quip\u00e9 du chipset Qualcomm MDM9215 "
            "et prend en charge des vitesses de t\u00e9l\u00e9chargement allant jusqu'\u00e0 150 Mbps et un upload jusqu'\u00e0 50 Mbps.\n\n"
            "Ce module utilise un format standard Mini PCIe Full Size. Le MC7350 fait partie de la m\u00eame famille que le MC7304 "
            "mais offre par d\u00e9faut une prise en charge plus large des bandes mondiales. Il prend en charge les interfaces USB 2.0, UART et SPI.\n\n"
            "Le MC7350 est certifi\u00e9 par les principaux op\u00e9rateurs mondiaux, ce qui le rend adapt\u00e9 aux routeurs industriels, "
            "\u00e0 la localisation d'actifs, aux compteurs intelligents et aux dispositifs de t\u00e9l\u00e9sant\u00e9."
        ),
        "features": [
            "Chipset Qualcomm MDM9215",
            "LTE-A Cat 4 avec t\u00e9l\u00e9chargement jusqu'\u00e0 150 Mbps",
            "Vitesse d'upload jusqu'\u00e0 50 Mbps",
            "Format standard Mini PCIe Full Size",
            "Prise en charge des interfaces USB 2.0, UART, SPI",
            "Large certification mondiale des op\u00e9rateurs",
            "GNSS int\u00e9gr\u00e9 GPS / GLONASS",
            "Large plage de temp\u00e9rature -40\u00b0C ~ +85\u00b0C",
        ],
    },
    "mc7354": {
        "title": "MC7354 LTE-A Cat 4 Module cellulaire",
        "desc": "Le module cellulaire MC7354 LTE-A Cat 4 est \u00e9quip\u00e9 du chipset Qualcomm MDM9215, avec t\u00e9l\u00e9chargement \u00e0 150 Mbps, format Mini PCIe optimis\u00e9 pour les combinaisons de bandes r\u00e9gionales.",
        "overview": (
            "Le MC7354 est un module cellulaire LTE-Advanced Cat 4 de Sierra Wireless. Il est \u00e9quip\u00e9 du chipset Qualcomm MDM9215 "
            "et prend en charge des vitesses de t\u00e9l\u00e9chargement allant jusqu'\u00e0 150 Mbps et un upload jusqu'\u00e0 50 Mbps.\n\n"
            "Ce module utilise un format standard Mini PCIe Full Size. Le MC7354 se distingue des autres modules de la s\u00e9rie MC "
            "par ses combinaisons de bandes sp\u00e9cifiques, optimis\u00e9es pour les r\u00e9seaux d'op\u00e9rateurs r\u00e9gionaux particuliers. "
            "Il prend en charge les interfaces USB 2.0, UART et SPI.\n\n"
            "Le MC7354 est id\u00e9al pour l'automatisation industrielle, le transport, les r\u00e9seaux intelligents "
            "et les applications de surveillance d'infrastructure n\u00e9cessitant une connectivit\u00e9 LTE fiable."
        ),
        "features": [
            "Chipset Qualcomm MDM9215",
            "LTE-A Cat 4 avec t\u00e9l\u00e9chargement jusqu'\u00e0 150 Mbps",
            "Vitesse d'upload jusqu'\u00e0 50 Mbps",
            "Format standard Mini PCIe Full Size",
            "Prise en charge des interfaces USB 2.0, UART, SPI",
            "Optimis\u00e9 pour les combinaisons de bandes r\u00e9gionales",
            "GNSS int\u00e9gr\u00e9 GPS / GLONASS",
            "Large plage de temp\u00e9rature -40\u00b0C ~ +85\u00b0C",
        ],
    },
    "mc7455": {
        "title": "MC7455 LTE-A Cat 6 Module cellulaire",
        "desc": "Le module cellulaire MC7455 LTE-A Cat 6 est \u00e9quip\u00e9 du chipset Qualcomm MDM9230, avec t\u00e9l\u00e9chargement \u00e0 300 Mbps, format Mini PCIe pour les syst\u00e8mes de communication industriels et v\u00e9hiculaires haute performance.",
        "overview": (
            "Le MC7455 est un module cellulaire LTE-Advanced Cat 6 de Sierra Wireless. Il est \u00e9quip\u00e9 du chipset Qualcomm MDM9230 "
            "et prend en charge l'agr\u00e9gation de porteuses 2\u00d720 MHz (2\u00d7CA) avec des vitesses de t\u00e9l\u00e9chargement allant jusqu'\u00e0 300 Mbps et un upload jusqu'\u00e0 50 Mbps.\n\n"
            "Ce module utilise un format standard Mini PCIe Full Size et est le mod\u00e8le le plus performant de la s\u00e9rie MC. "
            "Il prend en charge les interfaces USB 3.0, UART et SPI pour un d\u00e9bit de donn\u00e9es rapide.\n\n"
            "Le MC7455 prend en charge les principales bandes LTE mondiales, y compris FirstNet B14, "
            "et est largement d\u00e9ploy\u00e9 dans les routeurs industriels haute performance, les syst\u00e8mes de communication v\u00e9hiculaires, "
            "les stations de base de r\u00e9seaux priv\u00e9s et les solutions de connectivit\u00e9 d'entreprise."
        ),
        "features": [
            "Chipset Qualcomm MDM9230",
            "LTE-A Cat 6 avec agr\u00e9gation de porteuses 2\u00d7CA",
            "T\u00e9l\u00e9chargement jusqu'\u00e0 300 Mbps, upload jusqu'\u00e0 50 Mbps",
            "Format standard Mini PCIe Full Size",
            "Prise en charge des interfaces USB 3.0, UART, SPI",
            "Prise en charge de la bande FirstNet B14",
            "GNSS int\u00e9gr\u00e9 GPS / GLONASS / BeiDou",
            "Large plage de temp\u00e9rature -40\u00b0C ~ +85\u00b0C",
        ],
    },
}


# ── Spanish product content (formal, usted register) ──────────────────────

PRODUCT_ES = {
    "em7430": {
        "title": "EM7430 Módulo Celular LTE-A Cat 6",
        "desc": "El EM7430 es un módulo celular LTE-A Cat 6 con chipset Qualcomm MDM9230, descarga de 300 Mbps, formato M.2, ideal para routers industriales y pasarelas IoT.",
        "overview": (
            "El EM7430 es un módulo celular LTE-Advanced Cat 6 de Sierra Wireless. Utiliza el chipset Qualcomm MDM9230 "
            "y soporta agregación de portadoras 2×20 MHz (2×CA) con velocidades de descarga de hasta 300 Mbps y subida de hasta 50 Mbps.\n\n"
            "Este módulo utiliza el formato estándar M.2 3042 Key B, ideal para routers industriales, pasarelas IoT, puntos de acceso móviles "
            "y aplicaciones de videovigilancia. Soporta interfaces USB 3.0 y PCIe Gen2 para una integración flexible del sistema.\n\n"
            "El EM7430 soporta las principales bandas LTE globales (B1–5/7/8/12/13/20/25/26/29/30/41), "
            "siendo adecuado para dispositivos IoT y terminales M2M desplegados en todo el mundo."
        ),
        "features": [
            "Chipset Qualcomm MDM9230 para fiabilidad probada",
            "LTE-A Cat 6 con agregación de portadoras 2×CA",
            "Descarga hasta 300 Mbps, subida hasta 50 Mbps",
            "Formato industrial M.2 3042 Key B",
            "Soporte de interfaces duales USB 3.0 y PCIe Gen2",
            "GNSS integrado GPS / GLONASS / BeiDou",
            "Amplio rango de temperatura -40°C ~ +85°C",
            "Actualización FOTA de firmware por vía inalámbrica",
        ],
    },
    "em7455": {
        "title": "EM7455 Módulo Celular LTE-A Cat 6",
        "desc": "El EM7455 es un módulo celular LTE-A Cat 6 con chipset Qualcomm MDM9230, descarga de 300 Mbps y soporte de banda 14 FirstNet, formato M.2 para seguridad pública y routing empresarial.",
        "overview": (
            "El EM7455 es un módulo celular LTE-Advanced Cat 6 de Sierra Wireless. Utiliza el chipset Qualcomm MDM9230 "
            "y soporta agregación de portadoras 2×20 MHz (2×CA) con velocidades de descarga de hasta 300 Mbps y subida de hasta 50 Mbps.\n\n"
            "Este módulo utiliza el formato estándar M.2 3042 Key B. Pertenece a la misma familia que el EM7430 pero soporta específicamente "
            "la banda 14 (FirstNet), lo que lo hace ideal para aplicaciones de redes de seguridad pública estadounidenses. Soporta interfaces USB 3.0 y PCIe Gen2.\n\n"
            "El EM7455 soporta las principales bandas LTE globales (B1–5/7/8/12/13/14/20/25/26/29/30/41) "
            "y se utiliza ampliamente en routing empresarial, vehículos conectados y comunicaciones de seguridad pública."
        ),
        "features": [
            "Chipset Qualcomm MDM9230",
            "LTE-A Cat 6 con agregación de portadoras 2×CA",
            "Descarga hasta 300 Mbps, subida hasta 50 Mbps",
            "Soporte de banda 14 FirstNet para seguridad pública",
            "Formato industrial M.2 3042 Key B",
            "Soporte de interfaces USB 3.0 y PCIe Gen2",
            "GNSS integrado GPS / GLONASS / BeiDou",
            "Amplio rango de temperatura -40°C ~ +85°C",
        ],
    },
    "em7511": {
        "title": "EM7511 Módulo Celular LTE-A Pro Cat 12",
        "desc": "El EM7511 es un módulo celular LTE-A Pro Cat 12 con chipset Qualcomm SDX20, descarga de 600 Mbps, formato M.2 para aplicaciones empresariales e industriales de alto ancho de banda.",
        "overview": (
            "El EM7511 es un módulo celular LTE-Advanced Pro Cat 12 de Sierra Wireless. Utiliza el chipset Qualcomm SDX20 "
            "y soporta agregación de portadoras 3×20 MHz (3×CA) con velocidades de descarga de hasta 600 Mbps y subida de hasta 150 Mbps.\n\n"
            "Este módulo utiliza el formato estándar M.2 3042 Key B con interfaces USB 3.1, PCIe Gen3 y RGMII "
            "para un mayor ancho de banda del sistema. El módem SDX20 ofrece menor consumo de energía y rendimiento RF superior en comparación con generaciones anteriores.\n\n"
            "El EM7511 soporta bandas LTE globales y License-Assisted Access (LAA), ideal "
            "para videovigilancia de alto ancho de banda, oficinas sucursales empresariales y aplicaciones de punto de acceso móvil."
        ),
        "features": [
            "Chipset de módem Qualcomm SDX20",
            "LTE-A Pro Cat 12 con agregación de portadoras 3×CA",
            "Descarga hasta 600 Mbps, subida hasta 150 Mbps",
            "Soporte 256QAM DL / 64QAM UL",
            "Formato industrial M.2 3042 Key B",
            "Soporte de interfaces USB 3.1, PCIe Gen3, RGMII",
            "GNSS integrado GPS / GLONASS / BeiDou / Galileo",
            "Amplio rango de temperatura -40°C ~ +85°C",
        ],
    },
    "em7565": {
        "title": "EM7565 Módulo Celular LTE-A Pro Cat 12",
        "desc": "El EM7565 es un módulo celular LTE-A Pro Cat 12 con chipset Qualcomm SDX20, descarga de 600 Mbps y soporte FirstNet B14, formato M.2 para comunicaciones críticas.",
        "overview": (
            "El EM7565 es un módulo celular LTE-Advanced Pro Cat 12 de Sierra Wireless. Utiliza el chipset Qualcomm SDX20 "
            "y soporta agregación de portadoras 3×20 MHz (3×CA), DL 256QAM y UL 64QAM con velocidades de descarga de hasta 600 Mbps y subida de hasta 150 Mbps.\n\n"
            "El EM7565 utiliza el formato estándar M.2 3042 Key B y ofrece un soporte de agregación de portadoras más amplio que el EM7511. "
            "La plataforma SDX20 proporciona un rendimiento RF excepcional con un consumo de energía extremadamente bajo, ideal para operación industrial 24/7.\n\n"
            "Soporta las principales bandas LTE globales, incluyendo B14 FirstNet y B71 600 MHz, "
            "siendo adecuado para routers industriales, comunicaciones críticas y puntos de acceso móviles profesionales."
        ),
        "features": [
            "Chipset de módem Qualcomm SDX20",
            "LTE-A Pro Cat 12 con agregación de portadoras 3×CA",
            "Descarga hasta 600 Mbps, subida hasta 150 Mbps",
            "Soporte 256QAM DL / 64QAM UL / LAA",
            "Formato industrial M.2 3042 Key B",
            "Soporte de interfaces USB 3.1, PCIe Gen3, RGMII",
            "Soporte de bandas FirstNet B14 y B71",
            "GNSS de doble banda (GPS + Galileo)",
        ],
    },
    "em9190": {
        "title": "EM9190 Módulo Celular 5G NR Sub-6",
        "desc": "El EM9190 es un módulo celular 5G NR Sub-6 con chipset Qualcomm SDX55, descarga de 2.5 Gbps, formato M.2 para aplicaciones industriales y 5G de próxima generación.",
        "overview": (
            "El EM9190 es el módulo celular 5G NR Sub-6 insignia de Sierra Wireless. Utiliza el chipset Qualcomm SDX55, "
            "soporta modos 5G SA/NSA con velocidades de descarga de hasta 2.5 Gbps (5G) / 2.0 Gbps (LTE Cat 22) "
            "y subida de hasta 900 Mbps (5G).\n\n"
            "Este módulo soporta Categoría 22 LTE (8×CA) con una amplia cobertura de bandas 5G NR Sub-6, incluyendo "
            "n1/2/3/5/7/8/12/20/25/28/38/41/48/66/71/77/78/79. "
            "Utiliza el formato estándar M.2 3042 Key B para una conectividad 5G completa.\n\n"
            "El EM9190 cuenta con gestión avanzada de energía y diseño térmico optimizado, "
            "siendo adecuado para routers industriales de alto rendimiento, CPE, pasarelas empresariales y puntos de acceso móviles 5G."
        ),
        "features": [
            "Chipset de módem 5G Qualcomm SDX55",
            "Soporte de modo dual 5G NR Sub-6 SA/NSA",
            "Descarga 5G hasta 2.5 Gbps, subida 900 Mbps",
            "Descarga LTE Cat 22 hasta 2.0 Gbps",
            "Soporte de agregación de portadoras 8×CA",
            "Formato industrial M.2 3042 Key B",
            "Soporte USB 3.1, PCIe Gen3, RGMII",
            "GNSS multibanda (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "em9191": {
        "title": "EM9191 Módulo Celular 5G NR Sub-6 + mmWave",
        "desc": "El EM9191 es un módulo celular 5G NR Sub-6 + mmWave con chipset Qualcomm SDX55, descarga de 2.5 Gbps, soporte n260/n261 para cobertura 5G completa.",
        "overview": (
            "El EM9191 es el módulo celular 5G NR insignia de Sierra Wireless. Utiliza el chipset Qualcomm SDX55, "
            "soportando tanto Sub-6 como mmWave (n260 39GHz / n261 28GHz) para la cobertura 5G más completa.\n\n"
            "Las velocidades de descarga alcanzan hasta 2.5 Gbps (5G) / 2.0 Gbps (LTE Cat 22) "
            "con subida de hasta 900 Mbps (5G). Soporta 6 interfaces de antena para los requisitos de formación de haz mmWave.\n\n"
            "El EM9191 soporta todas las bandas Sub-6 (igual que el EM9190) más las bandas de alta frecuencia mmWave, "
            "combinado con GNSS multibanda. Ideal para Industria 4.0, salud inteligente "
            "y aplicaciones de edge computing que requieren la menor latencia y el mayor ancho de banda."
        ),
        "features": [
            "Chipset de módem 5G Qualcomm SDX55",
            "Soporte 5G NR Sub-6 + mmWave (n260/n261)",
            "Descarga 5G hasta 2.5 Gbps, subida 900 Mbps",
            "Descarga LTE Cat 22 hasta 2.0 Gbps",
            "Soporte 8×CA y formación de haz mmWave",
            "6 interfaces de antena (incluyendo antenas mmWave)",
            "Formato industrial M.2 3042 Key B",
            "GNSS multibanda (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "mc7304": {
        "title": "MC7304 Módulo Celular LTE-A Cat 4",
        "desc": "El MC7304 es un módulo celular LTE-A Cat 4 con chipset Qualcomm MDM9215, descarga de 150 Mbps, formato Mini PCIe para aplicaciones industriales de presupuesto ajustado.",
        "overview": (
            "El MC7304 es un módulo celular LTE-Advanced Cat 4 de Sierra Wireless. Utiliza el chipset Qualcomm MDM9215 "
            "y soporta velocidades de descarga de hasta 150 Mbps y subida de hasta 50 Mbps.\n\n"
            "Este módulo utiliza el formato estándar Mini PCIe Full Size, compatible con una amplia gama de "
            "placas base industriales y plataformas embebidas existentes. Soporta interfaces USB 2.0, UART y SPI, "
            "ideal para aplicaciones con presupuesto ajustado que requieren conectividad LTE fiable.\n\n"
            "El MC7304 soporta las principales bandas LTE globales y se implementa ampliamente en pasarelas industriales, "
            "máquinas expendedoras, señalización digital y aplicaciones de monitorización remota."
        ),
        "features": [
            "Chipset Qualcomm MDM9215",
            "LTE-A Cat 4 con descarga hasta 150 Mbps",
            "Velocidad de subida hasta 50 Mbps",
            "Formato estándar Mini PCIe Full Size",
            "Soporte de interfaces USB 2.0, UART, SPI",
            "GNSS integrado GPS / GLONASS",
            "Amplio rango de temperatura -40°C ~ +85°C",
            "Fiabilidad probada con amplio soporte de software",
        ],
    },
    "mc7350": {
        "title": "MC7350 Módulo Celular LTE-A Cat 4",
        "desc": "El MC7350 es un módulo celular LTE-A Cat 4 con chipset Qualcomm MDM9215, descarga de 150 Mbps, formato Mini PCIe con amplia certificación global de operadores.",
        "overview": (
            "El MC7350 es un módulo celular LTE-Advanced Cat 4 de Sierra Wireless. Utiliza el chipset Qualcomm MDM9215 "
            "y soporta velocidades de descarga de hasta 150 Mbps y subida de hasta 50 Mbps.\n\n"
            "Este módulo utiliza el formato estándar Mini PCIe Full Size. El MC7350 pertenece a la misma familia que el MC7304 "
            "pero ofrece por defecto un soporte de bandas globales más amplio. Soporta interfaces USB 2.0, UART y SPI.\n\n"
            "El MC7350 está certificado por los principales operadores globales, lo que lo hace adecuado para routers industriales, "
            "seguimiento de activos, contadores inteligentes y dispositivos de telemedicina."
        ),
        "features": [
            "Chipset Qualcomm MDM9215",
            "LTE-A Cat 4 con descarga hasta 150 Mbps",
            "Velocidad de subida hasta 50 Mbps",
            "Formato estándar Mini PCIe Full Size",
            "Soporte de interfaces USB 2.0, UART, SPI",
            "Amplia certificación global de operadores",
            "GNSS integrado GPS / GLONASS",
            "Amplio rango de temperatura -40°C ~ +85°C",
        ],
    },
    "mc7354": {
        "title": "MC7354 Módulo Celular LTE-A Cat 4",
        "desc": "El MC7354 es un módulo celular LTE-A Cat 4 con chipset Qualcomm MDM9215, descarga de 150 Mbps, formato Mini PCIe optimizado para combinaciones de bandas regionales.",
        "overview": (
            "El MC7354 es un módulo celular LTE-Advanced Cat 4 de Sierra Wireless. Utiliza el chipset Qualcomm MDM9215 "
            "y soporta velocidades de descarga de hasta 150 Mbps y subida de hasta 50 Mbps.\n\n"
            "Este módulo utiliza el formato estándar Mini PCIe Full Size. El MC7354 se distingue de otros módulos de la serie MC "
            "por sus combinaciones de bandas específicas, optimizadas para redes de operadores regionales particulares. "
            "Soporta interfaces USB 2.0, UART y SPI.\n\n"
            "El MC7354 es ideal para automatización industrial, transporte, redes inteligentes "
            "y aplicaciones de monitorización de infraestructuras que requieren conectividad LTE fiable."
        ),
        "features": [
            "Chipset Qualcomm MDM9215",
            "LTE-A Cat 4 con descarga hasta 150 Mbps",
            "Velocidad de subida hasta 50 Mbps",
            "Formato estándar Mini PCIe Full Size",
            "Soporte de interfaces USB 2.0, UART, SPI",
            "Optimizado para combinaciones de bandas regionales",
            "GNSS integrado GPS / GLONASS",
            "Amplio rango de temperatura -40°C ~ +85°C",
        ],
    },
    "mc7455": {
        "title": "MC7455 Módulo Celular LTE-A Cat 6",
        "desc": "El MC7455 es un módulo celular LTE-A Cat 6 con chipset Qualcomm MDM9230, descarga de 300 Mbps, formato Mini PCIe para sistemas de comunicación industriales y vehiculares de alto rendimiento.",
        "overview": (
            "El MC7455 es un módulo celular LTE-Advanced Cat 6 de Sierra Wireless. Utiliza el chipset Qualcomm MDM9230 "
            "y soporta agregación de portadoras 2×20 MHz (2×CA) con velocidades de descarga de hasta 300 Mbps y subida de hasta 50 Mbps.\n\n"
            "Este módulo utiliza el formato estándar Mini PCIe Full Size y es el modelo de mayor rendimiento de la serie MC. "
            "Soporta interfaces USB 3.0, UART y SPI para un rápido rendimiento de datos.\n\n"
            "El MC7455 soporta las principales bandas LTE globales, incluyendo FirstNet B14, "
            "y se implementa ampliamente en routers industriales de alto rendimiento, sistemas de comunicación vehicular, "
            "estaciones base de redes privadas y soluciones de conectividad empresarial."
        ),
        "features": [
            "Chipset Qualcomm MDM9230",
            "LTE-A Cat 6 con agregación de portadoras 2×CA",
            "Descarga hasta 300 Mbps, subida hasta 50 Mbps",
            "Formato estándar Mini PCIe Full Size",
            "Soporte de interfaces USB 3.0, UART, SPI",
            "Soporte de banda FirstNet B14",
            "GNSS integrado GPS / GLONASS / BeiDou",
            "Amplio rango de temperatura -40°C ~ +85°C",
        ],
    },
}



# ── Portuguese product content (Brazilian, formal) ─────────────────────

PRODUCT_PT = {
    "em7430": {
        "title": "EM7430 Módulo Celular LTE-A Cat 6",
        "desc": "O EM7430 é um módulo celular LTE-A Cat 6 com chipset Qualcomm MDM9230, download de 300 Mbps, formato M.2, ideal para roteadores industriais e gateways IoT.",
        "overview": (
            "O EM7430 é um módulo celular LTE-Advanced Cat 6 da Sierra Wireless. Utiliza o chipset Qualcomm MDM9230 "
            "e suporta agregação de portadoras 2×20 MHz (2×CA) com velocidades de download de até 300 Mbps e upload de até 50 Mbps.\n\n"
            "Este módulo utiliza o formato padrão M.2 3042 Key B, ideal para roteadores industriais, gateways IoT, hotspots móveis "
            "e aplicações de videovigilância. Suporta interfaces USB 3.0 e PCIe Gen2 para integração flexível do sistema.\n\n"
            "O EM7430 suporta as principais bandas LTE globais (B1–5/7/8/12/13/20/25/26/29/30/41), "
            "sendo adequado para dispositivos IoT e terminais M2M implantados em todo o mundo."
        ),
        "features": [
            "Chipset Qualcomm MDM9230 para confiabilidade comprovada",
            "LTE-A Cat 6 com agregação de portadoras 2×CA",
            "Download até 300 Mbps, upload até 50 Mbps",
            "Formato industrial M.2 3042 Key B",
            "Suporte a interfaces duais USB 3.0 e PCIe Gen2",
            "GNSS integrado GPS / GLONASS / BeiDou",
            "Ampla faixa de temperatura -40°C ~ +85°C",
            "Atualização FOTA de firmware via rádio",
        ],
    },
    "em7455": {
        "title": "EM7455 Módulo Celular LTE-A Cat 6",
        "desc": "O EM7455 é um módulo celular LTE-A Cat 6 com chipset Qualcomm MDM9230, download de 300 Mbps e suporte à banda 14 FirstNet, formato M.2 para segurança pública e roteamento empresarial.",
        "overview": (
            "O EM7455 é um módulo celular LTE-Advanced Cat 6 da Sierra Wireless. Utiliza o chipset Qualcomm MDM9230 "
            "e suporta agregação de portadoras 2×20 MHz (2×CA) com velocidades de download de até 300 Mbps e upload de até 50 Mbps.\n\n"
            "Este módulo utiliza o formato padrão M.2 3042 Key B. Pertence à mesma família do EM7430 mas suporta especificamente "
            "a banda 14 (FirstNet), tornando-o ideal para aplicações de redes de segurança pública dos EUA. Suporta interfaces USB 3.0 e PCIe Gen2.\n\n"
            "O EM7455 suporta as principais bandas LTE globais (B1–5/7/8/12/13/14/20/25/26/29/30/41) "
            "e é amplamente utilizado em roteamento empresarial, veículos conectados e comunicações de segurança pública."
        ),
        "features": [
            "Chipset Qualcomm MDM9230",
            "LTE-A Cat 6 com agregação de portadoras 2×CA",
            "Download até 300 Mbps, upload até 50 Mbps",
            "Suporte à banda 14 FirstNet para segurança pública",
            "Formato industrial M.2 3042 Key B",
            "Suporte a interfaces USB 3.0 e PCIe Gen2",
            "GNSS integrado GPS / GLONASS / BeiDou",
            "Ampla faixa de temperatura -40°C ~ +85°C",
        ],
    },
    "em7511": {
        "title": "EM7511 Módulo Celular LTE-A Pro Cat 12",
        "desc": "O EM7511 é um módulo celular LTE-A Pro Cat 12 com chipset Qualcomm SDX20, download de 600 Mbps, formato M.2 para aplicações empresariais e industriais de alta largura de banda.",
        "overview": (
            "O EM7511 é um módulo celular LTE-Advanced Pro Cat 12 da Sierra Wireless. Utiliza o chipset Qualcomm SDX20 "
            "e suporta agregação de portadoras 3×20 MHz (3×CA) com velocidades de download de até 600 Mbps e upload de até 150 Mbps.\n\n"
            "Este módulo utiliza o formato padrão M.2 3042 Key B com interfaces USB 3.1, PCIe Gen3 e RGMII "
            "para maior largura de banda do sistema. O modem SDX20 oferece menor consumo de energia e desempenho RF superior em comparação com gerações anteriores.\n\n"
            "O EM7511 suporta bandas LTE globais e License-Assisted Access (LAA), ideal "
            "para videovigilância de alta largura de banda, filiais empresariais e aplicações de hotspot móvel."
        ),
        "features": [
            "Chipset de modem Qualcomm SDX20",
            "LTE-A Pro Cat 12 com agregação de portadoras 3×CA",
            "Download até 600 Mbps, upload até 150 Mbps",
            "Suporte 256QAM DL / 64QAM UL",
            "Formato industrial M.2 3042 Key B",
            "Suporte a interfaces USB 3.1, PCIe Gen3, RGMII",
            "GNSS integrado GPS / GLONASS / BeiDou / Galileo",
            "Ampla faixa de temperatura -40°C ~ +85°C",
        ],
    },
    "em7565": {
        "title": "EM7565 Módulo Celular LTE-A Pro Cat 12",
        "desc": "O EM7565 é um módulo celular LTE-A Pro Cat 12 com chipset Qualcomm SDX20, download de 600 Mbps e suporte FirstNet B14, formato M.2 para comunicações críticas.",
        "overview": (
            "O EM7565 é um módulo celular LTE-Advanced Pro Cat 12 da Sierra Wireless. Utiliza o chipset Qualcomm SDX20 "
            "e suporta agregação de portadoras 3×20 MHz (3×CA), DL 256QAM e UL 64QAM com velocidades de download de até 600 Mbps e upload de até 150 Mbps.\n\n"
            "O EM7565 utiliza o formato padrão M.2 3042 Key B e oferece suporte de agregação de portadoras mais amplo que o EM7511. "
            "A plataforma SDX20 proporciona excelente desempenho RF com consumo de energia extremamente baixo, ideal para operação industrial 24/7.\n\n"
            "Suporta as principais bandas LTE globais, incluindo B14 FirstNet e B71 600 MHz, "
            "sendo adequado para roteadores industriais, comunicações críticas e hotspots móveis profissionais."
        ),
        "features": [
            "Chipset de modem Qualcomm SDX20",
            "LTE-A Pro Cat 12 com agregação de portadoras 3×CA",
            "Download até 600 Mbps, upload até 150 Mbps",
            "Suporte 256QAM DL / 64QAM UL / LAA",
            "Formato industrial M.2 3042 Key B",
            "Suporte a interfaces USB 3.1, PCIe Gen3, RGMII",
            "Suporte às bandas FirstNet B14 e B71",
            "GNSS de banda dupla (GPS + Galileo)",
        ],
    },
    "em9190": {
        "title": "EM9190 Módulo Celular 5G NR Sub-6",
        "desc": "O EM9190 é um módulo celular 5G NR Sub-6 com chipset Qualcomm SDX55, download de 2.5 Gbps, formato M.2 para aplicações industriais e 5G de próxima geração.",
        "overview": (
            "O EM9190 é o módulo celular 5G NR Sub-6 flagship da Sierra Wireless. Utiliza o chipset Qualcomm SDX55, "
            "suporta modos 5G SA/NSA com velocidades de download de até 2.5 Gbps (5G) / 2.0 Gbps (LTE Cat 22) "
            "e upload de até 900 Mbps (5G).\n\n"
            "Este módulo suporta Categoria 22 LTE (8×CA) com ampla cobertura de bandas 5G NR Sub-6, incluindo "
            "n1/2/3/5/7/8/12/20/25/28/38/41/48/66/71/77/78/79. "
            "Utiliza o formato padrão M.2 3042 Key B para conectividade 5G completa.\n\n"
            "O EM9190 possui gerenciamento avançado de energia e design térmico otimizado, "
            "sendo adequado para roteadores industriais de alto desempenho, CPE, gateways empresariais e hotspots móveis 5G."
        ),
        "features": [
            "Chipset de modem 5G Qualcomm SDX55",
            "Suporte a modo dual 5G NR Sub-6 SA/NSA",
            "Download 5G até 2.5 Gbps, upload 900 Mbps",
            "Download LTE Cat 22 até 2.0 Gbps",
            "Suporte a agregação de portadoras 8×CA",
            "Formato industrial M.2 3042 Key B",
            "Suporte USB 3.1, PCIe Gen3, RGMII",
            "GNSS multibanda (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "em9191": {
        "title": "EM9191 Módulo Celular 5G NR Sub-6 + mmWave",
        "desc": "O EM9191 é um módulo celular 5G NR Sub-6 + mmWave com chipset Qualcomm SDX55, download de 2.5 Gbps, suporte n260/n261 para cobertura 5G completa.",
        "overview": (
            "O EM9191 é o módulo celular 5G NR flagship da Sierra Wireless. Utiliza o chipset Qualcomm SDX55, "
            "suportando tanto Sub-6 quanto mmWave (n260 39GHz / n261 28GHz) para a cobertura 5G mais completa.\n\n"
            "As velocidades de download alcançam até 2.5 Gbps (5G) / 2.0 Gbps (LTE Cat 22) "
            "com upload de até 900 Mbps (5G). Suporta 6 interfaces de antena para os requisitos de beamforming mmWave.\n\n"
            "O EM9191 suporta todas as bandas Sub-6 (mesmo que o EM9190) mais as bandas de alta frequência mmWave, "
            "combinado com GNSS multibanda. Ideal para Indústria 4.0, saúde inteligente "
            "e aplicações de edge computing que exigem a menor latência e a maior largura de banda."
        ),
        "features": [
            "Chipset de modem 5G Qualcomm SDX55",
            "Suporte 5G NR Sub-6 + mmWave (n260/n261)",
            "Download 5G até 2.5 Gbps, upload 900 Mbps",
            "Download LTE Cat 22 até 2.0 Gbps",
            "Suporte 8×CA e beamforming mmWave",
            "6 interfaces de antena (incluindo antenas mmWave)",
            "Formato industrial M.2 3042 Key B",
            "GNSS multibanda (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "mc7304": {
        "title": "MC7304 Módulo Celular LTE-A Cat 4",
        "desc": "O MC7304 é um módulo celular LTE-A Cat 4 com chipset Qualcomm MDM9215, download de 150 Mbps, formato Mini PCIe para aplicações industriais de orçamento limitado.",
        "overview": (
            "O MC7304 é um módulo celular LTE-Advanced Cat 4 da Sierra Wireless. Utiliza o chipset Qualcomm MDM9215 "
            "e suporta velocidades de download de até 150 Mbps e upload de até 50 Mbps.\n\n"
            "Este módulo utiliza o formato padrão Mini PCIe Full Size, compatível com uma ampla gama de "
            "placas-mãe industriais e plataformas embarcadas existentes. Suporta interfaces USB 2.0, UART e SPI, "
            "ideal para aplicações com orçamento limitado que necessitam de conectividade LTE confiável.\n\n"
            "O MC7304 suporta as principais bandas LTE globais e é amplamente implantado em gateways industriais, "
            "máquinas de venda automática, sinalização digital e aplicações de monitoramento remoto."
        ),
        "features": [
            "Chipset Qualcomm MDM9215",
            "LTE-A Cat 4 com download até 150 Mbps",
            "Velocidade de upload até 50 Mbps",
            "Formato padrão Mini PCIe Full Size",
            "Suporte a interfaces USB 2.0, UART, SPI",
            "GNSS integrado GPS / GLONASS",
            "Ampla faixa de temperatura -40°C ~ +85°C",
            "Confiabilidade comprovada com amplo suporte de software",
        ],
    },
    "mc7350": {
        "title": "MC7350 Módulo Celular LTE-A Cat 4",
        "desc": "O MC7350 é um módulo celular LTE-A Cat 4 com chipset Qualcomm MDM9215, download de 150 Mbps, formato Mini PCIe com ampla certificação global de operadores.",
        "overview": (
            "O MC7350 é um módulo celular LTE-Advanced Cat 4 da Sierra Wireless. Utiliza o chipset Qualcomm MDM9215 "
            "e suporta velocidades de download de até 150 Mbps e upload de até 50 Mbps.\n\n"
            "Este módulo utiliza o formato padrão Mini PCIe Full Size. O MC7350 pertence à mesma família do MC7304 "
            "mas oferece por padrão um suporte de bandas globais mais amplo. Suporta interfaces USB 2.0, UART e SPI.\n\n"
            "O MC7350 é certificado pelos principais operadores globais, sendo adequado para roteadores industriais, "
            "rastreamento de ativos, medidores inteligentes e dispositivos de telemedicina."
        ),
        "features": [
            "Chipset Qualcomm MDM9215",
            "LTE-A Cat 4 com download até 150 Mbps",
            "Velocidade de upload até 50 Mbps",
            "Formato padrão Mini PCIe Full Size",
            "Suporte a interfaces USB 2.0, UART, SPI",
            "Ampla certificação global de operadores",
            "GNSS integrado GPS / GLONASS",
            "Ampla faixa de temperatura -40°C ~ +85°C",
        ],
    },
    "mc7354": {
        "title": "MC7354 Módulo Celular LTE-A Cat 4",
        "desc": "O MC7354 é um módulo celular LTE-A Cat 4 com chipset Qualcomm MDM9215, download de 150 Mbps, formato Mini PCIe otimizado para combinações de bandas regionais.",
        "overview": (
            "O MC7354 é um módulo celular LTE-Advanced Cat 4 da Sierra Wireless. Utiliza o chipset Qualcomm MDM9215 "
            "e suporta velocidades de download de até 150 Mbps e upload de até 50 Mbps.\n\n"
            "Este módulo utiliza o formato padrão Mini PCIe Full Size. O MC7354 se distingue de outros módulos da série MC "
            "por suas combinações de bandas específicas, otimizadas para redes de operadores regionais. "
            "Suporta interfaces USB 2.0, UART e SPI.\n\n"
            "O MC7354 é ideal para automação industrial, transporte, redes inteligentes "
            "e aplicações de monitoramento de infraestrutura que exigem conectividade LTE confiável."
        ),
        "features": [
            "Chipset Qualcomm MDM9215",
            "LTE-A Cat 4 com download até 150 Mbps",
            "Velocidade de upload até 50 Mbps",
            "Formato padrão Mini PCIe Full Size",
            "Suporte a interfaces USB 2.0, UART, SPI",
            "Otimizado para combinações de bandas regionais",
            "GNSS integrado GPS / GLONASS",
            "Ampla faixa de temperatura -40°C ~ +85°C",
        ],
    },
    "mc7455": {
        "title": "MC7455 Módulo Celular LTE-A Cat 6",
        "desc": "O MC7455 é um módulo celular LTE-A Cat 6 com chipset Qualcomm MDM9230, download de 300 Mbps, formato Mini PCIe para sistemas de comunicação industriais e veiculares de alto desempenho.",
        "overview": (
            "O MC7455 é um módulo celular LTE-Advanced Cat 6 da Sierra Wireless. Utiliza o chipset Qualcomm MDM9230 "
            "e suporta agregação de portadoras 2×20 MHz (2×CA) com velocidades de download de até 300 Mbps e upload de até 50 Mbps.\n\n"
            "Este módulo utiliza o formato padrão Mini PCIe Full Size e é o modelo de maior desempenho da série MC. "
            "Suporta interfaces USB 3.0, UART e SPI para rápida transferência de dados.\n\n"
            "O MC7455 suporta as principais bandas LTE globais, incluindo FirstNet B14, "
            "e é amplamente implantado em roteadores industriais de alto desempenho, sistemas de comunicação veicular, "
            "estações base de redes privadas e soluções de conectividade empresarial."
        ),
        "features": [
            "Chipset Qualcomm MDM9230",
            "LTE-A Cat 6 com agregação de portadoras 2×CA",
            "Download até 300 Mbps, upload até 50 Mbps",
            "Formato padrão Mini PCIe Full Size",
            "Suporte a interfaces USB 3.0, UART, SPI",
            "Suporte à banda FirstNet B14",
            "GNSS integrado GPS / GLONASS / BeiDou",
            "Ampla faixa de temperatura -40°C ~ +85°C",
        ],
    },
}



# ── Arabic product content (formal, professional) ────────────────────

PRODUCT_AR = {
    "em7430": {
        "title": "EM7430 وحدة خلوية LTE-A Cat 6",
        "desc": "EM7430 هي وحدة خلوية LTE-A Cat 6 مع مجموعة شرائح Qualcomm MDM9230، تحميل بسرعة 300 ميجابت/ثانية، بعامل شكل M.2، مثالية لأجهزة التوجيه الصناعية وبوابات إنترنت الأشياء.",
        "overview": (
            "EM7430 هي وحدة خلوية LTE-Advanced Cat 6 من Sierra Wireless. تستخدم مجموعة شرائح Qualcomm MDM9230 "
            "وتدعم تجميع الموجات الحاملة 2×20 ميجاهرتز (2×CA) بسرعات تحميل تصل إلى 300 ميجابت/ثانية ورفع يصل إلى 50 ميجابت/ثانية.\n\n"
            "تستخدم هذه الوحدة عامل الشكل القياسي M.2 3042 Key B، وهي مثالية لأجهزة التوجيه الصناعية وبوابات إنترنت الأشياء ونقاط الاتصال المتنقلة "
            "وتطبيقات المراقبة بالفيديو. تدعم واجهات USB 3.0 و PCIe Gen2 لتكامل مرن مع الأنظمة.\n\n"
            "تدعم EM7430 نطاقات LTE العالمية الرئيسية (B1–5/7/8/12/13/20/25/26/29/30/41)، "
            "مما يجعلها مناسبة لأجهزة إنترنت الأشياء ومحطات M2M المنتشرة في جميع أنحاء العالم."
        ),
        "features": [
            "مجموعة شرائح Qualcomm MDM9230 للموثوقية المثبتة",
            "LTE-A Cat 6 مع تجميع الموجات الحاملة 2×CA",
            "تحميل حتى 300 ميجابت/ثانية، رفع حتى 50 ميجابت/ثانية",
            "عامل شكل صناعي M.2 3042 Key B",
            "دعم واجهات مزدوجة USB 3.0 و PCIe Gen2",
            "نظام GNSS مدمج GPS / GLONASS / BeiDou",
            "نطاق درجة حرارة واسع -40°C ~ +85°C",
            "تحديث البرامج الثابتة FOTA عبر الأثير",
        ],
    },
    "em7455": {
        "title": "EM7455 وحدة خلوية LTE-A Cat 6",
        "desc": "EM7455 هي وحدة خلوية LTE-A Cat 6 مع مجموعة شرائح Qualcomm MDM9230، تحميل بسرعة 300 ميجابت/ثانية ودعم النطاق 14 FirstNet، بعامل شكل M.2 للسلامة العامة والتوجيه المؤسسي.",
        "overview": (
            "EM7455 هي وحدة خلوية LTE-Advanced Cat 6 من Sierra Wireless. تستخدم مجموعة شرائح Qualcomm MDM9230 "
            "وتدعم تجميع الموجات الحاملة 2×20 ميجاهرتز (2×CA) بسرعات تحميل تصل إلى 300 ميجابت/ثانية ورفع يصل إلى 50 ميجابت/ثانية.\n\n"
            "تستخدم هذه الوحدة عامل الشكل القياسي M.2 3042 Key B. وهي تنتمي إلى نفس عائلة EM7430 ولكنها تدعم بشكل خاص "
            "النطاق 14 (FirstNet)، مما يجعلها مثالية لتطبيقات شبكات السلامة العامة الأمريكية. تدعم واجهات USB 3.0 و PCIe Gen2.\n\n"
            "تدعم EM7455 نطاقات LTE العالمية الرئيسية (B1–5/7/8/12/13/14/20/25/26/29/30/41) "
            "وتستخدم على نطاق واسع في التوجيه المؤسسي والمركبات المتصلة واتصالات السلامة العامة."
        ),
        "features": [
            "مجموعة شرائح Qualcomm MDM9230",
            "LTE-A Cat 6 مع تجميع الموجات الحاملة 2×CA",
            "تحميل حتى 300 ميجابت/ثانية، رفع حتى 50 ميجابت/ثانية",
            "دعم النطاق 14 FirstNet للسلامة العامة",
            "عامل شكل صناعي M.2 3042 Key B",
            "دعم واجهات USB 3.0 و PCIe Gen2",
            "نظام GNSS مدمج GPS / GLONASS / BeiDou",
            "نطاق درجة حرارة واسع -40°C ~ +85°C",
        ],
    },
    "em7511": {
        "title": "EM7511 وحدة خلوية LTE-A Pro Cat 12",
        "desc": "EM7511 هي وحدة خلوية LTE-A Pro Cat 12 مع مجموعة شرائح Qualcomm SDX20، تحميل بسرعة 600 ميجابت/ثانية، بعامل شكل M.2 للتطبيقات الصناعية والمؤسسية عالية النطاق الترددي.",
        "overview": (
            "EM7511 هي وحدة خلوية LTE-Advanced Pro Cat 12 من Sierra Wireless. تستخدم مجموعة شرائح Qualcomm SDX20 "
            "وتدعم تجميع الموجات الحاملة 3×20 ميجاهرتز (3×CA) بسرعات تحميل تصل إلى 600 ميجابت/ثانية ورفع يصل إلى 150 ميجابت/ثانية.\n\n"
            "تستخدم هذه الوحدة عامل الشكل القياسي M.2 3042 Key B مع واجهات USB 3.1 و PCIe Gen3 و RGMII "
            "لزيادة النطاق الترددي للنظام. يوفر مودم SDX20 استهلاك طاقة أقل وأداء RF متفوق مقارنة بالأجيال السابقة.\n\n"
            "تدعم EM7511 نطاقات LTE العالمية و License-Assisted Access (LAA)، وهي مثالية "
            "لمراقبة الفيديو عالية النطاق الترددي والفروع المؤسسية وتطبيقات نقاط الاتصال المتنقلة."
        ),
        "features": [
            "مجموعة شرائح مودم Qualcomm SDX20",
            "LTE-A Pro Cat 12 مع تجميع الموجات الحاملة 3×CA",
            "تحميل حتى 600 ميجابت/ثانية، رفع حتى 150 ميجابت/ثانية",
            "دعم 256QAM DL / 64QAM UL",
            "عامل شكل صناعي M.2 3042 Key B",
            "دعم واجهات USB 3.1 و PCIe Gen3 و RGMII",
            "نظام GNSS مدمج GPS / GLONASS / BeiDou / Galileo",
            "نطاق درجة حرارة واسع -40°C ~ +85°C",
        ],
    },
    "em7565": {
        "title": "EM7565 وحدة خلوية LTE-A Pro Cat 12",
        "desc": "EM7565 هي وحدة خلوية LTE-A Pro Cat 12 مع مجموعة شرائح Qualcomm SDX20، تحميل بسرعة 600 ميجابت/ثانية ودعم FirstNet B14، بعامل شكل M.2 للاتصالات الحرجة.",
        "overview": (
            "EM7565 هي وحدة خلوية LTE-Advanced Pro Cat 12 من Sierra Wireless. تستخدم مجموعة شرائح Qualcomm SDX20 "
            "وتدعم تجميع الموجات الحاملة 3×20 ميجاهرتز (3×CA) و DL 256QAM و UL 64QAM بسرعات تحميل تصل إلى 600 ميجابت/ثانية ورفع يصل إلى 150 ميجابت/ثانية.\n\n"
            "تستخدم EM7565 عامل الشكل القياسي M.2 3042 Key B وتقدم دعماً أوسع لتجميع الموجات الحاملة مقارنة بـ EM7511. "
            "توفر منصة SDX20 أداء RF استثنائياً مع استهلاك طاقة منخفض للغاية، مثالية للتشغيل الصناعي على مدار الساعة.\n\n"
            "تدعم نطاقات LTE العالمية الرئيسية بما في ذلك B14 FirstNet و B71 600 ميجاهرتز، "
            "وهي مناسبة لأجهزة التوجيه الصناعية والاتصالات الحرجة ونقاط الاتصال المتنقلة المهنية."
        ),
        "features": [
            "مجموعة شرائح مودم Qualcomm SDX20",
            "LTE-A Pro Cat 12 مع تجميع الموجات الحاملة 3×CA",
            "تحميل حتى 600 ميجابت/ثانية، رفع حتى 150 ميجابت/ثانية",
            "دعم 256QAM DL / 64QAM UL / LAA",
            "عامل شكل صناعي M.2 3042 Key B",
            "دعم واجهات USB 3.1 و PCIe Gen3 و RGMII",
            "دعم نطاقات FirstNet B14 و B71",
            "نظام GNSS مزدوج النطاق (GPS + Galileo)",
        ],
    },
    "em9190": {
        "title": "EM9190 وحدة خلوية 5G NR Sub-6",
        "desc": "EM9190 هي وحدة خلوية 5G NR Sub-6 مع مجموعة شرائح Qualcomm SDX55، تحميل بسرعة 2.5 جيجابت/ثانية، بعامل شكل M.2 للتطبيقات الصناعية والجيل التالي من 5G.",
        "overview": (
            "EM9190 هي الوحدة الخلوية الرائدة 5G NR Sub-6 من Sierra Wireless. تستخدم مجموعة شرائح Qualcomm SDX55، "
            "وتدعم أوضاع 5G SA/NSA بسرعات تحميل تصل إلى 2.5 جيجابت/ثانية (5G) / 2.0 جيجابت/ثانية (LTE Cat 22) "
            "ورفع يصل إلى 900 ميجابت/ثانية (5G).\n\n"
            "تدعم هذه الوحدة الفئة 22 LTE (8×CA) مع تغطية واسعة لنطاقات 5G NR Sub-6 بما في ذلك "
            "n1/2/3/5/7/8/12/20/25/28/38/41/48/66/71/77/78/79. "
            "تستخدم عامل الشكل القياسي M.2 3042 Key B لاتصال 5G كامل.\n\n"
            "تم تجهيز EM9190 بإدارة متقدمة للطاقة وتصميم حراري محسّن، "
            "وهي مناسبة لأجهزة التوجيه الصناعية عالية الأداء ومعدات CPE وبوابات المؤسسات ونقاط الاتصال المتنقلة 5G."
        ),
        "features": [
            "مجموعة شرائح مودم 5G Qualcomm SDX55",
            "دعم الوضع المزدوج 5G NR Sub-6 SA/NSA",
            "تحميل 5G حتى 2.5 جيجابت/ثانية، رفع 900 ميجابت/ثانية",
            "تحميل LTE Cat 22 حتى 2.0 جيجابت/ثانية",
            "دعم تجميع الموجات الحاملة 8×CA",
            "عامل شكل صناعي M.2 3042 Key B",
            "دعم USB 3.1 و PCIe Gen3 و RGMII",
            "نظام GNSS متعدد النطاقات (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "em9191": {
        "title": "EM9191 وحدة خلوية 5G NR Sub-6 + mmWave",
        "desc": "EM9191 هي وحدة خلوية 5G NR Sub-6 + mmWave مع مجموعة شرائح Qualcomm SDX55، تحميل بسرعة 2.5 جيجابت/ثانية، دعم n260/n261 لتغطية 5G شاملة.",
        "overview": (
            "EM9191 هي الوحدة الخلوية 5G NR الرائدة من Sierra Wireless. تستخدم مجموعة شرائح Qualcomm SDX55، "
            "وتدعم كلاً من Sub-6 و mmWave (n260 39GHz / n261 28GHz) لأكثر تغطية 5G شمولاً.\n\n"
            "تصل سرعات التحميل إلى 2.5 جيجابت/ثانية (5G) / 2.0 جيجابت/ثانية (LTE Cat 22) "
            "مع رفع يصل إلى 900 ميجابت/ثانية (5G). تدعم 6 واجهات هوائي لمتطلبات تشكيل حزمة mmWave.\n\n"
            "تدعم EM9191 جميع نطاقات Sub-6 (مثل EM9190) بالإضافة إلى نطاقات mmWave عالية التردد، "
            "مقترنة بنظام GNSS متعدد النطاقات. مثالية للصناعة 4.0 والرعاية الصحية الذكية "
            "وتطبيقات الحوسبة الطرفية التي تتطلب أقل زمن وصول وأعلى نطاق ترددي."
        ),
        "features": [
            "مجموعة شرائح مودم 5G Qualcomm SDX55",
            "دعم 5G NR Sub-6 + mmWave (n260/n261)",
            "تحميل 5G حتى 2.5 جيجابت/ثانية، رفع 900 ميجابت/ثانية",
            "تحميل LTE Cat 22 حتى 2.0 جيجابت/ثانية",
            "دعم 8×CA وتشكيل حزمة mmWave",
            "6 واجهات هوائي (بما في ذلك هوائيات mmWave)",
            "عامل شكل صناعي M.2 3042 Key B",
            "نظام GNSS متعدد النطاقات (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "mc7304": {
        "title": "MC7304 وحدة خلوية LTE-A Cat 4",
        "desc": "MC7304 هي وحدة خلوية LTE-A Cat 4 مع مجموعة شرائح Qualcomm MDM9215، تحميل بسرعة 150 ميجابت/ثانية، بعامل شكل Mini PCIe للتطبيقات الصناعية محدودة الميزانية.",
        "overview": (
            "MC7304 هي وحدة خلوية LTE-Advanced Cat 4 من Sierra Wireless. تستخدم مجموعة شرائح Qualcomm MDM9215 "
            "وتدعم سرعات تحميل تصل إلى 150 ميجابت/ثانية ورفع يصل إلى 50 ميجابت/ثانية.\n\n"
            "تستخدم هذه الوحدة عامل الشكل القياسي Mini PCIe Full Size، المتوافقة مع مجموعة واسعة من "
            "اللوحات الأم الصناعية والمنصات المدمجة الحالية. تدعم واجهات USB 2.0 و UART و SPI، "
            "وهي مثالية للتطبيقات محدودة الميزانية التي تتطلب اتصال LTE موثوقاً.\n\n"
            "تدعم MC7304 نطاقات LTE العالمية الرئيسية ويتم نشرها على نطاق واسع في البوابات الصناعية "
            "وآلات البيع واللافتات الرقمية وتطبيقات المراقبة عن بعد."
        ),
        "features": [
            "مجموعة شرائح Qualcomm MDM9215",
            "LTE-A Cat 4 مع تحميل حتى 150 ميجابت/ثانية",
            "سرعة رفع حتى 50 ميجابت/ثانية",
            "عامل شكل قياسي Mini PCIe Full Size",
            "دعم واجهات USB 2.0 و UART و SPI",
            "نظام GNSS مدمج GPS / GLONASS",
            "نطاق درجة حرارة واسع -40°C ~ +85°C",
            "موثوقية مثبتة مع دعم برمجي واسع",
        ],
    },
    "mc7350": {
        "title": "MC7350 وحدة خلوية LTE-A Cat 4",
        "desc": "MC7350 هي وحدة خلوية LTE-A Cat 4 مع مجموعة شرائح Qualcomm MDM9215، تحميل بسرعة 150 ميجابت/ثانية، بعامل شكل Mini PCIe مع شهادة عالمية واسعة من المشغلين.",
        "overview": (
            "MC7350 هي وحدة خلوية LTE-Advanced Cat 4 من Sierra Wireless. تستخدم مجموعة شرائح Qualcomm MDM9215 "
            "وتدعم سرعات تحميل تصل إلى 150 ميجابت/ثانية ورفع يصل إلى 50 ميجابت/ثانية.\n\n"
            "تستخدم هذه الوحدة عامل الشكل القياسي Mini PCIe Full Size. تنتمي MC7350 إلى نفس عائلة MC7304 "
            "ولكنها توفر دعماً أوسع للنطاقات العالمية بشكل افتراضي. تدعم واجهات USB 2.0 و UART و SPI.\n\n"
            "حصلت MC7350 على شهادة من كبار المشغلين العالميين، مما يجعلها مناسبة لأجهزة التوجيه الصناعية "
            "وتتبع الأصول والعدادات الذكية وأجهزة الرعاية الصحية عن بعد."
        ),
        "features": [
            "مجموعة شرائح Qualcomm MDM9215",
            "LTE-A Cat 4 مع تحميل حتى 150 ميجابت/ثانية",
            "سرعة رفع حتى 50 ميجابت/ثانية",
            "عامل شكل قياسي Mini PCIe Full Size",
            "دعم واجهات USB 2.0 و UART و SPI",
            "شهادة عالمية واسعة من المشغلين",
            "نظام GNSS مدمج GPS / GLONASS",
            "نطاق درجة حرارة واسع -40°C ~ +85°C",
        ],
    },
    "mc7354": {
        "title": "MC7354 وحدة خلوية LTE-A Cat 4",
        "desc": "MC7354 هي وحدة خلوية LTE-A Cat 4 مع مجموعة شرائح Qualcomm MDM9215، تحميل بسرعة 150 ميجابت/ثانية، بعامل شكل Mini PCIe محسّن لمجموعات النطاقات الإقليمية.",
        "overview": (
            "MC7354 هي وحدة خلوية LTE-Advanced Cat 4 من Sierra Wireless. تستخدم مجموعة شرائح Qualcomm MDM9215 "
            "وتدعم سرعات تحميل تصل إلى 150 ميجابت/ثانية ورفع يصل إلى 50 ميجابت/ثانية.\n\n"
            "تستخدم هذه الوحدة عامل الشكل القياسي Mini PCIe Full Size. تتميز MC7354 عن وحدات سلسلة MC الأخرى "
            "بمجموعات النطاقات المحددة المحسّنة لشبكات مشغلين إقليميين معينين. "
            "تدعم واجهات USB 2.0 و UART و SPI.\n\n"
            "MC7354 مثالية للأتمتة الصناعية والنقل والشبكات الذكية "
            "وتطبيقات مراقبة البنية التحتية التي تتطلب اتصال LTE موثوقاً."
        ),
        "features": [
            "مجموعة شرائح Qualcomm MDM9215",
            "LTE-A Cat 4 مع تحميل حتى 150 ميجابت/ثانية",
            "سرعة رفع حتى 50 ميجابت/ثانية",
            "عامل شكل قياسي Mini PCIe Full Size",
            "دعم واجهات USB 2.0 و UART و SPI",
            "محسّن لمجموعات النطاقات الإقليمية",
            "نظام GNSS مدمج GPS / GLONASS",
            "نطاق درجة حرارة واسع -40°C ~ +85°C",
        ],
    },
    "mc7455": {
        "title": "MC7455 وحدة خلوية LTE-A Cat 6",
        "desc": "MC7455 هي وحدة خلوية LTE-A Cat 6 مع مجموعة شرائح Qualcomm MDM9230، تحميل بسرعة 300 ميجابت/ثانية، بعامل شكل Mini PCIe لأنظمة الاتصالات الصناعية والمركبات عالية الأداء.",
        "overview": (
            "MC7455 هي وحدة خلوية LTE-Advanced Cat 6 من Sierra Wireless. تستخدم مجموعة شرائح Qualcomm MDM9230 "
            "وتدعم تجميع الموجات الحاملة 2×20 ميجاهرتز (2×CA) بسرعات تحميل تصل إلى 300 ميجابت/ثانية ورفع يصل إلى 50 ميجابت/ثانية.\n\n"
            "تستخدم هذه الوحدة عامل الشكل القياسي Mini PCIe Full Size وهي الطراز الأعلى أداءً في سلسلة MC. "
            "تدعم واجهات USB 3.0 و UART و SPI لنقل البيانات بسرعة.\n\n"
            "تدعم MC7455 نطاقات LTE العالمية الرئيسية بما في ذلك FirstNet B14، "
            "ويتم نشرها على نطاق واسع في أجهزة التوجيه الصناعية عالية الأداء وأنظمة اتصالات المركبات "
            "ومحطات القاعدة للشبكات الخاصة وحلول الاتصال المؤسسي."
        ),
        "features": [
            "مجموعة شرائح Qualcomm MDM9230",
            "LTE-A Cat 6 مع تجميع الموجات الحاملة 2×CA",
            "تحميل حتى 300 ميجابت/ثانية، رفع حتى 50 ميجابت/ثانية",
            "عامل شكل قياسي Mini PCIe Full Size",
            "دعم واجهات USB 3.0 و UART و SPI",
            "دعم النطاق FirstNet B14",
            "نظام GNSS مدمج GPS / GLONASS / BeiDou",
            "نطاق درجة حرارة واسع -40°C ~ +85°C",
        ],
    },
}



# ── Russian product content (formal, professional) ────────────────────

PRODUCT_RU = {
    "em7430": {
        "title": "EM7430 Сотовый модуль LTE-A Cat 6",
        "desc": "EM7430 — сотовый модуль LTE-A Cat 6 на чипсете Qualcomm MDM9230, скорость загрузки до 300 Мбит/с, форм-фактор M.2, идеально подходит для промышленных маршрутизаторов и шлюзов IoT.",
        "overview": (
            "EM7430 — это сотовый модуль LTE-Advanced Cat 6 от Sierra Wireless на чипсете Qualcomm MDM9230, "
            "поддерживающий агрегацию несущих 2×20 МГц (2×CA) со скоростью загрузки до 300 Мбит/с и выгрузки до 50 Мбит/с.\n\n"
            "Модуль выполнен в стандартном форм-факторе M.2 3042 Key B, что идеально для промышленных маршрутизаторов, шлюзов IoT, мобильных точек доступа "
            "и систем видеонаблюдения. Поддерживает интерфейсы USB 3.0 и PCIe Gen2 для гибкой интеграции.\n\n"
            "EM7430 поддерживает основные глобальные диапазоны LTE (B1–5/7/8/12/13/20/25/26/29/30/41), "
            "что делает его пригодным для устройств IoT и терминалов M2M, развернутых по всему миру."
        ),
        "features": [
            "Чипсет Qualcomm MDM9230 для проверенной надежности",
            "LTE-A Cat 6 с агрегацией несущих 2×CA",
            "Загрузка до 300 Мбит/с, выгрузка до 50 Мбит/с",
            "Промышленный форм-фактор M.2 3042 Key B",
            "Поддержка двух интерфейсов USB 3.0 и PCIe Gen2",
            "Встроенная GNSS GPS / GLONASS / BeiDou",
            "Широкий температурный диапазон -40°C ~ +85°C",
            "Обновление прошивки FOTA по воздуху",
        ],
    },
    "em7455": {
        "title": "EM7455 Сотовый модуль LTE-A Cat 6",
        "desc": "EM7455 — сотовый модуль LTE-A Cat 6 на чипсете Qualcomm MDM9230, скорость загрузки до 300 Мбит/с и поддержка диапазона 14 FirstNet, форм-фактор M.2 для общественной безопасности и корпоративной маршрутизации.",
        "overview": (
            "EM7455 — это сотовый модуль LTE-Advanced Cat 6 от Sierra Wireless на чипсете Qualcomm MDM9230, "
            "поддерживающий агрегацию несущих 2×20 МГц (2×CA) со скоростью загрузки до 300 Мбит/с и выгрузки до 50 Мбит/с.\n\n"
            "Модуль выполнен в стандартном форм-факторе M.2 3042 Key B. Он относится к тому же семейству, что и EM7430, но специально поддерживает "
            "диапазон 14 (FirstNet), что делает его идеальным для сетей общественной безопасности США. Поддерживает интерфейсы USB 3.0 и PCIe Gen2.\n\n"
            "EM7455 поддерживает основные глобальные диапазоны LTE (B1–5/7/8/12/13/14/20/25/26/29/30/41) "
            "и широко используется в корпоративной маршрутизации, подключенных транспортных средствах и системах связи общественной безопасности."
        ),
        "features": [
            "Чипсет Qualcomm MDM9230",
            "LTE-A Cat 6 с агрегацией несущих 2×CA",
            "Загрузка до 300 Мбит/с, выгрузка до 50 Мбит/с",
            "Поддержка диапазона 14 FirstNet для общественной безопасности",
            "Промышленный форм-фактор M.2 3042 Key B",
            "Поддержка интерфейсов USB 3.0 и PCIe Gen2",
            "Встроенная GNSS GPS / GLONASS / BeiDou",
            "Широкий температурный диапазон -40°C ~ +85°C",
        ],
    },
    "em7511": {
        "title": "EM7511 Сотовый модуль LTE-A Pro Cat 12",
        "desc": "EM7511 — сотовый модуль LTE-A Pro Cat 12 на чипсете Qualcomm SDX20, скорость загрузки до 600 Мбит/с, форм-фактор M.2 для корпоративных и промышленных приложений с высокой пропускной способностью.",
        "overview": (
            "EM7511 — это сотовый модуль LTE-Advanced Pro Cat 12 от Sierra Wireless на чипсете Qualcomm SDX20, "
            "поддерживающий агрегацию несущих 3×20 МГц (3×CA) со скоростью загрузки до 600 Мбит/с и выгрузки до 150 Мбит/с.\n\n"
            "Модуль выполнен в стандартном форм-факторе M.2 3042 Key B с интерфейсами USB 3.1, PCIe Gen3 и RGMII "
            "для более высокой пропускной способности системы. Модем SDX20 обеспечивает меньшее энергопотребление и превосходную производительность RF по сравнению с предыдущими поколениями.\n\n"
            "EM7511 поддерживает глобальные диапазоны LTE и License-Assisted Access (LAA), идеально "
            "для видеонаблюдения с высокой пропускной способностью, корпоративных филиалов и мобильных точек доступа."
        ),
        "features": [
            "Чипсет модема Qualcomm SDX20",
            "LTE-A Pro Cat 12 с агрегацией несущих 3×CA",
            "Загрузка до 600 Мбит/с, выгрузка до 150 Мбит/с",
            "Поддержка 256QAM DL / 64QAM UL",
            "Промышленный форм-фактор M.2 3042 Key B",
            "Поддержка интерфейсов USB 3.1, PCIe Gen3, RGMII",
            "Встроенная GNSS GPS / GLONASS / BeiDou / Galileo",
            "Широкий температурный диапазон -40°C ~ +85°C",
        ],
    },
    "em7565": {
        "title": "EM7565 Сотовый модуль LTE-A Pro Cat 12",
        "desc": "EM7565 — сотовый модуль LTE-A Pro Cat 12 на чипсете Qualcomm SDX20, скорость загрузки до 600 Мбит/с и поддержка FirstNet B14, форм-фактор M.2 для ответственных коммуникаций.",
        "overview": (
            "EM7565 — это сотовый модуль LTE-Advanced Pro Cat 12 от Sierra Wireless на чипсете Qualcomm SDX20, "
            "поддерживающий агрегацию несущих 3×20 МГц (3×CA), DL 256QAM и UL 64QAM со скоростью загрузки до 600 Мбит/с и выгрузки до 150 Мбит/с.\n\n"
            "EM7565 выполнен в стандартном форм-факторе M.2 3042 Key B и предлагает более широкую поддержку агрегации несущих по сравнению с EM7511. "
            "Платформа SDX20 обеспечивает исключительную производительность RF при чрезвычайно низком энергопотреблении, идеально для круглосуточной промышленной эксплуатации.\n\n"
            "Поддерживает основные глобальные диапазоны LTE, включая B14 FirstNet и B71 600 МГц, "
            "подходит для промышленных маршрутизаторов, ответственных коммуникаций и профессиональных мобильных точек доступа."
        ),
        "features": [
            "Чипсет модема Qualcomm SDX20",
            "LTE-A Pro Cat 12 с агрегацией несущих 3×CA",
            "Загрузка до 600 Мбит/с, выгрузка до 150 Мбит/с",
            "Поддержка 256QAM DL / 64QAM UL / LAA",
            "Промышленный форм-фактор M.2 3042 Key B",
            "Поддержка интерфейсов USB 3.1, PCIe Gen3, RGMII",
            "Поддержка диапазонов FirstNet B14 и B71",
            "Двухдиапазонная GNSS (GPS + Galileo)",
        ],
    },
    "em9190": {
        "title": "EM9190 Сотовый модуль 5G NR Sub-6",
        "desc": "EM9190 — флагманский сотовый модуль 5G NR Sub-6 на чипсете Qualcomm SDX55, скорость загрузки до 2.5 Гбит/с, форм-фактор M.2 для промышленных приложений и 5G следующего поколения.",
        "overview": (
            "EM9190 — это флагманский сотовый модуль 5G NR Sub-6 от Sierra Wireless на чипсете Qualcomm SDX55, "
            "поддерживающий режимы 5G SA/NSA со скоростью загрузки до 2.5 Гбит/с (5G) / 2.0 Гбит/с (LTE Cat 22) "
            "и выгрузки до 900 Мбит/с (5G).\n\n"
            "Модуль поддерживает категорию 22 LTE (8×CA) с обширным покрытием диапазонов 5G NR Sub-6, включая "
            "n1/2/3/5/7/8/12/20/25/28/38/41/48/66/71/77/78/79. "
            "Использует стандартный форм-фактор M.2 3042 Key B для полной связи 5G.\n\n"
            "EM9190 оснащен передовым управлением питанием и оптимизированной термоконструкцией, "
            "подходит для высокопроизводительных промышленных маршрутизаторов, CPE, корпоративных шлюзов и мобильных точек доступа 5G."
        ),
        "features": [
            "Чипсет 5G модема Qualcomm SDX55",
            "Поддержка двойного режима 5G NR Sub-6 SA/NSA",
            "Загрузка 5G до 2.5 Гбит/с, выгрузка 900 Мбит/с",
            "Загрузка LTE Cat 22 до 2.0 Гбит/с",
            "Поддержка агрегации несущих 8×CA",
            "Промышленный форм-фактор M.2 3042 Key B",
            "Поддержка USB 3.1, PCIe Gen3, RGMII",
            "Многодиапазонная GNSS (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "em9191": {
        "title": "EM9191 Сотовый модуль 5G NR Sub-6 + mmWave",
        "desc": "EM9191 — сотовый модуль 5G NR Sub-6 + mmWave на чипсете Qualcomm SDX55, скорость загрузки до 2.5 Гбит/с, поддержка n260/n261 для полного покрытия 5G.",
        "overview": (
            "EM9191 — это флагманский сотовый модуль 5G NR от Sierra Wireless на чипсете Qualcomm SDX55, "
            "поддерживающий как Sub-6, так и mmWave (n260 39 ГГц / n261 28 ГГц) для наиболее полного покрытия 5G.\n\n"
            "Скорости загрузки достигают 2.5 Гбит/с (5G) / 2.0 Гбит/с (LTE Cat 22) "
            "с выгрузкой до 900 Мбит/с (5G). Поддерживает 6 антенных интерфейсов для лучеформирования mmWave.\n\n"
            "EM9191 поддерживает все диапазоны Sub-6 (как EM9190) плюс высокочастотные диапазоны mmWave, "
            "в сочетании с многодиапазонной GNSS. Идеален для Индустрии 4.0, умного здравоохранения "
            "и приложений периферийных вычислений, требующих минимальной задержки и максимальной пропускной способности."
        ),
        "features": [
            "Чипсет 5G модема Qualcomm SDX55",
            "Поддержка 5G NR Sub-6 + mmWave (n260/n261)",
            "Загрузка 5G до 2.5 Гбит/с, выгрузка 900 Мбит/с",
            "Загрузка LTE Cat 22 до 2.0 Гбит/с",
            "Поддержка 8×CA и лучеформирования mmWave",
            "6 антенных интерфейсов (включая антенны mmWave)",
            "Промышленный форм-фактор M.2 3042 Key B",
            "Многодиапазонная GNSS (GPS + GLONASS + BeiDou + Galileo + QZSS)",
        ],
    },
    "mc7304": {
        "title": "MC7304 Сотовый модуль LTE-A Cat 4",
        "desc": "MC7304 — сотовый модуль LTE-A Cat 4 на чипсете Qualcomm MDM9215, скорость загрузки до 150 Мбит/с, форм-фактор Mini PCIe для бюджетных промышленных приложений.",
        "overview": (
            "MC7304 — это сотовый модуль LTE-Advanced Cat 4 от Sierra Wireless на чипсете Qualcomm MDM9215, "
            "поддерживающий скорость загрузки до 150 Мбит/с и выгрузки до 50 Мбит/с.\n\n"
            "Модуль выполнен в стандартном форм-факторе Mini PCIe Full Size, совместим с широким спектром "
            "существующих промышленных материнских плат и встраиваемых платформ. Поддерживает интерфейсы USB 2.0, UART и SPI, "
            "идеален для бюджетных приложений, требующих надежного LTE-соединения.\n\n"
            "MC7304 поддерживает основные глобальные диапазоны LTE и широко применяется в промышленных шлюзах, "
            "торговых автоматах, цифровых вывесках и системах удаленного мониторинга."
        ),
        "features": [
            "Чипсет Qualcomm MDM9215",
            "LTE-A Cat 4 с загрузкой до 150 Мбит/с",
            "Скорость выгрузки до 50 Мбит/с",
            "Стандартный форм-фактор Mini PCIe Full Size",
            "Поддержка интерфейсов USB 2.0, UART, SPI",
            "Встроенная GNSS GPS / GLONASS",
            "Широкий температурный диапазон -40°C ~ +85°C",
            "Проверенная надежность с широкой программной поддержкой",
        ],
    },
    "mc7350": {
        "title": "MC7350 Сотовый модуль LTE-A Cat 4",
        "desc": "MC7350 — сотовый модуль LTE-A Cat 4 на чипсете Qualcomm MDM9215, скорость загрузки до 150 Мбит/с, форм-фактор Mini PCIe с широкой глобальной сертификацией операторов.",
        "overview": (
            "MC7350 — это сотовый модуль LTE-Advanced Cat 4 от Sierra Wireless на чипсете Qualcomm MDM9215, "
            "поддерживающий скорость загрузки до 150 Мбит/с и выгрузки до 50 Мбит/с.\n\n"
            "Модуль выполнен в стандартном форм-факторе Mini PCIe Full Size. MC7350 относится к тому же семейству, что и MC7304, "
            "но по умолчанию предлагает более широкую поддержку глобальных диапазонов. Поддерживает интерфейсы USB 2.0, UART и SPI.\n\n"
            "MC7350 сертифицирован ведущими мировыми операторами, что делает его подходящим для промышленных маршрутизаторов, "
            "отслеживания активов, интеллектуальных счетчиков и устройств телемедицины."
        ),
        "features": [
            "Чипсет Qualcomm MDM9215",
            "LTE-A Cat 4 с загрузкой до 150 Мбит/с",
            "Скорость выгрузки до 50 Мбит/с",
            "Стандартный форм-фактор Mini PCIe Full Size",
            "Поддержка интерфейсов USB 2.0, UART, SPI",
            "Широкая глобальная сертификация операторов",
            "Встроенная GNSS GPS / GLONASS",
            "Широкий температурный диапазон -40°C ~ +85°C",
        ],
    },
    "mc7354": {
        "title": "MC7354 Сотовый модуль LTE-A Cat 4",
        "desc": "MC7354 — сотовый модуль LTE-A Cat 4 на чипсете Qualcomm MDM9215, скорость загрузки до 150 Мбит/с, форм-фактор Mini PCIe, оптимизированный для региональных комбинаций диапазонов.",
        "overview": (
            "MC7354 — это сотовый модуль LTE-Advanced Cat 4 от Sierra Wireless на чипсете Qualcomm MDM9215, "
            "поддерживающий скорость загрузки до 150 Мбит/с и выгрузки до 50 Мбит/с.\n\n"
            "Модуль выполнен в стандартном форм-факторе Mini PCIe Full Size. MC7354 отличается от других модулей серии MC "
            "специфическими комбинациями диапазонов, оптимизированными для сетей конкретных региональных операторов. "
            "Поддерживает интерфейсы USB 2.0, UART и SPI.\n\n"
            "MC7354 идеален для промышленной автоматизации, транспорта, интеллектуальных сетей "
            "и приложений мониторинга инфраструктуры, требующих надежного LTE-соединения."
        ),
        "features": [
            "Чипсет Qualcomm MDM9215",
            "LTE-A Cat 4 с загрузкой до 150 Мбит/с",
            "Скорость выгрузки до 50 Мбит/с",
            "Стандартный форм-фактор Mini PCIe Full Size",
            "Поддержка интерфейсов USB 2.0, UART, SPI",
            "Оптимизирован для региональных комбинаций диапазонов",
            "Встроенная GNSS GPS / GLONASS",
            "Широкий температурный диапазон -40°C ~ +85°C",
        ],
    },
    "mc7455": {
        "title": "MC7455 Сотовый модуль LTE-A Cat 6",
        "desc": "MC7455 — сотовый модуль LTE-A Cat 6 на чипсете Qualcomm MDM9230, скорость загрузки до 300 Мбит/с, форм-фактор Mini PCIe для высокопроизводительных промышленных и транспортных систем связи.",
        "overview": (
            "MC7455 — это сотовый модуль LTE-Advanced Cat 6 от Sierra Wireless на чипсете Qualcomm MDM9230, "
            "поддерживающий агрегацию несущих 2×20 МГц (2×CA) со скоростью загрузки до 300 Мбит/с и выгрузки до 50 Мбит/с.\n\n"
            "Модуль выполнен в стандартном форм-факторе Mini PCIe Full Size и является самой производительной моделью в серии MC. "
            "Поддерживает интерфейсы USB 3.0, UART и SPI для быстрой передачи данных.\n\n"
            "MC7455 поддерживает основные глобальные диапазоны LTE, включая FirstNet B14, "
            "и широко применяется в высокопроизводительных промышленных маршрутизаторах, системах связи транспортных средств, "
            "базовых станциях частных сетей и корпоративных решениях связи."
        ),
        "features": [
            "Чипсет Qualcomm MDM9230",
            "LTE-A Cat 6 с агрегацией несущих 2×CA",
            "Загрузка до 300 Мбит/с, выгрузка до 50 Мбит/с",
            "Стандартный форм-фактор Mini PCIe Full Size",
            "Поддержка интерфейсов USB 3.0, UART, SPI",
            "Поддержка диапазона FirstNet B14",
            "Встроенная GNSS GPS / GLONASS / BeiDou",
            "Широкий температурный диапазон -40°C ~ +85°C",
        ],
    },
}



# ── Translation data: zh-tw phrase → locale string ──────────────────────────
# Keys are the zh-tw source text; translate_text() falls back to zh-tw if missing.

TRANSLATION_DATA = {
    "zh-cn": {
        "連結": "链接",
        "資源": "资源",
        "規格": "规格",
        "項目": "参数",
        "備註": "备注",
        "狀態": "状态",
        "作業系統": "操作系统",

        "法律免責聲明": "法律免责声明",
        "不支援": "不支持",
        "經 Sierra Wireless 驅動程式認證": "经 Sierra Wireless 驱动程序认证",
        "核心內建 QMI_WWAN / option 驅動": "内核内置 QMI_WWAN / option 驱动",
        "可透過 USB OTG 連接": "可通过 USB OTG 连接",
        "需安裝 kmod-usb-net-qmi-wwan": "需安装 kmod-usb-net-qmi-wwan",
        "核心內建 QMI_WWAN / MBIM 驅動": "内核内置 QMI_WWAN / MBIM 驱动",
        "支援 SDK 整合": "支持 SDK 集成",
        "核心內建 MHIM / QMI_WWAN 驅動": "内核内置 MBIM / QMI_WWAN 驱动",
        "核心內建 option 驅動": "内核内置 option 驱动",
        "需安裝 kmod-usb-serial-option": "需安装 kmod-usb-serial-option",
        "1 × 文件包裝": "1 × 文件包装",
        "2 × 文件包裝": "2 × 文件包装",
        "官方產品頁面": "官方产品页面",
        "技術規格書 (PDF)": "技术规格书 (PDF)",
        # EM series MC series titles
        "EM7430 LTE-A Cat 6 蜂窩模組": "EM7430 LTE-A Cat 6 蜂窝模块",
        "EM7455 LTE-A Cat 6 蜂窩模組": "EM7455 LTE-A Cat 6 蜂窝模块",
        "EM7511 LTE-A Pro Cat 12 蜂窩模組": "EM7511 LTE-A Pro Cat 12 蜂窝模块",
        "EM7565 LTE-A Pro Cat 12 蜂窩模組": "EM7565 LTE-A Pro Cat 12 蜂窝模块",
        "EM9190 5G NR Sub-6 蜂窩模組": "EM9190 5G NR Sub-6 蜂窝模块",
        "EM9191 5G NR Sub-6 + mmWave 蜂窩模組": "EM9191 5G NR Sub-6 + mmWave 蜂窝模块",
        "MC7304 LTE-A Cat 4 蜂窩模組": "MC7304 LTE-A Cat 4 蜂窝模块",
        "MC7350 LTE-A Cat 4 蜂窩模組": "MC7350 LTE-A Cat 4 蜂窝模块",
        "MC7354 LTE-A Cat 4 蜂窩模組": "MC7354 LTE-A Cat 4 蜂窝模块",
        "MC7455 LTE-A Cat 6 蜂窩模組": "MC7455 LTE-A Cat 6 蜂窝模块",
        # Spec values
        "全球 (多頻段)": "全球 (多频段)",
        "全球 (含 B14 FirstNet)": "全球 (含 B14 FirstNet)",
        "蜂窩模組": "蜂窝模块",
    },
    "en": {
        "連結": "Link",
        "資源": "Resource",
        "規格": "Value",
        "項目": "Parameter",
        "備註": "Notes",
        "狀態": "Status",
        "作業系統": "OS",

        "法律免責聲明": "Legal Disclaimer",
        "不支援": "Not supported",
        "經 Sierra Wireless 驅動程式認證": "Certified by Sierra Wireless drivers",
        "核心內建 QMI_WWAN / option 驅動": "In-kernel QMI_WWAN / option driver",
        "可透過 USB OTG 連接": "Available via USB OTG",
        "需安裝 kmod-usb-net-qmi-wwan": "Requires kmod-usb-net-qmi-wwan",
        "核心內建 QMI_WWAN / MBIM 驅動": "In-kernel QMI_WWAN / MBIM driver",
        "支援 SDK 整合": "SDK integration supported",
        "核心內建 MHIM / QMI_WWAN 驅動": "In-kernel MBIM / QMI_WWAN driver",
        "核心內建 option 驅動": "In-kernel option driver",
        "需安裝 kmod-usb-serial-option": "Requires kmod-usb-serial-option",
        "1 × 文件包裝": "1 × Documentation pack",
        "2 × 文件包裝": "2 × Documentation pack",
        "官方產品頁面": "Official Product Page",
        "技術規格書 (PDF)": "Technical Specification (PDF)",
        # EM series MC series titles
        "EM7430 LTE-A Cat 6 蜂窩模組": "EM7430 LTE-A Cat 6 Cellular Module",
        "EM7455 LTE-A Cat 6 蜂窩模組": "EM7455 LTE-A Cat 6 Cellular Module",
        "EM7511 LTE-A Pro Cat 12 蜂窩模組": "EM7511 LTE-A Pro Cat 12 Cellular Module",
        "EM7565 LTE-A Pro Cat 12 蜂窩模組": "EM7565 LTE-A Pro Cat 12 Cellular Module",
        "EM9190 5G NR Sub-6 蜂窩模組": "EM9190 5G NR Sub-6 Cellular Module",
        "EM9191 5G NR Sub-6 + mmWave 蜂窩模組": "EM9191 5G NR Sub-6 + mmWave Cellular Module",
        "MC7304 LTE-A Cat 4 蜂窩模組": "MC7304 LTE-A Cat 4 Cellular Module",
        "MC7350 LTE-A Cat 4 蜂窩模組": "MC7350 LTE-A Cat 4 Cellular Module",
        "MC7354 LTE-A Cat 4 蜂窩模組": "MC7354 LTE-A Cat 4 Cellular Module",
        "MC7455 LTE-A Cat 6 蜂窩模組": "MC7455 LTE-A Cat 6 Cellular Module",
        "全球 (多頻段)": "Global (Multi-band)",
        "全球 (含 B14 FirstNet)": "Global (with B14 FirstNet)",
        "蜂窩模組": "Cellular Module",
    },
    "ja": {
        "連結": "リンク",
        "資源": "リソース",
        "規格": "仕様",
        "項目": "項目",
        "備註": "備考",
        "狀態": "状態",
        "作業系統": "OS",

        "法律免責聲明": "法的免責事項",
        "不支援": "非対応",
        "經 Sierra Wireless 驅動程式認證": "Sierra Wireless ドライバー認証済み",
        "核心內建 QMI_WWAN / option 驅動": "カーネル内蔵 QMI_WWAN / option ドライバー",
        "可透過 USB OTG 連接": "USB OTG 経由で接続可能",
        "需安裝 kmod-usb-net-qmi-wwan": "kmod-usb-net-qmi-wwan のインストールが必要",
        "核心內建 QMI_WWAN / MBIM 驅動": "カーネル内蔵 QMI_WWAN / MBIM ドライバー",
        "支援 SDK 整合": "SDK 統合に対応",
        "核心內建 MHIM / QMI_WWAN 驅動": "カーネル内蔵 MBIM / QMI_WWAN ドライバー",
        "核心內建 option 驅動": "カーネル内蔵 option ドライバー",
        "需安裝 kmod-usb-serial-option": "kmod-usb-serial-option のインストールが必要",
        "1 × 文件包裝": "1 × ドキュメントパック",
        "2 × 文件包裝": "2 × ドキュメントパック",
        "官方產品頁面": "公式製品ページ",
        "技術規格書 (PDF)": "技術仕様書 (PDF)",
        # Titles
        "EM7430 LTE-A Cat 6 蜂窩模組": "EM7430 LTE-A Cat 6 セルラーモジュール",
        "EM7455 LTE-A Cat 6 蜂窩模組": "EM7455 LTE-A Cat 6 セルラーモジュール",
        "EM7511 LTE-A Pro Cat 12 蜂窩模組": "EM7511 LTE-A Pro Cat 12 セルラーモジュール",
        "EM7565 LTE-A Pro Cat 12 蜂窩模組": "EM7565 LTE-A Pro Cat 12 セルラーモジュール",
        "EM9190 5G NR Sub-6 蜂窩模組": "EM9190 5G NR Sub-6 セルラーモジュール",
        "EM9191 5G NR Sub-6 + mmWave 蜂窩模組": "EM9191 5G NR Sub-6 + mmWave セルラーモジュール",
        "MC7304 LTE-A Cat 4 蜂窩模組": "MC7304 LTE-A Cat 4 セルラーモジュール",
        "MC7350 LTE-A Cat 4 蜂窩模組": "MC7350 LTE-A Cat 4 セルラーモジュール",
        "MC7354 LTE-A Cat 4 蜂窩模組": "MC7354 LTE-A Cat 4 セルラーモジュール",
        "MC7455 LTE-A Cat 6 蜂窩模組": "MC7455 LTE-A Cat 6 セルラーモジュール",
        "全球 (多頻段)": "グローバル (マルチバンド)",
        "全球 (含 B14 FirstNet)": "グローバル (B14 FirstNet 対応)",
        "蜂窩模組": "セルラーモジュール",
    },
    "ar": {
        "連結": "الرابط",
        "資源": "المورد",
        "規格": "المواصفات",
        "項目": "المعيار",
        "備註": "ملاحظات",
        "狀態": "الحالة",
        "作業系統": "نظام التشغيل",

        "法律免責聲明": "إخلاء المسؤولية القانوني",
        "不支援": "غير مدعوم",
        "經 Sierra Wireless 驅動程式認證": "معتمد من برامج تشغيل Sierra Wireless",
        "核心內建 QMI_WWAN / option 驅動": "برنامج تشغيل QMI_WWAN / option مدمج في النواة",
        "可透過 USB OTG 連接": "متاح عبر USB OTG",
        "需安裝 kmod-usb-net-qmi-wwan": "يتطلب تثبيت kmod-usb-net-qmi-wwan",
        "核心內建 QMI_WWAN / MBIM 驅動": "برنامج تشغيل QMI_WWAN / MBIM مدمج في النواة",
        "支援 SDK 整合": "يدعم تكامل SDK",
        "核心內建 MHIM / QMI_WWAN 驅動": "برنامج تشغيل MBIM / QMI_WWAN مدمج في النواة",
        "核心內建 option 驅動": "برنامج تشغيل option مدمج في النواة",
        "需安裝 kmod-usb-serial-option": "يتطلب تثبيت kmod-usb-serial-option",
        "1 × 文件包裝": "1 × حزمة المستندات",
        "2 × 文件包裝": "2 × حزمة المستندات",
        "官方產品頁面": "صفحة المنتج الرسمية",
        "技術規格書 (PDF)": "المواصفات الفنية (PDF)",
        # Titles
        "EM7430 LTE-A Cat 6 蜂窩模組": "وحدة EM7430 LTE-A Cat 6 الخلوية",
        "EM7455 LTE-A Cat 6 蜂窩模組": "وحدة EM7455 LTE-A Cat 6 الخلوية",
        "EM7511 LTE-A Pro Cat 12 蜂窩模組": "وحدة EM7511 LTE-A Pro Cat 12 الخلوية",
        "EM7565 LTE-A Pro Cat 12 蜂窩模組": "وحدة EM7565 LTE-A Pro Cat 12 الخلوية",
        "EM9190 5G NR Sub-6 蜂窩模組": "وحدة EM9190 5G NR Sub-6 الخلوية",
        "EM9191 5G NR Sub-6 + mmWave 蜂窩模組": "وحدة EM9191 5G NR Sub-6 + mmWave الخلوية",
        "MC7304 LTE-A Cat 4 蜂窩模組": "وحدة MC7304 LTE-A Cat 4 الخلوية",
        "MC7350 LTE-A Cat 4 蜂窩模組": "وحدة MC7350 LTE-A Cat 4 الخلوية",
        "MC7354 LTE-A Cat 4 蜂窩模組": "وحدة MC7354 LTE-A Cat 4 الخلوية",
        "MC7455 LTE-A Cat 6 蜂窩模組": "وحدة MC7455 LTE-A Cat 6 الخلوية",
        "全球 (多頻段)": "عالمي (متعدد النطاقات)",
        "全球 (含 B14 FirstNet)": "عالمي (مع B14 FirstNet)",
        "蜂窩模組": "الخلوية",
    },
    "es": {
        "連結": "Enlace",
        "資源": "Recurso",
        "規格": "Valor",
        "項目": "Parámetro",
        "備註": "Notas",
        "狀態": "Estado",
        "作業系統": "SO",

        "法律免責聲明": "Aviso Legal",
        "不支援": "No compatible",
        "經 Sierra Wireless 驅動程式認證": "Certificado por controladores Sierra Wireless",
        "核心內建 QMI_WWAN / option 驅動": "Controlador QMI_WWAN / option en el núcleo",
        "可透過 USB OTG 連接": "Disponible vía USB OTG",
        "需安裝 kmod-usb-net-qmi-wwan": "Requiere kmod-usb-net-qmi-wwan",
        "核心內建 QMI_WWAN / MBIM 驅動": "Controlador QMI_WWAN / MBIM en el núcleo",
        "支援 SDK 整合": "Integración SDK compatible",
        "核心內建 MHIM / QMI_WWAN 驅動": "Controlador MBIM / QMI_WWAN en el núcleo",
        "核心內建 option 驅動": "Controlador option en el núcleo",
        "需安裝 kmod-usb-serial-option": "Requiere kmod-usb-serial-option",
        "1 × 文件包裝": "1 × Paquete de documentación",
        "2 × 文件包裝": "2 × Paquete de documentación",
        "官方產品頁面": "Página oficial del producto",
        "技術規格書 (PDF)": "Ficha técnica (PDF)",
        # Titles
        "EM7430 LTE-A Cat 6 蜂窩模組": "Módulo Celular EM7430 LTE-A Cat 6",
        "EM7455 LTE-A Cat 6 蜂窩模組": "Módulo Celular EM7455 LTE-A Cat 6",
        "EM7511 LTE-A Pro Cat 12 蜂窩模組": "Módulo Celular EM7511 LTE-A Pro Cat 12",
        "EM7565 LTE-A Pro Cat 12 蜂窩模組": "Módulo Celular EM7565 LTE-A Pro Cat 12",
        "EM9190 5G NR Sub-6 蜂窩模組": "Módulo Celular EM9190 5G NR Sub-6",
        "EM9191 5G NR Sub-6 + mmWave 蜂窩模組": "Módulo Celular EM9191 5G NR Sub-6 + mmWave",
        "MC7304 LTE-A Cat 4 蜂窩模組": "Módulo Celular MC7304 LTE-A Cat 4",
        "MC7350 LTE-A Cat 4 蜂窩模組": "Módulo Celular MC7350 LTE-A Cat 4",
        "MC7354 LTE-A Cat 4 蜂窩模組": "Módulo Celular MC7354 LTE-A Cat 4",
        "MC7455 LTE-A Cat 6 蜂窩模組": "Módulo Celular MC7455 LTE-A Cat 6",
        "全球 (多頻段)": "Global (Multibanda)",
        "全球 (含 B14 FirstNet)": "Global (con B14 FirstNet)",
        "蜂窩模組": "Módulo Celular",
    },
    "pt": {
        "連結": "Link",
        "資源": "Recurso",
        "規格": "Valor",
        "項目": "Parâmetro",
        "備註": "Observações",
        "狀態": "Status",
        "作業系統": "SO",

        "法律免責聲明": "Aviso Legal",
        "不支援": "Não suportado",
        "經 Sierra Wireless 驅動程式認證": "Certificado por drivers Sierra Wireless",
        "核心內建 QMI_WWAN / option 驅動": "Driver QMI_WWAN / option no kernel",
        "可透過 USB OTG 連接": "Disponível via USB OTG",
        "需安裝 kmod-usb-net-qmi-wwan": "Requer kmod-usb-net-qmi-wwan",
        "核心內建 QMI_WWAN / MBIM 驅動": "Driver QMI_WWAN / MBIM no kernel",
        "支援 SDK 整合": "Integração SDK suportada",
        "核心內建 MHIM / QMI_WWAN 驅動": "Driver MBIM / QMI_WWAN no kernel",
        "核心內建 option 驅動": "Driver option no kernel",
        "需安裝 kmod-usb-serial-option": "Requer kmod-usb-serial-option",
        "1 × 文件包裝": "1 × Pacote de documentação",
        "2 × 文件包裝": "2 × Pacote de documentação",
        "官方產品頁面": "Página oficial do produto",
        "技術規格書 (PDF)": "Especificações técnicas (PDF)",
        # Titles
        "EM7430 LTE-A Cat 6 蜂窩模組": "Módulo Celular EM7430 LTE-A Cat 6",
        "EM7455 LTE-A Cat 6 蜂窩模組": "Módulo Celular EM7455 LTE-A Cat 6",
        "EM7511 LTE-A Pro Cat 12 蜂窩模組": "Módulo Celular EM7511 LTE-A Pro Cat 12",
        "EM7565 LTE-A Pro Cat 12 蜂窩模組": "Módulo Celular EM7565 LTE-A Pro Cat 12",
        "EM9190 5G NR Sub-6 蜂窩模組": "Módulo Celular EM9190 5G NR Sub-6",
        "EM9191 5G NR Sub-6 + mmWave 蜂窩模組": "Módulo Celular EM9191 5G NR Sub-6 + mmWave",
        "MC7304 LTE-A Cat 4 蜂窩模組": "Módulo Celular MC7304 LTE-A Cat 4",
        "MC7350 LTE-A Cat 4 蜂窩模組": "Módulo Celular MC7350 LTE-A Cat 4",
        "MC7354 LTE-A Cat 4 蜂窩模組": "Módulo Celular MC7354 LTE-A Cat 4",
        "MC7455 LTE-A Cat 6 蜂窩模組": "Módulo Celular MC7455 LTE-A Cat 6",
        "全球 (多頻段)": "Global (Multibanda)",
        "全球 (含 B14 FirstNet)": "Global (com B14 FirstNet)",
        "蜂窩模組": "Módulo Celular",
    },
    "ru": {
        "連結": "Ссылка",
        "資源": "Ресурс",
        "規格": "Значение",
        "項目": "Параметр",
        "備註": "Примечания",
        "狀態": "Статус",
        "作業系統": "ОС",

        "法律免責聲明": "Юридическое предупреждение",
        "不支援": "Не поддерживается",
        "經 Sierra Wireless 驅動程式認證": "Сертифицировано драйверами Sierra Wireless",
        "核心內建 QMI_WWAN / option 驅動": "Встроенный драйвер QMI_WWAN / option в ядре",
        "可透過 USB OTG 連接": "Доступно через USB OTG",
        "需安裝 kmod-usb-net-qmi-wwan": "Требуется kmod-usb-net-qmi-wwan",
        "核心內建 QMI_WWAN / MBIM 驅動": "Встроенный драйвер QMI_WWAN / MBIM в ядре",
        "支援 SDK 整合": "Поддержка интеграции SDK",
        "核心內建 MHIM / QMI_WWAN 驅動": "Встроенный драйвер MBIM / QMI_WWAN в ядре",
        "核心內建 option 驅動": "Встроенный драйвер option в ядре",
        "需安裝 kmod-usb-serial-option": "Требуется kmod-usb-serial-option",
        "1 × 文件包裝": "1 × Пакет документации",
        "2 × 文件包裝": "2 × Пакет документации",
        "官方產品頁面": "Официальная страница продукта",
        "技術規格書 (PDF)": "Технические характеристики (PDF)",
        # Titles
        "EM7430 LTE-A Cat 6 蜂窩模組": "Сотовый модуль EM7430 LTE-A Cat 6",
        "EM7455 LTE-A Cat 6 蜂窩模組": "Сотовый модуль EM7455 LTE-A Cat 6",
        "EM7511 LTE-A Pro Cat 12 蜂窩模組": "Сотовый модуль EM7511 LTE-A Pro Cat 12",
        "EM7565 LTE-A Pro Cat 12 蜂窩模組": "Сотовый модуль EM7565 LTE-A Pro Cat 12",
        "EM9190 5G NR Sub-6 蜂窩模組": "Сотовый модуль EM9190 5G NR Sub-6",
        "EM9191 5G NR Sub-6 + mmWave 蜂窩模組": "Сотовый модуль EM9191 5G NR Sub-6 + mmWave",
        "MC7304 LTE-A Cat 4 蜂窩模組": "Сотовый модуль MC7304 LTE-A Cat 4",
        "MC7350 LTE-A Cat 4 蜂窩模組": "Сотовый модуль MC7350 LTE-A Cat 4",
        "MC7354 LTE-A Cat 4 蜂窩模組": "Сотовый модуль MC7354 LTE-A Cat 4",
        "MC7455 LTE-A Cat 6 蜂窩模組": "Сотовый модуль MC7455 LTE-A Cat 6",
        "全球 (多頻段)": "Глобальный (Многодиапазонный)",
        "全球 (含 B14 FirstNet)": "Глобальный (с B14 FirstNet)",
        "蜂窩模組": "Сотовый модуль",
    },
    "de": {
        "連結": "Link",
        "資源": "Ressource",
        "規格": "Wert",
        "項目": "Parameter",
        "備註": "Anmerkungen",
        "狀態": "Status",
        "作業系統": "Betriebssystem",

        "法律免責聲明": "Rechtlicher Hinweis",
        "不支援": "Nicht unterstützt",
        "經 Sierra Wireless 驅動程式認證": "Durch Sierra Wireless Treiber zertifiziert",
        "核心內建 QMI_WWAN / option 驅動": "Integrierter QMI_WWAN / option Kernel-Treiber",
        "可透過 USB OTG 連接": "Verfügbar über USB OTG",
        "需安裝 kmod-usb-net-qmi-wwan": "Erfordert kmod-usb-net-qmi-wwan",
        "核心內建 QMI_WWAN / MBIM 驅動": "Integrierter QMI_WWAN / MBIM Kernel-Treiber",
        "支援 SDK 整合": "SDK-Integration unterstützt",
        "核心內建 MHIM / QMI_WWAN 驅動": "Integrierter MBIM / QMI_WWAN Kernel-Treiber",
        "核心內建 option 驅動": "Integrierter option Kernel-Treiber",
        "需安裝 kmod-usb-serial-option": "Erfordert kmod-usb-serial-option",
        "1 × 文件包裝": "1 × Dokumentationspaket",
        "2 × 文件包裝": "2 × Dokumentationspaket",
        "官方產品頁面": "Offizielle Produktseite",
        "技術規格書 (PDF)": "Technisches Datenblatt (PDF)",
        # Titles
        "EM7430 LTE-A Cat 6 蜂窩模組": "EM7430 LTE-A Cat 6 Mobilfunkmodul",
        "EM7455 LTE-A Cat 6 蜂窩模組": "EM7455 LTE-A Cat 6 Mobilfunkmodul",
        "EM7511 LTE-A Pro Cat 12 蜂窩模組": "EM7511 LTE-A Pro Cat 12 Mobilfunkmodul",
        "EM7565 LTE-A Pro Cat 12 蜂窩模組": "EM7565 LTE-A Pro Cat 12 Mobilfunkmodul",
        "EM9190 5G NR Sub-6 蜂窩模組": "EM9190 5G NR Sub-6 Mobilfunkmodul",
        "EM9191 5G NR Sub-6 + mmWave 蜂窩模組": "EM9191 5G NR Sub-6 + mmWave Mobilfunkmodul",
        "MC7304 LTE-A Cat 4 蜂窩模組": "MC7304 LTE-A Cat 4 Mobilfunkmodul",
        "MC7350 LTE-A Cat 4 蜂窩模組": "MC7350 LTE-A Cat 4 Mobilfunkmodul",
        "MC7354 LTE-A Cat 4 蜂窩模組": "MC7354 LTE-A Cat 4 Mobilfunkmodul",
        "MC7455 LTE-A Cat 6 蜂窩模組": "MC7455 LTE-A Cat 6 Mobilfunkmodul",
        "全球 (多頻段)": "Global (Multiband)",
        "全球 (含 B14 FirstNet)": "Global (mit B14 FirstNet)",
        "蜂窩模組": "Mobilfunkmodul",
    },
    "fr": {
        "連結": "Lien",
        "資源": "Ressource",
        "規格": "Valeur",
        "項目": "Paramètre",
        "備註": "Remarques",
        "狀態": "État",
        "作業系統": "OS",

        "法律免責聲明": "Avis de non-responsabilité légal",
        "不支援": "Non pris en charge",
        "經 Sierra Wireless 驅動程式認證": "Certifié par les pilotes Sierra Wireless",
        "核心內建 QMI_WWAN / option 驅動": "Pilote QMI_WWAN / option intégré au noyau",
        "可透過 USB OTG 連接": "Disponible via USB OTG",
        "需安裝 kmod-usb-net-qmi-wwan": "Nécessite kmod-usb-net-qmi-wwan",
        "核心內建 QMI_WWAN / MBIM 驅動": "Pilote QMI_WWAN / MBIM intégré au noyau",
        "支援 SDK 整合": "Intégration SDK prise en charge",
        "核心內建 MHIM / QMI_WWAN 驅動": "Pilote MBIM / QMI_WWAN intégré au noyau",
        "核心內建 option 驅動": "Pilote option intégré au noyau",
        "需安裝 kmod-usb-serial-option": "Nécessite kmod-usb-serial-option",
        "1 × 文件包裝": "1 × Pack de documentation",
        "2 × 文件包裝": "2 × Pack de documentation",
        "官方產品頁面": "Page officielle du produit",
        "技術規格書 (PDF)": "Fiche technique (PDF)",
        # Titles
        "EM7430 LTE-A Cat 6 蜂窩模組": "Module cellulaire EM7430 LTE-A Cat 6",
        "EM7455 LTE-A Cat 6 蜂窩模組": "Module cellulaire EM7455 LTE-A Cat 6",
        "EM7511 LTE-A Pro Cat 12 蜂窩模組": "Module cellulaire EM7511 LTE-A Pro Cat 12",
        "EM7565 LTE-A Pro Cat 12 蜂窩模組": "Module cellulaire EM7565 LTE-A Pro Cat 12",
        "EM9190 5G NR Sub-6 蜂窩模組": "Module cellulaire EM9190 5G NR Sub-6",
        "EM9191 5G NR Sub-6 + mmWave 蜂窩模組": "Module cellulaire EM9191 5G NR Sub-6 + mmWave",
        "MC7304 LTE-A Cat 4 蜂窩模組": "Module cellulaire MC7304 LTE-A Cat 4",
        "MC7350 LTE-A Cat 4 蜂窩模組": "Module cellulaire MC7350 LTE-A Cat 4",
        "MC7354 LTE-A Cat 4 蜂窩模組": "Module cellulaire MC7354 LTE-A Cat 4",
        "MC7455 LTE-A Cat 6 蜂窩模組": "Module cellulaire MC7455 LTE-A Cat 6",
        "全球 (多頻段)": "Monde (Multibande)",
        "全球 (含 B14 FirstNet)": "Monde (avec B14 FirstNet)",
        "蜂窩模組": "Module cellulaire",
    },
}


# ── zh-tw → zh-cn character conversion ──────────────────────────────────────

ZH_TW_TO_CN = str.maketrans({
    "採": "采", "標": "标", "準": "准", "載": "载", "達": "达",
    "業": "业", "級": "级", "裝": "装", "雙": "双", "內": "内",
    "寬": "宽", "設": "设", "線": "线", "機": "机", "認": "认",
    "證": "证", "體": "体", "優": "优", "監": "监", "熱": "热",
    "點": "点", "視": "视", "訊": "讯", "終": "终", "導": "导",
    "驅": "驱", "動": "动", "號": "号", "碼": "码", "稱": "称",
    "組": "组", "統": "统", "靈": "灵", "閘": "闸", "頻": "频",
    "範": "范", "圍": "围", "專": "专", "協": "协", "議": "议",
    "韌": "韧", "異": "异", "構": "构", "網": "网", "絡": "络",
    "維": "维", "護": "护", "連": "连", "萬": "万", "億": "亿",
    "數": "数", "庫": "库", "雲": "云", "檔": "档", "關": "关",
    "鍵": "键", "預": "预", "測": "测", "穩": "稳", "價": "价",
    "臺": "台", "灣": "湾", "隊": "队", "際": "际", "與": "与",
    "實": "实", "踐": "践", "積": "积", "極": "极", "權": "权",
    "檢": "检", "驗": "验", "書": "书", "畫": "画", "節": "节",
    "產": "产", "務": "务", "強": "强", "態": "态", "軟": "软",
    "燒": "烧", "錄": "录", "適": "适", "於": "于", "應": "应",
    "選": "选", "擇": "择", "進": "进", "規": "规", "評": "评",
    "試": "试", "訂": "订", "變": "变", "壞": "坏", "確": "确",
    "報": "报", "費": "费", "準": "准", "遲": "迟", "讓": "让",
    "護": "护", "覽": "览", "釋": "释", "訊": "讯", "術": "术",
    "傷": "伤", "類": "类", "觀": "观", "讀": "读",
    "艦": "舰", "窩": "窝", "傳": "传", "棄": "弃",
    "衛": "卫", "戰": "战", "爭": "争", "庫": "库",
    "僅": "仅", "異": "异", "爾": "尔", "樂": "乐",
    "標": "标", "準": "准", "處": "处", "眾": "众",
    "團": "团", "隊": "队", "歸": "归", "禮": "礼",
    "擊": "击", "敗": "败", "勝": "胜", "協": "协",
    "廣": "广", "蓋": "盖", "計": "计", "別": "别",
    "據": "据", "車": "车", "輕": "轻", "較": "较",
    "輪": "轮", "響": "响", "續": "续", "層": "层",
    "揚": "扬", "塗": "涂", "膠": "胶", "彈": "弹",
    "壓": "压", "歸": "归", "懸": "悬", "匯": "汇",
    "廢": "废", "憂": "忧", "猶": "犹", "壓": "压",
    "頁": "页", "項": "项", "順": "顺", "頒": "颁",
    "額": "额", "顏": "颜", "願": "愿", "顯": "显",
    "風": "风", "飛": "飞", "食": "食", "首": "首",
    "香": "香", "馬": "马", "魚": "鱼", "鳥": "鸟",
    "鹵": "卤", "鹿": "鹿", "麥": "麦", "麻": "麻",
    "黃": "黄", "黑": "黑", "鼠": "鼠", "鼻": "鼻",
    "齊": "齐", "齒": "齿", "龍": "龙", "龜": "龟",
    "聲": "声", "聽": "听", "肅": "肃", "虛": "虚",
    "虎": "虎", "蟲": "虫", "血": "血", "行": "行",
    "衣": "衣", "襯": "衬", "西": "西", "見": "见",
    "覺": "觉", "解": "解", "觸": "触", "角": "角",
    "言": "言", "譽": "誉", "豐": "丰", "豔": "艳",
    "貝": "贝", "賦": "赋", "賬": "账", "質": "质",
    "賤": "贱", "貼": "贴", "賀": "贺", "賈": "贾",
    "賴": "赖", "贊": "赞", "贈": "赠", "贏": "赢",
    "赤": "赤", "走": "走", "足": "足", "踐": "践",
    "躍": "跃", "身": "身", "軀": "躯", "車": "车",
    "軍": "军", "軌": "轨", "軸": "轴", "輕": "轻",
    "較": "较", "載": "载", "輔": "辅", "輛": "辆",
    "輦": "辇", "輩": "辈", "輪": "轮", "輸": "输",
    "辻": "辻", "辛": "辛", "辦": "办", "辭": "辞",
    "辵": "辵", "邊": "边", "遼": "辽", "達": "达",
    "遷": "迁", "邏": "逻", "邑": "邑", "郵": "邮",
    "鄉": "乡", "鄧": "邓", "酉": "酉", "醬": "酱",
    "醫": "医", "釀": "酿", "采": "采", "釋": "释",
    "裏": "里", "補": "补", "裝": "装", "製": "制",
    "複": "复", "裡": "里", "褲": "裤", "襪": "袜",
    "襲": "袭", "覆": "覆", "訊": "讯", "註": "注",
    "誌": "志", "說": "说", "課": "课", "調": "调",
    "談": "谈", "請": "请", "論": "论", "諸": "诸",
    "諾": "诺", "講": "讲", "謎": "谜", "謝": "谢",
    "謠": "谣", "謗": "谤", "謙": "谦", "謹": "谨",
    "識": "识", "議": "议", "護": "护", "譽": "誉",
    "變": "变", "讓": "让", "讚": "赞", "豈": "岂",
    "財": "财", "責": "责", "貫": "贯", "貨": "货",
    "販": "贩", "貪": "贪", "貧": "贫", "責": "责",
    "貴": "贵", "買": "买", "費": "费", "貼": "贴",
    "貿": "贸", "資": "资", "賓": "宾", "賤": "贱",
    "賦": "赋", "賬": "账", "賭": "赌", "賴": "赖",
    "贊": "赞", "贈": "赠", "贏": "赢", "赫": "赫",
    "趙": "赵", "趕": "赶", "趨": "趋", "踐": "践",
    "蹈": "蹈", "蹟": "迹", "跳": "跳", "踐": "践",
    "躍": "跃", "躊": "踌", "躇": "躇", "躋": "跻",
    "躐": "躐", "躑": "踯", "軀": "躯", "輾": "辗",
    "轍": "辙", "轟": "轰", "轡": "辔", "轢": "轹",
    "轣": "轣", "轤": "轳", "辦": "办", "辨": "辨",
    "辭": "辞", "辮": "辫", "辯": "辩", "農": "农",
    "返": "返", "迎": "迎", "近": "近", "送": "送",
    "迪": "迪", "迴": "回", "迷": "迷", "追": "追",
    "退": "退", "送": "送", "逃": "逃", "逢": "逢",
    "遞": "递", "遠": "远", "適": "适", "遲": "迟",
    "遷": "迁", "選": "选", "遺": "遗", "避": "避",
    "還": "还", "邊": "边", "邏": "逻", "釀": "酿",
    "醫": "医", "醬": "酱", "釋": "释", "裏": "里",
    "補": "补", "裝": "装", "製": "制", "複": "复",
    "裡": "里", "褲": "裤", "襪": "袜", "襲": "袭",
    "覆": "覆", "訊": "讯", "註": "注", "誌": "志",
    "說": "说", "課": "课", "調": "调", "談": "谈",
    "請": "请", "論": "论", "諾": "诺", "講": "讲",
    "謝": "谢", "謠": "谣", "謗": "谤", "謙": "谦",
    "謹": "谨", "識": "识", "議": "议", "護": "护",
    "譽": "誉", "變": "变", "讓": "让", "讚": "赞",
    "豈": "岂", "財": "财", "責": "责", "貫": "贯",
    "貨": "货", "販": "贩", "貪": "贪", "貧": "贫",
    "責": "责", "貴": "贵", "買": "买", "費": "费",
    "貼": "贴", "貿": "贸", "資": "资", "賓": "宾",
    "賤": "贱", "賦": "赋", "賬": "账", "賭": "赌",
    "賴": "赖", "贊": "赞", "贈": "赠", "贏": "赢",
    "趙": "赵", "趕": "赶", "趨": "趋", "踐": "践",
    "蹈": "蹈", "蹟": "迹", "跳": "跳", "踐": "践",
    "躍": "跃", "躊": "踌", "躇": "躇", "躋": "跻",
    "躐": "躐", "躑": "踯", "軀": "躯", "輾": "辗",
    "轍": "辙", "轟": "轰", "轡": "辔", "轢": "轹",
    "轣": "轣", "轤": "轳", "辦": "办", "辨": "辨",
    "辭": "辞", "辮": "辫", "辯": "辩", "農": "农",
})

ZH_TW_TO_CN_WORDS = {
    "支援": "支持", "晶片": "芯片", "數據機": "数据机",
    "透過": "通过", "整合": "集成", "套件": "工具包",
    "資訊": "信息", "檔案": "文件",
    "閘道器": "网关", "行動熱點": "移动热点",
    "行動": "移动", "連線": "连接",
}


def zh_tw_to_cn(text):
    # Apply word replacements BEFORE char conversion so original TW keys still match
    for tw, cn in ZH_TW_TO_CN_WORDS.items():
        text = text.replace(tw, cn)
    text = text.translate(ZH_TW_TO_CN)
    return text


# ── Helper functions ─────────────────────────────────────────────────────────

def translate_text(text, lang):
    if lang == "zh-tw" or not text:
        return text
    return TRANSLATION_DATA.get(lang, {}).get(text, text)


def translate_or_fallback(zh_text, lang, en_fallback):
    if lang == "zh-tw":
        return zh_text
    translated = translate_text(zh_text, lang)
    if translated != zh_text:
        return translated
    if lang == "zh-cn":
        return zh_tw_to_cn(zh_text)
    return en_fallback


def translate_features(model, lang):
    """Translate feature list, falling back to English per-feature."""
    if lang == "zh-tw":
        return PRODUCT_ZH[model]["features"]
    en_list = PRODUCT_EN.get(model, {}).get("features", [])
    zh_list = PRODUCT_ZH[model]["features"]
    result = []
    for i, zh_f in enumerate(zh_list):
        translated = translate_text(zh_f, lang)
        if translated != zh_f:
            result.append(translated)
        elif lang == "zh-cn":
            result.append(zh_tw_to_cn(zh_f))
        elif i < len(en_list):
            result.append(en_list[i])
        else:
            result.append(zh_f)
    return result


def translate_package(model, lang):
    """Translate package items, handling 蜂窩模組 suffix per locale."""
    items = PACKAGE[model]
    if lang == "zh-tw":
        return items

    CELLULAR_SUFFIX = {
        "zh-cn": "蜂窝模块", "en": "Cellular Module",
        "ja": "セルラーモジュール", "ar": "الخلوية",
        "es": "Módulo Celular", "pt": "Módulo Celular",
        "ru": "Сотовый модуль", "de": "Mobilfunkmodul",
        "fr": "Module cellulaire",
    }
    suffix = CELLULAR_SUFFIX.get(lang)

    result = []
    for item in items:
        if "蜂窩模組" in item and suffix:
            idx = item.find("蜂窩模組")
            prefix = item[:idx]
            result.append(prefix + suffix)
        else:
            result.append(translate_text(item, lang))
    return result


def translate_resources(model, lang):
    """Translate resource names for a product."""
    resources = RESOURCES[model]
    if lang == "zh-tw":
        return resources
    return [(translate_text(name, lang), url) for name, url in resources]


def translate_os_rows(model, lang):
    """Translate OS support notes for a product."""
    rows = OS_ROWS[model]
    if lang == "zh-tw":
        return rows
    result = []
    for os_name, status, note in rows:
        result.append((os_name, status, translate_text(note, lang)))
    return result


def sh(lang):
    """Get section header translation."""
    return SECTION_HEADERS.get(lang, SECTION_HEADERS["zh-tw"])


def sl(lang):
    """Get spec label translation."""
    return SPEC_LABELS.get(lang, SPEC_LABELS["zh-tw"])


def generate_overview(lang):
    """Generate the overview _index.md page."""
    data = OVERVIEW_DATA.get(lang, OVERVIEW_DATA["zh-tw"])
    h = sh(lang)
    ch = COMP_HEADERS.get(lang, COMP_HEADERS["zh-tw"])

    # Build comparison table
    header_row = " | ".join(ch)
    sep_row = " | ".join(["---"] * len(ch))
    body_rows = "\n".join(f"| {' | '.join(row)} |" for row in COMP_ROWS)
    comp_table = f"| {header_row} |\n| {sep_row} |\n{body_rows}"

    # Build card-group
    cards = []
    for model in PRODUCTS:
        upper = model.upper()
        cards.append(
            f'  {{{{< card title="{upper}" href="/{lang}/products/sierra/{model}/" '
            f'image="/images/products/sierra/{model}.png" >}}}}'
        )
        cards.append(f"    {upper}")
        cards.append("  {{</card >}}")
    card_group = "{{< card-group >}}\n" + "\n".join(cards) + "\n{{< /card-group >}}"

    cta_text = CTA.get(lang, CTA["zh-tw"])

    content = f"""---
title: "{data['title']}"
description: "{data['desc']}"
date: 2026-07-29
draft: false
showBreadcrumbs: true
showTableOfContents: false
showChildPages: true
featureimage: "/images/products/sierra/sierra_banner.png"
---

{data['intro']}

---

## {h['產品線']}

{card_group}

---

## {h['規格比較']}

{comp_table}

---

{{{{< alert >}}}}
{cta_text}
{{{{</alert >}}}}
"""
    return content


def generate_product_page(lang, model):
    """Generate a product _index.md page."""
    zh = PRODUCT_ZH[model]
    h = sh(lang)
    label = sl(lang)
    cta_text = CTA.get(lang, CTA["zh-tw"])
    legal_text = LEGAL.get(lang, LEGAL["zh-tw"])

    # Translate content
    if lang == "zh-tw":
        title = zh["title"]
        desc = zh["desc"]
        overview = zh["overview"]
        features = zh["features"]
        package_items = PACKAGE[model]
        resources = RESOURCES[model]
        os_rows = OS_ROWS[model]
    else:
        # Try TRANSLATION_DATA first, fall back to PRODUCT_EN (English)
        en_data = PRODUCT_EN.get(model, {})
        title = translate_text(zh["title"], lang)
        desc = translate_or_fallback(zh["desc"], lang, en_data.get("desc", zh["desc"]))
        overview = translate_or_fallback(zh["overview"], lang, en_data.get("overview", zh["overview"]))
        features = translate_features(model, lang)
        package_items = translate_package(model, lang)
        resources = translate_resources(model, lang)
        os_rows = translate_os_rows(model, lang)

    # Override with locale-specific full dict for ja/de/fr
    locale_pages = {
        "ja": PRODUCT_JA,
        "de": PRODUCT_DE,
        "fr": PRODUCT_FR,
        "es": PRODUCT_ES,
        "pt": PRODUCT_PT,
        "ar": PRODUCT_AR,
        "ru": PRODUCT_RU,
    }
    locale_product = locale_pages.get(lang, {}).get(model, {})
    if locale_product:
        title = locale_product.get("title", title)
        desc = locale_product.get("desc", desc)
        overview = locale_product.get("overview", overview)
        features = locale_product.get("features", features)

    if model in ("em9190", "em9191"):
        featureimage_line = f'featureimage: "/images/products/sierra/{model}_hero.jpg"\n'
    else:
        featureimage_line = ""

    # Tags
    tags_str = ", ".join(f'"{t}"' for t in zh["tags"])

    # Build features
    features_bullets = "\n".join(f"- {f}" for f in features)

    # Build spec table
    spec_label = label.get("晶片型號", "晶片型號")
    spec_value = "規格"
    spec_rows_parts = []
    for spec_key, spec_val in PRODUCT_SPECS[model]:
        loc_key = label.get(spec_key, spec_key)
        # Translate spec values that might need translation
        val_parts = spec_val.split(" / ")
        translated_val_parts = []
        for vp in val_parts:
            translated_val_parts.append(translate_text(vp, lang) if lang != "zh-tw" else vp)
        loc_val = " / ".join(translated_val_parts)
        spec_rows_parts.append(f"| {loc_key} | {loc_val} |")
    spec_table_lines = "\n".join(spec_rows_parts)

    # Build OS support table
    os_header_os = translate_text("作業系統", lang) if lang != "zh-tw" else "OS"
    os_header_status = translate_text("狀態", lang) if lang != "zh-tw" else "Status"
    os_header_notes = translate_text("備註", lang) if lang != "zh-tw" else "Notes"
    os_table_parts = [f"| {os_header_os} | {os_header_status} | {os_header_notes} |",
                      "|------|---------|------|"]
    for os_name, status, note in os_rows:
        os_table_parts.append(f"| {os_name} | {status} | {note} |")
    os_table = "\n".join(os_table_parts)

    # Build package
    package_lines = "\n".join(f"- {item}" for item in package_items)

    # Build resources
    res_lines_parts = []
    for res_name, res_url in resources:
        res_lines_parts.append(f"| {res_name} | {res_url} |")
    res_table = "\n".join(res_lines_parts)

    # OS header label
    os_section_label = h.get("作業系統支援", "OS Support")

    content = f"""---
title: "{title}"
description: "{desc}"
date: 2026-07-29
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["sierra"]
tags: [{tags_str}]
{featureimage_line}---

{{{{< alert "warning" >}}}}
{legal_text}
{{{{</alert >}}}}

{{{{< gallery >}}}}
  <img src="/images/products/sierra/{model}.png" alt="Sierra Wireless {model.upper()}" />
{{{{</gallery >}}}}

## {h['產品概述']}

{overview}

## {h['主要特點']}

{features_bullets}

## {h['技術規格']}

| {translate_text("項目", lang) if lang != "zh-tw" else "項目"} | {translate_text("規格", lang) if lang != "zh-tw" else "規格"} |
|------|------|
{spec_table_lines}

## {os_section_label}

{os_table}

## {h['包裝內容']}

{package_lines}

## {h['資源與連結']}

| {translate_text("資源", lang) if lang != "zh-tw" else "資源"} | {translate_text("連結", lang) if lang != "zh-tw" else "連結"} |
|------|------|
{res_table}

---

{{{{< alert >}}}}
{cta_text}
{{{{</alert >}}}}
"""
    return content


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Project root: {base_dir}")

    for lang in LANGUAGES:
        print(f"\n{'='*60}")
        print(f"Processing: {lang}")
        print(f"{'='*60}")

        # Create directory
        sierra_dir = os.path.join(base_dir, "content", lang, "products", "sierra")
        os.makedirs(sierra_dir, exist_ok=True)
        print(f"  Directory: {sierra_dir}")

        # Generate overview page
        overview = generate_overview(lang)
        overview_path = os.path.join(sierra_dir, "_index.md")
        with open(overview_path, "w", encoding="utf-8") as f:
            f.write(overview)
        print(f"  Created overview: {overview_path}")

        # Generate product pages
        for model in PRODUCTS:
            prod_dir = os.path.join(sierra_dir, model)
            os.makedirs(prod_dir, exist_ok=True)

            page = generate_product_page(lang, model)
            prod_path = os.path.join(prod_dir, "_index.md")
            with open(prod_path, "w", encoding="utf-8") as f:
                f.write(page)
            print(f"  Created: {model.upper()} → {prod_path}")

    print(f"\n{'='*60}")
    print("Generation complete!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
