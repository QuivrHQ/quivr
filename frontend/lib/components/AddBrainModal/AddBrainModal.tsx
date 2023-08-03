/* eslint-disable max-lines */
import { MdAdd } from "react-icons/md";

import { PublicPrompts } from "@/app/brains-management/[brainId]/components/BrainManagementTabs/components/SettingsTab/components/PublicPrompts";
import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";
import { Modal } from "@/lib/components/ui/Modal";
import { models, paidModels } from "@/lib/context/BrainConfigProvider/types";
import { defineMaxTokens } from "@/lib/helpers/defineMexTokens";

import { useAddBrainModal } from "./hooks/useAddBrainModal";
import { Divider } from "../ui/Divider";
import { TextArea } from "../ui/TextArea";

export const AddBrainModal = (): JSX.Element => {
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
          Add New Brain
          <MdAdd className="text-xl" />
        </Button>
      }
      title="Add Brain"
      desc="Create a new brain to start aggregating content"
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
          label="Enter a brain name"
          autoFocus
          placeholder="E.g. History notes"
          autoComplete="off"
          className="flex-1"
          {...register("name")}
        />

        <TextArea
          label="Enter a brain description"
          placeholder="My new brain is about..."
          autoComplete="off"
          className="flex-1 m-3"
          {...register("description")}
        />

        <Field
          label="OpenAI API Key"
          placeholder="sk-xxx"
          autoComplete="off"
          className="flex-1"
          {...register("openAiKey")}
        />

        <fieldset className="w-full flex flex-col">
          <label className="flex-1 text-sm" htmlFor="model">
            Model
          </label>
          <select
            id="model"
            {...register("model")}
            className="px-5 py-2 dark:bg-gray-700 bg-gray-200 rounded-md"
          >
            {(openAiKey !== undefined ? paidModels : models).map(
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
            Temperature: {temperature}
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
            Max tokens: {maxTokens}
          </label>
          <input
            type="range"
            min="10"
            max={defineMaxTokens(model)}
            value={maxTokens}
            {...register("maxTokens")}
          />
        </fieldset>
        <Divider text="Custom prompt" />
        <PublicPrompts onSelect={pickPublicPrompt} />
        <Field
          label="Prompt title"
          placeholder="My awesome prompt name"
          autoComplete="off"
          className="flex-1"
          {...register("prompt.title")}
        />
        <TextArea
          label="Prompt content"
          placeholder="As an AI, your..."
          autoComplete="off"
          className="flex-1"
          {...register("prompt.content")}
        />
        <div className="flex flex-row justify-start w-full mt-4">
          <label className="flex items-center">
            <span className="mr-2 text-gray-700">Set as default brain</span>
            <input
              type="checkbox"
              {...register("setDefault")}
              className="form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-400"
            />
          </label>
        </div>

        <Button isLoading={isPending} className="mt-12 self-end" type="submit">
          Create
          <MdAdd className="text-xl" />
        </Button>
      </form>
    </Modal>
  );
};
