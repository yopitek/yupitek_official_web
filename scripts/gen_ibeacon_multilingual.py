#!/usr/bin/env python3
import os
import re

LANGUAGES = ["zh-tw", "zh-cn", "ja", "ar", "de", "es", "fr", "pt", "ru"]

# Localized titles and descriptions for the main iBeacon landing page
LANDING_INFO = {
    "zh-tw": {
        "title": "Yupitek iBeacon 系列 — BLE 5.0 藍牙信標",
        "desc": "Yupitek 代理專業 BLE 5.0 iBeacon 與 Eddystone 藍牙信標：YPB01、YPB02、YPB03、YPB04、YPB05，適用於室內定位、考勤打卡與資產追蹤。",
        "intro": "Yupitek iBeacon 產品代表了新一代藍牙低功耗 (BLE 5.0) 信標裝置，專為高性能定位、人員追蹤和商業廣告推播而設計。支援 Apple iBeacon™ 和 Google Eddystone™ (UID, URL, TLM) 協定，我們的信標支援多協定同時廣播（最多 6 個通道），並可透過 BeaconSET+ 行動 App 進行配置。",
        "topo_title": "藍牙信標系統架構",
        "topo_desc": "我們的 iBeacon 生態系統將物理位置與企業雲端網路連接起來。信標以定期時間間隔發射 BLE 無線訊號，這些訊號由行動裝置（執行企業 App）和 BLE 閘道掃描，並將安全日誌轉發到中央考勤和資產追蹤系統。",
        "prod_title": "產品線",
        "comp_title": "iBeacon 系列規格比較",
        "card_desc": "專業 BLE 5.0 信標，適用於室內定位、智慧考勤打卡、人員管理與資產追蹤。",
        "cta": "需要專屬報價或客製化解決方案？請直接來信聯絡我們的銷售團隊：**sales@yupitek.com**",
        "headers": ["型號", "外觀特徵", "電源規格", "電池容量 / 壽命", "最大距離", "感測器", "防水等級", "特殊功能"],
        "rows": [
            ["YPB01", "硬幣型 / 圓形", "可更換 CR2477", "1000 mAh (2年以上)", "100 米", "無", "IP67", "旋轉式外殼，內部電源按鈕"],
            ["YPB02", "硬幣型 / 圓形", "可更換 CR2477", "1000 mAh (2年以上)", "100 米", "LIS3DH 三軸加速度計", "IP67", "運動觸發廣播，跌落警報"],
            ["YPB03", "方形 / 壁掛式", "4 × AA 乾電池", "5800 mAh (最長10年)", "240 米", "無", "IP65", "工業級壽命，外部按鈕，安裝支架"],
            ["YPB04", "超薄卡片 / 胸卡", "充電式鋰聚合物", "270 mAh (3個月)", "150 米", "三軸加速度計", "IP67", "震動馬達，1個RGB LED，外部按鈕，選配RFID"],
            ["YPB05", "Micro USB 轉接器", "USB 接口 (無電池)", "持續供電 (外部電源)", "50 米", "無", "無", "超輕量 (2.0g)，隨插即用，支援軟體重啟"]
        ]
    },
    "zh-cn": {
        "title": "Yupitek iBeacon 系列 — BLE 5.0 蓝牙信标",
        "desc": "Yupitek 代理专业 BLE 5.0 iBeacon 与 Eddystone 蓝牙信标：YPB01、YPB02、YPB03、YPB04、YPB05，适用于室内定位、考勤打卡与资产追踪。",
        "intro": "Yupitek iBeacon 产品代表了新一代蓝牙低功耗 (BLE 5.0) 信标设备，专为高性能定位、人员追踪和商业广告推送而设计。支持 Apple iBeacon™ 和 Google Eddystone™ (UID, URL, TLM) 协议，我们的信标支持多协议同时广播（最多 6 个通道），并可轻松通过 BeaconSET+ 移动 App 进行配置。",
        "topo_title": "蓝牙信标系统架构",
        "topo_desc": "我们的 iBeacon 生态系统将物理位置与企业云网络连接起来。信标以定期时间间隔发射 BLE 无线信号，这些信号由移动设备（运行企业 App）和 BLE 网关扫描，并将安全日志转发到中央考勤和资产追踪系统。",
        "prod_title": "产品线",
        "comp_title": "iBeacon 系列规格比较",
        "card_desc": "专业 BLE 5.0 信标，适用于室内定位、智能考勤打卡、人员管理与资产追踪。",
        "cta": "需要专属报价或定制化解决方案？请直接来信联系我们的销售团队：**sales@yupitek.com**",
        "headers": ["型号", "外观特征", "电源规格", "电池容量 / 寿命", "最大距离", "传感器", "防水等级", "特殊功能"],
        "rows": [
            ["YPB01", "硬币型 / 圆形", "可更换 CR2477", "1000 mAh (2年以上)", "100 米", "无", "IP67", "旋转式外壳，内部电源按钮"],
            ["YPB02", "硬币型 / 圆形", "可更换 CR2477", "1000 mAh (2年以上)", "100 米", "LIS3DH 三轴加速度计", "IP67", "运动触发广播，跌落警报"],
            ["YPB03", "方形 / 壁挂式", "4 × AA 干电池", "5800 mAh (最长10年)", "240 米", "无", "IP65", "工业级寿命，外部按钮，安装支架"],
            ["YPB04", "超薄卡片 / 胸卡", "充电式锂聚合物", "270 mAh (3个月)", "150 米", "三轴加速度计", "IP67", "震动马达，1个RGB LED，外部按钮，选配RFID"],
            ["YPB05", "Micro USB 转接器", "USB 接口 (无电池)", "持续供电 (外部电源)", "50 米", "无", "无", "超轻量 (2.0g)，即插即用，支持软件重启"]
        ]
    },
    "ja": {
        "title": "Yupitek iBeacon シリーズ — BLE 5.0 ビーコン",
        "desc": "Yupitek プロフェッショナル BLE 5.0 iBeacon / Eddystone ビーコン：YPB01、YPB02、YPB03、YPB04、YPB05。屋内位置測位、勤怠管理、資産追跡に最適。",
        "intro": "Yupitek iBeacon 製品は、高性能な位置測位、人員追跡、商業広告配信向けに設計された新世代の Bluetooth® Low Energy (BLE 5.0) ビーコンデバイスです。Apple iBeacon™ および Google Eddystone™ (UID、URL、TLM) プロトコルの両方をサポートし、最大 6 スロットの同時マルチプロトコル配信に対応。BeaconSET+ アプリから簡単に設定できます。",
        "topo_title": "BLE ビーコン システム構成",
        "topo_desc": "iBeacon エコシステムは、物理的な位置と企業のクラウドネットワークを接続します。ビーコンは一定の間隔で BLE 信号を発信し、スマートフォン（社内アプリ実行中）や BLE ゲートウェイによって検出され、位置や勤怠ログを中央管理システムへ安全に送信します。",
        "prod_title": "製品ラインナップ",
        "comp_title": "iBeacon シリーズ 仕様比較",
        "card_desc": "屋内位置測位、スマート勤怠管理、人員管理、および資産追跡用のプロフェッショナル BLE 5.0 ビーコン。",
        "cta": "お見積もりやカスタム統合ソリューションが必要ですか？弊社営業チームまで直接メールでお問い合わせください：**sales@yupitek.com**",
        "headers": ["型番", "形状", "電源仕様", "電池容量 / 寿命", "最大射程", "センサー", "防水等級", "特別機能"],
        "rows": [
            ["YPB01", "コイン型 / 円形", "交換式 CR2477", "1000 mAh (2年以上)", "100 m", "なし", "IP67", "回転開閉式ケース、内部ボタン"],
            ["YPB02", "コイン型 / 円形", "交換式 CR2477", "1000 mAh (2年以上)", "100 m", "LIS3DH 3軸加速度センサー", "IP67", "モーション検知時配信、落下警告"],
            ["YPB03", "角型 / 壁掛け用", "単3乾電池×4", "5800 mAh (最大10年)", "240 m", "なし", "IP65", "工業用超長寿命、外部ボタン、取付用ブラケット"],
            ["YPB04", "極薄カード / バッジ", "充電式リチウムポリマー", "270 mAh (3ヶ月)", "150 m", "3軸加速度センサー", "IP67", "バイブレーション、RGB LED、外部ボタン、RFID対応(オプション)"],
            ["YPB05", "Micro USB ドングル", "USBポート給電", "継続給電 (外部電源)", "50 m", "なし", "非対応", "超軽量 (2.0g)、プラグ＆プレイ、ソフト再起動対応"]
        ]
    },
    "ar": {
        "title": "سلسلة منارات BLE 5.0 iBeacon من Yupitek",
        "desc": "تقوم Yupitek بتوزيع منارات BLE 5.0 iBeacon و Eddystone الاحترافية: YPB01 و YPB02 و YPB03 و YPB04 و YPB05 - لتحديد المواقع داخلياً وحضور الموظفين وتتبع الأصول.",
        "intro": "تمثل منتجات iBeacon من Yupitek جيلاً جديداً من أجهزة البلوتوث منخفض الطاقة (BLE 5.0) المصممة لتحديد المواقع عالي الأداء وتتبع الموظفين والترويج التجاري. من خلال دعم بروتوكولات Apple iBeacon™ و Google Eddystone™ (UID, URL, TLM) في آن واحد، تدعم مناراتنا بث بروتوكولات متعددة في وقت واحد (حتى 6 قنوات) ويتم تهيئتها بسهولة عبر تطبيق BeaconSET+ للهواتف المحمولة.",
        "topo_title": "مخطط بنية نظام منارات BLE",
        "topo_desc": "يربط نظامنا البيئي لـ iBeacon المواقع المادية بالشبكات السحابية للمؤسسات. تبث المنارات إشارات راديو BLE بفواصل زمنية منتظمة، والتي يتم مسحها ضوئياً بواسطة الهواتف المحمولة (التي تشغل تطبيقات المؤسسة) وبوابات BLE، مما يعيد توجيه سجلات الحضور وتتبع الأصول الآمنة إلى خادم مركزي.",
        "prod_title": "مجموعة المنتجات",
        "comp_title": "جدول مقارنة مواصفات سلسلة iBeacon",
        "card_desc": "منارات BLE 5.0 احترافية لتحديد المواقع الداخلي، وتسجيل الحضور الذكي، وإدارة الأفراد، وتتبع الأصول.",
        "cta": "هل تحتاج إلى عرض أسعار مخصص أو حل تكامل؟ يرجى الاتصال بفريق المبيعات لدينا مباشرة على: **sales@yupitek.com**",
        "headers": ["النموذج", "الشكل والخصائص", "مصدر الطاقة", "سعة البطارية / العمر", "أقصى مدى", "المستشعرات", "مقاومة الماء", "ميزات خاصة"],
        "rows": [
            ["YPB01", "دائري / عملة معدنية", "بطارية CR2477 قابلة للاستبدال", "1000 مللي أمبير (سنتان+)", "100 متر", "لا يوجد", "IP67", "هيكل دوار، زر تشغيل داخلي"],
            ["YPB02", "دائري / عملة معدنية", "بطارية CR2477 قابلة للاستبدال", "1000 مللي أمبير (سنتان+)", "100 متر", "مستشعر تسارع LIS3DH ثلاثي المحاور", "IP67", "البث عند استشعار الحركة، منبه السقوط"],
            ["YPB03", "مربع / يعلق على الجدار", "4 بطاريات AA", "5800 مللي أمبير (حتى 10 سنوات)", "240 متر", "لا يوجد", "IP65", "عمر تشغيل صناعي، زر خارجي، دعامة تثبيت"],
            ["YPB04", "بطاقة / شارة رفيعة", "بطارية ليثيوم قابلة للشحن", "270 مللي أمبير (3 أشهر)", "150 متر", "مستشعر تسارع ثلاثي المحاور", "IP67", "محرك اهتزاز، مؤشر RGB LED، زر خارجي، RFID اختياري"],
            ["YPB05", "Micro USB دونجل", "منفذ USB (بدون بطارية)", "مستمر (طاقة خارجية)", "50 متر", "لا يوجد", "لا ينطبق", "خفيف الوزن للغاية (2.0 جم)، تشغيل فوري، يدعم إعادة التشغيل البرمجية"]
        ]
    },
    "de": {
        "title": "Yupitek iBeacon Serie — BLE 5.0 Beacons",
        "desc": "Yupitek vertreibt professionelle BLE 5.0 iBeacon und Eddystone Beacons: YPB01, YPB02, YPB03, YPB04, und YPB05 — für Indoor-Lokalisierung, Zeiterfassung und Asset-Tracking.",
        "intro": "Yupitek iBeacon-Produkte repräsentieren eine neue Generation von Bluetooth® Low Energy (BLE 5.0) Beacons für hochpräzise Lokalisierung, Personen-Tracking und kommerzielle Werbung. Durch die gleichzeitige Unterstützung von Apple iBeacon™ und Google Eddystone™ (UID, URL, TLM) ermöglichen unsere Beacons parallele Ausstrahlungen auf bis zu 6 Kanälen und lassen sich einfach über die BeaconSET+ App konfigurieren.",
        "topo_title": "BLE Beacon Systemtopologie",
        "topo_desc": "Unser iBeacon-Ökosystem verbindet physische Standorte mit Cloud-Netzwerken. Die Beacons senden in regelmäßigen Intervallen BLE-Funksignale aus, die von mobilen Geräten und BLE-Gateways erfasst werden, um gesicherte Anwesenheits- und Tracking-Daten an ein zentrales System zu übermitteln.",
        "prod_title": "Produktlinie",
        "comp_title": "Spezifikationsvergleich der iBeacon-Serie",
        "card_desc": "Professionelle BLE 5.0 Beacons für Indoor-Lokalisierung, intelligente Zeiterfassung, Personenmanagement und Asset-Tracking.",
        "cta": "Benötigen Sie ein individuelles Angebot oder eine Integrationslösung? Bitte kontaktieren Sie unser Vertriebsteam direkt unter: **sales@yupitek.com**",
        "headers": ["Modell", "Formfaktor", "Stromquelle", "Batteriekapazität / Lebensdauer", "Max. Reichweite", "Sensoren", "Wasserdicht", "Besondere Merkmale"],
        "rows": [
            ["YPB01", "Münze / Rund", "Austauschbare CR2477", "1000 mAh (2+ Jahre)", "100 m", "Keine", "IP67", "Drehbares Gehäuse, interner Einschaltknopf"],
            ["YPB02", "Münze / Rund", "Austauschbare CR2477", "1000 mAh (2+ Jahre)", "100 m", "LIS3DH 3-Achsen-Beschleunigungssensor", "IP67", "Bewegungsgesteuerter Broadcast, Sturzalarm"],
            ["YPB03", "Quadratisch / Wandhalterung", "4 × AA Batterien", "5800 mAh (Bis zu 10 Jahre)", "240 m", "Keine", "IP65", "Industrielle Lebensdauer, externer Knopf, Montagerahmen"],
            ["YPB04", "Flacher Badge / Karte", "Wiederaufladbarer Li-po", "270 mAh (3 Monate)", "150 m", "3-Achsen-Beschleunigungssensor", "IP67", "Vibrationsmotor, 1 RGB LED, externer Knopf, optional RFID"],
            ["YPB05", "Micro USB Dongle", "USB-Anschluss (Keine Batterie)", "Dauerhaft (Externe Stromversorgung)", "50 m", "Keine", "N/A", "Ultraleicht (2,0g), Plug & Play, Software-Reboot"]
        ]
    },
    "es": {
        "title": "Serie Yupitek iBeacon — Balizas BLE 5.0",
        "desc": "Yupitek distribuye balizas profesionales BLE 5.0 iBeacon y Eddystone: YPB01, YPB02, YPB03, YPB04 y YPB05, para localización en interiores, control de asistencia y seguimiento de activos.",
        "intro": "Los productos iBeacon de Yupitek representan una nueva generación de dispositivos de baliza Bluetooth® de bajo consumo (BLE 5.0) diseñados para localización de alto rendimiento, seguimiento de personal y publicidad comercial. Al admitir los protocolos Apple iBeacon™ y Google Eddystone™ (UID, URL, TLM) simultáneamente, permiten transmisiones multiprotocolo en hasta 6 ranuras, configurables fácilmente mediante la aplicación BeaconSET+.",
        "topo_title": "Topología del Sistema de Balizas BLE",
        "topo_desc": "Nuestro ecosistema iBeacon conecta ubicaciones físicas con redes en la nube corporativas. Las balizas transmiten señales de radio BLE a intervalos regulares, que son escaneadas por dispositivos móviles y pasarelas (gateways) BLE, enviando registros seguros de asistencia y localización a un servidor central.",
        "prod_title": "Línea de Productos",
        "comp_title": "Comparativa de Especificaciones de la Serie iBeacon",
        "card_desc": "Balizas profesionales BLE 5.0 para localización en interiores, control de asistencia inteligente, gestión de personal y seguimiento de activos.",
        "cta": "¿Necesita un presupuesto personalizado o una solución de integración? Póngase en contacto con nuestro equipo de ventas directamente en: **sales@yupitek.com**",
        "headers": ["Modelo", "Factor de forma", "Fuente de alimentación", "Capacidad / Vida de batería", "Alcance máx.", "Sensores", "Impermeable", "Características especiales"],
        "rows": [
            ["YPB01", "Moneda / Redonda", "CR2477 reemplazable", "1000 mAh (2+ años)", "100 m", "Ninguno", "IP67", "Carcasa giratoria, botón de encendido interno"],
            ["YPB02", "Moneda / Redonda", "CR2477 reemplazable", "1000 mAh (2+ años)", "100 m", "Acelerómetro LIS3DH de 3 ejes", "IP67", "Transmisión por movimiento, alerta de caída"],
            ["YPB03", "Cuadrada / Soporte de pared", "4 pilas AA", "5800 mAh (Hasta 10 años)", "240 m", "Ninguno", "IP65", "Vida útil industrial, botón externo, soporte de tornillos"],
            ["YPB04", "Insignia / Tarjeta delgada", "Li-po recargable", "270 mAh (3 meses)", "150 m", "Acelerómetro de 3 ejes", "IP67", "Motor de vibración, 1 LED RGB, botón externo, RFID opcional"],
            ["YPB05", "Micro USB Dongle", "Ranura USB (Sin batería)", "Continuo (Alimentación externa)", "50 m", "Ninguno", "N/A", "Ultraligera (2,0g), Plug & Play, reinicio por software"]
        ]
    },
    "fr": {
        "title": "Série Yupitek iBeacon — Balises BLE 5.0",
        "desc": "Yupitek distribue des balises professionnelles BLE 5.0 iBeacon et Eddystone : YPB01, YPB02, YPB03, YPB04 et YPB05 — pour la géolocalisation intérieure, le contrôle de présence et le suivi des actifs.",
        "intro": "Les produits iBeacon de Yupitek représentent une nouvelle génération de balises Bluetooth® Low Energy (BLE 5.0) conçues pour la localisation haute performance, le suivi du personnel et la publicité commerciale. Compatibles simultanément avec les protocoles Apple iBeacon™ et Google Eddystone™ (UID, URL, TLM), nos balises permettent des diffusions multiprotocoles (jusqu'à 6 slots) configurables facilement depuis l'application BeaconSET+.",
        "topo_title": "Topologie du Système de Balises BLE",
        "topo_desc": "Notre écosystème iBeacon connecte les espaces physiques aux réseaux cloud de l'entreprise. Les balises émettent des signaux radio BLE à intervalles réguliers, captés par les smartphones et les passerelles BLE, pour remonter des données de présence et de localisation vers un serveur central.",
        "prod_title": "Gamme de Produits",
        "comp_title": "Comparatif des Spécifications de la Série iBeacon",
        "card_desc": "Balises professionnelles BLE 5.0 pour la localisation en intérieur, la gestion intelligente des présences et le suivi d'actifs.",
        "cta": "Besoin d'un devis sur mesure ou d'une solution d'intégration ? Veuillez contacter notre équipe commerciale directement à : **sales@yupitek.com**",
        "headers": ["Modèle", "Facteur de forme", "Source d'énergie", "Capacité / Durée de batterie", "Portée max.", "Capteurs", "Étanchéité", "Fonctions spéciales"],
        "rows": [
            ["YPB01", "Pièce / Ronde", "CR2477 remplaçable", "1000 mAh (2 ans et +)", "100 m", "Aucun", "IP67", "Boîtier rotatif, bouton d'alimentation interne"],
            ["YPB02", "Pièce / Ronde", "CR2477 remplaçable", "1000 mAh (2 ans et +)", "100 m", "Accéléromètre LIS3DH 3 axes", "IP67", "Diffusion déclenchée par mouvement, alerte chute"],
            ["YPB03", "Carré / Support mural", "4 piles AA", "5800 mAh (Jusqu'à 10 ans)", "240 m", "Aucun", "IP65", "Longévité industrielle, bouton externe, support vissable"],
            ["YPB04", "Badge / Carte mince", "Li-po rechargeable", "270 mAh (3 mois)", "150 m", "Accéléromètre 3 axes", "IP67", "Vibreur, 1 LED RGB, bouton externe, RFID optionnelle"],
            ["YPB05", "Micro USB Dongle", "Port USB (Sans batterie)", "Continu (Alimentation externe)", "50 m", "Aucun", "N/A", "Ultra-légère (2,0g), Plug & Play, redémarrage logiciel"]
        ]
    },
    "pt": {
        "title": "Série Yupitek iBeacon — Beacons BLE 5.0",
        "desc": "A Yupitek distribui beacons profissionais BLE 5.0 iBeacon e Eddystone: YPB01, YPB02, YPB03, YPB04 e YPB05 — para localização interna, controle de ponto e rastreamento de ativos.",
        "intro": "Os beacons iBeacon da Yupitek representam uma nova geração de dispositivos Bluetooth® Low Energy (BLE 5.0) projetados para localização de alta performance, rastreamento de pessoal e marketing de proximidade. Com suporte simultâneo aos protocolos Apple iBeacon™ e Google Eddystone™ (UID, URL, TLM), nossos beacons suportam transmissões em até 6 canais configurados via aplicativo BeaconSET+.",
        "topo_title": "Topologia do Sistema de Beacons BLE",
        "topo_desc": "Nosso ecossistema iBeacon conecta locais físicos com as redes em nuvem das empresas. Os beacons transmitem sinais de rádio BLE em intervalos regulares, que são detectados por celulares e gateways BLE, enviando relatórios de presença e rastreamento para um servidor central.",
        "prod_title": "Linha de Produtos",
        "comp_title": "Comparação de Especificações da Série iBeacon",
        "card_desc": "Beacons profissionais BLE 5.0 para localização em ambientes internos, controle de ponto inteligente, gestão de pessoal e rastreamento de ativos.",
        "cta": "Precisa de um orçamento personalizado ou solução de integração? Entre em contato diretamente com nossa equipe de vendas pelo e-mail: **sales@yupitek.com**",
        "headers": ["Modelo", "Formato / Design", "Fonte de energia", "Capacidade / Vida da bateria", "Alcance máx.", "Sensores", "Impermeabilidade", "Recursos especiais"],
        "rows": [
            ["YPB01", "Moeda / Redondo", "CR2477 substituível", "1000 mAh (2+ anos)", "100 m", "Nenhum", "IP67", "Gabinete rotativo, botão de liga/desliga interno"],
            ["YPB02", "Moeda / Redondo", "CR2477 substituível", "1000 mAh (2+ anos)", "100 m", "Acelerômetro LIS3DH de 3 eixos", "IP67", "Transmissão ativa por movimento, alerta de quedas"],
            ["YPB03", "Quadrado / Suporte de parede", "4 pilhas AA", "5800 mAh (Até 10 anos)", "240 m", "Nenhum", "IP65", "Vida útil industrial, botão externo, suporte de parafusos"],
            ["YPB04", "Crachá / Cartão fino", "Li-po recarregável", "270 mAh (3 meses)", "150 m", "Acelerômetro de 3 eixos", "IP67", "Motor de vibração, 1 LED RGB, botão externo, RFID opcional"],
            ["YPB05", "Micro USB Dongle", "Slot USB (Sem bateria)", "Contínuo (Alimentação externa)", "50 m", "Nenhum", "N/A", "Ultraleve (2,0g), Plug & Play, reinicialização via software"]
        ]
    },
    "ru": {
        "title": "Серия маяков Yupitek iBeacon — BLE 5.0",
        "desc": "Yupitek поставляет профессиональные BLE 5.0 iBeacon и Eddystone маяки: YPB01, YPB02, YPB03, YPB04 и YPB05 — для позиционирования внутри помещений, учета рабочего времени и отслеживания активов.",
        "intro": "Маяки iBeacon от Yupitek представляют собой новое поколение устройств Bluetooth® Low Energy (BLE 5.0), предназначенных для высокоточного позиционирования, мониторинга персонала и рекламных рассылок. Поддерживая протоколы Apple iBeacon™ и Google Eddystone™ (UID, URL, TLM), наши маяки осуществляют трансляцию на 6 слотах одновременно, легко настраиваясь через приложение BeaconSET+.",
        "topo_title": "Топология системы BLE-маяков",
        "topo_desc": "Экосистема iBeacon связывает физические объекты с корпоративными облачными сетями. Маяки регулярно отправляют BLE-сигналы, которые сканируются смартфонами и шлюзами BLE, пересылая защищенные логи на центральный сервер учета присутствия и отслеживания активов.",
        "prod_title": "Линейка продукции",
        "comp_title": "Таблица сравнения спецификаций серии iBeacon",
        "card_desc": "Профессиональные маяки BLE 5.0 для позиционирования в помещениях, умного учета рабочего времени, контроля персонала и отслеживания активов.",
        "cta": "Нужно индивидуальное предложение или интеграционное решение? Свяжитесь с нашим отделом продаж напрямую по адресу: **sales@yupitek.com**",
        "headers": ["Модель", "Форм-фактор", "Источник питания", "Емкость батареи / Ресурс", "Макс. дальность", "Датчики", "Влагозащита", "Особые свойства"],
        "rows": [
            ["YPB01", "Круглый / Монета", "Заменяемая CR2477", "1000 мАч (2+ года)", "100 м", "Нет", "IP67", "Поворотный корпус, внутренняя кнопка питания"],
            ["YPB02", "Круглый / Монета", "Заменяемая CR2477", "1000 мАч (2+ года)", "100 м", "3-осевой акселерометр LIS3DH", "IP67", "Трансляция при движении, оповещение о падении"],
            ["YPB03", "Квадратный / Настенный", "4 батарейки AA", "5800 мАч (До 10 лет)", "240 м", "Нет", "IP65", "Промышленный ресурс, внешняя кнопка, монтажный кронштейн"],
            ["YPB04", "Бейдж / Тонкая карта", "Перезаряжаемый Li-po", "270 мАч (3 месяца)", "150 м", "3-осевой акселерометр", "IP67", "Вибромотор, 1 RGB светодиод, внешняя кнопка, RFID опционально"],
            ["YPB05", "Micro USB донгл", "Порт USB (без батарейки)", "Непрерывно (внешнее питание)", "50 м", "Нет", "Нет", "Ультралегкий (2.0г), Plug & Play, программная перезагрузка"]
        ]
    }
}

