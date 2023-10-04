"use client";

import { useTranslation } from "react-i18next";

import Field from "@/lib/components/ui/Field";

import { PublicBrainItem } from "./components/PublicBrainItem/PublicBrainItem";
import { useBrainsLibrary } from "./hooks/useBrainsLibrary";

const BrainsLibrary = (): JSX.Element => {
  const { displayingPublicBrains, searchBarText, setSearchBarText } =
    useBrainsLibrary();
  const { t } = useTranslation("brain");

  return (
    <div className="flex flex-1 flex-col items-center">
      <div className="flex">
        <Field
          value={searchBarText}
          onChange={(e) => setSearchBarText(e.target.value)}
          name="search"
          inputClassName="w-max lg:min-w-[300px] md:min-w-[200px]  min-w-[100px]  mt-10 rounded-3xl bg-white lg:mb-5"
          placeholder={t("public_brains_search_bar_placeholder")}
        />
      </div>

      <div className="flex flex-wrap justify-stretch w-full">
        {displayingPublicBrains.map((brain) => (
          <div key={brain.id} className="lg:w-1/3 md:w-1/2 md:p-5 p-5 w-full">
            <PublicBrainItem brain={brain} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default BrainsLibrary;
