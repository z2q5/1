import streamlit as st
import pandas as pd
import datetime
import os
import random
import json
import pickle
from pathlib import Path
import requests

# ===== إعداد الصفحة =====
st.set_page_config(
    page_title="Smart Bus System - Al Muneera Private School", 
    layout="wide",
    page_icon="🚍",
    initial_sidebar_state="collapsed"
)

# ===== مسار حفظ البيانات =====
DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)

# ===== حالة التطبيق المحسنة =====
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
if "offline_mode" not in st.session_state:
    st.session_state.offline_mode = False
if "first_time" not in st.session_state:
    st.session_state.first_time = True
if "last_save" not in st.session_state:
    st.session_state.last_save = datetime.datetime.now()
if "font_size" not in st.session_state:
    st.session_state.font_size = "افتراضي"
if "high_contrast" not in st.session_state:
    st.session_state.high_contrast = False

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
            "lang": st.session_state.lang,
            "font_size": st.session_state.font_size,
            "high_contrast": st.session_state.high_contrast
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
                st.session_state.font_size = settings.get("font_size", "افتراضي")
                st.session_state.high_contrast = settings.get("high_contrast", False)
                
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")

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

# ===== الترجمة الكاملة =====
translations = {
    "ar": {
        # التنقل الرئيسي
        "title": "🚍 نظام الباص الذكي",
        "subtitle": "مدرسة المنيرة الخاصة - أبوظبي",
        "description": "نظام متكامل لإدارة النقل المدرسي الذكي",
        "student": "🎓 الطالب",
        "driver": "🚌 السائق", 
        "parents": "👨‍👩‍👧 أولياء الأمور",
        "admin": "🏫 الإدارة",
        "about": "ℹ️ حول النظام",
        
        # صفحة الطالب
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
        
        # صفحة السائق
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
        
        # صفحة أولياء الأمور
        "parents_title": "👨‍👩‍👧 بوابة أولياء الأمور",
        "parents_id_placeholder": "مثال: 1001",
        "attendance_tracking": "📊 متابعة الحضور",
        "bus_info": "🚌 معلومات الباص",
        "morning_time": "وقت الصباح التقريبي",
        "afternoon_time": "وقت الظهيرة التقريبي",
        "track_student": "🔍 متابعة الطالب",
        "enter_student_id": "أدخل رقم وزارة الطالب",
        "today_status": "حالة اليوم",
        "registration_time": "وقت التسجيل",
        "bus_schedule": "⏰ جدول الباص",
        "morning_pickup": "وقت الذهاب",
        "evening_return": "وقت العودة",
        "driver_contact": "📞 اتصال السائق",
        "contact_info": "معلومات الاتصال",
        "bus_location": "📍 موقع الباص",
        "current_location": "الموقع الحالي",
        
        # صفحة الإدارة
        "admin_title": "🏫 لوحة تحكم الإدارة",
        "admin_login": "🔐 تسجيل دخول الإدارة",
        "admin_password": "كلمة مرور الإدارة",
        "system_stats": "📊 إحصائيات النظام",
        "students_count": "عدد الطلاب",
        "attendance_records": "سجلات الحضور",
        "system_actions": "⚙️ إجراءات النظام",
        "reset_data": "🔄 إعادة تعيين البيانات",
        "backup": "📥 نسخة احتياطية",
        "change_admin_password": "تغيير كلمة مرور الإدارة",
        "current_passwords": "كلمات المرور الحالية",
        "change_bus_password": "تغيير كلمات مرور الباصات",
        "select_bus_password": "اختر الباص",
        "new_password": "كلمة المرور الجديدة",
        "save_changes": "💾 حفظ التغييرات",
        
        # إدارة الطلاب
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
        "manage_students": "👥 إدارة الطلاب",
        "export_data": "📤 تصدير البيانات",
        "filter_data": "🔍 تصفية البيانات",
        "filter_by_bus": "تصفية حسب الباص",
        "filter_by_grade": "تصفية حسب الصف",
        "filter_by_status": "تصفية حسب الحالة",
        "all": "الكل",
        
        # صفحة حول النظام
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
        
        # رسائل النظام
        "not_found": "لم يتم العثور على الطالب",
        "error": "حدث خطأ في النظام",
        "reset_success": "تم إعادة تعيين حالتك",
        "login_success": "تم الدخول بنجاح",
        "login_error": "كلمة مرور غير صحيحة",
        "data_reset_success": "تم إعادة تعيين البيانات",
        "backup_success": "تم إنشاء نسخة احتياطية",
        "password_updated": "تم تحديث كلمة المرور",
        
        # الإعدادات
        "theme_light": "☀️",
        "theme_dark": "🌙",
        "language": "🌐",
        
        # نظام التقييم
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
        
        # الفوتر
        "footer": "🚍 نظام الباص الذكي - الإصدار 2.0",
        "rights": "© 2025 جميع الحقوق محفوظة",
        "team": "تم التطوير بواسطة: إياد مصطفى | التصميم: ايمن جلال | الإشراف: قسم النادي البيئي",
        
        # مميزات النظام
        "feature1": "تسجيل حضور ذكي",
        "feature1_desc": "نظام تسجيل حضور آلي وسهل للطلاب",
        "feature2": "متابعة مباشرة", 
        "feature2_desc": "متابعة حية لتحركات الباصات والحضور",
        "feature3": "تقييم الخدمة",
        "feature3_desc": "نظام تقييم متطور لجودة الخدمة",
        "feature4": "إشعارات فورية",
        "feature4_desc": "إشعارات فورية لأولياء الأمور",
        "feature5": "واجهة متطورة",
        "feature5_desc": "تصميم حديث وسهل الاستخدام",
        "feature6": "أمان وحماية",
        "feature6_desc": "نظام حماية متكامل للبيانات",
        
        # مواصفات فنية
        "technical_specs": "المواصفات الفنية",
        "tech1": "واجهة مستخدم متعددة اللغات",
        "tech2": "تصميم متجاوب مع جميع الأجهزة",
        "tech3": "نظام حماية متكامل",
        "tech4": "نسخ احتياطي تلقائي"
    },
    "en": {
        # Main Navigation
        "title": "🚍 Smart Bus System",
        "subtitle": "Al Muneera Private School - Abu Dhabi",
        "description": "Integrated system for smart school transportation management",
        "student": "🎓 Student",
        "driver": "🚌 Driver", 
        "parents": "👨‍👩‍👧 Parents",
        "admin": "🏫 Admin",
        "about": "ℹ️ About",
        
        # Student Page
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
        
        # Driver Page
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
        
        # Parents Page
        "parents_title": "👨‍👩‍👧 Parents Portal",
        "parents_id_placeholder": "Example: 1001",
        "attendance_tracking": "📊 Attendance Tracking",
        "bus_info": "🚌 Bus Information",
        "morning_time": "Approximate Morning Time",
        "afternoon_time": "Approximate Afternoon Time",
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
        
        # Admin Page
        "admin_title": "🏫 Admin Control Panel",
        "admin_login": "🔐 Admin Login",
        "admin_password": "Admin Password",
        "system_stats": "📊 System Statistics",
        "students_count": "Students Count",
        "attendance_records": "Attendance Records",
        "system_actions": "⚙️ System Actions",
        "reset_data": "🔄 Reset Data",
        "backup": "📥 Backup",
        "change_admin_password": "Change Admin Password",
        "current_passwords": "Current Passwords",
        "change_bus_password": "Change Bus Passwords",
        "select_bus_password": "Select Bus",
        "new_password": "New Password",
        "save_changes": "💾 Save Changes",
        
        # Student Management
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
        "manage_students": "👥 Manage Students",
        "export_data": "📤 Export Data",
        "filter_data": "🔍 Filter Data",
        "filter_by_bus": "Filter by Bus",
        "filter_by_grade": "Filter by Grade",
        "filter_by_status": "Filter by Status",
        "all": "All",
        
        # About Page
        "about_title": "ℹ️ About System",
        "about_description": "Integrated system for smart school transportation management at Al Muneera Private School in Abu Dhabi.",
        "features": "🎯 Main Features",
        "development_team": "👥 Development Team",
        "developer": "System Developer",
        "designer": "UI Designer",
        "version_info": "📋 Version Information",
        "version": "Version",
        "release_date": "Release Date",
        "status_stable": "⭐ Stable Release",
        
        # System Messages
        "not_found": "Student not found",
        "error": "System error occurred",
        "reset_success": "Your status has been reset",
        "login_success": "Login successful",
        "login_error": "Incorrect password",
        "data_reset_success": "Data reset successfully",
        "backup_success": "Backup created successfully",
        "password_updated": "Password updated successfully",
        
        # Settings
        "theme_light": "☀️",
        "theme_dark": "🌙",
        "language": "🌐",
        
        # Rating System
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
        
        # Footer
        "footer": "🚍 Smart Bus System - Version 2.0",
        "rights": "© 2025 All Rights Reserved",
        "team": "Developed by: Eyad Mustafa | Design: Ayman Galal | Supervision: Environmental Club",
        
        # Features
        "feature1": "Smart Attendance",
        "feature1_desc": "Automatic and easy student attendance system",
        "feature2": "Live Tracking", 
        "feature2_desc": "Real-time tracking of buses and attendance",
        "feature3": "Service Rating",
        "feature3_desc": "Advanced service quality rating system",
        "feature4": "Instant Notifications",
        "feature4_desc": "Instant notifications for parents",
        "feature5": "Modern Interface",
        "feature5_desc": "Modern and user-friendly design",
        "feature6": "Security & Protection",
        "feature6_desc": "Integrated data protection system",
        
        # Technical Specifications
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

# ===== وظائف مساعدة محسنة =====
def add_notification(message):
    st.session_state.notifications.append({
        "time": datetime.datetime.now().strftime("%H:%M"),
        "message": message
    })
    save_data()

def show_notification(message, type="info", duration=3):
    """عرض إشعار مؤقت"""
    if type == "success":
        st.success(message)
    elif type == "warning":
        st.warning(message)
    elif type == "error":
        st.error(message)
    else:
        st.info(message)

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

# ===== وظائف إدارة الطلاب =====
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

# ===== وظائف مساعدة للصفحات =====
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

# ===== ميزات تحسين تجربة المستخدم =====

def check_missing_attendance():
    """التحقق من الطلاب الذين لم يسجلوا حضور اليوم"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    registered_ids = st.session_state.attendance_df[
        st.session_state.attendance_df["date"] == today
    ]["id"].astype(str).tolist()
    
    missing_students = st.session_state.students_df[
        ~st.session_state.students_df["id"].astype(str).isin(registered_ids)
    ]
    
    return missing_students

def advanced_search_students():
    """بحث متقدم عن الطلاب"""
    st.subheader("🔍 بحث متقدم")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        search_name = st.text_input("بحث بالاسم", placeholder="أدخل اسم الطالب...")
    with col2:
        search_grade = st.selectbox("بحث بالصف", ["الكل"] + list(st.session_state.students_df["grade"].unique()))
    with col3:
        search_bus = st.selectbox("بحث بالباص", ["الكل", "1", "2", "3"])
    
    # تطبيق البحث
    filtered_df = st.session_state.students_df.copy()
    
    if search_name:
        filtered_df = filtered_df[filtered_df["name"].str.contains(search_name, case=False, na=False)]
    
    if search_grade != "الكل":
        filtered_df = filtered_df[filtered_df["grade"] == search_grade]
    
    if search_bus != "الكل":
        filtered_df = filtered_df[filtered_df["bus"] == search_bus]
    
    return filtered_df

def admin_dashboard():
    """لوحة تحكم تفاعلية للإدارة"""
    st.header("📊 لوحة التحكم التفاعلية")
    
    # إحصائيات حية
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = len(st.session_state.students_df)
        st.metric("👥 إجمالي الطلاب", total_students)
    
    with col2:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        today_attendance = st.session_state.attendance_df[
            st.session_state.attendance_df["date"] == today
        ] if not st.session_state.attendance_df.empty else pd.DataFrame()
        registered_today = len(today_attendance)
        st.metric("📝 المسجلين اليوم", registered_today)
    
    with col3:
        missing_today = len(check_missing_attendance())
        st.metric("⚠️ لم يسجلوا", missing_today)
    
    with col4:
        attendance_rate = (registered_today / total_students * 100) if total_students > 0 else 0
        st.metric("📈 نسبة التسجيل", f"{attendance_rate:.1f}%")
    
    # مخطط بياني مبسط
    st.subheader("📈 إحصائيات الحضور للأسبوع")
    
    # بيانات الحضور للأسبوع الحالي
    attendance_data = get_weekly_attendance()
    if not attendance_data.empty:
        st.bar_chart(attendance_data.set_index("day")["count"])

def get_weekly_attendance():
    """الحصول على إحصائيات الحضور للأسبوع"""
    dates = []
    counts = []
    
    for i in range(7):
        date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        count = len(st.session_state.attendance_df[
            st.session_state.attendance_df["date"] == date
        ])
        dates.append(date)
        counts.append(count)
    
    return pd.DataFrame({
        "day": dates[::-1],
        "count": counts[::-1]
    })

def send_parent_notification(student_id, message_type):
    """إرسال إشعارات للوالدين"""
    student = st.session_state.students_df[
        st.session_state.students_df["id"].astype(str) == str(student_id)
    ].iloc[0]
    
    messages = {
        "attendance_registered": f"تم تسجيل حضور الطالب {student['name']} اليوم",
        "bus_departure": f"باص المدرسة رقم {student['bus']} في طريقه إلى المدرسة",
        "bus_arrival": f"باص المدرسة رقم {student['bus']} وصل إلى المدرسة",
        "delay": f"تأخير متوقع في باص المدرسة رقم {student['bus']}"
    }
    
    message = messages.get(message_type, "إشعار من نظام الباص الذكي")
    
    # محاكاة إرسال الإشعار
    show_notification(f"📱 إشعار: {message}", "info")

def check_connection():
    """التحقق من الاتصال بالإنترنت"""
    try:
        # محاولة الاتصال بخدمة خارجية
        requests.get("https://www.google.com", timeout=3)
        st.session_state.offline_mode = False
        return True
    except:
        st.session_state.offline_mode = True
        return False

def sync_offline_data():
    """مزامنة البيانات عند العودة للاتصال"""
    if st.session_state.offline_mode:
        st.warning("🔄 مزامنة البيانات...")
        save_data()
        st.session_state.offline_mode = False
        st.success("✅ تمت المزامنة بنجاح!")

def add_keyboard_shortcuts():
    """إضافة اختصارات لوحة المفاتيح"""
    st.markdown("""
    <script>
    document.addEventListener('keydown', function(e) {
        // اختصار للبحث (Ctrl/Cmd + K)
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[placeholder*="بحث"]');
            if (searchInput) searchInput.focus();
        }
        // اختصار للصفحة الرئيسية (Ctrl/Cmd + H)
        if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
            e.preventDefault();
            window.location.href = window.location.origin;
        }
    });
    </script>
    """, unsafe_allow_html=True)

def accessibility_features():
    """ميزات تحسين الوصول"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("♿ إعدادات الوصول")
    
    # حجم الخط
    font_size = st.sidebar.selectbox("حجم الخط", ["افتراضي", "كبير", "كبير جداً"], 
                                   index=["افتراضي", "كبير", "كبير جداً"].index(st.session_state.font_size))
    
    # وضع التباين العالي
    high_contrast = st.sidebar.checkbox("وضع التباين العالي", value=st.session_state.high_contrast)
    
    if font_size != st.session_state.font_size or high_contrast != st.session_state.high_contrast:
        st.session_state.font_size = font_size
        st.session_state.high_contrast = high_contrast
        save_data()
        st.rerun()
    
    return font_size, high_contrast

