from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from llm_agent import get_llm_decision
from pydantic import BaseModel


class VoiceInput(BaseModel):
    text: str

class DecideInput(BaseModel):
    user_command: str





app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContextInput(BaseModel):
    user_command: str
    ambient_temperature: float
    occupancy: bool
    ac_power: str
    set_temperature: float
    total_current_load: float
    cumulative_energy: float

def validate_actions(actions, context):
    validated = []
    for action in actions:
        device = action.get("device")
        act = action.get("action")

        if not context["occupancy"] and act == "turn_on":
            continue

        if device == "AC" and context["ac_power"] == "off" and act == "turn_off":
            continue

        if device == "AC" and context["ac_power"] == "off" and act in ["increase_temp", "decrease_temp"]:
            continue

        if device == "AC":
            if act == "increase_temp" and context["ambient_temperature"] <= context["set_temperature"]:
                continue
            if act == "decrease_temp" and context["ambient_temperature"] >= context["set_temperature"]:
                continue

        validated.append(action)

    return validated

def decide_from_command(user_command: str):
    command = user_command.lower()

    actions = []

    # 🔥 Temperature-related (AC)
    if "hot" in command or "warm" in command:
        actions.append(
            make_action(
                device_id="ac_1",
                action="ON",
                set_temperature=24
            )
        )

    if "cold" in command or "chilly" in command:
        actions.append(
            make_action(
                device_id="ac_1",
                action="OFF"
            )
        )

    if "save energy" in command or "reduce power" in command:
        actions.append(
            make_action(
                device_id="ac_1",
                action="INCREASE_TEMPERATURE",
                delta=2
            )
        )

    # 💡 Lights
    if "turn on light" in command or "lights on" in command:
        actions.append(
            make_action(
                device_id="light_1",
                action="ON"
            )
        )

    if "turn off light" in command or "lights off" in command:
        actions.append(
            make_action(
                device_id="light_1",
                action="OFF"
            )
        )

    # 🌀 Fan
    if "turn on fan" in command:
        actions.append(
            make_action(
                device_id="fan_1",
                action="ON",
                speed=2
            )
        )

    if "turn off fan" in command:
        actions.append(
            make_action(
                device_id="fan_1",
                action="OFF"
            )
        )

    if not actions:
        return {
            "actions": [],
            "message": "No matching action"
        }

    return {
        "actions": actions
    }

def make_action(device_id, action, **kwargs):
    payload = {
        "device_id": device_id,
        "action": action
    }
    payload.update(kwargs)
    return payload



@app.post("/decide")
async def decide(data: DecideInput):
    decision = decide_from_command(data.user_command)
    return decision

@app.post("/voice-decide")
async def voice_decide(data: VoiceInput):
    decision = decide_from_command(data.text)
    return decision


