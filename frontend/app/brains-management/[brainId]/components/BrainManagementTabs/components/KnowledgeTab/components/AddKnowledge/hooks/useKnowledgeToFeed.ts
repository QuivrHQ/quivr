import {
  FeedItemCrawlType,
  FeedItemUploadType,
} from "@/app/chat/[chatId]/components/ActionsBar/types";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

type UseKnowledgeToFeed = {
  files: File[];
  urls: string[];
};
export const useKnowledgeToFeed = (): UseKnowledgeToFeed => {
  const { knowledgeToFeed } = useKnowledgeToFeedContext();

  const files: File[] = (
    knowledgeToFeed.filter((c) => c.source === "upload") as FeedItemUploadType[]
  ).map((c) => c.file);

  const urls: string[] = (
    knowledgeToFeed.filter((c) => c.source === "crawl") as FeedItemCrawlType[]
  ).map((c) => c.url);

  return {
    files,
    urls,
  };
};
