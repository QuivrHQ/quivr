/* eslint-disable max-lines */

import { useTranslation } from "react-i18next";
import { MdAdd } from "react-icons/md";

import { PublicPrompts } from "@/app/brains-management/[brainId]/components/BrainManagementTabs/components/SettingsTab/components/PublicPrompts";
import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";
import { Modal } from "@/lib/components/ui/Modal";
import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";
import { cn } from "@/lib/utils";

import { PublicAccessConfirmationModal } from "./components/PublicAccessConfirmationModal";
import { useAddBrainConfig } from "./hooks/useAddBrainConfig";
import { useAddBrainConfigLabels } from "./hooks/useAddBrainConfigLabels";
import { ApiRequestDefinition } from "../../../ApiRequestDefinition";
import { Divider } from "../../../ui/Divider";
import { Radio } from "../../../ui/Radio";
import { TextArea } from "../../../ui/TextArea";

type AddBrainConfigProps = {
  triggerClassName?: string;
};

export const AddBrainConfig = ({
  triggerClassName,
}: AddBrainConfigProps): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);

  const {
    isShareModalOpen,
    setIsShareModalOpen,
    maxTokens,
    model,
    isPending,
    pickPublicPrompt,
    accessibleModels,
    isPublicAccessConfirmationModalOpened,
    onCancelPublicAccess,
    onConfirmPublicAccess,
    register,
    handleSubmit,
  } = useAddBrainConfig();

  const { brainStatusOptions, knowledgeSourceOptions } =
    useAddBrainConfigLabels();

  return (
    <>
      <Modal
        Trigger={
          <Button
            onClick={() => void 0}
            variant={"tertiary"}
            className={cn("border-0", triggerClassName)}
            data-testid="add-brain-button"
          >
            {t("newBrain", { ns: "brain" })}
            <MdAdd className="text-xl" />
          </Button>
        }
        title={t("newBrainTitle", { ns: "brain" })}
        desc={t("newBrainSubtitle", { ns: "brain" })}
        isOpen={isShareModalOpen}
        setOpen={setIsShareModalOpen}
        CloseTrigger={<div />}
      >
        <form
          onSubmit={(e) => {
            e.preventDefault();
            void handleSubmit();
          }}
          className="my-10 flex flex-col items-center gap-2"
        >
          <Field
            label={t("brainName", { ns: "brain" })}
            autoFocus
            placeholder={t("brainNamePlaceholder", { ns: "brain" })}
            autoComplete="off"
            className="flex-1"
            required
            data-testid="brain-name"
            {...register("name")}
          />

          <TextArea
            label={t("brainDescription", { ns: "brain" })}
            placeholder={t("brainDescriptionPlaceholder", { ns: "brain" })}
            autoComplete="off"
            className="flex-1 m-3"
            {...register("description")}
          />
          <fieldset className="w-full flex flex-col">
            <Radio
              items={brainStatusOptions}
              label={t("brain_status_label", { ns: "brain" })}
              className="flex-1 justify-between w-[50%]"
              {...register("status")}
            />
          </fieldset>
          
            <>
              <fieldset className="w-full flex flex-col">
                <Radio
                  items={knowledgeSourceOptions}
                  label={t("knowledge_source_label", { ns: "brain" })}
                  className="flex-1 justify-between w-[50%]"
                  {...register("brain_type")}
                />
              </fieldset>
              <ApiRequestDefinition />
            </>
          

          <fieldset className="w-full flex flex-col">
            <label className="flex-1 text-sm" htmlFor="model">
              {t("modelLabel", { ns: "config" })}
            </label>
            <select
              id="model"
              {...register("model")}
              className="px-5 py-2 dark:bg-gray-700 bg-gray-200 rounded-md"
            >
              {accessibleModels.map((availableModel) => (
                <option value={availableModel} key={availableModel}>
                  {availableModel}
                </option>
              ))}
            </select>
          </fieldset>

          
          <fieldset className="w-full flex mt-4">
            <label className="flex-1" htmlFor="tokens">
              {t("maxTokens", { ns: "config" })}: {maxTokens}
            </label>
            <input
              type="range"
              min="10"
              max={defineMaxTokens(model)}
              value={maxTokens}
              {...register("max_tokens")}
            />
          </fieldset>
          <Divider text={t("customPromptSection", { ns: "config" })} />
          <PublicPrompts onSelect={pickPublicPrompt} />
          <Field
            label={t("promptName", { ns: "config" })}
            placeholder={t("promptNamePlaceholder", { ns: "config" })}
            autoComplete="off"
            className="flex-1"
            {...register("prompt.title")}
          />
          <TextArea
            label={t("promptContent", { ns: "config" })}
            placeholder={t("promptContentPlaceholder", { ns: "config" })}
            autoComplete="off"
            className="flex-1"
            {...register("prompt.content")}
          />
          <div className="flex flex-row justify-start w-full mt-4">
            <label className="flex items-center">
              <span className="mr-2 text-gray-700">
                {t("setDefaultBrain", { ns: "brain" })}
              </span>
              <input
                type="checkbox"
                {...register("setDefault")}
                className="form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-400"
              />
            </label>
          </div>

          <Button
            isLoading={isPending}
            className="mt-12 self-end"
            type="submit"
            data-testid="create-brain-submit-button"
          >
            {t("createButton")}
            <MdAdd className="text-xl" />
          </Button>
        </form>
      </Modal>
      <PublicAccessConfirmationModal
        opened={isPublicAccessConfirmationModalOpened}
        onClose={onCancelPublicAccess}
        onCancel={onCancelPublicAccess}
        onConfirm={onConfirmPublicAccess}
      />
    </>
  );
};
