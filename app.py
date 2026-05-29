import streamlit as st
from emotion_detector import detect_emotion
from emotions.keywords import EMOTION_COLORS, EMOTION_DESCRIPTIONS

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