// "use client";
import { useParams, usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSharedChat = () => {
  const pathname = usePathname();
  const [isCopied, setIsCopied] = useState(false);
  const [isShareChatModalOpen, setIsShareChatModalOpen] = useState(false);
  const [isGeneratingShareId, setIsGeneratingShareId] = useState(false);
  const [chatShareURL, setChatShareURL] = useState<string>("");
  const { getShareChatId } = useChatApi();
  const params = useParams();
  const { publish } = useToast();

  const handleGetShareURL = async () => {
    setIsGeneratingShareId(true);

    const chatId = !Array.isArray(params?.chatId) ? params?.chatId ?? "" : "";
    try {
      const res = await getShareChatId(chatId);

      // eslint-disable-next-line @typescript-eslint/strict-boolean-expressions
      if (res.id) {
        const BASE_URL = `${location.origin}`;
        const shareURL = `${BASE_URL}/shared/chat/${res.id}`;
        setChatShareURL(shareURL);
      }
    } catch (e) {
      publish({
        variant: "danger",
        text: JSON.stringify(e),
      });
    } finally {
      setIsGeneratingShareId(false);
    }
  };

  const handleCopy = () => {
    if ((pathname ?? "") === "") {
      return;
    }

    // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
    navigator.clipboard.writeText(chatShareURL).then(
      () => {
        setIsCopied(true);
      },
      (err) => console.error("Failed to copy!", err)
    );
    setTimeout(() => setIsCopied(false), 2000); // Reset after 2 seconds
  };

  useEffect(() => {
    if (isShareChatModalOpen) {
      void handleGetShareURL();
    }
  }, [isShareChatModalOpen]);

  return {
    isCopied,
    handleCopy,
    isShareChatModalOpen,
    setIsShareChatModalOpen,
    chatShareURL,
    isGeneratingShareId,
  };
};