# English product data (the blueprints we read earlier)
EN_BLUEPRINTS = {
    "ypb01": {
        "title": "YPB01 BLE 5.0 Beacon",
        "spec_keys": ["Chip Model", "Bluetooth Version", "Waterproof Level", "Transmission Range", "Antenna Impedance", "Power Source", "Operating Voltage", "Peak Current", "Dimensions", "Default Settings"],
        "spec_vals": ["nRF52 series", "BLE 5.0", "IP67", "Up to 100 meters", "50 ohm", "1 × CR2477 coin battery", "1.8V - 3.9V", "5.3 mA", "Φ39 × 15.5 mm", "UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms"]
    },
    "ypb02": {
        "title": "YPB02 Motion-Sensing BLE Beacon",
        "spec_keys": ["Chip Model", "Bluetooth Version", "Waterproof Level", "Sensor", "Transmission Range", "Antenna Impedance", "Power Source", "Operating Voltage", "Peak Current", "Dimensions", "Default Settings"],
        "spec_vals": ["nRF52 series", "BLE 5.0", "IP67", "LIS3DH 3-axis accelerometer", "Up to 100 meters", "50 ohm", "1 × CR2477 coin battery", "1.8V - 3.9V", "5.3 mA", "Φ39 × 15.5 mm", "UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms"]
    },
    "ypb03": {
        "title": "YPB03 Long-Range Max Beacon",
        "spec_keys": ["Chip Model", "Bluetooth Version", "Waterproof Level", "Transmission Range", "Power Source", "Battery Lifetime", "Material", "Dimensions", "Net Weight", "Default Settings"],
        "spec_vals": ["nRF52 series", "BLE 5.0", "IP65", "Up to 240 meters", "4 × AA batteries", "Up to 10 years", "ABS + Silicone", "72 × 72 × 23 mm", "145 g", "UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms"]
    },
    "ypb04": {
        "title": "YPB04 Rechargeable Badge Beacon",
        "spec_keys": ["Chip Model", "Bluetooth Version", "Waterproof Level", "Sensors", "Feedback Elements", "Control Button", "RFID Compatibility", "Transmission Range", "Power Source", "Battery Lifetime", "Charging Time", "Dimensions & Weight"],
        "spec_vals": ["nRF52 series", "BLE 5.0", "IP67", "3-axis accelerometer", "1 × Vibration Motor, 1 × RGB LED", "1 × External physical button", "LF / HF / UHF", "Up to 150 meters (492 ft)", "Magnetic charging Li-po battery", "Up to 3 months", "Approximately 2 hours", "86 × 55 × 6 mm \| 19 g"]
    },
    "ypb05": {
        "title": "YPB05 Micro USB Beacon",
        "spec_keys": ["Chip Model", "Bluetooth Version", "Power Source", "Operating Voltage", "Max Current", "Transmission Range", "Antenna Impedance", "Dimensions & Weight", "Default Settings"],
        "spec_vals": ["nRF52 series", "BLE 5.0", "Powered by USB slot (No battery)", "4.5V - 5.5V", "5.3 mA", "Up to 50 meters", "50 ohm", "18 × 14 × 6 mm \| 2.0 g", "UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 4 dBm (Level 7)<br>Adv. Interval: 900 ms"]
    }
}

