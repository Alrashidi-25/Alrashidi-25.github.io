#!/usr/bin/env python3
"""Generate the Arabic page (ar/index.html) from the English page (index.html).

The English page is the source of truth. Every string below must still exist in it,
so if the English copy changes, this script stops and names the string to update.

    python3 tools/build_ar.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "ar" / "index.html"

MONTHS = {"Jan": "يناير", "Feb": "فبراير", "Mar": "مارس", "Apr": "أبريل", "May": "مايو", "Jun": "يونيو",
          "Jul": "يوليو", "Aug": "أغسطس", "Sep": "سبتمبر", "Oct": "أكتوبر", "Nov": "نوفمبر", "Dec": "ديسمبر"}

T = [
    # ---------------------------------------------------------------- head
    ('<html lang="en">', '<html lang="ar" dir="rtl">'),
    ('<title>Abdulrahman Alrashidi — Systems &amp; Business Analyst | Power BI, Project Management</title>',
     '<title>عبدالرحمن الرشيدي — محلل نظم وأعمال | Power BI وإدارة المشاريع</title>'),
    ('content="Abdulrahman Alrashidi — Computer Information Systems senior at King Faisal University. Aspiring Systems &amp; Business Analyst working across requirements, data analysis, Power BI, project management and cybersecurity."',
     'content="عبدالرحمن الرشيدي — طالب في السنة الأخيرة بتخصص نظم المعلومات الحاسوبية بجامعة الملك فيصل، يسعى للعمل محللاً للنظم والأعمال في مجالات المتطلبات وتحليل البيانات وPower BI وإدارة المشاريع والأمن السيبراني."'),
    ('<link rel="canonical" href="https://alrashidi-25.github.io/">', '<link rel="canonical" href="https://alrashidi-25.github.io/ar/">'),
    ('<meta property="og:url" content="https://alrashidi-25.github.io/">', '<meta property="og:url" content="https://alrashidi-25.github.io/ar/">\n<meta property="og:locale" content="ar_SA">'),
    ('<meta property="og:site_name" content="Abdulrahman Alrashidi">', '<meta property="og:site_name" content="عبدالرحمن الرشيدي">'),
    ('<meta property="og:title" content="Abdulrahman Alrashidi — Systems &amp; Business Analyst">', '<meta property="og:title" content="عبدالرحمن الرشيدي — محلل نظم وأعمال">'),
    ('<meta property="og:description" content="I translate business needs into clear systems, data, and decisions.">',
     '<meta property="og:description" content="أحوّل احتياجات الأعمال إلى أنظمة وبيانات وقرارات واضحة.">'),
    ('family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500',
     'family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500'),
    ('<link rel="stylesheet" href="style.css">', '<link rel="stylesheet" href="../style.css">\n<link rel="stylesheet" href="../ar.css">'),
    ('<a href="#main" class="skip-link">Skip to content</a>', '<a href="#main" class="skip-link">تخطَّ إلى المحتوى</a>'),

    # ---------------------------------------------------------------- nav
    ('<span class="logo-text">Abdulrahman Alrashidi</span>', '<span class="logo-text">عبدالرحمن الرشيدي</span>'),
    ('>About</a>', '>نبذة</a>'), ('>Focus</a>', '>التركيز</a>'), ('>Projects</a>', '>المشاريع</a>'),
    ('>Skills</a>', '>المهارات</a>'), ('>Experience</a>', '>الخبرات</a>'),
    ('>Certifications</a>', '>الشهادات</a>'), ('>Contact</a>', '>تواصل</a>'),
    ('<a href="ar/" class="lang-switch" hreflang="ar" lang="ar" title="النسخة العربية">عربي</a>',
     '<a href="../" class="lang-switch" hreflang="en" lang="en" title="English version">EN</a>'),
    ('</svg> Download CV</a>', '</svg> السيرة الذاتية</a>'),
    ('aria-label="Open menu"', 'aria-label="فتح القائمة"'),

    # ---------------------------------------------------------------- hero
    ('<span class="dot"></span> CIS Senior · King Faisal University</p>', '<span class="dot"></span> نظم المعلومات الحاسوبية · جامعة الملك فيصل</p>'),
    ('<h1 class="hero-name" data-reveal>Abdulrahman Alrashidi</h1>', '<h1 class="hero-name" data-reveal>عبدالرحمن الرشيدي</h1>'),
    ('<p class="hero-name-ar" data-reveal lang="ar">عبدالرحمن مناور الرشيدي</p>', '<p class="hero-name-ar" data-reveal lang="en" dir="ltr">Abdulrahman Alrashidi</p>'),
    ('Turning business needs into <span class="hl">clear systems, data&nbsp;&amp; decisions</span>.',
     'أحوّل احتياجات الأعمال إلى <span class="hl">أنظمة وبيانات</span> وقرارات واضحة.'),
    ('Aspiring Systems &amp; Business Analyst &nbsp;·&nbsp; Power BI &nbsp;·&nbsp; Project Management &nbsp;·&nbsp; Cybersecurity',
     'أسعى للعمل محللاً للنظم والأعمال &nbsp;·&nbsp; Power BI &nbsp;·&nbsp; إدارة المشاريع &nbsp;·&nbsp; الأمن السيبراني'),
    ('View Projects <svg', 'استعرض المشاريع <svg'),
    ('</svg> Profile Snapshot</span>', '</svg> لمحة سريعة</span>'),
    ('</svg> Open to internships</span>', '</svg> متاح للتدريب</span>'),
    ('<span class="kpi-label">Certifications</span>', '<span class="kpi-label">الشهادات</span>'),
    ('<span class="kpi-trend">Verified</span>', '<span class="kpi-trend">موثّقة</span>'),
    ('<span class="kpi-label">Job Simulations</span>', '<span class="kpi-label">محاكاة وظيفية</span>'),
    ('<span class="kpi-label">Focus Areas</span>', '<span class="kpi-label">مجالات التركيز</span>'),
    ('<span class="kpi-trend">BA · Data · PM · Sec</span>', '<span class="kpi-trend">أعمال · بيانات · مشاريع · أمن</span>'),
    ('<span class="snap-cat">Analysis</span><span class="snap-tags">Requirements · Process Mapping · Feasibility</span>',
     '<span class="snap-cat">التحليل</span><span class="snap-tags">المتطلبات · رسم العمليات · الجدوى</span>'),
    ('<span class="snap-cat">Data &amp; BI</span>', '<span class="snap-cat">البيانات</span>'),
    ('<span class="snap-cat">Delivery</span><span class="snap-tags">KPIs · Dashboards · Stakeholders</span>',
     '<span class="snap-cat">التنفيذ</span><span class="snap-tags">مؤشرات الأداء · لوحات البيانات · أصحاب المصلحة</span>'),
    ('<span class="snap-cat">Security</span><span class="snap-tags">Incident Response · Reporting</span>',
     '<span class="snap-cat">الأمن</span><span class="snap-tags">الاستجابة للحوادث · التقارير</span>'),

    # ---------------------------------------------------------------- about
    ('role="img" aria-label="Abdulrahman Alrashidi"', 'role="img" aria-label="عبدالرحمن الرشيدي"'),
    ('<span class="mono-sub">عبدالرحمن الرشيدي</span>', '<span class="mono-sub" lang="en" dir="ltr">Abdulrahman Alrashidi</span>'),
    ('</svg> Al-Ahsa, Saudi Arabia</div>', '</svg> الأحساء، المملكة العربية السعودية</div>'),
    ('<p class="section-eyebrow" data-reveal>About Me</p>', '<p class="section-eyebrow" data-reveal>نبذة عني</p>'),
    ('I sit where the business question meets the technical answer.', 'أقف حيث يلتقي سؤال الأعمال بالإجابة التقنية.'),
    ("I'm a senior Computer Information Systems student at King Faisal University in Al-Ahsa, building toward a career as a Systems &amp; Business Analyst — the person who turns a vague business need into requirements, data, and a solution a team can actually build.",
     'أنا طالب في السنة الأخيرة بتخصص نظم المعلومات الحاسوبية في جامعة الملك فيصل بالأحساء، وأبني مساري المهني نحو تحليل النظم والأعمال — الدور الذي يحوّل احتياجاً غير واضح إلى متطلبات وبيانات وحلٍّ يستطيع الفريق تنفيذه فعلاً.'),
    ("CIS gave me the foundation on both sides: systems analysis and design, databases, programming, and how business processes actually run inside an organization. On top of that I've focused on the analyst toolkit — gathering requirements, mapping processes, running feasibility studies, and writing the executive summary that helps a decision-maker choose.",
     'منحني التخصص أساساً في الجانبين: تحليل النظم وتصميمها، وقواعد البيانات، والبرمجة، وكيف تسير العمليات فعلياً داخل المنظمة. وبنيت فوق ذلك أدوات المحلل: جمع المتطلبات، ورسم العمليات، وإعداد دراسات الجدوى، وكتابة الملخص التنفيذي الذي يساعد صاحب القرار على الاختيار.'),
    ("I work with data because decisions need evidence. I use Power BI, Excel and SQL to clean data, build dashboards, and track the KPIs that tell you whether a project is actually working. Alongside that, I've trained in project management and in cybersecurity incident response — because a good solution also has to be delivered on time and be safe to run.",
     'أعمل مع البيانات لأن القرار يحتاج إلى دليل. أستخدم Power BI وExcel وSQL لتنظيف البيانات وبناء لوحات المعلومات وتتبّع مؤشرات الأداء التي تكشف هل ينجح المشروع فعلاً. وإلى جانب ذلك تدربت على إدارة المشاريع والاستجابة لحوادث الأمن السيبراني — لأن الحل الجيد يجب أن يُسلَّم في وقته وأن يعمل بأمان.'),
    ('Most of this was built through hands-on virtual job simulations with BCG, STC, Microsoft, Accenture, Siemens and McKinsey.org — real tasks, real deliverables, not just coursework.',
     'واكتسبت معظم ذلك عبر برامج محاكاة وظيفية تطبيقية مع BCG وstc وMicrosoft وAccenture وSiemens وMcKinsey.org — مهام حقيقية ومخرجات حقيقية، لا مجرد مقررات دراسية.'),
    ('<span>CIS Senior — King Faisal University</span>', '<span>نظم المعلومات الحاسوبية — جامعة الملك فيصل</span>'),
    ('<span>Systems &amp; Business Analysis</span>', '<span>تحليل النظم والأعمال</span>'),
    ('<span>Power BI &amp; Data Analysis</span>', '<span>Power BI وتحليل البيانات</span>'),
    ('<span>Project Management</span>', '<span>إدارة المشاريع</span>'),
    ('<span>Cybersecurity Incident Response</span>', '<span>الاستجابة لحوادث الأمن السيبراني</span>'),
    ('<span>Azure Cloud &amp; Applied AI</span>', '<span>سحابة Azure والذكاء الاصطناعي التطبيقي</span>'),

    # ---------------------------------------------------------------- focus
    ('<p class="section-eyebrow">My Focus</p>', '<p class="section-eyebrow">مجالات تركيزي</p>'),
    ('Understand → Analyze → Measure → Deliver', 'أفهم ← أحلّل ← أقيس ← أسلّم'),
    ('Four connected areas that make up how I approach a problem — from the first stakeholder conversation to a dashboard someone actually uses.',
     'أربعة مجالات مترابطة تشكّل طريقتي في التعامل مع أي مشكلة — من أول حديث مع أصحاب المصلحة إلى لوحة بيانات يستخدمها أحد فعلاً.'),
    ('<h3>Systems &amp; Requirements</h3>', '<h3>النظم والمتطلبات</h3>'),
    ('Gathering requirements, mapping current vs. future processes, and defining what the system actually has to do.',
     'جمع المتطلبات، ورسم العمليات الحالية مقابل المستقبلية، وتحديد ما يجب أن يقوم به النظام فعلاً.'),
    ('<h3>Business Analysis</h3>', '<h3>تحليل الأعمال</h3>'),
    ('Market study, feasibility, budget planning, and the executive summary that turns analysis into a decision.',
     'دراسة السوق والجدوى، وتخطيط الميزانية، والملخص التنفيذي الذي يحوّل التحليل إلى قرار.'),
    ('<h3>Data &amp; Business Intelligence</h3>', '<h3>البيانات وذكاء الأعمال</h3>'),
    ('Cleaning data, building Power BI dashboards, and choosing the KPIs that make performance visible.',
     'تنظيف البيانات، وبناء لوحات Power BI، واختيار مؤشرات الأداء التي تجعل الأداء واضحاً.'),
    ('<h3>Delivery &amp; Security</h3>', '<h3>التنفيذ والأمن</h3>'),
    ('Managing scope and stakeholders through delivery, with an eye on risk, incidents, and secure operation.',
     'إدارة النطاق وأصحاب المصلحة حتى التسليم، مع متابعة المخاطر والحوادث والتشغيل الآمن.'),

    # ---------------------------------------------------------------- projects
    ('<p class="section-eyebrow">Selected Work</p>', '<p class="section-eyebrow">أعمال مختارة</p>'),
    ('Projects that solve a real problem', 'مشاريع تحل مشكلة حقيقية'),
    ('The problem, the approach, and what was delivered.', 'المشكلة، والمنهجية، وما تم تسليمه.'),
    ('<strong>Problem:</strong>', '<strong>المشكلة:</strong>'),
    ('<strong>Approach:</strong>', '<strong>المنهجية:</strong>'),
    ('<strong>Solution:</strong>', '<strong>الحل:</strong>'),
    ('Open Live Demo <svg', 'جرّب النسخة الحية <svg'),
    ('</svg> Source Code</a>', '</svg> الكود المصدري</a>'),
    # Jisr
    ('alt="Jisr business analysis case study"', 'alt="دراسة حالة تحليل الأعمال لمشروع جسر"'),
    ('<span class="tag tag-primary">Business Analysis · SQL · Power BI</span>', '<span class="tag tag-primary">تحليل الأعمال · SQL · Power BI</span>'),
    ('<h3>جسر · Jisr — Co-op Placement System, End to End</h3>', '<h3>جسر — نظام التدريب التعاوني من البداية إلى النهاية</h3>'),
    ('One real problem taken from requirements, to a tested database, to a KPI dashboard.',
     'مشكلة حقيقية واحدة: من المتطلبات، إلى قاعدة بيانات مختبرة، إلى لوحة مؤشرات أداء.'),
    ("Co-op training placements run on paper forms, email and spreadsheets. Students can't see where their request is, staff type nomination letters one by one in the same few weeks every term, and nobody has reliable data on placements or partners.",
     'تُدار ترشيحات التدريب التعاوني بنماذج ورقية وبريد إلكتروني وجداول بيانات. لا يعرف الطالب أين وصل طلبه، ويكتب الموظفون خطابات الترشيح واحداً تلو الآخر في الأسابيع القليلة نفسها كل فصل، ولا توجد بيانات موثوقة عن الترشيحات أو جهات التدريب.'),
    ('Analyzed the process the way an analyst would, specified the system that fixes it, built and tested the database behind it, and designed the dashboard that measures whether the fix works.',
     'حللت العملية كما يفعل المحلل، وحددت مواصفات النظام الذي يعالجها، ثم بنيت قاعدة البيانات خلفه واختبرتها، وصممت لوحة المؤشرات التي تقيس هل نجح الحل.'),
    ('<strong>Headline finding</strong> <span>(synthetic data)</span> — requests arriving in the last three weeks before term met the review target only <b>46–49%</b> of the time, against <b>84–90%</b> for earlier ones: a timing problem, not a staffing one.',
     '<strong>أبرز نتيجة</strong> <span>(بيانات افتراضية)</span> — الطلبات التي وصلت في آخر ثلاثة أسابيع قبل بداية الفصل حققت هدف المراجعة في <b dir="ltr">46–49%</b> فقط من الحالات، مقابل <b dir="ltr">84–90%</b> للطلبات الأبكر: المشكلة في التوقيت لا في عدد الموظفين.'),
    ('<h4>Business analysis case study</h4>', '<h4>دراسة حالة لتحليل الأعمال</h4>'),
    ('Current and future process maps, 7 pain points traced to root causes, 28 requirements with MoSCoW priorities, use cases, user stories, KPIs, a weighted options analysis and a 17-page BRD.',
     'خرائط للعملية الحالية والمستقبلية، و7 مشكلات مربوطة بأسبابها الجذرية، و28 متطلباً بأولويات MoSCoW، وحالات استخدام، وقصص مستخدم، ومؤشرات أداء، وتحليل خيارات موزون، ووثيقة متطلبات أعمال (BRD) من 17 صفحة.'),
    ('Read case study <svg', 'اقرأ دراسة الحالة <svg'),
    ('<h4>Database &amp; SQL analysis</h4>', '<h4>قاعدة البيانات وتحليل SQL</h4>'),
    ('An 18-table SQLite schema that enforces the approval workflow with triggers, 563 synthetic requests, 16 business questions answered in SQL, and 11 tests proving the rules hold.',
     'مخطط SQLite من 18 جدولاً يفرض مسار الموافقات عبر Triggers، و563 طلباً افتراضياً، و16 سؤال أعمال مُجاب عنها بـSQL، و11 اختباراً تثبت أن القواعد تعمل.'),
    ('</svg> Source &amp; results</a>', '</svg> الكود والنتائج</a>'),
    ('<h4>Power BI dashboard</h4>', '<h4>لوحة Power BI</h4>'),
    ('Star schema with personal data removed, 27 DAX measures, a custom report theme, and four built pages — every card verified against independently computed values.',
     'نموذج Star Schema خالٍ من البيانات الشخصية، و27 مقياس DAX، وقالب ألوان مخصص، وأربع صفحات مبنية بالكامل — كل رقم فيها مُتحقَّق منه مقابل قيم محسوبة بشكل مستقل.'),
    ('View dashboard <svg', 'شاهد اللوحة <svg'),
    ('</svg> Model &amp; measures</a>', '</svg> النموذج والمقاييس</a>'),
    ('<span class="chip">Process mapping</span><span class="chip">Requirements</span><span class="chip">Use cases</span>',
     '<span class="chip">رسم العمليات</span><span class="chip">المتطلبات</span><span class="chip">حالات الاستخدام</span>'),
    # Ruaa
    ('<span class="tag tag-primary">Data Analysis · BI</span>', '<span class="tag tag-primary">تحليل البيانات · BI</span>'),
    ('<h3>رؤى · Ruaa — In-Browser Data Analysis</h3>', '<h3>رؤى — تحليل البيانات داخل المتصفح</h3>'),
    ('Drop in a CSV and get back what an analyst would actually tell you — in Arabic or English.',
     'ارفع ملف CSV واحصل على ما سيقوله لك محلل البيانات فعلاً — بالعربية أو الإنجليزية.'),
    ('Most CSV tools stop at drawing a chart. The hard part of analysis isn\'t the chart — it\'s noticing that 40% of a column is missing, that the mean is lying because of a long tail, or that two "distinct" categories are the same value spelled two ways.',
     'معظم أدوات CSV تتوقف عند رسم مخطط. لكن الجزء الصعب في التحليل ليس المخطط — بل أن تلاحظ أن 40% من عمودٍ ما مفقودة، أو أن المتوسط مضلِّل بسبب قيم متطرفة، أو أن فئتين «مختلفتين» هما القيمة نفسها مكتوبة بطريقتين.'),
    ('A client-side analysis engine that reads the file, infers what every column really is, profiles it statistically, then runs a rule set that writes its findings out in plain language — ranked critical to good. Thirteen rule families cover missing data, duplicates, Pareto concentration, Tukey outliers, skew, correlation and trend.',
     'محرك تحليل يعمل بالكامل في المتصفح: يقرأ الملف، ويستنتج نوع كل عمود فعلياً، ويحلله إحصائياً، ثم يطبّق مجموعة قواعد تكتب النتائج بلغة واضحة — مرتبة من الحرج إلى الجيد. ثلاث عشرة مجموعة قواعد تغطي البيانات المفقودة، والتكرار، وتركّز باريتو، والقيم الشاذة بطريقة Tukey، والالتواء، والارتباط، والاتجاه.'),
    ('RFC-4180 parser with delimiter sniffing; handles Arabic-Indic digits and regional date order',
     'قارئ CSV متوافق مع RFC-4180 يكتشف الفاصل تلقائياً، ويتعامل مع الأرقام الهندية وترتيب التاريخ الإقليمي'),
    ('Type inference across number, currency, percent, date, boolean, category and identifier',
     'استنتاج نوع البيانات: رقم، عملة، نسبة، تاريخ، منطقي، فئة، معرّف'),
    ('Insight engine: outlier fences, Pareto, skew, Pearson correlation, trend detection',
     'محرك استنتاجات: حدود القيم الشاذة، باريتو، الالتواء، ارتباط بيرسون، اكتشاف الاتجاه'),
    ('Five chart types hand-drawn in SVG — no charting library', 'خمسة أنواع مخططات مرسومة يدوياً بـSVG — دون أي مكتبة رسوم'),
    ('Full Arabic/English with RTL, and Unicode bidi isolation so numbers read correctly',
     'دعم كامل للعربية والإنجليزية مع اتجاه RTL، وعزل اتجاه النص (Unicode bidi) لتظهر الأرقام بشكل صحيح'),
    ('<span class="chip">Statistics</span>', '<span class="chip">الإحصاء</span>'),
    ('<span class="chip">Zero deps</span>', '<span class="chip">بلا مكتبات خارجية</span>'),
    # Masar
    ('<span class="tag tag-primary">Product · Data</span>', '<span class="tag tag-primary">منتج · بيانات</span>'),
    ('<h3>مسار · Masar — Academic GPA Planner</h3>', '<h3>مسار — مخطط المعدل الأكاديمي</h3>'),
    ('A free Arabic-first tool that helps Saudi university students calculate, understand, and plan their GPA.',
     'أداة عربية مجانية تساعد طلاب الجامعات السعودية على حساب معدلهم وفهمه والتخطيط له.'),
    ('Students guess at their GPA, lose track across semesters, and have no way to answer the one question that matters — "what do I need this term to reach the GPA I want?"',
     'يخمّن الطلاب معدلاتهم، ويفقدون تتبّعها بين الفصول، ولا يجدون طريقة للإجابة عن السؤال الأهم: «ما المعدل الذي أحتاجه هذا الفصل لأصل إلى المعدل الذي أريده؟»'),
    ('A fully client-side web app that calculates semester and cumulative GPA on both the 5.0 and 4.0 Saudi scales, then works backwards: set a target GPA and it tells you the exact average you need. Adds a what-if simulator, per-semester tracking saved in the browser, grade distribution analytics, and CSV export — no account, no server, nothing leaves the device.',
     'تطبيق ويب يعمل بالكامل في المتصفح، يحسب المعدل الفصلي والتراكمي على مقياسي 5 و4 المعتمدين في الجامعات السعودية، ثم يعمل بالعكس: حدّد المعدل المستهدف وسيخبرك بالمعدل الدقيق الذي تحتاجه. ويضيف محاكي «ماذا لو»، وتتبّعاً لكل فصل يُحفظ في المتصفح، وتحليلاً لتوزيع الدرجات، وتصديراً إلى CSV — بلا حساب ولا خادم، ولا تغادر أي بيانات جهازك.'),
    ('Dual-scale GPA engine (5.0 / 4.0) with official Saudi grade bands', 'محرك حساب على مقياسين (5.0 / 4.0) بفئات التقديرات المعتمدة في السعودية'),
    ('Target-GPA solver — computes the required term average to hit a goal', 'حاسبة المعدل المستهدف — تحسب المعدل الفصلي المطلوب للوصول إلى الهدف'),
    ('Multi-semester tracking with automatic cumulative rollup', 'تتبّع عدة فصول مع حساب تراكمي تلقائي'),
    ('Grade distribution + honors-standing analytics, CSV export', 'تحليل توزيع الدرجات ومرتبة الشرف، وتصدير CSV'),
    ('Arabic RTL interface, fully offline, zero dependencies', 'واجهة عربية من اليمين إلى اليسار، تعمل دون اتصال، وبلا مكتبات خارجية'),
    # Graduation project
    ('<span class="tag tag-accent">Graduation Project</span>', '<span class="tag tag-accent">مشروع التخرج</span>'),
    ('</svg> In Progress</span>', '</svg> قيد التنفيذ</span>'),
    ('<h3>Senior Capstone Project</h3>', '<h3>مشروع التخرج</h3>'),
    ('Final-year CIS project — King Faisal University.', 'مشروع السنة الأخيرة في نظم المعلومات الحاسوبية — جامعة الملك فيصل.'),
    ('Details and documentation coming soon — the project covers system analysis, database design and\n            implementation as part of the Computer Information Systems program.',
     'التفاصيل والتوثيق قريباً — يشمل المشروع تحليل النظام وتصميم قاعدة البيانات وتنفيذها ضمن برنامج نظم المعلومات الحاسوبية.'),
    ('<span class="chip">System Analysis</span><span class="chip">Database Design</span><span class="chip">Documentation</span>',
     '<span class="chip">تحليل النظم</span><span class="chip">تصميم قواعد البيانات</span><span class="chip">التوثيق</span>'),

    # ---------------------------------------------------------------- skills
    ('<p class="section-eyebrow">Skills</p>', '<p class="section-eyebrow">المهارات</p>'),
    ('The analyst toolkit', 'أدوات المحلل'),
    ('Built through the CIS program and hands-on job simulations with global firms.',
     'اكتسبتها من خلال تخصص نظم المعلومات وبرامج محاكاة وظيفية تطبيقية مع شركات عالمية.'),
    ('<h3>Systems &amp; Business Analysis</h3>', '<h3>تحليل النظم والأعمال</h3>'),
    ('<li>Requirements gathering &amp; documentation</li>', '<li>جمع المتطلبات وتوثيقها</li>'),
    ('<li>Process mapping (as-is / to-be)</li>', '<li>رسم العمليات (الوضع الحالي / المستهدف)</li>'),
    ('<li>Feasibility &amp; market studies</li>', '<li>دراسات الجدوى والسوق</li>'),
    ('<li>Use cases, ERD &amp; system design</li>', '<li>حالات الاستخدام وERD وتصميم النظم</li>'),
    ('<li>Stakeholder mapping</li>', '<li>تحليل أصحاب المصلحة</li>'),
    ('<li>Executive summaries</li>', '<li>الملخصات التنفيذية</li>'),
    ('<li>Power BI dashboards</li>', '<li>لوحات Power BI</li>'),
    ('<li>Excel — modelling &amp; budgeting</li>', '<li>Excel — النمذجة والميزانيات</li>'),
    ('<li>Data cleaning &amp; preparation</li>', '<li>تنظيف البيانات وتجهيزها</li>'),
    ('<li>Data visualization &amp; storytelling</li>', '<li>تصوير البيانات وعرضها بأسلوب قصصي</li>'),
    ('<li>User-behaviour analysis</li>', '<li>تحليل سلوك المستخدمين</li>'),
    ('<li>KPI design &amp; tracking</li>', '<li>تصميم مؤشرات الأداء وتتبّعها</li>'),
    ('<h3>Project Management</h3>', '<h3>إدارة المشاريع</h3>'),
    ('<li>Project scoping &amp; planning</li>', '<li>تحديد نطاق المشروع وتخطيطه</li>'),
    ('<li>KPI development</li>', '<li>تطوير مؤشرات الأداء</li>'),
    ('<li>Project dashboards &amp; reporting</li>', '<li>لوحات متابعة المشاريع والتقارير</li>'),
    ('<li>Stakeholder communication</li>', '<li>التواصل مع أصحاب المصلحة</li>'),
    ('<li>Community &amp; non-profit initiatives</li>', '<li>المبادرات المجتمعية وغير الربحية</li>'),
    ('<li>Risk &amp; progress tracking</li>', '<li>تتبّع المخاطر والتقدم</li>'),
    ('<h3>Cybersecurity</h3>', '<h3>الأمن السيبراني</h3>'),
    ('<li>Incident response analysis</li>', '<li>تحليل الاستجابة للحوادث</li>'),
    ('<li>Security incident reporting</li>', '<li>كتابة تقارير الحوادث الأمنية</li>'),
    ('<li>Threat handling procedures</li>', '<li>إجراءات التعامل مع التهديدات</li>'),
    ('<li>Ethical hacking &amp; CTF fundamentals</li>', '<li>أساسيات الاختراق الأخلاقي وCTF</li>'),
    ('<li>Mobile &amp; application security basics</li>', '<li>أساسيات أمن التطبيقات والجوال</li>'),
    ('<li>Security awareness fundamentals</li>', '<li>أساسيات التوعية الأمنية</li>'),
    ('<h3>Programming &amp; Databases</h3>', '<h3>البرمجة وقواعد البيانات</h3>'),
    ('<li>SQL &amp; relational databases</li>', '<li>SQL وقواعد البيانات العلائقية</li>'),
    ('<li>Python fundamentals</li>', '<li>أساسيات Python</li>'),
    ('<li>HTML, CSS &amp; JavaScript</li>', '<li>HTML وCSS وJavaScript</li>'),
    ('<li>Database design &amp; normalization</li>', '<li>تصميم قواعد البيانات والتطبيع</li>'),
    ('<li>Git &amp; GitHub version control</li>', '<li>إدارة الإصدارات بـGit وGitHub</li>'),
    ('<li>Vue.js frontend basics</li>', '<li>أساسيات الواجهات الأمامية بـVue.js</li>'),
    ('<h3>Cloud &amp; AI</h3>', '<h3>السحابة والذكاء الاصطناعي</h3>'),
    ('<li>Microsoft Azure fundamentals</li>', '<li>أساسيات Microsoft Azure</li>'),
    ('<li>Cloud solution building blocks</li>', '<li>مكونات بناء الحلول السحابية</li>'),
    ('<li>Machine learning concepts</li>', '<li>مفاهيم تعلّم الآلة</li>'),
    ('<li>Applied AI &amp; data science basics</li>', '<li>أساسيات الذكاء الاصطناعي التطبيقي وعلم البيانات</li>'),

    # ---------------------------------------------------------------- experience
    ('<p class="section-eyebrow">Experience</p>', '<p class="section-eyebrow">الخبرات</p>'),
    ('Virtual job simulations with global firms', 'برامج محاكاة وظيفية مع شركات عالمية'),
    ('Structured programs where I completed the same practical tasks the role does day to day — delivered through Misk Foundation and Forage.',
     'برامج منظمة أنجزت فيها المهام العملية نفسها التي يؤديها صاحب الوظيفة يومياً — مقدَّمة عبر مؤسسة مسك ومنصة Forage.'),
    ('<h3>Business Analysis — Boston Consulting Group (BCG)</h3>', '<h3>تحليل الأعمال — Boston Consulting Group (BCG)</h3>'),
    ('Misk Foundation × BCG · Virtual job experience', 'مؤسسة مسك × BCG · تجربة وظيفية افتراضية'),
    ('Conducted market study and feasibility analysis', 'أجريت دراسة سوق وتحليل جدوى'),
    ('Built a budget plan in Excel', 'بنيت خطة ميزانية في Excel'),
    ('Prepared an executive summary for decision-makers', 'أعددت ملخصاً تنفيذياً لصنّاع القرار'),
    ('<h3>Project Manager — Siemens</h3>', '<h3>مدير مشروع — Siemens</h3>'),
    ('Forage · Job simulation', 'Forage · محاكاة وظيفية'),
    ('Developed key performance indicators (KPIs)', 'طوّرت مؤشرات أداء رئيسية (KPIs)'),
    ('Managed project dashboards', 'أدرت لوحات متابعة المشروع'),
    ('<h3>Cybersecurity Incident Response — stc</h3>', '<h3>الاستجابة لحوادث الأمن السيبراني — stc</h3>'),
    ('Misk Foundation × Saudi Telecom Company · Virtual job experience', 'مؤسسة مسك × شركة الاتصالات السعودية · تجربة وظيفية افتراضية'),
    ('Produced cybersecurity incident reports', 'أعددت تقارير حوادث الأمن السيبراني'),
    ('Handled and triaged security threats', 'تعاملت مع التهديدات الأمنية وصنّفت أولوياتها'),
    ('Applied the appropriate incident response procedures', 'طبّقت إجراءات الاستجابة المناسبة للحوادث'),
    ('<h3>Data Analysis — stc</h3>', '<h3>تحليل البيانات — stc</h3>'),
    ('Studied and analyzed user behaviour', 'درست سلوك المستخدمين وحللته'),
    ('Built a predictive model for user behaviour', 'بنيت نموذجاً تنبؤياً لسلوك المستخدمين'),
    ('Applied machine learning algorithms and presented the data', 'طبّقت خوارزميات تعلّم الآلة وعرضت البيانات'),
    ('<h3>Cloud Computing — Microsoft Azure</h3>', '<h3>الحوسبة السحابية — Microsoft Azure</h3>'),
    ('Misk Foundation × Microsoft · Virtual job experience', 'مؤسسة مسك × Microsoft · تجربة وظيفية افتراضية'),
    ('Cloud computing fundamentals', 'أساسيات الحوسبة السحابية'),
    ('Built solutions on Azure and integrated services', 'بنيت حلولاً على Azure وربطت الخدمات ببعضها'),
    ('<h3>Project &amp; Community Initiative Management</h3>', '<h3>إدارة المشاريع والمبادرات المجتمعية</h3>'),
    ('Misk Foundation · Non-profit sector · Virtual job experience', 'مؤسسة مسك · القطاع غير الربحي · تجربة وظيفية افتراضية'),
    ('Managed projects and community initiatives', 'أدرت مشاريع ومبادرات مجتمعية'),
    ('Analyzed performance indicators', 'حللت مؤشرات الأداء'),
    ('Built a stakeholder map', 'بنيت خريطة أصحاب المصلحة'),

    # ---------------------------------------------------------------- certifications
    ('<p class="section-eyebrow">Certifications</p>', '<p class="section-eyebrow">الشهادات</p>'),
    ('Twelve certificates', 'اثنتا عشرة شهادة'),
    ('From SDAIA, Cisco Networking Academy, McKinsey.org, Siemens, BCG, stc, Microsoft, Accenture and Misk Foundation. Click any certificate to view it.',
     'من سدايا، وأكاديمية Cisco للشبكات، وMcKinsey.org، وSiemens، وBCG، وstc، وMicrosoft، وAccenture، ومؤسسة مسك. اضغط على أي شهادة لعرضها.'),
    ('</svg> View</span>', '</svg> عرض</span>'),
    ('<span class="cert-issuer">BCG · Misk</span>', '<span class="cert-issuer">BCG · مسك</span>'),
    ('<span class="cert-issuer">stc · Misk</span>', '<span class="cert-issuer">stc · مسك</span>'),
    ('<span class="cert-issuer">Microsoft · Misk</span>', '<span class="cert-issuer">Microsoft · مسك</span>'),
    ('<span class="cert-issuer">Accenture · Misk</span>', '<span class="cert-issuer">Accenture · مسك</span>'),
    ('<span class="cert-issuer">Misk Foundation</span>', '<span class="cert-issuer">مؤسسة مسك</span>'),
    ('<span class="cert-issuer">Cisco Networking Academy</span>', '<span class="cert-issuer">أكاديمية Cisco للشبكات</span>'),
    ('<span class="cert-issuer">SDAIA · Saudi Data &amp; AI Authority</span>', '<span class="cert-issuer">سدايا · الهيئة السعودية للبيانات والذكاء الاصطناعي</span>'),
    ('<h3>Forward Program</h3>', '<h3>برنامج Forward</h3>'),
    ('<h3>Project Manager Job Simulation</h3>', '<h3>محاكاة وظيفية: مدير مشروع</h3>'),
    ('Problem-solving, communication, adaptability and digital toolkit.', 'حل المشكلات، والتواصل، والتكيّف، والأدوات الرقمية.'),
    ('Developing KPIs and managing project dashboards.', 'تطوير مؤشرات الأداء وإدارة لوحات متابعة المشاريع.'),
    ('Market study, feasibility, Excel budgeting and executive summaries.', 'دراسة السوق، والجدوى، والميزانية في Excel، والملخصات التنفيذية.'),
    ('User behaviour analysis, ML algorithms and data presentation.', 'تحليل سلوك المستخدمين، وخوارزميات تعلّم الآلة، وعرض البيانات.'),
    ('Foundations of data science, the data lifecycle and analytical thinking.', 'أسس علم البيانات، ودورة حياة البيانات، والتفكير التحليلي.'),
    ('Incident reporting, threat handling and response procedures.', 'تقارير الحوادث، والتعامل مع التهديدات، وإجراءات الاستجابة.'),
    ('Machine learning, data analysis and innovative solutions on Azure.', 'تعلّم الآلة، وتحليل البيانات، وحلول مبتكرة على Azure.'),
    ('Advanced AI concepts and their applications — part of the One Million Saudis in AI initiative.',
     'مفاهيم متقدمة في الذكاء الاصطناعي وتطبيقاتها — ضمن مبادرة مليون سعودي في الذكاء الاصطناعي.'),
    ('Core AI principles — part of the One Million Saudis in AI initiative.', 'المبادئ الأساسية للذكاء الاصطناعي — ضمن مبادرة مليون سعودي في الذكاء الاصطناعي.'),
    ('Cloud fundamentals, building Azure solutions and integration.', 'أساسيات السحابة، وبناء الحلول على Azure، وتكامل الخدمات.'),
    ('Project management, KPI analysis and stakeholder mapping.', 'إدارة المشاريع، وتحليل مؤشرات الأداء، وخريطة أصحاب المصلحة.'),
    ('User journey mapping, platform analysis and research reporting.', 'رسم رحلة المستخدم، وتحليل المنصات، وكتابة التقارير البحثية.'),

    # ---------------------------------------------------------------- workshops
    ('<p class="section-eyebrow">Workshops &amp; Campus Activities</p>', '<p class="section-eyebrow">ورش العمل والأنشطة الجامعية</p>'),
    ('Hands-on training at King Faisal University', 'تدريب تطبيقي في جامعة الملك فيصل'),
    ("Bootcamps and workshops run by the university's Cybersecurity and AI clubs, plus campus involvement. Click any card to view the certificate.",
     'معسكرات وورش عمل قدّمها ناديا الأمن السيبراني والذكاء الاصطناعي في الجامعة، إلى جانب مشاركات جامعية. اضغط على أي بطاقة لعرض الشهادة.'),
    ('<span class="ws-tag">Cybersecurity</span>', '<span class="ws-tag">الأمن السيبراني</span>'),
    ('<span class="ws-tag ws-tag-blue">Development</span>', '<span class="ws-tag ws-tag-blue">تطوير</span>'),
    ('<span class="ws-tag ws-tag-green">Volunteering</span>', '<span class="ws-tag ws-tag-green">تطوع</span>'),
    ('<strong>Capture The Flag Bootcamp</strong>', '<strong>معسكر Capture The Flag</strong>'),
    ('<strong>Practical Ethical Hacking</strong>', '<strong>الاختراق الأخلاقي التطبيقي</strong>'),
    ('<strong>Mobile &amp; Application Security</strong>', '<strong>أمن التطبيقات والجوال</strong>'),
    ('<strong>Frontend Web Development with Vue.js</strong>', '<strong>تطوير الواجهات الأمامية بـVue.js</strong>'),
    ('<strong>Using Git &amp; GitHub</strong>', '<strong>استخدام Git وGitHub</strong>'),
    ('<strong>Interactive Web Interfaces with Framer</strong>', '<strong>واجهات ويب تفاعلية بـFramer</strong>'),
    ('<strong>Nabbih 2025 Cybersecurity Awareness Exhibition</strong>', '<strong>معرض نبّه 2025 للتوعية بالأمن السيبراني</strong>'),
    ('<span class="ws-org">KFU Cybersecurity Club × CyberXBytes</span>', '<span class="ws-org">نادي الأمن السيبراني بجامعة الملك فيصل × CyberXBytes</span>'),
    ('<span class="ws-org">KFU Cybersecurity Club</span>', '<span class="ws-org">نادي الأمن السيبراني بجامعة الملك فيصل</span>'),
    ('<span class="ws-org">KFU Peer Tutoring Initiative</span>', '<span class="ws-org">مبادرة التعليم بالأقران بجامعة الملك فيصل</span>'),
    ('<span class="ws-org">KFU AI Club × Student Advisory Council</span>', '<span class="ws-org">نادي الذكاء الاصطناعي × المجلس الاستشاري الطلابي</span>'),
    ('<span class="ws-org">KFU AI Club</span>', '<span class="ws-org">نادي الذكاء الاصطناعي بجامعة الملك فيصل</span>'),
    ('<span class="ws-org">KFU College of Computer Sciences &amp; IT</span>', '<span class="ws-org">كلية علوم الحاسب وتقنية المعلومات بجامعة الملك فيصل</span>'),
    ('<span class="ws-meta">Jan 2025 · 6 hours</span>', '<span class="ws-meta">يناير 2025 · 6 ساعات</span>'),
    ('<span class="ws-meta">May 2025 · 3 hours</span>', '<span class="ws-meta">مايو 2025 · 3 ساعات</span>'),
    ('<span class="ws-meta">Feb 2025 · 2 hours</span>', '<span class="ws-meta">فبراير 2025 · ساعتان</span>'),
    ('<span class="ws-meta">Feb 2025 · 2 days</span>', '<span class="ws-meta">فبراير 2025 · يومان</span>'),
    ('<span class="ws-meta">Workshop</span>', '<span class="ws-meta">ورشة عمل</span>'),
    ('<span class="ws-meta">Feb 2025</span>', '<span class="ws-meta">فبراير 2025</span>'),
    ('<span class="ws-meta">Oct 2025 · Contributor</span>', '<span class="ws-meta">أكتوبر 2025 · مشارك</span>'),

    # ---------------------------------------------------------------- education
    ('<p class="section-eyebrow">Education</p>', '<p class="section-eyebrow">التعليم</p>'),
    ('Academic background', 'المؤهل الأكاديمي'),
    ('<h3>Bachelor of Computer Information Systems</h3>', '<h3>بكالوريوس نظم المعلومات الحاسوبية</h3>'),
    ('King Faisal University — Al-Ahsa, Saudi Arabia', 'جامعة الملك فيصل — الأحساء، المملكة العربية السعودية'),
    ('Senior year. Coursework across systems analysis &amp; design, database management, programming, networks, information security and business process management.',
     'السنة الأخيرة. مقررات في تحليل النظم وتصميمها، وإدارة قواعد البيانات، والبرمجة، والشبكات، وأمن المعلومات، وإدارة عمليات الأعمال.'),
    ('<span class="chip">Systems Analysis &amp; Design</span><span class="chip">Database Management</span><span class="chip">Programming</span><span class="chip">Information Security</span><span class="chip">Business Processes</span>',
     '<span class="chip">تحليل النظم وتصميمها</span><span class="chip">إدارة قواعد البيانات</span><span class="chip">البرمجة</span><span class="chip">أمن المعلومات</span><span class="chip">عمليات الأعمال</span>'),

    # ---------------------------------------------------------------- contact & footer
    ('<p class="section-eyebrow">Contact</p>', '<p class="section-eyebrow">تواصل</p>'),
    ("Let's build something useful.", 'لنبنِ شيئاً مفيداً معاً.'),
    ("I'm looking for internships and entry-level opportunities in systems analysis, business analysis and data. The fastest way to reach me is email.",
     'أبحث عن فرص تدريب ووظائف للخريجين في تحليل النظم وتحليل الأعمال والبيانات. أسرع طريقة للتواصل معي هي البريد الإلكتروني.'),
    ('<span><strong>CV</strong>View or download (PDF)</span>', '<span><strong>السيرة الذاتية</strong>عرض أو تحميل (PDF بالإنجليزية)</span>'),
    ('<span><strong>Email</strong>a.alrashiddi@gmail.com</span>', '<span><strong>البريد الإلكتروني</strong><bdi>a.alrashiddi@gmail.com</bdi></span>'),
    ('<span id="year">2026</span> Abdulrahman Alrashidi</p>', '<span id="year">2026</span> عبدالرحمن الرشيدي</p>'),
    ('Built from scratch — HTML, CSS &amp; JavaScript.', 'صُمّم وبُني من الصفر — HTML وCSS وJavaScript.'),
    ('aria-label="Image viewer"', 'aria-label="عارض الصور"'),
    ('aria-label="Close"', 'aria-label="إغلاق"'),
    ('aria-label="Primary"', 'aria-label="القائمة الرئيسية"'),
]


def build():
    html = SRC.read_text(encoding="utf-8")

    missing = [en for en, _ in T if en not in html]
    if missing:
        raise SystemExit("These English strings are no longer in index.html — update tools/build_ar.py:\n\n"
                         + "\n\n".join(missing))

    # Longest first, so a short string never replaces part of a longer one.
    for en, ar in sorted(T, key=lambda p: len(p[0]), reverse=True):
        html = html.replace(en, ar)

    # Certificate titles: Arabic becomes the heading, English the subtitle.
    html = re.sub(r'<h3>([^<]+?) <span class="ar" lang="ar" dir="rtl">([^<]+)</span></h3>',
                  r'<h3>\2 <span class="ar" lang="en" dir="ltr">\1</span></h3>', html)
    html = re.sub(r'aria-label="View ([^"]+?) certificate"', r'aria-label="عرض شهادة \1"', html)
    # Image descriptions follow the Arabic card title (the lightbox reads them too).
    def alt_from(block, title_re):
        title = re.search(title_re, block)
        name = re.sub(r'<[^>]+>.*', '', title.group(1)).strip() if title else ''
        return re.sub(r'alt="[^"]*"', f'alt="شهادة {name}"', block, count=1)
    html = re.sub(r'<article class="cert".*?</article>', lambda m: alt_from(m.group(0), r'<h3>(.*?)</h3>'), html, flags=re.S)
    html = re.sub(r'<button type="button" class="ws".*?</button>', lambda m: alt_from(m.group(0), r'<strong>(.*?)</strong>'), html, flags=re.S)
    # Dates
    html = re.sub(r'(<span class="(?:tl-date|cert-date)">)([A-Z][a-z]{2}) (\d{4})</span>',
                  lambda m: f'{m.group(1)}{MONTHS[m.group(2)]} {m.group(3)}</span>', html)
    # Arrows point the other way in a right-to-left layout.
    html = html.replace('<svg class="ic"><use href="#i-arrow-right"/></svg>',
                        '<svg class="ic flip"><use href="#i-arrow-right"/></svg>')
    # The page lives one folder down.
    html = re.sub(r'(href|src|data-cert)="(assets/|script\.js)', r'\1="../\2', html)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(T)} strings)")


if __name__ == "__main__":
    build()
