import Link from "next/link";
import { useMemo } from "react";
import { useTranslation } from "react-i18next";

import { ApiBrainSecretsInputs } from "@/lib/components/ApiBrainSecretsInputs/ApiBrainSecretsInputs";
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

  const { t } = useTranslation(["upload", "brain"]);

  const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();
  const { currentBrainDetails } = useBrainContext();
  const brainsWithUploadRights = useMemo(
    () =>
      allBrains.filter((brain) => requiredRolesForUpload.includes(brain.role)),
    [allBrains]
  );

  const { feedBrain } = useFeedBrainInChat({
    dispatchHasPendingRequests,
  });

  return (
    <div className="flex-col w-full relative pt-3" data-testid="feed-card">
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
      {currentBrainDetails?.brain_type === "api" ? (
        <ApiBrainSecretsInputs
          brainId={currentBrainDetails.id}
          onUpdate={() => setShouldDisplayFeedCard(false)}
        />
      ) : (
        <KnowledgeToFeedInput feedBrain={() => void feedBrain()} />
      )}
      {Boolean(currentBrainId) && (
        <Link href={`/studio/${currentBrainId ?? ""}`}>
          <Button variant={"tertiary"}>
            {t("manage_brain", { ns: "brain" })}
          </Button>
        </Link>
      )}
    </div>
  );
};
