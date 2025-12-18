async function sendTextToBackend(text) {
  // 🔒 Guard against empty / undefined speech input
  if (!text || typeof text !== "string" || text.trim() === "") {
    console.warn("⚠️ Ignoring empty speech input");
    return;
  }

  const payload = {
    user_command: text.trim(),
    ambient_temperature: 30,
    occupancy: false,
    ac_power: "on",
    set_temperature: 22,
    total_current_load: 5.0,
    cumulative_energy: 14.2
  };

  let response;

  try {
    response = await fetch("http://127.0.0.1:8000/decide", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });
  } catch (err) {
    console.error("❌ Network error:", err);
    return;
  }


if (!response.ok) {
  const err = await response.text();
  console.error("422 DETAILS:", err);

  return;
}


  const data = await response.json();

  // 🛡 Defensive access
  const actions = Array.isArray(data.actions) ? data.actions : [];

  let summary;
  if (actions.length === 0) {
    summary = "No action is needed right now.";
  } else {
    summary = actions
      .map(a => `${a.action.replace("_", " ")} ${a.device}`)
      .join(", ");
  }

  document.getElementById("assistantText").innerText = summary;
  speakText(summary);
}
