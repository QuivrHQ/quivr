import { usePathname } from "next/navigation";
import { Fragment } from "react";
import { MdClose } from "react-icons/md";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";

import Button from "@/lib/components/ui/Button";
import { nonProtectedPaths } from "@/lib/config/routesConfig";

import { useNotificationBanner } from "./hooks/useNotificationBanner";

export const NotificationBanner = (): JSX.Element => {
  const { notificationBanner, isDismissed, dismissNotification } =
    useNotificationBanner();
  const pathname = usePathname() ?? "";

  if (
    isDismissed ||
    notificationBanner === undefined ||
    nonProtectedPaths.includes(pathname)
  ) {
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
      <ReactMarkdown
        rehypePlugins={[
          //@ts-expect-error bad typing from rehype-raw
          rehypeRaw,
        ]}
      >
        {notificationBanner.text}
      </ReactMarkdown>
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
