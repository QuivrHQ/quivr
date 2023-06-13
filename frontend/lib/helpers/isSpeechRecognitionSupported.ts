export function isSpeechRecognitionSupported() {
  if (
    typeof window !== "undefined" &&
    ("SpeechRecognition" in window || "webkitSpeechRecognition" in window)
  ) {
    return true;
  }
  return false;
}
