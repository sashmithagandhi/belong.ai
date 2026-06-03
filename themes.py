THEMES = {
    "Midnight": {
        "bg": "#0f0f0f",
        "surface": "#1a1a1a",
        "text": "#ffffff",
        "accent": "#A78BFA",
        "border": "#333333",
        "emoji": "🌑"
    },
    "Ocean": {
        "bg": "#0a1628",
        "surface": "#0d2137",
        "text": "#e0f0ff",
        "accent": "#38bdf8",
        "border": "#1e4a6e",
        "emoji": "🌊"
    },
    "Forest": {
        "bg": "#0a1a0f",
        "surface": "#0f2318",
        "text": "#d4f5d4",
        "accent": "#4ade80",
        "border": "#1a3a20",
        "emoji": "🌿"
    },
    "Sunset": {
        "bg": "#1a0a0a",
        "surface": "#2a1010",
        "text": "#ffe4d4",
        "accent": "#fb923c",
        "border": "#3a1818",
        "emoji": "🌅"
    },
    "Galaxy": {
        "bg": "#05051a",
        "surface": "#0a0a2a",
        "text": "#e0e0ff",
        "accent": "#818cf8",
        "border": "#15153a",
        "emoji": "✨"
    }
}

def get_theme_css(theme):
    t = THEMES[theme]
    return f"""
    <style>
    .stApp {{
        background-color: {t['bg']};
    }}
    .stTextArea textarea {{
        background-color: {t['surface']};
        color: {t['text']};
        border: 1px solid {t['border']};
        border-radius: 12px;
        font-size: 16px;
    }}
    .emotion-card {{
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        margin-top: 20px;
    }}
    .match-card {{
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid {t['border']};
        background-color: {t['surface']};
    }}
    .pulse-card {{
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid {t['border']};
        background-color: {t['surface']};
    }}
    </style>
    """
    