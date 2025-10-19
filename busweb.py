import streamlit as st
import pandas as pd
import datetime
import os
import random
import json
import pickle
from pathlib import Path

# ===== إعداد الصفحة =====
st.set_page_config(
    page_title="Smart Bus System - Al Munira Private School", 
    layout="wide",
    page_icon="🚍",
    initial_sidebar_state="collapsed"
)

# ===== مسار حفظ البيانات =====
DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)

# ===== وظائف حفظ البيانات =====
def save_data():
    """حفظ جميع البيانات في الملفات"""
    try:
        # حفظ بيانات الطلاب
        with open(DATA_DIR / "students.pkl", "wb") as f:
            pickle.dump(st.session_state.students_df.to_dict(), f)
        
        # حفظ بيانات الحضور
        with open(DATA_DIR / "attendance.pkl", "wb") as f:
            pickle.dump(st.session_state.attendance_df.to_dict(), f)
        
        # حفظ بيانات التقييمات
        with open(DATA_DIR / "ratings.pkl", "wb") as f:
            pickle.dump(st.session_state.ratings_df.to_dict(), f)
        
        # حفظ الإعدادات
        settings = {
            "bus_passwords": st.session_state.bus_passwords,
            "admin_password": st.session_state.admin_password,
            "theme": st.session_state.theme,
            "lang": st.session_state.lang
        }
        with open(DATA_DIR / "settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False)
            
    except Exception as e:
        st.error(f"خطأ في حفظ البيانات: {e}")

def load_data():
    """تحميل البيانات المحفوظة"""
    try:
        # تحميل بيانات الطلاب
        if (DATA_DIR / "students.pkl").exists():
            with open(DATA_DIR / "students.pkl", "rb") as f:
                students_data = pickle.load(f)
                st.session_state.students_df = pd.DataFrame(students_data)
        
        # تحميل بيانات الحضور
        if (DATA_DIR / "attendance.pkl").exists():
            with open(DATA_DIR / "attendance.pkl", "rb") as f:
                attendance_data = pickle.load(f)
                st.session_state.attendance_df = pd.DataFrame(attendance_data)
        
        # تحميل بيانات التقييمات
        if (DATA_DIR / "ratings.pkl").exists():
            with open(DATA_DIR / "ratings.pkl", "rb") as f:
                ratings_data = pickle.load(f)
                st.session_state.ratings_df = pd.DataFrame(ratings_data)
        else:
            st.session_state.ratings_df = pd.DataFrame(columns=["rating", "comment", "timestamp"])
                
        # تحميل الإعدادات
        if (DATA_DIR / "settings.json").exists():
            with open(DATA_DIR / "settings.json", "r", encoding="utf-8") as f:
                settings = json.load(f)
                st.session_state.bus_passwords = settings.get("bus_passwords", {"1": "1111", "2": "2222", "3": "3333"})
                st.session_state.admin_password = settings.get("admin_password", "admin123")
                st.session_state.theme = settings.get("theme", "light")
                st.session_state.lang = settings.get("lang", "ar")
                
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")

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
if "bus_passwords" not in st.session_state:
    st.session_state.bus_passwords = {"1": "1111", "2": "2222", "3": "3333"}
if "admin_password" not in st.session_state:
    st.session_state.admin_password = "admin123"
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "ratings_df" not in st.session_state:
    st.session_state.ratings_df = pd.DataFrame(columns=["rating", "comment", "timestamp"])
if "selected_rating" not in st.session_state:
    st.session_state.selected_rating = 0
if "hover_rating" not in st.session_state:
    st.session_state.hover_rating = 0

# تحميل البيانات المحفوظة
load_data()

# ===== البيانات الافتراضية =====
def initialize_data():
    if 'students_df' not in st.session_state:
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
        st.session_state.students_df = pd.DataFrame(students_data)
    
    if 'attendance_df' not in st.session_state:
        st.session_state.attendance_df = pd.DataFrame(columns=[
            "id", "name", "grade", "bus", "status", "time", "date"
        ])

# تهيئة البيانات
initialize_data()

# ===== الترجمة =====
translations = {
    "ar": {
        "title": "🚍 نظام الباص الذكي",
        "subtitle": "مدرسة المنيرة الخاصة - أبوظبي",
        "description": "نظام متكامل لإدارة النقل المدرسي الذكي",
        "student": "🎓 الطالب",
        "driver": "🚌 السائق",
        "parents": "👨‍👩‍👧 أولياء الأمور",
        "admin": "🏫 الإدارة",
        "about": "ℹ️ حول النظام",
        # ... باقي الترجمات تبقى كما هي
        "rating_system": "⭐ نظام التقييم المتطور",
        "rate_app": "قيم تجربتك مع التطبيق",
        "your_rating": "تقييمك",
        "your_comment": "شاركنا رأيك (اختياري)",
        "submit_rating": "إرسال التقييم 🚀",
        "thank_you_rating": "شكراً جزيلاً لتقييمك! 🌟",
        "average_rating": "متوسط التقييم",
        "total_ratings": "إجمالي التقييمات",
        "rating_success": "تم إرسال تقييمك بنجاح! 🎉",
        "select_rating": "اختر عدد النجوم",
        "excellent": "ممتاز",
        "very_good": "جيد جداً",
        "good": "جيد",
        "fair": "مقبول",
        "poor": "ضعيف"
    },
    "en": {
        "title": "🚍 Smart Bus System",
        "subtitle": "Al Munira Private School - Abu Dhabi",
        "description": "Integrated system for smart school transportation management",
        "student": "🎓 Student",
        "driver": "🚌 Driver",
        "parents": "👨‍👩‍👧 Parents",
        "admin": "🏫 Admin",
        "about": "ℹ️ About",
        # ... باقي الترجمات تبقى كما هي
        "rating_system": "⭐ Advanced Rating System",
        "rate_app": "Rate Your Experience",
        "your_rating": "Your Rating",
        "your_comment": "Share your feedback (optional)",
        "submit_rating": "Submit Rating 🚀",
        "thank_you_rating": "Thank you for your rating! 🌟",
        "average_rating": "Average Rating",
        "total_ratings": "Total Ratings",
        "rating_success": "Your rating has been submitted successfully! 🎉",
        "select_rating": "Select number of stars",
        "excellent": "Excellent",
        "very_good": "Very Good",
        "good": "Good",
        "fair": "Fair",
        "poor": "Poor"
    }
}

def t(key):
    """دالة الترجمة الآمنة"""
    try:
        return translations[st.session_state.lang][key]
    except KeyError:
        return key

# ===== وظائف مساعدة =====
def add_notification(message):
    st.session_state.notifications.append({
        "time": datetime.datetime.now().strftime("%H:%M"),
        "message": message
    })
    save_data()

def get_weather():
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
    coming = len(today_data[today_data["status"] == "قادم"]) if not today_data.empty else 0
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
    
    save_data()
    return now

def add_rating(rating, comment):
    """إضافة تقييم جديد"""
    new_rating = pd.DataFrame([{
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    if st.session_state.ratings_df.empty:
        st.session_state.ratings_df = new_rating
    else:
        st.session_state.ratings_df = pd.concat([
            st.session_state.ratings_df, new_rating
        ], ignore_index=True)
    
    save_data()

def get_average_rating():
    """حساب متوسط التقييم"""
    if st.session_state.ratings_df.empty:
        return 0, 0
    return st.session_state.ratings_df["rating"].mean(), len(st.session_state.ratings_df)

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    save_data()
    st.rerun()

def toggle_language():
    # حفظ اللغة الحالية قبل التغيير
    current_lang = st.session_state.lang
    # تبديل اللغة
    st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
    # حفظ الإعدادات
    save_data()
    # إعادة تحميل الصفحة
    st.rerun()

def select_rating(rating):
    """تحديد التقييم"""
    st.session_state.selected_rating = rating

def get_rating_label(rating):
    """الحصول على تسمية التقييم"""
    labels = {
        1: t("poor"),
        2: t("fair"),
        3: t("good"),
        4: t("very_good"),
        5: t("excellent")
    }
    return labels.get(rating, "")

# ===== تصميم متطور مع نجوم جميلة =====
def apply_custom_styles():
    if st.session_state.theme == "dark":
        dark_theme = """
        .main { 
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
        }
        .stApp {
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        }
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
        }
        .stTextInput>div>div>input {
            background-color: #2d3746;
            color: white;
            border: 1px solid #4a5568;
        }
        .stSelectbox>div>div>select {
            background-color: #2d3746;
            color: white;
        }
        .stTextArea>div>div>textarea {
            background-color: #2d3746;
            color: white;
            border: 1px solid #4a5568;
        }
        """
    else:
        dark_theme = """
        .main { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #2c3e50;
        }
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        """
    
    st.markdown(f"""
    <style>
        {dark_theme}
        
        .main-header {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}
        
        .stat-card {{
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin: 0.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.25);
        }}
        
        .student-card {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
        }}
        
        .weather-card {{
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
        }}
        
        .feature-card {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }}
        
        .feature-card:hover {{
            background: rgba(255, 255, 255, 0.2);
            transform: scale(1.02);
        }}
        
        .rating-card {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .star-container {{
            display: flex;
            justify-content: center;
            gap: 0.8rem;
            margin: 2rem 0;
        }}
        
        .star-button {{
            background: transparent;
            border: none;
            font-size: 3rem;
            cursor: pointer;
            transition: all 0.3s ease;
            padding: 0.5rem;
            border-radius: 50%;
        }}
        
        .star-button:hover {{
            transform: scale(1.3) rotate(15deg);
            background: rgba(255, 215, 0, 0.1);
        }}
        
        .star-active {{
            color: #FFD700;
            text-shadow: 0 0 20px #FFD700, 0 0 30px #FFD700;
            animation: starGlow 1.5s ease-in-out infinite alternate;
        }}
        
        .star-inactive {{
            color: #666;
            opacity: 0.6;
        }}
        
        .star-label {{
            font-size: 1.2rem;
            font-weight: bold;
            margin-top: 1rem;
            color: #FFD700;
            text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        }}
        
        .rating-description {{
            font-size: 1.1rem;
            color: rgba(255, 255, 255, 0.8);
            margin: 1rem 0;
            text-align: center;
        }}
        
        @keyframes starGlow {{
            0% {{
                text-shadow: 0 0 20px #FFD700, 0 0 30px #FFD700;
                transform: scale(1);
            }}
            100% {{
                text-shadow: 0 0 30px #FFD700, 0 0 40px #FFD700, 0 0 50px #FFD700;
                transform: scale(1.1);
            }}
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        .pulse-animation {{
            animation: pulse 2s infinite;
        }}
        
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
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .stTextInput>div>div>input {{
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 0.75rem;
            font-size: 1rem;
            background: rgba(255, 255, 255, 0.1);
            color: white;
        }}
        
        .stTextInput>div>div>input:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }}
        
        .stSelectbox>div>div>select {{
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
        }}
        
        .stTextArea>div>div>textarea {{
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 0.75rem;
            font-size: 1rem;
            background: rgba(255, 255, 255, 0.1);
            color: white;
        }}
        
        .content-section {{
            background: transparent;
            padding: 0;
            border-radius: 0;
            box-shadow: none;
            border: none;
        }}
        
        .section-title {{
            color: white;
            text-align: center;
            margin-bottom: 1rem;
            font-size: 1.5rem;
            font-weight: bold;
        }}
        
        .info-text {{
            color: rgba(255, 255, 255, 0.9);
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        .rating-success {{
            background: linear-gradient(135deg, #00b09b, #96c93d);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem 0;
            border: 1px solid rgba(255,255,255,0.3);
        }}
    </style>
    """, unsafe_allow_html=True)

apply_custom_styles()

# ===== الهيدر الرئيسي =====
col1, col2, col3 = st.columns([2, 3, 1])

with col1:
    weather_data = get_weather()
    st.markdown(f"""
    <div class='weather-card'>
        <h3>🌡️ {weather_data['temp']}°C</h3>
        <p>{weather_data['condition']}</p>
        <p>💧 {weather_data['humidity']}% | 💨 {weather_data['wind_speed']} km/h</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='main-header'>
        <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>{t('title')}</h1>
        <h3 style='font-size: 1.3rem; margin-bottom: 0.5rem; opacity: 0.9;'>{t('subtitle')}</h3>
        <p style='font-size: 1.1rem; opacity: 0.8;'>{t('description')}</p>
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
    (t("admin"), "admin"),
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

# ===== صفحة حول النظام مع التقييم المتطور =====
elif st.session_state.page == "about":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(t("about_title"))
        st.markdown(f"<p class='info-text'>{t('about_description')}</p>", unsafe_allow_html=True)
        
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
    
    with col2:
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
    
    # قسم التقييم المتطور
    st.markdown("---")
    st.subheader("✨ " + t("rating_system"))
    
    # عرض إحصائيات التقييم
    avg_rating, total_ratings = get_average_rating()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='rating-card pulse-animation'>
            <h3>⭐ {t('average_rating')}</h3>
            <h1 style='font-size: 3.5rem; color: #FFD700; margin: 1rem 0;'>{avg_rating:.1f}</h1>
            <p style='color: rgba(255,255,255,0.8);'>من 5 نجوم</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='rating-card'>
            <h3>📊 {t('total_ratings')}</h3>
            <h1 style='font-size: 3.5rem; color: #667eea; margin: 1rem 0;'>{total_ratings}</h1>
            <p style='color: rgba(255,255,255,0.8);'>تقييم مجمع</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # عرض النجوم بناءً على متوسط التقييم
        stars_html = ""
        full_stars = int(avg_rating)
        half_star = avg_rating - full_stars >= 0.5
        
        for i in range(5):
            if i < full_stars:
                stars_html += "⭐"
            elif i == full_stars and half_star:
                stars_html += "✨"
            else:
                stars_html += "☆"
        
        st.markdown(f"""
        <div class='rating-card'>
            <h3>🎯 التقييم الحالي</h3>
            <div style='font-size: 2.5rem; margin: 1rem 0; color: #FFD700;'>
                {stars_html}
            </div>
            <p style='color: rgba(255,255,255,0.8);'>بناءً على {total_ratings} تقييم</p>
        </div>
        """, unsafe_allow_html=True)
    
    # نظام التقييم المتطور
    st.markdown(f"<h3 style='text-align: center; color: white; margin: 3rem 0 1rem 0;'>✨ {t('rate_app')}</h3>", unsafe_allow_html=True)
    
    # أزرار النجوم المتطورة
    st.markdown(f"<p style='color: white; text-align: center; font-size: 1.1rem;'>{t('select_rating')}</p>", unsafe_allow_html=True)
    
    # عرض النجوم التفاعلية
    st.markdown("""
    <div class='star-container'>
        <button class='star-button' onclick='selectRating(1)'>⭐</button>
        <button class='star-button' onclick='selectRating(2)'>⭐</button>
        <button class='star-button' onclick='selectRating(3)'>⭐</button>
        <button class='star-button' onclick='selectRating(4)'>⭐</button>
        <button class='star-button' onclick='selectRating(5)'>⭐</button>
    </div>
    """, unsafe_allow_html=True)
    
    # عرض النجوم باستخدام أعمدة Streamlit
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        star_class = "star-active" if st.session_state.selected_rating >= 1 else "star-inactive"
        if st.button("⭐", key="star1", use_container_width=True):
            select_rating(1)
        if st.session_state.selected_rating >= 1:
            st.markdown(f"<div class='star-label'>{get_rating_label(1)}</div>", unsafe_allow_html=True)
    
    with col2:
        if st.button("⭐⭐", key="star2", use_container_width=True):
            select_rating(2)
        if st.session_state.selected_rating >= 2:
            st.markdown(f"<div class='star-label'>{get_rating_label(2)}</div>", unsafe_allow_html=True)
    
    with col3:
        if st.button("⭐⭐⭐", key="star3", use_container_width=True):
            select_rating(3)
        if st.session_state.selected_rating >= 3:
            st.markdown(f"<div class='star-label'>{get_rating_label(3)}</div>", unsafe_allow_html=True)
    
    with col4:
        if st.button("⭐⭐⭐⭐", key="star4", use_container_width=True):
            select_rating(4)
        if st.session_state.selected_rating >= 4:
            st.markdown(f"<div class='star-label'>{get_rating_label(4)}</div>", unsafe_allow_html=True)
    
    with col5:
        if st.button("⭐⭐⭐⭐⭐", key="star5", use_container_width=True):
            select_rating(5)
        if st.session_state.selected_rating >= 5:
            st.markdown(f"<div class='star-label'>{get_rating_label(5)}</div>", unsafe_allow_html=True)
    
    # عرض التقييم المحدد مع وصف
    if st.session_state.selected_rating > 0:
        st.markdown(f"""
        <div class='rating-description'>
            <h4 style='color: #FFD700; text-align: center;'>
                🎯 {t('your_rating')}: {st.session_state.selected_rating} ⭐ - {get_rating_label(st.session_state.selected_rating)}
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        # حقل التعليق المتطور
        st.markdown(f"<p style='color: white; text-align: center; margin-top: 2rem;'>💬 {t('your_comment')}</p>", unsafe_allow_html=True)
        comment = st.text_area(
            "",
            placeholder="أخبرنا عن تجربتك مع التطبيق...",
            height=100,
            key="rating_comment"
        )
        
        # زر إرسال التقييم المتطور
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                f"🚀 {t('submit_rating')}",
                type="primary",
                use_container_width=True,
                use_container_width=True
            ):
                add_rating(st.session_state.selected_rating, comment)
                st.markdown(f"""
                <div class='rating-success'>
                    <h3>🎉 {t('thank_you_rating')}</h3>
                    <p>تقييمك يساعدنا على التحسين المستمر</p>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.selected_rating = 0
                st.balloons()
                st.rerun()
    
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); text-align: center; margin-top: 3rem;'>
        <h3 style='color: white;'>📋 {t('version_info')}</h3>
        <div style='display: flex; justify-content: center; gap: 3rem; margin: 1.5rem 0;'>
            <div>
                <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0;'><strong>🔄 {t('version')}:</strong></p>
                <p style='color: #FFD700; font-size: 1.2rem; font-weight: bold;'>1.1</p>
            </div>
            <div>
                <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0;'><strong>📅 {t('release_date')}:</strong></p>
                <p style='color: #667eea; font-size: 1.2rem; font-weight: bold;'>أكتوبر 2025</p>
            </div>
            <div>
                <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0;'><strong>⚡ الحالة:</strong></p>
                <p style='color: #51cf66; font-size: 1.2rem; font-weight: bold;'>⭐ {t('status_stable')}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== التذييل =====
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: white; padding: 2rem 0;'>
    <p style='margin: 0.3rem 0; font-size: 1.1rem;'><strong>{t('footer')}</strong></p>
    <p style='margin: 0.3rem 0; opacity: 0.9;'>{t('subtitle')}</p>
    <p style='margin: 0.3rem 0; opacity: 0.8;'>{t('rights')}</p>
    <p style='margin: 0.3rem 0; font-size: 0.9rem; opacity: 0.7;'>{t('team')}</p>
</div>
""", unsafe_allow_html=True)
