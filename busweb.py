import streamlit as st
import pandas as pd
import os
from PIL import Image
import base64
import json
import webbrowser
from io import BytesIO

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
    
    /* تصميم شعار المدرسة */
    .school-logo-container {
        text-align: center;
        margin: 20px 0;
        padding: 15px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .school-logo {
        max-width: 300px;
        height: auto;
        margin: 0 auto;
        display: block;
    }
    
    .school-name {
        font-size: 1.5rem;
        color: #1B5E20;
        font-weight: bold;
        margin-top: 10px;
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
        
        .school-logo {
            max-width: 200px;
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

# دالة لإنشاء صورة base64 من الصورة المرفقة
def create_school_logo():
    # بيانات الصورة المرفقة (base64)
    # في بيئة حقيقية، ستكون الصورة مخزنة في ملف
    # هنا نعرض تصميم بديل مع نص الشعار
    return """
    <div class="school-logo-container">
        <div style="background: linear-gradient(135deg, #1B5E20, #2E7D32); 
                    padding: 25px 40px; 
                    border-radius: 12px;
                    display: inline-block;
                    text-align: center;
                    color: white;
                    box-shadow: 0 6px 15px rgba(27, 94, 32, 0.3);">
            <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 15px;">A.M.P.S</div>
            <div style="font-size: 2.2rem; font-weight: bold; margin-bottom: 10px;">ALMUNEERA</div>
            <div style="font-size: 1.8rem; font-weight: bold; opacity: 0.9;">PRIVATE SCHOOL</div>
        </div>
        <div class="school-name">مدرسة المنيرة الخاصة</div>
    </div>
    """

# جميع المواد الحقيقية المتاحة
def get_all_resources():
    return [
        {
            "id": 1,
            "title": "إصدار الاقتصاد الأخضر: فرص استثمارية واعدة",
            "description": "تقرير شامل عن الاقتصاد الأخضر وأساليب التحول نحوه، مع تحليل لخطط الدول الكبرى والتجربة المصرية الناجحة. يحتوي على معلومات عن الطاقة المتجددة، البناء الأخضر، السياحة البيئية، والسندات الخضراء.",
            "author": "المركز المصري للفكر والدراسات الاستراتيجية",
            "category": "تقرير بحثي",
            "type": "PDF",
            "year": 2023,
            "source": "المركز المصري للفكر والدراسات الاستراتيجية",
            "file_url": "https://ecss.com.eg/wp-content/uploads/2021/11/%D8%A7%D8%B5%D8%AF%D8%A7%D8%B1-%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF-%D8%A7%D9%84%D8%A7%D8%AE%D8%B6%D8%B1.pdf",
            "download_url": "https://ecss.com.eg/wp-content/uploads/2021/11/%D8%A7%D8%B5%D8%AF%D8%A7%D8%B1-%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF-%D8%A7%D9%84%D8%A7%D8%AE%D8%B6%D8%B1.pdf",
            "icon": "📊",
            "resource_type": "ملف",
            "pages": 55,
            "file_size": "4.2 MB",
            "downloads": 1560
        },
        # ... بقية المواد (كما هي في الكود الأصلي)
    ]

# دالة لعرض محتوى المادة
def display_resource_content(resource):
    st.markdown(f"## {resource.get('icon', '📄')} {resource['title']}")
    
    if resource['id'] == 1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # تصميم غلاف الكتاب بدون صور
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1B5E20, #2E7D32);
                        border-radius: 15px;
                        padding: 30px 20px;
                        text-align: center;
                        color: white;
                        margin-bottom: 20px;
                        box-shadow: 0 10px 20px rgba(27, 94, 32, 0.2);">
                <div style="font-size: 3rem; margin-bottom: 15px;">📘</div>
                <h3 style="margin: 0; font-size: 1.5rem;">الاقتصاد الأخضر</h3>
                <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 1.1rem;">فرص استثمارية واعدة</p>
            </div>
            """, unsafe_allow_html=True)
            
            # زر تحميل الكتاب
            st.markdown("### 📥 تحميل الكتاب")
            if os.path.exists(resource['file_url']):
                with open(resource['file_url'], "rb") as file:
                    file_data = file.read()
                    b64 = base64.b64encode(file_data).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="{resource["file_url"]}" class="download-button">📥 تحميل الكتاب (PDF)</a>'
                    st.markdown(href, unsafe_allow_html=True)
            else:
                st.warning("ملف الكتاب غير متاح للتحميل حالياً")
            
            # معلومات سريعة
            st.markdown("""
            <div style="background: #E8F5E9; 
                        border-radius: 12px; 
                        padding: 15px; 
                        margin-top: 20px;">
                <h4 style="color: #2E7D32; margin-top: 0;">📋 معلومات سريعة</h4>
                <p><strong>الصفحات:</strong> 55 صفحة</p>
                <p><strong>الحجم:</strong> 4.2 MB</p>
                <p><strong>التحميلات:</strong> 1,560</p>
                <p><strong>التصنيف:</strong> تقرير بحثي</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # معلومات الكتاب
            st.markdown("### 📋 معلومات الكتاب")
            
            info_cols = st.columns(2)
            with info_cols[0]:
                st.markdown(f"**المؤلف:** {resource['author']}")
                st.markdown(f"**السنة:** {resource['year']}")
                st.markdown(f"**التصنيف:** {resource['category']}")
            
            with info_cols[1]:
                st.markdown(f"**عدد الصفحات:** {resource['pages']}")
                st.markdown(f"**حجم الملف:** {resource['file_size']}")
                st.markdown(f"**التحميلات:** {resource['downloads']:,}")
            
            st.divider()
            
            # وصف الكتاب
            st.markdown("### 📝 عن الكتاب")
            st.write(resource['description'])
            
            # فصول الكتاب
            st.markdown("### 📑 الفصول الرئيسية")
            chapters = [
                "ماهية الاقتصاد الأخضر",
                "تطور مفهوم الاقتصاد الأخضر", 
                "أساليب التحول نحو الاقتصاد الأخضر",
                "خطط القوى الدولية نحو الاقتصاد الأخضر",
                "بورصة الكربون العالمية",
                "الصفقة الخضراء الأوروبية",
                "استراتيجية الصفر البريطانية",
                "التحول نحو الهيدروجين الأخضر"
            ]
            
            for i, chapter in enumerate(chapters, 1):
                st.markdown(f"**{i}.** {chapter}")
    else:
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
    
    # العنوان الرئيسي مع شعار المدرسة
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # عرض شعار المدرسة
        st.markdown(create_school_logo(), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="main-title">
            <div style="font-size: 3.5rem; margin-bottom: 10px;">🌿📚</div>
            المكتبة البيئية الرقمية
            <div style="font-size: 1.2rem; font-weight: normal; margin-top: 10px; opacity: 0.8;">
                مركز المعرفة البيئية والاستدامة<br>
                <span style="font-size: 1rem; color: #2E7D32;">برعاية مدرسة المنيرة الخاصة</span>
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
        # شعار المدرسة في الشريط الجانبي
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, #1B5E20, #2E7D32); 
                        padding: 20px 15px; 
                        border-radius: 10px;
                        text-align: center;
                        color: white;
                        box-shadow: 0 4px 12px rgba(27, 94, 32, 0.3);">
                <div style="font-size: 1.8rem; font-weight: bold; margin-bottom: 10px;">A.M.P.S</div>
                <div style="font-size: 1.5rem; font-weight: bold;">ALMUNEERA</div>
                <div style="font-size: 1.2rem; opacity: 0.9; margin-top: 5px;">PRIVATE SCHOOL</div>
            </div>
            <div style="color: #2E7D32; font-weight: bold; margin-top: 10px; font-size: 1.1rem;">
                مدرسة المنيرة الخاصة
            </div>
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
        total_downloads = sum([r.get('downloads', 0) for r in all_resources])
        total_views = sum([r.get('views', 0) for r in all_resources])
        
        stats_cols = st.columns(2)
        with stats_cols[0]:
            st.metric("المواد", f"{total_count:,}")
            st.metric("التحميلات", f"{total_downloads:,}")
        with stats_cols[1]:
            st.metric("المشاهدات", f"{total_views:,}")
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
                         if search_query in r['title'].lower() 
                         or search_query in r.get('author', '').lower()
                         or search_query in r.get('description', '').lower()
                         or search_query in r.get('category', '').lower()]
    
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
                    card_html = f"""
                    <div class="resource-card">
                        <div class="resource-type">{resource.get("type", "مادة")}</div>
                        <div class="resource-icon">{resource.get("icon", "📄")}</div>
                        <div class="resource-title">{resource["title"]}</div>
                        <div class="resource-description">{resource["description"]}</div>
                        <div class="resource-category">{resource.get("category", "غير مصنف")}</div>
                    """
                    
                    if resource.get('downloads'):
                        card_html += f'<div class="download-count">⬇️ {resource["downloads"]:,}</div>'
                    elif resource.get('views'):
                        card_html += f'<div class="download-count">👁️ {resource["views"]:,}</div>'
                    
                    card_html += "</div>"
                    
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # زر العرض
                    if st.button(f"عرض التفاصيل", key=f"view_{resource['id']}", use_container_width=True):
                        st.session_state['viewing_resource'] = resource
                        st.rerun()

if __name__ == "__main__":
    main()
