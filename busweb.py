import streamlit as st
import datetime
import random
import time

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
            if st.session_state.heart_click % 5 == 0:
                st.balloons()
    
    st.markdown("<h1 class='title'>For You Shiraz 💝</h1>", unsafe_allow_html=True)
    
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
        
        # Countdown
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
        
        if st.session_state.music_playing:
            st.video("https://youtu.be/-e7wiyNO2us?si=JYVdDi6YmadDeAJx")
            st.balloons()
        
        # Gift
        st.markdown("## 🎁 A Gift For You", unsafe_allow_html=True)
        
        if not st.session_state.gift_opened:
            if st.button("🎀 Open Your Gift"):
                st.session_state.gift_opened = True
                st.balloons()
        
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
                    My love for you ❤️
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Buttons
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            if st.button("💌 Love Message"):
                st.session_state.show_message = not st.session_state.show_message
        
        with col_b2:
            if st.button("❤️ I Love You"):
                st.session_state.love_count += 1
                st.balloons()
        
        if st.session_state.show_message:
            st.info("❤️ I love you Shiraz! You mean everything to me ❤️")
        
        if st.session_state.love_count > 0:
            st.markdown(f"<p style='text-align: center;'>❤️ {st.session_state.love_count} times today ❤️</p>", unsafe_allow_html=True)
        
        # Signature
        st.markdown("""
        <div class="signature">
            <div>❤️ Eyad ❤️</div>
            <div>February 14, 2026</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()