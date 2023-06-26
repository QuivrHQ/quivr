/* eslint-disable */
"use client";
import { MdMic, MdMicOff } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { useSpeech } from "@/lib/context/ChatsProvider/hooks/useSpeech";

type MicButtonProps = {
  setMessage: (newValue: string | ((prevValue: string) => string)) => void;
};

export const MicButton = ({ setMessage }: MicButtonProps): JSX.Element => {
  const { isListening, speechSupported, startListening } = useSpeech({
    setMessage,
  });

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
};