def apply_accessibility_styles(font_size, high_contrast):
    """تطبيق إعدادات الوصول"""
    styles = ""
    
    if font_size == "كبير":
        styles += "body { font-size: 1.2rem; }"
    elif font_size == "كبير جداً":
        styles += "body { font-size: 1.4rem; }"
    
    if high_contrast:
        styles += """
        .stApp { background: #000000 !important; color: #FFFFFF !important; }
        .main-header { background: #333333 !important; color: #FFFFFF !important; }
        .metric-card { background: #222222 !important; color: #FFFFFF !important; border: 2px solid #FFFFFF !important; }
        """
    
    if styles:
        st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)

def interactive_tour():
    """جولة تفاعلية للمستخدمين الجدد"""
    if st.session_state.first_time:
        st.info("""
        🎯 **مرحباً بك في نظام الباص الذكي!**
        
        **جولة سريعة:**
        - 🎓 **الطلاب**: سجل حضورك اليومي
        - 🚌 **السائقون**: تابع طلاب باصك
        - 👨‍👩‍👧 **أولياء الأمور**: تابع أبناءك
        - 🏫 **الإدارة**: أدير النظام بالكامل
        
        💡 **نصائح سريعة:**
        - استخدم Ctrl+K للبحث السريع
        - اضغط على ❓ للمساعدة في أي صفحة
        - البيانات تحفظ تلقائياً
        
        اضغط على ❌ لإغلاق هذه الرسالة
        """)
        
        if st.button("❌ فهمت، شكراً!"):
            st.session_state.first_time = False
            save_data()
            st.rerun()

