import { Content, Root } from "@radix-ui/react-tabs";
import { Fragment, useEffect } from "react";
import { useFormContext } from "react-hook-form";

import { allowedRequestMethods, CreateBrainInput } from "@/lib/api/brain/types";

import { useApiRequestDefinition } from "./hooks/useApiRequestDefinition";
import { HeadersDefinition } from "./tabs/HeadersDefinition";
import { ParamsDefinition } from "./tabs/ParamsDefinition";
import { SearchParamsDefinition } from "./tabs/SearchParamsDefinition";

export const ApiRequestDefinition = (): JSX.Element => {
  const { selectedTab, setSelectedTab } = useApiRequestDefinition();

  const { watch, register } = useFormContext<CreateBrainInput>();

  useEffect(() => {
    setSelectedTab("searchParams");
  }, [setSelectedTab]);

  const brainType = watch("brain_type");

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
          {...register("api_brain_definition.method")}
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
          {...register("api_brain_definition.url", { required: true })}
        />
      </div>
      <Root
        className="flex flex-col w-full h-full overflow-scroll bg-white dark:bg-black p-4 md:p-10 max-w-5xl"
        value={selectedTab}
      >
        <div className="flex-1 md:pt-0 pb-0">
          <Content value="people">
            <SearchParamsDefinition />
          </Content>
          <Content value="settings">
            <HeadersDefinition />
          </Content>
          <Content value="knowledge">
            <ParamsDefinition />
          </Content>
        </div>
      </Root>
    </>
  );
};
