from llm_agent import get_llm_decision
import json

context = {
    "user_command": "save energy",
    "hour_of_day": 23,
    "ambient_temperature": 30,
    "occupancy": False,
    "ac_power": "on",
    "set_temperature": 22,
    "total_current_load": 5.2,
    "cumulative_energy": 14.7
}

actions = get_llm_decision(context)

print("\nFINAL PARSED OUTPUT:")
print(json.dumps(actions, indent=2))
