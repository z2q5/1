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

# ===== البيانات الافتراضية - التصحيح النهائي =====
def initialize_data():
    """تهيئة جميع البيانات بشكل صحيح"""
    # بيانات الطلاب الافتراضية - التأكد من أن الأعمدة صحيحة
    students_data = [
        {"id": "1001", "name": "أحمد محمد", "grade": "10-A", "bus": "1", "parent_phone": "0501234567"},
        {"id": "1002", "name": "فاطمة علي", "grade": "9-B", "bus": "2", "parent_phone": "0507654321"},
        {"id": "1003", "name": "خالد إبراهيم", "grade": "8-C", "bus": "3", "parent_phone": "0505555555"},
        {"id": "1004", "name": "سارة عبدالله", "grade": "10-B", "bus": "1", "parent_phone": "0504444444"},
        {"id": "1005", "name": "محمد حسن", "grade": "7-A", "bus": "2", "parent_phone": "0503333333"},
        {"id": "1006", "name": "ريم أحمد", "grade": "11-A", "bus": "3", "parent_phone": "0506666666"},
    ]
    
    # التأكد من أن البيانات محفوظة في session state
    if 'students_df' not in st.session_state or st.session_state.students_df.empty:
        st.session_state.students_df = pd.DataFrame(students_data)
    
    if 'attendance_df' not in st.session_state:
        st.session_state.attendance_df = pd.DataFrame(columns=[
            "id", "name", "grade", "bus", "status", "time", "date", "expiry_time"
        ])
    
    if 'ratings_df' not in st.session_state:
        st.session_state.ratings_df = pd.DataFrame(columns=["rating", "comments", "timestamp"])

