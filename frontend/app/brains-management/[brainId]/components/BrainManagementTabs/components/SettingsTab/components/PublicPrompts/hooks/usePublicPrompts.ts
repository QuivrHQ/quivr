import { ChangeEvent, useEffect, useState } from "react";

import { usePromptApi } from "@/lib/api/prompt/usePromptApi";
import { Prompt } from "@/lib/types/Prompt";

type UsePublicPromptsProps = {
  onSelect: ({ title, content }: { title: string; content: string }) => void;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePublicPrompts = ({ onSelect }: UsePublicPromptsProps) => {
  const [publicPrompts, setPublicPrompts] = useState<Prompt[]>([]);
  const { getPublicPrompts } = usePromptApi();

  useEffect(() => {
    const fetchPublicPrompts = async () => {
      setPublicPrompts(await getPublicPrompts());
    };
    void fetchPublicPrompts();
  }, []);

  const handleChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const selectedPrompt = publicPrompts.find(
      (prompt) => prompt.id === event.target.value
    );
    if (selectedPrompt) {
      onSelect({
        title: selectedPrompt.title,
        content: selectedPrompt.content,
      });
    }
  };

  return {
    publicPrompts,
    handleChange,
  };
};
