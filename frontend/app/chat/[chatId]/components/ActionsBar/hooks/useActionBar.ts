import { useEffect, useState } from "react";

import { useChatContext } from "@/lib/context";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

import { checkIfHasPendingRequest } from "../utils/checkIfHasPendingRequest";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useActionBar = () => {
  const [hasPendingRequests, setHasPendingRequests] = useState(false);
  const { notifications } = useChatContext();

  const { shouldDisplayFeedCard } = useKnowledgeToFeedContext();

  useEffect(() => {
    setHasPendingRequests(checkIfHasPendingRequest(notifications));
  }, [notifications]);

  return {
    hasPendingRequests,
    setHasPendingRequests,
    shouldDisplayFeedCard,
  };
};
