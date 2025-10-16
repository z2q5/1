import streamlit as st
import sqlite3
import datetime
import requests
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

# إعداد قاعدة البيانات
conn = sqlite3.connect('bus_data.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS attendance
             (student_id TEXT, name TEXT, bus_no TEXT, status TEXT, date TEXT)''')
conn.commit()

# مفتاح API للطقس
WEATHER_API_KEY = "a90d21ff18d439b21a8a6795ada3e371"
CITY = "Abu Dhabi"

# إعداد اللغة
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

def t(ar, en):
    return ar if st.session_state.lang == "ar" else en

# الثيم
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown(
            """
            <style>
            body {background-color: #121212; color: white;}
            </style>
            """,
            unsafe_allow_html=True
        )

apply_theme()

# الواجهة العلوية
with st.sidebar:
    st.title("🚍 " + t("نظام حضور الباص", "Bus Attendance System"))
    st.markdown("**School: المنيرة الخاصة**")
    st.markdown("**Project by صف 10-B**")
    st.markdown("---")
    lang_choice = st.radio(t("اللغة:", "Language:"), ["العربية", "English"])
    st.session_state.lang = "ar" if lang_choice == "العربية" else "en"

    theme_choice = st.radio(t("الثيم:", "Theme:"), ["فاتح", "داكن"] if st.session_state.lang=="ar" else ["Light", "Dark"])
    st.session_state.theme = "dark" if theme_choice in ["داكن", "Dark"] else "light"
    st.markdown("---")

# التنقل بين الصفحات
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

# قائمة الطلاب
students = {
    "777442": {"name": "Ahmed", "bus": "1"},
    "777443": {"name": "Mohammed", "bus": "1"},
    "777444": {"name": "Sara", "bus": "2"},
    "777445": {"name": "Laila", "bus": "3"},
    "777446": {"name": "Hassan", "bus": "2"},
    "777447": {"name": "Mona", "bus": "1"},
    "777448": {"name": "Khalid", "bus": "3"},
    "777449": {"name": "Noura", "bus": "1"},
    "777450": {"name": "Omar", "bus": "2"},
    "777451": {"name": "Fatima", "bus": "3"},
}

# باسورد السائقين
drivers = {"1": "1111", "2": "2222", "3": "3333"}

# كلمة مرور الإدارة
ADMIN_PASS = "admin2025"

# واجهة الطالب
if selected == t("👩‍🎓 الطالب", "👩‍🎓 Student"):
    st.header(t("تسجيل الحضور", "Mark Attendance"))
    sid = st.text_input(t("أدخل رقم الوزارة", "Enter Ministry ID"), key="student_id")
    if sid and sid in students:
        name = students[sid]["name"]
        bus = students[sid]["bus"]
        st.success(f"{t('الطالب', 'Student')} {name} - {t('باص', 'Bus')} {bus}")
        status = st.radio(t("هل ستحضر اليوم؟", "Will you come today?"), [t("نعم", "Yes"), t("لا", "No")])
        if st.button(t("إرسال", "Submit")):
            c.execute("INSERT INTO attendance VALUES (?,?,?,?,?)",
                      (sid, name, bus, "Going" if status == t("نعم", "Yes") else "Not Going",
                       datetime.date.today().isoformat()))
            conn.commit()
            st.success(t("تم تسجيل حضورك!", "Attendance recorded!"))
    elif sid:
        st.error(t("رقم الوزارة غير صحيح", "Invalid ID"))

# واجهة السائق
elif selected == t("🧑‍✈️ السائق", "🧑‍✈️ Driver"):
    st.header(t("تسجيل دخول السائق", "Driver Login"))
    bus_no = st.text_input(t("رقم الباص", "Bus Number"), key="bus_no")
    password = st.text_input(t("كلمة المرور", "Password"), type="password", key="bus_pass")

    if st.button(t("دخول", "Login")):
        if bus_no in drivers and password == drivers[bus_no]:
            st.success(t("تم تسجيل الدخول", "Logged in"))
            st.subheader(f"{t('حالة الطلاب في الباص', 'Students in Bus')} {bus_no}")
            c.execute("SELECT name, status FROM attendance WHERE bus_no=? AND date=?",
                      (bus_no, datetime.date.today().isoformat()))
            data = c.fetchall()
            if data:
                for row in data:
                    st.write(f"👤 {row[0]} — {('✅ قادم' if row[1]=='Going' else '❌ غير قادم')}")
            else:
                st.info(t("لا توجد بيانات اليوم.", "No data for today."))
        else:
            st.error(t("معلومات غير صحيحة", "Incorrect credentials"))

# واجهة الإدارة
elif selected == t("🏫 الإدارة", "🏫 Admin"):
    st.header(t("تسجيل دخول الإدارة", "Admin Login"))
    ap = st.text_input(t("كلمة المرور", "Password"), type="password", key="admin_pass")

    if ap == ADMIN_PASS:
        st.success(t("مرحبًا بالإدارة", "Welcome Admin"))
        st.subheader(t("سجل الحضور الكامل", "Full Attendance Log"))
        df = st.session_state.get("attendance_df")
        c.execute("SELECT * FROM attendance")
        rows = c.fetchall()
        if rows:
            st.table(rows)
        else:
            st.info(t("لا توجد بيانات بعد", "No attendance yet"))

# واجهة الطقس
elif selected == t("🌤️ الطقس", "🌤️ Weather"):
    st.header(t("توقعات الطقس في أبوظبي", "Weather Forecast in Abu Dhabi"))
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ar"
    r = requests.get(url)
    data = r.json()

    days = {}
    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        if date not in days:
            days[date] = entry["main"]["temp"]

    plt.figure(figsize=(8, 4))
    plt.plot(list(days.keys()), list(days.values()), marker='o')
    plt.title(t("درجات الحرارة المتوقعة", "Expected Temperature"))
    plt.xticks(rotation=45)
    st.pyplot(plt)

    st.info(t("الأيام ذات الحرارة العالية قد تشهد غيابًا أكبر.", "High-temp days may have more absences."))

# الكريدتس
elif selected == t("💬 الكريدتس", "💬 Credits"):
    st.header(t("عن المشروع", "About the Project"))
    st.markdown("""
    **جميع الحقوق محفوظة لمدرسة المنيرة الخاصة 2025**  
    - 👑 البرمجة والتصميم المنطقي: **إياد مصطفى**  
    - 🎨 الرسوميات والعرض: **أيمن جلال**  
    - 🏫 الإشراف الأكاديمي: **صف 10-B**
    """)
    st.markdown("---")
    st.info(t("هذا النظام لا يزال تحت التجريب وقد تحدث بعض الأخطاء.", 
              "This system is under testing and errors may occur."))
