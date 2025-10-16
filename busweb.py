import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_option_menu import option_menu

# إعداد الصفحة
st.set_page_config(page_title="Bus Attendance 2025", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------------------------
# بيانات الطلاب الأولية
# ---------------------------------------------
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame([
        {"id": "777442", "name": "Ahmed", "bus": "1", "status": "Not Set"},
        {"id": "777443", "name": "Mohammed", "bus": "1", "status": "Not Set"},
        {"id": "777444", "name": "Sara", "bus": "2", "status": "Not Set"},
        {"id": "777445", "name": "Laila", "bus": "3", "status": "Not Set"},
    ])

if "theme" not in st.session_state:
    st.session_state.theme = "light"

# ---------------------------------------------
# الثيمات الحديثة
# ---------------------------------------------
def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>
        body { background-color: #0E1117; color: #FAFAFA; }
        .stButton>button { background-color: #1E88E5; color: white; border-radius: 8px; font-weight: 600; }
        .stSelectbox, .stTextInput>div>div>input { background-color: #1C1C1C !important; color: #FAFAFA !important; border-radius: 8px; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        body { background-color: #F4F6FB; color: #222222; }
        .stButton>button { background-color: #1565C0; color: white; border-radius: 8px; font-weight: 600; }
        .stSelectbox, .stTextInput>div>div>input { background-color: white !important; border-radius: 8px; }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

# ---------------------------------------------
# شريط التنقل
# ---------------------------------------------
selected = option_menu(
    None, ["Student", "Driver", "Admin", "About", "Credits"],
    icons=["person", "bus-front", "gear", "info-circle", "award"],
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#E3F2FD" if st.session_state.theme == "light" else "#212121"},
        "icon": {"color": "#1565C0", "font-size": "20px"},
        "nav-link": {"font-size": "17px", "text-align": "center", "margin": "0px"},
        "nav-link-selected": {"background-color": "#1565C0", "color": "white"},
    },
)

# ---------------------------------------------
# واجهة الطالب
# ---------------------------------------------
if selected == "Student":
    st.header("🎓 Student Login")
    sid = st.text_input("Student ID:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Coming"):
            df = st.session_state.students
            if sid in list(df["id"]):
                df.loc[df["id"] == sid, "status"] = "Coming"
                st.success("Marked as Coming")
            else:
                st.error("Invalid ID")
    with col2:
        if st.button("❌ Not Coming"):
            df = st.session_state.students
            if sid in list(df["id"]):
                df.loc[df["id"] == sid, "status"] = "Not Coming"
                st.warning("Marked as Not Coming")
            else:
                st.error("Invalid ID")

# ---------------------------------------------
# واجهة السائق
# ---------------------------------------------
if selected == "Driver":
    st.header("🚌 Driver View")
    bus_num = st.text_input("Bus Number:")
    if st.button("Show Students"):
        df = st.session_state.students
        df_bus = df[df["bus"] == bus_num]
        if not df_bus.empty:
            st.table(df_bus[["id", "name", "status"]])
            counts = df_bus["status"].value_counts()
            st.bar_chart(counts)
        else:
            st.error("No students found for this bus.")

# ---------------------------------------------
# واجهة الإدارة
# ---------------------------------------------
if selected == "Admin":
    st.header("⚙️ Admin Panel")
    password = st.text_input("Admin Password", type="password", key="adm")
    if password == "admin2025":
        st.success("Welcome, Admin!")
        st.dataframe(st.session_state.students)
    elif password:
        st.error("Wrong password")

# ---------------------------------------------
# نبذة
# ---------------------------------------------
if selected == "About":
    st.header("About the Project")
    st.write("""
    **Bus Attendance 2025** is a smart attendance system designed for schools.
    It allows students to easily mark their attendance, while bus drivers and
    school admins can track who is coming or not each day.
    """)

# ---------------------------------------------
# الكريدتس
# ---------------------------------------------
if selected == "Credits":
    st.header("Credits")
    st.markdown("""
    **Project:** Bus Attendance System 2025  
    **Programming:** Eyad Mustafa  
    **Graphics:** Ayman Jalal  
    **School:** Al Munira Private School - Grade 10-B  
    """)
    st.markdown("<small>All Rights Reserved © 2025</small>", unsafe_allow_html=True)

# ---------------------------------------------
# الثيم سويتشر
# ---------------------------------------------
st.sidebar.markdown("### Theme")
if st.sidebar.button("Toggle Theme"):
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.rerun()

