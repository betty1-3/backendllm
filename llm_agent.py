import os
import json
from openai import OpenAI

# -------------------------
# OpenRouter client
# -------------------------
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

if not os.getenv("OPENROUTER_API_KEY"):
    raise RuntimeError("OPENROUTER_API_KEY is not set")


# -------------------------
# LLM decision function
# -------------------------
def get_llm_decision(prompt: str) -> dict:
    """
    Sends prompt to LLM and returns parsed JSON.
    Always returns a dict with key: 'actions'
    """

    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON-only response generator. Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON strictly
        data = json.loads(content)

        # Safety: enforce schema
        if not isinstance(data, dict):
            return {"actions": []}

        if "actions" not in data or not isinstance(data["actions"], list):
            return {"actions": []}

        return data

    except json.JSONDecodeError:
        # LLM returned non-JSON
        return {"actions": []}

    except Exception as e:
        # Network / API / timeout issues
        print("LLM ERROR:", e)
        return {"actions": []}
