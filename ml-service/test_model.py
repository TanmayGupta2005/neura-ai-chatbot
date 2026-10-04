import joblib

model = joblib.load("models/intent_model.pkl")

while True:
    message = input("\nYou: ")

    if message.lower() == "exit":
        break

    prediction = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]

    confidence = max(probabilities)

    print("Intent:", prediction)
    print("Confidence:", round(confidence, 2))