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
        "condition_ar": random.choice(["☀️ مشمس", "🌤️ غائم جزئياً", "🌧️ ممطر", "💨 عاصف"]),
        "condition_en": "Sunny"
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
    
    # البحث في البيانات - التأكد من المقارنة الصحيحة
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
    
    # إزالة أي تسجيل سابق لنفس الطالب في نفس اليوم
    st.session_state.attendance_df = st.session_state.attendance_df[
        ~((st.session_state.attendance_df["id"].astype(str) == str(student["id"]).strip()) & 
          (st.session_state.attendance_df["date"] == today))
    ]
    
    # إضافة التسجيل الجديد
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

def toggle_language():
    """تبديل اللغة"""
    st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"

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
            padding: 2.5rem 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }}
        
        .main-header::before {{
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 20px 20px;
            animation: float 20s infinite linear;
        }}
        
        @keyframes float {{
            0% {{ transform: translate(0, 0) rotate(0deg); }}
            100% {{ transform: translate(-20px, -20px) rotate(360deg); }}
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
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }}
        
        /* كروت الطلاب */
        .student-card {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 5px solid #667eea;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }}
        
        .student-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.12);
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
            position: relative;
            overflow: hidden;
        }}
        
        .weather-card::before {{
            content: "";
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.1);
            transform: rotate(30deg);
        }}
        
        /* كروت المميزات */
        .feature-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem 1rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .feature-card:hover {{
            transform: scale(1.05);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}
        
        /* كروت الفريق */
        .team-card-blue {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 2rem 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .team-card-green {{
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: white;
            padding: 2rem 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .team-card-orange {{
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
            padding: 2rem 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .team-card-blue:hover, .team-card-green:hover, .team-card-orange:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        }}
        
        /* كروت التقييم */
        .rating-card {{
            background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
            color: white;
            padding: 2rem 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        /* تحسين النص */
        .stTextInput>div>div>input {{
            color: #2c3e50 !important;
            font-weight: 500;
            border-radius: 10px;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
        }}
        
        .stTextInput>div>div>input:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
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
            position: relative;
            overflow: hidden;
        }}
        
        .stButton>button::before {{
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }}
        
        .stButton>button:hover::before {{
            left: 100%;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }}
        
        /* تحسينات التنقل */
        .nav-button {{
            transition: all 0.3s ease;
            border-radius: 10px;
        }}
        
        .nav-button:hover {{
            transform: translateY(-2px);
        }}
        
        /* تحسينات عامة */
        .section-title {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            margin-bottom: 1rem;
        }}
        
        /* أنيميشن للبطاقات */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .animate-card {{
            animation: fadeInUp 0.6s ease-out;
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
    <div class='weather-card animate-card'>
        <h3>🌡️ {weather_data['temp']}°C</h3>
        <p>{weather_data['condition_ar']}</p>
        <p>💧 {weather_data['humidity']}% | 💨 {weather_data['wind_speed']} km/h</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='main-header animate-card'>
        <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>🚍 نظام الباص الذكي المتطور</h1>
        <h3 style='font-size: 1.3rem; margin-bottom: 0.5rem; opacity: 0.95;'>مدرسة المنيرة الخاصة - أبوظبي</h3>
        <p style='font-size: 1.1rem; opacity: 0.85;'>نظام متكامل لإدارة النقل المدرسي الذكي والحديث</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    col3a, col3b, col3c = st.columns(3)
    with col3a:
        theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
        if st.button(theme_icon, help="تبديل الثيم", use_container_width=True, key="theme_btn"):
            toggle_theme()
            st.rerun()
    
    with col3b:
        lang_text = "EN" if st.session_state.lang == "ar" else "AR"
        if st.button(f"🌐 {lang_text}", help="تبديل اللغة", use_container_width=True, key="lang_btn"):
            toggle_language()
            st.rerun()
    
    with col3c:
        if st.button("🔔", help="الإشعارات", use_container_width=True):
            st.session_state.page = "notifications"

# ===== شريط التنقل المحسن =====
pages = [
    ("🎓 الطالب", "student"),
    ("🚌 السائق", "driver"), 
    ("👨‍👩‍👧 أولياء الأمور", "parents"),
    ("🏫 الإدارة", "admin"),
    ("🌦️ الطقس", "weather"),
    ("⚙️ النظام", "system"),
    ("ℹ️ حول", "about")
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

# ===== صفحة الطالب - التصحيح النهائي =====
if st.session_state.page == "student":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 1.5rem;'>
            <h2 class='section-title'>🎓 تسجيل حضور الطالب</h2>
            <p style='color: #666; font-size: 1.1rem;'>أدخل رقم الوزارة لتسجيل حالتك اليوم</p>
        </div>
        """, unsafe_allow_html=True)
        
        # بطاقة البحث
        with st.container():
            st.markdown("<div class='animate-card' style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08);'>", unsafe_allow_html=True)
            
            student_id = st.text_input(
                "🔍 رقم الوزارة",
                placeholder="أدخل رقم الوزارة هنا...",
                help="يمكنك استخدام أي رقم من 1001 إلى 1008",
                key="student_id_input"
            )
            
            if student_id:
                # البحث عن الطالب - التصحيح النهائي
                try:
                    student_info = st.session_state.students_df[
                        st.session_state.students_df["id"].astype(str) == str(student_id).strip()
                    ]
                    
                    if not student_info.empty:
                        student = student_info.iloc[0]
                        
                        st.markdown(f"""
                        <div class='student-card animate-card'>
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
                        
                        # التحقق من التسجيل المسبق
                        already_registered, current_status = has_student_registered_today(student_id)
                        
                        if already_registered:
                            status_color = "#51cf66" if current_status == "قادم" else "#ff6b6b"
                            status_icon = "✅" if current_status == "قادم" else "❌"
                            st.markdown(f"""
                            <div class='animate-card' style='background: {status_color}; color: white; padding: 1.5rem; border-radius: 12px; text-align: center; margin: 1rem 0;'>
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
                    st.info("يرجى إدخال رقم صحيح مثل: 1001, 1002, إلخ...")
            
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='text-align: center; margin-bottom: 1rem;'><h3 class='section-title'>📊 إحصائيات اليوم</h3></div>", unsafe_allow_html=True)
        
        stats = calculate_attendance_stats()
        
        st.markdown(f"""
        <div class='stat-card animate-card'>
            <h3 style='color: #667eea; margin-bottom: 0.5rem;'>👥</h3>
            <h2 style='color: #2c3e50; margin: 0;'>{stats['total']}</h2>
            <p style='color: #666; margin: 0;'>إجمالي المسجلين</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='stat-card animate-card'>
            <h3 style='color: #51cf66; margin-bottom: 0.5rem;'>✅</h3>
            <h2 style='color: #2c3e50; margin: 0;'>{stats['coming']}</h2>
            <p style='color: #666; margin: 0;'>الحضور المتوقع</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='stat-card animate-card'>
            <h3 style='color: #ffd43b; margin-bottom: 0.5rem;'>📈</h3>
            <h2 style='color: #2c3e50; margin: 0;'>{stats['percentage']:.1f}%</h2>
            <p style='color: #666; margin: 0;'>نسبة الحضور</p>
        </div>
        """, unsafe_allow_html=True)
        
        if stats["total"] > 0:
            st.info(f"📊 حتى الآن: {stats['coming']} طالب مؤكد الحضور")

# ===== صفحة السائق - التصحيح الكامل =====
elif st.session_state.page == "driver":
    st.subheader("🚌 لوحة تحكم السائق المتطورة")
    
    if not st.session_state.driver_logged_in:
        st.markdown("""
        <div class='animate-card' style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); text-align: center;'>
            <h3 style='color: #2c3e50; margin-bottom: 1.5rem;'>🔐 تسجيل دخول السائق</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            bus_number = st.selectbox("اختر الباص", ["1", "2", "3"], key="bus_select")
        with col2:
            password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور...", key="driver_pass")
        
        if st.button("🚀 تسجيل الدخول", type="primary", use_container_width=True):
            if password == bus_passwords.get(bus_number, ""):
                st.session_state.driver_logged_in = True
                st.session_state.current_bus = bus_number
                st.success("✅ تم الدخول بنجاح")
                st.rerun()
            else:
                st.error("❌ كلمة مرور غير صحيحة")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # معلومات المساعدة
        st.info("""
        **💡 معلومات المساعدة:**
        - الباص 1: كلمة المرور 1111
        - الباص 2: كلمة المرور 2222  
        - الباص 3: كلمة المرور 3333
        """)
        
    else:
        st.success(f"✅ تم الدخول بنجاح - الباص رقم {st.session_state.current_bus}")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🚪 تسجيل الخروج", type="secondary", use_container_width=True):
                st.session_state.driver_logged_in = False
                st.rerun()
        
        # عرض طلاب الباص - التصحيح النهائي
        st.subheader(f"📋 قائمة الطلاب - الباص {st.session_state.current_bus}")
        
        bus_students = st.session_state.students_df[
            st.session_state.students_df["bus"] == st.session_state.current_bus
        ]
        
        if not bus_students.empty:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # الحصول على بيانات الحضور لهذا اليوم
            if not st.session_state.attendance_df.empty:
                today_attendance = st.session_state.attendance_df[
                    st.session_state.attendance_df["date"] == today
                ]
            else:
                today_attendance = pd.DataFrame()
            
            # الطلاب القادمون
            coming_students = today_attendance[
                (today_attendance["bus"] == st.session_state.current_bus) & 
                (today_attendance["status"] == "قادم")
            ] if not today_attendance.empty else pd.DataFrame()
            
            # الإحصائيات
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("👥 إجمالي الطلاب", len(bus_students))
            with col2:
                st.metric("✅ الحضور المؤكد", len(coming_students))
            with col3:
                percentage = (len(coming_students) / len(bus_students) * 100) if len(bus_students) > 0 else 0
                st.metric("📈 نسبة الحضور", f"{percentage:.1f}%")
            
            # عرض الطلاب القادمون
            if not coming_students.empty:
                st.subheader("🎒 الطلاب القادمون اليوم:")
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
            
            # عرض جميع طلاب الباص
            st.subheader("👥 جميع طلاب الباص:")
            for _, student in bus_students.iterrows():
                # البحث عن حالة الطالب
                student_attendance = today_attendance[
                    today_attendance["id"].astype(str) == str(student["id"])
                ] if not today_attendance.empty else pd.DataFrame()
                
                if not student_attendance.empty:
                    status = student_attendance.iloc[0]["status"]
                    status_icon = "✅" if status == "قادم" else "❌"
                    status_text = "قادم" if status == "قادم" else "لن يحضر"
                    status_color = "#d4edda" if status == "قادم" else "#f8d7da"
                    border_color = "#28a745" if status == "قادم" else "#dc3545"
                else:
                    status_icon = "⏳"
                    status_text = "لم يسجل"
                    status_color = "#fff3cd"
                    border_color = "#ffc107"
                
                st.markdown(f"""
                <div style='background: {status_color}; padding: 1rem; border-radius: 10px; border-right: 5px solid {border_color}; margin: 0.5rem 0;'>
                    <h4 style='color: #2c3e50; margin: 0;'>{status_icon} {student['name']}</h4>
                    <p style='color: #2c3e50; margin: 0.3rem 0;'>📚 {student['grade']} | 🚍 الباص {student['bus']} | 📱 {student['parent_phone']}</p>
                    <p style='color: #6c757d; margin: 0;'><strong>الحالة:</strong> {status_text}</p>
                </div>
                """, unsafe_allow_html=True)

# ===== صفحة أولياء الأمور =====
elif st.session_state.page == "parents":
    st.subheader("👨‍👩‍👧 بوابة أولياء الأمور المتطورة")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        student_id = st.text_input("أدخل رقم الوزارة الخاص بابنك/ابنتك", placeholder="مثال: 1001", key="parent_student_id")
        if student_id:
            student_info = st.session_state.students_df[
                st.session_state.students_df["id"].astype(str) == str(student_id).strip()
            ]
            
            if not student_info.empty:
                student = student_info.iloc[0]
                st.success(f"🎉 تم العثور على الطالب: {student['name']}")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
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
                            st.markdown(f"""
                            <div style='background: #d4edda; color: #155724; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                                <h3>✅ قادم 🎒</h3>
                                <p>آخر تحديث: {time}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style='background: #f8d7da; color: #721c24; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                                <h3>❌ لن يأتي</h3>
                                <p>آخر تحديث: {time}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("لا توجد بيانات حضور لهذا اليوم")
                
                with col_b:
                    st.subheader("🚌 معلومات الباص")
                    st.markdown(f"""
                    <div style='background: #d1ecf1; color: #0c5460; padding: 1.5rem; border-radius: 10px;'>
                        <h4>🚍 معلومات النقل</h4>
                        <p><strong>رقم الباص:</strong> {student['bus']}</p>
                        <p><strong>وقت الصباح:</strong> 7:00 صباحاً</p>
                        <p><strong>وقت الظهيرة:</strong> 2:00 ظهراً</p>
                        <p><strong>هاتف ولي الأمر:</strong> {student['parent_phone']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("❌ لم يتم العثور على الطالب")
    
    with col2:
        st.subheader("📞 معلومات الاتصال")
        st.markdown("""
        <div style='background: #e2e3e5; padding: 1.5rem; border-radius: 10px;'>
            <h4>📞 جهات الاتصال المهمة</h4>
            <p><strong>إدارة المدرسة:</strong> 02-1234567</p>
            <p><strong>النقل المدرسي:</strong> 02-7654321</p>
            <p><strong>الطوارئ:</strong> 050-1122334</p>
        </div>
        """, unsafe_allow_html=True)

# ===== صفحة النظام والإدارة =====
elif st.session_state.page == "system":
    st.subheader("⚙️ إدارة النظام والإعدادات")
    
    tab1, tab2, tab3 = st.tabs(["🎨 المظهر", "🔐 الأمان", "📊 البيانات"])
    
    with tab1:
        st.header("🎨 إعدادات المظهر")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("الثيم الحالي")
            current_theme = "☀️ فاتح" if st.session_state.theme == "light" else "🌙 مظلم"
            st.info(f"الثيم الحالي: {current_theme}")
            
            if st.button("تبديل الثيم", use_container_width=True):
                toggle_theme()
                st.rerun()
        
        with col2:
            st.subheader("إعدادات اللغة")
            current_lang = "العربية" if st.session_state.lang == "ar" else "English"
            st.info(f"اللغة الحالية: {current_lang}")
            
            if st.button("تبديل اللغة", use_container_width=True):
                toggle_language()
                st.rerun()
    
    with tab2:
        st.header("🔐 إعدادات الأمان")
        
        st.subheader("كلمات المرور")
        st.info("""
        **كلمات المرور الحالية:**
        - الباص 1: 1111
        - الباص 2: 2222
        - الباص 3: 3333
        - الإدارة: admin123
        """)
        
        st.subheader("تغيير كلمة المرور")
        bus_select = st.selectbox("اختر الباص", ["1", "2", "3"])
        new_pass = st.text_input("كلمة المرور الجديدة", type="password")
        
        if st.button("حفظ التغييرات"):
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
            st.subheader("نسخ احتياطي")
            if st.button("إنشاء نسخة احتياطية", use_container_width=True):
                st.success("✅ تم إنشاء النسخة الاحتياطية بنجاح")
            
            if st.button("استعادة البيانات", use_container_width=True):
                st.info("🔧 هذه الميزة قيد التطوير")

# ===== صفحة حول النظام =====
elif st.session_state.page == "about":
    st.subheader("ℹ️ حول النظام المتطور")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08);'>
            <h2 style='color: #2c3e50;'>🚍 نظام الباص الذكي المتطور</h2>
            <p style='color: #666; line-height: 1.6;'>
                نظام متكامل لإدارة النقل المدرسي الذكي في مدرسة المنيرة الخاصة بأبوظبي. 
                تم تطوير النظام بأحدث التقنيات لتوفير تجربة مستخدم فريدة وسلسة.
            </p>
            
            <h3 style='color: #2c3e50; margin-top: 2rem;'>🎯 المميزات الرئيسية</h3>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;'>
                <div class='feature-card'>تسجيل حضور ذكي</div>
                <div class='feature-card'>متابعة أولياء الأمور</div>
                <div class='feature-card'>لوحة تحكم للسائقين</div>
                <div class='feature-card'>إشعارات فورية</div>
                <div class='feature-card'>تقارير وإحصائيات</div>
                <div class='feature-card'>واجهة متعددة اللغات</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); text-align: center;'>
            <h3 style='color: #2c3e50;'>👥 فريق التطوير</h3>
            
            <div class='team-card-blue'>
                <h4>إياد مصطفى</h4>
                <p>مطور النظام</p>
            </div>
            
            <div class='team-card-green'>
                <h4>ايمن جلال</h4>
                <p>مصمم الواجهة</p>
            </div>
            
            <div class='team-card-orange'>
                <h4>النادي البيئي</h4>
                <p>الإشراف العام</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # معلومات الإصدار
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 15px; margin-top: 2rem; text-align: center;'>
        <h3>📋 معلومات الإصدار</h3>
        <p><strong>الإصدار:</strong> 2.0.0</p>
        <p><strong>آخر تحديث:</strong> ديسمبر 2024</p>
        <p><strong>الحالة:</strong> ⭐ الإصدار النهائي</p>
    </div>
    """, unsafe_allow_html=True)

# ===== صفحة الإشعارات =====
elif st.session_state.page == "notifications":
    st.subheader("🔔 الإشعارات الحديثة")
    
    if st.session_state.notifications:
        for notification in reversed(st.session_state.notifications[-10:]):  # آخر 10 إشعارات
            with st.container():
                st.markdown(f"""
                <div style='background: white; padding: 1rem; border-radius: 10px; border-left: 5px solid #667eea; margin: 0.5rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                    <div style='display: flex; justify-content: between; align-items: center;'>
                        <span style='font-weight: bold;'>{notification['message']}</span>
                        <span style='color: #666; font-size: 0.9rem;'>{notification['time']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📭 لا توجد إشعارات حالياً")

# ===== صفحة الطقس =====
elif st.session_state.page == "weather":
    st.subheader("🌦️ معلومات الطقس المتقدمة")
    
    weather_data = get_weather()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='weather-card' style='text-align: center;'>
            <h1>🌡️</h1>
            <h2>{weather_data['temp']}°C</h2>
            <p>درجة الحرارة</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='weather-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); text-align: center;'>
            <h1>💧</h1>
            <h2>{weather_data['humidity']}%</h2>
            <p>الرطوبة</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='weather-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); text-align: center;'>
            <h1>💨</h1>
            <h2>{weather_data['wind_speed']} km/h</h2>
            <p>سرعة الرياح</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); text-align: center; margin-top: 2rem;'>
        <h3 style='color: #2c3e50;'>حالة الطقس الحالية</h3>
        <h1 style='color: #667eea; font-size: 3rem;'>{weather_data['condition_ar']}</h1>
        <p style='color: #666;'>آخر تحديث: {datetime.datetime.now().strftime('%H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)

# ===== صفحة الإدارة =====
elif st.session_state.page == "admin":
    st.subheader("🏫 لوحة تحكم الإدارة")
    
    admin_password = st.text_input("كلمة مرور الإدارة", type="password", placeholder="أدخل كلمة مرور الإدارة...")
    
    if admin_password == admin_pass:
        st.success("✅ تم الدخول بنجاح كمسؤول")
        
        tab1, tab2, tab3 = st.tabs(["📊 التقارير", "👥 إدارة الطلاب", "⚙️ الإعدادات"])
        
        with tab1:
            st.header("📊 التقارير والإحصائيات")
            
            # إحصائيات الحضور
            stats = calculate_attendance_stats()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("إجمالي الطلاب", len(st.session_state.students_df))
            with col2:
                st.metric("المسجلين اليوم", stats["total"])
            with col3:
                st.metric("الحضور المتوقع", stats["coming"])
            with col4:
                st.metric("نسبة الحضور", f"{stats['percentage']:.1f}%")
            
            # رسم بياني
            if not st.session_state.attendance_df.empty:
                fig = px.pie(
                    values=[stats["coming"], stats["total"] - stats["coming"]],
                    names=["الحضور", "الغياب"],
                    title="توزيع الحضور والغياب"
                )
                st.plotly_chart(fig)
        
        with tab2:
            st.header("👥 إدارة بيانات الطلاب")
            st.dataframe(st.session_state.students_df, use_container_width=True)
            
            # إضافة طالب جديد
            with st.expander("➕ إضافة طالب جديد"):
                with st.form("add_student"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_id = st.text_input("رقم الوزارة")
                        new_name = st.text_input("اسم الطالب")
                    with col2:
                        new_grade = st.text_input("الصف")
                        new_bus = st.selectbox("الباص", ["1", "2", "3"])
                    new_phone = st.text_input("هاتف ولي الأمر")
                    
                    if st.form_submit_button("إضافة الطالب"):
                        if new_id and new_name:
                            new_student = pd.DataFrame([{
                                "id": new_id,
                                "name": new_name,
                                "grade": new_grade,
                                "bus": new_bus,
                                "parent_phone": new_phone
                            }])
                            st.session_state.students_df = pd.concat([st.session_state.students_df, new_student], ignore_index=True)
                            st.success("✅ تم إضافة الطالب بنجاح")
        
        with tab3:
            st.header("⚙️ إعدادات النظام المتقدمة")
            
            st.subheader("إعدادات قاعدة البيانات")
            if st.button("🔄 إعادة تعيين البيانات", type="secondary"):
                initialize_data()
                st.success("✅ تم إعادة تعيين البيانات بنجاح")
            
            st.subheader("تصدير البيانات")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 تصدير بيانات الطلاب"):
                    st.download_button(
                        "⬇️ تحميل ملف CSV",
                        st.session_state.students_df.to_csv(index=False),
                        "students_data.csv",
                        "text/csv"
                    )
            with col2:
                if st.button("📥 تصدير سجلات الحضور"):
                    st.download_button(
                        "⬇️ تحميل ملف CSV", 
                        st.session_state.attendance_df.to_csv(index=False),
                        "attendance_data.csv",
                        "text/csv"
                    )
    
    elif admin_password:
        st.error("❌ كلمة مرور خاطئة")

# ===== التذييل المحسن =====
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin-top: 2rem;'>
    <p style='margin: 0.3rem 0; font-size: 1.1rem;'><strong>🚍 نظام الباص الذكي المتطور</strong></p>
    <p style='margin: 0.3rem 0;'>مدرسة المنيرة الخاصة - أبوظبي</p>
    <p style='margin: 0.3rem 0;'>© 2024 جميع الحقوق محفوظة</p>
    <p style='margin: 0.3rem 0; font-size: 0.9rem;'>
        تم التطوير بواسطة: <strong>إياد مصطفى</strong> | 
        التصميم: <strong>ايمن جلال</strong> | 
        الإشراف: <strong>قسم النادي البيئي</strong>
    </p>
    <p style='margin: 0.3rem 0; font-size: 0.8rem; color: #888;'>
        الإصدار 2.0.0 | آخر تحديث: ديسمبر 2024
    </p>
</div>
""", unsafe_allow_html=True)
