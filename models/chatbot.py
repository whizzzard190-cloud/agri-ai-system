import nltk
import random
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Download once
try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt')
    nltk.download('wordnet')

intents = {
    "greeting": ["hello", "hi", "hey"],
    "crop": ["which crop", "suggest crop", "crop recommendation"],
    "disease": ["disease", "leaf problem", "infection"],
    "fertilizer": ["fertilizer", "nutrients"],
    "water": ["water", "irrigation"],
    "pest": ["pest", "insects"]
}

responses = {
    "greeting": ["Hello farmer!", "Hi! How can I help you?"],
    "crop": ["Enter soil data to get crop recommendation."],
    "disease": ["Upload a leaf image to detect disease."],
    "fertilizer": ["Use recommended fertilizer shown in results."],
    "water": ["Water based on crop and weather conditions."],
    "pest": ["Use neem oil or safe pesticides."]
}


def preprocess(sentence):
    words = nltk.word_tokenize(sentence.lower())
    words = [lemmatizer.lemmatize(w) for w in words]
    return words


def get_bot_response(user_input):
    words = preprocess(user_input)

    for intent, patterns in intents.items():
        for pattern in patterns:
            if any(word in pattern for word in words):
                return random.choice(responses[intent])

    return "Sorry, I didn't understand. Try asking about crop, disease, or farming."