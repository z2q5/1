import streamlit as st
import random
import datetime

# ==========================================
# 🧩 الإعدادات العامة وحالة الجلسة
# ==========================================
st.set_page_config(
    page_title="What I'm doing in my life",
    page_icon="🎸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تهيئة المتغيرات في الجلسة
if "saved_tabs" not in st.session_state:
    st.session_state.saved_tabs = []
if "current_tab_data" not in st.session_state:
    st.session_state.current_tab_data = None
if "generated_count" not in st.session_state:
    st.session_state.generated_count = 0

# ==========================================
# 🎨 التنسيق العصري والأنيق (Modern Dark UI)
# ==========================================
modern_dark_css = """
<style>
    /* الخلفية العامة والخطوط المريحة */
    .stApp {
        background-color: #0e1117;
        color: #cae1ff;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* العناوين الاحترافية */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
    }
    
    /* بطاقات العرض الأنيقة */
    .custom-card {
        background: #1f293d;
        border: 1px solid #2e3d52;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    
    /* صندوق التابز الفاخر */
    .tab-container {
        background-color: #090d16;
        color: #58a6ff; /* أزرق مريح للعين وعالي الوضوح */
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        padding: 18px;
        border-radius: 8px;
        border: 1px solid #21262d;
        white-space: pre;
        overflow-x: auto;
        line-height: 1.6;
        font-size: 1.1rem;
    }

    /* صندوق الكوردات المصاحبة */
    .chord-box {
        background: #26354a;
        border-left: 4px solid #1f6feb;
        padding: 12px;
        border-radius: 6px;
        margin: 5px 0;
    }
    
    /* الأزرار العصرية */
    .stButton>button {
        background: #1f6feb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: background 0.2s ease, transform 0.1s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background: #388bfd !important;
        transform: translateY(-1px);
    }
    .stButton>button:active {
        transform: translateY(1px);
    }
    
    /* النصوص الجانبية الهادئة */
    .sub-text {
        color: #8b949e;
        font-size: 0.95rem;
    }
</style>
"""
st.markdown(modern_dark_css, unsafe_allow_html=True)

# ==========================================
# 🧠 محرك التوليد الذكي للتابز والكوردات
# ==========================================
def generate_guitar_tab(genre, difficulty):
    """يولد تابز قيتار وكوردات متناسقة بناءً على الخيارات"""
    
    if difficulty == "Easy":
        length = 8
        frets = [0, 2, 3, 5, 0, 3, 2, 0]
    elif difficulty == "Intermediate":
        length = 12
        frets = [0, 2, 3, 5, 7, 8, 7, 5, 3, 2, 0, 0]
    else: # Hard
        length = 16
        frets = [0, 2, 3, 5, 7, 8, 10, 12, 11, 7, 5, 4, 2, 3, 2, 0]

    # كوردات احترافية حسب النمط الموسيقي المختار
    chords_pool = {
        "Rock / Post-Punk": ["Am", "G", "F", "C", "Em"],
        "Metal / Progress": ["Em", "C5", "D5", "A5", "F#5"],
        "Math Rock / Emo-Jazz": ["Cmaj7", "Bm7", "Em9", "G6", "Am9"],
        "Acoustic / Indie Pop": ["G", "D", "Em", "C", "Am"]
    }
    
    selected_chords = chords_pool.get(genre, ["G", "C"])
    
    # بناء أسطر التابز للأوتار الستة
    strings = { 'E': ["-"], 'A': ["-"], 'D': ["-"], 'G': ["-"], 'B': ["-"], 'e': ["-"] }
    
    for _ in range(length):
        fret = str(random.choice(frets))
        active_string = random.choice(['E', 'A', 'D', 'G', 'B', 'e'])
        
        for s in strings:
            if s == active_string:
                strings[s].append(fret + "-")
            else:
                strings[s].append("-" * (len(fret) + 1))
                
        for s in strings:
            strings[s].append("-")

    # توليد التاب كأوتار منفصلة للعرض المرن
    tab_lines = {}
    for s in ['e', 'B', 'G', 'D', 'A', 'E']:
        tab_lines[s] = f"{s}|{''.join(strings[s])}"
        
    title = f"Composition No. {random.randint(100, 999)}"
    
    return {
        "title": title,
        "genre": genre,
        "difficulty": difficulty,
        "chords": selected_chords,
        "tab_lines": tab_lines
    }

# ==========================================
# 🖥️ واجهة المستخدم المحدثة (UI Layout)
# ==========================================

st.markdown("<h1>What I'm doing in my life</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>An interactive smart assistant to invent, explore, and save unique guitar tabs.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# تقسيم الشاشة الرئيسي: مساحة العمل على اليسار، الأرشيف على اليمين
main_col1, main_col2 = st.columns([2.2, 1])

with main_col1:
    # لوحة التحكم والإعدادات
    st.markdown("### ⚙️ Generation Settings")
    
    config_col1, config_col2 = st.columns(2)
    with config_col1:
        song_genre = st.selectbox(
            "Song Style / Genre:",
            ["Acoustic / Indie Pop", "Rock / Post-Punk", "Metal / Progress", "Math Rock / Emo-Jazz"]
        )
    with config_col2:
        difficulty_level = st.select_slider(
            "Difficulty Level:",
            options=["Easy", "Intermediate", "Hard"]
        )
        
    # أزرار التشغيل والحفظ
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🎸 Invent New Tab"):
            st.session_state.current_tab_data = generate_guitar_tab(song_genre, difficulty_level)
            st.session_state.generated_count += 1
            
    with btn_col2:
        if st.button("💾 Save to Library"):
            if st.session_state.current_tab_data and st.session_state.current_tab_data not in st.session_state.saved_tabs:
                st.session_state.saved_tabs.append(st.session_state.current_tab_data)
                st.toast("Tab successfully saved to your library!", icon="✅")
            elif not st.session_state.current_tab_data:
                st.warning("Please generate a tab first before saving.")

    st.markdown("---")

    # عرض النتائج: فصل الكوردات في جهة والتابز في جهة داخل كرت العرض
    if st.session_state.current_tab_data:
        data = st.session_state.current_tab_data
        
        st.markdown(f"### 🎵 Now Playing: {data['title']}")
        
        # إنشاء عمودين داخل كرت العرض: عمود للكوردات وعمود للتابز
        display_col1, display_col2 = st.columns([1, 3])
        
        with display_col1:
            st.markdown("##### 🎼 Chords")
            for chord in data['chords']:
                st.markdown(f"<div class='chord-box'><b>{chord}</b></div>", unsafe_allow_html=True)
                
        with display_col2:
            st.markdown("##### 📋 Guitar Tabs")
            # تجميع أسطر التابز
            full_tab_text = "\n".join([data['tab_lines'][s] for s in ['e', 'B', 'G', 'D', 'A', 'E']])
            st.markdown(f"<pre class='tab-container'>{full_tab_text}</pre>", unsafe_allow_html=True)
            
    else:
        st.markdown("<div class='custom-card' style='text-align:center;'><p class='sub-text'>Your fretboard is currently clear. Choose your preferences above and click 'Invent New Tab'.</p></div>", unsafe_allow_html=True)

with main_col2:
    st.markdown("### 📚 Saved Library")
    st.markdown(f"<p class='sub-text'>Total saved tracks: {len(st.session_state.saved_tabs)}</p>", unsafe_allow_html=True)
    
    if st.session_state.saved_tabs:
        for i, saved_data in enumerate(st.session_state.saved_tabs):
            with st.expander(f"🎸 {saved_data['title']} ({saved_data['difficulty']})"):
                st.markdown(f"**Style:** {saved_data['genre']}")
                st.markdown("**Suggested Progression:** " + " → ".join(saved_data['chords']))
                
                # تجميع التاب المصغر داخل الأرشيف
                saved_tab_text = "\n".join([saved_data['tab_lines'][s] for s in ['e', 'B', 'G', 'D', 'A', 'E']])
                st.markdown(f"<pre class='tab-container' style='font-size:0.85rem; padding:10px;'>{saved_tab_text}</pre>", unsafe_allow_html=True)
                
                if st.button(f"Remove Track", key=f"del_{i}"):
                    st.session_state.saved_tabs.pop(i)
                    st.rerun()
    else:
        st.markdown("<p class='sub-text' style='font-style: italic;'>No saved tabs in your library yet.</p>", unsafe_allow_html=True)

# ==========================================
# ⏱️ شريط الإحصائيات السفلي الأنيق
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
foot_col1, foot_col2 = st.columns(2)

with foot_col1:
    st.markdown(f"<p class='sub-text'>⚡ Session Activity: <b>{st.session_state.generated_count}</b> tabs created during this session.</p>", unsafe_allow_html=True)

with foot_col2:
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    st.markdown(f"<p class='sub-text' style='text-align: right;'>🕒 Local Studio Time: <b>{current_time}</b></p>", unsafe_allow_html=True)
