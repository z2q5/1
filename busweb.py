import streamlit as st
import pandas as pd
import datetime
import os
import requests
import json
import time
import random
import plotly.express as px
import plotly.graph_objects as go

# ===== إعداد الصفحة =====
st.set_page_config(
    page_title="Smart Bus System - Al Munira Private School", 
    layout="wide",
    page_icon="🚍"
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
if "student_status_cache" not in st.session_state:
    st.session_state.student_status_cache = {}

DATA_FILE = "attendance_data.csv"
STUDENTS_FILE = "students_data.csv"
RATINGS_FILE = "ratings_data.csv"

# ===== الترجمة الشاملة لكل النصوص =====
translations = {
    "ar": {
        # العناوين الرئيسية
        "student": "الطالب",
        "driver": "السائق", 
        "parents": "أولياء الأمور",
        "admin": "الإدارة",
        "weather": "الطقس",
        "about": "حول البرنامج",
        "school_name": "مدرسة المنيرة الخاصة - أبوظبي",
        "smart_bus_system": "نظام الباص الذكي",
        "welcome": "مرحباً بك في نظام الباص الذكي",
        
        # أزرار وتحكم
        "search": "بحث",
        "submit": "إرسال",
        "login": "تسجيل الدخول",
        "logout": "تسجيل الخروج",
        "confirm": "تأكيد",
        "cancel": "إلغاء",
        "save": "حفظ",
        "delete": "حذف",
        "edit": "تعديل",
        "add": "إضافة",
        "update": "تحديث",
        "refresh": "تحديث",
        "download": "تحميل",
        "upload": "رفع",
        "select": "اختر",
        "change": "تغيير",
        
        # نصوص الصفحات
        "student_attendance": "تسجيل حضور الطالب",
        "search_by_ministry_id": "ابحث برقم الوزارة",
        "enter_ministry_id": "أدخل رقم الوزارة",
        "student_name": "اسم الطالب",
        "grade": "الصف",
        "bus_number": "رقم الباص",
        "today_status": "الحالة اليوم",
        "coming": "سأحضر",
        "not_coming": "لن أحضر",
        "confirm_status": "تأكيد الحالة",
        "status_recorded": "تم تسجيل الحالة بنجاح",
        "already_registered": "لقد سجلت حالتك مسبقاً",
        "current_status": "الحالة الحالية",
        "status_valid_until": "الحالة سارية حتى",
        "change_status": "تغيير الحالة",
        
        "driver_dashboard": "لوحة تحكم السائق",
        "select_bus": "اختر الباص",
        "password": "كلمة المرور",
        "incorrect_password": "كلمة مرور غير صحيحة",
        "student_list": "قائمة الطلاب",
        "students_coming": "الطلاب القادمون",
        "no_data_today": "لا توجد بيانات للباص اليوم",
        
        "parents_portal": "بوابة أولياء الأمور",
        "enter_student_id": "أدخل رقم الوزارة الخاص بابنك/ابنتك",
        "attendance_tracking": "متابعة الحضور",
        "bus_information": "معلومات الباص",
        "latest_status": "آخر حالة",
        "last_update": "آخر تحديث",
        "approximate_morning_time": "وقت الصباح التقريبي",
        "approximate_afternoon_time": "وقت الظهيرة التقريبي",
        
        "admin_panel": "لوحة تحكم الإدارة",
        "admin_password": "كلمة مرور الإدارة",
        "access_granted": "تم الدخول بنجاح",
        "attendance_data": "بيانات الحضور",
        "download_csv": "تحميل كملف CSV",
        "reports_analytics": "التقارير والإحصائيات",
        "attendance_reports": "تقارير الحضور",
        "student_management": "إدارة الطلاب",
        "add_new_student": "إضافة طالب جديد",
        "parent_phone": "هاتف ولي الأمر",
        "student_added": "تم إضافة الطالب بنجاح",
        
        "weather_forecast": "توقعات الطقس",
        "temperature": "درجة الحرارة",
        "humidity": "الرطوبة",
        "wind_speed": "سرعة الرياح",
        "uv_index": "مؤشر الأشعة فوق البنفسجية",
        "air_quality": "جودة الهواء",
        "weather_impact": "تأثير الطقس على الحضور",
        
        "about_system": "حول النظام",
        "system_concept": "فكرة النظام",
        "objective": "الهدف",
        "features": "المميزات",
        "technologies": "التقنيات",
        "benefits": "الفوائد",
        "development_team": "فريق التطوير",
        "lead_developer": "المطور الرئيسي",
        "designer": "مصمم الجرافيك",
        "supervisor": "المشرف",
        
        # الإحصائيات
        "today_stats": "إحصائيات اليوم",
        "total_students": "إجمالي الطلاب",
        "present_today": "الحاضرون اليوم",
        "attendance_rate": "نسبة الحضور",
        "buses_operating": "الباصات العاملة",
        "total_registered": "إجمالي المسجلين",
        "expected_attendance": "الحضور المتوقع",
        "expected_absent": "الغياب المتوقع",
        "average_rating": "متوسط التقييم",
        "total_ratings": "إجمالي التقييمات",
        
        # الرسائل
        "success": "نجح",
        "error": "خطأ",
        "warning": "تحذير",
        "info": "معلومات",
        "loading": "جاري التحميل",
        "processing": "جاري المعالجة",
        "saved_successfully": "تم الحفظ بنجاح",
        "updated_successfully": "تم التحديث بنجاح",
        "deleted_successfully": "تم الحذف بنجاح",
        
        # أيام الأسبوع
        "monday": "الإثنين",
        "tuesday": "الثلاثاء",
        "wednesday": "الأربعاء",
        "thursday": "الخميس",
        "friday": "الجمعة",
        "saturday": "السبت",
        "sunday": "الأحد",
        
        # أزرار اللغة
        "arabic": "العربية",
        "english": "English",
        
        # تقييم النظام
        "rating_system": "نظام التقييم",
        "rate_system": "قيم النظام",
        "your_rating": "تقييمك",
        "comments": "ملاحظاتك",
        "submit_rating": "إرسال التقييم",
        "thank_you_rating": "شكراً لتقييمك النظام",
        
        # حقوق الطبع
        "all_rights_reserved": "جميع الحقوق محفوظة",
        "version": "الإصدار",
        
        # الترجمات المضافة
        "hours": "ساعة",
        "minutes": "دقيقة", 
        "invalid_id": "رقم غير صحيح",
        "dashboard": "لوحة التحكم",
        "registered_students": "طالب مسجل",
        "students_confirmed_attendance": "طالب أكد الحضور",
        "attendance_percentage": "نسبة الحضور",
        "attendance_trends": "اتجاهات الحضور",
        "daily_attendance": "الحضور اليومي",
        "bus_distribution": "توزيع الباصات",
        "grade_distribution": "توزيع الصفوف",
        "relative_humidity": "الرطوبة النسبية",
        "wind_conditions": "ظروف الرياح",
        "uv_radiation": "الإشعاع فوق البنفسجي",
        "weather_impact_on_attendance": "تأثير الطقس على الحضور",
        "system_objective_description": "يهدف نظام الباص الذكي إلى تحسين إدارة النقل المدرسي وتوفير تجربة آمنة ومريحة للطلاب وأولياء الأمور.",
        "real_time_tracking": "تتبع في الوقت الحقيقي",
        "smart_notifications": "إشعارات ذكية",
        "weather_integration": "دمج بيانات الطقس",
        "analytics_reports": "تقارير وتحليلات متقدمة",
        "multi_language": "دعم متعدد اللغات",
        "contact_info": "معلومات الاتصال",
        "no_ratings_yet": "لا توجد تقييمات حتى الآن",
        "rating_distribution": "توزيع التقييمات",
        "environmental_club": "قسم النادي البيئي",
        "graphics_designer": "مصمم الجرافيك",
        "system_features": "مميزات النظام",
        "environmental_friendly": "صديق للبيئة",
        "real_time_monitoring": "مراقبة في الوقت الحقيقي",
        "smart_analytics": "تحليلات ذكية",
        "multi_platform": "متعدد المنصات",
        "easy_to_use": "سهل الاستخدام",
        "secure_system": "نظام آمن",
        "cost_effective": "موفر للتكاليف",
        "time_saving": "موفر للوقت",
        "parent_communication": "تواصل مع أولياء الأمور",
        "bus_tracking": "تتبع الباصات",
        "attendance_management": "إدارة الحضور",
        "weather_alerts": "تنبيهات الطقس",
        "reports_generation": "إنشاء التقارير"
    },
    "en": {
        # Main Titles
        "student": "Student",
        "driver": "Driver",
        "parents": "Parents",
        "admin": "Admin",
        "weather": "Weather",
        "about": "About",
        "school_name": "Al Munira Private School - Abu Dhabi",
        "smart_bus_system": "Smart Bus System",
        "welcome": "Welcome to Smart Bus System",
        
        # Buttons and Controls
        "search": "Search",
        "submit": "Submit",
        "login": "Login",
        "logout": "Logout",
        "confirm": "Confirm",
        "cancel": "Cancel",
        "save": "Save",
        "delete": "Delete",
        "edit": "Edit",
        "add": "Add",
        "update": "Update",
        "refresh": "Refresh",
        "download": "Download",
        "upload": "Upload",
        "select": "Select",
        "change": "Change",
        
        # Page Texts
        "student_attendance": "Student Attendance",
        "search_by_ministry_id": "Search by Ministry ID",
        "enter_ministry_id": "Enter Ministry ID",
        "student_name": "Student Name",
        "grade": "Grade",
        "bus_number": "Bus Number",
        "today_status": "Today's Status",
        "coming": "Coming",
        "not_coming": "Not Coming",
        "confirm_status": "Confirm Status",
        "status_recorded": "Status recorded successfully",
        "already_registered": "You have already registered today",
        "current_status": "Current Status",
        "status_valid_until": "Status valid until",
        "change_status": "Change Status",
        
        "driver_dashboard": "Driver Dashboard",
        "select_bus": "Select Bus",
        "password": "Password",
        "incorrect_password": "Incorrect password",
        "student_list": "Student List",
        "students_coming": "Students Coming",
        "no_data_today": "No data for this bus today",
        
        "parents_portal": "Parents Portal",
        "enter_student_id": "Enter your child's Ministry ID",
        "attendance_tracking": "Attendance Tracking",
        "bus_information": "Bus Information",
        "latest_status": "Latest Status",
        "last_update": "Last Update",
        "approximate_morning_time": "Approximate Morning Time",
        "approximate_afternoon_time": "Approximate Afternoon Time",
        
        "admin_panel": "Admin Panel",
        "admin_password": "Admin Password",
        "access_granted": "Access granted",
        "attendance_data": "Attendance Data",
        "download_csv": "Download as CSV",
        "reports_analytics": "Reports & Analytics",
        "attendance_reports": "Attendance Reports",
        "student_management": "Student Management",
        "add_new_student": "Add New Student",
        "parent_phone": "Parent Phone",
        "student_added": "Student added successfully",
        
        "weather_forecast": "Weather Forecast",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "wind_speed": "Wind Speed",
        "uv_index": "UV Index",
        "air_quality": "Air Quality",
        "weather_impact": "Weather Impact on Attendance",
        
        "about_system": "About the System",
        "system_concept": "System Concept",
        "objective": "Objective",
        "features": "Features",
        "technologies": "Technologies",
        "benefits": "Benefits",
        "development_team": "Development Team",
        "lead_developer": "Lead Developer",
        "designer": "Graphics Designer",
        "supervisor": "Supervisor",
        
        # Statistics
        "today_stats": "Today's Statistics",
        "total_students": "Total Students",
        "present_today": "Present Today",
        "attendance_rate": "Attendance Rate",
        "buses_operating": "Buses Operating",
        "total_registered": "Total Registered",
        "expected_attendance": "Expected Attendance",
        "expected_absent": "Expected Absent",
        "average_rating": "Average Rating",
        "total_ratings": "Total Ratings",
        
        # Messages
        "success": "Success",
        "error": "Error",
        "warning": "Warning",
        "info": "Info",
        "loading": "Loading",
        "processing": "Processing",
        "saved_successfully": "Saved successfully",
        "updated_successfully": "Updated successfully",
        "deleted_successfully": "Deleted successfully",
        
        # Days of the week
        "monday": "Monday",
        "tuesday": "Tuesday",
        "wednesday": "Wednesday",
        "thursday": "Thursday",
        "friday": "Friday",
        "saturday": "Saturday",
        "sunday": "Sunday",
        
        # Language buttons
        "arabic": "العربية",
        "english": "English",
        
        # Rating System
        "rating_system": "Rating System",
        "rate_system": "Rate System",
        "your_rating": "Your Rating",
        "comments": "Your Comments",
        "submit_rating": "Submit Rating",
        "thank_you_rating": "Thank you for rating the system",
        
        # Copyright
        "all_rights_reserved": "All Rights Reserved",
        "version": "Version",
        
        # Added translations
        "hours": "hours",
        "minutes": "minutes",
        "invalid_id": "Invalid ID",
        "dashboard": "Dashboard",
        "registered_students": "registered students",
        "students_confirmed_attendance": "students confirmed attendance",
        "attendance_percentage": "attendance percentage",
        "attendance_trends": "Attendance Trends",
        "daily_attendance": "Daily Attendance",
        "bus_distribution": "Bus Distribution",
        "grade_distribution": "Grade Distribution",
        "relative_humidity": "Relative Humidity",
        "wind_conditions": "Wind Conditions",
        "uv_radiation": "UV Radiation",
        "weather_impact_on_attendance": "Weather Impact on Attendance",
        "system_objective_description": "The Smart Bus System aims to improve school transportation management and provide a safe and comfortable experience for students and parents.",
        "real_time_tracking": "Real-time tracking",
        "smart_notifications": "Smart notifications",
        "weather_integration": "Weather data integration",
        "analytics_reports": "Advanced analytics and reports",
        "multi_language": "Multi-language support",
        "contact_info": "Contact Information",
        "no_ratings_yet": "No ratings yet",
        "rating_distribution": "Rating Distribution",
        "environmental_club": "Environmental Club Department",
        "graphics_designer": "Graphics Designer",
        "system_features": "System Features",
        "environmental_friendly": "Environmentally Friendly",
        "real_time_monitoring": "Real-time Monitoring",
        "smart_analytics": "Smart Analytics",
        "multi_platform": "Multi-Platform",
        "easy_to_use": "Easy to Use",
        "secure_system": "Secure System",
        "cost_effective": "Cost Effective",
        "time_saving": "Time Saving",
        "parent_communication": "Parent Communication",
        "bus_tracking": "Bus Tracking",
        "attendance_management": "Attendance Management",
        "weather_alerts": "Weather Alerts",
        "reports_generation": "Reports Generation"
    }
}

def t(key):
    """دالة الترجمة"""
    return translations[st.session_state.lang].get(key, key)

def switch_lang():
    """تبديل اللغة"""
    st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
    st.rerun()

# ===== تحميل البيانات =====
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["id","name","grade","bus","status","time","date","expiry_time"])

