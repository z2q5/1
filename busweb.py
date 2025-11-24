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

# ===== وظائف التحسين المضافة: التزامن والاتصال والتغذية الراجعة =====

def check_internet_connection(timeout=5):
    """التحقق من اتصال الإنترنت وتحديث حالة الوضع دون اتصال"""
    try:
        # محاولة الوصول إلى خادم موثوق به
        requests.get("https://www.google.com", timeout=timeout)
        if st.session_state.offline_mode:
            st.session_state.offline_mode = False
            #st.success("✅ تم استعادة الاتصال بالإنترنت.")
        return True
    except requests.exceptions.RequestException:
        if not st.session_state.offline_mode:
            st.session_state.offline_mode = True
            #st.warning("⚠️ تم الدخول في وضع عدم الاتصال (Offline Mode).")
        return False

def sync_data():
    """محاكاة وظيفة مزامنة البيانات مع الخادم المركزي"""
    # التحقق من الاتصال قبل محاولة التزامن
    if not check_internet_connection():
        st.session_state.sync_pending = True
        st.error(T["no_internet_sync_error"])
        return

    st.session_state.sync_pending = True
    with st.spinner(T["syncing_data"]):
        try:
            # === منطقة محاكاة التزامن (يجب استبدالها بكود API حقيقي) ===
            time.sleep(2) # محاكاة تأخير الشبكة

            # التأكد من حفظ البيانات محلياً قبل التزامن
            save_data(local_only=True)
            
            # محاكاة النجاح في الإرسال
            st.session_state.sync_pending = False
            st.session_state.last_save = datetime.datetime.now()
            st.success(T["sync_success"])
            # ==========================================================
            
        except Exception as e:
            st.session_state.sync_pending = True
            st.error(f"{T['sync_failed']}: {e}")

# ===== وظائف حفظ البيانات (تم تحسينها بالتغذية الراجعة) =====
def save_data(local_only=False):
    """حفظ جميع البيانات في الملفات مع مؤشر تحميل"""
    # تجنب عرض المؤشر عند الحفظ الداخلي للتزامن
    if not local_only:
        context_manager = st.spinner(T["saving_data"])
    else:
        # إذا كان الحفظ داخلياً لعملية أخرى، استخدم 'with' بدون 'st.spinner'
        class DummyContext:
            def __enter__(self): return self
            def __exit__(self, exc_type, exc_val, exc_tb): return False
        context_manager = DummyContext()

    with context_manager:
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
            }
            with open(DATA_DIR / "settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False)
            
            if not local_only:
                st.session_state.last_save = datetime.datetime.now()
                st.success(T["save_success"])
            
        except Exception as e:
            st.error(f"{T['save_error']}: {e}")

def load_data():
    """تحميل البيانات المحفوظة مع مؤشر تحميل"""
    with st.spinner(T["loading_data"]):
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

            # التحقق من نوع البيانات وضبطها (مهم لعمود التاريخ والوقت)
            if 'attendance_df' in st.session_state and not st.session_state.attendance_df.empty:
                # التحويل إلى datetime
                for col in ['date', 'time']:
                    if col in st.session_state.attendance_df.columns:
                        try:
                            # استخدام errors='coerce' لوضع NaT للقيم التي لا يمكن تحويلها
                            st.session_state.attendance_df[col] = pd.to_datetime(
                                st.session_state.attendance_df[col], errors='coerce'
                            )
                        except Exception:
                            pass
            
            st.success(T["load_success"])
            
        except Exception as e:
            st.error(f"{T['load_error']}: {e}")

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
        "contact_developer": "📧 التواصل مع المطور",
        "developer_email": "البريد الإلكتروني: eyadmustafaali99@gmail.com",
        "contact_form": "📝 نموذج التواصل",
        
        # رسائل النظام
        "not_found": "لم يتم العثور على الطالب",
        "error": "حدث خطأ في النظام",
        "reset_success": "تم إعادة تعيين حالتك",
        "login_success": "تم الدخول بنجاح",
        "login_error": "كلمة مرور غير صحيحة",
        "data_reset_success": "تم إعادة تعيين البيانات",
        "backup_success": "تم إنشاء نسخة احتياطية",
        "password_updated": "تم تحديث كلمة المرور",
        
        # رسائل التغذية الراجعة والوضع دون اتصال
        "saving_data": "💾 جارٍ حفظ البيانات محلياً...",
        "loading_data": "⏳ جارٍ تحميل البيانات المحفوظة...",
        "save_success": "✅ تم حفظ البيانات بنجاح.",
        "load_success": "✅ تم تحميل البيانات بنجاح.",
        "save_error": "❌ خطأ في حفظ البيانات",
        "load_error": "❌ خطأ في تحميل البيانات",
        "syncing_data": "🔄 جارٍ مزامنة البيانات مع الخادم...",
        "sync_success": "🎉 تم مزامنة البيانات بنجاح!",
        "sync_failed": "❌ فشل التزامن",
        "offline_warning": "⚠️ التطبيق في وضع عدم الاتصال. سيتم التزامن عند توفر الإنترنت.",
        "no_internet_sync_error": "❌ لا يوجد اتصال بالإنترنت. فشل التزامن.",
        "sync_pending": "⏳ بيانات غير متزامنة",
        
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
        
        # التواصل مع المطور
        "contact_title": "📧 التواصل مع المطور",
        "contact_name": "👤 الاسم الكامل",
        "contact_email": "📧 البريد الإلكتروني",
        "contact_subject": "📋 نوع الرسالة",
        "contact_message": "💬 الرسالة",
        "contact_success": "✅ تم إرسال رسالتك بنجاح!",
        
        # المساعد الذكي
        "ai_assistant": "🤖 المساعد الذكي",
        "ai_welcome": "مرحباً! أنا المساعد الذكي لنظام الباص. كيف يمكنني مساعدتك؟",
        "ai_questions": "💬 أسئلة سريعة",
        "ai_placeholder": "💭 اكتب سؤالك هنا...",
        "ai_send": "🚀 إرسال"
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
        "current_status": "
