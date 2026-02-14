import streamlit as st
import datetime
import random
import time
import base64

# ===== Page Config =====
st.set_page_config(
    page_title="💝 For Shiraz 💝",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== Session State =====
if "page" not in st.session_state:
    st.session_state.page = "main"
if "show_message" not in st.session_state:
    st.session_state.show_message = False
if "show_gift" not in st.session_state:
    st.session_state.show_gift = False
if "music_playing" not in st.session_state:
    st.session_state.music_playing = False
if "heart_click" not in st.session_state:
    st.session_state.heart_click = 0
if "love_count" not in st.session_state:
    st.session_state.love_count = 0
if "show_hide_memory" not in st.session_state:
    st.session_state.show_hide_memory = False
if "gift_opened" not in st.session_state:
    st.session_state.gift_opened = False

# ===== Interactive Enhancements =====
if "reaction_count" not in st.session_state:
    st.session_state.reaction_count = 0
if "last_reaction" not in st.session_state:
    st.session_state.last_reaction = None
if "message_replies" not in st.session_state:
    st.session_state.message_replies = []
if "heart_messages" not in st.session_state:
    st.session_state.heart_messages = [
        "💭 I'm thinking of you...",
        "🎵 ilomilo is playing in my head",
        "🌙 The moon shines for you",
        "📱 Why didn't you text me today?",
        "💝 Shiraz...",
        "⭐ You're the prettiest star in the sky",
        "🌹 Today's rose is for you",
        "💌 You're always on my mind"
    ]
if "sound_played" not in st.session_state:
    st.session_state.sound_played = False

# ===== Real Time Timer - UPDATED DATES =====
# First chat was approximately 404 days ago from Feb 14, 2026
# That would be around January 6, 2025
if "first_chat_date" not in st.session_state:
    st.session_state.first_chat_date = datetime.datetime(2025, 1, 6)  # 404 days before Feb 14, 2026

# Birthday is 202 days from Feb 14, 2026
# That would be around September 4, 2026
if "birthday_date" not in st.session_state:
    st.session_state.birthday_date = datetime.datetime(2026, 9, 4)  # 202 days from Feb 14, 2026

# ===== Custom CSS =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
        color: #333333 !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #ffd1d1 0%, #ffe6f0 50%, #fff0f5 100%);
        background-attachment: fixed;
        transition: background 1s ease;
    }
    
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #333333 !important;
    }
    
    /* Main Heart */
    .main-heart {
        position: relative;
        width: 200px;
        height: 200px;
        margin: 0 auto 30px;
        animation: heartbeat 1.5s ease-in-out infinite;
        cursor: pointer;
        filter: drop-shadow(0 0 30px rgba(255, 105, 180, 0.5));
    }
    
    @keyframes heartbeat {
        0% { transform: scale(1); }
        14% { transform: scale(1.2); }
        28% { transform: scale(1); }
        42% { transform: scale(1.2); }
        70% { transform: scale(1); }
    }
    
    /* Main Card */
    .card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 40px;
        padding: 40px;
        box-shadow: 0 30px 60px rgba(255, 105, 180, 0.2);
        border: 3px solid #ff69b4;
        margin: 20px 0;
        animation: cardAppear 1s ease-out;
    }
    
    @keyframes cardAppear {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Title */
    .title {
        font-size: 60px;
        font-weight: 900;
        color: #d43f8d !important;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 2px 2px 0 #ffe6f0;
    }
    
    /* Floating Hearts */
    .floating-heart {
        position: fixed;
        font-size: 20px;
        animation: float 4s infinite;
        pointer-events: none;
        z-index: 999;
        color: #ff69b4 !important;
    }
    
    @keyframes float {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) rotate(360deg);
            opacity: 0;
        }
    }
    
    /* Message Box */
    .message-box {
        background: #fff9fb;
        border-radius: 30px;
        padding: 30px;
        border: 3px dashed #ff69b4;
        position: relative;
        margin: 30px 0;
    }
    
    .message-box::before {
        content: "💌";
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 40px;
        background: white;
        border-radius: 50%;
        padding: 10px;
        box-shadow: 0 5px 15px rgba(255, 105, 180, 0.3);
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: rotate(-5deg); }
        50% { transform: rotate(5deg) translateY(-5px); }
    }
    
    .message-box p, .message-box div {
        color: #4a4a4a !important;
    }
    
    /* Highlighted Text */
    .highlight {
        font-size: 28px;
        font-weight: 900;
        color: #d43f8d !important;
        display: inline-block;
        animation: glow 2s infinite;
    }
    
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 10px #ffb6c1; }
        50% { text-shadow: 0 0 30px #ff69b4; }
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ff69b4, #d43f8d) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border: 2px solid white !important;
        width: 100%;
        margin: 5px 0;
        box-shadow: 0 10px 20px rgba(255, 105, 180, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(255, 20, 147, 0.4) !important;
    }
    
    .stButton > button p {
        color: white !important;
    }
    
    /* Music Box */
    .music-box {
        background: #fff0f5;
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        border: 2px solid #ff69b4;
        text-align: center;
    }
    
    .vinyl-record {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1a1a1a, #333);
        animation: spin 4s linear infinite;
        margin: 0 auto 15px;
        border: 3px solid white;
        box-shadow: 0 0 20px rgba(255, 105, 180, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white !important;
        font-size: 30px;
    }
    
    .vinyl-record div {
        color: white !important;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Gift Box */
    .gift-box {
        background: linear-gradient(135deg, #ff69b4, #d43f8d);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 3px solid white;
        animation: giftPulse 2s infinite;
    }
    
    .gift-box h3, .gift-box div {
        color: white !important;
    }
    
    @keyframes giftPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .gift-box:hover {
        transform: scale(1.05) rotate(2deg);
        box-shadow: 0 20px 40px rgba(255, 105, 180, 0.4);
    }
    
    .gift-content {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        border: 2px solid #ff69b4;
    }
    
    .gift-content p, .gift-content h3 {
        color: #333333 !important;
    }
    
    /* Hide Story */
    .hide-story {
        background: #2c2c2c;
        color: white !important;
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        border: 3px solid #ff69b4;
        position: relative;
        overflow: hidden;
    }
    
    .hide-story h3, .hide-story p, .hide-story div {
        color: white !important;
    }
    
    .hide-story::before {
        content: "👀";
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 30px;
        opacity: 0.2;
        animation: peek 3s infinite;
    }
    
    @keyframes peek {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(10px); }
    }
    
    /* Countdown */
    .countdown-box {
        background: #ffe6f0;
        border-radius: 100px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        border: 2px solid #ff69b4;
    }
    
    .countdown-box h3, .countdown-box div {
        color: #4a4a4a !important;
    }
    
    .timer {
        display: flex;
        justify-content: center;
        gap: 20px;
    }
    
    .time-unit {
        background: white;
        border-radius: 15px;
        padding: 10px;
        min-width: 70px;
        border: 2px solid #ff69b4;
    }
    
    .time-number {
        font-size: 36px;
        font-weight: 900;
        color: #d43f8d !important;
    }
    
    .time-label {
        color: #666 !important;
    }
    
    /* Photo Album */
    .photo-album {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 15px;
        margin: 30px 0;
    }
    
    .photo-frame {
        aspect-ratio: 1;
        background: linear-gradient(45deg, #ff69b4, #d43f8d);
        padding: 5px;
        border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .photo-frame:hover {
        transform: scale(1.05) rotate(3deg);
    }
    
    .photo-placeholder {
        width: 100%;
        height: 100%;
        background: white;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
    }
    
    /* Signature */
    .signature {
        text-align: center;
        margin-top: 40px;
        font-size: 24px;
        font-weight: 900;
        color: #d43f8d !important;
    }
    
    .signature div {
        color: #d43f8d !important;
    }
    
    /* Glass Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(255, 105, 180, 0.1);
    }
    
    /* Neon Text Effect */
    .neon-text {
        color: #fff;
        text-shadow: 
            0 0 7px #fff,
            0 0 10px #fff,
            0 0 21px #fff,
            0 0 42px #ff69b4,
            0 0 82px #ff69b4,
            0 0 92px #ff69b4,
            0 0 102px #ff69b4,
            0 0 151px #ff69b4;
        animation: flicker 1.5s infinite alternate;
    }
    
    @keyframes flicker {
        0%, 18%, 22%, 25%, 53%, 57%, 100% {
            text-shadow: 
                0 0 4px #fff,
                0 0 11px #fff,
                0 0 19px #fff,
                0 0 40px #ff69b4,
                0 0 80px #ff69b4,
                0 0 90px #ff69b4,
                0 0 100px #ff69b4,
                0 0 150px #ff69b4;
        }
        20%, 24%, 55% {        
            text-shadow: none;
        }
    }
    
    /* Hover Card Effect */
    .hover-card {
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    
    .hover-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 30px 60px rgba(255, 105, 180, 0.3);
    }
    
    /* Wave Effect */
    .wave-effect {
        position: relative;
        overflow: hidden;
    }
    
    .wave-effect::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.3s, height 0.3s;
    }
    
    .wave-effect:active::after {
        width: 200px;
        height: 200px;
    }
    
    /* Typing Effect */
    .typing-effect {
        overflow: hidden;
        border-right: .15em solid #ff69b4;
        white-space: nowrap;
        margin: 0 auto;
        animation: 
            typing 3.5s steps(40, end),
            blink-caret .75s step-end infinite;
    }
    
    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent; }
        50% { border-color: #ff69b4; }
    }
    
    /* Pulse Heart Effect */
    .pulse-heart {
        animation: heartbeat 2s infinite;
    }
    
    /* Pop In Animation */
    @keyframes popIn {
        0% { transform: scale(0); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .pop-in {
        animation: popIn 0.5s;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .title {
            font-size: 40px;
        }
        .timer {
            gap: 10px;
        }
        .time-unit {
            min-width: 50px;
        }
        .time-number {
            font-size: 24px;
        }
    }
    
    /* Streamlit overrides */
    .stMarkdown, .stMarkdown p {
        color: #333333 !important;
    }
    
    .stText {
        color: #333333 !important;
    }
    
    iframe {
        border-radius: 10px;
        border: 2px solid #ff69b4;
    }
</style>
""", unsafe_allow_html=True)

# ===== Helper Functions =====
def create_floating_hearts():
    """Generate floating hearts"""
    hearts_html = ""
    for i in range(20):
        left = random.randint(0, 100)
        delay = random.uniform(0, 4)
        size = random.randint(15, 25)
        hearts = ["❤️", "💖", "💝", "💗", "💓", "💕"]
        heart = random.choice(hearts)
        hearts_html += f"""
        <div class="floating-heart" style="
            left: {left}%;
            animation-delay: {delay}s;
            font-size: {size}px;
        ">{heart}</div>
        """
    return hearts_html

def countdown_to_valentine():
    """Countdown to Valentine's Day 2026"""
    now = datetime.datetime.now()
    valentine = datetime.datetime(2026, 2, 14)
    
    if now > valentine:
        return None
    
    diff = valentine - now
    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    seconds = diff.seconds % 60
    
    return days, hours, minutes, seconds

# ===== Interactive Functions =====
def get_random_heart_message():
    """Random message when clicking heart"""
    return random.choice(st.session_state.heart_messages)

def add_reaction(reaction_type):
    """Track reactions"""
    st.session_state.reaction_count += 1
    st.session_state.last_reaction = {
        "type": reaction_type,
        "time": datetime.datetime.now().strftime("%H:%M"),
        "count": st.session_state.reaction_count
    }

# ===== UPDATED: Real Time Timer Functions =====
def time_since_first_chat():
    """Time since first chat - approximately 404 days"""
    now = datetime.datetime.now()
    diff = now - st.session_state.first_chat_date
    return diff.days

def time_until_birthday():
    """Time until Shiraz's birthday - 202 days from now"""
    now = datetime.datetime.now()
    diff = st.session_state.birthday_date - now
    return max(0, diff.days)

def get_time_of_day_greeting():
    """Greeting based on time of day"""
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "🌅 Good morning Shiraz"
    elif hour < 17:
        return "☀️ Good afternoon beautiful"
    elif hour < 20:
        return "🌆 Good evening my love"
    else:
        return "🌙 Good night Shiraz, dream of me"

# ===== Audio Functions =====
def get_audio_player(audio_url, autoplay=False):
    """Create audio player"""
    autoplay_attr = "autoplay" if autoplay else ""
    return f"""
    <audio {autoplay_attr} controls style="width: 100%; margin: 10px 0;">
        <source src="{audio_url}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """

# ===== Main Page =====
def main():
    # Floating hearts
    st.markdown(create_floating_hearts(), unsafe_allow_html=True)
    
    # Header with heart
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="main-heart">
            <svg viewBox="0 0 32 29.6" style="width:100%; height:100%; fill: #ff69b4;">
                <path d="M23.6,0c-3.4,0-6.3,2.7-7.6,5.6C14.7,2.7,11.8,0,8.4,0C3.8,0,0,3.8,0,8.4c0,9.4,9.5,11.9,16,21.2
                c6.1-9.3,16-12.1,16-21.2C32,3.8,28.2,0,23.6,0z"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("❤️ Click the heart"):
            st.session_state.heart_click += 1
            add_reaction("heart_click")
            if st.session_state.heart_click % 5 == 0:
                st.balloons()
    
    st.markdown("<h1 class='title'>For You Shiraz 💝</h1>", unsafe_allow_html=True)
    
    # Time-based Greeting
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #fff0f5, #ffe6f0);
        padding: 15px;
        border-radius: 50px;
        text-align: center;
        margin: 10px 0 20px 0;
        border: 2px solid #ff69b4;
    ">
        <h3 style="color: #d43f8d; margin: 0;">{get_time_of_day_greeting()}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive Heart Messages
    if st.session_state.heart_click > 0:
        if st.session_state.heart_click % 3 == 0:
            st.markdown(f"""
            <div class="pop-in" style="
                background: rgba(255, 255, 255, 0.9);
                padding: 15px;
                border-radius: 50px;
                text-align: center;
                margin: 10px 0;
                border: 2px solid #ff69b4;
            ">
                <p style="color: #d43f8d; font-size: 18px; margin: 0;">
                    {get_random_heart_message()}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.session_state.heart_click == 10:
            st.balloons()
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #ffd700, #ff69b4);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                margin: 20px 0;
                border: 3px solid white;
            ">
                <h3 style="color: white; margin: 0;">✨ 10 times you clicked my heart ✨</h3>
                <p style="color: white;">Each time a flower blooms in my heart 💐</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.session_state.heart_click == 25:
            st.snow()
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #87CEEB, #FF69B4);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                margin: 20px 0;
                border: 3px solid white;
            ">
                <h3 style="color: white; margin: 0;">❄️ 25 times... ❄️</h3>
                <p style="color: white;">Each click makes the world more beautiful 💕</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Main Card
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Photos
        st.markdown("""
        <div class="photo-album">
            <div class="photo-frame"><div class="photo-placeholder">🤷‍♀️</div></div>
            <div class="photo-frame"><div class="photo-placeholder">🤷‍♂️</div></div>
            <div class="photo-frame"><div class="photo-placeholder">💭</div></div>
            <div class="photo-frame"><div class="photo-placeholder">🌹</div></div>
        </div>
        """, unsafe_allow_html=True)
        
        # ===== UPDATED: Real Time Timers with 404 and 202 =====
        st.markdown("---")
        st.markdown("### ⏰ Time Trackers", unsafe_allow_html=True)
        
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            days_since = time_since_first_chat()  # This will show approximately 404 days
            st.markdown(f"""
            <div class="hover-card" style="
                background: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                border: 2px solid #ff69b4;
                box-shadow: 0 5px 15px rgba(255,105,180,0.2);
            ">
                <h4 style="color: #d43f8d;">⏰ Since First Chat</h4>
                <div style="font-size: 48px; font-weight: 900; color: #ff1493;">{days_since}</div>
                <div style="color: #666;">days</div>
                <p style="color: #888; font-size: 14px; margin-top: 10px;">
                    404 days of thinking about you, and every day I love you more 💭
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_t2:
            days_until = time_until_birthday()  # This will show approximately 202 days
            if days_until > 0:
                st.markdown(f"""
                <div class="hover-card" style="
                    background: white;
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                    border: 2px solid #ff69b4;
                    box-shadow: 0 5px 15px rgba(255,105,180,0.2);
                ">
                    <h4 style="color: #d43f8d;">🎂 Until Your Birthday</h4>
                    <div style="font-size: 48px; font-weight: 900; color: #ff1493;">{days_until}</div>
                    <div style="color: #666;">days</div>
                    <p style="color: #888; font-size: 14px; margin-top: 10px;">
                        202 days until I get to celebrate you! Can't wait 🎉
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #ff69b4, #ff1493);
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                    border: 2px solid white;
                ">
                    <h4 style="color: white;">🎂 Happy Birthday Shiraz! 🎂</h4>
                    <div style="font-size: 24px; color: white;">Today is all about you! 🎉</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Live time display
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.5);
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin: 10px 0;
            font-size: 14px;
            color: #666;
            border: 1px dashed #ff69b4;
        ">
            🕒 Now: {datetime.datetime.now().strftime("%A, %B %d, %Y - %I:%M %p")}
        </div>
        """, unsafe_allow_html=True)
        
        # Animated progress bar
        st.markdown("### ⏳ Time passes and my love grows", unsafe_allow_html=True)
        progress_bar = st.progress(0)
        for i in range(100):
            if i % 25 == 0:
                progress_bar.progress(i/100)
                time.sleep(0.01)
        st.markdown("""
        <p style="text-align: center; color: #d43f8d;">
            404 days and still counting... every second makes me love you more 💝
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Valentine's Day countdown
        countdown = countdown_to_valentine()
        if countdown:
            days, hours, minutes, seconds = countdown
            st.markdown(f"""
            <div class="countdown-box">
                <h3>⏳ Time until Valentine's Day</h3>
                <div class="timer">
                    <div class="time-unit"><div class="time-number">{days}</div><div class="time-label">Days</div></div>
                    <div class="time-unit"><div class="time-number">{hours}</div><div class="time-label">Hours</div></div>
                    <div class="time-unit"><div class="time-number">{minutes}</div><div class="time-label">Minutes</div></div>
                    <div class="time-unit"><div class="time-number">{seconds}</div><div class="time-label">Seconds</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # The hiding story
        if st.button("👀 The day you hid from me"):
            st.session_state.show_hide_memory = not st.session_state.show_hide_memory
            add_reaction("hide_story")
        
        if st.session_state.show_hide_memory:
            st.markdown("""
            <div class="hide-story">
                <h3 style="text-align: center;">💔 The Day You Hid From Me</h3>
                <p style="text-align: center; font-size: 18px; line-height: 1.8;">
                    I still remember that day...<br><br>
                    I was going to meet you for the first time.<br>
                    My heart was beating so fast...<br><br>
                    And then... you hid from me 😔<br><br>
                    I don't know why, but I understand.<br>
                    What matters is that I forgive you.<br><br>
                    I'll wait for you until you're ready 🤍
                </p>
                <div style="text-align: center; font-size: 30px;">💔 I Waited ❤️</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Love message
        st.markdown("""
        <div class="message-box">
            <p style="font-size: 20px; text-align: center;">
                <span class="highlight">My Dearest Shiraz</span><br><br>
                I know we've never met face to face... 🥺<br><br>
                But I feel you, I feel like you're the closest person to my heart.<br><br>
                <span class="highlight">I love you Shiraz</span><br><br>
                I love you even though I haven't seen you.<br>
                I love you because you're you.<br><br>
                <span style="font-size: 28px; color: #d43f8d;">I Love You 💝</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Music - ilomilo
        st.markdown("""
        <div class="music-box">
            <div class="vinyl-record">🎵</div>
            <h3 style="color: #d43f8d;">Billie Eilish - ilomilo</h3>
            <p>Your favorite song</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎧 Play ilomilo"):
            st.session_state.music_playing = not st.session_state.music_playing
            add_reaction("music_play")
        
        if st.session_state.music_playing:
            st.video("https://youtu.be/-e7wiyNO2us?si=JYVdDi6YmadDeAJx")
            st.balloons()
        
        # Audio Section
        st.markdown("### 🎵 Sounds from the Heart", unsafe_allow_html=True)
        
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.markdown("""
            <div style="
                background: white;
                padding: 15px;
                border-radius: 15px;
                border: 2px solid #ff69b4;
            ">
                <h4 style="color: #d43f8d; text-align: center;">ilomilo (sample)</h4>
                <audio controls style="width: 100%;">
                    <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3">
                </audio>
            </div>
            """, unsafe_allow_html=True)
        
        with col_s2:
            st.markdown("""
            <div style="
                background: white;
                padding: 15px;
                border-radius: 15px;
                border: 2px solid #ff69b4;
            ">
                <h4 style="color: #d43f8d; text-align: center;">❤️ Heartbeat</h4>
                <audio controls style="width: 100%;">
                    <source src="https://www.soundjay.com/misc/heartbeat-1.mp3" type="audio/mp3">
                </audio>
            </div>
            """, unsafe_allow_html=True)
        
        # Sound buttons
        st.markdown("### 🎚️ Talking Buttons", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            st.markdown("""
            <button onclick="new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3').play();" 
            style="
                background: linear-gradient(135deg, #ff69b4, #d43f8d);
                color: white;
                border: none;
                border-radius: 50px;
                padding: 15px;
                font-size: 18px;
                font-weight: 700;
                cursor: pointer;
                border: 2px solid white;
                width: 100%;
                transition: all 0.3s ease;
                margin: 5px 0;
            ">
                🔔 Thinking of you
            </button>
            """, unsafe_allow_html=True)
        
        with col_btn2:
            st.markdown("""
            <button onclick="new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-06.mp3').play();" 
            style="
                background: linear-gradient(135deg, #ff69b4, #d43f8d);
                color: white;
                border: none;
                border-radius: 50px;
                padding: 15px;
                font-size: 18px;
                font-weight: 700;
                cursor: pointer;
                border: 2px solid white;
                width: 100%;
                transition: all 0.3s ease;
                margin: 5px 0;
            ">
                💝 I love you
            </button>
            """, unsafe_allow_html=True)
        
        with col_btn3:
            st.markdown("""
            <button onclick="new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-07.mp3').play();" 
            style="
                background: linear-gradient(135deg, #ff69b4, #d43f8d);
                color: white;
                border: none;
                border-radius: 50px;
                padding: 15px;
                font-size: 18px;
                font-weight: 700;
                cursor: pointer;
                border: 2px solid white;
                width: 100%;
                transition: all 0.3s ease;
                margin: 5px 0;
            ">
                🎵 ilomilo
            </button>
            """, unsafe_allow_html=True)
        
        # Gift
        st.markdown("## 🎁 A Gift For You", unsafe_allow_html=True)
        
        if not st.session_state.gift_opened:
            if st.button("🎀 Open Your Gift"):
                st.session_state.gift_opened = True
                st.balloons()
                add_reaction("gift_opened")
        
        if st.session_state.gift_opened:
            st.markdown("""
            <div class="gift-box">
                <div style="font-size: 50px;">🎁</div>
                <h3>For You Shiraz</h3>
            </div>
            <div class="gift-content">
                <h3 style="color: #d43f8d; text-align: center;">💝 My Gift</h3>
                <p style="text-align: center;">
                    This whole page is my gift to you<br>
                    Every heart is for you<br>
                    Every word is from my heart<br>
                    Your favorite song is here<br>
                    My love for you after 404 days ❤️
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Buttons
        col_b1, col_b2, col_b3 = st.columns(3)
        
        with col_b1:
            if st.button("💌 Love Message"):
                st.session_state.show_message = not st.session_state.show_message
                add_reaction("love_message")
        
        with col_b2:
            if st.button("❤️ I Love You"):
                st.session_state.love_count += 1
                st.balloons()
                add_reaction("love_click")
        
        with col_b3:
            if st.button("💭 Thinking of You"):
                st.info(f"💭 {get_random_heart_message()}")
                add_reaction("thinking")
        
        if st.session_state.show_message:
            st.info("❤️ I love you Shiraz! You mean everything to me after 404 days and counting ❤️")
        
        if st.session_state.love_count > 0:
            st.markdown(f"<p style='text-align: center;'>❤️ {st.session_state.love_count} times today ❤️</p>", unsafe_allow_html=True)
        
        # Last Reaction Display
        if st.session_state.last_reaction:
            st.markdown(f"""
            <div style="
                background: #fff0f5;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                margin: 10px 0;
                border: 1px solid #ff69b4;
            ">
                <p style="color: #666; margin: 0; font-size: 14px;">
                    Last reaction: {st.session_state.last_reaction['type']} 
                    at {st.session_state.last_reaction['time']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Design Touches
        st.markdown("---")
        st.markdown("### ✨ Love Touches ✨", unsafe_allow_html=True)
        
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        
        with col_d1:
            st.markdown("""
            <div class="hover-card" style="
                background: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                border: 2px solid #ff69b4;
            ">
                <div style="font-size: 40px;">💝</div>
                <p style="color: #d43f8d;">Love</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_d2:
            st.markdown("""
            <div class="hover-card" style="
                background: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                border: 2px solid #ff69b4;
            ">
                <div style="font-size: 40px;">⭐</div>
                <p style="color: #d43f8d;">Hope</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_d3:
            st.markdown("""
            <div class="hover-card" style="
                background: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                border: 2px solid #ff69b4;
            ">
                <div style="font-size: 40px;">🌹</div>
                <p style="color: #d43f8d;">Longing</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_d4:
            st.markdown("""
            <div class="hover-card" style="
                background: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                border: 2px solid #ff69b4;
            ">
                <div style="font-size: 40px;">💭</div>
                <p style="color: #d43f8d;">Memory</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Typing effect
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.5);
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
        ">
            <h3 class="typing-effect" style="color: #d43f8d; width: fit-content; margin: 0 auto;">
                404 days of loving you, 202 days until your birthday Shiraz
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Neon effect
        st.markdown("""
        <div style="
            background: #1a1a2e;
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
        ">
            <h2 class="neon-text">404 ❤️ 202</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Pulsing hearts
        st.markdown("""
        <div style="
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
        ">
            <div class="pulse-heart" style="font-size: 40px;">❤️</div>
            <div class="pulse-heart" style="font-size: 50px; animation-delay: 0.3s;">💖</div>
            <div class="pulse-heart" style="font-size: 40px; animation-delay: 0.6s;">💝</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Signature
        st.markdown("""
        <div class="signature">
            <div>❤️ Eyad ❤️</div>
            <div>February 14, 2026</div>
            <div style="font-size: 16px; margin-top: 10px;">404 days and counting... 202 days until your birthday 🎂</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
