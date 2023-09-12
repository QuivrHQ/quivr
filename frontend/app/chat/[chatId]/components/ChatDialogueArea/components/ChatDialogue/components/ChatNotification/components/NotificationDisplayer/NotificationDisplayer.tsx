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

  const { message, status, name } = JSON.parse(
    nonParsedMessage.replace(/'/g, '"')
  ) as NotificationMessage;

  return (
    <>
      <div
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className="flex flex-row flex-1 gap-1 p-3 rounded-md items-center"
      >
        <span className="text-gray-400 mb-1 text-2xl">
          {notificationStatusToIcon[status]}
        </span>
        <div className=" flex flex-row rounded-md bg-white p-3 flex-1">
          <div className="flex flex-row items-center gap-1">
            <div className="bg-gray-200 p-1 rounded-md items-center justify-center flex">
              {action === "CRAWL" ? <MdLink /> : getFileIcon(name)}
            </div>
            <span className="text-md flex flex-1">{name}</span>
          </div>
        </div>
      </div>
      <div>{isHovered ? <div>{message}</div> : <div></div>}</div>
    </>
  );
};