def load_students():
    if os.path.exists(STUDENTS_FILE):
        return pd.read_csv(STUDENTS_FILE)
    default_students = [
        {"id": "1001", "name": "أحمد محمد", "grade": "10-A", "bus": "1", "parent_phone": "0501234567"},
        {"id": "1002", "name": "فاطمة علي", "grade": "9-B", "bus": "2", "parent_phone": "0507654321"},
        {"id": "1003", "name": "خالد إبراهيم", "grade": "8-C", "bus": "3", "parent_phone": "0505555555"},
        {"id": "1004", "name": "سارة عبدالله", "grade": "10-B", "bus": "1", "parent_phone": "0504444444"},
        {"id": "1005", "name": "محمد حسن", "grade": "7-A", "bus": "2", "parent_phone": "0503333333"},
    ]
    return pd.DataFrame(default_students)

def load_ratings():
    if os.path.exists(RATINGS_FILE):
        return pd.read_csv(RATINGS_FILE)
    return pd.DataFrame(columns=["rating", "comments", "timestamp"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def save_students(df):
    df.to_csv(STUDENTS_FILE, index=False)

def save_ratings(df):
    df.to_csv(RATINGS_FILE, index=False)

if 'df' not in st.session_state:
    st.session_state.df = load_data()

if 'students_df' not in st.session_state:
    st.session_state.students_df = load_students()

if 'ratings_df' not in st.session_state:
    st.session_state.ratings_df = load_ratings()

# ===== كلمات المرور =====
bus_passwords = {"1": "1111", "2": "2222", "3": "3333"}
admin_pass = "admin123"

# ===== وظائف مساعدة =====
def add_notification(message):
    st.session_state.notifications.append({
        "time": datetime.datetime.now().strftime("%H:%M"),
        "message": message
    })

def get_abu_dhabi_weather():
    """طقس أبوظبي مع بيانات مفصلة"""
    try:
        import random
        temp = random.randint(28, 42)
        humidity = random.randint(30, 80)
        wind_speed = random.randint(5, 25)
        uv_index = random.randint(3, 11)
        
        conditions_ar = ["مشمس", "غائم جزئياً", "صافي", "مغبر", "رطب"]
        conditions_en = ["Sunny", "Partly Cloudy", "Clear", "Dusty", "Humid"]
        air_quality_levels = ["ممتازة", "جيدة", "متوسطة", "سيئة"]
        air_quality_en = ["Excellent", "Good", "Moderate", "Poor"]
        
        condition_idx = random.randint(0, 4)
        air_idx = random.randint(0, 3)
        
        return {
            "temp": temp,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "uv_index": uv_index,
            "condition_ar": conditions_ar[condition_idx],
            "condition_en": conditions_en[condition_idx],
            "air_quality_ar": air_quality_levels[air_idx],
            "air_quality_en": air_quality_en[air_idx]
        }
    except:
        return {
            "temp": 32, "humidity": 60, "wind_speed": 15, 
            "uv_index": 8, "condition_ar": "مشمس", "condition_en": "Sunny",
            "air_quality_ar": "جيدة", "air_quality_en": "Good"
        }

def calculate_attendance_stats():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_data = st.session_state.df[st.session_state.df["date"] == today] if "date" in st.session_state.df.columns else pd.DataFrame()
    
    if today_data.empty:
        return {"total": 0, "coming": 0, "not_coming": 0, "percentage": 0}
    
    total = len(today_data)
    coming = len(today_data[today_data["status"] == "قادم"])
    not_coming = len(today_data[today_data["status"] == "لن يأتي"])
    percentage = (coming / total * 100) if total > 0 else 0
    
    return {
        "total": total,
        "coming": coming,
        "not_coming": not_coming,
        "percentage": percentage
    }

def has_student_registered_today(student_id):
    """التحقق إذا كان الطالب سجل اليوم ولم تنته المدة"""
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    # البحث في البيانات المحفوظة
    student_data = st.session_state.df[
        (st.session_state.df["id"] == student_id) & 
        (st.session_state.df["date"] == today)
    ]
    
    if not student_data.empty:
        latest_record = student_data.iloc[-1]
        if "expiry_time" in latest_record and pd.notna(latest_record["expiry_time"]):
            try:
                expiry_time = datetime.datetime.strptime(latest_record["expiry_time"], "%Y-%m-%d %H:%M:%S")
                if now < expiry_time:
                    return True, latest_record["status"], expiry_time
            except:
                pass
    return False, None, None

def add_rating(rating, comments):
    """إضافة تقييم جديد"""
    new_rating = pd.DataFrame([{
        "rating": rating,
        "comments": comments,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    st.session_state.ratings_df = pd.concat([st.session_state.ratings_df, new_rating], ignore_index=True)
    save_ratings(st.session_state.ratings_df)

def get_ratings_stats():
    """الحصول على إحصائيات التقييمات"""
    if st.session_state.ratings_df.empty:
        return {"average": 0, "total": 0}
    
    return {
        "average": st.session_state.ratings_df["rating"].mean(),
        "total": len(st.session_state.ratings_df)
    }

# ===== واجهة مستخدم متطورة =====
st.markdown(f"""
    <style>
    .main-header {{
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}
    .stat-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
        border-left: 5px solid #2a5298;
        transition: transform 0.3s ease;
    }}
    .stat-card:hover {{
        transform: translateY(-5px);
    }}
    .weather-card {{
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
    }}
    .report-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }}
    .quick-action-btn {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem;
        border-radius: 15px;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    .quick-action-btn:hover {{
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }}
    .student-card {{
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 5px solid #667eea;
    }}
    .rating-card {{
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }}
    .feature-card {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        text-align: center;
    }}
    .team-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-top: 5px solid #667eea;
    }}
    </style>
""", unsafe_allow_html=True)

# ===== الهيدر الرئيسي =====
col1, col2, col3 = st.columns([2, 3, 1])

with col1:
    weather_data = get_abu_dhabi_weather()
    temp = weather_data["temp"]
    condition = weather_data["condition_ar"] if st.session_state.lang == "ar" else weather_data["condition_en"]
    st.metric(f"🌡️ {t('temperature')}", f"{temp}°C", f"{condition}")

with col2:
    st.markdown(f"""
    <div class='main-header'>
        <h1>🚍 {t('smart_bus_system')}</h1>
        <h3>{t('school_name')}</h3>
        <p>{t('welcome')}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    lang_button_text = t('english') if st.session_state.lang == "ar" else t('arabic')
    if st.button(f"🌐 {lang_button_text}", use_container_width=True, type="primary"):
        switch_lang()

# ===== الشريط العلوي =====
pages = [
    ("🧑‍🎓 " + t("student"), "student"),
    ("🚌 " + t("driver"), "driver"), 
    ("👨‍👩‍👧 " + t("parents"), "parents"),
    ("🏫 " + t("admin"), "admin"),
    ("🌦️ " + t("weather"), "weather"),
    ("ℹ️ " + t("about"), "about")
]

cols = st.columns(len(pages))
for i, (name, page_key) in enumerate(pages):
    if cols[i].button(name, use_container_width=True):
        st.session_state.page = page_key

st.markdown("---")

# ===== صفحة الطالب =====
if st.session_state.page == "student":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎓 " + t("student_attendance"))
        
        search_id = st.text_input("🔍 " + t("search_by_ministry_id"))
        if search_id:
            student_info = st.session_state.students_df[st.session_state.students_df["id"] == search_id]
            if not student_info.empty:
                student = student_info.iloc[0]
                
                st.markdown(f"""
                <div class='student-card'>
                    <h3>🎓 {student['name']}</h3>
                    <p><strong>{t('grade')}:</strong> {student['grade']}</p>
                    <p><strong>{t('bus_number')}:</strong> {student['bus']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # التحقق إذا كان الطالب سجل مسبقاً
                already_registered, current_status, expiry_time = has_student_registered_today(search_id)
                
                if already_registered:
                    remaining_time = expiry_time - datetime.datetime.now()
                    hours_remaining = int(remaining_time.total_seconds() / 3600)
                    minutes_remaining = int((remaining_time.total_seconds() % 3600) / 60)
                    
                    status_display = "قادم" if current_status == "قادم" else "لن يأتي"
                    if st.session_state.lang == "en":
                        status_display = "Coming" if current_status == "قادم" else "Not Coming"
                    
                    st.warning(f"""
                    ⚠️ **{t('already_registered')}**
                    
                    **{t('current_status')}:** {status_display}
                    **{t('status_valid_until')}:** {expiry_time.strftime("%H:%M")}
                    **{t('hours_remaining')}:** {hours_remaining} {t('hours')} {minutes_remaining} {t('minutes')}
                    """)
                    
                    if st.button(t('change_status'), type="secondary"):
                        # إعادة تعيين الحالة للسماح بالتسجيل الجديد
                        st.session_state.df = st.session_state.df[
                            ~((st.session_state.df["id"] == search_id) & 
                              (st.session_state.df["date"] == datetime.datetime.now().strftime("%Y-%m-%d")))
                        ]
                        save_data(st.session_state.df)
                        st.rerun()
                else:
                    coming_text = "سأحضر اليوم" if st.session_state.lang == "ar" else "I will come today"
                    not_coming_text = "لن أحضر اليوم" if st.session_state.lang == "ar" else "I will not come today"
                    
                    status = st.radio(t("today_status"), 
                                    [f"✅ {coming_text}", f"❌ {not_coming_text}"],
                                    key="status_radio")
                    
                    if st.button(t("confirm_status"), type="primary"):
                        now = datetime.datetime.now()
                        status_text = "قادم" if "سأحضر" in status or "come" in status else "لن يأتي"
                        
                        # حساب وقت الانتهاء (12 ساعة من الآن)
                        expiry_time = now + datetime.timedelta(hours=12)
                        
                        new_entry = pd.DataFrame([[
                            student["id"], student["name"], student["grade"], 
                            student["bus"], status_text,
                            now.strftime("%H:%M"),
                            now.strftime("%Y-%m-%d"),
                            expiry_time.strftime("%Y-%m-%d %H:%M:%S")
                        ]], columns=["id","name","grade","bus","status","time","date","expiry_time"])
                        
                        st.session_state.df = pd.concat([st.session_state.df, new_entry], ignore_index=True)
                        save_data(st.session_state.df)
                        
                        st.balloons()
                        success_msg = f"✅ {t('status_recorded')} - {t('status_valid_until')} {expiry_time.strftime('%H:%M')}"
                        st.success(success_msg)
                        
                        add_notification(f"طالب جديد سجل حضوره: {student['name']} - الباص {student['bus']}")

    with col2:
        st.subheader("📊 " + t("today_stats"))
        stats = calculate_attendance_stats()
        
        st.metric(t("total_registered"), stats["total"])
        st.metric(t("expected_attendance"), stats["coming"])
        st.metric(t("attendance_rate"), f"{stats['percentage']:.1f}%")

# ===== صفحة السائق =====
elif st.session_state.page == "driver":
    st.subheader("🚌 " + t("driver_dashboard"))
    
    if not st.session_state.driver_logged_in:
        col1, col2 = st.columns(2)
        with col1:
            bus_number = st.selectbox(t("select_bus"), ["1", "2", "3"])
        with col2:
            password = st.text_input(t("password"), type="password")
        
        if st.button(t("login")):
            if password == bus_passwords.get(bus_number, ""):
                st.session_state.driver_logged_in = True
                st.session_state.current_bus = bus_number
                st.success("✅ " + t("access_granted"))
                st.rerun()
            else:
                st.error("❌ " + t("incorrect_password"))
    else:
        st.success(f"✅ {t('access_granted')} - {t('bus_number')} {st.session_state.current_bus}")
        
        if st.button(t("logout")):
            st.session_state.driver_logged_in = False
            st.rerun()
        
        # قائمة طلاب الباص
        st.subheader(f"📋 {t('student_list')} - {t('bus_number')} {st.session_state.current_bus}")
        bus_students = st.session_state.students_df[st.session_state.students_df["bus"] == st.session_state.current_bus]
        
        if not bus_students.empty:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            today_data = st.session_state.df[
                (st.session_state.df["date"] == today) & 
                (st.session_state.df["bus"] == st.session_state.current_bus)
            ] if "date" in st.session_state.df.columns else pd.DataFrame()
            
            coming_students = today_data[today_data["status"] == "قادم"]
            
            st.metric(t("students_coming"), len(coming_students))
            
            for _, student in coming_students.iterrows():
                st.write(f"✅ {student['name']} - {student['grade']} - {student['time']}")
        else:
            st.info(t("no_data_today"))

# ===== صفحة أولياء الأمور =====
elif st.session_state.page == "parents":
    st.subheader("👨‍👩‍👧 " + t("parents_portal"))
    
    student_id = st.text_input(t("enter_student_id"))
    if student_id:
        student_info = st.session_state.students_df[st.session_state.students_df["id"] == student_id]
        if not student_info.empty:
            student = student_info.iloc[0]
            welcome_msg = f"مرحباً! تم العثور على الطالب: {student['name']}" if st.session_state.lang == "ar" else f"Welcome! Student found: {student['name']}"
            st.success(welcome_msg)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 " + t("attendance_tracking"))
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                today_status = st.session_state.df[
                    (st.session_state.df["id"] == student_id) & 
                    (st.session_state.df["date"] == today)
                ] if "date" in st.session_state.df.columns else pd.DataFrame()
                
                if not today_status.empty:
                    status = today_status.iloc[0]["status"]
                    time = today_status.iloc[0]["time"]
                    status_display = "قادم" if status == "قادم" else "لن يأتي"
                    if st.session_state.lang == "en":
                        status_display = "Coming" if status == "قادم" else "Not Coming"
                    
                    st.success(f"{t('latest_status')}: {status_display} - {t('last_update')}: {time}")
                else:
                    no_data_msg = "لا توجد بيانات حضور لهذا اليوم" if st.session_state.lang == "ar" else "No attendance data for today"
                    st.info(no_data_msg)
            
            with col2:
                st.subheader("🚌 " + t("bus_information"))
                st.write(f"{t('bus_number')}: {student['bus']}")
                st.write(f"{t('approximate_morning_time')}: 7:00 AM")
                st.write(f"{t('approximate_afternoon_time')}: 2:00 PM")
        else:
            st.error(t("invalid_id"))

# ===== صفحة الإدارة =====
elif st.session_state.page == "admin":
    st.subheader("🏫 " + t("admin_panel"))
    
    admin_password = st.text_input(t("admin_password"), type="password")
    if admin_password == admin_pass:
        st.success("✅ " + t("access_granted"))
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            t("dashboard"), 
            t("attendance_data"), 
            t("reports_analytics"), 
            t("student_management"), 
            t("rating_system")
        ])
        
        with tab1:
            st.subheader("📊 " + t("dashboard"))
            
            # إحصائيات سريعة
            stats = calculate_attendance_stats()
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>👥 {t('total_students')}</h3>
                    <h2>{len(st.session_state.students_df)}</h2>
                    <p style='font-size: 14px; color: #666;'>{t('registered_students')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>✅ {t('present_today')}</h3>
                    <h2>{stats['coming']}</h2>
                    <p style='font-size: 14px; color: #666;'>{t('students_confirmed_attendance')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>📈 {t('attendance_rate')}</h3>
                    <h2>{stats['percentage']:.1f}%</h2>
                    <p style='font-size: 14px; color: #666;'>{t('attendance_percentage')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                ratings_stats = get_ratings_stats()
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>⭐ {t('average_rating')}</h3>
                    <h2>{ratings_stats['average']:.1f}/5</h2>
                    <p style='font-size: 14px; color: #666;'>{t('total_ratings')}: {ratings_stats['total']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # مخطط الحضور
            st.subheader("📈 " + t("attendance_trends"))
            if not st.session_state.df.empty:
                attendance_by_date = st.session_state.df.groupby('date').size()
                fig = px.line(attendance_by_date, title=t("daily_attendance"))
                st.plotly_chart(fig)
        
        with tab2:
            st.subheader("📋 " + t("attendance_data"))
            st.dataframe(st.session_state.df)
            
            if st.button("📥 " + t("download_csv")):
                csv = st.session_state.df.to_csv(index=False)
                st.download_button(
                    label=t("download"),
                    data=csv,
                    file_name=f"attendance_data_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with tab3:
            st.subheader("📊 " + t("reports_analytics"))
            
            col1, col2 = st.columns(2)
            
            with col1:
                # توزيع الحضور حسب الباص
                if not st.session_state.df.empty:
                    bus_distribution = st.session_state.df.groupby('bus').size()
                    fig = px.pie(bus_distribution, values=bus_distribution.values, 
                                names=bus_distribution.index, title=t("bus_distribution"))
                    st.plotly_chart(fig)
            
            with col2:
                # توزيع الحضور حسب الصف
                if not st.session_state.df.empty:
                    grade_distribution = st.session_state.df.groupby('grade').size()
                    fig = px.bar(grade_distribution, x=grade_distribution.index, 
                                y=grade_distribution.values, title=t("grade_distribution"))
                    st.plotly_chart(fig)
        
        with tab4:
            st.subheader("👥 " + t("student_management"))
            
            st.dataframe(st.session_state.students_df)
            
            with st.expander("➕ " + t("add_new_student")):
                with st.form("add_student_form"):
                    new_id = st.text_input("ID")
                    new_name = st.text_input(t("student_name"))
                    new_grade = st.text_input(t("grade"))
                    new_bus = st.text_input(t("bus_number"))
                    new_phone = st.text_input(t("parent_phone"))
                    
                    if st.form_submit_button(t("add")):
                        new_student = pd.DataFrame([{
                            "id": new_id,
                            "name": new_name,
                            "grade": new_grade,
                            "bus": new_bus,
                            "parent_phone": new_phone
                        }])
                        st.session_state.students_df = pd.concat([st.session_state.students_df, new_student], ignore_index=True)
                        save_students(st.session_state.students_df)
                        st.success("✅ " + t("student_added"))
                        st.rerun()
        
        with tab5:
            st.subheader("⭐ " + t("rating_system"))
            
            if not st.session_state.ratings_df.empty:
                st.dataframe(st.session_state.ratings_df)
                
                # إحصائيات التقييمات
                ratings_stats = get_ratings_stats()
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(t("average_rating"), f"{ratings_stats['average']:.1f}/5")
                
                with col2:
                    st.metric(t("total_ratings"), ratings_stats['total'])
                
                # مخطط التقييمات
                rating_dist = st.session_state.ratings_df['rating'].value_counts().sort_index()
                fig = px.bar(rating_dist, x=rating_dist.index, y=rating_dist.values,
                            title=t("rating_distribution"))
                st.plotly_chart(fig)
            else:
                st.info("ℹ️ " + t("no_ratings_yet"))
    
    elif admin_password and admin_password != admin_pass:
        st.error("❌ " + t("incorrect_password"))

# ===== صفحة الطقس =====
elif st.session_state.page == "weather":
    st.subheader("🌦️ " + t("weather_forecast"))
    
    weather_data = get_abu_dhabi_weather()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>🌡️ {t('temperature')}</h3>
            <h2>{weather_data['temp']}°C</h2>
            <p>{weather_data['condition_ar'] if st.session_state.lang == 'ar' else weather_data['condition_en']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>💧 {t('humidity')}</h3>
            <h2>{weather_data['humidity']}%</h2>
            <p>{t('relative_humidity')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>💨 {t('wind_speed')}</h3>
            <h2>{weather_data['wind_speed']} km/h</h2>
            <p>{t('wind_conditions')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>☀️ {t('uv_index')}</h3>
            <h2>{weather_data['uv_index']}</h2>
            <p>{t('uv_radiation')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # تأثير الطقس على الحضور
    st.subheader("📊 " + t("weather_impact"))
    
    impact_data = {
        "condition": ["مشمس", "ممطر", "عاصف", "حار جداً"] if st.session_state.lang == "ar" else ["Sunny", "Rainy", "Windy", "Very Hot"],
        "attendance_rate": [95, 85, 90, 88]
    }
    impact_df = pd.DataFrame(impact_data)
    
    fig = px.bar(impact_df, x='condition', y='attendance_rate', 
                 title=t("weather_impact_on_attendance"))
    st.plotly_chart(fig)

# ===== صفحة حول النظام =====
elif st.session_state.page == "about":
    st.subheader("ℹ️ " + t("about_system"))
    
    # قسم المميزات
    st.markdown("### 🚀 " + t("system_features"))
    
    features_ar = [
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
    
    features_en = [
        "🌱 Environmentally Friendly System",
        "⏱️ Real-time Monitoring", 
        "📊 Smart Analytics",
        "📱 Multi-Platform",
        "🎯 Easy to Use",
        "🔒 Secure System",
        "💰 Cost Effective",
        "⏰ Time Saving",
        "👨‍👩‍👧‍👦 Parent Communication",
        "🚍 Bus Tracking",
        "📝 Attendance Management",
        "🌦️ Weather Alerts",
        "📈 Reports Generation"
    ]
    
    features = features_ar if st.session_state.lang == "ar" else features_en
    
    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 15px;
                margin: 0.5rem 0;
                text-align: center;
                border: none;
            '>
                <h4 style='color: white; margin: 0;'>{feature}</h4>
            </div>
            """, unsafe_allow_html=True)
    
    # قسم فريق التطوير
    st.markdown("### 👨‍💻 " + t("development_team"))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 0.5rem 0;
        '>
            <h3 style='color: white;'>💻 {t('lead_developer')}</h3>
            <h2 style='color: white; margin: 1rem 0;'>إياد مصطفى</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 0.5rem 0;
        '>
            <h3 style='color: white;'>🎨 {t('designer')}</h3>
            <h2 style='color: white; margin: 1rem 0;'>ايمن جلال</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 0.5rem 0;
        '>
            <h3 style='color: white;'>👨‍🏫 {t('supervisor')}</h3>
            <h2 style='color: white; margin: 1rem 0;'>قسم النادي البيئي</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # قسم التقنيات
    st.markdown("### 💻 " + t("technologies"))
    
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("""
        <div style='
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
        '>
            <h4>🐍 تقنيات البرمجة:</h4>
            <ul>
                <li>Python 3.11</li>
                <li>Streamlit Framework</li>
                <li>Pandas للبيانات</li>
                <li>Plotly للرسوم البيانية</li>
                <li>datetime لإدارة الوقت</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_col2:
        st.markdown("""
        <div style='
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
        '>
            <h4>📊 إدارة البيانات:</h4>
            <ul>
                <li>CSV Files</li>
                <li>Pandas DataFrames</li>
                <li>Session State Management</li>
                <li>Real-time Updates</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # قسم الهدف
    st.markdown("### 🎯 " + t("objective"))
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    '>
        <h3 style='color: white; text-align: center;'>رؤية ورسالة النظام</h3>
        <p style='color: white; text-align: center; font-size: 1.1rem;'>{t('system_objective_description')}</p>
        <p style='color: white; text-align: center;'><strong>💡 رؤيتنا:</strong> أن نكون النظام الرائد في إدارة النقل المدرسي الذكي</p>
        <p style='color: white; text-align: center;'><strong>🎯 رسالتنا:</strong> توفير نظام متكامل وآمن وفعال لإدارة نقل الطلاب</p>
    </div>
    """, unsafe_allow_html=True)
    
    # نظام التقييم
    st.markdown("### ⭐ " + t("rate_system"))
    
    with st.form("rating_form"):
        rating = st.slider(t("your_rating"), 1, 5, 5)
        comments = st.text_area(t("comments"))
        
        if st.form_submit_button(t("submit_rating")):
            add_rating(rating, comments)
            st.success("✅ " + t("thank_you_rating"))

# ===== الشريط السفلي =====
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])

with footer_col1:
    st.markdown(f"© 2024 {t('school_name')}. {t('all_rights_reserved')}")

with footer_col2:
    if st.session_state.notifications:
        with st.expander(f"🔔 الإشعارات ({len(st.session_state.notifications)})"):
            for notification in st.session_state.notifications[-5:]:
                st.write(f"{notification['time']}: {notification['message']}")

with footer_col3:
    if st.button("🔄 " + t("refresh")):
        st.rerun()

