import { useFieldArray } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { MdAdd } from "react-icons/md";

import Button from "@/lib/components/ui/Button";

import { ParamDefinitionRow } from "./components/ParamDefinitionRow";
import { defaultParamDefinitionRow } from "./config";
import { useParamsDefinition } from "./hooks/useParamsDefinition";

interface ParamsDefinitionProps {
  name: string;
}

const paramsNameStyle = "flex flex-1 justify-center";

export const ParamsDefinition = ({
  name,
}: ParamsDefinitionProps): JSX.Element => {
  const { t } = useTranslation(["brain"]);
  const { control, register } = useParamsDefinition({
    name,
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name,
  });

  return (
    <div>
      <div className="flex flex-1 font-medium">
        <div className="flex flex-1">
          <div className={paramsNameStyle}>{t("api_brain.name")}</div>
          <div className={paramsNameStyle}>{t("api_brain.description")}</div>
          <div className={paramsNameStyle}>{t("api_brain.type")}</div>
          <div className={paramsNameStyle}>{t("api_brain.required")}</div>
        </div>
      </div>
      {fields.map((field, index) => (
        <ParamDefinitionRow
          name={name}
          key={field.id}
          index={index}
          remove={remove}
          register={register}
        />
      ))}
      <div className="flex justify-end mt-3">
        <Button
          type="button"
          onClick={() => {
            append(defaultParamDefinitionRow);
          }}
          className="p-2"
          variant={"secondary"}
        >
          <MdAdd size={20} /> {t("api_brain.addRow")}
        </Button>
      </div>
    </div>
  );
};
