import { ReactElement } from "react";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";

interface Props {
  handleSubmit: (checkDirty: boolean) => Promise<void>;
}
export const SaveButton = ({ handleSubmit }: Props): ReactElement => {
  const { t } = useTranslation(["translation"]);

  return (
    <Button
      variant={"primary"}
      onClick={() => void handleSubmit(true)}
      type="button"
    >
      {t("saveButton")}
    </Button>
  );
};
