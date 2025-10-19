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
        "admin_title": "🏫 لوحة تحكم الإدارة",
        "admin_login": "🔐 تسجيل دخول الإدارة",
        "admin_password": "كلمة مرور الإدارة",
        "system_stats": "إحصائيات النظام",
        "students_count": "عدد الطلاب",
        "attendance_records": "سجلات الحضور",
        "system_actions": "إجراءات النظام",
        "reset_data": "🔄 إعادة تعيين البيانات",
        "backup": "📥 نسخة احتياطية",
        "change_admin_password": "تغيير كلمة مرور الإدارة",
        "current_passwords": "كلمات المرور الحالية",
        "change_bus_password": "تغيير كلمات مرور الباصات",
        "select_bus_password": "اختر الباص",
        "new_password": "كلمة المرور الجديدة",
        "save_changes": "حفظ التغييرات",
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
        "password_updated": "تم تحديث كلمة المرور",
        "theme_light": "☀️ فاتح",
        "theme_dark": "🌙 مظلم",
        "toggle_theme": "تبديل الثيم",
        "current_theme": "الثيم الحالي",
        "language": "اللغة",
        "arabic": "العربية",
        "english": "الإنجليزية",
        "rating_system": "⭐ نظام التقييم",
        "rate_app": "قيم التطبيق",
        "your_rating": "تقييمك",
        "your_comment": "تعليقك (اختياري)",
        "submit_rating": "إرسال التقييم",
        "thank_you_rating": "شكراً لتقييمك!",
        "average_rating": "متوسط التقييم",
        "total_ratings": "إجمالي التقييمات",
        "rating_success": "تم إرسال تقييمك بنجاح",
        "select_rating": "اختر عدد النجوم"
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
        "admin_title": "🏫 Admin Control Panel",
        "admin_login": "🔐 Admin Login",
        "admin_password": "Admin Password",
        "system_stats": "System Statistics",
        "students_count": "Students Count",
        "attendance_records": "Attendance Records",
        "system_actions": "System Actions",
        "reset_data": "🔄 Reset Data",
        "backup": "📥 Backup",
        "change_admin_password": "Change Admin Password",
        "current_passwords": "Current Passwords",
        "change_bus_password": "Change Bus Passwords",
        "select_bus_password": "Select Bus",
        "new_password": "New Password",
        "save_changes": "Save Changes",
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
        "password_updated": "Password updated successfully",
        "theme_light": "☀️ Light",
        "theme_dark": "🌙 Dark",
        "toggle_theme": "Toggle Theme",
        "current_theme": "Current Theme",
        "language": "Language",
        "arabic": "Arabic",
        "english": "English",
        "rating_system": "⭐ Rating System",
        "rate_app": "Rate the App",
        "your_rating": "Your Rating",
        "your_comment": "Your Comment (Optional)",
        "submit_rating": "Submit Rating",
        "thank_you_rating": "Thank you for your rating!",
        "average_rating": "Average Rating",
        "total_ratings": "Total Ratings",
        "rating_success": "Your rating has been submitted successfully",
        "select_rating": "Select number of stars"
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

