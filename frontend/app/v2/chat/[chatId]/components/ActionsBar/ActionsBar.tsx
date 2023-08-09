import { useTranslation } from "react-i18next";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { MentionItem, MentionsInput } from "./components";
import { useActionsBar } from "./hooks/useActionsBar";

export const ActionsBar = (): JSX.Element => {
  const { t } = useTranslation(["chat"]);
  const { currentBrain, setCurrentBrainId } = useBrainContext();
  const { handleChange, value } = useActionsBar();

  return (
    <div className="flex flex-row w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-6">
      <div className="flex flex-row">
        {currentBrain !== undefined && (
          <MentionItem
            text={currentBrain.name}
            onRemove={() => setCurrentBrainId(null)}
            prefix="@"
          />
        )}
      </div>
      <div className="flex flex-1 flex-col">
        <MentionsInput
          onChange={handleChange}
          value={value}
          placeholder={t("actions_bar_placeholder")}
        />
      </div>
    </div>
  );
};
