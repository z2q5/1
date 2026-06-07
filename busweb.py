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
    .stApp {
        background-color: #0e1117;
        color: #cae1ff;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    .custom-card {
        background: #1f293d;
        border: 1px solid #2e3d52;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* صندوق التابز العمودي الحقيقي */
    .vertical-fretboard-box {
        background-color: #090d16;
        color: #58a6ff;
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #21262d;
        line-height: 1.4;
        letter-spacing: 2px;
        display: inline-block;
    }

    .chord-box {
        background: #26354a;
        border-left: 4px solid #1f6feb;
        padding: 12px;
        border-radius: 6px;
        margin: 5px 0;
        font-weight: bold;
    }
    
    .stButton>button {
        background: #1f6feb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
    }
    .stButton>button:hover {
        background: #388bfd !important;
    }
    
    .sub-text {
        color: #8b949e;
        font-size: 0.95rem;
    }
</style>
"""
st.markdown(modern_dark_css, unsafe_allow_html=True)

# ==========================================
# 🧠 محرك توليد التابز الرأسية الحقيقية
# ==========================================
def generate_real_vertical_tab(genre, difficulty):
    """يولد لوحة أوتار رأسية حقيقية تقرأ من الأعلى للأسفل"""
    
    if difficulty == "Easy":
        steps_count = 8
        frets_pool = [0, 2, 3, 5]
    elif difficulty == "Intermediate":
        steps_count = 12
        frets_pool = [0, 2, 3, 5, 7, 8]
    else: # Hard
        steps_count = 16
        frets_pool = [0, 2, 3, 5, 7, 8, 10, 12, 11]

    chords_pool = {
        "Acoustic / Indie Pop": ["G", "D", "Em", "C"],
        "Rock / Post-Punk": ["Am", "F", "C", "G"],
        "Metal / Progress": ["Em", "C5", "D5", "A5"],
        "Math Rock / Emo-Jazz": ["Cmaj7", "Bm7", "Em9", "G6"]
    }
    
    selected_chords = chords_pool.get(genre, ["G", "C"])
    
    # ترتيب الأوتار أفقياً في السطر العلوي
    strings_order = ['e', 'B', 'G', 'D', 'A', 'E']
    
    # رأس النوتة (أسماء الأوتار)
    tab_lines = []
    tab_lines.append(" ↓ Time ↓")
    tab_lines.append(" e  B  G  D  A  E")
    tab_lines.append(" |  |  |  |  |  |")
    
    # توليد النوتات خطوة بخطوة نزولاً
    for _ in range(steps_count):
        active_string = random.choice(strings_order)
        fret = str(random.choice(frets_pool))
        
        row_cells = []
        for s in strings_order:
            if s == active_string:
                # إذا كان رقم الفريت يتكون من خانتين، نضبط المسافات لتبقى الأسطر متوازية
                row_cells.append(f"{fret} " if len(fret) == 1 else f"{fret}")
            else:
                row_cells.append("| ")
                
        tab_lines.append(" " + " ".join(row_cells))
        # إضافة فاصل صغير بين الضربات لمنع التداخل
        tab_lines.append(" |  |  |  |  |  |")
        
    tab_lines.append(" ✕  ✕  ✕  ✕  ✕  ✕ (End)")
    
    title = f"Riff Session #{random.randint(100, 999)}"
    
    return {
        "title": title,
        "genre": genre,
        "difficulty": difficulty,
        "chords": selected_chords,
        "raw_tab": "\n".join(tab_lines)
    }

# ==========================================
# 🖥️ واجهة المستخدم (UI Layout)
# ==========================================

st.markdown("<h1>What I'm doing in my life</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>An interactive smart assistant to invent, explore, and save unique guitar tabs.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

main_col1, main_col2 = st.columns([2.2, 1])

with main_col1:
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
        
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🎸 Invent New Tab"):
            st.session_state.current_tab_data = generate_real_vertical_tab(song_genre, difficulty_level)
            st.session_state.generated_count += 1
            
    with btn_col2:
        if st.button("💾 Save to Library"):
            if st.session_state.current_tab_data and st.session_state.current_tab_data not in st.session_state.saved_tabs:
                st.session_state.saved_tabs.append(st.session_state.current_tab_data)
                st.toast("Tab successfully saved to your library!", icon="✅")
            elif not st.session_state.current_tab_data:
                st.warning("Please generate a tab first before saving.")

    st.markdown("---")

    # عرض النتائج الجديدة
    if st.session_state.current_tab_data:
        data = st.session_state.current_tab_data
        
        st.markdown(f"### 🎵 Now Playing: {data['title']}")
        
        display_col1, display_col2 = st.columns([1, 2.5])
        
        with display_col1:
            st.markdown("##### 🎼 Background Chords")
            for chord in data['chords']:
                st.markdown(f"<div class='chord-box'>{chord}</div>", unsafe_allow_html=True)
                
        with display_col2:
            st.markdown("##### 📋 Vertical Guitar Tab (Read Top to Bottom)")
            # عرض التاب الحقيقي بالشكل الرأسي المتقاطع
            st.markdown(f"<pre class='vertical-fretboard-box'>{data['raw_tab']}</pre>", unsafe_allow_html=True)
            
    else:
        st.markdown("<div class='custom-card' style='text-align:center;'><p class='sub-text'>Your fretboard is currently clear. Choose your preferences above and click 'Invent New Tab'.</p></div>", unsafe_allow_html=True)

with main_col2:
    st.markdown("### 📚 Saved Library")
    st.markdown(f"<p class='sub-text'>Total saved tracks: {len(st.session_state.saved_tabs)}</p>", unsafe_allow_html=True)
    
    if st.session_state.saved_tabs:
        for i, saved_data in enumerate(st.session_state.saved_tabs):
            with st.expander(f"🎸 {saved_data['title']} ({saved_data['difficulty']})"):
                st.markdown(f"**Style:** {saved_data['genre']}")
                st.markdown("**Progression:** " + " → ".join(saved_data['chords']))
                
                st.markdown(f"<pre class='vertical-fretboard-box' style='font-size:0.95rem; padding:10px;'>{saved_data['raw_tab']}</pre>", unsafe_allow_html=True)
                
                if st.button(f"Remove Track", key=f"del_{i}"):
                    st.session_state.saved_tabs.pop(i)
                    st.rerun()
    else:
        st.markdown("<p class='sub-text' style='font-style: italic;'>No saved tabs in your library yet.</p>", unsafe_allow_html=True)

# ==========================================
# ⏱️ شريط الإحصائيات السفلي
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
foot_col1, foot_col2 = st.columns(2)

with foot_col1:
    st.markdown(f"<p class='sub-text'>⚡ Session Activity: <b>{st.session_state.generated_count}</b> tabs created during this session.</p>", unsafe_allow_html=True)

with foot_col2:
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    st.markdown(f"<p class='sub-text' style='text-align: right;'>🕒 Local Studio Time: <b>{current_time}</b></p>", unsafe_allow_html=True)
