import { useTranslation } from "react-i18next";

import { MenuButton } from "../MenuButton/MenuButton";

export const CreateBrainButton = (): JSX.Element => {
  const { t } = useTranslation("brain");

  return <MenuButton iconName="brain" label={t("createBrain")} type="add" />;
};
