"use client";
import Button from "@/lib/components/ui/Button";
import { useSpeech } from "@/lib/context/ChatsProvider/hooks/useSpeech";
import { MdMic, MdMicOff } from "react-icons/md";

export function MicButton() {
  const { isListening, speechSupported, startListening } = useSpeech();

  return (
    <Button
      className="p-2 sm:px-3"
      variant={"tertiary"}
      type="button"
      onClick={startListening}
      disabled={!speechSupported}
    >
      {isListening ? (
        <MdMicOff className="text-lg sm:text-xl lg:text-2xl" />
      ) : (
        <MdMic className="text-lg sm:text-xl lg:text-2xl" />
      )}
    </Button>
  );
}
