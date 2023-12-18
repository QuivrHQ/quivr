/* eslint max-lines:["error", 135] */

import { UUID } from "crypto";
import { FormProvider, useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { FaSpinner } from "react-icons/fa";

import { Divider } from "@/lib/components/ui/Divider";
import { Brain } from "@/lib/context/BrainProvider/types";

import { GeneralInformation, ModelSelection, Prompt } from "./components";
import { AccessConfirmationModal } from "./components/PrivateAccessConfirmationModal/AccessConfirmationModal";
import { useAccessConfirmationModal } from "./components/PrivateAccessConfirmationModal/hooks/useAccessConfirmationModal";
import { usePermissionsController } from "./hooks/usePermissionsController";
import { UsePromptProps } from "./hooks/usePrompt";
import { useSettingsTab } from "./hooks/useSettingsTab";

type SettingsTabProps = {
  brainId: UUID;
};

// eslint-disable-next-line complexity
export const SettingsTabContent = ({
  brainId,
}: SettingsTabProps): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const {
    handleSubmit,
    setAsDefaultBrainHandler,
    isSettingAsDefault,
    isUpdating,
    isDefaultBrain,
    formRef,
    accessibleModels,
    setIsUpdating,
  } = useSettingsTab({ brainId });

  const promptProps: UsePromptProps = {
    setIsUpdating,
  };

  const { onCancel, isAccessModalOpened, closeModal } =
    useAccessConfirmationModal();

  const { hasEditRights, isOwnedByCurrentUser, isPublicBrain } =
    usePermissionsController({
      brainId,
    });

  return (
    <>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          void handleSubmit();
        }}
        className="mb-10 mt-5 flex flex-col items-center gap-2"
        ref={formRef}
      >
        <GeneralInformation
          hasEditRights={hasEditRights}
          isDefaultBrain={isDefaultBrain}
          isOwnedByCurrentUser={isOwnedByCurrentUser}
          isPublicBrain={isPublicBrain}
          isSettingAsDefault={isSettingAsDefault}
          setAsDefaultBrainHandler={setAsDefaultBrainHandler}
        />
        <Divider
          textClassName="font-semibold text-black w-full mx-1"
          separatorClassName="w-full"
          className="w-full my-10"
          text={t("modelSection", { ns: "config" })}
        />
        <ModelSelection
          accessibleModels={accessibleModels}
          hasEditRights={hasEditRights}
          brainId={brainId}
          handleSubmit={handleSubmit}
        />
        <Divider text={t("customPromptSection", { ns: "config" })} />
        <Prompt
          usePromptProps={promptProps}
          isUpdatingBrain={isUpdating}
          hasEditRights={hasEditRights}
        />
        <div className="flex flex-row justify-end flex-1 w-full mt-8">
          {isUpdating && <FaSpinner className="animate-spin" />}
          {isUpdating && (
            <span className="ml-2 text-sm">
              {t("updatingBrainSettings", { ns: "config" })}
            </span>
          )}
        </div>
      </form>
      <AccessConfirmationModal
        opened={isAccessModalOpened}
        onClose={onCancel}
        onCancel={onCancel}
        onConfirm={closeModal}
      />
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
