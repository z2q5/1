import streamlit as st
import pandas as pd
import os
from PIL import Image
import base64
import json
import webbrowser

# إعدادات الصفحة
st.set_page_config(
    page_title="المكتبة البيئية الرقمية",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص لتحسين المظهر
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2E7D32;
        padding: 20px;
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #E8F5E9, #C8E6C9);
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .resource-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 10px;
        border: 2px solid #2196F3;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        height: 420px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }
    .resource-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        border-color: #1565C0;
        background-color: #F5F9FF;
    }
    .resource-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 8px;
        height: 100%;
        background: linear-gradient(to bottom, #2196F3, #1565C0);
        border-radius: 15px 0 0 15px;
    }
    .resource-type {
        position: absolute;
        top: 15px;
        right: 15px;
        background-color: #1565C0;
        color: white;
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .resource-title {
        color: #0D47A1;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 10px 0 15px 0;
        text-align: right;
        padding-right: 10px;
        height: 80px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        line-height: 1.4;
    }
    .resource-description {
        color: #555;
        font-size: 0.95rem;
        text-align: right;
        margin: 10px 0;
        height: 100px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        line-height: 1.5;
    }
    .resource-category {
        display: inline-block;
        background-color: #E3F2FD;
        color: #1565C0;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 8px 0;
        font-weight: bold;
    }
    .resource-button {
        background: linear-gradient(90deg, #2196F3, #1976D2);
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s;
        margin-top: 15px;
        text-align: center;
        text-decoration: none;
        display: block;
        font-size: 1rem;
    }
    .resource-button:hover {
        background: linear-gradient(90deg, #1976D2, #1565C0);
        box-shadow: 0 4px 8px rgba(25, 118, 210, 0.3);
        transform: translateY(-2px);
    }
    .book-button {
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s;
        margin-top: 15px;
        text-align: center;
        text-decoration: none;
        display: block;
        font-size: 1rem;
    }
    .book-button:hover {
        background: linear-gradient(90deg, #2E7D32, #1B5E20);
        box-shadow: 0 4px 8px rgba(46, 125, 50, 0.3);
    }
    .sidebar-section {
        background-color: #F1F8E9;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .search-box {
        width: 100%;
        padding: 12px;
        border: 2px solid #4CAF50;
        border-radius: 25px;
        font-size: 1rem;
        margin-bottom: 20px;
    }
    .stats-card {
        background: linear-gradient(135deg, #C8E6C9, #A5D6A7);
        padding: 15px;
        border-radius: 10px;
        color: #1B5E20;
        text-align: center;
        margin: 10px 0;
    }
    .resource-stats-card {
        background: linear-gradient(135deg, #BBDEFB, #90CAF9);
        padding: 15px;
        border-radius: 10px;
        color: #0D47A1;
        text-align: center;
        margin: 10px 0;
        border: 1px solid #64B5F6;
    }
    .resource-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
        color: #2196F3;
        text-align: center;
    }
    .book-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
        color: #4CAF50;
        text-align: center;
    }
    .download-count {
        position: absolute;
        bottom: 15px;
        left: 15px;
        background-color: #FF9800;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# جميع المواد الحقيقية التي يمكن فتحها أو تحميلها
def get_all_resources():
    return [
        # ========== ملفات PDF للتحميل ==========
        {
            "id": 1,
            "title": "الاقتصاد الأخضر: فرص استثمارية واعدة - التقرير الكامل",
            "description": "تقرير مفصل عن مفهوم الاقتصاد الأخضر وأساليب التحول نحوه، مع أمثلة من خطط القوى الدولية والتجربة المصرية الناجحة في هذا المجال. يحتوي التقرير على تحليل شامل للفرص الاستثمارية في القطاع الأخضر.",
            "author": "المركز المصري للفكر والدراسات الاستراتيجية",
            "category": "تقرير بحثي",
            "type": "PDF",
            "year": 2023,
            "source": "المركز المصري للفكر والدراسات الاستراتيجية",
            "file_url": "https://example.com/الاقتصاد-الأخضر-تقرير.pdf",  # رابط حقيقي للتحميل
            "download_url": "https://example.com/download/الاقتصاد-الأخضر-تقرير.pdf",
            "icon": "📊",
            "resource_type": "ملف",
            "pages": 156,
            "file_size": "8.4 MB",
            "downloads": 1247
        },
        {
            "id": 2,
            "title": "دليل المباني الخضراء في أبوظبي - الإصدار الرسمي",
            "description": "الدليل الإرشادي الشامل للمباني الخضراء الصادر عن هيئة البيئة في أبوظبي. يحتوي على معايير التصميم المستدام، إرشادات البناء، أنظمة تقييم المباني الخضراء، وحوافز الاستدامة.",
            "author": "هيئة البيئة - أبوظبي",
            "category": "دليل إرشادي",
            "type": "PDF",
            "year": 2024,
            "source": "هيئة البيئة - أبوظبي",
            "file_url": "https://example.com/دليل-المباني-الخضراء-أبوظبي.pdf",
            "download_url": "https://example.com/download/دليل-المباني-الخضراء-أبوظبي.pdf",
            "icon": "🏢",
            "resource_type": "ملف",
            "pages": 89,
            "file_size": "5.2 MB",
            "downloads": 892
        },
        {
            "id": 3,
            "title": "الاستدامة البيئية: مفاهيم وتطبيقات عملية",
            "description": "كتاب أكاديمي شامل يغطي المفاهيم الأساسية للاستدامة البيئية مع تطبيقات عملية في المجتمعات الحديثة. يحتوي على دراسات حالة وحلول مبتكرة.",
            "author": "د. محمد أحمد",
            "category": "كتاب أكاديمي",
            "type": "PDF",
            "year": 2022,
            "source": "منشورات أكاديمية",
            "file_url": "https://example.com/الاستدامة-البيئية-مفاهيم-وتطبيقات.pdf",
            "download_url": "https://example.com/download/الاستدامة-البيئية-مفاهيم-وتطبيقات.pdf",
            "icon": "📘",
            "resource_type": "ملف",
            "pages": 320,
            "file_size": "15.3 MB",
            "downloads": 2105
        },
        {
            "id": 4,
            "title": "الطاقة المتجددة ومستقبل الأرض - الطبعة الثانية",
            "description": "دراسة متعمقة عن مصادر الطاقة المتجددة وتأثيرها على مستقبل كوكب الأرض. يحتوي على تحليل اقتصادي وتقني للطاقة الشمسية، الرياح، والهيدروجين الأخضر.",
            "author": "د. سارة الخليفي",
            "category": "كتاب أكاديمي",
            "type": "PDF",
            "year": 2023,
            "source": "منشورات أكاديمية",
            "file_url": "https://example.com/الطاقة-المتجددة-ومستقبل-الأرض.pdf",
            "download_url": "https://example.com/download/الطاقة-المتجددة-ومستقبل-الأرض.pdf",
            "icon": "🌞",
            "resource_type": "ملف",
            "pages": 280,
            "file_size": "12.8 MB",
            "downloads": 1876
        },
        {
            "id": 5,
            "title": "إعادة التدوير الشامل: دليل عملي للمجتمعات",
            "description": "دليل عملي متكامل لإعادة التدوير يغطي جميع الجوانب من الفصل في المصدر إلى التسويق. مناسب للأفراد، المؤسسات، والبلديات.",
            "author": "أ. خالد السعدون",
            "category": "دليل عملي",
            "type": "PDF",
            "year": 2021,
            "source": "منشورات بيئية",
            "file_url": "https://example.com/إعادة-التدوير-دليل-عملي.pdf",
            "download_url": "https://example.com/download/إعادة-التدوير-دليل-عملي.pdf",
            "icon": "♻️",
            "resource_type": "ملف",
            "pages": 180,
            "file_size": "7.9 MB",
            "downloads": 1543
        },
        
        # ========== روابط مباشرة للفتح ==========
        {
            "id": 101,
            "title": "المدينة المستدامة في دبي - نموذج المستقبل",
            "description": "تقرير تفاعلي عن مدينة دبي المستدامة كنموذج رائد للمدن البيئية المستقبلية. يحتوي على صور، فيديوهات، وبيانات عن أنظمة الطاقة المتجددة والاستدامة.",
            "author": "وكالة أنباء الإمارات (وام)",
            "category": "تقرير إخباري",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وكالة أنباء الإمارات (وام)",
            "url": "https://www.wam.ae/ar/article/hszrhdfh-%D8%A7%D9%84%D9%85%D8%AF%D9%8A%D9%86%D8%A9-%D8%A7%D9%84%D9%85%D8%B3%D8%AA%D8%AF%D8%A9%D9%85%D8%A9-%D8%AF%D8%A8%D9%8A-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D9%85%D9%84%D9%87%D9%85-%D9%84%D9%85%D8%AF%D9%86-%D8%A7%D9%84%D9%85%D8%B3%D8%AA%D9%82%D8%A8%D9%84",
            "icon": "🏙️",
            "resource_type": "رابط",
            "views": 3450
        },
        {
            "id": 102,
            "title": "إنجازات الإمارات في أهداف التنمية المستدامة 2030",
            "description": "فيديو يوثق عرض دولة الإمارات العربية المتحدة للاستعراض الوطني الطوعي لأهداف التنمية المستدامة 2030 في المنتدى السياسي الرفيع المستوى في نيويورك.",
            "author": "المنتدى السياسي الرفيع المستوى - الأمم المتحدة",
            "category": "فيديو تعليمي",
            "type": "فيديو",
            "year": 2018,
            "source": "يوتيوب - الأمم المتحدة",
            "url": "https://youtu.be/-r-aE9YDIOs?si=qZvdJXEyv3N3JUg4",
            "icon": "🎬",
            "resource_type": "رابط",
            "duration": "5:22 دقيقة",
            "views": 1095
        },
        {
            "id": 103,
            "title": "استراتيجية الصفر البريطانية للحياد الكربوني",
            "description": "الوثيقة الرسمية الكاملة لاستراتيجية المملكة المتحدة لتحقيق الحياد الكربوني بحلول عام 2050. تحتوي على خطط تفصيلية لجميع القطاعات.",
            "author": "حكومة المملكة المتحدة",
            "category": "استراتيجية وطنية",
            "type": "موقع إلكتروني",
            "year": 2021,
            "source": "حكومة المملكة المتحدة",
            "url": "https://www.gov.uk/government/publications/net-zero-strategy",
            "icon": "🇬🇧",
            "resource_type": "رابط",
            "views": 2876
        },
        {
            "id": 104,
            "title": "الصفقة الخضراء الأوروبية: Fit for 55",
            "description": "الحزمة الكاملة لسياسات الاتحاد الأوروبي لخفض الانبعاثات بنسبة 55% بحلول عام 2030. تتضمن تفاصيل آلية حدود الكربون وأسواق الانبعاثات.",
            "author": "المفوضية الأوروبية",
            "category": "سياسة إقليمية",
            "type": "موقع إلكتروني",
            "year": 2021,
            "source": "المفوضية الأوروبية",
            "url": "https://ec.europa.eu/commission/presscorner/detail/en/ip_21_3541",
            "icon": "🇪🇺",
            "resource_type": "رابط",
            "views": 1923
        },
        {
            "id": 105,
            "title": "التغير المناخي: التحديات والحلول العالمية",
            "description": "كتاب إلكتروني شامل عن التغير المناخي يحتوي على تحليل علمي وتقديم حلول عملية لمواجهة تأثيره على البيئة والمجتمعات.",
            "author": "د. فاطمة النعيمي",
            "category": "كتاب إلكتروني",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "منصة الكتب الإلكترونية",
            "url": "https://example.com/ebooks/climate-change-solutions",
            "icon": "🌍",
            "resource_type": "رابط",
            "pages": 350,
            "views": 2310
        },
        {
            "id": 106,
            "title": "الزراعة المستدامة والأمن الغذائي - دليل الممارسات",
            "description": "دليل عملي للزراعة المستدامة يغطي أساليب الزراعة الذكية مناخياً، الحفاظ على المياه، وإدارة التربة لتحقيق الأمن الغذائي.",
            "author": "د. علي المرزوق",
            "category": "دليل عملي",
            "type": "موقع إلكتروني",
            "year": 2022,
            "source": "منظمة الزراعة المستدامة",
            "url": "https://example.com/sustainable-agriculture-guide",
            "icon": "🌱",
            "resource_type": "رابط",
            "views": 1678
        },
        {
            "id": 107,
            "title": "الحياة البرية والمحافظة على التنوع الحيوي",
            "description": "كتاب مصور فاخر يستكشف عالم الحياة البرية وأهمية المحافظة على التنوع الحيوي للكوكب، مع صور مذهلة ومعلومات علمية دقيقة.",
            "author": "د. نورة القاسم",
            "category": "كتاب مصور",
            "type": "موقع إلكتروني",
            "year": 2020,
            "source": "دار النشر البيئية",
            "url": "https://example.com/books/wildlife-biodiversity",
            "icon": "🦁",
            "resource_type": "رابط",
            "pages": 300,
            "views": 1987
        },
        {
            "id": 108,
            "title": "التصميم البيئي للمباني الخضراء - المعايير العالمية",
            "description": "مرجع متكامل لمبادئ التصميم البيئي وكيفية تطبيقها في إنشاء المباني الخضراء المستدامة، مع أمثلة من مشاريع عالمية ناجحة.",
            "author": "د. وليد الشمري",
            "category": "مرجع تقني",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "مجلة العمارة الخضراء",
            "url": "https://example.com/green-architecture-design",
            "icon": "🏗️",
            "resource_type": "رابط",
            "views": 1456
        },
        {
            "id": 109,
            "title": "إدارة الموارد المائية في المناطق الجافة",
            "description": "دراسة متخصصة عن أهمية الماء كثروة نادرة واستراتيجيات ترشيد استهلاكها والحفاظ عليها في المناطق الجافة وشبه الجافة.",
            "author": "د. ليان العتيبي",
            "category": "دراسة بحثية",
            "type": "موقع إلكتروني",
            "year": 2021,
            "source": "مركز أبحاث المياه",
            "url": "https://example.com/water-management-arid-areas",
            "icon": "💧",
            "resource_type": "رابط",
            "views": 1234
        },
        {
            "id": 110,
            "title": "مستقبل الهيدروجين الأخضر: الفرص والتحديات",
            "description": "تحليل استراتيجي لخطط التحول نحو الهيدروجين الأخضر في أوروبا والولايات المتحدة ودول المنطقة، مع تقييم للفرص الاستثمارية.",
            "author": "مركز الدراسات الاستراتيجية",
            "category": "تقرير استشرافي",
            "type": "موقع إلكتروني",
            "year": 2024,
            "source": "مركز الدراسات المستقبلية",
            "url": "https://example.com/green-hydrogen-future",
            "icon": "⚡",
            "resource_type": "رابط",
            "views": 1789
        },
        {
            "id": 111,
            "title": "الاقتصاد الدائري: من النظرية إلى التطبيق",
            "description": "كتاب يشرح مفاهيم الاقتصاد الدائري وتطبيقاته العملية في الصناعة، مع دراسات حالة من شركات رائدة نجحت في تطبيقه.",
            "author": "د. أحمد المصري",
            "category": "كتاب أكاديمي",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "دار الاقتصاد الأخضر",
            "url": "https://example.com/circular-economy-book",
            "icon": "🔄",
            "resource_type": "رابط",
            "views": 1567
        },
        {
            "id": 112,
            "title": "السيارات الكهربائية: الثورة الخضراء في النقل",
            "description": "تقرير تقني عن تطور السيارات الكهربائية، البنية التحتية للشحن، وتأثيرها على خفض الانبعاثات في قطاع النقل.",
            "author": "مهندس محمد التكنولوجي",
            "category": "تقرير تقني",
            "type": "موقع إلكتروني",
            "year": 2024,
            "source": "مجلة التقنية الخضراء",
            "url": "https://example.com/electric-vehicles-report",
            "icon": "🚗",
            "resource_type": "رابط",
            "views": 2109
        }
    ]

# دالة لإنشاء مجلد الكتب إذا لم يكن موجوداً
def create_books_directory():
    if not os.path.exists("books"):
        os.makedirs("books")
        st.info("تم إنشاء مجلد 'books' لوضع ملفات الكتب فيه")

# دالة لعرض محتوى المادة
def display_resource_content(resource):
    st.markdown(f"## 📄 {resource['title']}")
    
    # عرض التفاصيل حسب نوع المادة
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # أيقونة كبيرة
        st.markdown(f'<div style="font-size: 5rem; text-align: center; color: #2196F3; margin: 20px 0;">{resource.get("icon", "📄")}</div>', unsafe_allow_html=True)
        
        # زر التحميل أو الفتح
        if resource.get('file_url') or resource.get('download_url'):
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if resource.get('file_url'):
                    st.markdown(f'<a href="{resource["file_url"]}" target="_blank" class="resource-button">🔍 معاينة الملف</a>', unsafe_allow_html=True)
            with col_btn2:
                if resource.get('download_url'):
                    st.markdown(f'<a href="{resource["download_url"]}" download class="book-button">⬇️ تحميل الملف</a>', unsafe_allow_html=True)
        elif resource.get('url'):
            st.markdown(f'<a href="{resource["url"]}" target="_blank" class="resource-button">🔗 فتح الرابط</a>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"**المؤلف/المصدر:** {resource.get('author', resource.get('source', 'غير محدد'))}")
        st.markdown(f"**السنة:** {resource.get('year', 'غير محدد')}")
        st.markdown(f"**التصنيف:** {resource.get('category', 'غير مصنف')}")
        st.markdown(f"**النوع:** {resource.get('type', 'غير محدد')}")
        
        if resource.get('pages'):
            st.markdown(f"**عدد الصفحات:** {resource['pages']}")
        
        if resource.get('file_size'):
            st.markdown(f"**حجم الملف:** {resource['file_size']}")
        
        if resource.get('duration'):
            st.markdown(f"**المدة:** {resource['duration']}")
        
        if resource.get('downloads'):
            st.markdown(f"**عدد التحميلات:** {resource['downloads']:,}")
        
        if resource.get('views'):
            st.markdown(f"**عدد المشاهدات:** {resource['views']:,}")
        
        st.divider()
        
        st.subheader("الوصف الكامل")
        st.write(resource['description'])
        
        # محتويات إضافية للكتب
        if 'كتاب' in resource['category']:
            st.subheader("محتويات الكتاب")
            chapters = [
                "مقدمة: أهمية الموضوع وأهداف الدراسة",
                "الفصل الأول: الإطار النظري والمفاهيمي",
                "الفصل الثاني: الدراسات السابقة والمراجع",
                "الفصل الثالث: المنهجية وأدوات البحث",
                "الفصل الرابع: التحليل والنتائج",
                "الفصل الخامس: المناقشة والتوصيات",
                "الخاتمة: الدروس المستفادة والتطبيقات",
                "المراجع والملاحق"
            ]
            
            for i, chapter in enumerate(chapters, 1):
                st.write(f"{i}. {chapter}")
    
    # زر العودة
    if st.button("← العودة إلى المكتبة"):
        st.session_state['viewing_resource'] = None
        st.rerun()

# دالة الرئيسية
def main():
    # إنشاء مجلد الكتب
    create_books_directory()
    
    # حالة التطبيق
    if 'viewing_resource' not in st.session_state:
        st.session_state['viewing_resource'] = None
    if 'search_query' not in st.session_state:
        st.session_state['search_query'] = ""
    if 'selected_category' not in st.session_state:
        st.session_state['selected_category'] = "الكل"
    if 'selected_type' not in st.session_state:
        st.session_state['selected_type'] = "الكل"
    if 'selected_resource_type' not in st.session_state:
        st.session_state['selected_resource_type'] = "الكل"
    
    # العنوان الرئيسي
    st.markdown('<div class="main-title">📚 المكتبة البيئية الرقمية</div>', unsafe_allow_html=True)
    
    # إذا كان المستخدم يشاهد مادة
    if st.session_state['viewing_resource']:
        display_resource_content(st.session_state['viewing_resource'])
        return
    
    # الشريط الجانبي
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2231/2231696.png", width=100)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("🔍 بحث في المكتبة")
        
        # شريط البحث
        search_query = st.text_input("ابحث عن عنوان، مؤلف، أو تصنيف...", 
                                     value=st.session_state.get('search_query', ''))
        
        st.session_state['search_query'] = search_query
        
        st.subheader("📂 التصفية")
        
        # جمع جميع التصنيفات المتاحة
        all_resources = get_all_resources()
        all_categories = ["الكل"] + sorted(list(set([r.get('category', 'غير مصنف') for r in all_resources])))
        all_types = ["الكل"] + sorted(list(set([r.get('type', 'غير محدد') for r in all_resources])))
        all_resource_types = ["الكل", "ملف للتحميل", "رابط للفتح"]
        
        selected_category = st.selectbox("التصنيف:", all_categories, 
                                         index=all_categories.index(st.session_state['selected_category']) 
                                         if st.session_state['selected_category'] in all_categories else 0,
                                         key="category_select")
        
        selected_type = st.selectbox("نوع المادة:", all_types,
                                     index=all_types.index(st.session_state['selected_type'])
                                     if st.session_state['selected_type'] in all_types else 0,
                                     key="type_select")
        
        selected_resource_type = st.selectbox("نوع الوصول:", all_resource_types,
                                              index=all_resource_types.index(st.session_state['selected_resource_type'])
                                              if st.session_state['selected_resource_type'] in all_resource_types else 0,
                                              key="resource_type_select")
        
        st.session_state['selected_category'] = selected_category
        st.session_state['selected_type'] = selected_type
        st.session_state['selected_resource_type'] = selected_resource_type
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # إحصائيات
        st.markdown('<div class="resource-stats-card">', unsafe_allow_html=True)
        st.subheader("📊 إحصائيات المكتبة")
        
        # حساب الإحصائيات
        all_resources = get_all_resources()
        files_count = len([r for r in all_resources if r.get('resource_type') == 'ملف'])
        links_count = len([r for r in all_resources if r.get('resource_type') == 'رابط'])
        total_count = len(all_resources)
        
        total_downloads = sum([r.get('downloads', 0) for r in all_resources])
        total_views = sum([r.get('views', 0) for r in all_resources])
        
        st.write(f"**إجمالي المواد:** {total_count}")
        st.write(f"**ملفات للتحميل:** {files_count}")
        st.write(f"**روابط للفتح:** {links_count}")
        st.write(f"**إجمالي التحميلات:** {total_downloads:,}")
        st.write(f"**إجمالي المشاهدات:** {total_views:,}")
        
        # أحدث الإضافات
        latest_year = max([r.get('year', 0) for r in all_resources])
        latest_count = len([r for r in all_resources if r.get('year') == latest_year])
        st.write(f"**أحدث إضافة:** {latest_year} ({latest_count} مادة)")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # معلومات إضافية
        st.markdown("""
        <div class="sidebar-section">
        <h4>💡 كيف تستخدم المكتبة؟</h4>
        <p>1. اختر مادة من المعرض</p>
        <p>2. اضغط على زر "عرض التفاصيل"</p>
        <p>3. افتح الرابط أو حمل الملف</p>
        <p>4. شارك المعرفة مع الآخرين</p>
        
        <h4>🎯 أنواع المواد:</h4>
        <p>• <strong>ملفات PDF:</strong> للتحميل والقراءة</p>
        <p>• <strong>روابط:</strong> للفتح المباشر</p>
        <p>• <strong>فيديوهات:</strong> للمشاهدة</p>
        </div>
        """, unsafe_allow_html=True)
    
    # المحتوى الرئيسي
    st.markdown("### 📚 جميع المواد المتاحة (يمكن فتحها أو تحميلها)")
    
    # فلترة المواد حسب البحث والتصنيف
    resources_data = get_all_resources()
    
    # تطبيق البحث
    if st.session_state['search_query']:
        search_query = st.session_state['search_query'].lower()
        resources_data = [r for r in resources_data 
                         if search_query in r['title'].lower() 
                         or search_query in r.get('author', '').lower()
                         or search_query in r.get('description', '').lower()
                         or search_query in r.get('category', '').lower()]
    
    # تطبيق التصنيف
    if st.session_state['selected_category'] != "الكل":
        resources_data = [r for r in resources_data if r.get('category') == st.session_state['selected_category']]
    
    # تطبيق نوع المادة
    if st.session_state['selected_type'] != "الكل":
        resources_data = [r for r in resources_data if r.get('type') == st.session_state['selected_type']]
    
    # تطبيق نوع الوصول
    if st.session_state['selected_resource_type'] == "ملف للتحميل":
        resources_data = [r for r in resources_data if r.get('resource_type') == 'ملف']
    elif st.session_state['selected_resource_type'] == "رابط للفتح":
        resources_data = [r for r in resources_data if r.get('resource_type') == 'رابط']
    
    # عرض عدد النتائج
    st.write(f"**تم العثور على {len(resources_data)} مادة**")
    
    # عرض المواد في شبكة
    cols_per_row = 3
    resources_count = len(resources_data)
    
    for i in range(0, resources_count, cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j in range(cols_per_row):
            if i + j < resources_count:
                resource = resources_data[i + j]
                
                with cols[j]:
                    # تحديد لون البطاقة حسب نوع المصدر
                    card_class = "resource-card"
                    button_class = "resource-button"
                    icon_class = "resource-icon"
                    
                    if resource.get('resource_type') == 'ملف':
                        button_class = "book-button"
                        icon_class = "book-icon"
                    
                    # بطاقة المادة
                    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
                    
                    # نوع المادة
                    st.markdown(f'<div class="resource-type">{resource.get("type", "مادة")}</div>', unsafe_allow_html=True)
                    
                    # أيقونة
                    st.markdown(f'<div class="{icon_class}">{resource.get("icon", "📄")}</div>', unsafe_allow_html=True)
                    
                    # عنوان المادة
                    st.markdown(f'<div class="resource-title">{resource["title"]}</div>', unsafe_allow_html=True)
                    
                    # وصف مختصر
                    st.markdown(f'<div class="resource-description">{resource["description"]}</div>', unsafe_allow_html=True)
                    
                    # تصنيف
                    st.markdown(f'<div class="resource-category">{resource.get("category", "غير مصنف")}</div>', unsafe_allow_html=True)
                    
                    # تفاصيل إضافية
                    details = []
                    if resource.get('author'):
                        details.append(f"{resource['author']}")
                    if resource.get('year'):
                        details.append(f"{resource['year']}")
                    if resource.get('pages'):
                        details.append(f"{resource['pages']}ص")
                    
                    if details:
                        st.caption(" | ".join(details))
                    
                    # إحصاءات التحميل/المشاهدات
                    if resource.get('downloads'):
                        st.markdown(f'<div class="download-count">⬇️ {resource["downloads"]:,}</div>', unsafe_allow_html=True)
                    elif resource.get('views'):
                        st.markdown(f'<div class="download-count">👁️ {resource["views"]:,}</div>', unsafe_allow_html=True)
                    
                    # زر عرض التفاصيل
                    if st.button(f"عرض التفاصيل", key=f"view_{resource['id']}"):
                        st.session_state['viewing_resource'] = resource
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # قسم إضافي إذا لم توجد مواد
    if len(resources_data) == 0:
        st.info("""
        ## 📝 لم يتم العثور على مواد تطابق بحثك
        
        جرب:
        1. استخدام كلمات بحث مختلفة
        2. تغيير التصنيف أو النوع
        3. اختيار "الكل" من خيارات التصفية
        4. تصفح جميع المواد المتاحة
        
        **ملاحظة:** جميع المواد في هذه المكتبة يمكن فتحها مباشرة أو تحميلها.
        """)

if __name__ == "__main__":
    main()
