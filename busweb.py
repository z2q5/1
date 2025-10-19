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
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

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
        "not_found": "لم يتم العثور على الطالب",
        "error": "حدث خطأ في النظام",
        "reset_success": "تم إعادة تعيين حالتك",
        "login_success": "تم الدخول بنجاح",
        "login_error": "كلمة مرور غير صحيحة",
        "data_reset_success": "تم إعادة تعيين البيانات",
        "backup_success": "تم إنشاء نسخة احتياطية",
        "password_updated": "تم تحديث كلمة المرور",
        "theme_light": "☀️",
        "theme_dark": "🌙",
        "language": "🌐",
        "rating_system": "⭐ نظام التقييم المتطور",
        "rate_app": "قيم تجربتك مع التطبيق",
        "your_rating": "تقييمك",
        "your_comment": "شاركنا رأيك (اختياري)",
        "submit_rating": "إرسال التقييم",
        "thank_you_rating": "شكراً جزيلاً لتقييمك!",
        "average_rating": "متوسط التقييم",
        "total_ratings": "إجمالي التقييمات",
        "rating_success": "تم إرسال تقييمك بنجاح!",
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
        "not_found": "Student not found",
        "error": "System error occurred",
        "reset_success": "Your status has been reset",
        "login_success": "Login successful",
        "login_error": "Incorrect password",
        "data_reset_success": "Data reset successfully",
        "backup_success": "Backup created successfully",
        "password_updated": "Password updated successfully",
        "theme_light": "☀️",
        "theme_dark": "🌙",
        "language": "🌐",
        "rating_system": "⭐ Advanced Rating System",
        "rate_app": "Rate Your Experience",
        "your_rating": "Your Rating",
        "your_comment": "Share your feedback (optional)",
        "submit_rating": "Submit Rating",
        "thank_you_rating": "Thank you for your rating!",
        "average_rating": "Average Rating",
        "total_ratings": "Total Ratings",
        "rating_success": "Your rating has been submitted successfully!",
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
    st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
    save_data()
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

# ===== دالة بديلة لعرض بطاقة الطالب باستخدام Streamlit =====
def display_student_card_simple(student):
    """عرض بطاقة طالب باستخدام مكونات Streamlit مباشرة"""
    try:
        # استخراج البيانات
        name = student.get("name", "غير معروف")
        grade = student.get("grade", "غير معروف")
        bus = student.get("bus", "غير معروف")
        parent_phone = student.get("parent_phone", "غير معروف")
        attendance_status = student.get("attendance_status", "لم يسجل")
        status_icon = student.get("status_icon", "⏳")
        last_update = student.get("last_update", "-")
        
        # تحديد اللون بناءً على الحالة
        status_colors = {
            "قادم": "🟢",
            "لن يحضر": "🔴", 
            "لم يسجل": "🟡"
        }
        
        status_color = status_colors.get(attendance_status, "⚪")
        
        # إنشاء البطاقة باستخدام Streamlit
        with st.container():
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1rem 0;
                border: 1px solid rgba(255,255,255,0.2);
                color: white;
            '>
                <div style='text-align: center; margin-bottom: 1rem;'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{status_icon}</div>
                    <h4 style='margin: 0; color: white;'>{name}</h4>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # معلومات الطالب
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📚 الصف", grade)
                st.metric("🚍 الباص", bus)
            with col2:
                st.metric("📞 الهاتف", parent_phone)
                st.metric(f"{status_color} الحالة", attendance_status)
            
            # وقت التحديث
            st.caption(f"⏰ آخر تحديث: {last_update}")
            
            st.markdown("---")
            
    except Exception as e:
        st.error(f"خطأ في عرض بيانات الطالب: {e}")

