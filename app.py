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

    if "hot" in command or "heat" in command:
        return {"decision": "turn_on_ac"}

    if "cold" in command or "chilly" in command:
        return {"decision": "turn_off_ac"}

    if "save energy" in command or "reduce power" in command:
        return {"decision": "increase_ac_temperature"}

    if "turn off ac" in command:
        return {"decision": "turn_off_ac"}

    if "turn on ac" in command:
        return {"decision": "turn_on_ac"}

    return {"decision": "no_action"}


@app.post("/decide")
async def decide(data: DecideInput):
    decision = decide_from_command(data.user_command)
    return decision

@app.post("/voice-decide")
async def voice_decide(data: VoiceInput):
    decision = decide_from_command(data.text)
    return decision
