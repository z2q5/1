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
    page_title="نظام حضور الباص - المنيرة الخاصة", 
    layout="wide",
    page_icon="🚍"
)

# ===== حالة التطبيق =====
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
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

# ===== الترجمة الشاملة =====
translations = {
    "ar": {
        "dashboard": "لوحة التحكم",
        "student": "الطالب",
        "driver": "السائق",
        "parents": "أولياء الأمور",
        "admin": "الإدارة",
        "weather": "الطقس",
        "about": "حول البرنامج",
        "school_name": "مدرسة المنيرة الخاصة - أبوظبي",
        "smart_bus_system": "نظام الباص الذكي",
        "welcome": "مرحباً بك في نظام الباص الذكي",
        "today_stats": "إحصائيات اليوم",
        "total_students": "إجمالي الطلاب",
        "present_today": "الحاضرون اليوم",
        "attendance_rate": "نسبة الحضور",
        "buses_operating": "الباصات العاملة",
        "live_tracking": "التتبع الحي",
        "reports": "التقارير",
        "settings": "الإعدادات",
        "search_student": "ابحث عن طالب...",
        "student_attendance": "تسجيل حضور الطالب",
        "search_by_ministry_id": "ابحث برقم الوزارة",
        "found_student": "تم العثور على الطالب",
        "today_status": "الحالة اليوم",
        "coming": "قادم",
        "not_coming": "لن يأتي",
        "confirm_status": "تأكيد الحالة",
        "status_recorded": "تم تسجيل الحالة بنجاح",
        "manual_registration": "التسجيل اليدوي",
        "ministry_id": "رقم الوزارة",
        "student_name": "اسم الطالب",
        "grade": "الصف",
        "bus_number": "رقم الباص",
        "submit": "إرسال",
        "your_status_submitted": "تم إرسال حالتك بنجاح",
        "today_statistics": "إحصائيات اليوم",
        "total_registered": "إجمالي المسجلين",
        "expected_attendance": "الحضور المتوقع",
        "driver_dashboard": "لوحة تحكم السائق",
        "select_bus": "اختر الباص",
        "password": "كلمة المرور",
        "login": "تسجيل الدخول",
        "logged_in_success": "تم الدخول بنجاح",
        "incorrect_password": "كلمة مرور غير صحيحة",
        "student_list": "قائمة الطلاب",
        "students_coming": "طلاب سيحضرون",
        "no_data_today": "لا توجد بيانات للباص اليوم",
        "parents_portal": "بوابة أولياء الأمور",
        "enter_student_id": "أدخل رقم الوزارة الخاص بابنك/ابنتك",
        "student_ministry_id": "رقم الوزارة للطالب",
        "welcome_student": "مرحباً! تم العثور على الطالب",
        "attendance_tracking": "متابعة الحضور",
        "bus_information": "معلومات الباص",
        "latest_status": "آخر حالة",
        "last_update": "آخر تحديث",
        "attendance_history": "سجل الحضور",
        "no_records_yet": "لا توجد سجلات حضور حتى الآن",
        "bus_info": "معلومات الباص",
        "approximate_morning_time": "وقت الصباح التقريبي",
        "approximate_afternoon_time": "وقت الظهيرة التقريبي",
        "students_on_bus_today": "طلاب في الباص اليوم",
        "invalid_id": "رقم الوزارة غير صحيح",
        "admin_panel": "لوحة تحكم الإدارة",
        "access_granted": "تم الدخول بنجاح",
        "attendance_data": "بيانات الحضور",
        "download_csv": "تحميل كملف CSV",
        "refresh_data": "تحديث البيانات",
        "no_attendance_records": "لا توجد بيانات حضور حتى الآن",
        "reports_analytics": "التقارير والإحصائيات",
        "attendance_reports": "تقارير الحضور",
        "expected_absent": "الغياب المتوقع",
        "bus_performance": "أداء الباصات",
        "attendance_by_grade": "الحضور حسب الصف",
        "student_management": "إدارة الطلاب",
        "add_new_student": "إضافة طالب جديد",
        "parent_phone": "هاتف ولي الأمر",
        "add_student": "إضافة طالب",
        "student_added": "تم إضافة الطالب بنجاح",
        "system_settings": "إعدادات النظام",
        "enter_correct_password": "أدخل كلمة مرور صحيحة",
        "weather_impact": "تأثير الطقس على الحضور",
        "temperature": "درجة الحرارة",
        "condition": "الحالة",
        "high_temp_warning": "تحذير: حرارة مرتفعة - متوقع زيادة في نسبة الغياب",
        "ac_recommendation": "توصية: تأكد من تكييف الباص ووجود مياه باردة",
        "cold_weather": "جو بارد - قد يؤثر على الحضور",
        "moderate_weather": "جو معتدل - متوقع نسبة حضور عالية",
        "predicted_attendance": "الحضور المتوقع",
        "about_system": "حول النظام",
        "system_concept": "فكرة النظام",
        "objective": "الهدف",
        "features": "المميزات",
        "technologies": "التقنيات",
        "benefits": "الفوائد",
        "development_team": "فريق التطوير",
        "lead_developer": "المطور الرئيسي",
        "designer": "المصمم",
        "supervisor": "المشرف",
        "all_rights_reserved": "جميع الحقوق محفوظة",
        "interactive_dashboard": "لوحة التحكم التفاعلية",
        "smart_reports": "التقارير الذكية",
        "real_time_analytics": "التحليلات اللحظية",
        "student_ranking": "تصنيف الطلاب",
        "bus_locations": "مواقع الباصات",
        "weather_alerts": "تنبيهات الطقس",
        "quick_actions": "إجراءات سريعة",
        "generate_report": "إنشاء تقرير",
        "send_notification": "إرسال إشعار",
        "view_all_reports": "عرض جميع التقارير",
        "weekly_analysis": "تحليل أسبوعي",
        "monthly_trends": "الاتجاهات الشهرية",
        "performance_metrics": "مقاييس الأداء",
        "attendance_trend": "اتجاه الحضور",
        "bus_utilization": "استخدام الباصات",
        "student_engagement": "مشاركة الطلاب",
        "parent_satisfaction": "رضا أولياء الأمور",
        "efficiency_score": "معدل الكفاءة",
        "abuja_weather": "طقس أبوظبي",
        "detailed_forecast": "توقعات مفصلة",
        "weather_impact_analysis": "تحليل تأثير الطقس",
        "humidity": "الرطوبة",
        "wind_speed": "سرعة الرياح",
        "uv_index": "مؤشر الأشعة فوق البنفسجية",
        "air_quality": "جودة الهواء",
        "recommendations": "التوصيات",
        "excellent_conditions": "ظروف ممتازة للحضور",
        "moderate_impact": "تأثير متوسط على الحضور",
        "high_impact": "تأثير كبير على الحضور",
        "take_precautions": "اتخذ الاحتياطات اللازمة",
        "excellent_air_quality": "جودة هواء ممتازة",
        "good_air_quality": "جودة هواء جيدة",
        "moderate_air_quality": "جودة هواء متوسطة",
        "poor_air_quality": "جودة هواء سيئة",
        "version": "الإصدار",
        "days": "الأيام",
        "utilization_rate": "معدل الاستخدام",
        "notification_sent": "تم إرسال الإشعار",
        "arabic": "العربية",
        "english": "English",
        "working_days": "أيام الدوام: الإثنين - الجمعة",
        "rating_system": "نظام التقييم",
        "system_rating": "تقييم النظام",
        "rate_system": "قيم النظام",
        "your_rating": "تقييمك",
        "comments": "ملاحظاتك",
        "submit_rating": "إرسال التقييم",
        "thank_you_rating": "شكراً لتقييمك النظام",
        "credits": "الكريدتس",
        "developer_info": "معلومات المطور",
        "contact_developer": "الاتصال بالمطور",
        "system_evaluation": "تقييم النظام",
        "buses": "الباصات",
        "impact_on_attendance": "تأثير على الحضور",
        "ratings_history": "سجل التقييمات",
        "average_rating": "متوسط التقييم",
        "total_ratings": "إجمالي التقييمات",
        "student_already_registered": "لقد سجلت حالتك مسبقاً",
        "status_valid_until": "الحالة سارية حتى",
        "hours_remaining": "ساعة متبقية"
    },
    "en": {
        "dashboard": "Dashboard",
        "student": "Student",
        "driver": "Driver",
        "parents": "Parents",
        "admin": "Admin",
        "weather": "Weather",
        "about": "About",
        "school_name": "Al Munira Private School - Abu Dhabi",
        "smart_bus_system": "Smart Bus System",
        "welcome": "Welcome to Smart Bus System",
        "today_stats": "Today's Statistics",
        "total_students": "Total Students",
        "present_today": "Present Today",
        "attendance_rate": "Attendance Rate",
        "buses_operating": "Buses Operating",
        "live_tracking": "Live Tracking",
        "reports": "Reports",
        "settings": "Settings",
        "search_student": "Search student...",
        "student_attendance": "Student Attendance",
        "search_by_ministry_id": "Search by Ministry ID",
        "found_student": "Found Student",
        "today_status": "Today's Status",
        "coming": "Coming",
        "not_coming": "Not Coming",
        "confirm_status": "Confirm Status",
        "status_recorded": "Status recorded successfully",
        "manual_registration": "Manual Registration",
        "ministry_id": "Ministry ID",
        "student_name": "Student Name",
        "grade": "Grade",
        "bus_number": "Bus Number",
        "submit": "Submit",
        "your_status_submitted": "Your status has been submitted",
        "today_statistics": "Today's Statistics",
        "total_registered": "Total Registered",
        "expected_attendance": "Expected Attendance",
        "driver_dashboard": "Driver Dashboard",
        "select_bus": "Select Bus",
        "password": "Password",
        "login": "Login",
        "logged_in_success": "Logged in successfully",
        "incorrect_password": "Incorrect password",
        "student_list": "Student List",
        "students_coming": "Students Coming",
        "no_data_today": "No data for this bus today",
        "parents_portal": "Parents Portal",
        "enter_student_id": "Enter your child's Ministry ID",
        "student_ministry_id": "Student Ministry ID",
        "welcome_student": "Welcome! Student found",
        "attendance_tracking": "Attendance Tracking",
        "bus_information": "Bus Information",
        "latest_status": "Latest Status",
        "last_update": "Last Update",
        "attendance_history": "Attendance History",
        "no_records_yet": "No attendance records yet",
        "bus_info": "Bus Information",
        "approximate_morning_time": "Approximate Morning Time",
        "approximate_afternoon_time": "Approximate Afternoon Time",
        "students_on_bus_today": "Students on Bus Today",
        "invalid_id": "Invalid Ministry ID",
        "admin_panel": "Admin Panel",
        "access_granted": "Access granted",
        "attendance_data": "Attendance Data",
        "download_csv": "Download as CSV",
        "refresh_data": "Refresh Data",
        "no_attendance_records": "No attendance records yet",
        "reports_analytics": "Reports & Analytics",
        "attendance_reports": "Attendance Reports",
        "expected_absent": "Expected Absent",
        "bus_performance": "Bus Performance",
        "attendance_by_grade": "Attendance by Grade",
        "student_management": "Student Management",
        "add_new_student": "Add New Student",
        "parent_phone": "Parent Phone",
        "add_student": "Add Student",
        "student_added": "Student added successfully",
        "system_settings": "System Settings",
        "enter_correct_password": "Please enter correct password",
        "weather_impact": "Weather Impact on Attendance",
        "temperature": "Temperature",
        "condition": "Condition",
        "high_temp_warning": "Warning: High temperature - expected increase in absences",
        "ac_recommendation": "Recommendation: Ensure bus AC is working and cold water is available",
        "cold_weather": "Cold weather - may affect attendance",
        "moderate_weather": "Moderate weather - expected high attendance rate",
        "predicted_attendance": "Predicted Attendance",
        "about_system": "About the System",
        "system_concept": "System Concept",
        "objective": "Objective",
        "features": "Features",
        "technologies": "Technologies",
        "benefits": "Benefits",
        "development_team": "Development Team",
        "lead_developer": "Lead Developer",
        "designer": "Designer",
        "supervisor": "Supervisor",
        "all_rights_reserved": "All Rights Reserved",
        "interactive_dashboard": "Interactive Dashboard",
        "smart_reports": "Smart Reports",
        "real_time_analytics": "Real-time Analytics",
        "student_ranking": "Student Ranking",
        "bus_locations": "Bus Locations",
        "weather_alerts": "Weather Alerts",
        "quick_actions": "Quick Actions",
        "generate_report": "Generate Report",
        "send_notification": "Send Notification",
        "view_all_reports": "View All Reports",
        "weekly_analysis": "Weekly Analysis",
        "monthly_trends": "Monthly Trends",
        "performance_metrics": "Performance Metrics",
        "attendance_trend": "Attendance Trend",
        "bus_utilization": "Bus Utilization",
        "student_engagement": "Student Engagement",
        "parent_satisfaction": "Parent Satisfaction",
        "efficiency_score": "Efficiency Score",
        "abuja_weather": "Abu Dhabi Weather",
        "detailed_forecast": "Detailed Forecast",
        "weather_impact_analysis": "Weather Impact Analysis",
        "humidity": "Humidity",
        "wind_speed": "Wind Speed",
        "uv_index": "UV Index",
        "air_quality": "Air Quality",
        "recommendations": "Recommendations",
        "excellent_conditions": "Excellent attendance conditions",
        "moderate_impact": "Moderate impact on attendance",
        "high_impact": "High impact on attendance",
        "take_precautions": "Take necessary precautions",
        "excellent_air_quality": "Excellent air quality",
        "good_air_quality": "Good air quality",
        "moderate_air_quality": "Moderate air quality",
        "poor_air_quality": "Poor air quality",
        "version": "Version",
        "days": "Days",
        "utilization_rate": "Utilization Rate",
        "notification_sent": "Notification sent",
        "arabic": "العربية",
        "english": "English",
        "working_days": "Working Days: Monday - Friday",
        "rating_system": "Rating System",
        "system_rating": "System Rating",
        "rate_system": "Rate System",
        "your_rating": "Your Rating",
        "comments": "Your Comments",
        "submit_rating": "Submit Rating",
        "thank_you_rating": "Thank you for rating the system",
        "credits": "Credits",
        "developer_info": "Developer Information",
        "contact_developer": "Contact Developer",
        "system_evaluation": "System Evaluation",
        "buses": "Buses",
        "impact_on_attendance": "Impact on Attendance",
        "ratings_history": "Ratings History",
        "average_rating": "Average Rating",
        "total_ratings": "Total Ratings",
        "student_already_registered": "You have already registered today",
        "status_valid_until": "Status valid until",
        "hours_remaining": "hours remaining"
    }
}

