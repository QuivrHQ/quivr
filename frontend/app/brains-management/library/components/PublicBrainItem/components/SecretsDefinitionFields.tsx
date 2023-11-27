import { Fragment } from "react";
import { UseFormRegister } from "react-hook-form";

import { ApiBrainDefinitionSecret } from "@/lib/api/brain/types";

type SecretsDefinitionFieldsProps = {
  secrets?: ApiBrainDefinitionSecret[];
  register: UseFormRegister<{
    secrets?: Record<string, string>;
  }>;
};

export const SecretsDefinitionFields = ({
  secrets,
  register,
}: SecretsDefinitionFieldsProps): JSX.Element => {
  if (secrets === undefined) {
    return <Fragment />;
  }

  return (
    <div className="mb-3">
      {secrets.map((secret) => (
        <div key={secret.name} className="flex flex-col">
          <div className="flex flex-col">
            <p className="text-sm font-bold mb-1">{secret.name}</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {secret.description}
            </p>
          </div>
          <div className="flex flex-col">
            <input
              type="text"
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              placeholder={secret.description}
              {...register(`secrets.${secret.name}`)}
            />
          </div>
        </div>
      ))}
    </div>
  );
};
