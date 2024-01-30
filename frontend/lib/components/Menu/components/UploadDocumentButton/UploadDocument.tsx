import { useTranslation } from "react-i18next";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const UploadDocumentButton = (): JSX.Element => {
  const { t } = useTranslation("upload");

  return <MenuButton iconName="upload" label={t("title")} type="add" />;
};
