"use client";

/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import { useEffect } from "react";
import { useTranslation } from "react-i18next";

export const UpdateMetadata = () => {
  const { t } = useTranslation("vaccineTruth");

  useEffect(() => {
    const title = t("vaccineTruthAi");
    const description = t("vaccineTruthAi");
    document.title = title;
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription instanceof HTMLMetaElement) {
      metaDescription.content = description;
    }
  }, [t]);

  return null;
};
