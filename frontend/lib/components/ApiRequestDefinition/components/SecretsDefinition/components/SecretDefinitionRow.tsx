import { useFormContext, UseFormRegister } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { MdCancel } from "react-icons/md";

import { ApiDefinitionContextType } from "../../../types";
import { paramsNameStyle } from "../../styles";
import { brainSecretsSchemaDefinitionKeyInForm } from "../config";
import { SecretDefinition } from "../types";

type SecretControl = {
  [brainSecretsSchemaDefinitionKeyInForm]: SecretDefinition[];
};

type SecretDefinitionRowProps = {
  register: UseFormRegister<SecretControl>;
  index: number;
  remove: (index: number) => void;
};

export const SecretDefinitionRow = ({
  index,
  remove,
  register,
}: SecretDefinitionRowProps): JSX.Element => {
  const { t } = useTranslation(["brain"]);
  const { watch } = useFormContext<ApiDefinitionContextType>();
  const isApiDefinitionReadOnly = watch("isApiDefinitionReadOnly") ?? false;
  const isUpdatingApiDefinition = watch("isUpdatingApiDefinition") ?? false;

  return (
    <div className="flex flex-1 justify-between items-center py-4 border-b border-gray-300 relative gap-2">
      <div className={paramsNameStyle}>
        <input
          type="text"
          className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block shadow-sm sm:text-sm border-gray-300 dark:bg-gray-800 dark:text-gray-100 rounded-md w-full outline-none"
          placeholder={t("api_brain.name")}
          disabled={isApiDefinitionReadOnly}
          {...register(
            `${brainSecretsSchemaDefinitionKeyInForm}.${index}.name`
          )}
        />
      </div>
      <div className="flex-1">
        <input
          type="text"
          id={`description-${index}`}
          className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 dark:bg-gray-800 dark:text-gray-100 rounded-md outline-none"
          placeholder={t("api_brain.description")}
          disabled={isApiDefinitionReadOnly}
          {...register(
            `${brainSecretsSchemaDefinitionKeyInForm}.${index}.description`
          )}
        />
      </div>
      <div className="flex-1">
        <select
          id={`type-${index}`}
          className="mt-1 block w-full py-2 px-3 border border-gray-300 dark:bg-gray-800 dark:text-gray-100 bg-white dark:border-gray-800 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          disabled={isApiDefinitionReadOnly}
          {...register(
            `${brainSecretsSchemaDefinitionKeyInForm}.${index}.type`
          )}
        >
          <option value="string">string</option>
          <option value="number">number</option>
        </select>
      </div>
      {!isUpdatingApiDefinition && (
        <div className={paramsNameStyle}>
          <input
            type="text"
            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 dark:bg-gray-800 dark:text-gray-100 rounded-md outline-none"
            placeholder={t("api_brain.value")}
            {...register(
              `${brainSecretsSchemaDefinitionKeyInForm}.${index}.value`
            )}
          />
        </div>
      )}

      <button
        type="button"
        onClick={() => remove(index)}
        disabled={isApiDefinitionReadOnly}
        className="absolute right-0 text-red-500 bg-transparent border-none cursor-pointer"
      >
        <MdCancel />
      </button>
    </div>
  );
};
