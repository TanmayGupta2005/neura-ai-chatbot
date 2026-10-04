import json
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib


# Path to custom dataset
DATASET_PATH = r"..\dataset\chatbot-intents.json"


# Load dataset
with open(DATASET_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)


texts = []
labels = []


# Read sentences from custom dataset
for sentence in data["sentences"]:
    texts.append(sentence["text"])
    labels.append(sentence["intent"])


print("================================")
print("CUSTOM DATASET LOADED")
print("================================")
print(f"Training examples: {len(texts)}")
print(f"Intents: {len(set(labels))}")


# Create ML pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# Train model
model.fit(texts, labels)


# Create models directory
os.makedirs("models", exist_ok=True)


# Save model
joblib.dump(model, "models/intent_model.pkl")


print("================================")
print("ML MODEL TRAINED SUCCESSFULLY")
print("================================")
print(f"Training examples: {len(texts)}")
print(f"Intents: {len(set(labels))}")
print("Model saved to: models/intent_model.pkl")