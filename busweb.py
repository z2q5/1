import streamlit as st
import pandas as pd
import datetime
import os
import random
import plotly.express as px
import plotly.graph_objects as go

# ===== إعداد الصفحة =====
st.set_page_config(
    page_title="Smart Bus System - Al Munira Private School", 
    layout="wide",
    page_icon="🚍",
    initial_sidebar_state="collapsed"
)

# ===== حالة التطبيق =====
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "page" not in st.session_state:
    st.session_state.page = "student"
if "notifications" not in st.session_state:
    st.session_state.notifications = []
if "driver_logged_in" not in st.session_state:
    st.session_state.driver_logged_in = False
if "current_bus" not in st.session_state:
    st.session_state.current_bus = "1"
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# ===== البيانات الافتراضية =====
def initialize_data():
    """تهيئة جميع البيانات بشكل صحيح"""
    students_data = [
        {"id": "1001", "name": "أحمد محمد", "grade": "10-A", "bus": "1", "parent_phone": "0501234567"},
        {"id": "1002", "name": "فاطمة علي", "grade": "9-B", "bus": "2", "parent_phone": "0507654321"},
        {"id": "1003", "name": "خالد إبراهيم", "grade": "8-C", "bus": "3", "parent_phone": "0505555555"},
        {"id": "1004", "name": "سارة عبدالله", "grade": "10-B", "bus": "1", "parent_phone": "0504444444"},
        {"id": "1005", "name": "محمد حسن", "grade": "7-A", "bus": "2", "parent_phone": "0503333333"},
        {"id": "1006", "name": "ريم أحمد", "grade": "11-A", "bus": "3", "parent_phone": "0506666666"},
    ]
    
    if 'students_df' not in st.session_state or st.session_state.students_df.empty:
        st.session_state.students_df = pd.DataFrame(students_data)
    
    if 'attendance_df' not in st.session_state:
        st.session_state.attendance_df = pd.DataFrame(columns=[
            "id", "name", "grade", "bus", "status", "time", "date", "expiry_time"
        ])
    
    if 'ratings_df' not in st.session_state:
        st.session_state.ratings_df = pd.DataFrame(columns=["rating", "comments", "timestamp"])

# تهيئة البيانات
initialize_data()

# ===== كلمات المرور =====
bus_passwords = {"1": "1111", "2": "2222", "3": "3333"}
admin_pass = "admin123"

# ===== وظائف مساعدة =====
def add_notification(message):
    st.session_state.notifications.append({
        "time": datetime.datetime.now().strftime("%H:%M"),
        "message": message
    })

def get_weather():
    """بيانات الطقس"""
    return {
        "temp": random.randint(28, 42),
        "humidity": random.randint(30, 80),
        "wind_speed": random.randint(5, 25),
        "condition_ar": random.choice(["☀️ مشمس", "🌤️ غائم جزئياً", "🌧️ ممطر", "💨 عاصف"]),
        "condition_en": "Sunny"
    }

def calculate_attendance_stats():
    """حساب إحصائيات الحضور"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if st.session_state.attendance_df.empty or "date" not in st.session_state.attendance_df.columns:
        return {"total": 0, "coming": 0, "percentage": 0}
    
    today_data = st.session_state.attendance_df[
        st.session_state.attendance_df["date"] == today
    ]
    
    total = len(today_data)
    coming = len(today_data[today_data["status"] == "قادم"]) if not today_data.empty else 0
    percentage = (coming / total * 100) if total > 0 else 0
    
    return {
        "total": total,
        "coming": coming,
        "percentage": percentage
    }

def has_student_registered_today(student_id):
    """التحقق من تسجيل الطالب"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if st.session_state.attendance_df.empty or "date" not in st.session_state.attendance_df.columns:
        return False, None, None
    
    student_data = st.session_state.attendance_df[
        (st.session_state.attendance_df["id"] == student_id) & 
        (st.session_state.attendance_df["date"] == today)
    ]
    
    if not student_data.empty:
        latest_record = student_data.iloc[-1]
        expiry_time = datetime.datetime.now() + datetime.timedelta(hours=12)
        return True, latest_record["status"], expiry_time
    
    return False, None, None

