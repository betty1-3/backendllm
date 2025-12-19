from openai import OpenAI
import os
import json
import re



# =========================
# ENV + CLIENT SETUP
# =========================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)



# =========================
# JSON EXTRACTION (ROBUST)
# =========================

def extract_json(text):
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

Return your answer as a JSON array only.
If no action is needed, return [].
"""

response = client.chat.completions.create(
    model="mistralai/mistral-7b-instruct",
    messages=[
        {"role": "system", "content": "Return only valid JSON."},
        {"role": "user", "content": prompt}
    ],
    temperature=0
)



    content = response.choices[0].message.content
    return extract_json(content)
