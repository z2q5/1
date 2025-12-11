import streamlit as st
import pandas as pd
import os
from PIL import Image
import base64
import json

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
    .book-author {
        color: #666;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 10px;
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

# دالة الرئيسية
def main():
    # إنشاء مجلد الكتب
    create_books_directory()
    
    # حالة التطبيق
    if 'viewing_book' not in st.session_state:
        st.session_state['viewing_book'] = None
    if 'search_query' not in st.session_state:
        st.session_state['search_query'] = ""
    
    # العنوان الرئيسي
    st.markdown('<div class="main-title">📚 المكتبة البيئية الرقمية</div>', unsafe_allow_html=True)
    
    # إذا كان المستخدم يشاهد كتاباً
    if st.session_state['viewing_book']:
        display_pdf_content(st.session_state['viewing_book'])
        return
    
    # الشريط الجانبي
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2231/2231696.png", width=100)
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
        
        selected_category = st.selectbox("اختر تصنيفاً:", categories)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # إحصائيات
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
        <p>3. استميع بالقراءة أو حمل النسخة</p>
        <p>4. شارك مع زملائك المهتمين</p>
        </div>
        """, unsafe_allow_html=True)
    
    # المحتوى الرئيسي
    st.markdown("### 📖 عرض الكتب")
    
    # فلترة الكتب حسب البحث والتصنيف
    books_data = get_books_data()
    
    if st.session_state['search_query']:
        books_data = [book for book in books_data 
                     if st.session_state['search_query'].lower() in book['title'].lower() 
                     or st.session_state['search_query'].lower() in book['author'].lower()
                     or st.session_state['search_query'].lower() in book['category'].lower()]
    
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
