"use client";
import { Dispatch, SetStateAction } from "react";
import { MdMic, MdMicOff } from "react-icons/md";
import Button from "../../components/ui/Button";
import { useSpeech } from ".././hooks/useSpeech";

export function MicButton({
  setQuestion,
}: {
  setQuestion: Dispatch<SetStateAction<string>>;
}) {
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
