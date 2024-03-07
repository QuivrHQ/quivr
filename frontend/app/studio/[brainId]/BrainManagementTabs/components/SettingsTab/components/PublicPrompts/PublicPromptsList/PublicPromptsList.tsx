import { ChangeEvent } from "react";

import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";
import { Prompt } from "@/lib/types/Prompt";

import { usePublicPromptsList } from "./hooks/usePublicPromptsList";

type PublicPromptsListProps = {
  options: Prompt[];
  onChange: (event: ChangeEvent<HTMLSelectElement>) => void;
  onSelect: ({ title, content }: { title: string; content: string }) => void;
};

export const PublicPromptsList = ({
  options,
  onChange,
  onSelect,
}: PublicPromptsListProps): JSX.Element => {
  const { handleOptionClick, selectedOption } = usePublicPromptsList({
    onChange,
    onSelect,
  });

  const formattedOptions = options.map((option) => {
    return { label: option.title, value: option.id };
  });

  return (
    <SingleSelector
      options={formattedOptions}
      iconName="brain"
      selectedOption={
        selectedOption
          ? {
              label: selectedOption.title,
              value: selectedOption.id,
            }
          : undefined
      }
      placeholder="Select a Quivr prompt"
      onChange={(clickedOption) => {
        const findedOption = options.find(
          (option) => option.id === clickedOption
        );
        if (findedOption) {
          handleOptionClick(findedOption);
        }
      }}
    />
  );
};