def context_help():
    """مساعدة سياقية حسب الصفحة"""
    help_messages = {
        "student": """
        **💡 نصائح للطلاب:**
        - أدخل رقم وزارتك بدقة
        - سجل حضورك قبل الساعة 8 صباحاً
        - يمكنك تغيير حالتك إذا أخطأت
        - استخدم Ctrl+K للبحث السريع
        """,
        "driver": """
        **💡 نصائح للسائقين:**
        - تأكد من كلمة المرور قبل الدخول
        - راجع قائمة الحضور قبل الانطلاق
        - اتصل بالطلاب المتأخرين إذا لزم الأمر
        - استخدم Ctrl+K للبحث السريع
        """,
        "parents": """
        **💡 نصائح لأولياء الأمور:**
        - احفظ رقم وزارة ابنك
        - تابع حالة الباص بانتظام
        - اتصل بالسائق في الحالات الطارئة
        - استخدم Ctrl+K للبحث السريع
        """,
        "admin": """
        **💡 نصائح للإدارة:**
        - احفظ نسخة احتياطية بانتظام
        - راجع التقارير اليومية
        - حدث بيانات الطلاب عند الحاجة
        - استخدم Ctrl+K للبحث السريع
        """,
        "about": """
        **💡 حول النظام:**
        - نظام متكامل لإدارة النقل المدرسي
        - واجهة مستخدم سهلة ومتطورة
        - دعم كامل للغتين العربية والإنجليزية
        - نظام حماية متكامل للبيانات
        """
    }
    
    if st.sidebar.button("❓ مساعدة سياقية"):
        st.sidebar.info(help_messages.get(st.session_state.page, "مرحباً بك في النظام!"))

