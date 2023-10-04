import { useTranslation } from "react-i18next";

import Field from "@/lib/components/ui/Field";

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
    <Field
      name="brainsearch"
      placeholder={t("searchBrain")}
      autoFocus
      autoComplete="off"
      value={searchQuery}
      onChange={(e) => setSearchQuery(e.target.value)}
    />
  );
};
