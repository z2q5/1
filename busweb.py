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

# جميع المواد الحقيقية المتاحة
def get_all_resources():
    return [
        # ========== كتاب الاقتصاد الأخضر ==========
        {
            "id": 1,
            "title": "إصدار الاقتصاد الأخضر: فرص استثمارية واعدة",
            "description": "تقرير شامل عن الاقتصاد الأخضر وأساليب التحول نحوه، مع تحليل لخطط الدول الكبرى والتجربة المصرية الناجحة. يحتوي على معلومات عن الطاقة المتجددة، البناء الأخضر، السياحة البيئية، والسندات الخضراء.",
            "author": "المركز المصري للفكر والدراسات الاستراتيجية",
            "category": "تقرير بحثي",
            "type": "PDF",
            "year": 2023,
            "source": "المركز المصري للفكر والدراسات الاستراتيجية",
            "file_url": "اصدار-الاقتصاد-الاخضر.pdf",
            "download_url": "اصدار-الاقتصاد-الاخضر.pdf",
            "icon": "📊",
            "resource_type": "ملف",
            "pages": 55,
            "file_size": "4.2 MB",
            "downloads": 1560
        },
        
        # ========== رواقع حقيقية حول الاقتصاد الأخضر ==========
        {
            "id": 101,
            "title": "المركز المصري للفكر والدراسات الاستراتيجية - الموقع الرسمي",
            "description": "الموقع الرسمي للمركز المصري للفكر والدراسات الاستراتيجية الذي أصدر كتاب الاقتصاد الأخضر. يحتوي على جميع الأبحاث والدراسات المنشورة.",
            "author": "المركز المصري للفكر والدراسات الاستراتيجية",
            "category": "موقع رسمي",
            "type": "موقع إلكتروني",
            "year": 2024,
            "source": "ECSS",
            "url": "https://ecss.com.eg",
            "icon": "🏛️",
            "resource_type": "رابط",
            "views": 3450
        },
        {
            "id": 102,
            "title": "استراتيجية مصر للاقتصاد الأخضر 2030",
            "description": "الاستراتيجية الوطنية المصرية للتحول نحو الاقتصاد الأخضر بحلول عام 2030. تشمل مشاريع الطاقة المتجددة، النقل الكهربائي، وإدارة المخلفات.",
            "author": "وزارة البيئة المصرية",
            "category": "استراتيجية وطنية",
            "type": "موقع إلكتروني",
            "year": 2021,
            "source": "وزارة البيئة المصرية",
            "url": "https://www.eeaa.gov.eg/ar/البيئة-المصرية/الاقتصاد-الأخضر",
            "icon": "🇪🇬",
            "resource_type": "رابط",
            "views": 2876
        },
        {
            "id": 103,
            "title": "الصفقة الخضراء الأوروبية - Fit for 55",
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
            "id": 104,
            "title": "استراتيجية المملكة المتحدة للحياد الكربوني",
            "description": "الوثيقة الرسمية الكاملة لاستراتيجية المملكة المتحدة لتحقيق الحياد الكربوني بحلول عام 2050. تحتوي على خطط تفصيلية لجميع القطاعات.",
            "author": "حكومة المملكة المتحدة",
            "category": "استراتيجية وطنية",
            "type": "موقع إلكتروني",
            "year": 2021,
            "source": "حكومة المملكة المتحدة",
            "url": "https://www.gov.uk/government/publications/net-zero-strategy",
            "icon": "🇬🇧",
            "resource_type": "رابط",
            "views": 2105
        },
        {
            "id": 105,
            "title": "برنامج الأمم المتحدة للبيئة - الاقتصاد الأخضر",
            "description": "المصدر الرسمي لبرنامج الأمم المتحدة للبيئة حول مفاهيم وتطبيقات الاقتصاد الأخضر على مستوى العالم.",
            "author": "برنامج الأمم المتحدة للبيئة (UNEP)",
            "category": "منظمة دولية",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "UNEP",
            "url": "https://www.unep.org/explore-topics/green-economy",
            "icon": "🌍",
            "resource_type": "رابط",
            "views": 1876
        },
        {
            "id": 106,
            "title": "الهيئة العامة للطاقة المتجددة في مصر",
            "description": "الموقع الرسمي للهيئة العامة للطاقة المتجددة في مصر، يحتوي على معلومات عن مشاريع الطاقة الشمسية والرياح في مصر.",
            "author": "الهيئة العامة للطاقة المتجددة",
            "category": "هيئة حكومية",
            "type": "موقع إلكتروني",
            "year": 2024,
            "source": "NREA",
            "url": "https://nrea.gov.eg",
            "icon": "🌞",
            "resource_type": "رابط",
            "views": 1543
        },
        {
            "id": 107,
            "title": "السندات الخضراء المصرية",
            "description": "معلومات عن إصدارات السندات الخضراء السيادية المصرية وأهدافها في تمويل المشاريع الصديقة للبيئة.",
            "author": "وزارة المالية المصرية",
            "category": "تمويل أخضر",
            "type": "موقع إلكتروني",
            "year": 2022,
            "source": "وزارة المالية",
            "url": "https://www.mof.gov.eg/ar/green-bonds",
            "icon": "💰",
            "resource_type": "رابط",
            "views": 1095
        },
        {
            "id": 108,
            "title": "محطة بنبان للطاقة الشمسية",
            "description": "معلومات عن أكبر محطة للطاقة الشمسية في العالم في أسوان، مصر، كمشروع رائد في مجال الطاقة المتجددة.",
            "author": "وزارة الكهرباء والطاقة المتجددة",
            "category": "مشروع قومي",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة الكهرباء",
            "url": "https://www.moee.gov.eg/ar/benban-solar-park",
            "icon": "⚡",
            "resource_type": "رابط",
            "views": 2310
        },
        {
            "id": 109,
            "title": "محطة معالجة مصرف بحر البقر",
            "description": "معلومات عن أكبر محطة معالجة مياه في العالم في مصر، كمشروع رائد في مجال الإدارة المستدامة للمياه.",
            "author": "وزارة الإسكان والمرافق",
            "category": "مشروع قومي",
            "type": "موقع إلكتروني",
            "year": 2022,
            "source": "وزارة الإسكان",
            "url": "https://www.housing-utility.gov.eg/ar/bahr-el-baqar",
            "icon": "💧",
            "resource_type": "رابط",
            "views": 1678
        },
        {
            "id": 110,
            "title": "النقل الكهربائي في مصر",
            "description": "معلومات عن مشاريع النقل الكهربائي في مصر بما في ذلك السيارات الكهربائية والحافلات والمترو.",
            "author": "وزارة النقل المصرية",
            "category": "نقل أخضر",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة النقل",
            "url": "https://www.mot.gov.eg/ar/electric-transport",
            "icon": "🚗",
            "resource_type": "رابط",
            "views": 1987
        },
        {
            "id": 111,
            "title": "إدارة المخلفات الصلبة في مصر",
            "description": "معلومات عن المنظومة الجديدة لإدارة المخلفات الصلبة في مصر ومشاريع إعادة التدوير.",
            "author": "وزارة البيئة المصرية",
            "category": "إدارة المخلفات",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة البيئة",
            "url": "https://www.eeaa.gov.eg/ar/البيئة-المصرية/إدارة-المخلفات",
            "icon": "♻️",
            "resource_type": "رابط",
            "views": 1456
        },
        {
            "id": 112,
            "title": "الهيدروجين الأخضر في مصر",
            "description": "معلومات عن خطط مصر لتصدير الهيدروجين الأخضر والاستثمارات في هذا المجال.",
            "author": "وزارة الكهرباء والطاقة المتجددة",
            "category": "طاقة متجددة",
            "type": "موقع إلكتروني",
            "year": 2024,
            "source": "وزارة الكهرباء",
            "url": "https://www.moee.gov.eg/ar/green-hydrogen",
            "icon": "⚗️",
            "resource_type": "رابط",
            "views": 1234
        },
        {
            "id": 113,
            "title": "الزراعة المستدامة في مصر",
            "description": "معلومات عن مشاريع الزراعة المستدامة والري الحديث في مصر لتحقيق الأمن الغذائي.",
            "author": "وزارة الزراعة واستصلاح الأراضي",
            "category": "زراعة مستدامة",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة الزراعة",
            "url": "https://www.agr-egypt.gov.eg/ar/sustainable-agriculture",
            "icon": "🌱",
            "resource_type": "رابط",
            "views": 1789
        },
        {
            "id": 114,
            "title": "البناء الأخضر في مصر",
            "description": "معلومات عن معايير البناء الأخضر والمشاريع الصديقة للبيئة في مصر.",
            "author": "وزارة الإسكان والمرافق",
            "category": "بناء أخضر",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة الإسكان",
            "url": "https://www.housing-utility.gov.eg/ar/green-building",
            "icon": "🏗️",
            "resource_type": "رابط",
            "views": 1567
        },
        {
            "id": 115,
            "title": "السياحة البيئية في مصر",
            "description": "معلومات عن مشاريع السياحة البيئية والمنتجعات الخضراء في مصر.",
            "author": "وزارة السياحة والآثار",
            "category": "سياحة بيئية",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة السياحة",
            "url": "https://www.tourism.gov.eg/ar/eco-tourism",
            "icon": "🏨",
            "resource_type": "رابط",
            "views": 2109
        }
    ]

