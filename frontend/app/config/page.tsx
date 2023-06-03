"use client";
import { redirect } from "next/navigation";

import {
  anthropicModels,
  models,
} from "@/lib/context/BrainConfigProvider/types";
import Button from "../components/ui/Button";
import Field from "../components/ui/Field";
import { useSupabase } from "../supabase-provider";
import { useConfig } from "./hooks/useConfig";

export default function ExplorePage() {
  const { session } = useSupabase();
  const {
    handleSubmit,
    isDirty,
    maxTokens,
    saveConfig,
    register,
    temperature,
    model,
    resetBrainConfig,
  } = useConfig();

  if (session === null) {
    redirect("/login");
  }

  return (
    <main className="min-h-screen w-full flex flex-col">
      <section className="w-full outline-none pt-32 flex flex-col gap-5 items-center justify-center p-6">
        <div className="flex flex-col items-center justify-center">
          <h1 className="text-3xl font-bold text-center">Configuration</h1>
          <h2 className="opacity-50 text-center">
            Here, you can choose your model, set your credentials...
          </h2>
        </div>
        <form
          className="flex flex-col gap-5 py-5 w-full max-w-xl"
          onSubmit={handleSubmit(saveConfig)}
        >
          <div className="border-b border-gray-300 mt-8 mb-8">
            <p className="text-center text-gray-600 uppercase tracking-wide font-semibold">
              Model config
            </p>
          </div>
          <Field
            type="text"
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
              {models.map((model) => (
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
              max="3000"
              step="1"
              value={maxTokens}
              {...register("maxTokens")}
            />
          </fieldset>
          <div className="border-b border-gray-300 mt-8 mb-8">
            <p className="text-center text-gray-600 uppercase tracking-wide font-semibold">
              Backend config
            </p>
          </div>
          <Field
            type="text"
            placeholder="Backend URL"
            className="w-full"
            label="Backend URL"
            {...register("backendUrl")}
          />
          <Field
            type="text"
            placeholder="Supabase URL"
            className="w-full"
            label="Supabase URL"
            {...register("supabaseUrl")}
          />
          <Field
            type="text"
            placeholder="Supabase key"
            className="w-full"
            label="Supabase key"
            {...register("supabaseKey")}
          />
          <label className="flex items-center">
            <input
              type="checkbox"
              checked
              name="keepLocal"
              onChange={() => alert("Coming soon")}
              className="form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-400"
            />
            <span className="ml-2 text-gray-700">Keep in local</span>
          </label>
          <div className="flex justify-between">
            <Button
              variant="danger"
              className="self-end"
              type="button"
              onClick={resetBrainConfig}
            >
              Reset
            </Button>
            <Button
              disabled={!isDirty}
              variant="secondary"
              className="self-end"
            >
              Done
            </Button>
          </div>
        </form>
      </section>
    </main>
  );
}