def auto_save_reminder():
    """تذكير الحفظ التلقائي"""
    time_since_save = (datetime.datetime.now() - st.session_state.last_save).seconds
    
    if time_since_save > 300:  # 5 دقائق
        st.toast("💾 يتم حفظ بياناتك تلقائياً...", icon="✅")
        save_data()
        st.session_state.last_save = datetime.datetime.now()

def performance_optimization():
    """تحسينات الأداء"""
    try:
        # تنظيف البيانات القديمة (أكثر من 30 يوم)
        if st.session_state.attendance_df.empty:
            return
            
        old_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        
        # طريقة أكثر أماناً للتعامل مع التواريخ
        def is_old_date(date_str):
            try:
                return str(date_str) < old_date
            except:
                return False
        
        old_records_mask = st.session_state.attendance_df["date"].apply(is_old_date)
        old_records = st.session_state.attendance_df[old_records_mask]
        
        if len(old_records) > 100:
            st.session_state.attendance_df = st.session_state.attendance_df[~old_records_mask]
            save_data()
            show_notification(f"تم تنظيف {len(old_records)} سجل قديم", "info")
            
    except Exception as e:
        # تسجيل الخطأ دون إيقاف التطبيق
        print(f"Warning: Performance optimization skipped due to error: {e}")

# ===== تطبيق الميزات المحسنة =====

# التحقق من الاتصال
check_connection()

# إضافة اختصارات لوحة المفاتيح
add_keyboard_shortcuts()

# الجولة التفاعلية
interactive_tour()

# تحسين الأداء
performance_optimization()

# تذكير الحفظ التلقائي
auto_save_reminder()

