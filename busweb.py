import streamlit as st
import datetime
import random
import time
from PIL import Image
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

# ===== Custom CSS =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #8B0000 0%, #C71585 50%, #FF1493 100%);
        background-attachment: fixed;
    }
    
    /* Main Heart */
    .main-heart {
        position: relative;
        width: 200px;
        height: 200px;
        margin: 0 auto 30px;
        animation: heartbeat 1.5s ease-in-out infinite;
        cursor: pointer;
        filter: drop-shadow(0 0 30px rgba(255, 20, 147, 0.5));
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
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 40px;
        padding: 40px;
        box-shadow: 0 30px 60px rgba(139, 0, 0, 0.3),
                    0 0 0 5px rgba(255, 255, 255, 0.5);
        border: 3px solid white;
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
        background: linear-gradient(135deg, #8B0000, #C71585, #FF1493);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 3px 3px 0 rgba(255, 255, 255, 0.3);
    }
    
    /* Floating Hearts */
    .floating-heart {
        position: fixed;
        font-size: 20px;
        animation: float 4s infinite;
        pointer-events: none;
        z-index: 999;
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
        background: rgba(255, 240, 245, 0.9);
        border-radius: 30px;
        padding: 30px;
        border: 3px dashed #8B0000;
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
        box-shadow: 0 5px 15px rgba(139, 0, 0, 0.3);
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: rotate(-5deg); }
        50% { transform: rotate(5deg) translateY(-5px); }
    }
    
    /* Highlighted Text */
    .highlight {
        font-size: 28px;
        font-weight: 900;
        color: #8B0000;
        display: inline-block;
        animation: glow 2s infinite;
    }
    
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 10px #FF1493; }
        50% { text-shadow: 0 0 30px #C71585; }
    }
    
    /* Buttons */
    .custom-btn {
        background: linear-gradient(135deg, #8B0000, #C71585);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid white;
        width: 100%;
        margin: 5px 0;
        box-shadow: 0 10px 20px rgba(139, 0, 0, 0.3);
    }
    
    .custom-btn:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(199, 21, 133, 0.5);
    }
    
    /* Music Box */
    .music-box {
        background: linear-gradient(135deg, rgba(139, 0, 0, 0.1), rgba(199, 21, 133, 0.1));
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        border: 2px solid white;
        backdrop-filter: blur(5px);
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
        box-shadow: 0 0 20px rgba(199, 21, 133, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 30px;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Gift Box */
    .gift-box {
        background: linear-gradient(135deg, #FF1493, #C71585);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 3px solid white;
        animation: giftPulse 2s infinite;
    }
    
    @keyframes giftPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .gift-box:hover {
        transform: scale(1.05) rotate(2deg);
        box-shadow: 0 20px 40px rgba(255, 20, 147, 0.4);
    }
    
    .gift-content {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        border: 2px solid #8B0000;
    }
    
    /* Hide Story */
    .hide-story {
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        border: 3px solid #C71585;
        position: relative;
        overflow: hidden;
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
        background: rgba(139, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 100px;
        padding: 20px;
        text-align: center;
        color: white;
        margin: 20px 0;
    }
    
    .timer {
        display: flex;
        justify-content: center;
        gap: 20px;
    }
    
    .time-unit {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 10px;
        min-width: 70px;
    }
    
    .time-number {
        font-size: 36px;
        font-weight: 900;
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
        background: linear-gradient(45deg, #8B0000, #C71585);
        padding: 5px;
        border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .photo-frame:hover {
        transform: scale(1.05) rotate(3deg);
    }
    
    .photo-placeholder {
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.9);
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
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
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
</style>
""", unsafe_allow_html=True)

# ===== Helper Functions =====
def create_floating_hearts():
    """Generate floating hearts"""
    hearts_html = ""
    for i in range(30):
        left = random.randint(0, 100)
        delay = random.uniform(0, 4)
        size = random.randint(15, 30)
        hearts = ["❤️", "💖", "💝", "💗", "💓", "💕"]
        heart = random.choice(hearts)
        hearts_html += f"""
        <div class="floating-heart" style="
            left: {left}%;
            animation-delay: {delay}s;
            font-size: {size}px;
            color: {random.choice(['#FF69B4', '#FFB6C1', '#FF1493', '#DB7093'])};
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

def play_song():
    """Play ilomilo"""
    st.session_state.music_playing = not st.session_state.music_playing
    if st.session_state.music_playing:
        st.balloons()

# ===== Main Page =====
def main_page():
    # Floating hearts background
    st.markdown(create_floating_hearts(), unsafe_allow_html=True)
    
    # Header with heart
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Clickable heart
        st.markdown("""
        <div class="main-heart" onclick="
            this.style.transform='scale(1.3)';
            setTimeout(()=>this.style.transform='scale(1)', 200);
        ">
            <svg viewBox="0 0 32 29.6" style="width:100%; height:100%; fill: #8B0000;">
                <path d="M23.6,0c-3.4,0-6.3,2.7-7.6,5.6C14.7,2.7,11.8,0,8.4,0C3.8,0,0,3.8,0,8.4c0,9.4,9.5,11.9,16,21.2
                c6.1-9.3,16-12.1,16-21.2C32,3.8,28.2,0,23.6,0z"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("❤️ Click the heart", key="heart_btn"):
            st.session_state.heart_click += 1
            if st.session_state.heart_click % 5 == 0:
                st.balloons()
    
    st.markdown(f"<h1 class='title'>For Shiraz 💝</h1>", unsafe_allow_html=True)
    
    # Main Card
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Photo placeholders
        st.markdown("""
        <div class="photo-album">
            <div class="photo-frame"><div class="photo-placeholder">👧🏾</div></div>
            <div class="photo-frame"><div class="photo-placeholder">👦🏿</div></div>
            <div class="photo-frame"><div class="photo-placeholder">💭</div></div>
            <div class="photo-frame"><div class="photo-placeholder">🌹</div></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Valentine's Day countdown
        countdown = countdown_to_valentine()
        if countdown:
            days, hours, minutes, seconds = countdown
            st.markdown(f"""
            <div class="countdown-box">
                <h3>⏳ Time left until Valentine's Day</h3>
                <div class="timer">
                    <div class="time-unit"><div class="time-number">{days}</div><div>Days</div></div>
                    <div class="time-unit"><div class="time-number">{hours}</div><div>Hours</div></div>
                    <div class="time-unit"><div class="time-number">{minutes}</div><div>Minutes</div></div>
                    <div class="time-unit"><div class="time-number">{seconds}</div><div>Seconds</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="countdown-box">
                <h2>✨ Happy Valentine's Day Shiraz ✨</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # The story - when she hid from me
        if st.button("👀 The day you hid from me", key="hide_btn"):
            st.session_state.show_hide_memory = not st.session_state.show_hide_memory
        
        if st.session_state.show_hide_memory:
            st.markdown("""
            <div class="hide-story">
                <h3 style="color: #C71585; text-align: center;">💔 The Day You Hid From Me</h3>
                <p style="text-align: center; font-size: 18px; line-height: 1.8;">
                    <br>
                    I still remember that day... 📅<br>
                    <br>
                    I was going to meet you for the first time in my life.<br>
                    I got ready, I was excited, my heart was beating so fast... 💓<br>
                    <br>
                    And then... you hid from me 😔<br>
                    <br>
                    I don't know why, but I'm sure you had your reasons.<br>
                    Maybe you were scared, maybe you weren't ready, maybe something else.<br>
                    <br>
                    But what matters is that I forgive you, and I understand.<br>
                    I wasn't angry, but my heart hurt a little 💔<br>
                    <br>
                    But after that, I thought, maybe that's why our love is stronger.<br>
                    Maybe that's why you became even more precious to me.<br>
                    <br>
                    What matters is that I love you, and I'll wait for you until you're ready 🤍<br>
                </p>
                <div style="text-align: center; font-size: 30px; margin-top: 20px;">
                    💔 I Waited For You ❤️
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # The message
        st.markdown('<div class="message-box">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; font-size: 18px; line-height: 1.8;">
            <p><span class="highlight">My Dearest Shiraz</span></p>
            
            <p>I know we've never met face to face, and I still haven't seen you at school... 🥺</p>
            
            <p>But I swear, I can feel you, I can feel your presence, I feel like you're the closest person to my heart.</p>
            
            <p>Maybe our love is different, maybe our path is hard, maybe some people don't understand, but I believe in us 💪</p>
            
            <p><span class="highlight">I love you Shiraz</span></p>
            
            <p>I love you even though I haven't seen you, I love you even though we haven't met, I love you because you're you.</p>
            
            <p style="font-size: 28px; font-weight: 900; color: #8B0000; margin: 30px 0;">
                I Love You 💝
            </p>
            
            <p style="font-size: 20px; opacity: 0.8;">
                And I know that one day, the good times will come<br>
                We'll meet, we'll talk, we'll laugh<br>
                And we'll forget all these hard moments 🤍
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Music Box - ilomilo by Billie Eilish
        st.markdown('<div class="music-box">', unsafe_allow_html=True)
        
        col_m1, col_m2 = st.columns([1, 3])
        
        with col_m1:
            st.markdown('<div class="vinyl-record">🎵</div>', unsafe_allow_html=True)
        
        with col_m2:
            st.markdown("""
            <div style="text-align: left;">
                <div style="font-size: 24px; font-weight: 700; color: #8B0000;">Billie Eilish</div>
                <div style="font-size: 18px; color: #C71585;">ilomilo</div>
                <div style="font-size: 14px; margin-top: 10px;">Your favorite song</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Music player button
        if st.button("🎧 Play the song", key="play_music_btn"):
            play_song()
        
        # YouTube embed when playing
        if st.session_state.music_playing:
            st.markdown("""
            <div style="margin: 20px 0;">
                <iframe width="100%" height="100" src="https://www.youtube.com/embed/KBtk5FUeJrw" 
                title="ilomilo" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Gift Section
        st.markdown("## 🎁 A Gift For You", unsafe_allow_html=True)
        
        if not st.session_state.gift_opened:
            if st.button("🎀 Open Your Gift", key="open_gift_btn"):
                st.session_state.gift_opened = True
                st.balloons()
                st.session_state.show_gift = True
        
        if st.session_state.gift_opened:
            st.markdown("""
            <div class="gift-box">
                <div style="font-size: 50px; margin-bottom: 20px;">🎁</div>
                <h3 style="color: white;">For You Shiraz</h3>
            </div>
            
            <div class="gift-content">
                <h3 style="color: #8B0000; text-align: center;">💝 My Gift To You</h3>
                <p style="text-align: center; font-size: 18px; line-height: 1.8;">
                    <br>
                    💌 This whole page is my gift to you<br>
                    <br>
                    🌹 Every heart floating here is for you<br>
                    <br>
                    💖 Every word I wrote is from my heart<br>
                    <br>
                    🎵 Your favorite song is here for you<br>
                    <br>
                    💝 And most importantly... my love for you<br>
                    <br>
                    <span style="font-size: 24px; font-weight: 900; color: #C71585;">
                        I hope you like it ❤️
                    </span>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Interactive Buttons
        st.markdown("## 💝 Click Below", unsafe_allow_html=True)
        
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            if st.button("💌 Love Message", key="btn_love"):
                st.session_state.show_message = not st.session_state.show_message
        
        with col_b2:
            if st.button("❤️ I Love You", key="btn_heart"):
                st.session_state.love_count += 1
                st.balloons()
        
        # Love Message Popup
        if st.session_state.show_message:
            with st.container():
                st.markdown("""
                <div style="
                    background: white;
                    padding: 30px;
                    border-radius: 20px;
                    text-align: center;
