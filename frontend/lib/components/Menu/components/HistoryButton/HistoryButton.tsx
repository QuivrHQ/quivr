import { useTranslation } from "react-i18next";

import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";

export const HistoryButton = (): JSX.Element => {
  const { t } = useTranslation("chat");

  return (
    <FoldableSection label={t("history")} icon="history" darkMode={true}>
      History
    </FoldableSection>
  );
};
