import { useEffect, useState } from "react";
import { isSpeechRecognitionSupported } from "../helpers/isSpeechRecognitionSupported";
import { useQuestion } from "./useQuestion";

export const useSpeech = () => {
  const [isListening, setIsListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const { setQuestion } = useQuestion();

  useEffect(() => {
    if (isSpeechRecognitionSupported()) {
      setSpeechSupported(true);
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

      const mic = new SpeechRecognition();

      mic.continuous = true;
      mic.interimResults = false;
      mic.lang = "en-US";

      mic.onstart = () => {
        console.log("Mics on");
      };

      mic.onend = () => {
        console.log("Mics off");
      };

      mic.onerror = (event: SpeechRecognitionErrorEvent) => {
        console.log(event.error);
        setIsListening(false);
      };

      mic.onresult = (event: SpeechRecognitionEvent) => {
        const interimTranscript =
          event.results[event.results.length - 1][0].transcript;
        setQuestion((prevQuestion) => prevQuestion + interimTranscript);
      };

      if (isListening) {
        mic.start();
      }

      return () => {
        if (mic) {
          mic.stop();
        }
      };
    }
  }, [isListening]);

  const startListening = () => {
    setIsListening((prevIsListening) => !prevIsListening);
  };

  return { startListening, speechSupported, isListening };
};
