import random
import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Ensure downloads
try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt')
    nltk.download('wordnet')

# Expanded keyword map (much richer)
intent_keywords = {
    "greeting": ["hello", "hi", "hey", "greetings"],
    "crop": ["crop", "grow", "plant", "farming", "cultivate"],
    "disease": ["disease", "infection", "spots", "blight", "fungus"],
    "fertilizer": ["fertilizer", "nutrients", "npk", "manure"],
    "water": ["water", "irrigation", "watering", "moisture"],
    "pest": ["pest", "insect", "bugs", "worms", "aphids"]
}

# Rich responses (diverse + helpful)
responses = {
    "greeting": [
        "Hello farmer! 🌱 How can I assist you today?",
        "Hi! I can help with crops, diseases, and farming advice."
    ],
    "crop": [
        "You should enter soil details (N, P, K, pH, temperature, humidity, rainfall) to get the best crop recommendation.",
        "Use the crop prediction feature by filling all soil parameters in the dashboard."
    ],
    "disease": [
        "Upload a clear leaf image and I will detect the disease using AI.",
        "Make sure the leaf is clearly visible for accurate disease detection."
    ],
    "fertilizer": [
        "Fertilizer depends on the crop; check the recommendation section after prediction.",
        "Generally, NPK fertilizers improve plant growth, but follow system suggestions."
    ],
    "water": [
        "Water needs depend on crop type, soil, and weather conditions.",
        "Avoid overwatering; maintain proper irrigation based on crop recommendation."
    ],
    "pest": [
        "Use neem oil or organic pesticides for safe pest control.",
        "Monitor crops regularly and remove infected leaves to control pests."
    ],
    "default": [
        "I can help with crop selection, disease detection, fertilizer, water, and pest control.",
        "Try asking about crops, diseases, fertilizers, or farming advice."
    ]
}


def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    return [lemmatizer.lemmatize(word) for word in tokens]


def detect_intents(words):
    detected = []

    for intent, keywords in intent_keywords.items():
        for word in words:
            if word in keywords:
                detected.append(intent)
                break

    return detected


def get_bot_response(user_input):
    words = preprocess(user_input)
    intents = detect_intents(words)

    if not intents:
        return random.choice(responses["default"])

    # MULTI-INTENT RESPONSE (SMART)
    reply = []
    for intent in intents:
        reply.append(random.choice(responses[intent]))

    return " ".join(reply)