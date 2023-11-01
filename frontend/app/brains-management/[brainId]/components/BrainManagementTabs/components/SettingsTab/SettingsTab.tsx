/* eslint max-lines:["error", 135] */

import { UUID } from "crypto";
import { useTranslation } from "react-i18next";
import { FaSpinner } from "react-icons/fa";

import { Divider } from "@/lib/components/ui/Divider";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { GeneralInformation, ModelSelection, Prompt } from "./components";
import { AccessConfirmationModal } from "./components/PrivateAccessConfirmationModal/AccessConfirmationModal";
import { useAccessConfirmationModal } from "./components/PrivateAccessConfirmationModal/hooks/useAccessConfirmationModal";
import { useSettingsTab } from "./hooks/useSettingsTab";
import { getBrainPermissions } from "../../utils/getBrainPermissions";


type SettingsTabProps = {
  brainId: UUID;
};

// eslint-disable-next-line complexity
export const SettingsTab = ({ brainId }: SettingsTabProps): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const {
    handleSubmit,
    register,
    temperature,
    maxTokens,
    model,
    setAsDefaultBrainHandler,
    isSettingAsDefault,
    isUpdating,
    isDefaultBrain,
    formRef,
    accessibleModels,
    brainStatusOptions,
    status,
    setValue,
    dirtyFields,
    resetField,
    setIsUpdating,
    promptId,
    getValues,
    reset,
    updateFormValues,
  } = useSettingsTab({ brainId });

  const promptProps = {
    brainId,
    getValues,
    promptId,
    register,
    reset,
    setValue,
    resetField,
    updateFormValues,
    dirtyFields,
    setIsUpdating,
  };

  const { onCancel, isAccessModalOpened, closeModal } =
    useAccessConfirmationModal({
      status,
      setValue,
      isStatusDirty: Boolean(dirtyFields.status),
      resetField,
    });

  const { allBrains } = useBrainContext();

  const { hasEditRights, isOwnedByCurrentUser, isPublicBrain } =
    getBrainPermissions({
      brainId,
      userAccessibleBrains: allBrains,
    });

  return (
    <>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          void handleSubmit(true);
        }}
        className="my-10 mb-0 flex flex-col items-center gap-2"
        ref={formRef}
      >
        <GeneralInformation
          brainStatusOptions={brainStatusOptions}
          hasEditRights={hasEditRights}
          isDefaultBrain={isDefaultBrain}
          isOwnedByCurrentUser={isOwnedByCurrentUser}
          isPublicBrain={isPublicBrain}
          isSettingAsDefault={isSettingAsDefault}
          register={register}
          setAsDefaultBrainHandler={setAsDefaultBrainHandler}
        />
        <Divider text={t("modelSection", { ns: "config" })} />
        <ModelSelection
          accessibleModels={accessibleModels}
          model={model}
          maxTokens={maxTokens}
          temperature={temperature}
          register={register}
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
        selectedStatus={status}
      />
    </>
  );
};
