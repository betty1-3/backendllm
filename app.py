from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from llm_agent import get_llm_decision

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
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

@app.post("/decide")
def decide(data: ContextInput):

    context = {
        "user_command": data.user_command,
        "hour_of_day": datetime.now().hour,
        "ambient_temperature": data.ambient_temperature,
        "occupancy": data.occupancy,
        "ac_power": data.ac_power,
        "set_temperature": data.set_temperature,
        "total_current_load": data.total_current_load,
        "cumulative_energy": data.cumulative_energy
    }

    suggested_actions = get_llm_decision(context)
    validated_actions = validate_actions(suggested_actions, context)

    return {
        "actions": validated_actions,
        "rejected_count": len(suggested_actions) - len(validated_actions)
    }