# Localized specifications translation dictionary
SPEC_DICTS = {
    "zh-tw": {
        "Chip Model": "晶片型號", "Bluetooth Version": "藍牙版本", "Waterproof Level": "防水等級", "Transmission Range": "傳輸距離", "Antenna Impedance": "天線阻抗", "Power Source": "電源規格", "Operating Voltage": "工作電壓", "Peak Current": "峰值電流", "Dimensions": "外觀尺寸", "Default Settings": "預設參數", "Sensor": "感測器", "Sensors": "感測器", "Feedback Elements": "反饋機制", "Control Button": "控制按鈕", "RFID Compatibility": "RFID 相容性", "Battery Lifetime": "電池壽命", "Charging Time": "充電時間", "Dimensions & Weight": "外觀尺寸與重量", "Net Weight": "淨重", "Material": "外殼材質", "Max Current": "最大電流",
        "nRF52 series": "nRF52 系列", "BLE 5.0": "BLE 5.0 (低功耗藍牙)", "IP67": "IP67 (防塵防水)", "IP65": "IP65 (防塵防潑水)", "Up to 100 meters": "最遠 100 公尺 (開闊空間)", "Up to 240 meters": "最遠 240 公尺 (開闊空間)", "Up to 150 meters (492 ft)": "最遠 150 公尺 (492 英尺，開闊空間)", "Up to 50 meters": "最遠 50 公尺 (開闊空間)", "50 ohm": "50 歐姆", "1 × CR2477 coin battery": "1 × CR2477 鈕扣電池", "4 × AA batteries": "4 × AA (三號) 乾電池", "Magnetic charging Li-po battery": "磁吸充電式鋰聚合物電池 (270mAh)", "Powered by USB slot (No battery)": "Micro USB 插槽供電 (無電池)", "Up to 10 years": "最長可達 10 年 (預設參數下)", "Up to 3 months": "最長可達 3 個月 (一般按壓頻率)", "Approximately 2 hours": "約 2 小時 (室溫，5V/1A 電源供應器)", "ABS + Silicone": "ABS 塑膠 + 矽膠", "1 × Vibration Motor, 1 × RGB LED": "1 × 震動馬達，1 × RGB LED 指示燈", "1 × External physical button": "1 × 外部實體按鈕", "LF / HF / UHF": "低頻(LF) / 高頻(HF) / 超高頻(UHF) (選配)", "Compact circular shape": "緊湊圓形", "Wall-mountable square": "壁掛方形", "Ultra-low power consumption": "超低功耗晶片", "High efficiency and speed": "高傳輸效率與速率", "Splash and dust resistant (1m immersion)": "防塵防水 (支援短時間浸入 1 公尺水中)", "Open space": "開闊空間", "On-board / PCB Antenna": "板載 PCB 天線", "Replaceable (3.0V, 1000mAh)": "可更換 (3.0V, 1000mAh)", "DC": "直流電", "Tested at 0dBm transmission power": "於 0dBm 廣播功率測試", "Tested at 0dBm": "於 0dBm 測試", "Configurable via App": "可透過 App 自訂修改", "LIS3DH 3-axis accelerometer": "LIS3DH 三軸加速度感測器", "X, Y, Z axes telemetry": "X、Y、Z 三軸數據", "Low latency and high efficiency": "低延遲與高效率", "High range and throughput": "長距離與高傳輸量", "Dustproof and water-jet resistant": "防塵與防低壓噴水", "Maximum in open areas": "開闊空間最大距離", "5800mAh capacity total (Included)": "總容量 5800mAh (隨附)", "Based on default broadcasting parameters": "基於預設廣播參數", "Rugged industrial casing": "堅固工業外殼", "Including batteries": "含電池", "Secure connection and long range": "安全連線與長距離", "Displacement and movement detection": "位移與運動檢測", "Tactile and visual cues": "觸覺與視覺提示", "Activates triggers and alarms": "啟用觸發器與警報", "Optional build integrations": "選配整合", "Slim card format": "超薄卡片格式", "Pocket-sized": "口袋型", "Continuous operation": "持續不間斷運作", "Ultra-lightweight (2.0g)": "超輕量 2.0 公克", "Plug & play, software reboot": "隨插即用，支援指令重啟"
    },
    "zh-cn": {
        "Chip Model": "芯片型号", "Bluetooth Version": "蓝牙版本", "Waterproof Level": "防水等级", "Transmission Range": "传输距离", "Antenna Impedance": "天线阻抗", "Power Source": "电源规格", "Operating Voltage": "工作电压", "Peak Current": "峰值电流", "Dimensions": "外观尺寸", "Default Settings": "默认参数", "Sensor": "传感器", "Sensors": "传感器", "Feedback Elements": "反馈机制", "Control Button": "控制按钮", "RFID Compatibility": "RFID 兼容性", "Battery Lifetime": "电池寿命", "Charging Time": "充电时间", "Dimensions & Weight": "外观尺寸与重量", "Net Weight": "净重", "Material": "外壳材质", "Max Current": "最大电流",
        "nRF52 series": "nRF52 系列", "BLE 5.0": "BLE 5.0 (低功耗蓝牙)", "IP67": "IP67 (防尘防水)", "IP65": "IP65 (防尘防泼水)", "Up to 100 meters": "最远 100 米 (开阔空间)", "Up to 240 meters": "最远 240 米 (开阔空间)", "Up to 150 meters (492 ft)": "最远 150 米 (492 英尺，开阔空间)", "Up to 50 meters": "最远 50 米 (开阔空间)", "50 ohm": "50 欧姆", "1 × CR2477 coin battery": "1 × CR2477 纽扣电池", "4 × AA batteries": "4 × AA (三号) 干电池", "Magnetic charging Li-po battery": "磁吸充电式锂聚合物电池 (270mAh)", "Powered by USB slot (No battery)": "Micro USB 插槽供电 (无电池)", "Up to 10 years": "最长可达 10 年 (默认参数下)", "Up to 3 months": "最长可达 3 个月 (一般按压频率)", "Approximately 2 hours": "约 2 小时 (室温，5V/1A 电源适配器)", "ABS + Silicone": "ABS 塑料 + 硅胶", "1 × Vibration Motor, 1 × RGB LED": "1 × 震动马达，1 × RGB LED 指示灯", "1 × External physical button": "1 × 外部实体按钮", "LF / HF / UHF": "低频(LF) / 高频(HF) / 超高频(UHF) (选配)", "Compact circular shape": "紧凑圆形", "Wall-mountable square": "壁挂方形", "Ultra-low power consumption": "超低功耗芯片", "High efficiency and speed": "高传输效率与速率", "Splash and dust resistant (1m immersion)": "防尘防水 (支持短时间浸入 1 米水中)", "Open space": "开阔空间", "On-board / PCB Antenna": "板载 PCB 天线", "Replaceable (3.0V, 1000mAh)": "可更换 (3.0V, 1000mAh)", "DC": "直流电", "Tested at 0dBm transmission power": "于 0dBm 广播功率测试", "Tested at 0dBm": "于 0dBm 测试", "Configurable via App": "可透过 App 自定义修改", "LIS3DH 3-axis accelerometer": "LIS3DH 三轴加速度传感器", "X, Y, Z axes telemetry": "X、Y、Z 三轴数据", "Low latency and high efficiency": "低延迟与高效率", "High range and throughput": "长距离与高传输量", "Dustproof and water-jet resistant": "防尘与防低压喷水", "Maximum in open areas": "开阔空间最大距离", "5800mAh capacity total (Included)": "总容量 5800mAh (随附)", "Based on default broadcasting parameters": "基于默认广播参数", "Rugged industrial casing": "坚固工业外壳", "Including batteries": "含电池", "Secure connection and long range": "安全连线与长距离", "Displacement and movement detection": "位移与运动检测", "Tactile and visual cues": "触觉与视觉提示", "Activates triggers and alarms": "启用触发器与警报", "Optional build integrations": "选配整合", "Slim card format": "超薄卡片格式", "Pocket-sized": "口袋型", "Continuous operation": "持续不间断运作", "Ultra-lightweight (2.0g)": "超轻量 2.0 克", "Plug & play, software reboot": "即插即用，支持指令重启"
    }
}

