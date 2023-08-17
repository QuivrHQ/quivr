"use client";

import { MentionInput } from "./components";

type ChatBarProps = {
  onSubmit: (text?: string) => void;
};

export const ChatBar = ({ onSubmit }: ChatBarProps): JSX.Element => {
  return <MentionInput onSubmit={onSubmit} />;
};
