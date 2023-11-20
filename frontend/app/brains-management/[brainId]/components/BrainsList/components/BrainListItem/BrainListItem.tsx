import Link from "next/link";
import { useTranslation } from "react-i18next";
import { CgFileDocument } from "react-icons/cg";

import { Chip } from "@/lib/components/ui/Chip";
import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";
import { getBrainIconFromBrainType } from "@/lib/helpers/getBrainIconFromBrainType";
import { cn } from "@/lib/utils";

import { useBrainListItem } from "./hooks/useBrainListItem";

type BrainsListItemProps = {
  brain: MinimalBrainForUser;
};
export const BrainListItem = ({ brain }: BrainsListItemProps): JSX.Element => {
  const { selected } = useBrainListItem(brain);
  const { t } = useTranslation("brain");

  return (
    <div
      className={cn(
        "w-full min-w-48 border-b border-black/10 dark:border-white/25 last:border-none relative group flex overflow-x-hidden hover:bg-gray-100 dark:hover:bg-gray-800",
        selected
          ? "bg-gray-100 dark:bg-gray-800 text-primary dark:text-white"
          : ""
      )}
      data-testid="brains
      -list-item"
    >
      <Link
        className="flex flex-col flex-1 min-w-0 p-4"
        href={`/brains-management/${brain.id}`}
        key={brain.id}
      >
        <div className="flex flex-row flex-1 w-max">
          <div className="flex items-center gap-2">
            {getBrainIconFromBrainType(brain.brain_type, {
              iconSize: 24,
              DocBrainIcon: CgFileDocument,
            })}
            <p>{brain.name}</p>
          </div>
          {brain.status === "public" && (
            <Chip className="ml-3">{t("public_brain_label")}</Chip>
          )}
        </div>
      </Link>
    </div>
  );
};
