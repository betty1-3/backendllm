import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_agent import get_llm_decision


# -------------------------
# Device registry
# -------------------------
DEVICES = {
    "light_1": {
        "device_id": "light_1",
        "device_type": "Light",
        "room": "living_room"
    },
    "fan_1": {
        "device_id": "fan_1",
        "device_type": "Fan",
        "room": "bedroom"
    },
    "ac_1": {
        "device_id": "ac_1",
        "device_type": "AC",
        "room": "living_room"
    }
}


# -------------------------
# Models
# -------------------------
class VoiceInput(BaseModel):
    text: str

class DecideInput(BaseModel):
    user_command: str


# -------------------------
# App setup
# -------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# LLM-based decision
# -------------------------
def decide_from_command(user_command: str):

    prompt = f"""
You are a smart home command interpreter.

Convert the user's command into structured device actions.

Rules:
- Return ONLY valid JSON
- Do NOT explain anything
- Do NOT invent devices
- Use ONLY these devices:

{json.dumps(DEVICES, indent=2)}

Allowed actions:
- ON
- OFF
- SET_TEMPERATURE
- INCREASE_TEMPERATURE
- DECREASE_TEMPERATURE
- SET_FAN_SPEED

User command:
"{user_command}"

Output format:
{{
  "actions": [
    {{
      "device_id": "ac_1",
      "device_type": "AC",
      "room": "living_room",
      "action": "ON",
      "value": null
    }}
  ]
}}

If no action is required, return:
{{ "actions": [] }}
"""

    actions = get_llm_decision(prompt)

    # Hard safety check
    validated = []
    for action in actions.get("actions", []):
        device_id = action.get("device_id")
        if device_id in DEVICES:
            validated.append(action)

    return {"actions": validated}


# -------------------------
# Endpoints
# -------------------------
@app.post("/decide")
async def decide(data: DecideInput):
    return decide_from_command(data.user_command)


@app.post("/voice-decide")
async def voice_decide(data: VoiceInput):
    return decide_from_command(data.text)
