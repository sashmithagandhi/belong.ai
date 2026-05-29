import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from emotions.keywords import EMOTION_KEYWORDS

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt_tab', quiet=True)

lemmatizer = WordNetLemmatizer()

def preprocess(text):
    # Tokenize
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords but keep emotional words
    stop_words = set(stopwords.words('english'))
    emotional_exceptions = {
        "not", "no", "never", "cant", "dont", 
        "won't", "too", "very", "but"
    }
    stop_words = stop_words - emotional_exceptions
    
    # Lemmatize
    tokens = [lemmatizer.lemmatize(t) for t in tokens 
              if t not in stop_words]
    
    return tokens

def detect_emotion(text):
    tokens = preprocess(text)
    text_lower = text.lower()
    scores = {}

    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Check both tokens and full text
            if keyword in text_lower:
                score += 2
            elif any(keyword in token for token in tokens):
                score += 1
        scores[emotion] = score

    # Get the highest scoring emotion
    detected = max(scores, key=scores.get)

    # If no emotion detected default to reflective
    if scores[detected] == 0:
        detected = "hyperreflective"

    return detected, scores