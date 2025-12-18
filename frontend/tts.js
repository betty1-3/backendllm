function speakText(text) {
  if (!window.speechSynthesis) {
    console.error("TTS not supported in this browser");
    return;
  }

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";

  speechSynthesis.speak(utterance);
}
