import os
import re

BASE_DIR = "/home/yopitek/Documents/Obsidian_vault/GX10_HQ/05_SW/yupitek_official_web/content"

LOCALES = {
    'zh-cn': {
        'overview_title': 'Sierra Wireless 蜂窝网络模组 (Semtech)',
        'overview_desc': '榆閤科技代理 Sierra Wireless (现为 Semtech) 工业级 5G NR 与 4G LTE M.2 及 Mini PCIe 通讯卡模组，提供高可靠度车载、物联网与工业网关解决方案。',
        'intro': 'Sierra Wireless（现隶属于 Semtech）是全球领先的物联网 (IoT) 与蜂窝网络通讯模组制造商。其 AirPrime® 系列 M.2 与 Mini PCIe 模组广泛应用于工业网关、车载资通讯 (Telematics)、公共安全网络 (FirstNet)、远程医疗及高可靠度关键任务设备。',
        'product_series': '产品系列',
        'cat_5g': '5G NR 旗舰模组',
        'cat_cat12': '4G LTE-Advanced Pro Cat 12',
        'cat_cat6': '4G LTE-Advanced Cat 6',
        'cat_cat3': '4G LTE Cat 3 工业网关模组 (Mini PCIe)',
        'spec_table_title': '📊 全系列 Sierra Wireless 网络卡规格比较表',
        'drivers_title': '驱动程序与固件支持',
        'drivers_desc': 'Sierra Wireless 模组官方驱动程序、MBIM/QMI 模式切换工具与最新 FOTA 固件请造访[技术支持页面](/zh-cn/support/)进行查询。',
        'cta_btn': '询问报价 / 批量采购 Sierra Wireless 模组 →',
        'alert_msg': '需要 Sierra Wireless 模组项目评估、极低延迟 5G 工业网关规格咨询或批量采购报价？请来信[与我们联系](/zh-cn/contact/)',
        'headers': ['型号', '蜂窝技术', '速度类别', '最高下载 / 上传', '外型介面 (Form Factor)', '目标市场', '主要支持频段与特色', 'GNSS 定位'],
        'h_overview': '产品概述',
        'h_features': '产品特色',
        'h_specs': '技术规格',
        'h_os': '操作系统与驱动支持',
        'h_docs': '资源与文件下载',
        'col_item': '项目',
        'col_details': '规格细节',
        'lbl_mfr': '制造商',
        'lbl_model': '产品型号',
        'lbl_tech': '蜂窝技术',
        'lbl_chip': '核心芯片组',
        'lbl_speed': '最高下载 / 上传速率',
        'lbl_lte': 'LTE 频段',
        'lbl_form': '外型尺寸',
        'lbl_host': '主机控制介面',
        'lbl_sim': 'SIM 卡介面',
        'lbl_temp': '作业温度',
        'lbl_cert': '电信认证',
        'mkt_global': '全球 Global',
        'mkt_americas': '美洲 Americas',
        'mkt_apac': '亚太 APAC',
        'mkt_emea': '美洲 / 欧洲',
        'os_table_header': '| 操作系统 | 支持状态 | 备注 |',
        'win_desc': '提供官方 Windows MBIM / QMI 驱动与 Skylight 连线管理软件',
        'lin_desc': '内核内置 qmi_wwan / cdc_mbim 驱动与 ModemManager',
        'and_desc': '提供 Android RIL 整合驱动',
        'supported': '✅ 支持',
    },
    'en': {
        'overview_title': 'Sierra Wireless Cellular Modules (Semtech)',
        'overview_desc': 'Yopitek distributes Sierra Wireless (now Semtech) industrial-grade 5G NR and 4G LTE M.2 and Mini PCIe cellular cards for telematics, IoT, and gateway applications.',
        'intro': 'Sierra Wireless (now part of Semtech) is a global leader in IoT and cellular communication modules. Its AirPrime® series M.2 and Mini PCIe modules are widely deployed in industrial gateways, telematics, public safety networks (FirstNet), telemedicine, and mission-critical systems.',
        'product_series': 'Product Line',
        'cat_5g': '5G NR Flagship Modules',
        'cat_cat12': '4G LTE-Advanced Pro Cat 12',
        'cat_cat6': '4G LTE-Advanced Cat 6',
        'cat_cat3': '4G LTE Cat 3 Industrial Modules (Mini PCIe)',
        'spec_table_title': '📊 Sierra Wireless Module Full Specification Comparison',
        'drivers_title': 'Driver & Firmware Support',
        'drivers_desc': 'For official Sierra Wireless drivers, MBIM/QMI mode switching utilities, and FOTA updates, please visit our [Technical Support](/en/support/) page.',
        'cta_btn': 'Inquire / Bulk Purchase Sierra Wireless Modules →',
        'alert_msg': 'Need Sierra Wireless module project evaluation or bulk purchase quote? Please [contact us](/en/contact/).',
        'headers': ['Model', 'Cellular Tech', 'Speed Category', 'Max Down / Up', 'Form Factor', 'Target Market', 'Supported Bands & Features', 'GNSS Positioning'],
        'h_overview': 'Product Overview',
        'h_features': 'Key Features',
        'h_specs': 'Technical Specifications',
        'h_os': 'OS & Driver Support',
        'h_docs': 'Resources & Downloads',
        'col_item': 'Item',
        'col_details': 'Specification Details',
        'lbl_mfr': 'Manufacturer',
        'lbl_model': 'Model',
        'lbl_tech': 'Cellular Technology',
        'lbl_chip': 'Chipset',
        'lbl_speed': 'Peak Data Rates',
        'lbl_lte': 'LTE Bands',
        'lbl_form': 'Form Factor',
        'lbl_host': 'Host Interfaces',
        'lbl_sim': 'SIM Interface',
        'lbl_temp': 'Operating Temperature',
        'lbl_cert': 'Certifications',
        'mkt_global': 'Global',
        'mkt_americas': 'Americas',
        'mkt_apac': 'APAC',
        'mkt_emea': 'Americas / EMEA',
        'os_table_header': '| Operating System | Support Status | Notes |',
        'win_desc': 'Official Windows MBIM / QMI drivers and Skylight Connection Manager',
        'lin_desc': 'Built-in Linux kernel qmi_wwan / cdc_mbim drivers & ModemManager',
        'and_desc': 'Android RIL integration drivers provided',
        'supported': '✅ Supported',
    },
    'ja': {
        'overview_title': 'Sierra Wireless セルラー通信モジュール (Semtech)',
        'overview_desc': 'Yopitekは Sierra Wireless (現 Semtech) 産業用 5G NR / 4G LTE M.2 および Mini PCIe モジュールの正規代理店です。',
        'intro': 'Sierra Wireless（現 Semtech）は、IoT およびセルラー通信モジュールのグローバルリーダーです。AirPrime® シリーズ M.2 および Mini PCIe モジュールは、産業用ゲートウェイ、テレマティクス、公共安全ネットワーク（FirstNet）などで幅広く採用されています。',
        'product_series': '製品ラインナップ',
        'cat_5g': '5G NR フラグシップモジュール',
        'cat_cat12': '4G LTE-Advanced Pro Cat 12',
        'cat_cat6': '4G LTE-Advanced Cat 6',
        'cat_cat3': '4G LTE Cat 3 産業用モジュール (Mini PCIe)',
        'spec_table_title': '📊 Sierra Wireless 全モデルスペック比較表',
        'drivers_title': 'ドライバー＆ファームウェアサポート',
        'drivers_desc': '公式ドライバー、MBIM/QMI モード切替ツールおよび最新ファームウェアは[技術サポートページ](/ja/support/)をご確認ください。',
        'cta_btn': '見積もり・一括購入のお問い合わせ →',
        'alert_msg': 'Sierra Wireless モジュールの導入評価や大口購入のお見積もりは、お気軽に[お問い合わせ](/ja/contact/)ください。',
        'headers': ['型番', 'セルラー技術', '通信カテゴリ', '最大速度 下り/上り', 'フォームファクタ', '対象市場', '対応周波数帯＆特徴', 'GNSS 位置測位'],
        'h_overview': '製品概要',
        'h_features': '主な特徴',
        'h_specs': '技術仕様',
        'h_os': '対応OS・ドライバー',
        'h_docs': 'リソース・資料ダウンロード',
        'col_item': '項目',
        'col_details': '仕様詳細',
        'lbl_mfr': '製造元',
        'lbl_model': '型番',
        'lbl_tech': 'セルラー技術',
        'lbl_chip': 'チップセット',
        'lbl_speed': '最大伝送速度',
        'lbl_lte': 'LTE バンド',
        'lbl_form': 'フォームファクタ',
        'lbl_host': 'ホストインターフェース',
        'lbl_sim': 'SIM インターフェース',
        'lbl_temp': '動作温度',
        'lbl_cert': '認証',
        'mkt_global': 'グローバル (Global)',
        'mkt_americas': '北米・南米 (Americas)',
        'mkt_apac': 'アジア太平洋 (APAC)',
        'mkt_emea': '米州・欧州 (Americas/EMEA)',
        'os_table_header': '| オペレーティングシステム | サポート状態 | 備考 |',
        'win_desc': '公式 Windows MBIM / QMI ドライバーおよび Skylight コネクションマネージャー',
        'lin_desc': 'Linux カーネル標準 qmi_wwan / cdc_mbim ドライバーおよび ModemManager',
        'and_desc': 'Android RIL 統合ドライバー対応',
        'supported': '✅ 対応',
    },
    'ar': {
        'overview_title': 'وحدات Sierra Wireless الخلوية (Semtech)',
        'overview_desc': 'تقدم Yopitek وحدات Sierra Wireless (الآن Semtech) الصناعية بدرجة 5G NR و 4G LTE بصيغة M.2 و Mini PCIe.',
        'intro': 'تُعد Sierra Wireless (التابعة حاليًا لشركة Semtech) رائدة عالمية في وحدات الاتصالات الخلوية وإنترنت الأشياء (IoT). وتُستخدم وحدات AirPrime® بصيغة M.2 و Mini PCIe على نطاق واسع في البوابات الصناعية، ونظم معلومات المركبات، وشبكات السلامة العامة (FirstNet).',
        'product_series': 'سلسلة المنتجات',
        'cat_5g': 'وحدات 5G NR الرائدة',
        'cat_cat12': '4G LTE-Advanced Pro Cat 12',
        'cat_cat6': '4G LTE-Advanced Cat 6',
        'cat_cat3': 'وحدات 4G LTE Cat 3 الصناعية (Mini PCIe)',
        'spec_table_title': '📊 جدول مقارنة مواصفات وحدات Sierra Wireless',
        'drivers_title': 'دعم برامج التشغيل والبرامج الثابتة',
        'drivers_desc': 'للحصول على برامج التشغيل الرسمية وتحديثات الفيرموير لـ Sierra Wireless، يرجى زيارة [صفحة الدعم الفني](/ar/support/).',
        'cta_btn': 'طلب عرض أسعار / شراء بالجملة →',
        'alert_msg': 'هل تحتاج إلى تقييم مشروع أو عرض أسعار لشراء وحدات Sierra Wireless؟ يرجى [التواصل معنا](/ar/contact/).',
        'headers': ['الموديل', 'التقنية الخلوية', 'فئة السرعة', 'أقصى تنزيل / رفع', 'عامل الشكل', 'السوق المستهدف', 'النطاقات المدعومة والميزات', 'نظام تحديد المواقع GNSS'],
        'h_overview': 'نظرة عامة على المنتج',
        'h_features': 'الميزات الرئيسية',
        'h_specs': 'المواصفات الفنية',
        'h_os': 'دعم أنظمة التشغيل وبرامج التشغيل',
        'h_docs': 'الموارد والتنزيلات',
        'col_item': 'العنصر',
        'col_details': 'تفاصيل المواصفات',
        'lbl_mfr': 'الشركة المصنعة',
        'lbl_model': 'الموديل',
        'lbl_tech': 'التقنية الخلوية',
        'lbl_chip': 'الشريحة الرئيسية',
        'lbl_speed': 'أقصى سرعة نقل',
        'lbl_lte': 'نطاقات LTE',
        'lbl_form': 'عامل الشكل',
        'lbl_host': 'واجهات الجهاز',
        'lbl_sim': 'واجهة SIM',
        'lbl_temp': 'درجة حرارة التشغيل',
        'lbl_cert': 'الاعتمادات',
        'mkt_global': 'عالمي Global',
        'mkt_americas': 'الأمريكتان Americas',
        'mkt_apac': 'آسيا والمحيط الهادئ APAC',
        'mkt_emea': 'الأمريكتان / أوروبا EMEA',
        'os_table_header': '| نظام التشغيل | حالة الدعم | ملاحظات |',
        'win_desc': 'برامج تشغيل Windows MBIM / QMI الرسمية وبرنامج Skylight',
        'lin_desc': 'برامج تشغيل Linux kernel qmi_wwan / cdc_mbim المدمجة',
        'and_desc': 'توفير برامج تشغيل Android RIL',
        'supported': '✅ مدعوم',
    },
    'es': {
        'overview_title': 'Módulos Celulares Sierra Wireless (Semtech)',
        'overview_desc': 'Yopitek distribuye módulos celulares industriales Sierra Wireless (Semtech) 5G NR y 4G LTE en formato M.2 y Mini PCIe.',
        'intro': 'Sierra Wireless (ahora parte de Semtech) es un líder mundial en módulos de comunicación celular para IoT. Sus módulos M.2 y Mini PCIe de la serie AirPrime® se implementan ampliamente en puertas de enlace industriales, telemática y redes de seguridad pública (FirstNet).',
        'product_series': 'Línea de Productos',
        'cat_5g': 'Módulos Insignia 5G NR',
        'cat_cat12': '4G LTE-Advanced Pro Cat 12',
        'cat_cat6': '4G LTE-Advanced Cat 6',
        'cat_cat3': 'Módulos Industriales 4G LTE Cat 3 (Mini PCIe)',
        'spec_table_title': '📊 Tabla Comparativa de Especificaciones Sierra Wireless',
        'drivers_title': 'Soporte de Controladores y Firmware',
        'drivers_desc': 'Para descargar controladores oficiales Sierra Wireless y utilidades de modo MBIM/QMI, visite nuestra página de [Soporte Técnico](/es/support/).',
        'cta_btn': 'Solicitar Cotización / Compra al por Mayor →',
        'alert_msg': '¿Necesita evaluación de proyectos o cotización al por mayor para módulos Sierra Wireless? Por favor [contáctenos](/es/contact/).',
        'headers': ['Modelo', 'Tecnología Celular', 'Categoría de Velocidad', 'Máx Descarga / Carga', 'Factor de Forma', 'Mercado Objetivo', 'Bandas y Características', 'Posicionamiento GNSS'],
        'h_overview': 'Descripción General',
        'h_features': 'Características Principales',
        'h_specs': 'Especificaciones Técnicas',
        'h_os': 'Soporte de SO y Controladores',
        'h_docs': 'Recursos y Descargas',
        'col_item': 'Elemento',
        'col_details': 'Detalles de Especificación',
        'lbl_mfr': 'Fabricante',
        'lbl_model': 'Modelo',
        'lbl_tech': 'Tecnología Celular',
        'lbl_chip': 'Chipset',
        'lbl_speed': 'Velocidades Máximas',
        'lbl_lte': 'Bandas LTE',
        'lbl_form': 'Factor de Forma',
        'lbl_host': 'Interfaces del Host',
        'lbl_sim': 'Interfaz SIM',
        'lbl_temp': 'Temperatura de Operación',
        'lbl_cert': 'Certificaciones',
        'mkt_global': 'Global',
        'mkt_americas': 'Américas',
        'mkt_apac': 'APAC',
        'mkt_emea': 'Américas / EMEA',
        'os_table_header': '| Sistema Operativo | Estado de Soporte | Notas |',
        'win_desc': 'Controladores oficiales Windows MBIM / QMI y gestor Skylight',
        'lin_desc': 'Controladores qmi_wwan / cdc_mbim integrados en kernel Linux',
        'and_desc': 'Controladores de integración Android RIL proporcionados',
        'supported': '✅ Soportado',
    },
    'pt': {
        'overview_title': 'Módulos Celulares Sierra Wireless (Semtech)',
        'overview_desc': 'A Yopitek distribui módulos celulares industriais Sierra Wireless (Semtech) 5G NR e 4G LTE nos formatos M.2 e Mini PCIe.',
        'intro': 'A Sierra Wireless (agora parte da Semtech) é líder mundial em módulos de comunicação celular IoT. Seus módulos das séries AirPrime® M.2 e Mini PCIe são amplamente aplicados em gateways industriais, telemática e redes de segurança pública (FirstNet).',
        'product_series': 'Linha de Produtos',
        'cat_5g': 'Módulos Flagship 5G NR',
        'cat_cat12': '4G LTE-Advanced Pro Cat 12',
        'cat_cat6': '4G LTE-Advanced Cat 6',
        'cat_cat3': 'Módulos Industriais 4G LTE Cat 3 (Mini PCIe)',
        'spec_table_title': '📊 Tabela Comparativa de Especificações Sierra Wireless',
        'drivers_title': 'Suporte de Drivers e Firmware',
        'drivers_desc': 'Para drivers oficiais Sierra Wireless e utilitários de modo MBIM/QMI, visite nossa página de [Suporte Técnico](/pt/support/).',
        'cta_btn': 'Solicitar Cotação / Compra em Lote →',
        'alert_msg': 'Precisa de avaliação de projetos ou cotação em lote para módulos Sierra Wireless? Por favor [entre em contato](/pt/contact/).',
        'headers': ['Modelo', 'Tecnologia Celular', 'Categoria de Velocidade', 'Máx Download / Upload', 'Fator de Forma', 'Mercado Alvo', 'Bandas Suportadas e Recursos', 'Posicionamento GNSS'],
        'h_overview': 'Visão Geral do Produto',
        'h_features': 'Recursos Principais',
        'h_specs': 'Especificações Técnicas',
        'h_os': 'Suporte a SO e Drivers',
        'h_docs': 'Recursos e Downloads',
        'col_item': 'Item',
        'col_details': 'Detalhes da Especificação',
        'lbl_mfr': 'Fabricante',
        'lbl_model': 'Modelo',
        'lbl_tech': 'Tecnologia Celular',
        'lbl_chip': 'Chipset',
        'lbl_speed': 'Taxas de Transmissão Máximas',
        'lbl_lte': 'Bandas LTE',
        'lbl_form': 'Fator de Forma',
        'lbl_host': 'Interfaces Host',
        'lbl_sim': 'Interface SIM',
        'lbl_temp': 'Temperatura de Operação',
        'lbl_cert': 'Certificações',
        'mkt_global': 'Global',
        'mkt_americas': 'Américas',
        'mkt_apac': 'APAC',
        'mkt_emea': 'Américas / EMEA',
        'os_table_header': '| Sistema Operacional | Status de Suporte | Notas |',
        'win_desc': 'Drivers oficiais Windows MBIM / QMI e gerenciador Skylight',
        'lin_desc': 'Drivers qmi_wwan / cdc_mbim integrados no kernel Linux',
        'and_desc': 'Drivers de integração Android RIL fornecidos',
        'supported': '✅ Suportado',
    },
    'ru': {
        'overview_title': 'Сотовые модули Sierra Wireless (Semtech)',
        'overview_desc': 'Yopitek поставляет промышленные сотовые модули Sierra Wireless (Semtech) 5G NR и 4G LTE в форматах M.2 и Mini PCIe.',
        'intro': 'Sierra Wireless (ныне в составе Semtech) — мировой лидер в производстве модулей сотовой связи для IoT. Модули AirPrime® M.2 и Mini PCIe широко используются в промышленных шлюзах, телематике и сетях уровне первой необходимости.',
        'product_series': 'Серия продуктов',
        'cat_5g': 'Флагманские модули 5G NR',
        'cat_cat12': '4G LTE-Advanced Pro Cat 12',
        'cat_cat6': '4G LTE-Advanced Cat 6',
        'cat_cat3': 'Промышленные модули 4G LTE Cat 3 (Mini PCIe)',
        'spec_table_title': '📊 Сравнительная таблица характеристик Sierra Wireless',
        'drivers_title': 'Поддержка драйверов и прошивок',
        'drivers_desc': 'Официальные драйверы Sierra Wireless и утилиты переключения режимов MBIM/QMI доступны на [странице техподдержки](/ru/support/).',
        'cta_btn': 'Запросить цену / Оптовая закупка →',
        'alert_msg': 'Требуется консультация по проектам или оптовая закупка модулей Sierra Wireless? [Свяжитесь с нами](/ru/contact/).',
        'headers': ['Модель', 'Сотовая технология', 'Категория скорости', 'Макс Скачивание / Загрузка', 'Форм-фактор', 'Целевой рынок', 'Поддерживаемые диапазоны', 'Спутниковая навигация GNSS'],
        'h_overview': 'Обзор продукта',
        'h_features': 'Основные характеристики',
        'h_specs': 'Технические характеристики',
        'h_os': 'Поддержка ОС и драйверов',
        'h_docs': 'Ресурсы и документация',
        'col_item': 'Параметр',
        'col_details': 'Значение',
        'lbl_mfr': 'Производитель',
        'lbl_model': 'Модель',
        'lbl_tech': 'Технология сотовой связи',
        'lbl_chip': 'Чипсет',
        'lbl_speed': 'Максимальная скорость',
        'lbl_lte': 'Диапазоны LTE',
        'lbl_form': 'Форм-фактор',
        'lbl_host': 'Интерфейсы',
        'lbl_sim': 'Интерфейс SIM',
        'lbl_temp': 'Рабочая температура',
        'lbl_cert': 'Сертификаты',
        'mkt_global': 'Глобальный (Global)',
        'mkt_americas': 'Америка (Americas)',
        'mkt_apac': 'АТР (APAC)',
        'mkt_emea': 'Америка / Европа (EMEA)',
        'os_table_header': '| Операционная система | Статус поддержки | Примечания |',
        'win_desc': 'Официальные драйверы Windows MBIM / QMI и менеджер Skylight',
        'lin_desc': 'Встроенные драйверы ядра Linux qmi_wwan / cdc_mbim',
        'and_desc': 'Предоставляются драйверы интеграции Android RIL',
        'supported': '✅ Поддерживается',
    },
    'de': {
        'overview_title': 'Sierra Wireless Mobilfunkmodule (Semtech)',
        'overview_desc': 'Yopitek vertreibt industrielle Sierra Wireless (Semtech) 5G NR- und 4G LTE M.2 sowie Mini PCIe-Mobilfunkmodule.',
        'intro': 'Sierra Wireless (jetzt Teil von Semtech) ist ein weltweit führender Anbieter von Mobilfunkmodulen für das IoT. Die M.2- und Mini PCIe-Module der AirPrime®-Serie kommen in Industrie-Gateways, Telematik und öffentlichen Sicherheitsnetzen (FirstNet) zum Einsatz.',
        'product_series': 'Produktreihe',
        'cat_5g': '5G NR Flaggschiff-Module',
        'cat_cat12': '4G LTE-Advanced Pro Cat 12',
        'cat_cat6': '4G LTE-Advanced Cat 6',
        'cat_cat3': '4G LTE Cat 3 Industrie-Module (Mini PCIe)',
        'spec_table_title': '📊 Sierra Wireless Modul-Spezifikationsvergleich',
        'drivers_title': 'Treiber- & Firmware-Unterstützung',
        'drivers_desc': 'Offizielle Sierra Wireless Treiber und MBIM/QMI-Tools finden Sie auf unserer [Support-Seite](/de/support/).',
        'cta_btn': 'Angebot anfordern / Großabnahme →',
        'alert_msg': 'Benötigen Sie eine Projektbewertung oder ein Großabnahme-Angebot für Sierra Wireless Module? Bitte [kontaktieren Sie uns](/de/contact/).',
        'headers': ['Modell', 'Mobilfunktechnik', 'Geschwindigkeitskategorie', 'Max Download / Upload', 'Formfaktor', 'Zielmarkt', 'Unterstützte Frequenzen & Features', 'GNSS-Ortung'],
        'h_overview': 'Produktübersicht',
        'h_features': 'Hauptmerkmale',
        'h_specs': 'Technische Daten',
        'h_os': 'OS- & Treiber-Unterstützung',
        'h_docs': 'Ressourcen & Downloads',
        'col_item': 'Eigenschaft',
        'col_details': 'Spezifikation',
        'lbl_mfr': 'Hersteller',
        'lbl_model': 'Modell',
        'lbl_tech': 'Mobilfunktechnologie',
        'lbl_chip': 'Chipsatz',
        'lbl_speed': 'Max. Datenrate',
        'lbl_lte': 'LTE-Bänder',
        'lbl_form': 'Formfaktor',
        'lbl_host': 'Host-Schnittstellen',
        'lbl_sim': 'SIM-Schnittstelle',
        'lbl_temp': 'Betriebstemperatur',
        'lbl_cert': 'Zertifizierungen',
        'mkt_global': 'Global',
        'mkt_americas': 'Amerika (Americas)',
        'mkt_apac': 'APAC',
        'mkt_emea': 'Amerika / EMEA',
        'os_table_header': '| Betriebssystem | Unterstützungsstatus | Hinweise |',
        'win_desc': 'Offizielle Windows MBIM / QMI Treiber und Skylight Connection Manager',
        'lin_desc': 'Integrierte Linux-Kernel-Treiber qmi_wwan / cdc_mbim',
        'and_desc': 'Android RIL-Treiber verfügbar',
        'supported': '✅ Unterstützt',
    },
    'fr': {
        'overview_title': 'Modules Cellulaires Sierra Wireless (Semtech)',
        'overview_desc': 'Yopitek distribue les modules cellulaires industriels Sierra Wireless (Semtech) 5G NR et 4G LTE au format M.2 et Mini PCIe.',
        'intro': 'Sierra Wireless (faisant désormais partie de Semtech) est un leader mondial des modules de communication cellulaire IoT. Ses modules AirPrime® M.2 et Mini PCIe sont largement déployés dans les passerelles industrielles, la télématique et les réseaux de sécurité publique (FirstNet).',
        'product_series': 'Gamme de Produits',
        'cat_5g': 'Modules Amiraux 5G NR',
        'cat_cat12': '4G LTE-Advanced Pro Cat 12',
        'cat_cat6': '4G LTE-Advanced Cat 6',
        'cat_cat3': 'Modules Industriels 4G LTE Cat 3 (Mini PCIe)',
        'spec_table_title': '📊 Tableau Comparatif des Spécifications Sierra Wireless',
        'drivers_title': 'Support Pilotes & Firmware',
        'drivers_desc': 'Pour les pilotes officiels Sierra Wireless et les utilitaires MBIM/QMI, visitez notre page de [Support Technique](/fr/support/).',
        'cta_btn': 'Demander un Devis / Achat en Volume →',
        'alert_msg': 'Besoin d’une évaluation de projet ou d’un devis pour des modules Sierra Wireless ? Veuillez [nous contacter](/fr/contact/).',
        'headers': ['Modèle', 'Technologie Cellulaire', 'Catégorie de Vitesse', 'Max Débit Descendant / Montant', 'Facteur de Forme', 'Marché Cible', 'Bandes & Caractéristiques', 'Positionnement GNSS'],
        'h_overview': 'Présentation du Produit',
        'h_features': 'Caractéristiques Principales',
        'h_specs': 'Spécifications Techniques',
        'h_os': 'Support OS & Pilotes',
        'h_docs': 'Ressources & Téléchargements',
        'col_item': 'Élément',
        'col_details': 'Détails',
        'lbl_mfr': 'Fabricant',
        'lbl_model': 'Modèle',
        'lbl_tech': 'Technologie Cellulaire',
        'lbl_chip': 'Chipset',
        'lbl_speed': 'Débits Maximaux',
        'lbl_lte': 'Bandes LTE',
        'lbl_form': 'Facteur de Forme',
        'lbl_host': 'Interfaces Hôte',
        'lbl_sim': 'Interface SIM',
        'lbl_temp': 'Température de Fonctionnement',
        'lbl_cert': 'Certifications',
        'mkt_global': 'Mondial (Global)',
        'mkt_americas': 'Amériques',
        'mkt_apac': 'APAC',
        'mkt_emea': 'Amériques / EMEA',
        'os_table_header': '| Système d’Exploitation | Statut du Support | Remarques |',
        'win_desc': 'Pilotes officiels Windows MBIM / QMI et logiciel Skylight',
        'lin_desc': 'Pilotes noyau Linux qmi_wwan / cdc_mbim intégrés',
        'and_desc': 'Pilotes d’intégration Android RIL fournis',
        'supported': '✅ Supporté',
    }
}

