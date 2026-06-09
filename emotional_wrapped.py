import json
import os
from datetime import datetime, date
from collections import Counter
import plotly.graph_objects as go
from emotions.keywords import EMOTION_COLORS, EMOTION_DESCRIPTIONS
from gamification import load_data, BADGES

def is_wrapped_season():
    today = date.today()
    return today.day >= 25

def get_monthly_data():
    data = load_data()
    entries = data.get("entries", [])
    
    current_month = date.today().month
    current_year = date.today().year
    
    monthly_entries = [
        e for e in entries
        if datetime.fromisoformat(e["date"]).month == current_month
        and datetime.fromisoformat(e["date"]).year == current_year
    ]
    
    return monthly_entries, data

def get_dominant_emotion(entries):
    if not entries:
        return None
    emotions = [e["emotion"] for e in entries]
    return Counter(emotions).most_common(1)[0][0]

def get_emotional_journey(entries):
    if not entries:
        return None
    emotions = [e["emotion"] for e in entries]
    unique = list(set(emotions))
    return unique

def generate_wrapped():
    monthly_entries, data = get_monthly_data()
    
    if not monthly_entries:
        return None
    
    dominant = get_dominant_emotion(monthly_entries)
    journey = get_emotional_journey(monthly_entries)
    total = len(monthly_entries)
    streak = data.get("streak", 0)
    badges = data.get("badges", [])
    
    if total >= 20:
        growth_msg = "You showed up for yourself every day. That takes courage."
    elif total >= 10:
        growth_msg = "You are building a beautiful habit of self reflection."
    elif total >= 5:
        growth_msg = "You are just getting started. Keep going."
    else:
        growth_msg = "Every journey begins with a single step. You started."
    
    dominant_display = dominant.replace("_", " ").title()
    dominant_color = EMOTION_COLORS.get(dominant, "#A78BFA")
    
    return {
        "dominant_emotion": dominant,
        "dominant_display": dominant_display,
        "dominant_color": dominant_color,
        "dominant_description": EMOTION_DESCRIPTIONS.get(dominant, ""),
        "total_entries": total,
        "streak": streak,
        "badges": badges,
        "journey": journey,
        "growth_message": growth_msg,
        "month": date.today().strftime("%B %Y")
    }

def plot_wrapped_chart(wrapped):
    monthly_entries, _ = get_monthly_data()
    
    if not monthly_entries:
        return None
    
    emotions = [e["emotion"] for e in monthly_entries]
    emotion_counts = Counter(emotions)
    
    labels = [e.replace("_", " ").title() for e in emotion_counts.keys()]
    values = list(emotion_counts.values())
    colors = [EMOTION_COLORS.get(e, "#A78BFA") for e in emotion_counts.keys()]
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.4,
        textfont=dict(color="#ffffff")
    ))
    
    fig.update_layout(
        paper_bgcolor="#0f0f0f",
        plot_bgcolor="#0f0f0f",
        font=dict(color="#ffffff"),
        legend=dict(
            bgcolor="#1a1a1a",
            bordercolor="#333333"
        ),
        height=350
    )
    
    return fig
    