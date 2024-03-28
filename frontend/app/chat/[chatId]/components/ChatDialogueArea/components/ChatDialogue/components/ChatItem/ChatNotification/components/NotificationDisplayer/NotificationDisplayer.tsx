import { Fragment, useState } from "react";
import { MdLink } from "react-icons/md";

import { Notification } from "@/app/chat/[chatId]/types";
import { getFileIcon } from "@/lib/helpers/getFileIcon";

import { NotificationMessage, notificationStatusToIcon } from "./types";

type NotificationDisplayerProps = {
  content: Notification;
};

export const NotificationDisplayer = ({
  content,
}: NotificationDisplayerProps): JSX.Element => {
  const { message: nonParsedMessage, action } = content;
  const [isHovered, setIsHovered] = useState(false);

  if (nonParsedMessage === null || nonParsedMessage === undefined) {
    return <Fragment />;
  }

  let message, status, name;

  try {
    const parsedMessage = JSON.parse(
      nonParsedMessage.replace(/'/g, '"')
    ) as NotificationMessage;

    message = parsedMessage.message;
    status = parsedMessage.status;
    name = parsedMessage.name;
  } catch (error) {
    return <Fragment />;
  }

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="relative flex flex-row p-2 gap-1 rounded-sm items-center hover:bg-gray-100 transition duration-300 cursor-pointer"
    >
      <span className="text-gray-400 text-2xl">
        {notificationStatusToIcon[status]}
      </span>
      <div className="flex flex-row bg-white p-2 rounded-sm ml-2">
        <div className="flex flex-row items-center gap-1">
          <div className="bg-gray-100 p-1 rounded-sm items-center justify-center flex">
            {action === "CRAWL" ? <MdLink size={16} /> : getFileIcon(name)}
          </div>
          <span className="text-sm text-gray-600">{name}</span>
        </div>
      </div>
      {isHovered && (
        <div
          className="absolute bg-white p-2 rounded-sm border border-gray-100 shadow-sm transition-transform transform translate-y-1 translate-x-1/4 z-10"
          style={{ bottom: "-10px", right: "10px" }}
        >
          {message}
        </div>
      )}
    </div>
  );
};
