import { UseFormSetValue } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { LuLock, LuUnlock } from "react-icons/lu";

import { BrainConfig, BrainStatus } from "@/lib/types/BrainConfig";

import { BrainAccessRadio } from "./components/BrainAccessRadio";

type BrainAccessProps = {
  status: BrainStatus;
  setValue: UseFormSetValue<BrainConfig>;
};

export const BrainAccess = ({
  status,
  setValue,
}: BrainAccessProps): JSX.Element => {
  const { t } = useTranslation(["brain"]);
  const onSelect = (newStatus: BrainStatus) => () => {
    setValue("status", newStatus);
  };

  return (
    <div className="flex-col grid grid-cols-2 gap-5 w-full">
      <BrainAccessRadio
        label={t("private_brain_label")}
        description={t("private_brain_description")}
        Icon={LuLock}
        onSelect={onSelect("private")}
        isSelected={status === "private"}
      />
      <BrainAccessRadio
        label={t("public_brain_label")}
        description={t("public_brain_description")}
        Icon={LuUnlock}
        onSelect={onSelect("public")}
        isSelected={status === "public"}
      />
    </div>
  );
};
