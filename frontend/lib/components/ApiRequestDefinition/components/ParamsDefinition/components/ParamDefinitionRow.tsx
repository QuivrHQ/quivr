import { useFormContext, UseFormRegister } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { MdCancel } from "react-icons/md";

import { ApiDefinitionContextType } from "../../../types";
import { paramsNameStyle } from "../../styles";
import { ParameterDefinition } from "../types";

type ParamControl = {
  [name: string]: ParameterDefinition[];
};

type ParamDefinitionRowProps = {
  register: UseFormRegister<ParamControl>;
  index: number;
  remove: (index: number) => void;
  name: string;
};

export const ParamDefinitionRow = ({
  index,
  remove,
  register,
  name,
}: ParamDefinitionRowProps): JSX.Element => {
  const { t } = useTranslation(["brain"]);
  const { watch } = useFormContext<ApiDefinitionContextType>();
  const isApiDefinitionReadOnly = watch("isApiDefinitionReadOnly") ?? false;

  return (
    <div className="flex flex-1 justify-between items-center py-4 border-b border-gray-300 relative gap-2">
      <div className={paramsNameStyle}>
        <input
          type="text"
          className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block shadow-sm sm:text-sm border-gray-300 dark:bg-gray-800 dark:text-gray-100 rounded-md w-full outline-none"
          placeholder={t("api_brain.name")}
          disabled={isApiDefinitionReadOnly}
          {...register(
            `${name}[${index}].name` as `${typeof name}.${number}.name`
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
            `${name}[${index}].description` as `${typeof name}.${number}.description`
          )}
        />
      </div>
      <div className="flex-1">
        <select
          id={`type-${index}`}
          className="mt-1 block w-full py-2 px-3 border border-gray-300 dark:bg-gray-800 dark:text-gray-100 bg-white dark:border-gray-800 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          disabled={isApiDefinitionReadOnly}
          {...register(
            `${name}[${index}].type` as `${typeof name}.${number}.type`
          )}
        >
          <option value="string">string</option>
          <option value="number">number</option>
        </select>
      </div>
      <div className="flex-1 justify-center flex">
        <input
          type="checkbox"
          className="form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-400 outline-none"
          disabled={isApiDefinitionReadOnly}
          {...register(`${name}[${index}].required`)}
        />
      </div>

      <button
        type="button"
        disabled={isApiDefinitionReadOnly}
        onClick={() => remove(index)}
        className="absolute right-0 text-red-500 bg-transparent border-none cursor-pointer"
      >
        <MdCancel />
      </button>
    </div>
  );
};
