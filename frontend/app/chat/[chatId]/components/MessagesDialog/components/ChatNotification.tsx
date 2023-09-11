import { Fragment } from "react";
import { BsFiletypePdf } from "react-icons/bs";

import { Notification } from "../../../types";
type NotificationProps = {
  content: Notification;
};

type NotificationMessage = {
  message: string;
  type: "warning" | "error" | "success";
};

export const ChatNotification = ({
  content,
}: NotificationProps): JSX.Element => {
  if (content.message === undefined || content.message === null) {
    return <Fragment />;
  }

  console.log("content.message", content.message);
  const notificationType = JSON.parse(
    content.message.replace(/'/g, '"')
  ) as NotificationMessage;

  const backgroundColor = {
    warning: "bg-yellow-50",
    error: "bg-red-50",
    success: "bg-green-50",
  };

  return (
    <div
      className={`flex flex-row gap-1 p-3 rounded-md ${
        backgroundColor[notificationType.type]
      }`}
    >
      <BsFiletypePdf className="text-2xl" />
      <span className="text-sm">{notificationType.message}</span>
    </div>
  );
};
