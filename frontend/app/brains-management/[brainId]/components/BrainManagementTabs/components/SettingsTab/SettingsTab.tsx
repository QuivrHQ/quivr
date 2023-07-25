/* eslint-disable max-lines */

import { UUID } from "crypto";

import Button from "@/lib/components/ui/Button";
import { Divider } from "@/lib/components/ui/Divider";
import Field from "@/lib/components/ui/Field";
import { TextArea } from "@/lib/components/ui/TextField";
import { models, paidModels } from "@/lib/context/BrainConfigProvider/types";
import { defineMaxTokens } from "@/lib/helpers/defineMexTokens";

import { ApiKeyConfig } from "./components";
import { useSettingsTab } from "./hooks/useSettingsTab";

type SettingsTabProps = {
  brainId: UUID;
};

export const SettingsTab = ({ brainId }: SettingsTabProps): JSX.Element => {
  const {
    handleSubmit,
    register,
    hasChanges,
    openAiKey,
    temperature,
    maxTokens,
    model,
    setAsDefaultBrainHandler,
    isSettingAsDefault,
    isUpdating,
  } = useSettingsTab({ brainId });

  return (
    <form
      onSubmit={(e) => void handleSubmit(e)}
      className="my-10 mb-0 flex flex-col items-center gap-2"
    >
      <Field
        label="Name"
        placeholder="E.g. History notes"
        autoComplete="off"
        className="flex-1"
        {...register("name")}
      />
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
      <div className="flex flex-row justify-end flex-1 w-full mt-8">
        <Button isLoading={isUpdating} disabled={!hasChanges}>
          Save changes
        </Button>
      </div>
      <Divider text="Default brain" className="mt-4" />
      <Button
        variant={"secondary"}
        isLoading={isSettingAsDefault}
        onClick={() => void setAsDefaultBrainHandler()}
      >
        Set as default brain
      </Button>

      <ApiKeyConfig />
    </form>
  );
};
