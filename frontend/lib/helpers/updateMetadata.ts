/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import { useEffect } from 'react';
import { useTranslation } from "react-i18next";

export const UpdateMetadata = () => {
  const { t } = useTranslation();

  useEffect(() => {
    const title = t("title");
    const description = t("description");
    document.title = title;
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription instanceof HTMLMetaElement) {
      metaDescription.content = description;
    }
  }, [t]); 

  return null;
};
