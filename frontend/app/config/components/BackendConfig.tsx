/* eslint-disable */
"use client";

import { UseFormRegister } from "react-hook-form";

import Field from "@/lib/components/ui/Field";
import { BrainConfig } from "@/lib/context/BrainConfigProvider/types";

interface BackendConfigProps {
  register: UseFormRegister<BrainConfig>;
}

export const BackendConfig = ({
  register,
}: BackendConfigProps): JSX.Element => {
  return (
    <>
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
    </>
  );
};
