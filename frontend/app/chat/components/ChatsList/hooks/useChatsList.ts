import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useChatsContext } from "@/lib/context/ChatsProvider/hooks/useChatsContext";
import { useToast } from "@/lib/hooks";
import { useDevice } from "@/lib/hooks/useDevice";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatsList = () => {
  const { isMobile } = useDevice();
  const [open, setOpen] = useState(!isMobile);

  const pathname = usePathname();

  const { setAllChats } = useChatsContext();
  const { publish } = useToast();
  const { getChats } = useChatApi();

  useEffect(() => {
    const fetchAllChats = async () => {
      try {
        const response = await getChats();
        setAllChats(response.reverse());
      } catch (error) {
        console.error(error);
        publish({
          variant: "danger",
          text: "Error occurred while fetching your chats",
        });
      }
    };
    void fetchAllChats();
  }, []);

  useEffect(() => {
    setOpen(!isMobile);
  }, [isMobile, pathname]);

  return {
    open,
    setOpen,
  };
};
