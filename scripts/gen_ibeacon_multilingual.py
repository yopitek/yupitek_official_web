#!/usr/bin/env python3
import os
import re

LANGUAGES = ["zh-tw", "zh-cn", "ja", "ar", "de", "es", "fr", "pt", "ru"]

LANDING_INFO = {
    "zh-tw": {
        "title": "Yupitek iBeacon 系列 — BLE 5.0 藍牙信標",
        "desc": "Yupitek 代理專業 BLE 5.0 iBeacon 與 Eddystone 藍牙信標：YPB01、YPB02、YPB03、YPB04、YPB05，適用於室內定位、考勤打卡與資產追蹤。",
        "intro": "Yupitek iBeacon 產品是新一代藍牙低功耗 (BLE 5.0) 信標裝置，適用於高性能定位、人員追蹤與商業廣告推播。支援 Apple iBeacon™ 和 Google Eddystone™ (UID, URL, TLM) 協定，可同時廣播最多 6 個通道的多協定訊號，並能透過 BeaconSET+ 行動 App 進行配置。",
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
        "intro": "Yupitek iBeacon 产品是新一代蓝牙低功耗 (BLE 5.0) 信标设备，适用于高性能定位、人员追踪与商业广告推送。支持 Apple iBeacon™ 和 Google Eddystone™ (UID, URL, TLM) 协议，可同时广播最多 6 个通道的多协议信号，并能通过 BeaconSET+ 移动 App 进行配置。",
        "topo_title": "蓝牙信标系统架构",
        "topo_desc": "我们的 iBeacon 生态系统将物理位置与企业云网络连接起来。信标以定期时间间隔发射 BLE 信号，这些信号由移动设备（运行企业 App） and BLE 网关扫描，并将安全日志转发到中央考勤和资产追踪系统。",
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
        "intro": "Os beacons iBeacon da Yupitek representam uma nova geração de dispositivos Bluetooth® Low Energy (BLE 5.0) projetados para localização de alta performance, rastreamento de pessoal e marketing de proximidade. Com suporte simultâneo aos produtos Apple iBeacon™ e Google Eddystone™ (UID, URL, TLM), nossos beacons suportam transmissões em até 6 canais configurados via aplicativo BeaconSET+.",
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

SPEC_DICTS = {
    "zh-tw": {
        "Chip Model": "晶片型號", "Bluetooth Version": "藍牙版本", "Waterproof Level": "防水等級", "Transmission Range": "傳輸距離", "Antenna Impedance": "天線阻抗", "Power Source": "電源規格", "Operating Voltage": "工作電壓", "Peak Current": "峰值電流", "Dimensions": "外觀尺寸", "Default Settings": "預設參數", "Sensor": "感測器", "Sensors": "感測器", "Feedback Elements": "反饋機制", "Control Button": "控制按鈕", "RFID Compatibility": "RFID 相容性", "Battery Lifetime": "電池壽命", "Charging Time": "充電時間", "Dimensions & Weight": "外觀尺寸與重量", "Net Weight": "淨重", "Material": "外殼材質", "Max Current": "最大電流", "Protocol Support": "協定支援", "Service UUID": "服務 UUID", "Service Data Format": "服務數據格式",
        "nRF52 series": "nRF52 系列", "BLE 5.0": "BLE 5.0 (低功耗藍牙)", "IP67": "IP67 (防塵防水)", "IP65": "IP65 (防塵防潑水)", "Up to 100 meters": "最遠 100 公尺 (開闊空間)", "Up to 240 meters": "最遠 240 公尺 (開闊空間)", "Up to 150 meters (492 ft)": "最遠 150 公尺 (492 英尺，開闊空間)", "Up to 50 meters": "最遠 50 公尺 (開闊空間)", "50 ohm": "50 歐姆", "1 × CR2477 coin battery": "1 × CR2477 鈕扣電池", "4 × AA batteries": "4 × AA (三號) 乾電池", "Magnetic charging Li-po battery": "磁吸充電式鋰聚合物電池 (270mAh)", "Powered by USB slot (No battery)": "Micro USB 插槽供電 (無電池)", "Up to 10 years": "最長可達 10 年 (預設參數下)", "Up to 3 months": "最長可達 3 個月 (一般按壓頻率)", "Approximately 2 hours": "約 2 小時 (室溫，5V/1A 電源供應器)", "ABS + Silicone": "ABS 塑膠 + 矽膠", "1 × Vibration Motor, 1 × RGB LED": "1 × 震動馬達，1 × RGB LED 指示燈", "1 × External physical button": "1 × 外部實體按鈕", "LF / HF / UHF": "低頻(LF) / 高頻(HF) / 超高頻(UHF) (選配)", "Compact circular shape": "緊湊圓形", "Wall-mountable square": "壁掛方形", "Ultra-low power consumption": "超低功耗晶片", "High efficiency and speed": "高傳輸效率與速率", "Splash and dust resistant (1m immersion)": "防塵防水 (支援短時間浸入 1 公尺水中)", "Open space": "開闊空間", "On-board / PCB Antenna": "板載 PCB 天線", "Replaceable (3.0V, 1000mAh)": "可更換 (3.0V, 1000mAh)", "DC": "直流電", "Tested at 0dBm transmission power": "於 0dBm 廣播功率測試", "Tested at 0dBm": "於 0dBm 測試", "Configurable via App": "可透過 App 自訂修改", "LIS3DH 3-axis accelerometer": "LIS3DH 三軸加速度感測器", "X, Y, Z axes telemetry": "X、Y、Z 三軸數據", "Low latency and high efficiency": "低延遲與高效率", "High range and throughput": "長距離與高傳輸量", "Dustproof and water-jet resistant": "防塵與防低壓噴水", "Maximum in open areas": "開闊空間最大距離", "5800mAh capacity total (Included)": "總容量 5800mAh (隨附)", "Based on default broadcasting parameters": "基於預設廣播參數", "Rugged industrial casing": "堅固工業外殼", "Including batteries": "含電池", "Secure connection and long range": "安全連線與長距離", "Displacement and movement detection": "位移與運動檢測", "Tactile and visual cues": "觸覺與視覺提示", "Activates triggers and alarms": "啟用觸發器與警報", "Optional build integrations": "選配整合", "Slim card format": "超薄卡片格式", "Pocket-sized": "口袋型", "Continuous operation": "持續不間斷運作", "Ultra-lightweight (2.0g)": "超輕量 2.0 公克", "Plug & play, software reboot": "隨插即用，支援指令重啟",
        "LINE Simple Beacon / iBeacon": "LINE Simple Beacon / iBeacon", "0xFE6F": "0xFE6F", "0xFE6F + 5-Byte HWID + 0x7F00": "0xFE6F + 5位元組 HWID + 0x7F00"
    },
    "zh-cn": {
        "Chip Model": "芯片型号", "Bluetooth Version": "蓝牙版本", "Waterproof Level": "防水等级", "Transmission Range": "传输距离", "Antenna Impedance": "天线阻抗", "Power Source": "电源规格", "Operating Voltage": "工作电压", "Peak Current": "峰值电流", "Dimensions": "外观尺寸", "Default Settings": "默认参数", "Sensor": "传感器", "Sensors": "传感器", "Feedback Elements": "反馈机制", "Control Button": "控制按钮", "RFID Compatibility": "RFID 兼容性", "Battery Lifetime": "电池寿命", "Charging Time": "充电时间", "Dimensions & Weight": "外观尺寸与重量", "Net Weight": "净重", "Material": "外壳材质", "Max Current": "最大电流", "Protocol Support": "协议支持", "Service UUID": "服务 UUID", "Service Data Format": "服务数据格式",
        "nRF52 series": "nRF52 系列", "BLE 5.0": "BLE 5.0 (低功耗蓝牙)", "IP67": "IP67 (防尘防水)", "IP65": "IP65 (防尘防泼水)", "Up to 100 meters": "最远 100 米 (开阔空间)", "Up to 240 meters": "最远 240 米 (开阔空间)", "Up to 150 meters (492 ft)": "最远 150 米 (492 英尺，开阔空间)", "Up to 50 meters": "最远 50 米 (开阔空间)", "50 ohm": "50 欧姆", "1 × CR2477 coin battery": "1 × CR2477 纽扣电池", "4 × AA batteries": "4 × AA (三号) 干电池", "Magnetic charging Li-po battery": "磁吸充电式锂聚合物电池 (270mAh)", "Powered by USB slot (No battery)": "Micro USB 插槽供电 (无电池)", "Up to 10 years": "最长可达 10 年 (默认参数下)", "Up to 3 months": "最长可达 3 个月 (一般按压频率)", "Approximately 2 hours": "约 2 小时 (室温，5V/1A 电源适配器)", "ABS + Silicone": "ABS 塑料 + 硅胶", "1 × Vibration Motor, 1 × RGB LED": "1 × 震动马达，1 × RGB LED 指示灯", "1 × External physical button": "1 × 外部实体按钮", "LF / HF / UHF": "低频(LF) / 高频(HF) / 超高频(UHF) (选配)", "Compact circular shape": "紧凑圆形", "Wall-mountable square": "壁挂方形", "Ultra-low power consumption": "超低功耗芯片", "High efficiency and speed": "高传输效率与速率", "Splash and dust resistant (1m immersion)": "防尘防水 (支持短时间浸入 1 米水中)", "Open space": "开阔空间", "On-board / PCB Antenna": "板载 PCB 天线", "Replaceable (3.0V, 1000mAh)": "可更换 (3.0V, 1000mAh)", "DC": "直流电", "Tested at 0dBm transmission power": "于 0dBm 广播功率测试", "Tested at 0dBm": "于 0dBm 测试", "Configurable via App": "可透过 App 自定义修改", "LIS3DH 3-axis accelerometer": "LIS3DH 三轴加速度传感器", "X, Y, Z axes telemetry": "X、Y、Z 三轴数据", "Low latency and high efficiency": "低延迟与高效率", "High range and throughput": "长距离与高传输量", "Dustproof and water-jet resistant": "防尘与防低压喷水", "Maximum in open areas": "开阔空间最大距离", "5800mAh capacity total (Included)": "总容量 5800mAh (随附)", "Based on default broadcasting parameters": "基于默认广播参数", "Rugged industrial casing": "坚固工业外壳", "Including batteries": "含电池", "Secure connection and long range": "安全连线与长距离", "Displacement and movement detection": "位移与运动检测", "Tactile and visual cues": "触觉与视觉提示", "Activates triggers and alarms": "启用触发器与警报", "Optional build integrations": "选配整合", "Slim card format": "超薄卡片格式", "Pocket-sized": "口袋型", "Continuous operation": "持续不间断运作", "Ultra-lightweight (2.0g)": "超轻量 2.0 克", "Plug & play, software reboot": "即插即用，支持指令重启",
        "LINE Simple Beacon / iBeacon": "LINE Simple Beacon / iBeacon", "0xFE6F": "0xFE6F", "0xFE6F + 5-Byte HWID + 0x7F00": "0xFE6F + 5字节 HWID + 0x7F00"
    }
}

# Auto-translation templates for paragraphs in other languages
BODY_TEMPLATES = {
    "ar": {
        "ypb01": {
            "body": "## نظرة عامة على المنتج\n\nإنّ **YPB01** هو منارة بلوتوث منخفض الطاقة (BLE 5.0) صغيرة وقوية، مصممة لأنظمة تحديد المواقع الداخلية ومراقبة النشاط وتتبع الأصول. تعتمد على رقاقة nRF52 ذات الاستهلاك المنخفض للغاية، وتبث إطارات iBeacon و Eddystone (UID, URL, TLM) في وقت واحد.\n\nيسمح هيكلها الدوار الميكانيكي الذكي باستبدال بطارية العملة المعدنية بسهولة مع تحقيق تصنيف مقاومة الماء والغبار IP67، مما يجعلها مثالية للبيئات الرطبة أو الصعبة.\n\n---\n\n## الميزات الرئيسية\n\n* **هيكل حماية عالٍ:** تصنيف IP67 مقاوم للماء والغبار، مما يسمح بالتركيب الداخلي والخارجي الخفيف.\n* **بطارية قابلة للاستبدال:** بطارية CR2477 طويلة الأمد (1000 مللي أمبير) سهلة الاستبدال عبر الهيكل الدوار.\n* **بث متزامن:** يدعم البث في ما يصل إلى 6 فتحات إعلانية مختلفة في وقت واحد لبروتوكولات iBeacon و Eddystone.\n* **زر طاقة مادي:** زر ضغط داخلي لتشغيل أو إيقاف المنارة لحفظ البطارية أثناء النقل والتخزين.\n\n---\n\n## دليل التشغيل\n\n### كيفية تشغيل المنارة\n1. افتح الهيكل الدوار باتجاه عقارب الساعة.\n2. اضغط مع الاستمرار على \"الزر الداخلي\" لمدة **3 ثوانٍ**.\n3. سيضيء مؤشر LED الأزرق لمدة **5 ثوانٍ** ثم ينطفئ. منارة YPB01 نشطة الآن وتبث.\n\n### كيفية إيقاف تشغيل المنارة\n1. اضغط مع الاستمرار على الزر الداخلي لمدة **3 ثوانٍ**.\n2. سيومض مؤشر LED الأزرق لمدة **5 ثوانٍ** ثم ينطفئ. المنارة مغلقة الآن.\n\n---\n\n## إرشادات التهيئة\n\nيتم تهيئة معلمات YPB01 (بما في ذلك UUID و Major و Minor وقوة الإرسال وفاصل البث) لاسلكياً عبر تطبيق **BeaconSET**:\n1. قم بتنزيل **BeaconSET** من Google Play أو Apple App Store.\n2. تأكد من تمكين خدمات البلوتوث والموقع على هاتفك.\n3. افتح التطبيق، وامسح ضوئياً بحثاً عن عنوان MAC للمنارة، وانقر للاتصال.\n4. أدخل كلمة مرور التهيئة الافتراضية الآمنة لفتح وتعديل المعلمات."
        },
        "ypb02": {
            "body": "## نظرة عامة على المنتج\n\nإنّ **YPB02** هو منارة بلوتوث منخفض الطاقة (BLE 5.0) مستشعرة للحركة ومجهزة بمستشعر تسارع ثلاثي المحاور **LIS3DH**. تشارك نفس الحجم الصغير، والبطارية القابلة للاستبدال CR2477 (1000 مللي أمبير)، والهيكل المقاوم للماء والغبار IP67 للمنارة YPB01، ولكن يضيف YPB02 كشف الحركة الذكي والقياس عن بعد.\n\nتدعم المنارة البث المعتمد على المحفزات، مما يسمح لها ببث بيانات التسارع في الوقت الفعلي أو تعديل فاصل البث فقط عند الحركة أو الاهتزاز أو في حالة السقوط.\n\n---\n\n## الميزات الرئيسية\n\n* **مستشعر تسارع ثلاثي المحاور:** مستشعر LIS3DH لرسم خرائط الحركة والميل على محاور X و Y و Z.\n* **البث المعتمد على المحفزات:** يدعم التهيئة لبث الحركة فقط، وتنبيهات السقوط، أو تغيير الفاصل إلى 100 مللي ثانية عند الحركة.\n* **هيكل حماية عالٍ:** تصنيف IP67 مقاوم للماء والغبار.\n* **بطارية قابلة للاستبدال:** استخدام بطارية CR2477 طويلة الأمد سهلة الاستبدال.\n\n---\n\n## استشعار الحركة والقياس عن بعد\n\nباستخدام مستشعر LIS3DH، يدعم YPB02:\n1. **البث القائم على النشاط:** يبث إطارات قياسية باستمرار، ولكنه يحفز إطارات بيانات المستشعر فقط عند الحركة.\n2. **الوضع المزدوج:** يظل صامتاً في وضع السكون عند الثبات، ويبث بفاصل 100 مللي ثانية عند الحركة.\n3. **معايرة العتبة:** يمكن تخصيص عتبات التسارع ومدة المحفز داخل التطبيق.\n\n---\n\n## إرشادات التهيئة\n\nيتم تهيئة المعلمات لاسلكياً عبر تطبيق **BeaconSET+**:\n1. قم بتنزيل **BeaconSET+**.\n2. تأكد من تمكين خدمات البلوتوث والموقع.\n3. امسح واتصل بالمنارة عبر عنوان MAC.\n4. أدخل كلمة المرور لتعديل وحفظ المعلمات."
        },
        "ypb03": {
            "body": "## نظرة عامة على المنتج\n\nإنّ **YPB03** هو منارة صناعية طويلة المدى للبلتوث منخفض الطاقة (BLE 5.0) ومحسنة خصيصاً لتعمل كـ **LINE Beacon** تبث حزم **LINE Simple Beacon** القياسية. تعمل بـ **4 بطاريات AA** بسعة 5800 مللي أمبير، وتتميز بعمر بطارية يصل إلى **10 سنوات**.\n\nبفضل هوائي الكسب العالي، يصل مدى البث إلى **240 متراً**، وهو الخيار الأمثل للمساحات التجارية الكبيرة. لا يحتاج المستخدمون إلى تثبيت تطبيقات إضافية، بل يتلقون الإشعارات مباشرة في تطبيق **LINE**.\n\n---\n\n## الميزات الرئيسية\n\n* **توافق رسمي مع LINE Beacon:** يبث بروتوكول LINE Simple Beacon المفتوح للربط مع API لـ LINE Bot.\n* **عمر بطارية 10 سنوات:** سعة 5800 مللي أمبير باستخدام 4 بطاريات AA شائعة يقلل الصيانة.\n* **مدى 240 متراً:** إشارة BLE 5.0 قوية تغطي الصالات الكبيرة والمطارات.\n* **تفاعل سلس:** يحتاج المستخدم فقط لتفعيل البلوتوث ومتابعة حسابك الرسمي.\n* **هيكل IP65:** هيكل ABS متين ومقاوم للغبار ورذاذ الماء للاستخدام الصناعي.\n\n---\n\n## دليل تكامل LINE Beacon للمطورين\n\n### كيف تعمل disparadores التقارب\nعندما يدخل مستخدم لديه بلوتوث و LINE Beacon نطاق الإشارة:\n1. يكتشف تطبيق LINE **UUID الخدمة `0xFE6F`** ويقرأ معرف الأجهزة (HWID).\n2. ترسل منصة LINE حدث `beacon` إلى خادم Webhook الخاص بالبوت.\n3. يستجيب البوت في الوقت الفعلي بكوبونات أو معلومات ملاحة.\n\n```mermaid\nsequenceDiagram\n    participant User as المستخدم (تطبيق LINE)\n    participant Beacon as YPB03 (0xFE6F + HWID)\n    participant LINE as منصة LINE\n    participant Bot as خادم Webhook (البوت)\n\n    Beacon->>User: بث BLE (UUID: FE6F + HWID)\n    User->>LINE: توجيه HWID + User ID\n    LINE->>Bot: Webhook POST (حدث beacon: enter/stay/banner)\n    Bot->>User: استجابة API (مثل كوبون)\n```\n\n### الخطوة 1: تسجيل معرف الأجهزة (HWID)\n1. قم بتسجيل الدخول إلى **LINE Developers Console** أو **LINE Official Account Manager**.\n2. انتقل إلى قسم Beacon وسجل الجهاز للحصول على **HWID المكون من 5 بايت (10 رموز ست عشرية)**.\n\n### الخطوة 2: تهيئة YPB03 عبر BeaconSET+\n1. قم بتنزيل **BeaconSET+** واتصل بالمنارة (يتطلب كلمة مرور).\n2. اضبط إحدى قنوات البث كـ **Service Data** مع:\n   - **Service UUID:** `FE6F`\n   - **Data Value:** `FE6F` + `[HWID الخاص بك]` + `7F00` (مثال: `FE6F01234567897F00`).\n3. احفظ واقطع الاتصال. ستبدأ المنارة ببث إشارة LINE Beacon.\n\n### الخطوة 3: معالجة حدث الويب هوك\nسيتلقى خادمك كائن JSON يحتوي تفاصيل `beacon`:\n* **`hwid`**: معرف الأجهزة للمنارة.\n* **`type`**: نوع الإجراء (`enter` عند الدخول، `stay` يرسل كل 10 ثوانٍ عند البقاء، `banner` عند النقر على الإعلان).\n\n---\n\n## طرق التثبيت\n\n### الطريقة أ: شريط لاصق صناعي\n* **الأسطح:** الزجاج، الأكريليك، الألومنيوم النظيف.\n* **العملية:** نظف السطح. اضغط على الشريط (ثانيتين)، انتظر 30 دقيقة وثبت المنارة.\n\n### الطريقة ب: التثبيت ببراغي ودعامة (موصى به)\n* **الأسطح:** الخرسانة، الخشب، الطوب.\n* **العملية:** ثبت الدعامة على الجدار باستخدام البراغي. أدخل YPB03 حتى يستقر في مكانه.\n\n---\n\n## إرشادات التهيئة\n\nيتم تعديل المعلمات لاسلكياً عبر **BeaconSET+**:\n1. قم بتنزيل **BeaconSET+** وفعل البلوتوث.\n2. ابحث عن المنارة واتصل بكلمة المرور.\n3. قم بتهيئة UUID و Major و Minor وقوة الإرسال والفاصل."
        },
        "ypb04": {
            "body": "## نظرة عامة على المنتج\n\nإنّ **YPB04** هو منارة قابلة لإعادة الشحن بتصميم مسطح كبطاقة (شارة) مصممة لإدارة حضور الموظفين وتتبع التدفق. خفيفة جداً (19 جم) وبأبعاد 86 × 55 × 6 مم، يسهل حملها بالقلادة.\n\nتتميز بـ **زر مادي** و **محرك اهتزاز** و **مؤشر LED RGB** للاستجابة المادية والمرئية. تتضمن منفذ شحن مغناطيسي، ومستشعر تسارع، وتوافقاً اختيارياً مع **RFID (LF/HF/UHF)**.\n\n---\n\n## الميزات الرئيسية\n\n* **مستشعر تسارع ثلاثي المحاور:** كشف الحركة للتحكم في فاصل بث الإشارة.\n* **استجابة مرئية/مادية:** محرك اهتزاز و LED RGB للإنذارات.\n* **زر التحكم:** زر خارجي لإطلاق إنذارات الطوارئ (SOS).\n* **تكامل RFID:** رقاقة اختيارية لقارئات الدخول التقليدية.\n* **بطارية مغناطيسية:** بطارية Li-po قابلة لإعادة الشحن بسعة 270 مللي أمبير تدوم حتى 3 أشهر.\n\n---\n\n## دليل التشغيل\n\n### التشغيل\n* اضغط على الزر المادي لمدة **3 ثوانٍ**.\n* سيضيء مؤشر LED الأزرق لمدة 3 ثوانٍ ويهتز الجهاز مرة واحدة للاتصال.\n\n### إيقاف التشغيل\n* للأمان، يتم الإيقاف لاسلكياً فقط عبر تطبيق **BeaconSET+** (يتطلب كلمة مرور).\n* عند الإيقاف، سيومض مؤشر LED الأزرق 5 مرات.\n\n### حالة البطارية والشحن\n* **البطارية منخفضة:** تحت 20%، يومض مؤشر LED الأحمر كل 3 ثوانٍ.\n* **جاري الشحن:** مؤشر LED الأحمر يضيء باستمرار.\n* **اكتمال الشحن:** مؤشر LED الأخضر يضيء باستمرار.\n\n### محفزات الزر\n* **نقرة مزدوجة:** يومض مؤشر LED الأزرق مرتين ويهتز المحرك مرة واحدة.\n* **نقرة ثلاثية:** يومض مؤشر LED الأزرق 3 مرات ويهتز المحرك مرتين.\n\n---\n\n## إرشادات التهيئة\n\nاستخدم تطبيق **BeaconSET+** لتهيئة الشارة:\n1. ثبت التطبيق وفعل البلوتوث.\n2. اتصل بـ MAC الخاص بالشارة.\n3. أدخل كلمة المرور لتعديل المعلمات وتصرفات الزر."
        },
        "ypb05": {
            "body": "## نظرة عامة على المنتج\n\nإنّ **YPB05** هو منارة بلوتوث صغيرة جداً (BLE 5.0) بدون بطارية تعمل مباشرة من أي منفذ USB. تزن **2.0 جم** فقط وتبلغ أبعادها **18 × 14 × 6 مم**، مما يوفر حلاً سهلاً للتشغيل الفوري (plug-and-play).\n\nنظراً لأنها تعمل بدون بطارية، فهي مثالية للبث التجاري المستمر والتسويق الداخلي في المتاجر وتحديد المواقع في المكاتب.\n\n---\n\n## الميزات الرئيسية\n\n* **تشغيل مستمر:** التغذية عبر USB تلغي الحاجة لاستبدال وصيانة البطاريات.\n* **خفيفة وصغيرة جداً:** تثبيت غير مرئي في أي منفذ USB.\n* **تشغيل فوري:** تعمل بمجرد توصيلها بمصدر الطاقة دون الحاجة لأزرار.\n* **إعادة تشغيل برمجية:** تدعم إرسال أوامر إعادة التشغيل لاسلكياً.\n\n---\n\n## إرشادات التهيئة\n\nيتم تهيئتها لاسلكياً عبر **BeaconSET+**:\n1. قم بتنزيل **BeaconSET+** وشغل البلوتوث.\n2. اتصل بـ YPB05 عن طريق مسح عنوان MAC.\n3. أدخل كلمة المرور وقم بتهيئة UUID و Major و Minor وقوة الإرسال والفاصل."
        },
    },
    "de": {
        "ypb01": {
            "body": "## Produktübersicht\n\nDer **YPB01** ist ein kompakter, robuster Bluetooth® Low Energy (BLE 5.0) Coin-Cell-Beacon für Indoor-Lokalisierung, Aktivitätsüberwachung und Asset-Tracking. Basierend auf dem nRF52-Chipsatz strahlt er iBeacon- und Eddystone-Signale (UID, URL, TLM) gleichzeitig aus.\n\nDas drehbare Gehäuse ermöglicht einen einfachen Batteriewechsel (CR2477) bei gleichzeitigem IP67-Schutz, was den Beacon ideal für feuchte Umgebungen macht.\n\n---\n\n## Hauptmerkmale\n\n* **IP67 Schutz:** Staub- und wasserdicht für Innen- und leichten Außeneinsatz.\n* **Austauschbare Batterie:** Langlebige CR2477-Batterie (1000mAh) über drehbaren Deckel leicht zu wechseln.\n* **Simultane Ausstrahlung:** Bis zu 6 Werbe-Slots gleichzeitig für iBeacon- und Eddystone-Protokolle.\n* **Interner Einschaltknopf:** Mechanischer Taster im Inneren spart Strom bei Lagerung und Transport.\n\n---\n\n## Bedienungsanleitung\n\n### Beacon einschalten\n1. Gehäuse durch Drehen im Uhrzeigersinn öffnen.\n2. Den internen Taster für **3 Sekunden** gedrückt halten.\n3. Die blaue LED leuchtet für **5 Sekunden** auf. Der YPB01 ist nun aktiv.\n\n### Beacon ausschalten\n1. Den internen Taster für **3 Sekunden** gedrückt halten.\n2. Die blaue LED blinkt für **5 Sekunden** und erlischt. Der Beacon ist ausgeschaltet.\n\n---\n\n## Konfigurationsanleitung\n\nDie Parameter des YPB01 (UUID, Major, Minor, Sendeleistung und Intervall) werden drahtlos über die **BeaconSET** App konfiguriert:\n1. Laden Sie **BeaconSET** aus dem Google Play oder Apple App Store herunter.\n2. Aktivieren Sie Bluetooth und Standortdienste.\n3. Öffnen Sie die App, suchen Sie die MAC-Adresse des Beacons und verbinden Sie sich.\n4. Geben Sie das Passwort ein, um die Parameter zu bearbeiten."
        },
        "ypb02": {
            "body": "## Produktübersicht\n\nDer **YPB02** ist ein Bluetooth® Low Energy (BLE 5.0) Bewegungssensor-Beacon mit integriertem **LIS3DH 3-Achsen-Beschleunigungssensor**. Er teilt das Gehäuse, die CR2477-Batterie und die IP67-Schutzklasse mit dem YPB01, bietet jedoch zusätzlich intelligente Bewegungserkennung.\n\nDer Beacon unterstützt triggerbasierte Werbung, um Beschleunigungsdaten in Echtzeit zu senden oder das Sendeintervall nur bei Bewegung, Vibration oder Sturz zu verkürzen.\n\n---\n\n## Hauptmerkmale\n\n* **3-Achsen-Beschleunigungssensor:** LIS3DH-Sensor zur Erfassung von Bewegung, Neigung und Beschleunigung auf X-, Y- und Z-Achsen.\n* **Triggerbasierte Ausstrahlung:** Nur bei Bewegung senden, Sturzalarm senden oder das Intervall bei Bewegung auf 100 ms verkürzen.\n* **IP67 Schutz:** Staub- und wasserdicht.\n* **Austauschbare Batterie:** Einfacher Austausch der CR2477-Münzzelle.\n\n---\n\n## Bewegungsauslöser & Telemetrie\n\nUnterstützt durch den LIS3DH-Sensor bietet der YPB02:\n1. **Aktivitätsabhängiges Senden:** Sendet Standard-Frames dauerhaft, triggert Sensordaten-Frames jedoch nur bei Bewegung.\n2. **Ruhe- und Bewegungsmodus:** Schläft im Stillstand und sendet im 100ms-Intervall, sobald sich das Asset bewegt.\n3. **Schwellenwert-Kalibrierung:** Bewegungsschwellen und Dauer sind in der App konfigurierbar.\n\n---\n\n## Konfigurationsanleitung\n\nDie Konfiguration erfolgt drahtlos über die **BeaconSET+** App:\n1. Laden Sie **BeaconSET+** herunter.\n2. Aktivieren Sie Bluetooth und Standortdienste.\n3. Suchen Sie nach der MAC-Adresse und verbinden Sie sich.\n4. Geben Sie das Passwort ein, um die Bewegungsschwellen und andere Parameter anzupassen."
        },
        "ypb03": {
            "body": "## Produktübersicht\n\nDer **YPB03** is ein industrieller Bluetooth® Low Energy (BLE 5.0) Beacon, der als **LINE Beacon** optimiert ist und standardisierte **LINE Simple Beacon** Pakete sendet. Betrieben mit **4 × AA-Batterien** (5800mAh), erreicht er eine Lebensdauer von **bis zu 10 Jahren**.\n\nMit einer Sendeleistung von bis zu **240 Metern** eignet sich der YPB03 ideal für große Hallen, Museen und Einkaufszentren. Kunden benötigen keine separate App – sie empfangen Push-Benachrichtigungen direkt in ihrer **LINE** App.\n\n---\n\n## Hauptmerkmale\n\n* **Offizielle LINE Beacon Kompatibilität:** Sendet das LINE Simple Beacon Protokoll für die direkte Verknüpfung mit der LINE Bot Messaging API.\n* **10 Jahre Batterielaufzeit:** Große 5800mAh Kapazität mit vier Standard-AA-Batterien reduziert den Wartungsaufwand.\n* **240m Reichweite:** Leistungsstarke BLE 5.0 Reichweite für Messehallen und Bahnhöfe.\n* **Nahtlose Interaktion:** Benutzer müssen nur Bluetooth aktivieren und Ihren Kanal hinzufügen – kein App-Download nötig.\n* **IP65-Gehäuse:** Robustes, strahlwassergeschütztes Gehäuse für den industriellen Einsatz.\n\n---\n\n## LINE Beacon Entwicklerhandbuch\n\n### Funktionsweise der Näherungstrigger\nWenn ein Benutzer mit aktivem Bluetooth und LINE Beacon die Reichweite betritt:\n1. Die LINE App erkennt die **Service UUID `0xFE6F`** und liest die Hardware-ID (HWID).\n2. Die LINE Plattform sendet ein `beacon` Event an Ihren Bot Webhook-Server.\n3. Ihr Server reagiert in Echtzeit mit Gutscheinen, Nachrichten oder Wegbeschreibungen.\n\n```mermaid\nsequenceDiagram\n    participant User as Benutzer (LINE App)\n    participant Beacon as YPB03 (0xFE6F + HWID)\n    participant LINE as LINE Plattform\n    participant Bot as Webhook-Server (Bot)\n\n    Beacon->>User: BLE Broadcast (UUID: FE6F + HWID)\n    User->>LINE: HWID + User ID weiterleiten\n    LINE->>Bot: Webhook POST (beacon event: enter/stay/banner)\n    Bot->>User: Antwort über Messaging API (z. B. Coupon)\n```\n\n### Schritt 1: Hardware-ID (HWID) registrieren\n1. Gehen Sie in das **LINE Developers Portal** oder den **LINE Official Account Manager**.\n2. Registrieren Sie das Gerät und notieren Sie sich die **5-Byte (10 Hex-Zeichen) HWID**.\n\n### Schritt 2: YPB03 über BeaconSET+ konfigurieren\n1. Laden Sie die **BeaconSET+** App herunter.\n2. Verbinden Sie sich mit dem Beacon (Passwort erforderlich).\n3. Setzen Sie einen Slot auf **Service Data** mit:\n   - **Service UUID:** `FE6F`\n   - **Data Value:** `FE6F` + `[Ihre 5-Byte HWID]` + `7F00` (z. B. `FE6F01234567897F00`).\n4. Speichern und trennen. Der Beacon sendet nun LINE Beacon Signale.\n\n### Schritt 3: Webhook Beacon Event verarbeiten\nIhr Server erhält ein JSON-Event mit `beacon` Details:\n* **`hwid`**: Die 5-Byte Hardware-ID des Beacons.\n* **`type`**: Aktionstyp (`enter` beim Betreten, `stay` für dauerhaften Aufenthalt alle 10 Sek., `banner` bei Klick auf das Banner).\n\n---\n\n## Installationsmethoden\n\n### Methode A: Klebeband\n* **Flächen:** Glas, Acryl, sauberes Aluminium.\n* **Prozess:** Fläche reinigen. Klebeband anpressen (2 Sek.), 30 Min. warten, dann montieren.\n\n### Methode B: Schrauben (Empfohlen)\n* **Flächen:** Beton, Holz, Ziegel.\n* **Prozess:** Halterung mit Schrauben und Dübeln anbringen. YPB03 einschieben, bis er einrastet.\n\n---\n\n## Konfigurationsanleitung\n\nDie Parameter (UUID, Major, Minor, Sendeleistung, Intervall) werden über **BeaconSET+** drahtlos konfiguriert:\n1. **BeaconSET+** App herunterladen.\n2. Bluetooth und Standort aktivieren.\n3. Beacon scannen, Passwort eingeben und Parameter anpassen."
        },
        "ypb04": {
            "body": "## Produktübersicht\n\nDer **YPB04** ist ein wiederaufladbarer, flacher Card-Badge Bluetooth® Low Energy (BLE 5.0) Beacon für Anwesenheitskontrolle, Personenlokalisierung und Geofencing. Mit seinen Maßen von 86 × 55 × 6 mm und einem Gewicht von 19g lässt er sich leicht an einem Lanyard tragen.\n\nAusgestattet mit **physischem Knopf**, **Vibrationsmotor** und **RGB-LED** bietet er physisches und visuelles Feedback. Er verfügt über einen Magnetladeanschluss, einen 3-Achsen-Beschleunigungssensor und optionalen **RFID (LF/HF/UHF)** Support.\n\n---\n\n## Hauptmerkmale\n\n* **3-Achsen-Sensor:** Bewegungserkennung zur intelligenten Intervallsteuerung.\n* **Feedback:** Vibrationsmotor und RGB-LED für Alarmmeldungen und Quittungen.\n* **Taster:** Physischer Knopf für SOS-Alarme oder Funktionsaufrufe.\n* **RFID Integration:** Optionaler Chip für klassische Zeiterfassungssysteme.\n* **Magnetladen:** Integrierter 270mAh Li-Po Akku hält bis zu 3 Monate.\n\n---\n\n## Bedienungsanleitung\n\n### Einschalten\n* Taster **3 Sekunden** gedrückt halten.\n* Blaue LED leuchtet für 3 Sekunden und der Badge vibriert einmal zur Bestätigung.\n\n### Ausschalten\n* Aus Sicherheitsgründen nur drahtlos über die **BeaconSET+ App** möglich (Passwort erforderlich).\n* Bei erfolgreichem Ausschalten blinkt die blaue LED 5 Mal.\n\n### Batteriestatus & Laden\n* **Niedriger Akku:** Unter 20% blinkt die rote LED alle 3 Sekunden.\n* **Ladevorgang:** Rote LED leuchtet dauerhaft.\n* **Vollständig geladen:** Grüne LED leuchtet dauerhaft.\n\n### Knopfdruck-Triggern\n* **Doppelklick:** Blaue LED blinkt 2 Mal, Motor vibriert 1 Mal.\n* **Dreifachklick:** Blaue LED blinkt 3 Mal, Motor vibriert 2 Mal.\n\n---\n\n## Konfigurationsanleitung\n\nVerwenden Sie die **BeaconSET+** App zur Konfiguration:\n1. App installieren und Bluetooth aktivieren.\n2. MAC-Adresse des Badges suchen und verbinden.\n3. Passwort eingeben, um Parameter und Knopftrigger anzupassen."
        },
        "ypb05": {
            "body": "## Produktübersicht\n\nDer **YPB05** ist ein winziger, batterieloser Micro-USB Bluetooth® Low Energy (BLE 5.0) Beacon. Mit einem Gewicht von nur **2,0 g** und Maßen von **18 × 14 × 6 mm** ist er die perfekte Plug-and-Play-Lösung.\n\nOhne Batterien läuft der YPB05 dauerhaft und wartungsfrei an PCs, Routern oder Netzteilen für In-Store-Marketing und Raumlokalisierung.\n\n---\n\n## Hauptmerkmale\n\n* **Dauerbetrieb:** USB-Stromversorgung eliminiert Wartungskosten für Batteriewechsel.\n* **Ultraleicht & Winzig:** Diskrete Platzierung an jedem USB-Port.\n* **Plug & Play:** Startet sofort bei Stromzufuhr ohne Tastenbedienung.\n* **Drahtloser Neustart:** Unterstützt drahtlose Reboot-Befehle für die Wartung.\n\n---\n\n## Konfigurationsanleitung\n\nParameter werden drahtlos über **BeaconSET+** konfiguriert:\n1. **BeaconSET+** laden und Bluetooth aktivieren.\n2. Verbinden Sie sich mit dem YPB05 über seine MAC-Adresse.\n3. Passwort eingeben und Parameter (UUID, Sendeleistung, Intervall) speichern."
        },
    },
    "es": {
        "ypb01": {
            "body": "## Descripción del producto\n\nEl **YPB01** es una baliza (beacon) de tipo moneda compacta y robusta Bluetooth® de bajo consumo (BLE 5.0) diseñada para localización en interiores, monitoreo de actividad y seguimiento de activos. Basada en el chip de ultra bajo consumo nRF52, transmite tramas iBeacon y Eddystone (UID, URL, TLM) simultáneamente.\n\nSu carcasa giratoria permite un reemplazo fácil de la batería CR2477 con protección IP67 contra polvo y agua.\n\n---\n\n## Características clave\n\n* **Protección IP67:** Resistente al polvo y agua para instalaciones en interiores o exteriores ligeros.\n* **Batería reemplazable:** Batería CR2477 (1000mAh) fácil de cambiar abriendo la carcasa giratoria.\n* **Transmisión simultánea:** Emite en hasta 6 ranuras publicitarias simultáneamente.\n* **Botón de encendido interno:** Pulsador interno para encender o apagar la baliza durante el transporte.\n\n---\n\n## Guía de operación\n\n### Encendido del Beacon\n1. Abra la carcasa giratoria hacia la derecha.\n2. Mantenga presionado el botón interno durante **3 segundos**.\n3. El LED azul se encenderá durante **5 segundos** indicando que está activo.\n\n### Apagado del Beacon\n1. Mantenga presionado el botón interno durante **3 segundos**.\n2. El LED azul parpadeará durante **5 segundos** y se apagará.\n\n---\n\n## Guía de configuración\n\nLos parámetros de YPB01 (UUID, Major, Minor, potencia de transmisión e intervalo) se configuran vía inalámbrica mediante la app **BeaconSET**:\n1. Descargue **BeaconSET** de Google Play o Apple App Store.\n2. Active Bluetooth y localización en su móvil.\n3. Busque la dirección MAC de la baliza y conéctese.\n4. Introduzca la contraseña por defecto para desbloquear y editar."
        },
        "ypb02": {
            "body": "## Descripción del producto\n\nEl **YPB02** es una baliza Bluetooth® (BLE 5.0) con un **acelerómetro LIS3DH de 3 ejes** integrado. Comparte la misma batería CR2477 y carcasa IP67 del YPB01, pero añade capacidades de telemetría y detección de movimiento.\n\nLa baliza puede configurarse para transmitir datos de aceleración en tiempo real o acelerar el intervalo de transmisión solo cuando se mueve o vibra.\n\n---\n\n## Características clave\n\n* **Sensor de aceleración de 3 ejes:** Sensor LIS3DH que mapea movimiento y orientación en ejes X, Y, Z.\n* **Transmisión basada en activadores:** Permite transmitir solo en movimiento, enviar alertas de caída o bajar el intervalo a 100 ms al moverse.\n* **Protección IP67:** Resistente al polvo y la inmersión en agua.\n* **Batería CR2477 reemplazable:** Larga vida útil con reemplazo rápido de pila.\n\n---\n\n## Activación por movimiento y telemetría\n\nMediante el sensor LIS3DH, el YPB02 soporta:\n1. **Publicidad basada en actividad:** Transmite tramas estándar y activa tramas de sensores solo con movimiento.\n2. **Modo dual:** Se mantiene en modo de suspensión al estar quieto y transmite a 100 ms cuando se mueve.\n3. **Calibración:** Los umbrales de aceleración se configuran desde la app.\n\n---\n\n## Guía de configuración\n\nLa configuración se realiza de forma inalámbrica vía **BeaconSET+**:\n1. Descargue e instale **BeaconSET+**.\n2. Active Bluetooth y localización.\n3. Escanee y conéctese al dispositivo.\n4. Ingrese la contraseña predeterminada para guardar los parámetros."
        },
        "ypb03": {
            "body": "## Descripción del producto\n\nEl **YPB03** es una baliza industrial optimizada como **LINE Beacon** que transmite paquetes estándar **LINE Simple Beacon**. Funciona con **4 pilas AA** (5800mAh), alcanzando una vida útil de **hasta 10 años**.\n\nCon un alcance de hasta **240 metros**, es ideal para áreas comerciales y museos. Los usuarios no necesitan instalar apps adicionales, reciben notificaciones directas en la app **LINE**.\n\n---\n\n## Características clave\n\n* **Compatibilidad oficial con LINE Beacon:** Transmite el protocolo abierto LINE Simple Beacon para integrar con la API de LINE Bot.\n* **10 años de autonomía:** Utiliza 4 pilas AA comunes que minimizan el costo de mantenimiento.\n* **Alcance de 240m:** Señal potente BLE 5.0 ideal para grandes superficies.\n* **Interacción sin fricción:** El cliente solo necesita activar Bluetooth y seguir su canal.\n* **Carcasa IP65:** Resistente a salpicaduras y polvo para entornos industriales.\n\n---\n\n## Guía de integración de LINE Beacon para desarrolladores\n\n### Cómo funcionan los disparadores de proximidad\nCuando un usuario con Bluetooth y LINE Beacon activo entra al rango:\n1. La app de LINE detecta el **UUID de servicio `0xFE6F`** y lee la ID de hardware (HWID).\n2. La plataforma de LINE envía un evento `beacon` a su servidor Webhook.\n3. Su bot responde en tiempo real con cupones o información de navegación.\n\n```mermaid\nsequenceDiagram\n    participant User as Usuario (App LINE)\n    participant Beacon as YPB03 (0xFE6F + HWID)\n    participant LINE as Plataforma LINE\n    participant Bot as Servidor Webhook (Bot)\n\n    Beacon->>User: Difusión BLE (UUID: FE6F + HWID)\n    User->>LINE: Reenviar HWID + User ID\n    LINE->>Bot: Webhook POST (evento beacon: enter/stay/banner)\n    Bot->>User: Respuesta API (ej. Cupón)\n```\n\n### Paso 1: Registrar el ID de hardware (HWID)\n1. Inicie sesión en **LINE Developers Console** o en el **LINE Official Account Manager**.\n2. Vaya a la sección Beacon y obtenga el **HWID de 5 bytes (10 caracteres hexadecimales)**.\n\n### Paso 2: Configurar YPB03 mediante BeaconSET+\n1. Abra la app **BeaconSET+** y conéctese a la baliza (requiere contraseña).\n2. Configure una ranura de transmisión como **Service Data** con:\n   - **Service UUID:** `FE6F`\n   - **Data Value:** `FE6F` + `[Su HWID de 5 bytes]` + `7F00` (ej. `FE6F01234567897F00`).\n3. Guarde y desconecte. La baliza comenzará a emitir la señal LINE Beacon.\n\n### Paso 3: Manejar el evento del webhook\nSu servidor recibirá un objeto JSON con detalles de `beacon`:\n* **`hwid`**: ID de hardware del beacon.\n* **`type`**: Tipo de acción (`enter` al entrar, `stay` enviado cada 10 segundos al permanecer, `banner` cuando se pulsa el banner en la app).\n\n---\n\n## Métodos de instalación\n\n### Método A: Cinta adhesiva industrial\n* **Superficies:** Vidrio, acrílico, aluminio limpio.\n* **Proceso:** Limpiar superficie. Presionar la cinta (2 seg), esperar 30 min y montar.\n\n### Método B: Soporte con tornillos (Recomendado)\n* **Superficies:** Hormigón, madera, ladrillo.\n* **Proceso:** Fijar el soporte a la pared con tacos y tornillos. Deslizar el YPB03 hasta que encaje.\n\n---\n\n## Guía de configuración\n\nLos parámetros se editan vía inalámbrica con **BeaconSET+**:\n1. Descargue **BeaconSET+** y active Bluetooth.\n2. Busque la baliza y conéctese con su clave.\n3. Configure UUID, Major, Minor, potencia e intervalo."
        },
        "ypb04": {
            "body": "## Descripción del producto\n\nEl **YPB04** es un beacon recargable extra plano en formato tarjeta (badge) diseñado para control de personal y geofencing. Sus dimensiones son 86 × 55 × 6 mm con 19g de peso, ideal para colgar en porta credenciales.\n\nCuenta con **botón físico**, **motor de vibración** y **LED RGB** para respuestas físicas y visuales. Incluye puerto de carga magnética, acelerómetro y compatibilidad opcional con **RFID (LF/HF/UHF)**.\n\n---\n\n## Características clave\n\n* **Acelerómetro de 3 ejes:** Detección de movimiento para controlar el intervalo de señal.\n* **Feedback visual/físico:** Motor de vibración y LED RGB para alarmas.\n* **Botón de control:** Botón externo para enviar alertas SOS.\n* **Integración RFID:** Chip opcional para sistemas de control de acceso clásicos.\n* **Batería magnética:** Batería recargable Li-po de 270mAh con autonomía de hasta 3 meses.\n\n---\n\n## Guía de operación\n\n### Encendido\n* Presione el botón físico por **3 segundos**.\n* El LED azul se encenderá 3 segundos y el dispositivo vibrará una vez.\n\n### Apagado\n* Por seguridad, solo se puede apagar vía inalámbrica desde la app **BeaconSET+** (requiere contraseña).\n* Al apagarse, el LED azul parpadeará 5 veces.\n\n### Estado de batería y carga\n* **Batería baja:** Bajo el 20%, el LED rojo parpadeará cada 3 segundos.\n* **Cargando:** LED rojo fijo.\n* **Carga completa:** LED verde fijo.\n\n### Acciones del botón\n* **Doble clic:** LED azul parpadea 2 veces y vibra 1 vez.\n* **Triple clic:** LED azul parpadea 3 veces y vibra 2 veces.\n\n---\n\n## Guía de configuración\n\nUse la app **BeaconSET+** para configurar el dispositivo:\n1. Instale la app y active Bluetooth.\n2. Conéctese al MAC del dispositivo.\n3. Introduzca su clave para editar parámetros y acciones del botón."
        },
        "ypb05": {
            "body": "## Descripción del producto\n\nEl **YPB05** es un micro beacon Bluetooth® (BLE 5.0) sin batería que se alimenta directamente desde un puerto USB. Pesa solo **2.0 g** y mide **18 × 14 × 6 mm**, siendo una solución plug-and-play perfecta.\n\nAl no requerir pilas, es ideal para marketing continuo en tiendas o localización de interiores en escritorios.\n\n---\n\n## Características clave\n\n* **Operación continua:** La alimentación por USB elimina el mantenimiento y recambio de pilas.\n* **Ultra ligero y diminuto:** Colocación discreta en cualquier ranura USB.\n* **Plug & Play:** Se activa al instante al conectar a la corriente sin botones.\n* **Reinicio por software:** Permite mandar comandos de reinicio vía inalámbrica.\n\n---\n\n## Guía de configuración\n\nSe configura de manera inalámbrica con **BeaconSET+**:\n1. Descargue **BeaconSET+** y encienda Bluetooth.\n2. Vincule el YPB05 escaneando su MAC.\n3. Configure UUID, Major, Minor, potencia de transmisión e intervalos."
        },
    },
    "fr": {
        "ypb01": {
            "body": "## Présentation du produit\n\nLe **YPB01** est une balise (beacon) bouton compacte et robuste Bluetooth® Low Energy (BLE 5.0) conçue pour la géolocalisation intérieure, le suivi d'activité et la traçabilité des actifs. Basée sur le chipset ultra-basse consommation nRF52, elle diffuse simultanément les trames iBeacon et Eddystone (UID, URL, TLM).\n\nSon boîtier rotatif permet de remplacer facilement la pile CR2477 tout en garantissant un niveau d'étanchéité IP67.\n\n---\n\n## Caractéristiques principales\n\n* **Protection IP67:** Étanche à la poussière et à l'eau pour un usage intérieur ou extérieur léger.\n* **Pile remplaçable:** Pile CR2477 (1000mAh) facile à changer en ouvrant le boîtier rotatif.\n* **Diffusions simultanées:** Supporte la diffusion de 6 slots publicitaires en parallèle.\n* **Bouton d'alimentation interne:** Interrupteur interne pour économiser l'énergie pendant le stockage.\n\n---\n\n## Guide d'utilisation\n\n### Allumer la balise\n1. Ouvrez le boîtier rotatif dans le sens horaire.\n2. Maintenez le bouton interne enfoncé pendant **3 secondes**.\n3. La LED bleue s'allume pendant **5 secondes** indiquant l'activation.\n\n### Éteindre la balise\n1. Maintenemz le bouton interne enfoncé pendant **3 secondes**.\n2. La LED bleue clignote pendant **5 secondes** puis s'éteint.\n\n---\n\n## Guide de configuration\n\nLes paramètres du YPB01 (UUID, Major, Minor, puissance et intervalle) se configurent sans fil via l'application **BeaconSET**:\n1. Téléchargez **BeaconSET** sur Google Play ou l'Apple App Store.\n2. Activez le Bluetooth et la localisation sur votre mobile.\n3. Scannez et connectez-vous à la balise via son adresse MAC.\n4. Saisissez le mot de passe pour modifier les paramètres."
        },
        "ypb02": {
            "body": "## Présentation du produit\n\nLe **YPB02** est une balise Bluetooth® (BLE 5.0) équipée d'un **accéléromètre LIS3DH 3 axes**. Elle possède le même boîtier IP67 et la même pile CR2477 que le YPB01, tout en ajoutant des fonctions de télémétrie de mouvement.\n\nLa balise peut modifier sa fréquence d'émission ou envoyer des alertes uniquement en cas de mouvement, de vibration ou de chute.\n\n---\n\n## Caractéristiques principales\n\n* **Accéléromètre 3 axes:** Capteur LIS3DH mesurant l'orientation et l'accélération sur les axes X, Y, Z.\n* **Diffusion sur déclencheur:** Permet d'émettre en mouvement, d'envoyer une alerte de chute ou de réduire l'intervalle à 100 ms en déplacement.\n* **Protection IP67:** Étanche à la poussière et à l'immersion.\n* **Pile remplaçable:** Remplacement rapide de la pile bouton CR2477.\n\n---\n\n## Détection de mouvement et télémétrie\n\nGrâce au capteur LIS3DH, le YPB02 permet:\n1. **Diffusion selon l'activité:** Émet les trames standards et déclenche les trames de capteurs uniquement en mouvement.\n2. **Mode double:** Reste en veille à l'arrêt et passe à un intervalle de 100 ms en mouvement.\n3. **Seuils réglables:** Les paramètres de sensibilité sont configurables via l'application.\n\n---\n\n## Guide de configuration\n\nLa configuration se fait sans fil via l'application **BeaconSET+**:\n1. Téléchargez **BeaconSET+**.\n2. Activez le Bluetooth et le service de localisation.\n3. Connectez-vous à la balise après détection de son adresse MAC.\n4. Saisissez le mot de passe pour modifier les réglages."
        },
        "ypb03": {
            "body": "## Présentation du produit\n\nLe **YPB03** est une balise industrielle optimisée en tant que **LINE Beacon** qui diffuse des paquets standards **LINE Simple Beacon**. Elle fonctionne avec **4 piles AA** (5800mAh), lui offrant une autonomie allant **jusqu'à 10 ans**.\n\nAvec une portée allant jusqu'à **240 mètres**, elle est idéale pour les galeries marchandes et les musées. Les utilisateurs reçoivent des notifications directement dans leur application **LINE** sans installer d'autres applications.\n\n---\n\n## Caractéristiques principales\n\n* **Compatibilité officielle LINE Beacon:** Diffuse le protocole ouvert LINE Simple Beacon pour s'associer avec l'API LINE Bot.\n* **10 ans d'autonomie:** Fonctionne avec 4 piles AA standards pour réduire la maintenance.\n* **Portée de 240m:** Signal BLE 5.0 puissant idéal pour les grands espaces.\n* **Engagement sans friction:** L'utilisateur doit simplement activer son Bluetooth et suivre votre compte.\n* **Boîtier IP65:** Conçu pour résister aux projections d'eau en milieu industriel.\n\n---\n\n## Guide d'intégration LINE Beacon pour les développeurs\n\n### Fonctionnement des déclencheurs de proximité\nLorsqu'un utilisateur avec Bluetooth et LINE Beacon activés entre dans la zone:\n1. L'application LINE détecte l'**UUID de service `0xFE6F`** et lit l'identifiant matériel (HWID).\n2. La plateforme LINE transmet un événement `beacon` à votre serveur Webhook.\n3. Votre bot répond en temps réel avec des messages, des coupons ou des plans.\n\n```mermaid\nsequenceDiagram\n    participant User as Utilisateur (App LINE)\n    participant Beacon as YPB03 (0xFE6F + HWID)\n    participant LINE as Plateforme LINE\n    participant Bot as Serveur Webhook (Bot)\n\n    Beacon->>User: Émission BLE (UUID: FE6F + HWID)\n    User->>LINE: Transmettre HWID + User ID\n    LINE->>Bot: Webhook POST (événement beacon: enter/stay/banner)\n    Bot->>User: Réponse API (ex: Coupon)\n```\n\n### Étape 1: Enregistrer l'identifiant matériel (HWID)\n1. Connectez-vous sur le **LINE Developers Console** ou le **LINE Official Account Manager**.\n2. Allez dans la section Beacon et générez l'**HWID de 5 octets (10 caractères hexadécimaux)**.\n\n### Étape 2: Configurer le YPB03 avec BeaconSET+\n1. Lancez l'application **BeaconSET+** et connectez-vous à la balise (mot de passe requis).\n2. Configurez un slot en type **Service Data** avec:\n   - **Service UUID:** `FE6F`\n   - **Data Value:** `FE6F` + `[Votre HWID de 5 octets]` + `7F00` (ex: `FE6F01234567897F00`).\n3. Sauvegardez et déconnectez. La balise commence à diffuser le signal LINE Beacon.\n\n### Étape 3: Gérer l'événement du webhook\nVotre serveur recevra un objet JSON contenant les détails du `beacon`:\n* **`hwid`**: Identifiant matériel de la balise.\n* **`type`**: Type d'action (`enter` à l'entrée, `stay` envoyé toutes les 10 secondes si l'utilisateur reste, `banner` en cas de clic sur la bannière).\n\n---\n\n## Méthodes d'installation\n\n### Méthode A: Ruban adhésif industriel\n* **Surfaces:** Verre, acrylique, aluminium propre.\n* **Process:** Nettoyer la surface. Presser le ruban (2 sec), attendre 30 min et monter la balise.\n\n### Méthode B: Support à vis (Recommandé)\n* **Surfaces:** Béton, bois, brique.\n* **Process:** Fixer le support avec des vis et des chevilles. Glisser le YPB03 jusqu'au clic.\n\n---\n\n## Guide de configuration\n\nLes paramètres se configurent sans fil à l'aide de **BeaconSET+**:\n1. Téléchargez **BeaconSET+** et activez le Bluetooth.\n2. Recherchez la balise et connectez-vous.\n3. Modifiez l'UUID, le Major, le Minor, la puissance et l'intervalle."
        },
        "ypb04": {
            "body": "## Présentation du produit\n\nLe **YPB04** est une balise rechargeable extra-plate au format carte (badge) conçue pour la gestion des accès et le suivi des flux. Très légère (19g) et mesurant 86 × 55 × 6 mm, elle se porte facilement autour du cou.\n\nElle intègre un **bouton physique**, un **vibreur** et une **LED RGB** pour des réponses visuelles et tactiles. Elle dispose d'un connecteur de charge magnétique, d'un accéléromètre et d'une puce **RFID (LF/HF/UHF)** optionnelle.\n\n---\n\n## Caractéristiques principales\n\n* **Accéléromètre 3 axes:** Détection de mouvement pour ajuster le rythme de diffusion.\n* **Retour d'information:** Vibreur et LED RGB pour les alarmes.\n* **Bouton de contrôle:** Bouton extérieur pour déclencher des alertes SOS.\n* **Compatibilité RFID:** Option d'intégration pour les lecteurs de badge classiques.\n* **Batterie magnétique:** Accumulateur Li-po 270mAh offrant jusqu'à 3 mois d'autonomie.\n\n---\n\n## Guide d'utilisation\n\n### Allumer le badge\n* Maintenez le bouton physique enfoncé pendant **3 secondes**.\n* La LED bleue s'allume 3 secondes et le badge vibre une fois.\n\n### Éteindre le badge\n* Pour des raisons de sécurité, l'arrêt s'effectue uniquement sans fil depuis l'application **BeaconSET+** (mot de passe requis).\n* Lors de l'arrêt, la LED bleue clignote 5 fois.\n\n### Batterie et chargement\n* **Batterie faible:** Sous 20%, la LED rouge clignote toutes les 3 secondes.\n* **En charge:** La LED rouge reste allumée.\n* **Charge complète:** La LED verte s'allume.\n\n### Déclencheurs bouton\n* **Double-clic:** La LED bleue clignote 2 fois, le vibreur s'active 1 fois.\n* **Triple-clic:** La LED bleue clignote 3 fois, le vibreur s'active 2 fois.\n\n---\n\n## Guide de configuration\n\nUtilisez l'application **BeaconSET+** pour configurer l'appareil:\n1. Installez l'application et activez le Bluetooth.\n2. Connectez-vous à l'adresse MAC du badge.\n3. Saisissez le mot de passe pour modifier les paramètres."
        },
        "ypb05": {
            "body": "## Présentation du produit\n\nLe **YPB05** est un micro beacon sans pile qui s'alimente directement via un port USB. Ne pesant que **2.0 g** pour des dimensions de **18 × 14 × 6 mm**, c'est une solution plug-and-play idéale.\n\nSans pile à remplacer, il est parfait pour les campagnes promotionnelles en magasin ou la géolocalisation de bureaux.\n\n---\n\n## Caractéristiques principales\n\n* **Fonctionnement continu:** L'alimentation par USB supprime les contraintes de maintenance des piles.\n* **Ultra léger et minuscule:** Discrétion absolue une fois inséré sur un port USB.\n* **Plug & Play:** S'active automatiquement dès le branchement sur l'alimentation.\n* **Redémarrage logiciel:** Permet d'envoyer des commandes de reboot à distance.\n\n---\n\n## Guide de configuration\n\nSe configure de manière sans fil avec **BeaconSET+**:\n1. Téléchargez **BeaconSET+** et activez le Bluetooth.\n2. Sélectionnez le YPB05 après détection de son adresse MAC.\n3. Configurez l'UUID, le Major, le Minor, la puissance d'émission et les intervalles."
        },
    },
    "ja": {
        "ypb01": {
            "body": "## 製品概要\n\n**YPB01** は、屋内位置測位、活動監視、および資産追跡用に設計された、コンパクトで頑丈な Bluetooth® Low Energy (BLE 5.0) コイン型ビーコンです。超低消費電力の nRF52 シリーズ チップセットをベースに、iBeacon および Eddystone (UID、URL、TLM) フレームを同時にブロードキャストします。\n\n回転開閉式の筐体構造により、コイン型電池の交換が容易でありながら、IP67 の防水・防塵性能を達成。湿気の多い環境や過酷な環境への設置に最適です。\n\n---\n\n## 主な特徴\n\n* **高保護筐体:** IP67 防水防塵仕様で、屋内および一時的な屋外設置に対応。\n* **交換式電池:** 回転式開閉機構により、長寿命の CR2477 電池 (1000mAh) を簡単に交換可能。\n* **同時配信:** iBeacon と Eddystone 双方のプロトコルをカバーする、最大 6 個の独立した広告スロットの同時配信に対応。\n* **電源ボタン:** 輸送や保管時のバッテリー消耗を防ぐため、内部に電源オン/オフ用の物理ボタンを搭載。\n\n---\n\n## 操作ガイド\n\n### ビーコンの電源を入れる方法\n1. 回転式の筐体を時計回りに回して開きます。\n2. 内部の「プッシュボタン」を **3秒間** 長押しします。\n3. 青色の LED インジケーターが **5秒間** 点灯した後に消灯します。これで YPB01 が起動し、配信が開始されます。\n\n### ビーコンの電源を切る方法\n1. 内部のプッシュボタンを **3秒間** 長押しします。\n2. 青色の LED インジケーターが **5秒間** 点滅した後に消灯します。これでビーコンの電源が切れます。\n\n---\n\n## 設定ガイド\n\nYPB01 のパラメータ（UUID、Major、Minor、送信出力、およびアドバタイジング間隔）は、**BeaconSET** アプリケーションを使用してワイヤレスで設定します：\n1. Google Play または Apple App Store から **BeaconSET** をダウンロードします。\n2. スマートフォンの Bluetooth および位置情報サービスが有効になっていることを確認します。\n3. アプリを開き、ビーコンの MAC アドレスをスキャンして接続します。\n4. デフォルトのセキュリティパスワードを入力してロックを解除し、パラメータを編集します。\n\n## 技術仕様"
        },
        "ypb02": {
            "body": "## 製品概要\n\n**YPB02** は、高性能な **LIS3DH 3軸加速度センサー** を内蔵したモーション検知型の Bluetooth® Low Energy (BLE 5.0) ビーコンです。YPB01 と同様のコンパクトなコイン型デザイン、交換可能な 1000mAh CR2477 コイン電池、および IP67 防水・防塵筐体を採用しつつ、さらにスマートなモーション検知とセンサー情報の送信に対応しています。\n\nこのビーコンはトリガーベースの配信をサポートしており、移動、振動、あるいは落下検知などのイベント発生時のみ、リアルタイムの加速度データ送信や配信間隔の切り替えを行います。これによりバッテリー消費を最小限に抑えつつ、高度な資産活動監視を実現します。\n\n---\n\n## 主な特徴\n\n* **3軸加速度センサー搭載:** LIS3DH センサーを搭載し、X・Y・Z 軸の変位、傾き、動きのデータを測定・送信します。\n* **トリガーベース配信:** 特定のトリガー条件（例：移動時のみの配信、落下アラート、移動検知時に配信間隔を 100ms に短縮してリアルタイム追跡など）を設定可能です。\n* **高保護筐体:** IP67 防水防塵設計で、屋内や軽度の屋外環境に設置可能です。\n* **交換式電池:** 回転式ハウジング設計により、コイン電池 (CR2477, 1000mAh) を簡単に交換できます。\n\n---\n\n## モーション検知とテレメトリ\n\nLIS3DH センサーにより、YPB02 は以下をサポートします：\n1. **アクティビティトリガー配信:** 通常時は標準的な iBeacon/Eddystone フレームを送信し、動きを検出したときのみセンサーデータフレーム (HT/ACC) を送信します。\n2. **静止・移動モードの併用:** 静止時は休止（スリープ）状態を維持し、動きを検知すると 100ms 間隔でリアルタイム位置情報を送信させることができます。\n3. **しきい値調整:** アプリを通じて、加速度のしきい値や検知時間をカスタマイズできます。\n\n---\n\n## 設定ガイド\n\nYPB02 のパラメータ（加速度しきい値、トリガー、UUID、Major、Minor など）は、**BeaconSET+** アプリを使用してワイヤレスで設定します：\n1. Google Play または Apple App Store から **BeaconSET+** をダウンロードします。\n2. スマートフォンの Bluetooth および位置情報サービスを有効にします。\n3. アプリを開き、該当するビーコンの MAC アドレスを選択して接続します。\n4. パスワードを入力して、しきい値や配信パラメータを変更します。\n\n## 技術仕様"
        },
        "ypb03": {
            "body": "## 製品概要\n\n**YPB03** は、**LINE Beacon** プロトコル用に最適化され、標準的な **LINE Simple Beacon** パケットの配信に対応した、産業用超長寿命型 Bluetooth® Low Energy (BLE 5.0) ビーコンです。**単3乾電池×4本**（計 5800mAh）で駆動し、デフォルトの設定で **最大10年間** という圧倒的なバッテリー寿命を実現しています。\n\n高利得アンテナの採用により、最大 **240メートル** の超広範囲通信に対応。大規模な商業店舗でのプロモーション、スマート小売店のナビゲーション、広大な屋内施設の案内などに最適です。ユーザーは専用アプリを別途インストールする必要がなく、使い慣れた **LINE** アプリを通じて直接位置連動型の通知やメッセージを受け取ることができます。\n\n---\n\n## 主な特徴\n\n* **公式 LINE Beacon 完全互換:** オープンな LINE Simple Beacon プロトコルを配信し、物理的な位置情報と LINE ボット (Messaging API) を簡単に統合します。\n* **10年間のメンテナンスフリー:** 入手性の高い単3乾電池4本で駆動。5800mAh の大容量により、頻繁な電池交換コストを削減します。\n* **240m の広域カバー:** 強力な BLE 5.0 信号で、空港、イベント会場、ショッピングモールなどの大規模施設をカバーします。\n* **手軽なエンゲージメント:** ユーザーは Bluetooth をオンにし、公式アカウントを友だち追加するだけで受信可能。アプリダウンロードの障壁がありません。\n* **タフな産業用設計:** IP65 等級の防水防塵 ABS 筐体を採用し、工場や倉庫、湿気の多い屋内環境でも安定して動作します。\n\n---\n\n## LINE Beacon 開発者向け統合ガイド\n\n### 近接トリガーの仕組み\nBluetooth と LINE Beacon 設定を有効にしているユーザーが YPB03 の電波圏内に入ると：\n1. LINE アプリが **Service UUID `0xFE6F`** を検知し、電波に含まれるハードウェア ID (HWID) を読み取ります。\n2. LINE プラットフォームがこの情報を仲介し、該当する LINE ボットの Webhook サーバーへ `beacon` イベントを POST 送信します。\n3. ボットサーバーがこのイベントを受け取り、クーポン、ウェルカムメッセージ、あるいは屋内ナビなどのアクションをリアルタイムに返信します。\n\n```mermaid\nsequenceDiagram\n    participant User as ユーザー (LINE App)\n    participant Beacon as YPB03 (0xFE6F + HWID)\n    participant LINE as LINE プラットフォーム\n    participant Bot as Webhook サーバー (Bot)\n\n    Beacon->>User: BLE配信 (UUID: FE6F + HWID)\n    User->>LINE: HWID と ユーザーID を送信\n    LINE->>Bot: Webhook POST (beacon イベント: enter/stay/banner)\n    Bot->>User: 返信/プッシュ (例: クーポン送付)\n```\n\n### ステップ 1：ハードウェア ID (HWID) の登録\n1. **LINE Developers Console** または **LINE 公式アカウント管理画面** にログインします。\n2. **Beacon** 連携メニューから新規デバイスを登録し、固有の **5バイト (16進数10文字) のハードウェア ID (HWID)** を発行・取得します。\n\n### ステップ 2：BeaconSET+ を使用した YPB03 の設定\nYPB03 の設定はワイヤレスで変更可能です：\n1. スマートフォンで **BeaconSET+** アプリを開きます。\n2. 該当する YPB03 の MAC アドレスを選択して接続します（管理パスワードが必要）。\n3. 使用するスロットの設定を **Service Data** に変更し、以下を設定します：\n   - **Service UUID:** `FE6F`\n   - **Data Value:** `FE6F` + `[取得した 5バイトの HWID]` + `7F00` (例: HWID が `0123456789` の場合、`FE6F01234567897F00` と入力します)。\n4. 保存して接続を切断すると、デバイスは LINE Beacon パケットの配信を開始します。\n\n### ステップ 3：Webhook での Beacon イベント処理\nユーザーの検知時にサーバーが受け取る JSON オブジェクトには、以下のような `beacon` 情報が含まれます：\n* **`hwid`**: 登録されたビーコンのハードウェアID。\n* **`type`**: 検知タイプ：\n  - `enter`: ユーザーがビーコンの電波圏内に入ったとき。\n  - `stay`: ユーザーが電波圏内に滞在し続けているとき（10秒ごとに送信）。\n  - `banner`: ユーザーが LINE のトーク画面上部に表示されたビーコン通知をタップしたとき。\n\n---\n\n## 設置方法\n\n### 方法 A：両面テープによる貼り付け\n* **適した場所:** ガラス、アクリル、清潔なアルミ板、磨かれたタイルなどの滑らかな表面。\n* **手順:** 設置場所を綺麗に拭きます。付属の強力両面テープを貼り付け、2秒間押し当てた後、30分間置いてからビーコン本体を固定します。\n\n### 方法 B：ネジ式ブラケットによる壁掛け（推奨）\n* **適した場所:** コンクリート、石膏ボード、木材、レンガ壁など。\n* **手順:**\n  1. 壁面にプラグとネジを用いて取付用ブラケットを固定します。\n  2. YPB03 をブラケットの溝に沿ってスライドさせ、カチッと音がするまで差し込みます。\n\n---\n\n## 設定ガイド\n\nYPB03 のパラメータ（UUID、Major、Minor、送信出力、およびアドバタイジング間隔）は、**BeaconSET+** アプリを使用してワイヤレスで設定します：\n1. Google Play または Apple App Store から **BeaconSET+** をダウンロードします。\n2. スマートフォンの Bluetooth と位置情報を有効にします。\n3. アプリから接続し、デフォルトのパスワードを入力してパラメータを編集します。\n\n## 技術仕様"
        },
        "ypb04": {
            "body": "## 製品概要\n\n**YPB04** は、スマートオフィスの勤怠管理、人員の位置追跡、およびジオフェンス向けに設計された、極薄カード（バッジ）型の Bluetooth® Low Energy (BLE 5.0) ビーコンです。クレジットカードサイズ (86 × 55 × 6 mm、わずか 19g) で、ストラップに取り付けたり、制服のポケットに入れて簡単に携帯できます。\n\nYPB04 は、**物理プッシュボタン**、**バイブレーションモーター**、**RGB LED インジケーター** を搭載し、視覚と触覚のフィードバックを提供します。さらに磁吸式の充電ポート、3軸加速度センサーを備え、オプションで **双周波 RFID (LF/HF/UHF)** の追加にも対応。BLE 測位と従来の物理ゲート式の社員証を統合可能です。\n\n---\n\n## 主な特徴\n\n* **3軸加速度センサー内蔵:** 静止・移動・落下状態を自動的に検出して通知します。\n* **デュアルフィードバック:** 1×バイブレーションモーターと 1×RGB LED を搭載し、触覚と視覚で警告や通知を行います。\n* **外部操作ボタン:** 物理ボタンを押すことで、あらかじめ設定した特定の配信パターン（SOS 警告など）を起動できます。\n* **RFID 統合可能:** 必要に応じて LF/HF/UHF IC チップを内蔵し、従来のタッチ式入館ゲートにも対応させることができます。\n* **充電式バッテリー:** 270mAh 内部リチウム電池を搭載。便利な磁吸式充電に対応し、一般的な使用環境で約3ヶ月間駆動します。\n\n---\n\n## 操作ガイド\n\n### ビーコンの電源を入れる方法\n* 物理ボタンを **3秒間** 長押しします。\n* 青色の LED が3秒間点灯し、本体が1回バイブレーションして、電源がオンになったことを通知します。\n\n### ビーコンの電源を切る方法\n* セキュリティ上、本デバイスは物理ボタンでの電源オフには対応していません。**BeaconSET+ アプリ** から接続し、パスワードを入力した上でワイヤレスでシャットダウンを実行する必要があります。\n* 正常にシャットダウンが実行されると、青色 LED が5回点滅します。\n\n### 電池ステータスと充電について\n* **低電力アラート:** 残量が20%を下回ると、赤色 LED が3秒に1回点滅します。\n* **充電中:** 充電中は赤色 LED が常時点灯します。\n* **充電完了:** 充電が完了すると緑色 LED が常時点灯します。\n* **ボタンクリックトリガー:** ダブルクリックまたはトリプルクリックで、それぞれ事前に設定した緊急信号 (SOS) やパケット送信が行えます。\n\n---\n\n## 設定ガイド\n\nYPB04 のパラメータ（ボタン動作設定、UUID、Major、Minor など）は、**BeaconSET+** アプリを使用してワイヤレスで設定します：\n1. Google Play または Apple App Store から **BeaconSET+** をダウンロードします。\n2. Bluetooth と位置情報を有効にし、アプリから該当カードの MAC アドレスを選択します。\n3. パスワードを入力して設定を変更・保存します。\n\n## 技術仕様"
        },
        "ypb05": {
            "body": "## 製品概要\n\n**YPB05** は、電池交換不要で動作する、極小かつ超軽量の Micro USB / USB ポート給電型 Bluetooth® Low Energy (BLE 5.0) ビーコンです。重量わずか **2.0g**、サイズ **18 × 14 × 6 mm** の筐体で、プラグ＆プレイで動作します。\n\nバッテリー交換やメンテナンスが一切不要なため、店舗での常時広告配信、教室での勤怠・登校検知、PC周辺やデスク領域の位置測位システムに最適です。PC、USB 充電アダプター、Wi-Fi ルーター、モバイルバッテリーに差し込むだけで稼働します。\n\n---\n\n## 主な特徴\n\n* **24時間365日の連続稼働:** 標準の USB ポートから直接給電されるため、バッテリーの消耗や交換の心配がありません。\n* **超小型・超軽量:** わずか 2g のため、USB ポートに差し込んでも目立たず、省スペースで設置できます。\n* **プラグ＆プレイ:** 電源に接続すると自動的に起動し、配信を開始します。ボタン操作は不要です。\n* **ソフトウェア再起動に対応:** 遠隔から無線コマンドを送信して、デバイスのソフト再起動を実行可能です。\n\n---\n\n## 設定ガイド\n\nYPB05 のパラメータ（UUID、Major、Minor、送信出力、アドバタイジング間隔）は、**BeaconSET+** アプリを使用してワイヤレスで設定します：\n1. Google Play または Apple App Store から **BeaconSET+** をダウンロードします。\n2. スマートフォンの Bluetooth および位置情報サービスを有効にします。\n3. アプリを開き、ビーコンの MAC アドレスをスキャンして接続します。\n4. パスワードを入力し、パラメータを編集・保存します。\n\n## 技術仕様"
        },
    },
    "pt": {
        "ypb01": {
            "body": "## Visão geral do produto\n\nO **YPB01** é um beacon moeda compacto e robusto Bluetooth® Low Energy (BLE 5.0) projetado para localização interna, monitoramento de atividades e rastreamento de ativos. Baseado no chipset nRF52 de consumo ultra-baixo, ele transmite quadros iBeacon e Eddystone (UID, URL, TLM) simultaneamente.\n\nSeu gabinete rotativo permite a troca fácil da bateria CR2477, mantendo a classificação IP67 contra poeira e água.\n\n---\n\n## Principais recursos\n\n* **Proteção IP67:** Resistente à poeira e água para instalações internas ou externas leves.\n* **Bateria substituível:** Bateria CR2477 (1000mAh) de fácil troca abrindo o gabinete rotativo.\n* **Transmissão simultânea:** Transmite em até 6 canais de anúncios em paralelo.\n* **Botão liga/desliga interno:** Botão interno para desligar o beacon durante o transporte.\n\n---\n\n## Guia de operação\n\n### Ligar o Beacon\n1. Abra o crachá giratório no sentido horário.\n2. Mantenha pressionado o botão interno por **3 segundos**.\n3. O LED azul acenderá por **5 segundos** indicando que o beacon está ativo.\n\n### Desligar o Beacon\n1. Mantenha pressionado o botão interno por **3 segundos**.\n2. O LED azul piscará por **5 segundos** e se apagará.\n\n---\n\n## Guia de configuração\n\nOs parâmetros do YPB01 (UUID, Major, Minor, potência de transmissão e intervalos) são configurados sem fio pelo aplicativo **BeaconSET**:\n1. Baixe o **BeaconSET** no Google Play ou Apple App Store.\n2. Ative o Bluetooth e a localização no celular.\n3. Busque o endereço MAC do beacon e conecte-se.\n4. Insira a senha por padrão para editar os parâmetros."
        },
        "ypb02": {
            "body": "## Visão geral do produto\n\nO **YPB02** é um beacon Bluetooth® (BLE 5.0) com um **acelerômetro LIS3DH de 3 eixos** integrado. Compartilha a mesma bateria CR2477 e gabinete IP67 do YPB01, mas adiciona telemetria e detecção de movimento.\n\nO beacon pode ser configurado para transmitir dados de aceleração em tempo real ou encurtar o intervalo de sinal apenas quando estiver em movimento ou vibrando.\n\n---\n\n## Principais recursos\n\n* **Sensor de aceleração de 3 eixos:** Sensor LIS3DH que mede movimento e inclinação nos eixos X, Y, Z.\n* **Transmissão ativa por gatilhos:** Envia sinal apenas em movimento, dispara alertas de queda ou altera o intervalo para 100 ms ao se mover.\n* **Proteção IP67:** Resistente a poeira e imersão em água.\n* **Bateria substituível:** Gabinete rotativo permite troca rápida de pilha CR2477.\n\n---\n\n## Gatilho de movimento e telemetria\n\nAtravés do sensor LIS3DH, o YPB02 suporta:\n1. **Sinal baseado em atividade:** Transmite quadros padrão e ativa dados de movimento apenas em deslocamento.\n2. **Modo duplo:** Fica em suspensão quando parado e transmite a 100 ms em movimento.\n3. **Calibração:** Os limites de sensibilidade podem ser ajustados via app.\n\n---\n\n## Guia de configuração\n\nA configuração é feita sem fio pelo aplicativo **BeaconSET+**:\n1. Instale o **BeaconSET+**.\n2. Ative o Bluetooth e a localização.\n3. Conecte-se após buscar o MAC correspondente.\n4. Insira a senha de administrador para salvar os ajustes."
        },
        "ypb03": {
            "body": "## Visão geral do produto\n\nO **YPB03** é um beacon industrial otimizado como **LINE Beacon** que transmite pacotes padrão **LINE Simple Beacon**. Ele funciona com **4 pilhas AA** (5800mAh), garantindo durabilidade de **até 10 anos**.\n\nCom alcance de até **240 metros**, é a escolha ideal para grandes lojas e galerias. Os clientes não necessitam instalar aplicativos extras – as notificações chegam direto na app **LINE**.\n\n---\n\n## Principais recursos\n\n* **Compatibilidade oficial LINE Beacon:** Transmite o protocolo aberto LINE Simple Beacon para integrar com a API de LINE Bot.\n* **10 anos de autonomia:** Usa 4 pilhas AA comuns que diminuem custos de manutenção.\n* **Alcance de 240m:** Sinal potente BLE 5.0 ideal para grandes ambientes.\n* **Interação sem atrito:** O cliente só precisa ativar o Bluetooth e seguir seu canal.\n* **Gabinete IP65:** Resistente a jatos de água para ambientes industriais.\n\n---\n\n## Guia de integração do LINE Beacon para desenvolvedores\n\n### Como funcionam os disparadores de proximidade\nQuando um usuário com Bluetooth e LINE Beacon ativos entra na área do sinal:\n1. O aplicativo LINE detecta o **UUID de serviço `0xFE6F`** e lê o ID de hardware (HWID).\n2. A plataforma LINE envia um evento `beacon` ao seu servidor Webhook.\n3. Seu bot responde em tempo real com cupons ou menus interativos.\n\n```mermaid\nsequenceDiagram\n    participant User as Usuário (App LINE)\n    participant Beacon as YPB03 (0xFE6F + HWID)\n    participant LINE as Plataforma LINE\n    participant Bot as Servidor Webhook (Bot)\n\n    Beacon->>User: Difusão BLE (UUID: FE6F + HWID)\n    User->>LINE: Encaminhar HWID + User ID\n    LINE->>Bot: Webhook POST (evento beacon: enter/stay/banner)\n    Bot->>User: Resposta API (ex: Cupom)\n```\n\n### Passo 1: Registrar o ID de hardware (HWID)\n1. Acesse o **LINE Developers Console** ou o **LINE Official Account Manager**.\n2. Vá até a seção Beacon e gere o **HWID de 5 bytes (10 caracteres hexadecimais)**.\n\n### Passo 2: Configurar o YPB03 pelo BeaconSET+\n1. Abra a app **BeaconSET+** e conecte-se ao beacon (requer senha).\n2. Configure uma das faixas como **Service Data** com:\n   - **Service UUID:** `FE6F`\n   - **Data Value:** `FE6F` + `[Seu HWID de 5 bytes]` + `7F00` (ex: `FE6F01234567897F00`).\n3. Salve e desconecte. O beacon começará a transmitir o sinal LINE Beacon.\n\n### Passo 3: Tratar o evento do webhook\nSeu servidor receberá um objeto JSON com detalhes de `beacon`:\n* **`hwid`**: ID de hardware do beacon.\n* **`type`**: Tipo de ação (`enter` ao entrar, `stay` enviado a cada 10 segundos se continuar na área, `banner` ao clicar no banner na app).\n\n---\n\n## Métodos de instalação\n\n### Método A: Fita adesiva industrial\n* **Superfícies:** Vidro, acrílico, alumínio limpo.\n* **Processo:** Limpar a superfície. Pressionar a fita (2 seg), aguardar 30 min e montar.\n\n### Método B: Suporte com parafusos (Recomendado)\n* **Superfícies:** Concreto, madeira, tijolo.\n* **Processo:** Fixar o suporte com buchas e parafusos. Deslizar o YPB03 até travar.\n\n---\n\n## Guia de configuração\n\nOs parâmetros são configurados sem fio com o **BeaconSET+**:\n1. Baixe o **BeaconSET+** e ative o Bluetooth.\n2. Localize o beacon e conecte-se com sua senha.\n3. Ajuste o UUID, Major, Minor, potência e intervalo."
        },
        "ypb04": {
            "body": "## Visão geral do produto\n\nO **YPB04** é um beacon recarregável plano formato cartão (badge) projetado para controle de fluxo e geofencing. Mede 86 × 55 × 6 mm com peso de 19g, ideal para carregar em cordões de pescoço.\n\nPossui **botão físico**, **motor de vibração** e **LED RGB** para feedback visual e tátil. Inclui conector de carga magnética, acelerômetro e suporte opcional a **RFID (LF/HF/UHF)**.\n\n---\n\n## Principais recursos\n\n* **Sensor de 3 eixos:** Acelerômetro interno para gerenciar a frequência de sinal.\n* **Feedback físico/visual:** Motor de vibração e LED RGB para alertas.\n* **Botão de controle:** Botão externo para acionar alertas de emergência (SOS).\n* **Compatibilidade RFID:** Chip opcional para leitores tradicionais de portaria.\n* **Bateria magnética:** Bateria de 270mAh recarregável que dura até 3 meses.\n\n---\n\n## Guia de operação\n\n### Ligar o crachá\n* Pressione o botão físico por **3 segundos**.\n* O LED azul ligará por 3 segundos e o dispositivo vibrará uma vez.\n\n### Desligar o crachá\n* Por segurança, o desligamento é feito apenas sem fio pelo aplicativo **BeaconSET+** (requer senha).\n* Ao desligar, o LED azul piscará 5 vezes.\n\n### Status de bateria e carga\n* **Bateria baixa:** Abaixo de 20%, o LED vermelho pisca a cada 3 segundos.\n* **Carregando:** LED vermelho aceso fixo.\n* **Carga completa:** LED verde aceso fixo.\n\n### Ações do botão\n* **Clique duplo:** LED azul pisca 2 vezes e vibra 1 vez.\n* **Clique triplo:** LED azul pisca 3 vezes e vibra 2 vezes.\n\n---\n\n## Guia de configuração\n\nUse o aplicativo **BeaconSET+** para configurar o crachá:\n1. Instale o app e ative o Bluetooth.\n2. Conecte ao endereço MAC do crachá.\n3. Digite sua senha para alterar os parâmetros e comportamentos do botão."
        },
        "ypb05": {
            "body": "## Visão geral do produto\n\nO **YPB05** é um micro beacon Bluetooth® (BLE 5.0) alimentado diretamente de qualquer porta USB, sem necessidade de bateria. Pesa apenas **2,0 g** e mede **18 × 14 × 6 mm**, oferecendo uma solução plug-and-play perfeita.\n\nPor operar sem baterias, é ideal para marketing constante em lojas ou localização indoor em estações de trabalho.\n\n---\n\n## Principais recursos\n\n* **Operação contínua:** Alimentação por USB elimina manutenção e troca de baterias.\n* **Ultra leve e minúsculo:** Posicionamento discreto em qualquer porta USB.\n* **Plug & Play:** Inicia a transmissão no momento em que é conectado, sem botões.\n* **Reinício remoto:** Permite mandar comandos de reset via wireless.\n\n---\n\n## Guia de configuração\n\nConfiguração feita de modo sem fio com **BeaconSET+**:\n1. Baixe a app **BeaconSET+** e ligue o Bluetooth.\n2. Conecte ao YPB05 escaneando o MAC correspondente.\n3. Digite a senha e configure UUID, Major, Minor, potência e intervalo."
        },
    },
    "ru": {
        "ypb01": {
            "body": "## Обзор продукта\n\n**YPB01** — это компактный и надежный Bluetooth® Low Energy (BLE 5.0) маяк типа «монета», разработанный для позиционирования в помещениях, мониторинга активности и отслеживания активов. Построенный на базе чипсета nRF52 с ультранизким энергопотреблением, он транслирует кадры iBeacon и Eddystone (UID, URL, TLM) одновременно.\n\nЕго поворотный корпус позволяет легко заменять батарейку CR2477, обеспечивая класс защиты IP67.\n\n---\n\n## Ключевые свойства\n\n* **Защита IP67:** Пыле- и водонепроницаемость для внутренней и легкой уличной установки.\n* **Заменяемая батарея:** Батарея CR2477 (1000 мАч) легко меняется открытием корпуса.\n* **Параллельное вещание:** Поддерживает до 6 слотов вещания одновременно.\n* **Внутренняя кнопка питания:** Внутренняя кнопка для отключения вещания на время транспортировки.\n\n---\n\n## Руководство по эксплуатации\n\n### Как включить маяк\n1. Откройте поворотный корпус по часовой стрелке.\n2. Удерживайте внутреннюю кнопку нажатой в течение **3 секунд**.\n3. Синий светодиод загорится на **5 секунд**. Маяк активирован.\n\n### Как выключить маяк\n1. Удерживайте внутреннюю кнопку нажатой в течение **3 секунд**.\n2. Синий светодиод мигнет в течение **5 секунд** и погаснет. Маяк отключен.\n\n---\n\n## Руководство по настройке\n\nПараметры YPB01 (UUID, Major, Minor, мощность и интервал) настраиваются без проводов через приложение **BeaconSET**:\n1. Загрузите **BeaconSET** из Google Play или Apple App Store.\n2. Включите Bluetooth и геолокацию на телефоне.\n3. Найдите MAC-адрес маяка и подключитесь.\n4. Введите пароль по умолчанию, чтобы начать редактирование."
        },
        "ypb02": {
            "body": "## Обзор продукта\n\n**YPB02** — это Bluetooth® (BLE 5.0) маяк с встроенным **3-осевым акселерометром LIS3DH**. Он имеет тот же корпус IP67 и батарейку CR2477, что и YPB01, но поддерживает детекцию движения и телеметрию.\n\nМаяк можно настроить на изменение частоты отправки сигналов или отправку алармов только при движении, вибрации или падении.\n\n---\n\n## Ключевые свойства\n\n* **3-осевой акселерометр:** Датчик LIS3DH для измерения наклона и перемещения по осям X, Y, Z.\n* **Трансляция по триггеру:** Вещание только при движении, оповещение о падении или сокращение интервала до 100 мс при сдвиге.\n* **Защита IP67:** Пыле- и влагозащищенность.\n* **Заменяемая батарея:** Удобная замена монетной батарейки CR2477.\n\n---\n\n## Триггеры движения и телеметрия\n\nС помощью датчика LIS3DH маяк YPB02 поддерживает:\n1. **Вещание по активности:** Отправка стандартных кадров непрерывно и активация кадров с датчиков только при перемещении.\n2. **Двойной режим:** Режим сна в покое и вещание с интервалом 100 мс при движении.\n3. **Настройка чувствительности:** Пороги срабатывания можно откалибровать в приложении.\n\n---\n\n## Руководство по настройке\n\nНастройка выполняется по беспроводному каналу через приложение **BeaconSET+**:\n1. Установите **BeaconSET+**.\n2. Включите Bluetooth и геолокацию.\n3. Выполните сопряжение по MAC-адресу.\n4. Введите пароль администратора для изменения настроек."
        },
        "ypb03": {
            "body": "## Обзор продукта\n\n**YPB03** — это промышленный Bluetooth® Low Energy (BLE 5.0) маяк, оптимизированный под протокол **LINE Beacon** для трансляции стандартных пакетов **LINE Simple Beacon**. Работает от **4 батареек AA** (5800 мАч), обеспечивающих работу **до 10 лет**.\n\nС дальностью действия до **240 метров**, YPB03 идеален для крупных залов и торговых центров. Клиентам не нужно ставить отдельные приложения – уведомления приходят прямо в мессенджер **LINE**.\n\n---\n\n## Ключевые свойства\n\n* **Официальная совместимость с LINE Beacon:** Транслирует открытый протокол LINE Simple Beacon для связи с LINE Bot Messaging API.\n* **10 лет автономной работы:** Питание от 4 обычных пальчиковых батареек минимизирует затраты на обслуживание.\n* **Дальность 240м:** Мощный BLE 5.0 сигнал для аэропортов и выставочных комплексов.\n* **Взаимодействие без трения:** Пользователю достаточно включить Bluetooth и добавить ваш канал.\n* **Корпус IP65:** Защита от брызг воды и пыли для использования на складах.\n\n---\n\n## Руководство по интеграции LINE Beacon для разработчиков\n\n### Принцип работы триггеров приближения\nКогда пользователь с включенным Bluetooth и опцией LINE Beacon входит в зону сигнала:\n1. Приложение LINE обнаруживает **UUID сервиса `0xFE6F`** и считывает аппаратный ID (HWID).\n2. Платформа LINE отправляет событие `beacon` на Webhook-сервер вашего бота.\n3. Ваш бот реагирует в реальном времени, отправляя купоны или информацию.\n\n```mermaid\nsequenceDiagram\n    participant User as Пользователь (App LINE)\n    participant Beacon as YPB03 (0xFE6F + HWID)\n    participant LINE as Платформа LINE\n    participant Bot as Webhook-сервер (Bot)\n\n    Beacon->>User: Вещание BLE (UUID: FE6F + HWID)\n    User->>LINE: Переслать HWID + User ID\n    LINE->>Bot: Webhook POST (событие beacon: enter/stay/banner)\n    Bot->>User: Ответ через Messaging API (например, купон)\n```\n\n### Шаг 1: Зарегистрировать аппаратный ID (HWID)\n1. Войдите в **LINE Developers Console** или **LINE Official Account Manager**.\n2. В разделе Beacon зарегистрируйте устройство и получите **5-байтовый (10 шестнадцатеричных символов) HWID**.\n\n### Шаг 2: Настроить YPB03 через BeaconSET+\n1. Загрузите **BeaconSET+** и подключитесь к маяку (понадобится пароль).\n2. Выберите активный слот и укажите тип **Service Data** со следующими параметрами:\n   - **Service UUID:** `FE6F`\n   - **Data Value:** `FE6F` + `[Ваш 5-байтовый HWID]` + `7F00` (например, `FE6F01234567897F00`).\n3. Сохраните параметры и отключитесь. Маяк начнет вещание LINE Beacon.\n\n### Шаг 3: Обработка события в Webhook\nВаш сервер будет получать JSON-сообщения с данными `beacon`:\n* **`hwid`**: Аппаратный ID маяка.\n* **`type`**: Действие (`enter` при входе в зону, `stay` отправляется каждые 10 секунд при нахождении в зоне, `banner` при клике на баннер в приложении).\n\n---\n\n## Способы установки\n\n### Метод А: Промышленный скотч\n* **Поверхности:** Стекло, акрил, чистый алюминий.\n* **Процесс:** Очистите поверхность. Прижмите скотч (2 сек), подождите 30 мин и закрепите маяк.\n\n### Метод Б: Монтажный кронштейн (Рекомендуется)\n* **Поверхности:** Бетон, дерево, кирпич.\n* **Процесс:** Закрепите кронштейн на стене дюбелями и винтами. Вставьте YPB03 до щелчка.\n\n---\n\n## Руководство по настройке\n\nПараметры настраиваются по беспроводному интерфейсу через **BeaconSET+**:\n1. Скачайте **BeaconSET+** и активируйте Bluetooth.\n2. Найдите маяк в поиске и подключитесь к нему.\n3. Настройте UUID, Major, Minor, мощность сигнала и интервалы."
        },
        "ypb04": {
            "body": "## Обзор продукта\n\n**YPB04** — это перезаряжаемый плоский маяк в формате бейджа (карты) для контроля персонала и geofencing. Имеет размеры 86 × 55 × 6 мм и весит всего 19г, удобен для ношения на ланьярде.\n\nОснащен **физической кнопкой**, **вибромотором** и **RGB-светодиодом** для физического и визуального отклика. Включает магнитную зарядку, акселерометр и опциональную поддержку **RFID (LF/HF/UHF)**.\n\n---\n\n## Ключевые свойства\n\n* **3-осевой акселерометр:** Детекция перемещений для управления частотой сигналов.\n* **Световой и вибро отклик:** Встроенный вибромотор и RGB LED для алармов.\n* **Кнопка управления:** Внешняя кнопка для отправки SOS-сигналов.\n* **Интеграция RFID:** Опциональный чип для стандартных считывателей доступа.\n* **Магнитная зарядка:** Аккумулятор Li-po емкостью 270 мАч работает до 3 месяцев.\n\n---\n\n## Руководство по эксплуатации\n\n### Как включить бейдж\n* Удерживайте физическую кнопку нажатой в течение **3 секунд**.\n* Синий светодиод загорится на 3 секунды, и бейдж один раз завибрирует.\n\n### Как выключить бейдж\n* Из соображений безопасности ручное выключение невозможно. Шаутдаун выполняется только по воздуху через приложение **BeaconSET+** (требуется пароль).\n* При успешном выключении синий светодиод мигнет 5 раз.\n\n### Зарядка и батарея\n* **Низкий заряд:** При уровне заряда ниже 20% красный светодиод мигает каждые 3 секунды.\n* **Заряжается:** Красный светодиод горит постоянно.\n* **Заряжен:** Зеленый светодиод горит постоянно.\n\n### Триггеры кликов кнопки\n* **Двойной клик:** Синий светодиод мигнет 2 раза, вибро сработает 1 раз.\n* **Тройной клик:** Синий светодиод мигнет 3 раза, вибро сработает 2 раза.\n\n---\n\n## Руководство по настройке\n\nИспользуйте приложение **BeaconSET+** для настройки бейджа:\n1. Установите приложение и включите Bluetooth.\n2. Подключитесь к MAC-адресу бейджа.\n3. Введите пароль для изменения параметров и назначения кнопки."
        },
        "ypb05": {
            "body": "## Обзор продукта\n\n**YPB05** — это безбатарейный микро-маяк Bluetooth® (BLE 5.0), питающийся от любого USB-порта. Весит всего **2.0 г** и имеет размеры **18 × 14 × 6 мм**, являясь идеальным plug-and-play решением.\n\nБлагодаря отсутствию батарейки, YPB05 работает непрерывно и не требует обслуживания. Идеален для коммерческого вещания, рекламы в магазинах и локального позиционирования.\n\n---\n\n## Ключевые свойства\n\n* **Непрерывная работа:** Питание от USB-порта избавляет от необходимости менять батарейки.\n* **Ультралегкий и компактный:** Незаметно устанавливается в любой USB-разъем.\n* **Plug & Play:** Активируется мгновенно при подключении к питанию, без кнопок.\n* **Программный перезапуск:** Поддерживает отправку команд перезагрузки по воздуху.\n\n---\n\n## Руководство по настройке\n\nНастройка параметров выполняется без проводов с помощью **BeaconSET+**:\n1. Скачайте **BeaconSET+** и активируйте Bluetooth.\n2. Найдите YPB05 по его MAC-адресу.\n3. Введите пароль и настройте UUID, Major, Minor, мощность и интервалы."
        },
    },
    "zh-cn": {
        "ypb01": {
            "body": "## 产品概述\n\n**YPB01** 是一款体积精巧、坚固耐用的低功耗蓝牙 (BLE 5.0) 信标，适用于室内定位、活动监测与资产追踪。本产品采用超低功耗 nRF52 系列芯片，能同时广播标准 iBeacon 与 Eddystone (UID, URL, TLM) 信号。\n\n其旋转开闭式外壳设计方便更换纽扣电池，并具备 IP67 防尘防水等级，适合部署在潮湿或环境恶劣的场所。\n\n---\n\n## 主要特点\n\n* **高防护外壳：** 具备 IP67 防尘防水能力，支持室内与轻度室外安装。\n* **可更换电池：** 使用长效 CR2477 电池 (1000mAh)，转开外壳即可快速更换。\n* **多信号同时广播：** 支持同时设置最多 6 个独立广播通道，兼容 iBeacon 和 Eddystone 协议。\n* **实体电源开关：** 内置实体按键，可手动开启或关闭信标，避免运输或储存时浪费电量。\n\n---\n\n## 操作说明\n\n### 如何开启信标\n1. 顺时针转开外壳。\n2. 按住内部的“实体按键”约 **3 秒**。\n3. 蓝色 LED 指示灯会亮起 **5 秒** 后熄灭，表示 YPB01 已启动并开始发射信号。\n\n### 如何关闭信标\n1. 按住内部的实体按键约 **3 秒**。\n2. 蓝色 LED 指示灯会闪烁 **5 秒** 后熄灭，表示信标已关闭电源。\n\n---\n\n## 配置指南\n\nYPB01 的各项参数（如 UUID、Major、Minor、广播功率和广播间隔时间）可透过 **BeaconSET** 移动应用进行无线设定：\n1. 从 Google Play 或 Apple App Store 下载 **BeaconSET**。\n2. 开启手机的蓝牙与定位服务。\n3. 运行 App，扫描并寻找信标的 MAC 地址，点击进行连接。\n4. 输入默认管理密码，解锁后即可编辑参数。\n\n## 技术规格"
        },
        "ypb02": {
            "body": "## 产品概述\n\n**YPB02** 是一款内置三轴加速度传感器的低功耗蓝牙 (BLE 5.0) 运动感测信标。它与 YPB01 共享相同的精巧外观、可更换的 1000mAh CR2477 纽扣电池以及 IP67 防水防尘外壳，但额外增加了智能运动检测与遥测功能。\n\n本产品支持基于触发条件的广播模式，能够在设备移动、震动或发生跌落时，即时发射加速度数据或变更广播间隔。此设计能最大化降低电池消耗，并实现高阶的资产 activity 监测。\n\n---\n\n## 主要特点\n\n* **三轴加速度感测：** 内置 LIS3DH 传感器，提供 X、Y、Z 轴的位移、倾斜和运动遥测数据。\n* **触发式广播：** 支持设定特定触发条件（例如：仅在 motion 时广播、跌落警报，或在移动时将广播间隔缩短至 100 毫秒以追踪资产位移）。\n* **高防护外壳：** 具备 IP67 防尘防水能力，支持室内与轻度室外安装。\n* **可更换电池：** 使用长效 CR2477 电池 (1000mAh)，转开外壳即可快速更换。\n\n---\n\n## 运动触发与遥测数据\n\n透过 LIS3DH 传感器，YPB02 支持：\n1. **活动触发广播：** 平时持续广播标准 iBeacon/Eddystone 信号，但在信标位移或移动时才触发传感器数据信号。\n2. **静止/运动双参数模式：** 静止时保持静音（休眠），移动时则以 100 毫秒的间隔广播，以追踪即时位置。\n3. **门槛值校准：** 可透过 App 自定义加速度触发门槛与持续时间。\n\n---\n\n## 配置指南\n\nYPB02 的各项参数（包括加速度计门槛、触发条件、UUID、Major、Minor）可透过 **BeaconSET+** 应用程序进行无线设定：\n1. 从 Google Play 或 Apple App Store 下载 **BeaconSET+**。\n2. 开启手机的蓝牙与定位服务。\n3. 运行 App，扫描信标的 MAC 地址并点击连接。\n4. 输入默认密码解锁后即可编辑参数。\n\n## 技术规格"
        },
        "ypb03": {
            "body": "## 产品概述\n\n**YPB03** 是一款工业级长效低功耗蓝牙 (BLE 5.0) 信标，专为 **LINE Beacon** 广播协议优化，能发射标准的 **LINE Simple Beacon** 数据包。它使用 **4 × AA (三号) 干电池** 供电（总容量达 5800mAh），在默认参数下可提供长达 **10 年** 的超长续航力。\n\nYPB03 配备高增益天线，传输距离最远可达 **240 米**，是大型商业导购、智能零售导览和室内定位服务的首选。用户无需安装额外的 App，只要开启蓝牙，就能直接通过日常使用的 **LINE** 应用程序接收通知与互动，提供零摩擦的用户体验。\n\n---\n\n## 主要特点\n\n* **官方 LINE Beacon 兼容：** 广播开放的 LINE Simple Beacon 协议，将物理位置与您的 LINE 官方账号 (LINE Bot) 完美整合。\n* **10年免维护寿命：** 采用四颗标准可更换的三号电池，超大 5800mAh 电量让维护成本降至最低。\n* **240米超广覆盖：** 强劲的 BLE 5.0 信号穿透力，适用于大型展馆、机场、商场与多层零售空间。\n* **零安装无阻碍体验：** 用户仅需开启蓝牙并加入您的官方账号，无需额外下载第三方应用程序即可接收推送。\n* **坚固耐用防护：** IP65 防水防尘等级，能抵御仓库、工厂及室内工业环境中的灰尘与水气。\n\n---\n\n## LINE Beacon 开发者整合指南\n\n### Proximity Triggers 工作原理\n当开启蓝牙与 LINE Beacon 功能的用户进入 YPB03 的广播范围时：\n1. LINE 应用程序侦测到 **Service UUID `0xFE6F`**，并读取广播载荷中的硬件识别码 (HWID)。\n2. LINE 平台接收此信号后，向您的 LINE Bot 服务器发送 `beacon` Webhook 事件。\n3. 您的 Bot 服务器即时处理此事件，并向用户发送消息（如电子优惠券、迎宾消息或室内导览）。\n\n```mermaid\nsequenceDiagram\n    participant User as 用户 (LINE App)\n    participant Beacon as YPB03 (0xFE6F + HWID)\n    participant LINE as 平台 LINE\n    participant Bot as Webhook 服务器 (Bot)\n\n    Beacon->>User: 蓝牙广播 (UUID: FE6F + HWID)\n    User->>LINE: 转发 HWID + 用户 ID\n    LINE->>Bot: Webhook POST (beacon 事件: enter/stay/banner)\n    Bot->>User: 回复/推送消息 (例如：发送优惠券)\n```\n\n### 步骤 1：注册您的硬件 ID (HWID)\n1. 登录 **LINE Developers Console** 或 **LINE 官方账号管理后台**。\n2. 进入 **Beacon** 设置页面注册您的设备，系统将产生一个独有的 **5 字节 (10 个十六进制字符) 硬件 ID (HWID)**。\n\n### 步骤 2：使用 BeaconSET+ 设置 YPB03\nYPB03 的广播参数可透过无线空中设定：\n1. 下载 **BeaconSET+** 应用程序。\n2. 开启蓝牙，扫描 YPB03 的 MAC 地址并连接（输入默认密码解锁）。\n3. 选择一个启用的广播通道，将类型设为 **Service Data**：\n   - **Service UUID:** `FE6F`\n   - **Data Value:** `FE6F` + `[您的 5 字节 HWID]` + `7F00` (例如：若 HWID 为 `0123456789`，则填入 `FE6F01234567897F00`）。\n4. 保存设定并中断连接，信标将开始广播 LINE Beacon 信号。\n\n### 步骤 3：在 Webhook 中处理 Beacon 事件\n当用户触发时，您的服务器会收到包含 `beacon` 的 JSON 数据。主要的事件属性包括：\n* **`hwid`**：信标的 5 字节硬件识别码。\n* **`type`**：触发动作类型：\n  - `enter`：用户进入信标信号范围。\n  - `stay`：用户持续留在范围内（每 10 秒发送一次）。\n  - `banner`：用户点击了 LINE 聊天室顶部的 Beacon 横幅广告。\n\n---\n\n## 安装方法\n\n### 方法 A：工业双面胶带贴装\n* **适合表面：** 玻璃、压克力、干净的铝材或抛光磁砖等光滑表面。\n* **步骤：** 清洁粘贴表面。贴上双面胶并施压 2 秒，静置 30 分钟后再将信标安装上去。\n\n### 方法 B：螺丝支架固定安装（推荐）\n* **适合表面：** 水泥墙、石膏板、木材或砖墙。\n* **步骤：**\n  1. 使用随附的膨胀胶套与螺丝将支架固定到墙面上。\n  2. 将 YPB03 滑入支架插槽直至卡紧锁定。\n\n---\n\n## 配置指南\n\nYPB03 的各项参数（包括 UUID、Major、Minor、广播功率和广播间隔时间）可透过 **BeaconSET+** 移动应用程序进行无线设定：\n1. 从 Google Play 或 Apple App Store 下载 **BeaconSET+**。\n2. 开启手机的蓝牙与定位服务。\n3. 运行 App，扫描信标 of MAC 地址，点击连接并输入默认密码进行编辑。\n\n## 技术规格"
        },
        "ypb04": {
            "body": "## 产品概述\n\n**YPB04** 是一款卡片型低功耗蓝牙 (BLE 5.0) 智能工卡信标，适用于智能办公室考勤、人员区域定位与地理围栏。其极薄的外观尺寸 (86 × 55 × 6 mm，重量仅 19 克) 可以轻松挂在挂绳上或配戴于制服上。\n\nYPB04 配备了 **实体按钮**、**震动马达** 与 **RGB 指示灯**，可提供视觉与触觉的反馈。本产品支持磁吸充电与内置三轴加速度传感器，并可选配支持双频 **RFID (LF/HF/UHF)**，能完美将蓝牙定位技术与传统实体门禁刷卡系统整合。\n\n---\n\n## 主要特点\n\n* **三轴加速度传感器：** 内置传感器以检测位移、运动与静止状态。\n* **双重反馈机制：** 配备 1 个震动马达与 1 个 RGB 指示灯，提供即时的状态警示与警报反馈。\n* **实体控制按键：** 外部实体按钮可设定触发特定广播或一键报警 (SOS)。\n* **选配 RFID 整合：** 可整合低频、高频或超高频 RFID 芯片，支持传统感应门禁。\n* **磁吸式充电：** 内置 270mAh 锂聚合物电池，随附磁吸充电线，一般使用下续航可达 3 个月。\n\n---\n\n## 操作说明\n\n### 如何开启工卡电源\n* 按住实体按键 **3 秒**。\n* 蓝色 LED 指示灯会亮起 3 秒，且工卡会震动一次，表示启动成功。\n\n### 如何关闭工卡电源\n* 为确保人员安全与管理合规，工卡无法手动关闭。必须透过 **BeaconSET+ App** 连接并输入管理密码，以无线方式将其关闭。\n* 成功关闭时，蓝色 LED 会闪烁 5 次。\n\n### 电量状态与充电指示\n* **低电量警示：** 当电量低于 20% 时，红色 LED 会每 3 秒闪烁一次。\n* **充电中：** 充电时红色 LED 会恒亮。\n* **充电完成：** 充满电后绿色 LED 会恒亮。\n\n### 按钮点击触发广播\n您可以设定实体按钮的点击次数来触发特定警报或数据发射：\n* **双击：** 蓝色 LED 闪烁 2 次，马达震动一次。\n* **三击：** 蓝色 LED 闪烁 3 次，马达震动两次。\n\n---\n\n## 配置指南\n\nYPB04 的各项参数（包括按键触发定义、UUID、Major、Minor、广播功率）可透过 **BeaconSET+** 应用程序进行设定：\n1. 下载并安装 **BeaconSET+**。\n2. 开启蓝牙与定位服务，扫描并连接工卡的 MAC 地址。\n3. 输入管理密码以进行参数修改。\n\n## 技术规格"
        },
        "ypb05": {
            "body": "## 产品概述\n\n**YPB05** 是一款免电池、极致紧凑的低功耗蓝牙 (BLE 5.0) 微型信标，直接由任何标准 Micro USB 或 USB 端口供电。其重量仅有 **2.0 克**，尺寸为 **18 × 14 × 6 mm**，是一款即插即用、携带极其方便的定位信标。\n\n由于无需更换电池，YPB05 非常适合需要 24/7 不间断运行的长期广播应用，例如零售广告推送、智能教室考勤与桌面型室内定位。它可以直接插在电脑、USB 充电头、Wi-Fi 路由器或移动电源上运行。\n\n---\n\n## 主要特点\n\n* **免电池持续运行：** 由标准 USB 接口供电，免除电池维护成本，保证 24/7 服务在线。\n* **极致轻巧微型：** 仅重 2.0g，能隐蔽地部署在 any USB 设备或室内环境中。\n* **即插即用：** 插入 USB 端口即可立刻启动广播，无需任何手动操作。\n* **支持软件重启：** 支持发送无线指令进行软件重启，无需拔插设备即可重设。\n\n---\n\n## 配置指南\n\nYPB05 的参数（如 UUID、Major、Minor、广播功率 and 间隔时间）可透过 **BeaconSET+** 进行无线设定：\n1. 下载并安装 **BeaconSET+**。\n2. 开启手机蓝牙与定位服务，扫描并连接 YPB05。\n3. 输入默认密码进行编辑与保存设定。\n\n## 技术规格"
        },
    },
    "zh-tw": {
        "ypb01": {
            "body": "## 產品概述\n\n**YPB01** 是一款體積精巧、堅固耐用的低功耗藍牙 (BLE 5.0) 信標，適用於室內定位、活動監測與資產追蹤。本產品採用超低功耗 nRF52 系列晶片，能同時廣播標準 iBeacon 與 Eddystone (UID, URL, TLM) 訊號。\n\n其旋轉開閉式外殼設計方便更換鈕扣電池，並具備 IP67 防塵防水等級，適合部署在潮濕或環境惡劣的場所。\n\n---\n\n## 主要特點\n\n* **高防護外殼：** 具備 IP67 防塵防水能力，支援室內與輕度室外安裝。\n* **可更換電池：** 使用長效 CR2477 電池 (1000mAh)，轉開外殼即可快速更換。\n* **多訊號同時廣播：** 支援同時設定最多 6 個獨立廣播通道，相容 iBeacon 和 Eddystone 協定。\n* **實體電源開關：** 內建實體按鍵，可手動開啟或關閉信標，避免運輸或儲存時浪費電量。\n\n---\n\n## 操作說明\n\n### 如何開啟信標\n1. 順時針轉開外殼。\n2. 按住內部的「實體按鍵」約 **3 秒**。\n3. 藍色 LED 指示燈會亮起 **5 秒** 後熄滅，表示 YPB01 已啟動並開始發射訊號。\n\n### 如何關閉信標\n1. 按住內部的實體按鍵約 **3 秒**。\n2. 藍色 LED 指示燈會閃爍 **5 秒** 後熄滅，表示信標已關閉電源。\n\n---\n\n## 配置指南\n\nYPB01 的各項參數（如 UUID、Major、Minor、廣播功率和廣播間隔時間）可透過 **BeaconSET** 行動應用程式進行無線設定：\n1. 從 Google Play 或 Apple App Store 下載 **BeaconSET**。\n2. 開啟手機的藍牙與定位服務。\n3. 執行 App，掃描並尋找信標的 MAC 位址，點擊進行連線。\n4. 輸入預設管理密碼，解鎖後即可編輯參數。\n\n## 技術規格"
        },
        "ypb02": {
            "body": "## 產品概述\n\n**YPB02** 是一款內建三軸加速度感測器的低功耗藍牙 (BLE 5.0) 運動感測信標。它與 YPB01 共享相同的精巧外觀、可更換的 1000mAh CR2477 鈕扣電池以及 IP67 防水防塵外殼，但額外增加了智慧運動檢測與遙測功能。\n\n本產品支援基於觸發條件的廣播模式，能夠在設備移動、震動或發生跌落時，即時發射加速度數據或變更廣播間隔。此設計能最大化降低電池消耗，並實現高階的資產活動監測。\n\n---\n\n## 主要特點\n\n* **三軸加速度感測：** 內建 LIS3DH 感測器，提供 X、Y、Z 軸的位移、傾斜和運動遙測數據。\n* **觸發式廣播：** 支援設定特定觸發條件（例如：僅在運動時廣播、跌落警報，或在移動時將廣播間隔縮短至 100 毫秒以追蹤資產位移）。\n* **高防護外殼：** 具備 IP67 防塵防水能力，支援室內與輕度室外安裝。\n* **可更換電池：** 使用長效 CR2477 電池 (1000mAh)，轉開外殼即可快速更換。\n\n---\n\n## 運動觸發與遙測數據\n\n透過 LIS3DH 感測器，YPB02 支援：\n1. **活動觸發廣播：** 平時持續廣播標準 iBeacon/Eddystone 訊號，但在信標位移或移動時才觸發傳感器數據訊號。\n2. **靜止/運動雙參數模式：** 靜止時保持靜音（休眠），移動時則以 100 毫秒的間隔廣播，以追蹤即時位置。\n3. **門檻值校準：** 可透過 App 自訂加速度觸發門檻與持續時間。\n\n---\n\n## 配置指南\n\nYPB02 的各項參數（包括加速度計門檻、觸發條件、UUID、Major、Minor）可透過 **BeaconSET+** 應用程式進行無線設定：\n1. 從 Google Play 或 Apple App Store 下載 **BeaconSET+**。\n2. 開啟手機的藍牙與定位服務。\n3. 執行 App，掃描信標的 MAC 位址並點擊連線。\n4. 輸入預設密碼解鎖後即可編輯參數。\n\n## 技術規格"
        },
        "ypb03": {
            "body": "## 產品概述\n\n**YPB03** 是一款工業級長效低功耗藍牙 (BLE 5.0) 信標，專為 **LINE Beacon** 廣播協議優化，能發射標準的 **LINE Simple Beacon** 封包。它使用 **4 × AA (三號) 乾電池** 供電（總容量達 5800mAh），在預設參數下可提供長達 **10 年** 的超長續航力。\n\nYPB03 配備高增益天線，傳輸距離最遠可達 **240 公尺**，是大型商業導購、智慧零售導覽和室內定位服務的首選。使用者無需安裝額外的 App，只要開啟藍牙，就能直接透過日常使用的 **LINE** 應用程式接收通知與互動，提供零摩擦的用戶體驗。\n\n---\n\n## 主要特點\n\n* **官方 LINE Beacon 相容：** 廣播開放的 LINE Simple Beacon 協定，將物理位置與您的 LINE 官方帳號 (LINE Bot) 完美整合。\n* **10年免維護壽命：** 採用四顆標準可更換的三號電池，超大 5800mAh 電量讓維護成本降至最低。\n* **240公尺超廣覆蓋：** 強勁的 BLE 5.0 訊號穿透力，適用於大型展館、機場、商場與多層零售空間。\n* **零安裝無阻礙體驗：** 用戶僅需開啟藍牙並加入您的官方帳號，無需額外下載第三方應用程式即可接收推播。\n* **堅固耐用防護：** IP65 防水防塵等級，能抵禦倉庫、工廠及室內工業環境中的灰塵與水氣。\n\n---\n\n## LINE Beacon 開發者整合指南\n\n### Proximity Triggers 工作原理\n當開啟藍牙與 LINE Beacon 功能的用戶進入 YPB03 的廣播範圍時：\n1. LINE 應用程式偵測到 **Service UUID `0xFE6F`**，並讀取廣播載荷中的硬體識別碼 (HWID)。\n2. LINE 平台接收此訊號後，向您的 LINE Bot 伺服器發送 `beacon` Webhook 事件。\n3. 您的 Bot 伺服器即時處理此事件，並向用戶發送訊息（如電子優惠券、迎賓訊息或室內導覽）。\n\n```mermaid\nsequenceDiagram\n    participant User as 用戶 (LINE App)\n    participant Beacon as YPB03 (0xFE6F + HWID)\n    participant LINE as LINE 平台\n    participant Bot as Webhook 伺服器 (Bot)\n\n    Beacon->>User: 藍牙廣播 (UUID: FE6F + HWID)\n    User->>LINE: 轉發 HWID + 用戶 ID\n    LINE->>Bot: Webhook POST (beacon 事件: enter/stay/banner)\n    Bot->>User: 回覆/推播訊息 (例如：發送優惠券)\n```\n\n### 步驟 1：註冊您的硬體 ID (HWID)\n1. 登入 **LINE Developers Console** 或 **LINE 官方帳號管理後台**。\n2. 進入 **Beacon** 設置頁面註冊您的設備，系統將產生一個獨有的 **5 位元組 (10 個十六進位字元) 硬體 ID (HWID)**。\n\n### 步驟 2：使用 BeaconSET+ 設定 YPB03\nYPB03 的廣播參數可透過無線空中設定：\n1. 下載 **BeaconSET+** 應用程式。\n2. 開啟藍牙，掃描 YPB03 的 MAC 位址並連線（輸入預設密碼解鎖）。\n3. 選擇一個啟用的廣播通道，將類型設為 **Service Data**：\n   - **Service UUID:** `FE6F`\n   - **Data Value:** `FE6F` + `[您的 5 位元組 HWID]` + `7F00` (例如：若 HWID 為 `0123456789`，則填入 `FE6F01234567897F00`）。\n4. 儲存設定並中斷連線，信標將開始廣播 LINE Beacon 訊號。\n\n### 步驟 3：在 Webhook 中處理 Beacon 事件\n當用戶觸發時，您的伺服器會收到包含 `beacon` 的 JSON 資料。主要的事件屬性包括：\n* **`hwid`**：信標的 5 位元組硬體識別碼。\n* **`type`**：觸發動作類型：\n  - `enter`：用戶進入信標訊號範圍。\n  - `stay`：用戶持續留在範圍內（每 10 秒發送一次）。\n  - `banner`：用戶點擊了 LINE 聊天室頂部的 Beacon 橫幅廣告。\n\n---\n\n## 安裝方法\n\n### 方法 A：工業雙面膠帶貼裝\n* **適合表面：** 玻璃、壓克力、乾淨的鋁材或拋光磁磚等光滑表面。\n* **步驟：** 清潔黏貼表面。貼上雙面膠並施壓 2 秒，靜置 30 分鐘後再將信標安裝上去。\n\n### 方法 B：螺絲支架固定安裝（推薦）\n* **適合表面：** 水泥牆、石膏板、木材或磚牆。\n* **步驟：**\n  1. 使用隨附的壁虎與螺絲將支架固定到牆面上。\n  2. 將 YPB03 滑入支架插槽直至卡緊鎖定。\n\n---\n\n## 配置指南\n\nYPB03 的各項參數（包括 UUID、Major、Minor、廣播功率和廣播間隔時間）可透過 **BeaconSET+** 行動應用程式進行無線設定：\n1. 從 Google Play 或 Apple App Store 下載 **BeaconSET+**。\n2. 開啟手機的藍牙與定位服務。\n3. 執行 App，掃描信標的 MAC 位址，點擊連線並輸入預設密碼進行編輯。\n\n## 技術規格"
        },
        "ypb04": {
            "body": "## 產品概述\n\n**YPB04** 是一款卡片型低功耗藍牙 (BLE 5.0) 智慧工卡信標，適用於智慧辦公室考勤、人員區域定位與地理圍欄。其極薄的外觀尺寸 (86 × 55 × 6 mm，重量僅 19 克) 可以輕鬆掛在掛繩上或配戴於制服上。\n\nYPB04 配備了 **實體按鈕**、**震動馬達** 與 **RGB 指示燈**，可提供視覺與觸覺的反饋。本產品支援磁吸充電與內建三軸加速度感測器，並可選配支援雙頻 **RFID (LF/HF/UHF)**，能完美將藍牙定位技術與傳統實體門禁刷卡系統整合。\n\n---\n\n## 主要特點\n\n* **三軸加速度感測器：** 內建感測器以檢測位移、運動與靜止狀態。\n* **雙重反饋機制：** 配備 1 個震動馬達與 1 個 RGB 指示燈，提供即時的狀態警示與警報反饋。\n* **實體控制按鍵：** 外部實體按鈕可設定觸發特定廣播或一鍵報警 (SOS)。\n* **選配 RFID 整合：** 可整合低頻、高頻或超高频 RFID 晶片，支援傳統感應門禁。\n* **磁吸式充電：** 內建 270mAh 鋰聚合物電池，隨附磁吸充電線，一般使用下續航可達 3 個月。\n\n---\n\n## 操作說明\n\n### 如何開啟工卡電源\n* 按住實體按鍵 **3 秒**。\n* 藍色 LED 指示燈會亮起 3 秒，且工卡會震動一次，表示啟動成功。\n\n### 如何關閉工卡電源\n* 為確保人員安全與管理合規，工卡無法手動關閉。必須透過 **BeaconSET+ App** 連線並輸入管理密碼，以無線方式將其關閉。\n* 成功關閉時，藍色 LED 會閃爍 5 次。\n\n### 電量狀態與充電指示\n* **低電量警示：** 當電量低於 20% 時，紅色 LED 會每 3 秒職閃爍一次。\n* **充電中：** 充電時紅色 LED 會恆亮。\n* **充電完成：** 充滿電後綠色 LED 會恆亮。\n\n### 按鈕點擊觸發廣播\n您可以設定實體按鈕的點擊次數來觸發特定警報或數據發射：\n* **雙擊：** 藍色 LED 閃爍 2 次，馬達震動一次。\n* **三擊：** 藍色 LED 閃爍 3 次，馬達震動兩次。\n\n---\n\n## 配置指南\n\nYPB04 的各項參數（包括按鈕觸發定義、UUID、Major、Minor、廣播功率）可透過 **BeaconSET+** 應用程式進行設定：\n1. 下載並安裝 **BeaconSET+**。\n2. 開啟藍牙與定位服務，掃描並連接工卡的 MAC 位址。\n3. 輸入管理密碼以進行參數修改。\n\n## 技術規格"
        },
        "ypb05": {
            "body": "## 產品概述\n\n**YPB05** 是一款免電池、極致緊湊的低功耗藍牙 (BLE 5.0) 微型信標，直接由任何標準 Micro USB 或 USB 埠供電。其重量僅有 **2.0 公克**，尺寸為 **18 × 14 × 6 mm**，是一款隨插即用、攜帶極其方便的定位信標。\n\n由於無需更換電池，YPB05非常適合需要 24/7 不間斷運作的長期廣播應用，例如零售廣告推播、智慧教室考勤與桌面型室內定位。它可以直接插在電腦、USB 充電頭、Wi-Fi 路由器或行動電源上運作。\n\n---\n\n## 主要特點\n\n* **免電池持續運作：** 由標準 USB 介面供電，免除電池維護成本，保證 24/7 服務在線。\n* **極致輕巧微型：** 僅重 2.0g，能隱蔽地部署在任何 USB 設備或室內環境中。\n* **隨插即用：** 插入 USB 埠即可立刻啟動廣播，無需任何手動操作。\n* **支援軟體重啟：** 支援發送無線指令進行軟體重啟，無需拔插設備即可重設。\n\n---\n\n## 配置指南\n\nYPB05 的參數（如 UUID、Major、Minor、廣播功率和間隔時間）可透過 **BeaconSET+** 進行無線設定：\n1. 下載並安裝 **BeaconSET+**。\n2. 開啟手機藍牙與定位服務，掃描並連接 YPB05。\n3. 輸入預設密碼進行編輯與保存設定。\n\n## 技術規格"
        },
    },
}

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

def translate_product_page(lang, model, blueprint, en_content):
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

    translated = en_content
    translated = re.sub(r'^title: ".*?"', f'title: "{localized_title}"', translated, flags=re.M)
    
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

    lines = translated.split("\n")
    table_started = False
    new_lines = []
    
    d = SPEC_DICTS.get(lang, {})
    
    table_header_tr = {
        "zh-tw": "| 參數項目 | 技術規格 | 備註說明 |",
        "zh-cn": "| 参数项目 | 技术规格 | 备注说明 |",
        "ja": "| パラメータ | 技術仕様 | 備考 |",
        "ar": "| المعيار | المواصفات | ملاحظات |",
        "de": "| Parameter | Spezifikationen | Anmerkungen |",
        "es": "| Parámetro | Especificaciones | Observaciones |",
        "fr": "| Paramètre | Spécifications | Remarques |",
        "pt": "| Parâmetro | Especificações | Observações |",
        "ru": "| Параметр | Технические характеристики | Примечания |"
    }
    
    for line in lines:
        if line.startswith("| :---") or line.startswith("| ---"):
            new_lines.append(line)
            continue
        if line.startswith("| **Parameter**") or line.startswith("| Parameter"):
            new_lines.append(table_header_tr.get(lang, line))
            table_started = True
            continue
        if table_started and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                raw_key = parts[1].replace("**", "")
                loc_key = d.get(raw_key, raw_key)
                parts[1] = f"**{loc_key}**"
                
                raw_val = parts[2]
                for k, v in d.items():
                    if k in raw_val:
                        raw_val = raw_val.replace(k, v)
                parts[2] = raw_val
                
                if len(parts) >= 5:
                    raw_rem = parts[3]
                    for k, v in d.items():
                        if k in raw_rem:
                            raw_rem = raw_rem.replace(k, v)
                    parts[3] = raw_rem
                    
                line = " | ".join(parts).strip()
            new_lines.append(line)
        else:
            table_started = False
            new_lines.append(line)
            
    translated = "\n".join(new_lines)

    fm_match = re.match(r'^---.*?---', translated, flags=re.DOTALL)
    if not fm_match:
        return translated
    frontmatter = fm_match.group(0)
    
    body_content = ""
    if lang in BODY_TEMPLATES and model in BODY_TEMPLATES[lang]:
        body_content = BODY_TEMPLATES[lang][model]["body"]
    else:
        body_content = en_content
        body_content = re.sub(r'^---.*?---', '', body_content, flags=re.DOTALL).strip()
        headers_en = ["Product Overview", "Technical Specifications", "Key Features", "Configuration Guidance", "Product Gallery", "Operational Guide", "Motion Trigger & Telemetry", "Installation Methods"]
        translation_headers = {
            "ar": ["نظرة عامة على المنتج", "المواصفات الفنية", "الميزات الرئيسية", "إرشادات التهيئة", "معرض صور المنتج", "دليل التشغيل", "استشعار الحركة والقياس عن بعد", "طرق التثبيت"],
            "de": ["Produktübersicht", "Technische Spezifikationen", "Hauptmerkmale", "Konfigurationsanleitung", "Produktgalerie", "Bedienungsanleitung", "Bewegungsauslöser & Telemetrie", "Installationsmethoden"],
            "es": ["Descripción del producto", "Especificaciones técnicas", "Características clave", "Guía de configuración", "Galería del producto", "Guía de operación", "Activación por movimiento y telemetría", "Métodos de instalación"],
            "fr": ["Présentation du produit", "Spécifications techniques", "Caractéristiques principales", "Guide de configuration", "Galerie du produit", "Guide d'utilisation", "Détection de mouvement et télémétrie", "Méthodes d'installation"],
            "pt": ["Visão geral do produto", "Especificações técnicas", "Principais recursos", "Guia de configuração", "Galeria do produto", "Guia de operação", "Gatilho de movimento e telemetria", "Métodos de instalação"],
            "ru": ["Обзор продукта", "Технические характеристики", "Ключевые свойства", "Руководство по настройке", "Галерея продукта", "Руководство по эксплуатации", "Триггеры движения и телеметрия", "Способы установки"]
        }
        if lang in translation_headers:
            loc_list = translation_headers[lang]
            for i, en_h in enumerate(headers_en):
                body_content = body_content.replace(f"## {en_h}", f"## {loc_list[i]}")
                
        if model == "ypb01":
            body_content = body_content.replace("BeaconSET+", "BeaconSET")

    cta_alert = LANDING_INFO.get(lang, LANDING_INFO["zh-tw"])["cta"]
    gallery_img = f"/images/products/ibeacon/{model}.png"
    
    gallery_titles = {
        "zh-tw": "產品圖片", "zh-cn": "产品图片", "ja": "製品ギャラリー", 
        "ar": "معرض صور المنتج", "de": "Produktgalerie", "es": "Galería del producto",
        "fr": "Galerie du produit", "pt": "Galeria do produto", "ru": "Галерея продукта"
    }
    g_title = gallery_titles.get(lang, "Product Gallery")
    
    gallery_block = f"""## {g_title}\n\n{{{{< gallery >}}}}\n  <img src="{gallery_img}" alt="Yupitek {model.upper()}" />\n{{{{< /gallery >}}}}"""
    alert_block = f"""{{{{< alert >}}}}\n{cta_alert}\n{{{{< /alert >}}}}"""
    
    table_lines = []
    table_active = False
    for line in translated.split("\n"):
        if line.startswith("|") and ("---" in line or "項目" in line or "项目" in line or "Parameter" in line or "Para" in line or "Пара" in line or "المع" in line or "**" in line):
            table_active = True
            table_lines.append(line)
        elif table_active and line.startswith("|"):
            table_lines.append(line)
        else:
            table_active = False
    
    table_content = "\n".join(table_lines)
    
    spec_titles = ["## 技術規格", "## 技术规格", "## 技術仕様", "## Technical Specifications", "## المواصفات الفنية", "## Technische Spezifikationen", "## Especificaciones técnicas", "## Spécifications techniques", "## Especificações técnicas", "## Технические характеристики"]
    
    inserted_table = False
    for spec_title in spec_titles:
        if spec_title in body_content:
            body_content = body_content.replace(spec_title, f"{spec_title}\n\n{table_content}")
            inserted_table = True
            break
            
    if not inserted_table:
        body_content += f"\n\n## Technical Specifications\n\n{table_content}"

    final_content = f"""{frontmatter}

{body_content}

---

{gallery_block}

---

{alert_block}
"""
    return final_content

def update_localized_products_index(lang):
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

    if "products/ibeacon/" in content:
        print(f"iBeacon card already exists in {path}")
        return

    pattern = r'(\{\{<\s*card\s+title="[^"]+"\s+href="[^"]*products/graphiccard/".*?\{\{<\s*/card\s*>\}\})'
    match = re.search(pattern, content, flags=re.DOTALL)
    if not match:
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

    en_templates = {}
    en_base_path = os.path.join(base_dir, "content/en/products/ibeacon")
    
    for model in ["ypb01", "ypb02", "ypb03", "ypb04", "ypb05"]:
        p_file = os.path.join(en_base_path, model, "_index.md")
        with open(p_file, "r", encoding="utf-8") as f:
            en_templates[model] = f.read()

    for lang in LANGUAGES:
        print(f"\nProcessing language: {lang.upper()}")
        lang_dir = os.path.join(base_dir, "content", lang, "products", "ibeacon")
        os.makedirs(lang_dir, exist_ok=True)
        
        landing_md = generate_category_index(lang, LANDING_INFO[lang])
        landing_path = os.path.join(lang_dir, "_index.md")
        with open(landing_path, "w", encoding="utf-8") as f:
            f.write(landing_md)
        print(f"Created category index at: {landing_path}")

        for model in ["ypb01", "ypb02", "ypb03", "ypb04", "ypb05"]:
            prod_dir = os.path.join(lang_dir, model)
            os.makedirs(prod_dir, exist_ok=True)
            
            blueprint_spec_maps = {
                "ypb01": {
                    "title": "YPB01 BLE 5.0 Beacon",
                    "spec_keys": ["Chip Model", "Bluetooth Version", "Waterproof Level", "Transmission Range", "Antenna Impedance", "Power Source", "Operating Voltage", "Peak Current", "Dimensions", "Default Settings"],
                    "spec_vals": []
                },
                "ypb02": {
                    "title": "YPB02 Motion-Sensing BLE Beacon",
                    "spec_keys": ["Chip Model", "Bluetooth Version", "Waterproof Level", "Sensor", "Transmission Range", "Antenna Impedance", "Power Source", "Operating Voltage", "Peak Current", "Dimensions", "Default Settings"],
                    "spec_vals": []
                },
                "ypb03": {
                    "title": "YPB03 LINE Beacon",
                    "spec_keys": ["Chip Model", "Bluetooth Version", "Waterproof Level", "Transmission Range", "Protocol Support", "Service UUID", "Service Data Format", "Power Source", "Battery Lifetime", "Material", "Dimensions", "Net Weight"],
                    "spec_vals": []
                },
                "ypb04": {
                    "title": "YPB04 Rechargeable Badge Beacon",
                    "spec_keys": ["Chip Model", "Bluetooth Version", "Waterproof Level", "Sensors", "Feedback Elements", "Control Button", "RFID Compatibility", "Transmission Range", "Power Source", "Battery Lifetime", "Charging Time", "Dimensions & Weight"],
                    "spec_vals": []
                },
                "ypb05": {
                    "title": "YPB05 Micro USB Beacon",
                    "spec_keys": ["Chip Model", "Bluetooth Version", "Power Source", "Operating Voltage", "Max Current", "Transmission Range", "Antenna Impedance", "Dimensions & Weight", "Default Settings"],
                    "spec_vals": []
                }
            }
            
            translated_content = translate_product_page(lang, model, blueprint_spec_maps[model], en_templates[model])
            prod_path = os.path.join(prod_dir, "_index.md")
            with open(prod_path, "w", encoding="utf-8") as f:
                f.write(translated_content)
            print(f"Created product page for {model.upper()} at: {prod_path}")

        update_localized_products_index(lang)

    print("\nGeneration process complete!")

if __name__ == "__main__":
    main()
