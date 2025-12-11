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
        height: 380px;
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
        height: 70px;
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
        height: 90px;
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
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s;
        margin-top: 15px;
        text-align: center;
        text-decoration: none;
        display: block;
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
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s;
        margin-top: 15px;
        text-align: center;
        text-decoration: none;
        display: block;
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
        font-size: 2rem;
        margin-bottom: 10px;
        color: #2196F3;
        text-align: center;
    }
    .book-icon {
        font-size: 2rem;
        margin-bottom: 10px;
        color: #4CAF50;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# جميع المواد (كتب + وسائط متعددة)
def get_all_resources():
    return [
        # الكتب من البيانات الأصلية
        {
            "id": 1,
            "title": "الاستدامة البيئية: مفاهيم وتطبيقات",
            "description": "كتاب شامل عن مفاهيم الاستدامة البيئية وتطبيقاتها العملية في المجتمعات الحديثة.",
            "author": "د. محمد أحمد",
            "category": "العلوم البيئية",
            "type": "كتاب",
            "year": 2022,
            "source": "منشورات أكاديمية",
            "pages": 320,
            "file_path": "books/sustainability_concepts.pdf",
            "image_url": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=400",
            "icon": "📘",
            "resource_type": "كتاب"
        },
        {
            "id": 2,
            "title": "الطاقة المتجددة ومستقبل الأرض",
            "description": "دراسة متعمقة عن مصادر الطاقة المتجددة وأثرها على مستقبل كوكب الأرض.",
            "author": "د. سارة الخليفي",
            "category": "الطاقة المتجددة",
            "type": "كتاب",
            "year": 2023,
            "source": "منشورات أكاديمية",
            "pages": 280,
            "file_path": "books/renewable_energy.pdf",
            "image_url": "https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=400",
            "icon": "🌞",
            "resource_type": "كتاب"
        },
        {
            "id": 3,
            "title": "إعادة التدوير وحماية البيئة",
            "description": "دليل عملي لإعادة التدوير وكيفية المساهمة في حماية البيئة من التلوث.",
            "author": "أ. خالد السعدون",
            "category": "إعادة التدوير",
            "type": "كتاب",
            "year": 2021,
            "source": "منشورات أكاديمية",
            "pages": 180,
            "file_path": "books/recycling_guide.pdf",
            "image_url": "https://images.unsplash.com/photo-1587293852726-70cdb56c2866?w=400",
            "icon": "♻️",
            "resource_type": "كتاب"
        },
        {
            "id": 4,
            "title": "التغير المناخي: التحديات والحلول",
            "description": "تحليل علمي للتغير المناخي وتقديم حلول عملية لمواجهة تأثيره على البيئة.",
            "author": "د. فاطمة النعيمي",
            "category": "التغير المناخي",
            "type": "كتاب",
            "year": 2023,
            "source": "منشورات أكاديمية",
            "pages": 350,
            "file_path": "books/climate_change.pdf",
            "image_url": "https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=400",
            "icon": "🌍",
            "resource_type": "كتاب"
        },
        {
            "id": 5,
            "title": "الزراعة المستدامة والأمن الغذائي",
            "description": "أساليب الزراعة المستدامة ودورها في تحقيق الأمن الغذائي للمجتمعات.",
            "author": "د. علي المرزوق",
            "category": "الزراعة المستدامة",
            "type": "كتاب",
            "year": 2022,
            "source": "منشورات أكاديمية",
            "pages": 240,
            "file_path": "books/sustainable_agriculture.pdf",
            "image_url": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=400",
            "icon": "🌱",
            "resource_type": "كتاب"
        },
        {
            "id": 6,
            "title": "الحياة البرية والمحافظة على التنوع الحيوي",
            "description": "استكشاف عالم الحياة البرية وأهمية المحافظة على التنوع الحيوي للكوكب.",
            "author": "د. نورة القاسم",
            "category": "الحياة البرية",
            "type": "كتاب",
            "year": 2020,
            "source": "منشورات أكاديمية",
            "pages": 300,
            "file_path": "books/wildlife_conservation.pdf",
            "image_url": "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400",
            "icon": "🦁",
            "resource_type": "كتاب"
        },
        {
            "id": 7,
            "title": "التصميم البيئي للمباني الخضراء",
            "description": "مبادئ التصميم البيئي وكيفية تطبيقها في إنشاء المباني الخضراء المستدامة.",
            "author": "د. وليد الشمري",
            "category": "العمارة الخضراء",
            "type": "كتاب",
            "year": 2023,
            "source": "منشورات أكاديمية",
            "pages": 290,
            "file_path": "books/green_architecture.pdf",
            "image_url": "https://images.unsplash.com/photo-1487956382158-bb926046304a?w=400",
            "icon": "🏢",
            "resource_type": "كتاب"
        },
        {
            "id": 8,
            "title": "الماء: ثروة نادرة وكيفية الحفاظ عليها",
            "description": "دراسة عن أهمية الماء كثروة نادرة واستراتيجيات ترشيد استهلاكها والحفاظ عليها.",
            "author": "د. ليان العتيبي",
            "category": "إدارة الموارد المائية",
            "type": "كتاب",
            "year": 2021,
            "source": "منشورات أكاديمية",
            "pages": 210,
            "file_path": "books/water_conservation.pdf",
            "image_url": "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400",
            "icon": "💧",
            "resource_type": "كتاب"
        },
        
        # الوسائط المتعددة التي أرسلتها
        {
            "id": 101,
            "title": "دليل المباني الخضراء في أبوظبي",
            "description": "الدليل الإرشادي الشامل للمباني الخضراء الصادر عن هيئة البيئة في أبوظبي، والذي يحدد المعايير والإرشادات لتصميم وبناء المباني المستدامة.",
            "author": "هيئة البيئة - أبوظبي",
            "category": "دليل إرشادي",
            "type": "موقع إلكتروني",
            "year": 2024,
            "source": "هيئة البيئة - أبوظبي",
            "url": "https://abudhabienv.ae/2024/09/18/%D9%87%D9%8A%D8%A6%D8%A9-%D8%A7%D9%84%D8%A8%D9%8A%D8%A6%D8%A9-%D8%A3%D8%A8%D9%88%D8%B8%D8%A8%D9%8A%D8%8C-%D8%AA%D8%B7%D9%84%D9%82-%D8%A7%D9%84%D8%AF%D9%84%D9%8A%D9%84-%D8%A7%D9%84%D8%A5/",
            "icon": "📋",
            "resource_type": "وسائط"
        },
        {
            "id": 102,
            "title": "المدينة المستدامة في دبي - نموذج لمدن المستقبل",
            "description": "تقرير عن مدينة دبي المستدامة كنموذج رائد للمدن البيئية المستقبلية التي تعتمد على الطاقة المتجددة والاستدامة في جميع جوانبها.",
            "author": "وكالة أنباء الإمارات (وام)",
            "category": "تقرير إخباري",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وكالة أنباء الإمارات (وام)",
            "url": "https://www.wam.ae/ar/article/hszrhdfh-%D8%A7%D9%84%D9%85%D8%AF%D9%8A%D9%86%D8%A9-%D8%A7%D9%84%D9%85%D8%B3%D8%AA%D8%AF%D8%A9%D9%85%D8%A9-%D8%AF%D8%A8%D9%8A-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D9%85%D9%84%D9%87%D9%85-%D9%84%D9%85%D8%AF%D9%86-%D8%A7%D9%84%D9%85%D8%B3%D8%AA%D9%82%D8%A8%D9%84",
            "icon": "🏙️",
            "resource_type": "وسائط"
        },
        {
            "id": 103,
            "title": "إنجازات وتحديات الإمارات في تحقيق أهداف التنمية المستدامة 2030",
            "description": "فيديو يوثق عرض دولة الإمارات العربية المتحدة للاستعراض الوطني الطوعي لأهداف التنمية المستدامة 2030 في المنتدى السياسي الرفيع المستوى في نيويورك.",
            "author": "المنتدى السياسي الرفيع المستوى - الأمم المتحدة",
            "category": "عرض وطني",
            "type": "فيديو",
            "year": 2018,
            "source": "المنتدى السياسي الرفيع المستوى - الأمم المتحدة",
            "url": "https://youtu.be/-r-aE9YDIOs?si=qZvdJXEyv3N3JUg4",
            "icon": "🎬",
            "resource_type": "وسائط",
            "duration": "5:22 دقيقة"
        },
        {
            "id": 104,
            "title": "الاقتصاد الأخضر: فرص استثمارية واعدة",
            "description": "تقرير مفصل عن مفهوم الاقتصاد الأخضر وأساليب التحول نحوه، مع أمثلة من خطط القوى الدولية والتجربة المصرية الناجحة في هذا المجال.",
            "author": "المركز المصري للفكر والدراسات الاستراتيجية",
            "category": "تقرير بحثي",
            "type": "PDF",
            "year": 2023,
            "source": "المركز المصري للفكر والدراسات الاستراتيجية",
            "file_path": "اصدار-الاقتصاد-الاخضر.pdf",
            "icon": "📈",
            "resource_type": "وسائط"
        },
        {
            "id": 105,
            "title": "استراتيجية الصفر البريطانية للحياد الكربوني",
            "description": "نموذج استراتيجي من المملكة المتحدة لتحقيق الحياد الكربوني بحلول عام 2050، مع خطط تفصيلية لقطاعات الطاقة والصناعة والنقل والزراعة.",
            "author": "حكومة المملكة المتحدة",
            "category": "استراتيجية وطنية",
            "type": "مصدر عالمي",
            "year": 2021,
            "source": "حكومة المملكة المتحدة",
            "url": "https://www.gov.uk/government/publications/net-zero-strategy",
            "icon": "🇬🇧",
            "resource_type": "وسائط"
        },
        {
            "id": 106,
            "title": "الصفقة الخضراء الأوروبية: Fit for 55",
            "description": "حزمة سياسات شاملة للاتحاد الأوروبي لخفض الانبعاثات بنسبة 55% بحلول عام 2030، تتضمن توسيع أسواق الكربون وآلية حدود الكربون.",
            "author": "المفوضية الأوروبية",
            "category": "سياسة إقليمية",
            "type": "مصدر عالمي",
            "year": 2021,
            "source": "المفوضية الأوروبية",
            "url": "https://ec.europa.eu/commission/presscorner/detail/en/ip_21_3541",
            "icon": "🇪🇺",
            "resource_type": "وسائط"
        },
        {
            "id": 107,
            "title": "تجربة مصر في الاقتصاد الأخضر والمشاريع المستدامة",
            "description": "عرض للتجربة المصرية في التحول نحو الاقتصاد الأخضر، يشمل مشاريع الطاقة المتجددة، السندات الخضراء، النقل الكهربائي، وإدارة المخلفات.",
            "author": "ملخص من مصادر متعددة",
            "category": "دراسة حالة",
            "type": "ملخص تنفيذي",
            "year": 2023,
            "source": "ملخص من مصادر متعددة",
            "icon": "🇪🇬",
            "resource_type": "وسائط"
        },
        {
            "id": 108,
            "title": "مستقبل الهيدروجين الأخضر في المنطقة والعالم",
            "description": "تحليل لخطط التحول نحو الهيدروجين الأخضر في أوروبا والولايات المتحدة ودول المنطقة، والفرص الاستثمارية المرتبطة بهذا القطاع الواعد.",
            "author": "تحليل من مصادر دولية",
            "category": "تقرير استشرافي",
            "type": "تحليل استراتيجي",
            "year": 2024,
            "source": "تحليل من مصادر دولية",
            "icon": "⚡",
            "resource_type": "وسائط"
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
        if resource.get('image_url'):
            st.image(resource['image_url'], width=300)
        else:
            st.markdown(f'<div style="font-size: 5rem; text-align: center; color: #2196F3;">{resource.get("icon", "📄")}</div>', unsafe_allow_html=True)
        
        # زر التحميل أو الفتح
        if resource.get('file_path'):
            st.markdown(f'<a href="{resource["file_path"]}" download="{resource["title"]}.pdf" class="book-button">⬇️ تحميل الملف</a>', unsafe_allow_html=True)
        elif resource.get('url') and resource['url'].startswith('http'):
            st.markdown(f'<a href="{resource["url"]}" target="_blank" class="resource-button">🔗 فتح الرابط</a>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"**المؤلف/المصدر:** {resource.get('author', resource.get('source', 'غير محدد'))}")
        st.markdown(f"**السنة:** {resource.get('year', 'غير محدد')}")
        st.markdown(f"**التصنيف:** {resource.get('category', 'غير محدد')}")
        st.markdown(f"**النوع:** {resource.get('type', 'غير محدد')}")
        
        if resource.get('pages'):
            st.markdown(f"**عدد الصفحات:** {resource['pages']}")
        
        if resource.get('duration'):
            st.markdown(f"**المدة:** {resource['duration']}")
        
        st.divider()
        
        st.subheader("الوصف")
        st.write(resource['description'])
        
        # محتويات إضافية للكتب
        if resource['resource_type'] == 'كتاب':
            st.subheader("محتويات الكتاب")
            chapters = [
                "الفصل الأول: مقدمة في الموضوع",
                "الفصل الثاني: الأطر النظرية",
                "الفصل الثالث: الدراسات السابقة",
                "الفصل الرابع: المنهجية والتحليل",
                "الفصل الخامس: النتائج والتوصيات",
                "الخاتمة والمراجع"
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
        
        st.subheader("📂 التصنيفات")
        
        # جمع جميع التصنيفات المتاحة
        all_resources = get_all_resources()
        all_categories = ["الكل"] + sorted(list(set([r.get('category', 'غير مصنف') for r in all_resources])))
        all_types = ["الكل"] + sorted(list(set([r.get('type', 'غير محدد') for r in all_resources])))
        all_resource_types = ["الكل"] + sorted(list(set([r.get('resource_type', 'غير محدد') for r in all_resources])))
        
        selected_category = st.selectbox("اختر تصنيفاً:", all_categories, 
                                         index=all_categories.index(st.session_state['selected_category']) 
                                         if st.session_state['selected_category'] in all_categories else 0,
                                         key="category_select")
        
        selected_type = st.selectbox("اختر نوع المادة:", all_types,
                                     index=all_types.index(st.session_state['selected_type'])
                                     if st.session_state['selected_type'] in all_types else 0,
                                     key="type_select")
        
        selected_resource_type = st.selectbox("نوع المصدر:", all_resource_types,
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
        books_count = len([r for r in all_resources if r.get('resource_type') == 'كتاب'])
        media_count = len([r for r in all_resources if r.get('resource_type') == 'وسائط'])
        total_count = len(all_resources)
        
        st.write(f"**إجمالي المواد:** {total_count}")
        st.write(f"**الكتب:** {books_count}")
        st.write(f"**الوسائط المتعددة:** {media_count}")
        st.write(f"**أحدث إضافة:** 2024")
        
        # تحليل حسب السنوات
        years = [r.get('year') for r in all_resources if r.get('year')]
        if years:
            st.write(f"**التوزيع الزمني:** {min(years)} - {max(years)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # معلومات إضافية
        st.markdown("""
        <div class="sidebar-section">
        <h4>💡 كيف تستخدم المكتبة؟</h4>
        <p>1. اختر مادة من المعرض</p>
        <p>2. اضغط على زر "عرض التفاصيل"</p>
        <p>3. اقرأ أو حمل المادة</p>
        <p>4. شارك مع زملائك المهتمين</p>
        </div>
        """, unsafe_allow_html=True)
    
    # المحتوى الرئيسي
    st.markdown("### 📚 جميع المواد المتاحة")
    
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
    
    # تطبيق نوع المصدر
    if st.session_state['selected_resource_type'] != "الكل":
        resources_data = [r for r in resources_data if r.get('resource_type') == st.session_state['selected_resource_type']]
    
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
                    
                    if resource.get('resource_type') == 'كتاب':
                        button_class = "book-button"
                        icon_class = "book-icon"
                    
                    # بطاقة المادة
                    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
                    
                    # نوع المادة
                    st.markdown(f'<div class="resource-type">{resource.get("type", "مادة")}</div>', unsafe_allow_html=True)
                    
                    # أيقونة
                    if resource.get('image_url'):
                        st.image(resource['image_url'], use_column_width=True)
                    else:
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
                        details.append(f"المؤلف: {resource['author']}")
                    if resource.get('year'):
                        details.append(f"السنة: {resource['year']}")
                    if resource.get('pages'):
                        details.append(f"الصفحات: {resource['pages']}")
                    
                    if details:
                        st.caption(" | ".join(details))
                    
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
        """)

if __name__ == "__main__":
    main()
