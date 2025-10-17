import streamlit as st
import sqlite3
import datetime
import requests
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

# ===== إعداد قاعدة البيانات =====
conn = sqlite3.connect('bus_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS students
             (student_id TEXT PRIMARY KEY, name TEXT, grade TEXT, bus_no TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS attendance
             (student_id TEXT, name TEXT, bus_no TEXT, status TEXT, date TEXT)''')
conn.commit()

# ===== مفاتيح النظام =====
WEATHER_API_KEY = "a90d21ff18d439b21a8a6795ada3e371"
CITY = "Abu Dhabi"
ADMIN_PASS = "admin2025"
drivers = {"1": "1111", "2": "2222", "3": "3333"}

# ===== حالة التطبيق =====
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def t(ar, en):
    return ar if st.session_state.lang == "ar" else en

def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>
        body { background-color: #121212; color: white; }
        .stButton>button { background-color: #1E88E5; color: white; border-radius: 8px; }
        </style>""", unsafe_allow_html=True)
apply_theme()

# ===== الشريط الجانبي =====
with st.sidebar:
    st.title("🚍 " + t("نظام حضور الباص", "Bus Attendance System"))
    st.markdown("🏫 **مدرسة المنيرة الخاصة**")
    st.markdown("👨‍🎓 **الصف:** 10-B")
    st.markdown("---")

    lang_choice = st.radio(t("اللغة:", "Language:"), ["العربية", "English"])
    st.session_state.lang = "ar" if lang_choice == "العربية" else "en"

    theme_choice = st.radio(t("الثيم:", "Theme:"), ["فاتح", "داكن"] if st.session_state.lang=="ar" else ["Light", "Dark"])
    st.session_state.theme = "dark" if theme_choice in ["داكن", "Dark"] else "light"

# ===== شريط التنقل =====
selected = option_menu(
    None,
    [t("👩‍🎓 الطالب", "👩‍🎓 Student"),
     t("🧑‍✈️ السائق", "🧑‍✈️ Driver"),
     t("🏫 الإدارة", "🏫 Admin"),
     t("🌤️ الطقس", "🌤️ Weather"),
     t("💬 الكريدتس", "💬 Credits")],
    icons=["person", "truck", "shield", "cloud-sun", "info-circle"],
    orientation="horizontal"
)

# ===== واجهة الطالب =====
if selected == t("👩‍🎓 الطالب", "👩‍🎓 Student"):
    st.header(t("🧾 تسجيل أو حضور الطالب", "🧾 Student Registration or Attendance"))
    mode = st.radio(t("اختر العملية:", "Choose Action:"), [t("تسجيل جديد", "New Registration"), t("تسجيل حضور", "Mark Attendance")])

    # تسجيل جديد
    if mode == t("تسجيل جديد", "New Registration"):
        sid = st.text_input(t("رقم الوزارة", "Ministry ID"), key="sid")
        name = st.text_input(t("الاسم الكامل", "Full Name"), key="name")
        grade = st.text_input(t("الصف الدراسي", "Grade"), key="grade")
        bus_no = st.text_input(t("رقم الباص", "Bus Number"), key="bus")

        if st.button(t("حفظ", "Save")):
            if sid and name and grade and bus_no:
                try:
                    c.execute("INSERT INTO students VALUES (?,?,?,?)", (sid, name, grade, bus_no))
                    conn.commit()
                    st.success(t("تم التسجيل بنجاح!", "Registration successful!"))
                except sqlite3.IntegrityError:
                    st.warning(t("هذا الرقم مسجل مسبقًا.", "This ID is already registered."))
            else:
                st.error(t("يرجى تعبئة جميع الحقول.", "Please fill all fields."))

    # تسجيل الحضور
    elif mode == t("تسجيل حضور", "Mark Attendance"):
        sid = st.text_input(t("أدخل رقم الوزارة", "Enter Ministry ID"), key="sid_attend")
        if sid:
            c.execute("SELECT name, bus_no FROM students WHERE student_id=?", (sid,))
            student = c.fetchone()
            if student:
                name, bus_no = student
                status = st.radio(t("هل ستحضر اليوم؟", "Will you come today?"), [t("نعم", "Yes"), t("لا", "No")])
                if st.button(t("إرسال", "Submit")):
                    st_status = "Going" if status == t("نعم", "Yes") else "Not Going"
                    c.execute("INSERT INTO attendance VALUES (?,?,?,?,?)",
                              (sid, name, bus_no, st_status, datetime.date.today().isoformat()))
                    conn.commit()
                    st.success(t("تم تسجيل حضورك بنجاح!", "Attendance recorded successfully!"))
            else:
                st.error(t("الرقم غير مسجل، يرجى التسجيل أولاً.", "ID not found. Please register first."))

# ===== واجهة السائق =====
elif selected == t("🧑‍✈️ السائق", "🧑‍✈️ Driver"):
    st.header(t("تسجيل دخول السائق", "Driver Login"))
    bus_no = st.text_input(t("رقم الباص", "Bus Number"), key="driver_bus")
    password = st.text_input(t("كلمة المرور", "Password"), type="password", key="driver_pass")

    if st.button(t("دخول", "Login")):
        if bus_no in drivers and password == drivers[bus_no]:
            st.success(t("تم تسجيل الدخول بنجاح ✅", "Login successful ✅"))
            c.execute("SELECT name, status FROM attendance WHERE bus_no=? AND date=?", (bus_no, datetime.date.today().isoformat()))
            data = c.fetchall()
            if data:
                for name, status in data:
                    st.write(f"{'🟢' if status=='Going' else '🔴'} {name} — {t('قادم','Coming') if status=='Going' else t('غير قادم','Not Coming')}")
            else:
                st.info(t("لا توجد بيانات اليوم.", "No data for today."))
        else:
            st.error(t("بيانات الدخول غير صحيحة.", "Incorrect credentials."))

# ===== واجهة الإدارة =====
elif selected == t("🏫 الإدارة", "🏫 Admin"):
    st.header(t("دخول الإدارة", "Admin Login"))
    ap = st.text_input(t("كلمة المرور", "Password"), type="password", key="admin_pass")

    if ap == ADMIN_PASS:
        st.success(t("مرحبًا بك ", "Welcome "))
        c.execute("SELECT * FROM attendance")
        rows = c.fetchall()
        if rows:
            st.table(rows)
        else:
            st.info(t("لا توجد بيانات بعد.", "No data yet."))

# ===== واجهة الطقس =====
elif selected == t("🌤️ الطقس", "🌤️ Weather"):
    st.header(t("توقعات الطقس", "Weather Forecast"))
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ar"
        r = requests.get(url)
        data = r.json()
        if "list" in data:
            days = {}
            for entry in data["list"]:
                date = entry["dt_txt"].split(" ")[0]
                if date not in days:
                    days[date] = entry["main"]["temp"]

            plt.figure(figsize=(8, 4))
            plt.plot(list(days.keys()), list(days.values()), marker='o', color='orange')
            plt.title(t("درجات الحرارة القادمة", "Upcoming Temperatures"))
            plt.xticks(rotation=45)
            st.pyplot(plt)
        else:
            st.warning(t("فشل في جلب بيانات الطقس.", "Weather data unavailable."))
    except Exception as e:
        st.error(t("حدث خطأ في تحميل بيانات الطقس.", "Error loading weather data."))

# ===== الكريدتس =====
elif selected == t("💬 الكريدتس", "💬 Credits"):
    st.header(t("عن المشروع", "About the Project"))
    st.markdown("""
    **جميع الحقوق محفوظة لمدرسة المنيرة الخاصة 2025**  
    -  البرمجة والتصميم المنطقي: **إياد مصطفى**  
    -  الرسوميات والعرض: **أيمن جلال**  
    - 🏫 الإشراف الأكاديمي: **صف 10-B**  
    """)
    st.info(t("النظام لا يزال تحت التجريب وقد تحدث بعض الأخطاء.", 
              "This system is still in beta and minor issues may occur."))