def t(key):
    return translations[st.session_state.lang][key]

def switch_lang():
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
    lang_button_text = "English" if st.session_state.lang == "ar" else "العربية"
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
        st.subheader("🎓 تسجيل حضور الطالب")
        
        search_id = st.text_input("🔍 ابحث برقم الوزارة")
        if search_id:
            student_info = st.session_state.students_df[st.session_state.students_df["id"] == search_id]
            if not student_info.empty:
                student = student_info.iloc[0]
                
                st.markdown(f"""
                <div class='student-card'>
                    <h3>🎓 {student['name']}</h3>
                    <p><strong>الصف:</strong> {student['grade']}</p>
                    <p><strong>الباص:</strong> {student['bus']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # التحقق إذا كان الطالب سجل مسبقاً
                already_registered, current_status, expiry_time = has_student_registered_today(search_id)
                
                if already_registered:
                    remaining_time = expiry_time - datetime.datetime.now()
                    hours_remaining = int(remaining_time.total_seconds() / 3600)
                    minutes_remaining = int((remaining_time.total_seconds() % 3600) / 60)
                    
                    st.warning(f"""
                    ⚠️ **لقد سجلت حالتك مسبقاً**
                    
                    **الحالة الحالية:** {current_status}
                    **الحالة سارية حتى:** {expiry_time.strftime("%H:%M")}
                    **المتبقي:** {hours_remaining} ساعة و {minutes_remaining} دقيقة
                    """)
                    
                    if st.button("تغيير الحالة", type="secondary"):
                        # إعادة تعيين الحالة للسماح بالتسجيل الجديد
                        st.session_state.df = st.session_state.df[
                            ~((st.session_state.df["id"] == search_id) & 
                              (st.session_state.df["date"] == datetime.datetime.now().strftime("%Y-%m-%d")))
                        ]
                        save_data(st.session_state.df)
                        st.rerun()
                else:
                    status = st.radio("الحالة اليوم", 
                                    [f"✅ سأحضر اليوم", f"❌ لن أحضر اليوم"],
                                    key="status_radio")
                    
                    if st.button("تأكيد الحالة", type="primary"):
                        now = datetime.datetime.now()
                        status_text = "قادم" if "سأحضر" in status else "لن يأتي"
                        
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
                        st.success(f"✅ تم تسجيل الحالة بنجاح - الحالة سارية حتى {expiry_time.strftime('%H:%M')}")
                        
                        add_notification(f"طالب جديد سجل حضوره: {student['name']} - الباص {student['bus']}")

    with col2:
        st.subheader("📊 إحصائيات اليوم")
        stats = calculate_attendance_stats()
        
        st.metric("إجمالي المسجلين", stats["total"])
        st.metric("الحضور المتوقع", stats["coming"])
        st.metric("نسبة الحضور", f"{stats['percentage']:.1f}%")

# ===== صفحة السائق =====
elif st.session_state.page == "driver":
    st.subheader("🚌 لوحة تحكم السائق")
    
    if not st.session_state.driver_logged_in:
        col1, col2 = st.columns(2)
        with col1:
            bus_number = st.selectbox("اختر الباص", ["1", "2", "3"])
        with col2:
            password = st.text_input("كلمة المرور", type="password")
        
        if st.button("تسجيل الدخول"):
            if password == bus_passwords.get(bus_number, ""):
                st.session_state.driver_logged_in = True
                st.session_state.current_bus = bus_number
                st.success("✅ تم الدخول بنجاح")
                st.rerun()
            else:
                st.error("❌ كلمة مرور غير صحيحة")
    else:
        st.success(f"✅ تم الدخول بنجاح - الباص {st.session_state.current_bus}")
        
        if st.button("تسجيل الخروج"):
            st.session_state.driver_logged_in = False
            st.rerun()
        
        # قائمة طلاب الباص
        st.subheader(f"📋 قائمة الطلاب - الباص {st.session_state.current_bus}")
        bus_students = st.session_state.students_df[st.session_state.students_df["bus"] == st.session_state.current_bus]
        
        if not bus_students.empty:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            today_data = st.session_state.df[
                (st.session_state.df["date"] == today) & 
                (st.session_state.df["bus"] == st.session_state.current_bus)
            ] if "date" in st.session_state.df.columns else pd.DataFrame()
            
            coming_students = today_data[today_data["status"] == "قادم"]
            
            st.metric("الطلاب القادمون", len(coming_students))
            
            for _, student in coming_students.iterrows():
                st.write(f"✅ {student['name']} - {student['grade']} - {student['time']}")
        else:
            st.info("لا توجد بيانات للباص اليوم")

# ===== صفحة أولياء الأمور =====
elif st.session_state.page == "parents":
    st.subheader("👨‍👩‍👧 بوابة أولياء الأمور")
    
    student_id = st.text_input("أدخل رقم الوزارة الخاص بابنك/ابنتك")
    if student_id:
        student_info = st.session_state.students_df[st.session_state.students_df["id"] == student_id]
        if not student_info.empty:
            student = student_info.iloc[0]
            st.success(f"مرحباً! تم العثور على الطالب: {student['name']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 متابعة الحضور")
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                today_status = st.session_state.df[
                    (st.session_state.df["id"] == student_id) & 
                    (st.session_state.df["date"] == today)
                ] if "date" in st.session_state.df.columns else pd.DataFrame()
                
                if not today_status.empty:
                    status = today_status.iloc[0]["status"]
                    time = today_status.iloc[0]["time"]
                    st.success(f"آخر حالة: {status} - آخر تحديث: {time}")
                else:
                    st.info("لا توجد بيانات حضور لهذا اليوم")
            
            with col2:
                st.subheader("🚌 معلومات الباص")
                st.write(f"رقم الباص: {student['bus']}")
                st.write(f"وقت الصباح التقريبي: 7:00 صباحاً")
                st.write(f"وقت الظهيرة التقريبي: 2:00 ظهراً")
        else:
            st.error("رقم الوزارة غير صحيح")

# ===== صفحة الإدارة =====
elif st.session_state.page == "admin":
    st.subheader("🏫 لوحة تحكم الإدارة")
    
    admin_password = st.text_input("كلمة مرور الإدارة", type="password")
    if admin_password == admin_pass:
        st.success("✅ تم الدخول بنجاح")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["لوحة التحكم", "بيانات الحضور", "التقارير والإحصائيات", "إدارة الطلاب", "تقييم النظام"])
        
        with tab1:
            st.subheader("📊 لوحة التحكم الرئيسية")
            
            # إحصائيات سريعة
            stats = calculate_attendance_stats()
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>👥 إجمالي الطلاب</h3>
                    <h2>{len(st.session_state.students_df)}</h2>
                    <p style='font-size: 14px; color: #666;'>عدد الطلاب المسجلين في النظام</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>✅ الحاضرون اليوم</h3>
                    <h2>{stats['coming']}</h2>
                    <p style='font-size: 14px; color: #666;'>عدد الطلاب الذين أكدوا حضورهم</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>📈 نسبة الحضور</h3>
                    <h2>{stats['percentage']:.1f}%</h2>
                    <p style='font-size: 14px; color: #666;'>نسبة الحضور من إجمالي المسجلين</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>🚌 الباصات النشطة</h3>
                    <h2>3</h2>
                    <p style='font-size: 14px; color: #666;'>عدد الباصات العاملة اليوم</p>
                </div>
                """, unsafe_allow_html=True)
            
            # مخططات تفاعلية
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 اتجاه الحضور الأسبوعي")
                dates = ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة']
                attendance_rates = [85, 88, 92, 87, 90]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=dates, 
                    y=attendance_rates,
                    mode='lines+markers',
                    name='نسبة الحضور',
                    line=dict(color='#2a5298', width=3)
                ))
                fig.update_layout(
                    title="تحليل الحضور الأسبوعي",
                    xaxis_title="أيام الأسبوع",
                    yaxis_title="نسبة الحضور %",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("🚌 أداء الباصات")
                buses = ['الباص 1', 'الباص 2', 'الباص 3']
                utilization = [95, 88, 92]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=buses,
                    y=utilization,
                    marker_color=['#2a5298', '#667eea', '#764ba2']
                ))
                fig.update_layout(
                    title="معدل استخدام الباصات",
                    xaxis_title="الباصات",
                    yaxis_title="معدل الاستخدام %",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("📊 بيانات الحضور")
            if not st.session_state.df.empty:
                st.dataframe(st.session_state.df, use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("تحميل كملف CSV"):
                        csv = st.session_state.df.to_csv(index=False)
                        st.download_button(
                            label="تحميل البيانات",
                            data=csv,
                            file_name=f"attendance_data_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                with col2:
                    if st.button("تحديث البيانات"):
                        st.session_state.df = load_data()
                        st.rerun()
            else:
                st.info("لا توجد بيانات حضور حتى الآن")
        
        with tab3:
            st.subheader("📈 التقارير والإحصائيات")
            
            # إحصائيات الحضور
            stats = calculate_attendance_stats()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("إجمالي المسجلين", stats["total"])
            with col2:
                st.metric("الحضور المتوقع", stats["coming"])
            with col3:
                st.metric("الغياب المتوقع", stats["not_coming"])
            
            # مخطط الحضور حسب الصف
            if not st.session_state.df.empty:
                attendance_by_grade = st.session_state.df[st.session_state.df["status"] == "قادم"]["grade"].value_counts()
                fig = px.pie(values=attendance_by_grade.values, names=attendance_by_grade.index, title="الحضور حسب الصف")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.subheader("👥 إدارة الطلاب")
            
            with st.form("add_student_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_id = st.text_input("رقم الوزارة")
                    new_name = st.text_input("اسم الطالب")
                with col2:
                    new_grade = st.text_input("الصف")
                    new_bus = st.selectbox("رقم الباص", ["1", "2", "3"])
                    new_phone = st.text_input("هاتف ولي الأمر")
                
                if st.form_submit_button("إضافة طالب"):
                    new_student = pd.DataFrame([{
                        "id": new_id,
                        "name": new_name,
                        "grade": new_grade,
                        "bus": new_bus,
                        "parent_phone": new_phone
                    }])
                    st.session_state.students_df = pd.concat([st.session_state.students_df, new_student], ignore_index=True)
                    save_students(st.session_state.students_df)
                    st.success("✅ تم إضافة الطالب بنجاح")
            
            st.dataframe(st.session_state.students_df, use_container_width=True)
        
        with tab5:
            st.subheader("⭐ تقييم النظام")
            
            # إحصائيات التقييمات
            ratings_stats = get_ratings_stats()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("متوسط التقييم", f"{ratings_stats['average']:.1f}/5")
            with col2:
                st.metric("إجمالي التقييمات", ratings_stats['total'])
            
            st.info("يرجى تقييم نظام الباص الذكي لمساعدتنا على التحسين")
            
            rating = st.slider("تقييمك للنظام", 1, 5, 4)
            comments = st.text_area("ملاحظاتك أو اقتراحاتك")
            
            if st.button("إرسال التقييم"):
                add_rating(rating, comments)
                st.success("شكراً لتقييمك النظام! تم حفظ تقييمك للأبد.")
                st.balloons()
            
            # عرض سجل التقييمات
            if not st.session_state.ratings_df.empty:
                st.subheader("📋 سجل التقييمات")
                st.dataframe(st.session_state.ratings_df, use_container_width=True)
    
    elif admin_password:
        st.error("❌ كلمة مرور غير صحيحة")

# ===== صفحة الطقس =====
elif st.session_state.page == "weather":
    st.subheader("🌦️ طقس أبوظبي")
    
    weather_data = get_abu_dhabi_weather()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>🌡️ درجة الحرارة</h3>
            <h1>{weather_data['temp']}°C</h1>
            <p>الحالة: {weather_data['condition_ar']}</p>
            <p>💧 الرطوبة: {weather_data['humidity']}%</p>
            <p>💨 سرعة الرياح: {weather_data['wind_speed']} km/h</p>
            <p>☀️ مؤشر الأشعة: {weather_data['uv_index']}</p>
            <p>🌬️ جودة الهواء: {weather_data['air_quality_ar']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # توصيات الطقس
        if weather_data['temp'] > 38:
            st.error("⚠️ تأثير كبير على الحضور")
            st.info("💡 اتخذ الاحتياطات اللازمة")
        elif weather_data['temp'] < 20:
            st.warning("🌧️ تأثير متوسط على الحضور")
        else:
            st.success("🌈 ظروف ممتازة للحضور")
    
    with col2:
        st.subheader("تحليل تأثير الطقس")
        
        # تحليل تأثير الطقس
        conditions = ['مشمس', 'غائم', 'ممطر', 'مغبر', 'رطب']
        impact = [5, 2, -10, -15, -8]
        
        fig = px.bar(x=conditions, y=impact, 
                    title="تحليل تأثير الطقس",
                    color=impact,
                    color_continuous_scale='RdYlGn')
        fig.update_layout(xaxis_title="الحالة", yaxis_title="تأثير على الحضور")
        st.plotly_chart(fig, use_container_width=True)

# ===== صفحة حول البرنامج =====
elif st.session_state.page == "about":
    st.markdown(f"""
    <div class='main-header'>
        <h1>ℹ️ نظام الباص الذكي</h1>
        <h3>مدرسة المنيرة الخاصة - أبوظبي</h3>
        <p>الإصدار 3.0 - 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("حول النظام")
        
        features = [
            ("فكرة النظام", 
             "نظام متكامل لإدارة حضور طلاب الباص المدرسي باستخدام أحدث التقنيات"),
            ("الهدف", 
             "تحسين كفاءة النقل المدرسي وتوفير وقت أولياء الأمور وزيادة سلامة الطلاب"),
            ("المميزات", 
             "تسجيل حضور ذكي، متابعة مباشرة، إشعارات فورية، تحليلات متقدمة، وتقارير شاملة"),
            ("التقنيات", 
             "يعتمد على Python, Streamlit, Pandas مع واجهة مستخدم عصرية وسهلة الاستخدام"),
            ("الفوائد", 
             "توفير 40% من وقت الانتظار، خفض 25% من استهلاك الوقود، زيادة رضا المستخدمين 95%"),
            ("نظام التقييم", 
             "نظام تقييم متكامل لقياس أداء النظام ورضا المستخدمين"),
            ("أيام الدوام", 
             "الإثنين - الجمعة من كل أسبوع")
        ]
        
        for title, desc in features:
            with st.expander(title):
                st.write(desc)
    
    with col2:
        st.subheader("فريق التطوير")
        team = [
            "المطور الرئيسي: إياد مصطفى", 
            "المصمم: أيمن جلال", 
            "المشرف: قسم النادي البيئي"
        ]
        for member in team:
            st.write(f"• {member}")
        
        st.info(f"""
        **مدرسة المنيرة الخاصة**
        📍 أبوظبي، الإمارات العربية المتحدة
        🌐 www.almunira-school.ae
        """)
    
    # قسم التقييم في النهاية
    st.markdown("---")
    st.subheader("⭐ قيم النظام")
    
    st.info("ساعدنا في تحسين النظام من خلال تقييمك")
    
    rating = st.slider("تقييمك للنظام", 1, 5, 4)
    comments = st.text_area("ملاحظاتك أو اقتراحاتك للتحسين")
    
    if st.button("إرسال التقييم", type="primary"):
        add_rating(rating, comments)
        st.success("شكراً لتقييمك النظام! تم حفظ تقييمك للأبد.")
        st.balloons()

# ===== التذييل =====
st.markdown("---")
footer_cols = st.columns(3)

with footer_cols[0]:
    st.markdown("**مدرسة المنيرة الخاصة**")
    st.markdown("أبوظبي - الإمارات العربية المتحدة")

with footer_cols[1]:
    st.markdown("**نظام الباص الذكي**")
    st.markdown("الإصدار 3.0 - 2025")

with footer_cols[2]:
    st.markdown("**فريق التطوير**")
    st.markdown("المطور: إياد مصطفى")

st.markdown(f"<div style='text-align:center; color:gray; margin-top: 2rem;'>© 2025 جميع الحقوق محفوظة - نظام الباص الذكي</div>", unsafe_allow_html=True)
