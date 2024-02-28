"use client";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { useToast } from "@/lib/hooks";
import { useUrlBrain } from "@/lib/hooks/useBrainIdFromUrl";
import { Knowledge } from "@/lib/types/Knowledge";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

import { useKnowledge } from "../../../hooks/useKnowledge";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeItem = () => {
  const { deleteKnowledge } = useKnowledgeApi();
  const [isDeleting, setIsDeleting] = useState(false);
  const { publish } = useToast();
  const { track } = useEventTracking();
  const { brainId, brain } = useUrlBrain();
  const { invalidateKnowledgeDataKey } = useKnowledge({
    brainId,
  });

  const { t } = useTranslation(["translation", "explore"]);

  const onDeleteKnowledge = async (knowledge: Knowledge) => {
    setIsDeleting(true);
    void track("DELETE_DOCUMENT");
    const knowledge_name =
      "fileName" in knowledge ? knowledge.fileName : knowledge.url;
    try {
      if (brainId === undefined) {
        throw new Error(t("noBrain", { ns: "explore" }));
      }
      await deleteKnowledge({
        brainId,
        knowledgeId: knowledge.id,
      });

      invalidateKnowledgeDataKey();

      publish({
        variant: "success",
        text: t("deleted", {
          fileName: knowledge_name,
          brain: brain?.name,
          ns: "explore",
        }),
      });
    } catch (error) {
      publish({
        variant: "warning",
        text: t("errorDeleting", { fileName: knowledge_name, ns: "explore" }),
      });
      console.error("Error deleting", error);
    }
    setIsDeleting(false);
  };

  return {
    isDeleting,
    onDeleteKnowledge,
  };
};