# The files translation template generator
def generate_category_index(lang, info):
    headers = " | ".join(info["headers"])
    seps = " | ".join(["---"] * len(info["headers"]))
    rows = []
    for r in info["rows"]:
        rows.append(" | ".join(r))
    table = f"| {headers} |\n| {seps} |\n" + "\n".join([f"| {row} |" for row in rows])

    # Card titles
    cards_titles = {
        "ypb01": "YPB01 BLE 5.0 Beacon" if lang != "ja" else "YPB01 BLE 5.0 ビーコン",
        "ypb02": "YPB02 Sensor Beacon" if lang != "ja" else "YPB02 センサービーコン",
        "ypb03": "YPB03 Max Beacon" if lang != "ja" else "YPB03 Max ビーコン",
        "ypb04": "YPB04 Rechargeable Badge" if lang != "ja" else "YPB04 充電式バッジ",
        "ypb05": "YPB05 Micro USB Beacon" if lang != "ja" else "YPB05 Micro USB ビーコン"
    }

    # Custom localization elements
    title = info["title"]
    desc = info["desc"]
    intro = info["intro"]
    topo_title = info["topo_title"]
    topo_desc = info["topo_desc"]
    prod_title = info["prod_title"]
    comp_title = info["comp_title"]
    cta = info["cta"]

    content = f"""---
title: "{title}"
description: "{desc}"
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: false
showChildPages: false
---

{intro}

---

## {topo_title}

![BLE Beacon System Topology Diagram](/images/products/ibeacon/ibeacon_topology.png)

{topo_desc}

---

## {prod_title}

{{{{< card-group >}}}}
  {{{{< card title="{cards_titles['ypb01']}" href="/{lang}/products/ibeacon/ypb01/" image="/images/products/ibeacon/ypb01.png" >}}}}
    YPB01
  {{{{</card >}}}}
  {{{{< card title="{cards_titles['ypb02']}" href="/{lang}/products/ibeacon/ypb02/" image="/images/products/ibeacon/ypb02.png" >}}}}
    YPB02
  {{{{</card >}}}}
  {{{{< card title="{cards_titles['ypb03']}" href="/{lang}/products/ibeacon/ypb03/" image="/images/products/ibeacon/ypb03.png" >}}}}
    YPB03
  {{{{</card >}}}}
  {{{{< card title="{cards_titles['ypb04']}" href="/{lang}/products/ibeacon/ypb04/" image="/images/products/ibeacon/ypb04.png" >}}}}
    YPB04
  {{{{</card >}}}}
  {{{{< card title="{cards_titles['ypb05']}" href="/{lang}/products/ibeacon/ypb05/" image="/images/products/ibeacon/ypb05.png" >}}}}
    YPB05
  {{{{</card >}}}}
{{{{</card-group >}}}}

---

## {comp_title}

{table}

---

{{{{< alert >}}}}
{cta}
{{{{</alert >}}}}
"""
    return content

