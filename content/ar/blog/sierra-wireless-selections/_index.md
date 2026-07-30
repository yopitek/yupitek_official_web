---
title: "دليل اختيار وحدات Sierra Wireless الخلوية: من LTE Cat 4 إلى 5G mmWave"
date: 2026-07-30
slug: "sierra-wireless-selections"
tags:
  - sierra-wireless
  - وحدة-خلوية
  - 4g-lte
  - 5g-nr
  - دليل-اختيار
  - em7455
  - em9190
  - m2-pcie
  - اتصالات-لاسلكية
categories:
  - دليل اختيار المنتجات
series:
  - sierra-wireless-selection
series_order: 1
description: "دليل مقارنة شامل من Yupitek لعشر وحدات خلوية من سلسلتي EM/MC من Sierra Wireless (Semtech). دليل اختيار من LTE Cat 4 إلى 5G mmWave."
author: "yupitek"
draft: false
faq:
  - question: "ما هي موديلات Sierra Wireless المتوفرة وما الفروق بينها؟"
    answer: "تقدم Sierra Wireless سلسلتين رئيسيتين (EM و MC) بعشر وحدات تغطي نطاق LTE Cat 4 / Cat 6 / Cat 12 وصولاً إلى 5G Sub-6 و mmWave. الفرق الأساسي يكمن في نوع التغليف: وحدات EM تأتي بتغليف M.2، بينما وحدات MC تأتي بتغليف mPCIe. الموديلات التي تشترك في نفس مجموعة الشرائح (مثل EM7455 و MC7455) متطابقة في الأداء ولا تختلف إلا في شكل الموصل."
  - question: "هل EM7455 و MC7455 هما نفس الشريحة؟"
    answer: "نعم. كلا الموديلين يستخدمان مجموعة شرائح Qualcomm MDM9230 بنفس معدلات الذروة للتحميل والرفع (300 / 50 Mbps) ويدعمان تجميع الموجات الحاملة 2×CA، مع تطابق كامل في المواصفات. الفرق الوحيد هو أن EM7455 بتغليف M.2 بينما MC7455 بتغليف mPCIe."
  - question: "هل يجب علي اختيار موديل mmWave (EM9191) لشبكات الجيل الخامس؟"
    answer: "ليس بالضرورة. معظم شبكات الجيل الخامس الحالية تعتمد على Sub-6. تقنية mmWave مخصصة أساساً للأسواق الأمريكية (مثل النطاقين n260/n261). للتطبيقات العامة، اختر EM9190 (5G Sub-6 الاقتصادي)؛ أما إذا كنت تحتاج mmWave للمواصفات الأمريكية فاختر EM9191."
  - question: "كيف أختار بين وحدات M.2 و mPCIe الخلوية؟"
    answer: "يعتمد الاختيار على نوع الفتحة في جهازك. أجهزة الكمبيوتر المحمولة واللوحات المدمجة الحديثة تستخدم فتحات M.2 B-Key، لذا اختر سلسلة EM. أما أجهزة التوجيه الصناعية القديمة وأجهزة التحكم الصناعي التي تحتوي على فتحات mPCIe، فاختر سلسلة MC. إذا كانت لوحتك تحتوي فقط على M.2 وتريد استخدام وحدة MC، فستحتاج إلى محول M.2 إلى mPCIe."
  - question: "أين يمكنني شراء Sierra Wireless في الشرق الأوسط؟"
    answer: "يمكنك شراء جميع وحدات Sierra Wireless الخلوية عبر Yupitek. يرجى زيارة صفحة المنتجات على موقع Yupitek للاستعلام عن الموديلات والأسعار، أو التواصل عبر البريد الإلكتروني: sales@yupitek.com"
---

أكبر تحدٍ عند شراء الوحدات الخلوية هو «جدول المواصفات المعقد وتعدد الموديلات وخطر شراء تغليف غير مناسب لا يتوافق مع جهازك». هذا المقال يشرح بالتفصيل عشر وحدات من Sierra Wireless، لمساعدتك في الاختيار الصحيح من LTE Cat 4 إلى 5G mmWave.

Sierra Wireless أصبحت الآن جزءاً من Semtech. هذا الدليل من إعداد Yupitek ويغطي عشر وحدات خلوية: EM7430، EM7455، EM7511، EM7565، EM9190، EM9191، MC7304، MC7350، MC7354، MC7455. وحدات سلسلة EM بتغليف M.2 وسلسلة MC بتغليف mPCIe.

البيانات التقنية في هذا المقال من إعداد Yupitek.

