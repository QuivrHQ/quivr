import { Content, List, Root } from "@radix-ui/react-tabs";
import { Fragment } from "react";
import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { allowedRequestMethods } from "@/lib/api/brain/types";

import { BrainDefinitionTabTrigger } from "./components/BrainDefinitionTabTrigger";
import { ParamsDefinition } from "./components/ParamsDefinition/ParamsDefinition";
import { SecretsDefinition } from "./components/SecretsDefinition/SecretsDefinition";
import { useApiRequestDefinition } from "./hooks/useApiRequestDefinition";
import { ApiDefinitionContextType } from "./types";

export const ApiRequestDefinition = (): JSX.Element => {
  const { selectedTab, setSelectedTab } = useApiRequestDefinition();
  const { t } = useTranslation(["external_api_definition"]);

  const { watch, register } = useFormContext<ApiDefinitionContextType>();

  const brainType = watch("brain_type");
  const readOnly = watch("isApiDefinitionReadOnly") ?? false;

  if (brainType !== "api") {
    return <Fragment />;
  }

  const allowedMethodsOptions = allowedRequestMethods.map((method) => ({
    label: method,
    value: method,
  }));

  return (
    <>
      <div className="flex gap-2 w-full">
        <select
          className="block w-32 px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          defaultValue="GET"
          disabled={readOnly}
          {...register("brain_definition.method")}
        >
          {allowedMethodsOptions.map(({ label, value }) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>

        <input
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          placeholder="https://api.example.com/resource"
          disabled={readOnly}
          {...register("brain_definition.url", { required: true })}
        />
      </div>
      <Root
        className="flex flex-col w-full h-full overflow-scroll bg-white dark:bg-black py-4 md:py-10 max-w-5xl"
        value={selectedTab}
      >
        <List className="flex flex-col md:flex-row justify-between space-y-2 md:space-y-0">
          <BrainDefinitionTabTrigger
            value="params"
            label={t("params")}
            selected={selectedTab === "params"}
            onChange={setSelectedTab}
          />
          <BrainDefinitionTabTrigger
            value="searchParams"
            label={t("searchParams")}
            selected={selectedTab === "searchParams"}
            onChange={setSelectedTab}
          />
          <BrainDefinitionTabTrigger
            value="secrets"
            label={t("secrets")}
            selected={selectedTab === "secrets"}
            onChange={setSelectedTab}
          />
        </List>
        <div className="flex-1 md:pt-0 pb-0">
          <Content value="params">
            <ParamsDefinition
              description={t("paramsTabDescription")}
              name="params"
            />
          </Content>
          <Content value="searchParams">
            <ParamsDefinition
              description={t("searchParamsTabDescription")}
              name="search_params"
            />
          </Content>
          <Content value="secrets">
            <SecretsDefinition />
          </Content>
        </div>
      </Root>
    </>
  );
};
