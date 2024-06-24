import { UUID } from "crypto";

import { useFromConnectionsContext } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/hooks/useFromConnectionContext";
import { useSync } from "@/lib/api/sync/useSync";
import { useKnowledgeToFeedInput } from "@/lib/components/KnowledgeToFeedInput/hooks/useKnowledgeToFeedInput.ts";
import { useKnowledgeToFeedFilesAndUrls } from "@/lib/hooks/useKnowledgeToFeed";
import { useOnboarding } from "@/lib/hooks/useOnboarding";

type FeedBrainProps = {
  brainId: UUID;
  chatId: UUID;
};
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFeedBrainHandler = () => {
  const { files, urls } = useKnowledgeToFeedFilesAndUrls();
  const { crawlWebsiteHandler, uploadFileHandler } = useKnowledgeToFeedInput();
  const { updateOnboarding, onboarding } = useOnboarding();
  const {
    syncFiles,
    getActiveSyncsForBrain,
    deleteActiveSync,
    updateActiveSync,
  } = useSync();
  const { openedConnections } = useFromConnectionsContext();

  const updateOnboardingA = async () => {
    if (onboarding.onboarding_a) {
      await updateOnboarding({
        onboarding_a: false,
      });
    }
  };

  const handleFeedBrain = async ({
    brainId,
    chatId,
  }: FeedBrainProps): Promise<void> => {
    const uploadPromises = files.map((file) =>
      uploadFileHandler(file, brainId, chatId)
    );
    const crawlPromises = urls.map((url) =>
      crawlWebsiteHandler(url, brainId, chatId)
    );

    const existingConnections = await getActiveSyncsForBrain(brainId);

    await Promise.all(
      openedConnections
        .filter((connection) => connection.selectedFiles.files.length)
        .map(async (openedConnection) => {
          const existingConnectionIds = existingConnections.map(
            (connection) => connection.id
          );
          if (
            !openedConnection.id ||
            !existingConnectionIds.includes(openedConnection.id)
          ) {
            await syncFiles(openedConnection, brainId);
          } else if (!openedConnection.selectedFiles.files.length) {
            await deleteActiveSync(openedConnection.id);
          } else {
            await updateActiveSync(openedConnection);
          }
        })
    );

    await Promise.all([
      ...uploadPromises,
      ...crawlPromises,
      updateOnboardingA(),
    ]);
  };

  return {
    handleFeedBrain,
  };
};
