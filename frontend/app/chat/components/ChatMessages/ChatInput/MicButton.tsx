"use client";
import { MdMic, MdMicOff } from "react-icons/md";
import Button from "../../../../components/ui/Button";
import { useSpeech } from "../../../ChatsProvider/hooks/useSpeech";

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
