import { Content, Root } from "@radix-ui/react-tabs";

import { KnowledgeSource } from "@/lib/types/brainConfig";

import { useApiDefinitionTabs } from "./hooks/useApiDefinitionTabs";
import { HeadersDefinition } from "./tabs/HeadersDefinition";
import { ParamsDefinition } from "./tabs/ParamsDefinition";
import { SearchParamsDefinition } from "./tabs/SearchParamsDefinition";
export const ApiRequestDefinition = (knowledgeSource: {
  knowledgeSource: KnowledgeSource;
}): JSX.Element => {
  const { selectedTab, setSelectedTab } = useApiDefinitionTabs();
  console.log(knowledgeSource);

  setSelectedTab("searchParams");

  return (
    <>
      <Root
        className="flex flex-col w-full h-full overflow-scroll bg-white dark:bg-black p-4 md:p-10 max-w-5xl"
        value={selectedTab}
      >
        <div className="flex gap-2 p-4">
          <select
            className="block w-32 px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            defaultValue="GET"
            // {...register("api.method")}
          >
            <option value="GET">GET</option>
            <option value="POST">POST</option>
            <option value="PUT">PUT</option>
            <option value="DELETE">DELETE</option>
          </select>

          <input
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            placeholder="https://api.example.com/resource"
            // {...register("api.url", { required: true })}
          />
        </div>
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
