import streamlit as st
import pandas as pd
import datetime
import os
import requests

# ===== إعداد الصفحة =====
st.set_page_config(page_title="نظام حضور الباص - المنيرة الخاصة", layout="wide")

# ===== حالة التطبيق =====
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "page" not in st.session_state:
    st.session_state.page = "menu"

DATA_FILE = "attendance_data.csv"
RESET_INTERVAL_HOURS = 12

# ===== تحميل البيانات من الملف =====
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if "last_reset" in df.columns:
            try:
                last_reset = datetime.datetime.fromisoformat(df["last_reset"].iloc[0])
                if (datetime.datetime.now() - last_reset).total_seconds() > RESET_INTERVAL_HOURS * 3600:
                    os.remove(DATA_FILE)
                    return pd.DataFrame(columns=["id","name","grade","bus","status","time","last_reset"])
            except:
                pass
        return df
    return pd.DataFrame(columns=["id","name","grade","bus","status","time","last_reset"])

# ===== حفظ البيانات =====
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# ===== كلمات المرور =====
bus_passwords = {"1": "1111", "2": "2222", "3": "3333"}
admin_pass = "admin123"

# ===== الترجمة =====
def t(ar, en):
    return ar if st.session_state.lang == "ar" else en

def switch_lang():
    st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"

# ===== الواجهة الرئيسية =====
st.markdown(f"<h1 style='text-align:center;'>{t('🚍 نظام حضور الباص لمدرسة المنيرة الخاصة', '🚍 Al Munira School Bus Attendance')}</h1>", unsafe_allow_html=True)

# ===== الشريط العلوي =====
cols = st.columns(5)
if cols[0].button(t("🧑‍🎓 الطالب", "🧑‍🎓 Student")):
    st.session_state.page = "student"
if cols[1].button(t("🚌 السائق", "🚌 Driver")):
    st.session_state.page = "driver"
if cols[2].button(t("🏫 الإدارة", "🏫 Admin")):
    st.session_state.page = "admin"
if cols[3].button(t("🌦️ الطقس", "🌦️ Weather")):
    st.session_state.page = "weather"
if cols[4].button(t("🌟 الكريدتس", "🌟 Credits")):
    st.session_state.page = "credits"

st.markdown("---")

# ===== صفحة الطالب =====
if st.session_state.page == "student":
    st.subheader(t("تسجيل حضور الطالب", "Student Attendance"))
    sid = st.text_input(t("رقم الوزارة", "Ministry ID"), key="id_input")
    name = st.text_input(t("اسم الطالب", "Student Name"), key="name_input")
    grade = st.text_input(t("الصف الدراسي", "Grade"), key="grade_input")
    bus = st.selectbox(t("رقم الباص", "Bus Number"), ["1","2","3"], key="bus_input")
    status = st.radio(t("الحالة اليوم", "Today's Status"), [t("قادم", "Coming"), t("لن يأتي", "Not Coming")])

    if st.button(t("إرسال", "Submit")):
        now = datetime.datetime.now().isoformat()
        entry = pd.DataFrame([[sid, name, grade, bus, status, now, datetime.datetime.now().isoformat()]],
                             columns=["id","name","grade","bus","status","time","last_reset"])
        df = pd.concat([df, entry], ignore_index=True)
        save_data(df)
        st.success(t("تم إرسال حالتك بنجاح!", "Your status has been submitted!"))

# ===== صفحة السائق =====
elif st.session_state.page == "driver":
    st.subheader(t("دخول السائق", "Driver Login"))
    bus_num = st.selectbox(t("اختر الباص", "Select Bus"), ["1","2","3"])
    pwd = st.text_input(t("كلمة المرور", "Password"), type="password", key="driver_pass")

    if st.button(t("تسجيل الدخول", "Login")):
        if bus_passwords.get(bus_num) == pwd:
            st.success(t("تم الدخول بنجاح!", "Logged in successfully!"))
            bus_data = df[df["bus"] == bus_num]
            if not bus_data.empty:
                st.table(bus_data[["id","name","grade","status","time"]])
            else:
                st.info(t("لا توجد بيانات بعد.", "No data yet."))
        else:
            st.error(t("كلمة مرور غير صحيحة", "Incorrect password"))

# ===== صفحة الإدارة =====
elif st.session_state.page == "admin":
    st.subheader(t("صفحة الإدارة", "Admin Panel"))
    admin_p = st.text_input(t("كلمة المرور", "Password"), type="password", key="admin_pass")
    if admin_p == admin_pass:
        st.success(t("تم الدخول بنجاح!", "Access granted!"))
        if not df.empty:
            st.dataframe(df)
            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(t("📥 تحميل كملف Excel", "📥 Download as Excel"), csv, "attendance.csv")
        else:
            st.info(t("لا توجد بيانات.", "No attendance records yet."))
    else:
        st.warning(t("أدخل كلمة مرور صحيحة.", "Please enter the correct password."))

# ===== صفحة الطقس =====
elif st.session_state.page == "weather":
    st.subheader(t("توقعات الطقس في الإمارات", "UAE Weather Forecast"))
    try:
        api_key = "2b1d4e2f1f9f6a6efb2e3a7d71a6e6ad"
        url = f"https://api.openweathermap.org/data/2.5/forecast?q=Dubai,AE&appid={api_key}&units=metric&lang={'ar' if st.session_state.lang=='ar' else 'en'}"
        res = requests.get(url)
        data = res.json()
        days = {}
        for entry in data["list"]:
            day = entry["dt_txt"].split(" ")[0]
            temp = entry["main"]["temp"]
            desc = entry["weather"][0]["description"]
            if day not in days:
                days[day] = (temp, desc)
        for day, (temp, desc) in list(days.items())[:5]:
            st.write(f"📅 {day}: 🌡️ {temp}°C — {desc}")
        st.info(t("النظام يتوقع أن الغياب قد يزيد في الأيام ذات الحرارة المرتفعة جدًا.", 
                  "The system predicts higher absences on extremely hot days."))
    except Exception:
        st.error(t("حدث خطأ أثناء جلب بيانات الطقس.", "Error fetching weather data."))

# ===== صفحة الكريدتس =====
elif st.session_state.page == "credits":
    st.markdown("### 🌟 " + t("الكريدتس", "Credits"))
    st.markdown(t(
        """
        - 🧠 الفكرة والتطوير: **إياد مصطفى - الصف 10-B**  
        - 🎨 الرسوميات: **أيمن جلال**  
        - 🏫 المدرسة: **مدرسة المنيرة الخاصة**  
        - 📅 سنة التطوير: **2025**  
        - 💡 هذا النظام لا يزال تحت التجربة وقد تحدث بعض الأخطاء.
        """,
        """
        - 🧠 Concept & Development: **Eyad Mustafa - Grade 10-B**  
        - 🎨 Graphics: **Ayman Galal**  
        - 🏫 School: **Al Munira Private School**  
        - 📅 Year: **2025**  
        - 💡 This system is still under testing; minor bugs may occur.
        """
    ))

# ===== تذييل =====
st.markdown("---")
st.markdown(f"<div style='text-align:center; color:gray;'>{t('© 2025 جميع الحقوق محفوظة لمدرسة المنيرة الخاصة', '© 2025 All Rights Reserved - Al Munira Private School')}</div>", unsafe_allow_html=True)
