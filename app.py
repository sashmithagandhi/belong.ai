import streamlit as st
import base64
from emotion_detector import detect_emotion
from emotions.keywords import EMOTION_COLORS, EMOTION_DESCRIPTIONS
from matching import find_matches
from pulse_spaces import get_recommended_spaces
from themes import THEMES, get_theme_css
from auth import auth_gate

# Page config
st.set_page_config(
    page_title="belong.ai",
    page_icon="🌑",
    layout="centered"
)

# Theme selector in sidebar
st.sidebar.markdown("""
    <h3 style='color:#A78BFA;'>🎨 Choose Your Space</h3>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <p style='color:#6B7280; font-size:13px;'>
    Upload your own background image</p>
""", unsafe_allow_html=True)

uploaded_bg = st.sidebar.file_uploader(
    "Upload background",
    type=["png", "jpg", "jpeg", "webp"],
    label_visibility="collapsed"
)

selected_theme = st.sidebar.selectbox(
    "Or choose a theme",
    list(THEMES.keys()),
    format_func=lambda x: f"{THEMES[x]['emoji']} {x}"
)

# Apply uploaded background or theme
if uploaded_bg is not None:
    bg_bytes = uploaded_bg.read()
    bg_base64 = base64.b64encode(bg_bytes).decode()
    ext = uploaded_bg.name.split('.')[-1]
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/{ext};base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stTextArea textarea {{
            background-color: rgba(0,0,0,0.6);
            color: #ffffff;
            border: 1px solid #555;
            border-radius: 12px;
            font-size: 16px;
        }}
        .match-card {{
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            border: 1px solid #555;
            background-color: rgba(0,0,0,0.6);
        }}
        .pulse-card {{
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            border: 1px solid #555;
            background-color: rgba(0,0,0,0.6);
        }}
        </style>
    """, unsafe_allow_html=True)
    theme = THEMES["Midnight"]
else:
    st.markdown(get_theme_css(selected_theme), unsafe_allow_html=True)
    theme = THEMES[selected_theme]

# Auth gate
if not auth_gate():
    st.stop()

# Header
st.markdown(f"""
    <h1 style='text-align: center; color: {theme['accent']};
    font-size: 48px; margin-bottom: 0;'>belong.ai</h1>
    <p style='text-align: center; color: #6B7280;
    font-size: 16px; margin-top: 4px;'>
    you are not alone. you just haven't found
    your people yet.</p>
    <hr style='border: 1px solid #1f1f1f;'/>
""", unsafe_allow_html=True)

st.markdown(f"""
    <h3 style='color: {theme['text']}; font-size: 20px;'>
    📓 How are you feeling today?</h3>
    <p style='color: #6B7280; font-size: 14px;'>
    Write freely. No one is watching.
    This space belongs to you.</p>
""", unsafe_allow_html=True)

# Diary input
diary_entry = st.text_area(
    "",
    placeholder="Start writing here... let it all out.",
    height=200,
    label_visibility="collapsed"
)

# Analyze button
if st.button("✦ Understand my emotion", use_container_width=True):
    if diary_entry.strip() == "":
        st.warning("Write something first. Even one sentence is enough.")
    else:
        emotion, scores = detect_emotion(diary_entry)
        color = EMOTION_COLORS[emotion]
        description = EMOTION_DESCRIPTIONS[emotion]
        emotion_display = emotion.replace("_", " ").title()

        # Emotion card
        st.markdown(f"""
            <div class='emotion-card'
            style='background-color: {color}20;
            border: 1px solid {color};'>
                <h2 style='color: {color};
                font-size: 28px;'>{emotion_display}</h2>
                <p style='color: {theme['text']};
                font-size: 16px;'>{description}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <p style='color: #6B7280; font-size: 13px;
            text-align: center; margin-top: 16px;'>
            belong.ai detected your emotional state.
            You are seen.</p>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Emotional Matches
        st.markdown(f"""
            <h3 style='color: {theme['text']}; font-size: 20px;
            margin-top: 24px;'>
            👥 Your Emotional Matches</h3>
            <p style='color: #6B7280; font-size: 14px;'>
            People who emotionally resonate with you
            right now.</p>
        """, unsafe_allow_html=True)

        matches, user_emotion = find_matches(diary_entry)

        for match in matches:
            match_emotion_display = match['emotion'].replace(
                "_", " ").title()
            match_color = EMOTION_COLORS[match['emotion']]
            st.markdown(f"""
                <div class='match-card'>
                    <div style='display: flex;
                    justify-content: space-between;
                    align-items: center;'>
                        <div>
                            <p style='color: {theme['text']};
                            font-size: 16px;
                            font-weight: bold;
                            margin: 0;'>🌑 {match['alias']}</p>
                            <p style='color: {match_color};
                            font-size: 13px;
                            margin: 4px 0 0 0;'>
                            {match_emotion_display}</p>
                        </div>
                        <div style='text-align: right;'>
                            <p style='color: {theme['accent']};
                            font-size: 22px;
                            font-weight: bold;
                            margin: 0;'>
                            {match['resonance']}%</p>
                            <p style='color: #6B7280;
                            font-size: 11px;
                            margin: 0;'>
                            emotional resonance</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Pulse Spaces
        st.markdown(f"""
            <h3 style='color: {theme['text']}; font-size: 20px;
            margin-top: 24px;'>
            🌐 Your Pulse Spaces</h3>
            <p style='color: #6B7280; font-size: 14px;'>
            Anonymous spaces where people feel like you.</p>
        """, unsafe_allow_html=True)

        spaces = get_recommended_spaces(emotion)

        for space in spaces:
            st.markdown(f"""
                <div class='pulse-card'
                style='border-left: 3px solid {space["color"]};'>
                    <p style='color: {space["color"]};
                    font-size: 18px;
                    font-weight: bold;
                    margin: 0;'>
                    {space["emoji"]} {space["name"]}</p>
                    <p style='color: #8b949e;
                    font-size: 13px;
                    margin: 6px 0 0 0;'>
                    {space["description"]}</p>
                </div>
            """, unsafe_allow_html=True)

# Sidebar logout
st.sidebar.markdown("---")
if st.sidebar.button("🔒 Lock Diary"):
    st.session_state.authenticated = False
    st.rerun()
    