import * as Accordion from "@radix-ui/react-accordion";
import { ChangeEvent, useEffect, useState } from "react";

import { usePromptApi } from "@/lib/api/prompt/usePromptApi";
import { Prompt } from "@/lib/types/Prompt";

type PublicPromptsProps = {
  onSelect: ({ title, content }: { title: string; content: string }) => void;
};

export const PublicPrompts = ({
  onSelect,
}: PublicPromptsProps): JSX.Element => {
  const [publicPrompts, setPublicPrompts] = useState<Prompt[]>([]);

  const { getPublicPrompts } = usePromptApi();

  const fetchPublicPrompts = async () => {
    setPublicPrompts(await getPublicPrompts());
  };

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

  useEffect(() => {
    void fetchPublicPrompts();
  }, []);

  return (
    <Accordion.Root className="AccordionRoot" type="single" collapsible>
      <Accordion.Item className="AccordionItem" value="item-1">
        <Accordion.Trigger>Pick in public prompts</Accordion.Trigger>
        <Accordion.Content>
          <select
            onChange={handleChange}
            className="px-5 w-full py-2 dark:bg-gray-700 bg-gray-200 rounded-md"
          >
            {publicPrompts.map((prompt) => (
              <option value={prompt.id} key={prompt.id}>
                {prompt.title}
              </option>
            ))}
          </select>
        </Accordion.Content>
      </Accordion.Item>
    </Accordion.Root>
  );
};
