import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def get_llm_decision(prompt: str) -> dict:
    """
    INPUT: prompt (str)
    OUTPUT: dict { "actions": [...] }
    NEVER returns string
    """

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "Return ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        data = json.loads(content)
    except Exception:
        return {"actions": []}

    # HARD GUARANTEE
    if not isinstance(data, dict):
        return {"actions": []}

    if "actions" not in data or not isinstance(data["actions"], list):
        return {"actions": []}

    return data
