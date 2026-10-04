from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import random
from datetime import datetime

app = FastAPI()

# Load ML model
model = joblib.load("models/intent_model.pkl")


class ChatRequest(BaseModel):
    message: str


# Responses for each intent
responses = {
    "greeting": [
        "Hello! How can I help you?",
        "Hi! What would you like to know?",
        "Hey! How can I assist you today?"
    ],

    "goodbye": [
        "Goodbye! Have a great day!",
        "See you later!",
        "Bye! Take care!"
    ],

    "thanks": [
        "You're welcome!",
        "Happy to help!",
        "Anytime!"
    ],

    "howAreYou": [
        "I'm doing great! Thanks for asking.",
        "I'm doing well and ready to help!",
        "I'm good! What can I help you with?"
    ],

    "capabilities": [
        "I can answer questions, help with programming, education, general topics, and more.",
        "I can chat with you, understand your requests, and provide helpful answers.",
        "You can ask me about programming, learning, general questions, and more."
    ],

    "help": [
        "Sure! Tell me what you need help with.",
        "Of course! What can I help you with?",
        "I'm here to help. Tell me what you're working on."
    ],

    "name": [
        "I'm your AI chatbot.",
        "You can call me your AI assistant.",
        "I'm an AI chatbot built to help you."
    ],

    "whoAreYou": [
        "I'm an AI chatbot designed to understand your messages and respond to them.",
        "I'm your AI assistant. I can understand different types of requests.",
        "I'm a machine-learning powered chatbot."
    ],

    "time": [
        f"The current time is {datetime.now().strftime('%I:%M %p')}.",
    ],

    "date": [
        f"Today's date is {datetime.now().strftime('%d %B %Y')}.",
    ],

    "smallTalk": [
        "Sure! Let's chat. What would you like to talk about?",
        "I'm ready to chat! Tell me what's on your mind.",
        "Of course! Let's have a conversation."
    ],

    "affirmation": [
        "Great!",
        "Okay!",
        "Sounds good!",
        "Absolutely!"
    ],

    "negative": [
        "Okay, no problem.",
        "Understood.",
        "That's completely fine."
    ],

    "repeat": [
        "Sure! I'll repeat that. What would you like me to repeat?",
        "Of course. Which part should I repeat?",
        "Sure, I can repeat that."
    ]
}


@app.get("/")
def home():
    return {
        "message": "AI Chatbot ML Service is running"
    }


@app.post("/predict")
def predict(request: ChatRequest):
    message = request.message.strip()

    if not message:
        return {
            "reply": "Please enter a message.",
            "intent": "unknown",
            "confidence": 0
        }

    # Predict intent
    prediction = model.predict([message])[0]

    # Calculate confidence
    probabilities = model.predict_proba([message])[0]
    confidence = max(probabilities)

    # Low-confidence fallback
    if confidence < 0.40:
        return {
            "reply": "I'm not sure I understood that. Could you please rephrase it?",
            "intent": "unknown",
            "confidence": round(float(confidence), 3)
        }

    # Get response
    reply = random.choice(
        responses.get(
            prediction,
            ["I'm not sure how to answer that."]
        )
    )

    return {
        "reply": reply,
        "intent": prediction,
        "confidence": round(float(confidence), 3)
    }