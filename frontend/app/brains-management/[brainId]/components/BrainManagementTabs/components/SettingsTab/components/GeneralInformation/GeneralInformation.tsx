/* eslint max-lines:["error", 110] */
import { UseFormRegister } from "react-hook-form";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import { Chip } from "@/lib/components/ui/Chip";
import Field from "@/lib/components/ui/Field";
import { Radio } from "@/lib/components/ui/Radio";
import { TextArea } from "@/lib/components/ui/TextArea";
import { BrainConfig } from "@/lib/types/brainConfig";

type GeneralInformationProps = {
  register: UseFormRegister<BrainConfig>;
  hasEditRights: boolean;
  isPublicBrain: boolean;
  isOwnedByCurrentUser: boolean;
  isDefaultBrain: boolean;
  isSettingAsDefault: boolean;
  setAsDefaultBrainHandler: () => Promise<void>;
  brainStatusOptions: {
    label: string;
    value: "private" | "public";
  }[];
};

export const GeneralInformation = (
  props: GeneralInformationProps
): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const {
    register,
    hasEditRights,
    isPublicBrain,
    isOwnedByCurrentUser,
    isDefaultBrain,
    isSettingAsDefault,
    setAsDefaultBrainHandler,
    brainStatusOptions,
  } = props;

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 justify-between w-full items-end">
        <div>
          <Field
            label={t("brainName", { ns: "brain" })}
            placeholder={t("brainNamePlaceholder", { ns: "brain" })}
            autoComplete="off"
            className="flex-1"
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
            <div>
              {isDefaultBrain ? (
                <div className="border rounded-lg border-dashed border-black dark:border-white bg-white dark:bg-black text-black dark:text-white focus:bg-black dark:focus:bg-white dark dark focus:text-white dark:focus:text-black transition-colors py-2 px-4 shadow-none">
                  {t("defaultBrain", { ns: "brain" })}
                </div>
              ) : (
                hasEditRights && (
                  <Button
                    variant={"secondary"}
                    isLoading={isSettingAsDefault}
                    onClick={() => void setAsDefaultBrainHandler()}
                    type="button"
                  >
                    {t("setDefaultBrain", { ns: "brain" })}
                  </Button>
                )
              )}
            </div>
          </div>
        </div>
      </div>
      {isOwnedByCurrentUser && (
        <div className="w-full mt-4">
          <Radio
            items={brainStatusOptions}
            label={t("brain_status_label", { ns: "brain" })}
            className="flex-1 justify-between w-[50%]"
            {...register("status")}
          />
        </div>
      )}
      <TextArea
        label={t("brainDescription", { ns: "brain" })}
        placeholder={t("brainDescriptionPlaceholder", { ns: "brain" })}
        autoComplete="off"
        className="flex-1 m-3"
        disabled={!hasEditRights}
        {...register("description")}
      />
    </>
  );
};
