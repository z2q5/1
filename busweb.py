import streamlit as st
import random
import datetime

# ==========================================
# 🧩 الإعدادات العامة وحالة الجلسة (Session State)
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
if "current_tab" not in st.session_state:
    st.session_state.current_tab = None
if "generated_count" not in st.session_state:
    st.session_state.generated_count = 0

# ==========================================
# 🎨 التنسيق والتأثيرات الكئيبة (CSS)
# ==========================================
dark_theme_css = """
<style>
    /* الخلفية العامة والألوان */
    .stApp {
        background: linear-gradient(180deg, #0d0d0d 0%, #1a1a1a 100%);
        color: #b3b3b3;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* العناوين */
    h1, h2, h3 {
        color: #8c0000 !important; /* أحمر داكن/دموي */
        text-shadow: 2px 2px 4px #000000;
        letter-spacing: 2px;
    }
    
    /* البطاقات الشفافة المظلمة */
    .gothic-card {
        background: rgba(20, 20, 20, 0.75);
        border: 1px solid #333333;
        border-left: 4px solid #8c0000;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.7);
    }
    
    /* التابز (صندوق النوتة) */
    .tab-display {
        background-color: #050505;
        color: #00ff66; /* أخضر قديم مثل شاشات الاختراق أو أجهزة الرادار */
        font-family: 'Courier New', monospace;
        padding: 15px;
        border-radius: 4px;
        border: 1px dashed #444;
        white-space: pre-wrap;
        overflow-x: auto;
        line-height: 1.5;
    }
    
    /* الأزرار */
    .stButton>button {
        background-color: #262626 !important;
        color: #d9d9d9 !important;
        border: 1px solid #595959 !important;
        border-radius: 4px !important;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #8c0000 !important;
        color: #ffffff !important;
        border-color: #ff3333 !important;
        box-shadow: 0 0 10px rgba(140, 0, 0, 0.5);
    }
    
    /* نصوص جانبية رمادية */
    .melancholy-text {
        color: #666666;
        font-style: italic;
        font-size: 0.9rem;
    }
</style>
"""
st.markdown(dark_theme_css, unsafe_allow_html=True)

# ==========================================
# 🧠 محرك توليد التابز الكئيبة (Tab Generator Engine)
# ==========================================
def generate_melancholy_tab(genre, difficulty):
    """يولد تابز قيتار فريدة بناءً على نوع الأغنية والصعوبة"""
    
    # تفكيك مستويات الصعوبة إلى أطوال ونقشات
    if difficulty == "Easy":
        length = 8
        frets = [0, 2, 3, 0, 2, 3, 5, 0]
    elif difficulty == "Intermediate":
        length = 12
        frets = [0, 2, 3, 5, 7, 8, 5, 3, 2, 0, 1, 0]
    else: # Hard
        length = 16
        frets = [0, 7, 8, 10, 12, 11, 7, 8, 5, 4, 0, 2, 3, 2, 1, 0]

    # كوردات كئيبة حسب النوع
    chords_pool = {
        "Depressive Black Metal / Doom": ["Em", "F5", "A5", "Bb5", "G#5"],
        "Gothic Rock / Post-Punk": ["Am", "Dm", "Fmaj7", "C", "Esus4"],
        "Midwest Emo / Math Rock": ["Cmaj7", "Em9", "G6", "Dsus2", "Bmin7"],
        "Dark Ambient Acoustic": ["Esus2", "Am/E", "Fm", "C#m", "Bdim"]
    }
    
    selected_chords = chords_pool.get(genre, ["Am", "Em"])
    
    # بناء الأوتار الستة
    strings = { 'E': ["-"], 'B': ["-"], 'G': ["-"], 'D': ["-"], 'A': ["-"], 'e': ["-"] }
    
    # توليد التتابعات النغمية (Arpeggio / Riff)
    for _ in range(length):
        fret = str(random.choice(frets))
        active_string = random.choice(['E', 'A', 'D', 'G', 'B', 'e'])
        
        for s in strings:
            if s == active_string:
                strings[s].append(fret + "-")
            else:
                strings[s].append("-" * (len(fret) + 1))
                
        # إضافة فراغات بين النوتات
        for s in strings:
            strings[s].append("-")

    # تجميع التابز كـ نص
    tab_title = f"// Title: A Fragment of {random.choice(['Void', 'Regret', 'Silence', 'Decay', 'Solitude'])}\n"
    tab_title += f"// Genre: {genre} | Difficulty: {difficulty}\n"
    tab_title += f"// Suggested Chords: {' - '.join(selected_chords)}\n\n"
    
    tab_body = ""
    for s in ['e', 'B', 'G', 'D', 'A', 'E']:
        tab_body += f"{s}|{''.join(strings[s])}\n"
        
    return tab_title + tab_body

