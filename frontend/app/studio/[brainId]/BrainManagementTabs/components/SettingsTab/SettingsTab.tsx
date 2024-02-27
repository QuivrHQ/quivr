import { UUID } from "crypto";
import { FormProvider, useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { FaSpinner } from "react-icons/fa";

import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
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
  const { handleSubmit, isUpdating, formRef, accessibleModels, setIsUpdating } =
    useSettingsTab({ brainId });

  const promptProps: UsePromptProps = {
    setIsUpdating,
  };

  useBrainFormState();

  const { hasEditRights } = usePermissionsController({
    brainId,
  });

  const { brain } = useBrainFetcher({
    brainId,
  });

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
              <div className={styles.general_information}>
                <GeneralInformation hasEditRights={hasEditRights} />
              </div>
              {brain?.brain_type === "doc" && (
                <div className={styles.model_information}>
                  <ModelSelection
                    accessibleModels={accessibleModels}
                    hasEditRights={hasEditRights}
                    brainId={brainId}
                    handleSubmit={handleSubmit}
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
              <MessageInfoBox
                type="info"
                content="Select a suggested prompt or create your own for tailored interactions."
              />
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
