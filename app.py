import streamlit as st
import base64
from datetime import date
from emotion_detector import detect_emotion
from emotions.keywords import EMOTION_COLORS, EMOTION_DESCRIPTIONS
from matching import find_matches
from pulse_spaces import get_recommended_spaces
from themes import THEMES, get_theme_css
from auth import auth_gate
from gamification import add_entry, load_data, BADGES
from growth_tracker import plot_emotion_timeline, plot_emotion_distribution, get_stats
from emotional_wrapped import generate_wrapped, plot_wrapped_chart, is_wrapped_season
from storyteller import generate_story, STORY_STYLES
from pulse_chat import render_chat

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

# Load user data
data = load_data()
total_entries, streak, total_badges, unique_emotions = get_stats(data)

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

# Stats row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📝 Entries", total_entries)
with col2:
    st.metric("🔥 Streak", f"{streak} days")
with col3:
    st.metric("🏆 Badges", total_badges)
with col4:
    st.metric("🎭 Emotions", unique_emotions)

st.markdown("---")

# Badges section
if data.get("badges"):
    st.markdown(f"""
        <h3 style='color: {theme['accent']}; font-size: 18px;'>
        🏆 Your Badges</h3>
    """, unsafe_allow_html=True)

    badge_cols = st.columns(len(data["badges"]))
    for i, badge_id in enumerate(data["badges"]):
        badge = BADGES[badge_id]
        with badge_cols[i]:
            st.markdown(f"""
                <div style='text-align: center; padding: 10px;
                background-color: {theme['surface']};
                border-radius: 12px;
                border: 1px solid {theme['accent']};'>
                    <p style='font-size: 28px; margin: 0;'>
                    {badge['emoji']}</p>
                    <p style='color: {theme['accent']};
                    font-size: 11px; margin: 4px 0 0 0;
                    font-weight: bold;'>{badge['name']}</p>
                </div>
            """, unsafe_allow_html=True)
    st.markdown("---")

# Diary section
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

        # Save entry and check badges
        data, newly_earned = add_entry(emotion, diary_entry)

        # Show newly earned badges
        if newly_earned:
            for badge_id in newly_earned:
                badge = BADGES[badge_id]
                st.balloons()
                st.success(
                    f"🏆 Badge Unlocked: {badge['emoji']} "
                    f"{badge['name']} — {badge['description']}"
                )

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
            with st.expander(
                f"{space['emoji']} {space['name']} — tap to enter",
                expanded=False
            ):
                render_chat(space, theme)

# Growth tracking section
st.markdown("---")
st.markdown(f"""
    <h3 style='color: {theme['accent']}; font-size: 20px;'>
    📊 Your Emotional Growth</h3>
    <p style='color: #6B7280; font-size: 14px;'>
    Track your emotional journey over time.</p>
""", unsafe_allow_html=True)

timeline = plot_emotion_timeline()
if timeline:
    st.plotly_chart(timeline, use_container_width=True)
else:
    st.info("Write your first entry to start tracking your emotional journey!")

distribution = plot_emotion_distribution()
if distribution:
    st.plotly_chart(distribution, use_container_width=True)

# Emotional Wrapped Section
st.markdown("---")
st.markdown(f"""
    <h3 style='color: {theme['accent']}; font-size: 20px;'>
    🎬 Your Emotional Wrapped</h3>
    <p style='color: #6B7280; font-size: 14px;'>
    Your emotional story this month.</p>
""", unsafe_allow_html=True)

