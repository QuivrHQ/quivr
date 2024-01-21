import Link from "next/link";
import { useTranslation } from "react-i18next";
import { CgFileDocument } from "react-icons/cg";
import { LuChevronRightCircle } from "react-icons/lu";

import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";
import { getBrainIconFromBrainType } from "@/lib/helpers/getBrainIconFromBrainType";

type BrainItemProps = {
  brain: MinimalBrainForUser;
};

export const BrainItem = ({ brain }: BrainItemProps): JSX.Element => {
  const { t } = useTranslation("brain");

  const isBrainDescriptionEmpty = brain.description === "";
  const brainDescription = isBrainDescriptionEmpty
    ? t("empty_brain_description")
    : brain.description;

  return (
    <div className="flex justify-center items-center flex-col flex-1 w-full h-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl overflow-hidden dark:bg-black border border-black/10 dark:border-white/25 pb-2 bg-secondary">
      <div className="w-full">
        <div className="w-full py-2 flex gap-2 justify-center items-center bg-primary bg-opacity-40 px-2">
          {getBrainIconFromBrainType(brain.brain_type, {
            iconSize: 24,
            DocBrainIcon: CgFileDocument,
            iconClassName: "text-primary",
          })}
          <span className="line-clamp-1 mr-2 font-semibold text-md">
            {brain.name}
          </span>
        </div>
      </div>
      <div className="flex-1 py-2">
        <p
          className={`line-clamp-2 text-center px-5 ${
            isBrainDescriptionEmpty && "text-gray-400"
          }`}
        >
          {brainDescription}
        </p>
      </div>
      <div className="w-full px-2">
        <Link
          href={`/brains-management/${brain.id}`}
          className="px-8 py-3 flex items-center justify-center gap-2 bg-white text-primary rounded-lg border-0 w-content mt-3 disabled:bg-secondary hover:bg-primary/50 disabled:hover:bg-primary/50 w-full text-md"
        >
          <span>{t("configure")}</span>
          <LuChevronRightCircle className="text-md" />
        </Link>
      </div>
    </div>
  );
};
