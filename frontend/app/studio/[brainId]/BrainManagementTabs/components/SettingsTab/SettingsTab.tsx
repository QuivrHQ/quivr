import { UUID } from "crypto";
import { useEffect, useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { FaSpinner } from "react-icons/fa";

import { BrainSnippet } from "@/lib/components/BrainSnippet/BrainSnippet";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { Brain } from "@/lib/context/BrainProvider/types";

import styles from "./SettingsTab.module.scss";
import { GeneralInformation } from "./components/GeneralInformation/GeneralInformation";
import { ModelSelection } from "./components/ModelSelection/ModelSelection";
import { Prompt } from "./components/Prompt/Prompt";
import { useBrainFormState } from "./hooks/useBrainFormState";
import { usePermissionsController } from "./hooks/usePermissionsController";
import { UsePromptProps } from "./hooks/usePrompt";
import { useSettingsTab } from "./hooks/useSettingsTab";

import { useBrainFetcher } from "../../hooks/useBrainFetcher";

type SettingsTabProps = {
  brainId: UUID;
};

export const SettingsTabContent = ({
  brainId,
}: SettingsTabProps): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const [editSnippet, setEditSnippet] = useState<boolean>(false);
  const [snippetColor, setSnippetColor] = useState<string>("");
  const [snippetEmoji, setSnippetEmoji] = useState<string>("");

  const { hasEditRights } = usePermissionsController({
    brainId,
  });

  const { brain } = useBrainFetcher({
    brainId,
  });

  const settingsTabProps = {
    brainId,
    initialColor: brain?.snippet_color,
    initialEmoji: brain?.snippet_emoji,
  };
  const { handleSubmit, isUpdating, formRef, accessibleModels, setIsUpdating } =
    useSettingsTab(settingsTabProps);

  const promptProps: UsePromptProps = {
    setIsUpdating,
  };

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
            <span className={styles.section_title}>General Information</span>
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
                  className={styles.brain_snippet}
                  style={{ backgroundColor: snippetColor }}
                  onClick={() => {
                    if (!editSnippet) {
                      setEditSnippet(true);
                    }
                  }}
                >
                  <span>{snippetEmoji}</span>
                </div>
                <QuivrButton
                  label="Edit"
                  iconName="edit"
                  color="primary"
                  onClick={() => setEditSnippet(true)}
                  small={true}
                />
              </div>
              <div className={styles.general_information}>
                <GeneralInformation hasEditRights={hasEditRights} />
              </div>
              {(!!brain.integration_description?.allow_model_change ||
                brain.brain_type === "doc") && (
                <div className={styles.model_information}>
                  <ModelSelection
                    accessibleModels={accessibleModels}
                    hasEditRights={hasEditRights}
                    brainId={brainId}
                    handleSubmit={() => handleSubmit()}
                  />
                </div>
              )}
            </div>
            {hasEditRights && (
              <div className={styles.save_button}>
                <QuivrButton
                  label="Save"
                  iconName="upload"
                  color="primary"
                  onClick={() => handleSubmit()}
                />
              </div>
            )}
          </div>
          {hasEditRights && (
            <div className={styles.prompt_wrapper}>
              <span className={styles.section_title}>Prompt</span>
              <MessageInfoBox type="info">
                Select a suggested prompt or create your own for tailored
                interactions
              </MessageInfoBox>
              <Prompt
                usePromptProps={promptProps}
                isUpdatingBrain={isUpdating}
              />
              <div>
                {isUpdating && <FaSpinner className="animate-spin" />}
                {isUpdating && (
                  <span>{t("updatingBrainSettings", { ns: "config" })}</span>
                )}
              </div>
            </div>
          )}
        </div>
      </form>
    </>
  );
};

export const SettingsTab = ({ brainId }: SettingsTabProps): JSX.Element => {
  const methods = useForm<Brain>();

  return (
    <FormProvider {...methods}>
      <SettingsTabContent brainId={brainId} />
    </FormProvider>
  );
};
