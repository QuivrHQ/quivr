import { Fragment } from "react";
import { useTranslation } from "react-i18next";

import { useUrlBrain } from "@/lib/hooks/useBrainIdFromUrl";

export const ApiBrainDefinition = (): JSX.Element => {
  const { brainDetails } = useUrlBrain();
  const { t } = useTranslation(["external_api_definition"]);

  if (brainDetails?.brain_type !== "api") {
    return <Fragment />;
  }

  return (
    <div className="w-full">
      <hr className="border-t border-gray-300 w-full mb-3" />
      <div className="mb-2">
        <p>
          <span className="font-semibold">{t("url_placeholder")}</span>
          <span className="ml-2">{brainDetails.brain_definition?.url}</span>
        </p>
      </div>
      <div className="mb-2">
        <p>
          <span className="font-semibold">{t("method_label")}</span>
          <span className="ml-2">{brainDetails.brain_definition?.method}</span>
        </p>
      </div>
      {(brainDetails.brain_definition?.params.properties.length ?? 0) > 0 && (
        <div className="mb-3">
          <p>
            <span className="font-bold mr-1">{t("params")}:</span>
            <span>{t("paramsTabDescription")}</span>
          </p>
          {brainDetails.brain_definition?.params.properties.map((param) => (
            <div key={param.name}>
              <span className="mr-1">-</span>
              <span className="font-semibold">{param.name}:</span>
              <span className="ml-2">{param.type}</span>
              <span className="ml-2">
                {brainDetails.brain_definition?.params.required.includes(
                  param.name
                ) ?? false
                  ? "- Required"
                  : " - Optional"}
              </span>
            </div>
          ))}
        </div>
      )}
      {(brainDetails.brain_definition?.search_params.properties.length ?? 0) >
        0 && (
        <div className="mb-3">
          <p>
            <span className="font-bold mr-1">{t("searchParams")}:</span>
            <span>{t("searchParamsTabDescription")}</span>
          </p>

          {brainDetails.brain_definition?.search_params.properties.map(
            (param) => (
              <div key={param.name}>
                <span className="mr-1">-</span>
                <span className="font-semibold">{param.name}:</span>
                <span className="ml-2">{param.type}</span>
                <span className="ml-2">
                  {brainDetails.brain_definition?.search_params.required.includes(
                    param.name
                  ) ?? false
                    ? "- Required"
                    : " - Optional"}
                </span>
              </div>
            )
          )}
        </div>
      )}
      {(brainDetails.brain_definition?.secrets?.length ?? 0) > 0 && (
        <div className="mb-3">
          <p>
            <span className="font-bold mr-1">{t("secrets")}:</span>
            <span>{t("secretsTabDescription")}</span>
          </p>
          {brainDetails.brain_definition?.secrets?.map((param) => (
            <div key={param.name}>
              <span className="mr-1">-</span>
              <span className="font-bold">{param.name}:</span>
              <span className="ml-2">{param.type}</span>
            </div>
          ))}
        </div>
      )}
      <hr className="border-t border-gray-300 w-full mt-5" />
    </div>
  );
};