if is_wrapped_season():
    wrapped = generate_wrapped()
    if wrapped:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg,
            {wrapped["dominant_color"]}20, #0f0f0f);
            border: 1px solid {wrapped["dominant_color"]};
            border-radius: 16px; padding: 24px;
            text-align: center; margin-bottom: 20px;'>
                <p style='color: #6B7280; font-size: 13px;
                margin: 0;'>{wrapped["month"]}</p>
                <h2 style='color: {wrapped["dominant_color"]};
                font-size: 32px; margin: 8px 0;'>
                {wrapped["dominant_display"]}</h2>
                <p style='color: #ffffff; font-size: 15px;
                margin: 0;'>Your dominant emotion this month</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div style='text-align: center; padding: 16px;
                background-color: #1a1a1a;
                border-radius: 12px;'>
                    <p style='color: {theme["accent"]};
                    font-size: 28px; font-weight: bold;
                    margin: 0;'>{wrapped["total_entries"]}</p>
                    <p style='color: #6B7280; font-size: 12px;
                    margin: 4px 0 0 0;'>Entries Written</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style='text-align: center; padding: 16px;
                background-color: #1a1a1a;
                border-radius: 12px;'>
                    <p style='color: {theme["accent"]};
                    font-size: 28px; font-weight: bold;
                    margin: 0;'>{wrapped["streak"]}</p>
                    <p style='color: #6B7280; font-size: 12px;
                    margin: 4px 0 0 0;'>Day Streak</p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div style='text-align: center; padding: 16px;
                background-color: #1a1a1a;
                border-radius: 12px;'>
                    <p style='color: {theme["accent"]};
                    font-size: 28px; font-weight: bold;
                    margin: 0;'>{len(wrapped["badges"])}</p>
                    <p style='color: #6B7280; font-size: 12px;
                    margin: 4px 0 0 0;'>Badges Earned</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
            <p style='color: #ffffff; font-size: 15px;
            text-align: center; margin-top: 20px;
            font-style: italic;'>
            "{wrapped["growth_message"]}"</p>
        """, unsafe_allow_html=True)

        wrapped_chart = plot_wrapped_chart(wrapped)
        if wrapped_chart:
            st.plotly_chart(wrapped_chart, use_container_width=True)
    else:
        st.info("Write at least one entry this month to see your Emotional Wrapped!")
else:
    days_left = 25 - date.today().day
    st.markdown(f"""
        <div style='text-align: center; padding: 20px;
        background-color: #1a1a1a;
        border-radius: 16px;
        border: 1px solid #333;'>
            <p style='font-size: 28px; margin: 0;'>🎬</p>
            <p style='color: #A78BFA; font-size: 16px;
            font-weight: bold; margin: 8px 0;'>
            Emotional Wrapped arrives in {days_left} days</p>
            <p style='color: #6B7280; font-size: 13px;
            margin: 0;'>Your monthly emotional story is being written.
            Keep journaling.</p>
        </div>
    """, unsafe_allow_html=True)

# Emotional Storytelling Section
st.markdown("---")
st.markdown(f"""
    <h3 style='color: {theme['accent']}; font-size: 20px;'>
    📖 Your Life Chapter</h3>
    <p style='color: #6B7280; font-size: 14px;'>
    Let AI turn your emotional journey into a story.</p>
""", unsafe_allow_html=True)

story_style = st.selectbox(
    "Choose your story style",
    list(STORY_STYLES.keys())
)

if st.button("✦ Generate My Story", use_container_width=True):
    if len(data.get("entries", [])) == 0:
        st.warning("Write at least one diary entry first!")
    else:
        with st.spinner("Writing your story..."):
            story = generate_story(story_style)
            if story:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg,
                    #A78BFA20, #0f0f0f);
                    border: 1px solid #A78BFA;
                    border-radius: 16px;
                    padding: 32px;
                    margin-top: 16px;'>
                        <p style='color: #A78BFA;
                        font-size: 12px;
                        text-transform: uppercase;
                        letter-spacing: 2px;
                        margin: 0 0 16px 0;'>
                        {story_style} — Your Chapter</p>
                        <p style='color: #ffffff;
                        font-size: 16px;
                        line-height: 1.8;
                        font-style: italic;
                        margin: 0;'>{story}</p>
                    </div>
                """, unsafe_allow_html=True)

# Sidebar logout
st.sidebar.markdown("---")
if st.sidebar.button("🔒 Lock Diary"):
    st.session_state.authenticated = False
    st.rerun()
    