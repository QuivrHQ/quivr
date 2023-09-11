import { NotificationDisplayer } from "./components";
import { Notification } from "../../../../types";

type NotificationProps = {
  content: Notification[];
};

export const ChatNotification = ({
  content,
}: NotificationProps): JSX.Element => {
  console.log({ content });

  return (
    <div className="flex flex-col flex-1 p-3 rounded-xl bg-blue-50 max-w-[50%]">
      {content.map((notification) => (
        <NotificationDisplayer key={notification.id} content={notification} />
      ))}
    </div>
  );
};
