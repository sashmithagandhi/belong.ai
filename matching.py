from emotions.keywords import EMOTION_KEYWORDS
from emotion_detector import detect_emotion

# Simulated user pool with emotional states
SIMULATED_USERS = [
    {"id": "user_001", "alias": "Quiet Storm", "entry": "I keep overthinking everything at night. My mind never stops."},
    {"id": "user_002", "alias": "Faded Echo", "entry": "I feel numb. Nothing excites me anymore. Just empty."},
    {"id": "user_003", "alias": "Broken Compass", "entry": "I am so overwhelmed. Too much is happening at once."},
    {"id": "user_004", "alias": "Silent Wave", "entry": "I smile but inside I am hiding so much pain."},
    {"id": "user_005", "alias": "Lost Frequency", "entry": "People drain me. I just want to be alone and recharge."},
    {"id": "user_006", "alias": "Drifting Cloud", "entry": "I can't focus on anything. My thoughts are scattered everywhere."},
    {"id": "user_007", "alias": "Hollow Reed", "entry": "I feel disconnected from everyone around me. Like I don't belong."},
    {"id": "user_008", "alias": "Midnight Flame", "entry": "I am grateful today. Feeling hopeful and calm for once."},
]

def calculate_resonance(emotion1, scores1, emotion2, scores2):
    if emotion1 == emotion2:
        base = 75
    else:
        base = 30

    # Calculate similarity based on scores
    all_emotions = list(scores1.keys())
    similarity = 0
    for e in all_emotions:
        s1 = scores1.get(e, 0)
        s2 = scores2.get(e, 0)
        if s1 + s2 > 0:
            similarity += min(s1, s2) / max(s1, s2) * 10

    resonance = min(99, base + similarity)
    return round(resonance)

def find_matches(user_entry, top_n=3):
    user_emotion, user_scores = detect_emotion(user_entry)
    matches = []

    for user in SIMULATED_USERS:
        other_emotion, other_scores = detect_emotion(user["entry"])
        resonance = calculate_resonance(
            user_emotion, user_scores,
            other_emotion, other_scores
        )
        matches.append({
            "alias": user["alias"],
            "emotion": other_emotion,
            "resonance": resonance
        })

    # Sort by resonance score
    matches = sorted(matches, key=lambda x: x["resonance"], reverse=True)
    return matches[:top_n], user_emotion