import streamlit as st
from groq import Groq
from gamification import load_data

STORY_STYLES = {
    "Cinematic": "dramatic, visual, powerful like a movie narration",
    "Poetic": "metaphorical, lyrical, emotionally deep like a poem",
    "Reflective": "honest, thoughtful, calm like a personal journal",
    "Melancholic": "nostalgic, tender, quietly bittersweet",
    "Hopeful": "warm, uplifting, forward looking and gentle"
}

def build_prompt(style):
    data = load_data()
    entries = data.get("entries", [])
    emotions = data.get("emotions_experienced", [])
    streak = data.get("streak", 0)

    if not entries:
        return None

    recent_entries = entries[-5:]
    entry_summaries = "\n".join([
        f"- {e['date']}: felt {e['emotion'].replace('_', ' ')}"
        for e in recent_entries
    ])

    prompt = f"""Write a short emotional story (100 words) about someone's journey.
Style: {STORY_STYLES[style]}
Their recent emotional states:
{entry_summaries}
They have journaled for {streak} days straight.
Write in second person (you). Be poetic and personal. Only write the story."""

    return prompt

def generate_story(style):
    prompt = build_prompt(style)
    if not prompt:
        return None

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"