# ===== دالة بديلة أخرى باستخدام columns =====
def display_student_card_columns(student):
    """عرض بطاقة طالب باستخدام أعمدة Streamlit"""
    try:
        name = student.get("name", "غير معروف")
        grade = student.get("grade", "غير معروف")
        bus = student.get("bus", "غير معروف")
        parent_phone = student.get("parent_phone", "غير معروف")
        attendance_status = student.get("attendance_status", "لم يسجل")
        status_icon = student.get("status_icon", "⏳")
        last_update = student.get("last_update", "-")
        
        # إنشاء البطاقة
        with st.container():
            # الهيدر
            col_icon, col_name = st.columns([1, 4])
            with col_icon:
                st.write(f"### {status_icon}")
            with col_name:
                st.write(f"### {name}")
            
            # المعلومات
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**📚 الصف:** {grade}")
            with col2:
                st.info(f"**🚍 الباص:** {bus}")
            with col3:
                st.info(f"**📞 الهاتف:** {parent_phone}")
            
            # الحالة
            status_colors = {
                "قادم": "✅",
                "لن يحضر": "❌",
                "لم يسجل": "⏳"
            }
            
            status_display = f"{status_colors.get(attendance_status, '⏳')} **الحالة:** {attendance_status}"
            
            if attendance_status == "قادم":
                st.success(status_display)
            elif attendance_status == "لن يحضر":
                st.error(status_display)
            else:
                st.warning(status_display)
            
            # الوقت
            st.caption(f"🕒 **آخر تحديث:** {last_update}")
            
            st.markdown("---")
            
    except Exception as e:
        st.error(f"خطأ في عرض بيانات الطالب: {e}")

