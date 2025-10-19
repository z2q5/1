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

# تهيئة البيانات
initialize_data()

# ===== كلمات المرور =====
bus_passwords = {"1": "1111", "2": "2222", "3": "3333"}
admin_pass = "admin123"

# ===== الترجمة =====
translations = {
    "ar": {
        "title": "🚍 نظام الباص الذكي",
        "subtitle": "مدرسة المنيرة الخاصة - أبوظبي",
        "description": "نظام متكامل لإدارة النقل المدرسي الذكي",
        "student": "🎓 الطالب",
        "driver": "🚌 السائق",
        "parents": "👨‍👩‍👧 أولياء الأمور",
        "settings": "⚙️ الإعدادات",
        "about": "ℹ️ حول النظام",
        "student_title": "🎓 تسجيل حضور الطالب",
        "student_desc": "أدخل رقم الوزارة لتسجيل حالتك اليوم",
        "student_id": "🔍 رقم الوزارة",
        "student_id_placeholder": "أدخل رقم الوزارة هنا...",
        "student_info": "🎓 معلومات الطالب",
        "grade": "📚 الصف",
        "bus": "🚍 الباص",
        "parent_phone": "📞 هاتف ولي الأمر",
        "already_registered": "✅ تم التسجيل مسبقاً",
        "current_status": "حالتك الحالية",
        "change_status": "🔄 تغيير الحالة",
        "choose_status": "اختر حالتك اليوم:",
        "coming": "✅ سأحضر اليوم",
        "not_coming": "❌ لن أحضر اليوم",
        "registered_success": "🎉 تم التسجيل بنجاح!",
        "student_name": "الطالب",
        "status": "الحالة",
        "time": "وقت التسجيل",
        "bus_number": "رقم الباص",
        "stats_title": "📊 إحصائيات اليوم",
        "total_registered": "إجمالي المسجلين",
        "expected_attendance": "الحضور المتوقع",
        "attendance_rate": "نسبة الحضور",
        "driver_title": "🚌 لوحة تحكم السائق",
        "driver_login": "🔐 تسجيل دخول السائق",
        "select_bus": "اختر الباص",
        "password": "كلمة المرور",
        "password_placeholder": "أدخل كلمة المرور...",
        "login": "🚀 تسجيل الدخول",
        "logout": "🚪 تسجيل الخروج",
        "student_list": "📋 قائمة الطلاب",
        "coming_students": "🎒 الطلاب القادمون اليوم",
        "all_students": "👥 جميع طلاب الباص",
        "total_students": "👥 إجمالي الطلاب",
        "confirmed_attendance": "✅ الحضور المؤكد",
        "attendance_percentage": "📈 نسبة الحضور",
        "no_students": "🚫 لا يوجد طلاب قادمين اليوم",
        "status_coming": "قادم",
        "status_not_coming": "لن يحضر",
        "status_not_registered": "لم يسجل",
        "parents_title": "👨‍👩‍👧 بوابة أولياء الأمور",
        "parents_id_placeholder": "مثال: 1001",
        "attendance_tracking": "📊 متابعة الحضور",
        "bus_info": "🚌 معلومات الباص",
        "morning_time": "وقت الصباح التقريبي",
        "afternoon_time": "وقت الظهيرة التقريبي",
        "settings_title": "⚙️ إعدادات النظام",
        "appearance": "🎨 المظهر",
        "security": "🔐 الأمان",
        "data": "📊 البيانات",
        "current_theme": "الثيم الحالي",
        "light_theme": "☀️ فاتح",
        "dark_theme": "🌙 مظلم",
        "toggle_theme": "تبديل الثيم",
        "language_settings": "إعدادات اللغة",
        "current_language": "اللغة الحالية",
        "arabic": "العربية",
        "english": "English",
        "toggle_language": "تبديل اللغة",
        "current_passwords": "كلمات المرور الحالية",
        "change_password": "تغيير كلمة المرور",
        "select_bus_password": "اختر الباص",
        "new_password": "كلمة المرور الجديدة",
        "save_changes": "حفظ التغييرات",
        "system_stats": "إحصائيات النظام",
        "students_count": "عدد الطلاب",
        "attendance_records": "سجلات الحضور",
        "system_actions": "إجراءات النظام",
        "reset_data": "🔄 إعادة تعيين البيانات",
        "backup": "📥 نسخة احتياطية",
        "about_title": "ℹ️ حول النظام",
        "about_description": "نظام متكامل لإدارة النقل المدرسي الذكي في مدرسة المنيرة الخاصة بأبوظبي.",
        "features": "🎯 المميزات الرئيسية",
        "development_team": "👥 فريق التطوير",
        "developer": "مطور النظام",
        "designer": "مصمم الواجهة",
        "version_info": "📋 معلومات الإصدار",
        "version": "الإصدار",
        "release_date": "تاريخ الإصدار",
        "status_stable": "⭐ الإصدار المستقر",
        "footer": "🚍 نظام الباص الذكي - الإصدار 1.1",
        "rights": "© 2025 جميع الحقوق محفوظة",
        "team": "تم التطوير بواسطة: إياد مصطفى | التصميم: ايمن جلال | الإشراف: قسم النادي البيئي",
        "weather_sunny": "مشمس",
        "weather_partly_cloudy": "غائم جزئياً",
        "weather_rainy": "ممطر",
        "weather_windy": "عاصف",
        "temperature": "درجة الحرارة",
        "humidity": "الرطوبة",
        "wind_speed": "سرعة الرياح",
        "not_found": "لم يتم العثور على الطالب",
        "error": "حدث خطأ في النظام",
        "reset_success": "تم إعادة تعيين حالتك",
        "login_success": "تم الدخول بنجاح",
        "login_error": "كلمة مرور غير صحيحة",
        "data_reset_success": "تم إعادة تعيين البيانات",
        "backup_success": "تم إنشاء نسخة احتياطية",
        "password_updated": "تم تحديث كلمة المرور"
    },
    "en": {
        "title": "🚍 Smart Bus System",
        "subtitle": "Al Munira Private School - Abu Dhabi",
        "description": "Integrated system for smart school transportation management",
        "student": "🎓 Student",
        "driver": "🚌 Driver",
        "parents": "👨‍👩‍👧 Parents",
        "settings": "⚙️ Settings",
        "about": "ℹ️ About",
        "student_title": "🎓 Student Attendance Registration",
        "student_desc": "Enter your ministry number to register your status today",
        "student_id": "🔍 Ministry Number",
        "student_id_placeholder": "Enter ministry number here...",
        "student_info": "🎓 Student Information",
        "grade": "📚 Grade",
        "bus": "🚍 Bus",
        "parent_phone": "📞 Parent Phone",
        "already_registered": "✅ Already Registered",
        "current_status": "Your Current Status",
        "change_status": "🔄 Change Status",
        "choose_status": "Choose your status today:",
        "coming": "✅ I will attend today",
        "not_coming": "❌ I will not attend today",
        "registered_success": "🎉 Registration Successful!",
        "student_name": "Student",
        "status": "Status",
        "time": "Registration Time",
        "bus_number": "Bus Number",
        "stats_title": "📊 Today's Statistics",
        "total_registered": "Total Registered",
        "expected_attendance": "Expected Attendance",
        "attendance_rate": "Attendance Rate",
        "driver_title": "🚌 Driver Control Panel",
        "driver_login": "🔐 Driver Login",
        "select_bus": "Select Bus",
        "password": "Password",
        "password_placeholder": "Enter password...",
        "login": "🚀 Login",
        "logout": "🚪 Logout",
        "student_list": "📋 Student List",
        "coming_students": "🎒 Students Coming Today",
        "all_students": "👥 All Bus Students",
        "total_students": "👥 Total Students",
        "confirmed_attendance": "✅ Confirmed Attendance",
        "attendance_percentage": "📈 Attendance Percentage",
        "no_students": "🚫 No students coming today",
        "status_coming": "Coming",
        "status_not_coming": "Not Coming",
        "status_not_registered": "Not Registered",
        "parents_title": "👨‍👩‍👧 Parents Portal",
        "parents_id_placeholder": "Example: 1001",
        "attendance_tracking": "📊 Attendance Tracking",
        "bus_info": "🚌 Bus Information",
        "morning_time": "Approximate Morning Time",
        "afternoon_time": "Approximate Afternoon Time",
        "settings_title": "⚙️ System Settings",
        "appearance": "🎨 Appearance",
        "security": "🔐 Security",
        "data": "📊 Data",
        "current_theme": "Current Theme",
        "light_theme": "☀️ Light",
        "dark_theme": "🌙 Dark",
        "toggle_theme": "Toggle Theme",
        "language_settings": "Language Settings",
        "current_language": "Current Language",
        "arabic": "Arabic",
        "english": "English",
        "toggle_language": "Toggle Language",
        "current_passwords": "Current Passwords",
        "change_password": "Change Password",
        "select_bus_password": "Select Bus",
        "new_password": "New Password",
        "save_changes": "Save Changes",
        "system_stats": "System Statistics",
        "students_count": "Students Count",
        "attendance_records": "Attendance Records",
        "system_actions": "System Actions",
        "reset_data": "🔄 Reset Data",
        "backup": "📥 Backup",
        "about_title": "ℹ️ About System",
        "about_description": "Integrated system for smart school transportation management at Al Munira Private School in Abu Dhabi.",
        "features": "🎯 Main Features",
        "development_team": "👥 Development Team",
        "developer": "System Developer",
        "designer": "UI Designer",
        "version_info": "📋 Version Information",
        "version": "Version",
        "release_date": "Release Date",
        "status_stable": "⭐ Stable Release",
        "footer": "🚍 Smart Bus System - Version 1.1",
        "rights": "© 2025 All Rights Reserved",
        "team": "Developed by: Iyad Mustafa | Design: Ayman Jalal | Supervision: Environmental Club",
        "weather_sunny": "Sunny",
        "weather_partly_cloudy": "Partly Cloudy",
        "weather_rainy": "Rainy",
        "weather_windy": "Windy",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "wind_speed": "Wind Speed",
        "not_found": "Student not found",
        "error": "System error occurred",
        "reset_success": "Your status has been reset",
        "login_success": "Login successful",
        "login_error": "Incorrect password",
        "data_reset_success": "Data reset successfully",
        "backup_success": "Backup created successfully",
        "password_updated": "Password updated successfully"
    }
}