def add_rating(rating, comments):
    """إضافة تقييم جديد"""
    new_rating = pd.DataFrame([{
        "rating": rating,
        "comments": comments,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    if st.session_state.ratings_df.empty:
        st.session_state.ratings_df = new_rating
    else:
        st.session_state.ratings_df = pd.concat([
            st.session_state.ratings_df, new_rating
        ], ignore_index=True)

# ===== واجهة مستخدم متطورة جداً =====
st.markdown("""
<style>
    /* التصميم العام */
    .main {
        background-color: #f8f9fa;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* كروت الإحصائيات */
    .stat-card {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        text-align: center;
        margin: 0.5rem;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.12);
    }
    
    /* كروت الطلاب */
    .student-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        border-left: 6px solid #667eea;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* كروت الطقس */
    .weather-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* كروت المميزات */
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* كروت الفريق */
    .team-card-blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .team-card-green {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .team-card-orange {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* كروت التقييم */
    .rating-card {
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* تحسين النص في العناصر */
    .stTextInput>div>div>input {
        color: #2c3e50 !important;
        font-weight: 500;
    }
    
    .stSelectbox>div>div>select {
        color: #2c3e50 !important;
    }
    
    .stRadio>div>label>div>p {
        color: #2c3e50 !important;
        font-weight: 500;
    }
    
    /* تحسين الأزرار */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
    }
    
    /* تحسين التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# ===== الهيدر الرئيسي المطور =====
col1, col2, col3 = st.columns([2, 3, 1])

with col1:
    weather_data = get_weather()
    st.markdown(f"""
    <div class='weather-card'>
        <h3>🌡️ {weather_data['temp']}°C</h3>
        <p>{weather_data['condition_ar']}</p>
        <p>💧 {weather_data['humidity']}% | 💨 {weather_data['wind_speed']} km/h</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='main-header'>
        <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>🚍 نظام الباص الذكي</h1>
        <h3 style='font-size: 1.3rem; margin-bottom: 1rem; opacity: 0.9;'>مدرسة المنيرة الخاصة - أبوظبي</h3>
        <p style='font-size: 1.1rem; opacity: 0.8;'>نظام متكامل لإدارة النقل المدرسي الذكي</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    col3a, col3b = st.columns(2)
    with col3a:
        # زر تبديل الثيم
        theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
        theme_text = "الوضع الليلي" if st.session_state.theme == "light" else "الوضع النهاري"
        if st.button(f"{theme_icon}", help=theme_text, use_container_width=True):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()
    
    with col3b:
        # زر الترجمة
        lang_icon = "🌐"
        lang_text = "English" if st.session_state.lang == "ar" else "العربية"
        if st.button(f"{lang_icon}", help=lang_text, use_container_width=True):
            st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
            st.rerun()

# ===== شريط التنقل المطور =====
st.markdown("<br>", unsafe_allow_html=True)

pages = [
    ("🎓 الطالب", "student"),
    ("🚌 السائق", "driver"), 
    ("👨‍👩‍👧 أولياء الأمور", "parents"),
    ("🏫 الإدارة", "admin"),
    ("🌦️ الطقس", "weather"),
    ("ℹ️ حول النظام", "about")
]

# إنشاء أزرار التنقل
cols = st.columns(len(pages))
for i, (name, page_key) in enumerate(pages):
    with cols[i]:
        is_active = st.session_state.page == page_key
        button_type = "primary" if is_active else "secondary"
        if st.button(name, use_container_width=True, type=button_type):
            st.session_state.page = page_key
            st.rerun()

st.markdown("---")

# ===== صفحة الطالب المطورة =====
if st.session_state.page == "student":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2>🎓 تسجيل حضور الطالب</h2>
            <p style='color: #666;'>أدخل رقم الوزارة لتسجيل حالتك اليوم</p>
        </div>
        """, unsafe_allow_html=True)
        
        # بطاقة البحث
        with st.container():
            st.markdown("<div style='background: white; padding: 2rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
            
            student_id = st.text_input(
                "🔍 رقم الوزارة",
                placeholder="أدخل رقم الوزارة هنا...",
                help="يمكنك استخدام الأرقام: 1001, 1002, 1003, 1004, 1005, 1006"
            )
            
            if student_id:
                student_info = st.session_state.students_df[
                    st.session_state.students_df["id"].astype(str) == str(student_id).strip()
                ]
                
                if not student_info.empty:
                    student = student_info.iloc[0]
                    
                    st.markdown(f"""
                    <div class='student-card'>
                        <div style='text-align: center; margin-bottom: 1.5rem;'>
                            <h3 style='color: #2c3e50; margin-bottom: 0.5rem;'>🎓 {student['name']}</h3>
                            <div style='display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;'>
                                <div style='text-align: center;'>
                                    <div style='background: #667eea; color: white; padding: 0.5rem 1rem; border-radius: 10px; font-weight: bold;'>📚 {student['grade']}</div>
                                </div>
                                <div style='text-align: center;'>
                                    <div style='background: #764ba2; color: white; padding: 0.5rem 1rem; border-radius: 10px; font-weight: bold;'>🚍 الباص {student['bus']}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    already_registered, current_status, expiry_time = has_student_registered_today(student_id)
                    
                    if already_registered:
                        status_color = "#51cf66" if current_status == "قادم" else "#ff6b6b"
                        st.markdown(f"""
                        <div style='background: {status_color}; color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;'>
                            <h4>✅ تم التسجيل مسبقاً</h4>
                            <p>الحالة: <strong>{current_status}</strong></p>
                            <p>صالحة حتى: <strong>{expiry_time.strftime('%H:%M')}</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("🔄 تغيير الحالة", use_container_width=True, type="secondary"):
                            today = datetime.datetime.now().strftime("%Y-%m-%d")
                            st.session_state.attendance_df = st.session_state.attendance_df[
                                ~((st.session_state.attendance_df["id"] == student_id) & 
                                  (st.session_state.attendance_df["date"] == today))
                            ]
                            st.success("✅ تم إعادة تعيين حالتك")
                            st.rerun()
                    else:
                        st.markdown("<h4 style='text-align: center; color: #2c3e50;'>اختر حالتك اليوم:</h4>", unsafe_allow_html=True)
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("✅ سأحضر اليوم", use_container_width=True, type="primary"):
                                now = datetime.datetime.now()
                                new_entry = pd.DataFrame([{
                                    "id": student["id"],
                                    "name": student["name"], 
                                    "grade": student["grade"],
                                    "bus": student["bus"],
                                    "status": "قادم",
                                    "time": now.strftime("%H:%M"),
                                    "date": now.strftime("%Y-%m-%d"),
                                    "expiry_time": (now + datetime.timedelta(hours=12)).strftime("%Y-%m-%d %H:%M:%S")
                                }])
                                
                                st.session_state.attendance_df = pd.concat([
                                    st.session_state.attendance_df, new_entry
                                ], ignore_index=True)
                                
                                st.balloons()
                                st.success(f"🎉 تم التسجيل بنجاح! أنت قادم اليوم")
                                add_notification(f"طالب جديد سجل حضوره: {student['name']} - الباص {student['bus']}")
                                
                        with col_b:
                            if st.button("❌ لن أحضر اليوم", use_container_width=True, type="secondary"):
                                now = datetime.datetime.now()
                                new_entry = pd.DataFrame([{
                                    "id": student["id"],
                                    "name": student["name"], 
                                    "grade": student["grade"],
                                    "bus": student["bus"],
                                    "status": "لن يأتي",
                                    "time": now.strftime("%H:%M"),
                                    "date": now.strftime("%Y-%m-%d"),
                                    "expiry_time": (now + datetime.timedelta(hours=12)).strftime("%Y-%m-%d %H:%M:%S")
                                }])
                                
                                st.session_state.attendance_df = pd.concat([
                                    st.session_state.attendance_df, new_entry
                                ], ignore_index=True)
                                
                                st.success(f"📝 تم التسجيل بنجاح! لن تحضر اليوم")
                                add_notification(f"طالب أعلن عدم حضوره: {student['name']} - الباص {student['bus']}")
                
                else:
                    st.error("❌ لم يتم العثور على الطالب")
                    st.info("💡 جرب أحد هذه الأرقام: 1001, 1002, 1003, 1004, 1005, 1006")
            
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='text-align: center; margin-bottom: 1rem;'><h3>📊 إحصائيات اليوم</h3></div>", unsafe_allow_html=True)
        
        stats = calculate_attendance_stats()
        
        # إحصائيات بطريقة جديدة
        st.markdown(f"""
        <div class='stat-card'>
            <h3 style='color: #667eea; margin-bottom: 0.5rem;'>👥</h3>
            <h2 style='color: #2c3e50; margin: 0;'>{stats['total']}</h2>
            <p style='color: #666; margin: 0;'>إجمالي المسجلين</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='stat-card'>
            <h3 style='color: #51cf66; margin-bottom: 0.5rem;'>✅</h3>
            <h2 style='color: #2c3e50; margin: 0;'>{stats['coming']}</h2>
            <p style='color: #666; margin: 0;'>الحضور المتوقع</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='stat-card'>
            <h3 style='color: #ffd43b; margin-bottom: 0.5rem;'>📈</h3>
            <h2 style='color: #2c3e50; margin: 0;'>{stats['percentage']:.1f}%</h2>
            <p style='color: #666; margin: 0;'>نسبة الحضور</p>
        </div>
        """, unsafe_allow_html=True)
        
        if stats["total"] > 0:
            st.info(f"📊 حتى الآن: {stats['coming']} طالب مؤكد الحضور")

# ===== صفحة السائق =====
elif st.session_state.page == "driver":
    st.subheader("🚌 لوحة تحكم السائق")
    
    if not st.session_state.driver_logged_in:
        col1, col2 = st.columns(2)
        with col1:
            bus_number = st.selectbox("اختر الباص", ["1", "2", "3"])
        with col2:
            password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور...")
        
        if st.button("تسجيل الدخول", type="primary", use_container_width=True):
            if password == bus_passwords.get(bus_number, ""):
                st.session_state.driver_logged_in = True
                st.session_state.current_bus = bus_number
                st.success("✅ تم الدخول بنجاح")
                st.rerun()
            else:
                st.error("❌ كلمة مرور غير صحيحة")
    else:
        st.success(f"✅ تم الدخول بنجاح - الباص رقم {st.session_state.current_bus}")
        
        if st.button("تسجيل الخروج", type="secondary"):
            st.session_state.driver_logged_in = False
            st.rerun()
        
        # عرض طلاب الباص
        st.subheader(f"📋 قائمة الطلاب - الباص {st.session_state.current_bus}")
        
        bus_students = st.session_state.students_df[
            st.session_state.students_df["bus"] == st.session_state.current_bus
        ]
        
        if not bus_students.empty:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            
            if not st.session_state.attendance_df.empty and "date" in st.session_state.attendance_df.columns:
                today_attendance = st.session_state.attendance_df[
                    (st.session_state.attendance_df["date"] == today) & 
                    (st.session_state.attendance_df["bus"] == st.session_state.current_bus)
                ]
            else:
                today_attendance = pd.DataFrame()
            
            coming_students = today_attendance[today_attendance["status"] == "قادم"] if not today_attendance.empty else pd.DataFrame()
            
            # الإحصائيات
            col1, col2 = st.columns(2)
            with col1:
                st.metric("الطلاب القادمون", len(coming_students))
            with col2:
                st.metric("إجمالي طلاب الباص", len(bus_students))
            
            # الطلاب القادمون
            if not coming_students.empty:
                st.subheader("🎒 الطلاب القادمون اليوم:")
                for _, student in coming_students.iterrows():
                    st.success(f"✅ **{student['name']}** - {student['grade']} - الساعة: {student['time']}")
            else:
                st.info("🚫 لا يوجد طلاب قادمين اليوم")
            
            # جميع طلاب الباص
            st.subheader("👥 جميع طلاب الباص:")
            for _, student in bus_students.iterrows():
                if not today_attendance.empty:
                    student_status = today_attendance[today_attendance["id"] == student["id"]]
                    status_icon = "✅" if not student_status.empty and student_status.iloc[0]["status"] == "قادم" else "❌"
                    status_text = "قادم" if not student_status.empty and student_status.iloc[0]["status"] == "قادم" else "لم يسجل"
                else:
                    status_icon = "❌"
                    status_text = "لم يسجل"
                
                st.write(f"{status_icon} **{student['name']}** - {student['grade']} - الحالة: {status_text}")

# ===== صفحة أولياء الأمور =====
elif st.session_state.page == "parents":
    st.subheader("👨‍👩‍👧 بوابة أولياء الأمور")
    
    student_id = st.text_input("أدخل رقم الوزارة الخاص بابنك/ابنتك", placeholder="مثال: 1001")
    if student_id:
        student_info = st.session_state.students_df[
            st.session_state.students_df["id"].astype(str) == str(student_id).strip()
        ]
        
        if not student_info.empty:
            student = student_info.iloc[0]
            st.success(f"🎉 تم العثور على الطالب: {student['name']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 متابعة الحضور")
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                
                if not st.session_state.attendance_df.empty and "date" in st.session_state.attendance_df.columns:
                    today_status = st.session_state.attendance_df[
                        (st.session_state.attendance_df["id"] == student["id"]) & 
                        (st.session_state.attendance_df["date"] == today)
                    ]
                else:
                    today_status = pd.DataFrame()
                
                if not today_status.empty:
                    status = today_status.iloc[0]["status"]
                    time = today_status.iloc[0]["time"]
                    status_display = "قادم 🎒" if status == "قادم" else "لن يأتي ❌"
                    st.success(f"**آخر حالة:** {status_display}\n**آخر تحديث:** {time}")
                else:
                    st.info("لا توجد بيانات حضور لهذا اليوم")
            
            with col2:
                st.subheader("🚌 معلومات الباص")
                st.info(f"""
                **رقم الباص:** {student['bus']}
                **وقت الصباح التقريبي:** 7:00 صباحاً
                **وقت الظهيرة التقريبي:** 2:00 ظهراً
                **هاتف ولي الأمر:** {student['parent_phone']}
                """)
        else:
            st.error("❌ لم يتم العثور على الطالب")

# ===== صفحة الإدارة =====
elif st.session_state.page == "admin":
    st.subheader("🏫 لوحة تحكم الإدارة")
    
    admin_password = st.text_input("كلمة مرور الإدارة", type="password", placeholder="أدخل كلمة المرور...")
    if admin_password == admin_pass:
        st.success("✅ تم الدخول بنجاح")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 لوحة التحكم", 
            "📋 بيانات الحضور", 
            "👥 إدارة الطلاب", 
            "⭐ نظام التقييم"
        ])
        
        with tab1:
            st.subheader("📊 لوحة التحكم")
            stats = calculate_attendance_stats()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("إجمالي الطلاب", len(st.session_state.students_df))
            with col2:
                st.metric("الحاضرون اليوم", stats["coming"])
            with col3:
                st.metric("نسبة الحضور", f"{stats['percentage']:.1f}%")
            with col4:
                st.metric("الباصات العاملة", 3)
            
            # مخططات
            if not st.session_state.attendance_df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    bus_distribution = st.session_state.attendance_df["bus"].value_counts()
                    fig1 = px.pie(bus_distribution, values=bus_distribution.values, 
                                names=bus_distribution.index, title="توزيع الطلاب على الباصات")
                    st.plotly_chart(fig1)
        
        with tab2:
            st.subheader("📋 بيانات الحضور")
            if not st.session_state.attendance_df.empty:
                st.dataframe(st.session_state.attendance_df)
            else:
                st.info("لا توجد بيانات حضور")
        
        with tab3:
            st.subheader("👥 إدارة الطلاب")
            st.dataframe(st.session_state.students_df)
            
            with st.expander("➕ إضافة طالب جديد"):
                with st.form("add_student"):
                    new_id = st.text_input("ID")
                    new_name = st.text_input("اسم الطالب")
                    new_grade = st.text_input("الصف")
                    new_bus = st.text_input("رقم الباص")
                    new_phone = st.text_input("هاتف ولي الأمر")
                    
                    if st.form_submit_button("إضافة"):
                        new_student = pd.DataFrame([{
                            "id": new_id, "name": new_name, "grade": new_grade,
                            "bus": new_bus, "parent_phone": new_phone
                        }])
                        st.session_state.students_df = pd.concat([
                            st.session_state.students_df, new_student
                        ], ignore_index=True)
                        st.success("✅ تم إضافة الطالب بنجاح")
        
        with tab4:
            st.subheader("⭐ نظام التقييم")
            
            if not st.session_state.ratings_df.empty:
                st.subheader("📊 إحصائيات التقييمات")
                
                # إحصائيات التقييمات
                average_rating = st.session_state.ratings_df["rating"].mean()
                total_ratings = len(st.session_state.ratings_df)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("متوسط التقييم", f"{average_rating:.1f}/5")
                with col2:
                    st.metric("إجمالي التقييمات", total_ratings)
                
                # مخطط التقييمات
                rating_dist = st.session_state.ratings_df["rating"].value_counts().sort_index()
                fig = px.bar(rating_dist, x=rating_dist.index, y=rating_dist.values,
                            title="توزيع التقييمات", labels={'x': 'التقييم', 'y': 'عدد التقييمات'})
                st.plotly_chart(fig)
                
                st.subheader("📋 جميع التقييمات")
                st.dataframe(st.session_state.ratings_df)
            else:
                st.info("لا توجد تقييمات حتى الآن")
    
    elif admin_password and admin_password != admin_pass:
        st.error("❌ كلمة مرور غير صحيحة")

# ===== صفحة الطقس =====
elif st.session_state.page == "weather":
    st.subheader("🌦️ توقعات الطقس")
    
    weather_data = get_weather()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>🌡️ درجة الحرارة</h3>
            <h2>{weather_data['temp']}°C</h2>
            <p>{weather_data['condition_ar']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>💧 الرطوبة</h3>
            <h2>{weather_data['humidity']}%</h2>
            <p>الرطوبة النسبية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>💨 سرعة الرياح</h3>
            <h2>{weather_data['wind_speed']} km/h</h2>
            <p>سرعة الرياح</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("""
    **تأثير الطقس على الحضور:**
    - ☀️ طقس مشمس: نسبة حضور عالية (95%)
    - 🌧️ طقس ممطر: نسبة حضور متوسطة (85%) 
    - 💨 طقس عاصف: نسبة حضور جيدة (90%)
    """)

# ===== صفحة حول النظام =====
elif st.session_state.page == "about":
    st.subheader("ℹ️ حول النظام")
    
    st.markdown("### 🚀 مميزات النظام")
    
    features = [
        "🌱 نظام صديق للبيئة",
        "⏱️ مراقبة في الوقت الحقيقي", 
        "📊 تحليلات ذكية",
        "📱 متعدد المنصات",
        "🎯 سهل الاستخدام",
        "🔒 نظام آمن",
        "💰 موفر للتكاليف",
        "⏰ موفر للوقت",
        "👨‍👩‍👧‍👦 تواصل مع أولياء الأمور",
        "🚍 تتبع الباصات",
        "📝 إدارة الحضور",
        "🌦️ تنبيهات الطقس",
        "📈 إنشاء التقارير"
    ]
    
    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='feature-card'>
                <h4>{feature}</h4>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### 👨‍💻 فريق التطوير")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='team-card-blue'>
            <h3>💻 المطور الرئيسي</h3>
            <h2>إياد مصطفى</h2>
            <p>المسؤول عن برمجة النظام بالكامل</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='team-card-green'>
            <h3>🎨 مصمم الجرافيك</h3>
            <h2>ايمن جلال</h2>
            <p>مصمم الواجهات والمؤثرات البصرية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='team-card-orange'>
            <h3>👨‍🏫 المشرف</h3>
            <h2>قسم النادي البيئي</h2>
            <p>المشرف على المشروع</p>
        </div>
        """, unsafe_allow_html=True)
    
    # قسم التقييم في صفحة حول النظام
    st.markdown("### ⭐ قيم النظام")
    
    st.markdown("""
    <div class='rating-card'>
        <h3>كيف تقيم تجربتك مع النظام؟</h3>
        <p>شاركنا برأيك لمساعدتنا في التحسين</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("rating_form"):
        rating = st.slider("تقييمك للنظام", 1, 5, 5, help="1 = سيء, 5 = ممتاز")
        comments = st.text_area("ملاحظاتك أو اقتراحاتك")
        
        if st.form_submit_button("إرسال التقييم", type="primary"):
            add_rating(rating, comments)
            st.success("🎉 شكراً لتقييمك النظام! تم إرسال تقييمك بنجاح")
            st.info("📊 يمكنك رؤية إحصائيات التقييمات في صفحة الإدارة")

# ===== التذييل المطور =====
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])

with footer_col1:
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <h4 style='color: #2c3e50; margin-bottom: 1rem;'>🚍 نظام الباص الذكي</h4>
        <p style='margin: 0.5rem 0;'>مدرسة المنيرة الخاصة - أبوظبي</p>
        <p style='margin: 0.5rem 0;'>© 2024 جميع الحقوق محفوظة</p>
        <p style='margin: 0.5rem 0;'>تم التطوير بواسطة: إياد مصطفى | التصميم: ايمن جلال | الإشراف: قسم النادي البيئي</p>
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    if st.session_state.notifications:
        notification_count = len(st.session_state.notifications)
        if st.button(f"🔔 الإشعارات ({notification_count})", use_container_width=True):
            with st.expander("📋 الإشعارات الحديثة", expanded=True):
                for notification in st.session_state.notifications[-5:]:
                    st.write(f"⏰ {notification['time']}: {notification['message']}")

with footer_col3:
    if st.button("🔄 تحديث البيانات", use_container_width=True):
        st.rerun()
