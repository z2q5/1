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
    .media-section-title {
        text-align: center;
        color: #1565C0;
        padding: 15px;
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #E3F2FD, #BBDEFB);
        border-radius: 15px;
        margin: 40px 0 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 2px solid #2196F3;
    }
    .book-card {
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        margin: 10px;
        border: 2px solid #4CAF50;
        box-shadow: 0 6px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
        height: 420px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .media-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 10px;
        border: 2px solid #2196F3;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }
    .media-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        border-color: #1565C0;
        background-color: #F5F9FF;
    }
    .media-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 8px;
        height: 100%;
        background: linear-gradient(to bottom, #2196F3, #1565C0);
        border-radius: 15px 0 0 15px;
    }
    .media-type {
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
    .book-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.15);
        border-color: #2E7D32;
    }
    .book-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #ddd;
    }
    .book-title {
        color: #1B5E20;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: center;
        height: 60px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }
    .media-title {
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
    .book-author {
        color: #666;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 10px;
    }
    .media-description {
        color: #555;
        font-size: 0.95rem;
        text-align: right;
        margin: 10px 0;
        height: 80px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        line-height: 1.5;
    }
    .book-category {
        display: inline-block;
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 5px 0;
    }
    .media-category {
        display: inline-block;
        background-color: #E3F2FD;
        color: #1565C0;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 8px 0;
        font-weight: bold;
    }
    .view-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        transition: background-color 0.3s;
        margin-top: 10px;
    }
    .media-button {
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
    .media-button:hover {
        background: linear-gradient(90deg, #1976D2, #1565C0);
        box-shadow: 0 4px 8px rgba(25, 118, 210, 0.3);
        transform: translateY(-2px);
    }
    .view-button:hover {
        background-color: #2E7D32;
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
    .media-stats-card {
        background: linear-gradient(135deg, #BBDEFB, #90CAF9);
        padding: 15px;
        border-radius: 10px;
        color: #0D47A1;
        text-align: center;
        margin: 10px 0;
        border: 1px solid #64B5F6;
    }
    .media-icon {
        font-size: 2rem;
        margin-bottom: 10px;
        color: #2196F3;
    }
</style>
""", unsafe_allow_html=True)

# بيانات الكتب (يمكن استبدالها بقاعدة بيانات حقيقية)
def get_books_data():
    return [
        {
            "id": 1,
            "title": "الاستدامة البيئية: مفاهيم وتطبيقات",
            "author": "د. محمد أحمد",
            "category": "العلوم البيئية",
            "description": "كتاب شامل عن مفاهيم الاستدامة البيئية وتطبيقاتها العملية في المجتمعات الحديثة.",
            "pages": 320,
            "year": 2022,
            "file_path": "books/sustainability_concepts.pdf",
            "image_url": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=400"
        },
        {
            "id": 2,
            "title": "الطاقة المتجددة ومستقبل الأرض",
            "author": "د. سارة الخليفي",
            "category": "الطاقة المتجددة",
            "description": "دراسة متعمقة عن مصادر الطاقة المتجددة وأثرها على مستقبل كوكب الأرض.",
            "pages": 280,
            "year": 2023,
            "file_path": "books/renewable_energy.pdf",
            "image_url": "https://images.unsplash.com/photo-1466611653911-95081537e5b7?w-400"
        },
        {
            "id": 3,
            "title": "إعادة التدوير وحماية البيئة",
            "author": "أ. خالد السعدون",
            "category": "إعادة التدوير",
            "description": "دليل عملي لإعادة التدوير وكيفية المساهمة في حماية البيئة من التلوث.",
            "pages": 180,
            "year": 2021,
            "file_path": "books/recycling_guide.pdf",
            "image_url": "https://images.unsplash.com/photo-1587293852726-70cdb56c2866?w=400"
        },
        {
            "id": 4,
            "title": "التغير المناخي: التحديات والحلول",
            "author": "د. فاطمة النعيمي",
            "category": "التغير المناخي",
            "description": "تحليل علمي للتغير المناخي وتقديم حلول عملية لمواجهة تأثيره على البيئة.",
            "pages": 350,
            "year": 2023,
            "file_path": "books/climate_change.pdf",
            "image_url": "https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=400"
        },
        {
            "id": 5,
            "title": "الزراعة المستدامة والأمن الغذائي",
            "author": "د. علي المرزوق",
            "category": "الزراعة المستدامة",
            "description": "أساليب الزراعة المستدامة ودورها في تحقيق الأمن الغذائي للمجتمعات.",
            "pages": 240,
            "year": 2022,
            "file_path": "books/sustainable_agriculture.pdf",
            "image_url": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=400"
        },
        {
            "id": 6,
            "title": "الحياة البرية والمحافظة على التنوع الحيوي",
            "author": "د. نورة القاسم",
            "category": "الحياة البرية",
            "description": "استكشاف عالم الحياة البرية وأهمية المحافظة على التنوع الحيوي للكوكب.",
            "pages": 300,
            "year": 2020,
            "file_path": "books/wildlife_conservation.pdf",
            "image_url": "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400"
        },
        {
            "id": 7,
            "title": "التصميم البيئي للمباني الخضراء",
            "author": "د. وليد الشمري",
            "category": "العمارة الخضراء",
            "description": "مبادئ التصميم البيئي وكيفية تطبيقها في إنشاء المباني الخضراء المستدامة.",
            "pages": 290,
            "year": 2023,
            "file_path": "books/green_architecture.pdf",
            "image_url": "https://images.unsplash.com/photo-1487956382158-bb926046304a?w=400"
        },
        {
            "id": 8,
            "title": "الماء: ثروة نادرة وكيفية الحفاظ عليها",
            "author": "د. ليان العتيبي",
            "category": "إدارة الموارد المائية",
            "description": "دراسة عن أهمية الماء كثروة نادرة واستراتيجيات ترشيد استهلاكها والحفاظ عليها.",
            "pages": 210,
            "year": 2021,
            "file_path": "books/water_conservation.pdf",
            "image_url": "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400"
        }
    ]

# بيانات الوسائط المتعددة التي طلبت إضافتها
def get_media_data():
    return [
        {
            "id": 101,
            "title": "دليل المباني الخضراء في أبوظبي",
            "description": "الدليل الإرشادي الشامل للمباني الخضراء الصادر عن هيئة البيئة في أبوظبي، والذي يحدد المعايير والإرشادات لتصميم وبناء المباني المستدامة.",
            "category": "دليل إرشادي",
            "type": "موقع إلكتروني",
            "year": 2024,
            "source": "هيئة البيئة - أبوظبي",
            "url": "https://abudhabienv.ae/2024/09/18/%D9%87%D9%8A%D8%A6%D8%A9-%D8%A7%D9%84%D8%A8%D9%8A%D8%A6%D8%A9-%D8%A3%D8%A8%D9%88%D8%B8%D8%A8%D9%8A%D8%8C-%D8%AA%D8%B7%D9%84%D9%82-%D8%A7%D9%84%D8%AF%D9%84%D9%8A%D9%84-%D8%A7%D9%84%D8%A5/",
            "icon": "🏢"
        },
        {
            "id": 102,
            "title": "المدينة المستدامة في دبي - نموذج لمدن المستقبل",
            "description": "تقرير عن مدينة دبي المستدامة كنموذج رائد للمدن البيئية المستقبلية التي تعتمد على الطاقة المتجددة والاستدامة في جميع جوانبها.",
            "category": "تقرير إخباري",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وكالة أنباء الإمارات (وام)",
            "url": "https://www.wam.ae/ar/article/hszrhdfh-%D8%A7%D9%84%D9%85%D8%AF%D9%8A%D9%86%D8%A9-%D8%A7%D9%84%D9%85%D8%B3%D8%AA%D8%AF%D8%A7%D9%85%D8%A9-%D8%AF%D8%A8%D9%8A-%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D9%85%D9%84%D9%87%D9%85-%D9%84%D9%85%D8%AF%D9%86-%D8%A7%D9%84%D9%85%D8%B3%D8%AA%D9%82%D8%A8%D9%84",
            "icon": "🌇"
        },
        {
            "id": 103,
            "title": "إنجازات وتحديات الإمارات في تحقيق أهداف التنمية المستدامة 2030",
            "description": "فيديو يوثق عرض دولة الإمارات العربية المتحدة للاستعراض الوطني الطوعي لأهداف التنمية المستدامة 2030 في المنتدى السياسي الرفيع المستوى في نيويورك.",
            "category": "عرض وطني",
            "type": "فيديو",
            "year": 2018,
            "source": "المنتدى السياسي الرفيع المستوى - الأمم المتحدة",
            "url": "https://youtu.be/-r-aE9YDIOs?si=qZvdJXEyv3N3JUg4",
            "icon": "🎥",
            "duration": "5:22 دقيقة"
        },
        {
            "id": 104,
            "title": "الاقتصاد الأخضر: فرص استثمارية واعدة",
            "description": "تقرير مفصل عن مفهوم الاقتصاد الأخضر وأساليب التحول نحوه، مع أمثلة من خطط القوى الدولية والتجربة المصرية الناجحة في هذا المجال.",
            "category": "تقرير بحثي",
            "type": "PDF",
            "year": 2023,
            "source": "المركز المصري للفكر والدراسات الاستراتيجية",
            "url": "اصدار-الاقتصاد-الاخضر.pdf",
            "icon": "📊"
        },
        {
            "id": 105,
            "title": "استراتيجية الصفر البريطانية للحياد الكربوني",
            "description": "نموذج استراتيجي من المملكة المتحدة لتحقيق الحياد الكربوني بحلول عام 2050، مع خطط تفصيلية لقطاعات الطاقة والصناعة والنقل والزراعة.",
            "category": "استراتيجية وطنية",
            "type": "مصدر عالمي",
            "year": 2021,
            "source": "حكومة المملكة المتحدة",
            "url": "https://www.gov.uk/government/publications/net-zero-strategy",
            "icon": "🇬🇧"
        },
        {
            "id": 106,
            "title": "الصفقة الخضراء الأوروبية: Fit for 55",
            "description": "حزمة سياسات شاملة للاتحاد الأوروبي لخفض الانبعاثات بنسبة 55% بحلول عام 2030، تتضمن توسيع أسواق الكربون وآلية حدود الكربون.",
            "category": "سياسة إقليمية",
            "type": "مصدر عالمي",
            "year": 2021,
            "source": "المفوضية الأوروبية",
            "url": "https://ec.europa.eu/commission/presscorner/detail/en/ip_21_3541",
            "icon": "🇪🇺"
        },
        {
            "id": 107,
            "title": "تجربة مصر في الاقتصاد الأخضر والمشاريع المستدامة",
            "description": "عرض للتجربة المصرية في التحول نحو الاقتصاد الأخضر، يشمل مشاريع الطاقة المتجددة، السندات الخضراء، النقل الكهربائي، وإدارة المخلفات.",
            "category": "دراسة حالة",
            "type": "ملخص تنفيذي",
            "year": 2023,
            "source": "ملخص من مصادر متعددة",
            "url": "#",
            "icon": "🇪🇬"
        },
        {
            "id": 108,
            "title": "مستقبل الهيدروجين الأخضر في المنطقة والعالم",
            "description": "تحليل لخطط التحول نحو الهيدروجين الأخضر في أوروبا والولايات المتحدة ودول المنطقة، والفرص الاستثمارية المرتبطة بهذا القطاع الواعد.",
            "category": "تقرير استشرافي",
            "type": "تحليل استراتيجي",
            "year": 2024,
            "source": "تحليل من مصادر دولية",
            "url": "#",
            "icon": "⚡"
        }
    ]

# دالة لإنشاء مجلد الكتب إذا لم يكن موجوداً
def create_books_directory():
    if not os.path.exists("books"):
        os.makedirs("books")
        st.info("تم إنشاء مجلد 'books' لوضع ملفات الكتب فيه")

# دالة لعرض محتوى ملف PDF (محاكاة)
def display_pdf_content(book):
    st.markdown(f"## 📖 {book['title']}")
    st.markdown(f"**المؤلف:** {book['author']} | **السنة:** {book['year']} | **الصفحات:** {book['pages']}")
    st.markdown(f"**التصنيف:** {book['category']}")
    
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(book['image_url'], width=300)
        st.markdown(f'<a href="{book["file_path"]}" download="{book["title"]}.pdf" class="view-button">⬇️ تحميل الكتاب</a>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("وصف الكتاب")
        st.write(book['description'])
        
        st.subheader("محتويات الكتاب")
        
        # محاكاة لفهرس المحتويات (يمكن استبداله بمحتوى حقيقي)
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
        
        # عرض PDF (محاكاة)
        st.subheader("عرض الكتاب")
        st.info("""
        **ملاحظة:** في التطبيق الحقيقي، ستظهر هنا نافذة معاينة للكتاب.
        
        للتنفيذ الكامل، يمكنك استخدام:
        1. `streamlit-pdf-viewer` لعرض PDF مباشرة
        2 رفع الملفات إلى خادم وعرضها عبر `<embed>` أو `<iframe>`
        3. استخدام Google Books API للكتب المتاحة
        """)
        
        # زر العودة
        if st.button("← العودة إلى المكتبة"):
            st.session_state['viewing_book'] = None
            st.rerun()

# دالة لعرض قسم الوسائط المتعددة
def display_media_section():
    st.markdown('<div class="media-section-title">🌍 مركز الوسائط المتعددة للاستدامة</div>', unsafe_allow_html=True)
    
    # شريط جانبي مخصص للوسائط
    with st.sidebar:
        st.markdown('<div class="media-stats-card">', unsafe_allow_html=True)
        st.subheader("📊 إحصائيات الوسائط")
        media_data = get_media_data()
        
        # حساب الإحصائيات
        types_count = {}
        categories_count = {}
        
        for item in media_data:
            types_count[item['type']] = types_count.get(item['type'], 0) + 1
            categories_count[item['category']] = categories_count.get(item['category'], 0) + 1
        
        st.write(f"**عدد المواد:** {len(media_data)}")
        st.write(f"**أحدث مادة:** 2024")
        
        # عرض أنواع الوسائط
        st.write("**الأنواع:**")
        for t, count in types_count.items():
            st.write(f"• {t}: {count}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # تصفية الوسائط
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("🔍 تصفية الوسائط")
        
        # جمع جميع التصنيفات والأنواع
        all_categories = ["الكل"] + sorted(list(set([item['category'] for item in media_data])))
        all_types = ["الكل"] + sorted(list(set([item['type'] for item in media_data])))
        
        selected_media_category = st.selectbox("اختر تصنيفًا:", all_categories, key="media_category")
        selected_media_type = st.selectbox("اختر نوعًا:", all_types, key="media_type")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # عرض الوسائط في شبكة
    media_data = get_media_data()
    
    # تطبيق التصفية
    if selected_media_category != "الكل":
        media_data = [item for item in media_data if item['category'] == selected_media_category]
    
    if selected_media_type != "الكل":
        media_data = [item for item in media_data if item['type'] == selected_media_type]
    
    st.write(f"**تم العثور على {len(media_data)} مادة**")
    
    # عرض الوسائط في شبكة
    cols_per_row = 3
    media_count = len(media_data)
    
    for i in range(0, media_count, cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j in range(cols_per_row):
            if i + j < media_count:
                item = media_data[i + j]
                
                with cols[j]:
                    # بطاقة الوسائط
                    st.markdown(f'<div class="media-card">', unsafe_allow_html=True)
                    
                    # نوع الوسائط
                    st.markdown(f'<div class="media-type">{item["type"]}</div>', unsafe_allow_html=True)
                    
                    # أيقونة
                    st.markdown(f'<div class="media-icon" style="text-align: center; font-size: 2.5rem;">{item["icon"]}</div>', unsafe_allow_html=True)
                    
                    # عنوان المادة
                    st.markdown(f'<div class="media-title">{item["title"]}</div>', unsafe_allow_html=True)
                    
                    # وصف مختصر
                    st.markdown(f'<div class="media-description">{item["description"]}</div>', unsafe_allow_html=True)
                    
                    # تصنيف
                    st.markdown(f'<div class="media-category">{item["category"]}</div>', unsafe_allow_html=True)
                    
                    # مصدر وتاريخ
                    st.caption(f"المصدر: {item['source']} | السنة: {item['year']}")
                    
                    # زر العرض/الفتح
                    if item['url'].startswith('http'):
                        button_text = "فتح الرابط" if item['type'] == "موقع إلكتروني" else "مشاهدة الفيديو"
                        st.markdown(f'<a href="{item["url"]}" target="_blank" class="media-button">{button_text}</a>', unsafe_allow_html=True)
                    elif item['url'].endswith('.pdf'):
                        st.markdown(f'<a href="{item["url"]}" download="{item["title"]}.pdf" class="media-button">📥 تحميل الملف</a>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<button class="media-button" style="background: #9E9E9E;">غير متاح للتحميل</button>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # قسم إضافي إذا لم توجد وسائط
    if len(media_data) == 0:
        st.info("""
        ## 📝 لم يتم العثور على مواد تطابق تصفيتك
        
        جرب:
        1. تغيير التصنيف أو النوع المحدد
        2. اختيار "الكل" من خيارات التصفية
        3. تصفح جميع المواد المتاحة
        """)

# دالة الرئيسية
def main():
    # إنشاء مجلد الكتب
    create_books_directory()
    
    # حالة التطبيق
    if 'viewing_book' not in st.session_state:
        st.session_state['viewing_book'] = None
    if 'search_query' not in st.session_state:
        st.session_state['search_query'] = ""
    if 'active_section' not in st.session_state:
        st.session_state['active_section'] = "الكتب"
    
    # العنوان الرئيسي
    st.markdown('<div class="main-title">📚 المكتبة البيئية الرقمية</div>', unsafe_allow_html=True)
    
    # إذا كان المستخدم يشاهد كتاباً
    if st.session_state['viewing_book']:
        display_pdf_content(st.session_state['viewing_book'])
        return
    
    # الشريط الجانبي الرئيسي
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2231/2231696.png", width=100)
        
        # قسم التنقل بين الأقسام
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("📂 أقسام المكتبة")
        
        # أزرار التنقل بين الأقسام
        section = st.radio(
            "اختر القسم:",
            ["الكتب", "الوسائط المتعددة"],
            index=0 if st.session_state.get('active_section') == "الكتب" else 1,
            key="section_navigation"
        )
        
        st.session_state['active_section'] = section
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # إذا كان القسم النشط هو الكتب
        if section == "الكتب":
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.subheader("🔍 بحث في المكتبة")
            
            # شريط البحث
            search_query = st.text_input("ابحث عن كتاب، مؤلف، أو تصنيف...", 
                                         value=st.session_state.get('search_query', ''))
            
            st.session_state['search_query'] = search_query
            
            st.subheader("📂 التصنيفات")
            
            # التصنيفات
            categories = ["الكل", "العلوم البيئية", "الطاقة المتجددة", "إعادة التدوير", 
                         "التغير المناخي", "الزراعة المستدامة", "الحياة البرية", 
                         "العمارة الخضراء", "إدارة الموارد المائية"]
            
            selected_category = st.selectbox("اختر تصنيفاً:", categories, key="book_category")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # إحصائيات الكتب
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.subheader("📊 إحصائيات المكتبة")
            books_data = get_books_data()
            st.write(f"**عدد الكتب:** {len(books_data)}")
            st.write(f"**أحدث إصدار:** 2023")
            st.write(f"**الكتب الجديدة هذا العام:** 4")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # معلومات إضافية
            st.markdown("""
            <div class="sidebar-section">
            <h4>💡 كيف تستخدم المكتبة؟</h4>
            <p>1. اختر كتاباً من المعرض</p>
            <p>2. اضغط على زر "عرض الكتاب"</p>
            <p>3. استمتع بالقراءة أو حمل النسخة</p>
            <p>4. شارك مع زملائك المهتمين</p>
            </div>
            """, unsafe_allow_html=True)
    
    # المحتوى الرئيسي حسب القسم النشط
    if st.session_state['active_section'] == "الكتب":
        display_books_section()
    else:
        display_media_section()

# دالة لعرض قسم الكتب
def display_books_section():
    st.markdown("### 📖 عرض الكتب")
    
    # فلترة الكتب حسب البحث والتصنيف
    books_data = get_books_data()
    
    if st.session_state.get('search_query'):
        search_query = st.session_state['search_query'].lower()
        books_data = [book for book in books_data 
                     if search_query in book['title'].lower() 
                     or search_query in book['author'].lower()
                     or search_query in book['category'].lower()]
    
    # تطبيق تصفية التصنيف من الشريط الجانبي
    selected_category = st.session_state.get('selected_category', 'الكل')
    if selected_category != "الكل":
        books_data = [book for book in books_data if book['category'] == selected_category]
    
    # عرض عدد النتائج
    st.write(f"**تم العثور على {len(books_data)} كتاب**")
    
    # عرض الكتب في شبكة
    cols_per_row = 4
    books_count = len(books_data)
    
    for i in range(0, books_count, cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j in range(cols_per_row):
            if i + j < books_count:
                book = books_data[i + j]
                
                with cols[j]:
                    # بطاقة الكتاب
                    st.markdown(f'<div class="book-card">', unsafe_allow_html=True)
                    
                    # صورة الكتاب
                    st.image(book['image_url'], use_column_width=True)
                    
                    # عنوان الكتاب
                    st.markdown(f'<div class="book-title">{book["title"]}</div>', unsafe_allow_html=True)
                    
                    # مؤلف الكتاب
                    st.markdown(f'<div class="book-author">تأليف: {book["author"]}</div>', unsafe_allow_html=True)
                    
                    # تصنيف الكتاب
                    st.markdown(f'<div class="book-category">{book["category"]}</div>', unsafe_allow_html=True)
                    
                    # تفاصيل إضافية
                    st.caption(f"السنة: {book['year']} | الصفحات: {book['pages']}")
                    
                    # زر عرض الكتاب
                    if st.button(f"عرض الكتاب", key=f"view_{book['id']}"):
                        st.session_state['viewing_book'] = book
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # قسم إضافي إذا لم توجد كتب
    if len(books_data) == 0:
        st.info("""
        ## 📝 لم يتم العثور على كتب تطابق بحثك
        
        جرب:
        1. استخدام كلمات بحث مختلفة
        2. تغيير التصنيف
        3. تصفح جميع الكتب (اختر "الكل" من التصنيفات)
        """)

if __name__ == "__main__":
    main()