# Generates pages using English templates but substituting specs table keys and localized titles
def translate_product_page(lang, model, blueprint, en_content):
    title = blueprint["title"]
    # Look for title in localized landing info rows to match
    rows = LANDING_INFO.get(lang, LANDING_INFO["zh-tw"])["rows"]
    matched_title = ""
    for r in rows:
        if r[0].lower() == model.lower():
            matched_title = f"{r[0]} {r[7]}" if lang in ["zh-tw", "zh-cn"] else f"{r[0]} {r[1]} {r[5] if r[5] != 'None' and r[5] != '无' else ''}"
            # Let's clean it up slightly or define a strict title map
            break

    # Static title override mapping
    title_maps = {
        "zh-tw": {
            "ypb01": "YPB01 BLE 5.0 藍牙信標",
            "ypb02": "YPB02 三軸加速度感測 BLE 藍牙信標",
            "ypb03": "YPB03 工業級超長效 Max Beacon 藍牙信標",
            "ypb04": "YPB04 充電式多功能智慧工卡/胸卡信標",
            "ypb05": "YPB05 Micro USB 免電池隨插即用藍牙信標",
        },
        "zh-cn": {
            "ypb01": "YPB01 BLE 5.0 蓝牙信标",
            "ypb02": "YPB02 三轴加速度感测 BLE 蓝牙信标",
            "ypb03": "YPB03 工业级超长效 Max Beacon 蓝牙信标",
            "ypb04": "YPB04 充电式多功能智能工卡/胸卡信标",
            "ypb05": "YPB05 Micro USB 免电池随插即用蓝牙信标",
        },
        "ja": {
            "ypb01": "YPB01 BLE 5.0 ビーコン",
            "ypb02": "YPB02 加速度センサー内蔵 BLE ビーコン",
            "ypb03": "YPB03 長寿命 Max Beacon ビーコン",
            "ypb04": "YPB04 充電式スマートカードバッジ型ビーコン",
            "ypb05": "YPB05 Micro USB 給電式ビーコン",
        },
        "ar": {
            "ypb01": "منارة YPB01 BLE 5.0",
            "ypb02": "منارة YPB02 BLE بمستشعر حركة",
            "ypb03": "منارة YPB03 Max طويلة المدى",
            "ypb04": "شارة منارة YPB04 الذكية القابلة لإعادة الشحن",
            "ypb05": "منارة YPB05 Micro USB بدون بطارية",
        },
        "de": {
            "ypb01": "YPB01 BLE 5.0 Beacon",
            "ypb02": "YPB02 Bewegungssensor BLE Beacon",
            "ypb03": "YPB03 Langstrecken Max Beacon",
            "ypb04": "YPB04 Wiederaufladbarer Badge Beacon",
            "ypb05": "YPB05 Micro USB Beacon ohne Batterie",
        },
        "es": {
            "ypb01": "Baliza YPB01 BLE 5.0",
            "ypb02": "Baliza Sensora YPB02 BLE con Acelerómetro",
            "ypb03": "Baliza Max YPB03 BLE de Largo Alcance",
            "ypb04": "Baliza de Tarjeta YPB04 Recargable",
            "ypb05": "Baliza Micro USB YPB05 sin Batería",
        },
        "fr": {
            "ypb01": "Balise YPB01 BLE 5.0",
            "ypb02": "Balise Détectrice de Mouvement YPB02 BLE",
            "ypb03": "Balise Longue Portée YPB03 Max Beacon",
            "ypb04": "Balise Badge Carte Rechargeable YPB04",
            "ypb05": "Balise Micro USB YPB05 sans Batterie",
        },
        "pt": {
            "ypb01": "Beacon YPB01 BLE 5.0",
            "ypb02": "Beacon Sensor de Movimento YPB02 BLE",
            "ypb03": "Beacon Longo Alcance YPB03 Max Beacon",
            "ypb04": "Beacon Crachá Recarregável YPB04",
            "ypb05": "Beacon Micro USB YPB05 sem Bateria",
        },
        "ru": {
            "ypb01": "Маяк YPB01 BLE 5.0",
            "ypb02": "Маяк YPB02 BLE с датчиком движения",
            "ypb03": "Длиннодистанционный маяк YPB03 Max Beacon",
            "ypb04": "Перезаряжаемый маяк-бейдж YPB04",
            "ypb05": "Микро USB маяк YPB05 без батарейки",
        }
    }
    
    localized_title = title_maps.get(lang, {}).get(model, blueprint["title"])

    # Basic translations of section headers and texts
    # We will automatically perform high-quality search/replace on section headers:
    translated = en_content
    # Replace frontmatter title
    translated = re.sub(r'^title: ".*?"', f'title: "{localized_title}"', translated, flags=re.M)
    # Replace frontmatter description with a generic localized one
    desc_maps = {
        "zh-tw": f"{localized_title}。藍牙低功耗 BLE 5.0 技術，專為考勤打卡、定位與資產追蹤設計，可配置參數。",
        "zh-cn": f"{localized_title}。蓝牙低功耗 BLE 5.0 技术，专为考勤打卡、定位与资产追踪设计，可配置参数。",
        "ja": f"{localized_title}。低消費電力 Bluetooth BLE 5.0 技術、勤怠管理、位置測位、資産追跡に最適、設定可能。",
        "ar": f"{localized_title}. تقنية البلوتوث منخفض الطاقة BLE 5.0، لتحديد المواقع وحضور الموظفين وتتبع الأصول.",
        "de": f"{localized_title}. Bluetooth Low Energy BLE 5.0, für Lokalisierung, Zeiterfassung und Asset-Tracking.",
        "es": f"{localized_title}. Bluetooth Low Energy BLE 5.0, para localización, control de asistencia y seguimiento.",
        "fr": f"{localized_title}. Bluetooth Low Energy BLE 5.0, pour localisation, contrôle de présence et suivi d'actifs.",
        "pt": f"{localized_title}. Bluetooth Low Energy BLE 5.0, para localização, controle de presença e rastreamento.",
        "ru": f"{localized_title}. Bluetooth Low Energy BLE 5.0, для позиционирования, контроля присутствия и трекинга."
    }
    localized_desc = desc_maps.get(lang, blueprint["title"])
    translated = re.sub(r'^description: ".*?"', f'description: "{localized_desc}"', translated, flags=re.M)

    # Translate specs table keys and values
    d = SPEC_DICTS.get(lang, SPEC_DICTS["zh-tw"])
    for en_key in blueprint["spec_keys"]:
        # Translate key
        loc_key = d.get(en_key, en_key)
        # Search and replace in table: | key | -> | loc_key |
        # Let's escape special characters in key just in case
        pattern = r'\|\s*\*\*' + re.escape(en_key) + r'\*\*\s*\|'
        translated = re.sub(pattern, f"| **{loc_key}** |", translated)
        
        pattern_normal = r'\|\s*' + re.escape(en_key) + r'\s*\|'
        translated = re.sub(pattern_normal, f"| {loc_key} |", translated)

    # Translate known specifications cell values
    for en_val in blueprint["spec_vals"]:
        loc_val = d.get(en_val, en_val)
        translated = translated.replace(en_val, loc_val)
        
    # Translate table column headers in product specs: | Parameter | Specifications | Remarks |
    if lang in ["zh-tw", "zh-cn"]:
        translated = translated.replace("| Parameter | Specifications | Remarks |", "| 參數項目 | 技術規格 | 備註說明 |" if lang == "zh-tw" else "| 参数项目 | 技术规格 | 备注说明 |")
        translated = translated.replace("| Parameter | Specifications |", "| 參數項目 | 技術規格 |" if lang == "zh-tw" else "| 参数项目 | 技术规格 |")
    elif lang == "ja":
        translated = translated.replace("| Parameter | Specifications | Remarks |", "| パラメータ | 技術仕様 | 備考 |")
        translated = translated.replace("| Parameter | Specifications |", "| パラメータ | 技術仕様 |")
    elif lang == "de":
        translated = translated.replace("| Parameter | Specifications | Remarks |", "| Parameter | Spezifikationen | Anmerkungen |")
    elif lang == "es":
        translated = translated.replace("| Parameter | Specifications | Remarks |", "| Parámetro | Especificaciones | Observaciones |")
    elif lang == "fr":
        translated = translated.replace("| Parameter | Specifications | Remarks |", "| Paramètre | Spécifications | Remarques |")
    elif lang == "pt":
        translated = translated.replace("| Parameter | Specifications | Remarks |", "| Parâmetro | Especificações | Observações |")
    elif lang == "ru":
        translated = translated.replace("| Parameter | Specifications | Remarks |", "| Параметр | Технические характеристики | Примечания |")
    elif lang == "ar":
        translated = translated.replace("| Parameter | Specifications | Remarks |", "| المعيار | المواصفات | ملاحظات |")

    # Replace headers
    header_maps = {
        "zh-tw": {
            "## Product Overview": "## 產品概述",
            "## Technical Specifications": "## 技術規格",
            "## Key Features": "## 主要特點",
            "## Configuration Guidance": "## 配置指南",
            "## Product Gallery": "## 產品圖片",
            "## Operational Guide": "## 操作說明",
            "## Motion Trigger & Telemetry": "## 運動觸發與遙測數據",
            "## Installation Methods": "## 安裝方法",
            "Method A: Industrial Adhesive Tape": "方法 A：工業雙面膠帶貼裝",
            "Method B: Screw Bracket Mount (Recommended)": "方法 B：螺絲支架固定安裝（推薦）",
            "### How to Turn the Beacon ON": "### 如何開啟信標電源",
            "### How to Turn the Beacon OFF": "### 如何關閉信標電源",
            "### Battery Status & Charging": "### 電量狀態與充電指示",
            "### Button Click Triggers": "### 按鈕點擊觸發廣播"
        },
        "zh-cn": {
            "## Product Overview": "## 产品概述",
            "## Technical Specifications": "## 技术规格",
            "## Key Features": "## 主要特点",
            "## Configuration Guidance": "## 配置指南",
            "## Product Gallery": "## 产品图片",
            "## Operational Guide": "## 操作说明",
            "## Motion Trigger & Telemetry": "## 运动触发与遥测数据",
            "## Installation Methods": "## 安装方法",
            "Method A: Industrial Adhesive Tape": "方法 A：工业双面胶带贴装",
            "Method B: Screw Bracket Mount (Recommended)": "方法 B：螺丝支架固定安装（推荐）",
            "### How to Turn the Beacon ON": "### 如何开启信标电源",
            "### How to Turn the Beacon OFF": "### 如何关闭信标电源",
            "### Battery Status & Charging": "### 电量状态与充电指示",
            "### Button Click Triggers": "### 按钮点击触发广播"
        },
        "ja": {
            "## Product Overview": "## 製品概要",
            "## Technical Specifications": "## 技術仕様",
            "## Key Features": "## 主な特徴",
            "## Configuration Guidance": "## 設定ガイド",
            "## Product Gallery": "## 製品ギャラリー",
            "## Operational Guide": "## 操作ガイド",
            "## Motion Trigger & Telemetry": "## モーション検知とテレメトリ",
            "## Installation Methods": "## 設置方法",
            "Method A: Industrial Adhesive Tape": "方法 A：両面テープによる貼り付け",
            "Method B: Screw Bracket Mount (Recommended)": "方法 B：ネジ式ブラケットによる壁掛け（推奨）",
            "### How to Turn the Beacon ON": "### ビーコンの電源を入れる方法",
            "### How to Turn the Beacon OFF": "### ビーコンの電源を切る方法",
            "### Battery Status & Charging": "### 電池ステータスと充電について",
            "### Button Click Triggers": "### ボタンクリック時の動作設定"
        }
    }
    
    # Generic replacement of standard section headers for all languages
    headers = ["Product Overview", "Technical Specifications", "Key Features", "Configuration Guidance", "Product Gallery", "Operational Guide", "Motion Trigger & Telemetry", "Installation Methods"]
    translation_headers = {
        "ar": ["نظرة عامة على المنتج", "المواصفات الفنية", "الميزات الرئيسية", "إرشادات التهيئة", "معرض صور المنتج", "دليل التشغيل", "استشعار الحركة والقياس عن بعد", "طرق التثبيت"],
        "de": ["Produktübersicht", "Technische Spezifikationen", "Hauptmerkmale", "Konfigurationsanleitung", "Produktgalerie", "Bedienungsanleitung", "Bewegungsauslöser & Telemetrie", "Installationsmethoden"],
        "es": ["Descripción del producto", "Especificaciones técnicas", "Características clave", "Guía de configuración", "Galería del producto", "Guía de operación", "Activación por movimiento y telemetría", "Métodos de instalación"],
        "fr": ["Présentation du produit", "Spécifications techniques", "Caractéristiques principales", "Guide de configuration", "Galerie du produit", "Guide d'utilisation", "Détection de mouvement et télémétrie", "Méthodes d'installation"],
        "pt": ["Visão geral do produto", "Especificações técnicas", "Principais recursos", "Guia de configuração", "Galeria do produto", "Guia de operação", "Gatilho de movimento e telemetria", "Métodos de instalação"],
        "ru": ["Обзор продукта", "Технические характеристики", "Ключевые свойства", "Руководство по настройке", "Галерея продукта", "Руководство по эксплуатации", "Триггеры движения и телеметрия", "Способы установки"]
    }
    
    # Run replacements
    if lang in header_maps:
        for en_h, loc_h in header_maps[lang].items():
            translated = translated.replace(en_h, loc_h)
    elif lang in translation_headers:
        loc_list = translation_headers[lang]
        for i, en_h in enumerate(headers):
            translated = translated.replace(f"## {en_h}", f"## {loc_list[i]}")

    # Specific text translations or fallbacks
    # Let's keep it simple, clean and correct.
    # Replace CTA with localized alert
    cta_alert = LANDING_INFO.get(lang, LANDING_INFO["zh-tw"])["cta"]
    # Locating alert block
    translated = re.sub(
        r'\{\{< alert >\}\}.*?\{\{< /alert >\}\}',
        f'{{{{< alert >}}}}\n{cta_alert}\n{{{{</alert >}}}}',
        translated,
        flags=re.DOTALL
    )

    return translated