# ===== تصميم متطور =====
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
            border-radius: 25px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.1));
            backdrop-filter: blur(15px);
            color: white;
            padding: 2rem 1.5rem;
            border-radius: 20px;
            text-align: center;
            margin: 0.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.4s ease;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .student-card {{
            background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.08));
            backdrop-filter: blur(12px);
            padding: 2rem;
            border-radius: 20px;
            margin: 1.5rem 0;
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: white;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }}
        
        .feature-card {{
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
            backdrop-filter: blur(12px);
            color: white;
            padding: 1.8rem;
            border-radius: 16px;
            margin: 0.8rem 0;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: all 0.3s ease;
        }}
        
        .rating-card {{
            background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.08));
            backdrop-filter: blur(15px);
            color: white;
            padding: 2.5rem;
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            transition: all 0.4s ease;
        }}
        
        .stButton>button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 15px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.4s ease;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            border: 2px solid transparent;
        }}
        
        .stTextInput>div>div>input {{
            border-radius: 15px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            padding: 1rem 1.2rem;
            font-size: 1.1rem;
            background: rgba(255, 255, 255, 0.12);
            color: white;
        }}
        
        .stSelectbox>div>div>select {{
            background: rgba(255, 255, 255, 0.12);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 0.8rem;
        }}
        
        .section-title {{
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            font-size: 2.2rem;
            font-weight: bold;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        
        .info-text {{
            color: rgba(255, 255, 255, 0.85);
            text-align: center;
            margin-bottom: 3rem;
            font-size: 1.2rem;
            line-height: 1.6;
        }}
    </style>
    """, unsafe_allow_html=True)

apply_custom_styles()

# ===== الهيدر الرئيسي =====
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    stats = calculate_attendance_stats()
    st.markdown(f"""
    <div class='stat-card' style='padding: 1.5rem;'>
        <h3 style='margin-bottom: 0.5rem; font-size: 1.8rem;'>📊</h3>
        <h4 style='margin: 0; font-size: 1.1rem;'>الحضور اليوم</h4>
        <h2 style='margin: 0.5rem 0; font-size: 2rem; color: #51cf66;'>{stats['percentage']:.0f}%</h2>
        <p style='margin: 0; opacity: 0.8; font-size: 0.9rem;'>{stats['coming']}/{stats['total']} طالب</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='main-header'>
        <h1 style='font-size: 3rem; margin-bottom: 0.5rem;'>{t('title')}</h1>
        <h3 style='font-size: 1.5rem; margin-bottom: 0.5rem; opacity: 0.9;'>{t('subtitle')}</h3>
        <p style='font-size: 1.2rem; opacity: 0.8; line-height: 1.6;'>{t('description')}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    col3a, col3b = st.columns(2)
    with col3a:
        theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
        if st.button(theme_icon, use_container_width=True, key="theme_btn"):
            toggle_theme()
    with col3b:
        lang_icon = "🌐"
        if st.button(lang_icon, use_container_width=True, key="lang_btn"):
            toggle_language()

# ===== شريط التنقل =====
st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

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
        st.markdown(f"<h2 class='section-title'>{t('student_title')}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='info-text'>{t('student_desc')}</p>", unsafe_allow_html=True)
        
        student_id = st.text_input(
            t("student_id"),
            placeholder=t("student_id_placeholder"),
            key="student_id_input_main"
        )
        
        if student_id:
            try:
                student_info = st.session_state.students_df[
                    st.session_state.students_df["id"].astype(str) == str(student_id).strip()
                ]
                
                if not student_info.empty:
                    student = student_info.iloc[0]
                    
                    # عرض معلومات الطالب
                    st.success(f"🎓 تم العثور على الطالب: **{student['name']}**")
                    
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.info(f"**📚 الصف:** {student['grade']}")
                        st.info(f"**🚍 الباص:** {student['bus']}")
                    with col_info2:
                        st.info(f"**📞 هاتف ولي الأمر:** {student['parent_phone']}")
                    
                    already_registered, current_status = has_student_registered_today(student_id)
                    
                    if already_registered:
                        st.warning(f"**✅ تم التسجيل مسبقاً**\n\n**الحالة الحالية:** {current_status}")
                        
                        if st.button("🔄 تغيير الحالة", key="change_status_btn"):
                            today = datetime.datetime.now().strftime("%Y-%m-%d")
                            st.session_state.attendance_df = st.session_state.attendance_df[
                                ~((st.session_state.attendance_df["id"].astype(str) == str(student_id).strip()) & 
                                  (st.session_state.attendance_df["date"] == today))
                            ]
                            save_data()
                            st.success(t("reset_success"))
                            st.rerun()
                    
                    else:
                        st.info("**اختر حالتك اليوم:**")
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button("✅ سأحضر اليوم", use_container_width=True, key="coming_btn"):
                                now = register_attendance(student, "قادم")
                                st.balloons()
                                st.success(f"""
                                **🎉 تم التسجيل بنجاح!**
                                
                                **الطالب:** {student['name']}
                                **الحالة:** قادم
                                **الوقت:** {now.strftime('%H:%M')}
                                **الباص:** {student['bus']}
                                """)
                        with col_btn2:
                            if st.button("❌ لن أحضر اليوم", use_container_width=True, key="not_coming_btn"):
                                now = register_attendance(student, "لن يأتي")
                                st.success(f"""
                                **🎉 تم التسجيل بنجاح!**
                                
                                **الطالب:** {student['name']}
                                **الحالة:** لن أحضر  
                                **الوقت:** {now.strftime('%H:%M')}
                                **الباص:** {student['bus']}
                                """)
                
                else:
                    st.error(f"❌ {t('not_found')}")
                    
            except Exception as e:
                st.error(f"❌ {t('error')}")

    with col2:
        st.markdown(f"<h3 style='text-align: center; color: white;'>{t('stats_title')}</h3>", unsafe_allow_html=True)
        
        stats = calculate_attendance_stats()
        
        st.metric(t("total_registered"), stats['total'])
        st.metric(t("expected_attendance"), stats['coming'])
        st.metric(t("attendance_rate"), f"{stats['percentage']:.1f}%")

# ===== صفحة الإدارة =====
elif st.session_state.page == "admin":
    st.subheader(t("admin_title"))
    
    if not st.session_state.admin_logged_in:
        st.markdown(f"<h3 style='text-align: center; color: white; margin-bottom: 2rem;'>{t('admin_login')}</h3>", unsafe_allow_html=True)
        
        admin_password = st.text_input(t("admin_password"), type="password", placeholder=t("password_placeholder"), key="admin_login_password")
        
        if st.button(t("login"), type="primary", use_container_width=True, key="admin_login_btn"):
            if admin_password == st.session_state.admin_password:
                st.session_state.admin_logged_in = True
                st.success(t("login_success"))
                st.rerun()
            else:
                st.error(t("login_error"))
    
    else:
        st.success(f"✅ {t('login_success')}")
        
        if st.button(t("logout"), type="secondary", key="admin_logout_btn"):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        # تبويب عرض جميع الطلاب
        tab1, tab2, tab3, tab4 = st.tabs([
            "👥 جميع الطلاب", 
            t("system_stats"), 
            t("change_bus_password"), 
            t("change_admin_password")
        ])
        
        with tab1:
            st.header("👥 لوحة متابعة جميع الطلاب")
            
            # إحصائيات سريعة
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_students = len(st.session_state.students_df)
                st.metric("إجمالي الطلاب", total_students)
            with col2:
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                today_attendance = st.session_state.attendance_df[
                    st.session_state.attendance_df["date"] == today
                ] if not st.session_state.attendance_df.empty else pd.DataFrame()
                registered_today = len(today_attendance)
                st.metric("المسجلين اليوم", registered_today)
            with col3:
                coming_today = len(today_attendance[today_attendance["status"] == "قادم"]) if not today_attendance.empty else 0
                st.metric("الحضور المتوقع", coming_today)
            with col4:
                attendance_rate = (coming_today / total_students * 100) if total_students > 0 else 0
                st.metric("نسبة الحضور", f"{attendance_rate:.1f}%")
            
            # فلترة البيانات
            st.subheader("🔍 تصفية البيانات")
            col1, col2, col3 = st.columns(3)
            with col1:
                bus_filter = st.selectbox("تصفية حسب الباص", ["الكل", "1", "2", "3"], key="bus_filter_admin")
            with col2:
                grade_filter = st.selectbox("تصفية حسب الصف", ["الكل", "6", "7", "8", "9", "10", "11"], key="grade_filter_admin")
            with col3:
                status_filter = st.selectbox("تصفية حسب الحالة", ["الكل", "قادم", "لن يحضر", "لم يسجل"], key="status_filter_admin")
            
            # تطبيق الفلتر
            filtered_students = st.session_state.students_df.copy()
            
            if bus_filter != "الكل":
                filtered_students = filtered_students[filtered_students["bus"] == bus_filter]
            
            if grade_filter != "الكل":
                filtered_students = filtered_students[filtered_students["grade"].str.contains(grade_filter)]
            
            # دمج بيانات الحضور
            students_with_attendance = []
            for _, student in filtered_students.iterrows():
                today_status = today_attendance[
                    today_attendance["id"].astype(str) == str(student["id"])
                ] if not today_attendance.empty else pd.DataFrame()
                
                if not today_status.empty:
                    status = today_status.iloc[0]["status"]
                    status_icon = "✅" if status == "قادم" else "❌"
                    last_update = today_status.iloc[0]["time"]
                else:
                    status = "لم يسجل"
                    status_icon = "⏳"
                    last_update = "-"
                
                student_data = {
                    "id": student["id"],
                    "name": student["name"],
                    "grade": student["grade"],
                    "bus": student["bus"],
                    "parent_phone": student["parent_phone"],
                    "attendance_status": status,
                    "status_icon": status_icon,
                    "last_update": last_update
                }
                
                students_with_attendance.append(student_data)
            
            # تطبيق فلتر الحالة
            if status_filter != "الكل":
                students_with_attendance = [s for s in students_with_attendance if s["attendance_status"] == status_filter]
            
            # عرض البيانات - استخدام الطريقة البسيطة
            st.subheader(f"📋 قائمة الطلاب ({len(students_with_attendance)} طالب)")
            
            if students_with_attendance:
                # استخدام الطريقة البسيطة لعرض البطاقات
                for student in students_with_attendance:
                    display_student_card_columns(student)
            else:
                st.info("🚫 لا توجد بيانات تطابق معايير التصفية")
            
            # تصدير البيانات
            st.subheader("📤 تصدير البيانات")
            col1, col2 = st.columns(2)
            with col2:
                csv_data = pd.DataFrame(students_with_attendance)
                st.download_button(
                    "📊 تصدير كملف Excel",
                    data=csv_data.to_csv(index=False, encoding='utf-8-sig'),
                    file_name=f"students_report_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="export_csv_btn"
                )

# ===== الفوتر =====
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem; color: white;'>
    <h4>🚍 {t('footer')}</h4>
    <p>{t('rights')}</p>
    <p style='font-size: 0.9rem;'>{t('team')}</p>
</div>
""", unsafe_allow_html=True)
