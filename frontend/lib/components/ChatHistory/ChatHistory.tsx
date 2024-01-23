import { useTranslation } from "react-i18next";

import { ChatsListItem } from "@/lib/components/ChatsListItem";
import { useChatsContext } from "@/lib/context/ChatsProvider/hooks/useChatsContext";

import {
  isToday,
  isWithinLast30Days,
  isWithinLast7Days,
  isYesterday,
} from "./utils";

import Spinner from "../ui/Spinner";

export const ChatHistory = (): JSX.Element => {
  const { allChats, isLoading } = useChatsContext();
  const { t } = useTranslation("chat");
  const todayChats = allChats.filter((chat) =>
    isToday(new Date(chat.creation_time))
  );
  const yesterdayChats = allChats.filter((chat) =>
    isYesterday(new Date(chat.creation_time))
  );
  const last7DaysChats = allChats.filter((chat) =>
    isWithinLast7Days(new Date(chat.creation_time))
  );
  const last30DaysChats = allChats.filter((chat) =>
    isWithinLast30Days(new Date(chat.creation_time))
  );

  if (isLoading) {
    return (
      <div className="flex justify-center align-center">
        <Spinner />
      </div>
    );
  }

  return (
    <div
      data-testid="chats-list-items"
      className="flex-1 overflow-auto scrollbar h-full"
    >
      {todayChats.length > 0 && (
        <div className="bg-gray-100 text-black rounded-md px-3 py-1 mt-2">
          {t("today")}
        </div>
      )}
      {todayChats.map((chat) => (
        <ChatsListItem key={chat.chat_id} chat={chat} />
      ))}

      {yesterdayChats.length > 0 && (
        <div className="bg-gray-100 text-black rounded-md px-3 py-1 mt-2">
          {t("yesterday")}
        </div>
      )}
      {yesterdayChats.map((chat) => (
        <ChatsListItem key={chat.chat_id} chat={chat} />
      ))}

      {last7DaysChats.length > 0 && (
        <div className="bg-gray-100 text-black rounded-md px-3 py-1 mt-2">
          {t("last7Days")}
        </div>
      )}
      {last7DaysChats.map((chat) => (
        <ChatsListItem key={chat.chat_id} chat={chat} />
      ))}

      {last30DaysChats.length > 0 && (
        <div className="bg-gray-100 text-black rounded-md px-3 py-1 mt-2">
          {t("last30Days")}
        </div>
      )}
      {last30DaysChats.map((chat) => (
        <ChatsListItem key={chat.chat_id} chat={chat} />
      ))}
    </div>
  );
};