# تهيئة البيانات عند بدء التشغيل
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
    
    if st.session_state.attendance_df.empty:
        return {"total": 0, "coming": 0, "percentage": 0}
    
    # التأكد من وجود عمود التاريخ
    if "date" not in st.session_state.attendance_df.columns:
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
    
    if st.session_state.attendance_df.empty or "date" not in st.session_state.attendance_df.columns:
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
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
.student-card {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    border-left: 5px solid #667eea;
}
.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    text-align: center;
    margin: 0.5rem;
    border-left: 5px solid #2a5298;
}
.weather-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 20px;
    margin: 1rem 0;
}
.feature-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    margin: 0.5rem 0;
    text-align: center;
}
.team-card-blue {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin: 0.5rem 0;
}
.team-card-green {
    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin: 0.5rem 0;
}
.team-card-orange {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin: 0.5rem 0;
}
.rating-card {
    background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin: 1rem 0;
    text-align: center;
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

# ===== صفحة الطالب - التصحيح النهائي =====
if st.session_state.page == "student":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎓 تسجيل حضور الطالب")
        
        # إزالة زر الأكواد التجريبية ووضع المعلومات مباشرة
        st.info("""
        **💡 معلومات مهمة:**
        - أدخل رقم الوزارة الخاص بك
        - الأرقام المتاحة: 1001, 1002, 1003, 1004, 1005, 1006
        - بعد إدخال الرقم، س تظهر معلوماتك تلقائياً
        """)
        
        student_id = st.text_input("🔍 أدخل رقم الوزارة", placeholder="أدخل رقم الوزارة هنا...")
        
        if student_id:
            # التأكد من أن بيانات الطلاب محملة بشكل صحيح
            if st.session_state.students_df.empty:
                st.error("❌ جاري تحميل بيانات الطلاب...")
                initialize_data()
                st.rerun()
            
            # البحث عن الطالب - التصحيح النهائي هنا
            try:
                # تحويل student_id إلى string للمقارنة الصحيحة
                student_id_str = str(student_id).strip()
                
                # البحث في DataFrame
                student_info = st.session_state.students_df[
                    st.session_state.students_df["id"].astype(str) == student_id_str
                ]
                
                if not student_info.empty:
                    student = student_info.iloc[0]
                    
                    st.markdown(f"""
                    <div class='student-card'>
                        <h3>🎓 {student['name']}</h3>
                        <p><strong>الصف:</strong> {student['grade']}</p>
                        <p><strong>رقم الباص:</strong> {student['bus']}</p>
                        <p><strong>هاتف ولي الأمر:</strong> {student['parent_phone']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # التحقق من التسجيل المسبق
                    already_registered, current_status, expiry_time = has_student_registered_today(student_id_str)
                    
                    if already_registered:
                        st.warning(f"""
                        ⚠️ **لقد سجلت حالتك مسبقاً**
                        
                        **الحالة الحالية:** {current_status}
                        **الحالة سارية حتى:** {expiry_time.strftime('%H:%M')}
                        """)
                        
                        if st.button("تغيير الحالة", type="secondary", use_container_width=True):
                            # إزالة التسجيل القديم
                            today = datetime.datetime.now().strftime("%Y-%m-%d")
                            st.session_state.attendance_df = st.session_state.attendance_df[
                                ~((st.session_state.attendance_df["id"] == student_id_str) & 
                                  (st.session_state.attendance_df["date"] == today))
                            ]
                            st.success("✅ تم إعادة تعيين حالتك، يمكنك التسجيل مرة أخرى")
                            st.rerun()
                    else:
                        # خيارات التسجيل
                        status = st.radio("الحالة اليوم", ["✅ سأحضر اليوم", "❌ لن أحضر اليوم"])
                        
                        if st.button("تأكيد الحالة", type="primary", use_container_width=True):
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
                    **تأكد من إدخال الرقم الصحيح:**
                    - 1001 (أحمد محمد)
                    - 1002 (فاطمة علي) 
                    - 1003 (خالد إبراهيم)
                    - 1004 (سارة عبدالله)
                    - 1005 (محمد حسن)
                    - 1006 (ريم أحمد)
                    """)
                    
            except Exception as e:
                st.error(f"❌ حدث خطأ في البحث: {e}")
                st.info("جرب إدخال أحد هذه الأرقام: 1001, 1002, 1003, 1004, 1005, 1006")

    with col2:
        st.subheader("📊 إحصائيات اليوم")
        stats = calculate_attendance_stats()
        
        st.metric("إجمالي المسجلين", stats["total"])
        st.metric("الحضور المتوقع", stats["coming"])
        st.metric("نسبة الحضور", f"{stats['percentage']:.1f}%")
        
        if stats["total"] > 0:
            st.info(f"📝 حتى الآن: {stats['coming']} طالب مؤكد الحضور")

# ===== صفحة السائق =====
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
        
        # عرض طلاب الباص
        st.subheader(f"📋 قائمة الطلاب - الباص {st.session_state.current_bus}")
        
        bus_students = st.session_state.students_df[
            st.session_state.students_df["bus"] == st.session_state.current_bus
        ]
        
        if not bus_students.empty:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # التأكد من وجود عمود التاريخ
            if not st.session_state.attendance_df.empty and "date" in st.session_state.attendance_df.columns:
                today_attendance = st.session_state.attendance_df[
                    (st.session_state.attendance_df["date"] == today) & 
                    (st.session_state.attendance_df["bus"] == st.session_state.current_bus)
                ]
            else:
                today_attendance = pd.DataFrame()
            
            coming_students = today_attendance[today_attendance["status"] == "قادم"] if not today_attendance.empty else pd.DataFrame()
            
            # الإحصائيات
            col1, col2 = st.columns(2)
            with col1:
                st.metric("الطلاب القادمون", len(coming_students))
            with col2:
                st.metric("إجمالي طلاب الباص", len(bus_students))
            
            # الطلاب القادمون
            if not coming_students.empty:
                st.subheader("🎒 الطلاب القادمون اليوم:")
                for _, student in coming_students.iterrows():
                    st.success(f"✅ **{student['name']}** - {student['grade']} - الساعة: {student['time']}")
            else:
                st.info("🚫 لا يوجد طلاب قادمين اليوم")
            
            # جميع طلاب الباص
            st.subheader("👥 جميع طلاب الباص:")
            for _, student in bus_students.iterrows():
                if not today_attendance.empty:
                    student_status = today_attendance[today_attendance["id"] == student["id"]]
                    status_icon = "✅" if not student_status.empty and student_status.iloc[0]["status"] == "قادم" else "❌"
                else:
                    status_icon = "❌"
                
                st.write(f"{status_icon} **{student['name']}** - {student['grade']}")

# ===== صفحة أولياء الأمور =====
elif st.session_state.page == "parents":
    st.subheader("👨‍👩‍👧 بوابة أولياء الأمور")
    
    student_id = st.text_input("أدخل رقم الوزارة الخاص بابنك/ابنتك", placeholder="مثال: 1001")
    if student_id:
        # البحث عن الطالب
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
                
                if not st.session_state.attendance_df.empty and "date" in st.session_state.attendance_df.columns:
                    today_status = st.session_state.attendance_df[
                        (st.session_state.attendance_df["id"] == student["id"]) & 
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

# ===== صفحة الإدارة =====
elif st.session_state.page == "admin":
    st.subheader("🏫 لوحة تحكم الإدارة")
    
    admin_password = st.text_input("كلمة مرور الإدارة", type="password", placeholder="أدخل كلمة المرور...")
    if admin_password == admin_pass:
        st.success("✅ تم الدخول بنجاح")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 لوحة التحكم", 
            "📋 بيانات الحضور", 
            "👥 إدارة الطلاب", 
            "⭐ نظام التقييم"
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
            
            # مخططات
            if not st.session_state.attendance_df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    bus_distribution = st.session_state.attendance_df["bus"].value_counts()
                    fig1 = px.pie(bus_distribution, values=bus_distribution.values, 
                                names=bus_distribution.index, title="توزيع الطلاب على الباصات")
                    st.plotly_chart(fig1)
        
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
                st.subheader("📊 إحصائيات التقييمات")
                
                # إحصائيات التقييمات
                average_rating = st.session_state.ratings_df["rating"].mean()
                total_ratings = len(st.session_state.ratings_df)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("متوسط التقييم", f"{average_rating:.1f}/5")
                with col2:
                    st.metric("إجمالي التقييمات", total_ratings)
                
                # مخطط التقييمات
                rating_dist = st.session_state.ratings_df["rating"].value_counts().sort_index()
                fig = px.bar(rating_dist, x=rating_dist.index, y=rating_dist.values,
                            title="توزيع التقييمات", labels={'x': 'التقييم', 'y': 'عدد التقييمات'})
                st.plotly_chart(fig)
                
                st.subheader("📋 جميع التقييمات")
                st.dataframe(st.session_state.ratings_df)
            else:
                st.info("لا توجد تقييمات حتى الآن")
    
    elif admin_password and admin_password != admin_pass:
        st.error("❌ كلمة مرور غير صحيحة")

# ===== صفحة الطقس =====
elif st.session_state.page == "weather":
    st.subheader("🌦️ توقعات الطقس")
    
    weather_data = get_weather()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>🌡️ درجة الحرارة</h3>
            <h2>{weather_data['temp']}°C</h2>
            <p>{weather_data['condition_ar']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>💧 الرطوبة</h3>
            <h2>{weather_data['humidity']}%</h2>
            <p>الرطوبة النسبية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='weather-card'>
            <h3>💨 سرعة الرياح</h3>
            <h2>{weather_data['wind_speed']} km/h</h2>
            <p>سرعة الرياح</p>
        </div>
        """, unsafe_allow_html=True)
    
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
    
    st.markdown("### 👨‍💻 فريق التطوير")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='team-card-blue'>
            <h3>💻 المطور الرئيسي</h3>
            <h2>إياد مصطفى</h2>
            <p>المسؤول عن برمجة النظام بالكامل</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='team-card-green'>
            <h3>🎨 مصمم الجرافيك</h3>
            <h2>ايمن جلال</h2>
            <p>مصمم الواجهات والمؤثرات البصرية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='team-card-orange'>
            <h3>👨‍🏫 المشرف</h3>
            <h2>قسم النادي البيئي</h2>
            <p>المشرف على المشروع</p>
        </div>
        """, unsafe_allow_html=True)
    
    # قسم التقييم في صفحة حول النظام
    st.markdown("### ⭐ قيم النظام")
    
    st.markdown("""
    <div class='rating-card'>
        <h3>كيف تقيم تجربتك مع النظام؟</h3>
        <p>شاركنا برأيك لمساعدتنا في التحسين</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("rating_form"):
        rating = st.slider("تقييمك للنظام", 1, 5, 5, help="1 = سيء, 5 = ممتاز")
        comments = st.text_area("ملاحظاتك أو اقتراحاتك")
        
        if st.form_submit_button("إرسال التقييم", type="primary"):
            add_rating(rating, comments)
            st.success("🎉 شكراً لتقييمك النظام! تم إرسال تقييمك بنجاح")
            st.info("📊 يمكنك رؤية إحصائيات التقييمات في صفحة الإدارة")

# ===== التذييل =====
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    © 2024 نظام الباص الذكي - مدرسة المنيرة الخاصة. جميع الحقوق محفوظة<br>
    تم التطوير بواسطة: إياد مصطفى - تصميم: ايمن جلال - إشراف: قسم النادي البيئي
</div>
""", unsafe_allow_html=True)
