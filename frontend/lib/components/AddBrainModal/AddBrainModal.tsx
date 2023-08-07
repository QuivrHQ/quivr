/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable max-lines */
import { useTranslation } from "react-i18next";
import { MdAdd } from "react-icons/md";

import { PublicPrompts } from "@/app/brains-management/[brainId]/components/BrainManagementTabs/components/SettingsTab/components/PublicPrompts";
import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";
import { Modal } from "@/lib/components/ui/Modal";
import {
  freeModels,
  paidModels,
} from "@/lib/context/BrainConfigProvider/types";
import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";

import { useAddBrainModal } from "./hooks/useAddBrainModal";
import { Divider } from "../ui/Divider";
import { TextArea } from "../ui/TextArea";

export const AddBrainModal = (): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const {
    handleSubmit,
    isShareModalOpen,
    setIsShareModalOpen,
    register,
    openAiKey,
    temperature,
    maxTokens,
    model,
    isPending,
    pickPublicPrompt,
  } = useAddBrainModal();

  return (
    <Modal
      Trigger={
        <Button variant={"secondary"}>
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
          {...register("name")}
        />

        <TextArea
          label={t("brainDescription", { ns: "brain" })}
          placeholder={t("brainDescriptionPlaceholder", { ns: "brain" })}
          autoComplete="off"
          className="flex-1 m-3"
          {...register("description")}
        />

        <Field
          label={t("openAiKeyLabel", { ns: "config" })}
          placeholder={t("openAiKeyPlaceholder", { ns: "config" })}
          autoComplete="off"
          className="flex-1"
          {...register("openAiKey")}
        />

        <fieldset className="w-full flex flex-col">
          <label className="flex-1 text-sm" htmlFor="model">
            {t("modelLabel", { ns: "config" })}
          </label>
          <select
            id="model"
            {...register("model")}
            className="px-5 py-2 dark:bg-gray-700 bg-gray-200 rounded-md"
          >
            {(openAiKey !== undefined ? paidModels : freeModels).map(
              (availableModel) => (
                <option value={availableModel} key={availableModel}>
                  {availableModel}
                </option>
              )
            )}
          </select>
        </fieldset>

        <fieldset className="w-full flex mt-4">
          <label className="flex-1" htmlFor="temp">
            {t("temperature", { ns: "config" })}: {temperature}
          </label>
          <input
            id="temp"
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={temperature}
            {...register("temperature")}
          />
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
            {...register("maxTokens")}
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

        <Button isLoading={isPending} className="mt-12 self-end" type="submit">
          {t("createButton")}
          <MdAdd className="text-xl" />
        </Button>
      </form>
    </Modal>
  );
};
