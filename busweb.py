import streamlit as st
import datetime
import random
import time
from PIL import Image
import base64

# ===== إعداد الصفحة =====
st.set_page_config(
    page_title="💝 إلى شيراز 💝",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== تهيئة حالة التطبيق =====
if "page" not in st.session_state:
    st.session_state.page = "main"
if "show_message" not in st.session_state:
    st.session_state.show_message = False
if "show_surprise" not in st.session_state:
    st.session_state.show_surprise = False
if "music_playing" not in st.session_state:
    st.session_state.music_playing = False
if "heart_click" not in st.session_state:
    st.session_state.heart_click = 0
if "valentine_count" not in st.session_state:
    st.session_state.valentine_count = 0
if "memory_shown" not in st.session_state:
    st.session_state.memory_shown = 0
if "show_hide_memory" not in st.session_state:
    st.session_state.show_hide_memory = False

# ===== التصميم =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Readex+Pro:wght@300;400;700&display=swap');
    
    * {
        font-family: 'Readex Pro', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #4a0000 0%, #8B0000 50%, #c71585 100%);
        background-attachment: fixed;
    }
    
    /* القلب الرئيسي */
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
    
    /* البطاقة الرئيسية */
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
    
    /* العنوان */
    .title {
        font-size: 60px;
        font-weight: 900;
        background: linear-gradient(135deg, #8B0000, #c71585);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 3px 3px 0 rgba(255, 255, 255, 0.3);
    }
    
    /* القلوب المتطايرة */
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
    
    /* مربع الرسالة */
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
    
    /* النص المميز */
    .highlight {
        font-size: 28px;
        font-weight: 900;
        color: #8B0000;
        display: inline-block;
        animation: glow 2s infinite;
    }
    
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 10px #c71585; }
        50% { text-shadow: 0 0 30px #8B0000; }
    }
    
    /* الأزرار */
    .custom-btn {
        background: linear-gradient(135deg, #8B0000, #c71585);
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
    
    .custom-btn-white {
        background: white;
        color: #8B0000;
        border: 2px solid #8B0000;
    }
    
    /* صندوق الموسيقى */
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
    
    /* مشغل الموسيقى */
    .audio-player {
        background: white;
        border-radius: 50px;
        padding: 10px 20px;
        margin: 20px 0;
        border: 2px solid #8B0000;
    }
    
    /* العد التنازلي */
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
    
    /* ذكريات */
    .memory-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-right: 5px solid #8B0000;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .memory-card:hover {
        transform: translateX(-10px);
        box-shadow: 0 10px 25px rgba(139,0,0,0.2);
    }
    
    /* قصة الاختباء */
    .hide-story {
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        border: 3px solid #c71585;
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
    
    /* التوقيع */
    .signature {
        text-align: center;
        margin-top: 40px;
        font-size: 24px;
        font-weight: 900;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* البوم الصور */
    .photo-album {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 15px;
        margin: 30px 0;
    }
    
    .photo-frame {
        aspect-ratio: 1;
        background: linear-gradient(45deg, #8B0000, #c71585);
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
    
    /* تأثير الدموع */
    .tear-effect {
        position: relative;
    }
    
    .tear {
        position: absolute;
        width: 10px;
        height: 10px;
        background: rgba(173, 216, 230, 0.5);
        border-radius: 50%;
        animation: fall 3s infinite;
    }
    
    @keyframes fall {
        0% { transform: translateY(-20px); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(100px); opacity: 0; }
    }
    
    /* للشاشات الصغيرة */
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

# ===== دوال مساعدة =====
def create_floating_hearts():
    """توليد قلوب متطايرة"""
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
    """عد تنازلي للفلانتين"""
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
    """تشغيل أغنية ilomilo"""
    st.session_state.music_playing = not st.session_state.music_playing
    if st.session_state.music_playing:
        st.balloons()

# ===== الصفحة الرئيسية =====
def main_page():
    # قلوب متطايرة
    st.markdown(create_floating_hearts(), unsafe_allow_html=True)
    
    # الهيدر
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # القلب الرئيسي
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
        
        if st.button("❤️ إضغطي على القلب", key="heart_btn"):
            st.session_state.heart_click += 1
            if st.session_state.heart_click % 5 == 0:
                st.balloons()
    
    st.markdown(f"<h1 class='title'>شيراز يا أجمل شيراز 💝</h1>", unsafe_allow_html=True)
    
    # البطاقة الرئيسية
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # ألبوم الصور (مكان للصور الافتراضية)
        st.markdown("""
        <div class="photo-album">
            <div class="photo-frame"><div class="photo-placeholder">👧🏾</div></div>
            <div class="photo-frame"><div class="photo-placeholder">👦🏿</div></div>
            <div class="photo-frame"><div class="photo-placeholder">💭</div></div>
            <div class="photo-frame"><div class="photo-placeholder">🌹</div></div>
        </div>
        """, unsafe_allow_html=True)
        
        # العد التنازلي
        countdown = countdown_to_valentine()
        if countdown:
            days, hours, minutes, seconds = countdown
            st.markdown(f"""
            <div class="countdown-box">
                <h3>⏳ باقي على الفلانتين يا قمر</h3>
                <div class="timer">
                    <div class="time-unit"><div class="time-number">{days}</div><div>يوم</div></div>
                    <div class="time-unit"><div class="time-number">{hours}</div><div>ساعة</div></div>
                    <div class="time-unit"><div class="time-number">{minutes}</div><div>دقيقة</div></div>
                    <div class="time-unit"><div class="time-number">{seconds}</div><div>ثانية</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="countdown-box">
                <h2>✨ اليوم هو الفلانتين يا شيراز ✨</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # قصة الاختباء
        if st.button("👀 قصة اليوم اللي خبتي مني", key="hide_btn"):
            st.session_state.show_hide_memory = not st.session_state.show_hide_memory
        
        if st.session_state.show_hide_memory:
            st.markdown("""
            <div class="hide-story">
                <h3 style="color: #c71585; text-align: center;">😢 اليوم اللي خبتي مني</h3>
                <p style="text-align: center; font-size: 18px; line-height: 1.8;">
                    <br>
                    أنا لسه فاكر اليوم دا... 📅<br>
                    <br>
                    كنت هقابلك أول مرة في حياتي، كنت مرتاح وحاسس إنو أخيراً راح أشوفك<br>
                    جهزت نفسي، كنت متحمس، وقلبي كان بيدق بسرعة... 💓<br>
                    <br>
                    وبعدين... لقيتك خبتي مني 😔<br>
                    <br>
                    معرفش ليه، بس أكيد كان ليكي أسبابك<br>
                    يمكن كنتي خايفة، يمكن مش مستعدة، يمكن حاجة تانية<br>
                    <br>
                    بس المهم إني سامحتك، وإني فاهمك<br>
                    والله ما زعلت، بس تأذيت شوية في قلبي 💔<br>
                    <br>
                    بس بعديها فكرت، يمكن عشان كدا حبنا أقوى<br>
                    يمكن عشان كدا بقيتي أغلى عندي<br>
                    <br>
                    المهم إني بحبك، وإني مستنيكي لما تبقى جاهزة 🤍<br>
                </p>
                <div style="text-align: center; font-size: 30px; margin-top: 20px;">
                    💔 انتظرتك ❤️
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # الرسالة
        st.markdown('<div class="message-box">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; font-size: 18px; line-height: 1.8;">
            <p><span class="highlight">يا أجمل شيراز</span></p>
            
            <p>أنا عارف إحنا ما قابلنا بعض face to face، ولسه ما شفتك في المدرسة... 🥺</p>
            
            <p>بس والله العظيم إني بحس بيكي، بحس بوجودك، بحس إنك أقرب ناس لقلبي</p>
            
            <p>يمكن حبنا مختلف، يمكن طريقنا صعب، يمكن في ناس بتستغرب، بس أنا واثق فينا 💪</p>
            
            <p><span class="highlight">أنا بحبك يا شيراز</span></p>
            
            <p>بحبك حتى ولو ما شفتك، بحبك حتى ولو ما التقينا، بحبك لأنك أنتي</p>
            
            <p style="font-size: 28px; font-weight: 900; color: #8B0000; margin: 30px 0;">
                بحبك 💝
            </p>
            
            <p style="font-size: 20px; opacity: 0.8;">
                وأكيد راح تيجي الأيام الحلوة<br>
                ونتقابل ونحكي ونضحك<br>
                وننسى كل اللحظات الصعبة دي 🤍
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # صندوق الموسيقى - ilomilo (مشغل فعلي)
        st.markdown('<div class="music-box">', unsafe_allow_html=True)
        
        col_m1, col_m2 = st.columns([1, 3])
        
        with col_m1:
            st.markdown('<div class="vinyl-record">🎵</div>', unsafe_allow_html=True)
        
        with col_m2:
            st.markdown("""
            <div style="text-align: right;">
                <div style="font-size: 24px; font-weight: 700; color: #8B0000;">Billie Eilish</div>
                <div style="font-size: 18px; color: #c71585;">ilomilo</div>
                <div style="font-size: 14px; margin-top: 10px;">أغنيتك المفضلة</div>
            </div>
            """, unsafe_allow_html=True)
        
        # مشغل الموسيقى الفعلي (YouTube embed)
        if st.button("🎧 شغلي الأغنية", key="play_music_btn"):
            play_song()
        
        if st.session_state.music_playing:
            st.markdown("""
            <div style="margin: 20px 0;">
                <iframe width="100%" height="100" src="https://www.youtube.com/embed/KBtk5FUeJrw" 
                title="ilomilo" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
            </div>
            <div style="text-align: center; color: #8B0000; font-size: 14px;">
                🎵 ilomilo - Billie Eilish
            </div>
            """, unsafe_allow_html=True)
            
            # كلمات الأغنية
            with st.expander("🎤 كلمات ilomilo"):
                st.markdown("""
                ```
                Told you not to worry
                But maybe that's a lie
                Honey, what'd you hurry?
                I've been here your whole life
                
                I don't want to be alone
                I love you, won't you come home?
                
                Ilomilo, ilomilo, ilomilo
                If you're not here, where'd you go?
                ```
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ذكرياتنا
        st.markdown("## 📸 لحظاتنا", unsafe_allow_html=True)
        
        memories = [
            ("💭", "أول مرة كلمتك", "لسه فاكر أول رسالة بعتهالك وقلبي كان بيدق"),
            ("🎵", "لما عرفت إنك بتحبي ilomilo", "من يومها صارت أغنيتنا إحنا الاثنين"),
            ("🌙", "السهرة اللي فاتت", "لما قعدنا نحكي لين الصبح وما حسينا بالوقت"),
            ("💔", "اليوم اللي خبتي مني", "لسه فاكره ويمكن عشان كدا أنا كاتب الرسالة دي"),
            ("💭", "كل يوم بفكر فيكي", "حتى لو ما كنا سوا، انتي دايمًا في بالي")
        ]
        
        for i, (emoji, title, desc) in enumerate(memories):
            if i >= st.session_state.memory_shown:
                if st.button(f"{emoji} {title}", key=f"memory_{i}"):
                    st.session_state.memory_shown += 1
                    st.rerun()
                break
            else:
                st.markdown(f"""
                <div class="memory-card">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="font-size: 30px;">{emoji}</div>
                        <div>
                            <div style="font-weight: 700; color: #8B0000;">{title}</div>
                            <div style="opacity: 0.8;">{desc}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # الأزرار التفاعلية
        st.markdown("## 💝 اضغطي", unsafe_allow_html=True)
        
        col_b1, col_b2, col_b3 = st.columns(3)
        
        with col_b1:
            if st.button("💌 رسالة حب", key="btn_love"):
                st.session_state.show_me