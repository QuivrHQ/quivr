/* eslint-disable */
"use client";

import { UseFormRegister } from "react-hook-form";

import Field from "@/lib/components/ui/Field";
import {
  BrainConfig,
  Model,
  PaidModels,
  anthropicModels,
  models,
  paidModels,
} from "@/lib/context/BrainConfigProvider/types";
import { defineMaxTokens } from "@/lib/helpers/defineMexTokens";

interface ModelConfigProps {
  register: UseFormRegister<BrainConfig>;
  model: Model | PaidModels;
  openAiKey: string | undefined;
  temperature: number;
  maxTokens: number;
}

export const ModelConfig = ({
  register,
  model,
  openAiKey,
  temperature,
  maxTokens,
}: ModelConfigProps): JSX.Element => {
  

  return (
    <>
      <div className="border-b border-gray-300 mt-8 mb-8">
        <p className="text-center text-gray-600 uppercase tracking-wide font-semibold">
          Model config
        </p>
      </div>
      <Field
        type="password"
        placeholder="Open AI Key"
        className="w-full"
        label="Open AI Key"
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
          {(openAiKey ? paidModels : models).map((model) => (
            <option value={model} key={model}>
              {model}
            </option>
          ))}
        </select>
      </fieldset>
      {(anthropicModels as readonly string[]).includes(model) && (
        <Field
          type="text"
          placeholder="Anthropic API Key"
          className="w-full"
          label="Anthropic API Key"
          {...register("anthropicKey")}
        />
      )}
      <fieldset className="w-full flex">
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
      <fieldset className="w-full flex">
        <label className="flex-1" htmlFor="tokens">
          Tokens: {maxTokens}
        </label>
        <input
          type="range"
          min="256"
          max={defineMaxTokens(model)}
          step="32"
          value={maxTokens}
          {...register("maxTokens")}
        />
      </fieldset>
    </>
  );
};