def t(key):
    """دالة الترجمة الآمنة"""
    try:
        return translations[st.session_state.lang][key]
    except KeyError:
        return key  # إرجاع المفتاح نفسه إذا لم توجد ترجمة

# ===== وظائف مساعدة =====
def add_notification(message):
    st.session_state.notifications.append({
        "time": datetime.datetime.now().strftime("%H:%M"),
        "message": message
    })

def get_weather():
    """بيانات الطقس مع الترجمة"""
    conditions = [
        t("weather_sunny"),
        t("weather_partly_cloudy"), 
        t("weather_rainy"),
        t("weather_windy")
    ]
    
    condition = random.choice(conditions)
    
    return {
        "temp": random.randint(28, 42),
        "humidity": random.randint(30, 80),
        "wind_speed": random.randint(5, 25),
        "condition": condition
    }

def calculate_attendance_stats():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if st.session_state.attendance_df.empty:
        return {"total": 0, "coming": 0, "percentage": 0}
    
    today_data = st.session_state.attendance_df[
        st.session_state.attendance_df["date"] == today
    ]
    
    total = len(today_data)
    coming = len(today_data[today_data["status"] == t("status_coming")]) if not today_data.empty else 0
    percentage = (coming / total * 100) if total > 0 else 0
    
    return {
        "total": total,
        "coming": coming,
        "percentage": percentage
    }

