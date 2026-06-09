import streamlit as st
from datetime import datetime
from emotions.keywords import EMOTION_COLORS

PULSE_AVATARS = [
    "🌑", "🌊", "⚡", "🔥", "🌙", 
    "✨", "🎭", "🌿", "💫", "🌌"
]

def initialize_chat(space_name):
    key = f"chat_{space_name}"
    if key not in st.session_state:
        st.session_state[key] = [
            {
                "avatar": "🌑",
                "alias": "Quiet Storm",
                "message": "anyone else feel like they're carrying invisible weight?",
                "time": "11:42 PM"
            },
            {
                "avatar": "✨",
                "alias": "Faded Echo",
                "message": "every single day. you're not alone here.",
                "time": "11:43 PM"
            },
            {
                "avatar": "🌊",
                "alias": "Silent Wave",
                "message": "this space feels different. safer somehow.",
                "time": "11:45 PM"
            }
        ]
    return key

def render_chat(space, theme):
    st.markdown(f"""
        <div style='background-color: {space["color"]}15;
        border: 1px solid {space["color"]};
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;'>
            <h3 style='color: {space["color"]};
            font-size: 20px; margin: 0;'>
            {space["emoji"]} {space["name"]}</h3>
            <p style='color: #6B7280;
            font-size: 13px; margin: 4px 0 0 0;'>
            {space["description"]}</p>
        </div>
    """, unsafe_allow_html=True)

    chat_key = initialize_chat(space["name"])
    messages = st.session_state[chat_key]

    # Display messages
    for msg in messages:
        st.markdown(f"""
            <div style='display: flex;
            gap: 12px;
            margin-bottom: 16px;
            align-items: flex-start;'>
                <div style='font-size: 24px;
                flex-shrink: 0;'>{msg["avatar"]}</div>
                <div>
                    <div style='display: flex;
                    align-items: center;
                    gap: 8px;'>
                        <p style='color: {space["color"]};
                        font-size: 13px;
                        font-weight: bold;
                        margin: 0;'>{msg["alias"]}</p>
                        <p style='color: #6B7280;
                        font-size: 11px;
                        margin: 0;'>{msg["time"]}</p>
                    </div>
                    <p style='color: #ffffff;
                    font-size: 14px;
                    margin: 4px 0 0 0;
                    line-height: 1.5;'>{msg["message"]}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Message input
    st.markdown("<div style='margin-top: 16px;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        user_message = st.text_input(
            "Send a message",
            placeholder="say something... anonymously.",
            key=f"input_{space['name']}",
            label_visibility="collapsed"
        )
    with col2:
        send = st.button("Send", key=f"send_{space['name']}", 
                        use_container_width=True)

    if send and user_message.strip():
        import random
        new_msg = {
            "avatar": random.choice(PULSE_AVATARS),
            "alias": "You",
            "message": user_message,
            "time": datetime.now().strftime("%I:%M %p")
        }
        st.session_state[chat_key].append(new_msg)
        st.rerun()
        