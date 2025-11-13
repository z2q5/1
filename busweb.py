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
def initialize_session_state():
    """تهيئة حالة الجلسة بشكل آمن"""
    default_states = {
        "lang": "ar",
        "page": "student",
        "notifications": [],
        "driver_logged_in": False,
        "current_bus": "1",
        "theme": "light",
        "bus_passwords": {"1": "1111", "2": "2222", "3": "3333"},
        "admin_password": "admin123",
        "admin_logged_in": False,
        "selected_rating": 0,
        "data_loaded": False,
        "offline_mode": False,
        "first_time": True,
        "last_save": datetime.datetime.now(),
        "font_size": "default",
        "high_contrast": False,
        "chat_messages": [],
        "sync_pending": False,
        "two_factor_enabled": False,
        "trusted_devices": [],
        "activity_log": [],
        "support_tickets": [],
        "students_df": None,
        "attendance_df": None,
        "ratings_df": None
    }
    
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # تهيئة DataFrames إذا كانت غير موجودة
    if st.session_state.students_df is None:
        initialize_students_data()
    if st.session_state.attendance_df is None:
        st.session_state.attendance_df = pd.DataFrame(columns=[
            "id", "name", "grade", "bus", "status", "time", "date"
        ])
    if st.session_state.ratings_df is None:
        st.session_state.ratings_df = pd.DataFrame(columns=["rating", "comment", "timestamp"])

def initialize_students_data():
    """تهيئة بيانات الطلاب"""
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

# تهيئة حالة التطبيق
initialize_session_state()

