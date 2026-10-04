from fastapi import FastAPI
from pydantic import BaseModel
from model import generate_response

app = FastAPI()


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation: list[ChatMessage] = []


@app.get("/")
def home():
    return {
        "message": "AI Chatbot ML Service is running",
        "model": "Qwen2.5-0.5B-Instruct"
    }


def get_user_name(conversation):

    for item in conversation:

        if item["role"] != "user":
            continue

        text = item["content"].strip()

        lower_text = text.lower()

        patterns = [
            "my name is ",
            "i am ",
            "i'm "
        ]

        for pattern in patterns:

            if lower_text.startswith(pattern):

                name = text[len(pattern):].strip()

                if name:
                    return name.rstrip(".!?")

    return None


def create_conversation_summary(conversation):

    if not conversation:
        return "We haven't talked about anything yet."

    topics = []

    for item in conversation:

        if item["role"] == "user":

            text = item["content"].strip()

            if text:
                topics.append(text)

    if not topics:
        return "We haven't talked about anything yet."

    recent_topics = topics[-5:]

    summary = "So far, we talked about:\n"

    for topic in recent_topics:
        summary += f"• {topic}\n"

    return summary.strip()


@app.post("/predict")
def predict(request: ChatRequest):

    message = request.message.strip()

    if not message:
        return {
            "reply": "Please enter a message.",
            "intent": "unknown",
            "confidence": 0
        }


    conversation = [
        {
            "role": item.role,
            "content": item.content
        }
        for item in request.conversation
    ]


    lower_message = message.lower()


    # -----------------------------
    # NAME MEMORY
    # -----------------------------

    if "what is my name" in lower_message:

        name = get_user_name(conversation)

        if name:

            return {
                "reply": f"Your name is {name}.",
                "intent": "memory_name",
                "confidence": 1.0
            }

        return {
            "reply": "You haven't told me your name yet.",
            "intent": "memory_name",
            "confidence": 1.0
        }


    # -----------------------------
    # CONVERSATION SUMMARY
    # -----------------------------

    summary_questions = [
    "what did we talk",
    "what have we talked",
    "what did we discuss",
    "what have we discussed",
    "what are we talking about",
    "summarize our conversation",
    "summarise our conversation",
    "summary of our conversation",
    "summarize the conversation",
    "summarise the conversation",
    "what happened in our conversation"
]


    if any(
        question in lower_message
        for question in summary_questions
    ):

        summary = create_conversation_summary(
            conversation
        )

        return {
            "reply": summary,
            "intent": "conversation_summary",
            "confidence": 1.0
        }


    # -----------------------------
    # NORMAL AI RESPONSE
    # -----------------------------

    try:

        reply = generate_response(
            message,
            conversation
        )

        return {
            "reply": reply,
            "intent": "generative_ai",
            "confidence": 1.0
        }

    except Exception as e:

        return {
            "reply": "Sorry, I encountered an error while generating a response.",
            "intent": "error",
            "confidence": 0,
            "error": str(e)
        }