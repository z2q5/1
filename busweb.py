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
        "poor": "ضعيف",
        # الترجمات الجديدة
        "add_student": "➕ إضافة طالب جديد",
        "new_student_info": "معلومات الطالب الجديد",
        "student_name": "اسم الطالب",
        "student_name_placeholder": "أدخل اسم الطالب الكامل...",
        "student_id": "رقم الوزارة",
        "student_id_placeholder": "أدخل رقم الوزارة...",
        "select_grade": "اختر الصف",
        "select_bus": "اختر الباص",
        "parent_phone_placeholder": "أدخل رقم هاتف ولي الأمر...",
        "add_student_button": "➕ إضافة الطالب",
        "student_added_success": "✅ تم إضافة الطالب بنجاح!",
        "student_exists_error": "❌ رقم الوزارة موجود مسبقاً!",
        "delete_student": "🗑️ حذف الطالب",
        "delete_student_confirm": "هل أنت متأكد من حذف هذا الطالب؟",
        "student_deleted_success": "✅ تم حذف الطالب بنجاح!",
        "edit_student": "✏️ تعديل بيانات الطالب",
        "student_updated_success": "✅ تم تحديث بيانات الطالب بنجاح!",
        # ترجمات الصفحات الجديدة
        "track_student": "🔍 متابعة الطالب",
        "enter_student_id": "أدخل رقم وزارة الطالب",
        "today_status": "حالة اليوم",
        "registration_time": "وقت التسجيل",
        "bus_schedule": "⏰ جدول الباص",
        "morning_pickup": "وقت الصباح",
        "evening_return": "وقت العودة",
        "driver_contact": "📞 اتصال السائق",
        "contact_info": "معلومات الاتصال",
        "bus_location": "📍 موقع الباص",
        "current_location": "الموقع الحالي",
        "features_title": "المميزات الرئيسية",
        "feature1": "تسجيل حضور ذكي",
        "feature1_desc": "نظام تسجيل حضور آلي وسهل للطلاب",
        "feature2": "متابعة مباشرة", 
        "feature2_desc": "متابعة حية لتحركات الباصات والحضور",
        "feature3": "تقييم الخدمة",
        "feature3_desc": "نظام تقييم متطور لجودة الخدمة",
        "feature4": "إشعارات فورية",
        "feature4_desc": "إشعارات فورية لأولياء الأمور",
        "technical_specs": "المواصفات الفنية",
        "tech1": "واجهة مستخدم متعددة اللغات",
        "tech2": "تصميم متجاوب مع جميع الأجهزة",
        "tech3": "نظام حماية متكامل",
        "tech4": "نسخ احتياطي تلقائي"
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
        "poor": "Poor",
        # New translations
        "add_student": "➕ Add New Student",
        "new_student_info": "New Student Information",
        "student_name": "Student Name",
        "student_name_placeholder": "Enter full student name...",
        "student_id": "Ministry Number",
        "student_id_placeholder": "Enter ministry number...",
        "select_grade": "Select Grade",
        "select_bus": "Select Bus",
        "parent_phone_placeholder": "Enter parent phone number...",
        "add_student_button": "➕ Add Student",
        "student_added_success": "✅ Student added successfully!",
        "student_exists_error": "❌ Ministry number already exists!",
        "delete_student": "🗑️ Delete Student",
        "delete_student_confirm": "Are you sure you want to delete this student?",
        "student_deleted_success": "✅ Student deleted successfully!",
        "edit_student": "✏️ Edit Student Data",
        "student_updated_success": "✅ Student data updated successfully!",
        # New page translations
        "track_student": "🔍 Track Student",
        "enter_student_id": "Enter student ministry number",
        "today_status": "Today's Status",
        "registration_time": "Registration Time",
        "bus_schedule": "⏰ Bus Schedule",
        "morning_pickup": "Morning Pickup",
        "evening_return": "Evening Return",
        "driver_contact": "📞 Driver Contact",
        "contact_info": "Contact Information",
        "bus_location": "📍 Bus Location",
        "current_location": "Current Location",
        "features_title": "Main Features",
        "feature1": "Smart Attendance",
        "feature1_desc": "Automatic and easy student attendance system",
        "feature2": "Live Tracking", 
        "feature2_desc": "Real-time tracking of buses and attendance",
        "feature3": "Service Rating",
        "feature3_desc": "Advanced service quality rating system",
        "feature4": "Instant Notifications",
        "feature4_desc": "Instant notifications for parents",
        "technical_specs": "Technical Specifications",
        "tech1": "Multi-language user interface",
        "tech2": "Responsive design for all devices",
        "tech3": "Integrated security system",
        "tech4": "Automatic backup system"
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