# ===== تصميم حديث ومتطور مع إعدادات الوصول =====
def apply_modern_styles():
    font_size, high_contrast = accessibility_features()
    
    if st.session_state.theme == "dark":
        primary_color = "#6366f1"
        background = "linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)"
        card_bg = "rgba(30, 41, 59, 0.7)"
        text_color = "#f8fafc"
    else:
        primary_color = "#3b82f6"
        background = "linear-gradient(135deg, #eff6ff 0%, #dbeafe 50%, #bfdbfe 100%)"
        card_bg = "rgba(255, 255, 255, 0.9)"
        text_color = "#1e293b"
    
    # تطبيق إعدادات الوصول
    if high_contrast:
        background = "#000000" if st.session_state.theme == "dark" else "#FFFFFF"
        card_bg = "#333333" if st.session_state.theme == "dark" else "#F0F0F0"
        text_color = "#FFFFFF" if st.session_state.theme == "dark" else "#000000"
        primary_color = "#FFD700"  # ذهبي للتباين العالي
    
    base_styles = f"""
    <style>
        .stApp {{
            background: {background};
            color: {text_color};
        }}
        
        .main-header {{
            background: {card_bg};
            backdrop-filter: blur(20px);
            padding: 3rem 2rem;
            border-radius: 24px;
            color: {text_color};
            text-align: center;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        
        .stat-card {{
            background: {card_bg};
            backdrop-filter: blur(15px);
            color: {text_color};
            padding: 2rem 1.5rem;
            border-radius: 20px;
            text-align: center;
            margin: 0.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }}
        
        .feature-card {{
            background: {card_bg};
            backdrop-filter: blur(12px);
            color: {text_color};
            padding: 2rem;
            border-radius: 20px;
            margin: 1rem 0;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }}
        
        .feature-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.15);
        }}
        
        .student-card {{
            background: {card_bg};
            backdrop-filter: blur(12px);
            padding: 1.5rem;
            border-radius: 16px;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: {text_color};
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }}
        
        .nav-button {{
            background: {card_bg} !important;
            color: {text_color} !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            padding: 0.75rem 1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }}
        
        .nav-button:hover {{
            background: {primary_color} !important;
            color: white !important;
            transform: translateY(-2px) !important;
        }}
        
        .stButton>button {{
            background: linear-gradient(135deg, {primary_color} 0%, #8b5cf6 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        }}
        
        .stTextInput>div>div>input {{
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 0.75rem 1rem;
            background: {card_bg};
            color: {text_color};
            transition: all 0.3s ease;
        }}
        
        .stTextInput>div>div>input:focus {{
            border-color: {primary_color};
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }}
        
        .stSelectbox>div>div>select {{
            background: {card_bg};
            color: {text_color};
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 0.75rem;
        }}
        
        .section-title {{
            color: {text_color};
            text-align: center;
            margin-bottom: 2rem;
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, {primary_color}, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .info-text {{
            color: {text_color};
            text-align: center;
            margin-bottom: 3rem;
            font-size: 1.2rem;
            line-height: 1.6;
            opacity: 0.9;
        }}
        
        .metric-card {{
            background: {card_bg};
            backdrop-filter: blur(12px);
            padding: 1.5rem;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
        }}
    </style>
    """
    
    st.markdown(base_styles, unsafe_allow_html=True)
    apply_accessibility_styles(font_size, high_contrast)

apply_modern_styles()