def update_localized_products_index(lang):
    # Map title and descriptions for overview cards
    card_info = {
        "zh-tw": {
            "title": "iBeacon 藍牙信標",
            "desc": "專業 BLE 5.0 信標，支援室內定位、考勤打卡、智慧人員管理與資產追蹤。"
        },
        "zh-cn": {
            "title": "iBeacon 蓝牙信标",
            "desc": "专业 BLE 5.0 信标，支持室内定位、考勤打卡、智能人员管理与资产追踪。"
        },
        "ja": {
            "title": "iBeacon ビーコン",
            "desc": "屋内位置測位、勤怠管理、人員管理、および資産追跡用のプロフェッショナル BLE 5.0 ビーコン。"
        },
        "ar": {
            "title": "منارات iBeacon",
            "desc": "منارات BLE 5.0 احترافية لتحديد المواقع الداخلي، وتسجيل الحضور، وإدارة الأفراد، وتتبع الأصول."
        },
        "de": {
            "title": "iBeacon BLE Beacons",
            "desc": "Professionelle BLE 5.0 Beacons für Indoor-Lokalisierung, Anwesenheitskontrolle, Personenmanagement und Asset-Tracking."
        },
        "es": {
            "title": "Balizas iBeacon BLE",
            "desc": "Balizas profesionales BLE 5.0 para localización en interiores, control de asistencia, gestión de personal y seguimiento de activos."
        },
        "fr": {
            "title": "Balises iBeacon BLE",
            "desc": "Balises professionnelles BLE 5.0 pour la localisation en intérieur, la gestion intelligente des présences et le suivi d'actifs."
        },
        "pt": {
            "title": "Beacons iBeacon BLE",
            "desc": "Beacons profissionais BLE 5.0 para localização interna, controle de ponto, gestão de pessoal e rastreamento de ativos."
        },
        "ru": {
            "title": "Маяки iBeacon BLE",
            "desc": "Профессиональные маяки BLE 5.0 для позиционирования в помещениях, учета времени, контроля персонала и отслеживания активов."
        }
    }
    
    info = card_info.get(lang, card_info["zh-tw"])
    title = info["title"]
    desc = info["desc"]

    path = f"content/{lang}/products/_index.md"
    if not os.path.exists(path):
        print(f"Index file {path} not found!")
        return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if ibeacon card already exists
    if "products/ibeacon/" in content:
        print(f"iBeacon card already exists in {path}")
        return

    # Find the cards group closure or insert right after graphiccard card
    # We will search for the graphiccard block:
    # {{< card title="..." href="/{lang}/products/graphiccard/" ... >}} ... {{< /card >}}
    # And append the ibeacon card.
    
    # We use regex to find graphiccard card block
    pattern = r'(\{\{<\s*card\s+title="[^"]+"\s+href="[^"]*products/graphiccard/".*?\{\{<\s*/card\s*>\}\})'
    match = re.search(pattern, content, flags=re.DOTALL)
    if not match:
        # Fallback: search for first card-group end
        print(f"Could not locate graphiccard card block in {path}, appending at end of card group.")
        content = content.replace("{{< /card-group >}}", f'  {{{{< card title="{title}" href="/{lang}/products/ibeacon/" >}}}}\n    {desc}\n  {{{{</card >}}}}\n{{{{</card-group >}}}}')
    else:
        graphiccard_block = match.group(1)
        ibeacon_card = f'\n  {{{{< card title="{title}" href="/{lang}/products/ibeacon/" >}}}}\n    {desc}\n  {{{{</card >}}}}'
        content = content.replace(graphiccard_block, graphiccard_block + ibeacon_card)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Added iBeacon card to {path}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Project root directory: {base_dir}")

    # Read English templates first
    en_templates = {}
    en_base_path = os.path.join(base_dir, "content/en/products/ibeacon")
    
    for model in ["ypb01", "ypb02", "ypb03", "ypb04", "ypb05"]:
        p_file = os.path.join(en_base_path, model, "_index.md")
        with open(p_file, "r", encoding="utf-8") as f:
            en_templates[model] = f.read()

    # Generate directories and files for each language
    for lang in LANGUAGES:
        print(f"\nProcessing language: {lang.upper()}")
        lang_dir = os.path.join(base_dir, "content", lang, "products", "ibeacon")
        os.makedirs(lang_dir, exist_ok=True)
        
        # 1. Generate Landing Page
        landing_md = generate_category_index(lang, LANDING_INFO[lang])
        landing_path = os.path.join(lang_dir, "_index.md")
        with open(landing_path, "w", encoding="utf-8") as f:
            f.write(landing_md)
        print(f"Created category index at: {landing_path}")

        # 2. Generate Product Subpages
        for model in ["ypb01", "ypb02", "ypb03", "ypb04", "ypb05"]:
            prod_dir = os.path.join(lang_dir, model)
            os.makedirs(prod_dir, exist_ok=True)
            
            translated_content = translate_product_page(lang, model, EN_BLUEPRINTS[model], en_templates[model])
            prod_path = os.path.join(prod_dir, "_index.md")
            with open(prod_path, "w", encoding="utf-8") as f:
                f.write(translated_content)
            print(f"Created product page for {model.upper()} at: {prod_path}")

        # 3. Add to products index page
        update_localized_products_index(lang)

    print("\nGeneration process complete!")

if __name__ == "__main__":
    main()
