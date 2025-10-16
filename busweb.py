import streamlit as st
import json, os
import pandas as pd
import plotly.express as px

# -------------------------------
# إعدادات عامة
# -------------------------------
st.set_page_config(page_title="Bus Attendance 2025", layout="wide")

# ملف قاعدة البيانات
DATA_FILE = "attendance.json"

# إنشاء ملف قاعدة البيانات إذا لم يكن موجودًا
if not os.path.exists(DATA_FILE):
    data = {
        "students": {
            "777442": {"name": "Ahmed", "bus": "1", "status": "Not set"},
            "777443": {"name": "Mohammed", "bus": "1", "status": "Not set"},
            "777444": {"name": "Sara", "bus": "2", "status": "Not set"},
            "777445": {"name": "Laila", "bus": "3", "status": "Not set"},
            "777446": {"name": "Hassan", "bus": "2", "status": "Not set"},
            "777447": {"name": "Mona", "bus": "1", "status": "Not set"},
            "777448": {"name": "Khalid", "bus": "3", "status": "Not set"},
            "777449": {"name": "Noura", "bus": "1", "status": "Not set"},
            "777450": {"name": "Omar", "bus": "2", "status": "Not set"},
            "777451": {"name": "Fatima", "bus": "3", "status": "Not set"},
        }
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# تحميل البيانات
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# حفظ البيانات
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------------
# إعداد اللغة
# -------------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

lang = st.session_state.lang

texts = {
    "ar": {
        "title": "نظام حضور الباص - مدرسة المنيرة الخاصة",
        "student": "دخول الطالب",
        "driver": "دخول السائق",
        "admin": "الإدارة",
        "student_id": "أدخل رقم الوزارة",
        "go": "سأحضر اليوم",
        "nogo": "لن أحضر اليوم",
        "bus_number": "رقم الباص",
        "password": "كلمة المرور",
        "login": "تسجيل الدخول",
        "back": "رجوع",
        "language": "English",
        "theme": "تغيير الثيم",
        "footer": "© 2025 مدرسة المنيرة الخاصة — تطوير: إياد مصطفى (10-B) | تصميم: أيمن جلال",
        "going": "قادم",
        "not_going": "غير قادم",
        "not_set": "لم يحدد",
        "admin_pass": "كلمة مرور الإدارة غير صحيحة!",
        "admin_title": "لوحة تحكم الإدارة",
        "refresh": "تحديث",
        "download": "تنزيل ملف Excel",
    },
    "en": {
        "title": "Bus Attendance System - Al Munira Private School",
        "student": "Student Login",
        "driver": "Driver Login",
        "admin": "Admin Panel",
        "student_id": "Enter Ministry ID",
        "go": "Coming Today",
        "nogo": "Not Coming",
        "bus_number": "Bus Number",
        "password": "Password",
        "login": "Login",
        "back": "Back",
        "language": "العربية",
        "theme": "Toggle Theme",
        "footer": "© 2025 Al Munira Private School — Developed by Eyad Mustafa (10-B) | Design by Ayman Galal",
        "going": "Going",
        "not_going": "Not Going",
        "not_set": "Not set",
        "admin_pass": "Invalid admin password!",
        "admin_title": "Administration Panel",
        "refresh": "Refresh",
        "download": "Download Excel File",
    }
}

t = texts[lang]

# -------------------------------
# واجهة عامة
# -------------------------------
st.title(t["title"])

# أزرار اللغة والثيم
col1, col2 = st.columns(2)
if col1.button(t["language"]):
    st.session_state.lang = "en" if lang == "ar" else "ar"
    st.rerun()
theme = col2.selectbox(t["theme"], ["Light", "Dark"])
if theme == "Dark":
    st.markdown("<style>body {background-color: #121212; color: white;}</style>", unsafe_allow_html=True)

# -------------------------------
# الشاشات
# -------------------------------
page = st.sidebar.radio("", [t["student"], t["driver"], t["admin"]])

data = load_data()

if page == t["student"]:
    student_id = st.text_input(t["student_id"], key="student_id_input")
    if st.button(t["go"]):
        if student_id in data["students"]:
            data["students"][student_id]["status"] = "Going"
            save_data(data)
            st.success(f"{data['students'][student_id]['name']} {t['going']}")
        else:
            st.error("رقم غير صحيح!")
    if st.button(t["nogo"]):
        if student_id in data["students"]:
            data["students"][student_id]["status"] = "Not Going"
            save_data(data)
            st.warning(f"{data['students'][student_id]['name']} {t['not_going']}")
        else:
            st.error("رقم غير صحيح!")

elif page == t["driver"]:
    bus_number = st.text_input(t["bus_number"], key="bus_num")
    password = st.text_input(t["password"], type="password", key="bus_pass")
    if st.button(t["login"], key="driver_login"):
        if password == "1111" and bus_number == "1" or password == "2222" and bus_number == "2" or password == "3333" and bus_number == "3":
            students = [s for s in data["students"].values() if s["bus"] == bus_number]
            df = pd.DataFrame(students)
            st.table(df[["name", "status"]])
        else:
            st.error("بيانات السائق غير صحيحة!")

elif page == t["admin"]:
    admin_pass = st.text_input(t["password"], type="password", key="admin_login")
    if admin_pass == "admin123":
        st.subheader(t["admin_title"])
        df = pd.DataFrame(data["students"]).T
        st.dataframe(df)
        fig = px.pie(df, names="status", title="Attendance Status Overview")
        st.plotly_chart(fig)
        if st.button(t["refresh"]):
            st.rerun()
        st.download_button(label=t["download"], data=df.to_csv().encode('utf-8'), file_name="attendance.csv")
    elif admin_pass:
        st.error(t["admin_pass"])

st.markdown(f"<hr><center><small>{t['footer']}</small></center>", unsafe_allow_html=True)
