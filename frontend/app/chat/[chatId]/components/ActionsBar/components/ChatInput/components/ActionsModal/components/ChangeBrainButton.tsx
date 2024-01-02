import { useTranslation } from "react-i18next";
import { TbExchange } from "react-icons/tb";

import Button from "@/lib/components/ui/Button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/lib/components/ui/Popover";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { getBrainIconFromBrainType } from "@/lib/helpers/getBrainIconFromBrainType";
import { cn } from "@/lib/utils";

export const ChangeBrainButton = (): JSX.Element => {
  const { t } = useTranslation("chat");
  const { allBrains, setCurrentBrainId, currentBrainId } = useBrainContext();

  return (
    <Popover>
      <PopoverTrigger>
        <div className="flex items-center justify-center mt-4">
          <Button
            variant="tertiary"
            className="text-primary bg-secondary px-10 py-1"
          >
            <TbExchange />
            {t("change_brain")}
          </Button>
        </div>
      </PopoverTrigger>
      <PopoverContent
        align="center"
        className="min-h-[200px] w-[250px] max-h-[500px] overflow-auto"
      >
        {allBrains.map((brain) => (
          <div
            key={brain.id}
            className="flex items-center justify-between px-1 py-2"
          >
            <Button
              variant={"tertiary"}
              className={cn(
                "px-0 py-0",
                currentBrainId === brain.id ? "text-primary" : ""
              )}
              onClick={() => setCurrentBrainId(brain.id)}
            >
              {getBrainIconFromBrainType(brain.brain_type, {
                iconSize: 24,
              })}
              <span>{brain.name}</span>
            </Button>
          </div>
        ))}
      </PopoverContent>
    </Popover>
  );
};
