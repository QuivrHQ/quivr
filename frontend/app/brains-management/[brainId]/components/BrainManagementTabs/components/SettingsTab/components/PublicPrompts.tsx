import * as Accordion from "@radix-ui/react-accordion";

import { Prompt } from "@/lib/types/Prompt";
import { usePromptApi } from "@/lib/api/prompt/usePromptApi";
import { useEffect } from "react";

type PublicPromptsProps = {
  onSelect: ({ title, content }: { title: string; content: string }) => void;
};

export const PublicPrompts = ({
  onSelect,
}: PublicPromptsProps): JSX.Element => {
  const [publicPrompts, setPublicPrompts] = useState<Prompt[]>([]);
  const { getPrompt } = usePromptApi();

  useEffect(() => {
    setPublicPrompts(await getPrompt());
  }, []);

  return (
    <Accordion.Root
      className="AccordionRoot"
      type="single"
      defaultValue="item-1"
      collapsible
    >
      <Accordion.Item className="AccordionItem" value="item-1">
        <Accordion.Trigger>Is it accessible?</Accordion.Trigger>
        <Accordion.Content>
          Yes. It adheres to the WAI-ARIA design pattern.
        </Accordion.Content>
      </Accordion.Item>

      <Accordion.Item className="AccordionItem" value="item-2">
        <Accordion.Trigger>Is it unstyled?</Accordion.Trigger>
        <Accordion.Content>
          Yes. It's unstyled by default, giving you freedom over the look and
          feel.
        </Accordion.Content>
      </Accordion.Item>

      <Accordion.Item className="AccordionItem" value="item-3">
        <Accordion.Trigger>Can it be animated?</Accordion.Trigger>
        <Accordion.Content className="Accordion.Content">
          <div className="Accordion.ContentText">
            Yes! You can animate the Accordion with CSS or JavaScript.
          </div>
        </Accordion.Content>
      </Accordion.Item>
    </Accordion.Root>
  );
};
