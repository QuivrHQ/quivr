/* eslint-disable max-lines */

import { UUID } from "crypto";
import { FaSpinner } from "react-icons/fa";

import Button from "@/lib/components/ui/Button";
import { Divider } from "@/lib/components/ui/Divider";
import Field from "@/lib/components/ui/Field";
import { TextArea } from "@/lib/components/ui/TextArea";
import { models, paidModels } from "@/lib/context/BrainConfigProvider/types";
import { defineMaxTokens } from "@/lib/helpers/defineMexTokens";

import { PublicPrompts } from "./components/PublicPrompts";
import { useSettingsTab } from "./hooks/useSettingsTab";

type SettingsTabProps = {
  brainId: UUID;
};

export const SettingsTab = ({ brainId }: SettingsTabProps): JSX.Element => {
  const {
    handleSubmit,
    register,
    openAiKey,
    temperature,
    maxTokens,
    model,
    setAsDefaultBrainHandler,
    isSettingAsDefault,
    isUpdating,
    isDefaultBrain,
    formRef,
    promptId,
    pickPublicPrompt,
    removeBrainPrompt,
  } = useSettingsTab({ brainId });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        void handleSubmit();
      }}
      className="my-10 mb-0 flex flex-col items-center gap-2"
      ref={formRef}
    >
      <div className="flex flex-row flex-1 justify-between w-full">
        <div>
          <Field
            label="Name"
            placeholder="E.g. History notes"
            autoComplete="off"
            className="flex-1"
            {...register("name")}
          />
        </div>
        <div className="mt-4">
          {isDefaultBrain ? (
            <div className="border rounded-lg border-dashed border-black dark:border-white bg-white dark:bg-black text-black dark:text-white focus:bg-black dark:focus:bg-white dark dark focus:text-white dark:focus:text-black transition-colors py-2 px-4 shadow-none">
              Default brain
            </div>
          ) : (
            <Button
              variant={"secondary"}
              isLoading={isSettingAsDefault}
              onClick={() => void setAsDefaultBrainHandler()}
              type="button"
            >
              Set as default brain
            </Button>
          )}
        </div>
      </div>
      <TextArea
        label="Description"
        placeholder="My new brain is about..."
        autoComplete="off"
        className="flex-1 m-3"
        {...register("description")}
      />
      <Divider text="Model config" />
      <Field
        label="OpenAI API Key"
        placeholder="sk-xxx"
        autoComplete="off"
        className="flex-1"
        {...register("openAiKey")}
      />
      <fieldset className="w-full flex flex-col mt-2">
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
      {promptId !== "" && (
        <Button disabled={isUpdating} onClick={() => void removeBrainPrompt()}>
          Remove prompt
        </Button>
      )}
      <div className="flex flex-row justify-end flex-1 w-full mt-8">
        {isUpdating && <FaSpinner className="animate-spin" />}
        {isUpdating && (
          <span className="ml-2 text-sm">Updating brain settings...</span>
        )}
      </div>
    </form>
  );
};
