import json
import openai
from datetime import datetime

# Set API key (best to load from environment variables in real use)
openai.api_key = ""

# (1) Context prompt (rules for the AI)
context_prompt = """
You are a polite, helpful AI assistant.
Always consider metadata before answering.
If priority is 'high', keep the answer concise but accurate.
If priority is 'low', you may elaborate and give examples.
"""

# (2) Metadata (could come from a DB or API)
metadata = {
    "user_name": "Jhon",
    "language": "en",
    "priority": "high",  # Could be: high, medium, low
    "topic": "AI basics"
}

# (3) User input
user_message = "Explain what a neural network is."

# (4) Decide model dynamically based on metadata
model_map = {
    "high": "gpt-4o-mini",  # faster response for urgent queries
    "medium": "gpt-4o",
    "low": "gpt-4o"  # more detailed answers
}
selected_model = model_map.get(metadata["priority"], "gpt-4o-mini")

# (5) Merge context + metadata + user input
full_prompt = f"""
{context_prompt}

Metadata:
{json.dumps(metadata)}

User request:
{user_message}

Respond in {metadata['language']} and address {metadata['user_name']} by name.
"""

# (6) AI request with error handling
try:
    response = openai.ChatCompletion.create(
        model=selected_model,
        messages=[
            {"role": "system", "content": full_prompt}
        ],
        temperature=0.5  # moderate creativity
    )

    # (7) Extract AI output
    output_text = response.choices[0].message["content"].strip()

    # (8) Post-processing: format differently based on priority
    if metadata["priority"] == "high":
        output_text = f"[URGENT REPLY] {output_text}"
    else:
        output_text = f"Hello {metadata['user_name']},\n\n{output_text}"

    # (9) Logging (Python dev ensures traceability)
    with open("ai_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.now()} | {metadata} | {user_message} | {output_text}\n")

    # (10) Output final response
    print(output_text)

except Exception as e:
    print(f"Error occurred: {e}")
