"use client";
import { MdMic, MdMicOff } from "react-icons/md";
import Button from "../../../../components/ui/Button";
import { useSpeech } from "../../../ChatsProvider/hooks/useSpeech";

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