# ===== تصميم متطور بدون مربعات بيضاء =====
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
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
        }}
        
        .star-rating {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin: 1rem 0;
            font-size: 2rem;
        }}
        
        .star {{
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .star:hover {{
            transform: scale(1.2);
        }}
        
        .star.active {{
            color: #FFD700;
            text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
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

# ===== صفحة الطالب =====
if st.session_state.page == "student":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class='content-section'>
            <h2 class='section-title'>{t('student_title')}</h2>
            <p class='info-text'>{t('student_desc')}</p>
        </div>
        """, unsafe_allow_html=True)
        
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
                    <div class='student-card'>
                        <div style='text-align: center;'>
                            <h3 style='margin-bottom: 1rem;'>🎓 {student['name']}</h3>
                            <div style='display: flex; justify-content: center; gap: 1.5rem; margin-bottom: 1rem;'>
                                <div style='text-align: center;'>
                                    <div style='background: rgba(255,255,255,0.2); color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold;'>{t('grade')}: {student['grade']}</div>
                                </div>
                                <div style='text-align: center;'>
                                    <div style='background: rgba(255,255,255,0.2); color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold;'>{t('bus')}: {student['bus']}</div>
                                </div>
                            </div>
                            <p style='margin: 0; opacity: 0.9;'><strong>{t('parent_phone')}:</strong> {student['parent_phone']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    already_registered, current_status = has_student_registered_today(student_id)
                    
                    if already_registered:
                        status_color = "rgba(81, 207, 102, 0.3)" if current_status == "قادم" else "rgba(255, 107, 107, 0.3)"
                        status_icon = "✅" if current_status == "قادم" else "❌"
                        st.markdown(f"""
                        <div style='background: {status_color}; color: white; padding: 1.5rem; border-radius: 12px; text-align: center; margin: 1rem 0; border: 1px solid rgba(255,255,255,0.2);'>
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
                            save_data()
                            st.success(t("reset_success"))
                            st.rerun()
                    else:
                        st.markdown(f"<h4 style='text-align: center; color: white; margin-bottom: 1rem;'>{t('choose_status')}</h4>", unsafe_allow_html=True)
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("✅ سأحضر اليوم", use_container_width=True, type="primary"):
                                now = register_attendance(student, "قادم")
                                st.balloons()
                                st.success(f"""
                                **{t('registered_success')}**
                                
                                **{t('student_name')}:** {student['name']}
                                **{t('status')}:** قادم
                                **{t('time')}:** {now.strftime('%H:%M')}
                                **{t('bus_number')}:** {student['bus']}
                                """)
                                
                        with col_b:
                            if st.button("❌ لن أحضر اليوم", use_container_width=True, type="secondary"):
                                now = register_attendance(student, "لن يأتي")
                                st.success(f"""
                                **{t('registered_success')}**
                                
                                **{t('student_name')}:** {student['name']}
                                **{t('status')}:** لن أحضر
                                **{t('time')}:** {now.strftime('%H:%M')}
                                **{t('bus_number')}:** {student['bus']}
                                """)
                
                else:
                    st.error(f"❌ {t('not_found')}")
                    
            except Exception as e:
                st.error(f"❌ {t('error')}")

    with col2:
        st.markdown(f"<div style='text-align: center; margin-bottom: 1rem;'><h3 style='color: white;'>{t('stats_title')}</h3></div>", unsafe_allow_html=True)
        
        stats = calculate_attendance_stats()
        
        st.markdown(f"""
        <div class='stat-card'>
            <h3 style='margin-bottom: 0.5rem; font-size: 2rem;'>👥</h3>
            <h2 style='margin: 0; font-size: 2.5rem;'>{stats['total']}</h2>
            <p style='margin: 0; opacity: 0.9;'>{t('total_registered')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='stat-card'>
            <h3 style='margin-bottom: 0.5rem; font-size: 2rem;'>✅</h3>
            <h2 style='margin: 0; font-size: 2.5rem;'>{stats['coming']}</h2>
            <p style='margin: 0; opacity: 0.9;'>{t('expected_attendance')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='stat-card'>
            <h3 style='margin-bottom: 0.5rem; font-size: 2rem;'>📈</h3>
            <h2 style='margin: 0; font-size: 2.5rem;'>{stats['percentage']:.1f}%</h2>
            <p style='margin: 0; opacity: 0.9;'>{t('attendance_rate')}</p>
        </div>
        """, unsafe_allow_html=True)

# ===== صفحة السائق =====
elif st.session_state.page == "driver":
    st.subheader(t("driver_title"))
    
    if not st.session_state.driver_logged_in:
        st.markdown(f"<h3 style='text-align: center; color: white; margin-bottom: 2rem;'>{t('driver_login')}</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            bus_number = st.selectbox(t("select_bus"), ["1", "2", "3"])
        with col2:
            password = st.text_input(t("password"), type="password", placeholder=t("password_placeholder"))
        
        if st.button(t("login"), type="primary", use_container_width=True):
            if password == st.session_state.bus_passwords.get(bus_number, ""):
                st.session_state.driver_logged_in = True
                st.session_state.current_bus = bus_number
                st.success(t("login_success"))
                st.rerun()
            else:
                st.error(t("login_error"))
        
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
                (today_attendance["status"] == "قادم")
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
                    st.markdown(f"""
                    <div style='background: rgba(212, 237, 218, 0.2); padding: 1rem; border-radius: 10px; border-right: 5px solid #28a745; margin: 0.5rem 0;'>
                        <h4 style='color: white; margin: 0;'>✅ {student['name']}</h4>
                        <p style='color: rgba(255,255,255,0.8); margin: 0.3rem 0;'>📚 {student['grade']} | ⏰ {student['time']}</p>
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
                    if status == "قادم":
                        bg_color = "rgba(212, 237, 218, 0.2)"
                        border_color = "#28a745"
                        status_icon = "✅"
                    else:
                        bg_color = "rgba(248, 215, 218, 0.2)"
                        border_color = "#dc3545"
                        status_icon = "❌"
                else:
                    bg_color = "rgba(255, 243, 205, 0.2)"
                    border_color = "#ffc107"
                    status_icon = "⏳"
                
                st.markdown(f"""
                <div style='background: {bg_color}; padding: 1rem; border-radius: 10px; border-right: 5px solid {border_color}; margin: 0.5rem 0;'>
                    <h4 style='color: white; margin: 0;'>{status_icon} {student['name']}</h4>
                    <p style='color: rgba(255,255,255,0.8); margin: 0.3rem 0;'>📚 {student['grade']} | 📱 {student['parent_phone']}</p>
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
                    if status == "قادم":
                        st.success(f"**الحالة:** قادم 🎒\n**آخر تحديث:** {time}")
                    else:
                        st.error(f"**الحالة:** لن يأتي ❌\n**آخر تحديث:** {time}")
                else:
                    st.info("لا توجد بيانات حضور لهذا اليوم")
            
            with col2:
                st.subheader(t("bus_info"))
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2);'>
                    <p><strong>{t('bus')}:</strong> {student['bus']}</p>
                    <p><strong>{t('morning_time')}:</strong> 7:00 صباحاً</p>
                    <p><strong>{t('afternoon_time')}:</strong> 2:00 ظهراً</p>
                    <p><strong>{t('parent_phone')}:</strong> {student['parent_phone']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"❌ {t('not_found')}")

# ===== صفحة الإدارة =====
elif st.session_state.page == "admin":
    st.subheader(t("admin_title"))
    
    if not st.session_state.admin_logged_in:
        st.markdown(f"<h3 style='text-align: center; color: white; margin-bottom: 2rem;'>{t('admin_login')}</h3>", unsafe_allow_html=True)
        
        admin_password = st.text_input(t("admin_password"), type="password", placeholder=t("password_placeholder"))
        
        if st.button(t("login"), type="primary", use_container_width=True):
            if admin_password == st.session_state.admin_password:
                st.session_state.admin_logged_in = True
                st.success(t("login_success"))
                st.rerun()
            else:
                st.error(t("login_error"))
    
    else:
        st.success(f"✅ {t('login_success')}")
        
        if st.button(t("logout"), type="secondary"):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        tab1, tab2, tab3 = st.tabs([t("system_stats"), t("change_bus_password"), t("change_admin_password")])
        
        with tab1:
            st.header(t("system_stats"))
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(t("students_count"), len(st.session_state.students_df))
                st.metric(t("attendance_records"), len(st.session_state.attendance_df))
            
            with col2:
                st.subheader(t("system_actions"))
                if st.button(t("reset_data"), type="secondary", use_container_width=True):
                    initialize_data()
                    save_data()
                    st.success(t("data_reset_success"))
                
                if st.button(t("backup"), use_container_width=True):
                    save_data()
                    st.info(t("backup_success"))
        
        with tab2:
            st.header(t("change_bus_password"))
            
            st.subheader(t("current_passwords"))
            for bus, pwd in st.session_state.bus_passwords.items():
                st.write(f"**الباص {bus}:** {pwd}")
            
            bus_select = st.selectbox(t("select_bus_password"), ["1", "2", "3"])
            new_pass = st.text_input(t("new_password"), type="password")
            
            if st.button(t("save_changes")):
                if new_pass:
                    st.session_state.bus_passwords[bus_select] = new_pass
                    save_data()
                    st.success(f"✅ {t('password_updated')} {bus_select}")
        
        with tab3:
            st.header(t("change_admin_password"))
            
            current_admin_pass = st.text_input("كلمة المرور الحالية", type="password")
            new_admin_pass = st.text_input("كلمة المرور الجديدة", type="password")
            confirm_admin_pass = st.text_input("تأكيد كلمة المرور الجديدة", type="password")
            
            if st.button("تغيير كلمة المرور", type="primary"):
                if current_admin_pass == st.session_state.admin_password:
                    if new_admin_pass == confirm_admin_pass:
                        if new_admin_pass:
                            st.session_state.admin_password = new_admin_pass
                            save_data()
                            st.success("✅ تم تغيير كلمة مرور الإدارة بنجاح")
                        else:
                            st.error("❌ كلمة المرور الجديدة لا يمكن أن تكون فارغة")
                    else:
                        st.error("❌ كلمات المرور غير متطابقة")
                else:
                    st.error("❌ كلمة المرور الحالية غير صحيحة")

# ===== صفحة حول النظام مع التقييم =====
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
    
    # قسم التقييم
    st.markdown("---")
    st.subheader(t("rating_system"))
    
    # عرض إحصائيات التقييم
    avg_rating, total_ratings = get_average_rating()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='rating-card'>
            <h3>{t('average_rating')}</h3>
            <h1 style='font-size: 3rem; color: #FFD700;'>{avg_rating:.1f} ⭐</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='rating-card'>
            <h3>{t('total_ratings')}</h3>
            <h1 style='font-size: 3rem; color: #667eea;'>{total_ratings}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # نظام التقييم بدون استخدام st.form
    st.markdown(f"<h3 style='text-align: center; color: white; margin: 2rem 0;'>{t('rate_app')}</h3>", unsafe_allow_html=True)
    
    # أزرار النجوم
    st.markdown(f"<p style='color: white; text-align: center;'>{t('select_rating')}</p>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("⭐", key="star1", use_container_width=True):
            select_rating(1)
    with col2:
        if st.button("⭐⭐", key="star2", use_container_width=True):
            select_rating(2)
    with col3:
        if st.button("⭐⭐⭐", key="star3", use_container_width=True):
            select_rating(3)
    with col4:
        if st.button("⭐⭐⭐⭐", key="star4", use_container_width=True):
            select_rating(4)
    with col5:
        if st.button("⭐⭐⭐⭐⭐", key="star5", use_container_width=True):
            select_rating(5)
    
    # عرض التقييم المحدد
    if st.session_state.selected_rating > 0:
        st.info(f"📝 {t('your_rating')}: {st.session_state.selected_rating} ⭐")
        
        # حقل التعليق
        comment = st.text_area(t("your_comment"), placeholder="اكتب تعليقك هنا...")
        
        # زر إرسال التقييم
        if st.button(t("submit_rating"), type="primary", use_container_width=True):
            add_rating(st.session_state.selected_rating, comment)
            st.success(f"🎉 {t('rating_success')}")
            st.session_state.selected_rating = 0  # إعادة تعيين التقييم
            st.balloons()
            st.rerun()
    
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; border: 1px solid rgba(255,255,255,0.2); text-align: center; margin-top: 2rem;'>
        <h3 style='color: white;'>{t('version_info')}</h3>
        <p style='color: rgba(255,255,255,0.9);'><strong>{t('version')}:</strong> 1.1</p>
        <p style='color: rgba(255,255,255,0.9);'><strong>{t('release_date')}:</strong> أكتوبر 2025</p>
        <p style='color: rgba(255,255,255,0.9);'><strong>الحالة:</strong> ⭐ {t('status_stable')}</p>
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
