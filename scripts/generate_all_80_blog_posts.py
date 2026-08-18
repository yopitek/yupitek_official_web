#!/usr/bin/env python3
"""
generate_all_80_blog_posts.py
Complete generator for 8 articles x 10 locales (80 pages) for yupitek.com
"""

import os
import re

CONTENT_DIR = "/home/yopitek/Project/yupitek_official_web/content"
SOURCE_DIR = "/home/yopitek/Documents/Obsidian_vault/GX10_HQ/F_Daily/01_Daily_note/2026/2026-08/2026-08-17/blog_article/new_article/doc"

LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]

# Definitions for each of the 8 articles
ARTICLES_CONFIG = [
    {
        "id": "01",
        "file": "01_article.md",
        "slug": "mediatek-mt7921au-linux-in-kernel-driver-awus036axml",
        "image": "/images/blog/01_AWUS036AXML_blueprint.jpg",
        "image_alt": "ALFA AWUS036AXML MediaTek MT7921AU Linux In-Kernel Driver Blueprint",
        "date": "2026-08-18",
        "sku": "AWUS036AXML",
        "title": {
            "zh-tw": "別再折騰驅動編譯！為什麼 MediaTek MT7921AU 是現代 Linux 與 Kali 開發者的首選？",
            "zh-cn": "别再折腾驱动编译！为什么 MediaTek MT7921AU 是现代 Linux 与 Kali 开发者的首选？",
            "en": "Stop Wrestling with DKMS: Why MediaTek MT7921AU is the Top Choice for Modern Linux & Kali Developers",
            "ja": "DKMSコンパイルの苦労から解放！なぜMediaTek MT7921AUが最新Linux・Kali開発者に選ばれるのか？",
            "ar": "توقف عن المعاناة مع تجميع التعريفات: لماذا يعتبر MediaTek MT7921AU الخيار الأفضل لمطوري لينكس وكالي؟",
            "es": "¡Olvídate de compilar drivers! Por qué MediaTek MT7921AU es la opción preferida para desarrolladores de Linux y Kali",
            "pt": "Esqueça a compilação de drivers! Por que o MediaTek MT7921AU é a escolha ideal para desenvolvedores Linux e Kali",
            "ru": "Забудьте о сборке драйверов: почему MediaTek MT7921AU — лучший выбор для пользователей Linux и Kali",
            "de": "Schluss mit Treiber-Kompilierung: Warum der MediaTek MT7921AU die erste Wahl für Linux- und Kali-Entwickler ist",
            "fr": "Finie la compilation de pilotes : Pourquoi le MediaTek MT7921AU est le choix idéal pour Linux et Kali"
        },
        "description": {
            "zh-tw": "深入解析 MediaTek MT7921AU（AWUS036AXML）的 Linux 核心原生支援優勢，對比 Realtek RTL8812AU DKMS 編譯痛點，提供監聽模式與採購評估工作表。",
            "zh-cn": "深入解析 MediaTek MT7921AU（AWUS036AXML）的 Linux 内核原生支持优势，对比 Realtek RTL8812AU DKMS 编译痛点，提供监听模式与采购评估指南。",
            "en": "In-depth technical comparison between MediaTek MT7921AU in-kernel driver (mt7921u) and Realtek RTL8812AU DKMS builds on Kali Linux, featuring monitor mode setup and buying checklist.",
            "ja": "MediaTek MT7921AU（AWUS036AXML）のLinuxカーネル標準サポートの利点を徹底解説。Realtek RTL8812AUとの比較、モニターモード設定、導入チェックシートを収録。",
            "ar": "تحليل تقني معمق لمزايا دعم نواة لينكس المدمج لشريحة MediaTek MT7921AU مقارنة بتعريفات Realtek RTL8812AU مع إعداد وضع المراقبة ودليل الشراء.",
            "es": "Análisis técnico profundo de las ventajas del driver nativo en el kernel de MediaTek MT7921AU frente a Realtek RTL8812AU, con configuración de modo monitor y checklist.",
            "pt": "Análise técnica das vantagens do driver nativo no kernel do MediaTek MT7921AU em comparação com o Realtek RTL8812AU, com guia de modo monitor e checklist.",
            "ru": "Подробный технический анализ встроенного драйвера MediaTek MT7921AU в ядре Linux по сравнению с RTL8812AU, настройка режима мониторинга и чек-лист выбора.",
            "de": "Technischer Vergleich zwischen dem nativen Linux-Kernel-Treiber des MediaTek MT7921AU und Realtek RTL8812AU DKMS-Builds für Kali Linux mit Monitor-Mode-Praxis.",
            "fr": "Comparatif technique approfondi du pilote natif MediaTek MT7921AU face au Realtek RTL8812AU sous Kali Linux, avec configuration du mode moniteur et guide d'achat."
        },
        "faq": [
            {
                "q": {"zh-tw": "AWUS036AXML 是否支援 macOS？", "zh-cn": "AWUS036AXML 是否支持 macOS？", "en": "Does the AWUS036AXML support macOS?", "ja": "AWUS036AXMLはmacOSに対応していますか？", "ar": "هل يدعم AWUS036AXML نظام macOS؟", "es": "¿AWUS036AXML es compatible con macOS?", "pt": "O AWUS036AXML é compatível com macOS?", "ru": "Поддерживает ли AWUS036AXML систему macOS?", "de": "Unterstützt der AWUS036AXML macOS?", "fr": "L'AWUS036AXML est-il compatible avec macOS ?"},
                "a": {"zh-tw": "不支援。目前無適用於 Intel 或 Apple Silicon Mac 的 MT7921AU 驅動程式。", "zh-cn": "不支持。目前无适用于 Intel 或 Apple Silicon Mac 的 MT7921AU 驱动程序。", "en": "No. Currently there are no MT7921AU macOS drivers for Intel or Apple Silicon Macs.", "ja": "非対応です。現在IntelおよびApple Silicon Mac用のMT7921AUドライバは存在しません。", "ar": "لا يدعم. لا تتوفر حالياً أي تعريفات لشريحة MT7921AU لأنظمة ماك.", "es": "No. Actualmente no existen drivers de MT7921AU para macOS en Intel o Apple Silicon.", "pt": "Não. Atualmente não existem drivers do MT7921AU para macOS em Intel ou Apple Silicon.", "ru": "Нет. В настоящее время драйверы MT7921AU для macOS на Intel или Apple Silicon отсутствуют.", "de": "Nein. Derzeit gibt es keine MT7921AU macOS-Treiber für Intel oder Apple Silicon Macs.", "fr": "Non. Il n'existe actuellement aucun pilote macOS MT7921AU pour Intel ou Apple Silicon."}
            },
            {
                "q": {"zh-tw": "在 Linux 上使用需要手動編譯驅動嗎？", "zh-cn": "在 Linux 上使用需要手动编译驱动吗？", "en": "Do I need to compile drivers manually on Linux?", "ja": "Linuxで使用する場合、ドライバの手動コンパイルは必要ですか？", "ar": "هل أحتاج إلى تجميع التعريف يدوياً على لينكس؟", "es": "¿Necesito compilar el driver manualmente en Linux?", "pt": "Preciso compilar o driver manualmente no Linux?", "ru": "Нужно ли вручную компилировать драйвер в Linux?", "de": "Muss der Treiber unter Linux manuell kompiliert werden?", "fr": "Dois-je compiler le pilote manuellement sous Linux ?"},
                "a": {"zh-tw": "不需要。Linux Kernel 5.18+ 已原生內建 mt7921u 驅動，僅需確保安裝 linux-firmware 韌體套件。", "zh-cn": "不需要。Linux Kernel 5.18+ 已原生内置 mt7921u 驱动，仅需确保安装 linux-firmware 固件包。", "en": "No. Linux Kernel 5.18+ includes the native mt7921u driver. You only need the linux-firmware package installed.", "ja": "不要です。Linux Kernel 5.18以降にmt7921uドライバが標準搭載されており、linux-firmwareパッケージのみ必要です。", "ar": "لا. تتضمن نواة لينكس 5.18 وما فوق تعريف mt7921u مسبقاً، وتحتاج فقط إلى حزمة linux-firmware.", "es": "No. El kernel de Linux 5.18+ incluye el driver nativo mt7921u. Solo necesitas el paquete linux-firmware.", "pt": "Não. O kernel Linux 5.18+ já inclui o driver nativo mt7921u. Basta instalar o pacote linux-firmware.", "ru": "Нет. Ядро Linux 5.18+ уже содержит встроенный драйвер mt7921u. Требуется только пакет linux-firmware.", "de": "Nein. Linux-Kernel 5.18+ enthält den nativen mt7921u-Treiber. Es wird nur das linux-firmware-Paket benötigt.", "fr": "Non. Le noyau Linux 5.18+ inclut le pilote natif mt7921u. Seul le paquet linux-firmware est requis."}
            }
        ]
    },
    {
        "id": "02",
        "file": "02_article.md",
        "slug": "ros2-humble-robot-wifi-signal-optimization-awus036axml",
        "image": "/images/blog/02_ros2_robot_rf_coverage.jpg",
        "image_alt": "ROS 2 Humble Robot Wireless Optimization Blueprint",
        "date": "2026-08-18",
        "sku": "AWUS036AXML",
        "title": {
            "zh-tw": "ROS 2 Humble 機器人斷網與延遲排障：利用高功率外接網卡突破金屬屏蔽限制",
            "zh-cn": "ROS 2 Humble 机器人断网与延迟排障：利用高功率外接网卡突破金属屏蔽限制",
            "en": "ROS 2 Humble Robot Wi-Fi Disconnection & Latency Troubleshooting: Breaking Metal Shielding with High-Gain Adapters",
            "ja": "ROS 2 Humble ロボットのWi-Fi切断と遅延の解消法：高利得外部アダプターで金属シールドの壁を突破",
            "ar": "استكشاف أخطاء انقطاع وتأخر شبكة روبوتات ROS 2 Humble: اختراق الحجب المعدني بمحولات عالية الكسب",
            "es": "Solución a desconexiones y latencia en robots ROS 2 Humble: Superando el apantallamiento metálico con antenas de alta ganancia",
            "pt": "Solução de desconexões e latência em robôs ROS 2 Humble: Superando a blindagem metálica com adaptadores de alto ganho",
            "ru": "Устранение обрывов связи и задержек в роботах на ROS 2 Humble: преодоление экранирования корпусом с помощью мощных адаптеров",
            "de": "ROS 2 Humble Robotik-Netzwerkoptimierung: Beseitigung von Verbindungsabbrüchen und Latenzen durch externe High-Gain-Adapter",
            "fr": "Dépannage des déconnexions et de la latence Wi-Fi sur robots ROS 2 Humble : Surmonter le blindage métallique avec des adaptateurs haute puissance"
        },
        "description": {
            "zh-tw": "剖析移動機器人金屬與碳纖維外殼的法拉第籠效應，示範如何以 AWUS036AXML 外接天線改善 DDS 節點同步，並提供完整排障檢測流程。",
            "zh-cn": "剖析移动机器人金属与碳纤维外壳的法拉第笼效应，示范如何使用 AWUS036AXML 外接天线改善 DDS 节点同步，提供完整排障检测流程。",
            "en": "Comprehensive guide to eliminating Wi-Fi packet drops and DDS latency in ROS 2 mobile robots caused by Faraday cage metal chassis, utilizing the ALFA AWUS036AXML external antenna.",
            "ja": "自律移動ロボット（AMR）の金属・炭素繊維シャーシによるファラデーケージ効果を解説。AWUS036AXMLの外部アンテナでDDS通信遅延を劇的に改善する手順。",
            "ar": "دليل شامل للقضاء على فقدان الحزم وتأخر DDS في روبوتات ROS 2 الناتجة عن حجب الهياكل المعدنية باستخدام الهوائيات الخارجية لمحولات ALFA.",
            "es": "Guía práctica para eliminar pérdidas de paquetes y latencia DDS en robots móviles ROS 2 causadas por chasis metálicos, usando adaptadores ALFA de alta ganancia.",
            "pt": "Guia prático para eliminar quedas de pacotes e latência DDS em robôs móveis ROS 2 causadas por chassis metálicos, usando antenas externas ALFA.",
            "ru": "Руководство по устранению потерь пакетов и задержек DDS в мобильных роботах на ROS 2, вызванных клеткой Фарадея, с использованием внешних антенн ALFA AWUS036AXML.",
            "de": "Praxisleitfaden zur Beseitigung von Paketverlusten und DDS-Latenzen bei ROS 2 Robotern durch metallische Abschirmung mit externen High-Gain-WLAN-Adaptern.",
            "fr": "Guide pratique pour éliminer les pertes de paquets et la latence DDS sur les robots mobiles ROS 2 dues à la cage de Faraday, via les antennes externes ALFA."
        },
        "faq": [
            {
                "q": {"zh-tw": "碳纖維外殼是否也會屏蔽 Wi-Fi 訊號？", "zh-cn": "碳纤维外壳是否也会屏蔽 Wi-Fi 信号？", "en": "Does a carbon fiber chassis shield Wi-Fi signals?", "ja": "炭素繊維シャーシもWi-Fi信号をシールドしますか？", "ar": "هل تحجب هياكل ألياف الكربون إشارات Wi-Fi؟", "es": "¿El chasis de fibra de carbono también bloquea las señales Wi-Fi?", "pt": "O chassi de fibra de carbono também bloqueia sinais Wi-Fi?", "ru": "Экранирует ли корпус из углеродного волокна (карбона) сигналы Wi-Fi?", "de": "Schirmt ein Kohlefaser-Chassis Wi-Fi-Signale ab?", "fr": "Un châssis en fibre de carbone bloque-t-il les signaux Wi-Fi ?"},
                "a": {"zh-tw": "是的。導電碳纖維具有導體特性，會造成顯著的射頻信號衰減，建議將天線外置。", "zh-cn": "是的。导电碳纤维具有导体特性，会造成显著的射频信号衰减，建议将天线外置。", "en": "Yes. Conductive carbon fiber acts as a conductor, causing substantial RF attenuation. External antennas are strongly recommended.", "ja": "はい。導電性カーボンファイバーは導体として機能し、電波を大幅に減衰させるため、外部アンテナの配置を推奨します。", "ar": "نعم. تعمل ألياف الكربون الموصلة كحاجز كهرومغناطيسي، مما يتطلب استخدام هوائيات خارجية.", "es": "Sí. La fibra de carbono conductora actúa como conductor y atenúa la señal RF. Se recomienda usar antenas externas.", "pt": "Sim. A fibra de carbono condutiva atenua significativamente o sinal RF. Recomenda-se o uso de antenas externas.", "ru": "Да. Углеродное волокно проводит ток и сильно ослабляет радиосигналы, поэтому рекомендуется выносить антенны наружу.", "de": "Ja. Leitfähige Kohlefaser schwächt HF-Signale erheblich ab. Externe Antennen werden dringend empfohlen.", "fr": "Oui. La fibre de carbone conductrice atténue fortement les signaux RF. L'installation d'antennes externes est fortement recommandée."}
            }
        ]
    },
    {
        "id": "03",
        "file": "03_article.md",
        "slug": "openhd-vs-rubyfpv-vs-wfb-ng-fpv-wiring-topology",
        "image": "/images/blog/03_fpv_wiring_topology.jpg",
        "image_alt": "Open-Source Digital FPV Wiring Topology Blueprint",
        "date": "2026-08-18",
        "sku": "AWUS036ACH",
        "title": {
            "zh-tw": "DIY 數位圖傳天花板：OpenHD vs. RubyFPV vs. WFB-ng 底層協定解析與網卡供電防坑",
            "zh-cn": "DIY 数字图传天花板：OpenHD vs. RubyFPV vs. WFB-ng 底层协议解析与网卡供电防坑",
            "en": "Open-Source Digital FPV Deep Dive: OpenHD vs. RubyFPV vs. WFB-ng Architecture & High-Power Adapter Wiring",
            "ja": "オープンソース高画質デジタルFPV徹底比較：OpenHD vs RubyFPV vs WFB-ng プロトコル解析と外部電源配線ガイド",
            "ar": "أنظمة نقل الفيديو الرقمي مفتوحة المصدر (FPV): مقارنة بين OpenHD و RubyFPV و WFB-ng ودليل توصيل التغذية الكهربائية",
            "es": "Sistemas de Video Digital FPV de Código Abierto: OpenHD vs RubyFPV vs WFB-ng y Guía de Alimentación BEC",
            "pt": "Sistemas de Vídeo Digital FPV de Código Aberto: Comparativo OpenHD vs RubyFPV vs WFB-ng e Guia de Alimentação BEC",
            "ru": "Цифровое FPV с открытым исходным кодом: сравнение OpenHD, RubyFPV и WFB-ng и правильная схема питания мощных Wi-Fi адаптеров",
            "de": "Open-Source Digital-FPV im Detail: OpenHD vs. RubyFPV vs. WFB-ng Protokolle und BEC-Stromversorgung für High-Power-WLAN-Karten",
            "fr": "Transmission Vidéo Numérique FPV Open Source : Comparatif OpenHD vs RubyFPV vs WFB-ng et Câblage d'Alimentation BEC Dédiée"
        },
        "description": {
            "zh-tw": "解析開源數位圖傳監聽模式 Raw 封包廣播原理，對比 OpenHD、RubyFPV 與 WFB-ng 架構，揭密 AWUS036ACH 瞬間抽載與獨立 BEC 供電拓撲。",
            "zh-cn": "解析开源数字图传监听模式 Raw 数据包广播原理，对比 OpenHD、RubyFPV 与 WFB-ng 架构，详解 AWUS036ACH 瞬时抽载与独立 BEC 供电拓扑。",
            "en": "Master open-source digital FPV wireless broadcast fundamentals, compare OpenHD, RubyFPV, and WFB-ng stacks, and prevent in-flight brownouts with dedicated BEC wiring for AWUS036ACH.",
            "ja": "オープンソースデジタルFPVのRawパケット同報通信の仕組みを解説。OpenHD・RubyFPV・WFB-ngの比較と、AWUS036ACHの瞬間突入電流を防ぐ専用BEC配線トポロジー。",
            "ar": "شرح متعمق لتقنية البث اللاسلكي الخام في أنظمة FPV مفتوحة المصدر، ومقارنة بين البروتوكولات الثلاثة الكبرى، وتوصيل وحدة BEC لتفادي انقطاع التيار أثناء الطيران.",
            "es": "Domina la transmisión de paquetes Raw en FPV de código abierto, compara OpenHD, RubyFPV y WFB-ng, y evita reinicios en vuelo con alimentación BEC dedicada.",
            "pt": "Domine a transmissão de pacotes Raw em FPV open source, compare OpenHD, RubyFPV e WFB-ng, e evite reinicializações em voo com alimentação BEC dedicada.",
            "ru": "Разбор принципа широковещательной передачи Raw-пакетов в открытых FPV системах, сравнение OpenHD, RubyFPV и WFB-ng, и схема питания через BEC для адаптера AWUS036ACH.",
            "de": "Grundlagen der Raw-Paketübertragung für Open-Source FPV, Vergleich von OpenHD, RubyFPV und WFB-ng sowie sichere BEC-Stromversorgung gegen Spannungseinbrüche.",
            "fr": "Comprendre la diffusion de paquets Raw en FPV open source, comparer OpenHD, RubyFPV et WFB-ng, et sécuriser l'alimentation BEC pour l'adaptateur AWUS036ACH."
        },
        "faq": [
            {
                "q": {"zh-tw": "為什麼不能直接用樹莓派 USB 埠供電給 AWUS036ACH？", "zh-cn": "为什么不能直接用树莓派 USB 接口供电给 AWUS036ACH？", "en": "Why can't I power the AWUS036ACH directly from a Raspberry Pi USB port?", "ja": "なぜRaspberry PiのUSBポートからAWUS036ACHに直接給電してはいけないのですか？", "ar": "لماذا لا يمكن تغذية AWUS036ACH مباشرة من منفذ USB في راسبيري باي؟", "es": "¿Por qué no se debe alimentar el AWUS036ACH directamente desde el puerto USB de Raspberry Pi?", "pt": "Por que não devo alimentar o AWUS036ACH diretamente pela porta USB do Raspberry Pi?", "ru": "Почему нельзя питать AWUS036ACH напрямую от USB-порта Raspberry Pi?", "de": "Warum sollte der AWUS036ACH nicht direkt über den USB-Port des Raspberry Pi versorgt werden?", "fr": "Pourquoi ne pas alimenter l'AWUS036ACH directement via le port USB du Raspberry Pi ?"},
                "a": {"zh-tw": "高功率發射時瞬間電流抽載可能突破 1.5A–2A，會拉低樹莓派 5V 軌道電壓導致重開機或圖傳中斷，必須使用獨立 BEC (5V/3A) 供電。", "zh-cn": "高功率发射时瞬时电流抽载可能突破 1.5A–2A，会拉低树莓派 5V 电压导致重启或图传中断，必须使用独立 BEC (5V/3A) 供电。", "en": "Peak transmission bursts can draw 1.5A–2A, causing 5V rail voltage sag and triggering Pi reboots. A dedicated 5V/3A BEC is mandatory.", "ja": "高出力送信時の瞬間サージ電流が1.5A〜2Aに達し、Raspberry Piの5V電源を低下させて再起動を引き起こすため、独立したBEC（5V/3A）が必要です。", "ar": "تصل الذروة اللحظية للتيار أثناء البث إلى 1.5-2 أمبير، مما يسبب هبوط الجهد وإعادة تشغيل الجهاز، لذا يجب استخدام وحدة BEC مستقلة (5V/3A).", "es": "Los picos de transmisión pueden superar 1.5A-2A, provocando caídas de tensión en los 5V de la Raspberry Pi. Es obligatorio un BEC dedicado de 5V/3A.", "pt": "Picos de transmissão podem atingir 1.5A-2A, causando quedas de tensão no Raspberry Pi. É obrigatório o uso de um BEC dedicado de 5V/3A.", "ru": "Пиковый ток передачи может превышать 1.5–2 А, вызывая просадку шины 5 В и перезагрузку платы. Необходим отдельный BEC на 5 В / 3 А.", "de": "Spitzenströme beim Senden können 1,5A–2A erreichen und Spannungseinbrüche verursachen. Ein separates 5V/3A BEC ist zwingend erforderlich.", "fr": "Les pointes de courant peuvent dépasser 1,5A à 2A et provoquer des chutes de tension. Un BEC dédié 5V/3A est indispensable."}
            }
        ]
    },
    {
        "id": "04",
        "file": "04_article.md",
        "slug": "sdrlab-h4m-passive-reception-aviation-noaa",
        "image": "/images/blog/04_sdrlab_h4m_schematic.jpg",
        "image_alt": "SDRlab H4M Passive Signal Reception Schematic",
        "date": "2026-08-18",
        "sku": "SDRLAB-H4M",
        "title": {
            "zh-tw": "解鎖天空的頻譜：使用 SDRlab H4M 被動接收航空語音與 NOAA 衛星雲圖教學",
            "zh-cn": "解锁天空的频谱：使用 SDRlab H4M 被动接收航空语音与 NOAA 卫星云图教学",
            "en": "Unlocking Sky Frequencies: Passive Aviation Voice & NOAA Weather Satellite Decoding with SDRlab H4M",
            "ja": "大空の電波を傍受せよ：SDRlab H4Mによる航空管制AM音声とNOAA気象衛星画像受信ガイド",
            "ar": "استكشاف ترددات الفضاء: الاستقبال السلبي للمحادثات الجوية وفك تشفير صور أقمار NOAA باستخدام SDRlab H4M",
            "es": "Descifrando las frecuencias del cielo: Recepción pasiva de voz de aviación y satélites NOAA con SDRlab H4M",
            "pt": "Desvendando as frequências do céu: Recepção passiva de rádio de aviação e satélites meteorológicos NOAA com SDRlab H4M",
            "ru": "Радиомониторинг диапазона: пассивный прием авиадиапазона и декодирование спутников NOAA с помощью SDRlab H4M",
            "de": "Frequenzen des Himmels entschlüsseln: Passiver Flugfunkempfang und NOAA-Wettersatelliten-Dekodierung mit SDRlab H4M",
            "fr": "Décoder les fréquences du ciel : Réception passive des communications aériennes et satellites météo NOAA avec SDRlab H4M"
        },
        "description": {
            "zh-tw": "介紹軟體定義無線電（SDR）被動接收原理，實戰教學使用 SDRlab H4M 接收 118-137MHz 航空語音與 NOAA 137MHz 氣象衛星雲圖。",
            "zh-cn": "介绍软件定义无线电（SDR）被动接收原理，实战教学使用 SDRlab H4M 接收 118-137MHz 航空语音与 NOAA 137MHz 气象卫星云图。",
            "en": "Practical tutorial on passive radio reception using SDRlab H4M (R820T2 + RTL2832U), covering aviation AM voice tuning and NOAA satellite APT weather image decoding.",
            "ja": "ソフトウェア無線（SDR）のパッシブ受信の基礎から、SDRlab H4Mを使用した航空無線（118-137MHz）受信およびNOAA気象衛星APT画像のデコード実践手順。",
            "ar": "دليل عملي للاستقبال اللاسلكي السلبي باستخدام SDRlab H4M، يغطي التقاط المحادثات الصوتية للطيران وفك تشفير صور الطقس لأقمار NOAA الاصطناعية.",
            "es": "Tutorial práctico de radioescucha pasiva con SDRlab H4M: sintonización de radio aérea AM (118-137 MHz) y decodificación de imágenes meteorológicas NOAA.",
            "pt": "Tutorial prático de rádio escuta passiva com SDRlab H4M: sintonização de comunicações de aviação em AM e decodificação de imagens de satélite NOAA.",
            "ru": "Практическое руководство по пассивному приему радиосигналов с помощью SDRlab H4M: прослушивание авиадиапазона и прием снимков со спутников NOAA.",
            "de": "Praxisanleitung für passiven Funkempfang mit dem SDRlab H4M (R820T2 + RTL2832U): Flugfunk-AM-Empfang und NOAA-Wettersatellitenbild-Dekodierung.",
            "fr": "Tutoriel pratique de réception radio passive avec le SDRlab H4M : écoute des communications aéronautiques AM et décodage des images satellites NOAA."
        },
        "faq": [
            {
                "q": {"zh-tw": "SDRlab H4M 是否具有發射無線電信號的功能？", "zh-cn": "SDRlab H4M 是否具有发射无线电信号的功能？", "en": "Can the SDRlab H4M transmit radio signals?", "ja": "SDRlab H4Mは電波を送信する機能を備えていますか？", "ar": "هل يمتلك SDRlab H4M القدرة على إرسال إشارات الراديو؟", "es": "¿SDRlab H4M puede transmitir señales de radio?", "pt": "O SDRlab H4M pode transmitir sinais de rádio?", "ru": "Может ли SDRlab H4M передавать радиосигналы?", "de": "Kann das SDRlab H4M Funksignale senden?", "fr": "Le SDRlab H4M peut-il émettre des signaux radio ?"},
                "a": {"zh-tw": "不能。SDRlab H4M 為純被動接收架構（Receive-Only），無任何射頻功放與發射電路，符合各國無線電合法監聽規範。", "zh-cn": "不能。SDRlab H4M 为纯被动接收架构（Receive-Only），无任何射频功放与发射电路，符合各国无线电合法监听规范。", "en": "No. The SDRlab H4M is strictly receive-only with no transmit circuitry, ensuring compliance with local passive listening regulations.", "ja": "いいえ。SDRlab H4Mは完全な受信専用（Receive-Only）設計であり、電波法に適合した安全なパッシブ受信が可能です。", "ar": "لا. الجهاز مخصص للاستقبال فقط (Receive-Only) ولا يحتوي على دوائر إرسال، مما يجعله متوافقاً مع اللوائح القانونية.", "es": "No. SDRlab H4M es un dispositivo exclusivamente receptor (Receive-Only), sin circuitos de transmisión.", "pt": "Não. O SDRlab H4M é estritamente receptor (Receive-Only), sem circuitos de transmissão.", "ru": "Нет. SDRlab H4M работает только на прием (Receive-Only) и не имеет передающих цепей.", "de": "Nein. Das SDRlab H4M ist ein reines Empfangsgerät (Receive-Only) ohne Sendeschaltung.", "fr": "Non. Le SDRlab H4M est strictement conçu pour la réception passive (Receive-Only), sans émetteur."}
            }
        ]
    },
    {
        "id": "05",
        "file": "05_article.md",
        "slug": "kali-linux-rtl8812au-dkms-secure-boot-mok-setup",
        "image": "/images/blog/05_dkms_mok_flow_blueprint.jpg",
        "image_alt": "Linux Kernel DKMS and Secure Boot MOK Flowchart",
        "date": "2026-08-18",
        "sku": "AWUS036ACH",
        "title": {
            "zh-tw": "Kali Linux 核心更新後網卡罷工？RTL8812AU 驅動 DKMS 編譯失敗與 Secure Boot 排障",
            "zh-cn": "Kali Linux 内核更新后网卡罢工？RTL8812AU 驱动 DKMS 编译失败与 Secure Boot 排障",
            "en": "Wi-Fi Adapter Down After Kali Linux Kernel Upgrade? Fixing RTL8812AU DKMS Build Errors & Secure Boot MOK Signing",
            "ja": "Kali Linuxのカーネル更新でWi-Fiが停止？RTL8812AUドライバのDKMSビルドエラーとSecure Boot MOK署名完全解決",
            "ar": "توقف محول Wi-Fi بعد تحديث نواة Kali Linux؟ حل أخطاء بناء DKMS لتعريف RTL8812AU وتوقيع وحدات Secure Boot MOK",
            "es": "¿Adaptador Wi-Fi inactivo tras actualizar el kernel de Kali Linux? Solución de errores DKMS en RTL8812AU y firmas Secure Boot MOK",
            "pt": "Adaptador Wi-Fi parou após atualização de kernel no Kali Linux? Corrigindo erros DKMS no RTL8812AU e assinaturas Secure Boot MOK",
            "ru": "Wi-Fi адаптер перестал работать после обновления ядра Kali Linux? Устранение ошибок сборки DKMS для RTL8812AU и подпись модулей MOK Secure Boot",
            "de": "WLAN-Adapter nach Kali Linux Kernel-Upgrade ausgefallen? Behebung von RTL8812AU DKMS-Build-Fehlern und MOK-Signierung bei Secure Boot",
            "fr": "Adaptateur Wi-Fi inopérant après mise à jour du noyau Kali Linux ? Réparation de la compilation DKMS RTL8812AU et signature MOK Secure Boot"
        },
        "description": {
            "zh-tw": "詳解 Kali Linux 核心升級時 RTL8812AU 驅動失效成因，提供穩定社群驅動安裝步驟與 Secure Boot 開啟下的 MOK 模組簽署排障教學。",
            "zh-cn": "详解 Kali Linux 内核升级时 RTL8812AU 驱动失效原因，提供稳定社区驱动安装步骤与 Secure Boot 开启下的 MOK 模块签署排障教程。",
            "en": "Complete troubleshooting guide for Realtek RTL8812AU DKMS compilation failures on Kali Linux, including UEFI Secure Boot MOK module signing without disabling security features.",
            "ja": "Kali Linuxカーネル更新時にRTL8812AUドライバが無効化される原因と対策。最新ドライバのDKMSインストールと、Secure Bootを無効にしないMOK署名手順を解説。",
            "ar": "دليل استكشاف الأخطاء وإصلاحها لتعريف Realtek RTL8812AU عند فشل DKMS في Kali Linux، بما في ذلك توقيع المفاتيح المخصصة MOK مع بقاء Secure Boot مفعلًا.",
            "es": "Guía completa para solucionar fallos de compilación DKMS del driver RTL8812AU en Kali Linux y firmar módulos del kernel con MOK bajo Secure Boot.",
            "pt": "Guia definitivo para resolver falhas de compilação DKMS do driver RTL8812AU no Kali Linux e assinar módulos de kernel via MOK com Secure Boot ativado.",
            "ru": "Пошаговое руководство по исправлению ошибок компиляции DKMS для драйвера RTL8812AU в Kali Linux и настройке подписи модулей через MOK при включенном Secure Boot.",
            "de": "Umfassender Leitfaden zur Behebung von RTL8812AU DKMS-Kompilierungsfehlern in Kali Linux sowie Signierung von Kernel-Modulen via MOK bei aktivem Secure Boot.",
            "fr": "Guide complet pour résoudre les erreurs de compilation DKMS du pilote RTL8812AU sous Kali Linux et signer les modules du noyau via MOK avec Secure Boot activé."
        },
        "faq": [
            {
                "q": {"zh-tw": "遇到 Secure Boot 阻擋未簽署驅動時，應該關閉 Secure Boot 嗎？", "zh-cn": "遇到 Secure Boot 阻挡未签署驱动时，应该关闭 Secure Boot 吗？", "en": "Should I disable Secure Boot when unsigned drivers are blocked?", "ja": "未署名ドライバがブロックされた場合、Secure Bootを無効化すべきですか？", "ar": "هل يجب تعطيل Secure Boot عند حظر التعريفات غير الموقعة؟", "es": "¿Se debe desactivar Secure Boot cuando se bloquean controladores no firmados?", "pt": "Devo desativar o Secure Boot quando drivers não assinados são bloqueados?", "ru": "Следует ли отключать Secure Boot при блокировке неподписанных драйверов?", "de": "Sollte Secure Boot deaktiviert werden, wenn nicht signierte Treiber blockiert werden?", "fr": "Faut-il désactiver Secure Boot en cas de blocage de pilotes non signés ?"},
                "a": {"zh-tw": "不建議。安全作法是透過 mokutil 匯入自簽金鑰（MOK 機制），在維持系統安全防護的同時完成模組載入。", "zh-cn": "不建议。安全做法是通过 mokutil 导入自签密钥（MOK 机制），在维持系统安全防护的同时完成模块加载。", "en": "Not recommended. The secure approach is importing a machine owner key using mokutil to sign modules while keeping security intact.", "ja": "非推奨です。mokutilを用いて自署キーをMOKにインポートし、セキュリティ保護を維持したまま署名・読み込みを行うのが安全です。", "ar": "لا ينصح بذلك. الخيار الآمن هو توقيع الوحدة عبر آلية MOK واستيراد المفتاح باستخدام mokutil للحفاظ على أمان النظام.", "es": "No es recomendable. La práctica segura es registrar una clave MOK con mokutil para firmar los módulos manteniendo la seguridad activa.", "pt": "Não é recomendado. A prática segura é registrar uma chave MOK via mokutil para assinar os módulos mantendo a segurança.", "ru": "Не рекомендуется. Безопасный способ — использовать утилиту mokutil для подписи модуля через ключ MOK без отключения защиты.", "de": "Nicht empfohlen. Die sichere Methode ist das Signieren über MOK mit mokutil, um das System geschützt zu halten.", "fr": "Non recommandé. La méthode sécurisée consiste à importer une clé MOK via mokutil pour signer le module sans affaiblir la sécurité."}
            }
        ]
    },
    {
        "id": "06",
        "file": "06_article.md",
        "slug": "macos-acs-acr1252u-m1-web-nfc-apdu-guide",
        "image": "/images/blog/06_nfc_pcsc_stack_blueprint.jpg",
        "image_alt": "macOS ACS ACR1252U-M1 Web NFC and PC/SC Blueprint",
        "date": "2026-08-18",
        "sku": "ACR1252U-M1",
        "title": {
            "zh-tw": "macOS 免驅隨插即用：使用 ACS ACR1252U-M1 實戰 Web NFC API 與智慧卡 APDU 開發",
            "zh-cn": "macOS 免驱即插即用：使用 ACS ACR1252U-M1 实战 Web NFC API 与智能卡 APDU 开发",
            "en": "macOS Plug-and-Play NFC: Building Web NFC Apps & Smart Card APDU Workflows with ACS ACR1252U-M1",
            "ja": "macOSでドライバ不要の即時動作：ACS ACR1252U-M1によるWeb NFC APIとスマートカードAPDU開発実践ガイド",
            "ar": "تقنية NFC الفورية على macOS: تطوير تطبيقات Web NFC وأوامر APDU للبطاقات الذكية باستخدام ACS ACR1252U-M1",
            "es": "NFC Plug-and-Play en macOS: Desarrollo de Web NFC y comandos APDU de tarjetas inteligentes con ACS ACR1252U-M1",
            "pt": "NFC Plug-and-Play no macOS: Desenvolvimento de Web NFC e comandos APDU de Smart Cards com ACS ACR1252U-M1",
            "ru": "Plug-and-Play NFC в macOS: разработка приложений Web NFC и работа с APDU смарт-карт через ACS ACR1252U-M1",
            "de": "macOS Plug-and-Play NFC: Web NFC Entwicklung und Smartcard APDU-Workflows mit dem ACS ACR1252U-M1",
            "fr": "NFC Plug-and-Play sous macOS : Développement Web NFC et commandes APDU pour cartes à puce avec ACS ACR1252U-M1"
        },
        "description": {
            "zh-tw": "深入探討 ACS ACR1252U-M1 讀卡機在 Apple Silicon Mac 上的 CCID 原生支援，實戰 Web NFC NDEF 讀寫與底層 APDU 蜂鳴器控制指令。",
            "zh-cn": "深入探讨 ACS ACR1252U-M1 读卡器在 Apple Silicon Mac 上的 CCID 原生支持，实战 Web NFC NDEF 读写与底层 APDU 蜂鸣器控制指令。",
            "en": "Comprehensive development guide for ACS ACR1252U-M1 on Apple Silicon macOS, covering native CCID driverless integration, Web NFC API, and low-level APDU direct commands.",
            "ja": "Apple Silicon MacにおけるACS ACR1252U-M1の標準CCIDサポートを解説。Web NFC APIによるNDEFタグ読み書きやAPDUコマンドによるブザー・LED制御の実践。",
            "ar": "دليل برمجي شامل لقارئ ACS ACR1252U-M1 على أجهزة ماك، يغطي التوافق الأصلي مع معايير CCID وتطوير تطبيقات Web NFC وأوامر APDU المباشرة.",
            "es": "Guía práctica de desarrollo con ACS ACR1252U-M1 en macOS Apple Silicon: soporte nativo CCID, lectura/escritura Web NFC NDEF y comandos APDU directos.",
            "pt": "Guia prático de desenvolvimento com ACS ACR1252U-M1 no macOS Apple Silicon: suporte nativo CCID, leitura/gravação Web NFC NDEF e comandos APDU diretos.",
            "ru": "Руководство по разработке для считывателя ACS ACR1252U-M1 на macOS Apple Silicon: встроенный CCID, чтение/запись NDEF через Web NFC и команды APDU.",
            "de": "Umfassender Leitfaden für den ACS ACR1252U-M1 unter macOS Apple Silicon mit nativer CCID-Integration, Web NFC API und direkten APDU-Steuerbefehlen.",
            "fr": "Guide de développement avec le lecteur ACS ACR1252U-M1 sur macOS Apple Silicon : intégration CCID native, Web NFC et commandes directes APDU."
        },
        "faq": [
            {
                "q": {"zh-tw": "ACR1252U 在 macOS 下需要安裝額外的 Kernel Extension (kext) 嗎？", "zh-cn": "ACR1252U 在 macOS 下需要安装额外的 Kernel Extension (kext) 吗？", "en": "Does the ACR1252U require kernel extensions (kext) on macOS?", "ja": "ACR1252UはmacOSでカーネル拡張機能（kext）のインストールが必要ですか？", "ar": "هل يتطلب ACR1252U تثبيت امتدادات نواة (kext) على macOS؟", "es": "¿ACR1252U requiere extensiones del kernel (kext) en macOS?", "pt": "O ACR1252U requer extensões de kernel (kext) no macOS?", "ru": "Требуются ли расширения ядра (kext) для ACR1252U на macOS?", "de": "Benötigt das ACR1252U Kernel-Extensions (kext) unter macOS?", "fr": "L'ACR1252U nécessite-t-il des extensions de noyau (kext) sous macOS ?"},
                "a": {"zh-tw": "不需要。macOS 內建原生 CCID 類別驅動程式與 SmartCardServices，隨插即用。", "zh-cn": "不需要。macOS 内置原生 CCID 类驱动程序与 SmartCardServices，即插即用。", "en": "No. macOS includes native USB CCID class drivers and SmartCardServices for instant plug-and-play operation.", "ja": "不要です。macOSに標準のCCIDクラスドライバとSmartCardServicesが組み込まれており、完全プラグアンドプレイで動作します。", "ar": "لا. يتضمن نظام macOS تعريفات قياسية مدمجة لفئة CCID، ويعمل بشكل فوري دون برامج إضافية.", "es": "No. macOS incluye soporte nativo para la clase CCID y SmartCardServices, funcionando plug-and-play.", "pt": "Não. O macOS inclui drivers nativos da classe CCID e SmartCardServices com suporte plug-and-play.", "ru": "Нет. В macOS встроен стандартный драйвер класса CCID и служба SmartCardServices, все работает сразу.", "de": "Nein. macOS enthält native CCID-Klassentreiber und SmartCardServices für sofortigen Plug-and-Play-Betrieb.", "fr": "Non. macOS intègre nativement les pilotes de classe CCID et SmartCardServices pour une utilisation immédiate."}
            }
        ]
    },
    {
        "id": "07",
        "file": "07_article.md",
        "slug": "jetson-orin-nano-wifi-6e-6ghz-high-bandwidth-streaming",
        "image": "/images/blog/07_jetson_6ghz_streaming.jpg",
        "image_alt": "Jetson Orin Nano Wi-Fi 6E 6GHz Streaming Blueprint",
        "date": "2026-08-18",
        "sku": "AWUS036AXML",
        "title": {
            "zh-tw": "突破邊緣 AI 頻寬瓶頸：NVIDIA Jetson Orin Nano 安裝高功率網卡升級 6GHz 影音傳輸",
            "zh-cn": "突破边缘 AI 带宽瓶颈：NVIDIA Jetson Orin Nano 安装高功率网卡升级 6GHz 影音传输",
            "en": "Unlocking Edge AI Bandwidth: Upgrading NVIDIA Jetson Orin Nano with Wi-Fi 6E 6GHz Multi-Camera Streaming",
            "ja": "エッジAIの帯域幅ボトルネックを打破：NVIDIA Jetson Orin Nanoを高出力Wi-Fi 6Eで6GHz高速伝送にアップグレード",
            "ar": "كسر عنق زجاجة نطاق الذكاء الاصطناعي على الحافة: ترقية NVIDIA Jetson Orin Nano بمحولات Wi-Fi 6E لنقل الفيديو عبر 6 جيجاهرتز",
            "es": "Superando el cuello de botella en Edge AI: Actualizando NVIDIA Jetson Orin Nano con Wi-Fi 6E 6GHz para streaming multicámara",
            "pt": "Superando o gargalo de largura de banda em Edge AI: Atualizando NVIDIA Jetson Orin Nano com Wi-Fi 6E 6GHz para streaming multicâmera",
            "ru": "Преодоление ограничений пропускной способности в Edge AI: обновление NVIDIA Jetson Orin Nano с помощью Wi-Fi 6E 6 ГГц для многопотокового видео",
            "de": "Edge-KI-Bandbreitenengpässe überwinden: NVIDIA Jetson Orin Nano Upgrade mit Wi-Fi 6E 6GHz für hochauflösendes Video-Streaming",
            "fr": "Éliminer les goulets d'étranglement en IA Embarquée : Mise à niveau de la NVIDIA Jetson Orin Nano en Wi-Fi 6E 6 GHz pour le streaming vidéo"
        },
        "description": {
            "zh-tw": "探討在 JetPack 6 (Ubuntu 22.04 LTS) 下以 AWUS036AXML 啟用 6GHz 頻段，為多路 4K RTSP 串流提供超低延遲且免受干擾的無線通道。",
            "zh-cn": "探讨在 JetPack 6 (Ubuntu 22.04 LTS) 下使用 AWUS036AXML 启用 6GHz 频段，为多路 4K RTSP 串流提供超低延迟且免受干扰的无线通道。",
            "en": "Complete benchmark and setup guide for configuring the ALFA AWUS036AXML Wi-Fi 6E adapter on NVIDIA Jetson Orin Nano running JetPack 6 for multi-camera 4K RTSP streams.",
            "ja": "JetPack 6（Ubuntu 22.04 LTS）でAWUS036AXMLを使用し、6GHz帯を開放して複数4K RTSPカメラ映像を極小遅延かつ干渉なしで無線伝送する完全ガイド。",
            "ar": "دليل إعداد وتقييم أداء محول ALFA AWUS036AXML على منصة NVIDIA Jetson Orin Nano لدعم بث الفيديو 4K عبر تردد 6 جيجاهرتز بدون تداخل.",
            "es": "Guía completa de configuración del adaptador ALFA AWUS036AXML Wi-Fi 6E en NVIDIA Jetson Orin Nano con JetPack 6 para transmisión de múltiples cámaras 4K RTSP.",
            "pt": "Guia completo de configuração do adaptador ALFA AWUS036AXML Wi-Fi 6E no NVIDIA Jetson Orin Nano com JetPack 6 para transmissão de múltiplas câmeras 4K RTSP.",
            "ru": "Руководство по настройке адаптера ALFA AWUS036AXML Wi-Fi 6E на NVIDIA Jetson Orin Nano с JetPack 6 для передачи многоканального 4K RTSP видеопотока в диапазоне 6 ГГц.",
            "de": "Vollständiger Leitfaden zur Konfiguration des ALFA AWUS036AXML Wi-Fi 6E Adapters auf dem NVIDIA Jetson Orin Nano mit JetPack 6 für störungsfreies 4K-RTSP-Streaming.",
            "fr": "Guide complet de configuration de l'adaptateur Wi-Fi 6E ALFA AWUS036AXML sur NVIDIA Jetson Orin Nano sous JetPack 6 pour le flux multi-caméras 4K RTSP."
        },
        "faq": [
            {
                "q": {"zh-tw": "為什麼 6GHz 頻段對多路 4K 串流比 5GHz 更具優勢？", "zh-cn": "为什么 6GHz 频段对多路 4K 串流比 5GHz 更具优势？", "en": "Why is the 6GHz band superior to 5GHz for multi-camera 4K streaming?", "ja": "なぜ複数4Kストリーミングにおいて6GHz帯は5GHz帯よりも優れているのですか？", "ar": "لماذا يتفوق نطاق 6 جيجاهرتز على 5 جيجاهرتز في بث الفيديو المتعدد 4K؟", "es": "¿Por qué la banda de 6GHz es superior a la de 5GHz para streaming multicámara 4K?", "pt": "Por que a faixa de 6GHz é superior à de 5GHz para streaming multicâmera 4K?", "ru": "Почему диапазон 6 ГГц предпочтительнее 5 ГГц для многопотокового 4K видео?", "de": "Warum ist das 6GHz-Band dem 5GHz-Band für 4K-Mehrkanal-Streaming überlegen?", "fr": "Pourquoi la bande 6 GHz est-elle supérieure au 5 GHz pour le streaming 4K multi-flux ?"},
                "a": {"zh-tw": "6GHz 頻段擁有更寬廣且無舊式 Wi-Fi 設備競爭的乾淨頻寬，並具備 160MHz 大頻寬通道，顯著降低傳輸延遲與抖動。", "zh-cn": "6GHz 频段拥有更宽广且无旧式 Wi-Fi 设备竞争的干净带宽，具备 160MHz 超大频宽通道，显著降低传输延迟与抖动。", "en": "The 6GHz band provides pristine spectrum free from legacy Wi-Fi contention with 160MHz wide channels, eliminating transmission jitter.", "ja": "6GHz帯はレガシー機器の干渉がないクリーンな帯域であり、160MHzの超広帯域チャネルによりジッターと遅延を大幅に削減します。", "ar": "يوفر نطاق 6 جيجاهرتز طيفاً نقياً خالياً من تداخل الأجهزة القديمة مع قنوات عريضة 160 ميجاهرتز، مما يزيل التذبذب في البث.", "es": "La banda de 6GHz ofrece un espectro limpio sin interferencias de dispositivos antiguos y canales de 160MHz que reducen la latencia.", "pt": "A faixa de 6GHz oferece espectro limpo sem interferência de dispositivos antigos e canais de 160MHz que eliminam instabilidades.", "ru": "Диапазон 6 ГГц свободен от устаревших устройств и поддерживает широкие каналы 160 МГц, устраняя задержки и джиттер.", "de": "Das 6GHz-Band bietet ein störungsfreies Spektrum ohne Altgeräte und unterstützt 160MHz-Kanäle für minimale Latenz.", "fr": "La bande 6 GHz offre un spectre propre sans interférence d'anciens appareils avec des canaux de 160 MHz éliminant la latence."}
            }
        ]
    },
    {
        "id": "08",
        "file": "08_article.md",
        "slug": "vm-kali-linux-usb-passthrough-troubleshooting-guide",
        "image": "/images/blog/08_usb_passthrough_blueprint.jpg",
        "image_alt": "Virtual Machine USB Pass-Through Blueprint",
        "date": "2026-08-18",
        "sku": "AWUS036AXML",
        "title": {
            "zh-tw": "虛擬機 Kali Linux 抓不到外接網卡？VirtualBox/VMware USB 穿透與斷線診斷手冊",
            "zh-cn": "虚拟机 Kali Linux 抓不到外接网卡？VirtualBox/VMware USB 穿透与断线诊断手册",
            "en": "Wireless Adapter Not Detected in Kali VM? VirtualBox & VMware USB Pass-Through Troubleshooting Handbook",
            "ja": "仮想マシン上のKali LinuxでWi-Fi網カードが認識しない？VirtualBox・VMwareのUSBパススルーと切断対策ガイド",
            "ar": "المحول اللاسلكي لا يظهر في نظام Kali الافتراضي؟ دليل استكشاف أخطاء تمرير USB في VirtualBox و VMware",
            "es": "¿Tu máquina virtual Kali Linux no detecta la tarjeta Wi-Fi? Manual de diagnóstico de USB Pass-Through en VirtualBox y VMware",
            "pt": "A máquina virtual Kali Linux não detecta a placa Wi-Fi? Manual de diagnóstico de USB Pass-Through no VirtualBox e VMware",
            "ru": "Виртуальная машина Kali Linux не видит Wi-Fi адаптер? Руководство по настройке USB Pass-Through в VirtualBox и VMware",
            "de": "WLAN-Adapter in Kali Linux VM nicht erkannt? VirtualBox & VMware USB-Passthrough Fehlerbehebungshandbuch",
            "fr": "Adaptateur Wi-Fi non détecté dans la VM Kali Linux ? Manuel de dépannage du pass-through USB sous VirtualBox et VMware"
        },
        "description": {
            "zh-tw": "全面解析 VirtualBox 與 VMware 的 USB 穿透機制，解決 Kali 虛擬機無法辨識外接 USB 網卡、Extension Pack 設定及自動過濾器排障方案。",
            "zh-cn": "全面解析 VirtualBox 与 VMware 的 USB 穿透机制，解决 Kali 虚拟机无法识别外接 USB 网卡、Extension Pack 设置及自动过滤器排障方案。",
            "en": "Comprehensive troubleshooting guide for resolving USB wireless adapter detection failures in VirtualBox and VMware Kali Linux guest VMs, featuring USB 3.0 controller and filter setups.",
            "ja": "VirtualBoxおよびVMwareのUSBパススルー機構を徹底解説。Kali Linux仮想マシンでUSB無線LANカードが認識されない問題の診断とExtension Packの設定手順。",
            "ar": "دليل شامل لحل مشاكل عدم اكتشاف محولات Wi-Fi في أنظمة Kali Linux الافتراضية عبر VirtualBox و VMware وإعداد فلاتر USB وحزم التوسعة.",
            "es": "Guía paso a paso para resolver fallos de detección de adaptadores Wi-Fi USB en máquinas virtuales Kali Linux con VirtualBox y VMware, configurando controladores XHCI y filtros.",
            "pt": "Guia passo a passo para resolver falhas de detecção de adaptadores Wi-Fi USB em máquinas virtuais Kali Linux com VirtualBox e VMware, configurando controladores XHCI e filtros.",
            "ru": "Подробное руководство по устранению проблем с распознаванием USB Wi-Fi адаптеров в виртуальных машинах Kali Linux на VirtualBox и VMware с настройкой фильтров USB 3.0.",
            "de": "Schritt-für-Schritt-Anleitung zur Behebung von USB-WLAN-Erkennungsproblemen in Kali Linux VMs unter VirtualBox und VMware mit USB 3.0 Controller- und Filter-Konfiguration.",
            "fr": "Guide complet pour résoudre les problèmes de détection des adaptateurs Wi-Fi USB dans les machines virtuelles Kali Linux sous VirtualBox et VMware avec filtres XHCI."
        },
        "faq": [
            {
                "q": {"zh-tw": "為什麼虛擬機預設使用 NAT 或 Bridge 時無法使用網卡的監聽模式？", "zh-cn": "为什么虚拟机默认使用 NAT 或 Bridge 时无法使用网卡的监听模式？", "en": "Why can't I use monitor mode when the VM is set to NAT or Bridged mode?", "ja": "なぜ仮想マシンがNATやブリッジ接続の場合、モニターモードが使えないのですか？", "ar": "لماذا لا يمكن استخدام وضع المراقبة عندما يكون النظام الافتراضي في وضع NAT أو الجسر؟", "es": "¿Por qué no se puede usar el modo monitor en NAT o modo Puente?", "pt": "Por que não posso usar o modo monitor no modo NAT ou Bridge?", "ru": "Почему нельзя использовать режим мониторинга при подключении через NAT или Мост?", "de": "Warum kann der Monitor-Modus im NAT- oder Bridge-Modus der VM nicht genutzt werden?", "fr": "Pourquoi le mode moniteur ne fonctionne-t-il pas en mode NAT ou Pont ?"},
                "a": {"zh-tw": "NAT/Bridge 模式下虛擬機僅取得虛擬乙太網卡（eth0），只有透過 USB Pass-Through 實體穿透才能直接控制原生無線射頻介面。", "zh-cn": "NAT/Bridge 模式下虚拟机仅获得虚拟以太网卡（eth0），只有通过 USB Pass-Through 实体穿透才能直接控制原生无线射频接口。", "en": "NAT and Bridged modes expose a virtual Ethernet interface (eth0). Only raw USB pass-through gives the VM direct hardware control for monitor mode.", "ja": "NAT/ブリッジ接続では仮想Ethernetアダプタ（eth0）として認識されるため、USBパススルーでハードウェアを直接制御する必要があります。", "ar": "يقوم وضع NAT/Bridge بإنشاء واجهة إيثرنت افتراضية (eth0). يتطلب وضع المراقبة تحكماً مباشراً بالعتاد عبر تمرير USB الفعلي.", "es": "Los modos NAT/Puente solo emulan una tarjeta Ethernet virtual (eth0). Solo el USB Pass-Through permite control directo del hardware.", "pt": "Os modos NAT/Bridge emulam apenas uma placa Ethernet virtual (eth0). Somente o USB Pass-Through oferece controle direto do hardware.", "ru": "В режимах NAT/Bridge гостевая ОС видит только виртуальный Ethernet (eth0). Для режима монитора нужен прямой проброс USB.", "de": "NAT/Bridge stellt nur eine virtuelle Ethernet-Schnittstelle (eth0) bereit. Nur echtes USB-Passthrough erlaubt direkten Zugriff auf den WLAN-Chip.", "fr": "Les modes NAT/Pont n'émulent qu'une carte Ethernet virtuelle (eth0). Seul le pass-through USB direct permet le mode moniteur."}
            }
        ]
    }
]

def load_source_body(filename):
    path = os.path.join(SOURCE_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Remove top level H1 header if present since frontmatter provides title
    content = re.sub(r"^#\s+[^\n]+\n+", "", content)
    return content.strip()

print(f"Loaded configuration for {len(ARTICLES_CONFIG)} articles.")
