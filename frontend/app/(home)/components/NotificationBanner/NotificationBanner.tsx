import { Fragment } from "react";
import { MdClose } from "react-icons/md";
import ReactMarkdown from "react-markdown";

import Button from "@/lib/components/ui/Button";

import { useNotificationBanner } from "./hooks/useNotificationBanner";

export const NotificationBanner = (): JSX.Element => {
  const { notificationBanner, isDismissed, dismissNotification } =
    useNotificationBanner();

  if (isDismissed || notificationBanner === undefined) {
    return <Fragment />;
  }

  return (
    <div
      style={{
        position: "relative",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        ...notificationBanner.style,
      }}
    >
      <ReactMarkdown>{notificationBanner.text}</ReactMarkdown>
      {Boolean(notificationBanner.dismissible) && (
        <Button
          variant="tertiary"
          onClick={dismissNotification}
          className="right-2 p-0 absolute bg-white hover:bg-gray-300"
        >
          <MdClose size={20} />
        </Button>
      )}
    </div>
  );
};
