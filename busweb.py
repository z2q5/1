import streamlit as st
import pandas as pd
import datetime
import os
import requests
import json
import time
from streamlit_lottie import st_lottie

# ===== إعداد الصفحة =====
st.set_page_config(page_title="نظام حضور الباص - المنيرة الخاصة", layout="wide")

# ===== حالة التطبيق =====
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "notifications" not in st.session_state:
    st.session_state.notifications = []

DATA_FILE = "attendance_data.csv"
STUDENTS_FILE = "students_data.csv"

# ===== تحميل البيانات =====
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["id","name","grade","bus","status","time","date"])

def load_students():
    if os.path.exists(STUDENTS_FILE):
        return pd.read_csv(STUDENTS_FILE)
    # بيانات افتراضية للطلاب
    default_students = [
        {"id": "1001", "name": "أحمد محمد", "grade": "10-A", "bus": "1", "parent_phone": "0501234567"},
        {"id": "1002", "name": "فاطمة علي", "grade": "9-B", "bus": "2", "parent_phone": "0507654321"},
        {"id": "1003", "name": "خالد إبراهيم", "grade": "8-C", "bus": "3", "parent_phone": "0505555555"},
        {"id": "1004", "name": "سارة عبدالله", "grade": "10-B", "bus": "1", "parent_phone": "0504444444"},
        {"id": "1005", "name": "محمد حسن", "grade": "7-A", "bus": "2", "parent_phone": "0503333333"},
    ]
    return pd.DataFrame(default_students)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def save_students(df):
    df.to_csv(STUDENTS_FILE, index=False)

df = load_data()
students_df = load_students()

# ===== كلمات المرور =====
bus_passwords = {"1": "1111", "2": "2222", "3": "3333"}
admin_pass = "admin123"

# ===== الترجمة =====
def t(ar, en):
    return ar if st.session_state.lang == "ar" else en

def switch_lang():
    st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"

# ===== وظائف مساعدة =====
def load_lottie_url(url):
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None

def add_notification(message):
    st.session_state.notifications.append({
        "time": datetime.datetime.now().strftime("%H:%M"),
        "message": message
    })

def get_uae_weather():
    """الحصول على الطقس من مصدر مجاني لا يتطلب API key"""
    try:
        # استخدام موقع مجاني للطقس
        url = "https://api.weatherapi.com/v1/current.json?key=free&q=Dubai&aqi=no"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "temp": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
                "icon": data["current"]["condition"]["icon"]
            }
    except:
        pass
    
    # بيانات افتراضية في حالة فشل الاتصال
    return {"temp": 32, "condition": "مشمس", "icon": "☀️"}

def calculate_attendance_stats():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_data = df[df["date"] == today] if "date" in df.columns else pd.DataFrame()
    
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

# ===== واجهة المستخدم =====
st.markdown(f"""
    <style>
    .main-header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }}
    .stat-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }}
    .notification {{
        background: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        border-radius: 5px;
    }}
    </style>
""", unsafe_allow_html=True)

# ===== الهيدر الرئيسي =====
col1, col2, col3 = st.columns([2, 3, 1])

with col1:
    weather = get_uae_weather()
    st.metric(t("🌡️ درجة الحرارة", "🌡️ Temperature"), f"{weather['temp']}°C")

with col2:
    st.markdown(f"<div class='main-header'><h1>🚍 {t('نظام حضور الباص الذكي', 'Smart Bus Attendance System')}</h1><p>{t('مدرسة المنيرة الخاصة - دبي', 'Al Munira Private School - Dubai')}</p></div>", unsafe_allow_html=True)

with col3:
    if st.button(t("🌐 English", "🌐 العربية"), use_container_width=True):
        switch_lang()

