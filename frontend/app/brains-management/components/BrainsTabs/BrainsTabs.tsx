import { useTranslation } from "react-i18next";

import Spinner from "@/lib/components/ui/Spinner";
import { Tabs, TabsContent, TabsList } from "@/lib/components/ui/Tabs";

import { BrainSearchBar } from "./components/BrainSearchBar";
import { BrainsList } from "./components/BrainsList";
import { useBrainsTabs } from "./hooks/useBrainsTabs";
import { StyledTabsTrigger } from "../StyledTabsTrigger";

export const BrainsTabs = (): JSX.Element => {
  const { t } = useTranslation(["brain", "translation"]);
  const {
    searchQuery,
    isFetchingBrains,
    setSearchQuery,
    brains,
    privateBrains,
    publicBrains,
  } = useBrainsTabs();

  if (isFetchingBrains && brains.length === 0) {
    return (
      <div className="flex w-full h-full justify-center items-center">
        <Spinner />
      </div>
    );
  }

  return (
    <Tabs defaultValue="all" className="flex flex-col">
      <TabsList className="flex flex-row justify-start gap-2 border-b-2 rounded-none pb-3">
        <StyledTabsTrigger value="all">
          {t("translation:all")}
        </StyledTabsTrigger>
        <StyledTabsTrigger value="private" className="capitalize">
          {t("private_brain_label")}
        </StyledTabsTrigger>
        <StyledTabsTrigger value="public" className="capitalize">
          {t("public_brain_label")}
        </StyledTabsTrigger>
        <div className="w-full flex justify-end">
          <BrainSearchBar
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
          />
        </div>
      </TabsList>
      <TabsContent value="all">
        <BrainsList brains={brains} />
      </TabsContent>
      <TabsContent value="private">
        <BrainsList brains={privateBrains} />
      </TabsContent>
      <TabsContent value="public">
        <BrainsList brains={publicBrains} />
      </TabsContent>
    </Tabs>
  );
};
