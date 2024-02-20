/* eslint max-lines:["error", 150] */

import { useTranslation } from "react-i18next";

import { ApiRequestDefinition } from "@/lib/components/ApiRequestDefinition";
import { Chip } from "@/lib/components/ui/Chip";
import Field from "@/lib/components/ui/Field";
import { TextArea } from "@/lib/components/ui/TextArea";

import { useBrainFormState } from "../../hooks/useBrainFormState";

type GeneralInformationProps = {
  hasEditRights: boolean;
  isPublicBrain: boolean;
  isOwnedByCurrentUser: boolean;
  isDefaultBrain: boolean;
  isSettingAsDefault: boolean;
  setAsDefaultBrainHandler: () => Promise<void>;
};

export const GeneralInformation = (
  props: GeneralInformationProps
): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const { hasEditRights, isPublicBrain, isOwnedByCurrentUser } = props;
  const { register } = useBrainFormState();

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 justify-between w-full items-end">
        <div>
          <Field
            label={t("brainName", { ns: "brain" })}
            placeholder={t("brainNamePlaceholder", { ns: "brain" })}
            autoComplete="off"
            inputClassName="flex-1 border-0 bg-white"
            required
            disabled={!hasEditRights}
            {...register("name")}
          />
        </div>

        <div className="mt-4">
          <div className="flex flex-1 items-end flex-col">
            {isPublicBrain && !isOwnedByCurrentUser && (
              <Chip className="mb-3 bg-primary text-white w-full">
                {t("brain:public_brain_label")}
              </Chip>
            )}
          </div>
        </div>
      </div>
      <TextArea
        label={t("brainDescription", { ns: "brain" })}
        placeholder={t("brainDescriptionPlaceholder", { ns: "brain" })}
        autoComplete="off"
        className="flex-1 m-3"
        inputClassName="border-0 bg-white min-h-[100px]"
        disabled={!hasEditRights}
        {...register("description")}
      />

      <ApiRequestDefinition />
    </>
  );
};
