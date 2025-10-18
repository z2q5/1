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
        # ... (نفس الترجمات السابقة)
    },
    "en": {
        # ... (نفس الترجمات السابقة) 
    }
}

def t(key):
    """دالة الترجمة"""
    return translations[st.session_state.lang].get(key, key)

def switch_lang():
    """تبديل اللغة"""
    st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
    st.rerun()

# ===== تحميل البيانات - التصحيح هنا =====
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["id","name","grade","bus","status","time","date","expiry_time"])

def load_students():
    """تحميل بيانات الطلاب - تم التصحيح هنا"""
    try:
        if os.path.exists(STUDENTS_FILE):
            df = pd.read_csv(STUDENTS_FILE)
            # التأكد من أن الأعمدة موجودة
            required_columns = ["id", "name", "grade", "bus", "parent_phone"]
            for col in required_columns:
                if col not in df.columns:
                    st.error(f"العمود {col} مفقود في ملف الطلاب")
                    return create_default_students()
            return df
        else:
            # إذا الملف غير موجود، إنشاء بيانات افتراضية
            return create_default_students()
    except Exception as e:
        st.error(f"خطأ في تحميل بيانات الطلاب: {e}")
        return create_default_students()

def create_default_students():
    """إنشاء بيانات الطلاب الافتراضية"""
    default_students = [
        {"id": "1001", "name": "أحمد محمد", "grade": "10-A", "bus": "1", "parent_phone": "0501234567"},
        {"id": "1002", "name": "فاطمة علي", "grade": "9-B", "bus": "2", "parent_phone": "0507654321"},
        {"id": "1003", "name": "خالد إبراهيم", "grade": "8-C", "bus": "3", "parent_phone": "0505555555"},
        {"id": "1004", "name": "سارة عبدالله", "grade": "10-B", "bus": "1", "parent_phone": "0504444444"},
        {"id": "1005", "name": "محمد حسن", "grade": "7-A", "bus": "2", "parent_phone": "0503333333"},
        {"id": "1006", "name": "ريم أحمد", "grade": "11-A", "bus": "3", "parent_phone": "0506666666"},
        {"id": "1007", "name": "يوسف خالد", "grade": "6-B", "bus": "1", "parent_phone": "0507777777"},
        {"id": "1008", "name": "نورة سعيد", "grade": "9-A", "bus": "2", "parent_phone": "0508888888"},
    ]
    df = pd.DataFrame(default_students)
    # حفظ البيانات الافتراضية
    df.to_csv(STUDENTS_FILE, index=False)
    return df

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

# ===== تهيئة البيانات - التصحيح هنا =====
if 'students_df' not in st.session_state:
    st.session_state.students_df = load_students()

if 'df' not in st.session_state:
    st.session_state.df = load_data()

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
    if st.session_state.df.empty or "date" not in st.session_state.df.columns:
        return {"total": 0, "coming": 0, "not_coming": 0, "percentage": 0}
    
    today_data = st.session_state.df[st.session_state.df["date"] == today]
    
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
    
    if st.session_state.df.empty or "date" not in st.session_state.df.columns:
        return False, None, None
    
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

