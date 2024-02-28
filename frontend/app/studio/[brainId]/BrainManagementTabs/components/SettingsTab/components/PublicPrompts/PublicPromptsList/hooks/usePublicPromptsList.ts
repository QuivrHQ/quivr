import { ChangeEvent, useEffect, useRef, useState } from "react";

import { Prompt } from "@/lib/types/Prompt";

type UsePublicPromptsListProps = {
  onChange: (event: ChangeEvent<HTMLSelectElement>) => void;
  onSelect: ({ title, content }: { title: string; content: string }) => void;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePublicPromptsList = ({
  onChange,
  onSelect,
}: UsePublicPromptsListProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState<Prompt | null>(null);
  const selectRef = useRef<HTMLDivElement>(null);

  const toggleDropdown = () => {
    setIsOpen((prevIsOpen) => !prevIsOpen);
  };

  const handleOptionClick = (option: Prompt) => {
    setSelectedOption(option);
    setIsOpen(false);
    onChange({
      target: { value: option.id },
    } as ChangeEvent<HTMLSelectElement>);
    onSelect({
      title: option.title,
      content: option.content,
    });
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (
      selectRef.current &&
      !selectRef.current.contains(event.target as Node)
    ) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("click", handleClickOutside, true);

    return () => {
      document.removeEventListener("click", handleClickOutside, true);
    };
  }, []);

  return {
    isOpen,
    selectedOption,
    selectRef,
    toggleDropdown,
    handleOptionClick,
  };
};