# ===== وظائف إدارة الطلاب الجديدة =====
def add_new_student(student_id, name, grade, bus, parent_phone):
    """إضافة طالب جديد إلى النظام"""
    try:
        # التحقق من عدم وجود رقم وزارة مكرر
        if str(student_id).strip() in st.session_state.students_df["id"].astype(str).values:
            return False, "student_exists"
        
        # إنشاء بيانات الطالب الجديد
        new_student = {
            "id": str(student_id).strip(),
            "name": name.strip(),
            "grade": grade,
            "bus": bus,
            "parent_phone": parent_phone.strip()
        }
        
        # إضافة الطالب إلى DataFrame
        new_student_df = pd.DataFrame([new_student])
        st.session_state.students_df = pd.concat([
            st.session_state.students_df, new_student_df
        ], ignore_index=True)
        
        # حفظ البيانات
        save_data()
        return True, "success"
        
    except Exception as e:
        return False, str(e)

def delete_student(student_id):
    """حذف طالب من النظام"""
    try:
        # حذف الطالب من بيانات الطلاب
        st.session_state.students_df = st.session_state.students_df[
            st.session_state.students_df["id"].astype(str) != str(student_id).strip()
        ]
        
        # حذف سجلات الحضور الخاصة بالطالب
        st.session_state.attendance_df = st.session_state.attendance_df[
            st.session_state.attendance_df["id"].astype(str) != str(student_id).strip()
        ]
        
        # حفظ البيانات
        save_data()
        return True, "success"
        
    except Exception as e:
        return False, str(e)

def update_student(student_id, name, grade, bus, parent_phone):
    """تحديث بيانات طالب موجود"""
    try:
        # البحث عن الطالب وتحديث بياناته
        mask = st.session_state.students_df["id"].astype(str) == str(student_id).strip()
        if mask.any():
            st.session_state.students_df.loc[mask, "name"] = name.strip()
            st.session_state.students_df.loc[mask, "grade"] = grade
            st.session_state.students_df.loc[mask, "bus"] = bus
            st.session_state.students_df.loc[mask, "parent_phone"] = parent_phone.strip()
            
            # تحديث اسم الطالب في سجلات الحضور أيضاً
            attendance_mask = st.session_state.attendance_df["id"].astype(str) == str(student_id).strip()
            if attendance_mask.any():
                st.session_state.attendance_df.loc[attendance_mask, "name"] = name.strip()
            
            save_data()
            return True, "success"
        else:
            return False, "student_not_found"
            
    except Exception as e:
        return False, str(e)

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

# ===== وظائف جديدة للصفحات الأخرى =====
def get_bus_students(bus_number):
    """الحصول على قائمة طلاب الباص"""
    return st.session_state.students_df[
        st.session_state.students_df["bus"] == bus_number
    ]

