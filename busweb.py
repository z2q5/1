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
    
    /* حاوية التابز العمودية الفاخرة */
    .vertical-tab-container {
        background-color: #090d16;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #21262d;
        max-height: 400px;
        overflow-y: auto;
    }

    /* أسطر النوتات العمودية */
    .tab-step {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.1rem;
        padding: 6px 12px;
        margin-bottom: 4px;
        border-radius: 4px;
        background: #161b22;
        border-left: 3px solid #58a6ff;
        display: flex;
        justify-content: space-between;
    }
    .tab-step .step-num { color: #8b949e; font-size: 0.85rem; }
    .tab-step .string-name { color: #ff7b72; font-weight: bold; }
    .tab-step .fret-num { color: #58a6ff; font-weight: bold; }

    /* صندوق الكوردات المصاحبة */
    .chord-box {
        background: #26354a;
        border-left: 4px solid #1f6feb;
        padding: 12px;
        border-radius: 6px;
        margin: 5px 0;
        font-weight: bold;
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
    
    /* النصوص الجانبية الهادئة */
    .sub-text {
        color: #8b949e;
        font-size: 0.95rem;
    }
</style>
"""
st.markdown(modern_dark_css, unsafe_allow_html=True)

# ==========================================
# 🧠 محرك التوليد الذكي للتابز (العمودي)
# ==========================================
def generate_vertical_tab(genre, difficulty):
    """يولد خطوات عزف تتابعية عمودية واضحة جداً لكل وتر"""
    
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
    guitar_strings = ['e (High)', 'B', 'G', 'D', 'A', 'E (Low)']
    
    # توليد خطوات العزف خطوة بخطوة بالترتيب الزمني
    steps = []
    for i in range(steps_count):
        chosen_string = random.choice(guitar_strings)
        chosen_fret = random.choice(frets_pool)
        steps.append({
            "step": i + 1,
            "string": chosen_string,
            "fret": chosen_fret
        })
        
    title = f"Riff Session #{random.randint(100, 999)}"
    
    return {
        "title": title,
        "genre": genre,
        "difficulty": difficulty,
        "chords": selected_chords,
        "steps": steps
    }

# ==========================================
# 🖥️ واجهة المستخدم المحدثة (UI Layout)
# ==========================================

st.markdown("<h1>What I'm doing in my life</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>An interactive smart assistant to invent, explore, and save unique guitar tabs.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# تقسيم الشاشة الرئيسي
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
            st.session_state.current_tab_data = generate_vertical_tab(song_genre, difficulty_level)
            st.session_state.generated_count += 1
            
    with btn_col2:
        if st.button("💾 Save to Library"):
            if st.session_state.current_tab_data and st.session_state.current_tab_data not in st.session_state.saved_tabs:
                st.session_state.saved_tabs.append(st.session_state.current_tab_data)
                st.toast("Tab successfully saved to your library!", icon="✅")
            elif not st.session_state.current_tab_data:
                st.warning("Please generate a tab first before saving.")

    st.markdown("---")

    # عرض النتائج مع التابز الرأسية المقروءة
    if st.session_state.current_tab_data:
        data = st.session_state.current_tab_data
        
        st.markdown(f"### 🎵 Now Playing: {data['title']}")
        
        display_col1, display_col2 = st.columns([1, 2.5])
        
        with display_col1:
            st.markdown("##### 🎼 Background Chords")
            for chord in data['chords']:
                st.markdown(f"<div class='chord-box'>{chord}</div>", unsafe_allow_html=True)
                
        with display_col2:
            st.markdown("##### 📋 Play Order (Top to Bottom)")
            
            # بناء قائمة الخطوات الرأسية
            tab_html = "<div class='vertical-tab-container'>"
            for step in data['steps']:
                tab_html += f"""
                <div class='tab-step'>
                    <span class='step-num'>Step {step['step']}</span>
                    <span>Pluck String: <span class='string-name'>{step['string']}</span></span>
                    <span>Fret: <span class='fret-num'>{step['fret']}</span></span>
                </div>
                """
            tab_html += "</div>"
            st.markdown(tab_html, unsafe_allow_html=True)
            
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
                
                # عرض التاب العمودي داخل الأرشيف
                saved_tab_html = "<div class='vertical-tab-container' style='max-height: 250px;'>"
                for step in saved_data['steps']:
                    saved_tab_html += f"""
                    <div class='tab-step' style='font-size:0.9rem; padding:4px 8px;'>
                        <span class='step-num'>#{step['step']}</span>
                        <span>String: <span class='string-name'>{step['string']}</span></span>
                        <span>Fret: <span class='fret-num'>{step['fret']}</span></span>
                    </div>
                    """
                saved_tab_html += "</div>"
                st.markdown(saved_tab_html, unsafe_allow_html=True)
                
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
