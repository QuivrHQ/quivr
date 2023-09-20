import { ReactElement } from "react";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";

interface Props extends React.ComponentProps<typeof Button> {
  handleSubmit: (checkDirty: boolean) => Promise<void>;
}
export const SaveButton = ({ handleSubmit, ...props }: Props): ReactElement => {
  const { t } = useTranslation(["translation"]);

  return (
    <Button
      variant={"primary"}
      onClick={() => void handleSubmit(true)}
      type="button"
      {...props}
    >
      {t("saveButton")}
    </Button>
  );
};
