PULSE_SPACES = [
    {
        "name": "Midnight Overthinkers",
        "emoji": "🌙",
        "description": "For those whose minds never quiet down at night.",
        "emotions": ["hyperreflective", "cognitively_overloaded"],
        "color": "#F59E0B"
    },
    {
        "name": "Silent Burnout",
        "emoji": "🕯️",
        "description": "For those who are exhausted but still showing up.",
        "emotions": ["mentally_overwhelmed", "socially_exhausted"],
        "color": "#FF6B6B"
    },
    {
        "name": "Behind The Mask",
        "emoji": "🎭",
        "description": "For those who hide how they truly feel.",
        "emotions": ["emotionally_masked", "emotionally_guarded"],
        "color": "#B0B0B0"
    },
    {
        "name": "The Void",
        "emoji": "🌑",
        "description": "For those who feel empty and disconnected.",
        "emotions": ["emotionally_detached"],
        "color": "#6B7280"
    },
    {
        "name": "3AM Thoughts",
        "emoji": "⏰",
        "description": "For those awake when the world is asleep.",
        "emotions": ["hyperreflective", "emotionally_guarded"],
        "color": "#A78BFA"
    },
    {
        "name": "Emotionally Drained",
        "emoji": "🌊",
        "description": "For those running on empty.",
        "emotions": ["socially_exhausted", "mentally_overwhelmed"],
        "color": "#6B8CFF"
    },
    {
        "name": "Warm Frequency",
        "emoji": "☀️",
        "description": "For those in a good place emotionally.",
        "emotions": ["emotionally_open"],
        "color": "#34D399"
    }
]

def get_recommended_spaces(emotion, top_n=3):
    scored = []
    for space in PULSE_SPACES:
        if emotion in space["emotions"]:
            scored.append((space, 2))
        else:
            scored.append((space, 0))

    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    return [s[0] for s in scored[:top_n]]