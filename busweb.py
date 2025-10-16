import streamlit as st
import pandas as pd
import json, os
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="Bus Attendance 2025", layout="wide", page_icon="🚌")

# قاعدة البيانات
DATA_FILE = "attendance.json"
if not os.path.exists(DATA_FILE):
    data = {"students": {}}
    with open(DATA_FILE, "w") as f: json.dump(data, f)

# تحميل البيانات
def load_data():
    with open(DATA_FILE, "r") as f: return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# ترجمة النصوص
if "lang" not in st.session_state: st.session_state.lang = "ar"
lang = st.session_state.lang

texts = {
    "ar": {
        "title": "نظام حضور الباص 2025",
        "welcome": "مرحباً بكم في نظام حضور الباص الخاص بمدرسة المنيرة الخاصة",
        "student": "الطالب",
        "driver": "السائق",
        "admin": "الإدارة",
        "id": "رقم الوزارة",
        "go": "سأحضر اليوم",
        "nogo": "لن أحضر اليوم",
        "bus": "رقم الباص",
        "pass": "كلمة المرور",
        "login": "تسجيل الدخول",
        "back": "رجوع",
        "footer": "© 2025 مدرسة المنيرة الخاصة — الكود: إياد مصطفى (10-B) | التصميم: أيمن جلال",
        "lang": "English",
        "theme": "تبديل الثيم",
        "wrong": "البيانات غير صحيحة!",
        "admin_panel": "لوحة تحكم الإدارة",
        "chart": "نسبة الحضور والغياب",
        "download": "تنزيل ملف Excel",
        "students": "قائمة الطلاب",
        "bus_overview": "نظرة على الباصات",
        "coming": "قادم",
        "notcoming": "غير قادم",
    },
    "en": {
        "title": "Bus Attendance System 2025",
        "welcome": "Welcome to Al Munira Private School Bus Attendance System",
        "student": "Student",
        "driver": "Driver",
        "admin": "Administration",
        "id": "Ministry ID",
        "go": "I'm Coming Today",
        "nogo": "Not Coming",
        "bus": "Bus Number",
        "pass": "Password",
        "login": "Login",
        "back": "Back",
        "footer": "© 2025 Al Munira Private School — Code: Eyad Mustafa (10-B) | Design: Ayman Jalal",
        "lang": "العربية",
        "theme": "Toggle Theme",
        "wrong": "Invalid information!",
        "admin_panel": "Admin Dashboard",
        "chart": "Attendance Overview",
        "download": "Download Excel",
        "students": "Students List",
        "bus_overview": "Bus Overview",
        "coming": "Coming",
        "notcoming": "Not Coming",
    }
}
t = texts[lang]

# زر اللغة والثيم
col1, col2 = st.columns([1, 1])
if col1.button(t["lang"]):
    st.session_state.lang = "en" if lang == "ar" else "ar"
    st.rerun()

theme = col2.radio(t["theme"], ["Light", "Dark"], horizontal=True)
if theme == "Dark":
    st.markdown("""
    <style>
        body {background-color:#0e1117; color:white;}
        .stButton>button {background-color:#1f77b4; color:white;}
    </style>""", unsafe_allow_html=True)

# عرض العنوان
st.markdown(f"<h1 style='text-align:center; color:#2b5876;'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>{t['welcome']}</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Tabs
tab = st.tabs([t["student"], t["driver"], t["admin"]])
data = load_data()

# ---------------- الطالب ----------------
with tab[0]:
    sid = st.text_input(t["id"])
    if st.button(t["go"], use_container_width=True):
        if sid:
            data["students"].setdefault(sid, {"bus": "1", "status": t["coming"]})
            data["students"][sid]["status"] = t["coming"]
            save_data(data)
            st.success(f"{t['coming']} ✅")
    if st.button(t["nogo"], use_container_width=True):
        if sid:
            data["students"].setdefault(sid, {"bus": "1", "status": t["notcoming"]})
            data["students"][sid]["status"] = t["notcoming"]
            save_data(data)
            st.warning(f"{t['notcoming']} 🚫")

# ---------------- السائق ----------------
with tab[1]:
    bus = st.text_input(t["bus"])
    p = st.text_input(t["pass"], type="password")
    if st.button(t["login"], use_container_width=True):
        if (bus, p) in [("1", "1111"), ("2", "2222"), ("3", "3333")]:
            df = pd.DataFrame(data["students"]).T
            df = df[df["bus"] == bus]
            st.subheader(f"{t['bus']} {bus}")
            st.table(df)
        else:
            st.error(t["wrong"])

# ---------------- الإدارة ----------------
with tab[2]:
    ap = st.text_input(t["pass"], type="password")
    if ap == "admin123":
        df = pd.DataFrame(data["students"]).T
        st.subheader(t["admin_panel"])
        st.table(df)
        fig = px.pie(df, names="status", title=t["chart"])
        st.plotly_chart(fig)
        st.download_button(label=t["download"], data=df.to_csv().encode('utf-8'), file_name="attendance.csv")
    elif ap:
        st.error(t["wrong"])

st.markdown(f"<hr><center><small>{t['footer']}</small></center>", unsafe_allow_html=True)
