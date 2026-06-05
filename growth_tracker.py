import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from gamification import load_data
from emotions.keywords import EMOTION_COLORS

def get_emotion_history():
    data = load_data()
    entries = data.get("entries", [])
    if not entries:
        return None
    df = pd.DataFrame(entries)
    return df

def plot_emotion_timeline():
    df = get_emotion_history()
    if df is None or len(df) == 0:
        return None

    df["emotion_display"] = df["emotion"].apply(
        lambda x: x.replace("_", " ").title()
    )
    df["color"] = df["emotion"].apply(
        lambda x: EMOTION_COLORS.get(x, "#A78BFA")
    )

    fig = go.Figure()

    for emotion in df["emotion"].unique():
        subset = df[df["emotion"] == emotion]
        fig.add_trace(go.Scatter(
            x=subset["date"],
            y=subset["emotion_display"],
            mode="markers",
            marker=dict(
                size=14,
                color=EMOTION_COLORS.get(emotion, "#A78BFA"),
                line=dict(width=1, color="#ffffff")
            ),
            name=emotion.replace("_", " ").title()
        ))

    fig.update_layout(
        title="Your Emotional Journey",
        paper_bgcolor="#0f0f0f",
        plot_bgcolor="#0f0f0f",
        font=dict(color="#ffffff"),
        xaxis=dict(
            title="Date",
            gridcolor="#1f1f1f",
            color="#6B7280"
        ),
        yaxis=dict(
            title="Emotional State",
            gridcolor="#1f1f1f",
            color="#6B7280"
        ),
        legend=dict(
            bgcolor="#1a1a1a",
            bordercolor="#333333"
        ),
        height=400
    )
    return fig

def plot_emotion_distribution():
    df = get_emotion_history()
    if df is None or len(df) == 0:
        return None

    emotion_counts = df["emotion"].value_counts().reset_index()
    emotion_counts.columns = ["emotion", "count"]
    emotion_counts["emotion_display"] = emotion_counts["emotion"].apply(
        lambda x: x.replace("_", " ").title()
    )
    emotion_counts["color"] = emotion_counts["emotion"].apply(
        lambda x: EMOTION_COLORS.get(x, "#A78BFA")
    )

    fig = go.Figure(go.Bar(
        x=emotion_counts["emotion_display"],
        y=emotion_counts["count"],
        marker_color=emotion_counts["color"],
        text=emotion_counts["count"],
        textposition="auto"
    ))

    fig.update_layout(
        title="Your Emotional Patterns",
        paper_bgcolor="#0f0f0f",
        plot_bgcolor="#0f0f0f",
        font=dict(color="#ffffff"),
        xaxis=dict(
            gridcolor="#1f1f1f",
            color="#6B7280"
        ),
        yaxis=dict(
            gridcolor="#1f1f1f",
            color="#6B7280"
        ),
        height=350
    )
    return fig

def get_stats(data):
    total = len(data.get("entries", []))
    streak = data.get("streak", 0)
    badges = len(data.get("badges", []))
    emotions = len(set(data.get("emotions_experienced", [])))
    return total, streak, badges, emotions
    