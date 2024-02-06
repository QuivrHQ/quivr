import { useTranslation } from "react-i18next";

import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

type BrainSearchBarProps = {
  searchQuery: string;
  setSearchQuery: (searchQuery: string) => void;
};

export const BrainSearchBar = ({
  searchQuery,
  setSearchQuery,
}: BrainSearchBarProps): JSX.Element => {
  const { t } = useTranslation(["brain"]);

  return (
    <TextInput
      iconName="search"
      label={t("searchBrain")}
      inputValue={searchQuery}
      setInputValue={setSearchQuery}
    />
  );
};