def has_student_registered_today(student_id):
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

def register_attendance(student, status):
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
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.rerun()

def toggle_language():
    st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
    st.rerun()

# ===== تصميم متطور =====
def apply_custom_styles():
    if st.session_state.theme == "dark":
        dark_theme = """
        .main { background-color: #0e1117; color: #fafafa; }
        .stApp { background-color: #0e1117; }
        .stButton>button { background-color: #262730; color: #fafafa; border: 1px solid #555; }
        .stTextInput>div>div>input { background-color: #262730; color: #fafafa; border: 1px solid #555; }
        .stSelectbox>div>div>select { background-color: #262730; color: #fafafa; }
        """
    else:
        dark_theme = ""
    
    st.markdown(f"""
    <style>
        .main {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .stApp {{
            background: transparent;
        }}
        
        {dark_theme}
        
        .main-header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 2.5rem 2rem;
            border-radius: 25px;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .glass-card {{
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 1.5rem;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 20px;
            text-align: center;
            margin: 0.5rem;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .stat-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.6);
        }}
        
        .student-card {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 20px;
            margin: 1rem 0;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }}
        
        .student-card:hover {{
            transform: translateX(10px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }}
        
        .weather-card {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(79, 172, 254, 0.4);
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .feature-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 0.5rem 0;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .feature-card:hover {{
            transform: scale(1.05);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }}
        
        .stButton>button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 15px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .stButton>button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.6);
        }}
        
        .stTextInput>div>div>input {{
            border-radius: 15px;
            border: 2px solid #e9ecef;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            transition: all 0.3s ease;
        }}
        
        .stTextInput>div>div>input:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            transform: translateY(-2px);
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .animate-fadeIn {{
            animation: fadeIn 0.8s ease-out;
        }}
        
        .section-title {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            font-size: 1.5rem;
        }}
    </style>
    """, unsafe_allow_html=True)

