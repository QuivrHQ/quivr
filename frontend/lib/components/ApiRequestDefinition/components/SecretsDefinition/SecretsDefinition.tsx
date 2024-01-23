import { useFieldArray } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { MdAdd } from "react-icons/md";
import { TiInfoOutline } from "react-icons/ti";

import Button from "@/lib/components/ui/Button";

import { SecretDefinitionRow } from "./components/SecretDefinitionRow";
import {
  brainSecretsSchemaDefinitionKeyInForm,
  defaultSecretDefinitionRow,
} from "./config";
import { useSecretsDefinition } from "./hooks/useSecretsDefinition";

import { tabDescriptionStyle } from "../../styles";

const paramsNameStyle = "flex flex-1 justify-center";

export const SecretsDefinition = (): JSX.Element => {
  const { t } = useTranslation(["brain", "external_api_definition"]);

  const {
    control,
    register,
    isApiDefinitionReadOnly,
    isUpdatingApiDefinition,
  } = useSecretsDefinition();

  const { fields, append, remove } = useFieldArray({
    control,
    name: brainSecretsSchemaDefinitionKeyInForm,
  });

  return (
    <div>
      <div className={tabDescriptionStyle}>
        <TiInfoOutline size={30} />
        <p className="ml-5">
          {t("secretsTabDescription", { ns: "external_api_definition" })}
        </p>
      </div>
      <div className="flex flex-1 font-medium">
        <div className="flex flex-1">
          <div className={paramsNameStyle}>{t("api_brain.name")}</div>
          <div className={paramsNameStyle}>{t("api_brain.description")}</div>
          <div className={paramsNameStyle}>{t("api_brain.type")}</div>
          {!isUpdatingApiDefinition && (
            <div className={paramsNameStyle}>{t("api_brain.value")}</div>
          )}
        </div>
      </div>
      {fields.map((field, index) => (
        <SecretDefinitionRow
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
            append(defaultSecretDefinitionRow);
          }}
          className="p-2"
          disabled={isApiDefinitionReadOnly}
          variant={"secondary"}
        >
          <MdAdd size={20} /> {t("api_brain.addRow")}
        </Button>
      </div>
    </div>
  );
};
