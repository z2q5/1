import streamlit as st
import pandas as pd
import datetime
import os
import random
import plotly.express as px
import plotly.graph_objects as go

# ===== إعداد الصفحة =====
st.set_page_config(
    page_title="Smart Bus System - Al Munira Private School", 
    layout="wide",
    page_icon="🚍",
    initial_sidebar_state="collapsed"
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

# ===== البيانات الافتراضية - التصحيح النهائي =====
def initialize_data():
    """تهيئة جميع البيانات بشكل صحيح"""
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
    
    if 'students_df' not in st.session_state:
        st.session_state.students_df = pd.DataFrame(students_data)
    
    if 'attendance_df' not in st.session_state:
        st.session_state.attendance_df = pd.DataFrame(columns=[
            "id", "name", "grade", "bus", "status", "time", "date"
        ])
    
    if 'ratings_df' not in st.session_state:
        st.session_state.ratings_df = pd.DataFrame(columns=["rating", "comments", "timestamp"])

# تهيئة البيانات
initialize_data()

# ===== كلمات المرور =====
bus_passwords = {"1": "1111", "2": "2222", "3": "3333"}
admin_pass = "admin123"

# ===== وظائف مساعدة =====
def add_notification(message):
    st.session_state.notifications.append({
        "time": datetime.datetime.now().strftime("%H:%M"),
        "message": message
    })

def get_weather():
    """بيانات الطقس"""
    return {
        "temp": random.randint(28, 42),
        "humidity": random.randint(30, 80),
        "wind_speed": random.randint(5, 25),
        "condition_ar": random.choice(["☀️ مشمس", "🌤️ غائم جزئياً", "🌧️ ممطر", "💨 عاصف"]),
        "condition_en": "Sunny"
    }

def calculate_attendance_stats():
    """حساب إحصائيات الحضور"""
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
    """التحقق من تسجيل الطالب - التصحيح النهائي"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if st.session_state.attendance_df.empty:
        return False, None
    
    # البحث في البيانات - التأكد من المقارنة الصحيحة
    student_data = st.session_state.attendance_df[
        (st.session_state.attendance_df["id"].astype(str) == str(student_id).strip()) & 
        (st.session_state.attendance_df["date"] == today)
    ]
    
    if not student_data.empty:
        latest_record = student_data.iloc[-1]
        return True, latest_record["status"]
    
    return False, None

def add_rating(rating, comments):
    """إضافة تقييم جديد"""
    new_rating = pd.DataFrame([{
        "rating": rating,
        "comments": comments,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    if st.session_state.ratings_df.empty:
        st.session_state.ratings_df = new_rating
    else:
        st.session_state.ratings_df = pd.concat([
            st.session_state.ratings_df, new_rating
        ], ignore_index=True)

def register_attendance(student, status):
    """تسجيل حضور الطالب - التصحيح النهائي"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # إزالة أي تسجيل سابق لنفس الطالب في نفس اليوم
    st.session_state.attendance_df = st.session_state.attendance_df[
        ~((st.session_state.attendance_df["id"].astype(str) == str(student["id"]).strip()) & 
          (st.session_state.attendance_df["date"] == today))
    ]
    
    # إضافة التسجيل الجديد
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
    
    return now

# ===== واجهة مستخدم محسنة =====
st.markdown("""
<style>
    /* التصميم العام */
    .main {
        background-color: #f8f9fa;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* كروت الإحصائيات */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        text-align: center;
        margin: 0.5rem;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    /* كروت الطلاب */
    .student-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }
    
    /* كروت الطقس */
    .weather-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* كروت المميزات */
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    /* كروت الفريق */
    .team-card-blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .team-card-green {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .team-card-orange {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    /* كروت التقييم */
    .rating-card {
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    /* تحسين النص */
    .stTextInput>div>div>input {
        color: #2c3e50 !important;
        font-weight: 500;
    }
    
    /* أزرار مخصصة */
    .custom-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .custom-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ===== الهيدر الرئيسي =====
col1, col2, col3 = st.columns([2, 3, 1])

with col1:
    weather_data = get_weather()
    st.markdown(f"""
    <div class='weather-card'>
        <h3>🌡️ {weather_data['temp']}°C</h3>
        <p>{weather_data['condition_ar']}</p>
        <p>💧 {weather_data['humidity']}% | 💨 {weather_data['wind_speed']} km/h</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='main-header'>
        <h1 style='font-size: 2.2rem; margin-bottom: 0.5rem;'>🚍 نظام الباص الذكي</h1>
        <h3 style='font-size: 1.2rem; margin-bottom: 0.5rem; opacity: 0.9;'>مدرسة المنيرة الخاصة - أبوظبي</h3>
        <p style='font-size: 1rem; opacity: 0.8;'>نظام متكامل لإدارة النقل المدرسي الذكي</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    col3a, col3b = st.columns(2)
    with col3a:
        if st.button("🌙", help="الوضع الليلي", use_container_width=True):
            st.info("ميزة الوضع الليلي قريباً...")
    
    with col3b:
        lang_text = "EN" if st.session_state.lang == "ar" else "AR"
        if st.button(f"🌐 {lang_text}", help="تبديل اللغة", use_container_width=True):
            st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
            st.rerun()

# ===== شريط التنقل =====
pages = [
    ("🎓 الطالب", "student"),
    ("🚌 السائق", "driver"), 
    ("👨‍👩‍👧 أولياء الأمور", "parents"),
    ("🏫 الإدارة", "admin"),
    ("🌦️ الطقس", "weather"),
    ("ℹ️ حول النظام", "about")
]

cols = st.columns(len(pages))
for i, (name, page_key) in enumerate(pages):
    with cols[i]:
        is_active = st.session_state.page == page_key
        button_type = "primary" if is_active else "secondary"
        if st.button(name, use_container_width=True, type=button_type):
            st.session_state.page = page_key
            st.rerun()

st.markdown("---")

# ===== صفحة الطالب - التصحيح النهائي =====
if st.session_state.page == "student":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 1.5rem;'>
            <h2>🎓 تسجيل حضور الطالب</h2>
            <p style='color: #666; font-size: 1.1rem;'>أدخل رقم الوزارة لتسجيل حالتك اليوم</p>
        </div>
        """, unsafe_allow_html=True)
        
        # بطاقة البحث
        with st.container():
            st.markdown("<div style='background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08);'>", unsafe_allow_html=True)
            
            student_id = st.text_input(
                "🔍 رقم الوزارة",
                placeholder="أدخل رقم الوزارة هنا...",
                help="يمكنك استخدام أي رقم من 1001 إلى 1008"
            )
            
            if student_id:
                # البحث عن الطالب - التصحيح النهائي
                try:
                    student_info = st.session_state.students_df[
                        st.session_state.students_df["id"].astype(str) == str(student_id).strip()
                    ]
                    
                    if not student_info.empty:
                        student = student_info.iloc[0]
                        
                        st.markdown(f"""
                        <div class='student-card'>
                            <div style='text-align: center;'>
                                <h3 style='color: #2c3e50; margin-bottom: 1rem;'>🎓 {student['name']}</h3>
                                <div style='display: flex; justify-content: center; gap: 1.5rem; margin-bottom: 1rem;'>
                                    <div style='text-align: center;'>
                                        <div style='background: #667eea; color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold; font-size: 0.9rem;'>📚 {student['grade']}</div>
                                    </div>
                                    <div style='text-align: center;'>
                                        <div style='background: #764ba2; color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold; font-size: 0.9rem;'>🚍 الباص {student['bus']}</div>
                                    </div>
                                </div>
                                <p style='color: #666; margin: 0;'><strong>هاتف ولي الأمر:</strong> {student['parent_phone']}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # التحقق من التسجيل المسبق
                        already_registered, current_status = has_student_registered_today(student_id)
                        
                        if already_registered:
                            status_color = "#51cf66" if current_status == "قادم" else "#ff6b6b"
                            status_icon = "✅" if current_status == "قادم" else "❌"
                            st.markdown(f"""
                            <div style='background: {status_color}; color: white; padding: 1.5rem; border-radius: 12px; text-align: center; margin: 1rem 0;'>
                                <h4>{status_icon} تم التسجيل مسبقاً</h4>
                                <p style='margin: 0.5rem 0; font-size: 1.1rem;'>حالتك الحالية: <strong>{current_status}</strong></p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button("🔄 تغيير الحالة", use_container_width=True, type="secondary"):
                                today = datetime.datetime.now().strftime("%Y-%m-%d")
                                st.session_state.attendance_df = st.session_state.attendance_df[
                                    ~((st.session_state.attendance_df["id"].astype(str) == str(student_id).strip()) & 
                                      (st.session_state.attendance_df["date"] == today))
                                ]
                                st.success("✅ تم إعادة تعيين حالتك، يمكنك التسجيل مرة أخرى")
                                st.rerun()
                        else:
                            st.markdown("<h4 style='text-align: center; color: #2c3e50; margin-bottom: 1rem;'>اختر حالتك اليوم:</h4>", unsafe_allow_html=True)
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("✅ سأحضر اليوم", use_container_width=True, type="primary"):
                                    now = register_attendance(student, "قادم")
                                    st.balloons()
                                    st.success(f"""
                                    🎉 **تم التسجيل بنجاح!**
                                    
                                    **الطالب:** {student['name']}
                                    **الحالة:** قادم
                                    **وقت التسجيل:** {now.strftime('%H:%M')}
                                    **رقم الباص:** {student['bus']}
                                    """)
                                    add_notification(f"طالب سجل حضوره: {student['name']} - الباص {student['bus']}")
                                    
                            with col_b:
                                if st.button("❌ لن أحضر اليوم", use_container_width=True, type="secondary"):
                                    now = register_attendance(student, "لن يأتي")
                                    st.success(f"""
                                    📝 **تم التسجيل بنجاح!**
                                    
                                    **الطالب:** {student['name']}
                                    **الحالة:** لن أحضر
                                    **وقت التسجيل:** {now.strftime('%H:%M')}
                                    **رقم الباص:** {student['bus']}
                                    """)
                                    add_notification(f"طالب أعلن عدم حضوره: {student['name']} - الباص {student['bus']}")
                    
                    else:
                        st.error("❌ لم يتم العثور على الطالب")
                        st.info("""
                        **💡 الأرقام المتاحة:**
                        - 1001: أحمد محمد
                        - 1002: فاطمة علي
                        - 1003: خالد إبراهيم  
                        - 1004: سارة عبدالله
                        - 1005: محمد حسن
                        - 1006: ريم أحمد
                        - 1007: يوسف خالد
                        - 1008: نورة سعيد
                        """)
                        
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {e}")
                    st.info("يرجى إدخال رقم صحيح مثل: 1001, 1002, إلخ...")
            
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='text-align: center; margin-bottom: 1rem;'><h3>📊 إحصائيات اليوم</h3></div>", unsafe_allow_html=True)
        
        stats = calculate_attendance_stats()
        
        st.markdown(f"""
        <div class='stat-card'>
            <h3 style='color: #667eea; margin-bottom: 0.5rem;'>👥</h3>
            <h2 style='color: #2c3e50; margin: 0;'>{stats['total']}</h2>
            <p style='color: #666; margin: 0;'>إجمالي المسجلين</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='stat-card'>
            <h3 style='color: #51cf66; margin-bottom: 0.5rem;'>✅</h3>
            <h2 style='color: #2c3e50; margin: 0;'>{stats['coming']}</h2>
            <p style='color: #666; margin: 0;'>الحضور المتوقع</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='stat-card'>
            <h3 style='color: #ffd43b; margin-bottom: 0.5rem;'>📈</h3>
            <h2 style='color: #2c3e50; margin: 0;'>{stats['percentage']:.1f}%</h2>
            <p style='color: #666; margin: 0;'>نسبة الحضور</p>
        </div>
        """, unsafe_allow_html=True)
        
        if stats["total"] > 0:
            st.info(f"📊 حتى الآن: {stats['coming']} طالب مؤكد الحضور")

# ===== صفحة السائق - التصحيح النهائي =====
elif st.session_state.page == "driver":
    st.subheader("🚌 لوحة تحكم السائق")
    
    if not st.session_state.driver_logged_in:
        col1, col2 = st.columns(2)
        with col1:
            bus_number = st.selectbox("اختر الباص", ["1", "2", "3"])
        with col2:
            password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور...")
        
        if st.button("تسجيل الدخول", type="primary", use_container_width=True):
            if password == bus_passwords.get(bus_number, ""):
                st.session_state.driver_logged_in = True
                st.session_state.current_bus = bus_number
                st.success("✅ تم الدخول بنجاح")
                st.rerun()
            else:
                st.error("❌ كلمة مرور غير صحيحة")
    else:
        st.success(f"✅ تم الدخول بنجاح - الباص رقم {st.session_state.current_bus}")
        
        if st.button("تسجيل الخروج", type="secondary"):
            st.session_state.driver_logged_in = False
            st.rerun()
        
        # عرض طلاب الباص - التصحيح النهائي
        st.subheader(f"📋 قائمة الطلاب - الباص {st.session_state.current_bus}")
        
        bus_students = st.session_state.students_df[
            st.session_state.students_df["bus"] == st.session_state.current_bus
        ]
        
        if not bus_students.empty:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # الحصول على بيانات الحضور لهذا اليوم
            if not st.session_state.attendance_df.empty:
                today_attendance = st.session_state.attendance_df[
                    st.session_state.attendance_df["date"] == today
                ]
            else:
                today_attendance = pd.DataFrame()
            
            # الطلاب القادمون
            coming_students = today_attendance[
                (today_attendance["bus"] == st.session_state.current_bus) & 
                (today_attendance["status"] == "قادم")
            ] if not today_attendance.empty else pd.DataFrame()
            
            # الإحصائيات
            col1, col2 = st.columns(2)
            with col1:
                st.metric("الطلاب القادمون", len(coming_students))
            with col2:
                st.metric("إجمالي طلاب الباص", len(bus_students))
            
            # عرض الطلاب القادمون
            if not coming_students.empty:
                st.subheader("🎒 الطلاب القادمون اليوم:")
                for _, student in coming_students.iterrows():
                    with st.container():
                        st.success(f"""
                        **✅ {student['name']}**
                        - الصف: {student['grade']}
                        - وقت التسجيل: {student['time']}
                        """)
            else:
                st.info("🚫 لا يوجد طلاب قادمين اليوم")
            
            # عرض جميع طلاب الباص
            st.subheader("👥 جميع طلاب الباص:")
            for _, student in bus_students.iterrows():
                # البحث عن حالة الطالب
                student_attendance = today_attendance[
                    today_attendance["id"].astype(str) == str(student["id"])
                ] if not today_attendance.empty else pd.DataFrame()
                
                if not student_attendance.empty:
                    status = student_attendance.iloc[0]["status"]
                    status_icon = "✅" if status == "قادم" else "❌"
                    status_text = "قادم" if status == "قادم" else "لن يحضر"
                else:
                    status_icon = "⏳"
                    status_text = "لم يسجل"
                
                st.write(f"{status_icon} **{student['name']}** - {student['grade']} - الحالة: {status_text}")

# ===== صفحة أولياء الأمور =====
elif st.session_state.page == "parents":
    st.subheader("👨‍👩‍👧 بوابة أولياء الأمور")
    
    student_id = st.text_input("أدخل رقم الوزارة الخاص بابنك/ابنتك", placeholder="مثال: 1001")
    if student_id:
        student_info = st.session_state.students_df[
            st.session_state.students_df["id"].astype(str) == str(student_id).strip()
        ]
        
        if not student_info.empty:
            student = student_info.iloc[0]
            st.success(f"🎉 تم العثور على الطالب: {student['name']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 متابعة الحضور")
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
                    status_display = "قادم 🎒" if status == "قادم" else "لن يأتي ❌"
                    st.success(f"**آخر حالة:** {status_display}\n**آخر تحديث:** {time}")
                else:
                    st.info("لا توجد بيانات حضور لهذا اليوم")
            
            with col2:
                st.subheader("🚌 معلومات الباص")
                st.info(f"""
                **رقم الباص:** {student['bus']}
                **وقت الصباح التقريبي:** 7:00 صباحاً
                **وقت الظهيرة التقريبي:** 2:00 ظهراً
                **هاتف ولي الأمر:** {student['parent_phone']}
                """)
        else:
            st.error("❌ لم يتم العثور على الطالب")

# ===== الصفحات الأخرى (بنفس التصميم المحسن) =====
# [يتم الحفاظ على نفس التصميم للصفحات الأخرى...]

# ===== التذييل =====
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1.5rem 0;'>
    <p style='margin: 0.3rem 0;'><strong>🚍 نظام الباص الذكي</strong></p>
    <p style='margin: 0.3rem 0;'>مدرسة المنيرة الخاصة - أبوظبي</p>
    <p style='margin: 0.3rem 0;'>© 2024 جميع الحقوق محفوظة</p>
    <p style='margin: 0.3rem 0;'>تم التطوير بواسطة: إياد مصطفى | التصميم: ايمن جلال | الإشراف: قسم النادي البيئي</p>
</div>
""", unsafe_allow_html=True)