PRODUCTS = ["em7430", "em7455", "em7511", "em7565", "em9190", "em9191", "mc7304", "mc7350", "mc7354", "mc7455"]

def generate_overview_page(loc):
    cfg = LOCALES[loc]
    is_rtl = (loc == 'ar')
    rtl_frontmatter = 'dir: "rtl"\n' if is_rtl else ''

    content = f"""---
title: "{cfg['overview_title']}"
description: "{cfg['overview_desc']}"
date: 2026-07-29
draft: false
showBreadcrumbs: true
showTableOfContents: false
showChildPages: false
{rtl_frontmatter}featureimage: "/images/products/sierra/EM9190-5G.png"
---

{cfg['intro']}

---

## {cfg['product_series']}

### {cfg['cat_5g']}

{{{{< card-group >}}}}
  {{{{< card title="Sierra Wireless EM9190" href="/{loc}/products/sierra/em9190/" image="/images/products/sierra/EM9190-5G.png" >}}}}
    5G NR Sub-6 + mmWave, 5.5 Gbps Down / 3 Gbps Up, M.2 3042, Snapdragon X55, SA/NSA & CBRS.
  {{{{< /card >}}}}
  {{{{< card title="Sierra Wireless EM9191" href="/{loc}/products/sierra/em9191/" image="/images/products/sierra/EM9191-5G.png" >}}}}
    5G NR Sub-6, 4.5 Gbps Down, M.2 3042, Snapdragon X55, Global Bands, -40°C~+85°C.
  {{{{< /card >}}}}
{{{{< /card-group >}}}}

### {cfg['cat_cat12']}

{{{{< card-group >}}}}
  {{{{< card title="Sierra Wireless EM7511" href="/{loc}/products/sierra/em7511/" image="/images/products/sierra/EM7511.png" >}}}}
    4G LTE Cat 12 Americas, 600 Mbps / 150 Mbps, M.2 3042, FirstNet Band 14, CBRS & LAA.
  {{{{< /card >}}}}
  {{{{< card title="Sierra Wireless EM7565" href="/{loc}/products/sierra/em7565/" image="/images/products/sierra/EM7565.png" >}}}}
    4G LTE Cat 12 Global, 600 Mbps, M.2 3042, 24+ Global LTE Bands, CBRS & LAA.
  {{{{< /card >}}}}
{{{{< /card-group >}}}}

### {cfg['cat_cat6']}

{{{{< card-group >}}}}
  {{{{< card title="Sierra Wireless EM7430" href="/{loc}/products/sierra/em7430/" image="/images/products/sierra/EM7430.png" >}}}}
    4G LTE Cat 6 APAC, 300 Mbps / 50 Mbps, M.2 3042, Qualcomm MDM9230.
  {{{{< /card >}}}}
  {{{{< card title="Sierra Wireless EM7455" href="/{loc}/products/sierra/em7455/" image="/images/products/sierra/EM7455.png" >}}}}
    4G LTE Cat 6 Americas/EMEA, 300 Mbps, M.2 3042, Qualcomm MDM9230.
  {{{{< /card >}}}}
  {{{{< card title="Sierra Wireless MC7455" href="/{loc}/products/sierra/mc7455/" image="/images/products/sierra/MC7455.png" >}}}}
    4G LTE Cat 6 Mini PCIe, 300 Mbps, Americas/EMEA.
  {{{{< /card >}}}}
{{{{< /card-group >}}}}

### {cfg['cat_cat3']}

{{{{< card-group >}}}}
  {{{{< card title="Sierra Wireless MC7304" href="/{loc}/products/sierra/mc7304/" image="/images/products/sierra/MC7304.png" >}}}}
    4G LTE Cat 3 EMEA/APAC, 100 Mbps / 50 Mbps, Mini PCIe, 3G/2G Fallback.
  {{{{< /card >}}}}
  {{{{< card title="Sierra Wireless MC7350" href="/{loc}/products/sierra/mc7350/" image="/images/products/sierra/MC7350.png" >}}}}
    4G LTE Cat 3 North America AT&T, Mini PCIe, 100 Mbps, Qualcomm MDM9215.
  {{{{< /card >}}}}
  {{{{< card title="Sierra Wireless MC7354" href="/{loc}/products/sierra/mc7354/" image="/images/products/sierra/MC7354.png" >}}}}
    4G LTE Cat 3 North America Multi-carrier (Verizon/Sprint/AT&T), Mini PCIe, 100 Mbps.
  {{{{< /card >}}}}
{{{{< /card-group >}}}}

---

## {cfg['spec_table_title']}

| {cfg['headers'][0]} | {cfg['headers'][1]} | {cfg['headers'][2]} | {cfg['headers'][3]} | {cfg['headers'][4]} | {cfg['headers'][5]} | {cfg['headers'][6]} | {cfg['headers'][7]} |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **EM9190** | 5G NR / 4G LTE | 5G Sub-6 + mmWave | 5.5 Gbps / 3.0 Gbps | M.2 3042 | {cfg['mkt_global']} | n1/2/3/5/7/8/12/20/28/41/48/77/78/79, mmWave (n257-n261), CBRS | L1+L5 Dual-Band GNSS |
| **EM9191** | 5G NR / 4G LTE | 5G Sub-6 | 4.5 Gbps / 660 Mbps | M.2 3042 | {cfg['mkt_global']} | n1/2/3/5/7/8/12/20/28/41/48/77/78/79, CBRS, SA/NSA | Multi-constellation |
| **EM7511** | 4G LTE-A Pro / 3G | LTE Cat 12 | 600 Mbps / 150 Mbps | M.2 3042 | {cfg['mkt_americas']} | B1-B14, B18-B20, B26, B29, B30, B32, B41-B43, B46(LAA), B48(CBRS), Band 14 FirstNet | GPS/GLONASS/Beidou/Galileo |
| **EM7565** | 4G LTE-A Pro / 3G | LTE Cat 12 | 600 Mbps / 150 Mbps | M.2 3042 | {cfg['mkt_global']} | B1-B9, B12, B13, B18-B20, B26, B28-B30, B32, B41-B43, B46(LAA), B48(CBRS), B66 | GPS/GLONASS/Beidou/Galileo |
| **EM7430** | 4G LTE-A / 3G | LTE Cat 6 | 300 Mbps / 50 Mbps | M.2 3042 | {cfg['mkt_apac']} | B1, B3, B5, B7, B8, B18, B19, B21, B28, B38, B39, B40, B41 | GPS/GLONASS/Beidou/Galileo |
| **EM7455** | 4G LTE-A / 3G | LTE Cat 6 | 300 Mbps / 50 Mbps | M.2 3042 | {cfg['mkt_emea']} | B1-B5, B7, B8, B12, B13, B20, B25, B26, B29, B30, B41 | GPS/GLONASS/Beidou/Galileo |
| **MC7455** | 4G LTE-A / 3G | LTE Cat 6 | 300 Mbps / 50 Mbps | Mini PCIe | {cfg['mkt_emea']} | B1-B5, B7, B8, B12, B13, B20, B25, B26, B29, B30, B41 | GPS/GLONASS/Beidou/Galileo |
| **MC7304** | 4G LTE / 3G / 2G | LTE Cat 3 | 100 Mbps / 50 Mbps | Mini PCIe | {cfg['mkt_emea']} | B1, B3, B7, B8, B20 (3G/2G Fallback) | Standalone GPS / GLONASS |
| **MC7350** | 4G LTE / 3G | LTE Cat 3 | 100 Mbps / 50 Mbps | Mini PCIe | North America (AT&T) | B2, B4, B5, B17, B25 | Standalone GPS / GLONASS |
| **MC7354** | 4G LTE / 3G / CDMA | LTE Cat 3 | 100 Mbps / 50 Mbps | Mini PCIe | North America Multi-carrier | B2, B4, B5, B13, B17, B25, EV-DO Rev A / CDMA | Standalone GPS / GLONASS |

---

## {cfg['drivers_title']}

{cfg['drivers_desc']}

---

<div class="mt-6 text-center">
  <a href="/{loc}/contact/" class="btn-inquiry">{cfg['cta_btn']}</a>
</div>

{{{{< alert >}}}}
{cfg['alert_msg']}
{{{{< /alert >}}}}
"""
    target_path = os.path.join(BASE_DIR, loc, "products/sierra/_index.md")
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_product_page(loc, p):
    cfg = LOCALES[loc]
    is_rtl = (loc == 'ar')
    rtl_frontmatter = 'dir: "rtl"\n' if is_rtl else ''

    zh_path = os.path.join(BASE_DIR, "zh-tw/products/sierra", p, "_index.md")
    with open(zh_path, "r", encoding="utf-8") as f:
        src = f.read()

    # Replace section headers
    src = src.replace("## 產品概述", f"## {cfg['h_overview']}")
    src = src.replace("## 產品特色", f"## {cfg['h_features']}")
    src = src.replace("## 技術規格", f"## {cfg['h_specs']}")
    src = src.replace("## 作業系統與驅動支援", f"## {cfg['h_os']}")
    src = src.replace("## 資源與文件下載", f"## {cfg['h_docs']}")

    src = src.replace("| 項目 | 規格細節 |", f"| {cfg['col_item']} | {cfg['col_details']} |")
    src = src.replace("**製造商**", f"**{cfg['lbl_mfr']}**")
    src = src.replace("**產品型號**", f"**{cfg['lbl_model']}**")
    src = src.replace("**蜂窩技術**", f"**{cfg['lbl_tech']}**")
    src = src.replace("**核心晶片組**", f"**{cfg['lbl_chip']}**")
    src = src.replace("**最高下載 / 上傳速率**", f"**{cfg['lbl_speed']}**")
    src = src.replace("**LTE 頻段**", f"**{cfg['lbl_lte']}**")
    src = src.replace("**外型尺寸**", f"**{cfg['lbl_form']}**")
    src = src.replace("**主機介面**", f"**{cfg['lbl_host']}**")
    src = src.replace("**SIM 卡介面**", f"**{cfg['lbl_sim']}**")
    src = src.replace("**作業溫度**", f"**{cfg['lbl_temp']}**")

    # Replace OS table headers and descriptions
    src = src.replace("| 作業系統 | 支援狀態 | 備註 |", cfg['os_table_header'])
    src = src.replace("提供官方 Windows MBIM / QMI 驅動與 Skylight 連線管理軟體", cfg['win_desc'])
    src = src.replace("提供官方 Windows MBIM / QMI 驅動軟體包", cfg['win_desc'])
    src = src.replace("內建 Linux Kernel qmi_wwan / cdc_mbim 核心驅動與 ModemManager", cfg['lin_desc'])
    src = src.replace("核心內建 `qmi_wwan` / `cdc_mbim` 驅動", cfg['lin_desc'])
    src = src.replace("提供 Android RIL 整合驅動與範例庫", cfg['and_desc'])
    src = src.replace("支援 Android RIL 架構", cfg['and_desc'])
    src = src.replace("✅ 支援", cfg['supported'])

    # Replace alert message
    src = re.sub(r'\{\{< alert >\}\}[\s\S]*?\{\{< /alert >\}\}', f"{{{{< alert >}}}}\n{cfg['alert_msg']}\n{{{{< /alert >}}}}", src)

    # Insert RTL frontmatter if AR
    if is_rtl:
        src = src.replace("showTableOfContents: true\n", "showTableOfContents: true\ndir: \"rtl\"\n")

    # Fix contact links for specific locale
    src = src.replace("/zh-tw/contact/", f"/{loc}/contact/")

    target_path = os.path.join(BASE_DIR, loc, f"products/sierra/{p}/_index.md")
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(src)

def main():
    for loc in LOCALES:
        print(f"Generating localized pages for locale: {loc}...")
        generate_overview_page(loc)
        for p in PRODUCTS:
            generate_product_page(loc, p)
    print("All localized pages successfully generated!")

if __name__ == "__main__":
    main()
