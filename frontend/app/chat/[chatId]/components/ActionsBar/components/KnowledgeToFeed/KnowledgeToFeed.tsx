import { useMemo } from "react";
import { useTranslation } from "react-i18next";
import { MdClose } from "react-icons/md";

import { AddBrainModal } from "@/lib/components/AddBrainModal";
import { KnowledgeToFeedInput } from "@/lib/components/KnowledgeToFeedInput";
import Button from "@/lib/components/ui/Button";
import { Select } from "@/lib/components/ui/Select";
import { requiredRolesForUpload } from "@/lib/config/upload";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { useFeedBrainInChat } from "./hooks/useFeedBrainInChat";
import { formatMinimalBrainsToSelectComponentInput } from "./utils/formatMinimalBrainsToSelectComponentInput";

type KnowledgeToFeedProps = {
  closeFeedInput: () => void;
  dispatchHasPendingRequests?: () => void;
};
export const KnowledgeToFeed = ({
  closeFeedInput,
  dispatchHasPendingRequests,
}: KnowledgeToFeedProps): JSX.Element => {
  const { allBrains, currentBrainId, setCurrentBrainId } = useBrainContext();

  const { t } = useTranslation(["upload"]);

  const brainsWithUploadRights = useMemo(
    () =>
      allBrains.filter((brain) => requiredRolesForUpload.includes(brain.role)),
    [allBrains]
  );

  const { feedBrain } = useFeedBrainInChat({
    dispatchHasPendingRequests,
    closeFeedInput,
  });

  return (
    <div className="flex-col w-full relative">
      <div className="flex flex-1 justify-between">
        <AddBrainModal />
        <Button variant={"tertiary"} onClick={closeFeedInput}>
          <span>
            <MdClose className="text-3xl" />
          </span>
        </Button>
      </div>
      <div className="flex justify-center">
        <Select
          label={t("selected_brain_select_label")}
          options={formatMinimalBrainsToSelectComponentInput(
            brainsWithUploadRights
          )}
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
