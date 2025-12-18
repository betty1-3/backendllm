function startListening() {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert("Speech recognition not supported in this browser");
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";

  recognition.onstart = () => {
    console.log("🎙️ Listening...");
  };

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    document.getElementById("userText").innerText = text;

    // Send recognized text to backend
    sendTextToBackend(text);
  };

  recognition.onerror = (event) => {
    console.error("STT error:", event.error);
  };

  recognition.start();
}
