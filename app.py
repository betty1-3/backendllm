import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_agent import get_llm_decision


# =====================================================
# DEVICE REGISTRY (SOURCE OF TRUTH)
# =====================================================
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


# =====================================================
# INPUT MODELS
# =====================================================
class VoiceInput(BaseModel):
    text: str


class DecideInput(BaseModel):
    user_command: str


# =====================================================
# FASTAPI APP
# =====================================================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# CORE LLM DECISION FUNCTION
# =====================================================
def decide_from_command(user_command: str) -> dict:
    """
    INPUT  : user_command (string)
    OUTPUT : { "actions": [...] }
    GUARANTEE: Never raises TypeError
    """

    prompt = f"""
You are a smart home command interpreter.

Your task is to convert the user's command into structured device actions.

STRICT RULES:
- Return ONLY valid JSON
- Do NOT explain anything
- Do NOT invent devices
- Use ONLY the devices listed below

DEVICES:
{json.dumps(DEVICES, indent=2)}

ALLOWED ACTIONS:
- ON
- OFF
- SET_TEMPERATURE
- INCREASE_TEMPERATURE
- DECREASE_TEMPERATURE
- SET_FAN_SPEED

USER COMMAND:
"{user_command}"

OUTPUT FORMAT:
{{
  "actions": [
    {{
      "device_id": "fan_1",
      "device_type": "Fan",
      "room": "bedroom",
      "action": "OFF",
      "value": null
    }}
  ]
}}

If no action is required, return:
{{ "actions": [] }}
"""

    # 🔒 LLM CALL (string in → dict out)
    llm_result = get_llm_decision(prompt)

    # 🔒 HARD TYPE SAFETY (NO TYPEERROR POSSIBLE)
    actions = llm_result.get("actions", [])
    if not isinstance(actions, list):
        return {"actions": []}

    validated_actions = []

    for action in actions:
        if not isinstance(action, dict):
            continue

        device_id = action.get("device_id")

        if device_id in DEVICES:
            validated_actions.append(action)

    return {"actions": validated_actions}


# =====================================================
# API ENDPOINTS
# =====================================================
@app.post("/decide")
async def decide(data: DecideInput):
    return decide_from_command(data.user_command)


@app.post("/voice-decide")
async def voice_decide(data: VoiceInput):
    return decide_from_command(data.text)