def get_today_attendance_for_bus(bus_number):
    """الحصول على حضور اليوم لطلاب الباص"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if st.session_state.attendance_df.empty:
        return pd.DataFrame()
    
    bus_students = get_bus_students(bus_number)
    bus_student_ids = bus_students["id"].astype(str).tolist()
    
    today_attendance = st.session_state.attendance_df[
        (st.session_state.attendance_df["date"] == today) & 
        (st.session_state.attendance_df["id"].astype(str).isin(bus_student_ids))
    ]
    
    return today_attendance

def get_bus_schedule(bus_number):
    """جدول الباص"""
    schedules = {
        "1": {"morning": "07:00 AM", "evening": "02:30 PM"},
        "2": {"morning": "07:15 AM", "evening": "02:45 PM"}, 
        "3": {"morning": "07:30 AM", "evening": "03:00 PM"}
    }
    return schedules.get(bus_number, {"morning": "07:00 AM", "evening": "02:30 PM"})

def get_driver_contact(bus_number):
    """معلومات السائق"""
    drivers = {
        "1": {"name": "محمد أحمد", "phone": "0501111111"},
        "2": {"name": "علي حسن", "phone": "0502222222"},
        "3": {"name": "خالد سعيد", "phone": "0503333333"}
    }
    return drivers.get(bus_number, {"name": "غير محدد", "phone": "غير محدد"})

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

# ===== صفحة السائق =====
elif st.session_state.page == "driver":
    st.markdown(f"<h2 class='section-title'>{t('driver_title')}</h2>", unsafe_allow_html=True)
    
    if not st.session_state.driver_logged_in:
        st.markdown(f"<h3 style='text-align: center; color: white; margin-bottom: 2rem;'>{t('driver_login')}</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            bus_number = st.selectbox(t("select_bus"), ["1", "2", "3"], key="driver_bus_select")
        with col2:
            password = st.text_input(t("password"), type="password", placeholder=t("password_placeholder"), key="driver_password")
        
        if st.button(t("login"), type="primary", use_container_width=True, key="driver_login_btn"):
            if password == st.session_state.bus_passwords.get(bus_number, ""):
                st.session_state.driver_logged_in = True
                st.session_state.current_bus = bus_number
                st.success(t("login_success"))
                st.rerun()
            else:
                st.error(t("login_error"))
    
    else:
        st.success(f"✅ تم تسجيل الدخول كسائق للباص {st.session_state.current_bus}")
        
        if st.button(t("logout"), type="secondary", key="driver_logout_btn"):
            st.session_state.driver_logged_in = False
            st.rerun()
        
        # إحصائيات الباص
        bus_students = get_bus_students(st.session_state.current_bus)
        today_attendance = get_today_attendance_for_bus(st.session_state.current_bus)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(t("total_students"), len(bus_students))
        with col2:
            coming_today = len(today_attendance[today_attendance["status"] == "قادم"]) if not today_attendance.empty else 0
            st.metric(t("confirmed_attendance"), coming_today)
        with col3:
            not_coming = len(today_attendance[today_attendance["status"] == "لن يحضر"]) if not today_attendance.empty else 0
            st.metric("الغياب", not_coming)
        with col4:
            percentage = (coming_today / len(bus_students) * 100) if len(bus_students) > 0 else 0
            st.metric(t("attendance_percentage"), f"{percentage:.1f}%")
        
        # قائمة الطلاب القادمين اليوم
        st.subheader(f"🎒 {t('coming_students')}")
        
        if not today_attendance.empty:
            coming_students = today_attendance[today_attendance["status"] == "قادم"]
            
            if not coming_students.empty:
                for _, student in coming_students.iterrows():
                    with st.container():
                        col1, col2, col3 = st.columns([3, 2, 1])
                        with col1:
                            st.write(f"**{student['name']}**")
                        with col2:
                            st.write(f"📚 {student['grade']}")
                        with col3:
                            st.success("✅ قادم")
                        st.caption(f"⏰ وقت التسجيل: {student['time']}")
                        st.markdown("---")
            else:
                st.info(t("no_students"))
        else:
            st.info(t("no_students"))
        
        # جميع طلاب الباص
        st.subheader(f"👥 {t('all_students')}")
        
        for _, student in bus_students.iterrows():
            # التحقق من حالة الطالب اليوم
            today_status = today_attendance[
                today_attendance["id"].astype(str) == str(student["id"])
            ] if not today_attendance.empty else pd.DataFrame()
            
            status = "قادم" if not today_status.empty and today_status.iloc[0]["status"] == "قادم" else "لن يحضر" if not today_status.empty else "لم يسجل"
            status_icon = "✅" if status == "قادم" else "❌" if status == "لن يحضر" else "⏳"
            
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    st.write(f"**{student['name']}**")
                with col2:
                    st.write(f"📚 {student['grade']}")
                with col3:
                    st.write(f"📞 {student['parent_phone']}")
                with col4:
                    if status == "قادم":
                        st.success(f"{status_icon} {status}")
                    elif status == "لن يحضر":
                        st.error(f"{status_icon} {status}")
                    else:
                        st.warning(f"{status_icon} {status}")
                st.markdown("---")

# ===== صفحة أولياء الأمور =====
elif st.session_state.page == "parents":
    st.markdown(f"<h2 class='section-title'>{t('parents_title')}</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(t("track_student"))
        student_id = st.text_input(t("enter_student_id"), placeholder=t("parents_id_placeholder"), key="parent_student_id")
        
        if student_id:
            try:
                student_info = st.session_state.students_df[
                    st.session_state.students_df["id"].astype(str) == str(student_id).strip()
                ]
                
                if not student_info.empty:
                    student = student_info.iloc[0]
                    
                    st.success(f"🎓 تم العثور على الطالب: **{student['name']}**")
                    
                    # معلومات الطالب
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.info(f"**📚 الصف:** {student['grade']}")
                        st.info(f"**🚍 الباص:** {student['bus']}")
                    with col_info2:
                        st.info(f"**📞 هاتف ولي الأمر:** {student['parent_phone']}")
                    
                    # حالة اليوم
                    st.subheader(t("today_status"))
                    already_registered, current_status = has_student_registered_today(student_id)
                    
                    if already_registered:
                        # الحصول على وقت التسجيل
                        today = datetime.datetime.now().strftime("%Y-%m-%d")
                        registration_data = st.session_state.attendance_df[
                            (st.session_state.attendance_df["id"].astype(str) == str(student_id).strip()) & 
                            (st.session_state.attendance_df["date"] == today)
                        ]
                        
                        if not registration_data.empty:
                            registration_time = registration_data.iloc[0]["time"]
                            
                            if current_status == "قادم":
                                st.success(f"""
                                **✅ حالة اليوم:** قادم إلى المدرسة
                                **⏰ وقت التسجيل:** {registration_time}
                                """)
                            else:
                                st.error(f"""
                                **❌ حالة اليوم:** لن يحضر اليوم
                                **⏰ وقت التسجيل:** {registration_time}
                                """)
                    else:
                        st.warning("**⏳ حالة اليوم:** لم يتم تسجيل الحضور بعد")
                
                else:
                    st.error(f"❌ {t('not_found')}")
                    
            except Exception as e:
                st.error(f"❌ {t('error')}")
    
    with col2:
        st.subheader(t("bus_info"))
        
        if student_id and not st.session_state.students_df[
            st.session_state.students_df["id"].astype(str) == str(student_id).strip()
        ].empty:
            student = st.session_state.students_df[
                st.session_state.students_df["id"].astype(str) == str(student_id).strip()
            ].iloc[0]
            
            bus_number = student["bus"]
            schedule = get_bus_schedule(bus_number)
            driver = get_driver_contact(bus_number)
            
            # جدول الباص
            st.subheader(t("bus_schedule"))
            col_time1, col_time2 = st.columns(2)
            with col_time1:
                st.metric(t("morning_pickup"), schedule["morning"])
            with col_time2:
                st.metric(t("evening_return"), schedule["evening"])
            
            # معلومات السائق
            st.subheader(t("driver_contact"))
            st.info(f"""
            **👤 اسم السائق:** {driver['name']}
            **📞 رقم الهاتف:** {driver['phone']}
            """)
            
            # موقع الباص (محاكاة)
            st.subheader(t("bus_location"))
            locations = {
                "1": "شارع الخليج - أمام مركز الميرة",
                "2": "شارع الشيخ زايد - قرب مجمع أبوظبي",
                "3": "شارع المصفح - منطقة السادات"
            }
            current_loc = locations.get(bus_number, "في الطريق إلى المدرسة")
            st.success(f"**📍 {t('current_location')}:** {current_loc}")

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
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "👥 جميع الطلاب", 
            t("add_student"),
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
        
        with tab2:
            st.header("➕ إدارة الطلاب")
            
            # قسم إضافة طالب جديد
            st.subheader(t("add_student"))
            
            with st.form("add_student_form"):
                st.markdown(f"<h4 style='color: white;'>{t('new_student_info')}</h4>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    new_student_id = st.text_input(t("student_id"), placeholder=t("student_id_placeholder"), key="new_student_id")
                    new_student_name = st.text_input(t("student_name"), placeholder=t("student_name_placeholder"), key="new_student_name")
                with col2:
                    new_student_grade = st.selectbox(t("select_grade"), ["6-A", "6-B", "7-A", "7-B", "8-A", "8-B", "8-C", "9-A", "9-B", "10-A", "10-B", "11-A", "11-B"], key="new_student_grade")
                    new_student_bus = st.selectbox(t("select_bus"), ["1", "2", "3"], key="new_student_bus")
                
                new_parent_phone = st.text_input(t("parent_phone"), placeholder=t("parent_phone_placeholder"), key="new_parent_phone")
                
                submit_button = st.form_submit_button(t("add_student_button"), use_container_width=True)
                
                if submit_button:
                    if not all([new_student_id, new_student_name, new_parent_phone]):
                        st.error("❌ يرجى ملء جميع الحقول المطلوبة")
                    else:
                        success, message = add_new_student(
                            new_student_id, 
                            new_student_name, 
                            new_student_grade, 
                            new_student_bus, 
                            new_parent_phone
                        )
                        
                        if success:
                            st.success(f"✅ {t('student_added_success')}")
                            st.balloons()
                        elif message == "student_exists":
                            st.error(f"❌ {t('student_exists_error')}")
                        else:
                            st.error(f"❌ حدث خطأ: {message}")
            
            st.markdown("---")
            
            # قسم حذف الطلاب
            st.subheader("🗑️ إدارة الطلاب الحاليين")
            
            if not st.session_state.students_df.empty:
                # إنشاء قائمة بالطلاب للحذف
                student_options = {f"{row['id']} - {row['name']}": row['id'] for _, row in st.session_state.students_df.iterrows()}
                selected_student_display = st.selectbox("اختر الطالب للحذف", list(student_options.keys()), key="delete_student_select")
                
                if selected_student_display:
                    selected_student_id = student_options[selected_student_display]
                    
                    # عرض معلومات الطالب المحدد
                    student_info = st.session_state.students_df[
                        st.session_state.students_df["id"].astype(str) == str(selected_student_id)
                    ].iloc[0]
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.info(f"**الاسم:** {student_info['name']}")
                    with col2:
                        st.info(f"**الصف:** {student_info['grade']}")
                    with col3:
                        st.info(f"**الباص:** {student_info['bus']}")
                    
                    # زر الحذف مع تأكيد
                    if st.button("🗑️ حذف الطالب", type="secondary", key="delete_student_btn"):
                        if st.checkbox("✅ تأكيد الحذف", key="confirm_delete"):
                            success, message = delete_student(selected_student_id)
                            if success:
                                st.success(f"✅ {t('student_deleted_success')}")
                                st.rerun()
                            else:
                                st.error(f"❌ حدث خطأ: {message}")
            else:
                st.info("🚫 لا توجد طلاب في النظام")

        with tab3:
            st.header("📊 إحصائيات النظام")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_students = len(st.session_state.students_df)
                st.metric("إجمالي الطلاب", total_students)
            with col2:
                total_attendance_records = len(st.session_state.attendance_df)
                st.metric("سجلات الحضور", total_attendance_records)
            with col3:
                total_ratings = len(st.session_state.ratings_df)
                st.metric("التقييمات", total_ratings)
            with col4:
                avg_rating, _ = get_average_rating()
                st.metric("متوسط التقييم", f"{avg_rating:.1f}/5")
            
            # إحصائيات الباصات
            st.subheader("🚍 إحصائيات الباصات")
            bus_stats = []
            for bus in ["1", "2", "3"]:
                bus_students = get_bus_students(bus)
                today_attendance = get_today_attendance_for_bus(bus)
                coming_today = len(today_attendance[today_attendance["status"] == "قادم"]) if not today_attendance.empty else 0
                
                bus_stats.append({
                    "bus": bus,
                    "total_students": len(bus_students),
                    "coming_today": coming_today,
                    "percentage": (coming_today / len(bus_students) * 100) if len(bus_students) > 0 else 0
                })
            
            for stat in bus_stats:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(f"الباص {stat['bus']} - إجمالي الطلاب", stat['total_students'])
                with col2:
                    st.metric(f"الباص {stat['bus']} - الحضور اليوم", stat['coming_today'])
                with col3:
                    st.metric(f"الباص {stat['bus']} - النسبة", f"{stat['percentage']:.1f}%")
                with col4:
                    driver = get_driver_contact(stat['bus'])
                    st.info(f"السائق: {driver['name']}")

        with tab4:
            st.header("🔐 تغيير كلمات مرور الباصات")
            
            for bus in ["1", "2", "3"]:
                with st.expander(f"الباص {bus}"):
                    current_password = st.session_state.bus_passwords.get(bus, "")
                    st.info(f"كلمة المرور الحالية: **{current_password}**")
                    
                    new_password = st.text_input(f"كلمة المرور الجديدة للباص {bus}", type="password", key=f"new_bus_password_{bus}")
                    
                    if st.button(f"حفظ للباص {bus}", key=f"save_bus_{bus}"):
                        if new_password:
                            st.session_state.bus_passwords[bus] = new_password
                            save_data()
                            st.success(f"✅ تم تحديث كلمة مرور الباص {bus}")
                        else:
                            st.error("❌ يرجى إدخال كلمة مرور جديدة")

        with tab5:
            st.header("🔐 تغيير كلمة مرور الإدارة")
            
            current_password = st.session_state.admin_password
            st.info(f"كلمة المرور الحالية: **{current_password}**")
            
            new_admin_password = st.text_input("كلمة المرور الجديدة للإدارة", type="password", key="new_admin_password")
            confirm_password = st.text_input("تأكيد كلمة المرور الجديدة", type="password", key="confirm_admin_password")
            
            if st.button("حفظ كلمة مرور الإدارة", type="primary"):
                if new_admin_password and confirm_password:
                    if new_admin_password == confirm_password:
                        st.session_state.admin_password = new_admin_password
                        save_data()
                        st.success("✅ تم تحديث كلمة مرور الإدارة بنجاح")
                    else:
                        st.error("❌ كلمات المرور غير متطابقة")
                else:
                    st.error("❌ يرجى ملء جميع الحقول")

# ===== صفحة حول النظام =====
elif st.session_state.page == "about":
    st.markdown(f"<h2 class='section-title'>{t('about_title')}</h2>", unsafe_allow_html=True)
    
    st.markdown(f"<p class='info-text'>{t('about_description')}</p>", unsafe_allow_html=True)
    
    # المميزات الرئيسية
    st.subheader("🎯 المميزات الرئيسية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>🚍 نظام متكامل</h3>
            <p>نظام متكامل لإدارة النقل المدرسي يشمل جميع الجوانب التشغيلية</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h3>📱 واجهة سهلة</h3>
            <p>واجهة مستخدم بديهية وسهلة الاستخدام لجميع الفئات</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h3>🔒 أمان عالي</h3>
            <p>نظام حماية متكامل لحماية بيانات الطلاب والمستخدمين</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>📊 تقارير متقدمة</h3>
            <p>نظام تقارير وإحصائيات متطور لمتابعة الأداء</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h3>🌐 متعدد اللغات</h3>
            <p>دعم كامل للغتين العربية والإنجليزية</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h3>📈 قابلة للتطوير</h3>
            <p>تصميم مرن يمكن تطويره وإضافة مميزات جديدة</p>
        </div>
        """, unsafe_allow_html=True)
    
    # معلومات الفريق
    st.subheader("👥 فريق التطوير")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>🛠️ مطور النظام</h3>
            <p><strong>إياد مصطفى</strong></p>
            <p>مسؤول عن التطوير البرمجي والوظائف التقنية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>🎨 مصمم الواجهة</h3>
            <p><strong>ايمن جلال</strong></p>
            <p>مسؤول عن التصميم وتجربة المستخدم</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h3>👨‍🏫 الإشراف</h3>
            <p><strong>قسم النادي البيئي</strong></p>
            <p>الإشراف العام ومتابعة الجودة</p>
        </div>
        """, unsafe_allow_html=True)
    
    # معلومات الإصدار
    st.subheader("📋 معلومات الإصدار")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **الإصدار:** 1.1\n
        **الحالة:** ⭐ الإصدار المستقر
        """)
    
    with col2:
        st.info("""
        **تاريخ الإصدار:** 2025\n
        **آخر تحديث:** يناير 2025
        """)
    
    with col3:
        st.info("""
        **الترخيص:** خاص\n
        **المدرسة:** المنيرة الخاصة
        """)
    
    # نظام التقييم
    st.subheader("⭐ نظام التقييم")
    
    avg_rating, total_ratings = get_average_rating()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("متوسط التقييم", f"{avg_rating:.1f}/5")
    
    with col2:
        st.metric("إجمالي التقييمات", total_ratings)
    
    # نموذج التقييم
    with st.form("rating_form"):
        st.subheader("شاركنا رأيك")
        
        rating = st.slider("تقييمك للنظام", 1, 5, 5, key="about_rating")
        comment = st.text_area("تعليقك (اختياري)", placeholder="اكتب تعليقك هنا...", key="about_comment")
        
        if st.form_submit_button("إرسال التقييم", use_container_width=True):
            add_rating(rating, comment)
            st.success("شكراً لك على تقييمك! 🌟")

# ===== الفوتر =====
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem; color: white;'>
    <h4>🚍 {t('footer')}</h4>
    <p>{t('rights')}</p>
    <p style='font-size: 0.9rem;'>{t('team')}</p>
</div>
""", unsafe_allow_html=True)