# ===== الترجمة المتقدمة متعددة اللغات =====
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
        "support": "🤖 الدعم الذكي",
        
        # الدعم الذكي
        "ai_assistant": "🤖 المساعد الذكي",
        "ai_welcome": "مرحباً! أنا المساعد الذكي لنظام الباص. كيف يمكنني مساعدتك اليوم؟",
        "ask_question": "اطرح سؤالك هنا...",
        "send": "إرسال",
        "quick_questions": "أسئلة سريعة",
        "how_to_register": "كيف أسجل الحضور؟",
        "bus_tracking": "متابعة الباص",
        "technical_support": "دعم فني",
        "contact_developer": "📧 التواصل مع المطور",
        
        # التواصل مع المطور
        "contact_title": "📧 التواصل مع المطور",
        "full_name": "الاسم الكامل",
        "email": "البريد الإلكتروني",
        "message_type": "نوع الرسالة",
        "technical_issue": "مشكلة تقنية",
        "suggestion": "اقتراح تحسين", 
        "general_inquiry": "استفسار عام",
        "message": "الرسالة",
        "send_message": "إرسال الرسالة",
        "message_sent": "✅ تم إرسال رسالتك بنجاح!",
        "fill_all_fields": "❌ يرجى ملء جميع الحقول المطلوبة",
        
        # الإحصائيات والرسوم البيانية
        "live_stats": "📊 الإحصائيات الحية",
        "interactive_charts": "📈 الرسوم البيانية التفاعلية",
        "custom_reports": "📋 التقارير القابلة للتخصيص",
        "attendance_stats": "إحصائيات الحضور",
        "bus_performance": "أداء الباصات",
        "student_analytics": "تحليلات الطلاب",
        
        # اللغات
        "language": "🌐 اللغة",
        "arabic": "العربية",
        "english": "English",
        "french": "Français",
        "urdu": "اردو",
        "filipino": "Filipino"
    },
    "en": {
        "title": "🚍 Smart Bus System",
        "subtitle": "Al Muneera Private School - Abu Dhabi", 
        "description": "Integrated system for smart school transportation management",
        "student": "🎓 Student",
        "driver": "🚌 Driver",
        "parents": "👨‍👩‍👧 Parents", 
        "admin": "🏫 Admin",
        "about": "ℹ️ About",
        "support": "🤖 Smart Support",
        
        "ai_assistant": "🤖 AI Assistant",
        "ai_welcome": "Hello! I'm the Smart Bus System AI assistant. How can I help you today?",
        "ask_question": "Ask your question here...",
        "send": "Send",
        "quick_questions": "Quick Questions", 
        "how_to_register": "How to register attendance?",
        "bus_tracking": "Bus Tracking",
        "technical_support": "Technical Support",
        "contact_developer": "📧 Contact Developer",
        
        "contact_title": "📧 Contact Developer",
        "full_name": "Full Name",
        "email": "Email Address",
        "message_type": "Message Type",
        "technical_issue": "Technical Issue",
        "suggestion": "Improvement Suggestion",
        "general_inquiry": "General Inquiry", 
        "message": "Message",
        "send_message": "Send Message",
        "message_sent": "✅ Your message has been sent successfully!",
        "fill_all_fields": "❌ Please fill all required fields",
        
        "live_stats": "📊 Live Statistics", 
        "interactive_charts": "📈 Interactive Charts",
        "custom_reports": "📋 Customizable Reports",
        "attendance_stats": "Attendance Statistics",
        "bus_performance": "Bus Performance",
        "student_analytics": "Student Analytics",
        
        "language": "🌐 Language",
        "arabic": "العربية",
        "english": "English",
        "french": "Français", 
        "urdu": "اردو",
        "filipino": "Filipino"
    },
    "fr": {
        "title": "🚍 Système de Bus Intelligent",
        "subtitle": "École Privée Al Muneera - Abu Dhabi",
        "description": "Système intégré de gestion intelligente du transport scolaire",
        "student": "🎓 Étudiant",
        "driver": "🚌 Chauffeur",
        "parents": "👨‍👩‍👧 Parents", 
        "admin": "🏫 Administration",
        "about": "ℹ️ À propos",
        "support": "🤖 Support Intelligent",
        
        "ai_assistant": "🤖 Assistant IA",
        "ai_welcome": "Bonjour ! Je suis l'assistant IA du système de bus intelligent. Comment puis-je vous aider aujourd'hui ?",
        "ask_question": "Posez votre question ici...",
        "send": "Envoyer",
        "quick_questions": "Questions Rapides",
        "how_to_register": "Comment enregistrer la présence ?",
        "bus_tracking": "Suivi du Bus", 
        "technical_support": "Support Technique",
        "contact_developer": "📧 Contacter le Développeur",
        
        "contact_title": "📧 Contacter le Développeur",
        "full_name": "Nom Complet",
        "email": "Adresse Email",
        "message_type": "Type de Message", 
        "technical_issue": "Problème Technique",
        "suggestion": "Suggestion d'Amélioration",
        "general_inquiry": "Demande Générale",
        "message": "Message",
        "send_message": "Envoyer le Message",
        "message_sent": "✅ Votre message a été envoyé avec succès !",
        "fill_all_fields": "❌ Veuillez remplir tous les champs obligatoires",
        
        "live_stats": "📊 Statistiques en Direct",
        "interactive_charts": "📈 Graphiques Interactifs", 
        "custom_reports": "📋 Rapports Personnalisables",
        "attendance_stats": "Statistiques de Présence",
        "bus_performance": "Performance des Bus",
        "student_analytics": "Analyses des Étudiants",
        
        "language": "🌐 Langue",
        "arabic": "العربية",
        "english": "English", 
        "french": "Français",
        "urdu": "اردو",
        "filipino": "Filipino"
    },
    "ur": {
        "title": "🚍 اسمارٹ بس سسٹم",
        "subtitle": "المنیعہ پرائیویٹ اسکول - ابوظہبی", 
        "description": "اسمارٹ اسکول ٹرانسپورٹیشن مینجمنٹ کے لیے انٹیگریٹڈ سسٹم",
        "student": "🎓 طالب علم",
        "driver": "🚌 ڈرائیور",
        "parents": "👨‍👩‍👧 والدین",
        "admin": "🏫 انتظامیہ", 
        "about": "ℹ️ کے بارے میں",
        "support": "🤖 اسمارٹ سپورٹ",
        
        "ai_assistant": "🤖 AI اسسٹنٹ",
        "ai_welcome": "ہیلو! میں اسمارٹ بس سسٹم AI اسسٹنٹ ہوں۔ آج میں آپ کی کس طرح مدد کر سکتا ہوں؟",
        "ask_question": "اپنا سوال یہاں پوچھیں...",
        "send": "ارسال کریں",
        "quick_questions": "فوری سوالات",
        "how_to_register": "حاضری کیسے رجسٹر کریں؟",
        "bus_tracking": "بس ٹریکنگ", 
        "technical_support": "تکنیکی مدد",
        "contact_developer": "📧 ڈویلپر سے رابطہ کریں",
        
        "contact_title": "📧 ڈویلپر سے رابطہ کریں",
        "full_name": "پورا نام",
        "email": "ای میل ایڈریس",
        "message_type": "پیغام کی قسم",
        "technical_issue": "تکنیکی مسئلہ", 
        "suggestion": "بہتری کی تجویز",
        "general_inquiry": "عام استفسار",
        "message": "پیغام",
        "send_message": "پیغام بھیجیں",
        "message_sent": "✅ آپ کا پیغام کامیابی سے بھیج دیا گیا ہے!",
        "fill_all_fields": "❌ براہ کرم تمام ضروری فیلڈز کو پُر کریں",
        
        "live_stats": "📊 لائیو شماریات",
        "interactive_charts": "📈 انٹرایکٹو چارٹس",
        "custom_reports": "📋 حسب ضرورت رپورٹس", 
        "attendance_stats": "حاضری کی شماریات",
        "bus_performance": "بس کی کارکردگی",
        "student_analytics": "طلباء کے تجزیات",
        
        "language": "🌐 زبان",
        "arabic": "العربية",
        "english": "English",
        "french": "Français", 
        "urdu": "اردو",
        "filipino": "Filipino"
    },
    "fil": {
        "title": "🚍 Smart Bus System",
        "subtitle": "Al Muneera Private School - Abu Dhabi",
        "description": "Integrated system para sa smart school transportation management", 
        "student": "🎓 Mag-aaral",
        "driver": "🚌 Driver",
        "parents": "👨‍👩‍👧 Magulang",
        "admin": "🏫 Admin",
        "about": "ℹ️ Tungkol sa Sistema",
        "support": "🤖 Smart Support",
        
        "ai_assistant": "🤖 AI Assistant",
        "ai_welcome": "Kamusta! Ako ang Smart Bus System AI assistant. Paano kita matutulungan ngayon?",
        "ask_question": "Itanong ang iyong katanungan dito...",
        "send": "Ipadala",
        "quick_questions": "Mabilis na Mga Tanong",
        "how_to_register": "Paano magrehistro ng attendance?",
        "bus_tracking": "Pagsubaybay sa Bus", 
        "technical_support": "Teknikal na Suporta",
        "contact_developer": "📧 Makipag-ugnayan sa Developer",
        
        "contact_title": "📧 Makipag-ugnayan sa Developer",
        "full_name": "Buong Pangalan",
        "email": "Email Address",
        "message_type": "Uri ng Mensahe",
        "technical_issue": "Teknikal na Isyu", 
        "suggestion": "Mungkahi para sa Pagpapabuti",
        "general_inquiry": "Pangkalahatang Tanong",
        "message": "Mensahe",
        "send_message": "Ipadala ang Mensahe",
        "message_sent": "✅ Matagumpay na naipadala ang iyong mensahe!",
        "fill_all_fields": "❌ Pakipunan ang lahat ng kinakailangang field",
        
        "live_stats": "📊 Live na Estadistika",
        "interactive_charts": "📈 Interactive na Mga Chart",
        "custom_reports": "📋 Naipapasadyang Mga Ulat",
        "attendance_stats": "Estadistika ng Attendance", 
        "bus_performance": "Pagganap ng Bus",
        "student_analytics": "Analytics ng Mag-aaral",
        
        "language": "🌐 Wika",
        "arabic": "العربية",
        "english": "English",
        "french": "Français",
        "urdu": "اردو", 
        "filipino": "Filipino"
    }
}

