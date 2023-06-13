"use client";
import Button from "@/lib/components/ui/Button";
import { useSpeech } from "@/lib/context/ChatsProvider/hooks/useSpeech";
import { MdMic, MdMicOff } from "react-icons/md";

export function MicButton() {
  const { isListening, speechSupported, startListening } = useSpeech();

  return (
    <Button
      className="px-3"
      variant={"tertiary"}
      type="button"
      onClick={startListening}
      disabled={!speechSupported}
    >
      {isListening ? (
        <MdMicOff className="text-2xl" />
      ) : (
        <MdMic className="text-2xl" />
      )}
    </Button>
  );
}