apply_custom_styles()

# ===== الهيدر الرئيسي =====
col1, col2, col3 = st.columns([2, 3, 1])

with col1:
    weather_data = get_weather()
    st.markdown(f"""
    <div class='weather-card animate-fadeIn'>
        <h3>🌡️ {weather_data['temp']}°C</h3>
        <p>{weather_data['condition']}</p>
        <p>💧 {weather_data['humidity']}% | 💨 {weather_data['wind_speed']} km/h</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='main-header animate-fadeIn'>
        <h1 style='font-size: 2.8rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{t('title')}</h1>
        <h3 style='font-size: 1.4rem; margin-bottom: 0.5rem; color: #666;'>{t('subtitle')}</h3>
        <p style='font-size: 1.1rem; color: #888;'>{t('description')}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    col3a, col3b = st.columns(2)
    with col3a:
        theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
        if st.button(theme_icon, use_container_width=True, key="theme_btn"):
            toggle_theme()
    
    with col3b:
        lang_text = "EN" if st.session_state.lang == "ar" else "AR"
        if st.button(f"🌐 {lang_text}", use_container_width=True, key="lang_btn"):
            toggle_language()

# ===== شريط التنقل =====
pages = [
    (t("student"), "student"),
    (t("driver"), "driver"), 
    (t("parents"), "parents"),
    (t("settings"), "admin"),
    (t("about"), "about")
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
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2 class='section-title'>{t('student_title')}</h2>
            <p style='color: white; font-size: 1.1rem;'>{t('student_desc')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card animate-fadeIn'>", unsafe_allow_html=True)
        
        student_id = st.text_input(
            t("student_id"),
            placeholder=t("student_id_placeholder"),
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
                    <div class='student-card animate-fadeIn'>
                        <div style='text-align: center;'>
                            <h3 style='color: #2c3e50; margin-bottom: 1rem;'>🎓 {student['name']}</h3>
                            <div style='display: flex; justify-content: center; gap: 1.5rem; margin-bottom: 1rem;'>
                                <div style='text-align: center;'>
                                    <div style='background: #667eea; color: white; padding: 0.5rem 1rem; border-radius: 10px; font-weight: bold;'>{t('grade')}: {student['grade']}</div>
                                </div>
                                <div style='text-align: center;'>
                                    <div style='background: #764ba2; color: white; padding: 0.5rem 1rem; border-radius: 10px; font-weight: bold;'>{t('bus')}: {student['bus']}</div>
                                </div>
                            </div>
                            <p style='color: #666; margin: 0;'><strong>{t('parent_phone')}:</strong> {student['parent_phone']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    already_registered, current_status = has_student_registered_today(student_id)
                    
                    if already_registered:
                        status_color = "#51cf66" if current_status == t("status_coming") else "#ff6b6b"
                        status_icon = "✅" if current_status == t("status_coming") else "❌"
                        st.markdown(f"""
                        <div class='animate-fadeIn' style='background: {status_color}; color: white; padding: 1.5rem; border-radius: 15px; text-align: center; margin: 1rem 0;'>
                            <h4>{status_icon} {t('already_registered')}</h4>
                            <p style='margin: 0.5rem 0; font-size: 1.1rem;'>{t('current_status')}: <strong>{current_status}</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(t("change_status"), use_container_width=True, type="secondary"):
                            today = datetime.datetime.now().strftime("%Y-%m-%d")
                            st.session_state.attendance_df = st.session_state.attendance_df[
                                ~((st.session_state.attendance_df["id"].astype(str) == str(student_id).strip()) & 
                                  (st.session_state.attendance_df["date"] == today))
                            ]
                            st.success(t("reset_success"))
                            st.rerun()
                    else:
                        st.markdown(f"<h4 style='text-align: center; color: #2c3e50; margin-bottom: 1rem;'>{t('choose_status')}</h4>", unsafe_allow_html=True)
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button(t("coming"), use_container_width=True, type="primary"):
                                now = register_attendance(student, t("status_coming"))
                                st.balloons()
                                st.success(f"""
                                **{t('registered_success')}**
                                
                                **{t('student_name')}:** {student['name']}
                                **{t('status')}:** {t('status_coming')}
                                **{t('time')}:** {now.strftime('%H:%M')}
                                **{t('bus_number')}:** {student['bus']}
                                """)
                                
                        with col_b:
                            if st.button(t("not_coming"), use_container_width=True, type="secondary"):
                                now = register_attendance(student, t("status_not_coming"))
                                st.success(f"""
                                **{t('registered_success')}**
                                
                                **{t('student_name')}:** {student['name']}
                                **{t('status')}:** {t('status_not_coming')}
                                **{t('time')}:** {now.strftime('%H:%M')}
                                **{t('bus_number')}:** {student['bus']}
                                """)
                
                else:
                    st.error(f"❌ {t('not_found')}")
                    
            except Exception as e:
                st.error(f"❌ {t('error')}")
        
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div style='text-align: center; margin-bottom: 1rem;'><h3 style='color: white;'>{t('stats_title')}</h3></div>", unsafe_allow_html=True)
        
        stats = calculate_attendance_stats()
        
        st.markdown(f"""
        <div class='stat-card animate-fadeIn'>
            <h3 style='margin-bottom: 0.5rem; font-size: 2rem;'>👥</h3>
            <h2 style='margin: 0; font-size: 2.5rem;'>{stats['total']}</h2>
            <p style='margin: 0; opacity: 0.9;'>{t('total_registered')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='stat-card animate-fadeIn'>
            <h3 style='margin-bottom: 0.5rem; font-size: 2rem;'>✅</h3>
            <h2 style='margin: 0; font-size: 2.5rem;'>{stats['coming']}</h2>
            <p style='margin: 0; opacity: 0.9;'>{t('expected_attendance')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='stat-card animate-fadeIn'>
            <h3 style='margin-bottom: 0.5rem; font-size: 2rem;'>📈</h3>
            <h2 style='margin: 0; font-size: 2.5rem;'>{stats['percentage']:.1f}%</h2>
            <p style='margin: 0; opacity: 0.9;'>{t('attendance_rate')}</p>
        </div>
        """, unsafe_allow_html=True)

# ===== صفحة السائق =====
elif st.session_state.page == "driver":
    st.subheader(t("driver_title"))
    
    if not st.session_state.driver_logged_in:
        st.markdown("<div class='glass-card animate-fadeIn'>", unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='text-align: center; color: #2c3e50; margin-bottom: 2rem;'>{t('driver_login')}</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            bus_number = st.selectbox(t("select_bus"), ["1", "2", "3"])
        with col2:
            password = st.text_input(t("password"), type="password", placeholder=t("password_placeholder"))
        
        if st.button(t("login"), type="primary", use_container_width=True):
            if password == bus_passwords.get(bus_number, ""):
                st.session_state.driver_logged_in = True
                st.session_state.current_bus = bus_number
                st.success(t("login_success"))
                st.rerun()
            else:
                st.error(t("login_error"))
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.success(f"✅ {t('login_success')} - الباص رقم {st.session_state.current_bus}")
        
        if st.button(t("logout"), type="secondary"):
            st.session_state.driver_logged_in = False
            st.rerun()
        
        st.subheader(f"{t('student_list')} - الباص {st.session_state.current_bus}")
        
        bus_students = st.session_state.students_df[
            st.session_state.students_df["bus"] == st.session_state.current_bus
        ]
        
        if not bus_students.empty:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            today_attendance = st.session_state.attendance_df[
                st.session_state.attendance_df["date"] == today
            ] if not st.session_state.attendance_df.empty else pd.DataFrame()
            
            coming_students = today_attendance[
                (today_attendance["bus"] == st.session_state.current_bus) & 
                (today_attendance["status"] == t("status_coming"))
            ] if not today_attendance.empty else pd.DataFrame()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(t("total_students"), len(bus_students))
            with col2:
                st.metric(t("confirmed_attendance"), len(coming_students))
            with col3:
                percentage = (len(coming_students) / len(bus_students) * 100) if len(bus_students) > 0 else 0
                st.metric(t("attendance_percentage"), f"{percentage:.1f}%")
            
            st.subheader(t("coming_students"))
            if not coming_students.empty:
                for _, student in coming_students.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div style='background: #d4edda; padding: 1rem; border-radius: 15px; border-right: 5px solid #28a745; margin: 0.5rem 0;'>
                            <h4 style='color: #155724; margin: 0;'>✅ {student['name']}</h4>
                            <p style='color: #155724; margin: 0.3rem 0;'>📚 {student['grade']} | ⏰ {student['time']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info(t("no_students"))
            
            st.subheader(t("all_students"))
            for _, student in bus_students.iterrows():
                student_attendance = today_attendance[
                    today_attendance["id"].astype(str) == str(student["id"])
                ] if not today_attendance.empty else pd.DataFrame()
                
                if not student_attendance.empty:
                    status = student_attendance.iloc[0]["status"]
                    if status == t("status_coming"):
                        bg_color = "#d4edda"
                        border_color = "#28a745"
                        status_icon = "✅"
                    else:
                        bg_color = "#f8d7da"
                        border_color = "#dc3545"
                        status_icon = "❌"
                else:
                    bg_color = "#fff3cd"
                    border_color = "#ffc107"
                    status_icon = "⏳"
                
                st.markdown(f"""
                <div style='background: {bg_color}; padding: 1rem; border-radius: 15px; border-right: 5px solid {border_color}; margin: 0.5rem 0;'>
                    <h4 style='color: #2c3e50; margin: 0;'>{status_icon} {student['name']}</h4>
                    <p style='color: #2c3e50; margin: 0.3rem 0;'>📚 {student['grade']} | 📱 {student['parent_phone']}</p>
                </div>
                """, unsafe_allow_html=True)

# ===== صفحة أولياء الأمور =====
elif st.session_state.page == "parents":
    st.subheader(t("parents_title"))
    
    student_id = st.text_input(t("student_id"), placeholder=t("parents_id_placeholder"))
    if student_id:
        student_info = st.session_state.students_df[
            st.session_state.students_df["id"].astype(str) == str(student_id).strip()
        ]
        
        if not student_info.empty:
            student = student_info.iloc[0]
            st.success(f"🎉 تم العثور على الطالب: {student['name']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(t("attendance_tracking"))
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
                    if status == t("status_coming"):
                        st.success(f"**الحالة:** {t('status_coming')} 🎒\n**آخر تحديث:** {time}")
                    else:
                        st.error(f"**الحالة:** {t('status_not_coming')} ❌\n**آخر تحديث:** {time}")
                else:
                    st.info("لا توجد بيانات حضور لهذا اليوم")
            
            with col2:
                st.subheader(t("bus_info"))
                st.info(f"""
                **{t('bus')}:** {student['bus']}
                **{t('morning_time')}:** 7:00 صباحاً
                **{t('afternoon_time')}:** 2:00 ظهراً
                **{t('parent_phone')}:** {student['parent_phone']}
                """)
        else:
            st.error(f"❌ {t('not_found')}")

# ===== صفحة الإعدادات =====
elif st.session_state.page == "admin":
    st.subheader(t("settings_title"))
    
    tab1, tab2, tab3 = st.tabs([t("appearance"), t("security"), t("data")])
    
    with tab1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.header(t("appearance"))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(t("current_theme"))
            current_theme = t("light_theme") if st.session_state.theme == "light" else t("dark_theme")
            st.info(f"{t('current_theme')}: {current_theme}")
            
            if st.button(t("toggle_theme"), use_container_width=True):
                toggle_theme()
        
        with col2:
            st.subheader(t("language_settings"))
            current_lang = t("arabic") if st.session_state.lang == "ar" else t("english")
            st.info(f"{t('current_language')}: {current_lang}")
            
            if st.button(t("toggle_language"), use_container_width=True):
                toggle_language()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.header(t("security"))
        
        st.subheader(t("current_passwords"))
        st.info("""
        **كلمات مرور الباصات:**
        - الباص 1: 1111
        - الباص 2: 2222  
        - الباص 3: 3333
        """)
        
        st.subheader(t("change_password"))
        bus_select = st.selectbox(t("select_bus_password"), ["1", "2", "3"])
        new_pass = st.text_input(t("new_password"), type="password")
        
        if st.button(t("save_changes")):
            if new_pass:
                bus_passwords[bus_select] = new_pass
                st.success(f"✅ {t('password_updated')} {bus_select}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.header(t("data"))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(t("system_stats"))
            st.metric(t("students_count"), len(st.session_state.students_df))
            st.metric(t("attendance_records"), len(st.session_state.attendance_df))
        
        with col2:
            st.subheader(t("system_actions"))
            if st.button(t("reset_data"), type="secondary", use_container_width=True):
                initialize_data()
                st.success(t("data_reset_success"))
            
            if st.button(t("backup"), use_container_width=True):
                st.info(t("backup_success"))
        st.markdown("</div>", unsafe_allow_html=True)

# ===== صفحة حول النظام =====
elif st.session_state.page == "about":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.header(t("about_title"))
        st.markdown(f"<p style='color: #666; line-height: 1.6; font-size: 1.1rem;'>{t('about_description')}</p>", unsafe_allow_html=True)
        
        st.subheader(t("features"))
        features = [
            "تسجيل حضور ذكي للطلاب",
            "متابعة أولياء الأمور لحالة أبنائهم", 
            "لوحة تحكم متكاملة للسائقين",
            "إشعارات فورية للتحديثات",
            "تقارير وإحصائيات مفصلة",
            "واجهة مستخدم سهلة الاستخدام"
        ]
        
        for feature in features:
            st.markdown(f"<div class='feature-card'>{feature}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader(t("development_team"))
        
        st.markdown("""
        <div class='feature-card'>
            <h4>إياد مصطفى</h4>
            <p>مطور النظام</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h4>ايمن جلال</h4>
            <p>مصمم الواجهة</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # إصلاح السطر الذي كان يسبب الخطأ
    st.markdown(f"""
    <div class='glass-card' style='text-align: center;'>
        <h3>{t('version_info')}</h3>
        <p><strong>{t('version')}:</strong> 1.1</p>
        <p><strong>{t('release_date')}:</strong> أكتوبر 2025</p>
        <p><strong>الحالة:</strong> ⭐ {t('status_stable')}</p>
    </div>
    """, unsafe_allow_html=True)

# ===== التذييل =====
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: white; padding: 2rem 0;'>
    <p style='margin: 0.3rem 0; font-size: 1.1rem;'><strong>{t('footer')}</strong></p>
    <p style='margin: 0.3rem 0;'>{t('subtitle')}</p>
    <p style='margin: 0.3rem 0;'>{t('rights')}</p>
    <p style='margin: 0.3rem 0; font-size: 0.9rem;'>{t('team')}</p>
</div>
""", unsafe_allow_html=True)