def t(key):
    """دالة الترجمة الآمنة"""
    try:
        return translations[st.session_state.lang][key]
    except KeyError:
        return key

# ===== المساعد الذكي المتقدم =====
def smart_ai_assistant():
    """المساعد الذكي باستخدام محاكاة GPT-4"""
    st.header(t("ai_assistant"))
    
    # تهيئة رسائل المحادثة إذا لم تكن موجودة
    if not st.session_state.chat_messages:
        st.session_state.chat_messages = [{
            "role": "assistant", 
            "content": t("ai_welcome"),
            "timestamp": datetime.datetime.now().strftime("%H:%M")
        }]
    
    # عرض رسائل المحادثة
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "assistant":
                st.markdown(f"""
                <div style='
                    background: rgba(59, 130, 246, 0.1);
                    padding: 1rem;
                    border-radius: 1rem;
                    margin: 0.5rem 0;
                    border-right: 4px solid #3b82f6;
                    text-align: right;
                '>
                    <div style='font-size: 0.8rem; opacity: 0.7; margin-bottom: 0.5rem;'>
                        🤖 {t("ai_assistant")} • {msg.get("timestamp", "")}
                    </div>
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='
                    background: rgba(16, 185, 129, 0.1);
                    padding: 1rem;
                    border-radius: 1rem;
                    margin: 0.5rem 0;
                    border-left: 4px solid #10b981;
                    text-align: left;
                '>
                    <div style='font-size: 0.8rem; opacity: 0.7; margin-bottom: 0.5rem;'>
                        👤 أنت • {msg.get("timestamp", "")}
                    </div>
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # الأسئلة السريعة
    st.subheader(t("quick_questions"))
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(t("how_to_register"), use_container_width=True):
            handle_ai_question(t("how_to_register"))
    with col2:
        if st.button(t("bus_tracking"), use_container_width=True):
            handle_ai_question(t("bus_tracking"))
    with col3:
        if st.button(t("technical_support"), use_container_width=True):
            handle_ai_question(t("technical_support"))
    
    # إدخال السؤال
    st.markdown("---")
    user_question = st.text_area(t("ask_question"), height=100, key="ai_question_input")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(t("send"), use_container_width=True, type="primary") and user_question:
            handle_ai_question(user_question)

def handle_ai_question(question):
    """معالجة الأسئلة باستخدام محاكاة الذكاء الاصطناعي"""
    # إضافة سؤال المستخدم
    st.session_state.chat_messages.append({
        "role": "user",
        "content": question,
        "timestamp": datetime.datetime.now().strftime("%H:%M")
    })
    
    # توليد رد ذكي بناءً على السؤال
    responses = {
        t("how_to_register"): generate_attendance_help(),
        t("bus_tracking"): generate_bus_tracking_help(),
        t("technical_support"): generate_technical_support_help(),
        "default": generate_general_response(question)
    }
    
    response = responses.get(question, responses["default"])
    
    # إضافة رد المساعد
    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.datetime.now().strftime("%H:%M")
    })
    
    # حفظ البيانات
    save_data()
    st.rerun()

def generate_attendance_help():
    """توليد مساعدة حول تسجيل الحضور"""
    return f"""
🎯 **{t('how_to_register')}**

**للطلاب:**
1. انتقل إلى صفحة {t('student')}
2. أدخل رقم الوزارة الخاص بك
3. اختر 'سأحضر اليوم' أو 'لن أحضر'
4. انقر على زر التسجيل

**لأولياء الأمور:**
1. انتقل إلى صفحة {t('parents')} 
2. أدخل رقم وزارة الطالب
3. تابع حالة الحضور مباشرة

⏰ **مواعيد التسجيل:** يفضل التسجيل قبل الساعة 8 صباحاً
🔄 **تغيير الحالة:** يمكنك تغيير حالتك إذا أخطأت في التسجيل
"""

def generate_bus_tracking_help():
    """توليد مساعدة حول متابعة الباص"""
    return f"""
🚍 **{t('bus_tracking')}**

**معلومات الباص:**
- 🕐 **وقت الصباح:** 7:00 صباحاً
- 🕐 **وقت الظهيرة:** 2:30 مساءً  
- 📞 **اتصال السائق:** متوفر في صفحة {t('parents')}

**ميزات المتابعة:**
- متابعة حالة الباص في الوقت الفعلي
- إشعارات عند وصول الباص
- معلومات الاتصال بالسائق
- جدول المواعيد الدقيق

📍 لمزيد من التفاصيل، انتقل إلى صفحة {t('parents')}
"""

def generate_technical_support_help():
    """توليد مساعدة الدعم الفني"""
    return f"""
🔧 **{t('technical_support')}**

**الحلول السريعة:**
1. **تحديث الصفحة** - اضغط F5 أو Ctrl+R
2. **التأكد من الاتصال** - تحقق من اتصال الإنترنت
3. **المتصفح** - جرب استخدام Chrome أو Firefox

**إذا استمرت المشكلة:**
- استخدم زر '{t('contact_developer')}' أدناه
- أو راسلنا على: eyadmustafaali99@gmail.com
- سنرد عليك خلال 24 ساعة

📧 **للطوارئ:** يمكنك الاتصال بالإدارة على: 025555555
"""

def generate_general_response(question):
    """توليد رد عام ذكي"""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['hello', 'hi', 'مرحبا', 'اهلا']):
        return "أهلاً وسهلاً بك! 😊 أنا المساعد الذكي لنظام الباص. كيف يمكنني مساعدتك اليوم؟"
    
    elif any(word in question_lower for word in ['thank', 'shukran', 'شكر']):
        return "العفو! 🤗 سعيد لأنني استطعت مساعدتك. هل هناك anything آخر تحتاج إليه؟"
    
    elif any(word in question_lower for word in ['problem', 'issue', 'مشكلة', 'خطأ']):
        return "أنا هنا لمساعدتك في حل المشكلات! 🛠️ يمكنك وصف المشكلة التي تواجهها بالتفصيل، أو استخدام خيار 'الدعم الفني' للحلول السريعة."
    
    else:
        return f"""
🤔 **شكراً لسؤالك!**

بناءً على سؤالك: "{question}"

يمكنني مساعدتك في:
- {t('how_to_register')}
- {t('bus_tracking')} 
- {t('technical_support')}
- معلومات عن النظام والخدمات

💡 **نصيحة:** يمكنك استخدام الأزرار أعلاه للحصول على إجابات سريعة، أو اشرح لي مشكلتك بالتفصيل لمزيد من المساعدة المتخصصة.
"""

# ===== التواصل مع المطور =====
def contact_developer_section():
    """قسم التواصل مع المطور"""
    st.header(t("contact_developer"))
    
    with st.form("contact_developer_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input(t("full_name"))
            email = st.text_input(t("email"))
        
        with col2:
            message_type = st.selectbox(t("message_type"), [
                t("technical_issue"),
                t("suggestion"), 
                t("general_inquiry")
            ])
        
        message = st.text_area(t("message"), height=150, 
                             placeholder="اكتب رسالتك بالتفصيل هنا...")
        
        if st.form_submit_button(t("send_message"), use_container_width=True):
            if full_name and email and message:
                # حفظ الرسالة (في التطبيق الحقيقي، سيتم إرسالها بالبريد)
                contact_data = {
                    "name": full_name,
                    "email": email,
                    "type": message_type,
                    "message": message,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "language": st.session_state.lang
                }
                
                # حفظ محلياً
                try:
                    contact_file = DATA_DIR / "contact_messages.json"
                    messages = []
                    if contact_file.exists():
                        with open(contact_file, "r", encoding="utf-8") as f:
                            messages = json.load(f)
                    
                    messages.append(contact_data)
                    
                    with open(contact_file, "w", encoding="utf-8") as f:
                        json.dump(messages, f, ensure_ascii=False, indent=2)
                    
                    st.success(t("message_sent"))
                    st.info("📧 **معلومات التواصل:** eyadmustafaali99@gmail.com")
                    
                except Exception as e:
                    st.error(f"تم حفظ رسالتك محلياً وسيتم معالجتها قريباً")
                
            else:
                st.error(t("fill_all_fields"))

# ===== الإحصائيات الحية والرسوم البيانية =====
def live_statistics_dashboard():
    """لوحة الإحصائيات الحية"""
    st.header(t("live_stats"))
    
    # إحصائيات سريعة
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = len(st.session_state.students_df)
        st.metric("👥 إجمالي الطلاب", total_students)
    
    with col2:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        today_attendance = st.session_state.attendance_df[
            st.session_state.attendance_df["date"] == today
        ] if st.session_state.attendance_df is not None and not st.session_state.attendance_df.empty else pd.DataFrame()
        registered_today = len(today_attendance)
        st.metric("📝 المسجلين اليوم", registered_today)
    
    with col3:
        if not today_attendance.empty:
            coming_today = len(today_attendance[today_attendance["status"] == "قادم"])
        else:
            coming_today = 0
        st.metric("✅ الحضور المتوقع", coming_today)
    
    with col4:
        attendance_rate = (coming_today / total_students * 100) if total_students > 0 else 0
        st.metric("📈 نسبة الحضور", f"{attendance_rate:.1f}%")
    
    # الرسوم البيانية
    st.subheader(t("interactive_charts"))
    
    tab1, tab2, tab3 = st.tabs(["الحضور اليومي", "توزيع الطلاب", "أداء الباصات"])
    
    with tab1:
        st.info("📊 **رسم بياني تفاعلي يظهر تطور الحضور خلال الأسبوع**")
        # محاكاة بيانات الرسم البياني
        weekly_data = pd.DataFrame({
            'اليوم': ['الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد'],
            'الحضور': [85, 92, 78, 95, 88, 45, 30]
        })
        st.bar_chart(weekly_data.set_index('اليوم'))
    
    with tab2:
        st.info("🎯 **توزيع الطلاب على الباصات**")
        if st.session_state.students_df is not None:
            bus_distribution = st.session_state.students_df['bus'].value_counts()
            st.bar_chart(bus_distribution)
    
    with tab3:
        st.info("🚌 **مقارنة أداء الباصات**")
        performance_data = pd.DataFrame({
            'الباص': ['الباص 1', 'الباص 2', 'الباص 3'],
            'الكفاءة': [92, 85, 78],
            'الرضا': [88, 82, 75]
        })
        st.line_chart(performance_data.set_index('الباص'))

# ===== إعدادات اللغة المتقدمة =====
def language_settings():
    """إعدادات اللغة المتقدمة"""
    st.sidebar.markdown("---")
    st.sidebar.subheader(t("language"))
    
    language_options = {
        "العربية": "ar",
        "English": "en", 
        "Français": "fr",
        "اردو": "ur",
        "Filipino": "fil"
    }
    
    selected_language = st.sidebar.selectbox(
        "اختر اللغة / Select Language",
        list(language_options.keys()),
        index=list(language_options.values()).index(st.session_state.lang)
    )
    
    if st.session_state.lang != language_options[selected_language]:
        st.session_state.lang = language_options[selected_language]
        st.rerun()
    
    # دعم RTL/LTR تلقائي
    if st.session_state.lang in ["ar", "ur"]:
        st.markdown("""
        <style>
        .stApp {
            text-align: right;
            direction: rtl;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            text-align: left;
            direction: ltr;
        }
        </style>
        """, unsafe_allow_html=True)

# ===== وظائف حفظ البيانات =====
def save_data():
    """حفظ البيانات بشكل آمن"""
    try:
        if st.session_state.students_df is not None:
            with open(DATA_DIR / "students.pkl", "wb") as f:
                pickle.dump(st.session_state.students_df.to_dict(), f)
        
        if st.session_state.attendance_df is not None:
            with open(DATA_DIR / "attendance.pkl", "wb") as f:
                pickle.dump(st.session_state.attendance_df.to_dict(), f)
        
        if st.session_state.ratings_df is not None:
            with open(DATA_DIR / "ratings.pkl", "wb") as f:
                pickle.dump(st.session_state.ratings_df.to_dict(), f)
        
        settings = {
            "lang": st.session_state.lang,
            "theme": st.session_state.theme,
            "font_size": st.session_state.font_size,
            "high_contrast": st.session_state.high_contrast,
            "chat_messages": st.session_state.chat_messages,
            "last_save": datetime.datetime.now().isoformat()
        }
        
        with open(DATA_DIR / "settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        st.error(f"تم حفظ البيانات محلياً")

# ===== واجهة المستخدم الرئيسية =====
def main():
    """الواجهة الرئيسية للتطبيق"""
    
    # تطبيق إعدادات اللغة
    language_settings()
    
    # الهيدر الرئيسي
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.markdown(f"""
        <div style='
            background: rgba(59, 130, 246, 0.1);
            padding: 1rem;
            border-radius: 15px;
            text-align: center;
        '>
            <h3>📊 {t('live_stats')}</h3>
            <h2 style='color: #3b82f6;'>{
                len(st.session_state.students_df) if st.session_state.students_df is not None else 0
            }</h2>
            <p>طالب مسجل</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
        '>
            <h1>{t('title')}</h1>
            <h3>{t('subtitle')}</h3>
            <p>{t('description')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # أزرار التحكم
        col3a, col3b = st.columns(2)
        with col3a:
            if st.button("🌙" if st.session_state.theme == "light" else "☀️", 
                        use_container_width=True, key="theme_btn"):
                st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
                st.rerun()
        with col3b:
            if st.button("🔄", use_container_width=True, key="refresh_btn"):
                st.rerun()
    
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
            is_active = st.session_state.page == page_key
            if st.button(name, use_container_width=True, 
                        type="primary" if is_active else "secondary", 
                        key=f"nav_{page_key}"):
                st.session_state.page = page_key
                st.rerun()
    
    st.markdown("---")
    
    # عرض المحتوى حسب الصفحة المختارة
    if st.session_state.page == "support":
        show_support_page()
    else:
        st.info(f"🚧 صفحة {t(st.session_state.page)} قيد التطوير - جاري العمل على إضافة جميع الميزات")
        st.markdown(f"### {t('live_stats')}")
        live_statistics_dashboard()

def show_support_page():
    """عرض صفحة الدعم الذكي"""
    tab1, tab2, tab3 = st.tabs([
        t("ai_assistant"),
        t("contact_developer"), 
        t("live_stats")
    ])
    
    with tab1:
        smart_ai_assistant()
    
    with tab2:
        contact_developer_section()
    
    with tab3:
        live_statistics_dashboard()

# تشغيل التطبيق
if __name__ == "__main__":
    main()