# ==========================================
# 🖥️ واجهة المستخدم الرسومية (UI)
# ==========================================

# العنوان الرئيسي والتأثير البصري
st.markdown("<h1>WHAT I'M DOING IN MY LIFE?</h1>", unsafe_allow_html=True)
st.markdown("<p class='melancholy-text'>Constructing noise to distract from the endless ticking of time...</p>", unsafe_allow_html=True)
st.markdown("---")

# تقسيم الشاشة إلى جزأين: التحكم والأرشيف
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🖤 Invent a New Tab")
    
    # المدخلات
    song_genre = st.selectbox(
        "Select the atmosphere of your despair (Genre):",
        ["Gothic Rock / Post-Punk", "Depressive Black Metal / Doom", "Midwest Emo / Math Rock", "Dark Ambient Acoustic"]
    )
    
    difficulty_level = st.select_slider(
        "Select difficulty level (How much painful to play?):",
        options=["Easy", "Intermediate", "Hard"]
    )
    
    # أزرار التفاعل
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("🎸 Invent New Tab"):
            st.session_state.current_tab = generate_melancholy_tab(song_genre, difficulty_level)
            st.session_state.generated_count += 1
            
            # تأثيرات عشوائية كئيبة عند الضغط
            if st.session_state.generated_count % 5 == 0:
                st.toast("Another riff down the drain...", icon="🥀")
            
    with btn_col2:
        if st.button("💾 Save This Tab"):
            if st.session_state.current_tab and st.session_state.current_tab not in st.session_state.saved_tabs:
                st.session_state.saved_tabs.append(st.session_state.current_tab)
                st.success("Saved to your bleak memories archive.")
            elif not st.session_state.current_tab:
                st.warning("There is nothing here to save yet.")

    # عرض التاب الحالي
    if st.session_state.current_tab:
        st.markdown("<div class='gothic-card'>", unsafe_allow_html=True)
        st.markdown(f"<pre class='tab-display'>{st.session_state.current_tab}</pre>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='gothic-card'><p style='text-align:center; color:#555;'>The fretboard is empty. Click 'Invent New Tab' to summon something.</p></div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 🏛️ The Archive of Lost Riffs")
    st.markdown(f"<p class='melancholy-text'>You have saved {len(st.session_state.saved_tabs)} riffs so far.</p>", unsafe_allow_html=True)
    
    if st.session_state.saved_tabs:
        # عرض التابز المحفوظة في قائمة منسدلة أو كروت مصغرة
        for i, saved_tab in enumerate(st.session_state.saved_tabs):
            # استخراج العنوان فقط للعرض
            title_line = saved_tab.split("\n")[0].replace("// Title: ", "")
            genre_line = saved_tab.split("\n")[1].replace("// Genre: ", "")
            
            with st.expander(f"🖤 {title_line} ({genre_line.split(' | ')[1]})"):
                st.markdown(f"<pre class='tab-display' style='font-size:0.8rem;'>{saved_tab}</pre>", unsafe_allow_html=True)
                if st.button(f"Delete Riff #{i+1}", key=f"del_{i}"):
                    st.session_state.saved_tabs.pop(i)
                    st.rerun()
    else:
        st.markdown("<p style='color:#444; font-style:italic;'>No saved memories yet. Everything is forgotten.</p>", unsafe_allow_html=True)

# ==========================================
# ⏱️ عداد الزمن والعبثية (Footer Counters)
# ==========================================
st.markdown("---")
foot_col1, foot_col2, foot_col3 = st.columns(3)

with foot_col1:
    st.markdown("<p class='melancholy-text'>Current System Time:</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#666;'>{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)

with foot_col2:
    st.markdown("<p class='melancholy-text'>Total Riffs Invented in this session:</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#8c0000; font-weight:bold;'>{st.session_state.generated_count}</p>", unsafe_allow_html=True)

with foot_col3:
    st.markdown("<p class='melancholy-text'>Quote of the Void:</p>", unsafe_allow_html=True)
    quotes = [
        "\"Tuning down to Drop D won't fix your problems.\"",
        "\"The metronome ticks, drawing us closer to the end.\"",
        "\"Every chord is just a vibration in an empty room.\"",
        "\"Your amplifier cannot scream as loud as your thoughts.\""
    ]
    st.markdown(f"<p style='color:#666; font-style:italic;'>{random.choice(quotes)}</p>", unsafe_allow_html=True)
