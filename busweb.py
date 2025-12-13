import streamlit as st
import pandas as pd
import os
import base64

# إعدادات الصفحة
st.set_page_config(# ===== الشعار واسم المدرسة في أعلى الصفحة =====
top_left, top_center, top_right = st.columns([1, 2, 1])

with top_center:
    st.image("images.jpeg", width=180)
    st.markdown(
        """
        <h3 style="
            text-align:center;
            color:#1B5E20;
            margin-top:10px;
            font-weight:700;
        ">
            مدرسة المنيرة الخاصة
        </h3>
        """,
        unsafe_allow_html=True
    )

st.divider()
# ===========================================

    page_title="المكتبة البيئية الرقمية",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# شعار المدرسة (أضِف هنا فقط)
st.image("/mnt/data/images.jpeg", width=180)
st.markdown(
    "<h4 style='text-align:center; color:#2E7D32; margin-top:10px;'>مدرسة المنيرة الخاصة</h4>",
    unsafe_allow_html=True
)


# CSS مخصص لتحسين المظهر
st.markdown("""
<style>
    /* تصميم أنيق ونظيف */
    .main-title {
        text-align: center;
        color: #1B5E20;
        padding: 25px;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #E3F2FD, #C8E6C9);
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
        border: 1px solid #BBDEFB;
        font-family: 'Arial', sans-serif;
    }
    
    /* بطاقات المواد المعدلة */
    .resource-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.05);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: auto;
        min-height: 380px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
        border-left: 6px solid #4CAF50;
    }
    
    .resource-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 30px rgba(0,0,0,0.1);
        border-color: #4CAF50;
        background: linear-gradient(145deg, #f1f8e9, #e8f5e9);
        border-left: 6px solid #2E7D32;
    }
    
    .resource-type {
        position: absolute;
        top: 15px;
        right: 15px;
        background: linear-gradient(135deg, #4CAF50, #2E7D32);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        z-index: 2;
    }
    
    .resource-title {
        color: #1A237E;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 15px 0 20px 0;
        text-align: right;
        padding-right: 10px;
        line-height: 1.4;
        min-height: 70px;
        font-family: 'Arial', sans-serif;
    }
    
    .resource-description {
        color: #546E7A;
        font-size: 1rem;
        text-align: right;
        margin: 10px 0 15px 0;
        line-height: 1.6;
        min-height: 80px;
        opacity: 0.9;
    }
    
    .resource-category {
        display: inline-block;
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
        color: #1565C0;
        padding: 8px 18px;
        border-radius: 25px;
        font-size: 0.9rem;
        margin: 10px 0;
        font-weight: 600;
        border: 1px solid #90CAF9;
    }
    
    /* أزرار معدلة */
    .action-button {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        color: white;
        border: none;
        padding: 14px 24px;
        border-radius: 30px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s;
        margin-top: 15px;
        text-align: center;
        text-decoration: none;
        display: block;
        font-size: 1rem;
        box-shadow: 0 4px 8px rgba(33, 150, 243, 0.2);
    }
    
    .action-button:hover {
        background: linear-gradient(135deg, #1976D2, #0D47A1);
        box-shadow: 0 6px 12px rgba(33, 150, 243, 0.3);
        transform: translateY(-2px);
    }
    
    .download-button {
        background: linear-gradient(135deg, #4CAF50, #2E7D32);
        color: white;
        border: none;
        padding: 14px 24px;
        border-radius: 30px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s;
        margin-top: 15px;
        text-align: center;
        text-decoration: none;
        display: block;
        font-size: 1rem;
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.2);
    }
    
    .download-button:hover {
        background: linear-gradient(135deg, #2E7D32, #1B5E20);
        box-shadow: 0 6px 12px rgba(76, 175, 80, 0.3);
        transform: translateY(-2px);
    }
    
    /* الشريط الجانبي المعدل */
    .sidebar-section {
        background: linear-gradient(135deg, #F1F8E9, #E8F5E9);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        border: 1px solid #C8E6C9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    
    .search-box {
        width: 100%;
        padding: 14px 20px;
        border: 2px solid #4CAF50;
        border-radius: 30px;
        font-size: 1rem;
        margin-bottom: 25px;
        background: white;
        box-shadow: 0 3px 6px rgba(0,0,0,0.05);
        transition: all 0.3s;
    }
    
    .search-box:focus {
        outline: none;
        border-color: #2196F3;
        box-shadow: 0 4px 10px rgba(33, 150, 243, 0.2);
    }
    
    .stats-card {
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        padding: 20px;
        border-radius: 15px;
        color: #1B5E20;
        text-align: center;
        margin: 15px 0;
        border: 1px solid #A5D6A7;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    
    .resource-stats-card {
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
        padding: 20px;
        border-radius: 15px;
        color: #0D47A1;
        text-align: center;
        margin: 15px 0;
        border: 1px solid #90CAF9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    
    .resource-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        color: #4CAF50;
        text-align: center;
        opacity: 0.9;
    }
    
    .book-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        color: #2196F3;
        text-align: center;
        opacity: 0.9;
    }
    
    .download-count {
        position: absolute;
        bottom: 20px;
        left: 20px;
        background: linear-gradient(135deg, #FF9800, #F57C00);
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    }
    
    /* تحسينات عامة */
    .stSelectbox, .stTextInput {
        font-family: 'Arial', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Arial', sans-serif;
        font-weight: 700;
    }
    
    /* تأثيرات للبطاقات */
    .resource-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .resource-card:hover::before {
        opacity: 1;
    }
    
    /* تحسين العرض على الأجهزة الصغيرة */
    @media (max-width: 768px) {
        .resource-card {
            height: auto;
            min-height: 350px;
        }
        
        .resource-title {
            font-size: 1.2rem;
        }
        
        .main-title {
            font-size: 2rem;
            padding: 15px;
        }
    }
    
    /* تأثيرات التحميل */
    .loading-effect {
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# جميع المواد الحقيقية المتاحة
def get_all_resources():
    return [
        # ملاحظة: تمت إزالة العنصر الفارغ وإضافة جميع المواد بدءًا من ID 101
        {
            "id": 101,
            "title": "الأجندة الوطنية الخضراء - 2030",
            "description": "الرؤية الشاملة لدولة الإمارات العربية المتحدة للتحول نحو الاقتصاد الأخضر والتنمية المستدامة بحلول عام 2030.",
            "author": "حكومة دولة الإمارات العربية المتحدة",
            "category": "رؤية وطنية",
            "type": "موقع إلكتروني",
            "year": 2030,
            "source": "حكومة الإمارات",
            "url": "https://u.ae/ar/about-the-uae/strategies-initiatives-and-awards/strategies-plans-and-visions/environment-and-energy/the-uaes-green-agenda-2030",
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
            "url": "https://masdarcity.ae/ar/about",
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
            "url": "https://u.ae/ar/about-the-uae/strategies-initiatives-and-awards/strategies-plans-and-visions/environment-and-energy/uae-energy-strategy-2050#:~:text=%D8%AA%D9%87%D8%AF%D9%81%20%D8%A7%D8%B3%D8%AA%D8%B1%D8%A7%D8%AA%D9%8A%D8%AC%D9%8A%D8%A9%20%D8%A7%D9%84%D8%A5%D9%85%D8%A7%D8%B1%D8%A7%D8%AA%20%D9%84%D9%84%D8%B7%D8%A7%D9%82%D8%A9%20%2D%202050,%D8%A7%D9%84%D8%AF%D9%88%D9%84%D8%A9%20%D8%A8%D8%B3%D8%A8%D8%A8%20%D8%A7%D9%84%D9%86%D9%85%D9%88%20%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF%D9%8A%20%D8%A7%D9%84%D9%85%D8%AA%D8%B3%D8%A7%D8%B1%D8%B9.",
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
            "url": "https://noorabudhabi.ae/ar/our-plant/",
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
            "url": "https://u.ae/ar/about-the-uae/strategies-initiatives-and-awards/strategies-plans-and-visions/environment-and-energy/the-uae-net-zero-2050-strategy",
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
            "url": "https://u.ae/ar/about-the-uae/strategies-initiatives-and-awards/strategies-plans-and-visions/environment-and-energy/national-hydrogen-strategy",
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
            "source": "وكالة وام",
            "url": "https://www.wam.ae/ar/article/hszrhd0u-%D8%A7%D9%84%D8%B3%D9%8A%D8%A7%D8%AD%D8%A9-%D8%A7%D9%84%D9%85%D8%B3%D8%AA%D8%AF%D8%A9%D9%85%D8%A9-%D8%A7%D9%84%D8%A5%D9%85%D8%A7%D8%B1%D8%A7%D8%AA-%D8%AA%D9%86%D9%88%D9%8A%D8%B9-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF%D9%8A-%D9%88%D8%AE%D9%81%D8%B6",
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
            "url": "https://u.ae/ar/about-the-uae/economy/green-economy-for-sustainable-development",
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
            "url": "https://u.ae/ar-ae/information-and-services/environment-and-energy/waste-management",
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
            "url": "https://www.mediaoffice.abudhabi/ar/transport/integrated-transport-centre-abu-dhabi-mobility-advances-sustainable-mobility-with-strategic-investment-in-electric-vehicle-charging-infrastructure/",
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
            "url": "https://u.ae/ar/information-and-services/environment-and-energy/agriculture",
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
            "url": "https://www.dmt.gov.ae/adm/Media-Centre/News/08Jan2025",
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
            "url": "https://www.dubaiinvestments.com/Media/0d5k3agm/di-sustainability-report-2023-ar.pdf",
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
            "url": "https://u.ae/ar/about-the-uae/economy/circular-economy",
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
            "url": "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A7%D9%84%D9%85%D9%86%D8%A7%D8%B7%D9%82_%D8%A7%D9%84%D9%85%D8%AD%D9%85%D9%8A%D8%A9_%D9%81%D9%8A_%D8%AF%D9%88%D9%84%D8%A9_%D8%A7%D9%84%D8%A5%D9%85%D8%A7%D8%B1%D8%A7%D8%AA_%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9_%D8%A7%D9%84%D9%85%D8%AA%D8%AD%D8%AF%D8%A9",
            "icon": "🦜",
            "resource_type": "رابط",
            "views": 1234
        }
    ]

# دالة لعرض محتوى المادة
def display_resource_content(resource):
    st.markdown(f"## {resource.get('icon', '📄')} {resource['title']}")
    
    # عرض تفاصيل المادة
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f'<div style="font-size: 4rem; text-align: center; color: #2196F3; margin: 20px 0;">{resource.get("icon", "🌐")}</div>', unsafe_allow_html=True)
        
        if resource.get('url'):
            st.markdown(f'<a href="{resource["url"]}" target="_blank" class="action-button">🔗 فتح الرابط</a>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📋 معلومات المادة")
        
        info_cols = st.columns(2)
        with info_cols[0]:
            st.markdown(f"**المصدر:** {resource.get('author', resource.get('source', 'غير محدد'))}")
            st.markdown(f"**السنة:** {resource.get('year', 'غير محدد')}")
            st.markdown(f"**التصنيف:** {resource.get('category', 'غير مصنف')}")
        
        with info_cols[1]:
            st.markdown(f"**النوع:** {resource.get('type', 'غير محدد')}")
            if resource.get('views'):
                st.markdown(f"**المشاهدات:** {resource['views']:,}")
        
        st.divider()
        
        st.markdown("### 📝 الوصف")
        st.write(resource['description'])
        
        # معلومات إضافية حسب التصنيف
        if "الإمارات" in str(resource.get('author', '')):
            st.markdown("### 📋 معلومات إضافية")
            
            if "طاقة" in resource['title'].lower() or "شمسية" in resource['title'].lower():
                st.info("""
                **معلومات عن الطاقة المتجددة في الإمارات:**
                - تهدف الإمارات إلى توفير 50% من الكهرباء من مصادر نظيفة بحلول 2050
                - محطة نور أبوظبي تنتج 1.17 جيجاوات من الطاقة الشمسية
                - مشاريع الهيدروجين الأخضر قيد التنفيذ
                """)
            elif "مدينة" in resource['title'].lower():
                st.info("""
                **معلومات عن مدينة مصدر:**
                - أول مدينة في العالم تعمل بالطاقة النظيفة بنسبة 100%
                - تستخدم تقنيات البناء المستدام والطاقة المتجددة
                - مركز للأبحاث والابتكار في مجال الطاقة النظيفة
                """)

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
    
    # العنوان الرئيسي
    st.markdown("""
    <div class="main-title">
        <div style="font-size: 3.5rem; margin-bottom: 10px;">🌿📚</div>
        المكتبة البيئية الرقمية
        <div style="font-size: 1.2rem; font-weight: normal; margin-top: 10px; opacity: 0.8;">
            مركز المعرفة البيئية والاستدامة
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # إذا كان المستخدم يشاهد مادة
    if st.session_state['viewing_resource']:
        display_resource_content(st.session_state['viewing_resource'])
        
        # زر العودة
        if st.button("← العودة إلى المكتبة", type="primary", use_container_width=True):
            st.session_state['viewing_resource'] = None
            st.rerun()
        return
    
    # الشريط الجانبي
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="font-size: 3.5rem; color: #4CAF50;">🌿📖</div>
            <h3 style="color: #2E7D32; margin: 10px 0;">مركز المعرفة</h3>
            <p style="color: #546E7A;">موارد بيئية شاملة للبحث والدراسة</p>
        </div>
        """, unsafe_allow_html=True)
        
        # البحث
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🔍 بحث متقدم")
        search_query = st.text_input("اكتب كلمة البحث...", 
                                    placeholder="عنوان، مؤلف، أو كلمة مفتاحية",
                                    value=st.session_state.get('search_query', ''))
        st.session_state['search_query'] = search_query
        st.markdown('</div>', unsafe_allow_html=True)
        
        # التصفية
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🎯 تصفية النتائج")
        
        all_resources = get_all_resources()
        all_categories = ["الكل"] + sorted(list(set([r.get('category', 'غير مصنف') for r in all_resources])))
        all_types = ["الكل"] + sorted(list(set([r.get('type', 'غير محدد') for r in all_resources])))
        
        selected_category = st.selectbox(
            "التصنيف", 
            all_categories,
            index=all_categories.index(st.session_state['selected_category']) if st.session_state['selected_category'] in all_categories else 0
        )
        
        selected_type = st.selectbox(
            "نوع المادة", 
            all_types,
            index=all_types.index(st.session_state['selected_type']) if st.session_state['selected_type'] in all_types else 0
        )
        
        st.session_state['selected_category'] = selected_category
        st.session_state['selected_type'] = selected_type
        
        # زر إعادة التعيين
        if st.button("🔄 إعادة التعيين", use_container_width=True):
            st.session_state['search_query'] = ""
            st.session_state['selected_category'] = "الكل"
            st.session_state['selected_type'] = "الكل"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # إحصائيات
        st.markdown('<div class="resource-stats-card">', unsafe_allow_html=True)
        st.markdown("### 📊 إحصائيات")
        
        all_resources = get_all_resources()
        total_count = len(all_resources)
        total_views = sum([r.get('views', 0) for r in all_resources])
        
        stats_cols = st.columns(2)
        with stats_cols[0]:
            st.metric("المواد", f"{total_count:,}")
            st.metric("المشاهدات", f"{total_views:,}")
        with stats_cols[1]:
            st.metric("المعدل اليومي", "42")
            st.metric("معدل التفاعل", "85%")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # مساعدة
        st.markdown("""
        <div class="sidebar-section">
            <h4>💡 مساعدة سريعة</h4>
            <p>• اضغط على أي بطاقة لعرض التفاصيل</p>
            <p>• استخدم البحث للعثور على مواضيع محددة</p>
            <p>• اختر التصنيفات لتنظيم النتائج</p>
        </div>
        """, unsafe_allow_html=True)
    
    # المحتوى الرئيسي
    st.markdown("### 📚 المجموعة المتاحة")
    
    # فلترة المواد
    resources_data = get_all_resources()
    
    if st.session_state['search_query']:
        search_query = st.session_state['search_query'].lower()
        resources_data = [r for r in resources_data 
                         if (search_query in r.get('title', '').lower() 
                         or search_query in r.get('author', '').lower()
                         or search_query in r.get('description', '').lower()
                         or search_query in r.get('category', '').lower())]
    
    if st.session_state['selected_category'] != "الكل":
        resources_data = [r for r in resources_data if r.get('category') == st.session_state['selected_category']]
    
    if st.session_state['selected_type'] != "الكل":
        resources_data = [r for r in resources_data if r.get('type') == st.session_state['selected_type']]
    
    # عرض عدد النتائج
    if resources_data:
        st.markdown(f"**تم العثور على {len(resources_data)} نتيجة**")
    else:
        st.info("⚠️ لم يتم العثور على نتائج تطابق بحثك. جرب استخدام مصطلحات بحث مختلفة.")
    
    # عرض المواد
    cols_per_row = 3
    
    for i in range(0, len(resources_data), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j in range(cols_per_row):
            if i + j < len(resources_data):
                resource = resources_data[i + j]
                
                with cols[j]:
                    # التحقق من وجود المفاتيح الأساسية
                    if 'title' in resource and 'description' in resource:
                        card_html = f"""
                        <div class="resource-card">
                            <div class="resource-type">{resource.get("type", "مادة")}</div>
                            <div class="resource-icon">{resource.get("icon", "📄")}</div>
                            <div class="resource-title">{resource["title"]}</div>
                            <div class="resource-description">{resource["description"]}</div>
                            <div class="resource-category">{resource.get("category", "غير مصنف")}</div>
                        """
                        
                        if resource.get('views'):
                            card_html += f'<div class="download-count">👁️ {resource["views"]:,}</div>'
                        
                        card_html += "</div>"
                        
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        # زر العرض
                        if st.button(f"عرض التفاصيل", key=f"view_{resource['id']}", use_container_width=True):
                            st.session_state['viewing_resource'] = resource
                            st.rerun()
                    else:
                        st.error("⚠️ بيانات المادة غير مكتملة")

if __name__ == "__main__":
    main()
