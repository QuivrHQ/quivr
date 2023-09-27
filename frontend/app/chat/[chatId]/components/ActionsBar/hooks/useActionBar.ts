import { useEffect, useState } from "react";

import { useChatContext } from "@/lib/context";

import { checkIfHasPendingRequest } from "../utils/checkIfHasPendingRequest";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useActionBar = () => {
  const [hasPendingRequests, setHasPendingRequests] = useState(false);
  const { notifications } = useChatContext();

  useEffect(() => {
    setHasPendingRequests(checkIfHasPendingRequest(notifications));
  }, [notifications]);

  return {
    hasPendingRequests,
    setHasPendingRequests,
  };
};
