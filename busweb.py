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

# ===== البيانات الافتراضية =====
def initialize_data():
    """تهيئة جميع البيانات"""
    # بيانات الطلاب الافتراضية
    students_data = [
        {"id": "1001", "name": "أحمد محمد", "grade": "10-A", "bus": "1", "parent_phone": "0501234567"},
        {"id": "1002", "name": "فاطمة علي", "grade": "9-B", "bus": "2", "parent_phone": "0507654321"},
        {"id": "1003", "name": "خالد إبراهيم", "grade": "8-C", "bus": "3", "parent_phone": "0505555555"},
        {"id": "1004", "name": "سارة عبدالله", "grade": "10-B", "bus": "1", "parent_phone": "0504444444"},
        {"id": "1005", "name": "محمد حسن", "grade": "7-A", "bus": "2", "parent_phone": "0503333333"},
        {"id": "1006", "name": "ريم أحمد", "grade": "11-A", "bus": "3", "parent_phone": "0506666666"},
    ]
    
    if 'students_df' not in st.session_state:
        st.session_state.students_df = pd.DataFrame(students_data)
    
    if 'attendance_df' not in st.session_state:
        st.session_state.attendance_df = pd.DataFrame(columns=[
            "id", "name", "grade", "bus", "status", "time", "date", "expiry_time"
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
        "condition_ar": "مشمس",
        "condition_en": "Sunny"
    }

def calculate_attendance_stats():
    """حساب إحصائيات الحضور"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_data = st.session_state.attendance_df[
        st.session_state.attendance_df["date"] == today
    ] if "date" in st.session_state.attendance_df.columns else pd.DataFrame()
    
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
        return True, latest_record["status"], datetime.datetime.now() + datetime.timedelta(hours=12)
    
    return False, None, None

# ===== واجهة المستخدم =====
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.student-card {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    padding: 1rem;
    border-radius: 15px;
    margin: 1rem 0;
}
.stat-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    text-align: center;
    margin: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ===== الهيدر الرئيسي =====
col1, col2, col3 = st.columns([2, 3, 1])

with col1:
    weather_data = get_weather()
    st.metric("🌡️ درجة الحرارة", f"{weather_data['temp']}°C", weather_data['condition_ar'])

with col2:
    st.markdown("""
    <div class='main-header'>
        <h1>🚍 نظام الباص الذكي</h1>
        <h3>مدرسة المنيرة الخاصة - أبوظبي</h3>
        <p>مرحباً بك في نظام الباص الذكي</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if st.button("🌐 English" if st.session_state.lang == "ar" else "🌐 العربية"):
        st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
        st.rerun()

# ===== الشريط العلوي =====
pages = ["الطالب", "السائق", "أولياء الأمور", "الإدارة", "الطقس", "حول النظام"]
page_keys = ["student", "driver", "parents", "admin", "weather", "about"]

cols = st.columns(len(pages))
for i, (name, key) in enumerate(zip(pages, page_keys)):
    if cols[i].button(name, use_container_width=True):
        st.session_state.page = key

st.markdown("---")

# ===== صفحة الطالب =====
if st.session_state.page == "student":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎓 تسجيل حضور الطالب")
        
        # عرض أكواد الطلاب للمساعدة
        with st.expander("📋 أكواد الطلاب المتاحة"):
            st.write("**الأكواد المتاحة:** 1001, 1002, 1003, 1004, 1005, 1006")
        
        student_id = st.text_input("🔍 أدخل رقم الوزارة", placeholder="مثال: 1001")
        
        if student_id:
            student_info = st.session_state.students_df[
                st.session_state.students_df["id"] == student_id
            ]
            
            if not student_info.empty:
                student = student_info.iloc[0]
                
                st.markdown(f"""
                <div class='student-card'>
                    <h3>🎓 {student['name']}</h3>
                    <p><strong>الصف:</strong> {student['grade']}</p>
                    <p><strong>رقم الباص:</strong> {student['bus']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # التحقق من التسجيل المسبق
                already_registered, current_status, expiry_time = has_student_registered_today(student_id)
                
                if already_registered:
                    st.warning(f"""
                    ⚠️ **لقد سجلت حالتك مسبقاً**
                    
                    **الحالة الحالية:** {current_status}
                    **الحالة سارية حتى:** {expiry_time.strftime('%H:%M') if expiry_time else 'N/A'}
                    """)
                    
                    if st.button("تغيير الحالة", type="secondary"):
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
                    status = st.radio("الحالة اليوم", ["✅ سأحضر اليوم", "❌ لن أحضر اليوم"])
                    
                    if st.button("تأكيد الحالة", type="primary"):
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
                        st.success(f"✅ تم تسجيل حالتك بنجاح! أنت {status_text} اليوم")
                        add_notification(f"طالب جديد سجل حضوره: {student['name']}")
            else:
                st.error("❌ لم يتم العثور على الطالب")
                st.info("جرب أحد هذه الأرقام: 1001, 1002, 1003, 1004, 1005, 1006")

    with col2:
        st.subheader("📊 إحصائيات اليوم")
        stats = calculate_attendance_stats()
        
        st.metric("إجمالي المسجلين", stats["total"])
        st.metric("الحضور المتوقع", stats["coming"])
        st.metric("نسبة الحضور", f"{stats['percentage']:.1f}%")

# ===== صفحة السائق =====
elif st.session_state.page == "driver":
    st.subheader("🚌 لوحة تحكم السائق")
    
    if not st.session_state.driver_logged_in:
        col1, col2 = st.columns(2)
        with col1:
            bus_number = st.selectbox("اختر الباص", ["1", "2", "3"])
        with col2:
            password = st.text_input("كلمة المرور", type="password")
        
        if st.button("تسجيل الدخول"):
            if password == bus_passwords.get(bus_number, ""):
                st.session_state.driver_logged_in = True
                st.session_state.current_bus = bus_number
                st.success("✅ تم الدخول بنجاح")
                st.rerun()
            else:
                st.error("❌ كلمة مرور غير صحيحة")
    else:
        st.success(f"✅ تم الدخول بنجاح - الباص رقم {st.session_state.current_bus}")
        
        if st.button("تسجيل الخروج"):
            st.session_state.driver_logged_in = False
            st.rerun()
        
        # عرض طلاب الباص
        st.subheader(f"📋 قائمة الطلاب - الباص {st.session_state.current_bus}")
        
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
            
            st.metric("الطلاب القادمون", len(coming_students))
            
            if not coming_students.empty:
                st.subheader("🎒 الطلاب القادمون اليوم:")
                for _, student in coming_students.iterrows():
                    st.success(f"✅ **{student['name']}** - {student['grade']} - الساعة: {student['time']}")
            else:
                st.info("🚫 لا يوجد طلاب قادمين اليوم")
            
            # جميع طلاب الباص
            st.subheader("👥 جميع طلاب الباص:")
            for _, student in bus_students.iterrows():
                student_status = today_attendance[today_attendance["id"] == student["id"]]
                status_icon = "✅" if not student_status.empty and student_status.iloc[0]["status"] == "قادم" else "❌"
                st.write(f"{status_icon} **{student['name']}** - {student['grade']}")
        else:
            st.info("لا توجد بيانات للباص اليوم")

# ===== صفحة أولياء الأمور =====
elif st.session_state.page == "parents":
    st.subheader("👨‍👩‍👧 بوابة أولياء الأمور")
    
    student_id = st.text_input("أدخل رقم الوزارة الخاص بابنك/ابنتك")
    if student_id:
        student_info = st.session_state.students_df[
            st.session_state.students_df["id"] == student_id
        ]
        
        if not student_info.empty:
            student = student_info.iloc[0]
            st.success(f"🎉 تم العثور على الطالب: {student['name']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 متابعة الحضور")
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                today_status = st.session_state.attendance_df[
                    (st.session_state.attendance_df["id"] == student_id) & 
                    (st.session_state.attendance_df["date"] == today)
                ]
                
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

# ===== صفحة الإدارة =====
elif st.session_state.page == "admin":
    st.subheader("🏫 لوحة تحكم الإدارة")
    
    admin_password = st.text_input("كلمة مرور الإدارة", type="password")
    if admin_password == admin_pass:
        st.success("✅ تم الدخول بنجاح")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 لوحة التحكم", 
            "📋 بيانات الحضور", 
            "👥 إدارة الطلاب", 
            "⭐ التقييمات"
        ])
        
        with tab1:
            st.subheader("📊 لوحة التحكم")
            stats = calculate_attendance_stats()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("إجمالي الطلاب", len(st.session_state.students_df))
            with col2:
                st.metric("الحاضرون اليوم", stats["coming"])
            with col3:
                st.metric("نسبة الحضور", f"{stats['percentage']:.1f}%")
            with col4:
                st.metric("الباصات العاملة", 3)
            
            # مخطط بسيط
            if not st.session_state.attendance_df.empty:
                bus_distribution = st.session_state.attendance_df["bus"].value_counts()
                fig = px.pie(bus_distribution, values=bus_distribution.values, 
                            names=bus_distribution.index, title="توزيع الطلاب على الباصات")
                st.plotly_chart(fig)
        
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
    st.subheader("🌦️ توقعات الطقس")
    
    weather_data = get_weather()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌡️ درجة الحرارة", f"{weather_data['temp']}°C")
    with col2:
        st.metric("💧 الرطوبة", f"{weather_data['humidity']}%")
    with col3:
        st.metric("💨 سرعة الرياح", f"{weather_data['wind_speed']} km/h")
    
    st.info("""
    **تأثير الطقس على الحضور:**
    - ☀️ طقس مشمس: نسبة حضور عالية (95%)
    - 🌧️ طقس ممطر: نسبة حضور متوسطة (85%) 
    - 💨 طقس عاصف: نسبة حضور جيدة (90%)
    """)

# ===== صفحة حول النظام =====
elif st.session_state.page == "about":
    st.subheader("ℹ️ حول النظام")
    
    st.markdown("### 🚀 مميزات النظام")
    
    features = [
        "🌱 نظام صديق للبيئة",
        "⏱️ مراقبة في الوقت الحقيقي", 
        "📊 تحليلات ذكية",
        "📱 متعدد المنصات",
        "🎯 سهل الاستخدام",
        "🔒 نظام آمن"
    ]
    
    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            st.info(feature)
    
    st.markdown("### 👨‍💻 فريق التطوير")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("""
        **💻 المطور الرئيسي**
        # إياد مصطفى
        """)
    
    with col2:
        st.success("""
        **🎨 مصمم الجرافيك**
        # ايمن جلال
        """)
    
    with col3:
        st.success("""
        **👨‍🏫 المشرف**
        # قسم النادي البيئي
        """)

# ===== التذييل =====
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    © 2024 نظام الباص الذكي - مدرسة المنيرة الخاصة. جميع الحقوق محفوظة
</div>
""", unsafe_allow_html=True)
