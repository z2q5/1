import streamlit as st
import pandas as pd
import datetime
import os
import random
import plotly.express as px

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
if "students_df" not in st.session_state:
    st.session_state.students_df = pd.DataFrame()
if "attendance_df" not in st.session_state:
    st.session_state.attendance_df = pd.DataFrame()
if "ratings_df" not in st.session_state:
    st.session_state.ratings_df = pd.DataFrame()

# ===== الترجمة =====
def t(key):
    translations = {
        "student": "الطالب",
        "driver": "السائق", 
        "parents": "أولياء الأمور",
        "admin": "الإدارة", 
        "weather": "الطقس",
        "about": "حول البرنامج",
        "search_by_id": "ابحث برقم الوزارة",
        "enter_id": "أدخل رقم الوزارة",
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
        "change_status": "تغيير الحالة",
        "driver_dashboard": "لوحة تحكم السائق",
        "select_bus": "اختر الباص",
        "password": "كلمة المرور",
        "login": "تسجيل الدخول",
        "logout": "تسجيل الخروج",
        "student_list": "قائمة الطلاب", 
        "students_coming": "الطلاب القادمون",
        "no_data": "لا توجد بيانات",
        "parents_portal": "بوابة أولياء الأمور",
        "enter_student_id": "أدخل رقم الطالب",
        "attendance_tracking": "متابعة الحضور",
        "bus_info": "معلومات الباص",
        "latest_status": "آخر حالة",
        "last_update": "آخر تحديث",
        "admin_panel": "لوحة الإدارة",
        "admin_password": "كلمة مرور الإدارة",
        "access_granted": "تم الدخول بنجاح",
        "weather_forecast": "توقعات الطقس",
        "temperature": "درجة الحرارة",
        "humidity": "الرطوبة",
        "wind_speed": "سرعة الرياح",
        "about_system": "حول النظام",
        "features": "المميزات",
        "development_team": "فريق التطوير",
        "lead_developer": "المطور الرئيسي", 
        "designer": "مصمم الجرافيك",
        "supervisor": "المشرف",
        "today_stats": "إحصائيات اليوم",
        "total_students": "إجمالي الطلاب",
        "present_today": "الحاضرون اليوم", 
        "attendance_rate": "نسبة الحضور",
        "total_registered": "إجمالي المسجلين",
        "expected_attendance": "الحضور المتوقع",
        "all_rights_reserved": "جميع الحقوق محفوظة"
    }
    return translations.get(key, key)

# ===== تهيئة البيانات =====
def initialize_data():
    """تهيئة جميع البيانات بشكل صحيح"""
    # بيانات الطلاب الافتراضية
    if st.session_state.students_df.empty:
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
    
    # بيانات الحضور
    if st.session_state.attendance_df.empty:
        st.session_state.attendance_df = pd.DataFrame(columns=[
            "id", "name", "grade", "bus", "status", "time", "date", "expiry_time"
        ])
    
    # بيانات التقييمات
    if st.session_state.ratings_df.empty:
        st.session_state.ratings_df = pd.DataFrame(columns=[
            "rating", "comments", "timestamp"
        ])

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
        "condition_ar": random.choice(["مشمس", "غائم", "صافي", "مغبر"]),
        "condition_en": random.choice(["Sunny", "Cloudy", "Clear", "Dusty"])
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
    """التحقق من تسجيل الطالب"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if st.session_state.attendance_df.empty:
        return False, None, None
    
    student_data = st.session_state.attendance_df[
        (st.session_state.attendance_df["id"] == student_id) & 
        (st.session_state.attendance_df["date"] == today)
    ]
    
    if not student_data.empty:
        latest_record = student_data.iloc[-1]
        expiry_time = datetime.datetime.now() + datetime.timedelta(hours=12)
        return True, latest_record["status"], expiry_time
    
    return False, None, None

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
    .student-card {{
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
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
    .notification-card {{
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }}
    </style>
""", unsafe_allow_html=True)

# ===== الهيدر الرئيسي =====
col1, col2, col3 = st.columns([2, 3, 1])

