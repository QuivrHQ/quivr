import { UUID } from "crypto";
import { useEffect, useState } from "react";
import { FormProvider, useForm } from "react-hook-form";

import { BrainSnippet } from "@/lib/components/BrainSnippet/BrainSnippet";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { Brain } from "@/lib/context/BrainProvider/types";

import styles from "./SettingsTab.module.scss";
import { GeneralInformation } from "./components/GeneralInformation/GeneralInformation";
import { ModelSelection } from "./components/ModelSelection/ModelSelection";
import { Prompt } from "./components/Prompt/Prompt";
import { useBrainFormState } from "./hooks/useBrainFormState";
// eslint-disable-next-line sort-imports
import { UsePromptProps, usePrompt } from "./hooks/usePrompt";
import { useSettingsTab } from "./hooks/useSettingsTab";

import { useBrainFetcher } from "../../hooks/useBrainFetcher";

type SettingsTabProps = {
  brainId: UUID;
  hasEditRights: boolean;
};

export const SettingsTabContent = ({
  brainId,
  hasEditRights,
}: SettingsTabProps): JSX.Element => {
  const [editSnippet, setEditSnippet] = useState<boolean>(false);
  const [snippetColor, setSnippetColor] = useState<string>("");
  const [snippetEmoji, setSnippetEmoji] = useState<string>("");

  const { brain } = useBrainFetcher({
    brainId,
  });

  const settingsTabProps = {
    brainId,
    initialColor: brain?.snippet_color,
    initialEmoji: brain?.snippet_emoji,
  };
  const { handleSubmit, formRef, accessibleModels, setIsUpdating } =
    useSettingsTab(settingsTabProps);

  const promptProps: UsePromptProps = {
    setIsUpdating,
  };

  const { submitPrompt } = usePrompt(promptProps);

  useBrainFormState();

  useEffect(() => {
    if (brain && !snippetColor && !snippetEmoji) {
      setSnippetColor(brain.snippet_color ?? "");
      setSnippetEmoji(brain.snippet_emoji ?? "");
    }
  }),
    [brain];

  if (!brain) {
    return <></>;
  }

  return (
    <>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          void handleSubmit();
        }}
        ref={formRef}
      >
        <div className={styles.main_container}>
          <div className={styles.main_infos_wrapper}>
            <span className={styles.section_title}>{brain.name} Settings</span>
            <div className={styles.inputs_wrapper}>
              <div className={styles.brain_snippet_wrapper}>
                {editSnippet && (
                  <div className={styles.edit_snippet}>
                    <BrainSnippet
                      setVisible={setEditSnippet}
                      initialColor={brain.snippet_color}
                      initialEmoji={brain.snippet_emoji}
                      onSave={async (color: string, emoji: string) => {
                        await handleSubmit(color, emoji);
                        setSnippetColor(color);
                        setSnippetEmoji(emoji);
                      }}
                    />
                  </div>
                )}
                <div
                  className={`${styles.brain_snippet} ${
                    hasEditRights ? styles.clickable : ""
                  }`}
                  style={{ backgroundColor: snippetColor }}
                  onClick={() => {
                    if (!editSnippet && hasEditRights) {
                      setEditSnippet(true);
                    }
                  }}
                >
                  <span>{snippetEmoji}</span>
                </div>
                {hasEditRights && (
                  <QuivrButton
                    label="Edit"
                    iconName="edit"
                    color="primary"
                    onClick={() => setEditSnippet(true)}
                    small={true}
                  />
                )}
              </div>
              <div className={styles.second_column}>
                <div className={styles.general_information}>
                  <GeneralInformation hasEditRights={hasEditRights} />
                  <Prompt />
                </div>
                {brain.brain_type === "doc" && (
                  <div className={styles.model_information}>
                    <ModelSelection
                      accessibleModels={accessibleModels}
                      hasEditRights={hasEditRights}
                      brainId={brainId}
                      handleSubmit={() => handleSubmit()}
                    />
                  </div>
                )}
                {hasEditRights && (
                  <div className={styles.save_button}>
                    <QuivrButton
                      label="Save"
                      iconName="upload"
                      color="primary"
                      onClick={async () => {
                        await handleSubmit();
                        await submitPrompt();
                      }}
                    />
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </form>
    </>
  );
};

export const SettingsTab = ({
  brainId,
  hasEditRights,
}: SettingsTabProps): JSX.Element => {
  const methods = useForm<Brain>();

  return (
    <FormProvider {...methods}>
      <SettingsTabContent brainId={brainId} hasEditRights={hasEditRights} />
    </FormProvider>
  );
};
