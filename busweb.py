import streamlit as st
import pandas as pd
import datetime
import requests

# ===== إعداد الصفحة =====
st.set_page_config(page_title="نظام حضور الباص - المنيرة الخاصة", layout="wide")

# ===== الحالة العامة =====
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "students" not in st.session_state:
    st.session_state.students = []
if "bus_passwords" not in st.session_state:
    st.session_state.bus_passwords = {"1": "1111", "2": "2222", "3": "3333"}
if "admin_pass" not in st.session_state:
    st.session_state.admin_pass = "admin123"

# ===== وظائف اللغة =====
def t(ar, en):
    return ar if st.session_state.lang == "ar" else en

def switch_lang():
    st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"

# ===== واجهة العنوان =====
st.markdown(f"<h1 style='text-align:center;'>{t('🚍 نظام حضور الباص لمدرسة المنيرة الخاصة', '🚍 Al Munira School Bus Attendance')}</h1>", unsafe_allow_html=True)

# ===== شريط التنقل =====
menu = st.columns(5)
with menu[0]:
    if st.button(t("🧑‍🎓 الطالب", "🧑‍🎓 Student")):
        st.session_state.page = "student"
with menu[1]:
    if st.button(t("🚌 السائق", "🚌 Driver")):
        st.session_state.page = "driver"
with menu[2]:
    if st.button(t("🏫 الإدارة", "🏫 Admin")):
        st.session_state.page = "admin"
with menu[3]:
    if st.button(t("🌟 الكريدتس", "🌟 Credits")):
        st.session_state.page = "credits"
with menu[4]:
    if st.button("🌐 " + t("اللغة", "Language")):
        switch_lang()

st.markdown("---")

# ===== الطالب =====
if st.session_state.page == "student":
    st.subheader(t("تسجيل حضور الطالب", "Student Attendance"))
    id = st.text_input(t("رقم الوزارة", "Ministry ID"), key="student_id")
    name = st.text_input(t("اسم الطالب", "Student Name"), key="student_name")
    grade = st.text_input(t("الصف الدراسي", "Grade"), key="student_grade")
    bus = st.selectbox(t("رقم الباص", "Bus Number"), ["1", "2", "3"], key="student_bus")
    status = st.radio(t("الحالة", "Status"), [t("قادم", "Coming"), t("لن يأتي", "Not Coming")], horizontal=True)
    if st.button(t("إرسال", "Submit")):
        st.session_state.students.append({
            "id": id,
            "name": name,
            "grade": grade,
            "bus": bus,
            "status": "Going" if status == t("قادم", "Coming") else "Not Going",
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.success(t("✅ تم تسجيل الحضور بنجاح", "✅ Attendance submitted successfully"))

# ===== السائق =====
elif st.session_state.page == "driver":
    st.subheader(t("تسجيل دخول السائق", "Driver Login"))
    bus_num = st.text_input(t("رقم الباص", "Bus Number"))
    bus_pass = st.text_input(t("كلمة المرور", "Password"), type="password")
    if st.button(t("دخول", "Login")):
        if bus_num in st.session_state.bus_passwords and st.session_state.bus_passwords[bus_num] == bus_pass:
            st.session_state.driver_logged = bus_num
        else:
            st.error(t("❌ بيانات الدخول غير صحيحة", "❌ Invalid credentials"))

    if "driver_logged" in st.session_state:
        st.success(t(f"تم تسجيل الدخول إلى الباص {st.session_state.driver_logged}", f"Logged in to bus {st.session_state.driver_logged}"))
        data = [s for s in st.session_state.students if s["bus"] == st.session_state.driver_logged]
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.info(t("لا توجد بيانات بعد.", "No data yet."))

# ===== الإدارة =====
elif st.session_state.page == "admin":
    st.subheader(t("تسجيل دخول الإدارة", "Admin Login"))
    ap = st.text_input(t("كلمة المرور", "Password"), type="password")
    if ap == st.session_state.admin_pass:
        st.success(t("تم تسجيل الدخول بنجاح ✅", "Logged in successfully ✅"))
        df = pd.DataFrame(st.session_state.students)
        if not df.empty:
            df_ar = df.rename(columns={
                "id": "رقم الوزارة", "name": "اسم الطالب",
                "grade": "الصف", "bus": "رقم الباص",
                "status": "الحالة", "time": "الوقت"
            })
            st.dataframe(df_ar)
            csv = df_ar.to_csv(index=False).encode("utf-8-sig")
            st.download_button(t("📥 تنزيل التقرير (Excel)", "📥 Download Excel Report"), csv, "bus_report.csv", "text/csv")
        else:
            st.info(t("لا توجد بيانات بعد.", "No data yet."))

        st.markdown("---")
        st.subheader(t("🌤️ حالة الطقس وتوقع الغياب", "🌤️ Weather & Absence Prediction"))
        city = "Abu Dhabi"
        api_key = "8c1573b4b3ecbfb555c6bb8cc22d7e4d"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ar"
        res = requests.get(url).json()
        if res.get("main"):
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            st.write(f"🌡️ {t('درجة الحرارة الحالية', 'Temperature')}: {temp}°C")
            st.write(f"☁️ {t('الجو', 'Condition')}: {desc}")
            if temp > 40:
                st.warning(t("🔥 الجو حار جدًا، قد يقل الحضور.", "🔥 Very hot, attendance may drop."))
            elif temp < 20:
                st.info(t("❄️ الجو بارد قليلًا، الحضور طبيعي.", "❄️ Cool weather, normal attendance."))
            else:
                st.success(t("☀️ الجو معتدل، الحضور المتوقع ممتاز.", "☀️ Pleasant weather, excellent attendance."))

# ===== صفحة الكريدتس =====
elif st.session_state.page == "credits":
    st.subheader("🎖️ Credits")
    st.markdown("""
    ### المشروع: نظام حضور الباص الذكي  
    - 🧠 **البرمجة:** إياد مصطفى  
    - 🎨 **الرسوميات والتصميم:** أيمن جلال  
    - 🏫 **مدرسة المنيرة الخاصة**  
    - 📚 **الصف:** 10-B  
    - © جميع الحقوق محفوظة 2025
    """)
    st.info("هذا النظام ما زال تحت التجريب، والأخطاء واردة.")

# ===== التذييل =====
st.markdown("---")
st.caption("💡 اضغط على الزر أعلاه لتبديل اللغة 🌍 | جميع الحقوق محفوظة لمدرسة المنيرة الخاصة © 2025")
