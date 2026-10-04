from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
MODEL_PATH = r"E:\hf-models"

print("Loading AI model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    cache_dir=MODEL_PATH
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    cache_dir=MODEL_PATH
)

print("AI model loaded successfully!")


def generate_response(message, conversation=None):

    messages = [
        {
            "role": "system",
            "content": """You are Neura, a helpful conversational AI assistant.

IMPORTANT RULES:

1. Remember information from the conversation.
2. If the user tells you their name, remember it during this conversation.
3. If the user asks "What is my name?", answer using the name they previously provided.
4. If the user asks "What did we talk about?", summarize the previous conversation.
5. Understand follow-up questions using previous messages.
6. Never say that you cannot access the conversation history when the history is provided to you.
7. Give clear, natural and concise answers.
8. Do not invent information that was not provided by the user."""
        }
    ]


    # Add previous conversation
    if conversation:

        # Keep only the most recent 10 messages
        recent_conversation = conversation[-10:]

        for item in recent_conversation:

            role = item.get("role")
            content = item.get("content", "").strip()

            if role in ["user", "assistant"] and content:

                messages.append({
                    "role": role,
                    "content": content
                })


    # Add current user message
    messages.append({
        "role": "user",
        "content": message
    })


    # Convert conversation to Qwen chat format
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )


    inputs = tokenizer(
        [text],
        return_tensors="pt"
    )


    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.5,
            top_p=0.9,
            do_sample=True
        )


    # Only decode newly generated tokens
    response = outputs[0][
        inputs.input_ids.shape[1]:
    ]


    return tokenizer.decode(
        response,
        skip_special_tokens=True
    ).strip()


if __name__ == "__main__":

    conversation = [
        {
            "role": "user",
            "content": "My name is Tanmay."
        },
        {
            "role": "assistant",
            "content": "Nice to meet you, Tanmay!"
        }
    ]

    response = generate_response(
        "What is my name?",
        conversation
    )

    print("\nAI:", response)