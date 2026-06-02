import streamlit as st
from emotion_detector import detect_emotion
from emotions.keywords import EMOTION_COLORS, EMOTION_DESCRIPTIONS
from matching import find_matches
from pulse_spaces import get_recommended_spaces

# Page config
st.set_page_config(
    page_title="belong.ai",
    page_icon="🌑",
    layout="centered"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        background-color: #0f0f0f;
    }
    .stTextArea textarea {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 1px solid #333;
        border-radius: 12px;
        font-size: 16px;
    }
    .emotion-card {
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        margin-top: 20px;
    }
    .match-card {
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #333;
        background-color: #1a1a1a;
    }
    .pulse-card {
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #333;
        background-color: #1a1a1a;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <h1 style='text-align: center; color: #A78BFA;
    font-size: 48px; margin-bottom: 0;'>belong.ai</h1>
    <p style='text-align: center; color: #6B7280;
    font-size: 16px; margin-top: 4px;'>
    you are not alone. you just haven't found
    your people yet.</p>
    <hr style='border: 1px solid #1f1f1f;'/>
""", unsafe_allow_html=True)

st.markdown("""
    <h3 style='color: #ffffff; font-size: 20px;'>
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
                <p style='color: #ffffff;
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
        st.markdown("""
            <h3 style='color: #ffffff; font-size: 20px;
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
                            <p style='color: #ffffff;
                            font-size: 16px;
                            font-weight: bold;
                            margin: 0;'>🌑 {match['alias']}</p>
                            <p style='color: {match_color};
                            font-size: 13px;
                            margin: 4px 0 0 0;'>
                            {match_emotion_display}</p>
                        </div>
                        <div style='text-align: right;'>
                            <p style='color: #A78BFA;
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
        st.markdown("""
            <h3 style='color: #ffffff; font-size: 20px;
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