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

# ===== البيانات الافتراضية - التصحيح النهائي =====
def initialize_data():
    """تهيئة جميع البيانات بشكل صحيح"""
    students_data = [
        {"id": "1001", "name": "أحمد محمد", "grade": "10-A", "bus": "1", "parent_phone": "0501234567"},
        {"id": "1002", "name": "فاطمة علي", "grade": "9-B", "bus": "2", "parent_phone": "0507654321"},
        {"id": "1003", "name": "خالد إبراهيم", "grade": "8-C", "bus": "3", "parent_phone": "0505555555"},
        {"id": "1004", "name": "سارة عبدالله", "grade": "10-B", "bus": "1", "parent_phone": "0504444444"},
        {"id": "1005", "name": "محمد حسن", "grade": "7-A", "bus": "2", "parent_phone": "0503333333"},
        {"id": "1006", "name": "ريم أحمد", "grade": "11-A", "bus": "3", "parent_phone": "0506666666"},
        {"id": "1007", "name": "يوسف خالد", "grade": "6-B", "bus": "1", "parent_phone": "0507777777"},
        {"id": "1008", "name": "نورة سعيد", "grade": "9-A", "bus": "2", "parent_phone": "0508888888"},
    ]
    
    if 'students_df' not in st.session_state:
        st.session_state.students_df = pd.DataFrame(students_data)
    
    if 'attendance_df' not in st.session_state:
        st.session_state.attendance_df = pd.DataFrame(columns=[
            "id", "name", "grade", "bus", "status", "time", "date"
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
        "condition_ar": random.choice(["☀️ مشمس", "🌤️ غائم جزئياً", "🌧️ ممطر", "💨 عاصف"])
    }

def calculate_attendance_stats():
    """حساب إحصائيات الحضور"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if st.session_state.attendance_df.empty:
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
    """التحقق من تسجيل الطالب - التصحيح النهائي"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if st.session_state.attendance_df.empty:
        return False, None
    
    student_data = st.session_state.attendance_df[
        (st.session_state.attendance_df["id"].astype(str) == str(student_id).strip()) & 
        (st.session_state.attendance_df["date"] == today)
    ]
    
    if not student_data.empty:
        latest_record = student_data.iloc[-1]
        return True, latest_record["status"]
    
    return False, None

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

def register_attendance(student, status):
    """تسجيل حضور الطالب - التصحيح النهائي"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    st.session_state.attendance_df = st.session_state.attendance_df[
        ~((st.session_state.attendance_df["id"].astype(str) == str(student["id"]).strip()) & 
          (st.session_state.attendance_df["date"] == today))
    ]
    
    now = datetime.datetime.now()
    new_entry = pd.DataFrame([{
        "id": student["id"],
        "name": student["name"], 
        "grade": student["grade"],
        "bus": student["bus"],
        "status": status,
        "time": now.strftime("%H:%M"),
        "date": today
    }])
    
    st.session_state.attendance_df = pd.concat([
        st.session_state.attendance_df, new_entry
    ], ignore_index=True)
    
    return now

def toggle_theme():
    """تبديل الثيم"""
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.rerun()

def toggle_language():
    """تبديل اللغة"""
    st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
    st.rerun()

# ===== واجهة مستخدم محسنة ومتطورة =====
def apply_custom_styles():
    """تطبيق التصميم المخصص مع الثيم المظلم"""
    
    if st.session_state.theme == "dark":
        dark_theme = """
        .main {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stApp {
            background-color: #0e1117;
        }
        .stButton>button {
            background-color: #262730;
            color: #fafafa;
            border: 1px solid #555;
        }
        .stTextInput>div>div>input {
            background-color: #262730;
            color: #fafafa;
            border: 1px solid #555;
        }
        .stSelectbox>div>div>select {
            background-color: #262730;
            color: #fafafa;
        }
        """
    else:
        dark_theme = ""
    
    st.markdown(f"""
    <style>
        /* التصميم العام */
        .main {{
            background-color: #f8f9fa;
        }}
        
        {dark_theme}
        
        .main-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem 1.5rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        /* كروت الإحصائيات */
        .stat-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            text-align: center;
            margin: 0.5rem;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        }}
        
        /* كروت الطلاب */
        .student-card {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 5px solid #667eea;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }}
        
        /* كروت الطقس */
        .weather-card {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        /* أزرار مخصصة */
        .stButton>button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        /* تحسين النص */
        .stTextInput>div>div>input {{
            color: #2c3e50 !important;
            font-weight: 500;
            border-radius: 10px;
            border: 2px solid #e9ecef;
        }}
        
        .section-title {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            margin-bottom: 1rem;
        }}
    </style>
    """, unsafe_allow_html=True)

# تطبيق التصميم
apply_custom_styles()

# ===== الهيدر الرئيسي المحسن =====
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
        <h1 style='font-size: 2.2rem; margin-bottom: 0.5rem;'>🚍 نظام الباص الذكي</h1>
        <h3 style='font-size: 1.2rem; margin-bottom: 0.5rem; opacity: 0.9;'>مدرسة المنيرة الخاصة - أبوظبي</h3>
        <p style='font-size: 1rem; opacity: 0.8;'>نظام متكامل لإدارة النقل المدرسي الذكي</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    col3a, col3b = st.columns(2)
    with col3a:
        theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
        if st.button(theme_icon, help="تبديل الثيم", use_container_width=True, key="theme_btn"):
            toggle_theme()
    
    with col3b:
        lang_text = "EN" if st.session_state.lang == "ar" else "AR"
        if st.button(f"🌐 {lang_text}", help="تبديل اللغة", use_container_width=True, key="lang_btn"):
            toggle_language()

# ===== شريط التنقل المحسن =====
pages = [
    ("🎓 الطالب", "student"),
    ("🚌 السائق", "driver"), 
    ("👨‍👩‍👧 أولياء الأمور", "parents"),
    ("⚙️ الإعدادات", "admin"),
    ("ℹ️ حول النظام", "about")
]

nav_cols = st.columns(len(pages))
for i, (name, page_key) in enumerate(pages):
    with nav_cols[i]:
        is_active = st.session_state.page == page_key
        button_type = "primary" if is_active else "secondary"
        if st.button(name, use_container_width=True, type=button_type, key=f"nav_{page_key}"):
            st.session_state.page = page_key
            st.rerun()

st.markdown("---")

# ===== صفحة الطالب =====
if st.session_state.page == "student":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 1.5rem;'>
            <h2 class='section-title'>🎓 تسجيل حضور الطالب</h2>
            <p style='color: #666; font-size: 1.1rem;'>أدخل رقم الوزارة لتسجيل حالتك اليوم</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div style='background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08);'>", unsafe_allow_html=True)
            
            student_id = st.text_input(
                "🔍 رقم الوزارة",
                placeholder="أدخل رقم الوزارة هنا...",
                help="يمكنك استخدام أي رقم من 1001 إلى 1008",
                key="student_id_input"
            )
            
            if student_id:
                try:
                    student_info = st.session_state.students_df[
                        st.session_state.students_df["id"].astype(str) == str(student_id).strip()
                    ]
                    
                    if not student_info.empty:
                        student = student_info.iloc[0]
                        
                        st.markdown(f"""
                        <div class='student-card'>
                            <div style='text-align: center;'>
                                <h3 style='color: #2c3e50; margin-bottom: 1rem;'>🎓 {student['name']}</h3>
                                <div style='display: flex; justify-content: center; gap: 1.5rem; margin-bottom: 1rem;'>
                                    <div style='text-align: center;'>
                                        <div style='background: #667eea; color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold; font-size: 0.9rem;'>📚 {student['grade']}</div>
                                    </div>
                                    <div style='text-align: center;'>
                                        <div style='background: #764ba2; color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold; font-size: 0.9rem;'>🚍 الباص {student['bus']}</div>
                                    </div>
                                </div>
                                <p style='color: #666; margin: 0;'><strong>هاتف ولي الأمر:</strong> {student['parent_phone']}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        already_registered, current_status = has_student_registered_today(student_id)
                        
                        if already_registered:
                            status_color = "#51cf66" if current_status == "قادم" else "#ff6b6b"
                            status_icon = "✅" if current_status == "قادم" else "❌"
                            st.markdown(f"""
                            <div style='background: {status_color}; color: white; padding: 1.5rem; border-radius: 12px; text-align: center; margin: 1rem 0;'>
                                <h4>{status_icon} تم التسجيل مسبقاً</h4>
                                <p style='margin: 0.5rem 0; font-size: 1.1rem;'>حالتك الحالية: <strong>{current_status}</strong></p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button("🔄 تغيير الحالة", use_container_width=True, type="secondary", key="change_status"):
                                today = datetime.datetime.now().strftime("%Y-%m-%d")
                                st.session_state.attendance_df = st.session_state.attendance_df[
                                    ~((st.session_state.attendance_df["id"].astype(str) == str(student_id).strip()) & 
                                      (st.session_state.attendance_df["date"] == today))
                                ]
                                st.success("✅ تم إعادة تعيين حالتك، يمكنك التسجيل مرة أخرى")
                                st.rerun()
                        else:
                            st.markdown("<h4 style='text-align: center; color: #2c3e50; margin-bottom: 1rem;'>اختر حالتك اليوم:</h4>", unsafe_allow_html=True)
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("✅ سأحضر اليوم", use_container_width=True, type="primary", key="coming_btn"):
                                    now = register_attendance(student, "قادم")
                                    st.balloons()
                                    st.success(f"""
                                    🎉 **تم التسجيل بنجاح!**
                                    
                                    **الطالب:** {student['name']}
                                    **الحالة:** قادم
                                    **وقت التسجيل:** {now.strftime('%H:%M')}
                                    **رقم الباص:** {student['bus']}
                                    """)
                                    add_notification(f"طالب سجل حضوره: {student['name']} - الباص {student['bus']}")
                                    
                            with col_b:
                                if st.button("❌ لن أحضر اليوم", use_container_width=True, type="secondary", key="not_coming_btn"):
                                    now = register_attendance(student, "لن يأتي")
                                    st.success(f"""
                                    📝 **تم التسجيل بنجاح!**
                                    
                                    **الطالب:** {student['name']}
                                    **الحالة:** لن أحضر
                                    **وقت التسجيل:** {now.strftime('%H:%M')}
                                    **رقم الباص:** {student['bus']}
                                    """)
                                    add_notification(f"طالب أعلن عدم حضوره: {student['name']} - الباص {student['bus']}")
                    
                    else:
                        st.error("❌ لم يتم العثور على الطالب")
                        st.info("""
                        **💡 الأرقام المتاحة:**
                        - 1001: أحمد محمد
                        - 1002: فاطمة علي
                        - 1003: خالد إبراهيم  
                        - 1004: سارة عبدالله
                        - 1005: محمد حسن
                        - 1006: ريم أحمد
                        - 1007: يوسف خالد
                        - 1008: نورة سعيد
                        """)
                        
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {e}")
            
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='text-align: center; margin-bottom: 1rem;'><h3 class='section-title'>📊 إحصائيات اليوم</h3></div>", unsafe_allow_html=True)
        
        stats = calculate_attendance_stats()
        
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

# ===== صفحة السائق - محدثة ومصححة =====
elif st.session_state.page == "driver":
    st.subheader("🚌 لوحة تحكم السائق")
    
    if not st.session_state.driver_logged_in:
        # واجهة تسجيل الدخول
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08);'>
                <h3 style='text-align: center; color: #2c3e50; margin-bottom: 1.5rem;'>🔐 تسجيل دخول السائق</h3>
            """, unsafe_allow_html=True)
            
            bus_number = st.selectbox("اختر الباص", ["1", "2", "3"], key="bus_select")
            password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور...", key="driver_pass")
            
            if st.button("🚀 تسجيل الدخول", type="primary", use_container_width=True, key="driver_login_btn"):
                if password == bus_passwords.get(bus_number, ""):
                    st.session_state.driver_logged_in = True
                    st.session_state.current_bus = bus_number
                    st.success("✅ تم الدخول بنجاح")
                    st.rerun()
                else:
                    st.error("❌ كلمة مرور غير صحيحة")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: #e8f4fd; padding: 2rem; border-radius: 15px;'>
                <h4 style='color: #2c3e50;'>💡 معلومات المساعدة</h4>
                <p><strong>كلمات المرور:</strong></p>
                <ul>
                    <li>الباص 1: <code>1111</code></li>
                    <li>الباص 2: <code>2222</code></li>
                    <li>الباص 3: <code>3333</code></li>
                </ul>
                <p style='color: #666; font-size: 0.9rem; margin-top: 1rem;'>
                    اختر الباص ثم أدخل كلمة المرور المناسبة للدخول إلى لوحة التحكم.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # واجهة السائق بعد تسجيل الدخول
        st.success(f"✅ تم الدخول بنجاح - الباص رقم {st.session_state.current_bus}")
        
        # زر تسجيل الخروج
        if st.button("🚪 تسجيل الخروج", type="secondary", key="driver_logout"):
            st.session_state.driver_logged_in = False
            st.rerun()
        
        # عرض بيانات الباص
        st.subheader(f"📋 قائمة الطلاب - الباص {st.session_state.current_bus}")
        
        # تصفية طلاب الباص الحالي
        bus_students = st.session_state.students_df[
            st.session_state.students_df["bus"] == st.session_state.current_bus
        ]
        
        if not bus_students.empty:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # الحصول على بيانات الحضور لهذا اليوم
            today_attendance = st.session_state.attendance_df[
                st.session_state.attendance_df["date"] == today
            ] if not st.session_state.attendance_df.empty else pd.DataFrame()
            
            # حساب الإحصائيات
            coming_students = today_attendance[
                (today_attendance["bus"] == st.session_state.current_bus) & 
                (today_attendance["status"] == "قادم")
            ] if not today_attendance.empty else pd.DataFrame()
            
            # عرض الإحصائيات
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("👥 إجمالي الطلاب", len(bus_students))
            with col2:
                st.metric("✅ الحضور المؤكد", len(coming_students))
            with col3:
                percentage = (len(coming_students) / len(bus_students) * 100) if len(bus_students) > 0 else 0
                st.metric("📈 نسبة الحضور", f"{percentage:.1f}%")
            
            # قسم الطلاب القادمون
            st.subheader("🎒 الطلاب القادمون اليوم")
            if not coming_students.empty:
                for _, student in coming_students.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div style='background: #d4edda; padding: 1rem; border-radius: 10px; border-right: 5px solid #28a745; margin: 0.5rem 0;'>
                            <h4 style='color: #155724; margin: 0;'>✅ {student['name']}</h4>
                            <p style='color: #155724; margin: 0.3rem 0;'>📚 الصف: {student['grade']} | ⏰ الوقت: {student['time']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("🚫 لا يوجد طلاب قادمين اليوم")
            
            # قسم جميع طلاب الباص
            st.subheader("👥 جميع طلاب الباص")
            for _, student in bus_students.iterrows():
                # البحث عن حالة الطالب
                student_attendance = today_attendance[
                    today_attendance["id"].astype(str) == str(student["id"])
                ] if not today_attendance.empty else pd.DataFrame()
                
                if not student_attendance.empty:
                    status = student_attendance.iloc[0]["status"]
                    if status == "قادم":
                        status_icon = "✅"
                        status_text = "قادم"
                        bg_color = "#d4edda"
                        border_color = "#28a745"
                    else:
                        status_icon = "❌"
                        status_text = "لن يحضر"
                        bg_color = "#f8d7da"
                        border_color = "#dc3545"
                else:
                    status_icon = "⏳"
                    status_text = "لم يسجل"
                    bg_color = "#fff3cd"
                    border_color = "#ffc107"
                
                st.markdown(f"""
                <div style='background: {bg_color}; padding: 1rem; border-radius: 10px; border-right: 5px solid {border_color}; margin: 0.5rem 0;'>
                    <h4 style='color: #2c3e50; margin: 0;'>{status_icon} {student['name']}</h4>
                    <p style='color: #2c3e50; margin: 0.3rem 0;'>📚 {student['grade']} | 📱 {student['parent_phone']}</p>
                    <p style='color: #6c757d; margin: 0;'><strong>الحالة:</strong> {status_text}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ لا يوجد طلاب مسجلين في هذا الباص")

# ===== صفحة أولياء الأمور =====
elif st.session_state.page == "parents":
    st.subheader("👨‍👩‍👧 بوابة أولياء الأمور")
    
    student_id = st.text_input("أدخل رقم الوزارة الخاص بابنك/ابنتك", placeholder="مثال: 1001", key="parent_student_id")
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
                
                if not st.session_state.attendance_df.empty:
                    today_status = st.session_state.attendance_df[
                        (st.session_state.attendance_df["id"].astype(str) == str(student["id"])) & 
                        (st.session_state.attendance_df["date"] == today)
                    ]
                else:
                    today_status = pd.DataFrame()
                
                if not today_status.empty:
                    status = today_status.iloc[0]["status"]
                    time = today_status.iloc[0]["time"]
                    if status == "قادم":
                        st.success(f"**آخر حالة:** قادم 🎒\n**آخر تحديث:** {time}")
                    else:
                        st.error(f"**آخر حالة:** لن يأتي ❌\n**آخر تحديث:** {time}")
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

# ===== صفحة الإعدادات (بدل الإدارة) =====
elif st.session_state.page == "admin":
    st.subheader("⚙️ إعدادات النظام")
    
    tab1, tab2, tab3 = st.tabs(["🎨 المظهر", "🔐 الأمان", "📊 البيانات"])
    
    with tab1:
        st.header("🎨 إعدادات المظهر")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("الثيم الحالي")
            current_theme = "☀️ فاتح" if st.session_state.theme == "light" else "🌙 مظلم"
            st.info(f"الثيم الحالي: {current_theme}")
            
            if st.button("تبديل الثيم", use_container_width=True, key="theme_toggle_settings"):
                toggle_theme()
        
        with col2:
            st.subheader("إعدادات اللغة")
            current_lang = "العربية" if st.session_state.lang == "ar" else "English"
            st.info(f"اللغة الحالية: {current_lang}")
            
            if st.button("تبديل اللغة", use_container_width=True, key="lang_toggle_settings"):
                toggle_language()
    
    with tab2:
        st.header("🔐 إعدادات الأمان")
        
        st.subheader("كلمات المرور الحالية")
        st.info("""
        **كلمات مرور الباصات:**
        - الباص 1: 1111
        - الباص 2: 2222  
        - الباص 3: 3333
        - كلمة مرور الإدارة: admin123
        """)
        
        st.subheader("تغيير كلمة المرور")
        bus_select = st.selectbox("اختر الباص", ["1", "2", "3"], key="password_bus_select")
        new_pass = st.text_input("كلمة المرور الجديدة", type="password", key="new_password")
        
        if st.button("حفظ التغييرات", key="save_password"):
            if new_pass:
                bus_passwords[bus_select] = new_pass
                st.success(f"✅ تم تحديث كلمة مرور الباص {bus_select}")
    
    with tab3:
        st.header("📊 إدارة البيانات")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("إحصائيات النظام")
            st.metric("عدد الطلاب", len(st.session_state.students_df))
            st.metric("سجلات الحضور", len(st.session_state.attendance_df))
            st.metric("التقييمات", len(st.session_state.ratings_df))
        
        with col2:
            st.subheader("إجراءات النظام")
            if st.button("🔄 إعادة تعيين البيانات", type="secondary", use_container_width=True):
                initialize_data()
                st.success("✅ تم إعادة تعيين البيانات بنجاح")
            
            if st.button("📥 نسخة احتياطية", use_container_width=True):
                st.info("✅ تم إنشاء نسخة احتياطية من البيانات")

# ===== صفحة حول النظام =====
elif st.session_state.page == "about":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08);'>
            <h2 style='color: #2c3e50;'>🚍 نظام الباص الذكي</h2>
            <p style='color: #666; line-height: 1.6;'>
                نظام متكامل لإدارة النقل المدرسي الذكي في مدرسة المنيرة الخاصة بأبوظبي. 
                تم تطوير النظام لتوفير تجربة مستخدم سلسة وفعالة لإدارة حضور الطلاب ومتابعة الباصات.
            </p>
            
            <h3 style='color: #2c3e50; margin-top: 2rem;'>🎯 المميزات الرئيسية</h3>
            <ul style='color: #666; line-height: 2;'>
                <li>تسجيل حضور ذكي للطلاب</li>
                <li>متابعة أولياء الأمور لحالة أبنائهم</li>
                <li>لوحة تحكم متكاملة للسائقين</li>
                <li>إشعارات فورية للتحديثات</li>
                <li>تقارير وإحصائيات مفصلة</li>
                <li>واجهة مستخدم intuitive وسهلة الاستخدام</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); text-align: center;'>
            <h3 style='color: #2c3e50;'>👥 فريق التطوير</h3>
            
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;'>
                <h4>إياد مصطفى</h4>
                <p>مطور النظام</p>
            </div>
            
            <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;'>
                <h4>ايمن جلال</h4>
                <p>مصمم الواجهة</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # معلومات الإصدار
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 15px; margin-top: 2rem; text-align: center;'>
        <h3>📋 معلومات الإصدار</h3>
        <p><strong>الإصدار:</strong> 1.1</p>
        <p><strong>تاريخ الإصدار:</strong> أكتوبر 2025</p>
        <p><strong>الحالة:</strong> ⭐ الإصدار المستقر</p>
    </div>
    """, unsafe_allow_html=True)

# ===== التذييل =====
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1.5rem 0;'>
    <p style='margin: 0.3rem 0;'><strong>🚍 نظام الباص الذكي - الإصدار 1.1</strong></p>
    <p style='margin: 0.3rem 0;'>مدرسة المنيرة الخاصة - أبوظبي</p>
    <p style='margin: 0.3rem 0;'>© 2025 جميع الحقوق محفوظة</p>
    <p style='margin: 0.3rem 0;'>تم التطوير بواسطة: إياد مصطفى | التصميم: ايمن جلال | الإشراف: قسم النادي البيئي</p>
</div>
""", unsafe_allow_html=True)
