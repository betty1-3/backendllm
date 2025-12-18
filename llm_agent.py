import requests
import json
import re
# 1️⃣ Imports
import os
from mistralai.client import MistralClient   # or whatever lib you use

# 2️⃣ STEP 1: Read API key from environment
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise RuntimeError("MISTRAL_API_KEY is not set")

# 3️⃣ STEP 2: Create the LLM client (THIS is Step 2)
client = MistralClient(api_key=MISTRAL_API_KEY)




# =========================
# CONFIG
# =========================



API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "mistralai/mistral-7b-instruct"



HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "Smart Home Energy Agent"
}

# =========================
# JSON EXTRACTION (ROBUST)
# =========================

def extract_json(text):
    """
    Extracts the first JSON array found in LLM output.
    Prevents crashes if model adds extra text.
    """
    try:
        match = re.search(r"\[[\s\S]*\]", text)
        if not match:
            return []
        return json.loads(match.group())
    except Exception as e:
        print("❌ JSON parsing failed:", e)
        return []

# =========================
# LLM DECISION FUNCTION
# =========================

def get_llm_decision(context):
     response = client.chat(
        model="mistral-small",
        messages=[
            {"role": "system", "content": "You are a smart home assistant"},
            {"role": "user", "content": context["user_command"]}
        ]
    """
    context must include:
    - user_command
    - hour_of_day
    - ambient_temperature
    - occupancy
    - ac_power
    - set_temperature
    - total_current_load
    - cumulative_energy
    """

    prompt = f"""
You are a smart home assistant.

Based on the sensor data and the user's command, decide what actions to take
to optimize energy usage while maintaining comfort.

Sensor data:
- Hour of day: {context['hour_of_day']}
- Ambient temperature: {context['ambient_temperature']} °C
- Occupancy detected: {context['occupancy']}
- AC power state: {context['ac_power']}
- AC set temperature: {context['set_temperature']} °C
- Total current load: {context['total_current_load']} kW
- Cumulative energy usage: {context['cumulative_energy']} kWh

User command:
"{context['user_command']}"

Available devices:
- AC
- Fan
- Light

Possible actions:
- AC: turn_on, turn_off, increase_temp, decrease_temp
- Fan: turn_on, turn_off
- Light: turn_on, turn_off

Return your answer as a JSON array.
If no action is needed, return an empty array [].

Example:
[
  {{
    "device": "AC",
    "action": "turn_off",
    "reason": "room is unoccupied and energy usage is high"
  }}
]
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": 300
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)



    if response.status_code != 200:
        print("❌ LLM API error")
        return []

    content = response.json()["choices"][0]["message"]["content"]



    return extract_json(content)