# دالة لعرض محتوى المادة
def display_resource_content(resource):
    st.markdown(f"## 📄 {resource['title']}")
    
    # عرض تفاصيل خاصة بكتاب الاقتصاد الأخضر
    if resource['id'] == 1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # عرض غلاف الكتاب
            st.markdown("### 📖 غلاف الكتاب")
            st.image("https://images.unsplash.com/photo-1544716278-e513176f20b5?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", 
                     caption="الاقتصاد الأخضر: فرص استثمارية واعدة")
            
            # روابط خاصة للكتاب
            st.markdown("### 📥 تحميل الكتاب")
            
            # زر تحميل الكتاب
            if os.path.exists(resource['file_url']):
                with open(resource['file_url'], "rb") as file:
                    file_data = file.read()
                    b64 = base64.b64encode(file_data).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="{resource["file_url"]}" class="book-button">📥 تحميل الكتاب كامل</a>'
                    st.markdown(href, unsafe_allow_html=True)
            else:
                st.warning("ملف الكتاب غير متاح للتحميل حالياً")
            
            # فصول الكتاب
            st.markdown("### 📑 فصول الكتاب")
            chapters = [
                "ماهية الاقتصاد الأخضر",
                "تطور مفهوم الاقتصاد الأخضر", 
                "أساليب التحول نحو الاقتصاد الأخضر",
                "خطط القوى الدولية نحو الاقتصاد الأخضر",
                "بورصة الكربون",
                "خطة أوروبا للوصول إلى حياد الكربون",
                "الصفقة الخضراء للمفوضية الأوروبية",
                "استراتيجية الصفر البريطانية",
                "التحول نحو الهيدروجين الأخضر",
                "التجربة المصرية صوب الاقتصاد الأخضر",
                "استراتيجية مصر للاقتصاد الأخضر",
                "السندات الخضراء وبورصة الكربون المصرية",
                "المشاريع المصرية في مجال الاقتصاد الأخضر",
                "فوائد الاقتصاد الأخضر لمصر"
            ]
            
            for i, chapter in enumerate(chapters, 1):
                st.write(f"**الفصل {i}:** {chapter}")
        
        with col2:
            # معلومات الكتاب
            st.markdown("### 📋 معلومات الكتاب")
            st.markdown(f"**المؤلف:** {resource['author']}")
            st.markdown(f"**السنة:** {resource['year']}")
            st.markdown(f"**عدد الصفحات:** {resource['pages']}")
            st.markdown(f"**حجم الملف:** {resource['file_size']}")
            st.markdown(f"**التصنيف:** {resource['category']}")
            st.markdown(f"**تم التحميل:** {resource['downloads']:,} مرة")
            
            st.divider()
            
            # وصف الكتاب
            st.markdown("### 📝 ملخص الكتاب")
            st.write(resource['description'])
            
            st.markdown("""
            #### 📊 محتويات الكتاب الرئيسية:
            
            **الجزء الأول: المفاهيم والأسس**
            - تعريف الاقتصاد الأخضر وتطوره التاريخي
            - أساليب التحول نحو الاقتصاد الأخضر
            - البناء الأخضر والاقتصاد الدائري
            - الاستهلاك المستدام والطاقة المتجددة
            
            **الجزء الثاني: التجارب الدولية**
            - خطط الدول الكبرى (الاتحاد الأوروبي، المملكة المتحدة، الولايات المتحدة)
            - أسواق الكربون العالمية
            - استراتيجيات الحياد الكربوني
            - التحول نحو الهيدروجين الأخضر
            
            **الجزء الثالث: التجربة المصرية**
            - استراتيجية مصر للاقتصاد الأخضر 2030
            - المشاريع القومية الخضراء في مصر
            - السندات الخضراء وبورصة الكربون المصرية
            - قطاع الطاقة المتجددة في مصر
            - إدارة المياه والنقل الكهربائي
            - الفوائد الاقتصادية والبيئية لمصر
            
            **الجزء الرابع: المستقبل والفرص**
            - فرص الاستثمار في الاقتصاد الأخضر
            - التحديات والحلول
            - الرؤية المستقبلية للاقتصاد المستدام
            """)
            
            # روابط ذات صلة
            st.markdown("### 🔗 روابط ذات صلة")
            related_links = [
                ("🌐 الموقع الرسمي للمركز المصري للفكر", "https://ecss.com.eg"),
                ("🇪🇬 استراتيجية مصر للاقتصاد الأخضر", "https://www.eeaa.gov.eg/ar/البيئة-المصرية/الاقتصاد-الأخضر"),
                ("⚡ الهيئة العامة للطاقة المتجددة", "https://nrea.gov.eg"),
                ("💧 محطة معالجة بحر البقر", "https://www.housing-utility.gov.eg/ar/bahr-el-baqar")
            ]
            
            for link_text, link_url in related_links:
                st.markdown(f"[{link_text}]({link_url})", unsafe_allow_html=True)
    else:
        # عرض التفاصيل للمواد الأخرى
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f'<div style="font-size: 5rem; text-align: center; color: #2196F3; margin: 20px 0;">{resource.get("icon", "📄")}</div>', unsafe_allow_html=True)
            
            # زر فتح الرابط
            if resource.get('url'):
                st.markdown(f'<a href="{resource["url"]}" target="_blank" class="resource-button">🔗 فتح الرابط</a>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**المؤلف/المصدر:** {resource.get('author', resource.get('source', 'غير محدد'))}")
            st.markdown(f"**السنة:** {resource.get('year', 'غير محدد')}")
            st.markdown(f"**التصنيف:** {resource.get('category', 'غير مصنف')}")
            st.markdown(f"**النوع:** {resource.get('type', 'غير محدد')}")
            
            if resource.get('pages'):
                st.markdown(f"**عدد الصفحات:** {resource['pages']}")
            
            if resource.get('views'):
                st.markdown(f"**عدد المشاهدات:** {resource['views']:,}")
            
            st.divider()
            
            st.subheader("الوصف الكامل")
            st.write(resource['description'])
            
            # روابط إضافية حسب النوع
            if "مصر" in resource.get('category', ''):
                st.markdown("### 📋 معلومات إضافية")
                
                if "طاقة" in resource['title'].lower():
                    st.info("""
                    **معلومات عن الطاقة المتجددة في مصر:**
                    - تهدف مصر إلى توفير 42% من الكهرباء من مصادر متجددة بحلول 2035
                    - تمتلك مصر أكبر محطة للطاقة الشمسية في العالم (بنبان)
                    - مشاريع الهيدروجين الأخضر قيد التنفيذ
                    """)
                elif "مياه" in resource['title'].lower():
                    st.info("""
                    **معلومات عن إدارة المياه في مصر:**
                    - محطة بحر البقر أكبر محطة معالجة مياه في العالم
                    - إعادة استخدام المياه تصل إلى 20% من إجمالي الاستهلاك
                    - مشاريع تأهيل الترع لتقليل الفاقد من المياه
                    """)
                elif "نقل" in resource['title'].lower():
                    st.info("""
                    **معلومات عن النقل الأخضر في مصر:**
                    - خطة لاستبدال 11000 سيارة أجرة بسيارات كهربائية
                    - شبكة محطات شحن في 7 محافظات
                    - مشروع القطار الكهربائي السريع
                    """)
    
    # زر العودة
    if st.button("← العودة إلى المكتبة"):
        st.session_state['viewing_resource'] = None
        st.rerun()

# دالة الرئيسية
def main():
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
        st.markdown("""
        <div style="text-align: center;">
            <img src="https://images.unsplash.com/photo-1544716278-e513176f20b5?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80" width="150" style="border-radius: 15px; border: 3px solid #4CAF50;">
            <h3>🌿 المكتبة البيئية</h3>
            <p>مكتبة رقمية شاملة للكتب والموارد البيئية</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        # كتاب مميز
        st.markdown("""
        <div class="sidebar-section">
        <h4>⭐ الكتاب المميز</h4>
        <div style="text-align: center;">
            <img src="https://images.unsplash.com/photo-1621451537084-482c73073a0f?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80" 
                 style="border-radius: 10px; margin-bottom: 10px;">
            <p><strong>إصدار الاقتصاد الأخضر</strong></p>
            <p>فرص استثمارية واعدة</p>
            <p style="color: #4CAF50; font-size: 0.9rem;">⬇️ 1,560 تحميل</p>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
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
        <p>• <strong>مواقع رسمية:</strong> مصادر رسمية</p>
        </div>
        """, unsafe_allow_html=True)
    
    # المحتوى الرئيسي
    st.markdown("### 📚 جميع المواد المتاحة")
    
    # عرض كتاب مميز في الأعلى
    st.markdown("### ⭐ الكتاب المميز")
    col_featured1, col_featured2, col_featured3 = st.columns([1, 2, 1])
    
    with col_featured2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F5E9, #C8E6C9); 
                    border-radius: 20px; 
                    padding: 20px; 
                    text-align: center;
                    border: 3px solid #4CAF50;
                    margin-bottom: 30px;">
            <h3 style="color: #2E7D32;">📘 إصدار الاقتصاد الأخضر</h3>
            <p style="color: #555; font-size: 1.1rem;"><strong>فرص استثمارية واعدة</strong></p>
            <p>تقرير شامل عن الاقتصاد الأخضر وأساليب التحول نحوه</p>
            <div style="display: flex; justify-content: center; gap: 20px; margin: 20px 0;">
                <div style="background-color: white; padding: 10px 20px; border-radius: 15px;">
                    <p style="color: #2196F3; margin: 0;">📄 55 صفحة</p>
                </div>
                <div style="background-color: white; padding: 10px 20px; border-radius: 15px;">
                    <p style="color: #4CAF50; margin: 0;">⬇️ 1,560 تحميل</p>
                </div>
            </div>
            <a href="#resource_1" style="background: linear-gradient(90deg, #4CAF50, #2E7D32); 
                                         color: white; 
                                         padding: 12px 30px; 
                                         border-radius: 25px; 
                                         text-decoration: none;
                                         display: inline-block;
                                         font-weight: bold;
                                         margin-top: 10px;">
                📖 عرض الكتاب
            </a>
        </div>
        """, unsafe_allow_html=True)
    
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
        """)

if __name__ == "__main__":
    main()
