import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from streamlit_option_menu import option_menu

# إعداد الصفحة
st.set_page_config(page_title="Bus Attendance System", page_icon="🚌", layout="wide")

# ===================== الحالة العامة =====================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["ID", "Name", "Bus", "Status", "Time"])

def t(ar, en):
    return ar if st.session_state.lang == "ar" else en

# ===================== إعداد الثيم =====================
def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>
        body { background-color: #0e1117; color: white; }
        .stButton button { background-color: #1e90ff; color: white; border-radius: 10px; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stButton button { background-color: #0078d7; color: white; border-radius: 10px; }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

# ===================== الشريط العلوي =====================
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("🚌 " + t("نظام حضور الباص الذكي", "Smart Bus Attendance System"))
with col2:
    lang = st.selectbox("🌐 " + t("اللغة", "Language"), ["ar", "en"], index=0 if st.session_state.lang == "ar" else 1, key="lang_select")
    st.session_state.lang = lang
with col3:
    theme = st.selectbox("🎨 " + t("الثيم", "Theme"), ["light", "dark"], index=0 if st.session_state.theme == "light" else 1, key="theme_select")
    st.session_state.theme = theme
apply_theme()

# ===================== القائمة =====================
selected = option_menu(
    menu_title=None,
    options=[t("👨‍🎓 الطالب", "👨‍🎓 Student"),
             t("🚍 السائق", "🚍 Driver"),
             t("🏫 الإدارة", "🏫 Admin"),
             t("💡 حول", "💡 About")],
    icons=["person", "truck", "gear", "info-circle"],
    orientation="horizontal",
)

# ===================== واجهة الطالب =====================
if selected.endswith("الطالب") or selected.endswith("Student"):
    st.subheader("👨‍🎓 " + t("تسجيل حالة الحضور", "Mark Attendance"))
    sid = st.text_input(t("رقم الطالب", "Student ID"), key="sid_input")
    sname = st.text_input(t("(باللغة الانجلزية )اسم الطالب", "Student Name"), key="sname_input")
    bus = st.selectbox(t("رقم الباص", "Bus Number"), ["1", "2", "3"], key="bus_select")

    colA, colB = st.columns(2)
    with colA:
        if st.button("✅ " + t("سآتي اليوم", "Coming Today"), key="btn_come"):
            st.session_state.data.loc[len(st.session_state.data)] = [sid, sname, bus, "Coming", datetime.now().strftime("%H:%M")]
            st.success(t("تم تسجيل حضورك بنجاح!", "Your attendance has been marked!"))
    with colB:
        if st.button("❌ " + t("لن آتي اليوم", "Not Coming Today"), key="btn_nocome"):
            st.session_state.data.loc[len(st.session_state.data)] = [sid, sname, bus, "Not Coming", datetime.now().strftime("%H:%M")]
            st.warning(t("تم تسجيل غيابك!", "Your absence has been marked!"))

# ===================== واجهة السائق =====================
elif selected.endswith("السائق") or selected.endswith("Driver"):
    st.subheader("🚍 " + t("عرض حالة الطلاب", "View Bus Students"))
    bus_num = st.selectbox(t("اختر رقم الباص", "Select Bus Number"), ["1", "2", "3"], key="driver_bus_select")
    df_bus = st.session_state.data[st.session_state.data["Bus"] == bus_num]

    if df_bus.empty:
        st.info(t("لا توجد بيانات حتى الآن.", "No data available yet."))
    else:
        st.dataframe(df_bus, use_container_width=True)
        coming = len(df_bus[df_bus["Status"] == "Coming"])
        notcoming = len(df_bus[df_bus["Status"] == "Not Coming"])
        st.metric(t("القادمون", "Coming Students"), coming)
        st.metric(t("غير القادمون", "Not Coming Students"), notcoming)

# ===================== واجهة الإدارة =====================
elif selected.endswith("الإدارة") or selected.endswith("Admin"):
    st.subheader("🏫 " + t("لوحة تحكم الإدارة", "Admin Panel"))
    ap = st.text_input(t("كلمة المرور", "Password"), type="password", key="admin_pass_input")

    if ap == "admin123":
        st.success(t("تم تسجيل الدخول بنجاح!", "Logged in successfully!"))
        df = st.session_state.data
        st.dataframe(df, use_container_width=True)

        # إحصائيات بيانية
        if not df.empty:
            st.markdown("### 📊 " + t("الإحصائيات العامة", "Statistics"))
            stats = df["Status"].value_counts()
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.pie(stats, labels=stats.index, autopct='%1.1f%%', startangle=90, colors=["#4CAF50", "#F44336"])
            ax.axis("equal")
            st.pyplot(fig)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 " + t("تحميل السجلات", "Download Records"), csv, "attendance.csv")
    else:
        st.warning(t("أدخل كلمة مرور صحيحة (admin123)", "Enter correct password (admin123)"))

# ===================== واجهة حول / Credits =====================
elif selected.endswith("حول") or selected.endswith("About"):
    st.subheader("💡 " + t("حول المشروع", "About the Project"))
    st.markdown(f"""
    ### 🏫 {t("مدرسة المنيرة الخاصة", "Al Munira Private School")}
    **{t("مشروع نظام حضور الباص الذكي 2025", "Smart Bus Attendance Project 2025")}**

    👨‍💻 **{t("البرمجة:", "Coding:")}** إياد مصطفى  
    🎨 **{t("الرسوميات:", "Graphics:")}** أيمن جلال  
    🧑‍🏫 **{t("الصف:", "Class:")}** 10-B  
    ⚙️ **{t("جميع الحقوق محفوظة © 2025", "All rights reserved © 2025")}**

    ---
    🧠 {t("النسخة التجريبية • تحت التطوير المستمر", "Beta version • Constantly improving")}
    """)

st.markdown("---")
st.caption("🚧 " + t("النسخة التجريبية • الإصدار النهائي 2025", "Beta Version • Final Edition 2025"))

