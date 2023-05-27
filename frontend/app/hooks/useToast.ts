import { Message } from "postcss";
import { useEffect, useRef, useState } from "react";
import { ToastRef } from "../components/ui/Toast";

export const useToast = () => {
  const [message, setMessage] = useState<Message | null>(null);
  const messageToast = useRef<ToastRef>(null);

  useEffect(() => {
    if (!message) return;
    messageToast.current?.publish({
      variant:
        message.type === "error"
          ? "danger"
          : message.type === "warning"
          ? "neutral"
          : "success",
      text: message.text,
    });
  }, [message]);
  return {
    setMessage,
    messageToast,
  };
};