with col1:
    weather_data = get_weather()
    temp = weather_data["temp"]
    condition = weather_data["condition_ar"] if st.session_state.lang == "ar" else weather_data["condition_en"]
    st.metric(f"🌡️ {t('temperature')}", f"{temp}°C", f"{condition}")

with col2:
    st.markdown(f"""
    <div class='main-header'>
        <h1>🚍 نظام الباص الذكي</h1>
        <h3>مدرسة المنيرة الخاصة - أبوظبي</h3>
        <p>مرحباً بك في نظام الباص الذكي</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    lang_button = "🌐 English" if st.session_state.lang == "ar" else "🌐 العربية"
    if st.button(lang_button, use_container_width=True):
        st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
        st.rerun()

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
        
        # عرض أكواد الطلاب للمساعدة
        with st.expander("📋 أكواد الطلاب المتاحة (انقر هنا)", icon="ℹ️"):
            st.write("**يمكنك استخدام أي من هذه الأرقام:**")
            st.code("1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008")
            st.write("""
            **الأرقام والطلاب:**
            - 1001: أحمد محمد
            - 1002: فاطمة علي  
            - 1003: خالد إبراهيم
            - 1004: سارة عبدالله
            - 1005: محمد حسن
            - 1006: ريم أحمد
            - 1007: يوسف خالد
            - 1008: نورة سعيد
            """)
        
        student_id = st.text_input("🔍 " + t("enter_id"), placeholder="أدخل رقم الوزارة هنا...")
        
        if student_id:
            # البحث عن الطالب
            student_info = st.session_state.students_df[
                st.session_state.students_df["id"] == student_id
            ]
            
            if not student_info.empty:
                student = student_info.iloc[0]
                
                # عرض معلومات الطالب
                st.markdown(f"""
                <div class='student-card'>
                    <h3>🎓 {student['name']}</h3>
                    <p><strong>{t('grade')}:</strong> {student['grade']}</p>
                    <p><strong>{t('bus_number')}:</strong> {student['bus']}</p>
                    <p><strong>هاتف ولي الأمر:</strong> {student['parent_phone']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # التحقق من التسجيل المسبق
                already_registered, current_status, expiry_time = has_student_registered_today(student_id)
                
                if already_registered:
                    st.warning(f"""
                    ⚠️ **{t('already_registered')}**
                    
                    **{t('current_status')}:** {current_status}
                    **الحالة سارية حتى:** {expiry_time.strftime('%H:%M')}
                    """)
                    
                    if st.button(t('change_status'), type="secondary", use_container_width=True):
                        # إزالة التسجيل القديم
                        today = datetime.datetime.now().strftime("%Y-%m-%d")
                        st.session_state.attendance_df = st.session_state.attendance_df[
                            ~((st.session_state.attendance_df["id"] == student_id) & 
                              (st.session_state.attendance_df["date"] == today))
                        ]
                        st.success("✅ تم إعادة تعيين حالتك، يمكنك التسجيل مرة أخرى")
                        st.rerun()
                else:
                    # خيارات التسجيل
                    status = st.radio(
                        t("today_status"), 
                        ["✅ سأحضر اليوم", "❌ لن أحضر اليوم"]
                    )
                    
                    if st.button(t("confirm_status"), type="primary", use_container_width=True):
                        now = datetime.datetime.now()
                        status_text = "قادم" if "سأحضر" in status else "لن يأتي"
                        
                        new_entry = pd.DataFrame([{
                            "id": student["id"],
                            "name": student["name"], 
                            "grade": student["grade"],
                            "bus": student["bus"],
                            "status": status_text,
                            "time": now.strftime("%H:%M"),
                            "date": now.strftime("%Y-%m-%d"),
                            "expiry_time": (now + datetime.timedelta(hours=12)).strftime("%Y-%m-%d %H:%M:%S")
                        }])
                        
                        st.session_state.attendance_df = pd.concat([
                            st.session_state.attendance_df, new_entry
                        ], ignore_index=True)
                        
                        st.balloons()
                        st.success(f"""
                        🎉 **تم التسجيل بنجاح!**
                        
                        **الطالب:** {student['name']}
                        **الحالة:** {status_text}
                        **وقت التسجيل:** {now.strftime('%H:%M')}
                        **رقم الباص:** {student['bus']}
                        """)
                        
                        add_notification(f"طالب جديد سجل حضوره: {student['name']} - الباص {student['bus']}")
            else:
                st.error("❌ لم يتم العثور على الطالب")
                st.info("""
                **جرب أحد هذه الأرقام:**
                - 1001 (أحمد محمد)
                - 1002 (فاطمة علي) 
                - 1003 (خالد إبراهيم)
                - 1004 (سارة عبدالله)
                - 1005 (محمد حسن)
                - 1006 (ريم أحمد)
                """)

    with col2:
        st.subheader("📊 " + t("today_stats"))
        stats = calculate_attendance_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(t("total_registered"), stats["total"])
        with col2:
            st.metric(t("expected_attendance"), stats["coming"])
        with col3:
            st.metric(t("attendance_rate"), f"{stats['percentage']:.1f}%")
        
        # إشعارات سريعة
        if stats["total"] > 0:
            st.info(f"📝 حتى الآن: {stats['coming']} طالب مؤكد الحضور")

# ===== صفحة السائق =====
elif st.session_state.page == "driver":
    st.subheader("🚌 " + t("driver_dashboard"))
    
    if not st.session_state.driver_logged_in:
        col1, col2 = st.columns(2)
        with col1:
            bus_number = st.selectbox(t("select_bus"), ["1", "2", "3"])
        with col2:
            password = st.text_input(t("password"), type="password", placeholder="أدخل كلمة المرور...")
        
        if st.button(t("login"), type="primary", use_container_width=True):
            if password == bus_passwords.get(bus_number, ""):
                st.session_state.driver_logged_in = True
                st.session_state.current_bus = bus_number
                st.success("✅ " + t("access_granted"))
                st.rerun()
            else:
                st.error("❌ كلمة مرور غير صحيحة")
    else:
        st.success(f"✅ {t('access_granted')} - {t('bus_number')} {st.session_state.current_bus}")
        
        if st.button(t("logout"), type="secondary"):
            st.session_state.driver_logged_in = False
            st.rerun()
        
        # عرض طلاب الباص
        st.subheader(f"📋 {t('student_list')} - {t('bus_number')} {st.session_state.current_bus}")
        
        bus_students = st.session_state.students_df[
            st.session_state.students_df["bus"] == st.session_state.current_bus
        ]
        
        if not bus_students.empty:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            today_attendance = st.session_state.attendance_df[
                (st.session_state.attendance_df["date"] == today) & 
                (st.session_state.attendance_df["bus"] == st.session_state.current_bus)
            ]
            
            coming_students = today_attendance[today_attendance["status"] == "قادم"]
            
            # الإحصائيات
            col1, col2 = st.columns(2)
            with col1:
                st.metric(t("students_coming"), len(coming_students))
            with col2:
                st.metric("إجمالي طلاب الباص", len(bus_students))
            
            # الطلاب القادمون
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
            
            # جميع طلاب الباص
            st.subheader("👥 جميع طلاب الباص:")
            for _, student in bus_students.iterrows():
                student_status = today_attendance[today_attendance["id"] == student["id"]]
                status_icon = "✅" if not student_status.empty and student_status.iloc[0]["status"] == "قادم" else "❌"
                status_text = "قادم" if not student_status.empty and student_status.iloc[0]["status"] == "قادم" else "لم يسجل"
                
                st.write(f"{status_icon} **{student['name']}** - {student['grade']} - الحالة: {status_text}")
        else:
            st.info("لا توجد بيانات للباص اليوم")

# ===== صفحة أولياء الأمور =====
elif st.session_state.page == "parents":
    st.subheader("👨‍👩‍👧 " + t("parents_portal"))
    
    student_id = st.text_input(t("enter_student_id"), placeholder="أدخل رقم الطالب...")
    if student_id:
        student_info = st.session_state.students_df[
            st.session_state.students_df["id"] == student_id
        ]
        
        if not student_info.empty:
            student = student_info.iloc[0]
            st.success(f"🎉 تم العثور على الطالب: {student['name']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 " + t("attendance_tracking"))
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                today_status = st.session_state.attendance_df[
                    (st.session_state.attendance_df["id"] == student_id) & 
                    (st.session_state.attendance_df["date"] == today)
                ]
                
                if not today_status.empty:
                    status = today_status.iloc[0]["status"]
                    time = today_status.iloc[0]["time"]
                    status_display = "قادم 🎒" if status == "قادم" else "لن يأتي ❌"
                    st.success(f"""
                    **{t('latest_status')}:** {status_display}
                    **{t('last_update')}:** {time}
                    """)
                else:
                    st.info("لا توجد بيانات حضور لهذا اليوم")
            
            with col2:
                st.subheader("🚌 " + t("bus_info"))
                st.info(f"""
                **{t('bus_number')}:** {student['bus']}
                **وقت الصباح التقريبي:** 7:00 صباحاً
                **وقت الظهيرة التقريبي:** 2:00 ظهراً
                **هاتف ولي الأمر:** {student['parent_phone']}
                """)
        else:
            st.error("❌ لم يتم العثور على الطالب")

# ===== صفحة الإدارة =====
elif st.session_state.page == "admin":
    st.subheader("🏫 " + t("admin_panel"))
    
    admin_password = st.text_input(t("admin_password"), type="password", placeholder="أدخل كلمة المرور...")
    if admin_password == admin_pass:
        st.success("✅ " + t("access_granted"))
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 " + t("today_stats"), 
            "📋 بيانات الحضور", 
            "👥 إدارة الطلاب", 
            "⭐ التقييمات"
        ])
        
        with tab1:
            st.subheader("📊 لوحة التحكم")
            stats = calculate_attendance_stats()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(t("total_students"), len(st.session_state.students_df))
            with col2:
                st.metric(t("present_today"), stats["coming"])
            with col3:
                st.metric(t("attendance_rate"), f"{stats['percentage']:.1f}%")
            with col4:
                st.metric("الباصات النشطة", 3)
            
            # مخططات
            if not st.session_state.attendance_df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    bus_distribution = st.session_state.attendance_df["bus"].value_counts()
                    fig1 = px.pie(bus_distribution, values=bus_distribution.values, 
                                names=bus_distribution.index, title="توزيع الطلاب على الباصات")
                    st.plotly_chart(fig1)
                
                with col2:
                    grade_distribution = st.session_state.attendance_df["grade"].value_counts()
                    fig2 = px.bar(grade_distribution, x=grade_distribution.index, 
                                y=grade_distribution.values, title="توزيع الطلاب حسب الصف")
                    st.plotly_chart(fig2)
        
        with tab2:
            st.subheader("📋 بيانات الحضور")
            if not st.session_state.attendance_df.empty:
                st.dataframe(st.session_state.attendance_df)
            else:
                st.info("لا توجد بيانات حضور")
        
        with tab3:
            st.subheader("👥 إدارة الطلاب")
            st.dataframe(st.session_state.students_df)
            
            with st.expander("➕ إضافة طالب جديد"):
                with st.form("add_student"):
                    new_id = st.text_input("ID")
                    new_name = st.text_input("اسم الطالب")
                    new_grade = st.text_input("الصف")
                    new_bus = st.text_input("رقم الباص")
                    new_phone = st.text_input("هاتف ولي الأمر")
                    
                    if st.form_submit_button("إضافة"):
                        new_student = pd.DataFrame([{
                            "id": new_id, "name": new_name, "grade": new_grade,
                            "bus": new_bus, "parent_phone": new_phone
                        }])
                        st.session_state.students_df = pd.concat([
                            st.session_state.students_df, new_student
                        ], ignore_index=True)
                        st.success("✅ تم إضافة الطالب بنجاح")
        
        with tab4:
            st.subheader("⭐ نظام التقييم")
            if not st.session_state.ratings_df.empty:
                st.dataframe(st.session_state.ratings_df)
            else:
                st.info("لا توجد تقييمات حتى الآن")
            
            with st.form("rating_form"):
                rating = st.slider("تقييمك", 1, 5, 5)
                comments = st.text_area("ملاحظاتك")
                
                if st.form_submit_button("إرسال التقييم"):
                    new_rating = pd.DataFrame([{
                        "rating": rating,
                        "comments": comments,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    st.session_state.ratings_df = pd.concat([
                        st.session_state.ratings_df, new_rating
                    ], ignore_index=True)
                    st.success("✅ شكراً لتقييمك النظام")
    
    elif admin_password and admin_password != admin_pass:
        st.error("❌ كلمة مرور غير صحيحة")

# ===== صفحة الطقس =====
elif st.session_state.page == "weather":
    st.subheader("🌦️ " + t("weather_forecast"))
    
    weather_data = get_weather()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>🌡️ {t('temperature')}</h3>
            <h2>{weather_data['temp']}°C</h2>
            <p>{weather_data['condition_ar']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>💧 {t('humidity')}</h3>
            <h2>{weather_data['humidity']}%</h2>
            <p>الرطوبة النسبية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>💨 {t('wind_speed')}</h3>
            <h2>{weather_data['wind_speed']} km/h</h2>
            <p>سرعة الرياح</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>☀️ مؤشر الأشعة</h3>
            <h2>{random.randint(3, 11)}</h2>
            <p>متوسط إلى عالي</p>
        </div>
        """, unsafe_allow_html=True)
    
    # تأثير الطقس
    st.subheader("📊 تأثير الطقس على الحضور")
    
    impact_data = {
        "condition": ["مشمس", "ممطر", "عاصف", "حار جداً"],
        "attendance_rate": [95, 85, 90, 88]
    }
    impact_df = pd.DataFrame(impact_data)
    
    fig = px.bar(impact_df, x='condition', y='attendance_rate', 
                 title="تأثير الطقس على نسبة الحضور")
    st.plotly_chart(fig)

# ===== صفحة حول النظام =====
elif st.session_state.page == "about":
    st.subheader("ℹ️ " + t("about_system"))
    
    # قسم المميزات
    st.markdown("### 🚀 " + t("features"))
    
    features = [
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
    
    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='feature-card'>
                <h4>{feature}</h4>
            </div>
            """, unsafe_allow_html=True)
    
    # قسم فريق التطوير
    st.markdown("### 👨‍💻 " + t("development_team"))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='team-card'>
            <h3>💻 {t('lead_developer')}</h3>
            <h2>إياد مصطفى</h2>
            <p>المطور الرئيسي والمسؤول عن برمجة النظام</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='team-card'>
            <h3>🎨 {t('designer')}</h3>
            <h2>ايمن جلال</h2>
            <p>مصمم الجرافيك والواجهات</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='team-card'>
            <h3>👨‍🏫 {t('supervisor')}</h3>
            <h2>قسم النادي البيئي</h2>
            <p>المشرف على المشروع</p>
        </div>
        """, unsafe_allow_html=True)
    
    # قسم التقنيات
    st.markdown("### 💻 التقنيات المستخدمة")
    
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("""
        #### 🐍 تقنيات البرمجة:
        - Python 3.11
        - Streamlit Framework  
        - Pandas للبيانات
        - Plotly للرسوم البيانية
        - datetime لإدارة الوقت
        
        #### 🎨 تقنيات التصميم:
        - CSS3 المتقدم
        - تصميم متجاوب
        - ألوان متدرجة
        """)
    
    with tech_col2:
        st.markdown("""
        #### 📊 إدارة البيانات:
        - DataFrames
        - Session State Management  
        - Real-time Updates
        - CSV Files
        
        #### 🌐 المميزات التقنية:
        - واجهة متعددة اللغات
        - تحديث فوري
        - تصميم متكامل
        """)

# ===== التذييل =====
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])

with footer_col1:
    st.markdown(f"""
    <div style='text-align: center; color: #666; font-size: 12px;'>
        © 2024 نظام الباص الذكي - مدرسة المنيرة الخاصة. {t('all_rights_reserved')}<br>
        تم التطوير بواسطة: إياد مصطفى - تصميم: ايمن جلال - إشراف: قسم النادي البيئي
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    if st.session_state.notifications:
        with st.expander(f"🔔 الإشعارات ({len(st.session_state.notifications)})"):
            for notification in st.session_state.notifications[-5:]:
                st.write(f"{notification['time']}: {notification['message']}")

with footer_col3:
    if st.button("🔄 تحديث الصفحة"):
        st.rerun()