# ===== صفحة الطالب - التصحيح النهائي =====
if st.session_state.page == "student":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎓 " + t("student_attendance"))
        
        # عرض أكواد الطلاب المتاحة للمساعدة
        with st.expander("📋 أكواد الطلاب المتاحة للمساعدة"):
            st.write("**يمكنك استخدام أي من هذه الأرقام:**")
            st.code("1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008")
        
        search_id = st.text_input("🔍 " + t("enter_ministry_id"), placeholder="أدخل رقم الوزارة هنا...")
        
        if search_id:
            # التحقق من وجود بيانات الطلاب
            if st.session_state.students_df.empty:
                st.error("❌ لا توجد بيانات طلاب متاحة. جاري تحميل البيانات الافتراضية...")
                st.session_state.students_df = create_default_students()
                st.rerun()
            
            # البحث عن الطالب
            student_info = st.session_state.students_df[st.session_state.students_df["id"] == search_id]
            
            if not student_info.empty:
                student = student_info.iloc[0]
                
                # عرض معلومات الطالب
                st.markdown(f"""
                <div class='student-card'>
                    <h3>🎓 {t('welcome_student')} {student['name']}</h3>
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
                    **الوقت المتبقي:** {hours_remaining} {t('hours')} {minutes_remaining} {t('minutes')}
                    """)
                    
                    if st.button(t('change_status'), type="secondary", use_container_width=True):
                        # إعادة تعيين الحالة للسماح بالتسجيل الجديد
                        st.session_state.df = st.session_state.df[
                            ~((st.session_state.df["id"] == search_id) & 
                              (st.session_state.df["date"] == datetime.datetime.now().strftime("%Y-%m-%d")))
                        ]
                        save_data(st.session_state.df)
                        st.success("✅ تم إعادة تعيين حالتك، يمكنك التسجيل مرة أخرى")
                        time.sleep(2)
                        st.rerun()
                else:
                    # إذا لم يسجل بعد، نعرض خيارات التسجيل
                    coming_text = "✅ سأحضر اليوم" 
                    not_coming_text = "❌ لن أحضر اليوم"
                    if st.session_state.lang == "en":
                        coming_text = "✅ I will come today"
                        not_coming_text = "❌ I will not come today"
                    
                    status_choice = st.radio(
                        t("today_status"), 
                        [coming_text, not_coming_text],
                        key="status_radio"
                    )
                    
                    if st.button(t("confirm_status"), type="primary", use_container_width=True):
                        now = datetime.datetime.now()
                        status_text = "قادم" if "سأحضر" in status_choice or "come" in status_choice else "لن يأتي"
                        
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
                        status_message = "قادم" if status_text == "قادم" else "لن يأتي"
                        if st.session_state.lang == "en":
                            status_message = "Coming" if status_text == "قادم" else "Not Coming"
                            
                        st.success(f"""
                        🎉 **{t('registration_success')}**
                        
                        **{t('student_name')}:** {student['name']}
                        **{t('current_status')}:** {status_message}
                        **{t('status_valid_until')}:** {expiry_time.strftime('%H:%M')}
                        **{t('bus_number')}:** {student['bus']}
                        """)
                        
                        add_notification(f"طالب جديد سجل حضوره: {student['name']} - الباص {student['bus']}")
                        time.sleep(3)
                        st.rerun()
            else:
                st.error(f"❌ {t('student_not_found')}")
                st.info("""
                **جرب أحد هذه الأرقام:**
                - 1001 (أحمد محمد)
                - 1002 (فاطمة علي) 
                - 1003 (خالد إبراهيم)
                - 1004 (سارة عبدالله)
                - 1005 (محمد حسن)
                """)

    with col2:
        st.subheader("📊 " + t("today_stats"))
        stats = calculate_attendance_stats()
        
        st.metric(t("total_registered"), stats["total"])
        st.metric(t("expected_attendance"), stats["coming"])
        st.metric(t("attendance_rate"), f"{stats['percentage']:.1f}%")
        
        # عرض إشعار سريع
        if stats["total"] > 0:
            st.info(f"📝 حتى الآن: {stats['coming']} طالب مؤكد الحضور")

# ... (بقية الصفحات تبقى كما هي)

# ===== الشريط السفلي مع حقوق الملكية =====
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])

with footer_col1:
    st.markdown(f"""
    <div style='text-align: center; color: #666; font-size: 12px;'>
        © 2024 نظام الباص الذكي - {t('school_name')}. {t('all_rights_reserved')}<br>
        تم التطوير بواسطة: إياد مصطفى - تصميم: ايمن جلال - إشراف: قسم النادي البيئي
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    if st.session_state.notifications:
        with st.expander(f"🔔 الإشعارات ({len(st.session_state.notifications)})"):
            for notification in st.session_state.notifications[-5:]:
                st.write(f"{notification['time']}: {notification['message']}")

with footer_col3:
    if st.button("🔄 " + t("refresh")):
        st.rerun()
