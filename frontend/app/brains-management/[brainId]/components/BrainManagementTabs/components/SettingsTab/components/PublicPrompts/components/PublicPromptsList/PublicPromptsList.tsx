import { ChangeEvent } from "react";

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
  const {
    handleOptionClick,
    isOpen,
    selectRef,
    selectedOption,
    toggleDropdown,
  } = usePublicPromptsList({
    onChange,
    onSelect,
  });

  return (
    <div ref={selectRef} className="relative min-w-[200px] inline-block">
      <button
        onClick={toggleDropdown}
        type="button"
        className="px-4 py-2 w-full text-gray-700 bg-white border rounded-md focus:outline-none focus:border-blue-500"
      >
        {selectedOption ? selectedOption.title : "Select a Quivr Personality"}
      </button>
      {isOpen && (
        <div className="absolute top-10 w-full bg-white border rounded-md shadow-lg">
          {options.map((option) => (
            <div
              key={option.id}
              className="px-4 py-2 cursor-pointer hover:bg-gray-100"
              onClick={() => handleOptionClick(option)}
            >
              {option.title}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
