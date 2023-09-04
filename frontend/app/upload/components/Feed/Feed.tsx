import { useTranslation } from "react-i18next";

import { Divider } from "@/lib/components/ui/Divider";

import { Crawler } from "./components/Crawler";
import { FileUploader } from "./components/FileUploader";

export const Feed = (): JSX.Element => {
  const { t } = useTranslation(["translation"]);

  return (
    <>
      <FileUploader />
      <Divider text={t("or")} className="m-5" />
      <Crawler />
    </>
  );
};
