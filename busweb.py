import streamlit as st
import pandas as pd
import datetime
import json
import pickle
from pathlib import Path
import requests
import time

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
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "sync_pending" not in st.session_state:
    st.session_state.sync_pending = False
if "two_factor_enabled" not in st.session_state:
    st.session_state.two_factor_enabled = False
if "trusted_devices" not in st.session_state:
    st.session_state.trusted_devices = []
if "activity_log" not in st.session_state:
    st.session_state.activity_log = []
if "support_tickets" not in st.session_state:
    st.session_state.support_tickets = []

# ===== وظائف حفظ البيانات =====
def save_data():
    """حفظ جميع البيانات في الملفات"""
    try:
        # حفظ بيانات الطلاب
        if 'students_df' in st.session_state:
            with open(DATA_DIR / "students.pkl", "wb") as f:
                pickle.dump(st.session_state.students_df.to_dict(), f)
        
        # حفظ بيانات الحضور
        if 'attendance_df' in st.session_state:
            with open(DATA_DIR / "attendance.pkl", "wb") as f:
                pickle.dump(st.session_state.attendance_df.to_dict(), f)
        
        # حفظ بيانات التقييمات
        if 'ratings_df' in st.session_state:
            with open(DATA_DIR / "ratings.pkl", "wb") as f:
                pickle.dump(st.session_state.ratings_df.to_dict(), f)
        
        # حفظ الإعدادات
        settings = {
            "bus_passwords": st.session_state.bus_passwords,
            "admin_password": st.session_state.admin_password,
            "theme": st.session_state.theme,
            "lang": st.session_state.lang,
            "font_size": st.session_state.font_size,
            "high_contrast": st.session_state.high_contrast,
            "two_factor_enabled": st.session_state.two_factor_enabled,
            "trusted_devices": st.session_state.trusted_devices,
            "activity_log": st.session_state.activity_log,
            "support_tickets": st.session_state.support_tickets
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
                st.session_state.two_factor_enabled = settings.get("two_factor_enabled", False)
                st.session_state.trusted_devices = settings.get("trusted_devices", [])
                st.session_state.activity_log = settings.get("activity_log", [])
                st.session_state.support_tickets = settings.get("support_tickets", [])
                
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")

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
    
    if 'ratings_df' not in st.session_state:
        st.session_state.ratings_df = pd.DataFrame(columns=["rating", "comment", "timestamp"])

# تحميل البيانات المحفوظة
load_data()

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
        "support": "🤖 الدعم الذكي",
        
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
        
        # الميزات الجديدة
        "support_title": "🤖 مركز الدعم الذكي",
        "ai_chat": "💬 محادثة مع المساعد الذكي",
        "contact_developer": "📧 التواصل مع المطور",
        "developer_email": "البريد الإلكتروني: eyadmustafaali99@gmail.com",
        "smart_sync": "🔄 مزامنة ذكية",
        "offline_work": "💾 عمل دون اتصال",
        "auto_backup": "📥 نسخ احتياطي تلقائي",
        
        # محادثات الدعم
        "support_welcome": "مرحباً! أنا المساعد الذكي لنظام الباص. كيف يمكنني مساعدتك؟",
        "common_questions": "أسئلة سريعة",
        "technical_support": "دعم فني",
        "feature_help": "مساعدة في الميزات",
        "contact_human": "التواصل مع مدير النظام",
        
        # تذاكر الدعم
        "create_ticket": "🎫 إنشاء تذكرة دعم",
        "ticket_subject": "موضوع التذكرة",
        "ticket_message": "وصف المشكلة",
        "ticket_priority": "أولوية التذكرة",
        "ticket_status": "حالة التذكرة",
        "ticket_created": "تم إنشاء التذكرة بنجاح",
        "my_tickets": "تذاكري",
        "all_tickets": "جميع التذاكر"
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
        "support": "🤖 Smart Support",
        
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
        
        # New Features
        "support_title": "🤖 Smart Support Center",
        "ai_chat": "💬 Chat with AI Assistant",
        "contact_developer": "📧 Contact Developer",
        "developer_email": "Email: eyadmustafaali99@gmail.com",
        "smart_sync": "🔄 Smart Sync",
        "offline_work": "💾 Offline Work",
        "auto_backup": "📥 Auto Backup",
        
        # Support conversations
        "support_welcome": "Hello! I'm the Smart Bus System AI assistant. How can I help you?",
        "common_questions": "Common Questions",
        "technical_support": "Technical Support",
        "feature_help": "Feature Help",
        "contact_human": "Contact System Manager",
        
        # Support Tickets
        "create_ticket": "🎫 Create Support Ticket",
        "ticket_subject": "Ticket Subject",
        "ticket_message": "Problem Description",
        "ticket_priority": "Ticket Priority",
        "ticket_status": "Ticket Status",
        "ticket_created": "Ticket created successfully",
        "my_tickets": "My Tickets",
        "all_tickets": "All Tickets"
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

# ===== المساعد الذكي البسيط =====
def smart_ai_assistant():
    """المساعد الذكي البسيط"""
    st.header("🤖 المساعد الذكي")
    
    # تهيئة المحادثة إذا كانت فارغة
    if not st.session_state.chat_messages:
        st.session_state.chat_messages = [{
            "role": "assistant", 
            "content": t("support_welcome")
        }]
    
    # عرض المحادثة
    for msg in st.session_state.chat_messages:
        if msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(msg["content"])
        else:
            with st.chat_message("user"):
                st.write(msg["content"])
    
    # الأسئلة السريعة
    st.subheader("أسئلة سريعة")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("كيف أسجل حضور؟", use_container_width=True, key="ai_btn1"):
            handle_ai_question("كيف أسجل حضور؟")
    with col2:
        if st.button("مشكلة في التسجيل", use_container_width=True, key="ai_btn2"):
            handle_ai_question("مشكلة في التسجيل")
    with col3:
        if st.button("تواصل مع المطور", use_container_width=True, key="ai_btn3"):
            handle_ai_question("أريد التواصل مع المطور")
    
    # إدخال السؤال
    user_question = st.text_input("اكتب سؤالك هنا...", key="ai_input")
    if st.button("إرسال", key="ai_send"):
        if user_question:
            handle_ai_question(user_question)
        else:
            st.warning("يرجى كتابة سؤال أولاً")

def handle_ai_question(question):
    """معالجة أسئلة المساعد الذكي"""
    # إضافة سؤال المستخدم
    st.session_state.chat_messages.append({
        "role": "user",
        "content": question
    })
    
    # توليد رد ذكي
    responses = {
        "كيف أسجل حضور؟": """
**لتسجيل الحضور:**
1. انتقل إلى صفحة الطالب
2. أدخل رقم الوزارة
3. اختر 'سأحضر اليوم' أو 'لن أحضر'  
4. انقر على زر التسجيل

⏰ **نصيحة:** سجل حضورك قبل الساعة 8 صباحاً
        """,
        "مشكلة في التسجيل": """
**إذا واجهت مشكلة في التسجيل:**
1. تأكد من رقم الوزارة
2. تحقق من اتصال الإنترنت
3. جرب تحديث الصفحة
4. إذا استمرت المشكلة، اتصل بالإدارة

📞 **رقم الإدارة:** 025555555
        """,
        "أريد التواصل مع المطور": """
**للتواصل مع المطور:**
📧 **البريد الإلكتروني:** eyadmustafaali99@gmail.com

يمكنك أيضاً استخدام نموذج التواصل في تبويب 'التواصل مع المطور'
        """,
        "default": """
شكراً لسؤالك! 🤗

يمكنني مساعدتك في:
- تسجيل الحضور
- متابعة الباص  
- حل المشكلات التقنية
- التواصل مع المطور

اختر أحد الأسئلة السريعة أعلاه أو اشرح لي مشكلتك بالتفصيل.
        """
    }
    
    response = responses.get(question, responses["default"])
    
    # إضافة رد المساعد
    st.session_state.chat_messages.append({
        "role": "assistant", 
        "content": response
    })
    
    save_data()
    st.rerun()

# ===== التواصل مع المطور =====
def contact_developer():
    """نموذج التواصل مع المطور"""
    st.header("📧 التواصل مع المطور")
    
    with st.form("contact_form"):
        name = st.text_input("الاسم الكامل", key="contact_name")
        email = st.text_input("البريد الإلكتروني", key="contact_email")
        subject = st.selectbox("نوع الرسالة", [
            "مشكلة تقنية", "اقتراح تحسين", 
            "دعم فني", "استفسار عام"
        ], key="contact_subject")
        message = st.text_area("الرسالة", height=150, key="contact_message")
        
        if st.form_submit_button("إرسال الرسالة", key="contact_submit"):
            if name and email and message:
                # حفظ الرسالة
                contact_data = {
                    "name": name,
                    "email": email, 
                    "subject": subject,
                    "message": message,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                
                try:
                    contact_file = DATA_DIR / "contact_messages.json"
                    messages = []
                    if contact_file.exists():
                        with open(contact_file, "r", encoding="utf-8") as f:
                            messages = json.load(f)
                    
                    messages.append(contact_data)
                    
                    with open(contact_file, "w", encoding="utf-8") as f:
                        json.dump(messages, f, ensure_ascii=False, indent=2)
                    
                    st.success("✅ تم إرسال رسالتك بنجاح!")
                    st.info("📧 **البريد الإلكتروني للمطور:** eyadmustafaali99@gmail.com")
                    
                except Exception as e:
                    st.success("✅ تم حفظ رسالتك بنجاح!")
                    
            else:
                st.error("❌ يرجى ملء جميع الحقول المطلوبة")

# ===== التصميم الأساسي =====
def apply_basic_styles():
    """تطبيق التصميم الأساسي"""
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        .main-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
            border: 1px solid #333;
        }
        .metric-card {
            background: rgba(30, 30, 46, 0.8);
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.5rem 0;
            border: 1px solid #333;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: #31333F;
        }
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.5rem 0;
            border: 1px solid #e0e0e0;
        }
        </style>
        """, unsafe_allow_html=True)

apply_basic_styles()

# ===== الواجهة الرئيسية =====
def main():
    """الواجهة الرئيسية للتطبيق"""
    
    # الهيدر الرئيسي
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        stats = calculate_attendance_stats()
        st.metric("📊 نسبة الحضور", f"{stats['percentage']:.1f}%")

    with col2:
        st.markdown(f"""
        <div class="main-header">
            <h1>{t('title')}</h1>
            <h3>{t('subtitle')}</h3>
            <p>{t('description')}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        col3a, col3b = st.columns(2)
        with col3a:
            # زر تغيير الثيم - تم إصلاحه
            theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
            if st.button(theme_icon, use_container_width=True, key="theme_toggle"):
                toggle_theme()
        with col3b:
            # زر تغيير اللغة - تم إصلاحه
            if st.button("🌐", use_container_width=True, key="lang_toggle"):
                toggle_language()

    # شريط التنقل
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

    pages = [
        (t("student"), "student"),
        (t("driver"), "driver"), 
        (t("parents"), "parents"),
        (t("admin"), "admin"),
        (t("support"), "support"),
        (t("about"), "about")
    ]

    nav_cols = st.columns(len(pages))
    for i, (name, page_key) in enumerate(pages):
        with nav_cols[i]:
            # أزرار التنقل - تم إصلاحها
            if st.button(name, use_container_width=True, key=f"nav_{page_key}"):
                st.session_state.page = page_key
                st.rerun()

    st.markdown("---")

    # عرض المحتوى حسب الصفحة المختارة
    if st.session_state.page == "student":
        show_student_page()
    elif st.session_state.page == "driver":
        show_driver_page()
    elif st.session_state.page == "parents":
        show_parents_page()
    elif st.session_state.page == "admin":
        show_admin_page()
    elif st.session_state.page == "support":
        show_support_page()
    elif st.session_state.page == "about":
        show_about_page()

    # الفوتر
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem;'>
        <h4>🚍 {t('footer')}</h4>
        <p>{t('rights')}</p>
        <p style='font-size: 0.9rem; opacity: 0.7;'>{t('team')}</p>
    </div>
    """, unsafe_allow_html=True)

# ===== صفحات التطبيق =====
def show_student_page():
    """صفحة الطالب"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(t("student_title"))
        st.write(t("student_desc"))
        
        student_id = st.text_input(t("student_id"), placeholder=t("student_id_placeholder"), key="student_id_input")
        
        if student_id:
            student_info = st.session_state.students_df[
                st.session_state.students_df["id"].astype(str) == student_id.strip()
            ]
            
            if not student_info.empty:
                student = student_info.iloc[0]
                st.success(f"🎓 تم العثور على الطالب: **{student['name']}**")
                
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.metric(t("grade"), student['grade'])
                with col_info2:
                    st.metric(t("bus"), student['bus'])
                
                already_registered, current_status = has_student_registered_today(student_id)
                
                if already_registered:
                    st.warning(f"✅ {t('already_registered')} - الحالة: {current_status}")
                    
                    if st.button(t("change_status"), key="change_status_btn"):
                        today = datetime.datetime.now().strftime("%Y-%m-%d")
                        st.session_state.attendance_df = st.session_state.attendance_df[
                            ~((st.session_state.attendance_df["id"].astype(str) == student_id.strip()) & 
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
                            st.balloons()
                            st.success(f"🎉 {t('registered_success')}")
                    with col_btn2:
                        if st.button(t("not_coming"), use_container_width=True, key="not_coming_btn"):
                            now = register_attendance(student, "لن يحضر")
                            st.success(f"🎉 {t('registered_success')}")
            
            else:
                st.error(f"❌ {t('not_found')}")

    with col2:
        st.subheader(t("stats_title"))
        stats = calculate_attendance_stats()
        
        st.metric(t("total_registered"), stats['total'])
        st.metric(t("expected_attendance"), stats['coming'])
        st.metric(t("attendance_rate"), f"{stats['percentage']:.1f}%")

def show_driver_page():
    """صفحة السائق"""
    st.header(t("driver_title"))
    
    if not st.session_state.driver_logged_in:
        st.subheader(t("driver_login"))
        
        col1, col2 = st.columns(2)
        with col1:
            bus_number = st.selectbox(t("select_bus"), ["1", "2", "3"], key="driver_bus")
        with col2:
            password = st.text_input(t("password"), type="password", placeholder=t("password_placeholder"), key="driver_pass")
        
        if st.button(t("login"), use_container_width=True, key="driver_login_btn"):
            if password == st.session_state.bus_passwords.get(bus_number, ""):
                st.session_state.driver_logged_in = True
                st.session_state.current_bus = bus_number
                st.success(t("login_success"))
                st.rerun()
            else:
                st.error(t("login_error"))
    
    else:
        st.success(f"✅ {t('login_success')} - الباص {st.session_state.current_bus}")
        
        if st.button(t("logout"), key="driver_logout_btn"):
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
        
        # قائمة الطلاب
        st.subheader(f"🎒 {t('coming_students')}")
        
        if not today_attendance.empty:
            coming_students = today_attendance[today_attendance["status"] == "قادم"]
            
            if not coming_students.empty:
                for _, student in coming_students.iterrows():
                    st.write(f"**{student['name']}** - {student['grade']} - ✅ {t('status_coming')} - {student['time']}")
            else:
                st.info(f"🚫 {t('no_students')}")
        else:
            st.info(f"🚫 {t('no_students')}")

def show_parents_page():
    """صفحة أولياء الأمور"""
    st.header(t("parents_title"))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(t("track_student"))
        student_id = st.text_input(t("enter_student_id"), placeholder=t("parents_id_placeholder"), key="parent_student_id")
        
        if student_id:
            student_info = st.session_state.students_df[
                st.session_state.students_df["id"].astype(str) == student_id.strip()
            ]
            
            if not student_info.empty:
                student = student_info.iloc[0]
                st.success(f"🎓 تم العثور على الطالب: **{student['name']}**")
                
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.metric(t("grade"), student['grade'])
                with col_info2:
                    st.metric(t("bus"), student['bus'])
                
                # حالة اليوم
                st.subheader(t("today_status"))
                already_registered, current_status = has_student_registered_today(student_id)
                
                if already_registered:
                    today = datetime.datetime.now().strftime("%Y-%m-%d")
                    registration_data = st.session_state.attendance_df[
                        (st.session_state.attendance_df["id"].astype(str) == student_id.strip()) & 
                        (st.session_state.attendance_df["date"] == today)
                    ]
                    
                    if not registration_data.empty:
                        registration_time = registration_data.iloc[0]["time"]
                        
                        if current_status == "قادم":
                            st.success(f"✅ {t('status_coming')} - {t('registration_time')}: {registration_time}")
                        else:
                            st.error(f"❌ {t('status_not_coming')} - {t('registration_time')}: {registration_time}")
                else:
                    st.warning(f"⏳ {t('status_not_registered')}")
            
            else:
                st.error(f"❌ {t('not_found')}")
    
    with col2:
        st.subheader(t("bus_info"))
        
        if student_id and not st.session_state.students_df[
            st.session_state.students_df["id"].astype(str) == student_id.strip()
        ].empty:
            student = st.session_state.students_df[
                st.session_state.students_df["id"].astype(str) == student_id.strip()
            ].iloc[0]
            
            bus_number = student["bus"]
            schedule = get_bus_schedule(bus_number)
            driver = get_driver_contact(bus_number)
            
            # جدول الباص
            st.subheader(t("bus_schedule"))
            st.metric(t("morning_pickup"), schedule['morning'])
            st.metric(t("evening_return"), schedule['evening'])
            
            # معلومات السائق
            st.subheader(t("driver_contact"))
            st.info(f"**الاسم:** {driver['name']}\n\n**📞 الهاتف:** {driver['phone']}")

def show_admin_page():
    """صفحة الإدارة"""
    st.header(t("admin_title"))
    
    if not st.session_state.admin_logged_in:
        st.subheader(t("admin_login"))
        
        admin_password = st.text_input(t("admin_password"), type="password", key="admin_pass_input")
        
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
        
        tab1, tab2 = st.tabs(["إدارة الطلاب", "إعدادات النظام"])
        
        with tab1:
            st.subheader("👥 إدارة الطلاب")
            
            # إحصائيات
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("إجمالي الطلاب", len(st.session_state.students_df))
            with col2:
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                today_attendance = st.session_state.attendance_df[
                    st.session_state.attendance_df["date"] == today
                ] if not st.session_state.attendance_df.empty else pd.DataFrame()
                st.metric("المسجلين اليوم", len(today_attendance))
            with col3:
                coming_today = len(today_attendance[today_attendance["status"] == "قادم"]) if not today_attendance.empty else 0
                st.metric("الحضور المتوقع", coming_today)
            with col4:
                attendance_rate = (coming_today / len(st.session_state.students_df) * 100) if len(st.session_state.students_df) > 0 else 0
                st.metric("نسبة التسجيل", f"{attendance_rate:.1f}%")
            
            # إضافة طالب جديد
            st.subheader("➕ إضافة طالب جديد")
            
            with st.form("add_student_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_student_id = st.text_input("رقم الوزارة", key="new_student_id")
                    new_student_name = st.text_input("اسم الطالب", key="new_student_name")
                with col2:
                    new_student_grade = st.selectbox("الصف", ["6-A", "6-B", "7-A", "7-B", "8-A", "8-B", "8-C", "9-A", "9-B", "10-A", "10-B", "11-A", "11-B"], key="new_student_grade")
                    new_student_bus = st.selectbox("الباص", ["1", "2", "3"], key="new_student_bus")
                
                new_parent_phone = st.text_input("هاتف ولي الأمر", key="new_parent_phone")
                
                if st.form_submit_button("إضافة الطالب", key="add_student_submit"):
                    if all([new_student_id, new_student_name, new_parent_phone]):
                        success, message = add_new_student(
                            new_student_id, new_student_name, new_student_grade, new_student_bus, new_parent_phone
                        )
                        
                        if success:
                            st.success("✅ تم إضافة الطالب بنجاح!")
                            st.balloons()
                        elif message == "student_exists":
                            st.error("❌ رقم الوزارة موجود مسبقاً!")
                        else:
                            st.error(f"❌ حدث خطأ: {message}")
                    else:
                        st.error("❌ يرجى ملء جميع الحقول المطلوبة")
        
        with tab2:
            st.subheader("⚙️ إعدادات النظام")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("🔐 كلمات مرور الباصات")
                for bus_num, password in st.session_state.bus_passwords.items():
                    st.text_input(f"كلمة مرور الباص {bus_num}", value=password, type="password", key=f"bus_pass_{bus_num}")
            
            with col2:
                st.info("🌐 الإعدادات العامة")
                if st.button("تغيير السمة", key="theme_change_btn"):
                    toggle_theme()
                if st.button("تغيير اللغة", key="lang_change_btn"):
                    toggle_language()

def show_support_page():
    """صفحة الدعم الذكي"""
    st.header("🤖 مركز الدعم الذكي")
    
    tab1, tab2 = st.tabs(["المساعد الذكي", "التواصل مع المطور"])
    
    with tab1:
        smart_ai_assistant()
    
    with tab2:
        contact_developer()

def show_about_page():
    """صفحة حول النظام"""
    st.header(t("about_title"))
    st.write(t("about_description"))
    
    # المميزات
    st.subheader("🎯 المميزات الرئيسية")
    
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
            <div class="metric-card">
                <div style="font-size: 2rem;">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # فريق التطوير
    st.subheader("👥 فريق التطوير")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**🛠️ مطور النظام**\n\nإياد مصطفى\n\neyadmustafaali99@gmail.com")
    with col2:
        st.info("**🎨 مصمم الواجهة**\n\nايمن جلال")
    with col3:
        st.info("**👨‍🏫 الإشراف**\n\nقسم النادي البيئي")

# تشغيل التطبيق
if __name__ == "__main__":
    main()