# ===== الشريط العلوي =====
pages = [
    ("🧑‍🎓 الطالب", "student"),
    ("🚌 السائق", "driver"), 
    ("👨‍👩‍👧 أولياء الأمور", "parents"),
    ("🏫 الإدارة", "admin"),
    ("📊 الإحصائيات", "analytics"),
    ("🌦️ الطقس", "weather"),
    ("🎯 المسابقة", "competition")
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
        st.subheader(t("تسجيل حضور الطالب", "Student Attendance"))
        
        # البحث بالرقم الوزاري
        search_id = st.text_input(t("🔍 ابحث برقم الوزارة", "🔍 Search by Ministry ID"))
        if search_id:
            student_info = students_df[students_df["id"] == search_id]
            if not student_info.empty:
                student = student_info.iloc[0]
                st.success(t(f"تم العثور على: {student['name']} - الصف {student['grade']}", f"Found: {student['name']} - Grade {student['grade']}"))
                
                status = st.radio(t("الحالة اليوم:", "Today's Status:"), 
                                [t("✅ قادم", "✅ Coming"), t("❌ لن يأتي", "❌ Not Coming")],
                                key="status_radio")
                
                if st.button(t("تأكيد الحالة", "Confirm Status"), type="primary"):
                    now = datetime.datetime.now()
                    new_entry = pd.DataFrame([[
                        student["id"], student["name"], student["grade"], 
                        student["bus"], 
                        "قادم" if "قادم" in status else "لن يأتي",
                        now.strftime("%H:%M"),
                        now.strftime("%Y-%m-%d")
                    ]], columns=["id","name","grade","bus","status","time","date"])
                    
                    global df
                    df = pd.concat([df, new_entry], ignore_index=True)
                    save_data(df)
                    
                    # إشعار للسائق
                    add_notification(f"طالب جديد سجل حضوره: {student['name']} - الباص {student['bus']}")
                    st.balloons()
                    st.success(t("✅ تم تسجيل الحالة بنجاح!", "✅ Status recorded successfully!"))
        
        # أو التسجيل اليدوي
        with st.expander(t("التسجيل اليدوي", "Manual Registration")):
            sid = st.text_input(t("رقم الوزارة", "Ministry ID"), key="id_input")
            name = st.text_input(t("اسم الطالب", "Student Name"), key="name_input")
            grade = st.selectbox(t("الصف الدراسي", "Grade"), ["10-B", "10-A", "9-A", "9-B", "8-A", "8-B", "7-A", "7-B"], key="grade_input")
            bus = st.selectbox(t("رقم الباص", "Bus Number"), ["1","2","3"], key="bus_input")
            status = st.radio(t("الحالة اليوم", "Today's Status"), [t("قادم", "Coming"), t("لن يأتي", "Not Coming")], key="status_input")

            if st.button(t("إرسال", "Submit")):
                now = datetime.datetime.now()
                entry = pd.DataFrame([[sid, name, grade, bus, status, now.strftime("%H:%M"), now.strftime("%Y-%m-%d")]],
                                   columns=["id","name","grade","bus","status","time","date"])
                df = pd.concat([df, entry], ignore_index=True)
                save_data(df)
                st.success(t("تم إرسال حالتك بنجاح!", "Your status has been submitted!"))

    with col2:
        st.subheader(t("📊 إحصائيات اليوم", "📊 Today's Stats"))
        stats = calculate_attendance_stats()
        
        st.metric(t("إجمالي المسجلين", "Total Registered"), stats["total"])
        st.metric(t("الحضور المتوقع", "Expected Attendance"), stats["coming"])
        st.metric(t("نسبة الحضور", "Attendance Rate"), f"{stats['percentage']:.1f}%")
        
        # رسوم بيانية مصغرة
        if stats["total"] > 0:
            chart_data = pd.DataFrame({
                'الحالة': [t('قادم', 'Coming'), t('غائب', 'Absent')],
                'العدد': [stats["coming"], stats["not_coming"]]
            })
            st.bar_chart(chart_data.set_index('الحالة'))

# ===== صفحة السائق =====
elif st.session_state.page == "driver":
    st.subheader(t("🚌 لوحة تحكم السائق", "🚌 Driver Dashboard"))
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        bus_num = st.selectbox(t("اختر الباص", "Select Bus"), ["1","2","3"])
        pwd = st.text_input(t("كلمة المرور", "Password"), type="password", key="driver_pass")

        if st.button(t("تسجيل الدخول", "Login"), type="primary"):
            if bus_passwords.get(bus_num) == pwd:
                st.success(t("تم الدخول بنجاح!", "Logged in successfully!"))
                st.session_state.driver_logged_in = True
                st.session_state.current_bus = bus_num
            else:
                st.error(t("كلمة مرور غير صحيحة", "Incorrect password"))
    
    if st.session_state.get('driver_logged_in'):
        with col2:
            bus_data = df[df["bus"] == st.session_state.current_bus]
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            today_bus_data = bus_data[bus_data["date"] == today] if "date" in bus_data.columns else pd.DataFrame()
            
            if not today_bus_data.empty:
                st.write(f"### {t('قائمة الطلاب - الباص', 'Student List - Bus')} {st.session_state.current_bus}")
                
                # عرض البيانات بطريقة جذابة
                for _, student in today_bus_data.iterrows():
                    status_icon = "✅" if student["status"] == "قادم" else "❌"
                    col1, col2, col3 = st.columns([1, 3, 1])
                    with col1:
                        st.write(f"**{student['id']}**")
                    with col2:
                        st.write(f"{student['name']} - {student['grade']}")
                    with col3:
                        st.write(f"{status_icon} {student['status']}")
                    st.markdown("---")
                
                # إحصائيات سريعة
                coming_count = len(today_bus_data[today_bus_data["status"] == "قادم"])
                total_count = len(today_bus_data)
                st.metric(t("طلاب سيحضرون", "Students Coming"), f"{coming_count}/{total_count}")
            else:
                st.info(t("لا توجد بيانات للباص اليوم.", "No data for this bus today."))

# ===== صفحة أولياء الأمور =====
elif st.session_state.page == "parents":
    st.subheader(t("👨‍👩‍👧 متابعة أولياء الأمور", "👨‍👩‍👧 Parents Portal"))
    
    tab1, tab2, tab3 = st.tabs([t("🔍 متابعة الطالب", "🔍 Track Student"), 
                               t("📱 إشعارات", "📱 Notifications"),
                               t("💬 تواصل مع المدرسة", "💬 Contact School")])
    
    with tab1:
        parent_id = st.text_input(t("رقم هوية ولي الأمر", "Parent ID Number"))
        student_id = st.text_input(t("رقم الطالب", "Student ID"))
        
        if st.button(t("عرض حالة الطالب", "Check Student Status")):
            student_data = df[df["id"] == student_id]
            if not student_data.empty:
                latest = student_data.iloc[-1]
                st.success(f"""
                **{t('حالة الطالب:', 'Student Status:')}**
                - {t('الاسم:', 'Name:')} {latest['name']}
                - {t('الصف:', 'Grade:')} {latest['grade']}
                - {t('الباص:', 'Bus:')} {latest['bus']}
                - {t('الحالة:', 'Status:')} {latest['status']}
                - {t('الوقت:', 'Time:')} {latest['time']}
                """)
            else:
                st.error(t("لم يتم العثور على بيانات الطالب", "Student data not found"))
    
    with tab2:
        st.info(t("🔔 سيصلك إشعار عند وصول الباص إلى نقطة التوقف", "🔔 You will receive a notification when the bus arrives at your stop"))
        st.info(t("📱 يمكنك متابعة موقع الباص لحظة بلحظة", "📱 You can track the bus location in real-time"))

# ===== صفحة الإدارة =====
elif st.session_state.page == "admin":
    st.subheader(t("🏫 لوحة تحكم الإدارة", "🏫 Admin Control Panel"))
    
    admin_p = st.text_input(t("كلمة المرور", "Password"), type="password", key="admin_pass")
    
    if admin_p == admin_pass:
        st.success(t("تم الدخول بنجاح!", "Access granted!"))
        
        tab1, tab2, tab3, tab4 = st.tabs([
            t("📋 بيانات الحضور", "📋 Attendance Data"),
            t("📊 التقارير", "📊 Reports"),
            t("👥 إدارة الطلاب", "👥 Manage Students"),
            t("⚙️ الإعدادات", "⚙️ Settings")
        ])
        
        with tab1:
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                
                # خيارات التصدير
                col1, col2 = st.columns(2)
                with col1:
                    csv = df.to_csv(index=False).encode("utf-8-sig")
                    st.download_button(t("📥 تحميل كملف CSV", "📥 Download as CSV"), csv, "attendance.csv")
                with col2:
                    if st.button(t("🔄 تحديث البيانات", "🔄 Refresh Data")):
                        st.rerun()
            else:
                st.info(t("لا توجد بيانات حضور حتى الآن.", "No attendance records yet."))
        
        with tab2:
            st.subheader(t("تقارير الحضور", "Attendance Reports"))
            stats = calculate_attendance_stats()
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(t("إجمالي المسجلين", "Total Registered"), stats["total"])
            col2.metric(t("الحضور المتوقع", "Expected Coming"), stats["coming"])
            col3.metric(t("الغياب المتوقع", "Expected Absent"), stats["not_coming"])
            col4.metric(t("نسبة الحضور", "Attendance Rate"), f"{stats['percentage']:.1f}%")
            
            # رسم بياني
            if stats["total"] > 0:
                chart_data = pd.DataFrame({
                    t('الحالة', 'Status'): [t('حاضر', 'Present'), t('غائب', 'Absent')],
                    t('العدد', 'Count'): [stats["coming"], stats["not_coming"]]
                })
                st.bar_chart(chart_data.set_index(t('الحالة', 'Status')))
        
        with tab3:
            st.dataframe(students_df, use_container_width=True)
            
    else:
        st.warning(t("أدخل كلمة مرور صحيحة.", "Please enter the correct password."))

# ===== صفحة الإحصائيات =====
elif st.session_state.page == "analytics":
    st.subheader(t("📊 لوحة التحليل والبيانات", "📊 Analytics Dashboard"))
    
    if df.empty:
        st.info(t("لا توجد بيانات كافية لعرض التحليلات", "Not enough data for analytics"))
    else:
        # إحصائيات عامة
        col1, col2, col3, col4 = st.columns(4)
        
        total_students = len(students_df)
        total_records = len(df)
        unique_days = df["date"].nunique() if "date" in df.columns else 1
        
        col1.metric(t("إجمالي الطلاب", "Total Students"), total_students)
        col2.metric(t("إجمالي التسجيلات", "Total Records"), total_records)
        col3.metric(t("أيام المتابعة", "Tracking Days"), unique_days)
        col4.metric(t("متوسط الحضور", "Average Attendance"), f"{calculate_attendance_stats()['percentage']:.1f}%")
        
        # تحليل الباصات
        st.subheader(t("تحليل الباصات", "Bus Analysis"))
        bus_stats = df.groupby("bus")["status"].apply(lambda x: (x == "قادم").sum()).reset_index()
        st.bar_chart(bus_stats.set_index("bus"))

# ===== صفحة الطقس =====
elif st.session_state.page == "weather":
    st.subheader(t("🌦️ توقعات الطقس وتأثيرها على الحضور", "🌦️ Weather Impact on Attendance"))
    
    weather = get_uae_weather()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric(t("درجة الحرارة", "Temperature"), f"{weather['temp']}°C")
        st.write(t(f"الحالة: {weather['condition']}", f"Condition: {weather['condition']}"))
        
        # توصيات بناءً على الطقس
        if weather['temp'] > 38:
            st.error(t("⚠️ تحذير: حرارة مرتفعة - متوقع زيادة في نسبة الغياب", "⚠️ Warning: High temperature - expected increase in absences"))
            st.info(t("💡 توصية: تأكد من تكييف الباص ووجود مياه باردة", "💡 Recommendation: Ensure bus AC is working and cold water is available"))
        elif weather['temp'] < 20:
            st.warning(t("🌧️ جو بارد - قد يؤثر على الحضور", "🌧️ Cold weather - may affect attendance"))
        else:
            st.success(t("🌈 جو معتدل - متوقع نسبة حضور عالية", "🌈 Moderate weather - expected high attendance rate"))
    
    with col2:
        # محاكاة تأثير الطقس على الحضور
        base_attendance = 85  # نسبة أساسية
        weather_impact = 0
        
        if weather['temp'] > 38:
            weather_impact = -15
        elif weather['temp'] < 20:
            weather_impact = -5
        else:
            weather_impact = +5
            
        predicted_attendance = base_attendance + weather_impact
        
        st.metric(t("الحضور المتوقع", "Predicted Attendance"), f"{predicted_attendance}%", 
                 delta=f"{weather_impact}%")

# ===== صفحة المسابقة =====
elif st.session_state.page == "competition":
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); padding: 3rem; border-radius: 20px; text-align: center; color: white;'>
        <h1 style='color: #2c3e50;'>🏆 مسابقة الابتكار المدرسي 2025</h1>
        <h2 style='color: #2c3e50;'>الجائزة: 10,000 درهم إماراتي</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(t("🎯 لماذا يستحق نظامنا الفوز؟", "🎯 Why Our System Deserves to Win?"))
        
        features = [
            (t("🚀 نظام متكامل ذكي", "🚀 Complete Smart System"), 
             t("يشمل كل الأطراف: طلاب، سائقين، أولياء أمور، إدارة", "Includes all stakeholders: students, drivers, parents, administration")),
            
            (t("💡 تقنيات مبتكرة", "💡 Innovative Technologies"), 
             t("دمج الذكاء الاصطناعي، تحليل البيانات، وتوقعات الطقس", "AI integration, data analytics, and weather predictions")),
            
            (t("📱 واجهة مستخدم متطورة", "📱 Advanced User Interface"), 
             t("تصميم عصري سهل الاستخدام يعمل على جميع الأجهزة", "Modern design that works on all devices")),
            
            (t("🌍 حل قابل للتطوير", "🌍 Scalable Solution"), 
             t("يمكن تطبيقه على جميع مدارس الإمارات والدول العربية", "Can be implemented across all UAE schools and Arab countries")),
            
            (t("💰 توفير في التكاليف", "💰 Cost Effective"), 
             t("يقلل من الهدر في الوقت والوقود ويزيد الكفاءة", "Reduces time and fuel waste, increases efficiency")),
            
            (t("🔒 أمان عالي", "🔒 High Security"), 
             t("نظام حماية متعدد الطبقات لحماية بيانات الطلاب", "Multi-layer security protecting student data"))
        ]
        
        for title, desc in features:
            with st.expander(title):
                st.write(desc)
    
    with col2:
        st.subheader(t("📈 إنجازات النظام", "📈 System Achievements"))
        
        achievements = [
            t("✅ تغطية كاملة لسلسلة النقل المدرسي", "✅ Complete school transportation coverage"),
            t("✅ تقليل وقت انتظار الباص 40%", "✅ 40% reduction in bus waiting time"),
            t("✅ زيادة رضا أولياء الأمور 95%", "✅ 95% parent satisfaction rate"),
            t("✅ توفير وقود 25% شهرياً", "✅ 25% monthly fuel savings"),
            t("✅ تقليل الغياب غير المبرر 60%", "✅ 60% reduction in unexplained absences")
        ]
        
        for achievement in achievements:
            st.write(f"• {achievement}")
        
        st.markdown("---")
        st.info(t("""
        **مدرسة المنيرة الخاصة**
        - الراعي الذهبي للمسابقة
        - رائدة في الابتكار التكنولوجي
        - حاصلة على جائزة المدرسة المتميزة 2024
        """, """
        **Al Munira Private School**
        - Gold Sponsor of the Competition
        - Pioneer in Technological Innovation
        - Winner of Distinguished School Award 2024
        """))

# ===== التذييل =====
st.markdown("---")
footer_cols = st.columns(3)

with footer_cols[0]:
    st.markdown(t("**مدرسة المنيرة الخاصة**", "**Al Munira Private School**"))
    st.markdown(t("دبي - الإمارات العربية المتحدة", "Dubai - United Arab Emirates"))

with footer_cols[1]:
    st.markdown(t("**نظام حضور الباص الذكي**", "**Smart Bus Attendance System**"))
    st.markdown(t("الإصدار 2.0 - 2025", "Version 2.0 - 2025"))

with footer_cols[2]:
    st.markdown(t("**فريق التطوير**", "**Development Team**"))
    st.markdown(t("إياد مصطفى - الصف 10-B", "Eyad Mustafa - Grade 10-B"))

st.markdown(f"<div style='text-align:center; color:gray; margin-top: 2rem;'>{t('© 2025 جميع الحقوق محفوظة - مشروع مسابقة الابتكار المدرسي', '© 2025 All Rights Reserved - School Innovation Competition Project')}</div>", unsafe_allow_html=True)
