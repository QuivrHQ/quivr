"use client";

import { MentionInput } from "./components";

type ChatBarProps = {
  onSubmit: () => void;
  setMessage: (text: string) => void;
  message: string;
};

export const ChatBar = ({
  onSubmit,
  setMessage,
  message,
}: ChatBarProps): JSX.Element => {
  return (
    <MentionInput
      message={message}
      setMessage={setMessage}
      onSubmit={onSubmit}
    />
  );
};
