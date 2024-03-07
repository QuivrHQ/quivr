import { KeyboardEvent } from "react";

type UseEditorProps = {
  onSubmit: () => void;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useEditor = ({ onSubmit }: UseEditorProps) => {
  const submitOnEnter = (ev: KeyboardEvent<HTMLDivElement>) => {
    if (ev.key === "Enter" && !ev.shiftKey && !ev.metaKey) {
      onSubmit();
    }
  };

  return {
    submitOnEnter,
  };
};
