import { useTranslation } from "react-i18next";
import { LuSearch } from "react-icons/lu";

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
      autoComplete="off"
      value={searchQuery}
      onChange={(e) => setSearchQuery(e.target.value)}
      className="w-auto"
      inputClassName="w-max w-[200px] rounded-3xl border-none"
      icon={<LuSearch className="text-primary" size={20} />}
    />
  );
};