تغطي وحدات Sierra Wireless العشر نطاقاً من LTE Cat 4 / 6 / 12 إلى 5G Sub-6 و mmWave. الفرق بين سلسلتي EM و MC يقتصر على نوع التغليف: M.2 لسلسلة EM و mPCIe لسلسلة MC.

## جدول المواصفات الكامل للعشر وحدات

فيما يلي جدول المقارنة بالأرقام وفقاً لمواصفات Sierra Wireless الرسمية. يرجى ملاحظة أن معدلات الذروة للرفع لوحدتي EM9190 و EM9191 قد تختلف بين مصادر البيانات المختلفة، لذا نوصي بالتواصل معنا للحصول على أحدث المواصفات الرسمية قبل الشراء (انظر روابط الملحق في نهاية المقال).

| الطراز | المعيار الخلوي | مجموعة الشرائح | الذروة للتحميل/الرفع | تجميع الموجات الحاملة | 5G | mmWave | نوع التغليف | GNSS | ملاحظات |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](https://yupitek.com/ar/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | Cat 6 للمبتدئين (يرجى التأكد من توافق النطاقات مع مشغل الشبكة) |
| [EM7455](https://yupitek.com/ar/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | الأكثر شيوعاً في المجتمع وأكثرها توثيقاً بالدروس |
| [EM7511](https://yupitek.com/ar/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | رفع عالي مع Cat 12 |
| [EM7565](https://yupitek.com/ar/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | يدعم نطاقات CBRS/LAA (يرجى تأكيد نطاق الشهادات)، أوسع تغطية للنطاقات وأعلى رفع |
| [EM9190](https://yupitek.com/ar/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | تحميل 2.5 Gbps (الرفع يرجى التأكيد) | 8×CA | ✓ | — | M.2 | ✓ | مدخل 5G Sub-6 الاقتصادي |
| [EM9191](https://yupitek.com/ar/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | تحميل يصل إلى 4.5 Gbps (مع mmWave) / Sub-6 2.5 Gbps (الرفع يرجى التأكيد) | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | الرائد في 5G مع mmWave |
| [MC7304](https://yupitek.com/ar/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4 للمبتدئين (يقترب من نهاية الدورة) |
| [MC7350](https://yupitek.com/ar/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4، نطاقات أمريكا الشمالية |
| [MC7354](https://yupitek.com/ar/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4، النطاقات العالمية |
| [MC7455](https://yupitek.com/ar/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | إصدار mPCIe من EM7455 |

> ملاحظة: تشترك وحدتا EM9190 و EM9191 في نفس وثيقة المواصفات EM919x/EM7690. EM9190 هي وحدة 5G Sub-6 الاقتصادية بينما EM9191 هي الرائدة مع إضافة mmWave. وثيقة المواصفات الرسمية تتطلب تسجيل الدخول للتحميل. الأرقام المذكورة لمعدلات التحميل القصوى مأخوذة من مصادر متاحة للعموم. للحصول على أحدث الأرقام (خاصة معدلات الرفع لوحدتي EM9190/EM9191)، نوصي بالتواصل معنا قبل تقديم الطلب.

## الفرق بين سلسلتي EM (M.2) و MC (mPCIe) من حيث التغليف

هذا هو أول وأهم معيار في الاختيار، والأكثر تسبباً في أخطاء الشراء.

**سلسلة EM = تغليف M.2 B-Key**: حجم صغير (حوالي 30×42 مم)، مصممة لفتحات WWAN في أجهزة الكمبيوتر المحمولة واللوحات المدمجة الحديثة M.2، وهي الأكثر استخداماً في اللوحات الصناعية الحديثة وأجهزة الكمبيوتر المصغرة.

**سلسلة MC = تغليف Mini PCIe (mPCIe)**: تشبه بطاقات التوسعة التقليدية، مناسبة لفتحات mPCIe في أجهزة التوجيه الصناعية القديمة وأجهزة التحكم الصناعي. إذا كانت لوحتك تحتوي فقط على فتحات M.2، فستحتاج إلى محول (M.2 إلى mPCIe) لاستخدام وحدات سلسلة MC.

**المتطلبات المشتركة**: تتطلب كلتا السلسلتين قارئ بطاقة SIM خارجي وهوائيات. الموصلات غالباً من نوع U.FL، مع تكوين نموذجي 2×2 MIMO (هوائي رئيسي + هوائي تنوع) بالإضافة إلى هوائي GNSS للملاحة.

**نقطة مهمة تتكرر في الأسئلة**: EM7455 و MC7455 هما «نفس الشريحة باختلاف التغليف فقط» — كلاهما يستخدم Qualcomm MDM9230 بنفس المواصفات تماماً، والفرق الوحيد بين M.2 و mPCIe. لذا فالاختيار بينهما يعتمد كلياً على نوع الفتحة في جهازك.

## توصيات الاختيار حسب التطبيق

### أجهزة التوجيه اللاسلكية / CPE (OpenWrt / ROOter)

**التوصية:** [EM7455](https://yupitek.com/ar/products/sierra/em7455/) / [MC7455](https://yupitek.com/ar/products/sierra/mc7455/)
السبب: الأكثر دعماً في المجتمع، والأكثر توثيقاً في دروس ROOter وإعدادات QMI/MBIM، مما يجعل حل المشكلات أسهل عبر البحث.

### ترقية WWAN لأجهزة الكمبيوتر المحمولة

**التوصية:** [EM7430](https://yupitek.com/ar/products/sierra/em7430/) / [EM7455](https://yupitek.com/ar/products/sierra/em7455/)
السبب: كلاهما بتغليف M.2 مناسب لفتحات WWAN في أجهزة Dell و Lenovo التجارية. EM7455 معروف على نطاق واسع بتغطيته للنطاقات وسعره المنخفض في السوق المستعمل، مما يجعله الخيار الأمثل للترقية (يرجى التأكد من توافق النطاقات مع مشغل الشبكة قبل الطلب).

### أجهزة التوجيه الصناعية / البوابات (درجات حرارة واسعة، شهادات، إمداد طويل الأمد)

**التوصية:** سلسلة EM75 ([EM7511](https://yupitek.com/ar/products/sierra/em7511/)، [EM7565](https://yupitek.com/ar/products/sierra/em7565/))، [EM9190](https://yupitek.com/ar/products/sierra/em9190/)/[EM9191](https://yupitek.com/ar/products/sierra/em9191/)، [MC7455](https://yupitek.com/ar/products/sierra/mc7455/)
السبب: البيئات الصناعية تتطلب درجات حرارة واسعة (خيارات تصل إلى −40°C)، وشهادات اكتمال، وضمان الإمداد طويل الأمد. توفر وحدات Cat 12 و 5G معدلات رفع أعلى وسعة نطاق مستقبلية أكبر. يُرجى الرجوع إلى وثيقة المواصفات الرسمية للحصول على تفاصيل درجة الحرارة والشهادات، والتواصل معنا للحصول على أحدث إصدار قبل الاختيار النهائي.

### إنترنت الأشياء للمركبات / تتبع الأساطيل (تحديد المواقع GNSS)

**التوصية:** [EM7455](https://yupitek.com/ar/products/sierra/em7455/) / [EM7565](https://yupitek.com/ar/products/sierra/em7565/) / [EM9191](https://yupitek.com/ar/products/sierra/em9191/)
السبب: الثلاثة مزودة بنظام GNSS مدمج، مثالية لتتبع المركبات وإرسال بيانات الموقع. لتطبيقات المركبات التي تحتاج نطاقاً ترددياً عالياً من الجيل الخامس، اختر EM9191.

### شبكات 5G الخاصة / شبكات CBRS

**التوصية:** [EM9191](https://yupitek.com/ar/products/sierra/em9191/) (يدعم نطاقات CBRS)، [EM7565](https://yupitek.com/ar/products/sierra/em7565/) (يدعم نطاقات CBRS/LAA)
السبب: نطاقات CBRS (النطاق المشترك 3.5 GHz في الولايات المتحدة) و LAA من المتطلبات الشائعة للشبكات الخاصة. تدعم وحدتا EM9191 و EM7565 هذه النطاقات. ومع ذلك، يتطلب تطبيق الشبكات الخاصة مطابقة دقيقة للنطاقات والشهادات وفقاً للوائح المحلية وبيئة الاتصالات، لذا نوصي بالتواصل معنا لإجراء تقييم تقني كامل.

### أنظمة المراقبة بالفيديو / اللوحات الرقمية (نقل عالي النطاق)

**التوصية:** [EM9190](https://yupitek.com/ar/products/sierra/em9190/) / [EM9191](https://yupitek.com/ar/products/sierra/em9191/)
السبب: النطاق الترددي العالي للجيل الخامس (تحميل يصل إلى 2.5 Gbps على Sub-6، وحتى 4.5 Gbps مع mmWave) مناسب لنقل الفيديو متعدد القنوات في الوقت الفعلي وبث اللوحات الرقمية بدقة 4K.

### صيانة الأجهزة القديمة / التزويد طويل الأمد (Cat 4)

**التوصية:** [MC7304](https://yupitek.com/ar/products/sierra/mc7304/) / [MC7350](https://yupitek.com/ar/products/sierra/mc7350/) / [MC7354](https://yupitek.com/ar/products/sierra/mc7354/)
السبب: الخيار الأول لقطع غيار صيانة الأجهزة القديمة من Cat 4 بتغليف mPCIe. ولكن تجدر الإشارة بصراحة إلى أن سلسلة MC73xx تقترب من نهاية دورة حياتها (EOL). للتزويد طويل الأمد، نوصي بالانتقال إلى [EM7455](https://yupitek.com/ar/products/sierra/em7455/) أو [EM7565](https://yupitek.com/ar/products/sierra/em7565/) لضمان استمرارية الإمداد.

## اتصل بنا للشراء

ما زلت غير متأكد من اختيارك؟ يمكنك شراء جميع وحدات Sierra Wireless من سلسلتي EM/MC المذكورة في هذا المقال عبر Yupitek، بالإضافة إلى الهوائيات المناسبة ومحولات SIM ولوحات التقييم. نقدم خدمة تأكيد المواصفات ومقارنة النطاقات وعروض الأسعار الكمية والدعم الفني للتكامل.

## الأسئلة الشائعة FAQ

**س1: ما هي موديلات Sierra Wireless المتوفرة وما الفروق بينها؟**
تقدم Sierra Wireless سلسلتين رئيسيتين (EM و MC) بعشر وحدات تغطي نطاق LTE Cat 4 / Cat 6 / Cat 12 وصولاً إلى 5G Sub-6 و mmWave. الفرق الأساسي يكمن في نوع التغليف: وحدات EM تأتي بتغليف M.2، بينما وحدات MC تأتي بتغليف mPCIe. الموديلات التي تشترك في نفس مجموعة الشرائح (مثل EM7455 و MC7455) متطابقة في الأداء ولا تختلف إلا في شكل الموصل.

**س2: هل EM7455 و MC7455 هما نفس الشريحة؟**
نعم. كلا الموديلين يستخدمان مجموعة شرائح Qualcomm MDM9230 بنفس معدلات الذروة للتحميل والرفع (300 / 50 Mbps) ويدعمان تجميع الموجات الحاملة 2×CA، مع تطابق كامل في المواصفات. الفرق الوحيد هو أن EM7455 بتغليف M.2 بينما MC7455 بتغليف mPCIe.

**س3: هل يجب علي اختيار موديل mmWave (EM9191) لشبكات الجيل الخامس؟**
ليس بالضرورة. معظم شبكات الجيل الخامس الحالية تعتمد على Sub-6. تقنية mmWave مخصصة أساساً للأسواق الأمريكية (مثل النطاقين n260/n261). للتطبيقات العامة، اختر EM9190 (5G Sub-6 الاقتصادي)؛ أما إذا كنت تحتاج mmWave للمواصفات الأمريكية فاختر EM9191.

**س4: كيف أختار بين وحدات M.2 و mPCIe الخلوية؟**
يعتمد الاختيار على نوع الفتحة في جهازك. أجهزة الكمبيوتر المحمولة واللوحات المدمجة الحديثة تستخدم فتحات M.2 B-Key، لذا اختر سلسلة EM. أما أجهزة التوجيه الصناعية القديمة وأجهزة التحكم الصناعي التي تحتوي على فتحات mPCIe، فاختر سلسلة MC. إذا كانت لوحتك تحتوي فقط على M.2 وتريد استخدام وحدة MC، فستحتاج إلى محول M.2 إلى mPCIe.

**س5: أين يمكنني شراء Sierra Wireless في الشرق الأوسط؟**
يمكنك شراء جميع وحدات Sierra Wireless الخلوية عبر Yupitek. يرجى زيارة صفحة المنتجات على موقع Yupitek للاستعلام عن الموديلات والأسعار، أو التواصل عبر البريد الإلكتروني: sales@yupitek.com

## الملحق: روابط وثائق المواصفات الرسمية للعشر موديلات

الروابط أدناه من قاعدة الموارد التقنية الرسمية لـ Sierra Wireless (source.sierrawireless.com). **بعض المستندات تتطلب تسجيل الدخول لتحميل PDF**. الأرقام المذكورة في هذا المقال مستخلصة من البيانات المتاحة للعموم. إذا كنت بحاجة إلى التأكيد الرسمي لأي رقم (خاصة معدلات الرفع لوحدتي EM9190/EM9191)، نوصي بالتواصل معنا للحصول على المستندات الرسمية:

- **EM7430**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7430_product_technical_specification/
- **EM7455**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7455_product_technical_specification/
- **EM7511**: https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7511_product_technical_specification/
- **EM7565**: https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7565_product_technical_specification/
- **EM9190 / EM9191**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_em919x-7690_product_technical_specification/
- **MC7304**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7304_product_technical_specification_and_customer_design_guidelines/
- **MC7350**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_mc7455_product_technical_specification/