# ===== الهيدر الرئيسي المحدث =====
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    stats = calculate_attendance_stats()
    st.markdown(f"""
    <div class='stat-card'>
        <h3 style='margin-bottom: 0.5rem; font-size: 1.8rem;'>📊</h3>
        <h4 style='margin: 0; font-size: 1rem;'>{t('attendance_rate')}</h4>
        <h2 style='margin: 0.5rem 0; font-size: 2rem; color: #10b981;'>{stats['percentage']:.0f}%</h2>
        <p style='margin: 0; opacity: 0.8; font-size: 0.9rem;'>{stats['coming']}/{stats['total']} {t('students_count').lower()}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='main-header'>
        <h1 style='font-size: 3.5rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>{t('title')}</h1>
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

# عرض حالة الاتصال
if st.session_state.offline_mode:
    st.warning("🔴 الوضع غير متصل - يتم حفظ البيانات محلياً")
    if st.button("🔄 محاولة إعادة الاتصال", key="reconnect_btn"):
        if check_connection():
            sync_offline_data()
            st.rerun()

# ===== شريط التنقل المحدث =====
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
        button_style = f"""
        <style>
            div[data-testid="stButton"] > button[kind="secondary"] {{
                background: {'linear-gradient(135deg, #3b82f6, #8b5cf6)' if is_active else 'rgba(255, 255, 255, 0.1)'} !important;
                color: {'white' if is_active else 'inherit'} !important;
                border: {'none' if is_active else '1px solid rgba(255, 255, 255, 0.2)'} !important;
            }}
        </style>
        """
        st.markdown(button_style, unsafe_allow_html=True)
        if st.button(name, use_container_width=True, type="secondary" if not is_active else "primary", key=f"nav_{page_key}"):
            st.session_state.page = page_key
            st.rerun()

st.markdown("---")

# إضافة المساعدة السياقية
context_help()

# ===== صفحة الطالب المحدثة =====
if st.session_state.page == "student":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"<h2 class='section-title'>{t('student_title')}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='info-text'>{t('student_desc')}</p>", unsafe_allow_html=True)
        
        with st.container():
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
                        
                        st.success(f"🎓 تم العثور على الطالب: **{student['name']}**")
                        
                        # معلومات الطالب في بطاقة جميلة
                        col_info1, col_info2 = st.columns(2)
                        with col_info1:
                            st.markdown(f"""
                            <div class='metric-card'>
                                <h4>📚 {t('grade')}</h4>
                                <h3>{student['grade']}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"""
                            <div class='metric-card'>
                                <h4>🚍 {t('bus')}</h4>
                                <h3>{student['bus']}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_info2:
                            st.markdown(f"""
                            <div class='metric-card'>
                                <h4>📞 {t('parent_phone')}</h4>
                                <h3>{student['parent_phone']}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        already_registered, current_status = has_student_registered_today(student_id)
                        
                        if already_registered:
                            st.warning(f"**✅ {t('already_registered')}**\n\n**{t('current_status')}:** {current_status}")
                            
                            if st.button(t("change_status"), key="change_status_btn"):
                                today = datetime.datetime.now().strftime("%Y-%m-%d")
                                st.session_state.attendance_df = st.session_state.attendance_df[
                                    ~((st.session_state.attendance_df["id"].astype(str) == str(student_id).strip()) & 
                                      (st.session_state.attendance_df["date"] == today))
                                ]
                                save_data()
                                st.success(t("reset_success"))
                                st.rerun()
                        
                        else:
                            st.info(f"**{t('choose_status')}**")
                            
                            col_btn1, col_btn2 = st.columns(2)
                            with col_btn1:
                                if st.button(t("coming"), use_container_width=True, key="coming_btn"):
                                    now = register_attendance(student, "قادم")
                                    send_parent_notification(student_id, "attendance_registered")
                                    st.balloons()
                                    st.success(f"""
                                    **🎉 {t('registered_success')}**
                                    
                                    **{t('student_name')}:** {student['name']}
                                    **{t('status')}:** {t('status_coming')}
                                    **{t('time')}:** {now.strftime('%H:%M')}
                                    **{t('bus_number')}:** {student['bus']}
                                    """)
                            with col_btn2:
                                if st.button(t("not_coming"), use_container_width=True, key="not_coming_btn"):
                                    now = register_attendance(student, "لن يحضر")
                                    send_parent_notification(student_id, "attendance_registered")
                                    st.success(f"""
                                    **🎉 {t('registered_success')}**
                                    
                                    **{t('student_name')}:** {student['name']}
                                    **{t('status')}:** {t('status_not_coming')}
                                    **{t('time')}:** {now.strftime('%H:%M')}
                                    **{t('bus_number')}:** {student['bus']}
                                    """)
                    
                    else:
                        st.error(f"❌ {t('not_found')}")
                        
                except Exception as e:
                    st.error(f"❌ {t('error')}")

    with col2:
        st.markdown(f"<h3 style='text-align: center; margin-bottom: 2rem;'>{t('stats_title')}</h3>", unsafe_allow_html=True)
        
        stats = calculate_attendance_stats()
        
        st.markdown(f"""
        <div class='metric-card'>
            <h4>👥 {t('total_registered')}</h4>
            <h2 style='color: #3b82f6;'>{stats['total']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-card'>
            <h4>✅ {t('expected_attendance')}</h4>
            <h2 style='color: #10b981;'>{stats['coming']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-card'>
            <h4>📈 {t('attendance_rate')}</h4>
            <h2 style='color: #f59e0b;'>{stats['percentage']:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)

# ===== صفحة السائق المحدثة =====
elif st.session_state.page == "driver":
    st.markdown(f"<h2 class='section-title'>{t('driver_title')}</h2>", unsafe_allow_html=True)
    
    if not st.session_state.driver_logged_in:
        st.markdown(f"<h3 style='text-align: center; margin-bottom: 2rem;'>{t('driver_login')}</h3>", unsafe_allow_html=True)
        
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                bus_number = st.selectbox(t("select_bus"), ["1", "2", "3"], key="driver_bus_select")
            with col2:
                password = st.text_input(t("password"), type="password", placeholder=t("password_placeholder"), key="driver_password")
            
            if st.button(t("login"), use_container_width=True, key="driver_login_btn"):
                if password == st.session_state.bus_passwords.get(bus_number, ""):
                    st.session_state.driver_logged_in = True
                    st.session_state.current_bus = bus_number
                    st.success(t("login_success"))
                    st.rerun()
                else:
                    st.error(t("login_error"))
    
    else:
        st.success(f"✅ {t('login_success')} - {t('bus')} {st.session_state.current_bus}")
        
        if st.button(t("logout"), key="driver_logout_btn"):
            st.session_state.driver_logged_in = False
            st.rerun()
        
        # إحصائيات الباص
        bus_students = get_bus_students(st.session_state.current_bus)
        today_attendance = get_today_attendance_for_bus(st.session_state.current_bus)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <h4>👥 {t('total_students')}</h4>
                <h3>{len(bus_students)}</h3>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            coming_today = len(today_attendance[today_attendance["status"] == "قادم"]) if not today_attendance.empty else 0
            st.markdown(f"""
            <div class='metric-card'>
                <h4>✅ {t('confirmed_attendance')}</h4>
                <h3 style='color: #10b981;'>{coming_today}</h3>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            not_coming = len(today_attendance[today_attendance["status"] == "لن يحضر"]) if not today_attendance.empty else 0
            st.markdown(f"""
            <div class='metric-card'>
                <h4>❌ الغياب</h4>
                <h3 style='color: #ef4444;'>{not_coming}</h3>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            percentage = (coming_today / len(bus_students) * 100) if len(bus_students) > 0 else 0
            st.markdown(f"""
            <div class='metric-card'>
                <h4>📈 {t('attendance_percentage')}</h4>
                <h3 style='color: #f59e0b;'>{percentage:.1f}%</h3>
            </div>
            """, unsafe_allow_html=True)
        
        # إشعار انطلاق الباص
        if st.button("🚀 إشعار انطلاق الباص", key="bus_departure_btn"):
            for _, student in bus_students.iterrows():
                send_parent_notification(student["id"], "bus_departure")
            show_notification("تم إرسال إشعار انطلاق الباص لجميع أولياء الأمور", "success")
        
        # قائمة الطلاب القادمين اليوم
        st.subheader(f"🎒 {t('coming_students')}")
        
        if not today_attendance.empty:
            coming_students = today_attendance[today_attendance["status"] == "قادم"]
            
            if not coming_students.empty:
                for _, student in coming_students.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div class='student-card'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <div>
                                    <h4 style='margin: 0;'>{student['name']}</h4>
                                    <p style='margin: 0; opacity: 0.8;'>📚 {student['grade']}</p>
                                </div>
                                <div style='text-align: right;'>
                                    <span style='color: #10b981; font-weight: bold;'>✅ {t('status_coming')}</span>
                                    <p style='margin: 0; font-size: 0.8rem; opacity: 0.7;'>⏰ {student['time']}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info(f"🚫 {t('no_students')}")
        else:
            st.info(f"🚫 {t('no_students')}")

# ===== صفحة أولياء الأمور المحدثة =====
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
                        st.markdown(f"""
                        <div class='metric-card'>
                            <h4>📚 {t('grade')}</h4>
                            <h3>{student['grade']}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_info2:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <h4>🚍 {t('bus')}</h4>
                            <h3>{student['bus']}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # حالة اليوم
                    st.subheader(t("today_status"))
                    already_registered, current_status = has_student_registered_today(student_id)
                    
                    if already_registered:
                        today = datetime.datetime.now().strftime("%Y-%m-%d")
                        registration_data = st.session_state.attendance_df[
                            (st.session_state.attendance_df["id"].astype(str) == str(student_id).strip()) & 
                            (st.session_state.attendance_df["date"] == today)
                        ]
                        
                        if not registration_data.empty:
                            registration_time = registration_data.iloc[0]["time"]
                            
                            if current_status == "قادم":
                                st.success(f"""
                                **✅ {t('today_status')}:** {t('status_coming')}
                                **⏰ {t('registration_time')}:** {registration_time}
                                """)
                            else:
                                st.error(f"""
                                **❌ {t('today_status')}:** {t('status_not_coming')}
                                **⏰ {t('registration_time')}:** {registration_time}
                                """)
                    else:
                        st.warning(f"**⏳ {t('today_status')}:** {t('status_not_registered')}")
                
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
                st.markdown(f"""
                <div class='metric-card'>
                    <h4>🌅 {t('morning_pickup')}</h4>
                    <h3>{schedule['morning']}</h3>
                </div>
                """, unsafe_allow_html=True)
            with col_time2:
                st.markdown(f"""
                <div class='metric-card'>
                    <h4>🌇 {t('evening_return')}</h4>
                    <h3>{schedule['evening']}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            # معلومات السائق
            st.subheader(t("driver_contact"))
            st.markdown(f"""
            <div class='metric-card'>
                <h4>👤 {t('driver_contact')}</h4>
                <p><strong>الاسم:</strong> {driver['name']}</p>
                <p><strong>📞 الهاتف:</strong> {driver['phone']}</p>
            </div>
            """, unsafe_allow_html=True)

# ===== صفحة الإدارة المحدثة =====
elif st.session_state.page == "admin":
    st.markdown(f"<h2 class='section-title'>{t('admin_title')}</h2>", unsafe_allow_html=True)
    
    if not st.session_state.admin_logged_in:
        st.markdown(f"<h3 style='text-align: center; margin-bottom: 2rem;'>{t('admin_login')}</h3>", unsafe_allow_html=True)
        
        with st.container():
            admin_password = st.text_input(t("admin_password"), type="password", placeholder=t("password_placeholder"), key="admin_login_password")
            
            if st.button(t("login"), use_container_width=True, key="admin_login_btn"):
                if admin_password == st.session_state.admin_password:
                    st.session_state.admin_logged_in = True
                    st.success(t("login_success"))
                    st.rerun()
                else:
                    st.error(t("login_error"))
    
    else:
        st.success(f"✅ {t('login_success')}")
        
        if st.button(t("logout"), key="admin_logout_btn"):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        # تبويبات الإدارة المحسنة
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "👥 " + t("manage_students"),
            "📊 لوحة التحكم",
            "🔍 بحث متقدم", 
            "🔐 " + t("change_bus_password"),
            "⚙️ " + t("change_admin_password")
        ])
        
        with tab1:
            st.header("👥 " + t("manage_students"))
            
            # إحصائيات سريعة
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_students = len(st.session_state.students_df)
                st.metric(t("students_count"), total_students)
            with col2:
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                today_attendance = st.session_state.attendance_df[
                    st.session_state.attendance_df["date"] == today
                ] if not st.session_state.attendance_df.empty else pd.DataFrame()
                registered_today = len(today_attendance)
                st.metric("المسجلين اليوم", registered_today)
            with col3:
                coming_today = len(today_attendance[today_attendance["status"] == "قادم"]) if not today_attendance.empty else 0
                st.metric(t("expected_attendance"), coming_today)
            with col4:
                attendance_rate = (coming_today / total_students * 100) if total_students > 0 else 0
                st.metric(t("attendance_rate"), f"{attendance_rate:.1f}%")
            
            # قسم إضافة طالب جديد
            st.subheader("➕ " + t("add_student"))
            
            with st.form("add_student_form"):
                st.markdown(f"<h4 style='margin-bottom: 1rem;'>{t('new_student_info')}</h4>", unsafe_allow_html=True)
                
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

        with tab2:
            admin_dashboard()

        with tab3:
            filtered_students = advanced_search_students()
            st.subheader(f"📋 نتائج البحث ({len(filtered_students)} طالب)")
            
            if not filtered_students.empty:
                for _, student in filtered_students.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div class='student-card'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <div>
                                    <h4 style='margin: 0;'>{student['name']}</h4>
                                    <p style='margin: 0; opacity: 0.8;'>📚 {student['grade']} | 🚍 الباص {student['bus']}</p>
                                </div>
                                <div style='text-align: right;'>
                                    <p style='margin: 0; font-size: 0.9rem; opacity: 0.7;'>📞 {student['parent_phone']}</p>
                                    <p style='margin: 0; font-size: 0.8rem; opacity: 0.6;'>🆔 {student['id']}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("🚫 لا توجد نتائج تطابق معايير البحث")

        with tab4:
            st.header("🔐 " + t("change_bus_password"))
            
            st.info("💡 هنا يمكنك تغيير كلمات مرور الباصات للسائقين")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("كلمات المرور الحالية")
                for bus_num, password in st.session_state.bus_passwords.items():
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h4>🚍 الباص {bus_num}</h4>
                        <h3>{password}</h3>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.subheader("تغيير كلمة المرور")
                
                with st.form("change_bus_password_form"):
                    selected_bus = st.selectbox(
                        t("select_bus_password"),
                        ["1", "2", "3"],
                        key="change_bus_select"
                    )
                    
                    new_bus_password = st.text_input(
                        t("new_password"),
                        type="password",
                        placeholder="أدخل كلمة المرور الجديدة...",
                        key="new_bus_password"
                    )
                    
                    confirm_bus_password = st.text_input(
                        "تأكيد كلمة المرور",
                        type="password", 
                        placeholder="أعد إدخال كلمة المرور...",
                        key="confirm_bus_password"
                    )
                    
                    change_bus_submit = st.form_submit_button(t("save_changes"), use_container_width=True)
                    
                    if change_bus_submit:
                        if not new_bus_password:
                            st.error("❌ يرجى إدخال كلمة المرور الجديدة")
                        elif new_bus_password != confirm_bus_password:
                            st.error("❌ كلمات المرور غير متطابقة")
                        else:
                            st.session_state.bus_passwords[selected_bus] = new_bus_password
                            save_data()
                            st.success(f"✅ تم تغيير كلمة مرور الباص {selected_bus} بنجاح")
                            st.rerun()

        with tab5:
            st.header("⚙️ " + t("change_admin_password"))
            
            st.warning("⚠️ كن حذراً عند تغيير كلمة مرور الإدارة")
            
            with st.form("change_admin_password_form"):
                current_admin_password = st.text_input(
                    "كلمة المرور الحالية",
                    type="password",
                    placeholder="أدخل كلمة المرور الحالية...",
                    key="current_admin_password"
                )
                
                new_admin_password = st.text_input(
                    t("new_password"),
                    type="password",
                    placeholder="أدخل كلمة المرور الجديدة...",
                    key="new_admin_password"
                )
                
                confirm_admin_password = st.text_input(
                    "تأكيد كلمة المرور الجديدة",
                    type="password",
                    placeholder="أعد إدخال كلمة المرور الجديدة...",
                    key="confirm_admin_password"
                )
                
                change_admin_submit = st.form_submit_button(t("save_changes"), use_container_width=True)
                
                if change_admin_submit:
                    if not current_admin_password:
                        st.error("❌ يرجى إدخال كلمة المرور الحالية")
                    elif current_admin_password != st.session_state.admin_password:
                        st.error("❌ كلمة المرور الحالية غير صحيحة")
                    elif not new_admin_password:
                        st.error("❌ يرجى إدخال كلمة المرور الجديدة")
                    elif new_admin_password != confirm_admin_password:
                        st.error("❌ كلمات المرور غير متطابقة")
                    else:
                        st.session_state.admin_password = new_admin_password
                        save_data()
                        st.success("✅ تم تغيير كلمة مرور الإدارة بنجاح")
                        st.rerun()

# ===== صفحة حول النظام المحدثة =====
elif st.session_state.page == "about":
    st.markdown(f"<h2 class='section-title'>{t('about_title')}</h2>", unsafe_allow_html=True)
    
    st.markdown(f"<p class='info-text'>{t('about_description')}</p>", unsafe_allow_html=True)
    
    # المميزات الرئيسية
    st.subheader("🎯 " + t("features"))
    
    features = [
        ("🚍", t("feature1"), t("feature1_desc")),
        ("📱", t("feature2"), t("feature2_desc")),
        ("⭐", t("feature3"), t("feature3_desc")),
        ("🔔", t("feature4"), t("feature4_desc")),
        ("🎨", t("feature5"), t("feature5_desc")),
        ("🔒", t("feature6"), t("feature6_desc"))
    ]
    
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='feature-card'>
                <div style='font-size: 2.5rem; margin-bottom: 1rem;'>{icon}</div>
                <h3 style='margin-bottom: 0.5rem;'>{title}</h3>
                <p style='opacity: 0.8; line-height: 1.5;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # فريق التطوير
    st.subheader("👥 " + t("development_team"))
    
    team_cols = st.columns(3)
    with team_cols[0]:
        st.markdown(f"""
        <div class='feature-card'>
            <h3>🛠️ {t('developer')}</h3>
            <p><strong>إياد مصطفى</strong></p>
            <p>مسؤول عن التطوير البرمجي والوظائف التقنية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with team_cols[1]:
        st.markdown(f"""
        <div class='feature-card'>
            <h3>🎨 {t('designer')}</h3>
            <p><strong>ايمن جلال</strong></p>
            <p>مسؤول عن التصميم وتجربة المستخدم</p>
        </div>
        """, unsafe_allow_html=True)
    
    with team_cols[2]:
        st.markdown(f"""
        <div class='feature-card'>
            <h3>👨‍🏫 الإشراف</h3>
            <p><strong>قسم النادي البيئي</strong></p>
            <p>الإشراف العام ومتابعة الجودة</p>
        </div>
        """, unsafe_allow_html=True)

# ===== الفوتر المحدث =====
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 3rem 1rem;'>
    <h4 style='margin-bottom: 0.5rem;'>🚍 {t('footer')}</h4>
    <p style='margin-bottom: 0.5rem; opacity: 0.8;'>{t('rights')}</p>
    <p style='font-size: 0.9rem; opacity: 0.7;'>{t('team')}</p>
</div>
""", unsafe_allow_html=True)
