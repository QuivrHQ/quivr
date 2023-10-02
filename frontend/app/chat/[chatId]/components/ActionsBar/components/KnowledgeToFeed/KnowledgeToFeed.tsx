import { useMemo } from "react";
import { useTranslation } from "react-i18next";
import { MdClose } from "react-icons/md";

import { AddBrainModal } from "@/lib/components/AddBrainModal";
import { KnowledgeToFeedInput } from "@/lib/components/KnowledgeToFeedInput";
import Button from "@/lib/components/ui/Button";
import { Select } from "@/lib/components/ui/Select";
import { requiredRolesForUpload } from "@/lib/config/upload";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

import { useFeedBrainInChat } from "./hooks/useFeedBrainInChat";
import { formatMinimalBrainsToSelectComponentInput } from "./utils/formatMinimalBrainsToSelectComponentInput";

type KnowledgeToFeedProps = {
  dispatchHasPendingRequests: () => void;
};
export const KnowledgeToFeed = ({
  dispatchHasPendingRequests,
}: KnowledgeToFeedProps): JSX.Element => {
  const { allBrains, currentBrainId, setCurrentBrainId } = useBrainContext();

  const { t } = useTranslation(["upload"]);

  const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();

  const brainsWithUploadRights = useMemo(
    () =>
      allBrains.filter((brain) => requiredRolesForUpload.includes(brain.role)),
    [allBrains]
  );

  const { feedBrain } = useFeedBrainInChat({
    dispatchHasPendingRequests,
  });

  return (
    <div className="flex-col w-full relative" data-testid="feed-card">
      <div className="flex flex-1 justify-between">
        <AddBrainModal />
        <Button
          variant={"tertiary"}
          onClick={() => setShouldDisplayFeedCard(false)}
        >
          <span>
            <MdClose className="text-3xl" />
          </span>
        </Button>
      </div>
      <div className="flex justify-center">
        <Select
          options={formatMinimalBrainsToSelectComponentInput(
            brainsWithUploadRights
          )}
          emptyLabel={t("selected_brain_select_label")}
          value={currentBrainId ?? undefined}
          onChange={(newSelectedBrainId) =>
            setCurrentBrainId(newSelectedBrainId)
          }
          className="flex flex-row items-center"
        />
      </div>
      <KnowledgeToFeedInput feedBrain={() => void feedBrain()} />
    </div>
  );
};
