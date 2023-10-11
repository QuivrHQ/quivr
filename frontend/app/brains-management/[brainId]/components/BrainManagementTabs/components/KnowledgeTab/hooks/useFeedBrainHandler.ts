import { UUID } from "crypto";

import { useKnowledgeToFeedInput } from "@/lib/components/KnowledgeToFeedInput/hooks/useKnowledgeToFeedInput.ts";
import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { useKnowledgeToFeed } from "./useKnowledgeToFeed";

type FeedBrainProps = {
  brainId: UUID;
  chatId: UUID;
};
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFeedBrainHandler = () => {
  const { files, urls } = useKnowledgeToFeed();
  const { crawlWebsiteHandler, uploadFileHandler } = useKnowledgeToFeedInput();
  const { updateOnboarding, onboarding } = useOnboarding();

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
