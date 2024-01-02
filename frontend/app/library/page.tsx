"use client";

import { useTranslation } from "react-i18next";
import { LuGlobe, LuSearch } from "react-icons/lu";

import Field from "@/lib/components/ui/Field";
import Spinner from "@/lib/components/ui/Spinner";

import { PublicBrainItem } from "./components/PublicBrainItem/PublicBrainItem";
import { useBrainsLibrary } from "./hooks/useBrainsLibrary";

const BrainsLibrary = (): JSX.Element => {
  const { displayingPublicBrains, searchBarText, setSearchBarText, isLoading } =
    useBrainsLibrary();
  const { t } = useTranslation(["brain", "translation"]);

  return (
    <div className="w-full p-10 px-4 md:px-10 overflow-auto">
      <div className="flex flex-row items-center justify-center gap-2 w-full">
        <LuGlobe className="text-primary" size={30} />
        <span className="font-semibold text-3xl">
          {t("translation:Explore")}
        </span>
      </div>
      <div className="flex justify-center md:justify-end w-full mt-3">
        <div>
          <Field
            value={searchBarText}
            onChange={(e) => setSearchBarText(e.target.value)}
            name="search"
            inputClassName="w-max lg:min-w-[300px] md:min-w-[200px] min-w-[100px] rounded-3xl bg-white border-none"
            placeholder={t("brain:public_brains_search_bar_placeholder")}
            icon={<LuSearch className="text-primary" size={20} />}
          />
        </div>
      </div>
      <div className="flex flex-row items-center justify-center gap-2 w-full mt-3">
        <p className="font-normal text-2xl text-center">
          {t("brain:explore_brains")}
        </p>
        <div className="flex"></div>
      </div>
      <div className="flex flex-1 flex-col items-center justify-center">
        {isLoading && (
          <div className="flex justify-center items-center flex-1">
            <Spinner className="text-4xl" />
          </div>
        )}

        <div className="w-full lg:grid-cols-4 md:grid-cols-3 grid mt-5 gap-3 items-stretch">
          {displayingPublicBrains.map((brain) => (
            <div key={brain.id} className="h-[180px]">
              <PublicBrainItem brain={brain} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BrainsLibrary;
