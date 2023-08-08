import { useTranslation } from "react-i18next";
import { Mention } from "react-mentions"; // Import the required components

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { MentionItem, MentionsInput } from "./components";
import { useActionsBar } from "./hooks/useActionsBar";

export const ActionsBar = (): JSX.Element => {
  const { t } = useTranslation(["chat"]);
  const { allBrains } = useBrainContext();
  const {
    handleAddMention,
    handleChange,
    handleRemoveMention,
    mentions,
    value,
  } = useActionsBar();

  return (
    <div className="flex flex-row w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-6">
      <div className="flex flex-row">
        {mentions.map((mention) => (
          <MentionItem
            key={mention.id}
            text={mention.display}
            onRemove={() => handleRemoveMention(mention.id)}
            prefix="@"
          />
        ))}
      </div>
      <div className="flex flex-1 flex-col">
        <MentionsInput
          onChange={handleChange}
          value={value}
          placeholder={t("actions_bar_placeholder")}
          disabled={mentions.length !== 0}
        >
          <Mention
            trigger="@"
            data={allBrains.map(({ id, name }) => ({ id, display: name }))}
            renderSuggestion={(_, __, content) => (
              <p className="mb-2">{content}</p>
            )}
            onAdd={(id, display) => handleAddMention(String(id), display)}
            displayTransform={() => ""}
          />
        </MentionsInput>
      </div>
    </div>
  );
};
