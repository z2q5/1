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
        
        # ========== رواقع حقيقية حول الإمارات والاقتصاد الأخضر ==========
        {
            "id": 101,
            "title": "رؤية الإمارات 2021 - الاقتصاد الأخضر",
            "description": "الرؤية الشاملة لدولة الإمارات العربية المتحدة للتحول نحو الاقتصاد الأخضر والتنمية المستدامة بحلول عام 2021.",
            "author": "حكومة دولة الإمارات العربية المتحدة",
            "category": "رؤية وطنية",
            "type": "موقع إلكتروني",
            "year": 2021,
            "source": "حكومة الإمارات",
            "url": "https://u.ae/ar/about-the-uae/strategies-initiatives-and-awards/federal-governments-strategies-and-plans/UAE-green-growth-strategy",
            "icon": "🇦🇪",
            "resource_type": "رابط",
            "views": 3450
        },
        {
            "id": 102,
            "title": "مشروع مدينة مصدر - أبوظبي",
            "description": "المدينة المستدامة الأولى في العالم من حيث الطاقة النظيفة في أبوظبي، كمثال رائد للمدن الذكية والصديقة للبيئة.",
            "author": "شركة أبوظبي لطاقة المستقبل (مصدر)",
            "category": "مشروع مستدام",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "مصدر",
            "url": "https://masdar.ae/ar",
            "icon": "🏙️",
            "resource_type": "رابط",
            "views": 2876
        },
        {
            "id": 103,
            "title": "الاستراتيجية الوطنية للطاقة 2050 - الإمارات",
            "description": "الاستراتيجية الشاملة لدولة الإمارات لتحقيق التوازن بين الإنتاج والاستهلاك، مع التركيز على الطاقة النظيفة.",
            "author": "وزارة الطاقة والبنية التحتية",
            "category": "استراتيجية وطنية",
            "type": "موقع إلكتروني",
            "year": 2017,
            "source": "وزارة الطاقة الإماراتية",
            "url": "https://www.moei.gov.ae/ar/our-responsibilities/energy/energy-strategy-2050",
            "icon": "⚡",
            "resource_type": "رابط",
            "views": 1923
        },
        {
            "id": 104,
            "title": "محطة نور أبوظبي للطاقة الشمسية",
            "description": "أكبر محطة مستقلة للطاقة الشمسية في العالم في موقع واحد بسعة 1.17 جيجاوات في منطقة سويحان بأبوظبي.",
            "author": "شركة مياه وكهرباء الإمارات",
            "category": "طاقة متجددة",
            "type": "موقع إلكتروني",
            "year": 2019,
            "source": "EWEC",
            "url": "https://www.ewec.ae/ar/noor-abu-dhabi",
            "icon": "🌞",
            "resource_type": "رابط",
            "views": 2105
        },
        {
            "id": 105,
            "title": "الاستراتيجية الوطنية للتغير المناخي 2050 - الإمارات",
            "description": "الاستراتيجية الشاملة لمواجهة التغير المناخي وتحقيق الحياد المناخي بحلول عام 2050.",
            "author": "وزارة التغير المناخي والبيئة",
            "category": "استراتيجية وطنية",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة التغير المناخي",
            "url": "https://www.moccae.gov.ae/ar/our-responsibilities/climate-change/uae-net-zero-2050.aspx",
            "icon": "🌍",
            "resource_type": "رابط",
            "views": 1876
        },
        {
            "id": 106,
            "title": "الهيدروجين الأخضر في الإمارات",
            "description": "مشاريع الإمارات الرائدة في إنتاج وتصدير الهيدروجين الأخضر كمصدر للطاقة النظيفة.",
            "author": "وزارة الطاقة والبنية التحتية",
            "category": "طاقة نظيفة",
            "type": "موقع إلكتروني",
            "year": 2024,
            "source": "وزارة الطاقة الإماراتية",
            "url": "https://www.moei.gov.ae/ar/our-responsibilities/energy/hydrogen",
            "icon": "⚗️",
            "resource_type": "رابط",
            "views": 1543
        },
        {
            "id": 107,
            "title": "السياحة المستدامة في الإمارات",
            "description": "مبادرات السياحة البيئية والمستدامة في مختلف إمارات الدولة لتعزيز السياحة المسؤولة.",
            "author": "وزارة الاقتصاد",
            "category": "سياحة بيئية",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة الاقتصاد",
            "url": "https://www.economy.gov.ae/ar/sectors/tourism/sustainable-tourism",
            "icon": "🏨",
            "resource_type": "رابط",
            "views": 1095
        },
        {
            "id": 108,
            "title": "مبادرة الإمارات الخضراء",
            "description": "المبادرة الوطنية الشاملة لتحقيق الاستدامة البيئية في جميع القطاعات والمجالات.",
            "author": "وزارة التغير المناخي والبيئة",
            "category": "مبادرة وطنية",
            "type": "موقع إلكتروني",
            "year": 2022,
            "source": "وزارة التغير المناخي",
            "url": "https://www.moccae.gov.ae/ar/our-initiatives/green-uae.aspx",
            "icon": "🌿",
            "resource_type": "رابط",
            "views": 2310
        },
        {
            "id": 109,
            "title": "إدارة النفايات في دبي",
            "description": "الاستراتيجية الشاملة لإدارة النفايات في دبي وتحويلها إلى طاقة وموارد قابلة لإعادة التدوير.",
            "author": "بلدية دبي",
            "category": "إدارة النفايات",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "بلدية دبي",
            "url": "https://www.dm.gov.ae/ar/waste-management",
            "icon": "♻️",
            "resource_type": "رابط",
            "views": 1678
        },
        {
            "id": 110,
            "title": "النقل المستدام في الإمارات",
            "description": "مشاريع النقل الكهربائي والذكي في الإمارات بما في ذلك القطارات والمترو والمركبات الكهربائية.",
            "author": "وزارة الطاقة والبنية التحتية",
            "category": "نقل مستدام",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة الطاقة الإماراتية",
            "url": "https://www.moei.gov.ae/ar/our-responsibilities/transport/sustainable-transport",
            "icon": "🚗",
            "resource_type": "رابط",
            "views": 1987
        },
        {
            "id": 111,
            "title": "الزراعة المستدامة في الإمارات",
            "description": "تقنيات الزراعة الحديثة والمستدامة في المناطق الصحراوية لتحقيق الأمن الغذائي.",
            "author": "وزارة التغير المناخي والبيئة",
            "category": "زراعة مستدامة",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة التغير المناخي",
            "url": "https://www.moccae.gov.ae/ar/our-responsibilities/agriculture/sustainable-agriculture.aspx",
            "icon": "🌱",
            "resource_type": "رابط",
            "views": 1456
        },
        {
            "id": 112,
            "title": "البناء الأخضر في أبوظبي",
            "description": "معايير البناء الأخضر واستدامة المباني في إمارة أبوظبي وفق نظام استدامة المباني (ESTIDAMA).",
            "author": "هيئة البيئة - أبوظبي",
            "category": "بناء أخضر",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "هيئة البيئة أبوظبي",
            "url": "https://www.ead.gov.ae/ar/sustainable-buildings",
            "icon": "🏗️",
            "resource_type": "رابط",
            "views": 1567
        },
        {
            "id": 113,
            "title": "تقرير الاستدامة السنوي - الإمارات",
            "description": "التقرير السنوي الشامل عن إنجازات الاستدامة والأداء البيئي في دولة الإمارات.",
            "author": "وزارة التغير المناخي والبيئة",
            "category": "تقرير سنوي",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة التغير المناخي",
            "url": "https://www.moccae.gov.ae/ar/publications/sustainability-reports.aspx",
            "icon": "📈",
            "resource_type": "رابط",
            "views": 2109
        },
        {
            "id": 114,
            "title": "الاقتصاد الدائري في الإمارات",
            "description": "مبادرات ومشاريع الاقتصاد الدائري في الإمارات لتعظيم استفادة الموارد وتقليل الهدر.",
            "author": "وزارة الاقتصاد",
            "category": "اقتصاد دائري",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة الاقتصاد",
            "url": "https://www.economy.gov.ae/ar/sectors/circular-economy",
            "icon": "🔄",
            "resource_type": "رابط",
            "views": 1789
        },
        {
            "id": 115,
            "title": "محميات طبيعية في الإمارات",
            "description": "المحميات الطبيعية والمناطق المحمية في الإمارات للحفاظ على التنوع البيولوجي والبيئة.",
            "author": "وزارة التغير المناخي والبيئة",
            "category": "حماية بيئية",
            "type": "موقع إلكتروني",
            "year": 2023,
            "source": "وزارة التغير المناخي",
            "url": "https://www.moccae.gov.ae/ar/our-responsibilities/biodiversity/protected-areas.aspx",
            "icon": "🦜",
            "resource_type": "رابط",
            "views": 1234
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
            st.markdown('<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #E8F5E9, #C8E6C9); border-radius: 10px;">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #2E7D32;">الاقتصاد الأخضر</h3>', unsafe_allow_html=True)
            st.markdown('<p style="color: #555;">فرص استثمارية واعدة</p>', unsafe_allow_html=True)
            st.markdown('<p style="font-size: 0.9rem; color: #777;">المركز المصري للفكر والدراسات الاستراتيجية</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
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
                "التحول نحو الهيدروجين الأخضر"
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
            
            **الجزء الثالث: الفرص والتحديات**
            - فرص الاستثمار في الاقتصاد الأخضر
            - التحديات والحلول
            - الرؤية المستقبلية للاقتصاد المستدام
            """)
            
            # روابط ذات صلة
            st.markdown("### 🔗 رواقع ذات صلة")
            related_links = [
                ("🇦🇪 رؤية الإمارات 2021 - الاقتصاد الأخضر", "https://u.ae/ar/about-the-uae/strategies-initiatives-and-awards/federal-governments-strategies-and-plans/UAE-green-growth-strategy"),
                ("🏙️ مشروع مدينة مصدر - أبوظبي", "https://masdar.ae/ar"),
                ("⚡ الاستراتيجية الوطنية للطاقة 2050", "https://www.moei.gov.ae/ar/our-responsibilities/energy/energy-strategy-2050"),
                ("🌍 الاستراتيجية الوطنية للتغير المناخي 2050", "https://www.moccae.gov.ae/ar/our-responsibilities/climate-change/uae-net-zero-2050.aspx")
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
            
            if resource.get('views'):
                st.markdown(f"**عدد المشاهدات:** {resource['views']:,}")
            
            st.divider()
            
            st.subheader("الوصف الكامل")
            st.write(resource['description'])
            
            # معلومات إضافية حسب النوع
            if "الإمارات" in resource.get('author', ''):
                st.markdown("### 📋 معلومات إضافية")
                
                if "طاقة" in resource['title'].lower() or "شمسية" in resource['title'].lower():
                    st.info("""
                    **معلومات عن الطاقة المتجددة في الإمارات:**
                    - تهدف الإمارات إلى توفير 50% من الكهرباء من مصادر نظيفة بحلول 2050
                    - محطة نور أبوظبي تنتج 1.17 جيجاوات من الطاقة الشمسية
                    - مشاريع الهيدروجين الأخضر قيد التنفيذ في مصدر
                    """)
                elif "مدينة" in resource['title'].lower():
                    st.info("""
                    **معلومات عن مدينة مصدر:**
                    - أول مدينة في العالم تعمل بالطاقة النظيفة بنسبة 100%
                    - تستخدم تقنيات البناء المستدام والطاقة المتجددة
                    - مركز للأبحاث والابتكار في مجال الطاقة النظيفة
                    """)
                elif "نقل" in resource['title'].lower():
                    st.info("""
                    **معلومات عن النقل المستدام في الإمارات:**
                    - شبكة مترو دبي من أكثر شبكات المترو تطوراً
                    - مشاريع النقل الكهربائي والذكي في جميع الإمارات
                    - حافلات كهربائية في مختلف مناطق الدولة
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
            <div style="font-size: 4rem; color: #4CAF50;">🌿</div>
            <h3>المكتبة البيئية</h3>
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
        st.write(f"**رواقع للفتح:** {links_count}")
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
            <div style="font-size: 3rem; color: #4CAF50;">📘</div>
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
        <p>• <strong>رواقع:</strong> للفتح المباشر</p>
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
